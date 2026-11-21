"""
Acid On, Acid Off — Gut Motility, Secretion and Gut Hormones (Chapter 2)

COLOUR MAP (one colour per concept, carried from Film 1 + new acid/brake colours):
- BLUE    (#58C4DD) : smooth muscle wall of stomach and duodenum
- YELLOW  (#F5D547) : slow-wave electrical beat ticks propagating along the muscle wall
- FAT     (#F7E695) : pale yellow fat droplets inside chyme
- GREEN   (#83C167) : excitatory / ON signals (vagus, ACh, histamine, gastrin, G cell, 'on', food arrow)
- ORANGE  (#F0944D) : gut contents (food blobs, digested protein fragments, chyme)
- GREY    (#8B93A1) : outlines, blood vessel, ECL cell, K+/Cl- ions, tight junctions, schematic tags
- MAGENTA (#E05297) : acid (H+ ions, hydrochloric acid)
- CYAN    (#24E8D8) : brake signals (somatostatin, secretin, CCK, D/S/I cells, brake pads, 'off' switch)
- WHITE   (#FFFFFF) : mucus gel layer; TEXT (#E8EAF0) for labels, question card, end card
- BICARB  (#B8DCFF) : pale blue-white bicarbonate ions trapped in the mucus gel

ONE WORLD, CARRIED ALL FILM:
A side-view anatomical cross-section of the stomach (body upper-left, antrum lower-center, narrow pylorus)
flowing into the descending duodenum along the right edge, with YELLOW slow-wave beat ticks propagating
along the BLUE muscle wall and a circular/bay magnifying window on the body lining showing a parietal cell.

WHAT CHANGES PER SPOKEN SCENE (and what computes it):
- s00_link_and_question : Slow-wave phase travels down the BLUE wall; magnifying window opens on the body;
                          ValueTracker drives luminal H+ accumulation and drops the vertical pH gauge to
                          'about pH 1' against sparse cytosolic H+ ('about a million-fold'); 'on?' / 'off?' appear.
- s02_pump              : Zoomed parietal cell (65% height) + live scaled stomach inset; vesicle position tracker
                          merges 3 stored-pump vesicles into the deep fold membrane; cycle-angle tracker turns
                          turnstiles to swap MAGENTA H+ out for GREY K+ in with ATP flashes, then K+/Cl- exit.
- s03_switches          : Full world returns with ECL cell beside parietal cell; ACh, histamine, and gastrin
                          dock sequentially, each stepping up computed turnstile speed and MAGENTA emission;
                          vagus wire descends and 4 cephalic icons fire pulses down it while lumen stays empty.
- s04_gastric_phase     : ORANGE food enters and stretch tracker bows the BLUE wall outward; protein hits
                          antral G cell, which releases GREEN gastrin dots traveling along the blood vessel to
                          ECL cell -> histamine -> higher computed acid flux and lower schematic pH gauge.
- s05_idea              : Swirling food and acid in the world; GREEN 'food turns on' arc grows from incoming
                          food to parietal cell, then open-ended CYAN 'downstream turns down' arc grows toward
                          antrum/duodenum; both pulse together.
- s06_antrum_brake      : MAGENTA acid stream flows down to antrum, extending the CYAN arrow to antrum; acid hits
                          D cell -> CYAN somatostatin puffs onto G cell -> computed gastrin emission drops;
                          two-step feedback pulse plays 'more acid, less gastrin'.
- s07_predict           : Computed chyme bolus (ORANGE + MAGENTA + pale yellow fat) jets through pylorus into
                          duodenum past two dim unlabelled cells; question card 'More acid, or less?' appears.
- s09_answer            : Question dissolves; acid hits S cell -> CYAN secretin, fat/protein hit I cell -> CYAN
                          CCK; both travel up blood vessel to slow parietal turnstile speed and thin MAGENTA;
                          dashed 'probably' path links CCK toward somatostatin.
- s10_two_places        : CYAN downstream arrow forks to CYAN brake pads at antrum ('brake 1') and duodenum
                          ('brake 2'); duodenal pad glows, GREEN food arrow dims, MAGENTA thins, 'off?' lights CYAN.
- s11_protection        : Zoomed row of surface cells; bicarbonate rises into settling WHITE mucus gel;
                          computed depth-decay profile keeps MAGENTA dense in lumen and sparse at surface;
                          MAGENTA dot bounces elastically off glowing GREY tight junction seal.
- s12_close             : Full world summary; incoming food pulses GREEN arrow, chyme flows through pylorus
                          and pulses forked CYAN brake pads sequentially as MAGENTA settles to a steady trickle.
"""

from bp_parts import *

# Film-specific colour constants (see COLOUR MAP above)
ORANGE = "#F0944D"
MAGENTA = "#E05297"
CYAN = "#24E8D8"
FAT_COLOR = "#F7E695"
BICARB = "#B8DCFF"


# ------------------------------------------------------------------ spline & tube geometry helpers
def _catmull_rom(pts, n_per_seg=16):
    """Smooth polyline through control points using Catmull-Rom."""
    arr = [np.array([p[0], p[1], 0.0], dtype=float) for p in pts]
    if len(arr) < 2:
        return arr
    ext = [arr[0] + (arr[0] - arr[1])] + arr + [arr[-1] + (arr[-1] - arr[-2])]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(n_per_seg):
            t = k / float(n_per_seg)
            t2, t3 = t * t, t * t * t
            pt = 0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t3
            )
            out.append(pt)
    out.append(arr[-1])
    return out


def _sample_polyline(pts, s_frac):
    """Point and unit tangent along polyline pts at normalised arc position s_frac in [0, 1]."""
    arr = np.asarray(pts, dtype=float)
    diffs = np.diff(arr, axis=0)
    lens = np.linalg.norm(diffs, axis=1)
    cum = np.concatenate([[0.0], np.cumsum(lens)])
    total = max(cum[-1], 1e-6)
    target = np.clip(s_frac, 0.0, 1.0) * total
    idx = int(np.clip(np.searchsorted(cum, target, side="right") - 1, 0, len(diffs) - 1))
    seg_len = max(lens[idx], 1e-6)
    u = (target - cum[idx]) / seg_len
    pos = arr[idx] + u * diffs[idx]
    tang = diffs[idx] / seg_len
    return pos, tang


def _smooth_curve(pts, color=GREY, width=3.5, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m


# ------------------------------------------------------------------ Stomach-Duodenum Tube Model
# Smooth well-spaced axis from esophageal inlet -> body -> antrum -> pylorus -> descending duodenum
_STOMACH_AXIS = [
    (-3.72, 2.30), (-3.88, 1.50), (-3.72, 0.48), (-3.15, -0.58),
    (-2.05, -1.36), (-0.50, -1.62), (1.00, -1.46), (2.15, -1.12),
    (3.05, -0.78), (3.72, -1.04), (3.92, -1.72), (3.94, -2.50),
]

# Lumen half-width profile along the axis (smoothly pinches at pylorus s ~ 0.65)
_HALF_WIDTH_KNOTS = [
    (0.00, 0.28), (0.12, 0.58), (0.28, 0.86), (0.45, 0.78),
    (0.57, 0.44), (0.66, 0.16), (0.76, 0.26), (1.00, 0.27),
]

# Blood vessel along inner-left side of duodenum and outer antrum up to the parietal/ECL bay
_BLOOD_PATH_PTS = [
    (3.26, -2.42), (3.25, -1.25), (2.35, -1.58), (1.05, -2.38),
    (-0.45, -2.52), (-1.85, -2.26), (-2.38, -1.18), (-2.18, 0.15),
    (-1.76, 0.72),
]

_LUMEN_CENTERLINE = _catmull_rom(_STOMACH_AXIS, 12)


def _wall_contours(stretch=0.0, scale=1.0, offset=ORIGIN, wave_t=0.0):
    """Compute guaranteed non-crossing inner & outer stomach-duodenum walls from _STOMACH_AXIS."""
    axis = _LUMEN_CENTERLINE
    n = len(axis)
    s_vals = np.linspace(0.0, 1.0, n)
    ks = [k[0] for k in _HALF_WIDTH_KNOTS]
    ws = [k[1] for k in _HALF_WIDTH_KNOTS]
    r_in_arr = np.interp(s_vals, ks, ws)
    w_wall = 0.20

    # Compute smooth tangents & normals along axis
    arr = np.asarray(axis, dtype=float)
    tang = np.zeros_like(arr)
    tang[1:-1] = arr[2:] - arr[:-2]
    tang[0] = arr[1] - arr[0]
    tang[-1] = arr[-1] - arr[-2]
    norms = np.linalg.norm(tang, axis=1, keepdims=True)
    tang = tang / np.maximum(norms, 1e-6)
    n_left = np.stack([-tang[:, 1], tang[:, 0], np.zeros(n)], axis=1)

    inner_left, inner_right = [], []
    outer_left, outer_right = [], []
    for i in range(n):
        p = arr[i].copy()
        s = s_vals[i]
        # Stretch bows the greater-curvature side outward in stomach body & antrum (s in 0.08..0.58)
        st = stretch * np.sin(np.pi * np.clip((s - 0.06) / 0.54, 0.0, 1.0)) if 0.06 < s < 0.60 else 0.0
        # Travelling slow-wave wall beat ripple along the smooth muscle
        beat_rip = 0.032 * (0.5 + 0.5 * np.cos(3.4 * wave_t - 11.0 * s)) * np.sin(np.pi * s)
        r_l = r_in_arr[i] + 0.4 * beat_rip
        r_r = r_in_arr[i] + 0.22 * st + beat_rip
        il = (p + n_left[i] * r_l) * scale + offset
        ol = (p + n_left[i] * (r_l + w_wall)) * scale + offset
        ir = (p - n_left[i] * r_r) * scale + offset
        or_ = (p - n_left[i] * (r_r + w_wall)) * scale + offset
        inner_left.append(il)
        outer_left.append(ol)
        inner_right.append(ir)
        outer_right.append(or_)

    return outer_right, outer_left, inner_right, inner_left


class GutWorld(VGroup):
    """Carried world: stomach + duodenum with travelling YELLOW slow-wave beat ticks."""

    def __init__(self, stretch=0.0, show_blood=False, show_labels=True, accent_beat=False,
                 scale=1.0, offset=ORIGIN):
        super().__init__()
        self.t_clock = ValueTracker(0.0)
        self.stretch = ValueTracker(stretch)
        self.beat_boost = ValueTracker(1.0 if accent_beat else 0.0)
        self._scale = scale
        self._offset = np.array(offset, dtype=float)

        def _mk_wall():
            s = self.stretch.get_value()
            wt = self.t_clock.get_value()
            or_, ol, ir, il = _wall_contours(s, self._scale, self._offset, wave_t=wt)
            outer_ring = or_ + list(reversed(ol))
            inner_ring = ir + list(reversed(il))
            wall_poly = Polygon(*outer_ring, stroke_color=BLUE, stroke_width=3.2 * max(0.55, self._scale),
                                fill_color=BLUE, fill_opacity=0.16)
            lumen_poly = Polygon(*inner_ring, stroke_color=GREY, stroke_width=2.0 * max(0.55, self._scale),
                                 fill_color=BG, fill_opacity=0.96)
            return VGroup(wall_poly, lumen_poly)

        self.wall_group = always_redraw(_mk_wall)
        self.add(self.wall_group)

        # Travelling YELLOW slow-wave ticks embedded in the BLUE greater wall & outer duodenal wall
        self.ticks = VGroup()
        n_ticks = 24
        tick_fracs = np.linspace(0.05, 0.96, n_ticks)
        for idx, sf in enumerate(tick_fracs):
            tick = Line(ORIGIN, RIGHT * 0.14 * scale, color=YELLOW, stroke_width=4.5 * max(0.55, scale))
            tick._sf = sf
            tick._idx = idx

            def _upd_tick(m, dt):
                t = self.t_clock.get_value()
                s = self.stretch.get_value()
                or_, _, _, _ = _wall_contours(s, self._scale, self._offset, wave_t=t)
                pos, tang = _sample_polyline(or_, m._sf)
                normal = np.array([-tang[1], tang[0], 0.0])  # points inward across muscle wall
                wave = 0.5 + 0.5 * np.cos(3.4 * t - 11.0 * m._sf)
                boost = self.beat_boost.get_value()
                length = (0.14 + 0.13 * wave + 0.08 * boost * wave) * self._scale
                p0 = pos - normal * 0.02 * self._scale
                p1 = p0 + normal * length
                m.put_start_and_end_on(p0, p1)
                m.set_stroke(width=(3.2 + 3.2 * wave + 2.0 * boost * wave) * max(0.55, self._scale),
                             opacity=0.32 + 0.62 * wave + 0.06 * boost)

            tick.add_updater(_upd_tick)
            self.ticks.add(tick)
        self.add(self.ticks)

        # Optional blood vessel running along inner duodenum & antrum up to parietal/ECL bay
        if show_blood:
            bpts = [np.array(p, dtype=float) * self._scale + self._offset for p in _catmull_rom(_BLOOD_PATH_PTS, 14)]
            bv_outer = _smooth_curve(bpts, color=GREY, width=9.0 * max(0.55, scale), opacity=0.45)
            bv_inner = _smooth_curve(bpts, color=BG, width=4.5 * max(0.55, scale), opacity=0.95)
            self.blood_vessel = VGroup(bv_outer, bv_inner)
            self.add(self.blood_vessel)
            if show_labels:
                self.blood_label = T("blood", 24, GREY).move_to([2.45, -2.55, 0])
                self.add(self.blood_label)

        if show_labels:
            lb_body = T("body", 26, TEXT).move_to([-5.65, 1.25, 0])
            lb_antrum = T("antrum", 26, TEXT).move_to([-1.15, -3.05, 0])
            lb_duod = T("duodenum", 26, TEXT).move_to([5.45, -1.62, 0])
            self.anat_labels = VGroup(lb_body, lb_antrum, lb_duod)
            self.add(self.anat_labels)

        self.add_updater(lambda m, dt: self.t_clock.increment_value(dt))


def _acid_swarm(lumen_pts, n_dots, seed, speed=0.20, color=MAGENTA, radius=0.050,
                rate_tracker=None, scale=1.0, offset=ORIGIN):
    """Deterministic computed swarm of particles swirling inside a curved path."""
    rng = np.random.default_rng(seed)
    pts = [np.array(p, dtype=float) * scale + np.array(offset, dtype=float) for p in lumen_pts]
    dots = VGroup()
    for i in range(n_dots):
        sf0 = rng.uniform(0.06, 0.88)
        lat = rng.uniform(-0.34, 0.34) * scale
        phase = rng.uniform(0, TAU)
        freq = rng.uniform(1.2, 2.4)
        d = Dot(radius=radius, color=color, fill_opacity=0.88)
        d._sf0 = sf0
        d._lat = lat
        d._phase = phase
        d._freq = freq
        d._idx = i

        def _upd(m, dt, n=n_dots, sc=scale):
            rate = rate_tracker.get_value() if rate_tracker is not None else 1.0
            active = m._idx < max(2, int(round(rate * n)))
            m.set_opacity(0.88 if active else 0.0)
            if not active:
                return
            t = getattr(m, "_t", 0.0) + dt
            m._t = t
            sf = (m._sf0 + speed * (0.4 + 0.6 * rate) * t) % 0.78 + 0.06
            pos, tang = _sample_polyline(pts, sf)
            norm = np.array([-tang[1], tang[0], 0.0])
            offset_v = norm * (m._lat + 0.12 * sc * np.sin(m._freq * t + m._phase)) + tang * (0.07 * sc * np.cos(m._freq * t))
            m.move_to(pos + offset_v)

        d.add_updater(_upd)
        dots.add(d)
    return dots


def _box_swarm(cx, cy, w, h, n_dots, seed, color=MAGENTA, radius=0.045,
               rate_tracker=None, drift=(0.0, 0.0), amp=0.14):
    """Computed oscillating swarm inside a bounding box."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for i in range(n_dots):
        x0 = cx + rng.uniform(-w * 0.42, w * 0.42)
        y0 = cy + rng.uniform(-h * 0.42, h * 0.42)
        phx, phy = rng.uniform(0, TAU, 2)
        fx, fy = rng.uniform(1.0, 2.3, 2)
        d = Dot(point=[x0, y0, 0], radius=radius, color=color, fill_opacity=0.88)
        d._base = np.array([x0, y0, 0.0])
        d._ph = (phx, phy)
        d._fr = (fx, fy)
        d._idx = i
        d._t = 0.0

        def _upd(m, dt, n=n_dots):
            rate = rate_tracker.get_value() if rate_tracker is not None else 1.0
            active = m._idx < max(1, int(round(rate * n))) if rate > 0.01 else False
            m.set_opacity(0.88 if active else 0.0)
            m._t += dt
            dx = amp * np.sin(m._fr[0] * m._t + m._ph[0]) + drift[0] * (m._t % 2.0 - 1.0)
            dy = amp * np.cos(m._fr[1] * m._t + m._ph[1]) + drift[1] * (m._t % 2.0 - 1.0)
            p = m._base + np.array([dx, dy, 0.0])
            p[0] = np.clip(p[0], cx - w * 0.45, cx + w * 0.45)
            p[1] = np.clip(p[1], cy - h * 0.45, cy + h * 0.45)
            m.move_to(p)

        d.add_updater(_upd)
        dots.add(d)
    return dots


def _path_stream(pts, n_dots, seed, speed=0.22, color=GREEN, radius=0.055, rate_tracker=None):
    """Dots flowing smoothly along a polyline path."""
    rng = np.random.default_rng(seed)
    cpts = _catmull_rom(pts, 14)
    dots = VGroup()
    for i in range(n_dots):
        s0 = (i / float(n_dots)) + rng.uniform(-0.02, 0.02)
        lat = rng.uniform(-0.04, 0.04)
        d = Dot(radius=radius, color=color, fill_opacity=0.92)
        d._s0 = s0 % 1.0
        d._lat = lat
        d._idx = i
        d._t = 0.0

        def _upd(m, dt, n=n_dots):
            rate = rate_tracker.get_value() if rate_tracker is not None else 1.0
            active = m._idx < int(round(np.clip(rate, 0.0, 1.0) * n))
            m.set_opacity(0.92 if active else 0.0)
            if not active:
                return
            m._t += dt
            sf = (m._s0 + speed * (0.5 + 0.5 * rate) * m._t) % 1.0
            pos, tang = _sample_polyline(cpts, sf)
            norm = np.array([-tang[1], tang[0], 0.0])
            m.move_to(pos + norm * m._lat)

        d.add_updater(_upd)
        dots.add(d)
    return dots


def _switch_icon(label_text, color=GREY, state="question", center=ORIGIN):
    """Switch icon above the window: 'on?' / 'off?' or lit 'on' / 'off'."""
    box = RoundedRectangle(corner_radius=0.12, width=1.18, height=0.52,
                           stroke_color=color, stroke_width=2.8,
                           fill_color=color, fill_opacity=0.14 if state == "lit" else 0.05)
    txt = T(label_text, 26, color if state != "dim" else GREY)
    dot = Dot(radius=0.075, color=color if state == "lit" else GREY)
    inner = VGroup(dot, txt).arrange(RIGHT, buff=0.10).move_to(box)
    g = VGroup(box, inner).move_to(center)
    g.box, g.txt, g.dot = box, txt, dot
    return g


def _ph_gauge(ph_tracker, center=(1.55, 0.90, 0), height=1.75, show_pH1=True, schematic_only=False):
    """Vertical pH gauge driven directly by ph_tracker (pH 7 at top -> pH 1 at bottom)."""
    c = np.array(center, dtype=float)
    w = 0.28
    frame = RoundedRectangle(corner_radius=0.08, width=w, height=height,
                             stroke_color=GREY, stroke_width=2.5, fill_color=BG, fill_opacity=0.9).move_to(c)
    bot_y = c[1] - height / 2 + 0.04
    top_y = c[1] + height / 2 - 0.04
    usable = top_y - bot_y

    def _mk_fill():
        ph = float(np.clip(ph_tracker.get_value(), 0.7, 7.0))
        frac = (ph - 0.5) / 6.5
        h = max(0.08, frac * usable)
        col = MAGENTA if ph < 2.5 else (ORANGE if ph < 4.5 else BLUE)
        r = Rectangle(width=w - 0.08, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
        r.move_to([c[0], bot_y + h / 2, 0])
        return r

    bar = always_redraw(_mk_fill)
    title = T("pH", 24, TEXT).next_to(frame, UP, buff=0.12)
    g = VGroup(frame, bar, title)
    if show_pH1:
        y_mark = bot_y + ((1.0 - 0.5) / 6.5) * usable
        tick = Line([c[0] - w / 2 - 0.06, y_mark, 0], [c[0] + w / 2 + 0.06, y_mark, 0],
                    color=MAGENTA, stroke_width=3.5)
        lab = T("about pH 1", 24, MAGENTA).next_to(tick, RIGHT, buff=0.14)
        g.add(tick, lab)
    elif schematic_only:
        tick = Line([c[0] - w / 2 - 0.05, bot_y + 0.22, 0], [c[0] + w / 2 + 0.05, bot_y + 0.22, 0],
                    color=MAGENTA, stroke_width=3.0)
        g.add(tick)
    return g


def _turnstile_icon(center, radius=0.15, color=TEXT, speed_tracker=None):
    """Simple mechanical turnstile wheel (no molecular structure) rotated by speed_tracker."""
    ring = Circle(radius=radius, stroke_color=color, stroke_width=2.6, fill_color=BG, fill_opacity=0.85)
    b1 = Line(LEFT * radius * 0.9, RIGHT * radius * 0.9, color=color, stroke_width=2.8)
    b2 = Line(DOWN * radius * 0.9, UP * radius * 0.9, color=color, stroke_width=2.8)
    g = VGroup(ring, b1, b2).move_to(center)
    if speed_tracker is not None:
        def _spin(m, dt):
            spd = speed_tracker.get_value()
            if spd > 0.01:
                m.rotate(spd * 3.2 * dt)
        g.add_updater(_spin)
    return g


def _build_parietal_window(center=(-0.10, 0.92, 0), radius=1.08, rate_tracker=None,
                           show_ecl=False, window_mode="circle"):
    """Magnifying portal on the stomach body lining showing the parietal cell and lumen boundary."""
    c = np.array(center, dtype=float)
    portal_dot = Dot([-3.65, 0.85, 0], radius=0.10, color=TEXT, stroke_color=BLUE, stroke_width=2.5)

    if window_mode == "circle":
        rim = Circle(radius=radius, stroke_color=TEXT, stroke_width=3.0, fill_color=BG, fill_opacity=0.96).move_to(c)
        cell_bg = Sector(radius=radius - 0.03, start_angle=PI / 2, angle=PI,
                         arc_center=c, fill_color=BLUE, fill_opacity=0.14, stroke_width=0)
        membrane = Line(c + UP * (radius - 0.04), c + DOWN * (radius - 0.04), color=GREY, stroke_width=3.0)
        turnstile = _turnstile_icon(c + RIGHT * 0.02, radius=0.16, color=TEXT, speed_tracker=rate_tracker)
        sparse_cell = _box_swarm(c[0] - 0.48, c[1], 0.62, 1.10, 3, seed=11, color=MAGENTA, radius=0.044, amp=0.09)
        dense_lumen = _box_swarm(c[0] + 0.52, c[1], 0.68, 1.25, 34, seed=22, color=MAGENTA, radius=0.044,
                                 rate_tracker=rate_tracker, amp=0.11)
        p_top = c + np.array([-radius * 0.78, radius * 0.62, 0])
        p_bot = c + np.array([-radius * 0.78, -radius * 0.62, 0])
        conn1 = DashedLine([-3.65, 0.94, 0], p_top, color=GREY, stroke_width=2.0, dash_length=0.10)
        conn2 = DashedLine([-3.65, 0.76, 0], p_bot, color=GREY, stroke_width=2.0, dash_length=0.10)
        cell_lab = T("parietal cell", 24, TEXT).move_to(c + DOWN * (radius + 0.28))
        g = VGroup(conn1, conn2, portal_dot, rim, cell_bg, membrane, sparse_cell, dense_lumen, turnstile, cell_lab)
        g.rim, g.turnstile, g.cell_lab = rim, turnstile, cell_lab
        g.lumen_center = c + RIGHT * 0.52
        g.cell_center = c + LEFT * 0.48
        return g

    # Wide bay mode with generous clearance between ECL cell and parietal cell labels
    w, h = 3.70, 2.24
    rim = RoundedRectangle(corner_radius=0.22, width=w, height=h,
                           stroke_color=TEXT, stroke_width=2.8, fill_color=BG, fill_opacity=0.96).move_to(c)
    par_box = RoundedRectangle(corner_radius=0.16, width=1.18, height=1.28,
                               stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.15)
    par_box.move_to(c + RIGHT * 0.42 + UP * 0.16)
    turnstile = _turnstile_icon(par_box.get_right() + LEFT * 0.04, radius=0.15, color=TEXT, speed_tracker=rate_tracker)
    dense_lumen = _box_swarm(c[0] + 1.40, c[1] + 0.16, 0.54, 1.50, 26, seed=31, color=MAGENTA, radius=0.042,
                             rate_tracker=rate_tracker, amp=0.10)
    par_lab = T("parietal cell", 24, TEXT).move_to([par_box.get_center()[0] + 0.16, rim.get_bottom()[1] + 0.25, 0])

    conn1 = DashedLine([-3.65, 0.94, 0], [rim.get_left()[0], rim.get_top()[1] - 0.18, 0],
                       color=GREY, stroke_width=2.0, dash_length=0.10)
    conn2 = DashedLine([-3.65, 0.76, 0], [rim.get_left()[0], rim.get_bottom()[1] + 0.18, 0],
                       color=GREY, stroke_width=2.0, dash_length=0.10)

    g = VGroup(conn1, conn2, portal_dot, rim, par_box, dense_lumen, turnstile, par_lab)
    g.rim, g.par_box, g.turnstile, g.par_lab = rim, par_box, turnstile, par_lab
    if show_ecl:
        ecl_box = RoundedRectangle(corner_radius=0.16, width=0.88, height=0.88,
                                   stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.18)
        ecl_box.move_to(c + LEFT * 1.00 + UP * 0.18)
        ecl_lab = T("ECL cell", 24, GREY).move_to([ecl_box.get_center()[0], rim.get_bottom()[1] + 0.25, 0])
        g.add(ecl_box, ecl_lab)
        g.ecl_box, g.ecl_lab = ecl_box, ecl_lab
    return g


# ------------------------------------------------------------------ SCENE 00: Hook & Question
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.10)
        ph = ValueTracker(6.8)

        world = GutWorld(stretch=0.0, show_blood=False, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 52, seed=7, speed=0.14, color=MAGENTA, radius=0.048, rate_tracker=rate)
        self.add(world, lumen_acid)

        # Beat 1: slow wave ticks pulse on "keeping its own beat"
        self.at("keeping its own")
        self.play(world.beat_boost.animate.set_value(1.0), run_time=0.7)
        self.play(world.beat_boost.animate.set_value(0.0), run_time=0.9)

        # Beat 2: magnifying window opens on "a pump"
        self.at("a pump")
        win = _build_parietal_window(center=(-0.10, 1.04, 0), radius=1.05, rate_tracker=rate, window_mode="circle")
        gauge = _ph_gauge(ph, center=(1.75, 0.90, 0), height=1.60, show_pH1=True)
        self.play(FadeIn(win), FadeIn(gauge), run_time=0.8)

        # Beat 3: lumen fills with dense MAGENTA and pH gauge drops to "about pH 1"
        self.at("about pH 1")
        self.play(rate.animate.set_value(1.0), ph.animate.set_value(1.0), run_time=1.8)

        # Beat 4: "roughly a million times more acidic than inside the cell" -> bracket + label
        self.at("a million times")
        p_cell = win.cell_center + UP * 0.58
        p_lum = win.lumen_center + UP * 0.58
        br_l = Line(p_cell, p_cell + UP * 0.24, color=TEXT, stroke_width=2.5)
        br_r = Line(p_lum, p_lum + UP * 0.24, color=TEXT, stroke_width=2.5)
        br_top = Line(p_cell + UP * 0.24, p_lum + UP * 0.24, color=TEXT, stroke_width=2.5)
        million_lab = T("about a million-fold", 24, MAGENTA).move_to([-0.10, 2.40, 0])
        br_stem = Line([(p_cell[0] + p_lum[0]) / 2, p_cell[1] + 0.24, 0],
                       [million_lab.get_center()[0], million_lab.get_bottom()[1] - 0.08, 0],
                       color=TEXT, stroke_width=2.2)
        bracket = VGroup(br_l, br_r, br_top, br_stem)
        self.play(FadeIn(bracket), FadeIn(million_lab), run_time=0.8)

        # Beat 5: "What switches that pump on and what switches it off?" -> empty 'on?' and 'off?' switches
        self.at("What switches")
        sw_on = _switch_icon("on?", color=TEXT, state="question", center=[-0.95, 3.04, 0])
        sw_off = _switch_icon("off?", color=TEXT, state="question", center=[0.75, 3.04, 0])
        self.play(FadeIn(sw_on), FadeIn(sw_off), run_time=0.7)

        self.finish()


# ------------------------------------------------------------------ SCENE 01: Silent 2 s Title
class S01Title(NarratedScene):
    def construct(self):
        rate = ValueTracker(1.0)
        ph = ValueTracker(1.0)
        world = GutWorld(stretch=0.0, show_blood=False, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 52, seed=7, speed=0.14, color=MAGENTA, radius=0.048, rate_tracker=rate)
        win = _build_parietal_window(center=(-0.10, 1.04, 0), radius=1.05, rate_tracker=rate, window_mode="circle")
        gauge = _ph_gauge(ph, center=(1.75, 0.90, 0), height=1.60, show_pH1=True)

        sw_on = _switch_icon("on?", color=GREY, state="dim", center=[-0.95, 2.55, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.75, 2.55, 0])
        self.add(world, lumen_acid, win, gauge, sw_on, sw_off)

        title = T("Acid On, Acid Off", size=44, font=TITLE_FONT, color=TEXT).move_to([0, 3.36, 0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=3.5).next_to(title, DOWN, buff=0.10)
        self.play(FadeIn(title, shift=DOWN * 0.1), GrowFromCenter(rule), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ SCENE 02: The Parietal Pump
class S02Pump(SpokenScene):
    def construct(self):
        # Live moving stomach world inset properly scaled inside its top-right box
        inset_box = RoundedRectangle(corner_radius=0.14, width=3.15, height=2.20,
                                     stroke_color=GREY, stroke_width=2.2, fill_color=BG, fill_opacity=0.95)
        inset_box.move_to([4.60, 2.35, 0])
        inset_center = inset_box.get_center() + DOWN * 0.04
        inset_rate = ValueTracker(0.45)
        inset_world = GutWorld(stretch=0.0, show_blood=False, show_labels=False, scale=0.25, offset=inset_center)
        inset_acid = _acid_swarm(_LUMEN_CENTERLINE, 18, seed=19, speed=0.14, color=MAGENTA, radius=0.025,
                                 rate_tracker=inset_rate, scale=0.25, offset=inset_center)
        self.add(inset_box, inset_world, inset_acid)

        # Large zoomed parietal cell filling ~65% frame height on left/center
        cell_pts = [
            (-5.7, 2.55, 0), (-0.6, 2.55, 0), (-0.6, 0.95, 0), (-3.1, 0.95, 0),
            (-3.1, -0.95, 0), (-0.6, -0.95, 0), (-0.6, -2.55, 0), (-5.7, -2.55, 0),
        ]
        cell_wall = Polygon(*cell_pts, stroke_color=BLUE, stroke_width=3.8, fill_color=BLUE, fill_opacity=0.13)
        fold_lab = T("deep fold", 28, TEXT).move_to([0.20, 0.0, 0])
        cell_lab = T("parietal cell", 28, TEXT).move_to([-3.15, -3.05, 0])
        lumen_lab = T("lumen", 28, MAGENTA).move_to([1.65, 1.35, 0])
        self.add(cell_wall, fold_lab, cell_lab, lumen_lab)

        # Three stored vesicles inside cell cytoplasm, gently drifting while at rest
        ves_starts = [np.array([-4.4, 1.32, 0.0]), np.array([-4.5, 0.0, 0.0]), np.array([-4.4, -1.32, 0.0])]
        ves_targets = [np.array([-2.2, 0.95, 0.0]), np.array([-3.1, 0.0, 0.0]), np.array([-2.2, -0.95, 0.0])]
        merge_t = ValueTracker(0.0)
        spin_rate = ValueTracker(0.0)
        idle_t = ValueTracker(0.0)
        idle_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(idle_t)

        vesicles = VGroup()
        turnstiles = VGroup()
        for idx, (p0, p1) in enumerate(zip(ves_starts, ves_targets)):
            vc = Circle(radius=0.38, stroke_color=GREY, stroke_width=2.8, fill_color=BG, fill_opacity=0.9).move_to(p0)
            vc._p0, vc._p1, vc._idx = p0, p1, idx

            def _upd_ves(m, dt):
                u = merge_t.get_value()
                t = idle_t.get_value()
                drift = np.array([0.22 * np.sin(1.7 * t + m._idx * 2.1), 0.22 * np.cos(1.9 * t + m._idx * 1.4), 0.0]) * (1 - u)
                m.move_to(m._p0 * (1 - u) + m._p1 * u + drift)
                m.set_stroke(opacity=max(0.0, 1.0 - 1.5 * max(0.0, u - 0.35)))
                m.set_fill(opacity=max(0.0, 0.9 - 1.5 * max(0.0, u - 0.35)))

            vc.add_updater(_upd_ves)
            vesicles.add(vc)

            ts = _turnstile_icon(p0, radius=0.25, color=TEXT, speed_tracker=spin_rate)
            ts._p0, ts._p1, ts._idx = p0, p1, idx

            def _upd_ts(m, dt):
                u = merge_t.get_value()
                t = idle_t.get_value()
                drift = np.array([0.22 * np.sin(1.7 * t + m._idx * 2.1), 0.22 * np.cos(1.9 * t + m._idx * 1.4), 0.0]) * (1 - u)
                m.move_to(m._p0 * (1 - u) + m._p1 * u + drift)

            ts.add_updater(_upd_ts)
            turnstiles.add(ts)

        stored_lab = T("pumps, stored", 26, TEXT).move_to([-4.25, 2.18, 0])
        self.add(vesicles, turnstiles, stored_lab)

        # Beat 1b: "tucked inside" -> gentle pulse on vesicles and stored_lab during resting beat
        self.at("tucked inside")
        self.play(vesicles.animate.set_stroke(color=TEXT, width=4.2),
                  stored_lab.animate.set_color(GOLD), run_time=0.65)
        self.play(vesicles.animate.set_stroke(color=GREY, width=2.8),
                  stored_lab.animate.set_color(TEXT), run_time=0.65)

        # Beat 2: "When stimulated" -> vesicles drift to the fold and merge into its membrane
        self.at("When stimulated")
        self.play(FadeOut(stored_lab), merge_t.animate.set_value(1.0), run_time=3.5)

        # Beat 3: "swaps" -> turnstiles rotate, H+ (MAGENTA) moves out, K+ (GREY) moves in
        self.at("swaps")
        spin_rate.set_value(1.0)
        cycle_t = ValueTracker(0.0)
        cycle_t.add_updater(lambda m, dt: m.increment_value(dt * 0.65))
        self.add(cycle_t)

        swap_dots = VGroup()
        h_specs = [
            (np.array([-2.2, 1.58, 0]), np.array([-2.2, 0.38, 0])),
            (np.array([-3.75, 0.0, 0]), np.array([-2.48, 0.0, 0])),
            (np.array([-2.2, -1.58, 0]), np.array([-2.2, -0.38, 0])),
        ]
        k_specs = [
            (np.array([-1.92, 0.40, 0]), np.array([-1.92, 1.58, 0])),
            (np.array([-2.48, -0.28, 0]), np.array([-3.75, -0.28, 0])),
            (np.array([-1.92, -0.40, 0]), np.array([-1.92, -1.58, 0])),
        ]
        for phase_off in (0.0, 0.5):
            for (hp0, hp1), (kp0, kp1) in zip(h_specs, k_specs):
                hd = Dot(hp0, radius=0.105, color=MAGENTA)
                kd = Dot(kp0, radius=0.105, color=GREY)
                hd._a, hd._b, hd._off = hp0, hp1, phase_off
                kd._a, kd._b, kd._off = kp0, kp1, phase_off
                hd.add_updater(lambda m, dt: m.move_to(m._a + (m._b - m._a) * ((cycle_t.get_value() + m._off) % 1.0)))
                kd.add_updater(lambda m, dt: m.move_to(m._a + (m._b - m._a) * ((cycle_t.get_value() + m._off) % 1.0)))
                swap_dots.add(hd, kd)

        # Clean aligned legend on right well below inset_box
        h_dot_key = Dot([2.75, 0.55, 0], radius=0.09, color=MAGENTA)
        h_lab = T("hydrogen ion", 24, MAGENTA).move_to([3.00, 0.55, 0], aligned_edge=LEFT)
        k_dot_key = Dot([2.75, -0.05, 0], radius=0.09, color=GREY)
        k_lab = T("potassium", 24, GREY).move_to([3.00, -0.05, 0], aligned_edge=LEFT)
        self.add(swap_dots)
        self.play(FadeIn(h_dot_key), FadeIn(h_lab), FadeIn(k_dot_key), FadeIn(k_lab), run_time=0.6)

        # Beat 3b: ATP token flashes and fades at each turn (well clear of cell outlines)
        self.at("paid for")
        atp_badges = VGroup(
            T("ATP", 24, GOLD).move_to([-2.2, 1.92, 0]),
            T("ATP", 24, GOLD).move_to([-4.25, 0.36, 0]),
            T("ATP", 24, GOLD).move_to([-2.2, -1.92, 0]),
        )
        atp_badges.add_updater(lambda m, dt: m.set_opacity(0.22 + 0.78 * max(0.0, np.sin(PI * (cycle_t.get_value() % 1.0)))))
        self.add(atp_badges)

        # Beat 4: "Chloride follows" -> side doors open; K+ and Cl- exit; HCl accumulates inside deep fold
        self.at("Chloride follows")
        side_doors = VGroup(
            Line([-1.35, 0.95, 0], [-0.95, 0.95, 0], color=BG, stroke_width=7.0),
            Line([-1.35, -0.95, 0], [-0.95, -0.95, 0], color=BG, stroke_width=7.0),
        )
        cl_dot_key = Dot([2.75, -0.65, 0], radius=0.09, color=TEXT)
        cl_lab = T("chloride", 24, TEXT).move_to([3.00, -0.65, 0], aligned_edge=LEFT)
        cl_flow = _path_stream([(-1.15, 1.55), (-1.15, 0.42), (-0.75, 0.25)], 5, seed=41, speed=0.35, color=TEXT, radius=0.075)
        k_flow = _path_stream([(-1.25, -1.55), (-1.25, -0.42), (-0.75, -0.25)], 5, seed=42, speed=0.35, color=GREY, radius=0.075)
        hcl_rate = ValueTracker(0.25)
        # Keep HCl swarm inside [-2.85, -1.15] so it never touches fold_lab at [0.20, 0.0]
        hcl_swarm = _box_swarm(-2.05, 0.0, 1.55, 1.25, 28, seed=43, color=MAGENTA, radius=0.062, rate_tracker=hcl_rate, amp=0.11)
        hcl_lab = T("hydrochloric acid", 26, MAGENTA).move_to([2.75, -1.45, 0], aligned_edge=LEFT)
        self.add(side_doors, cl_flow, k_flow, hcl_swarm)
        self.play(FadeIn(cl_dot_key), FadeIn(cl_lab), FadeIn(hcl_lab), hcl_rate.animate.set_value(1.0), run_time=1.4)

        self.finish()


# ------------------------------------------------------------------ SCENE 03: Three Signals & Cephalic Phase
class S03Switches(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.18)
        world = GutWorld(stretch=0.0, show_blood=False, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 48, seed=51, speed=0.15, color=MAGENTA, radius=0.048, rate_tracker=rate)
        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")

        sw_on = _switch_icon("on?", color=GREY, state="dim", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])
        self.add(world, lumen_acid, win, sw_on, sw_off)

        # Beat 1a: acetylcholine docks on parietal cell
        self.at("acetylcholine")
        ach_lab = T("acetylcholine", 24, GREEN).move_to([2.30, 1.55, 0], aligned_edge=LEFT)
        ach_plug = Dot(win.par_box.get_top() + LEFT * 0.25, radius=0.09, color=GREEN)
        ach_arr = Arrow([2.18, 1.55, 0], ach_plug.get_center() + UP * 0.14 + RIGHT * 0.10,
                        buff=0.04, color=GREEN, stroke_width=3.5, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(ach_lab), GrowArrow(ach_arr), FadeIn(ach_plug), rate.animate.set_value(0.42), run_time=0.8)

        # Beat 1b: histamine puffs from ECL cell onto parietal cell
        self.at("histamine")
        his_dot_key = Dot([2.15, 0.85, 0], radius=0.07, color=GREEN)
        his_lab = T("histamine", 24, GREEN).move_to([2.30, 0.85, 0], aligned_edge=LEFT)
        his_puff = _path_stream(
            [(win.ecl_box.get_right()[0] + 0.05, win.ecl_box.get_center()[1]),
             (win.par_box.get_left()[0] - 0.05, win.par_box.get_center()[1])],
            5, seed=52, speed=0.45, color=GREEN, radius=0.055
        )
        his_arr = Arrow(win.ecl_box.get_right() + RIGHT * 0.04, win.par_box.get_left() + LEFT * 0.04,
                        buff=0.02, color=GREEN, stroke_width=3.0, max_tip_length_to_length_ratio=0.25)
        self.add(his_puff)
        self.play(FadeIn(his_dot_key), FadeIn(his_lab), GrowArrow(his_arr), rate.animate.set_value(0.68), run_time=0.8)

        # Beat 1c: gastrin docks mainly on ECL cell from outside stomach wall (clear of lumen acid)
        self.at("gastrin")
        gas_lab = T("gastrin", 24, GREEN).move_to([-4.8, -1.2, 0])
        gas_plug = Dot(win.ecl_box.get_left() + DOWN * 0.10, radius=0.09, color=GREEN)
        gas_arr = Arrow(gas_lab.get_right() + RIGHT * 0.10 + UP * 0.08, gas_plug.get_center() + LEFT * 0.08,
                        buff=0.04, color=GREEN, stroke_width=3.0, max_tip_length_to_length_ratio=0.07)
        self.play(FadeIn(gas_lab), GrowArrow(gas_arr), FadeIn(gas_plug), rate.animate.set_value(0.92), run_time=0.8)

        # Beat 2: "The vagus nerve can start acid early."
        self.at("The vagus nerve")
        vagus_pts = [(-3.0, 3.55), (-2.75, 2.75), (-2.35, 1.95), (-1.65, 1.55), (-1.02, 1.44)]
        vagus_wire = _smooth_curve(_catmull_rom(vagus_pts, 14), color=GREEN, width=4.0)
        vagus_lab = T("vagus", 24, GREEN).move_to([-2.05, 3.05, 0])
        self.play(Create(vagus_wire), FadeIn(vagus_lab), run_time=0.9)

        # Beat 3: "Sight, smell, taste, and chewing" -> 4 icons fire pulses down vagus
        self.at("Sight smell taste")
        eye = VGroup(Arc(0.22, PI * 0.2, PI * 0.6, color=TEXT, stroke_width=2.5),
                     Arc(0.22, -PI * 0.8, PI * 0.6, color=TEXT, stroke_width=2.5).shift(UP * 0.22),
                     Dot(UP * 0.11, radius=0.055, color=GREEN))
        nose = Polygon([-0.08, 0.15, 0], [0.12, -0.10, 0], [-0.08, -0.14, 0], color=TEXT, stroke_width=2.5)
        tongue = RoundedRectangle(corner_radius=0.10, width=0.30, height=0.22, color=TEXT, stroke_width=2.5)
        tooth = Polygon([-0.12, 0.14, 0], [0.12, 0.14, 0], [0.09, -0.14, 0], [0.0, -0.04, 0], [-0.09, -0.14, 0],
                        color=TEXT, stroke_width=2.5)
        icons = VGroup(eye, nose, tongue, tooth).arrange(RIGHT, buff=0.26).move_to([-4.65, 3.12, 0])
        vagus_pulses = _path_stream(vagus_pts, 6, seed=53, speed=0.55, color=GREEN, radius=0.065)
        self.add(vagus_pulses)
        self.play(FadeIn(icons), run_time=0.8)

        # Beat 4: "before food arrives" -> 'before food' tag beside empty lumen + 'on?' lights GREEN
        self.at("before food arrives")
        before_tag = T("before food", 24, ORANGE).move_to([-3.85, -2.35, 0])
        sw_on_lit = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        self.play(FadeIn(before_tag), swap(sw_on, sw_on_lit), run_time=0.7)

        self.finish()


# ------------------------------------------------------------------ SCENE 04: Gastric Phase
class S04GastricPhase(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.55)
        ph = ValueTracker(2.4)
        world = GutWorld(stretch=0.0, show_blood=True, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 50, seed=61, speed=0.14, color=MAGENTA, radius=0.046, rate_tracker=rate)
        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        gauge = _ph_gauge(ph, center=(2.35, 0.82, 0), height=1.75, show_pH1=False, schematic_only=True)
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])

        vagus_pts = [(-3.0, 3.55), (-2.75, 2.75), (-2.35, 1.95), (-1.65, 1.55), (-1.02, 1.44)]
        vagus_wire = _smooth_curve(_catmull_rom(vagus_pts, 14), color=GREEN, width=4.0)
        vagus_lab = T("vagus", 24, GREEN).move_to([-2.05, 3.05, 0])
        vagus_pulses = _path_stream(vagus_pts, 5, seed=62, speed=0.45, color=GREEN, radius=0.06)

        self.add(world, lumen_acid, win, gauge, sw_on, sw_off, vagus_wire, vagus_lab, vagus_pulses,
                 scope_tag("schematic"))

        # Beat 1: ORANGE food blobs enter and BLUE wall stretches outward
        self.at("stretches the stomach")
        food_blobs = _acid_swarm(_LUMEN_CENTERLINE[:46], 16, seed=63, speed=0.11, color=ORANGE, radius=0.11)
        stretch_lab = T("stretch", 24, BLUE).move_to([-5.78, -0.35, 0])
        self.add(food_blobs)
        self.play(world.stretch.animate.set_value(0.85), FadeIn(stretch_lab),
                  vagus_wire.animate.set_stroke(width=6.0), run_time=1.2)

        # Beat 2: "more acetylcholine"
        self.at("more acetylcholine")
        ach_pulse = Dot(win.par_box.get_top() + LEFT * 0.25, radius=0.10, color=GREEN)
        self.play(FadeIn(ach_pulse), rate.animate.set_value(0.75), run_time=0.7)

        # Beat 3: "protein" -> G cell in antrum glows GREEN when protein touches it
        self.at("protein")
        g_cell = RoundedRectangle(corner_radius=0.12, width=0.70, height=0.44,
                                  stroke_color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.20)
        g_cell.move_to([-0.85, -1.96, 0])
        g_lab = T("G cell", 24, GREEN).move_to([0.25, -3.05, 0])
        prot_frag = Dot([-1.55, -1.55, 0], radius=0.075, color=ORANGE)
        self.play(FadeIn(g_cell), FadeIn(g_lab), FadeIn(prot_frag), run_time=0.6)
        self.play(prot_frag.animate.move_to(g_cell.get_center() + UP * 0.14),
                  g_cell.animate.set_fill(opacity=0.65), run_time=0.8)

        # Beat 4: "travels in the blood" -> GREEN gastrin dots flow along blood vessel up to ECL cell
        self.at("travels in the blood")
        gastrin_stream = _path_stream(_BLOOD_PATH_PTS[4:], 10, seed=64, speed=0.36, color=GREEN, radius=0.06)
        his_puff = _path_stream(
            [(win.ecl_box.get_right()[0] + 0.05, win.ecl_box.get_center()[1]),
             (win.par_box.get_left()[0] - 0.05, win.par_box.get_center()[1])],
            5, seed=65, speed=0.48, color=GREEN, radius=0.055
        )
        self.add(gastrin_stream, his_puff)

        # Beat 5: "acid climbs" -> MAGENTA thickens, schematic pH gauge drops further
        self.at("acid climbs")
        self.play(rate.animate.set_value(1.0), ph.animate.set_value(1.1), run_time=1.3)

        self.finish()


# ------------------------------------------------------------------ SCENE 05: The One Idea
class S05Idea(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.9)
        world = GutWorld(stretch=0.4, show_blood=True, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 48, seed=71, speed=0.15, color=MAGENTA, radius=0.046, rate_tracker=rate)
        food_blobs = _acid_swarm(_LUMEN_CENTERLINE[:48], 14, seed=72, speed=0.10, color=ORANGE, radius=0.105)
        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])
        self.add(world, lumen_acid, food_blobs, win, sw_on, sw_off)

        # Beat 1: "Food arriving" -> large GREEN arrow from incoming food to parietal bay
        self.at("Food arriving")
        on_arc = CurvedArrow([-3.70, 1.85, 0], [win.rim.get_left()[0] - 0.08, 1.38, 0],
                             angle=-0.42, color=GREEN, stroke_width=6.0)
        on_lab = T("food turns on", 28, GREEN).move_to([-2.95, 2.75, 0])
        self.play(Create(on_arc), FadeIn(on_lab), run_time=1.2)

        # Beat 2: "turns it back down" -> large CYAN arc from MAGENTA acid pointing downstream (open end)
        self.at("turns it back down")
        down_pts = _catmull_rom([(-2.80, -0.55), (-1.45, -1.35), (0.55, -1.45), (1.95, -1.15)], 14)
        down_arc = _smooth_curve(down_pts, color=CYAN, width=6.5)
        down_lab = T("downstream turns down", 28, CYAN).move_to([1.15, -3.50, 0])
        self.play(Create(down_arc), FadeIn(down_lab), run_time=1.3)

        # Beat 3: "both halves" -> both arrows pulse once together
        self.at("both halves")
        self.play(on_arc.animate.set_stroke(width=9.5), down_arc.animate.set_stroke(width=10.0), run_time=0.55)
        self.play(on_arc.animate.set_stroke(width=6.0), down_arc.animate.set_stroke(width=6.5), run_time=0.55)

        self.finish()


# ------------------------------------------------------------------ SCENE 06: The Antrum Brake
class S06AntrumBrake(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.85)
        gastrin_rate = ValueTracker(0.95)
        soma_rate = ValueTracker(0.0)

        world = GutWorld(stretch=0.25, show_blood=True, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 46, seed=81, speed=0.14, color=MAGENTA, radius=0.046, rate_tracker=rate)
        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])

        # Antral G cell and D cell beside each other
        g_cell = RoundedRectangle(corner_radius=0.12, width=0.66, height=0.42,
                                  stroke_color=GREEN, stroke_width=2.8, fill_color=GREEN, fill_opacity=0.55)
        g_cell.move_to([-1.15, -1.96, 0])
        g_lab = T("G cell", 24, GREEN).move_to([-2.40, -3.05, 0])

        d_cell = RoundedRectangle(corner_radius=0.12, width=0.66, height=0.42,
                                  stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.22)
        d_cell.move_to([0.20, -1.92, 0])
        d_lab = T("D cell", 24, CYAN).move_to([0.35, -3.05, 0])

        gastrin_stream = _path_stream(_BLOOD_PATH_PTS[4:], 10, seed=82, speed=0.35, color=GREEN,
                                      radius=0.06, rate_tracker=gastrin_rate)
        self.add(world, lumen_acid, win, sw_on, sw_off, g_cell, g_lab, d_cell, d_lab, gastrin_stream)

        # Beat 1: Acid flows down to antrum & CYAN curved arrow reaches its first target (antrum)
        self.at("flows down")
        acid_down = _path_stream([(-3.55, 0.65), (-2.55, -0.95), (-0.95, -1.55), (0.20, -1.65)],
                                 8, seed=83, speed=0.36, color=MAGENTA, radius=0.065)
        cyan_arrow = CurvedArrow([-2.45, -0.60, 0], [0.15, -1.56, 0], angle=0.32, color=CYAN, stroke_width=5.5)
        self.add(acid_down)
        self.play(Create(cyan_arrow), run_time=1.0)

        # Beat 2: "release somatostatin" -> D cell puffs CYAN dots onto G cell; label sits clearly right/above arrow
        self.at("release somatostatin")
        soma_puffs = _path_stream([(0.05, -1.94), (-0.78, -1.96)], 6, seed=84, speed=0.55, color=CYAN,
                                  radius=0.06, rate_tracker=soma_rate)
        soma_lab = T("somatostatin", 24, CYAN).move_to([0.52, -1.18, 0])
        self.add(soma_puffs)
        self.play(d_cell.animate.set_fill(opacity=0.70), soma_rate.animate.set_value(1.0), FadeIn(soma_lab), run_time=0.9)

        # Beat 3: "holds back" -> G cell dims and gastrin stream slows to a trickle
        self.at("holds back")
        self.play(g_cell.animate.set_fill(opacity=0.18), gastrin_rate.animate.set_value(0.22),
                  rate.animate.set_value(0.45), run_time=1.1)

        # Beat 4: "The more acid" -> two-step loop + summary label
        self.at("The more acid")
        loop_lab = T("more acid, less gastrin", 26, CYAN).move_to([-0.95, -3.52, 0])
        self.play(FadeIn(loop_lab), run_time=0.5)
        for _ in range(2):
            self.play(d_cell.animate.set_fill(opacity=0.90), soma_rate.animate.set_value(1.0),
                      gastrin_rate.animate.set_value(0.15), run_time=0.45)
            self.play(d_cell.animate.set_fill(opacity=0.55), run_time=0.35)

        self.finish()


# ------------------------------------------------------------------ SHARED HELPER for S07 & S08
def _world_for_s07_s08(include_fat_label=True):
    """Exact shared world builder so s07 ends on the identical layout s08 PredictPause begins with."""
    rate = ValueTracker(0.55)
    world = GutWorld(stretch=0.15, show_blood=True, show_labels=True)
    lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 40, seed=91, speed=0.12, color=MAGENTA, radius=0.044, rate_tracker=rate)
    win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
    sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
    sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])

    duod_pts = [
        (1.60, -1.26), (2.15, -1.12), (3.05, -0.78), (3.72, -1.04),
        (3.92, -1.72), (3.94, -2.42),
    ]
    chyme_orange = _path_stream(duod_pts, 10, seed=92, speed=0.18, color=ORANGE, radius=0.095)
    chyme_acid = _path_stream(duod_pts, 8, seed=93, speed=0.18, color=MAGENTA, radius=0.045)
    chyme_fat = _path_stream(duod_pts, 7, seed=94, speed=0.18, color=FAT_COLOR, radius=0.068)

    s_cell = RoundedRectangle(corner_radius=0.10, width=0.34, height=0.48,
                              stroke_color=GREY, stroke_width=2.4, fill_color=GREY, fill_opacity=0.18).move_to([3.66, -1.28, 0])
    i_cell = RoundedRectangle(corner_radius=0.10, width=0.34, height=0.48,
                              stroke_color=GREY, stroke_width=2.4, fill_color=GREY, fill_opacity=0.18).move_to([3.68, -2.02, 0])
    fat_lab = T("fat", 24, FAT_COLOR).move_to([4.95, -0.75, 0])

    items = [world, lumen_acid, win, sw_on, sw_off, chyme_orange, chyme_acid, chyme_fat, s_cell, i_cell]
    if include_fat_label:
        items.append(fat_lab)
    g = VGroup(*items)
    return g, chyme_orange, chyme_acid, chyme_fat, fat_lab


# ------------------------------------------------------------------ SCENE 07: Predict
class S07Predict(SpokenScene):
    def construct(self):
        g, co, ca, cf, fat_lab = _world_for_s07_s08(include_fat_label=False)
        co.set_opacity(0.0), ca.set_opacity(0.0), cf.set_opacity(0.0)
        self.add(g)

        # Beat 1: Chyme with MAGENTA flecks and pale yellow fat crosses into duodenum
        self.at("fatty chyme")
        self.play(co.animate.set_opacity(0.92), ca.animate.set_opacity(0.90),
                  cf.animate.set_opacity(0.95), FadeIn(fat_lab), run_time=1.3)

        # Beat 2: Question card appears at top in white
        self.at("Will the duodenum")
        q = question_card("More acid, or less?", y=3.30, color=TEXT, size=34, max_w=11.0)
        self.play(FadeIn(q.question), run_time=0.7)

        self.finish()


# ------------------------------------------------------------------ SCENE 08: Predict Pause (4.5 s)
class S08Pause(PredictPause):
    QUESTION = "More acid, or less?"
    CARD = {"y": 3.30, "color": TEXT, "size": 34, "max_w": 11.0}
    SECONDS = 4.5

    def backdrop(self):
        g, _, _, _, _ = _world_for_s07_s08(include_fat_label=True)
        return g


# ------------------------------------------------------------------ SCENE 09: Duodenal Brake Answer
class S09Answer(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.65)
        world = GutWorld(stretch=0.15, show_blood=True, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 44, seed=101, speed=0.12, color=MAGENTA, radius=0.044, rate_tracker=rate)
        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])

        duod_pts = [(1.60, -1.26), (2.15, -1.12), (3.05, -0.78), (3.72, -1.04), (3.92, -1.72), (3.94, -2.42)]
        chyme_orange = _path_stream(duod_pts, 9, seed=102, speed=0.16, color=ORANGE, radius=0.09)
        chyme_acid = _path_stream(duod_pts, 8, seed=103, speed=0.16, color=MAGENTA, radius=0.045)
        chyme_fat = _path_stream(duod_pts, 7, seed=104, speed=0.16, color=FAT_COLOR, radius=0.065)

        s_cell = RoundedRectangle(corner_radius=0.10, width=0.34, height=0.48,
                                  stroke_color=GREY, stroke_width=2.4, fill_color=GREY, fill_opacity=0.20).move_to([3.66, -1.28, 0])
        i_cell = RoundedRectangle(corner_radius=0.10, width=0.34, height=0.48,
                                  stroke_color=GREY, stroke_width=2.4, fill_color=GREY, fill_opacity=0.20).move_to([3.68, -2.02, 0])
        q = question_card("More acid, or less?", y=3.30, color=TEXT, size=34, max_w=11.0)
        self.add(world, lumen_acid, win, sw_on, sw_off, chyme_orange, chyme_acid, chyme_fat, s_cell, i_cell, q)

        # Beat 1: "Less." -> question card dissolves, "Less." appears briefly
        self.at("Less")
        ans = T("Less.", 36, CYAN).move_to([0.0, 3.30, 0])
        self.play(swap(q.question, ans), run_time=0.7)

        # Beat 2: "releases secretin" -> S cell lights CYAN, releases secretin into blood vessel
        self.at("releases secretin")
        s_lab = T("S cell", 24, CYAN).move_to([5.45, -0.55, 0])
        sec_lab = T("secretin", 24, CYAN).move_to([5.45, -0.98, 0])
        sec_stream = _path_stream(_BLOOD_PATH_PTS[1:], 8, seed=105, speed=0.34, color=CYAN, radius=0.058)
        self.add(sec_stream)
        self.play(FadeOut(ans),
                  s_cell.animate.set_stroke(CYAN).set_fill(CYAN, opacity=0.65),
                  FadeIn(s_lab), FadeIn(sec_lab), run_time=0.8)

        # Beat 3: "CCK from I cells" -> I cell lights CYAN, releases CCK into blood vessel
        self.at("CCK from I cells")
        i_lab = T("I cell", 24, CYAN).move_to([5.45, -2.25, 0])
        cck_lab = T("CCK", 24, CYAN).move_to([5.45, -2.68, 0])
        cck_stream = _path_stream(_BLOOD_PATH_PTS, 8, seed=106, speed=0.32, color=CYAN, radius=0.058)
        self.add(cck_stream)
        self.play(i_cell.animate.set_stroke(CYAN).set_fill(CYAN, opacity=0.65),
                  FadeIn(i_lab), FadeIn(cck_lab), run_time=0.8)

        # Beat 4: "Both inhibit" -> turnstiles slow and MAGENTA output thins
        self.at("Both inhibit")
        self.play(rate.animate.set_value(0.22), run_time=1.3)

        # Beat 5: "probably works" -> dashed CYAN path from CCK toward antral somatostatin puff
        self.at("probably works")
        d_cell = RoundedRectangle(corner_radius=0.12, width=0.58, height=0.40,
                                  stroke_color=CYAN, stroke_width=2.5, fill_color=CYAN, fill_opacity=0.55).move_to([0.20, -1.92, 0])
        soma_lab = T("somatostatin", 24, CYAN).move_to([-0.15, -1.32, 0])
        prob_path = DashedVMobject(
            ArcBetweenPoints([2.25, -1.62, 0], [0.55, -1.92, 0], angle=-0.35, color=CYAN, stroke_width=3.5),
            num_dashes=8
        )
        prob_lab = T("probably", 24, CYAN).move_to([1.25, -2.85, 0])
        self.play(FadeIn(d_cell), Create(prob_path), FadeIn(prob_lab), FadeIn(soma_lab), run_time=1.0)

        self.finish()


# ------------------------------------------------------------------ SCENE 10: Two Downstream Brakes
class S10TwoPlaces(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.55)
        world = GutWorld(stretch=0.15, show_blood=False, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 44, seed=111, speed=0.12, color=MAGENTA, radius=0.044, rate_tracker=rate)
        duod_pts = [(1.60, -1.26), (2.15, -1.12), (3.05, -0.78), (3.72, -1.04), (3.92, -1.72), (3.94, -2.42)]
        chyme_orange = _path_stream(duod_pts, 8, seed=112, speed=0.14, color=ORANGE, radius=0.085)
        chyme_fat = _path_stream(duod_pts, 6, seed=113, speed=0.14, color=FAT_COLOR, radius=0.06)

        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off?", color=GREY, state="dim", center=[0.95, 2.48, 0])
        self.add(world, lumen_acid, chyme_orange, chyme_fat, win, sw_on, sw_off, scope_tag("schematic"))

        # Beat 1: "switches acid on" -> bright GREEN food-turns-on arrow
        self.at("switches acid on")
        on_arc = CurvedArrow([-3.70, 1.85, 0], [win.rim.get_left()[0] - 0.08, 1.38, 0],
                             angle=-0.42, color=GREEN, stroke_width=6.0)
        on_lab = T("food turns on", 26, GREEN).move_to([-2.95, 2.75, 0])
        self.play(Create(on_arc), FadeIn(on_lab), run_time=0.9)

        # Beat 2: "two places" -> CYAN downstream arrow forks to antrum (brake 1) and duodenum (brake 2)
        self.at("two places")
        stem = _smooth_curve(_catmull_rom([(-2.80, -0.55), (-1.75, -1.25), (-0.65, -1.45)], 10), color=CYAN, width=5.5)
        br1 = Arrow([-0.65, -1.45, 0], [0.05, -1.96, 0], buff=0.04, color=CYAN, stroke_width=5.0,
                    max_tip_length_to_length_ratio=0.22)
        br2 = Arrow([-0.65, -1.45, 0], [3.38, -1.45, 0], buff=0.06, color=CYAN, stroke_width=5.0,
                    max_tip_length_to_length_ratio=0.08)

        pad1 = RoundedRectangle(corner_radius=0.08, width=0.58, height=0.28,
                                stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.35).move_to([0.25, -2.14, 0])
        pad2 = RoundedRectangle(corner_radius=0.08, width=0.28, height=0.58,
                                stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.35).move_to([3.58, -1.45, 0])
        lab1 = T("brake 1", 24, CYAN).move_to([1.35, -3.05, 0])
        lab2 = T("brake 2", 24, CYAN).move_to([5.45, -0.82, 0])
        self.play(Create(stem), GrowArrow(br1), GrowArrow(br2), FadeIn(pad1), FadeIn(pad2),
                  FadeIn(lab1), FadeIn(lab2), run_time=1.2)

        # Beat 3: "Once chyme" -> duodenum pad glows, GREEN arrow dims slightly, MAGENTA thins, 'off?' lights CYAN
        self.at("Once chyme")
        sw_off_lit = _switch_icon("off", color=CYAN, state="lit", center=[0.95, 2.48, 0])
        self.play(pad2.animate.set_fill(opacity=0.90),
                  on_arc.animate.set_stroke(opacity=0.45),
                  on_lab.animate.set_opacity(0.65),
                  rate.animate.set_value(0.20),
                  swap(sw_off, sw_off_lit), run_time=1.3)

        self.finish()


# ------------------------------------------------------------------ SCENE 11: Mucus Gel, Bicarbonate & Tight Junctions
class S11Protection(SpokenScene):
    def construct(self):
        base_wall = Rectangle(width=11.4, height=0.55, stroke_color=BLUE, stroke_width=3.0,
                              fill_color=BLUE, fill_opacity=0.22).move_to([0, -2.88, 0])

        cells = VGroup()
        cell_xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        for cx in cell_xs:
            c = RoundedRectangle(corner_radius=0.14, width=1.96, height=1.80,
                                 stroke_color=GREY, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.16)
            c.move_to([cx, -1.65, 0])
            cells.add(c)
        cells_lab = T("surface cells", 26, TEXT).move_to([-4.2, -3.45, 0])
        lumen_lab = T("lumen: very acidic", 26, MAGENTA).move_to([-3.65, 3.10, 0])
        self.add(base_wall, cells, cells_lab, lumen_lab)

        rng = np.random.default_rng(121)
        gel_active = ValueTracker(0.0)
        acid_dots = VGroup()
        for i in range(64):
            x0 = rng.uniform(-5.4, 5.4)
            y_lumen = rng.uniform(1.05, 2.75)
            depth = min(1.55, rng.exponential(scale=0.35))
            y_deep = 0.90 - depth
            in_gel_candidate = (i % 4 == 0)
            y0 = y_deep if in_gel_candidate else y_lumen
            ph0 = rng.uniform(0, TAU)
            d = Dot([x0, y0, 0], radius=0.055, color=MAGENTA)
            d._base = np.array([x0, y0, 0.0])
            d._y_lumen = y_lumen
            d._y_deep = y_deep
            d._cand = in_gel_candidate
            d._ph = ph0
            d._t = 0.0

            def _upd_acid(m, dt):
                m._t += dt
                g = gel_active.get_value()
                y_tgt = m._y_deep * (1 - 0.55 * g) + m._y_lumen * (0.55 * g) if m._cand else m._y_lumen
                p = np.array([m._base[0] + 0.14 * np.sin(1.6 * m._t + m._ph),
                              y_tgt + 0.10 * np.cos(1.9 * m._t + m._ph), 0.0])
                m.move_to(p)

            d.add_updater(_upd_acid)
            acid_dots.add(d)
        self.add(acid_dots)

        # Beat 1: "secrete bicarbonate" -> pale blue-white dots rise from the surface cells
        self.at("secrete bicarbonate")
        bicarb_dots = _box_swarm(0.10, 0.0, 7.0, 1.25, 26, seed=122, color=BICARB, radius=0.058, drift=(0.0, 0.12), amp=0.14)
        bicarb_lab = T("bicarbonate", 26, BICARB).move_to([-4.15, 0.10, 0]).set_z_index(2)
        self.add(bicarb_dots)
        self.play(FadeIn(bicarb_lab), run_time=0.8)

        # Beat 2: "mucus gel" -> thick WHITE gel layer settles over surface cells, trapping bicarbonate
        self.at("mucus gel")
        gel_box = RoundedRectangle(corner_radius=0.18, width=11.4, height=1.62,
                                   stroke_color=WHITE, stroke_width=3.0, fill_color=WHITE, fill_opacity=0.16)
        gel_box.move_to([0, 0.10, 0])
        gel_lab = T("mucus gel", 28, WHITE).move_to([4.25, 0.10, 0])
        self.play(FadeIn(gel_box, shift=DOWN * 0.25), FadeIn(gel_lab), gel_active.animate.set_value(1.0), run_time=1.3)

        # Beat 3: "far less acidic" -> two-point comparison label
        self.at("far less acidic")
        surf_lab = T("surface: far less", 26, BICARB).move_to([0.0, -3.45, 0])
        self.play(FadeIn(surf_lab), run_time=0.8)

        # Beat 4: "Tight junctions" -> short GREY seals between cells glow; arrow points to seal #2, bouncer bounces off seal #2
        self.at("Tight junctions")
        seals = VGroup(*[
            RoundedRectangle(corner_radius=0.04, width=0.22, height=0.22,
                             stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.85)
            .move_to([(cell_xs[k] + cell_xs[k + 1]) / 2, -0.84, 0])
            for k in range(4)
        ])
        tj_lab = T("tight junctions", 26, TEXT).move_to([3.75, 3.10, 0])
        tj_arrow = Arrow([3.75, 2.82, 0], seals[2].get_top() + UP * 0.12,
                         buff=0.04, color=GREY, stroke_width=2.8, max_tip_length_to_length_ratio=0.08)
        self.play(FadeIn(seals), FadeIn(tj_lab), GrowArrow(tj_arrow), run_time=0.8)
        self.play(seals.animate.set_stroke(TEXT, width=4.0).set_fill(TEXT, opacity=0.95), run_time=0.45)

        self.at("leaks back in")
        # Single MAGENTA H+ dot bounces twice off glowing seal #2 at x = +1.10
        bouncer = Dot([1.10, 0.45, 0], radius=0.09, color=MAGENTA)
        self.add(bouncer)
        for _ in range(2):
            self.play(bouncer.animate.move_to([1.10, -0.66, 0]), run_time=0.42, rate_func=rush_into)
            self.play(bouncer.animate.move_to([1.10, 0.55, 0]), run_time=0.48, rate_func=rush_from)

        self.finish()


# ------------------------------------------------------------------ SCENE 12: Closing Synthesis
class S12Close(SpokenScene):
    def construct(self):
        rate = ValueTracker(0.45)
        world = GutWorld(stretch=0.15, show_blood=False, show_labels=True)
        lumen_acid = _acid_swarm(_LUMEN_CENTERLINE, 40, seed=131, speed=0.12, color=MAGENTA, radius=0.044, rate_tracker=rate)
        food_blobs = _acid_swarm(_LUMEN_CENTERLINE[:45], 12, seed=132, speed=0.11, color=ORANGE, radius=0.095)

        duod_pts = [(1.60, -1.26), (2.15, -1.12), (3.05, -0.78), (3.72, -1.04), (3.92, -1.72), (3.94, -2.42)]
        chyme_orange = _path_stream(duod_pts, 9, seed=133, speed=0.16, color=ORANGE, radius=0.085)
        chyme_acid = _path_stream(duod_pts, 7, seed=134, speed=0.16, color=MAGENTA, radius=0.042)
        chyme_fat = _path_stream(duod_pts, 6, seed=135, speed=0.16, color=FAT_COLOR, radius=0.062)

        win = _build_parietal_window(center=(0.10, 0.82, 0), rate_tracker=rate, show_ecl=True, window_mode="wide")
        sw_on = _switch_icon("on", color=GREEN, state="lit", center=[-0.75, 2.48, 0])
        sw_off = _switch_icon("off", color=CYAN, state="lit", center=[0.95, 2.48, 0])

        on_arc = CurvedArrow([-3.70, 1.85, 0], [win.rim.get_left()[0] - 0.08, 1.38, 0],
                             angle=-0.42, color=GREEN, stroke_width=5.5)
        on_lab = T("food turns on", 26, GREEN).move_to([-2.95, 2.75, 0])

        stem = _smooth_curve(_catmull_rom([(-2.80, -0.55), (-1.75, -1.25), (-0.65, -1.45)], 10), color=CYAN, width=5.0)
        br1 = Arrow([-0.65, -1.45, 0], [0.05, -1.96, 0], buff=0.04, color=CYAN, stroke_width=4.8,
                    max_tip_length_to_length_ratio=0.22)
        br2 = Arrow([-0.65, -1.45, 0], [3.38, -1.45, 0], buff=0.06, color=CYAN, stroke_width=4.8,
                    max_tip_length_to_length_ratio=0.08)
        pad1 = RoundedRectangle(corner_radius=0.08, width=0.58, height=0.28,
                                stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.45).move_to([0.25, -2.14, 0])
        pad2 = RoundedRectangle(corner_radius=0.08, width=0.28, height=0.58,
                                stroke_color=CYAN, stroke_width=2.8, fill_color=CYAN, fill_opacity=0.45).move_to([3.58, -1.45, 0])
        lab1 = T("brake 1", 24, CYAN).move_to([1.35, -3.05, 0])
        lab2 = T("brake 2", 24, CYAN).move_to([5.45, -0.82, 0])

        self.add(world, lumen_acid, food_blobs, chyme_orange, chyme_acid, chyme_fat,
                 win, sw_on, sw_off, on_arc, on_lab, stem, br1, br2, pad1, pad2, lab1, lab2,
                 scope_tag("schematic"))

        # Beat 1: "turned on" -> GREEN arrow pulses
        self.at("turned on")
        self.play(on_arc.animate.set_stroke(width=9.0), run_time=0.55)
        self.play(on_arc.animate.set_stroke(width=5.5), run_time=0.55)

        # Beat 2: "sends onward" -> forked CYAN arrow pulses
        self.at("sends onward")
        self.play(stem.animate.set_stroke(width=8.5), br1.animate.set_stroke(width=8.0),
                  br2.animate.set_stroke(width=8.0), run_time=0.55)
        self.play(stem.animate.set_stroke(width=5.0), br1.animate.set_stroke(width=4.8),
                  br2.animate.set_stroke(width=4.8), run_time=0.55)

        # Beat 3: "from the antrum" -> brake 1 pulses
        self.at("from the antrum")
        self.play(pad1.animate.set_fill(opacity=0.95), run_time=0.5)
        self.play(pad1.animate.set_fill(opacity=0.45), run_time=0.5)

        # Beat 4: "from the duodenum" -> brake 2 pulses, MAGENTA output settles to steady trickle
        self.at("from the duodenum")
        self.play(pad2.animate.set_fill(opacity=0.95), rate.animate.set_value(0.22), run_time=0.6)
        self.play(pad2.animate.set_fill(opacity=0.45), run_time=0.5)

        self.finish()


# ------------------------------------------------------------------ SCENE 13: Standard End Card
class S13End(EndCard):
    LINE = "Food switches acid on; what flows downstream switches it off."
