"""One Stain, Two Readings (chapter 2 of "Seeing neurons: Golgi, Cajal and the neuron doctrine")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept; shared by all chapters of this lesson)
  BLUE   = neuron one / the young cell and its fibre
  YELLOW = neuron two (the other cell)
  RED    = the limit of the light microscope (the blur disc, the blind spot)
  ORANGE = Golgi's reading: the branches are joined into a net
  GREEN  = Cajal's reading and the verdict: separate cells, free endings
  TEAL   = direction of signal flow (dynamic polarization)
  VIOLET = Nissl stain (cell bodies only)
  INK    = Golgi's black reaction (black on a pale yellowish field)
  GOLD   = string lights in the forest analogy (and the title rule)
  GREY   = tissue, outlines, unstained or de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
VIOLET = "#A66BDB"
INK = "#14110C"
FIELD = "#E6DDB0"
PALE = "#B9AB6E"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def smooth(points, color, w=6, opacity=1.0):
    m = VMobject()
    m.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in points])
    m.set_stroke(color, w, opacity=opacity)
    m.set_fill(opacity=0)
    return m


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def label(text, color=TEXT, size=26, **kw):
    return T(text, size, color, **kw)


def head(text, color=TEXT, size=36, y=3.3):
    return T(text, size, color, font=TITLE_FONT).move_to([0, y, 0])


def disc(radius, center, fill=0.0, dashed=True):
    c = Circle(radius=radius, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=fill).move_to([center[0], center[1], 0])
    return DashedVMobject(c, num_dashes=28) if dashed and fill == 0 else c


def blur(center, radius):
    """the blur disc of the light microscope: soft red fill and a dashed rim."""
    return VGroup(disc(radius, center, fill=0.28, dashed=False), disc(radius, center))


class Sc(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        # Same word alignment as SpokenScene, without creating an extra project file.
        target = self.t_of(phrase, nth) - lead
        if target - self.elapsed() > 0.02:
            self.wait(target - self.elapsed())

    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ---- Golgi panel -----------------------------------------------------------------------------
PX0, PX1, PY0, PY1 = -6.1, 6.1, -2.75, 2.75


def field():
    return RoundedRectangle(corner_radius=0.2, width=PX1 - PX0, height=PY1 - PY0, stroke_color=GREY,
                            stroke_width=2, fill_color=FIELD, fill_opacity=1)


def pale_cells(seed=3, n=15):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        x, y = rng.uniform(PX0 + 0.6, PX1 - 0.6), rng.uniform(PY0 + 0.5, PY1 - 0.5)
        e = Ellipse(width=rng.uniform(0.5, 0.8), height=rng.uniform(0.4, 0.6), stroke_color=PALE, stroke_width=2,
                    fill_color=PALE, fill_opacity=0.28).move_to([x, y, 0]).rotate(rng.uniform(0, 3))
        g.add(e)
    return g


def _inside(q, b):
    return b[0] <= q[0] <= b[1] and b[2] <= q[1] <= b[3]


class GN:
    """A Golgi-stained neuron: soma, branching dendrites and an axon, clipped at the section edge."""

    def __init__(self, c, s, seed, bounds=(PX0, PX1, PY0, PY1), axon_ang=0.0, ax_len=3.0, dd=2, ad=3):
        rng = np.random.default_rng(seed)
        self.c = np.array(c, float)
        self.s = s
        self.segs, self.cuts = [], []
        self.bounds = bounds
        da = [axon_ang + np.pi - 0.9, axon_ang + np.pi + 0.9, axon_ang + np.pi / 2 + 0.1, axon_ang - np.pi / 2 - 0.1]
        for a in da:
            self._grow(rng, self.c, a + rng.uniform(-.2, .2), 1.05 * s, dd, 5.0, None, 0.6, 0.78, 0)
        self._grow(rng, self.c, axon_ang, ax_len * s, ad, 3.4, None, 0.5, 0.72, 0)
        self.soma = Circle(radius=0.3 * s, stroke_color=INK, stroke_width=3, fill_color=INK, fill_opacity=1).move_to([self.c[0], self.c[1], 0])

    def _grow(self, rng, p0, ang, length, depth, w, parent, spread, shrink, level):
        n = 4
        pts = [np.array(p0, float)]
        a = ang
        cut = False
        for _ in range(n):
            a += rng.uniform(-.28, .28)
            q = pts[-1] + (length / n) * np.array([np.cos(a), np.sin(a)])
            if not _inside(q, self.bounds):
                p = pts[-1]
                t = 1.0
                b = self.bounds
                if q[0] > b[1]: t = min(t, (b[1] - p[0]) / (q[0] - p[0]))
                if q[0] < b[0]: t = min(t, (b[0] - p[0]) / (q[0] - p[0]))
                if q[1] > b[3]: t = min(t, (b[3] - p[1]) / (q[1] - p[1]))
                if q[1] < b[2]: t = min(t, (b[2] - p[1]) / (q[1] - p[1]))
                q = p + max(t, 0.0) * (q - p)
                if np.linalg.norm(q - p) > 0.05:
                    pts.append(q)
                cut = True
                break
            pts.append(q)
        if len(pts) < 2:
            return
        idx = len(self.segs)
        self.segs.append(dict(pts=pts, w=w, parent=parent, level=level, kids=0, cut=cut))
        if parent is not None:
            self.segs[parent]["kids"] += 1
        if cut:
            self.cuts.append(pts[-1])
            return
        if depth > 0:
            for sg in (1, -1):
                self._grow(rng, pts[-1], a + sg * spread * rng.uniform(.6, 1.3), length * shrink * rng.uniform(.85, 1.1),
                           depth - 1, max(w * .72, 1.6), idx, spread, shrink, level + 1)

    def lines(self, color=INK):
        return VGroup(*[smooth(sg["pts"], color, sg["w"]) for sg in self.segs])

    def mob(self, color=INK):
        return VGroup(self.lines(color), self.soma.copy())

    def path_to_leaf(self):
        leaves = [i for i, sg in enumerate(self.segs) if sg["kids"] == 0 and not sg["cut"] and sg["level"] >= 2]
        best = max(leaves, key=lambda i: self.segs[i]["level"] * 10 + np.linalg.norm(self.segs[i]["pts"][-1] - self.c))
        chain = []
        i = best
        while i is not None:
            chain.append(i)
            i = self.segs[i]["parent"]
        pts = []
        for i in reversed(chain):
            pts += [p for p in self.segs[i]["pts"] if not pts or np.linalg.norm(p - pts[-1]) > 1e-6]
        return pts


def golgi_set():
    """the four black cells of the sparse stain; the same set in every scene that shows the panel."""
    return [GN([-4.3, 0.5], 1.0, 11, axon_ang=0.35, ax_len=3.2),
            GN([-0.9, -1.2], 1.0, 23, axon_ang=-0.3, ax_len=3.4),
            GN([2.5, 1.2], 1.0, 35, axon_ang=0.1, ax_len=3.2),
            GN([4.9, -1.3], 1.0, 47, axon_ang=2.9, ax_len=2.6)]


def trace_line(lines_group, ink=INK):
    return lines_group


# ---- forest ---------------------------------------------------------------------------------
def fold(v, lo, hi):
    """reflect v back into [lo, hi] (so a wandering line bounces off the frame instead of running along it)."""
    span = hi - lo
    u = (v - lo) % (2 * span)
    return lo + (u if u <= span else 2 * span - u)


def tree_segs(x, base_y, s, seed, depth=3):
    rng = np.random.default_rng(seed)
    out = []

    def g(p0, ang, length, d, w):
        pts = [np.array(p0, float)]
        a = ang
        for _ in range(3):
            a += rng.uniform(-.12, .12)
            pts.append(pts[-1] + (length / 3) * np.array([np.cos(a), np.sin(a)]))
        out.append((pts, w))
        if d > 0:
            for sg in (1, -1):
                g(pts[-1], a + sg * 0.55 * rng.uniform(.7, 1.2), length * 0.74 * rng.uniform(.9, 1.1), d - 1, max(w * .7, 1.5))

    g([x, base_y], np.pi / 2, 1.75 * s, depth, 6.5)
    return out


def tree(x, base_y, s, seed, color, opacity=1.0, depth=3, wscale=1.0):
    return VGroup(*[smooth(p, color, w * wscale, opacity) for p, w in tree_segs(x, base_y, s, seed, depth)])


def lights(x, base_y, s, seed, depth=3):
    dots = VGroup()
    for p, w in tree_segs(x, base_y, s, seed, depth):
        for q in (p[1], p[3]):
            dots.add(Dot([q[0], q[1], 0], radius=0.075, color=GOLD))
    return dots


# ---- the net drawings -------------------------------------------------------------------------
NODES = np.array([[-4.76, 2.21], [-2.12, 1.86], [0.11, 2.1], [2.9, 1.94], [5.57, 2.24], [-4.8, -0.02], [-2.67, 0.23],
                  [0.48, -0.1], [3.07, 0.34], [4.88, 0.09], [-5.0, -1.85], [-2.43, -2.49], [-0.0, -2.21], [2.6, -1.83], [5.05, -2.42]])
EDGES = [(0, 1), (0, 5), (0, 6), (1, 2), (1, 5), (1, 6), (1, 7), (2, 3), (2, 7), (3, 4), (3, 7), (3, 8), (3, 9), (4, 8), (4, 9),
         (5, 6), (5, 10), (6, 7), (6, 10), (6, 11), (7, 8), (7, 12), (7, 13), (8, 9), (8, 13), (9, 13), (9, 14), (10, 11),
         (11, 12), (12, 13), (13, 14)]


def nodes_at(sx, sy, cx=0.0, cy=0.0):
    return NODES * np.array([sx, sy]) + np.array([cx, cy])


def edge_pts(nodes, a, b, k, r0=0.0, r1=0.0, n=14):
    A, B = nodes[a], nodes[b]
    d = B - A
    L = np.linalg.norm(d)
    nrm = np.array([-d[1], d[0]]) / L
    C = (A + B) / 2 + nrm * ((-1) ** k) * L * 0.07
    t = np.linspace(0, 1, 240)[:, None]
    P = (1 - t) ** 2 * A + 2 * (1 - t) * t * C + t ** 2 * B
    ok = np.where((np.linalg.norm(P - A, axis=1) >= r0) & (np.linalg.norm(P - B, axis=1) >= r1))[0]
    sel = np.linspace(ok[0], ok[-1], n).astype(int)
    return P[sel]


def net_edges(nodes, color, w=4, r0=0.0, r1=0.0):
    return VGroup(*[smooth(edge_pts(nodes, a, b, k, r0, r1), color, w) for k, (a, b) in enumerate(EDGES)])


def net_dots(nodes, color, r=0.1):
    return VGroup(*[Dot([p[0], p[1], 0], radius=r, color=color) for p in nodes])


def cajal_cells(nodes, r=0.3):
    return VGroup(*[Circle(radius=r, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.2).move_to([p[0], p[1], 0])
                    for p in nodes])


def bulbs(nodes, r0, r1, r=0.075):
    g = VGroup()
    for k, (a, b) in enumerate(EDGES):
        e = edge_pts(nodes, a, b, k, r0, r1)[-1]
        g.add(Dot([e[0], e[1], 0], radius=r, color=GREEN))
    return g


# ---- neuron outline from the lesson's earlier film --------------------------------------------
def neuron(color=BLUE):
    pts = [(-2.1, 1.15), (-1.3, .65), (-1.05, .35), (-.85, .43), (-1.0, 1.25),
           (-.78, 1.25), (-.55, .48), (-.25, .3), (.05, .13), (1.7, .13),
           (2.1, .6), (2.23, .48), (1.86, 0), (2.23, -.48), (2.1, -.6),
           (1.7, -.13), (.05, -.13), (-.25, -.3), (-.55, -.48), (-.78, -1.25),
           (-1.0, -1.25), (-.85, -.43), (-1.05, -.35), (-1.3, -.65),
           (-2.1, -1.15), (-2.23, -.98), (-1.55, -.42), (-1.24, 0),
           (-1.55, .42), (-2.23, .98)]
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color,
                   stroke_width=3, fill_color=color, fill_opacity=.15).round_corners(.07)


def chain(scale=0.9, spacing=4.25, y=0.9):
    return VGroup(*[neuron(c).scale(scale).move_to([x, y, 0]) for x, c in [(-spacing, BLUE), (0, YELLOW), (spacing, BLUE)]])


# ---------------------------------------------------------------------------------------------
# round-2 helpers
# ---------------------------------------------------------------------------------------------
LIGHT = "#D5D9DE"   # secondary captions: light, never dim grey


def tag(text, color=TEXT, size=30, pos=(0, 0), pad=0.12, **kw):
    """a label on a dark strip, so it never sits on top of lines behind it."""
    t = T(text, size, color, **kw)
    r = BackgroundRectangle(t, color=BG, fill_opacity=0.88, buff=pad)
    return VGroup(r, t).move_to([pos[0], pos[1], 0])


def blur_disc(center, r, smear="#E0C3AE"):
    """the blur of the light microscope, opaque: whatever lies under it becomes one smear."""
    cx, cy = center[0], center[1]
    c = Circle(radius=r, stroke_color=RED, stroke_width=5, fill_color="#6A3834", fill_opacity=1).move_to([cx, cy, 0])
    # Broad overlapping translucent halos have no resolved edge or gap.
    sm = VGroup(*[Ellipse(width=r * w, height=r * h, stroke_width=0,
                         fill_color=smear, fill_opacity=0.10).move_to([cx, cy, 0])
                  for w, h in [(1.75, 1.1), (1.55, 0.9), (1.3, 0.7), (1.05, 0.5)]])
    return VGroup(c, sm)


def cut_marks(pts, color=GOLD):
    g = VGroup()
    for p in pts:
        p = np.array([p[0], p[1], 0.0])
        d = np.zeros(3)
        if p[0] >= PX1 - .06: d[0] = 1
        elif p[0] <= PX0 + .06: d[0] = -1
        if p[1] >= PY1 - .06: d[1] = 1
        elif p[1] <= PY0 + .06: d[1] = -1
        if not d.any(): d = np.array([0, -1.0, 0])
        d = d / np.linalg.norm(d)
        ring = DashedVMobject(Circle(radius=0.3, stroke_color=color, stroke_width=5).move_to(p), num_dashes=12)
        g.add(ring, arr(p - d * 0.75, p - d * 0.36, color, 5, 0.2))
    return g


def edge_cuts(n, k=4):
    """cut ends that really lie on the section edge."""
    c = [p for p in n.cuts if p[0] >= PX1 - .06 or p[0] <= PX0 + .06 or p[1] >= PY1 - .06 or p[1] <= PY0 + .06]
    return c[:k]


def pic_panel(cx, cy, w, h):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2,
                            fill_color=FIELD, fill_opacity=1).move_to([cx, cy, 0])


def reading_picture(nd, joined, w=5, rc=0.3, gap=0.66):
    # Schematic branches, not data traces. Stable seeded arbors tie these readings
    # to the black-reaction panels; each intercell branch has an explicit end.
    ed, bodies, tips = VGroup(), VGroup(), VGroup()
    spacing = np.linalg.norm(nd[1] - nd[0])
    size = min(0.36, spacing * 0.17)
    for i, p in enumerate(nd):
        arbor = GN(p, size, 901+i, bounds=(-6.6, 6.6, -2.85, 2.85),
                   axon_ang=0.0, ax_len=0.7, dd=1, ad=0)
        ed.add(arbor.lines())
        bodies.add(Circle(radius=rc, stroke_color=INK, stroke_width=3,
                          fill_color=INK, fill_opacity=1).move_to([*p, 0]))
    # Fewer long axons, with secondary twigs; the visual reads as neural tissue.
    links = [(0,6),(1,7),(2,8),(3,9),(5,11),(6,12),(7,13),(8,14),(10,11),(11,12),(12,13),(13,14),(3,8),(4,9),(8,9)]
    for k, (a,b) in enumerate(links):
        pts = edge_pts(nd,a,b,k,rc*0.7,0 if joined else rc+gap)
        branch = smooth(pts, INK, w)
        ed.add(branch)
        if not joined:
            tips.add(Dot([*pts[-1],0], radius=0.09, color=INK))
    if joined:
        # Collaterals meet other axon branches away from the cell bodies.
        for k in (0, 1, 2, 4, 5, 6):
            a,b = links[k]
            c,d = links[k+1]
            start = edge_pts(nd,a,b,k)[8]
            end = edge_pts(nd,c,d,k+1)[6]
            middle = (start+end)/2 + np.array([0, 0.12])
            ed.add(smooth([start,middle,end],INK,w*0.75))
    return ed, bodies, tips


def golgi_pic(nd, w=5):
    ed, bodies, _ = reading_picture(nd, True, w)
    return ed, bodies


def cajal_pic(nd, w=5, rc=0.3, gap=0.66):
    return reading_picture(nd, False, w, rc, gap)


class S00Title(TitleCard):
    LESSON = "Seeing Neurons: Golgi, Cajal and the Neuron Doctrine"
    TITLE = "One Stain, Two Readings"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=28, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T("SEEING NEURONS: GOLGI, CAJAL\nAND THE NEURON DOCTRINE", size=26, color=LIGHT, line_spacing=0.8)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title), GrowFromCenter(rule), run_time=0.7)
        self.wait(1.9)
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


def tissue(seed=5, jit=0.06):
    """layered cell bodies and a crowd of fibres, all grey."""
    rng = np.random.default_rng(seed)
    bodies, fibres = VGroup(), VGroup()
    pos = []
    for row, y in enumerate([-1.7, 0.0, 1.7]):
        for i in range(7):
            x = -5.4 + i * 1.8 + (0.5 if row % 2 else 0.0) + rng.uniform(-jit, jit)
            if x > 5.7:
                continue
            pos.append((x, y + rng.uniform(-jit, jit)))
    for (x, y) in pos:
        bodies.add(Ellipse(width=0.7, height=0.56, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                           fill_opacity=0.4).move_to([x, y, 0]))
    for (x, y) in pos:
        for _ in range(3):
            a = rng.uniform(0, 2 * np.pi)
            pts = [np.array([x, y])]
            for _ in range(5):
                a += rng.uniform(-.7, .7)
                q = pts[-1] + 0.55 * np.array([np.cos(a), np.sin(a)])
                q = np.array([fold(q[0], -6.0, 6.0), fold(q[1], -2.7, 2.7)])
                pts.append(q)
            fibres.add(smooth(pts, GREY, 2.2, 0.55))
    return bodies, fibres


def tissue_panel():
    return RoundedRectangle(corner_radius=0.2, width=12.2, height=5.7, stroke_color=GREY, stroke_width=2,
                            fill_color=GREY, fill_opacity=0.05)


class S01Q(Sc):
    def construct(self):
        panel = tissue_panel().move_to([0, 0.35, 0])
        bodies, fibres = tissue()
        grp = VGroup(bodies, fibres).shift(UP * 0.35)
        q0 = T("How do you see one whole cell in a crowded brain?", 32).move_to([0, -3.15, 0])
        self.play(FadeIn(panel), LaggedStart(*[Create(f) for f in fibres], lag_ratio=0.01), FadeIn(bodies), FadeIn(q0), run_time=0.7)
        self.at("one whole cell")
        ring = DashedVMobject(Circle(radius=0.85, stroke_color=BLUE, stroke_width=5).move_to(bodies[10].get_center()), num_dashes=20)
        q = T("?", 60, BLUE, weight=BOLD).move_to(bodies[10].get_center() + UP * 1.55)
        self.play(Create(ring), FadeIn(q), run_time=0.6)
        self.at("crowded brain")
        self.play(Indicate(panel, scale_factor=1.01, color=GREY), run_time=0.5)
        self.finish()


class S02Nissl(Sc):
    def construct(self):
        panel = tissue_panel().move_to([0, 0.35, 0])
        bodies, fibres = tissue()
        VGroup(bodies, fibres).shift(UP * 0.35)
        self.add(panel, fibres, bodies)
        who = head("Franz Nissl", VIOLET)
        lab = T("Nissl stain: cell bodies", 32, VIOLET).move_to([0, -3.1, 0])
        self.play(FadeIn(who), FadeIn(lab), run_time=0.4)
        self.at("stain marks every cell body")
        self.play(*[b.animate.set_fill(VIOLET, 0.9).set_stroke(VIOLET, 3) for b in bodies], run_time=1.3)
        self.at("axons and dendrites")
        self.play(*[f.animate.set_stroke(opacity=0.04) for f in fibres], run_time=0.9)
        self.at("where the question of fusion")
        gx = float(np.mean([bodies[7].get_center()[0], bodies[8].get_center()[0]]))
        gy = bodies[7].get_center()[1]
        pale = T("axons and dendrites: almost invisible", 32, TEXT).move_to([0, -3.1, 0])
        ar = arr([gx, -2.75, 0], [gx, -0.5, 0], TEXT, 5, 0.22)
        self.play(FadeOut(lab), FadeIn(pale), GrowArrow(ar), run_time=0.7)
        self.at("stay almost invisible")
        self.play(Indicate(pale, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


def bath(x, name, num):
    w0, h0 = 4.8, 4.5
    body = Polygon([-w0 / 2, h0 / 2, 0], [w0 / 2, h0 / 2, 0], [w0 / 2 - 0.35, -h0 / 2, 0], [-w0 / 2 + 0.35, -h0 / 2, 0],
                   stroke_color=GREY, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([x, -0.55, 0])
    liquid = Polygon([-w0 / 2 + 0.07, 0.2, 0], [w0 / 2 - 0.07, 0.2, 0], [w0 / 2 - 0.37, -h0 / 2 + 0.05, 0], [-w0 / 2 + 0.4, -h0 / 2 + 0.05, 0],
                     stroke_width=0, fill_color=GREY, fill_opacity=0.4).move_to([x, -0.55 - 0.05 - (h0 / 2 - 0.2 + 0.05 - (h0 / 2)) * 0, 0])
    liquid.align_to(body, DOWN).shift(UP * 0.05)
    cap = label(name, TEXT, 30).move_to([x, -3.25, 0])
    mk = chip(num, GOLD, 40).move_to([x - 1.55, 1.7 - 0.0, 0]) if False else VGroup()
    return VGroup(body, liquid, cap), body


class S03Golgi(Sc):
    def construct(self):
        year = T("1873", 36, font=TITLE_FONT)
        name = T("Camillo Golgi", 36, font=TITLE_FONT, color=TEXT)
        hd = VGroup(year, name).arrange(RIGHT, buff=0.5).move_to([0, 3.3, 0])
        ytgt = hd[0].get_center().copy()
        year.move_to([0, 3.3, 0])
        (b1, bd1), (b2, bd2) = bath(-3.4, "1  potassium dichromate", "1"), bath(3.4, "2  silver nitrate", "2")
        self.play(FadeIn(year), FadeIn(b1), FadeIn(b2), run_time=0.5)
        self.until(1.9)
        self.at("camillo golgi")
        self.play(year.animate.move_to(ytgt), FadeIn(name), run_time=0.5)
        self.at("found the black reaction")
        slab = Rectangle(width=1.7, height=0.6, stroke_color=PALE, stroke_width=2, fill_color=FIELD, fill_opacity=1).move_to([-3.4, 2.2, 0])
        self.play(FadeIn(slab), run_time=0.15)
        self.play(slab.animate.move_to([-3.4, -0.55, 0]), run_time=0.55)
        self.wait(0.2)
        self.play(Indicate(b1[2], color=GOLD, scale_factor=1.03), run_time=0.2)
        self.play(slab.animate.move_to([3.4, 2.2, 0]), run_time=0.45)
        self.play(slab.animate.move_to([3.4, -0.55, 0]), run_time=0.55)
        self.wait(0.2)
        self.at("most cells stay pale")
        pan = field()
        cells = pale_cells()
        self.play(FadeOut(b1), FadeOut(b2), Transform(slab, pan), run_time=0.8)
        self.play(FadeIn(cells), run_time=0.3)
        self.at("a few fill with black")
        ns = golgi_set()
        self.play(*[FadeIn(n.soma) for n in ns], run_time=0.3)
        cl = tag("branches that leave the section are cut off", GOLD, 28, (0, -3.35))
        self.add(cl)
        self.play(AnimationGroup(*[LaggedStart(*[Create(m) for m in n.lines()], lag_ratio=0.05) for n in ns],
                                 lag_ratio=0.2), run_time=1.8)
        cp = []
        for n in ns:
            cp += edge_cuts(n, 20)
        selected = []
        for test in (lambda p: p[0] > PX1-.06, lambda p: p[1] > PY1-.06):
            candidates = [p for p in cp if test(p)]
            if candidates: selected.append(candidates[0])
        cm = cut_marks(selected)
        self.play(Create(cm), run_time=0.5)
        self.finish()


class S04Sparse(Sc):
    def construct(self):
        pan, cells, ns = field(), pale_cells(), golgi_set()
        year = T("1873", 36, font=TITLE_FONT)
        name = T("Camillo Golgi", 36, font=TITLE_FONT)
        hd = VGroup(year, name).arrange(RIGHT, buff=0.5).move_to([0, 3.3, 0])
        mobs = [n.mob() for n in ns]
        self.add(pan, cells, *mobs, hd)
        self.at("sparse")
        self.play(Transform(hd, head("Sparse labelling")), run_time=0.5)
        cap = T("a few cells", 40, TEXT).move_to([0, -3.35, 0])
        glow = VGroup(*[Circle(radius=0.62, stroke_width=0, fill_color=GOLD, fill_opacity=0.45).move_to(n.soma.get_center()) for n in ns])
        self.at("a few cells")
        self.play(FadeIn(cap), FadeIn(glow), cells.animate.set_opacity(0.45), run_time=0.7)
        self.at("filled completely")
        self.remove(cap)
        cap = T("filled completely", 40, TEXT).move_to([0, -3.35, 0])
        self.add(cap)
        self.play(Indicate(mobs[1], scale_factor=1.03, color=INK), run_time=0.6)
        self.at("apparently at random")
        self.remove(cap)
        self.add(T("apparently at random", 40, TEXT).move_to([0, -3.35, 0]))
        self.play(Indicate(glow, scale_factor=1.04, color=GOLD), run_time=0.6)
        self.finish()


class S05Forest(Sc):
    LIT = [2, 5, 8]
    S = 1.55

    def construct(self):
        xs = np.linspace(-5.7, 5.7, 10)
        S = self.S
        dark = VGroup(*[tree(x, -3.7, S + 0.08 * (i % 3), 100 + i, GREY, 0.5) for i, x in enumerate(xs)])
        lit = VGroup(*[tree(xs[i], -3.7, S + 0.08 * (i % 3), 100 + i, TEXT, 0.95) for i in self.LIT])
        dots = VGroup(*[lights(xs[i], -3.7, S + 0.08 * (i % 3), 100 + i) for i in self.LIT])
        forest = VGroup(dark, lit, dots)
        if forest.width > 12.6:
            forest.scale(12.6 / forest.width, about_point=ORIGIN)
        forest.move_to([0, -0.35, 0])
        lb = tag("lit trees = stained cells", GOLD, 34, (0, 3.35))
        self.add(forest, lb)
        self.at("few trees lit")
        self.play(Indicate(lit, scale_factor=1.015, color=GOLD), run_time=0.6)
        self.at("each lit")
        self.at("shape stands out")
        self.play(LaggedStart(*[Indicate(VGroup(lit[k], dots[k]), scale_factor=1.05, color=GOLD) for k in range(3)], lag_ratio=0.3), run_time=1.2)
        self.finish()


class S06Whose(Sc):
    def construct(self):
        pan, cells = field(), pale_cells()
        n = GN([-3.3, -0.6], 1.55, 61, axon_ang=0.3, ax_len=2.7, dd=2, ad=3)
        m = n.mob()
        self.add(pan, cells)
        q = head("Whose branch?")
        self.play(FadeIn(m), FadeIn(q), run_time=0.6)
        pts = n.path_to_leaf()
        tr = smooth(pts[::-1], BLUE, 9)
        self.at("traced back")
        self.play(Create(tr), run_time=0.9)
        self.at("its own cell")
        self.play(Transform(q, head("Whose branch? Answered.", BLUE)), Indicate(m[1], color=BLUE, scale_factor=1.5), run_time=0.7)
        self.at("where the section allows")
        marks = cut_marks(edge_cuts(n, 4))
        edge_note = tag("cut off at the section edge", GOLD, 30, (0, -3.3))
        self.play(Create(marks), FadeIn(edge_note), run_time=0.6)
        self.until(3.95)
        # --- a contact has two sides
        q2 = head("A contact has two sides")
        self.play(FadeOut(m), FadeOut(tr), FadeOut(marks), FadeOut(edge_note), Transform(q, q2), run_time=0.3)
        cellp = Ellipse(width=1.8, height=1.7, stroke_color=PALE, stroke_width=3, fill_color=PALE, fill_opacity=0.3).move_to([1.65, 0, 0])
        br = VGroup(smooth([(-5.8, 0.9), (-4.0, 0.2), (-2.1, 0.45), (-0.9, 0.05), (0.72, 0.0)], INK, 10),
                    smooth([(-4.0, 0.2), (-4.5, -1.2), (-4.7, -2.3)], INK, 5),
                    smooth([(-2.1, 0.45), (-2.5, 1.5), (-2.4, 2.5)], INK, 5),
                    Dot([0.72, 0.0, 0], radius=0.17, color=INK))
        stained = Circle(radius=0.9, color=INK, fill_color=INK, fill_opacity=1).move_to([-4.0, 0.2, 0])
        self.play(FadeIn(cellp), FadeIn(stained), Create(br), run_time=0.6)
        self.at("a contact has")
        ring = DashedVMobject(Circle(radius=0.85, stroke_color=INK, stroke_width=5).move_to([0.8, 0, 0]), num_dashes=22)
        cl = tag("contact", INK if False else TEXT, 30, (0.8, 1.45))
        self.play(Create(ring), FadeIn(cl), run_time=0.5)
        self.at("two sides")
        l1 = label("stained side", TEXT, 30).move_to([-2.6, -3.3, 0])
        l2 = label("other side", TEXT, 30).move_to([2.6, -3.3, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.at("both are rarely stained")
        self.play(Transform(l2, label("other side: unstained", TEXT, 30).move_to([2.6, -3.3, 0])), Indicate(cellp, scale_factor=1.03, color=PALE), run_time=0.9)
        self.finish()


class S08Res(Sc):
    def construct(self):
        pan = field()
        self.add(pan)
        L = VGroup(smooth([(-5.9, -1.2), (-4.2, -0.5), (-2.4, 0.4), (-1.1, -0.1), (-0.1, 0.0)], INK, 13),
                   smooth([(-4.2, -0.5), (-4.5, 1.0), (-4.7, 2.2)], INK, 6),
                   smooth([(-2.4, 0.4), (-2.0, 1.6), (-2.2, 2.4)], INK, 6))
        R = VGroup(smooth([(5.9, 1.3), (4.1, 0.6), (2.4, -0.4), (1.1, 0.1), (0.1, 0.0)], INK, 13),
                   smooth([(4.1, 0.6), (4.6, -0.9), (4.4, -2.3)], INK, 6),
                   smooth([(2.4, -0.4), (2.1, -1.5), (2.4, -2.4)], INK, 6))
        hd = head("Where two black branches meet")
        self.add(hd, L, R)
        a = arr([0, 2.2, 0], [0, 0.3, 0], INK, 6)
        g = T("gap", 34, INK, weight=BOLD).move_to([0.8, 2.2, 0])
        self.add(a, g)
        self.wait(1.0)
        bl = blur_disc([0, 0, 0], 1.3)
        cap = tag("blur of a light microscope", RED, 30, (0, -3.35))
        self.play(FadeOut(a), FadeOut(g), FadeIn(bl), FadeIn(cap), run_time=0.6)
        self.at("the gap")
        g2 = tag("real gap, not resolved", INK if False else TEXT, 30, (0, 2.35))
        a2 = arr([0, 1.95, 0], [0, 1.38, 0], TEXT, 5, 0.2)
        self.play(FadeIn(g2), GrowArrow(a2), run_time=0.5)
        self.at("far below what light can show")
        self.play(Indicate(bl, scale_factor=1.06, color=RED), run_time=0.8)
        self.finish()


def lit_limb(pts, w=7, nd=7, color=TEXT):
    line = smooth(pts, color, w, 0.95)
    dots = VGroup(*[Dot(line.point_from_proportion(t), radius=0.065, color=color) for t in np.linspace(0.08, 1.0, nd)])
    return line, dots


class S09Forest2(Sc):
    def construct(self):
        xs = np.linspace(-5.7, 5.7, 10)
        dark = VGroup(*[tree(x, -3.6, 1.3 + 0.07 * (i % 3), 100 + i, GREY, 0.07) for i, x in enumerate(xs)])
        L_t = [smooth([(-3.2, -3.6), (-3.15, -2.4), (-3.1, -1.2)], TEXT, 8)]
        R_t = [smooth([(3.2, -3.6), (3.15, -2.4), (3.1, -1.2)], TEXT, 8)]
        limbs_l = [[(-3.1, -1.2), (-4.0, 0.0), (-4.5, 1.2), (-4.8, 2.4)], [(-3.1, -1.2), (-3.2, 0.3), (-3.4, 1.6), (-3.2, 2.8)],
                   [(-4.0, 0.0), (-5.0, 0.4), (-5.8, 0.4)], [(-3.2, 0.3), (-2.3, 1.2), (-1.8, 2.2)]]
        limbs_r = [[(3.1, -1.2), (4.0, 0.0), (4.5, 1.2), (4.8, 2.4)], [(3.1, -1.2), (3.2, 0.3), (3.4, 1.6), (3.2, 2.8)],
                   [(4.0, 0.0), (5.0, 0.4), (5.8, 0.4)], [(3.2, 0.3), (2.3, 1.2), (1.8, 2.2)]]
        tl = [lit_limb(p, 5, 4) for p in limbs_l] + [(L_t[0], VGroup())]
        tr = [lit_limb(p, 5, 4) for p in limbs_r] + [(R_t[0], VGroup())]
        A = lit_limb([(-3.1, -1.2), (-2.0, -0.5), (-0.8, 0.0), (0.05, 0.55), (1.7, 1.65)], 9, 7, BLUE)
        B = lit_limb([(3.1, -1.2), (2.0, -0.7), (0.9, 0.0), (0.05, 0.55), (-1.7, 1.7)], 9, 7, YELLOW)
        side = VGroup(*[x for pair in tl + tr for x in pair])
        hd = head("Two lit branches, from two different trees", TEXT, 34, y=3.35)
        self.add(dark, side, hd)
        self.at("branches cross")
        self.play(Create(A[0]), Create(B[0]), run_time=1.2)
        self.play(FadeIn(A[1]), FadeIn(B[1]), run_time=0.4)
        self.at("still cannot tell")
        ring = DashedVMobject(Circle(radius=0.85, stroke_color=GOLD, stroke_width=5).move_to([0.05, 0.55, 0]), num_dashes=20)
        q = head("Touch or fusion?", GOLD, 40, y=3.3)
        self.play(Create(ring), Transform(hd, q), run_time=0.7)
        self.at("grafted together")
        un = tag("not answered", TEXT, 34, (0.05, -0.85))
        self.play(FadeIn(un), run_time=0.2)
        self.finish()


class S10Cajal(Sc):
    def construct(self):
        cy = 0.35
        pan = RoundedRectangle(corner_radius=0.2, width=12.2, height=6.0, stroke_color=GREY, stroke_width=2,
                               fill_color=FIELD, fill_opacity=1).move_to([0, cy, 0])
        cells = pale_cells(seed=8, n=10).move_to([0, cy, 0])
        bnd = (-6.1, 6.1, cy - 3.0, cy + 3.0)
        ns = [GN([-3.4 + 3.4 * i, cy + (0.7 if i % 2 else -0.5)], 1.15, 70 + i, bounds=bnd,
                 axon_ang=0.4 - 0.5 * i, ax_len=2.8) for i in range(3)]
        mobs = [n.mob() for n in ns]
        tissue = VGroup(pan, cells, *mobs)
        tissue.stretch(0.8, 1, about_point=[0, 3.35, 0])
        yr = label("Madrid, 1887", GOLD, 34).move_to([0, -3.3, 0])
        nm = T("Santiago Ramón y Cajal", 44, font=TITLE_FONT).move_to([0, -2.35, 0])
        self.add(tissue, nm)
        self.at("took up the stain")
        self.play(FadeIn(yr), run_time=0.4)
        self.at("took up the stain")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.05, color=INK) for m in mobs], lag_ratio=0.25), run_time=1.0)
        self.finish()


NDG = nodes_at(1.04, 1.02, 0, -0.1)


def big_panel():
    return pic_panel(0, -0.1, 12.2, 5.7)


class S11Net(Sc):
    def construct(self):
        pan = big_panel()
        ed, jn = golgi_pic(NDG, 6)
        self.add(pan, ed, jn)
        self.at("golgi read")
        hd = head("Golgi's reading", ORANGE)
        self.play(FadeIn(hd), run_time=0.35)
        self.at("a continuous net")
        hl = VGroup(*[Dot([p[0], p[1], 0], radius=0.2, color=ORANGE) for p in NDG])
        cp = tag("branches merge into one net", ORANGE, 32, (0, -3.35))
        self.play(FadeIn(hl), FadeIn(cp), Transform(hd, head("Golgi's reading: one continuous net", ORANGE, 34)), run_time=0.9)
        self.finish()


class S12Free(Sc):
    def construct(self):
        pan = big_panel()
        ed, jn = golgi_pic(NDG, 6)
        hl = VGroup(*[Dot([p[0], p[1], 0], radius=0.2, color=ORANGE) for p in NDG])
        hd = head("Golgi's reading: one continuous net", ORANGE, 34)
        cp = tag("branches merge into one net", ORANGE, 32, (0, -3.35))
        self.add(pan, ed, jn, hl, hd, cp)
        self.at("found branches")
        ced, cells, bl = cajal_pic(NDG, 6, 0.3, 0.7)
        self.play(Transform(hd, head("Cajal's reading", GREEN)), Transform(ed, ced), FadeOut(jn), FadeOut(hl), FadeIn(cells),
                  Transform(cp, tag("branches end near other cells, not joined", GREEN, 32, (0, -3.35))), run_time=1.0)
        self.play(FadeIn(bl), run_time=0.2)
        self.at("close to other cells")
        self.play(LaggedStart(*[Indicate(bl[k], scale_factor=2.4, color=GREEN) for k in (0, 5, 9)], lag_ratio=0.25), run_time=1.0)
        self.at("again and again")
        self.play(LaggedStart(*[Indicate(b, scale_factor=2.4, color=GREEN) for b in bl], lag_ratio=0.12), run_time=1.4)
        self.finish()


class S13Blind(Sc):
    def construct(self):
        nl, nr = nodes_at(0.5, 0.82, -3.4, -0.1), nodes_at(0.5, 0.82, 3.4, -0.1)
        pl, pr = pic_panel(-3.4, -0.1, 6.3, 5.3), pic_panel(3.4, -0.1, 6.3, 5.3)
        gl, gj = golgi_pic(nl, 4)
        cr, cc, cb = cajal_pic(nr, 4, 0.2, 0.42)
        t1, t2 = label("Golgi's reading", ORANGE, 30).move_to([-3.4, 3.3, 0]), label("Cajal's reading", GREEN, 30).move_to([3.4, 3.3, 0])
        self.add(pl, pr, gl, gj, cr, cc, cb, t1, t2)
        ci = 6
        b1, b2 = blur_disc(nl[ci], 0.85), blur_disc(nr[ci], 0.85)
        cp = tag("same blur, same contact", RED, 32, (0, -3.35))
        self.wait(0.35)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(cp), run_time=0.5)
        self.at("win at the contact")
        self.play(Indicate(VGroup(b1, b2), scale_factor=1.03), run_time=0.4)
        self.until(2.3)
        rng = np.random.default_rng(9)
        thicket = VGroup()
        for _ in range(80):
            x, y = rng.uniform(-6, 6), rng.uniform(-3, 3)
            a = rng.uniform(0, 6.3)
            pts = [np.array([x, y])]
            for _ in range(6):
                a += rng.uniform(-.8, .8)
                q = pts[-1] + 0.7 * np.array([np.cos(a), np.sin(a)])
                if abs(q[0]) > 6.2 or abs(q[1]) > 3.2:
                    break
                pts.append(q)
            if len(pts) >= 3:
                thicket.add(smooth(pts, GREY, 3, 0.7))
        wood = VGroup(*[tree(x, -3.6, 1.6, 500 + i, GREY, 0.9, depth=2, wscale=0.9) for i, x in enumerate([-5.0, -2.5, 0.0, 2.5, 5.0])])
        wood.scale(min(1.0, 12.6 / wood.width, 5.8 / wood.height)).move_to([0, -0.35, 0])
        tl = tag("crowded thicket", TEXT, 34, (0, 3.3))
        self.play(FadeOut(VGroup(pl, pr, gl, gj, cr, cc, cb, t1, t2, b1, b2, cp)), FadeIn(thicket), FadeIn(tl), run_time=0.4)
        self.at("turned to embryos")
        self.play(Indicate(thicket, scale_factor=1.0, color=GREY), run_time=0.4)
        self.at("cells are fewer")
        emb = head("Embryo: fewer cells, simpler", TEXT, 38)
        self.play(FadeOut(thicket), FadeOut(tl), FadeIn(wood), FadeIn(emb), run_time=0.6)
        self.at("fewer and simpler")
        self.play(Indicate(wood, scale_factor=1.04, color=TEXT), run_time=0.8)
        self.finish()


def tube_cells(c):
    g = VGroup()
    for r, n, rad in [(1.3, 12, 0.19), (1.9, 16, 0.17), (2.5, 22, 0.15)]:
        for k in range(n):
            a = 2 * np.pi * k / n + (0.1 if r == 1.9 else 0)
            p = c + r * np.array([np.cos(a), np.sin(a), 0])
            if r == 1.9 and abs(a - 0.1) < 0.2:
                continue
            if r == 2.5 and k == 0:
                continue
            g.add(Circle(radius=rad, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18).move_to(p))
    return g


class S14His(Sc):
    def construct(self):
        C = np.array([-0.8, -0.2, 0.0])
        wall = Circle(radius=2.95, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to(C)
        lumen = Circle(radius=0.8, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(C)
        cells = tube_cells(C)
        divs = VGroup()
        for a in (2.3, 3.6, 5.2):
            p = C + 1.3 * np.array([np.cos(a), np.sin(a), 0])
            t = np.array([-np.sin(a), np.cos(a), 0])
            d = VGroup(Circle(radius=0.17, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3).move_to(p - 0.16 * t),
                       Circle(radius=0.17, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3).move_to(p + 0.16 * t))
            divs.add(d)
        who = head("Wilhelm His", TEXT)
        self.play(FadeIn(who), Create(wall), run_time=0.6)
        self.play(FadeIn(lumen), FadeIn(cells), FadeIn(divs), run_time=0.7)
        l1 = label("dividing cells", TEXT, 30).move_to([-5.0, 1.9, 0])
        a1 = arr([-4.05, 1.75, 0], list(C + 1.3 * np.array([np.cos(2.3), np.sin(2.3), 0]) + [-0.25, 0.1, 0]), TEXT, 4, 0.18)
        l2 = label("central cavity", TEXT, 30).move_to([-5.0, -1.9, 0])
        a2 = arr([-4.05, -1.7, 0], list(C + [-0.5, -0.1, 0]), TEXT, 4, 0.18)
        self.play(FadeIn(l1), FadeIn(a1), FadeIn(l2), FadeIn(a2), run_time=0.4)
        nb_p = C + 2.2 * np.array([1, 0, 0])
        nb = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.55).move_to(nb_p)
        self.play(FadeIn(nb), run_time=0.2)
        ln = tag("neuroblast", BLUE, 34, (3.5, 1.6))
        an = arr([2.9, 1.3, 0], list(nb_p + [0.3, 0.2, 0]), BLUE, 5, 0.2)
        self.add(ln, an)
        self.at("grows out")
        fib = smooth([nb_p + [0.25, 0, 0], (1.9, -0.1), (3.3, -0.45), (4.8, 0.0), (6.3, -0.15)], BLUE, 7)
        self.play(Create(fib), run_time=0.7)
        self.at("single cell")
        self.play(Indicate(nb, scale_factor=2.0, color=BLUE), run_time=0.6)
        self.at("a neuroblast")
        self.play(Indicate(nb, color=BLUE, scale_factor=1.2), run_time=0.3)
        cp = tag("one fibre, one cell", TEXT, 32, (2.2, -3.4))
        self.play(FadeIn(cp), run_time=0.5)
        self.finish()


def cone_group(x0, y0=0.0, s=1.0):
    """a fibre tip that swells into a rounded cone with curved filopodia (a still drawing)."""
    shaft = smooth([(-6.4, y0 - 0.5), (-4.6, y0 + 0.15), (-3.0, y0 - 0.25), (x0 + 0.55 * s, y0)], BLUE, 11)
    cx = x0 + 1.15 * s
    ring = []
    for ang in np.linspace(0, 2 * np.pi, 13)[:-1]:
        rr = 1.0 + 0.1 * np.cos(2 * ang)
        ring.append((cx + 1.2 * s * rr * np.cos(ang) * (1.0 if np.cos(ang) > 0 else 0.55), y0 + 1.3 * s * rr * np.sin(ang) * (1.0 if np.cos(ang) > 0 else 0.45)))
    body = VMobject()
    body.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in ring + [ring[0]]])
    body.set_stroke(BLUE, 5)
    body.set_fill(BLUE, 0.3)
    spikes = VGroup()
    for k, ang in enumerate(np.linspace(-1.35, 1.35, 11)):
        base = np.array([cx + 1.2 * s * np.cos(ang), y0 + 1.3 * s * np.sin(ang)])
        d = np.array([np.cos(ang), np.sin(ang)])
        nrm = np.array([-d[1], d[0]])
        L = (0.95 + 0.25 * (k % 3)) * s
        bend = 0.25 * s * (1 if k % 2 else -1)
        pts = [base, base + d * L * 0.5 + nrm * bend, base + d * L + nrm * bend * 0.4]
        spikes.add(smooth(pts, BLUE, 4))
    return shaft, body, spikes


class S15Cone(Sc):
    def construct(self):
        shaft, body, spikes = cone_group(-1.6, 0.0, 1.3)
        top = label("chick embryo, 1890", GOLD, 30).move_to([-3.4, -3.35, 0])
        self.add(shaft, body, spikes, top)
        self.at("named the growth cone")
        self.play(Indicate(body, scale_factor=1.02, color=BLUE), run_time=0.4)
        gc = label("growth cone", BLUE, 38).move_to([0.2, 3.3, 0])
        ld = Line([0.2, 2.95, 0], [0.1, 1.75, 0], color=BLUE, stroke_width=4)
        self.play(FadeIn(gc), Create(ld), run_time=0.5)
        self.at("he read it")
        note = label("drawn from fixed specimens", LIGHT, 30).move_to([3.5, -3.35, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("advancing end")
        ad = arr([3.5, 0.0, 0], [5.4, 0.0, 0], GREEN, 8)
        al = tag("advancing end?", GREEN, 32, (4.5, 0.75))
        self.play(GrowArrow(ad), FadeIn(al), run_time=0.7)
        self.at("growing fiber")
        self.play(Indicate(shaft, scale_factor=1.0, color=BLUE), run_time=0.8)
        self.finish()


def card_frame():
    return RoundedRectangle(corner_radius=0.3, width=12.4, height=6.7, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.05)


def predict_cell():
    return Circle(radius=1.2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([-4.4, -0.55, 0])


def predict_fib():
    return smooth([(-3.2, -0.55), (-2.7, 0.05), (-2.1, -0.95), (-1.35, -0.4)], BLUE, 9)


def predict_net():
    nd = nodes_at(0.46, 0.55, 3.6, -0.45)
    return VGroup(net_edges(nd, ORANGE, 5), net_dots(nd, ORANGE, 0.1))


def predict_text():
    return VGroup(T("Does outgrowth from one cell", 42, TEXT, font=TITLE_FONT), T("rule out a net?", 42, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.18).move_to([0, 1.65, 0])


def predict_labels():
    return label("one cell with a fibre", TEXT, 30).move_to([-3.3, -2.3, 0]), label("Golgi's net", ORANGE, 30).move_to([3.6, -2.3, 0])


class S16Predict(Sc):
    def construct(self):
        fr = card_frame()
        tag_ = chip("PREDICT", TEAL, 30).move_to([0, 2.85, 0])
        txt = predict_text()
        cell, fib, net = predict_cell(), predict_fib(), predict_net()
        l1, l2 = predict_labels()
        self.add(fr, tag_, txt, cell, fib, net, l1, l2)
        self.at("grow out of one cell")
        self.play(Indicate(fib, scale_factor=1.02), run_time=0.5)
        self.at("does that rule out")
        self.play(Indicate(net, scale_factor=1.02), run_time=0.5)
        self.play(Indicate(txt, scale_factor=1.03, color=TEXT), run_time=0.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        fr = card_frame()
        tag_ = chip("PREDICT", TEAL, 30).move_to([0, 2.85, 0])
        l1, l2 = predict_labels()
        self.add(fr, tag_, predict_text(), predict_cell(), predict_fib(), predict_net(), l1, l2)
        pr = T("Pause. Decide: yes or no?", 32, TEAL).move_to([0, -2.95, 0])
        self.add(pr)
        t = ValueTracker(1.0)
        ring_bg = Circle(radius=0.7, stroke_color=GREY, stroke_width=4).move_to([-0.05, -0.55, 0])
        ring = always_redraw(lambda: Arc(radius=0.7, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 0.001),
                                        stroke_color=TEAL, stroke_width=10).move_to([-0.05, -0.55, 0]) if False else
                             Arc(radius=0.7, start_angle=PI / 2, angle=TAU * max(t.get_value(), 0.001),
                                 stroke_color=TEAL, stroke_width=10, arc_center=[-0.05, -0.55, 0]))
        num = always_redraw(lambda: T(str(max(1, int(np.ceil(5 * t.get_value() - 1e-6)))), 40, TEXT).move_to([-0.05, -0.55, 0]))
        self.add(ring_bg, ring, num)
        self.play(t.animate.set_value(0.0), run_time=4.7, rate_func=linear)
        self.finish()


def soma(color, center, r=1.5):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to(center)


class S18Reveal(Sc):
    A = np.array([-4.9, -0.2, 0.0])
    B = np.array([4.9, 0.8, 0.0])

    def construct(self):
        a, b = soma(BLUE, self.A, 1.6), soma(YELLOW, self.B, 1.6)
        no = head("No.", TEXT, 46, y=3.3)
        self.add(a, b)
        self.play(FadeIn(no), run_time=0.4)
        pts = [self.A + [1.6, 0.1, 0], (-2.6, -1.4), (-0.8, 0.8), (1.0, -0.6), (2.6, 0.6), self.B + [-1.6, -0.1, 0]]
        full = smooth(pts, BLUE, 9)
        stub = smooth(pts[:2], BLUE, 9)
        self.at("outgrowth shows")
        self.play(Create(stub), run_time=0.6)
        self.at("where a fiber begins")
        st = tag("begins here", BLUE, 34, (-2.7, -2.7))
        sa = arr([-3.4, -2.35, 0], list(self.A + [1.65, -0.5, 0]), BLUE, 5, 0.2)
        self.play(FadeIn(st), FadeIn(sa), run_time=0.4)
        self.play(Transform(stub, full), run_time=0.65)
        self.at("not how it ends")
        nc = tag("Not how it ends", TEXT, 36, (0, -3.4))
        # The contact is visible before its uncertainty is named.
        ring = DashedVMobject(Circle(radius=0.75, stroke_color=TEXT, stroke_width=5).move_to(self.B + [-1.6, -0.1, 0]), num_dashes=16)
        fz = VGroup(T("?", 64, TEXT, weight=BOLD), T("ends how? fuse?", 34, TEXT)).arrange(RIGHT, buff=0.25).move_to([1.4, 2.5, 0])
        fz = VGroup(tag("ends how? fuse?", TEXT, 36, (1.4, 2.5)))
        qm = T("?", 72, TEXT, weight=BOLD).move_to(self.B + [-1.6, 1.05, 0])
        self.play(Create(ring), FadeIn(fz), FadeIn(qm), run_time=0.45)
        self.play(FadeIn(nc), run_time=0.4)
        self.at("fiber could grow out")
        self.play(FadeOut(st), FadeOut(sa), run_time=0.4)
        self.at("then fuse")
        self.play(Indicate(ring, color=TEXT, scale_factor=1.08), run_time=0.6)
        self.finish()


def evidence_cards():
    hd = head("What embryo evidence establishes", TEXT, 38)
    left = RoundedRectangle(width=5.9, height=4.9, corner_radius=0.25,
                            color=GREEN, fill_color=GREEN, fill_opacity=0.08).move_to([-3.2,-0.1,0])
    right = DashedVMobject(RoundedRectangle(width=5.9,height=4.9,corner_radius=0.25,
                          color=TEXT),num_dashes=45).move_to([3.2,-0.1,0])
    cell = soma(BLUE,[-4.7,0.5,0],0.6)
    fib = smooth([(-4.1,0.5),(-3.4,1.1),(-2.7,0),(-1.5,0.5)],BLUE,8)
    cells = T("separate cells",36,GREEN).move_to([-3.2,-0.8,0])
    uncertain = T("?",96,TEXT).move_to([3.2,0.65,0])
    ends = T("the final contact",32,TEXT).move_to([3.2,-0.8,0])
    ml = T("more likely",42,GREEN).move_to([-3.2,-1.8,0])
    ns = T("not settled",42,TEXT).move_to([3.2,-1.8,0])
    return VGroup(hd,left,right,cell,fib,cells,uncertain,ends), ml, ns


class S19Reveal2(Sc):
    def construct(self):
        base, ml, ns = evidence_cards()
        self.add(base)
        self.at("more likely")
        self.play(FadeIn(ml), run_time=0.4)
        self.at("without settling it")
        self.play(FadeIn(ns), run_time=0.4)
        self.finish()


class S20Beat(NarratedScene):
    def construct(self):
        base, ml, ns = evidence_cards()
        self.add(base, ml, ns)
        self.finish()


CH_SX, CH_SP = 0.85, 4.6


def neuron_xy(color, sx, sy):
    pts = [(-2.1, 1.15), (-1.3, .65), (-1.05, .35), (-.85, .43), (-1.0, 1.25),
           (-.78, 1.25), (-.55, .48), (-.25, .3), (.05, .13), (1.7, .13),
           (2.1, .6), (2.23, .48), (1.86, 0), (2.23, -.48), (2.1, -.6),
           (1.7, -.13), (.05, -.13), (-.25, -.3), (-.55, -.48), (-.78, -1.25),
           (-1.0, -1.25), (-.85, -.43), (-1.05, -.35), (-1.3, -.65),
           (-2.1, -1.15), (-2.23, -.98), (-1.55, -.42), (-1.24, 0),
           (-1.55, .42), (-2.23, .98)]
    return Polygon(*[[x * sx, y * sy, 0] for x, y in pts], stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=.15).round_corners(.07)


def build_chain(sy, cy):
    sx = CH_SX
    xs = [-CH_SP, 0, CH_SP]
    cells = VGroup(*[neuron_xy(c, sx, sy).move_to([x, cy, 0]) for x, c in zip(xs, [BLUE, YELLOW, BLUE])])
    seg1 = VGroup(*[arr([x - 1.7 * sx, cy, 0], [x - 0.1 * sx, cy, 0], TEAL, 7, 0.2) for x in xs])
    seg2 = VGroup(*[arr([x - 0.1 * sx, cy, 0], [x + 1.75 * sx, cy, 0], TEAL, 7, 0.2) for x in xs])
    gaps = VGroup(*[arr([x + 2.3 * sx, cy, 0], [x + CH_SP - 2.3 * sx, cy, 0], TEAL, 7, 0.2) for x in xs[:2]])
    return cells, seg1, seg2, gaps


class S21Polar(Sc):
    def construct(self):
        cy, sy = 0.45, 1.85
        cells, seg1, seg2, gaps = build_chain(sy, cy)
        names = VGroup()
        hd = head("Dynamic polarization", TEAL, 38, y=3.5)
        base, ml, ns = evidence_cards()
        previous = VGroup(base, ml, ns)
        self.add(previous)
        self.play(FadeOut(previous), run_time=0.2)
        self.play(FadeIn(cells), run_time=0.25)
        self.at("added a rule")
        self.play(FadeIn(hd), run_time=0.5)
        self.at("signals enter")
        self.play(LaggedStart(*[GrowArrow(e) for e in seg1], lag_ratio=0.15), run_time=0.55)
        sxx = CH_SX
        self.at("the dendrites", lead=0.35)
        ld = label("dendrites", TEXT, 30).move_to([-2.5, -2.45, 0])
        l1 = Line([-2.2, -2.15, 0], [-2.0 * sxx - 0.15, cy - 1.0 * sy, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(ld), Create(l1), run_time=0.4)
        self.at("cell body", lead=0.3)
        lb = label("cell body", TEXT, 30).move_to([0.0, -2.45, 0])
        l2 = Line([-0.1, -2.15, 0], [-0.4 * sxx, cy - 0.55, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(lb), Create(l2), run_time=0.4)
        self.at("leave through the axon", lead=0.1)
        la = label("axon", TEXT, 30).move_to([2.5, -2.45, 0])
        l3 = Line([2.4, -2.15, 0], [1.3 * sxx, cy - 0.18, 0], color=TEXT, stroke_width=3)
        self.play(LaggedStart(*[GrowArrow(e) for e in seg2], lag_ratio=0.15), LaggedStart(*[GrowArrow(e) for e in gaps], lag_ratio=0.3),
                  FadeIn(la), Create(l3), run_time=1.0)
        self.finish()


class S22Polar2(Sc):
    def construct(self):
        big = VGroup(*build_chain(0.8, 2.0))
        sc = tag("separate cells", TEXT, 32, (-4.7, 3.35))
        dl = label("order sets a direction", TEXT, 32).move_to([-3.0, 0.45, 0])
        nd = nodes_at(0.9, 0.5, 0, -1.55)
        net = VGroup(net_edges(nd, ORANGE, 5), net_dots(nd, ORANGE, 0.1))
        ln = label("one continuous net", ORANGE, 32).move_to([3.4, 0.45, 0])
        self.add(big, sc, dl, net, ln)
        self.at("their order sets a direction")
        self.play(Indicate(big[1], color=TEAL, scale_factor=1.04),
                  Indicate(big[2], color=TEAL, scale_factor=1.04), run_time=0.9)
        self.at("continuity alone")
        cap = T("Continuity alone sets no direction", 36, TEXT).move_to([0, -3.15, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.at("sets none")
        qs = VGroup()
        for k in range(1, len(EDGES), 4):
            a, b = EDGES[k]
            m = (nd[a] + nd[b]) / 2
            qs.add(tag("?", TEXT, 44, (m[0], m[1]), pad=0.04, weight=BOLD))
        self.play(LaggedStart(*[FadeIn(q, scale=1.4) for q in qs], lag_ratio=0.12), run_time=1.0)
        self.at("the rule has exceptions")
        ex_note = T("The rule has exceptions", 28, LIGHT).move_to([0, -3.65, 0])
        self.play(FadeIn(ex_note), run_time=0.6)
        self.finish()


class S23Nobel(Sc):
    def construct(self):
        yr = T("1906", 56, font=TITLE_FONT, color=GOLD)
        pr = T("Nobel Prize in Physiology or Medicine", 34, font=TITLE_FONT)
        top = VGroup(yr, pr).arrange(RIGHT, buff=0.5).move_to([0, 3.3, 0])
        self.play(FadeIn(yr), run_time=0.5)
        self.play(FadeIn(pr), run_time=0.5)
        self.at("golgi and")
        g = chip("Camillo Golgi", ORANGE, 32).move_to([-3.4, 2.15, 0])
        c = chip("Santiago Ramón y Cajal", GREEN, 30).move_to([3.4, 2.15, 0])
        pl, pr2 = pic_panel(-3.4, -0.75, 6.3, 4.0), pic_panel(3.4, -0.75, 6.3, 4.0)
        nl, nr = nodes_at(0.52, 0.7, -3.4, -0.75), nodes_at(0.52, 0.7, 3.4, -0.75)
        ged, gj = golgi_pic(nl, 4)
        ced, cc, cb = cajal_pic(nr, 4, 0.22, 0.48)
        self.play(FadeIn(g), FadeIn(c), FadeIn(pl), FadeIn(pr2), run_time=0.7)
        self.play(FadeIn(ged), FadeIn(gj), FadeIn(ced), FadeIn(cc), FadeIn(cb), run_time=0.5)
        self.at("shared the nobel prize")
        self.play(Indicate(VGroup(g, c), scale_factor=1.04, color=TEXT), run_time=0.8)
        fe = label("free endings", GREEN, 32).move_to([3.4, -3.3, 0])
        self.play(FadeIn(fe), run_time=0.4)
        self.at("still defended his net")
        nl_ = label("still defended his net", ORANGE, 32).move_to([-3.4, -3.3, 0])
        self.play(FadeIn(nl_), Indicate(ged, color=ORANGE, scale_factor=1.03), run_time=0.8)
        self.finish()


class S24Take(Sc):
    def construct(self):
        L = RoundedRectangle(corner_radius=0.6, width=5.2, height=4.4, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                             fill_opacity=0.14).move_to([-2.75, 0.3, 0])
        R = RoundedRectangle(corner_radius=0.6, width=5.2, height=4.4, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                             fill_opacity=0.14).move_to([2.75, 0.3, 0])
        la, lb = T("cell A", 38, BLUE).move_to([-3.9, 0.3, 0]), T("cell B", 38, YELLOW).move_to([3.9, 0.3, 0])
        hd = head("A gap no light microscope could resolve", TEXT, 36, y=3.3)
        self.add(L, R, la, lb, hd)
        gp = tag("real gap, not resolved", TEXT, 30, (0, -2.7))
        ga = arr([0, -2.35, 0], [0, -1.6, 0], TEXT, 5, 0.2)
        self.play(FadeIn(gp), GrowArrow(ga), run_time=0.5)
        self.wait(0.3)
        bl = blur_disc([0, 0.3, 0], 2.35, smear="#D8D2B0")
        cap = tag("the blur hides the gap", RED, 32, (0, -2.7))
        self.play(FadeOut(gp), FadeOut(ga), FadeIn(bl), run_time=0.6)
        self.play(FadeIn(cap), run_time=0.3)
        self.at("separate cells were the better")
        self.play(Transform(cap, tag("Separate cells: the better explanation", GREEN, 34, (0, -2.7))), run_time=0.7)
        self.at("nobody had seen it")
        ns = tag("not yet seen", RED, 36, (0, -3.35))
        self.play(FadeIn(ns), Indicate(bl, scale_factor=1.08, color=RED), run_time=0.8)
        self.finish()


class S25End(EndCard):
    LINE = "Separate cells: the better explanation, not yet seen."

    def construct(self):
        a, b = self.LINE.split(", ", 1)
        line = VGroup(T(a + ",", 48, font=TITLE_FONT), T(b, 48, font=TITLE_FONT)).arrange(DOWN, buff=0.25)
        sub = T("biochemistrypedia.com", size=28, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
