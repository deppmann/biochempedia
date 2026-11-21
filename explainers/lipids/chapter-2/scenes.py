"""Two Faces, One Flag — STEMhop Lipids Chapter 2.

COLOUR MAP (one colour per concept for the whole film):
- BLUE (#58C4DD): straight saturated fatty-acyl tails
- YELLOW (#F5D547): kinked cis-unsaturated fatty-acyl tails
- GREEN (#83C167): cholesterol pegs in the hydrophobic core
- GREY (#8B93A1): glycerol backbones / unassigned neutral heads / cell seams
- PC_WHITE (#E8EAF0): phosphatidylcholine (PC) heads (neutral circles) & sphingomyelin (white squares)
- PS_MAGENTA (#E855B8): phosphatidylserine (PS) negative heads (magenta circle + white minus sign)
- FLIP_ORANGE (#F28C38): flippase & floppase ATP-driven pump doors + ATP tokens
- SCRAM_PURPLE (#9D6BFF): scramblase bidirectional doors
- PROT_CYAN (#38F2FF): positively charged cytoplasmic proteins (+ rounded blobs)
- MAC_PINK (#F9A8D4): macrophage cell outline & engulfing lobes
- PI_TEAL (#14B8A6): phosphatidylinositol (PI) heads & IP3/DAG messenger pieces
- LIME_SUGAR (#A3E635): outward-facing glycolipid sugar bead chains
- GOLD (#D4A843): PIP2 phosphate dots, guiding-idea highlight, predict countdown
- RED (#FC6255): flippase shut-off cross / dying-cell warning outline

THE WORLD CARRIED ALL FILM:
A wide horizontal phospholipid bilayer band crossing the frame, with outer leaflet heads on top,
inner leaflet heads below, mixed BLUE straight and YELLOW kinked tails pointing into the core,
GREEN cholesterol pegs wedged in the core, dark 'outside' space above, and tinted 'cytoplasm' below.
Zooms between a 3-cell-segment tissue view (for macrophage patrol & engulfment) and a 1-cell
close-up (for pumps, leaflets, and signaling).

WHAT CHANGES ON SCREEN (and what it is computed from) IN EACH SPOKEN SCENE:
- s00_link_and_question: Tails flex with computed thermal wave damped by distance to GREEN cholesterol; PINK macrophage glides past 2 healthy segments and extends pseudopods over dying cell 3, then rewinds.
- s01_title (silent 2s): Dying outline fades, title 'Two Faces, One Flag' settles above the continuing fluid bilayer and idling macrophage.
- s02_heads: Camera zooms to 1 cell; tails dim while head rows brighten; top heads convert to PC_WHITE and scattered inner heads convert to PS_MAGENTA(-).
- s03_pumps: Two FLIP_ORANGE flippase doors consume ATP tokens and transport two stray top PS_MAGENTA heads down to the inner row; a floppase moves one PC_WHITE head outward; SCRAM_PURPLE scramblase stays dim and closed.
- s04_inner_face: Camera pans up to widen cytoplasm; PROT_CYAN(+) blobs rise and dock to inner PS_MAGENTA(-); two inner heads become PI_TEAL, one gains GOLD phosphates (PIP2), and PLC scissors cleave it into drifting IP3 and inner-leaflet DAG.
- s05_outer_face: Camera pans down to widen outside; outer heads include PC_WHITE squares (sphingomyelin) and sprout outward LIME_SUGAR bead chains, then pans back to both faces.
- s06_idea: Charge (PC_WHITE vs PS_MAGENTA), ATP-driven flippase pumping one PS head inward, and dual-face function (PS+CYAN inside, sugars outside) highlight sequentially as 'charge + side = job' lands.
- s07_apoptosis: FLIP_ORANGE doors dim and cross out; SCRAM_PURPLE door brightens and opens, driving bidirectional head trajectories that accumulate PS_MAGENTA on the outer leaflet.
- s08_predict: Camera pulls back to 3 cells; middle dying cell's top row is veiled while scramblase runs; macrophage glides past healthy cell 1 and pauses over middle dying cell under 'What does it find?'.
- s09_pause (silent 4.5s): Macrophage hovers wobbling over middle cell while scramblase continues crossing heads and 4.5 s countdown ring empties.
- s10_answer: Haze clears to reveal outer PS_MAGENTA ('PS outside', 'eat me'); macrophage touches PS and flows around to engulf the dying segment while healthy neighbours keep PS inside.
- s11_close: Healthy 1-cell view; inner PS_MAGENTA ('the flag, kept inside') and active flippase+ATP are shown, then a ghost PS copy slides up through faded scramblase to the outer face and fades while the real PS stays inside.
- s12_end (silent 3.5s): Standard EndCard with take-home line.
"""
from bp_parts import *

# Film-specific concept colours (never redefined per scene)
PC_WHITE = TEXT          # "#E8EAF0"
PS_MAGENTA = "#E855B8"
FLIP_ORANGE = "#F28C38"
SCRAM_PURPLE = "#9D6BFF"
PROT_CYAN = "#38F2FF"
MAC_PINK = "#F9A8D4"
PI_TEAL = "#14B8A6"
LIME_SUGAR = "#A3E635"
CYTO_BG = "#161E2E"

OUTSIDE_AT = np.array([5.35, 3.20, 0.0])
CYTO_AT = np.array([-5.15, -3.20, 0.0])


def make_minus(color=TEXT, half=0.08, width=3.2):
    """Crisp geometric minus sign (avoids tiny Text inside small circles)."""
    return Line(LEFT * half, RIGHT * half, color=color, stroke_width=width)


def make_plus(color=BG, half=0.10, width=3.5):
    """Crisp geometric plus sign."""
    return VGroup(
        Line(LEFT * half, RIGHT * half, color=color, stroke_width=width),
        Line(DOWN * half, UP * half, color=color, stroke_width=width),
    )


def make_cross(color=RED, half=0.22, width=4.5):
    """Crisp geometric X mark for shut-off flippases."""
    return VGroup(
        Line([-half, -half, 0], [half, half, 0], color=color, stroke_width=width),
        Line([-half, half, 0], [half, -half, 0], color=color, stroke_width=width),
    )


def make_head(kind="grey", r=0.20):
    """Build a lipid head mobject: 'grey', 'pc', 'sm', 'ps', or 'pi'."""
    if kind == "pc":
        return Circle(radius=r, color=PC_WHITE, stroke_width=2.4, fill_color=PC_WHITE, fill_opacity=0.88)
    if kind == "sm":
        return RoundedRectangle(
            corner_radius=r * 0.25, width=r * 1.9, height=r * 1.9,
            color=PC_WHITE, stroke_width=2.4, fill_color=PC_WHITE, fill_opacity=0.88,
        )
    if kind == "ps":
        c = Circle(radius=r, color=PS_MAGENTA, stroke_width=2.6, fill_color=PS_MAGENTA, fill_opacity=0.92)
        m = make_minus(TEXT, half=r * 0.45, width=max(2.4, r * 14))
        return VGroup(c, m)
    if kind == "pi":
        return Circle(radius=r, color=PI_TEAL, stroke_width=2.6, fill_color=PI_TEAL, fill_opacity=0.92)
    return Circle(radius=r, color=GREY, stroke_width=2.2, fill_color=GREY, fill_opacity=0.72)


def make_sugar_chain(base_pt, n=3, bead_r=0.068, step=0.17):
    """Outward-facing LIME bead chain (beads only, never rings)."""
    g = VGroup()
    stem = Line(base_pt, base_pt + UP * (n * step), color=LIME_SUGAR, stroke_width=2.5)
    g.add(stem)
    for k in range(1, n + 1):
        dx = 0.04 if k % 2 == 1 else -0.04
        pos = base_pt + UP * (k * step) + RIGHT * dx
        g.add(Dot(pos, radius=bead_r, color=LIME_SUGAR))
    return g


def make_cholesterol(x, y_mid, leaflet="top", half_h=1.35, scale=1.0):
    """Rigid GREEN cholesterol peg wedged into one leaflet's tail zone."""
    sign = 1.0 if leaflet == "top" else -1.0
    peg_h = half_h * 0.52
    y_outer = y_mid + sign * (half_h - 0.30 * scale)
    y_inner = y_outer - sign * peg_h
    cy = 0.5 * (y_outer + y_inner)
    bar = RoundedRectangle(
        corner_radius=0.06 * scale, width=0.13 * scale, height=peg_h,
        color=GREEN, stroke_width=2.0, fill_color=GREEN, fill_opacity=0.85,
    ).move_to([x, cy, 0])
    tip = Dot([x, y_outer, 0], radius=0.055 * scale, color=GREEN)
    g = VGroup(bar, tip)
    g.peg_x = x
    return g


def make_tail_vmob(kinked, x_off, tail_len, color, width=2.8, opacity=0.9):
    """Create a 5-point polyline tail with base metadata for fast computed flexing."""
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m._tail_meta = (kinked, x_off, tail_len)
    return m


def _update_tail_points(m, t, damp, head_pos, y_mid):
    """Compute tail points from time t, cholesterol damping, head position, and bilayer center."""
    kinked, x_off, tail_len = m._tail_meta
    dy = head_pos[1] - y_mid
    # Tails always point inward into the hydrophobic core (smooth flip across y_mid)
    sign = -float(np.tanh(dy / 0.30))
    x0 = head_pos[0] + x_off
    y0 = head_pos[1]
    amp = (0.090 if kinked else 0.046) * damp
    phase = 1.7 * x0 + (0.9 if kinked else 0.0)
    omega = 2.9 if kinked else 2.2
    pts = []
    for i in range(5):
        s = i / 4.0
        kink_dx = 0.095 if (kinked and i >= 2) else 0.0
        flex_dx = amp * s * np.sin(omega * t + phase - 1.8 * s)
        pts.append([x0 + kink_dx + flex_dx, y0 + sign * (s * tail_len), 0.0])
    m.set_points_as_corners(pts)


class BilayerWorld(VGroup):
    """Carried bilayer band with computed cholesterol-buffered tail flexing."""

    def __init__(
        self,
        x_range=(-6.0, 6.0),
        y_center=0.0,
        half_h=1.55,
        n_cols=16,
        head_r=0.20,
        top_kinds=None,
        bot_kinds=None,
        chol_positions=None,
        door_xs=(),
        door_gap=0.44,
        seed=7,
        tail_opacity=0.90,
        tail_width=2.8,
        show_cyto=True,
    ):
        super().__init__()
        self.rng = np.random.default_rng(seed)
        self.x_range = x_range
        self.y_center = y_center
        self.half_h = half_h
        self.head_r = head_r
        self.tail_len = half_h - head_r * 1.15 - 0.14
        self._sim_t = 0.0

        # Reference marker tracks current y_center even when world is shifted/scaled
        self._center_ref = Dot([0.0, y_center, 0.0], radius=0.001).set_opacity(0)
        self._center_ref.layout_ok = True
        self.add(self._center_ref)

        # Tinted cytoplasm background polygon (Polygon avoids layout_check panel false-positives)
        if show_cyto:
            cy_top = y_center - half_h
            self.cyto_bg = Polygon(
                [-7.3, cy_top, 0], [7.3, cy_top, 0], [7.3, -4.5, 0], [-7.3, -4.5, 0],
                fill_color=CYTO_BG, fill_opacity=0.92, stroke_width=0,
            ).set_z_index(-8)
            self.cyto_bg.layout_ok = True
            self.add(self.cyto_bg)
        else:
            self.cyto_bg = None

        xs = np.linspace(x_range[0], x_range[1], n_cols)
        self.xs = xs
        if top_kinds is None:
            top_kinds = ["grey"] * n_cols
        if bot_kinds is None:
            bot_kinds = ["grey"] * n_cols

        # Cholesterol pegs in the core (keep clear of door gaps)
        self.chols = VGroup()
        self.chol_xs = []
        if chol_positions is None:
            chol_positions = [(-4.2, "top"), (-1.1, "bottom"), (1.9, "top"), (4.7, "bottom")]
        for cx, lf in chol_positions:
            if any(abs(cx - dx) < door_gap for dx in door_xs):
                continue
            peg = make_cholesterol(cx, y_center, leaflet=lf, half_h=half_h, scale=head_r / 0.20)
            self.chols.add(peg)
            self.chol_xs.append(cx)

        self.tails = VGroup()
        self.top_heads = VGroup()
        self.bot_heads = VGroup()
        self._pairs = []  # (head, [tail1, tail2], damp)

        for row_name, kinds, y_row, grp in (
            ("top", top_kinds, y_center + half_h, self.top_heads),
            ("bottom", bot_kinds, y_center - half_h, self.bot_heads),
        ):
            for idx, (x, kind) in enumerate(zip(xs, kinds)):
                if kind == "none" or any(abs(float(x) - dx) < door_gap for dx in door_xs):
                    # Hidden placeholder so column indices stay consistent
                    placeholder = Dot([float(x), y_row, 0], radius=0.001).set_opacity(0)
                    placeholder.layout_ok = True
                    placeholder.kind = "none"
                    grp.add(placeholder)
                    continue

                jy = float(self.rng.uniform(-0.025, 0.025))
                hx = float(x)
                hy = y_row + jy
                h = make_head(kind, r=head_r).move_to([hx, hy, 0])
                h.kind = kind
                h.base_x = hx
                h.base_y = hy
                h.leaflet = row_name
                grp.add(h)

                # Nearest cholesterol peg damps local tail flex (physical buffering)
                d_chol = min([abs(hx - cx) for cx in self.chol_xs] + [99.0])
                damp = 0.42 if d_chol < 0.85 else 1.0

                # Choose straight (BLUE) vs kinked (YELLOW) tails deterministically
                k1 = bool(self.rng.random() < 0.38)
                k2 = bool(self.rng.random() < 0.30)
                dx_off = head_r * 0.42
                t1 = make_tail_vmob(
                    k1, -dx_off, self.tail_len,
                    YELLOW if k1 else BLUE, width=tail_width, opacity=tail_opacity,
                )
                t2 = make_tail_vmob(
                    k2, dx_off, self.tail_len,
                    YELLOW if k2 else BLUE, width=tail_width, opacity=tail_opacity,
                )
                _update_tail_points(t1, 0.0, damp, h.get_center(), y_center)
                _update_tail_points(t2, 0.0, damp, h.get_center(), y_center)
                self.tails.add(t1, t2)
                self._pairs.append((h, [t1, t2], damp))

        self.tails.set_z_index(-2)
        self.chols.set_z_index(-1)
        self.top_heads.set_z_index(1)
        self.bot_heads.set_z_index(1)
        self.add(self.tails, self.chols, self.top_heads, self.bot_heads)

    def start_fluid_motion(self):
        """Attach continuous thermal tail-flex updater driven by elapsed time."""
        def _tick(mob, dt):
            mob._sim_t += dt
            t = mob._sim_t
            y_mid = mob._center_ref.get_center()[1]
            for h, ts, damp in mob._pairs:
                pos = h.get_center()
                for tl in ts:
                    _update_tail_points(tl, t, damp, pos, y_mid)
        self.add_updater(_tick)
        return self

    def recolor_head(self, leaflet, idx, new_kind):
        """Return (old_head, target_head) for in-place Transform while keeping old inside world."""
        grp = self.top_heads if leaflet == "top" else self.bot_heads
        old = grp[idx]
        target = make_head(new_kind, r=self.head_r).move_to(old.get_center())
        old.kind = new_kind
        return old, target


def make_door(x, y_center, half_h, color=FLIP_ORANGE, kind="flippase", width=0.68, closed=False):
    """Transmembrane channel door spanning both leaflets (never a plain empty box)."""
    h = half_h * 2 + 0.44
    gap = 0.06 if closed else 0.16
    wall_w = (width - gap) / 2
    left_wall = RoundedRectangle(
        corner_radius=0.09, width=wall_w, height=h,
        color=color, stroke_width=2.6, fill_color=color, fill_opacity=0.22,
    ).move_to([x - (gap + wall_w) / 2, y_center, 0])
    right_wall = RoundedRectangle(
        corner_radius=0.09, width=wall_w, height=h,
        color=color, stroke_width=2.6, fill_color=color, fill_opacity=0.22,
    ).move_to([x + (gap + wall_w) / 2, y_center, 0])

    if kind == "flippase":
        arrow = Arrow(
            [x, y_center + half_h * 0.55, 0], [x, y_center - half_h * 0.55, 0],
            buff=0, color=color, stroke_width=3.2, max_tip_length_to_length_ratio=0.22,
        )
    elif kind == "floppase":
        arrow = Arrow(
            [x, y_center - half_h * 0.55, 0], [x, y_center + half_h * 0.55, 0],
            buff=0, color=color, stroke_width=3.2, max_tip_length_to_length_ratio=0.22,
        )
    else:
        arrow = DoubleArrow(
            [x, y_center - half_h * 0.55, 0], [x, y_center + half_h * 0.55, 0],
            buff=0, color=color, stroke_width=3.0, tip_length=0.16,
        )
    door = VGroup(left_wall, right_wall, arrow).set_z_index(3)
    door.left_wall, door.right_wall, door.arrow = left_wall, right_wall, arrow
    door.door_x = x
    return door


def make_macrophage(center=(-5.0, 2.00, 0), rx=1.05, ry=0.55):
    """Pale PINK macrophage outline with soft wobbling membrane & engulfing shape."""
    n = 36
    m = VMobject(color=MAC_PINK, stroke_width=3.5, fill_color=MAC_PINK, fill_opacity=0.20)
    m._mac_t = 0.0
    m._mac_rx = rx
    m._mac_ry = ry
    m._mac_center = np.array(center, dtype=float)
    m._mac_reach = 0.0   # 0 = rounded, 1 = pseudopod lobes reaching down
    m._mac_engulf = 0.0  # 0 = hovering, 1 = rounded engulfment around dying segment

    def _build_pts(mob):
        cx, cy, _ = mob._mac_center
        t = mob._mac_t
        reach = mob._mac_reach
        eng = mob._mac_engulf
        pts = []
        cur_rx = interpolate(mob._mac_rx, 2.05, eng)
        cur_ry = interpolate(mob._mac_ry, 1.55, eng)
        for i in range(n):
            th = TAU * i / n
            wob = 0.045 * np.sin(3 * th + 2.4 * t) + 0.025 * np.cos(5 * th - 1.8 * t)
            x = cx + cur_rx * np.cos(th) * (1 + wob)
            y = cy + cur_ry * np.sin(th) * (1 + wob)
            # Pseudopod reach drops gently toward the outer PS heads before closing around cell
            if np.sin(th) < -0.15:
                lobe = np.exp(-((abs(np.cos(th)) - 0.65) ** 2) / 0.16)
                y -= reach * (1.0 - eng) * (0.58 * lobe + 0.15)
            pts.append([x, y, 0.0])
        mob.set_points_as_corners(pts + [pts[0]])
        mob.make_smooth()

    _build_pts(m)

    def _wobble(mob, dt):
        mob._mac_t += dt
        _build_pts(mob)

    m.add_updater(_wobble)
    m.set_z_index(4)
    return m


def make_positive_protein(center, w=1.05, h=0.50):
    """CYAN rounded cytoplasmic protein blob with crisp '+' sign."""
    pill = RoundedRectangle(
        corner_radius=h / 2, width=w, height=h,
        color=PROT_CYAN, stroke_width=2.6, fill_color=PROT_CYAN, fill_opacity=0.86,
    ).move_to(center)
    plus = make_plus(BG, half=0.11, width=3.5).move_to(pill)
    return VGroup(pill, plus).set_z_index(3)


def make_scissors(center):
    """Clean schematic scissors icon for phospholipase C (not a molecular structure)."""
    b1 = Line([-0.22, -0.12, 0], [0.22, 0.12, 0], color=GOLD, stroke_width=3.2)
    b2 = Line([-0.22, 0.12, 0], [0.22, -0.12, 0], color=GOLD, stroke_width=3.2)
    r1 = Circle(radius=0.08, color=GOLD, stroke_width=2.6).move_to([-0.28, -0.16, 0])
    r2 = Circle(radius=0.08, color=GOLD, stroke_width=2.6).move_to([-0.28, 0.16, 0])
    return VGroup(b1, b2, r1, r2).move_to(center).set_z_index(5)


def make_three_cell_world(dying_ps_top=False, veil_middle=False, open_scram=False):
    """Build the 3-cell tissue stretch used in s00, s01, s08, s09, s10."""
    n_cols = 30
    top_kinds = ["pc"] * n_cols
    bot_kinds = ["grey"] * n_cols
    for i in (1, 4, 7, 11, 17, 21, 24, 27):
        bot_kinds[i] = "ps"
    if dying_ps_top:
        for i in (11, 13, 16, 18):
            top_kinds[i] = "ps"

    door_xs = (0.0,) if open_scram else ()
    world = BilayerWorld(
        x_range=(-6.0, 6.0), y_center=-0.50, half_h=1.25,
        n_cols=n_cols, head_r=0.135,
        top_kinds=top_kinds, bot_kinds=bot_kinds,
        chol_positions=[(-4.8, "top"), (-2.9, "bottom"), (-1.1, "top"), (1.1, "bottom"), (3.1, "top"), (5.0, "bottom")],
        door_xs=door_xs, door_gap=0.35,
        seed=11, tail_width=2.3,
    )
    seams = VGroup(
        DashedLine([-2.0, 0.95, 0], [-2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
        DashedLine([2.0, 0.95, 0], [2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
    ).set_z_index(2)
    world.seams = seams
    world.add(seams)

    if open_scram:
        door = make_door(0.0, -0.50, 1.25, color=SCRAM_PURPLE, kind="scramblase", width=0.56, closed=False)
        world.scram_door = door
        world.add(door)

    if veil_middle:
        veil = RoundedRectangle(
            corner_radius=0.22, width=3.75, height=0.55,
            color=BG, stroke_width=0, fill_color="#1B2234", fill_opacity=0.88,
        ).move_to([0.0, 0.78, 0]).set_z_index(2)
        veil.layout_ok = True
        world.veil = veil
        world.add(veil)

    return world


def make_single_cell_world(
    y_center=0.0,
    half_h=1.55,
    top_kinds=None,
    bot_kinds=None,
    door_xs=(),
    door_gap=0.42,
    tail_opacity=0.88,
    sugar_indices=(),
):
    """Build the zoomed-in 1-cell bilayer stretch used in s02..s07 and s11."""
    if top_kinds is None:
        top_kinds = ["pc" if i not in (2, 6, 11) else "sm" for i in range(16)]
    if bot_kinds is None:
        bot_kinds = ["ps" if i in (1, 4, 6, 8, 13) else "grey" for i in range(16)]
    world = BilayerWorld(
        x_range=(-5.8, 5.8), y_center=y_center, half_h=half_h,
        n_cols=16, head_r=0.20,
        top_kinds=top_kinds, bot_kinds=bot_kinds,
        chol_positions=[(-4.5, "top"), (-1.5, "bottom"), (1.3, "top"), (4.2, "bottom")],
        door_xs=door_xs, door_gap=door_gap,
        seed=7, tail_opacity=tail_opacity, tail_width=2.8,
    )
    sugars = VGroup()
    for idx in sugar_indices:
        hd = world.top_heads[idx]
        if getattr(hd, "kind", None) != "none":
            sugars.add(make_sugar_chain(hd.get_top() + UP * 0.02))
    world.sugars = sugars
    world.add(sugars)
    return world


# ==============================================================================
# SCENE 00: Link & Question (17.2 s)
# ==============================================================================
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        world = BilayerWorld(
            x_range=(-6.0, 6.0), y_center=-0.50, half_h=1.25,
            n_cols=30, head_r=0.135,
            top_kinds=["grey"] * 30, bot_kinds=["grey"] * 30,
            chol_positions=[(-4.8, "top"), (-2.9, "bottom"), (-0.9, "top"), (1.1, "bottom"), (3.1, "top"), (5.0, "bottom")],
            seed=11, tail_width=2.3,
        )
        seams = VGroup(
            DashedLine([-2.0, 0.95, 0], [-2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
            DashedLine([2.0, 0.95, 0], [2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
        ).set_z_index(2)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(world, seams, out_lab, cy_lab)
        world.start_fluid_motion()

        self.at("cholesterol buffers")
        peg = world.chols[2]
        ring = SurroundingRectangle(peg, color=GREEN, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(ring), run_time=0.45)
        self.play(FadeOut(ring), run_time=0.45)

        self.at("watch a macrophage")
        mac = make_macrophage(center=(-5.2, 2.00, 0), rx=1.05, ry=0.55)
        self.play(FadeIn(mac, shift=RIGHT * 0.4), run_time=0.7)

        self.at("passes healthy cells")
        self.play(
            UpdateFromAlphaFunc(
                mac,
                lambda m, a: setattr(m, "_mac_center", np.array([interpolate(-5.2, 4.0, a), 2.00, 0.0])),
            ),
            run_time=1.8, rate_func=smooth,
        )

        self.at("swallows a dying")
        dying_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.2, width=3.65, height=2.95, color=RED, stroke_width=3.2).move_to([4.05, -0.50, 0]),
            num_dashes=28,
        ).set_z_index(3)
        dying_lab = T("dying cell", 28, RED).move_to([4.05, -2.35, 0])
        self.play(Create(dying_box), FadeIn(dying_lab, shift=UP * 0.1), run_time=0.65)
        self.play(
            UpdateFromAlphaFunc(mac, lambda m, a: setattr(m, "_mac_reach", a)),
            run_time=0.9,
        )

        self.at("What is it reading")
        q_text = T("What is it reading?", 38, TEXT, weight=BOLD).move_to([-0.2, 3.10, 0])
        self.play(
            FadeIn(q_text, shift=DOWN * 0.1),
            UpdateFromAlphaFunc(
                mac,
                lambda m, a: (
                    setattr(m, "_mac_reach", 1.0 - a),
                    setattr(m, "_mac_center", np.array([interpolate(4.0, -5.0, a), 2.00, 0.0])),
                ),
            ),
            run_time=1.2,
        )
        self.finish()


# ==============================================================================
# SCENE 01: Title (2.0 s silent)
# ==============================================================================
class S01Title(NarratedScene):
    def construct(self):
        world = BilayerWorld(
            x_range=(-6.0, 6.0), y_center=-0.50, half_h=1.25,
            n_cols=30, head_r=0.135,
            top_kinds=["grey"] * 30, bot_kinds=["grey"] * 30,
            chol_positions=[(-4.8, "top"), (-2.9, "bottom"), (-0.9, "top"), (1.1, "bottom"), (3.1, "top"), (5.0, "bottom")],
            seed=11, tail_width=2.3,
        )
        seams = VGroup(
            DashedLine([-2.0, 0.95, 0], [-2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
            DashedLine([2.0, 0.95, 0], [2.0, -1.95, 0], color=GREY, stroke_width=2.0, dash_length=0.12).set_opacity(0.45),
        ).set_z_index(2)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)
        mac = make_macrophage(center=(-5.0, 2.00, 0), rx=1.05, ry=0.55)
        dying_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.2, width=3.65, height=2.95, color=RED, stroke_width=3.2).move_to([4.05, -0.50, 0]),
            num_dashes=28,
        ).set_z_index(3)
        dying_lab = T("dying cell", 28, RED).move_to([4.05, -2.35, 0])
        q_text = T("What is it reading?", 38, TEXT, weight=BOLD).move_to([-0.2, 3.10, 0])

        self.add(world, seams, out_lab, cy_lab, mac, dying_box, dying_lab, q_text)
        world.start_fluid_motion()

        title = T("Two Faces, One Flag", 46, TEXT, font=TITLE_FONT).move_to([0.0, 3.05, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.14)
        self.play(FadeOut(q_text), FadeOut(dying_box), FadeOut(dying_lab), run_time=0.55)
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.65)
        self.finish()


# ==============================================================================
# SCENE 02: Heads (20.425 s)
# ==============================================================================
class S02Heads(SpokenScene):
    def construct(self):
        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=["grey"] * 16, bot_kinds=["grey"] * 16,
            tail_opacity=0.90,
        )
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        world.scale(0.86)
        self.add(world, out_lab, cy_lab)
        world.start_fluid_motion()
        self.play(world.animate.scale(1.0 / 0.86), run_time=0.8)

        self.at("not in the tails")
        self.play(world.tails.animate.set_stroke(opacity=0.52), run_time=0.9)

        self.at("in the heads")
        self.play(world.top_heads.animate.scale(1.14), world.bot_heads.animate.scale(1.14), run_time=0.6)
        self.play(world.top_heads.animate.scale(1.0 / 1.14), world.bot_heads.animate.scale(1.0 / 1.14), run_time=0.55)

        self.at("head group sets")
        self.play(
            LaggedStart(*[Indicate(h, color=GOLD, scale_factor=1.18) for h in world.top_heads[::2]], lag_ratio=0.14),
            run_time=1.8,
        )

        self.at("Phosphatidylcholine")
        pc_indices = [0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15]
        pc_swaps = []
        for idx in pc_indices:
            old, target = world.recolor_head("top", idx, "pc")
            pc_swaps.append(Transform(old, target))
        pc_lab = T("PC: no net charge", 30, PC_WHITE).move_to([0.0, 2.45, 0])
        self.play(LaggedStart(*pc_swaps, lag_ratio=0.09), FadeIn(pc_lab, shift=UP * 0.1), run_time=2.2)

        self.at("outer leaflet")
        self.play(
            Indicate(world.top_heads, color=PC_WHITE, scale_factor=1.08),
            run_time=1.4,
        )

        self.at("Phosphatidylserine")
        ps_indices = [1, 4, 7, 10, 13]
        ps_swaps = []
        for idx in ps_indices:
            old, target = world.recolor_head("bottom", idx, "ps")
            ps_swaps.append(Transform(old, target))
        ps_lab = T("PS: negative", 30, PS_MAGENTA).move_to([0.0, -2.45, 0])
        self.play(LaggedStart(*ps_swaps, lag_ratio=0.16), FadeIn(ps_lab, shift=DOWN * 0.1), run_time=2.2)

        self.at("held on the inner")
        self.play(
            *[Indicate(world.bot_heads[i], color=PS_MAGENTA, scale_factor=1.24) for i in ps_indices],
            run_time=1.4,
        )
        self.finish()


# ==============================================================================
# SCENE 03: Pumps (21.4 s)
# ==============================================================================
class S03Pumps(SpokenScene):
    def construct(self):
        # Doors sit cleanly in reserved column gaps at x = -3.48 (idx 3), -0.39 (idx 7), +2.71 (idx 11), +5.03 (idx 14)
        # Destination slots (bot[4], bot[8], top[12]) are open ("none") so moved heads never overlap existing heads.
        top_kinds = ["pc"] * 16
        top_kinds[2] = "ps"    # stray PS #1 adjacent to flippase 1 (-3.48)
        top_kinds[6] = "ps"    # stray PS #2 adjacent to flippase 2 (-0.39)
        top_kinds[12] = "none" # destination slot for floppase outward PC
        bot_kinds = ["ps" if i in (1, 5, 9, 13) else "grey" for i in range(16)]
        bot_kinds[4] = "none"  # destination slot for PS #1
        bot_kinds[8] = "none"  # destination slot for PS #2
        bot_kinds[10] = "pc"   # PC head adjacent to floppase (+2.71) to move outward

        door_xs = (-3.48, -0.39, 2.71, 5.03)
        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=top_kinds, bot_kinds=bot_kinds,
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.65,
        )
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        flip1 = make_door(-3.48, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        flip2 = make_door(-0.39, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        flip_lab = T("flippase", 26, FLIP_ORANGE).move_to([-1.95, 2.35, 0])

        self.add(world, out_lab, cy_lab, flip1, flip2, flip_lab)
        world.start_fluid_motion()

        self.at("pumps keep it there")
        self.play(
            Indicate(flip1, color=FLIP_ORANGE, scale_factor=1.06),
            Indicate(flip2, color=FLIP_ORANGE, scale_factor=1.06),
            run_time=1.0,
        )

        # First flippase pumps stray PS #1 inward using ATP
        self.at("Flippases spend")
        atp1 = boxed_label("ATP", FLIP_ORANGE, size=24, pad=0.10).move_to([-3.48, -2.70, 0]).set_z_index(4)
        self.play(FadeIn(atp1, shift=UP * 0.15), run_time=0.30)
        self.play(atp1.animate.move_to([-3.48, -1.95, 0]), run_time=0.40)
        self.play(FadeOut(atp1, scale=1.2), run_time=0.25)

        ps1 = world.top_heads[2]
        self.play(ps1.animate.move_to([-3.48, 1.55, 0]), run_time=0.35)
        self.play(ps1.animate.move_to([-3.48, -1.55, 0]), run_time=0.75)
        self.play(ps1.animate.move_to([-2.71, -1.55, 0]), run_time=0.30)

        # Second flippase pumps stray PS #2 inward using its own ATP
        atp2 = boxed_label("ATP", FLIP_ORANGE, size=24, pad=0.10).move_to([-0.39, -2.70, 0]).set_z_index(4)
        self.play(FadeIn(atp2, shift=UP * 0.15), run_time=0.30)
        self.play(atp2.animate.move_to([-0.39, -1.95, 0]), run_time=0.38)
        self.play(FadeOut(atp2, scale=1.2), run_time=0.22)

        ps2 = world.top_heads[6]
        self.play(ps2.animate.move_to([-0.39, 1.55, 0]), run_time=0.32)
        self.play(ps2.animate.move_to([-0.39, -1.55, 0]), run_time=0.75)
        self.play(ps2.animate.move_to([0.39, -1.55, 0]), run_time=0.30)

        # Floppase moves PC outward with ATP
        self.at("Floppases")
        flop = make_door(2.71, 0.0, 1.55, color=FLIP_ORANGE, kind="floppase", width=0.58)
        flop_lab = T("floppase", 26, FLIP_ORANGE).move_to([2.45, 2.35, 0])
        self.play(FadeIn(flop), FadeIn(flop_lab, shift=UP * 0.1), run_time=0.50)

        atp3 = boxed_label("ATP", FLIP_ORANGE, size=24, pad=0.10).move_to([2.71, -3.00, 0]).set_z_index(4)
        self.play(FadeIn(atp3), run_time=0.30)
        self.play(atp3.animate.move_to([2.71, -1.95, 0]), run_time=0.40)
        self.play(FadeOut(atp3, scale=1.2), run_time=0.25)

        pc_out = world.bot_heads[10]
        self.play(pc_out.animate.move_to([2.71, -1.55, 0]), run_time=0.35)
        self.play(pc_out.animate.move_to([2.71, 1.55, 0]), run_time=0.80)
        self.play(pc_out.animate.move_to([3.48, 1.55, 0]), run_time=0.35)

        # Scramblase appears dim and closed, then brief note on both-ways capability before healthy lock
        self.at("when switched")
        scram = make_door(5.03, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.45)
        scram_lab = T("scramblase: off", 26, SCRAM_PURPLE).move_to([5.10, 2.50, 0]).set_opacity(0.78)
        self.play(FadeIn(scram), FadeIn(scram_lab), run_time=0.8)

        self.at("cross both ways")
        self.play(Indicate(scram.arrow, color=SCRAM_PURPLE, scale_factor=1.15), run_time=0.9)

        self.at("stay off")
        self.play(
            Indicate(flip1, color=FLIP_ORANGE, scale_factor=1.05),
            Indicate(flip2, color=FLIP_ORANGE, scale_factor=1.05),
            run_time=0.9,
        )
        self.finish()


# ==============================================================================
# SCENE 04: Inner Face (17.775 s)
# ==============================================================================
class S04InnerFace(SpokenScene):
    def construct(self):
        # Doors at x = -3.48 (idx 3) and +5.03 (idx 14); PS at idx 1, 5, 7
        door_xs = (-3.48, 5.03)
        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=["pc"] * 16,
            bot_kinds=["ps" if i in (1, 5, 7) else "grey" for i in range(16)],
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.65,
        )
        flip1 = make_door(-3.48, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        scram = make_door(5.03, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.45)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        band_grp = VGroup(world, flip1, scram)
        self.add(band_grp, out_lab, cy_lab)
        world.start_fluid_motion()

        # Tilt toward inner face (inner_y = -1.55 + 0.85 = -0.70)
        self.play(band_grp.animate.shift(UP * 0.85), run_time=0.75)
        inner_y = -0.70

        self.at("carries negative PS")
        ps_heads = [world.bot_heads[i] for i in (1, 5, 7)]
        self.play(*[Indicate(h, color=PS_MAGENTA, scale_factor=1.18) for h in ps_heads], run_time=0.85)

        # Positive cyan proteins rise from cytoplasm and dock directly under PS heads (idx 1 & idx 5)
        self.at("positively charged proteins")
        x_p1 = world.bot_heads[1].get_center()[0]
        x_p2 = world.bot_heads[5].get_center()[0]
        prot1 = make_positive_protein([x_p1 + 0.65, -2.42, 0])
        prot2 = make_positive_protein([x_p2, -2.55, 0])
        prot_lab = T("positive proteins", 28, PROT_CYAN).move_to([0.5 * (x_p1 + x_p2), -2.25, 0])
        self.play(FadeIn(prot1, shift=UP * 0.15), FadeIn(prot2, shift=UP * 0.15), run_time=0.60)
        self.play(
            prot1.animate.move_to([x_p1, inner_y - 0.54, 0]),
            prot2.animate.move_to([x_p2, inner_y - 0.54, 0]),
            run_time=1.35,
        )
        self.play(FadeIn(prot_lab, shift=UP * 0.1), run_time=0.50)

        # PI heads appear on inner leaflet at idx 10 (x=1.93) and idx 12 (x=3.48)
        self.at("Phosphatidylinositol")
        pi_swaps = []
        for idx in (10, 12):
            old, target = world.recolor_head("bottom", idx, "pi")
            pi_swaps.append(Transform(old, target))
        pi_target = world.bot_heads[10]
        pi_x = pi_target.get_center()[0]
        pi_lab = T("PI", 28, PI_TEAL).move_to([3.48, inner_y - 0.58, 0])
        self.play(*pi_swaps, FadeIn(pi_lab, shift=UP * 0.1), run_time=1.0)

        # Phospholipase C + PIP2 phosphorylation right on pi_target (idx 10)
        self.at("Phospholipase C")
        p_dots = VGroup(
            Dot([pi_x - 0.10, inner_y - 0.28, 0], radius=0.065, color=GOLD),
            Dot([pi_x + 0.10, inner_y - 0.28, 0], radius=0.065, color=GOLD),
        ).set_z_index(4)
        pip2_lab = T("PIP2", 28, PI_TEAL).move_to([pi_x, inner_y - 0.68, 0])
        scissors = make_scissors([pi_x - 0.58, inner_y - 0.25, 0])
        plc_lab = T("phospholipase C", 26, GOLD).move_to([pi_x - 0.85, inner_y - 1.15, 0])
        self.play(FadeIn(scissors), FadeIn(plc_lab), run_time=0.65)
        self.at("phosphorylated")
        self.play(FadeIn(p_dots), swap(pi_lab, pip2_lab, run_time=0.70), run_time=0.80)

        # Cut PIP2 into IP3 (drifts into cytoplasm) and DAG (stays in inner leaflet)
        self.at("PIP2")
        self.play(scissors.animate.shift(RIGHT * 0.36), run_time=0.55)

        self.at("two messengers")
        ip3_head = VGroup(
            Circle(radius=0.18, color=PI_TEAL, stroke_width=2.5, fill_color=PI_TEAL, fill_opacity=0.9),
            Dot([-0.08, -0.22, 0], radius=0.06, color=GOLD),
            Dot([0.08, -0.22, 0], radius=0.06, color=GOLD),
        ).move_to(pi_target.get_center()).set_z_index(4)
        ip3_lab = T("IP3", 28, PI_TEAL).move_to([pi_x + 0.72, -2.55, 0])
        dag_lab = T("DAG", 28, GOLD).move_to([pi_x + 0.68, inner_y - 0.58, 0])

        self.play(
            FadeOut(scissors), FadeOut(plc_lab),
            FadeOut(p_dots),
            pi_target.animate.set_opacity(0.35),
            FadeIn(ip3_head),
            FadeOut(pip2_lab),
            run_time=0.45,
        )
        self.play(
            ip3_head.animate.move_to([pi_x, -2.55, 0]),
            FadeIn(ip3_lab, shift=DOWN * 0.1),
            FadeIn(dag_lab),
            run_time=0.85,
        )
        self.finish()


# ==============================================================================
# SCENE 05: Outer Face (16.05 s)
# ==============================================================================
class S05OuterFace(SpokenScene):
    def construct(self):
        door_xs = (-3.48, 5.03)
        world = make_single_cell_world(
            y_center=0.85, half_h=1.55,
            top_kinds=["pc"] * 16,
            bot_kinds=["ps" if i in (1, 5, 7) else ("pi" if i in (10, 12) else "grey") for i in range(16)],
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.65,
        )
        flip1 = make_door(-3.48, 0.85, 1.55, color=FLIP_ORANGE, kind="flippase")
        scram = make_door(5.03, 0.85, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.45)
        x_p1 = world.bot_heads[1].get_center()[0]
        x_p2 = world.bot_heads[5].get_center()[0]
        prot1 = make_positive_protein([x_p1, -0.70 - 0.54, 0])
        prot2 = make_positive_protein([x_p2, -0.70 - 0.54, 0])
        band_grp = VGroup(world, flip1, scram, prot1, prot2)

        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(band_grp, out_lab, cy_lab)
        world.start_fluid_motion()

        # Pan down toward outer face (y_center = -0.30 -> outer_y = +1.25)
        self.at("outer face")
        self.play(band_grp.animate.shift(DOWN * 1.15), run_time=0.95)

        # Rich in PC and sphingomyelin (white squares at idx 2, 6, 11)
        self.at("sphingomyelin")
        sm_indices = (2, 6, 11)
        sm_swaps = []
        for idx in sm_indices:
            old, target = world.recolor_head("top", idx, "sm")
            sm_swaps.append(Transform(old, target))
        sm_lab = T("sphingomyelin", 28, PC_WHITE).move_to([-1.16, 2.20, 0])
        self.play(*sm_swaps, FadeIn(sm_lab, shift=UP * 0.1), run_time=1.05)

        # Glycolipid sugars sprout outward only (LIME bead chains at idx 4, 9, 13, 15)
        self.at("Glycolipids")
        sugar_indices = (4, 9, 13, 15)
        chains = VGroup()
        for idx in sugar_indices:
            hd = world.top_heads[idx]
            chains.add(make_sugar_chain(hd.get_top() + UP * 0.02))
        sugar_lab = T("sugars: outward only", 28, LIME_SUGAR).move_to([3.0, 2.50, 0])
        self.play(
            *[GrowFromEdge(ch, DOWN) for ch in chains],
            FadeIn(sugar_lab, shift=UP * 0.1),
            run_time=1.1,
        )
        world.add(chains)
        band_grp.add(chains)

        # Name tag highlight and ease back to centered both-faces view
        self.at("name tag")
        self.play(
            *[Indicate(ch, color=LIME_SUGAR, scale_factor=1.15) for ch in chains],
            run_time=0.75,
        )
        self.play(
            FadeOut(sm_lab), FadeOut(sugar_lab),
            band_grp.animate.shift(UP * 0.30),
            run_time=0.8,
        )
        self.finish()


# ==============================================================================
# SCENE 06: The One Idea (13.5 s)
# ==============================================================================
class S06Idea(SpokenScene):
    def construct(self):
        door_xs = (-1.93, 5.03)
        top_kinds = ["pc" if i not in (2, 6, 11) else "sm" for i in range(16)]
        top_kinds[4] = "ps"  # stray PS adjacent to flippase (-1.93)
        bot_kinds = ["ps" if i in (1, 7) else ("pi" if i in (10, 12) else "grey") for i in range(16)]
        bot_kinds[6] = "none" # open destination slot for ps_move

        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=top_kinds, bot_kinds=bot_kinds,
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.65, sugar_indices=(8, 13, 15),
        )
        flip1 = make_door(-1.93, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        scram = make_door(5.03, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.45)
        x_p1 = world.bot_heads[1].get_center()[0]
        x_p2 = world.bot_heads[7].get_center()[0]
        prot1 = make_positive_protein([x_p1, -1.55 - 0.54, 0])
        prot2 = make_positive_protein([x_p2, -1.55 - 0.54, 0])
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(world, flip1, scram, prot1, prot2, out_lab, cy_lab)
        world.start_fluid_motion()

        self.at("sets a lipid's charge")
        self.play(Indicate(world.top_heads, color=PC_WHITE, scale_factor=1.08), run_time=0.65)
        self.play(
            *[Indicate(world.bot_heads[i], color=PS_MAGENTA, scale_factor=1.18) for i in (1, 7)],
            run_time=0.65,
        )

        self.at("Pumps")
        atp = boxed_label("ATP", FLIP_ORANGE, size=24, pad=0.10).move_to([-1.93, -2.75, 0]).set_z_index(4)
        self.play(Indicate(flip1, color=FLIP_ORANGE, scale_factor=1.06), FadeIn(atp), run_time=0.45)
        self.play(atp.animate.move_to([-1.93, -1.95, 0]), run_time=0.38)
        self.play(FadeOut(atp), run_time=0.22)

        ps_move = world.top_heads[4]
        self.play(ps_move.animate.move_to([-1.93, 1.55, 0]), run_time=0.35)
        self.play(ps_move.animate.move_to([-1.93, -1.55, 0]), run_time=0.80)
        self.play(ps_move.animate.move_to([-1.16, -1.55, 0]), run_time=0.32)

        self.at("Charge and location")
        idea_lab = T("charge + side = job", 34, GOLD, weight=BOLD).move_to([0.9, -3.05, 0])
        self.play(
            Indicate(prot1, color=PROT_CYAN, scale_factor=1.12),
            Indicate(prot2, color=PROT_CYAN, scale_factor=1.12),
            Indicate(world.sugars, color=LIME_SUGAR, scale_factor=1.12),
            FadeIn(idea_lab, shift=UP * 0.1),
            run_time=1.2,
        )
        self.finish()


# ==============================================================================
# SCENE 07: Apoptosis (16.125 s)
# ==============================================================================
class S07Apoptosis(SpokenScene):
    def construct(self):
        door_xs = (-3.48, -0.39, 3.48)
        top_kinds = ["pc" if i not in (2, 6) else "sm" for i in range(16)]
        top_kinds[11] = "none" # open slot for scrambled PS_c
        top_kinds[13] = "none" # open slot for scrambled PS_b
        bot_kinds = ["ps" if i in (1, 5, 6, 11, 13) else ("pi" if i in (9, 15) else "grey") for i in range(16)]

        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=top_kinds, bot_kinds=bot_kinds,
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.65, sugar_indices=(4, 8, 15),
        )
        flip1 = make_door(-3.48, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        flip2 = make_door(-0.39, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        scram = make_door(3.48, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.42)
        scram_off = T("scramblase: off", 26, SCRAM_PURPLE).move_to([3.48, 2.55, 0]).set_opacity(0.78)

        idea_lab = T("charge + side = job", 34, GOLD, weight=BOLD).move_to([0.9, -3.05, 0])
        apop_tag = boxed_label("apoptosis", RED, size=26, pad=0.12).move_to([-5.15, 3.15, 0])
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(world, flip1, flip2, scram, scram_off, idea_lab, out_lab, cy_lab)
        world.start_fluid_motion()

        self.play(FadeOut(idea_lab), FadeIn(apop_tag, shift=DOWN * 0.1), run_time=0.6)

        self.at("shut off")
        x1 = make_cross(RED).move_to(flip1)
        x2 = make_cross(RED).move_to(flip2)
        self.play(
            flip1.animate.set_opacity(0.28),
            flip2.animate.set_opacity(0.28),
            Create(x1), Create(x2),
            run_time=0.85,
        )

        self.at("switch on")
        scram_open = make_door(3.48, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=False)
        scram_on = T("scramblase: on", 26, SCRAM_PURPLE).move_to([3.48, 2.55, 0])
        self.play(
            Transform(scram, scram_open),
            swap(scram_off, scram_on, run_time=0.8),
            run_time=0.9,
        )

        self.at("crossing both ways")
        ps_a = world.bot_heads[5]
        ps_b = world.bot_heads[11]
        ps_c = world.bot_heads[13]
        pc_a = world.top_heads[10]
        pc_b = world.top_heads[9]

        # Batch 1: PS_c up -> top[11] (2.71), PC_a down -> bot[13] (4.25)
        self.play(
            ps_c.animate.move_to([3.48, -1.55, 0]),
            pc_a.animate.move_to([3.48, 1.55, 0]),
            run_time=0.50,
        )
        self.play(
            ps_c.animate.move_to([3.48, 1.55, 0]),
            pc_a.animate.move_to([3.48, -1.55, 0]),
            run_time=0.95,
        )
        self.play(
            ps_c.animate.move_to([2.71, 1.55, 0]),
            pc_a.animate.move_to([4.25, -1.55, 0]),
            run_time=0.45,
        )

        # Batch 2: PS_b up -> top[13] (4.25), PC_b arcs over parked PS_c to enter scramblase then down -> bot[11] (2.71), then PS_a up -> top[9] (1.16)
        p0 = pc_b.get_center()
        p1 = np.array([3.48, 1.55, 0.0])
        us = np.linspace(0.0, 1.0, 25)
        arc_pts = [
            [interpolate(p0[0], p1[0], u), interpolate(p0[1], p1[1], u) + 0.60 * np.sin(np.pi * u), 0.0]
            for u in us
        ]
        pc_b_arc = VMobject().set_points_smoothly(arc_pts)
        self.play(
            ps_b.animate.move_to([3.48, -1.55, 0]),
            MoveAlongPath(pc_b, pc_b_arc),
            run_time=0.50,
        )
        self.play(
            ps_b.animate.move_to([3.48, 1.55, 0]),
            pc_b.animate.move_to([3.48, -1.55, 0]),
            run_time=0.85,
        )
        self.play(
            ps_b.animate.move_to([4.25, 1.55, 0]),
            pc_b.animate.move_to([2.71, -1.55, 0]),
            ps_a.animate.move_to([3.48, -1.55, 0]),
            run_time=0.55,
        )
        self.play(ps_a.animate.move_to([3.48, 1.55, 0]), run_time=0.75)
        self.play(ps_a.animate.move_to([1.16, 1.55, 0]), run_time=0.45)
        self.finish()


# ==============================================================================
# SCENE 08: Predict (8.525 s)
# ==============================================================================
def _build_predict_world():
    """Shared builder for s08_predict, s09_pause, and s10_answer start state."""
    world = make_three_cell_world(dying_ps_top=True, veil_middle=True, open_scram=True)
    ps_cross = make_head("ps", r=0.11).move_to([0.0, -1.75, 0]).set_z_index(4)
    pc_cross = make_head("pc", r=0.11).move_to([0.0, 0.75, 0]).set_z_index(4)
    world.add(ps_cross, pc_cross)
    world._cross_t = 0.0

    def _scram_traffic(mob, dt):
        mob._cross_t += dt
        s = 0.5 - 0.5 * np.cos(1.4 * mob._cross_t)
        ps_cross.move_to([0.0, interpolate(-1.75, 0.75, s), 0])
        pc_cross.move_to([0.15, interpolate(0.75, -1.75, s), 0])

    world.add_updater(_scram_traffic)
    world.start_fluid_motion()
    return world


class S08Predict(SpokenScene):
    def construct(self):
        world = _build_predict_world()
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)
        self.add(world, out_lab, cy_lab)

        self.at("macrophage glides")
        mac = make_macrophage(center=(-5.4, 1.85, 0), rx=1.05, ry=0.55)
        self.play(FadeIn(mac, shift=RIGHT * 0.4), run_time=0.65)
        self.play(
            UpdateFromAlphaFunc(
                mac,
                lambda m, a: setattr(m, "_mac_center", np.array([interpolate(-5.4, 0.0, a), 1.85, 0.0])),
            ),
            run_time=2.7, rate_func=smooth,
        )

        self.at("What will it now find")
        q = question_card("What does it find?", y=3.20, color=TEXT, size=32, max_w=7.5)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ==============================================================================
# SCENE 09: Predict Pause (4.5 s silent)
# ==============================================================================
class S09Pause(PredictPause):
    QUESTION = "What does it find?"
    CARD = {"y": 3.20, "color": TEXT, "size": 32, "max_w": 7.5}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        world = _build_predict_world()
        mac = make_macrophage(center=(0.0, 1.85, 0), rx=1.05, ry=0.55)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)
        return VGroup(world, mac, out_lab, cy_lab)


# ==============================================================================
# SCENE 10: Answer (17.05 s)
# ==============================================================================
class S10Answer(SpokenScene):
    def construct(self):
        world = _build_predict_world()
        mac = make_macrophage(center=(0.0, 1.85, 0), rx=1.05, ry=0.55)
        q = question_card("What does it find?", y=3.20, color=TEXT, size=32, max_w=7.5)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(world, mac, q, out_lab, cy_lab)

        self.at("Phosphatidylserine")
        outer_ps = VGroup(*[world.top_heads[i] for i in (11, 13, 16, 18)])
        ps_out_lab = T("PS outside", 28, PS_MAGENTA).move_to([-2.7, 2.05, 0])
        self.play(
            FadeOut(q), FadeOut(world.veil),
            outer_ps.animate.scale(1.22),
            FadeIn(ps_out_lab, shift=UP * 0.1),
            run_time=1.3,
        )

        self.at("macrophage reads")
        self.play(
            UpdateFromAlphaFunc(
                mac,
                lambda m, a: (
                    setattr(m, "_mac_center", np.array([0.0, interpolate(1.85, 1.65, a), 0.0])),
                    setattr(m, "_mac_reach", a),
                ),
            ),
            run_time=2.1,
        )

        self.at("eat me signal")
        eat_lab = T("eat me", 28, GOLD, weight=BOLD).move_to([2.6, 2.05, 0])
        self.play(
            FadeIn(eat_lab, shift=UP * 0.1),
            Indicate(outer_ps, color=PS_MAGENTA, scale_factor=1.15),
            run_time=1.1,
        )

        self.at("engulfs the dying")
        self.play(
            FadeOut(ps_out_lab), FadeOut(eat_lab),
            UpdateFromAlphaFunc(
                mac,
                lambda m, a: (
                    setattr(m, "_mac_center", np.array([0.0, interpolate(1.65, -0.50, a), 0.0])),
                    setattr(m, "_mac_engulf", a),
                ),
            ),
            run_time=2.4,
        )

        self.at("healthy neighbors")
        left_ps = VGroup(*[world.bot_heads[i] for i in (1, 4, 7)])
        right_ps = VGroup(*[world.bot_heads[i] for i in (21, 24, 27)])
        left_tag = T("PS inside", 26, PS_MAGENTA).move_to([-4.1, -2.45, 0])
        right_tag = T("PS inside", 26, PS_MAGENTA).move_to([4.1, -2.45, 0])
        self.play(
            Indicate(left_ps, color=PS_MAGENTA, scale_factor=1.22),
            Indicate(right_ps, color=PS_MAGENTA, scale_factor=1.22),
            FadeIn(left_tag, shift=UP * 0.1),
            FadeIn(right_tag, shift=UP * 0.1),
            run_time=1.3,
        )
        self.finish()


# ==============================================================================
# SCENE 11: Close (13.35 s)
# ==============================================================================
class S11Close(SpokenScene):
    def construct(self):
        door_xs = (-1.93, 2.71)
        world = make_single_cell_world(
            y_center=0.0, half_h=1.55,
            top_kinds=["pc"] * 16,
            bot_kinds=["ps" if i in (1, 5, 7, 13) else "grey" for i in range(16)],
            door_xs=door_xs, door_gap=0.35,
            tail_opacity=0.68,
        )
        flip = make_door(-1.93, 0.0, 1.55, color=FLIP_ORANGE, kind="flippase")
        scram = make_door(2.71, 0.0, 1.55, color=SCRAM_PURPLE, kind="scramblase", closed=True).set_opacity(0.35)
        out_lab = T("outside", 28, TEXT).move_to(OUTSIDE_AT)
        cy_lab = T("cytoplasm", 28, TEXT).move_to(CYTO_AT)

        self.add(world, flip, scram, out_lab, cy_lab)
        world.start_fluid_motion()

        self.at("flag was there")
        flag_head = world.bot_heads[7]
        flag_lab = T("the flag, kept inside", 28, PS_MAGENTA).move_to([0.3, -2.45, 0])
        self.play(
            Indicate(flag_head, color=PS_MAGENTA, scale_factor=1.22),
            FadeIn(flag_lab, shift=UP * 0.1),
            run_time=1.0,
        )

        self.at("Pumps spending")
        atp = boxed_label("ATP", FLIP_ORANGE, size=24, pad=0.10).move_to([-1.93, -2.75, 0]).set_z_index(4)
        self.play(Indicate(flip, color=FLIP_ORANGE, scale_factor=1.06), FadeIn(atp), run_time=0.45)
        self.play(atp.animate.move_to([-1.93, -1.95, 0]), run_time=0.45)
        self.play(FadeOut(atp, scale=1.2), run_time=0.3)

        self.at("writes no new")
        self.play(Indicate(flag_head, color=PS_MAGENTA, scale_factor=1.12), run_time=0.7)

        self.at("moves an old")
        ghost = make_head("ps", r=0.20).set_opacity(0.75).move_to(flag_head.get_center()).set_z_index(5)
        self.add(ghost)
        self.play(ghost.animate.move_to([2.71, -1.55, 0]), run_time=0.4)
        self.play(ghost.animate.move_to([2.71, 1.55, 0]), run_time=0.9)
        self.play(Indicate(ghost, color=PS_MAGENTA, scale_factor=1.25), run_time=0.45)
        self.play(FadeOut(ghost), run_time=0.55)
        self.finish()


# ==============================================================================
# SCENE 12: End Card (3.5 s silent)
# ==============================================================================
class S12End(EndCard):
    LINE = "A lipid's charge and its side of the membrane set its job."
