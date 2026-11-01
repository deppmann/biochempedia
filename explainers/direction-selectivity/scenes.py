"""Direction is computed branch by branch  (Biochemistrypedia explainer, Sensory Systems)

COLOR MAP (one color per concept, whole film)
  YELLOW = the moving or flashed stimulus (spot, flashes); also the open question
  BLUE   = the direction selective ganglion cell and its spikes
  PURPLE = the starburst amacrine cell and its dendrites
  ORANGE = calcium signal in a starburst dendrite
  GREEN  = preferred direction (and outward, for a dendrite)
  RED    = null direction, suppression, inhibition
  TEAL   = transmitters released by starburst cells (acetylcholine, GABA)
  GREY   = receptive field, baselines, unknowns, de-emphasized
Left and right are the viewer's. Preferred is always drawn to the right, null to the left.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 2))


def bar(x, base, h, w=0.85, color=BLUE, op=0.75):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color,
                     fill_opacity=op).move_to([x, base + h / 2, 0])


def sac(center, R=2.5, w=3.5, n=8):
    """a starburst cell: soma and n radiating dendrites, each with two side branches."""
    c = np.array(center, float)
    soma = Circle(radius=0.3 * R / 2.5, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.9).move_to(c)
    prims = []
    for k in range(n):
        th = k * TAU / n
        d = np.array([np.cos(th), np.sin(th), 0])
        parts = [Line(c + d * 0.3 * R / 2.5, c + d * R)]
        for fr, sgn in ((0.42, 1), (0.7, -1)):
            p = c + d * fr * R
            a = th + sgn * 0.6
            parts.append(Line(p, p + 0.3 * R * np.array([np.cos(a), np.sin(a), 0])))
        g = VGroup(*parts).set_stroke(PURPLE, w, opacity=0.9)
        prims.append(g)
    return soma, prims


def mini_star(c, key_deg, key_len, other_len=0.9):
    c = np.array(c, float)
    soma = Circle(radius=0.26, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.9).move_to(c)
    others = VGroup()
    for k in range(1, 6):
        a = np.radians(key_deg + 60 * k)
        others.add(Line(c, c + other_len * np.array([np.cos(a), np.sin(a), 0]), color=PURPLE, stroke_width=3, stroke_opacity=0.55))
    a = np.radians(key_deg)
    tip = c + key_len * np.array([np.cos(a), np.sin(a), 0])
    key = arr(c, tip, PURPLE, w=6, tip=0.26)
    return VGroup(soma, others, key), key, tip


def mchip(text, color, size=24, pad=0.2):
    lab = T(text, size, color, line_spacing=0.9)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 2 * pad, height=lab.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, lab.move_to(box))


def sweep(spot, ticks, tas, x0, x1, run):
    def f(m, a):
        m.move_to([x0 + (x1 - x0) * a, spot.get_y(), 0])
        for t, ta in zip(ticks, tas):
            t.set_stroke(opacity=1.0 if a >= ta else 0.0)
    return UpdateFromAlphaFunc(spot, f, run_time=run, rate_func=linear)


class S00Title(TitleCard):
    LESSON = "Computing motion in the retina"
    TITLE = "Direction is computed branch by branch"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        head = T("One ganglion cell, rabbit retina", 28, GREY).to_edge(UP, buff=0.5)
        field = DashedVMobject(Ellipse(width=8, height=2.8, color=GREY, stroke_width=3), num_dashes=44).move_to([0, 1.1, 0])
        fl = T("receptive field", 22, GREY).move_to([0, 0.15, 0])
        spot = Circle(radius=0.28, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to([-3.2, 1.2, 0])
        self.at("ganglion cell")
        self.play(FadeIn(head), Create(field), FadeIn(fl), FadeIn(spot), run_time=1.0)

        def row(y, name):
            base = Line([-4.4, y, 0], [3.0, y, 0], color=GREY, stroke_width=2.5)
            lab = T(name, 22, GREY).move_to([-5.4, y + 0.25, 0])
            return base, lab

        b1, l1 = row(-1.2, "spikes")
        b2, l2 = row(-2.5, "spikes")
        t1 = np.linspace(0.1, 0.95, 14)
        ticks1 = VGroup(*[Line([-4.2 + a * 7.2, -1.2 + 0.08, 0], [-4.2 + a * 7.2, -1.2 + 0.75, 0], color=BLUE, stroke_width=4, stroke_opacity=0) for a in t1])
        t2 = [0.12]
        ticks2 = VGroup(*[Line([-4.2 + a * 7.2, -2.5 + 0.08, 0], [-4.2 + a * 7.2, -2.5 + 0.75, 0], color=BLUE, stroke_width=4, stroke_opacity=0) for a in t2])
        self.add(ticks1, ticks2)

        self.at("fires hard")
        self.play(Create(b1), FadeIn(l1), run_time=0.4)
        self.play(sweep(spot, ticks1, t1, -3.2, 3.2, 2.2))
        self.at("hardly fires")
        self.play(Create(b2), FadeIn(l2), run_time=0.4)
        self.play(sweep(spot, ticks2, t2, 3.2, -3.2, 2.2))

        pa = arr([3.5, -0.85, 0], [4.5, -0.85, 0], GREEN, w=6)
        pt = T("preferred", 24, GREEN).move_to([5.5, -0.85, 0])
        na = arr([4.5, -2.15, 0], [3.5, -2.15, 0], RED, w=6)
        nt = T("null", 24, RED).move_to([5.4, -2.15, 0])
        self.at("preferred direction")
        self.play(GrowArrow(pa), FadeIn(pt), run_time=0.6)
        self.at("null direction")
        self.play(GrowArrow(na), FadeIn(nt), run_time=0.6)

        self.at("Where in the retina")
        q = chip("?", YELLOW, size=64, pad=0.3).move_to([0, 1.1, 0])
        ask = T("where is the difference computed?", 28).move_to([0, 2.65, 0])
        self.play(FadeOut(VGroup(field, fl, spot)), FadeIn(q, scale=0.8), FadeIn(ask), run_time=0.8)
        self.at("which cells")
        wc = T("by which cells?", 28, YELLOW).next_to(q, RIGHT, buff=0.4)
        self.play(FadeIn(wc, shift=RIGHT * 0.2), Indicate(q, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Twoflash(SpokenScene):
    def construct(self):
        head = T("Rabbit, in vivo", 26, GREY).to_edge(UP, buff=0.5)
        field = DashedVMobject(Ellipse(width=5.2, height=2.8, color=GREY, stroke_width=3), num_dashes=36).move_to([-3.5, 1.6, 0])
        fl = T("one receptive field", 22, GREY).move_to([-3.5, 0.75, 0])
        A = Circle(radius=0.4, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.15).move_to([-4.6, 2.05, 0])
        B = Circle(radius=0.4, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.15).move_to([-2.4, 2.05, 0])
        An = T("A", 26, YELLOW).move_to([-4.6, 1.4, 0])
        Bn = T("B", 26, YELLOW).move_to([-2.4, 1.4, 0])
        self.at("recorded from")
        self.play(FadeIn(head), Create(field), FadeIn(fl), run_time=0.9)
        self.at("flashed two")
        self.play(FadeIn(A), FadeIn(B), FadeIn(An), FadeIn(Bn), run_time=0.7)

        base_y = -2.9
        xs = [1.75, 3.1, 4.45, 5.8]
        u = 1.8
        axis = Line([1.2, base_y, 0], [6.3, base_y, 0], color=GREY, stroke_width=2.5)
        labs = [T(s, 22, GREY).move_to([x, base_y - 0.38, 0]) for s, x in zip(["A alone", "B alone", "A + B", "pair"], xs)]
        ytitle = T("spikes, in this sketch", 22, GREY).move_to([3.75, 2.6, 0])

        def flash(s):
            return [s.animate.set_fill(YELLOW, 0.95)], [s.animate.set_fill(YELLOW, 0.15)]

        self.at("one after the other")
        self.play(FadeIn(axis), FadeIn(ytitle), *[FadeIn(l) for l in labs], run_time=0.5)
        on, off = flash(A)
        self.play(*on, run_time=0.25)
        barA = bar(xs[0], base_y, u)
        self.play(*off, GrowFromEdge(barA, DOWN), run_time=0.5)
        on, off = flash(B)
        self.play(*on, run_time=0.25)
        barB = bar(xs[1], base_y, u)
        self.play(*off, GrowFromEdge(barB, DOWN), run_time=0.5)

        order = T("preferred order: A then B", 24, GREEN).move_to([-3.5, -0.55, 0])
        self.at("preferred order")
        on, off = flash(A)
        self.play(FadeIn(order), *on, run_time=0.3)
        self.play(*off, run_time=0.2)
        on, off = flash(B)
        self.play(*on, run_time=0.25)
        self.play(*off, run_time=0.2)

        pair_p = bar(xs[3], base_y, 2.0 * u + 0.15, color=GREEN)
        self.at("pair gave")
        self.play(GrowFromEdge(pair_p, DOWN), run_time=0.7)
        sA = Rectangle(width=0.85, height=u, stroke_color=BLUE, stroke_width=2.5).move_to([xs[2], base_y + u / 2, 0])
        sB = Rectangle(width=0.85, height=u, stroke_color=BLUE, stroke_width=2.5).move_to([xs[2], base_y + 1.5 * u, 0])
        sumb = VGroup(DashedVMobject(sA, num_dashes=20), DashedVMobject(sB, num_dashes=20))
        sum_y = base_y + 2 * u
        sline = DashedLine([1.2, sum_y, 0], [6.3, sum_y, 0], color=GREY, stroke_width=2.5)
        note_p = T("about the sum", 24, GREEN).move_to([4.7, 1.55, 0])
        self.at("about the sum")
        self.play(FadeIn(sumb), Create(sline), FadeIn(note_p), run_time=0.8)
        self.at("single responses")
        self.play(Indicate(barA, color=BLUE, scale_factor=1.08), Indicate(barB, color=BLUE, scale_factor=1.08), run_time=0.8)

        # null order: clear the old answer in the same beat as the new label
        order_n = T("null order: B then A", 24, RED).move_to([-3.5, -0.55, 0])
        self.at("null order")
        on, off = flash(B)
        self.play(FadeOut(pair_p), FadeOut(note_p), ReplacementTransform(order, order_n), *on, run_time=0.4)
        self.play(*off, run_time=0.2)
        on, off = flash(A)
        self.play(*on, run_time=0.25)
        self.play(*off, run_time=0.2)
        pair_n = bar(xs[3], base_y, 1.0, color=RED)
        gap = DoubleArrow([5.8, sum_y - 0.05, 0], [5.8, base_y + 1.05, 0], buff=0, color=RED, stroke_width=4,
                          tip_length=0.16)
        note_n = T("far fewer than the sum", 24, RED).move_to([4.2, 1.55, 0])
        self.at("far fewer")
        self.play(GrowFromEdge(pair_n, DOWN), FadeIn(gap), FadeIn(note_n), run_time=0.8)

        sup = mchip("small subunits suppress\nnull-direction sequences", RED, 24).move_to([-3.5, -1.85, 0])
        self.at("small subunits")
        self.play(FadeIn(sup, shift=UP * 0.15), run_time=0.7)
        ten = mchip("which cells? left open", GREY, 24).move_to([-3.5, -3.2, 0])
        self.at("tentative")
        self.play(FadeIn(ten, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Dendrite(SpokenScene):
    def construct(self):
        C = [-3.4, -0.2, 0]
        soma, prims = sac(C)
        lab = T("starburst amacrine cell", 24, PURPLE).move_to([-3.4, 2.85, 0])
        self.at("Later work")
        self.play(FadeIn(soma, scale=0.5), FadeIn(lab), run_time=0.7)
        self.at("radiate")
        self.play(LaggedStart(*[Create(p) for p in prims], lag_ratio=0.15), run_time=1.6)

        head = T("isolated rabbit retina, ON starburst cell", 24, GREY).to_edge(UP, buff=0.5)
        ptitle = T("dendrite calcium\nin this sketch", 24, ORANGE, line_spacing=0.9).move_to([3.9, 2.5, 0])
        self.at("imaged calcium")
        self.play(FadeIn(ptitle), run_time=0.6)
        self.at("single dendrites")
        self.play(prims[0].animate.set_stroke(ORANGE, 6, opacity=1),
                  *[prims[k].animate.set_stroke(opacity=0.45) for k in range(1, 8)], run_time=0.8)
        self.at("isolated rabbit")
        self.play(FadeIn(head), run_time=0.6)

        base = -1.0
        ax = Line([2.6, base, 0], [5.6, base, 0], color=GREY, stroke_width=2.5)
        lo = T("outward", 22, GREEN).move_to([3.4, base - 0.35, 0])
        li = T("inward", 22, RED).move_to([4.9, base - 0.35, 0])
        dot = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to([-2.9, -0.2, 0])
        self.add(dot)
        dot.set_opacity(0)
        self.play(FadeIn(ax), run_time=0.3)
        self.at("motion outward")
        self.play(dot.animate.set_opacity(1), run_time=0.2)
        self.play(dot.animate.move_to([-1.0, -0.2, 0]), run_time=1.0, rate_func=linear)
        b_out = bar(3.4, base, 2.9, 1.1, ORANGE)
        self.play(GrowFromEdge(b_out, DOWN), FadeIn(lo), run_time=0.5)
        self.at("than inward")
        self.play(dot.animate.move_to([-2.9, -0.2, 0]), run_time=1.0, rate_func=linear)
        b_in = bar(4.9, base, 1.1, 1.1, ORANGE)
        self.play(GrowFromEdge(b_in, DOWN), FadeIn(li), run_time=0.5)
        self.play(FadeOut(dot), run_time=0.2)

        sv = mchip("soma voltage:\nnot the same preference", GREY, 22).move_to([4.1, -2.75, 0])
        self.at("The voltage")
        self.play(Indicate(soma, color=PURPLE, scale_factor=1.4), FadeIn(sv, shift=UP * 0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Wiring(SpokenScene):
    def construct(self):
        C = [-3.4, -0.2, 0]
        soma, prims = sac(C)
        for k in range(1, 8):
            prims[k].set_stroke(opacity=0.9)
        cell = VGroup(soma, *prims)
        self.add(cell)
        outs = VGroup()
        for deg in (0, 90, 180, 270):
            d = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
            outs.add(arr(np.array(C) + d * 0.55, np.array(C) + d * 1.3, GREEN, w=6, tip=0.2))
        side = mchip("each branch has its own\npreferred direction", GREEN, 24).move_to([3.0, 0.3, 0])
        self.at("its own preferred direction")
        self.play(LaggedStart(*[GrowArrow(o) for o in outs], lag_ratio=0.2), FadeIn(side), run_time=1.2)
        self.at("set by where")
        self.play(LaggedStart(*[Indicate(o, color=GREEN, scale_factor=1.25) for o in outs], lag_ratio=0.25), run_time=1.6)

        # ---- to the wiring diagram -----------------------------------------------------------
        head = T("mouse retina", 24, GREY).move_to([-5.3, 3.3, 0])
        D = np.array([0.0, 0.1, 0.0])
        fieldc = Circle(radius=1.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.1).move_to(D)
        gsoma = Circle(radius=0.45, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to(D)
        glab = T("ganglion cell", 24, BLUE).move_to([0, -2.3, 0])
        self.at("tested the wiring")
        self.play(FadeOut(VGroup(cell, outs, side)), run_time=0.5)
        self.play(FadeIn(head), FadeIn(fieldc), FadeIn(gsoma), FadeIn(glab), run_time=0.6)

        pa = arr([0.4, 2.9, 0], [2.4, 2.9, 0], GREEN, w=6)
        pt = T("preferred direction", 24, GREEN).move_to([4.3, 2.9, 0])
        na = arr([-0.4, 2.9, 0], [-2.4, 2.9, 0], RED, w=6)
        nt = T("null direction", 24, RED).move_to([-4.2, 2.9, 0])
        self.at("imaged each")
        self.play(GrowArrow(pa), FadeIn(pt), GrowArrow(na), FadeIn(nt), run_time=0.9)

        s1, k1, tip1 = mini_star([4.1, 1.6, 0], 200, 2.7, 1.2)
        s2, k2, tip2 = mini_star([4.1, -1.2, 0], 160, 2.7, 1.2)
        self.at("reconstructed")
        self.play(LaggedStart(FadeIn(s1), FadeIn(s2), lag_ratio=0.5), run_time=1.5)
        sk = T("schematic: branch direction,\nnot soma position", 22, GREY, line_spacing=0.9).move_to([-4.0, -1.4, 0])
        self.add(sk)
        sk.set_opacity(0)
        d1 = Dot(tip1, radius=0.13, color=TEXT)
        d2 = Dot(tip2, radius=0.13, color=TEXT)
        self.at("Most starburst input")
        self.play(FadeIn(d1, scale=2), FadeIn(d2, scale=2), sk.animate.set_opacity(1), run_time=0.7)
        self.play(Indicate(k1, color=PURPLE, scale_factor=1.1), Indicate(k2, color=PURPLE, scale_factor=1.1), run_time=0.8)

        c1 = mchip("branch direction", PURPLE, 24).move_to([-3.2, -3.1, 0])
        mid = T("predicted better than", 24, TEXT).move_to([0.3, -3.1, 0])
        c2 = mchip("line between bodies", GREY, 24).move_to([4.2, -3.1, 0])
        self.at("Branch direction predicted")
        self.play(FadeOut(sk), FadeIn(c1), FadeIn(mid), run_time=0.6)
        line = DashedLine(np.array([4.1, 1.6, 0]), D, color=GREY, stroke_width=3)
        self.at("line between")
        self.play(FadeIn(c2), Create(line), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Develop(SpokenScene):
    def construct(self):
        head = T("developing mouse retina, paired recordings", 24, GREY).move_to([0, 3.4, 0])
        dsgc = mchip("ganglion cell\nnasal-preferring ON-OFF", BLUE, 24).move_to([3.5, 0, 0])
        sn = mchip("starburst input,\nnull-direction branches\n(stronger later)", PURPLE, 22).move_to([-4.0, 1.5, 0])
        sp = mchip("starburst input,\npreferred-direction branches\n(about the same)", PURPLE, 22).move_to([-4.0, -1.5, 0])
        cap = T("line thickness: inhibition strength, in this sketch", 22, GREY).move_to([0, -3.2, 0])

        def conn(src, dst, w, color=RED):
            return inhib(src, dst, color, w)

        def pair(wn, wp, dashed_p=False):
            n = conn([-1.5, 1.5, 0], [1.2, 0.3, 0], wn)
            p = conn([-1.5, -1.5, 0], [1.2, -0.3, 0], wp)
            return n, p

        n0, p0 = pair(14, 5)
        self.play(FadeIn(head), FadeIn(dsgc), FadeIn(sn), FadeIn(sp), FadeIn(n0), FadeIn(p0), FadeIn(cap), run_time=1.0)
        self.at("asymmetry")
        self.play(Indicate(n0, color=RED, scale_factor=1.05), run_time=0.8)

        ghost = DashedVMobject(Line([-1.5, -1.5, 0], [1.2, -0.3, 0], color=GREY, stroke_width=4), num_dashes=14)
        prune = T("pruning: delete these branches", 22, GREY).move_to([0, -2.65, 0])
        self.at("Pruning would delete")
        self.play(FadeOut(p0), FadeIn(ghost), FadeIn(prune), run_time=0.8)

        stage1 = T("postnatal days 4 and 7", 30, TEXT, weight=BOLD).move_to([0, 2.85, 0])
        n1, p1 = pair(8, 8)
        self.at("recorded pairs")
        self.play(FadeOut(ghost), FadeOut(prune), FadeOut(n0), run_time=0.6)
        self.at("At postnatal days")
        self.play(FadeIn(stage1), FadeIn(n1), FadeIn(p1), run_time=0.8)

        stage2 = T("later", 30, TEXT, weight=BOLD).move_to([0, 2.85, 0])
        n2, p2 = pair(14, 8)
        self.at("Later")
        self.play(ReplacementTransform(stage1, stage2), ReplacementTransform(n1, n2), run_time=1.0)
        self.at("stayed about the same")
        self.play(Indicate(p1, color=RED, scale_factor=1.08), run_time=0.8)
        still = T("still present in adults", 24, GREEN).move_to([0, -2.3, 0])
        self.at("still there")
        self.play(FadeIn(still, shift=UP * 0.15), Indicate(p1, color=GREEN, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        head = T("adult mouse", 24, GREY).to_edge(UP, buff=0.5)
        pop = mchip("starburst cells\nwhole population", PURPLE, 24).move_to([-3.4, 2.3, 0])
        self.at("Removing the whole")
        self.play(FadeIn(head), FadeIn(pop), run_time=0.7)
        cross = Line(pop.get_corner(UR) + np.array([-0.25, 0.25, 0]), pop.get_corner(UR) + np.array([0.25, -0.25, 0]), color=RED, stroke_width=6)
        ab = T("selectivity abolished", 22, RED).move_to([-1.3, -2.15, 0])
        base = -1.2
        gI = bar(-5.25, base, 2.2, 0.7, GREEN)
        rI = bar(-4.35, base, 0.5, 0.7, RED)
        gR = bar(-1.75, base, 1.2, 0.7, GREEN)
        rR = bar(-0.85, base, 1.2, 0.7, RED)
        ax1 = Line([-5.9, base, 0], [-3.7, base, 0], color=GREY, stroke_width=2.5)
        ax2 = Line([-2.4, base, 0], [-0.2, base, 0], color=GREY, stroke_width=2.5)
        t1 = T("intact", 22, GREY).move_to([-4.8, base - 0.35, 0])
        t2 = T("cells removed", 22, GREY).move_to([-1.3, base - 0.35, 0])
        lg = VGroup(T("preferred", 22, GREEN), T("null", 22, RED), T("in this sketch", 22, GREY)).arrange(RIGHT, buff=0.45).move_to([-3.0, -2.95, 0])
        self.add(gI, rI, ax1, ax2, t1, t2, lg)
        for m in (gI, rI, ax1, ax2, t1, t2, lg):
            m.set_opacity(0)
        self.play(*[m.animate.set_opacity(1) for m in (gI, rI, ax1, t1, lg)], run_time=0.4)
        self.at("-abolish")
        self.play(Create(cross), FadeIn(ab), *[m.animate.set_opacity(1) for m in (ax2, t2)], run_time=0.5)
        gR.set_opacity(0); rR.set_opacity(0)
        self.add(gR, rR)
        self.play(gR.animate.set_opacity(0.75), rR.animate.set_opacity(0.75), run_time=0.6)

        self.at("needed in that assay")
        self.play(Indicate(pop, color=PURPLE, scale_factor=1.08), run_time=0.8)

        ach = mchip("acetylcholine", TEAL, 24).move_to([4.0, 1.7, 0])
        gab = mchip("GABA", TEAL, 24).move_to([4.0, 0.5, 0])
        self.at("acetylcholine")
        self.play(FadeIn(ach, shift=LEFT * 0.2), run_time=0.5)
        self.at("GABA")
        self.play(FadeIn(gab, shift=LEFT * 0.2), run_time=0.5)
        q = mchip("this assay\ncan't say which", YELLOW, 24).move_to([4.0, -1.1, 0])
        self.at("carries the asymmetry")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)

        self.at("keep this rule")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        soma, prims = sac([-3.5, 0.6, 0], R=2.2, w=4, n=6)
        outs = VGroup(*[arr(np.array([-3.5, 0.6, 0]) + 0.6 * np.array([np.cos(i * TAU / 6), np.sin(i * TAU / 6), 0]),
                            np.array([-3.5, 0.6, 0]) + 1.5 * np.array([np.cos(i * TAU / 6), np.sin(i * TAU / 6), 0]),
                            GREEN, w=6, tip=0.2) for i in range(6)])
        l1 = T("branch by branch", 32).move_to([-3.5, -2.2, 0])
        self.at("branch by branch")
        self.play(FadeIn(soma), *[Create(p) for p in prims], run_time=0.8)
        self.play(*[GrowArrow(o) for o in outs], FadeIn(l1), run_time=0.7)

        g = Circle(radius=0.55, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to([4.9, 0.6, 0])
        ln = inhib([1.9, 1.5, 0], [4.25, 0.85, 0], RED, 14)
        lp = inhib([1.9, -0.3, 0], [4.25, 0.35, 0], RED, 5)
        tn = T("null-direction branches", 24, RED).move_to([1.3, 2.0, 0])
        tp = T("preferred-direction branches", 24, GREY).move_to([1.3, -0.9, 0])
        l2 = T("inhibition from null-direction\nbranches strengthens", 32, line_spacing=0.9).move_to([3.4, -2.2, 0])
        self.at("inhibition strengthens")
        self.play(FadeIn(g), GrowFromEdge(ln, LEFT), GrowFromEdge(lp, LEFT), FadeIn(tn), FadeIn(tp), FadeIn(l2), run_time=1.4)
        self.finish()


class S07End(EndCard):
    LINE = "Direction is computed branch by branch; inhibition strengthens on the null side."
