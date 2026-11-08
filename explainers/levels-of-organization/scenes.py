"""Sharing the work among cells  (Biochemistrypedia Life Science explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = moving / cilia
  ORANGE = eating / food vacuoles
  BLUE   = extra water / contractile vacuole
  GREEN  = dividing
  PURPLE = muscle cell (and the first job group)
  TEAL   = nerve cell (and the second job group)
  RED    = red blood cell (and the third job group); also damage in s06
  GOLD   = the levels of organization, and the words division of labor
  GREY   = outlines, the pond drop, blood vessel walls, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def cell_shape(w=1.8, h=0.7, color=TEXT, fill=0.12, sw=3):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


def job_grid(cols=5, rows=3, s=0.9, center=(0, -0.2)):
    cells = VGroup(*[
        RoundedRectangle(corner_radius=0.12, width=s - 0.12, height=s - 0.12, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.15)
        for _ in range(cols * rows)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=0.12)
    cells.move_to([center[0], center[1], 0])
    return cells


def group_colors(cols, rows):
    """column groups: first 2 purple, next 1 teal, last rest red."""
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(PURPLE if c < 2 else (TEAL if c == 2 else RED))
    return out


def lvl_chip(text, size=26):
    return chip(text, GOLD, size=size)


class S00Title(TitleCard):
    LESSON = "From cells to organisms"
    TITLE = "Sharing the work among cells"


# ---------------------------------------------------------------------------------------------
class S01Drop(SpokenScene):
    def construct(self):
        drop = Circle(radius=2.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([-3.4, 0.3, 0])
        drop_lbl = T("a drop of pond water", 26, GREY).next_to(drop, DOWN, buff=0.2)
        self.at("Picture a drop")
        self.play(FadeIn(drop), FadeIn(drop_lbl), run_time=0.8)
        para = cell_shape(2.0, 0.8, TEXT).move_to([-4.2, 1.0, 0]).rotate(0.25)
        name = T("Paramecium", 28, TEXT, weight=BOLD)
        name.move_to([-3.4, -0.6, 0])
        self.at("A Paramecium swims")
        self.play(FadeIn(para, scale=0.8), run_time=0.5)
        self.play(para.animate.move_to([-2.8, 0.2, 0]).rotate(-0.4), run_time=1.2)
        self.play(para.animate.move_to([-3.4, 1.0, 0]).rotate(0.3), run_time=1.0)
        tag = T("one cell", 28, TEXT).move_to([-3.4, -1.25, 0])
        self.at("one cell")
        self.play(FadeIn(name), FadeIn(tag), run_time=0.5)
        # job chips
        jobs = [("moves", YELLOW, 2.3), ("eats", ORANGE, 1.1), ("removes extra water and wastes", BLUE, -0.1), ("divides", GREEN, -1.3)]
        chips = {}
        for text, col, y in jobs:
            c = chip(text, col, size=30)
            c.move_to([3.6, y, 0])
            c.align_to([6.2, 0, 0], RIGHT) if c.width > 5.4 else None
            chips[text] = c
        self.at("moves")
        self.play(FadeIn(chips["moves"], shift=LEFT * 0.2), para.animate.shift(RIGHT * 0.5 + DOWN * 0.3), run_time=0.6)
        self.at("eats")
        self.play(FadeIn(chips["eats"], shift=LEFT * 0.2), run_time=0.5)
        self.at("gets rid of extra water")
        self.play(FadeIn(chips["removes extra water and wastes"], shift=LEFT * 0.2), run_time=0.5)
        self.at("divide in two")
        a = cell_shape(1.1, 0.7, TEXT).move_to(para.get_center())
        b = cell_shape(1.1, 0.7, TEXT).move_to(para.get_center())
        self.play(FadeIn(chips["divides"], shift=LEFT * 0.2), FadeOut(para), FadeIn(a), FadeIn(b), run_time=0.3)
        self.play(a.animate.shift(LEFT * 0.7 + UP * 0.1), b.animate.shift(RIGHT * 0.7 + DOWN * 0.1), run_time=1.0)
        self.at("Your body does")
        q = T("So why does your body have trillions of cells?", 34, GOLD, weight=BOLD).move_to([0, -3.2, 0])
        self.at("trillions of cells")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Onecell(SpokenScene):
    def construct(self):
        cen = np.array([0, -0.3, 0])
        top = T("unicellular: one cell", 36, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        cell = Ellipse(width=6.4, height=2.6, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.06).move_to(cen)
        self.at("unicellular")
        self.play(FadeIn(top), Create(cell), run_time=1.0)
        # cilia
        ticks = VGroup()
        for t in np.linspace(0, 2 * np.pi, 48, endpoint=False):
            p = cen + np.array([3.2 * np.cos(t), 1.3 * np.sin(t), 0])
            d = np.array([np.cos(t) / 3.2, np.sin(t) / 1.3, 0]); d = d / np.linalg.norm(d)
            ticks.add(Line(p, p + d * 0.28, color=YELLOW, stroke_width=3))
        cil_lbl = T("cilia", 28, YELLOW, weight=BOLD).move_to([-5.0, 1.9, 0])
        cil_arrow = Arrow(cil_lbl.get_right() + RIGHT * 0.05, cen + np.array([-2.35, 0.95, 0]), buff=0.08, color=YELLOW, stroke_width=4, tip_length=0.2)
        self.at("cilia")
        self.play(Create(ticks, lag_ratio=0.02), run_time=1.2)
        self.play(FadeIn(cil_lbl), GrowArrow(cil_arrow), run_time=0.5)
        self.play(ticks.animate.shift(RIGHT * 0.0).set_opacity(1.0), run_time=0.1)
        # food vacuoles
        fv1 = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.3).move_to(cen + np.array([-1.5, -0.2, 0]))
        fv2 = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.3).move_to(cen + np.array([-0.5, -0.5, 0]))
        fv_lbl = T("food vacuoles", 28, ORANGE, weight=BOLD).move_to([-3.3, -2.5, 0])
        fv_a1 = Arrow(fv_lbl.get_top() + UP * 0.05, fv1.get_bottom(), buff=0.08, color=ORANGE, stroke_width=4, tip_length=0.2)
        self.at("food vacuoles")
        self.play(FadeIn(fv1, scale=0.5), FadeIn(fv2, scale=0.5), FadeIn(fv_lbl), GrowArrow(fv_a1), run_time=0.8)
        # contractile vacuole
        cv = Circle(radius=0.42, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(cen + np.array([1.6, 0.0, 0]))
        cv_lbl = T("contractile\nvacuole", 28, BLUE, weight=BOLD, line_spacing=0.8).move_to([5.1, -0.3, 0])
        cv_a = Arrow(cv_lbl.get_left() + LEFT * 0.05, cv.get_right(), buff=0.08, color=BLUE, stroke_width=4, tip_length=0.2)
        self.at("contractile vacuole")
        self.play(FadeIn(cv, scale=0.5), FadeIn(cv_lbl), GrowArrow(cv_a), run_time=0.8)
        self.at("squeezes out extra water")
        drop = Dot(radius=0.14, color=BLUE).move_to(cv.get_center())
        self.play(cv.animate.scale(0.4), FadeIn(drop), run_time=0.4)
        self.play(drop.animate.move_to(cen + np.array([1.6, -2.0, 0])), run_time=1.2)
        self.play(FadeOut(drop), cv.animate.scale(2.5), run_time=0.4)
        bot = T("one cell has parts for every life job", 32, GOLD, weight=BOLD).move_to([0, -3.3, 0])
        self.at("every life job")
        self.play(FadeIn(bot, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Many(SpokenScene):
    def construct(self):
        cols, rows = 5, 3
        top = T("multicellular: many cells", 36, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        grid = job_grid(cols, rows, 1.25, (0, 0.2))
        self.at("multicellular")
        self.play(FadeIn(top), LaggedStartMap(FadeIn, grid, lag_ratio=0.05), run_time=1.5)
        you = chip("you", TEXT, size=30).move_to([-5.4, 0.2, 0])
        oak = chip("an oak tree", TEXT, size=30).move_to([5.0, 0.2, 0])
        self.at("You are multicellular")
        self.play(FadeIn(you, shift=RIGHT * 0.2), run_time=0.5)
        self.at("oak tree")
        self.play(FadeIn(oak, shift=LEFT * 0.2), run_time=0.5)
        self.at("cells share the work")
        cols_list = group_colors(cols, rows)
        self.play(*[g.animate.set_stroke(c).set_fill(c, 0.35) for g, c in zip(grid, cols_list)], FadeOut(you), FadeOut(oak), run_time=1.2)
        dol = T("division of labor", 38, GOLD, weight=BOLD).move_to([0, -2.3, 0])
        self.at("division of labor")
        self.play(FadeIn(dol, shift=UP * 0.15), run_time=0.6)
        self.at("specialized cell")
        sp = T("specialized cell: shape and parts suit one job", 30, TEXT).move_to([0, -3.1, 0])
        # one cell highlighted
        hi = SurroundingRectangle(grid[7], color=TEXT, buff=0.06, stroke_width=4)
        self.play(Create(hi), FadeIn(sp, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Shapes(SpokenScene):
    def construct(self):
        # row 1: muscle
        mus = RoundedRectangle(corner_radius=0.25, width=3.4, height=0.55, stroke_color=PURPLE, stroke_width=4,
                               fill_color=PURPLE, fill_opacity=0.3).move_to([-3.6, 2.1, 0])
        m_name = T("muscle cell", 34, PURPLE, weight=BOLD).move_to([0.6, 2.4, 0]).align_to([-1.0, 0, 0], LEFT)
        m_desc = T("long and thin: shortens to pull on bones", 26, GREY).next_to(m_name, DOWN, buff=0.12).align_to(m_name, LEFT)
        self.at("A muscle cell")
        self.play(FadeIn(mus, scale=0.9), FadeIn(m_name), run_time=0.6)
        self.play(FadeIn(m_desc), run_time=0.4)
        self.at("shortens")
        self.play(mus.animate.stretch_to_fit_width(2.2), run_time=0.8)
        self.wait(0.3)
        self.play(mus.animate.stretch_to_fit_width(3.4), run_time=0.6)
        # row 2: nerve
        body = Circle(radius=0.32, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.3).move_to([-5.2, 0.0, 0])
        lines = VGroup(
            Line(body.get_center() + LEFT * 0.3 + UP * 0.1, [-5.95, 0.45, 0]), Line(body.get_center() + LEFT * 0.3 + DOWN * 0.1, [-5.95, -0.45, 0]),
            Line(body.get_right(), [-2.7, 0.0, 0]), Line([-2.7, 0, 0], [-2.35, 0.35, 0]), Line([-2.7, 0, 0], [-2.35, -0.35, 0]))
        lines.set_color(TEAL).set_stroke(width=4)
        n_name = T("nerve cell", 34, TEAL, weight=BOLD).move_to([0, 0.3, 0]).align_to([-1.0, 0, 0], LEFT)
        n_desc = T("long branches: signals over long distances", 26, GREY).next_to(n_name, DOWN, buff=0.12).align_to(n_name, LEFT)
        self.at("A nerve cell")
        self.play(FadeIn(body, scale=0.8), FadeIn(n_name), run_time=0.6)
        self.at("long branches")
        self.play(Create(lines), run_time=0.9)
        self.at("long distances")
        self.play(FadeIn(n_desc), run_time=0.5)
        sig = Dot(radius=0.12, color=YELLOW).move_to(body.get_right())
        self.play(FadeIn(sig), run_time=0.1)
        self.play(sig.animate.move_to([-2.7, 0, 0]), run_time=0.9)
        self.play(FadeOut(sig), run_time=0.1)
        # row 3: red blood cell
        w_top = VGroup(Line([-3.5, -1.35, 0], [-2.7, -1.75, 0]), Line([-2.7, -1.75, 0], [-1.2, -1.75, 0])).set_color(GREY).set_stroke(width=5)
        w_bot = VGroup(Line([-3.5, -2.85, 0], [-2.7, -2.45, 0]), Line([-2.7, -2.45, 0], [-1.2, -2.45, 0])).set_color(GREY).set_stroke(width=5)
        rbc = Ellipse(width=1.2, height=0.95, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.3).move_to([-5.0, -2.1, 0])
        r_name = T("red blood cell", 34, RED, weight=BOLD).move_to([0, -1.8, 0]).align_to([-1.0, 0, 0], LEFT)
        r_desc = T("small, flexible disc: carries oxygen", 26, GREY).next_to(r_name, DOWN, buff=0.12).align_to(r_name, LEFT)
        self.at("A red blood cell")
        self.play(FadeIn(rbc, scale=0.8), FadeIn(r_name), run_time=0.6)
        self.at("small")
        self.play(FadeIn(r_desc), run_time=0.5)
        self.at("very narrow vessels")
        self.play(Create(w_top), Create(w_bot), run_time=0.6)
        self.play(rbc.animate.move_to([-3.1, -2.1, 0]), run_time=0.8)
        self.play(rbc.animate.move_to([-2.0, -2.1, 0]).stretch_to_fit_height(0.5).stretch_to_fit_width(1.4), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
LEVELS = [("cell", "a muscle cell"), ("tissue", "muscle tissue"), ("organ", "the heart"),
          ("organ system", "the heart and blood vessels"), ("organism", "the whole body")]
YS = [2.5, 1.25, 0.0, -1.25, -2.5]


def build_levels(size=30):
    chips, arrows, ex = [], [], []
    for (name, e), y in zip(LEVELS, YS):
        c = lvl_chip(name, size).move_to([0, y, 0]).align_to([-4.0, 0, 0], LEFT)
        chips.append(c)
        ex.append(T(e, 28, GREY).move_to([0, y, 0]).align_to([0.3, 0, 0], LEFT))
    for a, b in zip(chips, chips[1:]):
        arrows.append(Arrow([-3.4, a.get_bottom()[1], 0], [-3.4, b.get_top()[1], 0], buff=0.04, color=GOLD, stroke_width=4, tip_length=0.18))
    return chips, arrows, ex


class S05Levels(SpokenScene):
    def construct(self):
        chips, arrows, ex = build_levels()
        head = VGroup()
        self.at("Cells are grouped")
        self.play(FadeIn(chips[0]), run_time=0.6)
        self.at("form a tissue")
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1], shift=DOWN * 0.1), run_time=0.5)
        self.at("muscle tissue")
        self.play(FadeIn(ex[0]), FadeIn(ex[1]), run_time=0.5)
        self.at("form an organ")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2], shift=DOWN * 0.1), run_time=0.5)
        self.at("such as the heart")
        self.play(FadeIn(ex[2]), run_time=0.5)
        self.at("Organs working together")
        self.play(GrowArrow(arrows[2]), FadeIn(chips[3], shift=DOWN * 0.1), run_time=0.5)
        self.at("blood vessels")
        self.play(FadeIn(ex[3]), run_time=0.5)
        self.at("make the organism")
        self.play(GrowArrow(arrows[3]), FadeIn(chips[4], shift=DOWN * 0.1), FadeIn(ex[4]), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        chips, arrows, ex = build_levels()
        head = VGroup()
        self.add(*chips, *arrows, *ex)
        self.at("heart tissue is damaged")
        self.play(chips[1][0].animate.set_stroke(RED).set_fill(RED, 0.3), chips[1][1].animate.set_color(RED), run_time=0.5)
        self.at("whole body can suffer")
        anims = []
        for c in chips[2:]:
            anims += [c[0].animate.set_stroke(RED).set_fill(RED, 0.3), c[1].animate.set_color(RED)]
        self.play(LaggedStart(*anims, lag_ratio=0.15), run_time=1.2)
        self.at("So how can one cell")
        self.play(FadeOut(VGroup(head, *chips, *arrows, *ex)), run_time=0.6)
        q = T("How can one cell do what a whole body does?", 34, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(q), run_time=0.4)
        para = cell_shape(5.0, 2.0, TEXT, 0.08, 4).move_to([-3.4, 0.7, 0])
        pl = T("one cell: parts for every job", 28, TEXT).move_to([-3.4, -1.0, 0])
        self.at("A Paramecium does it")
        self.play(FadeIn(para, scale=0.9), FadeIn(pl), run_time=0.7)
        grid = job_grid(4, 3, 0.95, (3.4, 0.7))
        bl = T("a body: jobs shared by\ntrillions of cells", 28, TEXT, line_spacing=0.8).move_to([3.4, -1.6, 0])
        self.at("A body shares the jobs")
        self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.05), FadeIn(bl), run_time=1.0)
        self.play(*[g.animate.set_stroke(c).set_fill(c, 0.35) for g, c in zip(grid, group_colors(4, 3))], run_time=0.8)
        lv = T("grouped into tissues, organs and organ systems", 32, GOLD, weight=BOLD).move_to([0, -2.9, 0])
        self.at("organ systems")
        self.play(FadeIn(lv, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "One cell can do every job; a body shares them."
