"""An Alarm Held Ready — Innate Immunity: Toll-like Receptors and NF-κB.

COLOUR MAP (one colour per concept across the entire film):
- AMBER   (#F5A623): microbial patterns (bacteria, outer coat fragments, nucleic acids, endotoxin)
- TEAL    (#2EC4B6): Toll-like receptors (TLRs) and their kinase relay (MyD88, IRAKs, TRAF6, TAK1, IKK)
- SKY     (#66B2FF): lysine-63 (K63) ubiquitin scaffold chains
- CORAL   (#FC6B5E): inhibitors (IκB), destruction tags (K48 chains), and blocked/OFF states
- EMERALD (#57CC78): NF-κB gene switch
- PURPLE  (#B388FF): nucleus, nuclear pores, nuclear entry tag, and target DNA
- GREY    (#8B93A1): cell boundaries (plasma membrane, endosome, proteasome barrel, structural labels)

ONE CARRIED WORLD:
A macrophage cross-section with a curved plasma membrane across the top, an endosome bubble on the
left, cytosol across the center, and a purple nucleus with nuclear pores and target DNA at the bottom.
Scenes zoom into the active region (surface/endosome, cytosol clamp, receptor-tower junction, K63
scaffold, proteasome shredder, nuclear pores) and pull back to the whole cell for predict/reveal/wrap.

WHAT CHANGES PER SPOKEN SCENE (and what it is computed from):
- s00_hook:     An amber bacterium glides along a quadratic Bezier path toward the top membrane while
                a clock dial hand sweeps linearly across 360 degrees and DNA signal rings expand.
- s02_patterns: Three microbial fragments drift along computed trajectories to surface teal horseshoes;
                inside the endosome, a bacterium drifts, splits into two capsule halves, and sinusoidal
                nucleic acid strands uncoil onto inward-facing horseshoes.
- s03_waiting:  Folded emerald NF-κB bobs gently in the cytosol while a coral IκB clamp closes over its
                purple nuclear key-tab; periodic dashed arrows travel toward the pore and bounce back.
- s04_tower:    Amber endotoxin drifts onto two teal TLR4/MD-2 horseshoes, pulling them inward to pair
                their TIR tails; MyD88 and IRAK blocks assemble along a 3D-projected helix and bright
                activation rings ripple sequentially along the stack.
- s05_scaffold: Active IRAK pulses while TRAF6 docks and spins out a 10-bead K63 ubiquitin chain along
                a computed sine-arch; TAK1 and IKK glide in above the chain and an activation spark arcs
                parabolically from TAK1 onto IKK.
- s06_destroy:  Lit IKK glides to IκB and stamps two phosphate marks; an E3 enzyme attaches a 6-bead
                coral K48 chain; a proteasome barrel draws IκB in and emits RNG-seeded shredded coral
                fragments, unveiling the glowing purple nuclear tag.
- s07_predict:  Mutant NF-κB loses its nuclear tag (dashed outline + coral X); endotoxin docks on top
                receptors, IκB shreds away, and the mutant bobs over the nucleus as the question lands.
- s09_reveal:   Tagless mutant NF-κB drops to the left nuclear pore and rebounds twice; normal NF-κB
                with its purple tag glides through the right pore onto DNA, radiating concentric waves.
- s10_wrap:     A propagating relay halo highlights each step from surface receptor to DNA while gene
                waves radiate continuously and an endosomal TLR3 branch highlights briefly.
"""
import numpy as np
from bp_parts import *

# ------------------------------------------------------------------ concept palette
AMBER = "#F5A623"       # microbial patterns
TEAL = "#2EC4B6"        # Toll-like receptors and kinase relay
SKY = "#66B2FF"         # K63 ubiquitin scaffold
CORAL = "#FC6B5E"       # IκB inhibitor, K48 destruction tag, blocked state
EMERALD = "#57CC78"     # NF-κB transcription factor
PURPLE = "#B388FF"      # nucleus, nuclear pores, nuclear entry tag, target DNA
CYTO_FILL = "#202A3C"   # rich dark slate-navy cytoplasm (distinct from BG, high contrast for all colours)
MEMB_COLOR = "#7D8CA3"  # lipid bilayer border


# ------------------------------------------------------------------ shared geometry builders
def make_horseshoe(color=TEAL, scale=1.0, facing=DOWN, with_tail=True, with_md2=False):
    """Schematic Toll-like receptor: curved horseshoe ectodomain + transmembrane stem + inner TIR tail."""
    ect = Arc(radius=0.38 * scale, start_angle=-0.2 * PI, angle=1.4 * PI,
              stroke_color=color, stroke_width=8 * scale)
    ect.move_to(UP * 0.28 * scale)
    g = VGroup(ect)
    if with_md2:
        md2 = RoundedRectangle(corner_radius=0.09 * scale, width=0.26 * scale, height=0.22 * scale,
                               stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.4)
        md2.move_to(ect.get_center() + DOWN * 0.02 * scale)
        g.add(md2)
    if with_tail:
        stem = Line(UP * 0.02 * scale, DOWN * 0.34 * scale, color=color, stroke_width=5 * scale)
        tir = RoundedRectangle(corner_radius=0.08 * scale, width=0.28 * scale, height=0.26 * scale,
                               stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.34)
        tir.move_to(DOWN * 0.46 * scale)
        g.add(stem, tir)
        g.tir = tir
        g.stem = stem
    g.ect = ect
    if np.allclose(facing, UP):
        g.rotate(PI)
    elif np.allclose(facing, LEFT):
        g.rotate(PI / 2)
    elif np.allclose(facing, RIGHT):
        g.rotate(-PI / 2)
    return g


def make_bacterium(scale=1.0, color=AMBER):
    """Schematic capsule bacterium with short surface coat protrusions (no molecular structures)."""
    body = RoundedRectangle(corner_radius=0.24 * scale, width=0.95 * scale, height=0.44 * scale,
                            stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.38)
    bumps = VGroup()
    for dx in (-0.28, 0.0, 0.28):
        for sgn in (-1, 1):
            bumps.add(Dot(radius=0.048 * scale, color=color).move_to([dx * scale, sgn * 0.24 * scale, 0]))
    tail = VMobject(stroke_color=color, stroke_width=3.2 * scale)
    pts = [np.array([-0.48 * scale - 0.14 * i * scale, 0.07 * scale * np.sin(i * 1.8), 0]) for i in range(6)]
    tail.set_points_smoothly(pts)
    return VGroup(body, bumps, tail)


def make_dna_bar(width=2.6, height=0.34, color=PURPLE):
    """Stylized double-strand DNA segment (two intertwined sinusoidal ribbons + rungs)."""
    xs = np.linspace(-width / 2, width / 2, 48)
    y1 = 0.5 * height * np.sin(2.4 * PI * xs / width)
    y2 = -y1
    s1 = VMobject(stroke_color=color, stroke_width=4.5).set_points_smoothly([np.array([x, y, 0]) for x, y in zip(xs, y1)])
    s2 = VMobject(stroke_color=color, stroke_width=4.5).set_points_smoothly([np.array([x, y, 0]) for x, y in zip(xs, y2)])
    rungs = VGroup()
    for i in range(4, 46, 5):
        rungs.add(Line([xs[i], y1[i], 0], [xs[i], y2[i], 0], color=color, stroke_width=2.2).set_opacity(0.7))
    return VGroup(rungs, s1, s2)


def make_macrophage_world(show_endosome=True, endo_r=1.05, nuc_center=(0.0, -2.15, 0), nuc_w=4.8, nuc_h=1.85,
                          pores=True):
    """Carried cross-section of the macrophage: plasma membrane arch, cytoplasm, endosome, purple nucleus."""
    xs = np.linspace(-6.0, 6.0, 60)
    ys_outer = 2.45 - 0.030 * xs ** 2
    ys_inner = ys_outer - 0.18
    cyto_pts = [np.array([x, y, 0]) for x, y in zip(xs, ys_inner)]
    cyto_pts += [np.array([6.0, -3.3, 0]), np.array([-6.0, -3.3, 0])]
    cyto = Polygon(*cyto_pts, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.9)
    memb_out = VMobject(stroke_color=MEMB_COLOR, stroke_width=4.5).set_points_smoothly(
        [np.array([x, y, 0]) for x, y in zip(xs, ys_outer)]
    )
    memb_in = VMobject(stroke_color=MEMB_COLOR, stroke_width=2.5).set_points_smoothly(
        [np.array([x, y, 0]) for x, y in zip(xs, ys_inner)]
    )
    membrane = VGroup(memb_out, memb_in)

    nc = np.array(nuc_center, dtype=float)
    nuc_body = Ellipse(width=nuc_w, height=nuc_h, stroke_color=PURPLE, stroke_width=4.5,
                       fill_color=PURPLE, fill_opacity=0.22).move_to(nc)
    dna = make_dna_bar(width=nuc_w * 0.52, height=0.32, color=PURPLE).move_to(nc + DOWN * 0.06)
    nuc_group = VGroup(nuc_body, dna)

    if pores:
        pore_group = VGroup()
        for px in (-1.2, 1.2):
            p_pos = nc + np.array([px, nuc_h * 0.44 * np.sqrt(max(0.1, 1 - (px / (nuc_w / 2)) ** 2)), 0])
            gap = Rectangle(width=0.56, height=0.24, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=1.0).move_to(p_pos)
            rim_l = Line(p_pos + LEFT * 0.28 + UP * 0.11, p_pos + LEFT * 0.28 + DOWN * 0.11, color=PURPLE, stroke_width=4.5)
            rim_r = Line(p_pos + RIGHT * 0.28 + UP * 0.11, p_pos + RIGHT * 0.28 + DOWN * 0.11, color=PURPLE, stroke_width=4.5)
            pore_group.add(gap, rim_l, rim_r)
        nuc_group.add(pore_group)

    endo = VGroup()
    if show_endosome:
        ec = np.array([-3.45, -0.05, 0.0])
        e_out = Circle(radius=endo_r, stroke_color=MEMB_COLOR, stroke_width=3.8,
                       fill_color=BG, fill_opacity=0.72).move_to(ec)
        e_in = Circle(radius=endo_r - 0.1, stroke_color=MEMB_COLOR, stroke_width=2.0).move_to(ec)
        endo.add(e_out, e_in)

    world = VGroup(cyto, membrane, endo, nuc_group)
    world.cyto = cyto
    world.membrane = membrane
    world.memb_y = lambda x: 2.45 - 0.030 * x ** 2
    world.endosome = endo
    world.endo_center = np.array([-3.45, -0.05, 0.0])
    world.nucleus = nuc_group
    world.nuc_body = nuc_body
    world.dna = dna
    return world


def make_nfkb(scale=1.0, has_tag=True, mutant_empty_tag=False):
    """Paired emerald NF-κB dimer with a notched purple nuclear entry key-tab."""
    lobe_l = RoundedRectangle(corner_radius=0.35 * scale, width=1.18 * scale, height=0.98 * scale,
                              stroke_color=EMERALD, stroke_width=4, fill_color=EMERALD, fill_opacity=0.38)
    lobe_r = RoundedRectangle(corner_radius=0.35 * scale, width=1.18 * scale, height=0.98 * scale,
                              stroke_color=EMERALD, stroke_width=4, fill_color=EMERALD, fill_opacity=0.30)
    lobe_l.shift(LEFT * 0.45 * scale)
    lobe_r.shift(RIGHT * 0.45 * scale)
    dimer = VGroup(lobe_l, lobe_r)

    tag = VGroup()
    if has_tag:
        stem = RoundedRectangle(corner_radius=0.08 * scale, width=0.52 * scale, height=0.32 * scale,
                                stroke_color=PURPLE, stroke_width=3.2, fill_color=PURPLE,
                                fill_opacity=0.10 if mutant_empty_tag else 0.65)
        notch = Triangle(stroke_color=PURPLE, stroke_width=3.2, fill_color=PURPLE,
                         fill_opacity=0.10 if mutant_empty_tag else 0.65).scale(0.16 * scale).rotate(-PI / 2)
        stem.next_to(lobe_r, RIGHT, buff=-0.04 * scale).shift(DOWN * 0.08 * scale)
        notch.next_to(stem, RIGHT, buff=-0.03 * scale)
        if mutant_empty_tag:
            stem = DashedVMobject(stem, num_dashes=10)
            notch = DashedVMobject(notch, num_dashes=6)
            x_center = stem.get_center() + RIGHT * 0.08 * scale
            cross = VGroup(
                Line(x_center + UL * 0.22 * scale, x_center + DR * 0.22 * scale, color=CORAL, stroke_width=5.5),
                Line(x_center + UR * 0.22 * scale, x_center + DL * 0.22 * scale, color=CORAL, stroke_width=5.5),
            )
            tag.add(stem, notch, cross)
        else:
            glow = SurroundingRectangle(VGroup(stem, notch), corner_radius=0.12 * scale, buff=0.06 * scale,
                                        stroke_color=PURPLE, stroke_width=2.5, stroke_opacity=0.7,
                                        fill_color=PURPLE, fill_opacity=0.0)
            tag.add(stem, notch, glow)

    g = VGroup(dimer, tag)
    g.dimer = dimer
    g.tag = tag
    return g


def set_tag_visibility(tag_group, fill_op, stroke_op=1.0):
    """Adjust tag fill/stroke without ever filling the outer glow rectangle."""
    if len(tag_group) >= 2:
        tag_group[0].set_fill(PURPLE, opacity=fill_op).set_stroke(PURPLE, opacity=stroke_op)
        tag_group[1].set_fill(PURPLE, opacity=fill_op).set_stroke(PURPLE, opacity=stroke_op)
    if len(tag_group) >= 3:
        tag_group[2].set_fill(opacity=0.0).set_stroke(PURPLE, opacity=0.7 * stroke_op)


def make_ikb_clamp(scale=1.0, closed=True):
    """Curved coral C-clamp shaped to wrap around NF-κB and cover its purple nuclear tag."""
    if closed:
        arc = Arc(radius=1.22 * scale, start_angle=-0.42 * PI, angle=1.55 * PI,
                  stroke_color=CORAL, stroke_width=24 * scale)
        cap_top = Dot(arc.get_start(), radius=0.14 * scale, color=CORAL)
        cap_bot = Dot(arc.get_end(), radius=0.14 * scale, color=CORAL)
        shield = RoundedRectangle(corner_radius=0.14 * scale, width=0.58 * scale, height=0.88 * scale,
                                  stroke_color=CORAL, stroke_width=3.2, fill_color=CORAL, fill_opacity=0.52)
        shield.move_to([1.18 * scale, -0.08 * scale, 0])
        g = VGroup(arc, cap_top, cap_bot, shield)
        g.shield = shield
    else:
        arc = Arc(radius=1.35 * scale, start_angle=0.15 * PI, angle=1.2 * PI,
                  stroke_color=CORAL, stroke_width=22 * scale)
        g = VGroup(arc)
    return g


def make_ubiquitin_chain(points, color=SKY, bead_r=0.20):
    """Chain of linked oval ubiquitin beads along a sequence of 3D points."""
    links = VGroup()
    beads = VGroup()
    for i, p in enumerate(points):
        b = Ellipse(width=bead_r * 2.25, height=bead_r * 1.55, stroke_color=TEXT, stroke_width=2.2,
                    fill_color=color, fill_opacity=0.9).move_to(p)
        if i > 0:
            d = p - points[i - 1]
            b.rotate(np.arctan2(d[1], d[0]))
            links.add(Line(points[i - 1], p, color=color, stroke_width=6))
        beads.add(b)
    return VGroup(links, beads)


def make_timer_dial(center=(4.75, 1.85, 0), radius=0.72, progress_tracker=None, label_text="Minutes"):
    """Analog minute dial driven by progress_tracker (0..1 -> 0..360 deg)."""
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, stroke_color=TEAL, stroke_width=4, fill_color=CYTO_FILL, fill_opacity=0.95).move_to(c)
    ticks = VGroup()
    for k in range(12):
        ang = PI / 2 - k * TAU / 12
        r_in = radius * (0.76 if k % 3 == 0 else 0.84)
        ticks.add(Line(c + r_in * np.array([np.cos(ang), np.sin(ang), 0]),
                       c + radius * 0.94 * np.array([np.cos(ang), np.sin(ang), 0]),
                       color=GREY, stroke_width=2.5 if k % 3 == 0 else 1.5))
    center_dot = Dot(c, radius=0.055, color=TEXT)
    lab = T(label_text, size=28, color=TEXT).next_to(rim, DOWN, buff=0.16)
    g = VGroup(rim, ticks, center_dot, lab)
    if progress_tracker is not None:
        sweep = always_redraw(lambda: Sector(
            radius=radius * 0.72, start_angle=PI / 2,
            angle=-max(0.01, progress_tracker.get_value()) * TAU,
            arc_center=c, fill_color=TEAL, fill_opacity=0.28, stroke_width=0
        ))
        hand = always_redraw(lambda: Line(
            c, c + radius * 0.68 * np.array([
                np.cos(PI / 2 - progress_tracker.get_value() * TAU),
                np.sin(PI / 2 - progress_tracker.get_value() * TAU), 0
            ]), color=TEXT, stroke_width=4.5
        ))
        g.add(sweep, hand)
    return g


# ------------------------------------------------------------------ scenes
class S00Hook(SpokenScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=0.95)
        lbl_mac = T("Macrophage", size=30, color=TEXT).move_to([-4.35, 2.85, 0])
        # Keep Nucleus label well clear of the DNA activation wave inside the nucleus
        lbl_nuc = T("Nucleus", size=28, color=PURPLE).move_to([-3.55, -2.35, 0])

        t_prog = ValueTracker(0.0)
        dial_g = make_timer_dial(center=(4.7, 1.9, 0), radius=0.7, progress_tracker=t_prog, label_text="Minutes")

        p0 = np.array([-2.5, 3.45, 0.0])
        p1 = np.array([-1.2, 3.45, 0.0])
        p2 = np.array([0.35, 2.74, 0.0])
        bact_t = ValueTracker(0.0)

        def get_bact():
            u = bact_t.get_value()
            pos = (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u ** 2 * p2
            deriv = 2 * (1 - u) * (p1 - p0) + 2 * u * (p2 - p1)
            ang = np.arctan2(deriv[1], deriv[0])
            return make_bacterium(scale=0.92, color=AMBER).rotate(ang).move_to(pos)

        bact = always_redraw(get_bact)
        surf_tlr = make_horseshoe(TEAL, scale=0.85, facing=DOWN).move_to([0.45, 2.38, 0])

        self.play(FadeIn(world), FadeIn(surf_tlr), FadeIn(lbl_mac), FadeIn(lbl_nuc), FadeIn(dial_g), run_time=0.85)
        self.add(bact)

        self.play(bact_t.animate.set_value(0.42), t_prog.animate.set_value(0.30),
                  run_time=max(0.4, self.t_of("defense genes") - self.elapsed() - 0.2), rate_func=linear)

        self.at("defense genes")
        sig_path = DashedVMobject(
            ArcBetweenPoints([0.45, 1.75, 0], [0.0, -1.35, 0], angle=-0.35), num_dashes=10, color=TEAL
        ).set_stroke(width=4)
        self.play(Create(sig_path), bact_t.animate.set_value(0.62), t_prog.animate.set_value(0.48),
                  run_time=max(0.4, self.t_of("Antibodies take days") - self.elapsed() - 0.2), rate_func=linear)

        self.at("Antibodies take days")
        self.play(bact_t.animate.set_value(0.88), t_prog.animate.set_value(0.75),
                  run_time=max(0.4, self.t_of("starts changing") - self.elapsed() - 0.2), rate_func=linear)

        self.at("starts changing")
        wave_r = ValueTracker(0.0)
        dna_wave = always_redraw(lambda: Ellipse(
            width=2.4 + 1.6 * wave_r.get_value(), height=0.55 + 0.65 * wave_r.get_value(),
            stroke_color=EMERALD, stroke_width=4.5, stroke_opacity=max(0.0, 1.0 - wave_r.get_value())
        ).move_to(world.dna.get_center()))
        self.add(dna_wave)
        self.play(
            bact_t.animate.set_value(1.0),
            t_prog.animate.set_value(1.0),
            wave_r.animate.set_value(1.0),
            world.dna.animate.set_color(EMERALD),
            run_time=max(0.6, self.narration_s - self.elapsed() - 0.1),
            rate_func=linear,
        )
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=0.95)
        surf_tlr = make_horseshoe(TEAL, scale=0.85, facing=DOWN).move_to([0.45, 2.38, 0])
        world_g = VGroup(world, surf_tlr)

        bact_t = ValueTracker(0.0)
        bact = always_redraw(lambda: make_bacterium(scale=0.92, color=AMBER).move_to(
            [0.35 + 0.6 * bact_t.get_value(), 2.74 - 0.04 * bact_t.get_value(), 0]
        ))

        dim = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=0.55)

        # Placed cleanly in open center-right cytoplasm away from membrane, receptor, endosome and nucleus
        title = T("An Alarm Held Ready", size=48, font=TITLE_FONT, color=TEXT).move_to([1.25, 0.45, 0])
        rule = Line(LEFT * 1.8, RIGHT * 1.8, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.18)
        title_g = VGroup(title, rule)

        self.add(world_g, dim, bact)
        self.play(FadeIn(title_g, shift=DOWN * 0.2), bact_t.animate.set_value(0.35), run_time=0.45)
        self.play(bact_t.animate.set_value(0.75), run_time=0.95, rate_func=linear)
        self.play(FadeOut(title_g, shift=UP * 0.15), FadeOut(dim),
                  bact_t.animate.set_value(1.0), run_time=0.55)
        self.finish()


class S02Patterns(SpokenScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=1.5)
        world.endosome.move_to([-3.35, -0.05, 0])
        endo_c = world.endosome.get_center()
        self.add(world)

        xs_surf = [-2.1, 0.45, 3.0]
        surf_tlrs = VGroup(*[
            make_horseshoe(TEAL, scale=0.92, facing=DOWN).move_to([x, world.memb_y(x) - 0.05, 0])
            for x in xs_surf
        ])

        # Swallowed amber bacterium drifting continuously inside the endosome from the start
        bact_t = ValueTracker(0.0)
        bact_in = always_redraw(lambda: make_bacterium(scale=0.72, color=AMBER).rotate(
            0.18 * np.sin(bact_t.get_value() * TAU)
        ).move_to(endo_c + np.array([0.28 * np.sin(bact_t.get_value() * TAU), 0.14 * np.cos(bact_t.get_value() * TAU), 0])))
        self.add(bact_in)

        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.18) for t in surf_tlrs], lag_ratio=0.18),
            bact_t.animate.set_value(0.45),
            run_time=max(1.2, self.t_of("Each receptor") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Shared microbial molecules drifting smoothly along computed paths to receptors
        self.at("Each receptor")
        frag_coat = RoundedRectangle(corner_radius=0.12, width=0.66, height=0.28, stroke_color=AMBER, stroke_width=3.5,
                                     fill_color=AMBER, fill_opacity=0.75)
        frag_lipid = Polygon([-0.3, -0.13, 0], [0.3, -0.13, 0], [0.18, 0.16, 0], [-0.18, 0.16, 0],
                             stroke_color=AMBER, stroke_width=3.5, fill_color=AMBER, fill_opacity=0.75)
        frag_rod = RoundedRectangle(corner_radius=0.11, width=0.72, height=0.22, stroke_color=AMBER, stroke_width=3.5,
                                    fill_color=AMBER, fill_opacity=0.75)

        starts = [np.array([-4.4, 3.25, 0]), np.array([0.0, 3.35, 0]), np.array([4.6, 3.15, 0])]
        ends = [surf_tlrs[i].ect.get_center() + UP * 0.25 for i in range(3)]
        frag_t = ValueTracker(0.0)

        def make_moving_frag(proto, p_a, p_b, phase):
            def _mk():
                u = frag_t.get_value()
                pos = (1 - u) * p_a + u * p_b + UP * 0.18 * np.sin(u * PI * 2 + phase)
                return proto.copy().move_to(pos)
            return always_redraw(_mk)

        m_frags = VGroup(
            make_moving_frag(frag_coat, starts[0], ends[0], 0.0),
            make_moving_frag(frag_lipid, starts[1], ends[1], 1.2),
            make_moving_frag(frag_rod, starts[2], ends[2], 2.4),
        )
        self.add(m_frags)
        self.play(
            frag_t.animate.set_value(0.85),
            bact_t.animate.set_value(1.25),
            run_time=max(1.0, self.t_of("outer coats") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Dock into surface horseshoes + label
        self.at("outer coats")
        lbl_surf = T("Surface: outer coats", size=30, color=TEAL).move_to([3.45, 0.75, 0])
        self.play(
            frag_t.animate.set_value(1.0),
            bact_t.animate.set_value(1.75),
            *[t.tir.animate.set_fill(TEAL, opacity=0.9) for t in surf_tlrs],
            FadeIn(lbl_surf, shift=UP * 0.1),
            run_time=max(1.2, self.t_of("nucleic acids") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Endosome: inward-facing teal horseshoes + microbial nucleic acids
        self.at("nucleic acids")
        endo_tlr_l = make_horseshoe(TEAL, scale=0.66, facing=LEFT, with_tail=True).move_to(endo_c + RIGHT * 1.15 + UP * 0.38)
        endo_tlr_r = make_horseshoe(TEAL, scale=0.66, facing=RIGHT, with_tail=True).move_to(endo_c + LEFT * 1.15 + DOWN * 0.38)
        endo_tlrs = VGroup(endo_tlr_l, endo_tlr_r)
        lbl_endo = T("Endosome: nucleic acids", size=28, color=AMBER).next_to(world.endosome, RIGHT, buff=0.35).shift(DOWN * 0.45)

        self.play(
            FadeIn(endo_tlrs),
            FadeIn(lbl_endo, shift=LEFT * 0.1),
            bact_t.animate.set_value(2.25),
            run_time=max(1.2, self.t_of("swallowed microbes break open") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Break open into two clear capsule halves and release wavy nucleic acid strands onto horseshoes
        self.at("swallowed microbes break open")
        self.remove(bact_in)
        half_l = RoundedRectangle(corner_radius=0.14, width=0.42, height=0.34, stroke_color=AMBER, stroke_width=3.5,
                                  fill_color=AMBER, fill_opacity=0.45).move_to(endo_c + LEFT * 0.24).rotate(0.3)
        half_r = RoundedRectangle(corner_radius=0.14, width=0.42, height=0.34, stroke_color=AMBER, stroke_width=3.5,
                                  fill_color=AMBER, fill_opacity=0.45).move_to(endo_c + RIGHT * 0.24).rotate(-0.3)

        strand_u = VMobject(stroke_color=AMBER, stroke_width=4.5).set_points_smoothly([
            endo_c + np.array([0.08 * k, 0.11 * np.sin(k * 1.7), 0]) for k in range(9)
        ])
        strand_d = VMobject(stroke_color=AMBER, stroke_width=4.5).set_points_smoothly([
            endo_c + np.array([-0.08 * k, -0.11 * np.sin(k * 1.7), 0]) for k in range(9)
        ])

        self.play(FadeIn(half_l), FadeIn(half_r), run_time=0.45)
        self.play(
            half_l.animate.shift(UL * 0.42 + LEFT * 0.15).rotate(0.4).set_opacity(0.45),
            half_r.animate.shift(DR * 0.42 + RIGHT * 0.15).rotate(-0.4).set_opacity(0.45),
            Create(strand_u),
            Create(strand_d),
            run_time=0.85,
        )
        self.play(
            strand_u.animate.move_to(endo_tlr_l.ect.get_center() + LEFT * 0.08),
            strand_d.animate.move_to(endo_tlr_r.ect.get_center() + RIGHT * 0.08),
            endo_tlr_l.tir.animate.set_fill(TEAL, opacity=0.95),
            endo_tlr_r.tir.animate.set_fill(TEAL, opacity=0.95),
            run_time=max(0.8, self.narration_s - self.elapsed() - 0.1),
        )
        self.finish()


class S03Waiting(SpokenScene):
    def construct(self):
        cyto_bg = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.9)
        nuc_rim = Arc(radius=6.2, start_angle=0.25 * PI, angle=0.5 * PI,
                      stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.22).move_to([0, -2.95, 0])
        pore_gap = Rectangle(width=1.05, height=0.28, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=1.0).move_to([0, -2.26, 0])
        pore_l = Line([-0.52, -2.12, 0], [-0.52, -2.4, 0], color=PURPLE, stroke_width=5)
        pore_r = Line([0.52, -2.12, 0], [0.52, -2.4, 0], color=PURPLE, stroke_width=5)
        lbl_nuc = T("Nucleus", size=28, color=PURPLE).move_to([-4.55, -3.05, 0])
        self.add(cyto_bg, nuc_rim, pore_gap, pore_l, pore_r, lbl_nuc)

        # NF-κB dimer + nuclear entry tag (label placed cleanly above where the IκB clamp will close)
        nfkb = make_nfkb(scale=1.42, has_tag=True).move_to([-0.3, 0.55, 0])
        lbl_nfkb = T("NF-κB", size=34, color=EMERALD).move_to([-0.3, 2.75, 0])
        lbl_tag = T("Nuclear tag", size=28, color=PURPLE).move_to([3.95, 0.42, 0])

        # Fold the two dimer lobes together smoothly while approaching "already built and folded"
        nfkb.dimer[0].shift(LEFT * 0.65)
        nfkb.dimer[1].shift(RIGHT * 0.65)
        self.play(FadeIn(nfkb.dimer), FadeIn(lbl_nfkb), run_time=0.8)
        self.play(
            nfkb.dimer[0].animate.shift(RIGHT * 0.65),
            nfkb.dimer[1].animate.shift(LEFT * 0.65),
            run_time=max(0.8, self.t_of("already built and folded") - self.elapsed() - 0.2),
        )

        self.at("already built and folded")
        tag_ptr = Line(lbl_tag.get_left() + LEFT * 0.1, nfkb.tag.get_right() + RIGHT * 0.12,
                       color=PURPLE, stroke_width=3.5)
        self.play(FadeIn(nfkb.tag, shift=RIGHT * 0.18), FadeIn(lbl_tag), Create(tag_ptr), run_time=0.9)
        # Continuous cytosolic bob while waiting for coral inhibitor
        bob_t = ValueTracker(0.0)
        nfkb_base = nfkb.get_center().copy()
        nfkb.add_updater(lambda m: m.move_to(nfkb_base + UP * 0.10 * np.sin(bob_t.get_value() * TAU)))
        self.play(
            bob_t.animate.set_value(1.5),
            run_time=max(0.8, self.t_of("A coral inhibitor") - self.elapsed() - 0.2),
            rate_func=linear,
        )
        nfkb.clear_updaters()
        nfkb.move_to(nfkb_base)

        # Coral IκB clamp glides in and wraps around NF-κB (clearing lbl_nfkb at y=2.75!)
        self.at("A coral inhibitor")
        clamp_start = make_ikb_clamp(scale=1.42, closed=True).move_to([-4.4, 0.55, 0]).set_opacity(0.0)
        clamp = make_ikb_clamp(scale=1.42, closed=True).move_to([-0.18, 0.55, 0])
        lbl_ikb = T("IκB", size=34, color=CORAL).move_to([-3.0, 0.55, 0])
        clamp_dur = max(0.8, self.t_of("covers its nuclear entry tag") - self.elapsed() - 0.7)
        self.play(ReplacementTransform(clamp_start, clamp), run_time=clamp_dur)
        self.play(FadeIn(lbl_ikb, shift=RIGHT * 0.15), run_time=0.5)

        # Clamp covers nuclear entry tag; pointer stays attached dynamically while complex keeps bobbing & probing
        self.at("covers its nuclear entry tag")
        self.remove(tag_ptr)
        tag_ptr_dyn = always_redraw(lambda: Line(
            lbl_tag.get_left() + LEFT * 0.1, clamp.shield.get_right() + RIGHT * 0.1,
            color=PURPLE, stroke_width=3.5
        ))
        self.add(tag_ptr_dyn)
        c_grp = VGroup(nfkb, clamp)
        c_base = c_grp.get_center().copy()
        self.play(
            nfkb.tag[0].animate.set_fill(PURPLE, opacity=0.22).set_stroke(PURPLE, opacity=0.45),
            nfkb.tag[1].animate.set_fill(PURPLE, opacity=0.22).set_stroke(PURPLE, opacity=0.45),
            nfkb.tag[2].animate.set_fill(opacity=0.0).set_stroke(PURPLE, opacity=0.2),
            clamp.shield.animate.set_fill(CORAL, opacity=0.72),
            run_time=0.8,
        )
        bounce_t = ValueTracker(0.0)
        arrows = always_redraw(lambda: VGroup(*[
            DashedLine(
                [dx, -1.02 - 0.54 * abs(np.sin(bounce_t.get_value() * PI)), 0],
                [dx, -1.72 - 0.44 * abs(np.sin(bounce_t.get_value() * PI)), 0],
                color=EMERALD, stroke_width=4.5
            ).add_tip(tip_length=0.2)
            for dx in (-0.65, 0.0, 0.65)
        ]))
        self.add(arrows)
        c_grp.add_updater(lambda m: m.move_to(c_base + DOWN * 0.18 * abs(np.sin(bounce_t.get_value() * PI))))
        self.play(
            bounce_t.animate.set_value(1.5),
            run_time=max(0.8, self.t_of("holds tight") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        self.at("holds tight")
        self.play(
            bounce_t.animate.set_value(3.5),
            run_time=max(1.0, self.narration_s - self.elapsed() - 0.1),
            rate_func=linear,
        )
        c_grp.clear_updaters()
        self.finish()


class S04Tower(SpokenScene):
    def construct(self):
        cyto_bg = Rectangle(width=14.4, height=5.8, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.9).move_to([0, -0.75, 0])
        memb_top = Line([-6.2, 2.25, 0], [6.2, 2.25, 0], color=MEMB_COLOR, stroke_width=5.5)
        memb_bot = Line([-6.2, 2.00, 0], [6.2, 2.00, 0], color=MEMB_COLOR, stroke_width=3.2)
        self.add(cyto_bg, memb_top, memb_bot)

        # Larger receptors (scale=1.22) + gentle membrane diffusion before endotoxin binds
        tlr_l = make_horseshoe(TEAL, scale=1.22, facing=DOWN, with_tail=True, with_md2=True).move_to([-2.3, 2.08, 0])
        tlr_r = make_horseshoe(TEAL, scale=1.22, facing=DOWN, with_tail=True, with_md2=True).move_to([2.3, 2.08, 0])
        lbl_tlr = T("TLR4 / MD-2", size=28, color=TEAL).move_to([-4.35, 2.95, 0])

        # Cytosolic MyD88/IRAK pieces waiting dispersed below so the lower half isn't empty
        myd88_wait = VGroup(*[
            RoundedRectangle(corner_radius=0.09, width=0.58, height=0.30, stroke_color=TEXT, stroke_width=2,
                             fill_color=TEAL, fill_opacity=0.55).move_to([x, y, 0])
            for x, y in [(-3.2, -0.4), (3.1, -0.55), (-2.1, -1.6), (2.2, -1.75)]
        ])
        self.play(FadeIn(tlr_l), FadeIn(tlr_r), FadeIn(lbl_tlr), FadeIn(myd88_wait), run_time=0.9)
        self.play(
            tlr_l.animate.shift(RIGHT * 0.25),
            tlr_r.animate.shift(LEFT * 0.25),
            myd88_wait[0].animate.shift(UR * 0.25),
            myd88_wait[1].animate.shift(UL * 0.25),
            run_time=max(0.8, self.t_of("bacterial endotoxin") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Amber endotoxin drifts down and bridges the two receptors
        self.at("bacterial endotoxin")
        endo = RoundedRectangle(corner_radius=0.14, width=1.15, height=0.52, stroke_color=AMBER, stroke_width=3.5,
                                fill_color=AMBER, fill_opacity=0.82).move_to([-1.2, 3.35, 0])
        lbl_endo = T("Endotoxin", size=28, color=AMBER).move_to([3.4, 3.25, 0])
        self.play(FadeIn(endo), FadeIn(lbl_endo), run_time=0.6)
        self.play(
            endo.animate.move_to([0, 2.74, 0]),
            run_time=max(1.2, self.t_of("move side by side") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Two teal receptors slide side by side
        self.at("move side by side")
        self.play(
            tlr_l.animate.move_to([-0.64, 2.08, 0]),
            tlr_r.animate.move_to([0.64, 2.08, 0]),
            run_time=max(1.2, self.t_of("inner tails pair") - self.elapsed() - 0.2),
        )

        # Inner tails pair and dock MyD88
        self.at("inner tails pair")
        pair_glow = SurroundingRectangle(VGroup(tlr_l.tir, tlr_r.tir), corner_radius=0.12, buff=0.09,
                                         stroke_color=TEAL, stroke_width=3.5)
        self.play(Create(pair_glow), run_time=0.8)

        self.at("dock an adapter")
        myd88_top = VGroup(*[
            RoundedRectangle(corner_radius=0.09, width=0.58, height=0.30, stroke_color=TEXT, stroke_width=2,
                             fill_color=TEAL, fill_opacity=0.82).move_to([x, 0.92, 0])
            for x in (-0.38, 0.38)
        ])
        lbl_myd88 = T("MyD88", size=28, color=TEAL).move_to([-2.4, 0.92, 0])
        self.play(
            ReplacementTransform(myd88_wait[:2], myd88_top),
            FadeIn(lbl_myd88),
            run_time=max(1.0, self.t_of("stacks with") - self.elapsed() - 0.2),
        )

        # Helical tower of MyD88 + IRAK kinases computed on a 3D helix
        self.at("stacks with")
        layers = []
        n_blocks = 12
        for k in range(n_blocks):
            theta = k * 1.15
            x = 0.62 * np.cos(theta)
            z = np.sin(theta)
            y = 0.52 - 0.29 * k
            is_irak = k >= 4
            op = 0.90 if is_irak else 0.68
            blk = RoundedRectangle(corner_radius=0.09, width=0.60, height=0.27, stroke_color=TEXT,
                                   stroke_width=2.0, fill_color=TEAL, fill_opacity=op).move_to([x, y, 0])
            layers.append((z, k, is_irak, blk))
        layers_sorted = [item[3] for item in sorted(layers, key=lambda t: t[0])]

        lbl_tower = T("MyD88–IRAK tower (schematic)", size=28, color=TEAL).move_to([3.65, -0.6, 0])
        lbl_irak = T("IRAK kinases", size=28, color=TEAL).move_to([-2.8, -1.35, 0])

        self.play(FadeOut(myd88_wait[2:]), run_time=0.25)
        self.play(
            LaggedStart(*[FadeIn(item[3], shift=UP * 0.25) for item in layers], lag_ratio=0.14),
            FadeIn(lbl_irak),
            FadeIn(lbl_tower),
            run_time=max(1.5, self.t_of("activate one another") - self.elapsed() - 0.25),
        )

        # Bright activation pulses rippling between neighboring IRAK blocks
        self.at("activate one another")
        irak_blocks = [item[3] for item in layers if item[2]]
        pulse_t = ValueTracker(0.0)
        sparks = always_redraw(lambda: VGroup(*[
            Circle(radius=0.20 + 0.10 * np.sin(pulse_t.get_value() * TAU - i * 0.8),
                   stroke_color=TEXT, stroke_width=4,
                   stroke_opacity=0.35 + 0.65 * max(0.0, np.sin(pulse_t.get_value() * TAU - i * 0.8))
                   ).move_to(b.get_center())
            for i, b in enumerate(irak_blocks)
        ]))
        self.add(sparks)
        self.play(pulse_t.animate.set_value(2.4), run_time=max(1.0, self.narration_s - self.elapsed() - 0.1),
                  rate_func=linear)
        self.finish()


class S05Scaffold(SpokenScene):
    def construct(self):
        cyto_bg = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.9)
        self.add(cyto_bg)

        # Lower end of active IRAK tower at upper-left, pulsing continuously
        tower_tail = VGroup()
        for k in range(5):
            theta = (k + 6) * 1.15
            x = -4.5 + 0.52 * np.cos(theta)
            y = 2.45 - 0.28 * k
            blk = RoundedRectangle(corner_radius=0.09, width=0.58, height=0.26, stroke_color=TEXT,
                                   stroke_width=2.0, fill_color=TEAL, fill_opacity=0.88).move_to([x, y, 0])
            tower_tail.add(blk)
        # Put Active IRAK label cleanly ABOVE tower_tail so TAK1 gliding in can never touch it!
        lbl_irak = T("Active IRAK", size=28, color=TEAL).move_to([-4.5, 3.05, 0])

        irak_pulse = ValueTracker(0.0)
        irak_rings = always_redraw(lambda: VGroup(*[
            Circle(radius=0.18 + 0.08 * np.sin(irak_pulse.get_value() * TAU - i * 0.9),
                   stroke_color=TEXT, stroke_width=3.2,
                   stroke_opacity=0.3 + 0.65 * max(0.0, np.sin(irak_pulse.get_value() * TAU - i * 0.9))
                   ).move_to(b.get_center())
            for i, b in enumerate(tower_tail)
        ]))

        traf6_box = RoundedRectangle(corner_radius=0.14, width=1.65, height=0.82, stroke_color=TEAL, stroke_width=3.5,
                                     fill_color=TEAL, fill_opacity=0.42)
        traf6 = VGroup(traf6_box, T("TRAF6", size=30, color=TEAL).move_to(traf6_box)).move_to([-4.5, -2.1, 0])

        self.play(FadeIn(tower_tail), FadeIn(lbl_irak), FadeIn(traf6), run_time=0.85)
        self.add(irak_rings)
        # TRAF6 glides smoothly upward toward IRAK tail while narrator introduces ubiquitin
        self.play(
            traf6.animate.move_to([-4.5, 0.2, 0]),
            irak_pulse.animate.set_value(2.0),
            run_time=max(1.2, self.t_of("engages") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # TRAF6 docks directly onto the activated IRAK
        self.at("engages")
        self.play(
            traf6.animate.move_to([-4.5, 0.65, 0]),
            irak_pulse.animate.set_value(3.2),
            run_time=max(1.0, self.t_of("sky blue") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Growing 10-bead sky-blue K63 ubiquitin scaffold sweeping across the frame
        self.at("sky blue")
        n_beads = 10
        xs = np.linspace(-3.3, 4.6, n_beads)
        ys = -0.15 + 0.68 * np.sin((xs + 3.3) * 0.46)
        chain_pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        k63_chain = make_ubiquitin_chain(chain_pts, color=SKY, bead_r=0.22)
        lbl_k63 = T("K63 scaffold", size=32, color=SKY).move_to([0.65, -1.35, 0])

        links, beads = k63_chain[0], k63_chain[1]
        anims = [FadeIn(beads[0], scale=0.6)]
        for i in range(1, n_beads):
            anims.append(AnimationGroup(Create(links[i - 1]), FadeIn(beads[i], scale=0.6)))
        self.play(
            LaggedStart(*anims, lag_ratio=0.22),
            FadeIn(lbl_k63, shift=UP * 0.1),
            irak_pulse.animate.set_value(5.5),
            run_time=max(1.8, self.t_of("destroys nothing") - self.elapsed() - 0.2),
        )

        self.at("destroys nothing")
        check_note = T("Platform — not destroyed", size=28, color=SKY).next_to(lbl_k63, DOWN, buff=0.25)
        self.play(FadeIn(check_note), irak_pulse.animate.set_value(6.5), run_time=1.0)

        # TAK1 and IKK complexes (docking feet reach directly down onto the K63 beads!)
        self.at("acts as a scaffold")
        tak1_box = RoundedRectangle(corner_radius=0.16, width=1.85, height=0.88, stroke_color=TEAL, stroke_width=3.5,
                                    fill_color=TEAL, fill_opacity=0.35)
        tak1_foot = Line([0, -0.44, 0], [0, -1.02, 0], color=TEAL, stroke_width=5)
        tak1 = VGroup(tak1_box, tak1_foot, T("TAK1", size=30, color=TEAL).move_to(tak1_box)).move_to([1.2, 2.75, 0])

        ikk_box = RoundedRectangle(corner_radius=0.18, width=2.15, height=0.98, stroke_color=TEAL, stroke_width=3.5,
                                   fill_color=TEAL, fill_opacity=0.20).set_z_index(2)
        ikk_foot = Line([0, -0.49, 0], [0, -1.44, 0], color=TEAL, stroke_width=5).set_z_index(2)
        ikk_lbl = T("IKK", size=32, color=TEAL).move_to(ikk_box).set_z_index(3)
        ikk = VGroup(ikk_box, ikk_foot, ikk_lbl).move_to([4.6, 2.75, 0])

        self.play(FadeIn(tak1), FadeIn(ikk), run_time=0.7)
        self.play(
            tak1.animate.move_to([0.25, 1.24, 0]),
            ikk.animate.move_to([3.05, 1.05, 0]),
            irak_pulse.animate.set_value(8.5),
            run_time=max(1.4, self.t_of("platform") - self.elapsed() - 0.25),
            rate_func=linear,
        )

        # Parabolic activation spark arcs from TAK1 onto IKK, lighting IKK up
        self.at("platform")
        spark_t = ValueTracker(0.0)
        p_start = tak1_box.get_right() + LEFT * 0.05
        p_end = ikk_box.get_left() + RIGHT * 0.05
        spark = always_redraw(lambda: Dot(
            (1 - spark_t.get_value()) * p_start + spark_t.get_value() * p_end
            + UP * 0.72 * np.sin(spark_t.get_value() * PI),
            radius=0.16, color=TEXT
        ))
        self.add(spark)
        self.play(spark_t.animate.set_value(1.0), run_time=0.45, rate_func=linear)
        self.remove(spark)

        ikk_halo = SurroundingRectangle(ikk_box, corner_radius=0.22, buff=0.09, stroke_color=TEXT, stroke_width=4).set_z_index(1)
        lbl_on = T("IKK ON", size=28, color=TEXT).next_to(ikk_box, UP, buff=0.22)
        self.play(
            ikk_box.animate.set_fill(TEAL, opacity=0.78).set_stroke(TEXT, width=4.5),
            ikk_lbl.animate.set_color(TEXT),
            Create(ikk_halo),
            FadeIn(lbl_on, shift=UP * 0.1),
            run_time=0.4,
        )
        self.play(
            irak_pulse.animate.set_value(10.0),
            run_time=max(0.2, self.narration_s - self.elapsed() - 0.1),
            rate_func=linear,
        )
        self.finish()


class S06Destroy(SpokenScene):
    def construct(self):
        cyto_bg = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=CYTO_FILL, fill_opacity=0.9)
        self.add(cyto_bg)

        # Large NF-κB + coral IκB clamp filling center
        nfkb = make_nfkb(scale=1.32, has_tag=True).move_to([-1.2, -0.35, 0])
        set_tag_visibility(nfkb.tag, fill_op=0.22, stroke_op=0.45)
        clamp = make_ikb_clamp(scale=1.32, closed=True).move_to([-1.08, -0.35, 0])
        clamp.shield.set_fill(CORAL, opacity=0.72)
        lbl_nfkb = T("NF-κB", size=32, color=EMERALD).next_to(nfkb.dimer, DOWN, buff=0.75)
        lbl_ikb = T("IκB", size=32, color=CORAL).next_to(clamp, LEFT, buff=0.28)

        ikk_box = RoundedRectangle(corner_radius=0.16, width=1.7, height=0.84, stroke_color=TEXT, stroke_width=3.8,
                                   fill_color=TEAL, fill_opacity=0.8)
        ikk = VGroup(ikk_box, T("IKK", size=30, color=TEXT).move_to(ikk_box)).move_to([-4.8, 2.25, 0])

        self.add(nfkb, clamp, lbl_nfkb, lbl_ikb, ikk)

        # IKK glides smoothly right up to IκB
        self.play(
            ikk.animate.move_to([-2.4, 1.85, 0]),
            run_time=max(1.2, self.t_of("stamps two phosphate marks") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Two bright phosphate dots stamped on the outer top rim of IκB (no scaled P text inside!)
        self.at("stamps two phosphate marks")
        p1 = Dot([-1.42, 1.46, 0], radius=0.17, color=TEXT, stroke_color=TEAL, stroke_width=3)
        p2 = Dot([-0.82, 1.50, 0], radius=0.17, color=TEXT, stroke_color=TEAL, stroke_width=3)
        p_dots = VGroup(p1, p2)
        lbl_p = T("2× Phosphate", size=26, color=TEXT).move_to([-0.82, 2.22, 0])
        self.play(FadeIn(p1, scale=1.5), run_time=0.65)
        self.play(
            FadeIn(p2, scale=1.5),
            ikk.animate.move_to([-3.2, 2.02, 0]),
            run_time=0.65,
            rate_func=linear,
        )
        self.play(
            FadeIn(lbl_p, shift=UP * 0.1),
            ikk.animate.move_to([-4.6, 2.25, 0]).set_opacity(0.45),
            run_time=max(1.0, self.t_of("hangs on") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        # Clamp hangs on (continuous shudder)
        self.at("hangs on")
        shudder = ValueTracker(0.0)
        clamp_group = VGroup(clamp, p_dots)
        base_c = clamp_group.get_center().copy()
        clamp_group.add_updater(lambda m: m.move_to(base_c + RIGHT * 0.10 * np.sin(shudder.get_value() * 5 * PI)))
        self.play(
            shudder.animate.set_value(1.0),
            run_time=max(1.2, self.t_of("second enzyme") - self.elapsed() - 0.2),
            rate_func=linear,
        )
        clamp_group.clear_updaters()
        clamp_group.move_to(base_c)

        # Second enzyme glides in cleanly with ample padding
        self.at("second enzyme")
        e3 = boxed_label("E3 enzyme", color=GREY, size=26, pad=0.28).move_to([1.65, 2.75, 0])
        self.play(FadeIn(e3), run_time=0.5)
        self.play(
            e3.animate.move_to([1.55, 1.95, 0]),
            run_time=max(0.8, self.t_of("attaches") - self.elapsed() - 0.2),
        )

        # Coral K48 ubiquitin chain attached cleanly; K48 tag label clear of red shield
        self.at("attaches")
        k48_pts = [np.array([0.45 + 0.36 * i, 0.78 + 0.18 * np.sin(i * 0.9), 0]) for i in range(6)]
        k48_chain = make_ubiquitin_chain(k48_pts, color=CORAL, bead_r=0.15)
        lbl_k48 = T("K48 tag", size=28, color=CORAL).move_to([2.0, -0.05, 0])
        self.play(
            Create(k48_chain[0]),
            LaggedStart(*[FadeIn(b, scale=0.7) for b in k48_chain[1]], lag_ratio=0.18),
            FadeIn(lbl_k48),
            run_time=max(2.0, self.t_of("proteasome") - self.elapsed() - 0.2),
        )

        # Proteasome barrel draws the coral clamp away and shreds it
        self.at("proteasome")
        prot_body = RoundedRectangle(corner_radius=0.28, width=1.95, height=2.65, stroke_color=GREY, stroke_width=4,
                                     fill_color="#232A38", fill_opacity=0.95).move_to([4.15, 0.35, 0])
        prot_rings = VGroup(*[
            Line([3.3, 0.35 + dy, 0], [5.0, 0.35 + dy, 0], color=GREY, stroke_width=3.5)
            for dy in (-0.75, -0.25, 0.25, 0.75)
        ])
        lbl_prot = T("Proteasome", size=28, color=TEXT).next_to(prot_body, DOWN, buff=0.25)
        proteasome = VGroup(prot_body, prot_rings, lbl_prot)
        self.play(FadeIn(proteasome, shift=LEFT * 0.25), FadeOut(e3), FadeOut(ikk), FadeOut(lbl_p), run_time=1.0)

        self.play(FadeOut(lbl_ikb), FadeOut(lbl_k48), run_time=0.25)

        target_pull = VGroup(clamp, p_dots, k48_chain)
        self.play(
            target_pull.animate.scale(0.45).move_to(prot_body.get_center()),
            run_time=max(1.2, self.t_of("which frees") - self.elapsed() - 0.2),
        )

        rng = np.random.default_rng(7)
        frags = VGroup()
        frag_targets = []
        for _ in range(16):
            d = RoundedRectangle(corner_radius=0.04, width=rng.uniform(0.14, 0.25),
                                 height=rng.uniform(0.10, 0.18), stroke_width=0,
                                 fill_color=CORAL, fill_opacity=0.92).move_to(prot_body.get_right() + LEFT * 0.2)
            frags.add(d)
            frag_targets.append(prot_body.get_right() + np.array([rng.uniform(0.4, 1.35), rng.uniform(-1.05, 1.05), 0]))

        self.at("which frees")
        lbl_freed = T("Nuclear tag uncovered", size=28, color=PURPLE).move_to([-1.2, 1.65, 0])
        self.play(
            FadeOut(target_pull),
            FadeIn(frags),
            *[f.animate.move_to(pos).set_opacity(0.25) for f, pos in zip(frags, frag_targets)],
            nfkb.dimer.animate.shift(LEFT * 0.2 + UP * 0.1),
            nfkb.tag[0].animate.shift(LEFT * 0.2 + UP * 0.1).set_fill(PURPLE, opacity=0.65).set_stroke(PURPLE, opacity=1.0),
            nfkb.tag[1].animate.shift(LEFT * 0.2 + UP * 0.1).set_fill(PURPLE, opacity=0.65).set_stroke(PURPLE, opacity=1.0),
            nfkb.tag[2].animate.shift(LEFT * 0.2 + UP * 0.1).set_fill(opacity=0.0).set_stroke(PURPLE, opacity=0.8),
            lbl_nfkb.animate.move_to([-1.4, -1.75, 0]),
            FadeIn(lbl_freed, shift=UP * 0.12),
            run_time=max(1.6, self.narration_s - self.elapsed() - 0.1),
        )
        self.finish()


def build_predict_state():
    """Shared builder for S07Predict's end frame and S08Pause's backdrop."""
    world = make_macrophage_world(show_endosome=True, endo_r=0.9, nuc_center=(0.0, -1.95, 0), nuc_w=4.6, nuc_h=1.55)
    tlr_l = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([-0.4, 2.38, 0])
    tlr_r = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([0.4, 2.38, 0])
    endo = RoundedRectangle(corner_radius=0.1, width=0.68, height=0.32, stroke_color=AMBER, stroke_width=3,
                            fill_color=AMBER, fill_opacity=0.85).move_to([0.0, 2.75, 0])
    lbl_endo = T("Endotoxin", size=26, color=AMBER).move_to([1.95, 2.85, 0])

    mutant = make_nfkb(scale=0.88, has_tag=True, mutant_empty_tag=True).move_to([0.0, 0.20, 0])
    lbl_mut = T("Mutant NF-κB: no nuclear tag", size=28, color=EMERALD).move_to([0.0, 1.66, 0])
    lbl_nuc = T("Nucleus", size=26, color=PURPLE).move_to([0.0, -2.42, 0])
    return VGroup(world, tlr_l, tlr_r, endo, lbl_endo, mutant, lbl_mut, lbl_nuc)


class S07Predict(SpokenScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=0.9, nuc_center=(0.0, -1.95, 0), nuc_w=4.6, nuc_h=1.55)
        tlr_l = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([-0.4, 2.38, 0])
        tlr_r = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([0.4, 2.38, 0])
        lbl_nuc = T("Nucleus", size=26, color=PURPLE).move_to([0.0, -2.42, 0])
        self.play(FadeIn(world), FadeIn(tlr_l), FadeIn(tlr_r), FadeIn(lbl_nuc), run_time=0.9)
        # Gentle receptor drift while narrator begins
        self.play(
            tlr_l.animate.shift(LEFT * 0.12),
            tlr_r.animate.shift(RIGHT * 0.12),
            run_time=max(0.8, self.t_of("Suppose a mutant") - self.elapsed() - 0.2),
            rate_func=there_and_back,
        )

        self.at("Suppose a mutant")
        mutant_normal = make_nfkb(scale=0.88, has_tag=True, mutant_empty_tag=False).move_to([0.0, 0.20, 0])
        clamp = make_ikb_clamp(scale=0.88, closed=True).move_to([0.05, 0.20, 0])
        clamp.shield.set_fill(CORAL, opacity=0.65)
        self.play(FadeIn(mutant_normal), FadeIn(clamp), run_time=0.9)

        self.at("lacks its nuclear entry tag")
        mutant_empty = make_nfkb(scale=0.88, has_tag=True, mutant_empty_tag=True).move_to([0.0, 0.20, 0])
        # Label sits at y = 1.66, safely above clamp top (0.20 + 1.17 = 1.37)
        lbl_mut = T("Mutant NF-κB: no nuclear tag", size=28, color=EMERALD).move_to([0.0, 1.66, 0])
        self.play(
            ReplacementTransform(mutant_normal.tag, mutant_empty.tag),
            FadeIn(lbl_mut),
            run_time=max(1.0, self.t_of("Endotoxin arrives") - self.elapsed() - 0.2),
        )

        self.at("Endotoxin arrives")
        endo = RoundedRectangle(corner_radius=0.1, width=0.68, height=0.32, stroke_color=AMBER, stroke_width=3,
                                fill_color=AMBER, fill_opacity=0.85).move_to([-2.4, 3.28, 0])
        lbl_endo = T("Endotoxin", size=26, color=AMBER).move_to([1.95, 2.85, 0])
        self.play(
            endo.animate.move_to([0.0, 2.75, 0]),
            FadeIn(lbl_endo),
            run_time=max(1.0, self.t_of("destroyed as usual") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        self.at("destroyed as usual")
        self.play(
            clamp.animate.shift(RIGHT * 1.8).scale(0.35).set_opacity(0.0),
            run_time=max(1.0, self.t_of("Will the defense") - self.elapsed() - 0.2),
        )
        self.remove(clamp)

        self.at("Will the defense")
        q = question_card("No nuclear tag: do defense genes switch on?", y=-3.05, color=GOLD, size=30, max_w=10.2)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.9)

        self.at("few seconds")
        bob_t = ValueTracker(0.0)
        m_grp = VGroup(mutant_normal.dimer, mutant_empty.tag)
        m_base = m_grp.get_center().copy()
        m_grp.add_updater(lambda m: m.move_to(m_base + UP * 0.10 * np.sin(bob_t.get_value() * TAU)))
        self.play(bob_t.animate.set_value(1.5), run_time=max(0.8, self.narration_s - self.elapsed() - 0.1),
                  rate_func=linear)
        m_grp.clear_updaters()
        m_grp.move_to(m_base)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "No nuclear tag: do defense genes switch on?"
    CARD = {"y": -3.05, "max_w": 10.2}
    RING_AT = (6.0, -3.0, 0)
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_state()


class S09Reveal(SpokenScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=0.85, nuc_center=(0.0, -1.8, 0), nuc_w=5.2, nuc_h=1.7)
        tlr_l = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([-0.4, 2.38, 0])
        tlr_r = make_horseshoe(TEAL, scale=0.72, facing=DOWN, with_tail=True, with_md2=True).move_to([0.4, 2.38, 0])
        endo = RoundedRectangle(corner_radius=0.1, width=0.68, height=0.32, stroke_color=AMBER, stroke_width=3,
                                fill_color=AMBER, fill_opacity=0.85).move_to([0.0, 2.75, 0])

        mutant = make_nfkb(scale=0.86, has_tag=True, mutant_empty_tag=True).move_to([0.0, 0.10, 0])
        lbl_mut = T("Mutant NF-κB: no nuclear tag", size=28, color=EMERALD).move_to([0.0, 1.55, 0])
        q = question_card("No nuclear tag: do defense genes switch on?", y=-3.05, color=GOLD, size=30, max_w=10.2)
        self.add(world, tlr_l, tlr_r, endo, mutant, lbl_mut, q)

        # Question clears to coral "No: genes stay off" cleanly on the far left; mutant bounces off left pore
        no_badge = boxed_label("No: genes stay off", color=CORAL, size=26, pad=0.16).move_to([-4.25, -2.97, 0])
        self.play(
            swap(q.question, no_badge, run_time=0.7),
            mutant.animate.move_to([-1.2, 0.45, 0]),
            FadeOut(lbl_mut),
            run_time=1.0,
        )

        # Mutant tries the left nuclear pore and bounces back twice so motion is unmistakable
        self.play(mutant.animate.move_to([-1.2, -0.68, 0]), run_time=0.8, rate_func=rush_into)
        self.play(mutant.animate.move_to([-1.35, 0.45, 0]), run_time=0.9, rate_func=rush_from)

        self.at("uncovering that tag")
        self.play(mutant.animate.move_to([-1.2, -0.65, 0]), run_time=0.9, rate_func=rush_into)
        self.play(mutant.animate.move_to([-1.45, 0.55, 0]), run_time=1.0, rate_func=rush_from)

        # Nuclear pores label placed cleanly on the RIGHT side away from the endosome!
        self.at("nuclear pores")
        pore_lbl = T("Nuclear pores", size=26, color=PURPLE).move_to([3.75, -1.05, 0])
        self.play(FadeIn(pore_lbl, shift=LEFT * 0.15), run_time=0.9)

        # Normal NF-κB glides through the right pore into nucleus and binds target DNA
        self.at("In a normal cell")
        normal = make_nfkb(scale=0.86, has_tag=True, mutant_empty_tag=False).move_to([1.35, 0.65, 0])
        lbl_norm = T("Normal NF-κB", size=28, color=EMERALD).next_to(normal, UP, buff=0.25)
        self.play(FadeIn(normal), FadeIn(lbl_norm), run_time=1.0)

        self.at("glides into")
        self.play(
            normal.animate.move_to([1.2, -1.1, 0]),
            FadeOut(lbl_norm),
            run_time=max(1.2, self.t_of("target DNA") - self.elapsed() - 0.2),
        )

        self.at("target DNA")
        self.play(
            normal.animate.scale(0.75).move_to(world.dna.get_center() + UP * 0.08),
            run_time=max(1.2, self.t_of("switch on within minutes") - self.elapsed() - 0.2),
        )

        # Concentric light waves pulse outward from DNA; label fades in crisply right on cue
        self.at("switch on within minutes")
        lbl_on = boxed_label("Normal cell: defense genes ON within minutes", color=EMERALD, size=22, pad=0.14).move_to([1.85, -2.97, 0])
        wave_t = ValueTracker(0.0)
        waves = always_redraw(lambda: VGroup(*[
            Ellipse(
                width=1.8 + 2.8 * ((wave_t.get_value() + k * 0.33) % 1.0),
                height=0.55 + 1.15 * ((wave_t.get_value() + k * 0.33) % 1.0),
                stroke_color=EMERALD, stroke_width=4,
                stroke_opacity=max(0.0, 0.9 * (1.0 - (wave_t.get_value() + k * 0.33) % 1.0)),
            ).move_to(world.dna.get_center())
            for k in range(3)
        ]))
        self.add(waves)
        self.play(
            FadeIn(lbl_on, shift=UP * 0.1),
            world.dna.animate.set_color(EMERALD),
            wave_t.animate.set_value(0.55),
            run_time=0.45,
            rate_func=linear,
        )
        self.play(
            wave_t.animate.set_value(2.6),
            run_time=max(0.9, self.narration_s - self.elapsed() - 0.1),
            rate_func=linear,
        )
        self.finish()


class S10Wrap(SpokenScene):
    def construct(self):
        world = make_macrophage_world(show_endosome=True, endo_r=0.95, nuc_center=(0.5, -2.1, 0), nuc_w=4.8, nuc_h=1.7)
        self.add(world)

        tlr_l = make_horseshoe(TEAL, scale=0.68, facing=DOWN, with_tail=True, with_md2=True).move_to([0.12, 2.38, 0])
        tlr_r = make_horseshoe(TEAL, scale=0.68, facing=DOWN, with_tail=True, with_md2=True).move_to([0.88, 2.38, 0])
        endo = RoundedRectangle(corner_radius=0.1, width=0.65, height=0.28, stroke_color=AMBER, stroke_width=3,
                                fill_color=AMBER, fill_opacity=0.85).move_to([0.5, 2.74, 0])
        tower = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.44, height=0.17, stroke_color=TEXT, stroke_width=1.6,
                             fill_color=TEAL, fill_opacity=0.85).move_to([0.5 + 0.16 * np.cos(k * 1.2), 1.55 - 0.17 * k, 0])
            for k in range(5)
        ])
        k63_pts = [np.array([0.85 + 0.40 * i, 0.65 - 0.10 * np.sin(i * 0.8), 0]) for i in range(6)]
        k63 = make_ubiquitin_chain(k63_pts, color=SKY, bead_r=0.12)
        lbl_k63 = T("K63 scaffold", size=26, color=SKY).move_to([3.05, 1.38, 0])

        rng = np.random.default_rng(11)
        shreds = VGroup(*[
            RoundedRectangle(corner_radius=0.03, width=0.16, height=0.10, stroke_width=0,
                             fill_color=CORAL, fill_opacity=0.8).move_to([4.1 + rng.uniform(-0.35, 0.35),
                                                                          -0.05 + rng.uniform(-0.35, 0.35), 0])
            for _ in range(9)
        ])
        lbl_ikb_gone = T("IκB destroyed", size=26, color=CORAL).move_to([4.15, -0.82, 0])

        nfkb_dna = make_nfkb(scale=0.64, has_tag=True).move_to(world.dna.get_center() + UP * 0.06)
        # Clear of nucleus ellipse right boundary (0.5 + 2.4 = 2.9)
        lbl_nfkb = T("NF-κB on DNA", size=28, color=EMERALD).move_to([4.55, -2.15, 0])

        canonical = VGroup(tlr_l, tlr_r, endo, tower, k63, lbl_k63, shreds, lbl_ikb_gone, nfkb_dna, lbl_nfkb)
        self.play(FadeIn(canonical), run_time=0.95)

        # Propagating relay glow routed cleanly down center-right without grazing any labels
        self.at("canonical")
        pulse_t = ValueTracker(0.0)
        relay_pts = [np.array([0.5, 2.7, 0]), np.array([0.5, 1.2, 0]), np.array([1.55, 0.48, 0]),
                     np.array([1.85, -0.55, 0]), world.dna.get_center()]

        def get_relay_glow():
            u = pulse_t.get_value() % 1.0
            idx = min(len(relay_pts) - 2, int(u * (len(relay_pts) - 1)))
            frac = u * (len(relay_pts) - 1) - idx
            pos = (1 - frac) * relay_pts[idx] + frac * relay_pts[idx + 1]
            ring_outer = Circle(radius=0.32, stroke_color=TEAL, stroke_width=4, stroke_opacity=0.9,
                                fill_color=TEAL, fill_opacity=0.45).move_to(pos)
            dot_inner = Dot(pos, radius=0.15, color=TEXT)
            dna_w = Ellipse(
                width=2.1 + 2.7 * u, height=0.58 + 1.05 * u,
                stroke_color=EMERALD, stroke_width=5.5, stroke_opacity=max(0.0, 0.95 * (1.0 - u))
            ).move_to(world.dna.get_center())
            return VGroup(ring_outer, dot_inner, dna_w)

        pdot = always_redraw(get_relay_glow)
        self.add(pdot)
        self.play(pulse_t.animate.set_value(2.4), run_time=max(1.0, self.t_of("A few routes") - self.elapsed() - 0.2),
                  rate_func=linear)

        self.at("A few routes")
        tlr3 = make_horseshoe(TEAL, scale=0.52, facing=LEFT, with_tail=True).move_to(world.endosome.get_center() + RIGHT * 0.62)
        branch_line = Arrow(tlr3.get_right() + RIGHT * 0.05, [-1.15, -0.32, 0], color="#AEB6C4", stroke_width=3.5, buff=0.05)
        lbl_tlr3 = T("TLR3 → interferon", size=24, color="#AEB6C4").move_to([-1.05, -0.78, 0])
        side_branch = VGroup(tlr3, branch_line, lbl_tlr3)
        self.play(FadeIn(side_branch), pulse_t.animate.set_value(4.0),
                  run_time=max(1.0, self.t_of("toward interferon") - self.elapsed() - 0.1), rate_func=linear)

        self.at("toward interferon")
        self.play(lbl_tlr3.animate.set_color(TEXT), pulse_t.animate.set_value(5.2),
                  run_time=max(0.8, self.t_of("core pathway") - self.elapsed() - 0.2), rate_func=linear)

        self.at("core pathway")
        self.play(lbl_tlr3.animate.set_color("#9EA7B8"), pulse_t.animate.set_value(6.2),
                  run_time=max(0.8, self.t_of("built and trapped") - self.elapsed() - 0.2), rate_func=linear)

        self.at("built and trapped")
        trap_box = make_nfkb(scale=0.52, has_tag=False).move_to([-1.6, 0.82, 0])
        trap_clamp = make_ikb_clamp(scale=0.52, closed=True).move_to([-1.55, 0.82, 0])
        self.play(FadeIn(trap_box), FadeIn(trap_clamp), pulse_t.animate.set_value(7.2),
                  run_time=max(0.8, self.t_of("pattern arrives") - self.elapsed() - 0.2), rate_func=linear)

        self.at("pattern arrives")
        self.play(
            FadeOut(trap_box), FadeOut(trap_clamp),
            endo.animate.scale(1.15),
            pulse_t.animate.set_value(8.4),
            run_time=max(0.8, self.t_of("inhibitor destruction") - self.elapsed() - 0.2),
            rate_func=linear,
        )

        self.at("inhibitor destruction")
        self.play(
            shreds.animate.shift(DOWN * 0.25).set_opacity(0.3),
            world.dna.animate.set_color(EMERALD),
            pulse_t.animate.set_value(10.5),
            run_time=max(1.0, self.narration_s - self.elapsed() - 0.1),
            rate_func=linear,
        )
        self.finish()


class S11End(EndCard):
    LINE = "Toll-like receptors free pre-made NF-κB by triggering inhibitor destruction."
