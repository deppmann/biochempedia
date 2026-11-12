"""The Climbing Line (global-change, film 1)

COLOR MAP (whole film)
  GOLD   = the isotherm (climate the species needs)
  GREEN  = the species (beetles, their range band)
  RED    = the gap between line and species
  ORANGE = warming / too warm
  COOL   = cool temperature bands
  TEXT   = labels
Mountain scale once the ruler is shown: 0.8 screen units = 100 m (schematic mountain).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
COOL = "#58C4DD"
BROWN = "#8B5A2B"
TREE = "#4E8F3A"

Y_BASE, Y_TOP = -3.5, 3.4
XL0, XR0, PKX = -5.2, 2.4, -1.4
SLOPE = (PKX - XL0) / (Y_TOP - Y_BASE)
Y0 = -1.1
BH = 0.8
U_ISO = 0.4    # 50 m per decade at 0.8 units per 100 m
U_SP = 0.16    # schematic, slower
PX = 4.75
LINE_X1 = 2.2
BR_X = 2.5


def xl(y): return XL0 + (y - Y_BASE) * SLOPE
def xr(y): return XR0 - (y - Y_BASE) * SLOPE
def iso_y(D): return Y0 + U_ISO * D
def sp_y(D): return Y0 + U_SP * D
def lerpc(a, b, t): return interpolate_color(ManimColor(a), ManimColor(b), float(min(1, max(0, t))))


def poly(y0, y1, inset=0.0):
    y0 = max(y0, Y_BASE); y1 = min(y1, Y_TOP)
    if y1 - y0 < 0.02:
        return None
    return Polygon([xl(y0) + inset, y0, 0], [xr(y0) - inset, y0, 0], [xr(y1) - inset, y1, 0], [xl(y1) + inset, y1, 0])


def outline():
    return Polygon([XL0, Y_BASE, 0], [PKX, Y_TOP, 0], [XR0, Y_BASE, 0], stroke_color=TEXT, stroke_width=4,
                   fill_color=TEXT, fill_opacity=0.06)


def beetle(x, y, s=1.0):
    body = Ellipse(width=0.42 * s, height=0.28 * s).set_fill(GREEN, 1).set_stroke(BG, 1.5).move_to([x, y, 0])
    head = Circle(radius=0.09 * s).set_fill(GREEN, 1).set_stroke(BG, 1.5).move_to([x + 0.24 * s, y, 0])
    legs = VGroup(*[Line([x + dx * s, y - 0.1 * s, 0], [x + (dx - 0.03) * s, y - 0.22 * s, 0], color=GREEN, stroke_width=3)
                    for dx in (-0.12, 0.0, 0.12)])
    ant = VGroup(Line([x + 0.3 * s, y + 0.03 * s, 0], [x + 0.42 * s, y + 0.15 * s, 0], color=GREEN, stroke_width=2.5),
                 Line([x + 0.3 * s, y - 0.03 * s, 0], [x + 0.42 * s, y - 0.12 * s, 0], color=GREEN, stroke_width=2.5))
    return VGroup(legs, ant, body, head)


FR = [0.2, 0.35, 0.5, 0.65, 0.8]


def band_bottom(p): return sp_y(p["D"]) + p["Lf"]


def g_bands(p):
    g = VGroup()
    if p["Ab"] <= 0.01:
        return g
    off = U_ISO * p["D"]
    for k in range(-1, 11):
        y0 = Y_BASE + BH * k + off
        pl = poly(y0, y0 + BH)
        if pl is None:
            continue
        c = lerpc(ORANGE, COOL, (k + 1) / 9)
        pl.set_fill(c, 0.34 * p["Ab"]).set_stroke(TEXT, 1, opacity=0.18 * p["Ab"])
        g.add(pl)
    return g


def g_tint(p):
    if p["At"] <= 0.01:
        return VGroup()
    pl = poly(Y_BASE, iso_y(p["D"]))
    if pl is None:
        return VGroup()
    return VGroup(pl.set_fill(ORANGE, 0.22 * p["At"]).set_stroke(width=0))


def g_band(p):
    g = VGroup()
    b = band_bottom(p)
    top = sp_y(p["D"]) + p["bh"]
    if p["Ae"] > 0.01 and top - b > 0.05:
        pl = poly(b, top, inset=0.12)
        if pl is not None:
            gl = p["glow"]
            pl.set_fill(GREEN, (0.3 + 0.25 * gl) * p["Ae"]).set_stroke(GREEN, 3 + 4 * gl, opacity=p["Ae"])
            g.add(pl)
    if p["beet"] > 0.01:
        mid = (b + min(top, b + 0.6)) / 2 if top - b > 0.05 else b + 0.3
        tm = p["tm"]
        for i, f in enumerate(FR):
            yy = mid + 0.04 * np.sin(1.6 * tm + i * 1.3)
            xx = xl(mid) + 0.12 + f * (xr(mid) - xl(mid) - 0.24)
            xx += 0.05 * np.sin(1.1 * tm + i)
            bt = beetle(xx, yy)
            bt.set_opacity(p["beet"])
            g.add(bt)
    return g


def g_gold(p):
    g = VGroup()
    if p["Ag"] <= 0.01:
        return g
    y = iso_y(p["D"])
    x0 = xl(y) - 0.5
    x1 = x0 + (LINE_X1 - x0) * p["Ag"]
    glow = 0.5 + 0.5 * np.sin(2.2 * p["tm"])
    g.add(Line([x0, y, 0], [x1, y, 0], color=GOLD, stroke_width=16, stroke_opacity=0.10 + 0.14 * glow + 0.3 * p["glow2"]))
    g.add(Line([x0, y, 0], [x1, y, 0], color=GOLD, stroke_width=6))
    return g


def g_bracket(p, x=BR_X):
    g = VGroup()
    if p["Ar"] <= 0.01:
        return g
    a = band_bottom(p)
    b = a + (iso_y(p["D"]) - a) * p["Ar"]
    if abs(b - a) < 0.03:
        return g
    for pts in (([x, a, 0], [x, b, 0]), ([x - 0.12, a, 0], [x + 0.12, a, 0]), ([x - 0.12, b, 0], [x + 0.12, b, 0])):
        g.add(Line(*pts, color=RED, stroke_width=6))
    return g


DEFAULT = dict(D=0, Ab=0, Ag=0, At=0, Ae=0, Ar=0, Lf=0, bh=0.6, glow=0, glow2=0, beet=1, tm=0)


def build_world(p):
    return VGroup(g_bands(p), g_tint(p), g_band(p), g_gold(p), g_bracket(p))


class World:
    def __init__(self, **kw):
        base = dict(DEFAULT); base.update(kw); base.pop("tm", None)
        self.v = {k: ValueTracker(x) for k, x in base.items()}
        self.v["mo"] = ValueTracker(kw.get("mo", 0))
        self.tm = ValueTracker(0)
        self.tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.outline = outline()
        self.dyn = always_redraw(lambda: build_world(self.p()))
        self.motes = self._motes()

    def p(self):
        d = {k: t.get_value() for k, t in self.v.items() if k != "mo"}
        d["tm"] = self.tm.get_value()
        return d

    def _motes(self):
        g = VGroup()
        rng = np.random.RandomState(4)
        for i in range(18):
            d = Dot(radius=0.06, color=ORANGE)
            d.fx, d.sp, d.y = rng.uniform(0.1, 0.9), rng.uniform(0.25, 0.5), rng.uniform(Y_BASE, Y_TOP)

            def up(m, dt, self=self):
                m.y += m.sp * dt
                if m.y > Y_TOP - 0.2:
                    m.y = Y_BASE + 0.1
                m.move_to([xl(m.y) + m.fx * (xr(m.y) - xl(m.y)), m.y, 0])
                m.set_opacity(0.55 * self.v["mo"].get_value())
            d.add_updater(up)
            g.add(d)
        return g

    def add(self, sc):
        sc.add(self.outline, self.motes, self.dyn, self.tm)

    def snap(self, **over):
        p = dict(DEFAULT); p.update(over)
        return VGroup(outline(), build_world(p))


def lab(text, size=30, color=TEXT, w=3.9, **kw):
    t = T(text, size, color, **kw)
    if t.width > w:
        t.scale(w / t.width)
    assert size * min(1, w / max(t.width, 1e-6)) >= 21.5 or t.width <= w
    return t


def panel(text, y, size=30, color=TEXT, w=3.9):
    return lab(text, size, color, w).move_to([PX, y, 0])


def counter(w):
    return always_redraw(lambda: M(f"decades: {w.v['D'].get_value():.1f}", 30, TEXT).move_to([PX, 3.25, 0]))


def gold_lab(w):
    return always_redraw(lambda: lab("isotherm", 32, GOLD).move_to([PX, iso_y(w.v["D"].get_value()) - 0.4, 0]))


def sp_lab(w, txt="species"):
    return always_redraw(lambda: lab(txt, 32, GREEN).move_to(
        [PX, sp_y(w.v["D"].get_value()) + w.v["bh"].get_value() + 0.4 + w.v["Lf"].get_value() * 0, 0]))


def ruler(pts_alpha=1):
    g = VGroup(Line([-5.9, Y_BASE, 0], [-5.9, Y_BASE + 0.8 * 8.5, 0], color=TEXT, stroke_width=4))
    for k in range(9):
        y = Y_BASE + 0.8 * k
        g.add(Line([-6.0, y, 0], [-5.8, y, 0], color=TEXT, stroke_width=4))
        g.add(T(str(100 * k), 22, TEXT).move_to([-6.42, y, 0]))
    g.add(T("m", 24, TEXT).move_to([-5.9, 3.55, 0]))
    return g


def thermo(L):
    g = VGroup()
    for k in range(9):
        y = Y_BASE + 0.8 * k
        c = lerpc(ORANGE, COOL, k / 8)
        g.add(RoundedRectangle(corner_radius=0.05, width=0.2, height=0.5).set_stroke(TEXT, 2).move_to([-5.45, y, 0]))
        h = 0.44 * (1 - 0.1 * k * L)
        g.add(Rectangle(width=0.12, height=max(h, 0.02)).set_fill(c, 1).set_stroke(width=0)
              .move_to([-5.45, y - 0.22 + h / 2, 0]))
    return g


class WS(SpokenScene):
    """Scene helper: a live world."""

    def world(self, **kw):
        w = World(**kw)
        w.add(self)
        return w

    def runD(self, w, to, t, **kw):
        self.play(w.v["D"].animate.set_value(to), run_time=t, rate_func=linear, **kw)


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Global Change: Species on the Move"
    TITLE = "The Climbing Line"


class S01Question(WS):
    def construct(self):
        w = self.world(beet=1)
        warm = VGroup(lab("warming:", 34, ORANGE), lab("0.3 °C per decade", 34, ORANGE)).arrange(DOWN, buff=0.15).move_to([PX, 1.2, 0])
        q = T("?", 110, TEXT).move_to([-1.4, 0.7, 0])
        arr = Arrow([-1.4, -0.4, 0], [-1.4, 0.2, 0], color=TEXT, buff=0, stroke_width=8)
        q.t0 = 0
        q.add_updater(lambda m, dt: m.shift(UP * 0.004 * np.sin(3 * w.tm.get_value())))
        self.at("warms")
        self.play(FadeIn(warm, shift=UP * 0.2), w.v["mo"].animate.set_value(1), run_time=1.5)
        self.at("How far uphill")
        self.play(FadeIn(q, shift=UP * 0.3), GrowArrow(arr), run_time=1.2)
        self.play(arr.animate.shift(UP * 0.35), run_time=1.0, rate_func=there_and_back)
        self.at("stay as cool")
        self.play(arr.animate.shift(UP * 0.45), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S02Isotherm(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Lf=0.1)
        warm = panel("warm", -2.9, 34, ORANGE)
        cool = panel("cool", 2.9, 34, COOL)
        q = T("?", 110, TEXT).move_to([-1.4, 0.7, 0])
        arr = Arrow([-1.4, -0.4, 0], [-1.4, 0.2, 0], color=TEXT, buff=0, stroke_width=8)
        wl = VGroup(lab("warming:", 34, ORANGE), lab("0.3 °C per decade", 34, ORANGE)).arrange(DOWN, buff=0.15).move_to([PX, 1.2, 0])
        self.add(q, arr, wl)
        self.at("Picture the slope")
        self.play(FadeOut(q), FadeOut(arr), FadeOut(wl), run_time=0.8)
        self.at("stacked bands")
        self.play(w.v["Ab"].animate.set_value(1), run_time=2.2)
        self.at("warm at the bottom")
        self.play(FadeIn(warm), run_time=0.8)
        self.at("cool at the top")
        self.play(FadeIn(cool), run_time=0.8)
        self.at("The gold line")
        self.play(FadeOut(warm), FadeOut(cool), w.v["Ag"].animate.set_value(1), run_time=1.0)
        gl = VGroup(lab("isotherm", 34, GOLD), lab("equal temperature", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([PX, Y0 - 0.6, 0])
        self.at("isotherm")
        self.play(FadeIn(gl), run_time=0.7)
        self.at("equal temperature")
        sl = panel("species", Y0 + 0.1 + 0.6 + 0.4, 32, GREEN)
        self.play(w.v["Ae"].animate.set_value(1), FadeIn(sl), run_time=1.2)
        self.play(w.v["glow"].animate.set_value(1), run_time=0.5)
        self.play(w.v["glow"].animate.set_value(0), run_time=0.5)
        self.finish()


class S03Edge(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Lf=0.1, Ab=1, Ag=1, Ae=1)
        gl = gold_lab(w)
        sl = panel("species", Y0 + 0.1 + 0.6 + 0.4, 32, GREEN)
        self.add(gl, sl)
        self.at("lives only where")
        self.play(w.v["glow"].animate.set_value(1), run_time=0.8)
        self.play(w.v["glow"].animate.set_value(0), run_time=0.8)
        self.at("So the gold line")
        edge = VGroup(lab("range edge set", 30, GREEN), lab("by temperature", 30, GREEN)).arrange(DOWN, buff=0.1).move_to([PX, -0.45, 0])
        self.play(w.v["Lf"].animate.set_value(0), FadeOut(sl), run_time=0.8)
        self.play(FadeIn(edge), w.v["glow2"].animate.set_value(1), run_time=0.8)
        self.at("warm edge")
        warm = lab("too warm", 34, ORANGE).move_to([-1.3, -2.4, 0])
        self.play(w.v["At"].animate.set_value(1), FadeIn(warm), run_time=1.5)
        self.play(w.v["glow2"].animate.set_value(0), run_time=0.5)
        self.finish()


class S04Warm(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1)
        gl = gold_lab(w)
        self.add(gl)
        edge = VGroup(lab("range edge set", 30, GREEN), lab("by temperature", 30, GREEN)).arrange(DOWN, buff=0.1).move_to([PX, -0.45, 0])
        warm = lab("too warm", 34, ORANGE).move_to([-1.3, -2.4, 0])
        self.add(edge, warm)
        self.at("Now warm")
        c = counter(w)
        self.play(FadeOut(edge), FadeOut(warm), FadeIn(c), w.v["mo"].animate.set_value(1.0), run_time=1.2)
        self.at("Every band slides")
        self.runD(w, 1.0, 4.5)
        self.at("on the move")
        self.play(w.v["glow2"].animate.set_value(1), run_time=0.6)
        self.play(w.v["glow2"].animate.set_value(0), run_time=0.6)
        self.finish()


class S05Lapse(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=1)
        gl = gold_lab(w)
        c = counter(w)
        self.add(gl, c)
        self.at("How fast does")
        self.play(w.v["D"].animate.set_value(0), run_time=0.6)
        self.runD(w, 1.0, 2.2)
        self.at("That depends")
        r = ruler()
        self.play(LaggedStart(*[FadeIn(m) for m in r], lag_ratio=0.08), run_time=2.6)
        self.at("lapse rate")
        L = ValueTracker(0)
        th = always_redraw(lambda: thermo(L.get_value()))
        self.add(th)
        self.at("Here it cools")
        lt = VGroup(lab("lapse rate:", 34, TEXT), lab("0.6 °C per 100 m", 34, COOL)).arrange(DOWN, buff=0.15).move_to([PX, 1.6, 0])
        self.play(FadeIn(lt), run_time=0.8)
        self.play(L.animate.set_value(1), run_time=3.0, rate_func=linear)
        self.finish()


class S06Velocity(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=1)
        gl = gold_lab(w)
        c = counter(w)
        r = ruler()
        self.add(gl, c, r)
        L = ValueTracker(1)
        th = always_redraw(lambda: thermo(L.get_value()))
        self.add(th)
        l1 = lab("0.3 °C per decade", 30, ORANGE).move_to([PX, 2.45, 0])
        self.play(FadeOut(th), w.v["D"].animate.set_value(0), FadeIn(l1, shift=UP * 0.15), run_time=1.0)
        self.remove(th)
        g0 = DashedLine([-5.9, Y0, 0], [xl(Y0) - 0.5, Y0, 0], color=GOLD, stroke_width=3)
        g1 = always_redraw(lambda: DashedLine([-5.9, iso_y(w.v["D"].get_value()), 0],
                                              [xl(iso_y(w.v["D"].get_value())) - 0.5, iso_y(w.v["D"].get_value()), 0],
                                              color=GOLD, stroke_width=3))
        self.add(g0, g1)
        l2 = lab("÷ 0.6 °C per 100 m", 30, COOL).move_to([PX, 1.8, 0])
        l3 = lab("= 0.5 × 100 m", 30, TEXT).move_to([PX, 1.15, 0])
        l4 = lab("= 50 m per decade", 34, GOLD).move_to([PX, 0.45, 0])
        cv = lab("climate velocity", 34, GOLD).move_to([PX, -0.4, 0])
        self.at("by the lapse rate")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.at("The result")
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.8)
        self.at("climate velocity")
        self.play(FadeIn(cv), w.v["glow2"].animate.set_value(1), run_time=0.8)
        self.at("On this slope")
        br = always_redraw(lambda: VGroup(
            Line([-5.5, Y0, 0], [-5.5, iso_y(w.v["D"].get_value()), 0], color=GOLD, stroke_width=7),
            Line([-5.6, Y0, 0], [-5.4, Y0, 0], color=GOLD, stroke_width=7),
            Line([-5.6, iso_y(w.v["D"].get_value()), 0], [-5.4, iso_y(w.v["D"].get_value()), 0], color=GOLD, stroke_width=7)))
        self.add(br)
        self.play(FadeIn(l4, shift=UP * 0.15), w.v["D"].animate.set_value(1), run_time=3.2, rate_func=linear)
        self.play(w.v["glow2"].animate.set_value(0), run_time=0.5)
        self.finish()


class S07Species(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=1)
        gl = gold_lab(w)
        c = counter(w)
        self.add(gl, c)
        self.at("Now let the population")
        sl = sp_lab(w)
        sch = panel("species: schematic", -3.3, 26, TEXT)
        self.play(FadeIn(sl), FadeIn(sch), run_time=0.8)
        self.runD(w, 3.0, 7.6)
        self.finish()


class S08Gap(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=3)
        c = counter(w)
        self.add(c)
        self.at("The red bracket")
        self.play(w.v["Ar"].animate.set_value(1), run_time=1.2)
        gp = lab("gap", 40, RED).move_to([3.5, -0.26, 0])
        self.play(FadeIn(gp), run_time=0.6)
        self.at("Each decade")
        self.play(w.v["D"].animate.set_value(0), FadeOut(gp), run_time=0.9)
        self.runD(w, 3.0, 3.0)
        gp2 = lab("gap", 40, RED).move_to([3.5, -0.26, 0])
        self.add(gp2)
        e1 = lab("gap =", 36, RED).move_to([PX, 2.55, 0])
        e2 = lab("(isotherm speed", 30, GOLD).move_to([PX, 1.95, 0])
        e3 = lab("− species speed)", 30, GREEN).move_to([PX, 1.35, 0])
        e4 = lab("× time", 30, TEXT).move_to([PX, 0.75, 0])
        self.at("started in step")
        fn = VGroup(lab("if the species", 26, TEXT), lab("started in step", 26, TEXT)).arrange(DOWN, buff=0.08).move_to([PX, -2.6, 0])
        self.play(FadeIn(fn), run_time=0.7)
        self.at("the gap is the difference")
        self.play(FadeIn(e1), run_time=0.5)
        self.at("difference in speeds")
        self.play(FadeIn(e2), FadeIn(e3), run_time=1.0)
        self.at("times the time")
        self.play(FadeIn(e4), run_time=0.6)
        self.finish()


class S09Rule(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=3, Ar=1)
        c = counter(w)
        self.add(c)
        mv = always_redraw(lambda: lab("moving", 34, GREEN).move_to([PX, band_bottom(w.p()) - 0.45, 0]))
        nk = always_redraw(lambda: lab("not keeping up", 34, RED).move_to([PX, (band_bottom(w.p()) + iso_y(w.v["D"].get_value())) / 2, 0]))
        self.at("So moving")
        self.play(FadeIn(mv), run_time=0.6)
        self.play(FadeIn(nk), run_time=0.6)
        self.add(mv, nk)
        self.play(w.v["D"].animate.set_value(3.5), run_time=2.4, rate_func=linear)
        self.at("A range keeps")
        ban = VGroup(lab("measure the gap", 34, TEXT), lab("(temperature-set range)", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([PX, -2.5, 0])
        self.play(FadeIn(ban, shift=UP * 0.15), run_time=0.8)
        self.play(w.v["D"].animate.set_value(3.8), run_time=3.0, rate_func=linear)
        self.finish()


# ---------------- split screen
SC, CEN = 0.7, np.array([-1.4, -0.05, 0.0])
SHIFT = np.array([-3.4, 0.25, 0.0])
DS = 3.5


def place(m):
    m.shift(-CEN).scale(SC, about_point=ORIGIN).shift(SHIFT)
    return m


def mscreen(x, y): return (np.array([x, y, 0]) - CEN) * SC + SHIFT


STRIP = (0.6, 6.6, -0.6, 2.0)
GX = 1.6
TK = [GX + 0.98 * j for j in range(6)]


def strip():
    g = VGroup()
    n = 15
    wd = (STRIP[1] - STRIP[0]) / n
    for i in range(n):
        r = Rectangle(width=wd, height=STRIP[3] - STRIP[2]).set_fill(lerpc(ORANGE, COOL, i / (n - 1)), 0.5).set_stroke(width=0)
        r.move_to([STRIP[0] + wd * (i + 0.5), (STRIP[2] + STRIP[3]) / 2, 0])
        g.add(r)
    return g


def pgold(x=GX, a=1.0):
    return VGroup(Line([x, STRIP[2], 0], [x, STRIP[3] + 0.1, 0], color=GOLD, stroke_width=14, stroke_opacity=0.18),
                  Line([x, STRIP[2], 0], [x, STRIP[3] + 0.1, 0], color=GOLD, stroke_width=6))


def ticks(labels):
    g = VGroup(Line([TK[0], -1.0, 0], [TK[-1], -1.0, 0], color=TEXT, stroke_width=3))
    for x, s in zip(TK, labels):
        g.add(Line([x, -1.0, 0], [x, -0.88, 0], color=TEXT, stroke_width=3))
        g.add(T(s.replace(" km", ""), 22, TEXT).move_to([x, -1.35, 0]))
        if s.endswith(" km"):
            g.add(T("km", 22, TEXT).move_to([x, -1.72, 0]))
    return g


TL_FAR = ["0", "40", "80", "120", "160", "200 km"]
TL_NEAR = ["0", "1", "2", "3", "4", "5 km"]


def headers():
    return VGroup(lab("mountain", 32, TEXT, w=4).move_to([-3.4, 3.35, 0]), lab("flat plain", 32, TEXT, w=4).move_to([3.6, 3.35, 0]),
                  Line([0, -2.1, 0], [0, 2.7, 0], color=GREY, stroke_width=2))


def mountain_snap(**over):
    base = dict(D=DS, Ab=1, Ag=1, At=1, Ae=1, Ar=0, beet=1)
    base.update(over)
    return place(VGroup(outline(), build_world(dict(DEFAULT, **base))))


def chips3():
    cs = VGroup(chip("1 m", COOL, 28), chip("100 m", COOL, 28), chip("~1 km", COOL, 28))
    for c, x in zip(cs, (2.3, 3.8, 5.4)):
        c.move_to([x, 1.0, 0])
    return cs


class S10Flat(WS):
    def construct(self):
        snap = VGroup(outline(), build_world(dict(DEFAULT, D=DS, Ab=1, Ag=1, At=1, Ae=1, Ar=1, beet=1)))
        self.add(snap)
        mv = lab("moving", 34, GREEN).move_to([PX, band_bottom(dict(DEFAULT, D=DS)) - 0.45, 0])
        self.add(mv)
        self.play(FadeOut(mv), run_time=0.4)
        self.at("Now set a flat")
        target = mountain_snap()
        hd = headers()
        st = strip()
        self.play(Transform(snap, target), run_time=1.0)
        self.play(FadeIn(hd), LaggedStart(*[FadeIn(r) for r in st], lag_ratio=0.1), run_time=1.4)
        pg = pgold()
        self.play(Create(pg), run_time=0.5)
        self.at("temperature changes toward")
        so = lab("south", 30, ORANGE).move_to([1.3, -2.0, 0])
        no = lab("north", 30, COOL).move_to([5.9, -2.0, 0])
        ar = Arrow([2.3, -2.0, 0], [4.9, -2.0, 0], color=TEXT, buff=0, stroke_width=5)
        self.play(FadeIn(so), FadeIn(no), GrowArrow(ar), run_time=1.2)
        sw = Rectangle(width=0.5, height=STRIP[3] - STRIP[2]).set_fill(TEXT, 0.12).set_stroke(width=0).move_to([STRIP[0], 0.7, 0])
        sw.add_updater(lambda m, dt: (m.shift(RIGHT * 1.0 * dt), m.move_to([STRIP[0], 0.7, 0]) if m.get_x() > STRIP[1] else None))
        self.add(sw)
        self.at("far more slowly")
        tk = ticks(TL_FAR)
        self.play(LaggedStart(*[FadeIn(m) for m in tk], lag_ratio=0.1), run_time=1.6)
        self.finish()


class Split(WS):
    """Rebuild the split frame of S10 (carried)."""

    def frame(self, chips=True, bar_glow=False):
        d = {}
        d["m"] = mountain_snap()
        d["h"] = headers()
        d["s"] = strip()
        d["g"] = pgold()
        d["t"] = ticks(TL_FAR)
        self.add(d["m"], d["h"], d["s"], d["g"], d["t"])
        return d


def bar_left(): return Rectangle(width=0.16, height=0.6).set_fill(GOLD, 1).set_stroke(width=0).move_to([-0.45, -0.35, 0])


class S11Predict(Split):
    def construct(self):
        d = self.frame()
        so = lab("south", 30, ORANGE).move_to([1.3, -2.0, 0])
        no = lab("north", 30, COOL).move_to([5.9, -2.0, 0])
        self.add(so, no)
        self.play(FadeOut(so), FadeOut(no), run_time=0.5)
        cs = chips3()
        for i, c in enumerate(cs):
            c.add_updater(lambda m, dt, i=i: m.shift(UP * 0.0045 * np.sin(2.5 * self.elapsed() + i * 2)))
        bl = bar_left()
        bt = lab("1 m up", 28, GOLD, w=1.4).move_to([-1.2, 0.15, 0])
        self.at("one meter")
        self.play(GrowFromCenter(bl), FadeIn(bt), run_time=0.9)
        self.play(bl.animate.scale(1.3), rate_func=there_and_back, run_time=0.8)
        self.at("A meter")
        self.play(FadeIn(cs[0], shift=UP * 0.2), run_time=0.7)
        self.at("a hundred meters")
        self.play(FadeIn(cs[1], shift=UP * 0.2), run_time=0.7)
        self.at("about a kilometer")
        self.play(FadeIn(cs[2], shift=UP * 0.2), run_time=0.7)
        self.add(*cs)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(mountain_snap(), headers(), strip(), pgold(), ticks(TL_FAR))
        self.add(bar_left(), lab("1 m up", 28, GOLD, w=1.4).move_to([-1.2, 0.15, 0]))
        cs = chips3()
        for i, c in enumerate(cs):
            c.add_updater(lambda m, dt, i=i: m.shift(UP * 0.0045 * np.sin(2.5 * self.elapsed() + i * 2)))
        self.add(*cs)
        cap = lab("Predict: how far poleward equals 1 m uphill?", 28, TEXT, w=9).move_to([0, -3.35, 0])
        self.add(cap)
        n = ValueTracker(5)
        ring = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * (n.get_value() / 5), color=GOLD, stroke_width=7).move_to([0, 3.3, 0]))
        num = always_redraw(lambda: M(str(max(1, int(np.ceil(n.get_value())))), 36, TEXT).move_to([0, 3.3, 0]))
        self.add(ring, num)
        self.play(n.animate.set_value(0.01), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S13Reveal(Split):
    def construct(self):
        d = self.frame()
        bl = bar_left()
        bt = lab("1 m up", 28, GOLD, w=1.4).move_to([-1.2, 0.15, 0])
        cs = chips3()
        self.add(bl, bt, cs)
        self.at("In one European")
        self.play(cs[0].animate.set_opacity(0.2), cs[1].animate.set_opacity(0.2), run_time=0.6)
        self.play(cs[2].animate.scale(1.25).set_stroke(GOLD), run_time=0.8)
        self.at("about a kilometer and")
        newt = ticks(TL_NEAR)
        pb = Rectangle(width=1.47, height=0.3).set_fill(GOLD, 1).set_stroke(width=0).move_to([GX + 0.735, -0.35, 0])
        dot = DashedLine([-0.45, -0.35, 0], [GX, -0.35, 0], color=GOLD, stroke_width=4)
        self.play(Transform(d["t"], newt), FadeOut(cs[0]), FadeOut(cs[1]), FadeOut(cs[2]), run_time=0.8)
        self.play(FadeIn(dot), GrowFromEdge(pb, LEFT), run_time=1.0)
        zi = lab("zoomed in", 24, TEXT).move_to([3.0, -1.75, 0])
        self.add(zi)
        self.at("A short climb")
        l1 = lab("same cooling: 1 m up ≈ 1.5 km poleward", 32, GOLD, w=9).move_to([0, -2.75, 0])
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.8)
        self.at("The exchange rate")
        l2 = lab("one European example; varies by region and season", 26, TEXT, w=10).move_to([0, -3.4, 0])
        self.play(FadeIn(l2), run_time=0.8)
        self.play(pb.animate.set_opacity(0.6), rate_func=there_and_back, run_time=1.2)
        self.finish()


def pband(x0=GX, w=0.6):
    r = Rectangle(width=w, height=STRIP[3] - STRIP[2] - 0.2).set_fill(GREEN, 0.35).set_stroke(GREEN, 3).move_to([x0 + w / 2, 0.7, 0])
    bts = VGroup(*[beetle(x0 + w / 2, y, 0.8) for y in (0.0, 0.7, 1.4)])
    return VGroup(r, bts)


GP2 = GX + 0.84


class S14Own(Split):
    def construct(self):
        d = self.frame()
        pb = pband()
        self.add(pb)
        self.at("raw distances")
        c1 = chip("11 m", GREEN, 30).move_to([-3.4, -2.75, 0])
        c2 = chip("17 km", GREEN, 30).move_to([3.6, -2.75, 0])
        ar = DoubleArrow([-1.7, -2.75, 0], [1.7, -2.75, 0], color=TEXT, buff=0, stroke_width=5)
        x = VGroup(Line([-0.3, -2.45, 0], [0.3, -3.05, 0], color=RED, stroke_width=8), Line([-0.3, -3.05, 0], [0.3, -2.45, 0], color=RED, stroke_width=8))
        nt = lab("raw distances: not comparable", 28, TEXT, w=8).move_to([0, -3.5, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)
        self.play(GrowFromCenter(ar), run_time=0.6)
        self.play(Create(x), FadeIn(nt), run_time=0.8)
        self.at("Each shift is judged")
        mb = place(VGroup(g_bracket(dict(DEFAULT, D=DS, Ae=1, Ar=1))))
        pgn = pgold(GP2)
        self.play(Transform(d["g"], pgn), run_time=0.7)
        pbr = VGroup(*[Line(*pts, color=RED, stroke_width=6) for pts in (
            ([GX, 2.3, 0], [GP2, 2.3, 0]), ([GX, 2.18, 0], [GX, 2.42, 0]), ([GP2, 2.18, 0], [GP2, 2.42, 0]))])
        self.play(Create(mb), Create(pbr), run_time=0.7)
        self.at("its own isotherm")
        self.play(Indicate(d["g"], color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("slope or plain")
        g2 = lab("gap", 30, RED).move_to([GX + 0.42, 2.75, 0])
        self.play(FadeIn(g2), run_time=0.6)
        self.finish()


class S15Chen(WS):
    def construct(self):
        a = ValueTracker(0)
        b = ValueTracker(0)
        t1 = lab("median poleward", 34, TEXT).move_to([0, 2.7, 0])
        n1 = always_redraw(lambda: VGroup(M(f"{a.get_value():.1f}", 90, GREEN), T("km per decade", 34, GREEN)).arrange(RIGHT, buff=0.4, aligned_edge=DOWN).move_to([0, 1.55, 0]))
        t2 = lab("median uphill", 34, TEXT).move_to([0, 0.0, 0])
        n2 = always_redraw(lambda: VGroup(M(f"{b.get_value():.1f}", 90, GREEN), T("m per decade", 34, GREEN)).arrange(RIGHT, buff=0.4, aligned_edge=DOWN).move_to([0, -1.15, 0]))
        src = lab("Chen and colleagues, Science, 2011", 30, TEXT, w=10).move_to([0, -3.1, 0])
        h = lab("land species, pooled studies", 32, GOLD, w=10).move_to([0, 3.4, 0])
        self.at("A 2011")
        self.play(FadeIn(src), FadeIn(h), run_time=1.0)
        self.at("The median shifts")
        self.play(FadeIn(t1), run_time=0.6)
        self.add(n1, n2)
        self.at("17 kilometers")
        self.play(a.animate.set_value(16.9), run_time=1.6)
        self.play(FadeIn(t2), run_time=0.6)
        self.at("11 meters")
        self.play(b.animate.set_value(11.0), run_time=1.6)
        self.finish()


class S16Spread(Split):
    def construct(self):
        d = self.frame()
        pgn = pgold(GP2)
        self.remove(d["g"])
        self.add(pgn)
        rng = np.random.RandomState(11)
        gy = iso_y(DS)
        md, pdts = VGroup(), VGroup()
        ys = []
        for i in range(22):
            y = float(np.clip(gy - 0.5 + rng.normal(0, 0.55), Y_BASE + 0.3, Y_TOP - 0.4))
            ys.append(y)
            x = xl(y) + 0.3 + rng.uniform(0, 1) * (xr(y) - xl(y) - 0.6)
            md.add(Dot(mscreen(x, y), radius=0.09, color=GREEN))
        xs = []
        for i in range(22):
            x = float(np.clip(GP2 + rng.normal(0, 0.8), 0.8, 6.4))
            xs.append(x)
            pdts.add(Dot([x, rng.uniform(-0.45, 1.85), 0], radius=0.09, color=GREEN))
        sch = lab("dots: schematic", 26, TEXT).move_to([3.6, -1.95, 0])
        self.at("But the medians")
        self.play(LaggedStart(*[FadeIn(m, scale=1.8) for m in md], lag_ratio=0.1), LaggedStart(*[FadeIn(m, scale=1.8) for m in pdts], lag_ratio=0.1), FadeIn(sch), run_time=3.0)
        mm = mscreen(0, float(np.median(ys)))[1]
        t1 = Line([-5.0, mm, 0], [-0.9, mm, 0], color=TEXT, stroke_width=6)
        t2 = Line([float(np.median(xs)), STRIP[2] - 0.05, 0], [float(np.median(xs)), STRIP[3] + 0.05, 0], color=TEXT, stroke_width=6)
        self.play(Create(t1), Create(t2), run_time=1.0)
        ml = lab("median", 26, TEXT).move_to([-5.9, mm, 0])
        self.add(ml)
        self.at("ran ahead")
        a1 = lab("ahead", 30, GREEN).move_to([-5.9, mscreen(0, gy + 1.0)[1], 0])
        self.play(FadeIn(a1), run_time=0.6)
        self.at("lagged behind")
        b1 = lab("behind", 28, GREEN).move_to([-6.05, mscreen(0, gy - 1.45)[1], 0])
        self.play(FadeIn(b1), run_time=0.6)
        self.play(*[m.animate.shift(UP * 0.05) for m in md], rate_func=there_and_back, run_time=1.2)
        self.finish()


def tree(x, y, s=0.5):
    return VGroup(Line([x, y - 0.15 * s, 0], [x, y + 0.25 * s, 0], color=BROWN, stroke_width=4),
                  Polygon([x - 0.35 * s, y + 0.2 * s, 0], [x, y + 1.0 * s, 0], [x + 0.35 * s, y + 0.2 * s, 0]).set_fill(TREE, 0.9).set_stroke(TREE, 2))


class S17Cause(WS):
    def construct(self):
        w = self.world(Ag=1, Ab=1, bh=1.4, beet=0, mo=0)
        w.v["Ab"].set_value(0.5)
        trees = VGroup()
        for row, y in enumerate((-3.1, -2.4, -1.7, -1.0, -0.3, 0.4, 1.1)):
            n = int((xr(y) - xl(y) - 0.8) / 0.8)
            for j in range(n + 1):
                trees.add(tree(xl(y) + 0.4 + j * 0.8, y))
        for t in trees:
            t.yc = t.get_center()[1]
        Fy = ValueTracker(Y_BASE)

        def hide(g):
            for t in g:
                t.set_opacity(0 if t.yc - 0.2 < Fy.get_value() else 1)
        trees.add_updater(hide)
        field = always_redraw(lambda: (poly(Y_BASE, Fy.get_value()) or VGroup()).set_fill(BROWN, 0.55).set_stroke(width=0) if Fy.get_value() > Y_BASE + 0.05 else VGroup())
        self.add(trees, field)
        gl = lab("isotherm", 32, GOLD).move_to([PX, Y0 - 0.4, 0])
        self.add(gl)
        self.at("One last")
        self.play(FadeIn(trees), run_time=1.0)
        self.at("For a forest beetle")
        fb = lab("a forest beetle", 34, GREEN).move_to([PX, 1.45, 0])
        self.play(w.v["Ae"].animate.set_value(1), w.v["beet"].animate.set_value(1), FadeIn(fb), run_time=1.2)
        self.at("clearing the lower")
        self.play(Fy.animate.set_value(-0.4), run_time=1.3, rate_func=linear)
        self.at("lift the range's")
        ar = Arrow([2.7, -1.1, 0], [2.7, -0.45, 0], color=GREEN, buff=0, stroke_width=7)
        fl = VGroup(lab("forest loss can also", 30, TEXT), lab("push a range uphill", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([PX, 0.35, 0])
        self.play(w.v["Lf"].animate.set_value(0.7), GrowArrow(ar), FadeIn(fl), run_time=1.6)
        self.at("whatever the temperature")
        self.play(w.v["glow2"].animate.set_value(1), run_time=0.8)
        self.play(w.v["glow2"].animate.set_value(0), run_time=0.8)
        self.at("A shift shows")
        ban = VGroup(lab("a shift shows change,", 34, TEXT), lab("not its cause", 34, GOLD)).arrange(DOWN, buff=0.12).move_to([PX, -2.9, 0])
        self.play(FadeIn(ban, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S18Close(WS):
    def construct(self):
        w = self.world(beet=1, mo=1, Ab=1, Ag=1, Ae=1, At=1, D=2, Ar=1)
        c = counter(w)
        self.add(c)
        l1 = VGroup(lab("A range keeps up", 36, TEXT), lab("only by moving", 36, TEXT)).arrange(DOWN, buff=0.12).move_to([PX, 2.0, 0])
        self.play(FadeIn(l1), run_time=0.6)
        self.add(l1)
        self.at("as fast as")
        l2 = VGroup(lab("as fast as", 40, GOLD), lab("its isotherm", 40, GOLD)).arrange(DOWN, buff=0.12).move_to([PX, 0.7, 0])
        self.play(FadeIn(l2, shift=UP * 0.15), w.v["glow2"].animate.set_value(1), run_time=0.7)
        self.runD(w, 4.0, 2.4)
        self.finish()


class S19End(EndCard):
    LINE = "A range keeps up only by moving as fast as its isotherm."
