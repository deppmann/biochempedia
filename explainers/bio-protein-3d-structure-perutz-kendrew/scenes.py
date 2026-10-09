"""Max Perutz & John Kendrew: scientist profile video (Biochemistrypedia, protein-3d-structure lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry (name,
dates, contribution, story, quotes). The portrait (public/scientists/perutz-kendrew.png, an AI-generated
engraving-style illustration from The Molecule Hunters) is cropped to the two figures (pk_crop.png) and
captioned "illustration · AI-generated" whenever it is on screen at a readable size. Left face = Perutz,
right face = Kendrew (the order of the names in the entry); a half-frame veil highlights whoever the
narration is about.

COLOR MAP (one color per concept, whole video)
  GOLD    = time: dates, the 22 years, the Nobel, the portrait frame, "the sausage model"
  BLUE    = hemoglobin (Perutz's one molecule)
  PURPLE  = myoglobin (Kendrew's first run)
  YELLOW  = method and tools: crystals, mercury and silver, the sheets of clear plastic
  TEAL    = the electron density: contours, the rod that rose out of the sheets, missing information
  RED     = what went wrong or was unexpected: no computer screen, no symmetry, surprise, "a mess"
  GREEN   = "exactly right"
  GREY    = axes, the ceiling, de-emphasized things
No molecular structure is drawn: the density is a stack of contour sheets computed from a smooth
function (contours.json, from gen_contours.py), and the "rod" is a plain thick path through them.
"""
import json
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

HERE = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
IMG = HERE / "pk_crop.png"
DATA = json.loads((HERE / "contours.json").read_text())
CAPTION = "illustration · AI-generated"
NAME = "Max Perutz & John Kendrew"
DATES = "1914–2002 · 1917–1997"
PURPLE = "#B39DDB"

# portrait inset (left column) and content area (x from -1.7 to 6.2)
PORT_X, PORT_Y, PORT_H = -4.2, 1.0, 2.5
CROP_AR = 1205 / 755.0
SPLIT = 0.53                      # x fraction where the left face ends and the right face begins
FACE_L, FACE_R = 0.26, 0.70       # x fraction of each face centre
DIM = 0.62
CX = 2.25

# oblique projection of the contour stack: (x, y, z) in the unit cube -> screen
BASE = np.array([2.4, -2.75, 0.0])
EX, EY, EZ = np.array([2.9, 0, 0]), np.array([0.9, 0.5, 0]), np.array([0, 4.4, 0])


def proj(x, y, z):
    return BASE + x * EX + y * EY + z * EZ


# ----------------------------------------------------------------------------- portrait helpers
def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height).move_to([center[0], center[1], 0]).set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def veils(focus="both"):
    """Two half-frame veils over the portrait: left = Perutz, right = Kendrew."""
    w = PORT_H * CROP_AR
    x0 = PORT_X - w / 2

    def mk(a, b, op):
        r = Rectangle(width=(b - a) * w, height=PORT_H, stroke_width=0, fill_color=BG, fill_opacity=op)
        return r.move_to([x0 + (a + b) / 2 * w, PORT_Y, 0]).set_z_index(2)

    return mk(0, SPLIT, DIM if focus == "right" else 0), mk(SPLIT, 1, DIM if focus == "left" else 0)


def column_labels(focus="both"):
    w = PORT_H * CROP_AR
    x0 = PORT_X - w / 2
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY, font=TITLE_FONT).move_to([PORT_X, y - 0.32, 0])
    nl = VGroup(T("Max", 24, TEXT, font=TITLE_FONT), T("Perutz", 24, TEXT, font=TITLE_FONT),
                T("1914–2002", 22, GOLD)).arrange(DOWN, buff=0.08)
    nr = VGroup(T("John", 24, TEXT, font=TITLE_FONT), T("Kendrew", 24, TEXT, font=TITLE_FONT),
                T("1917–1997", 22, GOLD)).arrange(DOWN, buff=0.08)
    nl.move_to([x0 + FACE_L * w, y - 1.3, 0])
    nr.move_to([x0 + FACE_R * w, y - 1.3, 0])
    nl.set_opacity(0.4 if focus == "right" else 1)
    nr.set_opacity(0.4 if focus == "left" else 1)
    return cap, nl, nr


def focus_anims(plate, which):
    dl, dr, nl, nr = plate
    return [dl.animate.set_fill(BG, opacity=DIM if which == "right" else 0),
            dr.animate.set_fill(BG, opacity=DIM if which == "left" else 0),
            nl.animate.set_opacity(0.4 if which == "right" else 1),
            nr.animate.set_opacity(0.4 if which == "left" else 1)]


# ----------------------------------------------------------------------------- shared pieces
def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def cross(center, r=0.28, color=RED, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color).set_stroke(width=w) \
        .move_to(center)


def poly(pts, **kw):
    m = VMobject(**kw)
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    return m


def make_sheet(k):
    """Sheet k of the stack: a clear-plastic parallelogram plus its contour lines (outer, middle, inner)."""
    s = DATA["sheets"][k]
    z = s["z"]
    plate = Polygon(proj(0, 0, z), proj(1, 0, z), proj(1, 1, z), proj(0, 1, z), stroke_color=YELLOW,
                    stroke_width=2, fill_color=BG, fill_opacity=0.5)
    plate.set_stroke(opacity=0.8)
    cols = {1.2: ("#2C8A91", 3.0), 3.5: (TEAL, 3.0), 6.5: ("#B8F0F2", 3.0)}
    lines = VGroup()
    for ln in s["lines"]:
        pts = [proj(x, y, z) for x, y in ln["pts"]]
        c, wd = cols[ln["lev"]]
        lines.add(poly(pts, stroke_color=c, stroke_width=wd, stroke_opacity=1.0))
    g = VGroup(plate, lines)
    g.set_z_index(10 + k)
    return plate, lines, g


def rod_group(color=TEAL):
    """The 'fat, irregular rod doubling back on itself': a plain thick path through the density centres."""
    pts = [proj(*p) for p in DATA["path"]]
    mk = lambda w, c, op: VMobject(stroke_color=c, stroke_width=w, stroke_opacity=op, fill_opacity=0,
                                   cap_style=CapStyleType.ROUND, joint_type=LineJointType.ROUND)
    outer = mk(40, color, 1.0).set_points_smoothly(pts)
    mid = mk(31, color, 1.0).set_points_smoothly(pts)
    core = mk(9, WHITE, 0.30).set_points_smoothly(pts)
    outer.set_color(interpolate_color(ManimColor(color), ManimColor(BG), 0.5))
    mid.set_color(color)
    rod = VGroup(outer, mid, core)
    rod.set_z_index(30)
    return rod


def rod_recolor(rod, color):
    return [rod[0].animate.set_color(interpolate_color(ManimColor(color), ManimColor(BG), 0.5)),
            rod[1].animate.set_color(color)]


class ProfileScene(SpokenScene):
    def add_column(self, focus="both"):
        img, border = portrait()
        cap, nl, nr = column_labels(focus)
        dl, dr = veils(focus)
        self.add(img, border, dl, dr, cap, nl, nr)
        self.plate = (dl, dr, nl, nr)

    def focus(self, which):
        return focus_anims(self.plate, which)


# ----------------------------------------------------------------------------- s00 title
class S00Title(ProfileScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 3.7
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.85, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).move_to([0, 0.85 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        fit(name, max_w=11.5)
        name.move_to([0, -2.1, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.55, 0])
        dates = T(DATES, 30, GOLD).move_to([0, -3.05, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        cap2, nl, nr = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(nl), FadeIn(nr))),
            run_time=0.8))
        self.finish()


# ----------------------------------------------------------------------------- s01 Max, hemoglobin since 1937
class S01Max(ProfileScene):
    def construct(self):
        self.add_column("left")
        q = T("“Please call me Max”", 44, TEXT, font=TITLE_FONT).move_to([CX, 2.3, 0])
        self.play(Write(q), run_time=1.2)

        young = lab("almost every young scientist", TEXT, 28).move_to([CX, 0.7, 0])
        self.at("almost every young scientist")
        self.play(pop(young), run_time=0.5)
        to_him = Arrow(young.get_left() + LEFT * 0.08, [-1.9, 0.7, 0], color=GOLD, stroke_width=4, buff=0,
                       max_tip_length_to_length_ratio=0.35)
        self.at("came to him")
        self.play(GrowArrow(to_him), run_time=0.5)

        # the model of hemoglobin hanging from the ceiling
        self.at("He had a model")
        self.play(FadeOut(VGroup(q, young, to_him)), run_time=0.4)
        ceil_y = 3.05
        ceiling = Line([-1.6, ceil_y, 0], [2.6, ceil_y, 0], color=GREY, stroke_width=5)
        hatch = VGroup(*[Line([x, ceil_y, 0], [x - 0.18, ceil_y + 0.18, 0], color=GREY, stroke_width=2)
                         for x in np.arange(-1.4, 2.7, 0.3)])
        self.play(Create(ceiling), FadeIn(hatch), run_time=0.5)
        model = lab("hemoglobin model", BLUE, 28).move_to([0.5, 1.45, 0])
        string = Line([0.5, ceil_y, 0], model.get_top(), color=GREY, stroke_width=3)
        self.at("hemoglobin")
        self.play(Create(string), pop(model), run_time=0.6)
        ceil_lab = T("his office ceiling", 26, GREY).move_to([4.5, ceil_y, 0])
        self.at("office ceiling")
        self.play(FadeIn(ceil_lab, shift=UP * 0.1), run_time=0.4)

        one = T("the one molecule", 30, BLUE).next_to(model, RIGHT, buff=0.85)
        arr = Arrow(one.get_left() + LEFT * 0.1, model.get_right() + RIGHT * 0.1, color=BLUE, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.3)
        self.at("the one molecule")
        self.play(FadeIn(one, shift=LEFT * 0.1), GrowArrow(arr), run_time=0.6)

        # timeline: 1937 to the solution, 22 years
        ay = -1.6
        x37, x59 = -0.4, 4.6
        axis = Arrow([-1.6, ay, 0], [6.05, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d37 = Dot([x37, ay, 0], radius=0.13, color=GOLD)
        l37 = M("1937", 38, GOLD).move_to([x37, ay + 0.55, 0])
        self.at("since 1937")
        self.play(Create(axis), FadeIn(d37, scale=2), FadeIn(l37, shift=UP * 0.1), run_time=0.7)
        span = DoubleArrow([x37 + 0.15, ay - 0.65, 0], [x59 - 0.15, ay - 0.65, 0], color=GOLD, stroke_width=4, buff=0,
                           tip_length=0.18)
        yrs = T("twenty-two years", 30, GOLD).move_to([(x37 + x59) / 2, ay - 1.2, 0])
        self.at("twenty two years")
        self.play(GrowArrow(span), FadeIn(yrs, shift=UP * 0.1), run_time=0.8)
        d59 = Dot([x59, ay, 0], radius=0.13, color=GOLD)
        l59 = M("1959", 38, GOLD).move_to([x59, ay + 0.55, 0])
        solved = T("solved", 30, BLUE).next_to(l59, UP, buff=0.12)
        self.at("solved it")
        self.play(FadeIn(d59, scale=2), FadeIn(l59, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(solved, shift=UP * 0.1), Indicate(model, color=BLUE, scale_factor=1.06), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02 the heavy-metal trick
def beaker(label, liquid, x, y):
    w, h = 1.15, 1.3
    wall = poly([(x - w / 2, y + h / 2 + 0.1), (x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2 + 0.1)],
                stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
    fluid = Rectangle(width=w - 0.08, height=h * 0.62, stroke_width=0, fill_color=liquid, fill_opacity=0.75) \
        .move_to([x, y - h / 2 + h * 0.31 + 0.02, 0])
    name = T(label, 28, TEXT).move_to([x, y - h / 2 - 0.4, 0])
    return VGroup(fluid, wall), name, fluid


def diamond(color=YELLOW, r=0.2):
    return Polygon([0, r * 1.2, 0], [r, 0, 0], [0, -r * 1.2, 0], [-r, 0, 0], stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.55)


class S02Trick(ProfileScene):
    def construct(self):
        self.add_column("both")
        yb = 1.55
        crystals = lab("crystals", YELLOW, 30).move_to([-0.15, yb, 0])
        self.at("soak the crystals")
        self.play(pop(crystals), run_time=0.45)

        b1, n1, f1 = beaker("mercury", "#8FA3B0", 2.3, yb)
        b2, n2, f2 = beaker("silver", "#D0D4D8", 5.0, yb)
        d1, d2 = diamond().move_to(crystals), diamond().move_to(crystals)
        self.at("mercury")
        self.add(d1)
        self.play(FadeIn(b1), FadeIn(n1), d1.animate.move_to([2.3, yb + 1.0, 0]), run_time=0.5)
        self.play(d1.animate.move_to([2.3, yb - 0.3, 0]), run_time=0.35)
        self.at("silver")
        self.add(d2)
        self.play(FadeIn(b2), FadeIn(n2), d2.animate.move_to([5.0, yb + 1.0, 0]), run_time=0.4)
        self.play(d2.animate.move_to([5.0, yb - 0.3, 0]), run_time=0.25)

        # triangulate: three rays meet on the missing information
        c = np.array([2.3, -1.45, 0.0])
        srcs = [np.array([-0.15, yb - 0.55, 0.0]), np.array([2.3, yb - 1.0, 0.0]), np.array([5.0, yb - 1.0, 0.0])]
        rays = VGroup(*[DashedLine(s, c, color=TEAL, stroke_width=4, dash_length=0.14) for s in srcs])
        dot = Dot(c, radius=0.16, color=TEAL)
        ring = Circle(radius=0.34, color=TEAL, stroke_width=3).move_to(c)
        miss = T("missing information", 30, TEAL).move_to([2.3, -2.2, 0])
        self.at("triangulate")
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.3), run_time=0.7)
        self.play(FadeIn(dot, scale=2), Create(ring), run_time=0.3)
        self.at("missing information")
        self.play(FadeIn(miss, shift=UP * 0.1), run_time=0.5)

        # Kendrew ran it first, on myoglobin
        ran = T("Kendrew ran it first", 30, TEXT).move_to([-0.3, -3.0, 0])
        self.at("Kendrew ran it")
        self.play(*self.focus("right"), FadeIn(ran, shift=UP * 0.1), run_time=0.5)
        myo = lab("myoglobin", PURPLE, 30).move_to([3.9, -3.0, 0])
        arrow = Arrow(ran.get_right() + RIGHT * 0.12, myo.get_left() + LEFT * 0.12, color=PURPLE, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("myoglobin")
        self.play(GrowArrow(arrow), pop(myo), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 the contour sheets
class S03Sheets(ProfileScene):
    def construct(self):
        self.add_column("both")
        LX = -0.15  # centre of the left text column in the content area

        screen = VGroup(RoundedRectangle(corner_radius=0.1, width=2.5, height=1.55, stroke_color=GREY, stroke_width=4),
                        Line([-0.45, -0.78, 0], [-0.45, -1.0, 0], color=GREY, stroke_width=4),
                        Line([0.45, -0.78, 0], [0.45, -1.0, 0], color=GREY, stroke_width=4),
                        Line([-0.7, -1.0, 0], [0.7, -1.0, 0], color=GREY, stroke_width=5)).move_to([LX, 1.5, 0])
        scr_lab = T("computer screen", 28, GREY).move_to([LX, 0.2, 0])
        self.at("no computer screen")
        self.play(FadeIn(screen), FadeIn(scr_lab), run_time=0.5)
        x = cross([LX, 1.5, 0], r=0.5, w=10)
        self.at("screen")
        self.play(FadeIn(x, scale=1.4), run_time=0.3)
        yr = M("1958", 56, GOLD).move_to([LX, 2.8, 0])
        self.at("1958")
        self.play(Write(yr), run_time=0.6)
        self.play(Indicate(x, color=RED, scale_factor=1.1), run_time=0.7)

        # sheet 0, drawn by hand
        plates, lines, groups = [], [], []
        for k in range(len(DATA["sheets"])):
            p, l, g = make_sheet(k)
            plates.append(p); lines.append(l); groups.append(g)
        dens = lab("electron density", TEAL, 28).move_to([LX, 1.5, 0])
        self.at("the group drew")
        self.play(FadeOut(VGroup(screen, scr_lab, x)), FadeIn(plates[0]), run_time=0.5)
        self.at("electron density")
        self.play(pop(dens), Create(lines[0][0]), run_time=1.0)
        hand = lab("by hand", TEXT, 28).move_to([LX, 0.4, 0])
        self.at("by hand")
        self.play(pop(hand), Create(lines[0][1:]), run_time=0.9, lag_ratio=0.5)

        def reveal(ks, run):
            return LaggedStart(*[AnimationGroup(FadeIn(plates[k]), Create(lines[k], lag_ratio=0.3)) for k in ks],
                               lag_ratio=0.45, run_time=run)

        # stack them up
        self.at("stacked the contours")
        self.play(reveal(range(1, 7), 1.3))
        dozens = lab("dozens of sheets", YELLOW, 28).move_to([LX, -0.6, 0])
        self.at("dozens of sheets")
        self.play(pop(dozens), reveal(range(7, 11), 0.9))
        plastic = lab("clear plastic", YELLOW, 28).move_to([LX, -1.6, 0])
        self.at("clear plastic")
        self.play(pop(plastic), reveal(range(11, len(groups)), 0.9))

        # up into three dimensions
        up = Arrow(proj(-0.12, 0, 0.0) + LEFT * 0.0, proj(-0.12, 0, 1.0) + UP * 0.2, color=TEAL, stroke_width=6,
                   buff=0, max_tip_length_to_length_ratio=0.12).set_z_index(50)
        self.at("climbed up")
        self.play(GrowArrow(up), run_time=1.3)
        three = lab("three dimensions", TEAL, 28).move_to([LX, -2.7, 0])
        self.at("three dimensions")
        self.play(pop(three), Indicate(VGroup(*groups), color=TEAL, scale_factor=1.03), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s04 the sausage
class S04Sausage(ProfileScene):
    def construct(self):
        self.add_column("both")
        LX = 0.1
        sheets = VGroup(*[make_sheet(k)[2] for k in range(len(DATA["sheets"]))])
        sheets.set_opacity(0.3)
        up = Arrow(proj(-0.12, 0, 0.0), proj(-0.12, 0, 1.0) + UP * 0.2, color=TEAL, stroke_width=6, buff=0,
                   max_tip_length_to_length_ratio=0.12).set_z_index(50)
        up.set_opacity(0.3)
        self.add(sheets, up)
        self.wait(0.3)

        rod = rod_group()
        fat = lab(["a fat, irregular rod"], TEAL, 26).move_to([LX, 2.65, 0])
        self.at("fat, irregular rod")
        self.play(pop(fat), sheets.animate.set_opacity(0.14), FadeOut(up), run_time=0.5)
        self.play(Create(rod[0]), Create(rod[1]), Create(rod[2]), run_time=1.4)

        # doubling back
        pts = [proj(*p) for p in DATA["path"]]
        back = lab("doubling back", TEAL, 26).move_to([LX, 1.65, 0])
        self.at("doubling back")
        self.play(pop(back), ShowPassingFlash(rod[2].copy().set_stroke(color=WHITE, width=12, opacity=1.0), time_width=0.35,
                                              run_time=1.4), run_time=1.4)

        # no symmetry
        axis_x = float(np.mean([p[0] for p in pts]))
        mirror = DashedLine([axis_x, -2.9, 0], [axis_x, 2.6, 0], color=RED, stroke_width=3, dash_length=0.14).set_z_index(5)
        nosym = lab(["no symmetry"], RED, 26).move_to([LX, 0.65, 0])
        self.at("no symmetry")
        self.play(pop(nosym), Create(mirror), run_time=0.8)
        xm = cross([axis_x, 0.0, 0], r=0.3, w=9).set_z_index(61)
        self.at("predicted")
        self.play(FadeIn(xm, scale=1.4), run_time=0.4)

        # the sausage model
        self.at("The lab called")
        self.play(FadeOut(VGroup(fat, back, nosym, mirror, xm)), run_time=0.5)
        naus = T("“the sausage model”", 36, GOLD, font=TITLE_FONT)
        naus.move_to([LX, 1.9, 0])
        fit(naus, max_w=3.7)
        self.at("sausage model")
        self.play(FadeIn(naus, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(rod[1], color=GOLD, scale_factor=1.03), run_time=0.7)

        # Kendrew's reaction
        surprise = lab("only surprise", RED, 28).move_to([LX, 0.5, 0])
        self.at("Kendrew admitted")
        self.play(*self.focus("right"), run_time=0.5)
        self.at("surprise")
        self.play(pop(surprise), run_time=0.45)
        twists = T("“unexpected twists”", 34, RED, font=TITLE_FONT).move_to([LX, -0.65, 0])
        fit(twists, max_w=3.7)
        self.at("unexpected twists")
        self.play(FadeIn(twists, shift=UP * 0.1), Indicate(rod[1], color=RED, scale_factor=1.03), run_time=0.7)
        aes = lab(["not recommended on", "aesthetic grounds"], TEXT, 26).move_to([LX - 0.15, -2.0, 0])
        self.at("conceding")
        self.play(pop(aes), run_time=0.5)
        self.at("aesthetic grounds")
        self.play(aes[0].animate.set_stroke(RED).set_fill(RED, opacity=0.16), aes[1].animate.set_color(RED), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s05 a mess, exactly right, Nobel
class S05Right(ProfileScene):
    def construct(self):
        self.add_column("both")
        rod = rod_group()
        sheets = VGroup(*[make_sheet(k)[2] for k in range(len(DATA["sheets"]))])
        sheets.set_opacity(0.12)
        stage = Group(sheets, rod)
        stage.scale(0.62, about_point=BASE).shift(np.array([-4.55 + 0.7, 0.5, 0]) + (np.array([0, 0, 0])))
        self.add(stage)

        first = lab(["the first protein", "ever seen"], TEAL, 28).move_to([4.2, 2.35, 0])
        self.at("The first protein")
        self.play(pop(first), run_time=0.5)
        mess = lab("a mess", RED, 32).move_to([4.2, 1.1, 0])
        self.at("mess")
        self.play(pop(mess), *rod_recolor(rod, RED), Wiggle(rod[1], scale_value=1.0, rotation_angle=0.03 * TAU,
                                                              n_wiggles=4), run_time=0.9)
        right = lab("exactly right", GREEN, 32).move_to([4.2, -0.15, 0])
        self.at("exactly right")
        tick = VGroup(Line([-0.3, 0.0, 0], [-0.1, -0.25, 0]), Line([-0.1, -0.25, 0], [0.35, 0.3, 0])) \
            .set_color(GREEN).set_stroke(width=10).next_to(right, LEFT, buff=0.18)
        self.play(pop(right), *rod_recolor(rod, GREEN), Create(tick), run_time=0.9)

        self.at("The two men")
        self.play(*self.focus("both"), run_time=0.4)
        medal = VGroup(Circle(radius=0.62, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.2),
                       T("Nobel", 24, GOLD, weight=BOLD)).move_to([2.9, -1.95, 0])
        yr = M("1962", 56, GOLD).move_to([5.0, -1.95, 0])
        self.at("shared")
        self.play(GrowFromCenter(medal), run_time=0.5)
        self.at("1962")
        self.play(Write(yr), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_column("left")
        mark = T("“", 130, GOLD, font=TITLE_FONT)
        q = T("Please call me Max”", 52, TEXT, font=TITLE_FONT)
        fit(q, max_w=7.6)
        q.move_to([CX + 0.4, 0.5, 0])
        mark.scale(0.7).next_to(q, LEFT, buff=0.1).align_to(q, UP).shift(UP * 0.1)
        att = T("— Max Perutz", 34, GOLD).next_to(q, DOWN, buff=0.6).align_to(q, RIGHT)
        sub = VGroup(T("the first words he offered almost every", 26, GREY),
                     T("young scientist", 26, GREY)).arrange(DOWN, buff=0.12).next_to(att, DOWN, buff=0.45)
        sub.move_to([CX + 0.4, sub.get_center()[1], 0])
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.5)
        self.play(Write(q), run_time=1.5)
        self.wait(0.4)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(ProfileScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).move_to([0, 2.0 - 1.15 - 0.3, 0])
        a = T("Solved the first protein structures:", 42, font=TITLE_FONT)
        b = T("myoglobin 1958, hemoglobin 1959.", 42, font=TITLE_FONT)
        lg = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · combined Perutz & Kendrew profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
