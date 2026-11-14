"""Why reciprocal crosses split: chromosome routes on one carried family board.

COLOR MAP
  TEAL = maternal X chromosomes and their routes
  GOLD = paternal X chromosomes and their routes
  RED  = red-eye allele and red eyes
  TEXT = white-eye allele and white eyes
  GREY = Y chromosome, neutral slots, and inactive marks
"""
from bp_parts import *


MATERNAL = TEAL
PATERNAL = GOLD
WHITE_EYE = TEXT
RED_EYE = RED
Y_COLOR = GREY


def eye_badge(color, radius=0.23):
    """A schematic eye badge, not an anatomical drawing."""
    outer = Circle(radius=radius, stroke_color=TEXT, stroke_width=2.5,
                   fill_color=color, fill_opacity=1)
    pupil = Dot(radius=radius * 0.24, color=BG if color == TEXT else TEXT)
    return VGroup(outer, pupil)


def allele_badge(color, letter, size=38):
    lab = T(letter, size=size, color=BG if color in (TEXT, RED) else TEXT, weight=BOLD)
    disk = Circle(radius=0.42, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=1)
    return VGroup(disk, lab.move_to(disk))


def chromosome_block(kind, color, allele=None, height=1.05):
    """A labelled chromosome block; allele badges sit beside, never on, its border."""
    width = 0.72 if kind == "X" else 0.62
    body = RoundedRectangle(corner_radius=0.13, width=width, height=height,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.22)
    # These blocks are scaled to 60% inside the family cards; start large enough
    # that the final glyphs remain above the film's 22 pt floor.
    label = T(kind, size=38, color=color, weight=BOLD).move_to(body)
    g = VGroup(body, label)
    if allele:
        badge = allele_badge(allele, "R" if allele == RED else "w", 38)
        badge.next_to(body, RIGHT, buff=0.13)
        g.add(badge)
        g.badge = badge
    return g


def person_card(title, eye, chromosomes=(), width=2.55, height=2.05):
    """The one reusable parent/offspring cartoon used throughout the film."""
    frame = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                             stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.18)
    ttl = fit_text(title, max_w=width - 0.35, size=32, color=TEXT,
                   min_size=30, max_lines=1).move_to(frame.get_top() + DOWN * 0.32)
    eye_mob = eye_badge(eye, 0.26).move_to(frame.get_center() + UP * 0.02)
    chroms = VGroup(*chromosomes)
    if len(chroms):
        chroms.arrange(RIGHT, buff=0.38).scale(0.6)
        chroms.move_to(frame.get_bottom() + UP * 0.42)
    g = VGroup(frame, ttl, eye_mob, chroms)
    g.frame, g.title, g.eye, g.chroms = frame, ttl, eye_mob, chroms
    return g


def family_board(cross="B", outcomes="neutral", routes=False):
    """The carried world: every family-board scene uses these exact landmarks."""
    if cross == "A":
        m_eye, f_eye = RED_EYE, WHITE_EYE
        m_allele, f_allele = RED_EYE, WHITE_EYE
    else:
        m_eye, f_eye = WHITE_EYE, RED_EYE
        m_allele, f_allele = WHITE_EYE, RED_EYE

    mother = person_card(
        "mother", m_eye,
        [chromosome_block("X", MATERNAL, m_allele), chromosome_block("X", MATERNAL, m_allele)],
    ).move_to([-3.7, 1.8, 0])
    father = person_card(
        "father", f_eye,
        [chromosome_block("X", PATERNAL, f_allele), chromosome_block("Y", Y_COLOR)],
    ).move_to([3.7, 1.8, 0])

    if outcomes == "A":
        d_eye, s_eye = RED_EYE, RED_EYE
        d_ch = [chromosome_block("X", MATERNAL, RED_EYE), chromosome_block("X", PATERNAL, WHITE_EYE)]
        s_ch = [chromosome_block("X", MATERNAL, RED_EYE), chromosome_block("Y", Y_COLOR)]
    elif outcomes == "B":
        d_eye, s_eye = RED_EYE, WHITE_EYE
        d_ch = [chromosome_block("X", MATERNAL, WHITE_EYE), chromosome_block("X", PATERNAL, RED_EYE)]
        s_ch = [chromosome_block("X", MATERNAL, WHITE_EYE), chromosome_block("Y", Y_COLOR)]
    else:
        d_eye = s_eye = GREY
        d_ch = [chromosome_block("X", MATERNAL), chromosome_block("X", PATERNAL)]
        s_ch = [chromosome_block("X", MATERNAL), chromosome_block("Y", Y_COLOR)]

    daughter = person_card("daughter", d_eye, d_ch).move_to([-3.0, -1.25, 0])
    son = person_card("son", s_eye, s_ch).move_to([3.0, -1.25, 0])

    # Broad tracks stop short of every card, leaving labels and borders clear.
    mx_d = CurvedArrow([-3.85, 0.72, 0], [-3.25, -0.13, 0], angle=0.12,
                       color=MATERNAL, stroke_width=8, tip_length=0.2)
    mx_s = CurvedArrow([-3.3, 0.72, 0], [2.68, -0.13, 0], angle=-0.18,
                       color=MATERNAL, stroke_width=8, tip_length=0.2)
    fx_d = CurvedArrow([3.28, 0.72, 0], [-2.65, -0.13, 0], angle=0.18,
                       color=PATERNAL, stroke_width=8, tip_length=0.2)
    fy_s = CurvedArrow([3.83, 0.72, 0], [3.25, -0.13, 0], angle=-0.12,
                       color=Y_COLOR, stroke_width=7, tip_length=0.2)
    tracks = VGroup(mx_d, mx_s, fx_d, fy_s)
    cards = VGroup(mother, father, daughter, son)
    board = VGroup(tracks, cards) if routes else VGroup(cards)
    board.mother, board.father = mother, father
    board.daughter, board.son = daughter, son
    board.tracks = tracks
    board.mx_d, board.mx_s, board.fx_d, board.fy_s = mx_d, mx_s, fx_d, fy_s
    return board


def parent_pair(cross="A", scale=0.82):
    """Compact reciprocal-parent picture for side-by-side comparisons."""
    if cross == "A":
        left = person_card("mother", RED_EYE, width=2.2, height=1.75)
        right = person_card("father", WHITE_EYE, width=2.2, height=1.75)
    else:
        left = person_card("mother", WHITE_EYE, width=2.2, height=1.75)
        right = person_card("father", RED_EYE, width=2.2, height=1.75)
    pair = VGroup(left, T("×", 38, GREY), right).arrange(RIGHT, buff=0.32)
    return pair.scale(scale)


def chromosome_pair_world():
    """Shared large chromosome layout for the location and hemizygosity scenes."""
    panels = TwoPanel("female", "male", colors=(MATERNAL, PATERNAL), top=3.0, bottom=-2.45)
    xx = VGroup(chromosome_block("X", MATERNAL, WHITE_EYE, 2.55),
                chromosome_block("X", MATERNAL, RED_EYE, 2.55)).arrange(RIGHT, buff=1.0)
    xy = VGroup(chromosome_block("X", PATERNAL, WHITE_EYE, 2.55),
                chromosome_block("Y", Y_COLOR, None, 2.0)).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
    panels.put(xx, "left")
    panels.put(xy, "right")
    return panels, xx, xy


def mini_result(cross):
    if cross == "A":
        d, s = RED_EYE, RED_EYE
    else:
        d, s = RED_EYE, WHITE_EYE
    daughter = VGroup(eye_badge(d, 0.3), T("daughters", 30, TEXT)).arrange(RIGHT, buff=0.25)
    son = VGroup(eye_badge(s, 0.3), T("sons", 30, TEXT)).arrange(RIGHT, buff=0.25)
    return VGroup(daughter, son).arrange(DOWN, buff=0.48, aligned_edge=LEFT)


class S00Title(TitleCard):
    LESSON = "Sex linkage and beyond"
    TITLE = "Why Reciprocal Crosses Split"

    def construct(self):
        ghost = family_board("B", "neutral", routes=True).scale(0.72).set_opacity(0.2)
        ghost.shift(DOWN * 0.2)
        title = fit_text(self.TITLE, max_w=11.4, size=52, font=TITLE_FONT,
                         color=TEXT).move_to(UP * 1.0)
        lesson = T(self.LESSON.upper(), 24, TEAL).next_to(title, UP, buff=0.3)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(ghost), run_time=0.55)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.15)
        self.wait(0.45)
        self.play(FadeOut(VGroup(ghost, lesson, title, rule)), run_time=0.55)
        self.finish()


class S01Hook(SpokenScene):
    def construct(self):
        panels = TwoPanel("Pair A", "Pair B", colors=(MATERNAL, PATERNAL), top=3.0, bottom=-2.35)
        pair_a, pair_b = parent_pair("A"), parent_pair("B")
        panels.put(pair_a, "left")
        panels.put(pair_b, "right")
        pair_a.shift(UP * 0.45)
        pair_b.shift(UP * 0.45)
        bob(pair_a, amp=0.055, speed=1.25)
        bob(pair_b, amp=0.055, speed=1.25, seed=2)
        qa = chip("sons?", GOLD, 31).next_to(pair_a, DOWN, buff=0.55)
        qb = chip("sons?", GOLD, 31).next_to(pair_b, DOWN, buff=0.55)
        pulse(qa[0], base=3.0, amp=1.2, speed=2.5)
        pulse(qb[0], base=3.0, amp=1.2, speed=2.5)
        self.play(FadeIn(panels), FadeIn(pair_a, shift=RIGHT * 0.2),
                  FadeIn(pair_b, shift=LEFT * 0.2), run_time=1.0)
        self.at("change every sun")
        self.play(FadeIn(qa), FadeIn(qb), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.at("Morgan's reciprocal")
        same = T("same alleles", 30, TEXT).move_to([0, -2.7, 0])
        self.play(FadeIn(same), Indicate(pair_a), Indicate(pair_b), run_time=1.2)
        self.at("Their offspring")
        a_out = mini_result("A").scale(0.78).move_to(qa)
        b_out = mini_result("B").scale(0.78).move_to(qb)
        self.play(FadeOut(qa), FadeOut(qb), FadeIn(a_out), FadeIn(b_out), run_time=1.0)
        self.at("The difference points")
        route = caption("The chromosome route changed — the inheritance law did not.", color=GOLD)
        self.play(swap(same, route), run_time=0.8)
        self.play(Indicate(b_out[1], color=GOLD), run_time=1.0)
        self.finish()


class S02Location(SpokenScene):
    def construct(self):
        panels, xx, xy = chromosome_pair_world()
        self.play(FadeIn(panels), run_time=0.6)
        self.at("inside the flies")
        self.play(FadeIn(xx[0], shift=UP * 0.2), FadeIn(xy[0], shift=UP * 0.2), run_time=0.8)
        self.at("A female has")
        self.play(FadeIn(xx[1], shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(xx, color=MATERNAL), run_time=0.9)
        self.at("A male has")
        self.play(FadeIn(xy[1], shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(xy, color=PATERNAL), run_time=0.7)
        self.at("The white gene")
        x_badges = VGroup(xx[0].badge, xy[0].badge)
        self.play(Indicate(x_badges, color=WHITE_EYE), run_time=0.7)
        no_slot = T("no white-gene slot", 28, GREY).next_to(xy[1], DOWN, buff=0.3)
        self.play(FadeIn(no_slot), run_time=0.7)
        self.at("Gene location")
        bob(xx[0], amp=0.05, speed=1.3)
        bob(xx[1], amp=0.05, speed=1.3, seed=1)
        bob(xy[0], amp=0.05, speed=1.3, seed=2)
        bob(xy[1], amp=0.05, speed=1.3, seed=3)
        rule = caption("Gene location decides the chromosome route.", color=GOLD)
        self.play(FadeIn(rule), run_time=0.7)
        self.play(Circumscribe(xy[0], color=GOLD), run_time=1.2)
        self.finish()


class S03Hemi(SpokenScene):
    def construct(self):
        panels, xx, xy = chromosome_pair_world()
        self.add(panels, xx, xy)
        pulse(panels.left_frame, base=2.5, amp=1.2, speed=1.35)
        pulse(panels.right_frame, base=2.5, amp=1.2, speed=1.35)
        ghost = RoundedRectangle(corner_radius=0.13, width=0.55, height=2.55,
                                 stroke_color=GREY, stroke_width=3).set_stroke(opacity=0.35)
        ghost.next_to(xy[0], LEFT, buff=0.7)
        hemi = chip("hemizygous: one allele present", GOLD, 29).move_to([3.25, -2.05, 0])
        self.play(xy.animate.scale(1.12), xx.animate.set_opacity(0.35), run_time=0.8)
        self.at("so he is")
        self.play(FadeIn(ghost), FadeIn(hemi), run_time=0.8)
        self.play(FadeOut(ghost), run_time=0.55)
        self.at("His Y carries")
        no_gene = T("no white gene", 28, GREY).next_to(xy[1], DOWN, buff=0.25)
        self.play(FadeOut(hemi), FadeIn(no_gene), Indicate(xy[1], color=GREY), run_time=0.8)
        self.at("A recessive white")
        male_eye = eye_badge(WHITE_EYE, 0.4).move_to([3.5, -1.35, 0])
        arrow = Arrow(xy[0].badge.get_right(), male_eye.get_left(), buff=0.15,
                      color=WHITE_EYE, stroke_width=6, tip_length=0.22)
        self.play(FadeOut(no_gene), GrowArrow(arrow), FadeIn(male_eye), run_time=1.0)
        bob(male_eye, amp=0.07, speed=1.3)
        self.at("No dominant allele")
        self.play(Indicate(xy[0].badge, color=GOLD), run_time=0.9)
        mask = T("nothing to mask it", 29, GOLD).next_to(male_eye, DOWN, buff=0.12)
        self.play(FadeIn(mask), run_time=0.7)
        self.at("A female can")
        carrier = VGroup(xx[0].badge, xx[1].badge)
        red_eye = eye_badge(RED_EYE, 0.48).move_to([-3.25, -1.75, 0])
        self.play(xx.animate.set_opacity(1), Indicate(carrier, color=GOLD),
                  FadeIn(red_eye), run_time=1.0)
        bob(red_eye, amp=0.055, speed=1.4, seed=2)
        self.play(Indicate(carrier[1], color=RED_EYE), run_time=0.8)
        self.finish()


class S04Route(SpokenScene):
    def construct(self):
        board = family_board("B", "neutral", routes=False)
        for i, card in enumerate((board.mother, board.father, board.daughter, board.son)):
            bob(card, amp=0.045, speed=1.15, seed=i)
        self.play(FadeIn(board), run_time=0.8)
        self.at("not the eye colors")
        self.play(board.mother.eye.animate.set_opacity(0.25),
                  board.father.eye.animate.set_opacity(0.25), run_time=0.6)
        self.at("Sons receive")
        self.play(Create(board.mx_s), run_time=1.2)
        traveler = Dot(board.mx_s.get_start(), color=MATERNAL, radius=0.12)
        self.play(MoveAlongPath(traveler, board.mx_s), run_time=0.9)
        self.at("while daughters")
        self.play(Create(board.mx_d), Create(board.fx_d), run_time=1.2)
        self.at("The father's Y")
        self.play(Create(board.fy_s), run_time=0.9)
        self.play(Indicate(board.son.chroms[1], color=GREY), run_time=0.8)
        self.at("That unequal route")
        route_rule = caption("Mother's X → sons and daughters; father's X → daughters.", color=GOLD)
        self.play(FadeIn(route_rule), run_time=0.8)
        self.play(ShowPassingFlash(board.tracks.copy().set_stroke(width=13), time_width=0.7), run_time=1.5)
        self.finish()


class S05FirstCross(SpokenScene):
    def construct(self):
        board = family_board("A", "neutral", routes=True)
        final_board = family_board("A", "A", routes=False)
        d_target = final_board.daughter.chroms
        s_target = final_board.son.chroms
        d_target[1].badge.set_opacity(0)
        for i, eye in enumerate((board.mother.eye, board.father.eye, board.daughter.eye, board.son.eye)):
            bob(eye, amp=0.055, speed=1.3, seed=i)
        for frame in (board.mother.frame, board.father.frame,
                      board.daughter.frame, board.son.frame):
            pulse(frame, base=2.5, amp=1.3, speed=1.25)
        for i, track in enumerate(board.tracks):
            pulse(track, base=8.0 if i < 3 else 7.0, amp=1.8, speed=1.1)
        self.add(board)
        self.play(Indicate(board.mother.eye, color=RED_EYE), run_time=0.7)
        self.at("Every child receives")
        self.play(ShowPassingFlash(VGroup(board.mx_d.copy(), board.mx_s.copy()).set_stroke(width=14),
                                   time_width=0.8), run_time=1.2)
        self.play(ReplacementTransform(board.daughter.chroms, d_target),
                  ReplacementTransform(board.son.chroms, s_target),
                  run_time=0.9)
        board.daughter.chroms = d_target
        board.son.chroms = s_target
        self.at("The white")
        self.play(ShowPassingFlash(board.fx_d.copy().set_stroke(width=14), time_width=0.8), run_time=1.0)
        self.play(FadeIn(d_target[1].badge), run_time=0.7)
        self.at("where her red")
        self.play(Indicate(board.daughter.chroms[0], color=RED_EYE), run_time=0.8)
        self.at("Every offspring")
        self.play(board.daughter.eye.animate.set_fill(RED_EYE, opacity=1),
                  board.son.eye.animate.set_fill(RED_EYE, opacity=1), run_time=0.8)
        all_red = caption("All offspring are red-eyed.", color=RED_EYE)
        self.play(FadeIn(all_red), run_time=0.6)
        self.at("The daughters carry")
        self.play(Indicate(board.daughter.chroms[1], color=WHITE_EYE), run_time=0.9)
        self.at("but their red")
        self.play(Indicate(board.daughter.chroms[0], color=RED_EYE), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        board_a = family_board("A", "A", routes=False)
        board_b = family_board("B", "neutral", routes=False)
        self.add(board_a)
        self.play(FadeTransform(board_a, board_b), run_time=1.0)
        board_a = board_b
        for i, eye in enumerate((board_a.mother.eye, board_a.father.eye,
                                 board_a.daughter.eye, board_a.son.eye)):
            bob(eye, amp=0.055, speed=1.25, seed=i)
        self.at("The mother now")
        self.play(Indicate(board_a.mother.chroms, color=WHITE_EYE), run_time=0.8)
        self.at("and the father")
        self.play(Indicate(board_a.father.chroms[0], color=RED_EYE), run_time=0.8)
        self.at("Before the chromosomes")
        neutral = VGroup(board_a.daughter.eye, board_a.son.eye)
        self.play(neutral.animate.set_opacity(0.4), run_time=0.6)
        self.at("which offspring")
        q = question_card("Which offspring are white-eyed?", y=-3.1, size=32)
        self.play(FadeIn(q), run_time=0.7)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which offspring are white-eyed?"
    SECONDS = 4.5
    CARD = {"y": -3.1, "size": 32}

    def backdrop(self):
        board = family_board("B", "neutral", routes=False)
        bob(board.mother.chroms, amp=0.035, speed=1.5)
        bob(board.father.chroms, amp=0.035, speed=1.5, seed=2)
        return board


class S08Reveal(SpokenScene):
    def construct(self):
        board = family_board("B", "neutral", routes=False)
        bob(board.mother.eye, amp=0.055, speed=1.25)
        bob(board.father.eye, amp=0.055, speed=1.25, seed=2)
        for frame in (board.mother.frame, board.father.frame,
                      board.daughter.frame, board.son.frame):
            pulse(frame, base=2.5, amp=1.3, speed=1.25)
        self.add(board)
        self.play(Create(board.fx_d), Create(board.mx_d), run_time=1.3)
        d_done = family_board("B", "B", routes=False).daughter
        self.play(Transform(board.daughter, d_done), run_time=1.0)
        self.at("She is")
        self.play(Indicate(board.daughter, color=RED_EYE, scale_factor=1.04), run_time=1.0)
        self.at("Every son")
        self.play(Create(board.mx_s), Create(board.fy_s),
                  Indicate(board.son, color=MATERNAL, scale_factor=1.04), run_time=1.2)
        s_done = family_board("B", "B", routes=False).son
        self.play(Transform(board.son, s_done), run_time=1.0)
        self.at("He is")
        self.play(Indicate(board.son, color=WHITE_EYE, scale_factor=1.04), run_time=1.0)
        self.at("This is")
        criss = caption("criss-cross inheritance", color=GOLD)
        self.play(FadeIn(criss), Indicate(VGroup(board.daughter, board.son),
                  color=GOLD, scale_factor=1.025), run_time=1.2)
        self.at("father to daughter")
        self.play(ShowPassingFlash(board.fx_d.copy().set_stroke(width=14), time_width=0.7),
                  Indicate(board.daughter, color=PATERNAL, scale_factor=1.03), run_time=0.8)
        self.at("mother to son")
        self.play(ShowPassingFlash(board.mx_s.copy().set_stroke(width=14), time_width=0.7),
                  Indicate(board.son, color=MATERNAL, scale_factor=1.03), run_time=0.8)
        self.finish()


class S09Compare(SpokenScene):
    def construct(self):
        panels = TwoPanel("Cross A", "Cross B", colors=(MATERNAL, PATERNAL), top=3.0, bottom=-2.45)
        a_par, b_par = parent_pair("A", 0.72), parent_pair("B", 0.72)
        a_res, b_res = mini_result("A"), mini_result("B")
        a = VGroup(a_par, a_res).arrange(DOWN, buff=0.65)
        b = VGroup(b_par, b_res).arrange(DOWN, buff=0.65)
        panels.put(a, "left")
        panels.put(b, "right")
        pulse(panels.left_frame, base=2.5, amp=1.3, speed=1.25)
        pulse(panels.right_frame, base=2.5, amp=1.3, speed=1.25)
        bob(a_par, amp=0.05, speed=1.2)
        bob(b_par, amp=0.05, speed=1.2, seed=2)
        self.play(FadeIn(panels), FadeIn(a_par), FadeIn(b_par), run_time=0.9)
        self.at("same red and white")
        badges = VGroup(a_par[0].eye, a_par[2].eye, b_par[0].eye, b_par[2].eye)
        self.play(Indicate(badges, color=GOLD), run_time=1.0)
        self.at("Only the carrier's")
        self.play(a_par[0].animate.shift(RIGHT * 0.08), b_par[0].animate.shift(LEFT * 0.08),
                  run_time=0.7, rate_func=there_and_back)
        self.at("Yet their first")
        self.play(FadeIn(a_res), FadeIn(b_res), run_time=0.8)
        bracket = Brace(VGroup(a_res[1], b_res[1]), DOWN, color=GOLD)
        diff = T("sons differ", 29, GOLD).next_to(bracket, DOWN, buff=0.22)
        self.play(GrowFromCenter(bracket), FadeIn(diff), run_time=0.8)
        self.at("Reciprocal crosses")
        xlinked = caption("Reciprocal crosses expose an X-linked route.", color=GOLD)
        self.play(FadeOut(diff), FadeIn(xlinked),
                  Indicate(VGroup(a, b), color=GOLD, scale_factor=1.025), run_time=2.6)
        self.at("An ordinary autosomal")
        auto = chip("autosomal: one copy from each parent", GREY, 28)
        auto.move_to([0, 0.35, 0])
        same = T("same route after the swap", 28, TEXT).next_to(auto, DOWN, buff=0.22)
        self.play(FadeOut(VGroup(panels, a, b, bracket, xlinked)),
                  FadeIn(auto), FadeIn(same), run_time=1.0)
        bob(auto, amp=0.06, speed=1.2)
        self.play(Indicate(auto, color=GREY), run_time=1.0)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        continue_tag = chip("ordinary segregation continues", GREY, 29).move_to([0, 2.75, 0])
        bob(continue_tag, amp=0.055, speed=1.2)
        self.play(FadeIn(continue_tag), run_time=0.7)
        self.at("It adds chromosome")
        ledger = Ledger([
            ("allele identity", "red or white", RED_EYE),
            ("chromosome location", "X chromosome", GOLD),
            ("parental origin", "mother or father", MATERNAL),
        ], top_left=(-5.7, 1.65), title="inheritance bookkeeping",
            row_h=0.95, key_w=4.0, width=11.4, size=30)
        self.play(FadeIn(ledger), run_time=0.7)
        self.at("Inheritance patterns")
        self.play(ledger.reveal(0), run_time=0.7)
        self.at("chromosome location")
        self.play(ledger.reveal(1), run_time=0.7)
        self.at("and parental origin")
        self.play(ledger.reveal(2), run_time=0.7)
        self.at("Here")
        self.play(ledger.mark(1, color=GOLD), run_time=0.8)
        route = caption("location changes the route", color=GOLD)
        self.play(FadeIn(route), run_time=0.7)
        self.at("Parent of origin")
        via = T("via the parent's sex", 29, MATERNAL).move_to([2.8, -1.85, 0])
        link = CurvedArrow([2.1, -0.4, 0], [2.8, -1.5, 0], angle=0.25,
                           color=MATERNAL, stroke_width=5, tip_length=0.2)
        self.play(Create(link), FadeIn(via), run_time=1.0)
        self.play(Indicate(ledger.rows[2], color=MATERNAL), run_time=1.0)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        board = family_board("B", "B", routes=True)
        board.tracks.set_opacity(0.28)
        for i, card in enumerate((board.mother, board.father, board.daughter, board.son)):
            bob(card, amp=0.045, speed=1.15, seed=i)
        self.add(board)
        spotlight = Circle(radius=0.16, color=GOLD, stroke_width=6).move_to(board.son.eye)
        self.play(FadeIn(spotlight), run_time=0.6)
        self.at("His ex points")
        reverse_s = board.mx_s.copy().reverse_points().set_stroke(opacity=1, width=11)
        self.play(MoveAlongPath(spotlight, reverse_s),
                  ShowPassingFlash(reverse_s, time_width=0.8), run_time=1.2)
        self.at("Read a daughter")
        self.play(spotlight.animate.move_to(board.daughter.eye), run_time=0.7)
        self.at("and one ex")
        reverse_d1 = board.mx_d.copy().reverse_points().set_stroke(opacity=1, width=11)
        reverse_d2 = board.fx_d.copy().reverse_points().set_stroke(opacity=1, width=11)
        s1, s2 = spotlight.copy(), spotlight.copy()
        self.play(FadeOut(spotlight), MoveAlongPath(s1, reverse_d1), MoveAlongPath(s2, reverse_d2),
                  ShowPassingFlash(reverse_d1), ShowPassingFlash(reverse_d2), run_time=1.4)
        self.at("Swapping the carrier")
        self.play(Indicate(VGroup(board.mother, board.father), color=GOLD), run_time=1.0)
        self.at("The allele itself")
        same = caption("same allele", color=TEXT)
        self.play(FadeIn(same), run_time=0.7)
        self.at("Its possible destinations")
        route_map = VGroup(
            Line([-2.6, 1.1, 0], [2.6, -1.2, 0], color=MATERNAL, stroke_width=12),
            Line([2.6, 1.1, 0], [-2.6, -1.2, 0], color=PATERNAL, stroke_width=12),
        )
        route_map.move_to([0, 0.15, 0])
        changed = caption("possible destinations changed", color=GOLD)
        self.play(FadeOut(VGroup(board, s1, s2)), FadeIn(route_map), swap(same, changed), run_time=1.2)
        self.play(ShowPassingFlash(route_map.copy().set_stroke(width=18), time_width=0.8), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "The route of an X-linked allele depends on its carrier parent."
