"""From Cluster to Cell Type (sensory-neuron-atlas, chapter 1).
COLOR MAP: BLUE neuron/type, TEAL RNA profile, GOLD genetic label, GREEN physiology, RED injury state, GREY uncertainty.
Everything is schematic: dot positions are hand-placed; the calcium trace is computed (spikes convolved with an exponential)."""
import numpy as np
from bp_style import *  # noqa: F401,F403

CY = [2.35, 0.2, -1.95]            # cluster centre y
CX = -2.2                        # cluster centre x
GC = np.array([0.0, -0.3, 0.0])  # ganglion centre
N = 45


def _disc(rng, c, s):
    while True:
        p = rng.normal(0, s / 2.0, 2)
        if np.hypot(*p) < s:
            return np.array([c[0] + p[0], c[1] + p[1], 0.0])


def gang_pos():
    rng = np.random.RandomState(7)
    out = []
    while len(out) < N:
        x, y = rng.uniform(-4.6, 4.6), rng.uniform(-2.6, 2.6)
        if (x / 4.6) ** 2 + (y / 2.6) ** 2 < 0.88:
            out.append(np.array([x, y - 0.3, 0.0]))
    return out


def cluster_pos(center=None, spread=0.8, ys=None):
    rng = np.random.RandomState(11)
    ys = ys or CY
    return [_disc(rng, [CX, ys[i % 3]], spread) for i in range(N)]


def split_pos():
    rng = np.random.RandomState(13)
    out = []
    for i in range(N):
        sgn = 1 if (i // 3) % 2 == 0 else -1
        out.append(_disc(rng, [CX, CY[i % 3] + 0.58 * sgn], 0.45))
    return out


def big_pos():
    """cluster 1 enlarged, the others stay."""
    base = cluster_pos()
    rng = np.random.RandomState(17)
    return [(_disc(rng, [CX, 1.4], 1.0) if i % 3 == 0 else base[i]) for i in range(N)]


IDX1 = [i for i in range(N) if i % 3 == 0]
IDX_OTHER = [i for i in range(N) if i % 3 != 0]


class DotField:
    """45 neuron dots. pos = lerp(src, dst, p) + slow wobble; colour = lerp(col0, col1, c); faded by masks."""

    def __init__(self, scene, base, fo=0.8, amp=0.18, so=0.9):
        self.s = scene
        self.fo, self.amp, self.so = fo, amp, so
        self.src = [np.array(b, dtype=float) for b in base]
        self.dst = [np.array(b, dtype=float) for b in base]
        self.col0 = [ManimColor(BLUE)] * N
        self.col1 = [ManimColor(BLUE)] * N
        self.p, self.c = ValueTracker(1), ValueTracker(1)
        self.fades = []
        rng = np.random.RandomState(3)
        self.dots = VGroup()
        for i in range(N):
            d = Circle(radius=0.19, stroke_width=4, stroke_color=BLUE).set_fill(BLUE, fo)
            d.i = i
            d.w = rng.uniform(0.5, 1.1, 2)
            d.ph = rng.uniform(0, 6.28, 2)
            d.add_updater(self._upd)
            d.move_to(self.src[i])
            self.dots.add(d)

    def _col(self, i):
        return interpolate_color(self.col0[i], self.col1[i], self.c.get_value())

    def _pos(self, i):
        a = self.p.get_value()
        return self.src[i] * (1 - a) + self.dst[i] * a

    def _upd(self, d):
        t = self.s.renderer.time
        i = d.i
        off = self.amp * np.array([np.sin(d.w[0] * t + d.ph[0]), np.cos(d.w[1] * t + d.ph[1]), 0])
        d.move_to(self._pos(i) + off)
        k = 1.0
        for tr, S in self.fades:
            if i in S:
                k *= 1 - 0.9 * tr.get_value()
        d.set_fill(self._col(i), opacity=self.fo * k)
        d.set_stroke(BLUE, 4, opacity=self.so * k)

    def fade(self, idx):
        tr = ValueTracker(0)
        self.fades.append((tr, set(idx)))
        return tr

    def prep(self, dst=None, cols=None):
        cur = [self._pos(i) for i in range(N)]
        curc = [self._col(i) for i in range(N)]
        self.src = cur
        self.dst = [np.array(x, dtype=float) if x is not None else cur[i] for i, x in enumerate(dst)] if dst else list(cur)
        self.col0 = curc
        self.col1 = [ManimColor(x) if x is not None else curc[i] for i, x in enumerate(cols)] if cols else list(curc)
        self.p.set_value(0)
        self.c.set_value(0)
        return [self.p.animate.set_value(1), self.c.animate.set_value(1)]


def sch():
    return T("schematic", 28, TEXT).move_to([-5.5, 3.45, 0])


def ganglion():
    e = Ellipse(width=10.4, height=6.0, stroke_color=GREY, stroke_width=5, fill_color=BLUE, fill_opacity=0.2)
    return e.move_to(GC)


def tree_lines(dim_others=False):
    g = VGroup()
    trunk = Line([-6.0, CY[1], 0], [-4.8, CY[1], 0])
    vert = Line([-4.8, CY[0], 0], [-4.8, CY[2], 0])
    hs = [Line([-4.8, y, 0], [-3.4, y, 0]) for y in CY]
    for m in [trunk, vert, *hs]:
        m.set_stroke(TEXT, 12, opacity=0.95)
    g.add(trunk, vert, *hs)
    g.trunk, g.vert, g.h = trunk, vert, hs
    return g


def split_lines():
    ls = VGroup()
    for y in CY:
        for sgn in (1, -1):
            ls.add(Line([-3.4, y, 0], [-3.1, y + 0.58 * sgn, 0]).set_stroke(TEXT, 6, opacity=0.9))
    return ls


def make_dial(c, r, tr):
    c = np.array([c[0], c[1], 0.0])
    ring = Circle(r, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.22).move_to(c)
    ang = lambda v: np.radians(210 - 240 * v)
    dr = lambda a: np.array([np.cos(a), np.sin(a), 0])
    ticks = VGroup(*[Line(c + 0.8 * r * dr(ang(v)), c + 0.95 * r * dr(ang(v))).set_stroke(TEAL, 3) for v in np.linspace(0, 1, 9)])
    needle = Line(c, c + 0.75 * r * dr(ang(tr.get_value()))).set_stroke(TEXT, 6)
    needle.add_updater(lambda m: m.put_start_and_end_on(c, c + 0.75 * r * dr(ang(tr.get_value()))))
    hub = Dot(c, radius=0.1, color=TEXT)
    g = VGroup(ring, ticks, needle, hub)
    g.ring = ring
    return g


def sock(label, pos, w=5.6, h=1.0, color=TEXT):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=3), num_dashes=40)
    t = T(label, 36, color)
    g = VGroup(box, t).move_to([pos[0], pos[1], 0])
    return g


def pulse_stroke(m, base=5, amp=2, w=2.0):
    m.add_updater(lambda x: x.set_stroke(width=base + amp * np.sin(w * x._sc.renderer.time)))


def bars(n=6, seed=0, h=0.5):
    rng = np.random.RandomState(seed)
    return VGroup(*[Line([0.1 * k, 0, 0], [0.1 * k, rng.uniform(0.25, 1) * h, 0]).set_stroke(TEAL, 4) for k in range(n)])


class WorldScene(SpokenScene):
    """Adds the tree world (dots in 3 clusters, tree lines) at the carried positions."""

    def tree_world(self, pos=None, lines=True):
        self.F = DotField(self, pos or cluster_pos())
        self.tree = tree_lines()
        self.add(self.tree if lines else VGroup(), self.F.dots, sch())
        return self.F, self.tree


# ------------------------------------------------------------------------------------------------
class S00Hook(SpokenScene):
    def construct(self):
        F = DotField(self, gang_pos(), amp=0.28)
        ell = ganglion()
        self.add(ell, F.dots)
        self.play(FadeIn(ell), run_time=0.8)
        self.add(sch())
        cs = []
        xs = [-2.6, 0.2, 3.0]
        for k, (txt, ph) in enumerate([("11", "11"), ("17", "17"), ("18", "18")]):
            c = M(txt, 80, BLUE, weight=BOLD).move_to([xs[k], 3.3, 0])
            cs.append(c)
            self.at(ph, lead=0.1)
            self.play(FadeIn(c, shift=DOWN * 0.6), run_time=0.7)
        q = T("?", 90, GREY, weight=BOLD).move_to([5.7, 3.3, 0])
        self.at("Which count")
        self.play(FadeIn(q, scale=0.4), run_time=0.8)
        self.at("trust")
        self.play(Indicate(q, scale_factor=1.25, color=TEXT), run_time=1.2)
        self.at("Watch the same")
        self.play(*[c.animate.shift(RIGHT * 0.5) for c in cs], run_time=1.4, rate_func=there_and_back)
        self.play(*[c.animate.shift(RIGHT * 0.5) for c in cs], run_time=1.4, rate_func=there_and_back)
        self.play(Indicate(q, scale_factor=1.2), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Sensory Neurons by Their Genes: the Atlas Era"
    TITLE = "From Cluster to Cell Type"

    def construct(self):
        F = DotField(self, gang_pos(), fo=0.07, so=0.12, amp=0.28)
        ell = ganglion().set_stroke(opacity=0.1).set_fill(opacity=0.0)
        self.add(ell, F.dots)
        super().construct()


class S02Measurement(SpokenScene):
    def construct(self):
        F = DotField(self, gang_pos(), amp=0.15)
        ell = ganglion()
        self.add(ell, F.dots, sch())
        order = sorted(range(N), key=lambda i: F.src[i][0])
        pick = [order[8], order[22], order[36]]
        rings = VGroup(*[Circle(0.32, stroke_color=TEXT, stroke_width=4) for _ in pick])
        for r, i in zip(rings, pick):
            r.add_updater(lambda m, i=i: m.move_to(F.dots[i].get_center()))
        lab = T("one neuron", 34, TEXT)
        lab.add_updater(lambda m: m.move_to([F.dots[pick[1]].get_center()[0], 3.2, 0]))
        self.play(FadeIn(rings), FadeIn(lab), run_time=1.0)
        self.at("Its measured RNA")
        self.play(FadeOut(lab), run_time=0.5)
        bc = VGroup()
        for k, i in enumerate(pick):
            b = bars(7, k, 0.8)
            b.add_updater(lambda m, i=i: m.move_to(F.dots[i].get_center() + RIGHT * 0.9))
            bc.add(b)
        self.play(LaggedStart(*[Create(b) for b in bc], lag_ratio=0.3), run_time=1.6)
        self.at("teal barcode")
        self.play(Indicate(bc, color=TEAL, scale_factor=1.3), run_time=1.2)
        self.at("clustering method")
        tree = tree_lines()
        self.play(FadeOut(bc), FadeOut(rings), FadeOut(ell), run_time=0.6)
        anims = F.prep(cluster_pos())
        self.play(*anims, LaggedStart(*[Create(m) for m in tree], lag_ratio=0.2), run_time=2.8)
        self.at("similar barcodes suggest")
        rings2 = VGroup(*[Circle(1.05, stroke_color=TEAL, stroke_width=5).move_to([CX, y, 0]) for y in CY])
        self.at("molecular programs")
        self.play(LaggedStart(*[Create(r) for r in rings2], lag_ratio=0.3), run_time=1.8)
        qs = VGroup(*[T("?", 64, GREY, weight=BOLD).move_to([-0.55, y, 0]) for y in CY])
        self.at("reveal a job")
        self.play(FadeIn(qs, lag_ratio=0.3), run_time=1.4)
        tag = T("this sample", 60, TEXT).move_to([3.4, 0.2, 0])
        self.at("map of this sample")
        self.play(FadeOut(qs), FadeIn(tag, shift=LEFT * 0.4), run_time=1.0)
        self.play(Indicate(tag, scale_factor=1.15), run_time=1.5)
        self.finish()


def predict_objects(scene):
    tr = ValueTracker(0.08)
    dial = make_dial([1.5, 0.3], 1.8, tr)
    dlab = T("resolution", 40, TEAL).move_to([1.5, -2.0, 0])
    return tr, dial, dlab


class S03Predict(SpokenScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        self.add(tree, F.dots, sch())
        cnt = T("45 neurons", 44, BLUE).move_to([1.5, 3.15, 0])
        self.at("every neuron")
        self.play(FadeIn(cnt, shift=DOWN * 0.3), run_time=0.8)
        tr, dial, dlab = predict_objects(self)
        self.at("Turn the clustering")
        self.play(FadeIn(dial, scale=0.8), FadeIn(dlab), run_time=1.2)
        chips = []
        for k, (txt, ph) in enumerate([("gain neurons", "gain neurons"), ("lose neurons", "lose neurons"), ("split branches", "split existing branches")]):
            c = chip(txt, TEXT, size=30).move_to([5.2, 1.7 - 1.4 * k, 0])
            if k == 0:
                self.at("Will the tree")
            else:
                self.at(ph)
            self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.6)
            chips.append(c)
        self.play(Indicate(dial.ring, color=TEAL, scale_factor=1.05), run_time=1.5)
        self.finish()


class S04Pause(NarratedScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        tr, dial, dlab = predict_objects(self)
        cnt = T("45 neurons", 44, BLUE).move_to([1.5, 3.15, 0])
        chips = VGroup(*[chip(t, TEXT, size=30).move_to([5.2, 1.7 - 1.4 * k, 0]) for k, t in enumerate(["gain neurons", "lose neurons", "split branches"])])
        self.add(tree, F.dots, sch(), cnt, dial, dlab, chips)
        tr.add_updater(lambda m: m.set_value(0.1 + 0.025 * np.sin(1.8 * self.renderer.time)))
        dial.ring.add_updater(lambda m: m.set_stroke(width=5 + 2.5 * np.sin(2.2 * self.renderer.time)))
        self.finish()


class S05Resolution(SpokenScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        tr, dial, dlab = predict_objects(self)
        cnt = T("45 neurons", 44, BLUE).move_to([1.5, 3.15, 0])
        self.add(tree, F.dots, sch(), cnt, dial, dlab)
        sl = split_lines()
        anims = F.prep(split_pos())
        self.play(*anims, tr.animate.set_value(0.95), LaggedStart(*[Create(m) for m in sl], lag_ratio=0.1), run_time=2.4)
        self.at("No new neuron")
        self.play(Indicate(cnt, color=TEXT, scale_factor=1.2), run_time=1.4)
        self.at("In real atlases")
        tags = []
        specs = [("11: 622 mouse neurons", "11"), ("17: larger mouse census", "17"), ("18: cross-species", "18")]
        self.play(FadeOut(dial), FadeOut(dlab), cnt.animate.set_opacity(0.0), run_time=1.2)
        for k, (txt, ph) in enumerate(specs):
            c = chip(txt, BLUE, size=38).move_to([3.3, 2.0 - 1.4 * k, 0])
            self.at(ph, lead=0.5)
            self.play(FadeIn(c, shift=LEFT * 0.4), run_time=0.8)
            tags.append(c)
        note = T("different data and methods", 36, TEXT).move_to([3.3, -1.9, 0])
        self.at("Those counts also differ")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.0)
        self.play(Indicate(note, scale_factor=1.1), run_time=1.5)
        self.finish()


def tile(label, y, icon, move_icon=True):
    box = RoundedRectangle(corner_radius=0.18, width=5.8, height=1.6, stroke_color=TEXT, stroke_width=3, fill_color=TEAL, fill_opacity=0.28)
    t = T(label, 28, TEXT)
    g = VGroup(box, t)
    g.move_to([3.6, y, 0])
    if move_icon:
        icon.move_to(g.get_left() + RIGHT * 0.9)
    t.move_to(g.get_center() + RIGHT * 0.8)
    return VGroup(box, t, icon)


class S06OtherControls(SpokenScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        self.add(tree, F.dots, sch())
        # tile 1: resolution
        tr = ValueTracker(0.5)
        d1 = make_dial([1.55, 2.3], 0.55, tr)
        tr.add_updater(lambda m: m.set_value(0.5 + 0.35 * np.sin(1.3 * self.renderer.time)))
        t1 = tile("resolution", 2.3, d1, move_icon=False)
        self.play(FadeIn(t1, shift=LEFT * 0.4), run_time=1.2)
        # tile 2: whole cell / nucleus filter
        bb = bars(6, 5, 0.9)
        t2 = tile("whole cell / nucleus", 0.4, bb)
        self.at("Whole cells")
        self.play(FadeIn(t2, shift=LEFT * 0.4), run_time=1.2)
        fade3 = F.fade([i for i in range(N) if i % 3 == 2])
        self.at("hide a branch")
        self.play(bb[1].animate.set_opacity(0.1), bb[4].animate.set_opacity(0.1), fade3.animate.set_value(1), tree.h[2].animate.set_opacity(0.2), run_time=2.0)
        rare = [i for i in range(N) if i % 3 == 1][:4]
        fade_r = F.fade(rare)
        self.at("rare cells")
        self.play(fade_r.animate.set_value(1), run_time=1.6)
        self.at("Injury can pull")
        mag = VGroup(Arc(radius=0.35, start_angle=PI, angle=PI, stroke_color=RED, stroke_width=9).rotate(PI),
                     Line([-0.35, 0, 0], [-0.35, 0.4, 0]).set_stroke(RED, 9), Line([0.35, 0, 0], [0.35, 0.4, 0]).set_stroke(RED, 9))
        mag.arc = None
        t3 = tile("injury magnet", -1.7, mag)
        isl = Circle(0.75, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.08).move_to([-0.3, 0.2, 0])
        rng = np.random.RandomState(21)
        sel = [i for i in range(N) if i % 3 == 0][:3] + [i for i in range(N) if i % 3 == 1][4:7] + [i for i in range(N) if i % 3 == 2][:3]
        dst = [None] * N
        cols = [None] * N
        for i in sel:
            dst[i] = _disc(rng, [-0.3, 0.2], 0.45)
            cols[i] = RED
        self.play(fade3.animate.set_value(0), fade_r.animate.set_value(0), tree.h[2].animate.set_opacity(0.8), FadeIn(t3, shift=LEFT * 0.4), FadeIn(isl), run_time=1.0)
        self.at("pull several")
        anims = F.prep(dst, cols)
        self.play(*anims, run_time=2.8)
        lab = T("injury state", 28, RED).move_to([-0.6, -1.0, 0])
        self.at("transcriptional state")
        self.play(FadeIn(lab), run_time=1.0)
        self.at("Neither change")
        self.play(Indicate(VGroup(t2, t3), scale_factor=1.04, color=TEXT), run_time=1.6)
        self.finish()


def selected_world(scene, pos, enlarged=True):
    F = DotField(scene, pos)
    tree = tree_lines()
    tree.set_stroke(opacity=0.25)
    tree.h[0].set_stroke(opacity=0.9)
    tree.trunk.set_stroke(opacity=0.9)
    F.fade(IDX_OTHER).set_value(0.85)
    return F, tree


class S07Rule(SpokenScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        self.add(tree, F.dots, sch())
        fo = F.fade(IDX_OTHER)
        anims = F.prep(big_pos())
        self.play(*anims, fo.animate.set_value(0.85), *[m.animate.set_stroke(opacity=0.25) for m in [tree.vert, tree.h[1], tree.h[2]]], run_time=2.6)
        lab = T("candidate type", 38, TEXT).move_to([CX, 3.45, 0])
        self.at("candidate type")
        self.play(FadeIn(lab, shift=DOWN * 0.2), run_time=0.8)
        s1 = sock("recurs", [3.5, 2.3], h=1.3)
        s2 = sock("independent anchor", [3.5, 0.7], h=1.3)
        self.at("recurs")
        self.play(Create(s1), run_time=1.2)
        self.at("independent measurement")
        self.play(Create(s2), run_time=1.2)
        self.play(Indicate(s2, scale_factor=1.05, color=TEXT), run_time=1.2)
        names = ["resolution", "preparation", "state"]
        ctl = VGroup()
        for k, nm in enumerate(names):
            cx = -4.3 + 4.3 * k
            lb = T(nm, 30, TEXT).move_to([cx, -3.05, 0])
            tk = Line([cx - 1.3, -3.55, 0], [cx + 1.3, -3.55, 0]).set_stroke(GREY, 4)
            kn = Dot(radius=0.16, color=TEAL)
            kn.add_updater(lambda m, cx=cx, k=k: m.move_to([cx + 1.1 * np.sin(0.9 * self.renderer.time + 2.1 * k), -3.55, 0]))
            ctl.add(lb, tk, kn)
        self.at("Its count and boundary")
        self.play(FadeIn(ctl), run_time=1.2)
        self.finish()


class S08Access(SpokenScene):
    def construct(self):
        F = DotField(self, big_pos())
        tree = tree_lines()
        for m in [tree.vert, tree.h[1], tree.h[2]]:
            m.set_stroke(opacity=0.25)
        F.fade(IDX_OTHER).set_value(0.85)
        self.add(tree, F.dots, sch())
        sw = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.4, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.3).move_to([4.6, 2.4, 0])
        swl = T("reporter", 34, GOLD).move_to(sw)
        self.at("A marker from the teal")
        badge = chip("marker", TEAL, size=30).move_to([CX + 1.7, 1.5, 0])
        self.play(FadeIn(badge, scale=0.6), FadeIn(VGroup(sw, swl)), run_time=1.0)
        self.play(badge.animate.move_to([1.3, 2.4, 0]), run_time=2.0)
        self.at("gold label")
        anims = F.prep(None, [GOLD if i % 3 == 0 else None for i in range(N)])
        self.play(*anims, Indicate(sw, color=GOLD, scale_factor=1.08), run_time=2.0)
        self.at("If one marker")
        self.play(FadeOut(badge), FadeOut(VGroup(sw, swl)), run_time=0.8)
        ca = Circle(1.5, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.08).move_to([2.3, 0.2, 0])
        cb = Circle(1.5, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.08).move_to([4.5, 0.2, 0])
        la = T("marker A", 30, TEAL).move_to([1.9, 2.25, 0])
        lb = T("marker B", 30, TEAL).move_to([4.9, 2.25, 0])
        self.play(Create(ca), Create(cb), FadeIn(la), FadeIn(lb), run_time=1.8)
        self.at("requiring two")
        self.play(ca.animate.move_to([2.8, 0.2, 0]), cb.animate.move_to([4.0, 0.2, 0]), run_time=1.6)
        inter = Intersection(ca, cb, fill_color=GOLD, fill_opacity=0.7, stroke_width=0)
        self.at("narrows the label")
        self.play(FadeIn(inter), run_time=0.8)
        keep = IDX1[: len(IDX1) // 2]
        anims = F.prep(None, [GOLD if i in keep else BLUE for i in range(N)])
        self.play(*anims, run_time=1.6)
        li = T("intersection", 32, GOLD).move_to([3.4, -1.9, 0])
        self.play(FadeIn(li, shift=UP * 0.2), run_time=0.8)
        self.finish()


class S09Function(SpokenScene):
    def construct(self):
        F = DotField(self, big_pos())
        keep = IDX1[: len(IDX1) // 2]
        F.col0 = F.col1 = [ManimColor(GOLD if i in keep else BLUE) for i in range(N)]
        tree = tree_lines()
        tree.set_stroke(opacity=0.2)
        fo = F.fade(IDX_OTHER)
        fo.set_value(0.95)
        skin = VGroup(Rectangle(width=13.2, height=0.6, stroke_width=0, fill_color=GREY, fill_opacity=0.4).move_to([0, -1.5, 0]),
                      Rectangle(width=13.2, height=1.9, stroke_width=0, fill_color=GREY, fill_opacity=0.17).move_to([0, -2.75, 0]))
        slab = T("skin", 34, TEXT).move_to([5.8, -3.2, 0])
        self.add(tree, skin, slab, F.dots, sch())
        self.at("follow those labeled")
        ends = [-3.4, -1.7, 0.0, 1.9]
        starts = [F.dots[keep[j]] for j in range(4)]
        axons = VGroup()
        for s, x in zip(starts, ends):
            ax = Line(s.get_center(), [x, -2.05, 0]).set_stroke(GOLD, 4)
            ax.add_updater(lambda m, s=s, x=x: m.put_start_and_end_on(s.get_center(), [x, -2.05, 0]))
            axons.add(ax)
        tips = VGroup(*[Dot([x, -2.05, 0], radius=0.1, color=GOLD) for x in ends])
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.2), run_time=2.4)
        self.play(FadeIn(tips), run_time=0.6)
        self.at("stimulate the skin")
        probe = VGroup(Rectangle(width=0.22, height=0.9, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([0, 0.45, 0]),
                       Circle(0.2, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([0, 0, 0]))
        probe.add_updater(lambda m: m.move_to([1.9, -0.45 - 0.3 * (0.5 + 0.5 * np.sin(1.7 * self.renderer.time)), 0]))
        self.play(FadeIn(probe), run_time=0.8)
        self.at("imaging the ganglion")
        halos = VGroup()
        gdots = [keep[0], keep[2], keep[3]]
        anims = F.prep(None, [GREEN if i in gdots else (GOLD if i in keep else BLUE) for i in range(N)])
        for i in gdots:
            h = Circle(0.38, stroke_color=GREEN, stroke_width=5)
            h.add_updater(lambda m, i=i: (m.move_to(F.dots[i].get_center()), m.set_stroke(opacity=0.35 + 0.65 * (0.5 + 0.5 * np.sin(1.7 * self.renderer.time)))))
            halos.add(h)
        self.play(*anims, FadeIn(halos), run_time=1.4)
        # response ranges (schematic)
        def row(y, name, bands):
            lab = T(name, 34, TEXT).move_to([2.1, y, 0])
            trk = Line([3.6, y, 0], [6.6, y, 0]).set_stroke(GREY, 5)
            bs = VGroup(*[Rectangle(width=w, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=op).move_to([x, y, 0]) for x, w, op in bands])
            return VGroup(lab, trk), bs
        r1, b1 = row(2.7, "force", [(4.2, 1.2, 0.85), (5.8, 1.4, 0.45)])
        r2, b2 = row(1.4, "temperature", [(4.7, 1.2, 0.85), (6.0, 1.0, 0.45)])
        self.at("labeled subtypes")
        self.play(FadeIn(r1), FadeIn(r2), run_time=1.0)
        self.at("different tested ranges")
        self.play(LaggedStart(GrowFromEdge(b1[0], LEFT), GrowFromEdge(b1[1], LEFT), GrowFromEdge(b2[0], LEFT), GrowFromEdge(b2[1], LEFT), lag_ratio=0.3), run_time=2.6)
        st = T("schematic ranges", 32, TEXT).move_to([4.2, 0.5, 0])
        self.play(FadeIn(st), run_time=0.6)
        self.at("A distinct ending")
        self.play(Indicate(axons, color=GOLD, scale_factor=1.0), run_time=1.6)
        self.at("independent of the clustering")
        self.play(Indicate(VGroup(b1, b2), color=GREEN, scale_factor=1.08), run_time=1.8)
        self.at("It strengthens")
        self.play(Indicate(VGroup(b1[0], b2[0], b1[1], b2[1]), scale_factor=1.12, color=GREEN), run_time=1.8)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        F = DotField(self, big_pos())
        keep = IDX1[: len(IDX1) // 2]
        F.col0 = F.col1 = [ManimColor(GOLD if i in keep else BLUE) for i in range(N)]
        tree = tree_lines()
        tree.set_stroke(opacity=0.2)
        fo = F.fade(IDX_OTHER)
        fo.set_value(0.95)
        self.add(tree, F.dots, sch())
        rep = RoundedRectangle(corner_radius=0.2, width=5.4, height=1.5, stroke_color=GOLD, stroke_width=5).move_to([3.5, 2.35, 0])
        rl = T("reporter", 32, GOLD).move_to(rep)
        self.at("A driver records")
        self.play(FadeIn(VGroup(rep, rl)), run_time=1.0)
        pl = Rectangle(width=2.65, height=1.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.55).move_to([rep.get_left()[0] + 1.325, 2.35, 0])
        pr = Rectangle(width=2.65, height=1.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.55).move_to([rep.get_right()[0] - 1.325, 2.35, 0])
        pl.shift(LEFT * 1.9).set_opacity(0.0)
        pr.shift(RIGHT * 1.9).set_opacity(0.0)
        wl = T("time window", 30, TEXT).move_to([3.5, 1.3, 0])
        self.at("sometimes during")
        self.play(pl.animate.shift(RIGHT * 1.9).set_opacity(0.55), pr.animate.shift(LEFT * 1.9).set_opacity(0.55), FadeIn(wl), run_time=1.4)
        self.at("chosen time window")
        self.play(pl.animate.shift(LEFT * 1.0), pr.animate.shift(RIGHT * 1.0), run_time=1.4)
        self.at("Calcium signals")
        x0 = -4.4
        times = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 4.0, 4.2, 4.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6]
        sp = VGroup(*[Line([x0 + t, 0.1, 0], [x0 + t, 1.1, 0]).set_stroke(GREEN, 7) for t in times])
        axis1 = Line([x0, 0.1, 0], [x0 + 10, 0.1, 0]).set_stroke(GREY, 3)
        tl = T("spikes", 32, TEXT).move_to([-5.7, 0.9, 0])
        self.play(FadeOut(VGroup(rep, rl, pl, pr, wl)), Create(axis1), LaggedStart(*[Create(s) for s in sp], lag_ratio=0.05), FadeIn(tl), run_time=1.1)

        def cal(t):
            f = sum(np.exp(-(t - ti) / 1.3) for ti in times if t >= ti)
            return np.array([x0 + t, -2.2 + 1.5 * np.tanh(f / 2.0), 0])
        trace = ParametricFunction(cal, t_range=[0, 10, 0.05], color=GREEN, stroke_width=9)
        self.at("do not count")
        axis2 = Line([x0, -2.2, 0], [x0 + 10, -2.2, 0]).set_stroke(GREY, 3)
        cl = T("calcium", 32, TEXT).move_to([-5.75, -1.3, 0])
        self.play(FadeIn(axis2), FadeIn(cl), TransformFromCopy(sp, trace), run_time=2.2)
        cur = Line([x0, -2.4, 0], [x0, 1.3, 0]).set_stroke(TEXT, 3, opacity=0.6)
        t0 = self.renderer.time
        cur.add_updater(lambda m: m.move_to([x0 + ((self.renderer.time - t0) * 0.9) % 10.0, -0.55, 0]))
        self.add(cur)
        self.at("The result supports")
        chips = []
        for nm, ph, x in [("preparation", "preparation", -4.2), ("stimuli", "stimuli", 0.0), ("sampled cells", "cells actually", 4.2)]:
            c = chip(nm, TEXT, size=34).move_to([x, -3.1, 0])
            self.at(ph, lead=0.1)
            self.play(FadeIn(c, shift=UP * 0.3), run_time=0.8)
            chips.append(c)
        frame = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=13.4, height=6.8, stroke_color=TEXT, stroke_width=4), num_dashes=80).move_to([0, -0.25, 0])
        self.at("actually tested")
        self.play(Create(frame), run_time=1.6)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        F = DotField(self, cluster_pos())
        tree = tree_lines()
        self.add(tree, F.dots, sch())
        cs = VGroup(*[M(t, 80, BLUE, weight=BOLD).move_to([3.6, y, 0]) for t, y in [("11", 2.4), ("17", 0.4), ("18", -1.6)]])
        self.play(FadeIn(cs, lag_ratio=0.3), run_time=1.4)
        self.at("Ask what produced")
        tags = VGroup(*[chip(f"{t}: its method", TEXT, size=38).move_to([3.6, y, 0]) for t, y in [("11", 2.4), ("17", 0.4), ("18", -1.6)]])
        self.play(*[ReplacementTransform(c, t) for c, t in zip(cs, tags)], run_time=2.0)
        self.at("then ask whether")
        socks = VGroup()
        for y in CY:
            for dx in (-0.8, -0.2):
                socks.add(DashedVMobject(Circle(0.24, stroke_color=TEXT, stroke_width=3), num_dashes=14).move_to([dx - 0.1, y, 0]))
        self.play(Create(socks), run_time=1.6)
        self.at("reaches the same")
        tick = VMobject().set_points_as_corners([[-0.95, CY[0], 0], [-0.82, CY[0] - 0.13, 0], [-0.62, CY[0] + 0.15, 0]]).set_stroke(TEXT, 6)
        g = Dot([-0.3, CY[0], 0], radius=0.24, color=GREEN)
        self.play(Create(tick), FadeIn(g, scale=0.4), run_time=1.6)
        self.at("That turns a cluster")
        ring = Circle(1.2, stroke_color=BLUE, stroke_width=6).move_to([CX, CY[0], 0])
        self.play(Create(ring), run_time=1.4)
        self.play(Indicate(ring, scale_factor=1.1, color=BLUE), run_time=1.4)
        self.finish()


class S12End(EndCard):
    LINE = "A cluster needs an independent anchor before it earns type."
