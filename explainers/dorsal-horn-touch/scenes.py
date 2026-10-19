"""Dorsal horn and dorsal column nuclei: two copies of one touch  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the direct route: touch afferents (primary afferent fibres and their terminal)
  ORANGE = the indirect route: the PSDC neuron and its axon
  GREEN  = excitatory (excitatory neurons, excitatory arrows)
  RED    = inhibitory (inhibitory neurons, inhibitory bar-ended arrows)
  PURPLE = the dorsal column nuclei (gracile, cuneate) in the brainstem
  YELLOW = a travelling spike, the vibration wave, and the 4.5 ms gap
  GOLD   = the IB4 border (one highlight), and synaptic delay in the timing chart
  GREY   = cord outline, laminae bands, dorsal column, labels

Anatomy rules kept: the cord is one flat schematic cross-section (the half on the hindpaw's side,
laminae as labelled bands, the dorsal column as a labelled box). The brainstem is only two labelled
boxes. Nothing is wired to a drawn body. The dorsal column stays on the hindpaw's own side.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def poly(pts, color, w=5, opacity=1.0):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w, opacity=opacity)
    m.set_fill(opacity=0)
    return m


def arr(a, b, color=GREEN, w=5, tip=0.2):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.2, b - perp * 0.2, color=color, stroke_width=w + 1))


def link(pa, ra, pb, rb, kind="exc", gap=0.05, color=None):
    pa, pb = np.array(pa, float), np.array(pb, float)
    d = (pb - pa) / np.linalg.norm(pb - pa)
    a = pa + d * (ra + gap)
    b = pb - d * (rb + gap)
    if kind == "exc":
        return arr(a, b, color or GREEN)
    return inhib(a, b, color or RED)


def amap(s, lc, sc):
    return lambda x, y: np.array([(x - lc[0]) * s + sc[0], (y - lc[1]) * s + sc[1], 0.0])


def lbl_right(text, size, color, pt):
    t = T(text, size, color)
    t.move_to(pt, aligned_edge=RIGHT)
    return t


def lbl_left(text, size, color, pt):
    t = T(text, size, color)
    t.move_to(pt, aligned_edge=LEFT)
    return t


class Cord:
    """The schematic half-cord. Local coordinates (x, y); f() maps them to the screen.
    Local layout: outline x -3.6..1.7, y -3.0..0.8. Dorsal column box x 0.2..1.4. Laminae x -3.3..0.0:
    IIiv 0..-0.55, III -0.55..-1.1, IV -1.1..-1.65. PSDC axon runs at x 0.55, direct axon at x 1.05."""

    def __init__(self, s=1.0, lc=(-0.95, -1.1), sc=(-0.1, -1.1), labels=True):
        self.s, self.f = s, amap(s, lc, sc)
        f = self.f
        self.outline = RoundedRectangle(corner_radius=0.45 * s, width=5.3 * s, height=3.8 * s, stroke_color=GREY,
                                        stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to(f(-0.95, -1.1))
        self.colbox = Rectangle(width=1.2 * s, height=2.3 * s, stroke_color=GREY, stroke_width=2,
                                fill_color=GREY, fill_opacity=0.22).move_to(f(0.8, -0.35))
        dl = VGroup(T("dorsal", 22, GREY), T("column", 22, GREY)).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
        dl.move_to(f(1.85, 0.2), aligned_edge=LEFT)
        self.collbl = dl
        self.bands = VGroup(*[
            Rectangle(width=3.3 * s, height=0.55 * s, stroke_color=GREY, stroke_width=1.5,
                      fill_color=GREY, fill_opacity=op).move_to(f(-1.65, yc))
            for yc, op in ((-0.275, 0.14), (-0.825, 0.26), (-1.375, 0.14))])
        self.ib4 = DashedLine(f(-3.3, 0), f(0.0, 0), color=GOLD, stroke_width=3, dash_length=0.12)
        self.ib4lbl = lbl_right("IB4 border", 22, GOLD, f(-3.8, 0.3))
        self.lamlbl = VGroup(*[lbl_right(t, 24, TEXT, f(-3.8, yc)) for t, yc in
                               (("IIiv", -0.275), ("III", -0.825), ("IV", -1.375))])
        self.base = VGroup(self.outline, self.colbox, self.bands)
        self.labels = VGroup(self.collbl, self.ib4, self.ib4lbl, self.lamlbl)


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def send(scene, pts, n=3, run=2.0, color=YELLOW, r=0.1):
    """spikes (dots) travelling along a polyline"""
    path = VMobject()
    path.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)]).set_opacity(0)
    scene.add(dots)

    def upd(m, a):
        for i, d in enumerate(m):
            aa = a - 0.13 * i
            if aa <= 0 or aa >= 1:
                d.set_opacity(0)
            else:
                d.set_opacity(1)
                d.move_to(path.point_from_proportion(aa))

    scene.play(UpdateFromAlphaFunc(dots, upd, run_time=run, rate_func=linear))
    scene.remove(dots)


def dcn(show=True, hi=None):
    """the dorsal column nuclei as labelled boxes (gracile above the cord's axons)"""
    title = T("dorsal column nuclei (DCN), brainstem", 22, PURPLE).move_to([3.1, 3.2, 0])
    g = RoundedRectangle(corner_radius=0.12, width=2.3, height=0.8, stroke_color=PURPLE, stroke_width=3,
                         fill_color=PURPLE, fill_opacity=0.18).move_to([1.65, 2.35, 0])
    c = RoundedRectangle(corner_radius=0.12, width=2.3, height=0.8, stroke_color=PURPLE, stroke_width=3,
                         fill_color=PURPLE, fill_opacity=0.08).move_to([4.55, 2.35, 0])
    gl = T("gracile", 26, TEXT).move_to(g)
    cl = T("cuneate", 26, GREY).move_to(c)
    return VGroup(title, g, c, gl, cl)


def rf_patch(center, r=0.4, label=True):
    """a patch of hindpaw skin (flat) with one receptive-field circle"""
    skin = Ellipse(width=2.5, height=1.6, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.15)
    skin.move_to(center)
    circ = Circle(radius=r, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.25).move_to(center)
    return skin, circ


class S00Title(TitleCard):
    LESSON = "Dorsal horn and dorsal column nuclei"
    TITLE = "Two Copies of One Touch"


# ---------------------------------------------------------------------------------------------
class S01Cable(SpokenScene):
    """the textbook cable, then a question mark over the dorsal horn"""

    def construct(self):
        C = Cord()
        f = C.f
        chipm = bchip("hindpaw skin indented", BLUE, 22).move_to([-4.6, -2.3, 0])
        cable_pts = [chipm.get_right() + RIGHT * 0.02, f(-3.6, -2.3), f(1.05, -2.3), f(1.05, 1.0), [1.9, 1.95]]
        cable_pts[0] = [chipm.get_right()[0], -2.3]
        cable = poly(cable_pts, BLUE, 6)
        caption = T("mouse lumbar cord, hindpaw side: schematic cross-section", 22, GREY).move_to([-0.1, -3.35, 0])
        self.at("skin")
        self.play(FadeIn(C.base), FadeIn(C.collbl), FadeIn(C.ib4), FadeIn(C.ib4lbl), FadeIn(C.lamlbl),
                  FadeIn(caption), FadeIn(chipm, shift=RIGHT * 0.2), run_time=1.2)
        self.at("textbook")
        tb = T("the textbook: a cable", 26, BLUE).move_to([4.5, 1.2, 0])
        # the cable reaches the brainstem boxes only when the narrator says brainstem
        self.play(Create(VMobject().set_points_as_corners([np.array([p[0], p[1], 0]) for p in cable_pts[:4]])
                         .set_stroke(BLUE, 6).set_fill(opacity=0)), FadeIn(tb), run_time=1.6)
        self.at("Touch spikes")
        send(self, cable_pts[:4], n=3, run=2.0)
        self.at("run up")
        boxes = dcn()
        self.play(FadeIn(boxes), Create(poly([[1.9, 0.8], [1.9, 1.95]], BLUE, 6)), run_time=1.0)
        self.at("missing branch")
        q = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.95, stroke_color=YELLOW, stroke_width=4,
                             fill_color=YELLOW, fill_opacity=0.12).move_to(f(-1.65, -0.825))
        qm = T("?", 56, YELLOW, weight=BOLD).move_to(q)
        self.play(FadeIn(q, scale=0.8), FadeIn(qm), run_time=0.7)
        self.at("circuitry")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.finish()


class S02Direct(SpokenScene):
    """the direct route: afferent axons, no synapse, to the gracile nucleus; vibration timing"""

    def construct(self):
        C = Cord()
        f = C.f
        chipm = bchip("hindpaw touch", BLUE, 24).move_to([-5.0, -2.3, 0])
        caption = T("mouse lumbar cord, hindpaw side: schematic cross-section", 22, GREY).move_to([-0.1, -3.35, 0])
        boxes = dcn()
        pts = [[chipm.get_right()[0], -2.3], f(-3.6, -2.3), f(1.05, -2.3), f(1.05, 1.0), [1.9, 1.95]]
        faint = poly(pts, BLUE, 6, opacity=0.35)
        self.add(C.base, C.collbl, C.ib4, C.ib4lbl, C.lamlbl, caption, chipm, boxes, faint)
        self.at("direct")
        lit = poly(pts, BLUE, 9)
        self.play(Create(lit), run_time=1.4)
        self.at("afferents")
        lab = T("touch afferents", 24, BLUE).move_to([-5.0, -2.85, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.at("synapse")
        nos = T("no synapse on the way", 24, BLUE).move_to([-2.0, 1.3, 0]).align_to([1.1, 0, 0], RIGHT)
        self.play(FadeIn(nos), run_time=0.5)
        send(self, pts, n=3, run=2.2)
        self.at("brainstem")
        self.play(boxes[1].animate.set_fill(PURPLE, 0.5), Indicate(boxes[3], color=YELLOW), run_time=1.0)
        # vibration panel, in this sketch
        self.at("vibration")
        wave = FunctionGraph(lambda x: 0.28 * np.sin(2 * np.pi * x / 0.52), x_range=[0, 2.6], color=YELLOW,
                             stroke_width=4).move_to([4.75, -1.1, 0])
        wlab = T("vibration", 24, YELLOW).move_to([4.75, -0.35, 0])
        self.play(Create(wave), FadeIn(wlab), run_time=1.0)
        self.at("precision")
        x0 = 4.75 - 1.3 + 0.13
        ticks = VGroup(*[Line([x0 + 0.52 * k, -2.18, 0], [x0 + 0.52 * k, -1.86, 0], color=BLUE, stroke_width=5)
                         for k in range(5)])
        tl = T("direct-route spikes", 22, BLUE).move_to([4.75, -2.6, 0])
        sk = T("in this sketch", 22, GREY).move_to([4.75, -3.05, 0])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), FadeIn(tl), FadeIn(sk), run_time=1.6)
        self.finish()


def circuit(C):
    """cells and fibres of the zone (local coordinates), returns dict of mobjects"""
    f, s = C.f, C.s
    R = {}
    R["A"] = (f(-2.2, -0.825), 0.14 * s)
    R["E"] = (f(-0.6, -0.275), 0.22 * s)
    R["G2"] = (f(-3.0, -1.35), 0.22 * s)
    R["I"] = (f(-1.55, -1.4), 0.22 * s)
    R["J"] = (f(-3.0, -0.3), 0.2 * s)
    R["P"] = (f(-0.6, -1.375), 0.28 * s)
    cols = {"A": BLUE, "E": GREEN, "G2": GREEN, "I": RED, "J": RED, "P": ORANGE}
    M_ = {}
    for k, (p, r) in R.items():
        c = Circle(radius=r, stroke_color=cols[k], stroke_width=3, fill_color=cols[k],
                   fill_opacity=0.9 if k == "A" else 0.28).move_to(p)
        M_[k] = c
    return R, M_


def fibres(C):
    f = C.f
    H = poly([f(-3.6, -2.05), f(-2.2, -2.05), f(-2.2, -0.96)], BLUE, 5)
    D = poly([f(-3.6, -2.45), f(1.05, -2.45), f(1.05, 1.1)], BLUE, 5, opacity=0.35)
    Pax = poly([f(-0.6 + 0.28, -1.375), f(0.55, -1.375), f(0.55, 1.1)], ORANGE, 5)
    return H, D, Pax


class S03Zone(SpokenScene):
    """zoom to the laminae; the zone's cells are 70 percent excitatory; the PSDC neuron; its axon goes up"""

    def construct(self):
        C = Cord(1.35, lc=(-1.15, -0.9), sc=(-1.24, -0.2))
        f, s = C.f, C.s
        R, M_ = circuit(C)
        H, D, Pax = fibres(C)
        self.add(C.base, C.collbl, D)
        self.at("also end")
        afl = lbl_right("afferent", 22, BLUE, f(-3.8, -2.05))
        self.play(Create(H), FadeIn(afl), run_time=1.0)
        self.play(FadeIn(M_["A"], scale=0.5), run_time=0.3)
        self.at("dorsal horn")
        self.play(FadeIn(C.ib4), run_time=0.5)
        self.at("laminae")
        surf = lbl_right("surface", 22, GREY, f(-3.8, 0.7))
        self.play(FadeIn(C.ib4lbl), FadeIn(surf), run_time=0.5)
        self.at("numbered")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in C.lamlbl], lag_ratio=0.35), run_time=1.5)
        self.at("mouse lumbar")
        mtag = T("mouse lumbar cord", 22, GREY).move_to(f(-1.9, 0.6))
        self.play(FadeIn(mtag), run_time=0.4)
        # 70 / 30 bar
        bx = 5.2
        top, bot = 0.7, -2.6
        h = top - bot
        gbar = Rectangle(width=1.6, height=0.7 * h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                         fill_opacity=0.35).move_to([bx, bot + 0.35 * h, 0])
        rbar = Rectangle(width=1.6, height=0.3 * h, stroke_color=RED, stroke_width=3, fill_color=RED,
                         fill_opacity=0.35).move_to([bx, top - 0.15 * h, 0])
        gt = T("about 70%", 22, GREEN).move_to(gbar)
        rt = T("about 30%", 22, RED).move_to(rbar)
        gt2 = T("excitatory", 24, GREEN).move_to([bx, bot - 0.3, 0])
        rt2 = T("inhibitory", 24, RED).move_to([bx, top + 0.3, 0])
        hdr = VGroup(T("neurons in", 22, GREY), T("this zone", 22, GREY)).arrange(DOWN, buff=0.04).move_to([bx, 1.85, 0])
        self.at("this zone")
        self.play(FadeIn(hdr), run_time=0.4)
        self.at("excitatory")
        self.play(GrowFromEdge(gbar, DOWN), FadeIn(gt), FadeIn(gt2), FadeIn(M_["E"], scale=0.5),
                  FadeIn(M_["G2"], scale=0.5), run_time=0.9)
        self.at("inhibitory")
        self.play(GrowFromEdge(rbar, DOWN), FadeIn(rt), FadeIn(rt2), FadeIn(M_["I"], scale=0.5),
                  FadeIn(M_["J"], scale=0.5), run_time=0.9)
        self.at("postsynaptic")
        pl = T("PSDC neuron", 22, ORANGE).move_to(f(-0.1, -1.95))
        self.play(FadeIn(M_["P"], scale=0.5), FadeIn(pl), run_time=0.8)
        self.at("excitation")
        a1 = link(*R["A"], *R["E"], "exc")
        a2 = link(*R["E"], *R["P"], "exc")
        self.play(GrowArrow(a1), run_time=0.5)
        self.play(GrowArrow(a2), run_time=0.5)
        self.at("axon")
        up = T("to the gracile nucleus", 22, ORANGE).move_to([1.3, 3.05, 0])
        self.play(Create(Pax), run_time=1.5)
        self.play(FadeIn(up), run_time=0.4)
        send(self, [f(-0.32, -1.375), f(0.55, -1.375), f(0.55, 1.1)], n=3, run=1.6)
        self.finish()


class S04Inhibit(SpokenScene):
    """feedforward inhibition, presynaptic inhibition, then disrupting either enlarges the receptive field"""

    def construct(self):
        C = Cord(1.35, lc=(-1.15, -0.9), sc=(-1.24, -0.2))
        f, s = C.f, C.s
        R, M_ = circuit(C)
        H, D, Pax = fibres(C)
        a1 = link(*R["A"], *R["E"], "exc")
        a2 = link(*R["E"], *R["P"], "exc")
        self.add(C.base, C.collbl, C.ib4, C.ib4lbl, C.lamlbl, D, H, Pax, *M_.values(), a1, a2)
        afl = lbl_right("afferent", 22, BLUE, f(-3.8, -2.05))
        pl = T("PSDC neuron", 22, ORANGE).move_to(f(-0.1, -1.95))
        self.add(afl, pl)
        self.at("Two kinds")
        self.play(Indicate(M_["P"], color=ORANGE, scale_factor=1.25), run_time=1.0)
        ff = T("feedforward", 24, RED).move_to([4.15, 2.5, 0], aligned_edge=LEFT)
        self.at("feed forward")
        self.play(FadeIn(ff), run_time=0.4)
        self.at("also excites")
        b1 = link(*R["A"], *R["I"], "exc")
        self.play(GrowArrow(b1), run_time=0.6)
        tagI = T("Rorβ", 22, TEXT).next_to(M_["I"], DOWN, buff=0.08)
        self.at("inhibits")
        b2 = link(*R["I"], *R["P"], "inh")
        self.play(Create(b2), FadeIn(tagI), run_time=0.7)
        self.wait(0.3)
        self.at("In presynaptic")
        ff2 = T("presynaptic", 24, RED).move_to([4.15, 1.9, 0], aligned_edge=LEFT)
        self.play(FadeIn(ff2), run_time=0.4)
        self.at("lands")
        c1 = link(*R["J"], *R["A"], "inh")
        tagJ = T("PVi", 22, TEXT).next_to(M_["J"], DOWN, buff=0.08)
        self.play(Create(c1), FadeIn(tagJ), run_time=0.7)
        self.at("turns down")
        self.play(M_["A"].animate.set_fill(BLUE, 0.3), run_time=0.7)
        # reset to a neutral state, then two separate knockouts, each with its own patch
        self.at("genetic")
        def patch(cy):
            skin = Ellipse(width=2.2, height=1.1, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                           fill_opacity=0.15).move_to([5.0, cy, 0])
            circ = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                          fill_opacity=0.25).move_to([5.0, cy, 0])
            return skin, circ
        skin1, circ1 = patch(-0.2)
        skin2, circ2 = patch(-2.0)
        rl = VGroup(T("PSDC", 22, ORANGE), T("receptive field", 22, ORANGE)).arrange(DOWN, buff=0.04).move_to([5.0, 0.95, 0])
        l1 = T("feedforward knockout", 22, TEXT).move_to([5.0, -1.0, 0])
        l2 = T("presynaptic knockout", 22, TEXT).move_to([5.0, -2.8, 0])
        self.play(M_["A"].animate.set_fill(BLUE, 0.9), FadeIn(skin1), FadeIn(circ1), FadeIn(skin2), FadeIn(circ2),
                  FadeIn(rl), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.at("either one")
        self.play(b2.animate.set_color(GREY), ff.animate.set_color(GREY), circ1.animate.scale(1.9), run_time=1.0)
        self.at("receptive")
        self.play(b2.animate.set_color(RED), ff.animate.set_color(RED), c1.animate.set_color(GREY),
                  ff2.animate.set_color(GREY), circ2.animate.scale(1.9), run_time=1.0)
        self.finish()


class S05Gap(SpokenScene):
    """the timing chart: direct 5.0 ms, indirect 9.5 ms, gap 4.5 ms (illustrative numbers)"""

    def construct(self):
        def X(ms):
            return -3.9 + 0.9 * ms
        top = T("illustrative numbers, not measurements", 26, TEXT).move_to([0.0, 3.3, 0])
        formula = M("t = L / v", 26, GREY).move_to([-5.4, -2.7, 0])
        axis = Line([X(0), -2.3, 0], [X(10), -2.3, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[Line([X(k), -2.3, 0], [X(k), -2.2, 0], color=GREY, stroke_width=3) for k in range(0, 11, 1)])
        tl = VGroup(*[T(str(k), 22, GREY).move_to([X(k), -2.65, 0]) for k in range(0, 11, 2)])
        msl = T("ms", 24, GREY).move_to([X(10) + 0.5, -2.3, 0])
        rl1 = T("direct", 26, BLUE).move_to([-5.3, 1.55, 0])
        rl2 = T("indirect", 26, ORANGE).move_to([-5.3, -0.1, 0])

        def seg(a, b, y, col, txt):
            r = Rectangle(width=0.9 * (b - a), height=0.7, stroke_color=col, stroke_width=2,
                          fill_color=col, fill_opacity=0.85).move_to([(X(a) + X(b)) / 2, y, 0])
            t = T(txt, 24, BG, weight=BOLD).move_to(r)
            return VGroup(r, t)

        self.add(top, formula, axis, ticks, tl, msl, rl1, rl2)
        self.at("direct route")
        d = seg(0, 5.0, 1.55, BLUE, "5.0 ms")
        dcap = T("0.08 m at 16 m/s", 22, BLUE).move_to([X(2.5), 0.9, 0])
        self.play(FadeIn(dcap), GrowFromEdge(d[0], LEFT), run_time=2.6, rate_func=linear)
        self.at("takes")
        self.play(FadeIn(d[1]), run_time=0.4)
        self.at("indirect route")
        self.wait(0.1)
        s1 = seg(0, 2.5, -0.1, BLUE, "2.5 ms")
        c1 = T("paw to cord", 22, BLUE).move_to([X(1.25), -0.72, 0])
        self.play(GrowFromEdge(s1[0], LEFT), FadeIn(s1[1]), FadeIn(c1), run_time=0.9)
        s2 = seg(2.5, 4.5, -0.1, GOLD, "2 ms")
        c2 = VGroup(T("2 synapses,", 22, GOLD), T("1 ms each (assumed)", 22, GOLD)).arrange(DOWN, buff=0.03)
        c2.move_to([X(3.5) + 0.05, -0.88, 0])
        self.at("Two synapses")
        self.play(GrowFromEdge(s2[0], LEFT), FadeIn(s2[1]), FadeIn(c2), run_time=0.9)
        s3 = seg(4.5, 9.5, -0.1, ORANGE, "5 ms")
        c3 = VGroup(T("PSDC axon,", 22, ORANGE), T("8 m/s (assumed)", 22, ORANGE)).arrange(DOWN, buff=0.03)
        c3.move_to([X(7.0), -0.88, 0])
        self.at("axon")
        self.play(GrowFromEdge(s3[0], LEFT), FadeIn(s3[1]), FadeIn(c3), run_time=1.0)
        self.at("total")
        e1 = Line([X(5.0), 1.9, 0], [X(5.0), 2.45, 0], color=YELLOW, stroke_width=4)
        e2 = Line([X(9.5), 0.35, 0], [X(9.5), 2.45, 0], color=YELLOW, stroke_width=4)
        tot = T("9.5 ms", 26, ORANGE).move_to([X(9.5) + 0.95, -0.1, 0])
        self.play(Create(e1), Create(e2), FadeIn(tot), run_time=0.9)
        br = DoubleArrow([X(5.0), 2.45, 0], [X(9.5), 2.45, 0], buff=0, color=YELLOW, stroke_width=5,
                         tip_length=0.2, max_tip_length_to_length_ratio=0.2)
        gl = T("4.5 ms later", 28, YELLOW, weight=BOLD).move_to([(X(5.0) + X(9.5)) / 2, 2.85, 0])
        self.at("later")
        self.play(GrowFromCenter(br), FadeIn(gl), run_time=0.9)
        self.finish()


class S06Meet(SpokenScene):
    """both copies converge on one thalamus-projecting neuron of the gracile nucleus; aligned receptive fields"""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.15, width=7.2, height=3.2, stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.12).move_to([1.3, 1.2, 0])
        bt = T("gracile nucleus", 26, PURPLE).move_to([-0.9, 2.4, 0])
        soma = Circle(radius=0.6, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15).move_to([1.6, 1.1, 0])
        sl = T("one thalamus-projecting neuron", 22, TEXT).move_to([1.6, 0.15, 0])
        out = arr([2.25, 1.1, 0], [5.6, 1.1, 0], TEXT, 4)
        ol = VGroup(T("to the", 22, TEXT), T("thalamus", 22, TEXT)).arrange(DOWN, buff=0.03).move_to([5.65, 1.6, 0])
        self.play(FadeIn(box), FadeIn(bt), FadeIn(soma), FadeIn(sl), run_time=1.0)
        self.play(GrowArrow(out), FadeIn(ol), run_time=0.8)
        # inputs
        d = bchip("direct input", BLUE, 26).move_to([-4.8, 2.0, 0])
        i = bchip("indirect input", ORANGE, 26).move_to([-4.8, 0.45, 0])
        da = arr(d.get_right() + RIGHT * 0.05, [1.0, 1.3, 0], BLUE, 5)
        ia = arr(i.get_right() + RIGHT * 0.05, [1.05, 0.9, 0], ORANGE, 5)
        self.at("direct and indirect")
        self.play(FadeIn(d), FadeIn(i), run_time=0.7)
        self.play(GrowArrow(da), GrowArrow(ia), run_time=0.9)
        # aligned receptive fields on the hindpaw skin
        self.at("aligned")
        skin = Ellipse(width=4.2, height=1.9, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                       fill_opacity=0.15).move_to([-1.2, -2.4, 0])
        rb = Circle(radius=0.75, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.15).move_to([-1.2, -2.4, 0])
        ro = DashedVMobject(Circle(radius=0.75, stroke_color=ORANGE, stroke_width=5).move_to([-1.2, -2.4, 0]),
                            num_dashes=18)
        rtext = VGroup(T("aligned receptive fields", 24, TEXT), T("on the hindpaw skin", 22, GREY)
                       ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([4.0, -2.4, 0])
        self.play(FadeIn(skin), FadeIn(rb), run_time=0.7)
        self.play(Create(ro), FadeIn(rtext), run_time=0.9)
        self.at("vibration")
        sub1 = T("vibration", 24, BLUE).next_to(d, DOWN, buff=0.12)
        self.play(FadeIn(sub1), run_time=0.5)
        self.at("sustained")
        sub2 = VGroup(T("sustained indentation,", 24, ORANGE), T("up to high forces", 24, ORANGE)
                      ).arrange(DOWN, buff=0.04).next_to(i, DOWN, buff=0.12)
        self.play(FadeIn(sub2), run_time=0.6)
        self.at("receives")
        both = T("a direct copy and a processed copy", 26, TEXT).move_to([1.3, 3.3, 0])
        self.play(FadeIn(both), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The brainstem receives a direct copy and a processed copy."
