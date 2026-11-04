"""Injury and regeneration, chapter 3: Drive Against Resistance  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, shared by every chapter of this film; taken from scenes.old.py)
  BLUE   = the neuron: cell body, axon, and its drive (the growth program)
  TEAL   = NMNAT2 (not used in this chapter)
  ORANGE = NMN (not used in this chapter)
  GREEN  = NAD+ and ATP (not used in this chapter)
  RED    = resistance from the tissue (central tissue tint, myelin inhibitors, scar lesion, crush site);
           SARM1 and the cut/destruction in chapter 2 (the SARM1 blocker chip here)
  YELLOW = calcium (not used in this chapter)
  PURPLE = calpain (not used in this chapter)
  GOLD   = growth cones, regrowth and "past the line" (what regrows)
  SAGE   = peripheral nerve graft, repair glia (Schwann cells and astrocytes)
  GREY   = labels, anatomy outlines, de-emphasized
"""
import numpy as np
from math import erf, sqrt, exp, pi, atan2
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAGE = "#9BB99B"


# ---------------------------------------------------------------------------------------------
# helpers (shared look with the other chapters)
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def tube(x0, x1, y, h=0.4, color=BLUE, op=0.3):
    return RoundedRectangle(corner_radius=h / 2, width=x1 - x0, height=h, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def beads(x0, x1, y, h=0.4, n=7, color=BLUE, op=0.3):
    pitch = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w, height=h * 0.9, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x0 + pitch * (i + 0.5), y + (0.05 if i % 2 else -0.05), 0]))
    return g


def soma_at(x, y, r=0.6):
    s = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    f = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([x, y, 0])
    n = Circle(radius=r * 0.36, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])
    return VGroup(s, f, n)


def cone(x=0.0, y=0.0, color=GOLD, s=1.0):
    # A broad, fingered growth tip; a schematic cell shape, not a molecule. Points to the right.
    p = Polygon([-0.45, -0.16, 0], [0.03, -0.37, 0], [0.48, -0.33, 0],
                [0.25, -0.10, 0], [0.58, 0, 0], [0.25, 0.10, 0],
                [0.48, 0.33, 0], [0.03, 0.37, 0], [-0.45, 0.16, 0],
                stroke_color=color, fill_color=color, fill_opacity=0.45, stroke_width=3)
    return p.scale(s).shift([x, y, 0])


def glia(x, y, w=0.85, h=0.4, color=SAGE):
    return Ellipse(width=w, height=h, color=color, fill_opacity=0.25, stroke_width=3).move_to([x, y, 0])


def inhib(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def xmark(center, size=0.3, color=TEXT, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def card_header(text):
    return T(text, 28, GREY).move_to([0, 3.3, 0])


def question_mark(x, y, size=72):
    return T("?", size, TEXT, weight=BOLD).move_to([x, y, 0])


def swap(scene, old, new, rt=0.4):
    scene.play(FadeOut(old), FadeIn(new), run_time=rt)


def ltext(text, size, color, y, xl=-6.7, font=FONT, **kw):
    m = T(text, size, color, **kw)
    return m.move_to([xl + m.width / 2, y, 0])


def rtext(text, size, color, y, xr=6.7, **kw):
    m = T(text, size, color, **kw)
    return m.move_to([xr - m.width / 2, y, 0])


def header(text):
    return ltext(text, 26, GREY, 3.5)


# ---------------------------------------------------------------------------------------------
# the graft world (scenes 2 to 6): an arch of peripheral nerve from the medulla to the spinal cord
# ---------------------------------------------------------------------------------------------
P0 = np.array([-5.2, -1.2, 0.0])
P1 = np.array([-5.2, 3.6, 0.0])
P2 = np.array([5.2, 3.6, 0.0])
P3 = np.array([5.2, -1.2, 0.0])
TAN = np.array([0.0, -1.0, 0.0])
EXT = 0.9
SPLIT = 0.9


def gbase(t):
    if t <= SPLIT:
        u = t / SPLIT
        return (1 - u) ** 3 * P0 + 3 * (1 - u) ** 2 * u * P1 + 3 * (1 - u) * u ** 2 * P2 + u ** 3 * P3
    return P3 + TAN * EXT * (t - SPLIT) / (1 - SPLIT)


def gdir(t):
    a, b = gbase(max(t - 0.01, 0)), gbase(min(t + 0.01, 1))
    d = b - a
    return d / np.linalg.norm(d)


def gpath(t, dy=0.0):
    p = gbase(t)
    if dy:
        d = gdir(t)
        p = p + np.array([-d[1], d[0], 0.0]) * dy
    return p


def gline(t0, t1, dy, color=BLUE, w=6, op=1.0):
    n = max(3, int(60 * abs(t1 - t0)) + 3)
    pts = [gpath(t0 + (t1 - t0) * i / (n - 1), dy) for i in range(n)]
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_stroke(color, width=w, opacity=op).set_fill(opacity=0)
    return m


def gcone(t, dy, s=0.42, back=False, color=GOLD):
    d = gdir(t)
    ang = atan2(d[1], d[0]) + (PI if back else 0)
    c = cone(0, 0, color=color, s=s)
    c.rotate(ang)
    c.move_to(gpath(t, dy) + d * (0.12 if not back else -0.12))
    return c


DYS = (-0.22, 0.0, 0.22)


def world_parts():
    med = RoundedRectangle(corner_radius=0.5, width=3.0, height=2.8, stroke_color=RED, stroke_width=3,
                           fill_color=RED, fill_opacity=0.12).move_to([-5.2, -1.9, 0])
    cord = RoundedRectangle(corner_radius=0.5, width=3.0, height=2.8, stroke_color=RED, stroke_width=3,
                            fill_color=RED, fill_opacity=0.12).move_to([5.2, -1.9, 0])
    pts = [gbase(i / 80 * SPLIT) for i in range(81)]
    bridge = VMobject()
    bridge.set_points_smoothly(pts)
    bridge.set_stroke(SAGE, width=70, opacity=0.4).set_fill(opacity=0)
    l_med = T("medulla", 26, GREY).move_to([-5.2, -3.0, 0])
    l_cord = T("spinal cord", 26, GREY).move_to([5.2, -3.0, 0])
    l_br = T("peripheral nerve", 28, SAGE).move_to([0, 1.15, 0])
    l_rat = ltext("adult rats", 26, GREY, 2.95)
    return dict(med=med, cord=cord, bridge=bridge, l_med=l_med, l_cord=l_cord, l_br=l_br, l_rat=l_rat)


WORLD_KEYS = ("med", "cord", "bridge", "l_med", "l_cord", "l_br", "l_rat")


def world_all():
    w = world_parts()
    return [w[k] for k in WORLD_KEYS]


def tips_wait():
    return [gline(0.0, 0.06, 0.0), gcone(0.06, 0.0, s=0.7), gline(0.93, 1.0, 0.0), gcone(0.93, 0.0, s=0.7, back=True)]


def gq_qs():
    return [question_mark(-6.0, 0.1), question_mark(6.0, 0.1)]


def gq_panelA():
    box = RoundedRectangle(corner_radius=0.2, width=3.3, height=3.3, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.07).move_to([-1.8, -0.85, 0])
    tt = T("central neurons\ncannot grow\nlong axons", 24, GREY, line_spacing=0.8).move_to([-1.8, -0.05, 0])
    stub = Line([-3.15, -1.85, 0], [-2.75, -1.85, 0], color=BLUE, stroke_width=6)
    cn = cone(-2.6, -1.85, s=0.4)
    q = T("?", 56, TEXT, weight=BOLD).move_to([-1.4, -1.8, 0])
    return VGroup(box, tt, stub, cn), q


def gq_panelB():
    box = RoundedRectangle(corner_radius=0.2, width=3.3, height=3.3, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.07).move_to([1.8, -0.85, 0])
    tt = T("tissue stops\nthem", 24, RED, line_spacing=0.8).move_to([1.8, -0.05, 0])
    ln = Line([0.4, -1.85, 0], [1.75, -1.85, 0], color=BLUE, stroke_width=6)
    cn = cone(1.95, -1.85, s=0.4)
    bar = Line([2.55, -2.2, 0], [2.55, -1.5, 0], color=RED, stroke_width=9)
    q = T("?", 56, TEXT, weight=BOLD).move_to([3.0, -1.8, 0])
    return VGroup(box, tt, ln, cn, bar), q


def gq_state():
    pa, qa = gq_panelA()
    pb, qb = gq_panelB()
    return world_all() + tips_wait() + gq_qs() + [pa, qa, pb, qb]


def bundle(tr, with_cones=True):
    mobs = []
    for dy in DYS:
        mobs.append(always_redraw(lambda dy=dy: gline(0.0, max(tr.get_value(), 0.01), dy)))
    if with_cones:
        for dy in DYS:
            mobs.append(always_redraw(lambda dy=dy: gcone(max(tr.get_value(), 0.01), dy, s=0.38)))
    return mobs


def measure():
    pts = [gpath(0.03 + (0.88 - 0.03) * i / 60, 0.62) for i in range(61)]
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_stroke(GOLD, width=5).set_fill(opacity=0)
    tips = []
    for ta, tb in ((pts[-1], pts[-6]), (pts[0], pts[5])):
        d = (ta - tb) / np.linalg.norm(ta - tb)
        n = np.array([-d[1], d[0], 0.0])
        tips.append(Polygon(ta + d * 0.05, ta - d * 0.25 + n * 0.14, ta - d * 0.25 - n * 0.14, stroke_width=0, fill_color=GOLD, fill_opacity=1))
    m = VGroup(m, *tips)
    lab = T("about 30 mm", 40, GOLD).move_to([0, 3.45, 0])
    return m, lab


def stop_parts():
    blunts = [Ellipse(width=0.26, height=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6)
              .move_to(gpath(0.97, dy) + np.array([0, -0.08, 0])) for dy in DYS]
    yb = gpath(0.97)[1] - 0.38
    bar = Line([4.75, yb, 0], [5.65, yb, 0], color=RED, stroke_width=9)
    lab = T("stop", 28, RED).move_to([6.2, yb, 0])
    return blunts, bar, lab


def gr_state():
    lines = [gline(0.0, 0.97, dy) for dy in DYS]
    blunts, bar, lab = stop_parts()
    arrow, ml = measure()
    return world_all() + lines + blunts + [bar, lab, arrow, ml]


# ---------------------------------------------------------------------------------------------
# the optic nerve world (scenes 7 to 10): a full-size layout, and a row layout for the comparison
# ---------------------------------------------------------------------------------------------
FULL = dict(ec=-4.4, er=2.4, rr=2.2, rgc=0.2, nx0=-2.0, nx1=6.8, nh=2.2, ys=[-0.6, -0.3, 0.0, 0.3, 0.6], cx=2.0,
            ch=2.4, cs=0.42, lw=4, pos=[-30, -15, 0, 15, 30])
ROW = dict(ec=-5.5, er=1.3, rr=1.2, rgc=0.11, nx0=-4.2, nx1=6.8, nh=1.5, ys=[-0.5, -0.25, 0.0, 0.25, 0.5], cx=1.4,
           ch=1.7, cs=0.3, lw=3, pos=[-30, -15, 0, 15, 30])
CROSS_IDX = (1, 3)


def optic(cfg, cy, dim=True, with_rgc=True):
    ec = np.array([cfg["ec"], cy, 0.0])
    eye = Circle(radius=cfg["er"], stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to(ec)
    retina = Arc(radius=cfg["rr"], start_angle=-0.8, angle=1.6, stroke_color=GREY, stroke_width=7).move_arc_center_to(ec)
    nerve = tube(cfg["nx0"], cfg["nx1"], cy, cfg["nh"], RED, 0.10)
    rgcs, axons = VGroup(), VGroup()
    for a, yy in zip(cfg["pos"], cfg["ys"]):
        pos = ec + cfg["rr"] * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        rgcs.add(Circle(radius=cfg["rgc"], stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6).move_to(pos))
        ln = VMobject()
        ln.set_points_as_corners([pos, [cfg["nx0"], cy + yy, 0], [cfg["cx"] - 0.15, cy + yy, 0]])
        ln.set_stroke(BLUE, width=cfg["lw"]).set_fill(opacity=0)
        axons.add(ln)
    dist = VGroup(*[Line([cfg["cx"] + 0.15, cy + yy, 0], [cfg["nx1"] - 0.5, cy + yy, 0], color=BLUE, stroke_width=cfg["lw"],
                         stroke_opacity=0.25 if dim else 1) for yy in cfg["ys"]])
    crush = RoundedRectangle(corner_radius=0.1, width=0.3 if cfg is FULL else 0.22, height=cfg["ch"], stroke_color=RED,
                             stroke_width=3, fill_color=RED, fill_opacity=0.55).move_to([cfg["cx"], cy, 0])
    cones = VGroup(*[cone(cfg["cx"] - 0.4, cy + yy, s=cfg["cs"]) for yy in cfg["ys"]])
    return dict(eye=eye, retina=retina, nerve=nerve, rgcs=rgcs, axons=axons, dist=dist, crush=crush, cones=cones)


def pten_chip():
    return bchip("PTEN", GREY, 30).move_to([-0.2, 2.4, 0])


def pten_x():
    return xmark([-1.5, 2.4, 0], 0.28, RED, 6)


def mtor_chip():
    return bchip("mTOR growth pathway", BLUE, 28).move_to([4.35, 2.4, 0])


def pten_bar(op=1.0):
    b = inhib([0.55, 2.4, 0], [1.95, 2.4, 0], GREY)
    b.set_stroke(opacity=op)
    return b


def optic_labels(on=True, ct=True, rgc=True, mouse=True):
    out = {}
    out["l_ct"] = T("central tissue", 28, RED).move_to([4.6, -1.75, 0])
    out["l_on"] = T("optic nerve", 28, GREY).move_to([0.4, -1.75, 0])
    out["l_rgc"] = T("retinal ganglion cells", 28, GREY).move_to([-4.6, -3.05, 0])
    out["leader"] = Line([-3.5, -2.75, 0], [-2.45, -0.75, 0], color=GREY, stroke_width=2.5)
    out["mouse"] = T("mouse eye", 28, GREY).move_to([-5.2, 0.0, 0])
    return out


def crush_state():
    """Final frame of scene 8, held through scene 9."""
    o = optic(FULL, 0.0)
    L = optic_labels()
    chip = pten_chip()
    cap = T("Will the axons cross?", 30, TEXT).move_to([2.2, -3.0, 0])
    gro = mtor_chip()
    return [o["eye"], o["retina"], o["nerve"], o["axons"], o["rgcs"], o["dist"], o["crush"], o["cones"],
            chip, pten_x(), pten_bar(0.25), gro, L["l_ct"], L["l_on"], L["l_rgc"], L["leader"], L["mouse"],
            question_mark(3.8, 0.0), cap], o


# ---------------------------------------------------------------------------------------------
# the threshold plot (scenes 12, 13, 16)
# ---------------------------------------------------------------------------------------------
PX0, PX1 = -5.9, 5.9
DMIN, DMAX = -4.2, 5.0
BASE = -2.3
SY = 11.5
LINE_H = 4.5


def X(d):
    return PX0 + (d - DMIN) * (PX1 - PX0) / (DMAX - DMIN)


def dens(d, mu, mix):
    d = np.asarray(d, float)
    n = np.exp(-(d - mu) ** 2 / 2) / sqrt(2 * pi)
    u = np.where((d >= -1.5 + mu) & (d <= 3.5 + mu), 0.2, 0.0)
    return (1 - mix) * n + mix * u


def mass(L, mu, mix):
    # Exact areas keep equal shifts of the line and the distribution identical.
    normal_tail = 0.5 * (1 - erf((L - mu) / sqrt(2)))
    uniform_tail = np.clip((3.5 + mu - L) / 5.0, 0.0, 1.0)
    return float((1 - mix) * normal_tail + mix * uniform_tail)


def fmt(v):
    return f"{100 * v:.1f}%"


class Thr:
    def __init__(self, mu=0.0, L=2.0, mix=0.0, vis=0.0, lvis=0.0, svis=0.0):
        self.mu, self.L, self.mix, self.vis = ValueTracker(mu), ValueTracker(L), ValueTracker(mix), ValueTracker(vis)
        self.lvis, self.svis = ValueTracker(lvis), ValueTracker(svis)
        self.ds = np.linspace(DMIN, DMAX, 280)
        self.fill = always_redraw(self._fill)
        self.outline = always_redraw(self._outline)
        self.sliver = always_redraw(self._sliver)
        self.line = always_redraw(self._line)
        self.line_label = always_redraw(self._line_label)
        self.readout = always_redraw(self._readout)

    def _pts(self, ds):
        y = BASE + SY * dens(ds, self.mu.get_value(), self.mix.get_value())
        return [np.array([X(d), yy, 0.0]) for d, yy in zip(ds, y)]

    def _fill(self):
        v = self.vis.get_value()
        pts = self._pts(self.ds)
        return Polygon(*([np.array([pts[0][0], BASE, 0])] + pts + [np.array([pts[-1][0], BASE, 0])]),
                       stroke_width=0, fill_color=BLUE, fill_opacity=0.28 * v)

    def _outline(self):
        v = self.vis.get_value()
        m = VMobject()
        m.set_points_as_corners(self._pts(self.ds))
        m.set_stroke(BLUE, width=4, opacity=v).set_fill(opacity=0)
        return m

    def _sliver(self):
        v = self.svis.get_value()
        L = min(self.L.get_value(), DMAX - 0.05)
        ds = np.linspace(L, DMAX, 120)
        pts = self._pts(ds)
        return Polygon(*([np.array([X(L), BASE, 0])] + pts + [np.array([pts[-1][0], BASE, 0])]),
                       stroke_width=0, fill_color=GOLD, fill_opacity=0.95 * v)

    def _line(self):
        v = self.lvis.get_value()
        x = X(self.L.get_value())
        return Line([x, BASE, 0], [x, BASE + LINE_H, 0], color=RED, stroke_width=7, stroke_opacity=v)

    def _line_label(self):
        v = self.lvis.get_value()
        x = X(self.L.get_value())
        return T("resistance", 26, RED).set_opacity(v).move_to([x, BASE + LINE_H + 0.4, 0])

    def _readout(self):
        v = mass(self.L.get_value(), self.mu.get_value(), self.mix.get_value())
        m = M("past the line: " + fmt(v), 30, GOLD)
        return m.move_to([-6.7 + m.width / 2, 3.55, 0])

    def mobs(self):
        return [self.fill, self.outline, self.sliver, self.line, self.line_label]


def plot_axes():
    ax = Arrow([-6.2, BASE, 0], [6.5, BASE, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
    ay = Arrow([-6.15, BASE, 0], [-6.15, 2.55, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
    yl = T("number of neurons", 26, GREY).rotate(PI / 2).move_to([-6.55, 0.1, 0])
    dl = T("drive", 28, BLUE).move_to([5.7, BASE - 0.5, 0])
    return ax, ay, yl, dl


def model_note(text="illustrative model, not data"):
    return rtext(text, 28, GREY, 3.55)


def thr_start(scene, mu=0.0, L=2.0, mix=0.0, hyp_text="hypothetical spread", note="illustrative model, not data"):
    t = Thr(mu, L, mix, 1, 1, 1)
    ax, ay, yl, dl = plot_axes()
    hyp = ltext(hyp_text, 28, BLUE, 3.0, xl=-5.75)
    nt = model_note(note)
    scene.add(*t.mobs(), ax, ay, yl, dl, hyp, nt, t.readout)
    return t, hyp, nt


def add_regrow_tag():
    tag = T("regrow", 28, GOLD).move_to([4.6, -0.9, 0])
    arr = Arrow([4.3, -1.2, 0], [X(2.6), BASE + 0.35, 0], buff=0.05, color=GOLD, stroke_width=4, tip_length=0.2)
    return tag, arr


# ---------------------------------------------------------------------------------------------
# the balance (scenes 11, 21)
# ---------------------------------------------------------------------------------------------
class Seesaw:
    L = 4.2

    def __init__(self, ang=12.0, red=1.0, blue=0.5, py=-0.1, vis=0.0):
        self.py = py
        self.a, self.r, self.b, self.vis = ValueTracker(ang), ValueTracker(red), ValueTracker(blue), ValueTracker(vis)
        self.fulcrum = always_redraw(self._fulcrum)
        self.beam = always_redraw(self._beam)
        self.rblock = always_redraw(lambda: self._block(-1, self.r.get_value(), RED))
        self.bblock = always_redraw(lambda: self._block(1, self.b.get_value(), BLUE))
        self.rlab = always_redraw(lambda: self._label(-1, "resistance", RED))
        self.blab = always_redraw(lambda: self._label(1, "drive", BLUE))

    def end(self, s):
        a = np.radians(self.a.get_value())
        return np.array([s * self.L * np.cos(a), self.py + s * self.L * np.sin(a), 0.0])

    def _fulcrum(self):
        v = self.vis.get_value()
        return Polygon([-0.9, self.py - 2.2, 0], [0.9, self.py - 2.2, 0], [0, self.py, 0], stroke_color=GREY,
                       stroke_width=3, stroke_opacity=v, fill_color=GREY, fill_opacity=0.25 * v)

    def _beam(self):
        v = self.vis.get_value()
        return Line(self.end(-1), self.end(1), color=TEXT, stroke_width=10, stroke_opacity=v)

    def _block(self, s, val, color):
        v = self.vis.get_value()
        size = 0.7 + 0.8 * val
        e = self.end(s)
        return RoundedRectangle(corner_radius=0.1, width=size * 1.3, height=size, stroke_color=color, stroke_width=3.5,
                                stroke_opacity=v, fill_color=color, fill_opacity=0.35 * v).move_to(e + UP * (size / 2 + 0.06))

    def _label(self, s, text, color):
        v = self.vis.get_value()
        return T(text, 32, color).set_opacity(v).move_to(self.end(s) + UP * 2.15)

    def mobs(self):
        return [self.fulcrum, self.beam, self.rblock, self.bblock, self.rlab, self.blab]


def gate_icon():
    posts = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.3, height=2.8, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=0.35).move_to([x, 0.2, 0]) for x in (-1.6, 1.6)])
    leaf = Rectangle(width=2.9, height=1.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([0, 0.4, 0])
    slats = VGroup(*[Line([-1.45, y, 0], [1.45, y, 0], color=GREY, stroke_width=4) for y in (0.0, 0.4, 0.8)])
    return VGroup(posts, leaf, slats).scale(1.75).move_to([0, 0.15, 0])


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Injury and Regeneration: Why the Brain Does Not Regrow"
    TITLE = "Drive Against Resistance"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.5)
        self.wait(2.2)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        soma = soma_at(-5.7, 0.0, 1.0)
        prox = tube(-4.7, -1.0, 0.0, 0.9)
        slab = RoundedRectangle(corner_radius=0.3, width=5.1, height=6.2, stroke_color=RED, stroke_width=3,
                                fill_color=RED, fill_opacity=0.12).move_to([4.15, 0.0, 0])
        l_att = T("attached piece", 30, BLUE).move_to([-3.4, -1.25, 0])
        self.add(soma, prox, slab)
        self.at("attached piece")
        self.play(FadeIn(l_att), run_time=0.4)
        tip = cone(-0.4, 0.0, s=1.5)
        longer = tube(-4.7, 0.5, 0.0, 0.9)
        self.at("can regrow")
        self.play(FadeIn(tip, scale=0.4), run_time=0.3)
        self.play(Transform(prox, longer), tip.animate.move_to([0.6, 0.0, 0]), run_time=1.0)
        self.at("stall")
        blunt = Ellipse(width=0.5, height=0.9, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([1.05, 0, 0])
        self.play(Transform(tip, blunt), run_time=0.4)
        q = question_mark(0.95, 1.5, 90)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        lab = T("brain and spinal cord", 32, RED).move_to([4.15, 2.3, 0])
        self.at("brain and spinal cord")
        self.play(FadeIn(lab), run_time=0.5)
        self.finish()


class S02Graft(SpokenScene):
    def construct(self):
        yr = M("1981", 58, TEXT).move_to([0, 1.2, 0])
        names = T("Samuel David and Albert Aguayo", 42, TEXT).move_to([0, 0.05, 0])
        what = T("changed mainly: the tissue", 38, SAGE).move_to([0, -1.1, 0])
        self.at("1981")
        self.play(FadeIn(yr, shift=UP * 0.15), run_time=0.5)
        self.at("samuel david")
        self.play(FadeIn(names, shift=UP * 0.15), run_time=0.6)
        self.at("changed mainly the tissue")
        self.play(FadeIn(what, shift=UP * 0.15), run_time=0.6)
        w = world_parts()
        head = header("David and Aguayo, 1981")
        self.at("in adult rats")
        self.play(FadeOut(yr), FadeOut(names), FadeOut(what), FadeIn(head),
                  FadeIn(w["med"]), FadeIn(w["cord"]), FadeIn(w["l_rat"]), run_time=0.7)
        self.at("bridged the medulla")
        self.play(AnimationGroup(Create(w["bridge"], run_time=2.0),
                                 FadeIn(w["l_med"], run_time=0.3),
                                 Succession(Wait(1.0), FadeIn(w["l_cord"], run_time=0.3))))
        self.at("peripheral nerve")
        self.play(FadeIn(w["l_br"]), run_time=0.4)
        self.finish()


class S03Gq(SpokenScene):
    def construct(self):
        head = header("David and Aguayo, 1981")
        self.add(head, *world_all())
        w = world_parts()
        lt, lc, rt, rc = tips_wait()
        qs = gq_qs()
        pa, qa = gq_panelA()
        pb, qb = gq_panelB()
        self.at("adult central neurons")
        self.play(FadeIn(lt), FadeIn(lc), FadeIn(rt), FadeIn(rc), run_time=0.6)
        self.at("cannot grow")
        self.play(FadeIn(pa, shift=UP * 0.15), run_time=0.6)
        self.at("nothing grows")
        self.play(FadeIn(qa, scale=0.6), FadeIn(qs[0], scale=0.6), run_time=0.5)
        self.at("if the tissue stops them")
        self.play(FadeIn(pb, shift=UP * 0.15), Indicate(w["med"], color=RED, scale_factor=1.04),
                  Indicate(w["cord"], color=RED, scale_factor=1.04), run_time=0.8)
        self.at("what should you see")
        self.play(FadeIn(qb, scale=0.6), FadeIn(qs[1], scale=0.6), run_time=0.5)
        self.finish()


class S04Pause(NarratedScene):
    def construct(self):
        self.add(header("David and Aguayo, 1981"), *gq_state())
        self.wait(self.narration_s)
        self.finish()


class S05Gr(SpokenScene):
    def construct(self):
        head = header("David and Aguayo, 1981")
        tips = tips_wait()
        qs = gq_qs()
        pa, qa = gq_panelA()
        pb, qb = gq_panelB()
        self.add(head, *world_all(), *tips, *qs, pa, qa, pb, qb)
        tr = ValueTracker(0.01)
        self.add(tr)
        self.at("central axons")
        self.play(*[FadeOut(m) for m in (*qs, pa, qa, pb, qb, *tips)], run_time=0.5)
        mobs = bundle(tr)
        self.add(*mobs)
        arrow, lab = measure()
        self.at("grew about")
        tr.add_updater(lambda m, dt: m.set_value(min(0.9, m.get_value() + dt * 0.4)))
        self.at("30 millimeters")
        self.play(FadeIn(arrow), FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        self.at("back in central tissue")
        tr.clear_updaters()
        self.play(tr.animate.set_value(0.97), run_time=1.0)
        blunts, bar, slab = stop_parts()
        self.at("they soon stopped")
        for c in mobs[3:]:
            self.remove(c)
        self.play(*[FadeIn(b) for b in blunts], FadeIn(bar), FadeIn(slab), Indicate(bar, color=RED, scale_factor=1.2), run_time=0.7)
        self.finish()


class S06Beat(NarratedScene):
    def construct(self):
        self.add(header("David and Aguayo, 1981"), *gr_state())
        self.wait(self.narration_s)
        self.finish()


def optic_add(scene, o):
    scene.add(o["eye"], o["retina"], o["nerve"], o["dist"])


class S07Pten(SpokenScene):
    def construct(self):
        o = optic(FULL, 0.0, dim=False)
        L = optic_labels()
        self.add(o["eye"], o["retina"], o["nerve"], o["dist"])
        self.at("keep the central tissue")
        self.play(Indicate(o["nerve"], color=RED, scale_factor=1.02), FadeIn(L["l_ct"]), run_time=0.9)
        self.at("change mainly the neuron")
        self.play(FadeIn(o["rgcs"]), FadeIn(o["axons"]), run_time=0.6)
        self.play(Indicate(o["rgcs"], color=BLUE, scale_factor=1.3), run_time=0.8)
        head = header("He laboratory, 2008")
        self.at("in 2008")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        chip = pten_chip()
        self.at("deleted", lead=-0.6)
        self.play(FadeIn(chip), run_time=0.4)
        cross = pten_x()
        self.at("from retinal", lead=0.0)
        self.play(Create(cross), run_time=0.4)
        self.at("retinal ganglion cells")
        self.play(FadeIn(L["l_rgc"]), Create(L["leader"]), Indicate(o["rgcs"], color=BLUE, scale_factor=1.3), run_time=0.7)
        self.at("in mice")
        self.play(FadeIn(L["mouse"]), run_time=0.4)
        self.finish()


class S08Pten2(SpokenScene):
    def construct(self):
        o = optic(FULL, 0.0, dim=False)
        L = optic_labels()
        head = header("He laboratory, 2008")
        chip = pten_chip()
        cross = pten_x()
        self.add(o["eye"], o["retina"], o["nerve"], o["dist"], o["rgcs"], o["axons"], head, chip, cross,
                 L["l_ct"], L["l_rgc"], L["leader"], L["mouse"])
        gro = mtor_chip()
        bar = pten_bar()
        self.at("is a")
        self.play(FadeOut(cross), run_time=0.3)
        self.play(FadeIn(gro), Create(bar), run_time=0.7)
        dim = optic(FULL, 0.0, dim=True)["dist"]
        self.at("then they crush")
        self.play(FadeIn(o["crush"], scale=1.6), Transform(o["dist"], dim), FadeIn(cross), bar.animate.set_stroke(opacity=0.25), run_time=0.6)
        self.at("the optic nerve")
        self.play(FadeIn(L["l_on"]), run_time=0.4)
        self.at("which is central tissue")
        self.play(Indicate(o["nerve"], color=RED, scale_factor=1.02), Indicate(L["l_ct"], color=RED), run_time=0.7)
        cones = o["cones"]
        q = question_mark(3.8, 0.0)
        cap = T("Will the axons cross?", 30, TEXT).move_to([2.2, -3.0, 0])
        self.at("will the axons cross")
        self.play(FadeIn(cones, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(q, scale=0.6), FadeIn(cap), run_time=0.4)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        mobs, o = crush_state()
        self.add(header("He laboratory, 2008"), *mobs)
        self.wait(self.narration_s)
        self.finish()


class S10Pr(SpokenScene):
    def construct(self):
        head = header("He laboratory, 2008")
        mobs, o = crush_state()
        self.add(head, *mobs)
        r1 = optic(ROW, 1.55)
        r2 = optic(ROW, -1.55)
        # row 1 is the PTEN nerve (shrunk from the full layout), row 2 the control
        others = [m for m in mobs if all(m is not o[k] for k in o)]
        t1 = T("PTEN\ndeleted", 26, BLUE, line_spacing=0.8).move_to([-5.75, 1.55, 0])
        t2 = T("normal\nnerve", 26, GREY, line_spacing=0.8).move_to([-5.75, -1.55, 0])
        self.at("some do")
        anims = [ReplacementTransform(o[k], r1[k]) for k in o] + [FadeOut(m) for m in others]
        self.play(*anims, run_time=0.9)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(r2["eye"]), FadeIn(r2["retina"]), FadeIn(r2["nerve"]), FadeIn(r2["axons"]),
                  FadeIn(r2["rgcs"]), FadeIn(r2["dist"]), FadeIn(r2["crush"]), FadeIn(r2["cones"]), run_time=0.6)
        lines, cones = [], []
        for i in CROSS_IDX:
            yy = 1.55 + ROW["ys"][i]
            lines.append(Line([ROW["cx"] + 0.15, yy, 0], [ROW["cx"] + 2.8, yy, 0], color=BLUE, stroke_width=4))
            cones.append(r1["cones"][i])
        self.at("they come from")
        anims = []
        for ln, cn in zip(lines, cones):
            anims += [GrowFromEdge(ln, LEFT), cn.animate.shift(RIGHT * 2.9)]
        self.play(*anims, run_time=1.2)
        self.at("a minority of the neurons")
        rg = VGroup(r1["rgcs"][1], r1["rgcs"][3])
        self.play(Indicate(rg, color=GOLD, scale_factor=2.0), run_time=0.9)
        self.at("far more than normal")
        yy = -1.55 + ROW["ys"][1]
        stub = Line([ROW["cx"] + 0.15, yy, 0], [ROW["cx"] + 0.75, yy, 0], color=BLUE, stroke_width=4, stroke_opacity=0.9)
        self.play(FadeIn(stub), Indicate(VGroup(*lines), color=GOLD, scale_factor=1.0), run_time=0.8)
        self.finish()


class S11Bal(SpokenScene):
    def construct(self):
        gate = gate_icon()
        cross = Cross(stroke_color=RED, stroke_width=10).scale(2.3).move_to(gate)
        lab_g = T("a gate that must open first", 30, GREY).move_to([0, -3.35, 0])
        self.add(gate, lab_g)
        self.at("gate")
        self.play(Create(cross), run_time=0.5)
        ss = Seesaw(12, 1.0, 0.5)
        self.at("each experiment")
        self.play(FadeOut(gate), FadeOut(cross), FadeOut(lab_g), run_time=0.4)
        self.add(*ss.mobs())
        self.play(ss.vis.animate.set_value(1), run_time=0.6)
        lab1 = T("graft: the tissue changed", 32, SAGE).move_to([0, -3.35, 0])
        self.at("got growth")
        self.play(FadeIn(lab1), ss.r.animate.set_value(0.3), ss.a.animate.set_value(-8), run_time=0.9)
        self.at("changing mainly")
        self.play(FadeOut(lab1), ss.r.animate.set_value(1.0), ss.a.animate.set_value(12), run_time=0.5)
        lab2 = T("PTEN deleted: the neuron changed", 32, BLUE).move_to([0, -3.35, 0])
        self.at("one side")
        self.play(FadeIn(lab2), ss.b.animate.set_value(1.0), ss.a.animate.set_value(-8), run_time=0.9)
        self.at("a balance")
        self.play(FadeOut(lab2), ss.r.animate.set_value(0.8), ss.b.animate.set_value(0.8), ss.a.animate.set_value(0), run_time=0.8)
        self.finish()


class S12Thr(SpokenScene):
    def construct(self):
        t = Thr()
        ax, ay, yl, dl = plot_axes()
        hyp = ltext("hypothetical spread", 28, BLUE, 3.0, xl=-5.75)
        nt = model_note()
        self.add(*t.mobs(), ax, ay, yl, nt)
        self.at("neurons spread out")
        self.play(FadeIn(ax), t.vis.animate.set_value(1), FadeIn(hyp), run_time=1.0)
        self.at("by drive")
        self.play(FadeIn(dl), run_time=0.4)
        self.at("a line set by the tissue")
        self.play(t.lvis.animate.set_value(1), run_time=0.8)
        tag, arr = add_regrow_tag()
        self.at("only neurons past")
        self.add(t.readout)
        self.play(t.svis.animate.set_value(1), run_time=0.6)
        self.at("regrow")
        self.play(FadeIn(tag), GrowArrow(arr), run_time=0.5)
        self.finish()


class S13Thr2(SpokenScene):
    def construct(self):
        t, hyp, nt = thr_start(self)
        SX = -5.75
        v0, v1, v2, v3 = mass(2.0, 0, 0), mass(1.5, 0, 0), mass(2.0, 0.5, 0), mass(1.5, 0.5, 0)
        lab_a = ltext("lower the line", 30, RED, 2.4, xl=SX)
        self.at("lower the line")
        # Settle before the first sampled hold: both single changes read 6.7%.
        self.play(FadeIn(lab_a), t.L.animate.set_value(1.5), run_time=0.4)
        lab_b = ltext("push the neurons up", 30, BLUE, 2.4, xl=SX)
        self.at("push the neurons up")
        self.play(FadeOut(lab_a), t.L.animate.set_value(2.0), run_time=0.3)
        self.play(FadeIn(lab_b), t.mu.animate.set_value(0.5), run_time=0.6)
        self.at("some get through")
        self.play(Indicate(t.sliver, color=GOLD, scale_factor=1.0), run_time=0.8)
        self.at("the line sits")
        self.play(FadeOut(lab_b), t.mu.animate.set_value(0.0), run_time=0.7)
        tail = T("thin tail", 28, GREY).move_to([4.6, -1.0, 0])
        tail_arr = Arrow([4.3, -1.3, 0], [X(3.0), BASE + 0.2, 0], buff=0.05, color=GREY, stroke_width=4, tip_length=0.2)
        self.at("thin tail")
        self.play(FadeIn(tail), GrowArrow(tail_arr), run_time=0.5)
        lab_c = ltext("do both", 30, GOLD, 2.4, xl=SX)
        self.at("doing both")
        self.play(FadeOut(tail), FadeOut(tail_arr), FadeIn(lab_c), t.L.animate.set_value(1.5), t.mu.animate.set_value(0.5), run_time=1.0)
        g1, g2, gb = 100 * (v1 - v0), 100 * (v2 - v0), 100 * (v3 - v0)
        eq = M(f"+{g1:.1f} and +{g2:.1f} = +{g1 + g2:.1f}, but both: +{gb:.1f}", 28, TEXT).move_to([0, -3.35, 0])
        self.at("more than the two gains added")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.6)
        hyp2 = ltext("another spread", 28, BLUE, 3.0, xl=-5.75)
        self.at("with another spread")
        self.play(FadeOut(eq), FadeOut(lab_c), FadeOut(hyp), FadeIn(hyp2), t.mix.animate.set_value(1.0),
                  t.mu.animate.set_value(0.0), t.L.animate.set_value(2.0), run_time=1.2)
        u0, u1, u2, u3 = mass(2.0, 0, 1), mass(1.5, 0, 1), mass(2.0, 0.5, 1), mass(1.5, 0.5, 1)
        h1, h2, hb = 100 * (u1 - u0), 100 * (u2 - u0), 100 * (u3 - u0)
        eq2 = M(f"+{h1:.0f} and +{h2:.0f} = +{h1 + h2:.0f}, both: +{hb:.0f}", 28, TEXT).move_to([0, -3.35, 0])
        self.at("gains might only add")
        self.play(t.L.animate.set_value(1.5), t.mu.animate.set_value(0.5), run_time=1.0)
        self.play(FadeIn(eq2, shift=UP * 0.1), run_time=0.5)
        self.at("this is a model")
        self.play(Indicate(nt, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


def myq_parts():
    ax = tube(-6.8, -0.1, 0.3, 0.9)
    block = RoundedRectangle(corner_radius=0.3, width=5.7, height=5.6, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.16).move_to([3.85, 0.3, 0])
    ys = (1.6, 0.3, -1.0)
    tabs = [RoundedRectangle(corner_radius=0.1, width=0.4, height=0.8, stroke_color=RED, stroke_width=3,
                             fill_color=RED, fill_opacity=0.6).move_to([1.3, y, 0]) for y in ys]
    chips = [bchip(n, RED, 30).move_to([2.55 + 0.0, y, 0]) for n, y in zip(("Nogo", "MAG", "OMgp"), ys)]
    for c in chips:
        c.shift(RIGHT * (c.width / 2 - 0.55 + 0.0))
    crosses = [xmark([1.3, y, 0], 0.3, TEXT, 6) for y in ys]
    l_my = T("myelin", 36, GREY).move_to([5.0, 2.45, 0])
    return ax, block, tabs, chips, crosses, l_my


def myq_blunt():
    return Ellipse(width=0.5, height=0.9, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0.0, 0.3, 0])


class S14Myq(SpokenScene):
    def construct(self):
        ax, block, tabs, chips, crosses, l_my = myq_parts()
        gc = cone(-0.2, 0.3, s=1.5)
        self.add(ax, gc)
        self.at("myelin proteins")
        self.play(FadeIn(block), FadeIn(l_my), run_time=0.5)
        self.at("such as")
        self.play(*[FadeIn(tb, shift=LEFT * 0.2) for tb in tabs], *[FadeIn(c) for c in chips], run_time=0.7)
        self.at("collapse growth cones")
        self.play(Transform(gc, myq_blunt()), run_time=0.8)
        self.at("mice lacking three")
        for cr in crosses:
            self.play(Create(cr), run_time=0.3)
        self.at("barely regrow more")
        self.play(Indicate(ax, color=BLUE, scale_factor=1.0), run_time=0.8)
        q = question_mark(0.0, 1.6, 90)
        why = T("Why?", 48, TEXT).move_to([-3.4, 1.9, 0])
        self.at("why")
        self.play(FadeIn(q, scale=0.6), FadeIn(why), run_time=0.5)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        ax, block, tabs, chips, crosses, l_my = myq_parts()
        self.add(ax, myq_blunt(), block, l_my, *tabs, *chips, *crosses, question_mark(0.0, 1.6, 90),
                 T("Why?", 48, TEXT).move_to([-3.4, 1.9, 0]))
        self.wait(self.narration_s)
        self.finish()


class TailInset:
    """A magnified view of the far tail of the spread, so a tiny sliver is visible."""
    X0, X1, Y0, Y1 = 3.3, 6.5, 0.95, 3.0
    D0, D1 = 1.2, 3.6
    ISC = 55.0

    def __init__(self, t):
        self.t = t
        self.box = Rectangle(width=self.X1 - self.X0, height=self.Y1 - self.Y0, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.06).move_to([(self.X0 + self.X1) / 2, (self.Y0 + self.Y1) / 2, 0])
        self.label = T("tail, magnified", 26, GREY).move_to([(self.X0 + self.X1) / 2, 0.6, 0])
        self.curve = always_redraw(self._curve)
        self.sliver = always_redraw(self._sliver)
        self.line = always_redraw(self._line)

    def ix(self, d):
        return self.X0 + 0.1 + (d - self.D0) / (self.D1 - self.D0) * (self.X1 - self.X0 - 0.2)

    def _y(self, d):
        v = dens(d, self.t.mu.get_value(), self.t.mix.get_value())
        return np.minimum(self.Y0 + self.ISC * v, self.Y1 - 0.05)

    def _curve(self):
        ds = np.linspace(self.D0, self.D1, 80)
        m = VMobject()
        m.set_points_as_corners([np.array([self.ix(d), y, 0]) for d, y in zip(ds, self._y(ds))])
        m.set_stroke(BLUE, width=4).set_fill(opacity=0)
        return m

    def _sliver(self):
        L = min(max(self.t.L.get_value(), self.D0), self.D1 - 0.05)
        ds = np.linspace(L, self.D1, 60)
        pts = [np.array([self.ix(d), y, 0]) for d, y in zip(ds, self._y(ds))]
        return Polygon(*([np.array([self.ix(L), self.Y0, 0])] + pts + [np.array([self.ix(self.D1), self.Y0, 0])]),
                       stroke_width=0, fill_color=GOLD, fill_opacity=0.95)

    def _line(self):
        x = self.ix(min(max(self.t.L.get_value(), self.D0), self.D1))
        return Line([x, self.Y0, 0], [x, self.Y1, 0], color=RED, stroke_width=6)


class S16Myr(SpokenScene):
    def construct(self):
        t, hyp, nt = thr_start(self, note="one possible explanation, not data")
        ins = TailInset(t)
        self.at("one way to see it")
        self.play(Indicate(nt, color=GOLD, scale_factor=1.03), run_time=0.6)
        self.at("most neurons may sit")
        self.add(ins.box, ins.curve, ins.sliver, ins.line, ins.label)
        self.play(t.mu.animate.set_value(-1.0), FadeIn(ins.box), FadeIn(ins.label), run_time=1.1)
        self.at("far below the line")
        self.play(Indicate(t.line, color=RED, scale_factor=1.0), run_time=0.8)
        self.at("lowering it a little")
        self.play(t.L.animate.set_value(1.6), run_time=0.8)
        self.at("moves few across")
        self.play(Indicate(ins.sliver, color=GOLD, scale_factor=1.15), run_time=0.8)
        bricks = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.35, height=0.8, stroke_color=RED, stroke_width=5,
                                           fill_color=RED, fill_opacity=0.8).move_to([x, -3.25, 0]) for x in (-4.8, -3.25, -1.7)])
        l_ob = ltext("Other barriers still block growth", 30, TEXT, -3.25, xl=-0.5)
        self.at("other barriers remain")
        self.play(FadeIn(bricks, shift=DOWN * 0.2), FadeIn(l_ob), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scar, recovery, fixes, take-home
# ---------------------------------------------------------------------------------------------
SC_Y = 0.2


def scar_panel(cx, ring=True):
    lesion = Circle(radius=1.4, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.22).move_to([cx, SC_Y, 0])
    rg = VGroup()
    n = 12
    for k in range(n):
        a = k * TAU / n
        e = glia(cx + 1.9 * np.cos(a), SC_Y + 1.9 * np.sin(a), w=0.95, h=0.42).rotate(a + PI / 2)
        rg.add(e)
    ys = [SC_Y - 0.5, SC_Y, SC_Y + 0.5]
    stubs = VGroup(*[Line([cx - 3.0, y, 0], [cx - 2.65, y, 0], color=BLUE, stroke_width=5) for y in ys])
    cones = VGroup(*[cone(cx - 2.55, y, s=0.4) for y in ys])
    return dict(lesion=lesion, ring=rg, stubs=stubs, cones=cones, ys=ys)


class S17Scar(SpokenScene):
    def construct(self):
        P = scar_panel(0.0)
        self.add(P["stubs"], P["cones"])
        l_scar = T("scar", 32, RED).move_to([0, -2.6, 0])
        self.at("the scar resists")
        bars = VGroup(*[inhib([-2.3, y, 0], [-1.6, y, 0], RED, 5) for y in P["ys"]])
        self.play(FadeIn(P["lesion"]), FadeIn(l_scar), Create(bars), run_time=0.5)
        l_ast = T("astrocyte border", 30, SAGE).move_to([0, 2.95, 0])
        self.at("but also helps")
        self.play(FadeIn(P["ring"], scale=0.9), FadeIn(l_ast), run_time=0.8)
        mice = T("in mice", 28, GREY).move_to([0, 3.55, 0])
        self.at("in mice")
        self.play(FadeIn(mice), run_time=0.4)
        Q = scar_panel(3.3)
        grp = VGroup(P["lesion"], P["ring"], P["stubs"], P["cones"])
        l_in = T("border intact", 30, SAGE).move_to([-3.3, 3.3, 0])
        l_out = T("border removed", 30, GREY).move_to([3.3, 3.3, 0])
        l_st1 = T("stimulated axons (in mice)", 26, GREY).move_to([-3.3, 2.75, 0])
        l_st2 = T("stimulated axons (in mice)", 26, GREY).move_to([3.3, 2.75, 0])
        self.at("removing its astrocyte border")
        self.play(FadeOut(bars), FadeOut(l_scar), FadeOut(l_ast), FadeOut(mice), grp.animate.shift(LEFT * 3.3),
                  FadeIn(Q["lesion"]), FadeIn(Q["stubs"]), FadeIn(Q["cones"]), FadeIn(l_in), FadeIn(l_out),
                  FadeIn(l_st1), FadeIn(l_st2), run_time=1.0)
        # same starting place on both sides; the intact side reaches the scar, the removed side stops sooner
        ys = P["ys"]
        cxl, cxr = -3.3, 3.3
        l1 = [Line([cxl - 2.65, y, 0], [cxl - 0.85, y, 0], color=BLUE, stroke_width=5) for y in ys]
        l2 = [Line([cxr - 2.65, y, 0], [cxr - 1.75, y, 0], color=BLUE, stroke_width=5) for y in ys]
        res1 = T("more regrowth", 28, GOLD).move_to([cxl, -2.55, 0])
        res2 = T("less regrowth", 28, GREY).move_to([cxr, -2.55, 0])
        self.at("reduced stimulated regrowth")
        anims = []
        for ln in l1:
            anims.append(GrowFromEdge(ln, LEFT))
        for c in P["cones"]:
            anims.append(c.animate.shift(RIGHT * 1.8))
        for ln in l2:
            anims.append(GrowFromEdge(ln, LEFT))
        for c in Q["cones"]:
            anims.append(c.animate.shift(RIGHT * 0.9))
        # Both advance together; the removed-border tips visibly halt before the lesion.
        self.play(*anims, run_time=0.9)
        stops = VGroup(*[Line([cxr - 1.42, y - 0.22, 0], [cxr - 1.42, y + 0.22, 0],
                             color=RED, stroke_width=6) for y in ys])
        self.play(Create(stops), FadeIn(res1), FadeIn(res2), run_time=0.3)
        rule = T("Change the scar, do not remove it", 36, SAGE).move_to([0, -3.4, 0])
        self.at("change the scar")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.finish()


RX0, RX1 = -4.8, 4.8
AXY = 0.95
RULE_Y = 0.0
REP_Y = -1.95
Q_MIN = 0.35


def ruler_parts():
    cord = RoundedRectangle(corner_radius=0.3, width=1.5, height=4.6, stroke_color=RED, stroke_width=3,
                            fill_color=RED, fill_opacity=0.12).move_to([-6.0, 0.0, 0])
    target = RoundedRectangle(corner_radius=0.3, width=1.5, height=4.6, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.18).move_to([6.0, 0.0, 0])
    rule = Rectangle(width=RX1 - RX0, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.12).move_to([0, RULE_Y, 0])
    ticks = VGroup(*[Line([RX0 + i * (RX1 - RX0) / 10, RULE_Y - 0.25, 0], [RX0 + i * (RX1 - RX0) / 10, RULE_Y - 0.25 - (0.35 if i % 5 == 0 else 0.2), 0],
                          color=GREY, stroke_width=3) for i in range(0, 11)])
    tl = VGroup(M("0", 26, TEXT).move_to([RX0, -0.95, 0]), M("0.5 m", 26, TEXT).move_to([0, -0.95, 0]),
                M("1 m", 26, TEXT).move_to([RX1, -0.95, 0]))
    l_cord = T("spinal\ncord", 26, GREY, line_spacing=0.8).move_to([-6.0, 0.0, 0])
    l_toe = T("toe", 26, GREY).move_to([6.0, 2.65, 0])
    l_tgt = T("distant\ntarget", 26, GREY, line_spacing=0.8).move_to([6.0, 0.0, 0])
    return dict(cord=cord, target=target, rule=rule, ticks=ticks, tl=tl, l_cord=l_cord, l_toe=l_toe, l_tgt=l_tgt)


def day_label(p):
    return M("day " + f"{int(round(1000 * p)):,}", 30, TEXT).move_to([min(max(RX0 + (RX1 - RX0) * p, -3.9), 3.9), 2.0, 0])


def ruler_state():
    R = ruler_parts()
    mobs = [R["cord"], R["target"], R["rule"], R["ticks"], R["tl"], R["l_cord"], R["l_toe"], R["l_tgt"]]
    mobs.append(Line([RX0, AXY, 0], [RX1, AXY, 0], color=BLUE, stroke_width=14))
    mobs.append(cone(RX1 - 0.25, AXY, s=1.1))
    mobs.append(M("1 mm a day", 42, GOLD).move_to([0, 3.3, 0]))
    bar = Rectangle(width=RX1 - RX0, height=0.6, stroke_color=SAGE, stroke_width=3, stroke_opacity=Q_MIN + 0.05,
                    fill_color=SAGE, fill_opacity=0.8 * Q_MIN).move_to([0, REP_Y, 0])
    mobs.append(bar)
    mobs.append(T("Schwann cell repair support", 28, SAGE).move_to([0, REP_Y - 0.65, 0]))
    mobs.append(M("about 1,000 days, nearly 3 years", 34, TEXT).move_to([0, -3.4, 0]))
    mobs.append(day_label(1.0))
    return mobs


class S18Rec(SpokenScene):
    def construct(self):
        R = ruler_parts()
        p = ValueTracker(0.0)
        q = ValueTracker(1.0)
        self.add(p, q)
        self.at("regrowth is not recovery")
        self.play(FadeIn(R["cord"]), FadeIn(R["target"]), FadeIn(R["rule"]), FadeIn(R["ticks"]), FadeIn(R["tl"]),
                  FadeIn(R["l_cord"]), FadeIn(R["l_toe"]), run_time=0.9)
        axon_line = always_redraw(lambda: Line([RX0, AXY, 0], [RX0 + (RX1 - RX0) * max(p.get_value(), 0.003), AXY, 0],
                                               color=BLUE, stroke_width=14))
        axon_cone = always_redraw(lambda: cone(RX0 + (RX1 - RX0) * p.get_value() - 0.25, AXY, s=1.1))
        rate = M("1 mm a day", 42, GOLD).move_to([0, 3.3, 0])
        self.at("at a steady millimeter a day")
        self.add(axon_line, axon_cone)
        self.play(FadeIn(rate, shift=UP * 0.1), run_time=0.6)
        counter = always_redraw(lambda: day_label(p.get_value()))
        dur = self.t_of("nearly three years") - self.t_of("a meter takes")
        self.at("a meter takes")
        self.add(counter)
        p.add_updater(lambda m, dt: m.set_value(min(1.0, m.get_value() + dt / dur)))
        res = M("about 1,000 days, nearly 3 years", 34, TEXT).move_to([0, -3.4, 0])
        self.at("nearly three years", lead=-0.1)
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.6)
        bar = Rectangle(width=RX1 - RX0, height=0.6, stroke_color=SAGE, stroke_width=3, fill_color=SAGE,
                        fill_opacity=0.8).move_to([0, REP_Y, 0])
        bar.add_updater(lambda m: m.set_stroke(SAGE, opacity=max(q.get_value(), Q_MIN + 0.05))
                        .set_fill(SAGE, opacity=0.8 * q.get_value()))
        self.at("over that long a time")
        self.add(bar)
        self.play(FadeIn(bar), run_time=0.4)
        q.add_updater(lambda m, dt: m.set_value(max(Q_MIN, m.get_value() - dt * 0.11)))
        lab = T("Schwann cell repair support", 28, SAGE).move_to([0, REP_Y - 0.65, 0])
        self.at("schwann cells lose")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("distant targets")
        self.play(FadeIn(R["l_tgt"]), Indicate(R["target"], color=GREY, scale_factor=1.05), run_time=0.8)
        self.at("hard to reach")
        self.play(Indicate(R["target"], color=GOLD, scale_factor=1.05), run_time=0.8)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self):
        self.add(*ruler_state())
        self.wait(self.narration_s)
        self.finish()


AX_L, AX_R = -4.3, 2.0


class S20Fix(SpokenScene):
    def construct(self):
        divider = Line([0, -3.7, 0], [0, 3.7, 0], color=GREY, stroke_opacity=0.4)
        soma_l = soma_at(AX_L, 2.7, 0.85)
        top_l = tube_v(AX_L, 1.85, 0.3, 0.9)
        fail = beads_v(AX_L, 0.3, -2.9, 0.9, 6)
        fail.set_opacity(0.55)
        self.add(divider, soma_l, top_l, fail)
        blk_l = bchip("SARM1 blocked", RED, 28)
        blk_l.next_to([AX_L + 0.5, -1.3, 0], RIGHT, buff=0.15)
        l_att = T("still attached", 30, BLUE).next_to([AX_L + 0.5, 1.2, 0], RIGHT, buff=0.15)
        self.at("blocking")
        self.play(FadeIn(blk_l, shift=DOWN * 0.1), run_time=0.5)
        solid = tube_v(AX_L, 0.3, -2.9, 0.9)
        self.at("may help failing axons")
        self.play(fail.animate.set_opacity(0.3), run_time=0.7)
        self.at("still attached")
        self.play(FadeIn(l_att), run_time=0.35)
        # Hold the beaded, fading state through its description before protection.
        self.play(ReplacementTransform(fail, solid), run_time=0.65)
        soma_r = soma_at(AX_R, 2.7, 0.85)
        prox_r = tube_v(AX_R, 1.85, 0.5, 0.9)
        stump = tube_v(AX_R, -0.4, -2.9, 0.9)
        cut = VGroup(*[Line([AX_R - 0.7, 0.05 + dy - 0.1, 0], [AX_R + 0.7, 0.05 + dy + 0.1, 0], color=TEXT, stroke_width=5) for dy in (-0.07, 0.07)])
        self.at("a fully severed stump")
        self.play(FadeIn(soma_r), FadeIn(prox_r), FadeIn(stump), FadeIn(cut), run_time=0.55)
        blk_r = bchip("SARM1 blocked", RED, 28)
        blk_r.next_to([AX_R + 0.5, -1.65, 0], RIGHT, buff=0.15)
        mark = xmark([AX_R + 1.4, 0.05, 0], 0.28, RED, 6)
        l_no = T("cannot rejoin", 30, GREY).next_to(mark, RIGHT, buff=0.2)
        self.at("cannot rejoin its cell body")
        self.play(FadeIn(blk_r, shift=DOWN * 0.1), Create(mark), FadeIn(l_no), run_time=0.5)
        self.at("on its own")
        self.play(Indicate(mark, color=RED, scale_factor=1.3), run_time=0.7)
        self.finish()


def tube_v(x, y_top, y_bot, w=0.9, color=BLUE, op=0.3):
    return RoundedRectangle(corner_radius=w / 2, width=w, height=y_top - y_bot, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=op).move_to([x, (y_top + y_bot) / 2, 0])


def beads_v(x, y_top, y_bot, w=0.9, n=6, color=BLUE, op=0.3):
    pitch = (y_top - y_bot) / n
    g = VGroup()
    for i in range(n):
        h = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w * 0.9, height=h, stroke_color=color, stroke_width=3.5,
                               fill_color=color, fill_opacity=op).move_to([x + (0.05 if i % 2 else -0.05), y_top - pitch * (i + 0.5), 0]))
    return g


def fix_chips():
    spec = [("Nogo blocker", RED), ("scar enzyme", RED), ("growth boost", BLUE), ("bridge", SAGE)]
    chips = [bchip(t, c, 28) for t, c in spec]
    VGroup(*chips).arrange(RIGHT, buff=0.3).move_to([0, -3.15, 0])
    return chips


class S21Fix2(SpokenScene):
    def construct(self):
        ss = Seesaw(12, 1.0, 0.5, py=0.2, vis=0.0)
        self.add(*ss.mobs())
        self.at("for regrowth")
        self.play(ss.vis.animate.set_value(1), run_time=0.8)
        chips = fix_chips()
        steps = [(0.85, None, 9), (0.7, None, 6), (None, 0.7, 3.5), (0.55, None, 1.5)]
        self.at("no single fix")
        for chp, (r, b, a) in zip(chips, steps):
            anims = [FadeIn(chp, shift=UP * 0.15), ss.a.animate.set_value(a)]
            if r is not None:
                anims.append(ss.r.animate.set_value(r))
            if b is not None:
                anims.append(ss.b.animate.set_value(b))
            self.play(*anims, run_time=0.45)
        note = T("none yet restores function reliably in people", 36, TEXT).move_to([0, 3.4, 0])
        self.at("none yet restores function")
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        l1 = T("One cut, two fates.", 52, TEXT, font=TITLE_FONT).move_to([0, 2.0, 0])
        l2 = T("A program for the cut-off piece", 40, TEXT, t2c={"program": RED}).move_to([0, 0.7, 0])
        a = T("and a balance of drive", 40, TEXT, t2c={"drive": BLUE})
        b = T("against resistance", 40, TEXT, t2c={"resistance": RED})
        l3 = VGroup(a, b).arrange(RIGHT, buff=0.2).move_to([0, -0.4, 0])
        l4 = T("for the attached one.", 40, TEXT).move_to([0, -1.5, 0])
        small = T("a rule of thumb, not a measured quantity", 26, GREY).move_to([0, -2.6, 0])
        self.at("one cut")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.6)
        self.at("a program for the")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.6)
        self.at("and a balance of drive")
        self.play(FadeIn(a, shift=UP * 0.15), run_time=0.5)
        self.at("against resistance")
        self.play(FadeIn(b, shift=UP * 0.15), run_time=0.5)
        self.at("for the attached one")
        self.play(FadeIn(l4, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(small), run_time=0.5)
        self.finish()


class S23End(EndCard):
    LINE = "Cut-off piece: a program. Attached piece: drive against resistance."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT, t2c={"program": RED, "drive": BLUE, "resistance": RED})
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
