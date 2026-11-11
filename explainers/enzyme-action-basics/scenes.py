"""Lower the Ridge, Not the Valleys — enzyme-action-basics teaching film.

All energy profiles in this film are computed from the function specified in
script.json.  The picture is explicitly schematic; no molecular structures are
drawn.

COLOR MAP
    YELLOW  substrate / forward trip
    GREEN   product / reverse trip / thermodynamic difference
    RED     uncatalysed pass / activation barrier / impossible push
    TEAL    enzyme / catalysed pass
    PURPLE  transition state
    GOLD    active-site contacts / binding energy
"""
from bp_style import *
import numpy as np


PURPLE = "#B58CF0"
X0, X1 = -6.2, 6.2
Y_SCALE, Y_SHIFT = 1.08, -0.55


def energy_y(x, height=4.2, reverse=False):
    """Computed energy profile, affinely mapped to fill the teaching frame."""
    step = -1.3 - 0.7 * np.tanh(x / 1.6)
    if reverse:
        step = -1.3 + 0.7 * np.tanh(x / 1.6)
    raw = step + height * np.exp(-((x / 1.1) ** 2))
    return Y_SCALE * raw + Y_SHIFT


def profile(height=4.2, color=RED, width=6, reverse=False, x0=X0, x1=X1):
    return ParametricFunction(
        lambda x: np.array([x, energy_y(x, height, reverse), 0]),
        t_range=[x0, x1, 0.025], color=color, stroke_width=width,
    )


def dashed_profile(height=4.2, color=RED, width=4, reverse=False):
    return DashedVMobject(profile(height, color, width, reverse), num_dashes=42)


def peak_x(height=4.2, reverse=False):
    xs = np.linspace(X0, X1, 4001)
    return float(xs[np.argmax([energy_y(x, height, reverse) for x in xs])])


def peak_point(height=4.2, reverse=False):
    x = peak_x(height, reverse)
    return np.array([x, energy_y(x, height, reverse), 0])


def schematic_tag():
    return T("schematic", 28, TEXT).move_to([5.25, -3.42, 0])


def ground_fill(height=4.2, reverse=False, opacity=.18):
    return Polygon(
        *[np.array([x, energy_y(x, height, reverse), 0]) for x in np.linspace(X0, X1, 180)],
        [X1, -3.42, 0], [X0, -3.42, 0], stroke_width=0,
        fill_color=GREY, fill_opacity=opacity,
    )


def landscape(height=4.2, color=RED, dashed=False, reverse=False, tag=True):
    curve = dashed_profile(height, color, 4, reverse) if dashed else profile(height, color, 6, reverse)
    ground = ground_fill(height, reverse, .22)
    parts = VGroup(ground, curve)
    if tag:
        parts.add(schematic_tag())
    return parts


def power_text(prefix="", base="10", exponent="17", color=TEAL, size=34):
    """Plain-text scientific notation with a real raised exponent (no caret glyph)."""
    lead = M(prefix + base, size, color)
    exp = M(exponent, int(size * .62), color).next_to(lead, UR, buff=.03).shift(DOWN * .03)
    return VGroup(lead, exp)


def counter_chip():
    label = VGroup(T("speed-up about", 30, TEAL), power_text(size=32)).arrange(RIGHT, buff=.18)
    box = RoundedRectangle(corner_radius=.14, width=label.width + .42, height=label.height + .34,
                           stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=.16)
    return VGroup(box, label.move_to(box)).scale(.88).move_to([4.55, 3.18, 0])


def question_chips():
    a = chip("which way?", GREEN, 28, fill_opacity=0.05)
    b = chip("how fast?", RED, 28, fill_opacity=0.05)
    return VGroup(a, b).arrange(RIGHT, buff=0.28).move_to([-3.75, 3.25, 0])


def valley_dots(n=8, side="left", color=None, height=4.2, reverse=False, moving=True):
    """Small living particles, constrained to the selected valley floor."""
    if color is None:
        color = YELLOW if side == "left" else GREEN
    xs = np.linspace(-5.5, -2.35, n) if side == "left" else np.linspace(2.35, 5.5, n)
    g = VGroup()
    for i, x in enumerate(xs):
        d = Dot(radius=0.15, color=color)
        phase = i * 0.83
        base_x = float(x)
        if moving:
            clock = [0.0]
            def drift(m, dt, bx=base_x, ph=phase, tm=clock):
                tm[0] += dt
                xx = bx + 0.18 * np.sin(1.45 * tm[0] + ph)
                m.move_to([xx, energy_y(xx, height, reverse)
                           + 0.19 + 0.11 * np.sin(2.1 * tm[0] + ph), 0])
            d.add_updater(drift)
        else:
            d.move_to([base_x, energy_y(base_x, height, reverse) + 0.16, 0])
        g.add(d)
    return g


def crossing_path(height=1.8, reverse=False, lift=.22):
    a, b = (5.35, -5.35) if reverse else (-5.35, 5.35)
    path = VMobject()
    path.set_points_smoothly([
        np.array([x, energy_y(x, height, reverse) + lift, 0])
        for x in np.linspace(a, b, 140)
    ])
    return path


def stream_animation(dots, height=1.8, reverse=False, run_time=2.5):
    """Staggered, visible crossings that occupy the whole sentence."""
    anims = []
    for i, d in enumerate(dots):
        anims.append(Succession(Wait(i * .18), MoveAlongPath(d, crossing_path(height, reverse),
                                                             rate_func=linear), Wait((len(dots)-i-1)*.18)))
    return AnimationGroup(*anims, lag_ratio=0, run_time=run_time)


def moving_dot(height=1.8, color=YELLOW, start=-5.3):
    tr = ValueTracker(start)
    dot = Dot(radius=0.15, color=color)
    dot.add_updater(lambda m: m.move_to([tr.get_value(), energy_y(tr.get_value(), height) + 0.17, 0]))
    return tr, dot


def route_arrow(a, b, color, height=1.8, reverse=False):
    xs = np.linspace(a, b, 80)
    path = VMobject(color=color, stroke_width=7)
    path.set_points_smoothly([np.array([x, energy_y(x, height, reverse) + 0.22, 0]) for x in xs])
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12)
    tip.rotate(-PI / 2 if b > a else PI / 2).move_to(path.get_end())
    return VGroup(path, tip)


def vbracket(x, y0, y1, color, label=None, dx=0.52):
    arr = DoubleArrow([x, y0, 0], [x, y1, 0], buff=0, color=color,
                      stroke_width=4, tip_length=0.17)
    g = VGroup(arr)
    if label:
        g.add(M(label, 34, color).move_to([x + dx, (y0 + y1) / 2, 0]))
    return g


def pin(point, color=TEAL):
    return VGroup(Line(point + UP * 0.35, point, color=color, stroke_width=5),
                  Dot(point, radius=0.09, color=color))


def cup(center=ORIGIN, scale=1.0):
    """Abstract active-site cleft: a cartoon protein block, never a molecule."""
    c = Arc(radius=1.65, start_angle=PI * 0.08, angle=PI * 0.84,
            color=TEAL, stroke_width=22).rotate(PI).scale(scale).move_to(center)
    return c


def contacts(center=ORIGIN, n=8, scale=1.0):
    g = VGroup()
    for ang in np.linspace(0.16 * PI, 0.84 * PI, n):
        p = center + scale * np.array([1.22 * np.cos(ang), -0.72 + 0.92 * np.sin(ang), 0])
        q = center + scale * np.array([0.94 * np.cos(ang), -0.72 + 0.64 * np.sin(ang), 0])
        g.add(Line(p, q, color=GOLD, stroke_width=5))
    return g


def ts_oval(center=ORIGIN, scale=1.0):
    return Ellipse(width=2.05 * scale, height=0.78 * scale, color=PURPLE,
                   fill_color=PURPLE, fill_opacity=0.34, stroke_width=5).move_to(center)


def breathing_grip(cup_mob):
    """Keep the active-site grip visibly flexing while its energetic effect is explained."""
    clock = [0.0]
    base_w = cup_mob.width
    def flex(m, dt):
        clock[0] += dt
        m.stretch_to_fit_width(base_w * (1 + .055 * np.sin(5.2 * clock[0])))
    cup_mob.add_updater(flex)
    return cup_mob


class S00Hook(SpokenScene):
    def construct(self):
        land = landscape()
        dots = valley_dots()
        self.add(land, dots)

        self.at("impossible reaction")
        uphill = CurvedArrow([4.7, -1.75, 0], [-2.0, 0.2, 0], angle=-0.35,
                             color=RED, stroke_width=7)
        badge1 = chip("?", RED, 40).scale(0.72).move_to([0.9, 0.0, 0])
        self.play(Create(uphill), run_time=0.9)
        self.play(FadeIn(badge1, scale=0.6), run_time=0.35)

        self.at("possible one fast")
        downhill = route_arrow(-5.0, 5.0, YELLOW, 4.2)
        badge2 = chip("?", TEAL, 40).scale(0.72).move_to([1.25, 2.45, 0])
        self.play(Create(downhill[0]), FadeIn(downhill[1]), run_time=1.0)
        self.play(FadeIn(badge2, scale=0.6), run_time=0.35)

        self.at("Start with a reaction")
        step = chip("one step toward RNA", YELLOW, 30).move_to([-3.9, 0.25, 0])
        self.play(FadeOut(VGroup(uphill, badge1, downhill, badge2)), FadeIn(step, shift=DOWN * 0.2), run_time=0.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        land = landscape()
        land[0].set_fill(opacity=.055)
        land[1].set_stroke(opacity=.25)
        land[2].set_opacity(.25)
        dots = valley_dots().set_opacity(0.25)
        self.add(land, dots)
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD)
        title = T("Lower the Ridge, Not the Valleys", 50, font=TITLE_FONT)
        fit(title, 11.4)
        rule = Line(LEFT * 1.35, RIGHT * 1.35, color=GOLD, stroke_width=4)
        card = VGroup(brand, title, rule).arrange(DOWN, buff=0.34)
        self.play(FadeIn(brand), Write(title), GrowFromCenter(rule), run_time=0.9)
        self.wait(0.7)
        self.play(FadeOut(card), land[0].animate.set_fill(opacity=.22),
                  land[1].animate.set_stroke(opacity=1), land[2].animate.set_opacity(1),
                  dots.animate.set_opacity(1), run_time=0.4)
        self.finish()


class S02Slow(SpokenScene):
    def construct(self):
        world = VGroup(landscape(tag=False), valley_dots()).scale(0.67).shift(UP * 1.72)
        timeline_tag = T("schematic", 28, TEXT).move_to([5.25, -.92, 0])
        self.add(world, timeline_tag)
        axis_y, xa, xb = -2.72, -5.45, 5.45
        axis = Arrow([xa, axis_y, 0], [xb, axis_y, 0], buff=0, color=TEXT, stroke_width=4)
        def xpos(seconds):
            return xa + (np.log10(seconds) + 3) / 19 * (xb - xa)
        ticks = VGroup()
        for power in range(-3, 17, 3):
            x = xpos(10 ** power)
            ticks.add(Line([x, axis_y - .12, 0], [x, axis_y + .12, 0], color=TEXT, stroke_width=3))
        labels = VGroup(T("a second", 28).move_to([xpos(1), -3.25, 0]),
                        T("a year", 28).move_to([xpos(3.156e7), -3.25, 0]),
                        T("a million years", 28).move_to([xpos(3.156e13), -3.25, 0]))
        self.play(Create(axis), Create(ticks), FadeIn(labels), run_time=1.4)
        scanner = Line([xa, -1.82, 0], [xa, -3.42, 0], color=TEAL, stroke_width=10).set_opacity(.55)
        self.add(scanner)
        self.play(scanner.animate.move_to([xpos(3.156e7), -2.62, 0]), run_time=2.05, rate_func=linear)
        self.remove(scanner)

        self.at("Half the molecules")
        half_s = 78e6 * 3.156e7
        marker = Dot([xa, axis_y, 0], radius=0.13, color=RED)
        half_label = T("half-life: 78 million years", 30, RED).move_to([2.35, -2.08, 0])
        blink = world[1][:4]
        self.add(marker)
        self.play(marker.animate.move_to([xpos(half_s), axis_y, 0]),
                  blink.animate.set_opacity(0.18), run_time=2.0, rate_func=rate_functions.ease_out_cubic)
        self.play(FadeIn(half_label), blink.animate.set_opacity(1), run_time=0.45)

        self.at("With its enzyme")
        em = Dot([xpos(1e-2), axis_y, 0], radius=0.13, color=TEAL)
        el = T("with enzyme: milliseconds", 30, TEAL).move_to([-2.85, -2.08, 0])
        gap = DoubleArrow([xpos(1e-2), axis_y + .35, 0], [xpos(half_s), axis_y + .35, 0],
                          buff=0, color=TEAL, stroke_width=4, tip_length=.16)
        self.play(FadeIn(em, shift=UP * .3), FadeIn(el), GrowFromCenter(gap), run_time=0.9)
        self.finish()


class S03Split(SpokenScene):
    def construct(self):
        land = landscape()
        dots = valley_dots()
        self.add(land, dots)
        self.at("speedup of about")
        count = counter_chip()
        self.play(FadeIn(count, shift=UP * .25), run_time=.7)
        self.at("push a reaction uphill")
        tr, dot = moving_dot(4.2, YELLOW, 4.8)
        self.add(dot)
        self.play(FadeOut(count), tr.animate.set_value(1.0), run_time=1.05, rate_func=rate_functions.ease_out_quad)
        self.play(tr.animate.set_value(4.8), run_time=.65, rate_func=rate_functions.ease_in_quad)
        self.play(tr.animate.set_value(1.25), run_time=.65, rate_func=rate_functions.ease_out_quad)
        self.at("No")
        cross = VGroup(Line([-.35,.35,0],[.35,-.35,0],color=RED,stroke_width=9),
                       Line([-.35,-.35,0],[.35,.35,0],color=RED,stroke_width=9)).move_to([1.1,-.15,0])
        self.play(Create(cross), tr.animate.set_value(4.8), run_time=.55)
        self.at("split one question")
        qs = question_chips()
        self.play(FadeOut(VGroup(dot, cross)), FadeIn(qs, shift=DOWN * .2), run_time=.75)
        self.finish()


class S04Valleys(SpokenScene):
    def construct(self):
        land, dots, qs = landscape(), valley_dots(), question_chips()
        self.add(land, dots, qs)
        yl, yr = energy_y(-5.2), energy_y(5.2)
        left = T("substrate", 30, YELLOW).move_to([-4.65, yl + .55, 0])
        right = T("product", 30, GREEN).move_to([4.75, yr + .55, 0])
        self.play(Indicate(land[1], color=YELLOW, scale_factor=1.01), FadeIn(left), FadeIn(right), run_time=.8)
        self.at("thermodynamics")
        dg = vbracket(5.55, yr, yl, GREEN)
        self.play(GrowFromCenter(dg), qs[0][0].animate.set_fill(GREEN, opacity=.18), run_time=.6)
        self.at("delta G")
        dgl = M("ΔG", 34, GREEN).move_to([6.02, (yl + yr) / 2, 0])
        self.play(FadeIn(dgl), run_time=.35)
        self.at("How high the ridge")
        peak = peak_point()
        barrier = vbracket(-.7, yl, peak[1], RED)
        self.play(GrowFromCenter(barrier), run_time=.65)
        self.at("how fast")
        self.play(qs[1][0].animate.set_fill(RED, opacity=.18), run_time=.4)
        self.play(FadeOut(qs), run_time=.35)
        self.finish()


class S05Top(SpokenScene):
    def construct(self):
        land, dots = landscape(), valley_dots()
        self.add(land, dots)
        peak = peak_point()
        br = vbracket(-.75, energy_y(-5.2), peak[1], RED)
        self.add(br)
        self.at("activation energy")
        lab = M("ΔG‡", 34, RED).move_to([-.12, .75, 0])
        self.play(FadeIn(lab), run_time=.45)
        self.at("very top")
        # Recompute a bounded close-up instead of scaling the full curve beyond the frame.
        close_curve = ParametricFunction(
            lambda x: np.array([2.35 * x, energy_y(x, 4.2) - .15, 0]),
            t_range=[-2.75, 2.75, .02], color=RED, stroke_width=7,
        )
        close_dots = VGroup(*[
            Dot([x, energy_y(x / 2.35, 4.2) + .04, 0], radius=.15, color=YELLOW)
            for x in np.linspace(-6.0, -4.9, 5)
        ])
        self.play(FadeOut(VGroup(land, dots, br, lab)), FadeIn(close_curve), FadeIn(close_dots), run_time=.65)
        p = np.array([2.35 * peak[0], peak[1] - .15, 0])
        ball = Dot([-4.65, energy_y(-4.65 / 2.35, 4.2) + .04, 0], radius=.18, color=YELLOW)
        oval = ts_oval(p, .55)
        climb = VMobject().set_points_smoothly([
            np.array([2.35*x, energy_y(x, 4.2) + .04, 0]) for x in np.linspace(-2.0, peak[0], 70)
        ])
        self.play(FadeIn(ball), MoveAlongPath(ball, climb), run_time=.75, rate_func=smooth)
        self.play(ReplacementTransform(ball, oval), run_time=.25)
        self.at("transition state")
        tl = T("transition state", 30, PURPLE).next_to(oval, UP, .22)
        self.play(FadeIn(tl), run_time=.35)
        self.at("bonds are partly")
        b1 = chip("bond breaking", PURPLE, 28).scale(.75).next_to(oval, LEFT, .3)
        b2 = chip("bond forming", PURPLE, 28).scale(.75).next_to(oval, RIGHT, .3)
        self.play(oval.animate.stretch(1.22, 0), FadeIn(b1), FadeIn(b2), run_time=.55)
        self.at("femtoseconds")
        green = Dot([5.4, energy_y(5.4 / 2.35) + .04, 0], radius=.18, color=GREEN)
        self.play(Wiggle(oval, scale_value=1.08), run_time=.45)
        self.play(FadeOut(VGroup(b1,b2,tl)), ReplacementTransform(oval, green), run_time=.6)
        whole = landscape()
        whole_dots = valley_dots()
        self.play(FadeOut(VGroup(close_curve, close_dots, green)), FadeIn(whole), FadeIn(whole_dots), run_time=.55)
        self.finish()


class S06Idea(SpokenScene):
    def construct(self):
        old = dashed_profile(4.2, RED)
        fill = landscape(4.2, RED)
        dots = valley_dots()
        self.add(fill, dots)
        self.at("whole idea")
        self.play(Transform(fill[1], old), run_time=.55)
        h = ValueTracker(4.2)
        low = always_redraw(lambda: profile(h.get_value(), TEAL, 7))
        self.add(low)
        self.at("lowers the ridge")
        self.play(h.animate.set_value(1.8), run_time=1.25, rate_func=smooth)
        yl, yr = energy_y(-5.2, 1.8), energy_y(5.2, 1.8)
        self.at("never moves the valleys")
        pins = VGroup(pin(np.array([-5.2, yl, 0])), pin(np.array([5.2, yr, 0])))
        self.play(FadeIn(pins, shift=DOWN*.25), Flash([-5.2,yl,0], color=TEAL), Flash([5.2,yr,0], color=TEAL), run_time=.65)
        runners = VGroup(*[Dot(radius=.16, color=YELLOW) for _ in range(4)])
        self.add(runners)
        self.play(stream_animation(runners, run_time=1.75), run_time=1.75)
        self.at("a lower pass")
        pp = peak_point(1.8)
        ll = T("lower pass", 30, TEAL).next_to(pp, UP, .25)
        self.play(FadeIn(ll, shift=DOWN*.15), run_time=.4)
        self.at("still a highest point")
        top = Dot(pp, radius=.14, color=PURPLE)
        tr, traveler = moving_dot(1.8)
        self.play(FadeIn(top), FadeIn(traveler), run_time=.3)
        self.play(tr.animate.set_value(5.25), run_time=1.1, rate_func=linear)
        self.remove(runners)
        self.finish()


class S07Rate(SpokenScene):
    def construct(self):
        # Match the carried landscape exactly: full-width profiles, unchanged
        # valley floors, and the lowered TEAL ridge from the end of s06.
        old = dashed_profile(4.2, RED)
        h = ValueTracker(1.8)
        low = always_redraw(lambda: profile(h.get_value(), TEAL, 7))
        dots = valley_dots()
        ground = ground_fill(4.2)
        self.add(ground, old, low, dots, schematic_tag())

        # The previous scene finishes at H=1.8. Briefly restore the comparison
        # baseline without moving any other part of the landscape.
        self.play(h.animate.set_value(4.2), run_time=.42, rate_func=smooth)

        bar = RoundedRectangle(width=.78, height=2.45, corner_radius=.12,
                               stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=.06).move_to([5.42,.18,0])

        def gauge_fill():
            drop_fraction = np.clip((4.2 - h.get_value()) / 2.0, 0, 1)
            fill_height = max(.001, 2.15 * drop_fraction)
            return Rectangle(
                width=.60, height=fill_height, stroke_width=0,
                fill_color=TEAL, fill_opacity=.78,
            ).move_to([bar.get_x(), bar.get_bottom()[1] + .14 + fill_height / 2, 0])

        labels = ["×1", "×10", "×100", "×1,000", "×10,000", "×100,000"]

        def gauge_number():
            step = int(np.clip(round((4.2 - h.get_value()) / .4), 0, 5))
            return M(labels[step], 32, TEAL).move_to([5.42,-1.42,0])

        fillbar = always_redraw(gauge_fill)
        number = always_redraw(gauge_number)
        gl = T("times faster", 28, TEAL).move_to([5.02,1.82,0])
        self.play(Create(bar), FadeIn(fillbar), FadeIn(gl), FadeIn(number), run_time=.68)
        self.at("At 25")
        self.play(Indicate(bar, color=TEAL, scale_factor=1.025), run_time=.45)
        self.at("every 5")
        note = chip("5.7 kJ/mol = ten times", TEAL, 30).scale(.82).move_to([3.05,3.25,0])
        self.play(FadeIn(note), run_time=.35)
        for hh in np.linspace(3.8, 2.2, 5):
            self.play(h.animate.set_value(float(hh)), run_time=.72, rate_func=smooth)
        self.finish()


class S08OmpBack(SpokenScene):
    def construct(self):
        old = dashed_profile(4.2, RED)
        h = ValueTracker(2.2)
        low = always_redraw(lambda: profile(h.get_value(), TEAL, 7))
        dots = valley_dots()
        number = M("×100,000", 32, TEAL).move_to([4.9,1.45,0])
        self.add(ground_fill(1.8), old, low, dots, schematic_tag(), number)
        self.at("about 97")
        drop = chip("97 kJ/mol", TEAL, 30).move_to([3.7,.55,0])
        final = power_text("×", size=35).move_to(number)
        self.play(h.animate.set_value(1.8), ReplacementTransform(number, final), FadeIn(drop), run_time=1.0)
        self.play(Indicate(final, color=TEAL, scale_factor=1.07), run_time=.45)
        self.at("flip the trip")
        rev = route_arrow(5.0, -5.0, GREEN, 1.8)
        self.play(FadeOut(VGroup(final,drop)), Create(rev[0]), FadeIn(rev[1]), run_time=1.0)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        old, low = dashed_profile(4.2, RED), profile(1.8, TEAL, 7)
        dots = VGroup(valley_dots(5), valley_dots(4,"right",GREEN,1.8))
        self.add(ground_fill(1.8), old, low, dots, schematic_tag())
        fwd = route_arrow(-5,5,YELLOW,1.8)
        rev = route_arrow(5,-5,GREEN,1.8)
        fl = chip("× 1,000,000", YELLOW, 30).scale(.8).move_to([-2.6,.55,0])
        rl = chip("× ?", GREEN, 38).scale(.8).move_to([2.8,-.2,0])
        self.at("forward trip")
        self.play(FadeIn(fl), FadeIn(rl), run_time=.45)
        self.at("Watch both arrows")
        self.play(Create(fwd[0]), FadeIn(fwd[1]), Create(rev[0]), FadeIn(rev[1]), run_time=1.1)
        self.at("backward trip")
        q = chip("Backward: faster, slower, unchanged?", TEXT, 34, fill_opacity=.12).move_to([0,-2.82,0])
        fit(q, 11.8)
        self.play(FadeIn(q, shift=UP*.25), rl.animate.scale(1.08), run_time=.55)
        self.finish()


class S10Think(Scene):
    def construct(self):
        old, low = dashed_profile(4.2, RED), profile(1.8, TEAL, 7)
        dots = VGroup(valley_dots(5), valley_dots(4,"right",GREEN,1.8))
        fwd, rev = route_arrow(-5,5,YELLOW,1.8), route_arrow(5,-5,GREEN,1.8)
        fl = chip("× 1,000,000", YELLOW, 30).scale(.8).move_to([-2.6,.55,0])
        rl = chip("× ?", GREEN, 38).scale(.8).move_to([2.8,-.2,0])
        q = chip("Backward: faster, slower, unchanged?", TEXT, 34, fill_opacity=.12).move_to([0,-2.82,0])
        fit(q, 11.8)
        self.add(ground_fill(1.8),old,low,dots,schematic_tag(),fwd,rev,fl,rl,q)
        self.play(rl.animate.scale(1.06), run_time=1.0, rate_func=there_and_back)
        self.wait(1.2)
        self.play(rl.animate.scale(1.06), run_time=1.0, rate_func=there_and_back)
        self.wait(1.3)


class S11Answer(SpokenScene):
    def construct(self):
        old, low = dashed_profile(4.2, RED), profile(1.8, TEAL, 7)
        dots = VGroup(valley_dots(5), valley_dots(4,"right",GREEN,1.8))
        fwd, rev = route_arrow(-5,5,YELLOW,1.8), route_arrow(5,-5,GREEN,1.8)
        fl = chip("× 1,000,000", YELLOW, 30).scale(.8).move_to([-2.6,.55,0])
        rl = chip("× ?", GREEN, 38).scale(.8).move_to([2.8,-.2,0])
        self.add(ground_fill(1.8),old,low,dots,schematic_tag(),fwd,rev,fl,rl)
        self.at("Also a million")
        ans = chip("× 1,000,000", GREEN, 30).scale(.8).move_to(rl)
        self.play(ReplacementTransform(rl,ans), run_time=.6)
        yl, yr, pp = energy_y(-5.2,1.8), energy_y(5.2,1.8), peak_point(1.8)
        self.at("two valleys")
        pins = VGroup(pin(np.array([-5.2,yl,0])),pin(np.array([5.2,yr,0])))
        self.play(FadeIn(pins), Flash([-5.2,yl,0],color=TEAL), Flash([5.2,yr,0],color=TEAL), run_time=.6)
        self.at("same lowered top")
        brs = VGroup(vbracket(-.6,yl,pp[1],YELLOW), vbracket(.65,yr,pp[1],GREEN),
                     Dot(pp,radius=.13,color=PURPLE))
        self.play(GrowFromCenter(brs[0]), GrowFromCenter(brs[1]), FadeIn(brs[2]), run_time=.75)
        self.at("their ratio")
        keq = chip("Keq: unchanged", TEXT, 34).move_to([0,2.65,0])
        self.play(ReplacementTransform(VGroup(fl,ans),keq), run_time=.75)
        self.finish()


class S12Uphill(SpokenScene):
    def construct(self):
        h = ValueTracker(1.8)
        revflag = ValueTracker(0)
        curve = always_redraw(lambda: profile(h.get_value(),TEAL,7,revflag.get_value()>.5))
        old = always_redraw(lambda: dashed_profile(4.2,RED,4,revflag.get_value()>.5))
        left = VGroup(*[Dot(radius=.11,color=YELLOW).move_to([-5.3+i*.34,energy_y(-5.3+i*.34,1.8)+.17,0]) for i in range(6)])
        right = VGroup(*[Dot(radius=.11,color=GREEN).move_to([3.8+i*.34,energy_y(3.8+i*.34,1.8)+.17,0]) for i in range(2)])
        counts = VGroup(M("6",32,YELLOW),T(":",30),M("2",32,GREEN)).arrange(RIGHT,.18).move_to([0,-3.05,0])
        ground = always_redraw(lambda: ground_fill(h.get_value(),revflag.get_value()>.5))
        self.add(ground,old,curve,schematic_tag(),left,right)
        self.at("same equilibrium")
        self.play(FadeIn(counts), run_time=.4)
        movers = VGroup(*[Dot(radius=.23,color=YELLOW) for _ in range(7)])
        self.add(movers)
        self.play(stream_animation(movers, run_time=2.25), run_time=2.25)
        self.remove(movers)
        noenz = VGroup(dashed_profile(4.2,RED).scale(.22), T("no enzyme: same end, later",28,RED)).arrange(DOWN,.1)
        noenz.move_to([-4.55,2.55,0])
        self.play(FadeIn(noenz), run_time=.4)
        self.at("cannot push")
        blocked = CurvedArrow([4.8, energy_y(4.8,1.8)+.25, 0],
                              [-1.3, energy_y(-1.3,1.8)+.45, 0], angle=-.18,
                              color=RED, stroke_width=11)
        self.play(FadeOut(noenz), Create(blocked), Indicate(old,color=RED,scale_factor=1.01), run_time=2.15)
        self.play(Uncreate(blocked), run_time=.6)
        self.at("far valley is higher")
        self.play(revflag.animate.set_value(1), run_time=1.15)
        self.at("other way")
        flows = VGroup(*[route_arrow(4.7-i*.3,-4.7+i*.3,GREEN,1.8,True)[0] for i in range(3)])
        self.play(LaggedStart(*[Create(p) for p in flows],lag_ratio=.18), run_time=1.0)
        self.finish()


class S13How(SpokenScene):
    def construct(self):
        old_bg, low_bg, bg_tag = dashed_profile(4.2,RED), profile(1.8,TEAL,7), schematic_tag()
        old_bg.set_stroke(opacity=.3); low_bg.set_stroke(opacity=.3); bg_tag.set_opacity(.3)
        bg_ground = ground_fill(1.8, opacity=.08)
        bg = VGroup(bg_ground, old_bg, low_bg, bg_tag)
        self.add(bg)
        self.at("protein lower the top")
        c = cup([0,-.15,0],1.55)
        label = T("active site",30,TEAL).move_to([0,2.75,0])
        self.play(Create(c), FadeIn(label), old_bg.animate.set_stroke(opacity=.12),
                  low_bg.animate.set_stroke(opacity=.12), bg_tag.animate.set_opacity(.12), run_time=.9)
        self.at("better matches")
        oval = ts_oval([0,.25,0],1.35)
        gold = contacts([0,.25,0],8,1.35)
        snug_c = c.copy().stretch(.9, 0)
        self.play(FadeIn(oval), Transform(c, snug_c),
                  LaggedStart(*[Create(x) for x in gold],lag_ratio=.13), run_time=3.75)
        self.at("substrate more loosely")
        ball = Circle(radius=.48,color=YELLOW,fill_color=YELLOW,fill_opacity=.35,stroke_width=5).move_to([0,.15,0])
        two = VGroup(gold[1],gold[-2]).copy()
        self.play(FadeOut(VGroup(oval,gold)),FadeIn(ball),FadeIn(two),run_time=.55)
        self.play(ball.animate.shift(LEFT*.22),run_time=.25,rate_func=there_and_back)
        self.at("transition state more snugly")
        oval2 = ts_oval([0,.25,0],1.35)
        gold2 = contacts([0,.25,0],8,1.35)
        self.play(ReplacementTransform(ball,oval2),FadeOut(two),LaggedStart(*[FadeIn(x) for x in gold2],lag_ratio=.04),run_time=.75)
        self.finish()


class S14Grip(SpokenScene):
    def construct(self):
        c = breathing_grip(cup([-3.5,-.15,0],1.05))
        oval = ts_oval([-3.5,.15,0],.92)
        gold = contacts([-3.5,.15,0],8,.92)
        self.add(c,oval,gold)
        # Computed zoom of the same energy profile, not a hand-sketched curve.
        zoom = ParametricFunction(
            lambda x: np.array([3.5 + 1.1*x, .55*energy_y(x,1.8) - .45, 0]),
            t_range=[-2.2,2.2,.02], color=TEAL, stroke_width=7,
        )
        self.add(zoom,schematic_tag())
        self.at("extra grip")
        sparks = VGroup(*[Dot(x.get_center(),radius=.07,color=GOLD) for x in gold[2:]])
        self.play(LaggedStart(*[
            s.animate(rate_func=smooth).move_to([2.9+(i%3)*.3,1.25-(i//3)*.28,0])
            for i,s in enumerate(sparks)
        ],lag_ratio=.14), zoom.animate.shift(DOWN*.28), run_time=3.85)
        self.play(FadeOut(sparks), run_time=.35)
        self.at("bound substrate")
        base_y=-1.6; top_y=1.0
        br=vbracket(4.55,base_y,top_y,YELLOW)
        self.play(GrowFromCenter(br),run_time=.45)
        short=vbracket(4.55,base_y,top_y-.5,YELLOW)
        self.play(Transform(br,short), zoom.animate.shift(DOWN*.5), run_time=3.55, rate_func=smooth)
        self.at("how many times tighter")
        num=T("grip on transition state",34,PURPLE)
        den=T("grip on substrate",34,YELLOW)
        frac=VGroup(num,Line(LEFT*1.75,RIGHT*1.75,color=TEXT),den).arrange(DOWN,.12)
        eq=T("= speed-up",36,TEAL)
        formula=VGroup(frac,eq).arrange(RIGHT,.35).scale(.82).move_to([0,-2.7,0])
        self.play(FadeIn(formula,shift=UP*.2),run_time=.6)
        self.finish()


class S15SameGrip(SpokenScene):
    def construct(self):
        c=breathing_grip(cup([-3.5,-.15,0],1.05))
        ball=Circle(radius=.42,color=YELLOW,fill_color=YELLOW,fill_opacity=.3,stroke_width=5).move_to([-3.5,.1,0])
        two=contacts([-3.5,.15,0],8,.92)
        self.add(c,ball,two[1],two[-2])
        base=Line([1.0,-1.15,0],[5.1,-1.15,0],color=YELLOW,stroke_width=6)
        top=Line([1.0,1.25,0],[5.1,1.25,0],color=PURPLE,stroke_width=6)
        br=vbracket(5.55,-1.15,1.25,YELLOW)
        self.add(base,top,br,schematic_tag())
        self.at("just as hard")
        extra = VGroup(*[two[i] for i in [0,2,3,4,5,7]])
        self.play(LaggedStart(*[FadeIn(x) for x in extra],lag_ratio=.09),run_time=.9)
        self.play(LaggedStart(*[Indicate(x, color=GOLD, scale_factor=1.25) for x in extra],
                              lag_ratio=.1), run_time=1.65)
        self.at("Both would sink together")
        self.play(base.animate.shift(DOWN*.65),top.animate.shift(DOWN*.65),br.animate.shift(DOWN*.65),run_time=1.65)
        no=chip("no faster",RED,30).move_to([3.0,2.15,0])
        self.play(FadeIn(no),run_time=.35)
        self.at("stay the same")
        self.play(FadeOut(VGroup(*[two[i] for i in [0,2,3,4,5,7]])),Indicate(br,color=YELLOW),run_time=.55)
        self.finish()


class S16Return(SpokenScene):
    def construct(self):
        old,low=dashed_profile(4.2,RED),profile(1.8,TEAL,7)
        dots=VGroup(valley_dots(6),valley_dots(3,"right",GREEN,1.8))
        pins=VGroup(pin(np.array([-5.2,energy_y(-5.2,1.8),0])),pin(np.array([5.2,energy_y(5.2,1.8),0])))
        qs=question_chips()
        self.add(ground_fill(1.8),old,low,dots,pins,schematic_tag())
        self.at("valleys decide")
        self.play(FadeIn(qs[0]),Flash([-5.2,energy_y(-5.2,1.8),0],color=YELLOW),Flash([5.2,energy_y(5.2,1.8),0],color=GREEN),run_time=.7)
        self.at("ridge decides")
        self.play(FadeIn(qs[1]),Indicate(low,color=TEAL,scale_factor=1.015),run_time=.65)
        runners=VGroup(*[Dot(radius=.16,color=YELLOW) for _ in range(5)])
        self.add(runners)
        self.play(stream_animation(runners,run_time=3.95),run_time=3.95)
        self.remove(runners)
        self.at("gripping the top hardest")
        pp=peak_point(1.8)
        c=cup(pp+UP*.05,.36)
        oval=ts_oval(pp+UP*.08,.32)
        gold=contacts(pp+UP*.08,8,.32)
        self.play(FadeIn(c),FadeIn(oval),LaggedStart(*[Create(x) for x in gold],lag_ratio=.04),run_time=.7)
        tr,d=moving_dot(1.8)
        self.add(d)
        self.play(tr.animate.set_value(5.2),run_time=.95,rate_func=linear)
        self.finish()


class S17End(EndCard):
    LINE = "An enzyme lowers the ridge. It never moves the valleys."

    def construct(self):
        old, low = dashed_profile(4.2,RED), profile(1.8,TEAL,7)
        old.set_stroke(opacity=.2); low.set_stroke(opacity=.2)
        ld, rd, tag = valley_dots(5), valley_dots(3,"right",GREEN,1.8), schematic_tag()
        ld.set_opacity(.2); rd.set_opacity(.2); tag.set_opacity(.2)
        ground = ground_fill(1.8, opacity=.045)
        living=VGroup(ground,old,low,ld,rd,tag)
        self.add(living)
        line=T(self.LINE,40,font=TITLE_FONT)
        fit(line,11.6)
        sub=T("biochemistrypedia.com",22,TEAL)
        card=VGroup(line,sub).arrange(DOWN,.42)
        self.play(FadeIn(line,shift=UP*.15),FadeIn(sub),run_time=.8)
        self.finish()
