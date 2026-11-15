"""How One Photon Becomes a Cellular Signal.

COLOR MAP: input = GOLD; active relay = BLUE; cGMP / diffusible messenger = TEAL;
open channels = GREEN; shutoff = RED; structure / inactive targets = GREY.
Biological drawings are explicitly schematic.  Numerical gain examples are the invented
examples in the lesson script; the response trace is a dimensionless computed schematic.
"""
from bp_parts import *


# --------------------------------------------------------------------------- carried rod world
def response_value(x, dip=0.0):
    """Dimensionless schematic dark-current trace with a smooth computed dip."""
    return -dip * np.exp(-((x - 0.64) / 0.12) ** 2)


def response_trace(dip=0.0, color=TEXT):
    xs = np.linspace(-5.7, 4.8, 180)
    pts = [np.array([x, -2.82 + 0.48 * response_value((x + 5.7) / 10.5, dip), 0]) for x in xs]
    line = VMobject(stroke_color=color, stroke_width=5, fill_opacity=0)
    line.set_points_as_corners(pts)
    return line


def gate(x, open_=True):
    """One schematic membrane gate; no molecular structure is implied."""
    col = GREEN if open_ else GREY
    left = Line([x - 0.22, -1.55, 0], [x - 0.22, -0.95, 0], color=col, stroke_width=9)
    right = Line([x + 0.22, -1.55, 0], [x + 0.22, -0.95, 0], color=col, stroke_width=9)
    if not open_:
        left.rotate(-0.55, about_point=left.get_bottom())
        right.rotate(0.55, about_point=right.get_bottom())
    return VGroup(left, right)


def rod_world(dip=0.0, active=False, closed=0, include_photon=False, trace_label=True):
    """The carried rod picture, rebuilt at identical coordinates in every rod scene."""
    shell = RoundedRectangle(width=12.0, height=5.05, corner_radius=0.45,
                             stroke_color=GREY, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.11).move_to([-.25, .25, 0])
    membrane = Line([-5.9, -1.55, 0], [5.4, -1.55, 0], color=GREY, stroke_width=7)
    rod_label = T("rod outer segment", 28, GREY).move_to([-3.9, 2.34, 0])
    receptor = boxed_label("rhodopsin", BLUE if active else GREY, size=28,
                           box=(2.05, 0.62), fill_opacity=0.22).move_to([-4.35, 1.25, 0])
    channels = VGroup(*[gate(x, i >= closed) for i, x in enumerate([-1.8, 0.2, 2.2])])
    cgmp = VGroup(*[Dot([x, -.55 + .08 * (i % 2), 0], radius=.11, color=TEAL)
                    for i, x in enumerate([-2.05, -1.55, -.05, .45, 1.95, 2.45]) if i // 2 >= closed])
    ions = VGroup(*[Dot([x, -1.95 - .16 * (i % 2), 0], radius=.075, color=TEXT)
                   for i, x in enumerate([-2.0, -1.6, 0.0, .4, 2.0, 2.4]) if i // 2 >= closed])
    trace = response_trace(dip)
    trace_lab = T("current · schematic", 24, GREY).move_to([-4.5, -3.28, 0]) if trace_label else VGroup()
    world = VGroup(shell, membrane, rod_label, receptor, channels, cgmp, ions, trace, trace_lab)
    world.shell, world.membrane, world.receptor = shell, membrane, receptor
    world.channels, world.cgmp, world.ions, world.trace, world.trace_lab = channels, cgmp, ions, trace, trace_lab
    world.dip = dip
    if include_photon:
        photon = Dot([-5.65, 1.25, 0], radius=.16, color=GOLD)
        photon.add(Annulus(inner_radius=.22, outer_radius=.25, color=GOLD).move_to(photon))
        world.add(photon)
        world.photon = photon
    return world


def animate_rod_idle(world):
    if len(world.cgmp):
        bob(world.cgmp, amp=.045, speed=1.5, seed=2)
    if len(world.ions):
        bob(world.ions, amp=.06, speed=2.0, seed=4)
    pulse(world.trace, base=5, amp=.7, speed=2.2)
    # A chain of dim carriers makes the schematic current visibly crawl even during narration holds.
    flow = VGroup(*[Dot([x, -2.82, 0], radius=.055, color=TEXT).set_opacity(.55)
                    for x in np.linspace(-5.6, 4.6, 11)])
    def drift(group, dt):
        for d in group:
            x = d.get_x() + .55 * dt
            if x > 4.8:
                x -= 10.5
            u = (x + 5.7) / 10.5
            d.move_to([x, -2.82 + .48 * response_value(u, world.dip), 0])
    flow.add_updater(drift)
    world.add(flow)
    world.flow = flow
    return world


def relay_blocks():
    trans = VGroup(*[boxed_label("T", BLUE, size=28, box=(.72, .55)) for _ in range(5)])
    trans.arrange(RIGHT, buff=.18).move_to([-.7, 1.25, 0])
    pde = VGroup(*[boxed_label("PDE", BLUE, size=24, box=(1.12, .52)) for _ in range(3)])
    pde.arrange(RIGHT, buff=.22).move_to([2.4, .25, 0])
    return trans, pde


# --------------------------------------------------------------------------- gain diagrams
def stage_card(text, x, color=BLUE):
    return boxed_label(text, color, size=28, box=(2.25, .82), fill_opacity=.18).move_to([x, .75, 0])


def gain_world(with_equation=True):
    backdrop = RoundedRectangle(width=12.55, height=6.35, corner_radius=.28,
                                stroke_opacity=0, fill_color=BLUE, fill_opacity=.075).set_z_index(-2)
    cards = VGroup(stage_card("catalytic", -4.2), stage_card("one-to-one", 0), stage_card("catalytic", 4.2))
    arrows = VGroup(Arrow(cards[0].get_right() + RIGHT * .08, cards[1].get_left() + LEFT * .08,
                          buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=.12),
                    Arrow(cards[1].get_right() + RIGHT * .08, cards[2].get_left() + LEFT * .08,
                          buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=.12))
    factors = VGroup(M("×100", 38, BLUE), M("×1", 38, BLUE), M("×100", 38, BLUE))
    for f, x in zip(factors, [-4.2, 0, 4.2]):
        f.move_to([x, -.45, 0])
    equation = M("100 × 1 × 100 = 10,000", 42, GOLD).move_to([0, -1.55, 0])
    note = T("invented example", 24, GREY).next_to(equation, DOWN, buff=.22)
    g = VGroup(backdrop, cards, arrows, factors)
    if with_equation:
        g.add(equation, note)
    g.cards, g.arrows, g.factors, g.equation, g.note = cards, arrows, factors, equation, note
    return g


def route_world(show_answers=False, simple=False):
    """Two invented routes at fixed coordinates, shared by predict, pause and reveal."""
    backdrop = RoundedRectangle(width=12.55, height=6.35, corner_radius=.28,
                                stroke_opacity=0, fill_color=BLUE, fill_opacity=.075).set_z_index(-2)
    title = T("simple model" if simple else "invented routes", 30, GOLD).move_to([0, 3.25, 0])
    rows = VGroup()
    all_factors, outputs = [], []
    for y, vals, col in [(1.75, [100, 1, 100], BLUE), (.15, [40, 1, 40], TEAL)]:
        inp = boxed_label("1 input", GOLD, size=24, box=(1.45, .52)).move_to([-5.55, y, 0])
        facs = VGroup(*[boxed_label(f"×{v}", col, size=26, box=(1.25, .55)) for v in vals])
        facs.arrange(RIGHT, buff=.65).move_to([-.35, y, 0])
        arr = VGroup()
        prev = inp
        for f in facs:
            arr.add(Arrow(prev.get_right() + RIGHT * .05, f.get_left() + LEFT * .05, buff=0,
                          color=col, stroke_width=4, max_tip_length_to_length_ratio=.18))
            prev = f
        out_text = "10,000" if vals[0] == 100 else "1,600"
        out = boxed_label(out_text if show_answers else "?", GOLD if vals[0] == 100 else GREY,
                          size=30, box=(1.55, .62)).move_to([5.35, y, 0])
        arr.add(Arrow(prev.get_right() + RIGHT * .05, out.get_left() + LEFT * .05, buff=0,
                      color=col, stroke_width=4, max_tip_length_to_length_ratio=.18))
        rows.add(VGroup(inp, arr, facs, out))
        all_factors.append(facs)
        outputs.append(out)
    g = VGroup(backdrop, title, rows)
    g.title, g.rows, g.factors, g.outputs = title, rows, all_factors, outputs
    return g


# --------------------------------------------------------------------------- local messenger world
def local_pool_world():
    boundary = DashedVMobject(Circle(radius=2.25, color=BLUE, stroke_width=4,
                                     fill_color=BLUE, fill_opacity=.09), num_dashes=32).move_to([-1.0, .25, 0])
    source = boxed_label("kinase", BLUE, size=28).move_to([-2.15, .55, 0])
    target = boxed_label("target", BLUE, size=28).move_to([.15, .55, 0])
    destroy = boxed_label("destroy", RED, size=26).move_to([-.95, -1.05, 0])
    outside = boxed_label("other target", GREY, size=26).move_to([4.25, .3, 0])
    anchor = Line([-2.4, -.15, 0], [.45, -.15, 0], color=GOLD, stroke_width=8)
    dots = VGroup(*[Dot([-1.8 + .42 * (i % 7), 1.5 - .32 * (i // 7), 0], radius=.1, color=TEAL)
                    for i in range(14)])
    g = VGroup(boundary, anchor, source, target, destroy, outside, dots, scope_tag("schematic"))
    g.boundary, g.source, g.target, g.destroy, g.outside, g.anchor, g.dots = boundary, source, target, destroy, outside, anchor, dots
    return g


# --------------------------------------------------------------------------- scenes
def shimmer(scene, y=0.0, h=3.4, w=2.4, x0=-6.0, x1=6.0, speed=1.7, color=BLUE, op=.16):
    """A soft translucent band that drifts across the stage behind everything, so long holds keep moving."""
    band = Rectangle(width=w, height=h, stroke_opacity=0, fill_color=color, fill_opacity=op).set_z_index(-1)
    band.move_to([x0, y, 0])
    def drift(m, dt):
        x = m.get_x() + speed * dt
        if x > x1:
            x = x0
        m.set_x(x)
    band.add_updater(drift)
    scene.add(band)
    return band


class S00Hook(SpokenScene):
    def construct(self):
        world = rod_world(include_photon=True)
        self.play(FadeIn(world.shell), Create(world.membrane), run_time=.8)
        self.play(FadeIn(VGroup(world.receptor, world.channels, world.cgmp, world.ions)), run_time=.8)
        animate_rod_idle(world)
        self.add(world.flow, scope_tag("schematic"))
        self.at("without letting its signal")
        self.play(world.photon.animate.move_to([-5.55, 1.25, 0]), run_time=1.6)
        self.at("Follow one photon")
        self.play(FadeIn(world.trace), FadeIn(world.trace_lab), run_time=.7)
        q = T("?", 52, GOLD).move_to([5.05, -1.9, 0])
        self.play(FadeIn(q), run_time=.5)
        self.at("reveals both the power")
        self.play(Indicate(world.receptor, color=BLUE), Indicate(q, color=GOLD), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Signaling Circuits"
    TITLE = "How One Photon Becomes a Cellular Signal"


class S02DarkCurrent(SpokenScene):
    def construct(self):
        world = rod_world(include_photon=True)
        animate_rod_idle(world)
        self.add(world, scope_tag("schematic"))
        shimmer(self, y=-.3, h=3.6, color=TEAL)
        self.play(Indicate(world.channels, color=GREEN), Indicate(world.cgmp, color=TEAL), run_time=1.1)
        self.at("ions carry")
        self.play(world.ions.animate.shift(UP * .42), run_time=1.2, rate_func=there_and_back)
        self.play(Indicate(world.trace, color=GOLD), run_time=1.0)
        self.at("photon activates")
        self.play(world.photon.animate.move_to(world.receptor.get_left() + LEFT * .28), run_time=1.0)
        active = boxed_label("rhodopsin", BLUE, size=28, box=(2.05, .62), fill_opacity=.22).move_to(world.receptor)
        self.play(FadeOut(world.photon), swap(world.receptor, active), run_time=.7)
        self.play(Indicate(active, color=BLUE, scale_factor=1.12), run_time=1.0)
        self.at("It does not add")
        no_add = T("not added current", 28, RED).move_to([3.75, 2.15, 0])
        self.play(FadeIn(no_add), run_time=.5)
        self.play(Indicate(world.channels, color=GREEN), Indicate(world.trace, color=GOLD), run_time=1.2)
        self.play(Indicate(world.cgmp, color=TEAL), run_time=.9)
        self.at("starts a relay")
        arrow = Arrow(active.get_right() + RIGHT * .1, world.channels.get_top() + UP * .08,
                      buff=.12, color=BLUE, stroke_width=5)
        self.play(FadeOut(no_add), GrowArrow(arrow), run_time=.9)
        self.play(Indicate(arrow, color=BLUE), run_time=.8)
        self.play(Indicate(world.channels, color=RED), run_time=1.0)
        self.at("existing current dips")
        dipped = response_trace(1.0)
        self.play(Transform(world.trace, dipped), run_time=1.4)
        self.finish()


class S03RelayStart(SpokenScene):
    def construct(self):
        world = rod_world(active=True)
        animate_rod_idle(world)
        self.add(world, scope_tag("schematic"))
        trans, pde = relay_blocks()
        self.play(Indicate(world.receptor, color=BLUE), run_time=.8)
        self.at("switches on many")
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT * .45) for t in trans], lag_ratio=.12), run_time=1.5)
        self.at("Each active")
        self.play(FadeIn(pde, shift=DOWN * .1), run_time=.9)
        self.at("destroys cyclic")
        self.play(LaggedStart(*[FadeOut(d, shift=DOWN * .25) for d in world.cgmp], lag_ratio=.07), run_time=1.5)
        self.finish()


class S03RelayOutput(SpokenScene):
    def construct(self):
        world = rod_world(active=True)
        animate_rod_idle(world)
        self.add(world, scope_tag("schematic"))
        self.at("some channels close")
        closed_world = rod_world(dip=1.0, active=True, closed=2)
        self.play(Transform(world.channels, closed_world.channels),
                  Transform(world.cgmp, closed_world.cgmp), Transform(world.ions, closed_world.ions), run_time=1.5)
        self.at("current dip")
        self.play(Transform(world.trace, closed_world.trace), run_time=1.2)
        self.at("small fraction")
        frac = T("small dip", 28, GOLD).move_to([3.95, -3.25, 0])
        self.play(FadeIn(frac), run_time=.5)
        self.at("One event")
        self.play(FadeOut(world[2]), run_time=.3)
        one = boxed_label("1 input", GOLD, size=28).move_to([-4.7, 2.15, 0])
        many = VGroup(*[Square(.3, color=BLUE, fill_color=BLUE, fill_opacity=.7) for _ in range(12)]).arrange_in_grid(3, 4, buff=.16).move_to([3.9, 1.4, 0])
        label = T("schematic count", 24, GREY).next_to(many, DOWN, buff=.2)
        self.play(FadeIn(one), run_time=.4)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * .12) for m in many], lag_ratio=.05), FadeIn(label), run_time=1.5)
        self.finish()


class S04GainProduct(SpokenScene):
    def construct(self):
        g = gain_world(False)
        self.play(FadeIn(g.cards), GrowFromCenter(g.arrows), run_time=1.0)
        self.at("output molecules per input")
        definition = T("gain = output per input", 34, GOLD).move_to([0, 2.45, 0])
        self.play(FadeIn(definition), run_time=.7)
        self.at("simple unsaturated cascade")
        self.play(LaggedStart(*[FadeIn(f) for f in g.factors], lag_ratio=.18), run_time=1.1)
        self.at("product of the step gains")
        self.play(FadeIn(g.equation), FadeIn(g.note), run_time=.9)
        self.play(Indicate(g.equation, color=GOLD), run_time=.8)
        self.finish()


class S04StepTypes(SpokenScene):
    def construct(self):
        g = gain_world(True)
        self.add(g)
        shimmer(self, y=0, h=4.6, color=BLUE)
        self.play(Indicate(g.cards[0], color=BLUE), Indicate(g.factors[0], color=GOLD), run_time=1.0)
        self.play(Indicate(g.equation, color=GOLD), run_time=1.0)
        self.play(Indicate(g.cards[2], color=BLUE), Indicate(g.factors[2], color=GOLD), run_time=1.0)
        self.at("handoff contributes")
        token = Square(.28, color=BLUE, fill_color=BLUE, fill_opacity=.8).move_to([-1.45, 1.55, 0])
        self.play(FadeIn(token), token.animate.move_to([1.45, 1.55, 0]), Indicate(g.factors[1], color=GOLD), run_time=1.5)
        self.at("contributes no multiplication")
        self.play(Indicate(g.cards[1], color=BLUE), run_time=.8)
        self.play(Indicate(g.factors[1], color=GOLD), run_time=.9)
        self.play(Indicate(g.arrows, color=BLUE), run_time=.9)
        self.at("between two catalytic")
        branches_l = VGroup(*[Line([-5.95, .48 + .18*i, 0], [-5.4, .48 + .18*i, 0], color=BLUE, stroke_width=3) for i in range(4)])
        branches_r = branches_l.copy().shift(RIGHT * 11.35)
        self.play(Create(branches_l), Create(branches_r), Indicate(g.cards[2], color=BLUE), run_time=1.5)
        self.play(token.animate.move_to([-1.45, 1.55, 0]), Indicate(g.cards[0], color=BLUE), run_time=1.2)
        self.play(token.animate.move_to([1.45, 1.55, 0]), Indicate(g.cards[1], color=BLUE), run_time=1.2)
        self.finish()


class S05RateLifetime(SpokenScene):
    def construct(self):
        catalyst = boxed_label("active catalyst", BLUE, size=32, box=(3.0, .9)).move_to([0, 1.75, 0])
        timer = Line([-4.6, -.1, 0], [4.6, -.1, 0], color=GREY, stroke_width=10)
        progress = Line([-4.6, -.1, 0], [-4.55, -.1, 0], color=GOLD, stroke_width=10)
        targets = VGroup(*[Square(.42, color=BLUE, fill_color=BLUE, fill_opacity=.65) for _ in range(12)]).arrange(RIGHT, buff=.22).move_to([0, -1.3, 0])
        count = ValueTracker(0)
        read = counter("targets reached: {:.0f}", count, at=[0, -2.25, 0], size=32, color=TEXT)
        shimmer(self, y=0, h=4.6, color=BLUE)
        self.play(FadeIn(catalyst), Create(timer), run_time=.8)
        self.at("working faster")
        self.add(read)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN*.15) for t in targets[:6]], lag_ratio=.09),
                  count.animate.set_value(6), Transform(progress, Line([-4.6,-.1,0],[0,-.1,0], color=GOLD, stroke_width=10)), run_time=1.7)
        self.at("remaining active longer")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN*.15) for t in targets[6:]], lag_ratio=.09),
                  count.animate.set_value(12), Transform(progress, Line([-4.6,-.1,0],[4.6,-.1,0], color=GOLD, stroke_width=10)), run_time=1.8)
        self.at("active lifetime helps")
        rule = T("rate × active lifetime → step gain", 34, GOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(rule), Indicate(progress, color=GOLD), run_time=1.0)
        self.finish()


class S05Uncoupling(SpokenScene):
    def construct(self):
        block = boxed_label("active catalyst", BLUE, size=30).move_to([-4.35, 1.8, 0])
        timer = Line([-5.4, .9, 0], [-3.3, .9, 0], color=GOLD, stroke_width=10)
        P = Plot(box=(-1.6, 4.9, -1.8, 2.2), xr=(0, 10), yr=(0, 1.1),
                 xticks=[0, 5, 10], yticks=[(0,"0"),(1,"peak")], xlabel="time", ylabel="output · schematic")
        long_fn = lambda x: min(x/2.5, 1.0) * np.exp(-max(x-4.0, 0)/4.5)
        short_fn = lambda x: min(x/2.5, 1.0) * np.exp(-max(x-4.0, 0)/1.25)
        long_curve = P.curve(long_fn, color=GREY, width=5)
        short_curve = P.curve(short_fn, color=BLUE, width=7)
        self.add(block, timer)
        self.play(Create(P), Create(long_curve), run_time=1.0)
        self.at("downstream shutoff")
        stop = boxed_label("downstream stop", RED, size=28).move_to([-4.35, -.15, 0])
        self.play(FadeIn(stop), Create(short_curve), run_time=1.3)
        peak = T("same peak", 28, GOLD).move_to([3.55, 2.75, 0])
        self.play(FadeIn(peak), Indicate(short_curve, color=BLUE), run_time=.8)
        self.at("Size and duration")
        icons = VGroup(T("wiring → size", 30, BLUE), T("clock → duration", 30, RED)).arrange(DOWN, aligned_edge=LEFT, buff=.28).move_to([-4.2, -1.45, 0])
        self.play(FadeIn(icons, shift=UP*.1), run_time=.8)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        routes = route_world(False)
        self.play(FadeIn(routes.title), FadeIn(VGroup(routes.rows[0][0], routes.rows[1][0])), run_time=.7)
        self.at("Both start")
        self.play(LaggedStart(*[Create(a) for row in routes.rows for a in row[1]], lag_ratio=.08),
                  FadeIn(VGroup(*[f for fs in routes.factors for f in fs])), run_time=2.0)
        self.at("Which root")
        self.play(FadeIn(VGroup(*routes.outputs)), run_time=.7)
        self.at("Follow every branch")
        q = question_card("Which route produces more?", y=-3.15, size=32)
        self.play(FadeIn(q), Indicate(routes.rows[0], color=BLUE), Indicate(routes.rows[1], color=TEAL), run_time=1.2)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which route produces more?"
    CARD = {"y": -3.15, "size": 32}
    SECONDS = 4.5

    def backdrop(self):
        g = route_world(False)
        pulse(g.rows[0][1], base=4, amp=.7, speed=1.8)
        pulse(g.rows[1][1], base=4, amp=.7, speed=1.6)
        return g


class S08Reveal(SpokenScene):
    def construct(self):
        routes = route_world(True, simple=True)
        hidden = route_world(False)
        self.add(hidden)
        shimmer(self, y=0, h=4.6, color=BLUE)
        self.play(swap(hidden.title, routes.title),
                  swap(hidden.outputs[0], routes.outputs[0]),
                  swap(hidden.outputs[1], routes.outputs[1]), run_time=1.2)
        self.at("larger product")
        bracket = Brace(routes.outputs[0], RIGHT, color=GOLD)
        self.play(GrowFromCenter(bracket), Indicate(routes.outputs[0], color=GOLD), run_time=.9)
        self.at("rule has limits")
        limits = T("when do factors stop multiplying?", 30, RED).move_to([0, -2.15, 0])
        self.play(FadeIn(limits), run_time=.7)
        self.finish()


class S08Scope(SpokenScene):
    def construct(self):
        backdrop = RoundedRectangle(width=12.55, height=6.35, corner_radius=.28,
                                    stroke_opacity=0, fill_color=BLUE, fill_opacity=.075).set_z_index(-2)
        self.add(backdrop)
        shimmer(self, y=0, h=4.6, color=BLUE)
        labels = ["saturation ?", "shared substrate ?", "deactivation ?", "feedback ?"]
        colors = [GOLD, TEAL, RED, RED]
        cards = VGroup(*[boxed_label(t, c, size=28, box=(2.7, .72)) for t, c in zip(labels, colors)]).arrange(RIGHT, buff=.38)
        fit(cards, max_w=12.2)
        cards.move_to([0, .65, 0])
        path = Arrow([-5.8, 2.1, 0], [5.7, 2.1, 0], color=BLUE, stroke_width=6, buff=0)
        self.play(GrowArrow(path), run_time=.8)
        self.at("shared substrates")
        self.play(LaggedStart(*[FadeIn(c, shift=UP*.12) for c in cards], lag_ratio=.15), run_time=1.8)
        self.at("depart from simple multiplication")
        narrow = Polygon([-1.1, 2.45,0],[1.1,2.45,0],[.45,1.75,0],[-.45,1.75,0], color=GOLD, fill_color=GOLD, fill_opacity=.12)
        self.play(FadeIn(narrow), path.animate.set_stroke(width=3), run_time=1.0)
        self.at("Use the product only")
        cap = caption("Use the product only when simple counting fits.", size=30, color=TEXT)
        self.play(FadeIn(cap), run_time=.8)
        self.finish()


class S09Evidence(SpokenScene):
    def construct(self):
        world = rod_world(dip=.8, active=True, closed=1)
        animate_rod_idle(world)
        self.add(world, scope_tag("schematic"))
        self.at("upstream fluctuations")
        bands = VGroup(*[response_trace(.8 + d, color=GREY).set_opacity(.35) for d in [-.16,-.08,.08,.16]])
        self.play(FadeIn(bands), run_time=.8)
        fl = T("fluctuation", 28, GREY).move_to([3.75, -3.3, 0])
        self.play(FadeIn(fl), run_time=.5)
        self.at("weak signals need evidence")
        self.play(Indicate(world.trace, color=GOLD), run_time=.8)
        self.at("separated blank trials")
        trials = VGroup(*[response_trace(.75 if i in [1,3,4] else 0, color=BLUE if i in [1,3,4] else GREY).scale(.48)
                          for i in range(5)]).arrange(DOWN, buff=.14).move_to([-.4, .55, 0])
        self.play(FadeOut(VGroup(world.shell, world.membrane, world.receptor, world.channels, world.cgmp, world.ions, bands, fl)),
                  LaggedStart(*[FadeIn(t) for t in trials], lag_ratio=.12), run_time=1.4)
        self.at("tested their counts")
        brace = Brace(trials, RIGHT, color=GOLD)
        test = T("Poisson test", 30, GOLD).next_to(brace, RIGHT, buff=.18)
        self.play(GrowFromCenter(brace), FadeIn(test), run_time=.8)
        self.finish()


class S09Shutoff(SpokenScene):
    def construct(self):
        world = rod_world(dip=1.0, active=True, closed=2)
        trans, _ = relay_blocks()
        self.add(world, trans, scope_tag("schematic"))
        self.at("needs a stop")
        self.remove(world[2])
        rings = VGroup(Circle(radius=1.25, color=RED, stroke_width=6).move_to(world.receptor),
                       *[Circle(radius=.55, color=RED, stroke_width=5).move_to(t) for t in trans])
        self.play(Create(rings), run_time=1.0)
        self.at("Rhodopsin is shut")
        self.play(FadeOut(world.receptor), rings[0].animate.set_opacity(.2), run_time=.8)
        self.at("switch itself off")
        self.play(LaggedStart(*[FadeOut(t, shift=DOWN*.1) for t in trans], lag_ratio=.08),
                  *[r.animate.set_opacity(.2) for r in rings[1:]], run_time=1.1)
        restored = rod_world(dip=0, active=False, closed=0)
        self.play(Transform(world.channels, restored.channels), Transform(world.cgmp, restored.cgmp),
                  Transform(world.ions, restored.ions), Transform(world.trace, restored.trace), run_time=1.3)
        self.finish()


class S10LocalPool(SpokenScene):
    def construct(self):
        g = local_pool_world()
        self.play(FadeIn(g.source), FadeIn(g.dots), run_time=.8)
        bob(g.dots, amp=.05, speed=1.6)
        self.at("unintended targets")
        self.play(g.dots.animate.shift(RIGHT * 2.1), Indicate(g.outside, color=GREY), FadeIn(g.outside), run_time=1.2)
        self.at("Local binding")
        self.play(Create(g.boundary), Create(g.anchor), FadeIn(g.target), run_time=1.1)
        self.at("destruction restrict")
        self.play(FadeIn(g.destroy), g.dots.animate.shift(LEFT * 1.5), run_time=1.0)
        self.at("Anchoring proteins")
        self.play(g.source.animate.shift(RIGHT * .35), g.target.animate.shift(LEFT * .35), Indicate(g.anchor, color=GOLD), run_time=1.0)
        self.at("enzyme within one")
        self.play(Indicate(g.destroy, color=RED), FadeOut(g.dots[-4:]), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Price(SpokenScene):
    def construct(self):
        g = local_pool_world()
        bob(g.dots, amp=.05, speed=1.8)
        self.add(g)
        self.play(Indicate(g.dots, color=TEAL), run_time=.8)
        self.at("strong signal")
        stop = boxed_label("stop it", RED, size=30).move_to([3.85, 1.6, 0])
        local = boxed_label("keep it local", BLUE, size=30).move_to([3.85, -.9, 0])
        self.play(FadeIn(stop), Indicate(g.destroy, color=RED), run_time=.8)
        self.at("kept near")
        self.play(FadeIn(local), Indicate(g.boundary, color=BLUE), run_time=.8)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        world = rod_world(include_photon=True)
        animate_rod_idle(world)
        self.add(world, scope_tag("schematic"))
        self.play(world.photon.animate.move_to(world.receptor.get_left() + LEFT * .28), run_time=.8)
        self.play(FadeOut(world.photon), run_time=.25)
        self.at("cascade made a detectable dip")
        trans, pde = relay_blocks()
        self.play(FadeIn(trans), FadeIn(pde), run_time=.8)
        active = rod_world(dip=1.0, active=True, closed=2)
        self.play(Transform(world.receptor, active.receptor), Transform(world.channels, active.channels),
                  Transform(world.cgmp, active.cgmp), Transform(world.ions, active.ions),
                  Transform(world.trace, active.trace), run_time=1.6)
        self.at("timed shutoff ended")
        self.remove(world[2])
        timers = VGroup(Circle(radius=1.25, color=RED).move_to(world.receptor),
                        *[Circle(radius=.55, color=RED).move_to(t) for t in trans])
        self.play(Create(timers), run_time=.7)
        restored = rod_world()
        self.play(FadeOut(VGroup(trans, pde, timers)), Transform(world.receptor, restored.receptor),
                  Transform(world.channels, restored.channels), Transform(world.cgmp, restored.cgmp),
                  Transform(world.ions, restored.ions), Transform(world.trace, restored.trace), run_time=1.5)
        self.at("In other pathways")
        frame = RoundedRectangle(width=4.35, height=2.55, corner_radius=.18, color=GREY).move_to([3.05, .65, 0])
        label = T("other pathways", 28, TEXT).move_to([3.05, 2.18, 0])
        boundary = DashedVMobject(Circle(radius=.85, color=BLUE), num_dashes=18).move_to([2.8, .65, 0])
        anchor = Line([2.25, .35, 0], [3.2, .35, 0], color=GOLD, stroke_width=7)
        destroy = Square(.28, color=RED, fill_color=RED, fill_opacity=.7).move_to([3.45, .7, 0])
        dots = VGroup(*[Dot([2.25 + .32*i, 1.05, 0], radius=.07, color=TEAL) for i in range(5)])
        inset = VGroup(boundary, anchor, destroy, dots)
        self.play(world.animate.set_opacity(.28), FadeIn(frame), FadeIn(inset), FadeIn(label), run_time=1.0)
        self.at("local anchoring and destruction")
        self.play(Indicate(inset, color=TEAL), run_time=1.0)
        self.at("Those safeguards")
        self.play(Indicate(VGroup(frame, inset), color=GOLD), run_time=.9)
        self.finish()


class S12End(EndCard):
    LINE = "Simple cascades multiply gain; high gain needs shutoff and sometimes insulation."
