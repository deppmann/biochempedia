"""Where the Volume Goes (chapter 2 of the measured eukaryotic cell film).

COLOR MAP (chapter 1's, kept; new ones marked)
  ORANGE RNA, protein, cytoplasm       PURPLE genome (and, new, a thin outline = nuclear envelope)
  BLUE   membrane and surface          YELLOW gauge, questions
  PINK   (new) schematic mitochondria  TEAL   (new) vacuole
  TAN    (new) cell wall               LEAF   (new) chloroplasts (dark leaf green)
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#EE7FB0"
TAN = "#C9A36A"
LEAF = "#2F7D3A"
PLASTID = "#C9D3C0"
VT = ValueTracker

CELL_C = np.array([-2.45, -0.15, 0.0])
GAUGE_X = 4.55


# ----------------------------------------------------------------- small helpers
def tag(text, pos=(3.9, -3.45), size=24, color=TEXT):
    return T(text, size, color).move_to([pos[0], pos[1], 0]).set_opacity(.8)


def lab(text, size=28, color=TEXT, pos=None, **kw):
    t = T(text, size, color, **kw)
    g = VGroup(BackgroundRectangle(t, color=BG, fill_opacity=.78, buff=.07), t)
    if pos is not None:
        g.move_to([pos[0], pos[1], 0])
    return g


def disk_pts(n):
    return [(math.sqrt((k + .5) / n) * math.cos(k * 2.39996), math.sqrt((k + .5) / n) * math.sin(k * 2.39996)) for k in range(n)]


def halton(i, b):
    f, r = 1.0, 0.0
    while i > 0:
        f /= b
        r += f * (i % b)
        i //= b
    return r


def box_pts(n):
    return [(2 * halton(k + 1, 2) - 1, 2 * halton(k + 1, 3) - 1) for k in range(n)]


DISK = disk_pts(30)
BOX = box_pts(28)
BOX2 = box_pts(48)


def field(pts, cx, cy, hx, hy, t, amp=.15, avoid=(), keep=None, r=.09, color=ORANGE, op=.9):
    g = VGroup()
    for k, (u, v) in enumerate(pts):
        bx, by = cx + u * hx, cy + v * hy
        if any(math.hypot(bx - ax, by - ay) < ar for ax, ay, ar in avoid):
            continue
        if keep and not keep(bx, by):
            continue
        x = bx + amp * math.sin(1.2 * t + 1.7 * k)
        y = by + amp * math.cos(.9 * t + 2.3 * k)
        g.add(Dot([x, y, 0], radius=r, color=color).set_opacity(op))
    return g


class Par:
    def __init__(s, **kw):
        for k, v in kw.items():
            setattr(s, k, VT(v))

    def v(s, k):
        return getattr(s, k).get_value()

    def go(s, **kw):
        return [getattr(s, k).animate.set_value(v) for k, v in kw.items()]


# ----------------------------------------------------------------- chapter 1 world
def cell_body(center, r, glow=0):
    return Circle(r, stroke_color=BLUE, stroke_width=7 + glow, fill_color=ORANGE,
                  fill_opacity=.20).move_to(center)


def genome(center=CELL_C):
    return RoundedRectangle(corner_radius=.12, width=.72, height=.5, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=.55).move_to(np.array(center) + [-.5, .25, 0])


def nuc_outline(extra=0):
    return RoundedRectangle(corner_radius=.2, width=1.06, height=.84, stroke_color=PURPLE,
                            stroke_width=2.5 + extra, fill_opacity=0).move_to(CELL_C + [-.5, .25, 0])


def content_dots(center=CELL_C, r=2.25, n=20, radius=.085, spread=.76):
    c = np.array(center, float)
    out = VGroup()
    for k in range(n):
        rr = spread * r * math.sqrt((k + .5) / n)
        a = k * math.pi * (3 - math.sqrt(5))
        out.add(Dot(c + [rr * math.cos(a), rr * math.sin(a), 0], radius=radius, color=ORANGE).set_opacity(.85))
    out.add_updater(lambda m, dt, pivot=c: m.rotate(.45 * dt, about_point=pivot))
    return out


# ----------------------------------------------------------------- share bar
class Bar:
    def __init__(s, cx, cy, h=4.25, w=1.0):
        s.cx, s.cy, s.h, s.w = VT(cx), VT(cy), VT(h), VT(w)
        s.segs = []

    def add(s, color, lo=0.0, hi=0.0, op=.72):
        t = (VT(lo), VT(hi), color, op)
        s.segs.append(t)
        return t

    def y(s, f):
        return s.cy.get_value() - s.h.get_value() / 2 + .09 + f * (s.h.get_value() - .18)

    def right(s):
        return s.cx.get_value() + s.w.get_value() / 2

    def build(s):
        cx, cy, h, w = s.cx.get_value(), s.cy.get_value(), s.h.get_value(), s.w.get_value()
        out = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0).move_to([cx, cy, 0])
        g = VGroup(out)
        for lo, hi, col, op in s.segs:
            a, b = lo.get_value(), hi.get_value()
            if b - a > .003:
                g.add(Rectangle(width=w - .18, height=(b - a) * (h - .18), stroke_width=0, fill_color=col,
                                fill_opacity=op).move_to([cx, cy - h / 2 + .09 + (a + b) / 2 * (h - .18), 0]))
        return g

    def mob(s):
        return always_redraw(s.build)

    def side(s, text, f, color, size=28, buff=.15):
        t = T(text, size, color)
        t.move_to([s.right() + buff + t.width / 2, s.y(f), 0])
        return t


# ----------------------------------------------------------------- cells (functions of trackers)
def hamster(P, t):
    cx, cy, w, h = P.v("cx"), P.v("cy"), P.v("w"), P.v("h")
    body = Ellipse(width=w, height=h, stroke_color=BLUE, stroke_width=6 + P.v("bg"), fill_color=ORANGE,
                   fill_opacity=.18).move_to([cx, cy, 0])
    nr = .26 * h
    nx, ny = cx - .12 * w, cy + .07 * h
    nuc = Circle(nr, stroke_color=PURPLE, stroke_width=4 + P.v("ng"), fill_color=PURPLE,
                 fill_opacity=.35).move_to([nx, ny, 0])
    dots = field(DISK, cx, cy, .82 * w / 2, .82 * h / 2, t, avoid=[(nx, ny, nr + .15)])
    return VGroup(body, dots, nuc)


def mito_mark(c, ang=0):
    e = Ellipse(width=.62, height=.32, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=.45)
    ln = Line([-.16, 0, 0], [.16, 0, 0], color=PINK, stroke_width=3)
    c = np.array(list(c) + [0] * (3 - len(c)), float)
    return VGroup(e, ln).rotate(ang).move_to(c)


def rod(P, t):
    cx, cy, w, h = P.v("cx"), P.v("cy"), P.v("w"), P.v("h")
    body = RoundedRectangle(corner_radius=h / 2 - .01, width=w, height=h, stroke_color=BLUE,
                            stroke_width=6 + P.v("bg"), fill_color=ORANGE, fill_opacity=.18).move_to([cx, cy, 0])
    area = w * h - .2146 * h * h
    nr = math.sqrt(.08 * area / math.pi)
    nuc = Circle(nr, stroke_color=PURPLE, stroke_width=4 + P.v("ng"), fill_color=PURPLE,
                 fill_opacity=.18).move_to([cx, cy, 0])
    blk = RoundedRectangle(corner_radius=.05, width=nr * .95, height=nr * .62, stroke_color=PURPLE, stroke_width=2,
                           fill_color=PURPLE, fill_opacity=.6).move_to([cx, cy, 0])
    dots = field(BOX, cx, cy, w / 2 - .5, h / 2 - .32, t, avoid=[(cx, cy, nr + .2)])
    return VGroup(body, dots, nuc, blk)


def rod_arrows(P):
    cx, cy, w = P.v("cx"), P.v("cy"), P.v("w")
    a = Arrow([cx + w / 2 + .12, cy, 0], [cx + w / 2 + .62, cy, 0], buff=0, color=BLUE, stroke_width=6, tip_length=.2)
    b = Arrow([cx - w / 2 - .12, cy, 0], [cx - w / 2 - .62, cy, 0], buff=0, color=BLUE, stroke_width=6, tip_length=.2)
    return VGroup(a, b).set_opacity(P.v("ar"))


def vac_poly(cx, cy, vw, vh, lob, t):
    pts = []
    for i in range(72):
        th = 2 * math.pi * i / 72
        wob = 1 + .025 * math.sin(2 * th + .8 * t)
        pts.append([cx + vw / 2 * math.cos(th) * wob,
                    cy + vh / 2 * math.sin(th) * (1 - lob * (1 - math.cos(2 * th)) / 2) * wob, 0])
    return Polygon(*pts, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=.55)


def root(P, t):
    cx, cy, w, h = P.v("cx"), P.v("cy"), P.v("w"), P.v("h")
    vf, lob = P.v("vf"), P.v("lob")
    wall = RoundedRectangle(corner_radius=.3, width=w, height=h, stroke_color=TAN, stroke_width=16,
                            fill_opacity=0).move_to([cx, cy, 0])
    mem = RoundedRectangle(corner_radius=.22, width=w - .26, height=h - .26, stroke_color=BLUE, stroke_width=5,
                           fill_color=ORANGE, fill_opacity=.18).move_to([cx, cy, 0])
    iw, ih = w - .46, h - .46
    s = min(.95, math.sqrt(vf) * .97)
    vw, vh = iw * s, ih * s
    nx, ny = cx - iw / 2 + .5, cy + ih * .1
    keep = lambda x, y: abs((x - cx) / (vw / 2 + .06)) ** 3 + abs((y - cy) / (vh / 2 + .06)) ** 3 > 1
    dots = field(BOX2, cx, cy, iw / 2 - .12, ih / 2 - .12, t, avoid=[(nx, ny, .55)], keep=keep, amp=.08, r=.075)
    vac = vac_poly(cx, cy, vw, vh, lob, t)
    nuc = Circle(.32, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=.4).move_to([nx, ny, 0])
    return VGroup(wall, mem, dots, vac, nuc)


# ----------------------------------------------------------------- scene bases
class Clk:
    def clk(self):
        self.tt = VT(0)
        self.tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.tt)

    def T_(self):
        return self.tt.get_value()


class Sc(Clk, SpokenScene):
    def world(self, r0=2.25, rate=.0125, nuc=False, level=.62, label=True):
        self.clk()
        self.r = VT(r0)
        self.r.add_updater(lambda m, dt: m.increment_value(rate * dt))
        self.add(self.r)
        self.gl = VT(0)
        self.nw = VT(0)
        self.body = always_redraw(lambda: cell_body(CELL_C, self.r.get_value(), self.gl.get_value()))
        self.dots = content_dots()
        self.gen = genome()
        self.nucm = always_redraw(lambda: nuc_outline(self.nw.get_value()))
        self.bar = Bar(GAUGE_X, -.2)
        self.yel = self.bar.add(YELLOW, 0, level)
        self.barm = self.bar.mob()
        self.blab = T("amount ÷ volume", 30, YELLOW).move_to([GAUGE_X, 2.4, 0])
        items = [self.body, self.dots, self.gen, self.barm]
        if nuc:
            items.append(self.nucm)
        if label:
            items.append(self.blab)
        return items


def qmark():
    q = T("?", 96, YELLOW, weight=BOLD).move_to([1.0, 2.1, 0])
    q.add_updater(lambda m, dt, st=[0]: (st.__setitem__(0, st[0] + dt), m.move_to([1.0, 2.1 + .12 * math.sin(2.2 * st[0]), 0])))
    return q


# ----------------------------------------------------------------- scenes
class S00Link(Sc):
    def construct(self):
        items = self.world()
        self.play(*[FadeIn(m) for m in items], run_time=1.4)
        self.at("where does all its volume go")
        q = qmark()
        self.play(FadeIn(q, shift=UP * .5), run_time=.9)
        self.at("chapter 1")
        self.play(Indicate(self.blab, color=YELLOW, scale_factor=1.12), run_time=1.1)
        self.at("yeast cell")
        self.play(self.gl.animate.set_value(8), rate_func=there_and_back, run_time=1.2)
        self.at("each compartment")
        self.play(Create(self.nucm), run_time=1.4)
        self.at("share holds")
        self.play(Indicate(self.blab, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.finish()


class S01Title(Clk, TitleCard):
    LESSON = "Cells Control Their Size: A Measured Eukaryotic Cell"
    TITLE = "Where the Volume Goes"

    def construct(self):
        self.clk()
        self.r = VT(2.45)
        self.r.add_updater(lambda m, dt: m.increment_value(.0125 * dt))
        self.add(self.r)
        body = always_redraw(lambda: cell_body(CELL_C, self.r.get_value()))
        dots, gen = content_dots(), genome()
        nuc = nuc_outline()
        bar = Bar(GAUGE_X, -.2)
        bar.add(YELLOW, 0, .62)
        blab = T("amount ÷ volume", 30, YELLOW).move_to([GAUGE_X, 2.4, 0])
        q = qmark()
        title = T(self.TITLE, 44, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.add(body, dots, gen, nuc, bar.mob(), blab, q)
        self.play(FadeOut(q), FadeIn(title, shift=DOWN * .15), run_time=.7)
        self.wait(.9)
        self.play(FadeOut(title), run_time=.4)
        self.finish()


class S02Share(Sc):
    def construct(self):
        self.world(r0=2.48, nuc=True)
        self.add(self.body, self.dots, self.gen, self.nucm, self.barm, self.blab)
        self.wait(.5)
        self.at("enclosed by a membrane")
        self.play(self.gl.animate.set_value(9), self.nw.animate.set_value(5), rate_func=there_and_back, run_time=1.3)
        self.at("nucleus")
        lb = lab("nucleus", 30, PURPLE, (-5.5, 2.0))
        ln = Line([-4.75, 1.9, 0], [-3.42, .42, 0], color=PURPLE, stroke_width=3)
        self.play(FadeIn(lb), Create(ln), self.nw.animate.set_value(3.5), run_time=1.0)
        self.play(self.nw.animate.set_value(0), run_time=.6)
        self.at("is one")
        self.play(self.nw.animate.set_value(4), rate_func=there_and_back, run_time=.9)
        self.at("divide its volume")
        new = T("nucleus volume\n÷ cell volume", 30, YELLOW, line_spacing=.7).move_to([GAUGE_X, 2.55, 0])
        pur = self.bar.add(PURPLE, 0, 0, .8)
        self.play(Transform(self.blab, new), self.yel[1].animate.set_value(0),
                  self.nw.animate(rate_func=there_and_back).set_value(6), run_time=.7)
        self.at("by the cells")
        self.play(self.gl.animate.set_value(10), rate_func=there_and_back, run_time=.8)
        self.at("you get its share")
        self.play(pur[1].animate.set_value(.3), run_time=1.1)
        y = self.bar.y(.3)
        mk = DashedLine([GAUGE_X - .7, y, 0], [GAUGE_X + .85, y, 0], color=PURPLE, stroke_width=4)
        sh = T("share", 30, PURPLE).move_to([GAUGE_X + 1.55, y, 0])
        sc = tag("schematic", (GAUGE_X, -2.75), 26)
        self.play(Create(mk), FadeIn(sh), FadeIn(sc), run_time=.7)
        self.finish()


def ham_bar_big():
    b = Bar(2.4, -.2, 4.25, 1.0)
    n = b.add(GREY, 0, 1.0, .18)
    p = b.add(PURPLE, 0, .27, .8)
    m = b.add(PINK, .27, .323, .85)
    return b, n, p, m


class S03Hamster(Sc):
    def construct(self):
        # carried: yeast cell + the share bar from the last scene
        self.clk()
        bar = Bar(GAUGE_X, -.2)
        neu = bar.add(GREY, 0, 0, .18)
        pur = bar.add(PURPLE, 0, .3, .8)
        pk = bar.add(PINK, .3, .3, .85)
        blab = T("nucleus volume\n÷ cell volume", 30, YELLOW, line_spacing=.7).move_to([GAUGE_X, 2.55, 0])
        yeast = VGroup(cell_body(CELL_C, 2.5), content_dots(CELL_C, 2.25, 20).clear_updaters(), genome(), nuc_outline())
        barm = bar.mob()
        self.add(yeast, barm, blab)
        P = Par(cx=-3.0, cy=.15, w=.4, h=.4, bg=0, ng=0)
        ham = always_redraw(lambda: hamster(P, self.T_()))
        self.add(ham)
        self.play(yeast.animate.scale(.2).move_to([-6.1, 3.0, 0]).set_opacity(0),
                  *P.go(w=5.0, h=4.4), pur[1].animate.set_value(0), pur[0].animate.set_value(0),
                  bar.cx.animate.set_value(2.4), neu[1].animate.set_value(1.0),
                  Transform(blab, T("share of cell\nvolume", 30, YELLOW, line_spacing=.7).move_to([2.4, 2.6, 0])),
                  run_time=1.6)
        self.at("hampster v79")
        cl = T("hamster V79 cell, in culture", 30, TEXT).move_to([-3.0, -2.7, 0])
        self.play(FadeIn(cl, shift=UP * .15), run_time=.8)
        cor = tag("computed shares; schematic shape", (3.5, -3.45))
        self.play(FadeIn(cor), run_time=.5)
        self.at("nucleus fills")
        self.play(*P.go(ng=5), run_time=.6)
        self.play(*P.go(ng=0), run_time=.5)
        self.at("27")
        self.play(pur[1].animate.set_value(.27), run_time=1.2)
        l27 = bar.side("27% nucleus", .135, PURPLE, 30)
        self.play(FadeIn(l27, shift=RIGHT * .2), run_time=.6)
        self.at("mitochondria")
        marks = VGroup(*[mito_mark(p, a) for p, a in [((-1.7, .9), .3), ((-1.4, -.4), -.5), ((-2.3, -1.2), .8), ((-3.8, -1.35), 0)]])
        mt = tag("schematic marks, not a count", (3.2, -2.85))
        self.play(FadeIn(marks, scale=.6), FadeIn(mt), run_time=.9)
        self.at("another compartment")
        tgt = np.array([2.4, bar.y(.30), 0])
        self.play(*[m.animate.scale(.35).move_to(tgt) for m in marks], run_time=1.1)
        self.play(FadeOut(marks), FadeOut(mt), run_time=.2)
        self.at("about 5")
        self.play(pk[0].animate.set_value(.27), pk[1].animate.set_value(.323), run_time=.9)
        l5 = bar.side("5% mitochondria", .30, PINK, 30)
        lo = bar.side("other cell volume", .66, TEXT, 28)
        self.play(FadeIn(l5, shift=RIGHT * .2), FadeIn(lo), run_time=.7)
        self.finish()


class _Pair(Sc):
    """The two-cell layout carried through scenes 4 to 7."""
    RW = 3.6

    def pair(self, ham=True, rod_on=True, bars=True, labels=True, rod_w=None):
        self.clk()
        out = []
        self.HP = Par(cx=-5.1, cy=.3, w=3.3, h=3.6, bg=0, ng=0)
        self.RP = Par(cx=2.2, cy=.3, w=rod_w or self.RW, h=2.3, bg=0, ng=0, ar=0)
        self.hb = Bar(-3.0, -.3, 3.6, .7)
        self.hn = self.hb.add(GREY, 0, 1, .18)
        self.hp = self.hb.add(PURPLE, 0, .27, .8)
        self.hm = self.hb.add(PINK, .27, .323, .85)
        self.rb = Bar(4.65, -.3, 3.6, .7)
        self.rn = self.rb.add(GREY, 0, 1, .18)
        self.rp = self.rb.add(PURPLE, 0, .08, .8)
        self.hamm = always_redraw(lambda: hamster(self.HP, self.T_()))
        self.rodm = always_redraw(lambda: rod(self.RP, self.T_()))
        self.hbm, self.rbm = self.hb.mob(), self.rb.mob()
        self.l27 = T("27%", 30, PURPLE).move_to([-2.5 + .4, self.hb.y(.135), 0])
        self.l5 = T("5%", 30, PINK).move_to([-2.5 + .3, self.hb.y(.297), 0])
        self.l8 = T("about 8%", 28, PURPLE).move_to([5.9, self.rb.y(.04) + .18, 0])
        self.hlab = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([-3.0, 2.3, 0])
        self.rlab = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([4.65, 2.3, 0])
        return [self.hamm, self.rodm, self.hbm, self.rbm, self.l27, self.l5, self.l8, self.hlab, self.rlab]


class S04Yeast(_Pair):
    def construct(self):
        self.clk()
        HB = Par(cx=-3.0, cy=.15, w=5.0, h=4.4, bg=0, ng=0)
        hb = Bar(2.4, -.2, 4.25, 1.0)
        hb.add(GREY, 0, 1, .18)
        hb.add(PURPLE, 0, .27, .8)
        hb.add(PINK, .27, .323, .85)
        ham = always_redraw(lambda: hamster(HB, self.T_()))
        hbm = hb.mob()
        l27 = hb.side("27% nucleus", .135, PURPLE, 30)
        l5 = hb.side("5% mitochondria", .30, PINK, 30)
        lo = hb.side("other cell volume", .66, TEXT, 28)
        cl = T("hamster V79 cell, in culture", 30, TEXT).move_to([-3.0, -2.7, 0])
        top = T("share of cell\nvolume", 30, YELLOW, line_spacing=.7).move_to([2.4, 2.6, 0])
        self.add(ham, hbm, l27, l5, lo, cl, top)
        # the rod side
        self.RP = Par(cx=2.2, cy=.3, w=3.0, h=2.3, bg=0, ng=0, ar=0)
        self.rb = Bar(4.65, -.3, 3.6, .7)
        rn = self.rb.add(GREY, 0, 1, .18)
        rp = self.rb.add(PURPLE, 0, .004, .8)
        rodm = always_redraw(lambda: rod(self.RP, self.T_()))
        arr = always_redraw(lambda: rod_arrows(self.RP))
        rbm = self.rb.mob()
        self.play(FadeOut(l27), FadeOut(l5), FadeOut(lo), FadeOut(cl), FadeOut(top),
                  HB.cx.animate.set_value(-5.1), HB.cy.animate.set_value(.3), HB.w.animate.set_value(3.3),
                  HB.h.animate.set_value(3.6), hb.cx.animate.set_value(-3.0), hb.cy.animate.set_value(-.3),
                  hb.h.animate.set_value(3.6), hb.w.animate.set_value(.7), run_time=1.1)
        hl27 = T("27%", 30, PURPLE).move_to([-2.1, hb.y(.135), 0])
        hl5 = T("5%", 30, PINK).move_to([-2.2, hb.y(.297), 0])
        hlab = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([-3.0, 2.3, 0])
        rlab = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([4.65, 2.3, 0])
        self.add(arr)
        self.play(FadeIn(hl27), FadeIn(hl5), FadeIn(hlab), FadeIn(rodm, scale=.9), FadeIn(rbm), FadeIn(rlab),
                  run_time=.8)
        self.at("grows at its ends")
        self.play(self.RP.ar.animate.set_value(1), run_time=.3)
        self.play(*self.RP.go(w=3.3), run_time=1.5)
        self.play(self.RP.ar.animate.set_value(0), run_time=.3)
        self.at("its nucleus")
        self.play(*self.RP.go(ng=5), run_time=.5)
        self.play(*self.RP.go(ng=0), run_time=.3)
        self.at("about 8")
        self.play(rp[1].animate.set_value(.08), run_time=.8)
        l8 = T("about 8%", 28, PURPLE).move_to([5.9, self.rb.y(.04) + .18, 0])
        cor = tag("schematic; mean 0.080 ± 0.013", (3.0, -3.45))
        self.play(FadeIn(l8, shift=RIGHT * .2), FadeIn(cor), run_time=.5)
        self.at("grows with the cell")
        self.play(self.RP.ar.animate.set_value(1), *self.RP.go(w=3.6, ng=3), run_time=1.6)
        self.play(*self.RP.go(ng=0), self.RP.ar.animate.set_value(0), run_time=.3)
        self.at("share holds")
        sh = T("share holds", 30, YELLOW).move_to([4.65, 3.2, 0])
        self.play(FadeIn(sh, shift=DOWN * .2), run_time=.6)
        self.play(Indicate(sh, color=YELLOW, scale_factor=1.1), run_time=.8)
        self.finish()


class S05Predict(_Pair):
    def construct(self):
        items = self.pair()
        self.add(*items)
        self.wait(.3)
        self.at("two very different answers")
        self.play(Indicate(self.l27, scale_factor=1.35), Indicate(self.l8, scale_factor=1.35), run_time=1.1)
        self.at("so which number")
        card = T("Which nuclear share?", 34, YELLOW).move_to([0, 3.25, 0])
        self.play(FadeIn(card, shift=DOWN * .2), run_time=.7)
        self.at("27")
        self.play(Indicate(self.l27, scale_factor=1.4), run_time=.8)
        self.at("or 8")
        self.play(Indicate(self.l8, scale_factor=1.4), run_time=.8)
        self.at("pause and decide")
        self.play(Indicate(card, color=YELLOW, scale_factor=1.08), run_time=.9)
        self.finish()


class S06Think(_Pair):
    def construct(self):
        items = self.pair()
        card = T("Which nuclear share?", 34, YELLOW).move_to([0, 3.25, 0])
        self.add(*items, card)
        self.finish()


class S07Reveal(_Pair):
    def construct(self):
        items = self.pair()
        card = T("Which nuclear share?", 34, YELLOW).move_to([0, 3.25, 0])
        self.add(*items, card)
        t1 = lab("hamster V79", 28, TEXT, (-3.0, -2.55))
        t2 = lab("fission yeast", 28, TEXT, (4.65, -2.55))
        self.play(FadeOut(card), FadeIn(t1, shift=UP * .2), FadeIn(t2, shift=UP * .2), run_time=.7)
        self.at("no universal")
        gb = Bar(-.55, -.3, 3.6, .7)
        gm = gb.mob()
        gl = T("any cell?", 28, TEXT).move_to([-.55, 1.95, 0])
        self.play(FadeIn(gm), FadeIn(gl), run_time=.8)
        self.at("nuclear fraction")
        x = VGroup(Line([-1.0, 1.4, 0], [-.1, -2.0, 0]), Line([-1.0, -2.0, 0], [-.1, 1.4, 0])).set_stroke(YELLOW, 8)
        self.play(Create(x), run_time=.8)
        self.play(FadeOut(x), FadeOut(gm), FadeOut(gl), run_time=.7)
        self.at("with its cell type attached")
        self.play(Indicate(t1, scale_factor=1.15), Indicate(t2, scale_factor=1.15), run_time=1.0)
        self.at("carry the cell type")
        k1 = Line([-3.0 + .9, -2.3, 0], [-2.3, self.hb.y(.135) - .2, 0], color=TEXT, stroke_width=2.5)
        k2 = Line([4.65 - .6, -2.3, 0], [5.4, self.rb.y(.04) - .05, 0], color=TEXT, stroke_width=2.5)
        self.play(Create(k1), Create(k2), run_time=.9)
        self.play(Indicate(t1, scale_factor=1.15), Indicate(t2, scale_factor=1.15), run_time=.9)
        self.finish()


def dna_arrows(a_on=1, b_on=1):
    pass


class S08Dna(_Pair):
    def construct(self):
        items = self.pair()
        self.add(*items)
        t1 = lab("hamster V79", 28, TEXT, (-3.0, -2.55))
        t2 = lab("fission yeast", 28, TEXT, (4.65, -2.55))
        self.add(t1, t2)
        self.play(FadeOut(VGroup(self.hamm, self.hbm, self.l27, self.l5, self.hlab, t1)),
                  FadeOut(VGroup(self.rbm, self.l8, self.rlab, t2)),
                  *self.RP.go(cx=0, cy=.1, w=6.8, h=3.0), run_time=1.7)
        self.at("the dna")
        a1 = Arrow([-2.5, 2.1, 0], [-.4, .5, 0], buff=0, color=YELLOW, stroke_width=6)
        l1 = lab("the DNA?", 30, YELLOW, (-3.1, 2.55))
        self.play(FadeIn(l1), GrowArrow(a1), run_time=.8)
        self.at("the cell around it")
        a2 = Arrow([3.0, -2.2, 0], [.55, -.35, 0], buff=0, color=YELLOW, stroke_width=6)
        l2 = lab("the cell?", 30, YELLOW, (3.5, -2.55))
        self.play(FadeIn(l2), GrowArrow(a2), run_time=.8)
        self.play(Indicate(a1, color=YELLOW, scale_factor=1.12), run_time=.6)
        self.play(Indicate(a2, color=YELLOW, scale_factor=1.12), run_time=.6)
        self.at("design problem below")
        ch = VGroup(Line([-.5, -3.0, 0], [0, -3.45, 0]), Line([0, -3.45, 0], [.5, -3.0, 0])).set_stroke(YELLOW, 9)
        yt = T("your turn", 30, YELLOW).move_to([1.7, -3.2, 0])
        self.play(FadeIn(ch, shift=DOWN * .2), FadeIn(yt), run_time=.7)
        self.play(Indicate(a1, color=YELLOW, scale_factor=1.12), run_time=.5)
        self.play(Indicate(a2, color=YELLOW, scale_factor=1.12), run_time=.5)
        self.finish()


class S09Hold(_Pair):
    def construct(self):
        self.pair()
        self.RP.cx.set_value(0); self.RP.cy.set_value(.1); self.RP.w.set_value(6.8); self.RP.h.set_value(3.0)
        a1 = Arrow([-2.5, 2.1, 0], [-.4, .5, 0], buff=0, color=YELLOW, stroke_width=6)
        l1 = lab("the DNA?", 30, YELLOW, (-3.1, 2.55))
        a2 = Arrow([3.0, -2.2, 0], [.55, -.35, 0], buff=0, color=YELLOW, stroke_width=6)
        l2 = lab("the cell?", 30, YELLOW, (3.5, -2.55))
        ch = VGroup(Line([-.5, -3.0, 0], [0, -3.45, 0]), Line([0, -3.45, 0], [.5, -3.0, 0])).set_stroke(YELLOW, 9)
        yt = T("your turn", 30, YELLOW).move_to([1.7, -3.2, 0])
        grp = VGroup(a1, l1, a2, l2, ch, yt)
        self.add(self.rodm, grp)
        self.play(Indicate(a1, color=YELLOW, scale_factor=1.12), run_time=.6)
        self.play(Indicate(a2, color=YELLOW, scale_factor=1.12), run_time=.6)
        self.play(FadeOut(grp), FadeOut(self.rodm), *self.RP.go(cx=-8.5), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------- plant
def root_layout():
    P = Par(cx=-1.6, cy=-.4, w=4.2, h=4.0, vf=.35, lob=.45)
    return P


class S10Plant(Sc):
    def construct(self):
        self.clk()
        P = root_layout()
        P.vf.set_value(.02)
        bar = Bar(2.5, -.4, 3.8, .8)
        bar.add(GREY, 0, 1, .18)
        band = bar.add(TEAL, .3, .3, .55)
        rm = always_redraw(lambda: root(P, self.T_()))
        self.add(rm)
        self.wait(.2)
        self.play(FadeIn(rm, scale=.9), run_time=1.2)
        self.at("take the outer layer")
        tip = VGroup(RoundedRectangle(corner_radius=.35, width=.8, height=1.5, stroke_color=TEXT, stroke_width=3, fill_opacity=0),
                     RoundedRectangle(corner_radius=.35, width=.8, height=1.5, stroke_color=TAN, stroke_width=9, fill_opacity=0)
                     ).move_to([-5.95, 2.55, 0])
        tl = T("root, outer layer", 28, TEXT).move_to([-3.6, 3.3, 0])
        ar = Arrow([-5.4, 2.1, 0], [-3.7, 1.5, 0], buff=0, color=TEXT, stroke_width=4)
        self.play(FadeIn(tip), FadeIn(tl), GrowArrow(ar), run_time=1.0)
        self.at("in young cells")
        self.play(P.vf.animate.set_value(.35), run_time=1.2)
        bm = bar.mob()
        top = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([2.5, 2.45, 0])
        self.play(FadeIn(bm), FadeIn(top), run_time=.6)
        self.at("thirty to forty percent")
        self.play(band[1].animate.set_value(.4), run_time=1.0)
        vl = bar.side("vacuole:\nabout 30–40%", .35, TEAL, 28)
        vo = bar.side("outside vacuole", .72, TEXT, 28)
        cor = tag("measured range; schematic shape", (3.1, -3.45))
        self.play(FadeIn(vl, shift=RIGHT * .2), FadeIn(vo), FadeIn(cor), run_time=.8)
        self.finish()


class S11Elongate(Sc):
    def construct(self):
        self.clk()
        P = root_layout()
        bar = Bar(2.5, -.4, 3.8, .8)
        bar.add(GREY, 0, 1, .18)
        band = bar.add(TEAL, .3, .4, .55)
        rm = always_redraw(lambda: root(P, self.T_()))
        bm = bar.mob()
        top = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([2.5, 2.45, 0])
        tip = VGroup(RoundedRectangle(corner_radius=.35, width=.8, height=1.5, stroke_color=TEXT, stroke_width=3, fill_opacity=0),
                     RoundedRectangle(corner_radius=.35, width=.8, height=1.5, stroke_color=TAN, stroke_width=9, fill_opacity=0)
                     ).move_to([-5.95, 2.55, 0])
        tl = T("root, outer layer", 28, TEXT).move_to([-3.6, 3.3, 0])
        ar = Arrow([-5.4, 2.1, 0], [-3.7, 1.5, 0], buff=0, color=TEXT, stroke_width=4)
        vl = bar.side("vacuole:\nabout 30–40%", .35, TEAL, 28)
        vo = bar.side("outside vacuole", .72, TEXT, 28)
        cor = tag("measured range; schematic shape", (3.1, -3.45))
        old = VGroup(tip, tl, ar, vl, vo, cor, top)
        self.add(rm, bm, old)
        self.wait(.2)
        top2 = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([4.6, 2.55, 0])
        self.play(FadeOut(old), *P.go(cx=-1.0, cy=.2, w=7.8, h=3.4), bar.cx.animate.set_value(4.6), bar.cy.animate.set_value(.2),
                  FadeIn(top2), run_time=1.8)
        self.at("vacuolar occupancy")
        self.play(*P.go(vf=.85, lob=.08), band[0].animate.set_value(.8), band[1].animate.set_value(.9), run_time=3.2)
        vl2 = bar.side("vacuole\n80–90%", .85, TEAL, 28)
        vl2.set_y(bar.y(.85) - .45)
        self.play(FadeIn(vl2, shift=RIGHT * .2), run_time=.5)
        self.at("14")
        r1 = T("cell volume:\nabout × 14", 28, TEXT, line_spacing=.7).move_to([-3.3, -2.55, 0])
        self.play(FadeIn(r1, shift=UP * .2), run_time=.7)
        self.play(Indicate(r1, scale_factor=1.12), run_time=.7)
        self.at("2 to 3")
        r2 = T("outside vacuole:\nabout × 2–3", 28, TEXT, line_spacing=.7).move_to([1.4, -2.55, 0])
        self.play(FadeIn(r2, shift=UP * .2), run_time=.7)
        self.play(Indicate(r2, scale_factor=1.12), run_time=.7)
        cor2 = tag("schematic shape; ratios as measured", (2.4, -3.5))
        self.play(FadeIn(cor2), run_time=.4)
        self.finish()


def elong_state(sc):
    P = Par(cx=-1.0, cy=.2, w=7.8, h=3.4, vf=.85, lob=.08)
    bar = Bar(4.6, .2, 3.8, .8)
    bar.add(GREY, 0, 1, .18)
    band = bar.add(TEAL, .8, .9, .55)
    return P, bar, band


class S12Cost(Sc):
    def construct(self):
        self.clk()
        P, bar, band = elong_state(self)
        rm = always_redraw(lambda: root(P, self.T_()))
        bm = bar.mob()
        top2 = T("share of\ncell volume", 28, TEXT, line_spacing=.7).move_to([4.6, 2.55, 0])
        vl2 = bar.side("vacuole\n80–90%", .85, TEAL, 28)
        vl2.set_y(bar.y(.85) - .45)
        cor = tag("schematic", (5.0, -3.45))
        self.add(rm, bm, top2, vl2, cor)
        self.wait(.3)
        self.at("vacuolar")
        self.play(P.lob.animate.set_value(.18), rate_func=there_and_back, run_time=1.2)
        self.at("outside")
        outline = RoundedRectangle(corner_radius=.2, width=7.4, height=3.0, stroke_color=ORANGE, stroke_width=5,
                                   fill_opacity=0).move_to([-1.0, .2, 0])
        self.play(Create(outline), run_time=.8)
        self.play(FadeOut(outline), run_time=.5)
        self.at("relatively little new")
        pts = [(-4.2, 1.45), (-3.0, -1.4), (-.8, 1.45), (1.2, -1.42), (2.5, 1.45)]
        nd = VGroup(*[Dot([x, y, 0], radius=.11, color=ORANGE) for x, y in pts])
        self.play(FadeIn(nd, scale=.4), run_time=.8)
        self.play(Indicate(nd, color=ORANGE, scale_factor=1.5), run_time=.8)
        self.at("biosynthetic cost")
        tg = lab("eases a synthesis cost", 28, YELLOW, (-1.0, -2.45))
        ln = Line([-1.0, -2.1, 0], [-.8, -1.55, 0], color=YELLOW, stroke_width=3)
        self.play(FadeIn(tg), Create(ln), run_time=.8)
        self.finish()


class S13Hold(Sc):
    def construct(self):
        self.clk()
        P, bar, band = elong_state(self)
        rm = always_redraw(lambda: root(P, self.T_()))
        bm = bar.mob()
        self.add(rm, bm)
        self.play(*P.go(cx=0, cy=.35, w=3.6, h=4.0, vf=.5, lob=.25), bar.cx.animate.set_value(7.5),
                  FadeOut(bm), run_time=2.0)
        self.play(FadeOut(rm), run_time=.4)
        self.finish()


# ----------------------------------------------------------------- parts of a cell
CY = .35
CX = (-4.3, 0.0, 4.3)


def sil(kind, cx, stroke=TEXT, sw=3, wall=False):
    if kind == "animal":
        return Ellipse(width=3.4, height=3.8, stroke_color=stroke, stroke_width=sw, fill_color=ORANGE, fill_opacity=.1).move_to([cx, CY, 0])
    if kind == "plant":
        return RoundedRectangle(corner_radius=.3, width=3.4, height=3.8, stroke_color=stroke, stroke_width=sw, fill_color=ORANGE, fill_opacity=.1).move_to([cx, CY, 0])
    return Ellipse(width=3.2, height=3.4, stroke_color=stroke, stroke_width=sw, fill_color=ORANGE, fill_opacity=.1).move_to([cx, CY, 0])


def wall_of(kind, cx):
    s = sil(kind, cx, TAN, 14)
    s.set_fill(opacity=0)
    return s


def wavy(c, w=1.0):
    p = [c + np.array([x * w, .12 * math.sin(x * 9) * w, 0]) for x in np.linspace(-.5, .5, 30)]
    return VMobject().set_points_smoothly(p).set_stroke(GREY, 4).set_color("#B9BFCB")


def marks(kind, cx):
    c = np.array([cx, CY, 0])
    if kind == "nucleus":
        return VGroup(Circle(.55, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=.4).move_to(c + [-.3, .45, 0]))
    if kind == "mito":
        return VGroup(*[mito_mark(c + [p[0], p[1], 0], a) for p, a in [((.7, .6), .3), ((.5, -.5), -.4), ((-.7, -.65), .2)]])
    if kind == "er":
        return VGroup(wavy(c + [.35, .3, 0], 1.1), wavy(c + [.4, .05, 0], 1.0), wavy(c + [.3, -.2, 0], 1.1)).set_stroke("#B9BFCB", 4)
    if kind == "golgi":
        return VGroup(*[Arc(radius=.7 - .06 * i, start_angle=PI * .15, angle=PI * .7, color="#B9BFCB", stroke_width=5).move_to(c + [.5, -.55 + .17 * i, 0]) for i in range(4)])
    if kind == "cyto":
        return VGroup(*[Line(c + [-1.1, -.9 + .55 * i, 0], c + [1.1, -.6 + .5 * i, 0], color=TEXT, stroke_width=2).set_opacity(.45) for i in range(4)])
    if kind == "chloro":
        return VGroup(*[Ellipse(width=.62, height=.34, stroke_color=LEAF, stroke_width=3, fill_color=LEAF, fill_opacity=.85).move_to(c + [p[0], p[1], 0]).rotate(a)
                        for p, a in [((.8, .7), .3), ((-.85, -.3), -.5), ((.6, -.85), .2), ((-.7, .9), .5)]])
    if kind == "vac":
        return VGroup(vac_poly(cx, CY - .1, 2.0, 1.7, .3, 0))
    if kind == "yvac":
        return VGroup(Ellipse(width=.9, height=.8, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=.55).move_to(c + [.5, -.3, 0]))
    return VGroup()


class S14Parts(Sc):
    def construct(self):
        self.clk()
        kinds = ["animal", "plant", "yeast"]
        sils = [sil(k, x) for k, x in zip(kinds, CX)]
        names = [T(n, 30, TEXT).move_to([x, -2.0, 0]) for n, x in zip(["animal", "plant leaf", "yeast"], CX)]
        for s in sils:
            s.add_updater(lambda m, dt: m.scale(1 + .0006 * math.cos(self.T_() * 2.0)))
        self.play(*[Create(s) for s in sils], *[FadeIn(n) for n in names], run_time=1.6)
        cor = tag("schematic", (5.6, -3.5))
        self.add(cor)

        cat = [None]

        def show(items, text, pulse=True):
            outs = []
            if cat[0] is not None:
                outs.append(FadeOut(cat[0]))
            grp = VGroup(*items)
            lb = lab(text, 30, TEXT, (0, -3.0))
            self.play(*outs, FadeIn(grp, scale=.9), FadeIn(lb), run_time=.55)
            cat[0] = VGroup(grp, lb)
            return grp

        def clear():
            if cat[0] is not None:
                self.play(FadeOut(cat[0]), run_time=.35)
                cat[0] = None

        self.at("plasma membrane")
        memlab = lab("plasma membrane", 30, BLUE, (0, -3.0))
        self.play(*[s.animate.set_stroke(BLUE, 7) for s in sils], FadeIn(memlab), run_time=.7)
        self.at("nucleus")
        self.play(FadeOut(memlab), run_time=.2)
        show([marks("nucleus", x) for x in CX], "nucleus")
        self.at("mitochondria")
        show([marks("mito", x) for x in CX], "mitochondria")
        self.at("er")
        show([marks("er", x) for x in CX], "ER")
        self.at("golgi")
        show([marks("golgi", x) for x in CX], "Golgi")
        self.at("cytoskeleton")
        show([marks("cyto", x) for x in CX], "cytoskeleton")
        self.at("for these core parts")
        clear()
        self.play(*[s.animate.set_stroke(BLUE, 4) for s in sils], run_time=.4)
        self.at("walls")
        show([wall_of("plant", CX[1]), wall_of("yeast", CX[2])], "walls")
        self.at("plastids")
        pl = marks("chloro", CX[1])
        show([pl], "plastids")
        self.at("vacuoles")
        show([marks("vac", CX[1]), marks("yvac", CX[2])], "vacuoles")
        self.at("root cell")
        clear()
        rl = T("plant root", 30, TEXT).move_to([CX[1], -2.0, 0])
        pl2 = marks("chloro", CX[1])
        self.play(Transform(names[1], rl), FadeIn(pl2), run_time=.6)
        self.at("has plastids")
        self.play(*[m.animate.set_fill(PLASTID, .8).set_stroke(PLASTID) for m in pl2], run_time=1.2)
        self.at("no chloroplasts")
        fin = lab("plastids, no chloroplasts", 30, TEXT, (0, -3.0))
        self.play(FadeIn(fin), Indicate(pl2, color=PLASTID, scale_factor=1.15), run_time=.9)
        self.finish()


# ----------------------------------------------------------------- return
class S15Return(Sc):
    def construct(self):
        self.clk()
        R = Par(cx=0, cy=1.1, w=4.2, h=2.6, bg=0, ng=0, ar=0)
        rm = always_redraw(lambda: rod(R, self.T_()))
        ro = T("nucleus\nabout 8%", 30, PURPLE, line_spacing=.7).move_to([5.0, 1.1, 0])
        self.add(rm)
        self.play(*R.go(w=6.4), FadeIn(ro), run_time=3.9)
        self.at("shares are")
        b1 = Bar(-5.3, -1.9, 2.2, .6)
        b1.add(GREY, 0, 1, .18)
        p1 = b1.add(PURPLE, 0, .004, .8)
        b2 = Bar(-.9, -1.9, 2.2, .6)
        b2.add(GREY, 0, 1, .18)
        b2.add(PURPLE, 0, .08, .8)
        b3 = Bar(3.7, -1.9, 2.2, .6)
        b3.add(GREY, 0, 1, .18)
        t3 = b3.add(TEAL, .3, .4, .55)
        H = Par(cx=-3.6, cy=-1.9, w=1.9, h=1.8, bg=0, ng=0)
        Q = Par(cx=1.1, cy=-1.9, w=1.8, h=1.0, bg=0, ng=0, ar=0)
        S = Par(cx=5.4, cy=-1.9, w=1.4, h=1.2, vf=.35, lob=.45)
        hm = always_redraw(lambda: hamster(H, self.T_()))
        qm = always_redraw(lambda: rod(Q, self.T_()))
        sm = always_redraw(lambda: self.root_mini(S))
        l1 = T("hamster V79", 28, TEXT).move_to([-4.5, -3.4, 0])
        l2 = T("share holds", 28, TEXT).move_to([.0, -3.4, 0])
        l3 = T("mostly vacuolar", 28, TEXT).move_to([4.5, -3.4, 0])
        self.play(FadeIn(b1.mob()), FadeIn(hm), FadeIn(l1), p1[1].animate.set_value(.27), run_time=.6)
        self.at("specific")
        self.play(FadeIn(b2.mob()), FadeIn(qm), FadeIn(l2), run_time=.8)
        self.at("elongating")
        self.play(FadeIn(b3.mob()), FadeIn(sm), FadeIn(l3), run_time=.7)
        self.play(*S.go(w=2.2, h=1.3, vf=.85, lob=.08), *Q.go(w=2.5), t3[0].animate.set_value(.8),
                  t3[1].animate.set_value(.9), run_time=3.0)
        self.finish()

    def root_mini(self, P):
        cx, cy, w, h = P.v("cx"), P.v("cy"), P.v("w"), P.v("h")
        mem = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=BLUE, stroke_width=4,
                               fill_color=ORANGE, fill_opacity=.18).move_to([cx, cy, 0])
        wall = RoundedRectangle(corner_radius=.14, width=w + .1, height=h + .1, stroke_color=TAN, stroke_width=8,
                                fill_opacity=0).move_to([cx, cy, 0])
        s = math.sqrt(P.v("vf"))
        vac = vac_poly(cx, cy, (w - .2) * s, (h - .2) * s, P.v("lob"), self.T_())
        return VGroup(wall, mem, vac)


class S16End(EndCard):
    LINE = "A compartment's share of cell volume depends on cell type and growth."
