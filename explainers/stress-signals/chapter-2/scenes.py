"""Pulses and Persistence: How Timing Sets Fate (stress-signals, chapter 2).

COLOUR MAP (one colour per concept for the whole film):
- TEAL (#3FB8C0): stress responders (p53; ER sensors IRE1, PERK, ATF6) and repair / recovery
- GOLD (#D4A843): restraints and chaperones (MDM2, MDM2 blocker, BiP)
- RED  (#FC6255): stress triggers (gamma rays, unfolded chains) and permanent arrest / senescence / death (CHOP, JNK)
- TEXT (#E8EAF0): population averages (dish blot average), neutral questions, hypothetical dimmer dial, panel labels
- GREY (#8B93A1): axes, cell outlines, membranes, structural dividers, schematic tag

CARRIED WORLD:
A two-panel live-cell monitor (living cell / organelle viewport on the left, computed signal-over-time
and fate monitor on the right) carried across scenes in the same frame coordinates.

SCENE-BY-SCENE COMPUTED MOTION:
- s01_hook: Restraint lifts and computed p53 level climbs inside four cells; coral damage tracker drives
  a hypothetical dimmer dial up via ValueTracker, then a microscope focus ring narrows onto one cell.
- s02_blot_vs_single: Live time tracker draws the damped dish-blot average curve synced with pooled cell
  brightness, then fires uniform single-cell Gaussian pulses while a coral dose tracker adds pulses (1 -> 2 -> 3).
- s03_average_math: Sweeping slot cursor t in [0, 4] drives four staggered Gaussian spikes peaking at 80,
  live cell numbers (80 or 0), the arithmetic readout (80 + 0 + 0 + 0) / 4 = 20, and the flat 20 average line
  plus the computed out-of-step 20-cell mean wave.
- s04_predict_q: Two computed traces of equal peak height build side by side (three pulses vs MDM2-blocked
  plateau) while a fate pointer settles at the '?' midpoint and the question card appears at top.
- s06_reveal_fate: Pulsed fate bar fills teal as the top cell pinches and divides into two; steady fate
  bar fills coral as the bottom cell locks inside a ring; cumulative areas grow and equal-total bars compare.
- s07_upr_bridge: Secreted protein ribbons travel through the ER pore and fold with BiP helpers, then coral
  unfolded chains accumulate, pulling amber BiP off IRE1/PERK/ATF6 so sensors brighten and hold teal repair.
- s08_upr_death_scope: Growing coral stress-duration bar shifts the fate meter from teal into coral death,
  lights arrows from PERK -> CHOP and IRE1 -> JNK, and sweeps across a shaded repair-death overlap zone.
- s09_closing: Side-by-side pulsed vs sustained traces draw live across the same time axis, then a single
  vertical snapshot cursor sweeps to one shared height before widening into a full-timeline sweep.
"""

from bp_parts import *

# Semantic concept colours (shared across the entire film)
RESPONDER = TEAL
REPAIR = TEAL
RESTRAINT = GOLD
STRESS = RED
ARREST = RED
AVERAGE = TEXT
STRUCT = GREY

RNG_SEED = 7


# ------------------------------------------------------------------ computed signal math
def damped_blot(t):
    """Smooth damped single wave seen on a whole-dish blot (schematic)."""
    if t <= 0:
        return 0.0
    return float(0.76 * (t / 2.2) * np.exp(1.0 - t / 2.2) * (1.0 + 0.14 * np.sin(1.7 * t)))


def pulse_train(t, centers, width=0.52, peak=0.88):
    """Sum of Gaussian pulses of fixed peak height and width."""
    return float(sum(peak * np.exp(-0.5 * ((t - c) / width) ** 2) for c in centers))


def steady_plateau(t, t_on=0.8, peak=0.88):
    """Drug-clamped p53 plateau held at the height of one natural pulse."""
    if t <= 0:
        return 0.0
    return float(peak * (1.0 - np.exp(-t / 0.45))) if t >= t_on * 0.2 else 0.0


def spike_slot(t, slot_idx, sigma=0.20, peak=80.0):
    """Single cell spike centered in hour slot `slot_idx` (0..3) peaking at 80."""
    return float(peak * np.exp(-0.5 * ((t - (slot_idx + 0.5)) / sigma) ** 2))


def blended_wave(t, n_cells=20):
    """True mean of out-of-step pulses peaking at 80, normalized to mean 20 across [0, 4]."""
    rng = np.random.default_rng(RNG_SEED)
    centers = np.linspace(-1.0, 5.0, 31) + rng.uniform(-0.08, 0.08, size=31)
    sigma = 0.38
    xs = np.linspace(0.0, 4.0, 81)[:, None]
    mean_v = float(np.mean(np.sum(80.0 * np.exp(-0.5 * ((xs - centers[None, :]) / sigma) ** 2), axis=1) / n_cells))
    val = float(np.sum(80.0 * np.exp(-0.5 * ((t - centers) / sigma) ** 2)) / n_cells)
    return val * (20.0 / mean_v)


# ------------------------------------------------------------------ shared carried builders
def make_monitor(left_title="Living cells", right_title="p53 signal",
                 left_col=TEXT, right_col=RESPONDER, top=3.1, bottom=-2.5):
    """Carried two-panel monitor filling the main stage."""
    return TwoPanel(left_title, right_title, colors=(left_col, right_col),
                    top=top, bottom=bottom, gap=0.4, width=12.6, size=30)


def make_cell(center, radius_w=2.1, radius_h=1.55, nuc_r=0.42,
              border_col=STRUCT, nuc_opacity=0.22, label=None, label_size=26):
    """A simple living cell: rounded outer membrane + teal p53 nuclear core."""
    body = RoundedRectangle(
        corner_radius=0.52, width=radius_w, height=radius_h,
        stroke_color=border_col, stroke_width=3,
        fill_color=RESPONDER, fill_opacity=0.05,
    ).move_to(center)
    nuc = Circle(
        radius=nuc_r, stroke_color=RESPONDER, stroke_width=3,
        fill_color=RESPONDER, fill_opacity=nuc_opacity,
    ).move_to(center)
    g = VGroup(body, nuc)
    g.body, g.nuc = body, nuc
    if label:
        lab = T(label, label_size, TEXT).move_to(center)
        g.add(lab)
        g.lab = lab
    return g


def make_fate_bar(center, width=4.8, height=0.38, left_text="Recover", right_text="Permanent arrest",
                  frac=0.5, show_q=False):
    """Split Repair-vs-Arrest fate meter with a movable marker driven by `frac` (0=teal, 1=coral)."""
    c = np.array(center, dtype=float)
    left_box = RoundedRectangle(
        corner_radius=0.12, width=width / 2, height=height,
        stroke_color=REPAIR, stroke_width=2.5, fill_color=REPAIR, fill_opacity=0.26,
    ).move_to(c + LEFT * (width / 4))
    right_box = RoundedRectangle(
        corner_radius=0.12, width=width / 2, height=height,
        stroke_color=ARREST, stroke_width=2.5, fill_color=ARREST, fill_opacity=0.26,
    ).move_to(c + RIGHT * (width / 4))
    l_lab = T(left_text, 24, REPAIR).next_to(left_box, DOWN, buff=0.12).align_to(left_box, LEFT)
    r_lab = T(right_text, 24, ARREST).next_to(right_box, DOWN, buff=0.12).align_to(right_box, RIGHT)
    mx = c[0] + (frac - 0.5) * (width - 0.35)
    marker = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1.0, stroke_width=2).scale(0.15)
    marker.rotate(PI).move_to([mx, c[1] + height / 2 + 0.16, 0])
    g = VGroup(left_box, right_box, l_lab, r_lab, marker)
    g.left_box, g.right_box, g.l_lab, g.r_lab, g.marker = left_box, right_box, l_lab, r_lab, marker
    g.bar_center, g.bar_width, g.bar_height = c, width, height
    if show_q:
        q = T("?", 26, RESTRAINT, weight=BOLD).next_to(marker, UP, buff=0.05)
        g.add(q)
        g.q = q
    return g


# ------------------------------------------------------------------ scene 00
class S00Title(TitleCard):
    LESSON = "Stress Signals: p38 and JNK, p53, Unfolded Proteins and Oxidants"
    TITLE = "Pulses and Persistence: How Timing Sets Fate"


# ------------------------------------------------------------------ scene 01
class S01Hook(SpokenScene):
    def construct(self):
        tp = make_monitor("Living cells", "p53 signal", TEXT, RESPONDER)
        tag = scope_tag("schematic")

        cell_pos = [(-4.65, 0.90, 0), (-1.95, 0.90, 0), (-4.65, -0.95, 0), (-1.95, -0.95, 0)]
        p53_lvl = ValueTracker(0.10)
        cells = VGroup()
        restraint_caps = VGroup()
        for i, pos in enumerate(cell_pos):
            lbl = "p53" if i == 0 else None
            c = make_cell(pos, radius_w=2.15, radius_h=1.55, nuc_r=0.45,
                          nuc_opacity=0.12, label=lbl, label_size=26)
            cells.add(c)
            cap = Arc(radius=0.54, start_angle=PI * 0.15, angle=PI * 0.7,
                      arc_center=pos, color=RESTRAINT, stroke_width=6)
            restraint_caps.add(cap)

        for c in cells:
            c.nuc.add_updater(lambda m, lv=p53_lvl: m.set_fill(
                RESPONDER, opacity=float(np.clip(lv.get_value() * 0.38, 0.08, 0.36))
            ).set_stroke(width=2.5 + 4.5 * lv.get_value()))

        restraint_tag = boxed_label("restraint", RESTRAINT, size=22, pad=0.10).move_to([-3.3, 2.02, 0])

        plot = Plot(
            box=(1.1, 5.9, 0.25, 1.90), xr=(0, 5), yr=(0, 1.15),
            xticks=[2, 5], yticks=[(0, "low"), (1, "high")],
            xlabel="time", ylabel="p53 level", color=STRUCT, size=22, label_size=24,
        )
        t_climb = ValueTracker(0.0)
        climb_fn = lambda x: 0.12 + 0.82 * (1.0 - np.exp(-0.9 * x))
        climb_curve = plot.live_curve(climb_fn, t_climb, color=RESPONDER, width=6)
        climb_dot = plot.dot(lambda: t_climb.get_value(), lambda: climb_fn(t_climb.get_value()), color=TEXT, ring=RESPONDER)

        rep_chip = boxed_label("Repair", REPAIR, size=26, pad=0.16).move_to([1.55, -1.78, 0])
        q_mark = T("?", 32, RESTRAINT, weight=BOLD).move_to([2.70, -1.78, 0])
        arr_chip = boxed_label("Permanent arrest", ARREST, size=22, pad=0.12).move_to([4.55, -1.78, 0])

        self.play(FadeIn(tp), FadeIn(cells), FadeIn(restraint_caps), FadeIn(restraint_tag),
                  FadeIn(plot), FadeIn(tag), run_time=1.4)

        self.at("removing a restraint")
        self.add(climb_curve, climb_dot)
        self.play(
            FadeOut(restraint_caps, shift=UP * 0.25),
            FadeOut(restraint_tag, shift=UP * 0.15),
            t_climb.animate.set_value(4.8),
            p53_lvl.animate.set_value(1.0),
            run_time=4.4,
        )

        self.at("Once P53 rises")
        arr_l = Arrow([3.10, -0.78, 0], [1.80, -1.32, 0], color=REPAIR, stroke_width=4, buff=0.04)
        arr_r = Arrow([3.50, -0.78, 0], [4.50, -1.32, 0], color=ARREST, stroke_width=4, buff=0.04)
        self.play(GrowArrow(arr_l), FadeIn(rep_chip), run_time=2.6)
        self.play(Indicate(rep_chip, color=REPAIR), run_time=1.2)
        self.at("permanent arrest")
        self.play(GrowArrow(arr_r), FadeIn(arr_chip), FadeIn(q_mark), run_time=2.0)

        self.at("Does heavier damage")
        bolts = VGroup(*[
            Arrow(np.array(p) + np.array([-1.02, 0.55, 0]), np.array(p) + np.array([-0.55, 0.25, 0]),
                  color=STRESS, stroke_width=5, buff=0.04, max_tip_length_to_length_ratio=0.32)
            for p in cell_pos
        ])
        for c in cells:
            c.nuc.clear_updaters()

        dim_val = ValueTracker(0.18)
        dim_dial = dial(dim_val, center=[3.3, 0.38, 0], radius=1.35, label="dimmer dial ?",
                        color=AVERAGE, fmt="{:.0f}%", scale=100.0, size=36)
        dmg_bar_bg = RoundedRectangle(corner_radius=0.1, width=3.8, height=0.28,
                                      stroke_color=STRESS, stroke_width=2, fill_opacity=0.14).move_to([3.3, -1.58, 0])
        dmg_lab = T("heavier damage", 24, STRESS).next_to(dmg_bar_bg, DOWN, buff=0.14)
        dmg_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08,
            width=max(0.25, 3.72 * dim_val.get_value()),
            height=0.22, stroke_width=0, fill_color=STRESS, fill_opacity=0.85,
        ).align_to(dmg_bar_bg, LEFT).shift(RIGHT * 0.04).set_y(dmg_bar_bg.get_y()))

        self.play(FadeOut(VGroup(plot, climb_curve, climb_dot, rep_chip, arr_chip, q_mark, arr_l, arr_r), run_time=0.45))
        self.play(
            FadeIn(bolts), FadeIn(dim_dial), FadeIn(dmg_bar_bg), FadeIn(dmg_fill), FadeIn(dmg_lab),
            dim_val.animate.set_value(0.92),
            run_time=4.4, rate_func=linear,
        )

        self.at("To find out")
        focus_ring = RoundedRectangle(
            corner_radius=0.58, width=2.32, height=1.70,
            stroke_color=RESPONDER, stroke_width=6,
        ).move_to(cell_pos[0])
        focus_ring_start = RoundedRectangle(
            corner_radius=1.2, width=4.4, height=3.6,
            stroke_color=RESPONDER, stroke_width=3,
        ).move_to([-3.3, 0.15, 0])
        empty_plot = Plot(
            box=(1.1, 5.9, -1.2, 1.5), xr=(0, 10), yr=(0, 1.1),
            xticks=[5, 10], yticks=[(0, "0"), (1, "peak")],
            xlabel="time", ylabel="single-cell p53", color=STRUCT, size=22, label_size=24,
        )
        one_lab = T("1 living cell", 26, RESPONDER).move_to([-3.3, -2.12, 0])

        self.play(FadeOut(VGroup(dim_dial, dmg_bar_bg, dmg_fill, dmg_lab, bolts)), run_time=0.45)
        self.play(
            FadeIn(empty_plot),
            cells[1].animate.set_opacity(0.22),
            cells[2].animate.set_opacity(0.22),
            cells[3].animate.set_opacity(0.22),
            Transform(focus_ring_start, focus_ring),
            FadeIn(one_lab),
            run_time=2.5,
        )
        self.finish()


# ------------------------------------------------------------------ scene 02
class S02BlotVsSingle(SpokenScene):
    def construct(self):
        tp = make_monitor("Dish of millions of cells", "p53 level over time", TEXT, RESPONDER)
        tag = scope_tag("schematic")

        rng = np.random.default_rng(RNG_SEED)
        crowd = VGroup()
        for r in range(4):
            for c in range(4):
                x = -4.8 + c * 1.0
                y = 1.45 - r * 0.85
                cell = Circle(radius=0.30, stroke_color=STRUCT, stroke_width=2,
                              fill_color=RESPONDER, fill_opacity=0.14).move_to([x, y, 0])
                cell._phase = float(rng.uniform(0.0, 1.0))
                crowd.add(cell)
        blot_lbl = T("millions -> dish blot", 26, AVERAGE).move_to([-3.3, -2.02, 0])

        plot = Plot(
            box=(1.1, 5.9, -0.7, 1.75), xr=(0, 10), yr=(0, 1.15),
            xticks=[5, 10], yticks=[(0, "0"), (0.88, "peak")],
            xlabel="time", ylabel="p53 level", color=STRUCT, size=22, label_size=24,
        )
        t_blot = ValueTracker(0.0)
        blot_curve = plot.live_curve(damped_blot, t_blot, color=AVERAGE, width=5)
        blot_dot = always_redraw(lambda: Dot(
            plot.pt(t_blot.get_value(), damped_blot(t_blot.get_value())),
            radius=0.10 if t_blot.get_value() > 0.15 else 0.0,
            color=AVERAGE, stroke_color=AVERAGE, stroke_width=2,
        ))
        blot_name = T("dish blot average", 24, AVERAGE).move_to([4.55, 1.48, 0])

        for c in crowd:
            c.add_updater(lambda m: m.set_fill(
                RESPONDER,
                opacity=float(np.clip(0.12 + 0.68 * damped_blot(t_blot.get_value() + 0.5 * m._phase), 0.12, 0.82))
            ))

        self.play(FadeIn(tp), FadeIn(crowd), FadeIn(blot_lbl), FadeIn(plot), FadeIn(tag), run_time=1.0)
        rad_flash = VGroup(*[
            Arrow([-5.8, 1.45 - r * 0.85, 0], [-5.2, 1.45 - r * 0.85, 0], color=STRESS, stroke_width=4, buff=0.02)
            for r in range(4)
        ])
        self.play(FadeIn(rad_flash), run_time=1.2)
        self.play(FadeOut(rad_flash), run_time=1.2)

        self.at("P53 rises")
        self.add(blot_curve, blot_dot)
        self.play(t_blot.animate.set_value(9.6), FadeIn(blot_name), run_time=5.4, rate_func=linear)

        self.at("looks like a dial")
        dial_note = boxed_label("looks like a dimmer dial", AVERAGE, size=24, pad=0.14).move_to([3.3, -1.95, 0])
        self.play(FadeIn(dial_note), run_time=1.6)

        self.at("Film single living cells")
        for c in crowd:
            c.clear_updaters()
        single_pos = [(-4.7, 1.25, 0), (-3.3, 1.25, 0), (-1.9, 1.25, 0)]
        single_cells = VGroup(*[
            make_cell(p, radius_w=1.18, radius_h=1.45, nuc_r=0.34,
                      border_col=RESPONDER if i == 0 else STRUCT,
                      nuc_opacity=0.15, label=f"C{i+1}", label_size=22)
            for i, p in enumerate(single_pos)
        ])
        cell_note = T("single living cells", 26, RESPONDER).move_to([-3.3, 0.15, 0])

        t_sc = ValueTracker(0.0)
        dose_val = ValueTracker(0.33)
        dose_track = RoundedRectangle(corner_radius=0.08, width=4.2, height=0.28,
                                      stroke_color=STRESS, stroke_width=2, fill_opacity=0.14).move_to([-3.3, -1.1, 0])
        dose_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.06, width=max(0.25, 4.12 * dose_val.get_value()), height=0.22,
            stroke_width=0, fill_color=STRESS, fill_opacity=0.85,
        ).align_to(dose_track, LEFT).shift(RIGHT * 0.04).set_y(dose_track.get_y()))
        dose_lab = T("gamma dose", 25, STRESS).move_to([-3.3, -0.68, 0])

        pulse_count_lbl = always_redraw(lambda: M(
            f"pulses: {sum(t_sc.get_value() >= c for c in (2.0, 5.0, 8.0))}",
            26, RESPONDER,
        ).move_to([-3.3, -1.78, 0]))

        static_blot = plot.curve(damped_blot, color=AVERAGE, width=3, opacity=0.28)
        self.remove(blot_curve, blot_dot)
        self.add(static_blot)

        centers = [2.0, 5.0, 8.0]
        sc_fn = lambda x: pulse_train(x, centers, width=0.52, peak=0.88)
        sc_curve = plot.live_curve(sc_fn, t_sc, color=RESPONDER, width=6)
        sc_dot = always_redraw(lambda: Dot(
            plot.pt(t_sc.get_value(), sc_fn(t_sc.get_value())),
            radius=0.10 if (0.15 < t_sc.get_value() < 9.85) else 0.0,
            color=TEXT, stroke_color=RESPONDER, stroke_width=3,
        ))
        sc_cursor = always_redraw(lambda: DashedLine(
            plot.pt(t_sc.get_value(), 0), plot.pt(t_sc.get_value(), 1.05),
            color=RESPONDER, stroke_width=2, dash_length=0.10,
        ) if (0.15 < t_sc.get_value() < 9.85) else VMobject())

        single_cells[0].nuc.add_updater(
            lambda m: m.set_fill(RESPONDER, opacity=float(np.clip(0.12 + 0.32 * sc_fn(t_sc.get_value()), 0.12, 0.42)))
                .set_stroke(width=2.5 + 4.5 * sc_fn(t_sc.get_value()))
        )
        single_cells[1].nuc.add_updater(
            lambda m: m.set_fill(RESPONDER, opacity=float(np.clip(0.12 + 0.32 * pulse_train(t_sc.get_value(), [1.0, 4.0, 7.0]), 0.12, 0.42)))
        )
        single_cells[2].nuc.add_updater(
            lambda m: m.set_fill(RESPONDER, opacity=float(np.clip(0.12 + 0.32 * pulse_train(t_sc.get_value(), [3.1, 6.1, 9.1]), 0.12, 0.42)))
        )

        peak_line = DashedLine(plot.pt(0, 0.88), plot.pt(10, 0.88), color=RESPONDER, stroke_width=2.5, dash_length=0.14)
        peak_lbl = T("same peak height", 24, RESPONDER).move_to([3.3, -1.95, 0])

        new_left_head = fit_text("Single living cells", max_w=5.7, size=30, color=RESPONDER).move_to(tp.left_head)
        self.play(
            FadeOut(crowd), FadeOut(blot_lbl), FadeOut(blot_name), FadeOut(dial_note),
            FadeOut(tp.left_head),
            run_time=0.6,
        )
        self.play(
            FadeIn(new_left_head), FadeIn(peak_lbl),
            FadeIn(single_cells), FadeIn(cell_note),
            FadeIn(dose_track), FadeIn(dose_fill), FadeIn(dose_lab), FadeIn(pulse_count_lbl),
            Create(peak_line),
            run_time=2.0,
        )
        tp.left_head = new_left_head
        self.add(sc_curve, sc_dot, sc_cursor)

        self.at("fires separate pulses")
        self.play(t_sc.animate.set_value(3.5), run_time=4.4, rate_func=linear)

        self.at("Higher doses add")
        self.play(dose_val.animate.set_value(0.67), t_sc.animate.set_value(6.5), run_time=2.0, rate_func=linear)
        self.play(dose_val.animate.set_value(1.00), t_sc.animate.set_value(9.6), run_time=2.0, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ scene 03
class S03AverageMath(SpokenScene):
    def construct(self):
        tp = make_monitor("4 cells (out of step)", "How the blot averages them", RESPONDER, AVERAGE)
        tag = scope_tag("schematic units")

        row_ys = [1.45, 0.55, -0.35, -1.25]
        t_cur = ValueTracker(0.0)
        show_vals = ValueTracker(0.0)

        def cell_level(i, t):
            return 80.0 if int(np.clip(np.floor(t), 0, 3)) == i else 0.0

        rows = VGroup()
        for i, y in enumerate(row_ys):
            circle = Circle(radius=0.30, stroke_color=RESPONDER, stroke_width=2.5,
                            fill_color=RESPONDER, fill_opacity=0.16).move_to([-5.55, y, 0])
            name = T(f"Cell {i + 1}", 25, TEXT).move_to([-4.55, y, 0])
            bar_bg = RoundedRectangle(corner_radius=0.06, width=1.95, height=0.32,
                                      stroke_color=STRUCT, stroke_width=2, fill_opacity=0.14).move_to([-2.7, y, 0])

            def mk_fill(idx=i, yy=y, bg=bar_bg):
                v = cell_level(idx, t_cur.get_value()) if show_vals.get_value() > 0.5 else 0.0
                w = max(0.08, 1.87 * (v / 80.0))
                return RoundedRectangle(
                    corner_radius=0.05, width=w, height=0.24, stroke_width=0,
                    fill_color=RESPONDER, fill_opacity=0.85 if v > 1 else 0.16,
                ).align_to(bg, LEFT).shift(RIGHT * 0.04).set_y(yy)

            fill = always_redraw(mk_fill)
            circle.add_updater(lambda m, idx=i: m.set_fill(
                RESPONDER,
                opacity=0.88 if (show_vals.get_value() > 0.5 and cell_level(idx, t_cur.get_value()) > 1) else 0.16
            ))
            num = always_redraw(lambda idx=i, yy=y: M(
                f"{int(cell_level(idx, t_cur.get_value())) if show_vals.get_value() > 0.5 else 0:2d}",
                25, RESPONDER if (show_vals.get_value() > 0.5 and cell_level(idx, t_cur.get_value()) > 1) else TEXT,
            ).move_to([-1.15, yy, 0]))
            rows.add(VGroup(circle, name, bar_bg, fill, num))

        formula = M("average = sum ÷ cell count", size=26, color=AVERAGE).move_to([3.3, 1.92, 0])
        plot = Plot(
            box=(1.1, 5.9, -0.82, 1.22), xr=(0, 4), yr=(0, 100),
            xticks=[(0.5, "h1"), (1.5, "h2"), (2.5, "h3"), (3.5, "h4")],
            yticks=[(0, "0"), (20, "20"), (80, "80")],
            xlabel="hour", ylabel="p53", color=STRUCT, size=22, label_size=24,
        )

        spikes = VGroup(*[
            plot.curve(lambda x, k=i: spike_slot(x, k), color=RESPONDER, width=5)
            for i in range(4)
        ])

        cursor_line = always_redraw(lambda: DashedLine(
            plot.pt(np.clip(t_cur.get_value(), 0, 4), 0),
            plot.pt(np.clip(t_cur.get_value(), 0, 4), 95),
            color=RESTRAINT, stroke_width=3, dash_length=0.12,
        ))
        avg_live = plot.live_curve(lambda x: 20.0, t_cur, color=AVERAGE, width=5)

        def mk_arith():
            k = int(np.clip(np.floor(t_cur.get_value()), 0, 3))
            vals = ["80" if j == k else "0" for j in range(4)]
            return M(f"({' + '.join(vals)}) ÷ 4 = 20", 24, AVERAGE).move_to([3.3, -2.14, 0])

        arith = always_redraw(mk_arith)

        self.play(FadeIn(tp), FadeIn(rows), FadeIn(plot), FadeIn(tag), run_time=2.4)

        self.at("cells pulse out of step")
        for i in range(4):
            self.play(Create(spikes[i]), run_time=0.65)

        self.at("An average equals")
        self.play(FadeIn(formula, shift=DOWN * 0.1), run_time=2.4)
        peak_ref = DashedLine(plot.pt(0, 80), plot.pt(4, 80), color=RESPONDER, stroke_width=2.5, dash_length=0.14)
        self.play(Create(peak_ref), run_time=1.8)

        self.at("peak at 80")
        # Flash each cell bar sequentially 1->2->3->4 to illustrate "four cells each peak at 80, one after another"
        show_vals.set_value(1.0)
        for target_t in (0.5, 1.5, 2.5, 3.5):
            self.play(t_cur.animate.set_value(target_t), run_time=0.72, rate_func=linear)
        t_cur.set_value(0.0)

        self.at("At any hour")
        self.add(cursor_line, avg_live, arith)
        for target_t in (0.5, 1.5, 2.5, 3.5, 4.0):
            self.play(t_cur.animate.set_value(target_t), run_time=1.45, rate_func=linear)

        self.at("blend into a low")
        t_wave = ValueTracker(0.0)
        wave_live = plot.live_curve(blended_wave, t_wave, color=AVERAGE, width=6)
        avg_live.clear_updaters()
        cursor_line.clear_updaters()
        self.add(wave_live)
        self.play(
            FadeOut(cursor_line),
            FadeOut(avg_live),
            t_wave.animate.set_value(0.5),
            run_time=0.35, rate_func=linear,
        )
        self.play(t_wave.animate.set_value(4.0), run_time=2.45, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ shared s04/s05/s06 world
def build_predict_world(include_question=True):
    """Build the split pulsed-vs-steady p53 monitor shared by S04, S05Pause, and S06."""
    tp = make_monitor("Cell state", "Same peak, different shape", TEXT, RESPONDER, top=2.75, bottom=-2.90)
    tag = scope_tag("schematic")

    top_cell = make_cell((-4.75, 0.90, 0), radius_w=1.85, radius_h=1.42, nuc_r=0.40,
                         border_col=REPAIR, nuc_opacity=0.35, label="p53", label_size=24)
    dsb = VGroup(
        Line([-5.35, 1.78, 0], [-4.85, 1.78, 0], color=STRESS, stroke_width=4),
        Line([-4.65, 1.78, 0], [-4.15, 1.78, 0], color=STRESS, stroke_width=4),
        Line([-5.35, 1.93, 0], [-4.85, 1.93, 0], color=STRESS, stroke_width=4),
        Line([-4.65, 1.93, 0], [-4.15, 1.93, 0], color=STRESS, stroke_width=4),
    )
    top_lbl = T("pulsed cell", 25, REPAIR).move_to([-2.25, 0.90, 0])

    bot_cell = make_cell((-4.75, -1.32, 0), radius_w=1.85, radius_h=1.42, nuc_r=0.40,
                         border_col=RESTRAINT, nuc_opacity=0.35, label="p53", label_size=24)
    blocker = boxed_label("MDM2 blocker", RESTRAINT, size=24, pad=0.14).move_to([-2.25, -1.02, 0])
    bot_lbl = T("steady cell", 25, TEXT).move_to([-2.25, -1.68, 0])

    p_top = Plot(
        box=(1.1, 5.9, 0.68, 1.44), xr=(0, 10), yr=(0, 1.15),
        xticks=[], yticks=[(0, "0"), (0.88, "1×")],
        ylabel="", color=STRUCT, size=22, label_size=22,
    )
    p_bot = Plot(
        box=(1.1, 5.9, -1.04, -0.28), xr=(0, 10), yr=(0, 1.15),
        xticks=[2, 8], yticks=[(0, "0"), (0.88, "1×")],
        xlabel="", ylabel="", color=STRUCT, size=22, label_size=22,
    )
    lbl_top = T("pulsed p53", 24, RESPONDER).move_to([1.15, 1.74, 0], aligned_edge=LEFT)
    same_pk = T("same peak", 24, AVERAGE).move_to([5.95, 1.74, 0], aligned_edge=RIGHT)
    lbl_bot = T("steady p53", 22, RESPONDER).move_to([0.75, 0.18, 0], aligned_edge=LEFT)
    time_lbl = T("time", 22, STRUCT).move_to([5.95, -1.32, 0], aligned_edge=RIGHT)

    ref_top = DashedLine(p_top.pt(0, 0.88), p_top.pt(10, 0.88), color=GREY, stroke_width=2, dash_length=0.12)
    ref_bot = DashedLine(p_bot.pt(0, 0.88), p_bot.pt(10, 0.88), color=GREY, stroke_width=2, dash_length=0.12)

    pulse_c = p_top.curve(lambda x: pulse_train(x, [2.0, 5.0, 8.0], width=0.50, peak=0.88), color=RESPONDER, width=5)
    steady_c = p_bot.curve(lambda x: steady_plateau(x, t_on=0.6, peak=0.88), color=RESPONDER, width=5)

    fate = make_fate_bar((3.3, -2.18, 0), width=4.6, height=0.34,
                         left_text="Recover", right_text="Permanent arrest", frac=0.5, show_q=True)

    world = VGroup(tp, tag, top_cell, dsb, top_lbl, bot_cell, blocker, bot_lbl,
                   p_top, p_bot, lbl_top, lbl_bot, same_pk, time_lbl, ref_top, ref_bot,
                   pulse_c, steady_c, fate)
    if include_question:
        q = question_card("Same peak, different shape: will steady cells still recover?",
                          y=3.32, color=RESTRAINT, size=30, max_w=12.0).move_to([0, 3.32, 0])
        world.add(q)
        world.q = q
    world.tp = tp
    world.top_cell, world.bot_cell = top_cell, bot_cell
    world.p_top, world.p_bot = p_top, p_bot
    world.pulse_c, world.steady_c = pulse_c, steady_c
    world.fate = fate
    world.same_pk = same_pk
    world.top_lbl, world.bot_lbl, world.blocker = top_lbl, bot_lbl, blocker
    return world


# ------------------------------------------------------------------ scene 04
class S04PredictQ(SpokenScene):
    def construct(self):
        tp = make_monitor("Cell state", "Same peak, different shape", TEXT, RESPONDER, top=2.75, bottom=-2.90)
        tag = scope_tag("schematic")

        top_cell = make_cell((-4.75, 0.90, 0), radius_w=1.85, radius_h=1.42, nuc_r=0.40,
                             border_col=REPAIR, nuc_opacity=0.35, label="p53", label_size=24)
        dsb = VGroup(
            Line([-5.35, 1.78, 0], [-4.85, 1.78, 0], color=STRESS, stroke_width=4),
            Line([-4.65, 1.78, 0], [-4.15, 1.78, 0], color=STRESS, stroke_width=4),
            Line([-5.35, 1.93, 0], [-4.85, 1.93, 0], color=STRESS, stroke_width=4),
            Line([-4.65, 1.93, 0], [-4.15, 1.93, 0], color=STRESS, stroke_width=4),
        )
        top_lbl = T("pulsed cell", 25, REPAIR).move_to([-2.25, 0.90, 0])

        bot_cell = make_cell((-4.75, -1.32, 0), radius_w=1.85, radius_h=1.42, nuc_r=0.40,
                             border_col=RESTRAINT, nuc_opacity=0.14, label="p53", label_size=24)
        blocker = boxed_label("MDM2 blocker", RESTRAINT, size=24, pad=0.14).move_to([-2.25, -1.02, 0])
        bot_lbl = T("steady cell", 25, TEXT).move_to([-2.25, -1.68, 0])

        p_top = Plot(
            box=(1.1, 5.9, 0.68, 1.44), xr=(0, 10), yr=(0, 1.15),
            xticks=[], yticks=[(0, "0"), (0.88, "1×")],
            ylabel="", color=STRUCT, size=22, label_size=22,
        )
        p_bot = Plot(
            box=(1.1, 5.9, -1.04, -0.28), xr=(0, 10), yr=(0, 1.15),
            xticks=[2, 8], yticks=[(0, "0"), (0.88, "1×")],
            xlabel="", ylabel="", color=STRUCT, size=22, label_size=22,
        )
        lbl_top = T("pulsed p53", 24, RESPONDER).move_to([1.15, 1.74, 0], aligned_edge=LEFT)
        same_pk = T("same peak", 24, AVERAGE).move_to([5.95, 1.74, 0], aligned_edge=RIGHT)
        lbl_bot = T("steady p53", 22, RESPONDER).move_to([0.75, 0.18, 0], aligned_edge=LEFT)
        time_lbl = T("time", 22, STRUCT).move_to([5.95, -1.32, 0], aligned_edge=RIGHT)

        ref_top = DashedLine(p_top.pt(0, 0.88), p_top.pt(10, 0.88), color=GREY, stroke_width=2, dash_length=0.12)
        ref_bot = DashedLine(p_bot.pt(0, 0.88), p_bot.pt(10, 0.88), color=GREY, stroke_width=2, dash_length=0.12)

        t_p = ValueTracker(0.0)
        pulse_live = p_top.live_curve(lambda x: pulse_train(x, [2.0, 5.0, 8.0], width=0.50, peak=0.88), t_p, color=RESPONDER, width=5)

        t_s = ValueTracker(0.0)
        steady_live = p_bot.live_curve(lambda x: steady_plateau(x, t_on=0.6, peak=0.88), t_s, color=RESPONDER, width=5)
        steady_cursor = always_redraw(lambda: DashedLine(
            p_bot.pt(t_s.get_value(), 0), p_bot.pt(t_s.get_value(), 0.96),
            color=RESTRAINT, stroke_width=2, dash_length=0.08,
        ) if (0.15 < t_s.get_value() < 9.85) else VMobject())

        fate = make_fate_bar((3.3, -2.18, 0), width=4.6, height=0.34,
                             left_text="Recover", right_text="Permanent arrest", frac=0.5, show_q=True)

        self.play(FadeIn(tp), FadeIn(top_cell), FadeIn(dsb), FadeIn(top_lbl),
                  FadeIn(p_top), FadeIn(lbl_top), Create(ref_top), FadeIn(tag), run_time=1.3)
        self.add(pulse_live)
        self.play(t_p.animate.set_value(10.0), run_time=4.0, rate_func=linear)

        self.at("read that pulsing shape")
        self.play(FadeIn(bot_cell), FadeIn(p_bot), FadeIn(time_lbl), Create(ref_bot), FadeIn(same_pk), run_time=3.2)

        self.at("blocked MDM2")
        self.play(
            FadeIn(blocker, shift=LEFT * 0.25),
            FadeIn(bot_lbl),
            FadeIn(lbl_bot),
            run_time=0.8,
        )
        self.add(steady_live, steady_cursor)
        self.play(
            bot_cell.nuc.animate.set_fill(RESPONDER, opacity=0.35),
            t_s.animate.set_value(10.0),
            run_time=6.8, rate_func=linear,
        )

        self.at("same peak")
        self.play(
            Indicate(ref_top, color=RESTRAINT, scale_factor=1.0),
            Indicate(ref_bot, color=RESTRAINT, scale_factor=1.0),
            FadeIn(fate), run_time=2.6,
        )

        self.at("Will the steady cells")
        q = question_card("Same peak, different shape: will steady cells still recover?",
                          y=3.32, color=RESTRAINT, size=30, max_w=12.0).move_to([0, 3.32, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.8)
        self.finish()


# ------------------------------------------------------------------ scene 05 (silent pause)
class S05Pause(PredictPause):
    QUESTION = "Same peak, different shape: will steady cells still recover?"
    CARD = {"y": 3.32, "max_w": 12.0, "color": RESTRAINT, "size": 30}
    RING_AT = (4.1, -3.30, 0)
    SECONDS = 4.5

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT, **self.CARD).move_to([0, 3.32, 0])
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.36)
        self.add(ring)
        self.play(run)
        self.finish()

    def backdrop(self):
        return build_predict_world(include_question=False)


# ------------------------------------------------------------------ scene 06
class S06RevealFate(SpokenScene):
    def construct(self):
        w = build_predict_world(include_question=True)
        self.add(w)

        self.at("Mostly not")
        answer_no = T("No — shape steered fate", 30, RESTRAINT, weight=BOLD).move_to([0, 3.32, 0])
        t_dot = ValueTracker(0.0)
        p_cursor = always_redraw(lambda: DashedLine(
            w.p_top.pt(t_dot.get_value(), 0), w.p_top.pt(t_dot.get_value(), 0.96),
            color=REPAIR, stroke_width=2.5, dash_length=0.08,
        ) if (0.1 < t_dot.get_value() < 9.6) else VMobject())
        self.add(p_cursor)
        self.play(
            swap(w.q, answer_no, run_time=0.7),
            FadeOut(w.fate.q, run_time=0.5),
            run_time=0.7,
        )
        w.fate.remove(w.fate.q)
        self.play(
            w.fate.marker.animate.move_to([w.fate.bar_center[0] + 1.5, w.fate.marker.get_y(), 0]),
            t_dot.animate.set_value(9.7),
            run_time=6.1, rate_func=linear,
        )
        self.remove(p_cursor)

        self.at("pulsing cells tended")
        rec_badge = boxed_label("recover & divide", REPAIR, size=22, pad=0.10).move_to([5.95, 1.74, 0], aligned_edge=RIGHT)
        d1 = make_cell((-5.45, 0.90, 0), radius_w=1.05, radius_h=1.20, nuc_r=0.28,
                       border_col=REPAIR, nuc_opacity=0.38)
        d2 = make_cell((-4.25, 0.90, 0), radius_w=1.05, radius_h=1.20, nuc_r=0.28,
                       border_col=REPAIR, nuc_opacity=0.38)
        div_lbl = T("2 daughter cells", 24, REPAIR).move_to([-2.05, 0.90, 0])

        self.play(
            swap(w.same_pk, rec_badge, run_time=0.7),
            swap(w.top_lbl, div_lbl, run_time=0.7),
            run_time=0.7,
        )
        self.play(FadeOut(w.top_cell.lab), run_time=0.25)
        w.top_cell.remove(w.top_cell.lab)
        self.play(
            Transform(w.top_cell, VGroup(d1, d2)),
            run_time=2.5,
        )
        w.top_lbl = div_lbl

        self.at("Steady cells more")
        sen_badge = boxed_label("senescence (exit)", ARREST, size=22, pad=0.10).move_to([5.95, 0.18, 0], aligned_edge=RIGHT)
        lock_ring = RoundedRectangle(corner_radius=0.58, width=2.08, height=1.65,
                                     stroke_color=ARREST, stroke_width=6).move_to(w.bot_cell.get_center())
        sen_lbl = T("locked (exit)", 24, ARREST).move_to([-2.25, -1.68, 0])
        self.play(
            FadeIn(sen_badge),
            swap(w.bot_lbl, sen_lbl, run_time=0.7),
            run_time=0.7,
        )
        self.play(
            Create(lock_ring),
            run_time=5.1,
        )
        w.bot_lbl = sen_lbl

        self.at("Steady P53")
        xs = np.linspace(0, 10, 120)
        p_pts = [w.p_top.pt(0, 0)] + [w.p_top.pt(x, pulse_train(x, [2.0, 5.0, 8.0], width=0.50, peak=0.88)) for x in xs] + [w.p_top.pt(10, 0)]
        s_pts = [w.p_bot.pt(0, 0)] + [w.p_bot.pt(x, steady_plateau(x, t_on=0.6, peak=0.88)) for x in xs] + [w.p_bot.pt(10, 0)]
        p_area = Polygon(*p_pts, stroke_width=0, fill_color=REPAIR, fill_opacity=0.30)
        s_area = Polygon(*s_pts, stroke_width=0, fill_color=ARREST, fill_opacity=0.30)
        p_area.layout_ok = True
        s_area.layout_ok = True
        tot_note = T("more total p53", 24, ARREST).move_to([3.3, -2.18, 0])

        self.play(FadeOut(w.fate, run_time=0.4))
        self.play(FadeIn(p_area), FadeIn(s_area), FadeIn(tot_note), run_time=0.8)

        self.at("yet at equal totals")
        self.play(FadeOut(tot_note, run_time=0.4))
        eq_title = T("at equal total p53 -> senescence genes:", 22, TEXT).move_to([3.3, -1.78, 0])
        bar_p_bg = RoundedRectangle(corner_radius=0.06, width=1.45, height=0.24, stroke_color=REPAIR, stroke_width=2)
        bar_p = RoundedRectangle(corner_radius=0.05, width=0.42, height=0.18, stroke_width=0, fill_color=REPAIR, fill_opacity=0.85).align_to(bar_p_bg, LEFT).shift(RIGHT * 0.03)
        bar_s_bg = RoundedRectangle(corner_radius=0.06, width=1.45, height=0.24, stroke_color=ARREST, stroke_width=2)
        bar_s = RoundedRectangle(corner_radius=0.05, width=1.35, height=0.18, stroke_width=0, fill_color=ARREST, fill_opacity=0.85).align_to(bar_s_bg, LEFT).shift(RIGHT * 0.03)
        p_bar_g = VGroup(bar_p_bg, bar_p)
        s_bar_g = VGroup(bar_s_bg, bar_s)
        lbl_bp = T("pulsed", 22, REPAIR)
        lbl_bs = T("steady", 22, ARREST)
        bars_g = VGroup(lbl_bp, p_bar_g, lbl_bs, s_bar_g).arrange(RIGHT, buff=0.14).move_to([3.3, -2.30, 0])
        fit(bars_g, max_w=5.6)

        self.play(FadeIn(eq_title), FadeIn(bars_g), run_time=2.6)

        self.at("How a stress signal unfolds")
        cap = caption("How a stress signal unfolds over time helps decide cell fate.", size=28, color=RESTRAINT, y=-3.25)
        tl_sw = ValueTracker(0.0)
        sw_line_top = always_redraw(lambda: Line(
            w.p_top.pt(tl_sw.get_value(), 0), w.p_top.pt(tl_sw.get_value(), 0.96),
            color=RESTRAINT, stroke_width=3,
        ) if (0.1 < tl_sw.get_value() < 9.7) else VMobject())
        sw_line_bot = always_redraw(lambda: Line(
            w.p_bot.pt(tl_sw.get_value(), 0), w.p_bot.pt(tl_sw.get_value(), 0.96),
            color=RESTRAINT, stroke_width=3,
        ) if (0.1 < tl_sw.get_value() < 9.7) else VMobject())
        self.play(FadeIn(cap, shift=UP * 0.12), run_time=1.0)
        self.add(sw_line_top, sw_line_bot)
        self.play(tl_sw.animate.set_value(9.6), run_time=4.2, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ shared s07/s08 ER world
def build_er_world():
    """Build the ER membrane (segmented around sensors) + IRE1/PERK/ATF6 + stress/fate timeline."""
    tp = make_monitor("Endoplasmic reticulum (ER)", "ER stress & fate", TEXT, RESPONDER)
    tag = scope_tag("schematic")

    mem_segs = VGroup(
        Rectangle(width=0.35, height=0.22, stroke_color=STRUCT, stroke_width=2, fill_color=STRUCT, fill_opacity=0.45).move_to([-5.97, 0.05, 0]),
        Rectangle(width=0.24, height=0.22, stroke_color=STRUCT, stroke_width=2, fill_color=STRUCT, fill_opacity=0.45).move_to([-5.32, 0.05, 0]),
        Rectangle(width=0.24, height=0.22, stroke_color=STRUCT, stroke_width=2, fill_color=STRUCT, fill_opacity=0.45).move_to([-3.975, 0.05, 0]),
        Rectangle(width=0.24, height=0.22, stroke_color=STRUCT, stroke_width=2, fill_color=STRUCT, fill_opacity=0.45).move_to([-2.625, 0.05, 0]),
        Rectangle(width=0.85, height=0.22, stroke_color=STRUCT, stroke_width=2, fill_color=STRUCT, fill_opacity=0.45).move_to([-0.97, 0.05, 0]),
    )
    cyto_lbl = T("cytoplasm", 24, TEXT).move_to([-1.35, 1.92, 0])
    lumen_lbl = T("ER lumen", 24, TEXT).move_to([-5.25, -2.18, 0])

    sx = [-4.65, -3.3, -1.95]
    names = ["IRE1", "PERK", "ATF6"]
    sensors = VGroup()
    bips = VGroup()
    for x, nm in zip(sx, names):
        blk = boxed_label(nm, RESPONDER, size=24, box=(1.05, 0.72), pad=0.10).move_to([x, 0.05, 0])
        blk.box.set_fill(BG, opacity=0.95)
        sensors.add(blk)
        bip = boxed_label("BiP", RESTRAINT, size=22, box=(0.82, 0.44), pad=0.06).move_to([x, -0.62, 0])
        bips.add(bip)

    entry_arr = Arrow([-5.62, 0.72, 0], [-5.62, -0.58, 0], color=TEXT, stroke_width=4, buff=0.04)

    rng = np.random.default_rng(RNG_SEED)
    chains = VGroup()
    for cx, cy in [(-4.75, -1.65), (-3.85, -1.78), (-2.95, -1.62), (-2.05, -1.78), (-1.35, -1.62)]:
        ts = np.linspace(0, 2.4 * PI, 36)
        pts = [np.array([cx + 0.34 * np.cos(t) + 0.06 * np.sin(3 * t),
                         cy + 0.14 * np.sin(2 * t + rng.uniform(-0.25, 0.25)), 0.0]) for t in ts]
        sq = VMobject(stroke_color=STRESS, stroke_width=3.5, fill_opacity=0)
        sq.set_points_as_corners(pts)
        chains.add(sq)

    dur_title = T("ER stress duration", 26, STRESS).move_to([3.3, 1.55, 0])
    dur_bg = RoundedRectangle(corner_radius=0.1, width=4.8, height=0.42,
                              stroke_color=STRESS, stroke_width=2.5, fill_opacity=0.12).move_to([3.3, 0.95, 0])
    dur_ticks = VGroup(
        T("brief", 24, REPAIR).move_to([1.3, 0.45, 0]),
        T("prolonged", 24, ARREST).move_to([5.0, 0.45, 0]),
    )
    fate = make_fate_bar((3.3, -0.62, 0), width=4.8, height=0.42,
                         left_text="Repair", right_text="Cell death", frac=0.15)
    repair_note = boxed_label("lower load + add chaperones", REPAIR, size=24, pad=0.14).move_to([3.3, -2.02, 0])

    return {
        "tp": tp, "tag": tag, "mem": mem_segs, "cyto_lbl": cyto_lbl, "lumen_lbl": lumen_lbl,
        "sensors": sensors, "bips": bips, "entry_arr": entry_arr, "chains": chains,
        "dur_title": dur_title, "dur_bg": dur_bg, "dur_ticks": dur_ticks,
        "fate": fate, "repair_note": repair_note, "sx": sx,
    }


# ------------------------------------------------------------------ scene 07
class S07UprBridge(SpokenScene):
    def construct(self):
        er = build_er_world()
        folded_pos = [(-4.4, -1.75, 0), (-3.1, -1.75, 0), (-1.8, -1.75, 0)]
        folded = VGroup(*[
            Ellipse(width=0.62, height=0.34, stroke_color=REPAIR, stroke_width=3.5,
                    fill_color=REPAIR, fill_opacity=0.35).move_to(p)
            for p in folded_pos
        ])
        for s in er["sensors"]:
            s.box.set_stroke(RESPONDER, width=2, opacity=0.45)

        stress_len = ValueTracker(0.22)
        dur_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08, width=max(0.22, 4.72 * stress_len.get_value()), height=0.34,
            stroke_width=0, fill_color=STRESS, fill_opacity=0.84,
        ).align_to(er["dur_bg"], LEFT).shift(RIGHT * 0.04).set_y(er["dur_bg"].get_y()))

        self.play(
            FadeIn(er["tp"]), FadeIn(er["mem"]), FadeIn(er["cyto_lbl"]), FadeIn(er["lumen_lbl"]),
            FadeIn(er["sensors"]), FadeIn(er["bips"]), FadeIn(er["tag"]),
            run_time=1.0,
        )

        # Secreted chains travel from pore across ER lumen and fold with BiP chaperone helpers
        helper_bip = boxed_label("BiP", RESTRAINT, size=22, box=(0.82, 0.44), pad=0.06).move_to([-5.15, -1.26, 0])
        self.play(FadeIn(er["entry_arr"]), FadeIn(helper_bip), run_time=1.0)
        ribbons = VGroup()
        for i, pos in enumerate(folded_pos):
            rib = Line([-5.62, -1.55, 0], [-5.05, -1.72, 0], color=AVERAGE, stroke_width=4.5)
            ribbons.add(rib)
            self.play(
                rib.animate.move_to(pos),
                helper_bip.animate.move_to([pos[0], -1.26, 0]),
                run_time=1.35,
            )
            self.play(Transform(rib, folded[i]), run_time=0.9)

        self.at("When unfolded chains")
        self.play(
            FadeOut(ribbons), FadeOut(helper_bip),
            FadeIn(er["chains"]),
            FadeIn(er["dur_title"]), FadeIn(er["dur_bg"]), FadeIn(dur_fill), FadeIn(er["dur_ticks"]),
            run_time=2.4,
        )

        self.at("three membrane sensors")
        bip_targets = [(-4.45, -1.15, 0), (-3.10, -1.15, 0), (-1.75, -1.15, 0)]
        self.play(
            *[b.animate.move_to(p) for b, p in zip(er["bips"], bip_targets)],
            *[s.box.animate.set_stroke(RESPONDER, width=4.5, opacity=1.0) for s in er["sensors"]],
            run_time=7.0,
        )

        self.at("buy time for repair")
        self.play(FadeIn(er["fate"]), FadeIn(er["repair_note"]), run_time=1.6)

        self.at("slowing new protein entry")
        slow_line = Line([-3.3, 0.55, 0], [-5.35, 0.55, 0], color=REPAIR, stroke_width=3.5)
        t_bar = Line([-5.35, 0.35, 0], [-5.35, 0.75, 0], color=REPAIR, stroke_width=4)
        self.play(
            Create(slow_line), Create(t_bar),
            er["entry_arr"].animate.set_stroke(width=1.5, opacity=0.45),
            run_time=1.6,
        )

        self.at("ordering more chaperones")
        extra_bips = VGroup(
            boxed_label("BiP", RESTRAINT, size=22, box=(0.82, 0.44), pad=0.06).move_to([-5.05, -0.62, 0]),
            boxed_label("BiP", RESTRAINT, size=22, box=(0.82, 0.44), pad=0.06).move_to([-2.40, -0.62, 0]),
        )
        self.play(
            FadeIn(extra_bips, shift=DOWN * 0.2),
            er["chains"][0].animate.set_stroke(opacity=0.35),
            er["chains"][2].animate.set_stroke(opacity=0.35),
            run_time=0.8,
        )
        self.finish()


# ------------------------------------------------------------------ scene 08
class S08UprDeathScope(SpokenScene):
    def construct(self):
        er = build_er_world()
        bip_targets = [(-4.45, -1.15, 0), (-3.10, -1.15, 0), (-1.75, -1.15, 0)]
        for b, p in zip(er["bips"], bip_targets):
            b.move_to(p)
        for s in er["sensors"]:
            s.box.set_stroke(RESPONDER, width=4.0, opacity=1.0)
        er["entry_arr"].set_stroke(width=1.5, opacity=0.45)

        stress_len = ValueTracker(0.22)
        dur_fill = always_redraw(lambda: RoundedRectangle(
            corner_radius=0.08, width=max(0.22, 4.72 * stress_len.get_value()), height=0.34,
            stroke_width=0, fill_color=STRESS, fill_opacity=0.84,
        ).align_to(er["dur_bg"], LEFT).shift(RIGHT * 0.04).set_y(er["dur_bg"].get_y()))

        fate_frac = ValueTracker(0.15)
        fate_marker = always_redraw(lambda: Triangle(
            color=TEXT, fill_color=TEXT, fill_opacity=1.0, stroke_width=2
        ).scale(0.15).rotate(PI).move_to([
            er["fate"].bar_center[0] + (fate_frac.get_value() - 0.5) * (er["fate"].bar_width - 0.35),
            er["fate"].bar_center[1] + er["fate"].bar_height / 2 + 0.16, 0,
        ]))
        er["fate"].remove(er["fate"].marker)
        er["fate"].add(fate_marker)

        self.add(
            er["tp"], er["tag"], er["mem"], er["cyto_lbl"], er["lumen_lbl"],
            er["sensors"], er["bips"], er["entry_arr"], er["chains"],
            er["dur_title"], er["dur_bg"], dur_fill, er["dur_ticks"],
            er["fate"], er["repair_note"],
        )

        extra_chains = VGroup(*[
            er["chains"][i].copy().shift(DOWN * 0.14 + RIGHT * 0.14) for i in range(4)
        ])

        self.at("backlog drags on")
        self.play(
            FadeIn(extra_chains),
            stress_len.animate.set_value(0.88),
            run_time=2.6, rate_func=linear,
        )

        self.at("shift their message")
        death_note = boxed_label("shift toward cell death", ARREST, size=24, pad=0.14).move_to([3.3, -2.02, 0])
        self.play(swap(er["repair_note"], death_note, run_time=0.7), run_time=0.7)
        self.play(
            fate_frac.animate.set_value(0.84),
            er["sensors"][0].box.animate.set_stroke(ARREST, width=4.5),
            er["sensors"][1].box.animate.set_stroke(ARREST, width=4.5),
            run_time=4.5,
        )

        self.at("called CHOP")
        chop_chip = boxed_label("CHOP", ARREST, size=26, pad=0.14).move_to([-3.3, 1.55, 0])
        perk_arrow = Arrow([-3.3, 0.44, 0], [-3.3, 1.15, 0], color=ARREST, stroke_width=4.5, buff=0.04)
        self.play(GrowArrow(perk_arrow), FadeIn(chop_chip), run_time=1.8)
        self.play(Indicate(chop_chip, color=ARREST), run_time=1.0)

        self.at("stress kinase JNK")
        jnk_chip = boxed_label("JNK", ARREST, size=26, pad=0.14).move_to([-4.65, 1.55, 0])
        ire_arrow = Arrow([-4.65, 0.44, 0], [-4.65, 1.15, 0], color=ARREST, stroke_width=4.5, buff=0.04)
        self.play(GrowArrow(ire_arrow), FadeIn(jnk_chip), run_time=1.8)
        self.play(Indicate(jnk_chip, color=ARREST), run_time=1.0)

        self.at("Stress strength and cell state")
        overlap_zone = RoundedRectangle(
            corner_radius=0.08, width=1.65, height=0.46,
            stroke_color=RESTRAINT, stroke_width=3, fill_color=RESTRAINT, fill_opacity=0.25,
        ).move_to([3.3, -0.62, 0])
        overlap_zone.layout_ok = True
        overlap_lbl = T("strength & cell state matter", 24, RESTRAINT).move_to([3.3, 0.04, 0])
        overlap_sub = T("repair & death overlap", 24, TEXT).move_to([3.3, -1.58, 0])

        self.play(FadeOut(death_note, run_time=0.4))
        self.play(
            FadeIn(overlap_zone), FadeIn(overlap_lbl), FadeIn(overlap_sub),
            fate_frac.animate.set_value(0.40),
            run_time=2.4,
        )
        self.play(fate_frac.animate.set_value(0.68), run_time=2.2, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ scene 09
class S09Closing(SpokenScene):
    def construct(self):
        tp = make_monitor("Brief or pulsed signal", "Sustained signal", REPAIR, ARREST, top=3.1, bottom=-2.3)
        tag = scope_tag("schematic")

        p_left = Plot(
            box=(-5.25, -0.85, -0.35, 1.45), xr=(0, 10), yr=(0, 1.15),
            xticks=[2, 5, 8], yticks=[(0, "0"), (0.88, "peak")],
            xlabel="time", ylabel="signal", color=STRUCT, size=22, label_size=24,
        )
        p_right = Plot(
            box=(1.35, 5.75, -0.35, 1.45), xr=(0, 10), yr=(0, 1.15),
            xticks=[2, 5, 8], yticks=[(0, "0"), (0.88, "peak")],
            xlabel="time", ylabel="signal", color=STRUCT, size=22, label_size=24,
        )
        p_left.ylabel.shift(UP * 0.24)
        p_right.ylabel.shift(UP * 0.24)

        t_l = ValueTracker(0.0)
        t_r = ValueTracker(0.0)
        l_fn = lambda x: pulse_train(x, [2.0, 5.0, 8.0], width=0.50, peak=0.88)
        r_fn = lambda x: steady_plateau(x, t_on=0.6, peak=0.88)

        l_live = p_left.live_curve(l_fn, t_l, color=REPAIR, width=5)
        r_live = p_right.live_curve(r_fn, t_r, color=ARREST, width=5)

        rec_chip = boxed_label("Repair & recover", REPAIR, size=26, pad=0.14).move_to([-3.3, -1.78, 0])
        arr_chip = boxed_label("Permanent arrest or death", ARREST, size=24, pad=0.14).move_to([3.3, -1.78, 0])

        self.play(FadeIn(tp), FadeIn(p_left), FadeIn(p_right), FadeIn(tag), run_time=1.3)
        self.add(l_live, r_live)

        self.at("brief or pulse")
        self.play(t_l.animate.set_value(10.0), run_time=1.2, rate_func=linear)
        self.at("favor repair")
        self.play(FadeIn(rec_chip), run_time=0.9)

        self.at("sustained ones")
        self.play(t_r.animate.set_value(10.0), FadeIn(arr_chip), run_time=1.6, rate_func=linear)

        self.at("One snapshot of protein")
        snap_x = 2.0
        snap_l = DashedLine(p_left.pt(snap_x, 0), p_left.pt(snap_x, 1.1), color=AVERAGE, stroke_width=3)
        snap_r = DashedLine(p_right.pt(snap_x, 0), p_right.pt(snap_x, 1.1), color=AVERAGE, stroke_width=3)
        dot_l = Dot(p_left.pt(snap_x, l_fn(snap_x)), radius=0.10, color=AVERAGE, stroke_color=REPAIR, stroke_width=3)
        dot_r = Dot(p_right.pt(snap_x, r_fn(snap_x)), radius=0.10, color=AVERAGE, stroke_color=ARREST, stroke_width=3)
        snap_lbl_l = T("snapshot = same", 22, AVERAGE).move_to([-2.3, 1.72, 0])
        snap_lbl_r = T("snapshot = same", 22, AVERAGE).move_to([4.3, 1.72, 0])
        snap_grp = VGroup(snap_l, snap_r, dot_l, dot_r, snap_lbl_l, snap_lbl_r)
        self.play(FadeIn(snap_grp), run_time=3.6)

        self.at("Reading the full timeline")
        self.play(FadeOut(snap_grp, run_time=0.45))
        tl_l = BraceBetweenPoints(p_left.pt(0, 1.06), p_left.pt(10, 1.06), direction=UP, color=RESTRAINT)
        tl_r = BraceBetweenPoints(p_right.pt(0, 1.06), p_right.pt(10, 1.06), direction=UP, color=RESTRAINT)
        tl_txt_l = T("full timeline", 24, RESTRAINT).move_to([-3.05, 1.98, 0])
        tl_txt_r = T("full timeline", 24, RESTRAINT).move_to([3.55, 1.98, 0])
        cap = caption("Read the full timeline: recovery vs. irreversible fate.", size=28, color=TEXT, y=-3.05)

        t_sw = ValueTracker(0.0)
        sw_l = always_redraw(lambda: Line(
            p_left.pt(t_sw.get_value(), 0), p_left.pt(t_sw.get_value(), 1.04),
            color=RESTRAINT, stroke_width=3,
        ) if (0.1 < t_sw.get_value() < 9.6) else VMobject())
        sw_r = always_redraw(lambda: Line(
            p_right.pt(t_sw.get_value(), 0), p_right.pt(t_sw.get_value(), 1.04),
            color=RESTRAINT, stroke_width=3,
        ) if (0.1 < t_sw.get_value() < 9.6) else VMobject())

        self.play(
            GrowFromCenter(tl_l), GrowFromCenter(tl_r),
            FadeIn(tl_txt_l), FadeIn(tl_txt_r),
            FadeIn(cap, shift=UP * 0.1),
            run_time=1.4,
        )
        self.add(sw_l, sw_r)
        self.play(t_sw.animate.set_value(9.5), run_time=3.8, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ scene 10
class S10End(EndCard):
    LINE = "How a stress signal unfolds over time helps decide cell fate."
