"""Animal reproduction, film 1: A Loop That Keeps Time (the gonadal control loop).

COLOUR MAP: GnRH GOLD; LH BLUE; FSH GREEN; testosterone / estradiol ORED; inhibin B PURP;
progesterone TEAL. Hypothalamus, pituitary, gonad = three stacked boxes, always in the same place.
Everything schematic is labelled so; nothing is a molecule.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORED = "#FF6A3D"
PURP = "#B58CD9"
BLOOD = "#B5413A"
TAN = "#C9A27A"
PINK = "#E8A5B5"

HX, BW, BH = -0.6, 4.2, 1.5
HY, PY, GY = 2.6, 0.2, -2.4
LE, RE = HX - BW / 2, HX + BW / 2          # -2.4, 1.2
RX = -3.8                                    # return arrow x
RIB_X = 1.95
BARX = (3.2, 4.3)
BAR_Y0, BAR_H, BAR_W = -0.55, 1.5, 0.55
TUBE_TOP, TUBE_BOT = HY - BH / 2, PY + BH / 2
SX0, SX1 = 2.75, 6.6                        # strip chart x range
SY0, SY1 = 1.95, 3.1


def lerp_path(pts, u):
    seg = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
    d = u * sum(seg)
    for i, s in enumerate(seg):
        if d <= s or i == len(seg) - 1:
            return pts[i] + (pts[i + 1] - pts[i]) * (min(d, s) / max(s, 1e-9))
        d -= s


def pedal(kind="brake", color=ORED):
    if kind == "brake":
        body = RoundedRectangle(corner_radius=0.1, width=0.6, height=0.9, stroke_color=color, stroke_width=4,
                                fill_color=color, fill_opacity=0.35)
        ridges = VGroup(*[Line([-0.18, y, 0], [0.18, y, 0], color=color, stroke_width=3) for y in (-0.2, 0, 0.2)])
        g = VGroup(body, ridges)
        g.rotate(0.3)
    else:
        body = RoundedRectangle(corner_radius=0.1, width=0.42, height=1.15, stroke_color=color, stroke_width=4,
                                fill_color=color, fill_opacity=0.35)
        ridges = VGroup(*[Line([-0.1, y, 0], [0.1, y, 0], color=color, stroke_width=3) for y in (-0.3, -0.1, 0.1, 0.3)])
        g = VGroup(body, ridges)
        g.rotate(-0.25)
    back = Circle(radius=0.62, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, g)


class WS(SpokenScene):
    """SpokenScene plus the carried world: three boxes, GnRH pulses, strip chart, bars, loops."""

    def setup(self):
        super().setup()
        self.clk = ValueTracker(0)
        self.clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clk)
        self.lh = ValueTracker(0.6)
        self.fsh = ValueTracker(0.6)
        self.brake = ValueTracker(1.0)
        self.pt0 = None
        self.P = 3.0
        self.nflash = ValueTracker(1.0)

    def now(self):
        return self.clk.get_value()

    # --- pulse envelopes ---
    def env(self):
        """1 right after a burst reaches the pituitary, decaying."""
        if self.pt0 is None:
            return 0.0
        u = (self.now() - self.pt0 - 0.9) % self.P
        return math.exp(-u / 0.8)

    def nenv(self):
        if self.pt0 is None:
            return 0.0
        u = (self.now() - self.pt0) % self.P
        return math.exp(-u / 0.35)

    def drift(self, tr, target, rate):
        def u(m, dt):
            v = m.get_value()
            if abs(v - target) > 1e-3:
                m.set_value(v + math.copysign(min(rate * dt, abs(target - v)), target - v))
        tr.add_updater(u)

    # --- boxes ---
    def mkbox(self, label, y):
        r = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=TEXT, stroke_width=4,
                             fill_color=GREY, fill_opacity=0.14).move_to([HX, y, 0])
        t = T(label, 28, TEXT).move_to([HX, y + 0.4, 0])
        return VGroup(r, t)

    def boxes(self, which="hpg"):
        self.hyp = self.mkbox("hypothalamus", HY)
        self.pit = self.mkbox("pituitary", PY)
        self.gon = self.mkbox("gonad", GY)
        self.pit_rect = self.pit[0]
        g = VGroup()
        if "h" in which: g.add(self.hyp)
        if "p" in which: g.add(self.pit)
        if "g" in which: g.add(self.gon)
        self.add(g)
        return g

    def glow_pit(self):
        r = self.pit[0]
        r.add_updater(lambda m: m.set_fill(GOLD, opacity=0.14 + 0.5 * self.env()))
        h = self.hyp[0]
        h.add_updater(lambda m: m.set_fill(GOLD, opacity=0.14 + 0.4 * self.nenv()))

    def gon_icons(self, mode="both"):
        y = GY - 0.36
        g = VGroup()
        if mode in ("both", "testis"):
            x = HX - (0.7 if mode == "both" else 0)
            g.add(Ellipse(width=0.8, height=0.5, stroke_color=TAN, stroke_width=3, fill_color=TAN, fill_opacity=0.5).move_to([x, y, 0]))
        if mode in ("both", "ovary"):
            x = HX + (0.7 if mode == "both" else 0)
            g.add(Ellipse(width=0.8, height=0.5, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.4).move_to([x, y, 0]))
        return g

    # --- GnRH tube + pulses ---
    def tube(self):
        g = VGroup(Line([HX - 0.17, TUBE_TOP, 0], [HX - 0.17, TUBE_BOT, 0], color=GREY, stroke_width=4),
                   Line([HX + 0.17, TUBE_TOP, 0], [HX + 0.17, TUBE_BOT, 0], color=GREY, stroke_width=4))
        self.add(g)
        return g

    def start_pulses(self, t0=None):
        self.pt0 = self.now() if t0 is None else t0
        dots = VGroup(*[Dot(radius=0.15, color=GOLD) for _ in range(3)])

        def upd(m):
            s0 = (self.now() - self.pt0) % self.P
            for i, d in enumerate(m):
                s = s0 - i * 0.3
                if 0 <= s < 1.0:
                    d.set_opacity(1)
                    d.move_to([HX, TUBE_TOP - (TUBE_TOP - TUBE_BOT) * s, 0])
                else:
                    d.set_opacity(0)
        dots.add_updater(upd)
        self.add(dots)
        self.pdots = dots
        return dots

    def neurons(self):
        g = VGroup()
        self.nsoma = []
        for k in range(4):
            x = HX - 1.2 + k * 0.8
            y = HY - 0.38
            soma = Dot(radius=0.13, color=YELLOW).move_to([x, y, 0])
            arms = VGroup(*[Line([x, y, 0], [x + dx, y + dy, 0], color=GREY, stroke_width=3)
                            for dx, dy in [(-0.25, 0.2), (0.25, 0.2), (0, -0.3)]])
            soma.add_updater(lambda m: m.set_fill(GOLD, opacity=0.35 + 0.65 * self.nenv()).set_stroke(GOLD, width=2))
            g.add(arms, soma)
        self.add(g)
        return g

    def strip(self, label=True):
        box = Rectangle(width=SX1 - SX0, height=SY1 - SY0, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1)
        box.move_to([(SX0 + SX1) / 2, (SY0 + SY1) / 2, 0])
        trace = VMobject(stroke_color=GOLD, stroke_width=4)

        def upd(m):
            if self.pt0 is None:
                return
            W, n = 9.0, 160
            pts = []
            for k in range(n + 1):
                w = k / n
                u = self.now() - W * (1 - w) - self.pt0
                if u < 0:
                    v = 0.0
                else:
                    d = u % self.P
                    v = d / 0.1 if d < 0.1 else math.exp(-(d - 0.1) / 0.25)
                pts.append([SX0 + 0.1 + (SX1 - SX0 - 0.2) * w, SY0 + 0.12 + v * (SY1 - SY0 - 0.3), 0])
            m.set_points_as_corners(pts)
        trace.add_updater(upd)
        g = VGroup(box, trace)
        if label:
            g.add(T("pulses (schematic)", 28, GOLD).move_to([(SX0 + SX1) / 2, 3.58, 0]))
        self.add(g)
        return g

    # --- bars and blood ---
    def bars(self):
        g = VGroup()
        for x, tr, col, name in [(BARX[0], self.lh, BLUE, "LH"), (BARX[1], self.fsh, GREEN, "FSH")]:
            frame = Rectangle(width=BAR_W, height=BAR_H, stroke_color=col, stroke_width=3).move_to([x, BAR_Y0 + BAR_H / 2, 0])
            fill = Rectangle(width=BAR_W - 0.08, height=0.05, stroke_width=0, fill_color=col, fill_opacity=0.85)

            def upd(m, tr=tr, x=x):
                h = max(0.03, BAR_H * min(0.98, tr.get_value() * (1 + 0.1 * self.env())))
                m.stretch_to_fit_height(h)
                m.move_to([x, BAR_Y0 + h / 2, 0])
            fill.add_updater(upd)
            lab = T(name, 28, col, weight=BOLD).move_to([x, BAR_Y0 - 0.38, 0])
            g.add(frame, fill, lab)
        self.add(g)
        return g

    def ribbon(self):
        pts = [[RE, PY, 0], [RIB_X, PY, 0], [RIB_X, GY, 0], [RE, GY, 0]]
        r = VMobject(stroke_color=BLOOD, stroke_width=10, stroke_opacity=0.6)
        r.set_points_as_corners(pts)
        self.add(r)
        return r

    def flow(self, pts, n, period, colors, r=0.09, fade=False, gate=None):
        pts = [np.array(p, float) for p in pts]
        dots = VGroup(*[Dot(radius=r, color=colors[i % len(colors)]) for i in range(n)])
        dots.g = ValueTracker(1.0)
        t0 = self.now()

        def upd(m):
            for i, d in enumerate(m):
                u = ((self.now() - t0) / period + i / n) % 1
                d.move_to(lerp_path(pts, u))
                op = (1 - u) if fade else (min(1, u * 8, (1 - u) * 8))
                d.set_opacity(op * m.g.get_value() * (gate() if gate else 1))
        dots.add_updater(upd)
        self.add(dots)
        return dots

    def blood_dots(self):
        pts = [[RE, PY, 0], [RIB_X, PY, 0], [RIB_X, GY, 0], [RE, GY, 0]]
        return self.flow(pts, 8, 4.0, [BLUE, GREEN], r=0.1)

    # --- return loops ---
    def ret(self, color=ORED, x=RX, tr=None, tracker=None):
        tr = tracker or self.brake
        vert = Line([x, GY, 0], [x, HY, 0])
        s0 = Line([LE, GY, 0], [x, GY, 0])
        a1 = Arrow([x, HY, 0], [LE - 0.04, HY, 0], buff=0, tip_length=0.28)
        a2 = Arrow([x, PY, 0], [LE - 0.04, PY, 0], buff=0, tip_length=0.28)
        g = VGroup(s0, vert, a1, a2)
        g.set_color(color)

        def upd(m):
            w = 3 + 8 * tr.get_value()
            for p in m:
                p.set_stroke(width=w)
        g.add_updater(upd)
        g.tr = tr
        return g

    def ret_dots(self, color=ORED, x=RX, tr=None):
        tr = tr or self.brake
        pts = [[LE, GY, 0], [x, GY, 0], [x, HY, 0], [LE, HY, 0]]
        return self.flow(pts, 8, 5.0, [color], r=0.1, gate=lambda: min(1.0, tr.get_value() * 1.6))

    def fb_label(self, text="negative\nfeedback", color=ORED):
        return T(text, 28, color, weight=BOLD, line_spacing=0.8).move_to([-5.35, 0.4, 0])

    def schem(self):
        return T("schematic", 28, GREY).move_to([5.7, -3.45, 0])

    def dashed_gon(self, label="testes removed"):
        new = VGroup(DashedVMobject(RoundedRectangle(corner_radius=0.2, width=BW, height=BH).move_to([HX, GY, 0]).set_stroke(TEXT, 4), num_dashes=40),
                     T(label, 28, GREY).move_to([HX, GY + 0.1, 0]))
        return new


# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    TITLE = "A Loop That Keeps Time"
    LESSON = "Animal Reproduction"


# ---------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        clk = ValueTracker(0)
        clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clk)
        # testis (left)
        testis = Ellipse(width=2.6, height=3.0, stroke_color=TAN, stroke_width=5, fill_color=TAN, fill_opacity=0.35).move_to([-3.4, 1.0, 0])
        coil = VGroup(*[Arc(radius=0.4, start_angle=0.2 + 0.3 * k, angle=2.6, stroke_color=TAN, stroke_width=3).shift([-3.4 + (-0.35 if k % 2 else 0.35), 1.0 + (k - 1) * 0.75, 0]) for k in range(3)])
        self.play(FadeIn(testis, shift=UP * 0.2), Create(coil), run_time=0.9)

        spath = [[-3.4, -0.3, 0], [-3.4, -2.05, 0]]
        sp = VGroup()
        for i in range(8):
            sp.add(VGroup(Dot(radius=0.09, color=TEXT), Line([0, -0.09, 0], [0, -0.3, 0], color=TEXT, stroke_width=3)))
        t0 = clk.get_value()
        gate = ValueTracker(0)

        def upd(m):
            for i, s in enumerate(m):
                u = ((clk.get_value() - t0) / 2.4 + i / 8) % 1
                p = lerp_path([np.array(q, float) for q in spath], u)
                s.move_to(p + np.array([0.18 * math.sin(7 * u + i), 0, 0]))
                s.set_opacity(min(1, u * 6, (1 - u) * 6) * gate.get_value())
        sp.add_updater(upd)
        self.add(sp)
        self.at("keep making")
        self.play(gate.animate.set_value(1), run_time=0.8)
        self.at("through adult life")
        lab1 = T("through adult life", 28, TEXT).move_to([-3.4, -2.75, 0])
        self.play(FadeIn(lab1, shift=UP * 0.1), run_time=0.6)

        # ovary + calendar (right)
        self.at("woman's")
        ovary = Ellipse(width=2.5, height=1.9, stroke_color=PINK, stroke_width=5, fill_color=PINK, fill_opacity=0.3).move_to([2.2, 1.0, 0])
        fols = VGroup(*[Circle(radius=r, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.25).move_to([2.2 + dx, 1.0 + dy, 0])
                        for r, dx, dy in [(0.3, -0.5, 0.1), (0.22, 0.45, -0.3), (0.18, 0.3, 0.4)]])
        cal_body = RoundedRectangle(corner_radius=0.12, width=2.3, height=2.5, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([5.3, 1.0, 0])
        cal_head = Rectangle(width=2.3, height=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.6).move_to([5.3, 1.95, 0])
        grid = VGroup(*[Line([4.3, y, 0], [6.3, y, 0], color=GREY, stroke_width=2) for y in (1.3, 0.8, 0.3)],
                      *[Line([x, 0.0, 0], [x, 1.65, 0], color=GREY, stroke_width=2) for x in (4.8, 5.3, 5.8)])
        page = VGroup(Rectangle(width=2.2, height=1.9, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([5.3, 0.78, 0]), grid.copy())
        cal = VGroup(cal_body, cal_head, grid)
        self.play(FadeIn(ovary, shift=UP * 0.2), FadeIn(fols), FadeIn(cal), run_time=0.9)
        self.add(page)
        self.at("usually release")
        egg = Circle(radius=0.22, stroke_color=PINK, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).move_to([2.2 + 0.3, 1.4, 0])
        self.add(egg)
        self.play(egg.animate.move_to([3.2, 2.75, 0]), page.animate.stretch(0.03, 1, about_edge=UP), run_time=1.4)
        self.remove(page)
        self.at("one egg per cycle")
        lab2 = T("usually one egg\nper cycle", 28, TEXT, line_spacing=0.8).move_to([4.1, -2.0, 0])
        self.play(FadeIn(lab2, shift=UP * 0.1), run_time=0.6)
        self.play(egg.animate.shift(RIGHT * 0.25), Wiggle(egg, scale_value=1.15, rotation_angle=0.05 * TAU), run_time=1.4)
        self.at("What keeps")
        q = T("?", 150, GOLD, weight=BOLD).move_to([-0.2, 0.9, 0])
        self.play(GrowFromCenter(q), run_time=1.0)
        self.play(Wiggle(q, scale_value=1.1, rotation_angle=0.04 * TAU), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------
class S02Boxes(WS):
    def construct(self):
        self.pt0 = None
        # three ghost levels
        self.at("three levels")
        ghosts = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.2, width=BW, height=BH).move_to([HX, y, 0]).set_stroke(GREY, 3), num_dashes=36)
                          for y in (HY, PY, GY)])
        self.play(Create(ghosts), run_time=1.2)
        self.at("stacked top to bottom")
        arrow = Arrow([-3.4, 3.2, 0], [-3.4, -3.2, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.3)
        self.play(GrowArrow(arrow), run_time=1.4)
        # brain
        self.at("hypothalamus")
        brain = VGroup(
            Ellipse(width=4.6, height=3.0, stroke_color=PINK, stroke_width=5, fill_color=PINK, fill_opacity=0.14),
            Arc(radius=0.7, start_angle=0.3, angle=2.4, stroke_color=PINK, stroke_width=3).shift([-1.0, 0.5, 0]),
            Arc(radius=0.7, start_angle=0.6, angle=2.4, stroke_color=PINK, stroke_width=3).shift([0.3, 0.55, 0]),
            Arc(radius=0.6, start_angle=3.6, angle=2.2, stroke_color=PINK, stroke_width=3).shift([-0.3, -0.1, 0]),
            Arc(radius=0.6, start_angle=3.9, angle=2.2, stroke_color=PINK, stroke_width=3).shift([1.1, 0.1, 0]),
        ).move_to([4.5, 1.6, 0])
        brain_lab = T("brain", 28, PINK).move_to([4.5, 3.3, 0])
        self.play(brain.animate.shift(LEFT * 0.0).set_opacity(1), FadeIn(brain, shift=LEFT * 1.0), FadeIn(brain_lab), run_time=1.0)
        spot = Ellipse(width=1.0, height=0.5, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.5).move_to([4.5, 0.55, 0])
        self.play(FadeIn(spot), run_time=0.5)
        self.play(Indicate(spot, color=YELLOW, scale_factor=1.25), run_time=0.8)
        hyp = self.mkbox("hypothalamus", HY)
        self.play(ReplacementTransform(spot, hyp[0]), FadeIn(hyp[1], shift=UP * 0.1), FadeOut(brain), FadeOut(brain_lab), run_time=1.6)
        self.at("pituitary gland")
        pit = self.mkbox("pituitary", PY)
        stalk = Line([HX, TUBE_TOP, 0], [HX, TUBE_BOT, 0], color=GREY, stroke_width=8)
        self.play(FadeIn(stalk), FadeIn(pit, shift=DOWN * 0.8), run_time=1.3)
        self.at("gonads, the testes")
        gon = self.mkbox("gonad", GY)
        self.play(Create(gon[0]), FadeIn(gon[1]), run_time=1.0)
        icons = self.gon_icons("both")
        lab = T("gonads:\ntestes or ovaries", 28, TEXT, line_spacing=0.8).move_to([4.3, GY, 0])
        lab_t = T("testes", 28, TAN).move_to([4.3, GY + 0.1, 0])
        self.play(FadeIn(icons), FadeIn(lab), run_time=0.9)
        self.play(Indicate(icons[0], color=TAN), run_time=0.7)
        self.play(Indicate(icons[1], color=PINK), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------
class S03Gnrh(WS):
    def construct(self):
        self.boxes()
        self.add(self.gon_icons("both"))
        self.glow_pit()
        self.nn = self.neurons()
        # start pulse clock for neuron flashing at the first words
        self.pt0 = self.now()
        self.wait(0.01)
        self.at("release a hormone")
        tube = self.tube()
        self.at("hormone called")
        self.pt0 = self.now() - 0.1
        self.start_pulses(self.pt0)
        self.at("GnRH")
        gl = T("GnRH", 28, GOLD, weight=BOLD).move_to([-2.2, 1.4, 0])
        self.play(FadeIn(gl, shift=RIGHT * 0.1), run_time=0.6)
        self.at("Portal vessels")
        pl = T("portal vessels", 28, TEXT).move_to([1.2, 1.4, 0])
        self.play(FadeIn(pl, shift=LEFT * 0.1), tube.animate.set_color(TEXT), run_time=0.8)
        self.at("in pulses")
        st = self.strip()
        self.add(st); self.wait(0.8)
        self.finish()


# ---------------------------------------------------------------------------
class S04Lhfsh(WS):
    def construct(self):
        self.boxes()
        self.add(self.gon_icons("both"))
        self.tube()
        self.pt0 = None
        self.start_pulses(self.now())
        self.glow_pit()
        self.strip(label=False)
        self.at("pituitary answers")
        self.wait(1.0)
        self.at("LH")
        self.lh.set_value(0.6); self.fsh.set_value(0.6)
        rib = self.ribbon()
        self.play(Create(rib), run_time=0.9)
        bars = self.bars()
        self.wait(0.9)
        dots = self.blood_dots()
        self.at("travel in the blood")
        bl = T("blood", 28, "#FF8A80").move_to([RIB_X + 0.9, -1.4, 0])
        self.play(FadeIn(bl), run_time=0.6)
        self.at("act on gonads")
        self.play(Indicate(self.gon[0], color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("gonadotropins")
        br = Brace(VGroup(bars[2], bars[5]), DOWN, buff=0.1, color=TEXT)
        gt = T("gonadotropins", 28, TEXT, weight=BOLD).next_to(br, DOWN, buff=0.12)
        self.play(FadeOut(bl), GrowFromCenter(br), FadeIn(gt), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------
class S05Testis(WS):
    def construct(self):
        self.boxes()
        ic5 = self.gon_icons("testis")
        self.add(ic5)
        tb = self.tube()
        pd = self.start_pulses(self.now())
        self.glow_pit()
        rb = self.ribbon()
        br = self.bars()
        bd = self.blood_dots()
        self.wait(0.4)
        # zoom: gonad box becomes the testis panel
        panel = RoundedRectangle(corner_radius=0.3, width=13.0, height=7.2, stroke_color=TAN, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([0, 0, 0])
        panel.set_z_index(30)
        gl = T("testis", 28, TAN, weight=BOLD).move_to([-5.7, -3.2, 0])
        self.play(ReplacementTransform(self.gon[0], panel), FadeOut(self.hyp), FadeOut(self.pit), run_time=1.5)
        for m in (tb, pd, rb, br, bd, ic5, self.gon[1]):
            self.remove(m)
        panel.set_z_index(0)
        # cross-section
        tub = VGroup()
        centers = [(-2.2, 0.3), (2.9, 1.0), (1.4, -1.8)]
        for cx, cy in centers:
            tub.add(Circle(radius=1.25, stroke_color=TAN, stroke_width=8, fill_color=TAN, fill_opacity=0.12).move_to([cx, cy, 0]))
        self.play(FadeIn(tub), FadeIn(gl), run_time=1.0)
        self.at("LH reaches")
        L = [(0.3, 0.9), (-0.9, -2.1), (5.2, -1.3)]
        leyd = VGroup()
        for cx, cy in L:
            cl = VGroup(*[Dot(radius=0.2, color=TAN) for _ in range(3)])
            cl[0].move_to([cx - 0.2, cy - 0.1, 0]); cl[1].move_to([cx + 0.2, cy - 0.1, 0]); cl[2].move_to([cx, cy + 0.2, 0])
            leyd.add(cl)
        for cx, cy in L:
            self.flow([[cx, cy + 1.3, 0], [cx, cy + 0.35, 0]], 3, 1.8, [BLUE], r=0.13)
        self.play(FadeIn(leyd), run_time=0.7)
        self.at("latic cells")
        leyl = T("Leydig cells", 28, TAN, weight=BOLD).move_to([0.3, 3.1, 0])
        leader = Line([0.3, 2.85, 0], [0.3, 1.2, 0], color=TAN, stroke_width=3)
        lhl = T("LH", 28, BLUE, weight=BOLD).move_to([-0.55, 2.0, 0])
        self.play(FadeIn(leyl), Create(leader), FadeIn(lhl), run_time=0.8)
        self.at("which sit between")
        self.play(Indicate(leyd, color=TAN, scale_factor=1.2), run_time=1.2)
        self.at("sperm making tubules")
        self.play(tub.animate.set_fill(TAN, opacity=0.3), run_time=1.0)
        self.at("make testosterone")
        self.play(leyd.animate.set_color(ORED), run_time=0.8)
        for cx, cy in L:
            self.flow([[cx, cy, 0], [cx + (0.9 if cx >= 0 else -0.9), cy + 0.6, 0]], 4, 2.0, [ORED], r=0.1, fade=True)
        tl = T("testosterone", 28, ORED, weight=BOLD).move_to([-1.9, -3.1, 0])
        tl_line = Line([-1.5, -2.85, 0], [-1.0, -2.45, 0], color=ORED, stroke_width=3)
        self.play(FadeIn(tl), Create(tl_line), run_time=0.8)
        self.at("FSH reaches")
        self.play(FadeOut(lhl), FadeOut(leyl), FadeOut(leader), run_time=0.5)
        cx, cy = centers[0]
        sert = VGroup()
        for k in range(10):
            a_ = k * TAU / 10
            p = np.array([cx + 1.08 * math.cos(a_), cy + 1.08 * math.sin(a_), 0])
            c = RoundedRectangle(corner_radius=0.05, width=0.2, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5)
            c.rotate(a_ - PI / 2).move_to(p)
            sert.add(c)
        self.play(FadeIn(sert), run_time=0.8)
        fl = T("FSH", 28, GREEN, weight=BOLD).move_to([-4.9, 2.7, 0])
        self.flow([[-4.2, 2.6, 0], [cx - 1.2, cy + 1.0, 0]], 3, 1.8, [GREEN], r=0.13)
        self.play(FadeIn(fl), run_time=0.5)
        self.at("sertile cells")
        sl = T("Sertoli\ncells", 28, GREEN, weight=BOLD, line_spacing=0.8).move_to([-5.3, 0.4, 0])
        self.play(FadeIn(sl), run_time=0.7)
        self.at("line the tubules")
        self.play(Indicate(sert, color=GREEN, scale_factor=1.1), run_time=1.0)
        self.at("support the")
        germ = VGroup(*[Dot(radius=0.1, color=TEXT).move_to([cx + 0.78 * math.cos(k * TAU / 8 + 0.2), cy + 0.78 * math.sin(k * TAU / 8 + 0.2), 0]) for k in range(8)])
        self.add(germ)
        self.play(*[g.animate.move_to([cx + 0.5 * math.cos(k * TAU / 8 + 0.2), cy + 0.5 * math.sin(k * TAU / 8 + 0.2), 0]) for k, g in enumerate(germ)], run_time=0.8)
        self.at("developing sperm")
        dl = T("developing\nsperm", 28, TEXT, weight=BOLD, line_spacing=0.8).move_to([-5.2, -1.6, 0])
        dl_line = Line([-3.95, -1.45, 0], [cx - 0.3, cy - 0.5, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(dl), Create(dl_line), run_time=0.6)
        self.play(*[g.animate.move_to([cx + 0.2 * math.cos(k * TAU / 8 + 0.2), cy + 0.2 * math.sin(k * TAU / 8 + 0.2), 0]) for k, g in enumerate(germ)], run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------
class S06Brake(WS):
    def construct(self):
        self.lh.set_value(0.6); self.fsh.set_value(0.6)
        self.brake.set_value(0.0)
        # start from the previous picture: testis panel, then zoom back out
        self.boxes()
        self.tube()
        self.add(self.gon_icons("testis"))
        self.start_pulses(self.now())
        self.glow_pit()
        self.ribbon()
        self.bars()
        panel = RoundedRectangle(corner_radius=0.3, width=13.0, height=7.2, stroke_color=TAN, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([0, 0, 0])
        tub = VGroup(*[Circle(radius=1.4, stroke_color=TAN, stroke_width=8, fill_color=TAN, fill_opacity=0.25).move_to([cx, cy, 0]) for cx, cy in [(-3.5, 0.9), (3.5, 0.9), (0.0, -1.0)]])
        panel.set_z_index(20); tub.set_z_index(21)
        self.add(panel, tub)
        self.wait(0.3)
        tgt = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([HX, GY, 0])
        tgt.set_z_index(20)
        self.play(FadeOut(tub), Transform(panel, tgt), run_time=1.5)
        self.remove(panel)
        self.blood_dots()
        self.at("Testosterone")
        r = self.ret()
        self.add(r)
        rd = self.ret_dots()
        self.play(Create(r), self.brake.animate.set_value(0.5), run_time=1.6)
        self.at("lowers the output")
        self.drift(self.lh, 0.3, 0.06); self.drift(self.fsh, 0.3, 0.06)
        self.at("hypothalamus", )
        self.play(Indicate(self.hyp[0], color=ORED, scale_factor=1.04), run_time=0.7)
        self.at("and the pituitary")
        self.play(Indicate(self.pit[0], color=ORED, scale_factor=1.04), run_time=0.8)
        self.at("negative feedback")
        pd = pedal("brake").move_to([RX, 0.4, 0])
        fl = self.fb_label()
        self.play(FadeIn(pd, scale=0.6), FadeIn(fl), run_time=1.0)
        self.at("Think of it")
        self.play(pd.animate.rotate(-0.25).shift(DOWN * 0.12), run_time=0.9)
        self.play(self.brake.animate.set_value(1.0), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------
class S07Balance(WS):
    def construct(self):
        self.lh.set_value(0.3); self.fsh.set_value(0.3)
        self.brake.set_value(1.0)
        self.boxes()
        self.add(self.gon_icons("testis"))
        self.tube()
        self.start_pulses(self.now())
        self.glow_pit()
        self.ribbon(); self.blood_dots(); self.bars()
        r = self.ret(); self.add(r); self.ret_dots()
        pd = pedal("brake").move_to([RX, 0.4, 0]).rotate(-0.25)
        fl = self.fb_label()
        self.add(pd, fl)
        sc = self.schem(); self.add(sc)
        self.at("LH")
        self.play(self.lh.animate.set_value(0.22), self.fsh.animate.set_value(0.22), run_time=1.8)
        self.at("testosterone drops")
        tl = T("testosterone\nfalls", 28, ORED, line_spacing=0.8).move_to([-5.35, -1.4, 0])
        self.play(FadeIn(tl), run_time=0.5)
        self.play(self.brake.animate.set_value(0.2), pd.animate.rotate(0.25).shift(UP * 0.12), run_time=2.2)
        self.at("LH and FSH climb")
        self.play(self.lh.animate.set_value(0.6), self.fsh.animate.set_value(0.6), run_time=2.4)
        self.finish()


# ---------------------------------------------------------------------------
def world_loop(self, gon_mode="testis", ret_on=True, lh=0.6, fsh=0.6, brake_v=0.5):
    self.lh.set_value(lh); self.fsh.set_value(fsh); self.brake.set_value(brake_v)
    self.boxes()
    self.tube()
    self.start_pulses(self.now())
    self.glow_pit()
    self.ribbon(); self.blood_dots(); bars = self.bars()
    if ret_on:
        r = self.ret(); self.add(r); rd = self.ret_dots()
        pd = pedal("brake").move_to([RX, 0.4, 0]).rotate(-0.1)
        self.add(pd)
        self.add(self.fb_label())
    return bars


class S08Predict(WS):
    def construct(self):
        world_loop(self, brake_v=0.5)
        icons = self.gon_icons("testis")
        self.add(icons)
        self.wait(0.5)
        self.at("Remove the testes")
        dg = self.dashed_gon()
        self.play(FadeOut(self.gon), FadeOut(icons), FadeIn(dg), run_time=1.2)
        self.at("What happens")
        card = VGroup(RoundedRectangle(corner_radius=0.2, width=4.0, height=1.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.12),
                      T("LH and FSH:\nup or down?", 32, TEXT, weight=BOLD, line_spacing=0.8)).move_to([4.6, -2.3, 0])
        card[1].move_to(card[0])
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.at("Do they go up")
        up = Arrow([4.0, -0.2, 0], [4.0, 0.9, 0], buff=0, color=GREY, stroke_width=0)
        self.play(Indicate(card[1], color=GOLD, scale_factor=1.06), run_time=1.0)
        self.finish()


class S09Pause(WS):
    def construct(self):
        world_loop(self, brake_v=0.5)
        dg = self.dashed_gon()
        self.remove(self.gon)
        self.add(dg)
        card = VGroup(RoundedRectangle(corner_radius=0.2, width=4.0, height=1.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.12),
                      T("LH and FSH:\nup or down?", 32, TEXT, weight=BOLD, line_spacing=0.8)).move_to([4.6, -2.3, 0])
        card[1].move_to(card[0])
        self.add(card)
        ring_bg = Circle(radius=0.45, stroke_color=GREY, stroke_width=5).move_to([6.0, -0.85, 0])
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()) + 1e-3, stroke_color=GOLD, stroke_width=7).move_to([6.0, -0.85, 0]))
        self.add(ring_bg, ring)
        self.play(tr.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


class S10Reveal(WS):
    def construct(self):
        world_loop(self, brake_v=0.5)
        dg = self.dashed_gon()
        self.remove(self.gon)
        self.add(dg)
        self.at("Both go up")
        self.play(self.lh.animate.set_value(0.8), self.fsh.animate.set_value(0.8), run_time=2.5)
        self.at("testes gone")
        self.wait(0.2)
        self.at("testosterone is gone")
        self.play(self.brake.animate.set_value(0.0), run_time=2.2)
        self.at("main break is off")
        self.wait(0.3)
        self.at("pituitary keeps driving")
        self.play(Indicate(self.pit[0], color=GOLD, scale_factor=1.05), run_time=1.2)
        self.at("climb")
        lab = T("LH and FSH rise\n(schematic)", 28, TEXT, line_spacing=0.8).move_to([4.7, -2.3, 0])
        self.play(self.lh.animate.set_value(0.97), self.fsh.animate.set_value(0.97), FadeIn(lab), run_time=1.5)
        self.finish()


class S11Inhibin(WS):
    def construct(self):
        # carried: removed state
        world_loop(self, brake_v=0.0, lh=0.97, fsh=0.97)
        dg = self.dashed_gon()
        self.remove(self.gon)
        self.add(dg)
        # rewind to the intact loop
        self.at("FSH has a second")
        icons = self.gon_icons("testis")
        gon = self.mkbox("gonad", GY)
        sert = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.16, height=0.42, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5).move_to([HX + 0.5 + 0.28 * k, GY - 0.38, 0]) for k in range(3)])
        icons[0].move_to([HX - 0.7, GY - 0.38, 0])
        self.play(FadeOut(dg), FadeIn(gon), FadeIn(icons), FadeIn(sert), self.brake.animate.set_value(0.5),
                  self.lh.animate.set_value(0.35), self.fsh.animate.set_value(0.35), run_time=1.8)
        self.gon = gon
        # purple loop to the FSH bar
        self.at("Sertoli cells release")
        pts = [[RE, GY - 0.4, 0], [5.5, GY - 0.4, 0], [5.5, 0.4, 0], [BARX[1] + 0.3, 0.4, 0]]
        path = VMobject(stroke_color=PURP, stroke_width=7)
        path.set_points_as_corners(pts)
        tip = Arrow([5.4, 0.4, 0], [BARX[1] + 0.3, 0.4, 0], buff=0, color=PURP, stroke_width=7, tip_length=0.28)
        self.play(Create(path), run_time=1.6)
        self.add(tip)
        pd = self.flow(pts, 8, 4.0, [PURP], r=0.1)
        self.at("inhibin B")
        il = T("inhibin B", 28, PURP, weight=BOLD).move_to([3.7, GY + 0.75, 0])
        self.play(FadeIn(il), run_time=0.6)
        self.at("lowers FSH")
        self.play(self.fsh.animate.set_value(0.2), run_time=1.6)
        self.at("Remove the testes")
        dg2 = self.dashed_gon()
        self.play(FadeOut(gon), FadeOut(icons), FadeOut(sert), FadeIn(dg2), run_time=1.0)
        self.at("that break goes too")
        self.play(FadeOut(path), FadeOut(tip), FadeOut(il), pd.g.animate.set_value(0), self.brake.animate.set_value(0.0),
                  self.lh.animate.set_value(0.95), self.fsh.animate.set_value(0.95), run_time=2.5)
        self.finish()


# ---------------------------------------------------------------------------
def E2(x):
    """Schematic estradiol rise over the follicular half (0..1 -> 0..1)."""
    return 1 / (1 + math.exp(-9 * (x - 0.45)))


class S12Ovary(WS):
    def construct(self):
        self.boxes()
        self.tube()
        self.start_pulses(self.now())
        self.glow_pit()
        self.brake.set_value(0.0)
        icons = self.gon_icons("both")
        self.add(icons)
        self.at("same loop")
        ov = Ellipse(width=1.9, height=0.62, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).move_to([HX, GY - 0.38, 0])
        self.play(FadeOut(icons), FadeIn(ov), run_time=1.2)
        self.at("the follicle")
        fol = Circle(radius=0.12, stroke_color=PINK, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).move_to([HX - 0.1, GY - 0.38, 0])
        self.play(GrowFromCenter(fol), run_time=0.8)
        self.at("the sac of cells")
        fl = T("follicle: egg plus\nsupporting cells", 28, PINK, line_spacing=0.8).move_to([4.5, GY, 0])
        ll = Line([2.55, GY - 0.1, 0], [HX + 0.4, GY - 0.38, 0], color=PINK, stroke_width=3)
        self.play(FadeIn(fl), Create(ll), fol.animate.scale(2.2), run_time=1.6)
        self.at("Its hormone")
        ed = self.flow([[HX - 0.1, GY - 0.38, 0], [LE - 0.5, GY - 0.38, 0]], 5, 2.2, [ORED], r=0.09, fade=True)
        self.at("estradiol")
        el = T("estradiol", 28, ORED, weight=BOLD).move_to([-5.35, -1.3, 0])
        self.play(FadeIn(el), run_time=0.6)
        self.at("most of the cycle's")
        r = self.ret(); self.add(r); self.ret_dots()
        pd = pedal("brake").move_to([RX, 0.4, 0]).rotate(-0.1)
        self.play(Create(r), self.brake.animate.set_value(0.6), FadeIn(pd), run_time=1.6)
        # calendar strip on the right; marker position follows scene time
        self.at("first half")
        X0, X1, Y0 = 2.7, 6.6, 1.2
        XM = (X0 + X1) / 2
        T0, TO, T1 = self.elapsed(), self.t_of("After ovulation"), self.narration_s

        def prog():
            t = self.elapsed()
            if t < TO:
                return 0.5 * max(0.0, (t - T0) / (TO - T0))
            return 0.5 + 0.48 * min(1.0, (t - TO) / (T1 - TO))

        base = Line([X0, Y0, 0], [X1, Y0, 0], color=GREY, stroke_width=5)
        mk = Dot(radius=0.14, color=TEXT).move_to([X0, Y0, 0])
        flab = T("follicular phase", 28, TEXT).move_to([X0 + 1.7, Y0 - 0.55, 0])
        sch = self.schem()
        mk.add_updater(lambda m: m.move_to([X0 + (X1 - X0) * prog(), Y0, 0]))
        area = VMobject(stroke_color=ORED, stroke_width=4, fill_color=ORED, fill_opacity=0.35)

        def upd_area(m):
            f = min(1.0, prog() * 2)
            pts = [[X0, Y0, 0]]
            for k in range(41):
                s = f * k / 40
                pts.append([X0 + (XM - X0) * s, Y0 + 1.2 * E2(s), 0])
            pts.append([X0 + (XM - X0) * f, Y0, 0])
            m.set_points_as_corners(pts)
        area.add_updater(upd_area)
        self.add(area)
        self.play(Create(base), FadeIn(flab), FadeIn(sch), FadeIn(mk), run_time=1.0)
        self.at("stays high")
        self.play(Indicate(area, color=ORED, scale_factor=1.04), run_time=1.2)
        self.at("becomes an accelerator")
        acc = pedal("accel", YELLOW).move_to([RX, 0.4, 0])
        al = T("high for long enough:\naccelerator", 28, YELLOW, weight=BOLD, line_spacing=0.8).move_to([4.7, -0.55, 0])
        self.play(FadeOut(pd), FadeIn(acc, scale=0.6), FadeIn(al), run_time=1.0)
        self.at("After ovulation")
        tick = Line([XM, Y0 - 0.2, 0], [XM, Y0 + 1.5, 0], color=TEXT, stroke_width=4)
        ol = T("ovulation", 28, TEXT, weight=BOLD).move_to([XM, Y0 + 1.85, 0])
        self.play(Create(tick), FadeIn(ol), run_time=0.7)
        self.at("progesterone")
        pa = VMobject(stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.4)

        def upd_pa(m):
            f = max(0.0, min(1.0, (prog() - 0.5) / 0.5))
            xe = XM + (X1 - XM) * f
            m.set_points_as_corners([[XM, Y0, 0], [XM, Y0 + 0.7, 0], [xe, Y0 + 0.7, 0], [xe, Y0, 0]])
        pa.add_updater(upd_pa)
        self.add(pa)
        pl = T("progesterone", 28, TEAL, weight=BOLD).move_to([-5.35, -1.3, 0])
        pd2 = pedal("brake", TEAL).move_to([RX, 0.4, 0]).rotate(-0.1)
        self.play(r.animate.set_color(TEAL), FadeOut(el), FadeOut(al), FadeOut(acc), FadeIn(pl), FadeIn(pd2), run_time=1.6)
        self.at("The lesson shows how")
        self.wait(0.5)
        self.finish()


# ---------------------------------------------------------------------------
class S13Open(WS):
    def construct(self):
        self.pt0 = None
        hy = RoundedRectangle(corner_radius=0.2, width=11.5, height=1.0, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([0, 3.2, 0])
        hl = T("hypothalamus", 28, TEXT).move_to(hy)
        pi = RoundedRectangle(corner_radius=0.2, width=11.5, height=1.0, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([0, -3.2, 0])
        pl = T("pituitary", 28, TEXT).move_to(pi)
        self.play(FadeIn(VGroup(hy, hl, pi, pl)), run_time=1.0)
        top, bot = 2.7, -2.7
        xL, xR = -3.4, 2.4
        tubeL = VGroup(Line([xL - 0.25, top, 0], [xL - 0.25, bot, 0], color=GREY, stroke_width=4), Line([xL + 0.25, top, 0], [xL + 0.25, bot, 0], color=GREY, stroke_width=4))
        self.play(Create(tubeL), run_time=0.8)
        # burst train: groups of dots with gaps
        clk = ValueTracker(0)
        clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clk)
        N = 12
        bursts = VGroup(*[Dot(radius=0.14, color=GOLD) for _ in range(N)])
        gateB = ValueTracker(0)

        def updB(m):
            for i, d in enumerate(m):
                grp, k = divmod(i, 4)
                u = ((clk.get_value() / 4.0) + grp / 3.0 + k * 0.025) % 1
                d.move_to([xL, top - (top - bot) * u, 0])
                d.set_opacity(min(1, u * 8, (1 - u) * 8) * gateB.get_value())
        bursts.add_updater(updB)
        self.add(bursts)
        self.play(gateB.animate.set_value(1), run_time=0.8)
        self.at("GnRH")
        gl = T("GnRH", 28, GOLD, weight=BOLD).move_to([xL - 1.6, 0.9, 0])
        self.play(FadeIn(gl), run_time=0.5)
        self.at("in bursts")
        bl = T("bursts", 28, GOLD, weight=BOLD).move_to([xL - 1.6, -0.1, 0])
        self.play(FadeIn(bl), run_time=0.6)
        self.at("Is the burst")
        bubble = VGroup(Ellipse(width=5.2, height=5.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([xR + 0.9, 0.0, 0]),
                        Circle(radius=0.2, stroke_color=GREY, stroke_width=3).move_to([xR - 2.1, -1.9, 0]),
                        Circle(radius=0.12, stroke_color=GREY, stroke_width=3).move_to([xR - 2.6, -2.3, 0]))
        sdots = VGroup(*[Dot(radius=0.14, color=GOLD) for _ in range(12)])
        gateS = ValueTracker(0)

        def updS(m):
            for i, d in enumerate(m):
                u = ((clk.get_value() / 4.0) + i / 12.0) % 1
                d.move_to([xR, 2.2 - 4.4 * u, 0])
                d.set_opacity(min(1, u * 8, (1 - u) * 8) * gateS.get_value())
        sdots.add_updater(updS)
        self.add(sdots)
        sl = T("one smooth\nstream", 28, GOLD, weight=BOLD, line_spacing=0.8).move_to([xR + 1.7, 0.0, 0])
        self.play(FadeIn(bubble), gateS.animate.set_value(1), FadeIn(sl), run_time=1.2)
        self.at("or is it the message")
        q = T("?", 140, TEAL, weight=BOLD).move_to([-0.35, 0.0, 0])
        self.play(GrowFromCenter(q), run_time=1.0)
        self.play(Wiggle(q, scale_value=1.1, rotation_angle=0.04 * TAU), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------
class S14Rule(WS):
    def construct(self):
        self.boxes()
        self.add(self.gon_icons("both"))
        self.tube()
        self.start_pulses(self.now())
        self.glow_pit()
        self.lh.set_value(0.6); self.fsh.set_value(0.6)
        self.strip(label=False)
        self.ribbon(); self.blood_dots(); bars = self.bars()
        self.at("brain drives")
        self.play(Indicate(self.hyp[0], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("through the pituitary")
        self.play(Indicate(self.pit[0], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("And the gonads")
        self.brake.set_value(0.5)
        r = self.ret(); rd = self.ret_dots()
        pd = pedal("brake").move_to([RX, 0.4, 0]).rotate(-0.1)
        self.play(Create(r), FadeIn(pd), run_time=0.9)
        pts = [[RE, GY - 0.4, 0], [5.5, GY - 0.4, 0], [5.5, 0.4, 0], [BARX[1] + 0.3, 0.4, 0]]
        path = VMobject(stroke_color=PURP, stroke_width=6)
        path.set_points_as_corners(pts)
        tip = Arrow([5.4, 0.4, 0], [BARX[1] + 0.3, 0.4, 0], buff=0, color=PURP, stroke_width=6, tip_length=0.28)
        self.play(Create(path), FadeIn(tip), run_time=0.9)
        self.flow(pts, 8, 4.0, [PURP], r=0.1)
        self.at("up as a break")
        self.play(pd.animate.rotate(-0.2).shift(DOWN * 0.1), self.lh.animate.set_value(0.4), self.fsh.animate.set_value(0.35), run_time=0.7)
        self.at("almost all the time")
        tag = T("ovulatory\ncycle: estradiol\nheld high, then\nLH surge", 28, ORED, line_spacing=0.8).move_to([-5.4, -1.5, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S15End(EndCard):
    LINE = "The brain drives the gonads in pulses; gonad hormones brake the brain."
