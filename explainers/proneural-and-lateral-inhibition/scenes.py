"""Proneural genes and lateral inhibition: two equal cells, and one wins  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREEN  = proneural activity (bar) and the neural-precursor fate (cell rim)
  YELLOW = Delta (the knob on the membrane) and the "slightly more Delta" note
  BLUE   = Notch (the cup on the membrane) and the piece of Notch that enters the nucleus
  RED    = E(spl) repressor (bar) and inhibition arrows
  GREY   = cells, nuclei, bar tracks, labels, cells that are held back
  GOLD   = the question mark and the compare arrow
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, DEL, NOT, REP = GREEN, YELLOW, BLUE, RED
R, CY, H = 2.4, 0.25, 2.2
AX, BX = -2.85, 2.85
BASE = CY - 1.1
BW = 0.44


def bar(x, v, color):
    h = max(1e-3, v * H)
    return Rectangle(width=BW, height=h, stroke_width=0, fill_color=color, fill_opacity=0.92).move_to([x, BASE + h / 2, 0])


def P(cx, a):
    a = np.radians(a)
    return np.array([cx + R * np.cos(a), CY + R * np.sin(a), 0])


class Cell:
    """One cell: grey body, nucleus with two bars (proneural, repressor), a Delta knob and a Notch cup."""

    def __init__(self, cx, side, name):
        self.cx, self.side = cx, side
        self.pro, self.rep = ValueTracker(0), ValueTracker(0)
        self.delta, self.notch = ValueTracker(0), ValueTracker(0)
        self.bind, self.cupvis = ValueTracker(0), ValueTracker(0)
        self.body = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([cx, CY, 0])
        self.nuc = Circle(radius=1.75, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([cx, CY, 0]).set_stroke(opacity=0.6)
        self.label = T(name, 28, GREY).move_to([cx, CY + R + 0.5, 0])
        self.bxp, self.bxr = cx - 0.55, cx + 0.55
        self.tracks = VGroup(*[Rectangle(width=BW, height=H, stroke_color=GREY, stroke_width=2, fill_opacity=0)
                               .set_stroke(opacity=0.45).move_to([x, BASE + H / 2, 0]) for x in (self.bxp, self.bxr)])
        ka = 18 if side > 0 else 198
        ca = -18 if side > 0 else 162
        self.kp, self.cp = P(cx, ka), P(cx, ca)
        self.cupc = self.cp + np.array([side * 0.3, 0, 0])
        self.bindamt = 2 * (abs(self.kp[0]) - 0.3)
        self.pro_bar = always_redraw(lambda: bar(self.bxp, self.pro.get_value(), PRO))
        self.rep_bar = always_redraw(lambda: bar(self.bxr, self.rep.get_value(), REP))
        self.knob = always_redraw(self._knob)
        self.stalk = always_redraw(self._stalk)
        self.cup = always_redraw(self._cup)
        self.dyn = [self.pro_bar, self.rep_bar, self.stalk, self.knob, self.cup]
        self.static = VGroup(self.body, self.nuc, self.label, self.tracks)

    def knob_c(self):
        return self.kp + np.array([self.side * (0.3 + self.bindamt * self.bind.get_value()), 0, 0])

    def _knob(self):
        r = max(0.001, 0.32 * self.delta.get_value())
        return Circle(radius=r, stroke_color=DEL, stroke_width=3 if r > 0.01 else 0, fill_color=DEL, fill_opacity=0.9).move_to(self.knob_c())

    def _stalk(self):
        on = self.delta.get_value() > 0.01
        return Line(self.kp, self.knob_c(), color=GREY, stroke_width=4 if on else 0)

    def _cup(self):
        w = self.cupvis.get_value() * (3 + 10 * self.notch.get_value())
        st = PI / 2 if self.side > 0 else -PI / 2
        return Arc(radius=0.3, start_angle=st, angle=PI, arc_center=self.cupc, color=NOT, stroke_width=max(0.001, w))

    def setv(self, pro=None, rep=None, delta=None, notch=None, cupvis=None, bind=None):
        for k, v in dict(pro=pro, rep=rep, delta=delta, notch=notch, cupvis=cupvis, bind=bind).items():
            if v is not None:
                getattr(self, k).set_value(v)

    def to(self, **kw):
        return [getattr(self, k).animate.set_value(v) for k, v in kw.items()]

    def win(self):
        return [self.body.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.2), self.label.animate.set_color(GREEN)]

    def neutral(self):
        return [self.body.animate.set_stroke(GREY, 4, opacity=1).set_fill(GREY, 0.08), self.label.animate.set_color(GREY)]

    def lose(self):
        return [self.body.animate.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04), self.label.animate.set_color(GREY).set_opacity(0.6)]


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def pair():
    return Cell(AX, +1, "cell A"), Cell(BX, -1, "cell B")


def put(scene, *cells, dyn=True):
    for c in cells:
        scene.add(c.static)
        if dyn:
            scene.add(*c.dyn)


def legend():
    names = [("proneural", PRO), ("Delta", DEL), ("Notch", NOT), ("E(spl) repressor", REP)]
    cs = {n: chip(n, c, size=22, pad=0.16) for n, c in names}
    VGroup(*cs.values()).arrange(RIGHT, buff=0.35).move_to([0, -3.25, 0])
    return cs


def inh_arrows():
    up = inhib([-0.75, 2.25, 0], [0.75, 2.25, 0])
    dn = inhib([0.75, -1.7, 0], [-0.75, -1.7, 0])
    return VGroup(up, dn)


def simulate(a0, b0, n=330, tmax=5.5):
    f = lambda x: 1 / (1 + (x / 0.5) ** 4)
    a, b, dt, out = a0, b0, tmax / n, [(a0, b0)]
    for _ in range(n):
        a, b = a + dt * (f(b) - a), b + dt * (f(a) - b)
        out.append((a, b))
    return out


def run_sim(scene, A, B, arr, run_time):
    s = ValueTracker(0)
    holder = Mobject()

    def upd(_):
        a, b = arr[int(round(s.get_value() * (len(arr) - 1)))]
        A.setv(pro=a, delta=a)
        B.setv(pro=b, delta=b)
        A.setv(notch=b, rep=b)
        B.setv(notch=a, rep=a)
    holder.add_updater(upd)
    scene.add(holder)
    scene.play(s.animate.set_value(1), run_time=run_time, rate_func=linear)
    holder.remove_updater(upd)
    scene.remove(holder)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "Two equal cells, and one wins"


# ---------------------------------------------------------------------------------------------
CL = {"A": (-0.95, 0.0), "B": (0.95, 0.0), "C": (0, 1.6), "D": (-1.95, -1.5), "E": (1.95, -1.5)}


SC = 1.2


def cluster_cells():
    return {k: Circle(radius=0.85 * SC, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([x * SC, y * SC - 0.2, 0])
            for k, (x, y) in CL.items()}


class S01Tie(SpokenScene):
    def construct(self):
        cells = cluster_cells()
        group = VGroup(*cells.values())
        self.at("the fly embryo")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in group], lag_ratio=0.15), run_time=1.4)
        self.at("small groups")
        self.play(group.animate.set_stroke(TEXT, 5), rate_func=there_and_back, run_time=0.9)
        self.at("start out equal")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.08) for c in group], run_time=0.9)
        self.at("can become")
        self.play(*[c.animate.set_stroke(GREEN, 6) for c in group], run_time=0.7)
        self.at("only one")
        lab = chip("neural precursor", GREEN, size=24)
        lab.move_to([-4.7, 1.7, 0])
        arrow = arr_to(lab.get_right() + RIGHT * 0.05, cells["A"].get_left() + UP * 0.35 + LEFT * 0.0)
        others = [cells[k] for k in "BCDE"]
        self.play(cells["A"].animate.set_fill(GREEN, 0.3), *[c.animate.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04) for c in others],
                  FadeIn(lab, shift=RIGHT * 0.2), GrowArrow(arrow), run_time=0.9)
        self.at("break the tie")
        q = T("?", 120, GOLD, font=TITLE_FONT).move_to([4.7, 0.2, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("group becomes able")
        c1 = chip("1  able", GREEN, size=24, pad=0.14)
        c2 = chip("2  one cell wins", GREEN, size=24, pad=0.14)
        st = VGroup(c1, c2).arrange(DOWN, buff=0.3).move_to([4.7, 0.2, 0])
        # clear the question before the steps appear
        self.play(FadeOut(q), run_time=0.3)
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.at("one wins")
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


def arr_to(a, b, color=GREEN):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=5, tip_length=0.22)


# ---------------------------------------------------------------------------------------------
class S02Proneural(SpokenScene):
    def construct(self):
        cells = cluster_cells()
        group = VGroup(*cells.values())
        cells["A"].set_stroke(GREEN, 6).set_fill(GREEN, 0.3)
        for k in "BCDE":
            cells[k].set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04)
        chipx = chip("neural precursor", GREEN, size=24).move_to([-4.7, 1.7, 0])
        arw = arr_to(chipx.get_right() + RIGHT * 0.05, cells["A"].get_left() + UP * 0.35)
        self.add(group, chipx, arw)
        A, B = pair()
        lg = legend()
        self.at("in the cluster")
        self.play(FadeOut(chipx), FadeOut(arw), *[FadeOut(cells[k]) for k in "CDE"],
                  ReplacementTransform(cells["A"], A.body), ReplacementTransform(cells["B"], B.body),
                  run_time=1.2)
        self.play(FadeIn(A.label), FadeIn(B.label), FadeIn(A.nuc), FadeIn(B.nuc), FadeIn(A.tracks), FadeIn(B.tracks), run_time=0.6)
        self.add(*A.dyn, *B.dyn)
        A.body.set_stroke(GREY, 4, opacity=1).set_fill(GREY, 0.08)
        self.at("genes and code")
        self.play(FadeIn(lg["proneural"], shift=UP * 0.15), *A.to(pro=0.5), *B.to(pro=0.5), run_time=1.0)
        self.at("casting call")
        self.play(A.body.animate.set_stroke(GREEN, 5), B.body.animate.set_stroke(GREEN, 5), run_time=0.6)
        self.at("raise their own")
        loops = VGroup(*[CurvedArrow([x - 0.68, BASE + 1.1, 0], [x - 0.68, BASE + 0.3, 0], angle=PI * 0.9, color=GREEN, stroke_width=5, tip_length=0.2)
                         for x in (A.bxp, B.bxp)])
        self.play(Create(loops), *A.to(pro=0.7), *B.to(pro=0.7), run_time=1.1)
        self.at("also raise")
        self.play(*A.to(pro=0.5), *B.to(pro=0.5), FadeOut(loops), A.body.animate.set_stroke(GREY, 4), B.body.animate.set_stroke(GREY, 4), run_time=0.5)
        ga = arr_to([AX + 1.5, A.kp[1] - 0.2, 0], [A.kp[0] - 0.05, A.kp[1], 0])
        gb = arr_to([BX - 1.5, B.kp[1] + 0.2, 0], [B.kp[0] + 0.05, B.kp[1], 0])
        self.play(GrowArrow(ga), GrowArrow(gb), *A.to(delta=0.5), *B.to(delta=0.5), FadeIn(lg["Delta"], shift=UP * 0.15), run_time=1.0)
        self.at("protein in the cell membrane")
        self.play(A.delta.animate.set_value(0.9), B.delta.animate.set_value(0.9), rate_func=there_and_back, run_time=1.0)
        self.play(FadeOut(ga), FadeOut(gb), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def base_pair_after_s02():
    A, B = pair()
    A.setv(pro=0.5, delta=0.5)
    B.setv(pro=0.5, delta=0.5)
    return A, B


class S03Notch(SpokenScene):
    def construct(self):
        A, B = base_pair_after_s02()
        lg = legend()
        put(self, A, B)
        self.add(lg["proneural"], lg["Delta"])
        self.at("Delta on one cell")
        self.play(A.delta.animate.set_value(0.9), rate_func=there_and_back, run_time=0.9)
        self.at("binds Notch")
        self.play(B.cupvis.animate.set_value(1), FadeIn(lg["Notch"], shift=UP * 0.15), run_time=0.5)
        self.play(A.bind.animate.set_value(1), B.notch.animate.set_value(0.8), run_time=0.8)
        self.at("touches")
        self.play(B.notch.animate.set_value(1.0), rate_func=there_and_back, run_time=0.7)
        self.at("Two cuts")
        cuts = VGroup(*[Line(B.cupc + np.array([-0.25 + 0.0, dy, 0]), B.cupc + np.array([0.15, dy, 0]), color=TEXT, stroke_width=4)
                        .rotate(0.5, about_point=B.cupc + np.array([0, dy, 0])) for dy in (0.12, -0.12)])
        # two short slashes across the cup stalk
        cuts = VGroup(*[Line(B.cp + np.array([0.0 - 0.1, dy - 0.12, 0]), B.cp + np.array([0.2, dy + 0.12, 0]), color=TEXT, stroke_width=5) for dy in (0.05, 0.35)])
        self.play(Create(cuts), run_time=0.6)
        self.at("inner part")
        piece = Circle(radius=0.17, stroke_color=NOT, stroke_width=3, fill_color=NOT, fill_opacity=0.9).move_to(B.cp + RIGHT * 0.25)
        self.play(FadeOut(cuts), FadeIn(piece), run_time=0.4)
        self.play(piece.animate.move_to([BX - 1.95, CY + 0.75, 0]), run_time=0.9)
        self.at("nucleus")
        nl = T("nucleus", 22, GREY).move_to([BX, CY - 2.05, 0])
        self.play(FadeIn(nl), Indicate(B.nuc, color=TEXT, scale_factor=1.05), piece.animate.move_to([BX - 1.1, CY + 0.75, 0]), run_time=0.8)
        self.at("protein called")
        csl = chip("CSL", NOT, size=22, pad=0.12).move_to([BX + 0.12, CY + 1.4, 0])
        self.play(FadeIn(csl, shift=DOWN * 0.15), piece.animate.move_to(csl.get_left() + LEFT * 0.19), run_time=0.8)
        self.at("turns on")
        self.play(FadeOut(piece), FadeIn(lg["E(spl) repressor"], shift=UP * 0.15), *B.to(rep=0.75), run_time=1.0)
        self.at("encode repressors")
        self.play(B.rep.animate.set_value(0.9), rate_func=there_and_back, run_time=0.8)
        self.at("genes off")
        T_inh = inh_bars(B)
        self.play(Create(T_inh), *B.to(pro=0.15), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
def inh_bars(c):
    return inhib([c.bxr - 0.27, BASE + 0.62 * H, 0], [c.bxp + 0.27, BASE + 0.62 * H, 0])


class S04Loop(SpokenScene):
    def construct(self):
        A, B = pair()
        A.setv(pro=0.5, delta=0.5)
        B.setv(pro=0.15, delta=0.5, rep=0.75, notch=0.8, cupvis=1, bind=0)
        A.setv(bind=1)
        lg = legend()
        put(self, A, B)
        self.add(*lg.values())
        ia, ib = inh_bars(A), inh_bars(B)
        self.add(ib)
        self.at("Follow the loop")
        # reset to a balanced start, and bring in the second cup and bars in the same move
        self.play(*B.to(pro=0.5, rep=0.35, notch=0.35), *A.to(rep=0.35, notch=0.35, cupvis=1, bind=0), FadeIn(ia), run_time=1.2)
        self.at("More Delta on cell A")
        self.play(*A.to(delta=0.85), run_time=1.2)
        self.at("more Notch activity")
        self.play(*B.to(notch=0.85), run_time=1.0)
        self.at("makes more repressor")
        self.play(*B.to(rep=0.85), run_time=1.0)
        self.at("it has less")
        self.play(*B.to(pro=0.15), run_time=0.9)
        self.at("and less Delta")
        self.play(*B.to(delta=0.15), run_time=0.9)
        self.at("less Notch activity")
        self.play(*A.to(notch=0.1, rep=0.1), run_time=1.0)
        self.at("activity rises")
        self.play(*A.to(pro=0.85), run_time=1.0)
        self.at("pulled ahead")
        self.play(*A.to(delta=0.95), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tip(SpokenScene):
    def construct(self):
        A, B = pair()
        A.setv(pro=0.5, delta=0.5, rep=0.35, notch=0.35, cupvis=1)
        B.setv(pro=0.5, delta=0.5, rep=0.35, notch=0.35, cupvis=1)
        lg = legend()
        put(self, A, B)
        self.add(*lg.values())
        ia, ib = inh_bars(A), inh_bars(B)
        self.add(ia, ib)
        arrows = inh_arrows()
        self.at("Each cell inhibits")
        self.play(Create(arrows), run_time=1.0)
        self.at("positive feedback")
        pf = T("positive feedback", 28, GREEN).move_to([0, -2.65, 0])
        self.play(FadeIn(pf, shift=UP * 0.15), run_time=0.6)
        self.at("balanced pair")
        eq = M("=", 52, TEXT).move_to([0, 3.1, 0])
        self.play(FadeOut(pf), FadeIn(eq), run_time=0.5)
        self.wait(0.8)
        self.at("noise")
        note = T("A: slightly more Delta", 24, YELLOW).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(eq, note), *A.to(pro=0.54, delta=0.54), B.notch.animate.set_value(0.54), B.rep.animate.set_value(0.54), run_time=0.8)
        self.at("magnifies")
        sim = simulate(0.54, 0.50)
        t1 = self.t_of("neural precursor") - 0.4 - self.elapsed()
        run_sim(self, A, B, sim, max(2.0, t1))
        self.at("precursor")
        pre = chip("neural precursor", GREEN, size=22, pad=0.12).move_to([AX, -2.55, 0])
        self.play(FadeOut(note), *A.win(), *B.lose(), FadeIn(pre, shift=UP * 0.15), run_time=0.8)
        self.at("matter of chance")
        self.wait(0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        A, B = pair()
        a, b = simulate(0.54, 0.50)[-1]
        A.setv(pro=a, delta=a, rep=b, notch=b, cupvis=1)
        B.setv(pro=b, delta=b, rep=a, notch=a, cupvis=1)
        lg = legend()
        put(self, A, B)
        self.add(*lg.values())
        ia, ib = inh_bars(A), inh_bars(B)
        arrows = inh_arrows()
        self.add(ia, ib, arrows)
        A.body.set_stroke(GREEN, 6).set_fill(GREEN, 0.2)
        A.label.set_color(GREEN)
        B.body.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04)
        B.label.set_color(GREY).set_opacity(0.6)
        pre = chip("neural precursor", GREEN, size=22, pad=0.12).move_to([AX, -2.55, 0])
        self.add(pre)
        self.at("take Notch away")
        # remove Notch: cups, repressors, inhibition arrows and every earlier result go together
        cross = VGroup(*[Cross(Circle(radius=0.3).move_to(c), stroke_color=RED, stroke_width=7).scale(0.9) for c in (A.cupc, B.cupc)])
        self.play(FadeIn(cross), A.cupvis.animate.set_value(0), B.cupvis.animate.set_value(0), *A.to(rep=0), *B.to(rep=0),
                  FadeOut(arrows), FadeOut(ia), FadeOut(ib), FadeOut(pre), *A.neutral(), *B.neutral(), *A.to(pro=0.5, delta=0.5),
                  *B.to(pro=0.5, delta=0.5), run_time=1.3)
        self.at("no cell can be told")
        nu = T("not you", 30, RED).move_to([0, 3.1, 0])
        self.play(FadeIn(nu, scale=0.8), run_time=0.5)
        self.play(FadeOut(cross), run_time=0.3)
        self.at("keep their")
        self.play(FadeOut(nu), *A.to(pro=1.0, delta=1.0), *B.to(pro=1.0, delta=1.0), run_time=1.1)
        self.at("become neural")
        self.play(*A.win(), *[B.body.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.2), B.label.animate.set_color(GREEN).set_opacity(1)], run_time=0.8)
        self.at("too many")
        nb = VGroup(*[chip("neuroblast", GREEN, size=22, pad=0.12).move_to([x, -2.55, 0]) for x in (AX, BX)])
        self.play(FadeIn(nb, shift=UP * 0.15), run_time=0.6)
        self.at("what decides")
        # clear the no-Notch answer and bring the working loop back in one move
        cmp_ = DoubleArrow([-1.6, 3.1, 0], [1.6, 3.1, 0], color=GOLD, stroke_width=5, buff=0, tip_length=0.22)
        self.play(FadeOut(nb), *A.neutral(), *B.neutral(), A.cupvis.animate.set_value(1), B.cupvis.animate.set_value(1),
                  *A.to(pro=0.85, delta=0.85, rep=0.1, notch=0.1), *B.to(pro=0.15, delta=0.15, rep=0.85, notch=0.85),
                  FadeIn(ia), FadeIn(ib), FadeIn(arrows), run_time=1.2)
        self.at("compares")
        cl = T("compare", 24, GOLD).move_to([0, 3.5, 0])
        self.play(GrowFromCenter(cmp_), FadeIn(cl), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "In fly mosaics, fate followed relative Notch signaling."
