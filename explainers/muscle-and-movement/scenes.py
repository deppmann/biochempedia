"""Muscle, bone and movement: filaments slide, nothing shortens  (Biochemistrypedia organismal biology explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = myosin: thick filaments, myosin heads, the binding sites on actin
  GREEN  = actin: thin filaments
  YELLOW = calcium
  ORANGE = ATP
  PURPLE = troponin and tropomyosin
  TEAL   = the nerve signal: motor neuron, acetylcholine, membrane, T tubules, voltage sensor
  PINK   = the sarcoplasmic reticulum (the calcium store), its release channel and pumps
  RED    = the problem, "no", blocked
  GREY   = outlines, sarcomere end bars, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB3"


def arr(a, b, color=GREY, w=6, tip=0.24):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=14)


def bar(x1, x2, y, h, color, op=0.5, r=0.06):
    """A horizontal rounded bar from x1 to x2 centred on y (a filament)."""
    return RoundedRectangle(corner_radius=min(r, h / 2.2), width=abs(x2 - x1), height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([(x1 + x2) / 2, y, 0])


def vbar(x, y1, y2, w, color, op=0.35, r=0.08):
    return RoundedRectangle(corner_radius=r, width=w, height=abs(y2 - y1), stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, (y1 + y2) / 2, 0])


def dot(x, y, color, r=0.14):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])


def run_dot(points, color=TEAL, rt=2.0, r=0.17):
    pts = [np.array([p[0], p[1], 0.0]) for p in points]
    d = dot(pts[0][0], pts[0][1], color, r)
    pm = VMobject()
    pm.set_points_as_corners(pts)
    return d, MoveAlongPath(d, pm, run_time=rt, rate_func=linear)


# ---- the sarcomere schematic (not to scale) -----------------------------------------------------
THICK_Y = (0.65, -0.65)
THIN_Y = (1.3, 0.0, -1.3)
THICK_HALF = 2.7
THIN_LEN = 3.2
D_REST, D_SHORT = 4.5, 3.5


def z_bars(d, cy=0.0):
    return VGroup(vbar(-d, cy - 1.75, cy + 1.75, 0.16, GREY, 0.7, 0.05), vbar(d, cy - 1.75, cy + 1.75, 0.16, GREY, 0.7, 0.05))


def thick_bars(cy=0.0):
    return VGroup(*[bar(-THICK_HALF, THICK_HALF, cy + y, 0.4, BLUE, 0.55) for y in THICK_Y])


def thin_bars(d, cy=0.0):
    left = [bar(-d, -d + THIN_LEN, cy + y, 0.22, GREEN, 0.6) for y in THIN_Y]
    right = [bar(d - THIN_LEN, d, cy + y, 0.22, GREEN, 0.6) for y in THIN_Y]
    return VGroup(*left, *right)


def sarcomere(d, cy=0.0):
    return VGroup(z_bars(d, cy), thick_bars(cy), thin_bars(d, cy))


def span_marker(x1, x2, y, label, color, size=26, up=False):
    """A bracket-like double arrow with a label, for a width that should be seen not changing or changing."""
    a = Line([x1, y, 0], [x2, y, 0], color=color, stroke_width=5)
    t1 = Line([x1, y - 0.15, 0], [x1, y + 0.15, 0], color=color, stroke_width=5)
    t2 = Line([x2, y - 0.15, 0], [x2, y + 0.15, 0], color=color, stroke_width=5)
    lab = T(label, size, color)
    lab.next_to(a, UP if up else DOWN, buff=0.2)
    return VGroup(a, t1, t2), lab


def head_mob(top, bot, color=BLUE, w=9):
    """A myosin head: a stalk from the thick filament to a blob at the lower end."""
    ln = Line([top[0], top[1], 0], [bot[0], bot[1], 0], color=color, stroke_width=w)
    bl = Circle(radius=0.2, stroke_width=0, fill_color=color, fill_opacity=1).move_to([bot[0], bot[1], 0])
    return VGroup(ln, bl)


def scope():
    return T("vertebrate skeletal muscle", 22, GREY).move_to([4.6, 3.4, 0])


class S00Title(TitleCard):
    LESSON = "Muscle, bone and movement"
    TITLE = "Filaments slide, nothing shortens"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """A fibre shortens, no filament does; the fibre is chains of sarcomeres holding thick and thin filaments."""

    def construct(self):
        Y = 0.6
        head = T("vertebrate skeletal muscle", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        fibre = RoundedRectangle(corner_radius=0.5, width=10.8, height=1.8, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.2).move_to([0, Y, 0])
        flab = T("muscle fibre", 28, GREY).move_to([0, Y - 1.5, 0])
        short = RoundedRectangle(corner_radius=0.5, width=8.4, height=1.8, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.2).move_to([0, Y, 0])
        ghost = fibre.copy().set_stroke(GREY, opacity=0.4, width=3).set_fill(opacity=0)
        a1 = arr([-6.3, Y], [-5.65, Y], RED)
        a2 = arr([6.3, Y], [5.65, Y], RED)
        self.at("fiber shortens")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(fibre), FadeIn(flab), run_time=0.6)
        self.add(ghost)
        self.play(Transform(fibre, short), flab.animate.move_to([0, Y - 1.5, 0]), run_time=0.9)
        self.at("none of its filaments")
        c1 = chip("no filament gets shorter", RED, 34).move_to([0, -2.0, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("how can that be")
        c2 = chip("how?", RED, 44, pad=0.3).move_to([5.0, -2.0, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("one long cell")
        full = fibre.copy().become(ghost).set_fill(GREY, opacity=0.2).set_stroke(GREY, opacity=1, width=4)
        self.play(FadeOut(c1), FadeOut(c2), Transform(fibre, full), FadeOut(ghost), run_time=0.9)
        self.at("repeating units")
        xs = [-4.32, -2.16, 0, 2.16, 4.32]
        divs = VGroup(*[Line([x, Y - 0.9, 0], [x, Y + 0.9, 0], color=GREY, stroke_width=4) for x in xs])
        units = T("sarcomeres", 30, GREY).move_to([0, -1.8, 0])
        self.play(Create(divs), FadeOut(flab), FadeIn(units), run_time=1.2)
        self.at("each sarcomere holds")
        mid = bar(-1.08, 1.08, Y, 1.8, GREY, 0.0, 0.1)  # the middle unit, which opens up
        self.play(FadeOut(head), FadeOut(fibre), FadeOut(divs), FadeOut(units), run_time=0.7)
        z = z_bars(D_REST)
        brace, blab = span_marker(-D_REST, D_REST, -2.65, "one sarcomere (not to scale)", GREY, 26)
        self.play(FadeIn(z), FadeIn(brace), FadeIn(blab), run_time=0.8)
        self.at("thick filaments")
        tk = thick_bars()
        tl = T("thick filaments: myosin", 28, BLUE).move_to([0, 2.55, 0])
        self.play(GrowFromCenter(tk), FadeIn(tl, shift=DOWN * 0.1), run_time=0.9)
        self.at("thin filaments")
        tn = thin_bars(D_REST)
        gl = T("thin filaments: actin", 28, GREEN).move_to([-4.2, 2.55, 0])
        self.play(*[GrowFromEdge(m, LEFT if i < 3 else RIGHT) for i, m in enumerate(tn)], FadeIn(gl, shift=DOWN * 0.1), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
FIB_X1, FIB_X2, MEM_Y, FIB_Y2 = -5.6, 5.6, 0.6, -3.4
TUB_X = [-1.2, 1.6, 4.4]
TUB_BOT = -2.2


def fibre_base():
    fib = Rectangle(width=FIB_X2 - FIB_X1, height=MEM_Y - FIB_Y2, stroke_color=GREY, stroke_width=3,
                    fill_color=GREY, fill_opacity=0.1).move_to([(FIB_X1 + FIB_X2) / 2, (MEM_Y + FIB_Y2) / 2, 0])
    mem = Line([FIB_X1, MEM_Y, 0], [FIB_X2, MEM_Y, 0], color=TEAL, stroke_width=7)
    tubs = VGroup(*[vbar(x, TUB_BOT, MEM_Y, 0.22, TEAL, 0.4, 0.06) for x in TUB_X])
    return fib, mem, tubs


class S02Signal(SpokenScene):
    """Neuromuscular junction, acetylcholine, action potential along the membrane and down the T tubules."""

    def construct(self):
        self.add(scope())
        fib, mem, tubs = fibre_base()
        fl = T("muscle fibre", 28, GREY).move_to([-3.9, -2.9, 0])
        mn = chip("motor neuron", TEAL, 30).move_to([-3.5, 3.0, 0])
        ax = vbar(-3.5, 1.35, 2.5, 0.3, TEAL, 0.35, 0.08)
        bulb = Circle(radius=0.38, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35).move_to([-3.5, 1.2, 0])
        nj = T("neuromuscular junction", 28, TEAL).move_to([-0.1, 1.45, 0])
        nj_l = arr([-1.6, 1.4], [-3.0, 1.0], TEAL, 3, 0.15)
        self.at("neuromuscular junction")
        self.play(FadeIn(fib), Create(mem), FadeIn(fl), FadeIn(mn), FadeIn(ax), FadeIn(bulb), run_time=1.0)
        self.play(FadeIn(nj), Create(nj_l), run_time=0.7)
        self.at("motor neuron meets")
        self.play(Indicate(mn, color=TEAL, scale_factor=1.1), run_time=0.6)
        self.at("releases acetylcholine")
        ach = VGroup(*[dot(-3.5 + dx, 0.95, TEAL, 0.09) for dx in (-0.25, 0, 0.25)])
        self.play(FadeIn(ach), run_time=0.3)
        self.play(*[a.animate.move_to([-3.5 + dx, 0.72, 0]) for a, dx in zip(ach, (-0.25, 0, 0.25))], run_time=0.9)
        al = T("acetylcholine", 26, TEAL).move_to([-5.3, 0.95, 0]).set_opacity(1)
        self.play(FadeIn(al), run_time=0.4)
        self.at("opens channels")
        seg = Line([-4.1, MEM_Y, 0], [-2.9, MEM_Y, 0], color=YELLOW if False else TEXT, stroke_width=9)
        self.play(Create(seg), run_time=0.5)
        self.play(FadeOut(seg), FadeOut(ach), FadeOut(al), run_time=0.4)
        self.at("travels along")
        d1, a1 = run_dot([[-3.5, MEM_Y], [FIB_X1 + 0.2, MEM_Y]], rt=1.2, r=0.2)
        d2, a2 = run_dot([[-3.5, MEM_Y], [FIB_X2 - 0.2, MEM_Y]], rt=3.2, r=0.2)
        self.add(d1, d2)
        apl = T("action potential", 28, TEAL).move_to([4.4, 1.4, 0])
        self.play(a1, a2, FadeIn(apl), run_time=3.2)
        self.remove(d1, d2)
        self.at("tubules which are")
        self.play(FadeOut(apl), FadeIn(tubs), run_time=0.8)
        tl = T("T tubules: infoldings of the membrane", 26, TEAL).move_to([1.6, -2.85, 0])
        self.play(FadeIn(tl), run_time=0.5)
        ds = []
        anims = []
        for x in TUB_X:
            d, a = run_dot([[x, MEM_Y], [x, TUB_BOT + 0.15]], rt=1.6, r=0.17)
            ds.append(d)
            anims.append(a)
        self.add(*ds)
        self.at("deep into the fiber")
        self.play(*anims)
        self.play(*[FadeOut(d) for d in ds], run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Calcium(SpokenScene):
    """The sarcoplasmic reticulum, the voltage sensor linked to the release channel, calcium floods out."""

    def construct(self):
        self.add(scope())
        fib, mem, tubs = fibre_base()
        fl = T("muscle fibre", 28, GREY).move_to([-3.9, -2.9, 0])
        mn = chip("motor neuron", TEAL, 30).move_to([-3.5, 3.0, 0])
        ax = vbar(-3.5, 1.35, 2.5, 0.3, TEAL, 0.35, 0.08)
        bulb = Circle(radius=0.38, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35).move_to([-3.5, 1.2, 0])
        self.add(fib, mem, tubs, fl, mn, ax, bulb)
        srs = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=2.0, stroke_color=PINK, stroke_width=3,
                                        fill_color=PINK, fill_opacity=0.25).move_to([x + 0.62, -0.7, 0]) for x in TUB_X])
        self.at("sarcoplasmic reticulum")
        sl = T("sarcoplasmic\nreticulum", 26, PINK, line_spacing=0.8).move_to([-3.9, -0.7, 0])
        self.play(FadeIn(srs, shift=LEFT * 0.1), FadeIn(sl), run_time=0.9)
        self.at("internal calcium store")
        cas = VGroup(*[dot(x + 0.62 + dx, -0.7 + dy, YELLOW, 0.09) for x in TUB_X for dx, dy in ((-0.15, 0.4), (0.15, 0.2), (-0.1, -0.1), (0.15, -0.3), (-0.15, -0.5))])
        sl2 = T("calcium store", 26, YELLOW).move_to([-3.9, -1.5, 0])
        self.play(FadeIn(cas), FadeIn(sl2), run_time=0.8)

        # zoom to one pair: tubule + store (large)
        self.at("voltage sensor")
        small = VGroup(fib, mem, tubs, fl, mn, ax, bulb, srs, cas, sl, sl2)
        tx = -0.6
        tub = vbar(tx, -3.0, 2.7, 0.34, TEAL, 0.4, 0.06)
        memb = Line([-5.8, 2.7, 0], [tx + 0.17, 2.7, 0], color=TEAL, stroke_width=7)
        sr = RoundedRectangle(corner_radius=0.2, width=2.4, height=3.4, stroke_color=PINK, stroke_width=4,
                              fill_color=PINK, fill_opacity=0.22).move_to([tx + 0.17 + 0.6 + 1.2, 0.0, 0])
        srx = sr.get_left()[0]
        sy = 0.9
        sensor = Rectangle(width=0.5, height=0.7, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.9).move_to([srx - 0.25, sy, 0])
        channel = Rectangle(width=0.3, height=0.7, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.9).move_to([srx + 0.15, sy, 0])
        link = Line([srx, sy - 0.35, 0], [srx, sy + 0.35, 0], color=TEXT, stroke_width=3)
        dots = VGroup(*[dot(srx + 0.55 + dx, -0.1 + dy, YELLOW, 0.1) for dx, dy in ((0, 0.9), (0.6, 0.6), (1.2, 0.9), (0.3, 0.1), (0.9, 0.2),
                                                                                  (0.3, -0.6), (1.0, -0.5), (0.6, -1.1), (1.3, -1.2), (0.2, -1.4))])
        sl_big = T("sarcoplasmic\nreticulum", 26, PINK, line_spacing=0.8).move_to([srx + 3.6, 0.3, 0])
        memlab = T("fibre membrane", 26, TEAL).move_to([-4.3, 2.3, 0])
        tublab = T("T tubule", 26, TEAL).move_to([-4.3, 1.6, 0])
        self.play(FadeOut(small), FadeIn(tub), FadeIn(memb), FadeIn(sr), FadeIn(dots), FadeIn(memlab), FadeIn(tublab), run_time=1.0)
        vs = T("voltage sensor", 28, TEAL).move_to([-4.3, sy, 0])
        vl = arr([-3.0, sy], [tx - 0.25, sy], TEAL, 3, 0.14)
        self.play(FadeIn(sensor), FadeIn(vs), Create(vl), FadeIn(sl_big), run_time=0.8)
        self.at("calcium release channel")
        cl = T("calcium release channel", 28, PINK).move_to([srx + 1.9, 2.5, 0])
        cla = arr([srx + 0.3, 2.2], [srx + 0.18, sy + 0.4], PINK, 3, 0.14)
        self.play(FadeIn(channel), FadeIn(link), FadeIn(cl), Create(cla), run_time=0.8)
        self.at("voltage changes")
        d, a = run_dot([[tx, 2.7], [tx, sy]], rt=1.3, r=0.2)
        self.add(d)
        self.play(a)
        self.remove(d)
        self.play(Indicate(sensor, color=TEXT, scale_factor=1.3), run_time=0.6)
        self.at("opens the channel")
        open_ch = Rectangle(width=0.3, height=0.7, stroke_color=PINK, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to(channel)
        self.play(Transform(channel, open_ch), run_time=0.5)
        self.at("floods out")
        outs = VGroup(*[dot(srx + 0.15, sy, YELLOW, 0.1) for _ in range(7)])
        self.add(outs)
        gx = srx - 0.45 + 0.1
        targets = [(srx + 0.4, -2.4), (srx + 1.0, -2.8), (srx + 1.6, -2.4), (srx + 2.2, -2.8), (srx + 2.8, -2.4), (srx + 3.4, -2.8), (srx + 4.0, -2.4)]
        self.play(*[o.animate.move_to([tt[0], tt[1], 0]) for o, tt in zip(outs, targets)], FadeOut(dots), run_time=2.2)
        self.at("from outside the cell")
        ncs = VGroup(arr([-5.4, 3.45], [-5.4, 2.85], YELLOW, 5, 0.18), Line([-5.7, 3.1, 0], [-5.1, 3.4, 0], color=RED, stroke_width=6),
                     Line([-5.7, 3.4, 0], [-5.1, 3.1, 0], color=RED, stroke_width=6))
        nct = T("calcium from outside:\nnot required", 26, YELLOW, line_spacing=0.8).move_to([-2.9, 3.15, 0])
        self.play(FadeIn(ncs), FadeIn(nct), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Uncover(SpokenScene):
    """Troponin, tropomyosin and the sites; calcium binds; the strand shifts; heads attach, swing, pull."""

    def construct(self):
        self.add(scope())
        TY = -0.95          # thin filament centre line
        site_x = [-3.2, -1.2, 0.8, 2.8]
        thick = bar(-5.6, 4.6, 0.8, 0.44, BLUE, 0.5)
        thick_l = T("thick filament: myosin", 28, BLUE).move_to([-3.9, 1.65, 0])
        thin = bar(-4.4, 3.8, TY, 0.3, GREEN, 0.55)
        thin_l = T("thin filament: actin", 28, GREEN).move_to([1.5, -2.35, 0])
        trop = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.42, stroke_color=PURPLE, stroke_width=3,
                                fill_color=PURPLE, fill_opacity=0.7).move_to([-2.2, TY - 0.38, 0])
        trop_l = T("troponin", 28, PURPLE).move_to([-4.0, -1.85, 0])
        sites = VGroup(*[Circle(radius=0.11, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.15).move_to([x, TY + 0.2, 0]) for x in site_x])
        strand = bar(-3.9, 3.4, TY + 0.2, 0.2, PURPLE, 0.85, 0.08)
        strand_l = T("tropomyosin", 26, PURPLE).move_to([5.2, -1.15, 0])
        # the thin filament and everything riding on it
        thin_g = VGroup(thin, trop, sites, strand)
        hang = [head_mob([x - 0.45, 0.58], [x - 0.3, -0.05]) for x in site_x]
        sites_l = T("myosin-binding\nsites", 24, BLUE, line_spacing=0.8).move_to([5.3, -0.2, 0])

        self.at("troponin is a protein")
        self.play(FadeIn(thin), FadeIn(thin_l), run_time=0.7)
        self.play(FadeIn(trop, scale=1.4), FadeIn(trop_l), run_time=0.6)
        self.at("tropomyosin")
        self.play(FadeIn(sites), GrowFromEdge(strand, LEFT), FadeIn(strand_l), run_time=0.9)
        self.at("where myosin binds")
        self.play(FadeIn(thick), FadeIn(thick_l), *[FadeIn(h) for h in hang], run_time=0.9)
        sblk = VGroup(*[Line(s.get_center() + np.array([-0.3, 0.55, 0]), s.get_center() + np.array([0.3, 0.55, 0]), color=RED, stroke_width=1) for s in sites])
        self.play(FadeIn(sites_l), run_time=0.4)
        self.at("calcium binds troponin")
        ca = VGroup(*[dot(-4.7 + 0.45 * i, -3.0 + 0.35 * i, YELLOW, 0.13) for i in range(3)])
        cal = T("calcium", 28, YELLOW).move_to([-5.6, -3.0, 0])
        self.play(FadeIn(ca), FadeIn(cal), run_time=0.4)
        self.play(*[c.animate.move_to([-2.2 + 0.28 * (i - 1), TY - 0.78 + 0.05 * i, 0]) for i, c in enumerate(ca)], run_time=1.2)
        self.play(trop.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), FadeOut(cal), run_time=0.5)
        self.at("shifts tropomyosin")
        self.play(strand.animate.shift(DOWN * 0.34), strand_l.animate.shift(DOWN * 0.0), run_time=1.0)
        self.at("sites are uncovered")
        self.play(sites.animate.set_fill(BLUE, 0.95).scale(1.3), FadeOut(sites_l), run_time=0.7)
        self.at("myosin heads attach")
        att = [head_mob([x - 0.45, 0.58], [x, TY + 0.3]) for x in site_x]
        self.play(*[Transform(h, a) for h, a in zip(hang, att)], run_time=1.0)
        cb = T("attached heads: cross-bridges", 28, BLUE).move_to([2.0, 1.75, 0])
        self.at("swing")
        pulled = [head_mob([x - 0.45, 0.58], [x - 0.9, TY + 0.3]) for x in site_x]
        mid = arr([3.8, -3.3], [-5.85, -3.3], GREEN, 7, 0.28)
        midline = DashedLine([-6.0, 2.1, 0], [-6.0, -3.6, 0], color=TEXT, stroke_width=3, dash_length=0.18).set_opacity(0.6)
        midline_l = T("middle of\nsarcomere", 24, TEXT, line_spacing=0.8).move_to([-5.1, 2.7, 0])
        mid_l = T("toward the middle of the sarcomere", 26, GREEN).move_to([-0.8, -2.85, 0])
        self.play(thin_g.animate.shift(LEFT * 0.9), trop_l.animate.shift(LEFT * 0.9),
                  *[Transform(h, p) for h, p in zip(hang, pulled)], run_time=2.0)
        self.at("toward the middle")
        self.play(FadeIn(mid_l), FadeIn(mid), Create(midline), FadeIn(midline_l), run_time=0.7)
        self.at("crossbridges")
        self.play(FadeIn(cb), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Slide(SpokenScene):
    """The sarcomere shortens by sliding; A band keeps its width; two combs."""

    def construct(self):
        self.add(scope())
        cy = -0.2
        s = sarcomere(D_REST, cy)
        sm, sl = span_marker(-D_REST, D_REST, cy - 2.55, "sarcomere", GREY, 26)
        title = T("sliding filament model", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        tk_l = T("thick: myosin", 26, BLUE).move_to([0, cy + 2.15, 0])
        self.add(s, sm, sl, tk_l)
        self.at("sliding filament model")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.6)
        self.at("do not get shorter")
        keep = chip("each filament keeps its length", GREEN, 28).move_to([0, 3.0 - 0.0, 0]).shift(DOWN * 0.1)
        self.play(FadeOut(title), run_time=0.3)
        self.play(FadeIn(keep, shift=DOWN * 0.1), run_time=0.5)
        self.at("slide past each other")
        s2 = sarcomere(D_SHORT, cy)
        sm2, sl2 = span_marker(-D_SHORT, D_SHORT, cy - 2.55, "sarcomere shorter", GREY, 26)
        self.play(Transform(s, s2), Transform(sm, sm2), Transform(sl, sl2), run_time=2.2)
        self.at("A band")
        ab, abl = span_marker(-THICK_HALF, THICK_HALF, cy + 2.0, "", BLUE, 26)
        abt = T("A band: the length of the thick filaments", 26, BLUE).move_to([0, cy + 2.6, 0])
        self.play(FadeOut(tk_l), FadeOut(keep), run_time=0.4)
        self.play(Create(ab), FadeIn(abt), run_time=0.8)
        self.at("keeps its width")
        self.play(Indicate(ab, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("two combs")
        self.play(*[FadeOut(m) for m in (s, sm, sl, ab, abt)], run_time=0.7)
        # two combs: a base bar and teeth, pushed tooth into tooth
        def comb(x0, direction, ys):
            base = vbar(x0, -1.9, 1.9, 0.3, GREY, 0.6, 0.06)
            teeth = VGroup(*[bar(x0, x0 + direction * 3.2, y, 0.2, GREY, 0.5) for y in ys])
            return VGroup(base, teeth)
        cl = comb(-4.5, 1, (1.5, 0.5, -0.5, -1.5))
        cr = comb(4.5, -1, (1.0, 0.0, -1.0))
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.7)
        self.play(cl.animate.shift(RIGHT * 1.6), cr.animate.shift(LEFT * 1.6), run_time=2.0)
        self.at("keeps its length")
        ln = chip("each comb keeps its length", GREY, 28).move_to([0, 2.95, 0])
        self.play(FadeIn(ln, shift=DOWN * 0.1), run_time=0.5)
        self.at("only the overlap")
        ov = span_marker(-1.6 - 0.0, 1.6, -2.55, "overlap", TEXT, 28)
        self.play(Create(ov[0]), FadeIn(ov[1]), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Atp(SpokenScene):
    """ATP's two jobs; then no ATP and the heads stay stuck."""

    def construct(self):
        # left panel: the head
        thick = bar(-5.9, -0.7, 1.55, 0.44, BLUE, 0.5)
        thin = bar(-5.9, -0.7, -1.0, 0.3, GREEN, 0.55)
        hx = -3.5
        head = head_mob([hx - 0.45, 1.33], [hx, -0.7])
        j1 = chip("job 1: the myosin head", ORANGE, 26).move_to([-3.3, 3.0, 0])
        # right panel: the store and pumps
        sr = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.5, stroke_color=PINK, stroke_width=4,
                              fill_color=PINK, fill_opacity=0.22).move_to([3.4, 1.45, 0])
        pump = Rectangle(width=0.5, height=0.3, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.95).move_to([3.4, 0.7, 0])
        sr_l = T("store", 26, PINK).move_to([4.7, 1.45, 0]).set_opacity(0)
        j2 = chip("job 2: the calcium pumps", ORANGE, 26).move_to([3.4, 3.0, 0])
        mthin = bar(0.9, 5.9, -1.9, 0.3, GREEN, 0.55)
        msites = VGroup(*[Circle(radius=0.11, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.95).move_to([x, -1.7, 0]) for x in (1.9, 3.4, 4.9)])
        mstrand = bar(1.4, 5.4, -2.12, 0.2, PURPLE, 0.85, 0.08)

        self.at("two jobs")
        self.play(FadeIn(j1), FadeIn(thick), FadeIn(thin), FadeIn(head), run_time=0.9)
        atp = chip("ATP", ORANGE, 30).move_to([-1.6, 0.35, 0])
        self.at("binding to a myosin head")
        self.play(FadeIn(atp, shift=LEFT * 0.1), run_time=0.4)
        self.play(atp.animate.move_to([hx + 0.95, 0.2, 0]), run_time=0.9)
        self.at("releases it from actin")
        rel = head_mob([hx - 0.45, 1.33], [hx - 0.2, 0.15])
        l1 = T("ATP binds: the head lets go", 26, ORANGE).move_to([-3.3, -2.3, 0])
        self.play(Transform(head, rel), FadeIn(l1), run_time=1.0)
        self.at("splitting the")
        self.play(Indicate(atp, color=ORANGE, scale_factor=1.3), run_time=0.8)
        self.at("head for the next")
        cock = head_mob([hx - 0.45, 1.33], [hx + 0.45, 0.1])
        l2 = T("ATP split: the head is re-cocked", 26, ORANGE).move_to([-3.3, -2.95, 0])
        self.play(Transform(head, cock), FadeOut(atp), FadeOut(l1), FadeIn(l2), run_time=1.0)
        self.at("pumps in the store")
        self.play(FadeIn(j2), FadeIn(sr), FadeIn(pump), FadeIn(sr_l), run_time=0.8)
        ca = VGroup(*[dot(2.7 + 0.7 * i, -0.2 + 0.1 * (i % 2), YELLOW, 0.12) for i in range(3)])
        patp = chip("ATP", ORANGE, 26).move_to([5.0, 0.0, 0])
        self.at("use ATP")
        self.play(FadeIn(ca), FadeIn(patp, shift=LEFT * 0.1), run_time=0.5)
        self.at("move calcium back")
        self.play(patp.animate.move_to([3.95, 0.25, 0]), *[c.animate.move_to([3.4 + 0.3 * (i - 1), 1.5 + 0.1 * i, 0]) for i, c in enumerate(ca)], run_time=1.6)
        self.play(FadeOut(patp), run_time=0.3)
        # the mini thin filament: strand uncovered, then covered again
        mstrand.shift(DOWN * 0.34)
        msites.set_fill(BLUE, 0.95)
        self.play(FadeIn(mthin), FadeIn(msites), FadeIn(mstrand), run_time=0.5)
        self.at("calcium falls")
        self.play(Indicate(ca, color=YELLOW, scale_factor=1.0), run_time=0.4)
        self.at("covers the sites again")
        cov = T("tropomyosin covers the sites", 26, PURPLE).move_to([3.4, -2.95, 0])
        self.play(mstrand.animate.shift(UP * 0.34), msites.animate.set_fill(BLUE, 0.15), FadeIn(cov), run_time=1.1)
        self.at("muscle relaxes")
        self.play(Indicate(cov, color=PURPLE, scale_factor=1.05), run_time=0.5)
        self.at("without ATP")
        self.play(*[FadeOut(m) for m in (mthin, msites, mstrand, cov, sr, pump, sr_l, j2, ca, j1, l2)], run_time=0.8)
        stuck = head_mob([hx - 0.45, 1.33], [hx, -0.7])
        gp = VGroup(thick, thin, head, stuck)
        self.play(Transform(head, stuck), run_time=0.6)
        xatp = chip("no ATP", RED, 30).move_to([-1.6, 0.35, 0])
        self.play(FadeIn(xatp, shift=LEFT * 0.1), run_time=0.5)
        self.at("stuck to actin")
        st_l = T("the head stays stuck to actin", 28, RED).move_to([-3.3, -2.3, 0])
        self.play(FadeIn(st_l), Indicate(head, color=RED, scale_factor=1.1), run_time=0.7)
        self.at("stiffen after death")
        s2 = chip("muscles stiffen after death", RED, 30).move_to([3.4, 0.2, 0])
        self.play(FadeIn(s2, shift=LEFT * 0.1), run_time=0.7)
        self.at("keep this rule")
        rule = T("Filaments slide, and ATP lets the heads go.", 34, GOLD).move_to([0, -3.1, 0])
        self.play(FadeOut(st_l), FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Filaments slide, and ATP lets the heads go."
