"""Follow the Flow, Not the Pile — quality control and autophagy.

COLOR MAP (one meaning throughout the film)
  BLUE   autophagosomes and carrier arrival
  ORANGE lysosomes and lysosomal clearance
  GOLD   proteasomes
  PURPLE LC3-II marks and LC3-II gauges
  RED    ubiquitin tags, blocks, and failed routes
  TEAL   ER folding helpers
  GREY   cell material, compartments, and structure
  YELLOW measured extra accumulation / the revealed difference

All diagrams are schematic.  Proteins are cartoons, tags, or blocks; no molecular
structures are drawn.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, size=30, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


def cell_outline(width=12.0, height=6.3, center=ORIGIN, opacity=0.18):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.7,
        stroke_color=GREY, stroke_width=4, fill_color=GREY,
        fill_opacity=opacity,
    ).move_to(center)


def carrier(center=ORIGIN, radius=0.43, lc3=False):
    """Double-membrane autophagosome cartoon."""
    outer = Circle(radius=radius, color=BLUE, stroke_width=5,
                   fill_color=BLUE, fill_opacity=0.07).move_to(center)
    inner = Circle(radius=radius * 0.72, color=BLUE, stroke_width=3).move_to(center)
    g = VGroup(outer, inner)
    if lc3:
        for angle in (0.35, 2.5, 4.4):
            g.add(Dot(np.array(center) + radius * np.array([math.cos(angle), math.sin(angle), 0]),
                      radius=0.09, color=PURPLE))
    return g


def membrane_cup(center=ORIGIN, openness=0.72, radius=1.35):
    """Two arcs; openness shrinks as the cup closes."""
    angle = TAU * (1 - openness)
    start = -PI / 2 - angle / 2
    return VGroup(*[
        Arc(radius=r, start_angle=start, angle=angle, arc_center=center,
            color=BLUE, stroke_width=5)
        for r in (radius, radius * 0.76)
    ])


def lysosome(center=p(4.35, -0.1), radius=1.35, with_label=True):
    body = Circle(radius=radius, color=ORANGE, stroke_width=5,
                  fill_color=ORANGE, fill_opacity=0.13).move_to(center)
    shine = Arc(radius=radius * 0.72, start_angle=0.2, angle=1.1,
                color=ORANGE, stroke_width=3).move_to(center).set_opacity(0.65)
    g = VGroup(body, shine)
    if with_label:
        g.add(label("lysosome", 30, ORANGE).next_to(body, DOWN, buff=0.28))
    return g


def proteasome(center=p(4.5, 2.15), scale=1.0, with_label=True):
    """A capped barrel, deliberately a machine cartoon rather than a molecule."""
    body = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.2,
                            stroke_color=GOLD, stroke_width=4,
                            fill_color=GOLD, fill_opacity=0.12).move_to(center)
    caps = VGroup(
        Line(body.get_left() + UP * 0.38, body.get_left() + DOWN * 0.38,
             color=GOLD, stroke_width=8),
        Line(body.get_right() + UP * 0.38, body.get_right() + DOWN * 0.38,
             color=GOLD, stroke_width=8),
    )
    bore = DashedLine(body.get_left() + RIGHT * 0.12, body.get_right() + LEFT * 0.12,
                      dash_length=0.12, color=GOLD, stroke_width=2)
    g = VGroup(body, caps, bore)
    if with_label:
        g.add(label("proteasome", 28, GOLD).next_to(body, UP, buff=0.2))
    return g.scale(scale)


def mitochondrion(center=ORIGIN, width=2.5, height=1.35, with_label=False):
    body = Ellipse(width=width, height=height, color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.14).move_to(center)
    # A simple internal fold line conveys an organelle without molecular detail.
    fold = VMobject(color=GREY, stroke_width=3).set_points_smoothly([
        np.array(center) + p(-0.75, 0), np.array(center) + p(-0.35, 0.32),
        np.array(center) + p(0.05, -0.25), np.array(center) + p(0.45, 0.28),
        np.array(center) + p(0.78, 0),
    ])
    g = VGroup(body, fold)
    if with_label:
        g.add(label("damaged mitochondrion", 28, GREY).next_to(body, DOWN, buff=0.25))
    return g


def blocks(center=ORIGIN, rows=2, cols=3, color=GREY, side=0.28):
    g = VGroup(*[
        Square(side_length=side, stroke_width=0, fill_color=color, fill_opacity=0.9)
        for _ in range(rows * cols)
    ]).arrange_in_grid(rows=rows, cols=cols, buff=0.15)
    return g.move_to(center)


def schematic_tag(pos=p(5.65, -3.25)):
    return label("schematic", 28, GREY).move_to(pos)


def arrow_between(start, end, color=GREY, width=5, **kw):
    return Arrow(start, end, buff=0.08, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.14, **kw)


def pool_panel(center_x, title_text, arrival_text, lc3=True):
    """Shared prediction geometry used without drift in scenes 7–10."""
    frame = RoundedRectangle(width=5.55, height=4.3, corner_radius=0.35,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.18).move_to(p(center_x, -0.35))
    title = label(title_text, 30, TEXT, weight=BOLD).move_to(p(center_x, 2.35))
    arrival = Arrow(p(center_x - 2.45, -0.2), p(center_x - 1.55, -0.2), buff=0,
                    color=BLUE, stroke_width=8 if "fast" in arrival_text else 4,
                    max_tip_length_to_length_ratio=0.22)
    arrival_label = label(arrival_text, 28, BLUE).move_to(p(center_x - 1.6, 1.5))
    ly = Circle(radius=0.72, color=ORANGE, stroke_width=4,
                fill_color=ORANGE, fill_opacity=0.1).move_to(p(center_x + 1.78, -0.2))
    exit_arrow = Arrow(p(center_x + 0.95, -0.2), p(center_x + 1.25, -0.2), buff=0,
                       color=ORANGE, stroke_width=5)
    cs = VGroup(*[
        carrier(p(center_x + dx, y), 0.35, lc3=lc3)
        for dx, y in [(-1.1, 0.55), (0.0, 0.55), (-0.55, -0.45), (0.55, -0.45)]
    ])
    return VGroup(frame, title, arrival, arrival_label, ly, exit_arrow, cs)


def baf_block(center_x):
    bar = Rectangle(width=0.24, height=1.65, stroke_width=0,
                    fill_color=RED, fill_opacity=1).move_to(p(center_x + 1.15, -0.2)).rotate(-0.3)
    return VGroup(bar, label("bafilomycin", 28, RED).move_to(p(center_x + 1.62, -1.65)))


def gauge(center_x, level, title_text, color=PURPLE, height=3.35, center_y=-0.25):
    """A self-contained readout whose fill is tied to the supplied tracker."""
    h = height
    outline = RoundedRectangle(width=1.25, height=h, corner_radius=0.14,
                               stroke_color=GREY, stroke_width=3).move_to(p(center_x, center_y))
    def fill():
        value = max(0.02, min(1.0, level.get_value()))
        rect = Rectangle(width=1.08, height=(h - 0.14) * value, stroke_width=0,
                         fill_color=color, fill_opacity=0.82)
        rect.move_to(outline).align_to(outline, DOWN).shift(UP * 0.07)
        return rect
    fill_mob = always_redraw(fill)
    title = label(title_text, 29, TEXT, weight=BOLD).next_to(outline, UP, buff=0.28)
    return VGroup(outline, fill_mob, title)


def yeast(center, route=True):
    cell = Ellipse(width=1.25, height=1.75, color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.08).move_to(center)
    vac = Circle(radius=0.34, color=ORANGE, stroke_width=3).move_to(np.array(center) + p(0.1, 0.2))
    route_mark = CurvedArrow(np.array(center) + p(-0.48, -0.3),
                             np.array(center) + p(-0.05, 0.15), angle=-0.7,
                             color=BLUE, stroke_width=4)
    g = VGroup(cell, vac, route_mark)
    if not route:
        g.add(Cross(route_mark, stroke_color=RED, stroke_width=6))
    return g


class S01Hook(SpokenScene):
    def construct(self):
        cell = cell_outline()
        cargo = blocks(p(-3.4, -0.2), rows=2, cols=2, side=0.35)
        ly = lysosome(p(4.25, -0.1), 1.45, with_label=False)
        cup0 = membrane_cup(cargo.get_center(), openness=0.73, radius=1.2)
        cup1 = membrane_cup(cargo.get_center(), openness=0.24, radius=1.2)
        closed = carrier(cargo.get_center(), 1.2)
        self.at("Autophagy wraps")
        self.play(Create(cell), FadeIn(cargo), Create(cup0), run_time=1.1)
        self.play(Transform(cup0, cup1), run_time=1.0)
        self.play(Transform(cup0, closed), run_time=0.8)
        self.at("sends it to lysosomes")
        self.play(FadeIn(ly), VGroup(cup0, cargo).animate.move_to(p(2.0, -0.1)), run_time=0.9)
        ly_lab = label("lysosome", 30, ORANGE).next_to(ly[0], DOWN, buff=0.25)
        self.play(FadeIn(ly_lab), VGroup(cup0, cargo).animate.move_to(ly[0]), run_time=0.65)
        self.at("Those carriers are")
        auto_lab = label("autophagosome", 30, BLUE).move_to(p(0.0, 2.7))
        pointer = arrow_between(auto_lab.get_bottom(), cup0.get_top(), BLUE, 4)
        self.play(FadeIn(auto_lab), GrowArrow(pointer), run_time=0.65)
        self.at("Yet two cells")
        self.play(FadeOut(VGroup(cup0, cargo, ly, ly_lab, auto_lab, pointer)), run_time=0.35)
        self.play(cell.animate.stretch_to_fit_width(5.65).stretch_to_fit_height(4.55).move_to(p(-3.15, -0.2)),
                  run_time=0.55)
        right_cell = cell.copy().move_to(p(3.15, -0.2))
        piles_l = VGroup(*[carrier(p(-4.3 + (i % 3) * 1.05, -0.2 + (i // 3) * 1.05), 0.34)
                           for i in range(5)])
        piles_r = VGroup(*[carrier(p(2.0 + (i % 3) * 1.05, -0.2 + (i // 3) * 1.05), 0.34)
                           for i in range(5)])
        self.play(FadeIn(right_cell), LaggedStart(*[FadeIn(x) for x in VGroup(piles_l, piles_r)], lag_ratio=0.04),
                  run_time=0.9)
        self.at("Is autophagy faster")
        question = label("Same pile. Same flow?", 38, TEXT, weight=BOLD).move_to(p(0, 3.15))
        scrub_l = Line(p(-5.45, -2.05), p(-5.45, 1.6), color=TEAL, stroke_width=5)
        scrub_r = Line(p(0.85, -2.05), p(0.85, 1.6), color=TEAL, stroke_width=5)
        scan_l = Rectangle(width=0.55, height=3.7, stroke_width=0,
                           fill_color=TEAL, fill_opacity=0.32).move_to(scrub_l)
        scan_r = Rectangle(width=0.55, height=3.7, stroke_width=0,
                           fill_color=TEAL, fill_opacity=0.32).move_to(scrub_r)
        def sweep_left(m, dt):
            m.shift(RIGHT * 2.2 * dt)
            if m.get_x() > -0.75:
                m.move_to(p(-5.45, -0.22))
        def sweep_right(m, dt):
            m.shift(RIGHT * 2.2 * dt)
            if m.get_x() > 5.55:
                m.move_to(p(0.85, -0.22))
        scan_l.add_updater(sweep_left)
        scan_r.add_updater(sweep_right)
        self.play(FadeIn(question), Create(scrub_l), Create(scrub_r),
                  FadeIn(scan_l), FadeIn(scan_r), run_time=0.7)
        self.at("One makes and clears")
        fast_in = carrier(p(-5.15, 0.8), 0.32)
        fast_out = piles_l[2]
        self.play(FadeIn(fast_in, shift=RIGHT * 0.4),
                  fast_out.animate.move_to(p(-0.75, -0.2)).set_opacity(0),
                  scrub_l.animate.shift(RIGHT * 3.6), run_time=1.15)
        self.remove(fast_out)
        fast_in.move_to(p(-3.25, -0.2))
        self.at("The other makes them slowly")
        slow_in = carrier(p(1.15, 0.85), 0.32)
        block = Rectangle(width=0.28, height=1.4, stroke_width=0,
                          fill_color=RED, fill_opacity=1).move_to(p(5.15, -0.15)).rotate(-0.35)
        self.play(FadeIn(slow_in, shift=RIGHT * 0.2),
                  scrub_r.animate.shift(RIGHT * 1.6), run_time=0.85)
        self.at("exit is blocked")
        self.play(FadeIn(block), slow_in.animate.move_to(p(3.1, -0.15)), run_time=0.65)
        fast_lab = label("fast in + fast out", 28, BLUE).move_to(p(-3.15, -2.95))
        slow_lab = label("slow in + blocked out", 28, RED).move_to(p(3.15, -2.95))
        schem = schematic_tag(p(5.55, 3.2))
        self.play(FadeIn(fast_lab), FadeIn(slow_lab), FadeIn(schem), run_time=0.55)
        self.at("A still picture")
        self.play(Indicate(piles_l, color=YELLOW, scale_factor=1.04),
                  Indicate(piles_r, color=YELLOW, scale_factor=1.04), run_time=1.25)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Quality control and autophagy"
    TITLE = "Follow the Flow, Not the Pile"


class S03ErRoute(SpokenScene):
    def construct(self):
        lumen = RoundedRectangle(width=11.7, height=4.2, corner_radius=0.45,
                                 stroke_color=GREY, stroke_width=5,
                                 fill_color=GREY, fill_opacity=0.18).move_to(p(0, 0.65))
        er_lab = label("ER lumen", 34, GREY).move_to(p(-4.2, 2.15))
        cyt_lab = label("cytosol", 30, GREY).move_to(p(-4.9, -2.35))
        client = VMobject(color=GREY, stroke_width=7).set_points_smoothly([
            p(-2.7, 0.8), p(-2.1, 1.4), p(-1.6, 0.2), p(-0.9, 1.25), p(-0.25, 0.55)
        ])
        client_lab = label("client", 28, GREY).next_to(client, UP, buff=0.25)
        helpers = VGroup(chip("helper", TEAL, 28), chip("helper", TEAL, 28)).arrange(RIGHT, buff=2.4).move_to(p(-1.45, -0.8))
        self.at("endoplasmic reticulum")
        self.play(Create(lumen), FadeIn(er_lab), FadeIn(cyt_lab), run_time=0.9)
        self.play(Create(client), FadeIn(client_lab), run_time=0.65)
        self.at("uses helpers to retry")
        retry_sweep = Dot(p(-5.1, -1.27), radius=0.13, color=TEAL).set_opacity(0.8)
        def retry_flow(m, dt):
            m.shift(RIGHT * 4.0 * dt)
            if m.get_x() > 5.1:
                m.move_to(p(-5.1, -1.27))
        retry_sweep.add_updater(retry_flow)
        self.add(retry_sweep)
        self.play(FadeIn(helpers, shift=UP * 0.25), run_time=0.5)
        self.play(helpers.animate.arrange(RIGHT, buff=0.25).move_to(client), run_time=0.7)
        self.play(helpers.animate.arrange(RIGHT, buff=2.4).move_to(p(-1.45, -0.8)), run_time=0.55)
        loop = CurvedArrow(p(1.2, 1.45), p(-3.7, 1.3), radius=-2.7,
                           color=TEAL, stroke_width=4)
        self.play(VGroup(client, client_lab).animate.shift(RIGHT * 2.25), Create(loop), run_time=0.7)
        self.play(VGroup(client, client_lab).animate.shift(LEFT * 2.25), run_time=0.55)
        self.at("This is a first picture")
        first = label("first picture", 30, TEAL).move_to(p(3.7, 2.15))
        self.play(FadeIn(first), Indicate(loop, color=TEAL), run_time=0.75)
        self.at("many failed proteins")
        retry_sweep.clear_updaters()
        fail = label("persistent failure", 28, RED).move_to(client_lab)
        self.play(Transform(client_lab, fail), FadeOut(helpers), FadeOut(loop), FadeOut(first),
                  FadeOut(retry_sweep), run_time=0.55)
        self.at("returned to the cytosol")
        boundary_gap = Rectangle(width=2.7, height=0.24, stroke_width=0,
                                 fill_color=BG, fill_opacity=1).move_to(p(0.1, -1.45))
        self.play(FadeIn(boundary_gap), client.animate.move_to(p(-2.0, -2.25)),
                  client_lab.animate.move_to(p(-2.0, -3.08)), run_time=0.9)
        self.at("tagged with ubiquitin")
        ub = chip("ubiquitin", RED, 28).scale(0.68).move_to(p(0.1, -2.25))
        self.play(FadeIn(ub, scale=0.5), run_time=0.55)
        machine = proteasome(p(3.8, -2.25), 1.0, with_label=False)
        self.at("destroyed by the proteasome")
        self.play(FadeIn(machine), client.animate.move_to(p(1.35, -2.25)),
                  FadeOut(client_lab), ub.animate.move_to(p(2.35, -2.9)), run_time=0.85)
        machine_lab = label("proteasome", 30, GOLD).move_to(p(4.45, -3.25))
        self.play(FadeIn(machine_lab), run_time=0.4)
        self.at("Ubiquitin is that small")
        self.play(ub.animate.scale(1.18).shift(UP * 0.18), client.animate.shift(RIGHT * 0.3),
                  run_time=0.55)
        self.play(ub.animate.scale(1 / 1.18).shift(DOWN * 0.18), client.animate.shift(LEFT * 0.3),
                  run_time=0.55)
        self.at("proteasome is a capped barrel")
        self.play(machine[1][0].animate.shift(LEFT * 0.22),
                  machine[1][1].animate.shift(RIGHT * 0.22), run_time=0.55)
        self.play(machine[1][0].animate.shift(RIGHT * 0.22),
                  machine[1][1].animate.shift(LEFT * 0.22), run_time=0.55)
        straight = Line(p(2.65, -2.25), p(4.95, -2.25), color=GREY, stroke_width=7)
        self.at("unfolds and destroys")
        self.play(Transform(client, straight), FadeOut(ub, scale=0.5), run_time=0.8)
        self.play(client.animate.shift(RIGHT * 1.35).set_opacity(0), run_time=0.9)
        self.finish()


class S04LysosomeRoute(SpokenScene):
    def construct(self):
        cell = cell_outline()
        machine = proteasome(p(4.75, 1.7), 0.9)
        mito = mitochondrion(p(-3.5, 0), 2.65, 1.4, with_label=True)
        self.at("damaged mitochondrion")
        self.play(Create(cell), FadeIn(machine), FadeIn(mito), run_time=0.85)
        self.at("cannot enter")
        self.play(mito.animate.move_to(p(2.7, 1.7)), run_time=0.85)
        self.play(mito.animate.shift(LEFT * 0.65), Wiggle(machine, scale_value=1.03), run_time=0.65)
        narrow = label("too wide", 30, RED).move_to(p(-0.5, 1.7))
        self.play(FadeIn(narrow), run_time=0.35)
        self.at("different physical solution")
        mito_label = mito[-1]
        self.play(mito.animate.move_to(p(-2.9, -0.25)), FadeOut(narrow), FadeOut(mito_label), run_time=0.8)
        mito.remove(mito_label)
        c0 = membrane_cup(p(-2.9, -0.25), openness=0.72, radius=1.75)
        c1 = membrane_cup(p(-2.9, -0.25), openness=0.38, radius=1.75)
        c2 = membrane_cup(p(-2.9, -0.25), openness=0.08, radius=1.75)
        self.at("blue membrane cup")
        growth_front = AnnularSector(inner_radius=1.25, outer_radius=1.72, angle=0.95,
                                     start_angle=0, color=BLUE, stroke_width=0,
                                     fill_opacity=0.36).move_to(p(-2.9, -0.25))
        growth_front.add_updater(lambda m, dt: m.rotate(2.1 * dt, about_point=p(-2.9, -0.25)))
        self.play(Create(c0), FadeIn(growth_front), mito.animate.rotate(0.10), run_time=0.8)
        c0.add_updater(lambda m, dt: m.rotate(0.75 * dt, about_point=p(-2.9, -0.25)))
        self.at("grows around the cargo")
        self.play(Transform(c0, c1), mito.animate.rotate(-0.20), run_time=0.9)
        self.at("closes into an autophagosome")
        self.play(Transform(c0, c2), mito.animate.rotate(0.10), run_time=0.8)
        auto_lab = label("autophagosome", 30, BLUE).move_to(p(-2.9, 2.0))
        self.play(FadeIn(auto_lab), run_time=0.4)
        ly = lysosome(p(3.55, -0.65), 1.55, with_label=True)
        self.at("carry bulk cytoplasm")
        bulk = blocks(p(-2.9, -0.15), 2, 2, GREY, 0.24)
        self.play(FadeIn(bulk), FadeIn(ly), run_time=0.7)
        self.play(Indicate(mito, color=GREY), run_time=0.55)
        self.at("carrier fuses")
        c0.clear_updaters()
        growth_front.clear_updaters()
        self.play(VGroup(c0, mito, bulk).animate.move_to(ly[0]), FadeOut(auto_lab),
                  FadeOut(growth_front), run_time=1.15)
        self.play(FadeOut(c0[0]), Transform(c0[1], ly[0].copy().scale(0.72)), run_time=0.55)
        self.at("acidic interior digests")
        self.play(Indicate(ly[0], color=ORANGE, scale_factor=1.06), run_time=0.6)
        products = blocks(ly[0].get_center(), 2, 3, GREY, 0.3)
        self.play(FadeOut(mito, scale=0.35), FadeOut(bulk, scale=0.35),
                  FadeOut(c0[1], scale=0.35), FadeIn(products), run_time=1.05)
        self.at("reusable blocks")
        self.play(products.animate.arrange(RIGHT, buff=0.35).move_to(p(0.1, -2.75)), run_time=0.85)
        self.finish()


class S05Starvation(SpokenScene):
    def construct(self):
        cell = cell_outline(height=5.7, center=p(0, -0.1))
        ly = lysosome(p(4.35, 0.25), 1.35, with_label=True)
        ly[1].add_updater(lambda m, dt: m.rotate(0.55 * dt, about_point=ly[0].get_center()))
        bin_box = RoundedRectangle(width=3.15, height=2.7, corner_radius=0.25,
                                   stroke_color=GREY, stroke_width=4).move_to(p(-0.4, -0.45))
        bin_lab = label("reuse bin", 31, TEXT).move_to(p(-0.4, -2.15))
        full = blocks(p(-0.4, -0.3), 3, 4, GREY, 0.3)
        inlet = Arrow(p(-6.2, 1.55), p(-2.2, 0.15), buff=0,
                      color=GREEN, stroke_width=9, max_tip_length_to_length_ratio=0.1)
        incoming = blocks(p(-5.15, 1.18), 1, 3, GREY, 0.28)
        self.play(Create(cell), FadeIn(bin_box), FadeIn(bin_lab), FadeIn(full), FadeIn(ly),
                  GrowArrow(inlet), FadeIn(incoming), run_time=0.9)
        self.at("Starvation reduces")
        starvation = label("STARVATION", 38, RED, weight=BOLD).move_to(p(-3.95, 3.3))
        thin_inlet = Arrow(p(-6.2, 1.55), p(-2.2, 0.15), buff=0,
                           color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(starvation), Transform(inlet, thin_inlet), FadeOut(incoming), run_time=0.7)
        self.at("reuse bin begins to empty")
        low = blocks(p(-0.4, -0.9), 1, 4, GREY, 0.3)
        self.play(Transform(full, low), run_time=1.05)
        self.at("More cytoplasm now enters")
        cargoes = VGroup(*[blocks(p(-4.4, y), 1, 2, GREY, 0.22) for y in (1.0, 0, -1.0)])
        cups = VGroup(*[carrier(c.get_center(), 0.58) for c in cargoes])
        self.play(LaggedStart(*[FadeIn(c) for c in cargoes], lag_ratio=0.12), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in cups], lag_ratio=0.12), run_time=0.85)
        self.at("reaches lysosomes")
        self.play(*[VGroup(cargoes[i], cups[i]).animate.move_to(ly[0]) for i in range(3)], run_time=1.0)
        recovered = blocks(ly[0].get_center(), 2, 3, GREY, 0.25)
        self.at("Digestion sends recovered")
        self.play(FadeOut(cargoes, scale=0.3), FadeOut(cups, scale=0.3), FadeIn(recovered), run_time=0.65)
        self.at("back into the bin")
        self.play(recovered.animate.move_to(bin_box), run_time=0.75)
        refilled = blocks(p(-0.4, -0.45), 2, 4, GREY, 0.3)
        self.play(Transform(VGroup(full, recovered), refilled), run_time=0.65)
        schem = schematic_tag(p(5.45, 3.3))
        recycle_cargo = carrier(p(0.3, -0.45), 0.52)
        self.at("During starvation")
        cycle = CurvedArrow(p(1.1, -1.0), p(3.4, -0.55), radius=-2.0,
                            color=BLUE, stroke_width=5)
        flow_glow = carrier(p(0.8, -0.45), 0.38)
        def recycling_flow(m, dt):
            m.shift(RIGHT * 4.2 * dt)
            if m.get_x() > 4.4:
                m.move_to(p(0.8, -0.45))
        flow_glow.add_updater(recycling_flow)
        self.play(FadeIn(schem), Create(cycle), FadeIn(recycle_cargo), FadeIn(flow_glow), run_time=0.65)
        self.play(recycle_cargo.animate.move_to(ly[0]), run_time=0.9)
        self.at("recycles cell material")
        return_blocks = blocks(ly[0].get_center(), 1, 3, GREY, 0.28)
        self.play(Transform(recycle_cargo, return_blocks), run_time=0.45)
        self.play(recycle_cargo.animate.move_to(bin_box),
                  refilled.animate.shift(UP * 0.12), run_time=0.9)
        self.at("autophagy defective yeast")
        flow_glow.clear_updaters()
        self.play(FadeOut(VGroup(inlet, starvation, cycle, flow_glow, recycle_cargo)),
                  VGroup(cell, ly, bin_box, bin_lab, refilled).animate.scale(0.66).shift(LEFT * 2.0),
                  run_time=0.8)
        normal = yeast(p(3.1, 0.4), True)
        defective = yeast(p(5.0, 0.4), False)
        labs = VGroup(label("autophagy", 28, BLUE).move_to(p(2.85, -0.95)),
                      label("defective", 28, RED).move_to(p(5.25, -0.95)))
        self.play(FadeIn(normal), FadeIn(defective), FadeIn(labs), run_time=0.75)
        self.at("lose viability faster")
        self.play(defective.animate.set_opacity(0.25).shift(DOWN * 0.35),
                  normal.animate.shift(UP * 0.15), run_time=1.0)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        cell = cell_outline(height=5.9, center=p(0, -0.2))
        pool_box = RoundedRectangle(width=4.0, height=3.6, corner_radius=0.35,
                                    stroke_color=GREY, stroke_width=4,
                                    fill_color=BLUE, fill_opacity=0.20).move_to(p(0, -0.25))
        pool = VGroup(*[carrier(p(-0.85 + (i % 3) * 0.85, -0.75 + (i // 3) * 0.9), 0.28)
                        for i in range(6)])
        arr = Arrow(p(-5.8, -0.25), p(-2.25, -0.25), buff=0,
                    color=BLUE, stroke_width=7)
        clr = Arrow(p(2.25, -0.25), p(5.8, -0.25), buff=0,
                    color=ORANGE, stroke_width=7)
        arrival_stream = VGroup(*[Dot(radius=0.14, color=BLUE) for _ in range(4)]).arrange(RIGHT, buff=0.18).move_to(p(-5.1, -0.25))
        clearance_stream = VGroup(*[Dot(radius=0.14, color=ORANGE) for _ in range(4)]).arrange(RIGHT, buff=0.18).move_to(p(2.9, -0.25))
        arrival_stream.speed = 3.2
        clearance_stream.speed = 3.2
        def arrival_flow(m, dt):
            m.shift(RIGHT * m.speed * dt)
            if m.get_x() > -2.45:
                m.move_to(p(-5.1, -0.25))
        def clearance_flow(m, dt):
            m.shift(RIGHT * m.speed * dt)
            if m.get_x() > 5.55:
                m.move_to(p(2.9, -0.25))
        arrival_stream.add_updater(arrival_flow)
        clearance_stream.add_updater(clearance_flow)
        labs = VGroup(label("arrival", 31, BLUE).move_to(p(-4.0, 0.65)),
                      label("clearance", 31, ORANGE).move_to(p(4.0, 0.65)),
                      label("carrier pool", 32, TEXT).move_to(p(0, 2.05)))
        self.at("watch the carrier pool")
        self.play(Create(cell), FadeIn(pool_box), FadeIn(pool), GrowArrow(arr), GrowArrow(clr),
                  FadeIn(arrival_stream), FadeIn(clearance_stream), FadeIn(labs), run_time=1.0)
        equation = M("pool change = arrival − clearance", 34, TEXT).move_to(p(0, 3.35))
        self.at("change equals arrival")
        flow_in = VGroup(*[carrier(p(-5.5, y), 0.24) for y in (-0.8, -0.25, 0.3)])
        flow_out = VGroup(*[carrier(p(1.25, y), 0.24) for y in (-0.8, -0.25, 0.3)])
        self.play(Write(equation), FadeIn(flow_in), FadeIn(flow_out), run_time=0.55)
        self.play(flow_in.animate.shift(RIGHT * 3.8), flow_out.animate.shift(RIGHT * 4.1).set_opacity(0),
                  run_time=1.25)
        self.at("over the interval")
        self.play(FadeOut(flow_in), Indicate(arr, color=BLUE), Indicate(clr, color=ORANGE), run_time=0.75)
        level = ValueTracker(0.52)
        gauge_mob = gauge(4.95, level, "pool", BLUE, height=1.4, center_y=-2.05)
        moving_in = carrier(p(-5.2, -0.25), 0.25)
        moving_out = pool[-1].copy()
        self.at("Matching rates")
        self.play(FadeIn(gauge_mob), FadeIn(moving_in), run_time=0.4)
        self.play(moving_in.animate.move_to(p(-1.45, -0.25)),
                  moving_out.animate.move_to(p(5.2, -0.25)).set_opacity(0), run_time=1.05)
        self.at("keep the pool level")
        self.play(Indicate(gauge_mob[0], color=BLUE), run_time=0.65)
        self.at("Faster arrival")
        arrival_stream.speed = 5.2
        thick_arr = Arrow(p(-5.8, -0.25), p(-2.25, -0.25), buff=0,
                          color=BLUE, stroke_width=13)
        extra = VGroup(carrier(p(-5.0, 0.1), 0.24), carrier(p(-5.0, -0.6), 0.24))
        self.play(Transform(arr, thick_arr), FadeIn(extra), run_time=0.45)
        self.play(extra.animate.move_to(p(-1.1, -0.25)), level.animate.set_value(0.9), run_time=1.0)
        high_mark = DashedLine(p(4.2, -1.55), p(5.7, -1.55), color=YELLOW, dash_length=0.12)
        self.play(FadeIn(high_mark), run_time=0.35)
        self.at("Slower clearance")
        arrival_stream.speed = 3.2
        clearance_stream.speed = 0.9
        self.play(Transform(arr, Arrow(p(-5.8, -0.25), p(-2.25, -0.25), buff=0,
                                      color=BLUE, stroke_width=7)),
                  FadeOut(extra), level.animate.set_value(0.52), run_time=0.55)
        thin_clr = Arrow(p(2.25, -0.25), p(5.8, -0.25), buff=0,
                         color=ORANGE, stroke_width=3)
        self.play(Transform(clr, thin_clr), run_time=0.45)
        backup = VGroup(carrier(p(1.2, 0.55), 0.24), carrier(p(1.2, -0.5), 0.24))
        self.play(FadeIn(backup), level.animate.set_value(0.9), run_time=0.95)
        self.at("larger pool can mean")
        brace_words = label("same high pool", 30, YELLOW).move_to(p(4.85, -3.5))
        self.play(FadeIn(brace_words), Indicate(high_mark, color=YELLOW), run_time=0.65)
        self.at("faster arrival or slower clearance")
        self.play(Indicate(arr, color=BLUE), Indicate(clr, color=ORANGE), run_time=0.9)
        self.at("experiment that separates")
        question = label("Close the exit. Watch the rise.", 36, TEXT, weight=BOLD).move_to(p(0, 3.35))
        self.play(FadeOut(VGroup(brace_words, equation)), FadeIn(question), run_time=0.75)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        left = pool_panel(-3.15, "POOL A", "fast arrival")
        right = pool_panel(3.15, "POOL B", "slow arrival")
        for panel in (left, right):
            for car in panel[-1]:
                center = car[0].get_center().copy()
                for mark in car[-3:]:
                    mark.add_updater(lambda m, dt, c=center: m.rotate(5.0 * dt, about_point=c))
        self.play(FadeIn(left), FadeIn(right), run_time=0.75)
        self.at("protein form attached")
        self.play(left[-1].animate.shift(UP * 0.18), right[-1].animate.shift(UP * 0.18),
                  run_time=0.55)
        self.play(left[-1].animate.shift(DOWN * 0.18), right[-1].animate.shift(DOWN * 0.18),
                  run_time=0.55)
        self.at("marks the carriers")
        lc = label("LC3-II", 34, PURPLE, weight=BOLD).move_to(p(0, 3.15))
        self.play(FadeIn(lc), run_time=0.5)
        self.at("Bafilomycin blocks")
        blocks_baf = VGroup(baf_block(-3.15), baf_block(3.15))
        self.play(FadeIn(blocks_baf), left[4].animate.set_fill(ORANGE, opacity=0.02),
                  right[4].animate.set_fill(ORANGE, opacity=0.02), run_time=0.7)
        self.at("closing the exit")
        self.play(Indicate(blocks_baf, color=RED, scale_factor=1.05), run_time=0.7)
        self.at("two LC32 pools")
        start_line = DashedLine(p(-5.7, 0.95), p(5.7, 0.95), color=YELLOW,
                                dash_length=0.15).set_opacity(0.75)
        self.play(Create(start_line), run_time=0.65)
        self.at("start equally high")
        self.play(Indicate(left[-1], color=PURPLE, scale_factor=1.03),
                  Indicate(right[-1], color=PURPLE, scale_factor=1.03), run_time=0.75)
        self.at("which pool rises more")
        q = label("After the block, which pool rises more?", 36, TEXT, weight=BOLD).move_to(p(0, 3.15))
        self.play(Transform(lc, q), run_time=0.7)
        self.at("fast arrival or slow")
        schem = VGroup(schematic_tag(p(-3.15, -3.2)), schematic_tag(p(3.15, -3.2)))
        self.play(FadeIn(schem),
                  left[-1].animate.shift(UP * 0.06), right[-1].animate.shift(DOWN * 0.06), run_time=0.8,
                  rate_func=there_and_back)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        left = pool_panel(-3.15, "POOL A", "fast arrival")
        right = pool_panel(3.15, "POOL B", "slow arrival")
        baf = VGroup(baf_block(-3.15), baf_block(3.15))
        q = label("After the block, which pool rises more?", 36, TEXT, weight=BOLD).move_to(p(0, 3.15))
        start_line = DashedLine(p(-5.7, 0.95), p(5.7, 0.95), color=YELLOW,
                                dash_length=0.15).set_opacity(0.75)
        schem = VGroup(schematic_tag(p(-3.15, -3.2)), schematic_tag(p(3.15, -3.2)))
        self.add(left, right, baf, q, start_line, schem)
        # The pause is deliberate, but the LC3 marks drift gently without revealing a result.
        self.play(left[-1].animate.shift(UP * 0.08), right[-1].animate.shift(DOWN * 0.08),
                  run_time=2.2, rate_func=there_and_back)
        self.play(left[-1].animate.shift(DOWN * 0.08), right[-1].animate.shift(UP * 0.08),
                  run_time=2.2, rate_func=there_and_back)


class S09Reveal(SpokenScene):
    def construct(self):
        left_level, right_level = ValueTracker(0.46), ValueTracker(0.46)
        left_g = gauge(-3.0, left_level, "fast arrival")
        right_g = gauge(3.0, right_level, "slow arrival")
        gauge_sheens = VGroup(*[
            Rectangle(width=1.0, height=0.34, stroke_width=0,
                      fill_color=TEXT, fill_opacity=0.38).move_to(p(x, -1.55))
            for x in (-3.0, 3.0)
        ])
        def lift_sheen(m, dt):
            m.shift(UP * 0.95 * dt)
            if m.get_y() > 1.05:
                m.move_to(p(m.get_x(), -1.55))
        for sheen in gauge_sheens:
            sheen.add_updater(lift_sheen)
        start = DashedLine(p(-5.0, -0.4), p(5.0, -0.4), color=YELLOW,
                           dash_length=0.16).set_opacity(0.8)
        baf = VGroup(
            Rectangle(width=1.55, height=0.22, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(p(-3, -2.35)),
            Rectangle(width=1.55, height=0.22, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(p(3, -2.35)),
            label("clearance stopped", 30, RED).move_to(p(0, -3.52)),
        )
        panels = VGroup(*[
            RoundedRectangle(width=5.45, height=6.35, corner_radius=0.4,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.18).move_to(p(x, 0))
            for x in (-3.0, 3.0)
        ])
        time_track = Line(p(-5.3, 3.3), p(5.3, 3.3), color=YELLOW,
                          stroke_width=3).set_opacity(0.55)
        time_cursor = Dot(p(-5.2, 3.3), radius=0.11, color=YELLOW)
        def advance_time(m, dt):
            m.shift(RIGHT * 4.0 * dt)
            if m.get_x() > 5.55:
                m.move_to(p(-5.2, 3.3))
        time_cursor.add_updater(advance_time)
        same_time = label("same time interval", 28, YELLOW).move_to(p(0, 3.62))
        self.add(panels, time_track, time_cursor, left_g, right_g, gauge_sheens,
                 start, baf, same_time)
        self.at("fast arrival pool")
        self.play(left_level.animate.set_value(0.92), run_time=1.2)
        self.at("rises more after")
        self.play(Indicate(left_g[1], color=PURPLE, scale_factor=1.03), run_time=0.65)
        self.at("purple gauge climbs")
        self.play(right_level.animate.set_value(0.56), run_time=1.0)
        self.at("slow arrival gauge")
        self.play(Indicate(right_g[1], color=PURPLE, scale_factor=1.03), run_time=0.65)
        left_delta = DoubleArrow(p(-4.0, -0.35), p(-4.0, 1.12), buff=0,
                                 color=YELLOW, stroke_width=5)
        right_delta = DoubleArrow(p(2.0, -0.35), p(2.0, -0.03), buff=0,
                                  color=YELLOW, stroke_width=5)
        delta_labs = VGroup(label("extra accumulation", 28, YELLOW).move_to(p(-3.0, 2.75)),
                            label("extra accumulation", 28, YELLOW).move_to(p(3.0, 2.75)))
        self.play(GrowArrow(left_delta), GrowArrow(right_delta), FadeIn(delta_labs), run_time=0.9)
        self.at("complete lysosomal block")
        self.play(baf[0].animate.scale(1.12), baf[1].animate.scale(1.12), run_time=0.55)
        self.play(baf[0].animate.scale(1 / 1.12), baf[1].animate.scale(1 / 1.12), run_time=0.55)
        self.at("formation unchanged")
        condition = chip("formation unchanged", BLUE, 28).scale(0.72).move_to(p(0, 3.62))
        continuing = VGroup(*[
            carrier(p(x, 0.1), 0.22) for x in (-5.5, -4.9, 4.9, 5.5)
        ])
        time_cursor.clear_updaters()
        self.play(FadeOut(delta_labs), FadeOut(VGroup(same_time, time_track, time_cursor)),
                  FadeIn(condition), FadeIn(continuing), run_time=0.55)
        self.play(continuing[:2].animate.shift(RIGHT * 1.2),
                  continuing[2:].animate.shift(LEFT * 1.2), run_time=0.85)
        self.at("extra LC32 estimates")
        self.play(Indicate(left_delta, color=YELLOW), Indicate(right_delta, color=YELLOW), run_time=0.8)
        turnover = label("extra LC3-II ≈ turnover over interval", 30, YELLOW).move_to(p(0, 3.52))
        self.play(FadeOut(condition), FadeOut(continuing), FadeIn(turnover), run_time=0.7)
        self.at("equal starting amounts")
        self.play(Indicate(start, color=YELLOW, scale_factor=1.0), run_time=0.75)
        self.at("could not reveal")
        self.play(Indicate(VGroup(left_delta, right_delta), color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        left = pool_panel(-3.15, "POOL A", "fast arrival")
        right = pool_panel(3.15, "POOL B", "slow arrival")
        start_line = DashedLine(p(-5.7, 0.95), p(5.7, 0.95), color=YELLOW,
                                dash_length=0.15).set_opacity(0.75)
        self.at("two cells with equal")
        self.play(FadeIn(left), FadeIn(right), Create(start_line), run_time=0.9)
        self.play(left[-1].animate.shift(UP * 0.16), right[-1].animate.shift(DOWN * 0.16),
                  run_time=1.15, rate_func=there_and_back)
        self.play(left[-1].animate.shift(DOWN * 0.16), right[-1].animate.shift(UP * 0.16),
                  run_time=1.15, rate_func=there_and_back)
        self.at("visible amounts matched")
        self.play(Indicate(left[-1], color=PURPLE), Indicate(right[-1], color=PURPLE), run_time=0.75)
        self.at("flows did not")
        self.play(Indicate(left[2], color=BLUE), Indicate(right[2], color=BLUE), run_time=0.75)
        baf = VGroup(baf_block(-3.15), baf_block(3.15))
        self.at("Closing the exit")
        self.play(FadeIn(baf), run_time=0.55)
        extra_fast = VGroup(carrier(p(-4.2, -1.25), 0.32, lc3=True),
                            carrier(p(-3.15, -1.25), 0.32, lc3=True))
        extra_slow = carrier(p(3.15, -1.25), 0.32, lc3=True)
        self.at("exposed the difference")
        self.play(FadeIn(extra_fast, shift=RIGHT * 0.35), FadeIn(extra_slow, shift=RIGHT * 0.12), run_time=1.0)
        self.at("same question works")
        self.remove(left[1], left[3], right[1], right[3], baf[0][1], baf[1][1])
        self.play(FadeOut(VGroup(left, right, start_line, baf, extra_fast, extra_slow)), run_time=0.55)
        cell = cell_outline()
        er = RoundedRectangle(width=3.6, height=2.2, corner_radius=0.3,
                              stroke_color=GREY, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.06).move_to(p(-3.6, 1.0))
        machine = proteasome(p(0.5, 1.0), 0.75)
        c = carrier(p(-2.9, -1.45), 0.65)
        ly = lysosome(p(2.8, -1.45), 1.05, with_label=False)
        self.play(Create(cell), FadeIn(er), FadeIn(machine), FadeIn(c), FadeIn(ly), run_time=0.9)
        self.at("cargo and route change")
        protein = VMobject(color=GREY, stroke_width=6).set_points_smoothly([
            p(-4.5, 1.1), p(-4.1, 1.45), p(-3.7, 0.65), p(-3.2, 1.25)
        ])
        self.play(Create(protein), protein.animate.move_to(p(-1.2, 1.0)), c.animate.move_to(p(0.8, -1.45)), run_time=0.9)
        self.play(protein.animate.move_to(machine[0]).set_opacity(0), c.animate.move_to(ly[0]), run_time=0.8)
        arrival = Arrow(p(-5.75, -2.55), p(-1.2, -2.55), buff=0,
                        color=BLUE, stroke_width=8)
        clearance = Arrow(p(1.2, -2.55), p(5.75, -2.55), buff=0,
                          color=ORANGE, stroke_width=8)
        self.at("Wherever material piles")
        self.play(GrowArrow(arrival), GrowArrow(clearance), run_time=0.75)
        self.at("ask two questions")
        q = label("Follow the flow", 38, TEXT, weight=BOLD).move_to(p(0, 3.48))
        self.play(FadeIn(q), run_time=0.55)
        self.at("How fast does it arrive")
        arr_lab = label("How fast does it arrive?", 30, BLUE).move_to(p(-3.5, -3.45))
        arr_pulse = VGroup(*[carrier(p(-5.45 + i * 0.5, -2.55), 0.22) for i in range(3)])
        self.play(FadeIn(arr_lab), FadeIn(arr_pulse), run_time=0.4)
        self.play(arr_pulse.animate.shift(RIGHT * 3.8), run_time=1.0)
        self.at("How fast does it leave", nth=0)
        clr_lab = label("How fast does it leave?", 30, ORANGE).move_to(p(3.5, -3.45))
        clr_pulse = VGroup(*[
            Square(side_length=0.35, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9)
            .move_to(p(1.45 + i * 0.5, -2.55)) for i in range(3)
        ])
        self.play(FadeIn(clr_lab), FadeIn(clr_pulse), run_time=0.4)
        self.play(clr_pulse.animate.shift(RIGHT * 3.65), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "Follow the flow, not the pile."
