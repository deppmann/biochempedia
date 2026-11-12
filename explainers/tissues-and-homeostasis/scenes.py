"""Leak and Push-Back  (Biochemistrypedia explainer, tissues-and-homeostasis, film 1)

ONE WORLD: an ORANGE outside bar on the left, a TEAL inside bar next to it, a dashed set-point line,
an ORANGE leak arrow and a TEAL push-back arrow whose thickness is the computed flow.
Model (computed, every scene): leak = L (outside - inside); push-back = P (inside - set point);
the inside settles where the two are equal: inside - set = (outside - set) L / (L + P).

COLOR MAP: ORANGE = outside / leak, TEAL = inside / push-back / set point (dashed, lighter teal).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEAL_L = "#9FE8EC"      # the dashed set-point line (lighter so it shows over the teal bar)
OUT_X, IN_X, BW = -5.3, -1.2, 1.3
YB, YT = -3.0, 2.7
PB_X = IN_X + 1.3       # push-back arrow column
EPS = 1e-6


def Yt(T):               # temperature scale, deg F
    return YB + 0.0318 * (T - 40.0)


def Yd(v):               # schematic scale, degrees about the set point
    return -0.3 + 0.25 * v


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


def flow_arrow(p0, p1, w, color, clk, n=4):
    """A block arrow of thickness w with light dots streaming along it (the flow)."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    Ln = float(np.linalg.norm(d))
    if Ln < 1e-6 or w < 0.04:
        return VMobject()
    u = d / Ln
    nn = np.array([-u[1], u[0], 0.0])
    hl = min(0.5, 0.5 * Ln)
    hw = max(w * 0.5 + 0.16, 0.28)
    base = p1 - u * hl
    pts = [p0 + nn * w / 2, base + nn * w / 2, base + nn * hw, p1, base - nn * hw, base - nn * w / 2, p0 - nn * w / 2]
    body = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.95)
    g = VGroup(body)
    sl = Ln - hl
    for i in range(n):
        ph = (clk * 0.4 + i / n) % 1.0
        a = ph * sl
        b = min(a + 0.3, sl)
        if b - a > 0.02:
            g.add(Polygon(p0 + u * a + nn * w * 0.5, p0 + u * b + nn * w * 0.5, p0 + u * b - nn * w * 0.5,
                          p0 + u * a - nn * w * 0.5, stroke_width=0, fill_color=WHITE, fill_opacity=0.38))
    return g


def waves_mob(sc, xc, y0, n=3, h=0.8, color=ORANGE):
    def f():
        t = sc.clk.get_value()
        g = VGroup()
        y_0 = y0() if callable(y0) else y0
        for i in range(n):
            xs = xc + (i - (n - 1) / 2) * 0.4
            ys = np.linspace(y_0, y_0 + h, 18)
            pts = [[xs + 0.09 * np.sin(7 * (y - y_0) - 3 * t + i * 1.7), y, 0] for y in ys]
            m = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=0.75)
            m.set_points_smoothly(pts)
            g.add(m)
        return g
    return always_redraw(f)


def bracket(x, y0, y1, color, tick=0.14):
    return VGroup(Line([x, y0, 0], [x, y1, 0]), Line([x - tick, y0, 0], [x + tick, y0, 0]),
                  Line([x - tick, y1, 0], [x + tick, y1, 0])).set_stroke(color, 4)


def tube(x, color=GREY):
    return RoundedRectangle(corner_radius=0.12, width=BW, height=YT - YB, stroke_color=color, stroke_width=3,
                            fill_color=BG, fill_opacity=0.6).move_to([x, (YT + YB) / 2, 0]).set_z_index(-2)


def bar_rect(x, ytop, color):
    ytop = max(ytop, YB + 0.08)
    h = ytop - YB - 0.06
    return Rectangle(width=BW - 0.14, height=h, stroke_width=0, fill_color=color, fill_opacity=0.92).move_to(
        [x, YB + 0.06 + h / 2, 0])


def make_dial(center, color, getP, r=0.65, clk=None):
    face = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(center)
    ticks = VGroup(*[Line(np.array(center) + r * 0.78 * np.array([np.cos(a), np.sin(a), 0]),
                          np.array(center) + r * 0.95 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(color, 3)
                     for a in np.linspace(0, np.pi, 7)])

    def needle():
        P = max(getP(), 0.0)
        th = np.pi * (1 - P / (P + 1))
        if clk is not None:
            th += 0.025 * np.sin(clk.get_value() * 3.1)
        tip = np.array(center) + r * 0.82 * np.array([np.cos(th), np.sin(th), 0])
        return VGroup(Line(center, tip).set_stroke(color, 6), Dot(center, radius=0.07, color=color))
    return VGroup(face, ticks, always_redraw(needle))


class World:
    """The carried picture. Trackers: u (outside), x (inside), P (push-back strength), vis_* (arrow visibility)."""

    def __init__(s, sc, ymap, u, x, sp, L=1.0, P=100.0, wk=0.0062, y_leak=-2.3, floor=0.0, wob=0.0):
        s.sc, s.ym, s.sp, s.L, s.wk, s.yl, s.floor = sc, ymap, sp, L, wk, y_leak, floor
        s.u, s.x, s.P = ValueTracker(u), ValueTracker(x), ValueTracker(P)
        s.vis_leak, s.vis_pb, s.wob = ValueTracker(0), ValueTracker(0), ValueTracker(wob)
        for t in (s.u, s.x, s.P, s.vis_leak, s.vis_pb, s.wob):
            sc.add(t)
        s.out_tube, s.in_tube = tube(OUT_X), tube(IN_X)
        s.out_bar = always_redraw(lambda: bar_rect(OUT_X, s.ym(s.u.get_value()), ORANGE))
        s.in_bar = always_redraw(lambda: bar_rect(IN_X, s.ym(s.x.get_value()) + s.wob.get_value() * np.sin(
            sc.clk.get_value() * 2.7), TEAL))
        s.set_line = DashedLine([IN_X - 1.4, ymap(sp), 0], [IN_X + 1.55, ymap(sp), 0], color=TEAL_L, stroke_width=5,
                                dash_length=0.18).set_z_index(5)
        s.leak = always_redraw(s._leak)
        s.pb = always_redraw(s._pb)

    def ysp(s):
        return s.ym(s.sp)

    def leak_val(s):
        return s.L * (s.u.get_value() - s.x.get_value())

    def pb_val(s):
        return s.P.get_value() * (s.x.get_value() - s.sp)

    def _wid(s, flow, vis):
        w = min(0.95, abs(flow) * s.wk) * vis
        if s.floor and vis > 0.01:
            w = max(w, s.floor * vis)
        return w

    def _leak(s):
        fl = s.leak_val()
        w = s._wid(fl, s.vis_leak.get_value())
        x0, x1 = OUT_X + BW / 2 + 0.05, IN_X - BW / 2 - 0.05
        a, b = ([x0, s.yl, 0], [x1, s.yl, 0]) if fl >= 0 else ([x1, s.yl, 0], [x0, s.yl, 0])
        return flow_arrow(a, b, w, ORANGE, s.sc.clk.get_value())

    def _pb(s):
        fl = s.pb_val()
        w = s._wid(fl, s.vis_pb.get_value())
        y = s.ysp()
        a, b = ([PB_X, y + 1.55, 0], [PB_X, y + 0.15, 0]) if fl >= 0 else ([PB_X, y - 1.55, 0], [PB_X, y - 0.15, 0])
        return flow_arrow(a, b, w, TEAL, s.sc.clk.get_value())

    def quasi(s):
        """Keep the inside bar at its settled value for the current outside and push-back strength."""
        s.x.add_updater(lambda m: m.set_value(s.sp + (s.u.get_value() - s.sp) * s.L / (s.L + max(s.P.get_value(), 0))))


def relax(x0, u, k, Tm):
    """Exponential approach of x toward u at rate k for Tm seconds: returns (end value, rate_func)."""
    end = u - (u - x0) * np.exp(-k * Tm)
    return end, (lambda a: (1 - np.exp(-k * Tm * a)) / (1 - np.exp(-k * Tm)))


def new_clock(sc):
    sc.clk = ValueTracker(0)
    sc.clk.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(sc.clk)


# ------------------------------------------------------------------------------------ cartoons
def egg_mob(h=2.4, cooked=False):
    e = Ellipse(width=0.78 * h, height=h, stroke_color=WHITE, stroke_width=4,
                fill_color="#E9CF78" if not cooked else WHITE, fill_opacity=0.8 if not cooked else 1.0)
    return e


def man_mob(h=3.2):
    skin = "#E8C39E"
    head = Circle(radius=0.42, fill_color=skin, fill_opacity=1, stroke_width=0).move_to([0, 1.15, 0])
    eyes = VGroup(Dot([-0.15, 1.22, 0], radius=0.05, color=BG), Dot([0.15, 1.22, 0], radius=0.05, color=BG))
    smile = ArcBetweenPoints([-0.14, 1.02, 0], [0.14, 1.02, 0], angle=-1.3).set_stroke(BG, 3)
    torso = RoundedRectangle(corner_radius=0.2, width=1.3, height=1.55, fill_color="#7A5C9E", fill_opacity=1,
                             stroke_width=0).move_to([0, 0.05, 0])
    legs = VGroup(*[Rectangle(width=0.5, height=1.1, fill_color="#3B3350", fill_opacity=1, stroke_width=0
                              ).move_to([sx * 0.3, -1.15, 0]) for sx in (-1, 1)])
    arms = VGroup(*[Line([sx * 0.62, 0.6, 0], [sx * 0.9, -0.45, 0]).set_stroke("#7A5C9E", 16) for sx in (-1, 1)])
    g = VGroup(legs, arms, torso, head, eyes, smile)
    return g.set_height(h)


def sway(sc, mob, amp=0.035, f=1.6):
    mob._ang = 0.0
    c = mob.get_bottom()

    def up(m, dt):
        a = amp * np.sin(sc.clk.get_value() * f)
        m.rotate(a - m._ang, about_point=c)
        m._ang = a
    mob.add_updater(up)
    return mob


def stove_mob(sc):
    body = RoundedRectangle(corner_radius=0.12, width=1.9, height=2.1, fill_color="#3a3d46", fill_opacity=1,
                            stroke_color=GREY, stroke_width=3)
    pipe = Rectangle(width=0.32, height=1.3, fill_color="#3a3d46", fill_opacity=1, stroke_color=GREY,
                     stroke_width=3).next_to(body, UP, buff=0)
    legs = VGroup(*[Rectangle(width=0.2, height=0.3, fill_color=GREY, fill_opacity=1, stroke_width=0
                              ).next_to(body, DOWN, buff=0).shift(RIGHT * sx * 0.7) for sx in (-1, 1)])
    door = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.8, stroke_width=0, fill_color=ORANGE,
                            fill_opacity=0.9).move_to(body)
    door.add_updater(lambda m: m.set_fill(ORANGE, opacity=0.75 + 0.2 * np.sin(sc.clk.get_value() * 4)))
    return VGroup(pipe, legs, body, door)


def skin_panel(cx=4.2):
    epi = Rectangle(width=4.8, height=0.45, fill_color="#C99A78", fill_opacity=1, stroke_width=0).move_to([cx, 2.33, 0])
    derm = Rectangle(width=4.8, height=2.05, fill_color="#4a2f33", fill_opacity=1, stroke_width=0).move_to([cx, 1.07, 0])
    return VGroup(derm, epi)


# ======================================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Tissues, Organs and Homeostasis"
    TITLE = "Leak and Push-Back"


class S01Question(SpokenScene):
    def construct(self):
        new_clock(self)
        wall = Rectangle(width=13.2, height=6.4, fill_color="#1c1813", fill_opacity=1, stroke_color="#3b3326",
                         stroke_width=3).move_to([0, 0.1, 0])
        floor = Line([-6.6, -2.75, 0], [6.6, -2.75, 0]).set_stroke("#5a4a35", 5)
        self.add(wall, floor)
        stove = stove_mob(self).move_to([-4.9, -1.55, 0])
        waves = waves_mob(self, -4.9, 0.0, n=4, h=1.9)
        self.play(FadeIn(stove), run_time=1.0)
        self.add(waves)
        self.at("cook an egg")
        table = VGroup(Rectangle(width=2.4, height=0.18, fill_color="#6b4f33", fill_opacity=1, stroke_width=0),
                       *[Rectangle(width=0.18, height=1.0, fill_color="#6b4f33", fill_opacity=1, stroke_width=0
                                   ).shift(DOWN * 0.55 + RIGHT * sx * 1.0) for sx in (-1, 1)]).move_to([2.9, -2.1, 0])
        egg = egg_mob(1.0).move_to([2.9, -1.45, 0])
        self.play(FadeIn(table), FadeIn(egg, shift=DOWN * 0.2), run_time=0.8)
        self.at("why didn't the man cook")
        chair = VGroup(Rectangle(width=1.5, height=0.2, fill_color="#6b4f33", fill_opacity=1, stroke_width=0).move_to([0, -1.2, 0]),
                       Rectangle(width=0.2, height=2.0, fill_color="#6b4f33", fill_opacity=1, stroke_width=0).move_to([-0.7, -0.3, 0]),
                       *[Rectangle(width=0.15, height=0.95, fill_color="#6b4f33", fill_opacity=1, stroke_width=0
                                   ).move_to([sx * 0.62, -1.78, 0]) for sx in (-1, 1)]).shift(RIGHT * 0.1)
        man = sway(self, man_mob(2.9).move_to([0.1, -0.5, 0]))
        self.play(FadeIn(chair), FadeIn(man, shift=UP * 0.2), run_time=0.9)
        q = lab("?", 96, YELLOW, weight=BOLD).move_to([1.5, 0.5, 0])
        q.add_updater(lambda m: m.set_opacity(0.6 + 0.4 * np.sin(self.clk.get_value() * 4)))
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.at("Charles")
        name = lab("Charles Blagden, 1775", 28, TEXT).move_to([0.1, -3.3, 0])
        self.play(FadeIn(name), run_time=0.6)
        self.at("heated close to the boiling")
        th_x = 5.8
        tube_t = RoundedRectangle(corner_radius=0.2, width=0.4, height=3.3, stroke_color=GREY, stroke_width=4,
                                  fill_color=BG, fill_opacity=1).move_to([th_x, 0.1, 0])
        bulb = Circle(radius=0.32, stroke_color=GREY, stroke_width=4, fill_color=ORANGE, fill_opacity=1).move_to([th_x, -1.75, 0])
        fill = ValueTracker(0.05)
        col = always_redraw(lambda: Rectangle(width=0.2, height=3.0 * fill.get_value(), stroke_width=0, fill_color=ORANGE,
                                              fill_opacity=1).move_to([th_x, -1.5 + 1.5 * fill.get_value(), 0]))
        self.play(FadeIn(tube_t), FadeIn(bulb), run_time=0.5)
        self.add(col)
        self.play(fill.animate.set_value(0.95), run_time=2.6, rate_func=linear)
        tl = VGroup(lab("about 200 °F", 28, ORANGE), lab("(about 93 °C)", 28, ORANGE)).arrange(DOWN, buff=0.1).move_to([4.5, 2.7, 0])
        self.play(FadeIn(tl), run_time=0.6)
        self.at("On another visit")
        tag = lab("separate visit", 28, TEXT).move_to([2.9, -0.6, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.7)
        self.at("roasted hard")
        self.play(egg.animate.set_fill(WHITE, opacity=1.0), run_time=1.0)
        self.finish()


X_EGG_END = 176.0


class S02Egg(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yt, u=200, x=70, sp=98.6, L=1.0, P=0.0)
        egg = egg_mob(2.9).move_to([3.9, -0.6, 0])
        l_in = lab("inside: egg", 28, TEAL).move_to([IN_X, -3.45, 0])
        self.add(w.in_bar)
        self.play(FadeIn(egg, scale=0.85), FadeIn(w.in_tube), run_time=1.0)
        self.play(FadeIn(l_in), run_time=0.5)
        self.at("Hot air")
        waves = waves_mob(self, OUT_X, Yt(200) + 0.15, n=3, h=0.7)
        l_out = lab("outside: air", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        self.add(w.out_bar, w.leak)
        self.play(FadeIn(w.out_tube), FadeIn(l_out), run_time=0.5)
        self.add(waves)
        self.at("pours heat")
        self.play(w.vis_leak.animate.set_value(1), run_time=1.0)
        self.at("Nothing pushes back")
        none = lab("push-back:\nnone", 28, TEAL).move_to([1.1, 0.1, 0])
        self.play(FadeIn(none, shift=RIGHT * 0.2), run_time=0.8)
        self.at("So the egg keeps warming")
        self.play(FadeOut(none), run_time=0.3)
        k = 0.28
        t_cook = self.t_of("It cooks along") - 0.2
        T1 = max(0.5, t_cook - self.elapsed())
        end1, rf1 = relax(70, 200, k, T1)
        self.play(w.x.animate(rate_func=rf1).set_value(end1), run_time=T1)
        T2 = max(0.5, self.narration_s + 0.4 - self.elapsed())
        end2, rf2 = relax(end1, 200, k, T2)
        tag = lab("cooked", 28, YELLOW).move_to([3.9, -2.6, 0])
        self.play(egg.animate.set_fill(WHITE, opacity=1.0), FadeIn(tag, shift=UP * 0.15),
                  w.x.animate(rate_func=rf2).set_value(end2), run_time=T2)
        self.finish()


class S03Leak(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yt, u=200, x=X_EGG_END, sp=98.6, L=1.0, P=100.0)
        egg = egg_mob(2.9, cooked=True).move_to([3.9, -0.6, 0])
        l_in = lab("inside: egg", 28, TEAL).move_to([IN_X, -3.45, 0])
        l_out = lab("outside: air", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, Yt(200) + 0.15, n=3, h=0.7)
        w.vis_leak.set_value(1)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.leak, waves, egg, l_in, l_out)
        man = sway(self, man_mob(3.4).move_to([4.5, -0.35, 0]))
        l_in2 = lab("inside: core temperature", 28, TEAL).move_to([IN_X, -3.45, 0])
        self.play(FadeOut(egg), FadeOut(l_in), FadeIn(man, shift=UP * 0.2), FadeIn(l_in2),
                  w.x.animate(rate_func=smooth).set_value(98.6), run_time=2.0)
        self.at("The same air pours heat into him")
        self.wait(0.2)
        self.at("Call that flow the leak")
        l_leak = lab("leak", 30, ORANGE, weight=BOLD).move_to([-3.2, -1.6, 0])
        self.play(FadeIn(l_leak, scale=1.2), run_time=0.6)
        self.at("Yet the thermometer under his tongue")
        thermo = VGroup(Line([4.55, 0.62, 0], [5.35, 0.45, 0]).set_stroke(WHITE, 6),
                        Circle(radius=0.09, color=WHITE, fill_opacity=1).move_to([5.38, 0.44, 0]))
        chip_r = always_redraw(lambda: M(f"{w.x.get_value():.1f} °F", 30, WHITE).move_to([5.75, 0.0, 0]))
        self.play(FadeIn(thermo), FadeIn(chip_r), run_time=0.8)
        self.at("barely moved")
        self.play(w.x.animate(rate_func=smooth).set_value(99.6), run_time=1.4)
        self.at("It stayed about one degree above his usual")
        cap = lab("about 1 degree\nabove his usual", 28, TEAL).move_to([4.5, -2.75, 0])
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S04Pushback(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yt, u=200, x=99.6, sp=98.6, L=1.0, P=100.0, wob=0.0)
        man = sway(self, man_mob(3.4).move_to([4.5, -0.35, 0]))
        l_in2 = lab("inside: core temperature", 28, TEAL).move_to([IN_X, -3.45, 0])
        l_out = lab("outside: air", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        l_leak = lab("leak", 30, ORANGE, weight=BOLD).move_to([-3.2, -1.6, 0])
        waves = waves_mob(self, OUT_X, Yt(200) + 0.15, n=3, h=0.7)
        thermo = VGroup(Line([4.55, 0.62, 0], [5.35, 0.45, 0]).set_stroke(WHITE, 6),
                        Circle(radius=0.09, color=WHITE, fill_opacity=1).move_to([5.38, 0.44, 0]))
        chip_r = always_redraw(lambda: M(f"{w.x.get_value():.1f} °F", 30, WHITE).move_to([5.75, 0.0, 0]))
        w.vis_leak.set_value(1)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.leak, waves, man, l_in2, l_out, l_leak, thermo, chip_r)
        self.add(w.pb)
        self.play(w.vis_pb.animate.set_value(1), run_time=1.6)
        self.at("Call it pushback")
        l_pb = lab("push-back", 30, TEAL, weight=BOLD).move_to([1.95, -0.3, 0])
        self.play(FadeIn(l_pb, scale=1.2), run_time=0.6)
        self.at("Leak drags the inside toward the outside")
        up = Arrow([IN_X, -0.9, 0], [IN_X, -0.1, 0], buff=0, color=ORANGE, stroke_width=12, tip_length=0.3)
        self.play(FadeIn(up, shift=UP * 0.2), Indicate(l_leak, color=ORANGE, scale_factor=1.25), run_time=1.2)
        self.at("Pushback drags it toward a fixed value")
        down = Arrow([IN_X, -0.1, 0], [IN_X, -0.95, 0], buff=0, color=TEAL, stroke_width=12, tip_length=0.3)
        self.play(FadeOut(up), FadeIn(down, shift=DOWN * 0.2), Indicate(l_pb, color=TEAL, scale_factor=1.25), run_time=1.2)
        self.at("fixed value")
        self.play(Create(w.set_line), w.wob.animate.set_value(0.07), run_time=1.2)
        self.play(FadeOut(down), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- the loop (s05-s07)
BX, BWD, BHT = 2.9, 3.2, 1.2
Y_SENS, Y_INT, Y_EFF = 2.6, -0.1, -2.9


def shell(n, y, lit=False):
    rect = RoundedRectangle(corner_radius=0.16, width=BWD, height=BHT, stroke_color=TEAL, stroke_width=4,
                            fill_color=TEAL, fill_opacity=0.18 if lit else 0.05).move_to([BX, y, 0])
    rect.set_stroke(opacity=1.0 if lit else 0.4)
    badge = VGroup(Circle(radius=0.27, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1),
                   lab(str(n), 26, TEXT)).move_to([BX - BWD / 2 + 0.4, y, 0])
    return VGroup(rect, badge)


def pipe(pts, color=TEAL, op=1.0, w=5):
    pts = [np.array(p + [0], float) for p in pts]
    g = VGroup()
    for a, b in zip(pts[:-2], pts[1:-1]):
        g.add(Line(a, b))
    g.add(Arrow(pts[-2], pts[-1], buff=0, tip_length=0.24, max_tip_length_to_length_ratio=0.9,
                max_stroke_width_to_length_ratio=12))
    return g.set_stroke(color, w, opacity=op)


P_SENSE = [[IN_X, -0.95], [IN_X, Y_SENS], [BX - BWD / 2 - 0.04, Y_SENS]]
P_SI = [[BX, Y_SENS - BHT / 2 - 0.03], [BX, Y_INT + BHT / 2 + 0.04]]
P_SET = [[IN_X + 1.65, -1.14], [0.95, -1.14], [0.95, Y_INT], [BX - BWD / 2 - 0.04, Y_INT]]
P_IE = [[BX, Y_INT - BHT / 2 - 0.03], [BX, Y_EFF + BHT / 2 + 0.04]]
P_BACK = [[BX - BWD / 2 - 0.04, Y_EFF], [0.2, Y_EFF], [0.2, -2.0], [IN_X + BW / 2 + 0.05, -2.0]]
PIPES = [P_SENSE, P_SI, P_SET, P_IE, P_BACK]


def c_sense(op): return pipe(P_SENSE, op=op)
def c_si(op): return pipe(P_SI, op=op)
def c_set(op): return pipe(P_SET, op=op)
def c_ie(op): return pipe(P_IE, op=op)
def c_back(op): return pipe(P_BACK, op=op)


def _plen(pts):
    return sum(float(np.linalg.norm(np.array(b, float) - np.array(a, float))) for a, b in zip(pts[:-1], pts[1:]))


def _pos(pts, d):
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = np.array(a + [0], float), np.array(b + [0], float)
        L = float(np.linalg.norm(b - a))
        if d <= L:
            return a + (b - a) * d / L
        d -= L
    return np.array(pts[-1] + [0], float)


def flow_dots(sc, on):
    def f():
        t = sc.clk.get_value()
        g = VGroup()
        for i, pts in enumerate(PIPES):
            if not on[i]:
                continue
            L = _plen(pts)
            n = max(2, int(round(L / 1.3)))
            for k in range(n):
                g.add(Dot(_pos(pts, (t * 1.4 + k * L / n) % L), radius=0.15, color=WHITE).set_opacity(0.9).set_z_index(7))
        return g
    return always_redraw(f)


def numbered(n, text, size=30, color=TEXT):
    b = VGroup(Circle(radius=0.27, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1), lab(str(n), 26, TEXT))
    return VGroup(b, lab(text, size, color)).arrange(RIGHT, buff=0.22)


def loop_base(sc, wob=0.07):
    """Inside bar + set line (carried at the same place), no outside."""
    w = World(sc, Yt, u=200, x=99.6, sp=98.6, L=1.0, P=100.0, wob=wob)
    sc.add(w.in_tube, w.in_bar, w.set_line)
    return w


class S05LoopA(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yt, u=200, x=99.6, sp=98.6, L=1.0, P=100.0, wob=0.07)
        man = sway(self, man_mob(3.4).move_to([4.5, -0.35, 0]))
        l_in2 = lab("inside: core temperature", 28, TEAL).move_to([IN_X, -3.45, 0])
        l_out = lab("outside: air", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, Yt(200) + 0.15, n=3, h=0.7)
        w.vis_leak.set_value(1)
        w.vis_pb.set_value(1)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, man, l_in2, l_out)
        # the picture clears; the push-back arrow unfolds into the loop skeleton
        sh = [shell(3, Y_SENS), shell(4, Y_INT), shell(5, Y_EFF)]
        conns = [c_sense(0.35), c_si(0.35), c_set(0.35), c_ie(0.35), c_back(0.35)]
        self.play(FadeOut(man), FadeOut(waves), FadeOut(l_out), FadeOut(l_in2), FadeOut(w.out_tube), FadeOut(w.out_bar),
                  w.vis_leak.animate.set_value(0), w.vis_pb.animate.set_value(0), run_time=1.4)
        self.remove(w.out_bar)
        self.play(*[Create(c) for c in conns[:1]], FadeIn(sh[0]), run_time=0.7)
        self.play(Create(conns[1]), FadeIn(sh[1]), Create(conns[2]), run_time=0.7)
        self.play(Create(conns[3]), FadeIn(sh[2]), Create(conns[4]), run_time=0.8)
        self.add(flow_dots(self, [True] * 5))
        self.at("First,")
        l1 = numbered(1, "regulated variable").move_to([-4.4, 1.5, 0]).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(l1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("quantity being held")
        self.play(Indicate(w.in_tube, color=TEAL, scale_factor=1.04), run_time=1.2)
        self.at("Here it is core body temperature")
        l1b = lab("core body temperature", 28, TEAL).next_to(l1, DOWN, buff=0.3).align_to(l1, LEFT)
        self.play(FadeIn(l1b, shift=RIGHT * 0.2), run_time=0.7)
        self.at("Second,")
        l2 = numbered(2, "set point").move_to([-4.35, -0.35, 0])
        self.play(FadeIn(l2, shift=RIGHT * 0.2), run_time=0.7)
        self.at("reference value")
        self.play(Indicate(w.set_line, color=TEAL_L, scale_factor=1.1), run_time=1.4)
        self.finish()


def sensor_details(sc):
    strip = Rectangle(width=1.8, height=0.28, fill_color="#C99A78", fill_opacity=1, stroke_width=0).move_to([5.7, 3.1, 0])
    nerves = VGroup(*[Line([5.7 + dx, 2.96, 0], [5.7 + dx, 2.55, 0]).set_stroke(TEAL, 4) for dx in (-0.55, 0, 0.55)])
    tips = VGroup(*[Dot([5.7 + dx, 2.55, 0], radius=0.08, color=TEAL) for dx in (-0.55, 0, 0.55)])
    brain = Ellipse(width=1.2, height=0.85, fill_color="#D9A0B5", fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to([5.7, 1.35, 0])
    l_skin = lab("skin", 26, TEXT).move_to([5.7, 2.2, 0])
    l_br = lab("brain", 26, TEXT).move_to([5.7, 0.75, 0])
    return VGroup(strip, nerves, tips, brain, l_skin, l_br)


class S06LoopB(SpokenScene):
    def construct(self):
        new_clock(self)
        w = loop_base(self)
        l1 = numbered(1, "regulated variable").move_to([-4.4, 1.5, 0]).align_to([-6.6, 0, 0], LEFT)
        l1b = lab("core body temperature", 28, TEAL).next_to(l1, DOWN, buff=0.3).align_to(l1, LEFT)
        l2 = numbered(2, "set point").move_to([-4.35, -0.35, 0])
        sh = [shell(3, Y_SENS), shell(4, Y_INT), shell(5, Y_EFF)]
        cs = [c_sense(0.35), c_si(0.35), c_set(0.35), c_ie(0.35), c_back(0.35)]
        self.add(l1, l1b, l2, *sh, *cs)
        self.add(flow_dots(self, [True] * 5))
        self.at("the sensor")
        t_s = lab("sensor", 30, TEXT, weight=BOLD).move_to([BX + 0.35, Y_SENS, 0])
        sh3 = shell(3, Y_SENS, lit=True)
        self.play(Transform(sh[0], sh3), FadeIn(t_s), cs[0].animate.set_stroke(opacity=1.0), run_time=0.9)
        self.at("which measures")
        dot = Dot([IN_X, -0.95, 0], radius=0.14, color=WHITE)
        path = VMobject().set_points_as_corners([[IN_X, -0.95, 0], [IN_X, Y_SENS, 0], [BX - BWD / 2, Y_SENS, 0]])
        self.play(MoveAlongPath(dot, path), run_time=1.8, rate_func=linear)
        self.remove(dot)
        self.at("Temperature-sensitive nerve cells")
        det = sensor_details(self)
        self.play(FadeIn(det), run_time=1.0)
        self.at("in the skin and brain")
        dot2 = Dot([5.7, 2.55, 0], radius=0.14, color=WHITE)
        path2 = VMobject().set_points_as_corners([[5.7, 2.55, 0], [5.0, 2.6, 0], [BX + BWD / 2, Y_SENS, 0]])
        self.play(MoveAlongPath(dot2, path2), run_time=1.5, rate_func=linear)
        self.remove(dot2)
        self.at("the integrator")
        t_i = lab("integrator", 30, TEXT, weight=BOLD).move_to([BX + 0.35, Y_INT + 0.2, 0])
        sh4 = shell(4, Y_INT, lit=True)
        self.play(Transform(sh[1], sh4), FadeIn(t_i), cs[1].animate.set_stroke(opacity=1.0),
                  cs[2].animate.set_stroke(opacity=1.0), FadeOut(det), run_time=1.0)
        self.at("hypothalamus")
        t_h = lab("(hypothalamus)", 24, TEAL).move_to([BX + 0.35, Y_INT - 0.27, 0])
        self.play(FadeIn(t_h), run_time=0.7)
        self.at("the sensed value")
        c1 = lab("sensed", 28, TEXT).move_to([5.7, 0.45, 0])
        c2 = lab(">", 40, YELLOW, weight=BOLD).move_to([5.7, -0.1, 0])
        c3 = lab("set point", 28, TEAL).move_to([5.7, -0.65, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeIn(c2), FadeIn(c3, shift=UP * 0.1), run_time=0.7)
        self.at("sends out a command")
        l_c = lab("command", 28, TEAL).move_to([4.2, -1.5, 0])
        self.play(cs[3].animate.set_stroke(opacity=1.0), FadeIn(l_c, shift=DOWN * 0.1), run_time=0.9)
        self.finish()


def vessel_mob(vt, cx=4.2):
    return always_redraw(lambda: RoundedRectangle(corner_radius=0.1, width=4.3, height=vt.get_value(), stroke_width=0,
                                                  fill_color="#E0645A", fill_opacity=0.95).move_to([cx, 0.65, 0]))


def gland_mob():
    coil = VGroup(*[Circle(radius=r, stroke_color="#8CC7E8", stroke_width=4) for r in (0.3, 0.17)]).move_to([5.5, 1.25, 0])
    duct = Line([5.5, 1.55, 0], [5.5, 2.6, 0]).set_stroke("#8CC7E8", 5)
    drops = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color="#8CC7E8", fill_opacity=0.95).move_to(p)
                     for p in ([5.35, 2.72, 0], [5.65, 2.72, 0], [5.5, 2.9, 0])])
    return VGroup(coil, duct, drops)


class S07LoopC(SpokenScene):
    def construct(self):
        new_clock(self)
        w = loop_base(self)
        l1 = numbered(1, "regulated variable").move_to([-4.4, 1.5, 0]).align_to([-6.6, 0, 0], LEFT)
        l1b = lab("core body temperature", 28, TEAL).next_to(l1, DOWN, buff=0.3).align_to(l1, LEFT)
        l2 = numbered(2, "set point").move_to([-4.35, -0.35, 0])
        sh3, sh4, sh5 = shell(3, Y_SENS, True), shell(4, Y_INT, True), shell(5, Y_EFF)
        t_s = lab("sensor", 30, TEXT, weight=BOLD).move_to([BX + 0.35, Y_SENS, 0])
        t_i = lab("integrator", 30, TEXT, weight=BOLD).move_to([BX + 0.35, Y_INT + 0.2, 0])
        t_h = lab("(hypothalamus)", 24, TEAL).move_to([BX + 0.35, Y_INT - 0.27, 0])
        cs = [c_sense(1), c_si(1), c_set(1), c_ie(1), c_back(0.35)]
        l_c = lab("command", 28, TEAL).move_to([4.2, -1.5, 0])
        old = VGroup(sh3, sh4, t_s, t_i, t_h, cs[0], cs[1], cs[2])
        on7 = [True] * 5
        self.add(l1, l1b, l2, sh5, cs[3], cs[4], l_c, old)
        self.add(flow_dots(self, on7))
        self.at("the effectors")
        t_e = lab("effector", 30, TEXT, weight=BOLD).move_to([BX + 0.35, Y_EFF, 0])
        self.play(Transform(sh5, shell(5, Y_EFF, True)), FadeIn(t_e), cs[4].animate.set_stroke(opacity=1.0), run_time=0.9)
        self.at("As he warms")
        panel = skin_panel()
        vt = ValueTracker(0.22)
        vess = vessel_mob(vt)
        on7[0] = on7[1] = on7[2] = False
        self.play(FadeOut(old), FadeIn(panel), FadeIn(vess), run_time=1.2)
        self.at("skin blood vessels widen")
        lw = lab("skin vessels widen", 28, TEXT).move_to([4.2, -0.4, 0])
        self.play(vt.animate.set_value(0.62), FadeIn(lw), run_time=1.3)
        self.at("carry heat")
        harr = VGroup(*[Arrow([x, 1.0, 0], [x, 2.0, 0], buff=0, color=ORANGE, stroke_width=8, tip_length=0.22)
                        for x in (2.7, 3.5, 4.3)])
        self.play(*[GrowArrow(a) for a in harr], run_time=1.0)
        self.at("Sweat glands")
        gl = gland_mob()
        ls = lab("sweat glands", 28, TEXT).move_to([4.2, -0.4, 0])
        self.play(FadeOut(lw), FadeIn(ls), FadeIn(gl), run_time=1.0)
        self.at("which removes heat")
        wisp = waves_mob(self, 5.5, 3.0, n=3, h=0.55, color="#8CC7E8")
        le = lab("evaporation removes heat", 28, TEXT).move_to([4.2, -0.4, 0])
        self.add(wisp)
        self.play(FadeOut(ls), FadeIn(le), run_time=0.8)
        self.finish()


class S08Cold(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yt, u=200, x=99.6, sp=98.6, L=1.0, P=100.0, wob=0.07)
        w.quasi()
        w.vis_leak.set_value(1)
        w.vis_pb.set_value(1)
        l_in2 = lab("inside: core temperature", 28, TEAL).move_to([IN_X, -3.45, 0])
        l_out = lab("outside: air", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, Yt(200) + 0.15, n=3, h=0.7)
        panel = skin_panel()
        vt = ValueTracker(0.62)
        vess = vessel_mob(vt)
        harr = VGroup(*[Arrow([x, 1.0, 0], [x, 2.0, 0], buff=0, color=ORANGE, stroke_width=8, tip_length=0.22)
                        for x in (2.7, 3.5, 4.3)])
        gl = gland_mob()
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, l_in2, l_out,
                 panel, vess, harr, gl)
        # the outside cools: a cooling input; the inside follows the computed settled value
        self.play(FadeOut(waves), FadeOut(gl), FadeOut(harr), w.u.animate(rate_func=smooth).set_value(55), run_time=3.0)
        self.at("Skin vessels narrow")
        ln = lab("skin vessels narrow", 28, TEXT).move_to([4.2, -0.4, 0])
        self.play(vt.animate.set_value(0.12), FadeIn(ln), run_time=1.4)
        self.at("muscles shiver")
        shoulder, elbow0 = np.array([2.9, -1.65, 0]), np.array([3.7, -2.25, 0])
        upper = Line(shoulder, elbow0).set_stroke("#C99A78", 26)
        fore = always_redraw(lambda: Line(elbow0, elbow0 + 1.3 * np.array([np.cos(0.55 + 0.4 * np.sin(self.clk.get_value() * 12)),
                                                                           np.sin(0.55 + 0.4 * np.sin(self.clk.get_value() * 12)), 0])
                                          ).set_stroke("#C99A78", 26))
        lsh = lab("shivering", 28, TEXT).move_to([6.0, -2.0, 0])
        self.play(FadeIn(upper), FadeIn(fore), FadeIn(lsh), run_time=0.8)
        self.at("Either way")
        self.play(Indicate(w.set_line, color=TEAL_L, scale_factor=1.15), run_time=1.4)
        self.at("That is negative feedback")
        cap = VGroup(lab("negative feedback =", 26, YELLOW), lab("push-back toward the set point,", 26, YELLOW),
                     lab("from either side", 26, YELLOW)).arrange(DOWN, buff=0.12).move_to([3.9, -2.5, 0])
        self.play(FadeOut(upper), FadeOut(fore), FadeOut(lsh), FadeOut(ln), FadeIn(cap, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------- schematic (s09-s13)
D1, D2 = np.array([2.4, 2.3, 0]), np.array([2.4, 0.5, 0])


def schem(sc, u, x, P, floor=0.0, wob=0.0, arrows=True):
    w = World(sc, Yd, u=u, x=x, sp=0.0, L=1.0, P=P, wk=0.08, floor=floor, wob=wob)
    l_out = lab("outside", 28, ORANGE).move_to([OUT_X, -3.45, 0])
    l_in = lab("inside", 28, TEAL).move_to([IN_X, -3.45, 0])
    waves = waves_mob(sc, OUT_X, lambda: Yd(w.u.get_value()) + 0.12, n=3, h=0.6)
    w.vis_leak.set_value(1 if arrows else 0)
    w.vis_pb.set_value(1 if arrows else 0)
    sc.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, l_out, l_in)
    return w


def dials(sc, w):
    d1 = make_dial(D1, ORANGE, lambda: 1.0, clk=sc.clk)
    d2 = make_dial(D2, TEAL, lambda: w.P.get_value(), clk=sc.clk)
    t1 = lab("leak\nstrength", 28, ORANGE).next_to(D1 + RIGHT * 0.65, RIGHT, buff=0.3)
    t2 = lab("push-back\nstrength", 28, TEAL).next_to(D2 + RIGHT * 0.65, RIGHT, buff=0.3)
    return d1, d2, t1, t2


class S09Dial(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yd, u=0, x=0, sp=0.0, L=1.0, P=1.6, wk=0.08, floor=0.5)
        l_out = lab("outside", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        l_in = lab("inside", 28, TEAL).move_to([IN_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, lambda: Yd(w.u.get_value()) + 0.12, n=3, h=0.6)
        self.add(w.out_bar, w.in_bar, w.leak, w.pb)
        self.play(FadeIn(w.out_tube), FadeIn(w.in_tube), FadeIn(l_out), FadeIn(l_in), run_time=1.0)
        self.add(waves)
        self.play(Create(w.set_line), w.vis_leak.animate.set_value(1), w.vis_pb.animate.set_value(1), run_time=1.4)
        tag = lab("schematic", 24, TEXT).move_to([5.6, -3.45, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.at("That depends")
        d1, d2, t1, t2 = dials(self, w)
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(t1), FadeIn(t2), run_time=1.2)
        self.at("how strong pushback is")
        self.play(Indicate(t2, color=TEAL, scale_factor=1.12), run_time=1.2)
        self.at("compared with leak")
        self.play(Indicate(t1, color=ORANGE, scale_factor=1.12), run_time=1.2)
        self.at("Strength means")
        cap = lab("strength = pull per\ndegree of gap", 28, TEXT).move_to([4.6, -1.5, 0])
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.9)
        self.finish()


def cards_group():
    cs = VGroup(*[chip(t, TEAL, size=30) for t in ("all", "half", "none")]).arrange(RIGHT, buff=0.35).move_to([4.2, -2.55, 0])
    q = lab("inside follows:", 28, TEAL).move_to([4.2, -1.6, 0])
    return cs, q


class S10Predict(SpokenScene):
    def construct(self):
        new_clock(self)
        w = schem(self, 0, 0, 1.6, floor=0.5)
        w.u.set_value(0)
        d1, d2, t1, t2 = dials(self, w)
        self.add(d1, d2, t1, t2)
        self.play(w.P.animate(rate_func=smooth).set_value(1.0), run_time=2.4)
        eq = lab("push-back strength = leak strength", 26, YELLOW).move_to([3.6, -1.1, 0])
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.7)
        self.at("raise the outside by")
        self.play(FadeOut(eq), w.u.animate(rate_func=smooth).set_value(10), w.vis_pb.animate.set_value(0), run_time=2.0)
        br = bracket(-4.4, Yd(0), Yd(10), ORANGE)
        l10 = lab("+10", 32, ORANGE, weight=BOLD).move_to([-3.7, Yd(5), 0])
        self.play(Create(br), FadeIn(l10), run_time=0.9)
        self.at("Does the inside follow")
        cs, q = cards_group()
        self.play(FadeIn(q), FadeIn(cs, shift=UP * 0.15, lag_ratio=0.3), run_time=1.4)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yd, u=10, x=0, sp=0.0, L=1.0, P=1.0, wk=0.08, floor=0.0)
        l_out = lab("outside", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        l_in = lab("inside", 28, TEAL).move_to([IN_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, lambda: Yd(w.u.get_value()) + 0.12, n=3, h=0.6)
        w.vis_leak.set_value(1)
        w.vis_pb.set_value(0)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, l_out, l_in)
        d1, d2, t1, t2 = dials(self, w)
        br = bracket(-4.4, Yd(0), Yd(10), ORANGE)
        l10 = lab("+10", 32, ORANGE, weight=BOLD).move_to([-3.7, Yd(5), 0])
        cs, q = cards_group()
        self.add(d1, d2, t1, t2, br, l10, q, cs)
        cs.add_updater(lambda m: m.set_opacity(0.8 + 0.2 * np.sin(self.clk.get_value() * 4)))
        ring_bg = Circle(radius=0.38, stroke_color=GREY, stroke_width=5).move_to([6.1, 3.15, 0])
        prog = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(prog.get_value(), 0.001),
                                         stroke_color=TEAL, stroke_width=7).move_to(ring_bg.get_center()))
        self.add(ring_bg, ring)
        self.play(prog.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yd, u=10, x=0, sp=0.0, L=1.0, P=1.0, wk=0.08, floor=0.0)
        l_out = lab("outside", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        l_in = lab("inside", 28, TEAL).move_to([IN_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, lambda: Yd(w.u.get_value()) + 0.12, n=3, h=0.6)
        w.vis_leak.set_value(1)
        w.vis_pb.set_value(1)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, l_out, l_in)
        br = bracket(-4.4, Yd(0), Yd(10), ORANGE)
        l10 = lab("+10", 32, ORANGE, weight=BOLD).move_to([-3.7, Yd(5), 0])
        cs, q = cards_group()
        self.add(br, l10, q, cs)
        self.play(Indicate(cs[1], color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.at("In this simple model")
        # mini dials replace the big ones; the cards give way to the rule
        m1 = make_dial([2.4, 3.0, 0], ORANGE, lambda: 1.0, r=0.42, clk=self.clk)
        m2 = make_dial([4.7, 3.0, 0], TEAL, lambda: 1.0, r=0.42, clk=self.clk)
        n1 = lab("leak", 26, ORANGE).move_to([3.0, 2.35, 0]).move_to([2.4, 2.3, 0])
        n2 = lab("push-back", 26, TEAL).move_to([4.7, 2.3, 0])
        self.play(FadeOut(cs), FadeOut(q), FadeIn(m1), FadeIn(m2), FadeIn(n1), FadeIn(n2), run_time=0.8)
        k = 0.6
        T_rise = self.t_of("settles") + 0.8 - self.elapsed()
        end, rf = relax(0, 5.0, k, T_rise)
        rd = always_redraw(lambda: lab(f"+{w.x.get_value():.1f}", 32, TEAL, weight=BOLD).move_to(
            [IN_X, Yd(w.x.get_value()) + 0.45, 0]))
        self.add(rd)
        self.play(w.x.animate(rate_func=rf).set_value(end), run_time=T_rise)
        rule = VGroup(lab("inside shift =", 26, TEXT), lab("outside shift × leak strength", 26, TEXT),
                      lab("÷ (leak strength +", 26, TEXT), lab("push-back strength)", 26, TEXT)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.2, 0.9, 0])
        num = M("10 × 1 ÷ (1 + 1) = 5", 28, YELLOW).move_to([4.2, -0.35, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.at("With equal strengths")
        self.play(FadeIn(num, shift=UP * 0.1), run_time=0.8)
        settled = lab("settled: the two pulls\nare equal", 26, WHITE).move_to([4.2, -1.45, 0])
        self.play(FadeIn(settled), run_time=0.6)
        self.at("the two gaps")
        b_lo = bracket(-2.15, Yd(0), Yd(5), TEAL)
        b_hi = bracket(-2.15, Yd(5), Yd(10), ORANGE)
        c_lo = lab("from set\npoint: 5", 24, TEAL).move_to([-3.6, Yd(2.5), 0])
        c_hi = lab("to outside: 5", 24, ORANGE).move_to([-3.4, Yd(7.5), 0])
        self.play(FadeOut(br), FadeOut(l10), run_time=0.4)
        self.play(Create(b_lo), Create(b_hi), FadeIn(c_lo), FadeIn(c_hi), run_time=0.8)
        self.at("halfway")
        tg = lab("simple model: after settling,\nset point fixed, effectors\nbelow their limit", 24, TEXT).move_to([4.2, -2.85, 0])
        self.play(FadeIn(tg), run_time=0.6)
        self.finish()


class S13Ends(SpokenScene):
    def construct(self):
        new_clock(self)
        w = World(self, Yd, u=10, x=5.0, sp=0.0, L=1.0, P=1.0, wk=0.08, floor=0.0)
        w.quasi()
        l_out = lab("outside", 28, ORANGE).move_to([OUT_X, -3.45, 0])
        l_in = lab("inside", 28, TEAL).move_to([IN_X, -3.45, 0])
        waves = waves_mob(self, OUT_X, lambda: Yd(w.u.get_value()) + 0.12, n=3, h=0.6)
        w.vis_leak.set_value(1)
        w.vis_pb.set_value(1)
        d1, d2, t1, t2 = dials(self, w)
        self.add(w.out_tube, w.in_tube, w.out_bar, w.in_bar, w.set_line, w.leak, w.pb, waves, l_out, l_in, d1, d2, t1, t2)
        # push-back strength to zero: the inside follows completely
        self.play(w.P.animate(rate_func=smooth).set_value(0.0), run_time=2.4)
        T_sw = max(1.0, self.t_of("That end of the dial") - 0.25 - self.elapsed())
        self.play(w.u.animate(rate_func=smooth).set_value(4.0), run_time=T_sw / 2)
        self.play(w.u.animate(rate_func=smooth).set_value(10.0), run_time=T_sw / 2)
        self.at("That end of the dial")
        lc = lab("conformer:\nfraction near 1", 26, ORANGE).move_to([-3.4, 1.25, 0])
        ax_o, ay_o = np.array([2.3, -3.1, 0]), None
        axes = VGroup(Line([2.3, -3.1, 0], [6.4, -3.1, 0]), Line([2.3, -3.1, 0], [2.3, -1.0, 0])).set_stroke(TEXT, 4)
        xl = lab("push-back ÷ leak", 24, TEXT).move_to([4.5, -3.55, 0])
        yl = lab("fraction", 24, TEXT).move_to([3.2, -0.75, 0])
        t1l, t0l = lab("1", 24, TEXT).move_to([2.0, -1.1, 0]), lab("0", 24, TEXT).move_to([2.0, -3.1, 0])
        self.play(FadeIn(lc), Create(axes), FadeIn(xl), FadeIn(yl), FadeIn(t1l), FadeIn(t0l), run_time=1.4)
        px = lambda r: 2.3 + 4.1 * r / 10.0
        py = lambda f: -3.1 + 2.1 * f
        rr = np.linspace(0, 10, 60)
        curve = VMobject().set_points_smoothly([[px(r), py(1 / (1 + r)), 0] for r in rr]).set_stroke(YELLOW, 6)
        dotp = always_redraw(lambda: Dot([px(w.P.get_value()), py(1 / (1 + w.P.get_value())), 0], radius=0.14, color=WHITE).set_z_index(6))
        self.play(Create(curve), run_time=1.6)
        self.add(dotp)
        self.at("Turn pushback strength far above")
        self.play(FadeOut(lc), w.P.animate(rate_func=smooth).set_value(9.0), run_time=2.8)
        self.at("barely moves")
        for hi_lo in (4.0, 10.0):
            self.play(w.u.animate(rate_func=smooth).set_value(hi_lo), run_time=0.9)
        self.at("That end is a regulator")
        lr = lab("regulator:\nfraction near 0", 26, TEAL).move_to([-3.4, 1.25, 0])
        self.play(FadeIn(lr), run_time=0.7)
        self.finish()


class S14Back(SpokenScene):
    def construct(self):
        new_clock(self)
        clk = self.clk
        oa = ValueTracker(-1.5)
        o_tube = tube(OUT_X)
        o_bar = bar_rect(OUT_X, 2.2, ORANGE)
        waves = waves_mob(self, OUT_X, 2.3, n=3, h=0.6)
        l_out = lab("outside: hot room", 28, ORANGE).move_to([OUT_X + 0.5, -3.45, 0])
        man = sway(self, man_mob(2.8).move_to([-0.6, 0.1, 0]))
        tube_m = RoundedRectangle(corner_radius=0.1, width=1.0, height=2.8, stroke_color=GREY, stroke_width=3,
                                  fill_color=BG, fill_opacity=0.6).move_to([2.0, 0.1, 0]).set_z_index(-2)
        set_m = DashedLine([1.3, 0.15, 0], [2.7, 0.15, 0], color=TEAL_L, stroke_width=5, dash_length=0.15).set_z_index(5)
        l_man = lab("Blagden", 28, TEXT).move_to([3.8, 0.1, 0])
        wobm = ValueTracker(0.0)

        def bar_h():
            return 1.5 + wobm.get_value() * np.sin(clk.get_value() * 2.7)
        bar_m = always_redraw(lambda: Rectangle(width=0.86, height=bar_h(), stroke_width=0, fill_color=TEAL, fill_opacity=0.92
                                                ).move_to([2.0, 0.2 + oa.get_value() + 1.5 + 0.06 + bar_h() / 2 - 1.5 + 0.0, 0]))
        a_lk = always_redraw(lambda: flow_arrow([-4.5, 0.55 + 1.5 + oa.get_value(), 0], [-1.9, 0.55 + 1.5 + oa.get_value(), 0], 0.4, ORANGE, clk.get_value()))
        self.add(o_tube, o_bar, waves, l_out)
        self.play(FadeIn(man), FadeIn(tube_m), FadeIn(l_man), run_time=1.0)
        self.add(bar_m)
        self.play(FadeIn(a_lk), Create(set_m), run_time=1.0)
        l_leak = lab("leak", 28, ORANGE, weight=BOLD).move_to([-3.2, 1.05, 0])
        self.add(l_leak)
        self.at("body pushed back")
        a_pb = always_redraw(lambda: flow_arrow([-1.9, -0.05 + 1.5 + oa.get_value(), 0], [-4.5, -0.05 + 1.5 + oa.get_value(), 0], 0.4, TEAL, clk.get_value()))
        l_pb = lab("push-back", 28, TEAL, weight=BOLD).move_to([-3.2, -0.55, 0])
        self.add(a_pb)
        self.play(FadeIn(l_pb, shift=LEFT * 0.2), run_time=0.8)
        self.at("so his temperature barely moved")
        self.play(wobm.animate.set_value(0.08), run_time=0.8)
        self.at("The trials lasted minutes")
        tag = lab("brief trials,\nminutes long", 28, TEXT).move_to([5.6, -1.2, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.8)
        self.at("so they show pushback")
        self.play(Indicate(l_pb, color=TEAL, scale_factor=1.2), run_time=1.2)
        self.at("not at strength")
        sch = lab("schematic", 24, TEXT).move_to([5.8, -3.45, 0])
        self.play(FadeIn(sch), run_time=0.5)
        self.at("The egg had no pushback")
        grpA = VGroup(man, tube_m, set_m, l_man, l_leak, l_pb)
        egg = egg_mob(1.8).move_to([-0.6, -1.9, 0])
        l_egg = lab("egg", 28, TEXT).move_to([3.8, -1.9, 0])
        tube_e = RoundedRectangle(corner_radius=0.1, width=1.0, height=2.6, stroke_color=GREY, stroke_width=3,
                                  fill_color=BG, fill_opacity=0.6).move_to([2.0, -1.9, 0]).set_z_index(-2)
        ev = ValueTracker(0.3)
        bar_e = always_redraw(lambda: Rectangle(width=0.86, height=ev.get_value(), stroke_width=0, fill_color=TEAL,
                                                fill_opacity=0.92).move_to([2.0, -3.2 + 0.06 + ev.get_value() / 2, 0]))
        a_e = always_redraw(lambda: flow_arrow([-4.5, -1.9, 0], [-1.6, -1.9, 0], 0.4, ORANGE, clk.get_value()))
        self.add(bar_e, a_e)
        self.play(grpA.animate.shift(UP * 1.5), oa.animate.set_value(0.0), tag.animate.move_to([5.6, -0.1, 0]),
                  FadeIn(egg), FadeIn(tube_e), FadeIn(l_egg), run_time=1.0)
        Tm = max(1.0, self.narration_s + 0.4 - self.elapsed())
        end, rf = relax(0.3, 2.4, 0.3, Tm)
        self.play(ev.animate(rate_func=rf).set_value(end), run_time=Tm)
        self.finish()


class S15End(EndCard):
    LINE = "The stronger the push-back compared with leak, the less the inside follows."
