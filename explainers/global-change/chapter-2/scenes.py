"""Two Forests, One Bird (global-change, film 2 of 2)

Same colour map as film 1:
  GOLD   = what the species needs (here: the caterpillar food peak)
  GREEN  = the species (here: the nestlings in the nest)
  RED    = the gap (trophic mismatch)
  ORANGE = warming
  COOL   = cool
  TEXT   = labels
World: a spring calendar strip, March to July, 0.08 screen units per day (schematic).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
COOL = "#58C4DD"
BROWN = "#8B5A2B"
TREE = "#4E8F3A"
EGGC = "#F3E9D2"
PINK = "#E58FB5"
BIRDC = "#9FB7D8"

# ---------------------------------------------------------------- shared helpers
AX0, DAY = -6.0, 0.08
AY, HB, SIG = -0.9, 2.5, 9.0
BAR_Y, BR_Y = -2.05, -2.75
RX = 3.9
MONTHS = [(15, "Mar"), (46, "Apr"), (76, "May"), (107, "Jun"), (137, "Jul")]
TICKS = [0, 31, 61, 92, 122, 150]


def dx(d): return AX0 + DAY * d
def lerpc(a, b, t): return interpolate_color(ManimColor(a), ManimColor(b), float(min(1, max(0, t))))


def bob(m, amp=0.06, sp=2.0, ph=0.0):
    """A slow bob so a held object is never frozen."""
    m.b0 = m.get_center().copy()
    m.bt = ph

    def up(mm, dt):
        mm.bt += dt
        mm.move_to(mm.b0 + np.array([0, amp * np.sin(sp * mm.bt), 0]))
    m.add_updater(up)
    return m


def lab(text, size=30, color=TEXT, w=4.0, **kw):
    t = T(text, size, color, **kw)
    if t.width > w:
        t.scale(w / t.width)
    return t


def egg(x, y, s=1.0):
    return Ellipse(width=0.3 * s, height=0.4 * s).set_fill(EGGC, 1).set_stroke(TEXT, 1.5).move_to([x, y, 0])


def leaf(x, y, s=1.0):
    e = Ellipse(width=0.3 * s, height=0.55 * s).set_fill(TREE, 1).set_stroke(TREE, 2).rotate(0.6).move_to([x, y, 0])
    st = Line([x - 0.14 * s, y - 0.2 * s, 0], [x + 0.14 * s, y + 0.2 * s, 0], color=BG, stroke_width=2)
    return VGroup(e, st)


def flower(x, y, s=1.0):
    g = VGroup()
    for k in range(5):
        a = k * TAU / 5
        g.add(Circle(radius=0.1 * s).set_fill(PINK, 1).set_stroke(width=0).move_to([x + 0.15 * s * np.cos(a), y + 0.15 * s * np.sin(a), 0]))
    g.add(Circle(radius=0.08 * s).set_fill("#FFE8A3", 1).set_stroke(width=0).move_to([x, y, 0]))
    return g


def bird(x, y, s=1.0, color=BIRDC, flip=False):
    body = Ellipse(width=0.8 * s, height=0.5 * s).set_fill(color, 1).set_stroke(BG, 1.5)
    head = Circle(radius=0.2 * s).set_fill(color, 1).set_stroke(BG, 1.5).move_to([0.38 * s, 0.17 * s, 0])
    beak = Polygon([0.55 * s, 0.2 * s, 0], [0.8 * s, 0.14 * s, 0], [0.55 * s, 0.1 * s, 0]).set_fill(ORANGE, 1).set_stroke(width=0)
    wing = Ellipse(width=0.4 * s, height=0.22 * s).set_fill(BG, 0.35).set_stroke(width=0).move_to([-0.05 * s, 0, 0])
    tail = Polygon([-0.35 * s, 0.05 * s, 0], [-0.7 * s, 0.2 * s, 0], [-0.7 * s, -0.08 * s, 0]).set_fill(color, 1).set_stroke(BG, 1.5)
    eye = Dot([0.43 * s, 0.2 * s, 0], radius=0.03 * s, color=BG)
    g = VGroup(tail, body, wing, head, beak, eye)
    if flip:
        g.flip(UP)
    return g.move_to([x, y, 0])


def caterpillar(x, y, s=1.0):
    g = VGroup()
    for i in range(5):
        g.add(Circle(radius=0.12 * s).set_fill(GOLD, 1).set_stroke(BG, 1.5).move_to([x - i * 0.17 * s, y + 0.03 * s * (i % 2), 0]))
    g.add(Circle(radius=0.14 * s).set_fill(GOLD, 1).set_stroke(BG, 1.5).move_to([x + 0.17 * s, y, 0]))
    return g


def thermo(x, y, h, level, color):
    """Thermometer, total height h, fill level 0..1."""
    w = 0.3
    outline = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_fill(BG, 1).set_stroke(TEXT, 3).move_to([x, y, 0])
    bulb = Circle(radius=0.26).set_fill(color, 1).set_stroke(TEXT, 3).move_to([x, y - h / 2 - 0.1, 0])
    fh = max(0.02, (h - 0.2) * level)
    fill = Rectangle(width=0.14, height=fh).set_fill(color, 1).set_stroke(width=0).move_to([x, y - h / 2 + 0.1 + fh / 2, 0])
    return VGroup(outline, bulb, fill)


def tree(x, y, s=0.5):
    return VGroup(Line([x, y - 0.15 * s, 0], [x, y + 0.25 * s, 0], color=BROWN, stroke_width=4),
                  Polygon([x - 0.35 * s, y + 0.2 * s, 0], [x, y + 1.0 * s, 0], [x + 0.35 * s, y + 0.2 * s, 0]).set_fill(TREE, 0.9).set_stroke(TREE, 2))


# ---------------------------------------------------------------- the calendar world
DEFAULT = dict(gc=75.0, bc=75.0, tint=0.0, Ag=0.0, Ab=0.0, Ar=0.0, Aax=1.0, glow=0.0, glowb=0.0, glowr=0.0, dim=1.0, mo=1.0)


def cal_build(p):
    g = VGroup()
    bd = RoundedRectangle(corner_radius=0.2, width=12.6, height=5.7).set_fill(TEXT, 0.09).set_stroke(TEXT, 2, opacity=0.3).move_to([0, -0.9, 0])
    g.add(bd)
    if p["tint"] > 0.01:
        g.add(RoundedRectangle(corner_radius=0.2, width=12.6, height=5.7).set_fill(ORANGE, 0.22 * p["tint"]).set_stroke(width=0).move_to([0, -0.9, 0]))
    if p["Aax"] > 0.01:
        a = p["Aax"]
        g.add(Line([AX0 + 0.1, AY, 0], [dx(150), AY, 0], color=TEXT, stroke_width=4, stroke_opacity=a))
        for d in TICKS:
            g.add(Line([dx(d), AY, 0], [dx(d), AY - 0.14, 0], color=TEXT, stroke_width=3, stroke_opacity=a))
        for d, s in MONTHS:
            g.add(T(s, 24, TEXT).set_opacity(a).move_to([dx(d), AY - 0.4, 0]))
    gc, bc = p["gc"], p["bc"]
    if p["Ag"] > 0.01:
        n = 70
        ds = np.linspace(gc - 3.2 * SIG, gc + 3.2 * SIG, n)
        pts = [[dx(d), AY + HB * (1 + 0.05 * np.sin(1.5 * p["tm"])) * np.exp(-((d - gc) ** 2) / (2 * SIG ** 2)), 0] for d in ds]
        k = max(3, int(n * min(1, p["Ag"])))
        pts = pts[:k]
        sh = 0.5 + 0.5 * np.sin(2.2 * p["tm"])
        if k >= 3:
            fillp = Polygon(*pts, [pts[-1][0], AY, 0], [pts[0][0], AY, 0]).set_fill(GOLD, 0.16 * p["dim"]).set_stroke(width=0)
            g.add(fillp)
            c1 = VMobject().set_points_as_corners(pts).set_stroke(GOLD, 16, opacity=(0.08 + 0.1 * sh + 0.4 * p["glow"]) * p["dim"])
            c2 = VMobject().set_points_as_corners(pts).set_stroke(GOLD, 6, opacity=p["dim"])
            g.add(c1, c2)
    if p["Ab"] > 0.01:
        r = Rectangle(width=14 * DAY, height=0.55).set_fill(GREEN, (0.45 + 0.3 * p["glowb"]) * p["Ab"] * p["dim"]).set_stroke(GREEN, 3 + 4 * p["glowb"], opacity=p["Ab"] * p["dim"])
        r.move_to([dx(bc), BAR_Y + 0.06 * np.sin(1.8 * p["tm"]), 0])
        g.add(r)
        # tiny nestling beaks (open, waiting): three dots on the bar
        for j in (-0.3, 0, 0.3):
            g.add(Dot([dx(bc) + j * 1.12 / 1.0 * 0.8, BAR_Y + 0.02 * np.sin(2.5 * p["tm"] + j * 9), 0], radius=0.07, color=BG).set_opacity(p["Ab"] * p["dim"]))
    if p["Ar"] > 0.01:
        x0 = dx(gc)
        x1 = x0 + (dx(bc) - x0) * min(1, p["Ar"])
        w = 7 + 5 * p["glowr"]
        g.add(Line([x0, BR_Y, 0], [x1, BR_Y, 0], color=RED, stroke_width=w))
        g.add(Line([x0, BR_Y - 0.15, 0], [x0, BR_Y + 0.15, 0], color=RED, stroke_width=w))
        g.add(Line([x1, BR_Y - 0.15, 0], [x1, BR_Y + 0.15, 0], color=RED, stroke_width=w))
        g.add(Dot([x0, BR_Y + 0.35, 0], radius=0.1, color=GOLD))
        if p["Ar"] > 0.98:
            g.add(Dot([x1, BR_Y + 0.35, 0], radius=0.1, color=GREEN))
    return g


class Cal:
    def __init__(self, **kw):
        base = dict(DEFAULT); base.update(kw)
        self.v = {k: ValueTracker(x) for k, x in base.items()}
        self.tm = ValueTracker(0)
        self.tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.dyn = always_redraw(lambda: cal_build(self.p()))
        self.motes = self._motes()

    def p(self):
        d = {k: t.get_value() for k, t in self.v.items()}
        d["tm"] = self.tm.get_value()
        return d

    def _motes(self):
        g = VGroup()
        rng = np.random.RandomState(7)
        for i in range(30):
            d = Dot(radius=0.07, color=TEXT)
            d.x, d.y, d.sp = rng.uniform(-5.8, 5.8), rng.uniform(-3.3, 1.8), rng.uniform(0.15, 0.4)

            def up(m, dt, self=self):
                m.x += m.sp * dt
                m.y += 0.05 * dt
                if m.x > 5.9:
                    m.x = -5.9
                if m.y > 1.8:
                    m.y = -3.3
                m.move_to([m.x, m.y, 0])
                m.set_color(lerpc(TEXT, ORANGE, self.v["tint"].get_value()))
                m.set_opacity(0.55 * self.v["mo"].get_value())
            d.add_updater(up)
            g.add(d)
        return g

    def add(self, sc):
        sc.add(self.motes, self.dyn, self.tm)

    def day(self, key):
        return self.v[key].get_value()


class Amb(SpokenScene):
    """Every scene gets a slow field of drifting motes so a held frame is never dead."""
    NO_AMB = False

    def setup(self):
        super().setup()
        if self.NO_AMB:
            return
        g = VGroup()
        rng = np.random.RandomState(11)
        for i in range(26):
            d = Dot(radius=0.07, color=TEXT)
            d.x, d.y, d.sp = rng.uniform(-6.5, 6.5), rng.uniform(-3.6, 3.6), rng.uniform(0.2, 0.5)

            def up(m, dt):
                m.x += m.sp * dt
                m.y += 0.08 * dt * np.sin(m.x)
                if m.x > 6.6:
                    m.x = -6.6
                m.move_to([m.x, m.y, 0])
                m.set_opacity(0.3)
            d.add_updater(up)
            g.add(d)
        self.add(g)


class CS(Amb):
    NO_AMB = True
    def cal(self, **kw):
        c = Cal(**kw)
        c.add(self)
        return c


def years_counter(c):
    def f():
        yr = 30 * ((75 - c.day("gc")) / 23 * 0.5 + (75 - c.day("bc")) / 8 * 0.5)
        return M(f"years: {yr:.0f}", 30, TEXT).move_to([0, 3.3, 0])
    return always_redraw(f)


def goldlab(): return lab("caterpillar peak (food)", 28, GOLD, w=4.6).move_to([RX, 1.2, 0])
def barlab(): return lab("nestlings in the nest (demand)", 26, GREEN, w=4.3).move_to([RX - 0.2, BAR_Y, 0])
def schem(): return lab("schematic", 26, TEXT, w=2.0).move_to([RX + 1.7, 2.45, 0])


# ================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Global Change: Species on the Move"
    TITLE = "Two Forests, One Bird"


def mountain_recap():
    P = lambda x, y: [x, y, 0]
    tri = Polygon(P(-3.0, -3.0), P(0, 3.0), P(3.0, -3.0), stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.06)
    band = Polygon(P(-1.9, -0.6), P(1.9, -0.6), P(1.85, -0.05), P(-1.85, -0.05)).set_fill(GREEN, 0.5).set_stroke(GREEN, 3)
    gold = Line(P(-2.1, 0.4), P(2.1, 0.4), color=GOLD, stroke_width=7)
    brk = VGroup(Line(P(2.5, -0.05), P(2.5, 0.4), color=RED, stroke_width=6), Line(P(2.4, -0.05), P(2.6, -0.05), color=RED, stroke_width=6),
                 Line(P(2.4, 0.4), P(2.6, 0.4), color=RED, stroke_width=6))
    return VGroup(tri, band, gold, brk)


class S01Question(CS):
    def construct(self):
        c = self.cal(Aax=1.0, mo=1.0)
        ey = -0.1
        e = egg(2.0, ey, 2.2)
        q = T("keeping up?", 54, TEXT).move_to([0, 2.4, 0])
        self.at("lays its eggs")
        self.play(FadeIn(e, scale=0.6), run_time=0.8)
        self.at("earlier every spring")
        ar = Arrow([2.0, 0.55, 0], [-0.6, 0.55, 0], color=ORANGE, buff=0, stroke_width=8)
        self.play(e.animate.move_to([-0.6, ey, 0]), GrowArrow(ar), run_time=1.6)
        self.at("keeping up")
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.8)
        m = mountain_recap().shift(DOWN * 0.0)
        mt = VGroup(m).move_to([-2.2, -0.25, 0]).scale(0.95)
        gl = lab("isotherm", 32, GOLD, w=3).move_to([4.6, 0.95, 0])
        sl = lab("species", 32, GREEN, w=3).move_to([4.6, -1.25, 0])
        gp = lab("gap in space", 34, RED, w=3.4).move_to([4.5, -0.15, 0])
        self.at("The first film")
        self.play(FadeOut(e), FadeOut(ar), FadeOut(q), FadeOut(c.dyn), FadeOut(c.motes), FadeIn(mt, shift=RIGHT * 0.3), run_time=1.2)
        self.at("species and its isotherm")
        self.play(FadeIn(gl), run_time=0.5)
        self.play(FadeIn(sl), run_time=0.5)
        self.play(FadeIn(gp), run_time=0.6)
        self.at("This film")
        self.play(FadeOut(gl), FadeOut(sl), FadeOut(gp),
                  Rotate(mt, angle=-PI / 2, about_point=mt.get_center()), mt.animate.scale(0.35).move_to([0, -0.2, 0]).set_opacity(0.0),
                  run_time=1.2)
        self.remove(mt)
        c2 = Cal(gc=63, bc=75, Ag=0, Ab=0, Ar=0)
        c2.add(self)
        self.play(c2.v["Ag"].animate.set_value(1), c2.v["Ab"].animate.set_value(1), run_time=0.7)
        self.at("gap in time")
        self.play(c2.v["Ar"].animate.set_value(1), run_time=0.8)
        gt = lab("gap in time", 40, RED, w=4).move_to([dx(69), -3.3, 0])
        self.play(FadeIn(gt), c2.v["glowr"].animate.set_value(1), run_time=0.6)
        self.play(c2.v["glowr"].animate.set_value(0), run_time=0.6)
        self.finish()


class S02Phenology(CS):
    def construct(self):
        c = self.cal(Aax=1.0)
        icon_y = 0.55
        ph = T("phenology", 52, TEXT).move_to([0, 2.45, 0])
        self.at("phenology")
        self.play(FadeIn(ph, shift=UP * 0.2), run_time=0.8)
        items = [("Leafing", "leaf", leaf, 36, TREE), ("flowering", "flower", flower, 64, PINK),
                 ("migration", "migration", bird, 92, BIRDC), ("egg laying", "egg", egg, 120, EGGC)]
        icons = []
        for phrase, name, fn, d, col in items:
            ic = fn(dx(d), icon_y, 1.9 if name != "migration" else 1.4)
            lb = lab(name, 30, TEXT, w=2.4).move_to([dx(d), icon_y + 1.0, 0])
            icons.append((ic, lb))
        for (phrase, *_), (ic, lb) in zip(items, icons):
            self.at(phrase)
            self.play(FadeIn(ic, scale=0.4), FadeIn(lb, shift=UP * 0.1), run_time=0.7)
        self.at("As springs have warmed")
        self.play(c.v["tint"].animate.set_value(1), run_time=2.0)
        self.at("earlier")
        el = lab("earlier", 40, ORANGE, w=3).move_to([0, -2.2, 0])
        ar = Arrow([1.4, -2.9, 0], [-1.4, -2.9, 0], color=ORANGE, buff=0, stroke_width=8)
        anims = []
        for ic, lb in icons:
            anims += [ic.animate.shift(LEFT * 0.9), lb.animate.shift(LEFT * 0.9)]
        self.play(*anims, FadeIn(el), GrowArrow(ar), run_time=2.2)
        self.finish()


class S03Calendar(CS):
    def construct(self):
        c = self.cal(Aax=1.0)
        self.at("Now one bird")
        b = bird(-4.8, 1.3, 1.1)
        ct = caterpillar(-3.2, 1.35, 1.1)
        self.play(FadeIn(b, scale=0.6), FadeIn(ct, shift=UP * 0.2), run_time=1.0)
        self.at("gold curve")
        self.play(FadeOut(b), FadeOut(ct), c.v["Ag"].animate.set_value(1), run_time=1.3)
        gl = goldlab()
        self.at("caterpillar peak")
        self.play(FadeIn(gl), run_time=0.7)
        self.at("green bar")
        self.play(c.v["Ab"].animate.set_value(1), run_time=1.4)
        bl = barlab()
        self.at("nestlings need feeding")
        self.play(FadeIn(bl), c.v["glowb"].animate.set_value(1), run_time=0.8)
        self.play(c.v["glowb"].animate.set_value(0), run_time=0.6)
        sc = schem()
        self.at("start in step")
        self.play(c.v["glow"].animate.set_value(1), c.v["glowb"].animate.set_value(1), FadeIn(sc), run_time=0.7)
        self.play(c.v["glow"].animate.set_value(0), c.v["glowb"].animate.set_value(0), run_time=0.8)
        self.finish()


class S04Shift(CS):
    def construct(self):
        c = self.cal(Ag=1, Ab=1)
        gl, bl, sc = goldlab(), barlab(), schem()
        self.add(gl, bl, sc)
        cnt = years_counter(c)
        self.at("Warm the springs")
        self.play(c.v["tint"].animate.set_value(1), FadeIn(cnt), run_time=2.0)
        self.at("gold peak slides")
        self.play(c.v["gc"].animate.set_value(52), run_time=3.0, rate_func=smooth)
        self.at("green bar slides")
        self.play(c.v["bc"].animate.set_value(67), run_time=2.4, rate_func=smooth)
        self.at("red bracket")
        self.play(c.v["Ar"].animate.set_value(1), run_time=1.4)
        self.play(c.v["glowr"].animate.set_value(1), run_time=0.5)
        self.play(c.v["glowr"].animate.set_value(0), run_time=0.5)
        self.finish()


class S05Mismatch(CS):
    def construct(self):
        c = self.cal(Ag=1, Ab=1, gc=52, bc=67, tint=1, Ar=1)
        gl, bl, sc = goldlab(), barlab(), schem()
        cnt = years_counter(c)
        self.add(gl, bl, sc, cnt)
        mm = lab("trophic mismatch", 40, RED, w=5).move_to([dx(59.5), -3.3, 0])
        self.at("trophic mismatch")
        self.play(FadeIn(mm, scale=1.15), c.v["glowr"].animate.set_value(1), run_time=0.8)
        self.play(c.v["glowr"].animate.set_value(0), run_time=0.8)
        self.at("Demand now peaks")
        t1 = lab("earlier", 34, GREEN, w=3).move_to([RX, -1.6, 0])
        self.play(FadeOut(bl), FadeOut(cnt), c.v["glowb"].animate.set_value(1), FadeIn(t1), run_time=1.0)
        self.play(c.v["glowb"].animate.set_value(0), run_time=0.6)
        self.at("cannot show")
        t2 = lab("still late for its food", 34, RED, w=4.6).move_to([RX - 0.4, -2.35, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), c.v["glowr"].animate.set_value(1), run_time=0.8)
        self.play(c.v["glowr"].animate.set_value(0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- the Both et al. scenes
def africa():
    pts = [(-1.0, 1.9), (0.1, 2.2), (1.2, 1.8), (1.9, 0.9), (1.4, 0.0), (1.0, -1.0), (0.5, -2.1), (-0.2, -2.0), (-0.6, -0.6), (-1.5, 0.3), (-1.6, 1.2)]
    return Polygon(*[[x, y, 0] for x, y in pts]).set_fill(BROWN, 0.5).set_stroke(TEXT, 2)


def europe():
    pts = [(-1.4, -0.5), (-0.5, 0.6), (1.0, 0.8), (2.0, 0.2), (1.6, -0.7), (0.0, -0.9)]
    return Polygon(*[[x, y, 0] for x, y in pts]).set_fill(TREE, 0.4).set_stroke(TEXT, 2)


class S06Both(Amb):
    def construct(self):
        q = T("Does mismatch cost birds?", 52, TEXT).move_to([0, 0.6, 0])
        brk = VGroup(Line([-2.0, -0.7, 0], [2.0, -0.7, 0], color=RED, stroke_width=8), Line([-2.0, -0.9, 0], [-2.0, -0.5, 0], color=RED, stroke_width=8),
                     Line([2.0, -0.9, 0], [2.0, -0.5, 0], color=RED, stroke_width=8))
        self.play(FadeIn(q, shift=UP * 0.2), Create(brk), run_time=1.0)
        bob(q, 0.06, 2.0)
        self.play(brk.animate.shift(RIGHT * 0.15), rate_func=there_and_back, run_time=1.2)
        bob(brk, 0.07, 2.4)
        card = lab("Both and colleagues, Nature, 2006", 34, TEXT, w=9).move_to([0, 3.3, 0])
        af = africa().scale(0.9).move_to([-4.0, -1.0, 0])
        eu = europe().scale(1.0).move_to([3.2, 0.4, 0])
        afl = lab("Africa", 32, TEXT, w=2.4).move_to([-4.0, -3.4, 0])
        nl = lab("Netherlands", 32, TEXT, w=3.2).move_to([3.4, -1.0, 0])
        self.at("colleagues")
        self.play(FadeOut(q), FadeOut(brk), FadeIn(card), FadeIn(af), FadeIn(eu), run_time=1.0)
        self.play(FadeIn(afl), FadeIn(nl), run_time=0.5)
        pins = VGroup(*[Dot([3.0 + 0.45 * (i % 3) - 0.2 + 0.1 * (i // 3), 0.1 + 0.4 * (i // 3) + 0.1 * (i % 2), 0], radius=0.1, color=RED) for i in range(9)])
        pins.move_to([3.35, 0.55, 0])
        self.at("nine Dutch populations")
        self.play(LaggedStart(*[FadeIn(p, scale=2.0) for p in pins], lag_ratio=0.15), run_time=1.2)
        pl = lab("9 nest-box sites", 30, RED, w=3.2).move_to([3.4, 1.9, 0])
        self.play(FadeIn(pl), run_time=0.3)
        fl = bird(-4.0, -0.3, 1.0, BIRDC)
        self.at("pied flycatcher")
        self.play(FadeIn(fl, scale=0.5), run_time=0.7)
        self.at("winters in Africa")
        wl = lab("winters", 30, TEXT, w=2).move_to([-4.0, 1.4, 0])
        self.play(FadeIn(wl), run_time=0.4)
        arc = ArcBetweenPoints([-3.5, 0.0, 0], [2.9, 0.9, 0], angle=-0.9).set_stroke(TEXT, 4)
        dash = DashedVMobject(arc, num_dashes=24)
        self.play(Create(dash), MoveAlongPath(fl, arc), FadeOut(wl), run_time=2.0, rate_func=smooth)
        self.at("European woods")
        bl = lab("breeds", 30, TEXT, w=2).move_to([3.0, 2.5, 0])
        self.play(FadeIn(bl), run_time=0.4)
        for i in range(2):
            self.play(fl.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- two forests
FW = 5.6
FC = (-3.4, 3.4)


def fx(cx, f): return cx + (f - 0.5) * FW


def mini_build(cx, oy, ky, gp, bp, Ar, glow, tm):
    g = VGroup()
    g.add(Line([fx(cx, 0.02), oy, 0], [fx(cx, 0.98), oy, 0], color=TEXT, stroke_width=3))
    amp = 1.6 * ky * (1 + 0.05 * np.sin(1.5 * tm))
    fs = np.linspace(gp - 0.2, gp + 0.2, 50)
    pts = [[fx(cx, f), oy + amp * np.exp(-((f - gp) ** 2) / (2 * 0.065 ** 2)), 0] for f in fs]
    g.add(Polygon(*pts, [pts[-1][0], oy, 0], [pts[0][0], oy, 0]).set_fill(GOLD, 0.16).set_stroke(width=0))
    sh = 0.5 + 0.5 * np.sin(2.2 * tm)
    g.add(VMobject().set_points_as_corners(pts).set_stroke(GOLD, 12, opacity=0.1 + 0.1 * sh + 0.3 * glow))
    g.add(VMobject().set_points_as_corners(pts).set_stroke(GOLD, 5))
    by = oy - 0.3 - 0.35 * ky
    g.add(Rectangle(width=0.17 * FW, height=0.3).set_fill(GREEN, 0.5).set_stroke(GREEN, 3).move_to([fx(cx, bp), by, 0]))
    if Ar > 0.01:
        ry = oy - 0.65 - 0.55 * ky
        x0 = fx(cx, gp)
        x1 = x0 + (fx(cx, bp) - x0) * min(1, Ar)
        if abs(x1 - x0) > 0.02:
            g.add(Line([x0, ry, 0], [x1, ry, 0], color=RED, stroke_width=6 + 4 * glow))
            g.add(Line([x0, ry - 0.12, 0], [x0, ry + 0.12, 0], color=RED, stroke_width=6))
            g.add(Line([x1, ry - 0.12, 0], [x1, ry + 0.12, 0], color=RED, stroke_width=6))
    return g


FD = dict(oy=0.3, ky=1.2, gpL=0.5, bpL=0.58, gpR=0.5, bpR=0.58, ArL=0.0, ArR=0.0, glow=0.0, hL=1.0, hR=1.0, Acnt=0.0, dec=0.0)
CB_BOT, CB_H = -3.2, 2.3


class Forests:
    def __init__(self, **kw):
        base = dict(FD); base.update(kw)
        self.v = {k: ValueTracker(x) for k, x in base.items()}
        self.tm = ValueTracker(0)
        self.tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.dyn = always_redraw(self.build)

    def val(self, k): return self.v[k].get_value()

    def build(self):
        g = VGroup()
        tm = self.val("dec") * 0 + self.tm.get_value()
        for cx, s in zip(FC, "LR"):
            g.add(mini_build(cx, self.val("oy"), self.val("ky"), self.val("gp" + s), self.val("bp" + s), self.val("Ar" + s), self.val("glow") if s == "L" else 0, tm))
        if self.val("Acnt") > 0.01:
            a = self.val("Acnt")
            for cx, s in zip(FC, "LR"):
                h = max(0.04, CB_H * self.val("h" + s))
                r = Rectangle(width=1.6, height=h).set_fill(GREEN, 0.55 * a).set_stroke(GREEN, 3, opacity=a)
                r.move_to([cx, CB_BOT + h / 2, 0])
                g.add(r)
                top = CB_BOT + CB_H
                g.add(DashedLine([cx - 2.5, top, 0], [cx + 2.5, top, 0], color=TEXT, stroke_width=3, stroke_opacity=0.6 * a))
        return g

    def add(self, sc):
        sc.add(self.dyn, self.tm)


def headers(early="early food peak", late="late food peak"):
    return VGroup(lab(early, 32, TEXT, w=3.0).move_to([-3.4, 3.25, 0]), lab(late, 32, TEXT, w=3.0).move_to([3.9, 3.25, 0]),
                  tree(-5.5, 3.0, 0.45), tree(1.7, 3.0, 0.45))


def forest_trees():
    g = VGroup()
    for cx in FC:
        for j in range(6):
            g.add(tree(cx - 2.4 + j * 0.96, -3.35 + 0.15 * (j % 2), 1.0))
    return g


class S07Forests(Amb):
    def construct(self):
        f = Forests(gpL=0.5, bpL=0.58, gpR=0.5, bpR=0.58)
        f.add(self)
        trees = forest_trees()
        hd = headers()
        self.at("In some of the forests")
        self.play(FadeIn(trees, lag_ratio=0.05), FadeIn(hd), run_time=1.6)
        self.at("caterpillars peaked early")
        self.play(f.v["gpL"].animate.set_value(0.28), run_time=2.0)
        self.play(f.v["ArL"].animate.set_value(1), run_time=1.0)
        self.at("In others they peaked late")
        self.play(f.v["gpR"].animate.set_value(0.64), run_time=1.5)
        self.at("birds that bred early")
        self.play(f.v["bpR"].animate.set_value(0.6), run_time=1.0)
        self.at("well timed")
        self.play(f.v["glow"].animate.set_value(0), run_time=0.2)
        self.finish()


class S08Counts(Amb):
    def construct(self):
        f = Forests(gpL=0.28, bpL=0.58, ArL=1, gpR=0.64, bpR=0.6, Acnt=0)
        f.add(self)
        trees = forest_trees()
        hd = headers()
        self.add(trees, hd)
        dec = ValueTracker(0)
        cnt = always_redraw(lambda: M(f"decades: {dec.get_value():.1f}", 24, TEXT).move_to([0, 2.7, 0]))
        sl = lab("start", 28, TEXT, w=1.6).move_to([-5.7, CB_BOT + CB_H + 0.3, 0])
        self.at("Where food peaked early")
        self.play(FadeOut(trees), f.v["oy"].animate.set_value(1.5), f.v["ky"].animate.set_value(0.5), f.v["Acnt"].animate.set_value(1), FadeIn(cnt), FadeIn(sl), run_time=1.8)
        self.at("flycatcher numbers fell")
        self.play(f.v["hL"].animate.set_value(0.1), dec.animate.set_value(2.0), run_time=4.0, rate_func=linear)
        tl = lab("about 90% decline", 32, RED, w=4.4).move_to([-3.4, -0.2, 0])
        self.play(FadeIn(tl), run_time=0.6)
        self.at("Where it peaked late")
        self.play(f.v["hR"].animate.set_value(0.88), run_time=2.2)
        tr = lab("weak decline at most", 32, GREEN, w=4.6).move_to([3.4, -0.2, 0])
        self.at("weak at most")
        self.play(FadeIn(tr), run_time=0.6)
        self.finish()


def bars_state():
    """kwargs for the end state of S08."""
    return dict(oy=1.5, ky=0.5, gpL=0.28, bpL=0.58, ArL=1, gpR=0.64, bpR=0.6, Acnt=1, hL=0.1, hR=0.88)


def counts_scene_base(sc):
    f = Forests(**bars_state())
    f.add(sc)
    hd = headers()
    sc.add(hd)
    return f, hd


def chips_yn():
    a = chip("yes, proven", COOL, 30).move_to([-3.4, -1.3, 0])
    b = chip("not yet", GOLD, 30).move_to([-3.4, -2.1, 0])
    return a, b


class S09Predict(Amb):
    def construct(self):
        f, hd = counts_scene_base(self)
        tl = lab("about 90% decline", 32, RED, w=4.4).move_to([-3.4, -0.2, 0])
        tr = lab("weak decline at most", 32, GREEN, w=4.6).move_to([3.4, -0.2, 0])
        self.add(tl, tr)
        self.at("The early forests lost")
        self.play(FadeOut(tr), f.v["glow"].animate.set_value(1), run_time=0.8)
        self.at("nine pairs in every ten")
        t9 = lab("9 of 10 pairs lost", 32, RED, w=4.4).move_to([-3.4, -0.2, 0])
        self.play(Transform(tl, t9), run_time=0.8)
        self.play(f.v["glow"].animate.set_value(0), run_time=0.6)
        a, b = chips_yn()
        self.at("Does that comparison prove")
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.6)
        self.play(f.v["glow"].animate.set_value(1), run_time=0.5)
        self.play(f.v["glow"].animate.set_value(0), run_time=0.5)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        f = Forests(**bars_state())
        f.add(self)
        self.add(headers())
        self.add(lab("9 of 10 pairs lost", 32, RED, w=4.4).move_to([-3.4, -0.2, 0]))
        a, b = chips_yn()
        self.add(a, b)
        cap = lab("Predict: proof, or not yet?", 34, TEXT, w=9).move_to([0, -3.6, 0])
        self.add(cap)
        n = ValueTracker(5)
        ring = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * (n.get_value() / 5), color=GOLD, stroke_width=7).move_to([0, 3.25, 0]))
        num = always_redraw(lambda: M(str(max(1, int(np.ceil(n.get_value())))), 36, TEXT).move_to([0, 3.25, 0]))
        self.add(ring, num)
        self.play(n.animate.set_value(0.01), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S11Reveal(Amb):
    def construct(self):
        f, hd = counts_scene_base(self)
        tl = lab("9 of 10 pairs lost", 32, RED, w=4.4).move_to([-3.4, -0.2, 0])
        self.add(tl)
        a, b = chips_yn()
        self.add(a, b)
        bob(tl, 0.08, 2.5)
        bob(a, 0.06, 2.2)
        self.at("Not yet")
        self.play(FadeOut(a), b.animate.scale(1.25).set_stroke(GOLD, 6), f.v["glow"].animate.set_value(1), run_time=0.8)
        self.play(f.v["glow"].animate.set_value(0), run_time=0.5)
        bob(b, 0.07, 2.5)
        self.at("compares sites")
        stamp = lab("comparison, not manipulation", 38, RED, w=8.4).move_to([0, -0.2, 0])
        box = SurroundingRectangle(stamp, color=RED, buff=0.18, stroke_width=5)
        sg = VGroup(box, stamp)
        self.play(FadeIn(sg, scale=1.4), FadeOut(tl), run_time=0.7)
        self.at("something else could differ")
        icons = []
        for i, (nm, x) in enumerate((("soil", -1.85), ("predators", -0.7), ("habitat", 0.8))):
            q = T("?", 56, GREY)
            tx = lab(nm, 26, GREY, w=1.5)
            gp = VGroup(q, tx).arrange(DOWN, buff=0.1).move_to([x, -2.8, 0])
            gp.ph = i
            gp.add_updater(lambda m, dt, i=i, x=x: m.move_to([x + 0.05 * np.sin(1.3 * self.elapsed() + i * 2), -2.5 + 0.2 * np.sin(1.0 * self.elapsed() + i), 0]))
            icons.append(gp)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.3) for g in icons], lag_ratio=0.4), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------- cue: field and aviaries
class S12Cue(Amb):
    def construct(self):
        nest = Arc(radius=1.1, start_angle=PI, angle=PI, color=BROWN, stroke_width=0).add(Ellipse(width=2.4, height=0.9).set_fill(BROWN, 0.9).set_stroke(BROWN, 3))
        nest.move_to([0, -1.9, 0])
        tit = bird(0, -1.2, 2.0, BIRDC)
        etxt = lab("earlier laying?", 40, TEXT, w=4.2).move_to([0, 3.3, 0])
        eg = egg(0, 2.3, 2.8)
        th_level = ValueTracker(0.3)
        th = always_redraw(lambda: thermo(-4.7, 0.0, 3.0, th_level.get_value(), ORANGE))
        thl = lab("warm spring", 30, ORANGE, w=2.6).move_to([-4.7, -2.4, 0])
        ct = caterpillar(4.6, 0.3, 2.2)
        ctl = lab("early food", 30, GOLD, w=2.6).move_to([4.6, -1.0, 0])
        self.add(nest)
        self.at("A second question")
        self.play(FadeIn(tit, shift=UP * 0.2), FadeIn(eg, scale=0.6), run_time=1.0)
        bob(tit, 0.05, 2.0)
        self.at("what tells a bird")
        self.play(FadeIn(etxt, shift=UP * 0.15), run_time=0.8)
        self.play(eg.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=1.0)
        bob(eg, 0.07, 2.6, 1.0)
        self.at("In the field")
        self.add(th)
        self.play(FadeIn(thl), th_level.animate.set_value(0.95), run_time=2.6, rate_func=smooth)
        self.at("they also bring early food")
        self.play(FadeIn(ct, shift=LEFT * 0.4), FadeIn(ctl), run_time=1.2)
        a1 = CurvedArrow([-3.9, 1.0, 0], [-0.7, 2.2, 0], angle=-0.7, color=ORANGE, stroke_width=7)
        a2 = CurvedArrow([3.7, 1.2, 0], [0.7, 2.2, 0], angle=0.7, color=GOLD, stroke_width=7)
        a3 = CurvedArrow([-3.7, 0.2, 0], [0.5, 1.8, 0], angle=0.5, color=ORANGE, stroke_width=4)
        a4 = CurvedArrow([3.5, 0.5, 0], [-0.5, 1.7, 0], angle=-0.5, color=GOLD, stroke_width=4)
        self.at("The pattern alone")
        self.play(Create(a1), Create(a2), Create(a3), Create(a4), run_time=1.6)
        self.play(eg.animate.scale(1.2), th_level.animate.set_value(0.8), run_time=0.6)
        self.play(eg.animate.scale(1 / 1.2), th_level.animate.set_value(0.95), run_time=0.6)
        self.finish()


def aviary(cx, y=-0.35, w=5.0, h=4.2):
    fr = Rectangle(width=w, height=h).set_fill(TEXT, 0.04).set_stroke(TEXT, 4).move_to([cx, y, 0])
    mesh = VGroup()
    for i in range(1, 8):
        mesh.add(Line([cx - w / 2 + i * w / 8, y - h / 2, 0], [cx - w / 2 + i * w / 8, y + h / 2, 0], color=TEXT, stroke_width=1, stroke_opacity=0.25))
    for j in range(1, 6):
        mesh.add(Line([cx - w / 2, y - h / 2 + j * h / 6, 0], [cx + w / 2, y - h / 2 + j * h / 6, 0], color=TEXT, stroke_width=1, stroke_opacity=0.25))
    return VGroup(fr, mesh)


def dish(cx, y):
    d = Ellipse(width=1.3, height=0.4).set_fill(BROWN, 1).set_stroke(TEXT, 2).move_to([cx, y, 0])
    food = VGroup(*[Dot([cx - 0.4 + 0.2 * i, y + 0.12 + 0.04 * (i % 2), 0], radius=0.07, color=GOLD) for i in range(5)])
    return VGroup(d, food)


class S13Aviary(Amb):
    def construct(self):
        card = lab("Visser, Holleman and Caro, 2009", 34, TEXT, w=9).move_to([0, 3.35, 0])
        avs = [aviary(-3.4), aviary(3.4)]
        birds = [VGroup(bird(cx - 0.6, -1.0, 1.0, BIRDC), bird(cx + 0.5, -0.6, 1.0, BIRDC, flip=True)) for cx in (-3.4, 3.4)]
        dishes = [dish(cx, -2.1) for cx in (-3.4, 3.4)]
        self.at("Marcel Visser")
        self.play(FadeIn(card, shift=DOWN * 0.15), run_time=0.8)
        self.at("kept breeding pairs")
        self.play(FadeIn(avs[0]), FadeIn(avs[1]), run_time=1.0)
        self.play(FadeIn(birds[0], scale=0.5), FadeIn(birds[1], scale=0.5), run_time=0.8)
        for b in birds:
            b.add_updater(lambda m, dt: m.shift(UP * 0.0025 * np.sin(4 * self.elapsed())))
        self.at("climatized aviaries")
        ids = lab("identical aviaries", 30, TEXT, w=4).move_to([0, 2.75, 0])
        self.play(FadeIn(ids), run_time=0.6)
        self.at("Every aviary had food")
        self.play(FadeOut(ids), FadeIn(dishes[0], shift=UP * 0.2), FadeIn(dishes[1], shift=UP * 0.2), run_time=1.0)
        fl = lab("food: freely available", 30, GOLD, w=4.4).move_to([0, -3.15, 0])
        self.play(FadeIn(fl), run_time=0.6)
        self.at("Only the temperature pattern")
        tl = ValueTracker(0.1)
        tr = ValueTracker(0.1)
        th1 = always_redraw(lambda: thermo(-5.7, 0.5, 2.4, tl.get_value(), ORANGE))
        th2 = always_redraw(lambda: thermo(5.7, 0.5, 2.4, tr.get_value(), COOL))
        self.add(th1, th2)
        tintL = Rectangle(width=5.0, height=4.2).set_fill(ORANGE, 0.0).set_stroke(width=0).move_to([-3.4, -0.35, 0])
        tintR = Rectangle(width=5.0, height=4.2).set_fill(COOL, 0.0).set_stroke(width=0).move_to([3.4, -0.35, 0])
        self.add(tintL, tintR)
        self.play(tl.animate.set_value(0.95), tr.animate.set_value(0.2), tintL.animate.set_fill(ORANGE, 0.25), tintR.animate.set_fill(COOL, 0.2), FadeOut(fl), run_time=2.4)
        self.at("warm or cold")
        wl = lab("warm", 36, ORANGE, w=2).move_to([-3.4, 2.4, 0])
        cl = lab("cold", 36, COOL, w=2).move_to([3.4, 2.4, 0])
        self.play(FadeIn(wl), FadeIn(cl), run_time=0.8)
        self.finish()


class S14Result(Amb):
    def construct(self):
        # rebuild film state of S13, then shrink the aviaries up
        avs = VGroup(aviary(-3.4), aviary(3.4))
        birds = VGroup(*[VGroup(bird(cx - 0.6, -1.0, 1.0, BIRDC), bird(cx + 0.5, -0.6, 1.0, BIRDC, flip=True)) for cx in (-3.4, 3.4)])
        dishes = VGroup(dish(-3.4, -2.1), dish(3.4, -2.1))
        tintL = Rectangle(width=5.0, height=4.2).set_fill(ORANGE, 0.25).set_stroke(width=0).move_to([-3.4, -0.35, 0])
        tintR = Rectangle(width=5.0, height=4.2).set_fill(COOL, 0.2).set_stroke(width=0).move_to([3.4, -0.35, 0])
        th1 = thermo(-5.7, 0.5, 2.4, 0.95, ORANGE)
        th2 = thermo(5.7, 0.5, 2.4, 0.2, COOL)
        wl = lab("warm", 36, ORANGE, w=2).move_to([-3.4, 2.4, 0])
        cl = lab("cold", 36, COOL, w=2).move_to([3.4, 2.4, 0])
        top = VGroup(avs, birds, dishes, tintL, tintR, th1, th2, wl, cl)
        self.add(top)
        for b in birds:
            b.add_updater(lambda m, dt: m.shift(UP * 0.0025 * np.sin(4 * self.elapsed())))
        # calendar strips
        def strip(cx):
            g = VGroup(Line([cx - 2.8, -1.0, 0], [cx + 2.8, -1.0, 0], color=TEXT, stroke_width=4))
            for k, s in enumerate(("Mar", "Apr", "May", "Jun")):
                x = cx - 2.8 + 5.6 * (k + 0.5) / 4
                g.add(Line([cx - 2.8 + 5.6 * k / 4, -1.0, 0], [cx - 2.8 + 5.6 * k / 4, -1.15, 0], color=TEXT, stroke_width=3))
                g.add(T(s, 24, TEXT).move_to([x, -1.45, 0]))
            g.add(Line([cx + 2.8, -1.0, 0], [cx + 2.8, -1.15, 0], color=TEXT, stroke_width=3))
            return g
        s1, s2 = strip(-3.4), strip(3.4)
        self.at("The warm aviaries")
        self.play(top.animate.scale(0.5, about_point=[0, 3.8, 0]), FadeIn(s1), FadeIn(s2), run_time=1.2)
        e1 = egg(-3.4 + 5.6 * (0.3 - 0.5), 1.4, 2.0)
        e2 = egg(3.4 + 5.6 * (0.65 - 0.5), 1.4, 2.0)
        self.at("generally laid earlier")
        e1.move_to([-3.4 + 5.6 * (0.3 - 0.5), 0.7, 0])
        e2.move_to([3.4 + 5.6 * (0.65 - 0.5), 0.7, 0])
        self.add(e1)
        self.play(e1.animate.shift(DOWN * 1.45), run_time=0.8)
        self.add(e2)
        self.play(e2.animate.shift(DOWN * 1.45), run_time=0.8)
        l1 = lab("warm: earlier laying, generally", 32, ORANGE, w=5.4).move_to([-3.4, -2.1, 0])
        self.play(FadeIn(l1), run_time=0.5)
        self.at("With food unlimited")
        fl = lab("food: unlimited", 30, GOLD, w=4).move_to([3.4, -2.1, 0])
        self.play(FadeIn(fl), run_time=0.6)
        self.at("likely acting as a cue")
        tg = chip("temperature: likely a cue", ORANGE, 34).move_to([0, -3.15, 0])
        self.play(FadeIn(tg, scale=1.15), run_time=0.8)
        bob(tg, 0.06, 2.4)
        self.at("a signal")
        self.play(tg.animate.scale(1.08), run_time=0.5)
        self.play(tg.animate.scale(1 / 1.08), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- the three designs
def card_frame(cx, col=TEXT):
    return RoundedRectangle(corner_radius=0.2, width=4.1, height=6.4).set_fill(TEXT, 0.05).set_stroke(col, 3, opacity=0.5).move_to([cx, -0.2, 0])


def stack(lines, size, color, cx, y, w=3.7):
    g = VGroup(*[lab(s, size, color, w=w) for s in lines]).arrange(DOWN, buff=0.08)
    return g.move_to([cx, y, 0])


class S15Ladder(Amb):
    def construct(self):
        xs = (-4.5, 0.0, 4.5)
        frames = [card_frame(x) for x in xs]
        glow = ValueTracker(-1)
        for i, fr in enumerate(frames):
            fr.add_updater(lambda m, dt, i=i: m.set_stroke(GOLD if glow.get_value() == i else TEXT, 3 + 2 * (glow.get_value() == i) * (0.5 + 0.5 * np.sin(4 * self.elapsed())), opacity=1.0 if glow.get_value() == i else 0.5))
        self.at("Each design answers")
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.3) for f in frames], lag_ratio=0.25), run_time=1.6)
        # card 1
        h1 = stack(["trend:", "did something", "change?"], 28, TEXT, -4.5, 2.1)
        ic1 = VGroup(Line([-5.3, 0.65, 0], [-3.7, 0.65, 0], color=TEXT, stroke_width=3))
        for i in range(5):
            ic1.add(Dot([-5.1 + 0.4 * i, 0.9 + 0.0, 0], radius=0.0))
        eg = egg(-3.9, 0.95, 1.6)
        ar = Arrow([-3.9, 1.3, 0], [-5.1, 1.3, 0], color=ORANGE, buff=0, stroke_width=6)
        b1 = stack(["detection tests it", "against chance", "and natural", "variation"], 28, TEXT, -4.5, -1.3)
        self.at("A trend suggests")
        glow.set_value(0)
        self.play(FadeIn(h1), run_time=0.8)
        self.play(FadeIn(ic1), FadeIn(eg), GrowArrow(ar), run_time=1.2)
        self.at("Testing it against chance")
        self.play(FadeIn(b1, shift=UP * 0.1), run_time=1.0)
        # card 2
        h2 = stack(["comparison across", "sites: does food", "timing go with", "decline?"], 28, TEXT, 0.0, 2.1)
        ic2 = VGroup(Line([-0.9, 0.55, 0], [0.9, 0.55, 0], color=TEXT, stroke_width=3), Rectangle(width=0.5, height=0.3).set_fill(GREEN, 0.6).set_stroke(GREEN, 2).move_to([0.2, 0.2, 0]),
                     Line([-0.5, 0.55, 0], [-0.5, 1.2, 0], color=GOLD, stroke_width=6))
        ic2.add(Line([-0.5, 0.0, 0], [0.2, 0.0, 0], color=RED, stroke_width=5))
        b2 = stack(["flycatcher forests", "(can be confounded)"], 28, TEXT, 0.0, -1.3)
        self.at("The forest comparison")
        glow.set_value(1)
        self.play(FadeIn(h2), FadeIn(ic2), run_time=1.0)
        self.at("sites can differ")
        self.play(FadeIn(b2, shift=UP * 0.1), run_time=1.0)
        # card 3
        h3 = stack(["manipulation:", "does temperature", "move laying?"], 28, TEXT, 4.5, 2.1)
        ic3 = VGroup(aviary(4.5, 0.75, 1.9, 1.3), bird(4.5, 0.75, 0.5, BIRDC), thermo(5.65, 0.75, 1.0, 0.8, ORANGE))
        b3 = stack(["great-tit aviaries", "(cause, in that", "preparation)"], 28, TEXT, 4.5, -1.3)
        self.at("The aviaries show")
        glow.set_value(2)
        self.play(FadeIn(h3), FadeIn(ic3), run_time=1.0)
        self.at("in great tits")
        self.play(FadeIn(b3, shift=UP * 0.1), run_time=1.0)
        self.finish()


class S16Close(CS):
    def construct(self):
        c = self.cal(Ag=1, Ab=1, gc=52, bc=67, tint=1, Ar=1)
        gl = goldlab()
        e = lab("earlier", 34, GREEN, w=3).move_to([RX, -1.7, 0])
        self.add(gl, e)
        mm = lab("trophic mismatch", 40, RED, w=5).move_to([dx(59.5), -3.3, 0])
        self.add(mm)
        self.at("the date alone")
        self.play(FadeOut(e), c.v["glowb"].animate.set_value(1), run_time=1.2)
        self.play(c.v["glowb"].animate.set_value(0), run_time=0.5)
        self.at("What counted")
        self.play(c.v["dim"].animate.set_value(0.4), FadeOut(gl), c.v["glowr"].animate.set_value(1), run_time=1.4)
        self.at("the food and the family")
        gp = lab("the gap", 44, RED, w=3).move_to([RX, BR_Y + 0.4, 0])
        self.play(FadeIn(gp), run_time=0.8)
        self.finish()


class S17End(EndCard):
    LINE = "Keeping up is judged by the gap, not by the date."
