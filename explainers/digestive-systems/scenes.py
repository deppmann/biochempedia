"""Why Order Matters in a Gut (digestive systems, film 1)

COLOR MAP (whole film)
  GREY (light)  = food: large blocks, then grains
  BLUE          = water (and bile / pancreatic juice)
  GREEN         = microbes and the fermenting chamber (vat)
  GOLD          = acid, the stomach
  RED           = blood capillaries
  PALE YELLOW   = lacteal (lymph)
  ORANGE        = fat, short-chain fatty acids
  TAN           = the shaded small intestine (the absorbing stretch)
One world: a horizontal tube, mouth at left, anus at right, same coordinates in every scene.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

FOOD = "#B4BBC8"
PALE = "#F5E6A3"
ORANGE = "#F2994A"
TAN = "#B08968"
DROP = "#8C7B5A"

TY = 0.0
XM0, XM1 = -6.4, -5.0
XS1 = -3.3
XI1 = 1.7
XC1 = 6.0
XA1 = 6.6


def top_at(x):
    if x < XM1:
        return 0.55
    if x < XS1:
        return 1.95
    if x < XI1:
        return 1.33
    if x < XC1:
        return 1.55
    return 0.5


# ---------------------------------------------------------------- helpers
def L(text, x, y, color=TEXT, size=30, max_w=6.2):
    m = T(text, size, color)
    fit(m, max_w=max_w, max_h=2)
    return m.move_to([x, y, 0])


def runner(m, pts, speed, phase=0.0, fn=None, loop=True):
    """Move m along a polyline at `speed` units/s, forever (updater)."""
    pts = [np.array(p, float) for p in pts]
    seg = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
    tot = sum(seg)
    m._t = phase

    def upd(mm, dt):
        mm._t += dt
        s = (mm._t * speed) % tot if loop else max(0.0, min(mm._t * speed, tot - 1e-6))
        k = 0
        while k < len(seg) - 1 and s > seg[k]:
            s -= seg[k]
            k += 1
        f = s / seg[k] if seg[k] > 0 else 0
        pos = pts[k] + (pts[k + 1] - pts[k]) * f
        mm.move_to(pos)
        if fn:
            fn(mm, pos)
    m.add_updater(upd)
    upd(m, 0)
    return m


def setsz(m, s):
    if abs(s - m._s) > 1e-3:
        m.scale(s / m._s)
        m._s = s


def food_size(x):
    if x < XM1:
        return 0.85
    if x < XS1:
        return 0.6
    if x < XI1:
        return 0.55 - 0.40 * (x - XS1) / (XI1 - XS1)
    return 0.15


def food_block(color=FOOD):
    b = RoundedRectangle(corner_radius=0.08, width=1, height=0.8, stroke_color=TEXT, stroke_width=2,
                         fill_color=color, fill_opacity=0.85)
    b._s = 1.0
    return b


def food_runner(phase, speed=1.1, y=0.0, shrink=True):
    b = food_block()
    pts = [[XM0 + 0.2, y, 0], [XA1 + 0.2, y, 0]]
    runner(b, pts, speed, phase, fn=(lambda m, p: setsz(m, food_size(p[0]))) if shrink else None)
    return b


def dot(color=GREEN, r=0.11, op=1.0):
    d = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op)
    return d


def jitter(m, base_fn, amp=0.18, seed=0.0):
    m._t2 = seed

    def upd(mm, dt):
        mm._t2 += dt
        b = base_fn()
        mm.move_to(b + np.array([amp * np.sin(1.7 * mm._t2 + seed * 3), amp * 0.8 * np.cos(2.3 * mm._t2 + seed * 5), 0]))
    m.add_updater(upd)
    upd(m, 0)
    return m


def brk(x0, x1, y, color, txt, ty, size=28, tx=None):
    ln = VGroup(Line([x0, y, 0], [x1, y, 0]), Line([x0, y, 0], [x0, y + 0.18, 0]), Line([x1, y, 0], [x1, y + 0.18, 0]))
    if ty > y:
        for l in ln[1:]:
            l.flip(RIGHT, about_point=np.array([0, y, 0]))
    ln.set_stroke(color, 5)
    lb = L(txt, (x0 + x1) / 2 if tx is None else tx, ty, color, size)
    return VGroup(ln, lb)


def gut(plain=False):
    """The carried world. Returns dict of parts at fixed coordinates."""
    d = {}
    if plain:
        pts = [(XM0, 1.0), (XA1, 1.0), (XA1, -1.0), (XM0, -1.0)]
        d["outline"] = Polygon(*[[x, y, 0] for x, y in pts], color=GREY, stroke_width=5).round_corners(0.35)
        return d
    tp = [(XM0, 0.55), (XM1, 0.55), (XM1, 1.95), (XS1, 1.95), (XS1, 1.33), (XI1, 1.33), (XI1, 1.55), (XC1, 1.55), (XC1, 0.5), (XA1, 0.5)]
    pts = tp + [(x, -y) for x, y in reversed(tp)]
    d["outline"] = Polygon(*[[x, y, 0] for x, y in pts], color=GREY, stroke_width=5).round_corners(0.2)
    d["stom"] = Rectangle(width=XS1 - XM1, height=3.9, stroke_width=0, fill_color=GOLD, fill_opacity=0.16).move_to([(XM1 + XS1) / 2, 0, 0])
    d["si"] = Rectangle(width=XI1 - XS1, height=2.66, stroke_width=0, fill_color=TAN, fill_opacity=0.30).move_to([(XS1 + XI1) / 2, 0, 0])
    return d


def gutg(plain=False):
    d = gut(plain)
    g = VGroup(*[v for k, v in d.items() if k != "outline"], d["outline"])
    return d, g


def ripple(x0, x1, h):
    r = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=TEXT, fill_opacity=0.14)
    runner(r, [[x0, 0, 0], [x1, 0, 0]], 1.3)
    return r


# ------------------------------------------------------------- the rabbit
def rabbit():
    fillc = "#CFC8BD"
    body = Ellipse(width=5.0, height=2.9, stroke_color=TEXT, stroke_width=4, fill_color=fillc, fill_opacity=0.9).move_to([0.2, -0.3, 0])
    tail = Circle(radius=0.42, stroke_color=TEXT, stroke_width=3, fill_color="#F2EFE9", fill_opacity=1).move_to([2.8, 0.1, 0])
    foot1 = Ellipse(width=1.7, height=0.55, stroke_color=TEXT, stroke_width=3, fill_color=fillc, fill_opacity=0.95).move_to([1.4, -1.75, 0])
    foot2 = Ellipse(width=1.2, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=fillc, fill_opacity=0.95).move_to([-1.7, -1.75, 0])
    hd = Circle(radius=0.95, stroke_color=TEXT, stroke_width=4, fill_color=fillc, fill_opacity=0.95).move_to([-2.7, 0.55, 0])
    ear1 = Ellipse(width=0.6, height=2.0, stroke_color=TEXT, stroke_width=3, fill_color=fillc, fill_opacity=0.95).rotate(0.15).move_to([-2.5, 2.0, 0])
    ear2 = Ellipse(width=0.6, height=2.0, stroke_color=TEXT, stroke_width=3, fill_color=fillc, fill_opacity=0.95).rotate(-0.2).move_to([-3.1, 1.95, 0])
    eye = Dot([-3.0, 0.85, 0], radius=0.09, color=BG)
    nose = Dot([-3.62, 0.5, 0], radius=0.1, color="#E59A9A")
    head = VGroup(ear1, ear2, hd, eye, nose)
    r = VGroup(foot1, foot2, tail, body, head)
    r.head = head
    r.body = body
    return r


def nibble(r):
    r._a = 0.0
    r._tt = 0.0

    def upd(m, dt):
        m._tt += dt
        a = 0.17 * (0.5 - 0.5 * np.cos(2.6 * m._tt))
        pivot = m.body.get_left() + RIGHT * 0.12 * m.body.width
        m.head.rotate(a - m._a, about_point=pivot)
        m._a = a
    r.add_updater(upd)


def pellets(x, y, n=5):
    g = VGroup()
    for i in range(n):
        g.add(Circle(radius=0.2, stroke_width=0, fill_color=DROP, fill_opacity=1).move_to([x + 0.38 * (i % 3) - 0.3 * (i // 3), y + 0.3 * (i // 3), 0]))
    return g


# ------------------------------------------------------------- the vat
VY = 2.55


def make_vat(x, strip=False, n=9, label=None):
    box = RoundedRectangle(corner_radius=0.4, width=2.8, height=1.5, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14).move_to([x, VY, 0])
    pipe = Line([x, VY - 0.75, 0], [x, top_at(x), 0], color=GREEN, stroke_width=8)

    def pupd(p):
        bx = box.get_center()[0]
        p.become(Line([bx, VY - 0.75, 0], [bx, top_at(bx) + 0.02, 0], color=GREEN, stroke_width=8))
    pipe.add_updater(pupd)
    micro = VGroup()
    rs = np.random.RandomState(4)
    for i in range(n):
        off = np.array([rs.uniform(-1.0, 1.0), rs.uniform(-0.3, 0.3), 0])
        m = dot(GREEN, 0.12)
        jitter(m, (lambda o=off: box.get_center() + o), 0.12, seed=i * 0.7)
        micro.add(m)
    parts = {"box": box, "pipe": pipe, "micro": micro}
    if strip:
        s = Line([-1.2, 0, 0], [1.2, 0, 0], color=RED, stroke_width=9)
        s.add_updater(lambda m: m.move_to(box.get_center() + UP * 0.92))
        s.move_to(box.get_center() + UP * 0.92)
        parts["strip"] = s
    return parts


def rel_dots(box, n, color, speed=0.45, y0=-0.2, y1=0.78, spread=0.5):
    g = VGroup()
    for i in range(n):
        d = dot(color, 0.11)
        d._t = i * 0.8
        ox = -spread + 2 * spread * i / max(n - 1, 1)

        def upd(m, dt, ox=ox):
            m._t += dt
            f = (m._t * speed) % 1.0
            m.move_to(box.get_center() + np.array([ox, y0 + f * (y1 - y0), 0]))
        d.add_updater(upd)
        upd(d, 0)
        g.add(d)
    return g


def vat_group(p):
    return VGroup(*p.values())


def qcard():
    t = T("Where does that protein go?", 38, GOLD)
    card = RoundedRectangle(corner_radius=0.2, width=t.width + 0.8, height=t.height + 0.6, stroke_color=GOLD, stroke_width=4,
                            fill_color=BG, fill_opacity=0.95)
    t.move_to(card)
    return VGroup(card, t).move_to([0.5, -2.75, 0])


def caption(txt):
    return T(txt, 46, TEXT, weight=BOLD).move_to([-5.3, -3.2, 0])


# =========================================================== scenes
class S00Title(TitleCard):
    LESSON = "Digestive Systems and Nutrition"
    TITLE = "Why Order Matters in a Gut"


class S01Hook(SpokenScene):
    def construct(self):
        r = rabbit()
        r.shift(LEFT * 0.2 + DOWN * 0.1)
        pl = pellets(-5.4, -2.0, 5)
        self.play(FadeIn(r, shift=UP * 0.3), FadeIn(pl), run_time=1.0)
        nibble(r)
        self.add(r)
        self.at("droppings")
        # the head dips and a pellet goes to the mouth
        self.play(pl[0].animate.move_to([-4.3, -0.5, 0]), run_time=0.7)
        self.wait(0.3)
        q = T("?", 120, GOLD, weight=BOLD).move_to([-5.2, 2.5, 0])
        self.at("Why would an animal")
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        q._t = 0.0

        def qup(m, dt):
            m._t += dt
            m.set_opacity(0.75 + 0.25 * np.sin(3.5 * m._t))
        q.add_updater(qup)
        self.add(q)
        self.wait(self.t_of("The answer lies") - 0.2 - self.elapsed())
        d, g = gutg(plain=True)
        self.play(FadeOut(q), r.animate.set_opacity(0.16), FadeOut(pl), run_time=0.8)
        self.at("shape of the gut")
        self.play(Create(d["outline"]), run_time=2.0)
        self.play(FadeOut(r), run_time=0.6)
        self.finish()


class S02Tube(SpokenScene):
    def construct(self):
        d, g = gutg(plain=True)
        self.add(g)
        rp = ripple(XM0 + 0.3, XA1 - 0.3, 1.8)
        self.add(rp)
        self.at("complete gut")
        self.play(g.animate.set_stroke(TEXT, 6), run_time=0.8)
        self.at("tube")
        self.play(g.animate.set_stroke(GREY, 5), run_time=0.5)
        self.at("mouth")
        lm = L("mouth", XM0 + 0.5, 1.75, TEXT, 34)
        self.play(FadeIn(lm, shift=DOWN * 0.2), run_time=0.6)
        self.at("anus")
        la = L("anus", XA1 - 0.4, 1.75, TEXT, 34)
        self.play(FadeIn(la, shift=DOWN * 0.2), run_time=0.6)
        self.at("Food moves")
        b = food_block()
        setsz(b, 0.85)
        runner(b, [[XM0 + 0.4, 0, 0], [XA1 - 0.3, 0, 0]], 1.5, 0, loop=False)
        self.add(b)
        arrow = Arrow([-3.0, -1.9, 0], [3.0, -1.9, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.4)
        lw = L("one way", 0, -2.7, TEXT, 38)
        self.play(GrowArrow(arrow), FadeIn(lw), run_time=1.2)
        self.finish()


class S03Stations(SpokenScene):
    def construct(self):
        dp, gp = gutg(plain=True)
        d, g = gutg()
        self.add(gp)
        self.play(ReplacementTransform(gp, g), run_time=1.6)
        # food moving through, shrinking as it goes
        foods = [food_runner(ph, 0.95) for ph in (0.0, 2.4, 4.8, 7.2)]
        for b in foods:
            self.add(b)
        self.at("The mouth")
        lm = L("mouth", -5.7, -1.0, TEXT, 30)
        self.play(FadeIn(lm), run_time=0.4)
        self.at("stomach")
        ls = L("stomach", -4.4, -2.5, GOLD, 30)
        self.play(FadeIn(ls), run_time=0.4)
        # gold acid droplets swirl in the stomach
        acid = VGroup()
        for i in range(7):
            a = dot(GOLD, 0.1)
            a._t = i * 0.9
            runner(a, [[-4.5, -1.4, 0], [-3.8, -1.4, 0], [-3.8, 1.4, 0], [-4.5, 1.4, 0]], 1.6, i * 0.9)
            acid.add(a)
        self.add(acid)
        self.at("duodenum")
        ld = brk(XS1, -1.2, -1.75, TAN, "duodenum", -2.3, 30, tx=-1.7)
        self.play(Create(ld[0]), FadeIn(ld[1]), run_time=0.7)
        self.at("small intestine")
        lsi = brk(XS1, XI1, -3.0, TAN, "small intestine", -3.55, 30)
        self.play(Create(lsi[0]), FadeIn(lsi[1]), run_time=0.9)
        self.at("bile")
        bp = Line([-2.7, 2.9, 0], [-2.7, 1.3, 0], color=BLUE, stroke_width=9)
        lb = L("bile", -2.7, 3.35, BLUE, 30)
        self.play(Create(bp), FadeIn(lb), run_time=0.6)
        self.at("pancreatic")
        pp = Line([-1.2, 2.9, 0], [-1.2, 1.3, 0], color=BLUE, stroke_width=9)
        lp = L("pancreatic juice", -0.3, 3.35, BLUE, 30)
        self.play(Create(pp), FadeIn(lp), run_time=0.6)
        drops = VGroup()
        for i, x in enumerate((-2.7, -1.2)):
            for k in range(3):
                dd = dot(BLUE, 0.1)
                runner(dd, [[x, 2.8, 0], [x, 0.5, 0]], 1.4, k * 0.55 + i * 0.2)
                drops.add(dd)
        self.add(drops)
        self.finish()


class S04Absorb(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        foods = [food_runner(ph, 0.9) for ph in (0.0, 3.0, 6.0, 9.0)]
        for b in foods:
            self.add(b)
        lsi = brk(XS1, XI1, -3.0, TAN, "small intestine", -3.55, 30)
        self.at("small intestine")
        self.play(d["si"].animate.set_fill(TAN, 0.55), Create(lsi[0]), FadeIn(lsi[1]), run_time=1.0)
        self.at("main absorbing")
        new = brk(XS1, XI1, -3.0, TAN, "main absorbing stretch", -3.55, 30)
        self.play(Transform(lsi, new), run_time=0.8)
        self.at("Enzymes")
        # big blocks entering the small intestine break into grains
        for k, x in enumerate((-2.9, -1.6, -0.3)):
            blk = food_block()
            setsz(blk, 0.55)
            blk.move_to([x, 0, 0])
            self.add(blk)
            grains = VGroup(*[dot(FOOD, 0.11).move_to([x + 0.17 * (j % 2) - 0.08, 0.17 * (j // 2) - 0.09, 0]) for j in range(4)])
            self.wait(0.3)
            self.play(ReplacementTransform(blk, grains), run_time=0.6)
            for j, gr in enumerate(grains):
                runner(gr, [gr.get_center(), [XI1, gr.get_center()[1], 0]], 0.6, 0, loop=False)
            self.wait(0.1)
        self.at("Transporters")
        gates = VGroup()
        gx = [-2.6, -1.5, -0.4, 0.7]
        for x in gx:
            gates.add(VGroup(Line([x - 0.3, -1.33, 0], [x - 0.08, -1.33, 0]), Line([x + 0.08, -1.33, 0], [x + 0.3, -1.33, 0])).set_stroke(TEXT, 8))
        lt = L("transporters", -0.9, -2.3, TEXT, 30)
        self.play(Create(gates), FadeIn(lt), run_time=0.9)
        self.at("carry")
        gr = VGroup(*[dot(FOOD, 0.13).move_to([x, -0.7, 0]) for x in gx])
        self.add(gr)
        self.play(*[g_[0].animate.shift(LEFT * 0.12) for g_ in gates], *[g_[1].animate.shift(RIGHT * 0.12) for g_ in gates], run_time=0.5)
        self.play(*[m.animate.move_to([m.get_center()[0], -1.8, 0]) for m in gr], run_time=1.6)
        self.play(*[FadeOut(m) for m in gr], run_time=0.4)
        self.finish()


class S05Villus(SpokenScene):
    def construct(self):
        wall = RoundedRectangle(corner_radius=0.9, width=3.8, height=6.4, stroke_color=TAN, stroke_width=6, fill_color=TAN, fill_opacity=0.18).move_to([1.8, -0.2, 0])
        lac = RoundedRectangle(corner_radius=0.3, width=0.8, height=4.8, stroke_color=PALE, stroke_width=5, fill_color=PALE, fill_opacity=0.25).move_to([2.6, 0.0, 0])
        cap = Ellipse(width=0.9, height=3.0, stroke_color=RED, stroke_width=9, fill_opacity=0).move_to([0.9, 1.4, 0])
        self.play(FadeIn(wall, scale=0.7), Create(cap), Create(lac), run_time=1.1)
        l1 = L("simple sugars", -4.4, 2.4, TEXT, 32)
        l2 = L("amino acids", -4.4, 1.4, TEXT, 32)
        gr = VGroup(*[dot(FOOD, 0.14).move_to([-3.0, 1.8 + 0.35 * (i - 1), 0]) for i in range(3)])
        self.play(FadeIn(l1), FadeIn(gr), run_time=0.4)
        self.at("amino")
        self.play(FadeIn(l2), run_time=0.4)
        self.at("cross into")
        self.play(*[Succession(Wait(0.2 * i), m.animate(run_time=1.1, rate_func=linear).move_to([0.9, 1.4 + 0.3 * (i - 1), 0])) for i, m in enumerate(gr)])
        for i, m in enumerate(gr):
            runner(m, [[0.9, 2.7, 0], [0.9, 0.1, 0]], 0.9, i * 1.0)
        self.at("capillaries")
        lc = L("blood capillary", -4.4, 0.4, RED, 32)
        self.play(FadeIn(lc), run_time=0.4)
        self.at("Most fat")
        lf = L("fat", -4.4, -1.2, ORANGE, 32)
        fat = VGroup(*[dot(ORANGE, 0.14).move_to([-3.0, -1.7 + 0.3 * (i - 1), 0]) for i in range(3)])
        self.play(FadeIn(lf), FadeIn(fat), run_time=0.4)
        self.at("packed")
        self.play(*[m.animate.move_to([0.4 + 0.18 * i, -1.7 + 0.15 * (i % 2), 0]) for i, m in enumerate(fat)], run_time=0.7)
        chy = Circle(radius=0.32, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.4).move_to([0.5, -1.65, 0])
        self.play(ReplacementTransform(fat, chy), run_time=0.5)
        self.at("particles")
        lch = L("chylomicrons", -4.4, -2.4, ORANGE, 32)
        self.play(FadeIn(lch), run_time=0.4)
        self.at("enter")
        ll = L("lacteal", 5.0, 1.0, PALE, 34)
        self.play(chy.animate.move_to([2.6, -1.0, 0]), FadeIn(ll), run_time=1.0)
        self.play(chy.animate.move_to([2.6, 1.2, 0]), run_time=2.2)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        foods = [food_runner(ph, 0.9) for ph in (0.0, 3.0, 6.0, 9.0)]
        for b in foods:
            self.add(b)
        self.at("Large food")
        t1 = L("broken down before or within", 0, 3.55, TEXT, 34, max_w=12)
        t2 = L("the stretch that can absorb them", 0, 3.05, TEXT, 34, max_w=12)
        self.play(FadeIn(t1, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(t2, shift=DOWN * 0.15), run_time=0.8)
        self.at("broken down")
        b1 = brk(XM0, XI1, -2.4, ORANGE, "break down", -3.0, 34, tx=-2.4)
        self.play(Create(b1[0]), FadeIn(b1[1]), run_time=1.0)
        self.at("absorb")
        b2 = brk(XS1, XI1, 1.8, TAN, "absorb", 2.35, 34)
        self.play(d["si"].animate.set_fill(TAN, 0.55), Create(b2[0]), FadeIn(b2[1]), run_time=1.0)
        self.finish()


def water_poly(xmax, wfun, x0=XM0 + 0.05):
    xs = np.linspace(x0, max(xmax, x0 + 0.02), 90)
    up = [[x, 1.35 * wfun(x) / 2, 0] for x in xs]
    dn = [[x, -1.35 * wfun(x) / 2, 0] for x in reversed(xs)]
    return Polygon(*(up + dn), stroke_width=0, fill_color=BLUE, fill_opacity=0.75)


def wfun_si(x):
    """schematic width of the water stream (not to scale)"""
    if x < XM1:
        return 0.35 + 0.25 * (x - XM0) / (XM1 - XM0)
    if x < XS1:
        return 0.6 + 0.9 * (x - XM1) / (XS1 - XM1)
    if x < -1.5:
        return 1.5 + 0.2 * (x - XS1) / (-1.5 - XS1)
    if x < XI1:
        f = (x + 1.5) / (XI1 + 1.5)
        return 1.7 - 1.2 * f ** 0.7
    if x < XC1:
        f = (x - XI1) / (XC1 - XI1)
        return 0.5 - 0.42 * f
    return 0.08


class S07Water(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        foods = [food_runner(ph, 0.9) for ph in (0.0, 3.0, 6.0, 9.0)]
        for b in foods:
            self.add(b)
        self.at("Whatever")
        eq = L("water leaving = came in + added − absorbed", 0, 3.45, TEXT, 34, max_w=12.4)
        self.play(FadeIn(eq, shift=DOWN * 0.15), run_time=1.0)
        self.at("Watch the water")
        pipes = VGroup(*[Line([x, 3.0, 0], [x, top_at(x) - 0.05, 0], color=BLUE, stroke_width=8) for x in (-5.7, -4.2, -2.7)])
        lj = L("the gut adds juices", 0.6, 2.7, BLUE, 30, max_w=6)
        self.play(Create(pipes), FadeIn(lj), run_time=0.7)
        tr = ValueTracker(XM0 + 0.1)
        w = water_poly(tr.get_value(), wfun_si)
        w.add_updater(lambda m: m.become(water_poly(tr.get_value(), wfun_si)))
        self.add(w)
        self.play(tr.animate.set_value(-1.5), run_time=1.5, rate_func=linear)
        self.at("small intestine")
        self.play(FadeOut(lj), run_time=0.3)
        self.play(tr.animate.set_value(XI1), run_time=2.4, rate_func=linear)
        self.finish()


class S08Leftover(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        foods = [food_runner(ph, 0.9) for ph in (0.0, 3.0, 6.0, 9.0)]
        for b in foods:
            self.add(b)
        tr = ValueTracker(XI1)
        w = water_poly(tr.get_value(), wfun_si)
        w.add_updater(lambda m: m.become(water_poly(tr.get_value(), wfun_si)))
        self.add(w)
        lc = L("colon", 4.0, 2.2, TEXT, 34)
        self.at("colon")
        self.play(FadeIn(lc), run_time=0.4)
        self.play(tr.animate.set_value(XA1 + 0.1), run_time=2.6, rate_func=linear)
        self.at("small leftover")
        ll = L("small leftover", 4.4, -2.3, BLUE, 34)
        self.play(FadeIn(ll), run_time=0.5)
        self.at("feces")
        lf = dot(DROP, 0.14).move_to([XA1 - 0.15, 0, 0])
        self.play(lf.animate.move_to([XA1 - 0.1, -3.0, 0]), run_time=1.2)
        self.finish()


def grass_blade():
    b = VGroup(Line([0, -0.35, 0], [0, 0.35, 0]), Line([-0.14, -0.3, 0], [-0.04, 0.2, 0]), Line([0.14, -0.3, 0], [0.04, 0.2, 0]))
    b.set_stroke(FOOD, 5)
    return b


class S09Grass(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        blades = [grass_blade() for _ in range(4)]
        for i, b in enumerate(blades):
            runner(b, [[XM0 + 0.2, 0, 0], [XA1 + 0.2, 0, 0]], 0.95, i * 3.2)
            self.add(b)
        self.at("tube grass")
        # blades keep running through the whole gut
        self.at("cellulose")
        lc = L("cellulose", -0.6, 2.9, FOOD, 36)
        self.play(FadeIn(lc), run_time=0.5)
        self.at("no vertebrate")
        lu = L("passes the small intestine unbroken", -0.6, -2.9, TEXT, 30, max_w=9)
        self.play(FadeIn(lu), run_time=0.8)
        self.at("Microbes do")
        self.play(FadeOut(lc), FadeOut(lu), run_time=0.3)
        vp = make_vat(3.6)
        self.play(FadeIn(vp["box"], scale=0.8), Create(vp["pipe"]), run_time=0.7)
        self.add(vp["pipe"])
        self.play(FadeIn(vp["micro"]), run_time=0.4)
        self.at("fermenting")
        lf = L("ferment the fiber, no oxygen", -2.4, 2.9, GREEN, 32, max_w=7)
        self.play(FadeIn(lf), run_time=0.6)
        self.finish()


class S10Acids(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        foods = [food_runner(ph, 0.9, shrink=False) for ph in (0.0, 5.0)]
        for b in foods:
            self.add(b)
        vp = make_vat(3.6, strip=True)
        for v in vp.values():
            self.add(v)
        self.at("short")
        lab = L("short-chain fatty acids", -3.0, 2.95, ORANGE, 32, max_w=6)
        self.play(FadeIn(lab), run_time=0.6)
        sc = rel_dots(vp["box"], 6, ORANGE, 0.35, -0.2, 0.78, 0.9)
        self.add(sc)
        self.at("wall")
        la = L("absorbed where made", -3.0, 2.95, RED, 32, max_w=6)
        self.play(FadeOut(lab), run_time=0.3)
        self.play(FadeIn(la), run_time=0.5)
        self.at("wherever")
        self.play(FadeOut(la), vp["box"].animate.move_to([-2.4, VY, 0]), run_time=1.6)
        self.play(vp["box"].animate.move_to([3.6, VY, 0]), run_time=1.8)
        self.finish()


class S11Protein(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(3.6)
        for v in vp.values():
            self.add(v)
        # microbes keep drifting along the gut
        flow = VGroup()
        for i in range(5):
            m = dot(GREEN, 0.11)
            runner(m, [[XM0 + 0.2, 0, 0], [XA1 + 0.2, 0, 0]], 1.0, i * 2.6)
            flow.add(m)
        self.add(flow)
        self.at("the microbes")
        self.play(*[Indicate(m, color=GREEN, scale_factor=1.5) for m in list(vp["micro"])[:4]], run_time=1.0)
        self.at("rich")
        glow = RoundedRectangle(corner_radius=0.5, width=3.3, height=1.95, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22).move_to(vp["box"])
        glow.add_updater(lambda m: m.move_to(vp["box"]))
        tag = L("protein", 6.1, 2.55, GREEN, 30)
        self.play(FadeIn(glow), FadeIn(tag), run_time=0.8)
        self.at("acid stomach")
        self.play(d["stom"].animate.set_fill(GOLD, 0.6), run_time=0.8)
        self.at("starts digesting")
        l1 = L("starts protein digestion", -4.0, -2.5, GOLD, 30, max_w=6.2)
        self.play(FadeIn(l1), run_time=0.6)
        self.at("small intestine")
        self.play(d["stom"].animate.set_fill(GOLD, 0.2), d["si"].animate.set_fill(TAN, 0.65), run_time=0.8)
        self.at("finishes")
        l2 = L("finishes it, absorbs amino acids", -0.2, -3.25, TAN, 30, max_w=7)
        self.play(FadeIn(l2), run_time=0.6)
        self.finish()


class S12Cow(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(3.6)
        for v in vp.values():
            self.add(v)
        cap = caption("cow")
        self.add(cap)
        self.at("ferments")
        self.play(vp["box"].animate.move_to([-5.2, VY, 0]), run_time=2.4)
        self.at("microbes wash")
        # microbes flow from the vat into the acid
        flow = VGroup()
        for i in range(6):
            m = dot(GREEN, 0.12)
            runner(m, [[-5.2, 1.9, 0], [-5.2, 0.55, 0], [-4.5, 0.0, 0], [-4.0, 0.0, 0]], 1.0, i * 0.8, loop=True)
            flow.add(m)
        self.add(flow)
        self.at("into the acid")
        # then through the acid and the small intestine as small grains
        grains = VGroup()
        for i in range(8):
            m = dot(GREEN, 0.07)
            runner(m, [[-4.5, 0.2, 0], [-3.3, 0.2, 0], [1.7, 0.2, 0]], 1.0, i * 0.9)
            grains.add(m)
        self.add(grains)
        self.at("small intestine")
        cap_s = Line([XS1 + 0.2, -1.55, 0], [XI1 - 0.2, -1.55, 0], color=RED, stroke_width=9)
        lr = L("capillaries", -0.8, -2.1, RED, 30)
        self.play(Create(cap_s), FadeIn(lr), run_time=0.8)
        self.at("There they")
        self.finish()


class S13Horse(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(-5.2)
        for v in vp.values():
            self.add(v)
        cap = caption("horse")
        self.add(cap)
        self.at("ferments")
        self.play(vp["box"].animate.move_to([3.6, VY, 0]), run_time=3.4)
        self.at("small intestine")
        lc = L("cecum and colon", -0.5, 2.55, GREEN, 30, max_w=4)
        self.play(FadeIn(lc), run_time=0.5)
        self.at("Its microbes")
        more = VGroup(*[dot(GREEN, 0.12) for _ in range(8)])
        rs = np.random.RandomState(9)
        for i, m in enumerate(more):
            off = np.array([rs.uniform(-1.0, 1.0), rs.uniform(-0.45, 0.45), 0])
            jitter(m, (lambda o=off: vp["box"].get_center() + o), 0.12, seed=i * 0.5 + 3)
        self.play(FadeIn(more, scale=0.4), run_time=1.0)
        self.at("protein")
        tag = L("protein", 6.1, 2.55, GREEN, 30)
        self.play(FadeIn(tag), run_time=0.5)
        self.at("small intestine", nth=1)
        self.play(d["si"].animate.set_fill(TAN, 0.6), run_time=0.8)
        ls = L("already behind", -0.6, -1.85, TAN, 32)
        self.play(FadeIn(ls), run_time=0.5)
        self.at("Where does")
        self.play(FadeOut(ls), d["si"].animate.set_fill(TAN, 0.3), run_time=0.4)
        q = qcard()
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S14Pause(NarratedScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(3.6)
        for v in vp.values():
            self.add(v)
        more = VGroup(*[dot(GREEN, 0.12) for _ in range(8)])
        rs = np.random.RandomState(9)
        for i, m in enumerate(more):
            off = np.array([rs.uniform(-1.0, 1.0), rs.uniform(-0.45, 0.45), 0])
            jitter(m, (lambda o=off: vp["box"].get_center() + o), 0.12, seed=i * 0.5 + 3)
        self.add(more)
        self.add(caption("horse"))
        self.add(qcard())
        tr = ValueTracker(0)
        ring = Circle(radius=0.4, color=GREY, stroke_width=5).move_to([6.1, -3.2, 0])
        arc = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001), color=GOLD, stroke_width=8).move_to(ring))
        self.add(ring, arc)
        self.play(tr.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S15Reveal(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(3.6, strip=True)
        for v in vp.values():
            self.add(v)
        more = VGroup(*[dot(GREEN, 0.12) for _ in range(8)])
        rs = np.random.RandomState(9)
        for i, m in enumerate(more):
            off = np.array([rs.uniform(-1.0, 1.0), rs.uniform(-0.45, 0.45), 0])
            jitter(m, (lambda o=off: vp["box"].get_center() + o), 0.12, seed=i * 0.5 + 3)
        self.add(more)
        self.add(caption("horse"))
        # most microbes flow down the pipe and out the anus
        out = VGroup()
        for i in range(9):
            m = dot(GREEN, 0.12)
            runner(m, [[3.6, 1.85, 0], [3.6, 0.0, 0], [XA1 + 0.1, 0.0, 0]], 1.5, i * 0.45)
            out.add(m)
        self.add(out)
        self.at("Most of it")
        lm = L("most microbial protein lost", 0.4, -3.25, GREEN, 34, max_w=9)
        self.play(FadeIn(lm), run_time=0.7)
        sc = rel_dots(vp["box"], 4, ORANGE, 0.5, -0.1, 0.78, 0.6)
        self.add(sc)
        self.at("The stretch")
        ar = Arrow([1.2, -1.9, 0], [-1.6, -1.9, 0], buff=0, color=TAN, stroke_width=8, tip_length=0.35)
        lb = L("already behind", -0.2, -2.45, TAN, 30)
        self.play(d["si"].animate.set_fill(TAN, 0.6), GrowArrow(ar), run_time=1.0)
        self.add(lb)
        self.play(FadeIn(lb), run_time=0.4)
        self.finish()


class S16Rabbit(SpokenScene):
    def construct(self):
        d, g = gutg()
        self.add(g)
        vp = make_vat(3.6)
        for v in vp.values():
            self.add(v)
        cap = caption("rabbit")
        self.add(cap)
        # slow trickle of microbes into the colon
        out = VGroup()
        for i in range(4):
            m = dot(GREEN, 0.1)
            runner(m, [[3.6, 1.9, 0], [3.6, 0.0, 0], [4.8, 0.0, 0]], 1.3, i * 0.9)
            out.add(m)
        self.add(out)
        self.at("after the small")
        lc = L("cecum", 1.0, 2.55, GREEN, 30)
        self.play(FadeIn(lc), run_time=0.5)
        self.at("soft pellets")
        route = [[3.3, 0.0, 0], [6.7, 0.0, 0], [6.7, -2.4, 0], [-6.2, -2.4, 0], [-6.2, 0.0, 0], [-5.6, 0.0, 0], [-3.3, 0.0, 0], [XI1, 0.0, 0]]
        pel = VGroup(*[Circle(radius=0.22, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.55) for _ in range(3)])
        for i, m in enumerate(pel):
            m._s = 1.0
            runner(m, route, 3.6, -0.9 * i, fn=lambda mm, p: setsz(mm, 0.45 if p[0] > XS1 and p[1] > -1 else 1.0), loop=False)
        self.play(FadeIn(pel, scale=0.5), run_time=0.8)
        self.add(pel)
        self.at("eats them")
        arc = VMobject().set_points_as_corners([[6.7, -0.6, 0], [6.7, -2.4, 0], [-6.2, -2.4, 0], [-6.2, -0.65, 0]]).set_stroke(GREEN, 7)
        tip = Triangle(fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.2).move_to([-6.2, -0.6, 0])
        self.play(Create(arc), FadeIn(tip), run_time=1.6)
        self.at("through the stomach")
        cap_s = Line([XS1 + 0.2, -1.55, 0], [XI1 - 0.2, -1.55, 0], color=RED, stroke_width=9)
        self.play(Create(cap_s), run_time=0.6)
        self.at("small intestine", nth=1)
        gr = VGroup(*[dot(GREEN, 0.08).move_to([-2.4 + 1.0 * i, -0.5, 0]) for i in range(4)])
        self.add(gr)
        self.play(*[m.animate.move_to([m.get_center()[0], -1.5, 0]) for m in gr], run_time=1.2)
        self.finish()


class S17Answer(SpokenScene):
    def construct(self):
        r = rabbit()
        r.shift(LEFT * 0.2 + DOWN * 0.1)
        pl = pellets(-5.4, -2.0, 4)
        tk0 = pl[0].copy().move_to([-4.3, -0.5, 0])
        self.add(r)
        self.add(pl)
        nibble(r)
        q = T("?", 120, GOLD, weight=BOLD).move_to([-5.2, 2.5, 0])
        self.add(q)
        self.at("droppings")
        tick = T("✓", 120, GREEN, weight=BOLD).move_to([-5.2, 2.5, 0])
        self.play(ReplacementTransform(q, tick), run_time=0.6)
        self.wait(0.4)
        self.at("Food must")
        small = VGroup(r, pl, tick)
        r.clear_updaters()
        self.play(small.animate.scale(0.3).move_to([5.3, 2.7, 0]), run_time=1.0)
        rows = [("cow", 2.5, "before", "microbes digested"), ("horse", 0.2, "after", "protein lost"), ("rabbit", -2.1, "after", "pellets loop back")]
        ridx = {"before": 0, "after": 1}
        groups = VGroup()
        for name, y, where, note in rows:
            nm = T(name, 34, TEXT, weight=BOLD).move_to([-5.6, y, 0])
            tube = Rectangle(width=4.6, height=0.7, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to([-2.3, y, 0])
            stom = Rectangle(width=0.8, height=0.9, stroke_width=0, fill_color=GOLD, fill_opacity=0.5).move_to([-4.2, y, 0])
            si = Rectangle(width=1.8, height=0.7, stroke_width=0, fill_color=TAN, fill_opacity=0.5).move_to([-3.2, y, 0])
            vx = -4.55 if where == "before" else -1.0
            vy = y + (0.0 if where == "before" else 0.95)
            vt = Circle(radius=0.38, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.3).move_to([vx, vy, 0])
            nt = T(note, 30, TEXT if True else GREY).move_to([0.5, y, 0]).align_to([0.5, y, 0], LEFT)
            grp = VGroup(nm, tube, stom, si, vt, nt)
            groups.add(grp)
        # build rows one at a time with the narration
        for i, gp in enumerate(groups):
            self.play(FadeIn(gp, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(0.8)
        loop = VMobject().set_points_as_corners([[0.0, -2.5, 0], [0.0, -3.3, 0], [-4.6, -3.3, 0], [-4.6, -2.5, 0]]).set_stroke(GREEN, 5)
        self.play(Create(loop), run_time=0.8)
        self.finish()


class S18End(EndCard):
    LINE = "Break food down before or within the stretch that can absorb it."
