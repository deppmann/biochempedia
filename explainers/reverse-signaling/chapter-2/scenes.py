"""
Animation for "Which Direction Did the Work?" (Reverse Signaling, Chapter 2).

COLOUR MAP (one colour per concept, carried across the whole film):
    RECEPTOR_COL = "#2DD4BF"  # Teal   : receptor cell, EphB2 / TNFR1, forward signal
    LIGAND_COL   = "#F59E0B"  # Amber  : ligand cell, ephrin-B / membrane TNF, axon, reverse signal
    KINASE_COL   = "#FB7185"  # Coral  : intracellular kinase domain on the receptor
    INERT_COL    = "#64748B"  # Slate  : inert bacterial marker, Fc antibody handle, protease, KO stamp
    GRIP_COL     = TEXT       # White  : physical cell-to-cell grip / binding clasp
    OFF_COL      = "#F87171"  # Red    : disabled / cut / knockout state

WORLD CARRIED ACROSS THE FILM:
    Two cells clasped across a narrow extracellular cleft: the teal receptor cell above
    (with an outer cup tip and an intracellular coral kinase) grips the amber ligand cell
    below (with an outer ball tip and an intracellular tail). Across the film, we zoom out
    to growing axons crossing floor cells, then return to the cleft to test soluble Receptor-Fc
    and protease cleavage of membrane TNF.

WHAT CHANGES ON SCREEN IN EACH SPOKEN SCENE (and what computes it):
    s01_link_and_hook : Reverse signal wave travels continuously into ligand tail; knockout
                        dissolves the ligand, a computed branching organ fragments, and '?' alternates.
    s02_ko_trap       : Ligand deletion drives Forward, Reverse, and Grip ValueTrackers to 0 as
                        membranes drift apart; receptor deletion drops all three bars together.
    s03_rule_idea     : Dashed cut trims only the receptor's inner kinase; Forward drops to 0 while
                        Grip stays at 1 and the amber reverse wave flows continuously inward.
    s04_ephb2_setup   : Computed axon paths grow across floor cells: straight across wild-type/outer-tip
                        receptors, veering downward along a bounded power-law curve when EphB2 is absent.
    s05_predict_prompt: Kinase block swaps for inert slate in the bottom lane while computed axons
                        glide straight across the outer tips; predict question card appears.
    s07_predict_reveal: Zoom into the kinase-less floor/axon contact; amber reverse signal waves stream
                        continuously into the axon as ephrins dock onto teal outer tips ('Acts as ligand').
    s08_receptor_fc   : Upper receptor cell slides away upward; Y-shaped Receptor-Fc bodies assemble,
                        dock onto lower membrane ligands, and drive continuous amber reverse waves.
    s09_tnf_cleavage  : TNFR1-Fc docks onto uncut membrane TNF -> computed axon tip branches sprout;
                        protease clips TNF loose, breaking inward link while released TNF docks afar.
    s10_close         : Side-by-side comparison updates Full KO bars (all 0) vs Targeted cut (Grip=1,
                        Forward=0, Reverse=1 with live continuous inward signal wave).
"""
import numpy as np
from bp_parts import *

# ---- Film-specific colour map ----
RECEPTOR_COL = "#2DD4BF"
LIGAND_COL = "#F59E0B"
KINASE_COL = "#FB7185"
INERT_COL = "#64748B"
GRIP_COL = TEXT
OFF_COL = "#F87171"


# ==============================================================================
# Shared builders for the carried world & live indicators
# ==============================================================================

def _membrane_slab(center_y, width, thickness, color, edge_is_bottom=True):
    """A clean cell compartment slab with a bright plasma membrane edge facing the cleft."""
    fill = Rectangle(
        width=width, height=thickness,
        stroke_width=0, fill_color=color, fill_opacity=0.14,
    ).move_to([0, center_y, 0])
    edge_y = center_y - thickness / 2 if edge_is_bottom else center_y + thickness / 2
    membrane = Line([-width / 2, edge_y, 0], [width / 2, edge_y, 0], color=color, stroke_width=5)
    return VGroup(fill, membrane), edge_y


def _receptor_protein(cleft_y=0.0, x=0.0, show_kinase=True, inert_kinase=False):
    """Upper teal receptor: cup outer tip at cleft_y, stem through membrane, inner kinase/inert block."""
    cup = Arc(
        radius=0.28, start_angle=0, angle=PI,
        arc_center=[x, cleft_y + 0.14, 0], color=RECEPTOR_COL, stroke_width=7,
    )
    stem = Line([x, cleft_y + 0.42, 0], [x, cleft_y + 1.05, 0], color=RECEPTOR_COL, stroke_width=7)
    outer_grp = VGroup(cup, stem)

    inner = VGroup()
    if show_kinase:
        col = INERT_COL if inert_kinase else KINASE_COL
        block = RoundedRectangle(
            corner_radius=0.1, width=0.58, height=0.40,
            stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.85,
        ).move_to([x, cleft_y + 1.25, 0])
        inner.add(block)
    return outer_grp, inner


def _ligand_protein(cleft_y=0.0, x=0.0, show_tail=True):
    """Lower amber ligand: ball outer tip docking inside the cup, stem through membrane, inner tail."""
    tip = Dot([x, cleft_y + 0.06, 0], radius=0.18, color=LIGAND_COL, stroke_color=TEXT, stroke_width=2)
    stem = Line([x, cleft_y - 0.12, 0], [x, cleft_y - 0.85, 0], color=LIGAND_COL, stroke_width=7)
    outer_grp = VGroup(tip, stem)

    tail = VGroup()
    if show_tail:
        tail_seg = Line([x, cleft_y - 0.85, 0], [x, cleft_y - 1.38, 0], color=LIGAND_COL, stroke_width=6)
        tail_end = RoundedRectangle(
            corner_radius=0.08, width=0.46, height=0.28,
            stroke_color=LIGAND_COL, stroke_width=2.5, fill_color=LIGAND_COL, fill_opacity=0.55,
        ).move_to([x, cleft_y - 1.50, 0])
        tail.add(tail_seg, tail_end)
    return outer_grp, tail


def _signal_wave(x, y_start, y_end, color, speed=1.35, n_beads=4, radius=0.10, width=0.34, wave_w=1.35):
    """Continuous dt-driven intracellular signal wave (arrow + traveling beads + downstream wave arc)."""
    arrow = Arrow(
        [x, y_start, 0], [x, y_end, 0],
        buff=0, color=color, stroke_width=5.5, max_tip_length_to_length_ratio=0.28,
    )
    phase = ValueTracker(0.0)
    sign = 1.0 if y_end >= y_start else -1.0

    def _tick(mob, dt):
        phase.increment_value(dt * speed)

    def _mk():
        p = phase.get_value()
        grp = VGroup()
        for k in range(n_beads):
            u = (p + k / n_beads) % 1.0
            cy = y_start + u * (y_end - y_start)
            fade = float(np.sin(u * PI))
            bar = RoundedRectangle(
                corner_radius=0.04, width=width, height=0.12,
                stroke_width=0, fill_color=TEXT, fill_opacity=0.25 + 0.72 * fade,
            ).move_to([x, cy, 0])
            dot = Dot([x, cy, 0], radius=radius * (0.65 + 0.45 * fade), color=color, stroke_color=TEXT, stroke_width=2)
            grp.add(bar, dot)
        # Propagating intracellular wave front moving from near membrane deeper into the cell
        for w_off in (0.0, 0.5):
            wu = (p * 0.75 + w_off) % 1.0
            wy = y_start + (0.20 + 0.80 * wu) * (y_end - y_start)
            wfade = float(np.sin(wu * PI))
            span = wave_w * (0.55 + 0.45 * wu)
            arc_line = Line(
                [x - span / 2, wy - sign * 0.04, 0],
                [x + span / 2, wy - sign * 0.04, 0],
                color=color, stroke_width=5.0,
            ).set_opacity(0.75 * wfade)
            grp.add(arc_line)
        return grp

    beads = always_redraw(_mk)
    g = VGroup(arrow, beads)
    g.add_updater(_tick)
    return g


def build_cleft_world(x_center=-2.1, width=5.6, cleft_y=0.0, inert_kinase=False):
    """Build the carried two-cell cleft world at x_center."""
    upper_slab, _ = _membrane_slab(cleft_y + 1.45, width, 1.50, RECEPTOR_COL, edge_is_bottom=True)
    lower_slab, _ = _membrane_slab(cleft_y - 1.45, width, 1.50, LIGAND_COL, edge_is_bottom=False)
    upper_slab.shift(RIGHT * x_center)
    lower_slab.shift(RIGHT * x_center)

    rec_outer, rec_inner = _receptor_protein(cleft_y, x=x_center, show_kinase=True, inert_kinase=inert_kinase)
    lig_outer, lig_tail = _ligand_protein(cleft_y, x=x_center, show_tail=True)

    rec_lab = T("Receptor cell", 28, RECEPTOR_COL).move_to([x_center, cleft_y + 2.55, 0])
    lig_lab = T("Ligand cell", 28, LIGAND_COL).move_to([x_center, cleft_y - 2.55, 0])

    return {
        "upper_slab": upper_slab,
        "lower_slab": lower_slab,
        "rec_outer": rec_outer,
        "rec_inner": rec_inner,
        "lig_outer": lig_outer,
        "lig_tail": lig_tail,
        "rec_lab": rec_lab,
        "lig_lab": lig_lab,
        "x": x_center,
        "cleft_y": cleft_y,
    }


def build_status_bars(trackers, top_left=(1.35, 1.45), bar_w=2.1, row_h=0.95):
    """Three live status bars ('Forward', 'Reverse', 'Grip') driven by ValueTrackers (0..1)."""
    specs = [
        ("Forward", RECEPTOR_COL, trackers["fwd"]),
        ("Reverse", LIGAND_COL, trackers["rev"]),
        ("Grip", GRIP_COL, trackers["grip"]),
    ]
    rows = VGroup()
    x0, y0 = top_left
    for idx, (name, col, tr) in enumerate(specs):
        y = y0 - idx * row_h
        lbl = T(name, 28, col).move_to([x0, y, 0], aligned_edge=LEFT)
        bx = x0 + 1.55
        track = RoundedRectangle(
            corner_radius=0.08, width=bar_w, height=0.34,
            stroke_color=INERT_COL, stroke_width=2.5, fill_color=BG, fill_opacity=0.85,
        ).move_to([bx + bar_w / 2, y, 0])

        def _fill_mk(t=tr, c=col, left_x=bx, cy=y, bw=bar_w):
            v = float(np.clip(t.get_value(), 0.0, 1.0))
            w = max(0.02, v * (bw - 0.06))
            r = RoundedRectangle(
                corner_radius=0.06, width=w, height=0.26,
                stroke_width=0, fill_color=c if v > 0.1 else OFF_COL,
                fill_opacity=0.88 if v > 0.1 else 0.15,
            )
            r.move_to([left_x + 0.03 + w / 2, cy, 0])
            return r

        def _stat_mk(t=tr, c=col, rx=bx + bar_w + 0.25, cy=y):
            v = t.get_value()
            txt = "ON" if v >= 0.5 else "OFF"
            scol = c if v >= 0.5 else OFF_COL
            return M(txt, 28, scol).move_to([rx, cy, 0], aligned_edge=LEFT)

        rows.add(VGroup(lbl, track, always_redraw(_fill_mk), always_redraw(_stat_mk)))
    return rows


def _branching_organ(origin, progress_tracker, scatter_tracker):
    """Computed recursive tree organ (schematic) that grows with progress and fragments with scatter."""
    rng = np.random.default_rng(7)
    segments = []

    def _add_seg(p0, angle, length, depth):
        p1 = p0 + length * np.array([np.cos(angle), np.sin(angle), 0.0])
        jitter = rng.uniform(-0.35, 0.35, size=2)
        drift = np.array([jitter[0], jitter[1] - 0.25, 0.0])
        segments.append((p0, p1, depth, drift))
        if depth > 0:
            _add_seg(p1, angle + 0.42, length * 0.68, depth - 1)
            _add_seg(p1, angle - 0.42, length * 0.68, depth - 1)

    _add_seg(np.array(origin, dtype=float), PI / 2, 0.95, 2)

    def _mk():
        prog = float(np.clip(progress_tracker.get_value(), 0.0, 1.0))
        scat = float(np.clip(scatter_tracker.get_value(), 0.0, 1.0))
        grp = VGroup()
        for p0, p1, depth, drift in segments:
            thresh = (2 - depth) * 0.28
            local = float(np.clip((prog - thresh) / 0.35, 0.0, 1.0))
            if local <= 0.02:
                continue
            q0 = p0 + scat * drift
            q1 = q0 + local * (p1 - p0) * (1.0 - 0.35 * scat)
            col = interpolate_color(ManimColor(TEXT), ManimColor(OFF_COL), scat)
            ln = Line(q0, q1, color=col, stroke_width=6 - (2 - depth) * 1.2)
            ln.set_opacity(1.0 - 0.45 * scat)
            grp.add(ln)
        return grp

    return always_redraw(_mk)


def _computed_axon_tract(x0, x1, y_axon, progress_tracker, veer_tracker, num_fibers=3, veer_start=-1.4):
    """Computed axon fibers growing left->right across floor cells, veering down inside the lane when EphB2 is lost."""
    offsets = np.linspace(-0.20, 0.20, num_fibers)
    span = max(0.1, x1 - veer_start)

    def _mk():
        p = float(np.clip(progress_tracker.get_value(), 0.02, 1.0))
        veer = float(np.clip(veer_tracker.get_value(), 0.0, 1.0))
        x_end = x0 + p * (x1 - x0)
        grp = VGroup()
        for off in offsets:
            xs = np.linspace(x0, x_end, 44)
            pts = []
            for xv in xs:
                u = max(0.0, (xv - veer_start) / span)
                dy = -veer * 1.12 * (u ** 1.4)
                pts.append([xv, y_axon + off + dy, 0.0])
            curve = VMobject(stroke_color=LIGAND_COL, stroke_width=5)
            curve.set_points_as_corners(pts)
            grp.add(curve)
            grp.add(Dot(pts[-1], radius=0.075, color=LIGAND_COL))
        return grp

    return always_redraw(_mk)


def _floor_cells_row(xs, y_floor, has_outer=True, kinase_mode="coral"):
    """Row of teal floor cells with EphB2 receptors (kinase_mode: 'coral' | 'inert' | 'none')."""
    cells = VGroup()
    outer_tips = VGroup()
    inner_blocks = VGroup()
    for cx in xs:
        cell = RoundedRectangle(
            corner_radius=0.14, width=1.45, height=0.66,
            stroke_color=RECEPTOR_COL, stroke_width=2.5,
            fill_color=RECEPTOR_COL, fill_opacity=0.16,
        ).move_to([cx, y_floor, 0])
        cells.add(cell)
        if has_outer:
            stem = Line([cx, y_floor + 0.12, 0], [cx, y_floor + 0.56, 0], color=RECEPTOR_COL, stroke_width=5)
            cup = Arc(
                radius=0.16, start_angle=PI, angle=PI,
                arc_center=[cx, y_floor + 0.70, 0], color=RECEPTOR_COL, stroke_width=5,
            )
            outer_tips.add(VGroup(stem, cup))
        if kinase_mode != "none":
            col = KINASE_COL if kinase_mode == "coral" else INERT_COL
            blk = RoundedRectangle(
                corner_radius=0.07, width=0.46, height=0.26,
                stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.88,
            ).move_to([cx, y_floor - 0.04, 0])
            inner_blocks.add(blk)
    return cells, outer_tips, inner_blocks


def _soluble_receptor_fc(center, scale=1.0):
    """Y-shaped Receptor-Fc: slate antibody Fc stem + two teal receptor outer-tip arms."""
    cx, cy = center[0], center[1]
    stem = Line([cx, cy + 0.45 * scale, 0], [cx, cy + 0.05 * scale, 0], color=INERT_COL, stroke_width=7 * scale)
    arm_l = Line([cx, cy + 0.05 * scale, 0], [cx - 0.34 * scale, cy - 0.25 * scale, 0], color=INERT_COL, stroke_width=6 * scale)
    arm_r = Line([cx, cy + 0.05 * scale, 0], [cx + 0.34 * scale, cy - 0.25 * scale, 0], color=INERT_COL, stroke_width=6 * scale)
    cup_l = Arc(
        radius=0.25 * scale, start_angle=0, angle=PI,
        arc_center=[cx - 0.34 * scale, cy - 0.50 * scale, 0], color=RECEPTOR_COL, stroke_width=6 * scale,
    )
    cup_r = Arc(
        radius=0.25 * scale, start_angle=0, angle=PI,
        arc_center=[cx + 0.34 * scale, cy - 0.50 * scale, 0], color=RECEPTOR_COL, stroke_width=6 * scale,
    )
    return VGroup(stem, arm_l, arm_r, cup_l, cup_r)


def _scissor_icon(center):
    """Clean slate protease scissor icon."""
    cx, cy = center[0], center[1]
    b1 = Line([cx - 0.30, cy + 0.20, 0], [cx + 0.26, cy - 0.14, 0], color=TEXT, stroke_width=4.5)
    b2 = Line([cx - 0.30, cy - 0.20, 0], [cx + 0.26, cy + 0.14, 0], color=TEXT, stroke_width=4.5)
    r1 = Circle(radius=0.10, color=INERT_COL, stroke_width=4).move_to([cx - 0.40, cy + 0.24, 0])
    r2 = Circle(radius=0.10, color=INERT_COL, stroke_width=4).move_to([cx - 0.40, cy - 0.24, 0])
    return VGroup(b1, b2, r1, r2)


# ==============================================================================
# Scenes
# ==============================================================================

class S00Title(TitleCard):
    LESSON = "Reverse Signaling: When the Ligand Is Also a Receptor"
    TITLE = "Which Direction Did the Work?"


class S01LinkAndHook(SpokenScene):
    def construct(self):
        # Shift slab slightly left while putting protein at -1.2 so open cleft space on left holds KO stamp cleanly
        upper_slab, _ = _membrane_slab(1.45, 5.8, 1.50, RECEPTOR_COL, edge_is_bottom=True)
        lower_slab, _ = _membrane_slab(-1.45, 5.8, 1.50, LIGAND_COL, edge_is_bottom=False)
        upper_slab.shift(LEFT * 2.1)
        lower_slab.shift(LEFT * 2.1)
        px = -0.8
        rec_outer, rec_inner = _receptor_protein(0.0, x=px, show_kinase=True)
        lig_outer, lig_tail = _ligand_protein(0.0, x=px, show_tail=True)
        rec_lab = T("Receptor cell", 28, RECEPTOR_COL).move_to([-2.1, 2.55, 0])
        lig_lab = T("Ligand cell", 28, LIGAND_COL).move_to([-2.1, -2.55, 0])
        tag = scope_tag("schematic", color=TEXT)

        self.add(
            upper_slab, lower_slab,
            rec_outer, rec_inner, lig_outer, lig_tail,
            rec_lab, lig_lab, tag,
        )

        # Organ panel on screen right
        organ_title = T("Organ", 28, TEXT).move_to([3.7, 2.35, 0])
        organ_prog = ValueTracker(0.25)
        organ_scat = ValueTracker(0.0)
        organ = _branching_organ([3.7, -0.35, 0], organ_prog, organ_scat)
        self.add(organ_title, organ)

        # Continuous reverse signal wave
        rev_wave = _signal_wave(px + 0.72, -0.30, -1.75, LIGAND_COL, speed=0.95)
        self.add(rev_wave)

        # Beat 1: ligand signals inward + organ grows
        self.at("membrane ligand signaled inward")
        self.play(organ_prog.animate.set_value(1.0), run_time=2.3)

        self.at("tail or partner")
        tail_glow = SurroundingRectangle(lig_tail, color=LIGAND_COL, buff=0.14, stroke_width=4)
        self.play(Create(tail_glow), run_time=1.4)

        # Beat 2: Delete ligand gene (placed cleanly in open left cleft)
        self.at("delete that")
        ko_stamp = boxed_label("Delete ligand gene", OFF_COL, size=26, fill_opacity=0.20).move_to([-3.25, 0.0, 0])
        self.play(FadeIn(ko_stamp, scale=1.06), FadeOut(tail_glow), run_time=0.6)
        rev_wave.clear_updaters()
        self.play(FadeOut(lig_outer), FadeOut(lig_tail), FadeOut(rev_wave), run_time=0.8)

        # Beat 3: Organ fails to form
        self.at("organ fails to form")
        fail_lbl = T("Fails to form", 28, OFF_COL).move_to([3.7, -1.35, 0])
        self.play(
            organ_scat.animate.set_value(1.0),
            FadeIn(fail_lbl),
            FadeOut(ko_stamp),
            run_time=1.8,
        )

        # Beat 4: Which direction caused the defect?
        self.at("How can you tell")
        q_top = boxed_label("?", RECEPTOR_COL, size=34, box=(0.75, 0.75)).move_to([-3.2, 1.45, 0])
        q_bot = boxed_label("?", LIGAND_COL, size=34, box=(0.75, 0.75)).move_to([-3.2, -1.45, 0])
        self.play(FadeIn(q_top), FadeIn(q_bot), run_time=0.7)
        self.play(Indicate(q_top, color=RECEPTOR_COL, scale_factor=1.12), run_time=1.1)
        self.play(Indicate(q_bot, color=LIGAND_COL, scale_factor=1.12), run_time=1.1)

        # Beat 5: One knockout removes too much at once
        self.at("One knockout removes")
        tangle_lbl = boxed_label("Removes too much at once", OFF_COL, size=28).move_to([3.5, -2.55, 0])
        self.play(FadeIn(tangle_lbl), run_time=1.0)
        self.finish()


class S02KoTrap(SpokenScene):
    def construct(self):
        w = build_cleft_world(x_center=-2.2, width=5.4, cleft_y=0.0)
        tag = scope_tag("schematic", color=TEXT)
        tr = {"fwd": ValueTracker(1.0), "rev": ValueTracker(1.0), "grip": ValueTracker(1.0)}
        bars = build_status_bars(tr, top_left=(1.2, 1.05))
        case_lbl = boxed_label("Both intact", TEXT, size=28).move_to([3.4, 2.55, 0])

        self.add(
            w["upper_slab"], w["lower_slab"],
            w["rec_outer"], w["rec_inner"],
            w["lig_outer"], w["lig_tail"],
            w["rec_lab"], w["lig_lab"],
            bars, case_lbl, tag,
        )

        fwd_wave = _signal_wave(w["x"] + 0.75, 0.30, 1.80, RECEPTOR_COL, speed=0.95)
        rev_wave = _signal_wave(w["x"] + 0.75, -0.30, -1.80, LIGAND_COL, speed=0.95)
        self.add(fwd_wave, rev_wave)

        # Beat 1: Delete ligand gene
        self.at("when you delete")
        ko_lig = boxed_label("Delete ligand gene", LIGAND_COL, size=28).move_to([3.4, 2.55, 0])
        self.play(
            swap(case_lbl, ko_lig, run_time=0.8),
            FadeOut(w["lig_outer"]), FadeOut(w["lig_tail"]),
            run_time=2.4,
        )

        # Beat 2: First, forward signal off
        self.at("First")
        fwd_wave.clear_updaters()
        self.play(tr["fwd"].animate.set_value(0.0), FadeOut(fwd_wave), run_time=3.2)

        # Beat 3: Second, reverse signal off
        self.at("Second")
        rev_wave.clear_updaters()
        self.play(tr["rev"].animate.set_value(0.0), FadeOut(rev_wave), run_time=3.4)

        # Beat 4: Third, grip lost -> membranes drift apart
        self.at("Third")
        upper_grp = VGroup(w["upper_slab"], w["rec_outer"], w["rec_inner"], w["rec_lab"])
        lower_grp = VGroup(w["lower_slab"], w["lig_lab"])
        self.play(
            tr["grip"].animate.set_value(0.0),
            upper_grp.animate.shift(UP * 0.45),
            lower_grp.animate.shift(DOWN * 0.45),
            run_time=3.6,
        )

        # Beat 5: Restore briefly, then delete receptor gene -> exact same tangle
        self.at("Deleting the receptor gene")
        both_lbl = boxed_label("Both intact", TEXT, size=28).move_to([3.4, 2.55, 0])
        ko_rec = boxed_label("Delete receptor gene", RECEPTOR_COL, size=28).move_to([3.4, 2.55, 0])
        self.play(
            upper_grp.animate.shift(DOWN * 0.45),
            lower_grp.animate.shift(UP * 0.45),
            FadeIn(w["lig_outer"]), FadeIn(w["lig_tail"]),
            tr["fwd"].animate.set_value(1.0),
            tr["rev"].animate.set_value(1.0),
            tr["grip"].animate.set_value(1.0),
            swap(ko_lig, both_lbl, run_time=0.6),
            run_time=0.6,
        )
        self.play(
            swap(both_lbl, ko_rec, run_time=0.7),
            FadeOut(w["rec_outer"]), FadeOut(w["rec_inner"]),
            tr["fwd"].animate.set_value(0.0),
            tr["rev"].animate.set_value(0.0),
            tr["grip"].animate.set_value(0.0),
            w["upper_slab"].animate.shift(UP * 0.45),
            w["rec_lab"].animate.shift(UP * 0.45),
            VGroup(w["lower_slab"], w["lig_outer"], w["lig_tail"], w["lig_lab"]).animate.shift(DOWN * 0.45),
            run_time=1.3,
        )
        same_lbl = T("Exact same tangle", 28, OFF_COL).move_to([3.4, -2.15, 0])
        self.play(FadeIn(same_lbl), run_time=0.5)
        self.finish()


class S03RuleIdea(SpokenScene):
    def construct(self):
        w = build_cleft_world(x_center=-2.2, width=5.4, cleft_y=0.0)
        tag = scope_tag("schematic", color=TEXT)
        tr = {"fwd": ValueTracker(1.0), "rev": ValueTracker(1.0), "grip": ValueTracker(1.0)}
        bars = build_status_bars(tr, top_left=(1.2, 1.05))
        rule_lbl = boxed_label("Disable one inner route", TEXT, size=28).move_to([3.4, 2.55, 0])

        self.add(
            w["upper_slab"], w["lower_slab"],
            w["rec_outer"], w["rec_inner"],
            w["lig_outer"], w["lig_tail"],
            w["rec_lab"], w["lig_lab"],
            bars, rule_lbl, tag,
        )

        fwd_wave = _signal_wave(w["x"] + 0.75, 0.30, 1.80, RECEPTOR_COL, speed=0.95)
        rev_wave = _signal_wave(w["x"] + 0.75, -0.30, -1.80, LIGAND_COL, speed=0.95)
        self.add(fwd_wave, rev_wave)

        self.at("disable one")
        self.wait(1.5)

        # Beat 2: Keep outer binding tip on cell surface (clear of clasp ring)
        self.at("Leave the outer binding tip")
        clasp_ring = Circle(radius=0.40, color=GRIP_COL, stroke_width=4).move_to([w["x"], 0.12, 0])
        tip_lbl = T("Outer tip kept", 28, GRIP_COL).move_to([w["x"] - 1.72, 0.12, 0])
        self.play(Create(clasp_ring), FadeIn(tip_lbl), run_time=1.0)

        self.at("two cells still grip")
        self.play(Indicate(bars[2], color=GRIP_COL, scale_factor=1.06), run_time=1.2)

        # Beat 3: Cut ONLY receptor's inner kinase domain
        self.at("Then cut or swap")
        cut_line = DashedLine(
            [w["x"] - 0.65, 0.96, 0], [w["x"] + 0.65, 0.96, 0],
            color=OFF_COL, stroke_width=4.5, dash_length=0.12,
        )
        self.play(Create(cut_line), FadeOut(clasp_ring), run_time=0.8)
        fwd_wave.clear_updaters()
        self.play(
            w["rec_inner"].animate.shift(UP * 0.25).set_opacity(0.0),
            FadeOut(fwd_wave),
            tr["fwd"].animate.set_value(0.0),
            run_time=1.6,
        )
        self.remove(w["rec_inner"])

        # Beat 4: Other side stays intact -> continuous reverse signal wave runs until finish
        self.at("keeping the other side intact")
        self.play(FadeOut(cut_line), run_time=0.6)
        self.finish()


# ==============================================================================
# Shared two-lane EphB2 / Ephrin-B builder for S04, S05, S06, S07
# ==============================================================================

def build_ephb2_lanes(
    top_label="No EphB2",
    top_has_outer=False,
    top_kinase="none",
    top_prog=1.0,
    top_veer=1.0,
    bot_label="Outer tip kept",
    bot_has_outer=True,
    bot_kinase="coral",
    bot_prog=1.0,
    bot_veer=0.0,
):
    """Build the two stacked developing brain tract lanes ('Anterior commissure')."""
    head = T("Anterior commissure", 30, TEXT).move_to([0, 3.25, 0])
    # Top-right scope tag leaves bottom-right clear for PredictPause countdown ring
    tag = T("schematic", 24, TEXT).move_to([5.75, 3.25, 0])
    floor_xs = [-1.55, 0.1, 1.75, 3.4, 5.05]

    # Top lane frame (y: 0.25 .. 2.75)
    top_frame = RoundedRectangle(
        corner_radius=0.16, width=12.3, height=2.45,
        stroke_color=INERT_COL, stroke_width=2.5, fill_color=BG, fill_opacity=0.45,
    ).move_to([0, 1.50, 0])
    top_lbl = boxed_label(top_label, OFF_COL if "No" in top_label else RECEPTOR_COL, size=26, box=(3.1, 0.55))
    top_lbl.move_to([-4.25, 2.25, 0])

    top_cells, top_outer, top_inner = _floor_cells_row(
        floor_xs, y_floor=0.72, has_outer=top_has_outer, kinase_mode=top_kinase,
    )
    t_prog = ValueTracker(top_prog)
    t_veer = ValueTracker(top_veer)
    top_axons = _computed_axon_tract(-5.7, 5.8, 1.62, t_prog, t_veer, veer_start=-1.4)

    # Bottom lane frame (y: -2.45 .. 0.05) -> leaves y -3.5..-2.55 clear for question_card
    bot_frame = RoundedRectangle(
        corner_radius=0.16, width=12.3, height=2.45,
        stroke_color=RECEPTOR_COL, stroke_width=2.5, fill_color=BG, fill_opacity=0.45,
    ).move_to([0, -1.20, 0])
    bot_lbl = boxed_label(bot_label, RECEPTOR_COL, size=26, box=(3.1, 0.55))
    bot_lbl.move_to([-4.25, -0.45, 0])

    bot_cells, bot_outer, bot_inner = _floor_cells_row(
        floor_xs, y_floor=-1.98, has_outer=bot_has_outer, kinase_mode=bot_kinase,
    )
    b_prog = ValueTracker(bot_prog)
    b_veer = ValueTracker(bot_veer)
    bot_axons = _computed_axon_tract(-5.7, 5.8, -1.08, b_prog, b_veer, veer_start=-1.4)

    return {
        "head": head,
        "tag": tag,
        "top_frame": top_frame,
        "top_lbl": top_lbl,
        "top_cells": top_cells,
        "top_outer": top_outer,
        "top_inner": top_inner,
        "top_axons": top_axons,
        "t_prog": t_prog,
        "t_veer": t_veer,
        "top_grp": VGroup(top_frame, top_lbl, top_cells, top_outer, top_inner, top_axons),
        "bot_frame": bot_frame,
        "bot_lbl": bot_lbl,
        "bot_cells": bot_cells,
        "bot_outer": bot_outer,
        "bot_inner": bot_inner,
        "bot_axons": bot_axons,
        "b_prog": b_prog,
        "b_veer": b_veer,
        "bot_grp": VGroup(bot_frame, bot_lbl, bot_cells, bot_outer, bot_inner, bot_axons),
        "floor_xs": floor_xs,
    }


class S04Ephb2Setup(SpokenScene):
    def construct(self):
        L = build_ephb2_lanes(
            top_label="Wild type", top_has_outer=True, top_kinase="coral",
            top_prog=0.18, top_veer=0.0,
            bot_label="Outer tip kept", bot_has_outer=True, bot_kinase="coral",
            bot_prog=0.18, bot_veer=0.0,
        )
        # Only add top lane initially (do not toggle opacity on bot_grp!)
        self.add(L["head"], L["tag"], L["top_frame"], L["top_lbl"], L["top_cells"], L["top_outer"], L["top_inner"], L["top_axons"])

        axon_tag = T("Axons (Ephrin-B)", 26, LIGAND_COL).move_to([-4.25, 1.05, 0])
        floor_tag = T("Floor cells (EphB2)", 26, RECEPTOR_COL).move_to([-4.25, 0.55, 0])
        self.play(FadeIn(axon_tag), FadeIn(floor_tag), run_time=0.8)

        # Beat 1: Growing axons carrying B-type ephrins cross floor cells carrying EphB2
        self.at("Growing axons carrying")
        self.play(L["t_prog"].animate.set_value(0.68), run_time=3.6, rate_func=linear)

        self.at("the receptor")
        self.play(
            Indicate(L["top_outer"], color=RECEPTOR_COL, scale_factor=1.1),
            L["t_prog"].animate.set_value(1.0),
            run_time=2.4, rate_func=linear,
        )

        # Beat 2: Mice lacking EphB2 completely -> swap floor label so it never says "(EphB2)" when EphB2 is gone
        self.at("In mice lacking")
        no_ephb2_lbl = boxed_label("No EphB2", OFF_COL, size=26, box=(3.1, 0.55)).move_to([-4.25, 2.25, 0])
        plain_floor_tag = T("Floor cells", 26, RECEPTOR_COL).move_to([-4.25, 0.55, 0])
        self.play(
            swap(L["top_lbl"], no_ephb2_lbl, run_time=0.6),
            swap(floor_tag, plain_floor_tag, run_time=0.6),
            FadeOut(L["top_outer"]), FadeOut(L["top_inner"]),
            L["t_prog"].animate.set_value(0.20),
            run_time=1.8,
        )

        self.at("those axons veer off course")
        self.play(
            L["t_prog"].animate.set_value(0.95),
            L["t_veer"].animate.set_value(1.0),
            run_time=2.8, rate_func=linear,
        )

        # Beat 3: Second mouse keeps EphB2's outer tip on the surface
        self.at("A second mouse keeps")
        self.play(
            FadeIn(L["bot_frame"]), FadeIn(L["bot_lbl"]),
            FadeIn(L["bot_cells"]), FadeIn(L["bot_outer"]), FadeIn(L["bot_inner"]),
            run_time=1.2,
        )
        self.add(L["bot_axons"])
        self.play(L["b_prog"].animate.set_value(0.55), run_time=2.4, rate_func=linear)
        self.finish()


def _inert_callout(target_block):
    """Slate swatch + 'Inert marker' label beside the floor cells with a leader arrow to a slate block."""
    swatch = RoundedRectangle(
        corner_radius=0.06, width=0.34, height=0.20,
        stroke_color=INERT_COL, stroke_width=2, fill_color=INERT_COL, fill_opacity=0.9,
    )
    lbl = T("Inert marker", 24, TEXT)
    tag = VGroup(swatch, lbl).arrange(RIGHT, buff=0.14).move_to([-3.85, -2.02, 0])
    arrow = Arrow(
        tag.get_right() + RIGHT * 0.10,
        target_block.get_left() + LEFT * 0.06,
        buff=0, color=INERT_COL, stroke_width=3.5, tip_length=0.16,
    )
    return VGroup(tag, arrow)


class S05PredictPrompt(SpokenScene):
    def construct(self):
        L = build_ephb2_lanes(
            top_label="No EphB2", top_has_outer=False, top_kinase="none",
            top_prog=0.95, top_veer=1.0,
            bot_label="Outer tip kept", bot_has_outer=True, bot_kinase="coral",
            bot_prog=0.55, bot_veer=0.0,
        )
        self.add(
            L["head"], L["tag"],
            L["top_frame"], L["top_lbl"], L["top_cells"], L["top_axons"],
            L["bot_frame"], L["bot_lbl"], L["bot_cells"], L["bot_outer"], L["bot_inner"], L["bot_axons"],
        )

        # Beat 1: Inert bacterial enzyme replaces receptor's inner kinase
        self.at("an inert bacterial enzyme replaces")
        kin_lbl = boxed_label("Kinase-less EphB2", RECEPTOR_COL, size=26, box=(3.1, 0.55)).move_to([-4.25, -0.45, 0])
        inert_blocks = VGroup(*[
            RoundedRectangle(
                corner_radius=0.07, width=0.46, height=0.26,
                stroke_color=INERT_COL, stroke_width=2, fill_color=INERT_COL, fill_opacity=0.9,
            ).move_to(b.get_center())
            for b in L["bot_inner"]
        ])
        inert_tag = _inert_callout(inert_blocks[0])
        self.play(
            swap(L["bot_lbl"], kin_lbl, run_time=0.9),
            ReplacementTransform(L["bot_inner"], inert_blocks),
            FadeIn(inert_tag),
            run_time=4.2,
        )

        # Beat 2: Removes receptor's own kinase signal
        self.at("That change removes")
        fwd_off = T("Forward kinase: OFF", 26, OFF_COL).move_to([3.85, -0.45, 0])
        self.play(FadeIn(fwd_off), Indicate(inert_blocks, color=INERT_COL, scale_factor=1.08), run_time=3.2)

        # Beat 3: Yet axons still stay right on course
        self.at("Yet the axons still stay right on course")
        self.play(L["b_prog"].animate.set_value(1.0), run_time=3.2, rate_func=linear)

        # Beat 4: Pause and think: question card appears
        self.at("Pause and think")
        q = question_card("Which cell received the guidance signal?", y=-3.05, color=TEXT, size=30)
        self.play(FadeIn(q), run_time=1.4)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which cell received the guidance signal?"
    CARD = {"color": TEXT, "y": -3.05, "size": 30}
    RING_AT = (5.9, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        L = build_ephb2_lanes(
            top_label="No EphB2", top_has_outer=False, top_kinase="none",
            top_prog=0.95, top_veer=1.0,
            bot_label="Kinase-less EphB2", bot_has_outer=True, bot_kinase="inert",
            bot_prog=1.0, bot_veer=0.0,
        )
        inert_tag = _inert_callout(L["bot_inner"][0])
        fwd_off = T("Forward kinase: OFF", 26, OFF_COL).move_to([3.85, -0.45, 0])
        return VGroup(
            L["head"], L["tag"],
            L["top_frame"], L["top_lbl"], L["top_cells"], L["top_axons"],
            L["bot_frame"], L["bot_lbl"], L["bot_cells"], L["bot_outer"], L["bot_inner"], L["bot_axons"],
            inert_tag, fwd_off,
        )


class S07PredictReveal(SpokenScene):
    def construct(self):
        # Start from the exact end frame of S06
        L = build_ephb2_lanes(
            top_label="No EphB2", top_has_outer=False, top_kinase="none",
            top_prog=0.95, top_veer=1.0,
            bot_label="Kinase-less EphB2", bot_has_outer=True, bot_kinase="inert",
            bot_prog=1.0, bot_veer=0.0,
        )
        inert_tag = _inert_callout(L["bot_inner"][0])
        fwd_off = T("Forward kinase: OFF", 26, OFF_COL).move_to([3.85, -0.45, 0])
        q = question_card("Which cell received the guidance signal?", y=-3.05, color=TEXT, size=30)
        self.add(
            L["head"], L["tag"],
            L["top_frame"], L["top_lbl"], L["top_cells"], L["top_axons"],
            L["bot_frame"], L["bot_lbl"], L["bot_cells"], L["bot_outer"], L["bot_inner"], L["bot_axons"],
            inert_tag, fwd_off, q,
        )

        # Transition cleanly to zoomed Kinase-less EphB2 contact
        self.play(
            FadeOut(q), FadeOut(L["head"]),
            FadeOut(L["top_grp"]), FadeOut(L["bot_grp"]),
            FadeOut(inert_tag), FadeOut(fwd_off),
            run_time=0.8,
        )

        lane_title = boxed_label("Kinase-less EphB2", RECEPTOR_COL, size=28).move_to([-3.9, 3.05, 0])
        axon_lbl = T("Axon carrying Ephrin-B", 28, LIGAND_COL).move_to([1.3, 3.05, 0])
        floor_xs = [-3.2, 0.0, 3.2]
        floor_cells = VGroup()
        outer_tips = VGroup()
        inert_blocks = VGroup()
        ephrin_plugs = VGroup()
        for cx in floor_xs:
            fc = RoundedRectangle(
                corner_radius=0.18, width=2.45, height=1.25,
                stroke_color=RECEPTOR_COL, stroke_width=3, fill_color=RECEPTOR_COL, fill_opacity=0.16,
            ).move_to([cx, -2.15, 0])
            floor_cells.add(fc)
            ib = RoundedRectangle(
                corner_radius=0.10, width=0.88, height=0.44,
                stroke_color=INERT_COL, stroke_width=2.5, fill_color=INERT_COL, fill_opacity=0.9,
            ).move_to([cx, -2.15, 0])
            inert_blocks.add(ib)
            stem = Line([cx, -1.52, 0], [cx, -0.62, 0], color=RECEPTOR_COL, stroke_width=7)
            cup = Arc(radius=0.28, start_angle=PI, angle=PI, arc_center=[cx, -0.34, 0], color=RECEPTOR_COL, stroke_width=7)
            outer_tips.add(VGroup(stem, cup))
            plug = Dot([cx, -0.34, 0], radius=0.16, color=LIGAND_COL, stroke_color=TEXT, stroke_width=2)
            ephrin_stem = Line([cx, -0.18, 0], [cx, 0.50, 0], color=LIGAND_COL, stroke_width=6)
            ephrin_plugs.add(VGroup(plug, ephrin_stem))

        inert_lbl = T("Inert (dark)", 26, TEXT).move_to([0.0, -3.10, 0])
        axon_slab = RoundedRectangle(
            corner_radius=0.22, width=10.8, height=1.25,
            stroke_color=LIGAND_COL, stroke_width=4, fill_color=LIGAND_COL, fill_opacity=0.16,
        ).move_to([0, 1.15, 0])

        self.play(
            FadeIn(lane_title), FadeIn(axon_lbl),
            FadeIn(floor_cells), FadeIn(inert_blocks), FadeIn(outer_tips),
            FadeIn(axon_slab), FadeIn(ephrin_plugs), FadeIn(inert_lbl),
            run_time=0.9,
        )

        # Beat 1: Axons received the signal -> continuous amber reverse waves inside axon slab
        self.at("received the signal")
        rev_waves = VGroup(*[
            _signal_wave(cx + 0.45, 0.68, 1.62, LIGAND_COL, speed=1.35, wave_w=1.15)
            for cx in floor_xs
        ])
        self.add(rev_waves)
        self.wait(1.6)

        # Beat 2: Only working part left was receptor's outer tip
        self.at("receptor's outer tip")
        tip_ring = Circle(radius=0.52, color=RECEPTOR_COL, stroke_width=4).move_to([0, -0.45, 0])
        self.play(Create(tip_ring), run_time=1.1)

        # Beat 3: Stayed on floor cells & gripped ephrins
        self.at("That tip stayed on the floor cells")
        self.play(FadeOut(tip_ring), Indicate(outer_tips, color=RECEPTOR_COL, scale_factor=1.05), run_time=1.5)

        # Beat 4: Message ran inward there
        self.at("so the message ran inward there")
        self.wait(1.2)

        # Beat 5: Receptor acted as ligand / ephrin acted as receptor (cleanly clear of stems and arrows!)
        self.at("Here the protein named receptor")
        lig_role = boxed_label("Acts as ligand", RECEPTOR_COL, size=26).move_to([-1.60, -0.98, 0])
        self.play(FadeIn(lig_role), run_time=0.9)

        self.at("acted as the ligand")
        rec_role = boxed_label("Acts as receptor", LIGAND_COL, size=26).move_to([0.0, 2.22, 0])
        self.play(FadeIn(rec_role), run_time=1.0)
        self.finish()


class S08ReceptorFc(SpokenScene):
    def construct(self):
        w = build_cleft_world(x_center=0.0, width=8.4, cleft_y=-0.3, inert_kinase=True)
        tag = scope_tag("schematic", color=TEXT)
        mode_lbl = boxed_label("Mutant: tests if needed", TEXT, size=28).move_to([-3.4, 3.05, 0])

        self.add(
            w["upper_slab"], w["lower_slab"],
            w["rec_outer"], w["rec_inner"],
            w["lig_outer"], w["lig_tail"],
            w["rec_lab"], w["lig_lab"],
            mode_lbl, tag,
        )

        lig_xs = [-2.2, 0.0, 2.2]
        extra_ligs = VGroup()
        for lx in (-2.2, 2.2):
            lo, lt = _ligand_protein(w["cleft_y"], x=lx, show_tail=True)
            extra_ligs.add(lo, lt)
        self.add(extra_ligs)

        rev_0 = _signal_wave(0.45, -0.60, -2.05, LIGAND_COL, speed=0.95)
        self.add(rev_0)

        # Beat 1: Second tool tests whether reverse signaling is enough on its own
        self.at("A second tool tests")
        suff_lbl = boxed_label("Tests if sufficient alone", LIGAND_COL, size=28).move_to([-3.4, 3.05, 0])
        upper_all = VGroup(w["upper_slab"], w["rec_outer"], w["rec_inner"], w["rec_lab"])
        rev_0.clear_updaters()
        self.play(
            swap(mode_lbl, suff_lbl, run_time=0.8),
            FadeOut(rev_0),
            FadeOut(upper_all, shift=UP * 2.0),
            run_time=2.8,
        )

        # Beat 2: Introduce the building blocks smoothly and fuse receptor outer tip to antibody handle
        tip_l = Arc(radius=0.18, start_angle=0, angle=PI, arc_center=[-2.4, 1.4, 0], color=RECEPTOR_COL, stroke_width=6)
        tip_r = Arc(radius=0.18, start_angle=0, angle=PI, arc_center=[2.4, 1.4, 0], color=RECEPTOR_COL, stroke_width=6)
        fc_handle = VGroup(
            Line([0, 2.35, 0], [0, 1.95, 0], color=INERT_COL, stroke_width=7),
            Line([0, 1.95, 0], [-0.34, 1.65, 0], color=INERT_COL, stroke_width=6),
            Line([0, 1.95, 0], [0.34, 1.65, 0], color=INERT_COL, stroke_width=6),
        )
        self.play(FadeIn(tip_l), FadeIn(tip_r), FadeIn(fc_handle), run_time=1.4)
        self.play(
            tip_l.animate.move_to([-0.9, 1.4, 0]),
            tip_r.animate.move_to([0.9, 1.4, 0]),
            run_time=1.3,
        )

        self.at("Scientists fuse")
        fc_body_c = _soluble_receptor_fc([0.0, 1.80], scale=1.0)
        self.play(
            ReplacementTransform(VGroup(tip_l, tip_r, fc_handle), fc_body_c),
            run_time=1.8,
        )

        # Beat 3: Soluble receptor body docks onto lower membrane ligands
        self.at("soluble receptor body")
        fc_tag = boxed_label("Receptor-Fc", RECEPTOR_COL, size=28).move_to([3.85, 1.65, 0])
        fc_body_l = _soluble_receptor_fc([-2.54, 1.85], scale=1.0)
        fc_body_r = _soluble_receptor_fc([1.86, 1.85], scale=1.0)
        self.play(FadeIn(fc_tag), FadeIn(fc_body_l), FadeIn(fc_body_r), run_time=1.3)

        self.at("With no receptor cell present")
        no_cell_note = T("No receptor cell present", 28, TEXT).move_to([3.3, 3.05, 0])
        self.play(
            FadeIn(no_cell_note),
            fc_body_c.animate.move_to([-0.34, 0.24, 0]),
            fc_body_l.animate.move_to([-2.54, 0.24, 0]),
            fc_body_r.animate.move_to([1.86, 0.24, 0]),
            run_time=2.0,
        )

        # Beat 4: Response must have entered through ligand -> continuous amber reverse waves
        self.at("a response that needs the ligand")
        rev_waves = VGroup(*[
            _signal_wave(lx + 0.45, -0.60, -2.05, LIGAND_COL, speed=0.95)
            for lx in lig_xs
        ])
        self.add(rev_waves)
        self.at("entered through it")
        self.finish()


class S09TnfCleavage(SpokenScene):
    def construct(self):
        tag = scope_tag("schematic", color=TEXT)
        title_lbl = boxed_label("Sympathetic axon", LIGAND_COL, size=28).move_to([-4.0, 3.05, 0])

        axon_slab = RoundedRectangle(
            corner_radius=0.20, width=7.6, height=1.55,
            stroke_color=LIGAND_COL, stroke_width=4, fill_color=LIGAND_COL, fill_opacity=0.14,
        ).move_to([-2.1, -1.65, 0])

        def _tnf_unit(cx):
            stalks = VGroup(*[
                Line([cx + dx, -1.35, 0], [cx + dx, -0.45, 0], color=LIGAND_COL, stroke_width=5)
                for dx in (-0.16, 0.0, 0.16)
            ])
            trimer = RoundedRectangle(
                corner_radius=0.10, width=0.68, height=0.40,
                stroke_color=TEXT, stroke_width=2, fill_color=LIGAND_COL, fill_opacity=0.92,
            ).move_to([cx, -0.25, 0])
            return stalks, trimer

        s1, t1 = _tnf_unit(-3.8)
        s2, t2 = _tnf_unit(-1.4)
        tnf_lbl = T("Membrane TNF", 28, LIGAND_COL).move_to([-2.6, -2.90, 0])

        branch_prog = ValueTracker(0.0)
        branch_specs = [
            ((1.65, -1.65, 0), (3.1, -1.65, 0), 0.0, 0.30, 6.0),
            ((3.1, -1.65, 0), (4.4, -0.85, 0), 0.30, 0.65, 5.1),
            ((3.1, -1.65, 0), (4.5, -2.35, 0), 0.30, 0.65, 5.1),
            ((4.4, -0.85, 0), (5.6, -0.35, 0), 0.65, 1.00, 4.1),
            ((4.4, -0.85, 0), (5.7, -1.25, 0), 0.65, 1.00, 4.1),
            ((4.5, -2.35, 0), (5.7, -1.95, 0), 0.65, 1.00, 4.1),
            ((4.5, -2.35, 0), (5.6, -2.85, 0), 0.65, 1.00, 4.1),
        ]

        def _branches_mk():
            p = float(np.clip(branch_prog.get_value(), 0.0, 1.0))
            grp = VGroup()
            for a, b, start, end, sw in branch_specs:
                local = float(np.clip((p - start) / (end - start), 0.0, 1.0))
                if local <= 0.01:
                    continue
                pa, pb = np.array(a), np.array(b)
                pc = pa + local * (pb - pa)
                grp.add(Line(pa, pc, color=LIGAND_COL, stroke_width=sw))
            return grp

        branches = always_redraw(_branches_mk)
        self.add(tag, title_lbl, axon_slab)

        # Beat 0: Developing sympathetic axon extends and displays uncut membrane TNF
        self.play(GrowFromEdge(axon_slab, LEFT), run_time=1.8)
        self.add(branches)
        self.play(branch_prog.animate.set_value(0.30), run_time=1.0)
        self.at("uncut membrane TNF")
        self.play(
            FadeIn(s1, shift=UP * 0.15), FadeIn(t1, shift=UP * 0.15),
            FadeIn(s2, shift=UP * 0.15), FadeIn(t2, shift=UP * 0.15),
            FadeIn(tnf_lbl),
            run_time=1.3,
        )
        self.play(Indicate(VGroup(s1, t1, s2, t2), color=LIGAND_COL, scale_factor=1.06), run_time=1.2)

        # Beat 1: Add soluble TNFR1-Fc -> docks onto uncut TNF
        self.at("Adding soluble TNF receptor 1")
        fc1 = _soluble_receptor_fc([-4.14, 1.55], scale=0.95)
        fc2 = _soluble_receptor_fc([-1.74, 1.55], scale=0.95)
        fc_lbl = boxed_label("TNFR1-Fc", RECEPTOR_COL, size=28).move_to([-0.2, 2.35, 0])
        self.play(FadeIn(fc1), FadeIn(fc2), FadeIn(fc_lbl), run_time=0.9)
        self.play(
            fc1.animate.move_to([-4.14, 0.44, 0]),
            fc2.animate.move_to([-1.74, 0.44, 0]),
            run_time=1.4,
        )

        # Beat 2: Continuous amber reverse signal waves + axon branches sprout
        self.at("those axons branch more")
        rev_p1 = _signal_wave(-3.25, -0.90, -2.20, LIGAND_COL, speed=0.95)
        rev_p2 = _signal_wave(-0.85, -0.90, -2.20, LIGAND_COL, speed=0.95)
        self.add(rev_p1, rev_p2)
        self.play(branch_prog.animate.set_value(0.65), run_time=2.5)

        self.at("That growth requires")
        self.play(branch_prog.animate.set_value(1.0), run_time=2.4)

        # Beat 3: Protease cuts TNF loose -> inward link breaks (label cleanly clear of axon & scissors)
        self.at("If a protease cuts TNF loose")
        scissors = _scissor_icon([0.1, -0.68, 0])
        prot_lbl = T("Protease", 26, TEXT).move_to([0.95, 0.10, 0])
        self.play(FadeIn(scissors), FadeIn(prot_lbl), run_time=0.6)
        self.play(scissors.animate.shift(LEFT * 4.2), run_time=1.3)

        self.at("that inward link breaks")
        rev_p1.clear_updaters()
        rev_p2.clear_updaters()
        self.play(
            FadeOut(scissors), FadeOut(prot_lbl),
            FadeOut(rev_p1), FadeOut(rev_p2),
            FadeOut(fc1), FadeOut(fc2), FadeOut(fc_lbl),
            s1.animate.scale([1, 0.55, 1], about_point=[-3.8, -1.35, 0]),
            s2.animate.scale([1, 0.55, 1], about_point=[-1.4, -1.35, 0]),
            run_time=1.2,
        )

        # Beat 4: Released TNF floats upward toward distant teal receptor and signals forward
        self.at("Released TNF can still float off")
        dist_cell = RoundedRectangle(
            corner_radius=0.18, width=3.4, height=1.25,
            stroke_color=RECEPTOR_COL, stroke_width=3, fill_color=RECEPTOR_COL, fill_opacity=0.15,
        ).move_to([3.8, 2.45, 0])
        dist_lbl = T("Target TNFR1", 26, RECEPTOR_COL).move_to([3.8, 3.35, 0])
        dist_cup = VGroup(
            Line([3.8, 1.82, 0], [3.8, 1.25, 0], color=RECEPTOR_COL, stroke_width=6),
            Arc(radius=0.28, start_angle=0, angle=PI, arc_center=[3.8, 0.98, 0], color=RECEPTOR_COL, stroke_width=6),
        )
        self.play(FadeIn(dist_cell), FadeIn(dist_lbl), FadeIn(dist_cup), run_time=0.6)
        self.play(
            t2.animate.move_to([3.8, 0.85, 0]),
            t1.animate.move_to([1.2, 1.55, 0]),
            run_time=1.2,
        )

        self.at("and signal forward")
        dist_fwd = _signal_wave(4.55, 1.45, 2.55, RECEPTOR_COL, speed=0.95)
        self.add(dist_fwd)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        tp = TwoPanel("Full KO", "Targeted cut", colors=(OFF_COL, RECEPTOR_COL), top=3.2, bottom=-2.6)
        tag = scope_tag("schematic", color=TEXT)
        self.add(tp, tag)

        # Left panel: Full KO (placed with clean clearance below heading)
        l_tr = {"fwd": ValueTracker(1.0), "rev": ValueTracker(1.0), "grip": ValueTracker(1.0)}
        lw = build_cleft_world(x_center=0.0, width=4.6, cleft_y=0.0)
        l_cleft = VGroup(lw["upper_slab"], lw["lower_slab"], lw["rec_outer"], lw["rec_inner"], lw["lig_outer"], lw["lig_tail"])
        l_cleft.scale(0.46).move_to([-3.2, 1.08, 0])
        l_bars = build_status_bars(l_tr, top_left=(-5.35, -0.55), bar_w=1.8, row_h=0.70)

        # Right panel: Targeted cut
        r_tr = {"fwd": ValueTracker(0.0), "rev": ValueTracker(1.0), "grip": ValueTracker(1.0)}
        rw = build_cleft_world(x_center=0.0, width=4.6, cleft_y=0.0)
        r_cleft = VGroup(rw["upper_slab"], rw["lower_slab"], rw["rec_outer"], rw["lig_outer"], rw["lig_tail"])
        r_cleft.scale(0.46).move_to([3.2, 1.08, 0])
        r_bars = build_status_bars(r_tr, top_left=(1.05, -0.55), bar_w=1.8, row_h=0.70)

        r_rev_wave = _signal_wave(3.68, 0.92, 0.15, LIGAND_COL, speed=1.35, width=0.22, wave_w=0.95)
        self.add(l_cleft, l_bars, r_cleft, r_bars, r_rev_wave)

        # Beat 1: Full knockouts erase forward, reverse, cell contact all at once
        self.at("forward signaling")
        self.play(
            FadeOut(lw["lig_outer"]), FadeOut(lw["lig_tail"]),
            l_tr["fwd"].animate.set_value(0.0),
            run_time=1.1,
        )
        # Remove deleted ligand from l_cleft so it can never reappear
        l_cleft.remove(lw["lig_outer"], lw["lig_tail"])

        self.at("reverse signaling")
        self.play(l_tr["rev"].animate.set_value(0.0), run_time=1.0)

        self.at("cell contact all at once")
        self.play(
            l_tr["grip"].animate.set_value(0.0),
            lw["upper_slab"].animate.shift(UP * 0.18),
            lw["rec_outer"].animate.shift(UP * 0.18),
            lw["rec_inner"].animate.shift(UP * 0.18),
            lw["lower_slab"].animate.shift(DOWN * 0.18),
            run_time=1.3,
        )

        # Beat 2: Keep outer binding intact and disable one inner route
        self.at("Keep outer binding intact")
        clasp = Circle(radius=0.34, color=GRIP_COL, stroke_width=4).move_to([3.2, 1.12, 0])
        self.play(Create(clasp), run_time=1.2)

        self.at("disable one")
        self.play(
            FadeOut(clasp),
            Indicate(r_bars[0], color=OFF_COL, scale_factor=1.05),
            run_time=1.6,
        )

        # Beat 3: Only then can you prove which cell received the message
        self.at("Only then can you prove")
        self.play(
            tp.left_frame.animate.set_stroke(opacity=0.25),
            lw["upper_slab"][0].animate.set_fill(opacity=0.05),
            lw["upper_slab"][1].animate.set_stroke(opacity=0.35),
            lw["lower_slab"][0].animate.set_fill(opacity=0.05),
            lw["lower_slab"][1].animate.set_stroke(opacity=0.35),
            lw["rec_outer"].animate.set_opacity(0.35),
            lw["rec_inner"].animate.set_opacity(0.35),
            tp.right_frame.animate.set_stroke(width=5),
            run_time=1.8,
        )
        self.finish()


class S11End(EndCard):
    LINE = "To separate bidirectional signals, disable one inner route while keeping binding."
