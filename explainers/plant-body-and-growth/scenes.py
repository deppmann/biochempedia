"""Plant body and growth: a root grows by cells times length  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = new cells / the zone of division / the rate of new cells
  ORANGE = elongation / the zone of elongation / final cell length
  GREEN  = maturation / mature cells
  TEAL   = water in the vacuoles
  YELLOW = the result: root growth rate (equation, bars, tip movement)
  RED    = blocked or halved (the changed condition)
  GREY   = root cap, outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEAL_W = "#3FB8C0"
BASE_X = 6.2


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def mix(c1, c2, a):
    return interpolate_color(ManimColor(c1), ManimColor(c2), a)


# ---------------------------------------------------------------------------------------------
# schematic root strip: tip at the LEFT, root cap, three zones (not to scale)
# ---------------------------------------------------------------------------------------------
class Strip:
    X0 = -5.2
    H = 2.4
    CAP = 0.9
    DIV = [0.7, 0.7, 0.7]
    EL = [0.7, 0.9, 1.1, 1.2]
    MAT = [1.7, 1.7]

    def __init__(self, y=0.5, colored=False, vac=0.2, hairs=False):
        H = self.H
        x = self.X0
        self.cap = RoundedRectangle(corner_radius=0.3, width=self.CAP, height=H * 0.9, stroke_color=GREY,
                                    stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([x + self.CAP / 2, y, 0])
        x += self.CAP
        self.x_div0 = x
        self.div, self.divlines = VGroup(), VGroup()
        for w in self.DIV:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            self.div.add(r)
            self.divlines.add(Line([x + w / 2, y - H / 2, 0], [x + w / 2, y + H / 2, 0], stroke_width=2.5))
            x += w
        self.x_el0 = x
        self.el, self.vacs = VGroup(), VGroup()
        for w in self.EL:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            v = RoundedRectangle(corner_radius=0.12, width=w * vac * 3.2 / 3.2, height=H * 0.15 + H * 0.6 * vac,
                                 stroke_width=0, fill_color=TEAL_W, fill_opacity=0.5).move_to(r)
            v.full_w = w * 0.78
            v.full_h = H * 0.75
            self.el.add(r)
            self.vacs.add(v)
            x += w
        self.x_mat0 = x
        self.mat = VGroup()
        for w in self.MAT:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            self.mat.add(r)
            x += w
        self.x_end = x
        self.y = y
        self.hairs = VGroup()
        for r in self.mat:
            for k in (-0.4, 0.0, 0.4):
                cx = r.get_center()[0] + k * r.width * 0.9
                self.hairs.add(Line([cx, y + H / 2, 0], [cx, y + H / 2 + 0.45, 0], stroke_width=3.5),
                               Line([cx, y - H / 2, 0], [cx, y - H / 2 - 0.45, 0], stroke_width=3.5))
        self.set_colors(GREY, GREY, GREY)
        if colored:
            self.set_colors(BLUE, ORANGE, GREEN)
        self.hairs.set_color(GREEN)
        self.set_vac(vac)
        self.divlines.set_color(BLUE)
        self.show_hairs = hairs

    def set_colors(self, cd, ce, cm):
        for grp, c in ((self.div, cd), (self.el, ce), (self.mat, cm)):
            for r in grp:
                r.set_stroke(c).set_fill(c, 0.14)

    def set_vac(self, a):
        for v in self.vacs:
            w = v.full_w * (0.25 + 0.75 * a)
            h = v.full_h * (0.25 + 0.75 * a)
            v.become(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_width=0,
                                      fill_color=TEAL_W, fill_opacity=0.5).move_to(v.get_center()))

    def body(self, with_divlines=True, with_vacs=True, with_hairs=None):
        g = VGroup(self.cap, self.div, self.el, self.mat)
        if with_divlines:
            g.add(self.divlines)
        if with_vacs:
            g.add(self.vacs)
        if with_hairs if with_hairs is not None else self.show_hairs:
            g.add(self.hairs)
        return g

    def zone_center(self, name):
        a, b = {"div": (self.x_div0, self.x_el0), "el": (self.x_el0, self.x_mat0), "mat": (self.x_mat0, self.x_end)}[name]
        return (a + b) / 2, a, b


# ---------------------------------------------------------------------------------------------
# the cell file used in the arithmetic scenes: tip at the left, base fixed at the right
# ---------------------------------------------------------------------------------------------
LONG, SHORT = 2.3, 0.115   # 300 and 15 micrometres at 1 : 20


class CellFile:
    def __init__(self, y=1.45, h=1.8, n_old=2):
        self.y, self.h = y, h
        self.cells = [(ValueTracker(1), LONG) for _ in range(n_old)]

    def add(self, final):
        t = (ValueTracker(0), final)
        self.cells.append(t)
        return t[0]

    def widths(self):
        return [SHORT + (L - SHORT) * v.get_value() for v, L in self.cells]

    def tip_x(self):
        return BASE_X - sum(self.widths())

    def build(self):
        g = VGroup()
        x = BASE_X
        for (v, L), w in zip(self.cells, self.widths()):
            a = v.get_value()
            col = mix(BLUE, ORANGE, a * 2) if a < 0.5 else mix(ORANGE, GREEN, a * 2 - 1)
            g.add(Rectangle(width=w, height=self.h, stroke_color=col, stroke_width=2.5, fill_color=col,
                            fill_opacity=0.2).move_to([x - w / 2, self.y, 0]))
            x -= w
        g.add(RoundedRectangle(corner_radius=0.25, width=0.5, height=self.h * 0.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.25).move_to([x - 0.25, self.y, 0]))
        g.add(Line([BASE_X, self.y - self.h / 2 - 0.15, 0], [BASE_X, self.y + self.h / 2 + 0.15, 0],
                   stroke_color=GREY, stroke_width=7))
        return g

    def mob(self):
        return always_redraw(self.build)


def bar_row(label, value, y, color=YELLOW):
    lab = T(label, 24, GREY).move_to([-6.0, y, 0], aligned_edge=LEFT)
    w = max(value * 0.8333, 0.05)
    bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.85)
    bar.move_to([-3.4 + w / 2, y, 0])
    txt = M(f"{value:g} mm/day", 24, color).next_to(bar, RIGHT, buff=0.2)
    return lab, bar, txt


def footer(text="illustrative numbers, not a measured species"):
    return T(text, 22, GREY).move_to([0, -3.45, 0])


class S00Title(TitleCard):
    LESSON = "Plant body and growth"
    TITLE = "A root grows by cells times length"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        st = Strip(y=0.5)
        note = T("one cell file, schematic, not to scale", 22, GREY).move_to([0, -3.3, 0])
        self.at("adding roots")
        tree = T("A tree keeps adding roots, branches and leaves", 30, TEXT).move_to([0, 2.9, 0])
        self.play(FadeIn(tree, shift=UP * 0.1), run_time=0.7)
        self.at("Take the root")
        self.play(FadeOut(tree), LaggedStart(FadeIn(st.cap), *[FadeIn(r) for r in st.div], *[FadeIn(r) for r in st.el],
                                             *[FadeIn(r) for r in st.mat], lag_ratio=0.12), FadeIn(note), run_time=1.6)
        self.at("It gets longer")
        grow = arr([-1.0, 2.35, 0], [-5.4, 2.35, 0], YELLOW, w=7)
        glab = T("the root gets longer", 26, YELLOW).move_to([-3.2, 2.9, 0])
        self.play(GrowArrow(grow), FadeIn(glab), run_time=0.8)
        self.at("Does it make more cells")
        c1 = chip("more cells?", BLUE, 28).move_to([1.8, 2.75, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.15), run_time=0.5)
        self.at("or do its cells get longer")
        c2 = chip("longer cells?", ORANGE, 28).move_to([4.7, 2.75, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.15), run_time=0.5)
        self.at("under a protective root cap")
        cl = T("root cap", 24, GREY).move_to([st.cap.get_center()[0], -1.3, 0])
        self.play(Indicate(st.cap, color=GREY, scale_factor=1.08), FadeIn(cl), run_time=0.8)
        self.at("three zones")
        braces, nums = VGroup(), VGroup()
        for i, name in enumerate(("div", "el", "mat")):
            cx, a, b = st.zone_center(name)
            br = Line([a + 0.05, -1.0, 0], [b - 0.05, -1.0, 0], color=GREY, stroke_width=4)
            n = T(str(i + 1), 28, GREY, weight=BOLD).move_to([cx, -1.6, 0])
            braces.add(br)
            nums.add(n)
        self.play(FadeOut(cl), LaggedStart(*[GrowFromCenter(b) for b in braces], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.25), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Zones(SpokenScene):
    def construct(self):
        st = Strip(y=0.5)
        for r in st.div:
            r.set_stroke(GREY).set_fill(GREY, 0.1)
        self.add(st.body(with_divlines=False, with_vacs=False))
        st.set_vac(0.0)
        note = T("one cell file, schematic, not to scale", 22, GREY).move_to([0, -3.3, 0])
        self.add(note)
        yb = -1.5

        def zone_label(name, text, color):
            cx, a, b = st.zone_center(name)
            br = Line([a + 0.05, yb, 0], [b - 0.05, yb, 0], color=color, stroke_width=5)
            lab = T(text, 26, color, weight=BOLD, line_spacing=0.8).move_to([cx, -2.3, 0])
            return br, lab

        # division
        self.at("zone of division")
        br, lab = zone_label("div", "zone of\ndivision", BLUE)
        self.play(st.div.animate.set_stroke(BLUE).set_fill(BLUE, 0.14), GrowFromCenter(br), FadeIn(lab), run_time=0.7)
        self.at("small cells divide")
        self.play(LaggedStart(*[Create(l) for l in st.divlines], lag_ratio=0.25), run_time=1.0)
        # elongation
        self.at("zone of elongation")
        br2, lab2 = zone_label("el", "zone of\nelongation", ORANGE)
        self.play(st.el.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.14), GrowFromCenter(br2), FadeIn(lab2), run_time=0.7)
        self.at("stop dividing")
        self.play(Indicate(st.el, color=ORANGE, scale_factor=1.03), run_time=0.7)
        self.at("as water fills their vacuoles")
        vl = T("vacuoles fill with water", 24, TEAL_W).move_to([st.zone_center("el")[0], 2.2, 0])
        self.add(st.vacs)
        self.play(FadeIn(vl), *[v.animate.become(RoundedRectangle(corner_radius=0.12, width=v.full_w, height=v.full_h,
                                                                   stroke_width=0, fill_color=TEAL_W, fill_opacity=0.5
                                                                   ).move_to(v.get_center())) for v in st.vacs],
                  run_time=1.5)
        # maturation
        self.at("zone of maturation")
        br3, lab3 = zone_label("mat", "zone of\nmaturation", GREEN)
        self.play(FadeOut(vl), st.mat.animate.set_stroke(GREEN).set_fill(GREEN, 0.14), GrowFromCenter(br3), FadeIn(lab3), run_time=0.7)
        self.at("final types")
        self.play(Indicate(st.mat, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.at("root hairs")
        hl = T("root hairs on the epidermis", 24, GREEN).move_to([st.zone_center("mat")[0], 3.0, 0])
        self.play(LaggedStart(*[Create(h) for h in st.hairs], lag_ratio=0.05), FadeIn(hl), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rule(SpokenScene):
    def construct(self):
        st = Strip(y=0.5, colored=True, vac=1.0, hairs=True)
        g = st.body()
        g.scale(0.72).move_to([0, -1.75, 0])
        self.add(g)
        # zone centres after the shrink
        s = 0.72
        def zc(name):
            cx = st.zone_center(name)[0]
            return cx * s, g.get_center()[1] + 0.9
        self.at("two parts")
        eq1 = T("root growth rate", 42, YELLOW, weight=BOLD)
        eq1b = T("=", 42, TEXT)
        top = VGroup(eq1, eq1b).arrange(RIGHT, buff=0.35).move_to([0, 2.35, 0])
        self.play(FadeIn(top, shift=UP * 0.1), run_time=0.6)
        self.at("division makes the cells")
        self.play(Indicate(VGroup(st.div, st.divlines), color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("elongation sets")
        self.play(Indicate(st.el, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.at("steady state")
        ss = T("steady state, every cell file alike", 24, GREY).move_to([0, 3.3, 0])
        self.play(FadeIn(ss), run_time=0.5)
        self.at("the rate of new cells per file")
        t1 = T("rate of new cells per file", 36, BLUE).move_to([-2.6, 1.05, 0])
        self.play(Write(t1), run_time=1.1)
        x, y = zc("div")
        a1 = arr(t1.get_bottom() + DOWN * 0.1, [x, y + 0.1, 0], BLUE, w=4)
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("times the final cell length")
        times = T("×", 40, TEXT).move_to([0.55, 1.05, 0])
        t2 = T("final cell length", 36, ORANGE).move_to([3.1, 1.05, 0])
        self.play(FadeIn(times), Write(t2), run_time=1.0)
        x, y = zc("el")
        xe = st.zone_center("el")[2] * s - 0.15
        a2 = arr(t2.get_bottom() + DOWN * 0.1, [xe, y + 0.1, 0], ORANGE, w=4)
        self.play(GrowArrow(a2), run_time=0.5)
        self.at("illustrative")
        f = footer()
        self.play(FadeIn(f), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class _FileScene(SpokenScene):
    def setup_file(self):
        self.cf = CellFile()
        self.fm = self.cf.mob()
        self.add(self.fm)

    def hour_label(self, n):
        return M(f"hour {n}", 26, TEXT).move_to([-5.0, 0.15, 0])


class S04Normal(_FileScene):
    def construct(self):
        self.setup_file()
        cf = self.cf
        f = footer("illustrative, not a measured species; one cell shown, timing not to scale")
        self.add(f)
        self.at("one file of cells")
        lab = T("one cell file", 26, GREY).move_to([-3.0, 3.2, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.at("one new cell per hour")
        rate = T("1 new cell per hour", 28, BLUE).move_to([-3.0, 3.2, 0])
        self.play(FadeIn(rate), FadeOut(lab), run_time=0.5)
        hr = self.hour_label(1)
        # ---- hour 1: the new cell appears tiny, then lengthens -----------------------------------
        x_before = cf.tip_x()
        tr = cf.add(LONG)
        self.play(FadeIn(hr), run_time=0.3)
        self.at("15 micrometers")
        cell_x = BASE_X - sum(cf.widths()[:-1]) - 0.05
        l15 = T("15 µm", 24, BLUE).move_to([cell_x - 0.9, 2.95, 0])
        pt = arr([cell_x - 0.65, 2.75, 0], [cell_x - 0.07, 2.4, 0], BLUE, w=3, tip=0.14)
        self.play(FadeIn(l15), GrowArrow(pt), run_time=0.5)
        self.at("matures at")
        self.play(FadeOut(l15), FadeOut(pt), tr.animate.set_value(1), run_time=1.6)
        x_after = cf.tip_x()
        l300 = T("300 µm", 24, GREEN).move_to([x_after + LONG / 2 + 0.1, 2.75, 0])
        adv = arr([x_before, 0.15, 0], [x_after, 0.15, 0], YELLOW, w=6)
        advl = T("tip moves 300 µm in 1 hour", 24, YELLOW).move_to([(x_before + x_after) / 2, -0.25, 0])
        self.play(FadeIn(l300), GrowArrow(adv), FadeIn(advl), run_time=0.7)
        self.at("One cell per hour times")
        e1 = M("1 cell/h × 300 µm = 300 µm/h", 28, YELLOW).move_to([0, -0.9, 0])
        self.play(FadeOut(l300), Write(e1), run_time=1.0)
        # ---- hours 2 and 3 as a quick time-lapse ------------------------------------------------
        self.at("is 300")
        for n in (2, 3):
            hr2 = self.hour_label(n)
            tr = cf.add(LONG)
            self.play(Transform(hr, hr2), FadeOut(adv), FadeOut(advl), run_time=0.3)
            self.play(tr.animate.set_value(1), run_time=1.0)
        self.at("that is")
        e2 = M("300 µm/h × 24 h = 7,200 µm = 7.2 mm/day", 28, YELLOW).move_to([0, -0.9, 0])
        self.play(ReplacementTransform(e1, e2), FadeOut(hr), run_time=0.8)
        self.at("millimeters per day")
        lab, bar, txt = bar_row("all normal", 7.2, -1.65)
        self.play(FadeIn(lab), GrowFromEdge(bar, LEFT), FadeIn(txt), run_time=1.0)
        self.finish()


class S05Block(_FileScene):
    def construct(self):
        self.setup_file()
        cf = self.cf
        f = footer()
        self.add(f)
        lab, bar, txt = bar_row("all normal", 7.2, -1.65)
        self.add(lab, bar, txt)
        x0 = BASE_X - 2 * LONG
        mk = DashedLine([x0, 0.35, 0], [x0, 2.55, 0], color=GREY, stroke_width=3)
        mkl = T("tip at start", 22, GREY).move_to([x0, 0.05, 0])
        self.add(mk, mkl)
        self.at("block elongation")
        divc = chip("division: unchanged", BLUE, 24).move_to([-3.3, 3.2, 0])
        elc = chip("elongation: blocked", ORANGE, 24).move_to([2.7, 3.2, 0])
        cross = Line(elc.get_left() + RIGHT * 0.1, elc.get_right() - RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(FadeIn(divc), FadeIn(elc), run_time=0.6)
        self.play(Create(cross), elc[0].animate.set_stroke(RED), run_time=0.5)
        self.at("one new cell per hour")
        e = M("1 cell/h × 15 µm = 15 µm/h", 28, YELLOW).move_to([0, -0.9, 0])
        hr = self.hour_label(1)
        self.play(FadeIn(hr), run_time=0.3)
        for n in (1, 2, 3):
            if n > 1:
                self.play(Transform(hr, self.hour_label(n)), run_time=0.25)
            c = (ValueTracker(0), SHORT)
            cf.cells.append(c)
            self.play(c[0].animate.set_value(1), run_time=0.6)
        self.at("the cells stay")
        l15 = T("15 µm", 24, GREEN).move_to([cf.tip_x() - 1.1, 2.75, 0])
        p15 = arr([cf.tip_x() - 0.65, 2.6, 0], [cf.tip_x() + 0.0, 2.1, 0], GREEN, w=3, tip=0.14)
        self.play(FadeIn(l15), GrowArrow(p15), run_time=0.4)
        self.at("One times")
        self.play(Write(e), FadeOut(hr), FadeOut(l15), FadeOut(p15), run_time=1.0)
        self.at("That is")
        e2 = M("15 µm/h × 24 h = 360 µm = 0.36 mm/day", 28, YELLOW).move_to([0, -0.9, 0])
        self.play(ReplacementTransform(e, e2), run_time=0.8)
        self.at("millimeters per day")
        lab2, bar2, txt2 = bar_row("no elongation", 0.36, -2.27)
        self.play(FadeIn(lab2), GrowFromEdge(bar2, LEFT), FadeIn(txt2), run_time=0.8)
        self.at("one twentieth")
        tw = T("1/20 of normal", 24, RED).next_to(txt2, RIGHT, buff=0.3)
        self.play(FadeIn(tw), run_time=0.6)
        self.at("supplies most")
        self.play(Indicate(elc, color=ORANGE, scale_factor=1.12), run_time=1.0)
        self.finish()


class S06Halve(_FileScene):
    def construct(self):
        self.setup_file()
        cf = self.cf
        f = footer()
        self.add(f)
        rows = [bar_row("all normal", 7.2, -1.65), bar_row("no elongation", 0.36, -2.27)]
        for r in rows:
            self.add(*r)
        x0 = BASE_X - 2 * LONG
        mk = DashedLine([x0, 0.35, 0], [x0, 2.55, 0], color=GREY, stroke_width=3)
        mkl = T("tip at start", 22, GREY).move_to([x0, 0.05, 0])
        self.add(mk, mkl)
        self.at("division and keep")
        divc = chip("division: halved", RED, 24).move_to([-3.3, 3.2, 0])
        elc = chip("elongation: normal", ORANGE, 24).move_to([2.7, 3.2, 0])
        self.play(FadeIn(divc), FadeIn(elc), run_time=0.6)
        hr = self.hour_label(1)
        self.at("Half a cell")
        e = M("0.5 cell/h × 300 µm = 150 µm/h", 28, YELLOW).move_to([0, -0.9, 0])
        self.play(FadeIn(hr), Write(e), run_time=0.8)
        for n in (1, 2, 3, 4):
            if n > 1:
                self.play(Transform(hr, self.hour_label(n)), run_time=0.3)
            if n % 2 == 0:
                tr = cf.add(LONG)
                self.play(tr.animate.set_value(1), run_time=1.2)
            else:
                self.wait(0.5)
        self.play(FadeOut(hr), run_time=0.2)
        self.at("that is")
        e2 = M("150 µm/h × 24 h = 3,600 µm = 3.6 mm/day", 28, YELLOW).move_to([0, -0.9, 0])
        self.play(ReplacementTransform(e, e2), run_time=0.8)
        self.at("millimeters per day")
        lab3, bar3, txt3 = bar_row("half division", 3.6, -2.89)
        self.play(FadeIn(lab3), GrowFromEdge(bar3, LEFT), FadeIn(txt3), run_time=0.8)
        self.at("Keep the rule")
        self.play(FadeOut(divc), FadeOut(elc), FadeOut(f), FadeOut(e2), FadeOut(mk), FadeOut(mkl), FadeOut(self.fm), run_time=0.6)
        rule1 = T("root growth rate", 34, YELLOW, weight=BOLD)
        eqs = T("=", 34, TEXT)
        t1 = T("new cells per hour", 34, BLUE)
        tx = T("×", 34, TEXT)
        t2 = T("final cell length", 34, ORANGE)
        rule = VGroup(rule1, eqs, t1, tx, t2).arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
        fit(rule)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "At steady state, growth equals new cells per file times final length."
