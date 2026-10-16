"""Neurulation and neural tube defects: the folds must be able to meet  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the neural plate / neural tube / the cells of the plate
  ORANGE = skin (the epidermis beside and over the plate)
  YELLOW = movement and reach: the folds' motion, hinge, cells in the act of pushing in
  TEAL   = planar cell polarity / Dishevelled signaling (the sideways sense of direction)
  RED    = disrupted, too far apart, open, failed
  GREEN  = meets, fused, closed, normal
  GREY   = labels, outlines, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
OY = 0.9          # y of the skin line in the cross-section
HALF = 6.2        # half-length of the skin line


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def sec(a, d, half=HALF, oy=OY, sc=1.0, cx=0.0):
    """Cross-section of the embryo's back. Skin (orange) either side; the plate (blue) is a groove
    whose edges (the fold tips) sit at x = +-a on the skin line and whose floor is d below it."""
    a = max(a, 0.02)
    plate = ParametricFunction(lambda p: np.array([a * np.cos(p), -d * np.sin(p), 0]),
                               t_range=[0, PI, PI / 60], color=BLUE, stroke_width=20)
    sl = Line([-half, 0, 0], [-a, 0, 0], color=ORANGE, stroke_width=9)
    sr = Line([a, 0, 0], [half, 0, 0], color=ORANGE, stroke_width=9)
    g = VGroup(sl, sr, plate)
    g.scale(sc, about_point=ORIGIN).shift([cx, oy, 0])
    return g


def tube(r=1.6, drop=0.0, half=HALF, oy=OY, sc=1.0, cx=0.0):
    """Closed tube: skin continuous over the top; tube a circle, drop below the skin (a gap if drop > 0)."""
    plate = ParametricFunction(lambda p: np.array([r * np.sin(p), -r - drop + r * np.cos(p), 0]),
                               t_range=[0, TAU, TAU / 80], color=BLUE, stroke_width=20)
    sl = Line([-half, 0, 0], [0, 0, 0], color=ORANGE, stroke_width=9)
    sr = Line([0, 0, 0], [half, 0, 0], color=ORANGE, stroke_width=9)
    g = VGroup(sl, sr, plate)
    g.scale(sc, about_point=ORIGIN).shift([cx, oy, 0])
    return g


def lab(text, color=TEXT, size=30, **kw):
    return T(text, size, color, **kw)


def darr(p, q, color=GREY, w=4):
    return DoubleArrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.22,
                       max_tip_length_to_length_ratio=0.3)


def parr(p, q, color=YELLOW, w=6):
    return Arrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.4)


def flash(self, pt, color=GREEN, r=0.5):
    ring = Circle(radius=0.12, color=color, stroke_width=6).move_to(pt)
    self.play(ring.animate.scale(r / 0.12).set_stroke(opacity=0), run_time=0.6)
    self.remove(ring)


class S00Title(TitleCard):
    LESSON = "Neurulation and neural tube defects"
    TITLE = "The folds must be able to meet"


# ---------------------------------------------------------------------------------------------
class S01Flat(SpokenScene):
    """flat sheet -> closed tube -> open groove with a question mark between the edges."""

    def construct(self):
        s = sec(2.8, 0)
        skin = lab("skin", ORANGE, 28).move_to([5.0, OY - 0.5, 0])
        self.play(FadeIn(s), FadeIn(skin), run_time=0.8)
        self.at("flat sheet")
        sheet = lab("a flat sheet of cells", BLUE, 32).move_to([0, OY + 0.9, 0])
        back = lab("back of the embryo", GREY, 26).move_to([0, OY + 1.7, 0])
        self.play(FadeIn(sheet, shift=DOWN * 0.1), FadeIn(back), run_time=0.6)
        self.at("fourth week")
        clock = chip("about 4 weeks after fertilization", GOLD, 28).move_to([0, -3.1, 0])
        self.play(FadeIn(clock, shift=UP * 0.1), run_time=0.6)
        self.at("rolled into a closed tube")
        closed = lab("a closed tube", GREEN, 32).move_to([0, OY + 0.9, 0])
        self.play(Transform(s, sec(1.5, 1.6)), run_time=0.7)
        self.play(Transform(s, sec(0.03, 3.2)), run_time=0.7)
        self.play(Transform(s, tube(1.6)), ReplacementTransform(sheet, closed), run_time=0.8)
        self.at("pregnant")
        self.wait(0.2)
        self.at("does not close")
        openl = lab("not closed", RED, 32).move_to([0, OY + 0.9, 0])
        self.play(Transform(s, sec(1.6, 2.6)), ReplacementTransform(closed, openl), run_time=1.0)
        self.at("How far apart")
        gap = darr([-1.35, OY - 0.55, 0], [1.35, OY - 0.55, 0], RED, 5)
        q = lab("?", RED, 72).move_to([0, OY - 1.6, 0])
        self.play(GrowFromCenter(gap), FadeIn(q), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fold(SpokenScene):
    """plate creases at a hinge, the folds rise and move in, fuse, the tube pinches off beneath the skin."""

    def construct(self):
        s = sec(2.8, 0)
        skin = lab("skin", ORANGE, 28).move_to([5.0, OY - 0.5, 0])
        self.add(s)
        self.at("neural plate")
        plate_l = lab("neural plate", BLUE, 34).move_to([0, OY + 1.0, 0])
        self.play(FadeIn(plate_l, shift=DOWN * 0.1), run_time=0.5)
        self.at("hinge points")
        self.play(Transform(s, sec(2.5, 1.0)), run_time=0.9)
        wedge = Polygon([-0.0, OY - 1.0 + 0.1, 0], [-0.32, OY - 1.0 - 0.5, 0], [0.32, OY - 1.0 - 0.5, 0],
                        color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.35)
        hinge = lab("hinge point", YELLOW, 28).move_to([0, OY - 2.0, 0])
        self.play(FadeIn(wedge), FadeIn(hinge), run_time=0.6)
        self.play(Indicate(wedge, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("neural folds")
        folds = lab("neural folds", BLUE, 30)
        folds.move_to([-4.3, OY + 0.8, 0])
        self.play(Transform(s, sec(1.8, 2.0)), FadeOut(wedge), FadeOut(hinge), ReplacementTransform(plate_l, folds), run_time=1.1)
        self.at("toward the middle")
        ar = VGroup(parr([-2.9, OY + 0.55, 0], [-1.0, OY + 0.55, 0]), parr([2.9, OY + 0.55, 0], [1.0, OY + 0.55, 0]))
        self.play(Transform(s, sec(0.5, 3.0)), FadeIn(ar), run_time=1.3)
        self.at("meet")
        self.play(Transform(s, sec(0.03, 3.2)), FadeOut(ar), run_time=0.7)
        self.at("fuse")
        flash(self, [0, OY, 0])
        self.play(Transform(s, tube(1.6)), run_time=0.7)
        self.play(FadeOut(folds), run_time=0.3)
        self.at("pinches off")
        tl = lab("neural tube", GREEN, 30).move_to([0, OY - 2.2 - 0.9, 0]) if False else lab("neural tube", GREEN, 30).move_to([4.2, OY - 2.0, 0])
        self.play(Transform(s, tube(1.6, drop=0.35)), FadeIn(tl), run_time=1.0)
        self.at("skin")
        self.play(FadeIn(skin, shift=DOWN * 0.1), run_time=0.4)
        self.at("seals over")
        seal = Line([-HALF, OY, 0], [HALF, OY, 0], color=ORANGE, stroke_width=8)
        self.play(Indicate(s[0:2], color=ORANGE, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Reach(SpokenScene):
    """a wide plate: the folds move a fixed reach and stop short. A narrow plate: the same reach closes it."""

    def construct(self):
        s = sec(3.6, 0)
        self.play(FadeIn(s), run_time=0.5)
        self.at("width of the plate")
        dim = darr([-3.6, OY + 1.9, 0], [3.6, OY + 1.9, 0], GREY, 5)
        wl = lab("wide", TEXT, 32).move_to([0, OY + 2.5, 0])
        self.play(GrowFromCenter(dim), FadeIn(wl), run_time=0.8)
        self.at("two people")
        table = RoundedRectangle(corner_radius=0.1, width=5.6, height=0.3, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.35).move_to([0, -2.2, 0])
        tl = lab("wide table", GREY, 26).move_to([0, -2.8, 0])

        def person(x):
            head = Circle(radius=0.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([x, -0.9, 0])
            body = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.0, stroke_color=TEXT, stroke_width=3,
                                    fill_color=TEXT, fill_opacity=0.25).move_to([x, -1.8, 0])
            return VGroup(head, body)
        pl, pr = person(-3.7), person(3.7)
        self.play(FadeIn(table), FadeIn(pl), FadeIn(pr), FadeIn(tl), run_time=0.8)
        self.at("reaching to shake hands")
        armL = Line([-3.35, -1.5, 0], [-3.35, -1.5, 0], color=YELLOW, stroke_width=8)
        armR = Line([3.35, -1.5, 0], [3.35, -1.5, 0], color=YELLOW, stroke_width=8)
        self.add(armL, armR)
        self.play(armL.animate.put_start_and_end_on([-3.35, -1.5, 0], [-1.35, -1.5, 0]),
                  armR.animate.put_start_and_end_on([3.35, -1.5, 0], [1.35, -1.5, 0]), run_time=1.2)
        self.at("fixed reach")
        self.play(Indicate(VGroup(armL, armR), color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("The folds are the same")
        ra = VGroup(parr([-3.6, OY + 0.55, 0], [-1.9, OY + 0.55, 0]), parr([3.6, OY + 0.55, 0], [1.9, OY + 0.55, 0]))
        rl = VGroup(lab("reach", YELLOW, 28).move_to([-2.75, OY + 1.1, 0]), lab("reach", YELLOW, 28).move_to([2.75, OY + 1.1, 0]))
        self.play(FadeOut(VGroup(table, pl, pr, tl, armL, armR)), run_time=0.5)
        self.play(GrowFromPoint(ra[0], ra[0].get_start()), GrowFromPoint(ra[1], ra[1].get_start()), FadeIn(rl), run_time=0.8)
        self.at("rise and move inward")
        self.play(Transform(s, sec(1.9, 2.4)), run_time=1.4)
        self.at("too far apart")
        gap = darr([-1.5, OY - 0.6, 0], [1.5, OY - 0.6, 0], RED, 5)
        self.play(FadeOut(VGroup(dim, wl, ra, rl)), GrowFromCenter(gap), run_time=0.6)
        self.at("never meet")
        nm = lab("never meet", RED, 34).move_to([0, OY - 1.3, 0])
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.5)
        self.at("before the tube can close")
        self.play(FadeOut(VGroup(gap, nm)), Transform(s, sec(3.6, 0)), run_time=0.8)
        self.at("narrow")
        na = VGroup(parr([-3.6, OY + 0.55, 0], [-1.75, OY + 0.55, 0], GREY), parr([3.6, OY + 0.55, 0], [1.75, OY + 0.55, 0], GREY))
        nl = lab("narrow", TEXT, 32).move_to([0, OY + 1.2, 0])
        self.play(Transform(s, sec(1.7, 0)), FadeIn(na), FadeIn(nl), run_time=1.0)
        self.play(FadeOut(na), run_time=0.3)
        self.play(Transform(s, sec(0.03, 3.2)), run_time=1.1)
        flash(self, [0, OY, 0])
        ml = lab("folds meet", GREEN, 34).move_to([4.2, OY - 1.5, 0])
        self.play(Transform(s, tube(1.6)), FadeIn(ml), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Squeeze(SpokenScene):
    """top view of plate cells: ten cells rearrange from a short wide block to a long thin one."""

    W, H = 1.3, 1.05

    def layout(self, rows):
        """positions for rows of cell counts, centred, rows spaced 1.15 apart (row 0 at the top)."""
        pos = []
        n = len(rows)
        for j, k in enumerate(rows):
            y = ((n - 1) / 2 - j) * 1.22
            for i in range(k):
                pos.append(np.array([(i - (k - 1) / 2) * 1.6, y, 0]))
        return pos

    def mkcell(self):
        r = RoundedRectangle(corner_radius=0.18, width=self.W, height=self.H, stroke_color=BLUE, stroke_width=3.5,
                             fill_color=BLUE, fill_opacity=0.28)
        bl = Rectangle(width=0.1, height=0.7, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(r.get_left() + RIGHT * 0.12)
        br = Rectangle(width=0.1, height=0.7, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(r.get_right() + LEFT * 0.12)
        bl.set_opacity(0); br.set_opacity(0)
        g = VGroup(r, bl, br)
        g.r, g.bl, g.br = r, bl, br
        return g

    def construct(self):
        p0 = self.layout([5, 5]); p1 = self.layout([4, 4, 2]); p2 = self.layout([2, 2, 2, 2, 2])
        cells = [self.mkcell().move_to(p) for p in p0]
        allc = VGroup(*cells)
        self.at("Narrowing")
        top = lab("convergent extension", TEAL, 34).move_to([0, 3.3, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.06), run_time=1.2)
        self.at("convergent extension")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.5)
        self.at("push in between")
        pushers = [cells[8], cells[9]]
        self.play(*[c.r.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.4) for c in pushers], run_time=0.5)
        self.at("intercalation")
        il = lab("intercalation", YELLOW, 34).move_to([0, -2.2, 0])
        self.play(FadeIn(il, shift=RIGHT * 0.1), run_time=0.5)
        self.at("narrower and longer")
        head = lab("head", GREY, 28).move_to([-2.6, 2.4, 0]); tail = lab("tail", GREY, 28).move_to([-2.6, -2.4, 0])
        # the three-row layout fits between head and tail
        self.play(*[c.r.animate.set_stroke(BLUE).set_fill(BLUE, 0.28) for c in pushers], FadeOut(il), run_time=0.3)
        self.play(*[c.animate.move_to(p) for c, p in zip(cells, p1)], run_time=1.2)
        self.at("short wide plate")
        self.wait(0.3)
        self.at("into a long thin")
        self.play(FadeOut(top), run_time=0.2)
        self.play(*[c.animate.move_to(p) for c, p in zip(cells, p2)], FadeIn(head), FadeIn(tail), run_time=1.6)
        self.at("which way is sideways")
        sd = darr([-1.6, -3.3, 0], [1.6, -3.3, 0], GREY, 5)
        sdl = lab("sideways", GREY, 28).move_to([3.1, -3.3, 0])
        self.play(GrowFromCenter(sd), FadeIn(sdl), run_time=0.7)
        self.at("planar cell polarity")
        pcp = chip("planar cell polarity", TEAL, 30).move_to([-4.3, 0.6, 0])
        self.play(FadeIn(pcp, shift=RIGHT * 0.1), run_time=0.6)
        self.at("including")
        dl = lab("Dishevelled", TEAL, 32).move_to([4.3, 1.3, 0])
        ar = Arrow([3.0, 1.3, 0], cells[1].br.get_center() + RIGHT * 0.2,
                   buff=0.05, color=TEAL, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(dl), GrowArrow(ar), run_time=0.6)
        self.at("opposite sides")
        self.play(FadeOut(sd), FadeOut(sdl),
                  *[o.animate.set_opacity(1) for c in cells for o in (c.bl, c.br)], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bar_over(x0, x1, color=RED, y=OY + 0.5):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=12)


class S05Frog(SpokenScene):
    """wide flat plate, Dishevelled disrupted at the midline: stays wide, folds rise, tube stays open."""

    def construct(self):
        s = sec(3.6, 0)
        self.at("Frog embryos")
        top = lab("frog embryo", GREY, 30).to_edge(UP, buff=0.45)
        self.play(FadeIn(s), FadeIn(top), run_time=0.8)
        self.at("early frog cell is mapped")
        ticks = VGroup(*[Line([x, OY + 0.18, 0], [x, OY - 0.18, 0], color=TEXT, stroke_width=3)
                         for x in np.linspace(-3.4, 3.4, 15)])
        ml = lab("each cell's fate is known", GREY, 28).move_to([0, OY + 1.3, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.05), FadeIn(ml), run_time=1.0)
        self.at("aim an injection")
        needle = VGroup(Line([0, OY + 2.2, 0], [0, OY + 1.0, 0], color=TEXT, stroke_width=5),
                        Polygon([-0.12, OY + 1.0, 0], [0.12, OY + 1.0, 0], [0, OY + 0.45, 0], color=TEXT, stroke_width=3,
                                fill_color=TEXT, fill_opacity=1))
        self.play(FadeOut(ml), FadeIn(needle, shift=DOWN * 0.2), run_time=0.7)
        self.at("a disrupted")
        bar = bar_over(-1.2, 1.2)
        barl = lab("Dishevelled disrupted", RED, 30).move_to([0, OY + 1.1, 0])
        mid = lab("midline", GREY, 26).move_to([0, OY - 0.65, 0])
        self.play(FadeOut(needle), FadeOut(ticks), GrowFromCenter(bar), FadeIn(barl), FadeIn(mid), run_time=0.7)
        self.at("stayed wide")
        dim = darr([-3.6, OY + 2.1, 0], [3.6, OY + 2.1, 0], RED, 5)
        wl = lab("plate stays wide", RED, 30).move_to([0, OY + 2.65, 0])
        self.play(FadeOut(top), GrowFromCenter(dim), FadeIn(wl), run_time=0.7)
        self.at("rose and moved inward")
        ra = VGroup(parr([-3.6, OY + 0.55, 0], [-2.0, OY + 0.55, 0]), parr([3.6, OY + 0.55, 0], [2.0, OY + 0.55, 0]))
        self.play(Transform(s, sec(1.9, 2.4)), FadeOut(mid), FadeIn(ra), run_time=1.3)
        self.at("tube stayed open")
        gap = darr([-1.5, OY - 0.6, 0], [1.5, OY - 0.6, 0], RED, 5)
        ol = lab("tube open", RED, 34).move_to([0, OY - 1.3, 0])
        self.play(FadeOut(ra), GrowFromCenter(gap), FadeIn(ol), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    """sides disrupted -> closes. Midline needed. Mouse: nothing starts. Rule: wide = open, narrow = closed."""

    def construct(self):
        # rebuild the end of the previous scene
        s = sec(1.9, 2.4)
        bar = bar_over(-1.2, 1.2)
        barl = lab("Dishevelled disrupted", RED, 30).move_to([0, OY + 1.1, 0])
        dim = darr([-3.6, OY + 2.1, 0], [3.6, OY + 2.1, 0], RED, 5)
        wl = lab("plate stays wide", RED, 30).move_to([0, OY + 2.65, 0])
        gap = darr([-1.5, OY - 0.6, 0], [1.5, OY - 0.6, 0], RED, 5)
        ol = lab("tube open", RED, 34).move_to([0, OY - 1.3, 0])
        old = VGroup(bar, barl, dim, wl, gap, ol)
        self.add(s, old)
        self.at("sides instead")
        sb = VGroup(bar_over(-3.6, -1.2), bar_over(1.2, 3.6))
        sbl = lab("Dishevelled disrupted at the sides", RED, 30).move_to([0, OY + 1.2, 0])
        self.play(FadeOut(old), Transform(s, sec(3.6, 0)), run_time=0.6)
        self.play(FadeIn(sb), FadeIn(sbl), run_time=0.6)
        self.at("This time")
        nb = VGroup(bar_over(-1.7, -0.55), bar_over(0.55, 1.7))
        self.play(Transform(s, sec(1.7, 0)), Transform(sb, nb), sbl.animate.move_to([0, OY + 1.2, 0]), run_time=0.8)
        self.play(Transform(s, sec(0.03, 3.2)), run_time=0.8)
        flash(self, [0, OY, 0], r=0.5)
        cl = lab("closes normally", GREEN, 34).move_to([4.2, OY - 1.5, 0])
        self.play(Transform(s, tube(1.6)), FadeIn(cl), run_time=0.5)
        self.at("needed at the midline")
        self.play(FadeOut(VGroup(sb, sbl, cl)), Transform(s, sec(3.6, 0)), run_time=0.8)
        mb = bar_over(-1.2, 1.2, TEAL)
        ml = lab("midline: narrowing sets the distance", TEAL, 30).move_to([0, OY + 1.2, 0])
        dd = darr([-3.6, OY + 2.1, 0], [3.6, OY + 2.1, 0], YELLOW, 5)
        dl = lab("distance between the folds", YELLOW, 30).move_to([0, OY + 2.65, 0])
        self.play(GrowFromCenter(mb), FadeIn(ml), run_time=0.7)
        self.at("distance between the folds")
        self.play(GrowFromCenter(dd), FadeIn(dl), run_time=0.7)
        self.at("Mice tell the same story")
        self.play(FadeOut(VGroup(mb, ml, dd, dl)), run_time=0.5)
        mouse = lab("loop-tail mouse", GREY, 32).to_edge(UP, buff=0.45)
        self.play(FadeIn(mouse), run_time=0.5)
        self.at("failed to extend")
        mb2 = bar_over(-1.2, 1.2, RED)
        ml2 = lab("midline failed to extend", RED, 30).move_to([0, OY + 1.2, 0])
        self.play(GrowFromCenter(mb2), FadeIn(ml2), run_time=0.7)
        self.at("closure never started")
        nv = lab("closure never started", RED, 34).move_to([0, OY - 1.4, 0])
        self.play(FadeIn(nv, shift=UP * 0.1), run_time=0.6)
        self.at("Keep this rule")
        self.play(FadeOut(VGroup(s, mb2, ml2, nv, mouse)), run_time=0.5)
        ob = sec(1.9, 2.4, half=2.9, sc=1.0, cx=-3.3, oy=OY)
        cb = tube(1.6, half=2.9, sc=1.0, cx=3.3, oy=OY)
        # left (wide) picture shows a wide plate whose folds stop short: draw it with a=1.9 on a wide plate
        self.play(FadeIn(cb), run_time=0.5)
        cbl = lab("narrow plate: folds meet", GREEN, 28).move_to([3.3, OY - 3.9, 0])
        self.play(FadeIn(cbl), run_time=0.4)
        self.at("stays too wide")
        wide_l = lab("wide plate: folds stop short", RED, 28).move_to([-3.3, OY - 3.9, 0])
        self.play(FadeIn(ob), FadeIn(wide_l), run_time=0.6)
        self.at("cannot meet")
        self.play(Indicate(wide_l, color=RED, scale_factor=1.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "If the plate stays too wide, the folds cannot meet."
