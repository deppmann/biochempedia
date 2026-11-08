"""Conservation and Restoration: protect habitat, support recovery  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  TEXT   = an individual animal, sex not stated
  BLUE   = a male
  ORANGE = a female
  YELLOW = chance / probability (dice, percentages)
  RED    = extinct run / fails the target
  GREEN  = meets the target
  PURPLE = effective size Ne
  GREY   = outlines, tracks, de-emphasized
  TEAL   = habitat / ecosystem recovery
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def dot(r=0.2, color=TEXT, letter=None, fill=0.9):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)
    if letter:
        return VGroup(c, T(letter, int(r * 56), BG, weight=BOLD).move_to(c))
    return VGroup(c)


def dice(side=1.8, color=YELLOW):
    sq = RoundedRectangle(corner_radius=0.2, width=side, height=side, stroke_color=color, stroke_width=5,
                          fill_color=color, fill_opacity=0.18)
    o = side * 0.24
    pips = VGroup(*[Circle(radius=side * 0.075, stroke_width=0, fill_color=color, fill_opacity=1).move_to(sq.get_center() + np.array([dx * o, dy * o, 0]))
                    for dx, dy in [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)]])
    return VGroup(sq, pips)


def arena(w, h, center):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to([center[0], center[1], 0])


def scatter(n, w, h, center, r, color=TEXT, seed=1, min_d=0.0):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = np.array([rng.uniform(-w / 2 + r + 0.1, w / 2 - r - 0.1), rng.uniform(-h / 2 + r + 0.1, h / 2 - r - 0.1)])
        if all(np.linalg.norm(p - q) >= max(min_d, 2.3 * r) for q in pts):
            pts.append(p)
    return VGroup(*[dot(r, color).move_to([center[0] + p[0], center[1] + p[1], 0]) for p in pts])


# Existing population, arena and dice helpers retain the original drawing language.
def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.05, 0])


def patch(w, h, x, y, damaged=False):
    return arena(w, h, [x, y]).set_stroke(GREY if damaged else TEAL).set_fill(TEAL, 0.05 if damaged else 0.22)


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.35)


def hbar(width, x, y, color):
    return Rectangle(width=width, height=0.48, stroke_color=color, fill_color=color,
                     fill_opacity=0.45, stroke_width=3).move_to([x + width / 2, y, 0])


class S00Title(TitleCard):
    LESSON = "Conservation and Restoration"
    TITLE = "Protect Habitat, Support Recovery"

    def construct(self):
        # Keep the house title layout, with every label at least 22 pt.
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 44, font=TITLE_FONT)
        fit(title, max_w=12.2)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand), FadeIn(lesson), run_time=0.6)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.0)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        title = heading("What drove the population down?")
        land = patch(7.0, 4.0, -2.2, 0)
        animals = scatter(5, 3.0, 2.3, [-2.2, 0], 0.22, seed=4, min_d=0.7)
        label = T("wild cats", 26).move_to([-2.2, -2.6, 0])
        self.at("Conservation starts", lead=0)
        self.play(FadeIn(title), FadeIn(land), FadeIn(animals), FadeIn(label), run_time=0.7)
        self.at("If habitat loss")
        self.play(Transform(land, patch(3.8, 2.8, -2.2, 0)), run_time=1.0)
        self.at("address it first")
        stop = chip("halt habitat loss", TEAL, 26).move_to([3.8, 1.5, 0])
        self.play(FadeIn(stop), run_time=0.5)
        self.at("Protect habitat")
        self.play(land.animate.set_stroke(TEAL, 6), run_time=0.5)
        other = patch(2.1, 2.8, 3.5, -0.6, damaged=True)
        self.at("connect isolated patches")
        corridor = Rectangle(width=2.75, height=0.45, stroke_color=TEAL, fill_color=TEAL,
                             fill_opacity=0.22).move_to([1.08, -0.6, 0])
        self.play(FadeIn(other), GrowFromEdge(corridor, LEFT), run_time=0.65)
        self.at("help damaged ecosystems")
        self.play(other.animate.set_fill(TEAL, 0.32).set_stroke(TEAL, 4), run_time=1.0)
        self.at("Small populations")
        isolated = VGroup(patch(1.8, 1.1, 3.5, -2.75), dot(0.2).move_to([3.5, -2.75, 0]))
        self.play(FadeOut(label), FadeIn(isolated),
                  Transform(title, heading("Small populations may need extra help")), run_time=0.6)
        self.at("A genetic gain")
        self.play(Transform(stop, chip("gain may be temporary", YELLOW, 24).move_to([3.7, 1.5, 0])), run_time=0.5)
        self.at("if habitat keeps shrinking")
        self.play(Transform(land, patch(3.1, 2.5, -2.2, 0)), run_time=0.8)
        self.finish()


class S08Habitat(SpokenScene):
    def construct(self):
        title = heading("What does the evidence show?")
        self.at("What does the evidence", lead=0)
        self.play(FadeIn(title), run_time=0.5)
        tag = T("Randomized experiment · one South Carolina site", 26, GREY).move_to([0, 2.25, 0])
        # Equal total habitat area: disconnected treatment redistributes corridor area.
        connected = VGroup(patch(1.4, 1.5, -4.5, 0.6), patch(1.4, 1.5, -2.1, 0.6),
                           Rectangle(width=1.0, height=0.35, stroke_color=TEAL,
                                     fill_color=TEAL, fill_opacity=0.22).move_to([-3.3, 0.6, 0]))
        disconnected = VGroup(patch(1.4 + 0.35 / 3, 1.5, 2.1, 0.6),
                              patch(1.4 + 0.35 / 3, 1.5, 4.5, 0.6))
        labs = VGroup(T("connected", 26).move_to([-3.3, 1.75, 0]),
                      T("unconnected", 26).move_to([3.3, 1.75, 0]),
                      T("equal habitat area", 24, GREY).move_to([0, -0.65, 0]))
        self.at("In a randomized experiment")
        self.play(FadeIn(tag), FadeIn(connected), FadeIn(disconnected), FadeIn(labs), run_time=0.8)
        species = VGroup(*[dot(0.12, TEAL).move_to([x, y, 0]) for x, y in [(-4.6, 0.5), (-2.2, 0.5), (2.0, 0.5), (4.4, 0.5)]])
        self.at("connected patches of equal area")
        self.play(FadeIn(species), run_time=0.6)
        gain = T("faster species gains", 28, TEAL).move_to([-3.3, -1.45, 0])
        self.at("gained plant species faster")
        new = dot(0.12, TEAL).move_to([-5.6, -0.4, 0])
        self.play(FadeIn(gain), FadeIn(new), run_time=0.3)
        self.play(new.animate.move_to([-4.15, 0.8, 0]), run_time=0.55)
        loss = T("slower species losses", 28, TEAL).move_to([-3.3, -2.15, 0])
        self.at("lost them more slowly")
        self.play(FadeOut(species[3]), FadeIn(loss), run_time=0.65)
        self.at("That does not establish")
        limit = T("One landscape: wider effects remain uncertain", 26, YELLOW).move_to([0, -3.05, 0])
        self.play(FadeIn(limit), run_time=0.6)
        self.at("Across conservation trials")
        clear(self)
        title = heading("Separate synthesis: conservation actions")
        action = chip("action", TEXT, 30).move_to([-3, 1.5, 0])
        noaction = chip("no action", GREY, 30).move_to([3, 1.5, 0])
        comparison = T("biodiversity outcomes compared", 26, GREY).move_to([0, 0.55, 0])
        self.play(FadeIn(title), FadeIn(action), FadeIn(noaction), FadeIn(comparison), run_time=0.6)
        base = hbar(9, -4.5, -0.6, GREY)
        better = hbar(6, -4.5, -0.6, GREEN)
        result = T("about two-thirds: improvement or slower decline", 28, GREEN).move_to([0, -1.65, 0])
        self.at("action improved biodiversity")
        self.play(FadeIn(base), run_time=0.4)
        self.at("about two -thirds")
        self.play(GrowFromEdge(better, LEFT), FadeIn(result), run_time=0.7)
        self.at("Recovery can still")
        clear(self)
        title = heading("Recovery can remain incomplete")
        ref = DashedLine([-5.4, 1.1, 0], [5.4, 1.1, 0], color=GREY)
        ref_label = T("complete recovery", 24, GREY).move_to([0, 1.65, 0])
        self.play(FadeIn(title), Create(ref), FadeIn(ref_label), run_time=0.5)
        self.at("Active restoration")
        active = chip("active restoration", TEAL, 28).move_to([-3, -1.45, 0])
        end = chip("end disturbance", TEAL, 28).move_to([3, -1.45, 0])
        bars = VGroup(Rectangle(width=1.0, height=1.4, color=TEAL, fill_opacity=0.3).move_to([-3, -0.3, 0]),
                      Rectangle(width=1.0, height=1.4, color=TEAL, fill_opacity=0.3).move_to([3, -0.3, 0]))
        self.play(FadeIn(active), FadeIn(end), GrowFromEdge(bars, DOWN), run_time=0.7)
        self.at("on average")
        note = T("No average advantage shown", 28).move_to([0, -2.35, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("though few studies")
        self.play(FadeIn(T("Few direct comparisons · schematic", 24, YELLOW).move_to([0, -3.05, 0])), run_time=0.5)
        self.finish()


class S02Luck(SpokenScene):
    def construct(self):
        title = heading("Why do small populations need help?")
        ar = arena(6.5, 3.6, [-2.5, 0])
        pop = scatter(5, 6.5, 3.6, [-2.5, 0], 0.3, seed=6, min_d=1)
        d = dice(1.8).move_to([3.8, 0.4, 0])
        self.at("Why give small", lead=0)
        self.play(FadeIn(title), FadeIn(ar), FadeIn(pop), run_time=0.7)
        self.at("who survives and breeds")
        self.play(FadeIn(d), run_time=0.3)
        self.play(Rotate(d, PI / 2), FadeOut(pop[3:]), run_time=0.8)
        self.at("Drift erodes genetic variation")
        variants = VGroup(*[Line([-4.5 + i * 1.0, -2.55, 0], [-4.5 + i * 1.0, -1.9, 0],
                               color=TEXT, stroke_width=6) for i in range(5)])
        vl = T("genetic variation", 26).move_to([2.8, -2.3, 0])
        self.play(FadeIn(variants), FadeIn(vl), run_time=0.35)
        self.play(variants[2:].animate.set_opacity(0.1), run_time=0.7)
        self.at("Inbreeding lowers survival")
        clear(self)
        title = heading("Inbreeding lowers survival and fertility")
        fewer = chip("fewer animals", TEXT, 30).move_to([-3.3, 1.2, 0])
        more = chip("more inbreeding", YELLOW, 30).move_to([3.3, 1.2, 0])
        lower = chip("lower survival", RED, 30).move_to([0, -1.7, 0])
        self.play(FadeIn(title), FadeIn(lower), run_time=0.6)
        self.at("Fewer animals mean")
        a = Arrow(fewer.get_right(), more.get_left(), buff=0.16, color=GREY)
        b = Arrow(more.get_bottom(), lower.get_right(), buff=0.18, color=GREY)
        c = Arrow(lower.get_left(), fewer.get_bottom(), buff=0.18, color=GREY)
        self.play(FadeIn(fewer), FadeIn(more), GrowArrow(a), GrowArrow(b), run_time=0.75)
        self.at("which can mean fewer")
        self.play(GrowArrow(c), Indicate(fewer, color=YELLOW), run_time=0.8)
        self.finish()


class S06Effective(SpokenScene):
    def construct(self):
        title = heading("Head count and effective size")
        census = hbar(10, -5, 1.5, TEXT)
        cl = T("N · census size", 28).move_to([0, 2.15, 0])
        self.at("The head count", lead=0)
        self.play(FadeIn(title), GrowFromEdge(census, LEFT), FadeIn(cl), run_time=0.7)
        el = T("Ne · effective size", 28, PURPLE).move_to([0, 0.5, 0])
        eff = hbar(10, -5, -0.15, PURPLE)
        definition = T("Ideal population with the same rate of genetic loss", 26, PURPLE).move_to([0, -1.05, 0])
        self.at("Effective size is")
        self.play(FadeIn(el), FadeIn(eff), FadeIn(definition), run_time=0.7)
        self.at("Unequal offspring numbers")
        parents = VGroup(dot(0.22).move_to([-3.5, -2, 0]), dot(0.22).move_to([3.5, -2, 0]))
        young = VGroup(*[dot(0.12).move_to([x, -3.0, 0]) for x in [-4.2, -3.5, -2.8, 3.5]])
        lines = VGroup(*[Line([-3.5 if x < 0 else 3.5, -2.25, 0], [x, -2.85, 0], color=GREY) for x in [-4.2, -3.5, -2.8, 3.5]])
        example = VGroup(parents, young, lines)
        self.play(FadeIn(example), run_time=0.7)
        self.at("uneven sex ratios")
        sex = VGroup(*[dot(0.25, BLUE if i == 0 else ORANGE).move_to([-2.1 + i * 1.05, -2.4, 0]) for i in range(5)])
        self.play(ReplacementTransform(example, sex), run_time=0.65)
        self.at("and population swings")
        swings = VMobject(color=TEXT, stroke_width=4).set_points_as_corners(
            [[-4, -2.8, 0], [-2, -1.8, 0], [0, -3.1, 0], [2, -2, 0], [4, -2.7, 0]])
        self.play(ReplacementTransform(sex, swings), run_time=0.65)
        self.at("usually make it smaller")
        self.play(Transform(eff, hbar(5.8, -5, -0.15, PURPLE)),
                  FadeIn(T("schematic · no fixed conversion", 22, GREY).move_to([0, -3.5, 0])), run_time=0.8)
        self.finish()


class S09Rescue(SpokenScene):
    def construct(self):
        title = heading("Genetic rescue: Florida panthers")
        tx = T("Texas donors", 28, ORANGE).move_to([-3.5, 2, 0])
        fl = T("existing Florida population", 28).move_to([2.9, 2, 0])
        ar = arena(5.6, 3.3, [2.9, -0.15])
        resident = scatter(3, 5.6, 3.3, [2.9, -0.15], 0.22, seed=3)
        self.at("Genetic rescue", lead=0)
        self.play(FadeIn(title), FadeIn(tx), FadeIn(fl), FadeIn(ar), FadeIn(resident), run_time=0.65)
        donors = VGroup(*[dot(0.19, ORANGE).move_to([-4.6 + (i % 4) * 0.65, 0.3 - (i // 4) * 0.7, 0]) for i in range(8)])
        release = T("1995 · eight females", 26, ORANGE).move_to([-3.5, -1.5, 0])
        self.at("After eight Texas females")
        self.play(FadeIn(donors), FadeIn(release), run_time=0.45)
        self.play(donors.animate.shift(RIGHT * 6.3), run_time=1.3)
        self.at("panther numbers")
        clear(self)
        title = heading("Reported assessment · 2010")
        counts = T("panther numbers", 28).move_to([-3.3, 1.9, 0])
        genetics = T("heterozygosity", 28).move_to([3.3, 1.9, 0])
        bars = VGroup(hbar(0.8, -4.7, 0.8, TEXT), hbar(0.8, 1.8, 0.8, TEXT))
        self.play(FadeIn(title), FadeIn(counts), FadeIn(genetics), FadeIn(bars), run_time=0.4)
        self.at("about tripled")
        self.play(Transform(bars[0], hbar(2.4, -4.7, 0.8, TEXT)),
                  FadeIn(T("about ×3", 30).move_to([-3.3, 0, 0])), run_time=0.65)
        self.at("heterozygosity doubled")
        self.play(Transform(bars[1], hbar(1.6, 1.8, 0.8, TEXT)),
                  FadeIn(T("×2", 30).move_to([3.3, 0, 0])), run_time=0.6)
        self.at("But managers must weigh")
        risk = T("Assess disease and donor suitability", 28, YELLOW).move_to([0, -1.2, 0])
        self.play(FadeIn(risk), run_time=0.55)
        self.at("Monitor survival")
        monitor = T("Monitor: survival · reproduction · genetics", 26, GREY).move_to([0, -2.2, 0])
        self.play(FadeIn(monitor), run_time=0.6)
        self.at("A later study")
        clear(self)
        title = heading("Later follow-up · 2016–2020")
        label = T("population stabilised, then declined", 30).move_to([0, -2.3, 0])
        track = VMobject(color=TEXT, stroke_width=5).set_points_as_corners(
            [[-5, 0.9, 0], [-2, 0.9, 0], [0, 0.85, 0], [2.5, 0, 0], [5, -0.8, 0]])
        note = T("schematic trend · no numerical scale", 22, GREY).move_to([0, -3.15, 0])
        self.play(FadeIn(title), FadeIn(note), run_time=0.5)
        self.at("population stabilized")
        self.play(Create(track), FadeIn(label), run_time=1.3)
        self.finish()


class S04Runs(SpokenScene):
    def construct(self):
        title = heading("Population viability analysis")
        self.at("Population viability analysis", lead=0)
        ax = VGroup(Line([-5.8, -1.3, 0], [5.8, -1.3, 0], color=GREY),
                    Line([-5.8, -1.3, 0], [-5.8, 2, 0], color=GREY),
                    T("chosen time horizon →", 24, GREY).move_to([0, -1.9, 0]),
                    T("solid: option A · dashed: option B · schematic runs", 24, GREY).move_to([0, 2.35, 0]))
        # Several runs per option; most persist, a few reach the extinction baseline.
        paths = VGroup()
        extinct = VGroup()
        for i in range(16):
            xs = np.linspace(-5.7, 5.6, 60)
            t = np.linspace(0, 1, 60)
            dies_out = i in (6, 7, 14, 15)
            trend = -2.5 - 0.12 * (i % 4) if dies_out else 0.1 + 0.19 * (i % 6)
            ys = 0.35 + 0.07 * (i % 4) + 0.18 * np.sin(t * (9 + i)) + trend * t
            ys = np.clip(ys, -1.3, 1.9)
            path = VMobject(color=RED if dies_out else TEXT, stroke_width=1.6).set_points_as_corners(
                [[x, y, 0] for x, y in zip(xs, ys)])
            if i >= 8:
                path = DashedVMobject(path, num_dashes=30)
            paths.add(path)
            if dies_out:
                extinct.add(path)
        # Begin drawing with the opening title, rather than leaving empty axes.
        self.play(FadeIn(title), FadeIn(ax),
                  LaggedStart(*[Create(paths[i]) for i in (0, 1, 8, 9)], lag_ratio=0.12), run_time=1.8)
        self.at("compare management options")
        self.play(LaggedStart(*[Create(paths[i]) for i in (2, 3, 10, 11)], lag_ratio=0.12), run_time=1.0)
        self.at("Run a population model")
        self.play(LaggedStart(*[Create(paths[i]) for i in (4, 5, 6, 7, 12, 13, 14, 15)],
                              lag_ratio=0.1), run_time=1.8)
        self.at("The fraction that goes extinct")
        formula = T("extinction risk = extinct runs / total runs", 30, YELLOW).move_to([0, -2.9, 0])
        self.play(FadeIn(formula), Indicate(extinct, color=RED, scale_factor=1), run_time=0.7)
        self.at("A minimum viable population")
        clear(self)
        title = heading("Minimum viable population")
        rule = T("smallest isolated population meeting the chosen target", 28).move_to([0, 1.95, 0])
        conditions = VGroup(*[chip(s, c, 28).move_to([x, 0.5, 0]) for s, c, x in
                             [("persistence target", YELLOW, -4.1), ("time", TEXT, 0), ("habitat", TEAL, 4.1)]])
        self.play(FadeIn(title), FadeIn(rule), FadeIn(conditions), run_time=0.7)
        self.at("Read model results")
        caution = T("Read with assumptions and uncertainty", 30, YELLOW).move_to([0, -0.8, 0])
        self.play(FadeIn(caution), run_time=0.6)
        self.at("Even the ranking")
        ranking = VGroup(chip("option A", TEXT, 28).move_to([-2, -1.65, 0]),
                         chip("option B", TEXT, 28).move_to([2, -1.65, 0]))
        structure = T("model structure changes → ranking can change", 26, GREY).move_to([0, -3.1, 0])
        rank_labels = VGroup(T("higher rank", 26, GREY).move_to([-2, -2.3, 0]),
                             T("lower rank", 26, GREY).move_to([2, -2.3, 0]))
        self.play(FadeOut(rule), FadeIn(ranking), FadeIn(structure), FadeIn(rank_labels), run_time=0.5)
        self.at("can change with model structure")
        self.play(ranking[0].animate.move_to([2, -1.65, 0]), ranking[1].animate.move_to([-2, -1.65, 0]), run_time=0.9)
        self.finish()


class S10Decisions(SpokenScene):
    def construct(self):
        title = heading("Cultus Lake: compare goals and tradeoffs")
        alternatives = chip("management alternatives", TEXT, 28).move_to([-3.4, 1.7, 0])
        outcomes = chip("predicted consequences", TEXT, 28).move_to([3.4, 1.7, 0])
        arrow = Arrow(alternatives.get_right(), outcomes.get_left(), buff=0.1, color=GREY)
        self.at("Evidence says", lead=0)
        self.play(FadeIn(title), FadeIn(alternatives), GrowArrow(arrow), FadeIn(outcomes), run_time=0.8)
        self.at("It does not choose")
        question = T("Which outcomes matter most?", 30, YELLOW).move_to([0, 0.6, 0])
        self.play(FadeIn(question), run_time=0.6)
        goals = VGroup(*[chip(s, TEXT, 28).move_to([x, -0.6, 0]) for x, s in
                        [(-4.1, "biological"), (0, "social"), (4.1, "economic")]])
        self.at("Set out biological")
        self.play(FadeOut(question), FadeIn(goals[0]), run_time=0.5)
        self.at("social")
        self.play(FadeIn(goals[1]), run_time=0.3)
        self.at("economic goals")
        self.play(FadeIn(goals[2]), run_time=0.35)
        people = T("fishery agencies · First Nations · commercial fishers", 25, GREY).move_to([0, -1.85, 0])
        self.at("with the people affected")
        self.play(FadeIn(people), run_time=0.6)
        self.at("then compare the trade")
        trade = T("Compare the tradeoffs together", 32, YELLOW).move_to([0, -3, 0])
        self.play(FadeIn(trade), Indicate(goals, color=YELLOW, scale_factor=1.03), run_time=0.7)
        self.finish()


class S07End(EndCard):
    TITLE = "Protect Habitat, Support Recovery"
    LINE = "Remove the cause of decline, and protect, connect and restore habitat."

    def construct(self):
        title = T(self.TITLE, 34, font=TITLE_FONT)
        line = T(self.LINE.replace(", and protect, ", ",\nand protect,\n"), 30,
                 font=TITLE_FONT, line_spacing=1.15)
        sub = T("biochemistrypedia.com", 22, TEAL)
        VGroup(title, line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(title), FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
