"""Too Little to Go Around  (chapter 1 of Competition: How Neurons Win a Target)

COLOR MAP (one color per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = a neuron whose fate is not yet decided (also the axons of the highlighted ganglion inside the mouse)
  GREEN  = a winner / a neuron that is protected or survives
  RED    = a loser / a neuron that dies or is pushed toward death (also the pro-death gene Bax)
  YELLOW = nerve growth factor (NGF)
  PURPLE = the receptor TrkA (its level) and the TrkA signal strength
  PINK   = how long each TrkA signal lasts (new in this chapter, used again in chapter 4)
  ORANGE = the punishment signal sent by winners
  TEAL   = the receptor p75
  TEXT   = plain labels and quotations (white)
  GOLD   = the question mark, "pause and guess", the leading neuron, and one highlight at a time
  GREY   = target, axons, axes, ganglion outline, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FB8"


def P(x, y):
    return np.array([x, y, 0.0])


# ----------------------------------------------------------------------------------------------
# small shape helpers
def soma(p, color=BLUE, r=0.27, op=0.9):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to(p)
    c.set_z_index(3)
    return c


def set_state(d, color, op=0.9):
    d.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)
    return d


def to_state(d, color, op=0.9):
    return d.animate.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)


def ngf_dot(p, r=0.1):
    d = Circle(radius=r, stroke_color=YELLOW, stroke_width=1.5, fill_color=YELLOW, fill_opacity=1).move_to(p)
    d.set_z_index(4)
    return d


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vbar(x, base, h, color=PURPLE, w=0.5):
    return Rectangle(width=w, height=max(h, 0.04), stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x, base + max(h, 0.04) / 2))


def hbar(x0, y, w, color=PURPLE, h=0.4):
    return Rectangle(width=max(w, 0.04), height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x0 + max(w, 0.04) / 2, y))


def axes_xy(x0, x1, y0, y1, xl, yl, size=26):
    ax = VGroup(Line(P(x0, y0), P(x1, y0), color=GREY, stroke_width=3),
                Line(P(x0, y0), P(x0, y1), color=GREY, stroke_width=3))
    xt = T(xl, size, GREY).move_to(P((x0 + x1) / 2, y0 - 0.5))
    yt = T(yl, size, GREY).rotate(PI / 2).move_to(P(x0 - 0.55, (y0 + y1) / 2))
    return VGroup(ax, xt, yt)


def box(cx, cy, w, h, color=GREY, op=0.12, r=0.25, sw=3):
    b = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                         fill_color=color, fill_opacity=op).move_to(P(cx, cy))
    b.set_z_index(0)
    return b


def left_text(s, x, y, size=26, color=TEXT, font=FONT, **kw):
    t = T(s, size, color, font=font, **kw)
    return t.move_to(P(x + t.width / 2, y))


def halo(p, r=0.5):
    h = Circle(radius=r, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to(p)
    h.set_z_index(2)
    return h


def stream(scene, dot, fn, period, phase):
    """A dot that drifts along fn(a), a from 0 to 1, over and over, fading in and out (a steady release)."""
    dot.clock = phase

    def up(m, dt):
        m.clock += dt
        a = (m.clock % period) / period
        m.move_to(fn(a))
        m.set_opacity(min(1.0, 5 * a, 5 * (1 - a)))

    dot.add_updater(up)
    scene.add(dot)


# ----------------------------------------------------------------------------------------------
# the stage that carries through the film (ganglion at left, three targets at right)
ZIG_Y = [2.45, 1.75, 1.05, 0.35, -0.35, -1.05, -1.75, -2.45]
ZIG = [P(-5.1 if i % 2 == 0 else -4.4, y) for i, y in enumerate(ZIG_Y)]
TARGETS = [("eye", 2.0), ("salivary gland", 0.0), ("heart", -2.0)]
TX, TW, TH = 4.9, 3.0, 1.3             # target boxes (left edge 3.4)
TEDGE = TX - TW / 2
LAND = [(0, 2.35), (0, 2.0), (0, 1.65), (1, 0.2), (1, -0.2), (2, -1.65), (2, -2.0), (2, -2.35)]
ZR = 0.34                               # cell radius on the stage


def stage_outline():
    o = RoundedRectangle(corner_radius=0.7, width=1.9, height=6.1, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.08).move_to(P(-4.75, 0))
    o.set_z_index(0)
    return o


def stage_label(text="sympathetic ganglion"):
    return T(text, 28, TEXT).move_to(P(-4.75, -3.45))


def stage_axons():
    out = VGroup()
    for i, (ti, ly) in enumerate(LAND):
        ln = Line(ZIG[i], P(TEDGE, ly), color=GREY, stroke_width=3)
        ln.set_z_index(1)
        out.add(ln)
    return out


def axon_y(i, x):
    """y of axon i at screen x (axons are straight lines from cell i to the target edge)."""
    x0, y0 = ZIG[i][0], ZIG[i][1]
    x1, y1 = TEDGE, LAND[i][1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def stage_target(i):
    name, ty = TARGETS[i]
    b = box(TX, ty, TW, TH)
    lab = T(name, 26, TEXT).move_to(b)
    return VGroup(b, lab)


def stage_static(scene, with_targets=True, with_axons=True):
    """Rebuild the ganglion + axons + targets stage exactly where scene 03 leaves it."""
    outline, label, axons = stage_outline(), stage_label(), stage_axons()
    somas = VGroup(*[soma(p, BLUE, ZR) for p in ZIG])
    tg = [stage_target(i) for i in range(3)]
    scene.add(outline, label, somas, *(tg if with_targets else []))
    if with_axons:
        scene.add(axons)
    return dict(outline=outline, label=label, axons=axons, somas=somas, targets=tg)


def cluster(cx, cy, sx=1.45, sy=1.25):
    rows = [(sy, [-sx, 0, sx]), (0, [-sx / 2, sx / 2]), (-sy, [-sx, 0, sx])]
    return [P(cx + x, cy + y) for y, xs in rows for x in xs]


# ---- scene-01 picture (one big target, eight axons) is reused by scene 02 and scenes 14-15
def build_s01():
    somas = VGroup(*[soma(p, BLUE, 0.32) for p in ZIG])
    tb = box(1.6, 0, 1.8, 5.8)
    tl = T("target", 26, TEXT).move_to(P(1.6, -3.35))
    ly = np.linspace(2.3, -2.3, 8)
    axons = VGroup(*[Line(ZIG[i], P(0.7, ly[i]), color=GREY, stroke_width=3) for i in range(8)])
    for a in axons:
        a.set_z_index(1)
    dots = VGroup(*[ngf_dot(p) for p in [P(2.85, 0.9), P(3.0, -0.1), P(2.85, -1.1)]])
    nchip = chip("NGF", YELLOW, 26).move_to(P(4.5, 1.7))
    q = T("?", 160, GOLD, weight=BOLD).move_to(P(5.3, -0.5))
    return dict(somas=somas, box=tb, tl=tl, axons=axons, dots=dots, nchip=nchip, q=q)


# ----------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "Too Little to Go Around"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        d = build_s01()
        self.at("A target makes")
        self.play(FadeIn(d["box"]), FadeIn(d["tl"]), run_time=0.8)
        self.at("too little")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.5, scale=0.4) for x in d["dots"]], lag_ratio=0.3), run_time=0.7)
        self.at("NGF")
        self.play(FadeIn(d["nchip"], shift=DOWN * 0.2), run_time=0.5)
        self.at("every neuron")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in d["somas"]], lag_ratio=0.08), run_time=0.9)
        self.play(LaggedStart(*[Create(a) for a in d["axons"]], lag_ratio=0.08), run_time=1.2)
        self.at("which neurons get to live")
        self.play(FadeIn(d["q"], scale=0.5), Indicate(d["somas"], color=BLUE, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ganglion_callouts():
    """The three callouts of scene 02 (they leave in scene 03)."""
    c1 = left_text("sympathetic neurons", -2.7, 1.9, 32, BLUE)
    l1 = Line(P(-2.8, 1.9), P(-4.02, 1.78), color=BLUE, stroke_width=3)
    brace = Brace(stage_outline(), RIGHT, color=GREY, buff=0.15)
    c2 = left_text("a small cluster of nerve cells", -2.2, 0.0, 32, TEXT)
    return c1, l1, brace, c2


class S02(SpokenScene):
    def construct(self):
        d = build_s01()
        somas = d["somas"]
        self.add(d["box"], d["tl"], d["axons"], d["dots"], d["nchip"], d["q"], somas)
        out = stage_outline()
        lab = stage_label()
        c1, l1, brace, c2 = ganglion_callouts()

        self.play(FadeOut(d["box"]), FadeOut(d["tl"]), FadeOut(d["axons"]), FadeOut(d["dots"]),
                  FadeOut(d["nchip"]), FadeOut(d["q"]),
                  *[somas[i].animate.scale(ZR / 0.32) for i in range(8)], run_time=0.8)
        self.at("Sympathetic neurons")
        self.play(FadeIn(out, scale=0.95), FadeIn(c1, shift=LEFT * 0.2), Create(l1), run_time=0.9)
        self.at("small clusters")
        self.play(GrowFromCenter(brace), FadeIn(c2, shift=LEFT * 0.2), Indicate(somas, color=BLUE, scale_factor=1.08),
                  run_time=1.0)
        self.at("ganglia")
        self.play(FadeIn(lab, shift=UP * 0.15), Indicate(out, color=GOLD, scale_factor=1.03), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    def construct(self):
        out, lab = stage_outline(), stage_label()
        somas = VGroup(*[soma(p, BLUE, ZR) for p in ZIG])
        c1, l1, brace, c2 = ganglion_callouts()
        self.add(out, lab, somas, c1, l1, brace, c2)
        axons = stage_axons()
        tg = [stage_target(i) for i in range(3)]

        self.play(FadeOut(c1), FadeOut(l1), FadeOut(brace), FadeOut(c2), run_time=0.5)
        self.at("axons to targets")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.1), run_time=1.1)
        self.at("the eye")
        self.play(FadeIn(tg[0], scale=0.9), run_time=0.6)
        self.at("salivary gland")
        self.play(FadeIn(tg[1], scale=0.9), run_time=0.6)
        self.at("the heart")
        self.play(FadeIn(tg[2], scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    def construct(self):
        st = stage_static(self)
        chipn = chip("nerve growth factor", YELLOW, 26).move_to(P(-0.6, 3.3))
        chipn2 = chip("nerve growth factor (NGF)", YELLOW, 26).move_to(P(-0.6, 3.3))
        made = T("made by the target", 28, TEXT).move_to(P(4.9, 3.3))
        nolab = T("no NGF here", 28, TEXT).move_to(P(-4.75, -3.45))
        cross = VGroup(Line(P(-5.5, 2.5), P(-4.0, -2.5), color=TEXT, stroke_width=9),
                       Line(P(-5.5, -2.5), P(-4.0, 2.5), color=TEXT, stroke_width=9)).set_opacity(0.9).set_z_index(6)

        # lanes of dots run between neighbouring axons, from the target edge toward the neurons
        lanes = [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7)]
        self.at("targets release")
        for k, (i, j) in enumerate(lanes):
            for m in range(2):
                def fn(a, i=i, j=j):
                    x = TEDGE - 0.12 - 1.9 * a
                    return P(x, (axon_y(i, x) + axon_y(j, x)) / 2)
                stream(self, ngf_dot(fn(0)), fn, 2.4, m * 1.2 + k * 0.3)
        self.wait(0.2)
        self.at("nerve growth factor")
        self.play(FadeIn(chipn, shift=DOWN * 0.2), run_time=0.6)
        self.at("NGF")
        self.play(Transform(chipn, chipn2), run_time=0.5)
        self.at("The target makes it")
        self.play(FadeIn(made, shift=DOWN * 0.1), Indicate(VGroup(*st["targets"]), color=YELLOW, scale_factor=1.04),
                  run_time=1.0)
        self.at("not the neurons")
        self.play(st["somas"].animate.set_opacity(0.3), FadeIn(cross), Transform(st["label"], nolab),
                  run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        st = stage_static(self)
        somas = st["somas"]
        winners, losers = [0, 2, 4, 6], [1, 3, 5, 7]

        def dots_for(i, n):
            ly = LAND[i][1]
            return [ngf_dot(P(TEDGE + 0.3 + 0.3 * k, ly), 0.1) for k in range(n)]

        wd = [dots_for(i, 3) for i in winners]
        ld = [dots_for(i, 1) for i in losers]
        top = T("enough NGF: the neuron lives", 28, GREEN).move_to(P(1.0, 3.4))
        bot = T("too little NGF: it dies through Bax", 28, RED).move_to(P(1.0, -3.4))

        def bax_badge(p):
            bx = RoundedRectangle(corner_radius=0.1, width=0.78, height=0.42, stroke_color=RED, stroke_width=2.5,
                                  fill_color=BG, fill_opacity=1)
            tx = T("Bax", 24, RED, weight=BOLD).move_to(bx)
            return VGroup(bx, tx).move_to(p).set_z_index(6)

        bax = [bax_badge(ZIG[i]) for i in losers]

        self.play(*[somas[i].animate.scale(1.3) for i in range(8)], *[FadeOut(t[1]) for t in st["targets"]], run_time=0.5)
        self.at("enough NGF")
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for g in wd for x in g], lag_ratio=0.05), run_time=0.7)
        self.at("live")
        self.play(*[to_state(somas[i], GREEN, 0.9) for i in winners], FadeIn(top, shift=UP * 0.1), run_time=0.6)
        self.at("Those that do not")
        self.play(*[FadeIn(x, scale=0.3) for g in ld for x in g], run_time=0.5)
        self.at("die through")
        self.play(*[to_state(somas[i], RED, 0.3) for i in losers], FadeIn(bot, shift=DOWN * 0.1), run_time=0.8)
        self.at("pro")
        self.play(*[FadeIn(b, scale=0.5) for b in bax], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(SpokenScene):
    def construct(self):
        X0, X1, Y0, Y1 = -5.0, 5.0, -2.8, 2.8
        axes = axes_xy(X0, X1, Y0, Y1, "time", "neurons")
        head = T("normal development, not damage", 36, TEXT).move_to(P(0, 3.45))

        def sg(z):
            return 1 / (1 + np.exp(-z))

        def N(t, k=11.0):
            lo, hi = sg(-0.5 * k), sg(0.5 * k)
            return 1 - 0.5 * (sg(k * (t - 0.5)) - lo) / (hi - lo)

        def pt(t):
            return P(X0 + 0.3 + t * (X1 - X0 - 0.6), Y0 + 0.25 + N(t) * (Y1 - Y0 - 0.5))

        ts = np.linspace(0, 1, 80)
        curve = VMobject(stroke_color=RED, stroke_width=6).set_points_smoothly([pt(t) for t in ts])
        dot = Dot(pt(0), radius=0.14, color=TEXT)
        full = DashedLine(P(X0, pt(0)[1]), P(X1, pt(0)[1]), color=GREY, stroke_width=2.5)
        halfy = Y0 + 0.25 + 0.5 * (Y1 - Y0 - 0.5)
        half = DashedLine(P(X0, halfy), P(X1, halfy), color=GOLD, stroke_width=3)
        hl = T("half", 28, GOLD).move_to(P(X1 - 0.6, halfy + 0.4))
        sch = T("schematic, not counts", 26, GOLD).move_to(P(2.6, -2.2))
        cap = T("roughly half die in\nmany developing populations", 30, TEXT, line_spacing=0.9).move_to(P(-1.6, -1.15))
        flab = T("all neurons", 26, GREY).move_to(P(X0 + 1.5, pt(0)[1] + 0.4))

        # the first things are on screen before the first word
        self.add(head, axes, full, sch, flab, dot)
        self.at("not damage")
        self.play(Create(curve, rate_func=linear), MoveAlongPath(dot, curve, rate_func=linear), run_time=3.5)
        self.at("roughly half")
        self.play(Create(half), FadeIn(hl), run_time=0.7)
        self.at("neurons die")
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(SpokenScene):
    def construct(self):
        head = T("the neurotrophic hypothesis", 34, TEXT).move_to(P(0, 3.3))
        rule = Line(P(-3.0, 2.9), P(3.0, 2.9), color=GOLD, stroke_width=4)
        l1 = T("“Neurons compete for", 40, TEXT, font=TITLE_FONT).move_to(P(0, 1.9))
        l2 = T("a limiting amount of neurotrophic factor", 40, TEXT, font=TITLE_FONT).move_to(P(0, 0.95))
        l3 = T("for survival.”", 40, TEXT, font=TITLE_FONT).move_to(P(0, 0.0))
        fit(l2, 12.0)
        xs = np.linspace(-3.9, 3.9, 6)
        ns = VGroup(*[soma(P(x, -2.4), BLUE, 0.5, 0.85) for x in xs])
        ds = VGroup(*[ngf_dot(P(x, -1.0), 0.14) for x in (-0.6, 0, 0.6)])

        self.add(head, rule, ns)
        self.at("Neurons compete")
        self.play(FadeIn(l1, shift=UP * 0.1), Indicate(ns, color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("limiting amount")
        self.play(FadeIn(l2, shift=UP * 0.1), LaggedStart(*[FadeIn(d, scale=0.3) for d in ds], lag_ratio=0.2), run_time=1.0)
        self.play(Indicate(ds, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("for survival")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    def construct(self):
        body = RoundedRectangle(corner_radius=1.4, width=6.0, height=5.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to(P(0, -0.1))
        cord = T("spinal cord:\nmotor neurons", 26, TEXT, line_spacing=0.9).move_to(P(0, 1.95))

        def block(cx):
            return VGroup(*[soma(P(cx + dx, y), BLUE, 0.2, 0.9) for y in (0.95, 0.4, -0.15, -0.7) for dx in (-0.3, 0.3)])

        lc, rc = block(-1.7), block(1.7)

        def limb(x, y, name, color=GREY, dashed=False):
            b = box(x, y, 2.4, 1.2, color, 0.12, 0.2)
            if dashed:
                b = DashedVMobject(b, num_dashes=40)
                b = VGroup(b, box(x, y, 2.4, 1.2, color, 0.12, 0.2).set_stroke(opacity=0))
            lab = T(name, 26, TEXT).move_to(P(x, y))
            return VGroup(b, lab)

        L1 = limb(-5.3, 0.1, "limb")
        R1 = limb(5.3, 1.4, "limb")
        R2 = limb(5.3, -1.2, "extra limb", GOLD, True)
        wl = Line(P(-2.5, 0.1), P(-4.1, 0.1), color=GREY, stroke_width=3)
        wr1 = Line(P(2.5, 0.1), P(4.1, 1.4), color=GREY, stroke_width=3)
        wr2 = Line(P(2.5, 0.1), P(4.1, -1.2), color=GOLD, stroke_width=3)
        top = T("chick embryo", 28, TEXT).move_to(P(-5.2, 3.5))
        sch = left_text("schematic, not counts", 3.2, 3.5, 24, GOLD)
        more = T("more target, more survivors", 30, GREEN).move_to(P(-0.4, 3.5))
        nl = T("normal side", 26, TEXT).move_to(P(-1.7, -3.05))
        el = T("extra-limb side", 26, TEXT).move_to(P(1.7, -3.05))
        nc = T("4 of 8 survive", 26, GREEN).move_to(P(-1.7, -3.55))
        ec = T("6 of 8 survive", 26, GREEN, weight=BOLD).move_to(P(1.7, -3.55))

        self.play(FadeIn(body), FadeIn(cord), FadeIn(lc), FadeIn(rc), FadeIn(L1), FadeIn(R1), FadeIn(wl), FadeIn(wr1),
                  FadeIn(nl), FadeIn(sch), run_time=1.0)
        self.at("the count follows")
        self.play(Indicate(VGroup(lc, rc), color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("chick embryo")
        self.play(FadeIn(top), run_time=0.5)
        self.at("extra limb")
        self.play(FadeIn(R2, shift=LEFT * 0.4), Create(wr2), FadeIn(el), run_time=0.9)
        self.at("fewer motor neurons")
        ldead, rdead = [1, 3, 4, 6], [2, 5]
        self.play(*[to_state(lc[i], RED if i in ldead else GREEN, 0.3 if i in ldead else 0.95) for i in range(8)],
                  *[to_state(rc[i], RED if i in rdead else GREEN, 0.3 if i in rdead else 0.95) for i in range(8)],
                  run_time=1.0)
        self.at("on that side")
        self.play(FadeIn(nc, shift=UP * 0.1), FadeIn(ec, shift=UP * 0.1), run_time=0.7)
        self.at("die")
        self.play(FadeIn(more, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
DIAL_C = P(-3.3, -1.0)
DIAL_R = 2.9


def make_dial(angle_deg=180):
    arc = Arc(radius=DIAL_R, start_angle=PI, angle=-PI, arc_center=DIAL_C, stroke_color=GREY, stroke_width=6)
    ticks = VGroup(*[Line(DIAL_C + (DIAL_R - 0.3) * P(np.cos(a), np.sin(a)), DIAL_C + DIAL_R * P(np.cos(a), np.sin(a)),
                          color=GREY, stroke_width=4) for a in np.linspace(PI, 0, 7)])
    ang = angle_deg * DEGREES
    needle = Line(DIAL_C, DIAL_C + (DIAL_R - 0.35) * P(np.cos(ang), np.sin(ang)), color=GOLD, stroke_width=9)
    hub = Dot(DIAL_C, radius=0.18, color=GOLD)
    title = T("target size", 34, TEXT).move_to(P(-3.3, 2.7))
    ends = VGroup(T("small target", 26, TEXT).move_to(P(-5.2, -1.7)), T("large target", 26, TEXT).move_to(P(-1.4, -1.7)))
    return arc, ticks, needle, hub, title, ends


CL9 = cluster(3.6, 0.35, 1.6, 1.35)
ORD9 = [[1, 6, 3], [1, 6, 3, 4, 0], [1, 6, 3, 4, 0, 7, 2]]


def count_text(n, color=GREEN):
    return T(f"{n} of 8 survive", 32, color).move_to(P(3.6, -2.75))


class S09(SpokenScene):
    def construct(self):
        arc, ticks, needle, hub, title, ends = make_dial(180)
        ns = VGroup(*[soma(CL9[i], BLUE, 0.55) for i in range(8)])

        def lit(order):
            return [to_state(ns[i], GREEN, 0.9) if i in order else to_state(ns[i], RED, 0.3) for i in range(8)]

        # everything starts blue (undecided): the earlier scene's result is cleared
        self.play(FadeIn(arc), FadeIn(ticks), FadeIn(needle), FadeIn(hub), FadeIn(ns), FadeIn(title), FadeIn(ends),
                  run_time=0.5)
        self.at("size of the target")
        c3 = count_text(3)
        self.play(needle.animate.rotate(-20 * DEGREES, about_point=DIAL_C), *lit(ORD9[0]), FadeIn(c3), run_time=0.5)
        self.at("sets roughly")
        c5 = count_text(5)
        self.play(needle.animate.rotate(-70 * DEGREES, about_point=DIAL_C), *lit(ORD9[1]), FadeOut(c3), FadeIn(c5),
                  run_time=0.6)
        self.at("how many")
        c7 = count_text(7)
        self.play(needle.animate.rotate(-70 * DEGREES, about_point=DIAL_C), *lit(ORD9[2]), FadeOut(c5), FadeIn(c7),
                  run_time=0.6)
        self.at("can win")
        self.play(Indicate(VGroup(*[ns[i] for i in ORD9[2]]), color=GREEN, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
CL10 = cluster(0, -0.95, 3.1, 1.45)


class S10(SpokenScene):
    def construct(self):
        arc, ticks, needle, hub, title, ends = make_dial(20)
        c7 = count_text(7)
        ns = VGroup(*[soma(CL9[i], GREEN if i in ORD9[2] else RED, 0.55, 0.9 if i in ORD9[2] else 0.3) for i in range(8)])
        self.add(arc, ticks, needle, hub, title, ends, ns, c7)
        q = T("?", 160, GOLD, weight=BOLD).move_to(P(0, 2.45))

        # the dial clears first, then the cells regroup and return to undecided blue
        self.play(FadeOut(arc), FadeOut(ticks), FadeOut(needle), FadeOut(hub), FadeOut(title), FadeOut(ends), FadeOut(c7),
                  run_time=0.6)
        self.play(*[Transform(ns[i], soma(CL10[i], BLUE, 0.68)) for i in range(8)], FadeIn(q, scale=0.5), run_time=1.0)
        self.at("a contest")
        self.play(Indicate(ns, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("how the contest is decided")
        self.play(Indicate(q, color=GOLD, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
WIN11, LOSE11 = [0, 2, 3, 6], [1, 4, 5, 7]
SX11, SY11 = -3.9, [1.9, 0.65, -0.6, -1.85]
TB11 = dict(cx=3.9, cy=0.1, w=5.2, h=5.6)
LAND11 = [P(1.3, y) for y in SY11]


def s11_pieces():
    surv = VGroup(*[soma(P(SX11, SY11[k]), GREEN, 0.5, 0.9) for k in range(4)])
    tbox = box(TB11["cx"], TB11["cy"], TB11["w"], TB11["h"])
    tlab = T("target", 26, TEXT).move_to(P(3.9, 3.4))
    axons = VGroup(*[Line(P(SX11 + 0.5, SY11[k]), LAND11[k], color=GREY, stroke_width=3) for k in range(4)])
    sparse, extra = VGroup(), VGroup()
    for k in range(4):
        for dy in (-0.5, 0, 0.5):
            sparse.add(Line(LAND11[k], P(3.5, SY11[k] + dy * 1.3), color=GREEN, stroke_width=2.5))
        for dy in (-0.62, -0.31, -0.15, 0.15, 0.31, 0.62):
            extra.add(Line(LAND11[k], P(6.45, SY11[k] + dy * 1.15), color=GREEN, stroke_width=2.5))
    lab1 = T("number of survivors", 28, GREEN).move_to(P(-3.3, -3.35))
    lab2 = T("how densely they\ncover the target", 28, TEXT, line_spacing=0.9).move_to(P(3.9, -3.3))
    q = T("?", 110, GOLD, weight=BOLD).move_to(P(-2.3, 3.0))
    return dict(q=q, surv=surv, tbox=tbox, tlab=tlab, axons=axons, sparse=sparse, extra=extra, lab1=lab1, lab2=lab2)


class S11(SpokenScene):
    def construct(self):
        ns = VGroup(*[soma(CL10[i], BLUE, 0.68) for i in range(8)])
        q0 = T("?", 160, GOLD, weight=BOLD).move_to(P(0, 2.45))
        self.add(ns, q0)
        pc = s11_pieces()
        q = pc["q"]

        # the old question mark leaves in the same move that rearranges the cells
        self.play(FadeOut(q0, scale=0.6), FadeOut(VGroup(*[ns[i] for i in LOSE11])),
                  *[Transform(ns[WIN11[k]], soma(P(SX11, SY11[k]), GREEN, 0.5)) for k in range(4)],
                  FadeIn(pc["tbox"]), FadeIn(pc["tlab"]), run_time=1.1)
        self.at("outcome")
        self.play(FadeIn(pc["lab1"], shift=UP * 0.1), Indicate(VGroup(*[ns[i] for i in WIN11]), color=GREEN, scale_factor=1.1),
                  run_time=0.8)
        self.at("fit between")
        self.play(LaggedStart(*[Create(a) for a in pc["axons"]], lag_ratio=0.1), FadeIn(q, scale=0.5),
                  FadeIn(pc["lab2"], shift=UP * 0.1), run_time=0.9)
        self.at("target and its")
        self.play(Create(pc["sparse"], lag_ratio=0.03), run_time=0.7)
        self.play(Create(pc["extra"], lag_ratio=0.03), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
MOUSE_PTS = [(-6.55, -0.75), (-5.9, -0.05), (-5.2, 0.7), (-4.5, 1.05), (-3.85, 0.9), (-3.3, 0.55), (-2.4, 1.3),
             (-1.0, 2.2), (0.8, 2.75), (2.8, 2.9), (4.7, 2.45), (6.0, 1.5), (6.6, 0.0), (6.35, -1.4), (5.2, -2.6),
             (3.2, -3.2), (1.0, -3.1), (-0.9, -2.6), (-2.2, -1.8), (-3.2, -1.3), (-3.9, -1.6), (-4.9, -1.7),
             (-5.8, -1.35), (-6.55, -0.75)]
GANG = P(-3.2, -0.35)
EYE = P(-5.25, 0.3)
GLAND = P(-4.55, -1.0)
MOUSE_FILL = "#1B1E27"


def build_mouse():
    sil = VMobject(stroke_color=GREY, stroke_width=4, fill_color=MOUSE_FILL, fill_opacity=1)
    sil.set_points_smoothly([P(x, y) for x, y in MOUSE_PTS])
    sil.set_z_index(1)
    # the ear sits behind the head, so only its outer edge shows
    ear = Circle(radius=0.8, stroke_color=GREY, stroke_width=4, fill_color=MOUSE_FILL, fill_opacity=1).move_to(P(-4.0, 1.35))
    ear.set_z_index(0)
    nose = Dot(P(-6.4, -0.72), radius=0.14, color=GREY).set_z_index(2)
    eye = Dot(EYE, radius=0.11, color=TEXT).set_z_index(2)
    mouse = VGroup(ear, sil, nose, eye)
    cells = VGroup(*[Circle(radius=0.14, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.9)
                     .move_to(GANG + P(dx, dy)).set_z_index(3)
                     for dx, dy in [(-0.22, 0.15), (0.1, 0.24), (0.25, -0.05), (-0.08, -0.12), (0.1, -0.3), (-0.28, -0.24)]])
    ring = Circle(radius=0.6, stroke_color=GOLD, stroke_width=4).move_to(GANG).set_z_index(3)
    glabel = left_text("superior cervical ganglion", -2.2, -0.35, 30, GOLD).set_z_index(3)
    return dict(mouse=mouse, sil=sil, ear=ear, cells=cells, ring=ring, glabel=glabel)


def chips_final():
    ca = T("one cell type:", 32, TEXT)
    cb = T("sympathetic neurons", 32, BLUE)
    row = VGroup(ca, cb).arrange(RIGHT, buff=0.25)
    row.move_to(P(-6.7 + row.width / 2, 3.4))
    return ca, cb


class S12(SpokenScene):
    def construct(self):
        # the last picture of scene 11 carries over and clears while the mouse is drawn in its place
        pc = s11_pieces()
        old = VGroup(pc["tbox"], pc["tlab"], pc["axons"], pc["sparse"], pc["extra"], pc["lab1"], pc["lab2"], pc["q"], pc["surv"])
        self.add(old)
        m = build_mouse()
        ca1, cb1 = chips_final()

        self.play(FadeOut(old), FadeIn(m["sil"]), FadeIn(m["ear"]), FadeIn(m["mouse"][2:]), run_time=1.4)
        self.at("one cell type")
        self.play(FadeIn(ca1, shift=DOWN * 0.15), run_time=0.5)
        self.at("sympathetic neurons")
        self.play(FadeIn(cb1, shift=DOWN * 0.15), run_time=0.6)
        self.at("superior cervical")
        self.play(FadeIn(m["cells"], scale=0.4), Create(m["ring"]), run_time=0.7)
        self.at("ganglion")
        self.play(FadeIn(m["glabel"], shift=RIGHT * 0.15), run_time=0.7)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        m = build_mouse()
        ca1, cb1 = chips_final()
        self.add(m["mouse"], m["cells"], m["ring"], m["glabel"], ca1, cb1)
        eye_t = Circle(radius=0.28, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to(EYE).set_z_index(2)
        gland = Ellipse(width=1.0, height=0.6, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to(GLAND).set_z_index(3)
        eye_lab = T("eye", 28, TEXT).move_to(P(-6.2, 1.9))
        eye_ld = Line(P(-6.0, 1.65), P(-5.4, 0.5), color=TEXT, stroke_width=2.5)
        gl_lab = T("salivary gland", 28, TEXT).move_to(P(-5.3, -2.65))
        gl_ld = Line(P(-4.9, -2.35), P(-4.6, -1.3), color=TEXT, stroke_width=2.5)
        neck_lab = T("neck", 28, GOLD).move_to(P(-3.0, -2.55))
        neck_ld = Line(P(-3.15, -2.25), P(-3.2, -1.35), color=GOLD, stroke_width=2.5)
        axons = VGroup(Line(GANG + P(-0.55, 0.2), EYE + P(0.3, -0.05), color=BLUE, stroke_width=6),
                       Line(GANG + P(-0.55, -0.15), GLAND + P(0.5, 0.05), color=BLUE, stroke_width=6)).set_z_index(3)
        for o in (eye_lab, eye_ld, gl_lab, gl_ld, neck_lab, neck_ld):
            o.set_z_index(3)
        dish = Circle(radius=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to(P(6.0, 3.05))
        cells = VGroup(*[soma(p, BLUE, 0.1, 0.9) for p in (P(5.85, 3.15), P(6.15, 3.15), P(5.9, 2.9), P(6.15, 2.9))])
        dlab = T("cultured rat neurons", 28, TEXT).move_to(P(3.3, 3.4))

        self.at("That ganglion sits")
        self.play(Indicate(m["ring"], color=GOLD, scale_factor=1.25), run_time=0.8)
        self.at("neck")
        self.play(FadeIn(neck_lab), Create(neck_ld), run_time=0.4)
        self.at("supplies the head")
        self.play(FadeIn(eye_t), FadeIn(gland), FadeIn(eye_lab), Create(eye_ld), FadeIn(gl_lab), Create(gl_ld), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.2), run_time=1.1)
        self.at("Some experiments")
        self.play(FadeIn(dish, scale=0.8), FadeIn(cells, scale=0.5), run_time=0.8)
        self.at("rat neurons")
        self.play(FadeIn(dlab, shift=RIGHT * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s14_question():
    return T("what decides\nwhich ones?", 40, GOLD, weight=BOLD, line_spacing=0.9).move_to(P(5.0, 1.7))


def s14_guess():
    return chip("Pause and guess", GOLD, 28).move_to(P(5.0, 0.2))


class S14(SpokenScene):
    def construct(self):
        d = build_s01()
        guess = s14_guess()
        q = s14_question()
        self.play(FadeIn(d["box"]), FadeIn(d["tl"]), FadeIn(d["axons"]), FadeIn(d["somas"]), FadeIn(guess, shift=UP * 0.15),
                  run_time=0.8)
        self.at("If a target can feed")
        self.play(LaggedStart(*[FadeIn(x, scale=0.4) for x in d["dots"]], lag_ratio=0.25), run_time=0.8)
        self.at("what decides which ones")
        self.play(FadeIn(q, scale=0.8), Indicate(d["somas"], color=BLUE, scale_factor=1.06), run_time=0.8)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        d = build_s01()
        self.add(d["box"], d["tl"], d["axons"], d["somas"], d["dots"], s14_guess(), s14_question())
        rc = P(5.0, -1.9)
        track = Circle(radius=0.85, stroke_color=GREY, stroke_width=6).move_to(rc)
        tr = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.85, start_angle=PI / 2, angle=max(TAU * tr.get_value(), 0.001),
                                         arc_center=rc, stroke_color=GOLD, stroke_width=9))
        num = always_redraw(lambda: T(str(max(1, int(np.ceil(5 * tr.get_value() - 1e-6)))), 44, GOLD, weight=BOLD).move_to(rc))
        self.add(track, ring, num)
        self.play(tr.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16(SpokenScene):
    def construct(self):
        card = box(0, 0, 12.4, 6.4, GREY, 0.05, 0.4, 3)
        tbar = box(0, 2.2, 8.6, 0.9, GREY, 0.14, 0.2)
        tlab = T("target", 28, TEXT).move_to(P(0, 2.2))
        dots = VGroup(*[ngf_dot(P(x, 1.4), 0.12) for x in (-0.9, -0.3, 0.3, 0.9)])
        xs = np.linspace(-5.25, 5.25, 8)
        ns = VGroup(*[soma(P(x, 0.1), BLUE, 0.5) for x in xs])
        t1 = T("The target sets how many.", 38, TEXT, font=TITLE_FONT).move_to(P(0, -1.65))
        t2 = T("The neurons decide which.", 38, GREEN, font=TITLE_FONT).move_to(P(0, -2.6))
        chosen = [1, 3, 4, 6]

        self.play(FadeIn(card), LaggedStart(*[FadeIn(n, scale=0.4) for n in ns], lag_ratio=0.08), run_time=1.2)
        self.at("target sets")
        self.play(FadeIn(tbar), FadeIn(tlab), run_time=0.6)
        self.at("how many")
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in dots], lag_ratio=0.2), FadeIn(t1, shift=UP * 0.1), run_time=1.0)
        self.at("neurons decide")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        self.at("which")
        self.play(*[to_state(ns[i], GREEN, 0.9) if i in chosen else to_state(ns[i], RED, 0.3) for i in range(8)], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scene 17: matched neurons, a small lead, and a curve that rises faster than in proportion
PX0, PX1, PY0, PY1 = -5.8, 0.4, -2.9, 3.0
SHARE_A, SHARE_B = 1.1, 0.9          # 55% vs 45%, as a multiple of an even share (same lead as scenes 20-21)


def PXs(s):
    return -5.5 + (s - 0.5) * 6.0


def PYv(v):
    return PY0 + 0.1 + v * 1.95


BAR_BASE = -2.6
BAR_K = 2.2
BAR_AX, BAR_BX = 2.9, 4.4
BR_X = 5.35


class S17(SpokenScene):
    def construct(self):
        axes = axes_xy(PX0, PX1, PY0, PY1, "NGF a neuron gets", "its signal")
        sv = np.linspace(0.5, 1.4, 60)
        lin = VMobject(stroke_color=GREY, stroke_width=5).set_points_smoothly([P(PXs(s), PYv(s)) for s in sv])
        cub = VMobject(stroke_color=PURPLE, stroke_width=6).set_points_smoothly([P(PXs(s), PYv(s ** 3)) for s in sv])

        def cell(s, name):
            c = soma(P(0, 0), BLUE, 0.2)
            return VGroup(c, T(name, 24, BG, weight=BOLD).set_z_index(6)).move_to(P(PXs(s), PY0))

        mA, mB = cell(SHARE_A, "A"), cell(SHARE_B, "B")
        lA, lB = T("A", 28, TEXT), T("B", 28, TEXT)
        lA.move_to(P(BAR_AX, BAR_BASE - 0.4)), lB.move_to(P(BAR_BX, BAR_BASE - 0.4))
        bar_base = Line(P(2.0, BAR_BASE), P(5.0, BAR_BASE), color=GREY, stroke_width=3)
        sig_lbl = T("signal", 28, TEXT).move_to(P(3.65, 0.55))

        def bars(ha, hb):
            return (vbar(BAR_AX, BAR_BASE, ha * BAR_K, PURPLE, 1.0), vbar(BAR_BX, BAR_BASE, hb * BAR_K, PURPLE, 1.0))

        ba, bb = bars(1.0, 1.0)

        def bracket(ha, hb):
            y1, y2 = BAR_BASE + ha * BAR_K, BAR_BASE + hb * BAR_K
            br = DoubleArrow(P(BR_X, y2), P(BR_X, y1), buff=0, color=GOLD, stroke_width=5, tip_length=0.14)
            g1 = DashedLine(P(BAR_AX + 0.5, y1), P(BR_X, y1), color=GOLD, stroke_width=2)
            g2 = DashedLine(P(BAR_BX + 0.5, y2), P(BR_X, y2), color=GOLD, stroke_width=2)
            return VGroup(br, g1, g2)

        def guides(sa, sb, f):
            return VGroup(DashedLine(P(PXs(sa), PY0), P(PXs(sa), PYv(f(sa))), color=GREY, stroke_width=2.5),
                          DashedLine(P(PXs(sb), PY0), P(PXs(sb), PYv(f(sb))), color=GREY, stroke_width=2.5))

        lead_lbl = T("lead", 28, GOLD).move_to(P(6.3, BAR_BASE + 1.0 * BAR_K))
        lin_lbl = T("in proportion", 30, WHITE, weight=BOLD).move_to(P(-4.0, -0.3))
        fast_lbl = T("faster than in proportion", 28, PURPLE).move_to(P(-3.0, 2.5))

        self.play(FadeIn(axes), Create(lin), FadeIn(mA), FadeIn(mB), FadeIn(bar_base), FadeIn(sig_lbl),
                  GrowFromEdge(ba, DOWN), GrowFromEdge(bb, DOWN), FadeIn(lA), FadeIn(lB), run_time=1.2)
        self.at("otherwise alike")
        self.play(Indicate(VGroup(ba, bb), color=PURPLE, scale_factor=1.04), run_time=0.8)
        self.at("small lead")
        g = guides(SHARE_A, SHARE_B, lambda s: s)
        br = bracket(SHARE_A, SHARE_B)
        nb = bars(SHARE_A, SHARE_B)
        self.play(Transform(ba, nb[0]), Transform(bb, nb[1]), FadeIn(g), FadeIn(br), FadeIn(lead_lbl), run_time=1.0)
        self.at("grow only if")
        self.play(Indicate(br, color=GOLD, scale_factor=1.2), run_time=0.7)
        self.at("faster than")
        g2 = guides(SHARE_A, SHARE_B, lambda s: s ** 3)
        br2 = bracket(SHARE_A ** 3, SHARE_B ** 3)
        nb2 = bars(SHARE_A ** 3, SHARE_B ** 3)
        self.play(Create(cub), FadeIn(fast_lbl), Transform(g, g2), Transform(br, br2),
                  Transform(ba, nb2[0]), Transform(bb, nb2[1]),
                  lead_lbl.animate.move_to(P(6.3, BAR_BASE + 1.0 * BAR_K * 0.5 * (SHARE_A ** 3 + SHARE_B ** 3))), run_time=0.9)
        self.at("in proportion")
        self.play(FadeIn(lin_lbl), Indicate(lin, color=GREY, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18(SpokenScene):
    def construct(self):
        tag = left_text("published simulations", -6.6, 3.6, 26, GREY)
        cA = VGroup(soma(P(0, 0), BLUE, 0.5), T("A", 30, BG, weight=BOLD).set_z_index(6)).move_to(P(-5.6, 1.5))
        cB = VGroup(soma(P(0, 0), BLUE, 0.5), T("B", 30, BG, weight=BOLD).set_z_index(6)).move_to(P(-5.6, -2.0))
        ngf = chip("NGF", YELLOW, 28).move_to(P(-5.6, -0.3))
        YA, YB = 0.9, -2.5

        def block(x, yb):
            return RoundedRectangle(corner_radius=0.08, width=0.34, height=0.75, stroke_color=PURPLE, stroke_width=2,
                                    fill_color=PURPLE, fill_opacity=0.9).move_to(P(x, yb + 0.07 + 0.375))
        sx = [-4.5 + 0.55 * k for k in range(6)]
        memA = Rectangle(width=3.4, height=0.14, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.6).move_to(P(-3.0, YA))
        memB = Rectangle(width=3.4, height=0.14, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.6).move_to(P(-3.0, YB))
        bA = [block(x, YA) for x in sx]
        bB = [block(x, YB) for x in sx[:3]]
        h_rec = chip("receptors", PURPLE, 28).move_to(P(-3.0, 2.8))
        h_rec2 = chip("TrkA receptors", PURPLE, 28).move_to(P(-3.0, 2.8))
        a1 = arr(P(-5.0, 0.0), P(-4.55, 0.78), PURPLE, 6, 0.24)
        # signal timelines
        axA = Line(P(-0.9, YA), P(2.7, YA), color=GREY, stroke_width=3)
        axB = Line(P(-0.9, YB), P(2.7, YB), color=GREY, stroke_width=3)
        tA = left_text("time", 2.8, YA, 26, GREY)
        tB = left_text("time", 2.8, YB, 26, GREY)
        sbA = hbar(-0.9, YA + 0.4, 0.9, PINK, 0.42)
        sbB = hbar(-0.9, YB + 0.4, 0.9, PINK, 0.42)
        h_sig = chip("TrkA signal", PINK, 28).move_to(P(1.0, 2.8))
        slab = left_text("signal lasts longer", -0.9, YA + 1.0, 26, PINK)
        a2 = arr(P(-5.0, -0.12), P(-1.15, 0.8), PINK, 6, 0.24)
        # result column
        rt = T("do they\nseparate?", 28, TEXT, line_spacing=0.9).move_to(P(5.3, 2.7))
        RB = -1.3
        rA, rB = 4.7, 6.0

        def rbars(ha, hb):
            return vbar(rA, RB, ha, GREEN if ha > hb + 0.01 else BLUE, 0.9), vbar(rB, RB, hb, RED if ha > hb + 0.01 else BLUE, 0.9)
        r1, r2 = rbars(1.3, 1.3)
        rl = VGroup(T("A", 26, TEXT).move_to(P(rA, RB - 0.4)), T("B", 26, TEXT).move_to(P(rB, RB - 0.4)))
        cap1 = T("one change:\nstay together", 26, TEXT, line_spacing=0.9).move_to(P(5.35, -2.45))
        cap2 = T("both changes:\nthey split", 26, GOLD, line_spacing=0.9).move_to(P(5.35, -2.45))
        both = T("both needed", 34, GOLD).move_to(P(-1.2, -3.45))
        loop = Arc(radius=0.95, start_angle=PI * 0.3, angle=PI * 1.5, arc_center=P(-5.6, 1.5), stroke_color=PURPLE, stroke_width=8)
        loop.add_tip(tip_length=0.3)
        loop_lbl = T("feedback", 28, PURPLE).move_to(P(-5.6, 2.95))

        self.play(FadeIn(tag), FadeIn(cA), FadeIn(cB), run_time=0.5)
        self.at("NGF")
        self.play(FadeIn(ngf, scale=0.7), run_time=0.4)
        self.at("raised its")
        self.play(GrowArrow(a1), FadeIn(memA), FadeIn(memB), *[FadeIn(b, shift=UP * 0.2) for b in bA[:3] + bB], run_time=0.7)
        self.at("receptor")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in bA[3:]], lag_ratio=0.25), FadeIn(h_rec), run_time=0.9)
        self.at("track a")
        self.play(Transform(h_rec, h_rec2), FadeIn(rt), GrowFromEdge(r1, DOWN), GrowFromEdge(r2, DOWN), FadeIn(rl),
                  FadeIn(cap1), run_time=0.7)
        self.at("lengthened")
        self.play(GrowArrow(a2), FadeIn(axA), FadeIn(axB), FadeIn(tA), FadeIn(tB), FadeIn(sbA), FadeIn(sbB), FadeIn(h_sig),
                  run_time=0.7)
        self.play(Transform(sbA, hbar(-0.9, YA + 0.4, 3.2, PINK, 0.42)), FadeIn(slab), run_time=1.2)
        self.at("both were needed")
        n1, n2 = rbars(2.6, 0.7)
        self.play(FadeOut(cap1), FadeIn(both, shift=UP * 0.1), run_time=0.4)
        self.play(Transform(r1, n1), Transform(r2, n2), FadeIn(cap2), run_time=0.9)
        self.at("neurons to separate")
        self.play(Create(loop), FadeIn(loop_lbl, shift=DOWN * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    def construct(self):
        tag = T("proposed model", 34, GREY).move_to(P(0, 3.45))
        WC, LC = P(-4.0, 0.0), P(4.0, 0.0)
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GREEN, fill_opacity=o).move_to(WC)
                        for r, o in ((2.0, 0.10), (1.7, 0.18))])
        winner = soma(WC, GREEN, 1.3, 0.9)
        loser = soma(LC, BLUE, 1.3, 0.55)
        strong = VGroup(*[ngf_dot(WC + 1.9 * P(np.cos(a), np.sin(a)), 0.13) for a in np.radians([100, 135, 170, 205, 240, 270])])
        weak = ngf_dot(LC + P(0.0, 1.9), 0.13)
        wl = T("winner", 30, GREEN).move_to(P(-4.0, -2.65))
        ll = T("loser", 30, TEXT).move_to(P(4.0, -2.65))
        rec = RoundedRectangle(corner_radius=0.06, width=0.34, height=1.2, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.95).move_to(P(2.7, 0.0))
        rec.set_z_index(5)
        rl = T("p75", 38, TEAL, weight=BOLD).move_to(P(2.5, 1.55))
        arrow = arr(P(-2.5, 0.0), P(2.4, 0.0), ORANGE, 9, 0.34)
        al = T("speeds death", 28, ORANGE).move_to(P(-0.05, 0.7))

        # both neurons are on screen before the first word: one fed well, one fed poorly
        self.add(tag)
        self.play(FadeIn(glow), FadeIn(winner, scale=0.8), FadeIn(loser, scale=0.8),
                  LaggedStart(*[FadeIn(x, scale=0.3) for x in strong], lag_ratio=0.08), FadeIn(weak, scale=0.3), run_time=0.8)
        self.at("winners then")
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.4)
        self.at("speed the death")
        self.play(GrowArrow(arrow), FadeIn(al), run_time=0.5)
        self.at("of losers")
        self.play(FadeIn(ll, shift=UP * 0.1), run_time=0.6)
        self.at("through a receptor")
        self.play(FadeIn(rec, shift=LEFT * 0.2), run_time=0.5)
        self.at("p 75")
        self.play(FadeIn(rl, shift=DOWN * 0.1), Indicate(rec, color=TEAL, scale_factor=1.4), run_time=0.7)
        self.play(to_state(loser, RED, 0.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
LIM_X = -6.6
LIST_Y = {1: 1.85, 2: 0.0, 3: -1.9}
LIST_TXT = {1: "1  where the first lead\n    comes from",
            2: "2  faster than in\n    proportion: needed,\n    not enough",
            3: "3  chick motor neurons:\n    several factors"}


def limits_title():
    return left_text("Limits", LIM_X, 3.1, 44, TEXT, TITLE_FONT)


def limit_item(n):
    return left_text(LIST_TXT[n], LIM_X, LIST_Y[n], 26, TEXT, line_spacing=0.9)


def mark(item):
    return SurroundingRectangle(item, color=GOLD, buff=0.1, corner_radius=0.1, stroke_width=3)


S20_K = 1.9
S20_AX, S20_BX, S20_BASE = 2.4, 4.2, -2.3


def s20_bars(ha, hb):
    return (vbar(S20_AX, S20_BASE, ha * S20_K, PURPLE, 1.1), vbar(S20_BX, S20_BASE, hb * S20_K, PURPLE, 1.1))


class S20(SpokenScene):
    def construct(self):
        title, item1 = limits_title(), limit_item(1)
        ba, bb = s20_bars(1.331, 0.729)
        la, lb = T("A", 28, TEXT).move_to(P(S20_AX, S20_BASE - 0.4)), T("B", 28, TEXT).move_to(P(S20_BX, S20_BASE - 0.4))
        rule = T("the rule", 28, TEXT).move_to(P(3.3, 0.9))
        q = T("?", 100, GOLD, weight=BOLD)
        y1, y2 = S20_BASE + 1.1 * S20_K, S20_BASE + 0.9 * S20_K
        br = VGroup(DoubleArrow(P(5.4, y2), P(5.4, y1), buff=0, color=GOLD, stroke_width=5, tip_length=0.14),
                    DashedLine(P(S20_AX + 0.55, y1), P(5.4, y1), color=GOLD, stroke_width=2),
                    DashedLine(P(S20_BX + 0.55, y2), P(5.4, y2), color=GOLD, stroke_width=2))
        q.move_to(P(6.2, (y1 + y2) / 2))

        self.play(GrowFromEdge(ba, DOWN), GrowFromEdge(bb, DOWN), FadeIn(la), FadeIn(lb), FadeIn(rule), run_time=0.8)
        self.at("has limits")
        self.play(FadeIn(title, shift=RIGHT * 0.2), run_time=0.6)
        self.at("does not say where")
        self.play(FadeIn(item1, shift=UP * 0.1), run_time=0.7)
        self.at("first small lead")
        self.play(Transform(ba, s20_bars(1.1, 0.9)[0]), Transform(bb, s20_bars(1.1, 0.9)[1]), FadeIn(br), run_time=1.0)
        self.at("comes from")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S21(SpokenScene):
    def construct(self):
        CXS = [-5.0, -1.5, 2.0]

        def panel(cx, kind):
            yA, yB = 1.35, -0.8
            A = soma(P(cx - 1.2, yA), BLUE, 0.34)
            B = soma(P(cx - 1.2, yB), BLUE, 0.34)
            tb = box(cx + 1.2, 0.2, 0.9, 3.9, GREY, 0.12, 0.15)
            hl = halo(P(cx - 1.2, yA), 0.52)
            if kind == "early":
                ax = [Line(P(cx - 0.85, yA), P(cx + 0.75, yA), color=GREY, stroke_width=5),
                      Line(P(cx - 0.85, yB), P(cx - 0.1, yB), color=GREY, stroke_width=5)]
            elif kind == "branch":
                ax = [Line(P(cx - 0.85, yA), P(cx - 0.1, yA), color=GREY, stroke_width=5),
                      Line(P(cx - 0.1, yA), P(cx + 0.75, yA + 0.8), color=GREY, stroke_width=5),
                      Line(P(cx - 0.1, yA), P(cx + 0.75, yA), color=GREY, stroke_width=5),
                      Line(P(cx - 0.1, yA), P(cx + 0.75, yA - 0.8), color=GREY, stroke_width=5),
                      Line(P(cx - 0.85, yB), P(cx + 0.75, yB), color=GREY, stroke_width=5)]
            else:
                A.move_to(P(cx + 0.05, yA))
                hl.move_to(P(cx + 0.05, yA))
                ax = [Line(P(cx + 0.4, yA), P(cx + 0.75, yA), color=GREY, stroke_width=5),
                      Line(P(cx - 0.85, yB), P(cx + 0.75, yB), color=GREY, stroke_width=5)]
            for a in ax:
                a.set_z_index(1)
            return VGroup(tb, A, B), VGroup(*ax), hl

        names = [("early", "arriving early"), ("branch", "branching more"), ("close", "sitting closer")]
        built = [panel(CXS[k], kind) + (T(nm, 28, TEXT).move_to(P(CXS[k], -2.65)),) for k, (kind, nm) in enumerate(names)]
        sketches = VGroup(*[m for g in built for m in g])

        # right side: the rule amplifies the lead into a tall-short pair
        K, base = 2.4, -2.4
        bx_a, bx_b = 3.7, 5.3

        def bars(ha, hb):
            return vbar(bx_a, base, ha * K, PURPLE, 1.1), vbar(bx_b, base, hb * K, PURPLE, 1.1)
        b0 = bars(1.1, 0.9)
        b1 = bars(1.331, 0.729)
        bl = VGroup(T("A", 28, TEXT).move_to(P(bx_a, base - 0.4)), T("B", 28, TEXT).move_to(P(bx_b, base - 0.4)))
        arrow = arr(P(-0.5, -0.5), P(2.6, -0.5), GOLD, 8, 0.3)
        alab = T("amplified", 32, GOLD).move_to(P(1.05, 0.1))

        def show(i, rt):
            fixed, axons, hl, lab = built[i]
            self.play(FadeIn(fixed, scale=0.9), FadeIn(lab, shift=UP * 0.1), run_time=0.3)
            self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.2), FadeIn(hl), run_time=rt)

        self.at("Arriving early")
        show(0, 0.5)
        self.at("branching more")
        show(1, 0.5)
        self.at("sitting closer")
        show(2, 0.5)
        self.at("all candidates")
        self.play(Indicate(VGroup(*[b[2] for b in built]), color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("The rule amplifies")
        # shrink the sketches to a thumbnail strip on the left and bring in the bars
        labs = VGroup(*[b[3] for b in built])
        thumb = VGroup(*[VGroup(b[0], b[1], b[2]) for b in built])
        self.play(FadeOut(labs), thumb.animate.scale(0.6).move_to(P(-3.6, 0.2)), run_time=0.8)
        self.at("amplifies")
        self.play(*[GrowFromEdge(b, DOWN) for b in b0], FadeIn(bl), GrowArrow(arrow), FadeIn(alab, shift=UP * 0.1), run_time=0.6)
        self.at("head start")
        self.play(Transform(b0[0], b1[0]), Transform(b0[1], b1[1]), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S22(SpokenScene):
    def construct(self):
        title, item1 = limits_title(), limit_item(1)
        item2, item3 = limit_item(2), limit_item(3)
        m2 = mark(item2)
        self.add(title, item1)
        # panel 2: bars A and B, equal top-up
        K, base = 1.0, -2.45
        ax_, bx_ = 0.5, 2.1

        def bars(ha, hb):
            return vbar(ax_, base, ha * K, PURPLE, 1.3), vbar(bx_, base, hb * K, PURPLE, 1.3)
        ba, bb = bars(2.8, 1.4)
        ab = VGroup(T("A", 30, TEXT).move_to(P(ax_, base - 0.4)), T("B", 30, TEXT).move_to(P(bx_, base - 0.4)))
        base_ln = Line(P(-0.4, base), P(3.0, base), color=GREY, stroke_width=3)
        rule_chip = chip("faster than in proportion", PURPLE, 28).move_to(P(2.2, 3.35))
        need = T("needed,", 32, GREEN).move_to(P(0.6, 2.45))
        notenough = T("not enough", 32, GOLD).move_to(P(3.0, 2.45))
        basal = chip("steady basal synthesis", GREY, 28).move_to(P(4.2, 1.45))
        ghosts = VGroup(*[Rectangle(width=1.3, height=1.2, stroke_color=TEXT, stroke_width=3, fill_color=PURPLE, fill_opacity=0.4)
                          .move_to(P(x, base + h * K + 0.6)) for x, h in ((ax_, 2.8), (bx_, 1.4))])
        ghosts[0].set_stroke(TEXT, 3)
        topup = T("same top-up for both", 28, TEXT).move_to(P(4.5, 0.55))
        l_a = Line(P(2.55, 0.62), P(1.2, base + 2.8 + 0.6), color=GREY, stroke_width=2.5)
        l_b = Line(P(2.8, 0.45), P(2.75, base + 1.4 + 0.6), color=GREY, stroke_width=2.5)
        r_a = T("A is 2× B", 32, GOLD).move_to(P(4.4, -1.2))
        r_b = T("A is 1.5× B", 32, GOLD).move_to(P(4.4, -1.2))
        # panel 3: one cell, several factors
        cell = soma(P(3.7, 0.2), BLUE, 1.0, 0.85)
        cell_lab = T("chick motor neuron", 30, TEXT).move_to(P(3.7, -1.55))
        fch = [chip(f"factor {k + 1}", TEXT, 28, 0.16, 0.1).move_to(P(0.0, y)) for k, y in enumerate((1.9, 0.2, -1.5))]
        fa = [arr(P(1.0, y), P(2.65, 0.2 + (y - 0.2) * 0.3), TEXT, 5, 0.22) for y in (1.9, 0.2, -1.5)]

        self.play(FadeIn(item2, shift=UP * 0.1), Create(m2), FadeIn(rule_chip), GrowFromEdge(ba, DOWN), GrowFromEdge(bb, DOWN),
                  FadeIn(ab), FadeIn(base_ln), run_time=0.9)
        self.at("needed")
        self.play(FadeIn(need, shift=UP * 0.1), run_time=0.5)
        self.at("not enough")
        self.play(FadeIn(notenough, shift=UP * 0.1), run_time=0.5)
        self.at("basal synthesis")
        self.play(FadeIn(basal, shift=LEFT * 0.2), FadeIn(r_a, shift=UP * 0.1), run_time=0.7)
        self.at("pulls neurons back")
        nb = bars(2.8 + 1.2, 1.4 + 1.2)
        self.play(Transform(ba, nb[0]), Transform(bb, nb[1]), FadeIn(ghosts), FadeIn(topup), Create(l_a), Create(l_b),
                  run_time=1.2)
        self.at("back together")
        self.play(Transform(r_a, r_b), run_time=0.5)
        self.at("And the rule does not")
        m3 = mark(item3)
        self.play(FadeIn(item3, shift=UP * 0.1), Transform(m2, m3), run_time=0.7)
        self.at("chick motor neurons")
        panel2 = VGroup(ba, bb, ab, base_ln, rule_chip, need, notenough, basal, ghosts, topup, l_a, l_b, r_a)
        self.play(FadeOut(panel2), FadeIn(cell, scale=0.6), FadeIn(cell_lab), run_time=0.8)
        self.at("several factors")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c, shift=RIGHT * 0.2), GrowArrow(a)) for c, a in zip(fch, fa)],
                              lag_ratio=0.25), run_time=1.0)
        self.at("at once")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23(SpokenScene):
    def construct(self):
        head = T("Takeaway", 40, GOLD, font=TITLE_FONT).move_to(P(0, 3.4))
        cardL = box(-3.45, 0.2, 6.2, 5.4, GREY, 0.05, 0.3, 2)
        cardR = box(3.45, 0.2, 6.2, 5.4, GREY, 0.05, 0.3, 2)
        # left: the supply sets how many
        tb = box(-3.45, 1.9, 3.8, 1.0, GREY, 0.14, 0.2)
        tl = T("target", 28, TEXT).move_to(P(-3.45, 1.9))
        dts = VGroup(*[ngf_dot(P(-3.45 + dx, 1.15), 0.12) for dx in (-0.45, 0, 0.45)])
        xs = np.linspace(-5.85, -1.05, 8)
        row = VGroup(*[soma(P(x, 0.1), BLUE, 0.3) for x in xs])
        cap1 = T("A limited supply sets\nroughly how many survive.", 34, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to(P(-3.45, -1.45))
        # right: the neurons' own feedback decides which
        big = soma(P(3.45, 0.85), BLUE, 0.85, 0.9)
        loop = Arc(radius=1.5, start_angle=PI * 0.3, angle=PI * 1.5, arc_center=P(3.45, 0.85), stroke_color=PURPLE, stroke_width=8)
        loop.add_tip(tip_length=0.3)
        cap2 = T("The neurons’ own feedback\ndecides which ones.", 34, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to(P(3.45, -1.45))
        keep = [0, 2, 5, 7]

        big.set_opacity(0.22)
        self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(cardL), FadeIn(cardR), FadeIn(big), run_time=0.7)
        self.at("A limited supply")
        self.play(FadeIn(tb), FadeIn(tl), LaggedStart(*[FadeIn(x, scale=0.3) for x in dts], lag_ratio=0.2),
                  FadeIn(row), FadeIn(cap1, shift=UP * 0.1), run_time=1.2)
        self.at("how many survive")
        self.play(*[to_state(row[i], GREEN, 0.9) if i in keep else to_state(row[i], RED, 0.3) for i in range(8)], run_time=0.8)
        self.at("the neuron's")
        self.play(big.animate.set_opacity(0.9), FadeIn(cap2, shift=UP * 0.1), run_time=0.7)
        self.at("own feedback")
        self.play(Create(loop), run_time=0.9)
        self.at("decides which")
        self.play(to_state(big, GREEN, 0.9), run_time=0.7)
        self.finish()


class S24End(EndCard):
    LINE = "Limited supply sets roughly how many survive;\nneurons’ own feedback decides which."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT, line_spacing=1.25)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
