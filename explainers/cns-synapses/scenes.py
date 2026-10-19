"""Synapses in the brain: sufficient in a dish is not required in the animal  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = neuroligin (the protein on the kidney cell, the dendrite-side partner)
  BLUE   = neurexin (the axon-side partner, and the soluble neurexin that caps neuroligin)
  TEAL   = synaptic vesicles
  GREEN  = working / normal / function and maturation
  RED    = blocked / impaired / died
  GREY   = cells, axon, de-emphasized outlines
  GOLD   = the rule to keep (used once, in the last scene)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---------------------------------------------------------------------------------------------
# geometry of the dish: an axon (top bar) crossing kidney cells (bottom blobs)
# ---------------------------------------------------------------------------------------------
AX_Y, AX_H = 1.05, 0.7
CELL_TOP, CELL_H = 0.1, 2.9
CELL_Y = CELL_TOP - CELL_H / 2
XS = [1.3, 2.5, 3.7, 4.9]                   # stub positions over the neuroligin cell (centred on x = 3.1)
LEFT_K = range(0, 6)
RIGHT_K = range(6, 12)
SC = [(-5.6 + 1.018 * k, AX_Y + (0.13 if k % 2 == 0 else -0.13)) for k in range(12)]   # scattered vesicles
SC3 = [(0.7, 1.05), (1.9, 0.93), (3.1, 1.17), (4.3, 0.93), (5.5, 1.05), (2.5, 1.2)]
CL = [(2.8, 0.92), (3.1, 0.92), (3.4, 0.92), (2.8, 1.18), (3.1, 1.18), (3.4, 1.18)]   # clustered vesicles


def cell(x, w=5.4):
    return RoundedRectangle(corner_radius=0.45, width=w, height=CELL_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.22).move_to([x, CELL_Y, 0])


def axon(x0=-6.3, x1=6.3):
    return RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=AX_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([(x0 + x1) / 2, AX_Y, 0])


def stub(x, color, yc, dx=0.0):
    return RoundedRectangle(corner_radius=0.07, width=0.3, height=0.3, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to([x + dx, yc, 0])


def stub_row(color, yc, xs=XS, dx=0.0):
    return VGroup(*[stub(x, color, yc, dx) for x in xs])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vdot(p):
    return Dot([p[0], p[1], 0], radius=0.12, color=TEAL)


def dashed_box(x, y, w=5.4, h=CELL_H, color=GREY):
    return DashedVMobject(RoundedRectangle(corner_radius=0.45, width=w, height=h, stroke_color=color, stroke_width=3),
                          num_dashes=60).move_to([x, y, 0])


def neuro_state():
    """cell + yellow stubs for the neuroligin cell at x = 3.1 and its labels."""
    c = cell(3.1)
    cl = T("kidney cell", 26, GREY).move_to([3.1, -2.3, 0])
    st = stub_row(YELLOW, 0.25)
    nl = T("neuroligin", 28, YELLOW).move_to([3.1, -0.8, 0])
    return c, cl, st, nl


class S00Title(TitleCard):
    LESSON = "Synapses in the brain"
    TITLE = "Sufficient in a dish, not required"


# ---------------------------------------------------------------------------------------------
class S01Kidney(SpokenScene):
    """A bare kidney cell gets neuroligin; an axon crosses it; the question marks pose the puzzle."""

    def construct(self):
        c, cl, st, nl = neuro_state()
        ax = axon()
        axl = T("axon", 26, GREY).move_to([-5.3, 1.8, 0])
        self.at("kidney cell")
        self.play(FadeIn(c, scale=0.95), FadeIn(cl), run_time=0.7)
        self.at("one neuronal protein")
        self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in st], lag_ratio=0.2), run_time=0.9)
        self.at("protein called")
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.5)
        self.at("axons that touch it")
        self.play(GrowFromEdge(ax, LEFT), FadeIn(axl), run_time=1.4)
        self.at("found a partner")
        self.play(Indicate(st, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("What do those axons do")
        q = T("?", 90, TEXT).move_to([3.1, 2.45, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.at("does the brain need")
        box = dashed_box(-3.1, CELL_Y)
        qm = T("?", 90, TEXT).move_to(box.get_center() + UP * 0.2)
        bl = T("in the brain", 26, GREY).move_to([-3.1, CELL_Y - 0.9, 0])
        self.play(Create(box), FadeIn(qm, scale=0.5), FadeIn(bl), run_time=0.9)
        self.at("what kind of synapse")
        self.play(Indicate(qm, color=TEXT, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cluster(SpokenScene):
    """Vesicles gather only over the neuroligin cell, are released and taken back."""

    def construct(self):
        c, cl, st, nl = neuro_state()
        ax = axon()
        axl = T("axon", 26, GREY).move_to([-5.3, 1.8, 0])
        c0 = cell(-3.1)
        c0l = T("other cell", 26, GREY).move_to([-3.1, -2.3, 0])
        self.add(c, cl, st, nl, ax, axl)
        self.at("Grow kidney cells")
        self.play(FadeIn(c0, scale=0.95), FadeIn(c0l), run_time=0.7)
        dots = [vdot(p) for p in SC]
        self.at("an axon crosses")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.08), run_time=1.0)
        self.at("a cell that makes")
        self.play(Indicate(st, color=YELLOW, scale_factor=1.2), run_time=0.7)
        vl = T("synaptic vesicles", 26, TEAL).move_to([-2.0, 1.85, 0])
        self.at("synaptic vesicles")
        self.play(FadeIn(vl), run_time=0.4)
        self.at("gather")
        self.play(*[dots[k].animate.move_to([CL[i][0], CL[i][1], 0]) for i, k in enumerate(RIGHT_K)], run_time=1.2)
        self.at("other cells")
        self.play(Indicate(c0, color=GREY, scale_factor=1.04), run_time=0.9)
        self.at("releases")
        bottom = [dots[RIGHT_K[i]] for i in range(3)]
        self.play(*[d.animate.shift(DOWN * 0.4) for d in bottom], run_time=0.8)
        self.at("takes them back")
        self.play(*[d.animate.shift(UP * 0.4) for d in bottom], run_time=0.8)
        self.at("working terminals")
        ring = RoundedRectangle(corner_radius=0.2, width=1.3, height=0.8, stroke_color=GREEN, stroke_width=4)
        ring.move_to([3.1, 1.05, 0])
        wt = T("working terminal", 26, GREEN).move_to([3.1, 1.85, 0])
        self.play(Create(ring), FadeIn(wt), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Block(SpokenScene):
    """Neurexin on the axon pairs with neuroligin; free neurexin caps neuroligin and the clusters go."""

    def construct(self):
        c, cl, st, nl = neuro_state()
        ax = axon()
        axl = T("axon", 26, GREY).move_to([-5.3, 1.8, 0])
        c0 = cell(-3.1)
        c0l = T("other cell", 26, GREY).move_to([-3.1, -2.3, 0])
        dots = [vdot(SC[k]) if k in LEFT_K else vdot(CL[k - 6]) for k in range(12)]
        self.add(c, cl, st, nl, ax, axl, c0, c0l, *dots)
        ns = stub_row(BLUE, 0.55)
        nxl = T("neurexin", 28, BLUE).move_to([5.0, 1.85, 0])
        self.at("sit on the axon side")
        self.play(LaggedStart(*[GrowFromEdge(s, UP) for s in ns], lag_ratio=0.2), FadeIn(nxl), run_time=1.0)
        self.at("partners")
        self.play(Indicate(VGroup(ns, st), color=TEXT, scale_factor=1.15), run_time=0.9)
        free = VGroup(*[stub(0.0, BLUE, y) for y in (-2.3, -1.6, -0.9, -0.2)])
        fl = T("soluble neurexin", 28, BLUE).move_to([0, -3.2, 0])
        self.at("add soluble")
        self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in free], lag_ratio=0.15), FadeIn(fl), run_time=0.9)
        self.at("first so the axon's")
        self.play(*[free[i].animate.move_to([XS[i], 0.55, 0]) for i in range(4)],
                  ns.animate.shift(UP * 0.3).set_opacity(0.3), run_time=1.3)
        self.at("cannot reach")
        self.play(Indicate(free, color=BLUE, scale_factor=1.2), run_time=0.6)
        self.at("clusters are blocked")
        blk = chip("blocked", RED, size=28).move_to([3.1, 2.45, 0])
        self.play(*[dots[k].animate.move_to([SC3[i][0], SC3[i][1], 0]) for i, k in enumerate(RIGHT_K)], FadeIn(blk), run_time=1.0)
        self.at("bond between")
        self.play(Indicate(VGroup(free, st), color=TEXT, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Enough(SpokenScene):
    """The dish becomes 'sufficient'; a dashed box asks whether the animal needs it."""

    def construct(self):
        # mini dish, built about x = 0 then placed at the right (where the neuroligin cell was)
        c = cell(0.0)
        cl = T("kidney cell", 28, GREY).move_to([0, -2.3, 0])
        st = stub_row(YELLOW, 0.25, xs=[-1.8, -0.6, 0.6, 1.8])
        nl = T("neuroligin", 28, YELLOW).move_to([0, -0.8, 0])
        ax = axon(-3.0, 3.0)
        cluster = VGroup(*[vdot((p[0] - 3.1, p[1])) for p in CL])
        dish = VGroup(c, cl, st, nl, ax, cluster).shift([3.1, 0, 0])
        self.at("can do this")
        self.play(FadeIn(dish, scale=0.95), run_time=0.8)
        self.at("Call that sufficient")
        self.play(dish.animate.scale(0.9).move_to([-3.4, 0.3, 0]), run_time=1.0)
        suf = T("sufficient in a dish", 30, TEXT).move_to([-3.4, -2.35, 0])
        self.play(FadeIn(suf, shift=UP * 0.1), run_time=0.5)
        self.at("clean test of one protein")
        self.play(Indicate(st, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("what the brain depends on")
        box = dashed_box(3.4, 0.3, w=5.4, h=3.8)
        q = T("?", 100, TEXT).move_to(box.get_center())
        req = T("required in the animal?", 30, TEXT).move_to([3.4, -2.35, 0])
        self.play(Create(box), FadeIn(q, scale=0.5), FadeIn(req), run_time=1.0)
        self.at("genetic experiment")
        self.play(Indicate(q, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("take the protein away")
        row = stub_row(YELLOW, -0.9, xs=[2.2, 3.0, 3.8, 4.6])
        self.play(FadeIn(row), run_time=0.4)
        x = Cross(row, stroke_color=RED, stroke_width=6)
        self.play(Create(x), run_time=0.5)
        self.play(FadeOut(row), FadeOut(x), run_time=0.5)
        self.at("look at the synapses")
        self.play(Indicate(q, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bar(x, h, color, base=-1.9, w=1.1):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
    return r.move_to([x, base + h / 2, 0])


class S05Knockout(SpokenScene):
    """Bars: synapse number stays level, transmission drops - first neuroligin mice, then neurexin mice."""

    def construct(self):
        base = -1.9
        H = 2.8
        xl, xr = -3.3, 3.3
        head = T("Mice lacking neuroligins 1, 2 and 3 (brainstem)", 32, TEXT).move_to([0, 3.2, 0])
        axes = VGroup(Line([xl - 1.7, base, 0], [xl + 1.7, base, 0], color=GREY, stroke_width=3),
                      Line([xr - 1.7, base, 0], [xr + 1.7, base, 0], color=GREY, stroke_width=3))
        t1 = T("synapse number", 28, TEXT).move_to([xl, 1.35, 0])
        t2 = T("transmission", 28, TEXT).move_to([xr, 1.35, 0])
        w1, w2 = bar(xl - 0.9, H, GREY), bar(xr - 0.9, H, GREY)
        n1 = T("normal", 24, GREY).move_to([xl - 0.9, -2.4, 0])
        n2 = T("normal", 24, GREY).move_to([xr - 0.9, -2.4, 0])
        l1 = T("lacking", 24, TEXT).move_to([xl + 0.9, -2.4, 0])
        l2 = T("lacking", 24, TEXT).move_to([xr + 0.9, -2.4, 0])
        note = T("bar heights are schematic", 22, GREY).move_to([0, -3.2, 0])
        self.at("Mice lacking")
        self.play(FadeIn(head), Create(axes), FadeIn(t1), FadeIn(t2), FadeIn(note), run_time=0.8)
        self.play(GrowFromEdge(w1, DOWN), GrowFromEdge(w2, DOWN), FadeIn(n1), FadeIn(n2), run_time=0.8)
        self.at("normal number and structure")
        k1 = bar(xl + 0.9, H, GREEN)
        self.play(GrowFromEdge(k1, DOWN), FadeIn(l1), run_time=0.8)
        self.at("transmission was impaired")
        k2 = bar(xr + 0.9, 1.1, RED)
        self.play(GrowFromEdge(k2, DOWN), FadeIn(l2), run_time=0.8)
        self.at("failed breathing")
        died = chip("died from failed breathing", RED, size=26).move_to([0, 2.35, 0])
        self.play(FadeIn(died, shift=DOWN * 0.1), run_time=0.5)
        self.at("lacking all three")
        head2 = T("Mice lacking all three alpha-neurexins", 32, TEXT).move_to([0, 3.2, 0])
        self.play(ReplacementTransform(head, head2), FadeOut(k1), FadeOut(k2), FadeOut(died),
                  FadeOut(l1), FadeOut(l2), run_time=0.9)
        self.at("soon after birth")
        died2 = chip("died soon after birth", RED, size=26).move_to([0, 2.35, 0])
        self.play(FadeIn(died2, shift=DOWN * 0.1), run_time=0.5)
        self.at("close to normal")
        k3 = bar(xl + 0.9, 2.65, GREEN)
        self.play(GrowFromEdge(k3, DOWN), FadeIn(l1), run_time=0.8)
        self.at("transmitter poorly")
        k4 = bar(xr + 0.9, 1.1, RED)
        self.play(GrowFromEdge(k4, DOWN), FadeIn(l2), run_time=0.8)
        self.at("Synapses formed")
        self.play(Indicate(k3, color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("worked badly")
        self.play(Indicate(k4, color=RED, scale_factor=1.08), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Function, not formation; many organizers overlap; one in a dish tests only itself; the rule."""

    def construct(self):
        nx = chip("alpha-neurexin", BLUE, size=30)
        nl = chip("neuroligin", YELLOW, size=30)
        pair = VGroup(nx, nl).arrange(DOWN, buff=0.35).move_to([-5.0, 0, 0])
        head = T("synapse", 28, GREY).move_to([3.4, 2.5, 0])
        fn = chip("function and maturation", GREEN, size=30).move_to([3.4, 1.4, 0])
        fm = chip("forming most synapses", GREY, size=30).move_to([3.4, -1.4, 0])
        a1 = arr([-3.6, 0.3, 0], [fn.get_left()[0] - 0.05, 1.4, 0], GREEN)
        a2 = arr([-3.6, -0.3, 0], [fm.get_left()[0] - 0.05, -1.4, 0], GREY)
        self.play(FadeIn(pair, shift=RIGHT * 0.2), run_time=0.7)
        self.at("normal synapse function")
        self.play(FadeIn(head), GrowArrow(a1), FadeIn(fn), run_time=0.9)
        self.at("not for forming most")
        self.play(GrowArrow(a2), FadeIn(fm), run_time=0.7)
        x = Cross(Square(0.5), stroke_color=RED, stroke_width=7).move_to(a2.point_from_proportion(0.55))
        self.play(Create(x), run_time=0.5)
        self.at("organizers overlap")
        self.play(*[FadeOut(m) for m in (pair, head, fn, fm, a1, a2, x)], run_time=0.6)
        yc = Circle(radius=1.6, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.18).move_to([-1.2, 0.4, 0])
        gcs = [Circle(radius=1.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18).move_to(p)
               for p in ([1.3, 1.1, 0], [1.3, -0.3, 0], [0.1, -1.1, 0])]
        yl = T("neuroligin", 28, YELLOW).move_to([-1.6, 0.6, 0])
        gl = T("other organizers", 28, GREY).move_to([4.6, 0.3, 0])
        self.play(LaggedStart(FadeIn(yc, scale=0.8), *[FadeIn(g, scale=0.8) for g in gcs], lag_ratio=0.25),
                  FadeIn(yl), FadeIn(gl), run_time=1.3)
        self.at("with one organizer")
        self.play(*[g.animate.set_stroke(opacity=0.25).set_fill(opacity=0.05) for g in gcs],
                  yc.animate.set_fill(YELLOW, 0.45), FadeOut(gl), run_time=0.8)
        self.at("what that one can do")
        tc = T("tests only what that one can do", 30, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(tc, shift=UP * 0.1), run_time=0.6)
        self.at("Keep the rule")
        self.play(*[FadeOut(m) for m in (yc, *gcs, yl, tc)], run_time=0.6)
        self.at("sufficient in a dish")
        r1 = chip("sufficient in a dish", TEXT, size=40).move_to([0, 1.5, 0])
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at("not the same as")
        r2 = T("is not the same as", 36, GOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(r2), run_time=0.5)
        self.at("required in the animal")
        r3 = chip("required in the animal", TEXT, size=40).move_to([0, -1.1, 0])
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Sufficient in a dish is not required in the animal."
