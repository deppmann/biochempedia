"""Spectrophotometry and enzyme kinetics: timing an enzyme with a beam of light  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All plots are computed from the equations and tagged "idealised". No structures are drawn.

COLOR MAP (one color per concept, whole video)
  BLUE   = the apparatus and the enzymes (lamp, cuvette, detector, kinases, dehydrogenases)
  YELLOW = light and absorbance (the 340 nm beam, the A340 progress curves)
  PURPLE = NADH (the thing that absorbs); NAD+ is shown GREY
  TEAL   = substrate
  GREEN  = rate, the initial slope, the fitted curve, the controls that fix a pitfall
  ORANGE = an inhibitor (the inhibited line)
  RED    = the pitfall or the trap
  GOLD   = dates, Vmax / Km markers, the closing rule
  GREY   = structure, axes, de-emphasised text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

VMAX_SC, KM_SC = 6.0, 2.5     # schematic constants for the progress-curve family (arbitrary units)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def dashed(a, b, color=GREY, w=3):
    return DashedLine(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), color=color, stroke_width=w,
                      dash_length=0.12)


def dot(p, color=YELLOW, r=0.09):
    return Dot(np.array([p[0], p[1], 0.0]), radius=r, color=color)


def mm(S, vmax=VMAX_SC, km=KM_SC):
    return vmax * S / (km + S)


class Plot:
    """Screen box (x0..x1, y0..y1) mapped to data ranges xr, yr. Axes cross at (xr[0], yr[0]) unless given."""

    def __init__(self, x0, x1, y0, y1, xr, yr, xlabel="", ylabel="", cross=None, lsize=24, ylabel_pos="top"):
        self.x0, self.x1, self.y0, self.y1, self.xr, self.yr = x0, x1, y0, y1, xr, yr
        cx, cy = cross if cross else (xr[0], yr[0])
        a = self.pt(xr[1], cy)
        b = self.pt(cx, yr[1])
        self.xaxis = arr(self.pt(xr[0], cy), a + RIGHT * 0.25, GREY, w=3, tip=0.16)
        self.yaxis = arr(self.pt(cx, yr[0]), b + UP * 0.25, GREY, w=3, tip=0.16)
        self.xl = lab(xlabel, lsize).next_to(self.pt(xr[1], cy), DOWN, buff=0.18).align_to(self.pt(xr[1], cy), RIGHT) if xlabel else VGroup()
        if ylabel:
            yl = lab(ylabel, lsize)
            if ylabel_pos == "top":
                yl.next_to(self.pt(cx, yr[1]), UP, buff=0.34)
                yl.align_to(self.pt(cx, yr[1]) + LEFT * 0.0, LEFT)
            self.yl = yl
        else:
            self.yl = VGroup()
        self.axes = VGroup(self.xaxis, self.yaxis, self.xl, self.yl)

    def pt(self, x, y):
        sx = self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.x1 - self.x0)
        sy = self.y0 + (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.y1 - self.y0)
        return np.array([sx, sy, 0.0])

    def curve(self, f, xa, xb, color=YELLOW, w=5, n=90):
        xs = np.linspace(xa, xb, n)
        return poly([self.pt(x, f(x)) for x in xs], color, w)

    def seg(self, xa, ya, xb, yb, color=GREEN, w=5):
        return poly([self.pt(xa, ya), self.pt(xb, yb)], color, w)

    def dseg(self, xa, ya, xb, yb, color=GREY, w=3):
        return dashed(self.pt(xa, ya), self.pt(xb, yb), color, w)

    def dot(self, x, y, color=YELLOW, r=0.09):
        return dot(self.pt(x, y), color, r)


def cuvette(cx, cy, w=1.5, h=2.2, fill=None, fill_frac=0.8, fill_op=0.28):
    body = Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
    liquid = Rectangle(width=w - 0.1, height=(h - 0.1) * fill_frac, stroke_width=0, fill_color=fill or BLUE,
                       fill_opacity=fill_op)
    liquid.move_to([cx, cy - h / 2 + 0.05 + (h - 0.1) * fill_frac / 2, 0])
    return VGroup(body, liquid)


def box(label, cx, cy, w, h, color=BLUE, size=24):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.13).move_to([cx, cy, 0])
    t = T(label, size, color).move_to(r)
    return VGroup(r, t)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Timing an Enzyme with a Beam of Light"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """velocity is a slope; watch a reaction run; doubling substrate stops doubling the rate (saturation)."""

    def construct(self):
        # left: product against time
        L = Plot(-6.0, -0.9, -2.5, 2.3, (0, 10), (0, 10), "time", "product formed")
        tag1 = lab("idealised", 22).move_to([-3.4, -3.15, 0])

        self.at("Velocity is a slope")
        line = L.seg(0.4, 0.9, 9.4, 9.0, YELLOW, 6)
        self.play(Create(L.axes), Create(line), run_time=1.0)
        a, b, c = L.pt(2.4, 2.7), L.pt(7.0, 2.7), L.pt(7.0, 6.9)
        run = dashed(a, b, GREEN, 4)
        rise = dashed(b, c, GREEN, 4)
        vlab = lab("velocity = slope", 26, GREEN).move_to(L.pt(4.4, 7.2))
        self.play(Create(run), Create(rise), FadeIn(vlab), FadeIn(tag1), run_time=0.9)

        self.at("watching a reaction run")
        marker = dot(L.pt(0.4, 0.9), YELLOW, 0.17)
        self.add(marker)
        self.play(MoveAlongPath(marker, line), run_time=1.8, rate_func=linear)

        # right: rate against substrate
        R = Plot(1.2, 6.2, -2.5, 2.3, (0, 9), (0, 6), "substrate", "rate")
        self.at("Doubling the substrate")
        self.play(Create(R.axes), run_time=0.6)
        S_vals = [1, 2, 4, 8]
        bars = VGroup()
        labs = VGroup()
        for i, s in enumerate(S_vals):
            xc = 1.2 + (i + 0.7) * 1.15
            h = mm(s, 6.0, 2.0) / 6.0 * 4.3
            base = R.pt(0, 0)[1]
            bar = Rectangle(width=0.8, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                            fill_opacity=0.4).move_to([xc, base + h / 2, 0])
            bars.add(bar)
            labs.add(lab(f"{s}×", 22, TEAL).next_to(bar, DOWN, buff=0.08).shift(DOWN * 0.0))
        # keep substrate multiples above the axis label row: place them inside the bar bottoms
        for l, bar in zip(labs, bars):
            l.move_to(bar.get_bottom() + UP * 0.28)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.35), FadeIn(labs), run_time=2.4)

        self.at("levels off")
        vm = R.dseg(0, 6.0, 9, 6.0, GOLD, 3)
        vl = lab("Vmax", 26, GOLD).next_to(R.pt(0, 6.0), LEFT, buff=0.12)
        vl.shift(RIGHT * 0.0)
        self.play(Create(vm), FadeIn(vl), FadeIn(lab("idealised", 22).move_to([3.7, -3.15, 0])), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Light(SpokenScene):
    """NADH absorbs 340 nm light, NAD+ does not; dehydrogenases followed by A340; coupling via pyruvate kinase + LDH."""

    def construct(self):
        rng = np.random.RandomState(4)
        cy = 1.3
        lamp = box("lamp", -5.2, cy, 1.9, 1.5, BLUE, 28)
        cu = cuvette(-0.7, cy, 2.2, 3.2, fill=BLUE, fill_frac=0.82)
        det = box("detector", 4.6, cy, 2.3, 1.5, BLUE, 28)
        beam1 = Line([-4.25, cy, 0], [-1.8, cy, 0], color=YELLOW, stroke_width=12)
        beam2 = Line([0.4, cy, 0], [3.4, cy, 0], color=YELLOW, stroke_width=12)
        wl = lab("340 nm light", 26, YELLOW).move_to([-3.0, cy + 0.55, 0])
        cul = lab("cuvette", 24).move_to([-0.7, cy + 1.95, 0])
        reading = M("A340: low", 30, YELLOW).move_to([4.6, cy - 1.25, 0])

        self.at("Pick a reaction")
        self.play(FadeIn(lamp), FadeIn(cu), FadeIn(det), FadeIn(cul), run_time=0.8)
        self.play(Create(beam1), Create(beam2), FadeIn(wl), FadeIn(reading), run_time=0.8)

        pts = []
        for _ in range(18):
            pts.append([-0.7 + rng.uniform(-0.85, 0.85), cy - 1.4 + rng.uniform(0.1, 2.35)])
        dots = VGroup(*[Dot([p[0], p[1], 0], radius=0.13, color=PURPLE) for p in pts])
        chip_pos = [-0.7, cy - 2.2, 0]
        chip_nadh = chip("NADH", PURPLE, 28).move_to(chip_pos)
        chip_nad = chip("NAD+", GREY, 28).move_to(chip_pos)

        self.at("absorbs at")
        self.play(FadeIn(dots), FadeIn(chip_nadh), beam2.animate.set_opacity(0.2),
                  Transform(reading, M("A340: high", 30, YELLOW).move_to(reading)), run_time=0.9)

        self.at("does not")
        grey = VGroup(*[Dot([p[0], p[1], 0], radius=0.13, color=GREY) for p in pts])
        self.play(Transform(dots, grey), Transform(chip_nadh, chip_nad), beam2.animate.set_opacity(1.0),
                  Transform(reading, M("A340: low", 30, YELLOW).move_to(reading)), run_time=0.9)

        self.at("makes or uses")
        up = VGroup(chip("makes NADH", PURPLE, 26), T("A340 rises", 26, YELLOW))
        up.arrange(RIGHT, buff=0.3)
        dn = VGroup(chip("uses NADH", PURPLE, 26), T("A340 falls", 26, YELLOW))
        dn.arrange(RIGHT, buff=0.3)
        both = VGroup(up, dn).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -2.45, 0])
        self.play(FadeIn(up, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(dn, shift=UP * 0.1), run_time=0.7)

        self.at("couple it")
        purple = VGroup(*[Dot([p[0], p[1], 0], radius=0.13, color=PURPLE) for p in pts])
        self.play(FadeOut(both), Transform(dots, purple),
                  Transform(chip_nadh, chip("NADH", PURPLE, 28).move_to(chip_pos)), beam2.animate.set_opacity(0.2),
                  Transform(reading, M("A340: high", 30, YELLOW).move_to(reading)), run_time=0.8)

        c1 = chip("pyruvate kinase", BLUE, 25)
        c2 = chip("pyruvate", GREEN, 25)
        c3 = chip("lactate dehydrogenase", BLUE, 25)
        a1 = arr(LEFT * 0.3, RIGHT * 0.3, GREY, w=4, tip=0.16)
        a2 = a1.copy()
        chain = VGroup(c1, a1, c2, a2, c3).arrange(RIGHT, buff=0.2).move_to([0, -2.6, 0])
        self.at("Pyruvate kinase makes")
        self.play(FadeIn(c1), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(c2), run_time=0.6)
        self.at("lactate dehydrogenase")
        self.play(GrowArrow(a2), FadeIn(c3), run_time=0.6)

        self.at("consumes")
        usedchip = chip("NADH", PURPLE, 24).move_to([c3.get_center()[0], -1.45, 0])
        dwn = arr([usedchip.get_center()[0], usedchip.get_bottom()[1] - 0.02, 0],
                  [c3.get_center()[0], c3.get_top()[1] + 0.03, 0], PURPLE, w=4, tip=0.16)
        self.play(FadeIn(usedchip), Create(dwn), dots.animate.set_opacity(0.15),
                  beam2.animate.set_opacity(1.0), Transform(reading, M("A340: falls", 30, YELLOW).move_to(reading)),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Curve(SpokenScene):
    """mix, start, read A340 every few seconds within the linear range, Beer-Lambert turns delta A into delta concentration."""

    def construct(self):
        CX, CY = -4.8, -0.2
        cu = cuvette(CX, CY, 2.0, 3.2, fill=BLUE, fill_frac=0.0)
        self.add(cu)
        names = [("buffer", GREY), ("coenzyme", PURPLE), ("enzyme", BLUE), ("substrate", TEAL)]
        liquid = cu[1]
        self.at("Mix buffer")
        for i, (nm, col) in enumerate(names):
            if i == 3:
                self.at("add substrate")
            elif i > 0:
                self.at(nm)
            c = chip(nm, col, 26).move_to([CX, 2.6, 0])
            self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.15)
            target = cuvette(CX, CY, 2.0, 3.2, fill=BLUE, fill_frac=0.25 * (i + 1))
            self.play(c.animate.move_to([CX, 1.7, 0]).set_opacity(0.0), Transform(liquid, target[1]), run_time=0.35)
            self.remove(c)
        self.at("to start")
        go = T("start", 30, GREEN, weight=BOLD).move_to([CX, -2.35, 0])
        self.play(FadeIn(go, scale=1.2), run_time=0.4)

        P = Plot(-2.6, 6.0, -0.45, 3.2, (0, 60), (0, 1.5), "time (s)", "A340")

        def A(t):  # idealised falling progress curve
            return 1.35 - 1.0 * (1 - np.exp(-t / 35.0))
        curve = P.curve(A, 0, 60, YELLOW, 5)
        self.at("Record the absorbance")
        self.play(Create(P.axes), run_time=0.6)
        ts = list(range(0, 61, 5))
        dots = VGroup(*[P.dot(t, A(t), YELLOW, 0.1) for t in ts])
        self.at("short intervals")
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.28), run_time=3.2)
        self.play(Create(curve), run_time=0.8)
        tagi = lab("idealised", 22).move_to(P.pt(52, 1.4))
        self.add(tagi)

        self.at("linear range")
        band = Rectangle(width=P.pt(60, 0)[0] - P.pt(0, 0)[0], height=P.pt(0, 1.45)[1] - P.pt(0, 0.1)[1],
                         stroke_width=0, fill_color=GREEN, fill_opacity=0.14).move_to(
            [(P.pt(60, 0)[0] + P.pt(0, 0)[0]) / 2, (P.pt(0, 1.45)[1] + P.pt(0, 0.1)[1]) / 2, 0])
        bl = lab("linear range", 24, GREEN).move_to(P.pt(48, 0.3))
        self.play(FadeIn(band), FadeIn(bl), FadeOut(tagi), run_time=0.8)

        self.at("turns that change")
        f1 = lines("change in concentration =", "change in A340 / (ε × path length)", size=26, color=TEXT, buff=0.1,
                   align=ORIGIN)
        f1.move_to([1.7, -1.75, 0])
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.9)
        self.at("epsilon is")
        f2 = M("NADH: ε = 6,220 per M per cm", 26, PURPLE).move_to([1.7, -2.85, 0])
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rate(SpokenScene):
    """early straight slope = initial velocity; slopes at many substrate levels build the saturation curve; Vmax and Km."""

    def construct(self):
        L = Plot(-6.1, -0.9, -2.2, 2.7, (0, 60), (0, 1.9), "time", "A340")
        R = Plot(1.0, 6.2, -2.2, 2.7, (0, 10), (0, 6.4), "substrate", "rate")
        Svals = [1.0, 2.5, 5.0, 10.0]
        A0 = 1.6
        TAU = 40.0

        def prog(v):
            return lambda t: A0 - 0.006 * v * TAU * (1 - np.exp(-t / TAU))

        vs = [mm(s) for s in Svals]
        self.at("straight early part")
        c2 = L.curve(prog(vs[2]), 0, 60, YELLOW, 5)
        self.play(Create(L.axes), Create(c2), run_time=1.0)
        tans = [L.seg(0, A0, 16, A0 - 0.006 * v * 16, GREEN, 7) for v in vs]
        self.play(Create(tans[2]), run_time=0.7)
        self.at("initial velocity")
        sl = lab("slope = initial velocity", 26, GREEN).move_to(L.pt(34, 1.78))
        self.play(FadeIn(sl), run_time=0.6)

        self.at("many substrate")
        others = [L.curve(prog(vs[i]), 0, 60, YELLOW, 5) for i in (0, 1, 3)]
        order = [others[0], others[1], others[2]]
        self.play(FadeOut(sl), LaggedStart(*[Create(o) for o in order], lag_ratio=0.5), run_time=1.6)
        self.play(*[Create(tans[i]) for i in (0, 1, 3)], run_time=0.8)

        self.at("Each slope is one point")
        self.play(Create(R.axes), run_time=0.5)
        dts = VGroup(*[R.dot(s, v, GREEN, 0.14) for s, v in zip(Svals, vs)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in dts], lag_ratio=0.4), run_time=1.6)
        tagi = lab("idealised", 22).move_to([3.6, -3.2, 0])
        self.add(tagi)

        self.at("Fit the curve")
        hyp = R.curve(lambda s: mm(s), 0, 10, GREEN, 6)
        mmlab = lab("Michaelis-Menten enzyme (idealised)", 22).move_to([3.4, -3.2, 0])
        self.play(Create(hyp), Transform(tagi, mmlab), run_time=1.2)

        self.at("nonlinear regression")
        nr = lab("nonlinear regression", 24, GREEN).move_to(R.pt(6.0, 1.0))
        self.play(FadeIn(nr), run_time=0.5)

        self.at("concentration at half")
        vm = R.dseg(0, VMAX_SC, 10, VMAX_SC, GOLD, 3)
        vml = lab("Vmax", 24, GOLD).next_to(R.pt(10, VMAX_SC), UP, buff=0.05).shift(LEFT * 0.4)
        half = R.dseg(0, VMAX_SC / 2, KM_SC, VMAX_SC / 2, GOLD, 3)
        down = R.dseg(KM_SC, VMAX_SC / 2, KM_SC, 0, GOLD, 3)
        hl = lab("half Vmax", 22, GOLD).move_to(R.pt(6.2, 2.5))
        kml = lab("Km", 24, GOLD).next_to(R.pt(KM_SC, 0), DOWN, buff=0.1)
        self.play(Create(vm), FadeIn(vml), run_time=0.7)
        self.play(Create(half), Create(down), FadeIn(hl), FadeIn(kml), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """worked example Vmax 60, Km 4, S 12 -> 45; double-reciprocal intercepts; competitive / uncompetitive / noncompetitive."""

    def construct(self):
        VM, KM = 60.0, 4.0

        def v(s):
            return VM * s / (KM + s)

        P = Plot(-5.8, 1.9, -2.5, 2.8, (0, 20), (0, 70), "[S] (mM)", "v (µmol/min)")
        tagi = lab("idealised example", 24).move_to([4.4, 3.0, 0])
        self.at("example")
        self.play(Create(P.axes), FadeIn(tagi), run_time=0.8)
        curve = P.curve(v, 0, 20, GREEN, 6)
        self.at("V max is")
        vm = P.dseg(0, VM, 20, VM, GOLD, 3)
        vml = lab("Vmax = 60", 24, GOLD).move_to(P.pt(14, 65))
        self.play(Create(curve), Create(vm), FadeIn(vml), run_time=1.2)
        self.at("is 4")
        hf = P.dseg(0, 30, KM, 30, GOLD, 3)
        hd = P.dseg(KM, 30, KM, 0, GOLD, 3)
        kml = lab("Km = 4", 24, GOLD).next_to(P.pt(KM, 0), DOWN, buff=0.1).shift(RIGHT * 0.15)
        self.play(Create(hf), Create(hd), FadeIn(kml), run_time=0.9)

        self.at("At 12")
        vv = P.dseg(12, 0, 12, 45, TEAL, 4)
        pdot = P.dot(12, 45, TEAL, 0.14)
        s12 = lab("[S] = 12", 24, TEAL).next_to(P.pt(12, 0), DOWN, buff=0.1).shift(RIGHT * 0.0)
        self.play(Create(vv), FadeIn(pdot), FadeIn(s12), run_time=0.9)
        self.at("three quarters")
        hh = P.dseg(0, 45, 12, 45, TEAL, 4)
        v45 = lab("v = 45", 26, TEAL).move_to(P.pt(15.5, 38))
        q = lab("¾ of Vmax", 24, GOLD).move_to(P.pt(15.5, 31))
        self.play(Create(hh), FadeIn(v45), FadeIn(q), run_time=0.9)

        eq = M("v = 60 × 12 / (4 + 12)", 22, TEXT).move_to([4.3, 0.4, 0])
        eq2 = M("  = 45", 24, TEXT).next_to(eq, DOWN, buff=0.15, aligned_edge=LEFT)
        eqs = VGroup(eq, eq2)
        self.play(FadeIn(eqs, shift=LEFT * 0.1), run_time=0.7)

        # beat 2: double-reciprocal
        self.at("plot 1 over")
        old = VGroup(P.axes, curve, vm, vml, hf, hd, kml, vv, pdot, s12, hh, v45, q, tagi, eqs)
        self.play(FadeOut(old), run_time=0.6)
        Q = Plot(-5.8, 2.0, -2.5, 2.8, (-0.4, 1.0), (-0.03, 0.095), "1/[S]", "1/v", cross=(0, 0))
        y_int = 1.0 / VM
        slope = KM / VM

        def lb(x):
            return y_int + slope * x
        green = Q.seg(-0.25, 0.0, 1.0, lb(1.0), GREEN, 6)
        self.play(Create(Q.axes), run_time=0.5)
        self.play(Create(green), run_time=0.9)
        tg = lab("idealised", 22).move_to([4.9, 3.0, 0])
        lbn = lab("Lineweaver-Burk plot", 26, TEXT).move_to([4.5, 2.55, 0])
        self.add(tg, lbn)
        self.at("intercept")
        yd = Q.dot(0, y_int, GOLD, 0.15)
        yl = lines("y-intercept", "= 1/Vmax", size=26, color=GOLD, buff=0.1).move_to([4.9, 1.7, 0])
        yarr = arr(yl.get_left() + LEFT * 0.15, Q.pt(0, y_int) + RIGHT * 0.3, GOLD, w=3, tip=0.16)
        self.play(FadeIn(yd, scale=1.6), FadeIn(yl), Create(yarr), run_time=0.8)
        self.at("intercept", nth=1)
        xd = Q.dot(-0.25, 0.0, GOLD, 0.15)
        xl = lines("x-intercept", "= −1/Km", size=26, color=GOLD, buff=0.1).move_to([4.9, -1.0, 0])
        xarr = arr(xl.get_left() + LEFT * 0.15, Q.pt(-0.25, 0) + RIGHT * 0.3, GOLD, w=3, tip=0.16)
        self.play(FadeIn(xd, scale=1.6), FadeIn(xl), Create(xarr), run_time=0.8)

        # beat 3: three inhibitor patterns
        self.at("competitive inhibitor")
        self.play(FadeOut(VGroup(Q.axes, green, yd, yl, yarr, xd, xl, xarr, tg, lbn)), run_time=0.6)
        centers = [-4.35, 0.0, 4.35]
        specs = [
            ("competitive", ["same Vmax, higher apparent Km:", "lines share a y-intercept"], 2.0, 1.0),
            ("uncompetitive", ["parallel lines"], 1.0, 2.0),
            ("noncompetitive", ["pure noncompetitive", "(binds E and ES equally)", "lower Vmax, same Km:", "share the x-intercept"], 2.0, 2.0),
        ]
        panels = []
        for cx, (name, notes, a_slope, a_int) in zip(centers, specs):
            pl = Plot(cx - 1.85, cx + 1.75, -1.2, 2.7, (-0.4, 1.0), (-0.04, 0.2), "1/[S]", "1/v", cross=(0, 0), lsize=22)
            g = pl.seg(-0.25, 0.0, 1.0, lb(1.0), GREEN, 5)
            if name == "uncompetitive":
                # parallel: y-intercept x2, same slope
                o = pl.seg(-0.25 * 2.0, 0.0, 1.0, 2 * y_int + slope * 1.0, ORANGE, 5)
            elif name == "competitive":
                o = pl.seg(-0.125, 0.0, 1.0, y_int + 2 * slope, ORANGE, 5)
            else:
                o = pl.seg(-0.25, 0.0, 1.0, 2 * (y_int + slope), ORANGE, 5)
            ttl = lab(name, 26, ORANGE).move_to([cx, -1.75, 0])
            nts = lines(*notes, size=22, color=TEXT, buff=0.08, align=ORIGIN).next_to(ttl, DOWN, buff=0.15)
            panels.append((pl, g, o, ttl, nts, name))
        # competitive
        pl, g, o, ttl, nts, name = panels[0]
        self.play(Create(pl.axes), Create(g), run_time=0.6)
        self.play(Create(o), FadeIn(ttl), FadeIn(nts), FadeIn(Dot(pl.pt(0, y_int), radius=0.13, color=GOLD)), run_time=0.8)
        self.at("uncompetitive")
        pl, g, o, ttl, nts, name = panels[1]
        self.play(Create(pl.axes), Create(g), run_time=0.6)
        self.play(Create(o), FadeIn(ttl), FadeIn(nts), run_time=0.8)
        self.at("non competitive")
        pl, g, o, ttl, nts, name = panels[2]
        self.play(Create(pl.axes), Create(g), run_time=0.6)
        self.play(Create(o), FadeIn(ttl), FadeIn(nts), FadeIn(Dot(pl.pt(-0.25, 0), radius=0.13, color=GOLD)), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """three traps: not an initial rate; more than 10 percent of substrate used; straight-line plot distorts."""

    def construct(self):
        cx = [-4.3, 0.0, 4.3]
        W = 3.9
        frames = []
        for x in cx:
            fr = RoundedRectangle(corner_radius=0.2, width=W, height=6.4, stroke_color=GREY, stroke_width=2,
                                  fill_opacity=0).move_to([x, -0.1, 0])
            frames.append(fr)

        def head(txt, x):
            return lab(txt, 26, RED, weight=BOLD).move_to([x, 2.75, 0])

        def ctrl(rows, x):
            g = lines(*rows, size=24, color=GREEN, buff=0.08, align=ORIGIN)
            return g.move_to([x, -2.35, 0])

        # panel 1: not an initial rate
        self.at("Not an initial rate")
        h1 = head("Not an initial rate", cx[0])
        p1 = Plot(cx[0] - 1.6, cx[0] + 1.5, 0.0, 1.95, (0, 60), (0, 1.6), "time", "A340", lsize=22)
        A0, TAU = 1.4, 25.0
        fcurve = lambda t: A0 - 0.016 * TAU * (1 - np.exp(-t / TAU))
        early = p1.curve(fcurve, 0, 12, GREEN, 6)
        late = p1.curve(fcurve, 12, 60, RED, 6)
        tang = p1.dseg(0, A0, 60, A0 - 0.016 * 60, GREEN, 3)
        self.play(FadeIn(frames[0]), FadeIn(h1), Create(p1.axes), run_time=0.7)
        self.play(Create(early), Create(late), Create(tang), run_time=1.2)
        t1 = lines("product can inhibit", "the enzyme or run the", "reaction backward", size=22, color=RED,
                   buff=0.06, align=ORIGIN).move_to([cx[0], -1.1, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.at("early linear stretch")
        c1 = ctrl(["early linear", "stretch only"], cx[0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)

        # panel 2: substrate used up
        self.at("Less than")
        h2 = head("Substrate used up", cx[1])
        bx, by, bw, bh = cx[1] - 0.9, 0.55, 1.1, 2.6
        outline = Rectangle(width=bw, height=bh, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([bx, by, 0])
        fillh = bh * 0.9
        fillr = Rectangle(width=bw - 0.1, height=fillh - 0.05, stroke_width=0, fill_color=TEAL, fill_opacity=0.4)
        fillr.move_to([bx, by - bh / 2 + 0.05 + (fillh - 0.05) / 2, 0])
        mark = dashed([bx - 0.8, by + bh / 2 - bh * 0.1, 0], [bx + 0.8, by + bh / 2 - bh * 0.1, 0], RED, 4)
        cons = lab("under 10%", 24, RED).move_to([cx[1] + 0.95, by + bh / 2 - bh * 0.05, 0])
        sub = lab("substrate", 22, TEAL).next_to(outline, DOWN, buff=0.15)
        used = lab("used", 22, RED).move_to([cx[1] + 0.95, by + bh / 2 - bh * 0.05 - 0.45, 0])
        self.play(FadeIn(frames[1]), FadeIn(h2), FadeIn(outline), FadeIn(fillr), FadeIn(sub), run_time=0.8)
        self.play(Create(mark), FadeIn(cons), FadeIn(used), run_time=0.8)
        self.at("read for less")
        c2 = ctrl(["read for less time", "or use less enzyme"], cx[1])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)

        # panel 3: double-reciprocal distortion
        self.at("straight line plot")
        h3 = head("Straight-line plot", cx[2])
        p3 = Plot(cx[2] - 1.6, cx[2] + 1.5, 0.0, 1.95, (0, 1.0), (0, 0.2), "1/[S]", "1/v", lsize=22)
        xs = [0.06, 0.1, 0.16, 0.45, 0.8, 1.0]
        ys = [0.0204, 0.0267, 0.0267 + 0.0045, 0.0467, 0.0767, 0.0933]
        ys = [0.017 + 0.0667 * x * (1 + 0.05 * (-1) ** i) for i, x in enumerate(xs)]
        pts = VGroup(*[p3.dot(x, y, RED, 0.1) for x, y in zip(xs, ys)])
        crowd = Ellipse(width=1.05, height=0.7, stroke_color=RED, stroke_width=3).move_to(
            (p3.pt(xs[0], ys[0]) + p3.pt(xs[2], ys[2])) / 2)
        self.play(FadeIn(frames[2]), FadeIn(h3), Create(p3.axes), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in pts], lag_ratio=0.2), run_time=1.2)
        t3 = lines("weights errors unequally,", "compresses the most", "accurate data", size=22, color=RED, buff=0.06,
                   align=ORIGIN).move_to([cx[2], -1.1, 0])
        self.play(Create(crowd), FadeIn(t3), run_time=0.7)
        self.at("Fit the curve")
        c3 = ctrl(["fit the curve; use the", "line only to see the pattern"], cx[2])
        fit(c3, max_w=3.7)
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Unlocked(SpokenScene):
    """1913 Michaelis and Menten (invertase, optical rotation); 1930s Warburg and Christian (the optical test)."""

    def construct(self):
        cards = []
        for x in (-3.15, 3.15):
            cards.append(RoundedRectangle(corner_radius=0.2, width=6.0, height=6.6, stroke_color=GREY, stroke_width=2,
                                          fill_opacity=0).move_to([x, -0.05, 0]))

        # left card
        self.at("Michaelis and")
        d1 = T("1913", 44, GOLD, font=TITLE_FONT).move_to([-3.15, 2.5, 0])
        who1 = lab("Michaelis and Menten", 26, TEXT).move_to([-3.15, 1.85, 0])
        self.play(FadeIn(cards[0]), FadeIn(d1), FadeIn(who1), run_time=0.8)
        P = Plot(-5.6, -1.0, -0.85, 0.85, (0, 10), (0, 6.4), "sucrose", "initial rate", lsize=22)
        self.play(Create(P.axes), run_time=0.5)
        self.at("initial velocities")
        Ss = [0.8, 1.6, 3.0, 5.0, 8.0]
        dts = VGroup(*[P.dot(s, mm(s, 6.0, 2.5), GREEN, 0.12) for s in Ss])
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dts], lag_ratio=0.3), run_time=1.5)
        hyp = P.curve(lambda s: mm(s, 6.0, 2.5), 0, 10, GREEN, 5)
        eq = M("v = Vmax[S] / (Km + [S])", 24, GOLD).move_to([-3.15, -1.55, 0])
        tg1 = lab("idealised sketch", 22).move_to([-3.15, -2.0, 0])
        self.play(Create(hyp), FadeIn(eq), FadeIn(tg1), run_time=1.0)
        self.at("optical rotation")
        inv = chip("invertase", BLUE, 24)
        opt = chip("optical rotation", YELLOW, 24)
        both = VGroup(inv, opt).arrange(RIGHT, buff=0.25).move_to([-3.15, -2.7, 0])
        self.play(FadeIn(both), run_time=0.7)

        # right card
        self.at("Warburg and Christian")
        d2 = T("1930s", 44, GOLD, font=TITLE_FONT).move_to([3.15, 2.5, 0])
        who2 = lab("Warburg and Christian", 26, TEXT).move_to([3.15, 1.85, 0])
        self.play(FadeIn(cards[1]), FadeIn(d2), FadeIn(who2), run_time=0.8)
        Q = Plot(0.7, 5.5, -0.85, 0.85, (300, 400), (0, 1.0), "wavelength", "absorbance", lsize=22)
        self.at("more sensitive")
        self.play(Create(Q.axes), run_time=0.5)
        red = Q.curve(lambda w: 0.08 + 0.85 * np.exp(-((w - 340) / 18.0) ** 2), 300, 400, PURPLE, 5)
        ox = Q.seg(300, 0.08, 400, 0.08, GREY, 5)
        rl = lab("reduced", 22, PURPLE).move_to(Q.pt(389, 0.62))
        ol = lab("oxidised", 22, GREY).move_to(Q.pt(389, 0.32))
        tg = lab("idealised sketch", 22).move_to([3.15, -1.6, 0])
        pk = Q.dseg(340, 0, 340, 0.93, PURPLE, 3)
        pkl = lab("340 nm", 22, PURPLE).next_to(Q.pt(340, 0), DOWN, buff=0.1)
        self.at("differ in absorption")
        self.play(Create(red), Create(ox), FadeIn(rl), FadeIn(ol), FadeIn(tg), Create(pk), FadeIn(pkl), run_time=1.2)
        self.at("optical test")
        ot = chip("the optical test", GREEN, 26)
        fr = lab("for dehydrogenases", 24, BLUE)
        grp = VGroup(ot, fr).arrange(DOWN, buff=0.15).move_to([3.15, -2.55, 0])
        self.play(FadeIn(ot), FadeIn(fr), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked(SpokenScene):
    """G6PD deficiency test (A340 rise); Chacko, Conti and Adelstein 1977; the rule: Km is not simply affinity."""

    def construct(self):
        cards = []
        for x in (-3.15, 3.15):
            cards.append(RoundedRectangle(corner_radius=0.2, width=6.0, height=6.6, stroke_color=GREY, stroke_width=2,
                                          fill_opacity=0).move_to([x, -0.05, 0]))
        # left: G6PD
        self.at("deficiency test")
        d1 = T("G6PD test", 38, GOLD, font=TITLE_FONT).move_to([-3.15, 2.5, 0])
        who1 = lab("red cells", 26, TEXT).move_to([-3.15, 1.9, 0])
        self.play(FadeIn(cards[0]), FadeIn(d1), FadeIn(who1), run_time=0.8)
        P = Plot(-5.6, -1.0, -0.75, 1.0, (0, 60), (0, 1.0), "time", "A340", lsize=22)
        self.at("rise in")
        self.play(Create(P.axes), run_time=0.4)
        rise = P.curve(lambda t: 0.1 + 0.8 * (1 - np.exp(-t / 45.0)), 0, 60, YELLOW, 6)
        self.play(Create(rise), run_time=1.2)
        conv = VGroup(chip("NADP+", GREY, 24), arr(LEFT * 0.3, RIGHT * 0.3, GREY, w=4, tip=0.15),
                      chip("NADPH", PURPLE, 24)).arrange(RIGHT, buff=0.15).move_to([-3.15, -1.7, 0])
        tg = lab("idealised", 22).move_to([-2.4, 1.35, 0])
        self.play(FadeIn(conv), FadeIn(tg), run_time=0.7)
        self.at("such as")
        dr = lines("guards against haemolysis", "from oxidative drugs,", "such as primaquine", size=24, color=RED,
                   buff=0.08, align=ORIGIN).move_to([-3.15, -2.65, 0])
        self.play(FadeIn(dr, shift=UP * 0.1), run_time=0.8)

        # right: Chacko
        self.at("In 1977")
        d2 = T("1977", 44, GOLD, font=TITLE_FONT).move_to([3.15, 2.5, 0])
        who2 = lab("Chacko, Conti and Adelstein", 24, TEXT).move_to([3.15, 1.85, 0])
        self.play(FadeIn(cards[1]), FadeIn(d2), FadeIn(who2), run_time=0.8)
        base = -0.9
        b1 = Rectangle(width=1.3, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                       fill_opacity=0.4).move_to([1.7, base + 0.35, 0])
        b2 = Rectangle(width=1.3, height=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                       fill_opacity=0.4).move_to([4.5, base + 0.75, 0])
        ax = Line([0.6, base, 0], [5.7, base, 0], color=GREY, stroke_width=3)
        l1 = lab("dephosphorylated", 22).move_to([1.7, base - 0.3, 0])
        l2 = lab("phosphorylated", 22).move_to([4.5, base - 0.3, 0])
        yl = lab("actin-activated ATPase", 24, BLUE).move_to([3.15, 1.3, 0])
        fit(yl, max_w=5.2)
        self.play(Create(ax), FadeIn(yl), FadeIn(b1), FadeIn(l1), run_time=0.7)
        self.at("had a higher")
        self.play(FadeIn(l2), GrowFromEdge(b2, DOWN), run_time=1.0)
        tg2 = lab("idealised", 22).move_to([3.15, -2.25, 0])
        self.add(tg2)
        self.at("a change in measured")
        ch = lab("a change in a measured rate", 26, GREEN).move_to([3.15, -2.9, 0])
        fit(ch, max_w=5.3)
        self.play(FadeIn(ch, shift=UP * 0.1), run_time=0.7)

        # the rule
        self.at("Remember")
        everything = VGroup(*cards, d1, who1, P.axes, rise, conv, tg, dr, d2, who2, ax, b1, b2, l1, l2, yl, tg2, ch)
        self.play(FadeOut(everything), run_time=0.7)
        rule = T("Km is not simply affinity", 58, GOLD, font=TITLE_FONT)
        fit(rule, max_w=11.8)
        rule.move_to([0, 1.2, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.at("dissociation constant")
        rb = lines("It approximates the dissociation constant", "only when catalysis is slow compared",
                   "with substrate falling off.", size=34, color=TEXT, buff=0.18, align=ORIGIN).move_to([0, -1.3, 0])
        self.play(FadeIn(rb, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Km is not simply affinity."
