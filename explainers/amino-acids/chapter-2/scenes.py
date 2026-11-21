"""
Charge on the Gel, Grease in the Cell — Animation Script (scenes.py)

COLOUR MAP (one colour per concept for the entire film):
- PROTON_COLOR = GOLD (#D4A843)        : proton token
- ACID_COLOR   = #F28C38 (ORANGE)      : acid-type switch (glutamate)
- BASE_COLOR   = #5C9EFF (BLUE)        : base-type switch
- CHARGE_COLOR = TEAL (#3FB8C0)        : net charge, charge badges, charge readout, 'charge' heading
- GREASE_COLOR = #A5BA42 (OLIVE)       : greasy / hydrophobic (valine, greasy core, patch, pocket, fibers)
- WATER_COLOR  = #8CE6F2 (pale CYAN)   : water bath specks
- RBC_COLOR    = #E04856 (CRIMSON)     : red blood cell
- HB_COLOR     = #B8C4D4               : hemoglobin molecule outline
- TEXT         = #E8EAF0 (WHITE)       : labels, pole signs, O2, polar tags

ONE WORLD CARRIED THROUGH THE FILM:
A pale CYAN water bath of drifting water specks fills the stage; a horizontal electrophoresis
gel strip ('−' to '+') tracks normal vs sickle hemoglobin drift (top in s00-s01, main in s03,
left half in s07 & s13, top-left thumbnail in s08-s12); and the main stage follows the large
hemoglobin molecule (schematic) through charge loss, hydrophobic patch exposure, oxygen-release
pocket opening, fiber chaining, and red-cell sickling.

PER-SCENE CHANGES & COMPUTED DRIVERS:
- s00_link_and_question: Gel blobs drift right (v_sickle = 0.65 * v_normal) while water specks flow around the large sickle hemoglobin blob; red cell fades in with flickering crescent outline, valine chip pulses, '?' appears.
- s01_title: Standard 2 s TitleCard.
- s02_gel_charge: Red cell yields to hemoglobin blob; proton tokens lift off ORANGE glutamate switches -> '−1' badges -> morph to OLIVE valine chips ('0', 'no switch') as water specks drift past.
- s03_gel_count: Ghost '−1' badges slide into TEAL readout counting change 0 -> +2 per molecule; camera rises to gel strip where normal pulls ahead of sickle (v_S = 0.65 * v_N) toward anode (+).
- s04_polarity: Water specks cluster around ghost ORANGE glutamate ('hydrophilic') and are pushed outside a growing radial halo (r: 0 -> 1.05) around OLIVE valine ('hydrophobic').
- s05_families: Semi-transparent blob reveals seeded OLIVE core tokens settling inward ('greasy core') while ORANGE/BLUE/polar tokens line the surface facing drifting water specks.
- s06_patch: Two position-6 surface sockets morph from glutamate (water hugging) to OLIVE valine patches whose growing halos (r: 0 -> 1.12) repel water specks on both flanks.
- s07_idea: Frame splits into gel strip (left, blobs drifting) under TEAL 'charge' and hemoglobin with greasy patch (right) under OLIVE 'polarity' + round red-cell outline with '?'.
- s08_oxygen: Gel shrinks to top-left thumbnail; four O2 dots drift out; parametric contour deforms (shift_t: 0 -> 1) opening an OLIVE hydrophobic pocket whose halo pushes water specks back.
- s09_predict: Second identical deoxygenated blob slides in from right; patch and pocket pulse across water gap; question card writes across top.
- s10_hold: Silent 4.5 s PredictPause holding question card, countdown ring, bobbing blobs, alternating patch/pocket pulse, and water specks drifting through the gap.
- s11_dock: Question card fades; blob 1 docks patch-into-pocket (squeezing water gap shut), blobs 3-5 chain in sequentially, and view pulls back to three parallel rigid fiber chains.
- s12_sickle: View pulls back inside CRIMSON red cell; parametric contour deforms (sickle_t: 0 -> 1) as internal fibers lengthen into a crescent; hemolysis, inflammation, blocked vessels appear with arrows.
- s13_return: Gel grows back to left half beside crescent cell on right; TEAL '0' badge pulses, OLIVE patch & water halo pulse, gel blobs drift, and fibers inside crescent glow OLIVE.
- s14_end: Standard EndCard with exact take-home line.
"""

from bp_parts import *
import numpy as np

# ------------------------------------------------------------------ Colour Map
PROTON_COLOR = GOLD
ACID_COLOR = "#F28C38"
BASE_COLOR = "#5C9EFF"
CHARGE_COLOR = TEAL
GREASE_COLOR = "#A5BA42"
WATER_COLOR = "#8CE6F2"
RBC_COLOR = "#E04856"
HB_COLOR = "#B8C4D4"
HB_FILL = "#253145"
RBC_FILL = "#4E1B26"
GEL_FILL = "#1F293B"

# Relative gel drift speeds (normal vs sickle, schematic proportional to net negative charge)
V_NORMAL = 1.00
V_SICKLE = 0.65


# ------------------------------------------------------------------ Geometry & Physics Helpers
def hb_contour_points(cx, cy, rx, ry, shift_t=0.0, pocket_depth=0.0, patch_bump=0.0, n=96):
    """Compute smooth closed parametric contour for a hemoglobin molecule.

    shift_t in [0, 1] elongates/reshapes the tetramer (oxy -> deoxy).
    pocket_depth in [0, 1] carves a concave hydrophobic pocket at theta = pi (left flank).
    patch_bump in [0, 1] adds a matching rounded hydrophobic tab at theta = 0 (right flank).
    """
    thetas = np.linspace(0, TAU, n, endpoint=False)
    pts = []
    sx = rx * (1.0 + 0.06 * shift_t)
    sy = ry * (1.0 - 0.05 * shift_t)
    for th in thetas:
        r_mod = 1.0 + 0.045 * np.cos(4 * th)
        d_left = ((th - PI + PI) % TAU) - PI
        pocket = pocket_depth * 0.30 * np.exp(-(d_left / 0.30) ** 2)
        d_right = ((th + PI) % TAU) - PI
        bump = patch_bump * 0.14 * np.exp(-(d_right / 0.24) ** 2)
        rr = r_mod - pocket + bump
        pts.append([cx + sx * rr * np.cos(th), cy + sy * rr * np.sin(th), 0.0])
    return pts


def make_hb_blob(center=(0, 0, 0), rx=2.5, ry=1.85, shift_t=0.0, pocket_depth=0.0, patch_bump=0.0,
                 stroke_width=4.5, fill_opacity=0.92):
    cx, cy = center[0], center[1]
    pts = hb_contour_points(cx, cy, rx, ry, shift_t=shift_t, pocket_depth=pocket_depth, patch_bump=patch_bump)
    m = VMobject(stroke_color=HB_COLOR, stroke_width=stroke_width, fill_color=HB_FILL, fill_opacity=fill_opacity)
    m.set_points_as_corners(pts + [pts[0]])
    m.make_smooth()
    return m


def make_pocket_lining(cx, cy, rx, ry, shift_t=1.0, pocket_depth=1.0, stroke_width=8.0, stroke_opacity=1.0):
    """OLIVE lining tracing the concave pocket on the left flank (never filled)."""
    thetas = np.linspace(PI - 0.36, PI + 0.36, 24)
    sx = rx * (1.0 + 0.06 * shift_t)
    sy = ry * (1.0 - 0.05 * shift_t)
    pts = []
    for th in thetas:
        r_mod = 1.0 + 0.045 * np.cos(4 * th)
        d_left = ((th - PI + PI) % TAU) - PI
        pocket = pocket_depth * 0.30 * np.exp(-(d_left / 0.30) ** 2)
        rr = r_mod - pocket
        pts.append([cx + sx * rr * np.cos(th), cy + sy * rr * np.sin(th), 0.0])
    m = VMobject(stroke_color=GREASE_COLOR, stroke_width=stroke_width, stroke_opacity=stroke_opacity,
                 fill_color=GREASE_COLOR, fill_opacity=0.0)
    m.set_points_as_corners(pts)
    m.make_smooth()
    return m


def make_patch_tab(cx, cy, rx, ry, shift_t=0.0, patch_bump=1.0):
    """OLIVE protruding hydrophobic patch on the right flank."""
    thetas = np.linspace(-0.28, 0.28, 22)
    sx = rx * (1.0 + 0.06 * shift_t)
    sy = ry * (1.0 - 0.05 * shift_t)
    pts = []
    for th in thetas:
        r_mod = 1.0 + 0.045 * np.cos(4 * th)
        d_right = ((th + PI) % TAU) - PI
        bump = patch_bump * 0.14 * np.exp(-(d_right / 0.24) ** 2)
        rr = r_mod + bump
        pts.append([cx + sx * rr * np.cos(th), cy + sy * rr * np.sin(th), 0.0])
    m = VMobject(stroke_color=GREASE_COLOR, stroke_width=8.5, fill_color=GREASE_COLOR, fill_opacity=0.40)
    m.set_points_as_corners(pts + [[cx + sx * 0.88, cy, 0.0], pts[0]])
    m.make_smooth()
    return m


def rbc_contour_points(cx, cy, rx, ry, sickle_t=0.0, n=96):
    """Smooth parametric deformation from a round red cell (sickle_t=0) to a crescent sickle (sickle_t=1)."""
    thetas = np.linspace(0, TAU, n, endpoint=False)
    pts = []
    for th in thetas:
        x0 = np.cos(th)
        y0 = np.sin(th)
        x = cx + rx * x0 * (1.0 + 0.22 * sickle_t)
        pinch = 1.0 - 0.56 * sickle_t
        bow = 0.88 * ry * sickle_t * (x0 ** 2) - 0.34 * ry * sickle_t
        y = cy + ry * y0 * pinch * (1.0 - 0.28 * sickle_t * (x0 ** 2)) + bow
        pts.append([x, y, 0.0])
    return pts


def make_rbc(center=(0, 0, 0), rx=2.0, ry=2.0, sickle_t=0.0, stroke_width=5.0, fill_opacity=0.88,
             dashed=False):
    pts = rbc_contour_points(center[0], center[1], rx, ry, sickle_t=sickle_t)
    m = VMobject(stroke_color=RBC_COLOR, stroke_width=stroke_width, fill_color=RBC_FILL, fill_opacity=fill_opacity)
    m.set_points_as_corners(pts + [pts[0]])
    m.make_smooth()
    if dashed:
        m = DashedVMobject(m, num_dashes=36)
    return m


def make_crescent_fibers(cx, cy, rx_c, ry_c, sickle_t, stroke_color=GREASE_COLOR, stroke_width=6.0):
    """Build 3 rigid fibers that lie strictly inside the red-cell contour at every sickle_t."""
    half_len = 0.56 * rx_c + 0.26 * rx_c * sickle_t
    y_mid = cy - 0.20 * ry_c * sickle_t
    max_x_scale = rx_c * (1.0 + 0.22 * sickle_t)
    lines = VGroup()
    for dy in (-0.22, 0.0, 0.22):
        pts = []
        for x_rel in np.linspace(-half_len, half_len, 24):
            u = x_rel / max_x_scale
            bow = 0.68 * ry_c * sickle_t * (u ** 2)
            pts.append([cx + x_rel, y_mid + dy * (1.0 - 0.30 * sickle_t) + bow, 0.0])
        ln = VMobject(stroke_color=stroke_color, stroke_width=stroke_width, fill_opacity=0.0)
        ln.set_points_as_corners(pts)
        ln.make_smooth()
        lines.add(ln)
    return lines


def make_switch_chip(label_text, color, badge_text=None, badge_color=CHARGE_COLOR, size=24, has_proton=False):
    """Compact chip for glutamate (ORANGE) or valine (OLIVE) with optional charge badge and proton token."""
    lbl = T(label_text, size=size, color=color)
    pad_x, pad_y = 0.16, 0.10
    box = RoundedRectangle(corner_radius=0.12, width=lbl.width + 2 * pad_x, height=lbl.height + 2 * pad_y,
                           stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=0.92)
    lbl.move_to(box)
    g = VGroup(box, lbl)
    g.box = box
    g.label = lbl
    if badge_text is not None:
        bt = M(badge_text, size=max(22, size - 2), color=badge_color)
        b_box = RoundedRectangle(corner_radius=0.10, width=bt.width + 0.22, height=bt.height + 0.16,
                                 stroke_color=badge_color, stroke_width=2.0, fill_color=BG, fill_opacity=0.94)
        bt.move_to(b_box)
        badge = VGroup(b_box, bt).next_to(box, RIGHT, buff=0.10)
        g.add(badge)
        g.badge = badge
    if has_proton:
        p_circ = Circle(radius=0.22, stroke_color=PROTON_COLOR, stroke_width=2.5, fill_color=PROTON_COLOR, fill_opacity=0.88)
        p_plus = M("+", size=22, color=BG).move_to(p_circ)
        p = VGroup(p_circ, p_plus).next_to(box, UP, buff=0.08)
        g.add(p)
        g.proton = p
    return g


def indicate_chip(chip_mob, color=TEXT, scale_factor=1.12, stroke_width=5.0):
    """Pulse a switch chip's border and label without washing out the label against the box fill."""
    return AnimationGroup(
        chip_mob.box.animate(rate_func=there_and_back).scale(scale_factor).set_stroke(color=color, width=stroke_width),
        Indicate(chip_mob.label, color=color, scale_factor=scale_factor),
    )


# ------------------------------------------------------------------ Water Bath (Physical Solvent)
class WaterBath(VGroup):
    """Seeded pale CYAN water specks drifting rightward with physical deflection around obstacles & halos."""

    def __init__(self, seed=7, n=56, x_lim=(-6.25, 6.25), y_lim=(-3.35, 3.35),
                 obstacles=None, halos=None, attractors=None, avoid_boxes=None, speed_scale=1.0):
        super().__init__()
        self.rng = np.random.default_rng(seed)
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.obstacles = obstacles or []
        self.halos = halos or []
        self.attractors = attractors or []
        self.avoid_boxes = avoid_boxes or []
        self.speed_scale = speed_scale

        self.specks = []
        for _ in range(n):
            x = self.rng.uniform(x_lim[0], x_lim[1])
            y = self.rng.uniform(y_lim[0], y_lim[1])
            r = float(self.rng.uniform(0.044, 0.062))
            op = float(self.rng.uniform(0.50, 0.78))
            d = Dot([x, y, 0], radius=r, color=WATER_COLOR).set_opacity(op)
            d._vx = float(self.rng.uniform(0.30, 0.48)) * speed_scale
            d._vy = float(self.rng.uniform(-0.08, 0.08)) * speed_scale
            d._phase = float(self.rng.uniform(0, TAU))
            self._enforce_geometry(d, dt=0.0)
            self.specks.append(d)
            self.add(d)

        self.set_z_index(-2)
        self.add_updater(self._step)

    def _enforce_geometry(self, d, dt):
        x, y = d.get_center()[0], d.get_center()[1]
        w = self.x_lim[1] - self.x_lim[0]
        h = self.y_lim[1] - self.y_lim[0]
        if x > self.x_lim[1]:
            x -= w
        elif x < self.x_lim[0]:
            x += w
        if y > self.y_lim[1]:
            y -= h
        elif y < self.y_lim[0]:
            y += h

        for att_fn in self.attractors:
            acx, acy, ar = att_fn()
            if ar <= 0:
                continue
            dx, dy = acx - x, acy - y
            dist = np.hypot(dx, dy)
            if 0.25 < dist < ar:
                pull = min(0.8 * dt, 0.15)
                x += dx / dist * pull
                y += dy / dist * pull

        for obs_fn in self.obstacles:
            ocx, ocy, orx, ory = obs_fn()
            if orx <= 0 or ory <= 0:
                continue
            nx = (x - ocx) / orx
            ny = (y - ocy) / ory
            rad = np.hypot(nx, ny)
            if rad < 1.04:
                if rad < 1e-4:
                    nx, ny, rad = 0.0, 1.0, 1.0
                scale = 1.06 / rad
                x = ocx + nx * scale * orx
                y = ocy + ny * scale * ory

        for halo_fn in self.halos:
            hcx, hcy, hr = halo_fn()
            if hr <= 0:
                continue
            dx, dy = x - hcx, y - hcy
            dist = np.hypot(dx, dy)
            if dist < hr:
                if dist < 1e-4:
                    dx, dy, dist = 1.0, 0.0, 1.0
                x = hcx + dx / dist * (hr + 0.08)
                y = hcy + dy / dist * (hr + 0.08)

        for box_fn in self.avoid_boxes:
            xmin, xmax, ymin, ymax = box_fn()
            if xmin <= x <= xmax and ymin <= y <= ymax:
                dl, dr = abs(x - xmin), abs(xmax - x)
                db, dt_e = abs(y - ymin), abs(ymax - y)
                m = min(dl, dr, db, dt_e)
                if m == db:
                    y = ymin - 0.10
                elif m == dt_e:
                    y = ymax + 0.10
                elif m == dl:
                    x = xmin - 0.10
                else:
                    x = xmax + 0.10

        d.move_to([x, y, 0])

    def _step(self, mob, dt):
        if dt <= 0:
            return
        for d in self.specks:
            d._phase += 1.4 * dt
            x, y = d.get_center()[0], d.get_center()[1]
            x += d._vx * dt
            y += (d._vy + 0.06 * np.sin(d._phase)) * dt
            d.move_to([x, y, 0])
            self._enforce_geometry(d, dt)


def mob_box(mob, pad=0.18):
    """Return a callable returning (xmin, xmax, ymin, ymax) for a mobject."""
    return lambda: (
        mob.get_left()[0] - pad,
        mob.get_right()[0] + pad,
        mob.get_bottom()[1] - pad,
        mob.get_top()[1] + pad,
    )


# ------------------------------------------------------------------ Gel Strip Helper
def build_gel_strip(center=(0, 2.45, 0), width=10.4, height=1.50, progress_tracker=None,
                    show_buffer=False, show_anode=False, show_badges=False, compact=False,
                    highlight_valine=False):
    """Build the carried horizontal electrophoresis gel strip.

    Blobs drift from left well toward '+' driven by progress_tracker in [0, 1],
    with V_SICKLE = 0.65 * V_NORMAL.
    """
    cx, cy = center[0], center[1]
    tray = RoundedRectangle(corner_radius=0.16, width=width, height=height,
                            stroke_color=HB_COLOR, stroke_width=2.5, fill_color=GEL_FILL, fill_opacity=0.92)
    tray.move_to([cx, cy, 0])

    g = VGroup(tray)
    g.tray = tray

    if compact:
        minus_lbl = M("−", size=24, color=TEXT).next_to(tray, LEFT, buff=0.12)
        plus_lbl = M("+", size=24, color=TEXT).next_to(tray, RIGHT, buff=0.12)
        gel_lbl = T("gel", size=22, color=HB_COLOR).next_to(tray, DOWN, buff=0.10)
        g.add(minus_lbl, plus_lbl, gel_lbl)
        lane_dy = height * 0.22
        x_start = cx - width * 0.34
        span = width * 0.62
        p_val = progress_tracker.get_value() if progress_tracker else 0.55

        def mk_thumb_blobs():
            p = progress_tracker.get_value() if progress_tracker else p_val
            nx = x_start + span * V_NORMAL * p
            sx = x_start + span * V_SICKLE * p
            nb = RoundedRectangle(corner_radius=0.10, width=0.46, height=0.26,
                                  stroke_color=HB_COLOR, stroke_width=2.0, fill_color=HB_COLOR, fill_opacity=0.40).move_to([nx, cy + lane_dy, 0])
            sb = RoundedRectangle(corner_radius=0.10, width=0.46, height=0.26,
                                  stroke_color=HB_COLOR, stroke_width=2.0, fill_color=HB_COLOR, fill_opacity=0.30).move_to([sx, cy - lane_dy, 0])
            sv = Dot([sx + 0.14, cy - lane_dy, 0], radius=0.075, color=GREASE_COLOR)
            return VGroup(nb, sb, sv)

        blobs = always_redraw(mk_thumb_blobs) if progress_tracker else mk_thumb_blobs()
        g.add(blobs)
        g.blobs = blobs
        return g

    pole_size = 32 if width > 7 else 28
    minus_lbl = M("−", size=pole_size, color=TEXT).next_to(tray, LEFT, buff=0.18)
    plus_lbl = M("+", size=pole_size, color=GOLD if show_anode else TEXT).next_to(tray, RIGHT, buff=0.18)
    g.add(minus_lbl, plus_lbl)
    g.minus_lbl, g.plus_lbl = minus_lbl, plus_lbl

    if show_anode:
        anode = T("anode (+)", size=26, color=GOLD).next_to(tray, RIGHT, buff=0.16).shift(UP * 0.45)
        g.add(anode)
        g.anode = anode

    if show_buffer:
        buf = T("alkaline buffer", size=28, color=TEXT).next_to(tray, UP, buff=0.22)
        g.add(buf)
        g.buffer_lbl = buf

    lane_dy = height * 0.23
    x_well = cx - width * 0.40
    span = width * 0.66
    t_size = 24 if width > 7 else 22

    def mk_blobs():
        p = progress_tracker.get_value() if progress_tracker else 0.55
        nx = x_well + span * V_NORMAL * p
        sx = x_well + span * V_SICKLE * p

        n_pill = RoundedRectangle(corner_radius=0.16, width=0.72, height=0.38,
                                  stroke_color=HB_COLOR, stroke_width=2.5, fill_color=HB_FILL, fill_opacity=0.95).move_to([nx, cy + lane_dy, 0])
        n_txt = T("normal hemoglobin" if width > 7 else "normal", size=t_size, color=TEXT).next_to(n_pill, RIGHT, buff=0.14)
        if n_txt.get_right()[0] > tray.get_right()[0] - 0.18:
            n_txt.next_to(n_pill, LEFT, buff=0.14)

        s_pill = RoundedRectangle(corner_radius=0.16, width=0.72, height=0.38,
                                  stroke_color=HB_COLOR, stroke_width=2.5, fill_color=HB_FILL, fill_opacity=0.95).move_to([sx, cy - lane_dy, 0])
        s_dot = Dot(s_pill.get_center() + RIGHT * 0.16, radius=0.10 if highlight_valine else 0.08, color=GREASE_COLOR)
        s_txt = T("sickle hemoglobin" if width > 7 else "sickle", size=t_size, color=GREASE_COLOR if highlight_valine else TEXT).next_to(s_pill, RIGHT, buff=0.14)
        if s_txt.get_right()[0] > tray.get_right()[0] - 0.18:
            s_txt.next_to(s_pill, LEFT, buff=0.14)

        grp = VGroup(n_pill, n_txt, s_pill, s_dot, s_txt)
        if show_badges:
            nb = M("−", size=28, color=CHARGE_COLOR).move_to(n_pill.get_center())
            sb = M("−", size=22, color=CHARGE_COLOR).move_to(s_pill.get_center() + LEFT * 0.12)
            grp.add(nb, sb)
        return grp

    blobs = always_redraw(mk_blobs) if progress_tracker else mk_blobs()
    g.add(blobs)
    g.blobs = blobs
    return g


# ------------------------------------------------------------------ Scene 00
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        drift = ValueTracker(0.25)
        gel = build_gel_strip(center=(0, 2.50, 0), width=10.4, height=1.55, progress_tracker=drift)

        # Main stage starts with the large schematic sickle hemoglobin blob (fills stage height)
        hb_blob = make_hb_blob(center=(0.0, -0.90, 0.0), rx=2.55, ry=1.70)
        hb_lbl = T("sickle hemoglobin", size=28, color=TEXT).move_to([0.0, -0.90, 0.0])

        rbc_c = np.array([0.0, -0.95, 0.0])
        rbc = make_rbc(center=rbc_c, rx=1.80, ry=1.80, sickle_t=0.0, stroke_width=5.0)
        crescent_ghost = make_rbc(center=rbc_c, rx=1.80, ry=1.80, sickle_t=1.0, stroke_width=4.0,
                                  fill_opacity=0.0, dashed=True)
        q_mark = M("?", size=68, color=TEXT).next_to(rbc, RIGHT, buff=0.55)

        valine_chip = make_switch_chip("valine", GREASE_COLOR, size=24).move_to([-2.45, 0.65, 0.0])
        arrow_grow = ValueTracker(0.0)

        def mk_val_arrow():
            t = arrow_grow.get_value()
            if t < 0.05:
                return VMobject()
            start = valine_chip.get_top() + UP * 0.08
            dot_c = gel.blobs[3].get_center()
            diff = dot_c - start
            dist = float(np.linalg.norm(diff))
            unit = diff / max(dist, 1e-6)
            end = dot_c - unit * 0.18
            cur_end = start + (end - start) * t
            return Arrow(start, cur_end, color=GREASE_COLOR, stroke_width=3.5, buff=0.0,
                         max_tip_length_to_length_ratio=0.10)

        val_arrow = always_redraw(mk_val_arrow)
        tag = scope_tag("schematic", size=24, color=TEXT)

        water = WaterBath(
            seed=7, n=56,
            obstacles=[lambda: (0, 2.50, 5.4, 0.95), lambda: (0.0, -0.90, 2.65, 1.80)],
            avoid_boxes=[mob_box(gel.minus_lbl), mob_box(gel.plus_lbl), mob_box(tag)],
        )

        self.add(water, gel, hb_blob, hb_lbl, tag)
        self.play(drift.animate(run_time=6.8, rate_func=linear).set_value(0.68))

        self.at("cannot bend a red cell")
        water.obstacles[1] = lambda: (rbc_c[0], rbc_c[1], 1.92, 1.92)
        self.play(
            FadeOut(hb_blob, run_time=0.45),
            FadeOut(hb_lbl, run_time=0.45),
            FadeIn(rbc, scale=0.94, run_time=0.9),
            drift.animate(run_time=1.3, rate_func=linear).set_value(0.78),
        )
        self.play(FadeIn(crescent_ghost, run_time=0.4))
        self.play(FadeOut(crescent_ghost, run_time=0.4))

        self.at("that one valine")
        water.avoid_boxes.extend([mob_box(valine_chip), mob_box(q_mark)])
        self.add(val_arrow)
        self.play(
            FadeIn(valine_chip, shift=DOWN * 0.1),
            arrow_grow.animate.set_value(1.0),
            FadeIn(q_mark, scale=1.15),
            drift.animate(run_time=1.0, rate_func=linear).set_value(0.86),
            run_time=1.0,
        )
        self.play(indicate_chip(valine_chip, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.play(drift.animate(run_time=max(0.4, self.narration_s - self.elapsed()), rate_func=linear).set_value(0.92))
        self.finish()


# ------------------------------------------------------------------ Scene 01
class S01Title(TitleCard):
    LESSON = "Amino Acids: How One Side Chain Decides Everything"
    TITLE = "Charge on the Gel, Grease in the Cell"


# ------------------------------------------------------------------ Scene 02
class S02GelCharge(SpokenScene):
    def construct(self):
        cx, cy = 0.0, -0.35
        rx, ry = 3.05, 2.15
        blob = make_hb_blob(center=(cx, cy, 0), rx=rx, ry=ry)
        tag = scope_tag("schematic", size=24, color=TEXT)

        s1_pos = np.array([cx - 1.55, cy + 1.85, 0])
        s2_pos = np.array([cx + 1.55, cy + 1.85, 0])
        sock1 = Circle(radius=0.14, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(s1_pos)
        sock2 = sock1.copy().move_to(s2_pos)

        beta1 = T("beta chain", size=28, color=TEXT).move_to([cx - 1.55, cy + 0.55, 0])
        beta2 = T("beta chain", size=28, color=TEXT).move_to([cx + 1.55, cy + 0.55, 0])
        pos6_lbl = T("position 6", size=28, color=TEXT).move_to([cx, cy + 1.15, 0])

        glu1 = make_switch_chip("glutamate", ACID_COLOR, size=26, has_proton=True).next_to(sock1, UP, buff=0.14)
        glu2 = make_switch_chip("glutamate", ACID_COLOR, size=26, has_proton=True).next_to(sock2, UP, buff=0.14)

        b1_neg = M("−1", size=28, color=CHARGE_COLOR).next_to(glu1, RIGHT, buff=0.12)
        b2_neg = M("−1", size=28, color=CHARGE_COLOR).next_to(glu2, RIGHT, buff=0.12)

        val1 = make_switch_chip("valine", GREASE_COLOR, badge_text="0", badge_color=CHARGE_COLOR, size=26).move_to(glu1.get_center())
        val2 = make_switch_chip("valine", GREASE_COLOR, badge_text="0", badge_color=CHARGE_COLOR, size=26).move_to(glu2.get_center())
        nosw1 = T("no switch", size=24, color=TEXT).next_to(val1, UP, buff=0.14)
        nosw2 = T("no switch", size=24, color=TEXT).next_to(val2, UP, buff=0.14)

        water = WaterBath(
            seed=12, n=54,
            obstacles=[lambda: (cx, cy, rx + 0.14, ry + 0.14)],
            avoid_boxes=[mob_box(tag)],
        )
        self.add(water, tag)

        rbc = make_rbc(center=(0, -0.6, 0), rx=1.7, ry=1.7, sickle_t=0.0)
        self.add(rbc)
        self.play(FadeOut(rbc, scale=0.85, run_time=0.5), FadeIn(blob, scale=0.92, run_time=0.8))
        self.play(FadeIn(sock1), FadeIn(sock2), FadeIn(beta1), FadeIn(beta2), FadeIn(pos6_lbl), run_time=0.7)

        self.at("Glutamate")
        water.avoid_boxes.extend([mob_box(glu1), mob_box(glu2)])
        self.play(FadeIn(glu1, shift=DOWN * 0.15), FadeIn(glu2, shift=DOWN * 0.15), run_time=0.8)

        self.at("let go")
        p1, p2 = glu1.proton, glu2.proton
        glu1.remove(p1)
        glu2.remove(p2)
        self.add(p1, p2)
        self.play(
            p1.animate.shift(UP * 0.9 + LEFT * 0.3).set_opacity(0.0),
            p2.animate.shift(UP * 0.9 + RIGHT * 0.3).set_opacity(0.0),
            run_time=0.9,
        )
        self.remove(p1, p2)

        self.at("minus one")
        water.avoid_boxes.extend([mob_box(b1_neg), mob_box(b2_neg)])
        self.play(FadeIn(b1_neg, scale=1.15), FadeIn(b2_neg, scale=1.15), run_time=0.55)

        self.at("Valine")
        water.avoid_boxes.extend([mob_box(val1), mob_box(val2), mob_box(nosw1), mob_box(nosw2)])
        self.play(
            FadeOut(b1_neg, run_time=0.35),
            FadeOut(b2_neg, run_time=0.35),
            ReplacementTransform(glu1, val1, run_time=0.75),
            ReplacementTransform(glu2, val2, run_time=0.75),
        )
        self.play(FadeIn(nosw1, shift=UP * 0.08), FadeIn(nosw2, shift=UP * 0.08), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ Scene 03
class S03GelCount(SpokenScene):
    def construct(self):
        cx, cy = -2.35, -0.35
        rx, ry = 2.50, 1.85
        blob = make_hb_blob(center=(cx, cy, 0), rx=rx, ry=ry)
        tag = scope_tag("schematic", size=24, color=TEXT)

        s1_pos = np.array([cx - 1.25, cy + 1.58, 0])
        s2_pos = np.array([cx + 1.25, cy + 1.58, 0])
        sock1 = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(s1_pos)
        sock2 = sock1.copy().move_to(s2_pos)
        beta1 = T("beta chain", size=26, color=TEXT).move_to([cx - 1.25, cy + 0.40, 0])
        beta2 = T("beta chain", size=26, color=TEXT).move_to([cx + 1.25, cy + 0.40, 0])

        val1 = make_switch_chip("valine", GREASE_COLOR, badge_text="0", badge_color=CHARGE_COLOR, size=24).next_to(sock1, UP, buff=0.14)
        val2 = make_switch_chip("valine", GREASE_COLOR, badge_text="0", badge_color=CHARGE_COLOR, size=24).next_to(sock2, UP, buff=0.14)

        chg_val = ValueTracker(0.0)
        ro = Readout(
            [("change", lambda: chg_val.get_value(), "{:+.0f} / molecule", CHARGE_COLOR)],
            at=[3.80, 0.15, 0], widest=[2], color=CHARGE_COLOR, size=28,
        )
        ro_title = T("charge shift", size=26, color=CHARGE_COLOR).next_to(ro, UP, buff=0.18)

        water = WaterBath(
            seed=14, n=50,
            obstacles=[lambda: (cx, cy, rx + 0.14, ry + 0.14)],
            avoid_boxes=[mob_box(val1), mob_box(val2), mob_box(ro), mob_box(ro_title), mob_box(tag)],
        )

        blob_group = VGroup(blob, sock1, sock2, beta1, beta2, val1, val2)
        self.add(water, blob_group, tag)

        self.at("two beta chains")
        # Place ghost -1 badges cleanly above the valine chips so they never touch sockets or blob outline
        g1 = M("−1", size=28, color=CHARGE_COLOR).next_to(val1, UP, buff=0.22)
        g2 = M("−1", size=28, color=CHARGE_COLOR).next_to(val2, UP, buff=0.22)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(ro), FadeIn(ro_title), run_time=0.7)

        self.at("removes two negative charges")
        self.play(
            g1.animate.move_to(ro.get_center()).set_opacity(0.0),
            g2.animate.move_to(ro.get_center()).set_opacity(0.0),
            chg_val.animate.set_value(2.0),
            run_time=1.3,
        )
        self.remove(g1, g2)

        self.at("alkaline buffer")
        drift = ValueTracker(0.12)
        gel = build_gel_strip(center=(-0.35, 0.15, 0), width=9.0, height=2.9, progress_tracker=drift,
                              show_buffer=True, show_anode=False, show_badges=True, highlight_valine=True)
        water.obstacles = [lambda: (-0.35, 0.15, 4.65, 1.55)]
        water.avoid_boxes = [mob_box(gel.minus_lbl), mob_box(gel.plus_lbl), mob_box(gel.buffer_lbl), mob_box(tag)]
        self.play(FadeOut(blob_group, run_time=0.40), FadeOut(ro, run_time=0.40), FadeOut(ro_title, run_time=0.40))
        self.play(FadeIn(gel, shift=DOWN * 0.25, run_time=0.65))

        self.at("drifts toward")
        self.play(drift.animate(run_time=0.55, rate_func=linear).set_value(0.30))

        self.at("positive pole")
        anode_lbl = T("anode (+)", size=28, color=GOLD).next_to(gel.tray, RIGHT, buff=0.18).shift(UP * 0.50)
        water.avoid_boxes.append(mob_box(anode_lbl))
        self.play(
            gel.plus_lbl.animate.set_color(GOLD),
            FadeIn(anode_lbl, shift=UP * 0.1),
            drift.animate(run_time=2.5, rate_func=linear).set_value(0.68),
            run_time=2.5,
        )

        self.at("falls behind")
        self.play(drift.animate(run_time=max(0.6, self.narration_s - self.elapsed()), rate_func=linear).set_value(0.92))
        self.finish()


# ------------------------------------------------------------------ Scene 04
class S04Polarity(SpokenScene):
    def construct(self):
        cx, cy = 0.0, -0.78
        rx, ry = 2.85, 1.92
        blob = make_hb_blob(center=(cx, cy, 0), rx=rx, ry=ry)
        tag = scope_tag("schematic", size=24, color=TEXT)

        s1_pos = np.array([cx - 1.50, cy + 1.65, 0])
        s2_pos = np.array([cx + 1.50, cy + 1.65, 0])
        sock1 = Circle(radius=0.13, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(s1_pos)
        sock2 = sock1.copy().move_to(s2_pos)

        val_chip = make_switch_chip("valine", GREASE_COLOR, size=26).next_to(sock2, UP, buff=0.14)
        glu_chip = make_switch_chip("glutamate", ACID_COLOR, badge_text="−1", badge_color=CHARGE_COLOR, size=26).next_to(sock1, UP, buff=0.14)

        head = T("polarity", size=42, color=TEXT).move_to([0, HEAD_Y + 0.05, 0])
        hydrophilic_lbl = T("hydrophilic", size=28, color=ACID_COLOR).next_to(glu_chip, UP, buff=0.25)
        hydrophobic_lbl = T("hydrophobic", size=28, color=GREASE_COLOR).move_to([val_chip.get_center()[0] + 0.4, val_chip.get_center()[1] + 1.35, 0])

        halo_r = ValueTracker(0.0)
        att_r = ValueTracker(0.0)
        halo_ring = always_redraw(lambda: DashedVMobject(
            Circle(radius=max(0.05, halo_r.get_value()), stroke_color=GREASE_COLOR, stroke_width=2.5, fill_opacity=0.0),
            num_dashes=20,
        ).move_to(val_chip.get_center()).set_stroke(opacity=0.70 if halo_r.get_value() > 0.2 else 0.0))

        water = WaterBath(
            seed=19, n=62,
            obstacles=[lambda: (cx, cy, rx + 0.14, ry + 0.14)],
            halos=[lambda: (val_chip.get_center()[0], val_chip.get_center()[1], halo_r.get_value())],
            attractors=[lambda: (glu_chip.get_center()[0], glu_chip.get_center()[1], att_r.get_value())],
            avoid_boxes=[mob_box(head), mob_box(val_chip), mob_box(tag)],
        )

        self.add(water, blob, sock1, sock2, val_chip, halo_ring, tag)

        self.at("polarity")
        self.play(Write(head), run_time=0.8)

        self.at("Glutamate")
        water.avoid_boxes.extend([mob_box(glu_chip), mob_box(hydrophilic_lbl)])
        att_r.set_value(2.1)
        self.play(FadeIn(glu_chip, shift=DOWN * 0.12), run_time=0.7)

        self.at("hydrophilic")
        self.play(FadeIn(hydrophilic_lbl, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)

        self.at("Valine")
        att_r.set_value(0.0)
        water.avoid_boxes.append(mob_box(hydrophobic_lbl))
        self.play(
            FadeOut(glu_chip, run_time=0.45),
            FadeOut(hydrophilic_lbl, run_time=0.45),
            indicate_chip(val_chip, color=TEXT, scale_factor=1.12),
            halo_r.animate(run_time=1.15).set_value(1.02),
        )

        self.at("hydrophobic")
        self.play(FadeIn(hydrophobic_lbl, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ Scene 05
class S05Families(SpokenScene):
    def construct(self):
        cx, cy = 0.0, -0.20
        rx, ry = 3.15, 2.20
        blob = make_hb_blob(center=(cx, cy, 0), rx=rx, ry=ry, fill_opacity=0.30)
        tag = scope_tag("schematic", size=24, color=TEXT)

        rng = np.random.default_rng(7)
        core_targets = []
        core_tokens = VGroup()
        # Pick 9 well-spaced core positions via rejection sampling
        while len(core_targets) < 9:
            ang = rng.uniform(0, TAU)
            rr = rng.uniform(0.18, 0.95)
            tx, ty = cx + rr * 1.25 * np.cos(ang), cy + rr * 0.72 * np.sin(ang) + 0.15
            if all(np.hypot(tx - q[0], ty - q[1]) >= 0.44 for q in core_targets):
                core_targets.append(np.array([tx, ty, 0.0]))
                sx, sy = cx + rng.uniform(-2.0, 2.0), cy + rng.uniform(-1.2, 1.2)
                tok = Circle(radius=0.17, stroke_color=GREASE_COLOR, stroke_width=2.5,
                             fill_color=GREASE_COLOR, fill_opacity=0.85).move_to([sx, sy, 0.0])
                core_tokens.add(tok)

        core_lbl = T("greasy core", size=30, color=GREASE_COLOR).move_to([cx, cy - 1.25, 0])

        surf_tokens = VGroup()
        angles = np.linspace(0, TAU, 16, endpoint=False)
        for i, th in enumerate(angles):
            px = cx + (rx - 0.12) * (1 + 0.045 * np.cos(4 * th)) * np.cos(th)
            py = cy + (ry - 0.12) * (1 + 0.045 * np.cos(4 * th)) * np.sin(th)
            if i % 3 == 0:
                t = Circle(radius=0.14, stroke_color=ACID_COLOR, stroke_width=2.5,
                           fill_color=ACID_COLOR, fill_opacity=0.88).move_to([px, py, 0])
            elif i % 3 == 1:
                t = Circle(radius=0.14, stroke_color=BASE_COLOR, stroke_width=2.5,
                           fill_color=BASE_COLOR, fill_opacity=0.88).move_to([px, py, 0])
            else:
                t = Circle(radius=0.12, stroke_color=TEXT, stroke_width=2.5,
                           fill_color=TEXT, fill_opacity=0.88).move_to([px, py, 0])
            surf_tokens.add(t)

        surf_lbl = T("water-facing surface", size=30, color=TEXT).move_to([cx, HEAD_Y - 0.1, 0])

        water = WaterBath(
            seed=23, n=56,
            obstacles=[lambda: (cx, cy, rx + 0.15, ry + 0.15)],
            avoid_boxes=[mob_box(surf_lbl), mob_box(tag)],
        )

        self.add(water, blob, tag)
        self.play(FadeIn(core_tokens), run_time=0.8)

        self.at("buried in the core")
        self.play(
            *[tok.animate.move_to(pos) for tok, pos in zip(core_tokens, core_targets)],
            FadeIn(core_lbl, shift=UP * 0.1),
            run_time=1.3,
        )

        self.at("Charged and polar")
        self.play(FadeIn(surf_tokens, scale=0.85), FadeIn(surf_lbl, shift=DOWN * 0.1), run_time=1.0)

        self.at("face the water")
        self.play(Indicate(surf_lbl, color=WATER_COLOR, scale_factor=1.06), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 06
class S06Patch(SpokenScene):
    def construct(self):
        cx, cy = 0.0, -0.30
        rx, ry = 2.85, 2.00
        blob = make_hb_blob(center=(cx, cy, 0), rx=rx, ry=ry)
        tag = scope_tag("schematic", size=24, color=TEXT)

        s_left = np.array([cx - rx - 0.05, cy + 0.25, 0])
        s_right = np.array([cx + rx + 0.05, cy + 0.25, 0])
        sock_l = Circle(radius=0.14, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(s_left)
        sock_r = sock_l.copy().move_to(s_right)

        pos6_l = T("position 6", size=24, color=TEXT).move_to([cx - 1.55, cy + 0.25, 0])
        pos6_r = T("position 6", size=24, color=TEXT).move_to([cx + 1.55, cy + 0.25, 0])

        glu_l = make_switch_chip("glutamate", ACID_COLOR, size=24).next_to(sock_l, LEFT, buff=0.14)
        glu_r = make_switch_chip("glutamate", ACID_COLOR, size=24).next_to(sock_r, RIGHT, buff=0.14)

        val_l = make_switch_chip("valine", GREASE_COLOR, size=24).next_to(sock_l, LEFT, buff=0.14)
        val_r = make_switch_chip("valine", GREASE_COLOR, size=24).next_to(sock_r, RIGHT, buff=0.14)

        halo_r = ValueTracker(0.0)
        patch_lbl = T("greasy patch", size=30, color=GREASE_COLOR).move_to(
            [val_r.get_center()[0] + 0.25, val_r.get_center()[1] + 1.50, 0]
        )

        halo_ring_l = always_redraw(lambda: DashedVMobject(
            Circle(radius=max(0.05, halo_r.get_value()), stroke_color=GREASE_COLOR, stroke_width=2.5, fill_opacity=0.0),
            num_dashes=18,
        ).move_to(val_l.get_center()).set_stroke(opacity=0.60 if halo_r.get_value() > 0.2 else 0.0))
        halo_ring_r = always_redraw(lambda: DashedVMobject(
            Circle(radius=max(0.05, halo_r.get_value()), stroke_color=GREASE_COLOR, stroke_width=2.5, fill_opacity=0.0),
            num_dashes=18,
        ).move_to(val_r.get_center()).set_stroke(opacity=0.75 if halo_r.get_value() > 0.2 else 0.0))

        att_r = ValueTracker(1.8)
        water = WaterBath(
            seed=29, n=60,
            obstacles=[lambda: (cx, cy, rx + 0.14, ry + 0.14)],
            halos=[
                lambda: (val_l.get_center()[0], val_l.get_center()[1], halo_r.get_value()),
                lambda: (val_r.get_center()[0], val_r.get_center()[1], halo_r.get_value()),
            ],
            attractors=[
                lambda: (glu_l.get_center()[0], glu_l.get_center()[1], att_r.get_value()),
                lambda: (glu_r.get_center()[0], glu_r.get_center()[1], att_r.get_value()),
            ],
            avoid_boxes=[mob_box(tag)],
        )

        self.add(water, blob, sock_l, sock_r, pos6_l, pos6_r, halo_ring_l, halo_ring_r, tag)

        self.at("facing water")
        water.avoid_boxes.extend([mob_box(glu_l), mob_box(glu_r)])
        self.play(FadeIn(glu_l, scale=0.9), FadeIn(glu_r, scale=0.9), run_time=0.8)

        self.at("glutamate")
        self.play(indicate_chip(glu_l, color=TEXT), indicate_chip(glu_r, color=TEXT), run_time=0.8)

        self.at("Swap in valine")
        att_r.set_value(0.0)
        water.avoid_boxes.extend([mob_box(val_l), mob_box(val_r)])
        self.play(
            ReplacementTransform(glu_l, val_l, run_time=0.7),
            ReplacementTransform(glu_r, val_r, run_time=0.7),
            halo_r.animate(run_time=1.1).set_value(1.12),
        )

        self.at("greasy patch")
        water.avoid_boxes.append(mob_box(patch_lbl))
        self.play(indicate_chip(val_r, color=TEXT, scale_factor=1.14), FadeIn(patch_lbl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ Scene 07
class S07Idea(SpokenScene):
    def construct(self):
        drift = ValueTracker(0.20)
        gel = build_gel_strip(center=(-3.35, -0.15, 0), width=5.4, height=2.4, progress_tracker=drift,
                              show_badges=True, highlight_valine=True)

        rcx, rcy = 3.15, -0.15
        rrx, rry = 1.85, 1.38
        blob = make_hb_blob(center=(rcx, rcy, 0), rx=rrx, ry=rry, patch_bump=0.9)
        patch_tab = make_patch_tab(rcx, rcy, rrx, rry, patch_bump=0.9)

        rbc_outline = make_rbc(center=(rcx, rcy, 0), rx=2.25, ry=2.05, sickle_t=0.0,
                               stroke_width=4.0, fill_opacity=0.0)
        # Place greasy patch label cleanly below the outer red-cell ring so nothing crosses it
        patch_lbl = T("greasy patch", size=28, color=GREASE_COLOR).move_to([rcx, -2.70, 0])

        charge_head = T("charge", size=40, color=CHARGE_COLOR).move_to([-3.35, 2.55, 0])
        polarity_head = T("polarity", size=40, color=GREASE_COLOR).move_to([rcx, 2.55, 0])

        q_mark = M("?", size=56, color=TEXT).move_to([5.80, 0.25, 0])
        tag = scope_tag("schematic", size=24, color=TEXT)

        water = WaterBath(
            seed=31, n=48,
            obstacles=[lambda: (-3.35, -0.15, 2.8, 1.3), lambda: (rcx, rcy, rrx + 0.1, rry + 0.1)],
            halos=[lambda: (rcx + rrx, rcy, 0.90)],
            avoid_boxes=[mob_box(charge_head), mob_box(polarity_head), mob_box(patch_lbl),
                         mob_box(gel.minus_lbl), mob_box(gel.plus_lbl), mob_box(tag)],
        )

        self.add(water, gel, blob, patch_tab, patch_lbl, tag)

        self.at("two properties")
        self.play(FadeIn(charge_head, shift=DOWN * 0.12), FadeIn(polarity_head, shift=DOWN * 0.12), run_time=0.8)

        self.at("Charge explains")
        self.play(
            Indicate(charge_head, color=CHARGE_COLOR, scale_factor=1.10),
            drift.animate(run_time=2.6, rate_func=linear).set_value(0.85),
            run_time=2.6,
        )

        self.at("Polarity explains")
        water.avoid_boxes.append(mob_box(q_mark))
        self.play(
            Indicate(polarity_head, color=GREASE_COLOR, scale_factor=1.10),
            Indicate(patch_tab, color=GREASE_COLOR, scale_factor=1.12),
            FadeIn(rbc_outline, run_time=0.9),
            FadeIn(q_mark, scale=1.1),
            run_time=1.2,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 08
class S08Oxygen(SpokenScene):
    def construct(self):
        thumb_drift = ValueTracker(0.45)
        thumb = build_gel_strip(center=(-4.55, 2.75, 0), width=3.4, height=1.15,
                                progress_tracker=thumb_drift, compact=True)
        tag = scope_tag("schematic", size=24, color=TEXT)

        cx, cy = 0.0, -0.25
        rx, ry = 2.95, 2.05
        shift_t = ValueTracker(0.0)
        pocket_t = ValueTracker(0.0)
        halo_r = ValueTracker(0.0)

        blob = always_redraw(lambda: make_hb_blob(
            center=(cx, cy, 0), rx=rx, ry=ry,
            shift_t=shift_t.get_value(),
            pocket_depth=pocket_t.get_value(),
            patch_bump=1.0,
        ))
        patch_tab = always_redraw(lambda: make_patch_tab(cx, cy, rx, ry, shift_t=shift_t.get_value(), patch_bump=1.0))
        pocket_line = always_redraw(lambda: make_pocket_lining(
            cx, cy, rx, ry, shift_t=shift_t.get_value(), pocket_depth=pocket_t.get_value(),
            stroke_opacity=min(1.0, pocket_t.get_value() * 1.4),
        ))

        patch_lbl = T("greasy patch", size=28, color=GREASE_COLOR).move_to([cx + 3.85, cy - 1.45, 0])
        pocket_lbl = T("greasy pocket", size=28, color=GREASE_COLOR).move_to([cx - 3.85, cy - 1.45, 0])

        o2_offsets = [(-1.1, 0.7), (0.9, 0.8), (-0.8, -0.6), (1.0, -0.5)]
        o2_dots = VGroup(*[
            VGroup(
                Circle(radius=0.36, stroke_color=TEXT, stroke_width=2.0, fill_color=BG, fill_opacity=0.95),
                T("O2", size=22, color=TEXT),
            ).move_to([cx + dx, cy + dy, 0])
            for dx, dy in o2_offsets
        ])
        for d in o2_dots:
            d[1].move_to(d[0])
        o2_lbl = T("oxygen leaves", size=28, color=TEXT).move_to([0.2, 2.75, 0])

        water = WaterBath(
            seed=37, n=54,
            obstacles=[lambda: (-4.55, 2.75, 1.9, 0.75), lambda: (cx, cy, rx + 0.14, ry + 0.14)],
            halos=[
                lambda: (cx + rx * (1 + 0.06 * shift_t.get_value()), cy, 1.05),
                lambda: (cx - rx * (1 + 0.06 * shift_t.get_value()), cy, halo_r.get_value()),
            ],
            avoid_boxes=[mob_box(thumb), mob_box(patch_lbl), mob_box(tag)],
        )

        self.add(water, thumb, blob, patch_tab, pocket_line, o2_dots, patch_lbl, tag)

        self.at("gives up its oxygen")
        water.avoid_boxes.append(mob_box(o2_lbl))
        self.play(
            FadeIn(o2_lbl, shift=DOWN * 0.1),
            *[d.animate.shift(np.array([dx * 2.4, dy * 2.4 + 0.8, 0])).set_opacity(0.0)
              for d, (dx, dy) in zip(o2_dots, o2_offsets)],
            thumb_drift.animate(run_time=1.8, rate_func=linear).set_value(0.62),
            run_time=1.8,
        )
        self.remove(o2_dots)

        self.at("shape shifts")
        self.play(
            FadeOut(o2_lbl, run_time=0.5),
            shift_t.animate(run_time=1.6).set_value(1.0),
            thumb_drift.animate(run_time=1.6, rate_func=linear).set_value(0.76),
        )

        self.at("hydrophobic pocket")
        water.avoid_boxes.append(mob_box(pocket_lbl))
        self.play(
            pocket_t.animate.set_value(1.0),
            halo_r.animate.set_value(1.05),
            FadeIn(pocket_lbl, shift=UP * 0.1),
            thumb_drift.animate(run_time=1.5, rate_func=linear).set_value(0.90),
            run_time=1.5,
        )
        self.at("greasy like the patch")
        self.play(
            Indicate(pocket_lbl, color=GREASE_COLOR),
            Indicate(patch_lbl, color=GREASE_COLOR),
            thumb_drift.animate(run_time=1.0, rate_func=linear).set_value(0.98),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------ Shared Builder for s09/s10
PREDICT_QUESTION = "Patch meets pocket: what happens?"
PREDICT_CARD = {"y": 2.75, "left": -2.35, "max_w": 8.4, "size": 30}


def build_predict_world(thumb_drift=None, bob_blobs=False, pulse_sites=False):
    """Exact shared picture for end of s09_predict and all of s10_hold."""
    thumb = build_gel_strip(center=(-4.55, 2.75, 0), width=3.4, height=1.15,
                            progress_tracker=thumb_drift, compact=True)
    # Place scope_tag cleanly on bottom-left so countdown ring in bottom-right has zero overlap
    tag = T("schematic", size=24, color=TEXT).move_to([-5.60, -3.20, 0])

    rx, ry = 2.05, 1.48
    c1 = np.array([-2.65, -0.20, 0.0])
    c2 = np.array([+2.65, -0.20, 0.0])

    b1_body = make_hb_blob(center=c1, rx=rx, ry=ry, shift_t=1.0, pocket_depth=1.0, patch_bump=1.0)
    b1_patch = make_patch_tab(c1[0], c1[1], rx, ry, shift_t=1.0, patch_bump=1.0)
    b1_pocket = make_pocket_lining(c1[0], c1[1], rx, ry, shift_t=1.0, pocket_depth=1.0)
    b1 = VGroup(b1_body, b1_patch, b1_pocket)

    b2_body = make_hb_blob(center=c2, rx=rx, ry=ry, shift_t=1.0, pocket_depth=1.0, patch_bump=1.0)
    b2_patch = make_patch_tab(c2[0], c2[1], rx, ry, shift_t=1.0, patch_bump=1.0)
    b2_pocket = make_pocket_lining(c2[0], c2[1], rx, ry, shift_t=1.0, pocket_depth=1.0)
    b2 = VGroup(b2_body, b2_patch, b2_pocket)

    patch_lbl = T("greasy patch", size=28, color=GREASE_COLOR).next_to(b1, DOWN, buff=0.35)
    pocket_lbl = T("greasy pocket", size=28, color=GREASE_COLOR).next_to(b2, DOWN, buff=0.35)

    if bob_blobs:
        bob(b1, amp=0.05, speed=1.8, seed=0)
        bob(b2, amp=0.05, speed=1.8, seed=2)
    if pulse_sites:
        pulse(b1_patch, base=8.5, amp=3.0, speed=3.0)
        pulse(b2_pocket, base=8.0, amp=3.0, speed=3.0)

    water = WaterBath(
        seed=41, n=54,
        obstacles=[
            lambda: (-4.55, 2.75, 1.9, 0.75),
            lambda: (b1.get_center()[0], b1.get_center()[1], rx * 1.06, ry),
            lambda: (b2.get_center()[0], b2.get_center()[1], rx * 1.06, ry),
        ],
        halos=[
            lambda: (b1_patch.get_center()[0], b1_patch.get_center()[1], 0.65),
            lambda: (b2_pocket.get_center()[0], b2_pocket.get_center()[1], 0.65),
        ],
        avoid_boxes=[mob_box(thumb), mob_box(patch_lbl), mob_box(pocket_lbl), mob_box(tag)],
    )
    return water, thumb, b1, b2, b1_patch, b2_pocket, patch_lbl, pocket_lbl, tag


# ------------------------------------------------------------------ Scene 09
class S09Predict(SpokenScene):
    def construct(self):
        thumb_drift = ValueTracker(0.25)
        water, thumb, b1, b2, b1_patch, b2_pocket, patch_lbl, pocket_lbl, tag = build_predict_world(thumb_drift=thumb_drift)

        b1_center = b1.get_center().copy()
        b2_center = b2.get_center().copy()
        b1.move_to([0.0, -0.20, 0.0]).scale(1.25)
        b2.shift(RIGHT * 6.5)

        self.add(water, thumb, b1, tag)

        self.at("side by side")
        self.play(
            b1.animate.scale(1.0 / 1.25).move_to(b1_center),
            b2.animate.move_to(b2_center),
            thumb_drift.animate(run_time=1.8, rate_func=linear).set_value(0.45),
            run_time=1.8,
        )

        self.at("greasy patch")
        self.play(FadeIn(patch_lbl, shift=UP * 0.1), Indicate(b1_patch, color=GREASE_COLOR, scale_factor=1.15), run_time=0.9)

        self.at("greasy pocket")
        self.play(FadeIn(pocket_lbl, shift=UP * 0.1), Indicate(b2_pocket, color=GREASE_COLOR, scale_factor=1.15), run_time=0.9)

        self.at("Neither is comfortable")
        self.play(thumb_drift.animate(run_time=1.8, rate_func=linear).set_value(0.70))

        self.at("What happens")
        q = question_card(PREDICT_QUESTION, **PREDICT_CARD)
        water.avoid_boxes.append(mob_box(q))
        self.play(FadeIn(q.question, shift=DOWN * 0.1), thumb_drift.animate(run_time=1.2, rate_func=linear).set_value(0.85), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ Scene 10
class S10Hold(PredictPause):
    QUESTION = PREDICT_QUESTION
    CARD = PREDICT_CARD
    RING_AT = (5.90, -2.95, 0)
    SECONDS = 4.5

    def backdrop(self):
        thumb_drift = ValueTracker(0.45)
        water, thumb, b1, b2, b1_patch, b2_pocket, patch_lbl, pocket_lbl, tag = build_predict_world(
            thumb_drift=thumb_drift, bob_blobs=True, pulse_sites=True
        )
        thumb_drift.add_updater(lambda m, dt: m.set_value((m.get_value() + 0.09 * dt) % 1.0))
        return VGroup(water, thumb, b1, b2, patch_lbl, pocket_lbl, tag)


# ------------------------------------------------------------------ Scene 11
class S11Dock(SpokenScene):
    def construct(self):
        thumb_drift = ValueTracker(0.25)
        water, thumb, b1, b2, b1_patch, b2_pocket, patch_lbl, pocket_lbl, tag = build_predict_world(thumb_drift=thumb_drift)
        q = question_card(PREDICT_QUESTION, **PREDICT_CARD)
        self.add(water, thumb, b1, b2, patch_lbl, pocket_lbl, q, tag)

        self.play(FadeOut(q), FadeOut(patch_lbl), FadeOut(pocket_lbl), run_time=0.7)

        rx, ry = 2.05, 1.48
        step = 1.76 * rx

        def mk_deoxy_hb(pos):
            body = make_hb_blob(center=pos, rx=rx, ry=ry, shift_t=1.0, pocket_depth=1.0, patch_bump=1.0)
            pt = make_patch_tab(pos[0], pos[1], rx, ry, shift_t=1.0, patch_bump=1.0)
            pk = make_pocket_lining(pos[0], pos[1], rx, ry, shift_t=1.0, pocket_depth=1.0)
            return VGroup(body, pt, pk)

        self.at("sticks into")
        water.halos.clear()
        dock_x1 = b2.get_center()[0] - step
        self.play(
            b1.animate.move_to([dock_x1, -0.20, 0.0]),
            thumb_drift.animate(run_time=1.3, rate_func=linear).set_value(0.45),
            run_time=1.3,
        )

        self.at("docks into")
        b3 = mk_deoxy_hb([7.5, -0.20, 0.0])
        self.add(b3)
        self.play(
            b1.animate.shift(LEFT * 2.2),
            b2.animate.shift(LEFT * 2.2),
            b3.animate.move_to([b2.get_center()[0] - 2.2 + step, -0.20, 0.0]),
            thumb_drift.animate(run_time=1.2, rate_func=linear).set_value(0.60),
            run_time=1.2,
        )

        self.at("and so on")
        chain = VGroup(b1, b2, b3)
        b4 = mk_deoxy_hb([8.5, -0.20, 0.0]).scale(0.62)
        b5 = mk_deoxy_hb([10.8, -0.20, 0.0]).scale(0.62)
        self.add(b4, b5)
        self.play(
            chain.animate.scale(0.62).move_to([-2.2, -0.20, 0.0]),
            b4.animate.move_to([-2.2 + step * 0.62 * 2, -0.20, 0.0]),
            b5.animate.move_to([-2.2 + step * 0.62 * 3, -0.20, 0.0]),
            thumb_drift.animate(run_time=1.4, rate_func=linear).set_value(0.78),
            run_time=1.4,
        )

        self.at("long rigid fibers")
        full_chain = VGroup(b1, b2, b3, b4, b5)
        s_f = 0.45
        dx = step * s_f
        center_y = -0.20
        dy = 1.42
        row_mid = VGroup(*[mk_deoxy_hb([(-2 + i) * dx, center_y, 0.0]).scale(s_f) for i in range(5)])
        row_top = VGroup(*[mk_deoxy_hb([(-2 + i) * dx, center_y + dy, 0.0]).scale(s_f) for i in range(5)])
        row_bot = VGroup(*[mk_deoxy_hb([(-2 + i) * dx, center_y - dy, 0.0]).scale(s_f) for i in range(5)])
        fiber_lbl = T("rigid fiber (schematic)", size=30, color=GREASE_COLOR).move_to([0.3, -2.80, 0.0])

        water.obstacles = [
            lambda: (-4.55, 2.75, 1.9, 0.75),
            lambda: (0.0, center_y + dy, 4.6, 0.78),
            lambda: (0.0, center_y, 4.6, 0.78),
            lambda: (0.0, center_y - dy, 4.6, 0.78),
        ]
        water.avoid_boxes.append(mob_box(fiber_lbl))
        self.play(
            ReplacementTransform(full_chain, row_mid, run_time=0.9),
            FadeIn(row_top, shift=DOWN * 0.4, run_time=0.9),
            FadeIn(row_bot, shift=UP * 0.4, run_time=0.9),
            FadeIn(fiber_lbl, shift=UP * 0.1, run_time=0.8),
            thumb_drift.animate(run_time=1.2, rate_func=linear).set_value(0.95),
        )
        self.finish()


# ------------------------------------------------------------------ Scene 12
class S12Sickle(SpokenScene):
    def construct(self):
        thumb_drift = ValueTracker(0.25)
        thumb = build_gel_strip(center=(-4.55, 2.75, 0), width=3.4, height=1.15,
                                progress_tracker=thumb_drift, compact=True)
        tag = scope_tag("schematic", size=24, color=TEXT)

        sickle_t = ValueTracker(0.0)
        cell_cx = ValueTracker(0.0)
        cell_cy = -0.25
        rx_c, ry_c = 2.65, 2.15

        rbc = always_redraw(lambda: make_rbc(
            center=(cell_cx.get_value(), cell_cy, 0), rx=rx_c, ry=ry_c,
            sickle_t=sickle_t.get_value(), stroke_width=5.5, fill_opacity=0.88,
        ))
        fibers = always_redraw(lambda: make_crescent_fibers(
            cell_cx.get_value(), cell_cy, rx_c, ry_c, sickle_t.get_value(),
            stroke_color=GREASE_COLOR, stroke_width=6.0,
        ))
        sickle_lbl = T("sickled red cell", size=30, color=RBC_COLOR).move_to([-1.65, -2.85, 0.0])

        water = WaterBath(
            seed=43, n=48,
            obstacles=[lambda: (-4.55, 2.75, 1.9, 0.75), lambda: (cell_cx.get_value(), cell_cy, rx_c * 1.15, ry_c * 0.9)],
            avoid_boxes=[mob_box(thumb), mob_box(tag)],
        )

        self.add(water, thumb, rbc, fibers, tag)

        self.at("deform the red cell")
        self.play(
            sickle_t.animate.set_value(1.0),
            cell_cx.animate.set_value(-1.70),
            thumb_drift.animate(run_time=2.4, rate_func=linear).set_value(0.55),
            run_time=2.4,
        )
        water.avoid_boxes.append(mob_box(sickle_lbl))
        self.play(FadeIn(sickle_lbl, shift=UP * 0.1), run_time=0.55)

        conseq_texts = ["hemolysis", "inflammation", "blocked vessels"]
        conseq_ys = [1.05, -0.25, -1.55]
        conseq_mobs = [T(txt, size=30, color=TEXT).move_to([4.35, yy, 0.0])
                       for txt, yy in zip(conseq_texts, conseq_ys)]

        arrows = [
            Arrow([1.85, cell_cy + 0.35 * (yy - cell_cy), 0.0],
                  [m.get_left()[0] - 0.18, yy, 0.0],
                  color=TEXT, stroke_width=3.5, buff=0.0, max_tip_length_to_length_ratio=0.18)
            for m, yy in zip(conseq_mobs, conseq_ys)
        ]

        for phrase, lbl, arr in zip(["Hemolysis", "inflammation", "blocked vessels"], conseq_mobs, arrows):
            self.at(phrase)
            water.avoid_boxes.append(mob_box(lbl))
            self.play(GrowArrow(arr), FadeIn(lbl, shift=RIGHT * 0.12), run_time=0.65)

        self.play(thumb_drift.animate(run_time=max(0.4, self.narration_s - self.elapsed()), rate_func=linear).set_value(0.90))
        self.finish()


# ------------------------------------------------------------------ Scene 13
class S13Return(SpokenScene):
    def construct(self):
        drift = ValueTracker(0.18)
        gel = build_gel_strip(center=(-3.30, 1.05, 0), width=5.4, height=2.25, progress_tracker=drift,
                              show_badges=True, highlight_valine=True)
        gel_lbl = T("charge", size=32, color=CHARGE_COLOR).next_to(gel.tray, UP, buff=0.25)

        val_chip = make_switch_chip("valine", GREASE_COLOR, badge_text="0", badge_color=CHARGE_COLOR, size=28).move_to([-3.30, -1.65, 0])
        nosw_lbl = T("no switch", size=24, color=TEXT).next_to(val_chip, DOWN, buff=0.16)

        halo_r = ValueTracker(1.20)
        halo_ring = always_redraw(lambda: DashedVMobject(
            Circle(radius=halo_r.get_value(), stroke_color=GREASE_COLOR, stroke_width=2.5, fill_opacity=0.0),
            num_dashes=20,
        ).move_to(val_chip.get_center()).set_stroke(opacity=0.75))

        rcx, rcy = 3.25, -0.25
        rx_c, ry_c = 2.25, 1.85
        rbc = make_rbc(center=(rcx, rcy, 0), rx=rx_c, ry=ry_c, sickle_t=1.0, stroke_width=5.0, fill_opacity=0.88)
        fibers = make_crescent_fibers(rcx, rcy, rx_c, ry_c, 1.0, stroke_color=GREASE_COLOR, stroke_width=5.5)

        pol_lbl = T("polarity", size=32, color=GREASE_COLOR).move_to([rcx, gel_lbl.get_y(), 0])
        cell_lbl = T("sickled red cell", size=28, color=RBC_COLOR).next_to(rbc, DOWN, buff=0.35)
        tag = scope_tag("schematic", size=24, color=TEXT)

        water = WaterBath(
            seed=47, n=52,
            obstacles=[lambda: (-3.30, 1.05, 2.8, 1.25), lambda: (rcx, rcy, rx_c * 1.15, ry_c * 0.9)],
            halos=[lambda: (val_chip.get_center()[0], val_chip.get_center()[1], halo_r.get_value())],
            avoid_boxes=[mob_box(gel_lbl), mob_box(pol_lbl), mob_box(val_chip), mob_box(nosw_lbl),
                         mob_box(cell_lbl), mob_box(gel.minus_lbl), mob_box(gel.plus_lbl), mob_box(tag)],
        )

        self.add(water, gel, gel_lbl, val_chip, nosw_lbl, halo_ring, rbc, fibers, pol_lbl, cell_lbl, tag)

        self.at("read each side chain")
        self.play(Indicate(val_chip, color=TEXT, scale_factor=1.06), run_time=0.8)

        self.at("its charge")
        self.play(Indicate(val_chip.badge, color=CHARGE_COLOR, scale_factor=1.22), run_time=0.8)

        self.at("comfort in water")
        self.play(
            Indicate(val_chip.box, color=GREASE_COLOR, scale_factor=1.10),
            halo_r.animate.set_value(1.35),
            run_time=0.7,
        )
        self.play(halo_r.animate.set_value(1.20), run_time=0.5)

        self.at("The gel counted")
        self.play(
            Indicate(gel_lbl, color=CHARGE_COLOR),
            drift.animate(run_time=2.6, rate_func=linear).set_value(0.88),
            run_time=2.6,
        )

        self.at("felt the new grease")
        self.play(
            Indicate(pol_lbl, color=GREASE_COLOR),
            fibers.animate.set_stroke(color="#D4EC5A", width=9.0),
            run_time=1.0,
        )
        self.finish()


# ------------------------------------------------------------------ Scene 14
class S14End(EndCard):
    LINE = "Charge explains the gel; polarity explains the sickle."
