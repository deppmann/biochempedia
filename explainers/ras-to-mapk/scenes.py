"""Ras to MAPK: one chain, two answers, set by time  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = growth factors (EGF, NGF): the signal outside the cell
  BLUE   = Ras, the GTP switch
  PINK   = SOS, the protein that loads Ras with GTP
  PURPLE = the kinases Raf, MEK, ERK
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = on / active (the GTP tag, an active kinase's outline, ERK activity, the open window)
  RED    = feedback and stopping (feedback arrows, the phosphatase, the closing edge of a window)
  ORANGE = the cell's answer (a dividing cell, a cell with fibres)
  GREY   = membrane, outlines, labels, and parts not yet known

No molecular structures: Ras is a mouth on the membrane, Raf is a block with a lid that folds over it,
MEK and ERK are blocks with labelled site tabs, a phosphate is a "P" badge, DNA is a bar.

Two framings of the same picture (BASE, and ZOOM which is BASE scaled up on the membrane):
  scene 2   ZOOM   Ras and Raf fill the frame; at the end the view pulls back to BASE
  scenes 3-4 BASE  the staircase membrane -> Ras -> Raf pair -> MEK -> ERK across the whole frame
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"


# ---------------------------------------------------------------------------------------------
# framings: BASE coordinates are used to place everything; a View maps them to the screen
# ---------------------------------------------------------------------------------------------
class View:
    def __init__(self, k=1.0, ox=0.0, oy=0.0, sx=0.0, sy=0.0):
        self.k, self.ox, self.oy, self.sx, self.sy = k, ox, oy, sx, sy
        self.sw = 3 * k ** 0.5

    def p(self, x, y):
        return np.array([self.sx + self.k * (x - self.ox), self.sy + self.k * (y - self.oy), 0.0])


BASE = View(k=1.2)
ZOOM = View(k=2.0, ox=-5.1, oy=1.2, sx=-4.9, sy=0.0)

MEM_X = -5.1
RAS_X, RAS_Y, RAS_R = -4.1, 1.2, 0.9
RAFA = (-1.9, 1.2)
RAFB = (-1.9, 0.15)
SOS_XY = (-4.35, -0.12)
MEK_XY = (1.4, -1.0)
ERK_XY = (3.7, -2.2)
RAF_W, RAF_H, LID_W, LID_H = 1.9, 0.9, 0.7, 0.55
KIN_W, KIN_H = 1.7, 1.2


def ZP(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24, color=GREY):
    """a dashed chip: something that is not there, or not yet there."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(k=1.0):
    """a phosphate."""
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation each: a new VGroup would re-add them on top)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def bez(a, c1, c2, b):
    return CubicBezier(np.array(a, float), np.array(c1, float), np.array(c2, float), np.array(b, float))


def tail_bar(curve_pts, color=RED, w=6, half=0.26):
    """the flat end of an inhibition arrow, across the direction of the last stretch."""
    a, b = np.array(curve_pts[0], float), np.array(curve_pts[1], float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return Line(b + perp * half, b - perp * half, color=color, stroke_width=w)


def fb_curve(a, c1, c2, b, color=RED, w=5):
    """a curved inhibition arrow: [curve, end bar]."""
    cv = bez(a, c1, c2, b)
    cv.set_stroke(color, w)
    return VGroup(cv, tail_bar((c2, b), color, w + 1))


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def bracket(x, y0, y1, side=1, color=GREY, w=4, d=0.14):
    """a square bracket on a vertical span; side=+1 opens to the left (sits on the right)."""
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w),
                  Line([x, y0, 0], [x - side * d, y0, 0], color=color, stroke_width=w),
                  Line([x, y1, 0], [x - side * d, y1, 0], color=color, stroke_width=w))


# ---- the cell's answers (S01, S05, S06) ----
def cell_icon(c, r=0.5, color=ORANGE):
    c = np.array(c, float)
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15).move_to(c),
                  Dot(c, radius=r * 0.22, color=GREY))


def dividing_icon(c, r=0.5, color=ORANGE):
    """a cell that has split in two."""
    c = np.array(c, float)
    rr = r * 0.72
    return VGroup(cell_icon(c + LEFT * rr * 0.95, rr, color), cell_icon(c + RIGHT * rr * 0.95, rr, color))


def fibres_icon(c, r=0.5, length=0.75, color=ORANGE):
    """a cell with long fibres growing from it."""
    c = np.array(c, float)
    fib = VGroup()
    for a, wob in ((25, 1), (75, -1), (140, 1), (200, -1), (255, 1), (320, -1)):
        t = np.radians(a)
        u = np.array([np.cos(t), np.sin(t), 0])
        v = np.array([-np.sin(t), np.cos(t), 0])
        p0 = c + u * r
        p1 = c + u * (r + length * 0.5) + v * 0.1 * wob
        p2 = c + u * (r + length) - v * 0.06 * wob
        f = VMobject(stroke_color=color, stroke_width=4).set_points_smoothly([p0, p1, p2])
        fib.add(VGroup(f, Dot(p2, radius=0.06, color=color)))
    return VGroup(fib, cell_icon(c, r, color))


# ---------------------------------------------------------------------------------------------
# the parts of the chain
# ---------------------------------------------------------------------------------------------
def membrane(V):
    return RoundedRectangle(corner_radius=0.1, width=0.3 * V.k, height=6.9, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([V.p(MEM_X, 0)[0], 0, 0])


def pac_points(c, R, mouth_deg, n=72):
    a = np.radians(mouth_deg) / 2
    angs = np.linspace(a, TAU - a, n)
    return [c] + [c + R * np.array([np.cos(t), np.sin(t), 0]) for t in angs]


def ras_body(V, mouth, on):
    c, R = V.p(RAS_X, RAS_Y), RAS_R * V.k
    col = GREEN if on else BLUE
    return Polygon(*pac_points(c, R, mouth), stroke_color=col, stroke_width=V.sw + (1 if on else 0),
                   fill_color=BLUE, fill_opacity=0.32 if on else 0.16)


def ras(V, mouth=18, on=False):
    """Ras: a mouth on the membrane. Slack with GDP, open with GTP."""
    c, R = V.p(RAS_X, RAS_Y), RAS_R * V.k
    body = ras_body(V, mouth, on)
    lbl = T("Ras", 30 * V.k, BLUE, weight=BOLD).move_to(c + LEFT * 0.3 * R)
    g = VGroup(body, lbl)
    g.body, g.lbl = body, lbl
    return g


def nt_tag(V, text, color):
    """the nucleotide Ras is holding, on top of it."""
    return bchip(text, color, 22 * V.k, pad=0.14 * V.k).move_to(V.p(RAS_X, RAS_Y + RAS_R + 0.38))


def sos_chip(V):
    return bchip("SOS", PINK, 24 * V.k, pad=0.18 * V.k).move_to(V.p(*SOS_XY))


def raf(V, x, y, open_=False, active=False):
    """Raf: a block (the kinase) and a lid (its front half). Folded shut the lid lies over the block;
    open, it swings out to the left, where Ras can hold it. [body, lid[back, box], label]"""
    k = V.k
    c = V.p(x, y)
    col = GREEN if active else PURPLE
    body = RoundedRectangle(corner_radius=0.2 * k, width=RAF_W * k, height=RAF_H * k, stroke_color=col,
                            stroke_width=V.sw + (1.5 if active else 0), fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    H = V.p(x - RAF_W / 2, y)
    lc = H + (LEFT if open_ else RIGHT) * LID_W * k / 2
    back = RoundedRectangle(corner_radius=0.12 * k, width=LID_W * k, height=LID_H * k, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(lc)
    box = RoundedRectangle(corner_radius=0.12 * k, width=LID_W * k, height=LID_H * k, stroke_color=col, stroke_width=V.sw,
                           fill_color=PURPLE, fill_opacity=0.55).move_to(lc)
    lid = VGroup(back, box)
    lbl = T("Raf", 28 * k, PURPLE, weight=BOLD).move_to(c + RIGHT * 0.35 * k)
    g = VGroup(body, lid, lbl)
    g.body, g.lid, g.lbl, g.H = body, lid, lbl, H
    return g


def kinase(V, name, x, y, tabs, w=KIN_W, h=KIN_H):
    """MEK or ERK: a block with site tabs stacked on its left edge. [back, body, label, tab, tab]"""
    k = V.k
    c = V.p(x, y)
    back = RoundedRectangle(corner_radius=0.24 * k, width=w * k, height=h * k, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.24 * k, width=w * k, height=h * k, stroke_color=PURPLE, stroke_width=V.sw,
                            fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    lbl = T(name, 30 * k, PURPLE, weight=BOLD).move_to(c)
    th, gap = 0.46, 0.04
    n = len(tabs)
    y0 = y + (n * th + (n - 1) * gap) / 2 - th / 2
    tab_g, sites = [], []
    for i, t in enumerate(tabs):
        ty = y0 - i * (th + gap)
        tx = x - w / 2 - 0.33
        rect = Rectangle(width=0.66 * k, height=th * k, stroke_color=PURPLE, stroke_width=V.sw, fill_color=PURPLE,
                         fill_opacity=0.3).move_to(V.p(tx, ty))
        tab_g.append(VGroup(rect, T(t, 22 * k, PURPLE).move_to(V.p(tx, ty))))
        sites.append(V.p(x - w / 2 - 0.66 - 0.2, ty))
    g = VGroup(back, body, lbl, *tab_g)
    g.body, g.lbl, g.tabs, g.sites = body, lbl, tab_g, sites
    return g


def go_on(g, extra=()):
    """animations: this kinase is active (green outline)."""
    anims = [g.body.animate.set_stroke(GREEN, 4.5)]
    for t in extra:
        anims.append(t.animate.set_stroke(GREEN))
    return anims


def go_quiet(g):
    return [g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.12), g.lbl.animate.set_color(GREY)]


def raf_on(g):
    return [g.body.animate.set_stroke(GREEN, 4.5), g.lid[1].animate.set_stroke(GREEN)]


def raf_weak(g):
    return [g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.12), g.lid[1].animate.set_stroke(GREY).set_fill(GREY, 0.3),
            g.lbl.animate.set_color(GREY)]


def stage(V, ras_on=True, rafs_on=True):
    """the membrane, Ras (holding GTP), SOS and the Raf pair, as they stand at the end of scene 2."""
    mem = membrane(V)
    r = ras(V, 70, ras_on)
    tag = nt_tag(V, "GTP", GREEN)
    sos = sos_chip(V)
    a = raf(V, *RAFA, open_=True, active=rafs_on)
    b = raf(V, *RAFB, open_=True, active=rafs_on)
    return mem, r, tag, sos, a, b


def reframe(old, new):
    """morph each piece into the same piece of another framing."""
    return [Transform(a, b) for a, b in zip(old, new)]


class Film(SpokenScene):
    def outro(self, *anims, then=None, run_time=0.38, hold=0.0):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        change framing. These run after the last word, so they add a short breath between scenes."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
            self.wait(0.15)
        if hold:
            self.wait(hold)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Ras to MAPK: The Kinase Cascade"
    TITLE = "One chain, two answers, set by time"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """EGF and NGF go in, different answers come out, through the same four proteins. (BASE)"""

    def construct(self):
        title = T("PC12 cell", 26, GREY).move_to([0, 3.22, 0])
        box = RoundedRectangle(corner_radius=0.3, width=2.7, height=5.2).move_to([0, 0.33, 0])
        edge = DashedVMobject(box, num_dashes=64).set_color(GREY)
        q = T("?", 80, GREY, weight=BOLD).move_to([0, 0.33, 0])
        self.play(FadeIn(title), Create(edge), FadeIn(q), run_time=0.9)

        # EGF: in at the top left, out at the bottom left
        egf = bchip("EGF", YELLOW, 30).move_to([-4.7, 2.35, 0])
        in_l = arr([-3.7, 2.35, 0], [-1.4, 2.35, 0], YELLOW)
        out_l = arr([-1.4, -1.55, 0], [-3.4, -1.55, 0], GREY)
        path_l = VMobject().set_points_as_corners([egf.get_center(), [-1.4, 2.35, 0], [0, 2.35, 0], [0, -1.55, 0], [-1.4, -1.55, 0], [-3.9, -1.55, 0]])
        dot = Dot(egf.get_center(), radius=0.15, color=YELLOW)
        div_lbl = T("divides", 28, ORANGE).move_to([-4.7, -2.65, 0])
        div_ic = dividing_icon([-4.7, -1.55, 0], 0.62)
        self.at("growth factor")
        self.play(FadeIn(egf, shift=RIGHT * 0.2), GrowArrow(in_l), run_time=0.5)
        self.play(FadeIn(dot), run_time=0.1)
        self.play(MoveAlongPath(dot, path_l), run_time=1.3, rate_func=linear)
        one = cell_icon([-4.7, -1.55, 0], 0.62)
        self.play(FadeOut(dot), FadeIn(out_l), FadeIn(one), run_time=0.2)
        self.at("divides")
        self.play(Transform(one, div_ic), FadeIn(div_lbl, shift=UP * 0.1), run_time=0.6)

        # NGF: the same box, a different answer
        ngf = bchip("NGF", YELLOW, 30).move_to([4.7, 2.35, 0])
        in_r = arr([3.7, 2.35, 0], [1.4, 2.35, 0], YELLOW)
        out_r = arr([1.4, -1.55, 0], [3.2, -1.55, 0], GREY)
        path_r = VMobject().set_points_as_corners([ngf.get_center(), [1.4, 2.35, 0], [0, 2.35, 0], [0, -1.55, 0], [1.4, -1.55, 0], [3.9, -1.55, 0]])
        dot2 = Dot(ngf.get_center(), radius=0.15, color=YELLOW)
        ghost = dividing_icon([4.7, -1.55, 0], 0.62).set_opacity(0.45)
        x_r = strike(ghost)
        fib = fibres_icon([4.7, -1.55, 0], 0.45, 0.75)
        fib_lbl = T("nerve-like fibres", 26, ORANGE).move_to([4.6, -3.1, 0])
        self.at("same cell")
        self.play(FadeIn(ngf, shift=LEFT * 0.2), GrowArrow(in_r), run_time=0.6)
        self.play(FadeIn(dot2), run_time=0.1)
        self.play(MoveAlongPath(dot2, path_r), run_time=1.2, rate_func=linear)
        self.play(FadeOut(dot2), FadeIn(out_r), run_time=0.2)
        self.at("stops dividing")
        self.play(FadeIn(ghost), Create(x_r), run_time=0.5)
        self.at("grows long")
        self.play(FadeOut(ghost), FadeOut(x_r), run_time=0.3)
        self.play(LaggedStart(*[Create(f) for f in fib[0]], lag_ratio=0.12), FadeIn(fib[1]), FadeIn(fib_lbl, shift=UP * 0.1),
                  run_time=1.1)

        # the same four proteins fill the box
        names = [("Ras", BLUE), ("Raf", PURPLE), ("MEK", PURPLE), ("ERK", PURPLE)]
        ys = [2.35, 1.0, -0.35, -1.7]
        chips = [bchip(n, c, 30).move_to([0, y, 0]) for (n, c), y in zip(names, ys)]
        links = [arr(chips[i].get_bottom(), chips[i + 1].get_top(), GREY, w=4, tip=0.16) for i in range(3)]
        self.at("proteins")
        self.play(FadeOut(q), run_time=0.3)
        self.wait(0.15)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c, scale=0.8), GrowArrow(l) if l is not None else Wait(0.01))
                               for c, l in zip(chips, [None] + links)], lag_ratio=0.55), run_time=2.3)
        self.at("one chain")
        self.play(LaggedStart(*[Indicate(c[1:], color=TEXT, scale_factor=1.08) for c in chips], lag_ratio=0.15), run_time=0.9)
        two = T("?", 64, ORANGE, weight=BOLD).move_to([0, -2.85, 0])
        self.at("two instructions")
        self.play(FadeIn(two, scale=0.6), *glow(one, fib[1], s=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Catch(Film):
    """SOS loads Ras with GTP; active Ras holds the folded Raf at the membrane and opens it; two Rafs pair. (ZOOM)"""

    def construct(self):
        V = ZOOM
        k = V.k
        mem = membrane(V)
        r = ras(V, 18, False)
        tag = nt_tag(V, "GDP", GREY)
        mlabel = T("membrane", 24, TEXT).rotate(PI / 2).move_to(ZP(V.p(MEM_X, 0)[0], -0.8))
        self.play(FadeIn(mem), FadeIn(r), FadeIn(tag), FadeIn(mlabel), run_time=0.8)

        sos = sos_chip(V)
        rest = sos.get_center().copy()
        sos.move_to(rest + ZP(4.2, 0.3))
        self.at("loads")
        self.play(FadeIn(sos), run_time=0.3)
        self.play(sos.animate.move_to(rest), run_time=0.7)
        self.play(tag.animate.shift(RIGHT * 1.2 + UP * 0.3).set_opacity(0), run_time=0.6)
        tag_on = nt_tag(V, "GTP", GREEN)
        self.at("is on")
        self.play(FadeIn(tag_on, scale=0.6), Transform(r.body, ras_body(V, 70, True)), run_time=0.8)
        self.play(*glow(r.body, s=1.05, color=GREEN), run_time=0.5)

        nk = T("not a kinase", 32, GREY).move_to(ZP(1.2, 2.55))
        self.at("not a kinase")
        self.play(FadeIn(nk, shift=UP * 0.1), run_time=0.4)
        by = T("works by contact", 32, TEXT).move_to(ZP(1.2, 2.55))
        self.at("by contact")
        self.play(Transform(r.body, ras_body(V, 36, True)), ReplacementTransform(nk, by), run_time=0.3)
        self.play(Transform(r.body, ras_body(V, 70, True)), run_time=0.3)

        # Raf, folded shut, floats in the cytosol
        rA = raf(V, -0.5, RAFA[1], open_=False)
        cyto = T("cytosol", 28, GREY).move_to(ZP(4.9, 3.0))
        self.at("catches")
        self.play(*glow(r.body, r.lbl, s=1.06, color=GREEN), FadeOut(by), run_time=0.6)
        self.at("floats")
        self.play(FadeIn(rA, shift=LEFT * 0.5), FadeIn(cyto), run_time=0.7)
        self.play(rA.animate(rate_func=there_and_back).shift(UP * 0.25), run_time=0.8)
        fs = T("folded shut", 30, GREY).next_to(rA, DOWN, buff=0.45)
        self.at("folded shut")
        self.play(FadeIn(fs), *glow(rA.lid[1], s=1.15), run_time=0.6)

        # Ras brings it to the membrane and opens it
        dx = (-0.5 - RAFA[0]) * k
        self.at("Binding")
        self.play(rA.animate.shift(LEFT * dx), FadeOut(fs), FadeOut(cyto), run_time=1.3)
        self.at("pull it open")
        self.play(Rotate(rA.lid, PI, about_point=rA.body.get_left()), run_time=0.8)
        rA.lid.become(raf(V, *RAFA, open_=True)[1])
        self.play(*glow(r.body, rA.lid[1], s=1.08, color=GREEN), run_time=0.5)

        # a second Raf pairs with it
        rB = raf(V, -0.5, RAFB[1], open_=True)
        self.at("Then two")
        self.play(FadeIn(rB, shift=LEFT * 0.5), run_time=0.6)
        self.at("pair")
        self.play(rB.animate.shift(LEFT * dx), run_time=0.9)
        br = bracket(rA.body.get_right()[0] + 0.45, rB.get_bottom()[1], rA.get_top()[1], side=1)
        pair_l = T("pair", 32, TEXT).next_to(br, RIGHT, buff=0.25)
        self.at("side by side")
        self.play(Create(br), FadeIn(pair_l), run_time=0.3)
        act_l = T("active", 32, GREEN).move_to(pair_l)
        self.at("normal activation")
        self.play(*raf_on(rA), *raf_on(rB), ReplacementTransform(pair_l, act_l), br.animate.set_color(GREEN), run_time=0.7)

        # pull back to the framing used by the next two scenes
        m2, r2, t2, s2, a2, b2 = stage(BASE)
        self.outro(FadeOut(mlabel), FadeOut(br), FadeOut(act_l),
                   then=reframe([mem, r, tag_on, sos, rA, rB], [m2, r2, t2, s2, a2, b2]))


# ---------------------------------------------------------------------------------------------
class S03Relay(Film):
    """Raf puts two phosphates on MEK; MEK puts two on ERK, and ERK needs both. (BASE)"""

    def construct(self):
        V = BASE
        k = V.k
        mem, r, tag, sos, rA, rB = stage(V)
        mek = kinase(V, "MEK", *MEK_XY, tabs=("Ser", "Ser"))
        erk = kinase(V, "ERK", *ERK_XY, tabs=("Thr", "Tyr"))
        self.add(mem, r, tag, sos, rA, rB)
        self.play(*glow(rA.body, rB.body, s=1.04, color=GREEN), run_time=0.6)

        # Raf -> MEK, two serines
        pa = pbadge(k).move_to(rA.body.get_right() + RIGHT * 0.3)
        pb = pbadge(k).move_to(rB.body.get_right() + RIGHT * 0.3)
        self.at("adds phosphates")
        self.play(FadeIn(pa, scale=0.5), FadeIn(pb, scale=0.5), run_time=0.4)
        self.at("next kinase")
        self.play(FadeIn(mek, scale=0.85), run_time=0.5)
        self.play(pa.animate(path_arc=0.5).move_to(mek.sites[0]), pb.animate(path_arc=0.5).move_to(mek.sites[1]), run_time=0.9)
        self.at("two serines")
        self.play(pop(pa, 1.4), pop(pb, 1.4), run_time=0.6)

        # MEK turns on
        self.at("unusual")
        self.play(*go_on(mek), *glow(mek.lbl, s=1.1), run_time=0.7)

        # MEK -> ERK: a threonine and a tyrosine, side by side
        src = mek.body.get_right() + RIGHT * 0.1
        p3 = pbadge(k).move_to(src + DOWN * 0.1)
        self.at("adds a phosphate")
        self.play(FadeIn(erk, scale=0.85), FadeIn(p3, scale=0.5), run_time=0.5)
        self.play(p3.animate(path_arc=0.5).move_to(erk.sites[0]), run_time=0.8)
        p4 = pbadge(k).move_to(src + DOWN * 0.45)
        self.at("and another")
        self.play(FadeIn(p4, scale=0.5), run_time=0.3)
        self.play(p4.animate(path_arc=0.5).move_to(erk.sites[1]), run_time=0.8)
        br = bracket(erk.sites[0][0] - 0.5, erk.sites[1][1] - 0.25, erk.sites[0][1] + 0.25, side=-1)
        apart = T("one residue apart", 26, GREY).next_to(br, LEFT, buff=0.2)
        self.at("apart")
        self.play(Create(br), FadeIn(apart), run_time=0.5)

        # ERK needs both
        self.at("needs both")
        self.play(*go_on(erk), pop(p3, 1.4), pop(p4, 1.4), FadeOut(apart), FadeOut(br), run_time=0.7)

        # take one off: ERK goes quiet
        self.at("Take either")
        self.play(p4.animate.shift(LEFT * 1.2).set_opacity(0), erk.body.animate.set_stroke(PURPLE, 3), run_time=0.8)
        self.at("goes quiet")
        self.play(*go_quiet(erk), run_time=0.6)

        # for the next scene: ERK is on again
        p5 = pbadge(k).move_to(src + DOWN * 0.45)
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(FadeIn(p5, scale=0.5), run_time=0.25)
        self.play(p5.animate(path_arc=0.5).move_to(erk.sites[1]),
                  erk.body.animate.set_stroke(GREEN, 4.5).set_fill(PURPLE, 0.3), erk.lbl.animate.set_color(PURPLE), run_time=0.9)
        self.wait(0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def chain_on(V):
    """the whole chain, every part on: [mem, ras, tag, sos, rafA, rafB, mek, erk, P x4 (MEK sites, ERK sites)]"""
    mem, r, tag, sos, rA, rB = stage(V)
    mek = kinase(V, "MEK", *MEK_XY, tabs=("Ser", "Ser"))
    erk = kinase(V, "ERK", *ERK_XY, tabs=("Thr", "Tyr"))
    for g in (mek, erk):
        g.body.set_stroke(GREEN, 4.5)
    ps = [pbadge(V.k).move_to(s) for s in mek.sites + erk.sites]
    return mem, r, tag, sos, rA, rB, mek, erk, ps


class S04Feedback(Film):
    """ERK shuts down what is above it, and turns on a phosphatase that takes its phosphates off. (BASE)"""

    def construct(self):
        V = BASE
        k = V.k
        mem, r, tag, sos, rA, rB, mek, erk, ps = chain_on(V)
        self.add(mem, r, tag, sos, rA, rB, mek, erk, *ps)
        pm1, pm2, pe1, pe2 = ps

        # the signal has a length
        neg = T("negative feedback", 34, RED, weight=BOLD).move_to(V.p(3.2, 2.5))
        self.at("Negative feedback")
        self.play(FadeIn(neg, shift=DOWN * 0.1), run_time=0.5)
        ck = clock(V.p(3.4, 1.3), 0.55)
        how = T("how long", 28, GREY).next_to(ck, RIGHT, buff=0.3)
        self.at("how long")
        self.play(FadeIn(ck), FadeIn(how), run_time=0.4)
        self.play(Rotate(ck.hand, -TAU * 0.6, about_point=ck.c, rate_func=linear), run_time=1.6)
        self.at("supplies its own")
        self.play(*glow(erk.body, erk.lbl, s=1.08, color=RED), run_time=0.7)

        # ERK -> back up the chain: Raf and SOS
        a1 = fb_curve(V.p(3.9, -1.6), V.p(4.6, 0.9), V.p(1.2, 2.4), V.p(-0.85, 1.35))
        a2 = fb_curve(V.p(3.3, -2.8), V.p(1.5, -2.9), V.p(-3.4, -2.4), V.p(-4.35, -0.43))
        q1 = pbadge(0.9 * k).move_to(a1[0].get_start())
        q2 = pbadge(0.9 * k).move_to(a2[0].get_start())
        self.at("phosphorylates proteins")
        self.play(FadeOut(neg), FadeOut(ck), FadeOut(how), Create(a1[0]), FadeIn(q1), run_time=0.3)
        self.play(MoveAlongPath(q1, a1[0]), run_time=1.1, rate_func=linear)
        self.play(FadeIn(a1[1]), FadeOut(q1), run_time=0.2)
        self.at("among them")
        self.play(Create(a2[0]), FadeIn(q2), run_time=0.2)
        self.play(MoveAlongPath(q2, a2[0]), run_time=1.1, rate_func=linear)
        self.play(FadeIn(a2[1]), FadeOut(q2), run_time=0.2)
        self.at("and that")
        self.play(*raf_weak(rA), *raf_weak(rB), sos[1].animate.set_stroke(GREY).set_fill(GREY, 0.1), sos[2].animate.set_color(GREY),
                  run_time=0.8)
        self.play(FadeOut(a1), FadeOut(a2), run_time=0.5)

        # ERK -> a gene -> a phosphatase (not there yet)
        gene = bchip("gene", GREY, 28).move_to(V.p(-3.6, -1.95))
        c2 = V.p(-2.4, -2.8)
        g_arrow = bez(V.p(3.4, -2.8), V.p(1.0, -2.95), c2, V.p(-3.3, -2.35))
        g_arrow.set_stroke(GREEN, 5)
        g_tip = Triangle(fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.14)
        d = np.array(g_arrow.get_end()) - c2
        g_tip.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(g_arrow.get_end())
        self.at("turns on genes")
        self.play(FadeIn(gene), run_time=0.3)
        self.play(Create(g_arrow), run_time=0.8)
        self.play(FadeIn(g_tip), gene[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.2), gene[2].animate.set_color(GREEN), run_time=0.4)
        ph_ghost = ghost_chip("phosphatase", 28, RED).move_to(V.p(-0.9, -2.15))
        self.at("phosphatases")
        self.play(FadeIn(ph_ghost, shift=RIGHT * 0.2), run_time=0.6)
        pointer = DashedLine(ph_ghost.get_right() + RIGHT * 0.05, [erk.sites[1][0] - 0.35, ph_ghost.get_center()[1], 0],
                             color=RED, stroke_width=4, dash_length=0.12)
        self.at("take both")
        self.play(Create(pointer), run_time=0.7)

        # slower: a protein has to be made
        ck2 = clock(V.p(-3.4, -0.95), 0.5)
        slow = T("slower", 30, RED).next_to(ck2, RIGHT, buff=0.3)
        self.at("slower")
        self.play(FadeIn(ck2), FadeIn(slow), run_time=0.4)
        self.play(Rotate(ck2.hand, -TAU * 1.0, about_point=ck2.c, rate_func=linear), run_time=1.1)
        ph = bchip("phosphatase", RED, 28).move_to(ph_ghost)
        self.at("has to be made")
        self.play(FadeOut(ph_ghost), FadeIn(ph), FadeOut(pointer), run_time=0.6)

        # it takes both phosphates off ERK
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(ph.animate.move_to([erk.sites[1][0] - 1.55, (erk.sites[0][1] + erk.sites[1][1]) / 2, 0]), run_time=0.9)
        self.play(pe1.animate.move_to(ph.get_center()).set_opacity(0), pe2.animate.move_to(ph.get_center()).set_opacity(0),
                  *go_quiet(erk), run_time=0.9)
        self.wait(0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
X0, X_HR, X_END = -3.7, -0.7, 3.9        # S05: time zero, "about an hour", the right end of the axis
YT, YB, AMP = 0.55, -2.3, 1.9            # S05: baselines of the top and bottom rows


def egf_curve(x0=X0, x1=X_HR, y0=YT, amp=AMP):
    """ERK activity after EGF: rises and falls back to nothing within about an hour (schematic)."""
    f = lambda t: (t / 0.15) * np.exp(1 - t / 0.15)
    return ParametricFunction(lambda t: np.array([x0 + (x1 - x0) * t, y0 + amp * f(t), 0]), t_range=[0, 1, 0.01],
                              color=GREEN, stroke_width=6)


def plateau_curve(x0=X0, x1=X_END, y0=YB, amp=AMP, color=GREEN, rise=0.12, run=2.6):
    """ERK activity after NGF: climbs to a plateau that lasts (schematic)."""
    f = lambda t: 1 - np.exp(-t / rise)
    return ParametricFunction(lambda t: np.array([x0 + (x1 - x0) * t / run, y0 + amp * f(t), 0]), t_range=[0, run, 0.01],
                              color=color, stroke_width=6)


def axes_row(x0, x1, y0, h):
    ya = Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3)
    xa = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3)
    return VGroup(ya, xa)


class S05Clock(Film):
    """Two rows on a shared clock: a short window and a long one; the difference is the instruction. (plots)"""

    def construct(self):
        H = AMP + 0.45
        rows = VGroup(axes_row(X0, X_HR + 0.6, YT, H), axes_row(X0, X_END + 0.3, YB, H))
        lab1 = T("stimulus 1", 24, GREY).move_to([-5.15, YT + 1.0, 0])
        lab2 = T("stimulus 2", 24, GREY).move_to([-5.15, YB + 1.0, 0])
        tarrow = Arrow([X_END + 0.3, YB, 0], [X_END + 0.65, YB, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        tlabel = T("time", 24, GREY).move_to([X_END + 0.2, YB - 0.42, 0])
        erk_l = T("ERK activity", 24, GREEN).move_to([X0 + 1.15, YT + H + 0.3, 0])
        self.at("Different stimuli")
        self.play(Create(rows), FadeIn(lab1), FadeIn(lab2), FadeIn(tlabel), FadeIn(tarrow), FadeIn(erk_l), run_time=1.0)

        # windows of different length, each closed by feedback
        w1 = Rectangle(width=X_HR - X0, height=H, stroke_width=0, fill_color=GREEN, fill_opacity=0.14).move_to([(X0 + X_HR) / 2, YT + H / 2, 0])
        w2 = Rectangle(width=X_END - X0, height=H, stroke_width=0, fill_color=GREEN, fill_opacity=0.14).move_to([(X0 + X_END) / 2, YB + H / 2, 0])
        e1 = Line([X_HR, YT, 0], [X_HR, YT + H, 0], color=RED, stroke_width=6)
        e2 = Line([X_END, YB, 0], [X_END, YB + H, 0], color=RED, stroke_width=6)
        self.at("different lengths")
        self.play(GrowFromEdge(w1, LEFT), GrowFromEdge(w2, LEFT), run_time=1.5)
        self.at("closes the window")
        self.play(Create(e1), Create(e2), run_time=0.6)

        # EGF: a pulse that rises and falls back within about an hour
        egf = bchip("EGF", YELLOW, 28).move_to(lab1)
        c1 = egf_curve()
        hour = DashedLine([X_HR, YB - 0.1, 0], [X_HR, YT + H, 0], color=GREY, stroke_width=3, dash_length=0.12)
        hl = T("about an hour", 24, GREY).move_to([X_HR, YB - 0.5, 0])
        self.at("activity after")
        self.play(ReplacementTransform(lab1, egf), run_time=0.5)
        self.at("rises and falls")
        self.play(Create(c1), run_time=1.6, rate_func=linear)
        self.at("about an hour")
        self.play(Create(hour), FadeIn(hl), run_time=0.5)

        # NGF: climbs to a plateau that goes on
        ngf = bchip("NGF", YELLOW, 28).move_to(lab2)
        c2 = plateau_curve()
        tip = Triangle(fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.14).rotate(-PI / 2).move_to([X_END + 0.12, YB + AMP, 0])
        self.at("climbs")
        self.play(ReplacementTransform(lab2, ngf), run_time=0.4)
        self.play(Create(c2), run_time=1.2, rate_func=linear)
        self.play(FadeIn(tip), run_time=0.15)
        self.at("lasts for hours")
        self.play(*glow(c2, s=1.0, color=TEXT), run_time=0.6)

        # the difference is the instruction
        arr_d = DoubleArrow([X_HR + 0.1, YB + 0.5, 0], [X_END - 0.1, YB + 0.5, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        diff = T("the difference", 26, TEXT).move_to([(X_HR + X_END) / 2, YB + 0.95, 0])
        self.at("proposed")
        self.play(GrowFromCenter(arr_d), FadeIn(diff), run_time=0.7)
        ins = T("the instruction", 28, TEXT, weight=BOLD).move_to(diff)
        self.at("instruction")
        self.play(ReplacementTransform(diff, ins), run_time=0.6)

        # brief -> division, sustained -> differentiation
        XI = 5.3
        brief = T("brief", 26, GREEN).move_to([XI, 2.5, 0])
        d_ic = dividing_icon([XI, 1.6, 0], 0.5)
        d_lbl = T("division", 24, ORANGE).move_to([XI, 0.85, 0])
        sust = T("sustained", 26, GREEN).move_to([XI, 0.15, 0])
        f_ic = fibres_icon([XI, -1.0, 0], 0.36, 0.5)
        f_lbl = T("differentiation", 22, ORANGE).move_to([XI - 0.1, -2.1, 0])
        self.at("brief signal")
        self.play(FadeOut(arr_d), FadeOut(ins), FadeIn(brief, shift=DOWN * 0.1), FadeIn(d_ic), FadeIn(d_lbl), run_time=0.8)
        self.at("sustained")
        self.play(FadeIn(sust, shift=DOWN * 0.1), FadeIn(f_ic), FadeIn(f_lbl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PX0, PXE, PYB, PH = -2.7, 3.7, -1.45, 3.0     # S06: plot origin x, right end, baseline, height


class S06Test(Film):
    """Force MEK on, no growth factor: ERK stays on, the cell grows fibres; one cell line; the rule."""

    def construct(self):
        axes = axes_row(PX0, PXE + 0.2, PYB, PH)
        tarrow = Arrow([PXE + 0.2, PYB, 0], [PXE + 0.55, PYB, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        tlabel = T("time", 24, GREY).move_to([PXE + 0.1, PYB - 0.42, 0])
        erk_l = T("ERK activity", 24, GREEN).move_to([PX0 + 1.15, PYB + PH + 0.3, 0])
        self.play(Create(axes), FadeIn(tlabel), FadeIn(tarrow), FadeIn(erk_l), run_time=0.9)

        # no growth factor, but MEK forced on
        gf = ghost_chip("growth factor", 26, YELLOW).move_to([-5.0, 2.3, 0])
        gx = strike(gf)
        mek = bchip("MEK", PURPLE, 32).move_to([-5.0, 0.55, 0])
        mek[1].set_stroke(GREEN, 5)
        on_l = T("always on", 26, GREEN).move_to([-5.0, -0.3, 0])
        self.at("force")
        self.play(FadeIn(mek, scale=0.8), run_time=0.5)
        self.at("on for good")
        self.play(FadeIn(on_l, shift=DOWN * 0.1), *glow(mek[1], mek[2], s=1.1, color=GREEN), run_time=0.6)
        self.at("no growth factor")
        self.play(FadeIn(gf), run_time=0.3)
        self.play(Create(gx), run_time=0.3)

        # ERK stays on without end
        trace = plateau_curve(PX0, PXE, PYB, PH - 0.5, GREEN, 0.12, 2.6)
        tip = Triangle(fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.14).rotate(-PI / 2).move_to([PXE + 0.12, PYB + PH - 0.5, 0])
        link = arr([-4.0, 0.55, 0], [PX0 - 0.1, 0.0, 0], GREEN, w=4, tip=0.18)
        self.at("then stays on")
        self.play(GrowArrow(link), run_time=0.4)
        self.play(Create(trace), run_time=1.0, rate_func=linear)
        self.play(FadeIn(tip), run_time=0.15)
        self.at("without end")
        self.play(*glow(trace, s=1.0, color=TEXT), run_time=0.6)

        # it looks to the cell like a long NGF signal
        ghost = DashedVMobject(plateau_curve(PX0, PXE, PYB, PH - 0.5, YELLOW, 0.12, 2.6), num_dashes=70).set_color(YELLOW)
        ngf_l = T("a long NGF signal", 24, YELLOW).move_to([1.8, PYB + PH - 0.05, 0])
        self.at("cannot tell apart")
        self.play(Create(ghost), FadeIn(ngf_l), run_time=1.0)

        # the 1994 result: fibres, with no NGF
        XI = 5.2
        f_ic = fibres_icon([XI, 0.35, 0], 0.38, 0.52)
        f_lbl = T("fibres", 26, ORANGE).move_to([XI, -1.0, 0])
        self.at("grew")
        self.play(FadeOut(ngf_l), FadeOut(ghost), run_time=0.3)
        self.play(LaggedStart(*[Create(f) for f in f_ic[0]], lag_ratio=0.12), FadeIn(f_ic[1]), FadeIn(f_lbl, shift=UP * 0.1), run_time=1.0)

        # one caution: one cell line
        one = T("one cell line", 26, TEXT).move_to(f_lbl)
        self.at("one caution")
        self.play(ReplacementTransform(f_lbl, one), *glow(f_ic[1], s=1.2), run_time=0.7)
        cells = VGroup(*[VGroup(Circle(radius=0.3, stroke_color=GREY, stroke_width=3), T("?", 28, GREY)) for _ in range(5)])
        cells.arrange(RIGHT, buff=0.55).move_to([0.4, -3.05, 0])
        for c in cells:
            c[1].move_to(c[0])
        self.at("how widely")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.15), run_time=1.0)

        # the rule
        span = DoubleArrow([PX0, PYB - 0.95, 0], [PXE, PYB - 0.95, 0], buff=0, color=GREEN, stroke_width=4, tip_length=0.2)
        rule = T("how long ERK stays on", 30, GREEN, weight=BOLD).move_to([(PX0 + PXE) / 2, PYB - 1.5, 0])
        self.at("So keep this rule")
        self.play(FadeOut(cells), FadeOut(one), run_time=0.4)
        self.play(GrowFromCenter(span), FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.at("carries the")
        self.play(*glow(trace, s=1.0, color=TEXT), *glow(f_ic[1], s=1.2), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "In PC12 cells, how long ERK stays on carries the instruction."
