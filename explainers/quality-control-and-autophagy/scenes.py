"""Follow the Flow, Not the Pile — Protein Quality Control and Organelle Turnover.

COLOUR MAP (one colour per concept for the whole film):
  BG     = #0f1117  dark background
  CYTO   = #212938  cell cross-section cytoplasm fill (distinct from BG, high text contrast)
  TEXT   = #E8EAF0  labels, cell outline, pool container
  GREY   = #8B93A1  ER lumen, cell material / mitochondrion / building blocks, schematic tag
  BLUE   = #58C4DD  autophagosome membrane cup / double-membrane carrier / arrival flow
  ORANGE = #F08C4B  lysosome (acidic recycling compartment) / clearance gate
  TEAL   = #3FB8C0  ER folding helpers
  GOLD   = #D4A843  proteasome barrel
  RED    = #FC6255  ubiquitin tag, bafilomycin / exit block, defective autophagy
  PURPLE = #B589F5  LC3-II membrane marker and LC3-II pool gauge
  YELLOW = #F5D547  extra accumulation increment and active gate highlight
  GREEN  = #83C167  normal autophagy-competent yeast

CARRIED WORLD:
  One large cross-section of the cell (ER on the left, autophagosome assembly in the center,
  gold proteasome at upper right, orange lysosome at lower right). The top-right corner
  (x > 5.8, y > 2.9) stays clear across every content scene for the corner Hex mark.

WHAT CHANGES IN EACH SPOKEN SCENE (and what drives it):
  s01_hook          : Blue cup wraps gray cargo into an autophagosome that moves to the orange
                      lysosome; two cell copies replay fast vs blocked flow along a 0..1 time
                      scrubber to the same 4-carrier pool.
  s03_er_route      : Zoomed ER lumen; a gray client squiggle cycles between teal helpers along
                      a retry loop, exits to cytosol with a red ubiquitin tag, straightens, and
                      threads through the gold proteasome barrel.
  s04_lysosome_route: Carried full map; a large gray mitochondrion reaches and is rejected by the
                      narrow proteasome entrance, gets wrapped by two closing blue arcs, fuses
                      with the orange lysosome, and becomes six gray building-block squares.
  s05_starvation    : Carried map with external inlet and reuse bin; narrowing the inlet drops
                      the computed bin level (0.84 -> 0.24), continuous autophagosome-to-lysosome
                      recycling returns blocks to partially recover the bin (0.24 -> 0.62), and
                      normal vs autophagy-defective yeast silhouettes appear.
  s06_rule          : Central carrier pool between arrival and clearance gates; dot streams and
                      a vertical pool gauge driven by pool_level(t) stay level at equal rates,
                      then climb to the same height via thick arrival or narrow clearance.
  s07_predict       : Two synchronized cell maps gain purple LC3-II membrane marks and red
                      bafilomycin exit blocks at equal high starting pools under thick vs thin
                      arrival arrows with continuous arrival flow, holding the prediction question.
  s09_reveal        : From the equal dashed baseline, both purple gauges advance over the same
                      interval while unchanged formation streams continue; fast arrival climbs
                      steeply, slow arrival barely moves, and yellow increments are highlighted.
  s10_return        : Two cells replay the diverged block, then merge into the single recycling
                      map running continuous ER-to-proteasome and autophagosome-to-lysosome
                      flows while highlighting arrival then clearance gates.
"""

from bp_parts import *

CYTO = "#212938"
ORANGE = "#F08C4B"
PURPLE = "#B589F5"

# Keep top-right corner (x > 5.8, y > 2.9) empty in every content scene for the standard Hex mark.


def dt_to(scene, phrase, lead=0.22, min_dt=0.35, nth=0):
    """Remaining seconds until `phrase` starts (minus lead), for pacing animations to narration."""
    return max(min_dt, scene.t_of(phrase, nth=nth) - lead - scene.elapsed())


def build_cell_outline(center=(-0.15, 0.15, 0), width=10.6, height=5.4, stroke_width=3.4):
    """Cell cross-section boundary filling ~68% of frame height."""
    return RoundedRectangle(
        corner_radius=1.1,
        width=width,
        height=height,
        stroke_color=TEXT,
        stroke_width=stroke_width,
        fill_color=CYTO,
        fill_opacity=1.0,
    ).move_to(center)


def build_er_patch(center=(-3.5, 0.1, 0), scale=1.0):
    """Layered gray ER lumen patch on the left of the cell cross-section."""
    outer = RoundedRectangle(
        corner_radius=0.35 * scale,
        width=2.1 * scale,
        height=3.1 * scale,
        stroke_color=GREY,
        stroke_width=2.6,
        fill_color=GREY,
        fill_opacity=0.16,
    ).move_to(center)
    folds = VGroup(
        Line(
            [center[0] - 0.65 * scale, center[1] + 0.7 * scale, 0],
            [center[0] + 0.55 * scale, center[1] + 0.7 * scale, 0],
            color=GREY,
            stroke_width=2.4,
        ),
        Line(
            [center[0] - 0.55 * scale, center[1] - 0.05 * scale, 0],
            [center[0] + 0.65 * scale, center[1] - 0.05 * scale, 0],
            color=GREY,
            stroke_width=2.4,
        ),
        Line(
            [center[0] - 0.65 * scale, center[1] - 0.8 * scale, 0],
            [center[0] + 0.55 * scale, center[1] - 0.8 * scale, 0],
            color=GREY,
            stroke_width=2.4,
        ),
    )
    return VGroup(outer, folds)


def build_lysosome(center=(3.0, -0.5, 0), radius=0.95):
    """Orange acidic recycling compartment."""
    ring = Circle(
        radius=radius,
        stroke_color=ORANGE,
        stroke_width=4.2,
        fill_color=ORANGE,
        fill_opacity=0.22,
    ).move_to(center)
    inner = Circle(
        radius=radius * 0.76,
        stroke_color=ORANGE,
        stroke_width=1.8,
        stroke_opacity=0.60,
        fill_opacity=0.0,
    ).move_to(center)
    return VGroup(ring, inner)


def build_proteasome(center=(3.1, 1.7, 0), scale=1.0):
    """Gold capped barrel with narrow central channel (no molecular structure)."""
    w, h = 1.15 * scale, 0.62 * scale
    c = np.array(center, dtype=float)
    top_wall = RoundedRectangle(
        corner_radius=0.06 * scale,
        width=w,
        height=0.18 * scale,
        stroke_color=GOLD,
        stroke_width=2.6,
        fill_color=GOLD,
        fill_opacity=0.28,
    ).move_to(c + UP * (0.22 * scale))
    bot_wall = RoundedRectangle(
        corner_radius=0.06 * scale,
        width=w,
        height=0.18 * scale,
        stroke_color=GOLD,
        stroke_width=2.6,
        fill_color=GOLD,
        fill_opacity=0.28,
    ).move_to(c + DOWN * (0.22 * scale))
    cap_l = RoundedRectangle(
        corner_radius=0.08 * scale,
        width=0.22 * scale,
        height=h,
        stroke_color=GOLD,
        stroke_width=2.6,
        fill_color=GOLD,
        fill_opacity=0.34,
    ).move_to(c + LEFT * (0.64 * scale))
    cap_r = RoundedRectangle(
        corner_radius=0.08 * scale,
        width=0.22 * scale,
        height=h,
        stroke_color=GOLD,
        stroke_width=2.6,
        fill_color=GOLD,
        fill_opacity=0.34,
    ).move_to(c + RIGHT * (0.64 * scale))
    pore = Line(
        c + LEFT * (0.76 * scale),
        c + RIGHT * (0.76 * scale),
        color=CYTO,
        stroke_width=8 * scale,
    )
    return VGroup(top_wall, bot_wall, pore, cap_l, cap_r)


def build_cargo_blob(center=(0, 0, 0), radius=0.26, color=GREY):
    """Simple gray parcel of cell material."""
    return RoundedRectangle(
        corner_radius=radius * 0.45,
        width=radius * 1.9,
        height=radius * 1.35,
        stroke_color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.55,
    ).move_to(center)


def build_autophagosome(center=(0, 0, 0), radius=0.42, lc3=False, cargo_radius=0.22):
    """Double-membrane blue carrier enclosing gray cell material, optionally marked with purple LC3-II."""
    c = np.array(center, dtype=float)
    outer = Circle(radius=radius, stroke_color=BLUE, stroke_width=3.4, fill_color=BLUE, fill_opacity=0.12).move_to(c)
    inner = Circle(radius=radius * 0.80, stroke_color=BLUE, stroke_width=2.4, fill_opacity=0.0).move_to(c)
    cargo = build_cargo_blob(c, radius=cargo_radius)
    parts = [outer, inner, cargo]
    if lc3:
        marks = VGroup(*[
            Dot(
                c + (radius * 1.03) * np.array([np.cos(a), np.sin(a), 0.0]),
                radius=0.065 * (radius / 0.42),
                color=PURPLE,
            )
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        parts.append(marks)
    return VGroup(*parts)


def build_mitochondrion(center=(0, 0, 0), width=1.65, height=0.82):
    """Simple mitochondrion cartoon: gray outer capsule and wavy inner cristae curve."""
    c = np.array(center, dtype=float)
    shell = RoundedRectangle(
        corner_radius=height * 0.48,
        width=width,
        height=height,
        stroke_color=GREY,
        stroke_width=3.4,
        fill_color=GREY,
        fill_opacity=0.28,
    ).move_to(c)
    xs = np.linspace(-width * 0.36, width * 0.36, 49)
    ys = (height * 0.24) * np.sin(np.linspace(0, 5 * PI, 49))
    pts = [c + np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    cristae = VMobject(stroke_color=TEXT, stroke_width=2.4, fill_opacity=0.0)
    cristae.set_points_as_corners(pts)
    return VGroup(shell, cristae)


def build_squiggle(center=(0, 0, 0), width=1.3, amp=0.28, n_waves=2.5, color=GREY):
    """Simple folded client protein squiggle (no molecular structure)."""
    c = np.array(center, dtype=float)
    ts = np.linspace(-0.5, 0.5, 60)
    pts = [c + np.array([t * width, amp * np.sin(t * n_waves * TAU), 0.0]) for t in ts]
    m = VMobject(stroke_color=color, stroke_width=5.0, fill_opacity=0.0)
    m.set_points_as_corners(pts)
    return m


def build_exit_block(center=(0, 0, 0), height=0.95):
    """Red bafilomycin/exit block bar."""
    return RoundedRectangle(
        corner_radius=0.06,
        width=0.20,
        height=height,
        stroke_color=RED,
        stroke_width=2.5,
        fill_color=RED,
        fill_opacity=0.92,
    ).move_to(center)


# ------------------------------------------------------------------ s01_hook
class S01Hook(SpokenScene):
    def construct(self):
        cell = build_cell_outline(center=(-0.2, 0.2, 0), width=10.6, height=5.3)
        er = build_er_patch(center=(-3.6, 0.2, 0), scale=0.95)
        lyso = build_lysosome(center=(2.8, -0.25, 0), radius=0.95)
        cargo = build_cargo_blob(center=(-1.2, 0.3, 0), radius=0.28)
        tag = scope_tag("schematic")

        self.play(FadeIn(cell), FadeIn(er), FadeIn(lyso), FadeIn(cargo), FadeIn(tag), run_time=0.7)

        c_pos = cargo.get_center()
        cup_outer = Arc(radius=0.52, start_angle=PI * 0.35, angle=PI * 1.3, arc_center=c_pos, stroke_color=BLUE, stroke_width=4.0)
        cup_inner = Arc(radius=0.41, start_angle=PI * 0.35, angle=PI * 1.3, arc_center=c_pos, stroke_color=BLUE, stroke_width=2.6)
        self.play(Create(cup_outer), Create(cup_inner), run_time=1.8)

        closed_outer = Circle(radius=0.52, stroke_color=BLUE, stroke_width=4.0, fill_color=BLUE, fill_opacity=0.12).move_to(c_pos)
        closed_inner = Circle(radius=0.41, stroke_color=BLUE, stroke_width=2.6, fill_opacity=0.0).move_to(c_pos)
        self.play(
            ReplacementTransform(cup_outer, closed_outer),
            ReplacementTransform(cup_inner, closed_inner),
            run_time=max(0.4, dt_to(self, "sends it to lysosomes")),
        )
        carrier = VGroup(closed_outer, closed_inner, cargo)

        self.at("sends it to lysosomes")
        self.play(carrier.animate.move_to([0.55, 0.05, 0]), run_time=1.5)
        lyso_lab = T("lysosome", 28, ORANGE).next_to(lyso, DOWN, buff=0.18)
        self.play(
            FadeIn(lyso_lab, shift=UP * 0.1),
            carrier.animate.move_to([0.85, 0.0, 0]),
            run_time=max(0.5, dt_to(self, "those carriers")),
        )

        self.at("those carriers")
        auto_lab = T("autophagosome", 28, BLUE).next_to(carrier, UP, buff=0.24).shift(LEFT * 0.4)
        self.play(FadeIn(auto_lab, shift=DOWN * 0.1), run_time=0.6)
        self.play(
            carrier.animate.move_to([1.25, -0.10, 0]),
            auto_lab.animate.shift(LEFT * 0.25),
            run_time=max(0.5, dt_to(self, "two cells")),
        )

        self.at("two cells")
        panel_w, panel_h = 4.95, 4.25
        left_c = np.array([-3.2, 0.15, 0.0])
        right_c = np.array([2.65, 0.15, 0.0])

        def mini_cell(c):
            box = RoundedRectangle(corner_radius=0.65, width=panel_w, height=panel_h, stroke_color=TEXT, stroke_width=2.8, fill_color=CYTO, fill_opacity=1.0).move_to(c)
            ly = build_lysosome(center=c + np.array([1.50, -0.12, 0.0]), radius=0.62)
            ly_lbl = T("lysosome", 24, ORANGE).next_to(ly, DOWN, buff=0.14)
            return VGroup(box, ly, ly_lbl), ly

        l_cell, l_lyso = mini_cell(left_c)
        r_cell, r_lyso = mini_cell(right_c)

        scrub_x = -6.05
        scrub_track = Line([scrub_x, -1.9, 0], [scrub_x, 2.2, 0], color=GREY, stroke_width=4.0)
        scrub_t = ValueTracker(0.0)
        scrub_knob = always_redraw(lambda: Dot([scrub_x, -1.9 + 4.1 * scrub_t.get_value(), 0], radius=0.13, color=YELLOW))
        scrub_lbl = T("time", 24, TEXT).next_to(scrub_track, UP, buff=0.14).align_to([-6.3, 0, 0], LEFT)

        pile_offsets = [
            np.array([-1.11, 0.74, 0]),
            np.array([-0.72, -0.66, 0]),
            np.array([0.12, 0.65, 0]),
            np.array([0.12, -0.32, 0]),
        ]
        l_pile = VGroup(*[build_autophagosome(left_c + off, radius=0.29, cargo_radius=0.14) for off in pile_offsets])
        r_pile = VGroup(*[build_autophagosome(right_c + off, radius=0.29, cargo_radius=0.14) for off in pile_offsets])

        single_grp = VGroup(cell, er, lyso, carrier, lyso_lab, auto_lab)
        two_grp = VGroup(l_cell, r_cell, l_pile, r_pile, scrub_track, scrub_lbl, scrub_knob)
        self.play(FadeOut(single_grp), FadeIn(two_grp), run_time=0.8)
        self.play(
            l_pile.animate.shift(RIGHT * 0.08),
            r_pile.animate.shift(RIGHT * 0.08),
            run_time=max(0.4, dt_to(self, "is autophagy faster")),
        )

        self.at("is autophagy faster")
        l_ring = DashedVMobject(RoundedRectangle(corner_radius=0.35, width=2.04, height=2.16, stroke_color=YELLOW, stroke_width=3.0).move_to(left_c + LEFT * 0.43 + UP * 0.07), num_dashes=20)
        r_ring = DashedVMobject(RoundedRectangle(corner_radius=0.35, width=2.04, height=2.16, stroke_color=YELLOW, stroke_width=3.0).move_to(right_c + LEFT * 0.43 + UP * 0.07), num_dashes=20)
        self.play(Create(l_ring), Create(r_ring), run_time=1.3)
        self.play(
            FadeOut(l_ring), FadeOut(r_ring),
            run_time=max(0.4, dt_to(self, "makes and clears")),
        )

        self.at("makes and clears")
        l_head = T("fast arrival, fast exit", 26, BLUE).next_to(l_cell[0], UP, buff=0.18)
        in_c1 = build_autophagosome(left_c + np.array([-1.95, 1.45, 0]), radius=0.29, cargo_radius=0.14)
        in_c2 = build_autophagosome(left_c + np.array([-1.95, 0.0, 0]), radius=0.29, cargo_radius=0.14)
        self.play(FadeIn(l_head), run_time=0.4)
        self.play(
            scrub_t.animate.set_value(0.55),
            l_pile[2].animate.move_to(l_lyso.get_center()).set_opacity(0.15),
            l_pile[3].animate.move_to(l_lyso.get_center()).set_opacity(0.15),
            FadeIn(in_c1, shift=RIGHT * 0.35),
            FadeIn(in_c2, shift=RIGHT * 0.35),
            run_time=1.4,
        )
        self.remove(l_pile[2], l_pile[3])
        self.play(
            scrub_t.animate.set_value(1.0),
            MoveAlongPath(in_c1, ArcBetweenPoints(in_c1.get_center(), left_c + pile_offsets[2] + RIGHT * 0.08, angle=-1.25)),
            MoveAlongPath(in_c2, ArcBetweenPoints(in_c2.get_center(), left_c + pile_offsets[3] + RIGHT * 0.08, angle=-0.8)),
            run_time=max(0.5, dt_to(self, "makes them slowly")),
        )

        self.at("makes them slowly")
        scrub_t.set_value(0.0)
        r_head = T("slow arrival, blocked exit", 26, RED).next_to(r_cell[0], UP, buff=0.18)
        slow_in = build_autophagosome(right_c + np.array([-1.95, 0.0, 0]), radius=0.29, cargo_radius=0.14)
        r_pile[3].set_opacity(0)
        self.play(FadeIn(r_head), FadeIn(slow_in), run_time=max(0.4, dt_to(self, "exit is blocked")))

        self.at("exit is blocked")
        r_block = build_exit_block(center=r_lyso.get_left() + LEFT * 0.12, height=1.1)
        block_lbl = T("blocked", 24, RED).next_to(r_lyso, UP, buff=0.20)
        self.play(
            FadeIn(r_block, shift=DOWN * 0.15),
            FadeIn(block_lbl),
            scrub_t.animate.set_value(1.0),
            MoveAlongPath(slow_in, ArcBetweenPoints(slow_in.get_center(), right_c + pile_offsets[3] + RIGHT * 0.08, angle=-0.8)),
            run_time=max(0.8, dt_to(self, "still picture")),
        )
        self.remove(r_pile[3])

        self.at("still picture")
        cap = caption("Same pile size, opposite flows.", color=YELLOW)
        eq_l = RoundedRectangle(corner_radius=0.25, width=2.04, height=2.16, stroke_color=YELLOW, stroke_width=2.8).move_to(left_c + LEFT * 0.43 + UP * 0.07)
        eq_r = RoundedRectangle(corner_radius=0.25, width=2.04, height=2.16, stroke_color=YELLOW, stroke_width=2.8).move_to(right_c + LEFT * 0.43 + UP * 0.07)
        self.play(FadeIn(cap), Create(eq_l), Create(eq_r), run_time=2.0)
        self.finish()


# ------------------------------------------------------------------ s02_title
class S02Title(TitleCard):
    LESSON = "Protein Quality Control and Organelle Turnover"
    TITLE = "Follow the Flow, Not the Pile"


# ------------------------------------------------------------------ s03_er_route
class S03ErRoute(SpokenScene):
    def construct(self):
        er_box = RoundedRectangle(
            corner_radius=0.45,
            width=6.4,
            height=5.3,
            stroke_color=GREY,
            stroke_width=3.5,
            fill_color=CYTO,
            fill_opacity=1.0,
        ).move_to([-2.8, 0.0, 0])
        er_lbl = T("ER lumen", 28, TEXT).move_to([-4.6, 2.15, 0])
        cyt_lbl = T("cytosol", 28, TEXT).move_to([2.4, 2.15, 0])
        client = build_squiggle(center=[-5.0, 0.2, 0], width=1.3, amp=0.28, color=GREY)
        client_lbl = T("client", 26, TEXT).next_to(client, UP, buff=0.18)

        self.play(FadeIn(er_box), FadeIn(er_lbl), FadeIn(client), FadeIn(client_lbl), run_time=0.8)
        self.play(
            client.animate.move_to([-3.6, 0.2, 0]),
            client_lbl.animate.move_to([-3.6, 0.78, 0]),
            run_time=max(0.5, dt_to(self, "uses helpers")),
        )

        self.at("uses helpers")
        helper_top = RoundedRectangle(corner_radius=0.14, width=1.35, height=0.56, stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.32).move_to([-2.4, 0.95, 0])
        helper_bot = RoundedRectangle(corner_radius=0.14, width=1.35, height=0.56, stroke_color=TEAL, stroke_width=3.2, fill_color=TEAL, fill_opacity=0.32).move_to([-2.4, -0.55, 0])
        helpers_lbl = T("helpers", 26, TEAL).next_to(helper_bot, DOWN, buff=0.20)
        loop_arc = CurvedArrow([-1.45, 0.55, 0], [-1.45, -0.15, 0], angle=-TAU * 0.55, color=TEAL, stroke_width=3.8)

        self.play(FadeIn(helper_top), FadeIn(helper_bot), FadeIn(helpers_lbl), run_time=0.7)
        self.play(
            client.animate.move_to([-2.4, 0.2, 0]),
            client_lbl.animate.move_to([-2.4, 1.62, 0]),
            helper_top.animate.shift(DOWN * 0.35),
            helper_bot.animate.shift(UP * 0.35),
            run_time=1.4,
        )
        self.play(
            helper_top.animate.shift(UP * 0.35),
            helper_bot.animate.shift(DOWN * 0.35),
            Create(loop_arc),
            run_time=1.3,
        )
        self.play(
            client.animate.shift(RIGHT * 0.55),
            helper_top.animate.shift(DOWN * 0.32),
            helper_bot.animate.shift(UP * 0.32),
            run_time=max(0.5, dt_to(self, "first picture")),
        )

        self.at("first picture")
        fp_lbl = T("first picture", 26, TEAL).move_to([-2.4, -1.95, 0])
        self.play(FadeIn(fp_lbl, shift=UP * 0.1), run_time=0.7)
        # Active second retry sweep across the pause
        self.play(
            helper_top.animate.shift(UP * 0.32),
            helper_bot.animate.shift(DOWN * 0.32),
            client.animate.shift(LEFT * 0.85),
            run_time=1.7,
        )
        self.play(
            helper_top.animate.shift(DOWN * 0.32),
            helper_bot.animate.shift(UP * 0.32),
            client.animate.shift(RIGHT * 0.45),
            run_time=max(0.5, dt_to(self, "returned to the cytosol")),
        )

        self.at("returned to the cytosol")
        self.play(FadeOut(fp_lbl), FadeOut(loop_arc), FadeIn(cyt_lbl), run_time=0.4)
        self.play(
            helper_top.animate.shift(UP * 0.32),
            helper_bot.animate.shift(DOWN * 0.32),
            client.animate.move_to([1.55, 0.2, 0]),
            client_lbl.animate.move_to([1.55, 0.85, 0]),
            run_time=max(0.6, dt_to(self, "tagged with ubiquitin")),
        )

        self.at("tagged with ubiquitin")
        self.play(FadeOut(client_lbl), run_time=0.25)
        ub_dot = Circle(radius=0.18, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.95).next_to(client, UP, buff=0.06)
        ub_lbl = T("ubiquitin", 26, RED).next_to(ub_dot, UP, buff=0.16)
        self.play(FadeIn(ub_dot, scale=0.6), FadeIn(ub_lbl, shift=UP * 0.1), run_time=max(0.4, dt_to(self, "destroyed by the proteasome")))

        self.at("destroyed by the proteasome")
        prot = build_proteasome(center=(4.15, 0.2, 0), scale=1.55)
        prot_lbl = T("proteasome", 28, GOLD).next_to(prot, DOWN, buff=0.25)
        tagged = VGroup(client, ub_dot)
        self.play(FadeIn(prot), FadeIn(prot_lbl), run_time=0.9)
        self.play(
            tagged.animate.move_to([1.95, 0.2, 0]),
            ub_lbl.animate.move_to([1.95, 1.15, 0]),
            run_time=max(0.6, dt_to(self, "ubiquitin is")),
        )

        self.at("ubiquitin is")
        # Progressive unfolding + approach into proteasome cap driven by unfold_t (0 -> 1)
        self.remove(client, ub_dot)
        unfold_t = ValueTracker(0.0)
        live_chain = always_redraw(lambda: build_squiggle(
            center=[1.95 + 0.95 * unfold_t.get_value(), 0.2, 0],
            width=1.35 + 0.25 * unfold_t.get_value(),
            amp=0.28 * (1.0 - 0.85 * unfold_t.get_value()),
            color=GREY,
        ))
        live_ub = always_redraw(lambda: Circle(
            radius=0.18,
            stroke_color=RED,
            stroke_width=2.5,
            fill_color=RED,
            fill_opacity=0.95,
        ).move_to([1.95 + 1.25 * unfold_t.get_value(), 0.72 + 0.10 * unfold_t.get_value(), 0]))
        self.add(live_chain, live_ub)
        self.play(
            unfold_t.animate.set_value(0.65),
            ub_lbl.animate.move_to([2.65, 1.22, 0]),
            run_time=max(0.8, dt_to(self, "capped barrel")),
            rate_func=linear,
        )

        self.at("capped barrel")
        self.play(
            unfold_t.animate.set_value(1.0),
            FadeOut(ub_lbl),
            run_time=max(0.6, dt_to(self, "unfolds and destroys")),
            rate_func=linear,
        )

        self.at("unfolds and destroys")
        live_chain.clear_updaters()
        live_ub.clear_updaters()
        straight = Line([2.15, 0.2, 0], [3.65, 0.2, 0], color=GREY, stroke_width=5.5)
        self.remove(live_chain)
        self.add(straight)
        self.play(
            straight.animate.put_start_and_end_on([3.60, 0.2, 0], [5.15, 0.2, 0]),
            FadeOut(live_ub),
            run_time=1.8,
        )
        frags = VGroup(*[
            Square(side_length=0.22, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.85).move_to([5.4 + 0.30 * (i % 2), 0.2 + 0.26 * (i // 2 - 0.5), 0])
            for i in range(4)
        ])
        self.play(ReplacementTransform(straight, frags), run_time=0.8)
        self.play(frags.animate.shift(RIGHT * 0.65).set_opacity(0.25), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ s04_lysosome_route
class S04LysosomeRoute(SpokenScene):
    def construct(self):
        cell = build_cell_outline(center=(-0.15, 0.15, 0), width=10.6, height=5.3)
        er = build_er_patch(center=(-3.7, 0.15, 0), scale=0.95)
        prot = build_proteasome(center=(3.15, 1.75, 0), scale=1.05)
        prot_lbl = T("proteasome", 26, GOLD).next_to(prot, DOWN, buff=0.18)
        lyso = build_lysosome(center=(3.05, -0.75, 0), radius=0.95)
        lyso_lbl = T("lysosome", 28, ORANGE).next_to(lyso, DOWN, buff=0.16)
        tag = scope_tag("schematic")

        self.play(FadeIn(cell), FadeIn(er), FadeIn(prot), FadeIn(prot_lbl), FadeIn(lyso), FadeIn(lyso_lbl), FadeIn(tag), run_time=0.6)

        self.at("damaged mitochondrion")
        mito = build_mitochondrion(center=(-2.1, 1.75, 0), width=1.95, height=0.96)
        mito_lbl = T("mitochondrion", 26, TEXT).next_to(mito, UP, buff=0.16)
        self.play(FadeIn(mito), FadeIn(mito_lbl), run_time=0.7)
        self.play(
            mito.animate.move_to([1.25, 1.75, 0]),
            mito_lbl.animate.move_to([1.25, 2.48, 0]),
            run_time=max(0.8, dt_to(self, "cannot enter")),
        )

        self.at("cannot enter")
        self.play(mito.animate.shift(RIGHT * 0.30), mito_lbl.animate.shift(RIGHT * 0.30), run_time=0.55)
        self.play(mito.animate.shift(LEFT * 0.55), mito_lbl.animate.shift(LEFT * 0.55), run_time=0.75)
        self.play(
            mito.animate.move_to([0.10, 0.85, 0]),
            mito_lbl.animate.move_to([0.10, 1.58, 0]),
            run_time=max(0.5, dt_to(self, "different physical solution")),
        )

        self.at("different physical solution")
        self.play(
            mito.animate.move_to([-0.65, -0.25, 0]),
            mito_lbl.animate.move_to([-0.65, 0.50, 0]),
            run_time=max(0.6, dt_to(self, "blue membrane cup") - 0.35),
        )
        self.play(FadeOut(mito_lbl), run_time=0.35)

        self.at("blue membrane cup")
        c = mito.get_center()
        arc_out_t = ValueTracker(0.15)
        arc_out = always_redraw(lambda: Arc(radius=1.18, start_angle=PI - arc_out_t.get_value() * PI, angle=arc_out_t.get_value() * TAU, arc_center=c, stroke_color=BLUE, stroke_width=5.5))
        arc_in = always_redraw(lambda: Arc(radius=1.00, start_angle=PI - arc_out_t.get_value() * PI, angle=arc_out_t.get_value() * TAU, arc_center=c, stroke_color=BLUE, stroke_width=3.6))
        self.add(arc_out, arc_in)
        self.play(arc_out_t.animate.set_value(0.68), run_time=max(0.8, dt_to(self, "closes into")))

        self.at("closes into")
        self.play(arc_out_t.animate.set_value(1.0), run_time=1.3)
        self.remove(arc_out, arc_in)
        outer_ring = Circle(radius=1.18, stroke_color=BLUE, stroke_width=5.5, fill_color=BLUE, fill_opacity=0.14).move_to(c)
        inner_ring = Circle(radius=1.00, stroke_color=BLUE, stroke_width=3.6, fill_opacity=0.0).move_to(c)
        self.add(outer_ring, inner_ring)
        auto_lbl = T("autophagosome", 26, BLUE).next_to(outer_ring, UP, buff=0.18)
        self.play(FadeIn(auto_lbl), run_time=max(0.5, dt_to(self, "autophagosomes carry")))

        self.at("autophagosomes carry")
        carrier = VGroup(outer_ring, inner_ring, mito)
        # Also show bulk-cytoplasm carrier arriving alongside organelle carrier
        cyto_carrier = build_autophagosome(center=(-2.2, -1.75, 0), radius=0.34, cargo_radius=0.16)
        self.play(FadeIn(cyto_carrier), run_time=0.5)
        self.play(
            carrier.animate.move_to([1.00, -0.42, 0]).scale(0.80),
            auto_lbl.animate.move_to([0.80, 0.80, 0]),
            cyto_carrier.animate.move_to([0.45, -1.82, 0]),
            run_time=max(1.0, dt_to(self, "carrier fuses")),
            rate_func=linear,
        )

        self.at("carrier fuses")
        self.play(
            FadeOut(auto_lbl),
            FadeOut(cyto_carrier),
            carrier.animate.move_to(lyso.get_center()).scale(0.72),
            run_time=1.6,
        )
        self.play(
            outer_ring.animate.scale(1.42).set_stroke(color=ORANGE, opacity=0.0),
            run_time=max(0.5, dt_to(self, "digests the cargo")),
        )
        self.remove(outer_ring)

        self.at("digests the cargo")
        blocks = VGroup(*[
            Square(side_length=0.24, stroke_color=TEXT, stroke_width=2.0, fill_color=GREY, fill_opacity=0.88)
            for _ in range(6)
        ]).arrange_in_grid(2, 3, buff=0.14).move_to(lyso.get_center())
        blocks_lbl = T("reusable blocks", 26, TEXT).next_to(lyso, UP, buff=0.18)
        self.play(ReplacementTransform(VGroup(inner_ring, mito), blocks), FadeIn(blocks_lbl), run_time=1.4)
        self.play(blocks.animate.arrange_in_grid(2, 3, buff=0.22).move_to(lyso.get_center()), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s05_starvation
class S05Starvation(SpokenScene):
    def construct(self):
        cell_c = np.array([-1.4, 0.05, 0.0])
        cell = build_cell_outline(center=cell_c, width=8.6, height=5.1)
        lyso = build_lysosome(center=(1.65, -0.55, 0), radius=0.88)
        lyso_lbl = T("lysosome", 26, ORANGE).next_to(lyso, DOWN, buff=0.16)
        tag = scope_tag("schematic")

        inlet_top = Line([-6.2, 1.45, 0], [-4.0, 1.45, 0], color=TEXT, stroke_width=3.5)
        inlet_bot = Line([-6.2, 0.85, 0], [-4.0, 0.85, 0], color=TEXT, stroke_width=3.5)
        inlet_arrow = Arrow([-5.9, 1.15, 0], [-4.1, 1.15, 0], color=GREY, stroke_width=4.5, buff=0)

        bin_c = np.array([-2.6, 0.1, 0.0])
        bin_w, bin_h = 1.5, 2.25
        bin_frame = RoundedRectangle(corner_radius=0.1, width=bin_w, height=bin_h, stroke_color=TEXT, stroke_width=3.0, fill_opacity=0.0).move_to(bin_c)
        bin_lbl = T("reuse bin", 26, TEXT).next_to(bin_frame, DOWN, buff=0.16)
        bin_lvl = ValueTracker(0.84)
        bin_fill = always_redraw(lambda: Rectangle(
            width=bin_w - 0.12,
            height=max(0.06, (bin_h - 0.12) * bin_lvl.get_value()),
            stroke_width=0,
            fill_color=GREY,
            fill_opacity=0.78,
        ).move_to([bin_c[0], bin_c[1] - (bin_h - 0.12) / 2 + max(0.06, (bin_h - 0.12) * bin_lvl.get_value()) / 2, 0]))

        starv_lbl = T("starvation", 30, RED).move_to([-4.6, 2.95, 0])

        self.play(
            FadeIn(cell), FadeIn(lyso), FadeIn(lyso_lbl), FadeIn(tag),
            FadeIn(inlet_top), FadeIn(inlet_bot), FadeIn(inlet_arrow),
            FadeIn(bin_frame), FadeIn(bin_fill), FadeIn(bin_lbl),
            FadeIn(starv_lbl),
            run_time=0.65,
        )
        self.play(
            inlet_top.animate.shift(DOWN * 0.22),
            inlet_bot.animate.shift(UP * 0.22),
            inlet_arrow.animate.set_stroke(width=1.5).set_opacity(0.35),
            run_time=max(0.8, dt_to(self, "begins to empty")),
        )

        self.at("begins to empty")
        self.play(bin_lvl.animate.set_value(0.24), run_time=max(0.8, dt_to(self, "more cytoplasm")))

        self.at("more cytoplasm")
        # Continuous autophagosome stream + return block stream driven by phase trackers
        auto_ph = ValueTracker(0.0)
        ret_ph = ValueTracker(0.0)
        p_start = np.array([-1.0, 1.35, 0.0])
        p_end = lyso.get_center()
        auto_stream = always_redraw(lambda: VGroup(*[
            build_autophagosome(
                p_start + ((auto_ph.get_value() + k / 3.0) % 1.0) * (p_end - p_start),
                radius=0.33,
                cargo_radius=0.16,
            )
            for k in range(3)
        ]))
        self.play(FadeIn(auto_stream), run_time=0.45)
        self.play(
            auto_ph.animate.set_value(1.8),
            run_time=max(0.8, dt_to(self, "sends recovered blocks")),
            rate_func=linear,
        )

        self.at("sends recovered blocks")
        ret_arc = CurvedArrow(lyso.get_left() + LEFT * 0.1 + DOWN * 0.1, bin_frame.get_right() + RIGHT * 0.1 + DOWN * 0.4, angle=-0.5, color=GREY, stroke_width=3.5)
        r_start = lyso.get_left() + LEFT * 0.15 + DOWN * 0.15
        r_end = bin_frame.get_right() + RIGHT * 0.05 + DOWN * 0.45
        ret_stream = always_redraw(lambda: VGroup(*[
            Square(side_length=0.22, stroke_color=TEXT, stroke_width=1.8, fill_color=GREY, fill_opacity=0.90).move_to(
                r_start + ((ret_ph.get_value() + k / 3.0) % 1.0) * (r_end - r_start) + DOWN * 0.28 * np.sin(PI * ((ret_ph.get_value() + k / 3.0) % 1.0))
            )
            for k in range(3)
        ]))
        self.play(Create(ret_arc), FadeIn(ret_stream), run_time=0.6)
        self.play(
            auto_ph.animate.set_value(3.3),
            ret_ph.animate.set_value(1.5),
            bin_lvl.animate.set_value(0.54),
            run_time=max(0.8, dt_to(self, "during starvation autophagy")),
            rate_func=linear,
        )

        self.at("during starvation autophagy")
        self.play(
            auto_ph.animate.set_value(6.5),
            ret_ph.animate.set_value(4.5),
            bin_lvl.animate.set_value(0.64),
            run_time=max(1.2, dt_to(self, "yeast lose viability")),
            rate_func=linear,
        )

        self.at("yeast lose viability")
        def yeast_icon(center, intact=True):
            c = np.array(center, dtype=float)
            col = GREEN if intact else RED
            body = Ellipse(width=1.15, height=0.82, stroke_color=col, stroke_width=3.0, fill_color=col, fill_opacity=0.16).move_to(c)
            bud = Circle(radius=0.22, stroke_color=col, stroke_width=2.6, fill_color=col, fill_opacity=0.16).move_to(c + np.array([0.52, 0.32, 0]))
            route = Arrow(c + LEFT * 0.35, c + RIGHT * 0.35, color=BLUE, stroke_width=3.5, buff=0)
            parts = [body, bud, route]
            if not intact:
                x1 = Line(c + np.array([-0.26, -0.22, 0]), c + np.array([0.26, 0.22, 0]), color=RED, stroke_width=4.0)
                x2 = Line(c + np.array([-0.26, 0.22, 0]), c + np.array([0.26, -0.22, 0]), color=RED, stroke_width=4.0)
                parts.extend([x1, x2])
            return VGroup(*parts)

        y_norm = yeast_icon((4.85, 1.25, 0), intact=True)
        y_norm_lbl = T("normal yeast", 24, GREEN).next_to(y_norm, DOWN, buff=0.16)
        y_def = yeast_icon((4.85, -0.95, 0), intact=False)
        y_def_lbl = T("autophagy-defective", 24, RED).next_to(y_def, DOWN, buff=0.16)

        self.play(
            FadeIn(y_norm), FadeIn(y_norm_lbl), FadeIn(y_def), FadeIn(y_def_lbl),
            auto_ph.animate.set_value(8.2),
            ret_ph.animate.set_value(6.2),
            run_time=3.5,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ s06_rule
class S06Rule(SpokenScene):
    def construct(self):
        eq = M("pool change = arrival − clearance", size=30, color=TEXT).move_to([-0.5, 3.05, 0])
        tag = scope_tag("schematic")

        pool_c = np.array([-0.6, -0.1, 0.0])
        pool_box = RoundedRectangle(corner_radius=0.25, width=2.5, height=3.2, stroke_color=BLUE, stroke_width=3.6, fill_color=CYTO, fill_opacity=1.0).move_to(pool_c)
        pool_lbl = T("carrier pool", 26, BLUE).next_to(pool_box, DOWN, buff=0.2)

        gauge_c = np.array([4.8, -0.1, 0.0])
        gauge_w, gauge_h = 0.78, 3.2
        gauge_frame = RoundedRectangle(corner_radius=0.08, width=gauge_w, height=gauge_h, stroke_color=TEXT, stroke_width=2.8, fill_color=CYTO, fill_opacity=1.0).move_to(gauge_c)
        gauge_lbl = T("pool level", 24, TEXT).next_to(gauge_frame, DOWN, buff=0.2)
        pool_lvl = ValueTracker(0.42)
        gauge_fill = always_redraw(lambda: Rectangle(
            width=gauge_w - 0.12,
            height=max(0.06, (gauge_h - 0.12) * pool_lvl.get_value()),
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.85,
        ).move_to([gauge_c[0], gauge_c[1] - (gauge_h - 0.12) / 2 + max(0.06, (gauge_h - 0.12) * pool_lvl.get_value()) / 2, 0]))

        arr_w = ValueTracker(5.5)
        clr_w = ValueTracker(5.5)
        arr_arrow = always_redraw(lambda: Arrow([-5.1, -0.1, 0], [-2.05, -0.1, 0], color=BLUE, stroke_width=arr_w.get_value(), max_tip_length_to_length_ratio=0.18, buff=0))
        clr_arrow = always_redraw(lambda: Arrow([0.85, -0.1, 0], [3.9, -0.1, 0], color=ORANGE, stroke_width=clr_w.get_value(), max_tip_length_to_length_ratio=0.18, buff=0))
        arr_lbl = T("arrival", 28, BLUE).move_to([-3.65, 0.65, 0])
        clr_lbl = T("clearance", 28, ORANGE).move_to([2.35, 0.65, 0])

        in_phase = ValueTracker(0.0)
        out_phase = ValueTracker(0.0)
        in_dots = always_redraw(lambda: VGroup(*[
            build_autophagosome([-5.0 + ((in_phase.get_value() + k / 3.0) % 1.0) * 2.70, -0.1, 0], radius=0.22, cargo_radius=0.10)
            for k in range(3)
        ]))
        out_dots = always_redraw(lambda: VGroup(*[
            Circle(radius=0.20, stroke_color=ORANGE, stroke_width=3.0, fill_color=ORANGE, fill_opacity=0.45).move_to([1.0 + ((out_phase.get_value() + k / 3.0) % 1.0) * 2.65, -0.1, 0])
            for k in range(3)
        ]))

        rng = np.random.default_rng(7)
        dot_coords = rng.uniform(-0.85, 0.85, size=(12, 2))
        dot_coords[:, 1] = np.linspace(-1.15, 1.15, 12)
        pool_dots = always_redraw(lambda: VGroup(*[
            Dot([pool_c[0] + x, pool_c[1] + y, 0], radius=0.12, color=BLUE)
            for idx, (x, y) in enumerate(dot_coords)
            if idx < max(2, int(round(pool_lvl.get_value() * 12)))
        ]))

        self.play(
            FadeIn(pool_box), FadeIn(pool_lbl),
            FadeIn(arr_arrow), FadeIn(clr_arrow), FadeIn(arr_lbl), FadeIn(clr_lbl),
            FadeIn(gauge_frame), FadeIn(gauge_fill), FadeIn(gauge_lbl),
            FadeIn(in_dots), FadeIn(out_dots), FadeIn(pool_dots),
            FadeIn(tag),
            run_time=1.0,
        )
        self.play(
            in_phase.animate.set_value(2.4),
            out_phase.animate.set_value(2.4),
            run_time=max(0.6, dt_to(self, "change equals arrival")),
            rate_func=linear,
        )

        self.at("change equals arrival")
        self.play(
            FadeIn(eq, shift=RIGHT * 0.2),
            in_phase.animate.set_value(4.5),
            out_phase.animate.set_value(4.5),
            run_time=max(0.8, dt_to(self, "matching rates")),
            rate_func=linear,
        )

        self.at("matching rates")
        state_lbl = T("equal rates", 26, TEXT).move_to([-0.6, 2.0, 0])
        self.play(
            FadeIn(state_lbl),
            in_phase.animate.set_value(6.0),
            out_phase.animate.set_value(6.0),
            run_time=max(0.6, dt_to(self, "faster arrival makes")),
            rate_func=linear,
        )

        self.at("faster arrival makes")
        fast_lbl = T("faster arrival", 26, BLUE).move_to([-0.6, 2.0, 0])
        self.play(swap(state_lbl, fast_lbl, run_time=0.4), arr_w.animate.set_value(12.0), run_time=0.45)
        self.play(
            pool_lvl.animate.set_value(0.88),
            in_phase.animate.set_value(8.7),
            out_phase.animate.set_value(6.8),
            run_time=max(0.8, dt_to(self, "slower clearance")),
            rate_func=linear,
        )

        self.at("slower clearance")
        slow_lbl = T("slower clearance", 26, ORANGE).move_to([-0.6, 2.0, 0])
        self.play(
            swap(fast_lbl, slow_lbl, run_time=0.4),
            arr_w.animate.set_value(5.5),
            pool_lvl.animate.set_value(0.42),
            run_time=0.45,
        )
        self.play(clr_w.animate.set_value(2.0), run_time=0.35)
        self.play(
            pool_lvl.animate.set_value(0.88),
            in_phase.animate.set_value(10.8),
            out_phase.animate.set_value(7.4),
            run_time=max(0.8, dt_to(self, "larger pool can mean")),
            rate_func=linear,
        )

        self.at("larger pool can mean")
        both_lbl = T("faster arrival or slower clearance?", 26, YELLOW).move_to([-0.6, 2.0, 0])
        self.play(swap(slow_lbl, both_lbl, run_time=0.45), run_time=0.5)
        self.play(
            in_phase.animate.set_value(13.8),
            out_phase.animate.set_value(8.5),
            arr_lbl.animate.set_color(YELLOW),
            run_time=3.6,
            rate_func=linear,
        )
        self.play(
            in_phase.animate.set_value(16.6),
            out_phase.animate.set_value(9.5),
            arr_lbl.animate.set_color(BLUE),
            clr_lbl.animate.set_color(YELLOW),
            run_time=3.6,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ shared builder for s07 / s08 / s09
def build_predict_panels(left_lvl=0.45, right_lvl=0.45, blocked=True, lc3_marked=True, show_baseline=False):
    """Two synchronized recycling panels carried across s07_predict, s08_pause, s09_reveal."""
    tp = TwoPanel("fast arrival", "slow arrival", colors=(BLUE, TEAL), top=2.85, bottom=-2.20, gap=0.45, width=12.4, size=30)

    def panel_content(side, lvl_val, fast=True):
        c, w, h = tp.area(side)
        # Compact cell map leaving space on left for 0.95u arrival stream and on right for labels & gauge
        cell_c = c + np.array([-0.70, 0.05, 0.0])
        cell = RoundedRectangle(corner_radius=0.38, width=2.35, height=2.90, stroke_color=TEXT, stroke_width=2.6, fill_color=CYTO, fill_opacity=1.0).move_to(cell_c)
        lyso_c = cell_c + np.array([0.68, -0.05, 0.0])
        lyso = build_lysosome(center=lyso_c, radius=0.40)
        arr = Arrow(
            cell_c + np.array([-2.14, 0.0, 0.0]),
            cell_c + np.array([-1.19, 0.0, 0.0]),
            color=BLUE,
            stroke_width=10.5 if fast else 3.0,
            max_stroke_width_to_length_ratio=20,
            max_tip_length_to_length_ratio=0.26,
            buff=0,
        )
        pool_pts = [np.array([-0.76, 0.90, 0]), np.array([-0.26, 0.90, 0]), np.array([-0.76, -0.90, 0]), np.array([-0.26, -0.90, 0])]
        carriers = VGroup(*[build_autophagosome(cell_c + p, radius=0.18, lc3=lc3_marked, cargo_radius=0.08) for p in pool_pts])
        block = build_exit_block(center=lyso.get_left() + LEFT * 0.09, height=0.60)
        if not blocked:
            block.set_opacity(0)

        gc = c + np.array([2.42, 0.02, 0.0])
        gw, gh = 0.56, 2.35
        g_frame = RoundedRectangle(corner_radius=0.06, width=gw, height=gh, stroke_color=TEXT, stroke_width=2.5, fill_color=CYTO, fill_opacity=1.0).move_to(gc)
        g_h = max(0.06, (gh - 0.1) * lvl_val)
        g_fill = Rectangle(width=gw - 0.1, height=g_h, stroke_width=0, fill_color=PURPLE, fill_opacity=0.88).move_to([gc[0], gc[1] - (gh - 0.1) / 2 + g_h / 2, 0])
        g_lbl = T("LC3-II", 24, PURPLE).next_to(g_frame, DOWN, buff=0.14)
        schem = T("schematic", 24, GREY).move_to([cell_c[0], c[1] - h / 2 + 0.16, 0])
        return VGroup(cell, lyso, arr, carriers, block, g_frame, g_fill, g_lbl, schem), gc, gw, gh

    l_grp, l_gc, gw, gh = panel_content("left", left_lvl, fast=True)
    r_grp, r_gc, _, _ = panel_content("right", right_lvl, fast=False)
    out = VGroup(tp, l_grp, r_grp)
    if show_baseline:
        base_y = l_gc[1] - (gh - 0.1) / 2 + (gh - 0.1) * 0.45
        dash_l = DashedLine([l_gc[0] - 0.40, base_y, 0], [l_gc[0] + 0.40, base_y, 0], color=TEXT, stroke_width=2.5)
        dash_r = DashedLine([r_gc[0] - 0.40, base_y, 0], [r_gc[0] + 0.40, base_y, 0], color=TEXT, stroke_width=2.5)
        out.add(dash_l, dash_r)
    return out


# ------------------------------------------------------------------ s07_predict
class S07Predict(SpokenScene):
    QUESTION = "After bafilomycin, which LC3-II pool rises more:\nfast arrival or slow arrival?"

    def construct(self):
        world = build_predict_panels(left_lvl=0.45, right_lvl=0.45, blocked=False, lc3_marked=False, show_baseline=False)
        tp, l_grp, r_grp = world[0], world[1], world[2]
        l_block, r_block = l_grp[4], r_grp[4]
        l_carriers, r_carriers = l_grp[3], r_grp[3]
        l_arr, r_arr = l_grp[2], r_grp[2]
        l_c = tp.area("left")[0]
        r_c = tp.area("right")[0]

        ph_l = ValueTracker(0.0)
        ph_r = ValueTracker(0.0)
        l_start, l_end = l_arr.get_start(), l_arr.get_end()
        r_start, r_end = r_arr.get_start(), r_arr.get_end()
        dots_l = always_redraw(lambda: VGroup(*[
            build_autophagosome(l_start + (0.12 + 0.76 * ((ph_l.get_value() + k / 2.0) % 1.0)) * (l_end - l_start), radius=0.125, lc3=True, cargo_radius=0.06)
            for k in range(2)
        ]))
        dots_r = always_redraw(lambda: build_autophagosome(r_start + (0.12 + 0.76 * (ph_r.get_value() % 1.0)) * (r_end - r_start), radius=0.125, lc3=True, cargo_radius=0.06))

        self.play(FadeIn(world), FadeIn(dots_l), FadeIn(dots_r), run_time=0.8)
        self.play(
            ph_l.animate.set_value(2.2),
            ph_r.animate.set_value(0.7),
            run_time=max(0.5, dt_to(self, "attached to")),
            rate_func=linear,
        )

        self.at("attached to")
        l_marks = VGroup(*[
            Dot(car.get_center() + 0.19 * np.array([np.cos(a), np.sin(a), 0]), radius=0.036, color=PURPLE)
            for car in l_carriers for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        r_marks = VGroup(*[
            Dot(car.get_center() + 0.19 * np.array([np.cos(a), np.sin(a), 0]), radius=0.036, color=PURPLE)
            for car in r_carriers for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        lc3_callout = T("LC3-II", 26, PURPLE).move_to([l_c[0] + 1.31, 0.75, 0])
        self.play(
            FadeIn(l_marks, scale=0.6), FadeIn(r_marks, scale=0.6), FadeIn(lc3_callout),
            ph_l.animate.set_value(4.5), ph_r.animate.set_value(1.5),
            run_time=1.8, rate_func=linear,
        )
        self.play(
            ph_l.animate.set_value(8.5), ph_r.animate.set_value(2.8),
            run_time=max(0.6, dt_to(self, "blocks lysosomal acidification")),
            rate_func=linear,
        )

        self.at("blocks lysosomal acidification")
        l_block.set_opacity(1)
        r_block.set_opacity(1)
        baf_l = T("bafilomycin", 24, RED).move_to([l_grp[0].get_center()[0] + 0.55, 1.80, 0])
        baf_r = T("bafilomycin", 24, RED).move_to([r_grp[0].get_center()[0] + 0.55, 1.80, 0])
        self.play(
            FadeOut(lc3_callout),
            FadeIn(l_block, shift=DOWN * 0.15), FadeIn(r_block, shift=DOWN * 0.15),
            FadeIn(baf_l), FadeIn(baf_r),
            ph_l.animate.set_value(11.0), ph_r.animate.set_value(3.6),
            run_time=1.8, rate_func=linear,
        )
        self.play(
            ph_l.animate.set_value(17.5), ph_r.animate.set_value(5.6),
            run_time=max(0.8, dt_to(self, "pools start equally high")),
            rate_func=linear,
        )

        self.at("pools start equally high")
        l_gc, r_gc = l_grp[5].get_center(), r_grp[5].get_center()
        gh = 2.35
        base_y = l_gc[1] - (gh - 0.1) / 2 + (gh - 0.1) * 0.45
        dash_l = DashedLine([l_gc[0] - 0.40, base_y, 0], [l_gc[0] + 0.40, base_y, 0], color=TEXT, stroke_width=2.5)
        dash_r = DashedLine([r_gc[0] - 0.40, base_y, 0], [r_gc[0] + 0.40, base_y, 0], color=TEXT, stroke_width=2.5)
        self.play(FadeOut(baf_l), FadeOut(baf_r), run_time=0.4)
        self.play(
            Create(dash_l), Create(dash_r),
            ph_l.animate.set_value(22.0), ph_r.animate.set_value(7.0),
            run_time=max(0.8, dt_to(self, "which pool rises more")),
            rate_func=linear,
        )

        self.at("which pool rises more")
        q = question_card(self.QUESTION, y=BOTTOM_Y + 0.15)
        self.play(
            FadeIn(q),
            ph_l.animate.set_value(27.5), ph_r.animate.set_value(8.8),
            run_time=3.5,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ s08_pause
class S08Pause(PredictPause):
    QUESTION = S07Predict.QUESTION
    SECONDS = 4.5

    def backdrop(self):
        return build_predict_panels(left_lvl=0.45, right_lvl=0.45, blocked=True, lc3_marked=True, show_baseline=True)


# ------------------------------------------------------------------ s09_reveal
class S09Reveal(SpokenScene):
    def construct(self):
        world = build_predict_panels(left_lvl=0.45, right_lvl=0.45, blocked=True, lc3_marked=True, show_baseline=True)
        tp, l_grp, r_grp = world[0], world[1], world[2]
        l_frame, r_frame = l_grp[5], r_grp[5]
        l_gc, r_gc = l_frame.get_center(), r_frame.get_center()
        l_c, r_c = tp.area("left")[0], tp.area("right")[0]
        gw, gh = 0.56, 2.35
        base_y = l_gc[1] - (gh - 0.1) / 2 + (gh - 0.1) * 0.45

        l_lvl = ValueTracker(0.45)
        r_lvl = ValueTracker(0.45)

        def mk_fill(gc, trk):
            return always_redraw(lambda: Rectangle(
                width=gw - 0.1,
                height=max(0.06, (gh - 0.1) * trk.get_value()),
                stroke_width=0,
                fill_color=PURPLE,
                fill_opacity=0.88,
            ).move_to([gc[0], gc[1] - (gh - 0.1) / 2 + max(0.06, (gh - 0.1) * trk.get_value()) / 2, 0]))

        l_fill = mk_fill(l_gc, l_lvl)
        r_fill = mk_fill(r_gc, r_lvl)
        l_grp[6].set_opacity(0)
        r_grp[6].set_opacity(0)

        ph_l = ValueTracker(0.0)
        ph_r = ValueTracker(0.0)
        l_s, l_e = l_grp[2].get_start(), l_grp[2].get_end()
        r_s, r_e = r_grp[2].get_start(), r_grp[2].get_end()
        dots_l = always_redraw(lambda: VGroup(*[
            build_autophagosome(l_s + (0.12 + 0.76 * ((ph_l.get_value() + k / 2.0) % 1.0)) * (l_e - l_s), radius=0.125, lc3=True, cargo_radius=0.06)
            for k in range(2)
        ]))
        dots_r = always_redraw(lambda: build_autophagosome(r_s + (0.12 + 0.76 * (ph_r.get_value() % 1.0)) * (r_e - r_s), radius=0.125, lc3=True, cargo_radius=0.06))

        self.add(world, l_fill, r_fill, dots_l, dots_r)

        t_prog = ValueTracker(0.0)
        t_bar_bg = Line([-2.5, -3.05, 0], [2.5, -3.05, 0], color=GREY, stroke_width=5)
        t_bar = always_redraw(lambda: Line([-2.5, -3.05, 0], [-2.5 + 5.0 * max(0.01, t_prog.get_value()), -3.05, 0], color=TEAL, stroke_width=7))
        t_lbl = T("assay interval", 24, TEXT).next_to(t_bar_bg, LEFT, buff=0.22)
        self.play(FadeIn(t_bar_bg), FadeIn(t_bar), FadeIn(t_lbl), run_time=0.6)

        extra_l1 = build_autophagosome(l_grp[0].get_center() + np.array([-0.78, 0.0, 0]), radius=0.16, lc3=True, cargo_radius=0.07)
        extra_l2 = build_autophagosome(l_grp[0].get_center() + np.array([-0.24, 0.24, 0]), radius=0.16, lc3=True, cargo_radius=0.07)
        self.play(
            t_prog.animate.set_value(0.35),
            l_lvl.animate.set_value(0.64),
            r_lvl.animate.set_value(0.47),
            ph_l.animate.set_value(5.0), ph_r.animate.set_value(1.6),
            FadeIn(extra_l1, shift=RIGHT * 0.35),
            run_time=max(0.8, dt_to(self, "purple gauge climbs")),
            rate_func=linear,
        )

        self.at("purple gauge climbs")
        self.play(
            t_prog.animate.set_value(0.75),
            l_lvl.animate.set_value(0.84),
            r_lvl.animate.set_value(0.51),
            ph_l.animate.set_value(12.0), ph_r.animate.set_value(3.8),
            FadeIn(extra_l2, shift=RIGHT * 0.35),
            run_time=max(1.2, dt_to(self, "complete lysosomal block")),
            rate_func=linear,
        )

        self.at("complete lysosomal block")
        cond = T("formation unchanged", 24, TEXT).move_to([0.0, -2.55, 0])
        extra_l3 = build_autophagosome(l_grp[0].get_center() + np.array([-0.24, -0.24, 0]), radius=0.16, lc3=True, cargo_radius=0.07)
        self.play(
            t_prog.animate.set_value(1.0),
            l_lvl.animate.set_value(0.90),
            r_lvl.animate.set_value(0.52),
            FadeIn(cond, shift=UP * 0.1),
            FadeIn(extra_l3, shift=RIGHT * 0.25),
            ph_l.animate.set_value(20.0), ph_r.animate.set_value(6.5),
            run_time=max(0.8, dt_to(self, "estimates lysosomal turnover")),
            rate_func=linear,
        )

        self.at("estimates lysosomal turnover")
        inc_t = ValueTracker(0.01)
        inc_l_h = (gh - 0.1) * (0.90 - 0.45)
        inc_r_h = (gh - 0.1) * (0.52 - 0.45)
        inc_l = always_redraw(lambda: Rectangle(
            width=gw - 0.1,
            height=max(0.02, inc_l_h * inc_t.get_value()),
            stroke_color=YELLOW,
            stroke_width=3.0,
            fill_color=YELLOW,
            fill_opacity=0.88,
        ).move_to([l_gc[0], base_y + max(0.02, inc_l_h * inc_t.get_value()) / 2, 0]))
        inc_r = always_redraw(lambda: Rectangle(
            width=gw - 0.1,
            height=max(0.02, inc_r_h * inc_t.get_value()),
            stroke_color=YELLOW,
            stroke_width=3.0,
            fill_color=YELLOW,
            fill_opacity=0.88,
        ).move_to([r_gc[0], base_y + max(0.02, inc_r_h * inc_t.get_value()) / 2, 0]))
        inc_lbl = T("extra\naccumulation", 22, YELLOW, line_spacing=0.85).move_to([l_c[0] + 1.52, 1.72, 0])
        self.add(inc_l, inc_r)
        self.play(
            inc_t.animate.set_value(1.0),
            FadeIn(inc_lbl),
            ph_l.animate.set_value(26.0), ph_r.animate.set_value(8.5),
            run_time=max(0.8, dt_to(self, "equal starting amounts")),
            rate_func=linear,
        )

        self.at("equal starting amounts")
        eq_lbl = T("equal\nstart", 24, TEXT, line_spacing=0.85).move_to([r_c[0] + 1.25, base_y, 0])
        self.play(
            FadeIn(eq_lbl),
            ph_l.animate.set_value(30.0), ph_r.animate.set_value(9.8),
            run_time=2.5,
            rate_func=linear,
        )
        self.finish()


# ------------------------------------------------------------------ s10_return
class S10Return(SpokenScene):
    def construct(self):
        world = build_predict_panels(left_lvl=0.45, right_lvl=0.45, blocked=True, lc3_marked=True, show_baseline=True)
        tp, l_grp, r_grp = world[0], world[1], world[2]
        l_gc, r_gc = l_grp[5].get_center(), r_grp[5].get_center()
        gw, gh = 0.56, 2.35
        l_lvl = ValueTracker(0.45)
        r_lvl = ValueTracker(0.45)
        l_grp[6].set_opacity(0)
        r_grp[6].set_opacity(0)

        l_fill = always_redraw(lambda: Rectangle(
            width=gw - 0.1,
            height=max(0.06, (gh - 0.1) * l_lvl.get_value()),
            stroke_width=0,
            fill_color=PURPLE,
            fill_opacity=0.88,
        ).move_to([l_gc[0], l_gc[1] - (gh - 0.1) / 2 + max(0.06, (gh - 0.1) * l_lvl.get_value()) / 2, 0]))
        r_fill = always_redraw(lambda: Rectangle(
            width=gw - 0.1,
            height=max(0.06, (gh - 0.1) * r_lvl.get_value()),
            stroke_width=0,
            fill_color=PURPLE,
            fill_opacity=0.88,
        ).move_to([r_gc[0], r_gc[1] - (gh - 0.1) / 2 + max(0.06, (gh - 0.1) * r_lvl.get_value()) / 2, 0]))

        ph = ValueTracker(0.0)
        l_s, l_e = l_grp[2].get_start(), l_grp[2].get_end()
        r_s, r_e = r_grp[2].get_start(), r_grp[2].get_end()
        d_l = always_redraw(lambda: VGroup(*[
            build_autophagosome(l_s + (0.12 + 0.76 * ((ph.get_value() + k / 2.0) % 1.0)) * (l_e - l_s), radius=0.125, lc3=True, cargo_radius=0.06)
            for k in range(2)
        ]))
        d_r = always_redraw(lambda: build_autophagosome(r_s + (0.12 + 0.76 * ((0.35 * ph.get_value()) % 1.0)) * (r_e - r_s), radius=0.125, lc3=True, cargo_radius=0.06))

        self.play(FadeIn(world), FadeIn(l_fill), FadeIn(r_fill), FadeIn(d_l), FadeIn(d_r), run_time=0.8)
        self.play(
            ph.animate.set_value(4.0),
            run_time=max(0.5, dt_to(self, "their visible amounts")),
            rate_func=linear,
        )

        self.at("their visible amounts")
        self.play(
            l_grp[3].animate.scale(1.06), r_grp[3].animate.scale(1.06),
            ph.animate.set_value(6.0),
            run_time=1.4,
        )
        self.play(
            l_grp[3].animate.scale(1 / 1.06), r_grp[3].animate.scale(1 / 1.06),
            ph.animate.set_value(9.5),
            run_time=max(0.6, dt_to(self, "closing the exit")),
        )

        self.at("closing the exit")
        self.play(
            l_lvl.animate.set_value(0.92),
            r_lvl.animate.set_value(0.51),
            ph.animate.set_value(16.0),
            run_time=max(1.0, dt_to(self, "across the recycling map")),
            rate_func=linear,
        )

        self.at("across the recycling map")
        cell = build_cell_outline(center=(-0.15, 0.15, 0), width=10.6, height=5.3)
        er = build_er_patch(center=(-3.45, 0.15, 0), scale=0.95)
        prot = build_proteasome(center=(3.15, 1.75, 0), scale=1.05)
        prot_lbl = T("proteasome", 26, GOLD).next_to(prot, DOWN, buff=0.16)
        lyso = build_lysosome(center=(3.05, -0.75, 0), radius=0.90)
        lyso_lbl = T("lysosome", 26, ORANGE).next_to(lyso, DOWN, buff=0.14)
        arr_gate = Arrow([-5.25, 0.15, 0], [-4.55, 0.15, 0], color=BLUE, stroke_width=6, buff=0)
        clr_gate = Arrow([4.05, -0.75, 0], [4.95, -0.75, 0], color=ORANGE, stroke_width=6, buff=0)
        tag = scope_tag("schematic")

        flow_t = ValueTracker(0.0)
        er_p0, er_p1 = np.array([-2.3, 1.75, 0.0]), np.array([2.25, 1.75, 0.0])
        au_p0, au_p1 = np.array([-1.8, -0.75, 0.0]), np.array([2.0, -0.75, 0.0])

        def er_stream_fn():
            g = VGroup()
            for k in range(2):
                p = er_p0 + ((flow_t.get_value() + k * 0.5) % 1.0) * (er_p1 - er_p0)
                s = build_squiggle(center=p, width=0.95, amp=0.22, color=GREY)
                u = Circle(radius=0.13, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.92).next_to(s, UP, buff=0.04)
                g.add(VGroup(s, u))
            return g

        er_stream = always_redraw(er_stream_fn)
        au_stream = always_redraw(lambda: VGroup(*[
            build_autophagosome(au_p0 + ((flow_t.get_value() + k / 3.0) % 1.0) * (au_p1 - au_p0), radius=0.40, lc3=True, cargo_radius=0.19)
            for k in range(3)
        ]))

        single_map = VGroup(cell, er, prot, prot_lbl, lyso, lyso_lbl, arr_gate, clr_gate, tag)
        l_fill.clear_updaters()
        r_fill.clear_updaters()
        d_l.clear_updaters()
        d_r.clear_updaters()
        self.play(FadeOut(VGroup(world, l_fill, r_fill, d_l, d_r)), FadeIn(single_map), FadeIn(er_stream), FadeIn(au_stream), run_time=0.9)

        self.play(
            flow_t.animate.set_value(3.0),
            run_time=max(1.2, dt_to(self, "how fast does it arrive")),
            rate_func=linear,
        )

        self.at("how fast does it arrive")
        q1_box = SurroundingRectangle(arr_gate, color=YELLOW, buff=0.12, stroke_width=3.5)
        q1_lbl = T("How fast does it arrive?", 28, YELLOW).move_to([-2.5, -3.05, 0])
        self.play(FadeIn(q1_box), FadeIn(q1_lbl), flow_t.animate.set_value(3.25), run_time=0.45, rate_func=linear)
        self.play(
            flow_t.animate.set_value(3.9),
            run_time=max(0.5, dt_to(self, "how fast does it leave")),
            rate_func=linear,
        )

        self.at("how fast does it leave")
        q2_box = SurroundingRectangle(clr_gate, color=YELLOW, buff=0.12, stroke_width=3.5)
        q2_lbl = T("How fast does it leave?", 28, YELLOW).move_to([2.3, -3.05, 0])
        self.play(FadeOut(q1_box), FadeIn(q2_box), FadeIn(q2_lbl), flow_t.animate.set_value(4.5), run_time=1.3, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s11_end
class S11End(EndCard):
    LINE = "Follow the flow, not the pile."
