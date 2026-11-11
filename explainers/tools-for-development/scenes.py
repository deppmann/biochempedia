"""What Can a Label Prove?  (tools-for-development, single film, re-animated 2026-11-11)

COLOR MAP (whole film)
  BLUE  = observed labels and tracers       GOLD  = time pulse
  GREEN = inherited mark or reporter        RED   = intervention (Cre)
  GREY  = unobserved cells and DNA
One world: a schematic neuron with four locked cards (identity, projection, birth window, ancestry).
Every picture is schematic; no curves are plotted.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

# ------------------------------------------------------------------ geometry of the carried neuron
SOMA = np.array([-3.6, 0.0, 0.0])
TERMS = [np.array([5.0, 1.5, 0.0]), np.array([5.55, 0.0, 0.0]), np.array([5.0, -1.5, 0.0])]


def axon_y(x):
    return 0.22 * np.sin(1.1 * (x + 2.75))


BRANCH = np.array([3.3, axon_y(3.3), 0.0])
DEND = [[(-4.25, 0.6), (-5.0, 1.1), (-5.75, 1.8)], [(-5.0, 1.1), (-5.9, 0.9)],
        [(-4.45, 0.0), (-5.3, -0.15), (-6.0, -0.4)], [(-5.3, -0.15), (-5.8, 0.4)],
        [(-4.25, -0.6), (-4.9, -1.2), (-5.5, -2.0)], [(-4.9, -1.2), (-5.9, -1.3)]]


class Path:
    def __init__(self, pts):
        self.p = np.array(pts, float)
        seg = np.linalg.norm(np.diff(self.p, axis=0), axis=1)
        self.c = np.concatenate([[0], np.cumsum(seg)])
        self.L = self.c[-1]

    def at(self, a):
        s = min(max(a, 0.0), 1.0) * self.L
        i = int(min(np.searchsorted(self.c, s, side="right") - 1, len(self.p) - 2))
        f = (s - self.c[i]) / max(self.c[i + 1] - self.c[i], 1e-9)
        return self.p[i] * (1 - f) + self.p[i + 1] * f


def _trunk():
    return [np.array([x, axon_y(x), 0.0]) for x in np.arange(-2.75, 3.31, 0.1)]


PATHS = [Path(_trunk() + [BRANCH + (t - BRANCH) * k for k in np.linspace(0.1, 1, 8)]) for t in TERMS]


def side_path(y0, tip):
    x0, x1 = -3.05, tip[0]
    pts = []
    for s in np.linspace(0, 1, 40):
        e = s * s * (3 - 2 * s)
        pts.append(np.array([x0 + s * (x1 - x0), y0 + (tip[1] - y0) * e, 0.0]))
    return Path(pts)


def make_neuron():
    dend = VGroup(*[VMobject().set_points_as_corners([np.array([x, y, 0.0]) for x, y in pts]).set_stroke(GREY, 6) for pts in DEND])
    axon = VMobject().set_points_smoothly([np.array([x, axon_y(x), 0.0]) for x in np.arange(-2.75, 3.31, 0.25)]).set_stroke(GREY, 7)
    br = VGroup(*[Line(BRANCH, t).set_stroke(GREY, 6) for t in TERMS])
    bou = VGroup(*[Dot(t, radius=0.15, color=GREY) for t in TERMS])
    soma = Circle(radius=0.85).move_to(SOMA).set_stroke(GREY, 6).set_fill(GREY, 0.35)
    nuc = Circle(radius=0.3).move_to(SOMA).set_stroke(width=0).set_fill(GREY, 0.6)
    g = VGroup(dend, axon, br, soma, nuc, bou)
    g.soma, g.nuc, g.bou = soma, nuc, bou
    return g


def side_neuron(y0, tip):
    path = side_path(y0, tip)
    soma = Circle(radius=0.55).move_to([-3.6, y0, 0]).set_stroke(GREY, 4).set_fill(GREY, 0.2)
    axon = VMobject().set_points_smoothly([path.at(a) for a in np.linspace(0, 1, 12)]).set_stroke(GREY, 4)
    bou = Dot(tip, radius=0.15, color=GREY)
    g = VGroup(axon, soma, bou)
    g.soma, g.bou, g.path = soma, bou, path
    return g


class Stream(VGroup):
    """Dots that loop along a Path. `gain` (0..1) is the opacity."""

    def __init__(self, path, n=4, color=BLUE, speed=1.6, radius=0.1, reverse=False, gain=0.0):
        super().__init__()
        self.path, self.n, self.color, self.speed, self.reverse = path, n, color, speed, reverse
        self.gain = ValueTracker(gain)
        self.t = 0.0
        self.dots = [Dot(radius=radius * 1.5) for _ in range(n)]
        self.add(*self.dots)
        self.add_updater(lambda m, dt: m.step(dt))
        self.step(0)

    def step(self, dt):
        self.t += dt
        g = self.gain.get_value()
        for k, d in enumerate(self.dots):
            a = (self.t * self.speed / self.path.L + k / self.n) % 1
            if self.reverse:
                a = 1 - a
            d.move_to(self.path.at(a))
            d.set_fill(self.color, opacity=g * float(np.sin(np.pi * a)) ** 0.5)
            d.set_stroke(width=0)


# ------------------------------------------------------------------ small helpers
def bob(m, amp=0.04, per=3.0, ph=0.0):
    m._bt = 0.0

    def u(mm, dt):
        mm._bt += dt
        d = amp * (np.sin(2 * np.pi * mm._bt / per + ph) - np.sin(2 * np.pi * (mm._bt - dt) / per + ph))
        mm.shift(UP * d)
    m.add_updater(u)
    return m


def shimmer(m, per=3.0, lo=0.08, hi=0.2, ph=0.0):
    m._st = 0.0

    def u(mm, dt):
        mm._st += dt
        mm.set_fill(opacity=lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * mm._st / per + ph)))
    m.add_updater(u)
    return m


def motes(scene, n=45, seed=1):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.06, 0.12), color=[TEAL, GREY, TEXT][rng.randint(3)]).set_opacity(rng.uniform(0.35, 0.6))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-0.4, 0.4), rng.uniform(0.3, 0.6))

        def dr(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.9:
                m.shift(DOWN * 7.8)
            if abs(m.get_x()) > 6.9:
                m.shift(LEFT * 13.8 * np.sign(m.get_x()))
        d.add_updater(dr)
        g.add(d)
    g.set_z_index(-5)
    scene.add(g)
    return g


def clock(scene):
    c = ValueTracker(0)
    c.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(c)
    return c


def label(text, color=TEXT, size=28, **kw):
    return T(text, size, color, **kw)


CARD = {"id": ("Identity", BLUE, (-3.6, 3.25)), "proj": ("Projection", BLUE, (3.6, 3.25)),
        "birth": ("Birth window", GOLD, (-3.6, -3.25)), "anc": ("Ancestry", GREEN, (3.6, -3.25))}


def make_card(key, locked=True):
    name, col, pos = CARD[key]
    box = RoundedRectangle(corner_radius=0.14, width=3.5, height=0.78, stroke_color=col, stroke_width=3,
                           fill_color=BG, fill_opacity=1)
    tint = RoundedRectangle(corner_radius=0.14, width=3.5, height=0.78, stroke_width=0, fill_color=col, fill_opacity=0.12)
    txt = T(name, 28, col).move_to([0.3, 0, 0])
    body = RoundedRectangle(corner_radius=0.04, width=0.3, height=0.24, stroke_width=0, fill_color=col, fill_opacity=1).move_to([-1.4, -0.06, 0])
    shackle = Arc(radius=0.09, start_angle=0, angle=PI, color=col, stroke_width=3).move_to([-1.4, 0.1, 0])
    if not locked:
        shackle.shift(UP * 0.09)
    box.set_z_index(1); tint.set_z_index(2)
    for m in (txt, body, shackle):
        m.set_z_index(4)
    g = VGroup(box, tint, txt, body, shackle)
    g.box, g.tint, g.txt, g.shackle, g.col, g.key = box, tint, txt, shackle, col, key
    g.move_to([pos[0], pos[1], 0])
    return g


def unlock(c):
    return AnimationGroup(c.shackle.animate.shift(UP * 0.09), c.tint.animate.set_fill(c.col, 0.4),
                          c.box.animate.set_stroke(width=5))


def pos_of(key):
    return np.array([*CARD[key][2], 0.0])


def schem():
    return label("schematic", TEXT, 28).move_to([0, -3.25, 0])


def world(scene, cards=("id", "proj", "birth", "anc"), with_label=True, locked=True, stream_gain=0.55):
    n = make_neuron()
    st = Stream(PATHS[1], n=4, color=TEXT, speed=1.5, gain=stream_gain)
    cs = {k: make_card(k, locked) for k in cards}
    scene.add(n, st, *cs.values())
    lb = None
    if with_label:
        lb = schem()
        scene.add(lb)
    return n, st, cs, lb


# ------------------------------------------------------------------ cell builders
def field_cell(pos, seed, badge=False):
    rng = np.random.RandomState(seed)
    r = 0.85
    shade = Circle(radius=0.68).set_stroke(width=0).set_fill(BLUE, 0.0)
    body = Circle(radius=r).set_stroke(GREY, 4).set_fill(GREY, 0.3)
    nuc = Circle(radius=0.3).set_stroke(width=0).set_fill(GREY, 0.55)
    brs = VGroup()
    for a in rng.uniform(0, 2 * PI, 3):
        d = np.array([np.cos(a), np.sin(a), 0.0])
        mid = d * (r + 0.3) + np.array([-d[1], d[0], 0]) * rng.uniform(-.15, .15)
        tip = d * (r + 0.6)
        brs.add(VMobject().set_points_as_corners([d * r, mid, tip]).set_stroke(GREY, 3))
    bd = RoundedRectangle(corner_radius=0.05, width=0.3, height=0.3).set_stroke(width=0).set_fill(BLUE, 1.0 if badge else 0.0).move_to([0.0, 0.0, 0])
    g = VGroup(brs, shade, body, nuc, bd)
    g.brs, g.shade, g.body, g.nuc, g.bd = brs, shade, body, nuc, bd
    g.move_to([pos[0], pos[1], 0])
    return g


FIELD_POS = [(-4.2, 1.2), (0.0, 1.2), (4.2, 1.2), (-4.2, -1.25), (0.0, -1.25), (4.2, -1.25)]


def field(badges=False):
    return [field_cell(p, i, badge=(badges and i in (3, 5))) for i, p in enumerate(FIELD_POS)]


def pcell(pos, r, gold=(), segs=6):
    """Progenitor: circle with a DNA bar of 6 segments; `gold` = indices that carry label."""
    body = Circle(radius=r).set_stroke(GREY, 3).set_fill(GREY, 0.14)
    w = r * 1.3
    sw = w / segs
    bars, golds = VGroup(), []
    for k in range(segs):
        x = -w / 2 + sw * (k + 0.5)
        bars.add(Rectangle(width=sw * 0.92, height=r * 0.28).set_stroke(width=0).set_fill(GREY, 0.55).move_to([x, 0, 0]))
        gd = Rectangle(width=sw * 0.92, height=r * 0.28).set_stroke(width=0).set_fill(GOLD, 1.0 if k in gold else 0.0).move_to([x, 0, 0])
        golds.append(gd)
    g = VGroup(body, bars, *golds)
    g.body, g.golds = body, golds
    g.move_to([pos[0], pos[1], 0])
    return g


def gold_count(c):
    return sum(float(d.fill_opacity) for d in c.golds)


def tree_cell(pos, r, mark=None, col=GREEN, dashed=False):
    body = Circle(radius=r)
    nuc = Circle(radius=r * 0.45)
    if dashed:
        body = DashedVMobject(body, num_dashes=18).set_stroke(GREY, 3)
        nuc = Circle(radius=r * 0.45).set_stroke(width=0).set_fill(GREY, 0.0)
        g = VGroup(body, nuc)
    else:
        body.set_stroke(GREY, 3).set_fill(GREY, 0.2)
        nuc.set_stroke(GREY, 2).set_fill(GREY, 0.25)
        gl = VGroup()
        if mark == "quail":
            nuc.set_stroke(col, 2).set_fill(col, 0.3)
            for dx, dy in [(-.45, .3), (.4, .35), (0, -.45), (.45, -.2), (-.4, -.25)]:
                gl.add(Dot(radius=r * 0.06, color=col).move_to(nuc.get_center() + np.array([dx, dy, 0]) * r * 0.45))
        elif mark == "retro":
            nuc.set_stroke(col, 2).set_fill(col, 0.3)
            gl.add(Square(side_length=r * 0.32).set_stroke(width=0).set_fill(col, 1).move_to(nuc))
        elif mark == "lit":
            body.set_stroke(col, 3).set_fill(col, 0.38)
            nuc.set_stroke(col, 2).set_fill(col, 0.9)
        elif mark == "full":
            body.set_stroke(col, 3).set_fill(col, 0.3)
            nuc.set_stroke(col, 2).set_fill(col, 0.85)
        g = VGroup(body, nuc, gl)
    g.move_to([pos[0], pos[1], 0])
    # keep nucleus and glyph centred on the body
    if not dashed:
        nuc.move_to(body)
        for m in g[2]:
            pass
    return g


# top-down family tree geometry relative to a centre point (matches S08 / S10)
REL = {"root": (0, 1.6), "g1": [(-2.0, -0.15), (2.0, -0.15)], "g2": [(-3.1, -2.1), (-0.9, -2.1), (0.9, -2.1), (3.1, -2.1)]}


class Tree(VGroup):
    def __init__(self, cx, cy, s=1.0, mark="full", col=GREEN, dashed=False, bars=False):
        super().__init__()
        c = np.array([cx, cy, 0.0])
        P = lambda rel: c + np.array([rel[0] * s, rel[1] * s, 0.0])
        self.root = tree_cell(P(REL["root"]), 0.65 * s, None if dashed else mark, col)
        self.g1 = [tree_cell(P(p), 0.5 * s, mark, col, dashed) for p in REL["g1"]]
        self.g2 = [tree_cell(P(p), 0.42 * s, mark, col, dashed) for p in REL["g2"]]
        self.edges = VGroup()
        for i, p in enumerate(self.g1):
            self.edges.add(self._edge(self.root, p, dashed))
        for i, p in enumerate(self.g2):
            self.edges.add(self._edge(self.g1[i // 2], p, dashed))
        self.bars = VGroup()
        if bars:
            for p in self.g2:
                ln = Line(LEFT, RIGHT).set_stroke(GREY, 3).scale(0.38 * s).move_to(p.get_center() + DOWN * 0.62 * s)
                bl = Square(side_length=0.2 * s).set_stroke(width=0).set_fill(col, 0.0).move_to(ln.get_center() + RIGHT * 0.1 * s)
                self.bars.add(VGroup(ln, bl))
        self.add(self.edges, self.bars, self.root, *self.g1, *self.g2)

    @staticmethod
    def _edge(a, b, dashed):
        d = b.get_center() - a.get_center()
        n = np.linalg.norm(d)
        u = d / n
        ra, rb = a[0].width / 2, b[0].width / 2
        ln = Line(a.get_center() + u * ra, b.get_center() - u * rb).set_stroke(GREY, 4)
        return DashedLine(ln.get_start(), ln.get_end(), dash_length=0.12).set_stroke(GREY, 3) if dashed else ln

    def cells(self):
        return [self.root] + self.g1 + self.g2

    def recolor(self, col, mark_op=1.0):
        anims = []
        for c in self.cells():
            anims.append(c[0].animate.set_stroke(col, 3).set_fill(col, 0.3 * mark_op))
            anims.append(c[1].animate.set_stroke(col, 2).set_fill(col, 0.85 * mark_op))
        return anims


def chip_box(text, color, size=28):
    return chip(text, color, size)


# ====================================================================== S00 hook
class S00Hook(NarratedScene):
    def construct(self):
        motes(self, seed=0)
        n = make_neuron()
        st = Stream(PATHS[1], n=4, color=TEXT, speed=1.5, gain=0.55)
        self.add(n, st)
        cards = []
        for i, k in enumerate(("id", "proj", "birth", "anc")):
            c = make_card(k, True)
            c._ph = i * PI / 2
            c._base = c.get_center().copy()
            c._t = 0.0

            def orb(m, dt):
                m._t += dt
                m.move_to(m._base + np.array([0.35 * np.cos(1.8 * m._t + m._ph), 0.25 * np.sin(1.8 * m._t + m._ph), 0]))
            c.add_updater(orb)
            cards.append(c)
            self.add(c)
        qs = VGroup()
        for p in [SOMA + UP * 0.0, np.array([-5.2, 1.3, 0]), np.array([0.5, axon_y(0.5) + 0.65, 0]), np.array([4.6, 0.75, 0])]:
            q = T("?", 52, TEXT, weight=BOLD).move_to(p)
            q._t = 0.0
            q._ph = float(p[0])

            def pul(m, dt):
                m._t += dt
                m.set_opacity(0.45 + 0.5 * (0.5 + 0.5 * np.sin(5 * m._t + m._ph)))
            q.add_updater(pul)
            qs.add(q)
        self.add(qs, schem())
        self.wait(self.narration_s + 0.4)


# ====================================================================== S01 question
class S01Question(SpokenScene):
    def construct(self):
        motes(self, seed=1)
        n, st, cs, lb = world(self)
        self.at("hides")
        rip = Circle(radius=0.9, color=TEXT, stroke_width=4).move_to(SOMA)
        self.play(rip.animate.scale(2.2).set_stroke(opacity=0), run_time=1.8, rate_func=linear)
        self.remove(rip)
        self.at("Which label")
        for k in ("id", "proj", "birth", "anc"):
            self.play(Indicate(cs[k], scale_factor=1.1, color=cs[k].col), run_time=0.8)

        def thread(frm, to, col):
            ln = DashedLine(frm, to, dash_length=0.14).set_stroke(col, 4)
            ring = Circle(radius=0.14, color=col, stroke_width=3).move_to(to)
            return ln, ring

        specs = [("shape", np.array([-3.6, 2.85, 0]), np.array([-3.85, 1.2, 0]), BLUE),
                 ("birth time", np.array([-3.6, -2.85, 0]), np.array([-3.55, -1.25, 0]), GOLD),
                 ("ancestry", np.array([3.6, -2.85, 0]), np.array([0.8, -0.75, 0]), GREEN),
                 ("projection", np.array([3.6, 2.85, 0]), np.array([4.6, 2.0, 0]), BLUE)]
        for ph, a, b, col in specs:
            self.at(ph)
            ln, ring = thread(a, b, col)
            self.play(Create(ln), run_time=1.0)
            self.play(FadeIn(ring, scale=1.5), run_time=0.3)
        self.at("Each question")
        st.color = TEXT
        self.play(st.gain.animate.set_value(1.0), run_time=0.8)
        self.finish()


# ====================================================================== S02 title
class S02Title(TitleCard):
    LESSON = "Tools for Following Cells and Genes"
    TITLE = "What Can a Label Prove?"

    def construct(self):
        n = make_neuron().set_opacity(0.25)
        cs = [make_card(k).set_opacity(0.3) for k in ("id", "proj", "birth", "anc")]
        for i, c in enumerate(cs):
            bob(c, 0.1, 2.0, i)
        self.add(n, *cs)
        super().construct()


# ====================================================================== S03 identity
class S03Identity(SpokenScene):
    def construct(self):
        motes(self, seed=3)
        n, st, cs, lb = world(self)
        cells = field()
        for i, c in enumerate(cells):
            bob(c, 0.05, 3.0, i)
        # transform neuron into the field of cells
        self.play(FadeOut(n), st.gain.animate.set_value(0), FadeOut(cs["proj"]), FadeOut(cs["anc"]),
                  LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.15), run_time=1.8)
        self.play(Indicate(cs["id"], scale_factor=1.08), run_time=0.8)
        self.at("nistle stain")
        lab = label("Nissl", BLUE).move_to([0, 3.25, 0])
        self.play(FadeIn(lab), *[c.shade.animate.set_fill(BLUE, 0.5) for c in cells], run_time=1.6)
        self.at("bodies", lead=-0.4)
        self.play(*[c.shade.animate.set_fill(BLUE, 0.0) for c in cells], FadeOut(lab), run_time=0.9)
        self.at("golgi stain")
        lab = label("Golgi", BLUE).move_to([0, 3.25, 0])
        g = cells[1]
        self.play(FadeIn(lab), g.body.animate.set_stroke(BLUE, 4).set_fill(BLUE, 0.35), run_time=1.0)
        self.play(g.brs.animate.set_stroke(BLUE, 4), run_time=1.2)
        self.at("branches", lead=-1.0)
        self.play(g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.14), g.brs.animate.set_stroke(GREY, 3), FadeOut(lab), run_time=0.8)
        self.at("antibody binds")
        lab = label("Antibody", BLUE).move_to([0, 3.25, 0])
        self.play(FadeIn(lab), run_time=0.6)
        self.at("one chosen protein")
        self.play(*[cells[i].bd.animate.set_fill(BLUE, 1.0) for i in (3, 5)], run_time=0.8)
        self.play(*[Indicate(cells[i].bd, scale_factor=1.8, color=BLUE) for i in (3, 5)], run_time=1.0)
        self.at("these marks report")
        self.play(*[Indicate(cells[i].bd, scale_factor=1.6, color=BLUE) for i in (3, 5)], run_time=1.0)
        self.at("not when")
        self.play(Indicate(cs["birth"], scale_factor=1.12, color=GOLD), run_time=1.0)
        self.finish()


# ====================================================================== S04 projection
class S04Projection(SpokenScene):
    def construct(self):
        motes(self, seed=4)
        cells = field(badges=True)
        idc, bc = make_card("id"), make_card("birth")
        pc = make_card("proj")
        self.add(*cells, idc, bc)
        n = make_neuron()
        st = Stream(PATHS[1], n=4, color=TEXT, speed=1.5, gain=0.0)
        self.add(st)
        self.play(*[FadeOut(c) for c in cells], FadeOut(idc), FadeOut(bc), FadeIn(n), FadeIn(pc), run_time=1.4)
        self.play(st.gain.animate.set_value(0.6), run_time=0.5)
        self.at("put a tracer")
        spot = Circle(radius=0.7).move_to(SOMA).set_stroke(BLUE, 3).set_fill(BLUE, 0.5)
        self.play(FadeIn(spot, scale=0.4), run_time=1.0)
        self.at("anterograde")
        arr = Arrow([-2.3, 1.2, 0], [1.9, 1.2, 0], color=BLUE, buff=0, stroke_width=6)
        al = label("anterograde", BLUE).move_to([-0.2, 1.75, 0])
        self.play(GrowArrow(arr), FadeIn(al), run_time=1.0)
        bs = [Stream(PATHS[i], n=4, color=BLUE, speed=1.7, radius=0.12) for i in range(3)]
        self.add(*bs)
        self.play(*[b.gain.animate.set_value(1.0) for b in bs], run_time=0.8)
        self.at("terminals", lead=0.0)
        self.play(*[d.animate.set_fill(BLUE, 1.0) for d in n.bou], run_time=0.9)
        self.at("terminals", lead=-1.0)
        self.play(*[b.gain.animate.set_value(0.0) for b in bs], FadeOut(arr), FadeOut(al), FadeOut(spot),
                  *[d.animate.set_fill(GREY, 1.0) for d in n.bou], run_time=0.7)
        n2, n3 = side_neuron(1.95, np.array([5.0, 2.0, 0])), side_neuron(-1.95, np.array([5.0, -2.0, 0]))
        self.play(FadeIn(n2), FadeIn(n3), run_time=0.7)
        self.at("at a target")
        inj = Ellipse(width=2.6, height=4.8).move_to([5.2, 0, 0]).set_stroke(BLUE, 3).set_fill(BLUE, 0.4)
        self.play(FadeIn(inj, scale=0.3), run_time=1.0)
        self.at("terminals carry")
        arr2 = Arrow([2.0, -0.95, 0], [-2.0, -0.95, 0], color=BLUE, buff=0, stroke_width=6)
        al2 = label("retrograde", BLUE).move_to([0, -1.45, 0])
        self.play(GrowArrow(arr2), FadeIn(al2), run_time=0.9)
        r1 = Stream(PATHS[1], n=4, color=BLUE, speed=1.7, radius=0.12, reverse=True)
        r2 = Stream(n2.path, n=4, color=BLUE, speed=1.7, radius=0.12, reverse=True)
        self.add(r1, r2)
        self.play(r1.gain.animate.set_value(1.0), r2.gain.animate.set_value(1.0), run_time=0.8)
        self.play(n.soma.animate.set_fill(BLUE, 0.6).set_stroke(BLUE, 5), n2.soma.animate.set_fill(BLUE, 0.6).set_stroke(BLUE, 4), run_time=1.4)
        self.at("sampled population")
        sl = label("sampled population", BLUE).move_to([-2.6, 3.25, 0])
        self.play(FadeIn(sl), FadeOut(inj), FadeOut(arr2), FadeOut(al2), run_time=0.8)
        self.at("not every synapse")
        self.play(Indicate(n3.soma, scale_factor=1.35, color=TEXT), run_time=1.2)
        self.finish()


# ====================================================================== S05 birth
TL_Y = -2.25
WIN = (-3.2, -1.8)
ROWS = [1.7, 0.25, -1.2]
X0, XEND = -6.0, 1.0


class S05Birth(SpokenScene):
    def construct(self):
        motes(self, seed=5)
        T0 = clock(self)
        n = make_neuron()
        st = Stream(PATHS[1], n=4, color=TEXT, speed=1.5, gain=0.55)
        bc = make_card("birth")
        self.add(n, st, bc)
        tl = Arrow([-6.3, TL_Y, 0], [6.4, TL_Y, 0], color=GOLD, buff=0, stroke_width=5)
        tt = label("time", GOLD).move_to([5.7, TL_Y + 0.4, 0])
        self.play(Transform(n, tl), st.gain.animate.set_value(0), FadeIn(tt), run_time=1.8)
        speeds = [0.8, 0.76, 0.84]
        cells = []
        for y, v in zip(ROWS, speeds):
            c = pcell([X0, y], 0.7)
            c._v = v
            c._y = y

            def mv(m, dt):
                t = T0.get_value()
                x = min(XEND, X0 + m._v * max(0.0, t - 3.6))
                m.move_to([x, m._y + 0.05 * np.sin(2 * t + m._y), 0])
                p = min(max((x - WIN[0]) / (WIN[1] - WIN[0]), 0.0), 1.0)
                for k, gd in enumerate(m.golds):
                    gd.set_fill(GOLD, 1.0 if p * 6 > k + 0.3 else 0.0)
            c.add_updater(mv)
            cells.append(c)
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.2), run_time=1.2)
        self.at("during a short pulse")
        band = Rectangle(width=WIN[1] - WIN[0], height=TL_Y * -1 + 2.45).set_stroke(GOLD, 2).set_fill(GOLD, 0.18)
        band.move_to([(WIN[0] + WIN[1]) / 2, (2.45 + TL_Y) / 2, 0])
        shimmer(band, 2.0, 0.12, 0.26)
        pl = label("pulse", GOLD).move_to([(WIN[0] + WIN[1]) / 2, 2.95, 0])
        self.play(GrowFromEdge(band, DOWN), FadeIn(pl), run_time=0.8)
        self.at("tritiated thymidine")
        c1 = chip("tritiated thymidine", GOLD).move_to([1.3, 3.1, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.7)
        self.at("brdu")
        c2 = chip("BrdU", GOLD).move_to([4.9, 3.1, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.2), run_time=0.7)
        self.at("enters")
        dl = label("DNA", GOLD).move_to([-4.6, 2.95, 0])
        self.play(FadeIn(dl), FadeOut(pl), run_time=0.6)
        self.at("in a dividing cell")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(dl), FadeOut(band), run_time=0.7)
        self.at("s phase")
        sp = label("S phase", GOLD).move_to([0.0, 3.1, 0])
        self.play(FadeIn(sp), run_time=0.6)
        self.at("the pulse marks")
        rect0 = RoundedRectangle(corner_radius=0.2, width=4.2, height=6.4).set_stroke(GOLD, 3).move_to([XEND, 0.25, 0])
        rect1 = RoundedRectangle(corner_radius=0.2, width=1.9, height=4.7).set_stroke(GOLD, 4).move_to([XEND, 0.25, 0])
        self.play(FadeOut(sp), FadeIn(rect0), run_time=0.3)
        self.play(Transform(rect0, rect1), run_time=0.8)
        self.at("cohort")
        ch = label("cohort", GOLD).move_to([3.1, 0.25, 0])
        self.play(FadeIn(ch), run_time=0.6)
        self.finish()


# ====================================================================== S06 dilution
class S06Dilution(SpokenScene):
    def construct(self):
        motes(self, seed=6)
        T0 = clock(self)
        tl = Arrow([-6.3, TL_Y, 0], [6.4, TL_Y, 0], color=GOLD, buff=0, stroke_width=5)
        tt = label("time", GOLD).move_to([-5.6, TL_Y + 0.4, 0])
        band = Rectangle(width=WIN[1] - WIN[0], height=4.7).set_stroke(GOLD, 2).set_fill(GOLD, 0.08).move_to([sum(WIN) / 2, 0.1, 0])
        bc = make_card("birth")
        A = pcell([XEND, ROWS[0]], 0.7, gold=range(6))
        B = pcell([XEND, ROWS[1]], 0.7, gold=range(6))
        C = pcell([XEND, ROWS[2]], 0.7, gold=range(6))
        self.add(tl, tt, band, bc, A, B, C)
        self.wait(0.4)
        SH = LEFT * 3.8
        chase = Line([-1.4, TL_Y, 0], [4.4, TL_Y, 0], color=GOLD, stroke_width=9)
        cl = label("chase", GOLD).move_to([1.5, TL_Y - 0.45, 0])
        self.play(A.animate.shift(SH), B.animate.shift(SH), C.animate.shift(SH + DOWN * 0.0), band.animate.shift(SH * 1.6).set_opacity(0),
                  Create(chase), FadeIn(cl), run_time=1.6)
        self.play(FadeOut(C), run_time=0.4)
        for c in (A, B):
            bob(c, 0.04, 2.5, c.get_y())
        boxes = [Rectangle(width=1.0, height=3.8).set_stroke(TEXT, 3).move_to([gx, -0.1, 0]) for gx in (3.5, 5.1)]
        gh, gw, jit = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        fh = Rectangle(width=0.9, height=0.01).set_stroke(width=0).set_fill(GOLD, 0.95)
        fw = Rectangle(width=0.9, height=0.01).set_stroke(width=0).set_fill(GOLD, 0.95)
        holder = {}

        def mkfill(f, box, tracker, getter, jitter):
            def u(m, dt):
                v = tracker.get_value() * getter()
                if jitter:
                    v = max(0.0, v + jit.get_value() * np.sin(7 * T0.get_value()))
                h = max(0.01, 3.7 * min(v, 1.0))
                m.stretch_to_fit_height(h)
                m.move_to([box.get_x(), box.get_bottom()[1] + 0.05 + h / 2, 0])
            f.add_updater(u)
        mkfill(fh, boxes[0], gh, lambda: gold_count(A) / 6.0, False)
        mkfill(fw, boxes[1], gw, lambda: gold_count(holder["g"]) / 6.0 if "g" in holder else 0.0, True)
        hl, wl = label("Heavy", GOLD).move_to([3.5, 2.15, 0]), label("Weak", GOLD).move_to([5.1, 2.15, 0])
        sc = label("schematic", TEXT).move_to([4.3, 3.05, 0])
        ax, ay = A.get_x(), B.get_y()
        self.at("each further division")
        d1 = pcell([-1.0, ay + 0.7], 0.5, gold=(0, 1, 2))
        d2 = pcell([-1.0, ay - 0.7], 0.5, gold=(3, 4, 5))
        e1 = Line([ax + 0.7, ay, 0], [-1.5, ay + 0.7, 0]).set_stroke(GREY, 3)
        e2 = Line([ax + 0.7, ay, 0], [-1.5, ay - 0.7, 0]).set_stroke(GREY, 3)
        self.play(FadeOut(B, shift=RIGHT * 0.4), FadeIn(d1, shift=LEFT * 1.2), FadeIn(d2, shift=LEFT * 1.2), Create(e1), Create(e2), run_time=1.4)
        self.at("dilutes")
        gy = [ay + 1.1, ay + 0.3, ay - 0.5, ay - 1.3]
        gs = [pcell([0.8, gy[0]], 0.36, gold=(0, 1)), pcell([0.8, gy[1]], 0.36, gold=(2,)),
              pcell([0.8, gy[2]], 0.36, gold=(3, 4)), pcell([0.8, gy[3]], 0.36, gold=(5,))]
        holder["g"] = gs[1]
        ge = [Line([-0.5, ay + 0.7, 0], [0.4, gy[0], 0]), Line([-0.5, ay + 0.7, 0], [0.4, gy[1], 0]),
              Line([-0.5, ay - 0.7, 0], [0.4, gy[2], 0]), Line([-0.5, ay - 0.7, 0], [0.4, gy[3], 0])]
        for e in ge:
            e.set_stroke(GREY, 3)
        self.play(*[FadeIn(g, shift=LEFT * 1.0) for g in gs], *[Create(e) for e in ge], run_time=1.6)
        self.at("heavy label")
        self.add(fh, fw)
        self.play(FadeIn(VGroup(*boxes)), FadeIn(hl), FadeIn(sc), gh.animate.set_value(1.0), Indicate(A, scale_factor=1.2, color=GOLD), run_time=1.1)
        self.at("approximate")
        ap = label("approximate, not exact", GOLD).move_to([-1.5, 3.25, 0])
        self.play(FadeIn(ap), run_time=0.6)
        self.at("weak label")
        self.play(FadeIn(wl), gw.animate.set_value(1.0), *[Indicate(g, scale_factor=1.25, color=GOLD) for g in gs], run_time=1.0)
        self.at("continued cycling")
        rings = []
        for g in gs:
            rg = DashedVMobject(Circle(radius=0.52), num_dashes=12).set_stroke(GOLD, 3).move_to(g)
            rg.add_updater(lambda m, dt: m.rotate(dt * 1.5))
            rings.append(rg)
        self.play(*[FadeIn(r) for r in rings], run_time=0.6)
        self.at("uptake and detection")
        self.play(jit.animate.set_value(0.06), run_time=0.5)
        self.finish()


# ====================================================================== S07 lineage
FX = np.array([-3.9, 0.25, 0.0])
G1 = [np.array([-0.8, 1.55, 0.0]), np.array([-0.8, -1.05, 0.0])]
G2 = [np.array([2.6, 2.2, 0.0]), np.array([2.6, 0.9, 0.0]), np.array([2.6, -0.4, 0.0]), np.array([2.6, -1.7, 0.0])]
SLOT = np.array([-3.9, -1.85, 0.0])


def lin_tree(mark):
    cells1 = [tree_cell(p, 0.65, mark) for p in G1]
    cells2 = [tree_cell(p, 0.5, mark) for p in G2]
    edges = []
    for i, c in enumerate(cells1):
        edges.append(Line(FX + RIGHT * 1.15, c.get_center() + LEFT * 0.65).set_stroke(GREY, 3))
    for i, c in enumerate(cells2):
        edges.append(Line(cells1[i // 2].get_center() + RIGHT * 0.65, c.get_center() + LEFT * 0.5).set_stroke(GREY, 3))
    return cells1, cells2, edges


def grow_lin(scene, mark, f, rt=1.3):
    c1, c2, ed = lin_tree(mark)
    scene.play(*[GrowFromPoint(c, f.get_right()) for c in c1], *[Create(e) for e in ed[:2]], run_time=rt)
    scene.play(*[GrowFromPoint(c, c1[i // 2].get_center()) for i, c in enumerate(c2)], *[Create(e) for e in ed[2:]], run_time=rt)
    return VGroup(*c1, *c2, *ed)


def lamp(on=False):
    core = Circle(radius=0.38).set_stroke(GREEN if on else GREY, 4).set_fill(GREEN if on else GREY, 0.9 if on else 0.2)
    rays = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * 0.55, np.array([np.cos(a), np.sin(a), 0]) * 0.8).set_stroke(GREEN if on else GREY, 4)
                    for a in np.linspace(0, 2 * PI, 9)[:-1]])
    g = VGroup(core, rays)
    g.core, g.rays = core, rays
    return g.move_to(SLOT)


class S07Lineage(SpokenScene):
    def construct(self):
        motes(self, seed=7)
        T0 = clock(self)
        f = tree_cell(FX, 1.15, "full")
        bob(f, 0.05, 2.5)
        self.add(f)
        self.play(FadeIn(f, scale=0.6), run_time=0.8)
        lab0 = label("durable mark", GREEN).move_to([0, 3.25, 0])
        self.at("survives")
        c1 = [tree_cell(p, 0.65, "full") for p in G1]
        ed = [Line(FX + RIGHT * 1.15, c.get_center() + LEFT * 0.65).set_stroke(GREEN, 4) for c in c1]
        self.play(*[GrowFromPoint(c, f.get_right()) for c in c1], *[Create(e) for e in ed], run_time=1.0)
        self.wait(0.2)
        self.play(*[FadeOut(m) for m in c1 + ed], f.animate.become(tree_cell(FX, 1.15, None)), run_time=0.6)
        f = self.mobjects[-1] if False else f
        # --- quail nucleus
        self.at("a grafted quail")
        q = tree_cell(np.array([-5.7, 2.0, 0]), 0.6, "quail")
        ql = label("quail nucleus", GREEN).move_to([0, 3.25, 0])
        self.play(FadeIn(q, scale=0.5), FadeIn(ql), run_time=1.0)
        self.at("stays")
        self.play(q.animate.move_to(FX).scale(0.85), run_time=1.0)
        newf = tree_cell(FX, 1.15, "quail")
        self.play(FadeOut(q), Transform(f, newf), run_time=0.3)
        self.at("chick tissue")
        tis = RoundedRectangle(corner_radius=0.3, width=10.2, height=5.5).move_to([-0.5, 0.0, 0]).set_stroke(GREY, 2).set_fill(GREY, 0.1)
        tis.set_z_index(-3)
        tl = label("chick tissue", GREY if False else TEXT).move_to([0, 3.25, 0])
        self.play(FadeIn(tis), FadeOut(ql), FadeIn(tl), run_time=0.5)
        fam1 = grow_lin(self, "quail", f, 0.7)
        self.at("a retroviral insert", lead=-0.2)
        self.play(FadeOut(fam1), FadeOut(tis), FadeOut(tl), Transform(f, tree_cell(FX, 1.15, None)), run_time=0.6)
        rl = label("retroviral insert", GREEN).move_to([0, 3.25, 0])
        ln = Line(LEFT, RIGHT).set_stroke(GREY, 5).scale(1.2).move_to(SLOT)
        blk = Square(side_length=0.45).set_stroke(width=0).set_fill(GREEN, 1).move_to([-6.1, -1.85, 0])
        self.play(Create(ln), FadeIn(rl), FadeIn(blk), run_time=0.6)
        self.at("dividing cell")
        self.play(blk.animate.move_to(SLOT + RIGHT * 0.3), run_time=1.4)
        self.wait(0.1)
        self.play(Transform(f, tree_cell(FX, 1.15, "retro")), run_time=0.4)
        fam2 = grow_lin(self, "retro", f, 0.7)
        self.at("cree can")
        self.play(FadeOut(fam2), FadeOut(rl), FadeOut(ln), FadeOut(blk), Transform(f, tree_cell(FX, 1.15, None)), run_time=0.6)
        cre = chip("Cre", RED).move_to([-5.7, -1.85, 0])
        lp = lamp(False)
        lp.move_to([-3.9, -1.85, 0])
        ll = label("reporter", GREEN).move_to([0, 3.25, 0])
        self.play(FadeIn(cre), FadeIn(lp), FadeIn(ll), run_time=0.6)
        self.at("switch on")
        self.play(Indicate(cre, color=RED), run_time=0.4)
        self.play(lp.core.animate.set_stroke(GREEN, 4).set_fill(GREEN, 0.9), lp.rays.animate.set_stroke(GREEN, 4),
                  Transform(f, tree_cell(FX, 1.15, "lit")), run_time=0.9)
        shimmer(lp.core, 1.6, 0.6, 1.0)
        fam3 = grow_lin(self, "lit", f, 0.7)
        self.at("in each case")
        self.play(*[Indicate(m, scale_factor=1.15, color=GREEN) for m in fam3[:6]], run_time=1.6)
        self.finish()


# ====================================================================== S08 / S09 predict
TREE_C = (-2.2, 0.4)
CHIP_X = 4.6
CHIP_Y = [1.7, 0.2, -1.3]
ANSWERS = ["Founder only", "One branch", "All descendants"]


def predict_frame(scene, question=True):
    t = Tree(TREE_C[0], TREE_C[1], 1.0, mark="retro", col=GREEN, dashed=True)
    root = tree_cell(t.root.get_center(), 0.65, "retro")
    t.remove(t.root)
    t.root = root
    t.add(root)
    chips = [chip(a, TEXT, 28).move_to([CHIP_X, y, 0]) for a, y in zip(ANSWERS, CHIP_Y)]
    halos = [Circle(radius=0.95).move_to(root).set_stroke(GREEN, 3),
             RoundedRectangle(corner_radius=0.3, width=3.6, height=3.3).move_to([-4.25, -0.75, 0]).set_stroke(GREEN, 3),
             RoundedRectangle(corner_radius=0.3, width=8.0, height=5.5).move_to([-2.2, 0.1, 0]).set_stroke(GREEN, 3)]
    for h in halos:
        h.set_stroke(opacity=0.0)
    q = label("Which cells carry the change?", TEXT, 30).move_to([0, 3.4, 0]) if question else None
    return t, chips, halos, q


class S08Predict(SpokenScene):
    def construct(self):
        motes(self, seed=8)
        t, chips, halos, q = predict_frame(self)
        self.add(*halos)
        bob(t.root, 0.08, 2.0)
        for i, c in enumerate(t.g1 + t.g2):
            bob(c, 0.05, 2.5, i)
        self.play(FadeIn(t.root, scale=0.6), run_time=1.0)
        self.play(FadeIn(VGroup(t.edges, *t.g1, *t.g2)), run_time=1.2)
        self.at("one founder")
        self.play(Indicate(t.root, scale_factor=1.2, color=GREEN), run_time=1.0)
        self.at("permanent")
        gl = t.root[2]
        self.play(Indicate(gl, scale_factor=2.0, color=GREEN), run_time=1.0)
        self.at("then divides twice")
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.15, color=GREEN) for c in t.g1 + t.g2], lag_ratio=0.2), run_time=1.6)
        self.at("which cell")
        self.play(FadeIn(q), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2), run_time=1.0)
        for c, h in zip(chips, halos):
            self.play(Indicate(c, scale_factor=1.1, color=GREEN), h.animate.set_stroke(opacity=0.7), run_time=0.6)
            self.play(h.animate.set_stroke(opacity=0.0), run_time=0.3)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        motes(self, seed=9)
        t, chips, halos, q = predict_frame(self)
        self.add(t, *chips, q)
        bob(t.root, 0.08, 2.0)
        for i, c in enumerate(t.g1 + t.g2):
            bob(c, 0.05, 2.5, i)
        ring = RoundedRectangle(corner_radius=0.3, width=3.7, height=4.3).move_to([CHIP_X, 0.2, 0]).set_stroke(GREEN, 4)
        self.play(Create(ring), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


# ====================================================================== S10 reveal
class S10Reveal(SpokenScene):
    def construct(self):
        motes(self, seed=10)
        T0 = Tree(TREE_C[0], TREE_C[1], 1.0, mark="retro", col=GREEN, dashed=True, bars=True)
        root = tree_cell(T0.root.get_center(), 0.65, "retro")
        T0.remove(T0.root)
        T0.root = root
        T0.add(root)
        full = Tree(TREE_C[0], TREE_C[1], 1.0, mark="full", col=GREEN, bars=True)
        self.add(T0)
        self.at("descendant")
        # gen1 then gen2 turn into marked cells
        self.play(*[Transform(a, b) for a, b in zip(T0.g1, full.g1)], Transform(T0.edges, full.edges), run_time=0.9)
        self.play(*[Transform(a, b) for a, b in zip(T0.g2, full.g2)], run_time=0.9)
        self.at("changed")
        sq = [Square(side_length=0.2).set_stroke(width=0).set_fill(GREEN, 1).move_to(c.get_center()) for c in full.g2]
        self.add(*sq)
        self.play(*[s.animate.move_to(b[1].get_center()) for s, b in zip(sq, T0.bars)], run_time=1.2)
        self.play(*[b[1].animate.set_fill(GREEN, 1.0) for b in T0.bars], FadeOut(VGroup(*sq)), run_time=0.4)
        # zoom out to three families
        self.at("yet")
        S = 0.75
        mid = Tree(0.0, 0.3, S, "full", GREEN, bars=True)
        L = Tree(-3.0, 0.9, S, "full", GREEN, bars=True)
        R = Tree(3.0, 0.9, S, "full", GREEN, bars=True)
        for tr in (L, R, mid):
            for b in tr.bars:
                b[1].set_fill(GREEN, 1.0)
        c0 = np.array([TREE_C[0], TREE_C[1], 0.0])
        self.play(T0.animate.scale(S, about_point=c0).shift(np.array([0.0, 0.3, 0]) - c0),
                  FadeIn(L), FadeIn(R), run_time=1.4)
        self.at("gives a population")
        pl = label("population fate map", GREEN).move_to([0, 3.25, 0])
        self.play(FadeIn(pl), run_time=0.7)
        self.at("not separate clones")
        nl = label("not separate clones", GREEN).move_to([0, 3.25, 0])
        self.play(FadeOut(pl), FadeIn(nl), run_time=0.7)
        fam_mid, fam_l, fam_r = T0, L, R
        self.at("sparse induction")
        sp = label("sparse induction", TEXT).move_to([0, 3.25, 0])
        self.play(FadeOut(nl), FadeIn(sp), *fam_l.recolor(GREY, 0.3), *fam_r.recolor(GREY, 0.3), run_time=1.0)
        self.at("multiple colors")
        ml = label("multiple colours", TEXT).move_to([0, 3.25, 0])
        self.play(FadeOut(sp), FadeIn(ml), *fam_l.recolor(TEAL, 1.0), *fam_r.recolor(PURPLE, 1.0), *fam_mid.recolor(ORANGE, 1.0), run_time=1.2)
        self.at("distinct barcodes")
        bl = label("distinct barcodes", TEXT).move_to([0, 3.25, 0])
        self.play(FadeOut(ml), FadeIn(bl), run_time=0.5)
        codes = VGroup()
        for fam, col, pat in ((fam_l, TEAL, (1, 0, 1, 1)), (fam_mid, ORANGE, (1, 1, 0, 1)), (fam_r, PURPLE, (0, 1, 1, 0))):
            rc = fam.root.get_center()
            bc = VGroup(*[Rectangle(width=0.09, height=0.45).set_stroke(width=0).set_fill(col, 1 if p else 0.25).move_to(rc + np.array([0.85 + 0.14 * i, 0, 0])) for i, p in enumerate(pat)])
            codes.add(bc)
        self.play(FadeIn(codes), run_time=0.8)
        self.at("separate neighboring")
        self.play(fam_l.animate.shift(LEFT * 0.6), fam_r.animate.shift(RIGHT * 0.6), codes[0].animate.shift(LEFT * 0.6), codes[2].animate.shift(RIGHT * 0.6), run_time=1.6)
        self.finish()


# ====================================================================== S11 rule
class S11Rule(SpokenScene):
    def construct(self):
        motes(self, seed=11)
        n, st, cs, lb = world(self, with_label=False)
        for i, k in enumerate(cs):
            bob(cs[k], 0.05, 2.5, i)
        self.at("a tool supports")
        for k in ("id", "proj", "birth", "anc"):
            self.play(Indicate(cs[k], scale_factor=1.08, color=cs[k].col), run_time=0.6)

        def fly(mob, key, rt=1.0):
            return mob.animate.move_to(pos_of(key)).scale(0.5).set_opacity(0.0)

        # identity
        self.at("protein binding")
        badge = RoundedRectangle(corner_radius=0.06, width=0.4, height=0.4).set_stroke(width=0).set_fill(BLUE, 1).move_to([-3.2, 1.2, 0])
        self.play(FadeIn(badge, scale=0.4), run_time=0.7)
        self.at("target detection", lead=0.6)
        self.play(badge.animate.move_to(pos_of("id") + DOWN * 0.1).scale(0.6), run_time=1.0)
        self.play(FadeOut(badge), unlock(cs["id"]), run_time=0.6)
        l1 = label("target detected", BLUE).move_to([-3.6, 2.45, 0])
        self.play(FadeIn(l1), run_time=0.5)
        # projection
        self.at("transport can")
        tr = VGroup(*[Dot(radius=0.12, color=BLUE).move_to(TERMS[0] + np.array([0.0 - 0.3 * i, 0.0, 0])) for i in range(3)])
        self.play(FadeIn(tr), run_time=0.6)
        self.at("a projection", lead=0.2)
        self.play(*[d.animate.move_to(pos_of("proj") + DOWN * 0.1 + RIGHT * (i - 1) * 0.25) for i, d in enumerate(tr)], run_time=1.0)
        self.play(FadeOut(tr), unlock(cs["proj"]), run_time=0.6)
        # birth
        self.at("synthesis can")
        ring = Circle(radius=0.3).set_stroke(GOLD, 7).move_to(SOMA)
        self.play(FadeIn(ring, scale=0.3), run_time=0.7)
        self.at("can date", lead=0.2)
        self.play(ring.animate.move_to(pos_of("birth") + UP * 0.1).scale(0.6), run_time=1.0)
        self.play(FadeOut(ring), unlock(cs["birth"]), run_time=0.6)
        l2 = label("approximately", GOLD).move_to([-3.6, -2.5, 0])
        self.play(FadeIn(l2), run_time=0.5)
        # ancestry
        self.at("and inherited")
        fk = VGroup(Dot(radius=0.12, color=GREEN), Dot(radius=0.12, color=GREEN), Dot(radius=0.12, color=GREEN))
        fk[0].move_to([1.0, 0.0, 0]); fk[1].move_to([1.35, 0.3, 0]); fk[2].move_to([1.35, -0.3, 0])
        fk.add(Line(fk[0].get_center(), fk[1].get_center()).set_stroke(GREEN, 4), Line(fk[0].get_center(), fk[2].get_center()).set_stroke(GREEN, 4))
        self.play(FadeIn(fk, scale=0.4), run_time=0.8)
        self.at("change can report")
        self.play(fk.animate.move_to(pos_of("anc") + UP * 0.1).scale(0.6), run_time=1.0)
        self.play(FadeOut(fk), unlock(cs["anc"]), run_time=0.6)
        self.finish()


# ====================================================================== S12 limit
PAN = {"id": ((-3.3, 1.9), "target only"), "proj": ((3.3, 1.9), "population only"),
       "birth": ((-3.3, -1.9), "approximate"), "anc": ((3.3, -1.9), "founders unresolved")}


class S12Limit(SpokenScene):
    def construct(self):
        motes(self, seed=12)
        n, st, cs, lb = world(self, with_label=False, locked=False)
        for k in cs:
            cs[k].shackle.shift(DOWN * 0.0)
        self.play(FadeOut(n), st.gain.animate.set_value(0.0), run_time=0.5)
        panels, names = {}, {}
        for k, (c, txt) in PAN.items():
            col = CARD[k][1]
            p = Rectangle(width=6.2, height=3.3).set_stroke(col, 3).set_fill(col, 0.1).move_to([c[0], c[1], 0])
            shimmer(p, 3.0, 0.07, 0.17, ph=len(k))
            p.set_z_index(0)
            panels[k] = p
        anims = []
        for k, c in cs.items():
            anims.append(Transform(c.box, panels[k]))
            anims.append(FadeOut(c.tint)); anims.append(FadeOut(c.shackle)); anims.append(FadeOut(c[3]))
            nm = CARD[k][0]
            anims.append(c.txt.animate.move_to([PAN[k][0][0] - 3.1 + 1.45, PAN[k][0][1] + 1.2, 0]))
        self.play(*anims, run_time=1.2)
        for k, c in cs.items():
            self.remove(c.box)
            self.add(panels[k])
            self.bring_to_front(c.txt)
        cross = VGroup(Line([-6.5, 0, 0], [6.5, 0, 0]), Line([0, -3.5, 0], [0, 3.5, 0])).set_stroke(TEXT, 4).set_z_index(5)
        self.play(Create(cross), run_time=0.5)

        def show(k):
            c = PAN[k][0]
            col = CARD[k][1]
            x0 = c[0] - 2.6
            xs = c[0] + 1.6
            arr = Line([x0, c[1] + 0.15, 0], [xs, c[1] + 0.15, 0]).set_stroke(col, 6)
            stop = Line([xs, c[1] - 0.2, 0], [xs, c[1] + 0.5, 0]).set_stroke(RED, 7)
            t = label(PAN[k][1], TEXT, 34).move_to([c[0], c[1] - 0.6, 0])
            self.play(Create(arr), run_time=0.9)
            self.play(FadeIn(stop), FadeIn(t), run_time=0.5)
            return VGroup(arr, stop, t)
        gs = {}
        self.at("the rule also")
        gs["id"] = show("id")
        self.at("a tracer does", lead=0.0)
        gs["proj"] = show("proj")
        self.at("a weak birth")
        gs["birth"] = show("birth")
        self.at("a shared lineage")
        gs["anc"] = show("anc")
        self.at("state the strongest")
        self.play(*[Indicate(panels[k], scale_factor=1.03, color=CARD[k][1]) for k in panels], run_time=1.2)
        self.at("then name")
        for k in ("id", "proj", "birth", "anc"):
            self.play(Indicate(gs[k][2], scale_factor=1.15, color=TEXT), run_time=0.5)
        self.finish()


# ====================================================================== S13 end
class S13End(EndCard):
    LINE = "A tool supports only what its mark records."
