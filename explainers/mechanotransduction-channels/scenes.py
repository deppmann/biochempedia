"""Flatten the dome, open the pore  (Biochemistrypedia explainer, Sensory Systems)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the Piezo channel (a labelled schematic cap, never a structure)
  GREY   = membrane bars, outlines, de-emphasized labels
  YELLOW = force / membrane tension
  PURPLE = projected area (the bracket under the cap)
  GREEN  = pore open / sufficient / the computed answer
  RED    = pore closed / a hedge
  ORANGE = the proposed cadherin and actin tether
  GOLD   = title rule only
All drawings of the channel are side-view schematics and are captioned as such.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

L_CAP = 5.4          # fixed length of the cap in this 2D schematic (its surface area stays fixed)
TH0 = 1.239          # half-angle of the curved cap: gives a width:depth ratio of 28:10
SC = 1.6


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cap_pts(theta, sc=SC, cx=0.0, y0=0.0):
    th = max(float(theta), 1e-3)
    R = L_CAP / (2 * th)
    phis = np.linspace(-th, th, 70)
    return [np.array([cx + sc * R * np.sin(p), y0 + sc * R * (np.cos(p) - np.cos(th)), 0.0]) for p in phis]


def dome(theta, sc=SC, cx=0.0, y0=0.0, half=6.1, w=10):
    """Membrane bar with the Piezo cap in it: flanks in grey, the cap (fixed length) in blue."""
    pts = cap_pts(theta, sc, cx, y0)
    cap = VMobject(stroke_color=BLUE, stroke_width=w, fill_opacity=0).set_points_as_corners(pts)
    xl, xr = pts[0][0], pts[-1][0]
    left = Line([cx - half, y0, 0], [xl, y0, 0], color=GREY, stroke_width=w)
    right = Line([xr, y0, 0], [cx + half, y0, 0], color=GREY, stroke_width=w)
    return VGroup(left, cap, right)


def live_dome(tr, **kw):
    return always_redraw(lambda: dome(tr.get_value(), **kw))


def bracket(tr, y_b, sc=SC, cx=0.0, y0=0.0, color=PURPLE):
    def make():
        pts = cap_pts(tr.get_value(), sc, cx, y0)
        xl, xr = pts[0][0], pts[-1][0]
        d1 = DashedLine([xl, y0 - 0.12, 0], [xl, y_b + 0.1, 0], color=color, stroke_width=3, dash_length=0.1)
        d2 = DashedLine([xr, y0 - 0.12, 0], [xr, y_b + 0.1, 0], color=color, stroke_width=3, dash_length=0.1)
        ar = DoubleArrow([xl, y_b, 0], [xr, y_b, 0], buff=0, color=color, stroke_width=5, tip_length=0.2)
        return VGroup(d1, d2, ar)
    return always_redraw(make)


def static_bracket(theta, y_b, sc, cx, y0, color=PURPLE):
    tr = ValueTracker(theta)
    return bracket(tr, y_b, sc, cx, y0, color)


def pore_chip(is_open, size=28):
    c = chip("pore: open" if is_open else "pore: closed", GREEN if is_open else RED, size=size)
    return c


def force_arrows(y, x_in=3.5, length=2.2, w=7, color=YELLOW):
    a = Arrow([-x_in, y, 0], [-x_in - length, y, 0], buff=0, color=color, stroke_width=w, tip_length=0.28)
    b = Arrow([x_in, y, 0], [x_in + length, y, 0], buff=0, color=color, stroke_width=w, tip_length=0.28)
    return VGroup(a, b)


def note(text="schematic, not a structure", y=-3.3):
    return T(text, 22, GREY).move_to([0, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Piezo channels and the physics of force"
    TITLE = "Flatten the dome, open the pore"


# ---------------------------------------------------------------------------------------------
class S01Dome(SpokenScene):
    def construct(self):
        y0 = -1.2
        th = ValueTracker(0.0)
        q = T("How does a protein turn force into ionic current?", 34, font=TITLE_FONT).to_edge(UP, buff=0.55)
        fit(q)
        mem = live_dome(th, sc=SC, y0=y0)
        self.play(Write(q), FadeIn(mem), run_time=1.6)

        self.at("leading model")
        hedge = chip("a leading model, still debated", RED, size=28).move_to([0, 3.1, 0])
        self.play(FadeOut(q), FadeIn(hedge), run_time=0.6)

        self.at("curved blades")
        lbl = T("Piezo channel\n(purified mouse PIEZO2)", 24, BLUE).move_to([-4.5, 1.0, 0])
        pore = pore_chip(False).move_to([0, 2.0, 0])
        self.play(FadeIn(lbl), FadeIn(pore), th.animate.set_value(TH0), run_time=2.0)
        sch = note(y=-3.3)
        self.play(FadeIn(sch), run_time=0.4)

        self.at("dome is about", lead=-0.6)
        pts = cap_pts(TH0, SC, 0, y0)
        xl, xr = pts[0][0], pts[-1][0]
        by = y0 - 0.7
        br = VGroup(DoubleArrow([xl, by, 0], [xr, by, 0], buff=0, color=PURPLE, stroke_width=5, tip_length=0.2),
                    T("about 28 nm across", 26, PURPLE).move_to([0, by - 0.5, 0]))
        self.play(FadeIn(br), run_time=0.6)

        self.at("Flatten it")
        fa = force_arrows(y0 + 0.5, x_in=4.4, length=1.6)
        fl = T("force", 26, YELLOW).move_to([-5.2, y0 + 1.0, 0])
        self.play(FadeOut(br), FadeIn(fa), FadeIn(fl), th.animate.set_value(0.0), run_time=1.3)
        self.at("pore in")
        self.play(FadeOut(pore), FadeIn(pore_chip(True).move_to(pore)), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Area(SpokenScene):
    def construct(self):
        y0 = -1.2
        th = ValueTracker(TH0)
        mem = live_dome(th, sc=SC, y0=y0)
        side = T("side view, schematic", 22, GREY).to_edge(UP, buff=0.5)
        self.play(FadeIn(mem), FadeIn(side), run_time=0.8)

        self.at("curved cap")
        cap_lbl = chip("cap: fixed surface area", BLUE, size=26).move_to([0, 2.45, 0])
        self.play(FadeIn(cap_lbl, shift=DOWN * 0.1), run_time=0.5)

        self.at("projects less")
        br = bracket(th, y0 - 0.75, sc=SC, y0=y0)
        small = T("projected area: smaller", 26, PURPLE).move_to([0, y0 - 1.35, 0])
        self.play(FadeIn(br), FadeIn(small), run_time=0.7)

        self.at("projects more")
        big = T("projected area: larger", 26, PURPLE).move_to([0, y0 - 1.35, 0])
        self.play(th.animate.set_value(0.0), Transform(small, big), run_time=1.8)

        self.at("flattening increases")
        self.play(Indicate(br, color=PURPLE, scale_factor=1.03), run_time=0.9)

        self.at("the flat state")
        rule = chip("more projected area favours the flat state", GREEN, size=28).move_to([0, -3.15, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tension(SpokenScene):
    def construct(self):
        y0 = -1.2
        th = ValueTracker(TH0)
        mem = live_dome(th, sc=SC, y0=y0)
        pore = pore_chip(False).move_to([0, 2.15, 0])
        self.add(mem, pore)

        self.at("add tension")
        small = force_arrows(y0 + 0.5, x_in=3.5, length=1.2, w=5)
        tl = T("tension in the membrane", 26, YELLOW).move_to([0, -2.7, 0])
        self.play(FadeIn(small), FadeIn(tl), run_time=0.6)

        self.at("lowers the energy")
        e1 = T("larger projected area: lower energy", 28, PURPLE).move_to([0, 3.05, 0])
        self.play(FadeIn(e1, shift=DOWN * 0.1), run_time=0.6)

        self.at("as tension rises")
        big = force_arrows(y0 + 0.5, x_in=4.4, length=1.7, w=10)
        tl2 = T("tension rises", 26, YELLOW).move_to([0, -2.7, 0])
        self.play(Transform(small, big), Transform(tl, tl2), th.animate.set_value(0.0), run_time=2.0)
        self.play(FadeOut(pore), FadeIn(pore_chip(True).move_to(pore)), run_time=0.4)

        self.at("energy change")
        eq = M("energy change = - tension x change in projected area", 26, PURPLE).move_to([0, 3.05, 0])
        fit(eq, max_w=12.2)
        self.play(FadeOut(e1), FadeIn(eq), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Evidence(SpokenScene):
    def construct(self):
        # ---- part A: purified channel in a droplet bilayer
        cL = Circle(radius=1.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-1.9, 0.2, 0])
        cR = Circle(radius=1.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([1.9, 0.2, 0])
        bar = Line([0, -1.1, 0], [0, 1.5, 0], color=GREY, stroke_width=10)
        blk = RoundedRectangle(corner_radius=0.1, width=0.6, height=1.1, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.45).move_to([0, 0.2, 0])
        A = VGroup(cL, cR, bar, blk)
        q = T("What is the evidence?", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(q), FadeIn(A), run_time=1.2)

        self.at("Purified mouse")
        lab = T("purified mouse PIEZO1", 26, BLUE).move_to([0, 2.45, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.at("no other cellular")
        dl = T("droplet bilayer, no other cellular components", 24, GREY).move_to([0, -2.0, 0])
        self.play(FadeIn(dl), run_time=0.5)
        self.at("still activated")
        fc = chip("force", YELLOW, size=26).move_to([-5.6, 0.2, 0])
        fa = Arrow([-4.8, 0.2, 0], [-3.9, 0.2, 0], buff=0, color=YELLOW, stroke_width=7, tip_length=0.26)
        act = chip("still activated by force", GREEN, size=26).move_to([0, -2.8, 0])
        self.play(FadeIn(fc), FadeIn(fa), FadeIn(act), run_time=0.7)
        self.at("plus lipid")
        suff = chip("protein plus lipid: sufficient in that preparation", GREEN, size=26).move_to([0, -2.8, 0])
        self.play(Transform(act, suff), run_time=0.6)

        # ---- part B: curved and flattened classes
        self.at("sorted purified")
        hdr = T("purified mouse PIEZO1 in liposome vesicles, cryo-EM", 26, GREY).to_edge(UP, buff=0.5)
        self.play(FadeOut(VGroup(A, lab, dl, fc, fa, act)), FadeOut(q), run_time=0.5)
        y0 = 0.5
        sc2 = 1.0
        cx1, cx2 = -3.3, 3.3
        d1 = dome(TH0, sc=sc2, cx=cx1, y0=y0, half=3.0, w=9)
        d2 = dome(0.0, sc=sc2, cx=cx2, y0=y0, half=3.0, w=9)
        l1 = T("curved class", 26, BLUE).move_to([cx1, y0 - 1.6, 0])
        l2 = T("flattened class", 26, BLUE).move_to([cx2, y0 - 1.6, 0])
        sch = note(y=-3.3)
        self.play(FadeIn(hdr), FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2), FadeIn(sch), run_time=0.9)
        b1 = static_bracket(TH0, y0 - 0.8, sc2, cx1, y0)
        b2 = static_bracket(0.0, y0 - 0.8, sc2, cx2, y0)
        self.at("differ by")
        diff = T("flattened: roughly 300 nm² more in-plane area", 28, PURPLE).move_to([0, -2.3, 0])
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(diff), run_time=0.8)
        self.at("hedge")
        hg = chip("the authors hedge: is this the gating transition itself?", RED, size=26).move_to([0, -3.15, 0])
        self.play(FadeOut(sch), FadeIn(hg), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Numbers(SpokenScene):
    def construct(self):
        top = T("Published fit: mouse Piezo1 in a human cell line, room temperature", 22, GREY).to_edge(UP, buff=0.4)

        # left column: the patch
        cx = -3.6
        arc = Arc(radius=1.3, start_angle=PI / 2 - 0.9, angle=1.8, arc_center=[cx, 0.8, 0], color=GREY, stroke_width=8)
        rad = Line([cx, 0.8, 0], arc.point_from_proportion(0.5), color=BLUE, stroke_width=4)
        centre = Dot([cx, 0.8, 0], radius=0.07, color=BLUE)
        patch = VGroup(arc, rad, centre)
        pl = T("illustrative patch\n(invented round numbers)", 22, GREY).move_to([cx, 2.7, 0])
        self.play(FadeIn(top), run_time=0.5)
        self.at("patches of mouse")
        self.play(Create(arc), FadeIn(pl), run_time=0.8)
        self.at("in radius")
        rl = M("R = 2.0 µm", 26, BLUE).move_to([cx + 2.4, 1.2, 0])
        self.play(Create(rad), FadeIn(centre), FadeIn(rl), run_time=0.7)
        self.at("under")
        dp = M("pressure difference 2000 Pa", 24, YELLOW).move_to([cx, -0.45, 0])
        self.play(FadeIn(dp), run_time=0.5)

        self.at("radius times pressure")
        f1 = M("T = R × ΔP / 2", 28, TEXT).move_to([cx, -1.1, 0])
        self.play(FadeIn(f1), run_time=0.5)
        self.at("That gives")
        f2 = M("T = 2.0 mN/m", 28, GREEN).move_to([cx, -1.75, 0])
        self.play(FadeIn(f2), run_time=0.5)

        # right: the Boltzmann fit
        self.at("Their fit has")
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 1, 0.5], x_length=5.0, y_length=4.0,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "tick_size": 0.07,
                               "include_tip": False}).move_to([3.4, -0.25, 0])
        xl = VGroup(*[M(str(i), 22, GREY).next_to(ax.c2p(i, 0), DOWN, buff=0.15) for i in range(6)])
        yl = VGroup(*[M(s, 22, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.12) for s, v in (("0", 0), ("0.5", 0.5), ("1", 1))])
        xt = T("tension (mN/m)", 24, GREY).next_to(ax, DOWN, buff=0.62)
        yt = T("I / Imax", 24, GREY).next_to(ax, UP, buff=0.15).align_to(ax, LEFT).shift(LEFT * 0.4)
        curve = ax.plot(lambda t: 1 / (1 + np.exp((2.7 - t) / 0.8)), x_range=[0, 5], color=BLUE, stroke_width=6)
        self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), run_time=0.7)
        self.play(Create(curve), run_time=1.0)

        self.at("tension of")
        t50 = DashedLine(ax.c2p(2.7, 0), ax.c2p(2.7, 0.5), color=PURPLE, stroke_width=4, dash_length=0.1)
        t50h = DashedLine(ax.c2p(0, 0.5), ax.c2p(2.7, 0.5), color=PURPLE, stroke_width=4, dash_length=0.1)
        t50l = M("T50 = 2.7", 24, PURPLE).move_to(ax.c2p(3.9, 0.3))
        self.play(Create(t50h), Create(t50), FadeIn(t50l), run_time=0.7)
        self.at("slope of")
        kl = M("k = 0.8", 24, PURPLE).move_to(ax.c2p(3.9, 0.12))
        self.play(FadeIn(kl), run_time=0.5)

        self.at("the fit predicts")
        y = 1 / (1 + np.exp(0.875))
        pt = Dot(ax.c2p(2.0, y), radius=0.12, color=GREEN)
        v1 = DashedLine(ax.c2p(2.0, 0), ax.c2p(2.0, y), color=GREEN, stroke_width=4, dash_length=0.1)
        v2 = DashedLine(ax.c2p(0, y), ax.c2p(2.0, y), color=GREEN, stroke_width=4, dash_length=0.1)
        ans = M("0.294", 24, GREEN).move_to(ax.c2p(0.8, y - 0.1))
        calc = M("1 / (1 + e^0.875) = 0.294", 24, GREEN).move_to([cx, -2.4, 0])
        pct = chip("about 29% of the plateau", GREEN, size=26).move_to([cx, -3.1, 0])
        self.play(Create(v1), Create(v2), FadeIn(pt), FadeIn(ans), FadeIn(calc), run_time=0.9)
        self.play(FadeIn(pct), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        y0 = -0.4
        mem = dome(TH0, sc=1.0, y0=y0, half=6.0)
        lipid = force_arrows(y0 + 0.45, x_in=2.5, length=1.5, w=7)
        ll = chip("force from lipid", YELLOW, size=26).move_to([-3.6, 2.9, 0])
        self.play(FadeIn(mem), FadeIn(lipid), FadeIn(ll), run_time=0.9)

        self.at("through protein")
        tether = VGroup(Line([0, y0 - 0.1, 0], [0, y0 - 1.1, 0], color=ORANGE, stroke_width=7),
                        Line([-1.8, y0 - 1.1, 0], [1.8, y0 - 1.1, 0], color=ORANGE, stroke_width=7))
        tl = chip("cadherin + actin tether", ORANGE, size=26).move_to([3.6, 2.9, 0])
        self.play(Create(tether), FadeIn(tl), run_time=0.9)
        self.at("has been proposed")
        pr = T("proposed in\ncultured cells", 24, ORANGE).move_to([4.2, y0 - 1.1, 0])
        self.play(FadeIn(pr), run_time=0.5)

        self.at("not rivals")
        nr = T("not rivals", 34, GREEN, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(nr), run_time=0.5)

        self.at("Sufficiency in")
        c1 = chip("Bilayer: sufficient.\nCannot exclude a coupling\nroute in an intact cell.", YELLOW, size=24).move_to([-3.2, -2.85, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("tether in")
        c2 = chip("Cultured cell: tether.\nCannot abolish the\nlipid energetics.", ORANGE, size=24).move_to([3.2, -2.85, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)

        self.at("Keep this rule")
        rule = T("Sufficient in one preparation\ndoes not mean exclusive in another", 34, TEXT, font=TITLE_FONT).move_to([0, -2.6, 0])
        self.play(FadeOut(VGroup(c1, c2, nr)), run_time=0.4)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Sufficient in one preparation does not mean exclusive in another."
