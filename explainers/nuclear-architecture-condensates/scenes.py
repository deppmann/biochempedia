"""Nuclear architecture and membraneless compartments: change the amount, watch the bodies.

COLOR MAP (one color per concept, whole video)
  BLUE   = the protein (dots) and the dense bodies it forms
  PURPLE = chromatin: chromosome territories, binding sites, the bead chain
  TEAL   = the phase-separation hypothesis and its prediction
  YELLOW = the saturation concentration (the threshold)
  GREEN  = protein A (fits the prediction)
  ORANGE = protein B (does not fit it)
  RED    = a problem: the missing membrane, "cannot tell"
  GREY   = nucleus outline, axes, de-emphasized things
  TEXT   = neutral marks (the total on the plot, the amount arrow)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

C_SAT, C_DENSE = 1.0, 50.0


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def nucleus(c, r):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to(c)


def pdot(p, color=BLUE, r=0.075):
    return Dot(p, radius=r, color=color)


def ring_points(n, c, r_in, r_out, seed, gap=0.3):
    """n points in an annulus around c, kept at least `gap` apart."""
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        a = rng.uniform(0, TAU)
        r = np.sqrt(rng.uniform(r_in ** 2, r_out ** 2))
        p = np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])
        if all(np.linalg.norm(p - q) > gap for q in pts):
            pts.append(p)
    return pts


def cluster_points(n, c, step=0.15):
    """golden-spiral packing: a tight round cluster of n points."""
    return [np.array([c[0] + step * np.sqrt(k + 0.5) * np.cos(k * 2.4),
                      c[1] + step * np.sqrt(k + 0.5) * np.sin(k * 2.4), 0]) for k in range(n)]


def phi_of(total):
    return max(0.0, (total - C_SAT) / (C_DENSE - C_SAT))


def body(c, R, phi, **kw):
    return Circle(radius=max(R * np.sqrt(phi), 0.001), stroke_color=BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.55).move_to(c)


# the concentration plot used in scenes 3, 5 (same place both times)
O = np.array([-5.0, -2.5, 0.0])
U = 0.62   # scene units per micromolar


def P(x, y):
    return O + np.array([x * U, y * U, 0])


def make_axes():
    g = VGroup()
    g.add(Line(P(0, 0), P(8.4, 0), color=GREY, stroke_width=3), Line(P(0, 0), P(0, 8.2), color=GREY, stroke_width=3))
    for v in (2, 4, 6, 8):
        g.add(Line(P(v, 0), P(v, 0) + DOWN * 0.1, color=GREY, stroke_width=2),
              M(str(v), 22, GREY).move_to(P(v, 0) + DOWN * 0.34))
        g.add(Line(P(0, v), P(0, v) + LEFT * 0.1, color=GREY, stroke_width=2),
              M(str(v), 22, GREY).move_to(P(0, v) + LEFT * 0.34))
    g.add(T("total protein, µM", 24, TEXT).move_to(P(4.2, 0) + DOWN * 0.75))
    yl = T("protein outside the bodies, µM", 24, TEXT).rotate(PI / 2).move_to(P(0, 4.1) + LEFT * 0.95)
    g.add(yl)
    return g


def model_curve(upto=8.0):
    pts = [P(0, 0), P(C_SAT, C_SAT)] + ([P(upto, C_SAT)] if upto > C_SAT else [])
    if upto <= C_SAT:
        pts = [P(0, 0), P(upto, upto)]
    m = VMobject(stroke_color=TEAL, stroke_width=6)
    m.set_points_as_corners(pts)
    return m


def out_of(t):
    return min(t, C_SAT)


class S00Title(TitleCard):
    LESSON = "Nuclear architecture and membraneless compartments"
    TITLE = "Change the amount, watch the bodies"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a nucleus with territories and bodies; no membrane inside; what holds it apart?; phase separation."""

    def construct(self):
        C = np.array([-2.7, -0.1, 0.0])
        R = 3.15
        nuc = nucleus(C, R)
        terr_spec = [((-1.1, 1.0), 2.5, 1.9, 20), ((1.1, 0.95), 2.2, 2.0, -15),
                     ((-1.2, -1.2), 2.4, 1.8, -10), ((1.15, -1.15), 2.3, 1.9, 15)]
        terrs = VGroup(*[Ellipse(width=w, height=h, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                                 fill_opacity=0.22).rotate(a * DEGREES).move_to(C + np.array([x, y, 0]))
                         for (x, y), w, h, a in terr_spec])
        nucleolus = Circle(radius=0.42, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55).move_to(C + [0.0, 0.0, 0])
        speck = VGroup(*[Circle(radius=0.17, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.55).move_to(C + np.array(p + (0,)))
                         for p in [(-0.05, 1.95), (-2.05, 0.05), (2.0, 0.15), (0.1, -2.0)]])

        # right column
        X = 3.7
        ml = Rectangle(width=0.9, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        mt = T("a membrane", 26, GREY)
        mem = VGroup(ml, mt).arrange(RIGHT, buff=0.3).move_to([X, 2.3, 0])
        strike = VGroup(Line(ml.get_corner(UL) + UL * 0.08, ml.get_corner(DR) + DR * 0.08, color=RED, stroke_width=6), Line(ml.get_corner(DL) + DL * 0.08, ml.get_corner(UR) + UR * 0.08, color=RED, stroke_width=6))
        nomem = T("none inside", 26, RED).next_to(mem, DOWN, buff=0.2)

        sw_t = Square(0.32, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3)
        row_t = VGroup(sw_t, T("each chromosome: its own region", 24, PURPLE)).arrange(RIGHT, buff=0.3)
        row_n = VGroup(Circle(radius=0.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55),
                       T("nucleolus: ribosomes built", 24, BLUE)).arrange(RIGHT, buff=0.3)
        row_s = VGroup(Circle(radius=0.12, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.55),
                       T("speckles: splicing factors", 24, BLUE)).arrange(RIGHT, buff=0.3)
        rows = VGroup(row_t, row_n, row_s).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([X + 0.1, 0.5, 0])
        q = T("What holds things apart?", 32, TEXT, weight=BOLD).move_to([X, -1.9, 0])
        prop = chip("phase separation?", TEAL, 30).move_to([X, -2.9, 0])

        self.play(Create(nuc), run_time=0.9)
        self.at("no membranes")
        self.play(FadeIn(mem), run_time=0.4)
        self.play(Create(strike), FadeIn(nomem), run_time=0.5)
        self.at("its own region")
        self.play(LaggedStart(*[FadeIn(t, scale=0.9) for t in terrs], lag_ratio=0.2), FadeIn(row_t), run_time=1.3)
        self.at("Ribosomes are assembled")
        self.play(GrowFromCenter(nucleolus), FadeIn(row_n), run_time=0.7)
        self.at("splicing factors")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in speck], lag_ratio=0.15), FadeIn(row_s), run_time=0.8)
        self.at("no walls")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.play(Wiggle(strike, scale_value=1.1, rotation_angle=0.02 * TAU), run_time=0.7)
        self.at("phase separation")
        self.play(FadeIn(prop, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Three(SpokenScene):
    """three ways to make a bright spot; all look the same; they differ when the amount changes."""

    def construct(self):
        cxs = [-4.2, 0.0, 4.2]
        cy, R = 0.9, 1.95
        nucs = [nucleus(np.array([x, cy, 0]), R) for x in cxs]
        labs = [T("phase separation", 26, TEAL), T("binding clustered sites", 26, PURPLE), T("bridging chromatin", 26, PURPLE)]
        for l, x in zip(labs, cxs):
            l.move_to([x, cy - R - 0.4, 0])

        # panel 1: dots demix into a drop
        c1 = np.array([cxs[0], cy, 0])
        start1 = ring_points(20, c1, 0.0, R - 0.3, 3, gap=0.3)
        tgt1 = cluster_points(14, c1 + np.array([0.25, 0.2, 0]), 0.14)
        d1 = VGroup(*[pdot(p) for p in start1])
        # panel 2: dots pile onto a cluster of sites on a DNA line
        c2 = np.array([cxs[1], cy, 0])
        line2 = Line(c2 + LEFT * (R - 0.15), c2 + RIGHT * (R - 0.15), color=PURPLE, stroke_width=4)
        sites = VGroup(*[Square(0.17, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9).move_to(c2 + np.array([0.28 + 0.2 * (k - 2), 0, 0]))
                         for k in range(5)])
        start2 = ring_points(12, c2 + np.array([0, 0.0, 0]), 0.0, R - 0.3, 5, gap=0.32)
        start2 = [p for p in start2 if abs(p[1] - c2[1]) > 0.22][:10]
        d2 = VGroup(*[pdot(p) for p in start2])
        tgt2 = [c2 + np.array([0.28 + 0.2 * (k - 2), 0.2 + 0.0, 0]) for k in range(5)] + \
               [c2 + np.array([0.28 + 0.2 * (k - 2), -0.2, 0]) for k in range(4)]
        # panel 3: bead chain collapses
        c3 = np.array([cxs[2], cy, 0])
        xs = np.linspace(-R + 0.3, R - 0.3, 14)
        beads_start = [c3 + np.array([x, 0.45 * np.sin(1.7 * x + 0.5), 0]) for x in xs]
        beads_end = cluster_points(14, c3, 0.13)
        beads = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p) for p in beads_start])
        chain = VMobject(stroke_color=PURPLE, stroke_width=3)
        chain.set_points_as_corners(beads_start)
        bridge = VGroup(*[pdot(beads_start[i] + np.array([0, 0.15, 0])) for i in (3, 7, 10)])

        self.at("A bright spot")
        self.play(*[Create(n) for n in nucs], run_time=0.8)
        self.play(FadeIn(d1), FadeIn(line2), FadeIn(sites), FadeIn(d2), FadeIn(chain), FadeIn(beads), FadeIn(bridge), run_time=0.6)

        self.at("phase separation")
        self.play(FadeIn(labs[0]), run_time=0.3)
        self.play(*[d1[k].animate.move_to(tgt1[k]) for k in range(14)], run_time=1.6)
        halo1 = Circle(radius=0.62, stroke_width=0, fill_color=BLUE, fill_opacity=0.0).move_to(c1 + np.array([0.25, 0.2, 0]))

        self.at("clustered sites")
        self.play(FadeIn(labs[1]), run_time=0.3)
        self.play(*[d2[k].animate.move_to(tgt2[k]) for k in range(min(len(d2), len(tgt2)))], run_time=1.6)

        self.at("bridge chromatin")
        self.play(FadeIn(labs[2]), run_time=0.3)
        self.play(*[beads[k].animate.move_to(beads_end[k]) for k in range(14)],
                  Transform(chain, VMobject(stroke_color=PURPLE, stroke_width=3).set_points_as_corners(beads_end)),
                  *[bridge[j].animate.move_to(beads_end[i]) for j, i in enumerate((3, 7, 10))], run_time=1.8)

        self.at("All three make")
        halos = [Circle(radius=0.65, stroke_width=0, fill_color=BLUE, fill_opacity=0.28).move_to(p)
                 for p in (c1 + np.array([0.25, 0.2, 0]), c2 + np.array([0.28, 0.0, 0]), c3)]
        self.play(*[FadeIn(h, scale=0.5) for h in halos], run_time=0.8)
        self.play(*[Indicate(h, color=BLUE, scale_factor=1.15) for h in halos], run_time=0.9)

        self.at("change the amount")
        arrow = Arrow(LEFT * 3.2, RIGHT * 3.2, color=TEXT, stroke_width=6, buff=0).move_to([0, -3.1, 0])
        al = T("change the amount of protein", 26, TEXT).next_to(arrow, UP, buff=0.12)
        self.play(GrowArrow(arrow), FadeIn(al), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Threshold(SpokenScene):
    """plot of protein outside vs total: the curve rises to the threshold and goes flat while a drop grows."""

    def construct(self):
        axes = make_axes()
        Cn = np.array([3.5, 0.0, 0.0])
        Rn = 2.55
        nuc = nucleus(Cn, Rn)
        dots_pos = ring_points(8, Cn, 1.2, Rn - 0.25, 11, gap=0.42)
        t = ValueTracker(0.0)

        def curve():
            return model_curve(max(t.get_value(), 0.001))

        def marker():
            x = t.get_value()
            return Dot(P(x, out_of(x)), radius=0.11, color=TEXT)

        def drop():
            ph = phi_of(t.get_value())
            if ph <= 0.0005:
                return VGroup()
            return body(Cn, Rn, ph)

        def dots():
            n = int(round(out_of(t.get_value()) * 8))
            return VGroup(*[pdot(p) for p in dots_pos[:n]])

        cv = always_redraw(curve)
        mk = always_redraw(marker)
        dr = always_redraw(drop)
        ds = always_redraw(dots)

        thr = DashedLine(P(0, C_SAT), P(8.4, C_SAT), color=YELLOW, stroke_width=3)
        thr_lbl = T("saturation concentration", 22, YELLOW).move_to(P(3.9, C_SAT) + UP * 0.42)

        self.at("predicts a threshold")
        self.play(FadeIn(axes), Create(nuc), run_time=1.0)
        self.play(Create(thr), FadeIn(thr_lbl), run_time=0.7)
        self.add(cv, mk, dr, ds)

        self.at("no bodies form")
        self.play(t.animate.set_value(C_SAT), run_time=1.6, rate_func=linear)
        self.wait(0.4)
        self.at("extra protein goes")
        self.play(t.animate.set_value(8.0), run_time=3.6, rate_func=linear)

        self.at("stays at the threshold")
        flat = Line(P(2, C_SAT), P(7.5, C_SAT), color=TEAL, stroke_width=10)
        self.play(Indicate(flat, color=TEAL, scale_factor=1.0), run_time=0.9)
        self.at("buffered dilute phase")
        chp = chip("buffered dilute phase", TEAL, 26).move_to(P(5.2, 3.4))
        ar = Arrow(chp.get_bottom() + RIGHT * 1.0, P(7.2, C_SAT) + UP * 0.12, color=TEAL, stroke_width=4, buff=0.1)
        self.play(FadeIn(chp, shift=UP * 0.1), GrowArrow(ar), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Numbers(SpokenScene):
    """mass balance: with c_dense 50 and c_sat 1, bodies fill 2.0, 6.1, 14.3 percent at totals 2, 4, 8."""

    def construct(self):
        a1 = chip("dense phase 50 µM", BLUE, 26)
        a2 = chip("saturation concentration 1 µM", YELLOW, 26)
        top = VGroup(a1, a2).arrange(RIGHT, buff=0.6).move_to([0, 3.1, 0])
        eq = M("fraction of volume = (total - c_sat) / (c_dense - c_sat)", 26, TEXT)
        fit(eq, max_w=11.8)
        eq.move_to([0, 2.3, 0])

        cxs = [-4.3, 0.0, 4.3]
        cy, R = -0.1, 1.4
        totals = [2, 4, 8]
        phis = [phi_of(v) for v in totals]
        pct = ["2.0", "6.1", "14.3"]
        nucs, bodies, heads, foots, dotgs = [], [], [], [], []
        for x, v, ph, pc in zip(cxs, totals, phis, pct):
            c = np.array([x, cy, 0])
            nucs.append(nucleus(c, R))
            bodies.append(body(c, R, ph))
            heads.append(T(f"total {v} µM", 26, TEXT).move_to([x, cy + R + 0.4, 0]))
            foots.append(T(f"bodies {pc}%", 26, BLUE, weight=BOLD).move_to([x, cy - R - 0.4, 0]))
            dotgs.append(VGroup(*[pdot(p) for p in ring_points(8, c, 0.75, R - 0.2, 21, gap=0.3)]))
        outs = [T("outside near 1 µM", 24, YELLOW).move_to([x, cy - R - 0.95, 0]) for x in cxs]

        self.at("Assume one dense")
        self.play(FadeIn(a1, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(a2, shift=DOWN * 0.15), run_time=0.5)
        self.at("mass balance")
        self.play(Write(eq), run_time=1.6)
        self.at("At totals of")
        self.play(*[Create(n) for n in nucs], *[FadeIn(h) for h in heads], *[FadeIn(d) for d in dotgs], run_time=0.9)
        self.at("bodies fill")
        for b, f in zip(bodies, foots):
            self.play(GrowFromCenter(b), FadeIn(f, shift=UP * 0.1), run_time=0.7)
        self.at("The bodies grow")
        self.play(*[Indicate(b, color=BLUE, scale_factor=1.15) for b in bodies], run_time=0.9)
        br = Arrow([-4.3, -3.2, 0], [4.3, -3.2, 0], buff=0, color=TEXT, stroke_width=4)
        sev = T("bodies grow sevenfold", 28, TEXT, weight=BOLD).move_to([0, -3.2, 0])
        sev_back = Rectangle(width=sev.width + 0.4, height=sev.height + 0.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(sev)
        self.play(GrowArrow(br), FadeIn(sev_back), FadeIn(sev), run_time=0.7)
        self.at("stays near")
        self.play(*[FadeIn(o, shift=UP * 0.1) for o in outs], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Two(SpokenScene):
    """protein A sits on the flat prediction; protein B climbs along a line through the origin."""

    def construct(self):
        axes = make_axes()
        thr = DashedLine(P(0, C_SAT), P(8.4, C_SAT), color=YELLOW, stroke_width=3)
        pred = model_curve(8.0)
        pred_l = T("prediction", 24, TEAL).move_to(P(6.0, C_SAT) + UP * 0.4)
        self.add(axes, thr)

        totals = [2, 4, 8]
        A = [1.0, 1.0, 1.1]
        B = [1.5, 2.8, 5.9]
        ptsA = [Dot(P(x, y), radius=0.12, color=GREEN) for x, y in zip(totals, A)]
        ptsB = [Dot(P(x, y), radius=0.12, color=ORANGE) for x, y in zip(totals, B)]
        lineB = VMobject(stroke_color=ORANGE, stroke_width=3).set_points_as_corners([P(x, y) for x, y in zip(totals, B)])

        X = 3.4
        hA = chip("protein A", GREEN, 28).move_to([X - 1.2, 2.55, 0])
        dA = M("1.0, 1.0, 1.1 µM", 26, GREEN).next_to(hA, DOWN, buff=0.25).align_to(hA, LEFT)
        vA = T("fits the prediction", 26, GREEN).next_to(dA, DOWN, buff=0.2).align_to(hA, LEFT)
        hB = chip("protein B", ORANGE, 28).move_to([X - 1.2, -0.05, 0])
        dB = M("1.5, 2.8, 5.9 µM", 26, ORANGE).next_to(hB, DOWN, buff=0.25).align_to(hB, LEFT)
        fr = VGroup(*[M(s, 26, ORANGE) for s in ("1.5/2 = 0.75", "2.8/4 = 0.70", "5.9/8 = 0.74")])
        fr.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(dB, DOWN, buff=0.2).align_to(hB, LEFT)
        vB = T("fits binding sites better", 26, ORANGE).next_to(fr, DOWN, buff=0.25).align_to(hB, LEFT)
        dash = DashedLine(P(0, 0), P(8, 5.9), color=ORANGE, stroke_width=3)

        self.at("test two proteins")
        self.play(Create(pred), FadeIn(pred_l), run_time=1.0)
        self.at("protein A")
        self.play(FadeIn(hA, shift=DOWN * 0.1), run_time=0.4)
        self.play(*[FadeIn(p, scale=0.4) for p in ptsA], FadeIn(dA), run_time=0.9)
        self.at("That fits")
        self.play(FadeIn(vA, shift=UP * 0.1), run_time=0.5)
        self.at("For protein B")
        self.play(FadeIn(hB, shift=DOWN * 0.1), run_time=0.4)
        self.play(*[FadeIn(p, scale=0.4) for p in ptsB], Create(lineB), FadeIn(dB), run_time=1.0)
        self.at("Divide by the totals")
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in fr], lag_ratio=0.5), run_time=1.7)
        self.at("constant fraction")
        self.play(Create(dash), run_time=0.9)
        self.at("binding sites better")
        self.play(FadeIn(vB, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """four observations cannot tell the models apart; two cautions; the rule: change the amount, measure inside and outside."""

    def construct(self):
        names = ["round shapes", "fusion", "fluorescence recovery", "hexanediol"]
        pos = [(-3.2, 1.6), (3.2, 1.6), (-3.2, 0.0), (3.2, 0.0)]
        chips = VGroup(*[chip(n, TEXT, 40).move_to([x, y, 0]) for n, (x, y) in zip(names, pos)])
        verdict = T("cannot tell the models apart", 44, RED, weight=BOLD).move_to([0, -1.8, 0])
        crosses = VGroup(*[Line(c.get_left() + LEFT * 0.1, c.get_right() + RIGHT * 0.1, color=RED, stroke_width=5) for c in chips])

        fails = VGroup(RoundedRectangle(corner_radius=0.2, width=5.8, height=3.0, stroke_color=ORANGE, stroke_width=3),
                       T("a protein that fails", 32, ORANGE, weight=BOLD),
                       T("may still phase separate,\nas one part of a mixture", 28, TEXT, line_spacing=0.9))
        fails[1].move_to(fails[0].get_center() + UP * 0.8)
        fails[2].move_to(fails[0].get_center() + DOWN * 0.45)
        fails.move_to([-3.3, 0.5, 0])
        passes = VGroup(RoundedRectangle(corner_radius=0.2, width=5.8, height=3.0, stroke_color=GREEN, stroke_width=3),
                        T("a protein that passes", 32, GREEN, weight=BOLD),
                        T("has not been shown\nto need its body", 28, TEXT, line_spacing=0.9))
        passes[1].move_to(passes[0].get_center() + UP * 0.8)
        passes[2].move_to(passes[0].get_center() + DOWN * 0.45)
        passes.move_to([3.3, 0.5, 0])

        self.at("Round shapes")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.25), run_time=1.6)
        self.at("cannot tell")
        self.play(LaggedStart(*[Create(x) for x in crosses], lag_ratio=0.15), FadeIn(verdict), run_time=1.2)
        self.at("Treat the result")
        self.play(FadeOut(chips), FadeOut(crosses), FadeOut(verdict), run_time=0.6)
        self.at("that fails")
        self.play(FadeIn(fails, shift=RIGHT * 0.2), run_time=0.7)
        self.at("that passes")
        self.play(FadeIn(passes, shift=LEFT * 0.2), run_time=0.7)

        # the rule: three nuclei at rising amounts, measured inside and outside
        cxs = [-4.3, 0.0, 4.3]
        cy, R = 0.5, 1.6
        totals = [2, 4, 8]
        nucs, bods, dgs = [], [], []
        for x, v in zip(cxs, totals):
            c = np.array([x, cy, 0])
            nucs.append(nucleus(c, R))
            bods.append(body(c, R, phi_of(v)))
            dgs.append(VGroup(*[pdot(p) for p in ring_points(8, c, 0.8, R - 0.2, 21, gap=0.3)]))
        arrow = Arrow(LEFT * 3.2, RIGHT * 3.2, color=TEXT, stroke_width=6, buff=0).move_to([0, -2.0, 0])
        al = T("change the amount of protein", 26, TEXT).next_to(arrow, UP, buff=0.12)
        ins = T("inside", 26, BLUE, weight=BOLD)
        outs = T("outside", 26, YELLOW, weight=BOLD)
        self.at("So change the amount")
        self.play(FadeOut(fails), FadeOut(passes), run_time=0.5)
        self.play(*[Create(n) for n in nucs], *[FadeIn(d) for d in dgs], run_time=0.7)
        self.play(*[GrowFromCenter(b) for b in bods], GrowArrow(arrow), FadeIn(al), run_time=0.9)
        self.at("measure inside")
        # labels on the third nucleus
        c3 = np.array([cxs[2], cy, 0])
        ins.move_to(c3 + np.array([-0.25, R + 0.4, 0]))
        l_in = Line(ins.get_bottom() + DOWN * 0.05, bods[2].get_top() + LEFT * 0.0, color=BLUE, stroke_width=3)
        self.play(FadeIn(ins), Create(l_in), run_time=0.6)
        self.at("outside the bodies")
        low = min(dgs[2], key=lambda d: d.get_center()[1])
        outs.move_to([cxs[2] + 1.0, cy - R - 0.4, 0])
        l_out = Line(outs.get_top() + UP * 0.05, low.get_center(), color=YELLOW, stroke_width=3)
        self.play(FadeIn(outs), Create(l_out), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Change the amount, then measure inside and outside the bodies."
