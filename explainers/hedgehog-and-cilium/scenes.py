"""Hedgehog Releases a Brake — animation scenes for STEMhop.

COLOUR MAP (one colour per concept across the whole film):
  BG            = "#0F1117"  dark canvas
  TEXT          = "#E8EAF0"  primary labels
  GREY          = "#8B93A1"  structural / muted notes
  HH_GOLD       = "#F5A623"  Hedgehog secreted signal & source cell
  PTCH_CORAL    = "#E05A47"  Patched brake / transporter (active)
  PTCH_DIM      = "#7D423B"  Patched shape fill when switched off
  PTCH_DIM_TEXT = "#C9857B"  Patched (OFF) high-contrast muted label
  SMO_TEAL      = "#2AB7CA"  Smoothened transducer (active ON)
  SMO_DIM       = "#345963"  Smoothened shape outline when OFF
  SMO_DIM_TEXT  = "#72A8B5"  Smoothened (OFF) high-contrast muted label
  STEROL_AMB    = "#FFD166"  sterol / cholesterol candidate (schematic)
  GLI_VIOLET    = "#9B72F2"  Gli DNA-binding front half (repressor)
  GLI_LAV       = "#C4B5FD"  Gli activating back half
  KINASE_BLUE   = "#6C8EBF"  kinases & proteasome machinery
  GENE_GREEN    = "#83C167"  target genes switched ON
  CELL_LINE     = "#4B5973"  cell / membrane outlines
  NUC_FILL      = "#222E47"  nucleus dome interior

CARRIED WORLD:
  S01-S02: A horizontal row of 6 schematic embryonic cells (left source cell + 5 receiving cells).
  S03-S09: Camera zooms into receiving cell #3: plasma membrane across the upper third,
           cytosol in the middle, nucleus dome with target gene bar at the bottom.
  S10:     Side-by-side split of that same cell cross-section (- Hedgehog vs + Hedgehog).

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
  S01Hook:           Gold Hedgehog spheres emit from the left source cell and drift rightward
                     across 6 cells (deterministic stream + rng(7)); above, a schematic switch
                     compares pressing an active ON button vs removing a coral brake block.
  S02Morphogen:      1D exponential diffusion simulation (C(x) = exp(-0.55*x), rng(7)) drives
                     gold Hedgehog spheres rightward while a live Plot draws the schematic gradient,
                     an exposure-time bar fills, and cells 1-5 shift tint from accumulated dose.
  S03OffSwitch:      Camera zooms from the 6-cell row into receiving cell #3; Patched actively
                     radiates brake waves that hold 1 then 3 separated Smoothened blocks OFF
                     across a visible no-contact gap.
  S04SterolModel:    Bilayer sterol simulation (rng(7)) moves amber sterol ovals; active Patched
                     sweeps them away from the 3 Smoothened blocks, carving a sterol-poor halo
                     while open-question badges mark unknown cargo and power source.
  S05DoubleNegative: Gold Hedgehog with 2 lipid tails docks into Patched's groove and dims it;
                     amber sterols immediately diffuse into the 3 Smoothened blocks, lighting
                     them ON while the double-negative logic chain (-| , -|) builds above.
  S06GliOff:         Panning into cytosol & nucleus (Hedgehog gone, Patched ON sweeping sterols,
                     Smoothened OFF): two-part Gli receives P beads from kinases, proteasome shreds
                     ONLY its lavender back half into fading specks (rng(7)), and the violet
                     front piece enters the nucleus and locks target genes OFF.
  S07Predict:        Hedgehog docks on Patched and turns Smoothened ON at top as sterols enter;
                     below, two dashed hypotheses animate (A: glue cut repressor + fragments vs
                     B: spare fresh full-length Gli) above the predict question card.
  S09Reveal:         Path A crosses out and fades; kinases dim and step back while sterols keep
                     Smoothened ON; fresh intact Gli glides past the idle proteasome into the
                     nucleus whole and switches target genes ON with active transcription pulses.
  S10Synthesis:      Side-by-side live comparison of the same cell cross-section without vs with
                     Hedgehog: active Patched / sterol sweep / trimmed Gli / Genes OFF on left vs
                     docked Hedgehog / sterols at Smoothened / intact Gli / Genes ON on right.
"""
from bp_parts import *

# ------------------------------------------------------------------ Film colour map
HH_GOLD       = "#F5A623"
PTCH_CORAL    = "#E05A47"
PTCH_DIM      = "#7D423B"
PTCH_DIM_TEXT = "#C9857B"
SMO_TEAL      = "#2AB7CA"
SMO_DIM       = "#345963"
SMO_DIM_TEXT  = "#72A8B5"
STEROL_AMB    = "#FFD166"
GLI_VIOLET    = "#9B72F2"
GLI_LAV       = "#C4B5FD"
KINASE_BLUE   = "#6C8EBF"
GENE_GREEN    = "#83C167"
CELL_LINE     = "#4B5973"
NUC_FILL      = "#222E47"

CELL_XS = [-4.75, -2.85, -0.95, 0.95, 2.85, 4.75]
CELL_W = 1.68
CELL_H = 2.05
CELL_Y = -1.65


# ------------------------------------------------------------------ Shared builders
def build_cell_row(highlight_source=True):
    """Build the 6-cell embryonic tissue strip shared by S01, S02 and the start of S03."""
    cells = VGroup()
    for idx, cx in enumerate(CELL_XS):
        is_src = idx == 0 and highlight_source
        col = HH_GOLD if is_src else CELL_LINE
        fop = 0.28 if is_src else 0.18
        body = RoundedRectangle(
            corner_radius=0.22, width=CELL_W, height=CELL_H,
            stroke_color=col, stroke_width=3.2, fill_color=col, fill_opacity=fop,
        ).move_to([cx, CELL_Y, 0])
        nuc = Ellipse(
            width=0.78, height=0.50,
            stroke_color=col, stroke_width=2.2, fill_color=NUC_FILL, fill_opacity=0.90,
        ).move_to([cx, CELL_Y - 0.42, 0])
        cells.add(VGroup(body, nuc))
    return cells


def build_hedgehog_ligand(radius=0.22, with_tails=False):
    """Schematic Hedgehog sphere (optionally carrying two simple lipid tail strokes)."""
    core = Circle(
        radius=radius, stroke_color=HH_GOLD, stroke_width=3.0,
        fill_color=HH_GOLD, fill_opacity=0.94,
    )
    if not with_tails:
        return VGroup(core)
    t1 = CubicBezier(
        core.get_bottom() + LEFT * 0.06,
        core.get_bottom() + DOWN * 0.22 + LEFT * 0.14,
        core.get_bottom() + DOWN * 0.40 + RIGHT * 0.04,
        core.get_bottom() + DOWN * 0.54 + LEFT * 0.04,
        color=STEROL_AMB, stroke_width=3.8,
    )
    t2 = CubicBezier(
        core.get_bottom() + RIGHT * 0.08,
        core.get_bottom() + DOWN * 0.19 + RIGHT * 0.16,
        core.get_bottom() + DOWN * 0.36 + RIGHT * 0.02,
        core.get_bottom() + DOWN * 0.49 + RIGHT * 0.12,
        color=STEROL_AMB, stroke_width=3.8,
    )
    return VGroup(t1, t2, core)


def build_patched_protein(center, active=True, transporter=False, scale=1.0):
    """Coral-red Patched transmembrane block with a top binding groove."""
    col = PTCH_CORAL if active else PTCH_DIM
    fop = 0.38 if active else 0.24
    w, h = 1.28 * scale, 1.32 * scale
    if not transporter:
        body = RoundedRectangle(
            corner_radius=0.16 * scale, width=w, height=h,
            stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=fop,
        ).move_to(center)
        groove = Arc(
            radius=0.26 * scale, start_angle=PI, angle=PI,
            arc_center=body.get_top() + DOWN * 0.05 * scale,
            stroke_color=col, stroke_width=3.5,
        )
        return VGroup(body, groove)
    left_lobe = RoundedRectangle(
        corner_radius=0.14 * scale, width=0.54 * scale, height=h,
        stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=fop,
    ).move_to(center + LEFT * 0.38 * scale)
    right_lobe = RoundedRectangle(
        corner_radius=0.14 * scale, width=0.54 * scale, height=h,
        stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=fop,
    ).move_to(center + RIGHT * 0.38 * scale)
    top_notch = Arc(
        radius=0.24 * scale, start_angle=PI, angle=PI,
        arc_center=center + UP * (h / 2 - 0.04 * scale),
        stroke_color=col, stroke_width=3.0,
    )
    return VGroup(left_lobe, right_lobe, top_notch)


def build_smoothened_protein(center, on=False, scale=1.0):
    """Teal Smoothened seven-pass transducer block (dim when OFF, vivid when ON)."""
    col = SMO_TEAL if on else SMO_DIM
    fop = 0.48 if on else 0.25
    sw = 4.0 if on else 2.8
    body = RoundedRectangle(
        corner_radius=0.15 * scale, width=0.88 * scale, height=1.18 * scale,
        stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fop,
    ).move_to(center)
    crown = RoundedRectangle(
        corner_radius=0.10 * scale, width=0.62 * scale, height=0.34 * scale,
        stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fop * 0.85,
    ).next_to(body, UP, buff=-0.04 * scale)
    return VGroup(body, crown)


def build_segmented_membrane(y_mid, gaps, x_left=-6.2, x_right=6.2, thickness=0.40):
    """Double-line bilayer broken cleanly around transmembrane protein x-intervals."""
    segs = VGroup()
    sorted_gaps = sorted(gaps)
    cur = x_left
    spans = []
    for g0, g1 in sorted_gaps:
        if g0 > cur + 0.05:
            spans.append((cur, g0))
        cur = max(cur, g1)
    if x_right > cur + 0.05:
        spans.append((cur, x_right))
    dy = thickness / 2.0
    for a, b in spans:
        fill = Rectangle(
            width=b - a, height=thickness, stroke_width=0,
            fill_color=CELL_LINE, fill_opacity=0.34,
        ).move_to([(a + b) / 2.0, y_mid, 0])
        top_ln = Line([a, y_mid + dy, 0], [b, y_mid + dy, 0], color=CELL_LINE, stroke_width=3.0)
        bot_ln = Line([a, y_mid - dy, 0], [b, y_mid - dy, 0], color=CELL_LINE, stroke_width=3.0)
        segs.add(fill, top_ln, bot_ln)
    return segs


def build_nucleus_dome(y_bottom=-3.45, height=1.75, width=10.8, center_x=0.0):
    """Large schematic nucleus dome along the bottom of the receiving cell."""
    dome = Arc(
        radius=width / 2.0, start_angle=0, angle=PI,
        arc_center=[center_x, y_bottom, 0],
        stroke_color=CELL_LINE, stroke_width=3.2,
        fill_color=NUC_FILL, fill_opacity=0.88,
    )
    dome.stretch(height / (width / 2.0), dim=1, about_point=[center_x, y_bottom, 0])
    base = Line(
        [center_x - width / 2.0, y_bottom, 0],
        [center_x + width / 2.0, y_bottom, 0],
        color=CELL_LINE, stroke_width=2.2,
    )
    return VGroup(dome, base)


def build_gli_bar(center, full=True, scale=1.0):
    """Two-part Gli transcription factor: violet DNA-binding front + lavender activator back."""
    front = RoundedRectangle(
        corner_radius=0.12 * scale, width=1.65 * scale, height=0.56 * scale,
        stroke_color=GLI_VIOLET, stroke_width=3.2,
        fill_color=GLI_VIOLET, fill_opacity=0.42,
    )
    if not full:
        front.move_to(center)
        return VGroup(front)
    back = RoundedRectangle(
        corner_radius=0.12 * scale, width=1.72 * scale, height=0.56 * scale,
        stroke_color=GLI_LAV, stroke_width=3.2,
        fill_color=GLI_LAV, fill_opacity=0.34,
    ).next_to(front, RIGHT, buff=0.06 * scale)
    g = VGroup(front, back).move_to(center)
    return g


def build_inhib_arrow(start_x, end_x, y, color=TEXT):
    """Crisp vector -| inhibition symbol between logic terms."""
    stem = Line([start_x, y, 0], [end_x, y, 0], color=color, stroke_width=3.5)
    bar = Line([end_x, y - 0.16, 0], [end_x, y + 0.16, 0], color=color, stroke_width=4.0)
    return VGroup(stem, bar)


def build_receiving_cell_shell(ptch_active=True, smo_on=False, n_smo=3, transporter=False, y_mem=1.55, y_nuc=-3.42):
    """Build receiving cell cross-section: segmented membrane, Patched, Smoothened(s), nucleus dome."""
    ptch_x = -2.8
    smo_xs = [1.8] if n_smo == 1 else [0.8, 2.55, 4.3]
    gaps = [(ptch_x - 0.66, ptch_x + 0.66)] + [(sx - 0.46, sx + 0.46) for sx in smo_xs]
    membrane = build_segmented_membrane(y_mem, gaps, x_left=-6.1, x_right=6.1, thickness=0.40)
    ptch = build_patched_protein(np.array([ptch_x, y_mem, 0]), active=ptch_active, transporter=transporter)
    smos = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=smo_on) for sx in smo_xs])
    nuc = build_nucleus_dome(y_bottom=y_nuc, height=1.65, width=10.8)
    return membrane, ptch, smos, nuc


# ------------------------------------------------------------------ S00 Title
class S00Title(TitleCard):
    LESSON = "Hedgehog and the Primary Cilium"
    TITLE = "Hedgehog Releases a Brake"


# ------------------------------------------------------------------ S01 Hook
class S01Hook(SpokenScene):
    def construct(self):
        cells = build_cell_row(highlight_source=True)
        src_lbl = T("Source", 26, HH_GOLD).next_to(cells[0], DOWN, buff=0.22)
        recv_lbl = T("Receiving embryonic cells", 26, TEXT).move_to([1.9, src_lbl.get_y(), 0])
        banner = T("One signal -> different cell fates?", 32, TEXT).move_to([0, 3.18, 0])

        rng = np.random.default_rng(7)
        stream = VGroup()
        for k in range(15):
            d = Dot(radius=0.11, color=HH_GOLD).set_opacity(0.92)
            d._u = k / 15.0
            d._y_off = float(rng.uniform(-0.14, 0.14))
            d.move_to([-4.75 + d._u * 10.2, -0.22 + d._y_off, 0])
            stream.add(d)

        def update_stream(mob, dt):
            for d in mob:
                d._u = (d._u + dt * 0.22) % 1.0
                x = -4.75 + d._u * 10.2
                op = float(np.clip(1.0 - 0.65 * d._u, 0.28, 0.95))
                d.move_to([x, -0.22 + d._y_off, 0]).set_opacity(op)

        self.at("How can one")
        self.play(FadeIn(cells), FadeIn(src_lbl), FadeIn(recv_lbl), FadeIn(banner), run_time=0.8)
        stream.add_updater(update_stream)
        self.add(stream)

        self.at("tell embryonic cells")
        self.play(
            cells[1][0].animate.set_fill(SMO_TEAL, opacity=0.38).set_stroke(SMO_TEAL),
            cells[2][0].animate.set_fill(SMO_TEAL, opacity=0.28).set_stroke(SMO_TEAL),
            run_time=1.3,
        )

        self.at("switching off a break")
        q2 = T("Why switch off a brake?", 32, HH_GOLD).move_to([0, 3.18, 0])
        self.play(swap(banner, q2, run_time=0.45), run_time=0.5)

        # Two schematic switches cleanly below y = 2.52 headings
        l_head = T("Most pathways", 26, GREY).move_to([-3.2, 2.52, 0])
        l_track = RoundedRectangle(
            corner_radius=0.14, width=3.8, height=0.92,
            stroke_color=CELL_LINE, stroke_width=2.8, fill_color=NUC_FILL, fill_opacity=0.85,
        ).move_to([-3.2, 0.86, 0])
        l_state = T("OFF", 28, GREY).move_to([-1.95, 0.86, 0])
        l_btn = boxed_label("Active signal", GENE_GREEN, size=24, pad=0.12).move_to([-3.95, 1.82, 0])

        r_head = T("Hedgehog", 26, HH_GOLD).move_to([3.2, 2.52, 0])
        r_track = RoundedRectangle(
            corner_radius=0.14, width=3.8, height=0.92,
            stroke_color=CELL_LINE, stroke_width=2.8, fill_color=NUC_FILL, fill_opacity=0.85,
        ).move_to([3.2, 0.86, 0])
        r_state = T("OFF", 28, PTCH_CORAL).move_to([4.45, 0.86, 0])
        r_brake = boxed_label("Brake", PTCH_CORAL, size=24, pad=0.14).move_to([2.85, 0.86, 0])
        r_brake.label.set_color(TEXT)
        hh_trigger = build_hedgehog_ligand(radius=0.20).move_to([1.65, 0.86, 0])

        self.at("add an active signal")
        l_on = T("ON", 28, GENE_GREEN).move_to(l_state.get_center())
        self.play(FadeIn(l_head), FadeIn(l_track), FadeIn(l_state), FadeIn(l_btn), run_time=0.5)
        self.play(l_btn.animate.move_to([-3.85, 0.86, 0]), run_time=0.65)
        self.play(swap(l_state, l_on, run_time=0.35), run_time=0.4)
        self.play(FadeIn(r_head), FadeIn(r_track), FadeIn(r_state), FadeIn(r_brake), FadeIn(hh_trigger), run_time=0.45)

        self.at("Hedgehog instead removes")
        r_on = T("ON", 28, SMO_TEAL).move_to(r_state.get_center())
        self.play(
            hh_trigger.animate.move_to([2.45, 0.86, 0]),
            r_brake.animate.move_to([3.15, 1.82, 0]),
            run_time=0.55,
        )
        self.play(swap(r_state, r_on, run_time=0.25), run_time=0.25)
        self.finish()


# ------------------------------------------------------------------ S02 Morphogen
class S02Morphogen(SpokenScene):
    def construct(self):
        cells = build_cell_row(highlight_source=True)
        src_lbl = T("Source", 26, HH_GOLD).next_to(cells[0], DOWN, buff=0.22)

        grad_fn = lambda x: np.exp(-0.55 * x)
        P = Plot(
            box=(-4.8, 4.8, 0.32, 2.22), xr=(0, 5), yr=(0, 1.05),
            xticks=[(0.45, "near"), (4.75, "far")],
            yticks=[(0.14, "low"), (1.0, "high")],
            ylabel="Hedgehog dose", color=GREY, size=24, label_size=26,
        )
        grad_lbl = T("schematic gradient", 24, HH_GOLD).move_to([3.4, 1.75, 0])

        time_t = ValueTracker(0.0)
        bar_bg = RoundedRectangle(
            corner_radius=0.08, width=2.8, height=0.28,
            stroke_color=GREY, stroke_width=2.0, fill_color=NUC_FILL, fill_opacity=0.85,
        ).move_to([4.1, 3.12, 0])
        bar_lbl = T("Duration", 24, TEXT).next_to(bar_bg, LEFT, buff=0.22)
        bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.04, 2.72 * time_t.get_value()), height=0.20,
            stroke_width=0, fill_color=HH_GOLD, fill_opacity=0.92,
        ).align_to(bar_bg.get_left() + RIGHT * 0.04, LEFT).set_y(bar_bg.get_y()))

        x_front = ValueTracker(0.0)
        live_curve = P.live_curve(grad_fn, x_front, color=HH_GOLD, width=5.5)

        rng = np.random.default_rng(7)
        p_rng = np.random.default_rng(702)
        particles = VGroup()
        for k in range(36):
            u = rng.random()
            px = float(-np.log(1.0 - u * (1.0 - np.exp(-0.55 * 5.0))) / 0.55)
            py = float(rng.uniform(-0.42, -0.14))
            d = Dot(radius=0.11, color=HH_GOLD).set_opacity(float(np.clip(1.05 - 0.16 * px, 0.25, 0.95)))
            d._x_home = px
            d._y_home = py
            d._phase = float(rng.uniform(0, TAU))
            d.move_to([-4.75 + px * 1.9, d._y_home, 0])
            particles.add(d)

        def update_particles(mob, dt):
            front = x_front.get_value()
            step = dt * 0.85
            p_respawn = 1.0 - np.exp(-0.55 * step)
            for d in mob:
                d._phase += dt * 2.2
                d._x_home += step
                if d._x_home > 5.0 or p_rng.random() < p_respawn:
                    d._x_home = float(p_rng.uniform(0.0, 0.22))
                visible = d._x_home <= front + 0.05
                x_scene = -4.75 + d._x_home * 1.9
                y_scene = d._y_home + 0.05 * np.sin(d._phase)
                base_op = float(np.clip(np.exp(-0.32 * d._x_home), 0.22, 0.95))
                d.move_to([x_scene, y_scene, 0]).set_opacity(base_op if visible else 0.0)

        self.at("Start across this row")
        self.play(FadeIn(cells), FadeIn(src_lbl), FadeIn(P), FadeIn(bar_lbl), FadeIn(bar_bg), run_time=0.8)
        self.add(bar_fill, live_curve)
        particles.add_updater(update_particles)
        self.add(particles)
        self.play(x_front.animate.set_value(1.2), time_t.animate.set_value(0.14), run_time=2.5, rate_func=linear)

        self.at("releases Hedgehog")
        self.play(x_front.animate.set_value(3.0), time_t.animate.set_value(0.32), run_time=2.4, rate_func=linear)

        self.at("fades with distance")
        self.play(
            x_front.animate.set_value(5.0),
            time_t.animate.set_value(0.50),
            FadeIn(grad_lbl),
            run_time=2.2, rate_func=linear,
        )

        self.at("Near cells see")
        self.play(
            time_t.animate.set_value(0.72),
            cells[1][0].animate.set_fill("#5EEAD4", opacity=0.54).set_stroke("#5EEAD4"),
            cells[2][0].animate.set_fill(SMO_TEAL, opacity=0.42).set_stroke(SMO_TEAL),
            run_time=1.8, rate_func=linear,
        )

        self.at("while distant cells")
        self.play(
            time_t.animate.set_value(0.88),
            cells[3][0].animate.set_fill("#2E6F7E", opacity=0.30).set_stroke("#2E6F7E"),
            cells[4][0].animate.set_fill(CELL_LINE, opacity=0.18).set_stroke(CELL_LINE),
            cells[5][0].animate.set_fill(CELL_LINE, opacity=0.16).set_stroke(CELL_LINE),
            run_time=2.5, rate_func=linear,
        )

        self.at("converts that reading")
        f1 = T("Fate A", 24, "#5EEAD4").next_to(cells[1], DOWN, buff=0.22)
        f2 = T("Fate B", 24, SMO_TEAL).next_to(cells[3], DOWN, buff=0.22)
        f3 = T("Fate C", 24, GREY).next_to(cells[5], DOWN, buff=0.22)
        self.play(FadeIn(f1), FadeIn(f2), FadeIn(f3), time_t.animate.set_value(0.96), run_time=3.2, rate_func=linear)

        self.at("Because concentration")
        morph_lbl = T("Morphogen: dose + duration", 30, HH_GOLD).move_to([-2.75, 3.12, 0])
        self.play(FadeIn(morph_lbl), time_t.animate.set_value(1.0), run_time=0.5, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ S03 Off Switch
class S03OffSwitch(SpokenScene):
    def construct(self):
        cells = build_cell_row(highlight_source=True)
        self.add(cells)

        self.at("Now zoom into")
        target_cell = cells[2]
        others = VGroup(cells[0], cells[1], cells[3], cells[4], cells[5])
        membrane, ptch, smos1, nuc = build_receiving_cell_shell(ptch_active=True, smo_on=False, n_smo=1, y_mem=1.55)
        mem_lbl = T("Plasma\nmembrane", 24, GREY, line_spacing=0.85).move_to([-5.05, 0.92, 0])
        nuc_lbl = T("Nucleus", 26, GREY).move_to([0, -2.75, 0])

        # Smooth zoom into cell #3 without any empty frame
        self.play(
            FadeOut(others, run_time=0.8),
            target_cell.animate.scale(3.6).move_to([0, -0.35, 0]).set_opacity(0.18),
            run_time=1.0,
        )
        self.play(
            FadeOut(target_cell, run_time=0.5),
            FadeIn(membrane, run_time=0.7),
            FadeIn(nuc, run_time=0.7),
            FadeIn(mem_lbl, run_time=0.7),
            FadeIn(nuc_lbl, run_time=0.7),
            run_time=0.75,
        )

        self.at("Two membrane proteins")
        ptch_lbl = T("Patched", 28, PTCH_CORAL).move_to([-2.8, 2.82, 0])
        smo_lbl1 = T("Smoothened (OFF)", 28, SMO_TEAL).move_to([1.8, 2.82, 0])
        self.play(FadeIn(ptch), FadeIn(smos1), run_time=0.7)

        self.at("patched and smoothened")
        self.play(FadeIn(ptch_lbl), FadeIn(smo_lbl1), run_time=0.6)

        self.at("Without hedgehog")
        no_hh = T("No Hedgehog", 28, GREY).move_to([-4.8, 3.25, 0])
        self.play(FadeIn(no_hh), run_time=0.45)

        # Downward-rightward stroke-only arcs from Patched (never filled wedges)
        self.at("stays active")
        wave_t = ValueTracker(0.0)
        waves = VGroup()
        for k in range(4):
            arc = always_redraw(lambda k=k: Arc(
                radius=0.68 + ((wave_t.get_value() + k / 4.0) % 1.0) * 1.30,
                start_angle=-PI * 0.58, angle=PI * 0.72,
                arc_center=ptch.get_center(),
                stroke_color=PTCH_CORAL, stroke_width=5.5, fill_opacity=0,
            ).set_stroke(opacity=0.92 * (1.0 - ((wave_t.get_value() + k / 4.0) % 1.0))))
            waves.add(arc)

        def advance_wave(mob, dt):
            wave_t.increment_value(dt * 0.80)

        waves.add_updater(advance_wave)
        self.add(waves)

        self.at("holds smoothened off")
        off_badge = boxed_label("OFF", SMO_DIM_TEXT, size=24, pad=0.12).move_to([1.8, 0.45, 0])
        self.play(FadeIn(off_badge), run_time=0.5)

        self.at("never touches smoothened")
        gap_line = DashedLine([-1.65, 0.45, 0], [0.95, 0.45, 0], color=TEXT, stroke_width=2.8, dash_length=0.14)
        gap_lbl = T("never touches", 24, TEXT).next_to(gap_line, DOWN, buff=0.18)
        self.play(Create(gap_line), FadeIn(gap_lbl), run_time=0.7)

        self.at("keep many smoothened")
        membrane3, _, smos3, _ = build_receiving_cell_shell(ptch_active=True, smo_on=False, n_smo=3, y_mem=1.55)
        smo_lbl3 = T("Smoothened (OFF)", 28, SMO_TEAL).move_to([2.55, 2.82, 0])
        off_badges = VGroup(*[
            boxed_label("OFF", SMO_DIM_TEXT, size=22, pad=0.10).move_to([sx, 0.45, 0])
            for sx in (0.8, 2.55, 4.3)
        ])
        gap_line3 = DashedLine([-1.65, 0.45, 0], [0.15, 0.45, 0], color=TEXT, stroke_width=2.8, dash_length=0.12)
        gap_lbl3 = T("no contact", 24, TEXT).next_to(gap_line3, DOWN, buff=0.18)
        many_note = T("1 Patched keeps many Smoothened quiet", 28, TEXT).move_to([0, -0.95, 0])

        self.play(
            FadeOut(membrane), FadeOut(smos1), FadeOut(off_badge),
            FadeOut(gap_line), FadeOut(gap_lbl), FadeOut(smo_lbl1),
            run_time=0.4,
        )
        self.play(
            FadeIn(membrane3), FadeIn(smos3), FadeIn(smo_lbl3),
            FadeIn(off_badges), Create(gap_line3), FadeIn(gap_lbl3), FadeIn(many_note),
            run_time=0.8,
        )
        self.finish()


# ------------------------------------------------------------------ S04 Sterol Model
class S04SterolModel(SpokenScene):
    def construct(self):
        membrane, ptch, smos, nuc = build_receiving_cell_shell(
            ptch_active=True, smo_on=False, n_smo=3, transporter=False, y_mem=1.55,
        )
        ptch_lbl = T("Patched", 28, PTCH_CORAL).move_to([-2.8, 2.82, 0])
        smo_lbl = T("Smoothened (OFF)", 28, SMO_TEAL).move_to([2.55, 2.82, 0])
        nuc_lbl = T("Nucleus", 26, GREY).move_to([0, -2.75, 0])
        self.add(membrane, ptch, smos, nuc, ptch_lbl, smo_lbl, nuc_lbl)

        self.at("without grabbing")
        q_top = T("How does Patched act without touching?", 28, TEXT).move_to([0, 3.48, 0])
        self.play(FadeIn(q_top), run_time=0.6)

        self.at("resembles a membrane transporter")
        ptch_trans = build_patched_protein(np.array([-2.8, 1.55, 0]), active=True, transporter=True)
        self.play(Transform(ptch, ptch_trans), run_time=0.7)

        rng = np.random.default_rng(7)
        sterols = VGroup()
        for k in range(18):
            st = Ellipse(
                width=0.22, height=0.13,
                stroke_color=STEROL_AMB, stroke_width=2.0,
                fill_color=STEROL_AMB, fill_opacity=0.90,
            )
            st._x = float(rng.uniform(-5.7, -3.6)) if k < 14 else float(rng.uniform(-1.8, -0.4))
            st._y = float(rng.uniform(1.42, 1.68))
            st._vx = float(rng.uniform(-0.85, -0.40))
            st.move_to([st._x, st._y, 0])
            sterols.add(st)

        sweep_on = ValueTracker(0.0)

        def update_sterols(mob, dt):
            pumping = sweep_on.get_value() > 0.5
            for s in mob:
                if pumping:
                    if -2.2 < s._x < 0.0:
                        s._x -= dt * 1.65
                    else:
                        s._x += s._vx * dt * 0.48
                    if s._x < -5.8:
                        s._x = -0.35
                else:
                    s._x += float(np.sin(s._y * 15.0 + s._x)) * dt * 0.24
                s.move_to([s._x, s._y, 0])

        self.at("In the leading model")
        tag = T("Proposed sterol model (schematic)", 26, GREY).move_to([-3.65, 3.30, 0])
        sterol_lbl = T("sterol?\n(schematic)", 24, STEROL_AMB, line_spacing=0.85).move_to([-4.95, 2.25, 0])
        self.play(swap(q_top, tag, run_time=0.4), FadeIn(sterol_lbl), FadeIn(sterols), run_time=0.75)
        sterols.add_updater(update_sterols)

        self.at("likely cholesterol")
        chol_note = T("likely\ncholesterol", 24, STEROL_AMB, line_spacing=0.85).move_to([-4.95, 0.78, 0])
        self.play(FadeIn(chol_note), run_time=0.5)

        self.at("Active patched keeps")
        sweep_on.set_value(1.0)
        halo = DashedVMobject(
            RoundedRectangle(
                corner_radius=0.35, width=5.15, height=1.94,
                stroke_color=GREY, stroke_width=2.5,
            ).move_to([2.55, 1.57, 0]),
            num_dashes=38,
        )
        halo_lbl = T("sterol-poor zone around Smoothened", 26, GREY).move_to([2.55, 0.25, 0])
        sweep_arr = Arrow([-1.5, 0.68, 0], [-3.8, 0.68, 0], color=PTCH_CORAL, stroke_width=4.2, buff=0.05)
        self.play(Create(halo), FadeIn(halo_lbl), GrowArrow(sweep_arr), run_time=0.8)

        self.at("What patched actually moves")
        q_cargo = boxed_label("?  What it moves", HH_GOLD, size=24, pad=0.14).move_to([-2.9, -0.35, 0])
        self.play(FadeIn(q_cargo), run_time=0.6)

        self.at("what powers it")
        q_power = boxed_label("?  What powers it", HH_GOLD, size=24, pad=0.14).move_to([-2.9, -1.05, 0])
        self.play(FadeIn(q_power), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S05 Double Negative
class S05DoubleNegative(SpokenScene):
    def construct(self):
        membrane, ptch, smos, nuc = build_receiving_cell_shell(
            ptch_active=True, smo_on=False, n_smo=3, transporter=True, y_mem=1.55,
        )
        # Put Patched label below membrane so Hedgehog docks cleanly on top
        ptch_lbl = T("Patched (ON)", 28, PTCH_CORAL).move_to([-2.8, 0.48, 0])
        smo_lbl = T("Smoothened (OFF)", 28, SMO_DIM_TEXT).move_to([2.55, 2.74, 0])
        nuc_lbl = T("Nucleus", 26, GREY).move_to([0, -2.75, 0])
        self.add(membrane, ptch, smos, nuc, ptch_lbl, smo_lbl, nuc_lbl)

        rng = np.random.default_rng(7)
        sterols = VGroup()
        for k in range(20):
            st = Ellipse(
                width=0.22, height=0.13,
                stroke_color=STEROL_AMB, stroke_width=2.0,
                fill_color=STEROL_AMB, fill_opacity=0.90,
            )
            st._x = float(rng.uniform(-5.7, -3.5))
            st._y = float(rng.uniform(1.42, 1.68))
            st._vx = float(rng.uniform(0.80, 1.35))
            st.move_to([st._x, st._y, 0])
            sterols.add(st)

        gate = ValueTracker(0.0)

        def update_sterols(mob, dt):
            on = gate.get_value() > 0.5
            for s in mob:
                if not on:
                    s._x -= dt * 0.95
                    if s._x < -5.8:
                        s._x = -3.4
                else:
                    s._x += s._vx * dt * 2.4
                    if s._x > 5.4:
                        s._x = -1.6
                s.move_to([s._x, s._y, 0])

        sterols.add_updater(update_sterols)
        self.add(sterols)

        hh = build_hedgehog_ligand(radius=0.24, with_tails=True).move_to([-2.8, 3.25, 0])
        hh_lbl = T("Hedgehog", 26, HH_GOLD).move_to([-4.65, 2.58, 0])
        tails_lbl = T("Lipid tails", 24, STEROL_AMB).move_to([-1.15, 2.25, 0])
        tails_arr = Arrow(
            tails_lbl.get_left() + LEFT * 0.08,
            np.array([-2.52, 2.25, 0]),
            color=STEROL_AMB, stroke_width=3.2, buff=0.04, max_tip_length_to_length_ratio=0.25,
        )

        self.at("Now Hedgehog arrives")
        self.play(FadeIn(hh), FadeIn(hh_lbl), run_time=0.45)
        self.play(
            hh.animate.move_to([-2.8, 2.58, 0]),
            run_time=0.95,
        )

        self.at("carries lipid tails")
        self.play(FadeIn(tails_lbl), GrowArrow(tails_arr), run_time=0.45)

        self.at("one plugs into")
        self.play(hh.animate.move_to([-2.8, 2.16, 0]), run_time=0.6)

        self.at("switching the brake off")
        gate.set_value(1.0)
        ptch_off = build_patched_protein(np.array([-2.8, 1.55, 0]), active=False, transporter=True)
        ptch_lbl_off = T("Patched (OFF)", 28, PTCH_DIM_TEXT).move_to(ptch_lbl.get_center())
        self.play(
            FadeOut(tails_lbl), FadeOut(tails_arr),
            Transform(ptch, ptch_off),
            swap(ptch_lbl, ptch_lbl_off, run_time=0.45),
            run_time=0.65,
        )

        self.at("now reaches smoothened")
        self.wait(1.0)

        self.at("lights up and turns on")
        smos_on = VGroup(*[build_smoothened_protein(np.array([sx, 1.55, 0]), on=True) for sx in (0.8, 2.55, 4.3)])
        smo_lbl_on = T("Smoothened (ON)", 28, SMO_TEAL).move_to(smo_lbl.get_center())
        self.play(
            Transform(smos, smos_on),
            swap(smo_lbl, smo_lbl_on, run_time=0.45),
            run_time=0.7,
        )

        self.at("never pressed an accelerator")
        no_accel = T("No direct accelerator — brake removed", 26, GREY).move_to([0.9, -0.35, 0])
        self.play(FadeIn(no_accel), run_time=0.6)

        self.at("switched off an off switch")
        t_hh = T("Hedgehog", 26, HH_GOLD).move_to([-5.00, 3.28, 0])
        inh1 = build_inhib_arrow(-4.05, -3.30, 3.28, color=HH_GOLD)
        t_pt = T("Patched", 26, PTCH_CORAL).move_to([-2.45, 3.28, 0])
        inh2 = build_inhib_arrow(-1.60, -0.85, 3.28, color=PTCH_CORAL)
        t_sm = T("Smoothened", 26, SMO_TEAL).move_to([0.55, 3.28, 0])
        self.play(FadeIn(t_hh), FadeIn(inh1), FadeIn(t_pt), FadeIn(inh2), FadeIn(t_sm), run_time=0.8)

        self.at("a double negative")
        dn_badge = boxed_label("Double negative = ON", SMO_TEAL, size=24, pad=0.14).move_to([4.35, 3.28, 0])
        self.play(FadeIn(dn_badge), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ S06 Gli Off
class S06GliOff(SpokenScene):
    def construct(self):
        y_mem = 2.15
        s06_scale = 0.80
        gaps = [(-2.8 - 0.66 * s06_scale, -2.8 + 0.66 * s06_scale)] + [
            (sx - 0.46 * s06_scale, sx + 0.46 * s06_scale) for sx in (0.8, 2.55, 4.3)
        ]
        membrane = build_segmented_membrane(y_mem, gaps, x_left=-6.1, x_right=6.1, thickness=0.32)
        ptch = build_patched_protein(np.array([-2.8, y_mem, 0]), active=True, transporter=True, scale=s06_scale)
        smos = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=False, scale=s06_scale) for sx in (0.8, 2.55, 4.3)])
        ptch_lbl = T("Patched (ON)", 24, PTCH_CORAL).move_to([-2.8, 3.16, 0])
        smo_lbl = T("Smoothened (OFF)", 24, SMO_DIM_TEXT).move_to([2.55, 3.16, 0])

        # Active Patched sweeps sterols leftward in top membrane so scene stays alive continuously
        rng = np.random.default_rng(7)
        sterols = VGroup()
        for _ in range(16):
            st = Ellipse(width=0.26, height=0.15, stroke_color=STEROL_AMB, stroke_width=2.0, fill_color=STEROL_AMB, fill_opacity=0.92)
            st._x = float(rng.uniform(-5.7, -3.5))
            st._y = float(rng.uniform(y_mem - 0.08, y_mem + 0.08))
            st.move_to([st._x, st._y, 0])
            sterols.add(st)

        def sweep_left(mob, dt):
            for s in mob:
                s._x -= dt * 1.35
                if s._x < -5.8:
                    s._x = -3.45
                s.move_to([s._x, s._y, 0])

        sterols.add_updater(sweep_left)

        nuc = build_nucleus_dome(y_bottom=-3.45, height=1.72, width=10.8)
        gene_bar = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=0.28,
            stroke_color=CELL_LINE, stroke_width=2.5, fill_color=CELL_LINE, fill_opacity=0.38,
        ).move_to([0, -2.62, 0])
        gene_lbl = T("Target genes", 24, TEXT).move_to([0, -3.08, 0])

        self.at("What does smoothen control")
        self.play(
            FadeIn(membrane), FadeIn(ptch), FadeIn(smos), FadeIn(ptch_lbl), FadeIn(smo_lbl),
            FadeIn(sterols), FadeIn(nuc), FadeIn(gene_bar), FadeIn(gene_lbl),
            run_time=0.8,
        )

        self.at("Follow the transcription factor")
        gli = build_gli_bar(np.array([-3.6, 0.05, 0]), full=True, scale=1.0)
        gli_lbl = T("Gli", 28, GLI_LAV).next_to(gli, UP, buff=0.20)
        dna_tag = T("DNA-binding", 22, GLI_VIOLET).next_to(gli[0], DOWN, buff=0.22)
        act_tag = T("activator", 22, GLI_LAV).next_to(gli[1], DOWN, buff=0.22)
        self.play(FadeIn(gli), FadeIn(gli_lbl), FadeIn(dna_tag), FadeIn(act_tag), run_time=0.9)

        self.at("While smoothened is off")
        kinases = boxed_label("Kinases", KINASE_BLUE, size=26, pad=0.18).move_to([-1.0, 1.45, 0])
        self.play(FadeIn(kinases), run_time=0.5)

        self.at("kinases add phosphates")
        phos = VGroup()
        for dx in (-0.45, 0.15, 0.75):
            p_dot = Circle(radius=0.22, stroke_color=STEROL_AMB, stroke_width=2.0, fill_color=KINASE_BLUE, fill_opacity=0.92)
            p_txt = T("P", 22, TEXT).move_to(p_dot)
            p_badge = VGroup(p_dot, p_txt).move_to([gli.get_center()[0] + dx, gli.get_top()[1] + 0.34, 0])
            phos.add(p_badge)
        self.play(FadeOut(gli_lbl), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in phos], lag_ratio=0.22), run_time=0.9)

        self.at("marking it for the proteasome")
        prot = RoundedRectangle(
            corner_radius=0.24, width=1.68, height=1.28,
            stroke_color=KINASE_BLUE, stroke_width=3.5, fill_color=KINASE_BLUE, fill_opacity=0.28,
        ).move_to([4.0, 0.05, 0])
        prot_lbl = T("Proteasome", 26, KINASE_BLUE).next_to(prot, UP, buff=0.20)
        self.play(FadeIn(prot), FadeIn(prot_lbl), run_time=0.6)

        self.at("shreds only its back")
        gli_bundle = VGroup(gli, phos, dna_tag, act_tag)
        self.play(gli_bundle.animate.shift(RIGHT * 4.75), run_time=0.8)

        specks = VGroup()
        for _ in range(16):
            sp = Dot(radius=0.065, color=GLI_LAV).set_opacity(0.88)
            sp._op = 0.88
            sp._vx = float(rng.uniform(0.35, 1.10))
            sp._vy = float(rng.uniform(-0.45, 0.55))
            sp.move_to([4.15 + rng.uniform(-0.2, 0.4), 0.05 + rng.uniform(-0.2, 0.2), 0])
            specks.add(sp)

        def shred_specks(mob, dt):
            for s in mob:
                s.shift([s._vx * dt, s._vy * dt, 0])
                s._op = max(0.0, s._op - dt * 0.30)
                s.set_opacity(s._op)

        self.play(
            FadeOut(gli[1], shift=RIGHT * 0.4),
            FadeOut(act_tag),
            FadeOut(phos),
            FadeIn(specks),
            run_time=0.9,
        )
        specks.add_updater(shred_specks)

        self.at("binding piece survives")
        rep_piece = gli[0]
        rep_lbl = T("Gli repressor", 26, GLI_VIOLET).next_to(rep_piece, LEFT, buff=0.24)
        self.play(FadeOut(dna_tag), FadeIn(rep_lbl), run_time=0.5)

        self.at("silences target genes")
        off_lbl = T("Genes OFF", 28, PTCH_CORAL).move_to(gene_lbl.get_center())
        # Place Gli repressor cleanly inside nucleus above gene_bar, with label to its left
        target_rep_pos = np.array([0.85, -2.18, 0])
        target_lbl_pos = np.array([-1.25, -2.18, 0])
        self.play(
            rep_piece.animate.move_to(target_rep_pos),
            rep_lbl.animate.move_to(target_lbl_pos),
            run_time=1.0,
        )
        self.play(
            gene_bar.animate.set_fill(PTCH_CORAL, opacity=0.38).set_stroke(PTCH_CORAL),
            swap(gene_lbl, off_lbl, run_time=0.45),
            run_time=0.6,
        )
        self.finish()


# ------------------------------------------------------------------ S07 Predict + S08 Pause
def build_s07_world():
    """Shared final state of S07Predict and backdrop of S08Pause."""
    y_mem = 2.05
    s07_scale = 0.78
    gaps = [(-2.8 - 0.66 * s07_scale, -2.8 + 0.66 * s07_scale)] + [
        (sx - 0.46 * s07_scale, sx + 0.46 * s07_scale) for sx in (0.8, 2.55, 4.3)
    ]
    membrane = build_segmented_membrane(y_mem, gaps, x_left=-6.1, x_right=6.1, thickness=0.32)
    ptch = build_patched_protein(np.array([-2.8, y_mem, 0]), active=False, transporter=True, scale=s07_scale)
    smos = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=True, scale=s07_scale) for sx in (0.8, 2.55, 4.3)])
    hh = build_hedgehog_ligand(radius=0.20, with_tails=True).move_to([-2.8, 2.52, 0])
    ptch_lbl = T("Patched (OFF)", 24, PTCH_DIM_TEXT).move_to([-4.65, 2.75, 0])
    smo_lbl = T("Smoothened (ON)", 24, SMO_TEAL).move_to([2.55, 3.05, 0])

    box_a = DashedVMobject(
        RoundedRectangle(corner_radius=0.16, width=5.3, height=2.65, stroke_color=GREY, stroke_width=2.5).move_to([-3.2, -0.35, 0]),
        num_dashes=42,
    )
    head_a = T("Path A: Glue back?", 26, TEXT).move_to([-3.2, 0.60, 0])
    cut_front = build_gli_bar(np.array([-4.1, -0.25, 0]), full=False, scale=0.82)
    frag1 = Dot(radius=0.09, color=GLI_LAV).move_to([-2.5, -0.10, 0])
    frag2 = Dot(radius=0.09, color=GLI_LAV).move_to([-2.1, -0.38, 0])
    frag3 = Dot(radius=0.09, color=GLI_LAV).move_to([-2.65, -0.45, 0])
    q_a = T("?", 34, HH_GOLD).move_to([-3.2, -1.12, 0])

    box_b = DashedVMobject(
        RoundedRectangle(corner_radius=0.16, width=5.3, height=2.65, stroke_color=GREY, stroke_width=2.5).move_to([3.2, -0.35, 0]),
        num_dashes=42,
    )
    head_b = T("Path B: Spare new Gli?", 26, TEXT).move_to([3.2, 0.60, 0])
    fresh_gli = build_gli_bar(np.array([3.2, -0.25, 0]), full=True, scale=0.78)
    q_b = T("?", 34, HH_GOLD).move_to([3.2, -1.12, 0])

    return VGroup(
        membrane, ptch, smos, hh, ptch_lbl, smo_lbl,
        box_a, head_a, cut_front, frag1, frag2, frag3, q_a,
        box_b, head_b, fresh_gli, q_b,
    )


class S07Predict(SpokenScene):
    def construct(self):
        y_mem = 2.05
        s07_scale = 0.78
        gaps = [(-2.8 - 0.66 * s07_scale, -2.8 + 0.66 * s07_scale)] + [
            (sx - 0.46 * s07_scale, sx + 0.46 * s07_scale) for sx in (0.8, 2.55, 4.3)
        ]
        membrane = build_segmented_membrane(y_mem, gaps, x_left=-6.1, x_right=6.1, thickness=0.32)
        ptch = build_patched_protein(np.array([-2.8, y_mem, 0]), active=True, transporter=True, scale=s07_scale)
        smos = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=False, scale=s07_scale) for sx in (0.8, 2.55, 4.3)])
        ptch_lbl = T("Patched (ON)", 24, PTCH_CORAL).move_to([-4.65, 2.75, 0])
        smo_lbl = T("Smoothened (OFF)", 24, SMO_DIM_TEXT).move_to([2.55, 3.05, 0])

        rng = np.random.default_rng(7)
        sterols = VGroup()
        for k in range(10):
            st = Ellipse(width=0.18, height=0.10, stroke_color=STEROL_AMB, stroke_width=1.6, fill_color=STEROL_AMB, fill_opacity=0.88)
            st._x = float(rng.uniform(-4.1, -3.35)) if k < 5 else float(rng.uniform(-5.7, -4.1))
            st._y = float(rng.uniform(y_mem - 0.08, y_mem + 0.08))
            st.move_to([st._x, st._y, 0])
            sterols.add(st)
        gate = ValueTracker(0.0)

        def update_sterols(mob, dt):
            on = gate.get_value() > 0.5
            for s in mob:
                if not on:
                    s._x -= dt * 0.45
                    if s._x < -5.8:
                        s._x = -3.35
                else:
                    s._x += dt * 3.1
                    if s._x > 5.4:
                        s._x = -1.6
                s.move_to([s._x, s._y, 0])

        self.at("Now pause and predict")
        self.play(FadeIn(membrane), FadeIn(ptch), FadeIn(smos), FadeIn(ptch_lbl), FadeIn(smo_lbl), FadeIn(sterols), run_time=0.7)
        sterols.add_updater(update_sterols)

        self.at("Hedgehog arrives")
        hh = build_hedgehog_ligand(radius=0.20, with_tails=True).move_to([-2.8, 3.25, 0])
        self.play(FadeIn(hh), run_time=0.3)
        self.play(hh.animate.move_to([-2.8, 2.52, 0]), run_time=0.75)

        self.at("switches off")
        ptch_off = build_patched_protein(np.array([-2.8, y_mem, 0]), active=False, transporter=True, scale=0.78)
        ptch_lbl_off = T("Patched (OFF)", 24, PTCH_DIM_TEXT).move_to(ptch_lbl.get_center())
        gate.set_value(1.0)
        self.play(Transform(ptch, ptch_off), swap(ptch_lbl, ptch_lbl_off, run_time=0.35), run_time=0.5)

        self.at("turns on")
        smos_on = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=True, scale=0.78) for sx in (0.8, 2.55, 4.3)])
        smo_lbl_on = T("Smoothened (ON)", 24, SMO_TEAL).move_to(smo_lbl.get_center())
        self.play(Transform(smos, smos_on), swap(smo_lbl, smo_lbl_on, run_time=0.35), run_time=0.55)

        world = build_s07_world()
        opt_a = VGroup(*world[6:13])
        opt_b = VGroup(*world[13:17])

        self.at("glue cut repressors")
        self.play(FadeIn(opt_a), run_time=0.7)
        self.play(
            world[9].animate.shift(LEFT * 0.25),
            world[10].animate.shift(LEFT * 0.25),
            rate_func=there_and_back, run_time=0.8,
        )

        self.at("or spare newly made")
        q_card = question_card("Glue cut repressors, or spare new Gli?")
        self.play(FadeIn(opt_b), FadeIn(q_card), run_time=0.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Glue cut repressors, or spare new Gli?"
    SECONDS = 4.5

    def backdrop(self):
        return build_s07_world()


# ------------------------------------------------------------------ S09 Reveal
class S09Reveal(SpokenScene):
    def construct(self):
        y_mem = 2.15
        s09_scale = 0.80
        gaps = [(-2.8 - 0.66 * s09_scale, -2.8 + 0.66 * s09_scale)] + [
            (sx - 0.46 * s09_scale, sx + 0.46 * s09_scale) for sx in (0.8, 2.55, 4.3)
        ]
        membrane = build_segmented_membrane(y_mem, gaps, x_left=-6.1, x_right=6.1, thickness=0.32)
        ptch = build_patched_protein(np.array([-2.8, y_mem, 0]), active=False, transporter=True, scale=s09_scale)
        smos = VGroup(*[build_smoothened_protein(np.array([sx, y_mem, 0]), on=True, scale=s09_scale) for sx in (0.8, 2.55, 4.3)])
        hh = build_hedgehog_ligand(radius=0.20, with_tails=True).move_to([-2.8, 2.62, 0])
        ptch_lbl = T("Patched (OFF)", 24, PTCH_DIM_TEXT).move_to([-4.65, 2.85, 0])
        smo_lbl = T("Smoothened (ON)", 24, SMO_TEAL).move_to([2.55, 3.18, 0])

        # Continuous sterol flow through active Smoothened membrane
        rng = np.random.default_rng(7)
        sterols = VGroup()
        for _ in range(18):
            st = Ellipse(width=0.26, height=0.15, stroke_color=STEROL_AMB, stroke_width=2.0, fill_color=STEROL_AMB, fill_opacity=0.92)
            st._x = float(rng.uniform(-1.5, 5.2))
            st._y = float(rng.uniform(y_mem - 0.08, y_mem + 0.08))
            st.move_to([st._x, st._y, 0])
            sterols.add(st)

        def flow_right(mob, dt):
            for s in mob:
                s._x += dt * 1.55
                if s._x > 5.4:
                    s._x = -1.6
                s.move_to([s._x, s._y, 0])

        sterols.add_updater(flow_right)

        box_a = DashedVMobject(
            RoundedRectangle(corner_radius=0.16, width=4.8, height=2.1, stroke_color=GREY, stroke_width=2.5).move_to([-3.4, 0.25, 0]),
            num_dashes=36,
        )
        head_a = T("Glue back?", 24, GREY).move_to([-3.4, 0.90, 0])
        cut_front = build_gli_bar(np.array([-3.4, 0.05, 0]), full=False, scale=0.80)
        opt_a = VGroup(box_a, head_a, cut_front)

        fresh_gli = build_gli_bar(np.array([-3.2, 0.45, 0]), full=True, scale=0.95)
        fresh_lbl = T("New full-length Gli", 26, GLI_LAV).next_to(fresh_gli, UP, buff=0.20)

        nuc = build_nucleus_dome(y_bottom=-3.45, height=1.72, width=10.8)
        gene_bar = RoundedRectangle(
            corner_radius=0.08, width=5.6, height=0.28,
            stroke_color=CELL_LINE, stroke_width=2.5, fill_color=CELL_LINE, fill_opacity=0.38,
        ).move_to([0, -2.62, 0])
        gene_lbl = T("Target genes", 24, TEXT).move_to([0, -3.08, 0])

        kinases = boxed_label("Kinases", KINASE_BLUE, size=24, pad=0.16).move_to([-0.25, 1.00, 0])
        prot = RoundedRectangle(
            corner_radius=0.24, width=1.68, height=1.24,
            stroke_color=KINASE_BLUE, stroke_width=3.0, fill_color=KINASE_BLUE, fill_opacity=0.22,
        ).move_to([3.7, 0.45, 0])
        prot_lbl = T("Proteasome (idle)", 24, GREY).next_to(prot, UP, buff=0.18)

        self.add(membrane, ptch, smos, hh, ptch_lbl, smo_lbl, sterols, opt_a, nuc, gene_bar, gene_lbl)

        self.at("It spares newly made")
        cross1 = Line([-5.2, -0.5, 0], [-1.6, 1.0, 0], color=PTCH_CORAL, stroke_width=4.0)
        cross2 = Line([-5.2, 1.0, 0], [-1.6, -0.5, 0], color=PTCH_CORAL, stroke_width=4.0)
        self.play(Create(cross1), Create(cross2), run_time=0.45)
        self.play(FadeOut(opt_a), FadeOut(cross1), FadeOut(cross2), run_time=0.4)
        self.play(
            FadeIn(fresh_gli), FadeIn(fresh_lbl), FadeIn(kinases), FadeIn(prot), FadeIn(prot_lbl),
            run_time=0.6,
        )

        self.at("turns on")
        inh_x_end = kinases.get_right()[0] + 0.08
        inh_stem = VMobject(color=SMO_TEAL, stroke_width=3.5).set_points_as_corners(
            [[0.80, 1.62, 0], [0.80, 1.00, 0], [inh_x_end, 1.00, 0]]
        )
        inh_bar = Line([inh_x_end, 0.84, 0], [inh_x_end, 1.16, 0], color=SMO_TEAL, stroke_width=4.0)
        inh_k = VGroup(inh_stem, inh_bar)
        self.play(Create(inh_k), run_time=0.45)

        self.at("kinase marking stops")
        self.play(
            kinases.box.animate.shift(DOWN * 0.20 + LEFT * 0.35).set_fill(opacity=0.10).set_stroke(opacity=0.45),
            kinases.label.animate.shift(DOWN * 0.20 + LEFT * 0.35).set_color(GREY).set_opacity(0.72),
            FadeOut(inh_k),
            run_time=0.7,
        )

        self.at("Cut repressors are never")
        never_note = T("Cut repressors are not re-glued", 24, GREY).move_to([-3.4, -0.95, 0])
        self.play(FadeIn(never_note), run_time=0.6)

        self.at("avoids the proteasome")
        gli_grp = VGroup(fresh_gli, fresh_lbl)
        self.play(FadeOut(never_note), gli_grp.animate.shift(DOWN * 0.65), run_time=0.45)
        self.play(gli_grp.animate.move_to([0.2, -0.45, 0]), run_time=1.35, rate_func=linear)

        self.at("keeps its activating half")
        act_keep = T("activating half intact", 24, GLI_LAV).next_to(fresh_gli[1], DOWN, buff=0.22)
        self.play(FadeIn(act_keep), run_time=0.4)
        self.play(VGroup(gli_grp, act_keep).animate.move_to([1.3, -0.75, 0]), run_time=1.2, rate_func=linear)

        self.at("moves into the nucleus")
        self.play(FadeOut(act_keep), FadeOut(fresh_lbl), run_time=0.4)
        self.play(fresh_gli.animate.move_to([0, -2.14, 0]), run_time=1.0)
        whole_lbl = T("Full-length Gli activator", 24, GLI_LAV).move_to([0, -1.42, 0])
        self.play(FadeIn(whole_lbl), run_time=0.45)

        self.at("switches target genes on")
        on_lbl = T("Genes ON", 28, GENE_GREEN).move_to(gene_lbl.get_center())
        tx_t = ValueTracker(0.0)
        tx_pulses = VGroup()
        for k in range(3):
            p = always_redraw(lambda k=k: Arrow(
                [-2.5 + ((tx_t.get_value() + k * 0.33) % 1.0) * 4.2, -2.62, 0],
                [-1.7 + ((tx_t.get_value() + k * 0.33) % 1.0) * 4.2, -2.62, 0],
                color=GENE_GREEN, stroke_width=4.2, buff=0,
            ).set_opacity(0.90))
            tx_pulses.add(p)

        def adv_tx(mob, dt):
            tx_t.increment_value(dt * 0.48)

        self.play(
            gene_bar.animate.set_fill(GENE_GREEN, opacity=0.48).set_stroke(GENE_GREEN),
            swap(gene_lbl, on_lbl, run_time=0.45),
            run_time=0.7,
        )
        tx_pulses.add_updater(adv_tx)
        self.add(tx_pulses)
        self.finish()


# ------------------------------------------------------------------ S10 Synthesis
def build_half_cell(panel_center, has_hh):
    """Build one half-frame cell schematic already sized for TwoPanel (no post-scale of text)."""
    cx, cy = panel_center[0], panel_center[1]
    y_mem = cy + 0.90
    y_nuc = cy - 2.18
    ptch_x = cx - 1.55
    smo_x = cx + 1.25

    gaps = [(ptch_x - 0.52, ptch_x + 0.52), (smo_x - 0.38, smo_x + 0.38)]
    mem = build_segmented_membrane(y_mem, gaps, x_left=cx - 2.75, x_right=cx + 2.75, thickness=0.26)
    ptch = build_patched_protein(np.array([ptch_x, y_mem, 0]), active=not has_hh, transporter=True, scale=0.65)
    smo = build_smoothened_protein(np.array([smo_x, y_mem, 0]), on=has_hh, scale=0.65)

    ptch_lbl = T("Patched ON" if not has_hh else "Patched OFF", 24, PTCH_CORAL if not has_hh else PTCH_DIM_TEXT).move_to([ptch_x, y_mem + 1.24, 0])
    smo_lbl = T("Smoothened OFF" if not has_hh else "Smoothened ON", 24, SMO_DIM_TEXT if not has_hh else SMO_TEAL).move_to([smo_x, y_mem + 1.24, 0])

    nuc = build_nucleus_dome(y_bottom=y_nuc, height=1.65, width=5.3, center_x=cx)
    gene_col = GENE_GREEN if has_hh else PTCH_CORAL
    gene_bar = RoundedRectangle(
        corner_radius=0.06, width=3.5, height=0.20,
        stroke_color=gene_col, stroke_width=2.5, fill_color=gene_col, fill_opacity=0.42,
    ).move_to([cx, y_nuc + 0.48, 0])
    gene_lbl = T("Genes ON" if has_hh else "Genes OFF", 24, gene_col).move_to([cx, y_nuc + 0.18, 0])

    gli = build_gli_bar(np.array([cx, cy - 0.25, 0]), full=has_hh, scale=0.70)
    gli_lbl = T("Intact Gli" if has_hh else "Trimmed Gli", 24, GLI_LAV if has_hh else GLI_VIOLET).next_to(gli, UP, buff=0.14)

    extra = VGroup()
    if has_hh:
        hh = build_hedgehog_ligand(radius=0.16, with_tails=True).move_to([ptch_x, y_mem + 0.36, 0])
        extra.add(hh)

    return {
        "mem": mem, "ptch": ptch, "smo": smo, "ptch_lbl": ptch_lbl, "smo_lbl": smo_lbl,
        "nuc": nuc, "gene_bar": gene_bar, "gene_lbl": gene_lbl,
        "gli": gli, "gli_lbl": gli_lbl, "extra": extra,
        "y_mem": y_mem, "cx": cx, "cy": cy,
    }


class S10Synthesis(SpokenScene):
    def construct(self):
        tp = TwoPanel("No Hedgehog", "+ Hedgehog", colors=(PTCH_CORAL, HH_GOLD), top=3.35, bottom=-2.30)
        self.at("Compare both states")
        self.play(FadeIn(tp), run_time=0.7)

        left = build_half_cell(tp.area("left")[0], has_hh=False)
        right = build_half_cell(tp.area("right")[0], has_hh=True)

        rng = np.random.default_rng(7)
        sterols_l, sterols_r = VGroup(), VGroup()
        for _ in range(6):
            sl = Ellipse(width=0.16, height=0.10, stroke_color=STEROL_AMB, stroke_width=1.5, fill_color=STEROL_AMB, fill_opacity=0.88)
            sl._x = float(rng.uniform(left["cx"] - 2.65, left["cx"] - 2.15))
            sl.move_to([sl._x, left["y_mem"], 0])
            sterols_l.add(sl)

            sr = Ellipse(width=0.16, height=0.10, stroke_color=STEROL_AMB, stroke_width=1.5, fill_color=STEROL_AMB, fill_opacity=0.88)
            sr._x = float(rng.uniform(right["cx"] - 0.85, right["cx"] + 2.4))
            sr.move_to([sr._x, right["y_mem"], 0])
            sterols_r.add(sr)

        def update_both_sterols(mob, dt):
            for s in sterols_l:
                s._x -= dt * 0.55
                if s._x < left["cx"] - 2.68:
                    s._x = left["cx"] - 2.12
                s.move_to([s._x, left["y_mem"], 0])
            for s in sterols_r:
                s._x += dt * 0.65
                if s._x > right["cx"] + 2.55:
                    s._x = right["cx"] - 0.90
                s.move_to([s._x, right["y_mem"], 0])

        self.at("Without hedgehog")
        self.play(
            FadeIn(left["mem"]), FadeIn(left["ptch"]), FadeIn(left["ptch_lbl"]),
            FadeIn(left["nuc"]), FadeIn(sterols_l),
            run_time=0.8,
        )
        sterols_l.add_updater(lambda mob, dt: [
            (setattr(s, "_x", s._x - dt * 0.55 if s._x - dt * 0.55 >= left["cx"] - 2.68 else left["cx"] - 2.12),
             s.move_to([s._x, left["y_mem"], 0]))
            for s in mob
        ])

        self.at("stays off")
        self.play(FadeIn(left["smo"]), FadeIn(left["smo_lbl"]), run_time=0.6)

        self.at("silences genes")
        self.play(
            FadeIn(left["gli"]), FadeIn(left["gli_lbl"]),
            FadeIn(left["gene_bar"]), FadeIn(left["gene_lbl"]),
            run_time=0.8,
        )

        self.at("With hedgehog")
        self.play(
            FadeIn(right["mem"]), FadeIn(right["ptch"]), FadeIn(right["extra"]),
            FadeIn(right["ptch_lbl"]), FadeIn(right["nuc"]), FadeIn(sterols_r),
            run_time=0.8,
        )
        sterols_r.add_updater(lambda mob, dt: [
            (setattr(s, "_x", s._x + dt * 0.65 if s._x + dt * 0.65 <= right["cx"] + 2.55 else right["cx"] - 0.90),
             s.move_to([s._x, right["y_mem"], 0]))
            for s in mob
        ])

        self.at("turns on")
        self.play(FadeIn(right["smo"]), FadeIn(right["smo_lbl"]), run_time=0.6)

        self.at("activates them")
        self.play(
            FadeIn(right["gli"]), FadeIn(right["gli_lbl"]),
            FadeIn(right["gene_bar"]), FadeIn(right["gene_lbl"]),
            run_time=0.8,
        )

        self.at("switches off patched")
        self.play(
            VGroup(left["gli"], left["gli_lbl"]).animate.shift(DOWN * 1.10),
            VGroup(right["gli"], right["gli_lbl"]).animate.shift(DOWN * 1.10),
            run_time=0.70,
        )

        self.at("keep glee whole")
        takeaway = caption(
            "Hedgehog switches off Patched, letting Smoothened keep Gli whole and active.",
            size=28, color=HH_GOLD, y=-3.05,
        )
        takeaway.set_x(0)
        self.play(FadeIn(takeaway), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ S11 End
class S11End(EndCard):
    LINE = "Hedgehog switches off Patched, letting Smoothened keep Gli whole and active."
