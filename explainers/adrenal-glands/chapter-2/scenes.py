"""
COLOUR MAP (one colour per concept for the entire film):
- C_ALDO = YELLOW   (#F5D547) : aldosterone & aldosterone branch
- C_CORT = PURPLE   (#B57EDC) : cortisol (filled dots, cortisol branch, adenoma, cortisol brake)
- C_PREC = PURPLE   (#B57EDC) : hollow purple rings = backed-up precursors (17-OH-progesterone / progesterone)
- C_MR   = BLUE     (#58C4DD) : mineralocorticoid / kidney receptor
- C_ENZ_ON  = GREEN (#83C167) : working enzyme (guard enzyme, 21-hydroxylase gates)
- C_ENZ_OFF = RED   (#FC6255) : switched-off / closed enzyme gate
- C_NA   = TEAL     (#3FB8C0) : sodium ions lost when MR is unactivated
- C_ANDR = MAGENTA  (#FF6EC7) : adrenal androgens & androgen branch
- C_ACTH = TEXT     (#E8EAF0) : ACTH (thick white arrows & signal pulses) & pituitary outline
- C_CHOL = GREY     (#8B93A1) : cholesterol base, shared trunk, cortex silhouette, divider

CARRIED WORLD:
Left 65% of the frame: THE STEROID TREE (an adrenal cortex silhouette enclosing the trunk from
cholesterol -> fork into aldosterone, cortisol, androgens, with 21-hydroxylase gates on aldosterone
& cortisol branches). Right side: white pituitary with ACTH arrow & signal pulses driving the trunk
base, and the blue kidney receptor in the lower-right corner. A small 'schematic' tag sits at
bottom-left all film.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Computed dot trajectories carry cortisol through the green guard enzyme
  (turning grey) and aldosterone into the blue receptor; camera pulls left as receptor shrinks to lower
  right and the tree grows with continuous Bezier-advected steroid flow; one gate flickers red and
  magenta androgen flow surges.
- s02_tree: Trunk glows; pituitary & ACTH arrow with traveling signal pulses appear and computed particle
  speed increases; each branch illuminates in turn; both 21-hydroxylase gates pulse; androgen branch glows.
- s03_rule: Three-step rule strip builds with pointers to gates, receptor, and pituitary; ghost block
  computed on the cortisol branch thins downstream dots and accumulates hollow precursor rings upstream.
- s04_step_one: Both 21-hydroxylase gates close (red X); computed downstream flow on cortisol &
  aldosterone drops near zero while hollow purple 17-OH-progesterone rings accumulate upstream of the block.
- s05_step_two: Kidney receptor scales up to ~1/4 frame; hollow purple rings drift along a trajectory from
  the pile to lodge loosely in the empty socket without lighting it; teal sodium dots drift downward.
- s06_step_three: Receptor shrinks back; cortisol brake arrow fades to ghost; ACTH arrow thickens and
  pulsing signal accelerates computed trunk flow, spilling surplus dots into the open magenta androgen
  branch while the cortex silhouette widens (hyperplasia) and teal sodium dots keep falling.
- s07_predict: Gates reopen; world splits into two side-by-side half-size trees, one driven by thick
  pulsing ACTH and one by an autonomous purple adenoma pumping cortisol; both androgen tips grey out to '?'.
- s09_answer: Left tree accelerates trunk flow into a bright swollen magenta branch ('androgens up');
  right tree builds a purple cortisol brake to the pituitary, thinning ACTH to dashed and emptying its
  androgen branch ('androgens down').
- s10_return: Trees merge back into the single full tree with receptor and pituitary; gates, receptor, and
  feedback loops pulse in sequence, and direction-only arrows settle beside the three branch tips.
"""
from bp_parts import *

# ------------------------------------------------------------------ concept palette
C_ALDO = YELLOW
C_CORT = "#B57EDC"
C_PREC = "#B57EDC"
C_MR = BLUE
C_ENZ_ON = GREEN
C_ENZ_OFF = RED
C_NA = TEAL
C_ANDR = "#FF6EC7"
C_ACTH = TEXT
C_CHOL = GREY


def make_schematic_tag():
    """Small 'schematic' tag at bottom-left, inside safe margin."""
    t = T("schematic", size=22, color=GREY)
    t.move_to([-6.55 + t.width / 2, -3.65 + t.height / 2, 0])
    return t


# ------------------------------------------------------------------ spline math
def bez(p0, p1, p2, p3, u):
    u = float(u)
    m = 1.0 - u
    return (m ** 3) * p0 + 3.0 * (m ** 2) * u * p1 + 3.0 * m * (u ** 2) * p2 + (u ** 3) * p3


def bez_tan(p0, p1, p2, p3, u):
    u = float(u)
    m = 1.0 - u
    v = 3.0 * (m ** 2) * (p1 - p0) + 6.0 * m * u * (p2 - p1) + 3.0 * (u ** 2) * (p3 - p2)
    n = np.linalg.norm(v[:2])
    return v / max(n, 1e-6)


def bez_mobject(p0, p1, p2, p3, color, width, opacity=1.0, n=40):
    pts = [bez(p0, p1, p2, p3, t) for t in np.linspace(0.0, 1.0, n)]
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


# ------------------------------------------------------------------ receptor geometry
def make_receptor(center, height=1.0, color=C_MR, fill_opacity=0.28, stroke_width=3.5):
    """Blue C-shaped mineralocorticoid receptor with socket facing left."""
    c = np.array(center, dtype=float)
    r_out = height * 0.50
    r_in = height * 0.25
    a1 = np.linspace(-0.72 * PI, 0.72 * PI, 28)
    outer = [np.array([r_out * np.cos(a), r_out * np.sin(a), 0.0]) for a in a1]
    inner = [np.array([r_in * np.cos(a), r_in * np.sin(a), 0.0]) for a in reversed(a1)]
    cup = Polygon(
        *(outer + inner),
        stroke_color=color,
        stroke_width=stroke_width,
        fill_color=color,
        fill_opacity=fill_opacity,
    )
    cup.move_to(c)
    cup.socket_center = cup.get_center() + LEFT * (height * 0.16)
    return cup


# ------------------------------------------------------------------ tree geometry & particle flow
def tree_spec(fork=(-2.4, -0.80, 0.0), scale=1.0):
    """Compute geometric control points for the steroid tree + pituitary."""
    f = np.array(fork, dtype=float)
    s = float(scale)
    P = lambda dx, dy: f + np.array([dx * s, dy * s, 0.0])

    base = P(0.0, -2.00)
    cort_dy = 2.65 if s > 0.7 else 2.90
    side_dy = 2.35 if s > 0.7 else 1.88
    aldo_dx = -3.05 if s > 0.7 else -2.75
    cort_dx = 0.38 if s > 0.7 else 0.25
    branches = {
        0: (P(0.0, 0.0), P(-1.78, 0.20), P(-2.90, 1.05), P(aldo_dx, side_dy)),
        1: (P(0.0, 0.0), P(0.16, 0.80), P(0.32, 1.72), P(cort_dx, cort_dy)),
        2: (P(0.0, 0.0), P(1.60, 0.28), P(2.72, 1.10), P(3.05, side_dy)),
    }
    gates_u = {0: 0.50, 1: 0.62}
    if s > 0.7:
        pit_center = P(6.95, 2.25)
        acth_pts = (
            pit_center + np.array([-1.05, -0.25, 0.0]),
            P(4.15, -0.05),
            P(2.35, -1.30),
            P(0.32, -1.42),
        )
        brake_pts = (
            branches[1][3] + np.array([0.85, 0.35, 0.0]),
            P(2.25, 3.38),
            P(4.95, 3.38),
            pit_center + np.array([-0.20, 0.42, 0.0]),
        )
    else:
        pit_center = P(5.80, 1.25)
        acth_pts = (
            pit_center + np.array([-0.72, -0.14, 0.0]),
            P(4.00, -0.35),
            P(2.20, -1.30),
            P(0.22, -1.35),
        )
        brake_pts = (
            branches[1][3] + np.array([1.02, 0.42, 0.0]),
            P(3.10, 5.25),
            P(6.35, 4.70),
            pit_center + np.array([0.18, 0.32, 0.0]),
        )
    return {
        "fork": f,
        "base": base,
        "scale": s,
        "branches": branches,
        "gates_u": gates_u,
        "pit_center": pit_center,
        "acth_pts": acth_pts,
        "brake_pts": brake_pts,
    }


def make_gate(pos, tangent, color=C_ENZ_ON, scale=1.0, closed=False):
    """Enzyme gate block oriented perpendicular to the branch."""
    ang = np.arctan2(tangent[1], tangent[0])
    w, h = 0.48 * scale, 0.26 * scale
    box = RoundedRectangle(
        corner_radius=0.07 * scale,
        width=h,
        height=w,
        stroke_color=color,
        stroke_width=3.2,
        fill_color=color,
        fill_opacity=0.32,
    )
    box.rotate(ang)
    box.move_to(pos)
    if closed:
        d = 0.19 * scale
        cross = VGroup(
            Line(pos + np.array([-d, -d, 0]), pos + np.array([d, d, 0]), color=C_ENZ_OFF, stroke_width=4.2),
            Line(pos + np.array([-d, d, 0]), pos + np.array([d, -d, 0]), color=C_ENZ_OFF, stroke_width=4.2),
        )
        return VGroup(box, cross)
    return VGroup(box)


def make_cortex_silhouette(spec, widen=1.0):
    """Rich shaded cortex organ silhouette hugging the trunk and three curved branches."""
    s = spec["scale"]
    f = spec["fork"]
    b = spec["base"]
    pts = [b + np.array([-0.52 * s * widen, -0.12 * s, 0.0]), f + np.array([-0.54 * s * widen, -0.48 * s, 0.0])]
    off = 0.33 * s * widen
    # Trace outer/inner offsets along each branch so the bays stay completely open
    for br_idx in (0, 1, 2):
        bp = spec["branches"][br_idx]
        us = np.linspace(0.15, 0.92, 6)
        left_pts, right_pts = [], []
        for u in us:
            p = bez(*bp, u)
            t = bez_tan(*bp, u)
            nrm = np.array([-t[1], t[0], 0.0])
            taper = 0.42 + 0.58 * ((u - 0.15) / 0.77)
            in_off = min(off, 0.34 * s) * taper
            l_off = off if br_idx == 0 else in_off
            r_off = off if br_idx == 2 else in_off
            left_pts.append(p + nrm * l_off)
            right_pts.append(p - nrm * r_off)
        pts.extend(left_pts)
        pts.extend(reversed(right_pts))
        if br_idx < 2:
            # Dip into fork bay
            nxt_p = bez(*spec["branches"][br_idx + 1], 0.18)
            cur_p = bez(*bp, 0.18)
            pts.append(0.5 * (cur_p + nxt_p) + np.array([0.0, -0.05 * s, 0.0]))
    pts.extend([f + np.array([0.54 * s * widen, -0.48 * s, 0.0]), b + np.array([0.52 * s * widen, -0.12 * s, 0.0])])
    poly = Polygon(
        *pts,
        stroke_color=C_CHOL,
        stroke_width=2.6,
        stroke_opacity=0.50,
        fill_color="#2A364F",
        fill_opacity=0.88,
    )
    poly.round_corners(radius=0.18 * s)
    return poly


class SteroidTree(VGroup):
    """Carried steroid tree + cortex silhouette + computed particle flow + ACTH pulse stream."""

    def __init__(
        self,
        fork=(-2.4, -0.75, 0.0),
        scale=1.0,
        label_size=28,
        show_labels=True,
        show_pituitary=False,
        pit_label_size=26,
        seed=7,
        n_dots=38,
        n_pile=14,
    ):
        super().__init__()
        self.spec = tree_spec(fork, scale)
        self.scale_val = scale
        self.rng = np.random.default_rng(seed)

        # Simulation state trackers
        self.flow_speed = ValueTracker(1.0)
        self.aldo_open = ValueTracker(1.0)
        self.cort_open = ValueTracker(1.0)
        self.andr_boost = ValueTracker(1.0)
        self.andr_grey = ValueTracker(0.0)
        self.pile_level = ValueTracker(0.0)
        self.adenoma_on = ValueTracker(0.0)
        self.gland_width = ValueTracker(1.0)
        self.acth_active = ValueTracker(1.0 if show_pituitary else 0.0)
        self.acth_suppressed = ValueTracker(0.0)

        s = self.spec["scale"]
        lw_trunk = 22.0 * s
        lw_branch = 16.0 * s

        # Shaded gland silhouette behind the tree
        self.cortex_bg = make_cortex_silhouette(self.spec, widen=1.0)
        self.add(self.cortex_bg)

        # Main pathway channels
        self.trunk_line = Line(self.spec["base"], self.spec["fork"], stroke_color=C_CHOL, stroke_width=lw_trunk, stroke_opacity=0.62)
        self.branch_lines = VGroup(
            bez_mobject(*self.spec["branches"][0], color=C_ALDO, width=lw_branch, opacity=0.42),
            bez_mobject(*self.spec["branches"][1], color=C_CORT, width=lw_branch, opacity=0.42),
            bez_mobject(*self.spec["branches"][2], color=C_ANDR, width=lw_branch, opacity=0.42),
        )
        self.add(self.trunk_line, self.branch_lines)

        # Enzyme gates on branches 0 and 1
        self.gate_pos = {}
        self.gate_tan = {}
        self.gates = VGroup()
        for b in (0, 1):
            u = self.spec["gates_u"][b]
            pts = self.spec["branches"][b]
            p = bez(*pts, u)
            tan = bez_tan(*pts, u)
            self.gate_pos[b] = p
            self.gate_tan[b] = tan
            self.gates.add(make_gate(p, tan, color=C_ENZ_ON, scale=s, closed=False))
        self.add(self.gates)

        # Particle pool (computed flow along trunk + branches)
        self.dots_layer = VGroup()
        self.particles = []
        r_dot = max(0.082, 0.115 * s)
        for i in range(n_dots):
            d = Dot(radius=r_dot, color=TEXT, fill_opacity=0.98)
            d.move_to(self.spec["base"])
            self.dots_layer.add(d)
            branch = i % 3
            s_prog = (i / n_dots) * 2.0
            lat = self.rng.uniform(-0.05 * s, 0.05 * s)
            sp = self.rng.uniform(0.90, 1.12)
            self.particles.append([d, branch, s_prog, lat, sp, False])
        self.add(self.dots_layer)

        # Precursor pile (hollow purple rings before cortisol gate)
        self.pile_layer = VGroup()
        self.pile_rings = []
        pile_center = bez(*self.spec["branches"][1], 0.36)
        self.pile_center = pile_center
        for i in range(n_pile):
            ang = i * 2.39996
            rad = (0.04 + 0.055 * np.sqrt(i)) * s
            offset = np.array([rad * np.cos(ang), rad * np.sin(ang) * 0.85, 0.0])
            ring = Circle(
                radius=max(0.055, 0.085 * s),
                stroke_color=C_PREC,
                stroke_width=3.2 if s > 0.7 else 2.4,
                fill_opacity=0.0,
            )
            ring.move_to(pile_center + offset)
            ring.set_stroke(opacity=0.0)
            self.pile_layer.add(ring)
            self.pile_rings.append((ring, offset, float(i) / n_pile))
        self.add(self.pile_layer)

        # Labels (created at full size, never scaled!)
        self.labels = VGroup()
        self.lbl_chol = T("cholesterol", size=max(24, label_size - 2), color=TEXT).next_to(
            self.spec["base"], DOWN, buff=0.22
        )
        t0 = self.spec["branches"][0][3]
        t1 = self.spec["branches"][1][3]
        t2 = self.spec["branches"][2][3]
        off_y = 0.42 if s > 0.7 else 0.44
        self.lbl_aldo = T("aldosterone", size=label_size, color=C_ALDO).move_to(t0 + UP * off_y)
        self.lbl_cort = T("cortisol", size=label_size, color=C_CORT).move_to(t1 + UP * off_y)
        self.lbl_andr = T("androgens", size=label_size, color=C_ANDR).move_to(t2 + UP * off_y)
        if s < 0.7:
            self.lbl_aldo.shift(RIGHT * 0.05)
            self.lbl_andr.shift(RIGHT * 0.20)
        if show_labels:
            self.labels.add(self.lbl_chol, self.lbl_aldo, self.lbl_cort, self.lbl_andr)
            self.add(self.labels)

        # Pituitary + ACTH arrow + traveling ACTH signal pulses
        self.pit_group = VGroup()
        self.acth_pulses = []
        if show_pituitary:
            pw = 2.35 if s > 0.7 else 1.54
            ph = 0.88 if s > 0.7 else 0.58
            self.pit_box = RoundedRectangle(
                corner_radius=0.14,
                width=pw,
                height=ph,
                stroke_color=C_ACTH,
                stroke_width=3.2,
                fill_color="#2A364F",
                fill_opacity=0.95,
            ).move_to(self.spec["pit_center"])
            self.pit_lbl = T("pituitary", size=pit_label_size, color=C_ACTH).move_to(self.pit_box)
            self.acth_curve = self._make_acth_arrow(width=6.5 if s > 0.7 else 5.0)
            mid_pt = bez(*self.spec["acth_pts"], 0.45)
            self.acth_lbl = T("ACTH", size=max(24, pit_label_size - 2), color=C_ACTH).next_to(
                mid_pt, DR, buff=0.26
            )
            pulse_layer = VGroup()
            for k in range(6):
                pd = Dot(radius=0.095 if s > 0.7 else 0.072, color=C_ACTH, fill_opacity=0.95)
                u_init = k / 6.0
                pd.move_to(bez(*self.spec["acth_pts"], u_init))
                pulse_layer.add(pd)
                self.acth_pulses.append([pd, u_init])
            self.pit_group.add(self.pit_box, self.pit_lbl, self.acth_curve, pulse_layer, self.acth_lbl)
            self.add(self.pit_group)

        self._last_gw = 1.0
        # Attach updater to dots_layer (never directly to SteroidTree) so animating sibling labels
        # with swap/FadeOut/Transform never suspends the simulation updater.
        self.dots_layer.add_updater(self._step)

    def _make_acth_arrow(self, width=6.5, dashed=False, opacity=1.0):
        pts = [bez(*self.spec["acth_pts"], u) for u in np.linspace(0.0, 1.0, 36)]
        if dashed:
            g = VGroup()
            for k in range(0, len(pts) - 2, 3):
                g.add(Line(pts[k], pts[k + 1], color=C_ACTH, stroke_width=width, stroke_opacity=opacity))
            tip_dir = pts[-1] - pts[-2]
        else:
            curve = VMobject(stroke_color=C_ACTH, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
            curve.set_points_as_corners(pts)
            g = VGroup(curve)
            tip_dir = pts[-1] - pts[-2]
        ang = np.arctan2(tip_dir[1], tip_dir[0])
        head = Triangle(fill_color=C_ACTH, fill_opacity=opacity, stroke_width=0).scale(0.14 * max(0.7, self.scale_val))
        head.rotate(ang - PI / 2).move_to(pts[-1])
        g.add(head)
        return g

    def _pos_for(self, branch, s_prog, lat):
        if s_prog <= 1.0:
            p = self.spec["base"] + s_prog * (self.spec["fork"] - self.spec["base"])
            return p + np.array([lat, 0.0, 0.0])
        u = np.clip(s_prog - 1.0, 0.0, 1.0)
        pts = self.spec["branches"][branch]
        p = bez(*pts, u)
        t = bez_tan(*pts, u)
        perp = np.array([-t[1], t[0], 0.0])
        return p + perp * lat

    def _choose_branch(self):
        w0 = 1.0 if self.aldo_open.get_value() > 0.3 else 0.14
        w1 = 1.0 if self.cort_open.get_value() > 0.3 else 0.22
        w2 = max(0.15, float(self.andr_boost.get_value()))
        if self.cort_open.get_value() <= 0.3 and w2 > 1.2:
            w2 *= 1.8
        probs = np.array([w0, w1, w2], dtype=float)
        probs /= probs.sum()
        return int(self.rng.choice([0, 1, 2], p=probs))

    def _step(self, mob, dt):
        if dt <= 0:
            return
        dt = min(dt, 0.1)
        v = float(self.flow_speed.get_value())
        aldo_on = self.aldo_open.get_value()
        cort_on = self.cort_open.get_value()
        andr_b = self.andr_boost.get_value()
        andr_g = self.andr_grey.get_value()
        adenoma = self.adenoma_on.get_value()
        gw = float(self.gland_width.get_value())
        s = self.scale_val

        # Update gland silhouette width only when it changes
        if abs(gw - self._last_gw) > 0.01:
            self._last_gw = gw
            new_bg = make_cortex_silhouette(self.spec, widen=gw)
            self.cortex_bg.become(new_bg)

        # Update androgen branch colour (magenta vs greyed)
        andr_col = interpolate_color(ManimColor(C_ANDR), ManimColor(C_CHOL), float(np.clip(andr_g, 0.0, 1.0)))
        andr_op = 0.24 if andr_b < 0.3 else (0.90 if andr_b > 1.5 else 0.46)
        andr_w = 16.0 * s * (1.42 if andr_b > 1.5 else (0.75 if andr_b < 0.3 else 1.0))
        self.branch_lines[2].set_stroke(color=andr_col, opacity=andr_op, width=andr_w)

        # Update precursor pile visibility
        pl = float(np.clip(self.pile_level.get_value(), 0.0, 1.0))
        for ring, _, frac in self.pile_rings:
            ring.set_stroke(opacity=0.95 if frac < pl else 0.0)

        # Step ACTH signal pulses along the arrow
        if self.acth_pulses and self.acth_active.get_value() > 0.5:
            sup = self.acth_suppressed.get_value()
            p_speed = 0.25 if sup > 0.5 else 0.55 * max(0.8, v * 0.8)
            p_op = 0.25 if sup > 0.5 else 0.95
            for pd_item in self.acth_pulses:
                pd, u = pd_item
                u = (u + dt * p_speed) % 1.0
                pd_item[1] = u
                pd.move_to(bez(*self.spec["acth_pts"], u))
                pd.set_fill(opacity=p_op)

        # Step steroid particles
        for idx, p in enumerate(self.particles):
            dot, br, sp, lat, mult, is_ad = p
            if is_ad:
                sp += dt * 0.72 * mult
                if sp >= 2.0:
                    sp = 1.58
                dot.move_to(self._pos_for(1, sp, lat))
                dot.set_color(C_CORT)
                dot.set_fill(opacity=0.98 if adenoma > 0.5 else 0.0)
                p[2] = sp
                continue

            if adenoma > 0.5 and idx % 5 == 0:
                p[5] = True
                p[1] = 1
                p[2] = 1.58 + (idx % 3) * 0.12
                continue

            rate = 0.68 * v * mult
            if sp > 1.0:
                gate_s = 1.0 + self.spec["gates_u"].get(br, 0.55)
                if br == 0 and aldo_on < 0.3 and sp > gate_s - 0.06:
                    rate *= 0.06
                elif br == 1 and cort_on < 0.3 and sp > gate_s - 0.06:
                    rate *= 0.06
                elif br == 2:
                    rate *= float(np.clip(andr_b, 0.20, 2.0))

            sp += dt * rate
            if sp >= 2.0:
                sp = 0.0
                br = self._choose_branch()
                p[1] = br
            if br == 1 and cort_on < 0.3 and 1.48 < sp < 1.56 and idx % 3 != 0:
                sp = 0.0
                br = self._choose_branch()
                p[1] = br

            p[2] = sp
            dot.move_to(self._pos_for(br, sp, lat))

            if sp <= 1.05:
                dot.set_color(TEXT)
                dot.set_fill(opacity=0.92)
            else:
                gate_s = 1.0 + self.spec["gates_u"].get(br, 0.55)
                if br == 0:
                    if sp >= gate_s:
                        dot.set_color(C_ALDO)
                        dot.set_fill(opacity=0.98 if aldo_on > 0.3 else 0.22)
                    else:
                        dot.set_color(TEXT)
                        dot.set_fill(opacity=0.92)
                elif br == 1:
                    if sp >= gate_s:
                        dot.set_color(C_CORT)
                        dot.set_fill(opacity=0.98 if cort_on > 0.3 else 0.22)
                    else:
                        dot.set_color(C_CORT if cort_on < 0.3 else TEXT)
                        dot.set_fill(opacity=0.92)
                else:
                    dot.set_color(andr_col)
                    dot.set_fill(opacity=0.22 if andr_b < 0.3 else 0.98)


# ------------------------------------------------------------------ shared builders
def build_carried_world(
    cort_open=1.0,
    aldo_open=1.0,
    pile_level=0.0,
    flow_speed=1.0,
    andr_boost=1.0,
    show_pituitary=True,
    receptor_big=False,
    seed=7,
):
    tree = SteroidTree(show_pituitary=show_pituitary, seed=seed)
    tree.cort_open.set_value(cort_open)
    tree.aldo_open.set_value(aldo_open)
    tree.pile_level.set_value(pile_level)
    tree.flow_speed.set_value(flow_speed)
    tree.andr_boost.set_value(andr_boost)
    if cort_open < 0.3:
        tree.gates[1].become(make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_OFF, 1.0, closed=True))
        tree.lbl_cort.set_opacity(0.45)
    if aldo_open < 0.3:
        tree.gates[0].become(make_gate(tree.gate_pos[0], tree.gate_tan[0], C_ENZ_OFF, 1.0, closed=True))
        tree.lbl_aldo.set_opacity(0.45)
    if receptor_big:
        rec = make_receptor((4.45, -1.20, 0.0), height=2.25)
        rec_lbl = T("kidney receptor", size=26, color=C_MR).move_to([4.65, 0.24, 0.0])
    else:
        rec = make_receptor((4.85, -1.95, 0.0), height=1.35)
        rec_lbl = T("kidney receptor", size=24, color=C_MR).next_to(rec, DOWN, buff=0.18)
    return tree, rec, rec_lbl


def make_rule_strip(active=None):
    items = [
        ("1 enzymes", -4.1),
        ("2 receptors", 0.0),
        ("3 loops", 4.1),
    ]
    g = VGroup()
    for idx, (txt, x) in enumerate(items, 1):
        is_on = (active == idx)
        col = GOLD if is_on else TEXT
        op = 1.0 if is_on else 0.55
        lbl = T(txt, size=28, color=col).set_opacity(op)
        box = RoundedRectangle(
            corner_radius=0.12,
            width=lbl.width + 0.44,
            height=lbl.height + 0.24,
            stroke_color=col,
            stroke_width=3.0 if is_on else 2.0,
            stroke_opacity=op,
            fill_color=col,
            fill_opacity=0.20 if is_on else 0.07,
        ).move_to([x, 3.22, 0.0])
        lbl.move_to(box)
        g.add(VGroup(box, lbl))
    return g


def make_brake_arrow(tree, width=3.5, opacity=1.0):
    pts = [bez(*tree.spec["brake_pts"], u) for u in np.linspace(0.0, 1.0, 32)]
    line = VMobject(stroke_color=C_CORT, stroke_width=width, stroke_opacity=opacity, fill_opacity=0.0)
    line.set_points_as_corners(pts)
    bdir = pts[-1] - pts[-2]
    tip = Triangle(fill_color=C_CORT, fill_opacity=opacity, stroke_width=0).scale(0.11 * max(0.75, tree.scale_val))
    tip.rotate(np.arctan2(bdir[1], bdir[0]) - PI / 2).move_to(pts[-1])
    return VGroup(line, tip)


# ------------------------------------------------------------------ Scene 0: Link back + Question
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())

        rec = make_receptor((3.1, 0.0, 0.0), height=3.2)
        rec_lbl = T("receptor", size=30, color=C_MR).next_to(rec, DOWN, buff=0.25)
        guard = boxed_label("guard enzyme", color=C_ENZ_ON, size=28)
        guard.move_to((-0.3, 0.78, 0.0))

        cort_p = ValueTracker(0.0)
        aldo_p = ValueTracker(0.0)

        def cort_pos():
            t = cort_p.get_value()
            if t < 0.5:
                u = t * 2.0
                return bez(
                    np.array([-4.5, 0.78, 0.0]),
                    np.array([-3.0, 0.16, 0.0]),
                    np.array([-1.6, 0.16, 0.0]),
                    np.array([-0.3, 0.16, 0.0]),
                    u,
                )
            u = (t - 0.5) * 2.0
            return np.array([-0.3 + 1.8 * u, 0.16 - 1.73 * (u ** 1.3), 0.0])

        cort_dot = always_redraw(lambda: Dot(
            cort_pos(),
            radius=0.18,
            color=C_CORT if cort_p.get_value() < 0.5 else GREY,
        ))
        cort_dot.set_z_index(-1)
        cort_lbl = T("cortisol", size=28, color=C_CORT).move_to((-4.5, 1.38, 0.0))

        def aldo_pos():
            t = aldo_p.get_value()
            return bez(
                np.array([-4.5, -0.88, 0.0]),
                np.array([-1.0, -1.08, 0.0]),
                np.array([1.2, -0.45, 0.0]),
                rec.socket_center,
                t,
            )

        aldo_dot = always_redraw(lambda: Dot(aldo_pos(), radius=0.18, color=C_ALDO))
        aldo_lbl = T("aldosterone", size=28, color=C_ALDO).move_to((-4.5, -1.48, 0.0))

        self.play(FadeIn(rec), FadeIn(rec_lbl), FadeIn(guard), run_time=0.6)
        self.add(cort_dot, aldo_dot)
        self.play(FadeIn(cort_lbl), FadeIn(aldo_lbl), run_time=0.4)
        self.play(cort_p.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.at("which steroid reaches it")
        self.play(aldo_p.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        self.play(rec.animate.set_fill(color=C_ALDO, opacity=0.38), run_time=0.4)

        # Pull left, shrink receptor to lower right, grow Steroid Tree
        self.at("Inside the adrenal gland")
        small_rec = make_receptor((4.85, -1.95, 0.0), height=1.35)
        small_rec_lbl = T("kidney receptor", size=24, color=C_MR).next_to(small_rec, DOWN, buff=0.18)
        self.play(
            FadeOut(guard),
            FadeOut(cort_dot),
            FadeOut(aldo_dot),
            FadeOut(cort_lbl),
            FadeOut(aldo_lbl),
            Transform(rec, small_rec),
            swap(rec_lbl, small_rec_lbl, run_time=0.8),
            run_time=1.0,
        )

        tree = SteroidTree(show_pituitary=False, seed=7)
        self.play(FadeIn(tree.cortex_bg), FadeIn(tree.trunk_line), FadeIn(tree.lbl_chol), run_time=0.6)
        self.play(
            FadeIn(tree.branch_lines),
            FadeIn(tree.gates),
            FadeIn(tree.lbl_aldo),
            FadeIn(tree.lbl_cort),
            FadeIn(tree.lbl_andr),
            run_time=0.9,
        )
        self.add(tree)

        self.at("Some newborns lack")
        red_gate = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_OFF, 1.0, closed=True)
        green_gate = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_ON, 1.0, closed=False)
        tree.cort_open.set_value(0.0)
        self.play(Transform(tree.gates[1], red_gate), run_time=0.35)
        self.play(Transform(tree.gates[1], green_gate), run_time=0.30)
        self.play(Transform(tree.gates[1], red_gate), run_time=0.35)

        self.at("one kind of hormone rises")
        self.play(tree.andr_boost.animate.set_value(1.90), run_time=1.1)

        self.at("How can losing")
        q = T("Lose an enzyme, gain a hormone?", size=36, color=TEXT).move_to([0.0, 3.15, 0.0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 1: Silent 2s Title
class S01Title(NarratedScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(cort_open=0.0, andr_boost=1.90, show_pituitary=False, seed=7)
        self.add(tree, rec, rec_lbl)
        q = T("Lose an enzyme, gain a hormone?", size=36, color=TEXT).move_to([0.0, 3.15, 0.0])
        self.add(q)

        title = T("One Missing Enzyme", size=44, font=TITLE_FONT, color=TEXT).move_to([0.0, 3.15, 0.0])
        green_gate = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_ON, 1.0, closed=False)
        self.play(
            swap(q, title, run_time=0.65),
            Transform(tree.gates[1], green_gate),
            tree.cort_open.animate.set_value(1.0),
            tree.andr_boost.animate.set_value(1.0),
            run_time=0.9,
        )
        self.wait(0.75)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


# ------------------------------------------------------------------ Scene 2: The Steroid Tree
class S02Tree(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(show_pituitary=False, seed=8)
        self.add(tree, rec, rec_lbl)

        self.at("one shared trunk")
        trunk_glow = Line(
            tree.spec["base"], tree.spec["fork"],
            stroke_color=TEXT, stroke_width=28, stroke_opacity=0.38,
        )
        self.play(FadeIn(trunk_glow), run_time=0.5)

        self.at("a CTH")
        pit_tree = SteroidTree(show_pituitary=True, seed=8)
        pit_box, pit_lbl = pit_tree.pit_box, pit_tree.pit_lbl
        acth_arrow = pit_tree.acth_curve
        acth_lbl = pit_tree.acth_lbl
        pulse_layer = VGroup(*[p[0] for p in pit_tree.acth_pulses])
        tree.acth_pulses = pit_tree.acth_pulses
        tree.acth_active.set_value(1.0)
        self.play(FadeOut(trunk_glow), FadeIn(pit_box), FadeIn(pit_lbl), run_time=0.6)
        self.play(Create(acth_arrow), FadeIn(acth_lbl), FadeIn(pulse_layer), tree.flow_speed.animate.set_value(1.50), run_time=0.9)

        self.at("Three branches")
        self.at("aldosterone")
        self.play(
            tree.branch_lines[0].animate.set_stroke(opacity=0.95, width=20),
            Indicate(tree.lbl_aldo, scale_factor=1.12, color=C_ALDO),
            run_time=0.7,
        )
        self.at("cortisol")
        self.play(
            tree.branch_lines[0].animate.set_stroke(opacity=0.42, width=16),
            tree.branch_lines[1].animate.set_stroke(opacity=0.95, width=20),
            Indicate(tree.lbl_cort, scale_factor=1.12, color=C_CORT),
            run_time=0.7,
        )
        self.at("androgens")
        self.play(
            tree.branch_lines[1].animate.set_stroke(opacity=0.42, width=16),
            tree.branch_lines[2].animate.set_stroke(opacity=0.95, width=20),
            Indicate(tree.lbl_andr, scale_factor=1.12, color=C_ANDR),
            run_time=0.7,
        )
        self.play(tree.branch_lines[2].animate.set_stroke(opacity=0.42, width=16), run_time=0.4)

        self.at("21")
        enz_lbl = T("21-\nhydroxylase", size=24, color=C_ENZ_ON, line_spacing=0.85).move_to([-3.47, 1.42, 0.0])
        l_left = Line(enz_lbl.get_bottom() + LEFT * 0.40 + DOWN * 0.16, tree.gate_pos[0] + UP * 0.28 + RIGHT * 0.04, color=C_ENZ_ON, stroke_width=2.5)
        l_right = Line(enz_lbl.get_bottom() + RIGHT * 0.20 + DOWN * 0.20, tree.gate_pos[1] + LEFT * 0.28 + UP * 0.06, color=C_ENZ_ON, stroke_width=2.5)
        self.play(
            FadeIn(enz_lbl),
            Create(l_left),
            Create(l_right),
            Indicate(tree.gates[0], scale_factor=1.25, color=C_ENZ_ON),
            Indicate(tree.gates[1], scale_factor=1.25, color=C_ENZ_ON),
            run_time=1.0,
        )

        self.at("The androgen branch")
        self.play(
            FadeOut(enz_lbl), FadeOut(l_left), FadeOut(l_right),
            tree.branch_lines[2].animate.set_stroke(opacity=0.95, width=20),
            run_time=0.8,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 3: The Three-Step Rule
class S03Rule(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(flow_speed=1.40, show_pituitary=True, seed=9)
        self.add(tree, rec, rec_lbl)

        strip = make_rule_strip(active=None)
        for pill in strip:
            pill.set_opacity(0.0)
        self.add(strip)

        # Step 1: route arrow cleanly between 'aldosterone' and 'cortisol' labels
        self.at("the enzymes")
        p1 = strip[0]
        pts1 = [np.array([-3.75, 2.82, 0.0]), np.array([-3.40, 1.65, 0.0]), tree.gate_pos[0] + UR * 0.26]
        arr1_line = VMobject(stroke_color=GOLD, stroke_width=3.0).set_points_as_corners(pts1)
        d1 = pts1[-1] - pts1[-2]
        arr1_tip = Triangle(fill_color=GOLD, fill_opacity=1.0, stroke_width=0).scale(0.11).rotate(np.arctan2(d1[1], d1[0]) - PI / 2).move_to(pts1[-1])
        arr1 = VGroup(arr1_line, arr1_tip)
        self.play(
            p1[0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            p1[1].animate.set_color(GOLD).set_opacity(1.0),
            Create(arr1),
            run_time=0.7,
        )

        self.at("lowers everything after it")
        ghost_gate = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_OFF, 1.0, closed=True)
        self.play(Transform(tree.gates[1], ghost_gate), tree.cort_open.animate.set_value(0.0), run_time=0.6)

        self.at("backs up what comes")
        self.play(tree.pile_level.animate.set_value(0.65), run_time=1.0)

        self.at("the receptors")
        green_gate = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_ON, 1.0, closed=False)
        p2 = strip[1]
        pts2 = [np.array([0.55, 2.82, 0.0]), np.array([2.65, 2.30, 0.0]), np.array([2.65, -1.80, 0.0]), np.array([4.05, -1.95, 0.0])]
        arr2_line = VMobject(stroke_color=GOLD, stroke_width=3.0).set_points_as_corners(pts2)
        arr2_tip = Triangle(fill_color=GOLD, fill_opacity=1.0, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to(pts2[-1])
        arr2 = VGroup(arr2_line, arr2_tip)
        self.play(
            Transform(tree.gates[1], green_gate),
            tree.cort_open.animate.set_value(1.0),
            tree.pile_level.animate.set_value(0.0),
            p1[0].animate.set_stroke(color=TEXT, width=2.0, opacity=0.55).set_fill(color=TEXT, opacity=0.07),
            p1[1].animate.set_color(TEXT).set_opacity(0.55),
            p2[0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            p2[1].animate.set_color(GOLD).set_opacity(1.0),
            FadeOut(arr1),
            Create(arr2),
            run_time=0.9,
        )

        self.at("only then")
        p3 = strip[2]
        arr3 = Arrow(
            [4.45, 2.82, 0.0],
            tree.pit_box.get_top() + UP * 0.06,
            color=GOLD, stroke_width=3.0, buff=0.05, max_tip_length_to_length_ratio=0.18,
        )
        self.play(
            p2[0].animate.set_stroke(color=TEXT, width=2.0, opacity=0.55).set_fill(color=TEXT, opacity=0.07),
            p2[1].animate.set_color(TEXT).set_opacity(0.55),
            p3[0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            p3[1].animate.set_color(GOLD).set_opacity(1.0),
            FadeOut(arr2),
            Create(arr3),
            run_time=0.7,
        )
        self.wait(0.4)
        self.play(
            FadeOut(arr3),
            p3[0].animate.set_stroke(color=TEXT, width=2.0, opacity=0.55).set_fill(color=TEXT, opacity=0.07),
            p3[1].animate.set_color(TEXT).set_opacity(0.55),
            run_time=0.5,
        )
        self.finish()


# ------------------------------------------------------------------ helper for pile labels (S04-S06)
def make_pile_annotations(tree):
    """Place 17-OH-progesterone & screening marker cleanly in the wide upper bay between Aldo and Cort."""
    pile_lbl = T("17-OH-\nprogesterone", size=24, color=C_PREC, line_spacing=0.85).move_to([-3.68, 1.09, 0.0])
    marker_lbl = T("screening\nmarker", size=24, color=TEXT, line_spacing=0.85).move_to([-3.48, 1.92, 0.0])
    ptr = Line(
        [-2.58, 0.68, 0.0],
        tree.pile_center + LEFT * 0.24,
        color=C_PREC,
        stroke_width=2.4,
    )
    return pile_lbl, marker_lbl, ptr


# ------------------------------------------------------------------ Scene 4: Step 1 (21-hydroxylase deficiency)
class S04StepOne(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(flow_speed=1.40, show_pituitary=True, seed=10)
        strip = make_rule_strip(active=None)
        self.add(tree, rec, rec_lbl, strip)

        title_lbl = T("21-hydroxylase deficiency", size=24, color=C_ENZ_OFF).move_to([-4.62, 2.66, 0.0])
        self.play(FadeIn(title_lbl), run_time=0.8)

        self.at("enzyme activity")
        red0 = make_gate(tree.gate_pos[0], tree.gate_tan[0], C_ENZ_OFF, 1.0, closed=True)
        red1 = make_gate(tree.gate_pos[1], tree.gate_tan[1], C_ENZ_OFF, 1.0, closed=True)
        self.play(
            Transform(tree.gates[0], red0),
            Transform(tree.gates[1], red1),
            run_time=0.9,
        )

        self.at("Step one")
        self.play(
            strip[0][0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            strip[0][1].animate.set_color(GOLD).set_opacity(1.0),
            run_time=0.5,
        )

        self.at("Cortisol and aldosterone")
        self.play(
            tree.aldo_open.animate.set_value(0.0),
            tree.cort_open.animate.set_value(0.0),
            tree.lbl_aldo.animate.set_opacity(0.45),
            tree.lbl_cort.animate.set_opacity(0.45),
            run_time=1.0,
        )

        self.at("17")
        pile_lbl, marker_lbl, ptr = make_pile_annotations(tree)
        self.play(
            tree.pile_level.animate.set_value(0.75),
            FadeIn(pile_lbl),
            Create(ptr),
            run_time=2.5,
        )

        self.at("piles up")
        self.play(tree.pile_level.animate.set_value(1.0), run_time=1.0)

        self.at("screening marker")
        self.play(FadeIn(marker_lbl), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 5: Step 2 (Receptor & salt loss)
class S05StepTwo(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(cort_open=0.0, aldo_open=0.0, pile_level=1.0, flow_speed=1.40, show_pituitary=True, seed=11)
        strip = make_rule_strip(active=1)
        title_lbl = T("21-hydroxylase deficiency", size=24, color=C_ENZ_OFF).move_to([-4.62, 2.66, 0.0])
        pile_lbl, marker_lbl, ptr = make_pile_annotations(tree)
        self.add(tree, rec, rec_lbl, strip, title_lbl, pile_lbl, ptr, marker_lbl)

        big_rec = make_receptor((4.45, -1.20, 0.0), height=2.25)
        big_rec_lbl = T("kidney receptor", size=26, color=C_MR).move_to([4.65, 0.24, 0.0])
        self.play(
            strip[0][0].animate.set_stroke(color=TEXT, width=2.0, opacity=0.55).set_fill(color=TEXT, opacity=0.07),
            strip[0][1].animate.set_color(TEXT).set_opacity(0.55),
            strip[1][0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            strip[1][1].animate.set_color(GOLD).set_opacity(1.0),
            Transform(rec, big_rec),
            swap(rec_lbl, big_rec_lbl, run_time=0.9),
            run_time=1.2,
        )

        # Place 'block before DOC' cleanly in open left-lower zone with short pointer to red gate
        self.at("before the precursor")
        doc_tag = T("block before DOC", size=24, color=TEXT).move_to([-4.65, -1.25, 0.0])
        doc_arr = Arrow(
            doc_tag.get_top() + UP * 0.04,
            tree.gate_pos[0] + DOWN * 0.26,
            color=TEXT, stroke_width=2.2, buff=0.05, max_tip_length_to_length_ratio=0.14,
        )
        self.play(
            Indicate(tree.gates[0], scale_factor=1.35, color=C_ENZ_OFF),
            FadeIn(doc_tag),
            Create(doc_arr),
            run_time=0.9,
        )

        self.at("progesterone")
        targets = [
            big_rec.socket_center + UP * 0.22 + LEFT * 0.08,
            big_rec.socket_center + DOWN * 0.18 + LEFT * 0.05,
            big_rec.socket_center + RIGHT * 0.12,
        ]
        blockers = VGroup()
        anims = []
        for idx, tgt in enumerate(targets):
            ring = Circle(radius=0.12, stroke_color=C_PREC, stroke_width=3.2, fill_opacity=0.0)
            ring.move_to(tree.pile_center + RIGHT * 0.15)
            blockers.add(ring)
            path = VMobject().set_points_as_corners([
                tree.pile_center + RIGHT * 0.15,
                np.array([0.8, -0.45 + 0.12 * idx, 0.0]),
                tgt,
            ])
            anims.append(MoveAlongPath(ring, path, run_time=2.8, rate_func=smooth))
        self.add(blockers)
        self.play(*anims)

        # Place 'weak blockers' cleanly left-below receptor, clear of ACTH curve and falling sodium
        self.at("weakly block")
        weak_lbl = T("weak blockers", size=26, color=C_PREC).move_to([2.65, -2.55, 0.0])
        for i, r in enumerate(blockers):
            bob(r, amp=0.03, speed=3.5, seed=i)
        self.play(FadeIn(weak_lbl), run_time=0.7)

        self.at("salt loss")
        rng = np.random.default_rng(5)
        na_dots = VGroup()
        for i in range(9):
            d = Dot(radius=0.085, color=C_NA)
            d.start_x = 5.45 + rng.uniform(-0.40, 0.40)
            d.phase = i / 9.0
            d.move_to([d.start_x, -1.85 - d.phase * 1.25, 0.0])

            def fall_na(m, dt):
                m.phase = (m.phase + dt * 0.65) % 1.0
                m.move_to([m.start_x, -1.85 - m.phase * 1.25, 0.0])
                m.set_fill(opacity=1.0 - 0.72 * m.phase)
            d.add_updater(fall_na)
            na_dots.add(d)
        na_lbl = T("sodium lost", size=26, color=C_NA).move_to([4.55, -3.40, 0.0])
        self.add(na_dots)
        self.play(FadeIn(na_lbl), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 6: Step 3 (Loops & hyperplasia)
class S06StepThree(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(
            cort_open=0.0, aldo_open=0.0, pile_level=1.0, flow_speed=1.40, show_pituitary=True, receptor_big=True, seed=12
        )
        strip = make_rule_strip(active=2)
        title_lbl = T("21-hydroxylase deficiency", size=24, color=C_ENZ_OFF).move_to([-4.62, 2.66, 0.0])
        pile_lbl, marker_lbl, ptr = make_pile_annotations(tree)
        doc_tag = T("block before DOC", size=24, color=TEXT).move_to([-4.65, -1.25, 0.0])
        doc_arr = Arrow(
            doc_tag.get_top() + UP * 0.04,
            tree.gate_pos[0] + DOWN * 0.26,
            color=TEXT, stroke_width=2.2, buff=0.05, max_tip_length_to_length_ratio=0.14,
        )
        weak_lbl = T("weak blockers", size=26, color=C_PREC).move_to([2.65, -2.55, 0.0])

        targets = [rec.socket_center + UP * 0.22, rec.socket_center + DOWN * 0.18, rec.socket_center + RIGHT * 0.12]
        blockers = VGroup(*[Circle(radius=0.12, stroke_color=C_PREC, stroke_width=3.2, fill_opacity=0.0).move_to(t) for t in targets])
        rng = np.random.default_rng(5)
        na_dots = VGroup()
        for i in range(9):
            d = Dot(radius=0.085, color=C_NA)
            d.start_x = 5.45 + rng.uniform(-0.40, 0.40)
            d.phase = i / 9.0
            d.move_to([d.start_x, -1.85 - d.phase * 1.25, 0.0])

            def fall_na(m, dt):
                m.phase = (m.phase + dt * 0.65) % 1.0
                m.move_to([m.start_x, -1.85 - m.phase * 1.25, 0.0])
                m.set_fill(opacity=1.0 - 0.72 * m.phase)
            d.add_updater(fall_na)
            na_dots.add(d)
        na_lbl = T("sodium lost", size=26, color=C_NA).move_to([4.55, -3.40, 0.0])
        self.add(tree, rec, rec_lbl, strip, title_lbl, pile_lbl, ptr, marker_lbl, doc_tag, doc_arr, weak_lbl, blockers, na_dots, na_lbl)

        # Step 3 brightens; receptor shrinks back; brake arrow appears
        small_rec = make_receptor((4.85, -1.95, 0.0), height=1.35)
        small_rec_lbl = T("kidney receptor", size=24, color=C_MR).next_to(small_rec, UP, buff=0.18)

        brake = make_brake_arrow(tree, width=3.5, opacity=1.0)
        brake_lbl = T("brake", size=24, color=C_CORT).move_to([2.45, 2.02, 0.0])

        self.play(
            strip[1][0].animate.set_stroke(color=TEXT, width=2.0, opacity=0.55).set_fill(color=TEXT, opacity=0.07),
            strip[1][1].animate.set_color(TEXT).set_opacity(0.55),
            strip[2][0].animate.set_stroke(color=GOLD, width=3.0, opacity=1.0).set_fill(color=GOLD, opacity=0.20),
            strip[2][1].animate.set_color(GOLD).set_opacity(1.0),
            FadeOut(doc_tag),
            FadeOut(doc_arr),
            FadeOut(weak_lbl),
            FadeOut(blockers),
            FadeOut(na_lbl),
            Transform(rec, small_rec),
            swap(rec_lbl, small_rec_lbl, run_time=0.8),
            Create(brake),
            FadeIn(brake_lbl),
            run_time=1.0,
        )

        # Low cortisol releases the brake -> dim stroke ONLY (keep fill_opacity=0!)
        self.at("releases the brake")
        self.play(
            brake[0].animate.set_stroke(opacity=0.22),
            brake[1].animate.set_fill(opacity=0.22),
            brake_lbl.animate.set_opacity(0.28),
            run_time=0.9,
        )

        # ACTH thickens & pulses, trunk accelerates
        self.at("drives the shared trunk")
        thick_acth = tree._make_acth_arrow(width=11.0)
        acth_up = T("ACTH up", size=26, color=C_ACTH).move_to(tree.acth_lbl).shift(DR * 0.14)
        self.play(
            Transform(tree.acth_curve, thick_acth),
            swap(tree.acth_lbl, acth_up, run_time=0.6),
            tree.flow_speed.animate.set_value(2.55),
            run_time=1.8,
        )
        tree.acth_lbl = acth_up
        pulse(tree.acth_curve[0], base=11.0, amp=3.8, speed=5.5)

        self.at("spills into")
        andr_up = T("androgens up", size=28, color=C_ANDR).move_to(tree.lbl_andr)
        self.play(
            tree.andr_boost.animate.set_value(2.1),
            swap(tree.lbl_andr, andr_up, run_time=0.7),
            run_time=3.6,
        )
        tree.lbl_andr = andr_up

        self.at("enlarges the gland")
        hyp_lbl = T("hyperplasia", size=26, color=TEXT).move_to([-4.35, -1.65, 0.0])
        self.play(tree.gland_width.animate.set_value(1.25), FadeIn(hyp_lbl), run_time=2.2)

        self.at("sodium is lost")
        vp_lbl = T("volume, pressure ↓", size=26, color=C_NA).move_to([4.55, -3.38, 0.0])
        self.play(FadeIn(vp_lbl), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ helper for two half-size trees (S07-S09)
def build_two_trees(pit_acth_thick=True, adenoma_on=True, andr_grey=1.0, left_tag="too much ACTH", right_tag="adrenal adenoma"):
    """Two well-separated half-size steroid trees with full-size readable labels."""
    left_tree = SteroidTree(
        fork=(-4.35, -1.35, 0.0), scale=0.48, label_size=24,
        show_pituitary=True, pit_label_size=24, seed=21, n_dots=28, n_pile=6,
    )
    right_tree = SteroidTree(
        fork=(2.35, -1.35, 0.0), scale=0.48, label_size=24,
        show_pituitary=True, pit_label_size=24, seed=22, n_dots=28, n_pile=6,
    )
    for tr in (left_tree, right_tree):
        tr.lbl_aldo.move_to(tr.spec["branches"][0][3] + UP * 0.44 + RIGHT * 0.10)
        tr.lbl_cort.move_to(tr.spec["branches"][1][3] + UP * 0.42)
        tr.lbl_andr.move_to(tr.spec["branches"][2][3] + UP * 0.44 + RIGHT * 0.22)
        tr.acth_lbl.shift(DOWN * 0.08 + LEFT * 0.10)
        tr.andr_grey.set_value(andr_grey)

    if pit_acth_thick:
        left_tree.acth_curve.become(left_tree._make_acth_arrow(width=9.0))
        left_tree.flow_speed.set_value(1.65)
    right_tree.flow_speed.set_value(1.0)
    if adenoma_on:
        right_tree.adenoma_on.set_value(1.0)

    ad_pos = bez(*right_tree.spec["branches"][1], 0.72)
    adenoma_lump = Circle(radius=0.20, stroke_color=C_CORT, stroke_width=3.0, fill_color=C_CORT, fill_opacity=0.68).move_to(ad_pos)
    ad_lbl_txt = T("adenoma", size=24, color=C_CORT).move_to([1.05, -1.62, 0.0])
    ad_ptr = Line(
        [1.62, -1.42, 0.0],
        ad_pos + np.array([-0.16, -0.16, 0.0]),
        color=C_CORT,
        stroke_width=2.4,
    )
    adenoma_lbl = VGroup(ad_lbl_txt, ad_ptr)

    div = DashedLine([0.0, -3.25, 0.0], [0.0, 2.55, 0.0], color=C_CHOL, stroke_width=2.0, dash_length=0.18).set_opacity(0.45)
    l_hdr = T(left_tag, size=28, color=C_ACTH).move_to([-3.3, 2.38, 0.0])
    r_hdr = T(right_tag, size=28, color=C_CORT).move_to([3.3, 2.38, 0.0])

    left_tree.lbl_cort.become(T("cortisol high", size=24, color=C_CORT).move_to(left_tree.lbl_cort))
    right_tree.lbl_cort.become(T("cortisol high", size=24, color=C_CORT).move_to(right_tree.lbl_cort))

    return left_tree, right_tree, adenoma_lump, adenoma_lbl, div, l_hdr, r_hdr


# ------------------------------------------------------------------ Scene 7: Predict
class S07Predict(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        left_tree, right_tree, ad_lump, ad_lbl, div, l_hdr, r_hdr = build_two_trees(
            pit_acth_thick=True, adenoma_on=True, andr_grey=0.0
        )
        left_tree.flow_speed.set_value(1.0)
        left_tree.acth_curve.become(left_tree._make_acth_arrow(width=5.0))
        right_tree.adenoma_on.set_value(0.0)
        ad_lump.set_opacity(0.0)
        ad_lbl.set_opacity(0.0)

        self.play(
            FadeIn(left_tree), FadeIn(right_tree), FadeIn(div),
            FadeIn(l_hdr), FadeIn(r_hdr),
            run_time=1.4,
        )

        self.at("In one")
        thick_l = left_tree._make_acth_arrow(width=9.5)
        self.play(
            Transform(left_tree.acth_curve, thick_l),
            left_tree.flow_speed.animate.set_value(1.65),
            Indicate(l_hdr, scale_factor=1.1, color=C_ACTH),
            Indicate(left_tree.lbl_cort, scale_factor=1.12, color=C_CORT),
            run_time=1.0,
        )
        pulse(left_tree.acth_curve[0], base=9.5, amp=2.5, speed=4.5)

        self.at("In the other")
        right_tree.adenoma_on.set_value(1.0)
        self.play(
            ad_lump.animate.set_opacity(1.0),
            ad_lbl.animate.set_opacity(1.0),
            Indicate(r_hdr, scale_factor=1.1, color=C_CORT),
            Indicate(right_tree.lbl_cort, scale_factor=1.12, color=C_CORT),
            run_time=1.0,
        )

        self.at("Which way")
        q1 = T("?", size=34, color=TEXT).move_to(left_tree.lbl_andr)
        q2 = T("?", size=34, color=TEXT).move_to(right_tree.lbl_andr)
        card = question_card("Androgens: up or down?", y=3.15, color=TEXT, size=34, max_w=11.0)
        self.play(
            left_tree.andr_grey.animate.set_value(1.0),
            right_tree.andr_grey.animate.set_value(1.0),
            swap(left_tree.lbl_andr, q1, run_time=0.6),
            swap(right_tree.lbl_andr, q2, run_time=0.6),
            FadeIn(card),
            run_time=1.1,
        )
        left_tree.lbl_andr = q1
        right_tree.lbl_andr = q2
        self.finish()


# ------------------------------------------------------------------ Scene 8: Silent 4.5s Predict Pause
class S08PredictPause(PredictPause):
    QUESTION = "Androgens: up or down?"
    CARD = {"y": 3.15, "color": TEXT, "size": 34, "max_w": 11.0}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        left_tree, right_tree, ad_lump, ad_lbl, div, l_hdr, r_hdr = build_two_trees(
            pit_acth_thick=True, adenoma_on=True, andr_grey=1.0
        )
        left_tree.flow_speed.set_value(1.3)
        right_tree.flow_speed.set_value(0.9)
        left_tree.lbl_andr.become(T("?", size=34, color=TEXT).move_to(left_tree.lbl_andr))
        right_tree.lbl_andr.become(T("?", size=34, color=TEXT).move_to(right_tree.lbl_andr))
        return VGroup(make_schematic_tag(), left_tree, right_tree, ad_lump, ad_lbl, div, l_hdr, r_hdr)


# ------------------------------------------------------------------ Scene 9: Answer
class S09Answer(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        left_tree, right_tree, ad_lump, ad_lbl, div, l_hdr, r_hdr = build_two_trees(
            pit_acth_thick=True, adenoma_on=True, andr_grey=1.0
        )
        q1 = T("?", size=34, color=TEXT).move_to(left_tree.lbl_andr)
        q2 = T("?", size=34, color=TEXT).move_to(right_tree.lbl_andr)
        left_tree.lbl_andr.become(q1)
        right_tree.lbl_andr.become(q2)
        card = question_card("Androgens: up or down?", y=3.15, color=TEXT, size=34, max_w=11.0)
        self.add(left_tree, right_tree, ad_lump, ad_lbl, div, l_hdr, r_hdr, card)
        pulse(left_tree.acth_curve[0], base=9.0, amp=3.0, speed=4.8)
        pulse(ad_lump, base=3.5, amp=2.5, speed=4.2)

        self.play(FadeOut(card), run_time=0.6)

        # Left tree: whole trunk driven, androgens rise
        self.at("whole trunk")
        andr_up = T("androgens up", size=24, color=C_ANDR).move_to(left_tree.lbl_andr).shift(RIGHT * 0.15)
        old_l = left_tree.lbl_andr
        self.play(
            left_tree.flow_speed.animate.set_value(2.35),
            left_tree.andr_grey.animate.set_value(0.0),
            left_tree.andr_boost.animate.set_value(2.15),
            swap(old_l, andr_up, run_time=0.7),
            run_time=2.8,
        )
        self.remove(old_l)
        left_tree.lbl_andr = andr_up

        # Right tree: adenoma cortisol suppresses ACTH (FadeOut/FadeIn dashed arrow cleanly!)
        self.at("suppresses")
        r_brake = make_brake_arrow(right_tree, width=3.2, opacity=1.0)
        dashed_acth = right_tree._make_acth_arrow(width=2.6, dashed=True, opacity=0.45)
        acth_down = T("ACTH down", size=24, color=GREY).move_to(right_tree.acth_lbl).shift(DOWN * 0.12)
        old_r_acth = right_tree.acth_curve
        old_r_lbl = right_tree.acth_lbl
        right_tree.acth_suppressed.set_value(1.0)
        self.play(
            Create(r_brake),
            FadeOut(old_r_acth, run_time=0.4),
            FadeIn(dashed_acth, run_time=0.6),
            swap(old_r_lbl, acth_down, run_time=0.6),
            right_tree.flow_speed.animate.set_value(0.32),
            run_time=2.4,
        )
        self.remove(old_r_acth, old_r_lbl)
        right_tree.acth_curve = dashed_acth
        right_tree.acth_lbl = acth_down

        # Androgen-making zone goes quiet
        self.at("goes quiet")
        andr_dn = T("androgens\ndown", size=24, color=GREY, line_spacing=0.85).move_to(right_tree.lbl_andr).shift(DOWN * 0.04 + RIGHT * 0.08)
        old_r_andr = right_tree.lbl_andr
        self.play(
            right_tree.andr_boost.animate.set_value(0.20),
            swap(old_r_andr, andr_dn, run_time=0.7),
            run_time=2.4,
        )
        self.remove(old_r_andr)
        right_tree.lbl_andr = andr_dn

        self.at("opposite directions")
        self.play(
            Indicate(left_tree.lbl_andr, scale_factor=1.22, color=C_ANDR),
            Indicate(right_tree.lbl_andr, scale_factor=1.18, color=GREY),
            run_time=2.2,
        )

        self.at("the loops")
        loop_lbl = T("the loop decides", size=32, color=GOLD).move_to([0.0, 3.15, 0.0])
        self.play(
            FadeIn(loop_lbl),
            Indicate(left_tree.acth_curve, scale_factor=1.08, color=GOLD),
            Indicate(right_tree.acth_curve, scale_factor=1.08, color=GOLD),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 10: Return
class S10Return(SpokenScene):
    def construct(self):
        self.add(make_schematic_tag())
        tree, rec, rec_lbl = build_carried_world(flow_speed=1.35, show_pituitary=True, seed=30)
        brake = make_brake_arrow(tree, width=3.2, opacity=1.0)
        brake_lbl = T("brake", size=24, color=C_CORT).move_to([2.45, 2.02, 0.0])

        self.play(FadeIn(tree), FadeIn(rec), FadeIn(rec_lbl), FadeIn(brake), FadeIn(brake_lbl), run_time=0.8)

        self.at("pathway breaks")
        self.play(
            Indicate(tree.gates[0], scale_factor=1.35, color=C_ENZ_ON),
            Indicate(tree.gates[1], scale_factor=1.35, color=C_ENZ_ON),
            run_time=1.2,
        )

        self.at("left behind")
        self.play(Indicate(rec, scale_factor=1.25, color=C_MR), run_time=1.2)

        self.at("feedback respond")
        self.play(
            Indicate(tree.acth_curve, scale_factor=1.06, color=C_ACTH),
            Indicate(brake, scale_factor=1.06, color=C_CORT),
            run_time=1.3,
        )

        self.at("direction")
        a0 = T("↑", size=30, color=C_ALDO).next_to(tree.lbl_aldo, LEFT, buff=0.10)
        a1 = T("↓", size=30, color=C_CORT).next_to(tree.lbl_cort, LEFT, buff=0.10)
        a2 = T("↑", size=30, color=C_ANDR).next_to(tree.lbl_andr, RIGHT, buff=0.10)
        b0 = T("↓", size=30, color=C_ALDO).next_to(tree.lbl_aldo, LEFT, buff=0.10)
        b1 = T("↑", size=30, color=C_CORT).next_to(tree.lbl_cort, LEFT, buff=0.10)
        b2 = T("↓", size=30, color=C_ANDR).next_to(tree.lbl_andr, RIGHT, buff=0.10)
        tag = T("direction, not size", size=28, color=TEXT).move_to([0.0, 3.20, 0.0])

        self.play(FadeIn(a0), FadeIn(a1), FadeIn(a2), FadeIn(tag), run_time=0.6)
        self.play(Transform(a0, b0), Transform(a1, b1), Transform(a2, b2), run_time=0.6)
        self.play(
            Transform(a0, T("↑", size=30, color=C_ALDO).next_to(tree.lbl_aldo, LEFT, buff=0.10)),
            Transform(a1, T("↓", size=30, color=C_CORT).next_to(tree.lbl_cort, LEFT, buff=0.10)),
            Transform(a2, T("↑", size=30, color=C_ANDR).next_to(tree.lbl_andr, RIGHT, buff=0.10)),
            run_time=0.6,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 11: Standard End Card
class S11End(EndCard):
    LINE = "Read adrenal disease in order: enzymes, then receptors, then loops."
