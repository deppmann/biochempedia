"""Crossing the midline once: deaf until it has crossed  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the axon and its growth cone (the axon's own cell)
  RED    = Slit, the midline repellent, and every "no / blocked" mark
  YELLOW = Robo, the receptor (Robo1 and Robo2 in mice)
  PURPLE = Comm (the fly protein that keeps Robo off the surface)
  ORANGE = Robo3 (the vertebrate silencer)
  GREY   = the midline strip, the lysosome, structure and de-emphasised labels
  GOLD   = a single highlight (title rule, circling the axon)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def strip(x, y0, y1, w=0.8):
    return RoundedRectangle(corner_radius=0.15, width=w, height=y1 - y0, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.3).move_to([x, (y0 + y1) / 2, 0])


def slit_dot(x, y, r=0.13):
    return Circle(radius=r, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([x, y, 0])


def make_cone(x, y, s=1.0, color=BLUE):
    body = Circle(radius=0.3 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    fil = VGroup(*[Line(ORIGIN, 0.33 * s * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                   .shift(0.3 * s * np.array([np.cos(a), np.sin(a), 0])) for a in (-0.7, -0.25, 0.25, 0.7)])
    g = VGroup(body, fil).move_to([x, y, 0])
    g.body = body
    return g


def axon_line(x0, cone, w=8):
    return always_redraw(lambda: Line([x0, cone.body.get_center()[1], 0], cone.body.get_center(),
                                      color=BLUE, stroke_width=w))


def robo_marks(cone, s=1.0, n=3, color=YELLOW, opacity=1.0):
    c = cone.body.get_center()
    caps = VGroup()
    for a in ([-0.6, 0.0, 0.6] if n == 3 else [-0.45, 0.45]):
        p = c + 0.36 * s * np.array([np.cos(a), np.sin(a), 0])
        caps.add(RoundedRectangle(corner_radius=0.05 * s, width=0.13 * s, height=0.32 * s, stroke_width=0,
                                  fill_color=color, fill_opacity=opacity).move_to(p))
    return caps


def tag(text, mob, color, direction=UP, size=24, buff=0.4):
    t = T(text, size, color)
    t.add_updater(lambda m: m.next_to(mob.body if hasattr(mob, "body") else mob, direction, buff=buff))
    t.next_to(mob.body if hasattr(mob, "body") else mob, direction, buff=buff)
    return t


def blocked(center, size=0.3):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=RED, stroke_width=7),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=RED, stroke_width=7))


def push(a, b, color=RED, w=7):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.25, max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


class S00Title(TitleCard):
    LESSON = "Crossing the midline once"
    TITLE = "Deaf until it has crossed"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        mid = strip(0, -2.8, 2.8)
        midl = T("midline", 24, GREY).move_to([0, -3.2, 0])
        cone = make_cone(-5.7, 1.0, 1.4)
        ax = axon_line(-6.2, cone)
        lab_c = T("commissural axon", 24, BLUE).move_to([-4.4, 1.65, 0])
        self.at("An axon grows")
        self.play(FadeIn(mid), FadeIn(midl), FadeIn(cone), FadeIn(lab_c), run_time=0.7)
        self.add(ax)
        self.play(cone.animate.move_to([-1.0, 1.0, 0]), run_time=2.0, rate_func=smooth)
        self.at("It crosses")
        self.play(cone.animate.move_to([4.7, 1.0, 0]), run_time=1.4, rate_func=smooth)
        self.at("never crosses back")
        back = push([3.9, 2.0, 0], [1.3, 2.0, 0], RED)
        x = blocked([2.6, 2.0, 0], 0.3)
        self.play(GrowArrow(back), run_time=0.5)
        self.play(Create(x), run_time=0.4)

        cone2 = make_cone(-5.7, -1.2, 1.4)
        ax2 = axon_line(-6.2, cone2)
        lab_i = T("neighbour axon", 24, BLUE).move_to([-4.4, -0.55, 0])
        self.at("stay on their own side")
        self.play(FadeIn(cone2), FadeIn(lab_i), run_time=0.5)
        self.add(ax2)
        self.play(cone2.animate.move_to([-1.1, -1.2, 0]), run_time=1.8, rate_func=smooth)
        self.at("The midline did not change")
        self.play(Indicate(mid, color=TEXT, scale_factor=1.06), run_time=1.2)
        q = T("?", 80, TEXT, weight=BOLD).move_to([5.75, 1.15, 0])
        self.at("So what changed")
        self.play(FadeIn(q, scale=1.5), run_time=0.5)
        self.at("The change has to be")
        grp = VGroup(ax, cone)
        self.play(Circumscribe(grp, color=GOLD, time_width=1.0, stroke_width=6), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Slit(SpokenScene):
    def construct(self):
        mid = strip(0, -2.8, 2.8)
        dots = VGroup(*[slit_dot(sx * 0.6, y) for sx in (-1, 1) for y in (-1.9, -1.0, 1.0, 1.9)])
        self.at("The midline holds")
        self.play(FadeIn(mid), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.08), run_time=0.9)
        slit_l = T("Slit", 30, RED, weight=BOLD).move_to([0, 3.2, 0])
        self.at("called Slit")
        self.play(FadeIn(slit_l, shift=DOWN * 0.15), run_time=0.4)

        cone = make_cone(-4.6, 1.5, 1.4)
        ax = axon_line(-6.3, cone)
        self.at("The axon carries a receptor")
        self.play(FadeIn(cone), run_time=0.5)
        self.add(ax)
        rb = robo_marks(cone, 1.4)
        rl = tag("Robo", cone, YELLOW, DOWN, 26, 0.55)
        self.at("called Robo")
        self.play(FadeIn(rb, scale=1.4), FadeIn(rl), run_time=0.5)
        cone.add(rb)
        self.at("When Slit binds Robo")
        self.play(cone.animate.move_to([-1.7, 1.5, 0]), run_time=1.4, rate_func=smooth)
        rep = push([-0.5, 2.55, 0], [-2.0, 2.55, 0], RED)
        self.play(GrowArrow(rep), Indicate(dots, color=RED, scale_factor=1.5), run_time=0.7)
        self.at("the growth cone retreats")
        self.play(cone.animate.move_to([-4.2, 1.5, 0]), FadeOut(rep), run_time=1.4, rate_func=smooth)
        lab_n = T("never cross", 24, GREY).move_to([-5.2, 2.2, 0])
        self.at("Axons that never cross")
        self.play(FadeIn(lab_n), run_time=0.4)
        self.at("carry Robo from the start")
        self.play(Indicate(rb, color=YELLOW, scale_factor=1.6), run_time=1.0)

        cone2 = make_cone(-4.6, -1.5, 1.4)
        ax2 = axon_line(-6.3, cone2)
        lab_d = T("do cross", 24, GREY).move_to([-5.2, -0.8, 0])
        self.at("Axons that do cross")
        self.play(FadeOut(rl), FadeIn(cone2), FadeIn(lab_d), run_time=0.5)
        self.add(ax2)
        self.play(cone2.animate.move_to([3.6, -1.5, 0]), run_time=2.6, rate_func=smooth)
        rb2 = robo_marks(cone2, 1.4)
        rl2 = tag("Robo", cone2, YELLOW, DOWN, 26, 0.55)
        self.at("only after they have crossed")
        self.play(FadeIn(rb2, scale=1.4), FadeIn(rl2), run_time=0.5)
        ln = Line([-6.2, -2.35, 0], [-0.7, -2.35, 0], color=GREY, stroke_width=4)
        deaf = T("deaf to Slit", 26, GREY).move_to([-3.4, -2.85, 0])
        self.at("deaf to Slit")
        self.play(Create(ln), FadeIn(deaf), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ladder(kind, cx, cy=0.6, h=4.0, w=1.5):
    g = VGroup()
    top, bot = cy + h / 2, cy - h / 2
    for dx in (-w / 2, w / 2):
        g.add(Line([cx + dx, bot, 0], [cx + dx, top, 0], color=BLUE, stroke_width=6))
    seg = h / 3
    for i in range(3):
        y0 = bot + i * seg
        if kind in ("normal",):
            for f in (0.3, 0.7):
                g.add(Line([cx - w / 2, y0 + f * seg, 0], [cx + w / 2, y0 + f * seg, 0], color=BLUE, stroke_width=4))
        elif kind == "robo":
            for f in (0.15, 0.4, 0.65, 0.9):
                g.add(Line([cx - w / 2, y0 + f * seg, 0], [cx + w / 2, y0 + f * seg, 0], color=BLUE, stroke_width=4))
            g.add(Line([cx - w / 2, y0 + 0.15 * seg, 0], [cx + w / 2, y0 + 0.65 * seg, 0], color=BLUE, stroke_width=3))
            g.add(Line([cx + w / 2, y0 + 0.4 * seg, 0], [cx - w / 2, y0 + 0.9 * seg, 0], color=BLUE, stroke_width=3))
    return g


class S03Fly(SpokenScene):
    def construct(self):
        xs = [-4.65, -1.55, 1.55, 4.65]

        def lab(text, x, slant=True):
            return T(text, 24, TEXT, slant=ITALIC if slant else NORMAL).move_to([x, -1.75, 0])

        l_norm, l_comm, l_robo, l_both = lab("normal", xs[0], False), lab("comm", xs[1]), lab("robo", xs[2]), lab("robo and comm", xs[3])
        l_both.shift(DOWN * 0)
        self.at("Its nerve cord looks like a ladder")
        norm = ladder("normal", xs[0])
        self.play(LaggedStart(*[Create(m) for m in norm], lag_ratio=0.05), FadeIn(l_norm), run_time=1.6)
        self.at("Lose Robo")
        robo = ladder("robo", xs[2])
        self.play(LaggedStart(*[Create(m) for m in robo], lag_ratio=0.03), FadeIn(l_robo), run_time=1.6)
        self.at("some cross back")
        self.play(Indicate(robo, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("Lose a protein")
        comm = ladder("comm", xs[1])
        self.play(LaggedStart(*[Create(m) for m in comm], lag_ratio=0.05), FadeIn(l_comm), run_time=1.2)
        self.at("almost no axon crosses")
        self.play(Indicate(comm, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("Lose both")
        both = ladder("robo", xs[3])
        self.play(LaggedStart(*[Create(m) for m in both], lag_ratio=0.03), FadeIn(l_both), run_time=1.4)
        eq = T("=", 48, TEXT, weight=BOLD).move_to([3.1, 0.6, 0])
        self.at("looks like the Robo mutant")
        self.play(FadeIn(eq, scale=1.4), Indicate(robo, color=BLUE, scale_factor=1.04),
                  Indicate(both, color=BLUE, scale_factor=1.04), run_time=1.0)
        c = bchip("Comm", PURPLE, 28).move_to([-1.9, -3.0, 0])
        r = bchip("Robo", YELLOW, 28).move_to([1.9, -3.0, 0])
        inh = Line([-1.0, -3.0, 0], [0.95, -3.0, 0], color=PURPLE, stroke_width=6)
        bar = Line([0.95, -2.75, 0], [0.95, -3.25, 0], color=PURPLE, stroke_width=8)
        self.at("works by lowering")
        self.play(FadeIn(c, shift=RIGHT * 0.2), Create(inh), Create(bar), FadeIn(r), run_time=1.0)
        self.at("Once Robo is gone")
        self.play(FadeOut(r), FadeOut(bar), FadeOut(inh), run_time=0.6)
        self.play(Indicate(c, color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Comm(SpokenScene):
    def construct(self):
        soma = Circle(radius=1.7, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to([-4.6, 0.3, 0])
        mid = strip(1.4, -1.9, 2.3, 0.7)
        midl = T("midline", 24, GREY).move_to([1.4, -2.35, 0])
        cone = make_cone(-2.0, 0.3)
        ax = axon_line(-2.9, cone)
        sdots = VGroup(*[slit_dot(1.4 + sx * 0.55, y) for sx in (-1, 1) for y in (-1.3, 1.8)])
        lyso = Circle(radius=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([-4.9, -0.3, 0])
        lyl = T("lysosome", 22, GREY).move_to([-4.6, -1.0, 0])
        road = DashedLine([-4.1, 0.3, 0], [-2.9, 0.3, 0], color=GREY, stroke_width=5)
        self.add(soma, mid, midl, sdots, cone, ax, lyso, lyl, road)
        self.wait(0.01)
        comm = bchip("Comm", PURPLE, 26).move_to([-4.0, 1.3, 0])
        self.at("works inside the commissural")
        self.play(FadeIn(comm, scale=1.2), run_time=0.6)
        bar = Line([-5.2, 2.75, 0], [2.4, 2.75, 0], color=PURPLE, stroke_width=8)
        bl = T("Comm is made", 24, PURPLE).move_to([-1.4, 3.2, 0])
        self.at("made for a short time")
        self.play(Create(bar), FadeIn(bl), run_time=1.6)
        dots = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-5.8, y, 0])
                        for y in (0.45, 0.05, -0.35)])
        rl = T("Robo", 24, YELLOW).next_to(dots, UP, buff=0.15).shift(LEFT * 0.0)
        rl.move_to([-5.55, 0.95, 0])
        self.at("It meets newly made Robo")
        self.play(FadeIn(dots, scale=1.5), FadeIn(rl), run_time=0.6)
        self.at("diverts it")
        x = blocked([-3.5, 0.3, 0], 0.25)
        self.play(Create(x), FadeOut(rl), run_time=0.4)
        self.play(*[d.animate.move_to(lyso.get_center() + o) for d, o in zip(dots, ([0.0, 0.0, 0], [0.12, 0.1, 0], [-0.12, 0.05, 0]))],
                  run_time=1.0)
        self.at("late endosomes")
        self.play(dots.animate.scale(0.1).set_opacity(0), lyso.animate.set_fill(RED, 0.35), run_time=0.9)
        note = T("a model: parts are still debated", 24, GREY).move_to([3.7, -3.1, 0])
        self.at("Parts of this model")
        self.play(FadeIn(note), run_time=0.5)
        self.at("The axon crosses")
        self.play(cone.animate.move_to([4.4, 0.3, 0]), run_time=2.0, rate_func=smooth)
        self.at("Then the neuron stops")
        self.play(FadeOut(bar), FadeOut(bl), FadeOut(comm), FadeOut(x), FadeOut(note), run_time=0.7)
        flow = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-4.6 + 0.0 * i, 0.3 + (i - 1) * 0.0, 0])
                        for i in range(3)])
        self.at("Robo reaches the growth cone")
        self.add(flow)
        self.play(LaggedStart(*[m.animate.move_to([4.2, 0.3, 0]) for m in flow], lag_ratio=0.25), run_time=1.5, rate_func=linear)
        rb = robo_marks(cone)
        self.play(FadeOut(flow), FadeIn(rb, scale=1.4), run_time=0.4)
        cone.add(rb)
        sl = T("Slit", 28, RED, weight=BOLD).move_to([2.7, 1.8, 0])
        rep = push([2.2, 0.95, 0], [3.7, 0.95, 0], RED)
        self.at("now repels it")
        self.play(FadeIn(sl), GrowArrow(rep), run_time=0.5)
        self.play(cone.animate.shift(RIGHT * 0.7), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Robo3(SpokenScene):
    def construct(self):
        mid = strip(0, -2.0, 2.0)
        dots = VGroup(*[slit_dot(sx * 0.6, y) for sx in (-1, 1) for y in (-1.7, -1.1, 1.1, 1.7)])
        self.add(mid, dots)
        cm = bchip("Comm", PURPLE, 28).move_to([-4.9, 2.8, 0])
        none = T("no vertebrate Comm found", 24, GREY).move_to([-1.85, 2.8, 0])
        self.at("No vertebrate")
        self.play(FadeIn(cm), FadeIn(none), run_time=0.5)
        xx = blocked(cm.get_center(), 0.3)
        self.play(Create(xx), run_time=0.4)
        S = 1.8
        cone = make_cone(-4.4, 0.0, S)
        ax = axon_line(-6.3, cone, 10)
        self.at("Mice use another protein")
        self.play(FadeOut(VGroup(cm, none, xx)), FadeIn(cone), run_time=0.6)
        self.add(ax)
        c0 = cone.body.get_center()
        cover = RoundedRectangle(corner_radius=0.14, width=0.4, height=1.5, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.3).move_to(c0 + [0.62, 0, 0])
        cl = tag("Robo3", cone, ORANGE, UP, 26, 0.85)
        self.at("commissural axons before they cross")
        self.play(FadeIn(cover, scale=1.3), FadeIn(cl), run_time=0.6)
        cone.add(cover)
        rb = robo_marks(cone, S, 2)
        for m in rb:
            m.shift(LEFT * 0.0)
        rl = tag("Robo1  Robo2", cone, YELLOW, DOWN, 24, 0.95)
        self.at("It blunts how")
        self.play(FadeIn(rb, scale=1.3), FadeIn(rl), run_time=0.6)
        cone.add(rb)
        sl = T("Slit", 28, RED, weight=BOLD).move_to([0, 2.5, 0])
        self.at("respond to Slit")
        self.play(FadeIn(sl), Indicate(dots, color=RED, scale_factor=1.5), run_time=0.7)
        self.at("while they stay in the membrane")
        self.play(cone.animate.move_to([4.0, 0.0, 0]), run_time=2.6, rate_func=smooth)
        self.at("largely disappears")
        self.play(FadeOut(cover), FadeOut(cl), run_time=0.9)
        cone.remove(cover)
        rep = push([0.6, 0.0, 0], [2.3, 0.0, 0], RED)
        self.at("free to respond")
        self.play(GrowArrow(rep), Indicate(rb, color=YELLOW, scale_factor=1.7), run_time=0.7)
        self.play(cone.animate.shift(RIGHT * 0.5), FadeOut(rep), run_time=0.8)
        c = chip("Comm destroys the receptor", PURPLE, 24).move_to([-3.3, -3.05, 0])
        v = chip("Robo3 silences it", ORANGE, 24).move_to([3.3, -3.05, 0])
        self.at("Comm destroys")
        self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)
        self.at("silences it")
        self.play(FadeIn(v, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        mid = strip(0, -1.6, 2.2, 0.7)
        cone = make_cone(-5.0, 0.3, 1.0)
        ax = axon_line(-6.3, cone)
        dim_rb = robo_marks(cone, 1.0, 3, YELLOW, 0.25)
        cone.add(dim_rb)
        self.at("Both routes")
        self.play(FadeIn(mid), FadeIn(cone), run_time=0.6)
        self.add(ax)
        self.play(cone.animate.move_to([-1.3, 0.3, 0]), run_time=1.6, rate_func=smooth)
        deaf = T("deaf to Slit", 30, GREY, weight=BOLD).move_to([-3.2, 1.9, 0])
        self.at("deaf to Slit before crossing")
        self.play(FadeIn(deaf), run_time=0.5)
        self.play(cone.animate.move_to([4.0, 0.3, 0]), run_time=1.6, rate_func=smooth)
        resp = T("responsive", 30, YELLOW, weight=BOLD).move_to([3.4, 1.9, 0])
        self.at("responsive after")
        self.play(FadeIn(resp), dim_rb.animate.set_fill(YELLOW, 1.0), run_time=0.6)
        self.wait(0.5)
        self.at("So you can predict")
        self.play(FadeOut(VGroup(mid, cone, ax, deaf, resp)), run_time=0.7)
        self.remove(ax)

        q1 = chip("Is Slit there?", RED, 26).move_to([-3.4, 1.9, 0])
        q2 = chip("Can the axon hear it?", YELLOW, 26).move_to([-3.4, 0.25, 0])
        q3 = chip("When does it start hearing?", BLUE, 26).move_to([-3.4, -1.4, 0])
        self.at("Is Slit there")
        self.play(FadeIn(q1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Can the axon hear it")
        self.play(FadeIn(q2, shift=RIGHT * 0.2), run_time=0.5)
        self.at("And when does it start hearing")
        self.play(FadeIn(q3, shift=RIGHT * 0.2), run_time=0.5)

        # panel A: hears too early
        mA = strip(4.4, 0.5, 2.7, 0.6)
        coneA = make_cone(1.3, 1.6, 0.9)
        axA = axon_line(0.9, coneA, 7)
        rbA = robo_marks(coneA, 0.9)
        coneA.add(rbA)
        capA = T("hears too early: never crosses", 22, TEXT).move_to([3.4, 0.1, 0])
        self.at("An axon that hears Slit too early")
        self.play(FadeIn(mA), FadeIn(coneA), run_time=0.4)
        self.add(axA)
        self.play(coneA.animate.move_to([3.3, 1.6, 0]), run_time=1.0)
        xA = blocked([3.85, 1.6, 0], 0.18)
        self.play(Create(xA), FadeIn(capA), run_time=0.5)
        # panel B: never hears
        mB = strip(4.4, -2.8, -0.7, 0.6)
        coneB = make_cone(1.3, -1.75, 0.9)
        axB = axon_line(0.9, coneB, 7)
        capB = T("never hears it: crosses again", 22, TEXT).move_to([3.4, -3.2, 0])
        self.at("One that never hears it")
        self.play(FadeIn(mB), FadeIn(coneB), run_time=0.4)
        self.add(axB)
        self.play(coneB.animate.move_to([5.7, -1.75, 0]), run_time=1.2)
        self.play(coneB.animate.move_to([3.2, -1.75, 0]), FadeIn(capB), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Is Slit there? Can the axon hear it? And when?"
