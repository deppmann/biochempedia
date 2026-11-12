"""Holding a Boulder Still (Diversity, Disturbance and Succession), film 2 of the lesson.

Same look as film 1 (../scenes.py): dark ground, NAVY 'equal species' columns for effective number,
a semicircle dial, a grey storm. Shore colours: Ulva GREEN, barnacles GREY, Gigartina RED, bare rock beige.
One world: boulders of three sizes stand at the same x in every scene (small -4.3, intermediate 0, large 4.3);
each has a clock above it. Everything on screen is schematic (Sousa's values are not drawn).
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

NAVY = "#5B7CFA"
ROCK = "#9C8A6E"
RIM = "#6E5F48"
BARN = GREY
GROUND = -2.3
XS, XM, XL = -4.3, 0.0, 4.3
SIZE_S, SIZE_M, SIZE_L = (1.7, 1.1), (2.7, 1.7), (3.8, 2.4)
CLK_Y, CLK_R = 1.3, 0.9
SEA_Y = -3.72


# ---------------------------------------------------------------- boulders and clocks
def patch_color(p, t, tufts):
    if t < 0.5:
        pres = float(np.clip((t - 0.15) / 0.3, 0, 1))
        if p.rr < pres:
            return GREEN if p.g < 0.6 else BARN
        return RED if (tufts and p.tuft) else None
    fr = float(np.clip((t - 0.4) / 0.55, 0, 1))
    if p.cr < fr:
        return RED
    gg = 0.55 * (1 - float(np.clip((t - 0.4) / 0.4, 0, 1)))
    return GREEN if p.g < gg else BARN


class Boulder:
    def __init__(self, cx, size, seed, t0=0.3, tufts=False, master=None):
        w, h = size
        self.cx, self.w, self.h = cx, w, h
        rng = random.Random(seed)
        cy = GROUND + h / 2
        self.center = np.array([cx, cy, 0.0])
        pts = []
        n = 14
        for i in range(n):
            a = 2 * PI * i / n
            rr = 1 + rng.uniform(-0.05, 0.05)
            pts.append([cx + 0.5 * w * rr * np.cos(a), cy + 0.5 * h * rr * np.sin(a), 0])
        self.body = Polygon(*pts, stroke_color=RIM, stroke_width=3, fill_color=ROCK, fill_opacity=1).round_corners(0.35 * h)
        self.body.set_z_index(1)
        self.t = master if master is not None else ValueTracker(t0)
        self.vis = ValueTracker(0)
        self.tufts = tufts
        n_p = max(6, int(round(w * 5.2)))
        r = 0.04 * w + 0.03
        self.r0 = r
        patches = VGroup()
        nA = int(n_p * 0.65)
        nB = n_p - nA
        specs = [(0.80, 0.78, 0.15 * PI, 0.85 * PI, nA), (0.52, 0.50, 0.25 * PI, 0.75 * PI, nB)]
        for fx, fy, a0, a1, k in specs:
            for j in range(k):
                th = a0 + (a1 - a0) * (j + rng.uniform(0.2, 0.8)) / k
                d = Circle(radius=r * rng.uniform(0.9, 1.15), stroke_width=0, fill_opacity=0)
                d.move_to([cx + 0.5 * w * fx * np.cos(th), cy + 0.5 * h * fy * np.sin(th), 0])
                d.rr, d.cr, d.g = rng.random(), rng.random(), rng.random()
                d.tuft = False
                patches.add(d)
        # three survivors: well separated along the upper face
        order = sorted(range(len(patches)), key=lambda i: patches[i].get_x())
        for q in (0.2, 0.55, 0.85):
            patches[order[int(q * (len(order) - 1))]].tuft = True
        patches.set_z_index(2)
        self.patches = patches

        def upd(g):
            tv, vv = self.t.get_value(), self.vis.get_value()
            for p in g.submobjects:
                col = patch_color(p, tv, self.tufts)
                if col is None:
                    p.set_fill(opacity=0)
                else:
                    p.set_fill(col, opacity=0.95 * vv)
        patches.add_updater(upd)
        self.group = VGroup(self.body, patches)

    def register(self, sc):
        sc.add(self.patches, self.t, self.vis)

    def appear(self):
        return [FadeIn(self.body), self.vis.animate.set_value(1)]

    def disappear(self):
        return [FadeOut(self.body), self.vis.animate.set_value(0)]

    def creep(self, rate, cap):
        self.t.add_updater(lambda m, dt: m.set_value(min(cap, m.get_value() + rate * dt)) if m.get_value() < cap else None)

    def stop(self):
        self.t.clear_updaters()

    def tuft_patches(self):
        return [p for p in self.patches if p.tuft]


SECT = [(0, .2, ROCK), (.2, .35, GREEN), (.35, .5, BARN), (.5, .5833, GREEN), (.5833, .6667, BARN), (.6667, .75, RED), (.75, 1.0, RED)]


class Clock:
    def __init__(self, cx, cy, R, t):
        self.t, self.cx, self.cy, self.R = t, cx, cy, R
        self.vis = ValueTracker(0)
        inner = 0.58 * R
        parts = VGroup()
        for a, b, col in SECT:
            s = AnnularSector(inner_radius=inner, outer_radius=R, angle=2 * PI * (b - a), start_angle=PI / 2 - 2 * PI * b,
                              fill_opacity=0.95, stroke_width=0, color=col).shift([cx, cy, 0])
            parts.add(s)
        parts.add(Circle(radius=R, stroke_color=TEXT, stroke_width=3).move_to([cx, cy, 0]),
                  Circle(radius=inner, stroke_color=TEXT, stroke_width=3).move_to([cx, cy, 0]))
        self.ring = parts
        c = np.array([cx, cy, 0.0])

        def mk():
            a = 2 * PI * self.t.get_value()
            v = self.vis.get_value()
            ln = Line(c, c + 0.95 * R * np.array([np.sin(a), np.cos(a), 0]), color=TEXT, stroke_width=6, stroke_opacity=v)
            hub = Dot(c, radius=0.09, color=TEXT).set_opacity(v)
            return VGroup(ln, hub)
        self.hand = always_redraw(mk)
        self.hand.set_z_index(6)

    def register(self, sc):
        sc.add(self.vis, self.hand)

    def appear(self):
        return [FadeIn(self.ring), self.vis.animate.set_value(1)]

    def sector_point(self, frac, r_scale=1.0):
        a = 2 * PI * frac
        return np.array([self.cx + r_scale * self.R * np.sin(a), self.cy + r_scale * self.R * np.cos(a), 0])


def wave_mob():
    pts = [[-1.2, 0, 0], [-0.8, 0.12, 0], [-0.3, 0.6, 0], [0.2, 1.15, 0], [0.65, 1.0, 0], [0.9, 0.35, 0], [1.2, 0, 0]]
    w = Polygon(*pts, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.45).round_corners(0.25)
    w.set_z_index(4)
    return w


def row_mob(cx, base, val, cw=0.42, ch=0.8, sp=0.52):
    g = VGroup()
    for i in range(4):
        f = min(max(val - i, 0), 1)
        if f <= 0.001:
            continue
        x = cx + (i - 1.5) * sp
        g.add(Rectangle(width=cw, height=ch, stroke_color=NAVY, stroke_width=2.5, fill_opacity=0).move_to([x, base + ch / 2, 0]))
        g.add(Rectangle(width=cw, height=ch * f, stroke_width=0, fill_color=NAVY, fill_opacity=0.9).move_to([x, base + ch * f / 2, 0]))
    return g


def row_live(cx, base, tr, **kw):
    return always_redraw(lambda: row_mob(cx, base, tr.get_value(), **kw))


def chain_link_v(x, y_top, y_bot, color=GREY):
    mid = (y_top + y_bot) / 2
    h = (y_top - y_bot) * 0.62
    a = RoundedRectangle(corner_radius=0.17, width=0.36, height=h, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([x, mid + (y_top - y_bot) * 0.19, 0])
    b = RoundedRectangle(corner_radius=0.17, width=0.36, height=h, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([x, mid - (y_top - y_bot) * 0.19, 0])
    return VGroup(a, b)


def chain_h(cx, y, n=3, color=GREY):
    g = VGroup()
    for i in range(n):
        g.add(RoundedRectangle(corner_radius=0.17, width=0.62, height=0.36, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([cx + (i - (n - 1) / 2) * 0.46, y, 0]))
    return g


def icon_ruler():
    r = Rectangle(width=1.7, height=0.42, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
    ticks = VGroup(*[Line([-0.8 + i * 0.32, 0.21, 0], [-0.8 + i * 0.32, 0.21 - (0.2 if i % 2 == 0 else 0.12), 0], color=TEXT, stroke_width=3) for i in range(6)])
    return VGroup(r, ticks)


def padlock():
    body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.35)
    sh = Arc(radius=0.2, start_angle=0, angle=PI, stroke_color=GOLD, stroke_width=5).shift(UP * 0.25)
    sh2 = VGroup(sh, Line([-0.2, 0.25, 0], [-0.2, 0.1, 0], color=GOLD, stroke_width=5), Line([0.2, 0.25, 0], [0.2, 0.1, 0], color=GOLD, stroke_width=5))
    return VGroup(body, sh2).scale(1.3)


def pin(color=GOLD, s=1.0):
    head = Circle(radius=0.28 * s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.9)
    tip = Polygon([-0.2 * s, -0.18 * s, 0], [0.2 * s, -0.18 * s, 0], [0, -0.7 * s, 0], stroke_width=0, fill_color=color, fill_opacity=0.9)
    return VGroup(tip, head.shift(UP * 0.0))


def frame_around(xs, w_each):
    x0, x1 = min(xs) - w_each / 2 - 0.15, max(xs) + w_each / 2 + 0.15
    fr = Rectangle(width=x1 - x0, height=1.55, stroke_color=GREY, stroke_width=6, fill_opacity=0).move_to([(x0 + x1) / 2, GROUND + 0.7, 0])
    posts = VGroup(*[Line([x, GROUND - 0.02, 0], [x, GROUND - 0.2, 0], color=GREY, stroke_width=9) for x in (x0 + 0.1, x1 - 0.1)])
    return VGroup(fr, posts)


def Ind(m, **kw):
    kw.setdefault('color', TEXT)
    return Indicate(m, **kw)


def txt(lines, size=28, color=TEXT, x=0.0, y=0.0):
    return VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.1).move_to([x, y, 0])


# ---------------------------------------------------------------- scene base
class Shore(SpokenScene):
    def until(self, phrase, nth=0, lead=0.2):
        return max(0.15, self.t_of(phrase, nth) - lead - self.elapsed())

    def reg(self, *things):
        for t in things:
            if hasattr(t, "register"):
                t.register(self)
            else:
                self.add(t)

    def base(self, sea=True):
        g = Line([-6.6, GROUND, 0], [6.6, GROUND, 0], color=GREY, stroke_width=4)
        self.add(g)
        if sea:
            tt = ValueTracker(0)
            tt.add_updater(lambda m, dt: m.increment_value(dt))
            self.add(tt)
            self.add(always_redraw(lambda: FunctionGraph(lambda x: 0.09 * np.sin(1.7 * x + 1.8 * tt.get_value()), x_range=[-6.8, 6.8, 0.2],
                                                         color=BLUE, stroke_width=5).shift([0, SEA_Y, 0])))
        return g

    def storm(self, flips=(), D=2.6, x0=-8.0, x1=8.0, dur=1.4, extra=()):
        wv = wave_mob()
        wv.move_to([x0, GROUND + 0.58, 0])
        self.add(wv)
        L = x1 - x0
        anims = [wv.animate(run_time=D, rate_func=linear).shift(RIGHT * L), *extra]
        seen = set()
        for b, to in flips:
            d = max(0.0, (b.cx - x0) / L * D - 0.55)
            anims.append(Succession(Wait(d), Rotate(b.group, angle=2 * PI, about_point=b.center, run_time=dur, rate_func=smooth,
                                                    suspend_mobject_updating=False)))
            if id(b.t) not in seen:
                seen.add(id(b.t))
                anims.append(Succession(Wait(d + 0.45), b.t.animate(run_time=0.5, rate_func=linear).set_value(to).build()))
        self.play(*anims)
        self.remove(wv)


def size_labels(sc, y=-2.85, names=("small", "intermediate", "large"), size=28):
    labs = VGroup(*[T(n, size).move_to([x, y, 0]) for n, x in zip(names, (XS, XM, XL))])
    return labs


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Diversity, Disturbance and Succession"
    TITLE = "Holding a Boulder Still"


class S01Link(Shore):
    def construct(self):
        self.base()
        S, M, L = Boulder(XS, SIZE_S, 1, 0.3), Boulder(XM, SIZE_M, 2, 0.62), Boulder(XL, SIZE_L, 3, 0.95)
        for b in (S, M, L):
            b.register(self)
        S.creep(0.06, 0.5)
        self.play(*S.appear(), *M.appear(), *L.appear(), run_time=1.6)
        self.at("winter waves", lead=0.4)
        self.storm([(S, 0.12), (M, 0.3)], D=3.0, dur=1.5)
        self.at("Middle")
        lab = T("most diverse", 34, GOLD).move_to([XM, 0.2, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), Ind(M.body, color=GOLD, scale_factor=1.06), run_time=1.2)
        self.at("diverse communities", lead=0.4)
        self.storm([(S, 0.12)], D=2.4, dur=1.3)
        self.at("Is that")
        q = T("?", 96, GOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(q, scale=1.5), run_time=0.8)
        self.at("size")
        rul = icon_ruler().move_to([-3.2, 2.7, 0])
        rl = T("size", 32).move_to([-3.2, 1.9, 0])
        self.play(FadeIn(rul, shift=DOWN * 0.2), FadeIn(rl), run_time=0.9)
        self.at("how often")
        wi = wave_mob().scale(0.45).move_to([3.2, 2.55, 0])
        wl = T("overturning", 32, BLUE).move_to([3.2, 1.9, 0])
        self.play(FadeIn(wi, shift=DOWN * 0.2), FadeIn(wl), run_time=0.9)
        self.play(Ind(q, scale_factor=1.3), run_time=1.0)
        self.finish()


class S02Shore(Shore):
    def construct(self):
        card = chip("Wayne Sousa, Ecology, 1979", GOLD, 32).move_to([0, 3.2, 0])
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=1.0)
        coast = [(-1.9, 3.0), (-1.7, 2.0), (-2.1, 1.0), (-1.6, 0.1), (-0.9, -0.9), (-0.1, -1.7), (0.9, -2.2), (2.4, -2.5)]
        land = Polygon(*[[x, y, 0] for x, y in coast], [3.6, -2.5, 0], [3.6, 3.0, 0], stroke_width=0, fill_color="#4B4638", fill_opacity=0.95)
        line = VMobject(color=TEXT, stroke_width=5).set_points_smoothly([np.array([x, y, 0]) for x, y in coast])
        mp = VGroup(land, line).shift(DOWN * 0.15)
        self.at("studied")
        self.play(FadeIn(land), Create(line), run_time=1.6)
        note = T("schematic map", 24, GREY).move_to([4.9, -3.2, 0])
        self.add(note)
        pn = pin().move_to([-0.15, -1.2, 0])
        lab = T("southern California coast", 30, TEXT).move_to([-3.4, -1.75, 0])
        self.at("southern")
        self.play(FadeIn(lab), run_time=0.8)
        self.at("California", lead=0.0)
        self.play(FadeIn(pn, shift=DOWN * 0.8), run_time=0.7)
        tip = pn.get_bottom()
        rp = Circle(radius=0.15, stroke_color=GOLD, stroke_width=4).move_to(tip)
        self.play(rp.animate(run_time=1.2).scale(5).set_stroke(opacity=0), run_time=1.2)
        self.remove(rp)
        self.at("There,", lead=0.1)
        self.base()
        S, M, L = Boulder(XS, SIZE_S, 1, 0.3), Boulder(XM, SIZE_M, 2, 0.62), Boulder(XL, SIZE_L, 3, 0.95)
        for b in (S, M, L):
            b.register(self)
        self.play(FadeOut(mp), FadeOut(lab), FadeOut(pn), FadeOut(note), *S.appear(), *M.appear(), *L.appear(), run_time=0.9)
        self.at("winter storm", lead=0.3)
        self.storm([(S, 0.12), (M, 0.3)], D=2.6, dur=1.4)
        self.finish()


class S03Reset(Shore):
    def construct(self):
        self.base()
        B = Boulder(0, (5.6, 2.8), 11, 0.66, tufts=True)
        B.register(self)
        self.play(*B.appear(), run_time=1.4)
        self.at("kills", lead=0.4)
        self.storm([(B, 0.05)], D=2.8, dur=1.8)
        self.at("opens")
        lab1 = T("bare rock", 34, TEXT).move_to([-3.4, 1.9, 0])
        ar1 = Arrow(lab1.get_bottom() + DOWN * 0.05, [-2.2, 0.55, 0], buff=0.05, color=TEXT, stroke_width=5)
        tf = sorted(B.tuft_patches(), key=lambda p: p.get_x())
        tgt = tf[-1]
        lab2 = T("survivors can regrow", 32, RED).move_to([3.5, 1.9, 0])
        ar2 = Arrow(lab2.get_bottom() + DOWN * 0.05, tgt.get_center() + UP * 0.12, buff=0.05, color=RED, stroke_width=5)
        self.play(FadeIn(lab1), GrowArrow(ar1), run_time=1.0)
        self.play(FadeIn(lab2), GrowArrow(ar2), *[p.animate(run_time=3.0).scale(1.7) for p in tf], run_time=1.0)
        self.at("So each turn", lead=0.2)
        lab3 = T("succession set back", 34, GOLD).move_to([0, 2.65, 0])
        ar3 = Arrow([3.2, 3.2, 0], [-3.2, 3.2, 0], buff=0, color=GOLD, stroke_width=7)
        self.play(FadeIn(lab3), GrowArrow(ar3, run_time=1.6), run_time=1.6)
        self.finish()


class S04Clock(Shore):
    def construct(self):
        self.base()
        B = Boulder(XM, SIZE_M, 21, 0.0)
        C = Clock(0, 1.3, 1.5, B.t)
        B.register(self)
        C.register(self)
        self.play(*B.appear(), *C.appear(), run_time=1.6)

        def lbl(text, frac, side, y):
            x = 3.9 if side > 0 else -3.9
            t = T(text, 30, TEXT)
            t.move_to([x, y, 0])
            if side > 0:
                t.align_to([2.5, 0, 0], LEFT)
                p1 = t.get_left() + LEFT * 0.08
            else:
                t.align_to([-2.5, 0, 0], RIGHT)
                p1 = t.get_right() + RIGHT * 0.08
            ln = Line(C.sector_point(frac, 1.0), p1, color=GREY, stroke_width=3)
            return VGroup(t, ln)
        l0 = lbl("bare rock", 0.1, 1, 2.45)
        l1 = lbl("Ulva + barnacles", 0.35, 1, 0.5)
        l2 = lbl("mixed", 0.625, -1, 0.5)
        l3 = lbl("Gigartina", 0.875, -1, 2.45)
        self.at("counting", lead=0.4)
        title = T("time since last cleared", 32, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(title), B.t.animate(run_time=self.until("fully"), rate_func=linear).set_value(0.1))
        self.play(FadeIn(l0, run_time=0.6), B.t.animate(run_time=self.until("Ulva"), rate_func=linear).set_value(0.2))
        self.play(FadeIn(l1, run_time=0.6), B.t.animate(run_time=self.until("Red"), rate_func=linear).set_value(0.4))
        self.play(FadeIn(l2, run_time=0.6), B.t.animate(run_time=self.until("Without"), rate_func=linear).set_value(0.64))
        self.play(B.t.animate(run_time=self.until("often"), rate_func=linear).set_value(0.74))
        self.play(FadeIn(l3, run_time=0.6), B.t.animate(run_time=self.until("Survivors"), rate_func=linear).set_value(0.97))
        cap = T("usual order on a cleared face; survivors can change it", 26, GOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(cap), Ind(C.ring, scale_factor=1.05, color=GOLD), B.t.animate(run_time=1.6, rate_func=linear).set_value(0.995))
        self.finish()


def three(sc, ts=(0.25, 0.5, 0.1), seeds=(31, 32, 33)):
    S, M, L = Boulder(XS, SIZE_S, seeds[0], ts[0]), Boulder(XM, SIZE_M, seeds[1], ts[1]), Boulder(XL, SIZE_L, seeds[2], ts[2])
    cl = [Clock(b.cx, CLK_Y, CLK_R, b.t) for b in (S, M, L)]
    for b in (S, M, L):
        b.register(sc)
    for c in cl:
        c.register(sc)
    return S, M, L, cl


class S05Sizes(Shore):
    def construct(self):
        self.base()
        S, M, L, cl = three(self, (0.25, 0.5, 0.1))
        labs = size_labels(self)
        S.creep(0.07, 0.45)
        L.creep(0.067, 0.975)
        anims = []
        for b, c in zip((S, M, L), cl):
            anims += b.appear() + c.appear()
        self.play(*anims, FadeIn(labs), run_time=1.4)
        self.storm([(S, 0.12)], D=2.0, dur=1.2)
        self.at("snapping", lead=0.5)
        self.storm([(S, 0.14)], D=2.2, dur=1.2)
        self.at("They carry")
        ub = T("Ulva + barnacles", 30, TEXT).move_to([XS, 2.85, 0])
        self.play(FadeIn(ub), run_time=0.8)
        self.at("ulva", lead=0.5)
        self.storm([(S, 0.14)], D=2.4, dur=1.3)
        self.at("Large", lead=0.1)
        self.play(Ind(L.body, scale_factor=1.04), run_time=1.0)
        self.at("rarely", lead=0.3)
        self.storm([(S, 0.12)], D=2.4, dur=1.3)
        self.at("takes")
        gg = T("Gigartina", 32, RED).move_to([XL, 2.85, 0])
        self.play(FadeIn(gg), run_time=0.8)
        self.finish()


class S06Middle(Shore):
    def construct(self):
        self.base()
        S, M, L, cl = three(self, (0.3, 0.5, 0.97))
        labs = size_labels(self)
        self.add(labs)
        anims = []
        for b, c in zip((S, M, L), cl):
            anims += b.appear() + c.appear()
        self.play(*anims, run_time=0.9)
        S.creep(0.07, 0.45)
        L.creep(0.01, 0.99)
        M.creep(0.1, 0.62)
        self.play(Ind(M.body, scale_factor=1.05), run_time=1.0)
        self.at("turn now", lead=0.5)
        self.storm([(S, 0.14), (M, 0.2)], D=2.6, dur=1.4)
        self.at("partway")
        self.play(Ind(cl[1].ring, scale_factor=1.08), run_time=1.2)
        self.at("most diverse", lead=0.4)
        trs = [ValueTracker(0) for _ in range(3)]
        rows = [row_live(x, 2.45, t) for x, t in zip((XS, XM, XL), trs)]
        self.add(*rows)
        note = T("schematic: not Sousa's values", 26, GREY).move_to([0, -3.35, 0])
        self.play(trs[0].animate.set_value(1.8), trs[1].animate.set_value(3.4), trs[2].animate.set_value(1.4), FadeIn(note), run_time=1.8)
        self.finish()


class S07Confound(Shore):
    def construct(self):
        self.base()
        S, M, L = Boulder(XS, SIZE_S, 41, 0.3), Boulder(XM, SIZE_M, 42, 0.62), Boulder(XL, SIZE_L, 43, 0.95)
        for b in (S, M, L):
            b.register(self)
        S.creep(0.06, 0.5)
        self.play(*S.appear(), *M.appear(), *L.appear(), run_time=0.5)
        self.at("size", lead=0.3)
        a1 = Arrow([-4.8, 2.5, 0], [4.8, 2.5, 0], buff=0, color=TEXT, stroke_width=8)
        l1 = T("size", 32, TEXT).move_to([0, 3.1, 0])
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.8)
        a2 = Arrow([-4.8, 1.0, 0], [4.8, 1.0, 0], buff=0, color=BLUE, stroke_width=8)
        l2 = T("how often overturned", 32, BLUE).move_to([0, 0.45, 0])
        self.at("overturning", lead=0.3)
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.8)
        self.at("travel", lead=0.3)
        chains = VGroup(*[chain_link_v(x, 2.5, 1.0) for x in (-4.0, -2.6, 2.6, 4.0)])
        conf = T("confounded", 32, GOLD).move_to([0, 1.75, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in chains], lag_ratio=0.2), run_time=0.9)
        self.play(FadeIn(conf), run_time=0.5)
        self.at("small rocks", lead=0.3)
        self.storm([(S, 0.12)], D=2.2, dur=1.2)
        self.at("A bigger", lead=0.1)
        self.play(FadeOut(VGroup(a1, a2, l1, l2, chains, conf)), run_time=0.8)
        br = VGroup()
        for b in (S, M, L):
            y = GROUND + b.h + 0.35
            hw = 0.4 * b.w
            br.add(VGroup(Line([b.cx - hw, y, 0], [b.cx + hw, y, 0], color=GOLD, stroke_width=6),
                          Line([b.cx - hw, y - 0.12, 0], [b.cx - hw, y + 0.12, 0], color=GOLD, stroke_width=6),
                          Line([b.cx + hw, y - 0.12, 0], [b.cx + hw, y + 0.12, 0], color=GOLD, stroke_width=6)))
        sa = T("surface area", 32, GOLD).move_to([0, 1.5, 0])
        self.play(LaggedStart(*[Create(x) for x in br], lag_ratio=0.3), FadeIn(sa), run_time=1.4)
        self.at("more species", lead=0.3)
        ms = T("more species?", 32, TEXT).move_to([0, 2.4, 0])
        self.play(FadeIn(ms), *[Ind(x, scale_factor=1.12) for x in br], run_time=1.4)
        self.at("pattern alone", lead=0.2)
        self.play(FadeOut(VGroup(br, sa, ms)), run_time=0.7)
        self.at("cannot")
        rul = icon_ruler().move_to([-3.2, 2.7, 0])
        rl = T("size", 32).move_to([-3.2, 1.9, 0])
        wi = wave_mob().scale(0.45).move_to([3.2, 2.55, 0])
        wl = T("overturning", 32, BLUE).move_to([3.2, 1.9, 0])
        q = T("?", 96, GOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(rul), FadeIn(rl), FadeIn(wi), FadeIn(wl), FadeIn(q, scale=1.4), run_time=1.0)
        self.play(Ind(q, scale_factor=1.3), run_time=1.0)
        self.finish()


FXS = (-5.1, -3.5, -1.9)
LXS = (1.9, 3.5, 5.1)
SIZE_T = (1.3, 0.9)


def groups(sc, tf, tl, seeds=(51, 52, 53, 54, 55, 56)):
    F = [Boulder(x, SIZE_T, s, 0.0, master=tf) for x, s in zip(FXS, seeds[:3])]
    Lo = [Boulder(x, SIZE_T, s, 0.0, master=tl) for x, s in zip(LXS, seeds[3:])]
    for b in F + Lo:
        b.patches.add_updater  # noqa
        sc.add(b.patches, b.vis)
    sc.add(tf, tl)
    return F, Lo


class S08Test(Shore):
    def construct(self):
        self.base()
        tf, tl = ValueTracker(0.3), ValueTracker(0.3)
        F, Lo = groups(self, tf, tl)
        allb = F + Lo
        self.play(*[a for b in allb for a in b.appear()], run_time=1.0)
        self.at("held", lead=0.3)
        sz = T("size", 32).move_to([-3.4, 3.3, 0])
        ov = T("overturning", 32, BLUE).move_to([3.4, 3.3, 0])
        ch = chain_h(0, 3.3, 3)
        self.play(FadeIn(sz), FadeIn(ov), FadeIn(ch), *[Ind(b.body, scale_factor=1.08) for b in F], run_time=1.0)
        self.at("fixed", lead=0.3)
        fr = frame_around(FXS, 1.3)
        pl = padlock().move_to([-3.5, 2.2, 0])
        fl = T("fixed: cannot overturn", 30, GOLD).move_to([-3.5, 1.15, 0])
        self.play(Create(fr), FadeIn(pl, scale=1.4), FadeIn(fl), run_time=1.2)
        self.at("waves", lead=0.3)
        snap = [Succession(Wait(1.3), AnimationGroup(ch[0].animate(run_time=0.7).shift(LEFT * 0.5).set_stroke(opacity=0.4).build(),
                                                    ch[2].animate(run_time=0.7).shift(RIGHT * 0.5).set_stroke(opacity=0.4).build(),
                                                    FadeOut(ch[1], run_time=0.5)))]
        self.storm([], D=2.4, x0=-8.0, x1=-0.4, extra=snap)
        self.at("Similar", lead=0.1)
        self.play(*[Ind(b.body, scale_factor=1.08) for b in Lo], run_time=1.2)
        self.at("loose", lead=0.2)
        ll = T("loose: free to roll", 30, TEXT).move_to([3.5, 1.15, 0])
        self.play(FadeIn(ll), run_time=0.8)
        self.at("free to", lead=0.5)
        self.storm([(b, 0.12) for b in Lo], D=2.2, dur=1.2)
        self.at("Both", lead=0.1)
        ar = DoubleArrow([-3.5, -2.9, 0], [3.5, -2.9, 0], buff=0, color=GREY, stroke_width=4)
        same = T("same height on the shore", 28, TEXT).move_to([0, -3.2, 0])
        self.play(FadeIn(ar), FadeIn(same), run_time=1.0)
        self.finish()


def time_bar(label="1975 to early 1977"):
    out = Rectangle(width=11.2, height=0.62, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([0, 3.1, 0])
    lab = T(label, 28, TEXT).move_to(out)
    lab.set_z_index(5)
    return out, lab


def clocks_two(sc, tf, tl):
    cf, cl = Clock(-3.5, 0.5, CLK_R, tf), Clock(3.5, 0.5, CLK_R, tl)
    cf.register(sc)
    cl.register(sc)
    return cf, cl


class S09Predict(Shore):
    def construct(self):
        self.base()
        tf, tl = ValueTracker(0.35), ValueTracker(0.35)
        F, Lo = groups(self, tf, tl)
        cf, cl = clocks_two(self, tf, tl)
        fr = frame_around(FXS, 1.3)
        fx = T("fixed", 28).move_to([-3.5, -2.85, 0])
        lx = T("loose", 28).move_to([3.5, -2.85, 0])
        self.add(fr, fx, lx)
        tl_creep = Lo[0]
        tl_creep.creep(0.08, 0.45)
        self.play(*[a for b in F + Lo for a in b.appear()], *cf.appear(), *cl.appear(), run_time=1.0)
        self.at("If", lead=0.0)
        out, lab = time_bar()
        self.play(FadeIn(out), FadeIn(lab), run_time=1.0)
        self.at("stay sparse", lead=0.3)
        tg1 = chip("stay sparse", TEXT, 28).move_to([-4.6, 1.95, 0])
        self.play(FadeIn(tg1, shift=DOWN * 0.2), run_time=0.8)
        self.at("If overturning", lead=0.3)
        self.storm([(b, 0.2) for b in Lo], D=2.4, dur=1.3)
        self.at("what should", lead=0.1)
        tg2 = chip("?", GOLD, 34).move_to([-2.4, 1.95, 0])
        self.play(FadeIn(tg2, scale=1.4), run_time=0.8)
        self.play(Ind(tg2, scale_factor=1.3), run_time=1.0)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        base = Line([-6.6, GROUND, 0], [6.6, GROUND, 0], color=GREY, stroke_width=4)
        tf, tl = ValueTracker(0.35), ValueTracker(0.35)
        F = [Boulder(x, SIZE_T, s, 0.0, master=tf) for x, s in zip(FXS, (51, 52, 53))]
        Lo = [Boulder(x, SIZE_T, s, 0.0, master=tl) for x, s in zip(LXS, (54, 55, 56))]
        for b in F + Lo:
            self.add(b.body, b.patches, b.vis)
            b.vis.set_value(1)
        self.add(base, frame_around(FXS, 1.3))
        self.add(T("fixed", 28).move_to([-3.5, -2.85, 0]), T("loose", 28).move_to([3.5, -2.85, 0]))
        cap = txt(["Predict: what do the fixed", "small boulders become?"], 34, TEXT, 0, 2.5)
        q = T("?", 96, GOLD).move_to([-3.5, 0.2, 0])
        self.add(cap, q)
        ring_t = ValueTracker(1)
        ring = always_redraw(lambda: VGroup(Circle(radius=0.5, color=GREY, stroke_width=4),
                                            Arc(radius=0.5, start_angle=PI / 2, angle=2 * PI * ring_t.get_value(), color=GOLD, stroke_width=8)
                                            ).move_to([0, -0.2, 0]))
        self.add(ring, ring_t)
        self.play(ring_t.animate.set_value(0.001), run_time=4.9, rate_func=linear)
        self.finish()


class S11Reveal(Shore):
    def construct(self):
        self.base()
        tf, tl = ValueTracker(0.35), ValueTracker(0.3)
        F, Lo = groups(self, tf, tl)
        cf, cl = clocks_two(self, tf, tl)
        self.add(frame_around(FXS, 1.3), T("fixed", 28).move_to([-3.5, -2.85, 0]), T("loose", 28).move_to([3.5, -2.85, 0]))
        out, lab = time_bar()
        fill_t = ValueTracker(0.001)
        fill = always_redraw(lambda: Rectangle(width=11.2 * fill_t.get_value(), height=0.62, stroke_width=0, fill_color=TEAL, fill_opacity=0.4)
                             .move_to([-5.6 + 5.6 * fill_t.get_value(), 3.1, 0]))
        self.add(fill, out, lab, fill_t)
        for b in F + Lo:
            b.vis.set_value(1)
            self.add(b.body)
        cf.vis.set_value(1)
        cl.vis.set_value(1)
        self.add(cf.ring, cl.ring)
        tf.add_updater(lambda m, dt: m.set_value(min(0.95, m.get_value() + 0.074 * dt)) if self.elapsed() > 0.5 else None)
        fill_t.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / 9.6)))
        Lo[0].creep(0.05, 0.42)
        self.at("They moved", lead=0.0)
        self.storm([(b, 0.2) for b in Lo], D=2.6, dur=1.3)
        self.at("Ulva", lead=0.2)
        self.play(Ind(F[1].body, scale_factor=1.1), run_time=1.5)
        self.at("red algae", lead=0.2)
        self.play(*[Ind(b.body, scale_factor=1.08, color=RED) for b in F], run_time=1.6)
        self.at("cover most", lead=0.2)
        self.wait(self.until("The loose", lead=0.3))
        self.at("The loose", lead=0.3)
        self.storm([(b, 0.2) for b in Lo], D=2.6, dur=1.3)
        self.play(*[Ind(b.body, scale_factor=1.08) for b in Lo], run_time=1.2)
        self.finish()


class S12Result(Shore):
    def construct(self):
        self.base()
        XF, XI = -2.7, 2.7
        F = Boulder(XF, SIZE_S, 61, 0.85)
        M = Boulder(XI, SIZE_M, 62, 0.62)
        for b in (F, M):
            b.register(self)
        M.creep(0.1, 0.62)
        fr = frame_around([XF], 1.7)
        self.add(fr)
        lf = T("fixed small", 28).move_to([XF, -2.85, 0])
        li = T("intermediate", 28).move_to([XI, -2.85, 0])
        self.add(lf, li)
        trf, tri = ValueTracker(1.6), ValueTracker(3.4)
        rf, ri = row_live(XF, 0.9, trf, cw=0.5, ch=1.1, sp=0.64), row_live(XI, 0.9, tri, cw=0.5, ch=1.1, sp=0.64)
        sch = T("schematic", 26, GREY).move_to([0, 1.5, 0])
        self.play(*F.appear(), *M.appear(), FadeIn(rf), FadeIn(ri), FadeIn(sch), run_time=1.4)
        self.at("became", lead=0.3)
        lab = txt(["as species-rich and diverse as", "larger, intermediate-sized boulders"], 30, TEXT, 0, 3.2)
        self.play(trf.animate(run_time=3.0, rate_func=smooth).set_value(3.4), Succession(Wait(1.1), FadeIn(lab, run_time=0.9)))
        self.play(Ind(ri, scale_factor=1.1), run_time=1.0)
        self.storm([(M, 0.25)], D=2.0, dur=1.2, x0=-8.0, x1=8.0)
        self.at("Their smaller", lead=0.1)
        y = GROUND + F.h + 0.35
        br = VGroup(Line([XF - 0.7, y, 0], [XF + 0.7, y, 0], color=GOLD, stroke_width=6),
                    Line([XF - 0.7, y - 0.12, 0], [XF - 0.7, y + 0.12, 0], color=GOLD, stroke_width=6),
                    Line([XF + 0.7, y - 0.12, 0], [XF + 0.7, y + 0.12, 0], color=GOLD, stroke_width=6))
        sm = T("smaller surface", 30, GOLD).move_to([XF, -0.2, 0])
        self.play(Create(br), FadeIn(sm), run_time=1.2)
        self.at("did not stop", lead=0.1)
        self.play(Ind(rf, scale_factor=1.1), run_time=1.2)
        self.at("how often", lead=0.3)
        ban = T("on this shore: overturning frequency, not surface area alone", 28, GOLD).move_to([0, 0.5, 0])
        self.play(FadeIn(ban), run_time=1.2)
        self.at("surface area", lead=0.2)
        self.play(Ind(br, scale_factor=1.12), run_time=1.2)
        self.at("accounted", lead=0.2)
        self.play(Ind(ban, scale_factor=1.04), run_time=1.4)
        self.finish()


def slider(y, label, color, pos, alpha=1.0):
    lab = T(label, 32, color).move_to([-5.2, y, 0]).align_to([-5.4, 0, 0], LEFT)
    tr = Line([-2.2, y, 0], [1.1, y, 0], color=color, stroke_width=8, stroke_opacity=alpha)
    kn = Circle(radius=0.24, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.85 * alpha).move_to([pos, y, 0])
    return lab, tr, kn


class S13Scope(Shore):
    def construct(self):
        panel = RoundedRectangle(corner_radius=0.2, width=7.4, height=3.8, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to([-2.0, 0.4, 0])
        a_lab, a_tr, a_kn = slider(1.3, "how often", GOLD, -0.5)
        b_lab, b_tr, b_kn = slider(-0.5, "how hard", GREY, -0.5, 0.45)
        b_lab.set_opacity(0.55)
        self.play(FadeIn(panel), FadeIn(a_lab), Create(a_tr), FadeIn(a_kn), FadeIn(b_lab), Create(b_tr), FadeIn(b_kn), run_time=1.4)
        self.at("how often", lead=0.3)
        for x in (-1.8, 0.8, -1.4, 0.9):
            self.play(a_kn.animate(run_time=0.6).move_to([x, 1.3, 0]), run_time=0.6)
        self.play(Ind(a_kn, scale_factor=1.3), run_time=0.8)
        self.at("It did not", lead=0.1)
        un = T("untouched", 26, GREY).move_to([-0.5, -1.25, 0])
        self.play(Ind(b_kn, scale_factor=1.4, color=GREY), Ind(b_lab, scale_factor=1.1, color=GREY), FadeIn(un), run_time=1.6)
        self.at("one shore", lead=0.4)
        pn = pin(GOLD, 1.3).move_to([5.0, 0.8, 0])
        pl = T("one shore", 32, TEXT).move_to([5.0, -0.5, 0])
        self.play(FadeIn(pn, shift=DOWN * 0.8), FadeIn(pl), run_time=0.9)
        tip = pn.get_bottom()
        rp = Circle(radius=0.15, stroke_color=GOLD, stroke_width=4).move_to(tip)
        self.play(rp.animate(run_time=1.2).scale(5).set_stroke(opacity=0), run_time=1.2)
        self.remove(rp)
        self.at("Even there", lead=0.2)
        self.base()
        S, M, L = Boulder(XS, SIZE_S, 71, 0.3), Boulder(XM, SIZE_M, 72, 0.62), Boulder(XL, SIZE_L, 73, 0.95)
        for b in (S, M, L):
            b.register(self)
        S.creep(0.06, 0.5)
        trs = [ValueTracker(1.8), ValueTracker(3.4), ValueTracker(1.5)]
        rows = [row_live(x, 1.0, t) for x, t in zip((XS, XM, XL), trs)]
        labs = size_labels(self)
        sch = T("schematic", 26, GREY).move_to([0, -3.35, 0])
        self.play(*[FadeOut(m) for m in (panel, a_lab, a_tr, a_kn, b_lab, b_tr, b_kn, un, pn, pl)],
                  *S.appear(), *M.appear(), *L.appear(), *[FadeIn(r) for r in rows], FadeIn(labs), FadeIn(sch), run_time=1.2)
        self.at("season", lead=0.3)
        ch = chip("season of the census", GOLD, 32).move_to([0, 3.2, 0])
        self.play(FadeIn(ch, shift=DOWN * 0.2), run_time=0.8)
        self.storm([(S, 0.12)], D=2.4, dur=1.3)
        self.at("In spring", lead=0.2)
        ch2 = chip("spring", GOLD, 32).move_to([0, 3.2, 0])
        self.play(ReplacementTransform(ch, ch2), run_time=0.8)
        self.at("large boulders", lead=0.3)
        self.play(trs[2].animate(run_time=2.4, rate_func=smooth).set_value(3.3))
        self.at("poorer", lead=0.2)
        self.play(Ind(rows[2], scale_factor=1.1), run_time=1.2)
        self.finish()


class S14Rule(Shore):
    def construct(self):
        self.base()
        S, M, L = Boulder(XS, SIZE_S, 81, 0.3), Boulder(XM, SIZE_M, 82, 0.62), Boulder(XL, SIZE_L, 83, 0.95)
        cl = [Clock(b.cx, 0.95, 0.8, b.t) for b in (S, M, L)]
        for b in (S, M, L):
            b.register(self)
        for c in cl:
            c.register(self)
        anims = []
        for b, c in zip((S, M, L), cl):
            anims += b.appear() + c.appear()
        self.play(*anims, run_time=1.0)
        # dial: frequent -> rare
        dc = np.array([0.0, 2.2, 0.0])
        dr = 0.6
        arc = Arc(radius=dr, start_angle=0, angle=PI, arc_center=dc, color=GREY, stroke_width=4)
        base = Line(dc + LEFT * dr, dc + RIGHT * dr, color=GREY, stroke_width=3)
        dv = ValueTracker(0)
        needle = always_redraw(lambda: Line(dc, dc + 0.52 * np.array([np.cos(PI * (1 - dv.get_value())), np.sin(PI * (1 - dv.get_value())), 0]),
                                           color=GOLD, stroke_width=6))
        fq = T("frequent", 28).move_to(dc + [-1.55, 0.0, 0])
        rr = T("rare", 28).move_to(dc + [1.2, 0.0, 0])
        ttl = T("how often disturbed", 30, GOLD).move_to([0, 3.35, 0])
        self.add(dv)
        self.storm([(M, 0.2)], D=1.6, dur=1.0)
        self.at("how often", lead=0.3)
        self.play(FadeIn(arc), FadeIn(base), FadeIn(needle), FadeIn(fq), FadeIn(rr), FadeIn(ttl), run_time=0.7)
        self.at("helps", lead=0.1)
        self.play(dv.animate(run_time=self.until("gets", lead=0.4), rate_func=smooth).set_value(1.0),
                  M.t.animate(run_time=self.until("gets", lead=0.4), rate_func=smooth).set_value(0.95))
        self.finish()


class S15End(EndCard):
    LINE = "How often disturbance strikes helps set how far succession gets."
