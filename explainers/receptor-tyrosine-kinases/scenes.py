"""
Two Together: How Pairing Switches an RTK On
Lesson: Receptor Tyrosine Kinases

COLOUR MAP (one colour per concept for the whole film):
- BG (#0f1117):          Dark slate cellular space (extracellular above membrane, cytoplasm below)
- MEMBRANE (GREY):       Plasma membrane lipid bilayer cross-section & neutral schematic lines
- LIGAND (BLUE):         Extracellular growth factor / ligand (GF, NGF dimer, EGF, Insulin)
- RTK (TEAL):            Receptor chain (ectodomain, dimerization arm, single helix, tyrosine tail; also HER2)
- KINASE_REST (#D9822B): Resting / self-inhibited kinase domain (amber)
- KINASE_ACTIVE (#F5C542): Switched-on active kinase domain (bright gold)
- LOOP (RED):            Activation loop (coral-red brake that plugs the cleft at rest, swings clear when active)
- PHOS (YELLOW):         Phosphate groups (P) and ATP
- HER3_COL (#9B72CF):    HER3 receptor (violet, nearly inactive kinase cleft)
- DISULFIDE (TEXT):      Covalent disulfide bonds (white bars) & high-contrast labels

ONE WORLD, CARRIED:
A cross-section of the grey plasma membrane bilayer spanning the frame horizontally, with teal receptor
tyrosine kinases spanning it (ectodomain outside, single helix through the bilayer, two-lobed amber kinase
and tyrosine tail inside). Wide views show ligands and pairing routes across the membrane; zoomed views
bring the two-lobed kinase cleft and activation loop to full frame height; the ending pulls back to the
same membrane view with the active pair switched on.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s01_hook: Sky-blue growth factor drifts along a bounded arc above the membrane without crossing;
  a highlight travels down the single narrow helix; the first RTK shifts left as a second RTK glides in.
- s02_architecture: Camera/receptor zooms smoothly (`zoom_t` 0->1), highlights each domain in turn,
  unfurls and sways the flexible tail (`tail_unfurl`, `phase`), closes the two kinase lobes (`lobe_close`),
  and folds the coral-red activation loop into the cleft (`loop_open` 0.85->0).
- s03_three_routes: First, a two-part NGF dimer descends onto two ectodomains and pulls both receptors
  inward (`sep` tracker); then ectodomains morph to folded EGFR, outer EGF dots dock, tucked
  dimerization arms swing open (`arm` tracker 0->1), and the arms clasp tip-to-tip while EGF stays apart.
- s04_insulin_route: Morphs into the disulfide-linked insulin receptor with splayed legs (`splay` tracker=1);
  insulin docks into the outer pocket, pivots the inner legs together (`splay` 1->0), and zooms onto
  the two resting kinases side by side.
- s05_trans_activation: Zoomed paired kinases settle together, launch 3+3 yellow phosphates along parabolic
  arcs onto each partner's coral loop (`p_prog`), the loops swing clear of the cleft (`loop_t` 0->1),
  ATP docks into each cleft, the lobes close (`lobe_t`), and both kinases brighten to active gold.
- s06_egfr_asymmetry: Two EGFR kinases with bare coral loops shift into a lopsided pair (`press_t` 0->1)
  where the left large lobe physically presses the right small lobe; only the right kinase snaps open to gold.
- s07_predict: Highlights the pressing surface, replaces left kinase with violet hatched HER3 facing amber
  HER2, and drifts both receptors smoothly closer while the question card appears in the bottom band.
- s09_reveal_and_rule: Question card clears immediately as HER3 presses its large lobe onto HER2's small
  lobe (`press_t` 0->1) and HER2 snaps open to active gold; both activation modes appear below the rule.
- s10_close: A lone helix twists slightly without waking its kinase; then the three pairing routes cycle
  sequentially into the side-by-side pair, opening both kinases progressively into active gold.
"""

import numpy as np
from bp_parts import *

# Concept colours
MEMBRANE = GREY
LIGAND = BLUE
RTK = TEAL
KINASE_REST = "#D9822B"
KINASE_ACTIVE = "#F5C542"
LOOP = RED
PHOS = YELLOW
HER3_COL = "#9B72CF"
DISULFIDE = TEXT


# ------------------------------------------------------------------ shared schematic builders
def make_membrane(y=0.45, width=13.6, thickness=0.64):
    """Horizontal plasma membrane bilayer cross-section."""
    band = Rectangle(
        width=width, height=thickness,
        fill_color=MEMBRANE, fill_opacity=0.32, stroke_width=0
    ).move_to([0, y, 0])
    top = Line([-width / 2, y + thickness / 2, 0], [width / 2, y + thickness / 2, 0],
               color=MEMBRANE, stroke_width=3.8)
    bot = Line([-width / 2, y - thickness / 2, 0], [width / 2, y - thickness / 2, 0],
               color=MEMBRANE, stroke_width=3.8)
    ticks = VGroup()
    xs = np.linspace(-width / 2 + 0.25, width / 2 - 0.25, 42)
    for x in xs:
        ticks.add(Line([x, y - thickness * 0.36, 0], [x, y + thickness * 0.36, 0],
                       color=MEMBRANE, stroke_width=1.6, stroke_opacity=0.46))
    g = VGroup(band, ticks, top, bot)
    g.y_center = y
    g.y_top = y + thickness / 2
    g.y_bot = y - thickness / 2
    return g


def make_helix(x, y_top, y_bot, color=RTK, width=0.25, tilt=0.0):
    """Single transmembrane helix spanning the bilayer."""
    h = max(0.2, y_top - y_bot)
    bar = RoundedRectangle(
        corner_radius=min(0.08, width / 2), width=width, height=h,
        color=color, stroke_width=3.4, fill_color=color, fill_opacity=0.42
    )
    stripes = VGroup()
    n_stripes = 4
    for i in range(n_stripes):
        yy = -h * 0.34 + i * (h * 0.68 / max(1, n_stripes - 1))
        stripes.add(Line(
            [-width * 0.42, yy - 0.05, 0], [width * 0.42, yy + 0.05, 0],
            color=color, stroke_width=2.2, stroke_opacity=0.88
        ))
    g = VGroup(bar, stripes).move_to([x, (y_top + y_bot) / 2, 0])
    if abs(tilt) > 1e-4:
        g.rotate(tilt, about_point=[x, y_top, 0])
    return g


def make_ectodomain_cup(x, y_bot, color=RTK, scale=1.0, fill_op=0.34):
    """Schematic U-shaped ectodomain that catches a growth factor."""
    pts = [
        [-0.25, 0.0, 0], [-0.65, 0.56, 0], [-0.68, 1.44, 0], [-0.36, 1.50, 0],
        [-0.25, 0.74, 0], [0.25, 0.74, 0], [0.36, 1.50, 0], [0.68, 1.44, 0],
        [0.65, 0.56, 0], [0.25, 0.0, 0],
    ]
    poly = Polygon(*pts, color=color, stroke_width=4.0, fill_color=color, fill_opacity=fill_op)
    poly.round_corners(0.08)
    poly.scale(scale).move_to([x, y_bot + poly.height * scale / 2, 0])
    poly.shift(UP * (y_bot - poly.get_bottom()[1]))
    return poly


def make_egfr_ectodomain(x, y_bot, facing=1, arm_open=0.0, color=RTK, scale=1.0):
    """EGFR-style ectodomain with an articulated dimerization arm that clasps tip-to-tip when open."""
    stem = RoundedRectangle(
        corner_radius=0.08, width=0.42 * scale, height=0.66 * scale,
        color=color, stroke_width=3.6, fill_color=color, fill_opacity=0.34
    ).move_to([x, y_bot + 0.33 * scale, 0])

    head = RoundedRectangle(
        corner_radius=0.14, width=0.66 * scale, height=0.90 * scale,
        color=color, stroke_width=3.8, fill_color=color, fill_opacity=0.34
    )
    head_pivot = np.array([x, y_bot + 0.58 * scale, 0])
    head.move_to(head_pivot + UP * 0.44 * scale + LEFT * facing * 0.14 * scale * (1 - arm_open))
    head.rotate(facing * 0.22 * (1 - arm_open), about_point=head_pivot)

    arm = RoundedRectangle(
        corner_radius=0.06, width=0.98 * scale, height=0.18 * scale,
        color=color, stroke_width=3.4, fill_color=color, fill_opacity=0.56
    )
    arm_pivot = np.array([x + facing * 0.14 * scale, y_bot + 0.84 * scale, 0])
    arm.move_to(arm_pivot + RIGHT * facing * 0.48 * scale)
    arm.rotate(-facing * 1.32 * (1 - arm_open), about_point=arm_pivot)

    g = VGroup(stem, head, arm)
    g.egf_anchor = head.get_center() + LEFT * facing * 0.36 * scale
    g.arm_tip = arm.get_right() if facing > 0 else arm.get_left()
    return g


def make_kinase_domain(
    center,
    color=KINASE_REST,
    loop_color=LOOP,
    tail_color=RTK,
    facing=1,
    loop_open=0.0,
    lobe_close=0.0,
    active=False,
    hatched=False,
    tail_phase=0.0,
    tail_unfurl=1.0,
    show_tail=True,
    tail_scale=1.0,
    scale=1.0,
):
    """Two-lobed schematic kinase domain with hinged small/large lobes, activation loop, and tail."""
    c = np.array(center, dtype=float)
    fill_op = 0.54 if active else 0.34
    sw = 5.0 if active else 3.8

    small_w, small_h = 1.28 * scale, 0.66 * scale
    large_w, large_h = 1.52 * scale, 0.98 * scale

    large = RoundedRectangle(
        corner_radius=0.16 * scale, width=large_w, height=large_h,
        color=color, stroke_width=sw, fill_color=color, fill_opacity=fill_op
    ).move_to(c + DOWN * 0.42 * scale)

    hinge = c + LEFT * facing * 0.44 * scale + UP * 0.16 * scale
    small = RoundedRectangle(
        corner_radius=0.14 * scale, width=small_w, height=small_h,
        color=color, stroke_width=sw, fill_color=color, fill_opacity=fill_op
    ).move_to(c + UP * (0.52 - 0.08 * lobe_close) * scale + LEFT * facing * 0.10 * scale)
    small.rotate(-facing * 0.15 * lobe_close, about_point=hinge)

    spine = RoundedRectangle(
        corner_radius=0.08 * scale, width=0.38 * scale, height=0.74 * scale,
        color=color, stroke_width=0, fill_color=color, fill_opacity=0.45 if active else 0.30
    ).move_to(c + LEFT * facing * 0.48 * scale + UP * 0.08 * scale)

    cleft_pt = c + RIGHT * facing * 0.36 * scale + UP * 0.08 * scale

    loop_anchor = c + RIGHT * facing * 0.32 * scale + DOWN * 0.24 * scale
    loop_pts = [
        loop_anchor,
        loop_anchor + UP * 0.48 * scale + LEFT * facing * 0.08 * scale,
        loop_anchor + UP * 0.58 * scale + RIGHT * facing * 0.22 * scale,
        loop_anchor + UP * 0.28 * scale + RIGHT * facing * 0.36 * scale,
        loop_anchor + RIGHT * facing * 0.16 * scale,
    ]
    loop = VMobject(color=loop_color, stroke_width=6.4 * scale, fill_opacity=0)
    loop.set_points_smoothly([np.array(p) for p in loop_pts])
    loop.rotate(-facing * 1.88 * loop_open, about_point=loop_anchor)

    hatch = VGroup()
    if hatched:
        for k in range(-2, 3):
            p0 = cleft_pt + np.array([-0.24 * scale, (k * 0.11 - 0.08) * scale, 0])
            p1 = cleft_pt + np.array([0.24 * scale, (k * 0.11 + 0.08) * scale, 0])
            hatch.add(Line(p0, p1, color=GREY, stroke_width=2.8 * scale))

    tail_grp = VGroup()
    if show_tail:
        ts = scale * tail_scale * (0.35 + 0.65 * tail_unfurl)
        t0 = large.get_bottom() + LEFT * facing * 0.12 * scale
        s1 = 0.24 * np.sin(tail_phase) * ts
        s2 = 0.28 * np.cos(tail_phase + 0.8) * ts
        t1 = t0 + DOWN * 0.36 * ts + RIGHT * (facing * 0.16 * ts + s1)
        t2 = t0 + DOWN * 0.74 * ts + RIGHT * (-facing * 0.10 * ts + s2)
        t3 = t0 + DOWN * 1.08 * ts + RIGHT * (facing * 0.14 * ts - s1 * 0.6)
        tail_curve = VMobject(color=tail_color, stroke_width=4.0 * scale)
        tail_curve.set_points_smoothly([t0, t1, t2, t3])
        tail_grp.add(tail_curve)
        for frac in (0.38, 0.66, 0.92):
            pt = tail_curve.point_from_proportion(frac)
            tail_grp.add(Dot(pt, radius=0.075 * scale, color=tail_color))

    g = VGroup(spine, large, small, hatch, loop, tail_grp)
    g.small_lobe = small
    g.large_lobe = large
    g.cleft_pt = cleft_pt
    g.loop = loop
    g.loop_tip = loop.point_from_proportion(0.5)
    g.tail = tail_grp
    g.top_anchor = np.array([c[0], kinase_top_y(g, c[0]), 0.0])
    return g


def kinase_top_y(kin, x):
    """Exact y-coordinate of kin.small_lobe's flat top edge at scene x (valid after rotation)."""
    p_r = kin.small_lobe.points[4]
    p_l = kin.small_lobe.points[7]
    dx = p_r[0] - p_l[0]
    if abs(dx) < 1e-6:
        return float(kin.small_lobe.get_top()[1])
    t = (x - p_l[0]) / dx
    return float(p_l[1] + t * (p_r[1] - p_l[1]))


def make_phosphate(pos, radius=0.18, text_size=22):
    """Yellow phosphate badge with dark 'P'."""
    c = Circle(radius=radius, color=PHOS, stroke_width=2.4, fill_color=PHOS, fill_opacity=0.95).move_to(pos)
    lbl = T("P", size=text_size, color=BG, weight=BOLD).move_to(c)
    return VGroup(c, lbl)


def make_atp(pos, width=0.58, height=0.28, text_size=22):
    """Yellow ATP badge with dark 'ATP'."""
    box = RoundedRectangle(
        corner_radius=0.09, width=width, height=height,
        color=PHOS, stroke_width=2.0, fill_color=PHOS, fill_opacity=0.94
    ).move_to(pos)
    lbl = T("ATP", size=text_size, color=BG, weight=BOLD).move_to(box)
    return VGroup(box, lbl)


def make_growth_factor(pos, label=None, radius=0.25):
    """Sky-blue ligand dot/pill."""
    dot = Circle(radius=radius, color=LIGAND, stroke_width=3.2, fill_color=LIGAND, fill_opacity=0.90).move_to(pos)
    if label:
        txt = T(label, size=28, color=LIGAND).next_to(dot, UP, buff=0.16)
        return VGroup(dot, txt)
    return dot


def make_ngf_dimer(pos):
    """Two-lobed sky-blue NGF dimer bridging two receptors."""
    left = Circle(radius=0.28, color=LIGAND, stroke_width=3.2, fill_color=LIGAND, fill_opacity=0.90).shift(LEFT * 0.48)
    right = Circle(radius=0.28, color=LIGAND, stroke_width=3.2, fill_color=LIGAND, fill_opacity=0.90).shift(RIGHT * 0.48)
    bar = RoundedRectangle(corner_radius=0.08, width=0.72, height=0.22, color=LIGAND, stroke_width=2.6,
                           fill_color=LIGAND, fill_opacity=0.82)
    return VGroup(bar, left, right).move_to(pos)


def make_insulin_receptor(splay=1.0, y_mem=0.50, scale=0.98):
    """Pre-paired disulfide-linked insulin receptor. splay=1: legs apart; splay=0: kinases side by side."""
    top_x = 0.72 * scale
    bot_x = (0.86 + 1.55 * splay) * scale
    y_top = y_mem + 1.90 * scale
    y_kin = y_mem - 1.42 * scale

    left_ecto = RoundedRectangle(
        corner_radius=0.18, width=0.76 * scale, height=1.54 * scale,
        color=RTK, stroke_width=3.8, fill_color=RTK, fill_opacity=0.34
    ).move_to([-top_x, y_mem + 1.12 * scale, 0])
    right_ecto = RoundedRectangle(
        corner_radius=0.18, width=0.76 * scale, height=1.54 * scale,
        color=RTK, stroke_width=3.8, fill_color=RTK, fill_opacity=0.34
    ).move_to([top_x, y_mem + 1.12 * scale, 0])

    left_ecto.rotate(-0.14 * (1 - splay), about_point=[-top_x * 0.6, y_top - 0.3, 0])
    right_ecto.rotate(0.14 * (1 - splay), about_point=[top_x * 0.6, y_top - 0.3, 0])

    ds1 = Line([-top_x + 0.36 * scale, y_mem + 1.48 * scale, 0],
               [top_x - 0.36 * scale, y_mem + 1.48 * scale, 0], color=DISULFIDE, stroke_width=4.8)
    ds2 = Line([-top_x + 0.36 * scale, y_mem + 1.18 * scale, 0],
               [top_x - 0.36 * scale, y_mem + 1.18 * scale, 0], color=DISULFIDE, stroke_width=4.8)

    l_leg = Line([-top_x, y_mem + 0.42 * scale, 0], [-bot_x, y_kin + 0.68 * scale, 0],
                 color=RTK, stroke_width=11.0 * scale)
    r_leg = Line([top_x, y_mem + 0.42 * scale, 0], [bot_x, y_kin + 0.68 * scale, 0],
                 color=RTK, stroke_width=11.0 * scale)

    k_left = make_kinase_domain([-bot_x, y_kin, 0], facing=1, loop_open=0.0, scale=0.84 * scale)
    k_right = make_kinase_domain([bot_x, y_kin, 0], facing=-1, loop_open=0.0, scale=0.84 * scale)

    g = VGroup(l_leg, r_leg, left_ecto, right_ecto, ds1, ds2, k_left, k_right)
    g.pocket = np.array([0.0, y_mem + 1.65 * scale, 0])
    g.k_left = k_left
    g.k_right = k_right
    return g


def build_monomer(x, y_mem, scale=1.02, egfr=False, facing=1, arm_open=0.0,
                  kinase_color=KINASE_REST, loop_open=0.0, lobe_close=0.0,
                  active=False, hatched=False, tail_phase=0.0):
    """Complete single RTK spanning the membrane at x."""
    y_top = y_mem + 0.32
    y_bot = y_mem - 0.32
    if egfr:
        ecto = make_egfr_ectodomain(x, y_top, facing=facing, arm_open=arm_open, scale=scale)
    else:
        ecto = make_ectodomain_cup(x, y_top, scale=scale)
    k_center = [x, y_bot - 0.90 * scale, 0]
    kin = make_kinase_domain(
        k_center, color=kinase_color, facing=facing,
        loop_open=loop_open, lobe_close=lobe_close,
        active=active, hatched=hatched, tail_phase=tail_phase, scale=0.85 * scale
    )
    helix = make_helix(x, y_top + 0.04, kin.top_anchor[1] - 0.04, width=0.23 * scale)
    g = VGroup(helix, ecto, kin)
    g.ecto = ecto
    g.helix = helix
    g.kinase = kin
    return g


def leader_arrow(start, end, color=GREY):
    return Line(start, end, color=color, stroke_width=2.6)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Receptor Tyrosine Kinases"
    TITLE = "Two Together: How Pairing Switches an RTK On"


class S01Hook(SpokenScene):
    def construct(self):
        mem = make_membrane(y=0.25)
        r1_x = ValueTracker(-0.8)
        rtk1 = always_redraw(lambda: build_monomer(r1_x.get_value(), mem.y_center, scale=1.02, facing=1))
        tag = scope_tag("schematic")

        t_gf = ValueTracker(0.0)

        def gf_pos():
            t = t_gf.get_value()
            x = -5.0 + 0.48 * t
            base_y = 2.68 + 0.24 * np.sin(1.6 * t)
            # Visible approach to and deflection upward off the membrane barrier between t=2.7 and t=5.6
            if 2.7 <= t <= 5.6:
                u = (t - 2.7) / 2.9
                target_y = mem.y_top + 0.08 + 0.38
                dip = np.sin(PI * u) ** 1.3
                y = (1 - dip) * base_y + dip * target_y
            else:
                y = base_y
            return np.array([x, y, 0.0])

        gf = always_redraw(lambda: make_growth_factor(gf_pos(), radius=0.30))
        gf_lbl = always_redraw(lambda: T("Growth factor", size=28, color=LIGAND).next_to(gf, UP, buff=0.14))

        self.add(mem, rtk1, tag, gf, gf_lbl)

        # Beat 1: Growth factor floats outside and never crosses the membrane
        self.play(t_gf.animate(run_time=2.5, rate_func=linear).set_value(2.7))
        self.at("never crosses")
        barrier = DashedLine([-4.2, mem.y_top + 0.08, 0], [-1.55, mem.y_top + 0.08, 0],
                             color=LIGAND, stroke_width=3.2, dash_length=0.16)
        self.play(Create(barrier), t_gf.animate(run_time=2.9, rate_func=linear).set_value(5.6))

        # Beat 2: Only one narrow helix connects outside to inside
        self.at("narrow helix")
        self.play(FadeOut(barrier, run_time=0.4), t_gf.animate(run_time=0.4, rate_func=linear).set_value(6.0))
        helix_glow = RoundedRectangle(
            corner_radius=0.1, width=0.40, height=1.04,
            color=LIGAND, stroke_width=4.4, fill_opacity=0
        ).move_to([-0.8, mem.y_center - 0.04, 0])
        helix_lbl = T("Single helix", size=28, color=RTK).move_to([-3.5, -0.75, 0])
        helix_ptr = leader_arrow(helix_lbl.get_right() + RIGHT * 0.1, [-1.02, -0.25, 0], color=RTK)
        self.play(Create(helix_glow), FadeIn(helix_lbl), Create(helix_ptr),
                  t_gf.animate(run_time=3.4, rate_func=linear).set_value(9.4))
        self.play(FadeOut(helix_glow, helix_lbl, helix_ptr, run_time=0.5),
                  t_gf.animate(run_time=1.3, rate_func=linear).set_value(10.7))

        # Beat 3: How does signal outside switch on enzyme on far side?
        # Shift first RTK left smoothly to prepare space for second receptor while ? appears
        self.at("switch on")
        q_badge = boxed_label("?", color=GOLD, size=34, box=(0.74, 0.74)).move_to([0.95, -0.98, 0])
        self.play(FadeIn(q_badge, run_time=0.5), r1_x.animate(run_time=2.5).set_value(-1.45),
                  t_gf.animate(run_time=2.5, rate_func=linear).set_value(13.0))

        # Second receptor begins gliding into view from the right as answer begins
        r2_x = ValueTracker(5.8)
        rtk2 = always_redraw(lambda: build_monomer(r2_x.get_value(), mem.y_center, scale=1.02, facing=-1))
        self.add(rtk2)
        self.play(FadeOut(q_badge, run_time=0.4), r2_x.animate(run_time=3.5).set_value(3.8),
                  t_gf.animate(run_time=3.5, rate_func=linear).set_value(16.5))

        # Beat 4: Bringing two receptors together
        self.at("bringing two")
        self.play(
            r1_x.animate.set_value(-1.15),
            r2_x.animate.set_value(1.15),
            t_gf.animate(rate_func=linear).set_value(18.2),
            run_time=2.0
        )
        self.finish()


class S02Architecture(SpokenScene):
    def construct(self):
        # Smoothly zoom from center onto zoomed RTK (cleft facing LEFT so Activation loop label is unobstructed)
        mem = make_membrane(y=1.05, width=13.6, thickness=0.56)
        zoom_t = ValueTracker(0.0)
        phase = ValueTracker(0.0)
        lobe_close = ValueTracker(0.0)
        loop_open = ValueTracker(0.75)  # starts un-plugged, folds tightly into cleft when "activation loop" is said
        tail_unfurl = ValueTracker(0.35)
        ecto_hi_t = ValueTracker(0.0)

        def mk_rtk():
            z = zoom_t.get_value()
            rx = -1.2 * z
            sc = 1.02 + 0.22 * z
            ecto = make_ectodomain_cup(rx, mem.y_top - 0.02, scale=sc, fill_op=0.34 + 0.20 * ecto_hi_t.get_value())
            kin = make_kinase_domain(
                [rx, -0.78, 0], color=KINASE_REST, facing=-1,
                loop_open=loop_open.get_value(), lobe_close=lobe_close.get_value(),
                tail_phase=phase.get_value(), tail_unfurl=tail_unfurl.get_value(), scale=sc
            )
            helix = make_helix(rx, mem.y_top + 0.02, kin.top_anchor[1] - 0.02, width=0.24 * sc / 1.2, color=RTK)
            return VGroup(helix, ecto, kin), ecto, helix, kin

        rtk_dyn = always_redraw(lambda: mk_rtk()[0])
        tag = scope_tag("schematic")
        self.add(mem, rtk_dyn, tag)

        # Beat 1: Zoom smoothly onto one receptor
        self.play(zoom_t.animate.set_value(1.0), phase.animate(rate_func=linear).set_value(1.8), run_time=2.0)
        self.at("shares one")
        plan_lbl = T("Three-part plan", size=32, color=TEXT).move_to([3.3, 2.78, 0])
        self.play(FadeIn(plan_lbl, shift=UP * 0.1), phase.animate(rate_func=linear).set_value(4.0), run_time=2.8)

        # Beat 2: Ectodomain lights up
        self.at("Outside sits")
        _, ecto0, helix0, kin0 = mk_rtk()
        lbl_ecto = T("Ectodomain", size=30, color=RTK).move_to([3.3, 2.08, 0])
        ptr_ecto = leader_arrow(lbl_ecto.get_left() + LEFT * 0.12, ecto0.get_right() + RIGHT * 0.1, color=RTK)
        self.play(ecto_hi_t.animate.set_value(1.0), FadeIn(lbl_ecto), Create(ptr_ecto),
                  phase.animate(rate_func=linear).set_value(6.5), run_time=2.8)

        # Beat 3: Single helix
        self.at("One helix")
        helix_hi = RoundedRectangle(corner_radius=0.08, width=0.42, height=helix0.height + 0.14,
                                    color=RTK, stroke_width=5.4, fill_opacity=0).move_to(helix0)
        lbl_helix = T("Single helix", size=30, color=RTK).move_to([3.3, 0.20, 0])
        ptr_helix = leader_arrow(lbl_helix.get_left() + LEFT * 0.12, helix0.get_right() + RIGHT * 0.08, color=RTK)
        self.play(ecto_hi_t.animate.set_value(0.0), Create(helix_hi), FadeIn(lbl_helix), Create(ptr_helix),
                  lobe_close.animate.set_value(-0.50), phase.animate(rate_func=linear).set_value(9.2), run_time=3.2)

        # Beat 4: Two-lobed kinase
        self.at("Inside hangs")
        lbl_kin = T("Two-lobed kinase", size=30, color=KINASE_REST).move_to([3.3, -0.82, 0])
        ptr_kin = leader_arrow(lbl_kin.get_left() + LEFT * 0.12, kin0.large_lobe.get_right() + RIGHT * 0.14, color=KINASE_REST)
        self.play(FadeOut(helix_hi, run_time=0.4), FadeIn(lbl_kin), Create(ptr_kin),
                  lobe_close.animate.set_value(-0.75), phase.animate(rate_func=linear).set_value(10.5), run_time=1.4)

        # Beat 4b: Small upper lobe
        self.at("small upper lobe")
        _, _, _, kin_open = mk_rtk()
        lbl_small = T("Small lobe", size=28, color=KINASE_REST).move_to([-4.5, 0.22, 0])
        ptr_small = leader_arrow(lbl_small.get_right() + RIGHT * 0.12, kin_open.small_lobe.get_left() + LEFT * 0.10, color=KINASE_REST)
        self.play(FadeIn(lbl_small), Create(ptr_small), phase.animate(rate_func=linear).set_value(11.8), run_time=1.2)

        # Beat 4c: Large lower lobe
        self.at("large lower lobe")
        lbl_large = T("Large lobe", size=28, color=KINASE_REST).move_to([-4.5, -1.85, 0])
        ptr_large = leader_arrow(lbl_large.get_right() + RIGHT * 0.12, kin_open.large_lobe.get_left() + DOWN * 0.36 + LEFT * 0.10, color=KINASE_REST)
        self.play(FadeIn(lbl_large), Create(ptr_large), phase.animate(rate_func=linear).set_value(13.2), run_time=1.5)

        # Beat 5: Tail carrying tyrosines unfurls and sways
        self.at("tail carrying")
        lbl_tail = T("Tail (tyrosines)", size=28, color=RTK).move_to([3.3, -2.35, 0])
        ptr_tail = leader_arrow(lbl_tail.get_left() + LEFT * 0.12, [-0.65, -2.35, 0], color=RTK)
        self.play(tail_unfurl.animate.set_value(1.0), FadeIn(lbl_tail), Create(ptr_tail),
                  phase.animate(rate_func=linear).set_value(16.0), run_time=2.2)

        # Beat 6: Left alone, holds itself shut
        self.at("Left alone")
        self.play(lobe_close.animate.set_value(0.45), phase.animate(rate_func=linear).set_value(24.5), run_time=6.4)

        # Beat 7: Coral activation loop folds tightly into active site cleft
        self.at("activation loop")
        lbl_loop = T("Activation loop", size=28, color=LOOP).move_to([-4.5, -0.78, 0])
        ptr_loop = leader_arrow(lbl_loop.get_right() + RIGHT * 0.12, kin0.cleft_pt + LEFT * 0.42, color=LOOP)
        self.play(loop_open.animate.set_value(0.0), FadeIn(lbl_loop), Create(ptr_loop),
                  phase.animate(rate_func=linear).set_value(29.0), run_time=3.4)
        self.finish()


class S03ThreeRoutes(SpokenScene):
    def construct(self):
        mem = make_membrane(y=0.25)
        tag = scope_tag("schematic")
        sep = ValueTracker(2.9)
        arm = ValueTracker(0.0)
        mode_egfr = ValueTracker(0.0)

        def mk_pair():
            x = sep.get_value()
            if mode_egfr.get_value() < 0.5:
                r1 = build_monomer(-x, mem.y_center, scale=0.98, egfr=False, facing=1)
                r2 = build_monomer(x, mem.y_center, scale=0.98, egfr=False, facing=-1)
            else:
                a = arm.get_value()
                r1 = build_monomer(-x, mem.y_center, scale=0.98, egfr=True, facing=1, arm_open=a)
                r2 = build_monomer(x, mem.y_center, scale=0.98, egfr=True, facing=-1, arm_open=a)
            return VGroup(r1, r2)

        pair = always_redraw(mk_pair)
        head = T("Three ways to pair", size=32, color=TEXT).move_to([0, HEAD_Y, 0])
        lbl_small = T("Small lobe", size=26, color=KINASE_REST).move_to([5.15, -0.48, 0])
        lbl_large = T("Large lobe", size=26, color=KINASE_REST).move_to([5.15, -1.38, 0])
        ptr_small = always_redraw(lambda: leader_arrow(
            lbl_small.get_left() + LEFT * 0.10, [sep.get_value() + 0.65, -0.52, 0], color=KINASE_REST
        ))
        ptr_large = always_redraw(lambda: leader_arrow(
            lbl_large.get_left() + LEFT * 0.10, [sep.get_value() + 0.72, -1.30, 0], color=KINASE_REST
        ))
        self.add(mem, pair, head, lbl_small, lbl_large, ptr_small, ptr_large, tag)

        # Continuous inward drift during intro so no 5s freeze occurs
        self.play(sep.animate.set_value(2.30), run_time=3.6)
        self.at("three ways")
        self.play(sep.animate.set_value(2.55), run_time=2.4)

        # Route 1: NGF dimer bridges two receptors
        self.at("nerve growth factor")
        head_ngf = T("1. Dimeric ligand (NGF)", size=32, color=LIGAND).move_to([0, HEAD_Y, 0])
        ngf_y = ValueTracker(2.35)
        ngf = always_redraw(lambda: make_ngf_dimer([0, ngf_y.get_value(), 0]))
        ngf_lbl = T("NGF dimer", size=28, color=LIGAND).move_to([0, 2.86, 0])
        self.play(swap(head, head_ngf, run_time=0.6), FadeIn(ngf, ngf_lbl, run_time=0.5))
        self.play(ngf_y.animate.set_value(1.58), sep.animate.set_value(1.20), run_time=1.4)

        self.at("bridge two receptors")
        self.wait(0.2)

        # Route 2: EGF binds one receptor, opens hidden arm, arms clasp
        self.at("Epidermal growth factor")
        head_egf = T("2. Exposed dimerization arm (EGF)", size=32, color=LIGAND).move_to([0, HEAD_Y, 0])
        self.play(FadeOut(ngf, ngf_lbl, run_time=0.4), swap(head_ngf, head_egf, run_time=0.6))
        mode_egfr.set_value(1.0)
        self.play(sep.animate.set_value(2.42), run_time=0.9)

        egf1 = make_growth_factor([-3.9, 2.30, 0], radius=0.22)
        egf2 = make_growth_factor([3.9, 2.30, 0], radius=0.22)
        self.play(
            egf1.animate.move_to([-3.04, 1.66, 0]),
            egf2.animate.move_to([3.04, 1.66, 0]),
            run_time=0.9
        )

        self.at("opens a hidden arm")
        arm_lbl = T("Dimerization arms", size=28, color=RTK).move_to([0, 2.48, 0])
        self.play(
            arm.animate.set_value(1.0),
            egf1.animate.shift(RIGHT * 0.14),
            egf2.animate.shift(LEFT * 0.14),
            FadeIn(arm_lbl, run_time=0.5),
            run_time=1.5
        )

        self.at("arms clasp together")
        dx = 2.42 - 1.06
        egf_lbl = T("EGF (apart)", size=26, color=LIGAND).move_to([-3.8, 2.25, 0])
        self.play(
            sep.animate.set_value(1.06),
            egf1.animate.shift(RIGHT * dx),
            egf2.animate.shift(LEFT * dx),
            FadeIn(egf_lbl, run_time=0.6),
            run_time=1.7
        )
        self.finish()


class S04InsulinRoute(SpokenScene):
    def construct(self):
        mem = make_membrane(y=0.50)
        tag = scope_tag("schematic")
        splay = ValueTracker(1.0)
        zoom_t = ValueTracker(0.0)

        ins_rec = always_redraw(lambda: make_insulin_receptor(
            splay=splay.get_value(), y_mem=mem.y_center + 0.55 * zoom_t.get_value(),
            scale=0.98 + 0.18 * zoom_t.get_value()
        ))
        head = T("3. Pre-paired receptor (Insulin)", size=32, color=RTK).move_to([0, HEAD_Y, 0])
        lbl_small = T("Small lobe", size=26, color=KINASE_REST).move_to([5.15, -0.42, 0])
        lbl_large = T("Large lobe", size=26, color=KINASE_REST).move_to([5.15, -1.34, 0])

        def _ins_lobe_pt(dy):
            sp = splay.get_value()
            zm = zoom_t.get_value()
            sc = 0.98 + 0.18 * zm
            ym = mem.y_center + 0.55 * zm
            bx = (0.86 + 1.55 * sp) * sc
            yk = ym - 1.42 * sc
            return np.array([bx + 0.62 * sc, yk + dy * 0.84 * sc, 0.0])

        ptr_small = always_redraw(lambda: leader_arrow(
            lbl_small.get_left() + LEFT * 0.10, _ins_lobe_pt(0.52), color=KINASE_REST
        ))
        ptr_large = always_redraw(lambda: leader_arrow(
            lbl_large.get_left() + LEFT * 0.10, _ins_lobe_pt(-0.42), color=KINASE_REST
        ))
        self.add(mem, ins_rec, head, lbl_small, lbl_large, ptr_small, ptr_large, tag)

        self.at("insulin receptor")
        self.play(splay.animate.set_value(0.88), run_time=2.4)
        self.play(splay.animate.set_value(1.0), run_time=2.4)

        self.at("disulfide bonds")
        ds_lbl = T("Disulfide bonds", size=28, color=DISULFIDE).move_to([0.0, 2.74, 0])
        ds_ptr = leader_arrow(ds_lbl.get_bottom() + DOWN * 0.08, [0.0, 1.98, 0], color=DISULFIDE)
        self.play(FadeIn(ds_lbl), Create(ds_ptr), splay.animate.set_value(0.92), run_time=1.8)
        self.play(splay.animate.set_value(1.0), run_time=1.2)

        self.at("held apart")
        apart_arrow = DoubleArrow([-1.45, -1.35, 0], [1.45, -1.35, 0], color=KINASE_REST, stroke_width=3.6, tip_length=0.22)
        apart_lbl = T("Held apart", size=28, color=KINASE_REST).move_to([0, -2.55, 0])
        self.play(Create(apart_arrow), FadeIn(apart_lbl), splay.animate.set_value(0.93), run_time=1.8)
        self.play(splay.animate.set_value(1.0), run_time=0.9)

        self.at("Binding insulin")
        self.play(FadeOut(ds_lbl, ds_ptr, run_time=0.35))
        ins_dot = make_growth_factor([0, 2.85, 0], radius=0.24)
        ins_lbl = T("Insulin", size=28, color=LIGAND).move_to([-2.9, 2.35, 0])
        self.play(FadeIn(ins_dot, ins_lbl, run_time=0.45))
        self.play(ins_dot.animate.move_to([0, 2.28, 0]), run_time=0.9)

        self.at("pulling those inner")
        self.play(FadeOut(apart_arrow, apart_lbl, run_time=0.4))
        self.play(splay.animate.set_value(0.0), run_time=2.2)

        self.at("All three")
        self.play(FadeOut(ins_lbl, ins_dot, run_time=0.4))
        head2 = T("All routes: two resting kinases side by side", size=30, color=GOLD).move_to([0, HEAD_Y, 0])
        self.play(swap(head, head2, run_time=0.6))

        self.at("side by side")
        box = RoundedRectangle(
            corner_radius=0.18, width=4.0, height=2.45,
            color=GOLD, stroke_width=3.6, fill_opacity=0
        ).move_to([0, -0.75, 0])
        self.play(Create(box), zoom_t.animate.set_value(0.62), mem.animate.shift(UP * 0.34), run_time=1.6)
        self.finish()


class S05TransActivation(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.55, width=13.6, thickness=0.46)
        sep_x = ValueTracker(2.25)
        loop_t = ValueTracker(0.0)
        lobe_t = ValueTracker(0.0)
        act_t = ValueTracker(0.0)
        tag = scope_tag("schematic")

        def mk_pair():
            sx = sep_x.get_value()
            col = interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), act_t.get_value())
            is_act = act_t.get_value() > 0.45
            kl = make_kinase_domain(
                [-sx, 0.10, 0], color=col, facing=1,
                loop_open=loop_t.get_value(), lobe_close=lobe_t.get_value(),
                active=is_act, show_tail=True, tail_scale=0.85, scale=1.22
            )
            kr = make_kinase_domain(
                [sx, 0.10, 0], color=col, facing=-1,
                loop_open=loop_t.get_value(), lobe_close=lobe_t.get_value(),
                active=is_act, show_tail=True, tail_scale=0.85, scale=1.22
            )
            hl = make_helix(-sx, mem.y_top, kinase_top_y(kl, -sx) - 0.07, width=0.26)
            hr = make_helix(sx, mem.y_top, kinase_top_y(kr, sx) - 0.07, width=0.26)
            return VGroup(hl, hr, kl, kr)

        kin_pair = always_redraw(mk_pair)
        head = T("Insulin receptor & most RTKs", size=32, color=TEXT).move_to([0, 3.40, 0])
        lbl_small = T("Small lobe", size=26, color=KINASE_REST).move_to([5.10, 0.73, 0])
        lbl_large = T("Large lobe", size=26, color=KINASE_REST).move_to([5.10, -0.41, 0])
        ptr_small = always_redraw(lambda: leader_arrow(
            lbl_small.get_left() + LEFT * 0.10, [sep_x.get_value() + 0.85, 0.73, 0],
            color=interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), act_t.get_value())
        ))
        ptr_large = always_redraw(lambda: leader_arrow(
            lbl_large.get_left() + LEFT * 0.10, [sep_x.get_value() + 0.96, -0.41, 0],
            color=interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), act_t.get_value())
        ))
        self.add(mem, kin_pair, head, lbl_small, lbl_large, ptr_small, ptr_large, tag)

        # Slide paired kinases smoothly into working distance
        self.at("paired kinases")
        self.play(sep_x.animate.set_value(1.85), run_time=2.8)

        self.at("insulin receptor")
        loop_lbl = T("Blocking activation loop", size=28, color=LOOP).move_to([0, -2.65, 0])
        self.play(FadeIn(loop_lbl, run_time=0.6), lobe_t.animate.set_value(0.15), run_time=2.4)

        self.at("adds phosphates")
        head_trans = T("Trans-autophosphorylation", size=32, color=PHOS).move_to([0, 3.40, 0])
        self.play(FadeOut(loop_lbl, run_time=0.4), swap(head, head_trans, run_time=0.6), lobe_t.animate.set_value(0.0), run_time=1.0)

        p_prog = ValueTracker(0.0)
        offsets = [(-0.22, -0.15), (0.0, 0.17), (0.22, -0.15)]

        def mk_phos():
            t = p_prog.get_value()
            if t <= 0.001:
                return VGroup()
            g = VGroup()
            lt = loop_t.get_value()
            ang_l = -1.88 * lt
            ang_r = 1.88 * lt
            anchor_l = np.array([-1.85 + 0.32 * 1.22, 0.10 - 0.24 * 1.22, 0])
            anchor_r = np.array([1.85 - 0.32 * 1.22, 0.10 - 0.24 * 1.22, 0])
            base_l = np.array([-1.20, 0.13, 0]) - anchor_l
            base_r = np.array([1.20, 0.13, 0]) - anchor_r
            rot = lambda v, a: np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a), 0])
            dst_l = anchor_l + rot(base_l, ang_l)
            dst_r = anchor_r + rot(base_r, ang_r)

            src_r = np.array([1.45, 0.20, 0])
            src_l = np.array([-1.45, 0.20, 0])

            for ox, oy in offsets:
                p_lr = (1 - t) * src_l + t * (dst_r + np.array([ox, oy, 0])) + UP * 0.65 * np.sin(PI * t)
                g.add(make_phosphate(p_lr, radius=0.16, text_size=22))
                p_rl = (1 - t) * src_r + t * (dst_l + np.array([ox, oy, 0])) + DOWN * 0.65 * np.sin(PI * t)
                g.add(make_phosphate(p_rl, radius=0.16, text_size=22))
            return g

        phos_grp = always_redraw(mk_phos)
        self.add(phos_grp)
        self.play(p_prog.animate.set_value(1.0), run_time=3.2)

        self.at("swing the blocking")
        self.play(loop_t.animate.set_value(1.0), run_time=2.6)

        self.at("two lobes close")
        atp_t = ValueTracker(0.0)

        def mk_atps():
            t = atp_t.get_value()
            if t <= 0.01:
                return VGroup()
            p_l = (1 - t) * np.array([-0.4, -2.4, 0]) + t * np.array([-1.32, 0.08, 0])
            p_r = (1 - t) * np.array([0.4, -2.4, 0]) + t * np.array([1.32, 0.08, 0])
            return VGroup(make_atp(p_l, text_size=22), make_atp(p_r, text_size=22))

        atp_grp = always_redraw(mk_atps)
        self.add(atp_grp)
        self.play(atp_t.animate.set_value(1.0), lobe_t.animate.set_value(0.85), run_time=2.0)

        self.at("catalysis begins")
        active_lbl = T("Active kinases", size=30, color=KINASE_ACTIVE).move_to([0, -2.75, 0])
        self.play(
            act_t.animate.set_value(1.0),
            lbl_small.animate.set_color(KINASE_ACTIVE),
            lbl_large.animate.set_color(KINASE_ACTIVE),
            FadeIn(active_lbl, run_time=0.5),
            run_time=1.8,
        )
        self.finish()


class S06EgfrAsymmetry(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.55, width=13.6, thickness=0.46)
        tag = scope_tag("schematic")

        press_t = ValueTracker(0.0)
        open_t = ValueTracker(0.0)

        def mk_pair():
            p = press_t.get_value()
            o = open_t.get_value()
            lx = -2.0 + 1.50 * p
            ly = 0.05 + 0.83 * p
            rx = 2.0 - 1.38 * p
            ry = 0.05 - 0.81 * p

            kl = make_kinase_domain(
                [lx, ly, 0], color=KINASE_REST, facing=-1,
                loop_open=0.0, lobe_close=0.0, active=False, tail_scale=0.68, scale=1.02
            )
            kl.rotate(-0.12 * p, about_point=[lx, ly, 0])

            r_col = interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), o)
            kr = make_kinase_domain(
                [rx, ry, 0], color=r_col, facing=1,
                loop_open=o, lobe_close=0.75 * o, active=(o > 0.45), tail_scale=0.68, scale=1.02
            )
            hl = make_helix(lx, mem.y_top, kinase_top_y(kl, lx) - 0.07, width=0.25)
            hr = make_helix(rx, mem.y_top, kinase_top_y(kr, rx) - 0.07, width=0.25)
            return VGroup(hl, hr, kl, kr)

        pair = always_redraw(mk_pair)
        head = T("EGF receptor", size=32, color=RTK).move_to([0, 3.40, 0])
        lbl_large = T("Large lobe", size=28, color=KINASE_REST).move_to([-4.35, 0.45, 0])
        lbl_small = T("Small lobe", size=28, color=KINASE_REST).move_to([4.35, -0.22, 0])
        ptr_large = always_redraw(lambda: leader_arrow(
            lbl_large.get_right() + RIGHT * 0.12,
            [-2.0 + 1.50 * press_t.get_value() - 0.85, 0.05 + 0.83 * press_t.get_value() - 0.50, 0],
            color=KINASE_REST
        ))
        ptr_small = always_redraw(lambda: leader_arrow(
            lbl_small.get_left() + LEFT * 0.12,
            [2.0 - 1.38 * press_t.get_value() + 0.72, 0.05 - 0.81 * press_t.get_value() + 0.52, 0],
            color=interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), open_t.get_value())
        ))
        self.add(mem, pair, head, lbl_large, lbl_small, ptr_large, ptr_small, tag)

        self.at("breaks that pattern")
        self.play(press_t.animate.set_value(0.12), run_time=2.4)

        self.at("no phosphate")
        bare_lbl = T("No loop phosphate", size=28, color=LOOP).move_to([0, -2.65, 0])
        self.play(FadeIn(bare_lbl, run_time=0.6), press_t.animate.set_value(0.0), run_time=2.6)

        self.at("lopsided pair")
        head_asym = T("Asymmetric pair", size=32, color=GOLD).move_to([0, 3.40, 0])
        self.play(FadeOut(bare_lbl, run_time=0.4), swap(head, head_asym, run_time=0.6),
                  press_t.animate.set_value(0.85), run_time=2.2)

        self.at("large lobe")
        self.play(Indicate(lbl_large, color=GOLD, scale_factor=1.08), run_time=1.0)

        self.at("presses against")
        self.play(press_t.animate.set_value(1.0), Indicate(lbl_small, color=GOLD, scale_factor=1.08), run_time=2.0)

        self.at("That push")
        self.play(
            open_t.animate.set_value(1.0),
            lbl_small.animate.set_color(KINASE_ACTIVE),
            run_time=2.2,
        )

        self.at("active shape")
        act_lbl = T("Only pressed copy switches on", size=28, color=KINASE_ACTIVE).move_to([0, -3.10, 0])
        self.play(FadeIn(act_lbl, run_time=0.6))
        self.finish()


def build_her3_her2_backdrop(approach=0.0):
    """Shared HER3 (left, violet) + HER2 (right, amber) backdrop for s07_predict and s08_pause."""
    mem = make_membrane(y=2.55, width=13.6, thickness=0.46)
    lx = -1.65 + 0.65 * approach
    ly = 0.85
    rx = 1.75 - 0.65 * approach
    ry = -0.60

    hl = make_helix(lx, mem.y_top, ly + 0.84, color=HER3_COL, width=0.24)
    hr = make_helix(rx, mem.y_top, ry + 0.84, color=RTK, width=0.24)

    kl = make_kinase_domain(
        [lx, ly, 0], color=HER3_COL, tail_color=HER3_COL,
        facing=-1, loop_open=0.0, hatched=True, show_tail=False, scale=1.04
    )
    kr = make_kinase_domain(
        [rx, ry, 0], color=KINASE_REST, tail_color=RTK,
        facing=1, loop_open=0.0, hatched=False, show_tail=False, scale=1.04
    )

    family_tag = T("EGFR family: EGFR, HER2, HER3", size=26, color=TEXT).move_to([-0.6, 3.38, 0])
    lbl3 = T("HER3", size=32, color=HER3_COL).move_to([-4.2, 1.25, 0])
    lbl3_sub = T("nearly inactive", size=26, color=HER3_COL).next_to(lbl3, DOWN, buff=0.14)
    lbl2 = T("HER2", size=32, color=RTK).move_to([4.2, -0.55, 0])
    lbl2_sub = T("active kinase", size=26, color=KINASE_REST).next_to(lbl2, DOWN, buff=0.14)
    tag = T("schematic", size=24, color=GREY).move_to([5.85, 3.40, 0])
    return VGroup(mem, hl, hr, kl, kr, family_tag, lbl3, lbl3_sub, lbl2, lbl2_sub, tag)


class S07Predict(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.55, width=13.6, thickness=0.46)
        tag = T("schematic", size=24, color=GREY).move_to([5.85, 3.40, 0])

        press_t = ValueTracker(1.0)

        def mk_egfr():
            p = press_t.get_value()
            lx = -1.10 + 0.60 * p
            ly = 0.95 - 0.07 * p
            rx = 1.20 - 0.58 * p
            ry = -0.55 - 0.21 * p
            kl = make_kinase_domain([lx, ly, 0], color=KINASE_REST, facing=-1, show_tail=False, scale=1.02)
            kl.rotate(-0.12 * p, about_point=[lx, ly, 0])
            kr = make_kinase_domain([rx, ry, 0], color=KINASE_ACTIVE, facing=1, loop_open=1.0, lobe_close=0.75, active=True, show_tail=False, scale=1.02)
            hl = make_helix(lx, mem.y_top, kinase_top_y(kl, lx) - 0.07, width=0.24)
            hr = make_helix(rx, mem.y_top, kinase_top_y(kr, rx) - 0.07, width=0.24)
            return VGroup(hl, hr, kl, kr)

        egfr_dyn = always_redraw(mk_egfr)
        head = T("Division of labor", size=32, color=GOLD).move_to([0, 3.40, 0])
        self.add(mem, egfr_dyn, head, tag)

        self.at("division of labor")
        surf_lbl = T("Pressing copy: surface only", size=28, color=KINASE_REST).move_to([-3.8, -0.45, 0])
        self.play(FadeIn(surf_lbl, run_time=0.6), press_t.animate.set_value(0.85), run_time=2.4)

        self.at("supply a surface")
        surf_arc = Line([-1.05, -0.02, 0], [0.15, 0.08, 0], color=GOLD, stroke_width=7.0)
        self.play(press_t.animate.set_value(1.0), Create(surf_arc), run_time=1.8)

        self.at("pause and predict")
        self.play(FadeOut(head, surf_lbl, surf_arc, run_time=0.5))

        self.at("Her two and")
        approach = ValueTracker(0.0)

        def mk_her_pair():
            a = approach.get_value()
            lx = -1.65 + 0.65 * a
            ly = 0.85
            rx = 1.75 - 0.65 * a
            ry = -0.60
            hl = make_helix(lx, mem.y_top, ly + 0.84, color=HER3_COL, width=0.24)
            hr = make_helix(rx, mem.y_top, ry + 0.84, color=RTK, width=0.24)
            kl = make_kinase_domain(
                [lx, ly, 0], color=HER3_COL, tail_color=HER3_COL,
                facing=-1, loop_open=0.0, hatched=True, show_tail=False, scale=1.04
            )
            kr = make_kinase_domain(
                [rx, ry, 0], color=KINASE_REST, tail_color=RTK,
                facing=1, loop_open=0.0, hatched=False, show_tail=False, scale=1.04
            )
            return VGroup(hl, hr, kl, kr)

        her_dyn = always_redraw(mk_her_pair)
        family_tag = T("EGFR family: EGFR, HER2, HER3", size=26, color=TEXT).move_to([-0.6, 3.38, 0])
        lbl3 = T("HER3", size=32, color=HER3_COL).move_to([-4.2, 1.25, 0])
        lbl3_sub = T("nearly inactive", size=26, color=HER3_COL).next_to(lbl3, DOWN, buff=0.14)
        lbl2 = T("HER2", size=32, color=RTK).move_to([4.2, -0.55, 0])
        lbl2_sub = T("active kinase", size=26, color=KINASE_REST).next_to(lbl2, DOWN, buff=0.14)

        self.play(FadeOut(egfr_dyn, run_time=0.4))
        self.add(her_dyn)
        self.play(FadeIn(family_tag, lbl3, lbl2, run_time=0.5), approach.animate.set_value(0.35), run_time=2.8)

        self.at("working kinase")
        self.play(FadeIn(lbl2_sub, run_time=0.45), approach.animate.set_value(0.55), run_time=1.3)

        self.at("barely has one")
        self.play(FadeIn(lbl3_sub, run_time=0.45), approach.animate.set_value(0.75), run_time=1.8)

        self.at("pairs with")
        q_card = question_card("Can HER2 + HER3 still switch on?")
        self.play(approach.animate.set_value(1.0), FadeIn(q_card, run_time=0.7), run_time=2.6)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Can HER2 + HER3 still switch on?"
    OPTIONS = ()
    SECONDS = 4.5

    def backdrop(self):
        return build_her3_her2_backdrop(approach=1.0)


class S09RevealAndRule(SpokenScene):
    def construct(self):
        mem = make_membrane(y=2.55, width=13.6, thickness=0.46)
        tag = T("schematic", size=24, color=GREY).move_to([5.85, 3.40, 0])
        q_card = question_card("Can HER2 + HER3 still switch on?")

        press_t = ValueTracker(0.0)
        open_t = ValueTracker(0.0)
        compact_t = ValueTracker(0.0)

        def mk_pair():
            p = press_t.get_value()
            o = open_t.get_value()
            cm = compact_t.get_value()
            sc = 1.04 - 0.28 * cm

            lx = -1.00 + 0.55 * p
            ly = 0.85 + 0.08 * p + 0.72 * cm
            rx = 1.10 - 0.52 * p
            ry = -0.60 - 0.14 * p + 1.08 * cm

            kl = make_kinase_domain(
                [lx, ly, 0], color=HER3_COL, tail_color=HER3_COL,
                facing=-1, loop_open=0.0, hatched=True, show_tail=False, scale=sc
            )
            kl.rotate(-0.12 * p, about_point=[lx, ly, 0])

            r_col = interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), o)
            kr = make_kinase_domain(
                [rx, ry, 0], color=r_col, tail_color=RTK,
                facing=1, loop_open=o, lobe_close=0.75 * o, active=(o > 0.45), show_tail=False, scale=sc
            )
            hl = make_helix(lx, mem.y_top, kinase_top_y(kl, lx) - 0.07 * sc, color=HER3_COL, width=0.22 * sc)
            hr = make_helix(rx, mem.y_top, kinase_top_y(kr, rx) - 0.07 * sc, color=RTK, width=0.22 * sc)
            return VGroup(hl, hr, kl, kr)

        pair = always_redraw(mk_pair)
        family_tag = T("EGFR family: EGFR, HER2, HER3", size=26, color=TEXT).move_to([-0.6, 3.38, 0])
        lbl3 = T("HER3", size=32, color=HER3_COL).move_to([-4.2, 1.25, 0])
        lbl3_sub = T("nearly inactive", size=26, color=HER3_COL).next_to(lbl3, DOWN, buff=0.14)
        lbl2 = T("HER2", size=32, color=RTK).move_to([4.2, -0.55, 0])
        lbl2_sub = T("active kinase", size=26, color=KINASE_REST).next_to(lbl2, DOWN, buff=0.14)
        self.add(mem, pair, family_tag, lbl3, lbl3_sub, lbl2, lbl2_sub, tag, q_card)

        # Immediately dismiss question card and begin moving HER3 toward HER2 so S08->S09 has no frozen bridge
        yes_lbl = T("Yes: strong signaling", size=32, color=KINASE_ACTIVE).move_to([0, 3.40, 0])
        self.play(FadeOut(q_card, family_tag, lbl3_sub, lbl2_sub, run_time=0.35),
                  press_t.animate(rate_func=linear).set_value(0.18), run_time=0.7)
        self.at("mixed pair")
        self.play(FadeIn(yes_lbl, run_time=0.4), press_t.animate(rate_func=linear).set_value(0.65), run_time=3.2)

        self.at("supplies the pressing")
        self.play(press_t.animate.set_value(1.0), run_time=2.0)

        self.at("switching")
        self.play(open_t.animate.set_value(1.0), run_time=1.8)

        self.at("loop phosphorylation")
        self.play(FadeOut(lbl3, lbl2, yes_lbl, run_time=0.4), compact_t.animate.set_value(1.0), run_time=1.2)

        m1_lbl = T("Loop phosphorylation", size=26, color=PHOS).move_to([-3.4, -0.80, 0])
        m1_l = make_kinase_domain([-4.15, -1.72, 0], color=KINASE_ACTIVE, facing=1, loop_open=1.0, active=True, show_tail=False, scale=0.42)
        m1_r = make_kinase_domain([-2.65, -1.72, 0], color=KINASE_ACTIVE, facing=-1, loop_open=1.0, active=True, show_tail=False, scale=0.42)
        m1_p1 = Dot([-3.68, -1.94, 0], radius=0.10, color=PHOS)
        m1_p2 = Dot([-3.12, -1.94, 0], radius=0.10, color=PHOS)

        m2_lbl = T("Lobe-to-lobe contact", size=26, color=KINASE_ACTIVE).move_to([3.4, -0.80, 0])
        m2_l = make_kinase_domain([3.15, -1.46, 0], color=KINASE_REST, facing=-1, show_tail=False, scale=0.40).rotate(-0.12)
        m2_r = make_kinase_domain([3.58, -2.04, 0], color=KINASE_ACTIVE, facing=1, loop_open=1.0, active=True, show_tail=False, scale=0.40)

        self.play(FadeIn(m1_lbl, m1_l, m1_r, m1_p1, m1_p2, m2_lbl, m2_l, m2_r, run_time=1.4))

        self.at("core rule holds")
        rule = caption("Bringing two receptor kinases together releases self-inhibition and activates the pair.", color=GOLD)
        self.play(FadeIn(rule, run_time=0.6))

        # Highlight the two activation modes sequentially before framing the active pair
        m1_box = RoundedRectangle(corner_radius=0.14, width=4.3, height=1.92, color=PHOS, stroke_width=2.8, fill_opacity=0).move_to([-3.4, -1.52, 0])
        m2_box = RoundedRectangle(corner_radius=0.14, width=4.3, height=1.92, color=KINASE_ACTIVE, stroke_width=2.8, fill_opacity=0).move_to([3.4, -1.52, 0])
        self.play(Create(m1_box), run_time=2.2)
        self.play(Create(m2_box), run_time=2.2)

        self.at("activates the pair")
        box = RoundedRectangle(corner_radius=0.16, width=4.2, height=2.68, color=GOLD, stroke_width=3.6, fill_opacity=0).move_to([0.05, 0.95, 0])
        self.play(Create(box), run_time=1.5)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        mem = make_membrane(y=0.40)
        tag = scope_tag("schematic")

        rtk1 = build_monomer(0.0, mem.y_center, scale=1.00, facing=1)
        self.add(mem, rtk1, tag)

        # Beat 1: One lonely helix cannot twist a resting kinase awake
        self.at("lonely helix")
        lone_lbl = T("One helix alone: inactive", size=30, color=KINASE_REST).move_to([0, HEAD_Y, 0])
        upper = VGroup(rtk1.helix, rtk1.ecto)
        self.play(FadeIn(lone_lbl, run_time=0.4))
        self.play(Rotate(upper, angle=0.14, about_point=[0, mem.y_center, 0]), run_time=0.9)
        self.play(Rotate(upper, angle=-0.28, about_point=[0, mem.y_center, 0]), run_time=1.1)
        self.play(Rotate(upper, angle=0.14, about_point=[0, mem.y_center, 0]), run_time=0.8)
        self.play(rtk1.animate.shift(LEFT * 2.2), run_time=1.2)

        # Beat 2: Bridge two chains
        self.at("bridge two chains")
        sep = ValueTracker(2.3)
        pair_cup = always_redraw(lambda: VGroup(
            build_monomer(-sep.get_value(), mem.y_center, scale=0.92, facing=1),
            build_monomer(sep.get_value(), mem.y_center, scale=0.92, facing=-1),
        ))
        ngf = make_ngf_dimer([0, 2.3, 0])
        head_routes = T("Three routes, one payoff", size=30, color=TEXT).move_to([0, HEAD_Y, 0])
        self.remove(rtk1)
        self.add(pair_cup, ngf)
        self.play(
            swap(lone_lbl, head_routes, run_time=0.5),
            ngf.animate.move_to([0, 1.72, 0]),
            sep.animate.set_value(1.15),
            run_time=1.1
        )

        # Beat 3: Expose a hidden arm
        self.at("expose a hidden arm")
        self.remove(pair_cup, ngf)
        arm = ValueTracker(0.0)
        sep_egf = ValueTracker(2.1)
        pair_egf = always_redraw(lambda: VGroup(
            build_monomer(-sep_egf.get_value(), mem.y_center, scale=0.92, egfr=True, facing=1, arm_open=arm.get_value()),
            build_monomer(sep_egf.get_value(), mem.y_center, scale=0.92, egfr=True, facing=-1, arm_open=arm.get_value()),
        ))
        egf_l = make_growth_factor([-2.6, 1.65, 0], radius=0.20)
        egf_r = make_growth_factor([2.6, 1.65, 0], radius=0.20)
        self.add(pair_egf, egf_l, egf_r)
        self.play(
            arm.animate.set_value(1.0),
            sep_egf.animate.set_value(1.02),
            egf_l.animate.shift(RIGHT * 1.08),
            egf_r.animate.shift(LEFT * 1.08),
            run_time=1.1
        )

        # Beat 4: Shift a pre-built pair
        self.at("shift a")
        self.remove(pair_egf, egf_l, egf_r)
        splay = ValueTracker(1.0)
        ins_rec = always_redraw(lambda: make_insulin_receptor(splay=splay.get_value(), y_mem=mem.y_center, scale=0.96))
        ins_dot = make_growth_factor([0, 2.08, 0], radius=0.22)
        self.add(ins_rec, ins_dot)
        self.play(splay.animate.set_value(0.0), run_time=2.4)

        # Beat 5: Either way, the payoff stays the same -> progressive opening into active gold pair
        self.at("payoff stays")
        self.remove(ins_rec, ins_dot)
        open_act = ValueTracker(0.0)
        tail_phase = ValueTracker(0.0)
        final_pair = always_redraw(lambda: VGroup(
            build_monomer(
                -1.10, mem.y_center, scale=0.98, facing=1,
                kinase_color=interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), open_act.get_value()),
                loop_open=open_act.get_value(), lobe_close=0.8 * open_act.get_value(),
                active=(open_act.get_value() > 0.35), tail_phase=tail_phase.get_value()
            ),
            build_monomer(
                1.10, mem.y_center, scale=0.98, facing=-1,
                kinase_color=interpolate_color(ManimColor(KINASE_REST), ManimColor(KINASE_ACTIVE), open_act.get_value()),
                loop_open=open_act.get_value(), lobe_close=0.8 * open_act.get_value(),
                active=(open_act.get_value() > 0.35), tail_phase=-tail_phase.get_value()
            ),
        ))
        self.add(final_pair)
        self.play(open_act.animate(rate_func=linear).set_value(0.80),
                  tail_phase.animate(rate_func=linear).set_value(1.6), run_time=2.8)

        self.at("opens the switch")
        on_lbl = T("Two together → active pair", size=32, color=KINASE_ACTIVE).move_to([0, HEAD_Y, 0])
        self.play(open_act.animate.set_value(1.0), swap(head_routes, on_lbl, run_time=0.8),
                  tail_phase.animate(rate_func=linear).set_value(2.6), run_time=1.2)
        self.finish()


class S11End(EndCard):
    LINE = "Bringing two receptor kinases together releases self-inhibition and activates the pair."
