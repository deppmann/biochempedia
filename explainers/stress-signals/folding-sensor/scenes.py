"""A sensor inside the folding compartment: IRE1 splices a message and shifts its reading frame.

COLOR MAP (one colour per concept, whole film)
  BLUE   = IRE1, the sensor
  ORANGE = unfolded protein chains
  TEAL   = the XBP1 messenger RNA
  RED    = a cut / the RNA-cutting activity / the removed piece
  GOLD   = the ligase that joins the ends
  YELLOW = the reading frame (brackets)
  PURPLE = the protein made from the message
  GREEN  = the active transcription factor and its new tail
  PINK   = chaperones
  GREY   = membranes, outlines, folded protein, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def membrane(y, x0=-6.3, x1=6.3, h=0.3):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def chain(x, y, color=ORANGE):
    f = ParametricFunction(lambda t: np.array([t, 0.17 * np.sin(t * 9), 0]), t_range=[-0.45, 0.45], color=color,
                           stroke_width=6)
    f.scale(1.5)
    return f.move_to([x, y, 0])


def blob(x, y):
    return Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45).move_to([x, y, 0])


class Ire:
    """IRE1: a body spanning the membrane and two blades at its cytoplasmic end."""
    def __init__(self, x, ymem, body_h=2.4):
        self.body = RoundedRectangle(corner_radius=0.18, width=0.55, height=body_h, stroke_color=BLUE, stroke_width=4,
                                     fill_color=BLUE, fill_opacity=0.35).move_to([x, ymem + 0.2, 0])
        yb = self.body.get_bottom()[1] - 0.05
        self.bl = Line([x, yb, 0], [x - 0.26, yb - 0.5, 0], color=GREY, stroke_width=6)
        self.br = Line([x, yb, 0], [x + 0.26, yb - 0.5, 0], color=GREY, stroke_width=6)
        self.group = VGroup(self.body, self.bl, self.br)

    def on(self):
        return [self.bl.animate.set_color(RED).rotate(0.25, about_point=self.bl.get_start()),
                self.br.animate.set_color(RED).rotate(-0.25, about_point=self.br.get_start())]


class S00Title(TitleCard):
    LESSON = "Stress signals"
    TITLE = "A Cut That Shifts the Frame"


# ---------------------------------------------------------------------------------------------
class S01Backlog(SpokenScene):
    def construct(self):
        ym = 0.0
        mem = membrane(ym)
        er = T("endoplasmic reticulum", 26, GREY).move_to([-4.0, 3.45, 0])
        cy = T("cytoplasm", 26, GREY).move_to([-5.2, -3.1, 0])
        pos = [(-5.3, 2.7), (-3.4, 1.9), (-0.4, 2.8), (2.9, 2.2), (4.8, 2.8), (-5.0, 1.0),
               (5.0, 0.8), (5.1, 1.7), (-2.2, 2.8), (0.8, 2.1), (3.2, 0.8), (-3.4, 0.8)]
        first = [chain(*pos[i]) for i in (0, 3, 4)]
        self.play(FadeIn(mem), FadeIn(er), FadeIn(cy), *[Create(c) for c in first], run_time=0.8)
        self.at("fold inside")
        blobs = [blob(*pos[i]) for i in (0, 3, 4)]
        self.play(*[ReplacementTransform(c, b) for c, b in zip(first, blobs)], run_time=0.9)
        self.at("arrive faster")
        extra = [chain(*pos[i]) for i in (1, 2, 5, 6, 7, 8, 9, 10, 11)]
        self.play(LaggedStart(*[Create(c) for c in extra[:4]], lag_ratio=0.15), run_time=1.0)
        self.at("needs to know")
        self.play(LaggedStart(*[Create(c) for c in extra[4:]], lag_ratio=0.15), run_time=1.0)
        lbl = T("unfolded chains pile up", 26, ORANGE).move_to([3.0, 3.45, 0])
        q = T("how does the cell know?", 30, YELLOW).move_to([0, -1.4, 0])
        self.play(FadeIn(lbl), FadeIn(q), run_time=0.5)
        self.at("three sensors")
        self.play(FadeOut(q), run_time=0.3)
        three = T("three sensors, each spanning the membrane", 28, BLUE).move_to([0, -1.4, 0])
        self.play(FadeIn(three), run_time=0.4)
        self.at("spans the membrane")
        ires = [Ire(-1.8, ym), Ire(1.8, ym)]
        self.play(FadeOut(three), *[FadeIn(i.group) for i in ires], run_time=0.7)
        tag = T("IRE1", 28, BLUE, weight=BOLD).next_to(ires[1].body, RIGHT, buff=0.3)
        self.play(FadeIn(tag), run_time=0.3)
        self.at("molecules cluster")
        self.play(FadeOut(tag), ires[0].group.animate.shift(RIGHT * 1.35), ires[1].group.animate.shift(LEFT * 1.35),
                  run_time=1.2)
        self.at("cutting activity")
        on = T("RNA-cutting activity on", 26, RED).move_to([0, -2.6, 0])
        self.play(*ires[0].on(), *ires[1].on(), FadeIn(on), run_time=0.8)
        self.wait(self.beat(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Splice(SpokenScene):
    def construct(self):
        ym = 2.7
        mem = membrane(ym)
        ires = [Ire(-0.9, ym, 1.0), Ire(0.9, ym, 1.0)]
        for i in ires:
            x = i.body.get_center()[0]
            i.body.move_to([x, ym + 0.3, 0])
            yb = i.body.get_bottom()[1] - 0.05
            i.bl.put_start_and_end_on([x, yb, 0], [x - 0.26, yb - 0.5, 0])
            i.br.put_start_and_end_on([x, yb, 0], [x + 0.26, yb - 0.5, 0])
            i.bl.set_color(RED); i.br.set_color(RED)
        self.play(FadeIn(mem), *[FadeIn(i.group) for i in ires], run_time=0.5)
        yr = 0.6

        def bar(w, x, col=TEAL):
            return RoundedRectangle(corner_radius=0.1, width=w, height=0.7, stroke_color=col, stroke_width=3,
                                    fill_color=col, fill_opacity=0.3).move_to([x, yr, 0])
        left, mid, right = bar(5.0, -3.5), bar(1.8, 0), bar(5.0, 3.5)
        name = T("XBP1 message", 26, TEAL).move_to([-3.5, yr + 0.8, 0])
        self.at("known job")
        self.play(FadeIn(left), FadeIn(mid), FadeIn(right), run_time=0.5)
        cuts = VGroup(Line([-0.9, yr + 0.5, 0], [-0.9, yr - 0.5, 0], color=RED, stroke_width=6),
                      Line([0.9, yr + 0.5, 0], [0.9, yr - 0.5, 0], color=RED, stroke_width=6))
        self.at("cuts a segment")
        self.play(Create(cuts), run_time=0.3)
        self.play(mid.animate.shift(DOWN * 1.6 + RIGHT * 4.5).set_stroke(RED).set_fill(RED, 0.3), FadeOut(cuts),
                  run_time=0.6)
        seg = T("segment removed", 24, RED).next_to(mid, DOWN, buff=0.15)
        self.play(FadeIn(seg), run_time=0.3)
        self.at("in animals")
        self.play(FadeIn(name), run_time=0.4)
        self.at("joins the ends")
        lig = bchip("ligase", GOLD, 26).move_to([0, yr - 1.3, 0])
        self.play(FadeIn(lig), left.animate.shift(RIGHT * 0.9), right.animate.shift(LEFT * 0.9),
                  FadeOut(seg), FadeOut(mid), name.animate.shift(RIGHT * 0.9), run_time=0.7)
        join = Rectangle(width=0.14, height=0.82, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([0, yr, 0])
        self.play(lig.animate.move_to([0, yr - 0.2, 0]).scale(0.4), run_time=0.3)
        self.play(FadeIn(join), FadeOut(lig), run_time=0.25)
        self.at("Only the spliced")
        tf = bchip("active transcription factor", GREEN, 28).move_to([0, -2.1, 0])
        self.play(GrowArrow(arr([0, yr - 0.5, 0], [0, -1.5, 0], GREEN)), FadeIn(tf), run_time=0.7)
        ghost = T("unspliced message: no active factor", 24, GREY).move_to([-3.4, -3.3, 0])
        self.play(FadeIn(ghost), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def squares(n, x0, y, color=TEAL, s=0.62):
    return VGroup(*[Square(side_length=s * 0.88, stroke_color=color, stroke_width=2, fill_color=color,
                           fill_opacity=0.3).move_to([x0 + s * (k + 0.5), y, 0]) for k in range(n)])


def bracket(x_left, k, y, color, s=0.62):
    return Rectangle(width=k * s - 0.03, height=0.85, stroke_color=color, stroke_width=3).move_to(
        [x_left + k * s / 2, y, 0])


class S03Frame(SpokenScene):
    def construct(self):
        s = 0.62
        y = 1.8
        pw = 2.6
        total = 6 * s * 2 + pw + 0.3
        lx = -total / 2
        L = squares(6, lx, y)
        pc_x0 = lx + 6 * s + 0.15
        piece = RoundedRectangle(corner_radius=0.08, width=pw, height=0.7, stroke_color=RED, stroke_width=3,
                                 fill_color=RED, fill_opacity=0.3).move_to([pc_x0 + pw / 2, y, 0])
        rx0 = pc_x0 + pw + 0.15
        R = squares(6, rx0, y)
        name = T("XBP1 message", 26, TEAL).move_to([lx + 1.4, y + 1.0, 0])
        note = T("idealised, not to scale", 22, GREY).move_to([0, -3.3, 0])
        self.at("piece that is removed")
        self.play(FadeIn(L), FadeIn(piece), FadeIn(R), FadeIn(name), FadeIn(note), run_time=0.8)
        self.at("26 nucleotides")
        lab = T("26 nucleotides", 26, RED).next_to(piece, UP, buff=0.35)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("not a multiple of three")
        bl = [bracket(lx + 3 * s * i, 3, y, GREY) for i in range(2)]
        br = [bracket(rx0 + 3 * s * i, 3, y, GREY) for i in range(2)]
        mult = T("26 is not a multiple of 3", 28, RED).move_to([0, y - 1.2, 0])
        self.play(*[Create(b) for b in bl + br], FadeIn(mult), run_time=0.9)
        self.at("reading frame shifts")
        self.play(FadeOut(piece), FadeOut(lab), FadeOut(mult), *[FadeOut(b) for b in br],
                  R.animate.shift(LEFT * (pw + 0.15)), run_time=0.9)
        gx = rx0 - pw - 0.15
        nb = [bracket(gx, 2, y, YELLOW), bracket(gx + 2 * s, 3, y, YELLOW), bracket(gx + 5 * s, 1, y, YELLOW)]
        self.play(*[Create(b) for b in nb], run_time=0.8)
        fs = T("the frame shifts", 28, YELLOW).move_to([gx + 3 * s, y - 1.2, 0])
        self.play(FadeIn(fs), run_time=0.3)
        self.at("gains a new tail")
        yp = -1.1
        p1 = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8, stroke_color=PURPLE, stroke_width=3,
                              fill_color=PURPLE, fill_opacity=0.3).move_to([-3.6, yp, 0])
        pl = T("protein", 26, PURPLE).next_to(p1, UP, buff=0.25)
        tail = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.8, stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.35).next_to(p1, RIGHT, buff=0)
        tl = T("new tail", 28, GREEN, weight=BOLD).next_to(tail, UP, buff=0.25)
        self.play(FadeIn(p1), FadeIn(pl), run_time=0.5)
        self.play(GrowFromEdge(tail, LEFT), FadeIn(tl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Repair(SpokenScene):
    def construct(self):
        er_box = RoundedRectangle(corner_radius=0.5, width=7.6, height=3.9, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.08).move_to([2.4, 1.6, 0])
        er = T("endoplasmic reticulum", 26, GREY).move_to([2.4, 3.2, 0])
        tf = bchip("active factor", GREEN, 28).move_to([-4.3, 1.6, 0])
        chains = [chain(x, y) for x, y in [(0.0, 2.3), (0.0, 0.4), (5.3, 2.3), (5.3, 0.4)]]
        self.play(FadeIn(er_box), FadeIn(er), FadeIn(tf), *[FadeIn(c) for c in chains], run_time=0.6)
        self.at("orders more chaperones")
        chaps = [bchip("chaperone", PINK, 24).move_to(p) for p in [(2.7, 2.4, 0), (2.7, 0.3, 0), (2.7, 1.35, 0)]]
        self.play(GrowArrow(arr([-3.0, 1.6, 0], [-1.3, 1.6, 0], PINK)),
                  LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chaps], lag_ratio=0.3), run_time=1.2)
        self.at("folding capacity rises")
        cap = Rectangle(width=0.6, height=1.4, stroke_color=PINK, stroke_width=3).move_to([-4.3, -0.55, 0])
        fill = Rectangle(width=0.6, height=0.25, stroke_width=0, fill_color=PINK, fill_opacity=0.8)
        fill.move_to(cap.get_bottom() + UP * 0.125)
        capl = T("folding capacity", 24, PINK).next_to(cap, DOWN, buff=0.15)
        self.play(FadeIn(cap), FadeIn(fill), FadeIn(capl), run_time=0.4)
        full = Rectangle(width=0.6, height=1.35, stroke_width=0, fill_color=PINK, fill_opacity=0.8)
        full.move_to(cap.get_bottom() + UP * 0.675)
        self.play(Transform(fill, full), run_time=0.9)
        self.at("repair branch")
        self.wait(0.2)
        self.at("Keep this order")
        steps = [("IRE1 clusters", BLUE), ("message cut and joined", TEAL), ("frame shifts", YELLOW),
                 ("active factor", GREEN)]
        chips = [bchip(t, c, 24) for t, c in steps]
        row = VGroup(*chips).arrange(RIGHT, buff=0.6).move_to([0, -3.1, 0])
        row = fit(row, 12.4, 1.2)
        arrows = [arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, 4, 0.16) for i in range(3)]
        for i, ph in enumerate(["clusters", "cut and joined", "frame shifts", "active factor appears"]):
            self.at(ph)
            anims = [FadeIn(chips[i], shift=RIGHT * 0.2)]
            if i > 0:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.35)
        self.finish()


class S05End(EndCard):
    LINE = "Only the spliced message yields an active factor."
