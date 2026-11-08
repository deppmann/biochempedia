"""Synapse elimination, chapter 1: Quieter Than Its Neighbour  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, shared by every chapter of this film series)
  BLUE   = motor axon A (the low-threshold input) and its terminal
  ORANGE = motor axon B (the middle-threshold input); the one that stays in this chapter
  PURPLE = motor axon C (the high-threshold input)
  PINK   = acetylcholine receptor sites on the muscle (the endplate strip)
  WHITE  = the stimulus: pointer, impulses travelling along axons, the electrode
  TEAL   = a lit motor unit and its twitch
  YELLOW = the question ("Predict", "?") and the guiding idea (the quieter input)
  RED    = lost, removed; the "neurons die" label
  GREEN  = the "neurons live, branches trimmed" label and the living cell body
  GREY   = muscle fiber, outlines (light grey for small labels)
  TEXT   = neutral things: motor neurons in the pool, measured share bars, plot baselines
  GOLD   = credit cards and the guiding-idea card frame
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B28CE8"
PINK = "#E58BC0"
STIM = "#FFFFFF"
UNIT = TEAL
LG = "#B9C0CC"          # light grey for small labels
AX = [BLUE, ORANGE, PURPLE]


def par(*a, **k):
    return AnimationGroup(*a, **k)


def snap(g):
    """Remember each part's own opacities so a group can be dimmed and restored."""
    return [(m.get_fill_opacity(), m.get_stroke_opacity(), m) for m in g.get_family() if m.has_points()]


def alpha_set(sn, f):
    for fo, so, m in sn:
        m.set_fill(opacity=fo * f)
        m.set_stroke(opacity=so * f)


def alpha_anims(sn, f):
    return [m.animate.set_fill(opacity=fo * f).set_stroke(opacity=so * f) for fo, so, m in sn]


# ----------------------------------------------------------------------------------------------
# the junction (one muscle fiber, three axons, one endplate)
# ----------------------------------------------------------------------------------------------
BIG = dict(fiber=(0, -2.95, 12.4, 1.5), ep=(0, -2.2, 2.9), beadx=[-1.0, 0.0, 1.0], beady=-1.6,
           tops=[(-4.6, 2.9), (0.0, 2.9), (4.6, 2.9)], bw=0.84)
SML = dict(fiber=(-3.2, -3.15, 6.3, 1.0), ep=(-3.2, -2.65, 2.3), beadx=[-3.95, -3.2, -2.45], beady=-2.2,
           tops=[(-3.55, 3.0), (-3.2, 3.0), (-2.85, 3.0)], bw=0.62)


def axon_curve(i, top, x, ybead, color=None, w=8):
    p0 = np.array([top[0], top[1], 0.0])
    p1 = np.array([x, ybead + 0.21, 0.0])
    dy = (p0[1] - p1[1]) * 0.45
    return CubicBezier(p0, p0 + DOWN * dy, p1 + UP * dy, p1, color=color or AX[i], stroke_width=w)


def junction(L):
    fx, fy, fw, fh = L["fiber"]
    fiber = RoundedRectangle(corner_radius=0.2, width=fw, height=fh, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.22).move_to([fx, fy, 0])
    ex, ey, ew = L["ep"]
    strip = RoundedRectangle(corner_radius=0.08, width=ew, height=0.26, stroke_color=PINK, stroke_width=3,
                             fill_color=PINK, fill_opacity=0.6).move_to([ex, ey, 0])
    axons, beads = [], []
    for i in range(3):
        x = L["beadx"][i]
        axons.append(axon_curve(i, L["tops"][i], x, L["beady"]))
        beads.append(RoundedRectangle(corner_radius=0.1, width=L["bw"], height=0.42, stroke_color=AX[i],
                                      stroke_width=3, fill_color=AX[i], fill_opacity=0.6).move_to([x, L["beady"], 0]))
    return dict(fiber=fiber, strip=strip, axons=axons, beads=beads, L=L)


def jgroup(J):
    return [J["fiber"], J["strip"], *J["axons"], *J["beads"]]


def release_dots(J, i, n=5):
    L = J["L"]
    x0 = L["beadx"][i]
    y0 = L["beady"] - 0.3
    ds = [Dot(radius=0.08, color=TEXT).move_to([x0 + (k - (n - 1) / 2) * 0.14, y0, 0]) for k in range(n)]
    return ds, L["ep"][1] + 0.16


def fire_dot(J, i):
    return Dot(radius=0.13, color=STIM).move_to(J["axons"][i].get_start())


# ----------------------------------------------------------------------------------------------
# the experiment layout: junction lower left, dial upper left, trace strip middle, plot right
# ----------------------------------------------------------------------------------------------
PX0, PW, PY0, PH = 2.1, 4.4, -2.7, 5.4
RMAX = 11.0
THR = [0.25, 0.5, 0.78]
AMP = [3, 4, 3]
TL = ["low", "middle", "high"]
DC = np.array([-5.5, 0.9, 0.0])
DR = 1.0


def sx(s):
    return PX0 + PW * s


def ry(R):
    return PY0 + PH * R / RMAX


def ang(s):
    return np.deg2rad(205 - 230 * s)


def dpt(s, r):
    a = ang(s)
    return DC + r * np.array([np.cos(a), np.sin(a), 0.0])


PIP_A = np.array([0.6, -0.7, 0.0])
PIP_B = np.array([-3.2, -2.95, 0.0])


def make_exp(tr):
    E = {}
    E["J"] = junction(SML)
    E["flab"] = T("muscle fiber", 26, LG).move_to([-5.15, -3.2, 0])
    E["sheath"] = RoundedRectangle(corner_radius=0.2, width=0.9, height=1.6, stroke_color=GREY,
                                   stroke_width=3).move_to([-3.2, 2.4, 0])
    E["nlab"] = T("nerve", 26, LG).move_to([-2.0, 2.4, 0])
    E["arrow"] = Arrow([-4.55, 2.7, 0], [-3.75, 2.7, 0], buff=0, color=STIM, stroke_width=5, tip_length=0.22,
                       max_tip_length_to_length_ratio=1)
    E["arc"] = Arc(radius=DR, start_angle=ang(1.0), angle=ang(0.0) - ang(1.0), arc_center=DC, color=GREY,
                   stroke_width=5)
    E["hub"] = Dot(DC, radius=0.09, color=STIM)
    E["ptr"] = always_redraw(lambda: Line(DC, dpt(tr.get_value(), 0.88), color=STIM, stroke_width=6))
    E["dlab"] = T("stimulus", 26, TEXT).move_to(DC + DOWN * 0.95)
    E["ticks"] = [Line(dpt(THR[i], 0.92), dpt(THR[i], 1.2), color=AX[i], stroke_width=7) for i in range(3)]
    E["tlabs"] = [T(TL[i], 26, AX[i]).move_to(dpt(THR[i], 1.48)) for i in range(3)]
    # A tapered glass electrode: its narrow tip penetrates below the endplate.
    axis = PIP_A - PIP_B
    normal = np.array([-axis[1], axis[0], 0.0]) / np.linalg.norm(axis)
    E["pip"] = Polygon(PIP_A + normal * 0.11, PIP_A - normal * 0.11, PIP_B,
                       stroke_color=STIM, stroke_width=3, fill_color=STIM, fill_opacity=0.2)
    E["tip"] = Dot(PIP_B, radius=0.09, color=STIM)
    E["ellab"] = VGroup(T("electrode", 26, TEXT).move_to([0.45, -1.5, 0]),
                         Line([-0.35, -1.6, 0], [-1.1, -1.85, 0], color=STIM, stroke_width=2))
    E["xa"] = Arrow([PX0, PY0, 0], [PX0 + PW + 0.3, PY0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2,
                    max_tip_length_to_length_ratio=1)
    E["ya"] = Arrow([PX0, PY0, 0], [PX0, PY0 + PH + 0.3, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2,
                    max_tip_length_to_length_ratio=1)
    E["xl"] = T("stimulus strength", 26, LG).move_to([PX0 + PW / 2, PY0 - 0.5, 0])
    E["yl"] = T("response size", 26, LG).rotate(PI / 2).move_to([PX0 - 0.55, PY0 + PH / 2, 0])
    E["schem"] = T("schematic, not data", 24, LG).move_to([PX0 + PW / 2 + 0.2, 3.5, 0])
    return E


def seg_line(c, a, b, w=6):
    return Line([sx(a[0]), ry(a[1]), 0], [sx(b[0]), ry(b[1]), 0], color=c, stroke_width=w)


def stair_segs(n=3):
    segs, s, R = [], 0.0, 0.0
    for i in range(n):
        segs.append(seg_line(TEXT, (s, R), (THR[i], R)))
        segs.append(seg_line(AX[i], (THR[i], R), (THR[i], R + AMP[i]), 8))
        s, R = THR[i], R + AMP[i]
    segs.append(seg_line(TEXT, (s, R), (1.0, R)))
    return segs


STRIP_X0, STRIP_W = -0.5, 1.8
STRIP_Y = [2.5, 0.85, -0.8]
STRIP_K = 0.15


def blip(x0, y0, w, h, color=STIM, sw=5):
    t = np.linspace(0, 1, 80)
    u = np.clip((t - 0.12) / 0.18, 0, None)
    f = u * np.exp(1 - u)
    pts = [np.array([x0 + w * ti, y0 + h * fi, 0.0]) for ti, fi in zip(t, f)]
    m = VMobject(color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def strip_trace(k, R, color=None):
    base = Line([STRIP_X0, STRIP_Y[k], 0], [STRIP_X0 + STRIP_W, STRIP_Y[k], 0], color=GREY, stroke_width=2)
    return base, blip(STRIP_X0, STRIP_Y[k], STRIP_W, STRIP_K * R, color or AX[k], 6)


PULSES = [(0.38, 3, [0]), (0.63, 7, [0, 1]), (0.9, 10, [0, 1, 2])]


def exp_state(scene, tr, ticks=True, plot=True, electrode_label=True):
    E = make_exp(tr)
    scene.add(*jgroup(E["J"]), E["flab"], E["pip"], E["tip"], E["sheath"], E["nlab"], E["arrow"],
              E["arc"], E["hub"], E["ptr"], E["dlab"])
    if ticks:
        scene.add(*E["ticks"], *E["tlabs"])
    if plot:
        scene.add(E["xa"], E["ya"], E["xl"], E["yl"])
    if electrode_label:
        scene.add(E["ellab"])
    return E


def fire_axon(scene, E, i, tr=None, to=None, rt=0.85):
    J = E["J"]
    d = fire_dot(J, i)
    scene.add(d)
    anims = [MoveAlongPath(d, J["axons"][i], run_time=0.55, rate_func=linear),
             Succession(Wait(0.55), Indicate(J["beads"][i], color=STIM, scale_factor=1.25, run_time=0.3))]
    if tr is not None:
        anims.append(tr.animate(run_time=rt, rate_func=linear).set_value(to))
    scene.play(par(*anims))
    scene.remove(d)


def flash_axon(scene, J, i, color=STIM, rt=0.5):
    scene.play(ShowPassingFlash(J["axons"][i].copy().set_stroke(color, 14), time_width=0.8), run_time=rt)


# ----------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Synapse Elimination: One Muscle Fiber, One Axon"
    TITLE = "Quieter Than Its Neighbour"


# ----------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        J = junction(BIG)
        flab = T("muscle fiber", 26, LG).move_to([-4.8, -2.95, 0])
        eplab = T("endplate", 26, PINK).move_to([2.75, -2.7, 0])
        tag = T("newborn rat", 32, TEXT).move_to([4.7, -1.2, 0])
        labs = [T("motor neuron", 26, AX[i]).move_to([BIG["tops"][i][0], 3.45, 0]) for i in range(3)]
        self.add(J["fiber"], J["strip"], flab, eplab, tag)
        # the axons grow in from the first word
        self.play(par(*[Succession(Wait(0.4 * i), Create(J["axons"][i], run_time=1.0), FadeIn(J["beads"][i], shift=DOWN * 0.1, run_time=0.2))
                        for i in range(3)],
                      *[Succession(Wait(0.4 * i + 0.5), FadeIn(labs[i], run_time=0.4)) for i in range(3)]))
        self.at("wired to")
        self.play(*[Indicate(J["beads"][i], color=STIM, scale_factor=1.2, run_time=0.5) for i in range(3)])
        self.at("works")
        self.play(*[b.animate.set_fill(STIM, 0.95) for b in J["beads"]], J["strip"].animate.set_fill(STIM, 0.8),
                  run_time=0.25)
        self.play(*[J["beads"][i].animate.set_fill(AX[i], 0.6) for i in range(3)],
                  J["strip"].animate.set_fill(PINK, 0.6), run_time=0.4)
        self.at("within weeks")
        tag2 = T("weeks later", 32, TEXT).move_to(tag)
        self.play(ReplacementTransform(tag, tag2), run_time=0.5)
        self.at("all but one")
        ghosts = []
        for i in (0, 2):
            g = DashedVMobject(J["axons"][i].copy(), num_dashes=22, dashed_ratio=0.6)
            g.set_color(RED).set_stroke(RED, opacity=0.95, width=7)
            ghosts.append(g)
        self.play(*[FadeOut(J["axons"][i]) for i in (0, 2)], *[FadeIn(g) for g in ghosts],
                  *[FadeOut(J["beads"][i]) for i in (0, 2)], *[FadeOut(labs[i]) for i in (0, 2)], run_time=0.8)
        self.at("decides which")
        q1 = T("?", 96, YELLOW, weight=BOLD).move_to(J["axons"][0].point_from_proportion(0.5))
        q2 = T("?", 96, YELLOW, weight=BOLD).move_to(J["axons"][2].point_from_proportion(0.5))
        self.play(FadeIn(q1, scale=0.6), FadeIn(q2, scale=0.6), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Work(SpokenScene):
    def construct(self):
        J = junction(BIG)
        flab = T("muscle fiber", 26, LG).move_to([-4.8, -2.95, 0])
        self.add(*jgroup(J), flab)
        d = fire_dot(J, 0)
        self.add(d)
        self.play(MoveAlongPath(d, J["axons"][0]), run_time=1.0, rate_func=linear)
        self.at("releases", lead=0.1)
        ds, yend = release_dots(J, 0)
        self.add(*ds)
        self.play(FadeOut(d), *[x.animate.set_y(yend) for x in ds], run_time=0.6)
        self.at("acetylcholine")
        ach = T("acetylcholine", 28, TEXT).move_to([-3.3, -1.55, 0])
        lead = Line([-2.15, -1.6, 0], [-1.45, -1.9, 0], color=TEXT, stroke_width=2)
        self.play(FadeIn(ach), Create(lead), run_time=0.4)
        self.play(*[x.animate.set_y(yend - 0.0).set_opacity(0.0) for x in ds], run_time=0.5)
        self.at("evokes")
        Js = junction(SML)
        flab2 = T("muscle fiber", 26, LG).move_to([-5.15, -3.2, 0])
        self.play(FadeOut(ach), FadeOut(lead), FadeOut(flab), run_time=0.2)
        pan = RoundedRectangle(corner_radius=0.2, width=5.9, height=6.3, stroke_color=GREY,
                               stroke_width=3).move_to([3.75, 0.1, 0])
        ph = T("voltage in the fiber", 28, TEXT).move_to([3.75, 2.75, 0])
        o = np.array([1.5, -2.25, 0.0])
        xa = Arrow(o, o + RIGHT * 5.0, buff=0, color=GREY, stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=1)
        ya = Arrow(o, o + UP * 4.3, buff=0, color=GREY, stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=1)
        xl = T("time", 26, LG).move_to([4.2, -2.75, 0])
        yl = T("voltage (mV)", 26, LG).rotate(PI / 2).move_to([1.05, 0.0, 0])
        self.play(ReplacementTransform(J["fiber"], Js["fiber"]), ReplacementTransform(J["strip"], Js["strip"]),
                  *[ReplacementTransform(J["axons"][i], Js["axons"][i]) for i in range(3)],
                  *[ReplacementTransform(J["beads"][i], Js["beads"][i]) for i in range(3)],
                  FadeIn(pan), FadeIn(ph), FadeIn(xa), FadeIn(ya), FadeIn(xl), FadeIn(yl), FadeIn(flab2), run_time=0.8)
        nocon = T("no contraction", 26, TEXT).move_to([-1.15, -1.55, 0])
        ach2 = T("acetylcholine", 26, TEXT).move_to([-5.5, -1.55, 0])
        blips = []
        amps = [2.3, 3.0, 2.3]
        for i in range(3):
            dd = fire_dot(Js, i)
            self.add(dd)
            extra = []
            if i == 0:
                extra = [FadeIn(ach2, run_time=0.4)]
            if i == 1:
                extra = [FadeIn(nocon, run_time=0.4)]
            self.play(MoveAlongPath(dd, Js["axons"][i]), run_time=0.25, rate_func=linear)
            bl = blip(o[0] + 0.15 + 1.5 * i, o[1], 1.4, amps[i], AX[i], 6)
            blips.append(bl)
            self.play(par(FadeOut(dd, run_time=0.15), Create(bl, run_time=0.4, rate_func=linear),
                          Indicate(Js["beads"][i], color=STIM, scale_factor=1.2, run_time=0.35), *extra))
        self.at("nothing is wrong")
        self.play(Indicate(VGroup(*Js["beads"]), color=GREEN, scale_factor=1.12), FadeOut(ach2), run_time=0.8)
        self.at("then they are removed")
        self.play(*[Js["axons"][i].animate.set_stroke(RED) for i in (0, 2)],
                  *[Js["beads"][i].animate.set_stroke(RED).set_fill(RED, 0.6) for i in (0, 2)], run_time=0.4)
        self.play(*[FadeOut(Js["axons"][i]) for i in (0, 2)], *[FadeOut(Js["beads"][i]) for i in (0, 2)],
                  FadeOut(blips[0]), FadeOut(blips[2]), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Count(SpokenScene):
    def construct(self):
        tr = ValueTracker(0.0)
        E = make_exp(tr)
        J = E["J"]
        self.add(J["fiber"], J["strip"], J["axons"][1], J["beads"][1], E["flab"], E["sheath"], E["nlab"])
        self.play(Create(J["axons"][0]), Create(J["axons"][2]), run_time=0.4)
        self.play(FadeIn(J["beads"][0]), FadeIn(J["beads"][2]), run_time=0.15)
        self.at("count them")
        self.play(*[Succession(Wait(0.25 * i), Indicate(J["beads"][i], color=STIM, scale_factor=1.25, run_time=0.3))
                    for i in range(3)])
        self.at("electrode")
        E["pip"].shift(UP * 0.85 + RIGHT * 0.3)
        E["tip"].shift(UP * 0.85 + RIGHT * 0.3)
        self.play(FadeIn(E["pip"]), FadeIn(E["tip"]), FadeIn(E["ellab"]),
                  *[FadeIn(E[k]) for k in ("xa", "ya", "xl", "yl")], run_time=0.4)
        self.at("inside one fiber")
        self.play(E["pip"].animate.shift(DOWN * 0.85 + LEFT * 0.3),
                  E["tip"].animate.shift(DOWN * 0.85 + LEFT * 0.3),
                  J["fiber"].animate.set_stroke(STIM), run_time=0.65)
        self.play(J["fiber"].animate.set_stroke(GREY), run_time=0.3)
        self.at("slowly")
        self.play(FadeIn(E["arc"]), FadeIn(E["hub"]), FadeIn(E["ptr"]), FadeIn(E["dlab"]), run_time=0.6)
        self.at("turn up")
        self.play(tr.animate(run_time=0.8, rate_func=linear).set_value(0.15))
        self.at("to its nerve")
        self.play(GrowArrow(E["arrow"]), Indicate(E["sheath"], color=STIM, scale_factor=1.08), run_time=0.7)
        self.finish()


class S04Thresh(SpokenScene):
    def construct(self):
        tr = ValueTracker(0.15)
        E = exp_state(self, tr, ticks=False)
        J = E["J"]
        self.add(E["arrow"])
        self.at("each axon")
        self.play(ShowPassingFlash(J["axons"][0].copy().set_stroke(STIM, 14), time_width=0.8), run_time=0.4)
        for i in (1, 2):
            flash_axon(self, J, i, rt=0.4)
        self.at("its own")
        for i in range(3):
            self.play(Create(E["ticks"][i]), FadeIn(E["tlabs"][i]), run_time=0.35)
            self.wait(0.05)
        self.at("fires")
        self.play(tr.animate(run_time=0.67, rate_func=linear).set_value(0.25))
        fire_axon(self, E, 0, tr, 0.355)
        self.play(tr.animate(run_time=0.97, rate_func=linear).set_value(0.5))
        fire_axon(self, E, 1, tr, 0.6)
        self.finish()


def predict_card():
    box = RoundedRectangle(corner_radius=0.2, width=4.1, height=4.4, stroke_color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.06).move_to([PX0 + PW / 2 + 0.15, 0.85, 0])
    pre = chip("Predict", YELLOW, size=30).move_to(box.get_top() + DOWN * 0.55)
    t1 = T("Three axons reach\nthis fiber.", 26, TEXT, line_spacing=0.8).move_to(box.get_center() + UP * 0.75)
    t2 = T("What does the\nresponse look like\nas the stimulus\nrises?", 26, YELLOW, line_spacing=0.8)
    t2.move_to(box.get_center() + DOWN * 0.8)
    return box, pre, t1, t2


QCENTER = np.array([PX0 + PW / 2 + 0.15, -2.0, 0.0])


class S05Predict(SpokenScene):
    def construct(self):
        tr = ValueTracker(0.6)
        E = exp_state(self, tr)
        J = E["J"]
        box, pre, t1, t2 = predict_card()
        self.play(tr.animate(run_time=0.5).set_value(0.0), FadeIn(box), FadeIn(pre, shift=DOWN * 0.15), run_time=0.5)
        self.at("three axons reach")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.4)
        for i in range(3):
            flash_axon(self, J, i)
        self.at("what does the response")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.at("as the stimulus")
        q = T("?", 90, YELLOW, weight=BOLD).move_to(QCENTER)
        self.play(FadeIn(q, scale=0.5), tr.animate(run_time=1.1, rate_func=linear).set_value(1.0))
        self.play(tr.animate(run_time=0.4).set_value(0.0))
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        tr = ValueTracker(0.0)
        E = exp_state(self, tr)
        box, pre, t1, t2 = predict_card()
        self.add(box, pre, t1, t2)
        tt = ValueTracker(5.0)
        ring_bg = Circle(radius=0.6, stroke_color=GREY, stroke_width=4).move_to(QCENTER)
        ring = always_redraw(lambda: Arc(radius=0.6, start_angle=PI / 2, angle=-2 * PI * max(tt.get_value(), 0.001) / 5.0,
                                         arc_center=QCENTER, color=YELLOW, stroke_width=8))
        nums = []
        for n in range(5, 0, -1):
            m = T(str(n), 48, YELLOW, weight=BOLD).move_to(QCENTER)
            m.add_updater(lambda mm, n=n: mm.set_opacity(1.0 if int(np.ceil(tt.get_value() - 1e-6)) == n else 0.0))
            nums.append(m)
        self.add(ring_bg, ring, *nums)
        self.play(tt.animate(run_time=4.9, rate_func=linear).set_value(0.0))
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        tr = ValueTracker(0.0)
        E = exp_state(self, tr)
        J = E["J"]
        box, pre, t1, t2 = predict_card()
        q = T("?", 90, YELLOW, weight=BOLD).move_to(QCENTER)
        self.add(box, pre, t1, t2, q)
        self.play(FadeOut(box), FadeOut(pre), FadeOut(t1), FadeOut(t2), FadeOut(q), run_time=0.4)

        def pulse(k):
            s, R, lit = PULSES[k]
            base, b = strip_trace(k, R)
            self.play(tr.animate(run_time=0.2).set_value(s))
            dot = Dot(radius=0.13, color=STIM).move_to([sx(s), ry(R), 0])
            self.play(par(*[J["beads"][i].animate(run_time=0.15).set_fill(STIM, 0.95) for i in lit],
                          FadeIn(base, run_time=0.15),
                          *([FadeIn(E["schem"], run_time=0.3)] if k == 0 else []),
                          Create(b, run_time=0.5, rate_func=linear),
                          FadeIn(dot, scale=2, run_time=0.3)))
            self.play(*[J["beads"][i].animate(run_time=0.25).set_fill(AX[i], 0.6) for i in lit])

        self.at("staircase")
        pulse(0)
        self.at("each threshold")
        pulse(1)
        self.at("adds one")
        pulse(2)
        self.at("three distinct steps")
        self.play(Succession(*[Create(sg, run_time=0.16, rate_func=linear) for sg in stair_segs(3)]))
        self.at("mean three axons")
        for i in range(3):
            flash_axon(self, J, i, AX[i], 0.45)
        self.finish()


def staircase_state(scene):
    tr = ValueTracker(0.9)
    E = exp_state(scene, tr)
    segs = stair_segs(3)
    scene.add(E["schem"], *segs)
    extras = []
    for k, (s, R, lit) in enumerate(PULSES):
        base, b = strip_trace(k, R)
        d = Dot(radius=0.13, color=STIM).move_to([sx(s), ry(R), 0])
        scene.add(base, b, d)
        extras += [base, b, d]
    return tr, E, segs, extras


class S08One(SpokenScene):
    def construct(self):
        tr, E, segs, extras = staircase_state(self)
        J = E["J"]
        dim = [J["axons"][1], J["axons"][2], J["beads"][1], J["beads"][2]]
        self.at("one axon", lead=-0.2)
        self.play(*[m.animate.set_opacity(0.15) for m in dim], *[FadeOut(m) for m in segs + extras],
                  FadeOut(E["schem"]), tr.animate(run_time=0.5).set_value(0.0), run_time=0.7)

        def live():
            s = tr.get_value()
            g = VGroup()
            if s > 0.01:
                g.add(seg_line(TEXT, (0, 0), (min(s, THR[0]), 0)))
            if s > THR[0]:
                g.add(seg_line(BLUE, (THR[0], 0), (THR[0], AMP[0]), 8), seg_line(TEXT, (THR[0], AMP[0]), (s, AMP[0])))
            return g
        self.add(always_redraw(live))
        self.at("gives one step")
        self.play(tr.animate(run_time=0.9, rate_func=linear).set_value(0.6))
        self.at("its own threshold")
        gl = DashedLine([sx(THR[0]), PY0, 0], [sx(THR[0]), ry(AMP[0]), 0], color=BLUE, stroke_width=4)
        self.play(Create(gl), Indicate(E["ticks"][0], color=STIM, scale_factor=1.6), run_time=0.8)
        self.at("one action")
        A = J["axons"][0]
        A2 = axon_curve(0, SML["tops"][0], SML["beadx"][0], -1.81)
        bx = [-4.4, -3.95, -3.5]
        stubs = VGroup(*[Line([-3.95, -1.6, 0], [x, -2.05, 0], color=BLUE, stroke_width=5) for x in bx])
        bout = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.3, height=0.38, stroke_color=BLUE,
                                         stroke_width=3, fill_color=BLUE, fill_opacity=0.6).move_to([x, -2.24, 0])
                        for x in bx])
        self.play(Transform(A, A2), FadeOut(J["beads"][0]), Create(stubs), FadeIn(bout), run_time=0.6)
        self.at("ordinarily")
        d = Dot(radius=0.13, color=STIM).move_to(A.get_start())
        self.add(d)
        self.play(MoveAlongPath(d, A), run_time=1.1, rate_func=linear)
        self.at("all its release")
        rs = T("release sites", 26, TEXT).move_to([-5.6, -1.3, 0])
        rl = Line([-4.75, -1.45, 0], [-4.45, -1.95, 0], color=TEXT, stroke_width=2)
        dd = [Dot(radius=0.11, color=STIM).move_to([-3.95, -1.6, 0]) for _ in bx]
        self.remove(d)
        self.add(*dd)
        self.play(*[x.animate.move_to([bx[k], -2.05, 0]) for k, x in enumerate(dd)], FadeIn(rs), Create(rl),
                  run_time=0.5, rate_func=linear)
        self.at("at once")
        base, b = strip_trace(0, 3)
        self.play(FadeOut(VGroup(*dd)), *[bout[k].animate.set_fill(STIM, 0.95) for k in range(3)],
                  FadeIn(base), Create(b, run_time=0.6, rate_func=linear), run_time=0.6)
        self.play(*[bout[k].animate.set_fill(BLUE, 0.6) for k in range(3)], run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S09Redfern(SpokenScene):
    def construct(self):
        yr = Text("1970", font=TITLE_FONT, font_size=130, color=GOLD).move_to([0, 1.65, 0])
        nm = Text("P. A. Redfern", font=TITLE_FONT, font_size=72, color=TEXT).move_to([0, -0.5, 0])
        sub = T("newborn rat diaphragm", 52, LG).move_to([0, -1.9, 0])
        rule = Line(LEFT * 2.8, RIGHT * 2.8, color=GOLD, stroke_width=4).move_to([0, 0.45, 0])
        self.play(FadeIn(yr, shift=UP * 0.15), GrowFromCenter(rule), run_time=0.5)
        self.at("did this", lead=0.5)
        self.play(FadeIn(nm, shift=UP * 0.15), run_time=0.5)
        self.at("newborn rat")
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
def mini_axes(x0, y0, w, h):
    xa = Arrow([x0, y0, 0], [x0 + w + 0.2, y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18,
               max_tip_length_to_length_ratio=1)
    ya = Arrow([x0, y0, 0], [x0, y0 + h + 0.2, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18,
               max_tip_length_to_length_ratio=1)
    return VGroup(xa, ya)


def mini_stair(x0, y0, w, unit, fracs, colors=None):
    pts = [[x0, y0, 0]]
    R = 0
    for f in fracs:
        pts.append([x0 + w * f, y0 + R, 0])
        R += unit
        pts.append([x0 + w * f, y0 + R, 0])
    pts.append([x0 + w, y0 + R, 0])
    m = VMobject(color=TEXT, stroke_width=6)
    m.set_points_as_corners(pts)
    return m


class S10Result(SpokenScene):
    def construct(self):
        y0, H, unit = -2.45, 4.3, 1.0
        h1 = T("at birth", 38, TEXT).move_to([-3.5, 2.9, 0])
        h2 = T("16 to 18 days", 38, TEXT).move_to([3.5, 2.9, 0])
        xs = [-6.15, -4.05, -1.95]
        ax_l = [mini_axes(x, y0, 1.15, H) for x in xs]
        ax_r = mini_axes(1.3, y0, 4.6, H)
        st = [mini_stair(xs[0], y0, 1.15, unit, [0.3, 0.65]),
              mini_stair(xs[1], y0, 1.15, unit, [0.2, 0.45, 0.75]),
              mini_stair(xs[2], y0, 1.15, unit, [0.15, 0.35, 0.55, 0.8])]
        one = mini_stair(1.3, y0, 4.6, unit, [0.4])
        cnt = [T(t, 26, LG).move_to([x + 0.575, 2.25, 0]) for x, t in zip(xs, ("2 steps", "3 steps", "4 steps"))]
        cnt_r = T("1 step", 26, LG).move_to([3.5, 2.25, 0])
        xl = VGroup(*[T("stimulus strength", 26, LG).move_to([x, -3.05, 0]) for x in (-3.5, 3.5)])
        yl = VGroup(*[T("response size", 22, LG).rotate(PI / 2).move_to([x, y0 + H / 2, 0]) for x in (-6.65, 0.65)])
        sch = T("schematic, not data", 24, LG).move_to([0, 3.6, 0])
        self.add(h1, h2, *ax_l, ax_r, xl, yl, sch)
        self.at("at birth", lead=0.0)
        self.play(Indicate(h1, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("two to four")
        for s, c in zip(st, cnt):
            self.play(Create(s), FadeIn(c), run_time=0.45, rate_func=linear)
        self.at("sixteen to eighteen")
        self.play(Indicate(h2, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("single steps")
        self.play(Create(one), FadeIn(cnt_r), run_time=0.7, rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S11Die(SpokenScene):
    def construct(self):
        J = junction(BIG)
        flab = T("muscle fiber", 26, LG).move_to([-4.8, -2.95, 0])
        band = RoundedRectangle(corner_radius=0.2, width=12.8, height=1.15, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.12).move_to([0, 3.2, 0])
        somas = [Circle(radius=0.42, stroke_color=AX[i], stroke_width=4, fill_color=AX[i], fill_opacity=0.3)
                 .move_to([BIG["tops"][i][0], 3.1, 0]) for i in range(3)]
        sc = T("spinal cord", 26, LG).move_to([2.35, 3.2, 0])
        self.add(J["fiber"], J["strip"], flab, J["axons"][1], J["beads"][1], band, *somas, sc)
        gh = []
        for i in (0, 2):
            g = DashedVMobject(J["axons"][i].copy().reverse_points(), num_dashes=24, dashed_ratio=0.55)
            g.set_color(AX[i])
            gh.append(g)
        self.at("extra", lead=0.0)
        qs = [T("?", 76, YELLOW, weight=BOLD).move_to(somas[i]) for i in (0, 2)]
        self.play(*[Succession(Create(g, run_time=0.9, rate_func=linear), FadeIn(q, scale=0.5, run_time=0.25))
                    for g, q in zip(gh, qs)])
        self.at("die")
        self.play(*[Indicate(q, color=YELLOW, scale_factor=1.3) for q in qs], run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
# the split diagram: two columns, one per hypothesis; each has a neuron counter and one unit's share
# ----------------------------------------------------------------------------------------------
CX = [-3.4, 3.4]
FRAME_W, FRAME_H = 6.4, 6.1
BAR_BASE, BAR_H = -1.45, 2.7
KEEP = list(range(16, 24))      # the 8 survivors: the bottom row of the 3 x 8 grid
DEAD = list(range(16))
LIVE_FRAC = 4.2 / 12.5
TOP_Y, BOT_Y = 3.5, -3.55


def dot_xy(c, k):
    row, col = divmod(k, 8)
    return [CX[c] - 1.35 + (col - 3.5) * 0.43, 1.3 - row * 0.5, 0]


def tick_x(c, j):
    return CX[c] - 1.35 + (j - 11.5) * 0.14


def make_split():
    S = {}
    S["frames"] = [RoundedRectangle(corner_radius=0.25, width=FRAME_W, height=FRAME_H, stroke_color=GREY, stroke_width=3)
                   .move_to([x, 0, 0]) for x in CX]
    S["nhead"] = [T("motor neurons: 24", 24, TEXT).move_to([CX[c] - 1.35, 2.1, 0]) for c in range(2)]
    S["shead"] = [T("unit's share", 24, TEXT).move_to([CX[c] + 1.55, 2.1, 0]) for c in range(2)]
    S["dots"] = [[Circle(radius=0.19, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.4)
                  .move_to(dot_xy(c, k)) for k in range(24)] for c in range(2)]
    S["ticks"] = [VGroup(*[Line([tick_x(c, j), -1.0, 0], [tick_x(c, j), -0.62, 0], color=LG, stroke_width=4) for j in range(24)])
                  for c in range(2)]
    S["flab"] = [T("muscle fibers", 26, LG).move_to([CX[c] - 1.35, -1.4, 0]) for c in range(2)]
    S["bars"] = [split_bar(c, BAR_H) for c in range(2)]
    S["base"] = [Line([CX[c] + 0.95, BAR_BASE, 0], [CX[c] + 2.15, BAR_BASE, 0], color=GREY, stroke_width=3) for c in range(2)]
    S["ref"] = [DashedLine([CX[c] + 0.95, BAR_BASE + BAR_H, 0], [CX[c] + 2.15, BAR_BASE + BAR_H, 0], color=LG, stroke_width=3)
                for c in range(2)]
    S["birth"] = [T("birth", 24, LG).move_to([CX[c] + 1.55, BAR_BASE + BAR_H + 0.4, 0]) for c in range(2)]
    S["die"] = chip("neurons die", RED, size=26, pad=0.15).move_to([CX[0], 2.62, 0])
    S["live"] = chip("neurons live, trim branches", GREEN, size=26, pad=0.15).move_to([CX[1], 2.62, 0])
    S["fan"] = VGroup(*[Line([dot_xy(0, 16 + m)[0], dot_xy(0, 16 + m)[1] - 0.19, 0], [tick_x(0, 3 * m + j), -0.62, 0],
                             color=TEXT, stroke_width=3) for m in range(8) for j in range(3)])
    return S


def split_bar(c, h):
    h = max(h, 0.02)
    return Rectangle(width=1.0, height=h, stroke_width=0, fill_color=TEXT, fill_opacity=0.65) \
        .move_to([CX[c] + 1.55, BAR_BASE + h / 2, 0])


def split_base(scene, S, c_parts=(0, 1), dots=True):
    for c in c_parts:
        scene.add(S["frames"][c], S["nhead"][c], S["shead"][c], S["ticks"][c], S["flab"][c], S["bars"][c],
                  S["base"][c], S["ref"][c], S["birth"][c])
        if dots:
            scene.add(*S["dots"][c])


def col_group(S, c, extra=()):
    parts = [S["frames"][c], S["nhead"][c], S["shead"][c], S["ticks"][c], S["flab"][c], S["bars"][c], S["base"][c],
             S["ref"][c], S["birth"][c], *S["dots"][c], *extra]
    return VGroup(*parts)


def banner_predict():
    pre = chip("Predict", YELLOW, size=28, pad=0.1)
    q = T("What happens to one unit's share?", 30, TEXT)
    g = VGroup(pre, q).arrange(RIGHT, buff=0.35).move_to([0, TOP_Y, 0])
    return g


def premise_tag():
    return chip("every fiber gives similar force", TEXT, size=26, pad=0.09, fill_opacity=0.24).move_to([0, BOT_Y, 0])


def die_result_state(scene, S, c=0):
    """The 'neurons die' column after the neurons are gone: 8 survivors in place, each reaching 3 fiber groups."""
    for k in DEAD:
        scene.remove(S["dots"][c][k])
    scene.add(S["fan"])
    S["nhead"][c].become(T("motor neurons: 8", 24, TEXT).move_to([CX[c] - 1.35, 2.1, 0]))


class S12Measures(SpokenScene):
    def construct(self):
        # two big gauge frames (same frames the split diagram will use later)
        fr = [RoundedRectangle(corner_radius=0.25, width=FRAME_W, height=FRAME_H, stroke_color=GREY, stroke_width=3)
              .move_to([x, 0, 0]) for x in CX]
        top = T("two measures", 32, LG).move_to([0, TOP_Y, 0])
        hl = T("motor neurons", 32, TEXT).move_to([CX[0], 2.2, 0])
        hr = T("one unit's share of the twitch", 28, TEXT).move_to([CX[1], 2.2, 0])
        dots = []
        for k in range(24):
            row, col = divmod(k, 8)
            dots.append(Circle(radius=0.24, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.4)
                        .move_to([CX[0] + (col - 3.5) * 0.62, 1.0 - row * 0.62, 0]))
        num = T("24", 130, TEXT, font=TITLE_FONT).move_to([CX[0], -1.5, 0])
        bar = Rectangle(width=1.8, height=3.7, stroke_width=0, fill_color=TEXT, fill_opacity=0.65).move_to([CX[1], -2.3 + 1.85, 0])
        base = Line([CX[1] - 1.4, -2.3, 0], [CX[1] + 1.4, -2.3, 0], color=GREY, stroke_width=3)
        ref = DashedLine([CX[1] - 1.4, 1.4, 0], [CX[1] + 1.4, 1.4, 0], color=LG, stroke_width=3)
        reflab = T("birth", 24, LG).move_to([CX[1] + 2.25, 1.4, 0])
        c1 = chip("1  count", TEXT, size=28, pad=0.08).move_to([CX[0], BOT_Y, 0])
        c2 = chip("2  measure", TEXT, size=28, pad=0.08).move_to([CX[1], BOT_Y, 0])
        ghost_bar = Rectangle(width=1.8, height=3.7, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(bar)
        for d in dots:
            d.set_fill(opacity=0.0).set_stroke(opacity=0.35)
        self.add(*dots)
        self.play(FadeIn(top), *[FadeIn(f) for f in fr], FadeIn(hl), FadeIn(hr), FadeIn(c1), FadeIn(c2), FadeIn(ghost_bar),
                  FadeIn(base), run_time=0.7)
        self.at("count the motor")
        self.play(FadeIn(num, scale=0.8), Indicate(c1, color=TEXT, scale_factor=1.1),
                  LaggedStart(*[d.animate.set_stroke(opacity=1).set_fill(opacity=0.4) for d in dots], lag_ratio=0.04), run_time=1.1)
        self.at("measure one")
        self.play(Indicate(c2, color=TEXT, scale_factor=1.1), GrowFromEdge(bar, DOWN), FadeOut(ghost_bar), run_time=0.9)
        self.play(FadeIn(ref), FadeIn(reflab), run_time=0.4)
        self.finish()


class S13Unit(SpokenScene):
    def construct(self):
        fy = [3.05 - 0.7 * k for k in range(9)]
        fibers = [RoundedRectangle(corner_radius=0.18, width=5.0, height=0.42, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.22).move_to([0.0, y, 0]) for y in fy]
        supplied = [1, 4, 7]
        soma = Circle(radius=0.5, stroke_color=TEXT, stroke_width=4, fill_color=TEXT,
                      fill_opacity=0.25).move_to([-5.7, 0.25, 0])
        trunk = Line([-5.2, 0.25, 0], [-3.2, 0.25, 0], color=TEXT, stroke_width=5)
        branches = [Line([-3.2, 0.25, 0], [-2.5, fy[k], 0], color=TEXT, stroke_width=5) for k in supplied]
        nlab = T("motor neuron", 26, TEXT).move_to([-5.7, -0.65, 0])
        ulab = T("motor unit", 34, UNIT, weight=BOLD).move_to([-4.4, 1.6, 0])
        other = T("grey fibers: other units", 26, LG).move_to([0.0, -3.4, 0])
        self.add(*fibers, soma, trunk, nlab)
        x0, y0, W, H = 3.75, -2.6, 2.7, 4.7
        xa = Arrow([x0, y0, 0], [x0 + W + 0.25, y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2,
                   max_tip_length_to_length_ratio=1)
        ya = Arrow([x0, y0, 0], [x0, y0 + H + 0.25, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2,
                   max_tip_length_to_length_ratio=1)
        yl = T("force", 26, LG).rotate(PI / 2).move_to([x0 - 0.5, y0 + H / 2, 0])
        xl = T("time", 26, LG).move_to([x0 + W / 2, y0 - 0.5, 0])
        pl = VGroup(xa, ya, xl, yl).set_opacity(0.25)
        self.add(pl)
        self.at("one motor neuron", lead=0.1)
        self.play(Indicate(soma, color=UNIT, scale_factor=1.3), run_time=0.6)
        self.at("all the fibers")
        for b in branches:
            self.play(Create(b), run_time=0.3)
        self.at("supplies")
        self.play(FadeIn(ulab), soma.animate.set_stroke(UNIT).set_fill(UNIT, 0.4),
                  trunk.animate.set_color(UNIT), *[b.animate.set_color(UNIT) for b in branches],
                  *[fibers[k].animate.set_stroke(UNIT).set_fill(UNIT, 0.3) for k in supplied], FadeIn(other),
                  run_time=0.6)
        self.at("twitch is")
        dots = [Dot(radius=0.13, color=STIM).move_to([-5.2, 0.25, 0]) for _ in range(3)]
        self.add(*dots)
        self.play(pl.animate.set_opacity(1.0),
                  *[MoveAlongPath(d, Line([-5.2, 0.25, 0], [-3.2, 0.25, 0]), run_time=0.4, rate_func=linear)
                    for d in dots], run_time=0.4)
        self.play(*[MoveAlongPath(d, branches[k], run_time=0.3, rate_func=linear) for k, d in enumerate(dots)])
        tw = blip(x0, y0, W, H * 0.9, UNIT, 7)
        self.play(FadeOut(VGroup(*dots)), Create(tw, run_time=1.0, rate_func=linear),
                  *[Indicate(fibers[k], color=UNIT, scale_factor=1.04, run_time=1.0) for k in supplied])
        self.at("to one impulse")
        self.play(Indicate(soma, color=STIM, scale_factor=1.25), run_time=0.7)
        self.finish()


class S13bPredict(SpokenScene):
    def construct(self):
        S = make_split()
        split_base(self, S)
        ban = banner_predict()
        self.add(ban, S["die"], S["live"])
        tag = premise_tag()
        self.at("every fiber")
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.6)
        self.at("what happens")
        self.play(*[Indicate(S["bars"][c], color=YELLOW, scale_factor=1.05) for c in range(2)], run_time=0.8)
        self.at("neurons die")
        self.play(Indicate(S["die"], color=RED, scale_factor=1.05), run_time=0.5)
        self.at("and if they live")
        self.play(Indicate(S["live"], color=GREEN, scale_factor=1.05), run_time=0.5)
        self.finish()


class S13cPause(NarratedScene):
    def construct(self):
        S = make_split()
        split_base(self, S)
        S["die"].become(chip("neurons die?", RED, size=26, pad=0.15).move_to([CX[0], 2.62, 0]))
        self.add(banner_predict(), premise_tag(), S["die"], S["live"])
        self.finish()


class S14Died(SpokenScene):
    def construct(self):
        S = make_split()
        split_base(self, S)
        ban = banner_predict()
        tag = premise_tag()
        self.add(ban, tag, S["die"], S["live"])
        right = col_group(S, 1, extra=[S["live"]])
        sr = snap(right)
        self.play(FadeOut(ban), *alpha_anims(sr, 0.28), run_time=0.3)
        self.at("neurons died", lead=0.1)
        gone = [S["dots"][0][k] for k in DEAD]
        self.play(*[d.animate.set_stroke(RED).set_fill(RED, 0.6) for d in gone], run_time=0.3)
        nh2 = T("motor neurons: 8", 24, TEXT).move_to(S["nhead"][0])
        self.play(*[FadeOut(d, scale=0.4) for d in gone], ReplacementTransform(S["nhead"][0], nh2), run_time=0.5)
        self.at("survivors")
        keep = [S["dots"][0][k] for k in KEEP]
        self.play(*[d.animate.set_stroke(STIM).set_fill(STIM, 0.5) for d in keep], run_time=0.4)
        self.at("keeps its")
        self.play(LaggedStart(*[Create(l) for l in S["fan"]], lag_ratio=0.03), run_time=1.2)
        self.at("so its share")
        self.play(Indicate(S["bars"][0], color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("stays the same")
        same = T("same", 28, TEXT, weight=BOLD).move_to([CX[0] + 2.65, BAR_BASE + BAR_H / 2, 0])
        self.play(FadeIn(same, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


def die_col_state(scene, S):
    scene.add(S["frames"][0], S["shead"][0], S["ticks"][0], S["flab"][0], S["bars"][0], S["base"][0], S["ref"][0],
              S["birth"][0], S["die"], S["fan"])
    nh = T("motor neurons: 8", 24, TEXT).move_to([CX[0] - 1.35, 2.1, 0])
    scene.add(nh)
    for k in KEEP:
        S["dots"][0][k].set_stroke(STIM).set_fill(STIM, 0.5)
        scene.add(S["dots"][0][k])
    same = T("same", 28, TEXT, weight=BOLD).move_to([CX[0] + 2.65, BAR_BASE + BAR_H / 2, 0])
    scene.add(same)
    return VGroup(S["frames"][0], S["shead"][0], S["ticks"][0], S["flab"][0], S["bars"][0], S["base"][0], S["ref"][0],
                  S["birth"][0], S["die"], S["fan"], nh, same, *[S["dots"][0][k] for k in KEEP])


def result_lines(c, day_text, color):
    l1 = T("birth: 3 ÷ 24 = 12.5%", 28, TEXT).move_to([CX[c], -2.0, 0])
    l2 = T(day_text, 28, color).move_to([CX[c], -2.5, 0])
    return l1, l2


class S15Kept(SpokenScene):
    def construct(self):
        S = make_split()
        left = die_col_state(self, S)
        sl = snap(left)
        alpha_set(sl, 0.28)
        split_base(self, S, c_parts=(1,))
        tag = premise_tag()
        self.add(S["live"], tag)
        self.at("the count holds")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.25) for d in S["dots"][1]], run_time=0.8)
        self.at("share falls", lead=0.0)
        low = split_bar(1, BAR_H * LIVE_FRAC)
        self.play(Transform(S["bars"][1], low), run_time=0.45)
        b1 = T("3 inputs per fiber at birth, 1 at day 14", 28, TEXT).move_to([0, 3.6, 0])
        b2 = T("share = inputs per fiber ÷ motor neurons", 24, LG).move_to([0, 3.25, 0])
        l1a, l2a = result_lines(0, "day 14: 1 ÷ 8 = 12.5%", RED)
        l1b, l2b = result_lines(1, "day 14: 1 ÷ 24 = about 4%", GREEN)
        self.play(FadeIn(b1, shift=DOWN * 0.1), FadeIn(b2, shift=DOWN * 0.1), *alpha_anims(sl, 0.6),
                  LaggedStart(FadeIn(l1b), FadeIn(l1a), FadeIn(l2b), FadeIn(l2a), lag_ratio=0.25), run_time=0.8)
        self.at("this assumes")
        t1 = chip("made-up numbers", LG, size=24, pad=0.1)
        t2 = chip("equal force per fiber", LG, size=24, pad=0.1)
        t3 = chip("fiber number steady", LG, size=24, pad=0.1)
        VGroup(t1, t2, t3).arrange(RIGHT, buff=0.3).move_to([0, BOT_Y, 0])
        self.play(FadeOut(tag), run_time=0.15)
        self.play(LaggedStart(*[FadeIn(t) for t in (t1, t2, t3)], lag_ratio=0.3), run_time=0.7)
        self.at("gain many")
        self.play(Indicate(t3, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S16Bjv(SpokenScene):
    def construct(self):
        yr = Text("1976", font=TITLE_FONT, font_size=120, color=GOLD).move_to([0, 2.45, 0])
        rule = Line(LEFT * 2.8, RIGHT * 2.8, color=GOLD, stroke_width=4).move_to([0, 1.4, 0])
        nms = [Text(t, font=TITLE_FONT, font_size=60, color=TEXT) for t in ("Brown", "Jansen", "Van Essen")]
        for i, n in enumerate(nms):
            n.move_to([0, 0.5 - 1.0 * i, 0])
        sub = T("rat soleus muscle", 52, LG).move_to([0, -2.9, 0])
        self.play(FadeIn(yr, shift=UP * 0.15), GrowFromCenter(rule), run_time=0.5)
        self.at("brown")
        self.play(FadeIn(nms[0], shift=UP * 0.12), run_time=0.4)
        self.wait(0.15)
        self.play(FadeIn(nms[1], shift=UP * 0.12), run_time=0.4)
        self.at("and van essen")
        self.play(FadeIn(nms[2], shift=UP * 0.12), run_time=0.4)
        self.at("rat soleus")
        self.play(FadeIn(sub, shift=UP * 0.12), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S17Res(SpokenScene):
    def construct(self):
        S = make_split()
        left = die_col_state(self, S)
        split_base(self, S, c_parts=(1,))
        self.add(S["live"])
        sl = snap(left)
        self.at("share of the twitch", lead=0.3)
        self.play(Indicate(S["bars"][1], color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("fell sharply")
        low = split_bar(1, BAR_H * LIVE_FRAC)
        res1 = T("share: fell sharply", 26, TEXT, weight=BOLD).move_to([CX[1], -2.05, 0])
        self.play(Transform(S["bars"][1], low), FadeIn(res1, shift=UP * 0.1), run_time=1.0)
        self.at("number of motor")
        res2 = T("neurons: no significant change", 26, TEXT, weight=BOLD).move_to([CX[1], -2.55, 0])
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.2) for d in S["dots"][1]], FadeIn(res2, shift=UP * 0.1),
                  run_time=0.8)
        self.at("did not change")
        self.play(*alpha_anims(sl, 0.25), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S18Branch(SpokenScene):
    def construct(self):
        fy = [2.75 - 1.1 * k for k in range(6)]
        fibers = [RoundedRectangle(corner_radius=0.2, width=3.2, height=0.5, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.22).move_to([4.9, y, 0]) for y in fy]
        soma = Circle(radius=0.65, stroke_color=TEXT, stroke_width=4, fill_color=TEXT,
                      fill_opacity=0.5).move_to([-5.2, 0.0, 0])
        trunk = Line([-4.55, 0.0, 0], [-2.0, 0.0, 0], color=TEXT, stroke_width=6)
        brs = [Line([-2.0, 0.0, 0], [3.3, y, 0], color=TEXT, stroke_width=5) for y in fy]
        nlab = T("motor neuron", 26, TEXT).move_to([-5.2, -1.1, 0])
        self.add(*fibers, soma, trunk, *brs, nlab)
        ring = Circle(radius=0.88, stroke_color=GREEN, stroke_width=6).move_to(soma)
        stay = T("cell body stays", 26, GREEN).move_to([-5.2, 1.35, 0])
        self.play(Create(ring), FadeIn(stay), run_time=0.8)
        lose = [0, 2, 3, 5]
        self.at("branches")
        self.play(*[brs[k].animate.set_color(RED).set_stroke(width=8) for k in lose], run_time=0.4)
        self.wait(0.4)
        shorts = [Line([-2.0, 0.0, 0], [-2.0 + 0.06 * 5.3, 0.06 * fy[k], 0], color=RED, stroke_width=5) for k in lose]
        self.play(*[Transform(brs[k], s) for k, s in zip(lose, shorts)], run_time=1.0)
        self.play(*[FadeOut(brs[k]) for k in lose], run_time=0.5)
        c1 = T("branch loss", 40, RED, weight=BOLD)
        c2 = T(", not neuron death", 40, TEXT)
        cap = VGroup(c1, c2).arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to([0, -3.3, 0])
        self.at("branch loss")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("not neuron")
        self.play(FadeIn(c2, shift=UP * 0.15), Indicate(ring, color=GREEN, scale_factor=1.15), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
def card_frame():
    box = RoundedRectangle(corner_radius=0.25, width=12.2, height=5.2, stroke_color=GOLD, stroke_width=3,
                           fill_color=GOLD, fill_opacity=0.05).move_to([0, -0.2, 0])
    head = T("THE IDEA WE WILL TEST", 26, GOLD).move_to([0, 3.2, 0])
    return box, head


def idea_lines(y1=1.45, y2=0.5, y3=-0.85, y4=-1.85):
    a = Text("A synapse is not removed", font=TITLE_FONT, font_size=46, color=TEXT).move_to([0, y1, 0])
    b = Text("just for being quiet.", font=TITLE_FONT, font_size=46, color=TEXT, t2c={"quiet": LG}).move_to([0, y2, 0])
    c = Text("What puts it at risk is being quieter", font=TITLE_FONT, font_size=44, color=TEXT,
             t2c={"quieter": YELLOW}).move_to([0, y3, 0])
    d = Text("than its neighbours at the same junction.", font=TITLE_FONT, font_size=44, color=TEXT,
             t2c={"than its neighbours": YELLOW}).move_to([0, y4, 0])
    return a, b, c, d


class S19Idea(SpokenScene):
    def construct(self):
        box, head = card_frame()
        a, b, c, d = idea_lines(0.35, -0.65)
        self.add(box, head)
        # Start revealing the idea immediately, including the introductory words.
        self.play(FadeIn(a, shift=UP * 0.12), run_time=0.35)
        self.at("just for")
        self.play(FadeIn(b, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S20Idea2(SpokenScene):
    def construct(self):
        box, head = card_frame()
        a, b, c, d = idea_lines(0.35, -0.65)
        self.add(box, head, a, b)
        self.at("what puts", lead=0.0)
        self.play(a.animate.move_to([0, 1.45, 0]), b.animate.move_to([0, 0.5, 0]), FadeIn(c, shift=UP * 0.12), run_time=0.7)
        self.at("than its")
        self.play(FadeIn(d, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S21Beat(NarratedScene):
    def construct(self):
        box, head = card_frame()
        self.add(box, head, *idea_lines())
        self.finish()


# ---- scope scenes: the card sits on top at nearly full size; two equal columns below -----------
CARD_S = 0.68
CARD_CY = 1.95
CY0 = -0.55          # column header height


def scope_card():
    box, head = card_frame()
    return VGroup(box, *idea_lines()).scale(CARD_S).move_to([0, CARD_CY, 0])


def scope_cols():
    lh = VGroup(T("which input goes", 40, GOLD, weight=BOLD), T("the idea", 28, LG)).arrange(DOWN, buff=0.1).move_to([-3.4, CY0, 0])
    rh = VGroup(T("how fast", 40, GOLD, weight=BOLD), T("overall activity", 28, LG)).arrange(DOWN, buff=0.1).move_to([3.4, CY0, 0])
    return lh, rh


def contest_mini():
    """Two inputs on one fiber, as in the first scene: the thinner one is the quieter."""
    fib = RoundedRectangle(corner_radius=0.15, width=5.4, height=0.7, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.22).move_to([-3.4, -3.4, 0])
    ax = []
    bd = []
    for i, x in ((0, -4.3), (1, -2.5)):
        a = Line([x, -1.55, 0], [x, -2.75, 0], color=AX[i], stroke_width=12 if i == 0 else 6)
        b = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.36, stroke_color=AX[i], stroke_width=3,
                             fill_color=AX[i], fill_opacity=0.6).move_to([x, -2.95, 0])
        ax.append(a)
        bd.append(b)
    return VGroup(fib, *ax, *bd), ax, bd


def right_rows():
    r1a = Arrow([2.1, -1.5, 0], [2.1, -2.5, 0], buff=0, color=TEXT, stroke_width=10, tip_length=0.35,
                max_tip_length_to_length_ratio=1)
    r1 = T("silence: slower", 38, TEXT).move_to([4.5, -2.0, 0])
    r2a = Arrow([2.1, -3.65, 0], [2.1, -2.75, 0], buff=0, color=TEXT, stroke_width=10, tip_length=0.35,
                max_tip_length_to_length_ratio=1)
    r2 = T("some stimulation\npatterns: faster", 38, TEXT, line_spacing=0.8).move_to([4.5, -3.15, 0])
    return VGroup(r1a, r1), VGroup(r2a, r2)


class S22Scope(SpokenScene):
    def construct(self):
        box, head = card_frame()
        g = VGroup(box, *idea_lines())
        self.add(g, head)
        lh, rh = scope_cols()
        mini, ax, bd = contest_mini()
        row1, row2 = right_rows()
        rh.set_opacity(0.25)
        self.play(FadeOut(head), g.animate.scale(CARD_S).move_to([0, CARD_CY, 0]), FadeIn(lh, shift=UP * 0.12),
                  FadeIn(rh), FadeIn(mini), run_time=0.8)
        self.at("which input")
        self.play(ax[1].animate.set_stroke(opacity=0.25), bd[1].animate.set_stroke(opacity=0.25).set_fill(opacity=0.12),
                  run_time=0.8)
        self.at("overall activity")
        self.play(rh.animate.set_opacity(1.0), run_time=0.6)
        self.at("silence slows")
        self.play(FadeIn(row1, shift=UP * 0.12), run_time=0.5)
        self.at("some patterns")
        self.play(FadeIn(row2, shift=UP * 0.12), run_time=0.6)
        self.finish()


def scope2_state(scene):
    g = scope_card()
    lh, rh = scope_cols()
    row1, row2 = right_rows()
    scene.add(g, lh, rh, row1, row2)
    return VGroup(g, lh, rh, row1, row2)


class S23Scope2(SpokenScene):
    def construct(self):
        g = scope_card()
        lh, rh = scope_cols()
        mini, ax, bd = contest_mini()
        ax[1].set_stroke(opacity=0.25)
        bd[1].set_stroke(opacity=0.25).set_fill(opacity=0.12)
        row1, row2 = right_rows()
        self.add(g, lh, rh, row1, row2, mini)
        n1 = T("quieter = weaker transmission", 32, YELLOW).move_to([-3.4, -1.75, 0])
        n1b = T("as the muscle sees it", 32, TEXT).move_to([-3.4, -2.35, 0])
        n2 = T("a bias, not a verdict", 40, GOLD, weight=BOLD).move_to([-3.4, -3.3, 0])
        self.at("quieter seems")
        self.play(FadeOut(mini), run_time=0.3)
        self.play(FadeIn(n1, shift=UP * 0.12), run_time=0.6)
        self.at("as the muscle")
        self.play(FadeIn(n1b, shift=UP * 0.12), run_time=0.5)
        self.at("and it is")
        self.play(FadeIn(n2, shift=UP * 0.12), run_time=0.6)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        g = scope_card()
        lh, rh = scope_cols()
        row1, row2 = right_rows()
        n1 = T("quieter = weaker transmission", 32, YELLOW).move_to([-3.4, -1.75, 0])
        n1b = T("as the muscle sees it", 32, TEXT).move_to([-3.4, -2.35, 0])
        n2 = T("a bias, not a verdict", 40, GOLD, weight=BOLD).move_to([-3.4, -3.3, 0])
        old = VGroup(g, lh, rh, row1, row2, n1, n1b, n2)
        self.add(old)
        # the first scene's fiber with three axons, now rivals
        Lc = dict(fiber=(0, -3.1, 9.0, 0.9), ep=(0, -2.65, 2.9), beadx=[-1.0, 0.0, 1.0], beady=-2.25,
                  tops=[(-2.0, 1.15), (0.0, 1.15), (2.0, 1.15)], bw=0.84)
        Jc = junction(Lc)
        somas = [Circle(radius=0.34, stroke_color=AX[i], stroke_width=4, fill_color=AX[i], fill_opacity=0.5)
                 .move_to([Lc["tops"][i][0], 1.15 + 0.34, 0]) for i in range(3)]
        l1 = Text("The neurons stay.", font=TITLE_FONT, font_size=60, color=TEXT).move_to([0, 3.35, 0])
        l2 = Text("Each fiber holds a contest.", font=TITLE_FONT, font_size=52, color=GOLD).move_to([0, 2.45, 0])
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(l1, shift=UP * 0.15), FadeIn(Jc["fiber"]), FadeIn(Jc["strip"]), *[FadeIn(s) for s in somas],
                  *[Create(a) for a in Jc["axons"]], *[FadeIn(b) for b in Jc["beads"]], run_time=0.8)
        self.at("each fiber", lead=0.0)
        # Each terminal advances into the shared endplate, then yields to its rival.
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.2)
        for i in range(3):
            bead = Jc["beads"][i]
            home = bead.get_center().copy()
            self.play(bead.animate.move_to([home[0] * 0.75, home[1] - 0.16, 0])
                      .set_fill(STIM, 0.95).scale(1.18),
                      ShowPassingFlash(Jc["axons"][i].copy().set_stroke(STIM, 14), time_width=0.7),
                      run_time=0.22)
            self.play(bead.animate.move_to(home).set_fill(AX[i], 0.6).scale(1 / 1.18), run_time=0.18)
        self.finish()


class S25End(EndCard):
    LINE = "A synapse is at risk when\nit is quieter than its neighbours."
