"""Two Kinds of Zero (film 2 of Movement and Spatial Populations)

COLOUR MAP (same as film 1): occupied pond TEAL, empty pond GREY, colonization GOLD, extinction RED,
symbol p = fraction occupied. New here: tick box 1 = detected (TEAL fill), 0 = not detected (white);
occupied-but-undetected pond = TEAL dashed outline with a toad hidden in reeds; naive counts GREY bars,
corrected estimates TEAL bars. The 40-site data are a seeded simulation (p 0.62, detection 0.5) and the
dials/bars are the maximum-likelihood fit to it (computed). Expected tallies are computed; the rest is schematic.
"""
import importlib.util
import math
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("film1_scenes", os.path.join(_here, "..", "scenes.py"))
F1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F1)

RANK, POS, frog, xmark, lab, Pond, MapW, new_map, BIG = F1.RANK, F1.POS, F1.frog, F1.xmark, F1.lab, F1.Pond, F1.MapW, F1.new_map, F1.BIG
add_motes, Sc, BROWN, FROG, WHITE = F1.add_motes, F1.Sc, F1.BROWN, F1.FROG, F1.WHITE
REED = "#5E9E4F"
RX = 4.1   # right column x


# ------------------------------------------------------------------ shared pieces
class BP(VGroup):
    """A pond: rippling ellipse. occ 0..1 (GREY..TEAL); dash 0..1 draws a dashed outline instead of a solid one."""
    def __init__(self, c, w, h, occ=0.0, dash=0.0, ph=0.0, dashable=True):
        self.body = Ellipse(width=w, height=h, stroke_width=3)
        self.rip = Ellipse(width=w, height=h, stroke_width=2)
        parts = [self.rip, self.body]
        self.dsh = None
        if dashable:
            self.dsh = DashedVMobject(Ellipse(width=w, height=h, stroke_width=4), num_dashes=26, dashed_ratio=0.55)
            parts.append(self.dsh)
        super().__init__(*parts)
        self.occ, self.dash, self.ph, self.t = occ, dash, ph, 0.0
        self.w0, self.h0 = w, h
        self.move_to([c[0], c[1], 0])
        self.add_updater(lambda m, dt: m.paint(dt))
        self.paint(0)

    def paint(self, dt=0.0):
        self.t += dt
        o = float(self.occ)
        d = float(self.dash)
        col = interpolate_color(ManimColor(GREY), ManimColor(TEAL), o)
        self.body.set_stroke(color=col, width=3, opacity=1 - d)
        self.body.set_fill(col, opacity=0.14 + 0.46 * o + 0.06 * o * math.sin(self.t * 1.6 + self.ph * 6))
        if self.dsh is not None:
            self.dsh.set_stroke(color=col, width=4, opacity=d)
        ph = (self.t * 0.3 + self.ph) % 1.0
        w, h = self.body.width, self.body.height
        self.rip.stretch_to_fit_width(w * (1 + 0.45 * ph))
        self.rip.stretch_to_fit_height(h * (1 + 0.45 * ph))
        self.rip.move_to(self.body.get_center())
        self.rip.set_stroke(color=TEAL, width=2, opacity=o * 0.5 * (1 - ph))
        self.rip.set_fill(opacity=0)


class Tw(Animation):
    """Tween a numeric attribute of a mobject (occ, dash)."""
    def __init__(self, m, attr, target, **kw):
        kw.setdefault("suspend_mobject_updating", False)
        super().__init__(m, **kw)
        self.attr, self.tg = attr, target

    def begin(self):
        self.s0 = getattr(self.mobject, self.attr)
        super().begin()

    def interpolate_mobject(self, a):
        setattr(self.mobject, self.attr, self.s0 + (self.tg - self.s0) * a)


class TB(VGroup):
    """A tick box. Blank until filled: 1 = TEAL, 0 = white."""
    def __init__(self, c, s=0.5, val=None, tsize=28):
        self.sq = Square(side_length=s, stroke_color=TEXT, stroke_width=3)
        super().__init__(self.sq)
        self.s, self.tsize, self.txt = s, tsize, None
        self.move_to([c[0], c[1], 0])
        if val is not None:
            self.set_now(val)

    def _mk(self, val):
        return M(str(val), self.tsize, BG, weight=BOLD).move_to(self.sq.get_center())

    def set_now(self, val):
        self.sq.set_fill(TEAL if val else WHITE, 0.92)
        self.txt = self._mk(val)
        self.add(self.txt)
        return self

    def fill(self, val):
        t = self._mk(val)
        self.txt = t
        self.add(t)
        return [self.sq.animate.set_fill(TEAL if val else WHITE, 0.92), FadeIn(t, scale=0.6)]

    def clear_anim(self):
        out = [self.sq.animate.set_fill(BG, 0)]
        if self.txt is not None:
            out.append(FadeOut(self.txt))
            self.remove(self.txt)
            self.txt = None
        return out


def boxes(cx, y, vals=None, s=0.5, gap=0.06, n=3, tsize=28):
    step = s + gap
    g = VGroup()
    for i in range(n):
        v = None if vals is None else vals[i]
        g.add(TB([cx + (i - (n - 1) / 2) * step, y], s, v, tsize))
    return g


def reeds(c, w):
    g = VGroup()
    for i in range(11):
        x = c[0] - 0.4 * w + i * 0.08 * w
        base = c[1] - 0.26 * w * (1 - ((x - c[0]) / (0.55 * w)) ** 2) ** 0.5 - 0.15
        h = 0.55 * w * (0.7 + 0.3 * math.sin(i * 2.3))
        g.add(Line([x, base, 0], [x + 0.08 * math.sin(i * 1.7), base + h * 0.55, 0]).set_stroke(REED, 7))
    g.set_z_index(6)
    return g


def hidden_toad(c, w):
    t = frog([c[0] + 0.02 * w, c[1] + 0.0, 0], 0.8 * w, 1.0)
    t.set_z_index(5)
    return t


def observer(c, s=1.0):
    head = Circle(radius=0.24 * s, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9)
    body = Polygon([-0.35, -0.2, 0], [0.35, -0.2, 0], [0.22, -1.0, 0], [-0.22, -1.0, 0], color=TEXT,
                   stroke_width=3, fill_color=TEXT, fill_opacity=0.35)
    body.scale(s)
    head.move_to(body.get_top() + UP * 0.38 * s)
    return VGroup(body, head).move_to([c[0], c[1], 0])


def sheet_pond(sc_obj, c, w, h, kind, ph=0.0):
    """kind 'empty' or 'hid'."""
    if kind == "empty":
        return BP(c, w, h, occ=0.0, dash=0.0, ph=ph)
    return BP(c, w, h, occ=1.0, dash=1.0, ph=ph)


def pw(base, exp, size=34, color=TEXT):
    a = M(base, size, color)
    b = M(exp, int(size * 0.62), color)
    b.next_to(a, RIGHT, buff=0.03).shift(UP * 0.17)
    return VGroup(a, b)


def hdr(det, y=3.2):
    return T(f"detection per visit = {det}", 28, TEXT).move_to([RX, y, 0])


# ---- the eight-pond grid (s05-s08)
HIST8 = ["110", "011", "101", "010", "111", "100", "001", "000"]
GX = [-5.7, -3.95, -2.2, -0.45]
GY = [(1.9, 0.9), (-0.9, -1.9)]   # pond y, boxes y


class Eight:
    def __init__(self, dashed=True, with_boxes=True):
        self.ponds, self.bx = [], []
        for k in range(8):
            r, c = divmod(k, 4)
            p = BP([GX[c], GY[r][0]], 1.6, 1.1, occ=1.0, dash=1.0 if dashed else 0.0, ph=k * 0.13)
            self.ponds.append(p)
            self.bx.append(boxes(GX[c], GY[r][1], None, s=0.46, gap=0.06, tsize=26))
        self.pg = VGroup(*self.ponds)
        self.bg = VGroup(*self.bx)

    def add_to(self, sc):
        sc.add(self.pg, self.bg)


# ---- the 40-site data (computed)
def _mle(Y):
    n = Y.shape[1]
    s = Y.sum(1)
    best = (-1e9, 0.0, 0.0)
    for p in np.arange(0.02, 1, 0.01):
        for d in np.arange(0.02, 1, 0.01):
            L = p * d ** s * (1 - d) ** (n - s) + (1 - p) * (s == 0)
            ll = np.log(L).sum()
            if ll > best[0]:
                best = (ll, p, d)
    return best


_r = np.random.RandomState(17)
Z = _r.rand(40) < 0.62
Y = ((_r.rand(40, 3) < 0.5) * Z[:, None]).astype(int)
NAIVE = float((Y.sum(1) > 0).mean())
_, P_HAT, D_HAT = _mle(Y)
P_HAT, D_HAT = float(P_HAT), float(D_HAT)
ZERO = [i for i in range(40) if Y[i].sum() == 0]
SILENT_OCC = [i for i in ZERO if Z[i]]


class Grid40:
    def __init__(self):
        self.ponds, self.bx = [], []
        for i in range(40):
            r, c = divmod(i, 8)
            x, y = -5.95 + 0.95 * c, 2.5 - 1.15 * r
            p = BP([x, y], 0.85, 0.5, occ=0.0, dash=0.0, ph=i * 0.11, dashable=(i in ZERO))
            self.ponds.append(p)
            self.bx.append(boxes(x, y - 0.42, [int(v) for v in Y[i]], s=0.2, gap=0.04, tsize=12))
        self.pg = VGroup(*self.ponds)
        self.bg = VGroup(*self.bx)

    def add_to(self, sc, lit=False):
        if lit:
            for i, p in enumerate(self.ponds):
                p.occ = 1.0 if Y[i].sum() > 0 else 0.0
        sc.add(self.pg, self.bg)


class Dial(VGroup):
    def __init__(self, c, r, tr, label, label_y, read_y):
        arc = Arc(radius=r, start_angle=PI, angle=-PI, color=GREY, stroke_width=6).move_to([c[0], c[1] + r * 0.32, 0])
        self.ctr = np.array([c[0], c[1], 0.0])
        self.r, self.tr = r, tr
        needle = Line(self.ctr, self.ctr + UP * r * 0.9, color=TEAL, stroke_width=8)

        def f(m):
            a = PI - tr.get_value() * PI
            m.put_start_and_end_on(self.ctr, self.ctr + r * 0.9 * np.array([math.cos(a), math.sin(a), 0]))
        needle.add_updater(f)
        hub = Dot(self.ctr, radius=0.1, color=TEXT)
        lb = T(label, 28, TEXT).move_to([c[0], label_y, 0])
        z0 = M("0", 24, TEXT).move_to(self.ctr + LEFT * r * 1.0 + DOWN * 0.3)
        z1 = M("1", 24, TEXT).move_to(self.ctr + RIGHT * r * 1.0 + DOWN * 0.3)
        self.read = always_redraw(lambda: M(f"{tr.get_value():.2f}", 34, TEAL).move_to([c[0], read_y, 0]))
        super().__init__(arc, needle, hub, lb, z0, z1)


def two_panels(sc, L=-3.4, R=3.4, y=0.7, w=4.1, h=2.86):
    pass


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Movement and Spatial Populations"
    TITLE = "Two Kinds of Zero"

    def construct(self):
        p = BP([0, -2.0, 0], 3.2, 2.0, occ=1.0, dash=1.0)
        bx = boxes(0, -3.4, None, s=0.7, gap=0.2)
        veil = Rectangle(width=14.3, height=8.1, stroke_width=0, fill_color=BG, fill_opacity=0.62).set_z_index(10)
        self.add(p, bx, veil)
        super().construct()


class S01Link(Sc):
    def construct(self):
        mp = new_map(BIG, n_occ=15)
        pt = M("p = 0.75", 36, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(mp, scale=1.05), FadeIn(pt), run_time=0.9)
        idx = next(i for i in (7, 8, 6, 12, 11, 13, 9, 10) if RANK[i] >= 15)
        pond = mp.ponds[idx]
        occ = [mp.ponds[i] for i in range(20) if RANK[i] < 15]
        self.at("which ponds")
        self.play(LaggedStart(*[Indicate(p, color=TEAL, scale_factor=1.15) for p in occ[:8]], lag_ratio=0.12), run_time=1.2)
        others = [p for p in mp.ponds if p is not pond]
        self.at("Three visits", lead=2.6)
        self.play(*[FadeOut(p) for p in others], FadeOut(mp.field), FadeOut(pt),
                  pond.animate.scale(3.4).move_to([0, 0.7, 0]), run_time=1.3)
        self.remove(pond)
        bp = BP([0, 0.7, 0], 4.08, 2.856, occ=0.0, dash=0.0, ph=0.3)
        self.add(bp)
        bxs = boxes(0, -1.5, None, s=0.9, gap=0.2, tsize=44)
        ob = observer([-4.6, 0.2, 0], 1.3)
        self.play(FadeIn(bxs), FadeIn(ob), run_time=0.6)
        for i, ph in enumerate(("visits", "toads", "heard")):
            self.at(ph)
            self.play(ob.animate.shift(RIGHT * 0.9), run_time=0.25)
            self.play(*bxs[i].fill(0), ob.animate.shift(LEFT * 0.9), run_time=0.35)
        self.at("Is the pond")
        q = lab("?", 120, YELLOW, weight=BOLD).move_to([4.6, 0.7, 0])
        self.play(FadeIn(q, scale=0.4), run_time=0.6)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("A survey sheet")
        card = RoundedRectangle(corner_radius=0.2, width=3.0, height=2.6, stroke_color=TEXT, stroke_width=3,
                                fill_color=TEXT, fill_opacity=0.12).move_to([4.6, 0.7, 0])
        t1 = T("survey sheet", 28, TEXT).move_to(card.get_top() + DOWN * 0.45)
        z = M("0", 100, TEXT, weight=BOLD).move_to(card.get_center() + DOWN * 0.3)
        self.play(FadeOut(q), FadeIn(card), FadeIn(t1), run_time=0.7)
        self.play(FadeIn(z, scale=0.5), run_time=0.7)
        self.play(Indicate(z, color=WHITE, scale_factor=1.2), run_time=1.0)
        self.finish()


class S02Two(Sc):
    def construct(self):
        pc = BP([0, 0.7, 0], 4.08, 2.856, occ=0.0, dash=0.0, ph=0.3)
        bc = boxes(0, -1.5, [0, 0, 0], s=0.9, gap=0.2, tsize=44)
        self.add(pc, bc)
        self.wait(0.6)
        self.at("two meanings", lead=0.8)
        pr = pc.copy()
        pr.t, pr.occ, pr.dash, pr.ph = pc.t, 0.0, 0.0, 0.6
        br = bc.copy()
        self.add(pr, br)
        self.play(pc.animate.move_to([-3.4, 0.7, 0]), bc.animate.move_to([-3.4, -1.5, 0]),
                  pr.animate.move_to([3.4, 0.7, 0]), br.animate.move_to([3.4, -1.5, 0]), run_time=1.4)
        self.at("The pond may")
        el = T("empty", 40, TEXT).move_to([-3.4, -2.9, 0])
        self.play(FadeIn(el), Indicate(pc, color=GREY, scale_factor=1.05), run_time=1.2)
        self.at("or toads", lead=0.4)
        toad = hidden_toad([3.4, 0.7, 0], 4.08)
        rd = reeds([3.4, 0.7, 0], 4.08)
        self.play(Tw(pr, "occ", 1.0), Tw(pr, "dash", 1.0), FadeIn(toad), run_time=1.2)
        self.play(FadeIn(rd, lag_ratio=0.1), run_time=1.0)
        self.at("missed them")
        r1 = T("occupied,", 36, TEAL).move_to([3.4, -2.6, 0])
        r2 = T("missed three times", 32, TEAL).move_to([3.4, -3.2, 0])
        self.play(FadeIn(r1), FadeIn(r2), run_time=0.8)
        self.play(*[Indicate(b, color=WHITE, scale_factor=1.15) for b in br], run_time=1.2)
        self.finish()


class S03Visits(Sc):
    def construct(self):
        strip = Line([-5.6, 2.2, 0], [5.6, 2.2, 0], color=GREY, stroke_width=5)
        ttl = T("one breeding season", 30, TEXT).move_to([0, 3.3, 0])
        pond = BP([0, -1.2, 0], 4.2, 2.4, occ=1.0, dash=0.0, ph=0.2)
        toad = frog([0.3, -1.2, 0], 2.6, 1.0).set_z_index(5)
        self.play(Create(strip), FadeIn(ttl), FadeIn(pond), FadeIn(toad), run_time=1.2)
        xs = [-4.0, 0.0, 4.0]
        dates, labs_, bx = VGroup(), VGroup(), boxes(0, 0.95, None, s=0.9, gap=0.2, tsize=44)
        for i, x in enumerate(xs):
            bx[i].move_to([x, 0.95, 0])
        self.at("surveyors return")
        for i, x in enumerate(xs):
            d = Dot([x, 2.2, 0], radius=0.17, color=TEXT)
            l = T(f"visit {i + 1}", 30, TEXT).move_to([x, 2.75 - 0.0, 0]).shift(DOWN * 0.0)
            ttl2 = None
            dates.add(d)
            labs_.add(l)
            self.play(FadeIn(d, scale=2), run_time=0.4)
            self.wait(0.3)
        self.play(FadeOut(ttl), FadeIn(labs_), run_time=0.8)
        self.at("while occupancy")
        fx = T("occupancy fixed within the season", 30, TEAL).move_to([0, -3.35, 0])
        self.play(FadeIn(fx), Indicate(pond, color=TEAL, scale_factor=1.05), run_time=1.2)
        self.at("Each visit")
        self.play(FadeIn(bx), run_time=0.7)
        self.at("scores a 1")
        self.play(*bx[0].fill(1), run_time=0.7)
        self.at("for detected")
        self.play(Indicate(bx[0], color=TEAL), run_time=0.8)
        self.at("for not", lead=1.0)
        self.play(*bx[1].fill(0), run_time=0.7)
        self.wait(0.4)
        self.play(*bx[2].fill(1), run_time=0.7)
        self.finish()


class S04History(Sc):
    def construct(self):
        hist = ["110", "010", "100", "000"]
        xs = [-5.1, -1.7, 1.7, 5.1]
        ponds = [BP([x, 1.0, 0], 2.7, 1.9, occ=0.0, dash=0.0, ph=i * 0.2, dashable=False) for i, x in enumerate(xs)]
        bxs = [boxes(x, -0.9, None, s=0.7, gap=0.1, tsize=36) for x in xs]
        self.play(FadeIn(VGroup(*ponds)), FadeIn(VGroup(*bxs[:2])), run_time=1.0)
        self.at("like")
        for j, ph in enumerate(["1", "1", "0"]):
            self.play(*bxs[0][j].fill(int(ph)), run_time=0.35)
        self.play(Tw(ponds[0], "occ", 1.0), run_time=0.6)
        self.at("or", lead=0.3)
        for j, v in enumerate([0, 1, 0]):
            self.play(*bxs[1][j].fill(v), run_time=0.35)
        self.wait(0.3)
        self.play(FadeIn(bxs[2]), FadeIn(bxs[3]), run_time=0.6)
        self.play(*[a for j, v in enumerate([1, 0, 0]) for a in bxs[2][j].fill(v)],
                  *[a for j in range(3) for a in bxs[3][j].fill(0)], run_time=0.8)
        self.play(Tw(ponds[2], "occ", 1.0), run_time=0.5)
        self.at("history shows")
        self.play(Indicate(bxs[1], color=WHITE, scale_factor=1.15), run_time=1.2)
        self.at("occupied", nth=0)
        self.play(Tw(ponds[1], "occ", 1.0), run_time=1.0)
        self.at("missed twice")
        ms = VGroup()
        for j in (0, 2):
            ms.add(T("missed", 28, TEAL).move_to(bxs[1][j].get_center() + DOWN * 0.9 + (LEFT * 0.25 if j == 0 else RIGHT * 0.25)))
        self.play(FadeIn(ms), run_time=0.8)
        self.play(*[Indicate(bxs[1][j], color=WHITE, scale_factor=1.3) for j in (0, 2)], run_time=1.0)
        self.finish()


def right_header(det, nvis=True):
    g = VGroup(hdr(det))
    if nvis:
        g.add(T("3 visits", 34, TEXT).move_to([RX, 2.4, 0]))
    return g


class S05Predict(Sc):
    def construct(self):
        e = Eight()
        self.add(e.pg)
        self.play(FadeIn(e.bg), run_time=0.8)
        self.play(*[Indicate(p, color=TEAL, scale_factor=1.1) for p in e.ponds[:4]], run_time=1.0)
        self.at("Each visit detects")
        h = right_header(0.5)
        self.play(FadeIn(h[0]), run_time=0.8)
        self.at("independently")
        self.play(*[Indicate(b, color=WHITE, scale_factor=1.12) for b in e.bx], run_time=1.3)
        self.at("After three visits")
        self.play(FadeIn(h[1]), run_time=0.6)
        q = VGroup(T("how many ponds", 36, TEXT), T("look empty?", 36, YELLOW)).arrange(DOWN, buff=0.15).move_to([RX, -0.4, 0])
        self.at("how many ponds")
        self.play(FadeIn(q), run_time=0.8)
        self.play(Indicate(q[1], color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        add_motes(self, "S06")
        e = Eight()
        e.add_to(self)
        h = right_header(0.5)
        q = VGroup(T("how many ponds", 36, TEXT), T("look empty?", 36, YELLOW)).arrange(DOWN, buff=0.15).move_to([RX, -0.4, 0])
        self.add(h, q)
        cur = None
        for n in (5, 4, 3, 2, 1):
            new = M(str(n), 64, YELLOW).move_to([RX, -2.4, 0])
            if cur is None:
                self.play(FadeIn(new), run_time=0.2)
            else:
                self.play(FadeOut(cur), FadeIn(new), run_time=0.2)
            cur = new
            self.wait(0.8)
        self.finish()


class S07Reveal(Sc):
    def construct(self):
        e = Eight()
        e.add_to(self)
        h = right_header(0.5)
        q = VGroup(T("how many ponds", 36, TEXT), T("look empty?", 36, YELLOW)).arrange(DOWN, buff=0.15).move_to([RX, -0.4, 0])
        self.add(h, q)
        self.wait(0.3)
        self.play(FadeOut(q), FadeOut(h[1]), run_time=0.5)
        for k, hs in enumerate(HIST8):
            acts = [a for j in range(3) for a in e.bx[k][j].fill(int(hs[j]))]
            if k < 7:
                acts.append(Tw(e.ponds[k], "dash", 0.0))
            self.play(*acts, run_time=0.32)
        ab = T("about 1 in 8", 34, TEAL).move_to([-3.4, -3.3, 0])
        self.at("three misses", lead=0.6)
        eq1 = M("0.5 × 0.5 × 0.5", 34, TEXT).move_to([RX, 2.3, 0])
        eq2 = M("= 0.125", 36, TEXT).move_to([RX, 1.5, 0])
        eq3 = M("= 1 in 8", 36, TEAL).move_to([RX, 0.7, 0])
        self.play(FadeIn(eq1), Indicate(e.bx[7], color=WHITE, scale_factor=1.2), run_time=0.9)
        self.play(FadeIn(eq2), run_time=0.7)
        self.play(FadeIn(eq3), Indicate(e.ponds[7], color=TEAL, scale_factor=1.15), run_time=0.9)
        note = VGroup(T("expected tally (computed);", 24, TEXT), T("in one real set of eight,", 24, TEXT),
                      T("the number of 000 ponds varies", 24, TEXT)).arrange(DOWN, buff=0.1).move_to([RX, -2.9, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.at("Each extra visit")
        b4 = TB([GX[3] + 1.17 - 0.06, GY[1][1]], 0.46, None, 26)
        self.play(FadeIn(b4), run_time=0.5)
        self.play(*b4.fill(0), run_time=0.5)
        self.at("halves")
        e4 = VGroup(pw("0.5", "4", 36), M("= 0.0625", 36, TEXT)).arrange(RIGHT, buff=0.12).move_to([RX, -0.7, 0])
        self.play(FadeIn(e4), run_time=0.8)
        self.play(Indicate(e4, color=TEAL, scale_factor=1.1), run_time=1.0)
        self.finish()


class S08Harder(Sc):
    def construct(self):
        e = Eight()
        hist = ["000", "000", "000", "100", "010", "001", "110", "011"]
        for k in range(8):
            for j in range(3):
                e.bx[k][j].set_now(int(HIST8[k][j]))
            if k < 7:
                e.ponds[k].dash = 0.0
        e.add_to(self)
        h = hdr(0.5)
        self.add(h)
        self.wait(0.5)
        self.at("Harder species")
        clr = [a for b in e.bx for t in b for a in t.clear_anim()]
        h2 = hdr(0.3)
        self.play(*clr, Transform(h, h2), *[Tw(p, "dash", 1.0) for p in e.ponds], run_time=1.2)
        self.at("When each visit")
        eq1 = M("0.7 × 0.7 × 0.7", 34, TEXT).move_to([RX, 2.2, 0])
        eq2 = M("= 0.343", 36, TEXT).move_to([RX, 1.4, 0])
        self.play(FadeIn(eq1), run_time=0.8)
        self.play(FadeIn(eq2), run_time=0.7)
        eq3 = M("about 1 in 3", 36, TEAL).move_to([RX, 0.6, 0])
        self.at("about one")
        self.play(FadeIn(eq3), run_time=0.8)
        self.at("comes out", lead=1.0)
        hs = ["000", "000", "000", "100", "010", "001", "110", "011"]
        order = [3, 4, 5, 6, 7, 0, 1, 2]
        for k in order:
            acts = [a for j in range(3) for a in e.bx[k][j].fill(int(hs[k][j]))]
            if k > 2:
                acts.append(Tw(e.ponds[k], "dash", 0.0))
            self.play(*acts, run_time=0.3)
        calc = M("8 × 0.343 = 2.7", 32, TEXT).move_to([RX, -0.6, 0])
        note = VGroup(T("expected tally (computed),", 24, TEXT), T("rounded to whole ponds", 24, TEXT)).arrange(DOWN, buff=0.1).move_to([RX, -2.9, 0])
        self.play(FadeIn(calc), FadeIn(note), *[Indicate(e.ponds[k], color=GREY, scale_factor=1.15) for k in (0, 1, 2)], run_time=1.2)
        self.finish()


class S09Model(Sc):
    def construct(self):
        g = Grid40()
        g.add_to(self)
        self.remove(g.pg, g.bg)
        self.play(FadeIn(g.pg, lag_ratio=0.02), run_time=0.5)
        q = lab("?", 90, YELLOW, weight=BOLD).move_to([RX, 0.7, 0])
        self.at("No single site", lead=0.0)
        self.play(FadeIn(g.bg, lag_ratio=0.02), Indicate(g.ponds[10], color=YELLOW, scale_factor=1.6), FadeIn(q), run_time=1.6)
        self.at("many sites")
        self.play(*[Indicate(p, color=WHITE, scale_factor=1.12) for p in g.ponds], FadeOut(q), run_time=1.6)
        self.at("Across them")
        self.play(*[Tw(p, "occ", 1.0 if Y[i].sum() > 0 else 0.0) for i, p in enumerate(g.ponds)], run_time=1.5)
        self.at("pattern of histories")
        self.play(*[Indicate(b, color=WHITE, scale_factor=1.1) for b in g.bx[::3]], run_time=1.5)
        t1, t2 = ValueTracker(0), ValueTracker(0)
        d1 = Dial([RX, 1.25, 0], 1.4, t1, "detection per visit", 3.1, 0.7)
        d2 = Dial([RX, -1.7, 0], 1.4, t2, "fraction occupied, p", 0.0, -2.45)
        self.at("A model estimates")
        self.play(FadeIn(d1), FadeIn(d2), run_time=1.0)
        self.add(d1.read, d2.read)
        a1 = Arrow([0.9, 0.8, 0], [2.5, 1.3, 0], color=TEXT, buff=0, stroke_width=5)
        a2 = Arrow([0.9, -0.8, 0], [2.5, -1.6, 0], color=TEXT, buff=0, stroke_width=5)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.at("chance of detection")
        self.play(t1.animate.set_value(min(1, D_HAT * 1.5)), run_time=1.2)
        self.play(t1.animate.set_value(D_HAT), run_time=0.8)
        self.at("fraction occupied together")
        self.play(t2.animate.set_value(min(1, P_HAT * 1.25)), run_time=1.0)
        self.play(t2.animate.set_value(P_HAT), run_time=0.8)
        self.finish()


class S10Naive(Sc):
    def construct(self):
        g = Grid40()
        g.add_to(self, lit=True)
        self.wait(0.3)
        self.at("A naive count")
        self.play(*[Indicate(p, color=TEAL, scale_factor=1.2) for i, p in enumerate(g.ponds) if Y[i].sum() > 0][:14], run_time=1.6)
        # bars
        base = -2.6
        unit = 5.2
        x1, x2 = 3.2, 5.6
        ln = Line([2.0, base, 0], [6.8, base, 0], color=GREY, stroke_width=4)
        b1 = Rectangle(width=1.6, height=NAIVE * unit, fill_color=GREY, fill_opacity=0.85, stroke_width=0).move_to([x1, base + NAIVE * unit / 2, 0])
        n1 = T("naive", 30, TEXT).move_to([x1, base - 0.4, 0])
        v1 = M(f"{NAIVE:.2f}", 34, TEXT).next_to(b1, UP, buff=0.12)
        self.play(Create(ln), FadeIn(n1), GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=1.2)
        self.at("The corrected estimate")
        b2 = Rectangle(width=1.6, height=P_HAT * unit, fill_color=TEAL, fill_opacity=0.85, stroke_width=0).move_to([x2, base + P_HAT * unit / 2, 0])
        n2 = T("corrected", 30, TEAL).move_to([x2, base - 0.4, 0])
        v2 = M(f"{P_HAT:.2f}", 34, TEAL).next_to(b2, UP, buff=0.12)
        self.play(FadeIn(n2), GrowFromEdge(b2, DOWN), run_time=1.4)
        self.play(FadeIn(v2), run_time=0.5)
        self.at("some silent ponds")
        sil = [g.ponds[i] for i in SILENT_OCC]
        self.play(*[Tw(p, "occ", 1.0) for p in sil], *[Tw(p, "dash", 1.0) for p in sil],
                  *[Indicate(p, color=TEAL, scale_factor=1.6) for p in sil], run_time=1.6)
        self.at("Treat every silent")
        sh = [g.ponds[i] for i in ZERO]
        self.play(*[Indicate(p, color=GREY, scale_factor=1.25) for p in sh[:12]], run_time=1.4)
        self.at("occupancy is counted")
        ln2 = DashedLine([x1 - 0.8, base + P_HAT * unit, 0], [x2 - 0.8, base + P_HAT * unit, 0], color=TEAL, stroke_width=4)
        low = T("counted low", 30, TEXT).move_to([x1, base + P_HAT * unit + 0.5, 0])
        self.play(Create(ln2), Indicate(b1, color=WHITE, scale_factor=1.04), FadeIn(low), run_time=1.2)
        self.finish()


MD = [(-79.49, 39.72), (-75.79, 39.72), (-75.70, 39.40), (-75.60, 38.70), (-75.05, 38.45), (-75.24, 38.03),
      (-75.90, 37.95), (-76.30, 38.20), (-76.35, 38.55), (-76.80, 38.45), (-77.25, 38.35), (-77.05, 38.80),
      (-77.55, 39.10), (-78.25, 39.55), (-78.35, 39.62), (-79.48, 39.20)]


def md_pts(cx, cy, w=8.4):
    lon0, lon1, lat0, lat1 = -79.5, -75.0, 37.9, 39.75
    s = w / (lon1 - lon0)
    return [np.array([cx + (x - (lon0 + lon1) / 2) * s, cy + (y - (lat0 + lat1) / 2) * s * 1.28, 0]) for x, y in MD]


class S11Mackenzie(Sc):
    def construct(self):
        t1 = T("MacKenzie and colleagues", 42, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        t2 = T("Ecology, 2002", 34, TEAL).move_to([0, 2.45, 0])
        self.at("Daryl", lead=0.0)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(t2), run_time=0.6)
        self.at("They tested")
        pts = md_pts(0, -0.45)
        _bx = (min(q[0] for q in pts) + max(q[0] for q in pts)) / 2
        pts = [q - np.array([_bx, 0, 0]) for q in pts]
        outline = Polygon(*pts, color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.18)
        self.play(Create(outline), run_time=0.9)
        rs = np.random.RandomState(4)
        dots = VGroup()
        P2 = [(q[0], q[1]) for q in pts]

        def inside(x, y):
            c = False
            for i in range(len(P2)):
                x1, y1 = P2[i]
                x2, y2 = P2[(i + 1) % len(P2)]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    c = not c
            return c
        while len(dots) < 22:
            x, y = rs.uniform(-4.2, 4.2), rs.uniform(-1.8, 0.9)
            if inside(x, y):
                dots.add(Dot([x, y, 0], radius=0.12, color=TEAL))
        self.at("volunteer surveys")
        self.play(FadeIn(dots, lag_ratio=0.12), run_time=1.0)
        self.at("wetlands")
        self.play(*[Indicate(d, color=TEAL, scale_factor=1.8) for d in list(dots)[:10]], run_time=1.2)
        toad = frog([-5.2, -2.7, 0], 3.2, 0.0)
        toad[0].set_fill(BROWN)
        self.at("made two years")
        lb = T("volunteer surveys, 2000", 32, TEXT).move_to([0, -2.9, 0])
        self.play(FadeIn(lb), FadeIn(toad), run_time=0.9)
        self.finish()


class S12Toads(Sc):
    def construct(self):
        base = -2.3
        unit = 6.0
        ln = Line([-6.0, base, 0], [6.0, base, 0], color=GREY, stroke_width=4)
        toad = frog([-4.9, 2.9, 0], 3.2, 0.0)
        toad[0].set_fill(BROWN)
        ttl = T("American toads", 36, TEXT).move_to([-2.5, 2.9, 0])
        self.play(Create(ln), FadeIn(toad), FadeIn(ttl), run_time=1.0)
        x1, x2 = -2.2, 2.4
        h1, h2 = 0.34 * unit, 0.49 * unit
        self.at("detected at least")
        b1 = Rectangle(width=2.4, height=h1, fill_color=GREY, fill_opacity=0.85, stroke_width=0).move_to([x1, base + h1 / 2, 0])
        l1 = VGroup(T("detected", 30, TEXT), M("10 / 29 = 0.34", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([x1, base - 0.7, 0])
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=1.6)
        self.at("only about")
        self.play(Indicate(b1, color=WHITE, scale_factor=1.04), run_time=1.0)
        self.at("The model put")
        b2 = Rectangle(width=2.4, height=h2, fill_color=TEAL, fill_opacity=0.85, stroke_width=0).move_to([x2, base + h2 / 2, 0])
        l2 = VGroup(T("estimated occupied", 30, TEAL), M("0.49", 28, TEAL)).arrange(DOWN, buff=0.1).move_to([x2, base - 0.7, 0])
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=1.6)
        self.at("near one half")
        gap = Rectangle(width=2.4, height=h2 - h1, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.15).move_to([x1, base + h1 + (h2 - h1) / 2, 0])
        ht = VGroup(*[frog([x1 + dx, base + h1 + 0.3, 0], 1.3, i) for i, dx in enumerate((-0.6, 0.0, 0.6))])
        gl = T("there, never heard", 32, TEAL).move_to([x1 - 0.0, base + h2 + 0.55, 0])
        self.play(FadeIn(gap), FadeIn(ht), FadeIn(gl), run_time=1.2)
        self.finish()


class S13Rules(Sc):
    def construct(self):
        g = Grid40()
        g.add_to(self, lit=True)
        texts = [("occupancy fixed", "within the season"), ("no false", "detections"), ("detection independent", "among sites and visits")]
        ys = [2.3, 0.2, -1.9]
        marks = [("The method has", None), ("Occupancy must", 0), ("Toads must", 1), ("detection must", 2)]
        cards = []
        for (a, b), y in zip(texts, ys):
            box = RoundedRectangle(corner_radius=0.2, width=5.3, height=1.7, stroke_color=TEXT, stroke_width=3,
                                   fill_color=TEXT, fill_opacity=0.1).move_to([RX + 0.0, y, 0])
            tx = VGroup(T(a, 24, TEXT), T(b, 24, TEXT)).arrange(DOWN, buff=0.1).move_to(box.get_center() + LEFT * 0.3)
            cards.append(VGroup(box, tx))
        self.wait(0.3)
        self.at("The method has")
        self.play(*[Indicate(p, color=WHITE, scale_factor=1.1) for p in g.ponds[::4]], run_time=1.4)
        for i, (ph, nth) in enumerate((("Occupancy must", 0), ("Toads must", 0), ("And detection", 0))):
            self.at(ph)
            self.play(FadeIn(cards[i], shift=LEFT * 0.4), run_time=0.8)
            self.wait(0.5)
            ck = VGroup(Line([-0.25, 0, 0], [-0.07, -0.2, 0]), Line([-0.07, -0.2, 0], [0.3, 0.28, 0])).set_stroke(TEAL, 10)
            ck.move_to(cards[i][0].get_right() + LEFT * 0.65)
            self.play(Create(ck), cards[i][0].animate.set_stroke(TEAL, 4), run_time=0.7)
            if i == 0:
                self.play(Indicate(g.bg, color=WHITE, scale_factor=1.02), run_time=1.0)
            elif i == 1:
                self.play(*[Indicate(p, color=GREY, scale_factor=1.15) for i2, p in enumerate(g.ponds) if i2 in ZERO[:8]], run_time=1.0)
            else:
                self.play(*[Indicate(p, color=TEAL, scale_factor=1.12) for p in g.ponds[8:16]], run_time=1.0)
        self.finish()


class S14Rule(Sc):
    def construct(self):
        L, R = -4.1, 4.1
        pc = BP([0, 0.2, 0], 3.4, 2.4, occ=0.0, dash=0.0, ph=0.3)
        bc = boxes(0, -1.5, [0, 0, 0], s=0.9, gap=0.2, tsize=44)
        self.add(pc, bc)
        self.wait(0.6)
        self.at("not proof")
        pl = BP([L, 0.2, 0], 3.4, 2.4, occ=0.0, dash=0.0, ph=0.1)
        pr = BP([R, 0.2, 0], 3.4, 2.4, occ=1.0, dash=1.0, ph=0.6)
        toad = hidden_toad([R, 0.2, 0], 3.4)
        rd = reeds([R, 0.2, 0], 3.4)
        el = T("empty", 38, TEXT).move_to([L, -1.5, 0])
        r1 = T("occupied,", 34, TEAL).move_to([R, -1.3, 0])
        r2 = T("missed", 34, TEAL).move_to([R, -1.85, 0])
        self.play(FadeOut(pc), FadeIn(pl), FadeIn(pr), FadeIn(toad), FadeIn(rd), FadeIn(el), FadeIn(r1), FadeIn(r2), run_time=1.2)
        mg = VGroup(Circle(radius=0.95, color=YELLOW, stroke_width=8), Line([0.67, -0.67, 0], [1.4, -1.4, 0]).set_stroke(YELLOW, 10))
        mg.move_to([0, -1.5, 0]).shift(LEFT * 0.0)
        self.at("How hard")
        self.play(FadeIn(mg, scale=1.4), run_time=0.8)
        q = VGroup(T("how hard did", 32, YELLOW), T("you look?", 32, YELLOW)).arrange(DOWN, buff=0.1).move_to([0, 1.2, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.play(mg.animate.shift(LEFT * 0.5), run_time=0.7)
        self.play(mg.animate.shift(RIGHT * 1.0), run_time=0.9)
        self.at("before any pond")
        self.play(mg.animate.shift(LEFT * 0.5), Indicate(el, color=YELLOW, scale_factor=1.15), Indicate(r1, color=YELLOW, scale_factor=1.15), run_time=1.5)
        self.finish()


class S15End(EndCard):
    LINE = "A survey zero is a result of looking, not proof of absence."
