"""What limits a population?  (Biochemistrypedia explainer, high school Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the population: crab tokens, crab-count bars, the population curve
  GREEN  = biotic factors, and things that RAISE carrying capacity
  ORANGE = abiotic factors
  RED    = limits and things that LOWER carrying capacity
  GOLD   = carrying capacity (dashed line) and the film's question
  TEAL   = the winter survey (site marks, dredge)
  PURPLE = what people do (crabbing)
  GREY   = outlines, axes, labels
Crab tokens are an illustration, not counts. The J bars use the lesson's own bacteria numbers
(10, 20, 40, 80, 160, 320 per 30-minute step). The S curve and the moving carrying capacity are a
MODEL SKETCH in made-up units (logistic curve computed here), labelled as such, never a measurement.
Survey comparisons use direction arrows, without invented counts.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
CTEAL = "#3FB8C0"
GOLDC = "#F2C94C"


def crab(s=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.36, height=0.26, stroke_color=BLUE, stroke_width=2.5,
                            fill_color=BLUE, fill_opacity=0.35)
    return VGroup(body).scale(s)


def arrow_to(a, b, color, w=6):
    return Arrow(a, b, color=color, stroke_width=w, buff=0.0, max_tip_length_to_length_ratio=0.3)


# ---- the model sketch (made-up units) --------------------------------------------------------
K0 = 8.0


def logistic(t):
    return K0 / (1 + np.exp(-1.1 * (t - 4.0)))


def wob(t):
    return 0.3 * np.clip((t - 6.0) / 3.0, 0, 1) * np.sin(2.4 * t)


def f_pop(t):
    return logistic(t) + wob(t)


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def K_of_t(t):
    t = np.asarray(t, dtype=float)
    return K0 + (9.2 - K0) * smooth((t - 7.0) / 1.4) + (5.6 - 9.2) * smooth((t - 10.0) / 1.8)


def make_axes():
    ax = Axes(x_range=[0, 13, 1], y_range=[0, 10, 1], x_length=8.4, y_length=4.9,
              axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3,
                           "tip_width": 0.2, "tip_height": 0.2}, tips=True)
    ax.move_to([2.4, -0.45, 0])
    xl = T("time", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.12).align_to(ax.x_axis, RIGHT)
    yl = T("population size", 24, GREY).next_to(ax.y_axis, UP, buff=0.12).align_to(ax.y_axis, LEFT)
    nt = T("model sketch, made-up units", 22, GREY).next_to(ax, DOWN, buff=0.45)
    nt.move_to([ax.get_center()[0], nt.get_center()[1], 0])
    return ax, VGroup(xl, yl), nt


def curve(ax, f, a, b, color=BLUE, w=6):
    return ax.plot(lambda t: float(f(t)), x_range=[a, b, 0.05], color=color, stroke_width=w, use_smoothing=False)


def poly(ax, ts, ys, color, w=6):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([ax.c2p(t, y) for t, y in zip(ts, ys)])
    return m


def kline(ax, a=0, b=13, y=K0, color=GOLDC):
    return DashedLine(ax.c2p(a, y), ax.c2p(b, y), color=color, stroke_width=5, dash_length=0.18)


def prior_scene(scene):
    """rebuild the end state of S04 in the same place (axes, S curve to t=7, gold line)."""
    ax, lbls, nt = make_axes()
    cur = curve(ax, f_pop, 0, 7.0, BLUE)
    kl = kline(ax, 0, 7)
    kt = chip("carrying capacity", GOLDC, 28).move_to(ax.c2p(3.6, 9.15))
    scene.add(ax, lbls, nt, cur, kl, kt)
    return ax, lbls, nt, cur, kl, kt


def delayed(anim, delay):
    return Succession(Wait(max(0.01, delay)), anim)


def model_ext(ax):
    """the model sketch after t=7: K steps up then down; the population follows (logistic step, made-up units)."""
    ts = np.arange(7.0, 13.0001, 0.05)
    Kv = K_of_t(ts)
    Nv = np.zeros_like(ts)
    N = float(logistic(7.0))
    for i in range(len(ts)):
        if i:
            N += 0.05 * 1.1 * N * (1 - N / Kv[i])
        Nv[i] = N
    Nv = Nv + wob(ts)
    cut = int(round((10.0 - 7.0) / 0.05))
    return ts, Kv, Nv, cut



def population_box():
    box = RoundedRectangle(corner_radius=0.25, width=4.6, height=3.6,
                           stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                           fill_opacity=0.07).move_to([-3.5, 0.45, 0])
    tokens = VGroup(*[crab(1.5).move_to(box.get_center() +
                     [(i % 3 - 1) * 1.2, (0.5 - i // 3) * 1.2, 0]) for i in range(6)])
    return box, tokens


def heading(text, color=TEXT):
    return T(text, 34, color, font=TITLE_FONT).move_to([0, 3.15, 0])


def panel_axes(x):
    ax = Axes(x_range=[0, 6, 1], y_range=[0, 10, 2], x_length=5.2, y_length=3.3,
              axis_config={"include_ticks": False, "include_numbers": False,
                           "color": GREY, "stroke_width": 3}, tips=False).move_to([x, 0, 0])
    return ax


class S00Title(TitleCard):
    LESSON = "Populations and Carrying Capacity"
    TITLE = "What Limits a Population?"

    def construct(self):
        title = T(self.TITLE, 48, font=TITLE_FONT).move_to([0, 2.6, 0])
        tokens = VGroup(*[crab(1.7).move_to([(i-1)*1.0, 0, 0]) for i in range(3)])
        labels = VGroup(chip("food", GREEN, 24).move_to([-3.4, 0.8, 0]),
                        chip("shelter", GREEN, 24).move_to([3.4, 0.8, 0]),
                        chip("predators", GREEN, 24).move_to([-3.4, -1.5, 0]),
                        chip("cold water", ORANGE, 24).move_to([3.4, -1.5, 0]))
        rule = Line([-1.3, 1.65, 0], [1.3, 1.65, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(title), Create(rule), FadeIn(tokens), run_time=0.8)
        self.play(FadeIn(labels), run_time=0.6)
        self.finish()


class S01Puzzle(SpokenScene):
    def construct(self):
        box, tokens = population_box()
        bay = T("Chesapeake Bay · crab tokens, not counts", 22, GREY).move_to([-3.5, -1.7, 0])
        estimate = T("Winter population estimates\ncan change by more than\n100 million", 30, BLUE).move_to([3.2, 0.7, 0])
        self.at("The number of")
        self.play(FadeIn(box), FadeIn(tokens), FadeIn(bay), FadeIn(estimate), run_time=0.8)
        limit = T("Growth cannot continue forever", 32, RED).move_to([0, 3.1, 0])
        self.at("But no population")
        self.play(FadeIn(limit), run_time=0.7)
        resource = chip("limited food\nand hiding places", RED, 28).move_to([3.2, 1.2, 0])
        self.at("Food and hiding")
        self.play(ReplacementTransform(estimate, resource), run_time=0.6)
        living = chip("predators · disease", GREEN, 24).move_to([3.2, -0.15, 0])
        physical = chip("temperature · salinity", ORANGE, 24).move_to([3.2, -1.2, 0])
        self.at("Predators disease")
        self.play(FadeIn(living), run_time=0.5)
        self.at("temperature and salinity")
        self.play(FadeIn(physical), run_time=0.6)
        groups = T("Resources + challenges", 30, TEXT).move_to([3.2, 2.35, 0])
        self.at("Together resources and challenges")
        self.play(FadeOut(limit), FadeIn(groups), run_time=0.6)
        definition = T("Largest population the environment\ncan support over time", 32, TEXT).move_to([0, -2.85, 0])
        self.at("the largest population")
        self.play(FadeIn(definition), run_time=0.7)
        name = heading("Carrying capacity", GOLDC)
        self.at("That is its")
        self.play(FadeIn(name), run_time=0.6)
        self.finish()


class S02Factors(SpokenScene):
    def construct(self):
        box, tokens = population_box()
        label = heading("One species, one place, one time", BLUE)
        self.at("A population is")
        self.play(FadeIn(box), FadeIn(tokens), FadeIn(label), run_time=0.7)
        limited = T("Limiting factor: keeps a population from growing larger", 26, RED).move_to([0, -3.2, 0])
        self.at("A limiting factor")
        self.play(FadeIn(limited), run_time=0.6)
        biotic = VGroup(T("Biotic: living", 30, GREEN),
                        T("predators · disease", 26, GREEN)).arrange(DOWN, buff=0.2).move_to([3.3, 1.65, 0])
        ba = arrow_to([0.8, 1.6, 0], [-0.95, 1.1, 0], GREEN)
        self.at("Biotic factors are")
        self.play(FadeIn(biotic), GrowArrow(ba), run_time=0.7)
        abiotic = VGroup(T("Abiotic: nonliving", 30, ORANGE),
                         T("temperature", 26, ORANGE), T("salinity = salt level", 26, ORANGE)
                         ).arrange(DOWN, buff=0.18).move_to([3.3, -0.45, 0])
        aa = arrow_to([0.8, -0.4, 0], [-0.95, -0.4, 0], ORANGE)
        self.at("Abiotic factors are")
        self.play(FadeIn(abiotic), GrowArrow(aa), run_time=0.7)
        resources = T("Limited food and shelter", 24, RED).move_to([-3.5, -1.85, 0])
        crowd = T("Crowding: competition + disease increase", 28, RED).move_to([0, -2.65, 0])
        self.at("Crowding makes")
        self.play(FadeOut(limited), FadeIn(resources), FadeIn(crowd),
                  *[c.animate.move_to(box.get_center() + [(i % 3 - 1)*0.62, (0.5-i//3)*0.5, 0])
                    for i, c in enumerate(tokens)], box.animate.set_stroke(RED), run_time=1.0)
        self.finish()


class S03Exp(SpokenScene):
    def construct(self):
        vals = [10, 20, 40, 80, 160, 320]
        base, H = -2.15, 3.8
        xs = [-4.5 + 1.8*i for i in range(6)]
        floor = Line([-5.6, base, 0], [5.7, base, 0], color=GREY, stroke_width=3)
        vertical = Line([-5.6, base, 0], [-5.6, 2.3, 0], color=GREY, stroke_width=3)
        axes_labels = VGroup(T("population size", 24, GREY).move_to([-4.4, 2.5, 0]),
                            T("time · steps of 30 minutes", 24, GREY).move_to([0, -3.1, 0]))
        steps = VGroup(*[M(str(i), 22, GREY).move_to([xs[i], base-0.35, 0]) for i in range(6)])
        top = heading("Fresh food · 10 bacteria", BLUE)
        bars, labels = [], []
        for i, value in enumerate(vals):
            height = H*value/320
            bar = Rectangle(width=1.0, height=height, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.45).move_to([xs[i], base+height/2, 0])
            bars.append(bar)
            labels.append(M(str(value), 28, TEXT).next_to(bar, UP, buff=0.12))
        self.at("Suppose 10 bacteria")
        self.play(FadeIn(top), Create(floor), Create(vertical), FadeIn(axes_labels), FadeIn(steps),
                  GrowFromEdge(bars[0], DOWN), FadeIn(labels[0]), run_time=0.8)
        split = T("Each splits in two every 30 minutes", 26, TEXT).move_to([1.6, 2.5, 0])
        self.at("Each one splits")
        self.play(FadeIn(split), run_time=0.6)
        for i, phrase in enumerate(["20", "40", "80", "160", "320"], 1):
            self.at(phrase)
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(labels[i]), run_time=0.4)
        exponential = heading("Exponential growth", BLUE)
        self.at("This is exponential growth")
        self.play(ReplacementTransform(top, exponential), FadeOut(split), run_time=0.6)
        jc = ParametricFunction(lambda t: np.array([-4.5+1.8*t, base+H*(10*2**t)/320, 0]),
                                t_range=[0, 5, 0.02], color=BLUE, stroke_width=7)
        jlabel = T("J shape", 36, BLUE).move_to([-1.5, 0.6, 0])
        self.at("It makes a J shape")
        self.play(Create(jc), FadeIn(jlabel), run_time=1.0)
        resources = T("Plentiful resources", 26, GREEN).move_to([2.6, 2.5, 0])
        self.at("while resources are plentiful")
        self.play(FadeIn(resources), run_time=0.6)
        self.finish()


class S04Logistic(SpokenScene):
    def construct(self):
        ax, labels, note = make_axes()
        # Reuse the original equation and axes, centered to use the entire frame.
        group = VGroup(ax, labels, note).shift(LEFT*2.4)
        note.become(T("Model, made-up units", 22, GREY).move_to([0, -3.4, 0]))
        start = curve(ax, f_pop, 0, 4)
        title = heading("Limits slow growth", RED)
        self.at("Then limits set in")
        self.play(Create(ax), FadeIn(labels), FadeIn(note), Create(start), FadeIn(title), run_time=0.8)
        food = chip("food becomes limited", RED, 24).move_to([-2.0, 1.7, 0])
        self.at("Food runs short")
        self.play(FadeIn(food), run_time=0.5)
        rest = curve(ax, logistic, 4, 9)
        self.at("growth slows into")
        self.play(Create(rest), run_time=1.7)
        capacity = kline(ax)
        caplabel = T("carrying capacity", 26, GOLDC).move_to([2.5, 1.8, 0])
        self.at("levels off near")
        self.play(Create(capacity), FadeIn(caplabel), run_time=0.8)
        movement = T("Little movement in or out", 24, GREY).move_to([2.5, -0.7, 0])
        self.at("If few individuals")
        self.play(FadeOut(food), FadeIn(movement), run_time=0.6)
        balance = chip("births ≈ deaths", TEXT, 28).move_to([2.5, -1.65, 0])
        self.at("births and deaths")
        self.play(FadeIn(balance), run_time=0.7)
        waves = curve(ax, f_pop, 9, 13)
        self.at("Small ups and downs")
        self.play(Create(waves), run_time=1.6)
        equilibrium = heading("Dynamic equilibrium", BLUE)
        self.at("dynamic equilibrium")
        self.play(ReplacementTransform(title, equilibrium), run_time=0.6)
        self.finish()


class S05Moves(SpokenScene):
    def construct(self):
        left, right = panel_axes(-3.3), panel_axes(3.3)
        title = heading("Capacity and population size are different", GOLDC)
        lh = T("Lasting resource change", 26, TEXT).move_to([-3.3, 2.35, 0])
        rh = T("Single freeze · resources unchanged", 24, TEXT).move_to([3.3, 2.35, 0])
        note = T("Model, made-up units · time →", 22, GREY).move_to([0, -3.4, 0])
        legend = VGroup(T("— population size", 24, BLUE), T("- - carrying capacity", 24, GOLDC)
                        ).arrange(RIGHT, buff=0.8).move_to([0, -2.85, 0])
        initial = kline(left, 0, 1.5)
        self.at("Carrying capacity can change")
        self.play(FadeIn(title), Create(left), FadeIn(lh), FadeIn(note), FadeIn(legend), Create(initial), run_time=0.8)
        up = poly(left, [1.5, 2.5, 3.6], [8, 9.2, 9.2], GOLDC, 5)
        updash = DashedVMobject(up, num_dashes=12)
        more = T("More shelter", 25, GREEN).move_to([-3.3, -2.2, 0])
        self.at("More hiding places")
        self.play(Create(updash), FadeIn(more), run_time=1.2)
        down = DashedVMobject(poly(left, [3.6, 4.6, 6], [9.2, 5.6, 5.6], GOLDC, 5), num_dashes=12)
        less = T("Marsh grass lost", 25, RED).move_to(more)
        self.at("Losing marsh grass")
        self.play(Create(down), ReplacementTransform(more, less), run_time=1.0)
        fixed = kline(right, 0, 6)
        pre = poly(right, [0, 1.8], [7.8, 7.8], BLUE)
        self.at("A single hard freeze")
        self.play(Create(right), FadeIn(rh), Create(fixed), Create(pre), run_time=0.7)
        unchanged = T("Resources and capacity unchanged", 24, GOLDC).move_to([3.3, -2.2, 0])
        self.at("If resources stay the same")
        self.play(FadeIn(unchanged), run_time=0.6)
        drop = poly(right, [1.8, 2.1], [7.8, 3.2], BLUE)
        freeze = arrow_to(right.c2p(2.1, 6.8), right.c2p(2.1, 3.6), ORANGE, 5)
        self.at("it pushes the population")
        self.play(Create(drop), GrowArrow(freeze), run_time=0.8)
        recovery = curve(right, lambda t: 8/(1+1.5*np.exp(-1.6*(t-2.1))), 2.1, 6)
        self.at("the population can grow back")
        self.play(Create(recovery), FadeOut(freeze), run_time=1.1)
        tokens = VGroup(*[crab(1.3).move_to([-4.6+i*0.85, -0.7, 0]) for i in range(4)])
        basket = RoundedRectangle(width=1, height=0.65, corner_radius=0.1,
                                  stroke_color=PURPLE).move_to([-1.5, -1.1, 0])
        crabbing = T("Crabbing removes individuals", 24, PURPLE).move_to([-3.3, -2.2, 0])
        self.at("Crabbing also removes")
        self.play(ReplacementTransform(less, crabbing), FadeIn(tokens), FadeIn(basket), run_time=0.5)
        self.play(tokens[-1].animate.move_to(basket).set_opacity(0), run_time=0.6)
        self.at("Fewer crabs does not")
        self.play(Indicate(fixed, color=GOLDC, scale_factor=1),
                  Indicate(initial, color=GOLDC, scale_factor=1), run_time=0.8)
        self.finish()


class S06Answer(SpokenScene):
    def construct(self):
        title = heading("What does the winter survey show?", CTEAL)
        bay = RoundedRectangle(corner_radius=0.4, width=9, height=3.3,
                               stroke_color=GREY, fill_color=GREY, fill_opacity=0.08).move_to([0, 0.2, 0])
        tokens = VGroup(*[crab(1.5).move_to([-3+i*1.2, -0.6, 0]) for i in range(6)])
        dredge = VGroup(Line([-4.0, 1.3, 0], [-3, 0.0, 0], color=CTEAL),
                        RoundedRectangle(width=1.1, height=0.7, corner_radius=0.1,
                                         stroke_color=CTEAL).move_to([-3, 0, 0]))
        dredgelab = T("Dredge samples crabs", 26, CTEAL).move_to([0, -2.3, 0])
        self.at("What does the winter survey show")
        self.play(FadeIn(title), FadeIn(bay), FadeIn(tokens), FadeIn(dredge), FadeIn(dredgelab), run_time=0.5)
        self.play(dredge.animate.shift(RIGHT*4.8), run_time=1.0)
        years = heading("2024–2025 → 2025–2026 · estimates", BLUE)
        self.at("In the last two survey winters")
        self.play(FadeOut(VGroup(bay, tokens, dredge, dredgelab)), ReplacementTransform(title, years), run_time=0.7)
        def result(text, x, up):
            label = T(text, 28, BLUE).move_to([x, 1.5, 0])
            a = arrow_to([x, -0.8 if up else 0.8, 0], [x, 0.8 if up else -0.8, 0], BLUE)
            return VGroup(label, a)
        total, young, adult = result("Total", -4, True), result("Juveniles", 0, True), result("Adult females", 4, False)
        self.at("the total rose")
        self.play(FadeIn(total), run_time=0.5)
        self.at("there were more young crabs")
        self.play(FadeIn(young), run_time=0.6)
        self.at("Adult females fell")
        self.play(FadeIn(adult), run_time=0.6)
        measured = T("Survey estimates population size", 32, BLUE).move_to([0, -2.2, 0])
        self.at("These are population estimates")
        self.play(FadeIn(measured), run_time=0.6)
        caution = T("Does not measure carrying capacity\nor identify the cause", 32, GOLDC).move_to([0, 0.65, 0])
        self.at("The survey does not measure")
        self.play(FadeOut(VGroup(total, young, adult)), FadeIn(caution), run_time=0.7)
        evidence = VGroup(chip("temperature", ORANGE, 24), chip("habitat", GREEN, 24),
                          chip("predator data", GREEN, 24)).arrange(RIGHT, buff=0.5).move_to([0, -0.9, 0])
        self.at("We need temperature")
        self.play(FadeIn(evidence), run_time=0.7)
        test = T("Evidence needed to test causes", 28, TEXT).move_to([0, -2.2, 0])
        self.at("to test that")
        self.play(ReplacementTransform(measured, test), run_time=0.5)
        self.at("The central rule")
        self.play(FadeOut(VGroup(years, caution, evidence, test)), run_time=0.6)
        rule = T("Environmental limits\nconstrain population growth.", 44, GOLD, font=TITLE_FONT)
        self.at("environmental limits constrain")
        self.play(FadeIn(rule, shift=UP*0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Limited resources set a carrying capacity, and it can change."