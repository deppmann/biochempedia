"""Why the Alarm Needs Brakes — STEMhop Explainer Animation (Chapter 2)

COLOUR MAP (one colour per concept for the entire film):
- EMERALD (#4ADE80): NF-κB, stay-alive survival arm/shield, controlled vaccine adjuvant balance
- PURPLE  (#B388FF): Nucleus and DNA
- AMBER   (#F5B041): Inflammatory alarm / TNF cytokine / endotoxin / Gram-negative bacteria
- CORAL   (#FC6255): Protective negative-feedback brakes / inhibitors (IκBα, A20) and warning halo
- CRIMSON (#E11D48): Cell death arm, septic shock, host injury, and failure extremes
- SKY     (#7DD3FC): Lysine-63 (K63) ubiquitin scaffold chains
- TEAL    (#3FB8C0): IKK complex, TNF receptor 1, immediate receptor checkpoint
- TEXT    (#E8EAF0): Primary labels, titles, neutral outlines
- GREY    (#8B93A1): Plot axes and schematic reference tracks only

ONE PICTURE OF THE WORLD:
We start inside the macrophage cross-section where Film 1 ended (plasma membrane, cytosol,
purple nucleus, glowing purple DNA with emerald NF-κB seated on it). We zoom onto that DNA
to watch fresh coral IκBα emerge and pull NF-κB out, pull back slightly to watch coral A20
snip the sky-blue K63 scaffold upstream as a delayed-feedback curve traces waves, widen to
watch amber TNF bind TNF receptor 1 on the same cell and a neighbor cell (forking into
coral Die vs emerald Stay alive and its split-frame block), then zoom out to a two-panel
mouse comparison and an innate alarm balance beam (too little MyD88/IRAK4 -> coral left;
too much septic shock -> coral right; controlled adjuvant -> emerald center), ending on a
wide schematic of NF-κB on purple DNA driving Defense, Survival, and Brakes.

WHAT CHANGES IN EACH SPOKEN SCENE (and what it is computed from):
- s00_hook:       Macrophage cross-section pulses with computed concentric amber alarm waves
                  expanding from NF-κB on DNA while a coral border halo flickers, then zooms toward DNA.
- s02_brakes:     Computed coral ribbon emerges from DNA, folds into an IκBα clamp, crosses the
                  nuclear boundary, lifts emerald NF-κB off DNA, and pulls it into the cytosol.
- s03_waves:      Coral A20 scissors glide up and snip the K63 bead chain (segments separate), teal
                  IKK dims, and a Plot traces a curve computed from a delayed negative-feedback ODE.
- s04_tnf:        Amber TNF particles travel along computed paths from macrophage to autocrine and
                  paracrine TNF receptor 1; intracellular signal forks into growing coral Die and emerald Stay alive arrows.
- s05_survival:   Teal receptor clamp halts coral death pulses, NF-κB enters the nucleus to raise an
                  emerald shield, then a TwoPanel contrast locks NF-κB behind coral IκB and fragments the cell.
- s06_predict:    TwoPanel schematic shows endotoxin streams hitting both mice (normal collapses into
                  coral shock, TLR4-mutant stays steady), then live bacteria arrive beside the mutant mouse.
- s08_reveal:     Bacteria multiply exponentially (5 -> 16 at seeded positions) as the mutant mouse
                  collapses; below, the balance beam (driven by a tilt tracker) tips left into coral.
- s09_sepsis_adj: Balance beam swings right into coral septic shock as computed blood vessel walls widen,
                  stream leak droplets, and a linked BP bar drops; beam settles to emerald center with calm pulses.
- s10_wrap:       TNFR1 immediate brake and cytosolic note appear cleanly, then NF-κB on purple DNA
                  drives three growing, pulsing output paths: Defense, Survival, and Brakes.
"""

import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ concept palette
EMERALD = "#4ADE80"
PURPLE = "#B388FF"
AMBER = "#F5B041"
CORAL = "#FC6255"
CRIMSON = "#E11D48"
SKY = "#7DD3FC"
TEAL = "#3FB8C0"


# ------------------------------------------------------------------ computed helpers
def dna_strand(center=ORIGIN, width=4.6, amp=0.22, cycles=2.5, n_pts=120, n_rungs=14, color=PURPLE):
    """Build a schematic double-helix DNA segment computed from sine waves."""
    cx, cy, _ = np.array(center, dtype=float)
    xs = np.linspace(cx - width / 2, cx + width / 2, n_pts)
    phase = cycles * TAU * (xs - (cx - width / 2)) / width
    y1 = cy + amp * np.sin(phase)
    y2 = cy - amp * np.sin(phase)
    s1 = VMobject(stroke_color=color, stroke_width=4.5).set_points_as_corners(
        [np.array([x, y, 0.0]) for x, y in zip(xs, y1)]
    )
    s2 = VMobject(stroke_color=color, stroke_width=4.5, stroke_opacity=0.8).set_points_as_corners(
        [np.array([x, y, 0.0]) for x, y in zip(xs, y2)]
    )
    rungs = VGroup()
    rx = np.linspace(cx - width / 2 + 0.18, cx + width / 2 - 0.18, n_rungs)
    for x in rx:
        ph = cycles * TAU * (x - (cx - width / 2)) / width
        ya = cy + amp * np.sin(ph)
        yb = cy - amp * np.sin(ph)
        if abs(ya - yb) > 0.06:
            rungs.add(Line([x, ya, 0], [x, yb, 0], color=color, stroke_width=2.4, stroke_opacity=0.65))
    return VGroup(rungs, s1, s2)


def nfkb_dimer(scale=1.0, label="NF-κB"):
    """Schematic emerald NF-κB dimer (seamless peanut contour) + optional centered label."""
    lobe1 = Circle(radius=0.38, color=EMERALD).shift(LEFT * 0.28)
    lobe2 = Circle(radius=0.38, color=EMERALD).shift(RIGHT * 0.28)
    body = Union(lobe1, lobe2, stroke_color=EMERALD, stroke_width=3.6,
                 fill_color=EMERALD, fill_opacity=0.34).scale(scale)
    if label:
        lab = T(label, size=max(24, int(round(25 * min(1.0, scale)))), color=TEXT, weight=BOLD).move_to(body)
        if lab.width > body.width - 0.24:
            body.stretch(lab.width / max(body.width - 0.26, 0.4), 0)
        return VGroup(body, lab)
    return body


def ikb_clamp(scale=1.0, label="New IκBα"):
    """Coral C-shaped clamp sized to cradle outside an NF-κB dimer without crossing its letters."""
    c_arc = Arc(radius=0.62 * scale, start_angle=0.58 * PI, angle=0.84 * PI,
                stroke_color=CORAL, stroke_width=8.5 * scale)
    arm_top = Line(c_arc.get_start(), c_arc.get_start() + RIGHT * 0.95 * scale,
                   stroke_color=CORAL, stroke_width=8.5 * scale)
    arm_bot = Line(c_arc.get_end(), c_arc.get_end() + RIGHT * 0.95 * scale,
                   stroke_color=CORAL, stroke_width=8.5 * scale)
    shape = VGroup(c_arc, arm_top, arm_bot)
    if label:
        lab = T(label, size=26, color=CORAL, weight=BOLD).next_to(shape, UP, buff=0.18)
        return VGroup(shape, lab)
    return shape


def tnfr1_icon(pos=ORIGIN, direction=RIGHT, scale=1.0):
    """Schematic teal TNF receptor 1 spanning a membrane."""
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0.0])
    stem = Line(pos - d * 0.35 * scale, pos + d * 0.28 * scale, color=TEAL, stroke_width=6.5 * scale)
    cup = ArcBetweenPoints(
        pos + d * 0.28 * scale + perp * 0.26 * scale,
        pos + d * 0.28 * scale - perp * 0.26 * scale,
        angle=1.4, color=TEAL, stroke_width=5.5 * scale,
    )
    return VGroup(stem, cup)


def scissor_icon(scale=1.0, color=CORAL):
    """Clean geometric scissor icon for A20."""
    b1 = Line([-0.32, -0.14, 0], [0.36, 0.16, 0], color=color, stroke_width=5.5)
    b2 = Line([-0.32, 0.14, 0], [0.36, -0.16, 0], color=color, stroke_width=5.5)
    r1 = Circle(radius=0.14, color=color, stroke_width=4.5).move_to([-0.42, -0.18, 0])
    r2 = Circle(radius=0.14, color=color, stroke_width=4.5).move_to([-0.42, 0.18, 0])
    pivot = Dot(ORIGIN, radius=0.055, color=TEXT)
    return VGroup(b1, b2, r1, r2, pivot).scale(scale)


def death_icon(scale=1.0, color=CRIMSON):
    """Geometric crimson death-signal icon (octagon with bold X)."""
    ring = RegularPolygon(n=8, radius=0.38 * scale, color=color, stroke_width=4,
                          fill_color=color, fill_opacity=0.25)
    x1 = Line([-0.16 * scale, -0.16 * scale, 0], [0.16 * scale, 0.16 * scale, 0], color=color, stroke_width=5.5)
    x2 = Line([-0.16 * scale, 0.16 * scale, 0], [0.16 * scale, -0.16 * scale, 0], color=color, stroke_width=5.5)
    return VGroup(ring, x1, x2)


def mouse_silhouette(color=TEXT, scale=1.0, slumped=False):
    """Clean schematic mouse outline with readable fill."""
    body = Ellipse(width=1.7 * scale, height=0.95 * scale, stroke_color=color, stroke_width=3.8,
                   fill_color=color, fill_opacity=0.26)
    head = Ellipse(width=0.72 * scale, height=0.52 * scale, stroke_color=color, stroke_width=3.8,
                   fill_color=color, fill_opacity=0.30).move_to(body.get_right() + LEFT * 0.05 * scale + UP * 0.08 * scale)
    ear = Circle(radius=0.18 * scale, stroke_color=color, stroke_width=3.2,
                 fill_color=color, fill_opacity=0.32).move_to(head.get_top() + LEFT * 0.12 * scale)
    eye = Dot(head.get_center() + RIGHT * 0.15 * scale + UP * 0.06 * scale, radius=0.048 * scale, color=TEXT)
    tail = CubicBezier(
        body.get_left() + UP * 0.05 * scale,
        body.get_left() + LEFT * 0.55 * scale + UP * 0.35 * scale,
        body.get_left() + LEFT * 0.75 * scale + DOWN * 0.25 * scale,
        body.get_left() + LEFT * 1.15 * scale + UP * 0.05 * scale,
        color=color, stroke_width=3.8,
    )
    g = VGroup(tail, body, head, ear, eye)
    if slumped:
        g.rotate(-0.18)
    return g


def bacterium_rod(color=AMBER, scale=1.0, angle=0.3):
    """Rod-shaped Gram-negative bacterium icon."""
    capsule = RoundedRectangle(corner_radius=0.12 * scale, width=0.46 * scale, height=0.20 * scale,
                               stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
    flag1 = CubicBezier(
        capsule.get_left(),
        capsule.get_left() + LEFT * 0.14 * scale + UP * 0.08 * scale,
        capsule.get_left() + LEFT * 0.24 * scale + DOWN * 0.08 * scale,
        capsule.get_left() + LEFT * 0.36 * scale + UP * 0.04 * scale,
        color=color, stroke_width=2.4,
    )
    return VGroup(capsule, flag1).rotate(angle)


def build_macrophage_world(dimmed=False):
    """Carried world from Film 1: macrophage cross-section, coral warning halo, purple nucleus, DNA, NF-κB."""
    opacity_scale = 0.45 if dimmed else 1.0
    cell_outer = Ellipse(width=11.0, height=5.4, stroke_color=TEAL, stroke_width=4.5,
                         fill_color=TEAL, fill_opacity=0.14 * opacity_scale).move_to(DOWN * 0.35)
    halo = Ellipse(width=11.28, height=5.68, stroke_color=CORAL, stroke_width=5.5,
                   stroke_opacity=0.6 * opacity_scale, fill_opacity=0).move_to(DOWN * 0.35)
    nucleus = Ellipse(width=6.6, height=3.5, stroke_color=PURPLE, stroke_width=4.5,
                      fill_color=PURPLE, fill_opacity=0.22 * opacity_scale).move_to(DOWN * 0.65)
    dna = dna_strand(center=DOWN * 0.72, width=4.8, amp=0.20, cycles=2.5, color=PURPLE)
    if dimmed:
        dna.set_stroke(opacity=0.65)
    nf = nfkb_dimer(scale=1.1, label="NF-κB").move_to(DOWN * 0.16 + LEFT * 0.4)
    if dimmed:
        nf.set_opacity(0.55)
    return VGroup(halo, cell_outer, nucleus, dna, nf), halo, cell_outer, nucleus, dna, nf


def compute_nfkb_waves(t_max=13.5, dt=0.02):
    """Compute nuclear NF-κB activity from a delayed negative-feedback ODE under constant stimulus."""
    n_steps = int(t_max / dt) + 1
    tau_steps = int(1.35 / dt)
    N = np.zeros(n_steps)
    I = np.zeros(n_steps)
    N[0] = 0.08
    I[0] = 0.05
    k_act, k_pull, k_syn, k_deg = 1.65, 2.4, 1.45, 0.65
    for k in range(n_steps - 1):
        n_del = N[k - tau_steps] if k >= tau_steps else N[0]
        dN = k_act * (1.0 - N[k]) / (1.0 + 3.2 * I[k]) - k_pull * I[k] * N[k]
        dI = k_syn * n_del - k_deg * I[k]
        N[k + 1] = np.clip(N[k] + dt * dN, 0.0, 1.0)
        I[k + 1] = max(0.0, I[k] + dt * dI)
    ts = np.linspace(0.0, t_max, n_steps)
    return ts, N


# ------------------------------------------------------------------ S00: Hook
class S00Hook(SpokenScene):
    def construct(self):
        world, halo, cell_outer, nucleus, dna, nf = build_macrophage_world(dimmed=False)
        nuc_lbl = T("Nucleus", size=26, color=PURPLE).move_to(nucleus.get_bottom() + UP * 0.36)
        dna_lbl = T("DNA", size=26, color=PURPLE).move_to(dna.get_bottom() + DOWN * 0.25)
        q_lbl = boxed_label("Alarm ON: what stops it?", CORAL, size=30).move_to([0, 3.15, 0])

        pulse_t = ValueTracker(0.0)
        pulse_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(pulse_t)

        def make_alarm_waves():
            t = pulse_t.get_value()
            waves = VGroup()
            origin = nf.get_top() + UP * 0.1
            for k in range(3):
                ph = (t * 0.55 + k / 3.0) % 1.0
                r = 0.35 + ph * 1.85
                op = 0.9 * (1.0 - ph)
                arc = Arc(radius=r, start_angle=0.18 * PI, angle=0.64 * PI,
                          arc_center=origin, stroke_color=AMBER, stroke_width=5, stroke_opacity=op)
                waves.add(arc)
            return waves

        alarm_waves = always_redraw(make_alarm_waves)
        halo_t = ValueTracker(0.0)
        halo.add_updater(lambda m, dt: (
            halo_t.increment_value(dt),
            m.set_stroke(opacity=0.35 + 0.5 * abs(np.sin(3.2 * halo_t.get_value())),
                         width=4.5 + 3.5 * abs(np.sin(3.2 * halo_t.get_value())))
        ))

        self.add(world, alarm_waves, nuc_lbl, dna_lbl)
        self.play(FadeIn(q_lbl, shift=DOWN * 0.1), run_time=0.45)

        self.at("Once that powerful")
        self.wait(max(0.2, self.t_of("kill the cell") - self.elapsed() - 0.2))

        self.at("kill the cell")
        self.wait(max(0.2, self.t_of("right on DNA") - self.elapsed() - 0.2))

        self.at("right on DNA")
        halo.clear_updaters()
        pulse_t.clear_updaters()
        self.play(
            FadeOut(q_lbl), FadeOut(nuc_lbl), FadeOut(dna_lbl), FadeOut(alarm_waves),
            world.animate.scale(1.18, about_point=dna.get_center()).shift(DOWN * 0.35),
            run_time=max(0.6, self.narration_s - self.elapsed() - 0.05),
        )
        self.finish()


# ------------------------------------------------------------------ S01: Title (silent 2.0 s)
class S01Title(NarratedScene):
    def construct(self):
        world, halo, cell_outer, nucleus, dna, nf = build_macrophage_world(dimmed=True)
        world.scale(1.18, about_point=dna.get_center()).shift(DOWN * 0.35)
        t_pulse = ValueTracker(0.0)
        dna.add_updater(lambda m, dt: (
            t_pulse.increment_value(dt),
            m.set_stroke(opacity=0.45 + 0.35 * np.sin(4.0 * t_pulse.get_value()))
        ))
        title = T("Why the Alarm Needs Brakes", size=44, font=TITLE_FONT, color=TEXT).move_to([0, 3.25, 0])
        fit(title, max_w=11.8)
        self.add(world)
        self.play(FadeIn(title, shift=DOWN * 0.08), run_time=0.45)
        self.wait(1.1)
        self.play(FadeOut(title), run_time=0.45)
        dna.clear_updaters()
        self.finish()


# ------------------------------------------------------------------ S02: Two Brakes & IκBα
class S02Brakes(SpokenScene):
    def construct(self):
        cyto_bg = Rectangle(width=14.6, height=8.4, stroke_width=0,
                            fill_color=TEAL, fill_opacity=0.11).move_to(ORIGIN)
        nuc_arc = Ellipse(width=8.4, height=5.0, stroke_color=PURPLE, stroke_width=4.5,
                          fill_color=PURPLE, fill_opacity=0.24).move_to([-1.6, -0.45, 0])
        cyto_lbl = T("Cytosol", size=28, color=TEXT).move_to([4.5, 2.9, 0])
        nuc_lbl = T("Nucleus", size=28, color=PURPLE).move_to([-1.6, 1.65, 0])
        dna = dna_strand(center=[-1.8, -1.05, 0], width=6.0, amp=0.25, cycles=3.0, color=PURPLE)
        dna_lbl = T("DNA", size=26, color=PURPLE).next_to(dna, DOWN, buff=0.24)
        nf = nfkb_dimer(scale=1.1, label="NF-κB").move_to([-3.2, -0.38, 0])
        world_grp = VGroup(nuc_arc, dna, nf, nuc_lbl, dna_lbl)

        self.add(cyto_bg, world_grp, cyto_lbl)

        # Gentle zoom settle onto DNA + glowing NF-κB promoter activation during opening line
        glow_nf = Circle(radius=0.85, color=EMERALD, stroke_width=0, fill_color=EMERALD, fill_opacity=0.25).move_to(nf)
        self.add(glow_nf)
        self.play(
            world_grp.animate.scale(1.06, about_point=dna.get_center()),
            glow_nf.animate.scale(1.4).set_fill(opacity=0.0),
            run_time=max(1.0, self.t_of("Along with inflammatory") - self.elapsed() - 0.15),
        )
        self.remove(glow_nf)

        self.at("Along with inflammatory")
        infl_mark = Circle(radius=0.20, color=AMBER, fill_color=AMBER, fill_opacity=0.92).move_to([-1.2, -1.05, 0])
        infl_lbl = T("Inflammatory genes", size=26, color=AMBER).move_to([-1.1, 0.45, 0])
        infl_arr = Arrow(infl_mark.get_top(), infl_lbl.get_bottom() + DOWN * 0.05, color=AMBER, buff=0.05, stroke_width=5)
        infl_mrna = VMobject(stroke_color=AMBER, stroke_width=6.5).set_points_smoothly([
            np.array([-1.2, -0.95, 0]), np.array([-0.1, -0.15, 0]),
            np.array([1.4, 0.45, 0]), np.array([3.2, 0.95, 0]),
        ])
        mrna_glow = Circle(radius=0.45, color=AMBER, stroke_width=0, fill_color=AMBER, fill_opacity=0.28).move_to(infl_mark)
        self.play(FadeIn(infl_mark), GrowArrow(infl_arr), FadeIn(infl_lbl), FadeIn(mrna_glow), run_time=0.5)
        self.play(
            Create(infl_mrna),
            mrna_glow.animate.move_to([3.2, 0.95, 0]).scale(1.3).set_fill(opacity=0.08),
            run_time=max(1.0, self.t_of("turns on two") - self.elapsed() - 0.15),
        )
        self.remove(mrna_glow)

        self.at("turns on two")
        site1 = Dot([-0.15, -1.05, 0], radius=0.19, color=CORAL)
        site2 = Dot([0.75, -1.05, 0], radius=0.19, color=CORAL)
        halo1 = Circle(radius=0.45, color=CORAL, stroke_width=4, fill_color=CORAL, fill_opacity=0.22).move_to(site1)
        halo2 = Circle(radius=0.45, color=CORAL, stroke_width=4, fill_color=CORAL, fill_opacity=0.22).move_to(site2)
        b_lbl = T("Two brake genes", size=26, color=CORAL).move_to([0.2, 0.25, 0])
        self.play(
            FadeOut(infl_arr), FadeOut(infl_lbl), FadeOut(infl_mark), FadeOut(infl_mrna),
            FadeIn(site1), FadeIn(site2), FadeIn(b_lbl),
            run_time=0.45,
        )
        self.play(FadeIn(halo1), FadeIn(halo2), run_time=0.4)
        self.play(
            halo1.animate.scale(1.9).set_opacity(0.0),
            halo2.animate.scale(1.9).set_opacity(0.0),
            run_time=max(0.8, self.t_of("First it makes") - self.elapsed() - 0.15),
        )
        self.remove(halo1, halo2)

        self.at("First it makes")
        ribbon_pts = [
            np.array([-0.15, -0.95, 0]),
            np.array([0.8, -0.15, 0]),
            np.array([2.0, 0.55, 0]),
            np.array([3.2, 0.85, 0]),
            np.array([4.3, 0.6, 0]),
        ]
        ribbon = VMobject(stroke_color=CORAL, stroke_width=7.5)
        ribbon.set_points_smoothly(ribbon_pts)
        self.play(FadeOut(b_lbl), run_time=0.35)
        self.play(Create(ribbon), run_time=2.0)

        clamp = ikb_clamp(scale=1.05, label="New IκBα")
        clamp[0].flip(UP, about_point=clamp[0].get_center())
        clamp.move_to([4.35, 0.65, 0])
        self.play(ReplacementTransform(ribbon, clamp[0]), FadeIn(clamp[1]),
                  run_time=max(0.8, self.t_of("enters the nucleus") - self.elapsed() - 0.15))

        self.at("enters the nucleus")
        self.remove(clamp[0], clamp[1])
        self.add(clamp)
        self.play(clamp.animate.move_to([-1.6, -0.05, 0]),
                  run_time=max(0.8, self.t_of("lifts the switch") - self.elapsed() - 0.15))

        self.at("lifts the switch")
        clamp_shape, clamp_lab = clamp[0], clamp[1]
        target_shape_center = nf.get_center() + RIGHT * 0.14
        self.play(
            clamp_shape.animate.move_to(target_shape_center),
            clamp_lab.animate.next_to(nf, UP, buff=0.45),
            run_time=0.8,
        )
        bound = VGroup(clamp_shape, nf, clamp_lab)
        self.play(bound.animate.shift(UP * 0.55),
                  run_time=max(0.5, self.t_of("pulls it outside") - self.elapsed() - 0.2))

        self.at("pulls it outside")
        off_lbl = T("DNA switch OFF", size=28, color=TEXT).move_to([-1.8, -0.05, 0])
        self.play(
            bound.animate(run_time=0.65, rate_func=rush_from).move_to([4.45, 0.0, 0]),
            Succession(Wait(0.22), FadeIn(off_lbl, run_time=0.38)),
        )
        self.finish()


# ------------------------------------------------------------------ S03: A20 & Waves
class S03Waves(SpokenScene):
    def construct(self):
        left_panel_box = RoundedRectangle(corner_radius=0.18, width=6.1, height=6.5,
                                          stroke_color=TEAL, stroke_width=3,
                                          fill_color=TEAL, fill_opacity=0.13).move_to([-3.3, 0.0, 0])
        tlr = boxed_label("TLR / TRAF6", AMBER, size=24).move_to([-4.65, 2.55, 0])

        chain_x = -4.65
        beads = VGroup(*[Circle(radius=0.19, color=SKY, fill_color=SKY, fill_opacity=0.6, stroke_width=3.8)
                         .move_to([chain_x, 1.85 - i * 0.44, 0]) for i in range(5)])
        links = VGroup(*[Line(beads[i].get_bottom(), beads[i + 1].get_top(), color=SKY, stroke_width=5)
                         for i in range(4)])
        k63_lbl = T("K63 chain", size=24, color=SKY).move_to([-2.0, 1.65, 0])
        k63_arrow = Line(beads[1].get_right() + RIGHT * 0.08, k63_lbl.get_left() + LEFT * 0.1, color=SKY, stroke_width=3)

        ikk = boxed_label("IKK ON", TEAL, size=26).move_to([-1.95, 0.25, 0])
        ikk_link = Line(beads[3].get_right() + RIGHT * 0.06, ikk.get_left() + LEFT * 0.08, color=TEAL, stroke_width=4.5)

        nuc = RoundedRectangle(corner_radius=0.4, width=5.4, height=1.95,
                               stroke_color=PURPLE, stroke_width=4,
                               fill_color=PURPLE, fill_opacity=0.24).move_to([-3.3, -2.08, 0])
        dna = dna_strand(center=[-3.3, -2.35, 0], width=4.4, amp=0.16, cycles=2.5, color=PURPLE)
        a20_icon = scissor_icon(scale=1.0, color=CORAL).flip(UP).move_to([-4.30, -1.62, 0])
        a20_lbl = T("A20", size=28, color=CORAL, weight=BOLD).next_to(a20_icon, RIGHT, buff=0.18)
        a20_grp = VGroup(a20_icon, a20_lbl)

        # Start upstream relay centered and larger so half the screen is never empty before Plot appears
        relay_grp = VGroup(left_panel_box, tlr, links, beads, k63_lbl, k63_arrow, ikk_link, ikk, nuc, dna, a20_grp)
        relay_grp.scale(1.12).move_to([0.0, 0.0, 0])
        relay_grp.remove(a20_grp)
        self.add(relay_grp)

        a20_grp.shift(UP * 0.12)
        self.play(FadeIn(a20_grp, shift=UP * 0.12), run_time=0.6)
        glow_ikk = SurroundingRectangle(ikk, color=TEAL, buff=0.12, stroke_width=4)
        self.play(
            LaggedStart(*[b.animate.set_fill(TEXT, opacity=0.9) for b in beads], lag_ratio=0.18),
            Create(glow_ikk),
            run_time=max(1.2, self.t_of("A20 strips") - self.elapsed() - 0.15),
        )
        self.play(FadeOut(glow_ikk), beads.animate.set_fill(SKY, opacity=0.6), run_time=0.35)

        self.at("A20 strips")
        target_snip = links[1].get_center() + RIGHT * (a20_grp.width / 2 + 0.10)
        self.play(a20_grp.animate.move_to(target_snip), run_time=1.3)
        self.play(Rotate(a20_icon, 0.45), rate_func=there_and_back, run_time=0.45)
        self.play(Rotate(a20_icon, 0.45), rate_func=there_and_back, run_time=0.45)
        self.play(
            FadeOut(links[1]), FadeOut(links[2]), FadeOut(ikk_link, run_time=0.5),
            beads[2:].animate.shift(DOWN * 0.75 + LEFT * 0.25).set_opacity(0.38),
            links[3].animate.shift(DOWN * 0.75 + LEFT * 0.25).set_opacity(0.38),
            FadeOut(k63_arrow),
            run_time=max(1.0, self.t_of("shutting the relay") - self.elapsed() - 0.15),
        )

        self.at("shutting the relay")
        ikk_off = boxed_label("IKK OFF", TEXT, size=26).move_to(ikk.get_center())
        self.play(
            swap(ikk, ikk_off, run_time=0.55),
            tlr[0].animate.set_stroke(opacity=0.45).set_fill(opacity=0.06),
            tlr[1].animate.set_opacity(0.55),
            run_time=max(0.9, self.t_of("New I") - self.elapsed() - 0.15),
        )

        self.at("New I")
        # Rebuild/move relay cleanly to left half without scaling text below 22 pt
        relay_grp_fixed = VGroup(left_panel_box, tlr, links[0], links[3], beads, k63_lbl, ikk_off, nuc, dna, a20_grp)
        ts, N_vals = compute_nfkb_waves(t_max=13.5, dt=0.03)
        P = Plot(
            box=(0.55, 6.1, -1.75, 2.2),
            xr=(0, 13.5), yr=(0, 1.05),
            xticks=[], yticks=[],
            xlabel="time", ylabel="",
            color=GREY, size=24, label_size=26,
        )
        p_title = T("Nuclear NF-κB (schematic)", size=28, color=EMERALD, weight=BOLD).move_to([3.32, 2.85, 0])
        delay_note = T("IκBα synthesis delay", size=24, color=CORAL).move_to([3.32, -2.75, 0])

        t_trk = ValueTracker(0.0)
        n_of = lambda t: float(np.interp(t, ts, N_vals))
        live = P.live_curve(n_of, t_trk, color=EMERALD, width=5.5)

        def mk_area():
            t1 = t_trk.get_value()
            if t1 < 0.08:
                return VMobject()
            xs = np.linspace(0, t1, max(4, int(120 * t1 / 13.5) + 2))
            pts = [P.pt(0, 0)] + [P.pt(x, n_of(x)) for x in xs] + [P.pt(t1, 0)]
            return Polygon(*pts, stroke_width=0, fill_color=EMERALD, fill_opacity=0.25)

        shaded = always_redraw(mk_area)
        dot = P.dot(lambda: t_trk.get_value(), lambda: n_of(t_trk.get_value()), color=EMERALD, ring=TEXT, radius=0.11)

        self.play(
            relay_grp_fixed.animate.scale(1 / 1.12).move_to([-3.3, 0.0, 0]),
            Create(P), FadeIn(p_title), FadeIn(delay_note),
            run_time=1.0,
        )
        self.add(shaded, live, dot)
        self.play(t_trk.animate(rate_func=linear).set_value(4.5),
                  run_time=max(0.6, self.t_of("arrives late") - self.elapsed()))

        self.at("arrives late")
        self.play(t_trk.animate(rate_func=linear).set_value(9.0),
                  run_time=max(0.8, self.t_of("rises and falls") - self.elapsed()))

        self.at("rises and falls")
        self.play(t_trk.animate(rate_func=linear).set_value(13.5),
                  run_time=max(1.0, self.narration_s - self.elapsed() - 0.05))
        self.finish()


# ------------------------------------------------------------------ S04: TNF Secretion & Dual Signal
class S04Tnf(SpokenScene):
    def construct(self):
        mac = Ellipse(width=4.8, height=5.8, stroke_color=TEAL, stroke_width=4.5,
                      fill_color=TEAL, fill_opacity=0.16).move_to([-3.65, -0.1, 0])
        mac_lbl = T("Macrophage", size=28, color=TEAL).move_to([-3.65, 3.15, 0])
        mac_nuc = Ellipse(width=3.2, height=2.3, stroke_color=PURPLE, stroke_width=4,
                          fill_color=PURPLE, fill_opacity=0.24).move_to([-3.85, -0.5, 0])
        mac_dna = dna_strand(center=[-3.85, -0.82, 0], width=2.3, amp=0.15, cycles=2.0, color=PURPLE)
        mac_nf = nfkb_dimer(scale=0.9, label="NF-κB").move_to([-3.85, -0.05, 0])
        mac_grp = VGroup(mac, mac_lbl, mac_nuc, mac_dna, mac_nf)

        nbr = Ellipse(width=5.6, height=5.8, stroke_color=TEAL, stroke_width=4.5,
                      fill_color=TEAL, fill_opacity=0.16).move_to([3.3, -0.1, 0])
        nbr_lbl = T("Neighbor cell", size=28, color=TEAL).move_to([3.3, 3.15, 0])
        nbr_nuc = Ellipse(width=2.1, height=2.2, stroke_color=PURPLE, stroke_width=4,
                          fill_color=PURPLE, fill_opacity=0.24).move_to([4.65, -0.2, 0])
        nbr_grp = VGroup(nbr, nbr_lbl, nbr_nuc)

        rec_self = tnfr1_icon(pos=np.array([-1.4, 1.1, 0]), direction=RIGHT * 0.9 + UP * 0.4, scale=1.05)
        rec_nbr = tnfr1_icon(pos=np.array([0.52, -0.1, 0]), direction=LEFT, scale=1.2)
        rec_lbl = T("TNF receptor 1", size=26, color=TEAL).move_to([0.25, -2.6, 0])
        rec_ptr = Line(rec_lbl.get_top() + UP * 0.08, rec_nbr.get_bottom() + DOWN * 0.14,
                       color=TEAL, stroke_width=3, stroke_opacity=0.8)

        # Start macrophage slightly centered, then pull left and FadeIn neighbor cell (never .set_opacity(1)!)
        mac_grp.shift(RIGHT * 1.8)
        rec_self.shift(RIGHT * 1.8)
        self.add(mac_grp, rec_self)

        self.play(
            mac_grp.animate.shift(LEFT * 1.8),
            rec_self.animate.shift(LEFT * 1.8),
            FadeIn(nbr_grp, shift=LEFT * 1.2),
            FadeIn(rec_nbr, shift=LEFT * 1.2),
            run_time=2.2,
        )
        tx_wave = Line([-4.6, -0.82, 0], [-4.5, -0.82, 0], color=AMBER, stroke_width=7)
        self.add(tx_wave)
        self.play(
            tx_wave.animate.put_start_and_end_on([-4.6, -0.82, 0], [-3.25, -0.82, 0]),
            run_time=max(0.8, self.t_of("tumor necrosis factor") - self.elapsed() - 0.15),
        )

        self.at("tumor necrosis factor")
        self.remove(tx_wave)
        tnf_gene = Dot([-3.3, -0.82, 0], radius=0.18, color=AMBER)
        tnf_lbl = T("TNF", size=28, color=AMBER, weight=BOLD).move_to([-0.45, 2.35, 0])
        rng = np.random.default_rng(7)

        def make_tnf_particle(pos):
            core = Dot(pos, radius=0.13, color=AMBER)
            glow = Circle(radius=0.22, color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.25).move_to(pos)
            return VGroup(glow, core)

        tnf_dots = VGroup(*[make_tnf_particle([-2.6, -0.2 + rng.uniform(-0.35, 0.35), 0]) for _ in range(10)])
        self.play(FadeIn(tnf_gene), FadeIn(tnf_lbl), run_time=0.45)
        self.play(FadeIn(tnf_dots, lag_ratio=0.08),
                  tnf_dots.animate.shift(RIGHT * 1.0 + UP * 0.25),
                  run_time=max(0.8, self.t_of("secreted signaling protein") - self.elapsed() - 0.15))

        self.at("secreted signaling protein")
        targets_mid = [
            np.array([-0.65, 1.55, 0]), np.array([-0.5, 1.15, 0]),
            np.array([-0.4, 0.75, 0]), np.array([-0.35, 0.35, 0]),
            np.array([-0.45, -0.05, 0]), np.array([-0.55, -0.45, 0]),
            np.array([-0.35, -0.85, 0]), np.array([-0.7, 0.45, 0]),
            np.array([-0.6, -0.25, 0]), np.array([-0.45, 0.95, 0]),
        ]
        self.play(
            *[d.animate.move_to(p) for d, p in zip(tnf_dots, targets_mid)],
            run_time=max(1.2, self.t_of("Amber TNF binds") - self.elapsed() - 0.15),
        )

        self.at("Amber TNF binds")
        self.play(
            tnf_dots[0].animate.move_to(rec_self.get_right() + LEFT * 0.05),
            tnf_dots[1].animate.move_to(rec_self.get_right() + DOWN * 0.18),
            tnf_dots[2].animate.move_to(rec_nbr.get_left() + RIGHT * 0.05),
            tnf_dots[3].animate.move_to(rec_nbr.get_left() + RIGHT * 0.05 + UP * 0.16),
            tnf_dots[4].animate.move_to(rec_nbr.get_left() + RIGHT * 0.05 + DOWN * 0.16),
            FadeIn(rec_lbl), Create(rec_ptr),
            run_time=2.0,
        )
        # Active receptor wave pulsing inside neighbor cell continuously up to fork
        fork_start = rec_nbr.get_right() + RIGHT * 0.08
        die_node = death_icon(scale=1.0, color=CRIMSON).move_to([3.05, 1.35, 0])
        die_lbl = T("Die", size=28, color=CRIMSON, weight=BOLD).next_to(die_node, UP, buff=0.16)
        alive_nf = nfkb_dimer(scale=0.92, label="NF-κB").move_to([3.05, -1.35, 0])
        alive_lbl = T("Stay alive", size=28, color=EMERALD, weight=BOLD).next_to(alive_nf, DOWN, buff=0.16)

        rip1 = Circle(radius=0.35, color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.2).move_to(rec_nbr.get_right())
        rip2 = Circle(radius=0.35, color=AMBER, stroke_width=4.5, fill_color=AMBER, fill_opacity=0.2).move_to(rec_self.get_left())
        self.add(rip1, rip2)
        self.play(
            rip1.animate.scale(4.2).set_opacity(0.0),
            rip2.animate.scale(3.2).set_opacity(0.0),
            run_time=max(1.2, self.t_of("two opposite messages") - self.elapsed() - 0.15),
        )
        self.remove(rip1, rip2)

        self.at("two opposite messages")
        arr_die = Arrow(fork_start, die_node.get_left() + LEFT * 0.12, color=CRIMSON, stroke_width=6, buff=0.05)
        arr_alive = Arrow(fork_start, alive_nf.get_left() + LEFT * 0.12, color=EMERALD, stroke_width=6, buff=0.05)

        self.play(
            GrowArrow(arr_die), FadeIn(die_node),
            GrowArrow(arr_alive), FadeIn(alive_nf),
            run_time=max(1.0, self.t_of("die and stay alive") - self.elapsed() - 0.1),
        )

        self.at("die and stay alive")
        self.play(FadeIn(die_lbl), FadeIn(alive_lbl), run_time=0.45)
        ring_d = Circle(radius=0.48, color=CRIMSON, stroke_width=4).move_to(die_node)
        ring_a = Circle(radius=0.55, color=EMERALD, stroke_width=4).move_to(alive_nf)
        self.add(ring_d, ring_a)
        self.play(
            ring_d.animate.scale(1.8).set_opacity(0.0),
            ring_a.animate.scale(1.8).set_opacity(0.0),
            run_time=max(0.7, self.narration_s - self.elapsed() - 0.05),
        )
        self.remove(ring_d, ring_a)
        self.finish()


# ------------------------------------------------------------------ S05: Survival Checkpoints & Contrast
class S05Survival(SpokenScene):
    def construct(self):
        nbr = Ellipse(width=10.6, height=6.2, stroke_color=TEAL, stroke_width=4.5,
                      fill_color=TEAL, fill_opacity=0.14).move_to([0.3, -0.05, 0])
        rec = tnfr1_icon(pos=np.array([-5.0, -0.05, 0]), direction=LEFT, scale=1.35)
        tnf_dot = Dot(rec.get_left() + RIGHT * 0.05, radius=0.15, color=AMBER)
        nuc = Ellipse(width=3.7, height=4.0, stroke_color=PURPLE, stroke_width=4.5,
                      fill_color=PURPLE, fill_opacity=0.22).move_to([3.2, -0.15, 0])
        dna = dna_strand(center=[3.2, -0.35, 0], width=2.6, amp=0.18, cycles=2.0, color=PURPLE)

        fork_start = rec.get_right() + RIGHT * 0.08
        die_node = death_icon(scale=1.15, color=CRIMSON).move_to([0.3, 1.55, 0])
        die_lbl = T("Die", size=28, color=CRIMSON, weight=BOLD).next_to(die_node, UP, buff=0.14)
        nf = nfkb_dimer(scale=1.0, label="NF-κB").move_to([-1.2, -1.45, 0])
        alive_lbl = T("Stay alive", size=28, color=EMERALD, weight=BOLD).next_to(nf, DOWN, buff=0.16)

        arr_die = Arrow(fork_start, die_node.get_left() + LEFT * 0.14, color=CRIMSON, stroke_width=5.5, buff=0.05)
        arr_alive = Arrow(fork_start, nf.get_left() + LEFT * 0.14, color=EMERALD, stroke_width=5.5, buff=0.05)

        self.add(nbr, rec, tnf_dot, nuc, dna, die_node, die_lbl, nf, alive_lbl, arr_die, arr_alive)

        self.at("Normally stay")
        sig_alive = Dot(fork_start, radius=0.11, color=EMERALD)
        self.add(sig_alive)
        self.play(
            arr_alive.animate.set_stroke(width=7.5),
            sig_alive.animate.move_to(nf.get_left() + LEFT * 0.14),
            run_time=max(1.0, self.t_of("immediate break") - self.elapsed() - 0.15),
        )
        self.remove(sig_alive)

        self.at("immediate break")
        clamp_pt = fork_start + RIGHT * 0.85 + UP * 0.32
        chk_ring = RoundedRectangle(corner_radius=0.12, width=0.52, height=0.72,
                                    stroke_color=TEAL, stroke_width=6, fill_color=BG, fill_opacity=0.95).move_to(clamp_pt)
        chk_bar = Line(chk_ring.get_top() + DOWN * 0.15, chk_ring.get_bottom() + UP * 0.15, color=TEAL, stroke_width=6)
        chk = VGroup(chk_ring, chk_bar)
        chk_lbl = T("Receptor\ncheckpoint", size=24, color=TEAL, weight=BOLD, line_spacing=0.85).move_to([-2.40, 1.60, 0])
        self.play(FadeIn(chk, scale=0.7), FadeIn(chk_lbl), run_time=0.45)
        self.play(
            arr_die.animate.set_opacity(0.35),
            VGroup(die_node, die_lbl).animate.set_opacity(0.35),
            run_time=0.7,
        )
        # Crimson death signal tries to push toward clamp and rebounds/halts continuously until 10.3s
        die_pulse = Dot(fork_start, radius=0.12, color=CRIMSON)
        self.add(die_pulse)
        for _ in range(2):
            self.play(die_pulse.animate.move_to(chk.get_left() + LEFT * 0.08), run_time=1.0)
            self.play(die_pulse.animate.move_to(fork_start), run_time=0.8)
        self.remove(die_pulse)

        self.at("NF kappa B turns on")
        self.play(FadeOut(alive_lbl), FadeOut(arr_alive), run_time=0.35)
        self.play(nf.animate.move_to([3.2, 0.38, 0]), run_time=1.5)
        shield = Arc(radius=2.1, start_angle=0.68 * PI, angle=0.64 * PI,
                     arc_center=[2.9, 0.1, 0], stroke_color=EMERALD, stroke_width=11)
        shield_lbl = T("Survival genes", size=26, color=EMERALD, weight=BOLD).move_to([3.2, -1.35, 0])
        self.play(Create(shield), FadeIn(shield_lbl, run_time=0.45),
                  run_time=max(1.2, self.t_of("Block that survival") - self.elapsed() - 0.15))

        self.at("Block that survival")
        tp = TwoPanel("Normal: survival wins", "Survival blocked", colors=(EMERALD, CRIMSON), top=3.05, bottom=-2.35)

        def mini_cell(blocked=False):
            c = Ellipse(width=4.4, height=3.1, stroke_color=CRIMSON if blocked else TEAL, stroke_width=4,
                        fill_color=(CRIMSON if blocked else TEAL), fill_opacity=0.14)
            r = tnfr1_icon(pos=c.get_left(), direction=LEFT, scale=0.82)
            td = Dot(r.get_left() + RIGHT * 0.04, radius=0.11, color=AMBER)
            nu = Ellipse(width=1.5, height=1.65, stroke_color=PURPLE, stroke_width=3.5,
                         fill_color=PURPLE, fill_opacity=0.22).move_to(c.get_center() + RIGHT * 1.05)
            nfm = nfkb_dimer(scale=0.6, label="").move_to(nu.get_center() if not blocked else c.get_center() + LEFT * 0.25 + DOWN * 0.72)
            grp = VGroup(c, r, td, nu, nfm)
            if not blocked:
                sh = Arc(radius=0.95, start_angle=0.65 * PI, angle=0.7 * PI,
                         arc_center=nu.get_center() + LEFT * 0.1, stroke_color=EMERALD, stroke_width=8)
                grp.add(sh)
            else:
                lk = ikb_clamp(scale=0.55, label="").move_to(nfm.get_center() + LEFT * 0.06)
                arr_d = Arrow(r.get_right() + RIGHT * 0.05, c.get_center() + RIGHT * 0.35 + UP * 0.55,
                              color=CRIMSON, stroke_width=5.5, buff=0.05)
                grp.add(lk, arr_d)
            return grp

        left_pic = mini_cell(blocked=False)
        right_pic = mini_cell(blocked=True)
        tp.put(left_pic, "left")
        tp.put(right_pic, "right")
        left_pic.shift(UP * 0.18)
        right_pic.shift(UP * 0.18)
        locked_lbl = T("Locked IκB", size=26, color=CORAL).next_to(right_pic, DOWN, buff=0.35)
        shield_ok = T("Shield intact", size=26, color=EMERALD).next_to(left_pic, DOWN, buff=0.35)

        self.play(
            FadeOut(VGroup(nbr, rec, tnf_dot, nuc, dna, die_node, die_lbl, nf, arr_die,
                           chk, chk_lbl, shield, shield_lbl)),
            run_time=0.35,
        )
        self.play(
            FadeIn(tp), FadeIn(left_pic), FadeIn(right_pic), FadeIn(locked_lbl), FadeIn(shield_ok),
            run_time=0.5,
        )

        self.at("kills the cell")
        right_cell = right_pic[0]
        shards = VGroup(*[
            Line(
                right_cell.point_from_proportion(i / 8.0),
                right_cell.point_from_proportion((i + 0.55) / 8.0),
                color=CRIMSON, stroke_width=4.5,
            )
            for i in range(8)
        ])
        self.add(shards)
        self.play(
            FadeOut(right_cell),
            *[s.animate.shift((s.get_center() - right_cell.get_center()) * 0.11) for s in shards],
            run_time=1.8,
        )

        self.at("anti death")
        cap = caption("The anti-death, death pathway", size=30, color=TEXT, y=-3.05)
        self.play(
            FadeIn(cap, run_time=0.45),
            *[s.animate.shift((s.get_center() - right_cell.get_center()) * 0.04) for s in shards],
            run_time=max(0.8, self.narration_s - self.elapsed() - 0.05),
        )
        self.finish()


# ------------------------------------------------------------------ S06 & S07: Predict & Pause
def build_mouse_panels(show_bact=False):
    """Shared TwoPanel builder for S06Predict and S07Pause (labels never scaled below 24 pt)."""
    tp = TwoPanel("Purified endotoxin", "Live bacteria", colors=(AMBER, AMBER), top=3.15, bottom=-2.35)

    lc, lw, lh = tp.area("left")
    norm_m = mouse_silhouette(CRIMSON, scale=0.72, slumped=True).move_to(lc + UP * 1.25)
    norm_lbl = T("Normal: Shock", size=26, color=CRIMSON, weight=BOLD).next_to(norm_m, DOWN, buff=0.28)
    mut_m = mouse_silhouette(EMERALD, scale=0.72, slumped=False).move_to(lc + DOWN * 0.65)
    mut_lbl = T("TLR4-mutant: No shock", size=26, color=EMERALD, weight=BOLD).next_to(mut_m, DOWN, buff=0.24)
    left_grp = VGroup(norm_m, norm_lbl, mut_m, mut_lbl)

    rc, rw, rh = tp.area("right")
    r_mut = mouse_silhouette(TEXT, scale=1.05, slumped=False).move_to(rc + DOWN * 0.25)
    r_lbl = T("TLR4-mutant mouse", size=28, color=TEXT, weight=BOLD).move_to(rc + UP * 1.45)
    bact_offsets = [(-1.55, 0.7), (-1.4, -0.45), (1.5, 0.75), (1.55, -0.35), (0.0, 0.8)]
    bacts = VGroup(*[
        bacterium_rod(AMBER, scale=0.95, angle=0.35 * (i % 3 - 1)).move_to(r_mut.get_center() + np.array([dx, dy, 0]))
        for i, (dx, dy) in enumerate(bact_offsets)
    ])
    if not show_bact:
        bacts.set_opacity(0)
    right_grp = VGroup(r_lbl, r_mut, bacts)
    return tp, left_grp, norm_m, norm_lbl, mut_m, mut_lbl, right_grp, r_lbl, r_mut, bacts


class S06Predict(SpokenScene):
    def construct(self):
        tp, left_grp, norm_m, norm_lbl, mut_m, mut_lbl, right_grp, r_lbl, r_mut, bacts = build_mouse_panels(show_bact=False)
        norm_upright = mouse_silhouette(TEXT, scale=0.72, slumped=False).move_to(norm_m.get_center())
        mut_neutral = mouse_silhouette(TEXT, scale=0.72, slumped=False).move_to(mut_m.get_center())
        norm_pre = T("Normal mouse", size=26, color=TEXT).move_to(norm_lbl.get_center())
        mut_pre = T("TLR4-mutant", size=26, color=TEXT).move_to(mut_lbl.get_center())

        self.play(
            FadeIn(tp), FadeIn(norm_upright), FadeIn(norm_pre),
            FadeIn(mut_neutral), FadeIn(mut_pre),
            FadeIn(r_lbl), FadeIn(r_mut),
            run_time=0.9,
        )
        self.wait(max(0.2, self.t_of("Normal mice collapse") - self.elapsed() - 0.15))

        self.at("Normal mice collapse")
        endo_dots = VGroup(*[Dot(norm_upright.get_left() + LEFT * 0.75 + UP * (0.2 * i - 0.2), radius=0.11, color=AMBER) for i in range(5)])
        shock_halo = Ellipse(width=1.85, height=0.88, stroke_color=CRIMSON, stroke_width=4, fill_color=CRIMSON, fill_opacity=0.22).move_to(norm_m[1].get_center() + RIGHT * 0.15)
        self.play(FadeIn(endo_dots), run_time=0.35)
        self.play(endo_dots.animate.shift(RIGHT * 0.85), run_time=1.3)
        self.play(
            ReplacementTransform(norm_upright, norm_m),
            FadeIn(shock_halo),
            swap(norm_pre, norm_lbl, run_time=0.45),
            run_time=1.0,
        )
        # Sweep second endotoxin wave toward mutant mouse up to "shrug off"
        endo_dots2 = VGroup(*[Dot(mut_neutral.get_left() + LEFT * 0.9 + UP * (0.18 * i - 0.25), radius=0.11, color=AMBER) for i in range(5)])
        self.play(
            shock_halo.animate.set_stroke(opacity=0.45),
            FadeIn(endo_dots2),
            endo_dots2.animate.shift(RIGHT * 0.5),
            run_time=max(1.2, self.t_of("shrug off") - self.elapsed() - 0.15),
        )

        self.at("shrug off")
        self.play(
            ReplacementTransform(mut_neutral, mut_m),
            swap(mut_pre, mut_lbl, run_time=0.45),
            endo_dots2.animate.shift(LEFT * 0.35 + UP * 0.25).set_opacity(0.6),
            run_time=max(1.2, self.t_of("How do those") - self.elapsed() - 0.15),
        )

        self.at("How do those")
        self.play(
            FadeOut(endo_dots), FadeOut(endo_dots2), FadeOut(shock_halo),
            run_time=0.45,
        )
        self.play(Indicate(r_mut, color=AMBER, scale_factor=1.08),
                  run_time=max(1.0, self.t_of("live gram") - self.elapsed() - 0.15))

        self.at("live gram")
        bacts.set_opacity(1)
        q = question_card("TLR4-mutant mice meet live bacteria: better or worse off?", y=-3.05, size=30)
        self.play(FadeIn(q), run_time=0.4)
        self.play(FadeIn(bacts, shift=LEFT * 0.45),
                  run_time=max(0.8, self.narration_s - self.elapsed() - 0.05))
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "TLR4-mutant mice meet live bacteria: better or worse off?"
    CARD = {"y": -3.05, "size": 30}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 4.5

    def backdrop(self):
        tp, left_grp, norm_m, norm_lbl, mut_m, mut_lbl, right_grp, r_lbl, r_mut, bacts = build_mouse_panels(show_bact=True)
        for i, b in enumerate(bacts):
            bob(b, amp=0.045, speed=2.2, seed=i + 1)
        return VGroup(tp, left_grp, right_grp)


# ------------------------------------------------------------------ S08: Reveal & Too Little Balance
def build_balance_beam(tilt_tracker, center=(0, -1.65, 0), half_len=4.1):
    """Horizontal balance beam driven by tilt_tracker (-1 left crimson, 0 level emerald, +1 right crimson)."""
    cx, cy, _ = np.array(center, dtype=float)
    fulcrum = Triangle(color=TEXT, stroke_width=3.5, fill_color=EMERALD, fill_opacity=0.35).scale(0.40).move_to([cx, cy - 0.36, 0])
    title = T("Innate alarm balance (schematic)", size=26, color=TEXT).move_to([cx, cy - 1.48, 0])

    def mk_beam():
        t = float(tilt_tracker.get_value())
        ang = -t * 0.19
        dx = half_len * np.cos(ang)
        dy = half_len * np.sin(ang)
        left_pt = np.array([cx - dx, cy - dy, 0.0])
        right_pt = np.array([cx + dx, cy + dy, 0.0])
        col = EMERALD if abs(t) < 0.25 else CRIMSON
        beam = Line(left_pt, right_pt, color=col, stroke_width=7.5)
        pivot = Dot([cx, cy, 0], radius=0.12, color=EMERALD if abs(t) < 0.25 else TEXT)
        l_pan = Circle(radius=0.20, color=CRIMSON if t < -0.25 else GREY, fill_color=CRIMSON if t < -0.25 else GREY, fill_opacity=0.65).move_to(left_pt)
        r_pan = Circle(radius=0.20, color=CRIMSON if t > 0.25 else GREY, fill_color=CRIMSON if t > 0.25 else GREY, fill_opacity=0.65).move_to(right_pt)
        return VGroup(beam, pivot, l_pan, r_pan)

    beam_dyn = always_redraw(mk_beam)
    return VGroup(fulcrum, beam_dyn, title)


class S08Reveal(SpokenScene):
    def construct(self):
        # Start full-stage (no empty lower 60%!), then compress cleanly to upper band when beam arrives
        stage_box = RoundedRectangle(corner_radius=0.2, width=12.2, height=5.1,
                                     stroke_color=CRIMSON, stroke_width=3.5,
                                     fill_color=CRIMSON, fill_opacity=0.06).move_to([0, 0.4, 0])
        r_mut = mouse_silhouette(TEXT, scale=1.35, slumped=False).move_to([-2.4, 0.2, 0])
        ans_lbl = T("Worse off: no early alarm", size=34, color=CRIMSON, weight=BOLD).move_to([2.6, 1.35, 0])
        q_old = question_card("TLR4-mutant mice meet live bacteria: better or worse off?", y=-3.05, size=30)

        rng = np.random.default_rng(7)
        bacts_start = VGroup(*[
            bacterium_rod(AMBER, scale=1.15, angle=rng.uniform(-0.6, 0.6))
            .move_to(r_mut.get_center() + np.array([dx, dy, 0]))
            for dx, dy in [(-1.85, 0.65), (-1.7, -0.55), (1.85, 0.65), (1.9, -0.55), (0.0, 1.0)]
        ])
        for i, b in enumerate(bacts_start):
            bob(b, amp=0.04, speed=2.2, seed=i)
        self.add(stage_box, r_mut, bacts_start, q_old)

        self.at("Far worse off")
        self.play(FadeOut(q_old, run_time=0.35), FadeIn(ans_lbl, run_time=0.4), run_time=0.6)
        self.wait(max(0.3, self.t_of("multiply faster") - self.elapsed() - 0.15))

        self.at("multiply faster")
        extra_bacts = VGroup(*[
            bacterium_rod(AMBER, scale=1.05, angle=rng.uniform(-0.8, 0.8))
            .move_to(r_mut.get_center() + np.array([rng.uniform(-2.3, 2.3), rng.uniform(-1.05, 1.15), 0]))
            for _ in range(11)
        ])
        collapsed_mut = mouse_silhouette(CRIMSON, scale=1.35, slumped=True).move_to(r_mut.get_center())
        sub_ans = T("Bacteria outrun defense", size=28, color=AMBER).move_to([2.6, 0.35, 0])
        self.play(FadeIn(sub_ans), run_time=0.4)
        self.play(
            FadeIn(extra_bacts, lag_ratio=0.12),
            ReplacementTransform(r_mut, collapsed_mut),
            run_time=max(1.2, self.t_of("Humans show both") - self.elapsed() - 0.15),
        )

        self.at("Humans show both")
        for b in bacts_start:
            b.clear_updaters()
        upper_box_target = RoundedRectangle(corner_radius=0.18, width=12.4, height=2.85,
                                            stroke_color=CRIMSON, stroke_width=3,
                                            fill_color=CRIMSON, fill_opacity=0.08).move_to([0, 1.98, 0])
        pic_only = VGroup(collapsed_mut, bacts_start, extra_bacts)
        tilt = ValueTracker(0.0)
        beam_grp = build_balance_beam(tilt, center=(0, -1.65, 0), half_len=4.1)
        self.play(
            ReplacementTransform(stage_box, upper_box_target),
            pic_only.animate.scale(0.62).move_to([-2.4, 1.92, 0]),
            ans_lbl.animate.scale(0.88).move_to([2.4, 2.78, 0]),
            sub_ans.animate.scale(0.92).move_to([2.4, 2.0, 0]),
            FadeIn(beam_grp),
            run_time=1.3,
        )

        self.at("without working")
        left_lbl = boxed_label("Too little: MyD88 or IRAK4 loss", CRIMSON, size=24).move_to([-3.3, -0.02, 0])
        self.play(FadeIn(left_lbl), run_time=0.4)
        self.play(
            tilt.animate.set_value(-1.0),
            run_time=max(1.2, self.t_of("pus forming") - self.elapsed() - 0.15),
        )

        self.at("pus forming")
        fever_lbl = T("Severe infections, little fever", size=26, color=AMBER).move_to([-3.3, -0.68, 0])
        self.play(FadeIn(fever_lbl), run_time=0.4)
        for i, b in enumerate(extra_bacts):
            bob(b, amp=0.03, speed=2.4, seed=i)
        self.wait(max(0.2, self.narration_s - self.elapsed() - 0.05))
        for b in extra_bacts:
            b.clear_updaters()
        self.finish()


# ------------------------------------------------------------------ S09: Sepsis & Vaccine Adjuvant
class S09SepsisAdj(SpokenScene):
    def construct(self):
        tilt = ValueTracker(-1.0)
        beam_grp = build_balance_beam(tilt, center=(0, -1.65, 0), half_len=4.1)
        left_lbl = boxed_label("Too little: MyD88 or IRAK4 loss", CRIMSON, size=24).move_to([-3.3, -0.02, 0])
        self.add(beam_grp, left_lbl)

        self.at("At the other extreme")
        self.play(FadeOut(left_lbl), run_time=0.4)
        self.play(
            tilt.animate.set_value(1.0),
            run_time=max(1.5, self.t_of("widespread TNF") - self.elapsed() - 0.15),
        )

        self.at("widespread TNF")
        rng = np.random.default_rng(11)
        tnf_swarm = VGroup(*[
            Dot([rng.uniform(-5.2, 5.2), rng.uniform(0.95, 2.55), 0], radius=0.11, color=AMBER)
            for _ in range(18)
        ])
        tnf_tag = T("Widespread TNF release", size=26, color=AMBER).move_to([-3.65, 2.98, 0])
        self.play(FadeIn(tnf_tag), run_time=0.4)
        self.play(FadeIn(tnf_swarm, lag_ratio=0.06), run_time=1.0)
        self.play(
            *[d.animate.shift(RIGHT * rng.uniform(-0.25, 0.25) + UP * rng.uniform(-0.15, 0.15)) for d in tnf_swarm],
            run_time=max(0.5, self.t_of("septic shock") - self.elapsed() - 0.15),
        )

        self.at("septic shock")
        right_lbl = boxed_label("Too much: septic shock", CRIMSON, size=26).move_to([3.3, 0.05, 0])
        self.play(
            FadeIn(right_lbl, run_time=0.45),
            *[d.animate.shift(RIGHT * rng.uniform(-0.25, 0.25) + UP * rng.uniform(-0.15, 0.15)) for d in tnf_swarm],
            run_time=max(0.6, self.t_of("Blood vessels widen") - self.elapsed() - 0.15),
        )

        self.at("Blood vessels widen")
        vaso = ValueTracker(0.0)
        leak_t = ValueTracker(0.0)
        leak_t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(leak_t)

        def mk_vessel():
            v = vaso.get_value()
            lt = leak_t.get_value()
            hw = 0.24 + 0.28 * v
            gap = 0.04 + 0.16 * v
            cx, cy = 0.65, 1.85
            lumen = Rectangle(width=3.6, height=2 * hw, stroke_width=0, fill_color=CRIMSON, fill_opacity=0.22).move_to([cx, cy, 0])
            top_l = Line([cx - 1.8, cy + hw, 0], [cx - gap, cy + hw, 0], color=CRIMSON, stroke_width=5.5)
            top_r = Line([cx + gap, cy + hw, 0], [cx + 1.8, cy + hw, 0], color=CRIMSON, stroke_width=5.5)
            bot_l = Line([cx - 1.8, cy - hw, 0], [cx - gap, cy - hw, 0], color=CRIMSON, stroke_width=5.5)
            bot_r = Line([cx + gap, cy - hw, 0], [cx + 1.8, cy - hw, 0], color=CRIMSON, stroke_width=5.5)
            leaks = VGroup()
            if v > 0.2:
                for k, sx in enumerate((-0.45, 0.0, 0.45)):
                    ph = (lt * 0.9 + k * 0.33) % 1.0
                    dy = 0.08 + ph * 0.22
                    op = (1.0 - 0.7 * ph) * v
                    leaks.add(Dot([cx + sx * (1 + ph * 0.4), cy + hw + dy, 0], radius=0.07, color=CRIMSON, fill_opacity=op))
                    leaks.add(Dot([cx + sx * (1 + ph * 0.4), cy - hw - dy, 0], radius=0.07, color=CRIMSON, fill_opacity=op))
            return VGroup(lumen, top_l, top_r, bot_l, bot_r, leaks)

        vessel = always_redraw(mk_vessel)
        vessel_lbl = T("Vessels widen & leak", size=26, color=CRIMSON).move_to([0.65, 3.15, 0])

        bp_track = RoundedRectangle(corner_radius=0.08, width=0.50, height=1.55,
                                    stroke_color=TEXT, stroke_width=2.5).move_to([4.55, 1.85, 0])
        bp_lbl = T("Blood pressure", size=26, color=TEXT).move_to([4.55, 2.98, 0])

        def mk_bp_fill():
            v = vaso.get_value()
            frac = 0.9 - 0.58 * v
            h = 1.46 * frac
            col = TEAL if v < 0.35 else CRIMSON
            return Rectangle(width=0.40, height=h, stroke_width=0, fill_color=col, fill_opacity=0.88).move_to(
                [4.55, bp_track.get_bottom()[1] + 0.04 + h / 2, 0]
            )

        bp_fill = always_redraw(mk_bp_fill)

        tnf_left = VGroup(*[d for d in tnf_swarm[:7]])
        self.play(
            FadeOut(VGroup(*tnf_swarm[7:])),
            tnf_left.animate.arrange_in_grid(3, 3, buff=0.22).move_to([-3.65, 1.85, 0]),
            FadeIn(vessel), FadeIn(vessel_lbl),
            FadeIn(bp_track), FadeIn(bp_fill), FadeIn(bp_lbl),
            run_time=0.65,
        )
        self.play(
            vaso.animate.set_value(1.0),
            run_time=max(1.2, self.t_of("blood pressure") + 0.9 - self.elapsed()),
            rate_func=linear,
        )
        self.wait(max(0.2, self.t_of("Human sepsis is") - self.elapsed() - 0.15))

        self.at("Human sepsis is")
        scope_note = T("Human sepsis: more complex than endotoxin alone", size=26, color=TEXT).move_to([0, 0.72, 0])
        self.play(FadeIn(scope_note), run_time=0.4)
        self.wait(max(0.5, self.t_of("modified endotoxin fragment") - self.elapsed() - 0.15))

        self.at("modified endotoxin fragment")
        leak_t.clear_updaters()
        center_zone = RoundedRectangle(corner_radius=0.24, width=6.2, height=2.25,
                                       stroke_color=EMERALD, stroke_width=2.5,
                                       fill_color=EMERALD, fill_opacity=0.16).move_to([0, 1.95, 0])
        center_lbl = boxed_label("Controlled vaccine adjuvant", EMERALD, size=28).move_to([0, 1.42, 0])
        amber_dot = Dot([0, 2.65, 0], radius=0.14, color=AMBER)
        # Clear sepsis scene elements FIRST so they never overlap controlled adjuvant mid-fade
        self.play(FadeOut(VGroup(vessel, vessel_lbl, bp_track, bp_fill, bp_lbl, scope_note, right_lbl, tnf_left, tnf_tag)), run_time=0.4)
        self.play(
            tilt.animate.set_value(0.0),
            FadeIn(center_zone), FadeIn(center_lbl), FadeIn(amber_dot),
            run_time=max(1.0, self.t_of("helps vaccines work") - self.elapsed() - 0.15),
        )

        self.at("helps vaccines work")
        self.play(amber_dot.animate.move_to(center_lbl.get_top() + UP * 0.58), run_time=0.4)
        for _ in range(2):
            pulse_ring = Circle(radius=0.22, color=EMERALD, stroke_width=5).move_to(amber_dot.get_center())
            self.add(pulse_ring)
            self.play(pulse_ring.animate.scale(2.2).set_stroke(opacity=0.0), run_time=0.8)
            self.remove(pulse_ring)
        self.finish()


# ------------------------------------------------------------------ S10: Scope & Wide Summary
class S10Wrap(SpokenScene):
    def construct(self):
        dna = dna_strand(center=[0, -1.35, 0], width=6.4, amp=0.24, cycles=3.0, color=PURPLE)
        dna_lbl = T("DNA", size=26, color=PURPLE).next_to(dna, DOWN, buff=0.2)
        nf = nfkb_dimer(scale=1.35, label="NF-κB").move_to([0, -0.35, 0])

        tnfr_chip = boxed_label("TNFR1: immediate brake on death", TEAL, size=24).move_to([-3.3, 2.15, 0])
        cyto_chip = boxed_label("Cytosolic alarms: next in text", TEXT, size=24).move_to([3.3, 2.15, 0])

        # Gentle living pulse on NF-κB + DNA from 0s
        self.add(dna, dna_lbl, nf)
        self.play(Indicate(nf, color=EMERALD, scale_factor=1.05),
                  run_time=max(0.8, self.t_of("TNF receptor") - self.elapsed() - 0.15))

        self.at("TNF receptor")
        self.play(FadeIn(tnfr_chip, shift=DOWN * 0.1), run_time=0.45)
        self.play(Indicate(tnfr_chip, color=TEAL, scale_factor=1.04),
                  run_time=max(0.6, self.t_of("cytosolic sensors") - self.elapsed() - 0.15))

        self.at("cytosolic sensors")
        self.play(FadeIn(cyto_chip, shift=DOWN * 0.1), run_time=0.45)
        self.play(Indicate(cyto_chip, color=TEXT, scale_factor=1.04),
                  run_time=max(0.6, self.t_of("canonical") - self.elapsed() - 0.15))

        self.at("canonical")
        canon_lbl = T("Canonical TLR signaling", size=30, color=TEXT, weight=BOLD).move_to([0, 2.95, 0])
        self.play(FadeOut(tnfr_chip), FadeOut(cyto_chip), run_time=0.4)
        self.play(
            dna.animate.shift(DOWN * 0.4),
            dna_lbl.animate.shift(DOWN * 0.4),
            nf.animate.scale(0.9).shift(DOWN * 0.45),
            FadeIn(canon_lbl),
            run_time=max(0.8, self.t_of("drives survival") - self.elapsed() - 0.15),
        )

        self.at("drives survival")
        def_box = boxed_label("Defense", AMBER, size=32).move_to([-4.0, 1.05, 0])
        surv_box = boxed_label("Survival", EMERALD, size=32).move_to([0.0, 1.35, 0])
        brk_box = boxed_label("Brakes", CORAL, size=32).move_to([4.0, 1.05, 0])

        a_def = Arrow(nf.get_top() + LEFT * 0.35 + UP * 0.06, def_box.get_bottom() + DOWN * 0.08,
                      color=AMBER, stroke_width=5.5, buff=0.05)
        a_surv = Arrow(nf.get_top() + UP * 0.06, surv_box.get_bottom() + DOWN * 0.08,
                       color=EMERALD, stroke_width=5.5, buff=0.05)
        a_brk = Arrow(nf.get_top() + RIGHT * 0.35 + UP * 0.06, brk_box.get_bottom() + DOWN * 0.08,
                      color=CORAL, stroke_width=5.5, buff=0.05)

        self.play(FadeIn(def_box), FadeIn(surv_box), FadeIn(brk_box), run_time=0.45)
        self.play(GrowArrow(a_def), GrowArrow(a_surv), GrowArrow(a_brk), run_time=1.0)
        d1 = Dot(a_def.get_start(), radius=0.11, color=AMBER)
        d2 = Dot(a_surv.get_start(), radius=0.11, color=EMERALD)
        d3 = Dot(a_brk.get_start(), radius=0.11, color=CORAL)
        self.add(d1, d2, d3)
        self.play(
            d1.animate.move_to(a_def.get_end()),
            d2.animate.move_to(a_surv.get_end()),
            d3.animate.move_to(a_brk.get_end()),
            run_time=max(0.8, self.t_of("spares the host") - self.elapsed() - 0.15),
        )
        self.remove(d1, d2, d3)

        self.at("spares the host")
        halo_ring = RoundedRectangle(corner_radius=0.35, width=11.4, height=5.2,
                                     stroke_color=EMERALD, stroke_width=4.5,
                                     fill_color=EMERALD, fill_opacity=0.12).move_to([0, -0.15, 0])
        spare_lbl = T("Protection balanced against host injury", size=28, color=EMERALD).move_to([0, -3.22, 0])
        self.play(FadeIn(spare_lbl), run_time=0.4)
        self.play(Create(halo_ring), run_time=max(0.6, self.narration_s - self.elapsed() - 0.05))
        self.finish()


# ------------------------------------------------------------------ S11: End Card
class S11End(EndCard):
    LINE = "NF-κB drives defense, survival and brakes, balancing protection against host injury."
