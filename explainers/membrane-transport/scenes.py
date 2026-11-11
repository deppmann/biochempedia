"""Two Pushes, One Hill — membrane transport explainer.

COLOR MAP
  ORANGE  potassium, concentration, and outward concentration push
  TEAL    membrane voltage and inward electrical push
  GREEN   equilibrium / zero net flow
  BLUE    transport proteins
  YELLOW  glucose / coupled uphill cargo
  GREY    membrane and secondary structure

The energy ramps use the lesson values: concentration = +8.59 kJ/mol for
outside -> inside K+, and electrical energy = 0.096485 * Vm kJ/mol.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
POTASSIUM = ORANGE
SODIUM = "#B9C1CC"
RX = 5.45


def arr(a, b, color=TEXT, width=8, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip)


def fluid_background():
    """The same outside/inside landscape behind close-ups and energy diagrams."""
    outside = Rectangle(width=13.2, height=3.8, stroke_width=0,
                        fill_color=BLUE, fill_opacity=0.13).move_to([0, 2.0, 0])
    inside = Rectangle(width=13.2, height=3.8, stroke_width=0,
                       fill_color=GOLD, fill_opacity=0.12).move_to([0, -2.0, 0])
    return VGroup(outside, inside).set_z_index(-5)


def ion(label="K+", color=POTASSIUM, r=0.19, size=18):
    disk = Circle(radius=r, color=color, stroke_width=2.5,
                  fill_color=color, fill_opacity=0.95)
    txt = T(label, size=size, color=BG, weight=BOLD).move_to(disk)
    return VGroup(disk, txt)


def drifting_ions(points, label="K+", color=POTASSIUM, r=0.17):
    """Deterministic, gentle ambient motion; stable placement from scene to scene."""
    group = VGroup()
    for i, point in enumerate(points):
        m = ion(label, color, r=r, size=15).move_to(point)
        m.phase = 0.61 * i
        m.anchor = np.array(point, dtype=float)

        def drift(dot, dt, i=i):
            dot.phase += dt
            dot.move_to(dot.anchor + np.array([
                0.045 * math.sin(1.3 * dot.phase + i),
                0.035 * math.cos(1.0 * dot.phase + 0.7 * i), 0]))
        m.add_updater(drift)
        group.add(m)
    return group


OUT_POINTS = [(-5.2, 2.25, 0), (-2.8, 2.65, 0), (2.7, 2.35, 0), (4.0, 2.75, 0)]
IN_POINTS = [(-5.45, -1.65, 0), (-4.55, -2.6, 0), (-3.45, -1.95, 0),
             (-2.4, -2.8, 0), (-1.35, -1.65, 0), (-0.2, -2.55, 0),
             (0.9, -1.75, 0), (2.0, -2.8, 0), (3.1, -1.75, 0),
             (4.25, -2.55, 0), (5.2, -1.75, 0)]


def membrane_world(channel_x=0, labels=True, ruler_on=True, open_gate=True):
    """The carried world: fields, membrane, channel, ions, and optional Vm ruler."""
    outside = Rectangle(width=13.2, height=3.15, stroke_width=0,
                        fill_color=BLUE, fill_opacity=0.07).move_to([0, 2.25, 0])
    inside = Rectangle(width=13.2, height=3.2, stroke_width=0,
                       fill_color=GOLD, fill_opacity=0.07).move_to([0, -2.2, 0])
    gap = 0.72
    left = RoundedRectangle(corner_radius=0.1, width=6.6 + channel_x - gap,
                            height=0.78, color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.42).move_to([(-6.6 + channel_x-gap)/2, 0, 0])
    right = RoundedRectangle(corner_radius=0.1, width=6.6 - channel_x - gap,
                             height=0.78, color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.42).move_to([(6.6 + channel_x+gap)/2, 0, 0])
    gates = VGroup(*[
        RoundedRectangle(corner_radius=0.14, width=0.34, height=1.24,
                         color=BLUE, stroke_width=3, fill_color=BLUE,
                         fill_opacity=0.7).move_to([channel_x + s * 0.52, 0, 0])
        for s in (-1, 1)])
    plug = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.6,
                            stroke_width=0, fill_color=GREY,
                            fill_opacity=0.9).move_to([channel_x, 0, 0])
    if open_gate:
        plug.set_opacity(0)
    outs = drifting_ions(OUT_POINTS)
    ins = drifting_ions(IN_POINTS)
    parts = VGroup(outside, inside, left, right, gates, plug, outs, ins)
    parts.outside, parts.inside = outside, inside
    parts.membrane = VGroup(left, right)
    parts.gates, parts.plug, parts.outs, parts.ins = gates, plug, outs, ins
    if labels:
        lo = T("OUTSIDE   5 mM K+", 30, ORANGE, weight=BOLD).move_to([-4.55, 3.25, 0])
        li = T("INSIDE   140 mM K+", 30, ORANGE, weight=BOLD).move_to([-4.35, -3.25, 0])
        parts.add(lo, li)
        parts.labels = VGroup(lo, li)
    if ruler_on:
        parts.add(voltage_ruler())
    return parts


def vy(v, top=2.75, bottom=-2.75):
    return top + (v / -120.0) * (bottom - top)


def voltage_ruler(x=RX, big=False):
    top, bot = (3.0, -3.0) if big else (2.75, -2.75)
    line = Line([x, top, 0], [x, bot, 0], color=GREY, stroke_width=4)
    ticks = VGroup()
    for v in (0, -20, -40, -60, -80, -100, -120):
        yy = top + (v / -120) * (bot - top)
        ticks.add(Line([x - 0.14, yy, 0], [x + 0.14, yy, 0], color=GREY, stroke_width=3))
    vm = T("Vm", 28, TEAL, weight=BOLD).next_to(line, UP, buff=0.14)
    z = M("0", 24, GREY).next_to(line.get_top(), LEFT, buff=0.18)
    n = M("-120 mV", 24, GREY).next_to(line.get_bottom(), LEFT, buff=0.18)
    return VGroup(line, ticks, vm, z, n)


def pointer(v, x=RX, text=None, side=RIGHT, color=TEAL):
    y = vy(v)
    tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.13).rotate(-PI/2)
    tri.move_to([x - 0.3, y, 0])
    label = M(text or f"{v:g}", 25, color).next_to(tri, side, buff=0.18)
    return VGroup(tri, label)


def equilibrium_mark(x=RX):
    y = vy(-89.1)
    line = Line([x - 0.27, y, 0], [x + 0.27, y, 0], color=GREEN, stroke_width=8)
    label = M("E_K = -89.1 mV", 28, GREEN).move_to([3.62, y + 0.34, 0])
    return VGroup(line, label)


def ramp(delta, center=(-2.3, 0.2, 0), width=4.0, color=TEXT, label=None):
    """Energy-to-enter ramp. delta is computed kJ/mol, with + meaning uphill."""
    cx, cy, _ = center
    dy = np.clip(delta / 8.59 * 2.0, -2.25, 2.25)
    line = Line([cx - width/2, cy - dy/2, 0], [cx + width/2, cy + dy/2, 0],
                color=color, stroke_width=8)
    left = T("OUT", 24, GREY).next_to(line.get_start(), DOWN, buff=0.15)
    right = T("IN", 24, GREY).next_to(line.get_end(), DOWN, buff=0.15)
    g = VGroup(line, left, right)
    if label:
        lab = T(label, 28, color, weight=BOLD).next_to(line, UP, buff=0.22)
        g.add(lab)
    g.line = line
    return g


def ball_on(line, at=0.5, color=POTASSIUM):
    return ion("K+", color, r=0.22, size=17).move_to(line.point_from_proportion(at) + UP * 0.26)


def flow(scene, world, direction="out", run_time=1.1, count=3):
    source = world.ins if direction == "out" else world.outs
    chosen = list(source[:count])
    for m in chosen:
        m.clear_updaters()
    mid_y, end_y = (0.0, 2.2) if direction == "out" else (0.0, -2.2)
    scene.play(*[m.animate.move_to([(-0.2 + 0.2*i), mid_y, 0]) for i, m in enumerate(chosen)],
               run_time=run_time * 0.45)
    scene.play(*[m.animate.move_to([(-0.45 + 0.45*i), end_y + 0.18*(i%2), 0]) for i, m in enumerate(chosen)],
               run_time=run_time * 0.55)


class S00Hook(SpokenScene):
    def construct(self):
        w = membrane_world(open_gate=False)
        q = T("?", 78, TEXT, weight=BOLD).move_to([0, 1.05, 0])
        badge = chip("28x", ORANGE, 34).move_to([-3.9, -1.25, 0])
        p = pointer(-70, text="-70", side=LEFT)
        self.play(FadeIn(w), FadeIn(q, scale=0.7), FadeIn(badge, scale=0.8), run_time=1.1)
        self.at("against a 28")
        self.play(Indicate(badge, color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.at("Take a cell")
        self.play(Indicate(w.labels, color=ORANGE, scale_factor=1.03), run_time=1.0)
        self.at("minus 70")
        self.play(FadeIn(p), FadeOut(w.plug), w.gates.animate.set_fill(BLUE, opacity=0.95),
                  FadeOut(q), run_time=0.9)
        self.at("Potassium leaves")
        flow(self, w, "out", 1.25, 3)
        self.at("minus 100")
        p2 = pointer(-100, text="-100", side=LEFT)
        self.play(ReplacementTransform(p, p2), run_time=0.7)
        self.at("potassium comes in")
        flow(self, w, "in", 1.25, 3)
        self.play(Indicate(badge, color=ORANGE, scale_factor=1.16), run_time=0.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Transport Across Membranes"
    TITLE = "Two Pushes, One Hill"


class S02Pushes(SpokenScene):
    def construct(self):
        w = membrane_world(ruler_on=False)
        self.play(FadeIn(w), run_time=0.8)
        self.at("first is concentration")
        crowd = SurroundingRectangle(w.ins, color=ORANGE, buff=0.16, corner_radius=0.2)
        self.play(Create(crowd), run_time=0.45)
        ca = arr([0, -0.8, 0], [0, 1.75, 0], ORANGE, 11, 0.32)
        self.play(GrowArrow(ca), run_time=0.7)
        self.at("where it is crowded")
        cl = T("concentration push", 30, ORANGE, weight=BOLD).move_to([-2.0, 1.25, 0])
        self.play(FadeIn(cl), Indicate(w.ins, color=ORANGE), run_time=0.9)
        self.at("second is voltage")
        plus = VGroup(*[T("+", 28, TEAL).move_to([x, 0.75, 0]) for x in (-3.6, -2.3, -1.0, 1.0, 2.3, 3.6)])
        minus = VGroup(*[T("-", 32, TEAL).move_to([x, -0.75, 0]) for x in (-3.6, -2.3, -1.0, 1.0, 2.3, 3.6)])
        self.play(FadeOut(crowd), LaggedStart(*[FadeIn(s) for s in VGroup(plus, minus)], lag_ratio=0.06), run_time=0.9)
        va = arr([0.55, 0.8, 0], [0.55, -1.8, 0], TEAL, 11, 0.32)
        self.play(GrowArrow(va), run_time=0.6)
        self.at("inside minus the outside")
        vl = T("voltage push", 30, TEAL, weight=BOLD).move_to([2.0, -1.15, 0])
        self.play(FadeIn(vl), run_time=0.5)
        self.at("pulls positive ions in")
        movers = list(w.outs[:2])
        for m in movers: m.clear_updaters()
        self.play(*[m.animate.shift(DOWN * 1.3 + RIGHT * (0.2*i)) for i, m in enumerate(movers)], run_time=1.2)
        self.finish()


class S03Hill(SpokenScene):
    def construct(self):
        bg = fluid_background()
        title = T("energy to enter  •  schematic", 28, GREY).to_edge(UP, buff=0.38)
        orange = ramp(8.59, center=(-2.25, 0.2, 0), color=ORANGE, label="concentration slope")
        teal = ramp(-6.75, center=(2.25, 0.2, 0), color=TEAL, label="voltage slope")
        final_center = orange.line.get_center()
        final_ball_pos = orange.line.point_from_proportion(0.25) + UP*0.26
        orange.line.rotate(-0.32, about_point=final_center)
        b1 = ball_on(orange.line, 0.05)
        # The energy subject is already visible while the opening sentence lands.
        # A slow roll keeps that spoken lead-in from becoming a static empty panel.
        self.add(bg, title, orange.line, b1)
        self.play(Rotate(orange.line, 0.32, about_point=final_center),
                  b1.animate.move_to(final_ball_pos),
                  run_time=4.7, rate_func=linear)
        self.at("hill with two slopes")
        self.play(FadeIn(orange[1:]), run_time=0.9)
        self.at("entering uphill")
        self.play(Indicate(orange.line, color=ORANGE, scale_factor=1.08),
                  b1.animate.move_to(orange.line.point_from_proportion(0.02)+UP*0.26), run_time=0.9)
        self.at("voltage slope")
        self.play(Create(teal.line), FadeIn(teal[1:]), run_time=0.9)
        self.at("makes it downhill")
        b2 = ball_on(teal.line, 0.2)
        self.play(FadeIn(b2), b2.animate.move_to(teal.line.point_from_proportion(0.78)+UP*0.26), run_time=0.9)
        self.at("the total")
        total = ramp(8.59-6.75, center=(0, -0.25, 0), width=5.3, color=TEXT, label="total at -70 mV")
        ball = ball_on(total.line, 0.65)
        self.play(FadeOut(VGroup(orange, teal, b1, b2)), FadeIn(total), FadeIn(ball), run_time=0.8)
        self.at("runs downhill")
        self.play(ball.animate.move_to(total.line.point_from_proportion(0.06)+UP*0.26), run_time=1.2)
        self.finish()


class S04Balance(SpokenScene):
    def construct(self):
        bg = fluid_background()
        title = T("energy to enter K+  •  computed", 28, GREY).to_edge(UP, buff=0.35)
        rl = voltage_ruler()
        voltage = ValueTracker(-70)
        total_line = always_redraw(lambda: ramp(8.59 + 0.096485*voltage.get_value(),
                                                  center=(-2.15, 0.25, 0), width=4.5,
                                                  color=TEXT, label="total")[0])
        orange = ramp(8.59, center=(-2.15, 0.25, 0), width=4.5, color=ORANGE)
        teal_line = always_redraw(lambda: ramp(0.096485*voltage.get_value(),
                                               center=(-2.15, 0.25, 0), width=4.5,
                                               color=TEAL)[0])
        voltage_wedge = always_redraw(lambda: Polygon(
            [-4.4, 0.25, 0], [0.1, 0.25, 0],
            [0.1, 0.25 + np.clip((0.096485*voltage.get_value()) / 8.59 * 2.0, -2.25, 2.25)/2, 0],
            [-4.4, 0.25 - np.clip((0.096485*voltage.get_value()) / 8.59 * 2.0, -2.25, 2.25)/2, 0],
            stroke_width=0, fill_color=TEAL, fill_opacity=0.12).set_z_index(-1))
        ptr = always_redraw(lambda: pointer(voltage.get_value(), text=f"{voltage.get_value():.1f}", side=LEFT))
        ball = ion("K+", POTASSIUM, 0.22, 17).move_to([-2.15, 0.55, 0])
        # Start on the complete, full-opacity panel: the narration begins immediately,
        # so fading this dense diagram up left an almost empty spoken frame.
        self.add(bg, title, rl, orange, voltage_wedge, teal_line, total_line, ptr, ball)
        # Show the two slopes approaching balance before naming the cancellation.
        self.play(voltage.animate.set_value(-84), run_time=2.4, rate_func=linear)
        self.at("slopes cancel")
        self.play(voltage.animate.set_value(-89.1), ball.animate.move_to([-2.15, 0.52, 0]), run_time=0.8)
        self.remove(ptr)
        ek = equilibrium_mark()
        self.play(FadeIn(ek, shift=LEFT*0.2), run_time=0.5)
        self.at("equilibrium potential")
        self.play(Indicate(ek, color=GREEN), run_time=0.9)
        self.at("For potassium")
        k_values = chip("K+ teaching values", ORANGE, 32).move_to([2.0, -2.25, 0])
        self.play(FadeIn(k_values, shift=LEFT*0.5), run_time=0.8)
        self.at("teaching values")
        conc_chip = chip("+8.59 kJ/mol", ORANGE, 30).move_to([-3.7, -2.15, 0])
        volt_chip = chip("-8.59 kJ/mol", TEAL, 30).move_to([1.35, -2.15, 0])
        self.play(ReplacementTransform(k_values, VGroup(conc_chip, volt_chip)), run_time=0.9)
        self.play(Indicate(conc_chip, color=ORANGE),
                  Indicate(volt_chip, color=TEAL), run_time=1.1)
        self.at("Nernst equation")
        balance_band = Rectangle(width=9.1, height=0.38, stroke_width=0,
                                 fill_color=GREEN, fill_opacity=0.14).move_to([0.75, vy(-89.1), 0])
        self.play(GrowFromEdge(balance_band, RIGHT), run_time=1.2)
        calc = VGroup(M("concentration  +8.59", 27, ORANGE),
                      M("voltage        -8.59", 27, TEAL),
                      M("total            0", 29, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.2, -2.1, 0])
        self.play(LaggedStart(*[FadeIn(row, shift=UP*0.1) for row in calc], lag_ratio=0.32),
                  FadeOut(balance_band), FadeOut(VGroup(conc_chip, volt_chip)), run_time=2.2)
        self.at("ions still cross")
        cross_band = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.58, color=GREY,
                                      stroke_width=2.5, fill_color=GREY, fill_opacity=0.42).move_to([2.25, 0.0, 0])
        cross_gate = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.25, height=0.94,
                                              color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to([2.25+s*0.4, 0, 0])
                              for s in (-1, 1)])
        up = VGroup(*[ion("K+", POTASSIUM, 0.23, 16).move_to([1.75+0.85*i, -1.2, 0]) for i in range(2)])
        down = VGroup(*[ion("K+", POTASSIUM, 0.23, 16).move_to([1.75+0.85*i, 1.2, 0]) for i in range(2)])
        self.play(FadeIn(cross_band), FadeIn(cross_gate), FadeIn(up), FadeIn(down), run_time=0.5)
        self.play(*[m.animate.shift(UP*2.4) for m in up],
                  *[m.animate.shift(DOWN*2.4) for m in down], run_time=1.4)
        self.at("equal numbers")
        counts = VGroup(M("12 out  •  12 in", 30, GREEN),
                        T("net 0", 30, GREEN, weight=BOLD)).arrange(DOWN, buff=0.16).move_to([2.3, 2.25, 0])
        self.play(FadeIn(counts), run_time=0.6)
        self.play(*[m.animate.shift(DOWN*2.4) for m in up],
                  *[m.animate.shift(UP*2.4) for m in down], run_time=1.4)
        self.finish()


def question_layout():
    w = membrane_world(labels=False, open_gate=True)
    w.ruler_on = True
    card = T("Which way at each voltage?", 40, TEXT, weight=BOLD).to_edge(UP, buff=0.28)
    ek = equilibrium_mark()
    p70 = pointer(-70, text="-70   ?", side=LEFT)
    p100 = pointer(-100, text="-100   ?", side=LEFT)
    return VGroup(w, card, ek, p70, p100)


class S05Predict(SpokenScene):
    def construct(self):
        q = question_layout()
        self.play(FadeIn(q[0]), run_time=0.7)
        self.at("green mark")
        self.play(FadeIn(q[2]), Indicate(q[2], color=GREEN), run_time=0.8)
        self.at("minus 70")
        self.play(FadeIn(q[1]), FadeIn(q[3]), run_time=0.7)
        self.at("minus 100")
        self.play(FadeIn(q[4]), run_time=0.6)
        self.at("Decide before")
        self.play(Indicate(q[3], color=TEAL), Indicate(q[4], color=TEAL), run_time=1.2)
        self.finish()


class S06Think(Scene):
    def construct(self):
        q = question_layout()
        self.add(q)
        self.play(Indicate(q[3], color=TEAL), Indicate(q[4], color=TEAL), run_time=1.3)
        self.wait(1.4)
        self.play(Indicate(q[3], color=TEAL), Indicate(q[4], color=TEAL), run_time=1.3)
        self.wait(0.5)


class S07Compare(SpokenScene):
    def construct(self):
        w = membrane_world(labels=False, ruler_on=False)
        rl = voltage_ruler()
        ek = equilibrium_mark()
        p70 = pointer(-70, text="-70", side=LEFT)
        self.add(w, rl, ek)
        self.at("Minus 70")
        self.play(FadeIn(p70), run_time=0.55)
        r70 = ramp(8.59-6.75, center=(-2.15, 1.05, 0), width=3.4, color=TEXT, label="uphill to enter")
        b = ball_on(r70.line, 0.65)
        self.at("shallower than")
        r70[-1].move_to([-2.15, 3.3, 0]).set_opacity(1)
        self.play(FadeIn(r70), FadeIn(b), run_time=0.7)
        self.at("potassium leaves")
        self.play(b.animate.move_to(r70.line.point_from_proportion(0.05)+UP*0.26), run_time=0.75)
        flow(self, w, "out", 1.0, 2)
        outlab = T("K+ OUT", 34, ORANGE, weight=BOLD).move_to([-2.2, -1.05, 0])
        self.play(FadeIn(outlab), run_time=0.35)
        self.at("Minus 100")
        p100 = pointer(-100, text="-100", side=LEFT)
        self.play(FadeOut(VGroup(r70, b, outlab)), ReplacementTransform(p70, p100), run_time=0.65)
        r100 = ramp(8.59-9.65, center=(-2.15, 1.05, 0), width=3.4, color=TEXT, label="downhill to enter")
        r100[-1].move_to([-2.15, 3.3, 0]).set_opacity(1)
        b2 = ball_on(r100.line, 0.1)
        self.play(FadeIn(r100), FadeIn(b2), run_time=0.55)
        self.at("potassium comes in")
        self.play(b2.animate.move_to(r100.line.point_from_proportion(0.92)+UP*0.26), run_time=0.7)
        flow(self, w, "in", 1.0, 2)
        inlab = T("K+ IN", 34, TEAL, weight=BOLD).move_to([-2.2, -1.05, 0])
        self.play(FadeIn(inlab), run_time=0.35)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        channel = membrane_world(channel_x=-3.6, labels=False, ruler_on=False)
        bar_x = 1.5
        bar = Line([bar_x, 2.65, 0], [bar_x, -2.65, 0], color=GREY, stroke_width=8)
        mark = Line([bar_x-0.45, 0, 0], [bar_x+0.45, 0, 0], color=GREEN, stroke_width=10)
        ex = T("E_X  (this ion)", 29, GREEN, weight=BOLD).next_to(mark, RIGHT, buff=0.2)
        self.play(FadeIn(channel), run_time=0.6)
        self.at("equilibrium potential")
        self.play(Create(bar), GrowFromCenter(mark), FadeIn(ex), run_time=0.8)
        pluschip = chip("X+", ORANGE, 34).move_to([-4.4, 3.2, 0])
        self.at("positive ion")
        self.play(FadeIn(pluschip), run_time=0.4)
        self.at("above the mark")
        top = Rectangle(width=2.0, height=2.55, stroke_width=0, fill_color=ORANGE, fill_opacity=0.13).move_to([bar_x, 1.3, 0])
        ao = arr([bar_x, 0.35, 0], [bar_x, 2.05, 0], ORANGE, 10, 0.3)
        lo = T("net out", 30, ORANGE, weight=BOLD).next_to(ao, LEFT, buff=0.25)
        self.play(FadeIn(top), GrowArrow(ao), FadeIn(lo), run_time=0.9)
        self.at("Below the mark")
        bottom = Rectangle(width=2.0, height=2.55, stroke_width=0, fill_color=TEAL, fill_opacity=0.13).move_to([bar_x, -1.3, 0])
        ai = arr([bar_x, -0.35, 0], [bar_x, -2.05, 0], TEAL, 10, 0.3)
        li = T("net in", 30, TEAL, weight=BOLD).next_to(ai, LEFT, buff=0.25)
        self.play(FadeIn(bottom), GrowArrow(ai), FadeIn(li), run_time=0.9)
        self.at("negative ion")
        minus = chip("X-", BLUE, 34).move_to(pluschip)
        ao_flip = arr([bar_x, 2.05, 0], [bar_x, 0.35, 0], ORANGE, 10, 0.3)
        ai_flip = arr([bar_x, -2.05, 0], [bar_x, -0.35, 0], TEAL, 10, 0.3)
        self.play(ReplacementTransform(pluschip, minus), FadeOut(VGroup(ao, ai, lo, li)),
                  FadeIn(VGroup(ao_flip, ai_flip)), run_time=1.0)
        flip = T("anion: directions flip", 30, BLUE, weight=BOLD).move_to([3.15, -3.15, 0])
        self.play(FadeIn(flip), run_time=0.45)
        self.finish()


def mini_world(x, voltage, direction):
    band = RoundedRectangle(corner_radius=0.1, width=5.7, height=0.62, color=GREY,
                            stroke_width=2.5, fill_color=GREY, fill_opacity=0.4).move_to([x, 0, 0])
    hole = Rectangle(width=1.05, height=0.8, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, 0, 0])
    gate = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.28, height=1.05, color=BLUE,
                                    fill_color=BLUE, fill_opacity=0.75).move_to([x+s*0.43, 0, 0]) for s in (-1,1)])
    dots = drifting_ions([(x+dx, y, 0) for dx,y in [(-1.8,-1.7),(-0.8,-2.3),(0.9,-1.6),(1.8,-2.3),(-1.4,1.8),(1.3,2.2)]], r=0.17)
    lab = M(f"{voltage} mV", 30, TEAL).move_to([x, 3.0, 0])
    arrow = arr([x, -0.65 if direction=='out' else 0.65, 0], [x, 1.35 if direction=='out' else -1.35, 0], ORANGE if direction=='out' else TEAL, 10, 0.3)
    return VGroup(band, hole, gate, dots, lab, arrow)


class S09Path(SpokenScene):
    def construct(self):
        bg = fluid_background()
        left = mini_world(-3.25, -70, "out")
        right = mini_world(3.25, -100, "in")
        self.play(FadeIn(bg), FadeIn(left), FadeIn(right), run_time=0.9)
        self.at("same thing")
        self.play(Indicate(left[2], color=BLUE), Indicate(right[2], color=BLUE), run_time=1.0)
        self.at("opened a path")
        self.play(GrowArrow(left[-1]), GrowArrow(right[-1]), run_time=0.8)
        # The identical open paths keep carrying K+ in opposite directions.
        ldot, rdot = left[3][0], right[3][-1]
        ldot.clear_updaters(); rdot.clear_updaters()
        self.play(ldot.animate.move_to([-3.25, 1.45, 0]),
                  rdot.animate.move_to([3.25, -1.45, 0]), run_time=1.4)
        self.at("which ion")
        na = ion("Na+", SODIUM, 0.24, 16).move_to([-3.25, 1.2, 0])
        self.play(FadeIn(na), na.animate.move_to([-3.8, 1.65, 0]), run_time=0.7, rate_func=there_and_back)
        self.at("slopes chose")
        r1 = ramp(1.84, center=(-3.25, 1.2, 0), width=2.1, color=TEXT)
        r2 = ramp(-1.06, center=(3.25, 1.2, 0), width=2.1, color=TEXT)
        self.play(FadeOut(na), FadeIn(r1), FadeIn(r2), run_time=0.8)
        self.at("never decide")
        self.play(Indicate(left[2], color=BLUE), Indicate(right[2], color=BLUE), run_time=1.0)
        self.finish()


def transporter(x, name, color=BLUE):
    block = RoundedRectangle(corner_radius=0.18, width=2.25, height=1.28, color=color,
                             stroke_width=3, fill_color=color, fill_opacity=0.22).move_to([x, 0, 0])
    label = T(name, 27, color, weight=BOLD).move_to(block)
    return VGroup(block, label)


class S10Couple(SpokenScene):
    def construct(self):
        bg = fluid_background()
        sides = VGroup(T("OUTSIDE", 28, GREY).move_to([-5.55, 3.25, 0]),
                       T("INSIDE", 28, GREY).move_to([-5.65, -3.25, 0]))
        band = RoundedRectangle(corner_radius=0.12, width=13.0, height=0.85, color=GREY,
                                stroke_width=3, fill_color=GREY, fill_opacity=0.38)
        pump = transporter(-3.4, "Na+/K+ pump")
        sglt = transporter(3.4, "SGLT1")
        self.play(FadeIn(bg), FadeIn(sides), FadeIn(band), run_time=0.5)
        uphill = arr([0, -2.15, 0], [0, 2.15, 0], YELLOW, 9, 0.3)
        uphill_q = T("uphill?", 32, YELLOW, weight=BOLD).move_to([1.25, 2.25, 0])
        self.play(GrowArrow(uphill), FadeIn(uphill_q), run_time=1.8)
        self.at("couples that trip")
        self.play(FadeOut(VGroup(uphill, uphill_q)), FadeIn(pump), FadeIn(sglt), run_time=0.8)
        self.play(Indicate(pump, color=BLUE), run_time=1.35)
        self.play(Indicate(sglt, color=BLUE), run_time=1.35)
        self.at("splits ATP")
        atp = chip("ATP", GREEN, 30).move_to([-5.2, -1.4, 0])
        split = chip("ATP split", GREEN, 28).move_to([-5.2, 2.6, 0])
        self.play(FadeIn(atp), atp.animate.move_to([-4.2, -0.8, 0]), run_time=0.65)
        self.play(ReplacementTransform(atp, split), run_time=0.55)
        self.at("three sodium out")
        nas = VGroup(*[ion("Na+", SODIUM, 0.22, 15).move_to([-4.15+0.72*i, -1.75, 0]) for i in range(3)])
        self.play(FadeIn(nas), run_time=0.3)
        self.play(*[m.animate.shift(UP*3.25) for m in nas], run_time=0.9)
        self.at("two potassium in")
        ks = VGroup(*[ion("K+", POTASSIUM, 0.22, 15).move_to([-3.75+0.72*i, 1.75, 0]) for i in range(2)])
        self.play(FadeIn(ks), *[m.animate.shift(DOWN*3.25) for m in ks], run_time=0.95)
        self.at("two sodium run downhill")
        self.play(FadeOut(VGroup(split, nas, ks)), run_time=0.35)
        nas2 = VGroup(*[ion("Na+", SODIUM, 0.24, 16).move_to([3.05+0.75*i, 2.2, 0]) for i in range(2)])
        tealr = ramp(-4.8, center=(3.4, 1.75, 0), width=2.5, color=TEAL)
        self.play(FadeIn(tealr), FadeIn(nas2), run_time=0.45)
        self.play(*[m.animate.shift(DOWN*4.25) for m in nas2], run_time=1.0)
        self.at("glucose to climb")
        glucose = chip("glucose", YELLOW, 27).move_to([4.65, -2.15, 0])
        yellowr = ramp(2.2, center=(4.55, -1.35, 0), width=2.1, color=YELLOW)
        self.play(FadeIn(yellowr), FadeIn(glucose), run_time=0.4)
        self.play(glucose.animate.move_to([3.75, 1.35, 0]), run_time=1.05)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        bg = fluid_background()
        sides = VGroup(T("OUTSIDE", 28, GREY).move_to([-5.55, 3.25, 0]),
                       T("INSIDE", 28, GREY).move_to([-5.65, -3.25, 0]))
        band = RoundedRectangle(corner_radius=0.12, width=13.0, height=0.72, color=GREY,
                                stroke_width=3, fill_color=GREY, fill_opacity=0.38)
        channel = transporter(-4.1, "K+ channel")
        pump = transporter(0, "Na+/K+ pump")
        sglt = transporter(4.1, "SGLT1")
        transports = VGroup(channel, pump, sglt)
        self.play(FadeIn(bg), FadeIn(sides), FadeIn(band), FadeIn(transports), run_time=0.8)
        self.at("same hill")
        ramps = VGroup(ramp(-1.06, center=(-4.1, 2.05, 0), width=2.4, color=TEXT),
                       ramp(-2.3, center=(0, 2.05, 0), width=2.4, color=TEXT),
                       ramp(-1.7, center=(4.1, 2.05, 0), width=2.4, color=TEXT))
        schematic = T("total energy  •  schematic", 28, GREY).to_edge(UP, buff=0.28)
        self.play(FadeIn(schematic), LaggedStart(*[FadeIn(r) for r in ramps], lag_ratio=0.18), run_time=1.1)
        ambient_balls = VGroup(*[ball_on(r.line, 0.08) for r in ramps])
        self.play(LaggedStart(*[FadeIn(b) for b in ambient_balls], lag_ratio=0.15), run_time=0.6)
        self.play(*[b.animate.move_to(r.line.point_from_proportion(0.45)+UP*0.24)
                    for b,r in zip(ambient_balls, ramps)], run_time=1.2)
        self.at("only opens the way")
        self.play(Indicate(channel, color=BLUE), run_time=0.8)
        self.at("slopes of everything")
        balls = ambient_balls
        self.play(*[b.animate.move_to(r.line.point_from_proportion(0.62)+UP*0.24)
                    for b,r in zip(balls, ramps)], run_time=0.7)
        self.at("total must run downhill")
        self.play(*[b.animate.move_to(r.line.point_from_proportion(0.92)+UP*0.24) for b,r in zip(balls, ramps)], run_time=1.35)
        self.finish()


class S12End(EndCard):
    LINE = "The total must run downhill."
