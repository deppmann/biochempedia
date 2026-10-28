"""A cut axon runs a program  (Biochemistrypedia explainer, Developmental Neuroscience)

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron: cell body, axon, stump
  TEAL   = NMNAT2 (the short-lived supply) and the Wlds protein that stands in for it
  ORANGE = NMN
  GREEN  = NAD+ and ATP (the axon's energy)
  RED    = SARM1 and the cut/destruction
  YELLOW = calcium
  PURPLE = calpain
  GOLD   = the program bracket
  GREY   = labels, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def dim(c, o=0.3):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def undim(c):
    return [c[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[2].animate.set_opacity(1)]


def tube(x0, x1, y, h=0.4, color=BLUE, op=0.3):
    return RoundedRectangle(corner_radius=h / 2, width=x1 - x0, height=h, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def beads(x0, x1, y, h=0.4, n=7, color=BLUE, op=0.3):
    pitch = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w, height=h * 0.9, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x0 + pitch * (i + 0.5), y + (0.05 if i % 2 else -0.05), 0]))
    return g


def neuron(y, xs=-5.4, xe=6.0, xc=-0.8, h=0.4, r=0.65):
    prox = tube(xs, xc, y, h)
    dist = tube(xc, xe, y, h)
    soma = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([xs, y, 0])
    soma_f = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([xs, y, 0])
    nuc = Circle(radius=r * 0.36, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([xs, y, 0])
    n = VGroup(prox, dist, soma, soma_f, nuc)
    n.prox, n.dist, n.soma, n.nuc, n.y, n.xc, n.xe = prox, dist, VGroup(soma, soma_f), nuc, y, xc, xe
    return n


def cutmark(x, y, h=0.9):
    return VGroup(*[Line([x + dx - 0.12, y - h / 2, 0], [x + dx + 0.12, y + h / 2, 0], color=TEXT, stroke_width=5)
                    for dx in (-0.2, 0.2)])


def do_cut(n, gap=0.18):
    """animations that open a gap in the axon."""
    return [n.prox.animate.shift(LEFT * gap), n.dist.animate.shift(RIGHT * gap)]


def padlock(color=RED, opened=False, scale=1.0):
    body = RoundedRectangle(corner_radius=0.18, width=1.5, height=1.1, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.3)
    sh = Arc(radius=0.46, start_angle=0, angle=PI, stroke_color=color, stroke_width=7).move_to(body.get_top() + UP * 0.38)
    if opened:
        sh.rotate(-0.55, about_point=sh.get_corner(DR)).shift(UP * 0.05)
    g = VGroup(sh, body)
    g.body, g.sh = body, sh
    g.scale(scale)
    return g


def gauge(w, h, color):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3)


class S00Title(TitleCard):
    LESSON = "Injury and regeneration"
    TITLE = "A cut axon runs a program"


# ---------------------------------------------------------------------------------------------
class S01Cut(SpokenScene):
    def construct(self):
        A, B = 0.4, -1.7
        na = neuron(A)
        la = T("normal mouse", 26, GREY).move_to([-4.2, A + 1.15, 0])
        self.play(FadeIn(na), FadeIn(la), run_time=0.7)
        cm = cutmark(-0.8, A)
        stump = T("part beyond the cut", 26, TEXT).move_to([2.6, A - 0.85, 0])
        self.at("The part of each axon")
        self.play(*do_cut(na), Create(cm), run_time=0.6)
        self.play(FadeIn(stump), run_time=0.4)
        self.at("looks normal")
        day = T("about 36 hours: looks normal", 26, GREY).move_to([2.6, A + 0.85, 0])
        self.play(FadeIn(day, shift=DOWN * 0.1), run_time=0.5)
        self.at("falls to pieces")
        bd = beads(-0.62, 6.18, A, 0.4, 8)
        day2 = T("falls to pieces", 26, RED).move_to([2.6, A + 0.85, 0])
        self.play(ReplacementTransform(na.dist, bd), ReplacementTransform(day, day2), FadeOut(stump), run_time=1.0)

        nb = neuron(B)
        lb = T("one strain of mouse", 26, GREY).move_to([-3.9, B + 1.15, 0])
        cmb = cutmark(-0.8, B)
        self.at("In one strain")
        self.play(VGroup(na.prox, na.soma, na.nuc, la, cm, bd, day2).animate.shift(UP * 1.1), FadeIn(nb), FadeIn(lb), run_time=0.8)
        self.play(*do_cut(nb), Create(cmb), run_time=0.5)
        self.at("the same cut axons")
        sb = T("same cut, stump still whole", 26, TEXT).move_to([2.6, B - 0.85, 0])
        self.play(FadeIn(sb), run_time=0.5)
        self.at("two weeks or more")
        wk = T("two weeks or more", 26, BLUE).move_to([2.6, B + 0.85, 0])
        self.play(FadeIn(wk, shift=DOWN * 0.1), run_time=0.5)
        self.at("What is different")
        q = T("?", 90, YELLOW, weight=BOLD).move_to([5.3, B + 1.0, 0])
        self.play(FadeIn(q, scale=0.6), Indicate(nb.dist, color=YELLOW, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Program(SpokenScene):
    def construct(self):
        A, B = 0.2, -1.5
        na = neuron(A, xc=-0.8)
        self.at("The axon is")
        self.play(FadeIn(na), run_time=0.7)
        br = Brace(Line([-4.6, A, 0], [6.0, A, 0]), UP, color=BLUE, buff=0.55)
        axl = T("axon: carries the neuron's output", 26, BLUE).next_to(br, UP, buff=0.12)
        self.at("long process")
        self.play(GrowFromCenter(br), FadeIn(axl), run_time=0.8)
        cb = T("cell body", 26, GREY).move_to([-5.4, A - 1.15, 0])
        nl = T("nucleus", 24, GREY).move_to([-3.6, A - 1.15, 0])
        nl_ar = arr([-4.0, A - 0.95, 0], [-5.25, A - 0.1, 0], GREY, w=3, tip=0.15)
        self.at("The cell body")
        self.play(FadeIn(cb), run_time=0.4)
        self.at("holds the nucleus")
        self.play(FadeIn(nl), GrowArrow(nl_ar), Indicate(na.nuc, color=YELLOW, scale_factor=1.3), run_time=0.8)

        cm = cutmark(-0.8, A)
        st = bchip("stump starves?", GREY, 26).move_to([2.8, A - 1.1, 0])
        self.at("simply starves")
        self.play(FadeOut(VGroup(br, axl, nl, nl_ar, cb)), *do_cut(na), Create(cm), FadeIn(st), run_time=0.8)
        bd = beads(-0.62, 6.18, A, 0.4, 8)
        self.play(ReplacementTransform(na.dist, bd), run_time=0.8)

        nb = neuron(B, xc=-0.8)
        gene = bchip("no Sarm1 gene", RED, 26).move_to([-4.3, B - 1.2, 0])
        self.at("But mice that lack")
        self.play(VGroup(na.prox, na.soma, na.nuc, cm, st, bd).animate.shift(UP * 1.5), FadeIn(nb), FadeIn(gene, shift=UP * 0.1), run_time=0.8)
        cmb = cutmark(-0.8, B)
        self.at("keep cut axons intact")
        self.play(*do_cut(nb), Create(cmb), run_time=0.6)
        ok = T("cut stump stays intact", 26, BLUE).move_to([2.8, B - 0.95, 0])
        self.play(FadeIn(ok), run_time=0.5)
        self.at("stop the breakdown")
        self.play(Indicate(nb.dist, color=BLUE, scale_factor=1.04), FadeOut(st), run_time=0.8)
        prog = bchip("something is running it", GOLD, 28).move_to([2.8, 0.45, 0])
        self.at("something is running it")
        box = SurroundingRectangle(bd, color=GOLD, buff=0.28, stroke_width=3.5, corner_radius=0.2)
        self.play(Create(box), FadeIn(prog), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Supply(SpokenScene):
    def construct(self):
        y = 0.9
        xs, xe, xc = -5.4, 6.0, 0.4
        n = neuron(y, xs=xs, xe=xe, xc=xc, h=0.9, r=0.95)
        n.nuc.set_opacity(0.0)
        self.add(n)
        self.add(n.soma)
        head = bchip("NMNAT2", TEAL, 34).move_to([-3.6, 2.9, 0])
        note = T("short-lived", 28, GREY).next_to(head, RIGHT, buff=0.3)
        self.at("An enzyme called")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.5)
        self.at("short")
        self.play(FadeIn(note), run_time=0.4)

        # gauge for NMNAT2 in the stump
        gw = 6.0
        g_out = gauge(gw, 0.5, TEAL).move_to([2.2, -2.3, 0])
        gl = T("NMNAT2 in the stump", 26, TEAL).next_to(g_out, LEFT, buff=0.3)
        tr = ValueTracker(0.08)
        fill = always_redraw(lambda: Rectangle(width=max(tr.get_value(), 0.01) * gw, height=0.5, stroke_width=0,
                                               fill_color=TEAL, fill_opacity=0.55).align_to(g_out, LEFT).align_to(g_out, DOWN))
        self.add(fill)
        self.add(g_out, gl)
        # packets stream from the cell body down the axon into the stump
        stump_xs = [1.4, 2.4, 3.4, 4.4, 5.3]
        pk = [Circle(radius=0.2, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.9).move_to([xs + 1.2, y, 0])
              for _ in stump_xs]
        trk = T("sent from the cell body", 26, GREY).move_to([-2.8, y - 1.2, 0])
        self.at("must keep sending it")
        for p in pk:
            self.add(p)
        order = list(reversed(range(len(pk))))
        anims = [Succession(Wait(0.4 * k), pk[i].animate(run_time=(stump_xs[i] - xs - 1.2) / 4.0, rate_func=linear).move_to([stump_xs[i], y, 0]))
                 for k, i in enumerate(order)]
        self.play(FadeIn(trk, run_time=0.6), *anims, tr.animate(run_time=3.0, rate_func=linear).set_value(0.95), run_time=3.0)

        cm = cutmark(xc, y, 1.5)
        self.at("A cut closes the road")
        self.play(*do_cut(n, 0.2), Create(cm), run_time=0.4)
        late = [Circle(radius=0.2, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.9).move_to([xs + 1.2, y, 0])
                for _ in range(2)]
        for p in late:
            self.add(p)
        la = [Succession(Wait(0.4 * i), p.animate(run_time=1.1, rate_func=linear).move_to([xc - 0.55 - 0.45 * i, y, 0]))
              for i, p in enumerate(late)]
        stop = inhib([xc - 0.2, y + 0.9, 0], [xc - 0.2, y - 0.9, 0])
        self.play(*la, FadeIn(stop), run_time=1.5)
        self.at("The supply stops")
        self.play(Indicate(VGroup(*late), color=RED, scale_factor=1.15), run_time=0.6)
        self.at("runs low")
        self.play(*[FadeOut(p) for p in pk], tr.animate.set_value(0.06), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Sensor(SpokenScene):
    def construct(self):
        base = -2.6
        t0 = tube(-6.2, 6.2, 3.0, 0.5, BLUE, 0.2)
        stl = T("inside the stump", 26, BLUE).move_to([-4.4, 2.35, 0])
        gone = bchip("NMNAT2 gone", TEAL, 26).move_to([4.0, 2.35, 0])
        xcross = VGroup(Line(gone.get_corner(UL), gone.get_corner(DR), color=RED, stroke_width=6),
                        Line(gone.get_corner(DL), gone.get_corner(UR), color=RED, stroke_width=6))
        self.add(t0)
        self.at("With")
        self.play(FadeIn(stl), FadeIn(gone), run_time=0.5)
        self.play(Create(xcross), gone[1].animate.set_stroke(opacity=0.4), gone[2].animate.set_opacity(0.4), run_time=0.5)

        xn, xa = -4.6, -2.2
        line = Line([-5.6, base, 0], [-1.2, base, 0], color=GREY, stroke_width=3)
        h = ValueTracker(0.0)
        a = ValueTracker(3.0)
        nmn = always_redraw(lambda: Rectangle(width=1.1, height=max(h.get_value(), 0.01), stroke_color=ORANGE, stroke_width=3,
                                              fill_color=ORANGE, fill_opacity=0.45).move_to([xn, base + max(h.get_value(), 0.01) / 2, 0]))
        nad = always_redraw(lambda: Rectangle(width=1.1, height=max(a.get_value(), 0.01), stroke_color=GREEN, stroke_width=3,
                                              fill_color=GREEN, fill_opacity=0.45).move_to([xa, base + max(a.get_value(), 0.01) / 2, 0]))
        ln = T("NMN", 28, ORANGE).move_to([xn, base - 0.4, 0])
        la = T("NAD+", 28, GREEN).move_to([xa, base - 0.4, 0])
        self.at("its raw material")
        self.add(line, nmn, nad)
        self.play(FadeIn(ln), FadeIn(la), h.animate.set_value(0.7), run_time=0.8)
        self.at("builds up")
        self.play(h.animate.set_value(3.6), run_time=1.3)
        self.at("begins to fall")
        self.play(a.animate.set_value(1.1), run_time=1.3)
        self.at("enzymes make")
        self.play(Indicate(la, color=GREEN, scale_factor=1.15), run_time=0.6)

        lock = padlock(RED, opened=False).scale(1.35).move_to([3.4, 0.2, 0])
        lock.body.set_fill(RED, 0.18).set_stroke(opacity=0.55)
        lock.sh.set_stroke(opacity=0.55)
        ll = T("SARM1", 34, RED, weight=BOLD).move_to([3.4, -1.3, 0])
        self.at("A protein called")
        self.play(FadeIn(lock, shift=DOWN * 0.15), FadeIn(ll), run_time=0.7)
        sh = T("held shut", 26, GREY).move_to([3.4, -1.9, 0])
        self.at("held shut")
        self.play(FadeIn(sh), run_time=0.4)
        self.at("switches it on")
        op = padlock(RED, opened=True).scale(1.35)
        op.shift(lock.body.get_center() - op.body.get_center())
        link = arr([-1.0, -0.6, 0], [2.0, -0.4, 0], ORANGE)
        self.play(Transform(lock, op), FadeIn(link), FadeOut(sh), run_time=0.9)
        self.play(Indicate(lock, color=RED, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Collapse(SpokenScene):
    def construct(self):
        ty = -1.5
        tb = tube(-6.2, 6.2, ty, 1.3, BLUE, 0.2)
        scaf = VGroup(*[Line([-6.0, ty + dy, 0], [6.0, ty + dy, 0], color=GREY, stroke_width=3) for dy in (-0.3, 0.0, 0.3)])
        stl = T("stump: no nucleus", 24, GREY).move_to([-4.6, ty - 1.1, 0])
        self.add(tb, scaf)

        lock = padlock(RED, opened=True).scale(1.0).move_to([-5.0, 2.0, 0])
        ll = T("SARM1", 30, RED, weight=BOLD).move_to([-5.0, 0.55, 0])
        self.at("is an enzyme")
        self.play(FadeIn(lock, shift=DOWN * 0.1), FadeIn(ll), run_time=0.6)

        nads = VGroup(*[bchip("NAD+", GREEN, 26).move_to([x, 2.0, 0]) for x in (-2.7, -1.2, 0.3)])
        self.at("it cleaves")
        self.play(FadeIn(nads, shift=RIGHT * 0.2), run_time=0.5)
        slash = VGroup(*[Line(c.get_corner(DL) + [0.05, -0.05, 0], c.get_corner(UR) + [-0.05, 0.05, 0], color=RED, stroke_width=6) for c in nads])
        self.play(LaggedStart(*[Create(s) for s in slash], lag_ratio=0.25), run_time=0.8)
        self.play(*[c.animate.set_opacity(0.45) for c in nads], FadeOut(slash), run_time=0.5)

        atp_l = T("ATP", 28, GREEN).move_to([2.7, 2.0, 0])
        atp_o = gauge(2.6, 0.5, GREEN).move_to([4.7, 2.0, 0])
        tr = ValueTracker(1.0)
        atp_f = always_redraw(lambda: Rectangle(width=max(tr.get_value(), 0.01) * 2.6, height=0.5, stroke_width=0, fill_color=GREEN,
                                                fill_opacity=0.5).align_to(atp_o, LEFT).align_to(atp_o, DOWN))
        self.add(atp_f)
        self.add(atp_o, atp_l)
        self.at("Then")
        self.play(tr.animate(run_time=1.4).set_value(0.05), run_time=1.4)

        # calcium
        rng = np.random.RandomState(4)
        ca = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to(
            [rng.uniform(-5.6, 5.6), ty + rng.uniform(-0.42, 0.42), 0]) for _ in range(26)])
        cal = T("calcium", 28, YELLOW).move_to([3.2, 0.0, 0])
        self.at("calcium rises")
        self.play(FadeIn(cal), LaggedStart(*[FadeIn(c, scale=0.3) for c in ca], lag_ratio=0.05), run_time=1.6)

        cps = VGroup(*[bchip("calpain", PURPLE, 24).move_to([x, 0.35, 0]) for x in (-2.4, 0.4, 3.2)])
        self.at("Calcium switches on")
        self.play(FadeOut(cal), FadeIn(cps, shift=DOWN * 0.1), run_time=0.7)
        self.at("enzymes that cut")
        self.play(*[c.animate.move_to([c.get_center()[0], ty + 0.95, 0]) for c in cps], run_time=0.7)
        sc = T("cytoskeleton", 24, GREY).move_to([4.6, ty - 1.05, 0])
        self.at("cut the cytoskeleton")
        cuts = VGroup(*[Line([x, ty + 0.65, 0], [x, ty - 0.65, 0], color=PURPLE, stroke_width=6) for x in (-2.4, 0.4, 3.2)])
        self.play(FadeIn(sc), LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.3), run_time=0.9)
        bd = beads(-6.0, 6.0, ty, 1.0, 9)
        self.at("the axon fragments")
        self.play(FadeOut(scaf), FadeOut(cuts), FadeOut(cps), FadeOut(sc), FadeOut(ca), ReplacementTransform(tb, bd), run_time=1.2)
        self.at("with no nucleus")
        self.play(FadeIn(stl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        cy = 1.9
        xs = [-4.8, -1.6, 1.6, 4.8]
        specs = [("NMNAT2\nsupply", TEAL), ("NMN up\nNAD+ down", ORANGE), ("SARM1\non", RED), ("axon\nfragments", BLUE)]
        chips = [bchip(t, c, 26).move_to([x, cy, 0]) for (t, c), x in zip(specs, xs)]
        # make chips equal width
        arrs = [arr(chips[i].get_right(), chips[i + 1].get_left(), GREY) for i in range(3)]
        res_y = -2.4
        frag = beads(-2.4, 2.4, res_y, 0.45, 7)
        whole = tube(-2.4, 2.4, res_y, 0.45)
        rl = T("the cut stump", 26, GREY).move_to([-4.6, res_y, 0])
        self.at("Now the slow mouse")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chips], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), run_time=1.6)
        self.play(FadeIn(rl), FadeIn(frag), run_time=0.5)

        wl = bchip("Wlds protein", TEAL, 26).move_to([-4.8, -0.1, 0])
        wa = arr(wl.get_top(), chips[0].get_bottom(), TEAL)
        wnote = T("a longer-lived source of NMNAT activity", 24, GREY).move_to([-2.5, -0.95, 0])
        self.at("Its")
        self.play(FadeIn(wl, shift=UP * 0.15), GrowArrow(wa), FadeOut(frag),
                  *[a for c in chips[1:] for a in dim(c)], *[a.animate.set_opacity(0.3) for a in arrs], run_time=0.7)
        self.play(FadeIn(wnote), run_time=0.3)
        self.at("keeps the tank full")
        # NMNAT supply stays up: downstream steps stay quiet, stump stays whole
        self.play(FadeIn(whole), run_time=0.8)
        okl = T("stump intact", 26, BLUE).move_to([4.2, res_y, 0])
        self.play(FadeIn(okl), run_time=0.3)

        # new case: clear the old answer first
        sdel = bchip("Sarm1 deleted", RED, 26).move_to([1.6, -0.1, 0])
        sbar = inhib([1.6, 0.4, 0], [1.6, cy - 0.65, 0])
        self.at("deletes")
        self.play(FadeOut(VGroup(wl, wa, wnote, whole, okl)),
                  *undim(chips[1]), arrs[0].animate.set_opacity(1.0),
                  FadeIn(sdel, shift=UP * 0.15), run_time=0.7)
        self.at("instead")
        xs_ = VGroup(Line(chips[2].get_corner(UL), chips[2].get_corner(DR), color=RED, stroke_width=6),
                     Line(chips[2].get_corner(DL), chips[2].get_corner(UR), color=RED, stroke_width=6))
        self.play(Create(xs_), run_time=0.5)
        self.at("survive two")
        whole2 = tube(-2.4, 2.4, res_y, 0.45)
        okl2 = T("stump intact", 26, BLUE).move_to([4.2, res_y, 0])
        self.play(FadeIn(whole2), FadeIn(okl2), run_time=0.8)

        self.at("The stump")
        box = Brace(VGroup(*chips), UP, color=GOLD, buff=0.2)
        pl = T("a program", 30, GOLD, weight=BOLD).next_to(box, UP, buff=0.12)
        self.play(Create(box), FadeIn(pl), run_time=0.8)
        self.at("parts that can be stopped")
        self.play(Indicate(chips[0], color=TEAL), Indicate(chips[2], color=RED), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Losing its supply sets off a program in the stump."
