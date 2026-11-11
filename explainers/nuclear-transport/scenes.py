"""One Pore, Two Directions — nuclear transport explainer.

COLOR MAP
  YELLOW  soluble protein cargo
  BLUE    importin alpha/beta and NLS
  PURPLE  CRM1 export receptor
  ORANGE  NES
  GREEN   RanGTP
  GREY    RanGDP, small particles, and nuclear envelope
  TEAL    FG repeats, RCC1, RanGAP, and RanBP1

The same large left/right cutaway is rebuilt at identical coordinates in every
scene.  All molecular actors are deliberately schematic labelled cartoons.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CYT_TINT = BG
NUC_TINT = "#24503B"


def label(text, pos, color=TEXT, size=28, weight=NORMAL):
    return T(text, size=size, color=color, weight=weight).move_to(pos)


def add_bob(mob, scene, amp=0.08, speed=1.0, phase=0.0, axis=UP):
    """Gentle ambient motion around a fixed centre; safe during narrated holds."""
    state = {"last": 0.0}

    def bob(m, dt):
        del dt
        now = amp * math.sin(speed * scene.renderer.time + phase)
        m.shift(axis * (now - state["last"]))
        state["last"] = now
    mob.add_updater(bob)
    return mob


def world(scene, question=None):
    """The film's carried world: left cytoplasm, right nucleus, one large pore."""
    left = Rectangle(width=6.75, height=7.0, stroke_width=0,
                     fill_color=CYT_TINT, fill_opacity=0.96).move_to([-3.38, 0, 0])
    right = Rectangle(width=6.75, height=7.0, stroke_width=0,
                      fill_color=NUC_TINT, fill_opacity=0.90).move_to([3.38, 0, 0])
    membranes = VGroup()
    for x in (-0.52, 0.52):
        for y in (-2.75, 2.75):
            membranes.add(RoundedRectangle(corner_radius=0.07, width=0.18, height=1.55,
                                            stroke_color=GREY, stroke_width=2,
                                            fill_color=GREY, fill_opacity=0.65).move_to([x, y, 0]))
    rims = VGroup(
        RoundedRectangle(corner_radius=0.20, width=1.65, height=0.30, stroke_color=GREY,
                         stroke_width=3, fill_color=GREY, fill_opacity=0.34).move_to([0, 2.0, 0]),
        RoundedRectangle(corner_radius=0.20, width=1.65, height=0.30, stroke_color=GREY,
                         stroke_width=3, fill_color=GREY, fill_opacity=0.34).move_to([0, -2.0, 0]),
    )
    chains = VGroup()
    for i, y in enumerate(np.linspace(-1.58, 1.58, 11)):
        side = -1 if i % 2 == 0 else 1
        chain = CubicBezier([side * 0.72, y, 0], [side * 0.25, y + 0.28, 0],
                            [-side * 0.12, y - 0.24, 0], [-side * 0.42, y, 0],
                            color=TEAL, stroke_width=7)
        phase = i * 0.72

        def make_wave(y0, side0, phase0):
            def wave(m, dt):
                del dt
                wiggle = 0.28 * math.sin(scene.renderer.time * 2.2 + phase0)
                m.become(CubicBezier([side0 * 0.72, y0, 0],
                                     [side0 * (0.32 + wiggle), y0 + 0.28, 0],
                                     [-side0 * (0.12 - wiggle), y0 - 0.24, 0],
                                     [-side0 * 0.42, y0, 0], color=TEAL, stroke_width=7))
            return wave
        chain.add_updater(make_wave(y, side, phase))
        chains.add(chain)
    places = VGroup(label("CYTOPLASM", [-4.8, -3.22, 0], TEXT, 28, BOLD),
                    label("NUCLEUS", [4.8, -3.22, 0], TEXT, 28, BOLD))
    schematic = chip("SCHEMATIC", TEAL, size=22, pad=0.15, fill_opacity=0.13).move_to([5.55, 3.28, 0])
    g = VGroup(left, right, membranes, rims, chains, places, schematic)
    g.chains, g.rims = chains, rims
    if question:
        q = label(question, [0, 3.18, 0], YELLOW, 34, BOLD)
        fit(q, max_w=9.7)
        q_bg = RoundedRectangle(corner_radius=0.12, width=q.width + 0.48,
                                height=q.height + 0.24, stroke_width=0,
                                fill_color=BG, fill_opacity=0.96).move_to(q)
        q_bg.set_z_index(20)
        q.set_z_index(21)
        g.add(q_bg, q)
        g.question = q
    return g


def cargo(pos, tag=None, tag_color=BLUE, scale=1.0):
    body = RoundedRectangle(corner_radius=0.20, width=1.12, height=0.88,
                            stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.86).move_to(pos)
    gloss = Line(body.get_corner(UL) + [0.16, -0.12, 0], body.get_top() + [0.22, -0.12, 0],
                 color=TEXT, stroke_width=2).set_opacity(0.55)
    g = VGroup(body, gloss)
    if tag:
        # Compensate for the final actor scale so every teaching tag remains 28 pt.
        txt = T(tag, size=28 / scale, color=BG, weight=BOLD)
        tab = RoundedRectangle(corner_radius=0.06, width=max(0.80, txt.width + 0.18),
                               height=max(0.42, txt.height + 0.12),
                               stroke_width=0, fill_color=tag_color, fill_opacity=1)
        txt.move_to(tab)
        badge = VGroup(tab, txt).move_to(body.get_top() + UP * 0.12)
        g.add(badge)
        g.tag = badge
    g.body = body
    return g.scale(scale)


def receptor(text, pos, color=BLUE, side=LEFT, scale=1.0):
    """A readable cup rather than an inert name chip."""
    s = -1 if np.allclose(side, LEFT) else 1
    cup = VGroup(
        Line([s * 0.62, 0.58, 0], [s * 0.62, -0.58, 0], color=color, stroke_width=8),
        Line([s * 0.62, 0.58, 0], [-s * 0.05, 0.58, 0], color=color, stroke_width=8),
        Line([s * 0.62, -0.58, 0], [-s * 0.05, -0.58, 0], color=color, stroke_width=8),
    )
    cup.scale(scale)
    txt = T(text, size=28, color=color, weight=BOLD)
    txt_bg = RoundedRectangle(corner_radius=0.06, width=txt.width + 0.18,
                              height=txt.height + 0.10, stroke_width=0,
                              fill_color=BG, fill_opacity=0.94)
    name = VGroup(txt_bg, txt.move_to(txt_bg)).next_to(cup, DOWN, buff=0.16)
    return VGroup(cup, name).move_to(pos)


def ran(pos, gtp=True, scale=1.0, text=True):
    col = GREEN if gtp else GREY
    radius = 0.38 / scale if text else 0.27
    dot = Circle(radius=radius, stroke_color=col, stroke_width=3,
                 fill_color=col, fill_opacity=0.82)
    pos = [pos[0], pos[1], 0] if len(pos) == 2 else pos
    if text:
        txt = T("GTP" if gtp else "GDP", size=28 / scale, color=BG, weight=BOLD).move_to(dot)
        return VGroup(dot, txt).scale(scale).move_to(pos)
    return dot.scale(scale).move_to(pos)


def ran_field(scene, equal=False, labelled=True):
    """Fixed density map used without lateral drift in every gradient scene."""
    nuc_pts = [(2.0, 2.25), (3.15, 1.50), (4.45, 2.28), (5.55, 1.20),
               (2.25, -1.30), (3.75, -2.20), (5.25, -1.35)]
    cyt_green = [(-5.4, 1.65), (-4.0, 2.35), (-2.75, 1.30),
                 (-5.15, -1.30), (-3.65, -2.15), (-2.25, -1.35)]
    cyt_grey = [(-5.35, 1.75), (-4.05, 2.30), (-2.65, 1.25),
                (-5.15, -1.35), (-3.65, -2.15), (-2.30, -1.35)]
    ng = VGroup(*[ran(p, True, 0.78, text=False) for p in nuc_pts])
    cg = VGroup(*[ran(p, equal, 0.78, text=False) for p in (cyt_green if equal else cyt_grey)])
    for i, d in enumerate([*ng, *cg]):
        add_bob(d, scene, amp=0.08, speed=0.75 + (i % 3) * 0.1, phase=i * 0.8,
                axis=RIGHT if i % 2 else UP)
    g = VGroup(ng, cg)
    g.nuclear, g.cytoplasmic = ng, cg
    if labelled:
        l1 = label("RanGTP high", [4.55, 2.95, 0], GREEN, 28, BOLD)
        l2 = label("RanGTP equal" if equal else "RanGDP high", [-4.35, 2.95, 0],
                   GREEN if equal else GREY, 28, BOLD)
        g.add(l1, l2)
    return g


def drift_dots(scene, points, color=GREY, radius=0.11):
    dots = VGroup(*[Dot(p, radius=radius, color=color) for p in points])
    for i, d in enumerate(dots):
        add_bob(d, scene, amp=0.10, speed=0.8 + i * 0.08, phase=i, axis=UP if i % 2 else RIGHT)
    return dots


class S00Hook(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        left_c = add_bob(cargo([-4.7, 0.35, 0]), self, 0.10, 0.9)
        right_c = add_bob(cargo([4.7, -0.35, 0]), self, 0.10, 0.9, 1.5)
        self.at("The nuclear pore")
        self.play(FadeIn(left_c), FadeIn(right_c), run_time=0.55)
        self.play(left_c.animate.shift(RIGHT * 2.7), right_c.animate.shift(LEFT * 2.7),
                  run_time=2.2, rate_func=smooth)
        self.at("So how can")
        q = label("?", [0, 0, 0], YELLOW, 112, BOLD)
        arrows = VGroup(Arrow([-2.8, 1.15, 0], [2.8, 1.15, 0], buff=0, color=GREY,
                              stroke_width=5, tip_length=0.25),
                        Arrow([2.8, -1.15, 0], [-2.8, -1.15, 0], buff=0, color=GREY,
                              stroke_width=5, tip_length=0.25))
        self.play(FadeIn(q, scale=0.6), Create(arrows), run_time=1.0)
        self.at("Watch one pore")
        self.play(Indicate(w.rims, color=TEAL, scale_factor=1.05), run_time=1.1)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Nuclear transport"
    TITLE = "One Pore, Two Directions"

    def construct(self):
        w = world(self)
        veil = Rectangle(width=13.5, height=7.1, stroke_width=0, fill_color=BG,
                         fill_opacity=0.52)
        title = T(self.TITLE.upper(), size=48, color=TEXT, font=TITLE_FONT, weight=BOLD)
        fit(title, max_w=11.2)
        rule = Line(LEFT * 2.0, RIGHT * 2.0, color=GOLD, stroke_width=4).next_to(title, DOWN, 0.28)
        panel = RoundedRectangle(corner_radius=0.18, width=title.width + 0.75,
                                 height=title.height + rule.height + 0.82,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.92)
        panel.move_to(VGroup(title, rule))
        self.add(w)
        self.play(FadeIn(veil), FadeIn(panel), FadeIn(title, shift=UP * 0.15),
                  GrowFromCenter(rule), run_time=0.45)
        self.wait(0.7)
        self.play(FadeOut(VGroup(veil, panel, title, rule)), run_time=0.35)


class S02Barrier(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        soluble = label("soluble cargo", [-4.65, 1.45, 0], YELLOW, 30, BOLD)
        free = cargo([-4.6, 0.4, 0], scale=0.92)
        self.at("Soluble cargo")
        self.play(FadeIn(free, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(soluble), free.animate.shift(UP * 0.18), run_time=0.6)
        self.play(free.animate.shift(RIGHT * 1.35 + DOWN * 0.55), run_time=1.7, rate_func=smooth)
        self.play(free.animate.shift(LEFT * 1.0 + UP * 0.25), run_time=1.5, rate_func=smooth)
        self.at("Here is a first picture")
        self.play(FadeOut(soluble), free.animate.shift(LEFT * 0.35 + DOWN * 0.35), run_time=0.55)
        two_way = VGroup(Arrow([-2.5, 1.28, 0], [2.5, 1.28, 0], buff=0, color=GREY,
                               stroke_width=4, tip_length=0.22),
                         Arrow([2.5, -1.28, 0], [-2.5, -1.28, 0], buff=0, color=GREY,
                               stroke_width=4, tip_length=0.22))
        self.at("For soluble protein cargo")
        self.play(Create(two_way), run_time=0.8)
        self.play(FadeOut(free), run_time=0.3)
        preview_a = VGroup(*[Dot([-5.2 - i * 0.35, 0.95 + 0.12 * (i % 2), 0],
                                    radius=0.11, color=GREY) for i in range(5)])
        preview_b = VGroup(*[Dot([5.2 + i * 0.35, -0.95 - 0.12 * (i % 2), 0],
                                    radius=0.11, color=GREY) for i in range(5)])
        self.add(preview_a, preview_b)
        self.play(preview_a.animate.shift(RIGHT * 10.8), preview_b.animate.shift(LEFT * 10.8),
                  run_time=5.4, rate_func=linear)
        self.play(FadeOut(preview_a), FadeOut(preview_b), run_time=0.2)
        small = VGroup(*[Dot([-4.8 - i * 0.32, 0.65 - i * 0.25, 0], radius=0.12, color=GREY)
                         for i in range(6)])
        self.at("Small gray particles")
        self.play(FadeIn(small), run_time=0.25)
        self.play(small.animate.shift(RIGHT * 10.2), run_time=2.0, rate_func=linear)
        self.play(FadeOut(small), run_time=0.2)
        lone = cargo([-4.7, 0, 0])
        self.at("Larger yellow cargo")
        self.play(FadeIn(lone), run_time=0.35)
        self.play(lone.animate.shift(RIGHT * 2.2), run_time=2.5, rate_func=linear)
        self.play(lone.animate.shift(LEFT * 0.3), run_time=0.35)
        rec = receptor("receptor", [-4.6, -0.05, 0], BLUE, side=RIGHT, scale=0.88)
        fast = cargo([-5.25, 0.15, 0], scale=0.84)
        self.at("Receptors engage")
        self.play(FadeOut(lone), FadeIn(rec), FadeIn(fast), run_time=0.5)
        complex_ = VGroup(rec, fast)
        self.play(complex_.animate.shift(RIGHT * 9.1), run_time=2.6, rate_func=smooth)
        self.finish()


class S03CargoLabels(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        imp_c = cargo([-4.65, 0.35, 0])
        exp_c = cargo([4.65, -0.35, 0])
        self.at("Cargo carries labels")
        self.play(FadeIn(imp_c), FadeIn(exp_c), run_time=0.7)
        nls = cargo([-4.65, 0.35, 0], "NLS", BLUE)
        alpha = receptor("α", [-3.25, 0.35, 0], BLUE, side=LEFT, scale=0.78)
        imp_label = label("importin", [-3.0, -0.82, 0], BLUE, 28, BOLD)
        self.at("A blue NLS tag")
        self.play(ReplacementTransform(imp_c, nls), FadeIn(alpha, shift=LEFT * 0.2),
                  FadeIn(imp_label), run_time=0.65)
        self.at("which holds cargo")
        self.play(alpha.animate.shift(LEFT * 0.55), run_time=0.65)
        beta = receptor("β", [-2.25, 0.35, 0], BLUE, side=LEFT, scale=0.78)
        self.at("joins it and engages")
        self.play(FadeIn(beta, shift=LEFT * 0.25), run_time=0.55)
        self.play(VGroup(nls, alpha, beta).animate.shift(RIGHT * 0.45), run_time=0.75)
        nes = cargo([4.65, -0.35, 0], "NES", ORANGE)
        self.at("An orange NES tag")
        self.play(ReplacementTransform(exp_c, nes), run_time=0.55)
        crm = receptor("CRM1", [3.05, -0.35, 0], PURPLE, side=RIGHT, scale=0.9)
        self.at("purple export receptor")
        self.play(FadeIn(crm, shift=RIGHT * 0.3), run_time=0.65)
        add_bob(crm, self, 0.08, 0.9, axis=LEFT)
        self.finish()


class S04Gradient(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        switch = VGroup(ran([-0.65, 0, 0], False, 1.2), DoubleArrow([-0.15, 0, 0], [0.95, 0, 0],
                        buff=0, color=TEAL, stroke_width=4, tip_length=0.18), ran([1.45, 0, 0], True, 1.2))
        self.at("difference between")
        self.play(FadeIn(switch), run_time=0.7)
        self.at("small switch protein")
        self.play(switch.animate.scale(1.10), run_time=0.45)
        self.play(switch.animate.scale(1 / 1.10), run_time=0.45)
        self.play(switch.animate.shift(UP * 0.32), run_time=0.65)
        self.play(switch.animate.shift(DOWN * 0.32), run_time=0.65)
        self.at("on with")
        on = label("ON", [2.25, 0, 0], GREEN, 30, BOLD)
        off = label("OFF", [-1.55, 0, 0], GREY, 30, BOLD)
        self.play(FadeIn(on), FadeIn(off), run_time=0.5)
        self.play(FadeOut(VGroup(switch, on, off)), run_time=0.35)
        field = ran_field(self, equal=False)
        rcc = chip("RCC1", TEAL, size=26).move_to([4.75, 0.10, 0])
        gap = chip("RanGAP", TEAL, size=26).move_to([-4.75, -0.05, 0])
        grey = ran([3.35, 0.05, 0], False, 0.92)
        self.at("Green RAN")
        self.play(FadeIn(field.nuclear), FadeIn(rcc), run_time=1.0)
        self.play(grey.animate.move_to(rcc.get_left() + LEFT * 0.35), run_time=0.65)
        green = ran(grey.get_center(), True, 0.92)
        self.play(ReplacementTransform(grey, green), green.animate.shift(UP * 0.65), run_time=0.55)
        self.at("Gray RAN")
        self.play(FadeIn(field.cytoplasmic), FadeIn(gap), run_time=0.9)
        turn = ran([-3.45, -0.05, 0], True, 0.92)
        self.play(turn.animate.move_to(gap.get_right() + RIGHT * 0.35), run_time=0.55)
        off_turn = ran(turn.get_center(), False, 0.92)
        self.play(ReplacementTransform(turn, off_turn), off_turn.animate.shift(DOWN * 0.65), run_time=0.55)
        self.at("unequal distribution")
        grad_text = label("RAN GRADIENT", ORIGIN, TEAL, 34, BOLD)
        grad_bg = RoundedRectangle(corner_radius=0.10, width=grad_text.width + 0.34,
                                   height=grad_text.height + 0.16, stroke_width=0,
                                   fill_color=BG, fill_opacity=0.94)
        grad = VGroup(grad_bg, grad_text.move_to(grad_bg)).move_to([0, 2.72, 0])
        grad.set_z_index(10)
        self.play(FadeOut(VGroup(rcc, gap, green, off_turn)), FadeIn(field[2:]), FadeIn(grad), run_time=0.7)
        self.finish()


class S05Import(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        self.add(w, field)
        c = cargo([-5.15, 0, 0], "NLS", BLUE, 0.85)
        a = receptor("α", [-4.15, 0, 0], BLUE, side=LEFT, scale=0.68)
        b = receptor("β", [-3.35, 0, 0], BLUE, side=LEFT, scale=0.72)
        comp = VGroup(c, a, b)
        self.at("simplest form")
        self.play(FadeIn(comp), run_time=0.55)
        self.play(comp.animate.shift(RIGHT * 4.1), run_time=2.0, rate_func=smooth)
        self.at("It moves from")
        self.play(comp.animate.shift(RIGHT * 2.7), run_time=2.2, rate_func=linear)
        self.at("In the nucleus")
        self.play(comp.animate.shift(RIGHT * 1.2), run_time=1.0)
        token = ran([4.9, 1.3, 0], True, 0.95)
        self.at("binds important beta")
        self.play(FadeIn(token), token.animate.move_to(b.get_top() + UP * 0.22), run_time=0.75)
        self.play(b.animate.shift(RIGHT * 1.05), a.animate.shift(LEFT * 0.35), run_time=0.75)
        self.at("then releases the blue")
        self.play(c.animate.shift(UP * 1.15 + RIGHT * 0.35), a.animate.shift(DOWN * 0.65), run_time=0.8)
        self.at("All three receptor")
        marks = VGroup(*[Circle(radius=0.72, color=TEAL, stroke_width=3).move_to(x.get_center())
                         for x in (c, a, b)])
        self.play(LaggedStart(*[Create(x) for x in marks], lag_ratio=0.18), run_time=0.9)
        self.play(FadeOut(marks), run_time=0.35)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = world(self, "CAN IT UNLOAD ONLY INSIDE?")
        loaded = VGroup(cargo([-1.85, 0, 0], "NLS", BLUE, 0.82),
                        receptor("importin", [-2.85, 0, 0], BLUE, side=LEFT, scale=0.72))
        self.add(w, loaded)
        field = ran_field(self, equal=False, labelled=False)
        self.add(field)
        self.at("Now predict")
        self.play(Indicate(w.question, color=YELLOW, scale_factor=1.03), run_time=0.65)
        equal = ran_field(self, equal=True, labelled=False)
        self.at("equally common")
        self.play(ReplacementTransform(field, equal), run_time=1.15)
        self.at("unload only inside")
        self.play(loaded.animate.shift(RIGHT * 3.7), run_time=1.3, rate_func=there_and_back)
        self.at("Hold the two")
        add_bob(loaded, self, 0.09, 0.8, axis=RIGHT)
        self.play(Indicate(VGroup(equal.nuclear, equal.cytoplasmic), color=GREEN, scale_factor=1.02), run_time=0.7)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        w = world(self, "CAN IT UNLOAD ONLY INSIDE?")
        field = ran_field(self, equal=True, labelled=False)
        loaded = VGroup(cargo([-1.85, 0, 0], "NLS", BLUE, 0.82),
                        receptor("importin", [-2.85, 0, 0], BLUE, side=LEFT, scale=0.72))
        add_bob(loaded, self, 0.09, 0.8, axis=RIGHT)
        self.add(w, field, loaded)
        self.wait(4.5)


class S08Reveal(SpokenScene):
    def construct(self):
        w = world(self)
        equal = ran_field(self, equal=True, labelled=False)
        self.add(w, equal)
        no = label("NO", [-5.65, 2.78, 0], RED, 54, BOLD)
        c1 = cargo([-3.95, 0.45, 0], "NLS", BLUE, 0.78)
        r1 = receptor("importin", [-2.85, 0.45, 0], BLUE, side=LEFT, scale=0.66)
        self.at("import could still cross")
        self.play(FadeIn(no), FadeIn(VGroup(c1, r1)), run_time=0.65)
        self.play(VGroup(c1, r1).animate.shift(RIGHT * 5.8), run_time=1.8)
        self.at("on either side")
        self.play(c1.animate.shift(UP * 1.15), r1.animate.shift(DOWN * 0.45), run_time=0.7)
        c2 = cargo([-4.6, -1.15, 0], "NLS", BLUE, 0.72)
        open_r = receptor("importin", [-3.2, -1.15, 0], BLUE, side=RIGHT, scale=0.66)
        x = T("×", size=58, color=RED, weight=BOLD).move_to([-5.55, -0.45, 0])
        self.play(FadeIn(c2), FadeIn(open_r), FadeIn(x, scale=0.7), run_time=0.65)
        self.at("Net import")
        two = DoubleArrow([-2.1, 0, 0], [2.1, 0, 0], buff=0, color=GREY,
                          stroke_width=5, tip_length=0.23)
        self.play(FadeOut(VGroup(c1, r1, c2, open_r, x, no)), Create(two), run_time=0.7)
        restored = ran_field(self, equal=False, labelled=False)
        self.at("Restore the gradient")
        self.play(FadeOut(two), ReplacementTransform(equal, restored), run_time=1.2)
        release = cargo([4.2, 0.3, 0], "NLS", BLUE, 0.8)
        check = T("✓", size=72, color=GREEN, weight=BOLD).next_to(release, RIGHT, 0.35)
        self.at("nuclear side")
        self.play(FadeIn(release, shift=UP * 0.2), FadeIn(check, scale=0.7), run_time=0.65)
        self.finish()


class S09Export(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        self.add(w, field)
        c = cargo([4.85, 0.15, 0], "NES", ORANGE, 0.82)
        crm = receptor("CRM1", [3.25, 0.15, 0], PURPLE, side=RIGHT, scale=0.78)
        token = ran([4.2, 1.35, 0], True, 0.86)
        self.at("Export reverses")
        self.play(FadeIn(c), FadeIn(crm), run_time=0.55)
        self.at("helps purple")
        self.play(FadeIn(token), token.animate.move_to(crm.get_top() + UP * 0.18), run_time=0.6)
        self.play(crm.animate.shift(RIGHT * 0.72), run_time=0.6)
        complex_ = VGroup(c, crm, token)
        self.at("complex crosses outward")
        self.play(complex_.animate.shift(LEFT * 7.8), run_time=2.6, rate_func=smooth)
        bp = chip("RanBP1", TEAL, size=28).move_to([-5.2, -1.45, 0])
        self.at("RAN binding proteins")
        self.play(FadeIn(bp), bp.animate.next_to(crm, DOWN, 0.34), run_time=0.65)
        self.at("cargo come free")
        self.play(c.animate.shift(RIGHT * 0.95 + UP * 0.85), crm.animate.shift(RIGHT * 0.3),
                  FadeOut(bp), run_time=0.75)
        self.at("Hydrolysis then")
        grey = ran(token.get_center(), False, 0.86)
        self.play(ReplacementTransform(token, grey), run_time=0.6)
        self.at("another round")
        self.play(crm.animate.shift(RIGHT * 0.65), grey.animate.shift(DOWN * 0.6), run_time=0.75)
        self.finish()


class S10SameRule(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        self.add(w, field)
        key_text = VGroup(label("IMPORTIN: UNLOAD", ORIGIN, BLUE, 28, BOLD),
                          label("CRM1: LOAD", ORIGIN, PURPLE, 28, BOLD)).arrange(DOWN, buff=0.14)
        key_bg = RoundedRectangle(corner_radius=0.12, width=key_text.width + 0.34,
                                  height=key_text.height + 0.24, stroke_width=0,
                                  fill_color=BG, fill_opacity=0.94)
        key = VGroup(key_bg, key_text.move_to(key_bg)).move_to([4.15, 2.56, 0])
        key.set_z_index(10)
        self.at("Nuclear RAN")
        self.play(FadeIn(key), run_time=0.6)
        imp = VGroup(cargo([-4.8, 0.85, 0], "NLS", BLUE, 0.64),
                     receptor("importin", [-3.9, 0.85, 0], BLUE, side=LEFT, scale=0.56))
        exp = VGroup(cargo([4.8, -0.85, 0], "NES", ORANGE, 0.64),
                     receptor("CRM1", [3.75, -0.85, 0], PURPLE, side=RIGHT, scale=0.61),
                     ran([4.25, -1.75, 0], True, 0.68))
        self.at("Blue importance carry")
        self.play(FadeIn(imp), run_time=0.35)
        self.play(MoveAlongPath(imp, ArcBetweenPoints([-4.35, 0.85, 0], [4.15, 0.85, 0], angle=-0.15)),
                  run_time=2.0, rate_func=smooth)
        self.at("Purple CRM1")
        self.play(FadeIn(exp), run_time=0.35)
        self.play(MoveAlongPath(exp, ArcBetweenPoints([4.2, -0.85, 0], [-4.15, -0.85, 0], angle=-0.15)),
                  run_time=2.0, rate_func=smooth)
        self.at("One asymmetry")
        self.play(Indicate(field.nuclear, color=GREEN, scale_factor=1.08),
                  Indicate(key, color=TEAL, scale_factor=1.03), run_time=0.9)
        self.finish()


class S11EnergyScope(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        rcc = chip("RCC1", TEAL, size=28).move_to([4.6, 0.25, 0])
        gap = chip("RanGAP", TEAL, size=28).move_to([-4.6, 0.25, 0])
        self.add(w, field)
        self.at("GTP hydrolysis maintains")
        self.play(FadeIn(rcc), FadeIn(gap), run_time=0.55)
        self.play(Indicate(rcc, color=TEAL), Indicate(gap, color=TEAL), run_time=0.85)
        piston = VGroup(Rectangle(width=1.25, height=0.52, color=RED, stroke_width=4).move_to([-2.65, 0.05, 0]),
                        Arrow([-3.55, 0.05, 0], [-1.75, 0.05, 0], buff=0, color=RED,
                              stroke_width=6, tip_length=0.24))
        no_push = Cross(piston, stroke_color=RED, stroke_width=6)
        self.at("does not push")
        self.play(FadeIn(piston), Create(no_push), run_time=0.65)
        rule_text = label("RAN SETS LOAD / UNLOAD", ORIGIN, GREEN, 32, BOLD)
        rule_bg = RoundedRectangle(corner_radius=0.10, width=rule_text.width + 0.34,
                                   height=rule_text.height + 0.20, stroke_width=0,
                                   fill_color=BG, fill_opacity=0.94)
        rule = VGroup(rule_bg, rule_text.move_to(rule_bg)).move_to([0, 2.90, 0])
        rule.set_z_index(10)
        self.at("RAN mainly sets")
        self.play(FadeOut(VGroup(piston, no_push)), FadeIn(rule), run_time=0.65)
        imp_c = cargo([-3.9, 1.1, 0], "NLS", BLUE, 0.66)
        self.play(imp_c.animate.shift(RIGHT * 7.8), run_time=1.5, rate_func=linear)
        self.at("Pore proteins")
        self.play(Indicate(w.rims, color=TEAL, scale_factor=1.05), run_time=0.65)
        two = DoubleArrow([-2.0, 0, 0], [2.0, 0, 0], buff=0, color=GREY,
                          stroke_width=4, tip_length=0.20)
        self.at("no direction of its own")
        self.play(Create(two), FadeOut(imp_c), run_time=0.65)
        rna = VGroup(RoundedRectangle(corner_radius=0.12, width=1.45, height=0.72,
                                      stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                      fill_opacity=0.45), T("RNA", size=28, color=TEXT, weight=BOLD))
        rna[1].move_to(rna[0])
        rna.move_to([4.4, -1.25, 0])
        other_text = label("another receptor", ORIGIN, TEXT, 28)
        other_bg = RoundedRectangle(corner_radius=0.08, width=other_text.width + 0.24,
                                    height=other_text.height + 0.14, stroke_width=0,
                                    fill_color=NUC_TINT, fill_opacity=0.98)
        other = VGroup(other_bg, other_text.move_to(other_bg)).move_to([3.9, -2.72, 0])
        path = DashedVMobject(Arrow([3.55, -1.25, 0], [-3.55, -1.25, 0], buff=0,
                                     color=GREY, stroke_width=3, tip_length=0.2), num_dashes=18)
        self.at("Most messenger")
        self.play(FadeOut(VGroup(rule, rcc, gap, two)), FadeIn(rna), FadeIn(other), Create(path), run_time=0.7)
        self.play(rna.animate.shift(LEFT * 8.0), run_time=1.7, rate_func=linear)
        self.finish()


class S12End(EndCard):
    LINE = "Ran mainly sets where cargo loads and unloads."

    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        veil = Rectangle(width=13.5, height=7.1, stroke_width=0, fill_color=BG, fill_opacity=0.48)
        line = T("IN RAN-DEPENDENT TRANSPORT,", size=34, color=TEXT, font=TITLE_FONT)
        rule = T("RAN MAINLY SETS LOADING AND UNLOADING.", size=42, color=GREEN,
                 font=TITLE_FONT, weight=BOLD)
        fit(rule, max_w=11.8)
        card = VGroup(line, rule).arrange(DOWN, buff=0.34)
        panel = RoundedRectangle(corner_radius=0.18, width=card.width + 0.65,
                                 height=card.height + 0.55, stroke_width=0,
                                 fill_color=BG, fill_opacity=0.93).move_to(card)
        self.add(w, field, veil)
        self.play(FadeIn(panel), FadeIn(card, shift=UP * 0.18), run_time=0.55)
        self.wait(2.45)
        self.play(card.animate.scale(1.025), run_time=0.5)
