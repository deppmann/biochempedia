"""Across or Along the Membrane? (chapter 2) -- one carried membrane world.

Same colour map as chapter 1:
  GREY membranes and the oily core   GOLD cytosol face   TEAL outside face
  BLUE protein (and PC)   YELLOW PS   GREEN PE   RED sphingomyelin   ORANGE the barrier
  PURPLE ATP
Every lipid token drifts with one shared motion so rows never collide; crossings are
changes of a token's target row (continuous), never a cut.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CYTO = GOLD
LUMEN = TEAL
MEM = GREY


def P(x, y):
    return np.array([x, y, 0.0])


def double_line(x0, x1, y, gap=0.16, color=MEM, width=6):
    return VGroup(Line(P(x0, y - gap / 2), P(x1, y - gap / 2), color=color, stroke_width=width),
                  Line(P(x0, y + gap / 2), P(x1, y + gap / 2), color=color, stroke_width=width))


def moving_specks(seed=1, count=72, area=(-6.5, 6.5, -3.45, 2.2)):
    """One visual object: a continuously drifting cytosol field."""
    rng = np.random.RandomState(seed)
    x0, x1, y0, y1 = area
    dots = VGroup()
    for _ in range(count):
        d = Dot(P(rng.uniform(x0, x1), rng.uniform(y0, y1)), radius=rng.uniform(.045, .085), color=CYTO)
        d.set_opacity(rng.uniform(.24, .52))
        d.v = P(rng.uniform(-.18, .20), rng.uniform(.11, .24))

        def drift(m, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            m.shift(m.v * dt)
            if m.get_y() > y1: m.shift(DOWN * (y1 - y0))
            if m.get_x() > x1: m.shift(LEFT * (x1 - x0))
            if m.get_x() < x0: m.shift(RIGHT * (x1 - x0))
        d.add_updater(drift)
        dots.add(d)
    return dots


def schematic_tag():
    return T("schematic", 28, GREY).to_corner(DR, buff=.26)


def protein(pos=P(0, 0), scale=1.0, sugar=True, vertical=True):
    """N points into teal, C into gold.  The membrane is horizontal."""
    if vertical:
        bar = RoundedRectangle(width=.34 * scale, height=1.48 * scale, corner_radius=.12,
                               stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(pos)
        npos, cpos = pos + UP * .93 * scale, pos + DOWN * .93 * scale
    else:
        bar = RoundedRectangle(width=1.48 * scale, height=.34 * scale, corner_radius=.12,
                               stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(pos)
        npos, cpos = pos + LEFT * .93 * scale, pos + RIGHT * .93 * scale
    def terminal(letter, center, color):
        circ = Circle(radius=.29 * scale, stroke_width=0, fill_color=color, fill_opacity=1).move_to(center)
        lab = T(letter, max(22, int(27 * scale)), BG, weight=BOLD).move_to(circ)
        return VGroup(circ, lab)
    n, c = terminal("N", npos, YELLOW), terminal("C", cpos, GREEN)
    g = VGroup(bar, n, c)
    g.bar, g.N, g.C = bar, n, c
    if sugar:
        hi = scale >= 1.0   # large membrane view: lift the tag clear of the lipid row
        stem = Line(npos + RIGHT * .18 * scale, npos + (P(.62, .80) if hi else P(.52, .42)) * scale,
                    color=ORANGE, stroke_width=max(3, 5 * scale))
        if scale >= .70:
            flag = RoundedRectangle(width=1.05 * scale, height=.48 * scale, corner_radius=.08,
                                    stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                                    fill_opacity=.22).move_to(npos + (P(.86, 1.05) if hi else P(.86, .50)) * scale)
            label = T("sugar", 28, ORANGE).move_to(flag)
            g.sugar = VGroup(stem, flag, label)
        else:
            flag = Square(side_length=.28 * scale, stroke_width=0, fill_color=ORANGE,
                          fill_opacity=1).move_to(npos + P(.58, .46) * scale)
            g.sugar = VGroup(stem, flag)
        g.add(g.sugar)
    return g


def whole_world(seed=2, proteins=False):
    """Stable whole-cell layout reused without lateral drift."""
    outside = Rectangle(width=13.3, height=1.18, stroke_width=0, fill_color=LUMEN,
                        fill_opacity=.20).move_to(P(0, 3.05))
    cyt = Rectangle(width=13.3, height=5.9, stroke_width=0, fill_color=CYTO,
                    fill_opacity=.075).move_to(P(0, -.45))
    pm = double_line(-6.6, 6.6, 2.43, .16)
    er = RoundedRectangle(width=4.15, height=2.05, corner_radius=.65, stroke_color=MEM,
                          stroke_width=7, fill_color=LUMEN, fill_opacity=.18).move_to(P(-3.75, .25))
    er2 = er.copy().scale(.88)
    erwall = VGroup(er, er2)
    golgi = VGroup()
    for i, (w, y) in enumerate([(3.05, .82), (2.75, .19), (2.42, -.44)]):
        sac = RoundedRectangle(width=w, height=.43, corner_radius=.20, stroke_color=MEM,
                               stroke_width=5, fill_color=LUMEN, fill_opacity=.20).move_to(P(1.50, y))
        golgi.add(sac)
    endo = Circle(radius=.72, stroke_color=MEM, stroke_width=6, fill_color=LUMEN,
                  fill_opacity=.20).move_to(P(4.35, -.90))
    labels = VGroup(T("outside", 28, LUMEN).move_to(P(-5.45, 3.05)),
                    T("ER lumen", 28, LUMEN).move_to(P(-4.78, .55)),
                    T("Golgi", 28, LUMEN).move_to(P(1.5, 1.42)),
                    T("cytosol", 28, CYTO).move_to(P(-.25, -2.75)))
    motes = moving_specks(seed)
    world = VGroup(cyt, outside, motes, pm, erwall, golgi, endo, labels)
    world.outside, world.cyt, world.pm, world.er, world.golgi, world.endo = outside, cyt, pm, erwall, golgi, endo
    world.motes, world.labels = motes, labels
    if proteins:
        ves = Circle(radius=.52, stroke_color=MEM, stroke_width=4, fill_color=LUMEN,
                     fill_opacity=.18).move_to(P(3.15, 1.30))
        ps = VGroup(protein(P(-3.72, -.74), .62), protein(P(1.5, -.67), .55),
                    protein(P(3.15, .78), .52), protein(P(4.4, 2.43), .62),
                    protein(P(4.35, -1.60), .50))
        world.proteins = ps
        world.add(ves, ps)
    return world




# ------------------------------------------------------------------ shared membrane world
PURPLE = "#B58CF5"
CYC = 17.6                 # tokens wrap after this many units, always off screen
OUT_Y, IN_Y = 1.5, -1.5
CORE = .82
PS_C, PE_C, PC_C, SM_C = YELLOW, GREEN, BLUE, RED
OUTER_C, INNER_C = LUMEN, CYTO


def F_of(t):
    """The film's computed example: 20 + 60 (1 - 2^(-t/4))."""
    return 20 + 60 * (1 - 2 ** (-t / 4.0))


def membrane_bg(seed=5, width=14.6, cx=0.0, specks=30):
    teal = Rectangle(width=width, height=3.18, stroke_width=0, fill_color=LUMEN, fill_opacity=.18).move_to(P(cx, 2.41))
    gold = Rectangle(width=width, height=3.18, stroke_width=0, fill_color=CYTO, fill_opacity=.075).move_to(P(cx, -2.41))
    core = Rectangle(width=width, height=2*CORE, stroke_width=0, fill_color=MEM, fill_opacity=.30).move_to(P(cx, 0))
    l1 = Line(P(cx - width / 2, CORE), P(cx + width / 2, CORE), color=MEM, stroke_width=5)
    l2 = Line(P(cx - width / 2, -CORE), P(cx + width / 2, -CORE), color=MEM, stroke_width=5)
    motes = moving_specks(seed, count=specks, area=(cx - width / 2 + .2, cx + width / 2 - .2, -3.9, -2.2))
    g = VGroup(gold, teal, motes, core, l1, l2)
    g.teal, g.gold, g.core = teal, gold, core
    return g


def tie_asym(bg, a):
    bg.gold.add_updater(lambda m: m.set_fill(opacity=.05 + .14 * a.get_value()))
    bg.teal.add_updater(lambda m: m.set_fill(opacity=.08 + .22 * a.get_value()))


def face_labels():
    return VGroup(T("outside", 30, LUMEN).move_to(P(-6.0, 3.45)), T("cytosol", 30, CYTO).move_to(P(-6.0, -3.45)))


def _lip_upd(m, dt):
    m.tt += dt
    if m.vx:
        m.x0 += m.vx * dt
        if m.x0 > CYC / 2:
            m.x0 -= CYC
    if m.tx is not None:
        m.x0 += (m.tx - m.x0) * min(1, dt * m.kx)
    if m.At is not None:
        m.A += (m.At - m.A) * min(1, dt * 2.0)
    y = m.get_y()
    y += (m.ty - y) * min(1, dt * m.k)
    m.move_to(P(m.x0 + m.A * math.sin(m.w * m.tt + m.ph), y))


def lip(label, color, x, y, size=32, vx=0.0, A=0.0, w=1.0, ph=0.0):
    txt = T(label, size, color)
    box = RoundedRectangle(width=max(.95, txt.width + .36), height=.8, corner_radius=.16, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=.18)
    txt.move_to(box)
    g = VGroup(box, txt).move_to(P(x, y))
    g.box, g.txt = box, txt
    g.x0, g.ty, g.tx, g.vx, g.kx = x, y, None, vx, 2.0
    g.A, g.At, g.w, g.ph, g.tt, g.k = A, None, w, ph, 0.0, 1.8
    g.add_updater(_lip_upd)
    return g


STD_OUT = [("sphingomyelin", SM_C, -6.6), ("PC", PC_C, -2.2), ("PC", PC_C, 2.2), ("sphingomyelin", SM_C, 6.6)]
STD_IN = [("PE", PE_C, -6.6), ("PS", PS_C, -4.4), ("PE", PE_C, 4.4), ("PS", PS_C, 6.6)]
EVEN_OUT = [("sphingomyelin", SM_C, -4.4), ("PC", PC_C, 0.0), ("PC", PC_C, 4.4)]
EVEN_IN = [("PE", PE_C, -5.1), ("PS", PS_C, -1.7), ("PE", PE_C, 1.7), ("PS", PS_C, 5.1)]
CLUMP_OUT = [("sphingomyelin", SM_C, -5.0), ("PC", PC_C, -1.3), ("PC", PC_C, 0.9)]
CLUMP_IN = [("PE", PE_C, -5.6), ("PS", PS_C, -4.0), ("PE", PE_C, -0.4), ("PS", PS_C, 3.6)]


def lips(spec, y, size=28, **kw):
    return [lip(l, c, x, y, size=(28 if l == "sphingomyelin" else 34), **kw) for l, c, x in spec]


def std_membrane(vx=.6, seed=5):
    bg = membrane_bg(seed)
    outer, inner = lips(STD_OUT, OUT_Y, vx=vx), lips(STD_IN, IN_Y, vx=vx)
    return bg, outer, inner


def pulse(m, color=None, scale=1.15):
    return Indicate(m, color=color or m.get_color(), scale_factor=scale)


def set_vx(toks, v):
    for t in toks:
        t.vx = v


class Machine(VGroup):
    """A gate in the oily core (gap, flippase or scramblase). Its name floats above the outer row. Drifts with the lipids."""

    def __init__(self, cx, kind="gap", vx=.6, sw=4.6):
        super().__init__()
        self.cx, self.vx, self.kind, self.on, self.sw = cx, vx, kind, False, sw
        self.build()
        self.add_updater(lambda m, dt: m.step(dt))

    def build(self):
        self.submobjects = []
        if self.kind == "gap":
            self.rect = RoundedRectangle(width=1.3, height=1.45, corner_radius=.1, stroke_color=ORANGE,
                                         stroke_width=4, fill_color=BG, fill_opacity=1)
            self.lab = self.arr = None
            self.add(self.rect)
        else:
            w = 1.3 if self.kind == "flippase" else self.sw
            self.rect = RoundedRectangle(width=w, height=1.45, corner_radius=.12, stroke_color=TEXT, stroke_width=4,
                                         fill_color=(TEAL if self.on else BG), fill_opacity=(.45 if self.on else 1))
            self.lab = T("flippase" if self.kind == "flippase" else "scramblase", 34, TEXT)
            if self.kind == "flippase":
                self.arr = Arrow(P(0, .5), P(0, -.5), buff=0, tip_length=.25, stroke_width=7, color=TEXT)
            else:
                self.arr = DoubleArrow(P(0, .5), P(0, -.5), buff=0, tip_length=.25, stroke_width=7,
                                       color=(TEXT if self.on else GREY))
            self.add(self.rect, self.arr, self.lab)
        self.place()

    def place(self):
        self.rect.move_to(P(self.cx, 0))
        if self.lab is not None:
            self.lab.move_to(P(self.cx, 2.72))
            self.lab.set_opacity(max(0., min(1., (5.4 - abs(self.cx)) / 1.2)))
            self.arr.move_to(P(self.cx, 0))

    def step(self, dt):
        if self.vx:
            self.cx += self.vx * dt
            if self.cx > CYC / 2:
                self.cx -= CYC
        self.place()

    def set_kind(self, kind, on=False):
        self.kind, self.on = kind, on
        self.build()


def clock(pos, r=.55, speed=1.4):
    face = Circle(radius=r, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(pos)
    hand = Line(pos, pos + UP * (r * .8), color=TEXT, stroke_width=5)
    hand.add_updater(lambda m, dt: m.rotate(-speed * dt, about_point=pos))
    return VGroup(face, hand)


def gauge(valfn, pos, label, color=PURPLE, H=2.0, W=.6):
    box = Rectangle(width=W, height=H, stroke_color=color, stroke_width=4).move_to(pos)

    def make():
        h = max(.02, (H - .1) * max(0., min(1., valfn())))
        return Rectangle(width=W - .1, height=h, stroke_width=0, fill_color=color, fill_opacity=.9).move_to(
            box.get_bottom() + UP * (.05 + h / 2))
    fill = always_redraw(make)
    lab = T(label, 28, color).next_to(box, LEFT, buff=.15)
    return VGroup(box, fill, lab)


def vertical_arrow_blocked(x=6.65):
    arr = DoubleArrow(P(x, -2.2), P(x, 2.2), buff=0, color=TEXT, stroke_width=5, tip_length=.25)
    cross = T("×", 64, RED, weight=BOLD).move_to(P(x, 0))
    return VGroup(arr, cross)


# ------------------------------------------------------------------ plots (computed from the film's equation)
class Plot:
    def __init__(s, x0, x1, y0, y1, tmin, tmax):
        s.x0, s.x1, s.y0, s.y1, s.tmin, s.tmax = x0, x1, y0, y1, tmin, tmax

    def X(s, t):
        return s.x0 + (t - s.tmin) / (s.tmax - s.tmin) * (s.x1 - s.x0)

    def Y(s, F):
        return s.y0 + F / 100.0 * (s.y1 - s.y0)

    def pt(s, t, F):
        return P(s.X(t), s.Y(F))

    def axes(s, xticks=(0, 8, 16), yticks=(20, 50, 80, 100)):
        g = VGroup(Line(P(s.x0, s.y0), P(s.x1 + .15, s.y0), color=TEXT, stroke_width=4),
                   Line(P(s.x0, s.y0), P(s.x0, s.y1 + .15), color=TEXT, stroke_width=4))
        for t in xticks:
            g.add(M(str(t), 22, TEXT).move_to(P(s.X(t), s.y0 - .33)))
        for f in yticks:
            g.add(M(str(f), 22, TEXT).move_to(P(s.x0 - .42, s.Y(f))))
        g.add(T("time", 28, TEXT).move_to(P(s.x1 - .2, s.y0 - .82)))
        g.add(T("fluorescence", 26, TEXT).rotate(PI / 2).move_to(P(s.x0 - 1.18, (s.y0 + s.y1) / 2)))
        return g

    def curve(s, ta=0.0, tb=16.0, color=BLUE, f=F_of, n=140, width=7):
        m = VMobject(color=color, stroke_width=width)
        m.set_points_as_corners([s.pt(t, f(t)) for t in np.linspace(ta, tb, n)])
        return m


# ------------------------------------------------------------------ FRAP window: one tracker-driven world
def _blk_upd(m, dt):
    F = m.F
    m.tt += dt
    k = min(1, dt * m.k)
    m.hx += (m.tx - m.hx) * k
    m.hy += (m.ty - m.hy) * k
    m.lit += (m.lt - m.lit) * min(1, dt * 2.5)
    wx = m.a * (math.sin(m.w1 * m.tt + m.ph) - math.sin(m.ph))
    wy = m.a * (math.cos(m.w2 * m.tt + m.ph) - math.cos(m.ph))
    s = F.s.get_value()
    m.set_width(max(.05, .5 * s))
    m.move_to(P(F.cx.get_value() + s * (m.hx + wx), F.cy.get_value() + s * (m.hy + wy)))
    m.set_stroke(TEXT, width=7, opacity=max(0., min(1., m.lit)))


class Frap:
    RL = 3.6

    def __init__(self, cx=0., cy=0., s=1., bleached=False):
        self.cx, self.cy, self.s = ValueTracker(cx), ValueTracker(cy), ValueTracker(s)
        self.ring, self.glow = ValueTracker(1. if bleached else 0.), ValueTracker(0.)
        self.win = always_redraw(lambda: Circle(radius=self.RL * self.s.get_value(), stroke_color=GREY, stroke_width=5,
                                                fill_color=GREY, fill_opacity=.12).move_to(self.c()))
        self.spot = always_redraw(lambda: Circle(radius=1.25 * self.s.get_value(), stroke_color=RED, stroke_width=5,
                                                 stroke_opacity=self.ring.get_value(), fill_color=TEXT,
                                                 fill_opacity=self.glow.get_value() * .25).move_to(self.c()))
        inner = [(-.6, .5), (.5, .65), (0, -.05), (-.7, -.55), (.65, -.4), (0, -.95)]
        outer = []
        for i in range(8):
            a = math.radians(i * 45 + 15)
            r = 2.15 if i % 2 == 0 else 2.9
            outer.append((r * math.cos(a), r * math.sin(a)))
        self.blocks = []
        rng = np.random.RandomState(4)
        for i, (x, y) in enumerate(inner + outer):
            b = Square(side_length=.5, stroke_width=7, stroke_color=TEXT, fill_color=BLUE, fill_opacity=.95)
            b.F, b.hx, b.hy, b.tx, b.ty = self, x, y, x, y
            b.k, b.tt, b.a = .8, 0., .22
            b.w1, b.w2, b.ph = rng.uniform(.7, 1.3), rng.uniform(.7, 1.3), rng.uniform(0, 6.28)
            dark = bleached and i < 6
            b.lit, b.lt = (0. if dark else 1.), (0. if dark else 1.)
            b.add_updater(_blk_upd)
            self.blocks.append(b)
        self.group = VGroup(self.win, self.spot, *self.blocks)

    def c(self):
        return P(self.cx.get_value(), self.cy.get_value())

    def brightness(self):
        n = sum(b.lit for b in self.blocks if math.hypot(b.hx, b.hy) < 1.25)
        return n / 6.0

    def bleach_targets(self):
        for b in self.blocks[:6]:
            b.lt = 0.

    def cycle(self, ids, k=.9):
        homes = [(self.blocks[i].tx, self.blocks[i].ty) for i in ids]
        for n, i in enumerate(ids):
            b = self.blocks[i]
            b.tx, b.ty = homes[(n + 1) % len(ids)]
            b.k = k

    def move(self, cx, cy, s):
        return [self.cx.animate.set_value(cx), self.cy.animate.set_value(cy), self.s.animate.set_value(s)]


def question_card(text="Sideways only: do the faces mix?", size=34):
    q = T(text, size, TEXT)
    box = RoundedRectangle(width=q.width + .6, height=q.height + .45, corner_radius=.15, stroke_color=TEXT,
                           stroke_width=2, fill_color=BG, fill_opacity=.92)
    return VGroup(box, q).move_to(P(0, 3.3))


# ================================================================== scenes
class S00Hook(SpokenScene, TitleCard):
    LESSON = "Membrane organization and topology"
    TITLE = "Across or Along the Membrane?"

    def construct(self):
        w = whole_world(10)
        tag = schematic_tag()
        p = protein(P(-3.72, -.74), .72)
        self.add(w, tag, p)
        path = VMobject().set_points_smoothly([P(-3.72, -.74), P(-1.6, -.45), P(1.5, -.2), P(3.15, 1.2), P(4.4, 2.43)])
        self.play(MoveAlongPath(p, path), run_time=4.2, rate_func=linear)
        self.at("but lipids")
        bg, outer, inner = std_membrane(.6, 20)
        lab = face_labels()
        pm = protein(P(-1.0, 0), 1.2)
        pm.vx = .6
        pm.add_updater(lambda m, dt: m.shift(RIGHT * m.vx * dt))
        self.play(FadeOut(w), FadeOut(p), FadeIn(bg), FadeIn(VGroup(*outer, *inner)), FadeIn(pm), run_time=1.3)
        self.at("locked in place")
        set_vx(outer + inner + [pm], 1.3)
        self.wait(1.2)
        set_vx(outer + inner + [pm], .6)
        self.at("how does")
        q = T("?", 84, TEXT, weight=BOLD).move_to(P(-3.3, 0))
        self.play(GrowFromCenter(q), run_time=.8)
        self.at("different lipids")
        self.play(pulse(VGroup(*outer), LUMEN, 1.1), pulse(VGroup(*inner), CYTO, 1.1), run_time=1.0)
        self.at("on the two faces")
        self.play(FadeIn(lab), run_time=.7)
        self.at("molecules still move")
        set_vx(outer + inner + [pm], 1.2)
        self.wait(1.4)
        set_vx(outer + inner + [pm], .6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        bg, outer, inner = std_membrane(.6, 21)
        title = T("Across or Along the Membrane?", 50, TEXT, font=TITLE_FONT)
        fit(title, max_w=12)
        rule = Line(LEFT * 1.25, RIGHT * 1.25, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=.3)
        plate = RoundedRectangle(width=title.width + .8, height=title.height + 1.0, corner_radius=.18, stroke_width=0,
                                 fill_color=BG, fill_opacity=.86).move_to(VGroup(title, rule))
        self.add(bg, *outer, *inner, face_labels())
        self.play(FadeIn(plate), FadeIn(title, shift=UP * .15), GrowFromCenter(rule), run_time=.5)
        self.wait(.95)
        self.play(FadeOut(VGroup(plate, title, rule)), run_time=.5)


class S02Pattern(SpokenScene):
    def construct(self):
        sea = Rectangle(width=14.6, height=8.2, stroke_width=0, fill_color=LUMEN, fill_opacity=.16)
        cell = Ellipse(width=5.4, height=3.6, stroke_color=MEM, stroke_width=8, fill_color=CYTO, fill_opacity=.18)
        cell.add_updater(lambda m, dt: m.scale(1 + .012 * math.sin(self.renderer.time * 3.0)))
        lab = T("red blood cell", 40, TEXT)
        self.add(sea, cell)
        self.play(FadeIn(lab), run_time=.6)
        self.at("gives the best")
        cell.clear_updaters()
        self.play(FadeOut(lab), cell.animate.scale(2.5), run_time=1.8)
        bg, outer, inner = std_membrane(.6, 22)
        self.play(ReplacementTransform(cell, bg.core), FadeOut(sea), FadeIn(bg.teal), FadeIn(bg.gold),
                  FadeIn(VGroup(bg[2], bg[4], bg[5])), FadeIn(VGroup(*outer, *inner)), run_time=1.5)
        self.add(bg)
        tag = schematic_tag()
        self.add(tag, face_labels())
        self.at("PS and PE")
        l1 = T("cytoplasmic leaflet", 32, CYTO).move_to(P(1.4, -3.05))
        self.play(FadeIn(l1), pulse(VGroup(*[t for t in inner if t.txt.text in ("PS", "PE")]), None, 1.18), run_time=1.1)
        self.at("PC and sphingomyelin")
        l2 = T("outer leaflet", 32, LUMEN).move_to(P(1.4, 3.05))
        self.play(FadeIn(l2), pulse(VGroup(*outer), None, 1.12), run_time=1.1)
        self.at("sideways drifting")
        a1 = DoubleArrow(P(-2.6, 2.4), P(2.6, 2.4), buff=0, color=LUMEN, stroke_width=5)
        a2 = DoubleArrow(P(-2.6, -2.4), P(2.6, -2.4), buff=0, color=CYTO, stroke_width=5)
        set_vx(outer + inner, 1.2)
        self.play(GrowFromCenter(a1), GrowFromCenter(a2), run_time=.9)
        self.at("erase that pattern")
        self.play(Indicate(VGroup(l1, l2), scale_factor=1.06), run_time=1.0)
        self.finish()


class S03Barrier(SpokenScene):
    def construct(self):
        a, atp = ValueTracker(.55), ValueTracker(0.)
        bg, outer, inner = std_membrane(.6, 23)
        tie_asym(bg, a)
        tr = inner[1]                         # the tracked yellow PS
        self.add(bg, *outer, *inner, face_labels(), schematic_tag())
        self.play(pulse(tr, YELLOW, 1.25), run_time=.9)
        up = always_redraw(lambda: DashedLine(P(tr.get_x(), -1.12), P(tr.get_x(), .55), color=TEXT, stroke_width=5)
                           .add_tip(tip_length=.2))
        self.play(Create(up), run_time=.9)
        self.at("polar head")
        head = always_redraw(lambda: T("polar head", 28, PS_C).move_to(P(tr.get_x(), -2.45)))
        self.play(FadeIn(head), run_time=.6)
        self.at("rarely enters")
        tr.ty = -1.12
        self.at("oily core")
        oily = T("oily core", 34, TEXT).move_to(P(-4.2, 0))
        self.play(bg.core.animate.set_fill(ORANGE, opacity=.5), FadeIn(oily), run_time=.7)
        tr.ty = IN_Y
        self.play(FadeOut(up), FadeOut(head), run_time=.6)
        self.at("without help")
        clk = clock(P(4.9, 0))
        slow = T("slow", 28, TEXT).move_to(P(6.1, 0))
        self.play(FadeIn(clk), FadeIn(slow), run_time=.6)
        self.at("change leaflets")
        ghost = tr.copy()
        ghost.clear_updaters()
        ghost.box.set_fill(opacity=.10).set_stroke(opacity=.4)
        ghost.txt.set_opacity(.45)
        ghost.x0, ghost.ty, ghost.tx, ghost.vx, ghost.kx = tr.x0, IN_Y, None, tr.vx, 2.0
        ghost.A, ghost.At, ghost.w, ghost.ph, ghost.tt, ghost.k = 0., None, 1., 0., 0., .75
        ghost.add_updater(_lip_upd)
        self.add(ghost)
        ghost.ty = OUT_Y
        self.wait(1.5)
        self.play(FadeOut(ghost), run_time=.6)
        self.at("slow is not zero")
        self.play(Indicate(clk, scale_factor=1.15), run_time=.9)
        self.at("spend energy")
        gap = Machine(0.0, "gap")
        g = gauge(lambda: atp.get_value(), P(5.2, -2.45), "ATP", H=1.0)
        self.play(FadeOut(clk), FadeOut(slow), FadeOut(oily), FadeIn(gap), FadeIn(g), run_time=.5)
        self.play(atp.animate.set_value(1.), a.animate.set_value(1.), run_time=1.9)
        self.finish()


class S04Machines(SpokenScene):
    def construct(self):
        a, atp = ValueTracker(1.), ValueTracker(1.)
        bg, outer, inner = std_membrane(.6, 24)
        tie_asym(bg, a)
        bg.core.set_fill(ORANGE, opacity=.5)
        psl = lip("PS", PS_C, 0.0, OUT_Y, vx=.6)              # a PS that leaked outward
        mach = Machine(0.0, "gap")
        g = gauge(lambda: atp.get_value(), P(5.2, -2.45), "ATP", H=1.0)
        self.add(bg, mach, *outer, *inner, psl, g, face_labels(), schematic_tag())
        self.wait(.3)
        mach.set_kind("flippase")
        atpc = lip("ATP", PURPLE, 0.0, -3.5, size=28, vx=.6)
        atpc.ty = -2.65
        self.play(FadeIn(atpc), Indicate(mach, scale_factor=1.06), run_time=.9)
        self.at("selects lipids")
        self.play(pulse(VGroup(psl, inner[1], inner[3]), None, 1.18), run_time=1.0)
        self.at("moves them inward")
        psl.ty = IN_Y
        self.wait(2.2)
        self.at("a scramblaze")
        mach.set_kind("scramblase")
        self.play(FadeOut(atpc), atp.animate.set_value(0.), Indicate(mach, scale_factor=1.06), run_time=1.0)
        self.at("when switched on")
        mach.set_kind("scramblase", on=True)
        self.play(Indicate(mach, color=TEAL, scale_factor=1.08), run_time=1.0)
        self.at("cross both ways")
        psl.ty = OUT_Y
        outer[1].ty = IN_Y                    # PC at -2.2 down
        outer[2].ty = IN_Y                    # PC at 2.2 down
        self.wait(.9)
        self.at("without energy")
        self.play(Indicate(g, color=PURPLE, scale_factor=1.12), run_time=.6)
        self.at("the two leaflets")
        mixed = T("mixed", 46, TEXT).move_to(P(0, -3.15))
        self.play(FadeIn(mixed, shift=UP * .2), a.animate.set_value(.2), run_time=1.5)
        self.finish()


class S04bSteady(SpokenScene):
    def construct(self):
        L = membrane_bg(25, width=6.8, cx=-3.5, specks=14)
        R = membrane_bg(26, width=6.8, cx=3.5, specks=14)
        div = Line(P(0, -4), P(0, 4), color=BG, stroke_width=10)
        divl = Line(P(0, -4), P(0, 4), color=TEXT, stroke_width=2)

        def row(spec, y, off):
            return [lip(l, c, x, y, A=.3, w=1.0, ph=off) for l, c, x in spec]
        lo = row([("PC", PC_C, -5.4), ("PC", PC_C, -0.9)], OUT_Y, 0.0)
        li = row([("PE", PE_C, -5.4), ("PS", PS_C, -2.6), ("PE", PE_C, -0.9)], IN_Y, 3.14)
        ro = row([("PC", PC_C, 1.3), ("PC", PC_C, 5.9)], OUT_Y, 0.0)
        ri = row([("PE", PE_C, 1.3), ("PS", PS_C, 3.55)], IN_Y, 3.14)
        leaker, rcross_in, rcross_out = li[1], ri[1], ro[1]
        self.add(L, R, div, divl, *lo, *li, *ro, *ri, schematic_tag())
        self.wait(.2)
        self.at("slow leakage")
        clk = clock(P(-6.25, 0))
        slow = T("slow", 28, TEXT).move_to(P(-4.95, 0))
        leaker.k = 2.2
        leaker.ty = OUT_Y
        self.play(FadeIn(clk), FadeIn(slow), run_time=.8)
        self.at("pumps")
        fl = Machine(-2.6, "flippase", vx=0)
        self.play(FadeIn(fl), run_time=.6)
        self.at("regulated scrambling")
        sc = Machine(3.55, "scramblase", vx=0, sw=4.4)
        self.play(FadeIn(sc), run_time=.7)
        self.at("steady state")
        self.play(FadeOut(clk), FadeOut(slow), run_time=.4)
        ss = T("steady state", 44, TEXT).move_to(P(-3.5, 3.35))
        self.play(FadeIn(ss, shift=UP * .15), run_time=.8)
        self.at("keep restoring")
        atpc = lip("ATP", PURPLE, -2.6, -3.5, size=28)
        atpc.ty = -2.65
        self.play(FadeIn(atpc), run_time=.6)
        leaker.k = 1.0
        leaker.ty = IN_Y
        self.wait(2.3)
        self.play(FadeOut(atpc), run_time=.4)
        leaker.k = 2.2
        leaker.ty = OUT_Y                     # leaks again, rarely
        self.at("switching on")
        sc.set_kind("scramblase", on=True)
        self.play(Indicate(sc, color=TEAL, scale_factor=1.08), run_time=.8)
        rcross_in.k = rcross_out.k = 1.4
        rcross_in.ty = OUT_Y
        rcross_out.ty = IN_Y
        self.wait(1.2)
        self.at("pattern collapse")
        mixed = T("mixed", 44, TEXT).move_to(P(3.5, 3.35))
        self.play(FadeIn(mixed, shift=UP * .15), run_time=.8)
        self.finish()


def _predict_world(seed):
    bg = membrane_bg(seed)
    outer = lips(CLUMP_OUT, OUT_Y, A=.8, w=1.6, ph=0.0)
    inner = lips(CLUMP_IN, IN_Y, A=.8, w=1.6, ph=3.14)
    return bg, outer, inner


class S05PredictQ(SpokenScene):
    def construct(self):
        bg, outer, inner = _predict_world(27)
        self.add(bg, *outer, *inner, face_labels(), schematic_tag())
        self.at("suppose every")
        arr = VGroup(DoubleArrow(P(-2.8, 2.4), P(2.8, 2.4), buff=0, color=LUMEN, stroke_width=5),
                     DoubleArrow(P(-2.8, -2.4), P(2.8, -2.4), buff=0, color=CYTO, stroke_width=5))
        self.play(GrowFromCenter(arr), run_time=1.0)
        self.at("but none crosses")
        blocked = vertical_arrow_blocked()
        self.play(FadeIn(blocked), run_time=.8)
        self.at("will the two faces")
        self.play(FadeIn(question_card(), shift=DOWN * .15), run_time=.8)
        self.finish()


class S06PredictPause(NarratedScene):
    def construct(self):
        bg, outer, inner = _predict_world(27)
        self.add(bg, *outer, *inner, face_labels(), schematic_tag(), vertical_arrow_blocked(), question_card())
        self.wait(4.4)


class S07PredictA(SpokenScene):
    def construct(self):
        bg, outer, inner = _predict_world(27)
        card = question_card()
        self.add(bg, *outer, *inner, face_labels(), schematic_tag(), vertical_arrow_blocked(), card)
        self.at("now")
        no = question_card("No", 54)
        self.play(Transform(card, no), run_time=.8)
        self.at("each leaflet")
        for t, x in zip(outer, [-4.4, 0.0, 4.4]):
            t.tx, t.At = x, .4
        for t, x in zip(inner, [-5.1, -1.7, 1.7, 5.1]):
            t.tx, t.At = x, .4
        self.wait(2.2)
        self.at("original face")
        self.play(pulse(VGroup(*outer), LUMEN, 1.1), pulse(VGroup(*inner), CYTO, 1.1), run_time=1.1)
        self.at("across and along")
        lab_a = T("across", 32, TEXT).move_to(P(5.35, 0))
        along = Arrow(P(-2.6, 2.5), P(5.0, 2.5), buff=0, color=LUMEN, stroke_width=6)
        lab_b = T("along", 34, LUMEN).move_to(P(-4.4, 2.5))
        self.play(FadeOut(card), FadeIn(lab_a), Create(along), FadeIn(lab_b), run_time=1.3)
        self.at("lateral diffusion")
        big = Arrow(P(-2.6, 2.5), P(5.0, 2.5), buff=0, color=LUMEN, stroke_width=11)
        lab_c = T("lateral diffusion", 34, LUMEN).move_to(P(-4.35, 2.5))
        self.play(Transform(along, big), Transform(lab_b, lab_c), run_time=1.0)
        self.finish()


def _frap_side(f, with_gauge=True):
    pass


class S08Bleach(SpokenScene):
    def construct(self):
        bg = membrane_bg(28)
        outer, inner = lips(EVEN_OUT, OUT_Y, A=.4, w=.8, ph=0.0), lips(EVEN_IN, IN_Y, A=.4, w=.8, ph=3.14)
        lab = face_labels()
        self.add(bg, *outer, *inner, lab)
        f = Frap(0., 0., .3)
        g = gauge(lambda: f.brightness(), P(5.9, -1.2), "spot", color=TEXT, H=3.2)
        tag = schematic_tag().to_corner(DL, buff=.26)
        self.wait(.4)
        self.add(f.group)
        self.play(FadeOut(bg), FadeOut(VGroup(*outer, *inner)), FadeOut(lab), FadeIn(f.group), f.s.animate.set_value(1.0),
                  run_time=2.0)
        self.add(tag)
        self.at("FRAP")
        frap_t = T("FRAP", 56, TEXT, weight=BOLD).move_to(P(5.3, 3.0))
        self.play(FadeIn(frap_t, shift=UP * .15), run_time=.7)
        self.at("lateral motion")
        arr = DoubleArrow(P(4.2, 2.1), P(6.4, 2.1), buff=0, color=TEXT, stroke_width=5)
        lat = T("lateral", 32, TEXT).move_to(P(5.3, 1.55))
        self.play(GrowFromCenter(arr), FadeIn(lat), run_time=.9)
        self.at("fluorescent membrane")
        self.play(FadeIn(g), run_time=.5)
        self.at("begin bright")
        bright = T("bright", 40, TEXT).move_to(P(5.3, .9))
        self.play(FadeIn(bright), Indicate(VGroup(*f.blocks), color=TEXT, scale_factor=1.2), run_time=1.2)
        self.at("a brief laser")
        self.play(FadeOut(VGroup(bright, arr, lat)), run_time=.2)
        beam = Rectangle(width=.16, height=2.8, stroke_width=0, fill_color=RED, fill_opacity=.9).move_to(P(-1.6, 0))
        self.play(FadeIn(beam), run_time=.2)
        self.play(beam.animate.move_to(P(1.6, 0)), run_time=.45, rate_func=linear)
        self.at("makes one spot dark")
        f.bleach_targets()
        self.play(FadeOut(beam), f.ring.animate.set_value(1.0), run_time=.9)
        self.at("unbleached proteins")
        f.cycle([0, 6, 1, 7, 2, 8], k=.55)
        f.cycle([3, 9, 4, 10], k=.55)
        self.wait(1.2)
        self.at("diffuse into it")
        self.play(Indicate(g, color=TEXT, scale_factor=1.08), run_time=1.0)
        self.finish()


def _s9_world(bleached=True, move=False):
    f = Frap(0., 0., 1.0, bleached=bleached)
    return f


class S09Curve(SpokenScene):
    def construct(self):
        f = Frap(0., 0., 1.0, bleached=True)
        pl = Plot(.9, 6.4, -2.7, 2.6, 0, 16)
        ax = pl.axes()
        cur = pl.curve(0, 16)
        tag = schematic_tag().to_corner(DL, buff=.26)
        self.add(f.group, tag)
        self.play(*f.move(-4.15, 0., .72), FadeIn(ax), run_time=1.6)
        self.at("answers two")
        self.play(Create(cur), run_time=1.8, rate_func=linear)
        f.cycle([0, 6, 1, 7], k=.5)
        self.at("how much fluorescence")
        top = pl.pt(14.8, 80)
        brk = DoubleArrow(pl.pt(14.8, 20), top, buff=0, color=YELLOW, stroke_width=6, tip_length=.2)
        inc = VGroup(T("recoverable", 28, YELLOW), T("increase", 28, YELLOW)).arrange(DOWN, buff=.08).move_to(P(pl.X(10), pl.Y(30)))
        self.play(GrowFromCenter(brk), FadeIn(inc), run_time=1.2)
        self.at("mobile fraction")
        self.play(Indicate(VGroup(brk, inc), color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.at("how quickly")
        half = DashedLine(pl.pt(0, 50), pl.pt(4, 50), color=TEXT, stroke_width=4)
        drop = DashedLine(pl.pt(4, 50), pl.pt(4, 0), color=TEXT, stroke_width=4)
        dot = Dot(pl.pt(0, 20), radius=.11, color=TEXT)
        self.play(FadeIn(dot), Create(half), run_time=.7)
        tt = ValueTracker(0.)
        dot.add_updater(lambda m: m.move_to(pl.pt(tt.get_value(), F_of(tt.get_value()))))
        self.play(tt.animate.set_value(4.0), run_time=2.0, rate_func=linear)
        f.cycle([2, 8, 3, 9], k=.5)
        self.play(Create(drop), run_time=.5)
        self.at("half time")
        ht = T("half-time", 28, TEXT).move_to(P(pl.X(4), pl.y0 - .82))
        self.play(FadeIn(ht), run_time=.6)
        self.at("dark molecules")
        f.cycle([4, 10, 5, 11], k=.5)
        self.wait(1.4)
        self.at("bleaching only")
        self.play(Indicate(VGroup(*f.blocks[:6]), color=TEXT, scale_factor=1.15), run_time=1.2)
        self.finish()


def _plot_big():
    return Plot(-5.3, 2.6, -2.7, 2.6, -5, 16)


class S09bFraction(SpokenScene):
    def construct(self):
        pl = _plot_big()
        ax = pl.axes(xticks=(0, 8, 16))
        cur = pl.curve(0, 16)
        self.add(ax)
        self.play(Create(cur), run_time=1.6, rate_func=linear)
        self.at("starts at 100")
        flat = VGroup(Line(pl.pt(-5, 100), pl.pt(0, 100), color=BLUE, stroke_width=7), DashedLine(pl.pt(0, 100), P(3.4, pl.Y(100)), color=TEXT, stroke_width=3))
        c_before = chip("before 100", TEXT, size=34).move_to(P(5.0, pl.Y(100)))
        self.play(Create(flat), FadeIn(c_before), run_time=1.0)
        self.at("falls to 20")
        fall = VGroup(Line(pl.pt(0, 100), pl.pt(0, 20), color=BLUE, stroke_width=7), DashedLine(pl.pt(0, 20), P(3.4, pl.Y(20)), color=TEXT, stroke_width=3))
        c_after = chip("after 20", TEXT, size=34).move_to(P(5.0, pl.Y(20)))
        self.play(Create(fall), FadeIn(c_after), run_time=1.0)
        self.at("plateaus at 80")
        pla = DashedLine(pl.pt(0, 80), P(3.4, pl.Y(80)), color=TEXT, stroke_width=4)
        c_pl = chip("plateau 80", TEXT, size=34).move_to(P(5.0, pl.Y(80)))
        self.play(Create(pla), FadeIn(c_pl), run_time=1.0)
        self.at("60 units returned")
        self.play(FadeOut(VGroup(c_before, c_after, c_pl)), run_time=.4)
        b1 = Rectangle(width=.6, height=pl.Y(80) - pl.Y(20), stroke_width=0, fill_color=YELLOW, fill_opacity=.9)
        b1.move_to(P(3.9, (pl.Y(80) + pl.Y(20)) / 2))
        l1 = VGroup(T("returned", 28, YELLOW), T("60", 34, YELLOW)).arrange(DOWN, buff=.08).move_to(P(3.9, -2.55))
        self.play(FadeIn(b1, shift=UP * .3), FadeIn(l1), run_time=1.1)
        self.at("but 80 were bleached")
        b2 = Rectangle(width=.6, height=pl.Y(100) - pl.Y(20), stroke_width=0, fill_color=RED, fill_opacity=.9)
        b2.move_to(P(5.9, (pl.Y(100) + pl.Y(20)) / 2))
        l2 = VGroup(T("bleached", 28, RED), T("80", 34, RED)).arrange(DOWN, buff=.08).move_to(P(5.9, -2.55))
        self.play(FadeIn(b2, shift=UP * .3), FadeIn(l2), run_time=1.1)
        self.at("mobile fraction is")
        self.play(FadeOut(VGroup(b1, l1, b2, l2)), run_time=.6)
        c1 = M("60 divided by 80", 24, TEXT).move_to(P(5.2, 1.0))
        c2 = M("= 0.75", 44, TEXT).move_to(P(5.2, 0.0))
        self.play(FadeIn(c1, shift=LEFT * .3), run_time=.9)
        self.at("or 0")
        self.play(FadeIn(c2, shift=LEFT * .3), run_time=.7)
        ring = SurroundingRectangle(c2, color=YELLOW, buff=.18, stroke_width=5)
        mf = T("mobile fraction", 34, YELLOW).move_to(P(4.7, -1.0))
        self.play(Create(ring), FadeIn(mf), run_time=.9)
        self.finish()


class S09cHalf(SpokenScene):
    def construct(self):
        pl = _plot_big()
        ax = pl.axes(xticks=(0, 8, 16))
        cur = pl.curve(0, 16)
        flat = Line(pl.pt(-5, 100), pl.pt(0, 100), color=BLUE, stroke_width=7)
        fall = Line(pl.pt(0, 100), pl.pt(0, 20), color=BLUE, stroke_width=7)
        pla = DashedLine(pl.pt(0, 80), pl.pt(16, 80), color=TEXT, stroke_width=4)
        hb = pl.Y(80) - pl.Y(20)
        b1 = Rectangle(width=.6, height=hb, stroke_width=0, fill_color=YELLOW, fill_opacity=.9)
        b1.move_to(P(3.9, (pl.Y(80) + pl.Y(20)) / 2))
        l1 = VGroup(T("returned", 28, YELLOW), T("60", 34, YELLOW)).arrange(DOWN, buff=.08).move_to(P(3.9, -2.55))
        self.add(ax, cur, flat, fall, pla, b1, l1)
        self.at("half of the recoverable")
        top = Rectangle(width=.6, height=hb / 2, stroke_width=0, fill_color=YELLOW, fill_opacity=.9)
        bot = top.copy().set_fill(opacity=.45)
        top.move_to(P(3.9, pl.Y(65)))
        bot.move_to(P(3.9, pl.Y(35)))
        t30 = T("30", 34, YELLOW).move_to(P(4.7, pl.Y(65)))
        self.play(FadeOut(b1), FadeOut(l1), FadeIn(top), FadeIn(bot), run_time=.8)
        self.play(FadeIn(t30), top.animate.shift(UP * .15), bot.animate.shift(DOWN * .15), run_time=.8)
        self.at("add that to 20")
        hb2 = hb / 2
        dest = P(pl.X(-3.3), pl.Y(20) + hb2 / 2)
        self.play(FadeOut(bot), top.animate.move_to(dest), t30.animate.move_to(dest + RIGHT * .65), run_time=1.5)
        self.at("halfway level 50")
        lvl = DashedLine(pl.pt(-5, 50), pl.pt(16, 50), color=TEXT, stroke_width=4)
        lv_t = T("halfway", 30, TEXT).move_to(P(pl.X(12), pl.Y(50) + .4))
        self.play(Create(lvl), FadeIn(lv_t), run_time=1.2)
        self.at("the curve reaches 50")
        dot = Dot(pl.pt(0, 20), radius=.12, color=TEXT)
        tt = ValueTracker(0.)
        dot.add_updater(lambda m: m.move_to(pl.pt(tt.get_value(), F_of(tt.get_value()))))
        self.add(dot)
        self.play(tt.animate.set_value(4.0), run_time=1.7, rate_func=linear)
        guide = DashedLine(pl.pt(4, 50), pl.pt(4, 0), color=YELLOW, stroke_width=5)
        sec = T("4 seconds", 30, YELLOW).move_to(P(pl.X(4), pl.y0 - .82))
        self.play(Create(guide), FadeIn(sec), run_time=.8)
        self.at("recovery half time")
        ht = T("half-time", 30, YELLOW).move_to(P(pl.X(4), pl.y0 - .82))
        self.play(Transform(sec, ht), run_time=.8)
        self.play(Indicate(sec, color=YELLOW, scale_factor=1.12), run_time=.8)
        self.finish()


class S10Model(SpokenScene):
    def construct(self):
        f = Frap(-4.15, 0., .72, bleached=True)
        for b in f.blocks[:6]:
            b.lit = b.lt = 1.0
        for b in f.blocks[:6]:
            b.lit = b.lt = 0.0
        for i, j in ((0, 6), (1, 7), (2, 8), (3, 9)):
            pass
        pl = Plot(.9, 6.4, -2.7, 2.2, 0, 16)
        ax = pl.axes()
        cur = pl.curve(0, 16)
        tag = schematic_tag().to_corner(DL, buff=.26)
        self.add(f.group, ax, cur, tag)
        self.at("diffusion model")
        c1 = chip("spot size", TEXT, size=28)
        plus = T("+", 34, TEXT)
        c2 = chip("half-time", TEXT, size=28)
        arr1 = Arrow(LEFT * .4, RIGHT * .4, buff=0, color=TEXT, stroke_width=5)
        box = chip("diffusion model", YELLOW, size=28)
        arr2 = Arrow(LEFT * .4, RIGHT * .4, buff=0, color=TEXT, stroke_width=5)
        out = chip("approximate D", GREEN, size=28)
        flow = VGroup(c1, plus, c2, arr1, box, arr2, out).arrange(RIGHT, buff=.22)
        fit(flow, max_w=13.2)
        flow.move_to(P(0, 3.3))
        ruler = VGroup(Line(f.c() + LEFT * 1.25 * .72, f.c() + RIGHT * 1.25 * .72, color=YELLOW, stroke_width=6),
                       Line(f.c() + LEFT * .9 + DOWN * .12, f.c() + LEFT * .9 + UP * .12, color=YELLOW, stroke_width=6),
                       Line(f.c() + RIGHT * .9 + DOWN * .12, f.c() + RIGHT * .9 + UP * .12, color=YELLOW, stroke_width=6))
        self.at("spot size and half time")
        ssz = T("spot size", 28, YELLOW).move_to(P(-4.15, -3.15))
        self.play(Create(ruler), FadeIn(ssz), FadeIn(c1), FadeIn(plus), FadeIn(c2), run_time=1.3)
        self.at("diffusion coefficient")
        self.play(FadeIn(arr1), FadeIn(box), FadeIn(arr2), FadeIn(out), run_time=1.3)
        self.at("the estimate is approximate")
        self.play(Indicate(out, color=GREEN, scale_factor=1.12), run_time=1.0)
        self.wait(1.2)
        self.at("binding or barriers")
        fence = VGroup(*[Line(P(-4.15 + .85, y), P(-4.15 + .85, y + .3), color=ORANGE, stroke_width=8)
                         for y in np.linspace(-1.5, 1.5, 6)])
        tether = Line(f.blocks[9].get_center(), f.blocks[9].get_center() + P(-.5, -.7), color=ORANGE, stroke_width=6)
        self.play(Create(fence), Create(tether), run_time=1.0)
        self.at("change recovery")
        alt = pl.curve(0, 16, color=ORANGE, f=lambda t: 20 + 45 * (1 - 2 ** (-t / 6.0)))
        warn = chip("check assumptions", ORANGE, size=28).move_to(P(pl.X(8.2), pl.Y(24)))
        self.play(Create(alt), FadeIn(warn), run_time=1.5)
        self.finish()


def _pblock(x, y, size=.5):
    b = Square(side_length=size, stroke_width=7, stroke_color=TEXT, fill_color=BLUE, fill_opacity=.95)
    b.x0, b.tx, b.y, b.ty, b.lit, b.lt, b.tt = x, x, y, y, 1., 1., 0.

    def upd(m, dt):
        m.tt += dt
        m.x0 += (m.tx - m.x0) * min(1, dt * 1.2)
        m.y += (m.ty - m.y) * min(1, dt * 1.2)
        m.lit += (m.lt - m.lit) * min(1, dt * 2.5)
        m.move_to(P(m.x0 + .25 * math.sin(.9 * m.tt), m.y))
        m.set_stroke(TEXT, width=7, opacity=max(0., min(1., m.lit)))
    b.add_updater(upd)
    return b


class S11Return(SpokenScene):
    def construct(self):
        bg = membrane_bg(29)
        A, W = .3, .9
        outer = [lip("PC", PC_C, -6.2, OUT_Y, A=A, w=W), lip("PC", PC_C, -2.6, OUT_Y, A=A, w=W),
                 lip("PC", PC_C, -.9, OUT_Y, A=A, w=W)]
        inner = [lip("PE", PE_C, -6.4, IN_Y, A=A, w=W), lip("PS", PS_C, -2.8, IN_Y, A=A, w=W),
                 lip("PS", PS_C, .9, IN_Y, A=A, w=W), lip("PE", PE_C, 2.4, IN_Y, A=A, w=W),
                 lip("PS", PS_C, 6.3, IN_Y, A=A, w=W)]
        blocks = [_pblock(3.3, OUT_Y, .6), _pblock(4.6, OUT_Y, .6), _pblock(5.9, OUT_Y, .6)]
        self.add(bg, *outer, *inner, *blocks, face_labels(), schematic_tag())
        self.at("components move")
        self.play(pulse(VGroup(*outer), LUMEN, 1.08), pulse(VGroup(*inner), CYTO, 1.08), run_time=1.2)
        self.at("fast crossing")
        v = DoubleArrow(P(-4.0, -2.3), P(-4.0, 2.3), buff=0, color=TEXT, stroke_width=6)
        vl = T("fast crossing: machine", 30, TEXT).move_to(P(-1.2, 3.05))
        self.play(GrowFromCenter(v), FadeIn(vl), run_time=1.0)
        self.at("sideways motion")
        h = DoubleArrow(P(-4.6, -2.5), P(4.4, -2.5), buff=0, color=LUMEN, stroke_width=6)
        hl = T("free diffusion", 30, LUMEN).move_to(P(-.2, -3.1))
        self.play(GrowFromCenter(h), FadeIn(hl), run_time=1.0)
        self.at("pumps build")
        self.play(FadeOut(VGroup(v, vl, h, hl)), run_time=.4)
        fl = Machine(-4.6, "flippase", vx=0)
        psl = lip("PS", PS_C, -4.6, OUT_Y, A=A, w=W)
        atpc = lip("ATP", PURPLE, -4.6, -3.5, size=28)
        atpc.ty = -2.65
        self.play(FadeIn(fl), FadeIn(psl), FadeIn(atpc), run_time=.6)
        psl.ty = IN_Y
        self.wait(1.0)
        self.play(FadeOut(atpc), run_time=.3)
        self.at("erase it")
        sc = Machine(0.0, "scramblase", vx=0, sw=4.6)
        sc.set_kind("scramblase", on=True)
        self.play(FadeIn(sc), run_time=.6)
        outer[2].ty = IN_Y                    # PC at -0.9 down
        inner[2].ty = OUT_Y                   # PS at 0.9 up
        self.wait(.7)
        self.at("frap measures")
        ring = Circle(radius=.8, stroke_color=RED, stroke_width=5).move_to(P(4.6, OUT_Y))
        self.play(Create(ring), run_time=.4)
        blocks[1].lt = 0.
        self.wait(.5)
        blocks[0].tx, blocks[0].ty = 4.6, OUT_Y + .25       # bright neighbour slides in
        blocks[1].tx, blocks[1].ty = 3.3, OUT_Y - .25
        blocks[0].lt = 1.0
        self.wait(.9)
        self.at("lateral diffusion")
        self.play(FadeOut(ring), Indicate(VGroup(*blocks), color=TEXT, scale_factor=1.12), run_time=1.1)
        self.finish()


class S12End(EndCard):
    LINE = "Fast crossing needs a machine; sliding sideways does not."
