"""Reading a PCR as It Grows — chapter 2.

COLOR MAP (kept exactly from chapter 1)
  GREY   = original DNA/RNA, outlines, axes, unresolved comparison
  YELLOW = primers and their candidate boundaries
  BLUE   = newly copied DNA, cDNA, fluorescence curves
  GREEN  = supported interpretation, threshold, passing controls
  RED    = unresolved question, failed result, schematic late behaviour
"""
import os
import random
import numpy as np
from bp_parts import *  # noqa: F401,F403


BAR_H = 0.16
N_HI, N_LO = 2.0 ** -10, 2.0 ** -13
THRESHOLD = 0.50
CT_HI, CT_LO = 9.0, 12.0


class PCRScene(SpokenScene):
    """Shared dark stage and slow background drift for this chapter's single visual world."""

    def setup(self):
        super().setup()
        stage = RoundedRectangle(corner_radius=0.28, width=13.25, height=7.15,
                                 stroke_width=0, fill_color="#162331", fill_opacity=1)
        stage.set_z_index(-20)
        self.add(stage)
        bands = VGroup(*[
            Rectangle(width=13.05, height=0.90, stroke_width=0,
                      fill_color="#344B60", fill_opacity=0.72).move_to([0, y, 0])
            for y in (-3.10, 3.10)
        ])
        bands.set_z_index(-19)
        self.add(bands)
        beam = Rectangle(width=0.42, height=7.05, stroke_width=0,
                         fill_color=BLUE, fill_opacity=0.14).move_to([-6.7, 0, 0])
        beam.set_z_index(-18)

        def scan(mob, dt):
            mob.shift(RIGHT * 0.75 * dt)
            if mob.get_x() > 6.7:
                mob.shift(LEFT * 13.4)
        beam.add_updater(scan)
        self.add(beam)
        rng = random.Random(os.environ.get("KX_SCENE_ID", "pcr"))
        motes = VGroup()
        for _ in range(34):
            dot = Dot(radius=rng.uniform(0.025, 0.055), color=rng.choice([BLUE, GREY, TEXT]))
            dot.set_opacity(rng.uniform(0.10, 0.22))
            dot.move_to([rng.uniform(-6.4, 6.4), rng.uniform(-3.35, 3.35), 0])
            dot.speed = rng.uniform(0.05, 0.13)

            def drift(mob, dt):
                mob.shift(RIGHT * mob.speed * dt)
                if mob.get_x() > 6.55:
                    mob.shift(LEFT * 13.1)
            dot.add_updater(drift)
            motes.add(dot)
        motes.set_z_index(-10)
        self.add(motes)


def dna_bar(x0, x1, y, color=GREY, height=BAR_H, opacity=1.0):
    """A schematic strand segment, never an atom-by-atom molecular drawing."""
    return Rectangle(width=x1 - x0, height=height, stroke_width=0,
                     fill_color=color, fill_opacity=opacity).move_to([(x0 + x1) / 2, y, 0])


def primer_arrow(x, y, direction):
    body = dna_bar(x, x + 1.35 * direction, y, YELLOW, 0.24)
    tip = Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.16)
    tip.rotate(-PI / 2 if direction > 0 else PI / 2)
    tip.move_to([x + 1.35 * direction, y, 0])
    return VGroup(body, tip)


def tube(center, glow=1.0, width=2.35, height=4.6):
    """Large PCR tube with a fluorescence fill and a softly pulsing endpoint."""
    x, y, _ = center
    body = RoundedRectangle(corner_radius=0.28, width=width, height=height,
                            stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(center)
    liquid = RoundedRectangle(corner_radius=0.22, width=width - 0.3, height=height * 0.62,
                              stroke_width=0, fill_color=BLUE, fill_opacity=0.18 + 0.32 * glow)
    liquid.align_to(body, DOWN).shift(UP * 0.15)
    rim = Line([x - width * 0.58, y + height / 2, 0], [x + width * 0.58, y + height / 2, 0],
               color=GREY, stroke_width=6)
    return VGroup(body, liquid, rim)


def boundary_world():
    """The carried template picture used by the boundary and cycle scenes."""
    top = dna_bar(-5.7, 5.7, 1.05, GREY, 0.28)
    bottom = dna_bar(-5.7, 5.7, -1.05, GREY, 0.28)
    p_bottom = primer_arrow(-3.7, -0.70, +1)
    p_top = primer_arrow(3.7, 0.70, -1)
    ends = VGroup(T("3'", 30, YELLOW, weight=BOLD).move_to([-2.05, -1.55, 0]),
                  T("3'", 30, YELLOW, weight=BOLD).move_to([2.05, 1.55, 0]))
    return VGroup(top, bottom), VGroup(p_bottom, p_top), ends


def early(c, n0):
    """The stated ideal early model: N = N0 * 2^cycle."""
    return n0 * 2.0 ** c


def late(c, ct):
    """A computed logistic used only for the explicitly schematic late bend."""
    return 0.96 / (1.0 + np.exp(-0.58 * (c - (ct + 1.8))))


def growth_plot(compact=False):
    """One graph builder used everywhere the PCR history is carried forward."""
    box = (-0.20, 6.25, -1.55, 2.15) if compact else (-5.75, 5.50, -2.20, 2.55)
    p = Plot(box=box, xr=(0, 24), yr=(0, 1.05), xticks=[0, 6, 12, 18, 24],
             yticks=[(0, "0"), (0.5, "0.5"), (1.0, "1.0")],
             xlabel="cycle", ylabel="fluorescence", size=22, label_size=26)
    return p


def graph_curves(p, include_late=True):
    hi = p.curve(lambda c: early(c, N_HI), 0, CT_HI + 0.25, color=BLUE, width=7)
    lo = p.curve(lambda c: early(c, N_LO), 0, CT_LO + 0.25, color=BLUE, width=4)
    group = VGroup(hi, lo)
    if include_late:
        hi_l = DashedVMobject(p.curve(lambda c: late(c, CT_HI), CT_HI, 24, color=RED, width=5),
                             num_dashes=24)
        lo_l = DashedVMobject(p.curve(lambda c: late(c, CT_LO), CT_LO, 24, color=RED, width=5),
                             num_dashes=20)
        group.add(hi_l, lo_l)
    return group


def threshold_world(compact=False, endpoints=True):
    p = growth_plot(compact)
    curves = graph_curves(p)
    threshold = p.hline(THRESHOLD, color=GREEN, dashed=False)
    guides = VGroup(DashedLine(p.pt(CT_HI, 0), p.pt(CT_HI, THRESHOLD), color=GREY, stroke_width=3),
                    DashedLine(p.pt(CT_LO, 0), p.pt(CT_LO, THRESHOLD), color=GREY, stroke_width=3))
    dots = VGroup()
    if endpoints:
        dots = VGroup(Dot(p.pt(24, late(24, CT_HI)), radius=0.13, color=BLUE),
                      Dot(p.pt(24, late(24, CT_LO)), radius=0.13, color=BLUE))
    return p, curves, threshold, guides, dots


def control_tube(label, positive=False, compact=False):
    width = 2.05 if compact else 2.65
    height = 1.45 if compact else 1.65
    size = 22 if compact else 26
    frame = RoundedRectangle(corner_radius=0.16, width=width, height=height,
                             stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.8)
    label_shift = (0.28 if compact else 0.35) if positive else (0.25 if compact else 0.31)
    lab = fit_text(label, max_w=width - 0.48, size=size, color=TEXT, max_lines=2,
                   min_size=22 if compact else 24).move_to(frame.get_center() + DOWN * label_shift)
    trace = Line(frame.get_left() + RIGHT * 0.22 + UP * 0.22,
                 frame.get_right() + LEFT * 0.22 + UP * 0.22, color=GREY, stroke_width=4)
    if positive:
        trace = VMobject(stroke_color=BLUE, stroke_width=5)
        a = frame.get_left()[0] + 0.22
        b = frame.get_right()[0] - 0.22
        y = frame.get_center()[1] + (0.3 if compact else 0.13)
        pts = [[x, y + 0.24 / (1 + np.exp(-8 * ((x - a) / (b - a) - 0.55))), 0]
               for x in np.linspace(a, b, 40)]
        trace.set_points_as_corners(pts)
    return VGroup(frame, trace, lab)


class S00Hook(PCRScene, TitleCard):
    LESSON = "Recombinant DNA, cloning and PCR"
    TITLE = "Reading a PCR as It Grows"

    def construct(self):
        left, right = tube([-3.1, 0, 0]), tube([3.1, 0, 0])
        self.play(FadeIn(left), run_time=0.8)
        self.at("Now two PCR tubes")
        self.play(FadeIn(right), run_time=0.8)
        self.at("equally bright")
        self.play(Indicate(left[1], color=BLUE), Indicate(right[1], color=BLUE), run_time=1.0)
        self.at("Did they start")
        def qmark(size, at):
            label = T("?", size, RED, weight=BOLD)
            plate = RoundedRectangle(corner_radius=0.16, width=label.width + 0.42,
                                     height=label.height + 0.30, stroke_color=RED, stroke_width=3,
                                     fill_color=BG, fill_opacity=1).move_to(at)
            return VGroup(plate, label.move_to(plate))
        qs = VGroup(qmark(64, [-0.45, 0.55, 0]), qmark(48, [0.50, -0.60, 0]))
        self.play(FadeIn(qs, scale=0.7), run_time=0.7)
        self.at("answer hides")
        ax1 = Axes(x_range=[0, 1], y_range=[0, 1], x_length=1.55, y_length=2.15,
                   axis_config={"include_ticks": False, "color": GREY, "stroke_width": 2}).move_to([-3.1, 0.15, 0])
        ax2 = ax1.copy().move_to([3.1, 0.15, 0])
        c1 = ax1.plot(lambda x: 0.96 / (1 + np.exp(-10 * (x - 0.35))), color=BLUE, stroke_width=5)
        c2 = ax2.plot(lambda x: 0.96 / (1 + np.exp(-10 * (x - 0.62))), color=BLUE, stroke_width=5)
        self.play(left[1].animate.set_opacity(0.12), right[1].animate.set_opacity(0.12),
                  FadeIn(ax1), FadeIn(ax2), Create(c1), Create(c2), run_time=1.6)
        self.at("Watch a bounded target")
        target = VGroup(dna_bar(-0.85, 0.85, 2.85, BLUE, 0.24),
                        Line([-0.85, 2.55, 0], [-0.85, 3.15, 0], color=YELLOW, stroke_width=4),
                        Line([0.85, 2.55, 0], [0.85, 3.15, 0], color=YELLOW, stroke_width=4))
        self.play(FadeOut(qs), FadeIn(target), run_time=0.7)
        self.at("become a curve")
        self.play(Transform(target, c1.copy().scale(0.8).move_to([0, 2.75, 0])), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Recombinant DNA, cloning and PCR"
    TITLE = "Reading a PCR as It Grows"


class S02Boundaries(PCRScene):
    def construct(self):
        strands, primers, ends = boundary_world()
        self.play(FadeIn(strands), run_time=0.8)
        self.at("primers")
        ingredients = VGroup(chip("template DNA", GREY), chip("primers", YELLOW),
                             chip("nucleotides", BLUE), chip("polymerase", GREY)).arrange(RIGHT, buff=0.25)
        ingredients.scale(0.88).move_to([0, 3.05, 0])
        self.play(FadeIn(ingredients, shift=DOWN * 0.15), run_time=1.0)
        self.at("A yellow primer")
        self.play(FadeIn(primers, shift=UP * 0.25), run_time=0.9)
        self.at("Their three prime ends")
        self.play(FadeIn(ends), Indicate(primers, color=YELLOW), run_time=0.9)
        window = Rectangle(width=4.1, height=2.65, stroke_color=YELLOW, stroke_width=0,
                           fill_color=YELLOW, fill_opacity=0.08).move_to(ORIGIN)
        self.at("point into the target")
        self.play(FadeIn(window), run_time=0.7)
        polymerases = VGroup(boxed_label("polymerase", GREY, size=24), boxed_label("polymerase", GREY, size=24))
        for polymerase in polymerases:
            polymerase.box.set_fill(BG, opacity=1)
        polymerases[0].move_to([-1.7, -0.2, 0]); polymerases[1].move_to([1.7, 0.2, 0])
        self.at("Polymerase extends")
        blue1 = dna_bar(-2.0, 1.7, -0.70, BLUE, 0.24)
        blue2 = dna_bar(-1.7, 2.0, 0.70, BLUE, 0.24)
        self.play(FadeIn(polymerases), GrowFromEdge(blue1, LEFT), GrowFromEdge(blue2, RIGHT), run_time=1.5)
        self.at("Primer placement sets")
        self.play(FadeOut(polymerases), Indicate(window, color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.finish()


class S03Cycle(PCRScene):
    def construct(self):
        steps = VGroup(*[boxed_label(s, c, size=28) for s, c in
                         [("denature", RED), ("anneal", YELLOW), ("extend", BLUE)]])
        for step in steps:
            step.box.set_fill(BG, opacity=1)
        steps.arrange(RIGHT, buff=0.65).move_to([0, 3.05, 0])
        track = Arc(radius=2.55, start_angle=0.15, angle=TAU - 0.3, color=GREY, stroke_width=3)
        track.stretch(1.8, 0).move_to([0, -0.15, 0])
        strands, primers, _ = boundary_world()
        strands.scale(0.72).move_to([0, 0.05, 0])
        self.play(Create(track), FadeIn(steps), FadeIn(strands), run_time=1.0)
        self.at("Heating separates")
        self.play(strands[0].animate.shift(UP * 0.65), strands[1].animate.shift(DOWN * 0.65),
                  Indicate(steps[0], color=RED), run_time=1.2)
        self.at("Cooling lets")
        primers.scale(0.72).move_to([0, 0.05, 0])
        self.play(FadeIn(primers), Indicate(steps[1], color=YELLOW), run_time=1.0)
        self.at("Polymerase extends")
        new_top = dna_bar(-2.55, 1.55, 0.30, BLUE, 0.18)
        new_bottom = dna_bar(-1.55, 2.55, -0.30, BLUE, 0.18)
        self.play(GrowFromEdge(new_top, RIGHT), GrowFromEdge(new_bottom, LEFT),
                  Indicate(steps[2], color=BLUE), run_time=1.6)
        self.at("Repeat the cycle")
        duplex = VGroup(strands.copy().scale(0.52), new_top.copy(), new_bottom.copy()).scale(0.54)
        rows = VGroup(*[duplex.copy() for _ in range(4)]).arrange(DOWN, buff=0.28).move_to([0, -0.15, 0])
        self.play(FadeOut(strands), FadeOut(primers), FadeOut(new_top), FadeOut(new_bottom),
                  FadeIn(rows[0]), run_time=0.8)
        self.at("earlier products become templates")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * (0.12 * i)) for i, r in enumerate(rows[1:], 1)],
                              lag_ratio=0.22), run_time=1.6)
        self.at("photocopier")
        group = boxed_label("copies can be copied", BLUE, size=30).move_to([0, -3.25, 0])
        self.play(FadeIn(group), rows.animate.scale(1.07), run_time=0.9)
        self.at("growing family")
        count = counter("grouped copies  x {:.0f}", ValueTracker(8), [-4.35, 2.36, 0], size=28, color=BLUE)
        self.play(FadeIn(count), run_time=0.6)
        self.finish()


class S04Growth(PCRScene):
    def construct(self):
        p = growth_plot()
        n = ValueTracker(0.4)
        live = p.live_curve(lambda c: early(c, N_HI), n, color=BLUE, width=7)
        dot = p.dot(lambda: n.get_value(), lambda: early(n.get_value(), N_HI), color=BLUE)
        self.play(Create(p), run_time=1.0)
        self.add(live, dot)
        self.at("each completed target")
        self.play(n.animate.set_value(4.5), run_time=1.6, rate_func=linear)
        self.at("double every cycle")
        self.play(n.animate.set_value(8.0), run_time=2.0, rate_func=linear)
        eq = M("N = N₀ × 2ⁿ", 36, TEXT).move_to([2.75, 3.12, 0])
        self.at("curve is computed")
        self.play(FadeIn(eq), n.animate.set_value(CT_HI + 0.2), run_time=1.3)
        tag = boxed_label("ideal early model", BLUE, size=28).move_to([-1.55, 3.15, 0])
        self.at("Real reactions")
        self.play(FadeIn(tag), run_time=0.7)
        self.finish()


class S05Plateau(PCRScene):
    def construct(self):
        p = growth_plot()
        hi = p.curve(lambda c: early(c, N_HI), 0, CT_HI + 0.25, color=BLUE, width=7)
        self.add(p, hi)
        self.at("amplification slows")
        late_hi = DashedVMobject(p.curve(lambda c: late(c, CT_HI), CT_HI, 24, color=RED, width=5), num_dashes=24)
        self.play(Create(late_hi), run_time=1.6)
        self.at("Different starting amounts")
        lo = p.curve(lambda c: early(c, N_LO), 0, CT_LO + 0.25, color=BLUE, width=4)
        late_lo = DashedVMobject(p.curve(lambda c: late(c, CT_LO), CT_LO, 24, color=RED, width=5), num_dashes=20)
        self.play(Create(lo), Create(late_lo), run_time=1.8)
        schematic = scope_tag("dashed late curves: schematic")
        dots = VGroup(Dot(p.pt(24, late(24, CT_HI)), radius=0.13, color=BLUE),
                      Dot(p.pt(24, late(24, CT_LO)), radius=0.13, color=BLUE))
        self.at("finish at similar levels")
        self.play(FadeIn(dots), FadeIn(schematic), run_time=0.9)
        self.at("Endpoint brightness")
        self.play(Indicate(dots, color=BLUE), run_time=1.0)
        self.at("Real time PCR")
        cursor = ValueTracker(0)
        scan = always_redraw(lambda: Line(p.pt(cursor.get_value(), 0), p.pt(cursor.get_value(), 1.02),
                                          color=GREEN, stroke_width=3))
        self.add(scan)
        self.play(cursor.animate.set_value(24), run_time=2.5, rate_func=linear)
        self.at("early curves remain separated")
        self.play(Indicate(VGroup(hi, lo), color=BLUE, scale_factor=1.0), run_time=1.0)
        self.finish()


class S06Predict(PCRScene):
    def construct(self):
        p = growth_plot()
        curves = graph_curves(p)
        self.add(p, curves)
        threshold = p.hline(THRESHOLD, color=GREEN, dashed=False)
        self.at("green threshold")
        self.play(Create(threshold), run_time=1.1)
        guides = VGroup(DashedLine(p.pt(CT_HI, 0), p.pt(CT_HI, THRESHOLD), color=GREY, stroke_width=3),
                        DashedLine(p.pt(CT_LO, 0), p.pt(CT_LO, THRESHOLD), color=GREY, stroke_width=3))
        dots = VGroup(Dot(p.pt(24, late(24, CT_HI)), radius=0.13, color=BLUE),
                      Dot(p.pt(24, late(24, CT_LO)), radius=0.13, color=BLUE))
        self.at("One curve reaches")
        self.play(Create(guides), FadeIn(dots), run_time=1.1)
        q = question_card("Which reaction began with more target?", y=-3.25, size=30)
        self.at("Which reaction")
        self.play(FadeIn(q), run_time=0.8)
        self.at("Think about")
        self.play(Indicate(guides, color=GREY, scale_factor=1.0), run_time=1.1)
        sweep = Dot(p.pt(0, THRESHOLD), radius=0.13, color=GOLD)
        self.add(sweep)
        flip = False
        while self.narration_s - self.elapsed() > 2.4:
            self.play(sweep.animate.move_to(p.pt(0 if flip else 24, THRESHOLD)), run_time=2.0, rate_func=smooth)
            flip = not flip
        self.remove(sweep)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        stage = RoundedRectangle(corner_radius=0.28, width=13.25, height=7.15,
                                 stroke_width=0, fill_color="#162331", fill_opacity=1)
        stage.set_z_index(-20)
        bands = VGroup(*[
            Rectangle(width=13.05, height=0.90, stroke_width=0,
                      fill_color="#344B60", fill_opacity=0.72).move_to([0, y, 0])
            for y in (-3.10, 3.10)
        ])
        bands.set_z_index(-19)
        self.add(stage, bands)
        p, curves, threshold, guides, dots = threshold_world()
        q = question_card("Which reaction began with more target?", y=-3.25, size=30)
        self.add(p, curves, threshold, guides, dots, q)
        cursor = Dot(p.pt(0, THRESHOLD), radius=0.13, color=GOLD)
        self.add(cursor)
        self.play(cursor.animate.move_to(p.pt(24, THRESHOLD)), run_time=2.0, rate_func=smooth)
        self.play(cursor.animate.move_to(p.pt(0, THRESHOLD)), run_time=2.0, rate_func=smooth)
        self.finish()


class S08Threshold(PCRScene):
    def construct(self):
        p, curves, threshold, guides, dots = threshold_world()
        self.add(p, curves, threshold, guides, dots)
        early_guide = guides[0]
        self.at("earlier crossing")
        self.play(early_guide.animate.set_color(GREEN).set_stroke(width=6), run_time=0.8)
        starts = VGroup(Dot(p.pt(0, early(0, N_HI)), radius=0.16, color=BLUE),
                        Dot(p.pt(0, early(0, N_LO)), radius=0.10, color=BLUE))
        self.at("more starting target")
        arrow = Arrow(p.pt(CT_HI, THRESHOLD), starts[0].get_center(), color=GREEN, stroke_width=5, buff=0.12)
        self.play(FadeIn(starts), GrowArrow(arrow), run_time=1.2)
        self.at("fewer rounds")
        self.play(Indicate(early_guide, color=GREEN), run_time=0.9)
        self.at("threshold cycle")
        ct1 = T("Ct", 30, GREEN).move_to(p.pt(CT_HI, 0) + RIGHT * 0.72 + UP * 0.32)
        ct2 = T("Ct", 30, GREY).move_to(p.pt(CT_LO, 0) + RIGHT * 0.72 + UP * 0.32)
        self.play(FadeIn(ct1), FadeIn(ct2), run_time=0.7)
        assumption = boxed_label("matched, near-perfect efficiency", GREEN, size=28).move_to([2.15, 2.95, 0])
        self.at("With matched")
        self.play(FadeIn(assumption), run_time=0.8)
        self.at("earlier threshold cycle")
        self.play(Indicate(VGroup(early_guide, ct1), color=GREEN), run_time=1.0)
        self.at("plateau cannot")
        self.play(dots.animate.set_color(GREY).set_opacity(0.35), FadeOut(arrow), run_time=0.9)
        self.finish()


class S09Names(PCRScene):
    def construct(self):
        p = growth_plot(compact=True)
        curves = graph_curves(p)
        self.play(FadeIn(p), Create(curves), run_time=1.1)
        self.at("Reverse transcription")
        rna = Arc(radius=0.75, start_angle=-0.7, angle=4.9, color=GREY, stroke_width=8).move_to([-4.8, 1.25, 0])
        self.play(Create(rna), run_time=0.8)
        rt = boxed_label("reverse\ntranscriptase", GREY, size=26, box=(2.35, 1.05)).move_to([-2.45, 1.25, 0])
        self.at("Reverse transcriptase")
        self.play(FadeIn(rt), run_time=0.7)
        cdna = dna_bar(-5.7, -3.8, -0.45, BLUE, 0.28)
        self.at("copies RNA")
        self.play(TransformFromCopy(rna, cdna), run_time=1.1)
        pcr = boxed_label("PCR", YELLOW, size=30).move_to([-2.45, -0.45, 0])
        self.at("which PCR")
        self.play(FadeIn(pcr), cdna.animate.next_to(pcr, LEFT, buff=0.25), run_time=0.9)
        route = fit_text("RNA  →  cDNA  →  amplified DNA", max_w=5.4, size=28, color=BLUE).move_to([-3.7, -2.72, 0])
        self.at("Combining the steps")
        self.play(FadeIn(route), Indicate(curves[0], color=BLUE, scale_factor=1.0), run_time=1.1)
        self.at("fluorescence still reports")
        note = boxed_label("signal: amplified DNA", BLUE, size=26).move_to([3.65, 3.12, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.at("not RNA directly")
        self.play(rna.animate.set_opacity(0.35), Indicate(note, color=BLUE), run_time=0.9)
        self.finish()


class S10Controls(PCRScene):
    def construct(self):
        p = growth_plot(compact=True)
        curves = graph_curves(p)
        self.add(p, curves)
        heading = T("controlled comparison", 32, GREEN).move_to([-3.65, 2.85, 0])
        self.at("controlled comparison")
        self.play(FadeIn(heading), run_time=0.7)
        blank = control_tube("no template").move_to([-4.1, 1.25, 0])
        self.at("no template")
        self.play(FadeIn(blank), blank[0].animate.set_stroke(GREEN, width=4), run_time=1.0)
        no_rt = control_tube("no RT").move_to([-4.1, -0.45, 0])
        self.at("without reverse transcriptase")
        self.play(FadeIn(no_rt), no_rt[0].animate.set_stroke(GREEN, width=4), run_time=1.0)
        pos = control_tube("known positive", positive=True).move_to([-4.1, -2.15, 0])
        self.at("known positive")
        self.play(FadeIn(pos), pos[0].animate.set_stroke(GREEN, width=4), run_time=1.1)
        self.at("Controls turn")
        self.play(Indicate(VGroup(blank, no_rt, pos), color=GREEN, scale_factor=1.01), run_time=1.2)
        self.finish()


class S11Close(PCRScene):
    def construct(self):
        p, curves, threshold, guides, dots = threshold_world()
        controls = VGroup(control_tube("no template", compact=True),
                          control_tube("known positive", positive=True, compact=True))
        controls[0].move_to([2.9, -1.0, 0])
        controls[1].move_to([5.1, -1.0, 0])
        self.add(p, curves, threshold, guides, dots, controls)
        self.at("early rising curve")
        self.play(Indicate(VGroup(curves[0], curves[1]), color=GREEN, scale_factor=1.0), run_time=1.2)
        self.at("end point")
        self.play(dots.animate.set_color(GREY).set_opacity(0.3),
                  curves[2:].animate.set_color(GREY).set_opacity(0.35), run_time=1.0)
        self.at("Read the crossing")
        guides[0].set_color(GREEN)
        arrows = VGroup(Arrow(p.pt(0, early(0, N_HI)), p.pt(CT_HI, THRESHOLD), buff=0.08,
                              color=GREEN, stroke_width=4),
                        Arrow(p.pt(0, early(0, N_LO)), p.pt(CT_LO, THRESHOLD), buff=0.08,
                              color=GREEN, stroke_width=4))
        self.play(Create(arrows), run_time=1.1)
        self.at("challenge the signal")
        self.play(Indicate(controls, color=GREEN, scale_factor=1.02), run_time=1.0)
        rule = caption("Useful measurement: when the curve arrives", color=GREEN, y=-3.36)
        self.at("useful measurement")
        self.play(FadeIn(rule), run_time=0.8)
        self.at("not how bright")
        self.play(Indicate(arrows, color=GREEN, scale_factor=1.0), run_time=0.9)
        self.finish()


class S12End(EndCard):
    LINE = "Copy timing estimates input; endpoint abundance does not."
