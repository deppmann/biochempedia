"""Retrograde signal: a signal that must travel home  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = NGF, the final target's factor (and the target that makes it)
  ORANGE = NT-3, the intermediate target's factor (the blood vessel that makes it, a factor that acts only locally)
  BLUE   = TrkA, the receptor
  TEAL   = the carried signal: the signaling endosome, the vehicle, trafficking
  PINK   = dynein, the motor
  PURPLE = the nucleus, and the kinase in the diffusion scene
  GREEN  = supported / kept alive / switched on
  RED    = fails: too slow, switched off, not kept alive, blocked
  GOLD   = a phosphate badge
  GREY   = the neuron's outline, axes, labels, microtubule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"
SOLID = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.17)
TIP = 4.4          # x of the axon tip, in neuron units


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Neuron:
    """A neuron drawn across the frame: cell body (left), axon, tip (right). p(x, y) maps neuron units to the frame."""

    def __init__(self, cx=0.0, cy=0.0, sc=1.0, tube=1.7):
        self.cx, self.cy, self.sc, self.tube = cx, cy, sc, tube
        h = tube * sc
        body = Circle(radius=1.3 * sc).move_to(self.p(-4.95, 0))
        axon = RoundedRectangle(corner_radius=h / 2, width=(TIP + 4.9) * sc, height=h).move_to(self.p((TIP - 4.9) / 2, 0))
        self.cell = Union(body, axon).set_stroke(GREY, 3).set_fill(SOLID, 1)
        self.nuc = Circle(radius=0.6 * sc, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                          fill_opacity=0.35).move_to(self.p(-5.0, 0))
        self.group = VGroup(self.cell, self.nuc)

    def p(self, x, y=0.0):
        return np.array([self.cx + x * self.sc, self.cy + y * self.sc, 0.0])

    def block(self, color=YELLOW):
        return RoundedRectangle(corner_radius=0.15 * self.sc, width=0.9 * self.sc, height=3.6 * self.sc, stroke_color=color,
                                stroke_width=3, fill_color=color, fill_opacity=0.14).move_to(self.p(5.8, 0))

    def chamber(self, color):
        fill = RoundedRectangle(corner_radius=0.2 * self.sc, width=2.9 * self.sc, height=2.8 * self.sc, stroke_width=0,
                                fill_color=color, fill_opacity=0.12).move_to(self.p(4.85, 0))
        edge = DashedVMobject(RoundedRectangle(corner_radius=0.2 * self.sc, width=2.9 * self.sc, height=2.8 * self.sc,
                                               stroke_color=color, stroke_width=3), num_dashes=40).move_to(self.p(4.85, 0))
        return VGroup(fill, edge)


def rec_bar(pos, sc=1.0, angle=0.0, color=BLUE):
    return RoundedRectangle(corner_radius=0.09 * sc, width=0.26 * sc, height=0.7 * sc, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.85).move_to(pos).rotate(angle)


def dot(pos, color, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=1).move_to(pos)


def endo(pos, sc=1.0, dot_color=YELLOW):
    """Signaling endosome: a teal bubble holding the factor and the receptor. Returns VGroup(bubble, bar, dot)."""
    bubble = Circle(radius=0.45 * sc, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.18).move_to(pos)
    bar = rec_bar(pos + np.array([-0.12, 0, 0]) * sc, sc * 0.75)
    d = dot(pos + np.array([0.14, 0.02, 0]) * sc, dot_color, 0.12 * sc)
    return VGroup(bubble, bar, d)


def legs(pos, sc=1.0):
    """Two pink motor feet reaching from an endosome down to the microtubule."""
    out = VGroup()
    for s_ in (-1, 1):
        top = pos + np.array([0.12 * s_, -0.42, 0]) * sc
        bot = pos + np.array([0.36 * s_, -0.87, 0]) * sc
        out.add(Line(top, bot, color=PINK, stroke_width=6), dot(bot, PINK, 0.09 * sc))
    return out


def glide(mob, dx, T):
    """Move mob left by dx over T seconds of scene time, whatever else the scene is doing (an updater)."""
    st = {"moved": 0.0}
    v = dx / max(T, 0.3)

    def upd(m, dt):
        step = min(v * dt, dx - st["moved"])
        if step > 0:
            m.shift(LEFT * step)
            st["moved"] += step
    mob.add_updater(upd)


def barred(a, b, color=RED, w=6):
    """An arrow that is blocked halfway (a bar across it)."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    mid = (a + b) / 2
    return VGroup(Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.25),
                  Line(mid + perp * 0.3, mid - perp * 0.3, color=color, stroke_width=w + 3))


def tag(text, color, size=24, **kw):
    return T(text, size, color, **kw)


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


class S00Title(TitleCard):
    LESSON = "The Signal from the Target Travels Home"
    TITLE = "A Signal That Must Travel Home"


# ---------------------------------------------------------------------------------------------
class S01Gap(SpokenScene):
    """A neuron, NGF at the far tip, centimetres of axon, a nucleus that decides, question boxes."""

    def construct(self):
        n = Neuron(cy=-0.45)
        block = n.block()
        blk_lbl = tag("target", YELLOW, 26).move_to(n.p(5.8, -2.3))
        self.at("A sympathetic neuron", lead=0.0)
        self.play(Create(n.cell), FadeIn(n.nuc), run_time=1.4)
        lbl_body = tag("cell body", GREY, 26).move_to(n.p(-4.95, -1.8))
        self.play(FadeIn(lbl_body), run_time=0.4)

        self.at("survival factor")
        dots = VGroup(*[dot(n.p(5.05, y), YELLOW, 0.15) for y in (-0.6, 0.0, 0.6)])
        ngf = tag("NGF", YELLOW, 30, weight=BOLD).move_to(n.p(5.8, 2.45))
        self.play(FadeIn(dots, scale=0.6), FadeIn(ngf), run_time=0.6)
        self.at("target releases it")
        self.play(FadeIn(block), FadeIn(blk_lbl), run_time=0.5)
        self.play(*[d.animate.shift(LEFT * 0.12) for d in dots], run_time=0.3)

        self.at("can sit")
        a = n.p(-3.6, 2.15)
        b = n.p(TIP, 2.15)
        dim = DoubleArrow(a, b, buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        cm = tag("centimetres", GREY, 30).move_to(n.p(0.4, 2.75))
        self.play(GrowFromCenter(dim), FadeIn(cm), run_time=0.9)

        self.at("nucleus decides")
        nl = tag("nucleus", PURPLE, 28).move_to(n.p(-5.4, 2.2))
        self.play(FadeIn(nl), Indicate(n.nuc, color=PURPLE, scale_factor=1.25), run_time=0.9)

        self.at("how does the message")
        qs = VGroup()
        for x in (-2.0, 0.3, 2.6):
            box = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.9, stroke_color=TEXT, stroke_width=3,
                                   fill_color=BG, fill_opacity=1).move_to(n.p(x, 0))
            qs.add(VGroup(box, T("?", 40, TEXT, weight=BOLD).move_to(box)))
        self.play(LaggedStart(*[FadeIn(q, scale=0.7) for q in qs[::-1]], lag_ratio=0.35), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Drift(SpokenScene):
    """time = distance squared: one centimetre is about two months; a kinase loses its phosphate; a vehicle is needed."""

    def construct(self):
        ax = Axes(x_range=[0, 1.05, 1], y_range=[0, 1.05, 1], x_length=6.2, y_length=5.0,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 4,
                               "tip_length": 0.22}).move_to([-3.0, 0.1, 0])
        xl = tag("distance", GREY, 30).next_to(ax.x_axis, DOWN, buff=0.7).align_to(ax.x_axis, LEFT).shift(RIGHT * 2.2)
        yl = tag("time", GREY, 30).next_to(ax.y_axis, UP, buff=0.18)
        self.at("Could the signal", lead=0.0)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)

        self.at("square of the distance")
        curve = ax.plot(lambda x: x * x, x_range=[0, 1], color=RED, stroke_width=6)
        self.play(Create(curve), run_time=2.2, rate_func=linear)

        self.at("soluble protein")
        end = ax.c2p(1, 1)
        vline = DashedLine(ax.c2p(1, 0), end, color=GREY, stroke_width=3)
        cm = tag("1 cm", TEXT, 30).next_to(ax.c2p(1, 0), DOWN, buff=0.3)
        self.play(Create(vline), FadeIn(cm), run_time=0.7)
        self.at("roughly two months")
        hline = DashedLine(end, ax.c2p(0, 1), color=GREY, stroke_width=3)
        mo = tag("roughly two months", RED, 30, weight=BOLD).next_to(hline, DOWN, buff=0.15).align_to(ax.c2p(0.05, 1), LEFT)
        pt = Dot(end, color=RED, radius=0.12)
        self.play(FadeIn(pt, scale=1.6), Create(hline), run_time=0.5)
        self.play(FadeIn(mo), run_time=0.4)

        self.at("phosphorylated kinase")
        kin = chip("kinase", PURPLE, 36).move_to([3.4, 2.1, 0])
        pb = pbadge(0.24).move_to(kin.get_corner(UR) + np.array([0.02, 0.02, 0]))
        self.play(FadeIn(kin), FadeIn(pb, scale=0.5), run_time=0.6)
        self.at("switched off")
        off = tag("switched off", RED, 30).next_to(kin, DOWN, buff=0.25)
        self.play(pb.animate.shift(UP * 0.9 + RIGHT * 0.5).set_opacity(0),
                  kin[0].animate.set_stroke(GREY).set_fill(GREY, 0.12), kin[1].animate.set_color(GREY),
                  FadeIn(off), run_time=0.9)

        self.at("needs a vehicle")
        veh = DashedVMobject(Circle(radius=0.85, stroke_color=TEAL, stroke_width=5), num_dashes=24).move_to([3.4, -0.55, 0])
        q = T("?", 52, TEAL, weight=BOLD).move_to(veh)
        vl = tag("a vehicle\nor relay", TEAL, 32).next_to(veh, DOWN, buff=0.25)
        self.play(FadeIn(veh, scale=0.6), FadeIn(q), FadeIn(vl), run_time=0.7)
        self.at("stay active")
        act = tag("active for hours", TEAL, 28).next_to(vl, DOWN, buff=0.25)
        self.play(FadeIn(act, shift=UP * 0.1), run_time=0.5)
        self.at("identity of the factor")
        fd = dot(veh.get_center(), YELLOW, 0.26)
        self.play(FadeOut(q), FadeIn(fd, scale=0.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Carry(SpokenScene):
    """NGF binds TrkA, the pair buds into a signaling endosome, dynein carries it along a microtubule to the cell body."""

    def construct(self):
        n = Neuron(cy=0.15)
        block = n.block()
        blk_lbl = tag("target", YELLOW, 26).move_to(n.p(5.8, -2.3))
        rec = rec_bar(n.p(TIP, 0), 1.2)
        dots = VGroup(*[dot(n.p(5.05, y), YELLOW, 0.15) for y in (-0.6, 0.0, 0.6)])
        self.add(n.cell, n.nuc, block, blk_lbl, rec, dots)
        self.at("binds its receptor", lead=0.3)
        ngf_l = tag("NGF", YELLOW, 30, weight=BOLD).move_to(n.p(5.8, 2.45))
        rec_l = tag("TrkA", BLUE, 30, weight=BOLD).move_to(n.p(TIP - 0.5, 1.6))
        d0 = dots[1]
        self.play(d0.animate.move_to(n.p(TIP + 0.34, 0)), FadeIn(ngf_l), FadeIn(rec_l), run_time=0.7)
        self.play(Indicate(rec, color=BLUE, scale_factor=1.3), run_time=0.5)

        self.at("pulled into the cell")
        pos = n.p(TIP - 1.0, 0.25)
        bubble = Circle(radius=0.45, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.18).move_to(pos)
        self.play(FadeOut(rec_l), FadeOut(ngf_l), FadeOut(dots[0]), FadeOut(dots[2]),
                  FadeIn(bubble, scale=0.5), run_time=0.5)
        bar_t = rec_bar(pos + np.array([-0.12, 0, 0]), 0.75)
        dot_t = dot(pos + np.array([0.14, 0.02, 0]), YELLOW, 0.12)
        self.play(Transform(rec, bar_t), Transform(d0, dot_t), run_time=0.8)
        ev = VGroup(bubble, rec, d0)
        self.remove(bubble, rec, d0)
        self.add(ev)
        self.at("signaling endosome")
        ev_l = chip("signaling endosome", TEAL, 28).move_to(n.p(2.4, -1.75))
        self.play(FadeIn(ev_l, shift=UP * 0.1), run_time=0.5)

        self.at("motor")
        lg = legs(pos)
        dyn = tag("dynein", PINK, 30, weight=BOLD).move_to(n.p(TIP - 1.0, 1.6))
        self.play(FadeIn(lg, shift=UP * 0.1), FadeIn(dyn), run_time=0.6)
        self.at("along microtubules")
        mt = Line(n.p(-4.5, -0.62), n.p(TIP - 0.45, -0.62), color=GREY, stroke_width=6)
        mt_l = tag("microtubule", GREY, 26).move_to(n.p(-1.0, 1.6))
        self.play(Create(mt), FadeIn(mt_l), run_time=0.8)
        self.at("toward the cell body")
        self.play(FadeOut(ev_l), FadeOut(dyn), run_time=0.3)
        mover = VGroup(ev, lg)
        self.add(mover)
        T_move = max(3.0, self.t_of("a few hours") - self.elapsed() + 0.5)
        glide(mover, (TIP - 1.0 - (-3.9)) * n.sc, T_move)

        self.at("each second")
        spd = tag("roughly 1 µm each second", TEXT, 30).move_to([0.0, -3.0, 0])
        self.play(FadeIn(spd), run_time=0.4)
        self.at("few")
        hrs = tag("1 cm takes a few hours", TEAL, 32, weight=BOLD).move_to([0.0, -3.0, 0])
        self.play(ReplacementTransform(spd, hrs), run_time=0.5)
        self.at("but not proven")
        fav = tag("favoured, not proven", GREY, 28).move_to([0.0, -3.5 + 0.05, 0]).shift(UP * 0.0)
        fav.move_to([0.0, -3.0, 0])
        self.play(FadeOut(hrs), FadeIn(fav, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Test(SpokenScene):
    """An axon grows along a vessel (NT-3) to a final target (NGF); both factors switch on TrkA; which keeps the neuron alive?"""

    def construct(self):
        def f(x):
            return -1.3 + 2.6 / (1 + np.exp(-1.2 * (x + 1.6)))

        body = Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([-5.1, -1.3, 0])
        nuc = Circle(radius=0.45, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to([-5.15, -1.3, 0])
        self.add(body, nuc)
        self.at("Now a test", lead=0.0)

        vessel = ParametricFunction(lambda t: np.array([t, f(t), 0]), t_range=[-3.9, 1.6], stroke_width=70,
                                    color=ORANGE, stroke_opacity=0.22)
        vessel.set_cap_style(CapStyleType.ROUND)
        axon = ParametricFunction(lambda t: np.array([t, f(t), 0]), t_range=[-4.1, 4.3], stroke_width=10, color=GREY)
        axon.set_cap_style(CapStyleType.ROUND)
        tipc = Circle(radius=0.24, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to([4.3, f(4.3), 0])

        self.at("axons grow out")
        self.play(Create(axon), run_time=1.5, rate_func=linear)
        self.add(tipc)
        self.at("blood vessels")
        vl = tag("blood vessel", ORANGE, 30).move_to([-3.1, 0.65, 0])
        self.play(FadeIn(vessel), FadeIn(vl), run_time=0.7)
        self.bring_to_front(axon, tipc)
        self.at("which make")
        nt = tag("NT-3", ORANGE, 34, weight=BOLD).move_to([0.9, -0.45, 0])
        nd = VGroup(*[dot([x, f(x) - 0.42, 0], ORANGE, 0.15) for x in (-1.2, -0.5, 0.2, 0.9)])
        self.play(FadeIn(nd, scale=0.5, lag_ratio=0.3), FadeIn(nt), run_time=0.9)

        self.at("final targets")
        blk = RoundedRectangle(corner_radius=0.15, width=0.9, height=2.9, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.14).move_to([5.8, f(4.3), 0])
        bl = tag("final\ntarget", YELLOW, 26, line_spacing=0.8).move_to([5.8, f(4.3) - 2.1, 0])
        self.play(FadeIn(blk), FadeIn(bl), run_time=0.6)
        self.at("targets make")
        ngf_l = tag("NGF", YELLOW, 34, weight=BOLD).move_to([5.8, f(4.3) + 2.0, 0])
        gd = VGroup(*[dot([5.1, f(4.3) + y, 0], YELLOW, 0.15) for y in (-0.55, 0.0, 0.55)])
        self.play(FadeIn(gd, scale=0.5, lag_ratio=0.3), FadeIn(ngf_l), run_time=0.7)

        self.at("Both factors")
        rows = VGroup()
        bars = []
        for i, col in enumerate((ORANGE, YELLOW)):
            y = -1.7 - 1.05 * i
            d = dot([1.7, y, 0], col, 0.2)
            ar = arr_simple([2.1, y, 0], [3.2, y, 0])
            bar = rec_bar([3.65, y, 0], 1.0)
            tl = tag("TrkA", BLUE, 30).move_to([4.6, y, 0])
            rows.add(VGroup(d, ar, bar, tl))
            bars.append(bar)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.4), run_time=1.0)
        self.at("switch on")
        rings = [Circle(radius=0.42, stroke_color=GREEN, stroke_width=5).move_to(b) for b in bars]
        self.play(*[Create(r) for r in rings], run_time=0.6)

        self.at("keeps the neuron alive")
        q = T("?", 96, TEXT, weight=BOLD).move_to([-5.1, 0.55, 0])
        ring = Circle(radius=1.2, stroke_color=TEXT, stroke_width=4).move_to(body)
        self.play(FadeIn(q, scale=0.5), Create(ring), run_time=0.9)
        self.finish()


def arr_simple(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.2)


# ---------------------------------------------------------------------------------------------
class S05Result(SpokenScene):
    """NT-3 and NGF on distal axons only: NT-3 grows the axon but not the cell body; NGF does both; only NGF's complex goes home."""

    def construct(self):
        sc = 0.85
        A = Neuron(cx=0.3, cy=1.45, sc=sc)
        B = Neuron(cx=0.3, cy=-2.0, sc=sc)
        chA, chB = A.chamber(ORANGE), B.chamber(YELLOW)
        hdA = chip("NT-3", ORANGE, 32).move_to(A.p(-4.95, 0) + UP * (1.3 * sc + 0.5))
        hdB = chip("NGF", YELLOW, 32).move_to(B.p(-4.95, 0) + UP * (1.3 * sc + 0.5))
        recA = rec_bar(A.p(TIP, 0), sc)
        recB = rec_bar(B.p(TIP, 0), sc)
        pts = ((5.1, 0.8), (5.7, 0.25), (5.1, -0.75), (5.8, -0.9))
        dA = VGroup(*[dot(A.p(x, y), ORANGE, 0.13) for x, y in pts])
        dB = VGroup(*[dot(B.p(x, y), YELLOW, 0.13) for x, y in pts])

        self.at("Give each factor", lead=0.0)
        self.play(FadeIn(A.group), FadeIn(B.group), run_time=0.8)
        self.at("distal axons")
        self.play(FadeIn(chA), FadeIn(chB), FadeIn(recA), FadeIn(recB), FadeIn(dA), FadeIn(dB), FadeIn(hdA), FadeIn(hdB),
                  run_time=0.9)
        self.bring_to_front(A.group, B.group, recA, recB)

        self.at("local growth")
        spA = VMobject(color=GREEN, stroke_width=8).set_points_smoothly([A.p(TIP + 0.15, 0), A.p(TIP + 0.7, 0.3), A.p(TIP + 1.2, 0.8)])
        glA = tag("axon grows", GREEN, 26).move_to(A.p(1.6, 1.35))
        self.play(Create(spA), FadeIn(glA), run_time=0.7)
        self.at("cell bodies")
        notA = tag("not kept alive", RED, 28, weight=BOLD).move_to(A.p(-2.2, 1.35))
        self.play(A.cell.animate.set_stroke(RED, 5), FadeIn(notA), run_time=0.6)

        self.at("supports both")
        spB = VMobject(color=GREEN, stroke_width=8).set_points_smoothly([B.p(TIP + 0.15, 0), B.p(TIP + 0.7, 0.3), B.p(TIP + 1.2, 0.8)])
        glB = tag("axon grows", GREEN, 26).move_to(B.p(1.6, 1.35))
        yesB = tag("kept alive", GREEN, 28, weight=BOLD).move_to(B.p(-1.2, -1.4))
        self.play(Create(spB), FadeIn(glB), B.cell.animate.set_stroke(GREEN, 5), FadeIn(yesB), run_time=0.8)

        self.at("trafficking")
        tr = tag("trafficking", TEAL, 32, weight=BOLD).move_to([0.3, -0.25, 0])
        self.play(FadeIn(tr, scale=0.8), run_time=0.5)
        self.at("carried back")
        eb = endo(B.p(TIP - 0.65, 0), sc * 1.2)
        self.play(FadeOut(recB), FadeOut(dB[0]), FadeIn(eb, scale=0.6), run_time=0.5)
        self.add(eb)
        T_move = max(2.8, self.t_of("are not") - self.elapsed() + 1.0)
        glide(eb, (TIP - 0.65 - (-3.9)) * sc, T_move)

        self.at("but complexes")
        dd = dot(A.p(TIP + 0.36, 0), ORANGE, 0.13)
        self.play(FadeOut(dA[0]), FadeIn(dd, scale=0.6), run_time=0.5)
        self.at("are not")
        bl = barred(A.p(TIP - 0.6, 0.0), A.p(TIP - 3.4, 0.0))
        self.play(Create(bl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """A carried signal reaches the nucleus; a local factor steers the tip but cannot select a neuron; the rule."""

    def construct(self):
        n = Neuron(cy=0.9)
        block = n.block()
        rec = rec_bar(n.p(TIP, 0), 1.2)
        yd = dot(n.p(TIP + 0.34, 0), YELLOW, 0.17)
        self.add(n.cell, n.nuc, block, rec, yd)
        self.at("So the factor", lead=0.0)
        pos = n.p(TIP - 1.0, 0.25)
        ev = endo(pos, 1.0)
        self.play(FadeOut(rec), FadeOut(yd), FadeIn(ev, scale=0.6), run_time=0.5)
        lg = legs(pos)
        mt = Line(n.p(-4.5, -0.62), n.p(TIP - 0.45, -0.62), color=GREY, stroke_width=6)
        self.play(FadeIn(mt), FadeIn(lg), run_time=0.3)
        mover = VGroup(ev, lg)
        self.add(mover)
        t_arr = max(3.0, self.t_of("nucleus") - self.elapsed() - 0.2)
        glide(mover, (TIP - 1.0 - (-3.9)), t_arr)
        self.at("neurons", lead=0.0)
        self.play(Indicate(n.nuc, color=PURPLE, scale_factor=1.3), run_time=0.7)

        self.at("not")
        self.play(FadeOut(mover), FadeOut(mt), run_time=0.4)
        rec2 = rec_bar(n.p(TIP, 0), 1.2)
        od = dot(n.p(TIP + 0.34, 0), ORANGE, 0.17)
        lf = tag("acts only locally", ORANGE, 28).move_to(n.p(2.2, -1.5))
        self.play(FadeIn(rec2), FadeIn(od, scale=0.6), FadeIn(lf), run_time=0.6)
        self.at("steer an axon")
        sp = VMobject(color=GREEN, stroke_width=8).set_points_smoothly([n.p(TIP + 0.15, 0.1), n.p(TIP + 0.6, 0.5), n.p(TIP + 1.0, 1.1)])
        sl = tag("steers the axon", GREEN, 28).move_to(n.p(2.0, 1.55))
        self.play(Create(sp), FadeIn(sl), run_time=0.7)
        self.at("this")
        bl = barred(n.p(TIP - 0.6, 0), n.p(-3.4, 0))
        self.play(Create(bl), run_time=0.8)

        self.at("Competition between")
        c1 = tag("competition for the final target depends on", TEXT, 30).move_to([0, -2.15, 0])
        self.play(FadeIn(c1), run_time=0.6)
        self.at("trafficking of the receptor")
        c2 = chip("receptor trafficking", TEAL, 32).move_to([-2.4, -3.0, 0])
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.at("not only on binding")
        c3 = chip("not only binding", GREY, 32).move_to([2.4, -3.0, 0])
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.6)

        self.at("rule")
        self.play(FadeOut(VGroup(c1, c2, c3)), run_time=0.5)
        r1 = T("The factor that decides survival", 36, TEXT, font=TITLE_FONT)
        r2 = T("is the one whose signal can travel", 36, TEAL, font=TITLE_FONT)
        rule = VGroup(r1, r2).arrange(DOWN, buff=0.2).move_to([0, -2.6, 0])
        self.at("signal can travel")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The factor that decides survival is the one whose signal can travel."
