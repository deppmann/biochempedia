"""Which Line Has Moved? — Chapter 2 of The Cardiac Cycle and Pressure-Volume Loops.

COLOUR MAP (one colour per concept, used throughout the film):
    WHITE   (#FFFFFF / TEXT #E8EAF0) : Baseline pressure-volume loop, circling beat dot, questions, 'same volume' reference line
    GREEN   (#83C167)                : Ventricle's line (ESPVR: P = Ees * (V - V0)), 'squeeze' ('muscle', 'walls + stiffness')
    ORANGE  (#FF862F)                : Arteries' line (Ea: P = Ea * (EDV - V)), aortic valve icon, 'load'
    CYAN    (#45D4E8)                : Passive filling curve (EDPVR), chamber floor glow, stiffness wedge, 'filling'
    MAGENTA (#E05CC8)                : Sick / shifted / domed loops and opening question-mark loops
    YELLOW  (#F5D547)                : Stroke-volume (SV) span arrow

CARRIED WORLD:
    One pressure-volume plot (x: volume 0..250 mL, y: pressure 0..160 mmHg) filling ~68% of the frame height,
    with the baseline loop (EDV 125 mL, ESV 45 mL, Pes 120 mmHg, V0 5 mL, Ees 3.0, Ea 1.5), a WHITE dot
    running counterclockwise round the active loop throughout, and the GREEN, ORANGE and CYAN lines.
    In S11Close the single plot splits into three side-by-side copies (reduced EF, preserved EF, aortic stenosis).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
    S00LinkAndQuestion : Circling dot advances around computed baseline loop; top-left crossing ring pulses;
                         GREEN and ORANGE lines highlight as named; bottom floor glows CYAN; baseline dims to
                         dashed ghost and two schematic MAGENTA '?' loops appear as the question lands.
    S02Floor           : CYAN floor glow extends into the computed exponential EDPVR curve (5..240 mL);
                         circling dot rides along the loop's floor on the curve; CYAN slope wedge appears at EDV.
    S03ReducedEf       : Driven by ValueTrackers (V0: 5->95, EDV: 125->215, EDPVR shift: 0->80, Ees: 3.0->1.35),
                         ESPVR, EDPVR, Ea line and MAGENTA loop slide right and pivot flatter with live computed
                         corner (ESV, Pes); pale full-volume bar and YELLOW SV arrow grow below loop.
    S04Idea            : Sick shapes smoothly return to baseline WHITE loop + three lines; GREEN, CYAN and
                         ORANGE lines glow in sequence as 'squeeze', 'filling', 'load' labels lock in.
    S05PreservedEf     : Driven by stiffness tracker (0->1), CYAN EDPVR shifts up-left and bends steeper above
                         a faint 'normal floor' ghost while loop bottom rises onto it; dot visibly slows on the
                         isovolumic relaxation (left) side.
    S06Predict         : Dashed WHITE vertical line drops from EDV=125 mL to axis across both floors;
                         question card 'Same volume: what pressure?' fades in at top.
    S08Answer          : Two intersection dots + vertical CYAN arrow connect normal (10 mmHg) and stiff (32.5 mmHg)
                         floors at 125 mL; study card appears; handgrip fist squeezes as Ea tilts (1.5->1.85) and
                         MAGENTA bottom-right corner climbs steeper up the stiff floor than the normal-floor ghost;
                         'cause?' marker settles beside the curve.
    S09SlopeCaution    : GREEN ESPVR pivots steeper (Ees 3.0->4.8, dashed); 'squeeze' splits into 'muscle' and
                         'walls + stiffness'; 'walls + stiffness' glows; 'muscle' drops downward while steep GREEN
                         line stays steep; both pulse together.
    S10AorticStenosis  : World returns to baseline; valve slit narrows on ORANGE line as Ea tilts (1.5->1.75);
                         MAGENTA loop top domes upward (computed parabolic dome); Ees steepens (3.0->3.6) so
                         top-left corner returns near 45 mL and YELLOW SV arrow holds near baseline length.
    S11Close           : Plot splits into three side-by-side plots (reduced EF, preserved EF, aortic stenosis)
                         revealed one by one, each with circling dot and dashed 'normal' ghost; GREEN, CYAN and
                         ORANGE lines glow in turn.
"""

from bp_parts import *
import numpy as np

# Concept colours extending bp_style / bp_parts
CYAN = "#45D4E8"
MAGENTA = "#E05CC8"

# Main plot geometry: y0=-2.45..y1=2.25 -> 4.70 units (~67% of 7.0 safe height).
# Leaves ylabel top <= 2.72 so top-left condition tags at y=3.32 and top headings at y=3.32 clear ylabel completely.
PLOT_BOX = (-5.0, 4.1, -2.45, 2.25)
PLOT_XR = (0.0, 250.0)
PLOT_YR = (0.0, 160.0)
PLOT_XTICKS = [0, 50, 100, 150, 200, 250]
PLOT_YTICKS = [0, 40, 80, 120, 160]


# ------------------------------------------------------------------ physiological model helpers
def edpvr_p(v, stiff=0.0, v_shift=0.0):
    """Computed schematic passive filling curve (EDPVR).

    Baseline (stiff=0, v_shift=0): passes near (45, 4.7) and (125, 10.0) and bends upward to the right.
    Shifted right (v_shift>0): dilated chamber in reduced EF.
    Stiffened (stiff>0): shifted up and left and bending more steeply in preserved EF.
    """
    veff = np.maximum(0.0, v - v_shift)
    base_off = 2.8 + 3.2 * stiff
    amp = 0.9 + 0.7 * stiff
    rate = 0.0166 + 0.0042 * stiff
    return base_off + amp * np.exp(rate * (veff + 10.0 * stiff))


def solve_crossing(edv=125.0, v0=5.0, ees=3.0, ea=1.5):
    """Exact intersection of ESPVR: P = Ees*(V - V0) and Ea: P = Ea*(EDV - V)."""
    sv = (edv - v0) / (1.0 + ea / ees)
    esv = edv - sv
    pes = ea * sv
    return sv, esv, pes


def loop_vp_points(edv=125.0, esv=45.0, pes=120.0, p_ao_open=80.0, stiff=0.0, v_shift=0.0, dome=0.0, n_side=32):
    """Counterclockwise (V, P) coordinates around the four phases of one beat."""
    p_ed = float(edpvr_p(edv, stiff=stiff, v_shift=v_shift))
    p_mo = float(edpvr_p(esv, stiff=stiff, v_shift=v_shift))
    pts = []
    # 0: isovolumic contraction (right vertical side, up)
    for u in np.linspace(0.0, 1.0, n_side, endpoint=False):
        pts.append((edv, p_ed + u * (p_ao_open - p_ed)))
    # 1: ejection (top side, right to left, with optional systolic dome)
    for u in np.linspace(0.0, 1.0, n_side, endpoint=False):
        v = edv + u * (esv - edv)
        p = p_ao_open + u * (pes - p_ao_open) + dome * 4.0 * u * (1.0 - u)
        pts.append((v, p))
    # 2: isovolumic relaxation (left vertical side, down)
    for u in np.linspace(0.0, 1.0, n_side, endpoint=False):
        pts.append((esv, pes + u * (p_mo - pes)))
    # 3: filling (bottom side, left to right along EDPVR)
    for u in np.linspace(0.0, 1.0, n_side, endpoint=False):
        v = esv + u * (edv - esv)
        pts.append((v, float(edpvr_p(v, stiff=stiff, v_shift=v_shift))))
    return np.array(pts, dtype=float)


def sample_loop(pts, phase):
    """Interpolate (V, P) at phase in [0, 1)."""
    n = len(pts)
    f = (phase % 1.0) * n
    i0 = int(np.floor(f)) % n
    i1 = (i0 + 1) % n
    a = f - np.floor(f)
    return (1.0 - a) * pts[i0] + a * pts[i1]


def make_loop_mob(plot, pts, color=WHITE, width=4.8, fill_opacity=0.08, dashed=False, opacity=0.90):
    """Closed Polygon / DashedVMobject in plot coordinates from (V, P) points."""
    scene_pts = [plot.pt(float(v), float(np.clip(p, PLOT_YR[0], PLOT_YR[1]))) for v, p in pts]
    poly = Polygon(*scene_pts, stroke_color=color, stroke_width=width, stroke_opacity=opacity,
                   fill_color=color, fill_opacity=fill_opacity if not dashed else 0.0)
    if dashed:
        d = DashedVMobject(poly, num_dashes=42, dashed_ratio=0.55)
        d.set_stroke(color=color, width=width * 0.72, opacity=opacity)
        return d
    return poly


def make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.0, max_p=152.0, dashed=False, opacity=1.0):
    """ESPVR line P = Ees * (V - V0) from V0 up to max_p (clipped to plot)."""
    v_end = min(PLOT_XR[1] - 4.0, v0 + max_p / max(ees, 0.1))
    p_end = ees * (v_end - v0)
    a = plot.pt(v0, 0.0)
    b = plot.pt(v_end, min(PLOT_YR[1], p_end))
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=width, dash_length=0.14).set_stroke(opacity=opacity)
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def make_ea_line(plot, edv=125.0, ea=1.5, v_stop=None, color=ORANGE, width=5.0, opacity=1.0):
    """Arteries' line P = Ea * (EDV - V) from EDV on volume axis up to v_stop (or P=150)."""
    if v_stop is None:
        v_stop = max(12.0, edv - 150.0 / max(ea, 0.1))
    p_stop = min(PLOT_YR[1], ea * (edv - v_stop))
    a = plot.pt(edv, 0.0)
    b = plot.pt(v_stop, p_stop)
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def make_edpvr_curve(plot, stiff=0.0, v_shift=0.0, x0=5.0, x1=242.0, color=CYAN, width=5.0, opacity=1.0, dashed=False):
    """Computed EDPVR curve clipped to plot."""
    c = plot.curve(lambda v: edpvr_p(v, stiff=stiff, v_shift=v_shift), x0=x0, x1=x1,
                   color=color, width=width, n=120, opacity=opacity)
    if dashed:
        d = DashedVMobject(c, num_dashes=36, dashed_ratio=0.55)
        d.set_stroke(color=color, width=width * 0.75, opacity=opacity)
        return d
    return c


def make_circling_dot(plot, pts_fn, phase_tracker, color=WHITE, radius=0.11, trail_frac=0.22):
    """WHITE dot running counterclockwise round pts_fn(), with a bold glowing comet trail along the beat."""
    def _build():
        pts = pts_fn()
        ph = phase_tracker.get_value() % 1.0
        v, p = sample_loop(pts, ph)
        pos = plot.pt(float(v), float(np.clip(p, PLOT_YR[0], PLOT_YR[1])))
        g = VGroup()
        n_seg = 12
        for k in range(n_seg):
            f0 = (ph - trail_frac * (n_seg - k) / n_seg) % 1.0
            f1 = (ph - trail_frac * (n_seg - k - 1) / n_seg) % 1.0
            v0, p0 = sample_loop(pts, f0)
            v1, p1 = sample_loop(pts, f1)
            seg = Line(
                plot.pt(float(v0), float(np.clip(p0, PLOT_YR[0], PLOT_YR[1]))),
                plot.pt(float(v1), float(np.clip(p1, PLOT_YR[0], PLOT_YR[1]))),
                color=color,
                stroke_width=4.0 + 7.0 * (k / n_seg),
                stroke_opacity=0.15 + 0.75 * (k / n_seg),
            )
            g.add(seg)
        halo = Dot(pos, radius=radius * 1.55, color=color, fill_opacity=0.25, stroke_width=0)
        dot = Dot(pos, radius=radius, color=color, stroke_color=BG, stroke_width=1.5)
        g.add(halo, dot)
        return g
    mob = always_redraw(_build)
    mob.layout_ok = True
    return mob


def build_base_plot(box=PLOT_BOX, label_size=26, tick_size=22):
    """Standard PV axes used across the film."""
    return Plot(
        box=box,
        xr=PLOT_XR,
        yr=PLOT_YR,
        xticks=PLOT_XTICKS,
        yticks=PLOT_YTICKS,
        xlabel="volume (mL)",
        ylabel="pressure (mmHg)",
        color=GREY,
        size=tick_size,
        label_size=label_size,
        stroke=3,
    )


def filling_label_pos(plot, stiff=0.0):
    """Safe inside-frame position for the 'filling' label right of the CYAN EDPVR curve."""
    if stiff < 0.5:
        return np.array([plot.x1 + 0.72, plot.pt(240.0, float(edpvr_p(240.0, stiff=0.0)))[1], 0.0])
    # At stiff=1.0, curve exits P=160 near V=208 (x~2.57); put 'filling' cleanly to its right at V=238, P=135
    return plot.pt(238.0, 135.0)


def build_three_labels(plot, stiff=0.0):
    """Permanent 'squeeze', 'filling', 'load' labels placed cleanly clear of every curve."""
    # 'squeeze' sits cleanly right/above baseline GREEN (55, 150) and above AS dome (131 at V=84)
    sq = T("squeeze", 28, GREEN).move_to(plot.pt(84.0, 156.0))
    # 'load' sits in the open area inside the loop well left/below all ORANGE lines (Ea=1.5..1.85)
    ld = T("load", 28, ORANGE).move_to(plot.pt(68.0, 56.0))
    fl = T("filling", 28, CYAN).move_to(filling_label_pos(plot, stiff=stiff))
    return sq, fl, ld


def attach_phase_clock(phase_tracker, rate=0.34, slow_relax_fn=None):
    """Updater advancing phase_tracker counterclockwise; slows on left side (0.50..0.75) when slow_relax_fn() is True."""
    def _tick(mob, dt):
        ph = mob.get_value() % 1.0
        mult = 0.25 if (slow_relax_fn is not None and slow_relax_fn() and 0.48 <= ph <= 0.76) else 1.0
        mob.increment_value(rate * mult * dt)
    phase_tracker.add_updater(_tick)
    return phase_tracker


def make_handgrip_icon(center, color=ORANGE):
    """Simple geometric handgrip / fist icon."""
    palm = RoundedRectangle(corner_radius=0.14, width=0.72, height=0.56, color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.18).move_to(center)
    fingers = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=0.14, height=0.22, color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=0.35)
        for _ in range(4)
    ]).arrange(RIGHT, buff=0.03).move_to(palm.get_top() + DOWN * 0.14)
    thumb = RoundedRectangle(corner_radius=0.06, width=0.28, height=0.13, color=color, stroke_width=2.5,
                             fill_color=color, fill_opacity=0.35).move_to(palm.get_left() + RIGHT * 0.16 + UP * 0.02)
    return VGroup(palm, fingers, thumb)


def make_valve_icon(center, openness=1.0, color=ORANGE):
    """Schematic aortic valve leaflets on the ORANGE line; openness 1.0 (open) -> 0.12 (slit)."""
    gap = 0.04 + 0.18 * openness
    top_leaf = Line(center + LEFT * 0.20 + UP * 0.20, center + RIGHT * 0.08 + UP * gap, color=color, stroke_width=4.5)
    bot_leaf = Line(center + LEFT * 0.20 + DOWN * 0.20, center + RIGHT * 0.08 + DOWN * gap, color=color, stroke_width=4.5)
    ring = Circle(radius=0.24, color=color, stroke_width=2.5).move_to(center)
    return VGroup(ring, top_leaf, bot_leaf)


def cond_tag(text, color):
    """Top-left condition tag placed cleanly above ylabel (ylabel top <= 2.72)."""
    return boxed_label(text, color, size=26, pad=0.14).move_to([-4.55, 3.32, 0])


# ------------------------------------------------------------------ SCENES
class S00LinkAndQuestion(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.12)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        base_loop = make_loop_mob(plot, base_pts, color=WHITE, width=4.8, fill_opacity=0.08)
        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)

        dot = make_circling_dot(plot, lambda: base_pts, phase, color=WHITE)
        self.add(plot, green_line, orange_line, base_loop, dot)

        # Cue: "crossed" -> top-left corner pulses where GREEN meets ORANGE
        self.at("crossed")
        pulse_ring = Circle(radius=0.16, color=GOLD, stroke_width=4.5).move_to(plot.pt(45, 120))
        self.play(pulse_ring.animate.scale(2.6).set_opacity(0), run_time=0.8)
        self.remove(pulse_ring)

        # Cue: "ventricles line" -> GREEN line highlights
        self.at("ventricles line")
        self.play(green_line.animate.set_stroke(width=9.5), run_time=0.5)
        self.play(green_line.animate.set_stroke(width=5.5), run_time=0.45)

        # Cue: "arteries line" -> ORANGE line highlights
        self.at("arteries line")
        self.play(orange_line.animate.set_stroke(width=9.5), run_time=0.5)
        self.play(orange_line.animate.set_stroke(width=5.5), run_time=0.45)

        # Cue: "a floor" -> loop's bottom edge glows CYAN
        self.at("a floor")
        floor_pts = [plot.pt(float(v), float(edpvr_p(v))) for v in np.linspace(45.0, 125.0, 36)]
        floor_glow = VMobject(stroke_color=CYAN, stroke_width=8.5, fill_opacity=0).set_points_as_corners(floor_pts)
        self.play(Create(floor_glow), run_time=0.7)

        # Cue: "when a heart fails" -> baseline dims to dashed ghost, two MAGENTA '?' loops appear + top question
        self.at("when a heart fails")
        ghost_loop = make_loop_mob(plot, base_pts, color=WHITE, width=3.8, dashed=True, opacity=0.75)
        # Put 'normal' cleanly between V=45 and q_loop_f left wall (V=78), below ORANGE (74 at V=76)
        ghost_lbl = T("normal", 24, WHITE).move_to(plot.pt(61, 32))

        # Schematic question-mark loop 1: far right (dilated)
        q_pts_r = loop_vp_points(215.0, 158.0, 86.0, 58.0, stiff=0.0, v_shift=80.0)
        q_loop_r = make_loop_mob(plot, q_pts_r, color=MAGENTA, width=4.5, fill_opacity=0.14)
        q_mark_r = T("?", 34, MAGENTA, weight=BOLD).move_to(plot.pt(186, 46))

        # Schematic question-mark loop 2: raised floor (78..145 mL so left wall clears 'normal' at 61)
        q_pts_f = loop_vp_points(145.0, 78.0, 134.0, 92.0, stiff=1.15)
        q_loop_f = make_loop_mob(plot, q_pts_f, color=MAGENTA, width=4.5, fill_opacity=0.10)
        q_mark_f = T("?", 34, MAGENTA, weight=BOLD).move_to(plot.pt(108, 72))

        top_q = T("Which line has moved?", 34, TEXT, weight=BOLD).move_to([0.0, 3.32, 0])
        stag = scope_tag("schematic")

        self.play(
            FadeOut(base_loop),
            FadeIn(ghost_loop),
            FadeIn(ghost_lbl),
            FadeIn(q_loop_r),
            FadeIn(q_mark_r),
            FadeIn(q_loop_f),
            FadeIn(q_mark_f),
            FadeIn(top_q),
            FadeIn(stag),
            run_time=1.0,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.18)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        ghost_loop = make_loop_mob(plot, base_pts, color=WHITE, width=3.8, dashed=True, opacity=0.75)
        ghost_lbl = T("normal", 24, WHITE).move_to(plot.pt(61, 32))
        base_loop = make_loop_mob(plot, base_pts, color=WHITE, width=4.8, fill_opacity=0.08)

        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)

        floor_pts = [plot.pt(float(v), float(edpvr_p(v))) for v in np.linspace(45.0, 125.0, 36)]
        floor_glow = VMobject(stroke_color=CYAN, stroke_width=8.5, fill_opacity=0).set_points_as_corners(floor_pts)

        q_pts_r = loop_vp_points(215.0, 158.0, 86.0, 58.0, stiff=0.0, v_shift=80.0)
        q_loop_r = make_loop_mob(plot, q_pts_r, color=MAGENTA, width=4.5, fill_opacity=0.14)
        q_mark_r = T("?", 34, MAGENTA, weight=BOLD).move_to(plot.pt(186, 46))

        q_pts_f = loop_vp_points(145.0, 78.0, 134.0, 92.0, stiff=1.15)
        q_loop_f = make_loop_mob(plot, q_pts_f, color=MAGENTA, width=4.5, fill_opacity=0.10)
        q_mark_f = T("?", 34, MAGENTA, weight=BOLD).move_to(plot.pt(108, 72))

        top_q = T("Which line has moved?", 34, TEXT, weight=BOLD).move_to([0.0, 3.32, 0])
        stag = scope_tag("schematic")
        dot = make_circling_dot(plot, lambda: base_pts, phase, color=WHITE)

        self.add(plot, green_line, orange_line, ghost_loop, ghost_lbl, floor_glow,
                 q_loop_r, q_mark_r, q_loop_f, q_mark_f, top_q, stag, dot)

        title = T("Which Line Has Moved?", 42, TEXT, font=TITLE_FONT).move_to([0.0, 3.32, 0])
        rule = Line(LEFT * 1.1, RIGHT * 1.1, color=GOLD, stroke_width=3).next_to(title, DOWN, buff=0.08)
        title_grp = VGroup(title, rule)

        # Fade out question & '?' loops FIRST so top text never overlaps during fade
        self.play(
            FadeOut(top_q),
            FadeOut(q_loop_r), FadeOut(q_mark_r),
            FadeOut(q_loop_f), FadeOut(q_mark_f),
            FadeOut(ghost_loop), FadeOut(ghost_lbl),
            FadeOut(stag),
            FadeIn(base_loop),
            run_time=0.45,
        )
        self.play(FadeIn(title_grp), run_time=0.55)
        self.wait(0.65)
        self.play(FadeOut(title_grp), run_time=0.3)
        self.finish()


class S02Floor(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.45)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        base_loop = make_loop_mob(plot, base_pts, color=WHITE, width=4.8, fill_opacity=0.08)
        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)

        floor_pts = [plot.pt(float(v), float(edpvr_p(v))) for v in np.linspace(45.0, 125.0, 36)]
        floor_glow = VMobject(stroke_color=CYAN, stroke_width=8.5, fill_opacity=0).set_points_as_corners(floor_pts)

        dot = make_circling_dot(plot, lambda: base_pts, phase, color=WHITE)
        self.add(plot, green_line, orange_line, base_loop, floor_glow, dot)

        # Cue: "runs a third line" -> smoothly extend CYAN glow into full EDPVR curve over 3.5s
        self.at("runs a third line")
        x_hi = ValueTracker(125.0)
        x_lo = ValueTracker(45.0)
        live_edpvr = always_redraw(lambda: plot.curve(
            lambda v: edpvr_p(v, stiff=0.0),
            x0=float(x_lo.get_value()),
            x1=float(x_hi.get_value()),
            color=CYAN, width=5.5, n=120,
        ))
        self.add(live_edpvr)
        stag = scope_tag("schematic")
        self.play(
            x_lo.animate.set_value(5.0),
            x_hi.animate.set_value(240.0),
            FadeOut(floor_glow),
            FadeIn(stag),
            run_time=3.4,
        )

        # Cue: "passive filling curve" -> label 'filling curve' + glowing pulse sweep along full curve
        self.at("passive filling curve")
        fill_lbl = T("filling curve", 28, CYAN).move_to(plot.pt(195, 50))
        self.play(FadeIn(fill_lbl), run_time=0.6)
        full_cyan_glow = plot.curve(lambda v: edpvr_p(v, stiff=0.0), x0=5.0, x1=240.0, color=WHITE, width=10.0, n=120)
        self.play(ShowPassingFlash(full_cyan_glow, time_width=0.55), run_time=3.6)

        # Cue: "once relaxation" -> trace glowing CYAN highlight ribbon along loop bottom edge synced with dot
        self.at("once relaxation")
        phase.set_value(0.75)
        floor_x = ValueTracker(45.0)
        floor_trace = always_redraw(lambda: plot.curve(
            lambda v: edpvr_p(v, stiff=0.0),
            x0=45.0, x1=max(46.0, float(floor_x.get_value())),
            color=CYAN, width=11.0, n=40,
        ))
        ride_ring = always_redraw(lambda: Circle(
            radius=0.22, color=CYAN, stroke_width=4.0
        ).move_to(plot.pt(*sample_loop(base_pts, phase.get_value()))))
        ride_ring.layout_ok = True
        self.add(floor_trace, ride_ring)
        self.play(floor_x.animate.set_value(125.0), run_time=3.8)

        # Cue: "its slope" -> tangent line + CYAN stiffness wedge near bottom-right corner (125..175 mL)
        self.at("its slope")
        self.play(FadeOut(ride_ring), FadeOut(floor_trace), run_time=0.35)
        v_a, v_b = 125.0, 175.0
        p_a = float(edpvr_p(v_a))
        slope_125 = (float(edpvr_p(126.0)) - float(edpvr_p(124.0))) / 2.0
        p_tan_b = p_a + slope_125 * (v_b - v_a)
        tan_line = Line(plot.pt(95.0, p_a - slope_125 * 30.0), plot.pt(190.0, p_a + slope_125 * 65.0 + 10.0),
                        color=CYAN, stroke_width=3.5, stroke_opacity=0.8)
        wedge = Polygon(
            plot.pt(v_a, p_a),
            plot.pt(v_b, p_a),
            plot.pt(v_b, p_tan_b + 8.0),
            color=CYAN, stroke_width=3.5, fill_color=CYAN, fill_opacity=0.28,
        )
        stiff_lbl = T("stiffness", 26, CYAN).move_to(plot.pt(205, 16))
        self.play(Create(tan_line), FadeIn(wedge), FadeIn(stiff_lbl), run_time=1.8)
        self.finish()


class S03ReducedEf(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.10)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        v0_t = ValueTracker(5.0)
        edv_t = ValueTracker(125.0)
        ees_t = ValueTracker(3.0)
        vshift_t = ValueTracker(0.0)
        ea_val = 1.5

        def cur_params():
            v0 = v0_t.get_value()
            edv = edv_t.get_value()
            ees = ees_t.get_value()
            vs = vshift_t.get_value()
            sv, esv, pes = solve_crossing(edv=edv, v0=v0, ees=ees, ea=ea_val)
            p_ao = 80.0 * (pes / 120.0)
            return v0, edv, ees, vs, sv, esv, pes, p_ao

        def cur_pts():
            _, edv, _, vs, _, esv, pes, p_ao = cur_params()
            return loop_vp_points(edv=edv, esv=esv, pes=pes, p_ao_open=p_ao, stiff=0.0, v_shift=vs)

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        base_loop = make_loop_mob(plot, base_pts, color=WHITE, width=4.8, fill_opacity=0.08)
        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)
        cyan_curve = make_edpvr_curve(plot, stiff=0.0, v_shift=0.0, x0=5.0, x1=242.0, color=CYAN, width=5.0)

        dot = make_circling_dot(plot, lambda: base_pts, phase, color=WHITE)
        self.add(plot, cyan_curve, green_line, orange_line, base_loop, dot)

        # Cue: "start with" -> tag top left 'reduced EF' + trace dashed 'normal' ghost ready
        self.at("start with")
        tag = cond_tag("reduced EF", MAGENTA)
        stag = scope_tag("schematic")
        ghost_loop = make_loop_mob(plot, base_pts, color=WHITE, width=3.8, dashed=True, opacity=0.70)
        ghost_lbl = T("normal", 24, WHITE).move_to(plot.pt(66, 32))
        self.play(FadeIn(tag), FadeIn(stag), run_time=0.8)
        self.play(Create(ghost_loop), FadeIn(ghost_lbl), run_time=2.2)

        # Cue: "remodeling shifts" -> slide GREEN, CYAN, ORANGE and MAGENTA loop right over 4.2s
        self.at("remodeling shifts")
        live_cyan = always_redraw(lambda: make_edpvr_curve(
            plot, stiff=0.0, v_shift=vshift_t.get_value(), x0=5.0, x1=242.0, color=CYAN, width=5.0
        ))
        live_green = always_redraw(lambda: make_espvr_line(
            plot, v0=v0_t.get_value(), ees=ees_t.get_value(), color=GREEN, width=5.5, max_p=150.0
        ))
        live_orange = always_redraw(lambda: make_ea_line(
            plot, edv=edv_t.get_value(), ea=ea_val, v_stop=cur_params()[5], color=ORANGE, width=5.5
        ))
        live_loop = always_redraw(lambda: make_loop_mob(
            plot, cur_pts(), color=MAGENTA, width=5.0, fill_opacity=0.14
        ))
        live_dot = make_circling_dot(plot, cur_pts, phase, color=WHITE)

        self.remove(base_loop, green_line, orange_line, cyan_curve, dot)
        self.add(live_cyan, live_green, live_orange, live_loop, live_dot)

        self.play(
            v0_t.animate.set_value(95.0),
            edv_t.animate.set_value(215.0),
            vshift_t.animate.set_value(80.0),
            run_time=4.2,
        )

        # Cue: "usually flatter" -> GREEN line pivots flatter (Ees: 3.0 -> 1.35) over 4.0s
        self.at("usually flatter")
        self.play(ees_t.animate.set_value(1.35), run_time=4.0)

        # Cue: "the result" -> pale full-volume bar grows 0->215 mL before YELLOW SV arrow
        self.at("the result")
        _, edv_f, _, _, _, esv_f, _, _ = cur_params()
        bar_x = ValueTracker(0.0)
        full_bar = always_redraw(lambda: Line(
            plot.pt(0.0, -1.8), plot.pt(max(0.5, bar_x.get_value()), -1.8),
            color=WHITE, stroke_width=6.0, stroke_opacity=0.80,
        ))
        full_lbl = T("full\nvolume", 23, WHITE).move_to(plot.pt(141.6, 23.0))
        self.add(full_bar)
        self.play(bar_x.animate.set_value(edv_f), FadeIn(full_lbl), run_time=2.0)

        # Cue: "small fraction" -> YELLOW stroke-volume arrow under MAGENTA loop
        self.at("small fraction")
        sv_arrow = DoubleArrow(
            plot.pt(esv_f, 20.0), plot.pt(edv_f, 20.0),
            color=YELLOW, stroke_width=5, tip_length=0.18, buff=0.0,
        )
        sv_lbl = T("SV", 24, YELLOW).move_to(plot.pt(171.0, 35.0))
        self.play(FadeIn(sv_arrow), FadeIn(sv_lbl), run_time=0.8)
        self.finish()


class S04Idea(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.20)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        v0_t = ValueTracker(95.0)
        edv_t = ValueTracker(215.0)
        ees_t = ValueTracker(1.35)
        vshift_t = ValueTracker(80.0)
        ea_val = 1.5

        def cur_params():
            v0, edv, ees, vs = v0_t.get_value(), edv_t.get_value(), ees_t.get_value(), vshift_t.get_value()
            sv, esv, pes = solve_crossing(edv=edv, v0=v0, ees=ees, ea=ea_val)
            return v0, edv, ees, vs, sv, esv, pes, 80.0 * (pes / 120.0)

        def cur_pts():
            _, edv, _, vs, _, esv, pes, p_ao = cur_params()
            return loop_vp_points(edv=edv, esv=esv, pes=pes, p_ao_open=p_ao, stiff=0.0, v_shift=vs)

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        ghost_loop = make_loop_mob(plot, base_pts, color=WHITE, width=3.8, dashed=True, opacity=0.70)
        ghost_lbl = T("normal", 24, WHITE).move_to(plot.pt(66, 32))
        tag = cond_tag("reduced EF", MAGENTA)
        stag = scope_tag("schematic")

        sv_arrow = DoubleArrow(plot.pt(158.2, 20.0), plot.pt(215.0, 20.0), color=YELLOW, stroke_width=5, tip_length=0.18, buff=0.0)
        sv_lbl = T("SV", 24, YELLOW).move_to(plot.pt(171.0, 35.0))
        full_bar = Line(plot.pt(0.0, -1.8), plot.pt(215.0, -1.8), color=WHITE, stroke_width=6.0, stroke_opacity=0.80)
        full_lbl = T("full\nvolume", 23, WHITE).move_to(plot.pt(141.6, 23.0))

        live_cyan = always_redraw(lambda: make_edpvr_curve(
            plot, stiff=0.0, v_shift=vshift_t.get_value(), x0=5.0, x1=242.0, color=CYAN, width=5.0
        ))
        live_green = always_redraw(lambda: make_espvr_line(
            plot, v0=v0_t.get_value(), ees=ees_t.get_value(), color=GREEN, width=5.5, max_p=150.0
        ))
        live_orange = always_redraw(lambda: make_ea_line(
            plot, edv=edv_t.get_value(), ea=ea_val, v_stop=cur_params()[5], color=ORANGE, width=5.5
        ))
        live_loop = always_redraw(lambda: make_loop_mob(
            plot, cur_pts(), color=MAGENTA, width=5.0, fill_opacity=0.14
        ))
        dot = make_circling_dot(plot, cur_pts, phase, color=WHITE)

        self.add(plot, ghost_loop, ghost_lbl, tag, stag, sv_arrow, sv_lbl, full_bar, full_lbl,
                 live_cyan, live_green, live_orange, live_loop, dot)

        # Cue: "so ask" -> clear sick tags first (0.5s), morph back to baseline (3.2s), show question
        self.at("so ask")
        top_q = T("Which line has moved?", 34, TEXT, weight=BOLD).move_to([0.3, 3.32, 0])
        self.play(
            FadeOut(tag), FadeOut(stag),
            FadeOut(sv_arrow), FadeOut(sv_lbl), FadeOut(full_bar), FadeOut(full_lbl),
            FadeOut(ghost_lbl),
            run_time=0.5,
        )
        self.play(
            v0_t.animate.set_value(5.0),
            edv_t.animate.set_value(125.0),
            ees_t.animate.set_value(3.0),
            vshift_t.animate.set_value(0.0),
            run_time=3.2,
        )
        base_loop = make_loop_mob(plot, base_pts, color=WHITE, width=4.8, fill_opacity=0.08)
        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)
        cyan_curve = make_edpvr_curve(plot, stiff=0.0, v_shift=0.0, x0=5.0, x1=242.0, color=CYAN, width=5.0)
        self.remove(ghost_loop, live_loop, live_green, live_orange, live_cyan, dot)
        dot_base = make_circling_dot(plot, lambda: base_pts, phase, color=WHITE)
        self.add(cyan_curve, green_line, orange_line, base_loop, dot_base)
        self.play(FadeIn(top_q), run_time=0.7)

        sq_lbl, fl_lbl, ld_lbl = build_three_labels(plot, stiff=0.0)

        # Cue: "the ventricles line" / "squeeze" -> GREEN glows and gets 'squeeze'
        self.at("squeeze")
        self.play(green_line.animate.set_stroke(width=9.5), FadeIn(sq_lbl), run_time=0.8)
        self.play(green_line.animate.set_stroke(width=5.5), run_time=0.6)

        # Cue: "filling" -> CYAN glows and gets 'filling'
        self.at("filling")
        self.play(cyan_curve.animate.set_stroke(width=9.5), FadeIn(fl_lbl), run_time=0.8)
        self.play(cyan_curve.animate.set_stroke(width=5.0), run_time=0.6)

        # Cue: "load" -> ORANGE glows and gets 'load'
        self.at("load")
        self.play(orange_line.animate.set_stroke(width=9.5), FadeIn(ld_lbl), run_time=0.6)
        self.play(orange_line.animate.set_stroke(width=5.5), run_time=0.35)
        self.finish()


class S05PreservedEf(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.15)
        slow_flag = [False]
        attach_phase_clock(phase, rate=0.34, slow_relax_fn=lambda: slow_flag[0])
        self.add(phase)

        stiff_t = ValueTracker(0.0)

        def cur_pts():
            return loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=stiff_t.get_value())

        green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)
        top_q = T("Which line has moved?", 34, TEXT, weight=BOLD).move_to([0.75, 3.32, 0])
        sq_lbl, fl_lbl, ld_lbl = build_three_labels(plot, stiff=0.0)

        live_cyan = always_redraw(lambda: make_edpvr_curve(
            plot, stiff=stiff_t.get_value(), x0=5.0, x1=232.0, color=CYAN, width=5.5
        ))
        live_loop = always_redraw(lambda: make_loop_mob(
            plot, cur_pts(), color=WHITE, width=4.8, fill_opacity=0.08
        ))
        dot = make_circling_dot(plot, cur_pts, phase, color=WHITE)

        self.add(plot, live_cyan, green_line, orange_line, live_loop, top_q, sq_lbl, fl_lbl, ld_lbl, dot)

        # Cue: "now heart failure" -> tag top left 'preserved EF'
        self.at("now heart failure")
        tag = cond_tag("preserved EF", CYAN)
        stag = scope_tag("schematic")
        self.play(FadeIn(tag), FadeIn(stag), run_time=0.8)

        # Cue: "the floor moves" -> pulse CYAN floor glow before shifting
        self.at("the floor moves")
        floor_hi = make_edpvr_curve(plot, stiff=0.0, x0=5.0, x1=240.0, color=CYAN, width=10.0, opacity=0.85)
        self.play(FadeIn(floor_hi), run_time=0.6)
        self.play(FadeOut(floor_hi), run_time=0.6)

        # Cue: "catheter studies" -> leave faint CYAN ghost 'normal floor'
        self.at("catheter studies")
        ghost_floor = make_edpvr_curve(plot, stiff=0.0, x0=5.0, x1=240.0, color=CYAN, width=3.5, opacity=0.45, dashed=True)
        nf_lbl = T("normal floor", 24, CYAN).move_to(plot.pt(214, 15))
        self.play(FadeIn(ghost_floor), FadeIn(nf_lbl), run_time=0.6)

        # Cue: "shifted up" -> CYAN curve slides up-left and bends steeper; 'filling' moves to safe spot beside it
        self.at("shifted up")
        self.play(
            stiff_t.animate.set_value(1.0),
            fl_lbl.animate.move_to(filling_label_pos(plot, stiff=1.0)),
            run_time=3.6,
        )

        # Cue: "relaxation was slower" -> dot visibly slows down left side (isovolumic relaxation)
        self.at("relaxation was slower")
        phase.set_value(0.50)
        slow_flag[0] = True
        slow_note = T("slower\nrelaxation", 24, CYAN).move_to(plot.pt(76, 33))
        self.play(FadeIn(slow_note), run_time=0.35)
        self.wait(1.6)
        slow_flag[0] = False
        self.play(FadeOut(slow_note), run_time=0.3)
        self.finish()


def build_s06_world():
    """Shared world builder for S06Predict and S07PredictPause."""
    plot = build_base_plot()
    pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=1.0)
    green_line = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=5.5, max_p=150.0)
    orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)
    ghost_floor = make_edpvr_curve(plot, stiff=0.0, x0=5.0, x1=240.0, color=CYAN, width=3.5, opacity=0.45, dashed=True)
    nf_lbl = T("normal floor", 24, CYAN).move_to(plot.pt(216, 15))
    stiff_cyan = make_edpvr_curve(plot, stiff=1.0, x0=5.0, x1=232.0, color=CYAN, width=5.5)
    loop_mob = make_loop_mob(plot, pts, color=WHITE, width=4.8, fill_opacity=0.08)
    tag = cond_tag("preserved EF", CYAN)
    stag = scope_tag("schematic")
    sq_lbl, fl_lbl, ld_lbl = build_three_labels(plot, stiff=1.0)
    same_v = DashedLine(plot.pt(125, 38), plot.pt(125, 0), color=WHITE, stroke_width=3.5, dash_length=0.12)
    # Narrow stacked 'same\nvolume' at (163, 33) clears both CYAN curves, 140 handgrip loop, and 'higher filling pressure'
    same_lbl = T("same\nvolume", 24, WHITE).move_to(plot.pt(163, 33))
    return VGroup(plot, ghost_floor, nf_lbl, stiff_cyan, green_line, orange_line, loop_mob,
                  tag, stag, sq_lbl, fl_lbl, ld_lbl, same_v, same_lbl), pts, plot


class S06Predict(SpokenScene):
    def construct(self):
        world, pts, plot = build_s06_world()
        phase = ValueTracker(0.25)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        same_v, same_lbl = world[-2], world[-1]
        world.remove(same_v, same_lbl)
        top_q = T("Which line has moved?", 34, TEXT, weight=BOLD).move_to([0.75, 3.32, 0])
        dot = make_circling_dot(plot, lambda: pts, phase, color=WHITE)

        self.add(world, top_q, dot)

        # Cue: "fill this stiffer" -> fade out old question, drop vertical dashed WHITE line from 125 mL
        self.at("fill this stiffer")
        self.play(FadeOut(top_q), run_time=0.4)
        self.play(Create(same_v), FadeIn(same_lbl), run_time=3.2)

        # Cue: "what happens" -> question card at top in white + visible pressure scan along V=125 mL
        self.at("what happens")
        q = question_card("Same volume: what pressure?", y=3.32, color=TEXT, size=32, max_w=7.2)
        q.move_to([1.05, 3.32, 0])
        self.play(FadeIn(q), run_time=1.2)
        probe_p = ValueTracker(10.0)
        probe_line = always_redraw(lambda: Line(
            plot.pt(118.0, probe_p.get_value()), plot.pt(132.0, probe_p.get_value()),
            color=GOLD, stroke_width=5.0,
        ))
        self.add(probe_line)
        self.play(probe_p.animate.set_value(32.5), run_time=1.3)
        self.play(probe_p.animate.set_value(10.0), run_time=1.2)
        self.play(FadeOut(probe_line), run_time=0.3)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Same volume: what pressure?"
    CARD = {"y": 3.32, "color": TEXT, "size": 32, "max_w": 7.2}
    RING_AT = (5.8, 3.32, 0)
    SECONDS = 4.5

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, **self.CARD).move_to([1.05, 3.32, 0])
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()

    def backdrop(self):
        world, pts, plot = build_s06_world()
        phase = ValueTracker(0.25)
        attach_phase_clock(phase, rate=0.18)
        self.add(phase)
        dot = make_circling_dot(plot, lambda: pts, phase, color=WHITE)
        return VGroup(world, dot)


class S08Answer(SpokenScene):
    def construct(self):
        world, base_stiff_pts, plot = build_s06_world()
        phase = ValueTracker(0.15)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        q = question_card("Same volume: what pressure?", y=3.32, color=TEXT, size=32, max_w=7.2).move_to([1.05, 3.32, 0])
        dot = make_circling_dot(plot, lambda: base_stiff_pts, phase, color=WHITE)
        self.add(world, q, dot)

        # Cue: "it runs higher" -> question card dissolves; two crossing dots + vertical CYAN arrow
        self.at("it runs higher")
        p_norm = float(edpvr_p(125.0, stiff=0.0))   # 10.0 mmHg
        p_stiff = float(edpvr_p(125.0, stiff=1.0))  # 32.5 mmHg
        d_norm = Dot(plot.pt(125.0, p_norm), radius=0.10, color=CYAN, stroke_color=WHITE, stroke_width=2)
        d_stiff = Dot(plot.pt(125.0, p_stiff), radius=0.10, color=CYAN, stroke_color=WHITE, stroke_width=2)
        hi_arrow = Arrow(
            plot.pt(125.0, p_norm + 2.0), plot.pt(125.0, p_stiff - 2.0),
            color=CYAN, stroke_width=5, tip_length=0.18, buff=0.0,
        )
        # Put 'higher filling pressure' cleanly in the open wedge at (200, 62), clear of both CYAN curves, 'same volume', and 140 handgrip loop
        hi_lbl = T("higher filling\npressure", 24, CYAN).move_to(plot.pt(200.0, 62.0))
        self.play(
            FadeOut(q),
            FadeIn(d_norm), FadeIn(d_stiff),
            GrowArrow(hi_arrow), FadeIn(hi_lbl),
            run_time=2.2,
        )

        # Cue: "a catheter study" -> small card at right: 'catheter study, 70 people'
        self.at("a catheter study")
        study_card = boxed_label("catheter study\n70 people", TEXT, size=24, pad=0.18).move_to([5.48, 2.35, 0])
        self.play(FadeIn(study_card), run_time=1.2)

        # Cue: "found stiffer" -> pulse stiff dot & curve to emphasize rest stiffness
        self.at("found stiffer")
        self.play(d_stiff.animate.scale(1.4), run_time=0.6)
        self.play(d_stiff.animate.scale(1.0 / 1.4), run_time=0.6)

        # Cue: "when handgrip" -> fist icon squeezes, ORANGE tilts steeper (1.5->1.78), MAGENTA corner climbs shifted CYAN curve
        self.at("when handgrip")
        fist = make_handgrip_icon([5.45, 0.35, 0], color=ORANGE)
        fist_lbl = T("handgrip", 24, ORANGE).next_to(fist, DOWN, buff=0.14)
        self.play(FadeIn(fist), FadeIn(fist_lbl), run_time=0.5)

        ea_t = ValueTracker(1.5)
        edv_hg_t = ValueTracker(125.0)
        static_orange, static_loop = world[5], world[6]
        self.remove(static_orange, static_loop)

        def hg_params():
            edv = edv_hg_t.get_value()
            ea = ea_t.get_value()
            sv, esv, pes = solve_crossing(edv=edv, v0=5.0, ees=3.0, ea=ea)
            return edv, ea, esv, pes

        def hg_pts():
            edv, _, esv, pes = hg_params()
            return loop_vp_points(edv=edv, esv=esv, pes=pes, p_ao_open=80.0, stiff=1.0)

        live_orange = always_redraw(lambda: make_ea_line(
            plot, edv=edv_hg_t.get_value(), ea=ea_t.get_value(), v_stop=hg_params()[2], color=ORANGE, width=5.5
        ))
        live_hg_loop = always_redraw(lambda: make_loop_mob(
            plot, hg_pts(), color=MAGENTA, width=5.0, fill_opacity=0.14
        ))
        ghost_corner = always_redraw(lambda: Dot(
            plot.pt(edv_hg_t.get_value(), float(edpvr_p(edv_hg_t.get_value(), stiff=0.0))),
            radius=0.09, color=WHITE, stroke_color=CYAN, stroke_width=2,
        ))
        stiff_corner = always_redraw(lambda: Dot(
            plot.pt(edv_hg_t.get_value(), float(edpvr_p(edv_hg_t.get_value(), stiff=1.0))),
            radius=0.11, color=MAGENTA, stroke_color=WHITE, stroke_width=2,
        ))
        self.remove(dot)
        live_dot = make_circling_dot(plot, hg_pts, phase, color=WHITE)
        self.add(live_orange, live_hg_loop, ghost_corner, stiff_corner, live_dot)

        self.play(
            fist.animate.scale(0.84),
            ea_t.animate.set_value(1.78),
            edv_hg_t.animate.set_value(140.0),
            run_time=2.6,
        )
        self.wait(1.4)
        self.play(
            fist.animate.scale(1.0 / 0.84),
            ea_t.animate.set_value(1.5),
            edv_hg_t.animate.set_value(125.0),
            run_time=2.0,
        )

        # Cue: "did not show" -> 'cause?' question mark settles beside shifted CYAN curve (in clear right space)
        self.at("did not show")
        cause_tag = boxed_label("cause?", GOLD, size=26, pad=0.16).move_to(plot.pt(232.0, 92.0))
        self.play(
            FadeOut(fist), FadeOut(fist_lbl),
            FadeOut(ghost_corner), FadeOut(stiff_corner),
            FadeIn(cause_tag),
            run_time=0.8,
        )
        self.finish()


class S09SlopeCaution(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.20)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        ees_t = ValueTracker(3.0)
        pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=1.0)
        ghost_floor = make_edpvr_curve(plot, stiff=0.0, x0=5.0, x1=240.0, color=CYAN, width=3.5, opacity=0.45, dashed=True)
        nf_lbl = T("normal floor", 24, CYAN).move_to(plot.pt(214, 15))
        stiff_cyan = make_edpvr_curve(plot, stiff=1.0, x0=5.0, x1=232.0, color=CYAN, width=5.5)
        orange_line = make_ea_line(plot, edv=125.0, ea=1.5, v_stop=45.0, color=ORANGE, width=5.5)
        loop_mob = make_loop_mob(plot, pts, color=WHITE, width=4.8, fill_opacity=0.08)
        tag = cond_tag("preserved EF", CYAN)
        stag = scope_tag("schematic")
        sq_lbl, fl_lbl, ld_lbl = build_three_labels(plot, stiff=1.0)
        cause_tag = boxed_label("cause?", GOLD, size=26, pad=0.16).move_to(plot.pt(232.0, 92.0))

        base_green = make_espvr_line(plot, v0=5.0, ees=3.0, color=GREEN, width=3.5, max_p=150.0, opacity=0.40)
        steep_green = always_redraw(lambda: make_espvr_line(
            plot, v0=5.0, ees=ees_t.get_value(), color=GREEN, width=5.5, max_p=150.0, dashed=True
        ))
        dot = make_circling_dot(plot, lambda: pts, phase, color=WHITE)

        self.add(plot, ghost_floor, nf_lbl, stiff_cyan, base_green, steep_green, orange_line, loop_mob,
                 tag, stag, sq_lbl, fl_lbl, ld_lbl, cause_tag, dot)

        # Cue: "steeper too" -> GREEN line pivots steeper (dashed, schematic)
        self.at("steeper too")
        self.play(ees_t.animate.set_value(4.8), run_time=1.8)

        # Cue: "whole chamber" -> 'squeeze' splits into 'muscle' and 'walls + stiffness'
        self.at("whole chamber")
        muscle_tag = boxed_label("muscle", GREEN, size=24, pad=0.14, fill_opacity=0.10).move_to(plot.pt(96.0, 144.0))
        walls_tag = boxed_label("walls + stiffness", CYAN, size=24, pad=0.14, fill_opacity=0.10).move_to(plot.pt(160.0, 144.0))
        self.play(FadeOut(sq_lbl), run_time=0.35)
        self.play(FadeIn(muscle_tag), FadeIn(walls_tag), run_time=0.8)

        # Cue: "thick walls" -> 'walls + stiffness' tag glows and stiff cyan + loop floor pulse
        self.at("thick walls")
        stiff_flash = make_edpvr_curve(plot, stiff=1.0, x0=5.0, x1=232.0, color=WHITE, width=10.5)
        self.play(
            walls_tag.box.animate.set_stroke(YELLOW, width=6.5),
            stiff_cyan.animate.set_stroke(width=11.0),
            loop_mob.animate.set_fill(CYAN, opacity=0.22),
            run_time=1.6,
        )
        self.play(
            ShowPassingFlash(stiff_flash, time_width=0.6),
            walls_tag.box.animate.set_stroke(CYAN, width=2.5),
            stiff_cyan.animate.set_stroke(width=5.5),
            loop_mob.animate.set_fill(WHITE, opacity=0.08),
            run_time=1.8,
        )

        # Cue: "community study" -> highlight steep GREEN line with passing flash, then drop 'muscle' tag downward
        self.at("community study")
        steep_static = make_espvr_line(plot, v0=5.0, ees=4.8, color=GREEN, width=5.5, max_p=150.0, dashed=True)
        self.remove(steep_green)
        self.add(steep_static)
        steep_glow = make_espvr_line(plot, v0=5.0, ees=4.8, color=YELLOW, width=10.0, max_p=150.0)
        self.play(ShowPassingFlash(steep_glow, time_width=0.6), run_time=2.8)

        self.at("depressed")
        muscle_down = boxed_label("muscle ↓", GREEN, size=24, pad=0.14, fill_opacity=0.06).move_to(
            muscle_tag.get_center() + DOWN * 0.45
        )
        muscle_down.label.set_opacity(0.85)
        muscle_down.box.set_stroke(opacity=0.65)
        self.play(swap(muscle_tag, muscle_down, run_time=1.6))

        # Cue: "need not mean" -> 'muscle ↓' tag and steep dashed GREEN line pulse once
        self.at("need not mean")
        self.play(
            muscle_down.animate.scale(1.12),
            steep_static.animate.set_stroke(width=9.0),
            run_time=0.5,
        )
        self.play(
            muscle_down.animate.scale(1.0 / 1.12),
            steep_static.animate.set_stroke(width=5.5),
            run_time=0.5,
        )
        self.finish()


class S10AorticStenosis(SpokenScene):
    def construct(self):
        plot = build_base_plot()
        phase = ValueTracker(0.10)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        ea_t = ValueTracker(1.5)
        ees_t = ValueTracker(3.0)
        dome_t = ValueTracker(0.0)
        openness_t = ValueTracker(1.0)

        def cur_params():
            ea = ea_t.get_value()
            ees = ees_t.get_value()
            sv, esv, pes = solve_crossing(edv=125.0, v0=5.0, ees=ees, ea=ea)
            return ea, ees, sv, esv, pes

        def cur_pts():
            _, _, _, esv, pes = cur_params()
            return loop_vp_points(edv=125.0, esv=esv, pes=pes, p_ao_open=80.0, stiff=0.0, dome=dome_t.get_value())

        cyan_curve = make_edpvr_curve(plot, stiff=0.0, x0=5.0, x1=240.0, color=CYAN, width=5.0)
        live_green = always_redraw(lambda: make_espvr_line(
            plot, v0=5.0, ees=ees_t.get_value(), color=GREEN, width=5.5, max_p=154.0
        ))
        live_orange = always_redraw(lambda: make_ea_line(
            plot, edv=125.0, ea=ea_t.get_value(), v_stop=cur_params()[3], color=ORANGE, width=5.5
        ))
        live_loop = always_redraw(lambda: make_loop_mob(
            plot, cur_pts(), color=MAGENTA if dome_t.get_value() > 0.5 else WHITE, width=5.0, fill_opacity=0.12
        ))
        dot = make_circling_dot(plot, cur_pts, phase, color=WHITE)

        sq_lbl, fl_lbl, ld_lbl = build_three_labels(plot, stiff=0.0)
        tag = cond_tag("aortic stenosis", MAGENTA)
        stag = scope_tag("schematic")
        # Place valve icon cleanly on the ORANGE line at V=106, P=33 (above SV arrow at P=14, right of 'load' at (76,56))
        valve = always_redraw(lambda: make_valve_icon(
            plot.pt(106.0, float(ea_t.get_value() * (125.0 - 106.0))),
            openness=openness_t.get_value(), color=ORANGE
        ))
        valve.layout_ok = True

        self.add(plot, cyan_curve, live_green, live_orange, live_loop, sq_lbl, fl_lbl, ld_lbl, tag, stag, valve, dot)

        # Cue: "the narrowed valve" -> valve icon narrows to slit; ORANGE line tilts steeper
        self.at("the narrowed valve")
        self.play(
            openness_t.animate.set_value(0.10),
            ea_t.animate.set_value(1.75),
            run_time=2.2,
        )

        # Cue: "ventricular pressure climbs" -> loop becomes MAGENTA and top domes upward well above 120 mmHg
        self.at("ventricular pressure climbs")
        self.play(dome_t.animate.set_value(20.0), run_time=2.8)

        # Cue: "a thickened wall" -> GREEN line steepens too (3.0 -> 3.6); YELLOW SV arrow holds near baseline length
        self.at("a thickened wall")
        sv_arrow = always_redraw(lambda: DoubleArrow(
            plot.pt(cur_params()[3], 13.0), plot.pt(125.0, 13.0),
            color=YELLOW, stroke_width=5, tip_length=0.18, buff=0.0,
        ))
        sv_lbl = T("SV", 24, YELLOW).move_to(plot.pt(85.0, 26.0))
        self.add(sv_arrow, sv_lbl)
        self.play(ees_t.animate.set_value(3.6), run_time=2.6)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        phase = ValueTracker(0.10)
        attach_phase_clock(phase, rate=0.34)
        self.add(phase)

        specs = [
            ("reduced EF", (-6.0, -2.3, -1.7, 2.0),
             dict(edv=215.0, esv=158.0, pes=85.0, p_ao=57.0, v0=95.0, ees=1.35, ea=1.5, stiff=0.0, vs=80.0, dome=0.0),
             "squeeze", GREEN, (85, 60)),
            ("preserved EF", (-1.85, 1.85, -1.7, 2.0),
             dict(edv=125.0, esv=45.0, pes=120.0, p_ao=80.0, v0=5.0, ees=3.0, ea=1.5, stiff=1.0, vs=0.0, dome=0.0),
             "filling", CYAN, (118, 134)),
            ("aortic stenosis", (2.3, 6.0, -1.7, 2.0),
             dict(edv=125.0, esv=44.3, pes=140.0, p_ao=80.0, v0=5.0, ees=3.6, ea=1.75, stiff=0.0, vs=0.0, dome=20.0),
             "load", ORANGE, (172, 102)),
        ]

        base_pts = loop_vp_points(125.0, 45.0, 120.0, 80.0, stiff=0.0)
        panels = []
        moved_lines = {}
        role_tags = {}

        for title_txt, box, p, role_txt, role_col, norm_vp in specs:
            P = Plot(box=box, xr=PLOT_XR, yr=PLOT_YR, xticks=[], yticks=[], xlabel="", ylabel="", color=GREY, stroke=2.5)
            head = T(title_txt, 28, TEXT, weight=BOLD).move_to([(box[0] + box[1]) / 2, 2.45, 0])
            ghost = make_loop_mob(P, base_pts, color=WHITE, width=2.8, dashed=True, opacity=0.55)
            ghost_lbl = T("normal", 22, WHITE).move_to(P.pt(*norm_vp))
            cyan = make_edpvr_curve(P, stiff=p["stiff"], v_shift=p["vs"], x0=5.0, x1=235.0, color=CYAN, width=4.0)
            green = make_espvr_line(P, v0=p["v0"], ees=p["ees"], color=GREEN, width=4.0, max_p=152.0)
            orange = make_ea_line(P, edv=p["edv"], ea=p["ea"], v_stop=p["esv"], color=ORANGE, width=4.0)
            pts = loop_vp_points(edv=p["edv"], esv=p["esv"], pes=p["pes"], p_ao_open=p["p_ao"],
                                 stiff=p["stiff"], v_shift=p["vs"], dome=p["dome"])
            loop = make_loop_mob(P, pts, color=MAGENTA, width=4.5, fill_opacity=0.14)
            dot = make_circling_dot(P, (lambda q=pts: q), phase, color=WHITE, radius=0.08, trail_frac=0.22)
            role = boxed_label(role_txt, role_col, size=26, pad=0.15).move_to([(box[0] + box[1]) / 2, -2.35, 0])

            grp = VGroup(P, head, ghost, ghost_lbl, cyan, green, orange, loop, role)
            panels.append((grp, dot))
            moved_lines[role_txt] = {"squeeze": green, "filling": cyan, "load": orange}[role_txt]
            role_tags[role_txt] = role

        stag = scope_tag("schematic")

        # Reveal each plot as the narrator names it!
        self.at("reduced ejection")
        self.play(FadeIn(panels[0][0]), FadeIn(stag), run_time=1.0)
        self.add(panels[0][1])

        self.at("preserved ejection")
        self.play(FadeIn(panels[1][0]), run_time=1.0)
        self.add(panels[1][1])

        self.at("narrowed valve")
        self.play(FadeIn(panels[2][0]), run_time=1.0)
        self.add(panels[2][1])

        # Cue: "each moves" -> sweep emphasis across the three moved lines before the final roll call
        self.at("each moves")
        self.play(
            moved_lines["squeeze"].animate.set_stroke(width=7.5),
            moved_lines["filling"].animate.set_stroke(width=7.5),
            moved_lines["load"].animate.set_stroke(width=7.5),
            run_time=1.0,
        )
        self.play(
            moved_lines["squeeze"].animate.set_stroke(width=4.0),
            moved_lines["filling"].animate.set_stroke(width=4.0),
            moved_lines["load"].animate.set_stroke(width=4.0),
            run_time=0.8,
        )

        # Cue: "squeeze" -> moved GREEN line glows in first copy
        self.at("squeeze")
        self.play(moved_lines["squeeze"].animate.set_stroke(width=8.5), role_tags["squeeze"].box.animate.set_stroke(width=5), run_time=0.5)

        # Cue: "filling" -> moved CYAN floor glows in second copy
        self.at("filling")
        self.play(moved_lines["filling"].animate.set_stroke(width=8.5), role_tags["filling"].box.animate.set_stroke(width=5), run_time=0.5)

        # Cue: "load" -> steeper ORANGE line glows in third copy
        self.at("load")
        self.play(moved_lines["load"].animate.set_stroke(width=8.5), role_tags["load"].box.animate.set_stroke(width=5), run_time=0.5)
        self.finish()


class S12End(EndCard):
    LINE = "To read a sick heart, ask which line has moved."
