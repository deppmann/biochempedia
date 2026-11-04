"""Out of Step (chapter 4 of Ocular Dominance and the Critical Period)

COLOR MAP (one colour per concept, the whole chapter; shared with the other chapters)
  ORANGE = right eye (contralateral to the recorded left hemisphere), and cells only it drives (group 1 end)
  BLUE   = left eye (ipsilateral), and cells only it drives (group 7 end)
  PURPLE = the cell (a cell driven by both eyes, the shared cell). Lit = bright purple fill; weakly lit = pale fill
  GREEN  = strengthened, kept, strong response (above the line)
  RED    = weakened, weak response (below the line), a crossed-out idea
  GOLD   = tags, rings and guide lines; the threshold line on the response meter
  TEXT   = a generic input (no eye named), the edge, patterned light
  GREY   = outlines, the scene bar, the membrane, neutral things
Histogram bars run from orange (group 1, left) through purple (group 4) to blue (group 7, right).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F2994A"
PINK = "#E58AB8"      # the co-agonist (only in the receptor scenes)

RNG = np.random.RandomState(11)


# ------------------------------------------------------------------ small helpers
def eye_icon(color, scale=1.0, dim=False):
    ell = Ellipse(width=2.0, height=1.1, stroke_color=color, stroke_width=4, fill_color=color,
                  fill_opacity=0.05 if dim else 0.15)
    pup = Circle(radius=0.3, stroke_width=0, fill_color=color, fill_opacity=0.15 if dim else 1)
    glint = Circle(radius=0.08, stroke_width=0, fill_color=BG, fill_opacity=0 if dim else 1).move_to(pup.get_center() + UR * 0.1)
    g = VGroup(ell, pup, glint).scale(scale)
    if dim:
        g.set_stroke(opacity=0.45)
    return g


def pos(x, y):
    return np.array([x, y, 0.0])


def tick(x, y, color, h=0.3, w=5):
    return Line(pos(x, y - h), pos(x, y + h), stroke_color=color, stroke_width=w)


def dashed_v(x, y0, y1, color=GOLD):
    return DashedLine(pos(x, y0), pos(x, y1), color=color, stroke_width=3, dash_length=0.12)


# ------------------------------------------------------------------ histogram (large: the plot fills the frame)
HX = [(i - 3) * 1.5 for i in range(7)]
BASE = -2.45
UNIT = 0.42
H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_STRAB = [12, 2, 1, 1, 1, 2, 12]


def gcol(i):
    O, P, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(O, P, i / 3) if i <= 3 else interpolate_color(P, B, (i - 3) / 3)


def hbars(h, op=0.6):
    out = VGroup()
    for i, v in enumerate(h):
        hh = max(v * UNIT, 0.04)
        out.add(Rectangle(width=1.2, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                          fill_opacity=op).move_to(pos(HX[i], BASE + hh / 2)))
    return out


def hist_axes():
    ax = Line(pos(-5.5, BASE), pos(5.5, BASE), color=GREY, stroke_width=3)
    ay = Line(pos(-5.5, BASE), pos(-5.5, BASE + 5.2), color=GREY, stroke_width=3)
    yl = T("cells", 26, GREY).rotate(PI / 2).move_to(pos(-6.1, BASE + 2.6))
    nums = VGroup(*[T(str(i + 1), 26, TEXT).move_to(pos(HX[i], BASE - 0.36)) for i in range(7)])
    t1 = T("right eye only", 26, ORANGE).move_to(pos(HX[0], BASE - 0.8))
    t4 = T("both", 26, PURPLE).move_to(pos(HX[3], BASE - 0.8))
    t7 = T("left eye only", 26, BLUE).move_to(pos(HX[6], BASE - 0.8))
    xt = T("ocular dominance group", 26, GREY).move_to(pos(0, BASE - 1.2))
    return VGroup(ax, ay, yl, nums, t1, t4, t7, xt)


def schem_tag():
    return T("schematic", 26, GOLD).move_to(pos(-5.2, 3.45))


def dot_columns(h=H_STRAB):
    cols = VGroup()
    for i, n in enumerate(h):
        col = VGroup(*[Circle(radius=0.16, stroke_width=0, fill_color=gcol(i), fill_opacity=1)
                       .move_to(pos(HX[i], BASE + 0.19 + UNIT * k)) for k in range(n)])
        cols.add(col)
    return cols


def hollow_box():
    return DashedVMobject(RoundedRectangle(corner_radius=0.2, width=4.5, height=2.1, stroke_color=GREY, stroke_width=3),
                          num_dashes=40).move_to(pos(0, BASE + 1.6))


def hollow_text(txt="hollow middle", col=GREY, size=28):
    return T(txt, size, col).move_to(pos(0, BASE + 1.6))


# ------------------------------------------------------------------ the gaze stage (top view)
BAR_Y = 2.55
AIM_FULL = 0.46     # right eye turned: where its line of sight lands, as a fraction of the bar width
AIM_DOCK = 0.45


def make_stage(cx=0.0, w=11.0, aimL=0.0, aimR=0.0):
    """Two eyes at the bottom, the scene bar at the top. Fixed structure so docked/full versions transform into each other.
    parts: bar, lab, bL, bR, nL, nR (names), pL, pR (pupils), lL, lR (lines of sight), dL, dR (landing dots), ring"""
    sep = 2.6 if w > 8 else 1.34
    r = 0.65 if w > 8 else 0.5
    ey = -2.45
    cL, cR = pos(cx - sep / 2, ey), pos(cx + sep / 2, ey)
    tL, tR = pos(cx + aimL * w, BAR_Y), pos(cx + aimR * w, BAR_Y)
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=1.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.06).move_to(pos(cx, BAR_Y))
    lab = T("the scene", 26, GREY).move_to(pos(cx - w / 2 + 1.05, BAR_Y + 0.65 + 0.3))
    bL = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(cL)
    bR = Circle(radius=r, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.15).move_to(cR)
    nL = T("left eye", 26, BLUE).move_to(pos(cx - sep / 2 - r - 0.95, ey))
    nR = T("right eye", 26, ORANGE).move_to(pos(cx + sep / 2 + r + 1.05, ey))

    def gz(c, t, col):
        d = t - c
        d = d / np.linalg.norm(d)
        off = 0.6 + 0.2 * min(1.0, max(0.0, abs(d[0]) - 0.3) / 0.3)   # pupil slides toward the rim as the eye turns
        pup = Dot(c + d * r * off, radius=0.3 * r, color=col)
        ln = Line(c + d * r, t, stroke_color=col, stroke_width=5)
        land = Dot(t, radius=0.16, color=col)
        return pup, ln, land

    pL, lL, dL = gz(cL, tL, BLUE)
    pR, lR, dR = gz(cR, tR, ORANGE)
    ring = Circle(radius=0.32, stroke_color=GOLD, stroke_width=4).move_to(tL)
    return dict(bar=bar, lab=lab, bL=bL, bR=bR, nL=nL, nR=nR, pL=pL, pR=pR, lL=lL, lR=lR, dL=dL, dR=dR, ring=ring,
                tL=tL, tR=tR, cR=cR, r=r)


KEYS = ["bar", "lab", "bL", "bR", "nL", "nR", "pL", "pR", "lL", "lR", "dL", "dR", "ring"]


def stage_group(st):
    return VGroup(*[st[k] for k in KEYS])


def stage_base(st):
    return VGroup(*[st[k] for k in ["bar", "lab", "bL", "bR", "nL", "nR", "pL", "pR"]])


def turned_tag(st):
    return T("turned", 28, GOLD).move_to(st["cR"] + DOWN * (st["r"] + 0.4))


# ------------------------------------------------------------------ raster rows (spike trains)
RX0, RW = 0.3, 3.6
RY_O, RY_B = 1.5, -1.1


def row_line(x0, w, y, color):
    return Line(pos(x0, y), pos(x0 + w, y), stroke_color=color, stroke_width=2, stroke_opacity=0.5)


def burst(x, y, color, n=3, gap=0.1):
    return VGroup(*[tick(x + (k - (n - 1) / 2) * gap, y, color, h=0.32, w=6) for k in range(n)])


# ------------------------------------------------------------------ the cell, its inputs, the response meter
CC = pos(0.0, 0.2)
CR = 1.7
LIT, WEAKLIT, DIM = 0.9, 0.3, 0.1     # one lit state for every cell in the chapter


def bsize(w):
    return 0.07 + 0.022 * w


def mk_cell(C=CC, r=CR, col=PURPLE, op=DIM):
    return Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=op).move_to(C)


def cell_lab(cell, size=30, text="cell"):
    """the 'cell' label turns dark when the cell is lit so it stays readable"""
    lab = T(text, size, TEXT).move_to(cell.get_center())
    lab.add_updater(lambda m: m.set_color(BG if cell.get_fill_opacity() > 0.45 else TEXT))
    return lab


def mk_fibre(color, y0, C=CC, r=CR, w=8, x0=-5.4, ang=None):
    start = pos(x0, y0)
    d = start - C
    d = d / np.linalg.norm(d)
    end = C + d * r
    if ang is not None:
        a = np.radians(ang)
        end = C + r * pos(-np.cos(a), np.sin(a))
    return VGroup(Line(start, end, stroke_color=color, stroke_width=w), Dot(end, radius=bsize(w), color=color))


def to_w(inp, w):
    f, b = inp
    return [f.animate.set_stroke(width=w), Transform(b, Dot(f.get_end(), radius=bsize(w), color=b.get_color()))]


def recolor(inp, color):
    return [inp[0].animate.set_stroke(color=color), inp[1].animate.set_color(color)]


def fire(scene, inps, run=0.5, col=TEXT):
    cols = col if isinstance(col, (list, tuple)) else [col] * len(inps)
    dots = [Dot(i[0].get_start(), radius=0.22, color=c) for i, c in zip(inps, cols)]
    scene.add(*dots)
    scene.play(*[d.animate.move_to(i[0].get_end()) for d, i in zip(dots, inps)], run_time=run, rate_func=linear)
    scene.remove(*dots)


def glow(cell, op):
    return cell.animate.set_fill(opacity=op)


MX, MB, MT = 3.7, -2.9, 2.9
STRONG_H, WEAK_H = 4.6, 1.5


def meter(L=0.5):
    above = Rectangle(width=0.8, height=MT - L, stroke_width=0, fill_color=GREEN, fill_opacity=0.15).move_to(pos(MX, (L + MT) / 2))
    below = Rectangle(width=0.8, height=L - MB, stroke_width=0, fill_color=RED, fill_opacity=0.15).move_to(pos(MX, (MB + L) / 2))
    frame = RoundedRectangle(corner_radius=0.1, width=0.8, height=MT - MB, stroke_color=GREY, stroke_width=3).move_to(pos(MX, 0))
    line = Line(pos(MX - 0.5, L), pos(MX + 0.5, L), color=GOLD, stroke_width=7)
    line.set_z_index(5)
    s = T("strong", 26, GREEN).move_to(pos(5.3, L + 0.7))
    wk = T("weak", 26, RED).move_to(pos(5.3, L - 0.7))
    th = T("threshold", 26, GOLD).move_to(pos(5.3, L))
    return VGroup(above, below, frame, line, s, wk, th)


def level(h, L=0.5, col=None):
    h = max(h, 0.03)
    col = col or (GREEN if MB + h > L else RED)
    return Rectangle(width=0.6, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(pos(MX, MB + h / 2)).set_z_index(2)


def meter_cap():
    return T("response", 26, GREY).move_to(pos(MX, 3.35))


def wire():
    return Arrow(pos(1.85, 0.2), pos(3.15, 0.2), buff=0, color=GREY, stroke_width=4, tip_length=0.2)


def small_eye(col, y, x=-5.95):
    return eye_icon(col, 0.42).move_to(pos(x, y))


def tag(text, color, x, y, size=26):
    return T(text, size, color).move_to(pos(x, y))


def respond(scene, cell, op, lv=None, h=None, run=0.35):
    anims = [glow(cell, op)]
    if lv is not None:
        anims.append(Transform(lv, level(h)))
    scene.play(*anims, run_time=run)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Ocular dominance and the critical period"
    TITLE = "Out of Step"


class S01(SpokenScene):
    def construct(self):
        eO = eye_icon(ORANGE, 1.0).move_to(pos(-5.2, 1.9))
        eB = eye_icon(BLUE, 1.0).move_to(pos(-5.2, -0.1))
        nO = T("right eye", 26, ORANGE).move_to(pos(-5.2, 1.15))
        nB = T("left eye", 26, BLUE).move_to(pos(-5.2, -0.85))
        lg = VGroup(chip("orange = right eye", ORANGE, 26), chip("blue = left eye", BLUE, 26),
                    T("recording: left hemisphere", 26, TEXT)).arrange(RIGHT, buff=0.45).move_to(pos(0, -3.1))
        self.play(FadeIn(VGroup(eO, eB, nO, nB), shift=RIGHT * 0.2), FadeIn(lg, shift=UP * 0.1), run_time=0.9)
        self.at("equal amounts")
        bO = RoundedRectangle(corner_radius=0.12, width=0.1, height=0.6, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to(pos(-3.55, 1.9))
        bB = RoundedRectangle(corner_radius=0.12, width=0.1, height=0.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to(pos(-3.55, -0.1))
        fO = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.6, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to(pos(-1.1, 1.9))
        fB = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to(pos(-1.1, -0.1))
        self.add(bO, bB)
        self.play(Transform(bO, fO), Transform(bB, fB), run_time=0.8)
        eq = T("equal", 32, GOLD).move_to(pos(-1.1, 0.9))
        self.play(FadeIn(eq), run_time=0.4)
        self.at("share a cell")
        cell = Circle(radius=1.2, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.15).move_to(pos(4.7, 0.9))
        lO = Line(pos(1.5, 1.9), pos(3.65, 1.3), stroke_color=ORANGE, stroke_width=6)
        lB = Line(pos(1.5, -0.1), pos(3.65, 0.5), stroke_color=BLUE, stroke_width=6)
        self.play(FadeIn(cell, scale=0.8), Create(lO), Create(lB), run_time=0.4)
        self.at("cell")
        q = T("?", 80, GOLD, weight=BOLD).move_to(cell)
        self.play(FadeIn(q, scale=1.3), run_time=0.4)
        self.finish()


def toy_table():
    xs = dict(lab=-5.3, a=-2.7, b=-0.8, d=2.0, c=5.0)
    ys = [2.6, 1.3, 0.0, -1.3]
    rows = [("both open", "10", "10", "100%", "50%"), ("one closed", "10", "1", "10%", "9%"),
            ("both closed", "1", "1", "10%", "50%")]
    hdr = VGroup(T("eye A", 26, ORANGE).move_to(pos(xs["a"], ys[0])), T("eye B", 26, BLUE).move_to(pos(xs["b"], ys[0])),
                 T("disuse", 26, GREY).move_to(pos(xs["d"], ys[0])), T("competition", 26, GREY).move_to(pos(xs["c"], ys[0])))
    body = VGroup()
    for (lab, a, b, d, c), y in zip(rows, ys[1:]):
        lt = T(lab, 26, TEXT).move_to(pos(xs["lab"], y))
        lt.align_to(pos(-6.3, 0), LEFT)
        body.add(VGroup(lt, M(a, 30, ORANGE).move_to(pos(xs["a"], y)), M(b, 30, BLUE).move_to(pos(xs["b"], y)),
                        M(d, 28, GREY).move_to(pos(xs["d"], y)), M(c, 28, GREY).move_to(pos(xs["c"], y))))
    rule = Line(pos(-6.4, 1.95), pos(6.4, 1.95), color=GREY, stroke_width=2)
    return hdr, body, rule


class S02(SpokenScene):
    def construct(self):
        hdr, body, rule = toy_table()
        note = T("toy numbers, illustrative", 26, GREY).move_to(pos(0, -3.4))
        dim = [hdr[2], hdr[3]] + [r[3] for r in body] + [r[4] for r in body]
        self.play(FadeIn(hdr), Create(rule), FadeIn(body, lag_ratio=0.2), FadeIn(note), run_time=0.7)
        self.at("counts only amount")
        box = RoundedRectangle(corner_radius=0.2, width=3.9, height=4.4, stroke_color=GOLD, stroke_width=4).move_to(pos(-1.75, 0.65))
        amt = T("amount", 30, GOLD).move_to(pos(-1.75, -2.2))
        self.play(Create(box), *[d.animate.set_opacity(0.3) for d in dim], FadeIn(amt), run_time=0.9)
        self.at("tests whether amount")
        q = T("enough?", 40, GOLD, weight=BOLD).move_to(pos(3.4, -2.2))
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        st = make_stage(aimL=0.0, aimR=0.0)
        self.play(FadeIn(stage_base(st)), run_time=0.7)
        self.play(Create(st["lL"]), Create(st["lR"]), FadeIn(st["dL"]), FadeIn(st["dR"]), FadeIn(st["ring"]), run_time=0.5)
        self.at("misaligned")
        st2 = make_stage(aimL=0.0, aimR=AIM_FULL)
        tt = turned_tag(st2)
        self.play(Transform(VGroup(st["pR"], st["lR"], st["dR"]), VGroup(st2["pR"], st2["lR"], st2["dR"])),
                  FadeOut(st["ring"]), FadeIn(tt, shift=UP * 0.1), run_time=1.2)
        self.at("points at a different part")
        self.play(Flash(st["dL"], color=BLUE, flash_radius=0.5), Flash(st["dR"], color=ORANGE, flash_radius=0.5), run_time=0.9)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        credit = T("Hubel and Wiesel", 40, TEXT, font=TITLE_FONT).move_to(pos(0, 3.25))
        self.play(Write(credit), run_time=0.8)
        c = pos(0, -0.1)
        R = 2.0
        ball = Circle(radius=R, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.12).move_to(c)
        iris = Circle(radius=0.55, stroke_color=ORANGE, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(c + UP * (R - 0.85))
        musL = Line(c + pos(-1.65, -1.1), pos(-4.3, -3.2), stroke_color=GREY, stroke_width=18)
        musR1 = Line(c + pos(1.65, -1.1), pos(2.7, -1.95), stroke_color=GREY, stroke_width=18)
        musR2 = Line(pos(3.25, -2.4), pos(4.3, -3.2), stroke_color=GREY, stroke_width=18)
        self.at("produced it")
        self.play(FadeIn(ball), FadeIn(iris), FadeIn(VGroup(musL, musR1, musR2)), run_time=0.7)
        self.at("young kittens")
        chipk = chip("young kitten", GOLD, size=28).move_to(pos(-4.6, 1.6))
        self.play(FadeIn(chipk, shift=UP * 0.1), run_time=0.5)
        self.at("cutting one eye")
        cut = VGroup(Line(pos(2.85, -1.85), pos(3.2, -2.55), stroke_color=RED, stroke_width=9),
                     Line(pos(3.05, -1.7), pos(3.4, -2.4), stroke_color=RED, stroke_width=9))
        cutlab = T("one eye muscle\ncut", 38, RED, line_spacing=0.6).move_to(pos(4.55, -0.35))
        lead = Arrow(pos(4.0, -0.95), pos(3.25, -1.8), buff=0.05, color=RED, stroke_width=5, tip_length=0.22)
        self.play(Create(cut), FadeIn(cutlab, shift=UP * 0.1), Create(lead), run_time=0.5)
        self.at("muscle")
        turned = T("eye turned", 40, GOLD).move_to(pos(-4.3, -0.2))
        self.play(iris.animate.rotate(1.35, about_point=c), FadeIn(turned, shift=UP * 0.1), run_time=0.9)
        self.finish()


def light_patch(x, col):
    g = VGroup()
    bg = Square(side_length=0.95, stroke_color=col, stroke_width=4, fill_color=BG, fill_opacity=1)
    g.add(bg)
    for k in range(5):
        g.add(Rectangle(width=0.13, height=0.95, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to(bg.get_center() + RIGHT * (k - 2) * 0.19))
    return g.move_to(pos(x, BAR_Y))


class S05(SpokenScene):
    def construct(self):
        st = make_stage(aimL=0.0, aimR=AIM_FULL)
        tt = turned_tag(st)
        self.add(stage_group(st), tt)
        self.wait(0.2)
        self.at("each eye still received")
        dots = [Dot(st["lL"].get_end(), radius=0.16, color=TEXT), Dot(st["lR"].get_end(), radius=0.16, color=TEXT)]
        self.add(*dots)
        self.play(dots[0].animate.move_to(st["lL"].get_start()), dots[1].animate.move_to(st["lR"].get_start()), run_time=0.9, rate_func=linear)
        self.remove(*dots)
        self.at("normal amount")
        lab = T("normal amount of light", 30, GOLD).move_to(pos(-3.9, 0.1))
        self.play(FadeIn(lab, shift=RIGHT * 0.15), run_time=0.5)
        self.at("patterned")
        pL = light_patch(st["tL"][0], BLUE)
        pR = light_patch(st["tR"][0], ORANGE)
        self.play(FadeOut(st["dL"]), FadeOut(st["dR"]), FadeIn(pL), FadeIn(pR), run_time=0.6)
        self.finish()


def strip_eyes():
    eO = eye_icon(ORANGE, 0.5).move_to(pos(-5.8, 3.2))
    eB = eye_icon(BLUE, 0.5).move_to(pos(0.65, 3.2))
    bO = RoundedRectangle(corner_radius=0.12, width=4.4, height=0.6, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to(pos(-2.95, 3.2))
    bB = RoundedRectangle(corner_radius=0.12, width=4.4, height=0.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to(pos(3.45, 3.2))
    tO = T("normal amount", 26, BG, weight=BOLD).move_to(bO)
    tB = T("normal amount", 26, BG, weight=BOLD).move_to(bB)
    return (eO, bO, tO), (eB, bB, tB)


def pred_question():
    q = T("?", 130, GOLD, weight=BOLD).move_to(pos(0, -0.3))
    cond = T("if amount is all that matters", 32, GOLD).move_to(pos(0, 1.5))
    return q, cond


class S06(SpokenScene):
    def construct(self):
        ax = hist_axes()
        (eO, bO, tO), (eB, bB, tB) = strip_eyes()
        pred = T("Predict", 56, GOLD, font=TITLE_FONT).move_to(pos(0, 3.2))
        q, cond = pred_question()
        # on screen from the first word: the title, the condition and the question
        self.play(FadeIn(ax), FadeIn(pred), FadeIn(cond), FadeIn(q, scale=1.2), run_time=0.4)
        self.at("each eye sends")
        bO0 = bO.copy()
        bB0 = bB.copy()
        bO.stretch_to_fit_width(0.1, about_edge=LEFT)
        bB.stretch_to_fit_width(0.1, about_edge=LEFT)
        bO.move_to(bO0.get_left() + RIGHT * 0.05)
        bB.move_to(bB0.get_left() + RIGHT * 0.05)
        self.add(bO, bB)
        self.play(FadeOut(pred), FadeIn(eO), FadeIn(eB), run_time=0.4)
        self.play(Transform(bO, bO0), Transform(bB, bB0), run_time=1.6)
        self.at("normal kitten")
        self.play(FadeIn(tO), FadeIn(tB), run_time=0.6)
        self.at("were all that mattered")
        self.play(Indicate(cond, scale_factor=1.12, color=GOLD), run_time=0.7)
        self.at("what should the histogram look like")
        self.play(Indicate(q, scale_factor=1.15, color=GOLD), run_time=0.8)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        ax = hist_axes()
        (eO, bO, tO), (eB, bB, tB) = strip_eyes()
        q, cond = pred_question()
        self.add(ax, eO, bO, tO, eB, bB, tB, q, cond)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        ax = hist_axes()
        (eO, bO, tO), (eB, bB, tB) = strip_eyes()
        q, cond = pred_question()
        self.add(ax, eO, bO, tO, eB, bB, tB, q, cond)
        self.at("alone set each")
        self.play(FadeOut(q), run_time=0.4)
        bars = hbars(H_NORMAL)
        predtag = VGroup(T("what amount", 28, GOLD), T("alone predicts", 28, GOLD), T("(schematic)", 26, GOLD)).arrange(DOWN, buff=0.15).move_to(pos(-3.75, 1.5))
        self.at("histogram would look")
        self.play(FadeOut(cond), run_time=0.3)
        self.play(FadeIn(predtag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), run_time=1.5)
        self.at("it did not")
        cross = VGroup(Line(pos(-5.2, -2.3), pos(5.2, 2.4), stroke_color=RED, stroke_width=8),
                       Line(pos(-5.2, 2.4), pos(5.2, -2.3), stroke_color=RED, stroke_width=8))
        self.play(Create(cross), bars.animate.set_fill(opacity=0.15).set_stroke(opacity=0.3), run_time=0.7)
        self.play(FadeOut(cross), FadeOut(bars), FadeOut(predtag), run_time=0.8)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        ax = hist_axes()
        sch = schem_tag()
        self.add(ax, sch)
        cols = dot_columns()
        flat = [d for col in cols for d in col]
        targets = [d.get_center() for d in flat]
        n = len(flat)
        pts = []
        while len(pts) < n:
            p = pos(RNG.uniform(-4.4, 4.4), RNG.uniform(-1.6, 2.0))
            if all(np.linalg.norm(p - q) > 0.5 for q in pts):
                pts.append(p)
        cloud = [Circle(radius=0.16, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p) for p in pts]
        self.play(FadeIn(VGroup(*cloud), lag_ratio=0.05), run_time=0.9)
        self.at("one eye or the other")
        anims = []
        for d, t, tgt in zip(cloud, flat, targets):
            anims.append(d.animate.move_to(tgt).set_fill(t.get_fill_color()))
        self.play(LaggedStart(*anims, lag_ratio=0.03), run_time=1.2)
        self.at("few to both")
        mids = [cloud[i] for i in range(n) if 2 <= self.col_of(i) <= 4]
        self.play(*[Indicate(m, scale_factor=1.8, color=PURPLE) for m in mids], run_time=0.8)
        self.finish()

    @staticmethod
    def col_of(i):
        acc = 0
        for c, k in enumerate(H_STRAB):
            acc += k
            if i < acc:
                return c
        return 6


class S10(SpokenScene):
    def construct(self):
        ax = hist_axes()
        sch = schem_tag()
        cols = dot_columns()
        self.add(ax, sch, cols)
        self.at("the histogram had")
        bars = hbars(H_STRAB)
        self.play(*[ReplacementTransform(c, b) for c, b in zip(cols, bars)], run_time=1.0)
        self.at("piles at groups")
        self.play(Indicate(bars[0], scale_factor=1.08, color=ORANGE), Indicate(bars[6], scale_factor=1.08, color=BLUE), run_time=1.0)
        self.at("hollow middle")
        hb = hollow_box()
        ht = hollow_text()
        self.play(Create(hb), FadeIn(ht), run_time=0.9)
        self.finish()


class S11Beat(NarratedScene):
    def construct(self):
        ax = hist_axes()
        bars = hbars(H_STRAB)
        hb = hollow_box()
        ht = hollow_text()
        self.add(ax, schem_tag(), bars, hb, ht)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        ax = hist_axes()
        bars = hbars(H_STRAB)
        hb = hollow_box()
        ht = hollow_text()
        self.add(ax, schem_tag(), bars, hb, ht)
        self.at("took over")
        top = BASE + 12 * UNIT
        guide = DashedLine(pos(-4.5, top + 0.3), pos(4.5, top + 0.3), color=GOLD, stroke_width=4, dash_length=0.15)
        bal = T("about equal", 30, GOLD).move_to(pos(0, top + 0.75))
        self.play(Create(guide), FadeIn(bal), run_time=0.9)
        self.at("eyes had shared")
        ht2 = hollow_text("lost shared cells", TEXT, 28)
        self.play(FadeOut(ht), FadeIn(ht2), run_time=0.7)
        self.at("equal amounts")
        eq = T("equal amounts were not enough", 32, RED).move_to(pos(0, 0.95))
        self.play(FadeIn(eq, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        ax = hist_axes()
        bars = hbars(H_STRAB)
        hb = hollow_box()
        self.add(ax, bars, hb)
        yO, yB = 0.5, -2.0
        x0, x1 = -4.7, 5.9
        eO = eye_icon(ORANGE, 0.5).move_to(pos(-5.8, yO))
        eB = eye_icon(BLUE, 0.5).move_to(pos(-5.8, yB))
        rO, rB = row_line(x0, x1 - x0, yO, ORANGE), row_line(x0, x1 - x0, yB, BLUE)
        tO = [-3.7, -2.4, -0.6, 0.9, 2.6, 4.1]
        tB = [-3.2, -1.7, -0.2, 1.7, 3.1, 4.6]
        ticksO = VGroup(*[tick(x, yO, ORANGE, h=0.55, w=7) for x in tO])
        ticksB = VGroup(*[tick(x, yB, BLUE, h=0.55, w=7) for x in tB])
        # the equal-count trains arrive with the first words
        self.play(FadeOut(VGroup(ax, bars, hb)), FadeIn(VGroup(eO, eB, rO, rB)),
                  LaggedStart(*[FadeIn(t) for t in ticksO], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(t) for t in ticksB], lag_ratio=0.1), run_time=1.0)
        self.at("amount")
        amt = T("amount", 52, TEXT, font=TITLE_FONT).move_to(pos(-2.2, 3.0))
        strike = Line(amt.get_left() + LEFT * 0.15, amt.get_right() + RIGHT * 0.15, stroke_color=RED, stroke_width=8)
        eqs = T("equal: six spikes each", 32, GREY).move_to(pos(-2.2, 2.2))
        self.play(FadeIn(amt), FadeIn(eqs), run_time=0.4)
        self.play(Create(strike), run_time=0.3)
        self.at("timing")
        tim = T("timing", 52, GOLD, font=TITLE_FONT).move_to(pos(2.6, 3.0))
        guides = VGroup(*[DashedLine(pos(x, yO - 0.65), pos(x, yB - 0.65), color=GOLD, stroke_width=3, dash_length=0.12, stroke_opacity=0.6) for x in tO])
        self.play(FadeIn(tim), Create(guides), run_time=0.5)
        self.at("between the eyes")
        gap = DoubleArrow(pos(0.9, yO - 0.65), pos(1.7, yB + 0.65), buff=0, color=GOLD, stroke_width=4, tip_length=0.2)
        glab = T("timing offset", 34, GOLD).move_to(pos(3.7, (yO + yB) / 2))
        gbk = Rectangle(width=glab.width + 0.3, height=glab.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(glab)
        self.play(Create(gap), FadeIn(gbk), FadeIn(glab, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        st = make_stage(aimL=0.0, aimR=0.0)
        self.play(FadeIn(stage_base(st)), run_time=0.6)
        self.at("aligned")
        chk = T("aligned", 36, GOLD).move_to(pos(-4.2, 0.0))
        self.play(FadeIn(chk), run_time=0.4)
        self.at("look at the same point")
        self.play(Create(st["lL"]), Create(st["lR"]), run_time=0.9)
        self.play(FadeIn(st["dL"]), FadeIn(st["dR"]), FadeIn(st["ring"]), Flash(st["ring"], color=GOLD, flash_radius=0.7), run_time=0.7)
        self.finish()


def edge_bar(x, y=BAR_Y):
    return Line(pos(x, y - 0.5), pos(x, y + 0.5), stroke_color=TEXT, stroke_width=10)


SC = pos(5.3, 0.2)


def shared_cell_panel():
    cell = mk_cell(SC, 0.85, PURPLE, DIM)
    lo = Line(pos(RX0 + RW + 0.1, RY_O), pos(SC[0] - 0.8, SC[1] + 0.3), stroke_color=ORANGE, stroke_width=4)
    lb = Line(pos(RX0 + RW + 0.1, RY_B), pos(SC[0] - 0.8, SC[1] - 0.3), stroke_color=BLUE, stroke_width=4)
    lbl = T("shared cell", 26, PURPLE).move_to(pos(SC[0], SC[1] - 1.3))
    return cell, lo, lb, lbl


def row_labels():
    a = T("right eye's input", 26, ORANGE).move_to(pos(RX0 + 1.7, RY_O + 0.7))
    b = T("left eye's input", 26, BLUE).move_to(pos(RX0 + 1.7, RY_B - 0.7))
    return a, b


BURSTS = [1.0, 2.1, 3.2]
CXD = -3.6


class S15(SpokenScene):
    def construct(self):
        full = make_stage(aimL=0.0, aimR=0.0)
        dock = make_stage(cx=CXD, w=5.6, aimL=0.0, aimR=0.0)
        self.add(stage_group(full))
        cell, lo, lb, lbl = shared_cell_panel()
        ra, rb = row_labels()
        rO, rB = row_line(RX0, RW, RY_O, ORANGE), row_line(RX0, RW, RY_B, BLUE)
        self.play(ReplacementTransform(stage_group(full), stage_group(dock)),
                  FadeIn(VGroup(rO, rB, ra, rb)), FadeIn(VGroup(cell, lo, lb, lbl)), run_time=0.7)
        cues = ["that point", "both eyes", "shared cell"]
        for k, bx in enumerate(BURSTS):
            self.at(cues[k])
            e = edge_bar(CXD - 1.5)
            self.add(e)
            self.play(e.animate.move_to(pos(CXD, BAR_Y)), run_time=0.3, rate_func=linear)
            bo = burst(bx, RY_O, ORANGE)
            bb = burst(bx + RNG.uniform(-0.03, 0.03), RY_B, BLUE)
            self.play(FadeIn(bo), FadeIn(bb), cell.animate.set_fill(opacity=LIT), e.animate.shift(RIGHT * 0.9), run_time=0.25, rate_func=linear)
            self.play(FadeOut(e), run_time=0.15)
            self.play(cell.animate.set_fill(opacity=DIM), run_time=0.2)
        self.at("same moments")
        guides = VGroup(*[dashed_v(bx, RY_O - 0.45, RY_B + 0.45) for bx in BURSTS])
        self.play(Create(guides), run_time=0.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        dock = make_stage(cx=CXD, w=5.6, aimL=0.0, aimR=0.0)
        self.add(stage_group(dock))
        cell, lo, lb, lbl = shared_cell_panel()
        ra, rb = row_labels()
        rO, rB = row_line(RX0, RW, RY_O, ORANGE), row_line(RX0, RW, RY_B, BLUE)
        self.add(rO, rB, ra, rb, cell, lo, lb, lbl)
        tk = []
        for bx in BURSTS:
            tk += [burst(bx, RY_O, ORANGE), burst(bx, RY_B, BLUE)]
        guides = VGroup(*[dashed_v(bx, RY_O - 0.45, RY_B + 0.45) for bx in BURSTS])
        self.add(*tk, guides)
        self.at("in step")
        l1 = T("in step", 36, GOLD)
        l2 = T("(correlated)", 36, GOLD)
        grp = VGroup(l1, l2).arrange(RIGHT, buff=0.25).move_to(pos(2.6, -2.7))
        self.play(FadeIn(l1, shift=UP * 0.1), cell.animate.set_fill(opacity=LIT), guides[0].animate.set_stroke(width=8), run_time=0.4)
        self.play(cell.animate.set_fill(opacity=DIM), guides[0].animate.set_stroke(width=3), run_time=0.2)
        self.at("correlated")
        self.play(FadeIn(l2, shift=UP * 0.1), cell.animate.set_fill(opacity=LIT), guides[1].animate.set_stroke(width=8), run_time=0.4)
        self.play(cell.animate.set_fill(opacity=DIM), guides[1].animate.set_stroke(width=3), run_time=0.2)
        self.play(cell.animate.set_fill(opacity=LIT), guides[2].animate.set_stroke(width=8), run_time=0.4)
        self.play(cell.animate.set_fill(opacity=DIM), guides[2].animate.set_stroke(width=3), run_time=0.2)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        cx = CXD
        dock = make_stage(cx=cx, w=5.6, aimL=0.0, aimR=0.0)
        mis = make_stage(cx=cx, w=5.6, aimL=0.0, aimR=AIM_DOCK)
        self.add(stage_group(dock))
        cell, lo, lb, lbl = shared_cell_panel()
        ra, rb = row_labels()
        rO, rB = row_line(RX0, RW, RY_O, ORANGE), row_line(RX0, RW, RY_B, BLUE)
        self.add(rO, rB, ra, rb, cell, lo, lb, lbl)
        tk = []
        for bx in BURSTS:
            tk += [burst(bx, RY_O, ORANGE), burst(bx, RY_B, BLUE)]
        guides = VGroup(*[dashed_v(bx, RY_O - 0.45, RY_B + 0.45) for bx in BURSTS])
        l1 = T("in step", 36, GOLD)
        l2 = T("(correlated)", 36, GOLD)
        grp = VGroup(l1, l2).arrange(RIGHT, buff=0.25).move_to(pos(2.6, -2.7))
        self.add(*tk, guides, grp)
        tt = turned_tag(mis)
        # the moment the eyes misalign, the old in-step picture goes away
        self.play(FadeOut(VGroup(*tk)), FadeOut(guides), FadeOut(grp),
                  Transform(VGroup(dock["pR"], dock["lR"], dock["dR"]),
                            VGroup(mis["pR"], mis["lR"], mis["dR"])), FadeOut(dock["ring"]), FadeIn(tt, shift=UP * 0.1),
                  run_time=0.9)
        ptL, ptR = cx, cx + AIM_DOCK * 5.6
        # raster x positions alternate: blue, orange, orange, blue, blue, orange (never lined up)
        plan = [(+1, 0.35, 1.0), (-1, 2.35, 1.7), (+1, 3.0, 3.65)]  # direction, blue x, orange x
        cues = ["each eye's input", "arrives while", "other is"]
        for k, (dr, xb, xo) in enumerate(plan):
            self.at(cues[k])
            a, b = (cx - 1.3, -0.9) if dr > 0 else (-0.9, cx - 1.3)
            e = edge_bar(a)
            self.add(e)
            first, second = (ptL, ptR) if dr > 0 else (ptR, ptL)
            self.play(e.animate.move_to(pos(first, BAR_Y)), run_time=0.2, rate_func=linear)
            b1 = burst(xb, RY_B, BLUE) if dr > 0 else burst(xo, RY_O, ORANGE)
            b2 = burst(xo, RY_O, ORANGE) if dr > 0 else burst(xb, RY_B, BLUE)
            self.play(FadeIn(b1), cell.animate.set_fill(opacity=WEAKLIT), e.animate.move_to(pos(second, BAR_Y)), run_time=0.3, rate_func=linear)
            self.play(cell.animate.set_fill(opacity=DIM), run_time=0.12)
            self.play(FadeIn(b2), cell.animate.set_fill(opacity=WEAKLIT), e.animate.move_to(pos(b, BAR_Y)), run_time=0.2, rate_func=linear)
            self.play(cell.animate.set_fill(opacity=DIM), FadeOut(e), run_time=0.15)
        self.at("unrelated")
        nt = T("not in step", 36, RED).move_to(pos(2.6, -2.7))
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.5)
        self.finish()


C19 = pos(0.4, 0.2)
R19 = 2.0


def hebb_parts(w=4):
    cell = mk_cell(C19, R19)
    inp = mk_fibre(TEXT, 0.2, C19, R19, w, x0=-5.8, ang=0)
    cl = cell_lab(cell, 34)
    il = T("input", 28, GREY).move_to(pos(-3.7, 0.75))
    out = Arrow(pos(C19[0] + R19, 0.2), pos(5.9, 0.2), buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    ol = T("output", 28, GREY).move_to(pos(4.5, 0.75))
    return cell, inp, cl, il, out, ol


class S18(SpokenScene):
    def construct(self):
        self.at("a rule that")
        cell, inp, cl, il, out, ol = hebb_parts()
        self.play(FadeIn(cell, scale=0.9), FadeIn(cl), Create(inp[0]), FadeIn(inp[1]), FadeIn(il), FadeIn(out), FadeIn(ol), run_time=1.0)
        name = T("Donald Hebb,", 60, TEXT, font=TITLE_FONT)
        yr = T("1949", 60, GOLD, font=TITLE_FONT)
        VGroup(name, yr).arrange(RIGHT, buff=0.45).move_to(pos(0, 3.0))
        self.at("Donald Hebb")
        self.play(Write(name), run_time=1.0)
        self.at("1949")
        self.play(FadeIn(yr, scale=1.2), run_time=0.5)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        cell, inp, cl, il, out, ol = hebb_parts()
        self.add(cell, inp, cl, il, out, ol)
        both = T("input fires, and the cell fires", 32, GOLD).move_to(pos(0, 3.0))

        def pulse(first=False):
            fire(self, [inp], run=0.3)
            od = Dot(pos(C19[0] + R19, 0.2), radius=0.2, color=TEXT)
            self.add(od)
            anims = [glow(cell, LIT), od.animate.move_to(pos(5.9, 0.2))]
            if first:
                anims.append(FadeIn(both, shift=UP * 0.1))
            self.play(*anims, run_time=0.35, rate_func=linear)
            self.remove(od)
            self.play(glow(cell, DIM), run_time=0.2)

        self.at("an input that")
        pulse(True)
        self.at("repeatedly")
        pulse()
        self.at("in firing")
        pulse()
        self.at("strengthened")
        tg = T("strengthened", 34, GREEN).move_to(pos(-3.6, -0.55))
        self.play(*to_w(inp, 15), *recolor(inp, GREEN), FadeIn(tg, shift=UP * 0.1), run_time=1.0)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        cell = mk_cell()
        inp = mk_fibre(TEXT, 0.2, w=10, ang=0)
        cl = cell_lab(cell)
        il = T("input", 28, GREY).move_to(pos(-3.4, 0.75))
        self.add(cell, inp, cl, il)
        hb = T("Hebb's half: strengthens", 28, GREEN).move_to(pos(-3.4, -2.0))
        self.play(FadeIn(hb, shift=UP * 0.1), run_time=0.5)
        self.at("added a weakening")
        added = T("added later", 34, GOLD).move_to(pos(-3.4, 2.9))
        self.play(FadeIn(added, shift=UP * 0.1), run_time=0.6)
        self.at("BCM model")
        bcm = T("BCM model", 40, GOLD, font=TITLE_FONT).move_to(pos(-3.4, 2.1))
        m, cap, w = meter(0.5), meter_cap(), wire()
        lv = level(0.0)
        self.play(FadeIn(bcm, shift=UP * 0.1), FadeIn(m), FadeIn(cap), FadeIn(w), FadeIn(lv), run_time=0.8)
        wd = T("weakened", 30, RED).move_to(pos(-3.2, -0.55))
        wk = T("weak response", 30, RED).move_to(pos(0.2, -2.55))
        self.at("an active input")
        fire(self, [inp], run=0.4)
        respond(self, cell, WEAKLIT, lv, WEAK_H, run=0.35)
        self.play(*to_w(inp, 7), glow(cell, DIM), Transform(lv, level(0.0)), run_time=0.4)
        self.at("weakens")
        self.play(*recolor(inp, RED), FadeIn(wd, shift=UP * 0.1), run_time=0.5)
        self.at("when the cell responds")
        fire(self, [inp], run=0.4)
        respond(self, cell, WEAKLIT, lv, WEAK_H, run=0.35)
        self.play(*to_w(inp, 4.5), glow(cell, DIM), Transform(lv, level(0.0)), run_time=0.4)
        self.at("but only weakly")
        self.play(FadeIn(wk, shift=UP * 0.1), run_time=0.4)
        fire(self, [inp], run=0.4)
        respond(self, cell, WEAKLIT, lv, WEAK_H, run=0.35)
        self.play(*to_w(inp, 3), run_time=0.5)
        self.finish()


def pulse_label(text, color, x, y, size=28):
    return T(text, size, color).move_to(pos(x, y))


class S20b(SpokenScene):
    def construct(self):
        cell = mk_cell()
        act = mk_fibre(TEXT, 1.7, w=8, ang=28)
        sil = mk_fibre(TEXT, -1.5, w=8, ang=-28)
        m, cap, w = meter(0.5), meter_cap(), wire()
        lv = level(0.0, col=GREEN)
        cl = cell_lab(cell)
        la = T("active input", 26, GREY).move_to(pos(-4.0, 2.55))
        ls = T("silent input", 26, GREY).move_to(pos(-4.0, -2.5))
        self.add(cell, act, sil, cl, la, ls, m, cap, w, lv)
        # beat 1: strong response first (meter above the line), then the active synapse thickens
        self.at("active input")
        fire(self, [act], run=0.4)
        self.play(glow(cell, LIT), Transform(lv, level(STRONG_H, col=GREEN)), run_time=0.35)
        self.at("strengthens when")
        g1 = pulse_label("strengthened", GREEN, -3.9, 0.85)
        self.play(*to_w(act, 13), *recolor(act, GREEN), FadeIn(g1, shift=UP * 0.1), run_time=0.5)
        self.at("responds strongly")
        # hold the strong state while "strongly" is spoken, then the compact weak beat fits the pause before "A silent input"
        t_weak = self.t_of("strongly") + 0.5
        if t_weak > self.elapsed():
            self.wait(t_weak - self.elapsed())
        self.play(glow(cell, DIM), Transform(lv, level(0.0)), FadeOut(g1), *to_w(act, 8), *recolor(act, TEXT), run_time=0.12)
        fire(self, [act], run=0.2)
        self.play(glow(cell, WEAKLIT), Transform(lv, level(WEAK_H)), run_time=0.12)
        r1 = pulse_label("weakened", RED, -3.9, 0.85)
        self.play(*to_w(act, 4), *recolor(act, RED), FadeIn(r1, shift=UP * 0.1), run_time=0.2)
        # beat 3: begins on the words "A silent input"; the label stays dim until then
        self.at("a silent input")
        self.play(glow(cell, DIM), Transform(lv, level(0.0)), FadeOut(r1), *to_w(act, 8), *recolor(act, TEXT),
                  Indicate(ls, scale_factor=1.15, color=TEXT), ls.animate.set_color(TEXT), run_time=0.5)
        nm = pulse_label("no response", GREY, 5.3, -2.55)
        self.play(FadeIn(nm), run_time=0.3)
        self.at("changes little")
        u = pulse_label("unchanged", GREY, -3.9, -0.45)
        self.play(FadeIn(u, shift=UP * 0.1), Indicate(sil[0], color=TEXT, scale_factor=1.0), run_time=0.8)
        self.finish()


class S20c(SpokenScene):
    def construct(self):
        cell = mk_cell()
        act = mk_fibre(TEXT, 1.7, w=8, ang=28)
        sil = mk_fibre(TEXT, -1.5, w=8, ang=-28)
        m, cap = meter(0.5), meter_cap()
        cl = cell_lab(cell)
        self.add(cell, act, sil, cl, m, cap)
        rowy = -2.55
        row = Line(pos(-5.3, rowy), pos(0.7, rowy), stroke_color=GREY, stroke_width=2, stroke_opacity=0.6)
        rl = T("cell activity", 26, GREY).move_to(pos(-4.3, rowy + 0.55))
        self.at("the line between")
        self.play(Indicate(m[3], scale_factor=1.0, color=GOLD), Indicate(m[0], scale_factor=1.0, color=GREEN),
                  Indicate(m[1], scale_factor=1.0, color=RED), run_time=0.8)
        busy = VGroup(*[tick(-5.1 + 0.45 * k, rowy, TEXT, h=0.3, w=6) for k in range(14)])
        bl = T("busy spell: cell fires a lot", 30, TEXT).move_to(pos(-2.3, rowy - 0.75))
        self.play(FadeIn(row), FadeIn(rl), LaggedStart(*[FadeIn(t) for t in busy], lag_ratio=0.08), FadeIn(bl), run_time=1.0)
        self.at("slides")
        up = Arrow(pos(2.6, 0.5), pos(2.6, 1.8), buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        self.play(Transform(m, meter(1.8)), Create(up), run_time=0.9)
        self.at("recent activity")
        quiet = VGroup(*[tick(-4.2 + 3.6 * k, rowy, TEXT, h=0.3, w=6) for k in range(2)])
        ql = T("quiet spell: cell fires little", 30, TEXT).move_to(pos(-2.3, rowy - 0.75))
        self.play(FadeOut(busy), FadeOut(bl), FadeOut(up), run_time=0.3)
        self.play(FadeIn(quiet), FadeIn(ql), run_time=0.4)
        dn = Arrow(pos(2.6, 1.8), pos(2.6, -0.6), buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        self.play(Transform(m, meter(-0.6)), Create(dn), run_time=1.0)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        cell = mk_cell()
        act = mk_fibre(TEXT, 1.7, w=8, ang=28)
        sil = mk_fibre(TEXT, -1.5, w=8, ang=-28)
        m, cap, w = meter(0.5), meter_cap(), wire()
        lv = level(0.0, col=GREEN)      # strong colour from the start: coincident volleys never flash red
        cl = cell_lab(cell)
        self.add(cell, act, sil, cl)
        eO, eB = small_eye(ORANGE, 1.7), small_eye(BLUE, -1.5)
        self.play(*recolor(act, ORANGE), *recolor(sil, BLUE), FadeIn(eO), FadeIn(eB),
                  FadeIn(m), FadeIn(cap), FadeIn(w), FadeIn(lv), run_time=0.9)
        self.at("arrive together")
        fire(self, [act, sil], run=0.4, col=[ORANGE, BLUE])
        self.play(glow(cell, LIT), Transform(lv, level(STRONG_H, col=GREEN)), run_time=0.12)
        self.wait(0.5)
        self.play(glow(cell, DIM), Transform(lv, level(0.0, col=GREEN)), run_time=0.3)
        self.at("responds strongly")
        fire(self, [act, sil], run=0.4, col=[ORANGE, BLUE])
        self.play(glow(cell, LIT), Transform(lv, level(STRONG_H, col=GREEN)), run_time=0.12)
        self.at("both are kept")
        kO = T("kept", 30, GREEN).move_to(pos(-3.4, 2.35))
        kB = T("kept", 30, GREEN).move_to(pos(-3.4, -2.2))
        self.play(FadeIn(kO, shift=UP * 0.1), FadeIn(kB, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        cell = mk_cell(op=LIT)
        act = mk_fibre(ORANGE, 1.7, w=8, ang=28)
        sil = mk_fibre(BLUE, -1.5, w=8, ang=-28)
        m, cap, w = meter(0.5), meter_cap(), wire()
        lv = level(STRONG_H)
        eO, eB = small_eye(ORANGE, 1.7), small_eye(BLUE, -1.5)
        kO = T("kept", 30, GREEN).move_to(pos(-3.4, 2.35))
        kB = T("kept", 30, GREEN).move_to(pos(-3.4, -2.2))
        cl = cell_lab(cell)
        self.add(cell, act, sil, m, cap, w, lv, eO, eB, kO, kB, cl)
        self.at("out of step")
        self.play(FadeOut(VGroup(m, cap, w, lv, kO, kB)), glow(cell, DIM), run_time=0.7)
        self.at("eye's input")
        fire(self, [act], run=0.4, col=ORANGE)
        self.play(glow(cell, WEAKLIT), run_time=0.12)
        self.play(glow(cell, DIM), run_time=0.15)
        self.at("often arrives")
        fire(self, [sil], run=0.4, col=BLUE)
        self.play(glow(cell, WEAKLIT), run_time=0.12)
        self.play(glow(cell, DIM), run_time=0.15)
        self.at("alone")
        fire(self, [act], run=0.4, col=ORANGE)
        self.play(glow(cell, WEAKLIT), run_time=0.12)
        self.play(glow(cell, DIM), run_time=0.15)
        fire(self, [sil], run=0.4, col=BLUE)
        self.play(glow(cell, WEAKLIT), run_time=0.12)
        self.play(glow(cell, DIM), run_time=0.15)
        self.at("one eye starts")
        self.play(*to_w(act, 14), run_time=0.9)
        st = T("starts slightly stronger", 28, GOLD).move_to(pos(-3.0, 2.95))
        ptr = Arrow(pos(-3.4, 2.65), pos(-3.4, 1.85), buff=0.05, color=GOLD, stroke_width=4, tip_length=0.2)
        self.at("slightly stronger")
        self.play(FadeIn(st, shift=UP * 0.1), Create(ptr), Indicate(act[0], scale_factor=1.0, color=GOLD), run_time=0.8)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        cell = mk_cell()
        act = mk_fibre(ORANGE, 1.7, w=14, ang=28)
        sil = mk_fibre(BLUE, -1.5, w=8, ang=-28)
        eO, eB = small_eye(ORANGE, 1.7), small_eye(BLUE, -1.5)
        st = T("starts slightly stronger", 28, GOLD).move_to(pos(-3.0, 2.95))
        cl = cell_lab(cell)
        self.add(cell, act, sil, eO, eB, st, cl)
        m, cap, w = meter(0.5), meter_cap(), wire()
        lv = level(0.0)
        self.play(FadeIn(m), FadeIn(cap), FadeIn(w), FadeIn(lv), FadeOut(st), run_time=0.6)
        self.at("it drives")
        fire(self, [act], run=0.45, col=ORANGE)
        self.play(glow(cell, LIT), Transform(lv, level(STRONG_H)), run_time=0.45)
        self.at("and is strengthened")
        sg = T("strengthened", 30, GREEN).move_to(pos(-3.4, 0.85))
        self.play(*to_w(act, 17), FadeIn(sg, shift=UP * 0.1), run_time=0.8)
        self.at("alone the other")
        self.play(FadeOut(sg), glow(cell, DIM), Transform(lv, level(0.0)), run_time=0.5)
        self.at("drives only a weak")
        fire(self, [sil], run=0.45, col=BLUE)
        self.play(glow(cell, WEAKLIT), Transform(lv, level(WEAK_H)), run_time=0.4)
        self.at("and is weakened")
        wd = T("weakened", 30, RED).move_to(pos(-3.4, -0.45))
        self.play(*to_w(sil, 4), FadeIn(wd, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S23b(SpokenScene):
    def construct(self):
        r = 1.2
        C1, C2 = pos(0.9, 1.65), pos(0.9, -1.65)
        # carried: the cell from the last scene (the moment it is split into two neighbouring cells)
        cell = mk_cell()
        act = mk_fibre(ORANGE, 1.7, w=17, ang=28)
        sil = mk_fibre(BLUE, -1.5, w=4, ang=-28)
        eO, eB = small_eye(ORANGE, 1.7), small_eye(BLUE, -1.5)
        cl = cell_lab(cell)
        self.add(cell, act, sil, eO, eB, cl)
        cell1 = mk_cell(C1, r, PURPLE, DIM)
        o1 = mk_fibre(ORANGE, 2.4, C1, r, 10.5, x0=-5.0, ang=28)
        b1 = mk_fibre(BLUE, 0.9, C1, r, 8, x0=-5.0, ang=-28)
        eO1, eB1 = small_eye(ORANGE, 2.4, -5.8), small_eye(BLUE, 0.9, -5.8)
        cl1 = cell_lab(cell1, 26)
        cell2 = mk_cell(C2, r, PURPLE, DIM)
        o2 = mk_fibre(ORANGE, -0.9, C2, r, 8, x0=-5.0, ang=28)
        b2 = mk_fibre(BLUE, -2.4, C2, r, 10.5, x0=-5.0, ang=-28)
        eO2, eB2 = small_eye(ORANGE, -0.9, -5.8), small_eye(BLUE, -2.4, -5.8)
        cl2 = cell_lab(cell2, 26)
        self.remove(cl)
        self.play(ReplacementTransform(cell, cell1), ReplacementTransform(act, o1), ReplacementTransform(sil, b1),
                  ReplacementTransform(eO, eO1), ReplacementTransform(eB, eB1), FadeOut(cl),
                  FadeIn(VGroup(cell2, o2, b2, eO2, eB2)), run_time=0.4)
        self.add(cl1, cl2)
        tgl = T("in a model with a sliding threshold", 30, GOLD).move_to(pos(0, -3.45))
        self.add(tgl)
        self.at("lead grows")
        self.play(*to_w(o1, 16), *to_w(b1, 3.5), run_time=1.2)
        self.at("answers mainly")
        m1 = T("mostly right eye", 28, ORANGE).move_to(pos(4.6, 1.65))
        self.play(cell1.animate.set_stroke(ORANGE).set_fill(ORANGE, WEAKLIT), FadeIn(m1, shift=LEFT * 0.15), run_time=1.0)
        self.at("which eye leads")
        self.play(*to_w(o2, 3.5), *to_w(b2, 16), run_time=1.2)
        self.at("from cell to cell")
        m2 = T("mostly left eye", 28, BLUE).move_to(pos(4.6, -1.65))
        self.play(cell2.animate.set_stroke(BLUE).set_fill(BLUE, WEAKLIT), FadeIn(m2, shift=LEFT * 0.15), run_time=1.0)
        self.finish()


def membrane(col=GREY):
    L = Rectangle(width=4.7, height=1.0, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to(pos(-3.95, 0))
    R = Rectangle(width=4.7, height=1.0, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35).move_to(pos(3.95, 0))
    return VGroup(L, R)


def receptor():
    a = RoundedRectangle(corner_radius=0.15, width=1.1, height=3.6, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.3).move_to(pos(-1.05, 0))
    b = RoundedRectangle(corner_radius=0.15, width=1.1, height=3.6, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.3).move_to(pos(1.05, 0))
    return VGroup(a, b)


class S24(SpokenScene):
    def construct(self):
        mem = membrane()
        out = tag("outside", GREY, -5.3, 1.0)
        ins = tag("inside the cell", GREY, -4.6, -1.0)
        brg = T("in the shared cell's membrane", 28, TEXT).move_to(pos(0, 2.55))
        self.play(FadeIn(mem), FadeIn(out), FadeIn(ins), FadeIn(brg), run_time=0.9)
        self.at("candidate")
        cand = T("a candidate", 44, GOLD, font=TITLE_FONT).move_to(pos(0, 3.3))
        self.play(FadeIn(cand, shift=DOWN * 0.1), run_time=0.5)
        self.at("detecting together")
        rec = receptor()
        self.play(FadeIn(rec, scale=0.9), run_time=0.9)
        self.at("receptor")
        nm = T("NMDA receptor", 40, TEAL, font=TITLE_FONT).move_to(pos(0, -2.75))
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        mem = membrane()
        out = tag("outside", GREY, -5.3, 1.0)
        ins = tag("inside the cell", GREY, -4.6, -1.0)
        rec = receptor()
        nm = T("NMDA receptor", 36, TEAL, font=TITLE_FONT).move_to(pos(0, -2.75))
        self.add(mem, out, ins, rec, nm)
        mg = VGroup(Circle(radius=0.4, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25),
                    T("Mg", 26, TEXT)).move_to(pos(0, 0.1))
        self.play(FadeIn(mg, scale=1.2), run_time=0.4)
        self.at("much current")
        ghost = DashedLine(pos(0, -0.5), pos(0, -1.7), color=GREY, stroke_width=6, dash_length=0.18)
        gl = T("current?", 28, GREY).move_to(pos(3.4, -1.1))
        self.play(Create(ghost), FadeIn(gl), run_time=0.7)
        self.at("glutamate")
        glu = chip("glutamate", YELLOW, size=26).move_to(pos(-4.8, 2.9))
        self.add(glu)
        self.play(glu.animate.move_to(pos(-3.0, 2.9)), run_time=0.3)
        ga = Arrow(pos(-1.7, 2.75), pos(-1.15, 1.85), buff=0.02, color=YELLOW, stroke_width=4, tip_length=0.2)
        self.play(Create(ga), run_time=0.2)
        self.at("and a")
        co = chip("co-agonist", PINK, size=26).move_to(pos(4.9, 2.9))
        self.add(co)
        self.play(co.animate.move_to(pos(3.1, 2.9)), run_time=0.5)
        ca = Arrow(pos(1.6, 2.75), pos(1.15, 1.85), buff=0.02, color=PINK, stroke_width=4, tip_length=0.2)
        self.play(Create(ca), run_time=0.3)
        self.at("bound")
        self.play(Flash(ga.get_end(), color=YELLOW, flash_radius=0.5), Flash(ca.get_end(), color=PINK, flash_radius=0.5), run_time=0.6)
        self.at("depolarized")
        dep = T("cell depolarized", 30, GOLD).move_to(pos(-4.3, -2.2))
        mgl = T("Mg = magnesium", 28, TEXT).move_to(pos(0, 3.5))
        mga = Arrow(pos(0, 3.2), pos(0, 0.55), buff=0.0, color=TEXT, stroke_width=3, tip_length=0.2)
        self.play(mem.animate.set_color(GOLD), FadeIn(dep, shift=UP * 0.1), FadeIn(mgl), Create(mga), run_time=0.8)
        self.at("clear")
        # magnesium leaves the pore, and a clear current runs through it for the rest of the scene
        pore = Rectangle(width=1.0, height=3.6, stroke_width=0, fill_color=TEXT, fill_opacity=0.0).move_to(pos(0, 0))
        pore.set_z_index(-1)
        self.add(pore)
        flow = Arrow(pos(0, 1.75), pos(0, -1.75), buff=0, color=TEXT, stroke_width=16, tip_length=0.35)
        cur = T("current flows", 40, TEXT, weight=BOLD).move_to(pos(4.35, -1.1))
        self.play(FadeOut(mga), FadeOut(ghost), FadeOut(gl), run_time=0.2)
        self.play(mg.animate.move_to(pos(0, 2.55)), pore.animate.set_fill(opacity=0.3), run_time=0.5)
        self.play(Create(flow), FadeIn(cur, shift=UP * 0.1), run_time=0.4)
        for _ in range(3):
            ions = [Dot(pos(0.0 + dx, 1.5), radius=0.1, color=TEXT) for dx in (-0.3, 0.0, 0.3)]
            self.add(*ions)
            self.play(*[d.animate.move_to(pos(d.get_center()[0], -1.5)) for d in ions], run_time=0.5, rate_func=linear)
            self.remove(*ions)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        def mini(cx, w):
            C = pos(cx, 1.55)
            cell = mk_cell(C, 1.1)
            return cell, mk_fibre(TEXT, 1.55, C, 1.1, w, x0=cx - 3.4, ang=0)
        cL, iL = mini(-2.6, 8)
        cR, iR = mini(4.0, 8)
        clL, clR = cell_lab(cL, 28), cell_lab(cR, 28)
        hl = VGroup(T("strong response:", 28, GREEN), T("strengthen", 40, GREEN, weight=BOLD)).arrange(DOWN, buff=0.12).move_to(pos(-3.75, -0.3))
        hr = VGroup(T("weak response:", 28, RED), T("weaken", 40, RED, weight=BOLD)).arrange(DOWN, buff=0.12).move_to(pos(2.85, -0.3))
        hdr = T("both halves of the rule", 38, GOLD, font=TITLE_FONT).move_to(pos(0, -2.5))
        self.at("both halves")
        self.play(FadeIn(VGroup(cL, iL, cR, iR, clL, clR)), FadeIn(hdr), run_time=0.35)
        fire(self, [iL], run=0.25)
        self.play(glow(cL, LIT), *to_w(iL, 15), *recolor(iL, GREEN), FadeIn(hl, shift=UP * 0.1), run_time=0.45)
        fire(self, [iR], run=0.25)
        self.play(glow(cR, WEAKLIT), *to_w(iR, 3), *recolor(iR, RED), FadeIn(hr, shift=UP * 0.1), run_time=0.45)
        self.at("the cell keeps")
        l1 = T("The cell keeps the eye", 54, TEXT, font=TITLE_FONT).move_to(pos(0, -2.1))
        l2 = T("that helps it fire.", 54, GOLD, font=TITLE_FONT).move_to(pos(0, -3.1))
        self.play(FadeOut(hdr), Write(l1), run_time=0.9)
        self.play(Write(l2), run_time=0.9)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        ys = [0.75, -0.65, -2.05]
        x0, x1 = -3.9, 5.9
        rowc = row_line(x0, x1 - x0, ys[0], TEXT)
        rowo = row_line(x0, x1 - x0, ys[1], ORANGE)
        rowb = row_line(x0, x1 - x0, ys[2], BLUE)
        lc = T("cell", 26, TEXT).move_to(pos(-6.3, ys[0])).align_to(pos(-6.3, 0), LEFT)
        lo = T("right eye", 26, ORANGE).move_to(pos(-6.3, ys[1])).align_to(pos(-6.3, 0), LEFT)
        lb = T("left eye", 26, BLUE).move_to(pos(-6.3, ys[2])).align_to(pos(-6.3, 0), LEFT)
        tc = [-3.3, -1.9, -0.4, 1.1, 2.8, 4.5]
        tbl = [-2.6, -1.1, 0.5, 2.0, 3.7, 5.4]
        cellt = VGroup(*[tick(x, ys[0], TEXT, h=0.32, w=6) for x in tc])
        ot = [tick(x, ys[1], ORANGE, h=0.32, w=6) for x in tc]
        bt = [tick(x, ys[2], BLUE, h=0.32, w=6) for x in tbl]
        tg = T("Takeaway", 28, GOLD).move_to(pos(-5.4, 3.5))
        self.add(tg, rowc, rowo, rowb, lc, lo, lb)
        # spikes begin with the first words: both eyes send the same number
        self.play(LaggedStart(*[FadeIn(t, scale=1.5) for t in ot[:3] + bt[:3]], lag_ratio=0.15), run_time=0.8)
        self.at("amount matters")
        p1 = T("Amount matters,", 38, TEXT, font=TITLE_FONT)
        p2 = T("but only activity in step", 38, GOLD, font=TITLE_FONT)
        l1 = VGroup(p1, p2).arrange(RIGHT, buff=0.25).move_to(pos(0, 2.85))
        self.play(Write(p1), LaggedStart(*[FadeIn(t, scale=1.5) for t in ot[3:] + bt[3:]], lag_ratio=0.15), run_time=1.0)
        self.at("but only")
        self.play(Write(p2), run_time=0.8)
        self.at("in step")
        guides = VGroup(*[dashed_v(x, ys[0] + 0.45, ys[1] - 0.45) for x in tc])
        self.play(FadeIn(cellt), Create(guides), run_time=0.6)
        self.at("with the")
        l2 = T("with the cell's firing helps an eye keep it.", 38, TEXT, font=TITLE_FONT).move_to(pos(0, 1.95))
        self.play(Write(l2), run_time=1.0)
        self.at("helps an eye")
        ring = RoundedRectangle(corner_radius=0.2, width=x1 - x0 + 0.6, height=0.9, stroke_color=GREEN, stroke_width=4).move_to(pos((x0 + x1) / 2, ys[1]))
        self.play(Create(ring), run_time=0.7)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        hd = T("a sharper test", 44, GOLD, font=TITLE_FONT).move_to(pos(0, 3.2))
        yS, yN = 1.1, -1.5
        eS = eye_icon(BLUE, 1.3, dim=True).move_to(pos(-5.0, yS))
        flat = Line(pos(-3.4, yS), pos(6.2, yS), stroke_color=BLUE, stroke_width=3, stroke_opacity=0.5)
        eN = eye_icon(ORANGE, 1.3).move_to(pos(-5.0, yN))
        rowN = Line(pos(-3.4, yN), pos(6.2, yN), stroke_color=ORANGE, stroke_width=3, stroke_opacity=0.5)
        # title, then both eyes straight away (the title is held for well under a second)
        self.play(FadeIn(hd, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(eS), Create(flat), FadeIn(eN), Create(rowN), run_time=0.6)
        self.at("an eye that is silent")
        ls = T("silent", 36, BLUE).move_to(pos(-5.0, yS - 1.1))
        self.play(FadeIn(ls), Flash(eS, color=BLUE, flash_radius=1.0), run_time=0.6)
        self.at("an eye that is noisy")
        ln = T("noisy", 36, ORANGE).move_to(pos(-5.0, yN - 1.1))
        xs = np.sort(RNG.uniform(-3.2, 6.0, 26))
        ticks = VGroup(*[tick(x, yN + RNG.uniform(-0.15, 0.15), ORANGE, h=RNG.uniform(0.2, 0.45)) for x in xs])
        self.play(FadeIn(ln), Flash(eN, color=ORANGE, flash_radius=1.0), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, scale=1.4) for t in ticks], lag_ratio=0.05), run_time=1.6)
        self.finish()


class S29End(EndCard):
    LINE = "Activity in step with the cell's firing helps an eye keep it."
