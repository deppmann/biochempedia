"""Too few neurons, or the wrong place  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = progenitors (radial glia) and their fibers
  YELLOW = neurons
  RED    = what goes wrong: the virus, the mutant X, the failure chips
  GREEN  = the normal X
  ORANGE = spindle pole (centrosome)
  TEAL   = microtubules (including the spindle's)
  PURPLE = doublecortin
  GOLD   = the switch from making progenitors to making neurons
  GREY   = tissue outlines, ventricle, labels, de-emphasized
  WHITE (TEXT) = nucleus
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow from it to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def slab(cx, cy, w, h, op=0.12):
    return RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=op).move_to([cx, cy, 0])


def ndot(x, y, r=0.09, color=YELLOW):
    return Dot([x, y, 0], radius=r, color=color)


def panel(cx, w, title=None, cortex=True):
    """tissue column: outline, ventricle bar at the bottom, shaded cortex zone at the top."""
    g = VGroup()
    out = RoundedRectangle(corner_radius=0.15, width=w, height=6.6, stroke_color=GREY, stroke_width=3).move_to([cx, 0, 0])
    vent = RoundedRectangle(corner_radius=0.08, width=w - 0.4, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([cx, -2.95, 0])
    g.add(out, vent)
    zone = None
    if cortex:
        zone = Rectangle(width=w - 0.04, height=1.7, stroke_width=0, fill_color=GREY, fill_opacity=0.14).move_to([cx, 1.75, 0])
        g.add(zone)
    if title:
        g.add(T(title, 26, GREY).move_to([cx, 2.95 if not cortex else 3.0, 0]))
    g.zone = zone
    return g


def soma(x, y, r=0.3, badge=None):
    body = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.4)
    nuc = Dot(radius=r * 0.42, color=TEXT)
    g = VGroup(body, nuc)
    g.move_to([x, y, 0])
    return g


def prog(x, y=-2.3):
    """a progenitor: a tall blue cell on the ventricle with its fiber running up."""
    cell = Ellipse(width=0.5, height=0.85, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([x, y, 0])
    fib = Line([x, y + 0.42, 0], [x, 2.55, 0], color=BLUE, stroke_width=2.5, stroke_opacity=0.7)
    return VGroup(cell, fib)


class S00Title(TitleCard):
    LESSON = "Microcephaly and malformations"
    TITLE = "Too few neurons, or the wrong place"


# ---------------------------------------------------------------------------------------------
class S01Two(SpokenScene):
    """two cortices that went wrong for opposite reasons."""

    def construct(self):
        rng = np.random.RandomState(4)
        t1 = T("Child 1", 28, GREY).move_to([-3.3, 0.85, 0])
        t2 = T("Child 2", 28, GREY).move_to([3.3, 3.05, 0])
        left = slab(-3.3, -1.0, 4.6, 2.8)
        right = slab(3.3, 0.1, 4.6, 5.0)
        self.at("Two children")
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(left), FadeIn(right), run_time=0.7)

        rows = VGroup()
        for i in range(6):
            y = -2.1 + i * 0.36
            for j in range(8):
                rows.add(ndot(-5.0 + j * 0.5 + 0.3, y))
        lab_l = T("small, layers in\nthe usual order", 24, GREY, line_spacing=0.8).move_to([-3.3, -2.95, 0])
        self.at("In one child")
        self.play(Indicate(left, color=GREY, scale_factor=1.04), run_time=0.6)
        self.at("its layers sit")
        self.play(LaggedStart(*[FadeIn(rows[k * 8:(k + 1) * 8], shift=UP * 0.1) for k in range(6)], lag_ratio=0.25),
                  FadeIn(lab_l), run_time=1.8)

        pts = []
        while len(pts) < 46:
            p = (rng.uniform(1.2, 5.4), rng.uniform(-2.2, 2.4))
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.28 for q in pts):
                pts.append(p)
        scat = VGroup(*[ndot(x, y) for x, y in pts])
        lab_r = T("thick, nearly smooth,\nneurons out of place", 24, GREY, line_spacing=0.8).move_to([3.3, -3.05, 0])
        self.at("In the other")
        self.play(Indicate(right, color=GREY, scale_factor=1.03), FadeIn(lab_r), run_time=0.6)
        self.at("many neurons")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in scat], lag_ratio=0.03), run_time=1.6)

        self.at("Which step")
        q = T("Which step failed?", 40, TEXT).move_to([-3.3, 2.2, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Jobs(SpokenScene):
    """progenitors divide and make a neuron; the neuron climbs a fiber; two ways to fail."""

    def construct(self):
        cx = -3.0
        pan = panel(cx, 4.6, cortex=False)
        top = RoundedRectangle(corner_radius=0.08, width=4.2, height=0.14, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.5).move_to([cx, 2.62, 0])
        l_v = lab_right("ventricle", GREY, -0.4, -2.95, [cx + 2.0, -2.95, 0], 26)
        l_o = lab_right("outer surface", GREY, -0.4, 2.62, [cx + 2.0, 2.62, 0], 26)
        self.at("Building a cortex")
        self.play(FadeIn(pan), FadeIn(top), FadeIn(l_v), FadeIn(l_o), run_time=0.8)

        pa, pb = prog(cx - 1.0), prog(cx + 0.5)
        self.at("First")
        self.play(FadeIn(pa, shift=UP * 0.2), FadeIn(pb, shift=UP * 0.2), run_time=0.7)
        lab = lab_right("radial glia", BLUE, 0.2, -2.3, [cx + 0.9, -2.3, 0], 28)
        self.play(FadeIn(lab), run_time=0.4)

        self.at("more of themselves")
        pa2, pa3 = prog(cx - 1.3), prog(cx - 0.7)
        pb2, pb3 = prog(cx + 0.2), prog(cx + 0.8)
        self.play(ReplacementTransform(pa, VGroup(pa2, pa3)), ReplacementTransform(pb, VGroup(pb2, pb3)), run_time=0.9)

        self.at("make neurons")
        nx = cx + 0.8
        n = soma(nx, -1.55, 0.2)
        n.set_opacity(0)
        self.play(n.animate.set_opacity(1), run_time=0.01)
        n.scale(0.1)
        self.play(n.animate.scale(10), run_time=0.6)
        lab_n = lab_right("neuron", YELLOW, 0.2, -1.35, [nx + 0.3, -1.45, 0], 28)
        self.play(FadeIn(lab_n), run_time=0.4)

        self.at("Second")
        self.play(Indicate(n, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.at("to its layer")
        self.play(n.animate.move_to([nx, 1.75, 0]), FadeOut(lab_n), run_time=1.6, rate_func=smooth)

        self.at("ways to go")
        c1 = chip("Too few neurons made", BLUE, 30).move_to([3.7, 1.0, 0])
        c2 = chip("Made, but stalled", YELLOW, 30).move_to([3.7, -0.8, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)
        self.at("Too few neurons are made")
        self.play(Indicate(c1, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("Or neurons are made")
        self.play(Indicate(c2, color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Number(SpokenScene):
    """the pool doubles each symmetric round; switching one round early halves it."""

    def construct(self):
        xs = [-5.6, -3.9, -2.2, -0.5]
        sp = 0.62
        g3 = [(i - 3.5) * sp for i in range(8)]
        g2 = [(g3[2 * i] + g3[2 * i + 1]) / 2 for i in range(4)]
        g1 = [(g2[2 * i] + g2[2 * i + 1]) / 2 for i in range(2)]
        g0 = [(g1[0] + g1[1]) / 2]
        gens = [g0, g1, g2, g3]

        def pd(x, y):
            return Dot([x, y, 0], radius=0.16, color=BLUE)

        dots = [[pd(xs[k], y) for y in gens[k]] for k in range(4)]
        edges = [[], [], [], []]
        for k in range(1, 4):
            for i, y in enumerate(gens[k]):
                py = gens[k - 1][i // 2]
                edges[k].append(Line([xs[k - 1], py, 0], [xs[k], y, 0], color=GREY, stroke_width=2))

        self.at("Take the first")
        lab = T("progenitors", 26, BLUE).move_to([xs[0] + 0.3, 1.3, 0])
        self.play(FadeIn(dots[0][0], scale=0.3), FadeIn(lab), run_time=0.6)

        self.at("Each division")
        for k in range(1, 4):
            self.play(*[Create(e) for e in edges[k]], *[FadeIn(d, scale=0.3) for d in dots[k]], run_time=0.7)
            self.wait(0.15)
        self.at("doubles the pool")
        cap = T("each round doubles the pool", 28, BLUE).move_to([-2.9, -3.2, 0])
        self.play(FadeOut(lab), FadeIn(cap), run_time=0.5)

        # the switch and the neurons
        sw_x = 0.4
        sw = DashedLine([sw_x, -2.7, 0], [sw_x, 2.7, 0], color=GOLD, stroke_width=4)
        sw_l = T("switch to neurons", 26, GOLD).move_to([sw_x + 0.2, 3.1, 0])
        nxs = 1.7
        neurons = VGroup(*[ndot(nxs, y, 0.16) for y in g3])
        links = VGroup(*[arr([xs[3] + 0.2, y, 0], [nxs - 0.22, y, 0], YELLOW, 2.5, 0.14) for y in g3])
        self.at("switch to making neurons")
        self.play(Create(sw), FadeIn(sw_l), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d, scale=0.3)) for a, d in zip(links, neurons)],
                              lag_ratio=0.06), run_time=1.0)
        nl = T("neurons", 28, YELLOW).move_to([nxs + 0.1, -3.2, 0])
        self.play(FadeIn(nl), run_time=0.4)

        # one round early
        self.at("In this simple model")
        mdl = chip("a simple model", GREY, 26).move_to([-4.6, 3.05, 0])
        self.play(FadeIn(mdl, shift=DOWN * 0.1), run_time=0.5)
        self.at("one round early")
        sw_x2 = -1.35
        neurons2 = VGroup(*[ndot(-0.1, y, 0.16) for y in g2])
        links2 = VGroup(*[arr([xs[2] + 0.2, y, 0], [-0.1 - 0.22, y, 0], YELLOW, 2.5, 0.14) for y in g2])
        self.play(sw.animate.move_to([sw_x2, 0, 0]), sw_l.animate.move_to([sw_x2 + 0.2, 3.1, 0]),
                  FadeOut(VGroup(*dots[3], *edges[3], neurons, links, nl)), run_time=1.0)
        self.at("halves the pool")
        cap2 = T("half the pool, half the neurons", 28, YELLOW).move_to([-2.0, -3.2, 0])
        nl2 = T("neurons", 28, YELLOW).move_to([-0.1 + 0.1, 2.9, 0])
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d, scale=0.3)) for a, d in zip(links2, neurons2)],
                              lag_ratio=0.1), FadeOut(cap), FadeIn(cap2), run_time=1.0)
        self.wait(0.2)

        # microcephaly + spindle
        self.at("Primary microcephaly")
        tag = chip("primary microcephaly", RED, 28).move_to([4.2, 2.9, 0])
        norm = T("layers usually normal", 26, GREY).move_to([4.2, 2.1, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.5)
        self.at("broadly normal")
        self.play(FadeIn(norm), run_time=0.4)

        self.at("Most of them")
        cc = [4.4, -0.55, 0]
        cell = Circle(radius=1.3, stroke_color=GREY, stroke_width=3).move_to(cc)
        self.play(Create(cell), run_time=0.5)
        self.at("such as")
        pl, pr = np.array([cc[0] - 0.95, cc[1], 0]), np.array([cc[0] + 0.95, cc[1], 0])
        fibs = VGroup(*[ArcBetweenPoints(pl, pr, angle=a, color=TEAL, stroke_width=3) for a in (-0.9, -0.45, 0, 0.45, 0.9)])
        pole_l = Dot(pl, radius=0.15, color=ORANGE)
        pole_r = Dot(pr, radius=0.15, color=ORANGE)
        lab_p = T("spindle pole", 26, ORANGE).move_to([cc[0], cc[1] - 1.75, 0])
        gene = T("ASPM", 30, ORANGE, weight=BOLD).move_to([cc[0], cc[1] + 1.75, 0])
        self.play(FadeIn(gene), run_time=0.4)
        self.at("spindle pole")
        self.play(Create(fibs), FadeIn(pole_l), FadeIn(pole_r), run_time=0.7)
        self.play(FadeIn(lab_p), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Zika(SpokenScene):
    """Zika virus fills progenitors; fewer neurons result; two cautions."""

    def construct(self):
        rng = np.random.RandomState(7)
        R = 1.15
        xs = [-4.3, 0.0, 4.3]
        cy = 1.35

        def cellc(x, col, r=R):
            return Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.2).move_to([x, cy, 0])

        stem, pro, imm = cellc(xs[0], GREY), cellc(xs[1], BLUE), cellc(xs[2], YELLOW)
        l_s = T("stem cell", 26, GREY).move_to([xs[0], cy - 1.45, 0])
        l_p = T("cortical progenitor", 26, BLUE).move_to([xs[1], cy - 1.45, 0])
        l_i = T("immature neuron", 26, YELLOW).move_to([xs[2], cy - 1.45, 0])
        self.at("A virus")
        self.play(FadeIn(VGroup(stem, l_s, pro, l_p, imm, l_i), shift=UP * 0.15), run_time=0.8)

        def virus(x, y):
            return Dot([x, y, 0], radius=0.11, color=RED)

        def inside(x, n):
            out = []
            for _ in range(n):
                while True:
                    a, b = rng.uniform(-0.7, 0.7, 2)
                    if a * a + b * b < 0.5:
                        break
                out.append((x + a, cy + b))
            return out

        self.at("Zika virus")
        vs = []
        anims = []
        for x, n in ((xs[0], 1), (xs[1], 11), (xs[2], 1)):
            for (px, py) in inside(x, n):
                v = virus(px + rng.uniform(-0.2, 0.2), 3.4)
                vs.append((v, px, py))
        for v, px, py in vs:
            v.set_opacity(0)
        self.add(*[v for v, _, _ in vs])
        for v, px, py in vs:
            v.set_opacity(1)
        self.play(LaggedStart(*[v.animate.move_to([px, py, 0]) for v, px, py in vs], lag_ratio=0.08), run_time=2.2)

        self.at("far more readily")
        self.play(pro.animate.set_stroke(RED, 5), run_time=0.5)
        vgroup_p = VGroup(*[v for v, px, py in vs if abs(px - xs[1]) < 1.1])

        # killed some, slowed the rest
        self.at("killed some")
        mini_pos = [(-0.55, cy + 0.5), (0.55, cy + 0.5), (-0.55, cy - 0.5), (0.55, cy - 0.5)]
        minis = VGroup(*[Circle(radius=0.42, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25)
                         .move_to([x, y, 0]) for x, y in mini_pos])
        mdots = VGroup(*[VGroup(*[Dot([x + dx, y + dy, 0], radius=0.07, color=RED) for dx, dy in ((-0.1, 0.05), (0.12, -0.1), (0.0, 0.15))])
                         for x, y in mini_pos])
        self.play(ReplacementTransform(pro, minis), ReplacementTransform(vgroup_p, mdots), run_time=0.8)
        dead = VGroup(minis[1], minis[2], mdots[1], mdots[2])
        xs_cross = VGroup(*[VGroup(Line([x - 0.3, y - 0.3, 0], [x + 0.3, y + 0.3, 0], color=RED, stroke_width=5),
                                   Line([x - 0.3, y + 0.3, 0], [x + 0.3, y - 0.3, 0], color=RED, stroke_width=5))
                            for x, y in (mini_pos[1], mini_pos[2])])
        self.play(dead.animate.set_opacity(0.25), FadeIn(xs_cross), run_time=0.7)
        self.at("slowed the growth")
        slow = T("slower growth", 26, GREY).move_to([0, cy - 1.45 - 0.5, 0])
        self.play(FadeOut(l_p), FadeIn(slow), Indicate(VGroup(minis[0], minis[3]), color=BLUE, scale_factor=1.1), run_time=0.8)

        self.at("Two cautions")
        c1 = chip("cultured cells and organoids: what the virus can do", GREY, 26).move_to([0, -1.35, 0])
        c2 = chip("most infections in pregnancy: no microcephaly", GREY, 26).move_to([0, -2.25, 0])
        self.at("cultured cells")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at("most infections")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)

        # fewer neurons
        self.at("short of neurons")
        slots = VGroup()
        for i in range(6):
            x = -1.5 + i * 0.6
            if i < 2:
                slots.add(Dot([x, -3.1, 0], radius=0.17, color=YELLOW))
            else:
                slots.add(Circle(radius=0.17, stroke_color=GREY, stroke_width=2.5).move_to([x, -3.1, 0]))
        sl = T("neurons made", 26, YELLOW).move_to([3.4, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in slots], lag_ratio=0.1), FadeIn(sl), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Place(SpokenScene):
    """neurons made but not moved: LIS1 knockdown, doublecortin, the boy."""

    def construct(self):
        # --- two panels: normal vs LIS1 knocked down -------------------------------------------
        pL, pR = panel(-3.3, 5.2, "normal"), panel(3.3, 5.2, "LIS1 knocked down")
        self.at("Now the second")
        self.play(FadeIn(pL), FadeIn(pR), run_time=0.8)

        def make_neuron(x):
            s = soma(x, -2.2, 0.3)
            tip = Dot([x, -1.7, 0], radius=0.1, color=YELLOW)
            proc = always_redraw(lambda s=s, tip=tip: Line(s[0].get_top(), tip.get_center(), color=YELLOW, stroke_width=7))
            return s, tip, proc

        sA, tA, prA = make_neuron(-3.3)
        sB, tB, prB = make_neuron(3.3)
        self.at("Here the progenitors")
        self.add(prA, prB)
        pgs = VGroup(*[prog(x, -2.4) for x in (-4.6, -2.0, 2.0, 4.6)])
        self.play(FadeIn(pgs, shift=UP * 0.1), run_time=0.6)
        self.at("neurons failed")
        self.play(FadeIn(sA), FadeIn(tA), FadeIn(sB), FadeIn(tB), run_time=0.6)

        self.play(Indicate(VGroup(sA, sB), color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.at("knocked down")
        self.wait(0.1)
        self.at("kept extending")
        self.play(tA.animate.move_to([-3.3, 1.9, 0]), tB.animate.move_to([3.3, 1.9, 0]), run_time=1.2)
        self.at("barely moved")
        self.play(sA.animate.move_to([-3.3, 1.45, 0]),
                  Indicate(sB, color=RED, scale_factor=1.35), run_time=1.2)
        nuc_lab = lab_right("nucleus stays", RED, 4.0, -2.2, [3.65, -2.2, 0], 26)
        self.play(FadeIn(nuc_lab), run_time=0.4)

        # --- doublecortin on microtubules -------------------------------------------------------
        self.at("Another gene")
        prA.clear_updaters(); prB.clear_updaters()
        self.play(FadeOut(VGroup(pL, pR, pgs, sA, tA, prA, sB, tB, prB, nuc_lab)), run_time=0.6)
        cxn = -2.6
        body = Circle(radius=0.85, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.35).move_to([cxn, -1.7, 0])
        nuc = Circle(radius=0.4, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).move_to([cxn, -1.7, 0])
        proc = Rectangle(width=0.8, height=4.0, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                         fill_opacity=0.25).move_to([cxn, 1.0, 0])
        bigneuron = VGroup(proc, body, nuc)
        self.play(FadeIn(bigneuron, shift=UP * 0.2), run_time=0.7)
        mts = VGroup(*[Line([cxn + dx, -1.3, 0], [cxn + dx, 2.8, 0], color=TEAL, stroke_width=4) for dx in (-0.22, 0, 0.22)])
        self.at("double cordon")
        dcs = VGroup(*[Dot([cxn + dx, y, 0], radius=0.07, color=PURPLE) for dx in (-0.22, 0.22) for y in (-0.6, 0.3, 1.2, 2.1)])
        lab_dc = lab_right("doublecortin", PURPLE, -0.6, 1.2, [cxn + 0.5, 1.2, 0], 30)
        self.play(Create(mts), run_time=0.5)
        self.play(FadeIn(dcs, lag_ratio=0.1), FadeIn(lab_dc), run_time=0.8)
        self.at("binds microtubules")
        lab_mt = lab_right("microtubules", TEAL, -0.6, -0.4, [cxn + 0.3, -0.4, 0], 30)
        self.play(FadeIn(lab_mt), run_time=0.5)
        self.at("stabilizes them")
        self.play(Indicate(mts, color=TEAL, scale_factor=1.05), run_time=0.8)

        # --- the boy -----------------------------------------------------------------------------
        self.at("A male has")
        self.play(FadeOut(VGroup(bigneuron, mts, dcs, lab_dc, lab_mt)), run_time=0.6)
        pan = panel(-2.5, 5.0, "male")
        xbig = T("X", 110, RED, weight=BOLD).move_to([3.7, 1.0, 0])
        xlab = T("a male has one X", 30, TEXT).move_to([3.7, -0.4, 0])
        self.play(FadeIn(pan), FadeIn(xbig, scale=0.6), FadeIn(xlab), run_time=0.7)

        self.at("carries the mutation")
        pos = [(-4.2, -2.2), (-3.4, -2.2), (-2.6, -2.2), (-1.8, -2.2), (-1.0, -2.2), (-3.8, -2.2), (-2.2, -2.2)]
        pos = [(-4.6 + 0.6 * i, -2.25) for i in range(8)]
        ns = VGroup()
        for (x, y) in pos:
            s = soma(x, y, 0.22)
            b = Dot([x + 0.2, y + 0.2, 0], radius=0.09, color=RED)
            ns.add(VGroup(s, b))
        legend = VGroup(Dot(radius=0.1, color=RED), T("mutant X", 26, RED)).arrange(RIGHT, buff=0.2).move_to([3.7, -1.5, 0])
        self.play(FadeIn(ns, lag_ratio=0.1), FadeIn(legend), run_time=0.9)
        self.at("no neuron makes")
        rise = [0.5, -0.1, 0.9, -0.6, 0.2, -1.1, 0.0, 3.0]
        self.play(*[n.animate.shift(UP * (1.0 + r)) for n, r in zip(ns, rise)], run_time=1.6)
        self.at("most neurons stall")
        st = T("stalled", 30, RED).move_to([3.7, -2.4, 0])
        self.play(FadeIn(st), Indicate(ns, color=RED, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Mosaic(SpokenScene):
    """a female's cortex is an X-inactivation mosaic; the closing rule."""

    def construct(self):
        cx = -3.6
        pan = panel(cx, 4.8, None)
        zl = lab_right("cortex", GREY, -0.5, 1.75, [cx + 2.45, 1.75, 0], 28)

        # six cells with two X's each
        gx, gy = [1.9, 3.6, 5.3], [1.8, 0.2]
        cells, dg, dr = VGroup(), [], []
        pattern = ["G", "R", "G", "G", "R", "R"]
        for k in range(6):
            x, y = gx[k % 3], gy[k // 3]
            circ = Circle(radius=0.62, stroke_color=GREY, stroke_width=3).move_to([x, y, 0])
            a = Dot([x - 0.22, y, 0], radius=0.15, color=GREEN)
            b = Dot([x + 0.22, y, 0], radius=0.15, color=RED)
            dg.append(a); dr.append(b)
            cells.add(VGroup(circ, a, b))
        self.at("A female has")
        self.play(FadeIn(pan), FadeIn(zl), FadeIn(cells, lag_ratio=0.1), run_time=1.0)
        leg = VGroup(Dot(radius=0.1, color=GREEN), T("normal X", 26, GREEN), Dot(radius=0.1, color=RED), T("mutant X", 26, RED))
        leg.arrange(RIGHT, buff=0.2).move_to([3.3, -1.5, 0])
        self.play(FadeIn(leg), run_time=0.4)

        self.at("silences one")
        anims = []
        for k, p in enumerate(pattern):
            col = GREEN if p == "G" else RED
            silent = dr[k] if p == "G" else dg[k]
            anims += [silent.animate.set_opacity(0.15), cells[k][0].animate.set_stroke(col, 5)]
        self.play(LaggedStart(*[AnimationGroup(anims[2 * i], anims[2 * i + 1]) for i in range(6)], lag_ratio=0.2), run_time=1.6)

        self.at("mosaic")
        mos = T("a mosaic", 30, TEXT).move_to([3.3, -2.4, 0])
        self.play(FadeIn(mos), run_time=0.4)

        # cells become neurons at the bottom of the panel
        self.at("On the standard interpretation")
        nx = [cx - 1.8 + 0.72 * i for i in range(6)]
        neurons = []
        tos = []
        for k, p in enumerate(pattern):
            x = nx[k]
            body = Circle(radius=0.28, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.4).move_to([x, -2.3, 0])
            a = Dot([x + 0.26, -2.04, 0], radius=0.1, color=GREEN)
            b = Dot([x + 0.26, -2.04, 0], radius=0.1, color=RED)
            (b if p == "G" else a).set_opacity(0)
            n = VGroup(body, a, b)
            neurons.append(n)
            tos.append(n)
        self.play(*[ReplacementTransform(cells[k], neurons[k]) for k in range(6)], FadeOut(leg), FadeOut(mos), run_time=1.4)
        leg2 = VGroup(Dot(radius=0.1, color=GREEN), T("normal X active", 26, GREEN)).arrange(RIGHT, buff=0.2).move_to([2.6, -1.9, 0])
        leg3 = VGroup(Dot(radius=0.1, color=RED), T("mutant X active", 26, RED)).arrange(RIGHT, buff=0.2).move_to([2.6, -2.6, 0])
        t1 = chip("standard interpretation", GREY, 26).move_to([3.4, 1.5, 0])
        self.play(FadeIn(leg2), FadeIn(leg3), FadeIn(t1), run_time=0.4)

        self.at("reach the cortex")
        greens = [k for k, p in enumerate(pattern) if p == "G"]
        reds = [k for k, p in enumerate(pattern) if p == "R"]
        self.play(*[neurons[k].animate.shift(UP * (3.9 + 0.12 * i)) for i, k in enumerate(greens)], run_time=1.3)
        self.at("stall partway")
        self.play(*[neurons[k].animate.shift(UP * 2.3) for k in reds], run_time=1.2)
        self.at("form a band")
        band = RoundedRectangle(corner_radius=0.1, width=4.4, height=0.9, stroke_color=RED, stroke_width=2.5,
                                fill_color=RED, fill_opacity=0.12).move_to([cx, -0.0, 0])
        bl = lab_right("band", RED, -0.5, 0.0, [cx + 2.25, 0.0, 0], 28)
        self.play(FadeIn(band), FadeIn(bl), run_time=0.7)

        self.at("The usual reading")
        t2 = chip("the usual reading", GREY, 26).move_to([3.4, 0.3, 0])
        self.play(FadeIn(t2), run_time=0.4)
        self.play(Indicate(VGroup(*neurons), color=YELLOW, scale_factor=1.1), run_time=1.0)

        self.at("So ask")
        self.play(FadeOut(VGroup(pan, zl, band, bl, leg2, leg3, t1, t2, *neurons)), run_time=0.7)
        q1 = chip("Too few neurons made", BLUE, 40).move_to([0, 1.2, 0])
        q2 = chip("Neurons made, but misplaced", YELLOW, 40).move_to([0, -1.2, 0])
        self.at("too few neurons made")
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
        self.at("made but misplaced")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Ask which step failed: too few neurons, or neurons misplaced."
