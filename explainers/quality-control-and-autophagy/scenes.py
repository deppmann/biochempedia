"""Quality control and autophagy: count the flux, not the dots  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = autophagosome / making them (the tap)
  PURPLE = LC3-II (dots on membranes, bars on the blot plot)
  ORANGE = lysosome / destroying (the drain)
  RED    = block: bafilomycin, the plugged drain, the misleading reading
  YELLOW = flux (the difference between the two measurements)
  GREY   = cell outline, axes, cytoplasm, structure
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def pt(x, y):
    return np.array([x, y, 0.0])


def autop(center, r=0.3, color=BLUE):
    c = pt(*center[:2])
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.12).move_to(c),
                  Circle(radius=r * 0.6, stroke_color=color, stroke_width=3).move_to(c))


def ring_dots(center, r, n, color=PURPLE, dr=0.07, start=0.0, span=2 * PI):
    c = np.array(center, float)
    out = VGroup()
    for i in range(n):
        a = start + span * i / n
        out.add(Dot(c + r * np.array([math.cos(a), math.sin(a), 0]), radius=dr, color=color))
    return out


def lbl(text, color=GREY, size=24):
    return T(text, size, color)


# ---- the sink ---------------------------------------------------------------------------------
class Sink:
    """basin, tap pipe and drain pipe centred at (cx, cy). Water height is set with water(h)."""

    def __init__(self, cx, cy, hw=1.9, wall=1.3):
        self.cx, self.cy, self.hw, self.wall = cx, cy, hw, wall
        self.basin = VMobject(color=GREY, stroke_width=6).set_points_as_corners(
            [pt(cx - hw, cy + wall), pt(cx - hw, cy - wall), pt(cx + hw, cy - wall), pt(cx + hw, cy + wall)])
        self.tx = cx - 1.0
        self.dx = cx + 1.15
        self.tap = VGroup(Line(pt(self.tx, cy + 2.55), pt(self.tx, cy + 1.75), color=BLUE, stroke_width=9),
                          Line(pt(self.tx - 0.35, cy + 2.55), pt(self.tx + 0.35, cy + 2.55), color=BLUE, stroke_width=9))
        self.stream = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
                               .move_to(pt(self.tx, cy + 1.5 - 0.35 * k)) for k in range(3)])
        self.drain = VGroup(Line(pt(self.dx, cy - wall), pt(self.dx, cy - wall - 0.75), color=ORANGE, stroke_width=9),
                            Rectangle(width=0.5, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
                            .move_to(pt(self.dx, cy - wall)))
        self.plug = Rectangle(width=0.62, height=0.2, stroke_width=0, fill_color=RED, fill_opacity=1) \
            .move_to(pt(self.dx, cy - wall + 0.1))

    def water(self, h, color=BLUE, op=0.35):
        r = Rectangle(width=2 * self.hw - 0.1, height=max(h, 0.02), stroke_width=0, fill_color=color, fill_opacity=op)
        return r.move_to(pt(self.cx, self.cy - self.wall + 0.05 + max(h, 0.02) / 2))


# ---- the blot plot -----------------------------------------------------------------------------
U = 0.9
BASE = -2.3
AX = -5.0
BW = 1.0


def bar(cx, v, strong):
    return Rectangle(width=BW, height=v * U, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                     fill_opacity=0.85 if strong else 0.45).move_to(pt(cx, BASE + v * U / 2))


def seg(cx, v0, v1):
    return Rectangle(width=BW, height=(v1 - v0) * U, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95) \
        .move_to(pt(cx, BASE + (v0 + v1) / 2 * U))


def vlab(cx, v):
    return M(f"{v:.1f}", 22, TEXT).move_to(pt(cx, BASE + v * U + 0.25))


def fluxlab(cx, v0, v1):
    return M(f"{v1:.1f} − {v0:.1f} = {v1 - v0:.1f}", 24, YELLOW).move_to(pt(cx, 2.55))


def axes():
    ax = VGroup(Line(pt(AX, BASE), pt(AX, BASE + 5 * U), color=GREY, stroke_width=3),
                Line(pt(AX, BASE), pt(5.6, BASE), color=GREY, stroke_width=3))
    for k in range(5):
        ax.add(Line(pt(AX - 0.08, BASE + k * U), pt(AX, BASE + k * U), color=GREY, stroke_width=3))
        ax.add(M(str(k), 22, GREY).move_to(pt(AX - 0.4, BASE + k * U)))
    ylab = T("LC3-II / actin", 22, GREY).rotate(PI / 2).move_to(pt(-6.0, BASE + 2 * U))
    ax.add(ylab)
    return ax


def legend():
    a = Square(0.22, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.45)
    ta = T("without bafilomycin", 22, TEXT)
    b = Square(0.22, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8)
    tb = T("with bafilomycin", 22, TEXT)
    row1 = VGroup(a, ta).arrange(RIGHT, buff=0.15)
    row2 = VGroup(b, tb).arrange(RIGHT, buff=0.15)
    return VGroup(row1, row2).arrange(RIGHT, buff=0.8).move_to(pt(0.2, 3.2))


def glabel(cx, name):
    return T(name, 26, TEXT).move_to(pt(cx, BASE - 0.4))


class S00Title(TitleCard):
    LESSON = "Protein quality control and organelle turnover"
    TITLE = "Count the flux, not the dots"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        cell = Ellipse(width=5.6, height=5.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06) \
            .move_to(pt(-3.9, 0.1))
        first = VGroup(*[autop(p) for p in [(-4.7, 1.0), (-3.1, -0.4), (-4.5, -1.2)]])
        more = VGroup(*[autop(p) for p in [(-3.2, 1.4), (-4.3, 0.0), (-2.6, 0.7), (-3.6, -1.8), (-5.3, -0.2)]])
        cl = lbl("autophagosomes", BLUE, 26).move_to(pt(-3.9, -2.95))
        self.at("You count")
        self.play(FadeIn(cell), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(a, scale=0.6) for a in first], lag_ratio=0.25), FadeIn(cl), run_time=1.4)
        self.at("you find more")
        self.play(LaggedStart(*[FadeIn(a, scale=0.6) for a in more], lag_ratio=0.2), run_time=1.5)
        self.at("make more of them")
        self.play(Indicate(more, color=BLUE, scale_factor=1.15), run_time=1.0)
        self.at("destroy fewer")
        self.play(Indicate(more, color=ORANGE, scale_factor=1.15), run_time=1.0)

        s = Sink(3.4, 0.0)
        w0 = s.water(0.7)
        self.at("Think of a sink")
        self.play(Create(s.basin), FadeIn(s.tap), FadeIn(s.drain), FadeIn(w0), run_time=1.0)
        tap_c = chip("made more?", BLUE, 24).move_to(pt(s.cx + 1.5, s.cy + 2.45))
        dr_c = chip("destroyed fewer?", ORANGE, 24).move_to(pt(s.cx - 0.5, s.cy - 2.5))
        self.at("tap is on harder")
        w1 = s.water(1.9)
        self.play(FadeIn(s.stream), FadeIn(tap_c), Transform(w0, w1), run_time=1.6)
        self.at("drain is blocked")
        self.play(FadeIn(s.plug, scale=0.5), FadeIn(dr_c), run_time=0.8)
        q = T("?", 90, RED, weight=BOLD).move_to(pt(-0.2, 0.1))
        self.at("fails on its own")
        self.play(FadeIn(q, scale=0.5), Indicate(tap_c, color=RED), Indicate(dr_c, color=RED), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Route(SpokenScene):
    def construct(self):
        cell = Ellipse(width=12.4, height=6.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.05) \
            .move_to(pt(0, -0.15))
        lyso = Circle(radius=1.9, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.12).move_to(pt(3.7, 0))
        ll = lbl("lysosome", ORANGE, 24).move_to(pt(3.7, 1.45))
        C = pt(-3.4, 0)
        blob = Circle(radius=0.6, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to(C)
        cl = lbl("cytoplasm", GREY, 24).move_to(pt(-3.4, -2.0))
        self.play(FadeIn(cell), FadeIn(lyso), FadeIn(ll), run_time=0.8)
        self.play(FadeIn(blob), FadeIn(cl), run_time=0.6)

        def arcs(span):
            st = 3 * PI / 2 - span / 2
            return VGroup(Arc(radius=1.5, start_angle=st, angle=span, arc_center=C, color=BLUE, stroke_width=5),
                          Arc(radius=1.05, start_angle=st, angle=span, arc_center=C, color=BLUE, stroke_width=5))
        a1, a2, a3 = arcs(2.6), arcs(4.8), arcs(2 * PI - 0.001)
        self.at("cup shaped membrane")
        self.play(Create(a1), run_time=1.3)
        self.play(Transform(a1, a2), run_time=1.5)
        self.at("closes into")
        self.play(Transform(a1, a3), run_time=1.2)
        apl = lbl("autophagosome", BLUE, 26).move_to(pt(-3.4, 1.85))
        self.play(FadeIn(apl), run_time=0.5)
        self.at("two membranes")
        self.play(Indicate(a1[0], color=BLUE, scale_factor=1.08), Indicate(a1[1], color=BLUE, scale_factor=1.08), run_time=1.0)
        outer_d = ring_dots(C, 1.5, 10, dr=0.09)
        inner_d = ring_dots(C, 1.05, 8, start=0.3, dr=0.09)
        key = VGroup(Dot(radius=0.08, color=PURPLE), T("LC3-II", 26, PURPLE)).arrange(RIGHT, buff=0.15).move_to(pt(-5.2, 3.1))
        self.at("lipid linked")
        self.play(FadeIn(outer_d, lag_ratio=0.1), FadeIn(inner_d, lag_ratio=0.1), FadeIn(key), run_time=1.4)

        grp = VGroup(a1, blob, outer_d, inner_d, apl)
        self.at("fuses with")
        self.remove(cl)
        self.play(grp.animate.shift(RIGHT * 3.9), run_time=1.2)
        # outer membrane joins the lysosome membrane; its dots end up on the rim
        rim = [pt(3.7 + 1.9 * math.cos(a), 1.9 * math.sin(a)) for a in np.linspace(2.4, 3.9, 10)]
        self.play(FadeOut(a1[0]), FadeOut(apl), FadeOut(outer_d),
                  Flash(pt(1.8, 0), color=ORANGE, flash_radius=0.5), run_time=0.8)
        inner_ring = a1[1]
        inner_grp = VGroup(inner_ring, blob)
        self.play(inner_grp.animate.shift(RIGHT * 3.2), inner_d.animate.shift(RIGHT * 3.2), run_time=0.9)
        self.at("its contents are digested")
        self.play(FadeOut(inner_ring, scale=0.3), FadeOut(blob, scale=0.3), run_time=1.3)
        self.at("are destroyed there")
        self.play(FadeOut(inner_d, scale=0.2), Indicate(lyso, color=ORANGE, scale_factor=1.04), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Block(SpokenScene):
    def construct(self):
        L = pt(-3.3, -0.7)
        lyso = Circle(radius=2.0, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.12).move_to(L)
        ll = lbl("lysosome", ORANGE, 26).move_to(L + DOWN * 2.45)
        pump = chip("V-ATPase", ORANGE, 26).move_to(L + UP * 2.4)
        pr = T("protons in", 24, ORANGE).move_to(L + UP * 3.95)
        pa = Arrow(L + UP * 3.65, L + UP * 2.8, buff=0.05, color=ORANGE, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(lyso), FadeIn(ll), run_time=0.5)
        self.at("Now block")
        self.play(FadeIn(pump), GrowArrow(pa), FadeIn(pr), run_time=0.8)
        baf = chip("bafilomycin", RED, 26).move_to(L + UP * 2.4 + RIGHT * 3.2)
        cross = VGroup(Line(L + UP * 3.2 + LEFT * 0.5, L + UP * 3.2 + RIGHT * 0.5, color=RED, stroke_width=9))
        self.at("blocks the")
        self.play(FadeIn(baf, shift=LEFT * 0.3), run_time=0.7)
        self.play(Create(cross), pa.animate.set_color(GREY), pr.animate.set_color(GREY), run_time=0.7)
        self.at("pump that keeps")
        self.play(Indicate(pump, color=ORANGE), run_time=0.9)
        self.at("degradation stops")
        v = VGroup(Circle(radius=0.95, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.1).move_to(L),
                   ring_dots(L, 0.95, 8, start=0.4, dr=0.09))
        self.play(lyso.animate.set_stroke(GREY).set_fill(GREY, 0.1), ll.animate.set_color(GREY), FadeIn(v, scale=0.5), run_time=1.2)
        self.at("Assume the block")
        self.play(Indicate(baf, color=RED), run_time=0.8)
        self.at("otherwise have been destroyed")
        self.play(*[d.animate.set_color(YELLOW).scale(1.5) for d in v[1]], run_time=0.8)
        self.play(Indicate(v[1], color=YELLOW, scale_factor=1.15), run_time=0.8)
        f0 = T("flux", 40, YELLOW, weight=BOLD)
        f1 = VGroup(T("LC3-II", 30, PURPLE), T("with bafilomycin", 30, RED)).arrange(RIGHT, buff=0.15)
        f2 = VGroup(T("−", 30, TEXT), T("LC3-II", 30, PURPLE), T("without", 30, GREY)).arrange(RIGHT, buff=0.15)
        eq = VGroup(VGroup(f0, T("=", 40, TEXT)).arrange(RIGHT, buff=0.2), f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        eq.move_to(pt(3.4, 0.2))
        self.at("equals")
        self.play(FadeIn(eq[0]), FadeIn(f1), run_time=0.8)
        self.at("minus")
        self.play(FadeIn(f2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Induce(SpokenScene):
    def construct(self):
        ax = axes()
        lg = legend()
        cC, cS = -2.3, 2.3
        self.at("made up data set")
        self.play(Create(ax), FadeIn(lg), run_time=1.2)
        self.at("normalized to actin")
        self.play(Indicate(ax[-1], color=YELLOW), run_time=0.8)
        b0, b1 = bar(cC - 0.6, 1.0, False), bar(cC + 0.6, 2.0, True)
        self.at("Control cells read")
        self.play(FadeIn(glabel(cC, "Control")), GrowFromEdge(b0, DOWN), FadeIn(vlab(cC - 0.6, 1.0)), run_time=0.9)
        self.at("and 2 with it")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(vlab(cC + 0.6, 2.0)), run_time=0.9)
        s0 = seg(cC + 0.6, 1.0, 2.0)
        self.at("flux is 2")
        self.play(FadeIn(s0), FadeIn(fluxlab(cC, 1.0, 2.0)), run_time=0.9)
        c0, c1 = bar(cS - 0.6, 1.5, False), bar(cS + 0.6, 4.5, True)
        self.at("Starved cells read")
        self.play(FadeIn(glabel(cS, "Starved")), GrowFromEdge(c0, DOWN), FadeIn(vlab(cS - 0.6, 1.5)), run_time=0.9)
        self.at("and 4")
        self.play(GrowFromEdge(c1, DOWN), FadeIn(vlab(cS + 0.6, 4.5)), run_time=1.0)
        s1 = seg(cS + 0.6, 1.5, 4.5)
        fl = fluxlab(cS, 1.5, 4.5)
        self.at("Their flux")
        self.play(FadeIn(s1), FadeIn(fl), run_time=0.9)
        tri = VGroup(Arrow(pt(-0.55, 2.55), pt(0.55, 2.55), buff=0, color=YELLOW, stroke_width=6, tip_length=0.25),
                     M("× 3", 30, YELLOW).move_to(pt(0, 2.05)))
        self.at("triples")
        self.play(FadeIn(tri), run_time=0.9)
        self.at("More autophagosomes")
        note = VGroup(T("more made", 26, BLUE), T("and", 26, TEXT), T("more destroyed", 26, ORANGE)).arrange(RIGHT, buff=0.2)
        note.move_to(pt(0.2, -3.35))
        self.play(FadeIn(note), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Drug(SpokenScene):
    def construct(self):
        ax = axes()
        lg = legend()
        cC, cS, cD = -3.6, 0.2, 4.0
        old = VGroup(bar(cC - 0.6, 1.0, False), bar(cC + 0.6, 2.0, True), seg(cC + 0.6, 1.0, 2.0),
                     vlab(cC - 0.6, 1.0), vlab(cC + 0.6, 2.0), fluxlab(cC, 1.0, 2.0), glabel(cC, "Control"),
                     bar(cS - 0.6, 1.5, False), bar(cS + 0.6, 4.5, True), seg(cS + 0.6, 1.5, 4.5),
                     vlab(cS - 0.6, 1.5), vlab(cS + 0.6, 4.5), fluxlab(cS, 1.5, 4.5), glabel(cS, "Starved"))
        self.add(ax, lg, old)
        d0, d1 = bar(cD - 0.6, 3.0, False), bar(cD + 0.6, 3.2, True)
        self.at("Now drug")
        self.play(FadeIn(glabel(cD, "Drug D")), run_time=0.6)
        self.at("has the most")
        self.play(GrowFromEdge(d0, DOWN), FadeIn(vlab(cD - 0.6, 3.0)), run_time=1.0)
        self.play(Indicate(d0, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("3 2")
        self.play(GrowFromEdge(d1, DOWN), FadeIn(vlab(cD + 0.6, 3.2)), run_time=0.9)
        sd = seg(cD + 0.6, 3.0, 3.2)
        fd = fluxlab(cD, 3.0, 3.2)
        self.at("flux is only")
        self.play(FadeIn(sd), FadeIn(fd), run_time=0.8)
        fifth = M("0.2 is 1/5 of 1.0", 22, YELLOW).move_to(pt(cD, 2.1))
        self.at("1 fifth")
        self.play(FadeIn(fifth), run_time=0.8)
        verdict = T("blocks fusion or degradation, not induction", 28, RED).move_to(pt(0.2, -3.35))
        self.at("blocks fusion")
        self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.9)
        withs = [o for o in old if isinstance(o, Rectangle) and o.get_fill_opacity() > 0.5] + [d1, sd]
        self.at("would look like")
        self.play(*[w.animate.set_opacity(0.2) for w in withs], FadeOut(verdict), run_time=0.9)
        box = SurroundingRectangle(d0, color=RED, buff=0.08, stroke_width=4)
        strong = T("read alone, drug D looks like the strongest inducer", 28, RED).move_to(pt(0.2, -3.35))
        self.at("strongest inducer")
        self.play(Create(box), FadeIn(strong), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        cx0, cx1 = -4.4, -2.9
        s = Sink(3.6, 0.0)
        water = s.water(0.9)
        tapc = chip("tap: made", BLUE, 24).move_to(pt(s.cx + 1.55, s.cy + 2.45))
        drc = chip("drain: destroyed", ORANGE, 24).move_to(pt(s.cx - 0.45, s.cy - 2.5))
        ylab = T("LC3-II", 26, PURPLE).move_to(pt(-3.5, 2.5))
        b0 = bar(cx0, 2.0, False)
        base = Line(pt(-5.2, BASE), pt(-1.5, BASE), color=GREY, stroke_width=3)
        self.at("do not read")
        self.play(FadeIn(base), FadeIn(ylab), GrowFromEdge(b0, DOWN), run_time=1.0)
        self.at("fuller")
        self.play(Create(s.basin), FadeIn(s.tap), FadeIn(s.drain), FadeIn(water), FadeIn(s.stream), run_time=1.2)
        self.at("tap or the drain")
        self.play(FadeIn(tapc), FadeIn(drc), run_time=0.8)
        b1 = bar(cx1, 3.0, True)
        w2 = s.water(1.5)
        self.at("lysosomal inhibitor")
        self.play(FadeIn(s.plug, scale=0.5), Transform(water, w2), GrowFromEdge(b1, DOWN), run_time=1.6)
        sg = seg(cx1, 2.0, 3.0)
        extra = Rectangle(width=2 * s.hw - 0.1, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.45) \
            .move_to(pt(s.cx, s.cy - s.wall + 0.05 + 1.5 + 0.3))
        self.at("subtract")
        self.play(FadeIn(sg), run_time=0.8)
        fl = T("flux", 30, YELLOW, weight=BOLD).move_to(pt(cx1 + 1.35, BASE + 2.5 * U))
        self.at("difference shows")
        self.play(FadeIn(fl), Indicate(sg, color=YELLOW), FadeIn(extra), run_time=1.0)
        box = SurroundingRectangle(b0, color=RED, buff=0.1, stroke_width=4)
        self.at("steady state")
        self.play(Create(box), run_time=0.8)
        self.at("Keep the rule")
        self.play(Indicate(fl, color=YELLOW, scale_factor=1.3), Indicate(sg, color=YELLOW), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Measure the flux, not just the dots."
