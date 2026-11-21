"""
Paid to Let Go — STEMhop explainer film ("The Proton-Motive Force and ATP Synthase").

COLOUR MAP (one colour per concept for the whole film):
- YELLOW (#F5D547): protons (H+) and proton-driven gradient energy glow
- BLUE (#58C4DD): electron transport chain block (opening link only)
- ROTOR_COL (#96E072, bright green): rotating parts of ATP synthase (c-ring rotor, bent gamma shaft)
- GREEN (#83C167): ATP (small solid squares; hollow outlined square for Walker's look-alike) and synthase outlines
- STATOR_FILL (#9EB39E, pale green-grey fill with GREEN outline): fixed synthase parts (a subunit, alpha/beta head)
- GOLD (#D4A843): ADP (dots)
- ORANGE (#FF862F): inorganic phosphate Pi (dots)
- GREY (#8B93A1): inner mitochondrial membrane band, axes, structural frames, scope tag
- RED (#FC6255): brief block/leak ghosts in s00; cross on unloaded c-subunit in s02
- TEXT (#E8EAF0): neutral labels, questions, counters, tallies
- TEAL (#3FB8C0): scientist/section tags ("Boyer", "Walker: one crystal", "vertebrate ring")

CARRIED WORLD:
A horizontal GREY inner mitochondrial membrane band crosses the frame, with crowded YELLOW protons
above (intermembrane space) and the matrix below. ATP synthase spans the membrane (c-ring rotor + fixed
a subunit in the membrane, bent gamma shaft reaching down into the alpha3-beta3 head in the matrix).
A small GREY "schematic" tag sits at bottom-right across the film (except the standard EndCard).

WHAT CHANGES PER SPOKEN SCENE (and what computes it):
- s00_link_and_hook: Brief RED block/leak ghosts flash (protons rebound off plug, stream through leak); BLUE chain fades out left while camera zooms onto ATP synthase; YELLOW protons fall through, GOLD ADP enters and GREEN ATP squares exit (computed continuous stream).
- s02_rotor: Membrane block resolves into enlarged 8-segment c-ring drum (projected 3D cylinder angles theta + k*pi/4) against fixed a subunit; proton slides down narrow upper half-channel onto notch; ring turns 45 deg into membrane while unloaded neighbor hits RED cross.
- s03_turn: Ring angle executes a fixed-seed (seed=7) biased random walk (jostling + 45 deg proton catches), carrying one marked proton ~315 deg to the lower half-channel and out into matrix, while bolted bent gamma shaft rotates synchronously.
- s04_head: Side-view c-ring shrinks to upper-left inset (turning); head expands simultaneously to top-down 6-segment ring around off-centre gamma lobe; lobe angle tracker drives trigonometric radial/angular deformation of all 3 beta wedges into distinct shapes.
- s05_predict: GOLD ADP and ORANGE Pi sit in one beta with flickering "new bond" link; YELLOW glow travels from inset down shaft conduit to hub; question card and two option chips fade in.
- s07_boyer: Question clears; gamma turns a full cycle showing conformational wave, then settles as open beta widens to take in ADP+Pi, loose holds them apart, and tight clamps shut to merge ADP+Pi into trapped GREEN ATP square (no flash/glow).
- s08_idea: Empty "bond" bar stays near zero; protons turn inset and gamma +120 deg, YELLOW glow flows to release trapped ATP square as "release" bar grows tall, smaller glow drives ADP+Pi binding from matrix as "binding" bar grows partway.
- s09_steps: Gamma steps 3 x 120 deg, advancing open/loose/tight labels and releasing 1, 2, 3 ATP squares (live counter); white crystal frame freezes head showing ATP look-alike, ADP, and empty site while inset ring keeps turning.
- s10_count: Returns to side view; 8 c-subunits highlight around the ring, then 8 protons drop in one by one, turning the c-ring 8 x 45 deg = 360 deg and releasing 3 ATP squares (every 120 deg), computing live tally "8 protons", "3 ATP", "8 / 3 = 2.7 per ATP".
- s11_tax: Translocase and phosphate carrier doors open in membrane; ATP/ADP electrogenic swap takes a YELLOW "toll" from gradient; Pi + H+ co-import; tally adds "+ about 1" -> "about 3.7 per exported ATP".
- s12_close: Carrier doors/tally fade; one bright marked proton drops in, rides ~315 deg around the c-ring ("its share: 45 degrees"), exits; camera follows gamma to tight site, which springs open to release finished ATP with brief YELLOW edge glow.
"""
from bp_parts import *

# ------------------------------------------------------------------ concept palette
PROTON_COL = YELLOW
ETC_COL = BLUE
ROTOR_COL = "#96E072"
ATP_COL = GREEN
STATOR_FILL = "#9EB39E"
ADP_COL = GOLD
PI_COL = ORANGE
MEMB_COL = GREY
ALERT_COL = RED


# ------------------------------------------------------------------ shared primitives
def make_membrane(y_bot=0.1, y_top=1.4):
    h = y_top - y_bot
    ym = (y_bot + y_top) / 2.0
    fill = Rectangle(width=14.6, height=h, stroke_width=0, fill_color=MEMB_COL, fill_opacity=0.20).move_to([0, ym, 0])
    top = Line([-7.3, y_top, 0], [7.3, y_top, 0], color=MEMB_COL, stroke_width=3)
    bot = Line([-7.3, y_bot, 0], [7.3, y_bot, 0], color=MEMB_COL, stroke_width=3)
    g = VGroup(fill, top, bot)
    g.set_z_index(-5)
    return g


def make_proton(pos=ORIGIN, radius=0.085, glow=False):
    d = Dot(pos, radius=radius, color=PROTON_COL, stroke_width=0)
    if not glow:
        return d
    halo = Circle(
        radius=radius * 2.1, stroke_color=PROTON_COL, stroke_width=2.5,
        fill_color=PROTON_COL, fill_opacity=0.28,
    ).move_to(pos)
    return VGroup(halo, d)


def make_adp(pos=ORIGIN, radius=0.11):
    return Dot(pos, radius=radius, color=ADP_COL, stroke_width=0)


def make_pi(pos=ORIGIN, radius=0.095):
    return Dot(pos, radius=radius, color=PI_COL, stroke_width=0)


def make_atp(pos=ORIGIN, side=0.23, hollow=False):
    if hollow:
        return Square(side_length=side, color=ATP_COL, stroke_width=3.5, fill_color=ATP_COL, fill_opacity=0.12).move_to(pos)
    return Square(side_length=side, color=ATP_COL, stroke_width=2.0, fill_color=ATP_COL, fill_opacity=0.92).move_to(pos)


def proton_pool(y_min=1.7, y_max=3.25, count=22, seed=7, x_min=-6.2, x_max=6.2, avoid_rects=()):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < count and tries < 600:
        tries += 1
        x = float(rng.uniform(x_min, x_max))
        y = float(rng.uniform(y_min, y_max))
        if any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in avoid_rects):
            continue
        if any(np.hypot(x - px, y - py) < 0.42 for px, py in pts):
            continue
        pts.append((x, y))
    return VGroup(*[make_proton([x, y, 0]) for x, y in pts])


def make_falling_proton_stream(x_top, y_top, y_bot, n=3, speed=0.65, radius=0.085):
    """Deterministic vertical stream of protons dropping through a channel."""
    dots = VGroup()
    span = y_top - y_bot
    for i in range(n):
        d = make_proton([x_top, y_top, 0], radius=radius)
        d._phase = i / n

        def upd(m, dt, sp=speed, yt=y_top, spn=span):
            m._phase = (m._phase + dt * sp) % 1.0
            m.move_to([x_top, yt - m._phase * spn, 0])

        d.add_updater(upd)
        dots.add(d)
    return dots


def make_leaving_atp_stream(x0, y0, dx=0.5, dy=-1.3, n=2, speed=0.45, side=0.22):
    """Deterministic stream of ATP squares leaving the head into the matrix."""
    sqs = VGroup()
    for i in range(n):
        sq = make_atp([x0, y0, 0], side=side)
        sq._phase = i / n

        def upd(m, dt, sp=speed):
            m._phase = (m._phase + dt * sp) % 1.0
            p = m._phase
            m.move_to([x0 + dx * p, y0 + dy * p, 0])
            op = 1.0 if p < 0.78 else max(0.0, (1.0 - p) / 0.22)
            m.set_opacity(op)

        sq.add_updater(upd)
        sqs.add(sq)
    return sqs


# ------------------------------------------------------------------ side-view rotary synthase
def build_c_ring(center, width, height, phase_tracker, loaded_fn=None, lit_fn=None, marked_idx=None, proton_radius=0.075):
    """Live 8-segment cylindrical c-ring rotor computed from phase_tracker (radians). Fixed topology for safe FadeIn/FadeOut."""
    cx, cy, _ = center
    R = width * 0.46
    seg_w = width * 0.19

    def mk():
        th = phase_tracker.get_value()
        items = []
        for k in range(8):
            a = th + k * (TAU / 8.0)
            ca = float(np.cos(a))
            sa = float(np.sin(a))
            x = cx + R * sa
            w_app = max(0.08, seg_w * (0.35 + 0.65 * abs(ca)))
            is_lit = lit_fn(k) if lit_fn else False
            if ca >= 0:
                fill_op = 0.88 if is_lit else 0.72
                col = PROTON_COL if is_lit else ROTOR_COL
                stroke_col = TEXT if is_lit else ATP_COL
                z = 1.0 + ca
            else:
                fill_op = 0.32 if is_lit else 0.20
                col = PROTON_COL if is_lit else ATP_COL
                stroke_col = ATP_COL
                z = -1.0 + ca
            rect = RoundedRectangle(
                corner_radius=0.05, width=w_app, height=height,
                stroke_color=stroke_col, stroke_width=2.0,
                fill_color=col, fill_opacity=fill_op,
            ).move_to([x, cy, 0])
            notch_r = min(0.065, w_app * 0.34)
            notch = Circle(
                radius=notch_r, stroke_color=BG, stroke_width=1.8,
                fill_color=BG, fill_opacity=0.85 if ca >= 0 else 0.55,
            ).move_to([x, cy, 0])
            is_loaded = bool(loaded_fn and loaded_fn(k))
            is_marked = bool(is_loaded and marked_idx is not None and k == marked_idx)
            pr = proton_radius * (1.15 if is_marked else 0.95)
            halo = Circle(
                radius=pr * 2.1, stroke_color=PROTON_COL, stroke_width=2.5,
                stroke_opacity=1.0 if is_marked else 0.0,
                fill_color=PROTON_COL, fill_opacity=0.28 if is_marked else 0.0,
            ).move_to([x, cy, 0])
            p = make_proton([x, cy, 0], radius=pr, glow=False)
            p.set_opacity((0.45 if ca < 0 else 1.0) if is_loaded else 0.0)
            grp = VGroup(rect, notch, halo, p)
            items.append((z, grp))
        items.sort(key=lambda t: t[0])
        return VGroup(*[g for _, g in items])

    return always_redraw(mk)


def build_bent_shaft(ring_center, ring_h, head_center, phase_tracker, bend_amp=0.35, stroke_w=9.0):
    """Live bent gamma shaft bolted to the c-ring, sweeping smoothly with phase_tracker."""
    cx, ry, _ = ring_center
    top_y = ry - ring_h * 0.45
    bot_y = head_center[1] + 0.05

    def mk():
        th = phase_tracker.get_value()
        bx = bend_amp * float(np.cos(th))
        p0 = np.array([cx, top_y, 0.0])
        p1 = np.array([cx + 0.15 * bx, 0.55 * top_y + 0.45 * bot_y, 0.0])
        p2 = np.array([cx + 0.95 * bx, 0.25 * top_y + 0.75 * bot_y, 0.0])
        p3 = np.array([cx + bx, bot_y, 0.0])
        shaft = CubicBezier(p0, p1, p2, p3, color=ROTOR_COL, stroke_width=stroke_w)
        tip = Dot(p3, radius=stroke_w * 0.01, color=ROTOR_COL)
        return VGroup(shaft, tip)

    return always_redraw(mk)


def build_a_subunit(c_center, c_width, c_height, gap=0.14, upper_open=True, lower_open=False):
    """Fixed pale green-grey a subunit pressed against the right side of the c-ring, with open-stroke half-channels."""
    w, h = c_width * 0.56, c_height * 1.02
    ax = c_center[0] + c_width * 0.52 + gap + w * 0.5
    ay = c_center[1]
    body = RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        stroke_color=ATP_COL, stroke_width=2.8, fill_color=STATOR_FILL, fill_opacity=0.18,
    ).move_to([ax, ay, 0])
    g = VGroup(body)
    left_x = ax - w * 0.5
    if upper_open:
        t_up = VMobject(stroke_color=PROTON_COL, stroke_width=5.0, fill_opacity=0)
        t_up.set_points_as_corners([
            [ax - w * 0.1, ay + h * 0.50, 0],
            [ax - w * 0.1, ay + h * 0.05, 0],
            [left_x - 0.02, ay + h * 0.05, 0],
        ])
        g.add(t_up)
    if lower_open:
        t_lo = VMobject(stroke_color=PROTON_COL, stroke_width=5.0, fill_opacity=0)
        t_lo.set_points_as_corners([
            [left_x - 0.02, ay - h * 0.06, 0],
            [ax + w * 0.16, ay - h * 0.06, 0],
            [ax + w * 0.16, ay - h * 0.50, 0],
        ])
        g.add(t_lo)
    g.body = body
    g.ax = ax
    g.ay = ay
    g.w = w
    g.h = h
    return g


def build_side_head(center, width=2.4, height=1.75):
    """Side-view F1 head (fixed pale green-grey with GREEN outline)."""
    return RoundedRectangle(
        corner_radius=0.45, width=width, height=height,
        stroke_color=ATP_COL, stroke_width=3.0, fill_color=STATOR_FILL, fill_opacity=0.16,
    ).move_to(center)


# ------------------------------------------------------------------ top-down F1 head
BETA_ANGLES = [PI / 2, -PI / 6, 7 * PI / 6]    # top (90), lower-right (330), lower-left (210)
ALPHA_ANGLES = [PI / 6, 3 * PI / 2, 5 * PI / 6]  # 30, 270, 150


def _beta_params(delta):
    """Smooth trigonometric conformation as a function of delta = beta_angle - gamma_angle."""
    c = float(np.cos(delta))
    s = float(np.sin(delta))

    def interp(tight_v, loose_v, open_v):
        a0 = (tight_v + loose_v + open_v) / 3.0
        a1 = tight_v - a0
        b1 = (loose_v - open_v) / np.sqrt(3.0)
        return a0 + a1 * c + b1 * s

    d_ang = interp(0.54, 0.72, 0.88)
    r_in = interp(0.70, 0.56, 0.44)
    r_out = interp(0.92, 0.99, 1.08)
    return d_ang, r_in, r_out


def build_topdown_head(center, radius, gamma_tracker, extra_tight_pinch=0.0,
                       open_flare=None, loose_pinch=None, tight_pinch_tr=None):
    """Top-down alpha3-beta3 ring + rotating off-centre green gamma lobe."""
    c = np.array(center, dtype=float)

    def mk():
        ga = gamma_tracker.get_value()
        parts = VGroup()
        for a0 in ALPHA_ANGLES:
            w = AnnularSector(
                inner_radius=0.48 * radius, outer_radius=0.94 * radius,
                angle=0.52, start_angle=a0 - 0.26,
                arc_center=c, color=STATOR_FILL, fill_opacity=0.14,
                stroke_color=MEMB_COL, stroke_width=2.2,
            )
            parts.add(w)
        for idx, b0 in enumerate(BETA_ANGLES):
            d_ang, ri, ro = _beta_params(b0 - ga)
            if idx == 0 and open_flare is not None:
                f = open_flare.get_value()
                d_ang += 0.18 * f
                ro += 0.08 * f
            if idx == 1 and loose_pinch is not None:
                p = loose_pinch.get_value()
                d_ang -= 0.10 * p
                ro -= 0.04 * p
            if idx == 2 and tight_pinch_tr is not None:
                t = tight_pinch_tr.get_value()
                d_ang -= 0.14 * t
                ri += 0.05 * t
            elif abs(np.cos(b0 - ga)) > 0.8:
                d_ang -= extra_tight_pinch
            w = AnnularSector(
                inner_radius=ri * radius, outer_radius=ro * radius,
                angle=d_ang, start_angle=b0 - d_ang / 2.0,
                arc_center=c, color=STATOR_FILL, fill_opacity=0.22,
                stroke_color=ATP_COL, stroke_width=3.6,
            )
            parts.add(w)
        hub_bg = Circle(radius=0.38 * radius, stroke_color=ATP_COL, stroke_width=1.8, fill_color=BG, fill_opacity=0.9).move_to(c)
        cam_dir = np.array([np.cos(ga), np.sin(ga), 0.0])
        lobe_main = Circle(radius=0.21 * radius, stroke_color=TEXT, stroke_width=1.5, fill_color=ROTOR_COL, fill_opacity=0.92).move_to(c + cam_dir * (0.12 * radius))
        lobe_tip = Dot(c + cam_dir * (0.31 * radius), radius=0.09 * radius, color=ROTOR_COL)
        parts.add(hub_bg, lobe_main, lobe_tip)
        return parts

    return always_redraw(mk)


def beta_pocket_pos(center, radius, beta_idx, frac=0.73):
    a = BETA_ANGLES[beta_idx]
    return np.array(center, dtype=float) + frac * radius * np.array([np.cos(a), np.sin(a), 0.0])


def make_inset_rotor(center=(-4.8, 1.55, 0), phase_tracker=None, proton_stream=True):
    """Side-view c-ring inset at upper left that keeps turning slowly."""
    c = np.array(center, dtype=float)
    box = RoundedRectangle(corner_radius=0.14, width=2.85, height=2.0, stroke_color=MEMB_COL, stroke_width=2.2, fill_color=BG, fill_opacity=0.88).move_to(c)
    mem = Rectangle(width=2.65, height=0.74, stroke_width=0, fill_color=MEMB_COL, fill_opacity=0.24).move_to(c)
    ring = build_c_ring(c + LEFT * 0.28, width=1.35, height=0.98, phase_tracker=phase_tracker,
                        loaded_fn=lambda k: np.sin(phase_tracker.get_value() + k * TAU / 8.0) < 0.25,
                        proton_radius=0.062)
    a_sub = RoundedRectangle(corner_radius=0.07, width=0.52, height=1.0, stroke_color=ATP_COL, stroke_width=2.2, fill_color=STATOR_FILL, fill_opacity=0.18).move_to(c + RIGHT * 0.74)
    g = VGroup(box, mem, ring, a_sub)
    if proton_stream:
        stream = make_falling_proton_stream(c[0] + 0.74, c[1] + 0.82, c[1] - 0.78, n=3, speed=0.85, radius=0.07)
        g.add(stream)
    return g


# ------------------------------------------------------------------ Scenes
class S00LinkAndHook(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))

        mem = make_membrane(-0.1, 1.2)
        protons = proton_pool(1.55, 3.25, count=22, seed=7)
        etc = RoundedRectangle(corner_radius=0.16, width=1.9, height=1.8, stroke_color=ETC_COL, stroke_width=3, fill_color=ETC_COL, fill_opacity=0.20).move_to([-3.8, 0.55, 0])
        etc_lbl = T("electron chain", 24, ETC_COL).next_to(etc, DOWN, buff=0.22)
        etc_grp = VGroup(etc, etc_lbl)

        syn_fo = RoundedRectangle(corner_radius=0.14, width=1.5, height=1.6, stroke_color=ATP_COL, stroke_width=3, fill_color=ROTOR_COL, fill_opacity=0.28).move_to([2.6, 0.55, 0])
        syn_stem = Line([2.6, -0.25, 0], [2.6, -0.75, 0], color=ROTOR_COL, stroke_width=7)
        syn_head = RoundedRectangle(corner_radius=0.42, width=2.2, height=1.55, stroke_color=ATP_COL, stroke_width=3, fill_color=STATOR_FILL, fill_opacity=0.18).move_to([2.6, -1.5, 0])
        syn_lbl = T("ATP synthase", 26, ATP_COL).next_to(syn_head, DOWN, buff=0.22)
        syn_grp = VGroup(syn_fo, syn_stem, syn_head)

        self.add(mem, protons, etc_grp, syn_grp, syn_lbl)

        # Ghost 1: block the proton flow (brief RED plug + protons rebounding off it)
        self.at("block the proton")
        plug = RoundedRectangle(corner_radius=0.1, width=1.15, height=0.75, stroke_color=ALERT_COL, stroke_width=4, fill_color=ALERT_COL, fill_opacity=0.90).move_to(syn_fo.get_center())
        p_blk = VGroup(
            make_proton([2.25, 1.85, 0], radius=0.12, glow=True),
            make_proton([2.60, 1.70, 0], radius=0.12, glow=True),
            make_proton([2.95, 1.85, 0], radius=0.12, glow=True),
        )
        self.play(FadeIn(plug), FadeIn(p_blk), run_time=0.4)
        self.play(p_blk.animate.shift(DOWN * 0.70), run_time=0.45)
        self.play(p_blk.animate.shift(UP * 0.85), run_time=0.45)
        self.play(FadeOut(plug), FadeOut(p_blk), run_time=0.35)

        # Ghost 2: leak around (brief RED leak channel + 4 protons pouring through)
        self.at("leak around")
        leak = DashedLine([4.7, 1.55, 0], [4.7, -0.45, 0], color=ALERT_COL, stroke_width=8, dash_length=0.16)
        leak_dots = VGroup(*[make_proton([4.7, 1.55 + i * 0.35, 0], radius=0.115, glow=True) for i in range(4)])
        self.play(Create(leak), FadeIn(leak_dots), run_time=0.35)
        self.play(leak_dots.animate.shift(DOWN * 2.5), run_time=1.0, rate_func=linear)
        self.play(FadeOut(leak), FadeOut(leak_dots), run_time=0.35)

        # Push in on ATP synthase until it fills ~70% of frame height; BLUE chain slides out and fades
        self.at("look inside")
        self.play(FadeOut(syn_lbl), run_time=0.2)
        target_mem = make_membrane(0.25, 1.95)
        new_fo = RoundedRectangle(corner_radius=0.18, width=2.4, height=2.05, stroke_color=ATP_COL, stroke_width=3.5, fill_color=ROTOR_COL, fill_opacity=0.28).move_to([0, 1.1, 0])
        new_stem = Line([0, 0.08, 0], [0, -0.58, 0], color=ROTOR_COL, stroke_width=10)
        new_head = RoundedRectangle(corner_radius=0.55, width=3.4, height=2.25, stroke_color=ATP_COL, stroke_width=3.5, fill_color=STATOR_FILL, fill_opacity=0.18).move_to([0, -1.7, 0])
        zoom_syn = VGroup(new_fo, new_stem, new_head)
        zoom_protons = proton_pool(2.2, 3.2, count=18, seed=11)

        self.play(
            etc_grp.animate.shift(LEFT * 2.5).set_opacity(0.0),
            Transform(mem, target_mem),
            Transform(syn_grp, zoom_syn),
            Transform(protons, zoom_protons),
            run_time=1.35,
        )
        self.remove(etc_grp)

        # Protons fall through inside the membrane block (stay within new_fo bounds so no panel 'outside' warning)
        self.at("Protons fall through")
        p_stream = make_falling_proton_stream(0.0, 1.95, 0.25, n=3, speed=0.68, radius=0.10)
        self.add(p_stream)

        # ADP enters head, ATP squares leave head (start just outside head border so no panel 'outside' warning)
        self.at("comes out")
        adp1 = make_adp([-2.4, -2.1, 0], radius=0.12)
        adp2 = make_adp([-2.7, -1.6, 0], radius=0.12)
        self.play(
            adp1.animate.move_to([-0.6, -1.7, 0]),
            adp2.animate.move_to([0.5, -1.8, 0]),
            run_time=0.75,
        )
        self.play(FadeOut(adp1), FadeOut(adp2), run_time=0.2)
        atp_stream = make_leaving_atp_stream(1.85, -2.15, dx=1.35, dy=-0.75, n=2, speed=0.55, side=0.24)
        self.add(atp_stream)

        # Question across top
        self.at("How does a")
        q = T("How does a proton pay?", 40, TEXT).move_to([0, 3.22, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(0.25, 1.95)
        protons = proton_pool(2.2, 3.2, count=18, seed=11)
        new_fo = RoundedRectangle(corner_radius=0.18, width=2.4, height=2.05, stroke_color=ATP_COL, stroke_width=3.5, fill_color=ROTOR_COL, fill_opacity=0.28).move_to([0, 1.1, 0])
        new_stem = Line([0, 0.08, 0], [0, -0.58, 0], color=ROTOR_COL, stroke_width=10)
        new_head = RoundedRectangle(corner_radius=0.55, width=3.4, height=2.25, stroke_color=ATP_COL, stroke_width=3.5, fill_color=STATOR_FILL, fill_opacity=0.18).move_to([0, -1.7, 0])
        p_stream = make_falling_proton_stream(0.0, 1.95, 0.25, n=3, speed=0.60, radius=0.10)
        atp_stream = make_leaving_atp_stream(1.85, -2.15, dx=1.35, dy=-0.75, n=2, speed=0.50, side=0.24)
        q = T("How does a proton pay?", 40, TEXT).move_to([0, 3.22, 0])
        self.add(mem, protons, new_fo, new_stem, new_head, p_stream, atp_stream, q)

        title = T("Paid to Let Go", 48, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeOut(q, run_time=0.45))
        self.play(FadeIn(title, shift=UP * 0.08), run_time=0.6)
        self.finish()


class S02Rotor(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(-1.45, 1.55)
        protons = proton_pool(1.9, 3.25, count=16, seed=13)
        block = RoundedRectangle(corner_radius=0.18, width=4.2, height=3.15, stroke_color=ATP_COL, stroke_width=3.5, fill_color=ROTOR_COL, fill_opacity=0.25).move_to([-0.2, 0.05, 0])
        self.add(mem, protons, block)

        theta = ValueTracker(0.0)
        loaded = set()
        c_center = np.array([-1.3, 0.05, 0.0])
        c_w, c_h = 3.5, 3.0
        c_ring = build_c_ring(c_center, c_w, c_h, theta, loaded_fn=lambda k: k in loaded, proton_radius=0.115)
        a_sub = build_a_subunit(c_center, c_w, c_h, gap=0.16, upper_open=True, lower_open=False)
        a_sub[1].set_stroke(opacity=0.0)

        self.at("ring of C subunits")
        lbl_c = T("c-ring rotor", 30, ROTOR_COL).next_to(c_ring, DOWN, buff=0.32)
        self.play(FadeOut(block, run_time=0.3), FadeIn(c_ring, run_time=0.45))
        self.play(FadeIn(lbl_c), run_time=0.35)

        self.at("presses against")
        a_sub.shift(RIGHT * 0.7)
        self.play(FadeIn(a_sub), run_time=0.35)
        self.play(a_sub.animate.shift(LEFT * 0.7), run_time=0.45)
        lbl_a = T("a subunit (fixed)", 28, TEXT).next_to(a_sub, RIGHT, buff=0.28)
        self.play(FadeIn(lbl_a), run_time=0.35)

        self.at("half channel")
        self.play(a_sub[1].animate.set_stroke(opacity=1.0), run_time=0.35)
        p_in = make_proton([a_sub.ax - a_sub.w * 0.1, a_sub.ay + a_sub.h * 0.78, 0], radius=0.125, glow=True)
        self.play(FadeIn(p_in), run_time=0.2)
        self.play(
            p_in.animate.move_to([a_sub.ax - a_sub.w * 0.1, a_sub.ay + a_sub.h * 0.05, 0]),
            theta.animate.set_value(0.05),
            run_time=0.5,
        )

        self.at("lands on an acid")
        r_drum = c_w * 0.46
        notch_pos = np.array([c_center[0] + r_drum, c_center[1], 0.0])
        self.play(p_in.animate.move_to(notch_pos), theta.animate.set_value(0.0), run_time=0.5)
        loaded.add(2)
        self.remove(p_in)
        self.add(c_ring)

        self.at("Only a loaded")
        self.play(theta.animate.set_value(-TAU / 8.0), run_time=2.4, rate_func=smooth)
        cross_pt = c_center + LEFT * (r_drum + 0.55)
        cross = VGroup(
            Line(cross_pt + UL * 0.24, cross_pt + DR * 0.24, color=ALERT_COL, stroke_width=6),
            Line(cross_pt + UR * 0.24, cross_pt + DL * 0.24, color=ALERT_COL, stroke_width=6),
        )
        self.play(FadeIn(cross), run_time=0.25)
        for _ in range(3):
            self.play(theta.animate.set_value(-TAU / 8.0 - 0.12), run_time=0.35)
            self.play(theta.animate.set_value(-TAU / 8.0), run_time=0.35)
        self.finish()


class S03Turn(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(-0.3, 1.65)
        protons = proton_pool(2.0, 3.25, count=16, seed=13)
        self.add(mem, protons)

        theta = ValueTracker(-TAU / 8.0)
        loaded = {2}
        marked = 2
        c_center = np.array([-1.0, 0.70, 0.0])
        c_w, c_h = 2.9, 2.05
        head_center = np.array([-1.0, -2.0, 0.0])

        c_ring = build_c_ring(c_center, c_w, c_h, theta, loaded_fn=lambda k: k in loaded, marked_idx=marked, proton_radius=0.095)
        a_sub = build_a_subunit(c_center, c_w, c_h, gap=0.14, upper_open=True, lower_open=True)
        a_sub[2].set_stroke(opacity=0.0)
        lbl_c = T("c-ring rotor", 26, ROTOR_COL).next_to(c_center + LEFT * (c_w * 0.55), LEFT, buff=0.25)
        lbl_a = T("a subunit", 26, TEXT).next_to(a_sub, RIGHT, buff=0.25)
        self.add(c_ring, a_sub, lbl_c, lbl_a)

        self.at("random jostling")
        rng = np.random.default_rng(7)
        t_cur = theta.get_value()
        for _ in range(5):
            jit = float(rng.choice([-1, 1]) * rng.uniform(0.08, 0.15))
            self.play(theta.animate.set_value(t_cur + jit), run_time=0.20, rate_func=linear)
        self.play(theta.animate.set_value(t_cur), run_time=0.15)

        self.at("mostly one way")
        dir_arrow = CurvedArrow(
            c_center + RIGHT * 1.1 + UP * 1.32,
            c_center + LEFT * 1.1 + UP * 1.32,
            angle=0.45, color=PROTON_COL, stroke_width=4,
        )
        dir_lbl = T("mostly one way", 26, PROTON_COL).next_to(dir_arrow, UP, buff=0.15)
        self.play(Create(dir_arrow), FadeIn(dir_lbl), run_time=0.4)

        self.at("Nearly a full turn")
        for step in range(2, 8):
            next_val = -step * (TAU / 8.0)
            self.play(theta.animate.set_value(theta.get_value() + 0.08), run_time=0.07, rate_func=linear)
            loaded.add((step + 1) % 8)
            self.play(theta.animate.set_value(next_val), run_time=0.19, rate_func=smooth)

        self.at("proton leaves")
        self.play(a_sub[2].animate.set_stroke(opacity=1.0), run_time=0.25)
        self.play(theta.animate.set_value(-TAU), run_time=0.35)
        loaded.discard(marked)
        p_out = make_proton([a_sub.ax - a_sub.w * 0.45, a_sub.ay - a_sub.h * 0.06, 0], radius=0.10, glow=True)
        self.add(p_out)
        self.play(p_out.animate.move_to([a_sub.ax + a_sub.w * 0.16, a_sub.ay - a_sub.h * 0.06, 0]), run_time=0.3)
        self.play(p_out.animate.move_to([a_sub.ax + a_sub.w * 0.16, a_sub.ay - a_sub.h * 1.05, 0]).set_opacity(0.0), run_time=0.55)
        self.remove(p_out)

        self.at("bent shaft")
        head = build_side_head(head_center, width=2.8, height=1.75)
        shaft = build_bent_shaft(c_center, c_h, head_center, theta, bend_amp=0.42, stroke_w=10.0)
        lbl_gamma = T("gamma shaft", 26, ROTOR_COL).next_to(head, RIGHT, buff=0.35).shift(UP * 0.45)
        self.play(FadeIn(head), FadeIn(shaft), FadeIn(lbl_gamma), run_time=0.55)
        self.play(theta.animate.set_value(-TAU - TAU * 0.45), run_time=1.8, rate_func=linear)
        self.finish()


class S04Head(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(-0.3, 1.65)
        c_center = np.array([-1.0, 0.70, 0.0])
        c_w, c_h = 2.9, 2.05
        head_center = np.array([-1.0, -2.0, 0.0])
        theta_side = ValueTracker(-TAU)
        side_ring = build_c_ring(c_center, c_w, c_h, theta_side, loaded_fn=lambda k: k in {0, 1, 3, 5, 7}, proton_radius=0.09)
        side_a = build_a_subunit(c_center, c_w, c_h, gap=0.14, upper_open=True, lower_open=True)
        side_head = build_side_head(head_center, width=2.8, height=1.75)
        side_shaft = build_bent_shaft(c_center, c_h, head_center, theta_side, bend_amp=0.42, stroke_w=10.0)
        self.add(mem, side_ring, side_a, side_head, side_shaft)

        self.at("reaches into the")
        self.play(theta_side.animate.set_value(-TAU - 0.8), run_time=0.9)

        gamma_ang = ValueTracker(7 * PI / 6)
        inset_phase = ValueTracker(0.0)
        inset_phase.add_updater(lambda m, dt: m.increment_value(-1.2 * dt))
        self.add(inset_phase)

        inset = make_inset_rotor(center=(-4.8, 1.65, 0), phase_tracker=inset_phase, proton_stream=True)
        head_c = np.array([0.4, -0.15, 0.0])
        head_r = 2.25
        top_head = build_topdown_head(head_c, head_r, gamma_ang)

        # Crossfade side view directly into inset + top-down head simultaneously (never leave inset alone)
        self.play(
            FadeOut(mem, side_ring, side_a, side_head, side_shaft, run_time=0.5),
            FadeIn(inset, top_head, run_time=0.6),
        )

        self.at("Three alpha and")
        lbl_alpha = T("alpha", 28, TEXT).move_to(head_c + np.array([np.cos(PI / 6), np.sin(PI / 6), 0]) * (head_r + 0.65))
        lbl_beta = T("beta", 28, ATP_COL).move_to(head_c + UP * (head_r + 0.58))
        self.play(FadeIn(lbl_alpha), FadeIn(lbl_beta), run_time=0.5)
        self.play(gamma_ang.animate.set_value(7 * PI / 6 + 0.8), run_time=3.0, rate_func=linear)

        self.at("presses differently")
        self.play(gamma_ang.animate.set_value(7 * PI / 6 + 2.2), run_time=2.5, rate_func=linear)

        self.at("holding each in")
        self.play(gamma_ang.animate.set_value(7 * PI / 6 + 2.7), run_time=1.5, rate_func=smooth)
        self.finish()


def _s05_world(bob_dots=True):
    """Shared builder for S05Predict end state and S06Pause backdrop."""
    inset_phase = ValueTracker(0.0)
    inset_phase.add_updater(lambda m, dt: m.increment_value(-1.2 * dt))
    inset = make_inset_rotor(center=(-4.8, 1.65, 0), phase_tracker=inset_phase, proton_stream=True)

    head_c = np.array([-0.3, -0.5, 0.0])
    head_r = 2.0
    gamma_ang = ValueTracker(7 * PI / 6)
    top_head = build_topdown_head(head_c, head_r, gamma_ang)

    lbl_alpha = T("alpha", 28, TEXT).move_to(head_c + np.array([np.cos(PI / 6), np.sin(PI / 6), 0]) * (head_r + 0.62))
    lbl_beta = T("beta", 28, ATP_COL).move_to(head_c + UP * (head_r + 0.52))

    p_base = beta_pocket_pos(head_c, head_r, 1, frac=0.72)
    adp = make_adp(p_base + LEFT * 0.16 + UP * 0.05, radius=0.115)
    pi = make_pi(p_base + RIGHT * 0.16 + DOWN * 0.05, radius=0.10)
    if bob_dots:
        bob(adp, amp=0.04, speed=3.0, seed=1)
        bob(pi, amp=0.04, speed=3.0, seed=3)
    bond = Line(adp.get_center(), pi.get_center(), color=TEXT, stroke_width=3.5)
    bond_lbl = T("new bond", 26, TEXT).move_to(head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.95))
    bond_ptr = Line(bond_lbl.get_left() + LEFT * 0.1, head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.05), color=TEXT, stroke_width=2.0)

    glow = Circle(radius=0.42, stroke_color=PROTON_COL, stroke_width=4.0, fill_color=PROTON_COL, fill_opacity=0.35).move_to(head_c)
    pulse(glow, base=4.0, amp=2.2, speed=4.2)

    return VGroup(inset, top_head, lbl_alpha, lbl_beta, adp, pi, bond, bond_lbl, bond_ptr, glow), inset_phase, adp, pi, bond, bond_lbl, bond_ptr, glow, head_c, inset


class S05Predict(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        grp, inset_phase, adp, pi, bond, bond_lbl, bond_ptr, glow, head_c, inset = _s05_world(bob_dots=True)
        inset, top_head, lbl_alpha, lbl_beta = grp[0], grp[1], grp[2], grp[3]
        self.add(inset_phase, inset, top_head, lbl_alpha, lbl_beta)

        self.at("beta subunit")
        self.play(Indicate(lbl_beta, color=PROTON_COL, scale_factor=1.15), run_time=0.8)

        self.at("from")
        self.play(FadeIn(adp), FadeIn(pi), run_time=0.45)
        self.play(Create(bond), FadeIn(bond_lbl), Create(bond_ptr), run_time=0.5)
        for _ in range(3):
            self.play(bond.animate.set_opacity(0.25), run_time=0.25)
            self.play(bond.animate.set_opacity(1.0), run_time=0.25)

        self.at("what does the")
        traveler = Dot(inset.get_center(), radius=0.18, color=PROTON_COL).set_opacity(0.9)
        self.add(traveler)
        self.play(traveler.animate.move_to(head_c), run_time=0.85)
        self.remove(traveler)
        self.add(glow)

        q = question_card("What does the energy buy?", ["the bond?", "something else?"],
                          y=3.15, color=TEXT, left=-2.0, max_w=8.0, chips_at=[4.4, 1.5, 0])
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.5)

        self.at("Making the bond")
        self.play(FadeIn(q.chips[0]), run_time=0.35)
        self.play(FadeIn(q.chips[1]), run_time=0.35)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What does the energy buy?"
    OPTIONS = ["the bond?", "something else?"]
    CHIPS_AT = [4.4, 1.5, 0]
    CARD = {"y": 3.15, "color": TEXT, "left": -2.0, "max_w": 8.0}
    RING_AT = (5.9, -2.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        grp, inset_phase, *_ = _s05_world(bob_dots=True)
        grp.add_updater(lambda m, dt, ph=inset_phase: ph.increment_value(-1.2 * dt))
        return VGroup(scope_tag("schematic"), grp)


class S07Boyer(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        grp, inset_phase, adp_old, pi_old, bond_old, bond_lbl_old, bond_ptr_old, glow_old, _, _ = _s05_world(bob_dots=False)
        q = question_card("What does the energy buy?", ["the bond?", "something else?"],
                          y=3.15, color=TEXT, left=-2.0, max_w=8.0, chips_at=[4.4, 1.5, 0])
        self.add(inset_phase, grp, q)

        tag_boyer = T("Boyer", 30, TEAL).move_to([-5.3, 3.22, 0])
        self.at("Paul Boyer")
        self.play(
            FadeOut(q), FadeOut(adp_old), FadeOut(pi_old), FadeOut(bond_old),
            FadeOut(bond_lbl_old), FadeOut(bond_ptr_old), FadeOut(glow_old),
            FadeOut(grp[2]), FadeOut(grp[3]),
            FadeIn(tag_boyer),
            run_time=0.65,
        )
        self.remove(grp[0], grp[1])

        inset_new = make_inset_rotor(center=(-4.8, 1.35, 0), phase_tracker=inset_phase, proton_stream=True)
        head_c = np.array([0.3, -0.15, 0.0])
        head_r = 2.1
        gamma_ang = ValueTracker(7 * PI / 6 - TAU)
        open_flare = ValueTracker(0.0)
        loose_pinch = ValueTracker(0.0)
        tight_pinch_tr = ValueTracker(0.0)
        top_head = build_topdown_head(head_c, head_r, gamma_ang,
                                      open_flare=open_flare, loose_pinch=loose_pinch, tight_pinch_tr=tight_pinch_tr)
        self.add(inset_new, top_head)

        p_loose = beta_pocket_pos(head_c, head_r, 1, frac=0.73)
        adp_l = make_adp(p_loose + LEFT * 0.16, radius=0.115)
        pi_l = make_pi(p_loose + RIGHT * 0.16, radius=0.10)

        p_tight = beta_pocket_pos(head_c, head_r, 2, frac=0.83)
        adp_t = make_adp(p_tight + LEFT * 0.15, radius=0.115)
        pi_t = make_pi(p_tight + RIGHT * 0.15, radius=0.10)
        self.add(adp_l, pi_l, adp_t, pi_t)

        lbl_open = T("open", 30, TEXT).move_to(head_c + UP * (head_r + 0.78))
        lbl_loose = T("loose", 30, TEXT).move_to(head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.90))
        lbl_tight = T("tight", 30, TEXT).move_to(head_c + np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]) * (head_r + 0.90))

        self.at("As the shaft turns")
        self.play(gamma_ang.animate.set_value(7 * PI / 6), run_time=3.6, rate_func=smooth)
        self.play(FadeIn(lbl_open), FadeIn(lbl_loose), FadeIn(lbl_tight), run_time=0.5)

        self.at("Open takes in")
        p_open = beta_pocket_pos(head_c, head_r, 0, frac=0.73)
        adp_o = make_adp(p_open + RIGHT * 1.45 + UP * 0.45, radius=0.115)
        pi_o = make_pi(p_open + RIGHT * 1.80 + UP * 0.25, radius=0.10)
        self.play(FadeIn(adp_o), FadeIn(pi_o), run_time=0.25)
        self.play(
            open_flare.animate.set_value(1.0),
            adp_o.animate.move_to(p_open + LEFT * 0.18),
            pi_o.animate.move_to(p_open + RIGHT * 0.18),
            run_time=1.4,
        )

        self.at("Loose holds")
        self.play(
            loose_pinch.animate.set_value(1.0),
            adp_l.animate.move_to(p_loose + LEFT * 0.12 + UP * 0.04),
            pi_l.animate.move_to(p_loose + RIGHT * 0.12 + DOWN * 0.04),
            run_time=1.0,
        )

        self.at("In tight")
        atp_t = make_atp(p_tight, side=0.25)
        self.play(
            tight_pinch_tr.animate.set_value(1.0),
            adp_t.animate.move_to(p_tight),
            pi_t.animate.move_to(p_tight),
            run_time=0.7,
        )
        self.play(FadeOut(adp_t, run_time=0.2), FadeOut(pi_t, run_time=0.2), FadeIn(atp_t, run_time=0.25))

        self.at("held too firmly")
        for dx in (0.08, -0.08, 0.07, -0.07, 0.0):
            self.play(atp_t.animate.move_to(p_tight + np.array([dx, -0.04, 0])), run_time=0.22, rate_func=linear)
        self.finish()


class S08Idea(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        tag_boyer = T("Boyer", 30, TEAL).move_to([-5.3, 3.22, 0])
        inset_phase = ValueTracker(0.0)
        inset_phase.add_updater(lambda m, dt: m.increment_value(-1.2 * dt))
        inset = make_inset_rotor(center=(-5.0, 1.35, 0), phase_tracker=inset_phase, proton_stream=True)

        head_c = np.array([-0.9, 0.15, 0.0])
        head_r = 1.95
        gamma_ang = ValueTracker(7 * PI / 6)
        top_head = build_topdown_head(head_c, head_r, gamma_ang)

        lbl_open = T("open", 28, TEXT).move_to(head_c + UP * (head_r + 0.60))
        lbl_loose = T("loose", 28, TEXT).move_to(head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.85))
        lbl_tight = T("tight", 28, TEXT).move_to(head_c + np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]) * (head_r + 0.85))

        p_open = beta_pocket_pos(head_c, head_r, 0, frac=0.73)
        p_loose = beta_pocket_pos(head_c, head_r, 1, frac=0.73)
        p_tight = beta_pocket_pos(head_c, head_r, 2, frac=0.81)

        adp_o = make_adp(p_open + LEFT * 0.16, radius=0.11)
        pi_o = make_pi(p_open + RIGHT * 0.16, radius=0.095)
        adp_l = make_adp(p_loose + LEFT * 0.12 + UP * 0.04, radius=0.11)
        pi_l = make_pi(p_loose + RIGHT * 0.12 + DOWN * 0.04, radius=0.095)
        atp_t = make_atp(p_tight, side=0.24)

        self.add(tag_boyer, inset_phase, inset, top_head, lbl_open, lbl_loose, lbl_tight, adp_o, pi_o, adp_l, pi_l, atp_t)

        bar_base_y = -1.6
        bar_h = 3.2
        bar_w = 0.58
        xs = [2.65, 4.15, 5.65]

        def make_bar(x, lbl_str, col):
            track = Rectangle(width=bar_w, height=bar_h, stroke_color=MEMB_COL, stroke_width=2.2, fill_color=BG, fill_opacity=0.6).move_to([x, bar_base_y + bar_h / 2, 0])
            lbl = T(lbl_str, 24, TEXT).move_to([x, bar_base_y - 0.35, 0])
            val = ValueTracker(0.01)
            fill = always_redraw(lambda: Rectangle(
                width=bar_w - 0.08, height=max(0.02, val.get_value() * bar_h),
                stroke_width=0, fill_color=col, fill_opacity=0.88,
            ).move_to([x, bar_base_y + max(0.02, val.get_value() * bar_h) / 2, 0]))
            return track, lbl, fill, val

        t_bond, l_bond, f_bond, v_bond = make_bar(xs[0], "bond", ATP_COL)
        t_rel, l_rel, f_rel, v_rel = make_bar(xs[1], "release", PROTON_COL)
        t_bind, l_bind, f_bind, v_bind = make_bar(xs[2], "binding", ADP_COL)

        self.at("costs almost nothing")
        self.play(FadeIn(t_bond), FadeIn(l_bond), FadeIn(f_bond), run_time=0.4)
        self.play(v_bond.animate.set_value(0.04), run_time=0.5)

        self.at("Here is the idea")
        cap = caption("energy goes to letting go")
        self.play(FadeIn(cap), run_time=0.5)

        self.at("Protons turn the")
        glow1 = Dot(inset.get_center(), radius=0.16, color=PROTON_COL)
        self.add(glow1)
        p_loose_tight = beta_pocket_pos(head_c, head_r, 1, frac=0.81)
        self.play(
            glow1.animate.move_to(head_c),
            gamma_ang.animate.set_value(7 * PI / 6 + TAU / 3.0),
            adp_l.animate.move_to(p_loose_tight + np.array([0.07, 0.11, 0])),
            pi_l.animate.move_to(p_loose_tight + np.array([-0.07, -0.11, 0])),
            FadeOut(lbl_open, run_time=0.3), FadeOut(lbl_loose, run_time=0.3), FadeOut(lbl_tight, run_time=0.3),
            run_time=1.2,
        )

        self.at("pry")
        self.play(FadeIn(t_rel), FadeIn(l_rel), FadeIn(f_rel), run_time=0.3)
        self.play(
            glow1.animate.move_to(p_tight),
            atp_t.animate.move_to(p_tight + np.array([0.4, -1.2, 0])).set_opacity(0.0),
            v_rel.animate.set_value(0.92),
            run_time=1.1,
        )
        self.remove(glow1, atp_t)
        lbl_open2 = T("open", 28, TEXT).move_to(head_c + np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]) * (head_r + 0.85))
        lbl_loose2 = T("loose", 28, TEXT).move_to(head_c + UP * (head_r + 0.60))
        lbl_tight2 = T("tight", 28, TEXT).move_to(head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.85))
        self.play(FadeIn(lbl_open2), FadeIn(lbl_loose2), FadeIn(lbl_tight2), run_time=0.35)

        # Binding: bring ADP and Pi from below (clear of "open" label at lower-left)
        self.at("drives the binding")
        glow2 = Dot(head_c, radius=0.11, color=PROTON_COL)
        adp_new = make_adp(p_tight + np.array([0.25, -1.25, 0]), radius=0.11)
        pi_new = make_pi(p_tight + np.array([0.65, -1.25, 0]), radius=0.095)
        self.play(FadeIn(t_bind), FadeIn(l_bind), FadeIn(f_bind), FadeIn(glow2), FadeIn(adp_new), FadeIn(pi_new), run_time=0.3)
        self.play(
            glow2.animate.move_to(p_tight).set_opacity(0.0),
            adp_new.animate.move_to(p_tight + LEFT * 0.16),
            pi_new.animate.move_to(p_tight + RIGHT * 0.16),
            v_bind.animate.set_value(0.42),
            run_time=1.2,
        )
        self.remove(glow2)
        self.finish()


class S09Steps(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        inset_phase = ValueTracker(0.0)
        inset_phase.add_updater(lambda m, dt: m.increment_value(-2.2 * dt))
        inset = make_inset_rotor(center=(-4.9, 1.45, 0), phase_tracker=inset_phase, proton_stream=True)

        head_c = np.array([-0.4, -0.1, 0.0])
        head_r = 2.05
        gamma_ang = ValueTracker(7 * PI / 6)
        top_head = build_topdown_head(head_c, head_r, gamma_ang)

        atp_n = ValueTracker(0.0)
        atp_counter = counter("{:.0f} ATP per turn", atp_n, at=[4.45, 0.2, 0], size=30, color=ATP_COL)

        self.add(inset_phase, inset, top_head, atp_counter)

        pos_open = head_c + UP * (head_r + 0.58)
        pos_loose = head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.85)
        pos_tight = head_c + np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]) * (head_r + 0.85)
        positions = [pos_open, pos_loose, pos_tight]
        state_names = ["open", "loose", "tight"]
        cur_lbls = VGroup(*[T(state_names[i], 28, TEXT).move_to(positions[i]) for i in range(3)])
        self.add(cur_lbls)

        self.at("Each 120")
        release_betas = [2, 1, 0]
        for step in range(1, 4):
            rel_idx = release_betas[step - 1]
            p_rel = beta_pocket_pos(head_c, head_r, rel_idx, frac=0.81)
            out_dir = np.array([np.cos(BETA_ANGLES[rel_idx]), np.sin(BETA_ANGLES[rel_idx]), 0.0])
            sq = make_atp(p_rel, side=0.24)
            self.add(sq)
            new_lbls = VGroup(*[T(state_names[(i + step) % 3], 28, TEXT).move_to(positions[i]) for i in range(3)])
            self.play(
                gamma_ang.animate.set_value(7 * PI / 6 + step * TAU / 3.0),
                FadeOut(cur_lbls, run_time=0.35),
                run_time=0.9,
            )
            atp_n.set_value(step)
            self.play(
                sq.animate.move_to(p_rel + out_dir * 1.15).set_opacity(0.0),
                FadeIn(new_lbls, run_time=0.35),
                run_time=0.75,
            )
            self.remove(sq)
            cur_lbls = new_lbls

        self.at("John Walker")
        self.play(FadeOut(cur_lbls), FadeOut(atp_counter), run_time=0.35)
        snap_frame = RoundedRectangle(corner_radius=0.16, width=4.9, height=4.9, stroke_color=TEXT, stroke_width=3.5, fill_opacity=0).move_to(head_c)
        tag_walker = T("Walker: one crystal", 28, TEAL).move_to([-4.6, 3.22, 0])
        self.play(Create(snap_frame), FadeIn(tag_walker), run_time=0.65)

        self.at("ATP lookalike")
        p2 = beta_pocket_pos(head_c, head_r, 2, frac=0.81)
        lookalike = make_atp(p2, side=0.25, hollow=True)
        lbl_look = T("ATP look-alike", 26, ATP_COL).move_to(head_c + LEFT * 3.85 + DOWN * 1.55)
        ptr_look = Line(lbl_look.get_right() + RIGHT * 0.1, head_c + np.array([np.cos(7 * PI / 6), np.sin(7 * PI / 6), 0]) * (head_r + 0.05), color=ATP_COL, stroke_width=2.0)
        self.play(FadeIn(lookalike), FadeIn(lbl_look), Create(ptr_look), run_time=0.55)

        self.at("one ADP")
        p1 = beta_pocket_pos(head_c, head_r, 1, frac=0.72)
        adp_w = make_adp(p1, radius=0.13)
        lbl_adp = T("ADP", 26, ADP_COL).move_to(head_c + RIGHT * 3.35 + DOWN * 1.25)
        ptr_adp = Line(lbl_adp.get_left() + LEFT * 0.1, head_c + np.array([np.cos(-PI / 6), np.sin(-PI / 6), 0]) * (head_r + 0.05), color=ADP_COL, stroke_width=2.0)
        self.play(FadeIn(adp_w), FadeIn(lbl_adp), Create(ptr_adp), run_time=0.55)

        self.at("was empty")
        lbl_emp = T("empty", 26, TEXT).move_to(head_c + UP * (head_r + 0.72))
        self.play(FadeIn(lbl_emp), run_time=0.45)
        self.finish()


class S10Count(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(0.15, 1.35)
        protons_bg = proton_pool(1.75, 3.25, count=14, seed=19, x_min=-6.2, x_max=2.5,
                                 avoid_rects=[(-6.2, 2.75, -3.1, 3.4)])
        self.add(mem, protons_bg)

        theta = ValueTracker(0.0)
        lit_set = set()
        c_center = np.array([-2.2, 0.75, 0.0])
        c_w, c_h = 2.6, 1.85
        head_center = np.array([-2.2, -1.85, 0.0])

        c_ring = build_c_ring(c_center, c_w, c_h, theta, lit_fn=lambda k: k in lit_set, proton_radius=0.085)
        a_sub = build_a_subunit(c_center, c_w, c_h, gap=0.14, upper_open=True, lower_open=True)
        head = build_side_head(head_center, width=2.7, height=1.7)
        shaft = build_bent_shaft(c_center, c_h, head_center, theta, bend_amp=0.38, stroke_w=9.0)
        self.add(c_ring, a_sub, head, shaft)

        tag = T("vertebrate ring", 28, TEAL).move_to([-4.8, 3.22, 0])
        self.at("vertebrate ring")
        self.play(FadeIn(tag), run_time=0.4)
        self.play(theta.animate.set_value(-TAU), run_time=2.6, rate_func=linear)
        theta.set_value(0.0)

        tally_box = RoundedRectangle(corner_radius=0.14, width=5.2, height=2.45, stroke_color=MEMB_COL, stroke_width=2.2, fill_color=BG, fill_opacity=0.92).move_to([3.65, -1.6, 0])
        h_cnt = ValueTracker(0.0)
        atp_cnt = ValueTracker(0.0)
        row_h = counter("{:.0f} protons", h_cnt, at=[3.65, -0.85, 0], size=30, color=PROTON_COL)
        row_a = counter("{:.0f} ATP", atp_cnt, at=[3.65, -1.55, 0], size=30, color=ATP_COL)
        row_eq = M("8 / 3 = 2.7 per ATP", 28, TEXT).move_to([3.65, -2.30, 0])

        self.at("Eight protons")
        self.play(FadeIn(tally_box), FadeIn(row_h), run_time=0.25)
        atp_shown = False
        released_atps = VGroup()
        self.add(released_atps)

        for i in range(8):
            k_lit = (2 + i) % 8
            lit_set.add(k_lit)
            h_cnt.set_value(i + 1)
            p_drop = make_proton([a_sub.ax - a_sub.w * 0.1, a_sub.ay + a_sub.h * 0.72, 0], radius=0.085)
            self.add(p_drop)
            anims = [
                p_drop.animate.move_to([a_sub.ax - a_sub.w * 0.1, a_sub.ay + 0.04, 0]).set_opacity(0.0),
                theta.animate.set_value(-(i + 1) * (TAU / 8.0)),
            ]
            if i == 2 and not atp_shown:
                atp_shown = True
                self.add(row_a)
            if i in (2, 5, 7):
                idx = (2, 5, 7).index(i)
                atp_cnt.set_value(idx + 1)
                sq = make_atp(head_center + RIGHT * 0.9, side=0.23)
                released_atps.add(sq)
                anims.append(sq.animate.move_to(head_center + DOWN * 1.15 + RIGHT * (0.1 + idx * 0.45)))
            self.play(*anims, run_time=0.25, rate_func=linear)
            self.remove(p_drop)

        self.at("releases three")
        if not atp_shown:
            self.add(row_a)
        atp_cnt.set_value(3.0)
        self.play(
            released_atps.animate.shift(DOWN * 0.40 + RIGHT * 0.85),
            theta.animate.set_value(-TAU - 0.35),
            run_time=1.4,
        )

        self.at("about 2")
        self.play(
            FadeIn(row_eq),
            released_atps.animate.shift(DOWN * 0.25 + RIGHT * 0.90),
            theta.animate.set_value(-TAU - 0.85),
            run_time=2.0,
        )
        self.play(theta.animate.set_value(-TAU - 1.25), run_time=1.5)
        self.finish()


class S11Tax(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(0.15, 1.35)
        protons_bg = proton_pool(1.65, 3.2, count=14, seed=23, x_min=-6.2, x_max=5.8,
                                 avoid_rects=[(-2.7, 2.2, -0.2, 3.2), (0.2, 2.2, 3.1, 3.2), (-0.5, 1.65, 0.9, 2.45)])
        self.add(mem, protons_bg)

        theta = ValueTracker(0.0)
        theta.add_updater(lambda m, dt: m.increment_value(-1.1 * dt))
        self.add(theta)
        c_center = np.array([-4.4, 0.75, 0.0])
        c_w, c_h = 2.0, 1.65
        head_center = np.array([-4.4, -1.75, 0.0])

        c_ring = build_c_ring(c_center, c_w, c_h, theta, loaded_fn=lambda k: np.sin(theta.get_value() + k * TAU / 8.0) < 0.25, proton_radius=0.075)
        a_sub = build_a_subunit(c_center, c_w, c_h, gap=0.12, upper_open=True, lower_open=True)
        head = build_side_head(head_center, width=2.1, height=1.5)
        shaft = build_bent_shaft(c_center, c_h, head_center, theta, bend_amp=0.28, stroke_w=8.0)
        p_stream = make_falling_proton_stream(a_sub.ax - a_sub.w * 0.1, 1.85, 0.15, n=2, speed=0.65, radius=0.07)

        tally_box = RoundedRectangle(corner_radius=0.14, width=3.6, height=2.25, stroke_color=MEMB_COL, stroke_width=2.2, fill_color=BG, fill_opacity=0.92).move_to([4.5, -1.6, 0])
        t_27 = M("2.7 per ATP", 28, TEXT).move_to([4.5, -0.95, 0])
        t_plus = M("+ about 1", 28, PROTON_COL).move_to([4.5, -1.5, 0])
        t_tot = fit_text("about 3.7\nper exported ATP", max_w=3.25, size=26, color=ATP_COL, font=MONO).move_to([4.5, -2.18, 0])
        self.add(c_ring, a_sub, head, shaft, p_stream, tally_box, t_27)

        tx_door = RoundedRectangle(corner_radius=0.12, width=0.95, height=1.5, stroke_color=ATP_COL, stroke_width=3, fill_color=STATOR_FILL, fill_opacity=0.18).move_to([-1.45, 0.75, 0])
        tx_lbl = T("translocase", 26, TEXT).move_to([-1.45, 2.65, 0])
        tx_ptr = Line([-1.45, 2.38, 0], [-1.45, 1.55, 0], color=MEMB_COL, stroke_width=2)

        pi_door = RoundedRectangle(corner_radius=0.12, width=0.95, height=1.5, stroke_color=PI_COL, stroke_width=3, fill_color=STATOR_FILL, fill_opacity=0.18).move_to([1.65, 0.75, 0])
        pi_lbl = T("phosphate carrier", 26, TEXT).move_to([1.65, 2.65, 0])
        pi_ptr = Line([1.65, 2.38, 0], [1.65, 1.55, 0], color=MEMB_COL, stroke_width=2)

        self.at("translocase")
        self.play(FadeIn(tx_door), FadeIn(tx_lbl), Create(tx_ptr), FadeIn(pi_door), FadeIn(pi_lbl), Create(pi_ptr), run_time=0.65)

        self.at("swaps each")
        atp_swap = make_atp([-1.65, -1.2, 0], side=0.23)
        adp_swap = make_adp([-1.25, 2.0, 0], radius=0.115)
        self.play(FadeIn(atp_swap), FadeIn(adp_swap), run_time=0.25)
        self.play(
            atp_swap.animate.move_to([-1.65, 2.0, 0]),
            adp_swap.animate.move_to([-1.25, -1.2, 0]),
            run_time=1.35,
        )

        # Keep "toll" chip cleanly above membrane line (no straddle); drop a YELLOW dot from it into membrane
        self.at("moves charge")
        toll_chip = boxed_label("toll", PROTON_COL, size=24, pad=0.14).move_to([0.2, 2.05, 0])
        toll_dot = make_proton([0.2, 1.65, 0], radius=0.09, glow=True)
        self.play(FadeIn(toll_chip), FadeIn(toll_dot), run_time=0.35)
        self.play(toll_dot.animate.move_to([0.2, 0.35, 0]).set_opacity(0.0), run_time=0.9)
        self.remove(toll_dot)
        self.play(FadeOut(toll_chip), run_time=0.3)

        self.at("Phosphate comes in")
        pi_in = make_pi([1.45, 2.0, 0], radius=0.105)
        h_in = make_proton([1.85, 2.0, 0], radius=0.09, glow=True)
        self.play(FadeIn(pi_in), FadeIn(h_in), run_time=0.25)
        self.play(
            pi_in.animate.move_to([1.45, -1.35, 0]),
            h_in.animate.move_to([1.85, -1.35, 0]),
            run_time=1.25,
        )

        self.at("Together")
        self.play(FadeIn(t_plus), run_time=0.4)
        self.play(FadeIn(t_tot), run_time=0.55)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        self.add(scope_tag("schematic"))
        mem = make_membrane(0.15, 1.45)
        protons_bg = proton_pool(1.8, 3.25, count=14, seed=29, x_min=-6.2, x_max=5.8,
                                 avoid_rects=[(1.8, 1.6, 5.8, 3.0)])
        self.add(mem, protons_bg)

        theta = ValueTracker(0.0)
        loaded = {0, 1, 3, 5, 7}
        marked = 2
        c_center = np.array([-0.5, 0.80, 0.0])
        c_w, c_h = 2.6, 1.85
        head_center = np.array([-0.5, -1.85, 0.0])

        c_ring = build_c_ring(c_center, c_w, c_h, theta, loaded_fn=lambda k: k in loaded, marked_idx=marked, proton_radius=0.09)
        a_sub = build_a_subunit(c_center, c_w, c_h, gap=0.14, upper_open=True, lower_open=True)
        head = build_side_head(head_center, width=2.8, height=1.8)
        shaft = build_bent_shaft(c_center, c_h, head_center, theta, bend_amp=0.40, stroke_w=9.5)
        self.add(c_ring, a_sub, head, shaft)

        self.at("follow one proton")
        p_one = make_proton([a_sub.ax - a_sub.w * 0.1, a_sub.ay + a_sub.h * 0.9, 0], radius=0.11, glow=True)
        self.play(FadeIn(p_one), run_time=0.4)

        self.at("rides the ring")
        self.play(p_one.animate.move_to([a_sub.ax - a_sub.w * 0.1, a_sub.ay + 0.06, 0]), run_time=0.4)
        self.play(p_one.animate.move_to([c_center[0] + c_w * 0.46, c_center[1], 0]), run_time=0.3)
        loaded.add(marked)
        self.remove(p_one)
        self.add(c_ring)
        self.play(theta.animate.set_value(-7 * TAU / 8.0), run_time=1.8, rate_func=linear)

        self.at("eighth of a turn")
        share_tag = boxed_label("its share: 45 degrees", PROTON_COL, size=26).move_to([3.7, 2.25, 0])
        self.play(FadeIn(share_tag), run_time=0.4)
        self.play(theta.animate.set_value(-TAU), run_time=0.45)
        loaded.discard(marked)
        p_exit = make_proton([a_sub.ax - a_sub.w * 0.4, a_sub.ay - 0.08, 0], radius=0.105, glow=True)
        self.add(p_exit)
        self.play(p_exit.animate.move_to([a_sub.ax + a_sub.w * 0.16, a_sub.ay - a_sub.h * 0.85, 0]), run_time=0.55)

        self.at("bond costs")
        self.play(FadeOut(share_tag), FadeOut(p_exit), run_time=0.3)
        atp_tight = make_atp(head_center + RIGHT * 0.65, side=0.28)
        tight_lbl = T("tight site", 26, TEXT).next_to(head, RIGHT, buff=0.35)
        self.play(FadeIn(atp_tight), FadeIn(tight_lbl), run_time=0.45)

        self.at("above all")
        self.play(theta.animate.set_value(-TAU - TAU / 3.0), run_time=1.1)

        self.at("moment")
        target_pos = head_center + RIGHT * 2.5 + DOWN * 0.55
        edge_glow = Square(side_length=0.42, stroke_color=PROTON_COL, stroke_width=4, fill_opacity=0).move_to(atp_tight.get_center())
        edge_glow.set_stroke(opacity=0.0)
        self.add(edge_glow)
        self.play(
            FadeOut(tight_lbl, run_time=0.3),
            atp_tight.animate.move_to(target_pos),
            edge_glow.animate.move_to(target_pos).set_stroke(opacity=1.0),
            run_time=0.7,
        )
        self.play(
            atp_tight.animate.shift(RIGHT * 1.1 + DOWN * 0.3),
            edge_glow.animate.shift(RIGHT * 1.1 + DOWN * 0.3).set_stroke(opacity=0.0),
            run_time=1.0,
        )
        self.finish()


class S13End(EndCard):
    LINE = "Protons turn the rotor; the turning pays mainly to release ATP."
