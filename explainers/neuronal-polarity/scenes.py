"""Neuronal polarity, chapter 1: Cut the Axon (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The one plotted chart (scene s22) is computed from the lesson's race model: five neurites, four at
15 micrometres and one at 20, a supply of 20 micrometres an hour shared in proportion to length squared
(feedback plus competition), against growth in simple proportion to length (illustrative model).
The chart's length axis is logarithmic, so equal vertical gaps mean equal ratios.

COLOR MAP (one color per concept, whole chapter series; taken from scenes.old.py)
  YELLOW = the axon, and the neurite that wins and becomes it
  BLUE   = dendrites and dendrite proteins (MAP2, receptors, spines)
  GREY   = cell body, outlines, the dish, neurites that have not been chosen
  LG     = light grey, for label text that is not a biological concept
  GREEN  = PIP3 and positive feedback
  RED    = negative feedback / competition, a blocked step, the cut
  ORANGE = actin
  TEAL   = microtubules (the tracks)
  PURPLE = ankyrin G, the axon initial segment, the gate
  GOLD   = guide text and questions (not a biological concept)
  NEURITE_COLS = five pastel hues (pink, mint, tan, periwinkle, white) used ONLY to tell the five
                 young neurites apart; they carry no meaning.
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LG = "#C5CAD6"
SOMA_FILL = "#262b36"
NEURITE_COLS = ["#FF8FAB", "#7FD1AE", "#E0C3A0", "#8FA8FF", "#F2F2F2"]

C0 = np.array([-2.4, -0.1, 0.0])                 # cell body of the big mature neuron
FULL_D = [(112, 2.1), (155, 2.2), (205, 2.1), (250, 2.0)]
YA = [25, 95, 165, 230, 305]                       # angles of the five young neurites (index 0 leads)


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def lab(text, col=TEXT, size=28, pos=(0, 0), **kw):
    return T(text, max(size, 28), col, **kw).move_to([pos[0], pos[1], 0])


def leader(a, b, col=TEXT, w=3):
    return Line(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), color=col, stroke_width=w)


# ---------------------------------------------------------------------------------------------
# opacity helpers (set_opacity would fill outline-only shapes, so scale each piece's own opacities)
# ---------------------------------------------------------------------------------------------
def _base(m):
    if not hasattr(m, "_b"):
        m._b = (m.get_fill_opacity(), m.get_stroke_opacity())
    return m._b


def fx(mob, f):
    """animations that set a mobject to fraction f of its normal opacity"""
    out = []
    for m in mob.family_members_with_points():
        b = _base(m)
        out.append(m.animate.set_fill(opacity=b[0] * f).set_stroke(opacity=b[1] * f))
    return out


def setf(mob, f):
    for m in mob.family_members_with_points():
        b = _base(m)
        m.set_fill(opacity=b[0] * f).set_stroke(opacity=b[1] * f)
    return mob


# ---------------------------------------------------------------------------------------------
# the neuron: tapering dendrite arbors, an even-width axon, a round cell body
# ---------------------------------------------------------------------------------------------
def tube(pts, ws, color):
    pts = [np.array(p, float) for p in pts]
    n = len(pts)
    left, right = [], []
    for i, p in enumerate(pts):
        d = pts[1] - pts[0] if i == 0 else (pts[-1] - pts[-2] if i == n - 1 else pts[i + 1] - pts[i - 1])
        d = d / (np.linalg.norm(d) + 1e-9)
        nr = np.array([-d[1], d[0], 0.0])
        w = max(ws[i], 0.03)
        left.append(p + nr * w / 2)
        right.append(p - nr * w / 2)
    return Polygon(*(left + right[::-1]), stroke_width=0, fill_color=color, fill_opacity=1)


def arbor(c, ang, trunk, s, R, color):
    """one dendrite: a tapering trunk with two branches and four twigs. Returns (VGroup(trunk, twigs), ends)."""
    d = u(ang)
    p0 = c + d * R * 0.8
    pm = p0 + u(ang + 4) * trunk * s * 0.5
    p1 = pm + u(ang - 5) * trunk * s * 0.5
    trunk_poly = tube([p0, pm, p1], [0.26 * s, 0.17 * s, 0.10 * s], color)
    twigs = VGroup()
    ends = []
    for sg in (-1, 1):
        a = ang + sg * 34
        be = pm + u(a) * trunk * s * 0.42
        twigs.add(tube([pm, be], [0.14 * s, 0.07 * s], color))
        for sg2 in (-1, 1):
            a2 = a + sg2 * 30
            e2 = be + u(a2) * trunk * s * 0.17
            twigs.add(tube([be, e2], [0.07 * s, 0.03 * s], color))
            ends.append((e2, a2))
    ends.append((p1, ang - 5))
    return VGroup(trunk_poly, twigs), ends


class Neu:
    def __init__(self, c=C0, s=1.12, dends=FULL_D, axon_len=9.0, R=0.8, wob=0.1, axw=13, t1=1.0):
        self.c = np.array([c[0], c[1], 0.0])
        self.s = s
        self.dd = dends
        self.R = R * s
        self.L = axon_len
        self.wob = wob * s
        self.axw = axw
        self.soma = Circle(radius=self.R, stroke_color=GREY, stroke_width=max(2.0, 4 * s),
                           fill_color=SOMA_FILL, fill_opacity=1).move_to(self.c)
        self.dends, self.ends = [], []
        for ang, tl in dends:
            g, e = arbor(self.c, ang, tl, s, self.R, BLUE)
            self.dends.append(g)
            self.ends.append(e)
        self.dgroup = VGroup(*self.dends)
        self.axon = self.piece(0, t1)
        self.group = VGroup(self.axon, self.dgroup, self.soma)

    def pt(self, t):
        x = self.c[0] + self.R * 0.9 + t * self.L
        return np.array([x, self.c[1] + self.wob * np.sin(1.1 * (x - self.c[0]) / self.s), 0.0])

    def piece(self, t0, t1, color=YELLOW, w=None):
        return ParametricFunction(self.pt, t_range=[t0, t1, (t1 - t0) / 80], color=color,
                                  stroke_width=w or self.axw)

    def outer(self, i):
        return max(self.ends[i], key=lambda e: np.linalg.norm(e[0] - self.c))

    def trunk_end(self, i):
        return self.ends[i][-1]

    def polys(self, i):
        """centre-line polylines of dendrite i: one to the trunk end and four to the twig ends"""
        ang, trunk = self.dd[i]
        s, R, c = self.s, self.R, self.c
        p0 = c + u(ang) * R * .8
        pm = p0 + u(ang + 4) * trunk * s * .5
        p1 = pm + u(ang - 5) * trunk * s * .5
        out = [[p0, pm, p1]]
        for sg in (-1, 1):
            a = ang + sg * 34
            be = pm + u(a) * trunk * s * .42
            for sg2 in (-1, 1):
                out.append([p0, pm, be, be + u(a + sg2 * 30) * trunk * s * .17])
        return out

    def spines(self, col=BLUE, sw=4):
        """small lollipop spines along every dendrite trunk"""
        g = VGroup()
        for i, (ang, trunk) in enumerate(self.dd):
            p0, pm, p1 = self.polys(i)[0]
            for k, f in enumerate((.25, .55, .85)):
                pos = p0 + (p1 - p0) * f if f < .5 else pm + (p1 - pm) * (f - .5) * 2
                side = 1 if (k + i) % 2 == 0 else -1
                d = (p1 - p0) / np.linalg.norm(p1 - p0)
                nr = np.array([-d[1], d[0], 0.0]) * side
                a = pos + nr * .1 * self.s
                b = pos + nr * (.1 + .3) * max(self.s, .9)
                g.add(VGroup(Line(a, b, color=col, stroke_width=sw),
                             Circle(radius=.1 * max(self.s, .9), stroke_color=col, stroke_width=2, fill_color=col,
                                    fill_opacity=.9).move_to(b)))
        return g


def poly_at(pl, f):
    pl = [np.array(p, float) for p in pl]
    seg = [np.linalg.norm(pl[i + 1] - pl[i]) for i in range(len(pl) - 1)]
    tot = sum(seg)
    d = f * tot
    for i, sl in enumerate(seg):
        if d <= sl or i == len(seg) - 1:
            return pl[i] + (pl[i + 1] - pl[i]) * min(1.0, d / max(sl, 1e-9))
        d -= sl
    return pl[-1]


def bend_pts(p0, h0, h1, L, n=120):
    """points of a curve starting at p0, heading h0 degrees and turning steadily to h1 over length L"""
    pts = [np.array(p0, float)]
    for k in range(1, n + 1):
        h = h0 + (h1 - h0) * (k - .5) / n
        pts.append(pts[-1] + u(h) * (L / n))
    return pts


def grow_line(pts, tr, color, w):
    """a line that shows the first tr (0..1) of pts"""
    m = VMobject().set_stroke(color, w).set_fill(opacity=0)

    def upd(mm):
        k = max(2, int(round(tr.get_value() * (len(pts) - 1))) + 1)
        mm.set_points_as_corners(pts[:k])
    m.add_updater(upd, call_updater=True)
    return m


def tip_of(pts, tr):
    return pts[max(1, int(round(tr.get_value() * (len(pts) - 1))))]


def cutmark(p, h=0.5):
    return DashedLine(p + UP * h, p + DOWN * h, color=RED, stroke_width=6, dash_length=0.12)


def blade(tip, side=1):
    """a scalpel whose point is at `tip`; body leans up and to `side` (+1 right, -1 left)"""
    g = VGroup(Polygon([0, 0, 0], [side * 1.4, .55, 0], [side * 1.4, .3, 0],
                       stroke_width=0, fill_color=TEXT, fill_opacity=1),
               Polygon([side * 1.4, .55, 0], [side * 2.2, .9, 0], [side * 2.2, .65, 0], [side * 1.4, .3, 0],
                       stroke_width=0, fill_color=GREY, fill_opacity=1))
    return g.shift(np.array(tip, float))


def sprinkles():
    rng = np.random.RandomState(11)
    blue = VGroup(*[Dot([rng.uniform(-5.6, -3.6), rng.uniform(-2.3, 2.3), 0], radius=.07, color=BLUE) for _ in range(16)])
    yel = VGroup(*[Dot([rng.uniform(-0.9, 6.3), -0.15 + rng.uniform(-.42, .42), 0], radius=.07, color=YELLOW) for _ in range(16)])
    return blue, yel


def do_cut(scene, n, t, side=1, drift=(.9, -.5), shift_in=2.4):
    """lower a blade onto the axon of Neu n at parameter t, cut, let the far piece drift off and fade.
    Returns (prox, mark). The Neu's axon is replaced by the proximal piece."""
    cp = n.pt(t)
    bl = blade(cp, side).shift(UP * shift_in + RIGHT * shift_in * .35 * side)
    scene.add(bl)
    scene.play(bl.animate.shift(DOWN * shift_in + LEFT * shift_in * .35 * side), run_time=.5, rate_func=rate_functions.ease_in_quad)
    prox, dist = n.piece(0, t, w=n.axw), n.piece(t, 1.0, w=n.axw)
    n.group.remove(n.axon)
    scene.remove(n.axon)
    n.axon = prox
    n.group.add(prox)
    scene.add(prox, dist, bl)
    cm = cutmark(cp, .5)
    scene.play(FadeIn(cm, run_time=.15))
    scene.play(dist.animate.shift(RIGHT * drift[0] + DOWN * (-drift[1])).rotate(-.12).set_opacity(0),
               bl.animate.shift(UP * shift_in + RIGHT * shift_in * .35 * side).set_opacity(0), run_time=1.0)
    return prox, cm


# ---------------------------------------------------------------------------------------------
# the young stage-3 neuron: five neurites, growth cones, dish
# ---------------------------------------------------------------------------------------------
def fan_shape(d, col, r=0.55):
    ang = np.degrees(np.arctan2(d[1], d[0]))
    pts = [np.zeros(3)] + [u(a) * r for a in np.linspace(ang - 48, ang + 48, 9)]
    poly = Polygon(*pts, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.28)
    fil = VGroup(*[Line(u(a) * r, u(a) * (r + 0.2), color=col, stroke_width=2.5) for a in (ang - 30, ang, ang + 30)])
    g = VGroup(poly, fil)
    g.base = np.zeros(3)
    return g


class Young:
    def __init__(self, c=(0, 0), sc=1.0, lens=(2.3,) * 5, cols=None, col=GREY, cones=False):
        self.c = np.array([c[0], c[1], 0.0])
        self.sc = sc
        self.R = 0.75 * sc
        self.tr = [ValueTracker(l * sc) for l in lens]
        self.dirs = [u(a) for a in YA]
        self.lines, self.fans = [], []
        for i, d in enumerate(self.dirs):
            colr = (cols or [col] * 5)[i]
            ln = Line(self.c + d * self.R * .9, self.c + d * (self.R + .5), color=colr, stroke_width=9 * max(sc, .65))
            ln.add_updater(lambda m, d=d, t=self.tr[i]: m.put_start_and_end_on(
                self.c + d * self.R * .9, self.c + d * (self.R + max(t.get_value(), .05))))
            self.lines.append(ln)
        self.soma = Circle(radius=self.R, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL,
                           fill_opacity=1).move_to(self.c)
        self.fan_group = VGroup()
        if cones:
            self.make_fans(cols or [col] * 5)
        self.group = VGroup(*self.lines, self.fan_group, self.soma)

    def tip(self, i):
        return self.c + self.dirs[i] * (self.R + self.tr[i].get_value())

    def make_fans(self, cols, add=True):
        out = VGroup()
        for i, d in enumerate(self.dirs):
            f = fan_shape(d, cols[i], 0.55 * max(self.sc, .75))
            f.add_updater(lambda m, i=i: (m.shift(self.tip(i) - m.base), setattr(m, "base", self.tip(i))), call_updater=True)
            self.fans.append(f)
            out.add(f)
        if add:
            self.fan_group.add(*out)
        return out

    def recolor(self, i, col):
        out = [self.lines[i].animate.set_color(col)]
        if self.fans:
            out.append(self.fans[i].animate.set_color(col))
        return out


# ---------------------------------------------------------------------------------------------
# scenes 0-7: the two ends of a neuron
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "Cut the Axon"


class S01(SpokenScene):
    def construct(self):
        n = Neu()
        n.dgroup.set_color(GREY)
        n.axon.set_color(GREY)
        ld = lab("dendrites", BLUE, 30, (-5.3, 2.5))
        la = lab("axon", YELLOW, 30, (3.0, 0.65))
        self.play(FadeIn(n.group), run_time=1.0)
        self.at("its dendrites")
        self.play(n.dgroup.animate.set_color(BLUE), FadeIn(ld), run_time=.6)
        self.at("its axon")
        self.play(n.axon.animate.set_color(YELLOW), FadeIn(la), run_time=.6)
        self.at("how does it")
        q = lab("?", GOLD, 96, (-0.9, 1.3), font=TITLE_FONT)
        self.play(FadeIn(q, scale=.6), run_time=.5)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        n = Neu()
        setf(n.dgroup, .35)
        setf(n.axon, .3)
        self.add(n.group)
        ld = lab("dendrites", BLUE, 30, (-5.3, 2.5))
        self.add(ld)
        # input arrows come in during the first sentence
        arrows, blobs = VGroup(), VGroup()
        for i in range(4):
            pt, a = n.outer(i)
            d = u(200 if i == 3 else a)      # the lowest dendrite is approached from the side so the input stays in frame
            arrows.add(Arrow(pt + d * .9, pt + d * .12, buff=0, color=TEXT, stroke_width=5, tip_length=.22,
                             max_tip_length_to_length_ratio=.4))
            blobs.add(Circle(radius=.2, stroke_color=GREY, fill_color=GREY, fill_opacity=.5, stroke_width=2).move_to(pt + d * 1.1))
        self.play(*fx(n.dgroup, 1), run_time=.5)
        self.play(*[GrowArrow(a) for a in arrows], run_time=.5)
        self.at("several")
        badges = VGroup()
        for i, (ang, tl) in enumerate(FULL_D):
            p = n.c + u(ang) * (n.R * .8 + tl * .22)
            b = Circle(radius=.28, stroke_color=BLUE, stroke_width=3, fill_color=SOMA_FILL, fill_opacity=1).move_to(p)
            badges.add(VGroup(b, T(str(i + 1), 28, TEXT).move_to(p)))
        sv = lab("several", BLUE, 34, (-0.1, 2.75))
        svl = leader((-1.0, 2.5), (-2.55, 1.35), BLUE, 3)
        self.play(LaggedStart(*[FadeIn(b, scale=1.4) for b in badges], lag_ratio=.3), FadeIn(sv), Create(svl), run_time=.9)
        self.at("short")
        pa, pb = n.ends[3][-1][0], n.c + u(250) * n.R * .8
        nrm0 = np.array([.94, -.34, 0.0])
        off = nrm0 * .55
        dim = DoubleArrow(pa + off, pb + off, buff=0, color=LG, stroke_width=4, tip_length=.17)
        sh = lab("short", BLUE, 34, ((pa + pb)[0] / 2 + nrm0[0] * 1.35, (pa + pb)[1] / 2 + nrm0[1] * 1.35))
        self.play(FadeOut(VGroup(sv, svl)), GrowFromCenter(dim), FadeIn(sh), run_time=.5)
        self.at("branched")
        self.play(FadeOut(badges), FadeOut(dim), FadeOut(sh), run_time=.3)
        twigs = VGroup(*[d[1] for d in n.dends])
        br = lab("branched", BLUE, 34, (-0.1, -2.7))
        brl = leader((-1.15, -2.55), (-2.85, -2.2), BLUE, 3)
        self.play(Indicate(twigs, color=BLUE, scale_factor=1.08), FadeIn(br), Create(brl), run_time=.8)
        self.at("receive input")
        t0_ = arrows[0].get_start()
        inp = lab("input", TEXT, 34, (t0_[0] - .85, t0_[1] + .1))
        self.play(FadeOut(VGroup(br, brl)), FadeIn(inp), run_time=.4)
        self.at("other cells")
        b3 = blobs[3].get_center()
        oc = lab("other cells", LG, 30, (b3[0] + 0.2, b3[1] - .55))
        self.play(FadeIn(blobs), FadeIn(oc), run_time=.5)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        n = Neu()
        setf(n.dgroup, .35)
        setf(n.axon, .3)
        self.add(n.group)
        self.play(*fx(n.axon, 1), run_time=.5)
        self.at("single")
        single = lab("single", YELLOW, 32, (0.0, 0.95))
        self.play(FadeIn(single), run_time=.4)
        self.at("even in width")
        g1 = ParametricFunction(lambda t: n.pt(t) + UP * .3, t_range=[0.04, 1, .01], color=LG, stroke_width=3)
        g2 = ParametricFunction(lambda t: n.pt(t) + DOWN * .3, t_range=[0.04, 1, .01], color=LG, stroke_width=3)
        ew = lab("even width", TEXT, 32, (2.9, 0.95))
        self.play(Create(g1), Create(g2), FadeIn(ew), run_time=.8)
        self.at("often very long")
        y0 = -1.1
        a1 = Line([-1.5, y0, 0], [4.9, y0, 0], color=LG, stroke_width=4)
        a2 = Arrow([5.5, y0, 0], [6.9, y0, 0], buff=0, color=LG, stroke_width=4, tip_length=.25)
        brk = VGroup(*[Line([x - .12, y0 - .25, 0], [x + .12, y0 + .25, 0], color=LG, stroke_width=4) for x in (5.05, 5.35)])
        ol = lab("often very long, up to centimetres", TEXT, 30, (2.6, -1.75))
        self.play(Create(a1), FadeIn(brk), run_time=.5)
        self.play(GrowArrow(a2), FadeIn(ol), run_time=.4)
        self.at("it carries", lead=.3)
        self.play(FadeOut(VGroup(single, g1, g2, ew, a1, a2, brk, ol)), run_time=.4)
        tr = ValueTracker(0)
        pulse = VGroup(Dot(radius=.5, color=YELLOW).set_opacity(.3), Dot(radius=.3, color=YELLOW).set_opacity(.6),
                       Dot(radius=.17, color=TEXT))
        pulse.add_updater(lambda m: m.move_to(n.pt(tr.get_value())))
        pulse.move_to(n.pt(0))
        ap = lab("action potential", TEXT, 32, (0, 0))
        ap.add_updater(lambda m: m.move_to(n.pt(tr.get_value()) + UP * .95))
        self.add(pulse)
        self.play(FadeIn(ap, run_time=.25), tr.animate.set_value(.34), run_time=.6, rate_func=linear)
        self.play(tr.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.at("other cells")
        oc = lab("to other cells", LG, 30, (5.0, -0.85))
        self.play(FadeIn(oc), run_time=.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        n = Neu()
        self.add(n.group)
        a = T("polarity", 42, GOLD, TITLE_FONT)
        b = T("= two distinct domains", 36, TEXT, TITLE_FONT)
        VGroup(a, b).arrange(RIGHT, buff=.25).move_to([0.9, 3.3, 0])
        self.play(FadeIn(a), run_time=.4)
        self.at("two distinct domains")
        zl = VGroup(Ellipse(width=5.2, height=6.0, stroke_width=0, fill_color=BLUE, fill_opacity=.09),
                    DashedVMobject(Ellipse(width=5.2, height=6.0, color=BLUE, stroke_width=3), num_dashes=50)).move_to([-3.75, -0.1, 0])
        zr = VGroup(RoundedRectangle(corner_radius=.4, width=7.7, height=2.9, stroke_width=0, fill_color=YELLOW, fill_opacity=.09),
                    DashedVMobject(RoundedRectangle(corner_radius=.4, width=7.7, height=2.9, color=YELLOW, stroke_width=3), num_dashes=50)).move_to([3.0, -0.1, 0])
        dl = lab("dendritic domain", BLUE, 28, (-3.75, -3.4))
        al = lab("axonal domain", YELLOW, 28, (3.0, -1.95))
        self.play(FadeIn(b), FadeIn(zl), FadeIn(zr), FadeIn(dl), FadeIn(al), run_time=.8)
        self.at("different in structure")
        st_d = lab("structure", BLUE, 28, (-4.95, 0.22))
        st_a = lab("structure", YELLOW, 28, (1.9, 0.95))
        self.play(FadeIn(st_d), FadeIn(st_a), Indicate(n.dgroup, color=BLUE, scale_factor=1.04),
                  Indicate(n.axon, color=YELLOW, scale_factor=1.1), run_time=.9)
        self.at("and molecules")
        blue, yel = sprinkles()
        ml_d = lab("molecules", BLUE, 28, (-4.95, -0.5))
        ml_a = lab("molecules", YELLOW, 28, (5.0, 0.95))
        self.play(FadeIn(ml_d), FadeIn(ml_a), FadeIn(blue), FadeIn(yel), run_time=.6)
        self.finish()


# the zoom inset shared by scenes 5 and 6: a magnified stretch of dendrite (blue) or axon (gold)
PC = (3.7, 0.1)
PW, PH = 6.4, 6.8
BT, BB = 1.75, -1.35          # top and bottom edges of the magnified band
PX0, PX1 = PC[0] - PW / 2 + .05, PC[0] + PW / 2 - .05


def zoom_inset(lp, col, bt=BT, bb=BB):
    ring = Circle(radius=.45, color=TEXT, stroke_width=3).move_to(lp)
    lines = VGroup()
    for cpt in [(PC[0] - PW / 2, PC[1] + PH / 2, 0), (PC[0] - PW / 2, PC[1] - PH / 2, 0)]:
        d = np.array(cpt, float) - lp
        d = d / np.linalg.norm(d)
        lines.add(Line(lp + d * .45, cpt, color=GREY, stroke_width=2))
    panel = RoundedRectangle(corner_radius=.2, width=PW, height=PH, stroke_color=GREY, stroke_width=2.5,
                             fill_color=BG, fill_opacity=1).move_to([PC[0], PC[1], 0])
    band = Rectangle(width=PW - .1, height=bt - bb, stroke_width=0, fill_color=col, fill_opacity=.25).move_to([PC[0], (bt + bb) / 2, 0])
    e1 = Line([PX0, bt, 0], [PX1, bt, 0], color=col, stroke_width=6)
    e2 = Line([PX0, bb, 0], [PX1, bb, 0], color=col, stroke_width=6)
    lines.set_z_index(-1)
    return ring, lines, panel, band, e1, e2


class S05(SpokenScene):
    def construct(self):
        n = Neu()
        blue, yel = sprinkles()
        self.add(n.group, blue, yel)
        self.at("molecular")
        self.play(Indicate(blue, color=BLUE, scale_factor=1.3), Indicate(yel, color=YELLOW, scale_factor=1.3), run_time=.7)
        self.at("dendrites carry")
        lp = (n.c + u(112) * (n.R * .8 + 1.0)).copy()
        ring, lines, panel, band, e1, e2 = zoom_inset(lp, BLUE, bt=2.2, bb=-1.9)
        self.play(*fx(n.axon, .35), FadeOut(yel), FadeOut(blue), FadeIn(ring), Create(lines), run_time=.5)
        self.play(FadeIn(panel), FadeIn(band), Create(e1), Create(e2), run_time=.5)
        self.at("map two")
        bt, bb = 2.2, -1.9
        rng = np.random.RandomState(3)
        pts = [(x, bb + .25 + rng.uniform(0, bt - bb - .5)) for x in list(np.linspace(.9, 2.55, 7)) + list(np.linspace(4.85, 6.5, 7))]
        md = VGroup(*[Dot([x, y, 0], radius=.11, color=BLUE) for x, y in pts])
        mchip = chip("MAP2", BLUE, 34).move_to([3.7, (bt + bb) / 2, 0])
        self.play(FadeIn(md), FadeIn(mchip), run_time=.6)
        self.at("receptors for")
        recs = VGroup()
        for x in (1.3, 2.7, 4.7, 6.1):
            recs.add(VGroup(Line([x, bt, 0], [x, bt + .3, 0], color=BLUE, stroke_width=7),
                            Line([x, bt + .3, 0], [x - .3, bt + .6, 0], color=BLUE, stroke_width=7),
                            Line([x, bt + .3, 0], [x + .3, bt + .6, 0], color=BLUE, stroke_width=7)))
        rl = lab("neurotransmitter receptors", BLUE, 28, (3.7, 3.2))
        self.play(Create(recs), FadeIn(rl), run_time=.7)
        self.at("often spines")
        sp = VGroup()
        for x in (1.5, 3.0, 4.5, 6.0):
            sp.add(VGroup(Line([x, bb, 0], [x + .05, bb - .35, 0], color=BLUE, stroke_width=7),
                          Circle(radius=.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=1).move_to([x + .05, bb - .6, 0])))
        sl = lab("spines", TEXT, 36, (3.7, -3.0))
        ms = n.spines(sw=6).set_opacity(1)
        self.play(FadeIn(sp), FadeIn(sl), FadeIn(ms), run_time=.2)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        n = Neu()
        setf(n.dgroup, .35)
        self.add(n.group)
        lp = n.pt(.17).copy()
        ring, lines, panel, band, e1, e2 = zoom_inset(lp, YELLOW)
        self.at("axon carries")
        self.play(FadeIn(ring), Create(lines), run_time=.4)
        self.play(FadeIn(panel), FadeIn(band), Create(e1), Create(e2), run_time=.5)
        self.at("tau")
        taus = VGroup()
        for x, y in ([(x, yy) for x in (1.0, 1.75, 2.5) for yy in (1.2, .75, .3)] +
                     [(x, yy) for x in (4.9, 5.65, 6.4) for yy in (1.2, .75, .3)]):
            taus.add(RoundedRectangle(corner_radius=.07, width=.5, height=.15, stroke_width=0, fill_color=YELLOW,
                                      fill_opacity=1).move_to([x + .08 * np.sin(7 * x + 3 * y), y, 0]))
        tchip = chip("tau", YELLOW, 34).move_to([3.7, .35, 0])
        self.play(FadeIn(taus, lag_ratio=.05), FadeIn(tchip), run_time=.6)
        self.at("channels")
        chs = VGroup()
        for x, y in ((1.5, BT), (3.7, BT), (5.9, BT), (2.0, BB), (5.4, BB)):
            chs.add(VGroup(RoundedRectangle(corner_radius=.12, width=.55, height=1.0, stroke_color=YELLOW, stroke_width=4,
                                            fill_color=YELLOW, fill_opacity=.55).move_to([x, y, 0]),
                           Line([x, y - .38, 0], [x, y + .38, 0], color=BG, stroke_width=5)))
        cl = lab("channels", YELLOW, 30, (3.7, 3.05))
        cll = leader((3.7, 2.78), (3.7, 2.35), YELLOW, 3)
        self.play(FadeIn(chs, scale=1.3), FadeIn(cl), Create(cll), run_time=.6)
        self.at("vesicle machinery")
        ves = VGroup()
        for x in (1.2, 3.0, 4.4, 6.0):
            ves.add(VGroup(Line([x - .22, -.95, 0], [x - .1, -.55, 0], color=YELLOW, stroke_width=4),
                           Line([x + .22, -.95, 0], [x + .1, -.55, 0], color=YELLOW, stroke_width=4),
                           Circle(radius=.28, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=.35).move_to([x, -.3, 0])))
        vl = lab("vesicle machinery", YELLOW, 30, (3.7, -3.0))
        vll = leader((3.7, -2.7), (3.7, -1.55), YELLOW, 3)
        self.play(FadeIn(ves, shift=UP * .2), FadeIn(vl), Create(vll), run_time=.7)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        n = Neu()
        setf(n.dgroup, .4)
        setf(n.axon, .4)
        self.add(n.group)
        rng = np.random.RandomState(7)
        tau = ValueTracker(0)
        dots = VGroup()
        polys = [n.polys(i) for i in range(4)]
        for k in range(230):
            if rng.rand() < .4:
                kind, i, pl, f, col = "a", 0, None, rng.uniform(.04, .9), YELLOW
            else:
                i = rng.randint(4)
                kind, pl, f, col = "d", polys[i][rng.randint(5)], rng.uniform(.4, 1.0), "#8FE3FF"
            delay, trav = rng.uniform(0, 3.0), rng.uniform(.9, 1.3)
            off = rng.uniform(-.06, .06)
            r0, th0 = .62 * np.sqrt(rng.rand()) * n.R / .9, rng.uniform(0, TAU)
            s0 = n.c + np.array([np.cos(th0), np.sin(th0), 0.0]) * r0
            ph = rng.uniform(0, TAU)
            dot = Dot(s0, radius=.075, color=col, stroke_width=0)

            def upd(m, kind=kind, pl=pl, f=f, delay=delay, trav=trav, off=off, s0=s0, ph=ph):
                T_ = tau.get_value()
                q = float(np.clip((T_ - delay) / trav, 0, 1))
                q = q * q * (3 - 2 * q)
                jit = np.array([np.sin(7 * T_ + ph), np.cos(6 * T_ + ph), 0.0]) * .035
                if kind == "a":
                    pos = n.pt(q * f) + UP * off
                else:
                    pos = poly_at(pl, q * f)
                w = min(1.0, q / .18)
                w = w * w * (3 - 2 * w)
                m.move_to(s0 * (1 - w) + pos * w + jit * (1 - w))
            dot.add_updater(upd, call_updater=True)
            dots.add(dot)
        self.add(dots)
        self.play(tau.animate.set_value(1.0), run_time=.1, rate_func=linear)
        self.play(tau.animate.set_value(3.55), run_time=3.45, rate_func=linear)
        self.at("keep them there")
        clock = Circle(radius=.85, color=TEXT, stroke_width=5, fill_color=SOMA_FILL, fill_opacity=1).move_to([3.5, 2.15, 0])
        cc = clock.get_center()
        ticks = VGroup(*[Line(cc + u(a) * .68, cc + u(a) * .8, color=TEXT, stroke_width=4) for a in (0, 90, 180, 270)])
        hand = Line(cc, cc + UP * .62, color=GOLD, stroke_width=7)
        hand.add_updater(lambda m, dt: m.rotate(-5.5 * dt, about_point=cc))
        hub = Dot(cc, radius=.07, color=TEXT)
        self.play(FadeIn(VGroup(clock, ticks, hub)), FadeIn(hand), tau.animate.set_value(4.6), run_time=.5)
        self.at("decades")
        self.play(FadeIn(lab("decades", GOLD, 44, (3.5, 0.95))), run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 8-13: the puzzle from the dish
# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    def construct(self):
        n = Neu()
        self.add(n.group)
        dish = RoundedRectangle(corner_radius=.7, width=13.4, height=7.3, stroke_color=LG, stroke_width=3)
        dl = lab("cultured neurons live in a dish", LG, 28, (3.2, -3.3))
        self.play(Create(dish), FadeIn(dl), run_time=.7)
        self.at("mature neuron")
        mn = lab("mature neuron", TEXT, 32, (2.4, -1.75))
        mnl = leader((1.2, -1.5), (-1.55, -.6), TEXT, 3)
        self.play(FadeIn(mn), Create(mnl), run_time=.5)
        self.at("cut its axon", lead=.55)
        t = 0.9 / n.L
        prox, cm = do_cut(self, n, t, drift=(.9, -.5))
        self.at("close to the")
        self.play(FadeOut(mn), FadeOut(mnl), run_time=.3)
        self.at("cell body")
        st = lab("short stump", YELLOW, 32, (0.4, -1.1))
        stl = leader((.3, -.8), (-.55, -.25), YELLOW, 3)
        self.play(FadeIn(st), Create(stl), run_time=.4)
        self.finish()


DENDL = [(35, 1.9), (100, 1.7), (165, .9), (230, 1.6)]
DENDR = [(40, 1.6), (110, 1.7), (170, 1.1), (235, 1.7)]
LC = (-4.8, -0.35)
RC = (2.65, -0.35)


def make_split(cut_right=True):
    S = SimpleNamespace()
    S.pl = RoundedRectangle(corner_radius=.25, width=6.5, height=6.6, stroke_color=GREY, stroke_width=2.5).move_to([-3.45, 0.4, 0])
    S.pr = S.pl.copy().move_to([3.45, 0.4, 0])
    S.tl = T("cut close to the cell body", 26, LG).move_to([-3.45, 3.35, 0])
    S.tr = T("cut far from the cell body", 26, LG).move_to([3.45, 3.35, 0])
    S.L = Neu(c=LC, s=1.1, dends=DENDL, axon_len=.55, axw=9, wob=.05)
    S.tcut = .5
    S.R = Neu(c=RC, s=1.1, dends=DENDR, axon_len=3.0, axw=9, wob=.05, t1=S.tcut if cut_right else 1.0)
    S.lcutp = S.L.pt(1.0)
    S.rcutp = S.R.pt(S.tcut)
    S.lcut = cutmark(S.lcutp, .45)
    S.rcut = cutmark(S.rcutp, .45)
    S.q = T("What grows out in each case?", 32, GOLD).move_to([0, -3.5, 0])
    S.ql = T("?", 96, GOLD, TITLE_FONT).move_to([-1.2, 0.3, 0])
    S.qr = T("?", 96, GOLD, TITLE_FONT).move_to([5.7, 0.3, 0])
    return S


def split_mobs(S):
    return [S.pl, S.pr, S.tl, S.tr, S.L.group, S.R.group, S.lcut, S.rcut, S.q, S.ql, S.qr]


class S09(SpokenScene):
    def construct(self):
        S = make_split(cut_right=False)
        self.play(FadeIn(S.pl), FadeIn(S.tl), FadeIn(S.L.group), FadeIn(S.lcut), run_time=.5)
        self.play(FadeIn(S.pr), FadeIn(S.R.group), run_time=.5)
        self.at("far from", lead=.7)
        prox, cm = do_cut(self, S.R, S.tcut, side=-1, drift=(.7, -.4), shift_in=2.2)
        self.play(FadeIn(S.tr), run_time=.2)
        self.at("what grows out")
        self.play(FadeIn(S.q), FadeIn(S.ql, scale=.6), FadeIn(S.qr, scale=.6), run_time=.6)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        S = make_split(True)
        self.add(*[m for m in split_mobs(S) if m is not S.q])
        think = T("Pause. What do you predict?", 40, GOLD, TITLE_FONT).move_to([0, -3.3, 0])
        bar_bg = Rectangle(width=8.0, height=.14, stroke_width=0, fill_color=GREY, fill_opacity=.4).move_to([0, -3.82, 0])
        tr = ValueTracker(1.0)
        bar = Rectangle(width=8.0, height=.14, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([0, -3.82, 0])
        bar.add_updater(lambda m: m.stretch_to_fit_width(max(.01, 8.0 * tr.get_value())).move_to([-4.0 + 4.0 * tr.get_value(), -3.82, 0]))
        self.play(FadeIn(think), FadeIn(bar_bg), FadeIn(bar), run_time=.4)
        self.play(tr.animate.set_value(0.0), run_time=4.4, rate_func=linear)
        self.finish()


def new_axon_geom(S):
    """the converted dendrite of the left panel: trunk end, and the path the new axon takes"""
    p1, h = S.L.trunk_end(0)
    pts = bend_pts(p1, h, 10, 2.2)
    return p1, pts


def style_converted(S, f=1.0):
    S.L.dends[0][0].set_color(YELLOW)
    S.L.dends[0][1].set_color(YELLOW)
    S.L.dends[0][1].set_fill(opacity=.55).set_stroke(opacity=.55)


class S11(SpokenScene):
    def construct(self):
        S = make_split(True)
        self.add(*split_mobs(S))
        rgrp = VGroup(S.pr, S.tr, S.R.group, S.rcut)
        self.play(S.pl.animate.set_stroke(TEXT, width=4), FadeOut(S.q), FadeOut(S.ql), FadeOut(S.qr), *fx(rgrp, .35), run_time=.5)
        self.at("one of the dendrites")
        d = S.L.dends[0]
        p1, pts = new_axon_geom(S)
        self.play(Indicate(d, color=YELLOW, scale_factor=1.1), run_time=.7)
        self.at("grow out")
        tr = ValueTracker(0.02)
        line = grow_line(pts, tr, YELLOW, 9)
        na = lab("new axon", YELLOW, 32, (0, 0))
        na.move_to([-2.4, 2.5, 0])
        self.add(line)
        self.play(d[0].animate.set_color(YELLOW), d[1].animate.set_color(YELLOW).set_opacity(.55), FadeIn(na), run_time=.25)
        self.play(tr.animate.set_value(1.0), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.finish()


def finish_left(S):
    """end state of the left panel: the dendrite has become a gold axon"""
    style_converted(S)
    p1, pts = new_axon_geom(S)
    line = VMobject().set_stroke(YELLOW, 9).set_fill(opacity=0)
    line.set_points_as_corners(pts)
    na = lab("new axon", YELLOW, 32, (-2.4, 2.5))
    return line, na


class S12(SpokenScene):
    def construct(self):
        S = make_split(True)
        self.add(*split_mobs(S))
        self.remove(S.ql, S.qr, S.q)
        line, na = finish_left(S)
        self.add(line, na)
        S.pl.set_stroke(TEXT, width=4)
        lgrp = VGroup(S.pl, S.tl, S.L.group, line, na)
        rgrp = VGroup(S.pr, S.tr, S.R.group, S.rcut)
        setf(rgrp, .35)
        self.play(*fx(lgrp, .35), *fx(rgrp, 1), S.pr.animate.set_stroke(TEXT, width=4), run_time=.4)
        self.at("the old axon")
        stump = S.R.piece(0, S.tcut, YELLOW, w=9)
        ghost = DashedVMobject(S.R.piece(S.tcut, 1.0, LG, w=9), num_dashes=22).set_opacity(.5)
        self.play(Indicate(stump, color=YELLOW, scale_factor=1.3), Create(ghost), run_time=.35)
        self.at("simply regrows", lead=.3)
        tr = ValueTracker(0.001)
        pts = [S.R.pt(S.tcut + (1.0 - S.tcut) * k / 80) for k in range(81)]
        reg = grow_line(pts, tr, YELLOW, 9)
        rl = lab("old axon regrows", YELLOW, 32, (4.65, -1.5))
        rll = leader((5.75, -1.12), pts[-1][:2] + np.array([0, -.15]), YELLOW, 3)
        self.add(reg, rl, rll)
        self.play(tr.animate.set_value(1.0), FadeOut(S.rcut), FadeOut(ghost), run_time=.65, rate_func=rate_functions.ease_out_sine)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        # the neuron that will lose its axon sits along the bottom
        nn = Neu(c=(-5.0, -2.45), s=.6, dends=[(95, 1.8), (150, 1.6), (210, 1.6)], axon_len=9.6, wob=.04, axw=9)
        imprint = VGroup(RoundedRectangle(corner_radius=.25, width=7.0, height=2.8, stroke_color=YELLOW, stroke_width=10),
                         T("AXON", 120, YELLOW, weight=BOLD))
        cross = VGroup(Line(imprint[0].get_corner(UL) + RIGHT * .15 + DOWN * .15, imprint[0].get_corner(DR) + LEFT * .15 + UP * .15, color=RED, stroke_width=14),
                       Line(imprint[0].get_corner(UR) + LEFT * .15 + DOWN * .15, imprint[0].get_corner(DL) + RIGHT * .15 + UP * .15, color=RED, stroke_width=14))
        tool = VGroup(RoundedRectangle(corner_radius=.2, width=1.6, height=1.5, stroke_width=0, fill_color=GREY, fill_opacity=1),
                      Rectangle(width=4.6, height=.4, stroke_width=0, fill_color=GREY, fill_opacity=1).shift(DOWN * .95))
        grp = VGroup(imprint, cross)
        imprint.move_to([0, 0.3, 0])
        cross.move_to(imprint.get_center())
        grp_imprint = VGroup(imprint)
        grp.rotate(-.1, about_point=imprint.get_center())
        tool.move_to([0, 3.4, 0])
        self.play(FadeIn(tool), run_time=.3)
        self.play(tool.animate.shift(DOWN * 1.7), run_time=.25)
        self.add(imprint)
        self.play(FadeIn(imprint, scale=1.25), tool.animate.shift(UP * 1.7), run_time=.3)
        self.at("not a permanent")
        self.play(Create(cross), run_time=.3)
        self.at("permanent label")
        pl = lab("a permanent label? No.", LG, 44, (0, -2.2))
        self.play(FadeIn(pl), run_time=.4)
        self.at("a state", lead=.4)
        track = RoundedRectangle(corner_radius=.9, width=4.4, height=1.8, stroke_color=YELLOW, stroke_width=6,
                                 fill_color=YELLOW, fill_opacity=.35).move_to([1.6, 1.3, 0])
        knob = Circle(radius=.72, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([2.7, 1.3, 0])
        axl = lab("axon", YELLOW, 52, (-2.0, 1.3), weight=BOLD)
        self.play(FadeOut(VGroup(imprint, cross, pl, tool)), FadeIn(track), FadeIn(knob), FadeIn(axl), FadeIn(nn.group), run_time=.6)
        tl = lab("axon length", LG, 28, (3.8, -1.55))
        self.at("the cell keeps")
        title = lab("axon = a state the cell keeps", GOLD, 44, (0, 3.3), font=TITLE_FONT)
        glow = Circle(radius=.95, color=TEXT, stroke_width=5).move_to(knob.get_center())
        self.play(FadeIn(title), Create(glow), run_time=.6)
        self.play(FadeOut(glow), run_time=.3)
        self.at("losing most", lead=.5)
        prox, cm = do_cut(self, nn, .07, drift=(1.2, -.5), shift_in=1.7)
        self.at("most of the")
        self.play(FadeIn(lab("most of the axon is gone", RED, 30, (2.6, -2.1))), run_time=.4)
        self.at("can reset")
        rs = lab("reset", TEXT, 52, (-2.0, 1.3), weight=BOLD)
        self.play(knob.animate.move_to([.5, 1.3, 0]).set_fill(GREY), track.animate.set_stroke(GREY).set_fill(GREY, opacity=.2),
                  ReplacementTransform(axl, rs), run_time=.6)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        c1 = RoundedRectangle(corner_radius=.3, width=6.2, height=4.8, stroke_color=GOLD, stroke_width=3).move_to([-3.4, 0, 0])
        c2 = c1.copy().move_to([3.4, 0, 0])

        def numeral(k, x):
            return VGroup(Circle(radius=.5, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                          T(str(k), 44, BG, weight=BOLD)).move_to([x, 1.5, 0])
        n1, n2 = numeral(1, -3.4), numeral(2, 3.4)
        head = T("That raises two questions", 40, GOLD, TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeIn(head), Create(c1), Create(c2), run_time=.8)
        self.at("two questions")
        self.play(FadeIn(n1, scale=1.4), FadeIn(n2, scale=1.4), run_time=.4)
        t1 = T("How is the\naxon won?", 46, TEXT, TITLE_FONT).move_to([-3.4, -.35, 0])
        self.at("questions", lead=-.35)
        self.play(Write(t1), run_time=1.0)
        self.at("and once", lead=.15)
        self.play(*fx(VGroup(c1, n1, t1), .45), FadeOut(head), run_time=.3)
        t2 = T("How is it\nheld?", 46, TEXT, TITLE_FONT).move_to([3.4, -.35, 0])
        self.play(Write(t2), run_time=.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 15-19: the map
# ---------------------------------------------------------------------------------------------
def dish_ellipse():
    return Ellipse(width=13.0, height=7.3, stroke_color=LG, stroke_width=3)


SC = 1.05
LENS0 = [2.1, 2.0, 2.0, 2.0, 2.0]
WIN = 4.0        # length (in units of SC) of the neurite that has pulled ahead


class S15(SpokenScene):
    def construct(self):
        dish = dish_ellipse()
        y = Young(sc=SC, lens=[2.0] * 5)
        dl = lab("cultured neuron, in a dish", LG, 30, (0, -3.15))
        nl = lab("five neurites,\nabout equal\nin length", TEXT, 32, (-3.9, 1.5))
        self.add(y.group)
        self.play(Create(dish), FadeIn(dl), run_time=1.0)
        self.at("a young neuron")
        self.play(FadeIn(nl), y.soma.animate.set_fill(SOMA_FILL, opacity=1), run_time=.2)
        self.at("pulls ahead")
        nl2 = lab("one pulls\nahead", YELLOW, 32, (-3.9, 1.5))
        self.play(y.tr[0].animate.set_value(2.1 * SC), FadeOut(nl), FadeIn(nl2), run_time=.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        dish = dish_ellipse()
        y = Young(sc=SC, lens=LENS0)
        self.add(dish, y.group)
        self.at("in the middle")
        self.play(Indicate(y.soma, color=TEXT, scale_factor=1.15), run_time=.6)
        self.at("cell body")
        cb = lab("cell body", TEXT, 32, (2.6, -0.5))
        ld = leader((1.45, -0.42), (0.8, -0.1), TEXT, 3)
        self.play(FadeIn(cb), Create(ld), run_time=.4)
        self.at("minor neurites")
        mn = lab("minor neurites", TEXT, 32, (-4.65, 0.55))
        ml = leader((-3.1, 0.5), (-2.35, 0.5), TEXT, 3)
        self.play(*[a for i in range(5) for a in y.recolor(i, NEURITE_COLS[i])], FadeIn(mn), Create(ml), run_time=.6)
        self.at("all alike")
        ring = DashedVMobject(Circle(radius=y.R + 2.05 * SC, color=TEXT, stroke_width=3).move_to(y.c), num_dashes=60)
        eq = lab("about equal\nlength", TEXT, 32, (4.9, -1.35))
        eql = leader((3.85, -1.2), (2.8, -1.05), TEXT, 3)
        note = lab("colours only\ntell them apart", LG, 26, (-4.5, -1.55))
        self.play(Create(ring), FadeIn(eq), Create(eql), FadeIn(note), run_time=.8)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        dish = dish_ellipse()
        y = Young(sc=SC, lens=LENS0, cols=NEURITE_COLS, cones=True)
        setf(y.fan_group, 0)
        self.add(dish, y.group)
        self.at("ends in")
        rings = VGroup(*[Circle(radius=.3, color=TEXT, stroke_width=3).move_to(y.tip(i)) for i in range(5)])
        self.play(Create(rings), run_time=.5)
        self.at("growth cone")
        self.play(FadeOut(rings), *fx(y.fan_group, 1), run_time=.5)
        gl = lab("growth cone", TEXT, 34, (4.8, 0.0))
        gll = Arrow([4.4, .35, 0], [3.45, 1.2, 0], buff=.1, color=TEXT, stroke_width=4, tip_length=.2)
        self.play(FadeIn(gl), GrowArrow(gll), run_time=.5)
        self.at("motile tip")
        mt = lab("the motile tip", LG, 30, (4.8, -0.65))
        self.play(FadeIn(mt), *[Wiggle(f, scale_value=1.1, rotation_angle=.05 * TAU) for f in y.fans], run_time=.9)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        dish = dish_ellipse()
        y = Young(sc=SC, lens=LENS0, cols=NEURITE_COLS, cones=True)
        self.add(dish, y.group)
        self.at("pulled ahead")
        self.play(y.tr[0].animate.set_value(WIN * SC), run_time=1.4)
        self.at("the axon")
        la = lab("the axon", YELLOW, 34, (4.65, -.35))
        lal = leader((4.35, .05), (3.55, 1.5), YELLOW, 3)
        self.play(*y.recolor(0, YELLOW), FadeIn(la), Create(lal), run_time=.5)
        self.at("the others")
        self.play(*[a for i in range(1, 5) for a in y.recolor(i, BLUE)], run_time=.6)
        self.at("become dendrites")
        ld = lab("future dendrites", BLUE, 34, (-4.0, -1.2))
        l1 = leader((-3.2, -0.9), (-2.0, 0.45), BLUE, 3)
        l2 = leader((-2.25, -1.3), (-1.2, -1.35), BLUE, 3)
        self.play(FadeIn(ld), Create(l1), Create(l2), run_time=.5)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        dish = dish_ellipse()
        cols = [YELLOW] + [BLUE] * 4
        y = Young(sc=SC, lens=[WIN] + [2.0] * 4, cols=cols, cones=True)
        self.add(dish, y.group)
        d = u(25)
        nrm = np.array([np.sin(np.radians(25)), -np.cos(np.radians(25)), 0.0])
        a, b = y.c + d * .9, y.c + d * 2.5
        self.at("few tens")
        br = Brace(Line(a, b), direction=nrm, color=LG, buff=.2)
        fl = lab("first few tens of\nmicrometres", TEXT, 30, (3.7, -1.7))
        fll = leader((2.9, -1.25), br.get_tip() + RIGHT * .1, LG, 3)
        self.play(GrowFromCenter(br), FadeIn(fl), Create(fll), run_time=.7)
        self.at("the proximal axon")
        pa = lab("proximal axon", YELLOW, 34, (4.6, -.65))
        pl = leader((3.15, -.4), (a + b)[:2] / 2 + np.array([.15, -.1]), YELLOW, 3)
        self.play(FadeIn(pa), Create(pl), run_time=.5)
        self.at("initial segment")
        isl = lab("future initial\nsegment", PURPLE, 32, (2.5, 2.65))
        ill = leader((2.1, 2.05), (a + b)[:2] / 2 + np.array([0.0, .12]), PURPLE, 3)
        self.play(br.animate.set_color(PURPLE), FadeIn(isl), Create(ill), run_time=.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 21-25: the idea to carry
# ---------------------------------------------------------------------------------------------
CARD_X = -3.95
ROW_H = [1.15, 1.45, 1.45]


def card_ys(k):
    gap = .5
    H = sum(ROW_H[:k]) + gap * (k - 1)
    y, ys = H / 2, []
    for i in range(k):
        ys.append(y - ROW_H[i] / 2)
        y -= ROW_H[i] + gap
    return ys, H + 1.1


def card_row(k, ys):
    y = ys[k - 1]
    if k == 1:
        return [T("An axon is won in a race,", 30, TEXT, TITLE_FONT).move_to([CARD_X, y + .28, 0]),
                T("then held.", 30, GOLD, TITLE_FONT).move_to([CARD_X, y - .28, 0])]
    if k == 2:
        return [T("The race: positive\nfeedback in each neurite\n+ competition", 26, TEXT, line_spacing=.8,
                  t2c={"positive": GREEN, "feedback": GREEN, "competition": RED}).move_to([CARD_X, y, 0])]
    return [T("The hold: microtubule\ntracks + a gate near\nthe start", 26, TEXT, line_spacing=.8,
              t2c={"microtubule": TEAL, "tracks": TEAL, "gate": PURPLE}).move_to([CARD_X, y, 0])]


class Card:
    """The idea card: rows are added one scene at a time, and the frame grows around them."""

    def __init__(self, k):
        self.k = k
        ys, h = card_ys(k)
        self.frame = RoundedRectangle(corner_radius=.3, width=5.7, height=h, stroke_color=GREY, stroke_width=2.5).move_to([CARD_X, 0, 0])
        self.rows = [card_row(i, ys) for i in range(1, k + 1)]

    def mobs(self):
        return [self.frame] + [m for r in self.rows for m in r]

    def grow(self):
        nk = self.k + 1
        ys, h = card_ys(nk)
        new_frame = RoundedRectangle(corner_radius=.3, width=5.7, height=h, stroke_color=GREY, stroke_width=2.5).move_to([CARD_X, 0, 0])
        anims = [Transform(self.frame, new_frame)]
        for i, r in enumerate(self.rows):
            for m, nm in zip(r, card_row(i + 1, ys)):
                anims.append(m.animate.move_to(nm.get_center()))
        nr = card_row(nk, ys)
        anims += [FadeIn(m) for m in nr]
        self.rows.append(nr)
        self.k = nk
        return anims


ZC = (2.7, -0.1)     # centre of the young neuron in the picture zone beside the card
ZS = .9


class S21(SpokenScene):
    def construct(self):
        card = Card(1)
        a, b = card.rows[0]
        y = Young(c=ZC, sc=ZS, lens=[2.3] * 5, cols=NEURITE_COLS, cones=True)
        setf(y.group, 0)
        self.add(y.group)
        self.play(FadeIn(card.frame), FadeIn(a), *fx(y.group, 1), run_time=.7)
        self.at("an axon is")
        self.wait(.3)
        self.at("won in a race")
        self.play(y.tr[0].animate.set_value(3.6 * ZS), run_time=.7)
        self.play(*y.recolor(0, YELLOW), *[x for i in range(1, 5) for x in y.recolor(i, BLUE)], run_time=.4)
        self.at("then held")
        self.play(FadeIn(b), Indicate(y.lines[0], color=TEXT, scale_factor=1.05), run_time=.6)
        self.finish()


def race_data():
    dt, S = 0.02, 20.0
    L = np.array([20., 15, 15, 15, 15])
    ts, lead, sib = [0.0], [20.0], [15.0]
    for i in range(int(48 / dt)):
        w = L ** 2
        L = L + dt * S * w / w.sum()
        ts.append((i + 1) * dt); lead.append(L[0]); sib.append(L[1])
    ts, lead, sib = np.array(ts), np.array(lead), np.array(sib)
    k = np.log(lead[-1] / 20.0) / 48.0
    plead, psib = 20 * np.exp(k * ts), 15 * np.exp(k * ts)
    return ts, lead, sib, plead, psib


class S22(SpokenScene):
    def construct(self):
        ts, lead, sib, plead, psib = race_data()
        X0, X1 = 1.05, 6.7
        YB, YT = -2.55, 2.65           # screen y of 10 and 1000 micrometres
        X = lambda t: X0 + t / 48.0 * (X1 - X0)
        Y = lambda v: YB + (np.log10(v) - 1.0) / 2.0 * (YT - YB)
        idx = np.unique(np.round(np.linspace(0, np.sqrt(len(ts) - 1), 220) ** 2).astype(int))

        def curve_pts(v):
            return [np.array([X(ts[i]), Y(v[i]), 0.0]) for i in idx]

        def live(v, col, tt, w=7):
            pts = curve_pts(v)
            times = ts[idx]
            m = VMobject().set_stroke(col, w).set_fill(opacity=0)

            def upd(mm):
                k = max(2, int(np.searchsorted(times, tt.get_value())) + 1)
                mm.set_points_as_corners(pts[:k])
            m.add_updater(upd, call_updater=True)
            return m, pts

        card = Card(1)
        self.add(*card.mobs())
        # axes, already ticked, with both starting values marked
        grid = VGroup()
        ticklabs = VGroup()
        for v in (10, 15, 20, 50, 100, 200, 500):
            col = YELLOW if v == 20 else (LG if v == 15 else GREY)
            ticklabs.add(T(str(v), 26, col).move_to([X0 - .1 - .22 * len(str(v)), Y(v), 0]))
            if v not in (10, 15, 20):
                grid.add(Line([X0, Y(v), 0], [X1, Y(v), 0], color=GREY, stroke_width=1.5).set_opacity(.35))
        ax = VGroup(Line([X0, YB, 0], [X1 + .1, YB, 0], color=LG, stroke_width=4),
                    Line([X0, YB, 0], [X0, YT, 0], color=LG, stroke_width=4))
        xt = VGroup(*[T(s, 26, GREY).move_to([X(t), YB - .38, 0]) for s, t in (("0", 0), ("24", 24), ("48", 48))])
        for t in (24, 48):
            ax.add(Line([X(t), YB, 0], [X(t), YB - .12, 0], color=LG, stroke_width=3))
        xl = lab("time (hours)", LG, 26, (X(24), -3.55))
        yl = lab("length (µm, log scale)", LG, 26, (-0.7, 0.0)).rotate(PI / 2)
        tag = lab("illustrative model, not data", GOLD, 28, (3.4, 3.72))
        d20, d15 = Dot([X0, Y(20), 0], radius=.1, color=YELLOW), Dot([X0, Y(15), 0], radius=.1, color=LG)
        lg1 = VGroup(Line([3.9, -1.2, 0], [4.45, -1.2, 0], color=YELLOW, stroke_width=7), T("leader", 28, YELLOW).next_to([4.55, -1.2, 0], RIGHT, buff=0))
        lg2 = VGroup(Line([3.9, -1.8, 0], [4.45, -1.8, 0], color=LG, stroke_width=7), T("four siblings", 28, LG).next_to([4.55, -1.8, 0], RIGHT, buff=0))
        self.play(*card.grow(), Create(ax), FadeIn(grid), FadeIn(ticklabs), FadeIn(xt), FadeIn(xl), FadeIn(yl),
                  FadeIn(d20), FadeIn(d15), FadeIn(lg1), FadeIn(lg2), FadeIn(tag), run_time=.9)
        # feedback alone: the lead compounds, the siblings are still rising
        self.at("positive feedback")
        ch1 = chip("positive feedback", GREEN, 28)
        ch1.move_to([0.25 + ch1.width / 2, 2.98, 0])
        self.play(FadeIn(ch1), run_time=.4)
        self.at("in each")
        tt = ValueTracker(0.0)
        cl, plp = live(lead, YELLOW, tt)
        cs, psp = live(sib, LG, tt)
        self.add(cs, cl)
        self.play(tt.animate.set_value(6.0), run_time=2.7, rate_func=linear)
        # competition arrives; only now do the siblings stall
        self.at("competition")
        ch2 = chip("competition", RED, 28)
        ch2.move_to([3.85 + ch2.width / 2, 2.98, 0])
        self.play(FadeIn(ch2, scale=1.1), run_time=.4)
        self.play(tt.animate.set_value(48.0), run_time=2.5, rate_func=rate_functions.ease_out_sine)
        self.at("decides the race")
        endp = np.array([X(48), Y(lead[-1]), 0])
        ring = Circle(radius=.24, color=YELLOW, stroke_width=5).move_to(endp)
        win = lab("winner", YELLOW, 32, (6.2, 1.75))
        self.play(Create(ring), FadeIn(win), run_time=.5)
        self.wait(.2)
        # proportional growth: no winner
        self.at("growth in simple", lead=.25)
        self.play(FadeOut(VGroup(cl, cs, ring, win, ch1, ch2)), run_time=.4)
        tt2 = ValueTracker(0.0)
        pl_, _ = live(plead, YELLOW, tt2)
        ps_, _ = live(psib, LG, tt2)
        rt = lab("ratio stays 1.33", YELLOW, 40, (X0 + .2 + 1.95, 2.15))
        rt2 = lab("leader : sibling", LG, 28, (X0 + .2 + 1.45, 1.55))
        self.add(ps_, pl_)
        logcue = lab("parallel lines = same ratio", TEXT, 28, (3.85, 2.98))
        self.play(FadeIn(rt), FadeIn(rt2), FadeIn(logcue), tt2.animate.set_value(48.0), run_time=1.4, rate_func=linear)
        pl_.update(0)
        ps_.update(0)
        self.at("picks no winner")
        nw = lab("no winner", TEXT, 36, (5.5, -0.35))
        self.play(FadeIn(nw), run_time=.5)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        card = Card(2)
        y = Young(c=ZC, sc=ZS, lens=[3.6, 2.3, 2.3, 2.3, 2.3], cols=[YELLOW] + [BLUE] * 4, cones=True)
        y.lines[0].set_stroke(width=26, opacity=.45)
        self.add(*card.mobs(), y.group)
        self.at("structures in the axon")
        self.play(*card.grow(), run_time=.6)
        d = u(25)
        nrm = np.array([-np.sin(np.radians(25)), np.cos(np.radians(25)), 0.0])
        self.at("microtubule tracks", lead=.3)
        st, en = y.c + d * (y.R + .35), y.c + d * (y.R + 3.6 * ZS - .3)
        trk = VGroup(*[Arrow(st + nrm * o, en + nrm * o, buff=0, color=TEAL, stroke_width=9, tip_length=.24,
                             max_tip_length_to_length_ratio=.25) for o in (-.17, 0, .17)])
        tl = lab("microtubule\ntracks", TEAL, 34, (4.9, -.65))
        tll = leader((4.5, -.15), y.c + d * 2.3 - nrm * .05, TEAL, 3)
        self.play(Create(trk), FadeIn(tl), Create(tll), run_time=.7)
        self.at("a gate", lead=.2)
        gate = Ellipse(width=.3, height=1.0, color=PURPLE, stroke_width=7, fill_color=PURPLE, fill_opacity=.3
                       ).rotate(np.radians(25)).move_to(y.c + d * (y.R + 1.0))
        gl = lab("a gate near\nthe start", PURPLE, 32, (5.4, 3.0))
        gll = leader((4.5, 2.55), gate.get_center() + UP * .4, PURPLE, 3)
        self.play(FadeIn(gate), FadeIn(gl), Create(gll), run_time=.2)
        self.finish()


def big_neuron(c, s=1.0, axon_len=8.0):
    return Neu(c=c, s=s, dends=[(60, 1.9), (125, 1.8), (190, 1.6), (245, 1.8)], axon_len=axon_len, wob=.06, axw=11)


class S24(SpokenScene):
    def construct(self):
        # part 1: loosen the hold
        n1 = big_neuron((-4.3, -.6), s=1.0, axon_len=9.4)
        coll = Ellipse(width=.34, height=1.0, color=PURPLE, stroke_width=7, fill_color=PURPLE, fill_opacity=.35
                       ).move_to(n1.pt(.09) + UP * 0)
        gl = lab("the gate holds the axon's features", PURPLE, 32, (0.3, 2.2))
        gll = leader((-1.5, 1.95), n1.pt(.09) + UP * .45, PURPLE, 3)
        self.play(FadeIn(n1.group), FadeIn(coll), FadeIn(gl), Create(gll), run_time=.5)
        self.at("loosen the hold", lead=.0)
        self.play(FadeOut(coll), FadeOut(gl), FadeOut(gll), run_time=.2)
        loose = lab("gate loosened", PURPLE, 36, (-1.0, 2.2))
        self.add(loose)
        self.at("lose features", lead=.65)
        patches = VGroup(*[Line(n1.pt(t0), n1.pt(t0 + .045), color=BLUE, stroke_width=24)
                           for t0 in (.045, .115, .185, .255, .325, .395, .465)])
        pl = lab("proximal axon loses features", BLUE, 36, (.2, -2.15))
        pll = leader((-0.6, -1.85), n1.pt(.18) + DOWN * .25, BLUE, 3)
        fa = lab("far axon: still gold", YELLOW, 34, (4.3, 0.9))
        self.add(pl, fa)
        self.play(FadeIn(patches), Create(pll), run_time=.25)
        self.at("cut almost", lead=.45)
        part1 = VGroup(n1.group, patches, pl, pll, fa, loose)
        # part 2: cut almost all, the race can reopen
        n2 = big_neuron((-4.3, -.6), s=1.0, axon_len=9.4)
        self.play(FadeOut(part1), FadeIn(n2.group), run_time=.4)
        self.at("cut almost all")
        prox, cm = do_cut(self, n2, .07, drift=(1.5, -.4), shift_in=2.4)
        cl = lab("almost all of the axon cut away", RED, 32, (1.2, -1.7))
        cll = leader((.2, -1.4), (-2.75, -.8), RED, 3)
        self.play(FadeIn(cl), Create(cll), run_time=.4)
        self.at("the race")
        p1, h = n2.trunk_end(0)
        pts = bend_pts(p1, 35, -10, 5.0)
        d = n2.dends[0]
        tr = ValueTracker(0.02)
        line = grow_line(pts, tr, YELLOW, 11)
        self.add(line)
        rr = lab("race can reopen", YELLOW, 42, (1.2, 1.2))
        self.play(d[0].animate.set_color(YELLOW), d[1].animate.set_color(YELLOW).set_opacity(.55), FadeIn(rr), FadeOut(VGroup(cl, cll)), run_time=.3)
        self.play(tr.animate.set_value(1.0), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        t1 = T("Won, then held.", 64, TEXT, TITLE_FONT).move_to([0, 2.95, 0])
        self.play(Write(t1), run_time=.9)
        self.at("but this race")
        dish = Ellipse(width=8.6, height=4.8, stroke_color=LG, stroke_width=3).move_to([0, -0.1, 0])
        self.play(Create(dish), run_time=.8)
        self.at("seen in a dish")
        y = Young(c=(0, -0.1), sc=.7, lens=[2.3] * 5, cols=NEURITE_COLS)
        self.play(FadeIn(y.group), run_time=.6)
        self.at("next we watch")
        t3 = T("Next: Five Stages and a Race", 42, GOLD, TITLE_FONT).move_to([0, -3.15, 0])
        self.play(FadeIn(t3), run_time=.6)
        self.at("watch it begin")
        self.play(y.tr[0].animate.set_value(2.3 * .7 + .5), run_time=.9)
        self.finish()


class S26End(EndCard):
    LINE = "An axon is won in a race, then held."
