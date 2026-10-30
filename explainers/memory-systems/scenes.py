"""Memory systems: opposite failures separate memory systems  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = declarative memory / the questionnaire task (memory for the training)
  PURPLE = skill learning / the probabilistic classification task
  TEAL   = working memory
  GREY   = controls, frames, de-emphasized
  ORANGE = amnesic patients
  GOLD   = Parkinson's patients
  YELLOW = chance level (guessing)
  GREEN  = kept / passes        RED = lost / fails
  TEXT   = the double-dissociation claim and the take-home
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SC = 0.036          # scene units per percentage point
BASE = -1.9         # y of 0 % on the score panels


def tick(c=GREEN, s=0.2, w=6):
    return VGroup(Line([-s, 0, 0], [-s * 0.3, -s * 0.8, 0], color=c, stroke_width=w),
                  Line([-s * 0.3, -s * 0.8, 0], [s, s * 0.9, 0], color=c, stroke_width=w))


def cross(c=RED, s=0.2, w=6):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=c, stroke_width=w),
                  Line([-s, s, 0], [s, -s, 0], color=c, stroke_width=w))


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tag():
    return T("invented numbers, not the study's data", 22, GREY).move_to([0, 3.4, 0])


GCOL = {"ctrl": GREY, "am": ORANGE, "pd": GOLD}
VALS = {"ctrl": (70, 80), "am": (68, 40), "pd": (52, 78)}
CHANCE = (50, 25)


class Panel:
    """One score panel (task idx 0 classification, 1 questionnaire), drawn without LaTeX."""

    def __init__(self, cx, idx):
        self.cx, self.idx = cx, idx
        col = PURPLE if idx == 0 else BLUE
        name = "Classification" if idx == 0 else "Questionnaire"
        sub = "2 choices, chance 50%" if idx == 0 else "4 choices, chance 25%"
        ax_x = cx - 2.2
        self.axis = VGroup(Line([ax_x, BASE, 0], [ax_x, BASE + 100 * SC, 0], color=GREY, stroke_width=3),
                           Line([ax_x, BASE, 0], [cx + 2.3, BASE, 0], color=GREY, stroke_width=3))
        for v in (0, 50, 100):
            self.axis.add(M(str(v), 22, GREY).move_to([ax_x - 0.33, BASE + v * SC, 0]))
        self.title = VGroup(T(name, 28, col, weight=BOLD).move_to([cx, 2.78, 0]),
                            T(sub, 22, GREY).move_to([cx, 2.3, 0]))
        y = BASE + CHANCE[idx] * SC
        self.chance = DashedLine([ax_x, y, 0], [cx + 2.3, y, 0], color=YELLOW, stroke_width=4, dash_length=0.14)
        self.xs = {"ctrl": cx - 0.9, "am": cx + 0.3, "pd": cx + 1.5}
        self.bars, self.labs = {}, {}
        for g in ("ctrl", "am", "pd"):
            v = VALS[g][idx]
            b = Rectangle(width=0.8, height=v * SC, stroke_color=GCOL[g], stroke_width=3,
                          fill_color=GCOL[g], fill_opacity=0.55)
            b.move_to([self.xs[g], BASE + v * SC / 2, 0])
            self.bars[g] = b
            self.labs[g] = M(str(v), 22, TEXT).move_to([self.xs[g], BASE + v * SC + 0.28, 0])
        self.base = VGroup(self.axis, self.title)


def legend(y=-2.75):
    items = []
    for key, name in (("ctrl", "Controls"), ("am", "Amnesic patients"), ("pd", "Parkinson's patients")):
        sw = Square(0.26, stroke_color=GCOL[key], fill_color=GCOL[key], fill_opacity=0.6, stroke_width=3)
        items.append(VGroup(sw, T(name, 22, TEXT).next_to(sw, RIGHT, buff=0.15)))
    sw = DashedLine(LEFT * 0.2, RIGHT * 0.2, color=YELLOW, stroke_width=4, dash_length=0.1)
    items.append(VGroup(sw, T("chance", 22, TEXT).next_to(sw, RIGHT, buff=0.15)))
    return VGroup(*items).arrange(RIGHT, buff=0.5).move_to([0, y, 0])


def build_panels():
    return Panel(-3.4, 0), Panel(3.4, 1)


class S00Title(TitleCard):
    LESSON = "Memory systems"
    TITLE = "Opposite failures separate memory systems"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        t1 = T("1953", 56, font=TITLE_FONT).move_to([0, 1.3, 0])
        t2 = chip("Inner part of both temporal lobes removed", GREY, 30).move_to([0, 0.1, 0])
        t3 = chip("severe epilepsy", GREY, 28).move_to([0, -1.2, 0])
        self.at("In 1953")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("removed tissue")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        self.at("severe epilepsy")
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.6)

        head = T("1953 · patient H.M. · inner part of both temporal lobes removed", 24, GREY).move_to([0, 3.15, 0])
        fit(head, max_w=12.2)
        self.at("the patient known")
        self.play(ReplacementTransform(VGroup(t1, t2, t3), head), run_time=0.9)

        # left card: events
        cl = RoundedRectangle(corner_radius=0.2, width=5.8, height=4.3, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.06).move_to([-3.4, 0.3, 0])
        ct = T("Events from an hour ago", 28, BLUE, weight=BOLD).move_to([-3.4, 1.85, 0])
        dots = VGroup(*[Circle(0.28, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
                        for _ in range(3)]).arrange(RIGHT, buff=0.55).move_to([-3.4, 0.7, 0])
        lost = T("not remembered", 26, RED).move_to([-3.4, -0.6, 0])
        self.at("could not remember")
        self.play(FadeIn(cl), FadeIn(ct), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), run_time=1.0)
        self.at("an hour earlier")
        xs = VGroup(*[cross(RED, 0.2, 6).move_to(d) for d in dots])
        self.play(*[d.animate.set_opacity(0.25) for d in dots], FadeIn(xs), FadeIn(lost), run_time=0.8)

        # right card: mirror drawing across three days
        cr = RoundedRectangle(corner_radius=0.2, width=5.8, height=4.3, stroke_color=PURPLE, stroke_width=3,
                              fill_color=PURPLE, fill_opacity=0.06).move_to([3.4, 0.3, 0])
        rt = T("Mirror drawing", 28, PURPLE, weight=BOLD).move_to([3.4, 1.85, 0])
        star = Star(n=5, outer_radius=0.8, inner_radius=0.34, color=PURPLE, stroke_width=4).move_to([1.7, 0.45, 0])
        dot = Dot(star.get_start(), radius=0.1, color=TEXT)
        days = VGroup(*[T(f"Day {i}", 24, TEXT) for i in (1, 2, 3)]).arrange(RIGHT, buff=0.35).move_to([4.5, 0.95, 0])
        up = arr([3.55, 0.35, 0], [5.45, 0.75, 0], GREEN)
        better = T("better with practice", 24, GREEN).move_to([4.5, -0.1, 0])
        nomem = T("no memory of practising", 26, RED).move_to([3.4, -0.95, 0])
        self.at("new hand skill")
        self.play(FadeIn(cr), FadeIn(rt), Create(star), run_time=0.6)
        self.add(dot)
        self.play(MoveAlongPath(dot, star), FadeIn(days, lag_ratio=0.3), run_time=0.7)
        self.play(GrowArrow(up), FadeIn(better), FadeIn(nomem), run_time=0.5)

        q1 = chip("one ability?", GREY, 30)
        q2 = chip("several?", GREY, 30)
        qs = VGroup(q1, q2).arrange(RIGHT, buff=1.0).move_to([0, -2.75, 0])
        self.at("Is memory one ability")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.5)
        self.at("or several")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mem_box(x, title, col, sub, w=3.7, h=2.6, y=0.3):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=col, stroke_width=3,
                           fill_color=col, fill_opacity=0.1).move_to([x, y, 0])
    t = T(title, 28, col, weight=BOLD).move_to([x, y + 0.6, 0])
    fit(t, max_w=w - 0.3)
    s = T(sub, 24, TEXT).move_to([x, y - 0.25, 0])
    fit(s, max_w=w - 0.3)
    return VGroup(box, t, s)


class S02Dissociation(SpokenScene):
    def construct(self):
        head = T("dissociation: one ability fails, another survives", 30, TEXT).move_to([0, 3.0, 0])
        wm = mem_box(-4.7, "Working memory", TEAL, "digit span: normal")
        dm = mem_box(0.0, "Declarative memory", BLUE, "new ones: rare")
        sk = mem_box(4.7, "Skill learning", PURPLE, "mirror drawing: improves")
        note = T("the notepad", 24, TEAL).move_to([-4.7, -1.35, 0])
        b_wm = tick().move_to([-4.7, -0.55, 0])
        b_dm = cross().move_to([0, -0.55, 0])
        b_sk = tick().move_to([4.7, -0.55, 0])

        self.at("The test is a dissociation")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
        self.at("digit span was normal")
        self.play(FadeIn(wm), run_time=0.8)
        self.at("repeat back at once")
        self.play(Indicate(wm[2], color=TEAL, scale_factor=1.08), run_time=0.8)
        self.at("could hold")
        self.play(Indicate(wm[1], color=TEAL, scale_factor=1.1), run_time=0.8)
        self.at("working memory worked")
        self.play(FadeIn(b_wm, scale=0.6), FadeIn(note), run_time=0.6)
        self.at("nothing on that notepad")
        a = arr([-2.8, 0.3, 0], [-1.95, 0.3, 0], GREY)
        self.play(FadeIn(dm), GrowArrow(a), run_time=0.8)
        stop = Line([-2.45, 0.7, 0], [-2.45, -0.1, 0], color=RED, stroke_width=8)
        self.at("reached")
        self.play(Create(stop), FadeIn(b_dm, scale=0.6), run_time=0.6)
        self.at("skill learning survived")
        self.play(FadeIn(sk), run_time=0.7)
        self.play(FadeIn(b_sk, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Single(SpokenScene):
    def construct(self):
        grp = chip("one patient group", GREY, 30).move_to([-4.2, 0.9, 0])
        ta = chip("Task A", GREY, 30).move_to([0.2, 1.9, 0])
        tb = chip("Task B", GREY, 30).move_to([0.2, -0.1, 0])
        a1 = arr([grp.get_right() + RIGHT * 0.05, ], [ta.get_left() + LEFT * 0.05], GREY) if False else \
            arr(grp.get_right() + UP * 0.1, ta.get_left(), GREY)
        a2 = arr(grp.get_right() + DOWN * 0.1, tb.get_left(), GREY)
        ok = tick().move_to([1.9, 1.9, 0])
        bad = cross().move_to([1.9, -0.1, 0])
        okt = T("passes", 26, GREEN).next_to(ok, RIGHT, buff=0.25)
        badt = T("fails", 26, RED).next_to(bad, RIGHT, buff=0.25)
        # difficulty scale
        sc_line = Line([-3.0, -1.8, 0], [3.0, -1.8, 0], color=GREY, stroke_width=4)
        easy = T("easier", 24, GREY).next_to(sc_line.get_left(), DOWN, buff=0.25)
        hard = T("harder", 24, GREY).next_to(sc_line.get_right(), DOWN, buff=0.25)
        ma = Dot([-1.6, -1.8, 0], radius=0.14, color=GREY)
        mb = Dot([2.0, -1.8, 0], radius=0.14, color=RED)
        qa = T("A", 24, TEXT).next_to(ma, UP, buff=0.2)
        qb = T("B", 24, TEXT).next_to(mb, UP, buff=0.2)
        why = T("or is Task B just harder?", 28, RED).move_to([0.2, -0.95, 0])

        self.at("One task fails")
        self.play(FadeIn(grp), FadeIn(ta), FadeIn(tb), GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        self.play(FadeIn(ok, scale=0.6), FadeIn(okt), FadeIn(bad, scale=0.6), FadeIn(badt), run_time=0.7)
        self.at("single dissociation")
        self.play(Indicate(VGroup(grp, bad, badt), color=RED, scale_factor=1.05), run_time=0.8)
        self.at("only that the task is harder")
        self.play(Create(sc_line), FadeIn(easy), FadeIn(hard), FadeIn(ma), FadeIn(mb), FadeIn(qa), FadeIn(qb), FadeIn(why), run_time=1.0)
        self.at("worked problem")
        diag = VGroup(grp, ta, tb, a1, a2, ok, bad, okt, badt, sc_line, easy, hard, ma, mb, qa, qb, why)
        self.play(FadeOut(diag), run_time=0.5)
        tg = tag()
        pl, pr = build_panels()
        self.at("invented numbers")
        self.play(FadeIn(tg), run_time=0.5)
        self.at("There are two tasks")
        self.play(FadeIn(pl.base), FadeIn(pr.base), run_time=0.8)
        self.at("classification where")
        self.play(Indicate(pl.title, color=PURPLE, scale_factor=1.1), run_time=0.7)
        self.at("where chance is")
        self.play(Create(pl.chance), run_time=0.6)
        self.at("questionnaire about")
        self.play(Indicate(pr.title, color=BLUE, scale_factor=1.1), run_time=0.7)
        self.at("where chance is", nth=1)
        self.play(Create(pr.chance), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Scores(SpokenScene):
    def construct(self):
        tg = tag()
        pl, pr = build_panels()
        for p in (pl, pr):
            self.add(p.base, p.chance)
        self.add(tg)
        leg = legend()

        def grow(g):
            self.play(*[GrowFromEdge(p.bars[g], DOWN) for p in (pl, pr)],
                      *[FadeIn(p.labs[g], shift=UP * 0.1) for p in (pl, pr)], run_time=0.9)

        self.at("Control scores")
        self.play(FadeIn(leg[0]), FadeIn(leg[3]), run_time=0.4)
        grow("ctrl")
        self.at("Amnesic patients score")
        self.play(FadeIn(leg[1]), run_time=0.3)
        grow("am")
        self.at("patients score", nth=1)
        self.play(FadeIn(leg[2]), run_time=0.3)
        grow("pd")
        self.at("Look at")
        hl = VGroup(SurroundingRectangle(VGroup(pr.bars["ctrl"], pr.labs["ctrl"]), color=TEXT, buff=0.1, stroke_width=3),
                    SurroundingRectangle(VGroup(pr.bars["am"], pr.labs["am"]), color=TEXT, buff=0.1, stroke_width=3))
        self.play(Create(hl), run_time=0.7)
        self.at("It looks like")
        half = T("half?", 30, TEXT).move_to([pr.cx - 0.3, 1.85, 0])
        self.play(FadeIn(half), run_time=0.5)
        self.at("hide the guessing")
        g = Rectangle(width=0.8, height=25 * SC, stroke_width=0, fill_color=YELLOW, fill_opacity=0.65)
        g.move_to([pr.xs["am"], BASE + 25 * SC / 2, 0])
        g2 = Rectangle(width=0.8, height=25 * SC, stroke_width=0, fill_color=YELLOW, fill_opacity=0.65)
        g2.move_to([pr.xs["ctrl"], BASE + 25 * SC / 2, 0])
        self.play(FadeIn(g), FadeIn(g2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Chance(SpokenScene):
    def construct(self):
        tg = tag()
        self.add(tg)
        f0 = M("relative score =", 24, TEXT)
        f1 = M("(patient - chance)", 24, ORANGE)
        f2 = M("/", 24, TEXT)
        f3 = M("(control - chance)", 24, GREY)
        f1 = M("(patient − chance)", 24, TEXT)
        f2 = M("÷", 24, TEXT)
        f3 = M("(control − chance)", 24, TEXT)
        formula = VGroup(f0, f1, f2, f3).arrange(RIGHT, buff=0.22).move_to([0, 2.7, 0])
        fit(formula, max_w=12.2)

        # gains above chance (questionnaire), left
        cy = -1.1
        chance_line = DashedLine([-6.0, cy, 0], [-0.7, cy, 0], color=YELLOW, stroke_width=4, dash_length=0.14)
        chance_lab = T("chance, 25%", 24, YELLOW).move_to([-5.0, cy - 0.38, 0])
        gc = 55 * 0.045
        ga = 15 * 0.045
        bc = Rectangle(width=1.0, height=gc, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55)
        bc.move_to([-4.5, cy + gc / 2, 0])
        ba = Rectangle(width=1.0, height=ga, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.55)
        ba.move_to([-2.2, cy + ga / 2, 0])
        lc = M("80 − 25 = 55", 22, TEXT).move_to([-4.5, cy + gc + 0.3, 0])
        la = M("40 − 25 = 15", 22, TEXT).move_to([-2.2, cy + ga + 0.3, 0])
        qlab = T("Questionnaire, above chance", 24, BLUE).move_to([-3.3, 2.2, 0])
        quarter = T("about a quarter, not a half", 24, TEXT).move_to([-3.3, -2.3, 0])

        # table, right
        cx1, cx2 = 3.0, 5.2
        h1 = T("Classification", 22, PURPLE).move_to([cx1, 1.55, 0])
        h2 = T("Questionnaire", 22, BLUE).move_to([cx2, 1.55, 0])
        r1 = T("Amnesic", 24, ORANGE).move_to([0.75, 0.6, 0])
        r2 = T("Parkinson's", 24, GOLD).move_to([0.75, -0.6, 0])
        cells = {("am", 0): ("18/20 = 90%", cx1, 0.6), ("am", 1): ("15/55 = 27%", cx2, 0.6),
                 ("pd", 0): ("2/20 = 10%", cx1, -0.6), ("pd", 1): ("53/55 = 96%", cx2, -0.6)}
        cm = {k: M(v[0], 22, TEXT).move_to([v[1], v[2], 0]) for k, v in cells.items()}

        self.at("subtract chance first")
        self.play(FadeIn(formula, shift=DOWN * 0.1), Create(chance_line), FadeIn(chance_lab), run_time=0.9)
        self.play(Indicate(f1, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("Then divide")
        self.play(Indicate(f3, color=YELLOW, scale_factor=1.08), FadeIn(qlab), GrowFromEdge(bc, DOWN), FadeIn(lc), run_time=1.0)
        self.at("The amnesic questionnaire")
        self.play(GrowFromEdge(ba, DOWN), FadeIn(la), FadeIn(h1), FadeIn(h2), FadeIn(r1), FadeIn(r2), run_time=0.9)
        self.play(FadeIn(cm[("am", 1)], shift=UP * 0.1), run_time=0.6)
        self.at("about a quarter")
        self.play(FadeIn(quarter), Indicate(cm[("am", 1)], color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.at("guessing")
        self.play(Indicate(chance_line, color=YELLOW, scale_factor=1.0), Indicate(chance_lab, color=YELLOW), run_time=0.8)
        self.at("Amnesic classification")
        self.play(FadeIn(cm[("am", 0)], shift=UP * 0.1), run_time=0.6)
        self.at("patients get")
        self.play(FadeIn(cm[("pd", 0)], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(cm[("pd", 1)], shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Double(SpokenScene):
    def construct(self):
        tg = tag()
        self.add(tg)
        ax_x = -5.5
        x1, x2 = -4.4, -2.0
        axis = VGroup(Line([ax_x, BASE, 0], [ax_x, BASE + 100 * SC, 0], color=GREY, stroke_width=3),
                      Line([ax_x, BASE, 0], [-0.9, BASE, 0], color=GREY, stroke_width=3))
        for v in (0, 50, 100):
            axis.add(M(str(v), 22, GREY).move_to([ax_x - 0.33, BASE + v * SC, 0]))
        ytitle = T("% of controls' gain above chance", 22, GREY).move_to([-3.1, 2.55, 0])
        c1 = T("Classification", 24, PURPLE).move_to([x1, BASE - 0.4, 0])
        c2 = T("Questionnaire", 24, BLUE).move_to([x2 + 0.1, BASE - 0.4, 0])
        chart = VGroup(axis, ytitle, c1, c2)

        def pt(x, v, col):
            return Dot([x, BASE + v * SC, 0], radius=0.15, color=col)

        am1, am2 = pt(x1, 90, ORANGE), pt(x2, 27, ORANGE)
        pd1, pd2 = pt(x1, 10, GOLD), pt(x2, 96, GOLD)
        lam = Line(am1.get_center(), am2.get_center(), color=ORANGE, stroke_width=5)
        lpd = Line(pd1.get_center(), pd2.get_center(), color=GOLD, stroke_width=5)
        v_am1 = M("90%", 22, ORANGE).move_to(am1.get_center() + LEFT * 0.62)
        v_pd1 = M("10%", 22, GOLD).move_to(pd1.get_center() + LEFT * 0.62)
        v_am2 = M("27%", 22, ORANGE).move_to(am2.get_center() + DOWN * 0.38)
        v_pd2 = M("96%", 22, GOLD).move_to(pd2.get_center() + UP * 0.38)
        n_am = T("Amnesic", 24, ORANGE).move_to(am2.get_center() + RIGHT * 1.2)
        n_pd = T("Parkinson's", 24, GOLD).move_to(pd2.get_center() + RIGHT * 1.35)
        fail_am = cross(RED, 0.16, 5).move_to(am2.get_center() + RIGHT * 0.0 + DOWN * 0.0)
        fail_pd = cross(RED, 0.16, 5).move_to(pd1.get_center())

        self.at("Now compare")
        self.play(FadeIn(chart), run_time=0.8)
        self.at("Each group fails")
        self.play(FadeIn(am1), FadeIn(pd1), run_time=0.5)
        self.play(Create(lam), Create(lpd), FadeIn(am2), FadeIn(pd2), run_time=1.0)
        self.play(FadeIn(v_am1), FadeIn(v_pd1), FadeIn(v_am2), FadeIn(v_pd2), FadeIn(n_am), FadeIn(n_pd), run_time=0.7)
        self.play(FadeIn(fail_am, scale=0.5), FadeIn(fail_pd, scale=0.5), run_time=0.5)
        self.at("double dissociation")
        dd = chip("double dissociation", TEXT, 30).move_to([3.7, 2.7, 0])
        self.play(FadeIn(dd, shift=DOWN * 0.1), Indicate(VGroup(lam, lpd), scale_factor=1.03), run_time=0.8)

        # difficulty scales: no single order fits
        def scale_row(y, name, ncol, left_col, right_col):
            ln = Line([1.5, y, 0], [5.9, y, 0], color=GREY, stroke_width=4)
            lab = T(name, 24, ncol).move_to([3.7, y + 0.5, 0])
            l_lab = T("easier", 22, GREY).move_to([2.0, y - 0.4, 0])
            r_lab = T("harder", 22, GREY).move_to([5.4, y - 0.4, 0])
            dl = Dot([2.0, y, 0], radius=0.17, color=left_col)
            dr = Dot([5.4, y, 0], radius=0.17, color=right_col)
            return VGroup(ln, lab, l_lab, r_lab, dl, dr)

        r1 = scale_row(1.1, "Amnesic patients", ORANGE, PURPLE, BLUE)
        r2 = scale_row(-0.7, "Parkinson's patients", GOLD, BLUE, PURPLE)
        nofit = T("no one order fits both", 26, RED).move_to([3.7, -1.75, 0])
        self.at("No single difficulty scale")
        self.play(FadeIn(r1), run_time=0.7)
        self.at("hard for one group")
        self.play(FadeIn(r2), run_time=0.7)
        self.play(FadeIn(nofit), run_time=0.5)

        self.at("two separable learning processes")
        self.play(FadeOut(VGroup(r1, r2, nofit)), run_time=0.5)
        p1 = chip("classification", PURPLE, 22).move_to([2.2, 1.6, 0])
        p2 = chip("questionnaire", BLUE, 22).move_to([5.0, 1.6, 0])
        sep = DashedLine([3.62, 2.1, 0], [3.62, 1.1, 0], color=GREY, stroke_width=3)
        cap = T("evidence for separate processes", 24, TEXT).move_to([3.7, 0.7, 0])
        self.play(FadeIn(p1), FadeIn(p2), Create(sep), FadeIn(cap), run_time=0.9)

        self.at("pin each")
        target = chip("one structure?", GREY, 24).move_to([3.7, -0.9, 0])
        e1 = arr([2.4, 1.2, 0], [3.2, -0.5, 0], GREY, 4)
        e2 = arr([4.9, 1.2, 0], [4.2, -0.5, 0], GREY, 4)
        x1m, x2m = cross(RED, 0.16, 5).move_to([2.8, 0.35, 0]), cross(RED, 0.16, 5).move_to([4.55, 0.35, 0])
        self.play(FadeOut(cap), FadeIn(target), GrowArrow(e1), GrowArrow(e2), run_time=0.8)
        self.play(FadeIn(x1m, scale=0.5), FadeIn(x2m, scale=0.5), run_time=0.4)
        self.at("more than the striatum")
        pk = T("Parkinson's disease damages", 22, GOLD).move_to([3.7, -1.75, 0])
        pk2 = T("more than the striatum", 22, GOLD).move_to([3.7, -2.15, 0])
        self.play(FadeIn(pk), FadeIn(pk2), run_time=0.6)

        self.at("A lesion shows")
        self.play(FadeOut(VGroup(p1, p2, sep, target, e1, e2, x1m, x2m, pk, pk2)), run_time=0.5)
        les = chip("lesion: structure needed", GREEN, 30).move_to([3.7, 1.0, 0])
        sto = chip("memory lives there", GREY, 30).move_to([3.7, -0.7, 0])
        self.play(FadeIn(les, shift=UP * 0.1), run_time=0.6)
        self.at("not that the memory")
        sl = Line(sto.get_left() + RIGHT * 0.1, sto.get_right() + LEFT * 0.1, color=RED, stroke_width=7)
        self.play(FadeIn(sto), run_time=0.5)
        self.play(FadeIn(sl, scale=0.5), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "A lesion shows a structure is needed, not that memory lives there."
