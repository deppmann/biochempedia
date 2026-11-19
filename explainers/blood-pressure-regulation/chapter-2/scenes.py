"""Moving the Line -- STEMhop Lesson: Regulating Arterial Pressure (Chapter 2)

COLOUR MAP (one colour per concept for the entire film):
- Pressure marker & structural focus: WHITE (#FFFFFF) / TEXT (#E8EAF0)
- Sodium (salt) dots, salt-intake dashed line, balance gaps: GOLD (#D4A843)
- Normal kidney line (y = 10 * (P - 85)) & normal crossing ring: GREEN (#83C167)
- Moved / flattened / Liddle / essential-hypertension kidney lines: MAGENTA (#E066FF)
- Blood / extracellular fluid in the circulation loop: PALE_BLUE (#7AD3EA)
- Sympathetic output / renal nerves wire: ORANGE (#FF862F)
- Vagal wire: PURPLE (#9A72AC)
- Baroreceptor stretch sensors & afferent wire: CYAN (#3FB8C0)
- Ghost clamp from Chapter 1 (s00 recap only): RED (#FC6255)
- Plot axes & tick marks: AXIS_COL (#C0C8D6)

ONE CARRIED WORLD:
- Left 65% of the frame (~70% height): Renal pressure-natriuresis plot, x = mean pressure 85..125 mmHg
  (ticks every 5), y = sodium out per day (hidden scale 0..300, no numbers), 'teaching lines' tag below.
- Right 35% of the frame: Circulation loop (brainstem, cyan sensors + afferent, purple vagal wire,
  orange sympathetic/renal-nerve wire, heart, arterioles, kidney + outlet) with pale blue blood boluses
  circulating continuously and gold salt dots entering at the top and exiting at the kidney outlet at
  rates computed from intake and the active kidney curve.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_link_and_question: Recap ghost marker slides from 106.7 to 100 along y = 10*(P-85) as ghost red
  clamp fades; then pressure ValueTracker strains right toward 114 and snaps back to 100 twice.
- s02_shift: Ghost marker tests draining at 110 (y=250>150) and piling up at 91 (y=60<150); ring at 100
  pulses; magenta line slides +10 mmHg right to y = 10*(P-95) computed from shift tracker.
- s03_shift_result: With shifted curve y = 10*(P-95), pressure ValueTracker P moves from 100 to 110 while
  vertical gold gap 150 - 10*(P-95) shrinks to 0, loop fluid thickens and salt excretion catches up to intake.
- s04_flatten: Magenta line slides back and slope ValueTracker rotates from 10 to 5 about (100, 150) giving
  y = 5*(P-70); pressure tracker slides from 110 back to 100; 'teaching lines' tag highlights.
- s05_predict: Intake ValueTracker lifts from 150 to 250; loop salt entry speeds up by 250/150; question
  card appears at top while pressure waits at 100.
- s07_answer: Green marker climbs y = 10*(P-85) from 100 to 110 (+10 bracket); magenta marker climbs
  y = 5*(P-70) from 100 to 120 (+20 bracket).
- s08_sensitivity: Magenta bracket glows; dashed green real-curve slope tracker swings from 10 to 80 about
  (100, 150) crossing y=250 near 101.25; angiotensin II and aldosterone labels drop and dim inside loop.
- s09_idea: Reset to normal green line + usual intake 150; opposing gold arrows pulse at (100, 150);
  magenta ghost line shifts +10 mmHg right and back; gold ghost intake lifts to 250 and back.
- s10_movers: Angiotensin II token, aldosterone token, and brightened orange renal-nerve wire each arrive at
  kidney while magenta ghost nudges right; natriuretic peptides from heart nudge magenta ghost left.
- s11_channel: Zoom into collecting tubule cell (65% height) + inset plot; ENaC doors move to tubule face
  and open, passing computed gold sodium stream; Liddle mutations add more open ENaC doors, raising stream rate.
- s12_liddle: Pull back with pinned open-ENaC cell icon beside kidney; magenta line shifts +12 mmHg right; loop
  fluid thickness rises first at P=100, then pressure tracker slides to new crossing (~112) as excretion matches intake.
- s13_essential: Reset to normal; three magenta dashed variants appear in sequence (shifted right y=10*(P-95),
  flattened below intake y=5*(P-85), and both y=5*(P-93)), then haze settles over them.
- s14_where_not_what: Shifted magenta line + '?' question mark; kidney, orange renal nerves, and hormone
  tokens highlight in turn in the loop while '?' remains.
- s15_close: Clear question mark; opposing balance arrows highlight 'written in salt', then magenta line +
  kidney outlet pulse together on salt out and gold intake line + top salt inlet pulse together on salt in.
"""

from bp_parts import *

# ------------------------------------------------------------------ Film Palette
MAGENTA = "#E066FF"
PALE_BLUE = "#7AD3EA"
ORANGE = "#FF862F"
PURPLE = "#9A72AC"
CYAN = "#3FB8C0"
AXIS_COL = "#C0C8D6"
TAG_COL = "#E8EAF0"

# ------------------------------------------------------------------ Equations (lesson numbers)
def kidney_normal(p):
    return 10.0 * (p - 85.0)

def kidney_shifted(p, shift=10.0):
    return 10.0 * (p - (85.0 + shift))

def kidney_flat(p):
    return 5.0 * (p - 70.0)

def kidney_pivot(p, slope, p0=100.0, y0=150.0):
    return slope * (p - p0) + y0

# ------------------------------------------------------------------ Plot Helper
PLOT_BOX = (-5.55, 1.30, -1.95, 2.25)

def clipped_segment(plot, fn, color=GREEN, width=6, dashed=False, opacity=1.0):
    """Compute exact intersections of line/curve y=fn(x) with the plot box [85..125] x [0..300]."""
    xs = np.linspace(plot.xr[0], plot.xr[1], 400)
    ys = np.array([fn(x) for x in xs], dtype=float)
    ok = (ys >= plot.yr[0] - 1e-6) & (ys <= plot.yr[1] + 1e-6)
    pts = [plot.pt(x, float(np.clip(y, plot.yr[0], plot.yr[1]))) for x, y in zip(xs[ok], ys[ok])]
    if len(pts) < 2:
        return VMobject()
    if dashed:
        p0, p1 = pts[0], pts[-1]
        return DashedLine(p0, p1, color=color, stroke_width=width, dash_length=0.16, stroke_opacity=opacity)
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners(pts)
    return m

def make_plot():
    return Plot(
        box=PLOT_BOX,
        xr=(85, 125),
        yr=(0, 300),
        xticks=[85, 90, 95, 100, 105, 110, 115, 120, 125],
        yticks=(),
        xlabel="mean pressure (mmHg)",
        ylabel="sodium out per day",
        color=AXIS_COL,
        size=24,
        label_size=28,
        stroke=4.0,
    )

def make_ring(plot, p, y, color=GREEN, radius=0.18):
    return Circle(radius=radius, color=color, stroke_width=5.0, fill_opacity=0).move_to(plot.pt(p, y))

def make_marker_static(plot, p, y, color=WHITE):
    """WHITE dot at (p, y) with vertical dashed stem to x-axis at p."""
    top = plot.pt(p, y)
    bot = plot.pt(p, 0)
    stem = DashedLine(top, bot, color=color, stroke_width=2.8, dash_length=0.1, stroke_opacity=0.85)
    tick = Triangle(color=color, fill_color=color, fill_opacity=1.0, stroke_width=0).scale(0.10).move_to(bot + UP * 0.06)
    dot = Dot(top, radius=0.12, color=color, stroke_color=BG, stroke_width=2)
    return VGroup(stem, tick, dot)

def make_marker_live(plot, p_tracker, y_fn, color=WHITE):
    def _mk():
        p = float(p_tracker.get_value())
        y = float(y_fn(p))
        return make_marker_static(plot, p, y, color=color)
    return always_redraw(_mk)

def make_intake_line(plot, y_val, color=GOLD, width=4.5, opacity=1.0, dashed=True):
    a, b = plot.pt(plot.xr[0], y_val), plot.pt(plot.xr[1], y_val)
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=width, dash_length=0.16, stroke_opacity=opacity)
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)

def teaching_tag(text="teaching lines", color=TAG_COL):
    t = T(text, size=24, color=color)
    t.move_to([-2.12, -3.30, 0])
    return t

# ------------------------------------------------------------------ Circulation Loop
class CirculationLoop(VGroup):
    """Right-side circulation loop (x ~ 1.85..6.35, y ~ -2.55..2.75) with live blood & salt flow.

    Vessel segments terminate cleanly at the borders of heart_box and kidney_box (zero straddle).
    Blood/salt boluses are hidden while inside organ boxes so no shapes sit behind organ text.
    """

    def __init__(self, intake_rate=1.0, excretion_rate=1.0, volume=1.0, nerve_bright=0.0, seed=7):
        super().__init__()
        self.intake_t = ValueTracker(intake_rate)
        self.excretion_t = ValueTracker(excretion_rate)
        self.volume_t = ValueTracker(volume)
        self.nerve_t = ValueTracker(nerve_bright)

        # Loop geometry centered at (4.55, -0.05), wide enough for interior labels
        self.cx, self.cy = 4.55, -0.05
        self.lw, self.lh = 2.60, 3.15
        self._loop_path = RoundedRectangle(corner_radius=0.72, width=self.lw, height=self.lh).move_to([self.cx, self.cy, 0])

        # Open vessel arcs that stop cleanly outside heart and kidney boxes:
        # Heart box: center [5.65, 1.38], w=1.18, h=0.68 -> x [5.06..6.24], y [1.04..1.72]
        # Kidney box: center [4.55, -1.62], w=1.60, h=0.76 -> x [3.75..5.35], y [-2.00..-1.24]
        def _vessel_parts():
            vw = 22.0 + 20.0 * max(0.0, self.volume_t.get_value() - 1.0)
            vop = 0.48 + 0.26 * min(1.0, max(0.0, self.volume_t.get_value() - 1.0))
            # Right arterial limb: heart bottom (5.85, 1.04) -> kidney right (5.35, -1.62)
            art = CubicBezier([5.85, 1.04, 0], [5.85, -0.35, 0], [5.85, -1.62, 0], [5.35, -1.62, 0])
            # Left venous limb: kidney left (3.75, -1.62) -> top arch -> heart left (5.06, 1.52)
            ven = VMobject()
            p_a = np.array([3.75, -1.62, 0.0])
            p_b = np.array([3.25, -1.00, 0.0])
            p_c = np.array([3.25, 0.90, 0.0])
            p_d = np.array([3.65, 1.52, 0.0])
            p_e = np.array([5.06, 1.52, 0.0])
            ven.set_points_smoothly([p_a, p_b, p_c, p_d, p_e])
            g = VGroup()
            for seg in (art, ven):
                lumen = seg.copy().set_stroke(PALE_BLUE, width=vw, opacity=vop)
                wall = seg.copy().set_stroke(PALE_BLUE, width=3.5, opacity=0.90)
                g.add(lumen, wall)
            return g

        self.vessels = always_redraw(_vessel_parts)

        # Brainstem boxed_label (auto-sized with generous padding, zero tight border)
        self.brain_grp = boxed_label("brainstem", TEXT, size=24, pad=0.20, stroke=2.4, fill_opacity=0.14)
        self.brain_grp.box.set_fill(BG, opacity=0.96)
        self.brain_grp.move_to([2.45, 2.38, 0])

        # Heart box (clear of all vessel strokes)
        self.heart_box = RoundedRectangle(
            corner_radius=0.20, width=1.18, height=0.68,
            stroke_color=PALE_BLUE, stroke_width=3.0, fill_color=PALE_BLUE, fill_opacity=0.18,
        ).move_to([5.65, 1.38, 0])
        self.heart_lbl = T("heart", size=24, color=TEXT).move_to(self.heart_box)
        self.heart_grp = VGroup(self.heart_box, self.heart_lbl)

        # Sensors on arterial top arch
        self.sensor_dot = Dot([3.95, 1.53, 0], radius=0.10, color=CYAN)
        self.sensor_arc = Arc(radius=0.20, start_angle=0.2, angle=PI - 0.4, arc_center=[3.95, 1.53, 0],
                              color=CYAN, stroke_width=3.5)

        # Reflex wires (stopping right at brain_grp.get_right(), clear of salt_in at x=4.65)
        br_r = self.brain_grp.get_right()
        self.afferent_wire = CubicBezier(
            [3.95, 1.73, 0], [3.85, 2.15, 0], [3.62, 2.30, 0], [br_r[0], 2.34, 0],
            color=CYAN, stroke_width=2.8, stroke_opacity=0.75,
        )
        self.vagal_wire = CubicBezier(
            [br_r[0], 2.24, 0], [4.15, 2.02, 0], [4.95, 1.98, 0], [5.48, 1.72, 0],
            color=PURPLE, stroke_width=2.8, stroke_opacity=0.75,
        )

        # Sympathetic / renal nerve wire from brainstem bottom down left side to kidney left border
        br_b = self.brain_grp.get_bottom()
        def _mk_symp():
            b = float(self.nerve_t.get_value())
            w = 2.8 + 3.8 * b
            op = 0.72 + 0.28 * b
            return CubicBezier(
                [br_b[0], br_b[1], 0], [2.42, 0.30, 0], [2.52, -1.48, 0], [3.75, -1.62, 0],
                color=ORANGE, stroke_width=w, stroke_opacity=op,
            )
        self.renal_wire = always_redraw(_mk_symp)

        # Small arteries reference point on right limb
        self.artery_pos = np.array([5.85, -0.05, 0.0])

        # Kidney box (clear of all vessel strokes)
        self.kidney_box = RoundedRectangle(
            corner_radius=0.26, width=1.60, height=0.76,
            stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.18,
        ).move_to([4.55, -1.62, 0])
        self.kidney_lbl = T("kidney", size=26, color=GREEN).move_to(self.kidney_box)
        self.kidney_grp = VGroup(self.kidney_box, self.kidney_lbl)

        # Salt intake spout (at x=4.65, entering top arch cleanly between sensors and heart)
        self.inlet_tube = Line([4.65, 2.45, 0], [4.65, 1.54, 0], color=GOLD, stroke_width=3.5, stroke_opacity=0.70)
        self.inlet_lbl = T("salt in", size=24, color=GOLD).move_to([4.65, 2.75, 0])

        # Kidney outlet (bottom of kidney down to -2.65)
        self.outlet_tube = Line([4.55, -2.00, 0], [4.55, -2.68, 0], color=GOLD, stroke_width=3.8, stroke_opacity=0.75)
        self.outlet_lbl = T("salt out", size=24, color=GOLD).move_to([5.32, -2.26, 0])

        # 26 pale blue blood boluses orbiting loop (hidden inside organ boxes)
        self.blood_dots = VGroup()
        for ph in np.linspace(0, 1, 26, endpoint=False):
            d = Dot(radius=0.12, color=PALE_BLUE, fill_opacity=0.95)
            d._ph = float(ph)
            self.blood_dots.add(d)

        # 7 GOLD salt dots entering top & 7 exiting kidney outlet
        self.inlet_dots = VGroup()
        for ph in np.linspace(0, 1, 7, endpoint=False):
            d = Dot(radius=0.10, color=GOLD, fill_opacity=0.96)
            d._ph = float(ph)
            self.inlet_dots.add(d)

        self.outlet_dots = VGroup()
        for ph in np.linspace(0, 1, 7, endpoint=False):
            d = Dot(radius=0.10, color=GOLD, fill_opacity=0.96)
            d._ph = float(ph)
            self.outlet_dots.add(d)

        # 8 GOLD salt dots circulating inside the loop
        self.loop_salt_dots = VGroup()
        for ph in np.linspace(0.04, 0.96, 8, endpoint=False):
            d = Dot(radius=0.095, color=GOLD, fill_opacity=0.92)
            d._ph = float(ph)
            self.loop_salt_dots.add(d)

        self.add(
            self.vessels,
            self.afferent_wire, self.vagal_wire, self.renal_wire,
            self.inlet_tube, self.outlet_tube,
            self.blood_dots, self.loop_salt_dots, self.inlet_dots, self.outlet_dots,
            self.sensor_dot, self.sensor_arc,
            self.brain_grp, self.heart_grp, self.kidney_grp,
            self.inlet_lbl, self.outlet_lbl,
        )
        self._place_dots(0.0)
        self.start_flow()

    @staticmethod
    def _in_box(pt, cx, cy, hw, hh):
        return (cx - hw <= pt[0] <= cx + hw) and (cy - hh <= pt[1] <= cy + hh)

    def _place_dots(self, dt):
        in_r = float(self.intake_t.get_value())
        ex_r = float(self.excretion_t.get_value())
        for d in self.blood_dots:
            d._ph = (d._ph + 0.30 * dt) % 1.0
            pt = self._loop_path.point_from_proportion(d._ph)
            d.move_to(pt)
            inside = self._in_box(pt, 5.65, 1.38, 0.62, 0.36) or self._in_box(pt, 4.55, -1.62, 0.84, 0.42)
            d.set_opacity(0.0 if inside else 0.95)
        for d in self.loop_salt_dots:
            d._ph = (d._ph + 0.30 * dt) % 1.0
            pt = self._loop_path.point_from_proportion(d._ph)
            d.move_to(pt)
            inside = self._in_box(pt, 5.65, 1.38, 0.62, 0.36) or self._in_box(pt, 4.55, -1.62, 0.84, 0.42)
            d.set_opacity(0.0 if inside else 0.92)
        for d in self.inlet_dots:
            d._ph = (d._ph + 0.78 * in_r * dt) % 1.0
            d.move_to([4.65, 2.42 - 0.88 * d._ph, 0])
        for d in self.outlet_dots:
            d._ph = (d._ph + 0.78 * max(0.14, ex_r) * dt) % 1.0
            d.move_to([4.55, -2.02 - 0.66 * d._ph, 0])
            d.set_opacity(min(1.0, 0.40 + 0.60 * ex_r))

    def start_flow(self):
        self.add_updater(lambda mob, dt: mob._place_dots(dt) if dt > 0 else None)

def build_world(p_val=100.0, intake_y=150.0, show_normal=True, normal_opacity=1.0,
                shifted=None, flattened=False, volume=1.0, ring_at=(100.0, 150.0, GREEN),
                tag_text="teaching lines", seed=7):
    P = make_plot()
    green_line = clipped_segment(P, kidney_normal, color=GREEN, width=6, opacity=normal_opacity) if show_normal else VMobject()
    intake_line = make_intake_line(P, intake_y, color=GOLD, width=4.5, dashed=True)
    ring = make_ring(P, ring_at[0], ring_at[1], color=ring_at[2]) if ring_at else VMobject()
    if shifted is not None:
        ex_fn = lambda p: kidney_shifted(p, shifted)
    elif flattened:
        ex_fn = kidney_flat
    else:
        ex_fn = kidney_normal
    loop = CirculationLoop(
        intake_rate=intake_y / 150.0,
        excretion_rate=max(0.1, ex_fn(p_val) / 150.0),
        volume=volume,
        seed=seed,
    )
    tag = teaching_tag(tag_text) if tag_text else VMobject()
    return P, green_line, intake_line, ring, loop, tag


def make_icon_doors():
    """Three small OPEN doors (gaps with gold frames) on the left face of the pinned cell icon."""
    g = VGroup()
    for i in range(3):
        g.add(Rectangle(width=0.10, height=0.14, stroke_color=GOLD, stroke_width=2.5,
                        fill_color=BG, fill_opacity=1.0).move_to([2.66, -1.95 + i * 0.20, 0]))
    return g


# ================================================================== SCENES

class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(p_val=100.0, intake_y=150.0)
        p_t = ValueTracker(100.0)
        marker = make_marker_live(P, p_t, lambda p: 150.0, color=WHITE)

        out_in_lbl = T("out = in", size=26, color=GOLD).move_to(P.pt(92.0, 222))
        p_now_lbl = always_redraw(
            lambda: T("pressure now", size=24, color=WHITE).move_to(
                P.pt(p_t.get_value() + 6.4, 115)
            )
        )

        self.add(P, green_line, intake_line, ring, marker, out_in_lbl, p_now_lbl, tag, loop)

        # Recap clamp + ghost marker sliding from 106.7 down to 100
        self.at("shed salt")
        clamp = VGroup(
            Line(loop.artery_pos + LEFT * 0.25 + UP * 0.14, loop.artery_pos + RIGHT * 0.25 + UP * 0.14, color=RED, stroke_width=5),
            Line(loop.artery_pos + LEFT * 0.25 + DOWN * 0.14, loop.artery_pos + RIGHT * 0.25 + DOWN * 0.14, color=RED, stroke_width=5),
        ).set_opacity(0.65)
        last_tag = T("last time", size=24, color=RED).next_to(clamp, LEFT, buff=0.16)
        gp = ValueTracker(106.7)
        ghost_dot = always_redraw(
            lambda: Dot(P.pt(gp.get_value(), kidney_normal(gp.get_value())), radius=0.11, color=RED, fill_opacity=0.75)
        )
        self.play(FadeIn(clamp), FadeIn(last_tag), FadeIn(ghost_dot), run_time=0.45)

        self.at("where its line met")
        self.play(gp.animate.set_value(100.0), run_time=1.35, rate_func=smooth)
        self.play(FadeOut(clamp), FadeOut(last_tag), FadeOut(ghost_dot), run_time=0.45)

        # Question + marker straining right toward 114 and snapping back twice
        self.at("how does anyone's pressure")
        q_top = T("How does pressure stay high?", size=36, color=WHITE).move_to([-1.2, 3.28, 0])
        self.play(FadeIn(q_top, shift=DOWN * 0.1), run_time=0.35)
        for _ in range(2):
            self.play(p_t.animate.set_value(114.0), run_time=0.55, rate_func=rush_from)
            self.play(p_t.animate.set_value(100.0), run_time=0.45, rate_func=smooth)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(p_val=100.0, intake_y=150.0)
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        out_in_lbl = T("out = in", size=26, color=GOLD).move_to(P.pt(92.0, 222))
        p_now_lbl = T("pressure now", size=24, color=WHITE).move_to(P.pt(106.4, 115))
        q_top = T("How does pressure stay high?", size=36, color=WHITE).move_to([-1.2, 3.28, 0])
        title = T("Moving the Line", size=44, font=TITLE_FONT, color=WHITE).move_to([-1.2, 3.28, 0])

        self.add(P, green_line, intake_line, ring, marker, out_in_lbl, p_now_lbl, tag, loop, q_top)
        self.play(swap(q_top, title, run_time=0.50))
        self.wait(1.05)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


class S02Shift(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(p_val=100.0, intake_y=150.0)
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        out_in_lbl = T("out = in", size=26, color=GOLD).move_to(P.pt(92.0, 222))
        self.add(P, green_line, intake_line, ring, marker, out_in_lbl, tag, loop)

        # On 'draining': ghost right of ring shows GOLD gap above intake, slides back
        self.at("draining")
        g_r = ValueTracker(110.0)
        gap_r = always_redraw(lambda: Line(
            P.pt(g_r.get_value(), 150.0),
            P.pt(g_r.get_value(), kidney_normal(g_r.get_value())),
            color=GOLD, stroke_width=10, stroke_opacity=0.85,
        ))
        dot_r = always_redraw(lambda: Dot(P.pt(g_r.get_value(), 150.0), radius=0.09, color=WHITE, fill_opacity=0.85))
        lost_lbl = T("salt lost", size=24, color=GOLD).move_to(P.pt(116.5, 200))
        self.add(gap_r, dot_r, lost_lbl)
        self.play(g_r.animate.set_value(100.0), FadeOut(lost_lbl, run_time=0.45), run_time=0.50, rate_func=smooth)
        self.remove(gap_r, dot_r)

        # On 'piling up': ghost left of ring shows GOLD gap below intake, slides back
        self.at("piling up")
        g_l = ValueTracker(91.0)
        gap_l = always_redraw(lambda: Line(
            P.pt(g_l.get_value(), kidney_normal(g_l.get_value())),
            P.pt(g_l.get_value(), 150.0),
            color=GOLD, stroke_width=10, stroke_opacity=0.85,
        ))
        dot_l = always_redraw(lambda: Dot(P.pt(g_l.get_value(), 150.0), radius=0.09, color=WHITE, fill_opacity=0.85))
        gain_lbl = T("salt gained", size=24, color=GOLD).move_to(P.pt(95.5, 58))
        self.add(gap_l, dot_l, gain_lbl)
        self.play(g_l.animate.set_value(100.0), FadeOut(gain_lbl, run_time=0.6), run_time=0.75, rate_func=smooth)
        self.remove(gap_l, dot_l)

        # On 'the crossing must move': ring pulses
        self.at("the crossing must move")
        self.play(ring.animate.scale(1.45).set_stroke(width=7), run_time=0.4, rate_func=there_and_back)

        # On 'shift the kidney's line': MAGENTA copy slides 10 mmHg right
        self.at("shift the kidney's line")
        shift_t = ValueTracker(0.0)
        mag_line = always_redraw(
            lambda: clipped_segment(P, lambda p: kidney_shifted(p, shift_t.get_value()), color=MAGENTA, width=6)
        )
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(103.5, 272))
        self.add(mag_line)
        self.play(
            FadeOut(out_in_lbl, run_time=0.4),
            green_line.animate.set_stroke(opacity=0.45),
            FadeIn(norm_lbl),
            shift_t.animate.set_value(10.0),
            run_time=1.8,
            rate_func=smooth,
        )
        arr = Arrow(P.pt(104.5, 195.0), P.pt(114.5, 195.0), buff=0, color=MAGENTA, stroke_width=4, tip_length=0.16)
        arr_lbl = T("10 mmHg", size=24, color=MAGENTA).move_to(P.pt(120.8, 182.0))
        self.play(FadeIn(arr), FadeIn(arr_lbl), run_time=0.45)
        self.finish()


class S03ShiftResult(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=100.0, intake_y=150.0, normal_opacity=0.45, shifted=10.0,
        )
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(103.5, 272))
        mag_line = clipped_segment(P, lambda p: kidney_shifted(p, 10.0), color=MAGENTA, width=6)
        p_t = ValueTracker(100.0)
        marker = make_marker_live(P, p_t, lambda p: 150.0, color=WHITE)
        self.add(P, green_line, mag_line, intake_line, ring, marker, norm_lbl, tag, loop)

        # Vertical GOLD bar at P=100 showing MAGENTA below GOLD intake
        self.at("excretes less sodium")
        gap_bar = always_redraw(lambda: Line(
            P.pt(p_t.get_value(), kidney_shifted(p_t.get_value(), 10.0)),
            P.pt(p_t.get_value(), 150.0),
            color=GOLD, stroke_width=10, stroke_opacity=0.9,
        ) if p_t.get_value() < 109.95 else VMobject())
        less_lbl = T("less out than in", size=24, color=GOLD).move_to(P.pt(114.0, 75))
        self.play(FadeIn(gap_bar), FadeIn(less_lbl), loop.volume_t.animate.set_value(1.55), run_time=1.0)

        # Marker slides right from 100 to 110; gap shrinks; excretion catches up
        self.at("The crossing moves to 110")
        self.play(FadeOut(less_lbl), run_time=0.35)
        loop.excretion_t.add_updater(lambda m: m.set_value(max(0.15, kidney_shifted(p_t.get_value(), 10.0) / 150.0)))
        self.play(p_t.animate.set_value(110.0), run_time=2.3, rate_func=smooth)
        loop.excretion_t.clear_updaters()
        loop.excretion_t.set_value(1.0)

        new_ring = make_ring(P, 110.0, 150.0, color=MAGENTA)
        bal_lbl = T("new balance: 110", size=26, color=MAGENTA).move_to(P.pt(119.5, 115))
        self.play(FadeIn(new_ring), FadeIn(bal_lbl), run_time=0.45)

        self.at("same intake")
        same_lbl = T("same intake", size=24, color=GOLD).move_to(P.pt(91.5, 174))
        self.play(FadeIn(same_lbl), run_time=0.45)
        self.finish()


class S04Flatten(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=110.0, intake_y=150.0, normal_opacity=0.45, shifted=10.0, volume=1.55,
        )
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(103.5, 272))
        shift_t = ValueTracker(10.0)
        slope_t = ValueTracker(10.0)
        mag_line = always_redraw(lambda: clipped_segment(
            P,
            lambda p: slope_t.get_value() * (p - (100.0 + shift_t.get_value())) + 150.0,
            color=MAGENTA, width=6,
        ))
        p_t = ValueTracker(110.0)
        marker = make_marker_live(P, p_t, lambda p: 150.0, color=WHITE)
        new_ring = make_ring(P, 110.0, 150.0, color=MAGENTA)
        bal_lbl = T("new balance: 110", size=26, color=MAGENTA).move_to(P.pt(119.5, 115))
        same_lbl = T("same intake", size=24, color=GOLD).move_to(P.pt(91.5, 174))
        self.add(P, green_line, mag_line, intake_line, ring, new_ring, marker, norm_lbl, bal_lbl, same_lbl, tag, loop)

        # Slide back and flatten about (100, 150); restore GREEN to full brightness
        self.at("tilt the line flatter")
        self.play(
            FadeOut(new_ring), FadeOut(bal_lbl), FadeOut(same_lbl),
            green_line.animate.set_stroke(opacity=1.0),
            norm_lbl.animate.move_to(P.pt(96.5, 215)),
            shift_t.animate.set_value(0.0),
            run_time=0.8, rate_func=smooth,
        )
        self.play(slope_t.animate.set_value(5.0), run_time=1.3, rate_func=smooth)
        flat_lbl = T("flatter", size=26, color=MAGENTA).move_to(P.pt(115.2, 182))
        self.play(FadeIn(flat_lbl), run_time=0.35)

        # WHITE marker slides back from 110 to 100
        self.at("At the usual intake")
        self.play(
            p_t.animate.set_value(100.0),
            loop.volume_t.animate.set_value(1.0),
            loop.excretion_t.animate.set_value(1.0),
            run_time=1.5, rate_func=smooth,
        )

        # Brighten 'teaching lines' tag
        self.at("teaching lines")
        self.play(tag.animate.set_color(GOLD).scale(1.12), run_time=0.45, rate_func=there_and_back)
        self.play(tag.animate.set_color(GOLD), run_time=0.3)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=100.0, intake_y=150.0, flattened=True,
        )
        mag_line = clipped_segment(P, kidney_flat, color=MAGENTA, width=6)
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(96.5, 215))
        flat_lbl = T("flatter", size=26, color=MAGENTA).move_to(P.pt(115.2, 182))
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        self.add(P, green_line, mag_line, intake_line, ring, marker, norm_lbl, flat_lbl, tag, loop)

        # Raise intake from 150 to 250; keep usual ghost
        self.at("raise the salt you eat")
        ghost_intake = make_intake_line(P, 150.0, color=GOLD, width=3, opacity=0.40)
        usual_lbl = T("usual", size=24, color=GOLD).move_to(P.pt(89.5, 172))
        in_y = ValueTracker(150.0)
        live_intake = always_redraw(lambda: make_intake_line(P, in_y.get_value(), color=GOLD, width=4.5))
        self.remove(intake_line)
        self.add(ghost_intake, usual_lbl, live_intake)
        self.play(
            in_y.animate.set_value(250.0),
            loop.intake_t.animate.set_value(250.0 / 150.0),
            run_time=1.8, rate_func=smooth,
        )
        more_lbl = T("more salt", size=24, color=GOLD).move_to(P.pt(89.5, 274))
        self.play(FadeIn(more_lbl), run_time=0.4)

        # Question card at top in WHITE (matches S06Pause)
        self.at("Which kidney lets pressure")
        q = question_card("Which line climbs further?", y=3.28, color=WHITE, size=36, max_w=11.0)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.45)

        self.at("the normal line")
        self.play(green_line.animate.set_stroke(width=11), run_time=0.7, rate_func=there_and_back)
        self.at("flatter one")
        self.play(mag_line.animate.set_stroke(width=11), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which line climbs further?"
    CARD = {"y": 3.28, "color": WHITE, "size": 36, "max_w": 11.0}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        P, green_line, _, ring, loop, tag = build_world(p_val=100.0, intake_y=250.0, flattened=True)
        loop.excretion_t.set_value(1.0)
        mag_line = clipped_segment(P, kidney_flat, color=MAGENTA, width=6)
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(96.5, 215))
        flat_lbl = T("flatter", size=26, color=MAGENTA).move_to(P.pt(115.2, 182))
        ghost_intake = make_intake_line(P, 150.0, color=GOLD, width=3, opacity=0.40)
        usual_lbl = T("usual", size=24, color=GOLD).move_to(P.pt(89.5, 172))
        raised_intake = make_intake_line(P, 250.0, color=GOLD, width=4.5)
        more_lbl = T("more salt", size=24, color=GOLD).move_to(P.pt(89.5, 274))
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        return VGroup(P, green_line, mag_line, ghost_intake, usual_lbl, raised_intake, more_lbl,
                      ring, marker, norm_lbl, flat_lbl, tag, loop)


class S07Answer(SpokenScene):
    def construct(self):
        P, green_line, _, ring, loop, tag = build_world(p_val=100.0, intake_y=250.0, flattened=True)
        loop.excretion_t.set_value(1.0)
        mag_line = clipped_segment(P, kidney_flat, color=MAGENTA, width=6)
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(96.5, 215))
        flat_lbl = T("flatter", size=26, color=MAGENTA).move_to(P.pt(115.2, 182))
        ghost_intake = make_intake_line(P, 150.0, color=GOLD, width=3, opacity=0.40)
        usual_lbl = T("usual", size=24, color=GOLD).move_to(P.pt(89.5, 172))
        raised_intake = make_intake_line(P, 250.0, color=GOLD, width=4.5)
        more_lbl = T("more salt", size=24, color=GOLD).move_to(P.pt(89.5, 274))
        p_g = ValueTracker(100.0)
        m_g = make_marker_live(P, p_g, kidney_normal, color=WHITE)
        q = question_card("Which line climbs further?", y=3.28, color=WHITE, size=36, max_w=11.0)

        self.add(P, green_line, mag_line, ghost_intake, usual_lbl, raised_intake, more_lbl,
                 ring, m_g, norm_lbl, flat_lbl, tag, loop, q)

        self.at("The flatter one")
        self.play(FadeOut(q), run_time=0.45)

        # Normal line crosses at 110 (+10)
        self.at("The normal line now crosses")
        g_ring = make_ring(P, 110.0, 250.0, color=GREEN)
        plus10 = T("+10", size=26, color=GREEN).move_to(P.pt(106.2, 276))
        br_g = VGroup(
            Line(P.pt(100, 48), P.pt(110, 48), color=GREEN, stroke_width=4.5),
            Line(P.pt(100, 38), P.pt(100, 58), color=GREEN, stroke_width=3.5),
            Line(P.pt(110, 38), P.pt(110, 58), color=GREEN, stroke_width=3.5),
        )
        self.play(p_g.animate.set_value(110.0), run_time=1.35, rate_func=smooth)
        self.play(FadeIn(g_ring), FadeIn(plus10), Create(br_g), run_time=0.55)

        # Flatter line crosses at 120 (+20)
        self.at("The flatter line crosses")
        p_m = ValueTracker(100.0)
        m_m = make_marker_live(P, p_m, kidney_flat, color=WHITE)
        m_ring = make_ring(P, 120.0, 250.0, color=MAGENTA)
        plus20 = T("+20", size=26, color=MAGENTA).move_to(P.pt(117.2, 276))
        br_m = VGroup(
            Line(P.pt(100, 22), P.pt(120, 22), color=MAGENTA, stroke_width=4.5),
            Line(P.pt(100, 12), P.pt(100, 32), color=MAGENTA, stroke_width=3.5),
            Line(P.pt(120, 12), P.pt(120, 32), color=MAGENTA, stroke_width=3.5),
        )
        self.add(m_m)
        self.play(p_m.animate.set_value(120.0), loop.excretion_t.animate.set_value(250.0 / 150.0),
                  run_time=1.55, rate_func=smooth)
        self.play(FadeIn(m_ring), FadeIn(plus20), Create(br_m), run_time=0.55)
        self.finish()


class S08Sensitivity(SpokenScene):
    def construct(self):
        P, green_line, _, ring, loop, tag = build_world(p_val=120.0, intake_y=250.0, flattened=True)
        mag_line = clipped_segment(P, kidney_flat, color=MAGENTA, width=6)
        norm_lbl = T("normal", size=26, color=GREEN).move_to(P.pt(96.5, 215))
        flat_lbl = T("flatter", size=26, color=MAGENTA).move_to(P.pt(115.2, 182))
        ghost_intake = make_intake_line(P, 150.0, color=GOLD, width=3, opacity=0.40)
        usual_lbl = T("usual", size=24, color=GOLD).move_to(P.pt(89.5, 172))
        raised_intake = make_intake_line(P, 250.0, color=GOLD, width=4.5)
        more_lbl = T("more salt", size=24, color=GOLD).move_to(P.pt(89.5, 274))
        m_g = make_marker_static(P, 110.0, 250.0, color=WHITE)
        m_m = make_marker_static(P, 120.0, 250.0, color=WHITE)
        g_ring = make_ring(P, 110.0, 250.0, color=GREEN)
        m_ring = make_ring(P, 120.0, 250.0, color=MAGENTA)
        plus10 = T("+10", size=26, color=GREEN).move_to(P.pt(106.2, 276))
        plus20 = T("+20", size=26, color=MAGENTA).move_to(P.pt(117.2, 276))
        br_g = VGroup(
            Line(P.pt(100, 48), P.pt(110, 48), color=GREEN, stroke_width=4.5),
            Line(P.pt(100, 38), P.pt(100, 58), color=GREEN, stroke_width=3.5),
            Line(P.pt(110, 38), P.pt(110, 58), color=GREEN, stroke_width=3.5),
        )
        br_m = VGroup(
            Line(P.pt(100, 22), P.pt(120, 22), color=MAGENTA, stroke_width=4.5),
            Line(P.pt(100, 12), P.pt(100, 32), color=MAGENTA, stroke_width=3.5),
            Line(P.pt(120, 12), P.pt(120, 32), color=MAGENTA, stroke_width=3.5),
        )
        self.add(P, green_line, mag_line, ghost_intake, usual_lbl, raised_intake, more_lbl,
                 ring, g_ring, m_ring, m_g, m_m, plus10, plus20, br_g, br_m,
                 norm_lbl, flat_lbl, tag, loop)

        # Glow MAGENTA bracket + 'salt sensitivity' above the plot/flatter curve
        self.at("salt sensitivity")
        sens_lbl = T("salt sensitivity", size=28, color=MAGENTA).move_to(P.pt(116.5, 318))
        self.play(br_m[0].animate.set_stroke(width=8), FadeIn(sens_lbl), run_time=0.65)

        # Dashed GREEN real steep line swings from slope 10 up to 80
        self.at("A real normal line is much steeper")
        steep_s = ValueTracker(10.0)
        steep_line = always_redraw(lambda: clipped_segment(
            P, lambda p: kidney_pivot(p, steep_s.get_value(), 100.0, 150.0),
            color=GREEN, width=4.5, dashed=True,
        ))
        self.add(steep_line)
        self.play(steep_s.animate.set_value(80.0), run_time=1.35, rate_func=smooth)
        steep_dot = Dot(P.pt(101.25, 250.0), radius=0.095, color=GREEN)
        steep_lbl = T("real: steeper (schematic)", size=26, color=GREEN).move_to([-1.2, 3.28, 0])
        self.play(FadeIn(steep_dot), FadeIn(steep_lbl), run_time=0.45)

        # Angiotensin II and aldosterone inside loop interior (clear of all wires)
        self.at("angiotensin II and aldosterone")
        ang_lbl = T("angiotensin II", size=24, color=ORANGE).move_to([4.55, 0.35, 0])
        ald_lbl = T("aldosterone", size=24, color=ORANGE).move_to([4.55, -0.15, 0])
        self.play(FadeIn(ang_lbl), FadeIn(ald_lbl), run_time=0.55)

        self.at("fall")
        self.play(
            ang_lbl.animate.shift(DOWN * 0.35).set_opacity(0.45),
            ald_lbl.animate.shift(DOWN * 0.35).set_opacity(0.45),
            run_time=0.75,
        )
        self.play(FadeOut(steep_line), FadeOut(steep_dot), FadeOut(steep_lbl),
                  FadeOut(ang_lbl), FadeOut(ald_lbl), run_time=0.55)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(p_val=100.0, intake_y=150.0)
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        self.add(P, green_line, intake_line, ring, marker, tag, loop)

        self.at("In Guyton's framework")
        fw_tag = T("Guyton's framework", size=30, color=WHITE).move_to([-3.8, 3.28, 0])
        self.play(FadeIn(fw_tag, shift=DOWN * 0.1), run_time=0.5)

        self.at("salt out equals salt in")
        arr_in = Arrow(P.pt(100, 198), P.pt(100, 160), buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
        arr_out = Arrow(P.pt(100, 102), P.pt(100, 140), buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
        eq_lbl = T("out = in", size=26, color=GOLD).move_to(P.pt(92.0, 185))
        self.play(
            ring.animate.scale(1.4).set_stroke(width=7),
            FadeIn(arr_in), FadeIn(arr_out), FadeIn(eq_lbl),
            run_time=0.55, rate_func=smooth,
        )
        self.play(ring.animate.scale(1.0 / 1.4).set_stroke(width=4.5), run_time=0.35)

        self.at("a moved line")
        sh_t = ValueTracker(0.0)
        ghost_line = always_redraw(lambda: clipped_segment(
            P, lambda p: kidney_shifted(p, sh_t.get_value()), color=MAGENTA, width=5, opacity=0.8,
        ))
        self.add(ghost_line)
        self.play(sh_t.animate.set_value(10.0), run_time=0.55, rate_func=smooth)
        self.play(sh_t.animate.set_value(0.0), run_time=0.45, rate_func=smooth)
        self.remove(ghost_line)

        self.at("a changed intake")
        in_t = ValueTracker(150.0)
        ghost_in = always_redraw(lambda: make_intake_line(P, in_t.get_value(), color=GOLD, width=4.5, opacity=0.85))
        new_tag = teaching_tag("move the line, or the intake", color=GOLD)
        self.add(ghost_in)
        self.play(
            in_t.animate.set_value(240.0),
            swap(tag, new_tag, run_time=0.6),
            run_time=0.65, rate_func=smooth,
        )
        self.play(in_t.animate.set_value(150.0), run_time=0.55, rate_func=smooth)
        self.remove(ghost_in)
        self.finish()


class S10Movers(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=100.0, intake_y=150.0, tag_text="schematic",
        )
        marker = make_marker_static(P, 100.0, 150.0, color=WHITE)
        self.add(P, green_line, intake_line, ring, marker, tag, loop)

        sh_t = ValueTracker(0.0)
        ghost_line = always_redraw(lambda: clipped_segment(
            P, lambda p: kidney_shifted(p, sh_t.get_value()), color=MAGENTA, width=5.5, opacity=0.88,
        ) if abs(sh_t.get_value()) > 0.2 else VMobject())
        self.add(ghost_line)

        self.at("What moves the line")
        self.play(green_line.animate.set_stroke(width=11), run_time=0.8, rate_func=there_and_back)
        self.at("hold more sodium")
        self.play(loop.kidney_box.animate.set_stroke(width=7), run_time=0.8, rate_func=there_and_back)
        self.at("at a given pressure")
        self.play(ring.animate.scale(1.4).set_stroke(width=7), run_time=0.6, rate_func=there_and_back)

        self.at("push it right")
        r_arr = Arrow(P.pt(108, 225), P.pt(117, 225), buff=0, color=MAGENTA, stroke_width=4, tip_length=0.18)
        r_lbl = T("right: hold sodium", size=24, color=MAGENTA).move_to(P.pt(100, 265))
        self.play(sh_t.animate.set_value(5.0), FadeIn(r_arr), FadeIn(r_lbl), run_time=0.7)

        # Tokens travel cleanly inside loop interior [4.55, 0.55 -> -0.55] (clear of walls & kidney!)
        self.at("Angiotensin II")
        tok_ang = boxed_label("angiotensin II", MAGENTA, size=24, pad=0.14)
        tok_ang.box.set_fill(BG, opacity=0.94)
        tok_ang.move_to([4.55, 0.55, 0])
        self.play(FadeIn(tok_ang), run_time=0.25)
        self.play(tok_ang.animate.move_to([4.55, -0.55, 0]), sh_t.animate.set_value(8.0), run_time=0.75)

        self.at("aldosterone")
        tok_ald = boxed_label("aldosterone", MAGENTA, size=24, pad=0.14)
        tok_ald.box.set_fill(BG, opacity=0.94)
        tok_ald.move_to([4.55, 0.55, 0])
        self.play(FadeOut(tok_ang, run_time=0.2))
        self.play(FadeIn(tok_ald, run_time=0.2), tok_ald.animate.move_to([4.55, -0.55, 0]), sh_t.animate.set_value(11.0), run_time=0.65)

        self.at("renal sympathetic nerves")
        nerve_lbl = T("renal nerves", size=24, color=ORANGE).move_to([4.55, 0.0, 0])
        self.play(
            FadeOut(tok_ald, run_time=0.2),
            loop.nerve_t.animate.set_value(1.0),
            FadeIn(nerve_lbl),
            sh_t.animate.set_value(13.5),
            run_time=0.95,
        )

        self.at("Natriuretic peptides")
        tok_np = boxed_label("natriuretic\npeptides", CYAN, size=24, pad=0.14)
        tok_np.box.set_fill(BG, opacity=0.94)
        tok_np.move_to([4.50, 0.35, 0])
        self.play(
            FadeOut(r_arr), FadeOut(r_lbl), FadeOut(nerve_lbl),
            loop.nerve_t.animate.set_value(0.0),
            sh_t.animate.set_value(0.0),
            run_time=0.55,
        )
        self.play(FadeIn(tok_np), run_time=0.25)
        self.play(tok_np.animate.move_to([4.55, -0.55, 0]), run_time=0.55)

        self.at("push it left")
        l_arr = Arrow(P.pt(105, 225), P.pt(96, 225), buff=0, color=MAGENTA, stroke_width=4, tip_length=0.18)
        l_lbl = T("left: shed sodium", size=24, color=MAGENTA).move_to(P.pt(93.5, 276))
        self.play(sh_t.animate.set_value(-8.0), FadeIn(l_arr), FadeIn(l_lbl), run_time=0.7)
        self.play(FadeOut(tok_np), FadeOut(l_arr), FadeOut(l_lbl), sh_t.animate.set_value(0.0), run_time=0.45)
        self.finish()


class S11Channel(SpokenScene):
    def construct(self):
        inset_box = (-6.1, -3.5, 1.15, 3.15)
        P_in = Plot(box=inset_box, xr=(85, 125), yr=(0, 300), xticks=(), yticks=(), color=AXIS_COL, stroke=2.5)
        in_green = clipped_segment(P_in, kidney_normal, color=GREEN, width=4.5)
        in_gold = make_intake_line(P_in, 150.0, color=GOLD, width=3)
        in_dot = Dot(P_in.pt(100.0, 150.0), radius=0.08, color=WHITE)
        in_lbl = T("normal line", size=24, color=GREEN).next_to(P_in, DOWN, buff=0.18)
        inset = VGroup(P_in, in_green, in_gold, in_dot, in_lbl)

        tubule_band = Rectangle(width=2.1, height=5.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.10).move_to([-2.0, 0.0, 0])
        blood_band = Rectangle(width=1.8, height=5.2, stroke_width=0, fill_color=PALE_BLUE, fill_opacity=0.12).move_to([5.1, 0.0, 0])
        cell = RoundedRectangle(
            corner_radius=0.32, width=5.0, height=5.2,
            stroke_color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.92,
        ).move_to([1.65, 0.0, 0])

        tub_lbl = T("tubule fluid", size=28, color=GOLD).move_to([-2.05, 2.95, 0])
        cell_lbl = T("collecting tubule cell", size=28, color=TEXT).move_to([1.65, 2.95, 0])
        blood_lbl = T("blood", size=28, color=PALE_BLUE).move_to([5.1, 2.95, 0])

        def make_door(y, open_frac=0.0, col=GOLD):
            frame = RoundedRectangle(corner_radius=0.06, width=0.34, height=0.60,
                                     stroke_color=col, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to([-0.85, y, 0])
            # closed (open_frac 0): the two leaves meet in the middle; open (1): short stubs at the ends, wide gap
            leaf_top = Line([-0.85, y + 0.26, 0], [-0.85, y + 0.02 + 0.16 * open_frac, 0], color=col, stroke_width=5)
            leaf_bot = Line([-0.85, y - 0.26, 0], [-0.85, y - 0.02 - 0.16 * open_frac, 0], color=col, stroke_width=5)
            return VGroup(frame, leaf_top, leaf_bot)

        self.add(inset, tubule_band, blood_band, cell, tub_lbl, cell_lbl, blood_lbl)

        # Blood dots flowing upward through blood band continuously
        blood_flow = VGroup()
        for i in range(10):
            bd = Dot(radius=0.10, color=PALE_BLUE, fill_opacity=0.85)
            bd._ph = i / 10.0
            bd._x = 4.85 if i % 2 == 0 else 5.35
            bd.move_to([bd._x, -2.4 + 4.8 * bd._ph, 0])
            blood_flow.add(bd)
        def _upd_bf(mob, dt):
            if dt <= 0:
                return
            for bd in mob:
                bd._ph = (bd._ph + 0.30 * dt) % 1.0
                bd.move_to([bd._x, -2.4 + 4.8 * bd._ph, 0])
        self.add(blood_flow)

        self.at("Aldosterone")
        ald_chip = boxed_label("aldosterone", MAGENTA, size=24, pad=0.16)
        ald_chip.box.set_fill(BG, opacity=0.95)
        ald_chip.move_to([2.0, -1.75, 0])
        self.play(FadeIn(ald_chip), run_time=0.4)

        self.at("sodium channels")
        door_ys = [0.95, -0.85]
        doors = VGroup(*[make_door(y, 0.0, GOLD).shift(RIGHT * 1.4) for y in door_ys])
        enac_lbl = T("ENaC", size=26, color=GOLD).move_to([0.15, 2.22, 0])
        self.play(
            FadeIn(doors), FadeIn(enac_lbl),
            doors[0].animate.shift(LEFT * 1.4),
            doors[1].animate.shift(LEFT * 1.4),
            run_time=1.0,
        )
        open_doors = VGroup(*[make_door(y, 1.0, GOLD) for y in door_ys])
        self.play(Transform(doors, open_doors), FadeOut(ald_chip), run_time=0.6)

        n_active = ValueTracker(2.0)
        flow_speed = ValueTracker(0.70)
        na_dots = VGroup()
        for i in range(26):
            d = Dot(radius=0.11, color=GOLD, fill_opacity=0.95)
            d._ph = (i * 0.1346) % 1.0
            na_dots.add(d)

        all_ys = [0.95, -0.85, 1.78, 0.05, -1.70]
        def _upd_na(mob, dt):
            if dt <= 0:
                return
            k = int(round(n_active.get_value()))
            sp = flow_speed.get_value()
            for idx, d in enumerate(mob):
                lane = idx % max(1, k)
                y = all_ys[lane]
                d._ph = (d._ph + sp * dt) % 1.0
                x = -2.4 + 6.3 * d._ph
                d.move_to([x, y, 0])
                d.set_opacity(0.95 * min(1.0, max(0.0, (3.95 - x) / 0.55)))
        na_dots.add_updater(_upd_na)
        self.add(na_dots)

        self.at("tubule")
        mem_hi = Line([-0.85, -2.35, 0], [-0.85, 2.35, 0], color=GOLD, stroke_width=6, stroke_opacity=0.6)
        self.play(FadeIn(mem_hi), run_time=0.45)
        self.play(FadeOut(mem_hi), run_time=0.45)

        self.at("mutations")
        liddle_tag = T("Liddle syndrome", size=34, color=MAGENTA).move_to([-5.0, -0.1, 0])
        self.play(FadeIn(liddle_tag), run_time=0.55)

        self.at("active")
        extra_ys = [1.78, 0.05, -1.70]
        extra_doors = VGroup(*[make_door(y, 1.0, MAGENTA) for y in extra_ys])
        self.play(
            FadeIn(extra_doors, shift=LEFT * 0.6),
            n_active.animate.set_value(5.0),
            flow_speed.animate.set_value(0.95),
            run_time=0.9,
        )
        self.finish()


class S12Liddle(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(p_val=100.0, intake_y=150.0)
        p_t = ValueTracker(100.0)
        marker = make_marker_live(P, p_t, lambda p: 150.0, color=WHITE)

        icon_cell = RoundedRectangle(corner_radius=0.10, width=0.72, height=0.72,
                                     stroke_color=MAGENTA, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to([3.02, -1.75, 0])
        icon_doors = make_icon_doors()
        icon_lbl = T("more ENaC active", size=24, color=MAGENTA).move_to([3.02, -2.42, 0])
        enac_icon = VGroup(icon_cell, icon_doors, icon_lbl)

        self.add(P, green_line, intake_line, ring, marker, tag, loop, enac_icon)

        self.at("higher at any pressure")
        sh_t = ValueTracker(0.0)
        mag_line = always_redraw(lambda: clipped_segment(
            P, lambda p: kidney_shifted(p, sh_t.get_value()), color=MAGENTA, width=6,
        ))
        liddle_lbl = T("Liddle", size=26, color=MAGENTA).move_to(P.pt(121.2, 180))
        self.add(mag_line)
        self.play(
            green_line.animate.set_stroke(opacity=0.45),
            sh_t.animate.set_value(12.0),
            FadeIn(liddle_lbl),
            run_time=1.35, rate_func=smooth,
        )

        self.at("Volume rises first")
        loop.excretion_t.set_value(0.25)
        self.play(loop.volume_t.animate.set_value(1.65), run_time=0.95, rate_func=smooth)

        self.at("then pressure")
        loop.excretion_t.add_updater(lambda m: m.set_value(max(0.2, kidney_shifted(p_t.get_value(), 12.0) / 150.0)))
        self.play(p_t.animate.set_value(112.0), run_time=2.3, rate_func=smooth)
        loop.excretion_t.clear_updaters()
        loop.excretion_t.set_value(1.0)
        new_ring = make_ring(P, 112.0, 150.0, color=MAGENTA)
        hi_lbl = T("higher balance", size=26, color=MAGENTA).move_to(P.pt(119.2, 115))
        self.play(FadeIn(new_ring), FadeIn(hi_lbl), run_time=0.45)

        self.at("matches salt in")
        self.play(
            loop.outlet_tube.animate.set_stroke(width=7.5),
            loop.inlet_tube.animate.set_stroke(width=7.5),
            run_time=0.8, rate_func=there_and_back,
        )
        self.at("higher level")
        self.play(new_ring.animate.scale(1.4).set_stroke(width=7), run_time=0.7, rate_func=there_and_back)

        self.at("One channel")
        self.play(icon_cell.animate.scale(1.3).set_stroke(width=5), run_time=0.7, rate_func=there_and_back)

        self.at("moved the line")
        mag_static = clipped_segment(P, lambda p: kidney_shifted(p, 12.0), color=MAGENTA, width=6)
        self.remove(mag_line)
        self.add(mag_static)
        self.play(mag_static.animate.set_stroke(width=11), run_time=0.45, rate_func=there_and_back)
        self.finish()


class S13Essential(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=112.0, intake_y=150.0, normal_opacity=0.45, shifted=12.0, volume=1.65,
        )
        mag_line = clipped_segment(P, lambda p: kidney_shifted(p, 12.0), color=MAGENTA, width=6)
        liddle_lbl = T("Liddle", size=26, color=MAGENTA).move_to(P.pt(121.2, 180))
        hi_lbl = T("higher balance", size=26, color=MAGENTA).move_to(P.pt(119.2, 115))
        new_ring = make_ring(P, 112.0, 150.0, color=MAGENTA)
        p_t = ValueTracker(112.0)
        marker = make_marker_live(P, p_t, lambda p: 150.0, color=WHITE)
        icon_cell = RoundedRectangle(corner_radius=0.10, width=0.72, height=0.72,
                                     stroke_color=MAGENTA, stroke_width=2.5, fill_color=BG, fill_opacity=0.95).move_to([3.02, -1.75, 0])
        icon_doors = make_icon_doors()
        icon_lbl = T("more ENaC active", size=24, color=MAGENTA).move_to([3.02, -2.42, 0])
        enac_icon = VGroup(icon_cell, icon_doors, icon_lbl)

        self.add(P, green_line, mag_line, intake_line, ring, new_ring, marker,
                 liddle_lbl, hi_lbl, enac_icon, tag, loop)

        self.play(
            FadeOut(liddle_lbl), FadeOut(hi_lbl), FadeOut(new_ring), FadeOut(enac_icon), FadeOut(mag_line),
            green_line.animate.set_stroke(opacity=1.0),
            p_t.animate.set_value(100.0),
            loop.volume_t.animate.set_value(1.0),
            loop.excretion_t.animate.set_value(1.0),
            run_time=1.0, rate_func=smooth,
        )

        self.at("The working model")
        top_lbl = T("essential hypertension: working model", size=30, color=WHITE).move_to([-1.4, 3.28, 0])
        self.play(FadeIn(top_lbl, shift=DOWN * 0.1), run_time=0.45)

        self.at("shifted right")
        v_shift = clipped_segment(P, lambda p: kidney_shifted(p, 10.0), color=MAGENTA, width=4.5, dashed=True)
        self.play(Create(v_shift), run_time=0.75)

        self.at("flattened")
        v_flat = clipped_segment(P, lambda p: 5.0 * (p - 85.0), color=MAGENTA, width=4.5, dashed=True)
        self.play(FadeIn(v_flat), run_time=0.25)

        self.at("or both")
        v_both = clipped_segment(P, lambda p: 5.0 * (p - 93.0), color=MAGENTA, width=4.5, dashed=True)
        self.play(Create(v_both), run_time=0.65)

        self.at("hard to measure directly")
        hard_lbl = T("hard to measure\nin people", size=24, color=TEXT, line_spacing=0.85).move_to(P.pt(96.0, 255))
        self.play(FadeIn(hard_lbl),
                  v_shift.animate.set_stroke(opacity=0.35),
                  v_flat.animate.set_stroke(opacity=0.35),
                  v_both.animate.set_stroke(opacity=0.35),
                  run_time=0.65)
        self.finish()


class S14WhereNotWhat(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=110.0, intake_y=150.0, normal_opacity=0.35, shifted=10.0, ring_at=(110.0, 150.0, MAGENTA),
        )
        mag_line = clipped_segment(P, lambda p: kidney_shifted(p, 10.0), color=MAGENTA, width=6)
        marker = make_marker_static(P, 110.0, 150.0, color=WHITE)
        self.add(P, green_line, mag_line, intake_line, ring, marker, tag, loop)

        self.at("where balance lies")
        where_lbl = T("where balance lies", size=26, color=MAGENTA).move_to(P.pt(119.8, 95))
        self.play(FadeIn(where_lbl), run_time=0.4)
        self.play(ring.animate.scale(1.3).set_stroke(width=7), run_time=0.45, rate_func=there_and_back)

        self.at("not what moved it")
        q_mark = T("?", size=56, color=GOLD).move_to(P.pt(89.5, 240))
        what_lbl = T("what moved it?", size=26, color=GOLD).next_to(q_mark, RIGHT, buff=0.18)
        self.play(FadeIn(q_mark), FadeIn(what_lbl), run_time=0.55)

        self.at("The kidney itself")
        k_lbl = T("kidney", size=26, color=GREEN).move_to([4.55, 0.05, 0])
        self.play(
            loop.kidney_box.animate.set_stroke(color=GOLD, width=6),
            FadeIn(k_lbl),
            run_time=0.65,
        )

        self.at("its nerves")
        n_lbl = T("nerves", size=26, color=ORANGE).move_to([4.55, 0.05, 0])
        self.play(
            loop.kidney_box.animate.set_stroke(color=GREEN, width=3.5),
            swap(k_lbl, n_lbl, run_time=0.45),
            loop.nerve_t.animate.set_value(1.0),
            run_time=0.65,
        )

        self.at("hormones")
        h_lbl = T("hormones", size=26, color=MAGENTA).move_to([4.55, 0.05, 0])
        self.play(
            loop.nerve_t.animate.set_value(0.0),
            swap(n_lbl, h_lbl, run_time=0.45),
            run_time=0.65,
        )
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        P, green_line, intake_line, ring, loop, tag = build_world(
            p_val=110.0, intake_y=150.0, normal_opacity=0.35, shifted=10.0, ring_at=(110.0, 150.0, MAGENTA),
        )
        mag_line = clipped_segment(P, lambda p: kidney_shifted(p, 10.0), color=MAGENTA, width=6)
        marker = make_marker_static(P, 110.0, 150.0, color=WHITE)
        self.add(P, green_line, mag_line, intake_line, ring, marker, tag, loop)

        # On 'every lasting level': show opposing salt balance arrows at the crossing
        self.at("every lasting level")
        arr_in = Arrow(P.pt(110, 198), P.pt(110, 160), buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
        arr_out = Arrow(P.pt(110, 102), P.pt(110, 140), buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
        eq_lbl = T("out = in", size=26, color=GOLD).move_to(P.pt(118.2, 115))
        self.play(FadeIn(arr_in), FadeIn(arr_out), FadeIn(eq_lbl), run_time=0.55)
        self.wait(1.0)
        self.play(FadeOut(arr_in), FadeOut(arr_out), FadeOut(eq_lbl), run_time=0.45)

        self.at("what the kidney lets go")
        self.play(
            mag_line.animate.set_stroke(width=10),
            loop.outlet_tube.animate.set_stroke(width=7.5),
            loop.kidney_box.animate.set_stroke(color=MAGENTA, width=6.5),
            run_time=0.65, rate_func=there_and_back,
        )

        self.at("what comes in")
        self.play(
            intake_line.animate.set_stroke(width=8.5),
            loop.inlet_tube.animate.set_stroke(width=7.5),
            run_time=0.65, rate_func=there_and_back,
        )
        self.finish()


class S16End(EndCard):
    LINE = "To hold a new pressure, move the kidney's line or the intake."
