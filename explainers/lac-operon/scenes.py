"""The lac operon: two inputs produce high expression.

The cell, DNA rail, regulators, and expression meter are rebuilt by shared
builders so carried pictures never drift between scenes.  All geometry is
schematic; no molecular structures are shown.
"""
from types import SimpleNamespace

from bp_parts import *  # noqa: F401,F403


# One colour per concept, following this film's script.
GLUCOSE = BLUE
LACTOSE = YELLOW
GENE = GREEN
OPERATOR = ORANGE = "#F29E4C"
POLYMERASE = TEXT
REPRESSOR = RED
ACTIVATOR = TEAL

RAIL_Y = -1.25
GX = (0.2, 1.9, 3.6)


def sugar(text, color, at, size=28):
    return boxed_label(text, color=color, size=size, pad=0.18).move_to(at)


def membrane(width=12.0, y=2.35, gate_x=3.4, gate_color=LACTOSE):
    """Cell membrane with a single labelled-cartoon gate-sized gap."""
    left = Line([-width / 2, y, 0], [gate_x - 0.55, y, 0], color=GREY, stroke_width=8)
    right = Line([gate_x + 0.55, y, 0], [width / 2, y, 0], color=GREY, stroke_width=8)
    gate = RoundedRectangle(corner_radius=0.14, width=0.85, height=0.7,
                            stroke_color=gate_color, stroke_width=4,
                            fill_color=gate_color, fill_opacity=0.25).move_to([gate_x, y, 0])
    return VGroup(left, right, gate)


def expression_meter(value=0.08, center=(4.8, 0.6, 0), label="lac expression"):
    level = ValueTracker(value)
    gauge = dial(level, center=center, radius=1.25, label=label, color=GENE,
                 fmt="{:.0f}%", scale=100, size=34)
    return gauge, level


def cell_shell():
    body = RoundedRectangle(corner_radius=1.0, width=12.2, height=5.8,
                            stroke_color=TEXT, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.12).move_to([0, -0.05, 0])
    # Breathing the outline is visible but does not distract from the teaching action.
    pulse(body, base=4.0, amp=1.0, speed=1.3)
    bob(body, amp=0.045, speed=0.9)
    return body


def compact_rail(y=RAIL_Y, include_genes=True):
    """The carried DNA picture used inside the cell."""
    prom = boxed_label("promoter", GREY, 26, pad=0.14).move_to([-3.35, y, 0])
    op = boxed_label("operator", OPERATOR, 26, pad=0.14).move_to([-1.45, y, 0])
    genes = VGroup()
    if include_genes:
        genes = VGroup(*[boxed_label(name, GENE, 28, box=(1.45, 0.72), pad=0.13)
                         .move_to([x, y, 0]) for name, x in zip(("lacZ", "lacY", "lacA"), GX)])
        genes[2].shift(UP * 0.08)
    blocks = [prom, op, *genes]
    endpoints = [(-4.75, blocks[0].get_left()[0] - 0.08)]
    endpoints += [(a.get_right()[0] + 0.08, b.get_left()[0] - 0.08)
                  for a, b in zip(blocks, blocks[1:])]
    endpoints += [(blocks[-1].get_right()[0] + 0.08, 4.25)]
    line = VGroup(*[Line([a, y, 0], [b, y, 0], color=GREY, stroke_width=7)
                    for a, b in endpoints if b > a])
    return SimpleNamespace(group=VGroup(line, prom, op, genes), line=line,
                           promoter=prom, operator=op, genes=genes)


def repressor(at=(-1.45, -0.25, 0), open_state=False, label=True):
    """A red two-jaw clamp.  Open jaws are rotated away from the operator."""
    x, y, _ = at
    left = RoundedRectangle(corner_radius=0.15, width=0.48, height=1.35,
                            stroke_color=REPRESSOR, stroke_width=4,
                            fill_color=REPRESSOR, fill_opacity=0.32).move_to([x - 0.3, y, 0])
    right = left.copy().move_to([x + 0.3, y, 0])
    if open_state:
        left.rotate(0.38, about_point=[x - 0.3, y - 0.55, 0])
        right.rotate(-0.38, about_point=[x + 0.3, y - 0.55, 0])
    jaws = VGroup(left, right)
    lab = T("repressor", 28, REPRESSOR).next_to(jaws, UP, buff=0.14) if label else VGroup()
    return SimpleNamespace(group=VGroup(jaws, lab), jaws=jaws, label=lab,
                           left=left, right=right)


def polymerase(at=(-3.9, 0.35, 0), label=True):
    body = RoundedRectangle(corner_radius=0.28, width=1.15, height=0.72,
                            stroke_color=POLYMERASE, stroke_width=4,
                            fill_color=POLYMERASE, fill_opacity=0.15).move_to(at)
    lab = T("polymerase", 28, POLYMERASE).next_to(body, UP, buff=0.14) if label else VGroup()
    return SimpleNamespace(group=VGroup(body, lab), body=body, label=lab)


def cap_unit(at=(-4.0, 0.25, 0), with_badge=True):
    cap = boxed_label("CAP", ACTIVATOR, 28, box=(1.25, 0.72)).move_to(at)
    badge = boxed_label("cyclic AMP", ACTIVATOR, 24, pad=0.12)
    badge.next_to(cap, UP, buff=0.13)
    return SimpleNamespace(group=VGroup(cap, badge) if with_badge else VGroup(cap),
                           cap=cap, badge=badge)


def hook_world(meter_value=0.08, question=True):
    """The full cell used by the hook, title, prediction, and reveal."""
    shell = cell_shell()
    rail = compact_rail(y=-1.25)
    gauge, level = expression_meter(meter_value, center=(4.65, 0.55, 0))
    glu = sugar("glucose", GLUCOSE, [-3.55, 1.35, 0])
    lac = sugar("lactose", LACTOSE, [0.0, 1.35, 0])
    q = T("?", 56, LACTOSE, weight=BOLD).next_to(lac, RIGHT, buff=0.3) if question else VGroup()
    return SimpleNamespace(group=VGroup(shell, rail.group, gauge, glu, lac, q), shell=shell,
                           rail=rail, gauge=gauge, level=level, glucose=glu, lactose=lac, question=q)


def prediction_backdrop(meter_value=0.42, with_labels=False):
    """Same compact cell state for predict, pause, and reveal."""
    world = hook_world(meter_value=meter_value, question=False)
    rep = repressor(at=(-1.45, -0.18, 0), open_state=True, label=False)
    cap = cap_unit(at=(-4.0, 0.25, 0), with_badge=False)
    blocker = boxed_label("transport", GLUCOSE, 24, pad=0.12).move_to([1.95, 1.45, 0])
    permease = boxed_label("permease", LACTOSE, 24, pad=0.12).move_to([1.95, 0.65, 0])
    extras = VGroup(rep.group, cap.group, blocker, permease)
    if with_labels:
        classic = boxed_label("classic account", ACTIVATOR, 24, pad=0.12).move_to([-4.45, 2.25, 0])
        exclusion = boxed_label("inducer exclusion", GLUCOSE, 24, pad=0.12).move_to([2.7, 2.25, 0])
        extras.add(classic, exclusion)
    bob(world.glucose, amp=0.05, speed=1.0)
    bob(world.lactose, amp=0.05, speed=1.2, seed=2)
    group = VGroup(world.group, extras)
    group.world = world
    group.extras = extras
    return group


def high_state():
    """The enlarged, stable high-expression cell used by the last two spoken scenes."""
    shell = cell_shell()
    rail = compact_rail(y=-1.25)
    rep = repressor(at=(0.4, 1.25, 0), open_state=True, label=False)
    allo = boxed_label("allolactose", LACTOSE, 24, pad=0.12).next_to(rep.jaws, RIGHT, buff=0.2)
    cap = cap_unit(at=(-4.0, 0.28, 0), with_badge=True)
    poly = polymerase(at=(-2.6, 0.25, 0), label=False)
    link = Line(cap.cap.get_right(), poly.body.get_left(), color=ACTIVATOR, stroke_width=7)
    gauge, level = expression_meter(0.9, center=(4.65, 0.65, 0))
    return SimpleNamespace(group=VGroup(shell, rail.group, rep.group, allo, cap.group, link, poly.group, gauge),
                           shell=shell, rail=rail, rep=rep, allo=allo, cap=cap, poly=poly,
                           link=link, gauge=gauge, level=level)


class S01Hook(SpokenScene):
    def construct(self):
        world = hook_world()
        # Show the whole question before naming its parts.
        self.play(FadeIn(world.shell), FadeIn(world.rail.group), run_time=0.8)
        self.play(FadeIn(world.glucose, shift=DOWN * 0.15),
                  FadeIn(world.lactose, shift=DOWN * 0.15), run_time=0.7)
        self.at("glucose and lactose")
        self.play(world.glucose.animate.shift(DOWN * 0.45),
                  world.lactose.animate.shift(DOWN * 0.1), run_time=0.9)
        self.at("postpone")
        self.play(FadeIn(world.gauge), FadeIn(world.question, scale=0.7), run_time=0.7)
        self.play(world.glucose.animate.shift(LEFT * 1.0).set_opacity(0.35),
                  Wiggle(world.lactose, scale_value=1.04), run_time=1.0)
        self.at("Follow one promoter")
        self.play(Indicate(world.rail.promoter, color=TEXT), run_time=0.8)
        self.at("Two signals")
        arrows = VGroup(Arrow(world.glucose.get_bottom(), world.rail.promoter.get_top(), buff=0.15,
                              color=GLUCOSE, stroke_width=5),
                        Arrow(world.lactose.get_bottom(), world.rail.operator.get_top(), buff=0.15,
                              color=LACTOSE, stroke_width=5))
        self.play(GrowArrow(arrows[0]), run_time=0.5)
        self.play(GrowArrow(arrows[1]), run_time=0.5)
        self.at("output becomes high")
        self.play(Indicate(world.gauge, color=GENE, scale_factor=1.04), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        world = hook_world()
        bob(world.glucose, amp=0.04, speed=1.1)
        bob(world.lactose, amp=0.04, speed=1.3, seed=2)
        self.add(world.group, scope_tag("schematic"))
        title = fit_text("When Are the lac Genes High?", max_w=10.0, size=50,
                         font=TITLE_FONT, color=TEXT).move_to([0, 2.35, 0])
        self.play(Write(title), run_time=0.7)
        self.wait(0.7)
        self.play(FadeOut(title), run_time=0.5)
        self.finish()


class S03Operon(SpokenScene):
    def construct(self):
        shell = cell_shell()
        rail = compact_rail(y=-0.55)
        self.add(shell)
        self.play(Create(rail.line), run_time=0.7)
        self.at("lacC")  # the aligned audio's near-match for spoken lac Z
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in rail.genes], lag_ratio=0.25), run_time=1.2)
        self.at("one promoter")
        self.play(FadeIn(rail.promoter, shift=UP * 0.15), run_time=0.6)
        poly = polymerase(at=(-4.15, 0.42, 0))
        rna = Line([-2.65, -1.55, 0], [-2.55, -1.55, 0], color=GENE, stroke_width=8)
        self.at("Polymerase")
        self.play(FadeIn(poly.group), run_time=0.6)
        self.at("copy them")
        self.play(poly.group.animate.shift(RIGHT * 7.1),
                  rna.animate.put_start_and_end_on([-2.65, -1.55, 0], [3.55, -1.55, 0]),
                  run_time=2.2, rate_func=linear)
        mrna_label = T("one messenger RNA", 30, GENE).next_to(rna, DOWN, buff=0.2)
        self.at("Together")
        self.play(FadeIn(mrna_label), LaggedStart(*[Indicate(g, color=GENE, scale_factor=1.04)
                                                   for g in rail.genes], lag_ratio=0.2), run_time=1.4)
        self.at("three coding regions")
        self.play(LaggedStart(*[Indicate(g, color=GENE, scale_factor=1.04)
                                for g in rail.genes], lag_ratio=0.2), run_time=0.8)
        self.at("red repressor")
        self.play(FadeOut(VGroup(poly.group, rna, mrna_label)), FadeIn(rail.operator), run_time=0.6)
        rep = repressor(at=(-1.45, 0.55, 0))
        self.play(FadeIn(rep.group, shift=UP * 0.2), run_time=0.7)
        poly2 = polymerase(at=(-3.55, 0.42, 0), label=False)
        self.at("operator")
        self.play(FadeIn(poly2.group), Indicate(rail.operator, color=OPERATOR), run_time=0.6)
        self.at("blocks transcription")
        self.play(poly2.group.animate.shift(RIGHT * 1.0), run_time=0.5)
        self.play(poly2.group.animate.shift(LEFT * 0.35), Wiggle(rep.jaws), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Inducer(SpokenScene):
    def construct(self):
        shell = cell_shell()
        rail = compact_rail(y=-1.2)
        mem = membrane(y=2.45, gate_x=3.5)
        rep = repressor(at=(-1.45, -0.05, 0), label=False)
        poly = polymerase(at=(-3.55, -0.22, 0), label=False)
        self.add(shell, rail.group, rep.group, poly.group)
        self.play(FadeIn(mem), run_time=0.6)
        lac = sugar("lactose", LACTOSE, [3.5, 3.15, 0], 26)
        self.at("Yellow lactose")
        self.play(FadeIn(lac), run_time=0.4)
        self.play(lac.animate.move_to([3.5, 1.55, 0]), run_time=1.1)
        gate_lab = T("permease", 28, LACTOSE).move_to([3.5, 3.1, 0])
        self.at("permease")
        self.play(FadeIn(gate_lab), Indicate(mem[2], color=LACTOSE), run_time=0.6)
        enzyme = boxed_label("β-galactosidase", GENE, 28, pad=0.18).move_to([0.2, 1.55, 0])
        self.at("Beta")
        self.play(FadeIn(enzyme, shift=RIGHT * 0.2), run_time=0.6)
        self.at("turns a little lactose")
        self.play(lac.animate.next_to(enzyme, RIGHT, buff=0.85), run_time=0.7)
        allo = boxed_label("allolactose", LACTOSE, 28, pad=0.18).move_to(lac.get_center())
        self.at("allolactose")
        self.play(Transform(lac, allo), run_time=0.8)
        natural = T("natural inducer", 28, LACTOSE).next_to(lac, DOWN, buff=0.32)
        self.at("natural inducer")
        self.play(FadeIn(natural), run_time=0.5)
        self.at("Lactose itself")
        old = T("lactose", 30, LACTOSE).move_to([1.5, 0.1, 0])
        new = T("conversion matters", 30, TEXT).move_to([1.5, 0.1, 0])
        self.play(FadeIn(old), run_time=0.4)
        self.at("Conversion matters")
        self.play(swap(old, new), run_time=0.7)
        self.at("Allolactose reshapes")
        self.play(FadeOut(VGroup(natural, enzyme, new, gate_lab)), run_time=0.3)
        self.play(lac.animate.move_to([-1.45, 0.95, 0]), run_time=0.6)
        self.play(rep.left.animate.rotate(0.38, about_point=[-1.55, -0.6, 0]),
                  rep.right.animate.rotate(-0.38, about_point=[-0.95, -0.6, 0]), run_time=0.9)
        self.at("lowers its affinity")
        self.play(VGroup(rep.group, lac).animate.shift(UP * 0.65 + RIGHT * 1.2), run_time=0.9)
        rna = Line([-2.65, -2.0, 0], [-2.55, -2.0, 0], color=GENE, stroke_width=8)
        self.at("polymerase can move")
        self.play(poly.group.animate.shift(RIGHT * 6.7),
                  rna.animate.put_start_and_end_on([-2.65, -2.0, 0], [3.55, -2.0, 0]),
                  run_time=1.8, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


class S05Leak(SpokenScene):
    def construct(self):
        shell = cell_shell()
        field = Circle(radius=3.15, stroke_width=0, fill_color=GENE, fill_opacity=0.10)
        loop = Arc(radius=2.8, start_angle=0.25, angle=TAU - 0.5,
                   color=GENE, stroke_width=7)
        tip = Triangle(color=GENE, fill_color=GENE, fill_opacity=1).scale(0.16).rotate(-0.3)
        tip.move_to(loop.get_end())
        gate = boxed_label("permease", LACTOSE, 28).move_to([0, 1.75, 0])
        enzyme = boxed_label("β-galactosidase", GENE, 28).move_to([1.55, -0.15, 0])
        signal = boxed_label("allolactose", LACTOSE, 28).move_to([0, -1.75, 0])
        genes = boxed_label("lac genes", GENE, 28).move_to([-1.55, -0.15, 0])
        self.add(shell)
        self.play(FadeIn(field), Create(loop), FadeIn(tip), run_time=0.8)
        self.at("This creates a loop")
        self.play(LaggedStart(*[FadeIn(x) for x in (gate, enzyme, signal, genes)], lag_ratio=0.2), run_time=1.3)
        self.at("help produce the signal")
        self.play(Indicate(gate, color=LACTOSE), Indicate(enzyme, color=GENE), run_time=0.8)
        self.play(Indicate(signal, color=LACTOSE), run_time=0.6)
        self.at("increases their own production")
        self.play(Indicate(genes, color=GENE), Rotate(tip, angle=TAU, about_point=ORIGIN), run_time=1.4)
        self.at("amplify a small beginning")
        meter, level = expression_meter(0.08, center=(4.85, 0.35, 0), label="expression")
        self.play(FadeOut(VGroup(field, loop, tip, signal, gate, enzyme, genes)), run_time=0.35)
        gate.move_to([-4.45, 1.05, 0])
        enzyme.move_to([-4.45, 0.0, 0])
        genes.move_to([-4.45, -1.05, 0])
        self.play(FadeIn(VGroup(gate, enzyme, genes)), FadeIn(meter), run_time=0.6)
        self.play(level.animate.set_value(0.7), run_time=2.4, rate_func=smooth)
        tiny = VGroup(boxed_label("permease", LACTOSE, 24, pad=0.1),
                      boxed_label("β-gal", GENE, 24, pad=0.1)).arrange(DOWN, buff=0.25).move_to([-2.35, 1.45, 0])
        self.at("Basal leak")
        self.play(FadeIn(tiny), run_time=0.6)
        leak_lab = T("basal leak", 30, TEXT).move_to([-0.2, 1.45, 0])
        self.play(FadeIn(leak_lab), level.animate.set_value(0.12), run_time=0.8)
        self.at("not perfectly binary")
        band = Line([3.45, 0.35, 0], [4.2, 0.35, 0], color=GENE, stroke_width=12)
        self.play(Create(band), Indicate(meter, color=GENE), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Activator(SpokenScene):
    def construct(self):
        shell = cell_shell()
        rail = compact_rail(y=-1.25)
        rep = repressor(at=(0.6, 1.25, 0), open_state=True, label=False)
        poly = polymerase(at=(-2.65, 0.18, 0), label=False)
        meter, level = expression_meter(0.22, center=(4.65, 0.65, 0))
        self.add(shell, rail.group, rep.group, poly.group, meter)
        self.at("Removing the brake")
        self.play(Indicate(rep.jaws, color=REPRESSOR), run_time=0.7)
        self.play(level.animate.set_value(0.24), run_time=2.2, rate_func=linear)
        self.at("weak by itself")
        self.play(poly.group.animate.shift(RIGHT * 0.55), run_time=0.45)
        self.play(poly.group.animate.shift(LEFT * 0.55), level.animate.set_value(0.26), run_time=0.55)
        cap = cap_unit(at=(-4.55, 1.65, 0), with_badge=True)
        self.at("TLCAP")  # transcript's joined rendering of “teal C A P”
        self.play(FadeIn(cap.cap, shift=DOWN * 0.15), run_time=0.6)
        self.at("cyclic AMP")
        self.play(FadeIn(cap.badge), run_time=0.5)
        self.at("docks upstream")
        self.play(cap.group.animate.move_to([-4.35, 0.65, 0]), run_time=0.9)
        link = Line(cap.cap.get_right(), poly.body.get_left(), color=ACTIVATOR, stroke_width=8)
        self.at("contacts polymerase")
        self.play(Create(link), Indicate(poly.body, color=ACTIVATOR), run_time=0.7)
        rna = Line([-2.65, -1.7, 0], [-2.55, -1.7, 0], color=GENE, stroke_width=9)
        self.at("helps transcription start")
        self.play(poly.group.animate.shift(RIGHT * 6.2),
                  rna.animate.put_start_and_end_on([-2.65, -1.7, 0], [3.55, -1.7, 0]),
                  level.animate.set_value(0.88), run_time=2.2, rate_func=linear)
        brake = boxed_label("repressor: brake", REPRESSOR, 28).move_to([-2.5, 2.35, 0])
        boost = boxed_label("CAP: activator", ACTIVATOR, 28).move_to([1.4, 2.35, 0])
        self.at("does not remove repressor")
        self.play(FadeIn(brake), FadeIn(boost), run_time=0.8)
        self.at("different job")
        self.play(Indicate(brake, color=REPRESSOR), Indicate(boost, color=ACTIVATOR), run_time=0.8)
        positive = T("positive control", 34, ACTIVATOR).move_to([0, -2.5, 0])
        self.at("positive control")
        self.play(FadeIn(positive), run_time=0.6)
        self.add(scope_tag("schematic"))
        self.finish()


class S07Glucose(SpokenScene):
    def construct(self):
        panels = TwoPanel("classic account", "inducer exclusion",
                          colors=(ACTIVATOR, GLUCOSE), top=2.85, bottom=-2.45, size=30)
        panels.left_frame.set_fill(ACTIVATOR, opacity=0.12)
        panels.right_frame.set_fill(GLUCOSE, opacity=0.12)
        pulse(panels.left_frame, base=2.5, amp=0.8, speed=1.2)
        pulse(panels.right_frame, base=2.5, amp=0.8, speed=1.4)
        bob(panels.left_frame, amp=0.045, speed=0.85)
        bob(panels.right_frame, amp=0.045, speed=1.0, seed=2)
        self.play(FadeIn(panels), run_time=0.7)
        # Left: glucose plentiful -> cyclic AMP sparse -> CAP docks less often.
        gleft = VGroup(*[Dot(radius=0.16, color=GLUCOSE) for _ in range(6)]).arrange(RIGHT, buff=0.22)
        cap = boxed_label("CAP", ACTIVATOR, 28)
        camps = VGroup(*[boxed_label("cAMP", ACTIVATOR, 24, pad=0.1) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        left = VGroup(gleft, camps, cap).arrange(DOWN, buff=0.55)
        panels.put(left, "left")
        # Right: a transport-system block narrows permease and slows lactose.
        perm = boxed_label("permease", LACTOSE, 28)
        transport = boxed_label("transport protein", GLUCOSE, 26)
        lact = VGroup(*[boxed_label("lactose", LACTOSE, 24, pad=0.1) for _ in range(3)]).arrange(DOWN, buff=0.18)
        right = VGroup(transport, perm, lact).arrange(DOWN, buff=0.35)
        panels.put(right, "right")
        self.at("Glucose changes both inputs")
        self.play(FadeIn(gleft), FadeIn(transport), run_time=0.7)
        self.play(gleft.animate.shift(DOWN * 0.35), run_time=1.5, rate_func=smooth)
        self.at("classic account")
        self.play(FadeIn(camps), run_time=0.6)
        self.at("lower when glucose")
        self.play(FadeOut(camps[1:]), cap.animate.set_opacity(0.45), run_time=0.8)
        self.at("debated")
        debated = T("importance in living cells is debated", 24, TEXT).move_to([-3.25, -1.9, 0])
        self.play(FadeIn(debated), run_time=0.6)
        self.at("transport protein")
        self.play(FadeIn(perm), FadeIn(lact), run_time=0.5)
        self.play(transport.animate.next_to(perm, UP, buff=0.05), run_time=0.8)
        self.at("Less lactose enters")
        self.play(lact.animate.set_opacity(0.3).shift(UP * 0.25), run_time=0.8)
        allo = boxed_label("allolactose", LACTOSE, 24, pad=0.1).move_to([4.75, -1.2, 0])
        self.at("less allolactose")
        self.play(FadeOut(lact), run_time=0.3)
        self.play(FadeIn(allo), allo.animate.set_opacity(0.3), run_time=0.5)
        clamp = repressor(at=(2.15, -1.25, 0), open_state=False, label=False)
        self.at("repressor")
        self.play(FadeIn(clamp.group), Wiggle(clamp.jaws), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Predict(SpokenScene):
    QUESTION = "Will lac expression reach high, or stop below it?"
    OPTIONS = ("high", "below high")

    def construct(self):
        back = prediction_backdrop(meter_value=0.42)
        self.play(FadeIn(back), run_time=0.8)
        self.at("Lactose is present")
        self.play(Indicate(back[0][4], color=LACTOSE), run_time=0.6)
        self.at("glucose is also plentiful")
        self.play(Indicate(back[0][3], color=GLUCOSE), run_time=0.7)
        q = question_card(self.QUESTION, self.OPTIONS, y=-3.35, size=28, chip_size=24)
        self.at("Will the expression meter")
        self.play(FadeIn(q.chips), run_time=0.5)
        self.play(FadeIn(q.question), run_time=0.5)
        self.at("Hold both signals")
        self.play(Wiggle(back[0][3], scale_value=1.03), Wiggle(back[0][4], scale_value=1.03), run_time=0.9)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = S08Predict.QUESTION
    OPTIONS = S08Predict.OPTIONS
    SECONDS = 4.5
    CARD = {"y": -3.35, "size": 28, "chip_size": 24}

    def backdrop(self):
        return prediction_backdrop(meter_value=0.42)


class S10Reveal(SpokenScene):
    def construct(self):
        back = prediction_backdrop(meter_value=0.42, with_labels=True)
        self.add(back)
        meter, level = back.world.gauge, back.world.level
        reduced = boxed_label("reduced", GENE, 32).move_to([4.65, -2.0, 0])
        self.at("output is reduced")
        self.play(level.animate.set_value(0.45), FadeIn(reduced), run_time=1.0)
        self.at("not high")
        high = T("not high  •  not absent", 28, REPRESSOR).move_to([-0.2, -2.5, 0])
        absent = VGroup()
        self.play(FadeIn(high), FadeIn(absent), run_time=0.8)
        self.at("Some inducer")
        rep = repressor(at=(-1.45, -0.18, 0), open_state=True, label=False)
        self.play(Indicate(rep.jaws, color=REPRESSOR), run_time=0.7)
        self.at("activation is weaker")
        poly = polymerase(at=(-3.1, 0.2, 0), label=False)
        self.play(FadeIn(poly.group), poly.group.animate.shift(RIGHT * 2.1), run_time=1.0)
        self.at("lactose entry is inhibited")
        self.play(Indicate(back.extras[3], color=GLUCOSE), run_time=0.7)
        self.at("two controls combine")
        self.play(Indicate(reduced, color=GENE), level.animate.set_value(0.48), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Cases(SpokenScene):
    def construct(self):
        shell = cell_shell()
        col_heads = VGroup(T("lactose absent", 28, LACTOSE), T("lactose present", 28, LACTOSE))
        col_heads[0].move_to([-2.1, 2.45, 0]); col_heads[1].move_to([3.25, 2.45, 0])
        row_heads = VGroup(T("scarce", 28, GLUCOSE), T("plentiful", 28, GLUCOSE))
        row_heads[0].rotate(PI / 2).move_to([-5.45, 1.0, 0])
        row_heads[1].rotate(PI / 2).move_to([-5.45, -1.65, 0])
        centers = [(-2.1, 1.0), (3.25, 1.0), (-2.1, -1.65), (3.25, -1.65)]
        outcomes = (("very low", 0.08), ("high", 0.9), ("very low", 0.08), ("reduced", 0.45))
        cells = VGroup()
        fills = VGroup()
        for (x, y), (word, amount) in zip(centers, outcomes):
            box = RoundedRectangle(corner_radius=0.18, width=4.75, height=2.25,
                                   stroke_color=GREY, stroke_width=2.5,
                                   fill_color=GENE, fill_opacity=0.10).move_to([x, y, 0])
            pulse(box, base=2.5, amp=0.7, speed=1.0 + 0.15 * len(cells))
            label = T(word, 32, GENE if word != "very low" else TEXT, weight=BOLD).move_to([x, y + 0.35, 0])
            track = Line([x - 1.65, y - 0.45, 0], [x + 1.65, y - 0.45, 0], color=GREY,
                         stroke_width=14, stroke_opacity=0.35)
            fill = Line([x - 1.65, y - 0.45, 0], [x - 1.65 + 3.3 * amount, y - 0.45, 0],
                        color=GENE, stroke_width=14)
            cells.add(VGroup(box, label, track)); fills.add(fill)
        self.add(shell)
        self.play(FadeIn(col_heads), FadeIn(row_heads), FadeIn(cells), run_time=1.0)
        self.at("Without lactose")
        self.play(Create(fills[0]), Create(fills[2]), run_time=0.9)
        self.at("very low")
        self.play(Indicate(cells[0][1]), Indicate(cells[2][1]), run_time=0.7)
        self.at("With both sugars")
        self.play(Create(fills[3]), run_time=0.7)
        self.at("reduced")
        self.play(Indicate(cells[3][1], color=GENE), run_time=0.6)
        self.at("Only lactose with scarce glucose")
        self.play(Create(fills[1]), run_time=0.9)
        self.at("strong activation together")
        self.play(Indicate(cells[1], color=GENE, scale_factor=1.03), run_time=0.8)
        self.at("This table predicts")
        note = caption("expression levels — not identical behaviour in every cell", size=26, y=-3.35)
        self.play(FadeIn(note), run_time=0.6)
        self.at("not whether every cell")
        high = high_state()
        self.play(FadeOut(VGroup(shell, col_heads, row_heads, cells, fills, note)), run_time=0.5)
        self.play(FadeIn(high.group), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        high = high_state()
        self.add(high.group)
        lactose = boxed_label("lactose present", LACTOSE, 28).move_to([-2.25, 2.35, 0])
        scarce = boxed_label("glucose scarce", GLUCOSE, 28).move_to([1.65, 2.35, 0])
        self.at("two conditions")
        self.play(FadeIn(lactose), run_time=0.5)
        self.play(FadeIn(scarce), run_time=0.5)
        together = Line(lactose.get_right() + RIGHT * 0.08,
                        scarce.get_left() + LEFT * 0.08, color=GENE, stroke_width=6)
        self.play(Create(together), Indicate(high.gauge, color=GENE), run_time=0.8)
        self.at("not naming a preferred food")
        food = T("preferred food?", 28, GREY).move_to([0, -2.6, 0])
        strike = Line(food.get_left(), food.get_right(), color=REPRESSOR, stroke_width=5)
        strike.layout_ok = "covered"
        self.play(FadeIn(food), Create(strike), run_time=0.7)
        self.at("Keep the scope clear")
        self.play(FadeOut(VGroup(food, strike)), FadeIn(scope_tag("standard model")), run_time=0.6)
        scope = fit_text("wild-type E. coli", max_w=4.5, size=30, color=TEXT).move_to([0, -2.55, 0])
        self.at("wild type E")
        self.play(FadeIn(scope), run_time=0.7)
        synthetic = boxed_label("synthetic inducer", LACTOSE, 28).move_to([-2.25, 2.35, 0])
        self.at("synthetic inducer")
        self.play(FadeOut(together), run_time=0.2)
        self.play(swap(lactose, synthetic), run_time=0.8)
        self.at("stand in for lactose")
        self.play(Indicate(synthetic, color=LACTOSE), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "In wild-type E. coli, high lac expression requires lactose and scarce glucose."
