"""Local organizers: one bead builds a midbrain  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = forebrain tissue
  GREEN  = midbrain tissue (also the new, induced midbrain)
  PURPLE = hindbrain tissue (rhombomere 1 and behind)
  TEAL   = Otx2
  PINK   = Gbx2
  YELLOW = FGF8 and the organizer / bead (the signal source)
  ORANGE = Wnt1
  TEXT (white) = Engrailed and Pax2/5, and Hox
  RED    = repression, loss, removal
  GREY   = tube outline, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"
FORE, MID, HIND = BLUE, GREEN, PURPLE
OTX, GBX, FGF, WNT = TEAL, PINK, YELLOW, ORANGE

H = 1.9          # tube half-height
XL, XR = -6.0, 6.0
XI = 0.6         # the isthmus
X_MID0, X_R1, X_HIND0 = -2.4, 2.6, 2.6


def prof(x):
    b = H * max(0.0, 1 - (abs(x) / 6.0) ** 4) ** 0.25
    return b * (1 - 0.30 * np.exp(-((x - XI) / 0.35) ** 2))


def poly(xa, xb, ty, color=None, op=0.25, stroke=0, sc=None):
    xs = np.linspace(xa, xb, 70)
    top = [[x, ty + prof(x), 0] for x in xs]
    bot = [[x, ty - prof(x), 0] for x in xs[::-1]]
    p = Polygon(*(top + bot), stroke_width=stroke, stroke_color=sc or color or GREY)
    if color:
        p.set_fill(color, op)
    else:
        p.set_fill(opacity=0)
    return p


class Tube:
    """Neural tube, side view: forebrain | midbrain | isthmus | hindbrain (first segment = rhombomere 1)."""

    def __init__(self, ty, labels=True, cere=False):
        self.ty = ty
        self.fore = poly(XL, X_MID0, ty, FORE)
        self.mid = poly(X_MID0, XI, ty, MID)
        self.r1 = poly(XI, X_R1, ty, HIND)
        self.hind = poly(X_R1, XR, ty, HIND)
        self.out = poly(XL, XR, ty, None, stroke=4, sc=GREY)
        ly = ty + H + 0.38
        self.lab = VGroup(T("forebrain", 24, FORE).move_to([-4.2, ly, 0]),
                          T("midbrain", 24, MID).move_to([-1.3, ly, 0]),
                          T("hindbrain", 24, HIND).move_to([4.3, ly, 0]))
        if cere:
            self.lab.add(T("cerebellum", 24, HIND).move_to([1.6, ly, 0]))
            self.lab[2].move_to([4.6, ly, 0])
        self.body = VGroup(self.fore, self.mid, self.r1, self.hind, self.out)
        self.all = VGroup(self.body, self.lab) if labels else VGroup(self.body)

    def y(self):
        return self.ty


def bead(pos, r=0.2):
    return Circle(radius=r, stroke_color=BG, stroke_width=2, fill_color=FGF, fill_opacity=1).move_to(pos)


def bar(x0, x1, y, color, label, h=0.55, size=26):
    r = RoundedRectangle(corner_radius=0.14, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.28).move_to([(x0 + x1) / 2, y, 0])
    return VGroup(r, T(label, size, color).move_to(r))


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5, tb=0.13):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * tb, b - perp * tb, color=color, stroke_width=w + 1))


def cross(c, color=RED, s=0.5):
    p = c.get_center()
    return VGroup(Line(p + [-s, -s * 0.8, 0], p + [s, s * 0.8, 0], color=color, stroke_width=7),
                  Line(p + [-s, s * 0.8, 0], p + [s, -s * 0.8, 0], color=color, stroke_width=7))


class S00Title(TitleCard):
    LESSON = "Local organizers: the midbrain-hindbrain boundary"
    TITLE = "One bead builds a midbrain"


# ---------------------------------------------------------------------------------------------
class S01Bead(SpokenScene):
    def construct(self):
        ty = -0.1
        tb = Tube(ty)
        self.add(tb.out)
        self.play(FadeIn(tb.fore), FadeIn(tb.mid), FadeIn(tb.r1), FadeIn(tb.hind), FadeIn(tb.lab), run_time=0.4)
        bx = np.array([-3.15, ty + 0.1, 0])
        b = bead(bx + UP * 3.0)
        self.at("Push a tiny bead")
        self.play(FadeIn(b), run_time=0.3)
        self.play(b.animate.move_to(bx), run_time=1.0)
        blab = T("FGF8 bead", 26, FGF).move_to([-4.9, ty - H - 0.45, 0])
        self.at("soaked in one protein")
        self.play(FadeIn(blab), Indicate(b, color=FGF, scale_factor=1.6), run_time=0.8)
        new = Ellipse(width=1.4, height=2.5, stroke_color=MID, stroke_width=4, fill_color=MID, fill_opacity=0.45).move_to(bx)
        nlab = T("second midbrain", 26, MID).move_to([-1.6, ty - H - 0.45, 0])
        self.at("second midbrain can grow")
        self.play(GrowFromCenter(new), run_time=1.2)
        self.bring_to_front = None
        self.add(b)
        self.play(FadeIn(nlab), run_time=0.4)
        self.at("How can one bead")
        qs = VGroup(*[T("?", 44, TEXT, weight=BOLD).move_to([x, ty + dy, 0]) for x, dy in
                      [(-1.9, 0.5), (-0.9, -0.5), (1.9, 0.5), (3.0, -0.5), (4.4, 0.6), (5.2, -0.6)]])
        self.at("Cells in the neural tube")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.15), run_time=1.2)
        who = T("Who tells the cells where they are?", 34).move_to([0, -3.2, 0])
        self.at("Who tells them")
        self.play(FadeIn(who, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Organizer(SpokenScene):
    def construct(self):
        ty = -0.1
        tb = Tube(ty)
        self.add(tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)
        hox = VGroup()
        for i, y in enumerate([0.75, 0.25, -0.25, -0.75]):
            x0 = 2.2 + 0.55 * i
            hox.add(RoundedRectangle(corner_radius=0.1, width=5.7 - x0, height=0.24, stroke_color=TEXT, stroke_width=2,
                                     fill_color=TEXT, fill_opacity=0.45).move_to([(x0 + 5.7) / 2, ty + y, 0]))
        hlab = T("Hox genes", 26, TEXT).move_to([4.0, ty - H - 0.45, 0])
        self.at("Hox genes give")
        self.play(LaggedStart(*[GrowFromEdge(h, LEFT) for h in hox], lag_ratio=0.25), FadeIn(hlab), run_time=1.6)
        nohox = T("no Hox code", 28, GREY).move_to([-3.2, ty, 0])
        self.at("But the midbrain")
        self.play(FadeIn(nohox, shift=UP * 0.1), run_time=0.6)
        self.at("They need other instructions")
        self.play(Indicate(nohox, color=TEXT, scale_factor=1.15), run_time=0.8)
        glow = Circle(radius=0.55, stroke_width=0, fill_color=FGF, fill_opacity=0.25).move_to([XI, ty, 0])
        dot = Circle(radius=0.26, stroke_color=BG, stroke_width=2, fill_color=FGF, fill_opacity=1).move_to([XI, ty, 0])
        olab = T("local organizer", 26, FGF).move_to([-0.6, ty - H - 0.45, 0])
        self.at("A local organizer")
        self.play(GrowFromCenter(glow), GrowFromCenter(dot), FadeIn(olab), run_time=0.9)
        outs = VGroup(arr([XI - 0.35, ty, 0], [-1.5, ty, 0], FGF), arr([XI + 0.35, ty, 0], [1.9, ty, 0], FGF),
                      arr([XI, ty + 0.3, 0], [XI, ty + 1.05, 0], FGF, tip=0.16), arr([XI, ty - 0.3, 0], [XI, ty - 1.05, 0], FGF, tip=0.16))
        self.at("It tells the cells")
        self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Line(SpokenScene):
    def construct(self):
        ty = -0.6
        tb = Tube(ty)
        self.add(tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)
        glow = Circle(radius=0.55, stroke_width=0, fill_color=FGF, fill_opacity=0.25).move_to([XI, ty, 0])
        dot = Circle(radius=0.26, stroke_color=BG, stroke_width=2, fill_color=FGF, fill_opacity=1).move_to([XI, ty, 0])
        self.add(glow, dot)
        isth = T("isthmus", 24, TEXT)
        isth_bg = Rectangle(width=isth.width + 0.2, height=isth.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1)
        isth_g = VGroup(isth_bg, isth).move_to([XI, ty + H + 0.38, 0])
        line = DashedLine([XI, ty - H - 0.1, 0], [XI, ty + H + 0.1, 0], color=TEXT, stroke_width=3)
        self.at("The best studied")
        self.play(Indicate(dot, color=FGF, scale_factor=1.5), run_time=0.7)
        self.at("called the isthmus")
        self.play(Create(line), FadeIn(isth_g), run_time=0.8)
        self.at("Two transcription factors")
        self.play(FadeOut(glow), FadeOut(dot), run_time=0.3)
        # both domains overlap at first
        o_bar = bar(-6.0, 1.6, 2.95, OTX, "Otx2")
        g_bar = bar(-0.6, 3.8, 2.3, GBX, "Gbx2")
        self.at("is on in the forebrain")
        self.play(GrowFromEdge(o_bar, LEFT), run_time=0.9)
        self.at("is on in the front")
        self.play(GrowFromEdge(g_bar, RIGHT), run_time=0.9)
        # mutual repression diagram below the tube
        co = chip("Otx2", OTX, 26).move_to([-1.0, -3.15, 0])
        cg = chip("Gbx2", GBX, 26).move_to([2.2, -3.15, 0])
        i1 = inhib([co.get_right()[0] + 0.1, -2.95, 0], [cg.get_left()[0] - 0.1, -2.95, 0])
        i2 = inhib([cg.get_left()[0] - 0.1, -3.35, 0], [co.get_right()[0] + 0.1, -3.35, 0])
        self.at("Each represses the other")
        self.play(FadeIn(co), FadeIn(cg), run_time=0.5)
        self.play(Create(i1), Create(i2), run_time=0.8)
        o2 = bar(-6.0, XI, 2.5, OTX, "Otx2")
        g2 = bar(XI, 3.8, 2.5, GBX, "Gbx2")
        self.at("so the edge")
        self.play(Transform(o_bar, o2), Transform(g_bar, g2), run_time=1.2)
        self.play(Indicate(line, color=TEXT), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Loop(SpokenScene):
    def construct(self):
        ty = -0.6
        tb = Tube(ty)
        self.add(tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)
        o2 = bar(-6.0, XI, 2.5, OTX, "Otx2")
        g2 = bar(XI, 3.8, 2.5, GBX, "Gbx2")
        isth = T("isthmus", 24, TEXT)
        line = DashedLine([XI, ty - H - 0.1, 0], [XI, ty + H + 0.1, 0], color=TEXT, stroke_width=3)
        isth_g = VGroup(Rectangle(width=isth.width + 0.2, height=isth.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1), isth).move_to([XI, ty + H + 0.38, 0])
        self.add(o2, g2, line, isth_g)
        self.at("At that line")
        up = 1.3
        self.play(FadeOut(o2), FadeOut(g2), FadeOut(isth_g), FadeOut(line),
                  *[m.animate.shift(UP * up) for m in (tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)], run_time=1.0)
        ty += up
        enp = poly(-0.9, 1.9, ty, TEXT, 0.16, stroke=2)
        wnt = poly(-0.2, 0.5, ty, WNT, 0.7)
        fgf = poly(0.7, 1.3, ty, FGF, 0.7)
        c_f = chip("Fgf8", FGF, 28).move_to([-3.7, -1.95, 0])
        c_w = chip("Wnt1", WNT, 28).move_to([3.7, -1.95, 0])
        c_e = chip("Engrailed, Pax2/5", TEXT, 28).move_to([0, -3.1, 0])
        L = VGroup(DoubleArrow(c_f.get_right() + RIGHT * 0.1, c_w.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0, tip_length=0.2),
                   DoubleArrow(c_f.get_bottom() + DOWN * 0.1 + RIGHT * 0.5, c_e.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0, tip_length=0.2),
                   DoubleArrow(c_w.get_bottom() + DOWN * 0.1 + LEFT * 0.5, c_e.get_right() + RIGHT * 0.1, color=GREY, stroke_width=4, buff=0, tip_length=0.2))
        self.at("forms a band")
        self.play(FadeIn(fgf), FadeIn(c_f, shift=UP * 0.2), run_time=0.8)
        self.at("forms a ring")
        self.play(FadeIn(wnt), FadeIn(c_w, shift=UP * 0.2), run_time=0.8)
        self.at("span the boundary")
        self.play(FadeIn(enp), FadeIn(c_e, shift=UP * 0.2), run_time=0.8)
        self.at("keep each other")
        self.play(LaggedStart(*[Create(l) for l in L], lag_ratio=0.3), run_time=1.2)
        self.at("Remove")
        x = cross(c_w)
        self.play(Create(x), run_time=0.4)
        self.play(wnt.animate.set_fill(opacity=0.0), fgf.animate.set_fill(opacity=0.2), enp.animate.set_fill(opacity=0.04).set_stroke(opacity=0.3),
                  c_f.animate.set_opacity(0.3), c_e.animate.set_opacity(0.3), c_w.animate.set_opacity(0.3), L.animate.set_opacity(0.25), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Mirror(SpokenScene):
    def construct(self):
        ty = 0.7
        tb = Tube(ty)
        self.add(tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)
        bx = np.array([-3.15, ty + 0.1, 0])
        self.at("Is that enough")
        self.play(Indicate(tb.mid, color=MID, scale_factor=1.03), run_time=0.8)
        b = bead(bx + UP * 2.2)
        blab = T("FGF8 bead", 26, FGF).move_to([-4.9, ty - H - 0.45, 0])
        self.at("in the forebrain")
        self.play(FadeIn(b), run_time=0.2)
        self.play(b.animate.move_to(bx), FadeIn(blab), run_time=0.9)
        glow = Ellipse(width=1.4, height=2.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.14).move_to(bx)
        elab = T("Engrailed on", 26, TEXT).move_to([-1.9, ty - H - 0.45, 0])
        self.at("Cells next to it")
        self.add(glow, b)
        self.play(FadeIn(glow, scale=0.6), FadeIn(elab), run_time=0.9)
        mlab = T("new midbrain", 26, MID).move_to([-1.9, ty - H - 0.45, 0])
        self.at("Later they form")
        self.play(glow.animate.set_stroke(MID).set_fill(MID, 0.45), ReplacementTransform(elab, mlab), run_time=1.0)
        # ---- panel of two graded strips ------------------------------------------------------
        self.at("mirror image")
        self.play(FadeOut(tb.all), FadeOut(glow), FadeOut(b), FadeOut(blab), FadeOut(mlab), run_time=0.7)
        dark, bright = ManimColor("#2B5B33"), ManimColor(GREEN)

        def strip(x0, x1, near_right):
            n = 5
            w = (x1 - x0) / n
            segs = VGroup()
            for i in range(n):
                k = i / (n - 1)
                near = k if near_right else 1 - k
                col = interpolate_color(dark, bright, near)
                segs.add(Rectangle(width=w, height=3.0, stroke_color=BG, stroke_width=3, fill_color=col, fill_opacity=0.95)
                         .move_to([x0 + w * (i + 0.5), 0.3, 0]))
            return segs
        s_norm, s_new = strip(-5.8, -1.8, True), strip(1.8, 5.8, False)
        mir = DashedLine([0, -1.7, 0], [0, 2.9, 0], color=GREY, stroke_width=2)
        c_isth = chip("isthmus", FGF, 26).move_to([-0.9, 0.3, 0])
        c_bead = chip("bead", FGF, 26).move_to([0.9, 0.3, 0])
        l_norm = T("normal midbrain", 28, MID).move_to([-3.8, 2.3, 0])
        l_new = T("new midbrain", 28, MID).move_to([3.8, 2.3, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in s_norm], lag_ratio=0.15), FadeIn(c_isth), FadeIn(l_norm), Create(mir), run_time=1.2)
        n_near = T("near", 26, GREY).move_to([-2.2, -1.5, 0])
        n_far = T("far", 26, GREY).move_to([-5.4, -1.5, 0])
        self.at("nearest the isthmus")
        self.play(FadeIn(n_near), Indicate(s_norm[4], color=WHITE, scale_factor=1.05), run_time=0.8)
        m_near = T("near", 26, GREY).move_to([2.2, -1.5, 0])
        m_far = T("far", 26, GREY).move_to([5.4, -1.5, 0])
        self.at("nearest the bead")
        self.play(FadeIn(c_bead), FadeIn(l_new), LaggedStart(*[FadeIn(s) for s in s_new], lag_ratio=0.15), FadeIn(m_near), run_time=1.2)
        self.at("farther forward")
        self.play(FadeIn(n_far), Indicate(s_norm[0], color=WHITE, scale_factor=1.05), run_time=0.8)
        self.at("farther away")
        self.play(FadeIn(m_far), Indicate(s_new[4], color=WHITE, scale_factor=1.05), run_time=0.8)
        rd = T("cells read their distance from a source", 32).move_to([0, -2.8, 0])
        self.at("read their distance")
        self.play(FadeIn(rd, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Both(SpokenScene):
    def construct(self):
        ty = 0.7
        tb = Tube(ty, cere=True)
        mouse = T("mouse", 28, GREY).move_to([-5.5, 3.6, 0])
        self.add(tb.out, tb.fore, tb.mid, tb.r1, tb.hind, tb.lab)
        lost = poly(X_MID0, X_R1, ty, None, stroke=3, sc=RED)
        lost_mid = poly(X_MID0, XI, ty, None, stroke=3, sc=RED)
        self.at("Now test necessity")
        self.play(FadeIn(mouse), run_time=0.4)
        c1 = chip("no Wnt1", WNT, 30).move_to([0, -1.95, 0])
        self.at("Mouse embryos")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("lack the midbrain")
        self.play(tb.mid.animate.set_fill(opacity=0), tb.r1.animate.set_fill(opacity=0.08), tb.lab[1].animate.set_opacity(0.3),
                  tb.lab[3].animate.set_opacity(0.3), FadeIn(lost_mid), run_time=1.3)
        c2 = chip("greatly reduced Fgf8", FGF, 30).move_to([0, -1.95, 0])
        self.at("greatly reduced")
        self.play(ReplacementTransform(c1, c2), tb.mid.animate.set_fill(MID, 0.25), tb.r1.animate.set_fill(HIND, 0.25),
                  tb.lab[1].animate.set_opacity(1), tb.lab[3].animate.set_opacity(1), FadeOut(lost_mid), run_time=0.7)
        self.at("lose the midbrain")
        self.play(tb.mid.animate.set_fill(opacity=0), tb.r1.animate.set_fill(opacity=0), tb.lab[1].animate.set_opacity(0.3),
                  tb.lab[3].animate.set_opacity(0.3), FadeIn(lost), run_time=1.3)
        # verdict cards
        self.at("Add a factor")
        self.play(FadeOut(c2), tb.mid.animate.set_fill(MID, 0.25), tb.r1.animate.set_fill(HIND, 0.25),
                  tb.lab[1].animate.set_opacity(1), tb.lab[3].animate.set_opacity(1), FadeOut(lost), run_time=0.7)

        def card(x, top, bottom, tag, color):
            r = RoundedRectangle(corner_radius=0.2, width=5.9, height=2.0, stroke_color=color, stroke_width=3,
                                 fill_color=color, fill_opacity=0.12).move_to([x, -2.5, 0])
            t1 = T(top, 28, TEXT).move_to([x, -1.95, 0])
            t2 = T(bottom, 32, color, weight=BOLD).move_to([x, -2.5, 0])
            t3 = T(tag, 26, GREY).move_to([x, -3.05, 0])
            return VGroup(r, t1, t2, t3)
        cL = card(-3.2, "add it where it is absent", "the structure forms", "sufficient", GREEN)
        cR = card(3.2, "remove it", "the structure is lost", "necessary", RED)
        self.play(FadeIn(cL, shift=UP * 0.2), run_time=0.7)
        self.at("Remove it")
        self.play(FadeIn(cR, shift=UP * 0.2), run_time=0.7)
        self.at("You need both")
        self.play(Indicate(cL, color=GREEN, scale_factor=1.04), Indicate(cR, color=RED, scale_factor=1.04), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Add it and the structure forms. Remove it and it is lost."
