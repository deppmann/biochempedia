"""The Charge That Changes the Odds — phosphorylation switch explainer.

Protein copies are schematic teal blocks that flex between compact and open states.
The same builders are used whenever a picture is carried across a scene boundary.
"""
from bp_parts import *


VIOLET = "#B58CD9"
PROTEIN = TEAL
PHOSPHATE = GOLD
KINASE = BLUE
PHOSPHATASE = RED
ATP = VIOLET


def phosphate_badge(scale=1.0):
    r = max(0.23 * scale, 0.24)
    c = Circle(radius=r, stroke_color=PHOSPHATE, stroke_width=3,
               fill_color=PHOSPHATE, fill_opacity=1)
    p = T("P", max(24 * scale, 22), BG, weight=BOLD).move_to(c)
    return VGroup(c, p)


def protein_block(center=ORIGIN, open_state=False, scale=1.0, phosphorylated=False):
    """One labelled-cartoon protein; compact/open are two arrangements, not two proteins."""
    w, h = ((2.43, 1.35) if open_state else (1.89, 1.78))
    body = RoundedRectangle(corner_radius=0.32, width=w * scale, height=h * scale,
                            stroke_color=PROTEIN, stroke_width=5,
                            fill_color=PROTEIN, fill_opacity=0.38)
    cleft = Arc(radius=0.34 * scale, start_angle=-PI / 2, angle=PI,
                stroke_color=PROTEIN, stroke_width=4).move_to(body.get_right() + LEFT * 0.05 * scale)
    g = VGroup(body, cleft).move_to(center)
    if phosphorylated:
        if scale < 0.65:
            badge = Dot(radius=0.10, color=PHOSPHATE)
        else:
            badge = phosphate_badge(0.82 * scale)
        badge.move_to(body.get_corner(UR) + LEFT * 0.42 * scale + DOWN * 0.38 * scale)
        g.add(badge)
    return g


def keep_alive(proteins):
    """Continuous breathing outlines; enough motion to make a held sentence visibly alive."""
    items = proteins if isinstance(proteins, VGroup) and len(proteins) and isinstance(proteins[0], VGroup) else [proteins]
    for i, p in enumerate(items):
        if len(p) >= 2:
            pulse(p[0], base=5.0, amp=1.8, speed=1.25 + 0.08 * i)
            pulse(p[1], base=4.0, amp=1.3, speed=1.35 + 0.07 * i)
    return proteins


def breathe_until(scene, phrase, subject, scale=1.06):
    """Use time before a cue for a slow flex instead of a frozen wait."""
    rest = scene.t_of(phrase) - 0.2 - scene.elapsed()
    if rest > 0.05:
        scene.play(subject.animate.scale(scale), rate_func=there_and_back, run_time=rest)


def cycle_until(scene, phrase, objs, color=None):
    """Visible motion in a long wait: pulse each object in turn until the cue."""
    i = 0
    while scene.t_of(phrase) - 0.2 - scene.elapsed() > 0.9:
        scene.play(Indicate(objs[i % len(objs)], scale_factor=1.12, color=color), run_time=0.9)
        i += 1
    breathe_until(scene, phrase, objs[0], 1.04)


POP_POS = [(-4.8, 1.65), (-2.25, 1.65), (0.3, 1.65), (2.85, 1.65),
           (-4.8, -1.05), (-2.25, -1.05), (0.3, -1.05), (2.85, -1.05)]


def protein_population(states=(0, 1, 0, 1, 1, 0, 1, 0), phosphorylated=False, scale=0.90):
    return VGroup(*[protein_block([x, y, 0], bool(s), scale, phosphorylated)
                    for (x, y), s in zip(POP_POS, states)])


def factory_picture():
    box = RoundedRectangle(corner_radius=0.18, width=2.0, height=2.25,
                           stroke_color=GREY, stroke_width=3, fill_color=GREY,
                           fill_opacity=0.08).move_to([5.25, 0.25, 0])
    belt = Line([4.45, -0.42, 0], [6.05, -0.42, 0], color=GREY, stroke_width=5)
    gears = VGroup(*[Circle(radius=0.17, color=GREY, stroke_width=3).move_to([x, -0.72, 0])
                     for x in (4.7, 5.25, 5.8)])
    lab = T("new protein", 24, GREY).move_to([5.25, 0.96, 0])
    mini = protein_block([5.25, 0.25, 0], False, 0.38).set_opacity(0.45)
    return VGroup(box, belt, gears, lab, mini)


PREDICT_QUESTION = "Must phosphorylation always activate its target?"
PREDICT_OPTIONS = ["active", "inhibited", "depends on target"]


def prediction_world():
    prot = protein_block([0, 0.45, 0], True, 1.35, True)
    choices = VGroup(*[boxed_label(x, c, size=30, pad=0.3) for x, c in
                       zip(PREDICT_OPTIONS, (GREEN, RED, PHOSPHATE))])
    choices.arrange(RIGHT, buff=0.55).move_to([0, -1.65, 0])
    return VGroup(prot, choices)


def tally_group(center, open_count, label, accent):
    title = fit_text(label, max_w=5.0, size=30, color=TEXT, max_lines=2).move_to(center + UP * 1.72)
    blocks = VGroup(*[protein_block(ORIGIN, i < open_count, 0.36, True) for i in range(5)])
    blocks.arrange(RIGHT, buff=0.22).move_to(center + UP * 0.42)
    compact = Rectangle(width=4.45, height=0.42, stroke_color=GREY, stroke_width=2).move_to(center + DOWN * 0.7)
    fill = Rectangle(width=0.65 + 0.65 * open_count, height=0.36, stroke_width=0,
                     fill_color=accent, fill_opacity=0.8).align_to(compact, LEFT).move_to(compact, aligned_edge=LEFT)
    result = T("toward active" if accent == GREEN else "toward inhibited", 28, accent).move_to(center + DOWN * 1.35)
    return VGroup(title, blocks, compact, fill, result)


class S00Hook(SpokenScene):
    def construct(self):
        states = [0, 1, 0, 1, 1, 0, 1, 0]
        pop = protein_population(states)
        keep_alive(pop)
        factory = factory_picture()
        q = T("?", 70, PHOSPHATE, weight=BOLD).next_to(pop[2], UP, buff=0.2)
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in pop], lag_ratio=0.08), run_time=1.7)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        breathe_until(self, "Watch this population", pop)
        new_states = [1 - s for s in states]
        self.play(*[Transform(p, protein_block(p.get_center(), bool(s), 0.90))
                    for p, s in zip(pop, new_states)], q.animate.next_to(pop[2], UP, buff=0.2), run_time=2.2)
        self.at("Each copy flickers")
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), bool(states[i]), 0.90))
                    for i in (0, 2, 3, 5, 7)], run_time=2.0)
        contacts = VGroup(*[Line(pop[i].get_right(), pop[i + 1].get_left(), color=GREY, stroke_width=3)
                            for i in (0, 1, 4, 5)])
        self.at("different contacts")
        self.play(LaggedStart(*[Create(x) for x in contacts], lag_ratio=0.15), run_time=1.2)
        self.at("change the odds")
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), True, 0.90)) for i in (0, 1, 4, 6)],
                  *[Transform(pop[i], protein_block(pop[i].get_center(), False, 0.90)) for i in (2, 3, 5, 7)],
                  FadeOut(contacts), run_time=2.2)
        self.at("not manufacture")
        self.play(FadeIn(factory, shift=LEFT * 0.2), q.animate.next_to(pop[6], UP, buff=0.2), run_time=1.0)
        self.at("faster than waiting")
        self.play(LaggedStart(*[p.animate.shift(UP * 0.08).shift(DOWN * 0.08) for p in pop], lag_ratio=0.08),
                  factory.animate.set_opacity(0.28), run_time=2.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Phosphorylation switch"
    TITLE = "The Charge That Changes the Odds"

    def construct(self):
        pop = protein_population(scale=0.35).scale(0.75).move_to([0, -1.9, 0]).set_opacity(0.42)
        keep_alive(pop)
        title = fit_text(self.TITLE, max_w=11.2, size=52, color=TEXT, font=TITLE_FONT).move_to([0, 0.55, 0])
        lesson = T(self.LESSON.upper(), 24, PROTEIN).next_to(title, UP, buff=0.4)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=PHOSPHATE, stroke_width=4).next_to(title, DOWN, buff=0.36)
        self.add(pop)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=0.9)
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), i % 2 == 0, 0.26)) for i in range(8)], run_time=0.8)
        self.play(FadeOut(VGroup(pop, lesson, title, rule)), run_time=0.3)
        self.finish()


class S02Write(SpokenScene):
    def construct(self):
        prot = protein_block([2.7, 0.0, 0], False, 1.90)
        keep_alive(prot)
        site = Dot(prot[0].get_top() + LEFT * 0.55, radius=0.12, color=GREY)
        site_lab = T("hydroxyl site", 28, GREY).move_to([2.25, 2.55, 0])
        ptr = Line(site_lab.get_bottom(), site.get_center() + UP * 0.08, color=GREY, stroke_width=3)
        kinase = boxed_label("kinase", KINASE, size=34, pad=0.34).move_to([-2.1, 0.4, 0])
        atp = boxed_label("ATP", ATP, size=34, pad=0.34).move_to([-5.0, 0.4, 0])
        badge = phosphate_badge(1.15).next_to(atp, UP, buff=0.18)
        self.play(FadeIn(prot), run_time=1.0)
        self.play(FadeIn(site), FadeIn(site_lab), Create(ptr), run_time=0.8)
        self.at("a TP beside")
        self.play(FadeIn(kinase), FadeIn(atp), FadeIn(badge, scale=0.5), run_time=1.0)
        self.play(atp.animate.next_to(kinase, LEFT, buff=0.15), badge.animate.next_to(kinase, UP, buff=0.15), run_time=1.0)
        self.at("transfers the end phosphate")
        self.play(badge.animate.move_to(site.get_center() + DOWN * 0.68 + LEFT * 0.12), run_time=1.3)
        adp = boxed_label("ADP", ATP, size=34, pad=0.34).move_to(atp)
        self.at("leaving a DP")
        self.play(swap(atp, adp, run_time=0.8), run_time=0.8)
        self.play(adp.animate.shift(LEFT * 1.2).set_opacity(0), run_time=0.7)
        names = VGroup(*[boxed_label(n, PROTEIN, size=28, pad=0.2) for n in ("serine", "threonine", "tyrosine")])
        names.arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        self.at("best studied targets")
        self.play(FadeOut(site_lab), FadeOut(ptr), LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in names], lag_ratio=0.25), run_time=1.8)
        chain = prot[0].copy().set_stroke(width=9, opacity=0.65).set_fill(opacity=0)
        breathe_until(self, "same chain", prot)
        self.play(Create(chain), run_time=1.2)
        self.at("local chemistry has changed")
        self.play(Indicate(badge, color=PHOSPHATE, scale_factor=1.35), run_time=1.0)
        cov = caption("reversible covalent modification", color=PHOSPHATE)
        breathe_until(self, "reversible covalent", prot)
        self.play(FadeOut(names), FadeIn(cov, shift=UP * 0.15), run_time=1.0)
        self.play(Transform(prot, protein_block(prot.get_center(), True, 1.90)), run_time=1.4)
        self.finish()


class S03Charge(SpokenScene):
    def construct(self):
        pop = protein_population(phosphorylated=True)
        keep_alive(pop)
        ph = T("near pH 7", 30, TEXT).move_to([-4.7, 3.15, 0])
        charge = boxed_label("about −2", PHOSPHATE, size=30, pad=0.26).move_to([-2.5, 3.15, 0])
        self.play(FadeIn(pop), run_time=1.0)
        self.at("strong negative charge")
        self.play(FadeIn(ph), FadeIn(charge), run_time=0.8)
        marks = VGroup()
        for p in pop:
            marks.add(T("+", 22, BLUE).move_to(p.get_center() + LEFT * 0.38),
                      T("−", 22, PHOSPHATE).move_to(p.get_center() + DOWN * 0.34))
        self.at("among the protein's other charges")
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.05), run_time=1.4)
        self.at("Attractions strengthen")
        self.play(*[m.animate.shift((UP if i % 2 else DOWN) * 0.12) for i, m in enumerate(marks)], run_time=1.5)
        breathe_until(self, "population shifts", pop)
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), i not in (2, 6), 0.90, True)) for i in range(8)],
                  *[m.animate.shift((RIGHT if i % 2 else LEFT) * 0.10) for i, m in enumerate(marks)], run_time=2.1)
        mini_pop = protein_population((1, 1, 0, 1, 1, 0, 1, 1), True, scale=0.5)
        mini_pop.scale(0.72).move_to([-3.75, 0.25, 0])
        keep_alive(mini_pop)
        self.play(FadeOut(marks), FadeOut(ph), FadeOut(charge), FadeOut(pop), FadeIn(mini_pop), run_time=1.1)
        pop = mini_pop
        bars = VGroup()
        for i, (lab, n, col) in enumerate((("compact", 2, GREY), ("open", 6, PHOSPHATE))):
            y = 0.8 - i * 1.3
            label = T(lab, 28, col).move_to([1.9, y, 0])
            frame = Rectangle(width=3.2, height=0.48, color=GREY, stroke_width=2).move_to([4.5, y, 0])
            fill = Rectangle(width=0.45 * n, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85)
            fill.move_to(frame, aligned_edge=LEFT)
            bars.add(VGroup(label, frame, fill))
        tall = fit_text("population shift, schematic states", max_w=5.0, size=28, color=TEXT).move_to([3.7, 2.25, 0])
        self.play(FadeIn(tall), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2), run_time=1.2)
        self.at("Partners can also read")
        partner = Arc(radius=0.55, start_angle=-PI / 2, angle=PI, color=BLUE, stroke_width=9).move_to([3.7, -1.65, 0])
        pb = phosphate_badge(1.0).move_to([4.6, -1.65, 0])
        self.play(FadeIn(partner), FadeIn(pb), pb.animate.move_to([4.48, -1.65, 0]), run_time=1.3)
        rule = caption("Phosphate changes probabilities — not a universal command.", color=PHOSPHATE)
        self.at("Phosphate changes probabilities")
        self.play(FadeOut(tall), FadeOut(bars), FadeIn(rule), run_time=1.0)
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), i not in (2, 5), 0.36, True))
                    for i in range(8)], run_time=1.4)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = prediction_world()
        prot, choices = world
        keep_alive(prot)
        self.play(FadeIn(prot), run_time=0.8)
        self.at("Here is your prediction")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in choices], lag_ratio=0.18), run_time=1.2)
        q = question_card(PREDICT_QUESTION, y=3.15, max_w=11.0, size=34)
        self.at("chemical mark is always the same")
        self.play(FadeIn(q.question), run_time=0.8)
        self.at("always activate")
        self.play(prot.animate.scale(1.08), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = PREDICT_QUESTION
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": 3.15, "max_w": 11.0, "size": 34}

    def backdrop(self):
        world = prediction_world()
        bob(world[0], amp=0.055, speed=1.4)
        keep_alive(world[0])
        return world


class S06Direction(SpokenScene):
    def construct(self):
        tp = TwoPanel("glycogen phosphorylase", "glycogen synthase", colors=(GREEN, RED), top=3.0, bottom=-2.45)
        left = tally_group(np.array([-3.35, -0.05, 0]), 4, "", GREEN)
        right = tally_group(np.array([3.35, -0.05, 0]), 3, "", RED)
        left.remove(left[0]); right.remove(right[0])
        keep_alive(left[0]); keep_alive(right[0])
        self.play(FadeIn(tp), run_time=1.0)
        self.at("toward activity")
        self.play(FadeIn(left), run_time=1.4)
        self.at("inhibits glycogen synthase")
        self.play(FadeIn(right), run_time=1.4)
        self.play(*[Transform(left[0][i], protein_block(left[0][i].get_center(), i != 4, 0.36, True)) for i in range(5)],
                  *[Transform(right[0][i], protein_block(right[0][i].get_center(), i in (0, 4), 0.36, True)) for i in range(5)], run_time=1.8)
        answer = caption("depends on target", size=36, color=PHOSPHATE)
        self.at("direction depends")
        self.play(FadeIn(answer, shift=UP * 0.15), run_time=0.8)
        self.at("same charge can favor")
        self.play(left[0].animate.scale(1.07), right[0].animate.scale(1.07), rate_func=there_and_back, run_time=2.2)
        self.finish()


class S07Outcomes(SpokenScene):
    def construct(self):
        prot = protein_block([0, 0.1, 0], True, 1.85, True)
        keep_alive(prot)
        self.play(FadeIn(prot), run_time=0.9)
        dock_lab = T("docking", 32, PHOSPHATE).move_to([-4.7, 2.7, 0])
        partner = Arc(radius=0.85, start_angle=-PI / 2, angle=PI, color=BLUE, stroke_width=12).move_to([-3.1, 0.1, 0])
        self.at("contact not catalytic activity")
        self.play(FadeIn(dock_lab), FadeIn(partner), run_time=0.8)
        breathe_until(self, "surface and dock", prot, 1.09)
        self.play(partner.animate.move_to([-1.35, 0.1, 0]), run_time=1.3)
        loc_lab = T("location", 32, PHOSPHATE).move_to([0, 2.7, 0])
        tag = boxed_label("location signal", PROTEIN, size=28).move_to([0, 0.1, 0]).set_opacity(0)
        cover = Rectangle(width=2.7, height=0.6, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(tag)
        self.at("Elsewhere")
        self.play(FadeOut(partner), FadeIn(loc_lab), FadeIn(tag), FadeIn(cover), run_time=0.9)
        self.at("expose or hide")
        self.play(cover.animate.shift(DOWN * 1.1), run_time=1.3)
        prime_lab = T("priming", 32, PHOSPHATE).move_to([4.7, 2.7, 0])
        site = Dot([1.0, -0.25, 0], radius=0.13, color=GREY)
        kinase = boxed_label("kinase", KINASE, size=30).move_to([5.0, 0.1, 0])
        breathe_until(self, "prepare a nearby site", prot, 1.08)
        self.play(FadeOut(tag), FadeOut(cover), FadeIn(prime_lab), FadeIn(site), run_time=1.0)
        self.at("another kinase")
        self.play(FadeIn(kinase), kinase.animate.move_to([3.25, 0.1, 0]), run_time=1.3)
        sequence = VGroup(dock_lab, loc_lab, prime_lab)
        self.at("different outcomes")
        self.play(LaggedStart(*[Indicate(x, color=PHOSPHATE, scale_factor=1.15) for x in sequence], lag_ratio=0.25), run_time=2.3)
        self.play(Transform(prot, protein_block([0, 0.1, 0], False, 1.85, True)), run_time=1.4)
        self.finish()


class S08Erase(SpokenScene):
    def construct(self):
        upper = Line([-5.8, 1.45, 0], [5.8, 1.45, 0], color=GREY, stroke_width=2)
        lower = Line([-5.8, -1.0, 0], [5.8, -1.0, 0], color=GREY, stroke_width=2)
        kinase = boxed_label("kinase", KINASE, 30).move_to([-4.7, 2.25, 0])
        phosphatase = boxed_label("phosphatase", PHOSPHATASE, 30).move_to([-4.5, -1.85, 0])
        prot = protein_block([0.4, -1.85, 0], True, 1.10, True)
        keep_alive(prot)
        water = boxed_label("water", TEXT, 28).move_to([-2.2, -1.85, 0])
        self.play(Create(lower), FadeIn(prot), run_time=1.0)
        self.at("enzyme removes it")
        self.play(FadeIn(phosphatase), run_time=0.8)
        self.at("uses water")
        self.play(FadeIn(water), water.animate.next_to(phosphatase, RIGHT, buff=0.25), run_time=0.9)
        free_p = phosphate_badge(0.9).move_to(prot[2])
        free_p.set_opacity(0)
        self.add(free_p)
        unmod = protein_block(prot.get_center(), True, 1.10, False)
        self.at("release inorganic phosphate")
        self.play(Transform(prot, unmod), free_p.animate.set_opacity(1).move_to([2.65, -1.85, 0]), run_time=1.4)
        pi = T("inorganic phosphate", 28, PHOSPHATE).next_to(free_p, RIGHT, buff=0.2)
        self.play(FadeIn(pi), run_time=0.7)
        breathe_until(self, "does not reverse", prot, 1.08)
        self.play(Create(upper), FadeIn(kinase), run_time=0.8)
        reverse = Arrow([2.8, 2.25, 0], [0.3, 2.25, 0], color=GREY, stroke_width=4, buff=0.1)
        cross = VGroup(Line([1.25, 1.85, 0], [1.85, 2.65, 0], color=RED, stroke_width=7),
                       Line([1.85, 1.85, 0], [1.25, 2.65, 0], color=RED, stroke_width=7))
        self.play(GrowArrow(reverse), Create(cross), run_time=1.0)
        breathe_until(self, "separate reactions", prot, 1.08)
        self.play(Indicate(kinase, color=KINASE), Indicate(phosphatase, color=PHOSPHATASE), run_time=1.1)
        spent = ValueTracker(1)
        count = counter("ATP available: {:.0f}", spent, at=[4.5, 3.15, 0], size=28, color=ATP)
        self.add(count)
        breathe_until(self, "complete trip spends", prot, 1.08)
        self.play(spent.animate.set_value(0), run_time=1.5)
        self.finish()


class S09Control(SpokenScene):
    def construct(self):
        pop = protein_population(phosphorylated=True)
        keep_alive(pop)
        factory = factory_picture().set_opacity(0.25)
        kinase = boxed_label("kinase", KINASE, 28).move_to([-5.0, 3.15, 0])
        atps = VGroup(*[boxed_label("ATP", ATP, 24, pad=0.15).move_to([-3.6 + i * 1.05, 3.15, 0]) for i in range(3)])
        self.play(FadeIn(pop), FadeIn(factory), run_time=1.0)
        self.at("stable and reversible")
        self.play(*[Indicate(p[2], color=PHOSPHATE, scale_factor=1.25) for p in pop], run_time=1.3)
        self.at("plentiful enough")
        self.play(FadeIn(kinase), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in atps], lag_ratio=0.15), run_time=1.2)
        breathe_until(self, "persists without an eraser", pop)
        self.play(*[Transform(pop[i], protein_block(pop[i].get_center(), i % 3 != 0, 0.90, True)) for i in range(8)], run_time=2.0)
        phosphatase = boxed_label("phosphatase", PHOSPHATASE, 28).move_to([-5.1, -2.55, 0])
        self.at("phosphatase acts")
        self.play(FadeIn(phosphatase), run_time=0.7)
        for inds in ((0, 4), (1, 5), (2, 6), (3, 7)):
            self.play(phosphatase.animate.shift(RIGHT * 1.15),
                      *[Transform(pop[i], protein_block(pop[i].get_center(), i % 2 == 0, 0.90, False)) for i in inds],
                      run_time=0.65)
        fast = caption("alter existing proteins", color=PROTEIN)
        self.at("faster than rebuilding")
        self.play(FadeOut(VGroup(phosphatase, kinase, atps)), FadeIn(fast), factory.animate.set_opacity(0.10),
                  *[p.animate.shift(UP * 0.08).shift(DOWN * 0.08) for p in pop], run_time=1.8)
        self.finish()


class S10Apply(SpokenScene):
    def construct(self):
        prot = protein_block([0, 0.15, 0], True, 1.55)
        keep_alive(prot)
        self.play(FadeIn(prot), run_time=0.8)
        labels = [boxed_label("activity", GREEN, 27), boxed_label("inhibition", RED, 27),
                  boxed_label("docking", BLUE, 27), boxed_label("movement", PROTEIN, 27),
                  boxed_label("priming", KINASE, 27)]
        poses = [(-4.4, 1.8), (-4.4, -1.6), (0, 3.15), (4.4, 1.8), (4.4, -1.6)]
        for lab, pos in zip(labels, poses):
            lab.move_to([*pos, 0])
        self.at("Ask where the phosphate appears")
        badge = phosphate_badge(1.05).move_to([-2.8, 0.15, 0])
        self.play(FadeIn(badge), badge.animate.move_to(prot.get_center() + UP * 0.58), run_time=1.4)
        self.at("which shapes or partners")
        self.play(Transform(prot, protein_block(prot.get_center(), False, 1.55, False)), run_time=1.2)
        breathe_until(self, "outcome may be", prot, 1.08)
        self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in labels], lag_ratio=0.14), run_time=2.0)
        arrow_list = []
        for i, x in enumerate(labels):
            if i == 2:  # the docking icon sits directly above; no connector is needed
                continue
            direction = x.get_center() - prot.get_center()
            direction = direction / np.linalg.norm(direction)
            arrow_list.append(Arrow(prot.get_center() + 1.45 * direction, x.get_center(), buff=0.90,
                                    color=GREY, stroke_width=3, tip_length=0.16))
        arrows = VGroup(*arrow_list)
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.1), run_time=1.3)
        eraser = boxed_label("phosphatase", PHOSPHATASE, 28).move_to([-3.9, -2.65, 0])
        cycle_until(self, "stable phosphate", [labels[0], labels[3], labels[4], labels[1], labels[2]])
        self.play(Indicate(badge, color=PHOSPHATE, scale_factor=1.35), run_time=0.8)
        breathe_until(self, "enzyme can erase", badge, 1.16)
        eraser.move_to([-1.3, -3.2, 0])
        self.play(FadeIn(eraser), eraser.animate.move_to([-1.3, -2.25, 0]), run_time=1.0)
        final_badge = phosphate_badge(1.55).move_to([0, 0.15, 0])
        self.play(FadeOut(VGroup(prot, arrows, eraser, *labels)), Transform(badge, final_badge), run_time=1.5)
        self.finish()


class S11End(EndCard):
    LINE = "A stable, removable phosphate changes protein behavior through its charge and shape."
