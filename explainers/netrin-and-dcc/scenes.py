"""Netrin and DCC: one cue, two answers  (Biochemistrypedia explainer, developmental neuroscience)

COLOR MAP (one color per concept, whole video)
  YELLOW = netrin, the cue (source dot and its fading contours)
  BLUE   = the growth cone and its axon
  TEAL   = DCC receptor (cups on the growth cone surface)
  PURPLE = UNC5 receptor (cups)
  ORANGE = cyclic AMP inside the growth cone (dots)
  PINK   = antibody to DCC (caps that fill the DCC cups)
  GREEN  = attraction, the turn toward the source
  RED    = repulsion, the turn away; also a blocked signal
  GREY   = pipette, ghost arrows, outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BD0"

START = np.array([-1.0, -1.5, 0.0])
SRC = np.array([5.4, 0.4, 0.0])
R = 1.0  # growth cone radius


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def smooth(points):
    m = VMobject()
    m.set_points_smoothly([np.array(p, float) for p in points])
    return m


PATH_TOWARD = [START, [0.6, -1.25, 0], [2.2, -0.3, 0], [3.25, 0.3, 0]]
PATH_AWAY = [START, [-0.15, -1.1, 0], [-1.4, 0.1, 0], [-2.9, 0.9, 0], [-3.9, 1.3, 0]]
PATH_STRAIGHT = [START, [0.0, -1.5, 0], [1.0, -1.5, 0]]


def axon_in():
    return Line([-6.3, -1.5, 0], START, color=BLUE, stroke_width=11).set_z_index(-1)


def cups(center, angles, color, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        sw = 8 * max(scale, 0.6)
        out.add(Arc(radius=0.27 * scale, start_angle=phi + PI / 2, angle=PI, arc_center=c,
                    stroke_color=color, stroke_width=sw))
        out.add(Line(center + R * scale * u, center + (R + 0.18) * scale * u, color=color, stroke_width=sw * 0.8))
    return out


def caps(center, angles, scale=1.0):
    out = VGroup()
    for deg in angles:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        c = center + (R * scale + 0.45 * scale) * u
        out.add(Circle(radius=0.21 * scale, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                       fill_opacity=0.95).move_to(c))
    return out


DCC_A = [30, 70, 110]
UNC_A = [-30, -70, -110]


def body(center, scale=1.0):
    bg = Circle(radius=R * scale, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(center)
    disc = Circle(radius=R * scale, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25)
    disc.move_to(center)
    fil = VGroup()
    for deg in [0, 150, 180, 210]:
        phi = np.radians(deg)
        u = np.array([np.cos(phi), np.sin(phi), 0])
        fil.add(Line(center + R * scale * u, center + (R + 0.3) * scale * u, color=BLUE, stroke_width=4))
    return VGroup(bg, disc, fil)


DOT_OFFS = [(-0.3, 0.2), (0.0, 0.35), (0.25, 0.15), (-0.1, -0.1), (0.3, -0.2), (-0.35, -0.3), (0.05, -0.4)]


def dots(center, scale=1.0, live=True):
    g = VGroup()
    for dx, dy in DOT_OFFS:
        d = Circle(radius=0.095 * scale, stroke_color=ORANGE, stroke_width=2)
        if live:
            d.set_fill(ORANGE, 1)
        else:
            d.set_fill(ORANGE, 0).set_stroke(GREY, opacity=0.5)
        d.move_to(center + np.array([dx, dy, 0]) * 1.25 * scale)
        g.add(d)
    return g


def stage():
    """the netrin source and its fading contours"""
    arcs = VGroup()
    radii = [1.1, 2.3, 3.7, 5.2, 6.9, 8.7]
    ops = [0.95, 0.75, 0.58, 0.42, 0.3, 0.2]
    for r, o in zip(radii, ops):
        a = min(0.6, np.arcsin(min(1.0, 2.2 / r)))
        arc = Arc(radius=r, start_angle=PI - a, angle=2 * a, arc_center=SRC, stroke_color=YELLOW,
                  stroke_width=4, stroke_opacity=o).set_z_index(-2)
        arcs.add(arc)
    src = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to(SRC)
    lbl = T("netrin source", 24, YELLOW).move_to(SRC + DOWN * 0.8)
    return arcs, src, lbl


def pipette():
    p = Polygon([6.3, 2.5, 0], [6.05, 2.3, 0], [5.5, 0.62, 0], stroke_color=GREY, stroke_width=3,
                fill_color=GREY, fill_opacity=0.5)
    return p


def btext(text, size=26, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def banner(text, color):
    return T(text, 30, color, weight=BOLD).move_to([-1.6, 3.15, 0])


def run(self, mobs, path, t, rate=linear):
    """move a list of mobjects along a path while drawing the axon trail."""
    full = smooth(path).set_stroke(BLUE, 11).set_fill(opacity=0).set_z_index(-1)
    trail = full.copy()
    trail.pointwise_become_partial(full, 0, 0.001)
    self.add(trail)
    g = VGroup(*mobs)
    last = [np.array(path[0], float)]

    def step(m, a):
        a = max(a, 0.001)
        p = full.point_from_proportion(a)
        m.shift(p - last[0])
        last[0] = p
        trail.pointwise_become_partial(full, 0, a)

    self.play(UpdateFromAlphaFunc(g, step, rate_func=rate), run_time=t)
    return trail


class S00Title(TitleCard):
    LESSON = "Netrin and DCC"
    TITLE = "One cue, two answers"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        src = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95).move_to(SRC)
        nlbl = T("netrin", 28, YELLOW).move_to(SRC + DOWN * 0.8)
        cone_a = body(START)
        self.play(FadeIn(src), FadeIn(nlbl), FadeIn(cone_a), run_time=0.8)

        self.at("pull an axon toward")
        g_arr = Arrow(START + RIGHT * 1.2 + UP * 0.2, [3.7, 0.3, 0], buff=0, color=GREEN, stroke_width=8)
        g_lbl = T("pulled in", 28, GREEN).next_to(g_arr, DOWN, buff=0.15)
        self.play(GrowArrow(g_arr), FadeIn(g_lbl), run_time=0.8)

        self.at("push another axon away")
        cone_b = body(np.array([-3.4, 1.6, 0]))
        r_arr = Arrow([-4.4, 1.6, 0], [-6.0, 1.6, 0], buff=0, color=RED, stroke_width=8)
        r_lbl = T("pushed away", 28, RED).next_to(cone_b, DOWN, buff=0.35)
        self.play(FadeIn(cone_b), GrowArrow(r_arr), FadeIn(r_lbl), run_time=0.8)

        self.at("That protein is netrin")
        self.play(Indicate(src, color=YELLOW, scale_factor=1.5), Indicate(nlbl, color=YELLOW), run_time=0.9)

        self.at("Here is a growth cone")
        axon = axon_in()
        gc = T("growth cone", 28, BLUE).move_to(START + UP * 1.7)
        self.play(FadeOut(VGroup(g_arr, g_lbl, cone_b, r_arr, r_lbl)), run_time=0.5)
        self.play(Create(axon), FadeIn(gc), run_time=1.0)
        self.play(Indicate(cone_a, color=BLUE, scale_factor=1.15), run_time=0.8)

        self.at("released from a source")
        arcs, _, slbl = stage()
        self.play(Transform(nlbl, slbl), Indicate(src, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.at("thins out")
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.35), run_time=2.6)

        self.at("Which way will")
        up = DashedLine(START + RIGHT * 1.1 + UP * 0.25, START + RIGHT * 3.0 + UP * 1.5, color=GREY,
                        stroke_width=6, dash_length=0.15).add_tip(tip_length=0.28)
        dn = DashedLine(START + LEFT * 0.4 + UP * 1.0, START + LEFT * 2.4 + UP * 2.4, color=GREY,
                        stroke_width=6, dash_length=0.15).add_tip(tip_length=0.28)
        q1 = T("?", 52, YELLOW, weight=BOLD).move_to(START + RIGHT * 3.4 + UP * 1.8)
        q2 = T("?", 52, YELLOW, weight=BOLD).move_to(START + LEFT * 2.8 + UP * 2.7)
        self.play(FadeOut(gc), Create(up), Create(dn), FadeIn(q1), FadeIn(q2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def base_stage(self, with_axon=True):
    arcs, src, lbl = stage()
    self.add(arcs, src, lbl)
    axon = axon_in()
    self.add(axon)
    return arcs, src, lbl, axon


class S02Attract(SpokenScene):
    def construct(self):
        arcs, src, lbl, axon = base_stage(self)
        cone = body(START)
        self.add(cone)
        self.wait(0.8)

        self.at("receptors on its surface")
        dcc = cups(START, DCC_A, TEAL)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in dcc], lag_ratio=0.3), run_time=1.0)
        self.at("One receptor")
        tag = btext("DCC receptor", 28, TEAL).move_to(START + np.array([-0.3, 2.5, 0]))
        ptr = Arrow(tag.get_bottom() + DOWN * 0.05, START + np.array([0.5, 1.4, 0]), buff=0.05, color=TEAL,
                    stroke_width=5, tip_length=0.22)
        self.play(FadeIn(tag), GrowArrow(ptr), run_time=0.7)

        self.at("turns toward")
        self.play(FadeOut(VGroup(tag, ptr)), run_time=0.3)
        trail = run(self, [cone, dcc], PATH_TOWARD, 2.4, rate=smooth_rate)
        self.at("That is attraction")
        ban = banner("DCC: usually attracts", GREEN)
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.5)

        self.at("In the worm")
        w = bchip("worm: no DCC relative, fails mainly to go toward the cue", BLUE, size=24).move_to([-0.5, -3.05, 0])
        self.play(FadeIn(w, shift=UP * 0.15), run_time=0.7)
        self.finish()


smooth_rate = rate_functions.ease_in_out_sine


class S03Repel(SpokenScene):
    def construct(self):
        arcs, src, lbl, axon = base_stage(self)
        cone = body(START)
        dcc = cups(START, DCC_A, TEAL)
        self.add(cone, dcc)
        self.wait(0.05)

        self.at("Now add a second receptor")
        unc = cups(START, UNC_A, PURPLE)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in unc], lag_ratio=0.3), run_time=1.0)
        tag = btext("UNC5 receptor", 28, PURPLE).move_to(START + np.array([3.4, -1.25, 0]))
        ptr = Arrow(tag.get_left() + LEFT * 0.05, START + np.array([1.35, -0.8, 0]), buff=0.05, color=PURPLE,
                    stroke_width=5, tip_length=0.22)
        self.play(FadeIn(tag), GrowArrow(ptr), run_time=0.6)

        self.at("turns away from")
        self.play(FadeOut(VGroup(tag, ptr)), run_time=0.3)
        trail = run(self, [cone, dcc, unc], PATH_AWAY, 3.4, rate=smooth_rate)
        ban = banner("DCC + UNC5: usually repels", RED)
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.5)

        self.at("did not change")
        self.play(Indicate(lbl, color=YELLOW), Indicate(arcs[0], color=YELLOW), run_time=1.0)
        self.at("Only the receptors")
        self.play(Indicate(VGroup(dcc, unc), color=TEXT, scale_factor=1.25), run_time=1.0)

        self.at("In worms")
        w = bchip("worm touch neurons forced to make UNC-5: axons grow away", PURPLE, size=24).move_to([0.0, -3.05, 0])
        self.play(FadeIn(w, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S04Inside(SpokenScene):
    def construct(self):
        arcs, src, lbl, axon = base_stage(self)
        cone = body(START)
        dcc = cups(START, DCC_A, TEAL)
        self.add(cone, dcc)
        self.wait(0.8)

        self.at("interstate")
        ds = dots(START)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in ds], lag_ratio=0.12), run_time=1.0)
        self.play(Indicate(ds, color=ORANGE, scale_factor=1.3), run_time=0.8)

        self.at("frog spinal")
        ban = banner("frog spinal growth cone", BLUE)
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.6)

        self.at("fine pipette")
        pip = pipette()
        pl = T("pipette", 24, GREY).move_to([5.9, 2.85, 0])
        self.play(FadeIn(pip, shift=DOWN * 0.2), FadeIn(pl), run_time=0.7)
        self.play(Indicate(arcs[0], color=YELLOW, scale_factor=1.12), run_time=0.7)

        self.at("turned toward it")
        trail = run(self, [cone, dcc, ds], PATH_TOWARD, 3.0, rate=smooth_rate)

        self.at("cyclic")
        cl = btext("cyclic AMP (cAMP)", 28, ORANGE).move_to([3.0, -2.2, 0])
        cp = Arrow(cl.get_top() + UP * 0.05, [3.25, -0.2, 0], buff=0.1, color=ORANGE, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(cl), GrowArrow(cp), run_time=0.6)
        self.play(Indicate(ds, color=ORANGE, scale_factor=1.4), run_time=0.9)
        self.at("With that signal on")
        ban2 = banner("cAMP signal on: attraction", GREEN)
        self.play(Transform(ban, ban2), run_time=0.6)
        self.finish()


class S05Flip(SpokenScene):
    def construct(self):
        arcs, src, lbl, axon = base_stage(self)
        pip = pipette()
        pl = T("pipette", 24, GREY).move_to([5.9, 2.85, 0])
        self.add(pip, pl)
        cone = body(START)
        dcc = cups(START, DCC_A, TEAL)
        ds = dots(START)
        self.add(cone, dcc, ds)
        self.wait(0.8)

        self.at("block the signal")
        blk = bchip("cAMP signalling blocked", RED, size=26).move_to(START + np.array([0.0, 2.2, 0]))
        self.play(FadeIn(blk, shift=DOWN * 0.15),
                  *[d.animate.set_fill(ORANGE, 0).set_stroke(GREY, opacity=0.5) for d in ds], run_time=0.8)

        self.at("turn away")
        self.play(FadeOut(blk), run_time=0.25)
        trail = run(self, [cone, dcc, ds], PATH_AWAY, 2.0, rate=smooth_rate)
        ban = banner("cAMP blocked: repulsion", RED)
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.4)

        # ---- the antibody, with normal cAMP (lane A) and blocked cAMP (lane B) --------------
        self.at("An antibody to")
        yA, yB = -2.0, 1.1
        pa, pb = np.array([-1.0, yA, 0]), np.array([-1.0, yB, 0])
        axA = Line([-6.3, yA, 0], pa, color=BLUE, stroke_width=11).set_z_index(-1)
        axB = Line([-6.3, yB, 0], pb, color=BLUE, stroke_width=11).set_z_index(-1)
        cA, kA, dA, xA = body(pa), cups(pa, DCC_A, TEAL), dots(pa), caps(pa, DCC_A)
        cB, kB, dB, xB = body(pb), cups(pb, DCC_A, TEAL), dots(pb, live=False), caps(pb, DCC_A)
        tA = btext("normal cAMP", 26, ORANGE).move_to([-4.0, yA + 0.8, 0])
        tB = btext("cAMP blocked", 26, RED).move_to([-4.0, yB + 0.8, 0])
        self.play(FadeOut(VGroup(cone, dcc, ds, trail, ban, axon)), run_time=0.3)
        self.play(FadeIn(VGroup(axA, axB, cA, kA, dA, cB, kB, dB, tA, tB)), run_time=0.4)
        ab = btext("antibody to DCC on both", 28, PINK).move_to([-3.5, -0.45, 0])
        self.play(FadeIn(xA, scale=0.3), FadeIn(xB, scale=0.3), FadeIn(ab), run_time=0.6)

        self.at("stopped both turns")
        sA = run(self, [cA, kA, dA, xA], [pa, [0.0, yA, 0], [1.0, yA, 0]], 1.0)
        sB = run(self, [cB, kB, dB, xB], [pb, [0.0, yB, 0], [1.0, yB, 0]], 0.01)
        nA = btext("no turn", 28, TEXT).move_to([2.8, yA, 0])
        nB = btext("no turn", 28, TEXT).move_to([2.8, yB, 0])
        self.play(FadeIn(nA), FadeIn(nB), run_time=0.4)

        # ---- the lesson of it ---------------------------------------------------------------
        self.at("Both turns")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        ic = VGroup(body(np.array([-4.3, 0.0, 0]), 1.2), cups(np.array([-4.3, 0.0, 0]), DCC_A, TEAL, 1.2))
        recep = T("both turns need DCC", 30, TEAL).move_to([-4.3, -1.7, 0])
        self.play(FadeIn(ic), FadeIn(recep), run_time=0.5)
        self.at("Blocking cyclic")
        camp = bchip("cAMP level", ORANGE, size=40).move_to([-0.3, 0.0, 0])
        a1 = Arrow([-2.9, 0, 0], camp.get_left() + LEFT * 0.05, buff=0.05, color=GREY, stroke_width=6)
        self.play(GrowArrow(a1), FadeIn(camp), run_time=0.6)
        self.at("the direction")
        hi = Arrow(camp.get_right() + RIGHT * 0.1, [3.0, 1.5, 0], buff=0.05, color=GREEN, stroke_width=8)
        lo = Arrow(camp.get_right() + RIGHT * 0.1, [3.0, -1.5, 0], buff=0.05, color=RED, stroke_width=8)
        hl = T("signal on: toward", 28, GREEN).next_to(hi.get_end(), RIGHT, buff=0.15)
        ll = T("blocked: away", 28, RED).next_to(lo.get_end(), RIGHT, buff=0.15)
        self.play(GrowArrow(hi), GrowArrow(lo), FadeIn(hl), FadeIn(ll), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mini(center, receptors, live=None):
    s = 0.65
    parts = VGroup(body(center, s))
    if "d" in receptors:
        parts.add(cups(center, DCC_A, TEAL, s))
    if "u" in receptors:
        parts.add(cups(center, UNC_A, PURPLE, s))
    if live is not None:
        parts.add(dots(center, s, live=live))
    return parts


def row(cx, y, receptors, live, toward, label, color):
    ic = mini(np.array([cx, y, 0]), receptors, live)
    if toward:
        ar = Arrow([cx + 1.05, y, 0], [cx + 2.5, y, 0], buff=0, color=GREEN, stroke_width=8)
    else:
        ar = Arrow([cx - 1.05, y, 0], [cx - 2.5, y, 0], buff=0, color=RED, stroke_width=8)
    tx = T(label, 26, color).move_to([cx, y - 1.3, 0])
    return VGroup(ic, ar, tx)


class S06Rule(SpokenScene):
    def construct(self):
        self.wait(0.5)
        self.at("ask two questions")
        h1 = T("1  Which receptors?", 32, TEAL, weight=BOLD).move_to([-3.1, 3.1, 0])
        h2 = T("2  What cAMP level?", 32, ORANGE, weight=BOLD).move_to([3.1, 3.1, 0])
        div = Line([0, 3.4, 0], [0, -2.9, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(h1, shift=DOWN * 0.15), FadeIn(h2, shift=DOWN * 0.15), Create(div), run_time=0.9)

        self.at("usually attracts")
        r1 = row(-3.1, 1.65, "d", None, True, "DCC: usually toward netrin", GREEN)
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.8)
        self.at("add repulsion")
        r2 = row(-3.1, -1.15, "du", None, False, "DCC with UNC5: usually away", RED)
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.8)

        self.at("what is its")
        r3 = row(3.1, 1.65, "d", True, True, "cAMP on: toward (frog)", GREEN)
        self.play(FadeIn(r3, shift=UP * 0.15), run_time=0.8)
        self.at("lowering it")
        r4 = row(3.1, -1.15, "d", False, False, "cAMP low: away (frog)", RED)
        self.play(FadeIn(r4, shift=UP * 0.15), run_time=0.8)

        self.at("starting point")
        sp = bchip("a starting point: netrin has other receptors and partners", YELLOW, size=24).move_to([0, -3.2, 0])
        self.play(FadeIn(sp, shift=UP * 0.15), run_time=0.7)

        self.at("does not decide")
        self.play(FadeOut(sp), run_time=0.4)
        self.at("receptors and the interstate")
        self.play(Indicate(h1, color=TEAL, scale_factor=1.15), Indicate(h2, color=ORANGE, scale_factor=1.15),
                  run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Netrin does not decide the turn alone."
