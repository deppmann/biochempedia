"""Remove One Letter: chapter 2 of "Head to Tail: Hox Genes, Retinoic Acid and Rhombomeres"
(Biochemistrypedia chaptered film).

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  ORANGE = retinoic acid (the drug, the drops, the gradient, the dose)   [chapter 3]
  GREEN  = made / switched on (Raldh2, a gene that is on, the right dose) [chapter 3]
  RED    = destroyed / removed / failed (Cyp26; here: a gene knocked out, a nucleus that fails)
  BLUE   = the retinoic acid receptors (RAR, RXR)                        [chapter 3]
  PURPLE = Hox genes and the Hox code (four shades = gene groups 1 to 4, light to dark)
  GOLD   = the short DNA stretch the receptor pair binds                 [chapter 3]
  TEAL   = trigeminal identity (jaw, chewing)
  YELLOW = facial identity (face, facial expression)
  GREY   = segment outlines, DNA, labels, segment genes such as Krox20
  TEXT (near white) = neutral cells whose identity is not yet shown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
HOX = ["#DCC8F4", "#C39EE6", "#A573CF", "#8650B8"]   # Hox groups 1..4, 3' to 5'

# --- strips. LEFT strip (scenes 3, 8, 9): seven rhombomeres, front (r1) at the left, back (r7) at the right,
#     pushed left so the right third holds the face / code panel.
LX = [-5.25 + 1.22 * i for i in range(7)]
LW = 1.12
LSY, LSH = 0.35, 5.0
LCX = (LX[0] + LX[6]) / 2
# CENTRED strip (scene 12): full width
CX = [-4.35 + 1.45 * i for i in range(7)]
CW = 1.35


def bchip(text, color=BLUE, size=26, pad=0.22, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def header(text, color=TEXT, size=30, x=0.0, y=3.4):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def xmark(center, size=0.34, color=RED, w=6):
    h = size / 2
    return VGroup(Line([-h, h, 0], [h, -h, 0], color=color, stroke_width=w),
                  Line([-h, -h, 0], [h, h, 0], color=color, stroke_width=w)).move_to(center)


def kox(chp, size=0.5, gap=0.35):
    """A red X BESIDE a chip (never on top of its letters)."""
    return xmark(chp.get_right() + RIGHT * (gap + size / 2), size, RED, 6)


def seg_strip(xs, y, h, w, lab=24):
    bs = VGroup(*[RoundedRectangle(corner_radius=0.26, width=w, height=h, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0]) for x in xs])
    labs = VGroup(*[T(f"r{i + 1}", lab, GREY).move_to([x, y + h / 2 - 0.4, 0]) for i, x in enumerate(xs)])
    return bs, labs


def lstrip():
    return seg_strip(LX, LSY, LSH, LW)


def front_back():
    y = LSY + LSH / 2 + 0.3
    return VGroup(T("front", 24, GREY).move_to([LX[0], y, 0]), T("back", 24, GREY).move_to([LX[6], y, 0]))


def cell(color, x, y, r=0.24, op=0.95):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def face(x, y, color=YELLOW, r=0.75):
    k = r / 0.62
    return VGroup(Circle(r, color=color, stroke_width=4),
                  Dot([-0.22 * k, 0.16 * k, 0], radius=0.06, color=color),
                  Dot([0.22 * k, 0.16 * k, 0], radius=0.06, color=color),
                  Arc(radius=0.3 * k, start_angle=PI * 1.2, angle=PI * 0.6, color=color, stroke_width=4)
                  .shift(DOWN * 0.1 * k)).move_to([x, y, 0])


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=2.5).set_opacity(0.8)


# --- the hindbrain Hox code grid (simplified table from the lesson): rows are genes, columns are r1..r7
ROWS = [("Hoxa2", 1, {1, 2, 3, 4, 5, 6}), ("Hoxb2", 1, {2, 3, 4, 5, 6}), ("Hoxb1", 0, {3}),
        ("Hoxb3", 2, {4, 5, 6}), ("Hoxb4", 3, {6})]


class Grid:
    def __init__(self, cols, xs, ys, r, head_y, top, bot, label_right, colw, rows=ROWS):
        self.frames = VGroup(*[RoundedRectangle(corner_radius=0.25, width=colw, height=top - bot, stroke_color=GREY,
                                                stroke_width=2.5, fill_color=GREY, fill_opacity=0.08)
                               .move_to([x, (top + bot) / 2, 0]) for x in xs])
        self.heads = VGroup(*[T(f"r{c + 1}", 26, GREY).move_to([x, head_y, 0]) for c, x in zip(cols, xs)])
        self.labels, self.dots, self.y, self.x = {}, {}, {}, {}
        for (name, g, present), y in zip(rows, ys):
            self.y[name] = y
            self.labels[name] = T(name, 26, PURPLE).move_to([label_right, y, 0], aligned_edge=RIGHT)
            for c, x in zip(cols, xs):
                self.x[c] = x
                if c in present:
                    strong = name == "Hoxb1"
                    self.dots[(name, c)] = Circle(radius=r * (1.25 if strong else 1), stroke_color=TEXT if strong else HOX[g],
                                                  stroke_width=4 if strong else 0, fill_color=HOX[g],
                                                  fill_opacity=0.95).move_to([x, y, 0])
        self.label_group = VGroup(*self.labels.values())

    def dot_group(self):
        return VGroup(*self.dots.values())


def grid7():
    # moved right so the row labels clear the r1 column
    return Grid(range(7), [-3.55 + 1.3 * i for i in range(7)], [1.55, 0.6, -0.35, -1.3, -2.25], 0.3,
                2.55, 2.95, -2.75, -4.35, 1.15)


def grid2():
    return Grid([2, 3], [-1.3, 2.0], [1.6, 0.35, -0.9], 0.45, 2.5, 2.95, -2.65, -3.0, 2.8, rows=ROWS[:3])


# ============================================================================================
class S00Title(TitleCard):
    LESSON = "Head to Tail: Hox Genes, Retinoic Acid and Rhombomeres"
    TITLE = "Remove One Letter"


# --------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        g = grid7()
        self.play(FadeIn(g.frames), FadeIn(g.heads), FadeIn(g.label_group), run_time=0.5)
        self.at("hox code")
        self.play(FadeIn(header("The Hox code", PURPLE, 32)),
                  LaggedStart(*[GrowFromCenter(d) for d in g.dot_group()], lag_ratio=0.08), run_time=0.9)
        self.at("identity")
        self.play(Indicate(g.frames[3], color=PURPLE, scale_factor=1.03), g.frames[3].animate.set_stroke(PURPLE, 4), run_time=0.7)
        self.at("one gene")
        hl = RoundedRectangle(corner_radius=0.2, width=10.9, height=0.8, stroke_color=PURPLE, stroke_width=3.5
                              ).move_to([-0.55, g.y["Hoxb1"], 0])
        self.play(Create(hl), run_time=0.5)
        self.at("taken away")
        d = g.dots[("Hoxb1", 3)]
        # the dot visibly blinks off ...
        for _ in range(2):
            self.play(d.animate.set_fill(HOX[0], 0.05).set_stroke(TEXT, 1), run_time=0.15)
            self.play(d.animate.set_fill(HOX[0], 0.95).set_stroke(TEXT, 4), run_time=0.15)
        self.play(d.animate.set_fill(HOX[0], 0.05).set_stroke(TEXT, 1), run_time=0.15)
        # ... and stays off: an empty red dashed ring marks where it was
        ring = DashedVMobject(Circle(0.38, color=RED, stroke_width=4), num_dashes=14).move_to(d.get_center())
        self.play(FadeOut(d), Create(ring), g.labels["Hoxb1"].animate.set_color(RED), run_time=0.4)
        self.finish()


# --------------------------------------------------------------------------------------------
def mouse(scale=1.0):
    SOLID = "#1a1e27"
    body = Ellipse(width=3.2, height=2.0, color=GREY, stroke_width=4, fill_color=SOLID, fill_opacity=1).move_to([-3.4, 0, 0])
    head = Ellipse(width=1.5, height=1.2, color=GREY, stroke_width=4, fill_color=SOLID, fill_opacity=1).move_to([-5.2, 0.15, 0])
    ears = VGroup(Circle(0.34, color=GREY, stroke_width=4, fill_color=SOLID, fill_opacity=1).move_to([-5.0, 0.85, 0]),
                  Circle(0.34, color=GREY, stroke_width=4, fill_color=SOLID, fill_opacity=1).move_to([-4.4, 0.8, 0]))
    eye = Dot([-5.5, 0.3, 0], radius=0.07, color=TEXT)
    nose = Dot([-5.95, 0.1, 0], radius=0.09, color=GREY)
    tail = VMobject(stroke_color=GREY, stroke_width=4)
    tail.set_points_smoothly([np.array(p) for p in ([-1.8, -0.2, 0], [-1.2, -0.7, 0], [-0.8, -0.1, 0], [-0.5, 0.5, 0])])
    return VGroup(tail, ears, body, head, eye, nose).scale(scale)


class S02Ko(SpokenScene):
    def construct(self):
        m = mouse(0.92).move_to([-3.95, 0.15, 0])
        self.play(FadeIn(m), run_time=0.35)
        self.at("conventional")
        self.play(FadeIn(header("conventional knockout", TEXT, 36)), run_time=0.5)
        px = 3.85
        panel = RoundedRectangle(corner_radius=0.25, width=5.7, height=5.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.06).move_to([px, -0.2, 0])
        cells, bars, crosses = VGroup(), VGroup(), []
        for yy in (1.55, -0.2, -1.95):
            for xx in (px - 1.75, px, px + 1.75):
                cells.add(Circle(0.66, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([xx, yy, 0]))
                bars.add(RoundedRectangle(corner_radius=0.06, width=0.8, height=0.22, stroke_width=0,
                                          fill_color=PURPLE, fill_opacity=0.95).move_to([xx, yy, 0]))
                crosses.append(xmark([xx, yy, 0], 0.55, RED, 7))
        lines = VGroup(DashedLine([-1.7, 0.7, 0], [px - 2.85, 2.3, 0], color=GREY),
                       DashedLine([-1.7, -0.5, 0], [px - 2.85, -2.7, 0], color=GREY))
        self.at("one gene")
        gl = T("gene", 28, PURPLE).move_to([px - 1.75, -3.45, 0])
        gl_line = leader([px - 1.75, -3.2, 0], [px - 1.75, -2.55, 0], PURPLE)
        self.play(Create(lines), FadeIn(panel), FadeIn(cells), FadeIn(bars), FadeIn(gl), Create(gl_line), run_time=0.7)
        self.at("disrupted")
        self.play(Create(crosses[0]), run_time=0.25)
        self.at("every cell", lead=0.3)
        self.play(LaggedStart(*[Create(c) for c in crosses[1:]], lag_ratio=0.06), run_time=0.45)
        self.finish()


# --------------------------------------------------------------------------------------------
NO = [(-0.28, 1.5), (0.28, 0.8), (-0.28, 0.1), (0.28, -0.6), (0.0, -1.3)]   # neurons in r4 (offsets from segment centre)


def r4_neurons(color):
    return VGroup(*[cell(color, LX[3] + dx, LSY + dy) for dx, dy in NO])


class S03Normal(SpokenScene):
    def construct(self):
        bs, labs = lstrip()
        fb = front_back()
        self.play(FadeIn(bs), FadeIn(labs), FadeIn(fb), run_time=0.3)
        self.at("normal mouse")
        self.play(FadeIn(header("Normal mouse", TEXT, 32, x=LCX)), run_time=0.4)
        neurons = r4_neurons(YELLOW)
        lab = T("facial motor neurons", 24, YELLOW).move_to([LX[3], -2.55, 0])
        self.at("facial motor neurons")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("born in")
        self.play(bs[3].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.14),
                  LaggedStart(*[GrowFromCenter(n) for n in neurons], lag_ratio=0.12), run_time=0.9)
        self.at("migrate back")
        arrow = Arrow([LX[3] + 0.7, LSY - 1.75, 0], [LX[5] - 0.55, LSY - 1.75, 0], color=YELLOW, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.2)
        self.play(FadeOut(lab), FadeIn(arrow),
                  bs[3].animate.set_stroke(GREY, 3).set_fill(GREY, 0.12),            # the highlight leaves with the cells
                  LaggedStart(*[n.animate.move_to([LX[5] + dx * 0.6, LSY + dy * 0.75 - 0.1, 0]) for n, (dx, dy) in zip(neurons, NO)],
                              lag_ratio=0.12), run_time=1.7)
        self.at("form the")
        ell = Ellipse(width=1.0, height=2.7, color=YELLOW, stroke_width=4).move_to([LX[5], LSY - 0.02, 0])
        self.play(Create(ell), FadeOut(arrow), run_time=0.5)
        nlab = T("facial motor nucleus", 24, YELLOW).move_to([LX[5] - 0.3, -2.55, 0], aligned_edge=RIGHT)
        nerve = VMobject(stroke_color=YELLOW, stroke_width=5)
        nerve.set_points_as_corners([[LX[5], LSY - 1.4, 0], [LX[5], -3.1, 0], [4.55, -3.1, 0]])
        fc = face(5.3, -3.1, r=0.65)
        nv = T("nerve VII", 24, YELLOW).move_to([LX[5] + 0.3, -2.6, 0], aligned_edge=LEFT)
        self.at("facial motor nucleus")
        self.play(FadeIn(nlab), bs[5].animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.1), run_time=0.4)
        self.play(Create(nerve), FadeIn(nv), run_time=0.7)
        self.play(FadeIn(fc), run_time=0.3)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Code(SpokenScene):
    def construct(self):
        g = grid2()
        note = T("simplified table", 26, GREY).move_to([-4.9, -3.3, 0])
        self.play(FadeIn(g.frames), FadeIn(g.heads), FadeIn(g.label_group), FadeIn(note), run_time=0.5)
        self.at("hox", nth=0)
        shared = [g.dots[(n, c)] for n in ("Hoxa2", "Hoxb2") for c in (2, 3)]
        glows = VGroup(*[Circle(radius=0.58, stroke_width=0, fill_color=d.get_fill_color(), fill_opacity=0.28).move_to(d.get_center())
                         for d in shared])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in shared], lag_ratio=0.12), FadeIn(glows), run_time=0.7)
        self.at("hox", nth=1)
        ring = DashedVMobject(Circle(0.5, color=GREY, stroke_width=3), num_dashes=12).move_to([g.x[2], g.y["Hoxb1"], 0])
        self.play(GrowFromCenter(g.dots[("Hoxb1", 3)]), FadeIn(ring), g.labels["Hoxb1"].animate.set_color(TEXT), run_time=0.4)
        self.play(Indicate(g.dots[("Hoxb1", 3)], color=TEXT, scale_factor=1.3), run_time=0.4)
        self.at("clearest difference")
        by = -2.9
        br = VGroup(Line([g.x[2], by + 0.15, 0], [g.x[2], by, 0], color=TEXT, stroke_width=3.5),
                    Line([g.x[2], by, 0], [g.x[3], by, 0], color=TEXT, stroke_width=3.5),
                    Line([g.x[3], by, 0], [g.x[3], by + 0.15, 0], color=TEXT, stroke_width=3.5))
        bl = T("the difference", 26, TEXT).move_to([(g.x[2] + g.x[3]) / 2, by - 0.4, 0])
        self.play(Create(br), FadeIn(bl), run_time=0.6)
        self.at("r4")
        self.play(g.frames[1].animate.set_stroke(PURPLE, 5), run_time=0.4)
        self.at("r3")
        self.play(g.frames[0].animate.set_stroke(PURPLE, 5), run_time=0.4)
        self.finish()


# --------------------------------------------------------------------------------------------
PRX = 3.6
PBY = -0.2


def predict_box(x, with_q=True):
    b = RoundedRectangle(corner_radius=0.28, width=3.4, height=3.6, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.12)
    parts = [b, T("r4", 30, GREY).move_to(b.get_top() + DOWN * 0.45)]
    if with_q:
        parts.append(T("?", 90, TEXT).move_to(b.get_center() + DOWN * 0.2))
    return VGroup(*parts).move_to([x, PBY, 0])


def predict_top():
    chp = bchip("Hoxb1", PURPLE, 30).move_to([-0.4, 2.55, 0])
    return chp, kox(chp, 0.6)


LBL_L = lambda: T("disappears?", 28, TEXT).move_to([-PRX, -2.7, 0])
LBL_R = lambda: T("stays, becomes\nsomething else?", 28, TEXT).move_to([PRX, -2.8, 0])


class S05Predict(SpokenScene):
    def construct(self):
        hdr = header("Predict", TEXT, 40)
        r4 = predict_box(0, with_q=False)
        self.play(FadeIn(hdr), FadeIn(r4), run_time=0.6)
        chp, x = predict_top()
        self.at("knockout")
        self.play(FadeIn(chp), run_time=0.4)
        self.play(Create(x), run_time=0.4)
        self.at("does r4 disappear")
        q = T("?", 90, TEXT).move_to([-PRX, PBY - 0.2, 0])
        self.play(r4.animate.move_to([-PRX, PBY, 0]), run_time=0.6)
        self.play(FadeIn(q), run_time=0.2)
        ll = LBL_L()
        self.at("disappear")
        self.play(FadeIn(ll), run_time=0.4)
        R = predict_box(PRX)
        Lg = VGroup(r4[0], r4[1], q)
        self.at("or does it stay")
        self.play(TransformFromCopy(Lg, R), FadeIn(LBL_R()), run_time=0.8)
        self.at("something else")
        self.play(Indicate(R, color=TEXT, scale_factor=1.04), Indicate(Lg, color=TEXT, scale_factor=1.04), run_time=0.7)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        chp, x = predict_top()
        L, R = predict_box(-PRX), predict_box(PRX)
        hdr = header("Pause. Decide.", TEXT, 40)
        self.add(hdr, chp, x, L, R, LBL_L(), LBL_R())
        num = T("5", 72, GREY).move_to([0, PBY, 0]).set_opacity(0.8)
        self.add(num)
        for k in (5, 4, 3, 2, 1):
            new = T(str(k), 72, GREY).move_to([0, PBY, 0]).set_opacity(0.8)
            self.play(Transform(num, new), Indicate(L, color=GREY, scale_factor=1.03), Indicate(R, color=GREY, scale_factor=1.03),
                      run_time=0.95)
            self.wait(0.05)
        self.finish()


# --------------------------------------------------------------------------------------------
class S07Reveal(SpokenScene):
    def construct(self):
        year = T("1996", 96, GOLD, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(year, shift=UP * 0.2), run_time=0.6)
        self.at("two groups")
        cards = []
        for x in (-3.4, 3.4):
            c = RoundedRectangle(corner_radius=0.25, width=6.2, height=4.3, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.08).move_to([x, -0.35, 0])
            ch = bchip("Hoxb1", PURPLE, 34).move_to([x - 0.4, 1.3, 0])
            mi = mouse(0.42).move_to([x, 0.2, 0])
            kt = T("knockout mouse, 1996", 28, TEXT).move_to([x, -0.75, 0])
            cards.append(VGroup(c, ch, kox(ch, 0.55), mi, kt))
        self.play(year.animate.scale(0.45).move_to([0, 3.3, 0]),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.0)
        self.at("one was led")
        self.play(FadeIn(T("Studer and Krumlauf", 32, TEXT).move_to([-3.4, -1.7, 0]), shift=UP * 0.1), run_time=0.5)
        self.at("the other")
        self.play(FadeIn(T("Goddard and Capecchi", 32, TEXT).move_to([3.4, -1.7, 0]), shift=UP * 0.1), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------------------------
PROG_Y = [LSY + 1.3, LSY + 0.1, LSY - 1.1]
PX0, PX1 = LX[3] - 0.28, LX[3] + 0.28


def s08_strip():
    bs, labs = lstrip()
    bs[3].set_stroke(TEXT, 6)
    return bs, labs


class S08Stays(SpokenScene):
    def construct(self):
        bs, labs = s08_strip()
        self.play(FadeIn(header("Hoxb1 knockout mouse", TEXT, 32, x=LCX)), FadeIn(bs), FadeIn(labs), FadeIn(front_back()), run_time=0.4)
        prog = VGroup(*[Circle(0.24, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([LX[3], y, 0]) for y in PROG_Y])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in prog], lag_ratio=0.15), run_time=0.4)
        self.at("still there")
        self.play(Indicate(bs[3], color=TEXT, scale_factor=1.04), Indicate(labs[3], color=TEXT, scale_factor=1.25), run_time=0.7)
        lab = T("progenitors", 24, TEXT).move_to([LX[3] - 1.15, -2.65, 0])
        ld = leader([LX[3] - 0.85, -2.45, 0], [PX0, PROG_Y[2] - 0.32, 0])
        self.at("progenitor")
        self.play(FadeIn(lab), Create(ld), run_time=0.6)
        new = VGroup(*[Circle(0.24, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([PX1, y, 0]) for y in PROG_Y])
        self.at("still divided")
        self.play(*[p.animate.move_to([PX0, p.get_center()[1], 0]) for p in prog],
                  *[TransformFromCopy(p, n) for p, n in zip(prog, new)], run_time=1.0)
        lab2 = T("motor neurons", 24, TEXT).move_to([LX[3] + 1.3, -2.65, 0])
        ld2 = leader([LX[3] + 0.95, -2.45, 0], [PX1, PROG_Y[2] - 0.32, 0])
        self.at("made motor neurons")
        self.play(*[c.animate.set_fill(TEXT, 0.95) for c in new], FadeIn(lab2), Create(ld2), run_time=0.8)
        self.finish()


def s09_cells():
    prog = VGroup(*[Circle(0.24, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([PX0, y, 0]) for y in PROG_Y])
    new = VGroup(*[cell(TEXT, PX1, y) for y in PROG_Y])
    return prog, new


class S09Identity(SpokenScene):
    def construct(self):
        bs, labs = s08_strip()
        prog, new = s09_cells()
        self.add(header("Hoxb1 knockout mouse", TEXT, 32, x=LCX), bs, labs, front_back(), prog, new)
        # the Hox code of r4, labelled gene by gene (right panel)
        ptitle = T("Hox code of r4", 26, PURPLE).move_to([4.85, 2.4, 0])
        chips = [bchip(n, PURPLE, 26).move_to([4.5, y, 0]) for n, y in (("Hoxa2", 1.5), ("Hoxb2", 0.6), ("Hoxb1", -0.3))]
        self.at("r4")
        self.play(FadeIn(ptitle), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.1), run_time=0.5)
        self.at("lost parts")
        self.play(Create(kox(chips[2], 0.45, 0.3)), chips[2].animate.set_opacity(0.35), run_time=0.6)
        mlab = T("motor neurons", 24, TEXT).move_to([LX[3] + 0.75, -2.6, 0])
        self.at("its motor neurons")
        self.play(Indicate(new, color=TEXT, scale_factor=1.12), FadeIn(mlab), run_time=0.7)
        tn = VGroup(*[cell(TEAL, LX[i] + dx, LSY + dy) for i in (1, 2) for dx, dy in [(-0.25, 1.2), (0.25, 0.1), (-0.1, -1.0)]])
        brk = VGroup(Line([LX[1], -2.3, 0], [LX[1], -2.5, 0], color=TEAL, stroke_width=3.5),
                     Line([LX[1], -2.5, 0], [LX[2], -2.5, 0], color=TEAL, stroke_width=3.5),
                     Line([LX[2], -2.5, 0], [LX[2], -2.3, 0], color=TEAL, stroke_width=3.5))
        tl = T("trigeminal neurons", 24, TEAL).move_to([(LX[1] + LX[2]) / 2 - 0.3, -3.15, 0])
        self.at("trigeminal")
        self.play(bs[1].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.14), bs[2].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.14),
                  LaggedStart(*[GrowFromCenter(n) for n in tn], lag_ratio=0.1), Create(brk), FadeIn(tl), run_time=1.0)
        self.at("of r2")
        self.play(*[c.animate.set_color(TEAL).set_fill(TEAL, 0.95) for c in new],
                  mlab.animate.set_color(TEAL), bs[3].animate.set_fill(TEAL, 0.14), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
S10CX = (-3.4, 3.4)
S10Y, S10H = 0.2, 4.7
S10N = [(-0.3, 1.2), (0.3, 0.5), (-0.3, -0.2), (0.3, -0.9)]
S10DEST = [(0.5, 1.4), (0.55, 0.5), (-0.3, -0.6), (0.1, -1.6)]   # stalled in r5 near the border, one straying low


def s10_boxes(cx):
    xs = [cx - 1.75, cx, cx + 1.75]
    bs = VGroup(*[RoundedRectangle(corner_radius=0.26, width=1.55, height=S10H, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12).move_to([x, S10Y, 0]) for x in xs])
    labs = VGroup(*[T(n, 24, GREY).move_to([x, S10Y + S10H / 2 - 0.4, 0]) for n, x in zip(("r4", "r5", "r6"), xs)])
    bs[0].set_stroke(TEXT, 5)
    return bs, labs, xs


def s10_cells(cx, color=TEAL):
    xs = [cx - 1.75, cx, cx + 1.75]
    return VGroup(*[cell(color, xs[0] + dx, S10Y + dy, 0.22) for dx, dy in S10N])


def s10_ellipse(cx):
    return DashedVMobject(Ellipse(width=1.0, height=2.6, color=YELLOW, stroke_width=4), num_dashes=24).move_to([cx + 1.75, S10Y, 0])


def s10_nlab(cx):
    return T("facial motor nucleus", 24, YELLOW).move_to([cx + 1.75, -3.0, 0])


def s10_stall(cx):
    return DashedLine([cx + 0.875, S10Y - 2.0, 0], [cx + 0.875, S10Y + 2.0, 0], color=RED, stroke_width=5, dash_length=0.18).set_opacity(0.75)


class S10Fail(SpokenScene):
    def construct(self):
        cL, cR = S10CX
        bL, lL, xL = s10_boxes(cL)
        bR, lR, xR = s10_boxes(cR)
        self.at("both")
        ttl = T("fail to form", 30, TEXT, weight=BOLD).move_to([cL, 2.92, 0])
        ttr = T("fail to migrate normally", 30, TEXT, weight=BOLD).move_to([cR, 2.92, 0])
        self.play(FadeIn(header("Both knockouts", TEXT, 32, y=3.58)), FadeIn(bL), FadeIn(lL), FadeIn(bR), FadeIn(lR),
                  FadeIn(ttl), FadeIn(ttr), run_time=0.6)
        nL, nR = s10_cells(cL), s10_cells(cR)
        tagL = T("r4 neurons", 24, TEAL).move_to([xL[0], -2.5, 0])
        tagR = T("r4 neurons", 24, TEAL).move_to([xR[0], -2.5, 0])
        self.at("facial motor neurons")
        self.play(*[LaggedStart(*[GrowFromCenter(c) for c in g], lag_ratio=0.1) for g in (nL, nR)], FadeIn(tagL), FadeIn(tagR), run_time=0.8)
        self.at("failed to form")
        ghosts = VGroup(*[DashedVMobject(Circle(0.22, color=GREY, stroke_width=2.5), num_dashes=10).move_to(c.get_center()) for c in nL])
        tagL2 = T("none made", 24, GREY).move_to([xL[0], -2.5, 0])
        self.play(Indicate(ttl, color=RED, scale_factor=1.08), FadeOut(nL), FadeIn(ghosts), ReplacementTransform(tagL, tagL2), run_time=0.9)
        self.at("to migrate")
        self.play(Indicate(ttr, color=RED, scale_factor=1.08), LaggedStart(*[c.animate.move_to([cR + dx, S10Y + dy, 0]) for c, (dx, dy) in zip(nR, S10DEST)],
                                           lag_ratio=0.12), run_time=1.5)
        tagR2 = T("stalled and straying", 24, TEAL).move_to([cR + 0.2, -2.5, 0])
        self.play(Create(s10_stall(cR)), ReplacementTransform(tagR, tagR2), run_time=0.5)
        eL, eR = s10_ellipse(cL), s10_ellipse(cR)
        self.at("no normal")
        self.play(Create(eL), Create(eR), run_time=0.4)
        self.at("facial motor nucleus")
        self.play(FadeIn(s10_nlab(cL)), FadeIn(s10_nlab(cR)), run_time=0.5)
        self.at("formed")
        self.play(Create(xmark(eL.get_center(), 0.7, RED, 7)), Create(xmark(eR.get_center(), 0.7, RED, 7)), run_time=0.5)
        self.finish()


class S11Beat(NarratedScene):
    def construct(self):
        cL, cR = S10CX
        bL, lL, xL = s10_boxes(cL)
        bR, lR, xR = s10_boxes(cR)
        nR = s10_cells(cR)
        for c, (dx, dy) in zip(nR, S10DEST):
            c.move_to([cR + dx, S10Y + dy, 0])
        ghosts = VGroup(*[DashedVMobject(Circle(0.22, color=GREY, stroke_width=2.5), num_dashes=10).move_to(
            [xL[0] + dx, S10Y + dy, 0]) for dx, dy in S10N])
        eL, eR = s10_ellipse(cL), s10_ellipse(cR)
        self.add(header("Both knockouts", TEXT, 32, y=3.58), bL, lL, bR, lR, nR, ghosts, s10_stall(cR), eL, eR,
                 T("fail to form", 30, TEXT, weight=BOLD).move_to([cL, 2.92, 0]),
                 T("fail to migrate normally", 30, TEXT, weight=BOLD).move_to([cR, 2.92, 0]),
                 T("none made", 24, GREY).move_to([xL[0], -2.5, 0]), T("stalled and straying", 24, TEAL).move_to([cR + 0.2, -2.5, 0]),
                 s10_nlab(cL), s10_nlab(cR),
                 xmark(eL.get_center(), 0.7, RED, 7), xmark(eR.get_center(), 0.7, RED, 7))
        self.wait(1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S12Krox(SpokenScene):
    def construct(self):
        y0, h0 = 0.3, 5.0
        bs, labs = seg_strip(CX, y0, h0, CW)
        for i in (2, 4):                                # the segments that carry the gene
            bs[i].set_fill(GREY, 0.28)
        self.play(FadeIn(bs), FadeIn(labs), run_time=0.5)
        chips = VGroup(*[bchip("Krox20", GREY, 26, pad=0.14).move_to([CX[i] - 0.3, -2.8, 0]) for i in (2, 4)])
        self.at("different gene")
        self.play(FadeIn(chips), run_time=0.5)
        self.at("without it")
        crosses = VGroup(*[kox(c, 0.5, 0.25) for c in chips])
        hdr = header("Krox20 knockout mouse", TEXT, 32, y=3.45)
        self.play(Create(crosses), FadeIn(hdr), run_time=0.7)
        self.at("r3 and r5")
        self.play(Indicate(bs[2], color=TEXT, scale_factor=1.06), Indicate(bs[4], color=TEXT, scale_factor=1.06), run_time=0.8)
        self.at("do not persist")
        self.play(*[bs[i].animate.set_stroke(GREY, 1).set_fill(GREY, 0.0) for i in (2, 4)],
                  FadeOut(labs[2]), FadeOut(labs[4]), FadeOut(chips), FadeOut(crosses),
                  run_time=1.2)
        # lineage-marked survivors stay in the r3 / r5 slots first
        starts = [(CX[2] - 0.25, y0 + 0.9), (CX[2] + 0.25, y0 - 0.8), (CX[4] - 0.25, y0 + 0.9), (CX[4] + 0.25, y0 - 0.8)]
        cells = VGroup(*[cell(TEXT, x, y) for x, y in starts])
        cl = T("cells from r3 and r5", 26, TEXT).move_to([0, -2.8, 0])
        self.at("some of their cells")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.12), FadeIn(cl), run_time=0.9)
        dest = [(CX[1] + 0.1, y0 + 0.6), (CX[3] - 0.25, y0 - 0.7), (CX[3] + 0.25, y0 + 0.8), (CX[5] - 0.1, y0 - 0.3)]
        cl2 = T("they take on the neighbours' character", 26, TEXT).move_to([0, -2.8, 0])
        self.at("mix with")
        self.play(*[c.animate.move_to([x, y, 0]) for c, (x, y) in zip(cells, dest)], run_time=1.3)
        self.at("take on their character")
        cols = [PURPLE] * 4                              # one colour: they carry the neighbours' Hox identity
        self.play(*[c.animate.set_color(col).set_fill(col, 0.95) for c, col in zip(cells, cols)], ReplacementTransform(cl, cl2), run_time=0.8)
        # kreisler: a new row replaces the Krox20 row (its own title)
        bk, lk = seg_strip(CX, y0, h0, CW)
        hk = header("kreisler (MafB) mutant", TEXT, 32, y=3.45)
        self.at("mutants", lead=0.55)
        self.play(FadeOut(VGroup(bs, labs, cells, cl2)), FadeOut(hdr), FadeIn(bk), FadeIn(lk), FadeIn(hk), run_time=0.5)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.26, width=CW, height=h0, color=RED, stroke_width=3), num_dashes=40
                               ).move_to([CX[4], y0, 0])
        ml = T("r5 missing", 26, RED).move_to([CX[4], -2.8, 0])
        self.at("r5 is missing", lead=0.75)
        self.play(FadeOut(bk[4]), FadeOut(lk[4]), FadeIn(ghost), Create(xmark([CX[4], y0, 0], 1.1, RED, 9)), FadeIn(ml), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------------------------
MX = [-4.4 + 1.0 * i for i in range(7)]
RA_Y, RB_Y, RH = 1.65, -1.4, 1.8
CHA_Y, CHB_Y = 3.1, 0.1


def mini_row(y):
    bs = VGroup(*[RoundedRectangle(corner_radius=0.2, width=0.92, height=RH, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0]) for x in MX])
    labs = VGroup(*[T(f"r{i + 1}", 24, GREY).move_to([x, y + RH / 2 - 0.35, 0]) for i, x in enumerate(MX)])
    return bs, labs


def chips_rows():
    ck = bchip("Krox20", GREY, 26, pad=0.16)
    ck.move_to([-4.86, CHA_Y, 0], aligned_edge=LEFT)
    ch = bchip("Hoxb1", PURPLE, 26, pad=0.16)
    ch.move_to([-4.86, CHB_Y, 0], aligned_edge=LEFT)
    return ck, ch


def out1():
    t = VGroup(T("territory lost", 32, TEXT, weight=BOLD),
               T("cells survive, mix,\nchange identity", 24, GREY)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    return t.move_to([2.6, RA_Y, 0], aligned_edge=LEFT)


def out2():
    t = VGroup(T("identity changed", 32, TEXT, weight=BOLD),
               T("segment kept", 24, GREY)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    return t.move_to([2.6, RB_Y - 0.05, 0], aligned_edge=LEFT)


class S13Two(SpokenScene):
    def construct(self):
        bt, lt = mini_row(RA_Y)
        bb, lb = mini_row(RB_Y)
        bb[3].set_stroke(YELLOW, 5).set_fill(YELLOW, 0.14)
        ck, ch = chips_rows()
        self.at("there are two")
        self.play(FadeIn(bt), FadeIn(lt), FadeIn(bb), FadeIn(lb), FadeIn(ck), FadeIn(ch), run_time=0.8)
        self.at("without", nth=0)
        self.play(Create(kox(ck, 0.5, 0.3)), run_time=0.4)
        self.play(bt[2].animate.set_stroke(GREY, 1).set_fill(GREY, 0.0), bt[4].animate.set_stroke(GREY, 1).set_fill(GREY, 0.0),
                  lt[2].animate.set_opacity(0.1), lt[4].animate.set_opacity(0.1), run_time=0.6)
        t1 = out1()
        self.at("distinct territories")
        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("without", nth=1)
        self.play(Create(kox(ch, 0.5, 0.3)), run_time=0.4)
        t2 = out2()
        self.at("remains")
        self.play(bb[3].animate.set_stroke(TEXT, 5), FadeIn(t2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("changes")
        self.play(bb[3].animate.set_fill(TEAL, 0.32), run_time=0.7)
        self.finish()


def s13_final():
    bt, lt = mini_row(RA_Y)
    bb, lb = mini_row(RB_Y)
    for i in (2, 4):
        bt[i].set_stroke(GREY, 1).set_fill(GREY, 0.0)
        lt[i].set_opacity(0.1)
    bb[3].set_stroke(TEXT, 5).set_fill(TEAL, 0.32)
    ck, ch = chips_rows()
    return [bt, lt, bb, lb, ck, ch, kox(ck, 0.5, 0.3), kox(ch, 0.5, 0.3), out1(), out2()], ck, ch


def elbow(chp, y, end_y):
    x0 = chp.get_right()[0] + 0.95
    seg = Line([x0, y, 0], [3.5, y, 0], color=TEXT, stroke_width=3.5)
    tip = Arrow([3.5, y, 0], [3.5, end_y, 0], color=TEXT, stroke_width=3.5, buff=0, max_tip_length_to_length_ratio=0.35)
    return VGroup(seg, tip)


class S14Cause(SpokenScene):
    def construct(self):
        mobs, ck, ch = s13_final()
        self.add(*mobs)
        ea, eb = elbow(ck, CHA_Y, 2.55), elbow(ch, CHB_Y, -0.75)
        self.at("code")
        self.play(Create(ea), Create(eb), run_time=0.7)
        a = T("a cause", 40, TEXT, weight=BOLD)
        b = T("not just a marker", 40, GREY)
        line = VGroup(a, b).arrange(RIGHT, buff=0.45).move_to([0, -2.95, 0])
        sub = T("needed for identity", 26, GREY).move_to([0, -3.5, 0])
        self.at("cause")
        self.play(FadeIn(a, shift=UP * 0.15), run_time=0.5)
        self.at("not just")
        self.play(FadeIn(b, shift=UP * 0.15), run_time=0.5)
        self.at("marker")
        self.play(FadeIn(sub), run_time=0.4)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        mobs, ck, ch = s13_final()
        self.add(*mobs, elbow(ck, CHA_Y, 2.55), elbow(ch, CHB_Y, -0.75))
        a = T("a cause", 40, TEXT, weight=BOLD)
        b = T("not just a marker", 40, GREY)
        self.add(VGroup(a, b).arrange(RIGHT, buff=0.45).move_to([0, -2.95, 0]), T("needed for identity", 26, GREY).move_to([0, -3.5, 0]))
        self.wait(0.3)
        self.play(Indicate(mobs[8], color=TEXT, scale_factor=1.05), run_time=0.8)
        self.wait(0.2)
        self.play(Indicate(mobs[9], color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S16Bridge(SpokenScene):
    def construct(self):
        g = grid7()
        self.add(g.frames, g.heads, g.label_group, g.dot_group())
        q = T("Where do the edges come from?", 34, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        first = {"Hoxa2": 1, "Hoxb2": 2, "Hoxb1": 3, "Hoxb3": 4, "Hoxb4": 6}
        rings = VGroup(*[Circle(0.43, stroke_color=TEXT, stroke_width=4).move_to(g.dots[(n, c)].get_center()) for n, c in first.items()])
        brks = VGroup(*[VGroup(Line([g.dots[(n, c)].get_center()[0] - 0.6, g.y[n] + 0.3, 0], [g.dots[(n, c)].get_center()[0] - 0.6, g.y[n] - 0.3, 0],
                                    color=TEXT, stroke_width=5)) for n, c in first.items()])
        self.at("where do")
        self.play(FadeIn(q), FadeIn(rings), FadeIn(brks), run_time=0.5)
        self.at("edges")
        self.play(*[Indicate(rg, color=TEXT, scale_factor=1.3) for rg in rings], *[Indicate(b, color=TEXT, scale_factor=1.2) for b in brks], run_time=0.9)
        self.finish()


class S17Take(SpokenScene):
    def construct(self):
        bx = -2.5
        box = RoundedRectangle(corner_radius=0.3, width=4.6, height=5.4, stroke_color=YELLOW, stroke_width=5,
                               fill_color=YELLOW, fill_opacity=0.14).move_to([bx, -0.1, 0])
        r4 = T("r4", 40, TEXT, weight=BOLD).move_to(box.get_top() + DOWN * 0.55)
        chips = [bchip(n, PURPLE, 28).move_to([bx - 0.4, y, 0]) for n, y in (("Hoxa2", 1.2), ("Hoxb2", 0.3), ("Hoxb1", -0.6))]
        self.play(FadeIn(box), FadeIn(r4), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.15), run_time=0.7)
        self.at("without")
        self.play(Create(kox(chips[2], 0.5, 0.3)), chips[2].animate.set_opacity(0.4), run_time=0.7)
        keep = T("segment kept", 36, TEXT, weight=BOLD).move_to([3.3, 0.9, 0])
        self.at("survives")
        self.play(box.animate.set_stroke(TEXT, 7), Indicate(box, color=TEXT, scale_factor=1.03), FadeIn(keep, shift=LEFT * 0.2), run_time=0.8)
        self.at("loses key parts")
        self.play(box.animate.set_fill(TEAL, 0.32), run_time=0.8)
        lab = T("identity changed", 36, TEAL, weight=BOLD).move_to([3.3, -0.3, 0])
        self.at("identity")
        self.play(FadeIn(lab, shift=LEFT * 0.2), run_time=0.5)
        sp = T("other Hox genes, other outcomes", 28, GREY).move_to([0, -3.4, 0])
        self.at("other")
        self.play(FadeIn(sp), run_time=0.6)
        self.at("gene by gene")
        self.play(Indicate(sp, color=TEXT, scale_factor=1.06), run_time=0.8)
        self.finish()


class S18End(EndCard):
    LINE = "Without Hoxb1, r4 survives but loses key parts of its identity."
