"""The carbon fatty acid synthesis throws away.

COLOR MAP (one color per concept throughout)
  BLUE    machinery: ACC and fatty acid synthase
  YELLOW  bicarbonate carbon / temporary carboxyl handle / CO2
  GREEN   acetyl units and the growing fatty-acid chain
  TEAL    ATP
  PURPLE  NADPH
  RED     blocked or uphill route
  GREY    assembly-floor structure

Everything is a labelled block, badge, machine, track, or counter.  No molecular
structures are drawn.  The energy track in S07 is explicitly marked schematic.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


# ---------------------------------------------------------------------------
# Shared assembly-floor vocabulary.  Reusing these coordinates is deliberate:
# the viewer stays in one world as ACC feeds the same FAS loop.
ACC_X = -3.75
FAS_C = np.array([2.25, 0.25, 0.0])
LOOP_R = 1.72
TRAVEL_R = 0.72


def label_box(text, color, width=2.15, height=0.86, size=28):
    box = RoundedRectangle(
        corner_radius=0.14, width=width, height=height,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.18,
    )
    lab = T(text, size=size, color=color, weight=BOLD).move_to(box)
    return VGroup(box, lab)


def carbon_block(text="2C", width=1.65, color=GREEN, size=28):
    return label_box(text, color, width=width, height=0.9, size=size)


def badge(text="CO₂", size=28):
    return chip(text, YELLOW, size=size, pad=0.17, fill_opacity=0.25)


def coin(text="ATP", size=28):
    disk = Circle(radius=0.43, stroke_color=TEAL, stroke_width=3,
                  fill_color=TEAL, fill_opacity=0.22)
    return VGroup(disk, T(text, size=size, color=TEAL, weight=BOLD).move_to(disk))


def battery(text="NADPH", size=28):
    body = RoundedRectangle(corner_radius=0.1, width=1.65, height=0.72,
                            stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.2)
    nub = Rectangle(width=0.16, height=0.28, stroke_color=PURPLE,
                    fill_color=PURPLE, fill_opacity=1).next_to(body, RIGHT, buff=0)
    lab = T(text, size=size, color=PURPLE, weight=BOLD).move_to(body)
    return VGroup(body, nub, lab)


def gear(radius=0.48, color=BLUE, speed=0.38):
    ring = Circle(radius=radius, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.08)
    spokes = VGroup(*[
        Line(LEFT * radius * 0.82, RIGHT * radius * 0.82,
             color=color, stroke_width=3).rotate(a)
        for a in (0, PI / 4, PI / 2, 3 * PI / 4)
    ])
    g = VGroup(ring, spokes)
    g.add_updater(lambda m, dt: m.rotate(speed * dt))
    return g


def conveyor(y=-3.25, x=0, width=11.8, speed=0.48):
    """A continuously moving belt; its broad ticks register in the motion lint."""
    base = RoundedRectangle(corner_radius=0.18, width=width, height=0.68,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    left = x - width / 2 + 0.28
    right = x + width / 2 - 0.28
    ticks = VGroup(*[
        Line(DOWN * 0.22, UP * 0.22, color=TEXT, stroke_width=6).set_opacity(0.58)
        .move_to([xx, y, 0])
        for xx in np.arange(left, right + 0.01, 0.65)
    ])

    def crawl(m, dt):
        for tick in m:
            tick.shift(RIGHT * speed * dt)
            if tick.get_x() > right:
                tick.set_x(left)

    ticks.add_updater(crawl)
    rollers = VGroup(
        Circle(radius=0.2, stroke_color=GREY, stroke_width=3).move_to([left, y, 0]),
        Circle(radius=0.2, stroke_color=GREY, stroke_width=3).move_to([right, y, 0]),
    )
    rollers.add_updater(lambda m, dt: m.rotate(-speed * dt * 2.2))
    return VGroup(base, ticks, rollers)


def floor_world(scene, dim=1.0):
    belt = conveyor()
    motes = VGroup(*[
        Dot([x, y, 0], radius=0.035, color=GREY).set_opacity(0.28)
        for x, y in [(-6, 2.7), (-4.8, 1.1), (-2.7, 3.1), (-0.5, 2.5),
                     (1.2, 3.15), (3.5, 2.55), (5.7, 1.2), (4.8, -1.5)]
    ])

    def drift(m, dt):
        for d in m:
            d.shift(UP * 0.075 * dt + RIGHT * 0.025 * dt)
            if d.get_y() > 3.55:
                d.set_y(-2.2)

    motes.add_updater(drift)
    world = VGroup(belt, motes).set_opacity(dim)
    scene.add(world)
    return world


def acc_gate(pos=np.array([ACC_X, 0.15, 0]), scale=1.0):
    body = RoundedRectangle(corner_radius=0.28, width=2.15, height=2.65,
                            stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.14).move_to(pos)
    slot = RoundedRectangle(corner_radius=0.08, width=1.38, height=0.34,
                            stroke_color=GREY, stroke_width=2).move_to(pos + DOWN * 0.56)
    g = gear(0.45, BLUE, 0.4).move_to(pos + UP * 0.42)
    lab = T("ACC", size=31, color=BLUE, weight=BOLD).next_to(body, UP, buff=0.16)
    return VGroup(body, slot, g, lab).scale(scale)


def fas_machine(center=FAS_C, compact=False):
    w, h = (4.45, 4.65) if not compact else (4.1, 4.25)
    shell = RoundedRectangle(corner_radius=0.42, width=w, height=h,
                             stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.1).move_to(center)
    mouth = RoundedRectangle(corner_radius=0.12, width=1.1, height=0.58,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=BG, fill_opacity=1).move_to(shell.get_left())
    chute = Arrow(center + UP * 1.0, center + UP * 2.75, buff=0.08,
                  color=YELLOW, stroke_width=6, tip_length=0.22)
    lab = T("fatty acid synthase", size=28, color=BLUE, weight=BOLD)
    lab.next_to(shell, DOWN, buff=0.16)
    g1 = gear(0.38, BLUE, -0.42).move_to(center + RIGHT * 1.15 + DOWN * 1.15)
    g2 = gear(0.30, BLUE, 0.5).move_to(center + RIGHT * 0.35 + DOWN * 1.35)
    return VGroup(shell, mouth, chute, lab, g1, g2)


def prediction_layout(scene):
    """Exact same construction in the spoken prediction and its silent hold."""
    floor_world(scene)
    fas = fas_machine(center=np.array([2.35, -0.05, 0]))
    ext = carbon_block("2C EXTENDER", width=2.45).move_to([-1.15, -0.45, 0])
    handle = badge("CO₂").scale(0.86).next_to(ext, UP, buff=0.08)
    question = T("Where does this carbon go?", size=38, font=TITLE_FONT)
    question.move_to([0, 3.18, 0])
    chain_target = carbon_block("CHAIN", width=2.0).move_to([4.6, 1.25, 0])
    out_target = badge("CO₂").move_to([1.0, 2.0, 0])
    a_chain = Arrow(handle.get_right(), chain_target.get_left(), buff=0.12,
                    color=GREEN, stroke_width=6, tip_length=0.24)
    a_out = Arrow(handle.get_top(), out_target.get_bottom(), buff=0.12,
                  color=YELLOW, stroke_width=6, tip_length=0.24)
    return fas, ext, handle, question, chain_target, out_target, a_chain, a_out


def loop_world(scene, show_acc=False):
    floor_world(scene)
    shell = RoundedRectangle(corner_radius=0.4, width=4.7, height=4.95,
                             stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.09).move_to(FAS_C)
    # Cargo travels on the inner rail so it never covers the C/R/D/R station labels.
    path = Circle(radius=TRAVEL_R, color=GREY, stroke_width=5).move_to(FAS_C)
    path.add_tip(tip_length=0.22, tip_width=0.22)
    angles = [135, 45, -45, -135]
    letters = ["C", "R", "D", "R"]
    stations = VGroup()
    for a, letter in zip(angles, letters):
        p = FAS_C + LOOP_R * np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0])
        station = VGroup(
            Circle(radius=0.39, stroke_color=BLUE, stroke_width=3,
                   fill_color=BG, fill_opacity=1),
            T(letter, size=30, color=BLUE, weight=BOLD),
        ).move_to(p)
        station[1].move_to(station[0])
        station.add_updater(lambda m, dt: m[0].rotate(0.28 * dt))
        stations.add(station)
    lab = T("fatty acid synthase", size=28, color=BLUE, weight=BOLD)
    lab.next_to(shell, DOWN, buff=0.1)
    group = VGroup(shell, path, stations, lab)
    if show_acc:
        acc = acc_gate()
        group.add(acc)
    scene.add(group)
    return group, path, stations


def spring(center=np.array([0, 0, 0]), width=2.2, height=0.55, turns=8, color=TEAL):
    pts = []
    for i in range(turns * 2 + 1):
        x = -width / 2 + width * i / (turns * 2)
        y = (height / 2) * (1 if i % 2 else -1)
        if i in (0, turns * 2):
            y = 0
        pts.append(center + np.array([x, y, 0]))
    return VMobject(color=color, stroke_width=6).set_points_as_corners(pts)


# ---------------------------------------------------------------------------
class S00Hook(SpokenScene):
    def construct(self):
        floor_world(self)
        gate = acc_gate(pos=np.array([-1.3, 0.2, 0]), scale=1.1)
        chute = Arrow([2.1, 0.7, 0], [3.45, 1.65, 0], buff=0.1,
                      color=YELLOW, stroke_width=7, tip_length=0.28)
        block = carbon_block("2C acetyl CoA", width=2.55).move_to([-4.7, -0.55, 0])
        atp = coin().move_to([-2.0, 2.25, 0])
        handle = badge().move_to([0.15, 1.5, 0])
        question = T("Why add, then discard?", size=40, font=TITLE_FONT).move_to([1.45, 3.12, 0])

        self.play(FadeIn(gate), FadeIn(block, shift=RIGHT * 0.3), run_time=0.8)
        self.at("pay to attach")
        self.play(atp.animate.move_to([-3.05, 1.35, 0]),
                  block.animate.move_to([-2.6, -0.55, 0]), run_time=1.0)
        self.at("carbon dioxide")
        self.play(FadeIn(handle, shift=DOWN * 0.2), Rotate(gate[2], PI / 2), run_time=0.85)
        self.play(handle.animate.next_to(block, UP, buff=0.08), FadeOut(atp, scale=0.5), run_time=0.55)
        self.at("throw it away")
        self.play(block.animate.move_to([1.2, -0.55, 0]),
                  handle.animate.move_to([1.2, 0.35, 0]), GrowArrow(chute), run_time=1.1)
        self.play(handle.animate.move_to([3.55, 2.45, 0]), run_time=0.75)
        self.at("That apparent waste")
        self.play(Write(question), block.animate.shift(LEFT * 0.35), run_time=0.8)
        self.at("the trick")
        self.play(block.animate.shift(RIGHT * 0.7), Indicate(chute, color=YELLOW), run_time=1.0)
        self.at("move forward")
        self.play(block.animate.shift(RIGHT * 1.5), run_time=0.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Fatty acid synthesis"
    TITLE = "The carbon fatty acid synthesis throws away"

    def construct(self):
        floor_world(self, dim=0.5)
        gate = acc_gate(pos=np.array([-4.7, -0.15, 0]), scale=0.72).set_opacity(0.45)
        attached = carbon_block("2C", width=1.3).move_to([-0.1, -0.85, 0])
        handle = badge().scale(0.82).next_to(attached, UP, buff=0.08)
        title = VGroup(
            T("The carbon fatty acid synthesis", size=47, font=TITLE_FONT),
            T("throws away", size=52, color=YELLOW, font=TITLE_FONT),
        ).arrange(DOWN, buff=0.16).move_to([0.8, 1.45, 0])
        self.add(gate, attached, handle)
        self.play(FadeIn(title, shift=UP * 0.16), run_time=0.75)
        self.play(attached.animate.shift(RIGHT * 0.8), handle.animate.shift(RIGHT * 0.8), run_time=0.8)
        self.finish()


class S02Scope(SpokenScene):
    def construct(self):
        floor_world(self)
        small_title = T("The carbon fatty acid synthesis throws away", size=28,
                        font=TITLE_FONT, color=GREY).to_edge(UP, buff=0.25)
        clamp = RoundedRectangle(corner_radius=0.22, width=3.0, height=1.5,
                                 stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.1).move_to([-4.2, 0.55, 0])
        gate = acc_gate(pos=np.array([2.85, 0.35, 0]), scale=0.9)
        primer = carbon_block("2C PRIMER", width=2.45).move_to([-4.2, 0.55, 0])
        pair = carbon_block("2C", width=1.35).move_to([-4.9, -1.65, 0])
        self.add(small_title, clamp, gate)

        self.at("begin with acetyl")
        self.play(FadeIn(primer, shift=RIGHT * 0.35), run_time=0.8)
        self.at("already in the cytoplasm")
        cyt = T("cytoplasm", size=28, color=GREY).move_to([-4.2, 1.75, 0])
        self.play(FadeIn(cyt), clamp.animate.set_stroke(GREEN, width=4), run_time=0.8)
        self.at("two carbons")
        self.play(Indicate(primer, color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("Every later pair")
        self.play(FadeIn(pair), pair.animate.move_to([0.6, -1.65, 0]), run_time=1.25)
        self.at("malonyl")
        self.play(pair.animate.move_to([1.05, -0.25, 0]), Rotate(gate[2], PI), run_time=0.9)
        extender = carbon_block("2C EXTENDER", width=2.55).move_to([5.0, -1.2, 0])
        self.at("the extender")
        self.play(ReplacementTransform(pair, extender), run_time=0.9)
        self.at("carboxylase")
        self.play(Indicate(gate[3], color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("a CC")
        self.play(gate[2].animate.rotate(PI), extender.animate.shift(RIGHT * 0.35), run_time=0.7)
        self.finish()


class S03Acc(SpokenScene):
    def construct(self):
        floor_world(self)
        gate = acc_gate(pos=np.array([0, 0.1, 0]), scale=1.28)
        acetyl = carbon_block("acetyl CoA", width=2.45).move_to([-4.6, 0.2, 0])
        bicarbonate = badge("bicarbonate", size=28).move_to([-2.3, 2.3, 0])
        atp = coin().move_to([0.1, 2.55, 0])
        crank = gear(0.65, TEAL, 0).move_to([2.0, 0.25, 0])
        arm = Line([0.8, 0.25, 0], [1.35, 0.25, 0], color=TEAL, stroke_width=6)
        self.add(gate, crank, arm)

        self.at("combines acetyl")
        self.play(FadeIn(acetyl), acetyl.animate.move_to([-2.8, -0.65, 0]), run_time=1.0)
        self.at("with bicarbonate")
        self.play(FadeIn(bicarbonate), bicarbonate.animate.move_to([-2.55, 1.15, 0]), run_time=0.85)
        self.at("spends 1 ATP")
        acetyl_token = Dot(radius=0.18, color=GREEN).move_to([-0.45, -0.6, 0])
        bicarbonate_token = Dot(radius=0.18, color=YELLOW).move_to([-0.45, 0.65, 0])
        self.play(ReplacementTransform(acetyl, acetyl_token),
                  ReplacementTransform(bicarbonate, bicarbonate_token),
                  FadeIn(atp), atp.animate.move_to([2.95, 1.25, 0]),
                  Rotate(crank, PI), run_time=0.9)
        product = carbon_block("2C EXTENDER", width=2.55).move_to([4.5, -0.45, 0])
        handle = badge().scale(0.84).next_to(product, UP, buff=0.08)
        self.at("The product")
        self.play(FadeOut(acetyl_token), FadeOut(bicarbonate_token), FadeOut(atp, scale=0.4),
                  FadeIn(product, shift=RIGHT * 0.5), FadeIn(handle), run_time=1.0)
        self.at("extra carboxyl group")
        self.play(Indicate(handle, color=YELLOW, scale_factor=1.18), run_time=0.85)
        alt1 = Line([3.1, -0.5, 0], [5.5, 1.35, 0], color=GREY, stroke_width=4)
        alt2 = Line([3.1, -0.5, 0], [5.5, -2.0, 0], color=GREY, stroke_width=4)
        route = Arrow([3.1, -1.25, 0], [5.7, -1.25, 0], buff=0.05,
                      color=GREEN, stroke_width=7, tip_length=0.25)
        self.at("Because the malonyl")
        self.play(product.animate.shift(RIGHT * 0.35), handle.animate.shift(RIGHT * 0.35),
                  Rotate(crank, PI), run_time=1.35)
        self.at("essentially one fate")
        self.play(Create(alt1), Create(alt2), run_time=0.45)
        self.play(Uncreate(alt1), Uncreate(alt2), GrowArrow(route), run_time=0.9)
        committed = chip("COMMITTED STEP", GOLD, size=29).move_to([0, -1.9, 0])
        self.at("committed step")
        self.play(FadeIn(committed, shift=UP * 0.2), product.animate.shift(RIGHT * 0.35),
                  handle.animate.shift(RIGHT * 0.35), run_time=0.85)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        fas, ext, handle, question, chain, out, a_chain, a_out = prediction_layout(self)
        self.add(fas, ext, handle)
        self.at("Now predict")
        self.play(ext.animate.move_to([0.2, -0.45, 0]), handle.animate.shift(RIGHT * 1.35), run_time=1.0)
        self.at("fatty acid synthase")
        self.play(Indicate(fas[0], color=BLUE, scale_factor=1.03), run_time=0.75)
        self.at("newly attached carboxyl")
        self.play(Indicate(handle, color=YELLOW, scale_factor=1.22), run_time=0.8)
        self.at("carbon end up")
        self.play(Write(question), run_time=0.7)
        self.at("In the chain")
        self.play(GrowArrow(a_chain), FadeIn(chain), run_time=0.65)
        self.at("somewhere else")
        self.play(GrowArrow(a_out), FadeIn(out), run_time=0.65)
        self.play(a_chain.animate.set_opacity(0.45), a_out.animate.set_opacity(1), run_time=0.35)
        self.finish()


class S05PredictHold(Scene):
    def construct(self):
        fas, ext, handle, question, chain, out, a_chain, a_out = prediction_layout(self)
        self.add(fas, ext, handle, question, chain, out, a_chain, a_out)
        self.play(Indicate(handle, color=YELLOW, scale_factor=1.2),
                  a_chain.animate.set_opacity(0.42), run_time=1.1)
        self.play(Indicate(out, color=YELLOW, scale_factor=1.15),
                  a_out.animate.set_opacity(0.45), a_chain.animate.set_opacity(1), run_time=1.1)
        self.play(Indicate(handle, color=YELLOW, scale_factor=1.2),
                  a_out.animate.set_opacity(1), a_chain.animate.set_opacity(0.45), run_time=1.1)
        self.wait(1.2)


class S06Condense(SpokenScene):
    def construct(self):
        floor_world(self)
        fas = fas_machine(center=np.array([1.55, -0.05, 0]))
        primer = carbon_block("2C PRIMER", width=2.25).move_to([-4.8, 0.25, 0])
        extender = carbon_block("2C EXTENDER", width=2.45).move_to([-4.8, -1.15, 0])
        handle = badge().scale(0.84).next_to(extender, UP, buff=0.05)
        self.add(fas, primer, extender, handle)

        self.at("joins the extender")
        self.play(primer.animate.move_to([0.35, 0.85, 0]), run_time=0.65)
        self.play(extender.animate.move_to([0.35, -0.75, 0]),
                  handle.animate.move_to([0.35, -0.05, 0]), run_time=0.75)
        chain = carbon_block("4C CHAIN", width=3.7).move_to([1.8, -0.3, 0])
        self.at("During condensation")
        self.play(ReplacementTransform(VGroup(primer, extender), chain), run_time=0.9)
        correct = Arrow(handle.get_center(), [2.4, 2.0, 0], buff=0.2,
                        color=YELLOW, stroke_width=7, tip_length=0.25)
        self.at("leaves as carbon dioxide")
        self.play(GrowArrow(correct), handle.animate.move_to([2.4, 2.7, 0]), run_time=1.1)
        star = T("★", size=34, color=YELLOW).move_to(handle)
        self.at("labeled bicarbonate")
        self.play(FadeIn(star, scale=0.5), handle.animate.shift(UP * 0.45),
                  star.animate.shift(UP * 0.45), run_time=0.8)
        clean = chip("NO LABEL IN CHAIN", GREEN, size=28).move_to([-3.8, 2.05, 0])
        self.at("remains in palmitate")
        self.play(FadeIn(clean), Indicate(chain, color=GREEN, scale_factor=1.05),
                  FadeOut(VGroup(handle, star), shift=UP * 0.4), run_time=1.0)
        self.finish()


class S07Why(SpokenScene):
    def construct(self):
        floor_world(self)
        schematic = chip("SCHEMATIC ENERGY TRACK", GREY, size=28).move_to([0, 3.2, 0])
        # Piecewise linear track: the height is explanatory, not quantitative.
        track = VMobject(color=GREY, stroke_width=8).set_points_as_corners([
            [-5.8, -1.4, 0], [-2.7, -1.4, 0], [-0.6, 1.2, 0],
            [1.0, 1.2, 0], [3.0, -1.6, 0], [5.8, -1.6, 0],
        ])
        a = carbon_block("acetyl", width=1.55).move_to([-5.0, -0.85, 0])
        b = carbon_block("acetyl", width=1.55).move_to([-3.3, -0.85, 0])
        self.add(schematic, track, a, b)
        self.at("That loss is useful")
        self.play(Indicate(track, color=YELLOW), run_time=0.8)
        self.at("Joining two acetyl")
        self.play(a.animate.move_to([-5.0, 0.2, 0]),
                  b.animate.move_to([-3.3, 1.9, 0]), run_time=0.4)
        self.play(a.animate.move_to([-2.2, 0.2, 0]),
                  b.animate.move_to([-0.9, 1.9, 0]), run_time=0.6)
        self.at("is uphill")
        self.play(a.animate.move_to([-5.0, 0.2, 0]),
                  b.animate.move_to([-3.3, 1.9, 0]), run_time=0.45)
        self.play(a.animate.move_to([-5.0, -0.85, 0]),
                  b.animate.move_to([-3.3, -0.85, 0]), run_time=0.4)
        spr = spring(center=np.array([-0.4, -2.0, 0]), width=2.8)
        atp = coin().move_to([-2.7, 2.0, 0])
        loaded = carbon_block("malonyl", width=1.9).move_to([0.3, 1.95, 0])
        co = badge().scale(0.82).next_to(loaded, UP, buff=0.05)
        self.at("Releasing carbon dioxide")
        self.play(FadeIn(loaded), FadeIn(co), FadeIn(spr), run_time=0.8)
        self.at("strongly downhill")
        self.play(co.animate.move_to([2.7, 1.8, 0]), loaded.animate.move_to([3.3, -1.05, 0]), run_time=1.0)
        joined = carbon_block("new C–C bond", width=2.65).move_to([4.35, -1.0, 0])
        self.at("coupling the events")
        self.play(ReplacementTransform(VGroup(a, b, loaded), joined),
                  spr.animate.stretch(1.35, 0), run_time=1.05)
        self.at("bond forward")
        self.play(joined.animate.shift(RIGHT * 0.7), FadeOut(co, shift=UP * 0.3), run_time=0.75)
        self.at("spend a TP")
        self.play(FadeIn(atp), atp.animate.move_to(spr.get_left() + LEFT * 0.25), run_time=0.75)
        self.at("load this molecular spring")
        self.play(Transform(spr, spring(center=spr.get_center(), width=1.5)),
                  FadeOut(atp, scale=0.5), run_time=1.0)
        self.finish()


class S08Crdr(SpokenScene):
    def construct(self):
        group, path, stations = loop_world(self)
        cargo = RoundedRectangle(corner_radius=0.1, width=0.78, height=0.42,
                                 stroke_color=GREEN, stroke_width=3,
                                 fill_color=GREEN, fill_opacity=0.28).move_to(FAS_C + UP * TRAVEL_R)
        cap = Dot(radius=0.1, color=YELLOW).move_to(cargo.get_top() + DOWN * 0.05)
        chain_label = carbon_block("4C CHAIN", width=2.0).move_to([-3.75, 0.35, 0])
        carbonyl = chip("carbonyl", YELLOW, size=28).move_to([-3.75, 1.5, 0])
        self.add(cargo, cap, chain_label, carbonyl)
        self.at("Condensation leaves")
        self.play(Indicate(cargo, color=GREEN), Indicate(chain_label, color=GREEN), run_time=0.9)
        self.at("carbonyl")
        self.play(Indicate(carbonyl, color=YELLOW, scale_factor=1.12),
                  Indicate(cap, color=YELLOW, scale_factor=1.6), run_time=0.75)
        crdr = T("C   R   D   R", size=40, color=TEXT, weight=BOLD).move_to([-3.4, 2.6, 0])
        self.at("fatty acid synthase")
        self.remove(chain_label, carbonyl)
        self.play(FadeIn(crdr, shift=DOWN * 0.15), run_time=0.75)
        self.at("finishes CRDR")
        self.play(VGroup(cargo, cap).animate.move_to(FAS_C + RIGHT * TRAVEL_R), run_time=0.9)
        n1 = battery().move_to([-3.7, 0.8, 0])
        n2 = battery().move_to([-3.7, -0.4, 0])
        self.at("reduction", nth=0)
        self.play(FadeIn(n1), Indicate(stations[1], color=PURPLE), run_time=0.7)
        self.at("dehydration")
        self.play(VGroup(cargo, cap).animate.move_to(FAS_C + DOWN * TRAVEL_R),
                  FadeOut(n1, scale=0.5), run_time=0.8)
        self.at("reduction", nth=1)
        self.play(FadeIn(n2), VGroup(cargo, cap).animate.move_to(FAS_C + LEFT * TRAVEL_R),
                  Indicate(stations[3], color=PURPLE), run_time=0.8)
        electrons = VGroup(*[Dot(radius=0.1, color=PURPLE) for _ in range(4)]).arrange(RIGHT, buff=0.18)
        electrons.move_to([-3.7, -1.5, 0])
        self.at("four electrons")
        self.play(FadeIn(electrons), electrons.animate.move_to(cargo), FadeOut(n2, scale=0.5), run_time=0.9)
        saturated = chip("saturated segment", GREEN, size=28).move_to([-3.45, 0.25, 0])
        self.at("saturated segment")
        self.play(FadeIn(saturated), FadeOut(electrons), FadeOut(cap),
                  cargo.animate.move_to(FAS_C + UP * TRAVEL_R), run_time=1.0)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        group, path, stations = loop_world(self, show_acc=True)
        rule = T("ONE TURN", size=34, font=TITLE_FONT).move_to([0, 3.25, 0])
        primer = carbon_block("P", width=0.78).move_to(FAS_C + UP * TRAVEL_R)
        primer_label = carbon_block("primer", width=1.55).move_to([-1.0, 2.1, 0])
        extender = carbon_block("2C", width=1.25).move_to([-5.65, -0.85, 0])
        self.add(rule, primer, primer_label)
        self.at("Here is the rule")
        self.play(Indicate(rule, color=GOLD, scale_factor=1.08), run_time=0.75)
        self.at("After the primer")
        self.play(Indicate(primer_label, color=GREEN, scale_factor=1.1),
                  Indicate(primer, color=GREEN, scale_factor=1.1), run_time=0.75)
        self.at("each CRDR turn")
        self.play(FadeOut(primer_label), MoveAlongPath(primer, path), run_time=1.1, rate_func=linear)
        self.at("adds two carbons")
        self.play(FadeIn(extender), extender.animate.move_to([-1.0, 0.1, 0]), run_time=0.9)
        counter = label_box("+2 CARBONS", GREEN, width=2.65).move_to([-5.3, 2.35, 0])
        self.at("one malonyl")
        self.play(ReplacementTransform(extender, counter), Indicate(primer, color=GREEN), run_time=0.85)
        atp = coin().move_to([-5.5, 1.2, 0])
        n1 = battery().move_to([-1.2, -1.15, 0])
        n2 = battery().move_to([-1.2, -2.05, 0])
        self.at("costs one ATP")
        self.play(FadeIn(atp), Indicate(group[-1][2], color=TEAL), run_time=0.75)
        bill1 = label_box("−1 ATP", TEAL, width=1.8).move_to([-4.65, -1.85, 0])
        self.at("at a CC")
        self.play(ReplacementTransform(atp, bill1), run_time=0.65)
        self.at("two NADPH")
        self.play(FadeIn(n1), FadeIn(n2), Indicate(stations[1], color=PURPLE),
                  Indicate(stations[3], color=PURPLE), run_time=0.8)
        bill2 = label_box("−2 NADPH", PURPLE, width=2.35).move_to([-1.4, -1.9, 0])
        self.at("fatty acid synthase")
        self.play(ReplacementTransform(VGroup(n1, n2), bill2),
                  MoveAlongPath(primer, path), run_time=1.0, rate_func=linear)
        self.finish()


class S10Repeat(SpokenScene):
    def construct(self):
        group, path, stations = loop_world(self, show_acc=True)
        chain = carbon_block("4C", width=0.85).move_to(FAS_C + UP * TRAVEL_R)
        counter = M("4 C", size=44, color=GREEN).move_to([-3.8, 2.55, 0])
        atp_used = M("ATP used  1", size=29, color=TEAL).move_to([-3.8, -1.55, 0])
        nadph_used = M("NADPH used  2", size=29, color=PURPLE).move_to([-3.8, -2.05, 0])
        self.add(chain, counter, atp_used, nadph_used)
        self.at("chain returns")
        self.play(MoveAlongPath(chain, path), run_time=1.25, rate_func=linear)
        self.at("same machine repeats")
        counts = [6, 8, 10, 12, 14, 16]
        for i, count in enumerate(counts, start=2):
            mal = carbon_block("malonyl", width=1.55, size=28).move_to([-6.0, 0.05, 0])
            new_chain = carbon_block(f"{count}C", width=0.95).move_to(chain)
            new_count = M(f"{count} C", size=44, color=GREEN).move_to(counter)
            new_atp = M(f"ATP used  {i}", size=29, color=TEAL).move_to(atp_used)
            new_nad = M(f"NADPH used  {2*i}", size=29, color=PURPLE).move_to(nadph_used)
            self.play(FadeIn(mal, shift=RIGHT * 0.2), mal.animate.move_to([-1.0, 0.05, 0]),
                      MoveAlongPath(chain, path), run_time=0.46, rate_func=linear)
            self.play(FadeOut(mal, scale=0.4), Transform(chain, new_chain),
                      Transform(counter, new_count), Transform(atp_used, new_atp),
                      Transform(nadph_used, new_nad), run_time=0.38)
        self.at("Fatty acid synthase then releases")
        self.play(chain.animate.move_to([0, 3.3, 0]), run_time=0.9)
        pal = chip("PALMITATE", GREEN, size=34).move_to([0, 3.3, 0])
        self.at("palmitate")
        self.remove(chain)
        self.play(FadeIn(pal), run_time=0.8)
        self.at("saturated 16")
        self.play(Indicate(counter, color=GREEN, scale_factor=1.14),
                  pal.animate.set_fill(GREEN, opacity=0.28), run_time=0.9)
        self.finish()


class S11ScopeReturn(SpokenScene):
    def construct(self):
        group, path, stations = loop_world(self, show_acc=True)
        pal = chip("PALMITATE  ·  16C SATURATED", GREEN, size=31).move_to([0, 3.3, 0])
        stop = VGroup(RegularPolygon(n=8, radius=0.62, color=RED,
                                     fill_color=RED, fill_opacity=0.2),
                      T("STOP", size=28, color=RED, weight=BOLD)).move_to([5.45, 0.05, 0])
        stop[1].move_to(stop[0])
        self.add(pal)
        self.at("mostly stops there")
        self.play(FadeIn(stop, scale=0.7), pal.animate.shift(RIGHT * 0.25), run_time=0.85)
        longer = Arrow([3.9, 1.35, 0], [5.85, 1.35, 0], buff=0.05,
                       color=GREY, stroke_width=4, tip_length=0.2)
        double = Arrow([3.9, -1.1, 0], [5.85, -1.1, 0], buff=0.05,
                       color=GREY, stroke_width=4, tip_length=0.2)
        longer_l = T("longer later", size=28, color=TEXT).next_to(longer, UP, buff=0.12)
        double_l = T("double bonds later", size=28, color=TEXT).next_to(double, DOWN, buff=0.12)
        self.at("Longer chains")
        self.remove(stop)
        self.play(GrowArrow(longer), FadeIn(longer_l), run_time=0.8)
        self.at("double bonds")
        self.play(GrowArrow(double), FadeIn(double_l), run_time=0.8)
        frame = RoundedRectangle(corner_radius=0.3, width=12.3, height=6.45,
                                 stroke_opacity=0, fill_color=GOLD,
                                 fill_opacity=0.035).move_to([0, -0.05, 0])
        frame.set_z_index(-1)
        tag = chip("THIS FILM'S RULE", GOLD, size=28).move_to([-4.7, 2.75, 0])
        self.at("this film's rule")
        self.remove(longer, longer_l, double, double_l)
        self.play(Create(frame), FadeIn(tag), run_time=0.85)
        self.at("saturated chain")
        self.remove(tag)
        self.play(Indicate(pal, color=GREEN, scale_factor=1.08), run_time=0.8)
        input_block = carbon_block("acetyl CoA", width=2.15).move_to([-5.3, -2.0, 0])
        self.at("starts from acetyl")
        self.play(FadeIn(input_block, shift=RIGHT * 0.25), run_time=0.75)
        self.at("in the cytoplasm")
        cyt = T("cytoplasm", size=28, color=GREY).move_to([-5.3, -1.35, 0])
        marker = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.42,
                                  stroke_color=GREEN, stroke_width=3,
                                  fill_color=GREEN, fill_opacity=0.25).move_to([-5.2, -0.7, 0])
        self.play(FadeIn(cyt), ReplacementTransform(input_block, marker), run_time=0.8)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        group, path, stations = loop_world(self, show_acc=True)
        chain = carbon_block("C", width=0.78).move_to(FAS_C + UP * TRAVEL_R)
        additions = label_box("ADDITIONS  4", GREEN, width=2.8).move_to([-5.1, 2.65, 0])
        gains = label_box("CARBONS  +8", GREEN, width=2.7).move_to([-1.55, 3.2, 0])
        costs = VGroup(
            label_box("ATP  4", TEAL, width=2.15),
            label_box("NADPH  8", PURPLE, width=2.35),
        ).arrange(RIGHT, buff=0.2).move_to([-3.6, -2.2, 0])
        handle = badge().scale(0.78).move_to([-1.4, 1.5, 0])
        self.add(chain, additions, gains, costs, handle)
        self.at("discarded carbon")
        self.play(Indicate(handle, color=YELLOW), run_time=0.9)
        self.at("never a building block")
        hdot = Dot(radius=0.18, color=YELLOW).move_to(handle)
        self.play(ReplacementTransform(handle, hdot), run_time=0.3)
        self.play(hdot.animate.move_to([1.1, 2.45, 0]),
                  Indicate(chain, color=GREEN), run_time=0.5)
        temp = chip("TEMPORARY HANDLE", YELLOW, size=28).move_to([3.0, 3.2, 0])
        self.at("temporary handle")
        self.play(ReplacementTransform(hdot, temp), run_time=0.75)
        atp = coin().move_to([-5.65, 0.35, 0])
        self.at("bought with a TP")
        self.play(FadeIn(atp), Indicate(group[-1][2], color=TEAL), run_time=0.8)
        self.at("release drives")
        self.play(FadeOut(temp, shift=UP * 0.4), FadeOut(atp, scale=0.4),
                  MoveAlongPath(chain, path), run_time=1.0, rate_func=linear)
        # Three representative cycles: attach handle, release it, transfer electrons, +2.
        for idx, total in enumerate((5, 6, 7), start=1):
            h = Dot(radius=0.18, color=YELLOW).move_to([-1.2, 1.3, 0])
            electrons = VGroup(*[Dot(radius=0.08, color=PURPLE) for _ in range(4)])
            electrons.arrange(RIGHT, buff=0.1).move_to([-1.25, -1.15, 0])
            self.play(FadeIn(h), FadeIn(electrons), h.animate.move_to([1.0, 1.6, 0]), run_time=0.48)
            new_add = label_box(f"ADDITIONS  {total}", GREEN, width=2.8).move_to(additions)
            new_gain = label_box(f"CARBONS  +{total*2}", GREEN, width=2.7).move_to(gains)
            new_costs = VGroup(
                label_box(f"ATP  {total}", TEAL, width=2.15),
                label_box(f"NADPH  {total*2}", PURPLE, width=2.35),
            ).arrange(RIGHT, buff=0.2).move_to(costs)
            self.play(h.animate.shift(UP * 1.3), electrons.animate.move_to(chain), FadeOut(electrons),
                      MoveAlongPath(chain, path), Transform(additions, new_add),
                      Transform(gains, new_gain), Transform(costs, new_costs),
                      run_time=0.72, rate_func=linear)
            self.remove(h)
        self.at("Count the malonyl additions")
        self.play(Indicate(additions, color=GREEN, scale_factor=1.1), run_time=0.75)
        self.at("two carbon gains")
        self.play(Indicate(gains, color=GREEN, scale_factor=1.1), run_time=0.75)
        self.at("their cost")
        self.play(Indicate(costs, color=GOLD, scale_factor=1.06), run_time=0.85)
        self.finish()


class S13End(EndCard):
    LINE = "Each two-carbon addition costs one ATP and two NADPH."

    def construct(self):
        floor_world(self, dim=0.34)
        line = T(self.LINE, size=43, font=TITLE_FONT)
        fit(line, max_w=11.7)
        line.move_to([0, 1.0, 0])
        block = carbon_block("+2C", width=1.45).move_to([-5.4, -1.15, 0])
        rule = Line([-5.8, 0.25, 0], [5.8, 0.25, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(line, shift=UP * 0.15), Create(rule), run_time=0.8)
        self.play(FadeIn(block), block.animate.move_to([5.25, -1.15, 0]), run_time=2.15, rate_func=linear)
        self.finish()
