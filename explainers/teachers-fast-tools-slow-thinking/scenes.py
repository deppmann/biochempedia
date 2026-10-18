"""Fast Tools, Slow Thinking: a talk for middle and high school biology teachers (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the tool / things that get built
  GREEN  = done, finished, checked by a person
  RED    = wrong, lazy thinking, a miss
  ORANGE = imprecise claims
  YELLOW = the student's own thinking / commitments
  TEAL   = the room, the app, the link
  GREY   = structure, labels, not-yet
  GOLD   = the one rule on screen per scene
Every number on screen and in the narration comes from the talk brief.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def person(color=GREY, scale=1.0):
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    body = RoundedRectangle(corner_radius=0.3, width=1.2, height=0.8, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.25).next_to(head, DOWN, buff=0.12)
    return VGroup(head, body).scale(scale)


def tick(color=GREEN, size=0.22):
    return VGroup(Line([-size, 0, 0], [-size * 0.35, -size * 0.7, 0], color=color, stroke_width=6),
                  Line([-size * 0.35, -size * 0.7, 0], [size, size * 0.8, 0], color=color, stroke_width=6))


def cross(color=RED, size=0.22):
    return VGroup(Line(UL * size, DR * size, color=color, stroke_width=6), Line(UR * size, DL * size, color=color, stroke_width=6))


class S00Title(TitleCard):
    LESSON = "Teaching life science in the age of AI"
    TITLE = "Fast Tools, Slow Thinking"


# ---------------------------------------------------------------------------------------------
class S01Hook(SpokenScene):
    def construct(self):
        stu = person(BLUE, 1.5).move_to([-5.5, -0.9, 0])
        bubble = RoundedRectangle(corner_radius=0.35, width=4.6, height=2.4, stroke_color=BLUE, stroke_width=4,
                                  fill_color=BLUE, fill_opacity=0.10).move_to([-2.2, 1.0, 0])
        lines = VGroup(*[RoundedRectangle(corner_radius=0.08, width=w, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.75)
                         for w in (3.6, 3.0, 3.4)]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(bubble)
        self.at("talk a lot")
        self.play(FadeIn(stu, shift=UP * 0.2), FadeIn(bubble, scale=0.9), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(l, LEFT) for l in lines], lag_ratio=0.3), run_time=1.0)
        self.at("sound like they know")
        known = T("sounds like they know", 26, BLUE).next_to(bubble, DOWN, buff=0.25)
        self.play(FadeIn(known, shift=UP * 0.1), run_time=0.5)

        card = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.6, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.08).move_to([3.7, 0.0, 0])
        head = T("the reading", 28, GREY).move_to(card.get_top() + DOWN * 0.5)
        rows = VGroup()
        for i in range(3):
            box = Square(0.36, stroke_color=GREY, stroke_width=3)
            bar = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.5)
            rows.add(VGroup(box, bar).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(card.get_center() + DOWN * 0.3)
        self.at("never did the reading")
        self.play(FadeIn(card), FadeIn(head), FadeIn(rows), run_time=0.7)
        self.at("We have all had one")
        self.play(Indicate(stu, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("could not see it")
        veil = Rectangle(width=4.6, height=3.6, stroke_width=0, fill_color="#0f1117", fill_opacity=0.75).move_to(card)
        q = T("?", 110, YELLOW, weight=BOLD).move_to(card)
        note = T("hidden from the teacher", 26, YELLOW).next_to(card, DOWN, buff=0.3)
        self.play(FadeIn(veil), FadeIn(q, scale=0.6), FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pace(SpokenScene):
    def construct(self):
        X0 = -6.2
        k = 6.4 / 119.0   # 119 days (17 weeks) = 6.4 units; both bars share this scale
        l1 = T("first 30 lessons", 28, BLUE).move_to([X0, 2.75, 0], aligned_edge=LEFT)
        b1 = Rectangle(width=119 * k, height=0.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
        b1.move_to([X0 + 119 * k / 2, 2.15, 0])
        t1 = T("about 17 weeks", 28, TEXT).next_to(b1, RIGHT, buff=0.3)
        l2 = T("next 173 lessons", 28, GREEN).move_to([X0, 1.2, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=8 * k, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.45)
        b2.move_to([X0 + 8 * k / 2, 0.6, 0])
        t2 = T("about 8 days", 28, TEXT).next_to(b2, RIGHT, buff=0.3)
        start = T("starting in June", 24, GREY).move_to([4.6, 3.0, 0])
        self.at("starting in June")
        self.play(FadeIn(start), run_time=0.4)
        self.at("first 30 lessons")
        self.play(FadeIn(l1), GrowFromEdge(b1, LEFT), run_time=1.2)
        self.at("17 weeks")
        self.play(FadeIn(t1, shift=LEFT * 0.1), run_time=0.4)
        self.at("next 173")
        self.play(FadeIn(l2), GrowFromEdge(b2, LEFT), run_time=0.6)
        self.at("eight days")
        self.play(FadeIn(t2, shift=LEFT * 0.1), Indicate(b2, color=GREEN, scale_factor=1.3), run_time=0.7)

        big = M("203", 80, GOLD, weight=BOLD)
        word = T("lessons", 40, TEXT)
        total = VGroup(big, word).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([0, -0.7, 0])
        self.at("That is 203")
        self.play(FadeIn(total, scale=1.2), run_time=0.6)
        names = ["Biochemistry", "Cell Signaling", "Developmental Neuroscience", "Genetics", "Cell Biology", "Ecology & Evolution"]
        chips = VGroup(*[chip(n, TEAL, size=22, pad=0.14) for n in names])
        row1 = VGroup(*chips[:3]).arrange(RIGHT, buff=0.25)
        row2 = VGroup(*chips[3:]).arrange(RIGHT, buff=0.25)
        grid = VGroup(row1, row2).arrange(DOWN, buff=0.25).move_to([0, -2.35, 0])
        self.at("six courses")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.15), run_time=1.2)
        free = chip("free for any student", GREEN, size=26).move_to([4.2, -0.7, 0])
        self.at("free for any student")
        self.play(FadeIn(free, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Ladder(SpokenScene):
    def ladder(self, x, low, high, color_lo, color_hi):
        lo = chip(low, color_lo, size=26).move_to([x, -1.6, 0])
        hi = chip(high, color_hi, size=26).move_to([x, 1.4, 0])
        ar = Arrow(lo.get_top(), hi.get_bottom(), buff=0.15, color=GOLD, stroke_width=6, tip_length=0.25)
        return lo, hi, ar

    def construct(self):
        rule = T("When you finish a goal, move up one level", 34, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        fit(rule, max_w=12)
        self.at("When you finish a goal")
        self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.7)
        lo1, hi1, ar1 = self.ladder(-3.4, "one course", "a whole pre-med\ncurriculum", GREY, BLUE)
        self.at("One course became")
        self.play(FadeIn(lo1), run_time=0.4)
        self.play(GrowArrow(ar1), run_time=0.6)
        self.play(FadeIn(hi1, shift=UP * 0.2), run_time=0.5)

        lo2 = chip("a standard question", GREY, size=26).move_to([3.4, -1.6, 0])
        hi2 = chip("a question that points\nto its lesson", TEAL, size=26).move_to([3.4, 1.4, 0])
        ar2 = Arrow(lo2.get_top(), hi2.get_bottom(), buff=0.15, color=GOLD, stroke_width=6, tip_length=0.25)
        self.at("Standard questions")
        self.play(FadeIn(lo2), run_time=0.4)
        self.play(GrowArrow(ar2), run_time=0.6)
        self.play(FadeIn(hi2, shift=UP * 0.2), run_time=0.5)
        lesson = chip("the exact lesson", GREEN, size=24).move_to([3.4, -3.0, 0])
        back = CurvedArrow(hi2.get_right() + RIGHT * 0.05, lesson.get_right() + RIGHT * 0.05, angle=-TAU / 4, color=GREEN, stroke_width=5, tip_length=0.22)
        self.at("back to the exact lesson")
        self.play(FadeIn(lesson, shift=UP * 0.1), Create(back), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Catch(SpokenScene):
    def construct(self):
        W = 11.0
        X0 = -W / 2
        total = Rectangle(width=W, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([0, 1.2, 0])
        wrong_w, imp_w = W * 49 / 3468, W * 453 / 3468
        wrong = Rectangle(width=wrong_w, height=0.9, stroke_width=0, fill_color=RED, fill_opacity=0.95)
        wrong.move_to([X0 + wrong_w / 2, 1.2, 0])
        imp = Rectangle(width=imp_w, height=0.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9)
        imp.move_to([X0 + wrong_w + imp_w / 2, 1.2, 0])
        lab = T("nearly 3,500 claims in one course", 30, TEXT).move_to([0, 2.45, 0])
        ck = chip("AI fact-checker", BLUE, size=26).move_to([-4.6, 3.2, 0])
        self.at("In one course")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.at("AI fact checker")
        self.play(FadeIn(ck, shift=RIGHT * 0.2), run_time=0.4)
        self.at("went through")
        self.play(GrowFromEdge(total, LEFT), run_time=1.4)

        n1 = M("49", 44, RED, weight=BOLD)
        t1 = T("flat wrong", 28, RED)
        g1 = VGroup(n1, t1).arrange(DOWN, buff=0.1).move_to([-4.3, -0.9, 0])
        a1 = Line(wrong.get_bottom(), g1.get_top() + UP * 0.05, color=RED, stroke_width=4)
        self.at("49")
        self.play(FadeIn(wrong), Create(a1), FadeIn(g1, shift=UP * 0.1), run_time=0.7)
        n2 = M("453", 44, ORANGE, weight=BOLD)
        t2 = T("imprecise", 28, ORANGE)
        g2 = VGroup(n2, t2).arrange(DOWN, buff=0.1).move_to([-1.9, -0.9, 0])
        a2 = Line(imp.get_bottom(), g2.get_top() + UP * 0.05, color=ORANGE, stroke_width=4)
        self.at("453")
        self.play(FadeIn(imp), Create(a2), FadeIn(g2, shift=UP * 0.1), run_time=0.7)

        mk = chip("making lessons: cheap", BLUE, size=28).move_to([-3.0, -3.0, 0])
        jb = chip("checking them: the job", GREEN, size=28).move_to([3.3, -3.0, 0])
        arr = Arrow(mk.get_right(), jb.get_left(), buff=0.15, color=GREY, stroke_width=5, tip_length=0.22)
        self.at("Making lessons got cheap")
        self.play(FadeIn(mk, shift=UP * 0.1), run_time=0.5)
        self.at("Checking them became")
        self.play(GrowArrow(arr), FadeIn(jb, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Prework(SpokenScene):
    def construct(self):
        head = T("Pre-work as homework", 34, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("classroom side")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        steps = [("1  predict", BLUE), ("2  commit", YELLOW), ("3  reveal", GREEN)]
        cs = VGroup(*[chip(t, c, size=34, pad=0.3) for t, c in steps]).arrange(RIGHT, buff=1.2).move_to([0, 1.2, 0])
        ars = [Arrow(cs[i].get_right(), cs[i + 1].get_left(), buff=0.12, color=GREY, stroke_width=5, tip_length=0.22) for i in range(2)]
        self.at("They predict")
        self.play(FadeIn(cs[0], shift=UP * 0.15), run_time=0.5)
        self.at("commit to")
        self.play(GrowArrow(ars[0]), FadeIn(cs[1], shift=UP * 0.15), run_time=0.6)
        self.at("see the result")
        self.play(GrowArrow(ars[1]), FadeIn(cs[2], shift=UP * 0.15), run_time=0.6)

        g1 = chip("graded: the reasoning", TEAL, size=30).move_to([-3.4, -0.9, 0])
        k1 = tick().next_to(g1, LEFT, buff=0.25)
        g2 = chip("not graded: right or wrong", GREY, size=30).move_to([3.4, -0.9, 0])
        k2 = cross(GREY).next_to(g2, LEFT, buff=0.25)
        self.at("grade the reasoning")
        self.play(FadeIn(g1), Create(k1), run_time=0.6)
        self.at("not the correctness")
        self.play(FadeIn(g2), Create(k2), run_time=0.6)
        q = T("A wrong answer argued well costs nothing.", 34, GOLD, font=TITLE_FONT).move_to([0, -2.7, 0])
        fit(q, max_w=12)
        self.at("A wrong answer argued well")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Bar(SpokenScene):
    def construct(self):
        N, S, GAP = 12, 0.78, 0.2
        row_w = N * S + (N - 1) * GAP
        x0 = -row_w / 2 + S / 2

        def square(i, state):
            sq = Square(S, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06)
            sq.move_to([x0 + i * (S + GAP), 0.5, 0])
            if state == "done":
                sq.set_stroke(GREEN).set_fill(GREEN, 0.85)
            elif state == "part":
                sq.set_stroke(YELLOW).set_fill(YELLOW, 0.4)
            return sq

        sqs = VGroup(*[square(i, "none") for i in range(N)])
        title = T("pre-work finished, class of 12", 32, TEXT).move_to([0, 3.0, 0])
        self.at("a class of 12")
        self.play(FadeIn(title), FadeIn(sqs), run_time=0.7)
        when = T("Thursday morning", 36, GOLD, font=TITLE_FONT).move_to([0, 1.9, 0])
        cnt = M("2 of 12", 56, GREEN, weight=BOLD).move_to([0, -1.4, 0])
        self.at("Thursday morning")
        self.play(FadeIn(when, shift=DOWN * 0.1), run_time=0.4)
        self.at("two students had finished")
        self.play(*[sqs[i].animate.set_stroke(GREEN).set_fill(GREEN, 0.85) for i in range(2)], FadeIn(cnt, scale=0.9), run_time=0.7)
        leg1 = VGroup(Square(0.3, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.85), T("finished", 24, GREEN)).arrange(RIGHT, buff=0.2)
        leg3 = VGroup(Square(0.3, stroke_color=GREY, stroke_width=3), T("not finished yet", 24, GREY)).arrange(RIGHT, buff=0.2)
        legend = VGroup(leg1, leg3).arrange(RIGHT, buff=0.8).move_to([0, -2.7, 0])
        self.play(FadeIn(legend), run_time=0.4)

        when2 = T("Friday, 8:40 am", 36, GOLD, font=TITLE_FONT).move_to([0, 1.9, 0])
        self.at("By 8 40")
        self.play(ReplacementTransform(when, when2), run_time=0.5)
        cnt2 = M("9 of 12", 56, GREEN, weight=BOLD).move_to([0, -1.4, 0])
        self.at("nine had finished")
        self.play(*[sqs[i].animate.set_stroke(GREEN).set_fill(GREEN, 0.85) for i in range(2, 9)], ReplacementTransform(cnt, cnt2), run_time=1.0)
        leg2 = VGroup(Square(0.3, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.4), T("part way", 24, YELLOW)).arrange(RIGHT, buff=0.2)
        legend2 = VGroup(leg1.copy(), leg2, leg3.copy()).arrange(RIGHT, buff=0.8).move_to([0, -2.7, 0])
        self.at("three more")
        self.play(*[sqs[i].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.4) for i in range(9, 12)],
                  ReplacementTransform(legend, legend2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Room(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=7.6, height=5.6, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.07).move_to([-2.9, -0.1, 0])
        hdr = T("THE ROOM", 22, TEAL, weight=BOLD).move_to(card.get_top() + DOWN * 0.45)
        anon = T("anonymous answers from the pre-work", 22, GREY).next_to(hdr, DOWN, buff=0.15)
        qq = T("Does a dynein block prove\nTrkA is the cargo?", 34, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to(card.get_center() + UP * 0.5)
        self.at("room's own words")
        self.play(FadeIn(card), FadeIn(hdr), FadeIn(anon), run_time=0.6)
        self.at("Does a")
        self.play(FadeIn(qq, shift=UP * 0.1), run_time=0.8)

        U = 0.62
        by = card.get_center()[1] - 1.5
        x0 = -5.6
        lab_y = T("yes", 28, GREEN).move_to([x0 - 0.0, by + 0.35, 0], aligned_edge=LEFT)
        yes = Rectangle(width=2 * U, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.6)
        yes.move_to([x0 + 0.9 + U, by + 0.35, 0])
        ny = M("2", 34, GREEN, weight=BOLD).next_to(yes, RIGHT, buff=0.2)
        lab_n = T("no", 28, RED).move_to([x0, by - 0.4, 0], aligned_edge=LEFT)
        no = Rectangle(width=6 * U, height=0.5, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.6)
        no.move_to([x0 + 0.9 + 3 * U, by - 0.4, 0])
        nn = M("6", 34, RED, weight=BOLD).next_to(no, RIGHT, buff=0.2)
        self.at("Two say yes")
        self.play(FadeIn(lab_y), GrowFromEdge(yes, LEFT), FadeIn(ny), run_time=0.7)
        self.at("Six say no")
        self.play(FadeIn(lab_n), GrowFromEdge(no, LEFT), FadeIn(nn), run_time=0.8)
        self.at("everyone learns")

        note = RoundedRectangle(corner_radius=0.2, width=4.8, height=3.4, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.08).move_to([4.2, 0.2, 0])
        nh = T("a short note, before class", 24, BLUE, weight=BOLD).move_to(note.get_top() + DOWN * 0.45)
        items = VGroup(*[T(s, 24, TEXT) for s in ("where you are", "a point from your answers", "what to focus on")]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        items.move_to(note.get_center() + DOWN * 0.3)
        self.at("short note")
        self.play(FadeIn(note, shift=LEFT * 0.2), FadeIn(nh), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in items], lag_ratio=0.4), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Risk(SpokenScene):
    def construct(self):
        risk = T("The risk: lazy thinking", 40, RED, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("real risk")
        self.play(FadeIn(risk, shift=DOWN * 0.1), run_time=0.6)
        slow = T("Slow thinking is the point", 40, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("Slow thinking is")
        self.play(ReplacementTransform(risk, slow), run_time=0.7)

        tool = chip("the tool", BLUE, size=28).move_to([-3.6, 1.7, 0])
        mind = chip("the student's thinking", YELLOW, size=28).move_to([3.0, 1.7, 0])
        ar = Arrow(tool.get_right(), mind.get_left(), buff=0.15, color=GREY, stroke_width=5, tip_length=0.22)
        x = cross(RED, 0.3).move_to(ar.get_center())
        self.at("design the tool")
        self.play(FadeIn(tool), FadeIn(mind), run_time=0.5)
        self.at("cannot think")
        self.play(GrowArrow(ar), FadeIn(x, scale=1.4), run_time=0.6)

        g = [chip("reasoning is graded", TEAL, size=26), chip("paste is guarded", TEAL, size=26),
             chip("stuck note first: 25+ words", TEAL, size=26)]
        guards = VGroup(*g).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.6, -0.7, 0])
        self.at("Reasoning is graded")
        self.play(FadeIn(g[0], shift=RIGHT * 0.2), run_time=0.4)
        self.at("Paste is guarded")
        self.play(FadeIn(g[1], shift=RIGHT * 0.2), run_time=0.4)
        self.at("stuck note")
        self.play(FadeIn(g[2], shift=RIGHT * 0.2), run_time=0.5)

        d = chip("AI draft", BLUE, size=26).move_to([3.7, -0.1, 0])
        c = chip("a person checks", GREEN, size=26).move_to([3.7, -1.3, 0])
        s = chip("sent", GREY, size=26).move_to([3.7, -2.5, 0])
        a1 = Arrow(d.get_bottom(), c.get_top(), buff=0.08, color=GREY, stroke_width=4, tip_length=0.18)
        a2 = Arrow(c.get_bottom(), s.get_top(), buff=0.08, color=GREY, stroke_width=4, tip_length=0.18)
        self.at("a human checks")
        self.play(FadeIn(d, shift=DOWN * 0.1), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(c), run_time=0.5)
        self.play(GrowArrow(a2), FadeIn(s), run_time=0.5)

        self.at("Once the AI said")
        self.play(FadeOut(VGroup(guards, tool, mind, ar, x)), run_time=0.5)
        w = chip("AI summary: no activity", RED, size=28).move_to([-3.4, 0.7, 0])
        r = chip("raw answers: finished", GREEN, size=28).move_to([-3.4, -0.8, 0])
        ne = T("is not", 24, GREY).move_to([-3.4, -0.05, 0])
        self.play(FadeIn(w, shift=RIGHT * 0.2), run_time=0.5)
        self.at("That student had finished")
        self.play(FadeIn(ne), FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Close(SpokenScene):
    def construct(self):
        res = T("Resources for teachers", 44, TEXT, font=TITLE_FONT).move_to([0, 1.3, 0])
        url = T("biochemistrypedia.com/teachers", 40, TEAL, weight=BOLD).move_to([0, 0.1, 0])
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4).move_to([0, -0.9, 0])
        self.at("resources for teachers")
        self.play(FadeIn(res, shift=UP * 0.15), run_time=0.6)
        self.at("biochemistrypedia")
        self.play(FadeIn(url, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.7)
        f1 = T("Fast tools.", 38, BLUE, font=TITLE_FONT)
        f2 = T("Slow thinking.", 38, GOLD, font=TITLE_FONT)
        tag = VGroup(f1, f2).arrange(RIGHT, buff=0.35).move_to([0, -2.0, 0])
        self.at("Fast tools")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.4)
        self.at("slow thinking")
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.5)
        self.finish()
