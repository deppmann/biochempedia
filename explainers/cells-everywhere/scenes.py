"""Cells are everywhere: too small to see, still alive  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = cells and tiny living things
  TEAL   = microscopes and their lenses
  ORANGE = size limits (the eye's limit, the light microscope's limit)
  YELLOW = vocabulary words as they are defined
  GREEN  = results, totals, the cell theory, the answer
  RED    = the crossed-out "guess"
  GREY   = outlines, axes, neutral structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def vocab(text, size=36):
    return T(text, size, YELLOW, weight=BOLD)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell_shape(w=1.2, h=0.8, x=0, y=0, color=BLUE, op=0.18):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def wander(mob, base, ax, ay, w1, w2, p, clock):
    base = np.array(base, float)
    mob.add_updater(lambda m, dt: m.move_to(base + np.array([ax * np.sin(w1 * clock() + p), ay * np.cos(w2 * clock() + 1.7 * p), 0])))


class S00Title(TitleCard):
    LESSON = "Cells are everywhere"
    TITLE = "Too small to see, still alive"


# ---------------------------------------------------------------------------------------------
class S01Drop(SpokenScene):
    def construct(self):
        cy = 0.7
        drop = Circle(radius=1.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to([-4.0, cy, 0])
        d_lbl = T("a drop of pond water", 30, TEXT).next_to(drop, DOWN, buff=0.3)
        q = T("?", 100, GREY, weight=BOLD).move_to(drop)
        clear = T("looks clear", 30, GREY).next_to(drop, UP, buff=0.25)
        self.at("completely clear")
        self.play(FadeIn(drop), FadeIn(d_lbl), FadeIn(q), FadeIn(clear), run_time=0.8)

        view = Circle(radius=2.4, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.05).move_to([3.5, cy, 0])
        mic = vocab("microscope", 38).next_to(view, UP, buff=0.25)
        link = arr([-1.8, cy, 0], [0.9, cy, 0], TEAL)
        self.at("under a microscope")
        self.play(GrowArrow(link), FadeIn(view), FadeIn(mic), run_time=0.9)

        blobs = VGroup()
        specs = [(-1.2, 0.9, 1.1, 0.65), (0.9, 1.1, 0.9, 0.55), (-0.5, -0.7, 1.2, 0.7), (1.1, -0.6, 1.0, 0.6), (0.1, 0.1, 0.75, 0.46)]
        for i, (dx, dy, w, h) in enumerate(specs):
            b = cell_shape(w, h, 3.5 + dx, cy + dy)
            wander(b, [3.5 + dx * 0.8, cy + dy * 0.8, 0], 0.35, 0.3, 0.9 + 0.2 * i, 0.7 + 0.15 * i, i * 1.3, self.elapsed)
            blobs.add(b)
        lv = T("tiny living things", 30, BLUE).next_to(view, DOWN, buff=0.25)
        self.at("tiny living things")
        self.play(FadeIn(blobs, lag_ratio=0.2), FadeIn(lv), run_time=0.9)
        self.at("swimming and turning")
        self.wait(0.1)

        ques = T("How can we know it is alive if it is too small to see?", 34, TEXT)
        fit(ques, max_w=12.2)
        ques.move_to([0, -3.35, 0])
        self.at("How can we know")
        self.play(FadeIn(ques, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Limit(SpokenScene):
    def construct(self):
        x0, x1, y = -6.0, 6.0, 0.9
        bar = Rectangle(width=12, height=0.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15).move_to([0, y, 0])
        mm = T("1 millimetre (mm)", 34, TEXT).next_to(bar, UP, buff=0.3)
        self.at("Your eyes have a limit")
        self.play(FadeIn(bar), FadeIn(mm), run_time=0.8)

        seg = Rectangle(width=1.2, height=0.8, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.55).move_to([x0 + 0.6, y, 0])
        tenth = M("0.1 mm", 34, ORANGE, weight=BOLD).next_to(seg, DOWN, buff=0.25, aligned_edge=LEFT)
        self.at("one tenth of a")
        self.play(FadeIn(seg), FadeIn(tenth), run_time=0.7)

        mu = vocab("micrometre (µm)", 38).move_to([2.2, -0.7, 0])
        mu_eq = M("1 mm = 1,000 µm", 32, TEXT).next_to(mu, DOWN, buff=0.25)
        self.at("A micrometer is")
        self.play(FadeIn(mu), run_time=0.5)
        self.at("one thousandth")
        self.play(FadeIn(mu_eq), run_time=0.5)

        lim = M("about 100 µm", 34, ORANGE, weight=BOLD).move_to(tenth, aligned_edge=LEFT)
        self.at("So the limit")
        self.play(ReplacementTransform(tenth, lim), run_time=0.6)

        # enlarge the first tenth: what is inside is smaller than the eye's limit (not to scale)
        top = VGroup(bar, mm, seg)
        self.at("Most cells are smaller")
        self.play(FadeOut(mu), FadeOut(mu_eq), FadeOut(lim), top.animate.shift(UP * 1.5), run_time=0.7)
        y2 = y + 1.5
        box = Rectangle(width=12, height=2.9, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.05).move_to([0, -1.3, 0])
        l1 = DashedLine([x0, y2 - 0.4, 0], [x0, 0.15, 0], color=ORANGE, stroke_width=3)
        l2 = DashedLine([x0 + 1.2, y2 - 0.4, 0], [x1, 0.15, 0], color=ORANGE, stroke_width=3)
        lim2 = M("the limit: about 100 µm across this box", 28, ORANGE, weight=BOLD).move_to([0, -0.2, 0])
        self.play(Create(l1), Create(l2), FadeIn(box), FadeIn(lim2), run_time=0.6)
        cells = VGroup(cell_shape(1.2, 0.8, -3.6, -1.5), cell_shape(0.7, 0.48, -0.8, -1.2), cell_shape(1.0, 0.65, 1.9, -1.8),
                       cell_shape(0.5, 0.34, 4.2, -1.3), cell_shape(0.8, 0.54, 4.9, -1.95))
        note = T("most cells are smaller than the limit (not to scale)", 30, BLUE).move_to([0, -3.2, 0])
        self.play(FadeIn(cells, lag_ratio=0.2), FadeIn(note), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Scope(SpokenScene):
    def construct(self):
        mic = vocab("microscope", 40).to_edge(UP, buff=0.5)
        self.at("A microscope is a tool")
        self.play(FadeIn(mic), run_time=0.5)
        sample = Square(0.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([-4.6, 0.2, 0])
        s_lbl = T("real thing", 30, TEXT).move_to([-4.6, -1.9, 0])
        lens = Ellipse(width=0.9, height=3.2, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.2).move_to([0, 0.2, 0])
        l_lbl = T("lenses", 30, TEAL).move_to([0, -1.9, 0])
        self.at("with lenses")
        self.play(FadeIn(sample), FadeIn(s_lbl), FadeIn(lens), FadeIn(l_lbl), run_time=0.8)
        a1 = arr([-3.8, 0.2, 0], [-0.7, 0.2, 0], TEAL)
        a2 = arr([0.7, 0.2, 0], [2.3, 0.2, 0], TEAL)
        image = Square(2.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([4.6, 0.2, 0])
        i_lbl = T("image looks larger", 30, BLUE).move_to([4.6, -1.9, 0])
        self.at("larger")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.4)
        self.play(FadeIn(image), FadeIn(i_lbl), run_time=0.4)
        mag = vocab("magnification", 44).move_to([0, 2.6, 0])
        mag_d = T("how many times larger the image looks than the real thing", 28, TEXT).move_to([0, -3.1, 0])
        self.at("Magnification is")
        self.play(ReplacementTransform(mic, mag), FadeIn(mag_d), run_time=0.6)
        self.wait(0.1)

        # phase B: eyepiece x objective = total
        first = VGroup(sample, s_lbl, lens, l_lbl, a1, a2, image, i_lbl, mag_d)
        eye = chip("eyepiece: 10x", TEAL, size=36).move_to([-3.7, 1.2, 0])
        self.at("A school microscope")
        self.play(FadeOut(first), run_time=0.4)
        self.play(FadeIn(eye), run_time=0.5)
        ob_lbl = T("objective lenses (often)", 32, TEAL).move_to([-3.7, -0.1, 0])
        ob = VGroup(*[chip(t, TEAL, size=36) for t in ["4x", "10x", "40x"]]).arrange(RIGHT, buff=0.3).move_to([-3.7, -1.2, 0])
        self.at("Its objective lenses")
        self.play(FadeIn(ob_lbl), FadeIn(ob, lag_ratio=0.3), run_time=0.9)
        rows = VGroup(*[VGroup(M(f"10x × {o}", 40, TEXT), M("=", 40, GREY), M(t, 44, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.3)
                        for o, t in [("4x", "40x"), ("10x", "100x"), ("40x", "400x")]]).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.4, 0.4, 0])
        self.at("Multiply them")
        self.play(FadeIn(rows[0]), run_time=0.5)
        self.at("That gives")
        self.play(FadeIn(rows[1]), run_time=0.5)
        self.play(FadeIn(rows[2]), run_time=0.5)
        tot = T("total magnification", 32, GREEN).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(tot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Light(SpokenScene):
    def construct(self):
        def X(s):  # log10 axis, 2.4 units per decade, 0.01 um at the left
            return -6.0 + 2.4 * (np.log10(s) + 2)
        ay = 0.5
        axis = Arrow([-6.2, ay, 0], [6.3, ay, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        ticks = VGroup()
        for v, lab in [(0.01, ""), (0.1, ""), (1, "1"), (10, "10"), (100, "100"), (1000, "1,000")]:
            ticks.add(Line([X(v), ay - 0.14, 0], [X(v), ay + 0.14, 0], color=GREY, stroke_width=3))
            if lab:
                ticks.add(M(lab, 26, GREY).move_to([X(v), ay - 0.5, 0]))
        ax_lbl = T("size in micrometres (µm), each step is 10 times", 26, GREY).move_to([0, ay - 1.05, 0])
        lm = Line([X(0.2), ay + 1.0, 0], [X(0.2), ay - 0.15, 0], color=ORANGE, stroke_width=5)
        lm_t = T("light microscope:\nfinest detail\nabout 0.2 µm", 30, ORANGE)
        lm_t.move_to([X(0.2) + 0.25 + lm_t.width / 2, ay + 2.2, 0])
        self.at("A light microscope")
        self.play(Create(axis), FadeIn(ticks), FadeIn(ax_lbl), run_time=0.9)
        self.at("details down to")
        self.play(Create(lm), FadeIn(lm_t), run_time=0.7)

        x_mid = (X(0.2) + 6.2) / 2
        band = Rectangle(width=6.2 - X(0.2), height=0.55, stroke_width=0, fill_color=GREEN, fill_opacity=0.25).move_to([x_mid, ay, 0])
        band_t = T("a light microscope can show\nthings this size and larger", 28, GREEN, weight=BOLD).move_to([0.5, ay + 0.95, 0])
        eye_l = Line([X(100), ay + 1.6, 0], [X(100), ay - 0.15, 0], color=ORANGE, stroke_width=5)
        eye_t = T("limit of the eye:\nabout 100 µm", 28, ORANGE).move_to([X(100), ay + 2.2, 0])
        self.at("enough to see most whole cells")
        self.play(FadeIn(band), FadeIn(band_t), run_time=0.8)
        self.play(Create(eye_l), FadeIn(eye_t), run_time=0.6)

        ey = ay - 2.3
        el = arr([X(0.2), ey, 0], [-6.1, ey, 0], TEAL)
        el_t = vocab("electron microscope", 34)
        el_t.set_color(TEAL)
        el_t.move_to([X(0.2) + 0.35 + el_t.width / 2, ey + 0.2, 0])
        el_n = T("a beam of electrons, not light", 28, TEXT).next_to(el_t, DOWN, buff=0.15, aligned_edge=LEFT)
        sm = T("cell parts far too small\nfor any light microscope", 26, TEAL).move_to([-4.3, ey - 0.95, 0])
        self.at("electron microscope")
        self.play(FadeIn(el_t), run_time=0.5)
        self.at("It uses a beam")
        self.play(FadeIn(el_n), run_time=0.5)
        self.at("It showed cell parts")
        self.play(GrowArrow(el), FadeIn(sm), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def card_state(card, on, dur=0.4):
    box, n, lab = card
    return [box.animate.set_fill(GREEN, 0.35 if on else 0.08).set_stroke(GREEN, opacity=1 if on else 0.4),
            n.animate.set_opacity(1 if on else 0.4), lab.animate.set_opacity(1 if on else 0.45)]


class S05Theory(SpokenScene):
    def construct(self):
        cell = cell_shape(3.0, 2.0, 3.6, 0.5)
        c_lbl = vocab("cell", 40).next_to(cell, DOWN, buff=0.35)
        self.at("A cell is the smallest unit")
        self.play(FadeIn(cell), FadeIn(c_lbl), run_time=0.7)
        head = vocab("cell theory", 42).to_edge(UP, buff=0.5)
        self.at("The cell theory")
        self.play(FadeIn(head), run_time=0.5)
        self.at("three parts")
        texts = ["All living things are made of\none or more cells", "The cell is the basic\nunit of life", "All cells come from cells\nthat already exist"]
        cards = VGroup()
        for i, t in enumerate(texts):
            n = T(str(i + 1), 44, GREEN, weight=BOLD)
            lab = T(t, 28, TEXT)
            box = RoundedRectangle(corner_radius=0.14, width=6.4, height=1.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.08)
            n.move_to(box.get_left() + RIGHT * 0.6)
            lab.move_to(box.get_left() + RIGHT * (1.1 + lab.width / 2))
            cards.add(VGroup(box, n, lab))
        cards.arrange(DOWN, buff=0.35).move_to([-3.2, -0.4, 0])
        for c in cards:
            c[0].set_stroke(opacity=0.4); c[1].set_opacity(0.4); c[2].set_opacity(0.45)
        self.play(FadeIn(cards), run_time=0.5)

        # part 1: one cell, or many cells
        self.at("First")
        self.play(*card_state(cards[0], True), run_time=0.4)
        grid = VGroup(*[cell_shape(0.9, 0.62, 0, 0) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.14)
        g_lbl = T("many cells", 32, BLUE)
        self.at("one or more cells")
        one_lbl = T("one cell", 32, BLUE).move_to([1.5, -1.2, 0])
        self.play(cell.animate.move_to([1.5, 0.5, 0]).scale(0.62), ReplacementTransform(c_lbl, one_lbl), run_time=0.6)
        grid.move_to([4.9, 0.5, 0]); g_lbl.move_to([4.9, -1.2, 0])
        self.play(FadeIn(grid, lag_ratio=0.1), FadeIn(g_lbl), run_time=0.8)

        # part 2: basic unit
        self.at("Second")
        self.play(*card_state(cards[0], False), *card_state(cards[1], True),
                  FadeOut(grid), FadeOut(g_lbl), FadeOut(one_lbl), cell.animate.move_to([3.6, 0.5, 0]).scale(1 / 0.62), run_time=0.7)
        unit = T("basic unit of life", 34, GREEN, weight=BOLD).move_to([3.6, -1.3, 0])
        self.at("basic unit of life")
        self.play(FadeIn(unit), Indicate(cell, color=GREEN, scale_factor=1.08), run_time=0.8)

        # part 3: from a cell
        self.at("Third")
        self.play(*card_state(cards[1], False), *card_state(cards[2], True), FadeOut(unit),
                  cell.animate.move_to([1.5, 0.5, 0]).scale(0.62), run_time=0.7)
        new = cell_shape(1.9, 1.3, 5.0, 0.5, color=GREEN)
        nl = T("new cell", 30, GREEN).move_to([5.0, -0.7, 0])
        ol = T("cell that\nalready exists", 28, BLUE).move_to([1.5, -0.8, 0])
        link = arr([2.5, 0.5, 0], [3.9, 0.5, 0], GREEN)
        self.at("come from cells that")
        self.play(FadeIn(ol), GrowArrow(link), run_time=0.5)
        self.play(FadeIn(new), FadeIn(nl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        th = vocab("theory", 46).move_to([0, 2.7, 0])
        defn = T("a well-tested explanation backed by\na great deal of evidence", 36, TEXT).move_to([0, 1.3, 0])
        self.at("In science, a theory")
        self.play(FadeIn(th), run_time=0.5)
        self.at("well tested explanation")
        self.play(FadeIn(defn), run_time=0.8)
        guess = T("a guess", 48, GREY).move_to([0, -0.5, 0])
        self.at("It is not a guess")
        self.play(FadeIn(guess), run_time=0.4)
        cross = Line(guess.get_left() + LEFT * 0.2, guess.get_right() + RIGHT * 0.2, color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.4)

        tools = VGroup(*[chip(t, TEAL, size=32) for t in ["eye", "light microscope", "electron microscope"]]).arrange(RIGHT, buff=0.8).move_to([0, 0.0, 0])
        links = VGroup(arr(tools[0].get_right(), tools[1].get_left(), TEAL), arr(tools[1].get_right(), tools[2].get_left(), TEAL))
        ev = chip("new evidence", GREEN, size=34).move_to([0.2, -1.9, 0])
        evar = VGroup(*[Arrow(t.get_bottom(), ev.get_top() + RIGHT * dx, buff=0.1, color=GREEN, stroke_width=5, tip_length=0.22) for t, dx in [(tools[1], -0.5), (tools[2], 0.5)]])
        ct = chip("cell theory", GREEN, size=36).move_to([4.4, -1.9, 0])
        ctar = arr(ev.get_right(), ct.get_left(), GREEN)
        self.at("The cell theory grew")
        self.play(FadeOut(guess), FadeOut(cross), FadeOut(th), FadeOut(defn), run_time=0.4)
        self.play(FadeIn(tools[1]), run_time=0.4)
        self.at("better microscopes")
        self.play(FadeIn(tools[0]), GrowArrow(links[0]), run_time=0.4)
        self.play(FadeIn(tools[2]), GrowArrow(links[1]), run_time=0.4)
        self.at("new evidence")
        self.play(*[GrowArrow(a) for a in evar], FadeIn(ev), run_time=0.5)
        self.play(GrowArrow(ctar), FadeIn(ct), run_time=0.5)
        self.wait(0.3)

        # the answer: drop -> microscope -> cells
        old = VGroup(tools, links, ev, evar, ct, ctar)
        self.at("So how do we know")
        q = T("How do we know it is alive\nwhen it is too small to see?", 34, TEXT).to_edge(UP, buff=0.45)
        self.play(FadeOut(old), FadeIn(q), run_time=0.5)
        cy = -0.6
        drop = Circle(radius=1.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to([-4.4, cy, 0])
        d_l = T("pond water drop", 28, TEXT).next_to(drop, DOWN, buff=0.25)
        view = Circle(radius=2.1, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.05).move_to([3.2, cy, 0])
        m_l = T("microscope", 30, TEAL).next_to(view, UP, buff=0.2)
        lk = arr([-2.5, cy, 0], [0.9, cy, 0], TEAL)
        self.at("A microscope makes it")
        self.play(FadeIn(drop), FadeIn(d_l), GrowArrow(lk), FadeIn(view), FadeIn(m_l), run_time=0.9)
        cells = VGroup(cell_shape(1.0, 0.65, 2.3, cy + 0.6), cell_shape(0.75, 0.5, 3.9, cy + 0.4), cell_shape(1.1, 0.7, 2.8, cy - 0.7), cell_shape(0.7, 0.46, 3.9, cy - 0.8))
        for i, c in enumerate(cells):
            wander(c, c.get_center(), 0.14, 0.12, 0.9 + 0.2 * i, 0.7 + 0.15 * i, i * 1.3, self.elapsed)
        self.at("large enough to see")
        self.play(FadeIn(cells, lag_ratio=0.2), run_time=0.7)
        ans = T("each one is made of one or more cells", 34, GREEN, weight=BOLD).move_to([0, -3.35, 0])
        fit(ans, max_w=12.2)
        self.at("made of one or more cells")
        self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A microscope shows each one is made of cells."
