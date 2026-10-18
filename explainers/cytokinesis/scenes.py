"""Cytokinesis: the spindle tells the cell where to cut  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = the cell outline, neutral / off state (RhoA with GDP), notes
  YELLOW = the spindle (microtubules, poles) and the signal it sends
  GREEN  = active RhoA (GTP bound): the RhoA band, the GTP badge, ON
  BLUE   = the furrow and the actin ring (filaments, formin)
  PURPLE = Ect2
  ORANGE = myosin II
  TEAL   = the fluorescent probe in scene 2, and ESCRT-III from scene 5 on
  RED    = blocked / not allowed (drug, crossed out)
  WHITE  = chromosomes
  GOLD   = number badges
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def pulse(c, color, s=1.1, **kw):
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def pill(text, color, size=24):
    t = T(text, size, color, weight=BOLD)
    box = RoundedRectangle(corner_radius=(t.height + 0.2) / 2, width=t.width + 0.4, height=t.height + 0.2,
                           stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.22)
    back = RoundedRectangle(corner_radius=(t.height + 0.2) / 2, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    return VGroup(back, box, t.move_to(box))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def cross(center, s=0.28, color=RED, w=8):
    c = np.array([center[0], center[1], 0.0])
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w))


def beads(x0, x1, y, n, color=BLUE, r=0.1):
    xs = np.linspace(x0, x1, n)
    line = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3, stroke_opacity=0.7)
    dots = VGroup(*[Dot([x, y, 0], radius=r, color=color) for x in xs])
    return VGroup(line, dots)


def badge(n, size=22):
    c = Circle(radius=0.23, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T(str(n), size, BG, weight=BOLD).move_to(c))


def polyline(pts, color, width, opacity):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, width, opacity=opacity)
    m.set_fill(opacity=0)
    return m


class Rig:
    """One cell drawn from value trackers, so the outline, the green band, the furrow and the spindle can
    each move on their own. Lengths scale with r / 2.5. u, ub, sp are screen offsets from the cell centre.
    d is the depth of the furrow dent. Everything is always_redraw."""

    def __init__(self, cx=0.0, cy=-0.2, r=2.5, u=0.0, d=0.0, ub=0.0, sp=0.0, a=0.0, bandop=0.0, chop=0.0,
                 mtop=0.0, polop=0.0, ringop=0.0, rings=0.0, L=1.0):
        self.L = L
        V = ValueTracker
        self.cx, self.cy, self.r = V(cx), V(cy), V(r)
        self.u, self.d, self.ub, self.sp = V(u), V(d), V(ub), V(sp)
        self.a, self.bandop, self.chop, self.mtop, self.polop = V(a), V(bandop), V(chop), V(mtop), V(polop)
        self.ringop, self.rings = V(ringop), V(rings)
        self.cut, self.sep = V(0), V(0)
        self.outline = always_redraw(self._outline)
        self.hi = always_redraw(self._hi)
        self.band = always_redraw(self._band)
        self.ring = always_redraw(self._ring)
        self.escrt = always_redraw(self._escrt)
        self.chroms = always_redraw(self._chroms)
        self.mts = always_redraw(self._mts)
        self.poles = always_redraw(self._poles)
        self.parts = [self.outline, self.hi, self.band, self.ring, self.escrt, self.chroms, self.mts, self.poles]

    # --- geometry -----------------------------------------------------------------------
    def k(self):
        return self.r.get_value() / 2.5

    def xf(self):
        return self.cx.get_value() + self.u.get_value()

    def ytop(self, x):
        cx, r, k = self.cx.get_value(), self.r.get_value(), self.k()
        base = math.sqrt(max(r * r - (x - cx) ** 2, 0.0))
        dent = self.d.get_value() * k * math.exp(-((x - self.xf()) / (0.55 * k)) ** 2)
        return max(base - dent, 0.04 * k)

    def _span(self, xc, w, n=26):
        cx, r = self.cx.get_value(), self.r.get_value()
        x0, x1 = max(xc - w, cx - r + 0.02), min(xc + w, cx + r - 0.02)
        return np.linspace(x0, x1, n)

    def _outline(self):
        cx, cy, r = self.cx.get_value(), self.cy.get_value(), self.r.get_value()
        a = self.a.get_value()
        phis = np.linspace(-math.pi / 2, math.pi / 2, 120)
        xs = cx + r * np.sin(phis)
        yt = np.array([self.ytop(x) for x in xs])
        kw = dict(stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.07 * a, stroke_opacity=a)
        if self.cut.get_value() > 0.5:
            xf, sep = self.xf(), self.sep.get_value()
            out = VGroup()
            for side in (-1, 1):
                sel = xs <= xf if side < 0 else xs >= xf
                x, y = xs[sel], yt[sel]
                pts = [[xi + side * sep, cy + yi, 0] for xi, yi in zip(x, y)] + \
                      [[xi + side * sep, cy - yi, 0] for xi, yi in zip(x[::-1], y[::-1])]
                out.add(Polygon(*pts, **kw))
            return out
        pts = [[x, cy + y, 0] for x, y in zip(xs, yt)] + [[x, cy - y, 0] for x, y in zip(xs[::-1], yt[::-1])]
        return Polygon(*pts, **kw)

    def _hi(self):
        cy, k = self.cy.get_value(), self.k()
        op = min(1.0, self.d.get_value() / 0.3) * self.a.get_value()
        if self.cut.get_value() > 0.5:
            op = 0
        xs = self._span(self.xf(), 1.5 * k, 40)
        top = [(x, cy + self.ytop(x)) for x in xs]
        bot = [(x, cy - self.ytop(x)) for x in xs]
        return VGroup(polyline(top, BLUE, 8, op), polyline(bot, BLUE, 8, op))

    def _band(self):
        cx, cy, k = self.cx.get_value(), self.cy.get_value(), self.k()
        op = self.bandop.get_value()
        xs = self._span(cx + self.ub.get_value(), 0.6 * k)
        top = [(x, cy + self.ytop(x)) for x in xs]
        bot = [(x, cy - self.ytop(x)) for x in xs]
        return VGroup(polyline(top, GREEN, 16, op), polyline(bot, GREEN, 16, op))

    def _ring(self):
        cy, k = self.cy.get_value(), self.k()
        op = self.ringop.get_value()
        xs = self._span(self.xf(), 0.9 * k, 60)
        ys = np.array([self.ytop(x) for x in xs])
        seg = np.hypot(np.diff(xs), np.diff(ys))
        sl = np.concatenate([[0], np.cumsum(seg)])
        out = VGroup()
        for t in np.linspace(0, sl[-1], 9):
            x, y = np.interp(t, sl, xs), np.interp(t, sl, ys)
            i = min(max(int(np.searchsorted(sl, t)), 1), len(xs) - 1)
            tx, ty = xs[i] - xs[i - 1], ys[i] - ys[i - 1]
            n = math.hypot(tx, ty) or 1.0
            px, py = x + (ty / n) * 0.27 * k, y - (tx / n) * 0.27 * k
            for sgn in (1, -1):
                out.add(Dot([px, cy + sgn * py, 0], radius=0.09 * k, color=BLUE).set_opacity(op))
        return out

    def _escrt(self):
        cy, k = self.cy.get_value(), self.k()
        op = self.rings.get_value()
        xf = self.xf()
        out = VGroup()
        for dx in (-0.22, 0.0, 0.22):
            x = xf + dx * k
            h = 2 * (self.ytop(x) + 0.14 * k)
            out.add(Ellipse(width=0.13 * k, height=h, stroke_color=TEAL, stroke_width=5, fill_opacity=0,
                            stroke_opacity=op).move_to([x, cy, 0]))
        return out

    def _chroms(self):
        cx, cy, k = self.cx.get_value(), self.cy.get_value(), self.k()
        op = self.chop.get_value()
        sp, sep = self.sp.get_value(), self.sep.get_value()
        out = VGroup()
        for s in (-1, 1):
            out.add(Ellipse(width=0.34 * k, height=1.0 * k, stroke_width=0, fill_color=TEXT, fill_opacity=0.92 * op)
                    .move_to([cx + sp + s * (1.0 * k * self.L + sep), cy, 0]))
        return out

    def _mts(self):
        cx, cy, k = self.cx.get_value(), self.cy.get_value(), self.k()
        op = self.mtop.get_value()
        sp = self.sp.get_value()
        out = VGroup()
        for s in (-1, 1):
            pole = np.array([cx + sp + s * 1.8 * k * self.L, cy, 0])
            for dy in (-0.4, -0.13, 0.13, 0.4):
                tgt = np.array([cx + sp + s * (1.0 * self.L + 0.19) * k, cy + dy * k, 0])
                out.add(Line(pole, tgt, color=YELLOW, stroke_width=3, stroke_opacity=0.85 * op))
        return out

    def _poles(self):
        cx, cy, k = self.cx.get_value(), self.cy.get_value(), self.k()
        op = self.polop.get_value()
        sp = self.sp.get_value()
        return VGroup(*[Dot([cx + sp + s * 1.8 * k * self.L, cy, 0], radius=0.12 * k, color=YELLOW).set_opacity(op) for s in (-1, 1)])


class LiveScene(SpokenScene):
    """SpokenScene whose animations run a little slower than written, so that motion fills the narration."""
    STRETCH = 1.35

    def play(self, *anims, run_time=None, **kw):
        if run_time is not None:
            kw["run_time"] = run_time * self.STRETCH
        return super().play(*anims, **kw)


def put(scene, rig):
    scene.add(*rig.parts)


def to(tracker, v):
    return tracker.animate.set_value(v)


class S00Title(TitleCard):
    LESSON = "Cytokinesis and organelle inheritance"
    TITLE = "The spindle tells the cell where to cut"


# ---------------------------------------------------------------------------------------------
class S01Where(LiveScene):
    """the question: where does the cell cut? -> midway between the sets -> the spindle sends the signal."""

    def construct(self):
        rig = Rig(cx=0, cy=-0.2, r=2.5)
        put(self, rig)
        lbl_chr = T("two sets of chromosomes", 24, TEXT).move_to([0, -1.4, 0])

        self.at("sorted its chromosomes")
        self.play(to(rig.a, 1), to(rig.chop, 1), FadeIn(lbl_chr), run_time=1.0)

        self.at("cut itself")
        self.play(Indicate(rig.outline, color=TEXT, scale_factor=1.03), run_time=0.8)

        # the puzzle: three possible places, none known
        cands = VGroup()
        for x in (-1.8, 0.0, 1.8):
            ln = DashedLine([x, -0.2 - 0.65, 0], [x, -0.2 + 0.65, 0], color=GREY, stroke_width=4, dash_length=0.14)
            q = T("?", 44, GREY, weight=BOLD).move_to([x, 0.95, 0])
            cands.add(VGroup(ln, q))
        self.at("But where")
        self.play(LaggedStart(*[FadeIn(c) for c in cands], lag_ratio=0.25), run_time=1.0)

        # the answer: midway between the two sets
        furrow_lbl = T("furrow", 30, BLUE, weight=BOLD).move_to([0, 2.95, 0])
        furrow_arr = arr([0, 2.65, 0], [0, 2.05, 0], BLUE)
        self.at("forms midway")
        self.play(FadeOut(cands[0]), FadeOut(cands[2]), FadeOut(cands[1]), to(rig.d, 0.4),
                  FadeIn(furrow_lbl), GrowArrow(furrow_arr), run_time=1.0)

        self.at("not an accident")
        self.play(Indicate(furrow_lbl, color=BLUE, scale_factor=1.12), run_time=0.8)

        sp_lbl = T("spindle", 30, YELLOW, weight=BOLD).move_to([4.7, 1.1, 0])
        sp_ln = Line([3.75, 0.95, 0], [1.95, -0.12, 0], color=YELLOW, stroke_width=2.5, stroke_opacity=0.8)
        self.at("The spindle")
        self.play(to(rig.polop, 1), FadeIn(sp_lbl), Create(sp_ln), run_time=0.7)
        self.at("array of microtubules")
        self.play(to(rig.mtop, 1), run_time=1.0)

        sig = VGroup(arr([0, -0.05, 0], [0, 1.5, 0], YELLOW, w=7), arr([0, -0.35, 0], [0, -1.9, 0], YELLOW, w=7))
        sig_lbl = T("signal", 30, YELLOW, weight=BOLD).move_to([1.05, 0.95, 0])
        self.at("sends the signal")
        self.play(FadeOut(lbl_chr), run_time=0.3)
        self.play(LaggedStart(*[GrowArrow(s) for s in sig], lag_ratio=0.2), FadeIn(sig_lbl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Switch(LiveScene):
    """RhoA is a switch; Ect2 loads GTP; a probe that binds only GTP-RhoA lights the band."""

    def construct(self):
        rig = Rig(cx=0, cy=-0.2, r=2.5, d=0.4, a=1, chop=1, mtop=1, polop=1)
        put(self, rig)
        # carry over: the cell slides left and shrinks, the furrow mark is cleared
        self.play(to(rig.cx, -3.8), to(rig.cy, 0.05), to(rig.r, 2.3), to(rig.d, 0), run_time=0.9)

        rho = chip("RhoA", GREY, 44).move_to([1.0, 2.35, 0])
        self.at("small switch protein")
        self.play(FadeIn(rho, shift=DOWN * 0.15), run_time=0.6)

        slot = np.array([3.2, 2.35, 0])
        gtp = pill("GTP", GREEN, 32).move_to(slot)
        on = T("ON", 44, GREEN, weight=BOLD).move_to([5.3, 2.35, 0])
        self.at("on when it holds")
        self.play(FadeIn(gtp, shift=LEFT * 0.2), *recolor_chip(rho, GREEN), FadeIn(on), run_time=0.7)

        gdp = pill("GDP", GREY, 32).move_to(slot)
        off = T("OFF", 44, GREY, weight=BOLD).move_to([5.3, 2.35, 0])
        self.at("off when it holds")
        self.play(FadeOut(gtp, shift=RIGHT * 0.2), FadeOut(on), FadeIn(gdp, shift=LEFT * 0.2), FadeIn(off),
                  *recolor_chip(rho, GREY), run_time=0.7)

        ect2 = bchip("Ect2", PURPLE, 36).move_to([1.3, 0.8, 0])
        self.at("an enzyme called")
        self.play(FadeIn(ect2, shift=UP * 0.25), run_time=0.6)
        self.at("switches it on")
        self.play(ect2.animate.move_to([1.3, 1.1, 0]), run_time=0.4)
        self.play(pulse(ect2, PURPLE, 1.08), run_time=0.5)

        gtp2 = pill("GTP", GREEN, 32).move_to([5.3, 0.9, 0])
        self.at("swaps")
        self.play(gdp.animate.move_to([3.9, 0.9, 0]).set_opacity(0.0), run_time=0.7)
        on2 = T("ON", 44, GREEN, weight=BOLD).move_to([5.3, 2.35, 0])
        self.play(gtp2.animate.move_to(slot), *recolor_chip(rho, GREEN), ReplacementTransform(off, on2), run_time=0.8)
        self.remove(gdp)

        # visible: the probe binds only the GTP form
        self.at("made active")
        self.play(FadeOut(ect2, shift=DOWN * 0.2), run_time=0.5)

        YB = -0.9
        rA = chip("RhoA", GREEN, 34).move_to([0.7, YB, 0])
        gA = pill("GTP", GREEN, 26).move_to([2.35, YB, 0])
        rB = chip("RhoA", GREY, 34).move_to([4.2, YB, 0])
        gB = pill("GDP", GREY, 26).move_to([5.75, YB, 0])
        glow = RoundedRectangle(corner_radius=0.3, width=3.15, height=1.5, stroke_width=0, fill_color=GREEN,
                                fill_opacity=0.0).move_to([1.5, YB, 0])
        glow.set_z_index(-1)
        self.add(glow)
        probe = bchip("probe", TEAL, 30).move_to([2.7, -2.75, 0])
        self.play(FadeIn(VGroup(rA, gA, rB, gB)), run_time=0.7)
        self.at("fused a green")
        self.play(FadeIn(probe, shift=UP * 0.2), run_time=0.7)
        pnote = T("green fluorescent protein + fragment", 24, TEAL).move_to([2.7, -3.45, 0])
        self.play(FadeIn(pnote), run_time=0.5)

        self.at("binds only")
        self.play(probe.animate.move_to([1.5, -2.05, 0]), run_time=0.7)
        self.play(glow.animate.set_fill(GREEN, 0.3), run_time=0.4)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=1.7, height=0.8, stroke_color=TEAL), num_dashes=24).move_to([4.9, -2.05, 0])
        x = cross([4.9, -2.05])
        self.play(Create(ghost), Create(x), run_time=0.6)

        # the glow shows where RhoA is on
        self.at("The glow marks")
        self.play(to(rig.bandop, 1), run_time=0.9)
        band_lbl = T("RhoA is on here", 26, GREEN).move_to([-3.8, -2.85, 0])
        self.play(FadeIn(band_lbl), run_time=0.5)
        self.finish()


def recolor_chip(c, color):
    return [c[0].animate.set_stroke(color).set_fill(color, 0.16), c[1].animate.set_color(color)]


# ---------------------------------------------------------------------------------------------
class S03Before(LiveScene):
    """the band forms 1 to 4 minutes before the furrow; with actin assembly blocked it still forms."""

    def construct(self):
        rig = Rig(cx=-3.8, cy=0.05, r=2.3, a=1, chop=1, mtop=1, polop=1)
        put(self, rig)
        self.wait(0.3)

        axis = Arrow([0.4, 0.4, 0], [6.1, 0.4, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        t_lbl = T("time", 26, GREY).move_to([5.7, -0.05, 0])
        m1 = Dot([1.4, 0.4, 0], radius=0.17, color=GREEN)
        m1l = T("band appears", 28, GREEN).move_to([1.5, 1.1, 0])
        m2 = Dot([4.8, 0.4, 0], radius=0.17, color=BLUE)
        m2l = T("furrow appears", 28, BLUE).move_to([4.6, 1.1, 0])
        br = VGroup(Line([1.4, 2.0, 0], [4.8, 2.0, 0], color=TEXT, stroke_width=3),
                    Line([1.4, 2.0, 0], [1.4, 1.75, 0], color=TEXT, stroke_width=3),
                    Line([4.8, 2.0, 0], [4.8, 1.75, 0], color=TEXT, stroke_width=3))
        br_t = T("1 to 4 minutes", 34, TEXT).move_to([3.1, 2.6, 0])

        self.at("bounded band")
        self.play(to(rig.bandop, 1), run_time=0.8)
        self.at("The band appears")
        self.play(GrowArrow(axis), FadeIn(t_lbl), FadeIn(m1, scale=0.5), FadeIn(m1l), run_time=0.9)
        self.at("one to four minutes")
        self.play(Create(br), FadeIn(br_t), run_time=0.9)
        self.at("before the furrow")
        self.play(FadeIn(m2, scale=0.5), FadeIn(m2l), to(rig.d, 0.5), run_time=0.9)

        tag1 = bchip("sea urchin", GREY, 28).move_to([1.7, -1.0, 0])
        tag2 = bchip("frog", GREY, 28).move_to([4.2, -1.0, 0])
        self.at("sea urchin")
        self.play(FadeIn(tag1, shift=UP * 0.15), run_time=0.5)
        self.at("frog")
        self.play(FadeIn(tag2, shift=UP * 0.15), run_time=0.5)

        # reset to a neutral state before the drug case
        chain_rho = bchip("RhoA band", GREEN, 32).move_to([1.5, 1.7, 0])
        chain_act = bchip("actin ring", BLUE, 32).move_to([4.7, 1.7, 0])
        chain_a = arr(chain_rho.get_right(), chain_act.get_left(), GREY)
        self.at("Next, the researchers")
        self.play(FadeOut(VGroup(axis, t_lbl, m1, m1l, m2, m2l, br, br_t, tag1, tag2)), to(rig.d, 0), run_time=0.6)
        self.play(FadeIn(chain_rho), GrowArrow(chain_a), FadeIn(chain_act), run_time=0.6)

        drug = bchip("actin assembly blocked", RED, 26).move_to([3.6, -0.4, 0])
        drug_n = T("cytochalasin D, latrunculin B", 24, GREY).move_to([3.6, -1.25, 0])
        bar = inhib([4.7, drug.get_top()[1], 0], chain_act.get_bottom(), RED)
        self.at("blocked actin assembly")
        self.play(FadeIn(drug, shift=UP * 0.15), Create(bar), FadeIn(drug_n), run_time=0.9)

        still = T("band still forms", 30, GREEN, weight=BOLD).move_to([1.5, 0.95, 0])
        self.at("the band still formed")
        self.play(FadeIn(still, shift=UP * 0.15), Indicate(rig.band, color=GREEN, scale_factor=1.05), run_time=0.9)

        b1, b2 = badge(1).move_to(chain_rho.get_corner(UL) + [-0.02, 0.2, 0]), badge(2).move_to(chain_act.get_corner(UL) + [-0.02, 0.2, 0])
        self.at("switches on before")
        self.play(FadeIn(b1, scale=0.5), run_time=0.4)
        self.at("actin ring")
        self.play(FadeIn(b2, scale=0.5), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Push(LiveScene):
    """a needle pushes the spindle aside: the band relocates, then the furrow follows."""

    def construct(self):
        rig = Rig(cx=0, cy=0.15, r=2.4, d=0.45, L=0.9)
        put(self, rig)
        c1 = bchip("spindle moves", YELLOW, 30).move_to([-4.2, -3.1, 0])
        c2 = bchip("band moves", GREEN, 30).move_to([0.0, -3.1, 0])
        c3 = bchip("furrow moves", BLUE, 30).move_to([4.2, -3.1, 0])
        ar1 = arr(c1.get_right(), c2.get_left(), GREY)
        ar2 = arr(c2.get_right(), c3.get_left(), GREY)

        self.play(to(rig.a, 1), to(rig.chop, 1), to(rig.mtop, 1), to(rig.polop, 1), to(rig.bandop, 1), run_time=0.8)

        needle = VGroup(Line([-6.2, 0.15, 0], [-1.6, 0.15, 0], color=GREY, stroke_width=16),
                        Dot([-1.6, 0.15, 0], radius=0.11, color=GREY))
        needle.shift(LEFT * 1.0)
        nl = T("blunt needle", 28, GREY).move_to([-4.6, 0.85, 0])
        self.at("pushed the spindle aside")
        self.play(FadeIn(c1), needle.animate.shift(RIGHT * 1.0), FadeIn(nl), run_time=0.9)
        self.play(needle.animate.shift(RIGHT * 0.6), nl.animate.shift(RIGHT * 0.6), to(rig.sp, 0.6),
                  pulse(c1, YELLOW, 1.1), run_time=1.4)

        clock = Rectangle(width=2.6, height=0.28, stroke_color=GREY, stroke_width=3).move_to([4.8, 2.3, 0])
        fill = Rectangle(width=0.02, height=0.28, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).align_to(clock, LEFT).align_to(clock, DOWN)
        clk_l = T("3 to 5 minutes", 28, TEXT).move_to([4.8, 2.9, 0])
        self.at("The band relocated")
        self.play(FadeIn(clock), FadeIn(fill), FadeIn(clk_l), FadeIn(c2), GrowArrow(ar1), run_time=0.5)
        fill_end = Rectangle(width=2.6, height=0.28, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).align_to(clock, LEFT).align_to(clock, DOWN)
        self.play(to(rig.ub, 0.6), Transform(fill, fill_end), run_time=1.8)
        self.play(pulse(c2, GREEN, 1.1), run_time=0.4)

        self.at("the furrow followed")
        self.play(to(rig.u, 0.6), FadeIn(c3), GrowArrow(ar2), run_time=1.3)
        self.play(pulse(c3, BLUE, 1.1), run_time=0.4)

        self.at("Move the spindle")
        self.play(pulse(c1, YELLOW, 1.12), run_time=0.5)
        self.at("the signal moves first")
        self.play(pulse(c2, GREEN, 1.15), Indicate(rig.band, color=GREEN, scale_factor=1.05), run_time=0.8)

        dl = T("delay", 26, TEXT).move_to([-2.1, -2.55, 0])
        self.at("The delay")
        self.play(FadeIn(dl, shift=UP * 0.1), Indicate(ar1, color=TEXT), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ring(LiveScene):
    """RhoA -> formin -> filaments; RhoA -> myosin II pulls them; ring; furrow; bridge; ESCRT-III cuts."""

    def construct(self):
        rig = Rig(cx=3.4, cy=-0.2, r=2.4, a=0, bandop=0, chop=0, mtop=0, polop=0)
        put(self, rig)
        self.play(to(rig.a, 1), to(rig.chop, 1), to(rig.bandop, 1), run_time=0.7)

        rho = bchip("active RhoA", GREEN, 30).move_to([-3.4, 2.9, 0])
        formin = bchip("formin", BLUE, 30).move_to([-5.0, 1.9, 0])
        a_f = arr(rho.get_left(), formin.get_top(), GREEN)
        row1 = beads(-5.6, -2.3, 0.95, 12)
        self.at("turns on")
        self.play(FadeIn(rho, shift=DOWN * 0.15), run_time=0.4)
        self.play(GrowArrow(a_f), FadeIn(formin), run_time=0.6)
        self.at("long actin filaments")
        self.play(FadeIn(row1[0]), LaggedStart(*[FadeIn(d, scale=0.4) for d in row1[1]], lag_ratio=0.12), run_time=1.6)

        myo = bchip("myosin II", ORANGE, 30).move_to([-4.0, 0.3, 0])
        a_m = CurvedArrow([-2.0, 2.75, 0], [-2.8, 0.55, 0], angle=-0.9, color=GREEN, stroke_width=5, tip_length=0.22)
        self.at("promotes myosin")
        self.play(Create(a_m), FadeIn(myo), run_time=0.9)
        row2 = beads(-5.6, -2.3, -0.35, 12)
        row2_l = T("actin filaments", 26, BLUE).move_to([-4.0, -1.0, 0])
        self.at("a motor that pulls")
        self.play(FadeIn(row2), FadeIn(row2_l), run_time=0.7)
        self.at("past each other")
        self.play(row1.animate.shift(LEFT * 0.4), row2.animate.shift(RIGHT * 0.4), pulse(myo, ORANGE, 1.1), run_time=1.4)

        ringlbl = T("contractile ring", 30, BLUE, weight=BOLD).move_to([3.4, 2.95, 0])
        self.at("contractile ring")
        self.play(to(rig.ringop, 1), FadeIn(ringlbl), run_time=1.0)
        self.at("as it tightens")
        self.play(to(rig.d, 1.1), run_time=0.9)
        self.at("furrow ingresses")
        self.play(to(rig.d, 2.0), run_time=1.6)

        bridge = T("thin bridge", 28, TEXT).move_to([3.4, 2.95, 0])
        b_ar = arr([3.4, 2.6, 0], [3.4, 0.45, 0], TEXT)
        self.at("thin bridge")
        self.play(FadeOut(ringlbl), to(rig.ringop, 0), FadeIn(bridge), GrowArrow(b_ar), run_time=0.9)

        esc = bchip("ESCRT-III", TEAL, 30).move_to([3.4, -3.05, 0])
        self.at("assembles in the bridge")
        self.play(FadeOut(b_ar), to(rig.rings, 1), FadeIn(esc, shift=UP * 0.15), run_time=0.9)
        self.at("constricts it")
        self.play(to(rig.d, 2.3), run_time=1.0)
        self.at("cuts it")
        self.play(FadeOut(bridge), to(rig.rings, 0), run_time=0.3)
        rig.cut.set_value(1)
        self.play(to(rig.sep, 0.4), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(LiveScene):
    """caveats (timings from large embryonic cells; ring arrangement differs) and the rule."""

    def construct(self):
        card = RoundedRectangle(corner_radius=0.2, width=5.8, height=4.1, stroke_color=GREY, stroke_width=3).move_to([-3.35, 0.25, 0])
        ct = T("large embryonic cells", 32, TEXT, weight=BOLD).move_to([-3.35, 1.85, 0])
        r1 = T("band: 1 to 4 minutes", 28, GREEN).move_to([-3.35, 0.95, 0])
        r1b = T("before the furrow", 28, GREEN).move_to([-3.35, 0.45, 0])
        r2 = T("band moves: 3 to 5 minutes", 28, GREEN).move_to([-3.35, -0.35, 0])
        self.at("These timings come")
        self.play(Create(card), FadeIn(ct), run_time=0.8)
        self.play(FadeIn(r1), FadeIn(r1b), FadeIn(r2), run_time=0.8)

        hum = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.4, height=4.1, stroke_color=GREY), num_dashes=60).move_to([3.35, 0.25, 0])
        ht = T("a human cell", 32, TEXT, weight=BOLD).move_to([3.35, 1.85, 0])
        hq = T("same minutes?", 34, RED).move_to([3.35, 0.75, 0])
        hq2 = T("do not assume", 28, GREY).move_to([3.35, -0.05, 0])
        self.at("do not assume")
        self.play(Create(hum), FadeIn(ht), run_time=0.7)
        self.play(FadeIn(hq), FadeIn(hq2), run_time=0.7)

        # the ring cartoon, and a different arrangement
        clear1 = VGroup(card, ct, r1, r1b, r2, hum, ht, hq, hq2)
        cen = np.array([-3.3, 0.35, 0])
        ring_a = VGroup(Circle(radius=1.9, color=BLUE, stroke_width=3, stroke_opacity=0.6).move_to(cen),
                        *[Dot(cen + [1.9 * math.cos(a), 1.9 * math.sin(a), 0], radius=0.14, color=BLUE) for a in np.linspace(0, TAU, 21)[:-1]])
        ring_a_l = T("the drawstring cartoon", 30, BLUE).move_to([-3.3, -2.45, 0])
        self.at("standard cartoon")
        self.play(FadeOut(clear1), run_time=0.5)
        self.play(FadeIn(ring_a, scale=0.8), FadeIn(ring_a_l), run_time=0.9)
        arr_b = VGroup(*[beads(0.9, 5.7, y, 12, r=0.13) for y in (1.55, 0.85, 0.15, -0.55)])
        for i, rw in enumerate(arr_b):
            rw.shift(RIGHT * (0.2 if i % 2 else -0.2))
        arr_b_l = T("another arrangement", 30, BLUE).move_to([3.3, -2.45, 0])
        self.at("differs between systems")
        self.play(FadeIn(arr_b), FadeIn(arr_b_l), Wiggle(ring_a, scale_value=1.03, rotation_angle=0.02 * TAU), run_time=1.2)

        # the rule
        s1 = bchip("spindle", YELLOW, 40).move_to([-4.6, 0.3, 0])
        s2 = bchip("RhoA band", GREEN, 40).move_to([0.0, 0.3, 0])
        s3 = bchip("furrow", BLUE, 40).move_to([4.6, 0.3, 0])
        a1 = arr(s1.get_right(), s2.get_left(), GREY, w=7)
        a2 = arr(s2.get_right(), s3.get_left(), GREY, w=7)
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(ring_a, ring_a_l, arr_b, arr_b_l)), run_time=0.6)
        self.play(FadeIn(s1, shift=UP * 0.15), run_time=0.5)
        self.at("places the signal")
        self.play(GrowArrow(a1), FadeIn(s2), run_time=0.7)
        self.at("furrow follows")
        self.play(GrowArrow(a2), FadeIn(s3), run_time=0.7)
        self.play(pulse(s1, YELLOW, 1.08), pulse(s2, GREEN, 1.08), pulse(s3, BLUE, 1.08), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The spindle places the signal, and the furrow follows."
