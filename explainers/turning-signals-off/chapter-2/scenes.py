"""
==============================================================================
"Where the Signal Runs Out" — Turning the Signal Off (Chapter 2)
==============================================================================

COLOUR MAP (one colour per concept for the entire film):
  YELLOW (#F5D547) : agonist and active receptor (and input stimulus pulses/bars)
  GREEN  (#83C167) : G protein (active G-alpha·GTP pool and blocks)
  GOLD   (#D4A843) : phosphate marks ("P" badges on receptor & targets, question/highlight)
  RED    (#FC6255) : arrestin (receptor blocker), closed valves, inhibitor stops, downstream block
  BLUE   (#58C4DD) : cyclic nucleotide (second messenger pool/tank, messenger-activated kinase)
  TEAL   (#3FB8C0) : removal machinery (RGS, PDE, phosphatase, exit outlets, adaptive brake, timers)
  GREY   (#8B93A1) : inactive states (GDP, 5'-AMP / 5'-GMP, inactive trays), axes, schematic tag
  TEXT   (#E8EAF0) : primary labels and target protein bodies

CARRIED PICTURE OF THE WORLD:
  A four-layer vertical signalling cascade filling the frame from membrane to target:
    1. Receptor at the membrane (top, y ≈ +2.48): yellow receptor + agonist, gold P marks, red arrestin cap
    2. G-protein pool (upper-mid, y ≈ +0.88): green active G-alpha blocks with IN / OUT arrows
    3. Second-messenger tank (lower-mid, y ≈ -0.76): blue cyclic nucleotide tank with synthesis IN / PDE OUT
    4. Phosphorylated target pool (bottom, y ≈ -2.42): target blocks carrying gold P badges & glow
  Zoomed scenes focus on one layer of this same world; synthesis scenes reassemble all four layers.

WHAT CHANGES ON SCREEN (and what it is computed from):
  s01_hook    : Arrestin blocks receptor at top while downstream green/blue/gold pools keep circulating
                and a question mark travels down the 3 active layers (seeded particle motion).
  s02_title   : Standard TitleCard ("Where the Signal Runs Out").
  s03_layers  : Active receptor feeds green G-alpha blocks into pool -> blue dots fill messenger tank
                -> blue kinase adds gold P badges to targets; IN/OUT arrows animate; pool levels follow ODEs.
  s03_overlap : Receptor gate closes at top; 3-layer cascade ODEs (k_G=0.72, k_M=0.38, k_P=0.19) drive
                the 3 pool levels and active particles to decay at visibly different rates.
  s04_rgs     : Zoomed G-alpha·GTP hydrolyzes slowly to GDP; teal RGS clamp closes and speeds hydrolysis,
                rapidly emptying the active green pool bar into distinct slots in the inactive tray.
  s05_pde     : Zoomed blue messenger tank receives 'cyclic messenger' blocks via synthesis; teal PDE
                drain relabels them '5′-AMP or 5′-GMP' and dims them; narrowing PDE raises tank + level bar.
  s06_predict : Synthesis valve closes ('production = 0'), teal inhibitor bar blocks PDE drain, tank
                sits nearly empty with 1 drifting messenger block under the predict question.
  s07_pause   : PredictPause (4.5 s) holding the question, closed valves, drifting block, and countdown ring.
  s08_reveal  : Same tank runs 3 computed ODE cases one by one (empty + no input -> flat; partly full +
                inhibited drain -> slower decay vs uninhibited reference; continuing input + inhibition -> rise).
  s09_targets : Target block carried forward; blue kinase adds gold P badges from left, teal phosphatase
                lifts them from right; balance meter tips toward removal and target glow/activity fades.
  s09_compare : Generic blue pool morphs between narrow vs wide teal outlet with identical inflow;
                side-by-side computed ODE curves trace high-level/long-tail vs lower-level/short-tail.
  s10_curve   : Two dimensionless computed curves from dX/dt = I - k*X (k=1 vs k=2, same I=1, switch off
                at t=6) on shared axis with no numbers plus synchronized pool bars, showing lower plateau,
                identical switch-off slope, and faster clearance.
  s11_adapt   : Carried TwoPanel comparing steady yellow input vs separated yellow pulses; computed adaptive
                brake B(t) trace and live teal brake meter climb steadily vs partially recover in pulse gaps;
                response gauges revealed after both patterns settle.
  s13_pulses  : Carried TwoPanel reveals computed response R(t) = stim*(1 - 0.82*B): repeated peaks under
                pulses, shrinking response under steady input; bottom GnRH gonadotrope strip animates active
                receptor vs downstream release block ('GnRH: main block appears downstream').
  s14_rule    : Full 4-layer world reassembled with receptor blocked and 3 teal timers sweeping at different
                computed speeds beside G-alpha, messenger, and target until the last downstream glow fades.
  s15_end     : Standard EndCard ("Each downstream layer fades when removal outruns production.").
==============================================================================
"""

from bp_parts import *  # noqa: F401,F403

# ------------------------------------------------------------------ Film-wide colour aliases
C_REC = YELLOW       # agonist and active receptor
C_G = GREEN          # G protein
C_P = GOLD           # phosphate marks
C_ARR = RED          # arrestin / stop / closed valve
C_MSG = BLUE         # cyclic nucleotide / second messenger
C_REM = TEAL         # removal machinery (RGS, PDE, phosphatase, brake, timers)
C_TGT = GOLD         # phosphorylated target marks
C_INACT = GREY       # inactive forms, axes, schematic tags

# Layer y-centres for the carried 4-tier cascade (inside y in [-3.5, 3.5])
Y_REC = 2.48
Y_G = 0.88
Y_MSG = -0.76
Y_TGT = -2.42
BOX_W = 5.0
BOX_H = 1.08


class BaseSpoken(SpokenScene):
    """SpokenScene without ambient background motes: all motion comes from the biological process."""

    def setup(self):
        NarratedScene.setup(self)


# ------------------------------------------------------------------ Shared geometry helpers
def arrow_between(p0, p1, color=TEXT, stroke=3.5, tip=0.16):
    """Straight arrow with clean tip, never passing inside boxes when endpoints have buff."""
    return Arrow(p0, p1, buff=0, color=color, stroke_width=stroke,
                 max_tip_length_to_length_ratio=0.35, tip_length=tip)


def p_badge(radius=0.22, color=C_P, label_color=BG):
    """Circular phosphate badge 'P' sized so font_size >= 22 with comfortable internal margin."""
    c = Circle(radius=radius, color=color, stroke_width=0, fill_color=color, fill_opacity=0.96)
    txt = T("P", size=22, color=label_color, weight=BOLD).move_to(c)
    return VGroup(c, txt)


def build_membrane_receptor(center=(0, Y_REC, 0), blocked=True, phosphorylated=True):
    """Build the membrane bar, yellow receptor, agonist dot, optional gold P marks and red arrestin cap."""
    cx, cy, _ = center
    mem = Line([cx - 2.4, cy + 0.24, 0], [cx + 2.4, cy + 0.24, 0], color=GREY, stroke_width=5)
    rec_pts = [
        [cx - 0.55, cy + 0.54, 0], [cx - 0.55, cy - 0.20, 0],
        [cx - 0.22, cy - 0.20, 0], [cx - 0.22, cy + 0.22, 0],
        [cx + 0.22, cy + 0.22, 0], [cx + 0.22, cy - 0.20, 0],
        [cx + 0.55, cy - 0.20, 0], [cx + 0.55, cy + 0.54, 0],
    ]
    rec = VMobject(stroke_color=C_REC, stroke_width=4, fill_color=C_REC, fill_opacity=0.22)
    rec.set_points_as_corners(rec_pts + [rec_pts[0]])
    agonist = Dot([cx, cy + 0.42, 0], radius=0.16, color=C_REC)
    tail = Line([cx + 0.55, cy - 0.14, 0], [cx + 2.15, cy - 0.14, 0], color=C_REC, stroke_width=4)

    g = VGroup(mem, rec, agonist, tail)
    g.receptor = rec
    g.agonist = agonist
    g.tail = tail

    if phosphorylated:
        marks = VGroup(*[p_badge(radius=0.21) for _ in range(3)])
        for i, m in enumerate(marks):
            m.move_to([cx + 1.00 + i * 0.48, cy - 0.46, 0])
        g.add(marks)
        g.marks = marks
    else:
        g.marks = VGroup()

    if blocked:
        arr = RoundedRectangle(corner_radius=0.14, width=1.40, height=0.48,
                               stroke_color=C_ARR, stroke_width=3, fill_color=C_ARR, fill_opacity=0.42)
        arr.move_to([cx, cy - 0.46, 0])
        arr_lbl = T("arrestin", size=22, color=TEXT, weight=BOLD).move_to(arr)
        g.add(arr, arr_lbl)
        g.arrestin = VGroup(arr, arr_lbl)
    else:
        g.arrestin = VGroup()
    return g


def build_pool_container(center, color, fill_frac=0.6, width=BOX_W, height=BOX_H):
    """A pool box with a bottom-anchored dynamic fill bar (fill_frac in 0..1)."""
    cx, cy, _ = center
    frame = RoundedRectangle(corner_radius=0.14, width=width, height=height,
                             stroke_color=color, stroke_width=2.8, fill_opacity=0.0)
    frame.move_to(center)
    fill_h = max(0.03, (height - 0.10) * np.clip(fill_frac, 0.0, 1.0))
    fill = Rectangle(width=width - 0.10, height=fill_h, stroke_width=0,
                     fill_color=color, fill_opacity=0.38)
    fill.move_to([cx, cy - height / 2 + 0.05 + fill_h / 2, 0])
    return VGroup(fill, frame), frame, fill


def make_g_block(pos=ORIGIN, active=True):
    """Green (or grey if inactive) G-alpha ON block with dark backing for high text contrast."""
    col = C_G if active else C_INACT
    lbl = T("G-alpha", size=22, color=TEXT if active else C_INACT, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.11, width=lbl.width + 0.28, height=lbl.height + 0.24,
                           stroke_color=col, stroke_width=2.5, fill_color=BG, fill_opacity=0.94)
    lbl.move_to(box)
    return VGroup(box, lbl).move_to(pos)


def make_target_block(pos=ORIGIN, n_p=2, glow_opacity=0.45):
    """Target protein block with n_p gold P badges inside the pool bounds above the glow border."""
    body = RoundedRectangle(corner_radius=0.10, width=1.42, height=0.46,
                            stroke_color=TEXT, stroke_width=2.2, fill_color=BG, fill_opacity=0.96).move_to(pos)
    glow = RoundedRectangle(corner_radius=0.15, width=1.56, height=0.58,
                            stroke_color=C_P, stroke_width=4.5, stroke_opacity=glow_opacity,
                            fill_color=C_P, fill_opacity=glow_opacity * 0.22).move_to(pos)
    lbl = T("target", size=22, color=TEXT).move_to(body)
    badges = VGroup()
    for i in range(n_p):
        b = p_badge(radius=0.20)
        b.move_to([pos[0] - 0.27 + i * 0.54, pos[1] + 0.50, 0])
        badges.add(b)
    return VGroup(glow, body, lbl, badges)


def build_cascade_world(rec_blocked=True, rec_p=True, g_frac=0.75, m_frac=0.75, t_frac=0.75,
                        show_in_out=False, seed=7):
    """Build the 4-layer cascade filling x in [-5.8, 4.8], y in [-3.0, 3.1]."""
    rng = np.random.default_rng(seed)
    rec = build_membrane_receptor([0, Y_REC, 0], blocked=rec_blocked, phosphorylated=rec_p)

    l_rec = T("receptor", size=28, color=C_REC).move_to([-4.2, Y_REC, 0])
    l_g = T("G-protein pool", size=28, color=C_G).move_to([-4.2, Y_G, 0])
    l_m = T("messenger tank", size=28, color=C_MSG).move_to([-4.2, Y_MSG, 0])
    l_t = T("target pool", size=28, color=C_TGT).move_to([-4.2, Y_TGT, 0])
    for lb in (l_rec, l_g, l_m, l_t):
        lb.align_to([-2.85, 0, 0], RIGHT)

    g_pool, g_frame, g_fill = build_pool_container([0, Y_G, 0], C_G, fill_frac=g_frac)
    m_pool, m_frame, m_fill = build_pool_container([0, Y_MSG, 0], C_MSG, fill_frac=m_frac)
    t_pool, t_frame, t_fill = build_pool_container([0, Y_TGT, 0], C_TGT, fill_frac=t_frac)

    # 3 non-overlapping G-alpha blocks inside BOX_W=5.0
    g_blocks = VGroup()
    for i in range(3):
        bx = -1.68 + i * 1.68
        by = Y_G + rng.uniform(-0.08, 0.08)
        g_blocks.add(make_g_block([bx, by, 0], active=True))

    m_dots = VGroup()
    for _ in range(16):
        dx = rng.uniform(-2.10, 2.10)
        dy = Y_MSG - BOX_H / 2 + 0.20 + rng.uniform(0.0, (BOX_H - 0.36) * max(0.30, m_frac))
        m_dots.add(Dot([dx, dy, 0], radius=0.095, color=C_MSG))

    t_blocks = VGroup()
    for i in range(2):
        tx = -1.20 + i * 2.40
        t_blocks.add(make_target_block([tx, Y_TGT - 0.21, 0], n_p=2, glow_opacity=0.45 * t_frac))

    a_rg_top = Y_REC - 0.74 if rec_blocked else Y_REC - 0.28
    a_rg = arrow_between([0, a_rg_top, 0], [0, Y_G + BOX_H / 2 + 0.08, 0],
                         color=C_INACT if rec_blocked else C_G, stroke=3.5)
    a_gm = arrow_between([0, Y_G - BOX_H / 2 - 0.08, 0],
                         [0, Y_MSG + BOX_H / 2 + 0.08, 0], color=C_MSG, stroke=3.5)
    a_mt = arrow_between([0, Y_MSG - BOX_H / 2 - 0.08, 0],
                         [0, Y_TGT + BOX_H / 2 + 0.08, 0], color=C_P, stroke=3.5)

    world = VGroup(rec, l_rec, l_g, l_m, l_t,
                   g_pool, m_pool, t_pool,
                   g_blocks, m_dots, t_blocks,
                   a_rg, a_gm, a_mt)
    world.rec = rec
    world.labels = VGroup(l_rec, l_g, l_m, l_t)
    world.pools = (g_pool, m_pool, t_pool)
    world.frames = (g_frame, m_frame, t_frame)
    world.fills = (g_fill, m_fill, t_fill)
    world.g_blocks = g_blocks
    world.m_dots = m_dots
    world.t_blocks = t_blocks
    world.arrows = (a_rg, a_gm, a_mt)
    world.in_out = VGroup()

    if show_in_out:
        io = VGroup()
        for arr_m, y_mid, col in ((a_rg, Y_G, C_G), (a_gm, Y_MSG, C_MSG), (a_mt, Y_TGT, C_P)):
            in_lbl = T("IN", size=22, color=col, weight=BOLD).move_to([0.42, arr_m.get_center()[1] - 0.10, 0])
            out_arr = arrow_between([BOX_W / 2 + 0.10, y_mid, 0], [BOX_W / 2 + 1.15, y_mid, 0], color=C_REM, stroke=3.5)
            out_lbl = T("OUT", size=22, color=C_REM, weight=BOLD).next_to(out_arr, UP, buff=0.08)
            io.add(in_lbl, out_arr, out_lbl)
        world.add(io)
        world.in_out = io

    return world


def attach_downstream_motion(world, g_rate=1.0, m_rate=1.0, t_rate=1.0, seed=11):
    """Attach bounded continuous motion to downstream active pools without any collisions."""
    rng = np.random.default_rng(seed)
    for idx, blk in enumerate(world.g_blocks):
        base = blk.get_center().copy()
        phase = idx * 2.1

        def u_g(m, dt, base=base, ph=phase):
            if not hasattr(m, "_t"):
                m._t = ph
            m._t += dt * 2.1 * g_rate
            if g_rate > 0.02:
                # Vertical-only drift keeps fixed horizontal separation between G-alpha blocks
                m.move_to(base + UP * 0.11 * np.sin(m._t))

        blk.add_updater(u_g)

    for idx, dot in enumerate(world.m_dots):
        base = dot.get_center().copy()
        ph = rng.uniform(0, TAU)
        spd = rng.uniform(1.5, 2.5)

        def u_m(m, dt, base=base, ph=ph, spd=spd):
            if not hasattr(m, "_t"):
                m._t = ph
            m._t += dt * spd * m_rate
            if m_rate > 0.02:
                m.move_to(base + RIGHT * 0.18 * np.cos(m._t) + UP * 0.10 * np.sin(1.4 * m._t))

        dot.add_updater(u_m)

    for idx, tblk in enumerate(world.t_blocks):
        base = tblk.get_center().copy()
        ph = idx * 1.7

        def u_t(m, dt, base=base, ph=ph):
            if not hasattr(m, "_t"):
                m._t = ph
            m._t += dt * 1.6 * t_rate
            if t_rate > 0.02:
                m.move_to(base + RIGHT * 0.10 * np.sin(m._t))

        tblk.add_updater(u_t)


# ------------------------------------------------------------------ ODE computations
def solve_cascade_decay(t_stop=3.5, t_max=17.0, k_g=0.72, k_m=0.38, k_p=0.19, dt=0.05):
    """Compute normalized 3-layer cascade pool levels when receptor input drops to 0 at t_stop."""
    ts = np.arange(0.0, t_max + dt, dt)
    g = np.ones_like(ts)
    m = np.ones_like(ts)
    p = np.ones_like(ts)
    for i in range(1, len(ts)):
        u = 1.0 if ts[i] < t_stop else 0.0
        dg = k_g * (u - g[i - 1])
        dm = k_m * (g[i - 1] - m[i - 1])
        dp = k_p * (m[i - 1] - p[i - 1])
        g[i] = max(0.0, g[i - 1] + dg * dt)
        m[i] = max(0.0, m[i - 1] + dm * dt)
        p[i] = max(0.0, p[i - 1] + dp * dt)
    return ts, g, m, p


def dimensionless_curve(t, k, t_off=6.0, inp=1.0):
    """Exact solution to dX/dt = I(t) - k*X, with I=inp on [0, t_off] and I=0 after."""
    if t <= t_off:
        return (inp / k) * (1.0 - np.exp(-k * t))
    x_off = (inp / k) * (1.0 - np.exp(-k * t_off))
    return x_off * np.exp(-k * (t - t_off))


def compute_adapt_traces(t_max=10.0, dt=0.02):
    """Compute steady vs pulsed input, adaptive brake B(t), and response R(t) = stim*(1 - 0.82*B)."""
    ts = np.arange(0.0, t_max + dt, dt)
    pulses = [(0.5, 1.5), (3.0, 4.0), (5.5, 6.5), (8.0, 9.0)]
    u_steady = np.array([1.0 if 0.5 <= t <= 9.5 else 0.0 for t in ts])
    u_pulse = np.array([1.0 if any(a <= t <= b for a, b in pulses) else 0.0 for t in ts])

    def sim(u):
        b = np.zeros_like(ts)
        for i in range(1, len(ts)):
            db = 0.52 * u[i - 1] * (1.0 - b[i - 1]) - 0.65 * (1.0 - u[i - 1]) * b[i - 1]
            b[i] = np.clip(b[i - 1] + db * dt, 0.0, 1.0)
        r = u * (1.0 - 0.82 * b)
        return b, r

    b_s, r_s = sim(u_steady)
    b_p, r_p = sim(u_pulse)
    return ts, u_steady, b_s, r_s, u_pulse, b_p, r_p


# ==============================================================================
# SCENE 1: HOOK
# ==============================================================================
class S01Hook(BaseSpoken):
    def construct(self):
        world = build_cascade_world(rec_blocked=True, rec_p=True, g_frac=0.75, m_frac=0.75, t_frac=0.75)
        attach_downstream_motion(world, seed=7)

        cross_pt = world.arrows[0].get_center()
        x_mark = VGroup(
            Line(cross_pt + UL * 0.14, cross_pt + DR * 0.14, color=C_ARR, stroke_width=5),
            Line(cross_pt + UR * 0.14, cross_pt + DL * 0.14, color=C_ARR, stroke_width=5),
        )
        blocked_lbl = T("new input reduced", size=24, color=C_ARR).move_to([3.9, Y_REC - 0.44, 0])

        self.add(world, x_mark, scope_tag("schematic"))

        self.at("cut new G protein")
        self.play(FadeIn(blocked_lbl, shift=LEFT * 0.1), run_time=0.45)

        self.at("a mark")
        if len(world.rec.marks):
            self.play(Indicate(world.rec.marks, color=C_P, scale_factor=1.2), run_time=0.5)

        self.at("its reader")
        if len(world.rec.arrestin):
            self.play(Indicate(world.rec.arrestin, color=C_ARR, scale_factor=1.1), run_time=0.55)

        self.at("What ends")
        q_badge = boxed_label("?", color=C_P, size=36, pad=0.18, stroke=3)
        q_badge.move_to([3.15, Y_G, 0])
        self.play(FadeIn(q_badge, scale=0.8), run_time=0.35)
        self.play(q_badge.animate.move_to([3.15, Y_MSG, 0]), run_time=0.85, rate_func=smooth)

        self.at("already downstream")
        self.play(q_badge.animate.move_to([3.15, Y_TGT, 0]), run_time=0.85, rate_func=smooth)
        self.finish()


# ==============================================================================
# SCENE 2: TITLE CARD
# ==============================================================================
class S02Title(TitleCard):
    LESSON = "Turning the Signal Off: Arrestins, RGS Proteins and Phosphodiesterases"
    TITLE = "Where the Signal Runs Out"


# ==============================================================================
# SCENE 3A: ACTIVE LAYERS
# ==============================================================================
class S03Layers(BaseSpoken):
    def construct(self):
        world = build_cascade_world(rec_blocked=False, rec_p=False, g_frac=0.18, m_frac=0.18, t_frac=0.18,
                                    show_in_out=False, seed=13)
        world.g_blocks.set_opacity(0)
        world.m_dots.set_opacity(0)
        world.t_blocks.set_opacity(0)
        self.add(world, scope_tag("schematic"))

        in_labels = VGroup()
        out_group = VGroup()
        for arr_m, y_mid, col in ((world.arrows[0], Y_G, C_G), (world.arrows[1], Y_MSG, C_MSG), (world.arrows[2], Y_TGT, C_P)):
            in_lb = T("IN", size=24, color=col, weight=BOLD).move_to([0.42, arr_m.get_center()[1], 0])
            out_a = arrow_between([BOX_W / 2 + 0.10, y_mid, 0], [BOX_W / 2 + 1.15, y_mid, 0], color=C_REM, stroke=4)
            out_lb = T("OUT", size=24, color=C_REM, weight=BOLD).next_to(out_a, UP, buff=0.08)
            in_labels.add(in_lb)
            out_group.add(out_a, out_lb)

        g_lvl = ValueTracker(0.18)
        m_lvl = ValueTracker(0.18)
        t_lvl = ValueTracker(0.18)

        def bind_fill(fill_rect, y_c, tr, col):
            def upd(mob):
                f = np.clip(tr.get_value(), 0.04, 1.0)
                h = (BOX_H - 0.10) * f
                r = Rectangle(width=BOX_W - 0.10, height=h, stroke_width=0, fill_color=col, fill_opacity=0.32)
                r.move_to([0, y_c - BOX_H / 2 + 0.05 + h / 2, 0])
                mob.become(r)
            fill_rect.add_updater(upd)

        bind_fill(world.fills[0], Y_G, g_lvl, C_G)
        bind_fill(world.fills[1], Y_MSG, m_lvl, C_MSG)
        bind_fill(world.fills[2], Y_TGT, t_lvl, C_TGT)

        self.at("an input")
        self.play(FadeIn(in_labels, shift=DOWN * 0.1), run_time=0.45)

        self.at("an exit")
        self.play(FadeIn(out_group, shift=RIGHT * 0.15), run_time=0.55)

        self.at("Receptors produce")
        # Animate the 3 g_blocks entering in their own lanes so they never overlap
        targets_g = [b.get_center().copy() for b in world.g_blocks]
        for b, pt in zip(world.g_blocks, targets_g):
            b.move_to([pt[0], Y_G + 0.24, 0]).set_opacity(0)
        self.play(
            *[b.animate.move_to(pt).set_opacity(1) for b, pt in zip(world.g_blocks, targets_g)],
            g_lvl.animate.set_value(0.76),
            run_time=1.35,
        )
        attach_downstream_motion(world, g_rate=1.0, m_rate=0.0, t_rate=0.0, seed=13)

        self.at("help produce second messenger")
        falling_dots = VGroup(*[Dot([(-0.45 + i * 0.45), Y_G - 0.65, 0], radius=0.095, color=C_MSG) for i in range(3)])
        self.play(FadeIn(falling_dots), run_time=0.2)
        self.play(
            falling_dots.animate.move_to([0, Y_MSG + 0.05, 0]),
            world.m_dots.animate.set_opacity(1),
            m_lvl.animate.set_value(0.76),
            run_time=1.25,
        )
        self.remove(falling_dots)
        attach_downstream_motion(world, g_rate=1.0, m_rate=1.0, t_rate=0.0, seed=13)

        self.at("Messenger activates")
        # Place kinase chip well to the right of the flying P badges
        kinase_chip = chip("kinase", color=C_MSG, size=22, pad=0.10).move_to([1.95, (Y_MSG + Y_TGT) / 2, 0])
        self.play(FadeIn(kinase_chip, scale=0.85), run_time=0.45)

        self.at("adds phosphate marks")
        p1 = p_badge(radius=0.20).move_to([0.95, (Y_MSG + Y_TGT) / 2, 0])
        p2 = p_badge(radius=0.20).move_to([-0.95, (Y_MSG + Y_TGT) / 2, 0])
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.2)
        self.play(
            p1.animate.move_to([0.94, Y_TGT + 0.36, 0]),
            p2.animate.move_to([-0.94, Y_TGT + 0.36, 0]),
            run_time=0.95,
        )
        self.remove(p1, p2)
        self.play(world.t_blocks.animate.set_opacity(1), t_lvl.animate.set_value(0.76), run_time=0.4)
        attach_downstream_motion(world, g_rate=1.0, m_rate=1.0, t_rate=1.0, seed=13)
        self.finish()


# ==============================================================================
# SCENE 3B: OVERLAPPING POOLS (COMPUTED 3-LAYER DECAY)
# ==============================================================================
class S03Overlap(BaseSpoken):
    def construct(self):
        world = build_cascade_world(rec_blocked=False, rec_p=True, g_frac=0.82, m_frac=0.82, t_frac=0.82,
                                    show_in_out=True, seed=21)
        attach_downstream_motion(world, seed=21)
        self.add(world, scope_tag("schematic"))

        t_sim = ValueTracker(0.0)
        ts, gs, ms, ps = solve_cascade_decay(t_stop=3.4, t_max=17.0, k_g=0.72, k_m=0.38, k_p=0.19)

        def interp(arr):
            return float(np.interp(t_sim.get_value(), ts, arr))

        for idx, (y_c, col, arr) in enumerate(((Y_G, C_G, gs), (Y_MSG, C_MSG, ms), (Y_TGT, C_TGT, ps))):
            fill_rect = world.fills[idx]

            def upd_f(mob, y_c=y_c, col=col, arr=arr):
                f = max(0.04, 0.82 * interp(arr))
                h = (BOX_H - 0.10) * f
                r = Rectangle(width=BOX_W - 0.10, height=h, stroke_width=0, fill_color=col, fill_opacity=0.32)
                r.move_to([0, y_c - BOX_H / 2 + 0.05 + h / 2, 0])
                mob.become(r)

            fill_rect.add_updater(upd_f)

        bar_labels = VGroup()
        for y_c, col, name, arr in ((Y_G, C_G, "G-alpha·GTP", gs), (Y_MSG, C_MSG, "messenger", ms), (Y_TGT, C_P, "target-P", ps)):
            track = Rectangle(width=1.75, height=0.32, stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=0.9)
            track.move_to([5.1, y_c - 0.25, 0])
            bar = always_redraw(lambda y_c=y_c, col=col, arr=arr, tr=track: Rectangle(
                width=max(0.04, 1.68 * interp(arr)), height=0.25, stroke_width=0, fill_color=col, fill_opacity=0.92
            ).move_to([tr.get_left()[0] + 0.035 + max(0.04, 1.68 * interp(arr)) / 2, tr.get_center()[1], 0]))
            nm = T(name, size=24, color=col).next_to(track, UP, buff=0.10).align_to(track, LEFT)
            bar_labels.add(track, bar, nm)
        self.add(bar_labels)

        gate = RoundedRectangle(corner_radius=0.10, width=1.30, height=0.30, stroke_color=C_ARR,
                                stroke_width=3, fill_color=C_ARR, fill_opacity=0.88).move_to([0, Y_REC - 0.35, 0])
        gate_lbl = T("gate closed", size=24, color=C_ARR, weight=BOLD).move_to([-1.65, Y_REC - 0.35, 0])

        t_sim.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t_sim)

        self.at("Stopping new receptor")
        self.play(FadeIn(gate, shift=DOWN * 0.12), FadeIn(gate_lbl),
                  world.arrows[0].animate.set_color(C_INACT).set_opacity(0.45), run_time=0.5)

        self.at("GTP")
        self.play(Indicate(world.g_blocks, color=C_G, scale_factor=1.06), run_time=0.5)

        self.at("messenger")
        self.play(Indicate(world.m_dots, color=C_MSG, scale_factor=1.08), run_time=0.5)

        self.at("target phosphate")
        self.play(Indicate(world.t_blocks, color=C_P, scale_factor=1.06), run_time=0.55)

        self.at("Each pool keeps")
        self.wait(max(0.1, self.t_of("settle the balance") - 0.35 - self.elapsed()))
        self.at("settle the balance")
        self.finish()


# ==============================================================================
# SCENE 4: RGS SPEEDS GTP HYDROLYSIS
# ==============================================================================
class S04Rgs(BaseSpoken):
    def construct(self):
        stage_title = T("G-alpha · GTP hydrolysis", size=30, color=C_G).move_to([-1.4, 3.12, 0])

        active_zone = RoundedRectangle(corner_radius=0.18, width=7.2, height=2.25,
                                       stroke_color=C_G, stroke_width=2.5, fill_color=C_G, fill_opacity=0.08).move_to([-1.6, 1.38, 0])
        active_lbl = T("active zone", size=24, color=C_G).next_to(active_zone, UP, buff=0.10).align_to(active_zone, LEFT)

        tray = RoundedRectangle(corner_radius=0.18, width=7.2, height=1.85,
                                stroke_color=C_INACT, stroke_width=2.5, fill_color=C_INACT, fill_opacity=0.08).move_to([-1.6, -1.78, 0])
        tray_lbl = T("inactive tray (GDP)", size=24, color=TEXT).next_to(tray, DOWN, buff=0.10).align_to(tray, LEFT)

        # Right panel: Active green pool bar
        pool_track = RoundedRectangle(corner_radius=0.10, width=1.25, height=4.4,
                                      stroke_color=C_G, stroke_width=2.5, fill_color=BG, fill_opacity=0.92).move_to([4.3, -0.15, 0])
        pool_lbl = T("active green\npool", size=24, color=C_G, line_spacing=0.85).next_to(pool_track, UP, buff=0.14)
        pool_val = ValueTracker(0.92)
        pool_bar = always_redraw(lambda: Rectangle(
            width=1.10, height=max(0.05, 4.24 * np.clip(pool_val.get_value(), 0.01, 1.0)),
            stroke_width=0, fill_color=C_G, fill_opacity=0.82
        ).move_to([4.3, pool_track.get_bottom()[1] + 0.08 + max(0.05, 4.24 * np.clip(pool_val.get_value(), 0.01, 1.0)) / 2, 0]))

        def zoomed_g(pos, gtp=True, active=True):
            col = C_G if active else C_INACT
            body = RoundedRectangle(corner_radius=0.16, width=3.1, height=1.10,
                                    stroke_color=col, stroke_width=3.5, fill_color=BG, fill_opacity=0.96)
            txt = T("G-alpha", size=30, color=TEXT if active else C_INACT, weight=BOLD).move_to(body.get_left() + RIGHT * 0.92)
            bcol = C_P if gtp else C_INACT
            badge = RoundedRectangle(corner_radius=0.12, width=1.08, height=0.62,
                                     stroke_color=bcol, stroke_width=2.5, fill_color=bcol,
                                     fill_opacity=0.95 if gtp else 0.25).move_to(body.get_right() + LEFT * 0.70)
            btxt = T("GTP" if gtp else "GDP", size=24, color=BG if gtp else TEXT, weight=BOLD).move_to(badge)
            return VGroup(body, txt, badge, btxt).move_to(pos)

        def tray_g_block(pos):
            """Native size >= 22 tray block sized by boxed_label so nothing overflows or overlaps."""
            return boxed_label("G-alpha · GDP", color=C_INACT, size=22, pad=0.14).move_to(pos)

        # Teal RGS U-clamp positioned OUTSIDE active block (around left/top/bottom of [-1.6, 1.38])
        rgs_u = VMobject(stroke_color=C_REM, stroke_width=10)
        rgs_u.set_points_as_corners([
            [-0.45, 2.08, 0], [-3.35, 2.08, 0], [-3.35, 0.68, 0], [-0.45, 0.68, 0]
        ])
        rgs_lbl = T("RGS", size=26, color=C_REM, weight=BOLD).next_to(rgs_u, LEFT, buff=0.18)
        rgs_clamp = VGroup(rgs_u, rgs_lbl)

        rx_track = Rectangle(width=5.0, height=0.24, stroke_color=C_REM, stroke_width=2, fill_color=BG, fill_opacity=0.9).move_to([-1.6, -0.22, 0])
        rx_p = ValueTracker(0.0)
        rx_bar = always_redraw(lambda: Rectangle(
            width=max(0.02, 4.94 * np.clip(rx_p.get_value(), 0.0, 1.0)), height=0.18,
            stroke_width=0, fill_color=C_REM, fill_opacity=0.92
        ).move_to([rx_track.get_left()[0] + 0.03 + max(0.02, 4.94 * np.clip(rx_p.get_value(), 0.0, 1.0)) / 2, rx_track.get_center()[1], 0]))
        rx_lbl = T("hydrolysis progress", size=22, color=TEXT).next_to(rx_track, DOWN, buff=0.10)

        tray_slots = [[-3.15, -1.36, 0], [-0.05, -1.36, 0], [-3.15, -2.18, 0], [-0.05, -2.18, 0]]

        g1 = zoomed_g([-1.6, 1.38, 0], gtp=True, active=True)
        self.add(stage_title, active_zone, active_lbl, tray, tray_lbl,
                 pool_track, pool_lbl, pool_bar, rx_track, rx_bar, rx_lbl, g1, scope_tag("timing: schematic"))

        self.at("hydrolyzes it")
        self.play(rx_p.animate.set_value(1.0), pool_val.animate.set_value(0.68), run_time=2.0, rate_func=linear)
        g1_gdp = zoomed_g([-1.6, 1.38, 0], gtp=False, active=False)
        self.play(Transform(g1, g1_gdp), run_time=0.32)
        t1 = tray_g_block(tray_slots[0])
        self.play(FadeOut(g1, shift=DOWN * 0.3), FadeIn(t1, shift=DOWN * 0.2), run_time=0.45)

        self.at("An RGS protein")
        rx_p.set_value(0.0)
        g2 = zoomed_g([-1.6, 1.38, 0], gtp=True, active=True)
        rgs_clamp.shift(LEFT * 0.9)
        self.play(FadeIn(g2, shift=DOWN * 0.15), FadeIn(rgs_clamp, shift=RIGHT * 0.2), run_time=0.45)

        self.at("speeds that reaction")
        self.play(rgs_clamp.animate.shift(RIGHT * 0.9), run_time=0.30)
        self.play(rx_p.animate.set_value(1.0), pool_val.animate.set_value(0.40), run_time=0.55, rate_func=linear)
        g2_gdp = zoomed_g([-1.6, 1.38, 0], gtp=False, active=False)
        self.play(Transform(g2, g2_gdp), rgs_clamp.animate.shift(LEFT * 0.9), run_time=0.25)
        t2 = tray_g_block(tray_slots[1])
        self.play(FadeOut(g2, shift=DOWN * 0.3), FadeIn(t2, shift=DOWN * 0.2), run_time=0.35)

        self.at("Faster hydrolysis")
        for idx, slot in enumerate(tray_slots[2:]):
            rx_p.set_value(0.0)
            gk = zoomed_g([-1.6, 1.38, 0], gtp=True, active=True)
            self.play(FadeIn(gk), rgs_clamp.animate.shift(RIGHT * 0.9), run_time=0.20)
            self.play(rx_p.animate.set_value(1.0),
                      pool_val.animate.set_value(0.18 if idx == 0 else 0.05),
                      run_time=0.45, rate_func=linear)
            gk_gdp = zoomed_g([-1.6, 1.38, 0], gtp=False, active=False)
            self.play(Transform(gk, gk_gdp), rgs_clamp.animate.shift(LEFT * 0.9), run_time=0.18)
            tk = tray_g_block(slot)
            self.play(FadeOut(gk, shift=DOWN * 0.25), FadeIn(tk, shift=DOWN * 0.2), run_time=0.25)

        self.at("active green pool")
        self.play(Indicate(pool_track, color=C_G), run_time=0.6)
        self.finish()


# ==============================================================================
# SCENE 5: PHOSPHODIESTERASE DRAINS CYCLIC NUCLEOTIDE
# ==============================================================================
def build_tank_stage(tank_center=(-0.6, -0.1, 0), tank_w=3.8, tank_h=3.1, init_fill=0.45):
    """Reusable zoomed blue messenger tank with vivid fluid level, meniscus, synthesis pipe, and PDE drain."""
    cx, cy, _ = tank_center
    tank = RoundedRectangle(corner_radius=0.18, width=tank_w, height=tank_h,
                            stroke_color=C_MSG, stroke_width=3.2, fill_opacity=0.0).move_to(tank_center)
    lvl = ValueTracker(init_fill)

    def mk_fill():
        f = np.clip(lvl.get_value(), 0.005, 0.97)
        h = max(0.04, (tank_h - 0.14) * f)
        y_bot = cy - tank_h / 2 + 0.07
        r = Rectangle(width=tank_w - 0.14, height=h, stroke_width=0, fill_color=C_MSG, fill_opacity=0.42)
        r.move_to([cx, y_bot + h / 2, 0])
        top_ln = Line([cx - tank_w / 2 + 0.10, y_bot + h, 0],
                      [cx + tank_w / 2 - 0.10, y_bot + h, 0], color=C_MSG, stroke_width=3.5)
        return VGroup(r, top_ln)

    fill = always_redraw(mk_fill)

    # Top-left synthesis pipe
    syn_y = cy + tank_h / 2 - 0.55
    syn_x0 = cx - tank_w / 2 - 2.2
    syn_x1 = cx - tank_w / 2 - 0.05
    syn_pipe = VGroup(
        Line([syn_x0, syn_y + 0.36, 0], [syn_x1, syn_y + 0.36, 0], color=C_MSG, stroke_width=3),
        Line([syn_x0, syn_y - 0.36, 0], [syn_x1, syn_y - 0.36, 0], color=C_MSG, stroke_width=3),
    )
    syn_lbl = T("synthesis", size=24, color=C_MSG).next_to(syn_pipe, UP, buff=0.16)
    syn_arr = arrow_between([syn_x0 + 0.15, syn_y, 0], [syn_x1 - 0.1, syn_y, 0], color=C_MSG, stroke=4.5)

    # Bottom-right PDE drain pipe
    pde_y = cy - tank_h / 2 + 0.55
    pde_x0 = cx + tank_w / 2 + 0.05
    pde_x1 = cx + tank_w / 2 + 2.2
    pde_pipe = VGroup(
        Line([pde_x0, pde_y + 0.36, 0], [pde_x1, pde_y + 0.36, 0], color=C_REM, stroke_width=3),
        Line([pde_x0, pde_y - 0.36, 0], [pde_x1, pde_y - 0.36, 0], color=C_REM, stroke_width=3),
    )
    pde_gate = RoundedRectangle(corner_radius=0.08, width=0.58, height=0.84,
                                stroke_color=C_REM, stroke_width=3, fill_color=C_REM, fill_opacity=0.28).move_to([(pde_x0 + pde_x1) / 2, pde_y, 0])
    pde_lbl = T("PDE drain", size=24, color=C_REM).next_to(pde_pipe, UP, buff=0.22)
    pde_arr = arrow_between([pde_x0 + 0.1, pde_y, 0], [pde_x1 - 0.1, pde_y, 0], color=C_REM, stroke=4.5)

    g = VGroup(fill, tank, syn_pipe, syn_lbl, syn_arr, pde_pipe, pde_gate, pde_lbl, pde_arr)
    g.tank = tank
    g.lvl = lvl
    g.fill = fill
    g.syn_arr = syn_arr
    g.syn_lbl = syn_lbl
    g.pde_gate = pde_gate
    g.pde_arr = pde_arr
    g.pde_lbl = pde_lbl
    g.syn_y = syn_y
    g.pde_y = pde_y
    g.syn_x0 = syn_x0
    g.pde_x0 = pde_x0
    g.pde_x1 = pde_x1
    return g


class S05Pde(BaseSpoken):
    def construct(self):
        stage = build_tank_stage(tank_center=[-0.8, -0.05, 0], tank_w=3.8, tank_h=3.1, init_fill=0.45)
        title = T("cyclic nucleotide pool", size=30, color=C_MSG).move_to([0, 3.08, 0])

        # Live level bar on far right
        lvl_tr = Rectangle(width=0.60, height=3.1, stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([5.2, -0.05, 0])
        lvl_bar = always_redraw(lambda: Rectangle(
            width=0.48, height=max(0.04, 2.98 * np.clip(stage.lvl.get_value(), 0.01, 0.98)),
            stroke_width=0, fill_color=C_MSG, fill_opacity=0.88
        ).move_to([5.2, lvl_tr.get_bottom()[1] + 0.06 + max(0.04, 2.98 * np.clip(stage.lvl.get_value(), 0.01, 0.98)) / 2, 0]))
        lvl_lbl = T("level", size=24, color=C_MSG).next_to(lvl_tr, UP, buff=0.14)

        # Circulating blue cyclic messenger dots inside the tank fluid
        rng = np.random.default_rng(19)
        fluid_dots = VGroup()
        for _ in range(10):
            dx = -0.8 + rng.uniform(-1.55, 1.55)
            dy = -1.35 + rng.uniform(0.0, 0.95)
            d = Dot([dx, dy, 0], radius=0.09, color=C_MSG).set_opacity(0.88)
            base = d.get_center().copy()
            ph = rng.uniform(0, TAU)
            d.add_updater(lambda m, dt, b=base, ph=ph: (setattr(m, "_t", getattr(m, "_t", ph) + dt * 2.2),
                                                        m.move_to(b + RIGHT * 0.18 * np.sin(m._t))))
            fluid_dots.add(d)

        self.add(title, stage, fluid_dots, lvl_tr, lvl_bar, lvl_lbl, scope_tag("schematic"))

        def cyclic_block(pos):
            lbl = T("cyclic messenger", size=22, color=C_MSG)
            box = RoundedRectangle(corner_radius=0.14, width=lbl.width + 0.32, height=lbl.height + 0.22,
                                   stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.96)
            return VGroup(box, lbl.move_to(box)).move_to(pos)

        def open_block(pos):
            lbl = T("5′-AMP or 5′-GMP", size=22, color=C_INACT)
            box = RoundedRectangle(corner_radius=0.14, width=lbl.width + 0.32, height=lbl.height + 0.22,
                                   stroke_color=C_INACT, stroke_width=2.0, fill_color=BG, fill_opacity=0.92)
            return VGroup(box, lbl.move_to(box)).move_to(pos)

        # Strictly non-overlapping path positions: above synthesis pipe -> inside tank center -> below PDE drain
        pos_syn_entry = [-3.8, stage.syn_y + 1.18, 0]
        pos_tank_mid = [-0.8, 0.30, 0]
        pos_pde_exit = [2.6, stage.pde_y - 1.00, 0]

        b_flow = cyclic_block(pos_syn_entry)
        self.add(b_flow)

        self.at("drains")
        self.play(b_flow.animate.move_to([-0.8, stage.syn_y + 1.18, 0]), run_time=0.8, rate_func=linear)
        self.play(b_flow.animate.move_to(pos_tank_mid), run_time=0.5, rate_func=linear)
        self.play(b_flow.animate.move_to(pos_pde_exit), run_time=0.55, rate_func=linear)

        self.at("opening the")
        b_open = open_block(pos_pde_exit)
        self.play(FadeOut(b_flow, run_time=0.2), FadeIn(b_open, run_time=0.25))
        self.play(b_open.animate.shift(RIGHT * 1.4).set_opacity(0.45), run_time=1.1)
        self.remove(b_open)

        self.at("When synthesis")
        bal_lbl = T("synthesis = breakdown (steady)", size=26, color=TEXT).move_to([-0.8, -2.55, 0])
        b_steady = cyclic_block(pos_syn_entry)
        self.play(FadeIn(bal_lbl), FadeIn(b_steady), run_time=0.35)
        self.play(b_steady.animate.move_to([-0.8, stage.syn_y + 1.18, 0]), run_time=0.7, rate_func=linear)
        self.play(b_steady.animate.move_to(pos_tank_mid), run_time=0.45, rate_func=linear)
        self.play(b_steady.animate.move_to(pos_pde_exit), run_time=0.5, rate_func=linear)
        b_open2 = open_block(pos_pde_exit)
        self.play(FadeOut(b_steady, run_time=0.2), FadeIn(b_open2, run_time=0.2))
        self.play(b_open2.animate.shift(RIGHT * 1.2).set_opacity(0.45), run_time=0.7)
        self.remove(b_open2)

        self.at("Slower breakdown")
        narrow_gate = RoundedRectangle(corner_radius=0.06, width=0.86, height=0.86,
                                       stroke_color=C_REM, stroke_width=3.5, fill_color=C_REM, fill_opacity=0.65).move_to(stage.pde_gate)
        new_lbl = T("slower breakdown -> higher pool", size=26, color=C_MSG).move_to([-0.8, -2.55, 0])
        b_rise = cyclic_block(pos_syn_entry)
        self.add(b_rise)
        self.play(b_rise.animate.move_to([-0.8, stage.syn_y + 1.18, 0]), run_time=0.7, rate_func=linear)
        self.play(Transform(stage.pde_gate, narrow_gate),
                  stage.pde_arr.animate.scale(0.55),
                  swap(bal_lbl, new_lbl, run_time=0.6),
                  b_rise.animate.move_to(pos_tank_mid),
                  stage.lvl.animate.set_value(0.88),
                  run_time=2.2, rate_func=smooth)
        self.finish()


# ==============================================================================
# SCENE 6: PREDICT — SHUT SYNTHESIS OFF, INHIBIT DRAIN
# ==============================================================================
def add_pulse(m, base=0.8, amp=0.2, speed=2.6, phase=0.0, stroke_only=False):
    """Gentle opacity breathing so a held beat is never a frozen frame."""
    def _u(o, dt):
        o._pt = getattr(o, "_pt", phase) + dt
        v = base + amp * np.sin(speed * o._pt)
        if stroke_only:
            o.set_stroke(opacity=v)
        else:
            o.set_opacity(v)
    m.add_updater(_u)
    return m


def build_predict_tank_backdrop():
    """Shared builder for s06_predict end frame and s07_pause backdrop."""
    stage = build_tank_stage(tank_center=[0, -0.35, 0], tank_w=4.0, tank_h=2.9, init_fill=0.07)
    valve = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.92,
                             stroke_color=C_ARR, stroke_width=3, fill_color=C_ARR, fill_opacity=0.92)
    valve.move_to([stage.syn_x0 + 1.0, stage.syn_y, 0])
    stage.syn_arr.set_opacity(0.0)
    prod_zero = T("production = 0", size=24, color=C_ARR, weight=BOLD).move_to([-4.2, stage.syn_y - 0.85, 0])

    inhib = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.94,
                             stroke_color=C_REM, stroke_width=3, fill_color=C_REM, fill_opacity=0.95)
    inhib.move_to(stage.pde_gate.get_center())
    inhib_lbl = T("PDE inhibited", size=24, color=C_REM, weight=BOLD).move_to([3.5, stage.pde_y - 0.85, 0])
    stage.pde_arr.set_opacity(0.18)

    lbl = T("cyclic messenger", size=22, color=C_MSG)
    bx = RoundedRectangle(corner_radius=0.14, width=lbl.width + 0.28, height=lbl.height + 0.18,
                          stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.96)
    last_blk = VGroup(bx, lbl.move_to(bx)).move_to([0, -1.15, 0])

    def drift(m, dt):
        if not hasattr(m, "_t"):
            m._t = 0.0
        m._t += dt
        m.move_to([0.65 * np.sin(1.2 * m._t), -1.15 + 0.08 * np.cos(0.9 * m._t), 0])

    last_blk.add_updater(drift)
    add_pulse(inhib, 0.8, 0.2, 3.0)
    add_pulse(valve, 0.8, 0.2, 3.0, 1.5)
    sc = scope_tag("schematic").move_to([-5.4, -3.25, 0])
    g = VGroup(stage, valve, prod_zero, inhib, inhib_lbl, last_blk, sc)
    return g, stage, valve, prod_zero, inhib, inhib_lbl, last_blk


class S06Predict(BaseSpoken):
    def construct(self):
        stage = build_tank_stage(tank_center=[0, -0.35, 0], tank_w=4.0, tank_h=2.9, init_fill=0.35)
        lbl = T("cyclic messenger", size=22, color=C_MSG)
        bx = RoundedRectangle(corner_radius=0.14, width=lbl.width + 0.28, height=lbl.height + 0.18,
                              stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.96)
        last_blk = VGroup(bx, lbl.move_to(bx)).move_to([0, -1.15, 0])

        def drift(m, dt):
            if not hasattr(m, "_t"):
                m._t = 0.0
            m._t += dt
            m.move_to([0.65 * np.sin(1.2 * m._t), -1.15 + 0.08 * np.cos(0.9 * m._t), 0])

        last_blk.add_updater(drift)
        sc = scope_tag("schematic").move_to([-5.4, -3.25, 0])
        self.add(stage, last_blk, sc)

        valve = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.92,
                                 stroke_color=C_ARR, stroke_width=3, fill_color=C_ARR, fill_opacity=0.92)
        valve.move_to([stage.syn_x0 + 1.0, stage.syn_y, 0])
        prod_zero = T("production = 0", size=24, color=C_ARR, weight=BOLD).move_to([-4.2, stage.syn_y - 0.85, 0])

        inhib = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.94,
                                 stroke_color=C_REM, stroke_width=3, fill_color=C_REM, fill_opacity=0.95)
        inhib.move_to(stage.pde_gate.get_center())
        inhib_lbl = T("PDE inhibited", size=24, color=C_REM, weight=BOLD).move_to([3.5, stage.pde_y - 0.85, 0])

        self.at("shut messenger synthesis off")
        self.play(FadeIn(valve, shift=DOWN * 0.25), stage.syn_arr.animate.set_opacity(0.0),
                  FadeIn(prod_zero), stage.lvl.animate.set_value(0.07), run_time=1.35)

        self.at("inhibit the drain")
        self.play(FadeIn(inhib, shift=DOWN * 0.25), stage.pde_arr.animate.set_opacity(0.18),
                  FadeIn(inhib_lbl), run_time=1.05)

        self.at("Can protecting")
        q = question_card("Can protecting the remaining messenger create a new signal?", y=3.05, max_w=11.6)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.6)
        add_pulse(inhib, 0.8, 0.2, 3.0)
        add_pulse(valve, 0.8, 0.2, 3.0, 1.5)
        self.finish()


# ==============================================================================
# SCENE 7: PREDICT PAUSE (4.5 s)
# ==============================================================================
class S07Pause(PredictPause):
    QUESTION = "Can protecting the remaining messenger create a new signal?"
    CARD = {"y": 3.05, "max_w": 11.6}
    SECONDS = 4.5

    def backdrop(self):
        g, *_ = build_predict_tank_backdrop()
        return g


# ==============================================================================
# SCENE 8: REVEAL — THREE CASES IN THE SAME TANK
# ==============================================================================
class S08Reveal(BaseSpoken):
    def construct(self):
        stage = build_tank_stage(tank_center=[-0.5, -0.35, 0], tank_w=4.0, tank_h=2.9, init_fill=0.06)
        valve = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.92,
                                 stroke_color=C_ARR, stroke_width=3, fill_color=C_ARR, fill_opacity=0.92)
        valve.move_to([stage.syn_x0 + 1.0, stage.syn_y, 0])
        stage.syn_arr.set_opacity(0.0)
        prod_lbl = T("input = 0", size=24, color=C_ARR, weight=BOLD).move_to([-4.6, stage.syn_y - 0.85, 0])

        inhib = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.94,
                                 stroke_color=C_REM, stroke_width=3, fill_color=C_REM, fill_opacity=0.95)
        inhib.move_to(stage.pde_gate.get_center())
        stage.pde_arr.set_opacity(0.18)

        meter_tr = Rectangle(width=0.60, height=2.9, stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([5.2, -0.35, 0])
        meter_fill = always_redraw(lambda: Rectangle(
            width=0.48, height=max(0.04, 2.78 * np.clip(stage.lvl.get_value(), 0.005, 0.98)),
            stroke_width=0, fill_color=C_MSG, fill_opacity=0.88
        ).move_to([5.2, meter_tr.get_bottom()[1] + 0.06 + max(0.04, 2.78 * np.clip(stage.lvl.get_value(), 0.005, 0.98)) / 2, 0]))
        meter_lbl = T("level", size=24, color=C_MSG).next_to(meter_tr, UP, buff=0.14)

        self.add(stage, valve, prod_lbl, inhib, meter_tr, meter_fill, meter_lbl, scope_tag("levels: schematic"))

        no_head = T("No. No new messenger is made.", size=34, color=C_ARR, weight=BOLD).move_to([0, 3.08, 0])
        self.play(FadeIn(no_head, scale=0.92), run_time=0.45)

        self.at("No new messenger")
        case1 = T("Case 1: no input, empty pool", size=28, color=TEXT).move_to([0, 2.25, 0])
        res1 = T("stays near zero", size=26, color=C_MSG).move_to([-0.5, -2.55, 0])
        self.play(FadeIn(case1), run_time=0.4)

        self.at("An empty pool")
        self.play(FadeIn(res1), stage.lvl.animate.set_value(0.03), run_time=1.8, rate_func=linear)

        self.at("Messenger already present")
        case2 = T("Case 2: no input, partly full pool", size=28, color=TEXT).move_to([0, 2.25, 0])
        res2 = T("protected -> slower decay", size=26, color=C_REM).move_to([-0.5, -2.55, 0])
        ref_line = DashedLine([stage.tank.get_left()[0] + 0.14, stage.tank.get_bottom()[1] + 0.56, 0],
                              [stage.tank.get_right()[0] - 0.14, stage.tank.get_bottom()[1] + 0.56, 0],
                              color=TEXT, stroke_width=2.5)
        ref_lbl = T("uninhibited decay", size=22, color=TEXT).next_to(ref_line, DOWN, buff=0.14)
        self.play(FadeOut(case1), FadeOut(res1), stage.lvl.animate.set_value(0.68), run_time=0.4)
        self.play(FadeIn(case2), FadeIn(ref_line), FadeIn(ref_lbl), run_time=0.45)
        self.play(FadeIn(res2), stage.lvl.animate.set_value(0.45), run_time=2.6, rate_func=linear)

        self.at("With continuing input")
        case3 = T("Case 3: continuing input + PDE inhibited", size=28, color=TEXT).move_to([0, 2.25, 0])
        res3 = T("level rises and lasts longer", size=26, color=C_MSG).move_to([-0.5, -2.55, 0])
        prod_on = T("input > 0", size=24, color=C_MSG, weight=BOLD).move_to(prod_lbl)
        self.play(FadeOut(case2), FadeOut(res2), FadeOut(ref_line), FadeOut(ref_lbl),
                  FadeOut(valve), stage.syn_arr.animate.set_opacity(1.0),
                  Transform(prod_lbl, prod_on), stage.lvl.animate.set_value(0.38), run_time=0.5)
        self.play(FadeIn(case3), FadeIn(res3), stage.lvl.animate.set_value(0.88), run_time=2.8, rate_func=smooth)
        self.finish()


# ==============================================================================
# SCENE 9A: PHOSPHORYLATED TARGETS & KINASE / PHOSPHATASE BALANCE
# ==============================================================================
class S09Targets(BaseSpoken):
    def construct(self):
        title = T("phosphorylated target pool", size=30, color=C_P).move_to([0, 3.08, 0])

        n_badges = ValueTracker(3.0)
        glow_tr = ValueTracker(0.75)

        target_body = RoundedRectangle(corner_radius=0.16, width=3.0, height=1.25,
                                       stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.96).move_to([0, 0.35, 0])
        target_lbl = T("target protein", size=26, color=TEXT, weight=BOLD).move_to(target_body)
        target_glow = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.22, width=3.34, height=1.58,
            stroke_color=C_P, stroke_width=8, stroke_opacity=np.clip(glow_tr.get_value(), 0.02, 0.92),
            fill_color=C_P, fill_opacity=0.24 * np.clip(glow_tr.get_value(), 0.0, 1.0)
        ).move_to([0, 0.35, 0]))

        # Fixed 5 slots strictly ABOVE target_glow top (0.35 + 0.79 = 1.14) -> y = 1.48!
        slots_pos = [[-1.08 + i * 0.54, 1.48, 0] for i in range(5)]
        badges = always_redraw(lambda: VGroup(*[
            p_badge(radius=0.20).move_to(slots_pos[i])
            for i in range(int(round(np.clip(n_badges.get_value(), 0, 5))))
        ]))

        kinase = boxed_label("kinase", color=C_MSG, size=28, pad=0.24).move_to([-4.6, 0.35, 0])
        k_arr = arrow_between([kinase.get_right()[0] + 0.10, 0.35, 0],
                              [target_body.get_left()[0] - 0.22, 0.35, 0], color=C_MSG, stroke=4.5)
        k_add_lbl = T("+ P", size=24, color=C_P, weight=BOLD).next_to(k_arr, UP, buff=0.14)

        phos = boxed_label("phosphatase", color=C_REM, size=28, pad=0.24).move_to([4.6, 0.35, 0])
        p_arr = arrow_between([target_body.get_right()[0] + 0.22, 0.35, 0],
                              [phos.get_left()[0] - 0.10, 0.35, 0], color=C_REM, stroke=4.5)
        p_rem_lbl = T("− P", size=24, color=C_REM, weight=BOLD).next_to(p_arr, UP, buff=0.14)

        bal_tr = ValueTracker(-0.25)
        fulcrum = Polygon([-0.22, -2.28, 0], [0.22, -2.28, 0], [0, -1.88, 0],
                          color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.7)
        beam = always_redraw(lambda: Line(
            [-1.9 * np.cos(-0.26 * bal_tr.get_value()), -1.88 - 1.9 * np.sin(-0.26 * bal_tr.get_value()), 0],
            [1.9 * np.cos(-0.26 * bal_tr.get_value()), -1.88 + 1.9 * np.sin(-0.26 * bal_tr.get_value()), 0],
            color=TEXT, stroke_width=5
        ))
        b_left_lbl = T("addition", size=24, color=C_MSG).move_to([-2.4, -2.48, 0])
        b_right_lbl = T("removal", size=24, color=C_REM).move_to([2.4, -2.48, 0])

        act_lbl = T("target activity", size=24, color=C_P).move_to([-4.6, -1.55, 0])
        act_tr = Rectangle(width=2.2, height=0.30, stroke_color=C_P, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).next_to(act_lbl, DOWN, buff=0.12)
        act_fill = always_redraw(lambda: Rectangle(
            width=max(0.03, 2.12 * np.clip(glow_tr.get_value(), 0.01, 1.0)), height=0.23,
            stroke_width=0, fill_color=C_P, fill_opacity=0.92
        ).move_to([act_tr.get_left()[0] + 0.04 + max(0.03, 2.12 * np.clip(glow_tr.get_value(), 0.01, 1.0)) / 2, act_tr.get_center()[1], 0]))

        self.add(title, target_glow, target_body, target_lbl, badges,
                 fulcrum, beam, b_left_lbl, b_right_lbl, act_lbl, act_tr, act_fill, scope_tag("schematic"))

        self.at("A kinase")
        self.play(FadeIn(kinase, shift=RIGHT * 0.15), GrowArrow(k_arr), FadeIn(k_add_lbl), run_time=0.55)
        fly_p = p_badge(radius=0.20).move_to([-3.2, 1.48, 0])
        self.play(FadeIn(fly_p), run_time=0.15)
        self.play(fly_p.animate.move_to(slots_pos[3]),
                  glow_tr.animate.set_value(0.95), bal_tr.animate.set_value(-0.55), run_time=0.9)
        self.remove(fly_p)
        n_badges.set_value(4)

        self.at("A protein phosphatase")
        self.play(FadeIn(phos, shift=LEFT * 0.15), GrowArrow(p_arr), FadeIn(p_rem_lbl), run_time=0.55)
        lift_p = p_badge(radius=0.20).move_to(slots_pos[3])
        n_badges.set_value(3)
        self.play(lift_p.animate.move_to([3.2, 1.48, 0]), run_time=0.8)
        self.play(FadeOut(lift_p), run_time=0.2)

        self.at("The phosphorylated pool fades")
        self.play(k_arr.animate.set_opacity(0.35), kinase.box.animate.set_stroke(opacity=0.4),
                  bal_tr.animate.set_value(0.85), run_time=1.0)
        for target_n, g_v in ((2, 0.65), (1, 0.40), (0, 0.25)):
            fly_out = p_badge(radius=0.20).move_to(slots_pos[target_n])
            n_badges.set_value(target_n)
            self.play(fly_out.animate.move_to([3.2, 1.48, 0]).set_opacity(0.0),
                      glow_tr.animate.set_value(g_v),
                      run_time=1.45, rate_func=linear)
            self.remove(fly_out)

        self.at("that phosphate activates")
        # Target glow and activity bar fade out together as the narrator says "its activity fades too"
        self.play(glow_tr.animate.set_value(0.01), run_time=2.8, rate_func=smooth)
        self.finish()


# ==============================================================================
# SCENE 9B: NARROW VS WIDE EXIT (POOL + COMPUTED CURVE)
# ==============================================================================
class S09Compare(BaseSpoken):
    def construct(self):
        tank_cx, tank_cy = -3.8, -0.15
        tank = RoundedRectangle(corner_radius=0.18, width=3.2, height=3.2,
                                stroke_color=C_MSG, stroke_width=3.2, fill_color=BG, fill_opacity=0.92).move_to([tank_cx, tank_cy, 0])
        lvl_tr = ValueTracker(0.0)

        def mk_fill():
            f = np.clip(lvl_tr.get_value(), 0.005, 0.96)
            h = max(0.04, 3.06 * f)
            y_bot = tank_cy - 1.6 + 0.07
            r = Rectangle(width=3.06, height=h, stroke_width=0, fill_color=C_MSG, fill_opacity=0.45)
            r.move_to([tank_cx, y_bot + h / 2, 0])
            top_ln = Line([tank_cx - 1.50, y_bot + h, 0], [tank_cx + 1.50, y_bot + h, 0], color=C_MSG, stroke_width=3.5)
            return VGroup(r, top_ln)

        fill = always_redraw(mk_fill)

        in_arr = arrow_between([tank_cx, tank_cy + 2.35, 0], [tank_cx, tank_cy + 1.68, 0], color=C_MSG, stroke=5)
        in_lbl = T("same inflow", size=24, color=C_MSG).next_to(in_arr, UP, buff=0.10)

        out_w = ValueTracker(0.26)
        out_pipe = always_redraw(lambda: Rectangle(
            width=out_w.get_value(), height=0.72,
            stroke_color=C_REM, stroke_width=2.8, fill_color=C_REM, fill_opacity=0.40
        ).move_to([tank_cx, tank_cy - 1.98, 0]))
        case_lbl = T("narrow exit", size=28, color=C_REM).move_to([tank_cx, -2.85, 0])

        P = Plot(box=(0.2, 5.8, -2.0, 2.2), xr=(0, 11.0), yr=(0, 1.15),
                 xticks=(), yticks=(), xlabel="time", ylabel="active pool", color=TEXT, size=24, label_size=26)
        v_off = P.vline(6.0, "input stops", color=GREY, size=22)

        t_tr = ValueTracker(0.0)
        fn_narrow = lambda t: dimensionless_curve(t, k=1.0, t_off=6.0, inp=1.0)
        fn_wide = lambda t: dimensionless_curve(t, k=2.2, t_off=6.0, inp=1.0)

        live_n = P.live_curve(fn_narrow, t_tr, color=C_MSG, width=6)
        dot_n = P.dot(lambda: t_tr.get_value(), lambda: fn_narrow(t_tr.get_value()), color=C_MSG, ring=TEXT)

        self.add(tank, fill, in_arr, in_lbl, out_pipe, P, v_off, scope_tag("schematic"))

        self.at("A narrow exit")
        self.play(FadeIn(case_lbl), run_time=0.3)
        self.add(live_n, dot_n)
        lvl_tr.add_updater(lambda m: m.set_value(0.85 * fn_narrow(t_tr.get_value())))
        self.add(lvl_tr)
        self.play(t_tr.animate.set_value(11.0), run_time=3.4, rate_func=linear)
        lvl_tr.clear_updaters()

        static_n = P.curve(fn_narrow, color=C_MSG, width=4, opacity=0.60)
        n_tag = T("narrow exit", size=24, color=C_MSG).move_to(P.pt(3.8, 1.07))
        self.remove(live_n, dot_n)
        self.add(static_n, n_tag)

        self.at("A wide exit")
        t_tr2 = ValueTracker(0.0)
        wide_lbl = T("wide exit", size=28, color=C_REM).move_to([tank_cx, -2.85, 0])
        self.play(out_w.animate.set_value(1.25), lvl_tr.animate.set_value(0.0),
                  swap(case_lbl, wide_lbl, run_time=0.5), run_time=0.55)

        live_w = P.live_curve(fn_wide, t_tr2, color=C_REM, width=6)
        dot_w = P.dot(lambda: t_tr2.get_value(), lambda: fn_wide(t_tr2.get_value()), color=C_REM, ring=TEXT)
        self.add(live_w, dot_w)
        lvl_tr.add_updater(lambda m: m.set_value(0.85 * fn_wide(t_tr2.get_value())))
        self.play(t_tr2.animate.set_value(11.0), run_time=3.8, rate_func=linear)
        lvl_tr.clear_updaters()

        w_tag = T("wide exit", size=24, color=C_REM).move_to(P.pt(3.5, 0.54))
        self.play(FadeIn(w_tag), run_time=0.35)
        self.finish()


# ==============================================================================
# SCENE 10: COMPUTED DIMENSIONLESS CURVES (dX/dt = I - k*X)
# ==============================================================================
class S10Curve(BaseSpoken):
    def construct(self):
        # Plot on left/center (x in [-5.4, 3.6]), synchronized live pool gauges on right (x = 4.5, 5.5)
        P = Plot(box=(-5.4, 3.6, -2.2, 2.05), xr=(0, 11.0), yr=(0, 1.15),
                 xticks=(), yticks=(), xlabel="time", ylabel="active pool", color=TEXT, size=24, label_size=28)
        eq = M("dX/dt = input - k * X", size=28, color=TEXT).move_to([3.3, 3.08, 0])
        v_off = P.vline(6.0, "input off", color=TEXT, size=24)
        thresh = P.hline(0.06, "small threshold", color=GREY, size=22, dashed=True)
        thresh[1].shift(UP * 0.10)

        fn_slow = lambda t: dimensionless_curve(t, k=1.0, t_off=6.0, inp=1.0)
        fn_fast = lambda t: dimensionless_curve(t, k=2.0, t_off=6.0, inp=1.0)

        t1 = ValueTracker(0.0)
        t2 = ValueTracker(0.0)
        live1 = P.live_curve(fn_slow, t1, color=C_MSG, width=6)
        dot1 = P.dot(lambda: t1.get_value(), lambda: fn_slow(t1.get_value()), color=C_MSG, ring=TEXT)
        live2 = P.live_curve(fn_fast, t2, color=C_REM, width=6)
        dot2 = P.dot(lambda: t2.get_value(), lambda: fn_fast(t2.get_value()), color=C_REM, ring=TEXT)

        # Two live pool level gauges driven directly by the same ODE values
        g1_tr = Rectangle(width=0.65, height=3.8, stroke_color=C_MSG, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([4.5, -0.2, 0])
        g1_fill = always_redraw(lambda: Rectangle(
            width=0.55, height=max(0.04, 3.68 * np.clip(fn_slow(t1.get_value()), 0.01, 1.0)),
            stroke_width=0, fill_color=C_MSG, fill_opacity=0.85
        ).move_to([4.5, g1_tr.get_bottom()[1] + 0.06 + max(0.04, 3.68 * np.clip(fn_slow(t1.get_value()), 0.01, 1.0)) / 2, 0]))
        g1_lbl = T("slow", size=22, color=C_MSG).next_to(g1_tr, UP, buff=0.12)

        g2_tr = Rectangle(width=0.65, height=3.8, stroke_color=C_REM, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([5.55, -0.2, 0])
        g2_fill = always_redraw(lambda: Rectangle(
            width=0.55, height=max(0.04, 3.68 * np.clip(fn_fast(t2.get_value()), 0.01, 1.0)),
            stroke_width=0, fill_color=C_REM, fill_opacity=0.85
        ).move_to([5.55, g2_tr.get_bottom()[1] + 0.06 + max(0.04, 3.68 * np.clip(fn_fast(t2.get_value()), 0.01, 1.0)) / 2, 0]))
        g2_lbl = T("fast", size=22, color=C_REM).next_to(g2_tr, UP, buff=0.12)

        self.add(P, eq, v_off, thresh, g1_tr, g1_fill, g1_lbl, g2_tr, g2_fill, g2_lbl, scope_tag("computed model"))

        self.at("Under constant input")
        self.add(live1, dot1)
        self.play(t1.animate.set_value(6.0), run_time=3.8, rate_func=linear)
        s_lbl = T("slower removal (k = 1)", size=24, color=C_MSG).move_to(P.pt(3.0, 1.07))
        self.play(FadeIn(s_lbl), run_time=0.35)

        self.at("When input stops")
        self.play(t1.animate.set_value(11.0), run_time=3.1, rate_func=linear)

        self.at("A faster removal")
        self.add(live2, dot2)
        self.play(t2.animate.set_value(6.0), run_time=1.15, rate_func=linear)
        f_lbl = T("faster removal (k = 2)", size=24, color=C_REM).move_to(P.pt(3.9, 0.34))
        self.play(FadeIn(f_lbl), run_time=0.25)

        self.at("lowers the balance")
        self.play(t2.animate.set_value(11.0), run_time=2.3, rate_func=linear)

        sl1 = Line(P.pt(6.0, 1.0), P.pt(6.55, 0.45), color=GOLD, stroke_width=4.5)
        sl2 = Line(P.pt(6.0, 0.5), P.pt(6.45, 0.05), color=GOLD, stroke_width=4.5)
        sl_lbl = T("same initial slope", size=24, color=GOLD).move_to(P.pt(8.2, 0.90))
        self.play(Create(sl1), Create(sl2), FadeIn(sl_lbl), run_time=0.7)
        self.finish()


# ==============================================================================
# SHARED BUILDER FOR S11_ADAPT & S13_PULSES (CARRIED TWO-PANEL)
# ==============================================================================
def build_adapt_panels():
    """TwoPanel comparing steady yellow input (left) vs separated yellow pulses (right)."""
    tp = TwoPanel("steady input", "separated pulses", colors=(C_REC, C_REC), top=3.20, bottom=-1.92, gap=0.35, width=12.8, size=30)

    # Left panel plots (x in [-5.8, -0.8])
    p_in_s = Plot(box=(-5.75, -0.85, 1.72, 2.25), xr=(0, 10), yr=(0, 1.25), xticks=(), yticks=(), ylabel="input", color=C_REC, label_size=22)
    p_bk_s = Plot(box=(-5.75, -0.85, 0.12, 0.96), xr=(0, 10), yr=(0, 1.05), xticks=(), yticks=(), ylabel="adaptive brake", color=C_REM, label_size=22)
    p_rp_s = Plot(box=(-5.75, -0.85, -1.25, -0.35), xr=(0, 10), yr=(0, 1.1), xticks=(), yticks=(), xlabel="time", ylabel="response", color=TEXT, label_size=22)

    # Right panel plots (x in [0.8, 5.8])
    p_in_p = Plot(box=(0.85, 5.75, 1.72, 2.25), xr=(0, 10), yr=(0, 1.25), xticks=(), yticks=(), ylabel="input", color=C_REC, label_size=22)
    p_bk_p = Plot(box=(0.85, 5.75, 0.12, 0.96), xr=(0, 10), yr=(0, 1.05), xticks=(), yticks=(), ylabel="adaptive brake", color=C_REM, label_size=22)
    p_rp_p = Plot(box=(0.85, 5.75, -1.25, -0.35), xr=(0, 10), yr=(0, 1.1), xticks=(), yticks=(), xlabel="time", ylabel="response", color=TEXT, label_size=22)

    return tp, (p_in_s, p_bk_s, p_rp_s), (p_in_p, p_bk_p, p_rp_p)


# ==============================================================================
# SCENE 11: ADAPTIVE BRAKE & RECOVERY IN GAPS
# ==============================================================================
class S11Adapt(BaseSpoken):
    def construct(self):
        tp, (p_in_s, p_bk_s, _), (p_in_p, p_bk_p, _) = build_adapt_panels()
        ts, u_s, b_s, r_s, u_p, b_p, r_p = compute_adapt_traces()

        f_us = lambda t: float(np.interp(t, ts, u_s))
        f_bs = lambda t: float(np.interp(t, ts, b_s))
        f_up = lambda t: float(np.interp(t, ts, u_p))
        f_bp = lambda t: float(np.interp(t, ts, b_p))

        bar_s = p_in_s.curve(f_us, color=C_REC, width=6, n=220)
        bar_p = p_in_p.curve(f_up, color=C_REC, width=6, n=240)

        t_tr = ValueTracker(0.0)
        live_bs = p_bk_s.live_curve(f_bs, t_tr, color=C_REM, width=5)
        dot_bs = p_bk_s.dot(lambda: t_tr.get_value(), lambda: f_bs(t_tr.get_value()), color=C_REM, ring=TEXT)
        live_bp = p_bk_p.live_curve(f_bp, t_tr, color=C_REM, width=5)
        dot_bp = p_bk_p.dot(lambda: t_tr.get_value(), lambda: f_bp(t_tr.get_value()), color=C_REM, ring=TEXT)

        # Live teal brake gauge bars inside the lower half of each panel (y = -0.95)
        bk_bar_s_tr = Rectangle(width=4.6, height=0.45, stroke_color=C_REM, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([-3.3, -0.92, 0])
        bk_bar_s = always_redraw(lambda: Rectangle(
            width=max(0.04, 4.50 * np.clip(f_bs(t_tr.get_value()), 0.01, 1.0)), height=0.35,
            stroke_width=0, fill_color=C_REM, fill_opacity=0.85
        ).move_to([bk_bar_s_tr.get_left()[0] + 0.05 + max(0.04, 4.50 * np.clip(f_bs(t_tr.get_value()), 0.01, 1.0)) / 2, -0.92, 0]))
        bk_bar_s_lbl = T("brake gauge", size=22, color=C_REM).next_to(bk_bar_s_tr, UP, buff=0.10).align_to(bk_bar_s_tr, LEFT)

        bk_bar_p_tr = Rectangle(width=4.6, height=0.45, stroke_color=C_REM, stroke_width=2.2, fill_color=BG, fill_opacity=0.9).move_to([3.3, -0.92, 0])
        bk_bar_p = always_redraw(lambda: Rectangle(
            width=max(0.04, 4.50 * np.clip(f_bp(t_tr.get_value()), 0.01, 1.0)), height=0.35,
            stroke_width=0, fill_color=C_REM, fill_opacity=0.85
        ).move_to([bk_bar_p_tr.get_left()[0] + 0.05 + max(0.04, 4.50 * np.clip(f_bp(t_tr.get_value()), 0.01, 1.0)) / 2, -0.92, 0]))
        bk_bar_p_lbl = T("brake gauge", size=22, color=C_REM).next_to(bk_bar_p_tr, UP, buff=0.10).align_to(bk_bar_p_tr, LEFT)

        # Response gauges revealed ONLY after both brake patterns settle (in bottom band y = -2.55)
        g_s = boxed_label("response: suppressed", color=C_ARR, size=26, pad=0.16).move_to([-3.3, -2.55, 0])
        g_p = boxed_label("response: preserved", color=C_G, size=26, pad=0.16).move_to([3.3, -2.55, 0])

        self.add(tp, p_in_s, p_bk_s, p_in_p, p_bk_p, bar_s, bar_p,
                 bk_bar_s_tr, bk_bar_s, bk_bar_s_lbl, bk_bar_p_tr, bk_bar_p, bk_bar_p_lbl,
                 scope_tag("schematic"))

        self.at("build a slower adaptive brake")
        self.add(live_bs, dot_bs, live_bp, dot_bp)
        self.play(t_tr.animate.set_value(4.5), run_time=3.8, rate_func=linear)

        self.at("A gap can let")
        self.play(t_tr.animate.set_value(7.5), run_time=2.8, rate_func=linear)

        self.at("Separated pulses")
        self.play(t_tr.animate.set_value(10.0), run_time=2.8, rate_func=linear)

        self.at("steady input")
        self.wait(max(0.1, self.t_of("never provides") - 0.1 - self.elapsed()))
        self.play(FadeIn(g_s, shift=UP * 0.1), FadeIn(g_p, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ==============================================================================
# SCENE 13: SEPARATED PULSES VS CONSTANT INPUT (GnRH EXAMPLE)
# ==============================================================================
class S13Pulses(BaseSpoken):
    def construct(self):
        tp, (p_in_s, p_bk_s, p_rp_s), (p_in_p, p_bk_p, p_rp_p) = build_adapt_panels()
        ts, u_s, b_s, r_s, u_p, b_p, r_p = compute_adapt_traces()

        f_us = lambda t: float(np.interp(t, ts, u_s))
        f_bs = lambda t: float(np.interp(t, ts, b_s))
        f_rs = lambda t: float(np.interp(t, ts, r_s))
        f_up = lambda t: float(np.interp(t, ts, u_p))
        f_bp = lambda t: float(np.interp(t, ts, b_p))
        f_rp = lambda t: float(np.interp(t, ts, r_p))

        bar_s = p_in_s.curve(f_us, color=C_REC, width=6, n=220)
        bar_p = p_in_p.curve(f_up, color=C_REC, width=6, n=240)
        bk_s_c = p_bk_s.curve(f_bs, color=C_REM, width=5, n=220)
        bk_p_c = p_bk_p.curve(f_bp, color=C_REM, width=5, n=240)

        tp_p = ValueTracker(0.0)
        tp_s = ValueTracker(0.0)
        live_rp = p_rp_p.live_curve(f_rp, tp_p, color=C_G, width=5)
        dot_rp = p_rp_p.dot(lambda: tp_p.get_value(), lambda: f_rp(tp_p.get_value()), color=C_G, ring=TEXT)
        live_rs = p_rp_s.live_curve(f_rs, tp_s, color=C_ARR, width=5)
        dot_rs = p_rp_s.dot(lambda: tp_s.get_value(), lambda: f_rs(tp_s.get_value()), color=C_ARR, ring=TEXT)

        self.add(tp, p_in_s, p_bk_s, p_rp_s, p_in_p, p_bk_p, p_rp_p,
                 bar_s, bar_p, bk_s_c, bk_p_c, scope_tag("schematic"))

        lamp_s = Circle(radius=0.2, stroke_width=0, fill_color=C_REC, fill_opacity=0.6).move_to([-0.55, 2.2, 0])
        lamp_p = Circle(radius=0.2, stroke_width=0, fill_color=C_REC, fill_opacity=0.6).move_to([6.05, 2.2, 0])
        add_pulse(lamp_s, 0.5, 0.45, 5.0, 0.0)
        add_pulse(lamp_p, 0.5, 0.45, 5.0, 2.0)
        self.add(lamp_s, lamp_p)
        self.at("Separated pulses")
        self.add(live_rp, dot_rp)
        self.play(tp_p.animate.set_value(10.0), run_time=6.2, rate_func=linear)

        self.at("Constant input")
        self.add(live_rs, dot_rs)
        self.play(tp_s.animate.set_value(10.0), run_time=3.2, rate_func=linear)

        # Bottom GnRH gonadotrope pathway strip (y = -2.55) animating during 10.5s..22.8s
        self.at("Pituitary responses")
        rec_box = boxed_label("GnRH receptor", color=C_REC, size=22, pad=0.12).move_to([-4.6, -2.55, 0])
        a1 = arrow_between([rec_box.get_right()[0] + 0.08, -2.55, 0], [-2.15, -2.55, 0], color=TEXT, stroke=3)
        msg_box = boxed_label("2nd messenger", color=C_MSG, size=22, pad=0.12).move_to([-0.9, -2.55, 0])
        a2 = arrow_between([msg_box.get_right()[0] + 0.08, -2.55, 0], [1.15, -2.55, 0], color=TEXT, stroke=3)
        rel_val = ValueTracker(0.95)
        rel_track = RoundedRectangle(corner_radius=0.10, width=2.4, height=0.56, stroke_color=C_G, stroke_width=2.2, fill_color=BG, fill_opacity=0.95).move_to([2.5, -2.55, 0])
        rel_fill = always_redraw(lambda: Rectangle(
            width=max(0.08, 2.28 * np.clip(rel_val.get_value(), 0.04, 1.0)), height=0.44,
            stroke_width=0, fill_color=C_G if rel_val.get_value() > 0.4 else C_ARR, fill_opacity=0.45
        ).move_to([rel_track.get_left()[0] + 0.06 + max(0.08, 2.28 * np.clip(rel_val.get_value(), 0.04, 1.0)) / 2, -2.55, 0]))
        rel_lbl = T("release step", size=22, color=TEXT).move_to(rel_track)
        self.play(FadeIn(rec_box), GrowArrow(a1), FadeIn(msg_box), GrowArrow(a2),
                  FadeIn(rel_track), FadeIn(rel_fill), FadeIn(rel_lbl), run_time=1.2)

        for _m, _p in ((a1, 0.0), (a2, 1.0), (rel_track, 2.0)):
            add_pulse(_m, 0.65, 0.35, 3.6, _p, stroke_only=True)
        lamp_g = Circle(radius=0.2, stroke_width=0, fill_color=C_G, fill_opacity=0.6).move_to([4.6, -2.55, 0])
        add_pulse(lamp_g, 0.5, 0.45, 5.0)
        self.add(lamp_g)
        # Animate continuous GnRH signal traveling receptor -> messenger -> release while narrator explains GnRH
        sig_dot = Dot([-4.6, -2.12, 0], radius=0.09, color=C_REC)
        self.play(FadeIn(sig_dot), run_time=0.2)
        for _ in range(2):
            sig_dot.move_to([-4.6, -2.12, 0])
            self.play(sig_dot.animate.move_to([2.5, -2.12, 0]), run_time=1.8, rate_func=linear)
        self.play(FadeOut(sig_dot), run_time=0.2)

        self.at("gonadotrop")
        block_lbl = T("GnRH: main block appears downstream", size=24, color=C_P, weight=BOLD).move_to([-0.9, -3.22, 0])
        stop_bar = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.72,
                                    stroke_color=C_ARR, stroke_width=2.5, fill_color=C_ARR, fill_opacity=0.92).move_to([0.92, -2.55, 0])
        self.play(FadeIn(stop_bar, shift=DOWN * 0.2), rel_val.animate.set_value(0.10), run_time=3.0, rate_func=smooth)
        self.play(FadeIn(block_lbl, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ==============================================================================
# SCENE 14: FULL PATHWAY + THREE TEAL TIMERS
# ==============================================================================
def build_timer_dial(center, progress_tracker, label="", radius=0.44):
    """Compact circular teal timer with wedge progress and hand sweeping clockwise from 12 o'clock."""
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, stroke_color=C_REM, stroke_width=3.5, fill_color=BG, fill_opacity=0.94).move_to(c)
    wedge = always_redraw(lambda: Sector(
        radius=radius * 0.88, start_angle=PI / 2,
        angle=-TAU * np.clip(progress_tracker.get_value(), 0.001, 0.999),
        arc_center=c, fill_color=C_REM, fill_opacity=0.30, stroke_width=0
    ))
    arc = always_redraw(lambda: Arc(
        radius=radius, start_angle=PI / 2,
        angle=-TAU * np.clip(progress_tracker.get_value(), 0.001, 0.999),
        arc_center=c, stroke_color=C_REM, stroke_width=6
    ))
    hand = always_redraw(lambda: Line(
        c, c + 0.76 * radius * np.array([np.sin(TAU * progress_tracker.get_value()),
                                         np.cos(TAU * progress_tracker.get_value()), 0]),
        color=TEXT, stroke_width=3.5
    ))
    g = VGroup(ring, wedge, arc, hand)
    if label:
        g.add(T(label, size=22, color=C_REM).next_to(ring, RIGHT, buff=0.18))
    return g


class S14Rule(BaseSpoken):
    def construct(self):
        world = build_cascade_world(rec_blocked=True, rec_p=True, g_frac=0.82, m_frac=0.82, t_frac=0.82,
                                    show_in_out=False, seed=31)
        t_rec = ValueTracker(1.0)
        t_g = ValueTracker(0.0)
        t_m = ValueTracker(0.0)
        t_t = ValueTracker(0.0)

        d_rec = build_timer_dial([3.1, Y_REC, 0], t_rec, label="receptor timer (done)")
        d_g = build_timer_dial([3.1, Y_G, 0], t_g, label="GTP hydrolysis")
        d_m = build_timer_dial([3.1, Y_MSG, 0], t_m, label="PDE breakdown")
        d_t = build_timer_dial([3.1, Y_TGT, 0], t_t, label="dephosphorylation")

        for idx, (y_c, col, tr, grp) in enumerate((
            (Y_G, C_G, t_g, world.g_blocks),
            (Y_MSG, C_MSG, t_m, world.m_dots),
            (Y_TGT, C_TGT, t_t, world.t_blocks),
        )):
            fill_rect = world.fills[idx]

            def upd_f(mob, y_c=y_c, col=col, tr=tr):
                f = max(0.04, 0.82 * (1.0 - np.clip(tr.get_value(), 0.0, 1.0)))
                h = (BOX_H - 0.10) * f
                r = Rectangle(width=BOX_W - 0.10, height=h, stroke_width=0, fill_color=col, fill_opacity=0.30)
                r.move_to([0, y_c - BOX_H / 2 + 0.05 + h / 2, 0])
                mob.become(r)

            fill_rect.add_updater(upd_f)

            def upd_grp(mob, tr=tr):
                mob.set_opacity(max(0.45, 1.0 - 0.55 * np.clip(tr.get_value(), 0.0, 1.0)))

            grp.add_updater(upd_grp)

        self.add(world, d_rec, d_g, d_m, d_t, scope_tag("schematic"))

        t_g.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / 7.2)))
        t_m.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / 12.2)))
        t_t.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / 17.5)))
        self.add(t_g, t_m, t_t)

        self.at("only one timer")
        self.play(Indicate(d_rec, color=C_ARR), run_time=0.55)

        self.at("GTP hydrolysis")
        self.play(Indicate(d_g, color=C_REM), run_time=0.45)

        self.at("messenger breakdown")
        self.play(Indicate(d_m, color=C_REM), run_time=0.45)

        self.at("dephosphorylation")
        self.play(Indicate(d_t, color=C_REM), run_time=0.45)

        self.at("Each downstream layer fades")
        self.wait(max(0.1, self.t_of("slowest surviving layer") - 0.35 - self.elapsed()))
        self.at("surviving")
        self.play(Indicate(world.pools[2], color=C_P), run_time=0.6)
        self.finish()


# ==============================================================================
# SCENE 15: END CARD
# ==============================================================================
class S15End(EndCard):
    LINE = "Each downstream layer fades when removal outruns production."
