"""Look Alike, Far Apart  (Biochemistrypedia explainer, lesson: Microbes, Protists and Fungi)

COLOUR MAP (fixed for the whole film)
  BLUE   = bacteria (E. coli, Bacillus)
  ORANGE = archaea (methanogens, Asgard)
  GREEN  = eukaryotes (yeast)
  WHITE  = ribosomal RNA (ribbon of beads)
  YELLOW = shared pieces / score / the thing being measured
  RED    = changes (mutations), the 'absence' word, the 'no' stamps
  GREY   = cells before we know what they are
Trees and the score grid are schematic (not computed from data) and say so on screen.
No molecule is drawn.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58BC0"
FIELD_BG = "#26304a"
WH = "#FFFFFF"
CA = [-1.8, 0.3, 0]
CB = [1.8, 0.3, 0]


# ------------------------------------------------------------------ helpers
def motes(scene, n=26, seed=1):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.03, 0.07), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.18, 0.4))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.1, 0.35))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.1:
                m.shift(DOWN * 8.2)
            if abs(m.get_x()) > 7.2:
                m.shift(LEFT * 14.4 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-10)
    scene.add(g)
    return g


def capsule(color, w=2.4, h=1.1, fill=0.28, sw=4):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill)


def icon(color, w=1.1, h=0.55):
    return capsule(color, w, h, 0.5, 4)


def bob(m, amp=0.09, sp=0.9, ph=0.0, rot=0.0):
    m._t = ph
    m._last = np.zeros(3)

    def f(mm, dt):
        mm._t += dt * sp
        new = np.array([amp * math.sin(mm._t * 1.3), amp * math.cos(mm._t), 0.0])
        mm.shift(new - mm._last)
        mm._last = new
        if rot:
            mm.rotate(rot * dt * math.cos(mm._t * 0.8))
    m.add_updater(f)
    return m


def pulse(m, base=1.0, amp=0.08, sp=2.0):
    m._pt = 0.0
    m._ps = 1.0

    def f(mm, dt):
        mm._pt += dt * sp
        s = base + amp * math.sin(mm._pt)
        mm.scale(s / mm._ps)
        mm._ps = s
    m.add_updater(f)
    return m


def pl_partial(pts, f):
    pts = [np.array(p, float) for p in pts]
    L = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
    d = max(1e-3, min(1.0, f)) * sum(L)
    out = [pts[0]]
    for i, l in enumerate(L):
        if d >= l:
            out.append(pts[i + 1])
            d -= l
        else:
            out.append(pts[i] + (pts[i + 1] - pts[i]) * (d / l))
            break
    if len(out) < 2:
        out.append(pts[0] + np.array([1e-3, 0, 0]))
    return out


def pl_point(pts, f):
    return pl_partial(pts, f)[-1]


def grow_line(pts, tr, color=TEXT, sw=11):
    m = VMobject(stroke_color=color, stroke_width=sw)

    def upd(mm):
        mm.set_points_as_corners(pl_partial(pts, tr.get_value()))
    m.add_updater(upd)
    upd(m)
    return m


def darrow(a, b, color=YELLOW, sw=5):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    ang = math.atan2(d[1], d[0])
    end = b - d / np.linalg.norm(d) * 0.1
    line = DashedLine(a, end, dash_length=0.18, color=color, stroke_width=sw)
    tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=1).scale(0.17)
    tri.rotate(ang - PI / 2).move_to(b - d / np.linalg.norm(d) * 0.12)
    return VGroup(line, tri)


def seg(a, b, color=TEXT, sw=11):
    return Line(a, b, stroke_color=color, stroke_width=sw)


def scissors():
    l1 = Line([-0.35, 0.45, 0], [0.35, -0.45, 0], stroke_color=YELLOW, stroke_width=6)
    l2 = Line([-0.35, -0.45, 0], [0.35, 0.45, 0], stroke_color=YELLOW, stroke_width=6)
    r1 = Circle(radius=0.14, stroke_color=YELLOW, stroke_width=5).move_to([0.45, -0.55, 0])
    r2 = Circle(radius=0.14, stroke_color=YELLOW, stroke_width=5).move_to([-0.45, -0.55, 0])
    g = VGroup(l1, l2, r1, r2)
    g.rotate(PI)  # blades point down
    return g


def check():
    return VMobject(stroke_color=GREEN, stroke_width=9).set_points_as_corners([[-0.3, 0, 0], [-0.1, -0.25, 0], [0.32, 0.3, 0]])


def cross():
    return VGroup(Line([-0.28, 0.28, 0], [0.28, -0.28, 0], stroke_color=RED, stroke_width=9),
                  Line([-0.28, -0.28, 0], [0.28, 0.28, 0], stroke_color=RED, stroke_width=9))


class Ribbon(VGroup):
    """A white ribbon of beads that wiggles gently. p = how much has unspooled, gap = pieces pulled apart."""

    def __init__(self, x0, x1, y, n=44, amp=0.22, freq=1.7, color=WH, r=0.075, speed=1.0, nseg=8, p=1.0):
        super().__init__(*[Dot(radius=r, color=color) for _ in range(n)])
        self.x0, self.x1, self.y0, self.n, self.amp, self.freq, self.sp, self.nseg = x0, x1, y, n, amp, freq, speed, nseg
        self.base = color
        self.p = ValueTracker(p)
        self.gap = ValueTracker(0.0)
        self.t = random.random() * 6
        self.vis = [None] * n
        self.add_updater(lambda m, dt: m._step(dt))
        self._step(0)

    def _step(self, dt):
        self.t += dt
        p = self.p.get_value()
        g = self.gap.get_value()
        for i, d in enumerate(self.submobjects):
            u = i / (self.n - 1)
            x = self.x0 + (self.x1 - self.x0) * u
            y = self.y0 + self.amp * math.sin(self.freq * x + self.t * self.sp * 2.2)
            sg = min(self.nseg - 1, int(u * self.nseg))
            y += g * 0.11 * (1 if sg % 2 == 0 else -1)
            x += g * 0.1 * (sg - (self.nseg - 1) / 2)
            d.move_to([x, y, 0])
            v = u <= p + 1e-9
            if v != self.vis[i]:
                d.set_opacity(1 if v else 0)
                self.vis[i] = v

    def highlight(self, segs, color=YELLOW):
        for i, d in enumerate(self.submobjects):
            sg = min(self.nseg - 1, int(i / (self.n - 1) * self.nseg))
            d.set_color(color if sg in segs else self.base)


def cow():
    body = RoundedRectangle(corner_radius=0.2, width=1.5, height=0.8, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15)
    head = Ellipse(width=0.55, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15).move_to([-0.95, 0.2, 0])
    spots = VGroup(Ellipse(width=0.4, height=0.28, fill_color=GREY, fill_opacity=0.7, stroke_width=0).move_to([-0.1, 0.1, 0]),
                   Ellipse(width=0.3, height=0.22, fill_color=GREY, fill_opacity=0.7, stroke_width=0).move_to([0.4, -0.1, 0]))
    legs = VGroup(*[Line([x, -0.4, 0], [x, -0.85, 0], stroke_color=TEXT, stroke_width=4) for x in (-0.55, -0.25, 0.25, 0.55)])
    tail = Line([0.75, 0.2, 0], [0.95, -0.2, 0], stroke_color=TEXT, stroke_width=3)
    return VGroup(legs, tail, body, head, spots)


def microscope(label_cells=True):
    field = Circle(radius=3.55, stroke_color=GREY, stroke_width=4, fill_color=FIELD_BG, fill_opacity=1).move_to([0, -0.1, 0])
    ca = capsule(GREY, 3.0, 1.5, 0.45).move_to(CA)
    cb = capsule(GREY, 3.0, 1.5, 0.45).move_to(CB)
    la = T("methanogen", 34).move_to([CA[0], -1.2, 0])
    lb = T("E. coli", 34).move_to([CB[0], -1.2, 0])
    bob(ca, 0.14, 1.0, 0)
    bob(cb, 0.14, 1.1, 2)
    return field, ca, cb, la, lb


# ---- the score grid (schematic) and the first tree
ORDER = [ORANGE, ORANGE, BLUE, BLUE, GREEN]
SCORE = np.array([[1.0, 0.85, 0.30, 0.28, 0.22],
                  [0.85, 1.0, 0.31, 0.27, 0.24],
                  [0.30, 0.31, 1.0, 0.80, 0.21],
                  [0.28, 0.27, 0.80, 1.0, 0.23],
                  [0.22, 0.24, 0.21, 0.23, 1.0]])


def grid_cell_xy(i, j):
    return [-5.5 + 1.0 * (j + 0.5), 2.4 - 1.0 * (i + 0.5), 0]


def build_grid(filled=True):
    cells = VGroup()
    for i in range(5):
        for j in range(5):
            s = Square(side_length=0.95, stroke_color=GREY, stroke_width=1.5, fill_color=WH,
                       fill_opacity=(0.1 + 0.75 * SCORE[i][j]) if filled else 0.0).move_to(grid_cell_xy(i, j))
            cells.add(s)
    icons = VGroup()
    for k, c in enumerate(ORDER):
        icons.add(icon(c, 0.8, 0.4).move_to([grid_cell_xy(0, k)[0], 3.1, 0]))
        icons.add(icon(c, 0.8, 0.4).move_to([-6.2, grid_cell_xy(k, 0)[1], 0]))
    sch = T("schematic", 22, GREY).move_to([-3.0, -3.2, 0])
    return cells, icons, sch


T6 = dict(A=[2.0, 0, 0], Y=[3.3, 0, 0], B=[4.6, 0, 0],
          m1=[1.3, 1.7, 0], m2=[1.3, -1.7, 0], e=[5.5, 1.7, 0], b=[5.5, -1.7, 0], y=[3.3, -2.4, 0])


def tree6_lines(with_m=True):
    L = [seg(T6["Y"], T6["B"]), seg(T6["B"], T6["e"]), seg(T6["B"], T6["b"]), seg(T6["Y"], T6["y"])]
    if with_m:
        L += [seg(T6["A"], T6["Y"]), seg(T6["A"], T6["m1"]), seg(T6["A"], T6["m2"])]
    return L


def tree6_tips(with_m=True):
    tips = {"e": icon(BLUE).move_to(T6["e"]), "b": icon(BLUE).move_to(T6["b"]), "y": icon(GREEN).move_to(T6["y"])}
    if with_m:
        tips["m1"] = icon(ORANGE).move_to(T6["m1"])
        tips["m2"] = icon(ORANGE).move_to(T6["m2"])
    return tips


# ---- predict scene (also reused by the pause)
MF = [[0.9, 2.8, 0], [2.7, 2.8, 0]]


def predict_world(full=True):
    lines = VGroup(*tree6_lines(False))
    tips = tree6_tips(False)
    m1 = icon(ORANGE).move_to(MF[0])
    m2 = icon(ORANGE).move_to(MF[1])
    bob(m1, 0.2, 1.5, 0)
    bob(m2, 0.2, 1.7, 1.5)
    q = T("Where do the\nmethanogens\nland?", 46, TEXT, weight=BOLD).move_to([-3.3, 0.2, 0])
    a1 = darrow([2.9, 2.55, 0], [4.9, 2.25, 0])
    a2 = darrow([1.1, 2.4, 0], [0.2, 1.3, 0])
    qm = T("?", 60, YELLOW).move_to([-0.2, 0.9, 0])
    pulse(qm, 1.0, 0.15, 3.0)
    return lines, tips, m1, m2, q, a1, a2, qm


# ---- Y tree (three domains)
YC = np.array([1.4, 0.2, 0])
YP = dict(C=[1.4, 0.2, 0], NA=[1.4, 1.9, 0], NB=[3.2, 0.2, 0],
          m1=[0.5, 3.0, 0], m2=[2.4, 3.0, 0], b1=[4.2, 1.4, 0], b2=[4.2, -1.0, 0], eu=[1.4, -3.0, 0])


def ytree(opacity=1.0):
    P = YP
    lines = VGroup(seg(P["C"], P["NA"], ORANGE), seg(P["NA"], P["m1"], ORANGE), seg(P["NA"], P["m2"], ORANGE),
                   seg(P["C"], P["NB"], BLUE), seg(P["NB"], P["b1"], BLUE), seg(P["NB"], P["b2"], BLUE),
                   seg(P["C"], P["eu"], GREEN))
    tips = VGroup(icon(ORANGE).move_to(P["m1"]), icon(ORANGE).move_to(P["m2"]), icon(BLUE).move_to(P["b1"]),
                  icon(BLUE).move_to(P["b2"]), icon(GREEN).move_to(P["eu"]))
    g = VGroup(lines, tips)
    if opacity < 1:
        g.set_opacity(opacity)
    return lines, tips, g


def ylabels():
    return (T("Archaea", 34, ORANGE).move_to([4.2, 2.9, 0]),
            T("Bacteria", 34, BLUE).move_to([5.9, 0.2, 0]),
            T("Eukarya", 34, GREEN).move_to([3.4, -3.0, 0]))


# ---- 2020s tree
T13 = dict(S=[0.0, -0.2, 0], Nb=[-2.2, -0.2, 0], Na=[2.0, -0.2, 0], Nag=[2.8, 0.9, 0],
           b1=[-3.6, 1.0, 0], b2=[-3.6, -1.4, 0],
           a1=[3.9, 2.6, 0], a2=[4.5, 2.0, 0], a3=[3.9, 1.4, 0], o1=[4.0, -1.2, 0], o2=[3.6, -2.2, 0], g=[5.3, 0.2, 0])


def tree13(opacity=1.0, green=True):
    P = T13
    lines = VGroup(seg(P["Nb"], P["S"], BLUE), seg(P["S"], P["Na"], ORANGE),
                   seg(P["Nb"], P["b1"], BLUE), seg(P["Nb"], P["b2"], BLUE),
                   seg(P["Na"], P["Nag"], ORANGE), seg(P["Nag"], P["a1"], ORANGE), seg(P["Nag"], P["a2"], ORANGE),
                   seg(P["Nag"], P["a3"], ORANGE), seg(P["Na"], P["o1"], ORANGE), seg(P["Na"], P["o2"], ORANGE))
    tips = VGroup(icon(BLUE).move_to(P["b1"]), icon(BLUE).move_to(P["b2"]),
                  *[icon(ORANGE).move_to(P[k]) for k in ("a1", "a2", "a3", "o1", "o2")])
    g = VGroup(lines, tips)
    gl = VGroup()
    if green:
        gl = VGroup(seg(P["Nag"], P["g"], GREEN), icon(GREEN).move_to(P["g"]))
        g.add(gl)
    if opacity < 1:
        g.set_opacity(opacity)
    return g, lines, tips, gl


# =================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Microbes, Protists and Fungi"
    TITLE = "Look Alike, Far Apart"


class S01Puzzle(SpokenScene):
    def construct(self):
        motes(self)
        field, ca, cb, la, lb = microscope()
        self.play(FadeIn(field), FadeIn(ca), FadeIn(cb), run_time=1.0)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.7)
        self.at("look almost the same")
        self.play(Indicate(ca, scale_factor=1.08, color=GREY), Indicate(cb, scale_factor=1.08, color=GREY), run_time=1.6)
        self.at("are they close relatives")
        q = T("?", 110, WH, weight=BOLD).move_to([0, 2.0, 0])
        pulse(q, 1.0, 0.12, 3.0)
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.at("both are small cells")
        dn = [DashedVMobject(Ellipse(width=1.0, height=0.75, stroke_color=TEXT, stroke_width=3), num_dashes=20).move_to([x - 0.5, 0.3, 0]) for x in (CA[0], CB[0])]
        self.play(*[Create(d) for d in dn], run_time=1.4)
        self.at("with no nucleus")
        nn = T("no nucleus", 34, WH).move_to([0, -2.3, 0])
        self.play(FadeOut(VGroup(*dn)), FadeIn(nn), run_time=1.2)
        self.at("methanogen makes methane")
        cw = cow().scale(1.7).move_to([-4.6, 2.5, 0])
        self.play(FadeIn(cw, shift=DOWN * 0.2), run_time=1.2)
        self.at("lives in a")
        lab = T("from a\ncow's rumen", 34, TEXT).move_to([-5.3, 0.6, 0])
        self.play(FadeIn(lab), run_time=0.5)
        ar = Arrow([-3.8, 0.5, 0], [-3.3, 0.4, 0], buff=0.05, color=ORANGE, stroke_width=6)
        self.play(GrowArrow(ar), run_time=1.0)
        self.finish()


class S02Absence(SpokenScene):
    def construct(self):
        motes(self)
        field, ca, cb, la, lb = microscope()
        self.add(field, ca, cb, la, lb)
        box = RoundedRectangle(corner_radius=0.3, width=10.0, height=4.4, stroke_color=TEXT, stroke_width=6, fill_color="#26304a", fill_opacity=0.9).move_to([0, 0.3, 0])
        box.set_z_index(-3)
        title = VGroup(T("prokaryotes:", 40), T("no", 40, RED, weight=BOLD), T("nucleus", 40)).arrange(RIGHT, buff=0.25).move_to([0, 3.15, 0])
        pulse(title[1], 1.0, 0.12, 3.0)
        self.at("lumped all cells")
        self.play(FadeOut(field), Create(box), run_time=1.6)
        self.at("prokaryotes")
        self.play(FadeIn(title), run_time=1.0)
        self.at("but that grouping")
        glow = Circle(radius=0.42, stroke_color=RED, stroke_width=5).move_to(title[1])
        self.play(Indicate(title[1], color=RED, scale_factor=1.5), Create(glow), run_time=1.6)
        self.at("something missing")
        self.play(glow.animate.scale(1.5).set_opacity(0), run_time=1.0)
        self.at("two cells can both lack")
        crack = VMobject(stroke_color=RED, stroke_width=7).set_points_as_corners(
            [[0, -1.9, 0], [0.22, -1.4, 0], [-0.2, -0.8, 0], [0.18, -0.2, 0], [-0.1, 0.4, 0]])
        self.play(Create(crack), run_time=1.5)
        self.at("still be distant")
        self.play(ca.animate.shift(LEFT * 1.0), la.animate.shift(LEFT * 1.0), cb.animate.shift(RIGHT * 1.0),
                  lb.animate.shift(RIGHT * 1.0), FadeOut(crack), run_time=1.6)
        self.at("relatives")
        rel = T("related?", 40, YELLOW, weight=BOLD).move_to([0, 0.3, 0])
        self.play(FadeIn(rel, scale=0.7), run_time=0.8)
        self.finish()


class S03Molecule(SpokenScene):
    def construct(self):
        motes(self)
        ca = capsule(GREY, 3.0, 1.5, 0.45).move_to([CA[0] - 1.0, 0.3, 0])
        cb = capsule(GREY, 3.0, 1.5, 0.45).move_to([CB[0] + 1.0, 0.3, 0])
        self.add(ca, cb)
        big = capsule("#3a4766", 13.2, 7.0, 0.35, 5)
        card = chip("Carl Woese", GOLD, 38).move_to([2.4, -2.4, 0])
        self.play(FadeOut(cb), Transform(ca, big), FadeIn(card, shift=UP * 0.2), run_time=1.2)
        self.at("looked for a part")
        large = Ellipse(width=4.4, height=3.0, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.35).move_to([-3.8, -0.9, 0])
        small = Ellipse(width=3.0, height=2.0, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.35).move_to([-3.8, 1.3, 0])
        ribo = VGroup(large, small)
        bob(ribo, 0.07, 0.8, 0.5)
        self.play(FadeIn(ribo, scale=0.6), run_time=1.5)
        self.at("chose the ribosome")
        rl = T("ribosome", 38, TEAL).move_to([-3.8, -2.8, 0])
        self.play(FadeIn(rl), run_time=0.7)
        self.at("particle that makes")
        self.play(Indicate(large, color=TEAL, scale_factor=1.08), run_time=1.8)
        self.at("inside its small subunit")
        sl = T("small subunit", 34, TEAL).move_to([-3.8, 2.85, 0])
        self.play(small.animate.set_fill(TEAL, 0.75), FadeIn(sl), run_time=1.0)
        self.at("strand of RNA")
        rib = Ribbon(-2.2, 6.0, 1.3, n=60, amp=0.35, freq=1.3, r=0.12, p=0)
        self.add(rib)
        self.play(rib.p.animate.set_value(1), run_time=2.0, rate_func=linear)
        rt = T("small-subunit\nribosomal RNA", 36, WH).move_to([2.2, 2.65, 0])
        self.play(FadeIn(rt), run_time=0.8)
        self.finish()


class S04Compare(SpokenScene):
    def construct(self):
        motes(self)
        rows = [("methanogen 1", ORANGE), ("methanogen 2", ORANGE), ("E. coli", BLUE), ("Bacillus", BLUE), ("yeast", GREEN)]
        ys = [2.8, 1.4, 0, -1.4, -2.8]
        ribs = []
        for (nm, c), y in zip(rows, ys):
            ic = icon(c, 0.7, 0.34).move_to([-6.25, y, 0])
            lb = T(nm, 28, c).move_to([-5.75, y, 0], aligned_edge=LEFT)
            rb = Ribbon(-2.4, 3.6, y, n=44, amp=0.2, freq=2.2, r=0.105, p=0)
            self.add(rb)
            ribs.append(rb)
            self.play(FadeIn(ic), FadeIn(lb), rb.p.animate.set_value(1), run_time=1.15, rate_func=linear)
        sch = T("schematic", 22, GREY).move_to([5.6, -3.4, 0])
        self.add(sch)
        self.at("they cut each strand")
        sc = scissors().move_to([0.6, 3.5, 0])
        self.add(sc)
        gs = [r.gap.animate.set_value(1.0) for r in ribs]
        self.play(sc.animate.move_to([0.6, -3.4, 0]), *gs, run_time=2.4, rate_func=linear)
        self.play(FadeOut(sc), run_time=0.3)
        self.at("compared the pieces")

        def pair(i, j, segs, mid_label):
            yi, yj = ys[i], ys[j]
            br = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_as_corners(
                [[3.85, yi, 0], [4.15, yi, 0], [4.15, yj, 0], [3.85, yj, 0]])
            my = (yi + yj) / 2
            cnt = ValueTracker(0)
            num = always_redraw(lambda: M(str(int(round(cnt.get_value()))), 56, YELLOW).move_to([5.5, my, 0]))
            self.play(Create(br), FadeIn(num), run_time=0.6)
            return br, num, cnt

        br, num, cnt = pair(0, 1, None, None)
        done = []
        for k in [0, 1, 2, 4, 5, 7]:
            done.append(k)
            ribs[0].highlight(done)
            ribs[1].highlight(done)
            self.play(cnt.animate.set_value(len(done)), run_time=0.45)
        self.at("each pair got")
        sl = T("similarity score", 28, YELLOW).move_to([5.1, 3.45, 0])
        self.play(FadeIn(sl), run_time=0.7)
        self.at("similarity score")
        self.wait(0.5)
        ribs[0].highlight([])
        ribs[1].highlight([])
        self.play(FadeOut(br), FadeOut(num), run_time=0.3)
        br2, num2, cnt2 = pair(0, 2, None, None)
        done = []
        for k in [3, 6]:
            done.append(k)
            ribs[0].highlight(done)
            ribs[2].highlight(done)
            self.play(cnt2.animate.set_value(len(done)), run_time=0.4)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        motes(self)
        root = Ribbon(-6.4, -4.4, 0, n=14, amp=0.14, freq=2.4, r=0.13, p=0)
        self.add(root)
        P = ValueTracker(0)
        up = [[-4.4, 0, 0], [-3.2, 2.0, 0], [2.4, 2.0, 0]]
        lo = [[-4.4, 0, 0], [-3.2, -2.0, 0], [2.4, -2.0, 0]]
        bu, bl = grow_line(up, P), grow_line(lo, P)
        self.add(bu, bl)
        dots = VGroup()
        for pts, fr in ((up, [0.25, 0.4, 0.55, 0.7, 0.82, 0.95]), (lo, [0.15, 0.25, 0.36, 0.46, 0.57, 0.68, 0.78, 0.88, 0.96])):
            for f in fr:
                d = Dot(radius=0.2, color=RED).move_to(pl_point(pts, f))
                d.f = f
                d.add_updater(lambda m: m.set_opacity(float(np.clip((P.get_value() - m.f) / 0.04, 0, 1))))
                dots.add(d)
        self.add(dots)
        track = seg([-4.4, -3.0, 0], [2.4, -3.0, 0], GREY, 5)
        knob = Dot(radius=0.22, color=YELLOW)
        knob.add_updater(lambda m: m.move_to([-4.4 + 6.8 * P.get_value(), -3.0, 0]))
        sl = T("time since common ancestor", 28, YELLOW).move_to([-1.0, -3.55, 0])
        self.play(root.p.animate.set_value(1), run_time=1.3, rate_func=linear)
        self.play(FadeIn(track), FadeIn(knob), FadeIn(sl), P.animate.set_value(0.1), run_time=1.2, rate_func=linear)
        self.at("small changes pile up")
        rt = max(0.5, self.t_of("so fewer differences") - 0.2 - self.elapsed())
        self.play(P.animate.set_value(0.8), run_time=rt, rate_func=linear)
        rule = VGroup(T("fewer differences:", 28, YELLOW, weight=BOLD), T("usually a more recent", 28, TEXT), T("common ancestor", 28, TEXT)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.85, 0, 0])
        rt2 = max(0.5, self.narration_s - self.elapsed())
        self.play(FadeIn(rule, shift=LEFT * 0.3), P.animate.set_value(1.0), run_time=rt2, rate_func=linear)
        self.finish()


class S06Grid(SpokenScene):
    def construct(self):
        motes(self)
        cells, icons, sch = build_grid(filled=False)
        self.play(FadeIn(icons), FadeIn(cells), FadeIn(sch), run_time=1.0)
        self.at("scores fill a grid")
        anims = []
        order = [(i, j) for d in range(9) for i in range(5) for j in range(5) if i + j == d]
        for (i, j) in order:
            anims.append(cells[i * 5 + j].animate.set_fill(WH, 0.1 + 0.75 * SCORE[i][j]))
        self.play(LaggedStart(*anims, lag_ratio=0.12), run_time=3.3)
        self.at("a stated grouping method")
        lines = tree6_lines(True)
        tips = tree6_tips(True)
        for tp in tips.values():
            bob(tp, 0.07, 0.9, random.random() * 5)
        self.play(*[Create(l) for l in lines[4:7]], FadeIn(tips["m1"]), FadeIn(tips["m2"]), Create(lines[0]), run_time=1.3)
        self.at("propose a tree")
        self.play(Create(lines[1]), Create(lines[2]), Create(lines[3]),
                  FadeIn(tips["e"]), FadeIn(tips["b"]), FadeIn(tips["y"]), run_time=1.6)
        lab = T("proposed by a grouping method", 30, TEXT).move_to([3.4, -3.4, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("different methods make different assumptions")
        tag = T("other methods, other assumptions", 30, YELLOW).move_to([3.4, 3.3, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=1.0)
        self.at("so the grid alone")
        self.play(*[Indicate(cells[k], color=YELLOW, scale_factor=1.0) for k in (1, 5, 7, 11, 13, 17)], run_time=2.0)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        motes(self)
        cells, icons, sch = build_grid(filled=True)
        lines = VGroup(*tree6_lines(True))
        tips = tree6_tips(True)
        self.add(cells, icons, sch, lines, *tips.values())
        lines_p, tips_p, m1, m2, q, a1, a2, qm = predict_world()
        # grid fades, tree sheds the methanogen side while the methanogen tips lift off
        self.play(FadeOut(cells), FadeOut(icons), FadeOut(sch),
                  FadeOut(VGroup(lines[4], lines[5], lines[6])),
                  tips["m1"].animate.move_to(MF[0]), tips["m2"].animate.move_to(MF[1]), run_time=1.8)
        self.remove(tips["m1"], tips["m2"])
        self.add(m1, m2)
        self.at("where do you think")
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=1.0)
        self.at("close to")
        self.play(Create(a1), run_time=1.0)
        self.at("or somewhere else")
        self.play(Create(a2), FadeIn(qm, scale=0.5), run_time=1.0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        motes(self)
        lines, tips, m1, m2, q, a1, a2, qm = predict_world()
        self.add(lines, *tips.values(), m1, m2, q, a1, a2, qm)
        ring_bg = Circle(radius=0.55, stroke_color=GREY, stroke_width=5).move_to([6.0, 3.1, 0])
        pulse(ring_bg, 1.0, 0.15, 4.0)
        bars = VGroup(Rectangle(width=0.1, height=0.4, fill_color=TEXT, fill_opacity=1, stroke_width=0).move_to([5.9, 3.1, 0]),
                      Rectangle(width=0.1, height=0.4, fill_color=TEXT, fill_opacity=1, stroke_width=0).move_to([6.1, 3.1, 0]))
        tr = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=2 * PI * max(tr.get_value(), 0.001), stroke_color=YELLOW, stroke_width=7, arc_center=[6.0, 3.1, 0]))
        self.add(ring_bg, bars, arc)
        self.play(tr.animate.set_value(0.0), run_time=4.9, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        motes(self)
        lines, tips, m1, m2, q, a1, a2, qm = predict_world()
        self.add(lines, *tips.values(), m1, m2, q, a1, a2, qm)
        # the wrong guess is crossed out
        x = cross().scale(1.2).move_to([4.9, 1.9, 0])
        self.play(FadeOut(q), FadeOut(a2), FadeOut(qm), a1.animate.set_opacity(0.35), Create(x), run_time=1.6)
        self.at("and George Fox")
        yr = T("1977: Woese and Fox", 34, GOLD).move_to([-3.6, 3.2, 0])
        self.play(FadeIn(yr, shift=DOWN * 0.2), run_time=0.9)
        self.at("formed their own group")
        yl, yt, yg = ytree()
        ytips = {"m1": m1, "m2": m2, "e": tips["e"], "b": tips["b"], "y": tips["y"]}
        tgt = {"m1": YP["m1"], "m2": YP["m2"], "e": YP["b1"], "b": YP["b2"], "y": YP["eu"]}
        self.play(FadeOut(lines), FadeOut(a1), FadeOut(x),
                  *[ytips[k].animate.move_to(tgt[k]) for k in ytips],
                  *[Create(l) for l in yl], run_time=2.4)
        self.at("it sat about")
        P = YP

        def bar(y):
            return VGroup(seg([-5.6, y, 0], [-1.6, y, 0], YELLOW, 7), seg([-5.6, y - 0.2, 0], [-5.6, y + 0.2, 0], YELLOW, 6),
                          seg([-1.6, y - 0.2, 0], [-1.6, y + 0.2, 0], YELLOW, 6))
        la = T("archaea to bacteria", 30, TEXT).move_to([-3.6, 1.45, 0])
        b1 = bar(0.9)
        p1 = VMobject(stroke_color=YELLOW, stroke_width=11).set_points_as_corners([P["m1"], P["NA"], P["C"], P["NB"], P["b1"]])
        p1.set_stroke(opacity=0.85)
        self.play(FadeIn(la), Create(p1), run_time=1.0)
        self.play(Create(b1), run_time=0.6)
        self.at("as from eukaryotes")
        self.play(FadeOut(p1), run_time=0.3)
        lb = T("archaea to eukaryotes", 30, TEXT).move_to([-3.6, -0.4, 0])
        b2 = bar(-0.95)
        p2 = VMobject(stroke_color=YELLOW, stroke_width=11).set_points_as_corners([P["m1"], P["NA"], P["C"], P["eu"]])
        p2.set_stroke(opacity=0.85)
        self.play(FadeIn(lb), Create(p2), run_time=0.9)
        self.play(Create(b2), run_time=0.6)
        self.at("the cells with a nucleus")
        eq = T("about equal", 38, YELLOW, weight=BOLD).move_to([-3.6, -2.3, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), Indicate(ytips["y"], color=GREEN, scale_factor=1.3), run_time=1.6)
        self.finish()


class S10Domains(SpokenScene):
    def construct(self):
        motes(self)
        yl, yt, yg = ytree()
        for tp in yt:
            bob(tp, 0.06, 0.9, random.random() * 5)
        self.add(yg)
        old = T("archaebacteria", 36, ORANGE).move_to([5.0, 3.0, 0])
        self.at("the new group")
        self.play(FadeIn(old, shift=DOWN * 0.2), Indicate(yt[0], color=ORANGE), Indicate(yt[1], color=ORANGE), run_time=1.6)
        self.at("later")
        la, lb, le = ylabels()
        yr = T("1990", 72, GOLD, weight=BOLD).move_to([-3.6, 1.2, 0])
        who = T("Woese and colleagues", 32, TEXT).move_to([-3.6, 0.1, 0])
        self.play(FadeOut(old), FadeIn(yr, shift=RIGHT * 0.4), FadeIn(who), run_time=1.3)
        self.at("three domains")
        td = T("three domains", 40, YELLOW, weight=BOLD).move_to([-3.6, -1.2, 0])
        self.play(FadeIn(td, shift=UP * 0.2), run_time=0.9)
        self.at("bacteria")
        self.play(Write(lb), run_time=0.9)
        self.at("archaea")
        self.play(Write(la), run_time=0.9)
        self.at("eukarya")
        self.play(Write(le), run_time=0.9)
        self.at("those names")
        self.play(Indicate(la, scale_factor=1.15), Indicate(lb, scale_factor=1.15), Indicate(le, scale_factor=1.15), run_time=1.4)
        self.at("the standard labels")
        self.play(Circumscribe(VGroup(la, lb, le), color=GOLD, stroke_width=4, run_time=1.2))
        self.finish()


class S11Rank(SpokenScene):
    def construct(self):
        motes(self)
        yl, yt, yg = ytree()
        for tp in yt:
            bob(tp, 0.06, 0.9, random.random() * 5)
        la, lb, le = ylabels()
        self.add(yg, la, lb, le)
        self.at("tell us")
        self.wait(0.3)
        self.at("they rank closeness")
        s1 = VGroup(check().move_to([-6.0, 1.6, 0]), T("ranks closeness", 36, GREEN, weight=BOLD).move_to([-5.45, 1.6, 0], aligned_edge=LEFT))
        self.play(FadeIn(s1, scale=1.6), run_time=0.9)
        self.at("do not date a split")
        s2 = VGroup(cross().move_to([-6.0, 0.3, 0]), T("dates a split", 36, RED, weight=BOLD).move_to([-5.45, 0.3, 0], aligned_edge=LEFT))
        self.play(FadeIn(s2, scale=1.6), run_time=0.9)
        self.at("reveal an ancestor")
        s3 = VGroup(cross().move_to([-6.0, -1.0, 0]), T("shows an ancestor", 36, RED, weight=BOLD).move_to([-5.45, -1.0, 0], aligned_edge=LEFT))
        self.play(FadeIn(s3, scale=1.6), run_time=0.9)
        self.play(Indicate(s3, color=RED, scale_factor=1.05), run_time=1.5)
        self.finish()


class S12Deep(SpokenScene):
    def construct(self):
        motes(self)
        yl, yt, yg = ytree()
        la, lb, le = ylabels()
        self.add(yg, la, lb, le)
        C2 = np.array([3.6, 0.4, 0])
        arms = {"o": (ORANGE, np.array([0.0, 1.0, 0])), "b": (BLUE, np.array([math.cos(-PI / 6), math.sin(-PI / 6), 0])),
                "g": (GREEN, np.array([-math.cos(-PI / 6), math.sin(-PI / 6), 0]))}
        amp = ValueTracker(0.12)
        junction = VGroup()
        for k, (col, d) in arms.items():
            for ph in range(3):
                ln = Line(C2, C2 + d * 2.4, stroke_color=col, stroke_width=16 if ph == 0 else 9)
                ln.d, ln.ph = d, ph
                ln.t = 0.0

                def wob(m, dt, col=col):
                    m.t += dt
                    a = amp.get_value()
                    end = C2 + m.d * 2.4 + np.array([a * math.sin(m.t * 1.9 + m.ph * 2.1 + m.d[0] * 3), a * math.cos(m.t * 1.5 + m.ph * 1.7 + m.d[1] * 3), 0])
                    start = C2 + np.array([0.3 * a * math.sin(m.t * 1.3 + m.ph), 0.3 * a * math.cos(m.t * 1.1 + m.ph * 2), 0])
                    m.put_start_and_end_on(start, end)
                ln.add_updater(wob)
                if ph:
                    ln.set_stroke(opacity=0.6)
                junction.add(ln)
        self.play(yg.animate.scale(1.6, about_point=YC).set_opacity(0), FadeOut(VGroup(la, lb, le)), FadeIn(junction), run_time=1.9)
        self.remove(yg)
        self.at("repeated changes at one site")
        rib = Ribbon(-6.2, -1.6, 1.7, n=30, amp=0.15, freq=2.0, r=0.12, p=0)
        self.add(rib)
        rl = T("repeated changes at one site", 30, TEXT).move_to([-3.9, 0.5, 0])
        self.play(rib.p.animate.set_value(1), FadeIn(rl), run_time=0.8, rate_func=linear)
        site = Circle(radius=0.28, stroke_color=YELLOW, stroke_width=6).move_to([-3.9, 1.7, 0])
        stack = VGroup()
        self.play(Create(site), run_time=0.4)
        for i in range(4):
            d = Dot(radius=0.15, color=RED).move_to([-3.9, 2.35 + 0.34 * i, 0])
            stack.add(d)
            self.play(FadeIn(d, shift=DOWN * 0.2), run_time=0.3)
        self.at("blur the signal")
        self.play(amp.animate.set_value(0.45), run_time=2.2, rate_func=linear)
        self.at("many genes")
        cols = [TEAL, PURPLE, PINK, GOLD]
        lab = T("many genes + models of change", 26, TEXT).move_to([-3.9, -0.7, 0])
        self.play(FadeIn(lab), run_time=0.4)
        rs = []
        for k, c in enumerate(cols):
            r = Ribbon(-6.3, -1.6, -1.5 - 0.6 * k, n=34, amp=0.12, freq=2.0, color=c, r=0.1, p=0)
            self.add(r)
            rs.append(r)
        self.play(*[r.p.animate.set_value(1) for r in rs], run_time=1.6, rate_func=linear)
        self.at("sharpen the branching pattern")
        self.play(amp.animate.set_value(0.0), run_time=2.6, rate_func=smooth)
        self.at("which branch came off first")
        tag = VGroup(T("which came first?", 32, YELLOW, weight=BOLD), T("needs an outside reference", 30, TEXT)).arrange(DOWN, buff=0.15).move_to([3.6, -3.0, 0])
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=1.2)
        self.at("needs an outside reference")
        self.play(Indicate(tag[1], color=YELLOW, scale_factor=1.06), run_time=1.5)
        self.finish()


class S13Update(SpokenScene):
    def construct(self):
        motes(self)
        yl, yt, yg = ytree()
        la0, lb0, le0 = ylabels()
        self.add(yg, la0, lb0, le0)
        g, lines, tips, gl = tree13(1.0, green=False)
        for tp in tips:
            bob(tp, 0.06, 0.9, random.random() * 5)
        sch = T("schematic", 22, GREY).move_to([-5.8, -3.5, 0])
        self.at("most recent trees")
        self.play(FadeOut(yg), FadeOut(VGroup(la0, lb0, le0)), *[Create(l) for l in lines], FadeIn(tips), FadeIn(sch), run_time=2.4)
        lb = T("Bacteria", 34, BLUE).move_to([-3.4, -2.4, 0])
        la = T("Archaea", 34, ORANGE).move_to([1.5, -2.3, 0])
        self.play(FadeIn(lb), FadeIn(la), run_time=0.8)
        self.at("eukaryotes inside the archaea")
        P = T13
        base = VGroup(*[Dot(radius=r, color=GREEN).set_opacity(o).move_to([P["Nag"][0] + dx, P["Nag"][1] + dy, 0])
                        for r, o, dx, dy in ((0.5, 0.12, 0.3, -0.1), (0.32, 0.18, 0.0, 0.0), (0.4, 0.12, 0.7, -0.3))])
        for d in base:
            pulse(d, 1.0, 0.12, 2.0)
        gline = seg(P["Nag"], P["g"], GREEN)
        gtip = icon(GREEN).move_to(P["g"])
        bob(gtip, 0.06, 0.9, 1)
        le = T("Eukarya", 34, GREEN).move_to([5.1, -0.55, 0])
        self.play(FadeIn(base), Create(gline), FadeIn(gtip), FadeIn(le), run_time=2.0)
        self.at("closest to a group")
        br = RoundedRectangle(corner_radius=0.2, width=2.2, height=2.3, stroke_color=ORANGE, stroke_width=5).move_to([4.15, 2.0, 0])
        self.play(Create(br), run_time=1.0)
        self.at("asgard archaea")
        asg = T("Asgard archaea", 34, ORANGE).move_to([3.5, 3.4, 0])
        self.play(FadeIn(asg, shift=DOWN * 0.2), run_time=1.0)
        self.at("exactly where")
        self.play(Indicate(base, color=GREEN, scale_factor=1.3), run_time=1.3)
        self.at("still debated")
        tag = T("exact position debated", 34, YELLOW).move_to([0.2, -3.3, 0])
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=1.0)
        self.at("on that view")
        self.wait(0.3)
        self.at("two primary branches")
        self.play(lines[0].animate.set_stroke(width=14), lines[1].animate.set_stroke(width=14), run_time=1.2)
        self.at("bacteria and archaea")
        self.play(Indicate(lb, scale_factor=1.2), Indicate(la, scale_factor=1.2), run_time=1.5)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        motes(self)
        faint, _, _, _ = tree13(0.15, green=True)
        self.add(faint)
        field, ca, cb, la, lb = microscope()
        self.at("back to the methanogen")
        self.play(FadeIn(field), FadeIn(ca), FadeIn(cb), FadeIn(la), FadeIn(lb), run_time=1.5)
        self.at("their looks hid")
        self.play(Indicate(ca, scale_factor=1.08, color=GREY), Indicate(cb, scale_factor=1.08, color=GREY), run_time=1.0)
        self.at("how far apart")
        self.play(FadeOut(field), ca.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.4).move_to([-5.0, 0.3, 0]),
                  cb.animate.set_stroke(BLUE).set_fill(BLUE, 0.4).move_to([5.0, 0.3, 0]),
                  la.animate.set_color(ORANGE).move_to([-5.0, -1.2, 0]), lb.animate.set_color(BLUE).move_to([5.0, -1.2, 0]),
                  run_time=2.2)
        self.at("a molecule")
        rib = Ribbon(-3.4, 3.4, 0.3, n=60, amp=0.35, freq=1.5, r=0.12, p=0)
        self.add(rib)
        self.play(rib.p.animate.set_value(1), run_time=1.1, rate_func=linear)
        self.at("every cell shares")
        rl = T("ribosomal RNA", 34, WH).move_to([0, 1.5, 0])
        self.play(FadeIn(rl, shift=DOWN * 0.2), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Read relatedness from a shared molecule, not from looks."
