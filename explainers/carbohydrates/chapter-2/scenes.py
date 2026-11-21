"""
Which Sugar Sits Where — Film 2 of "Carbohydrates: One Bond Decides Fuel or Fiber"

COLOUR MAP (one colour per concept, carried across the whole film):
    TEXT    (#E8EAF0) : glucose/core sugar tiles, cell membrane lines, blood bags, lysosome,
                        immune cell, virus body, "which sugar" chip, general labels
    GOLD    (#D4A843) : the anomeric carbon and its bond (joints, pins, title rule, countdown ring)
    TEAL    (#3FB8C0) : carbon six (C6 tab), "which position" chip/arrow, mannose-6-phosphate tag
    BLUE    (#58C4DD) : alpha bond face (down) & bread icon (s00 only)
    GREEN   (#83C167) : beta bond face (up) & plank icon (s00 only)
    RED     (#FC6255) : "cannot" X marks and I-cell disease loss only
    PURPLE  (#B88CFF) : proteins that act on or read sugars (surface proteins, A/B enzymes,
                        lectins, selectins, hemagglutinin spikes)
    ORANGE  (#FFA048) : A sugar (N-acetylgalactosamine) and type A
    PINK    (#FF9CC8) : B sugar (galactose) and type B
    MAGENTA (#E052D6) : sialic acid (charged terminal sugar, with minus badge)
    MAROON  (#B23A52) : red blood cell outline (distinct from RED)

ONE WORLD CARRIED FROM SCENE TO SCENE:
    A horizontal double-line cell surface membrane across the lower frame (rippling gently via a
    computed wave updater) from which short chains of sugar tiles ("stalks") rise on GOLD
    anomeric joints and sway smoothly (computed sinusoidal sway, amplitude 0.05, period 3 s).
    Chain lengths and sugar counts are marked "schematic" whenever stalks appear.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    s00_hook     : Anomeric bond flag rocks via sin(t) between BLUE (alpha) and GREEN (beta);
                   tiles shrink into a swaying stalk on a red-cell rim; centre tip swaps to
                   ORANGE and blood bags/X reveal transfusion mismatch.
    s02_coat     : Four PURPLE proteins rise under stalks and one secreted glycoprotein drifts
                   out of frame; zoomed stalk flashes each GOLD anomeric joint in sequence.
    s03_h        : Three identical H-antigen stalks glow together, dashed tip slots open, and
                   three inherited PURPLE enzyme shapes drop in above them.
    s04_abo      : A and B enzymes dock ORANGE and PINK tips onto the left/middle stalks by
                   identical GOLD bonds while the O allele fades hollow and leaves tip 3 bare.
    s05_c2       : ORANGE and PINK tip tiles lift and enlarge side by side; their C2 badges
                   blink (square vs dot) to show the single carbon difference, then return.
    s06_rule     : GOLD rule draws above the 3 stalks and the 3-part code ("which sugar",
                   "which bond", "which position") lights up on the matching tile/joint/tip.
    s07_address  : Tagged enzyme blobs (TEAL P on C6) follow Bezier paths into the lysosome;
                   loss of the tag (RED X) sends untagged blobs out the membrane gap to blood.
    s08_lectin   : A single-pocket PURPLE lectin docks onto one tip and loops a computed on-off
                   wobble with a breaking dotted contact line to show weak single binding.
    s09_predict  : The wobbling single-pocket lectin continues while the "How to hold on?"
                   question card drops into upper centre.
    s11_multi    : The lectin widens into a 5-pocket bar gripping 5 tips at once; 5 contacts
                   flicker independently from deterministic RNG phases while the bar holds fast.
    s12_selectin : Circulating immune cell rolls left-to-right across a flowing dot stream and
                   decelerates via a computed step-drag velocity curve at each selectin contact.
    s13_flu      : Spiked flu virus drifts in, locks 3 PURPLE hemagglutinin spikes onto MAGENTA
                   sialic acid tips, and dimples the computed membrane curve beneath it.
    s14_return   : Wide red-cell view with A, B, O tips; a multi-pocket lectin sweeps left-to-
                   right lighting each tip in turn as the three rule chips return above.
"""

from bp_parts import *

# ------------------------------------------------------------------ Film Palette
PURPLE = "#B88CFF"
ORANGE = "#FFA048"
PINK = "#FF9CC8"
MAGENTA = "#E052D6"
MAROON = "#B23A52"

# Standard surface geometry
MEM_Y_TOP = -2.4
MEM_Y_BOT = -2.8
MEM_X0 = -6.2
MEM_X1 = 6.2
STALK_XS_8 = [-4.9, -3.5, -2.1, -0.7, 0.7, 2.1, 3.5, 4.9]
STALK_XS_3 = [-3.8, -0.2, 3.4]
DEFAULT_TIPS_8 = ["glucose", "A", "sialic", "B", "A", "sialic", "B", "A"]


# ------------------------------------------------------------------ World Builders
def make_glucose_tile(width=1.3, color=TEXT, fill_op=0.15, show_labels=True,
                      tab_color=TEAL, pin_color=GOLD):
    """Rounded square glucose/sugar tile with C6 tab (top), anomeric pin (right), and C4 port (left)."""
    s = width
    sq = RoundedRectangle(
        corner_radius=0.14 * (s / 1.3),
        width=s,
        height=s,
        stroke_color=color,
        stroke_width=2.8 if s >= 1.0 else 2.2,
        fill_color=color,
        fill_opacity=fill_op,
    )
    # C6 tab on top
    tab = RoundedRectangle(
        corner_radius=0.06 * (s / 1.3),
        width=0.40 * s,
        height=0.22 * s,
        stroke_color=tab_color,
        stroke_width=2.2 if s >= 1.0 else 1.8,
        fill_color=tab_color,
        fill_opacity=0.22,
    ).next_to(sq, UP, buff=-0.02)

    # Anomeric carbon pin on right edge
    pin = RoundedRectangle(
        corner_radius=0.05 * (s / 1.3),
        width=0.18 * s,
        height=0.28 * s,
        stroke_color=pin_color,
        stroke_width=2.0,
        fill_color=pin_color,
        fill_opacity=0.85,
    ).next_to(sq, RIGHT, buff=-0.02)

    # C4 port on left edge
    port = RoundedRectangle(
        corner_radius=0.05 * (s / 1.3),
        width=0.24 * s,
        height=0.26 * s,
        stroke_color=TEXT,
        stroke_width=2.0 if s >= 1.0 else 1.5,
        fill_color=BG,
        fill_opacity=0.95,
    ).next_to(sq, LEFT, buff=-0.02)

    g = VGroup(sq, tab, pin, port)
    g.sq, g.c6_tab, g.c1_pin, g.c4_port = sq, tab, pin, port
    g.c6_txt = None
    g.c4_txt = None

    if show_labels and s >= 1.1:
        c6_txt = T("C6", size=22, color=TEAL).next_to(tab, UP, buff=0.08)
        c4_txt = M("4", size=22, color=TEXT).move_to(port)
        g.c6_txt, g.c4_txt = c6_txt, c4_txt
        g.add(c6_txt, c4_txt)

    return g


def make_stalk_tile(kind="glucose", width=0.56):
    """A small sugar tile in a cell-surface stalk (no sub-22pt text)."""
    if kind == "A":
        col, op = ORANGE, 0.70
    elif kind == "B":
        col, op = PINK, 0.70
    elif kind == "sialic":
        col, op = MAGENTA, 0.70
    else:
        col, op = TEXT, 0.21

    sq = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=width,
        stroke_color=col,
        stroke_width=2.4,
        fill_color=col,
        fill_opacity=op,
    )
    tab = RoundedRectangle(
        corner_radius=0.03,
        width=width * 0.36,
        height=width * 0.16,
        stroke_color=TEAL,
        stroke_width=1.8,
        fill_color=TEAL,
        fill_opacity=0.25,
    ).next_to(sq, UP, buff=-0.01)

    g = VGroup(sq, tab)
    g.sq = sq
    g.tab = tab
    g.badge = None
    if kind == "sialic":
        circ = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2.0, fill_color=BG, fill_opacity=0.95)
        bar = Line(LEFT * 0.065, RIGHT * 0.065, stroke_color=TEXT, stroke_width=2.5).move_to(circ)
        badge = VGroup(circ, bar).move_to(sq.get_corner(UR) + DL * 0.02)
        g.badge = badge
        g.add(badge)
    return g


def make_membrane(y_top=MEM_Y_TOP, y_bot=MEM_Y_BOT, x0=MEM_X0, x1=MEM_X1,
                  gap=None, amp=0.032, period=4.0, dimple_tracker=None, dimple_x=0.625):
    """Horizontal double-line cell surface with a slow computed wave updater (and optional gap/dimple)."""
    segs = [(x0, x1)] if gap is None else [(x0, gap[0]), (gap[1], x1)]
    top_lines = VGroup()
    bot_lines = VGroup()

    def build_pts(xa, xb, y_base, phase):
        xs = np.linspace(xa, xb, 64)
        ys = y_base + amp * np.sin(2.0 * np.pi * (xs / 3.2) - phase)
        if dimple_tracker is not None:
            d = dimple_tracker.get_value()
            if d > 1e-4:
                ys = ys - d * np.exp(-((xs - dimple_x) / 1.15) ** 2)
        return np.column_stack([xs, ys, np.zeros_like(xs)])

    for xa, xb in segs:
        lt = VMobject(stroke_color=TEXT, stroke_width=3.5)
        lt.set_points_as_corners(build_pts(xa, xb, y_top, 0.0))
        lb = VMobject(stroke_color=TEXT, stroke_width=3.5)
        lb.set_points_as_corners(build_pts(xa, xb, y_bot, 0.0))
        top_lines.add(lt)
        bot_lines.add(lb)

    mem = VGroup(top_lines, bot_lines)
    mem._phase = 0.0
    mem.top_lines = top_lines
    mem.bot_lines = bot_lines

    def ripple(mob, dt):
        mob._phase += dt * (TAU / period)
        for idx, (xa, xb) in enumerate(segs):
            mob.top_lines[idx].set_points_as_corners(build_pts(xa, xb, y_top, mob._phase))
            mob.bot_lines[idx].set_points_as_corners(build_pts(xa, xb, y_bot, mob._phase))

    mem.add_updater(ripple)
    return mem


class SwayStalk(VGroup):
    """Vertical sugar stalk of small tiles + GOLD joints that sways sinusoidally from its base."""

    def __init__(self, x_base, y_base=MEM_Y_TOP, n_tiles=3, tip_kind="glucose",
                 tile_w=0.56, step_y=0.72, amp=0.05, period=3.0, seed=0):
        super().__init__()
        self.x_base = x_base
        self.y_base = y_base
        self.n_tiles = n_tiles
        self.tile_w = tile_w
        self.step_y = step_y
        self.amp = amp
        self.period = period
        self._phase = seed * 0.55

        self.stem = Line([x_base, y_base, 0], [x_base, y_base + 0.28, 0], color=GOLD, stroke_width=3.0)
        self.tiles = VGroup()
        self.joints = VGroup()

        for i in range(n_tiles):
            kind = tip_kind if (i == n_tiles - 1 and tip_kind != "none") else "glucose"
            if i == n_tiles - 1 and tip_kind == "none":
                continue
            y = y_base + 0.28 + tile_w * 0.5 + i * step_y
            tile = make_stalk_tile(kind=kind, width=tile_w).move_to([x_base, y, 0])
            self.tiles.add(tile)
            if i > 0:
                jy = y - step_y * 0.5
                jdot = Dot([x_base, jy, 0], radius=0.075, color=GOLD)
                self.joints.add(jdot)

        self.add(self.stem, self.tiles, self.joints)
        self._record_rest()
        self.add_updater(self._sway_update)

    def _record_rest(self):
        self._rest_tiles = [t.get_center().copy() for t in self.tiles]
        self._rest_joints = [j.get_center().copy() for j in self.joints]
        self._rest_stem_end = self.stem.get_end().copy()
        self._rest_stem_start = self.stem.get_start().copy()

    def _sway_update(self, mob, dt):
        mob._phase += dt * (TAU / mob.period)
        s = np.sin(mob._phase)
        h_max = max(0.8, mob.n_tiles * mob.step_y)
        for idx, tile in enumerate(mob.tiles):
            p0 = mob._rest_tiles[idx]
            frac = max(0.0, (p0[1] - mob.y_base) / h_max)
            tile.move_to(p0 + RIGHT * (mob.amp * s * frac))
        for idx, jdot in enumerate(mob.joints):
            p0 = mob._rest_joints[idx]
            frac = max(0.0, (p0[1] - mob.y_base) / h_max)
            jdot.move_to(p0 + RIGHT * (mob.amp * s * frac))
        if len(mob.tiles) > 0:
            p0 = mob._rest_stem_end
            frac = max(0.0, (p0[1] - mob.y_base) / h_max)
            mob.stem.put_start_and_end_on(mob._rest_stem_start, p0 + RIGHT * (mob.amp * s * frac))

    def tip_tile(self):
        return self.tiles[-1]

    def tip_anchor(self):
        """Top centre of the stalk (or top of last tile) for docking."""
        return self.tiles[-1].get_top().copy()

    def shift_base(self, delta):
        """Translate the stalk and update its rest positions cleanly."""
        self.shift(delta)
        self.x_base += delta[0]
        self.y_base += delta[1]
        self._record_rest()
        return self


def make_red_cell_disc(y_flat=MEM_Y_TOP, top_y=2.48, half_w=5.95):
    """Large MAROON red-cell outline whose lower rim flattens along the membrane."""
    thetas = np.linspace(PI, 0.0, 56)
    xs = half_w * np.cos(thetas)
    # Smooth rounded dome with broad shoulders so title and scanner sit cleanly inside
    ys = y_flat + (top_y - y_flat) * (np.sin(thetas) ** 0.42) - 0.12 * np.exp(-(xs / 2.2) ** 2) * np.sin(thetas)
    pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    outline = VMobject(stroke_color=MAROON, stroke_width=5.5, fill_color=MAROON, fill_opacity=0.07)
    outline.set_points_smoothly(pts)
    return outline


def make_blood_bag(color=TEXT):
    """Small cartoon blood bag outline."""
    body = RoundedRectangle(corner_radius=0.12, width=0.82, height=1.08,
                            stroke_color=color, stroke_width=2.8, fill_color=BG, fill_opacity=0.85)
    hang = Arc(radius=0.14, start_angle=0, angle=PI, stroke_color=color, stroke_width=2.5).next_to(body, UP, buff=-0.02)
    tube = Line(body.get_bottom(), body.get_bottom() + DOWN * 0.22, stroke_color=color, stroke_width=2.5)
    drop = Polygon(
        [0, 0.22, 0], [0.14, -0.05, 0], [0, -0.18, 0], [-0.14, -0.05, 0],
        stroke_color=MAROON, stroke_width=2.2, fill_color=MAROON, fill_opacity=0.55,
    ).move_to(body)
    return VGroup(body, hang, tube, drop)


def make_red_x(center, size=0.65):
    """Bold RED cross for incompatibility / blocked tag."""
    a = Line(UL * size * 0.5, DR * size * 0.5, stroke_color=RED, stroke_width=6.0)
    b = Line(UR * size * 0.5, DL * size * 0.5, stroke_color=RED, stroke_width=6.0)
    return VGroup(a, b).move_to(center)


def make_enzyme_pacman(radius=0.52, color=PURPLE):
    """Cartoon enzyme pac-man facing downward toward its sugar stalk."""
    body = Sector(
        radius=radius,
        start_angle=-PI * 0.28,
        angle=TAU - PI * 0.44,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=0.24,
    )
    return body


def make_lectin_cap(width=1.9, height=0.72, n_pockets=1, pocket_xs=None, color=PURPLE):
    """PURPLE rounded lectin cap with notched pockets along its underside."""
    w2 = width / 2.0
    h = height
    if pocket_xs is None:
        if n_pockets == 1:
            pocket_xs = [0.0]
        else:
            margin = min(0.55, width * 0.22)
            pocket_xs = np.linspace(-w2 + margin, w2 - margin, n_pockets)

    spacing = width / max(1, n_pockets)
    pw = min(0.22, spacing * 0.26)
    ph = min(0.24, height * 0.44)
    pts = [
        [-w2, 0.0, 0],
        [-w2, h * 0.72, 0],
        [-w2 * 0.78, h, 0],
        [w2 * 0.78, h, 0],
        [w2, h * 0.72, 0],
        [w2, 0.0, 0],
    ]
    for px in sorted(pocket_xs, reverse=True):
        pts.extend([
            [px + pw, 0.0, 0],
            [px + pw * 0.65, ph, 0],
            [px - pw * 0.65, ph, 0],
            [px - pw, 0.0, 0],
        ])
    poly = Polygon(*pts, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22)
    poly.round_corners(radius=0.08 if n_pockets == 1 else 0.025)
    return poly


def make_protein_blob(width=0.92, height=0.54, color=PURPLE):
    """Rounded PURPLE membrane protein blob."""
    return RoundedRectangle(
        corner_radius=0.22,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=3.0,
        fill_color=color,
        fill_opacity=0.28,
    )


def make_virus(radius=0.88, n_spikes=12):
    """Flu virus cartoon: TEXT circle studded with PURPLE hemagglutinin spikes."""
    body = Circle(radius=radius, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.08)
    spikes = VGroup()
    for k in range(n_spikes):
        ang = k * TAU / n_spikes - PI / 2.0  # k=0 points straight down (-90 deg)
        u = np.array([np.cos(ang), np.sin(ang), 0.0])
        perp = np.array([-np.sin(ang), np.cos(ang), 0.0])
        p0 = u * radius
        p1 = u * (radius + 0.26)
        stem = Line(p0, p1, stroke_color=PURPLE, stroke_width=3.5)
        head = Arc(radius=0.14, start_angle=ang - PI * 0.45, angle=PI * 0.9,
                   arc_center=u * (radius + 0.36), stroke_color=PURPLE, stroke_width=3.5)
        sp = VGroup(stem, head)
        sp.tip_pt = p1 + u * 0.04
        sp.perp = perp
        spikes.add(sp)
    g = VGroup(body, spikes)
    g.body = body
    g.spikes = spikes
    return g


def make_rule_chips(size=30):
    """The three second-rule chips: which sugar, which bond, which position."""
    c1 = boxed_label("which sugar", color=TEXT, size=size, fill_opacity=0.16)
    c2 = boxed_label("which bond", color=GOLD, size=size, fill_opacity=0.16)
    c3 = boxed_label("which position", color=TEAL, size=size, fill_opacity=0.16)
    row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.45)
    return row


def make_schematic_tag():
    return scope_tag("schematic", size=28, color=TEXT)


def _scale_mob_opacity(mob, factor):
    """Scale stroke and fill opacities proportionally per leaf mobject (preserving translucent fills)."""
    for m in mob.family_members_with_points():
        if not hasattr(m, "_base_op"):
            m._base_op = (m.get_stroke_opacity(), m.get_fill_opacity())
        so, fo = m._base_op
        m.set_stroke(opacity=so * factor)
        m.set_fill(opacity=fo * factor)


def _anim_mob_opacity(mob, factor):
    """Animate stroke and fill opacities proportionally per leaf mobject without suspending updaters."""
    leaves = []
    for m in mob.family_members_with_points():
        if not hasattr(m, "_base_op"):
            m._base_op = (m.get_stroke_opacity(), m.get_fill_opacity())
        so0, fo0 = m.get_stroke_opacity(), m.get_fill_opacity()
        so1, fo1 = m._base_op[0] * factor, m._base_op[1] * factor
        leaves.append((m, so0, fo0, so1, fo1))

    def updater(grp, alpha):
        for m, so0, fo0, so1, fo1 in leaves:
            m.set_stroke(opacity=so0 + (so1 - so0) * alpha)
            m.set_fill(opacity=fo0 + (fo1 - fo0) * alpha)

    return UpdateFromAlphaFunc(mob, updater, suspend_mobject_updating=False)


# ------------------------------------------------------------------ Scenes
class S00Hook(SpokenScene):
    def construct(self):
        # Open directly on film 1's last picture: 2 glucose tiles + rocking bond flag + bread/plank
        t_left = make_glucose_tile(1.3, color=TEXT, fill_op=0.18, show_labels=True).move_to(LEFT * 1.48)
        t_right = make_glucose_tile(1.3, color=TEXT, fill_op=0.18, show_labels=True).move_to(RIGHT * 1.48)
        bond_line = Line(t_left.c1_pin.get_right(), t_right.c4_port.get_left(), color=GOLD, stroke_width=5)
        bond_dot = Dot(bond_line.get_center(), radius=0.11, color=GOLD)

        # Rocking flag between BLUE (down) and GREEN (up), staying strictly in the central gap
        flag_stem = Line(ORIGIN, DOWN * 0.45, color=BLUE, stroke_width=4)
        flag_head = RoundedRectangle(corner_radius=0.06, width=0.42, height=0.24,
                                     stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.25)
        flag = VGroup(flag_stem, flag_head)
        flag._t = 0.0

        def update_flag(mob, dt):
            mob._t += dt
            val = np.sin(mob._t * 3.0)
            col = GREEN if val >= 0 else BLUE
            pivot = bond_dot.get_center()
            tip = pivot + np.array([0.08 * np.cos(val), 0.72 * val, 0.0])
            mob[0].put_start_and_end_on(pivot, tip).set_color(col)
            mob[1].move_to(tip + np.array([0.22, 0.0, 0.0])).set_stroke(col).set_fill(col, opacity=0.25)

        flag.add_updater(update_flag)

        # Tiny cartoon bread (BLUE outline) left and plank (GREEN outline) right at 40%
        bread = VGroup(
            RoundedRectangle(corner_radius=0.18, width=1.1, height=0.68, stroke_color=BLUE, stroke_width=3),
            Arc(radius=0.56, start_angle=0.15, angle=PI - 0.30, stroke_color=BLUE, stroke_width=3).shift(UP * 0.18),
        ).move_to([-4.3, -0.2, 0]).set_opacity(0.4)
        plank = VGroup(
            Rectangle(width=1.45, height=0.45, stroke_color=GREEN, stroke_width=3),
            Line([-0.55, 0.05, 0], [0.55, 0.05, 0], stroke_color=GREEN, stroke_width=2),
            Line([-0.40, -0.10, 0], [0.45, -0.10, 0], stroke_color=GREEN, stroke_width=2),
        ).move_to([4.3, -0.2, 0]).set_opacity(0.4)

        self.add(t_left, t_right, bond_line, bond_dot, flag, bread, plank)

        self.at("fuel or fiber")
        flag.clear_updaters()
        # Bread and plank fade out; two tiles shrink and rise into place as top of centre stalk
        mem = make_membrane()
        red_cell = make_red_cell_disc()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4, tip_kind="glucose", seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        centre_stalk = stalks[4]
        target_top = centre_stalk.tiles[-1].get_center()
        target_mid = centre_stalk.tiles[-2].get_center()
        scale_f = centre_stalk.tile_w / 1.3
        tag = make_schematic_tag()

        # Remove C6 / 4 text cleanly before shrinking
        lbl_outs = [m for m in (t_left.c6_txt, t_left.c4_txt, t_right.c6_txt, t_right.c4_txt) if m is not None]
        for m in lbl_outs:
            t_left.remove(m)
            t_right.remove(m)
        self.play(
            FadeOut(bread),
            FadeOut(plank),
            FadeOut(flag),
            FadeOut(bond_line),
            *[FadeOut(m) for m in lbl_outs],
            run_time=0.45,
        )
        self.play(
            t_left.animate.scale(scale_f).move_to(target_mid),
            t_right.animate.scale(scale_f).move_to(target_top),
            bond_dot.animate.scale(0.68).move_to((target_mid + target_top) / 2),
            run_time=1.0,
        )

        self.at("a red blood cell")
        # Pull back into red blood cell disc + membrane (FadeIn avoids Create partial-fill wipe)
        self.play(
            FadeIn(red_cell),
            FadeIn(mem),
            FadeIn(tag),
            run_time=1.2,
        )

        self.at("Short sugar chains")
        # Swap t_left/t_right/bond_dot cleanly out as all 8 swaying stalks fade in
        self.play(
            FadeOut(t_left, run_time=0.35),
            FadeOut(t_right, run_time=0.35),
            FadeOut(bond_dot, run_time=0.35),
            FadeIn(stalks, run_time=1.1),
        )

        # Pulse tip tiles WHITE as "surface" lands
        tip_highlights = VGroup(*[
            SurroundingRectangle(s.tip_tile().sq, color=TEXT, buff=0.06, corner_radius=0.08, stroke_width=3.5)
            for s in stalks
        ])
        self.play(FadeIn(tip_highlights), run_time=0.45)
        self.play(FadeOut(tip_highlights), run_time=0.45)

        self.at("Change one small sugar")
        # Centre stalk tip swaps WHITE -> ORANGE -> WHITE -> ORANGE
        c_stalk = stalks[4]
        white_tip = c_stalk.tip_tile()
        orange_tip = make_stalk_tile("A", width=c_stalk.tile_w).move_to(white_tip.get_center())
        self.play(FadeOut(white_tip, run_time=0.35), FadeIn(orange_tip, run_time=0.35))
        self.wait(0.2)
        white_tip2 = make_stalk_tile("glucose", width=c_stalk.tile_w).move_to(orange_tip.get_center())
        self.play(FadeOut(orange_tip, run_time=0.35), FadeIn(white_tip2, run_time=0.35))
        self.wait(0.15)
        orange_final = make_stalk_tile("A", width=c_stalk.tile_w).move_to(white_tip2.get_center())
        self.play(FadeOut(white_tip2, run_time=0.35), FadeIn(orange_final, run_time=0.35))
        # Swap into stalk's tile list so swaying continues seamlessly
        c_stalk.tiles.remove(white_tip)
        c_stalk.tiles.add(orange_final)
        c_stalk._record_rest()

        self.at("which blood")
        bag1 = make_blood_bag().move_to([3.5, 2.55, 0])
        bag2 = make_blood_bag().move_to([5.1, 2.55, 0])
        self.play(FadeIn(bag1, shift=LEFT * 0.6), FadeIn(bag2, shift=LEFT * 0.6), run_time=0.75)
        x_mark = make_red_x(bag2.get_center(), size=0.85)
        self.play(Create(x_mark), run_time=0.5)

        self.at("How can one sugar")
        # Dim everything to 40% except the one ORANGE tip tile, which glows
        glow_ring = RoundedRectangle(
            corner_radius=0.12, width=0.78, height=0.78,
            stroke_color=ORANGE, stroke_width=4.5, fill_opacity=0.0,
        ).move_to(orange_final.sq.get_center())
        glow_ring.add_updater(lambda m: m.move_to(orange_final.sq.get_center()))

        dim_anims = [
            red_cell.animate.set_stroke(opacity=0.4).set_fill(opacity=0.02),
            mem.animate.set_opacity(0.4),
            bag1.animate.set_opacity(0.4),
            bag2.animate.set_opacity(0.4),
            x_mark.animate.set_opacity(0.4),
        ]
        for idx, s in enumerate(stalks):
            if idx != 4:
                dim_anims.append(s.animate.set_opacity(0.4))
            else:
                dim_anims.append(s.stem.animate.set_opacity(0.4))
                for t in s.tiles[:-1]:
                    dim_anims.append(t.animate.set_opacity(0.4))
                dim_anims.append(s.joints.animate.set_opacity(0.4))
        self.play(*dim_anims, FadeIn(glow_ring), run_time=0.9)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        # Rebuild end state of s00_hook at 30% opacity while stalks keep swaying
        mem = make_membrane().set_opacity(0.30)
        red_cell = make_red_cell_disc().set_stroke(opacity=0.30).set_fill(opacity=0.02)
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind="A" if i == 4 else "glucose", seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        for idx, s in enumerate(stalks):
            if idx != 4:
                _scale_mob_opacity(s, 0.30)
            else:
                _scale_mob_opacity(s.stem, 0.30)
                for t in s.tiles[:-1]:
                    _scale_mob_opacity(t, 0.30)
                _scale_mob_opacity(s.joints, 0.30)

        orange_tip = stalks[4].tip_tile()
        glow_ring = RoundedRectangle(
            corner_radius=0.12, width=0.78, height=0.78,
            stroke_color=ORANGE, stroke_width=4.5, fill_opacity=0.0,
        ).move_to(orange_tip.sq.get_center())
        glow_ring.add_updater(lambda m: m.move_to(orange_tip.sq.get_center()))

        bag1 = make_blood_bag().move_to([3.5, 2.55, 0]).set_opacity(0.30)
        bag2 = make_blood_bag().move_to([5.1, 2.55, 0]).set_opacity(0.30)
        x_mark = make_red_x(bag2.get_center(), size=0.85).set_opacity(0.30)
        tag = make_schematic_tag()

        # Title and gold rule cleanly above the stalks and below the top rim
        title = T("Which Sugar Sits Where", size=54, font=TITLE_FONT, color=TEXT)
        fit(title, max_w=10.5)
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4.5)
        title_grp = VGroup(title, rule).arrange(DOWN, buff=0.22).move_to([0.0, 1.24, 0])

        self.add(red_cell, mem, stalks, glow_ring, bag1, bag2, x_mark, tag, title_grp)
        self.wait(1.55)

        # Title out in the last ~0.45 s; bags slide away, red cell fades, stalks brighten for s02
        glow_ring.clear_updaters()
        self.play(
            FadeOut(title_grp),
            FadeOut(glow_ring),
            bag1.animate.shift(RIGHT * 4.5).set_opacity(0),
            bag2.animate.shift(RIGHT * 4.5).set_opacity(0),
            x_mark.animate.shift(RIGHT * 4.5).set_opacity(0),
            FadeOut(red_cell),
            mem.animate.set_opacity(1.0),
            *[_anim_mob_opacity(s, 1.0) for s in stalks],
            run_time=0.45,
        )
        self.finish()


class S02Coat(SpokenScene):
    def construct(self):
        mem = make_membrane()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind="A" if i == 4 else "glucose", seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        tag = make_schematic_tag()
        self.add(mem, stalks, tag)

        self.at("Most proteins")
        prot_idxs = [1, 3, 5, 7]
        proteins = VGroup()
        lift_anims = []
        for idx in prot_idxs:
            p = make_protein_blob().move_to([STALK_XS_8[idx], MEM_Y_TOP - 0.08, 0])
            proteins.add(p)
            stalks[idx].shift_base(UP * 0.25)
            lift_anims.append(FadeIn(p, shift=UP * 0.25))
        prot_label = T("protein", size=30, color=PURPLE).move_to([STALK_XS_8[5], -3.22, 0])
        self.play(*lift_anims, FadeIn(prot_label), run_time=0.9)

        self.at("and most")
        # Secreted glycoprotein (index 1: protein + stalk[1]) detaches and drifts up-left out of frame
        secreted_p = proteins[0]
        secreted_s = stalks[1]
        secreted_s.clear_updaters()
        self.play(
            FadeOut(VGroup(secreted_p, secreted_s), shift=LEFT * 3.5 + UP * 3.5),
            run_time=1.6,
        )

        self.at("Every link")
        # Ease in on one stalk at centre filling 60% of frame height (4 large tiles)
        other_mobs = [s for i, s in enumerate(stalks) if i != 1] + list(proteins[1:]) + [prot_label]
        zoom_stalk = SwayStalk(0.0, y_base=MEM_Y_TOP, n_tiles=4, tip_kind="glucose",
                               tile_w=0.92, step_y=1.18, amp=0.04, period=3.0, seed=0)
        self.play(
            *[FadeOut(m) for m in other_mobs],
            FadeIn(zoom_stalk),
            run_time=0.9,
        )

        # Each GOLD joint flashes in turn from base to tip + one label 'anomeric carbon'
        ano_label = T("anomeric carbon", size=30, color=GOLD).move_to([2.95, zoom_stalk.joints[1].get_y(), 0])
        ano_arrow = Arrow(
            ano_label.get_left() + LEFT * 0.12,
            zoom_stalk.joints[1].get_right() + RIGHT * 0.15,
            color=GOLD, stroke_width=3.5, buff=0.0, max_tip_length_to_length_ratio=0.18,
        )
        self.play(FadeIn(ano_label), GrowArrow(ano_arrow), run_time=0.6)

        for j in zoom_stalk.joints:
            ring = Circle(radius=0.22, stroke_color=GOLD, stroke_width=4).move_to(j.get_center())
            self.play(FadeIn(ring), j.animate.scale(1.6), run_time=0.32)
            self.play(FadeOut(ring), j.animate.scale(1 / 1.6), run_time=0.32)

        self.at("first rule")
        # Bright GOLD dots mark every joint and stay
        lit_dots = VGroup(*[
            Dot(j.get_center(), radius=0.14, color=GOLD) for j in zoom_stalk.joints
        ])
        for d, j in zip(lit_dots, zoom_stalk.joints):
            d.add_updater(lambda mob, j_ref=j: mob.move_to(j_ref.get_center()))
        self.play(FadeIn(lit_dots), run_time=0.5)

        self.at("what the coat says")
        q_mark = T("?", size=48, color=TEXT, weight=BOLD).move_to([-1.65, zoom_stalk.tiles[2].get_y(), 0])
        self.play(FadeIn(q_mark, scale=1.2), run_time=0.6)
        self.finish()


class S03H(SpokenScene):
    def construct(self):
        mem = make_membrane()
        tag = make_schematic_tag()
        # Three identical stalks side by side, ~50% of frame height
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3, tip_kind="glucose",
                      tile_w=0.76, step_y=0.98, amp=0.05, period=3.0, seed=i)
            for i, x in enumerate(STALK_XS_3)
        ])
        self.add(mem, stalks, tag)

        self.at("shared core chain")
        glows = VGroup(*[
            SurroundingRectangle(s.tiles, color=TEXT, buff=0.10, corner_radius=0.12, stroke_width=3.5)
            for s in stalks
        ])
        for g, s in zip(glows, stalks):
            g.add_updater(lambda m, sr=s: m.move_to(sr.tiles.get_center()))
        brace = Brace(stalks[0].tiles, LEFT, color=TEXT, buff=0.22)
        h_label = T("H antigen", size=30, color=TEXT).next_to(brace, LEFT, buff=0.16)
        self.play(FadeIn(glows), FadeIn(brace), FadeIn(h_label), run_time=0.9)

        self.at("lands on its tip")
        for g in glows:
            g.clear_updaters()
        dashed_tips = VGroup()
        for x, s in zip(STALK_XS_3, stalks):
            top_y = s.tiles[-1].get_center()[1] + 0.98
            box = DashedVMobject(
                RoundedRectangle(corner_radius=0.09, width=0.76, height=0.76, stroke_color=TEXT, stroke_width=2.5),
                num_dashes=16,
            ).move_to([x, top_y, 0])
            j = DashedLine(s.tiles[-1].get_top(), box.get_bottom(), color=GOLD, stroke_width=2.8)
            dashed_tips.add(VGroup(j, box))
        self.play(FadeOut(glows), FadeIn(dashed_tips), run_time=0.8)

        self.at("the enzyme you inherit")
        names = ["A enzyme", "B enzyme", "O allele"]
        enzymes = VGroup()
        enz_labels = VGroup()
        for x, name in zip(STALK_XS_3, names):
            pac = make_enzyme_pacman(radius=0.52, color=PURPLE).move_to([x, 2.25, 0])
            lab = T(name, size=30, color=PURPLE).move_to([x, 3.10, 0])
            enzymes.add(pac)
            enz_labels.add(lab)
        self.play(
            *[FadeIn(e, shift=DOWN * 0.4) for e in enzymes],
            *[FadeIn(l, shift=DOWN * 0.3) for l in enz_labels],
            run_time=0.9,
        )
        self.finish()


class S04Abo(SpokenScene):
    def construct(self):
        mem = make_membrane()
        tag = make_schematic_tag()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3, tip_kind="glucose",
                      tile_w=0.76, step_y=0.98, amp=0.05, period=3.0, seed=i)
            for i, x in enumerate(STALK_XS_3)
        ])
        dashed_tips = VGroup()
        for x, s in zip(STALK_XS_3, stalks):
            top_y = s.tiles[-1].get_center()[1] + 0.98
            box = DashedVMobject(
                RoundedRectangle(corner_radius=0.09, width=0.76, height=0.76, stroke_color=TEXT, stroke_width=2.5),
                num_dashes=16,
            ).move_to([x, top_y, 0])
            j = DashedLine(s.tiles[-1].get_top(), box.get_bottom(), color=GOLD, stroke_width=2.8)
            dashed_tips.add(VGroup(j, box))

        names = ["A enzyme", "B enzyme", "O allele"]
        enzymes = VGroup(*[make_enzyme_pacman(radius=0.52, color=PURPLE).move_to([x, 2.25, 0]) for x in STALK_XS_3])
        enz_labels = VGroup(*[T(n, size=30, color=PURPLE).move_to([x, 3.10, 0]) for x, n in zip(STALK_XS_3, names)])
        self.add(mem, stalks, dashed_tips, enzymes, enz_labels, tag)

        # Beat 1: A enzyme adds ORANGE tile
        self.at("adds one sugar")
        a_tip_pos = dashed_tips[0][1].get_center()
        a_tile = make_stalk_tile("A", width=0.76).move_to(enzymes[0].get_bottom() + DOWN * 0.15)
        a_joint = Dot([STALK_XS_3[0], (stalks[0].tiles[-1].get_center()[1] + a_tip_pos[1]) / 2, 0],
                      radius=0.08, color=GOLD)
        lab_a = T("type A", size=32, color=ORANGE).move_to([STALK_XS_3[0], -3.22, 0])
        self.play(FadeIn(a_tile), run_time=0.25)
        self.play(
            enzymes[0].animate.shift(DOWN * 0.45),
            a_tile.animate.move_to(a_tip_pos),
            FadeOut(dashed_tips[0]),
            FadeIn(a_joint),
            run_time=0.85,
        )
        stalks[0].n_tiles = 4
        stalks[0].tiles.add(a_tile)
        stalks[0].joints.add(a_joint)
        stalks[0]._record_rest()
        self.play(enzymes[0].animate.shift(UP * 0.45), FadeIn(lab_a), run_time=0.45)

        # Beat 2: B enzyme adds PINK tile
        self.at("The B enzyme")
        b_tip_pos = dashed_tips[1][1].get_center()
        b_tile = make_stalk_tile("B", width=0.76).move_to(enzymes[1].get_bottom() + DOWN * 0.15)
        b_joint = Dot([STALK_XS_3[1], (stalks[1].tiles[-1].get_center()[1] + b_tip_pos[1]) / 2, 0],
                      radius=0.08, color=GOLD)
        lab_b = T("type B", size=32, color=PINK).move_to([STALK_XS_3[1], -3.22, 0])
        self.play(FadeIn(b_tile), run_time=0.25)
        self.play(
            enzymes[1].animate.shift(DOWN * 0.45),
            b_tile.animate.move_to(b_tip_pos),
            FadeOut(dashed_tips[1]),
            FadeIn(b_joint),
            run_time=0.85,
        )
        stalks[1].n_tiles = 4
        stalks[1].tiles.add(b_tile)
        stalks[1].joints.add(b_joint)
        stalks[1]._record_rest()
        self.play(enzymes[1].animate.shift(UP * 0.45), FadeIn(lab_b), run_time=0.4)

        # Beat 3: by the same bond -> two new GOLD joints flash together
        self.at("by the same bond")
        ra = Circle(radius=0.24, stroke_color=GOLD, stroke_width=4.5).move_to(a_joint)
        rb = Circle(radius=0.24, stroke_color=GOLD, stroke_width=4.5).move_to(b_joint)
        self.play(FadeIn(ra), FadeIn(rb), a_joint.animate.scale(1.5), b_joint.animate.scale(1.5), run_time=0.45)
        self.play(FadeOut(ra), FadeOut(rb), a_joint.animate.scale(1 / 1.5), b_joint.animate.scale(1 / 1.5), run_time=0.45)

        # Beat 4: O allele fades to empty outline, right tip stays bare, label 'type O', enzymes fade out
        self.at("The O allele")
        o_outline = DashedVMobject(
            Circle(radius=0.52, stroke_color=PURPLE, stroke_width=2.5),
            num_dashes=16,
        ).move_to(enzymes[2].get_center())
        lab_o = T("type O", size=32, color=TEXT).move_to([STALK_XS_3[2], -3.22, 0])
        self.play(
            FadeOut(enzymes[2]),
            FadeIn(o_outline),
            FadeOut(dashed_tips[2]),
            FadeIn(lab_o),
            run_time=0.85,
        )
        self.play(
            FadeOut(enzymes[0]), FadeOut(enzymes[1]), FadeOut(o_outline), FadeOut(enz_labels),
            run_time=0.75,
        )
        self.finish()


class S05C2(SpokenScene):
    def construct(self):
        mem = make_membrane()
        tag = make_schematic_tag()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP,
                      n_tiles=4 if i < 2 else 3,
                      tip_kind="A" if i == 0 else ("B" if i == 1 else "glucose"),
                      tile_w=0.76, step_y=0.98, amp=0.05, period=3.0, seed=i)
            for i, x in enumerate(STALK_XS_3)
        ])
        labs = VGroup(
            T("type A", size=32, color=ORANGE).move_to([STALK_XS_3[0], -3.22, 0]),
            T("type B", size=32, color=PINK).move_to([STALK_XS_3[1], -3.22, 0]),
            T("type O", size=32, color=TEXT).move_to([STALK_XS_3[2], -3.22, 0]),
        )
        self.add(mem, stalks, labs, tag)

        self.at("A and B sugars")
        tip_a = stalks[0].tip_tile()
        tip_b = stalks[1].tip_tile()
        ghost_a = DashedVMobject(
            RoundedRectangle(corner_radius=0.09, width=0.76, height=0.76, stroke_color=ORANGE, stroke_width=2.5),
            num_dashes=16,
        ).move_to(tip_a.sq.get_center())
        ghost_b = DashedVMobject(
            RoundedRectangle(corner_radius=0.09, width=0.76, height=0.76, stroke_color=PINK, stroke_width=2.5),
            num_dashes=16,
        ).move_to(tip_b.sq.get_center())

        big_a = make_glucose_tile(1.60, color=ORANGE, fill_op=0.70, show_labels=False).move_to([-2.15, 2.52, 0])
        big_b = make_glucose_tile(1.60, color=PINK, fill_op=0.70, show_labels=False).move_to([2.15, 2.52, 0])

        # C2 badges cleanly outside the bottom-right edge of each big tile, clear of dashed ghosts
        c2_sq = RoundedRectangle(corner_radius=0.05, width=0.34, height=0.34,
                                 stroke_color=TEXT, stroke_width=3.0, fill_color=TEXT, fill_opacity=0.85
                                 ).move_to(big_a.sq.get_corner(DR) + UP * 0.20 + RIGHT * 0.28)
        c2_dot = Dot(big_b.sq.get_corner(DR) + UP * 0.20 + RIGHT * 0.28, radius=0.13, color=TEXT)
        c2_lab_a = T("C2", size=26, color=TEXT).next_to(c2_sq, RIGHT, buff=0.16)
        c2_lab_b = T("C2", size=26, color=TEXT).next_to(c2_dot, RIGHT, buff=0.10)

        tip_a.set_opacity(0)
        tip_b.set_opacity(0)
        self.add(ghost_a, ghost_b)
        start_a = make_glucose_tile(0.76, color=ORANGE, fill_op=0.70, show_labels=False).move_to(ghost_a.get_center())
        start_b = make_glucose_tile(0.76, color=PINK, fill_op=0.70, show_labels=False).move_to(ghost_b.get_center())
        self.add(start_a, start_b)

        self.play(Transform(start_a, big_a), Transform(start_b, big_b), run_time=1.0)
        self.play(FadeIn(c2_sq), FadeIn(c2_dot), FadeIn(c2_lab_a), FadeIn(c2_lab_b), run_time=0.45)

        self.at("only one carbon")
        for _ in range(2):
            self.play(
                c2_sq.animate.scale(1.25).set_stroke(GOLD, width=4.5),
                c2_dot.animate.scale(1.35).set_color(GOLD),
                start_a.sq.animate.set_stroke(TEXT, width=4.5),
                start_b.sq.animate.set_stroke(TEXT, width=4.5),
                run_time=0.55,
            )
            self.play(
                c2_sq.animate.scale(1 / 1.25).set_stroke(TEXT, width=3.0),
                c2_dot.animate.scale(1 / 1.35).set_color(TEXT),
                start_a.sq.animate.set_stroke(ORANGE, width=2.8),
                start_b.sq.animate.set_stroke(PINK, width=2.8),
                run_time=0.55,
            )

        self.at("sets your blood type")
        self.play(FadeOut(c2_sq), FadeOut(c2_dot), FadeOut(c2_lab_a), FadeOut(c2_lab_b), run_time=0.25)
        back_a = make_stalk_tile("A", width=0.76).move_to(ghost_a.get_center())
        back_b = make_stalk_tile("B", width=0.76).move_to(ghost_b.get_center())
        self.play(Transform(start_a, back_a), Transform(start_b, back_b), run_time=0.75)
        self.remove(start_a, start_b, ghost_a, ghost_b)
        tip_a.set_opacity(1)
        tip_b.set_opacity(1)
        self.play(labs[0].animate.scale(1.18), labs[1].animate.scale(1.18), run_time=0.3)
        self.play(labs[0].animate.scale(1 / 1.18), labs[1].animate.scale(1 / 1.18), run_time=0.3)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        mem = make_membrane()
        tag = make_schematic_tag()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP,
                      n_tiles=4 if i < 2 else 3,
                      tip_kind="A" if i == 0 else ("B" if i == 1 else "glucose"),
                      tile_w=0.76, step_y=0.98, amp=0.05, period=3.0, seed=i)
            for i, x in enumerate(STALK_XS_3)
        ])
        _scale_mob_opacity(stalks, 0.70)
        labs = VGroup(
            T("type A", size=32, color=ORANGE).move_to([STALK_XS_3[0], -3.22, 0]),
            T("type B", size=32, color=PINK).move_to([STALK_XS_3[1], -3.22, 0]),
            T("type O", size=32, color=TEXT).move_to([STALK_XS_3[2], -3.22, 0]),
        )
        self.add(mem, stalks, labs, tag)

        self.at("second rule")
        gold_rule = Line([-5.6, 2.15, 0], [5.6, 2.15, 0], color=GOLD, stroke_width=4.0)
        self.play(Create(gold_rule), run_time=0.9)

        chips = make_rule_chips(size=30).move_to([0.0, 2.85, 0])

        self.at("which sugar")
        glow_a = SurroundingRectangle(stalks[0].tip_tile().sq, color=ORANGE, buff=0.08, corner_radius=0.10, stroke_width=4.5)
        glow_b = SurroundingRectangle(stalks[1].tip_tile().sq, color=PINK, buff=0.08, corner_radius=0.10, stroke_width=4.5)
        glow_a.add_updater(lambda m: m.move_to(stalks[0].tip_tile().sq.get_center()))
        glow_b.add_updater(lambda m: m.move_to(stalks[1].tip_tile().sq.get_center()))
        _scale_mob_opacity(stalks[0].tip_tile(), 1.0)
        _scale_mob_opacity(stalks[1].tip_tile(), 1.0)
        self.play(FadeIn(chips[0]), FadeIn(glow_a), FadeIn(glow_b), run_time=0.75)

        self.at("which bond")
        j_a = stalks[0].joints[-1]
        j_b = stalks[1].joints[-1]
        ring_a = Circle(radius=0.22, stroke_color=GOLD, stroke_width=4.5).move_to(j_a)
        ring_b = Circle(radius=0.22, stroke_color=GOLD, stroke_width=4.5).move_to(j_b)
        ring_a.add_updater(lambda m: m.move_to(j_a.get_center()))
        ring_b.add_updater(lambda m: m.move_to(j_b.get_center()))
        self.play(FadeIn(chips[1]), FadeIn(ring_a), FadeIn(ring_b), run_time=0.7)

        self.at("which position")
        pos_arrow = Arrow(
            [1.1, 1.45, 0],
            stalks[1].tip_tile().get_right() + RIGHT * 0.14,
            color=TEAL, stroke_width=4.5, buff=0.0, max_tip_length_to_length_ratio=0.22,
        )
        pos_arrow.add_updater(lambda m: m.put_start_and_end_on(
            [1.1, 1.45, 0], stalks[1].tip_tile().get_right() + RIGHT * 0.14
        ))
        self.play(FadeIn(chips[2]), GrowArrow(pos_arrow), run_time=0.7)
        self.finish()


class S07Address(SpokenScene):
    def construct(self):
        chips = make_rule_chips(size=28).move_to([0.0, 3.22, 0])
        mem = make_membrane(y_top=-2.35, y_bot=-2.65, gap=(2.6, 4.0))
        tag = make_schematic_tag()

        lysosome = Circle(radius=1.52, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.07).move_to([-4.3, 0.35, 0])
        lyso_lab = T("lysosome", size=30, color=TEXT).move_to([-4.3, 2.22, 0])

        blood_arrow = Arrow([3.3, -2.15, 0], [3.3, -2.92, 0], color=TEXT, stroke_width=4.0, buff=0.0)
        blood_lab = T("blood", size=30, color=TEXT).move_to([3.3, -3.25, 0])

        self.add(chips, mem, lysosome, lyso_lab, blood_arrow, blood_lab, tag)

        def make_tagged_enzyme(pos, with_tag=True):
            blob = make_protein_blob(width=0.90, height=0.50, color=PURPLE).move_to(pos)
            tile = make_stalk_tile("glucose", width=0.38).next_to(blob, UP, buff=0.08)
            grp = VGroup(blob, tile)
            if with_tag:
                p_pill = RoundedRectangle(corner_radius=0.10, width=0.46, height=0.46,
                                          stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.22
                                          ).next_to(tile.tab, UP, buff=0.08)
                p_txt = T("P", size=28, color=TEAL).move_to(p_pill)
                p_badge = VGroup(p_pill, p_txt)
                grp.p_pill = p_pill
                grp.p_txt = p_txt
                grp.p_badge = p_badge
                grp.add(p_badge)
            else:
                grp.p_pill = grp.p_txt = grp.p_badge = None
            return grp

        self.at("mannose")
        hero = make_tagged_enzyme([0.0, 0.25, 0], with_tag=True)
        m6p_lab = T("mannose-6-phosphate tag", size=28, color=TEAL).move_to([1.25, 2.05, 0])
        self.play(FadeIn(hero), FadeIn(m6p_lab), run_time=0.75)

        self.at("sends enzymes to the lysosome")
        e2 = make_tagged_enzyme([-0.95, -1.05, 0], with_tag=True)
        e3 = make_tagged_enzyme([0.95, -1.05, 0], with_tag=True)
        self.play(FadeIn(e2), FadeIn(e3), run_time=0.4)
        self.play(
            FadeOut(m6p_lab),
            hero.animate.scale(0.80).move_to([-4.30, 1.06, 0]),
            e2.animate.scale(0.80).move_to([-4.82, -0.24, 0]),
            e3.animate.scale(0.80).move_to([-3.78, -0.24, 0]),
            run_time=2.3,
        )

        self.at("Lose the ability")
        u1 = make_tagged_enzyme([-0.8, 0.75, 0], with_tag=True)
        u2 = make_tagged_enzyme([0.4, 0.10, 0], with_tag=True)
        u3 = make_tagged_enzyme([1.6, 0.85, 0], with_tag=True)
        self.play(FadeIn(u1), FadeIn(u2), FadeIn(u3), run_time=0.5)
        # Fade P letters out first, then flash RED X over the tag pill cleanly
        for u in (u1, u2, u3):
            u.p_badge.remove(u.p_txt)
        self.play(FadeOut(u1.p_txt), FadeOut(u2.p_txt), FadeOut(u3.p_txt), run_time=0.25)
        rx = make_red_x(u2.p_pill.get_center(), size=0.65)
        self.play(Create(rx), run_time=0.4)
        for u in (u1, u2, u3):
            u.remove(u.p_badge)
        self.play(FadeOut(rx), FadeOut(u1.p_badge), FadeOut(u2.p_badge), FadeOut(u3.p_badge), run_time=0.45)

        self.at("dumped into the blood")
        self.play(
            u1.animate.move_to([3.0, -1.35, 0]),
            u2.animate.move_to([3.3, -2.05, 0]),
            u3.animate.move_to([3.6, -1.15, 0]),
            run_time=1.3,
        )
        self.play(
            u1.animate.move_to([2.6, -3.2, 0]).set_opacity(0),
            u2.animate.move_to([3.3, -3.4, 0]).set_opacity(0),
            u3.animate.move_to([4.0, -3.2, 0]).set_opacity(0),
            run_time=1.0,
        )

        self.at("disease")
        icell_chip = boxed_label("I-cell disease", color=RED, size=30, fill_opacity=0.18).move_to([4.4, -0.5, 0])
        self.play(FadeIn(icell_chip, scale=1.08), run_time=0.6)
        self.finish()


def make_wobbling_lectin(target_stalk):
    """Build a single-pocket PURPLE lectin and its dotted contact line, looping an on-off wobble."""
    lectin = make_lectin_cap(width=1.9, height=0.72, n_pockets=1, color=PURPLE)
    lectin._wobble_t = 0.0
    lectin._angle = 0.0

    def wobble_clean(mob, dt):
        mob._wobble_t += dt
        u = 0.5 - 0.5 * np.cos(TAU * mob._wobble_t / 2.2)
        tip_top = target_stalk.tip_tile().get_top()
        lift = (u ** 1.5) * 0.95
        new_ang = 0.07 * np.sin(mob._wobble_t * 4.5) * u
        mob.rotate(new_ang - mob._angle)
        mob._angle = new_ang
        mob.move_to([tip_top[0], tip_top[1] + 0.22 + lift, 0])

    contact_line = DashedLine(ORIGIN, UP * 0.3, color=TEXT, stroke_width=2.8, dash_length=0.07)

    def update_contact(mob):
        tip_top = target_stalk.tip_tile().get_top()
        pocket_y = lectin.get_bottom()[1] + 0.16
        if pocket_y - tip_top[1] < 0.55:
            mob.set_opacity(1.0)
            mob.put_start_and_end_on(tip_top + UP * 0.02, [tip_top[0], pocket_y, 0])
        else:
            mob.set_opacity(0.0)

    lectin.add_updater(wobble_clean)
    contact_line.add_updater(update_contact)
    return lectin, contact_line


class S08Lectin(SpokenScene):
    def construct(self):
        mem = make_membrane()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind=DEFAULT_TIPS_8[i], seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        tag = make_schematic_tag()
        self.add(mem, stalks, tag)

        self.at("readers are lectins")
        target_stalk = stalks[4]  # ORANGE tip at x = 0.7
        lectin = make_lectin_cap(width=1.9, height=0.72, n_pockets=1, color=PURPLE)
        lectin.move_to([target_stalk.x_base, 2.35, 0])
        lectin_lab = T("lectin", size=30, color=PURPLE).move_to([2.8, 2.35, 0])
        self.play(FadeIn(lectin, shift=DOWN * 0.4), FadeIn(lectin_lab), run_time=1.0)

        self.at("bind specific sugar chains")
        dock_y = target_stalk.tip_anchor()[1] + 0.16
        self.play(
            lectin.animate.move_to([target_stalk.x_base, dock_y, 0]),
            lectin_lab.animate.move_to([2.8, 1.55, 0]),
            run_time=1.1,
        )

        self.at("grip is weak")
        self.remove(lectin)
        w_lectin, contact_line = make_wobbling_lectin(target_stalk)
        self.add(w_lectin, contact_line)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        mem = make_membrane()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind=DEFAULT_TIPS_8[i], seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        lectin, contact_line = make_wobbling_lectin(stalks[4])
        lectin_lab = T("lectin", size=30, color=PURPLE).move_to([2.8, 1.55, 0])
        tag = make_schematic_tag()
        self.add(mem, stalks, lectin, contact_line, lectin_lab, tag)

        self.at("firmly enough")
        q_card = question_card("How to hold on?", y=2.65, color=TEXT, size=38, max_w=8.0)
        q_box = RoundedRectangle(
            corner_radius=0.16, width=q_card.width + 0.7, height=q_card.height + 0.45,
            stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.9,
        ).move_to(q_card)
        self.play(FadeIn(q_box, shift=DOWN * 0.3), FadeIn(q_card, shift=DOWN * 0.3), run_time=0.8)
        self.finish()


class S10Think(PredictPause):
    QUESTION = "How to hold on?"
    CARD = {"y": 2.65, "color": TEXT, "size": 38, "max_w": 8.0}
    RING_AT = (2.75, 2.65, 0)
    SECONDS = 4.5

    def backdrop(self):
        mem = make_membrane()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind=DEFAULT_TIPS_8[i], seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        lectin, contact_line = make_wobbling_lectin(stalks[4])
        lectin_lab = T("lectin", size=30, color=PURPLE).move_to([2.8, 1.55, 0])
        q_card_ref = question_card(self.QUESTION, **self.CARD)
        q_box = RoundedRectangle(
            corner_radius=0.16, width=q_card_ref.width + 0.7, height=q_card_ref.height + 0.45,
            stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.9,
        ).move_to(q_card_ref)
        tag = make_schematic_tag()
        return VGroup(mem, stalks, lectin, contact_line, lectin_lab, q_box, tag)


class S11Multi(SpokenScene):
    def construct(self):
        # 5 neighbouring stalks in middle carry ORANGE tips of uniform height so all 5 align cleanly with pockets
        tips_multi = ["sialic", "A", "A", "A", "A", "A", "B", "sialic"]
        heights_multi = [4, 3, 3, 3, 3, 3, 3, 4]
        mem = make_membrane()
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=heights_multi[i],
                      tip_kind=tips_multi[i], seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        target_stalks = [stalks[i] for i in range(1, 6)]
        lectin_small = make_lectin_cap(width=1.9, height=0.72, n_pockets=1, color=PURPLE)
        lectin_small.move_to([stalks[4].x_base, stalks[4].tip_tile().get_top()[1] + 0.5, 0])
        q_card = question_card("How to hold on?", y=2.65, color=TEXT, size=38, max_w=8.0)
        q_box = RoundedRectangle(
            corner_radius=0.16, width=q_card.width + 0.7, height=q_card.height + 0.45,
            stroke_color=GOLD, stroke_width=2.8, fill_color=BG, fill_opacity=0.9,
        ).move_to(q_card)
        tag = make_schematic_tag()
        self.add(mem, stalks, lectin_small, q_box, q_card, tag)

        self.play(FadeOut(q_box, shift=UP * 0.4), FadeOut(q_card, shift=UP * 0.4), run_time=0.45)

        self.at("many sugars at once")
        # Widen into a long PURPLE bar with 5 pockets aligned above stalks[1..5] (x = -3.5 .. +2.1, centre = -0.7)
        pocket_xs = [s.x_base - (-0.7) for s in target_stalks]
        bar_y = 0.60
        lectin_bar = make_lectin_cap(width=6.6, height=0.82, n_pockets=5, pocket_xs=pocket_xs, color=PURPLE)
        lectin_bar.move_to([-0.7, bar_y, 0])
        self.play(Transform(lectin_small, lectin_bar), run_time=0.95)

        # Five dotted contact lines light between pockets and tips
        contacts = VGroup()
        for s in target_stalks:
            ln = DashedLine(
                s.tip_tile().get_top() + UP * 0.03,
                [s.x_base, lectin_small.get_bottom()[1] + 0.16, 0],
                color=TEXT, stroke_width=3.0, dash_length=0.07,
            )
            contacts.add(ln)
        self.play(FadeIn(contacts), run_time=0.5)

        self.at("weak handholds")
        # Contacts flicker independently using deterministic RNG phases while bar stays down
        rng = np.random.default_rng(7)
        phases = rng.uniform(0, TAU, size=5)
        freqs = rng.uniform(3.2, 4.8, size=5)
        contacts._t = 0.0

        def flicker_contacts(mob, dt):
            mob._t += dt
            for idx, (ln, s) in enumerate(zip(mob, target_stalks)):
                tip_top = s.tip_tile().get_top()
                ln.put_start_and_end_on(tip_top + UP * 0.03, [s.x_base, lectin_small.get_bottom()[1] + 0.16, 0])
                v = np.sin(mob._t * freqs[idx] + phases[idx])
                ln.set_opacity(0.15 if v < -0.45 else 1.0)

        contacts.add_updater(flicker_contacts)

        self.at("selective grip")
        # Bar holds steady and gets a brief bright stroke pulse
        self.play(lectin_small.animate.set_stroke(TEXT, width=4.5), run_time=0.45)
        self.play(lectin_small.animate.set_stroke(PURPLE, width=3.5), run_time=0.45)

        self.at("hook and loop")
        # Small inset at upper right: cartoon strip of hooks meeting loops
        inset = RoundedRectangle(corner_radius=0.16, width=4.1, height=2.25,
                                 stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.92).move_to([4.15, 2.25, 0])
        inset_lab = T("hook and loop", size=24, color=TEXT).move_to([4.15, 3.02, 0])
        top_strip = Line([2.55, 2.52, 0], [5.75, 2.52, 0], stroke_color=TEXT, stroke_width=3.5)
        bot_strip = Line([2.55, 1.55, 0], [5.75, 1.55, 0], stroke_color=TEXT, stroke_width=3.5)
        hooks = VGroup()
        loops = VGroup()
        for hx in np.linspace(2.85, 5.45, 5):
            hk = VMobject(stroke_color=TEXT, stroke_width=3.0)
            hk.set_points_smoothly([
                [hx, 2.52, 0], [hx, 2.15, 0], [hx + 0.12, 2.02, 0], [hx + 0.18, 2.14, 0]
            ])
            lp = Arc(radius=0.18, start_angle=0.0, angle=PI, arc_center=[hx + 0.04, 1.55, 0],
                     stroke_color=TEXT, stroke_width=3.0)
            hooks.add(hk)
            loops.add(lp)

        self.play(FadeIn(inset), FadeIn(inset_lab), FadeIn(top_strip), FadeIn(bot_strip),
                  FadeIn(hooks), FadeIn(loops), run_time=0.8)

        self.at("No single hook")
        # One hook alone pops free around its top_strip attachment without piercing the strip
        hx2 = 4.15
        pulled_hook = VMobject(stroke_color=GOLD, stroke_width=3.2)
        pulled_hook.set_points_smoothly([
            [hx2, 2.52, 0], [hx2 + 0.14, 2.24, 0], [hx2 + 0.30, 2.15, 0], [hx2 + 0.38, 2.26, 0]
        ])
        self.play(Transform(hooks[2], pulled_hook), run_time=0.65)
        self.finish()


class S12Selectin(SpokenScene):
    def construct(self):
        mem = make_membrane()
        # Leave x = 3.9 open for the site of injury spark
        xs_sel = [-5.2, -3.9, -2.6, -1.3, 0.0, 1.3, 2.6, 5.2]
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=2, tip_kind=DEFAULT_TIPS_8[i],
                      tile_w=0.54, step_y=0.68, amp=0.04, period=3.0, seed=i)
            for i, x in enumerate(xs_sel)
        ])
        tag = make_schematic_tag()

        # Left-to-right flow of pale dots above vessel wall (explicitly in visual note)
        rng = np.random.default_rng(12)
        flow_dots = VGroup()
        for _ in range(14):
            d = Dot(
                [rng.uniform(-6.0, 6.0), rng.uniform(-0.3, 2.7), 0],
                radius=0.05, color=TEXT,
            ).set_opacity(0.35)
            d._vx = rng.uniform(1.6, 2.2)

            def drift(m, dt):
                m.shift(RIGHT * m._vx * dt)
                if m.get_x() > 6.3:
                    m.shift(LEFT * 12.6)

            d.add_updater(drift)
            flow_dots.add(d)

        # PURPLE selectin many-pocket bars on the wall, raised clear of stalk tips and minus badges
        selectin_xs = [-3.2, -1.0, 1.2]
        selectins = VGroup(*[
            make_lectin_cap(width=1.65, height=0.45, n_pockets=3, color=PURPLE).rotate(PI).move_to([sx, -0.40, 0])
            for sx in selectin_xs
        ])
        sel_lab = T("selectins", size=30, color=PURPLE).move_to([-4.6, -3.22, 0])

        # Immune cell rolling from left
        cell_r = 0.88
        cell_ring = Circle(radius=cell_r, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.10)
        cell_bumps = VGroup(*[
            Dot([cell_r * np.cos(a), cell_r * np.sin(a), 0], radius=0.07, color=ORANGE)
            for a in np.linspace(0, TAU, 10, endpoint=False)
        ])
        immune_cell = VGroup(cell_ring, cell_bumps).move_to([-5.6, 0.77, 0])
        immune_lab = T("immune cell", size=30, color=TEXT)
        immune_lab.add_updater(lambda m: m.next_to(immune_cell, UP, buff=0.22))

        self.add(mem, stalks, flow_dots, selectins, sel_lab, immune_cell, immune_lab, tag)

        # Computed rolling deceleration: fast initially, then step-drag at each selectin zone
        self.at("Selectins")
        self.play(
            *[s.animate.set_stroke(PURPLE, width=4.5) for s in selectins],
            immune_cell.animate.shift(RIGHT * 2.2).rotate(-2.2 / cell_r),
            run_time=1.8, rate_func=linear,
        )

        # Active contact line when passing selectins
        grip_line = DashedLine(ORIGIN, DOWN * 0.4, color=GOLD, stroke_width=3.0)

        def update_grip(mob):
            cx = immune_cell.get_center()[0]
            near = [sx for sx in selectin_xs if abs(cx - sx) < 0.9]
            if near:
                sx = near[0]
                mob.set_opacity(1.0)
                mob.put_start_and_end_on(immune_cell.get_bottom() + UP * 0.05, [sx, -0.17, 0])
            else:
                mob.set_opacity(0.0)

        grip_line.add_updater(update_grip)
        self.add(grip_line)

        self.at("slow circulating immune cells")
        # Each touch slows it more: 1.5 -> 1.1 -> 0.7 u
        self.play(immune_cell.animate.shift(RIGHT * 1.9).rotate(-1.9 / cell_r), run_time=1.1, rate_func=linear)
        self.play(immune_cell.animate.shift(RIGHT * 1.5).rotate(-1.5 / cell_r), run_time=1.3, rate_func=linear)

        self.at("site of injury")
        # Small WHITE spark icon (not RED) on the wall ahead; cell slows to a near stop beside it
        spark = Star(n=6, outer_radius=0.32, inner_radius=0.13, stroke_color=TEXT, stroke_width=2.8,
                     fill_color=TEXT, fill_opacity=0.65).move_to([3.9, -1.95, 0])
        injury_lab = T("site of injury", size=28, color=TEXT).move_to([4.15, -0.35, 0])
        self.play(
            FadeIn(spark, scale=1.2),
            FadeIn(injury_lab),
            immune_cell.animate.shift(RIGHT * 1.4).rotate(-1.4 / cell_r),
            run_time=1.6, rate_func=rate_functions.ease_out_cubic,
        )
        self.finish()


class S13Flu(SpokenScene):
    def construct(self):
        dimple = ValueTracker(0.0)
        # Space 3 centre stalks nicely under the virus spikes
        xs = [-4.6, -3.3, -2.0, -0.6, 0.625, 1.85, 3.25, 4.6]
        mem = make_membrane(dimple_tracker=dimple, dimple_x=0.625)
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3, tip_kind="sialic", seed=i)
            for i, x in enumerate(xs)
        ])
        airway_lab = T("airway cell", size=30, color=TEXT).move_to([-4.6, -3.22, 0])
        sialic_lab = T("sialic acid", size=30, color=MAGENTA).move_to([-3.8, 1.35, 0])
        sialic_arrow = Arrow(
            sialic_lab.get_bottom() + DOWN * 0.08,
            stalks[1].tip_tile().get_top() + UP * 0.12,
            color=MAGENTA, stroke_width=3.5, buff=0.0,
        )
        tag = make_schematic_tag()
        self.add(mem, stalks, airway_lab, sialic_lab, sialic_arrow, tag)

        self.at("The flu virus")
        virus = make_virus(radius=0.88, n_spikes=12).move_to([4.5, 2.35, 0])
        self.play(FadeIn(virus), virus.animate.move_to([2.0, 1.75, 0]), run_time=1.5)

        self.at("hemagglutinin")
        # Highlight spike 4 (upper-right) with label 'hemagglutinin'
        hi_spike = virus.spikes[4]
        hema_lab = T("hemagglutinin", size=30, color=PURPLE).move_to([4.5, 2.85, 0])
        hema_arrow = Arrow(
            hema_lab.get_left() + LEFT * 0.1,
            hi_spike.get_center() + RIGHT * 0.12,
            color=PURPLE, stroke_width=3.5, buff=0.0,
        )
        self.play(
            hi_spike.animate.set_stroke(TEXT, width=5.0),
            FadeIn(hema_lab), GrowArrow(hema_arrow),
            run_time=0.9,
        )

        self.at("grips sialic acid")
        # Virus moves over centre stalks (x = 0.625) and descends to dock 3 spikes onto 3 MAGENTA tips
        self.play(FadeOut(hema_arrow), run_time=0.25)
        target_x = 0.625
        dock_y = stalks[4].tip_tile().get_top()[1] + 1.42
        self.play(
            hema_lab.animate.move_to([3.5, 2.35, 0]),
            virus.animate.move_to([target_x, dock_y, 0]),
            run_time=1.4,
        )

        # Dotted contact lines between 3 bottom spikes (indices 11, 0, 1) and stalks 3, 4, 5
        dock_pairs = [(11, 3), (0, 4), (1, 5)]
        dock_lines = VGroup()
        for sp_i, st_i in dock_pairs:
            sp = virus.spikes[sp_i]
            st = stalks[st_i]
            ln = DashedLine(sp[1].get_bottom(), st.tip_tile().get_top(), color=TEXT, stroke_width=3.0, dash_length=0.07)
            ln.add_updater(lambda m, sp_ref=sp, st_ref=st: m.put_start_and_end_on(
                sp_ref[1].get_bottom(), st_ref.tip_tile().get_top() + UP * 0.04
            ))
            dock_lines.add(ln)
        self.play(FadeIn(dock_lines), run_time=0.55)

        self.at("latches on")
        self.play(virus.animate.shift(DOWN * 0.16), run_time=0.45)

        self.at("before it gets in")
        # Membrane begins to dimple slightly beneath the latched virus
        for i in (3, 4, 5):
            stalks[i].clear_updaters()
        self.play(
            dimple.animate.set_value(0.38),
            virus.animate.shift(DOWN * 0.22),
            *[stalks[i].animate.shift(DOWN * 0.25) for i in (3, 4, 5)],
            run_time=1.1,
        )
        for i in (3, 4, 5):
            stalks[i].y_base -= 0.25
            stalks[i]._record_rest()
            stalks[i].add_updater(stalks[i]._sway_update)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        mem = make_membrane()
        red_cell = make_red_cell_disc(top_y=2.20)
        tips_abo = ["glucose", "A", "B", "glucose", "A", "B", "glucose", "A"]
        stalks = VGroup(*[
            SwayStalk(x, y_base=MEM_Y_TOP, n_tiles=3 if i % 2 == 0 else 4,
                      tip_kind=tips_abo[i], seed=i)
            for i, x in enumerate(STALK_XS_8)
        ])
        tag = make_schematic_tag()
        self.add(red_cell, mem, stalks, tag)

        self.at("one small sugar")
        # ORANGE tip from hook (index 4) glows again
        hero_tip = stalks[4].tip_tile()
        glow = RoundedRectangle(
            corner_radius=0.12, width=0.80, height=0.80,
            stroke_color=ORANGE, stroke_width=4.5, fill_opacity=0.0,
        ).move_to(hero_tip.sq.get_center())
        glow.add_updater(lambda m: m.move_to(hero_tip.sq.get_center()))
        self.play(FadeIn(glow), run_time=0.7)

        self.at("read like a message")
        # PURPLE many-pocket lectin bar sweeps slowly across the row of tips, lighting each in turn
        scanner = make_lectin_cap(width=2.6, height=0.62, n_pockets=2, color=PURPLE).move_to([-4.2, 1.15, 0])
        self.play(FadeIn(scanner), run_time=0.4)

        lit_rings = VGroup()
        for s in stalks:
            r = RoundedRectangle(corner_radius=0.10, width=0.72, height=0.72,
                                 stroke_color=GOLD, stroke_width=3.5, fill_opacity=0.0).move_to(s.tip_tile().sq.get_center())
            r.set_stroke(opacity=0.0)
            r.add_updater(lambda m, sr=s: m.move_to(sr.tip_tile().sq.get_center()))
            lit_rings.add(r)
        self.add(lit_rings)

        def light_near_scanner(mob):
            sx = scanner.get_center()[0]
            for r, s in zip(mob, stalks):
                r.set_stroke(opacity=1.0 if abs(s.x_base - sx) < 1.35 else 0.0)

        lit_rings.add_updater(light_near_scanner)
        self.play(scanner.animate.move_to([4.2, 1.15, 0]), run_time=3.2, rate_func=linear)
        lit_rings.clear_updaters()
        self.play(FadeOut(scanner), FadeOut(lit_rings), run_time=0.4)

        self.at("which sugar sits where")
        chips = make_rule_chips(size=30).move_to([0.0, 2.90, 0])
        self.play(FadeIn(chips, shift=DOWN * 0.25), run_time=0.85)
        self.finish()


class S15End(EndCard):
    LINE = "On the cell surface, the message is which sugar sits where."
