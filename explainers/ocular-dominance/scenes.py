"""Ocular dominance and the critical period, chapter 1: One Cell, Two Eyes  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film; same in every chapter)
  ORANGE = the RIGHT eye = contralateral to the recorded (left) hemisphere, and cells / axons / bars it drives (group 1 end)
  BLUE   = the LEFT eye = ipsilateral, and cells / axons / bars it drives (group 7 end)
  PURPLE = a cortical cell driven by both eyes (binocular)
  RED    = silent / unresponsive cell, a crossed-out idea
  GOLD   = time tags ("1 week"), the question mark, the credit card line
  GREY   = outlines, brain, cortex, neutral and unmeasured cells
Histogram bars run from orange (group 1) through purple (group 4) to blue (group 7).
The old single film (scenes.old.py) used blue/yellow for eye A/B; here the eyes are tied to the lesson's convention
(left hemisphere recorded, right eye contralateral = orange, left eye ipsilateral = blue).

Fix round (FIXES.md): layouts zoomed onto the left hemisphere, stripes grown in layer 4, the s09 layer stack carried into
s10 and s11, a bigger two-eye recording scene, readable group boxes, a complete histogram with axes.
"""
import numpy as np

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
from bp_style import *  # noqa: F401,F403

# ------------------------------------------------------------------ small helpers


def arr(a, b, color=GREY, w=6, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def make_eye(color, scale=1.0):
    ell = Ellipse(width=2.0, height=1.1, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1)
    return VGroup(ell, pup, glint).scale(scale)


def eye_close(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.07), g[1].animate.set_opacity(0), g[2].animate.set_opacity(0)]


def gcol(i):
    """colour of ocular dominance group i (0..6): orange -> purple -> blue"""
    O, P, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(O, P, i / 3) if i <= 3 else interpolate_color(P, B, (i - 3) / 3)


def halo(text, size=24, color=TEXT, **kw):
    """text with a dark outline so it stays legible over stripes"""
    t = T(text, size, color, **kw)
    t.set_stroke(BG, 8, background=True)
    return t


def cell_dot(color, r=0.3, op=0.7, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)


def recolor(c, color, op=0.7):
    return c.animate.set_stroke(color).set_fill(color, op)


def at_left(mob, x):
    return mob.move_to([x + mob.width / 2, mob.get_center()[1], 0])


# ------------------------------------------------------------------ the cats (scene 1)


def cat_head(scale=1.0, kitten=False):
    """order: earL, earR, head, eye of the animal's right (orange), eye of its left (blue), nose, whiskers, [tabby marks]"""
    kw = dict(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    if kitten:
        earL = Polygon([-1.1, 0.5, 0], [-0.95, 1.25, 0], [-0.3, 0.95, 0], **kw)
        earR = Polygon([1.1, 0.5, 0], [0.95, 1.25, 0], [0.3, 0.95, 0], **kw)
        head = Ellipse(width=2.5, height=2.15, **kw)
        eR = make_eye(ORANGE, 0.4).move_to([-0.55, 0.12, 0])
        eL = make_eye(BLUE, 0.4).move_to([0.55, 0.12, 0])
        nose = Polygon([-0.09, -0.22, 0], [0.09, -0.22, 0], [0, -0.34, 0], stroke_width=0, fill_color=GREY, fill_opacity=0.9)
    else:
        earL = Polygon([-1.15, 0.45, 0], [-1.0, 1.4, 0], [-0.3, 0.95, 0], **kw)
        earR = Polygon([1.15, 0.45, 0], [1.0, 1.4, 0], [0.3, 0.95, 0], **kw)
        head = Ellipse(width=2.6, height=2.1, **kw)
        eR = make_eye(ORANGE, 0.31).move_to([-0.55, 0.15, 0])
        eL = make_eye(BLUE, 0.31).move_to([0.55, 0.15, 0])
        nose = Polygon([-0.12, -0.2, 0], [0.12, -0.2, 0], [0, -0.36, 0], stroke_width=0, fill_color=GREY, fill_opacity=0.9)
    wh = VGroup(*[Line([s * 0.55, -0.3 - 0.05 * k, 0], [s * 1.55, -0.2 - 0.22 * k, 0], color=GREY, stroke_width=3)
                  for s in (-1, 1) for k in range(-1, 2)])
    parts = [earL, earR, head, eR, eL, nose, wh]
    if not kitten:
        parts.append(VGroup(*[Line([x, 0.62, 0], [x * 0.8, 0.95, 0], color=GREY, stroke_width=3) for x in (-0.3, 0, 0.3)]))
    return VGroup(*parts).scale(scale)


def cortex_strip(colors, cx, cy):
    box = RoundedRectangle(corner_radius=0.2, width=4.2, height=0.95, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.08)
    cs = [cell_dot(c, 0.28, 0.7).move_to([x, 0, 0]) for x, c in zip((-1.5, -0.75, 0, 0.75, 1.5), colors)]
    g = VGroup(box, *cs).move_to([cx, cy, 0])
    return g, list(g)[1:]


# ------------------------------------------------------------------ the brain seen from above (front at the top)
BC = np.array([0.0, -0.35, 0.0])
EYE_R = np.array([3.4, 3.4, 0.0])     # the animal's right eye is on the viewer's right (seen from above, front up)
EYE_L = np.array([-3.4, 3.4, 0.0])
LGN_C = np.array([-2.9, 0.8, 0.0])    # left hemisphere
V1_C = np.array([-2.4, -2.25, 0.0])


def brain():
    d = {}
    d["out"] = Ellipse(width=12.0, height=6.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to(BC)
    d["mid"] = DashedLine([0, 3.0, 0], [0, -3.7, 0], color=GREY, stroke_width=2, dash_length=0.12).set_opacity(0.5)
    d["front"] = T("front", 28, GREY).move_to([0.75, 2.55, 0])
    d["back"] = T("back", 28, GREY).move_to([0.75, -3.3, 0])
    d["eR"] = make_eye(ORANGE, 0.5).move_to(EYE_R)
    d["eL"] = make_eye(BLUE, 0.5).move_to(EYE_L)
    kr = VGroup(make_eye(ORANGE, 0.36), T("right eye", 32, ORANGE))
    kr[1].next_to(kr[0], RIGHT, buff=0.25)
    kl = VGroup(make_eye(BLUE, 0.36), T("left eye", 32, BLUE))
    kl[1].next_to(kl[0], RIGHT, buff=0.25)
    d["key"] = VGroup(kr, kl).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.0, -0.35, 0])
    d["lgn"] = Ellipse(width=2.3, height=1.25, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.18).move_to(LGN_C)
    d["v1"] = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.32).move_to(V1_C)
    d["aR"] = arr([3.4, 3.1, 0], [-1.9, 1.25, 0], ORANGE, 7)
    d["aL"] = arr([-3.4, 3.1, 0], [-3.5, 1.42, 0], BLUE, 7)
    d["bR"] = arr([-3.7, 0.18, 0], [-3.7, -1.72, 0], ORANGE, 7)
    d["bL"] = arr([-2.1, 0.18, 0], [-1.7, -1.72, 0], BLUE, 7)
    return d


def v1_label(text="visual cortex", size=24):
    return T(text, size, TEXT).move_to(V1_C)


def lgn_label():
    return T("LGN", 28, TEXT, weight=BOLD).move_to([-2.9, -0.45, 0])


# ------------------------------------------------------------------ the LGN stack (scenes 4, 5)
SLAB_Y = [1.95 - 0.78 * i for i in range(6)]


def lgn_stack():
    d = {}
    d["frame"] = RoundedRectangle(corner_radius=0.25, width=8.3, height=5.3, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.05).move_to([0, 0, 0])
    d["slabs"] = VGroup(*[Rectangle(width=7.8, height=0.6, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                                    fill_opacity=0.12).move_to([0, y, 0]) for y in SLAB_Y])
    d["lines"] = VGroup(*[arr([-6.3, y, 0], [-4.0, y, 0], ORANGE if i % 2 == 0 else BLUE, 6, tip=0.2)
                          for i, y in enumerate(SLAB_Y)])
    d["cells"] = VGroup(*[Circle(radius=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.1)
                          .move_to([x, y, 0]) for y in SLAB_Y for x in np.arange(-3.0, 3.01, 1.0)])
    d["name"] = T("LGN", 30, TEXT, weight=BOLD).move_to([0, 3.15, 0])
    d["fromR"] = T("from the right eye", 24, ORANGE).move_to([-5.0, 3.3, 0])
    d["fromL"] = T("from the left eye", 24, BLUE).move_to([-5.0, 2.8, 0])
    d["tag"] = T("six layers drawn, schematic", 22, GREY).move_to([0, -3.3, 0])
    return d


def color_slabs(d):
    anims = []
    for i, s in enumerate(d["slabs"]):
        c = ORANGE if i % 2 == 0 else BLUE
        anims.append(s.animate.set_stroke(c).set_fill(c, 0.28))
    return anims


def color_cells(d, skip=()):
    anims = []
    for i, y in enumerate(SLAB_Y):
        c = ORANGE if i % 2 == 0 else BLUE
        for j in range(7):
            if i * 7 + j in skip:
                continue
            anims.append(d["cells"][i * 7 + j].animate.set_stroke(c).set_fill(c, 0.9))
    return anims


# ------------------------------------------------------------------ the cortex cross-section (scenes 6, 9, 10, 11)
LAYER_H = [0.6, 0.9, 0.9, 1.15, 0.95, 1.0]


class Slab:
    """six cortical layers, ten alternating stripes in layer 4, five binocular cells above and below, their inputs.
    Same structure for every size, so one slab can transform into another."""

    def __init__(self, xl=-4.6, xr=4.8, ytop=3.0, hs=1.0, cell_col=GREY, cell_op=0.2, cr=0.34):
        self.xl, self.xr, self.sw = xl, xr, (xr - xl) / 10.0
        ys, y = [], ytop
        for h in LAYER_H:
            ys.append((y, y - h * hs))
            y -= h * hs
        self.ys = ys
        self.l4top, self.l4bot = ys[3]
        self.l4mid = (self.l4top + self.l4bot) / 2
        self.bands = VGroup(*[Rectangle(width=xr - xl, height=a - b, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                                        fill_opacity=0.07 if i % 2 else 0.13).move_to([(xl + xr) / 2, (a + b) / 2, 0])
                              for i, (a, b) in enumerate(ys)])
        self.nums = VGroup(*[T(str(i + 1), 24, GREY).move_to([xl - 0.45, (a + b) / 2, 0]) for i, (a, b) in enumerate(ys)])
        self.stripes = VGroup(*[Rectangle(width=self.sw, height=self.l4top - self.l4bot, stroke_width=0,
                                          fill_color=ORANGE if k % 2 == 0 else BLUE, fill_opacity=0.45)
                                .move_to([self.sx(k), self.l4mid, 0]) for k in range(10)])
        c2, c6 = (ys[1][0] + ys[1][1]) / 2, (ys[5][0] + ys[5][1]) / 2
        self.cpos = [(xl + self.sw * b, c2) for b in (1, 5, 9)] + [(xl + self.sw * b, c6) for b in (3, 7)]
        self.cells = VGroup(*[cell_dot(cell_col, cr, cell_op).move_to([x, y, 0]) for x, y in self.cpos])
        ins = VGroup()
        for (x, y), b in zip(self.cpos, (1, 5, 9, 3, 7)):
            up = y > self.l4mid
            edge = self.l4top + 0.02 if up else self.l4bot - 0.02
            tgt = y - cr if up else y + cr
            ins.add(arr([self.sx(b - 1), edge, 0], [x - 0.12, tgt, 0], ORANGE, 5, tip=0.16))
            ins.add(arr([self.sx(b), edge, 0], [x + 0.12, tgt, 0], BLUE, 5, tip=0.16))
        self.inputs = ins
        self.group = VGroup(self.bands, self.stripes, self.cells, self.inputs)

    def sx(self, k):
        return self.xl + self.sw * (k + 0.5)

    def l4_label(self):
        t = T("layer 4", 24, TEXT, weight=BOLD)
        return t.move_to([self.xl - 0.25 - t.width / 2, self.l4mid, 0])

    def side_label(self, which, text=None, color=TEXT):
        if which == "above":
            y = (self.ys[0][0] + self.ys[2][1]) / 2
            txt = text or "above\nlayer 4"
        else:
            y = (self.ys[4][0] + self.ys[5][1]) / 2
            txt = text or "below\nlayer 4"
        return T(txt, 24, color, line_spacing=0.9).move_to([self.xr + 1.15, y, 0])

    def stripes_nudged(self, d):
        """stripes with the orange ones wider by d and the blue ones narrower by d (boundaries move)"""
        g, x = VGroup(), self.xl
        for k in range(10):
            w = self.sw + d if k % 2 == 0 else self.sw - d
            g.add(Rectangle(width=w, height=self.l4top - self.l4bot, stroke_width=0,
                            fill_color=ORANGE if k % 2 == 0 else BLUE, fill_opacity=0.45).move_to([x + w / 2, self.l4mid, 0]))
            x += w
        return g


def slab_end_s09():
    """the s09 end state: full slab, purple cells, labels"""
    sl = Slab(cell_col=PURPLE, cell_op=0.75, cr=0.36)
    sl.nums[3].become(sl.l4_label())
    sl.bands[3].set_stroke(TEXT, 4)
    ab, be = sl.side_label("above"), sl.side_label("below")
    return sl, ab, be


# ------------------------------------------------------------------ stripe / patch maps (scenes 7, 8)
def _rgb(c):
    return np.array(ManimColor(c).to_rgb()) * 255


PW, PH = 6.2, 5.0


def make_map(kind, w=PW, h=PH, dim=1.0, seed=5):
    W, H = 248, 200
    xs = np.linspace(0, w, W)[None, :]
    ys = np.linspace(0, h, H)[:, None]
    per = 1.55
    if kind == "macaque":
        v = np.sin(2 * np.pi * xs / per) * np.ones_like(ys)
        t = 1 / (1 + np.exp(-v * 30))
    else:
        rng = np.random.default_rng(seed)

        def noise():
            n = np.zeros((H, W))
            for _ in range(4):
                kx, ky = rng.normal(0, 1.5, 2)
                n += np.sin(kx * xs + ky * ys + rng.uniform(0, 2 * np.pi))
            return n / 2.0
        v = np.sin(2 * np.pi * xs / per + 1.0 * noise()) + 0.55 * noise()
        t = 1 / (1 + np.exp(-v * 2.4))
    o, b, bg = _rgb(ORANGE), _rgb(BLUE), _rgb(BG)
    rgb = t[..., None] * o + (1 - t[..., None]) * b
    rgb = rgb * dim + bg * (1 - dim)
    img = np.dstack([rgb, np.full((H, W), 255.0)]).astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    im.scale_to_fit_width(w)
    return im


MAC_C = np.array([-3.4, -0.05, 0.0])
CAT_C = np.array([3.4, -0.05, 0.0])
PER = 1.55


def panel(kind, center, dim=1.0):
    im = make_map(kind, dim=dim).move_to(center)
    fr = Rectangle(width=PW, height=PH, stroke_color=GREY, stroke_width=3).move_to(center)
    return im, fr


# ------------------------------------------------------------------ neurons and spike trains
def neuron(c=(0.0, 0.0), s=1.0):
    c = np.array([c[0], c[1], 0.0])
    soma = Ellipse(width=1.0 * s, height=0.9 * s, stroke_color=GREY, stroke_width=4, fill_color=TEXT, fill_opacity=0.14).move_to(c)
    dend = VGroup()
    for a, L in [(1.9, 1.25), (1.2, 1.1), (2.7, 1.0), (0.5, 1.0), (0.0, 0.8)]:
        d0 = np.array([np.cos(a), np.sin(a), 0.0])
        p0 = c + np.array([0.5 * np.cos(a) * s, 0.45 * np.sin(a) * s, 0.0])
        p1 = p0 + L * s * d0
        dend.add(Line(p0, p1, color=GREY, stroke_width=4))
        for da in (-0.55, 0.55):
            p2 = p1 + 0.55 * L * s * np.array([np.cos(a + da), np.sin(a + da), 0.0])
            dend.add(Line(p1, p2, color=GREY, stroke_width=3))
    pts = [c + np.array(p) * s for p in ([0.15, -0.45, 0], [0.3, -1.3, 0], [1.2, -2.0, 0], [2.4, -2.2, 0])]
    axon = VMobject(color=GREY, stroke_width=4).set_points_smoothly(pts)
    return VGroup(dend, axon, soma)


def poisson(rate, seed, start=0.04, gap=0.05):
    rng = np.random.default_rng(seed)
    t, out = start, []
    while True:
        t += gap + rng.exponential(1.0 / rate)
        if t >= 0.97:
            return out
        out.append(t)


def trace(x0, x1, y0, amp, spikes, color, sw=4):
    xs = np.linspace(x0, x1, int((x1 - x0) / 0.03))
    ys = y0 + 0.03 * np.sin(xs * 17) + 0.02 * np.sin(xs * 41)
    for s in spikes:
        xc = x0 + s * (x1 - x0)
        ys = ys + amp * np.clip(1 - np.abs(xs - xc) / 0.09, 0, None) - 0.25 * amp * np.clip(1 - np.abs(xs - xc - 0.14) / 0.07, 0, None)
    m = VMobject(color=color, stroke_width=sw)
    m.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    return m


# ------------------------------------------------------------------ the seven groups (scenes 17 to 25)
HX = [-4.2 + 1.6 * i for i in range(7)]
CX = 0.6            # centre of the group row
BW = 1.45
YB = -2.3           # baseline of the histogram
UNIT = 1.1          # height of one cell
BOXH = 0.75
COUNTS = [2, 3, 4, 2, 2, 1, 1]
ORDER = [3, 2, 4, 3, 5, 2, 1, 3, 6, 5, 2, 4, 7, 3, 1]   # fifteen cells, by group; their counts equal COUNTS
BIG_Y, BIG_H = -0.1, 3.2
FRAC = [1, 5 / 6, 2 / 3, 0.5, 1 / 3, 1 / 6, 0]          # share of orange in each group's box


def big_boxes():
    rects = VGroup(*[Rectangle(width=BW, height=BIG_H, stroke_color=gcol(i), stroke_width=3, fill_color=gcol(i),
                               fill_opacity=0.06).move_to([HX[i], BIG_Y, 0]) for i in range(7)])
    nums = VGroup(*[T(str(i + 1), 54, TEXT, weight=BOLD).move_to([HX[i], BIG_Y + BIG_H / 2 + 0.5, 0]) for i in range(7)])
    return rects, nums


def small_boxes():
    cy = YB - BOXH / 2
    rects = VGroup(*[Rectangle(width=BW, height=BOXH, stroke_color=gcol(i), stroke_width=3, fill_color=gcol(i),
                               fill_opacity=0.25).move_to([HX[i], cy, 0]) for i in range(7)])
    nums = VGroup(*[T(str(i + 1), 32, TEXT, weight=BOLD).move_to([HX[i], cy, 0]) for i in range(7)])
    return rects, nums


def box_center(i):
    return np.array([HX[i], YB - BOXH / 2, 0.0])


MID_Y, MID_H = -2.95, 1.2     # the readable group boxes of the worked cells (s20 to s22)


def mid_boxes():
    rects = VGroup(*[Rectangle(width=BW, height=MID_H, stroke_color=gcol(i), stroke_width=3, fill_color=gcol(i),
                               fill_opacity=0.25).move_to([HX[i], MID_Y, 0]) for i in range(7)])
    nums = VGroup(*[T(str(i + 1), 44, TEXT, weight=BOLD).move_to([HX[i] - 0.15, MID_Y, 0]) for i in range(7)])
    return rects, nums


def mid_center(i):
    return np.array([HX[i], MID_Y, 0.0])


def split_fill(i, frac, op=0.6):
    g = VGroup()
    if frac > 0:
        g.add(Rectangle(width=BW * frac, height=BIG_H, stroke_width=0, fill_color=ORANGE, fill_opacity=op)
              .move_to([HX[i] - BW / 2 + BW * frac / 2, BIG_Y, 0]))
    if frac < 1:
        g.add(Rectangle(width=BW * (1 - frac), height=BIG_H, stroke_width=0, fill_color=BLUE, fill_opacity=op)
              .move_to([HX[i] + BW / 2 - BW * (1 - frac) / 2, BIG_Y, 0]))
    return g


def hist_bars(counts=COUNTS, op=0.6):
    out = VGroup()
    for i, c in enumerate(counts):
        h = max(c * UNIT, 0.02)
        out.add(Rectangle(width=BW, height=h, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                          fill_opacity=op).move_to([HX[i], YB + h / 2, 0]))
    return out


def hump(counts=COUNTS):
    """outline through the real bar tops: along each bar's top edge, a short step over each gap"""
    pts = []
    for i, c in enumerate(counts):
        y = YB + c * UNIT + 0.05
        pts += [np.array([HX[i] - BW / 2, y, 0]), np.array([HX[i] + BW / 2, y, 0])]
    m = VMobject(color=TEXT, stroke_width=6).set_points_as_corners(pts)
    return m


def axes():
    x = -5.1
    line = Line([x, YB, 0], [x, YB + 4.5 * UNIT, 0], color=GREY, stroke_width=3)
    base = Line([x, YB, 0], [6.2, YB, 0], color=GREY, stroke_width=3)
    ticks = VGroup(*[Line([x - 0.12, YB + k * UNIT, 0], [x, YB + k * UNIT, 0], color=GREY, stroke_width=3) for k in range(5)])
    labs = VGroup(*[T(str(k), 26, TEXT).move_to([x - 0.42, YB + k * UNIT, 0]) for k in range(5)])
    yl = T("number of cells", 26, TEXT).rotate(PI / 2).move_to([-6.35, YB + 2.2 * UNIT, 0])
    xt = T("ocular dominance group", 26, GREY).move_to([CX, -3.55, 0])
    return VGroup(line, base, ticks, labs, yl, xt)


def hist_title(text="normal adult cat (schematic)"):
    return T(text, 30, TEXT, font=TITLE_FONT).move_to([CX, 3.55, 0])


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Ocular Dominance and the Critical Period"
    TITLE = "One Cell, Two Eyes"


class S01(SpokenScene):
    def construct(self):
        kit = cat_head(1.15, kitten=True).move_to([-3.5, 0.3, 0])
        ad = cat_head(1.55).move_to([3.5, 0.3, 0])
        nk = T("young kitten", 30).move_to([-3.5, 3.45, 0])
        na = T("adult cat", 30).move_to([3.5, 3.45, 0])
        self.play(FadeIn(kit), FadeIn(ad), run_time=0.4)
        self.at("one eye")
        self.play(*eye_close(kit[3]), run_time=0.5)
        self.at("young kitten")
        self.play(FadeIn(nk), run_time=0.4)
        wk = chip("1 week", GOLD, size=26).move_to([-3.5, 2.8, 0])
        self.at("week")
        self.play(FadeIn(wk, shift=DOWN * 0.1), run_time=0.4)
        sk, ck = cortex_strip([ORANGE, PURPLE, PURPLE, PURPLE, BLUE], -3.5, -2.15)
        lk = T("cortical cells", 26, GREY).move_to([-3.5, -3.0, 0])
        key = VGroup(T("a cell is driven by", 22, GREY),
                     *[VGroup(Dot(radius=0.13, color=c), T(t, 24, c)).arrange(RIGHT, buff=0.2)
                       for c, t in ((ORANGE, "right eye"), (BLUE, "left eye"), (PURPLE, "both eyes"))])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0.1, -2.2, 0])
        self.at("visual cortex")
        self.play(FadeIn(sk, shift=UP * 0.1), FadeIn(lk), FadeIn(key), run_time=0.6)
        lk2 = T("changed", 30, TEXT).move_to([-3.5, -3.5, 0])
        self.at("changes")
        self.play(*[recolor(c, col, 0.7) for c, col in zip(ck, [BLUE, BLUE, PURPLE, BLUE, BLUE])],
                  FadeIn(lk2, shift=UP * 0.1), run_time=0.9)
        self.at("close an")
        self.play(FadeIn(na), run_time=0.4)
        self.at("eye for")
        self.play(*eye_close(ad[3]), run_time=0.5)
        ma = chip("months", GOLD, size=26).move_to([3.5, 2.8, 0])
        self.at("months")
        self.play(FadeIn(ma, shift=DOWN * 0.1), run_time=0.4)
        sa, ca = cortex_strip([ORANGE, PURPLE, PURPLE, PURPLE, BLUE], 3.5, -2.15)
        la = T("cortical cells", 26, GREY).move_to([3.5, -3.0, 0])
        self.at("the cortex looks")
        self.play(FadeIn(sa, shift=UP * 0.1), FadeIn(la), run_time=0.5)
        la2 = T("looks normal", 30, TEXT).move_to([3.5, -3.5, 0])
        self.at("looks normal")
        self.play(FadeIn(la2, shift=UP * 0.1), run_time=0.5)
        q = T("?", 140, GOLD, weight=BOLD).move_to([0, 0.5, 0])
        self.at("why")
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        b = brain()
        self.play(Create(b["out"]), FadeIn(b["mid"]), run_time=1.0)
        self.play(FadeIn(b["front"]), FadeIn(b["back"]), run_time=0.5)
        self.at("the eyes")
        self.play(FadeIn(b["eR"], shift=DOWN * 0.15), FadeIn(b["eL"], shift=DOWN * 0.15), FadeIn(b["key"]), run_time=0.5)
        self.at("the cortex")
        self.play(FadeIn(b["v1"], shift=UP * 0.1), FadeIn(v1_label()), run_time=0.6)
        self.finish()


def brain_base(b, key=True):
    """brain of s02 as carried into later scenes"""
    g = [b["out"], b["mid"], b["front"], b["back"], b["eR"], b["eL"], b["v1"], v1_label()]
    if key:
        g.append(b["key"])
    return g


class S03(SpokenScene):
    def construct(self):
        b = brain()
        self.add(*brain_base(b))
        self.at("its axons")
        self.play(Create(b["aR"]), Create(b["aL"]), run_time=1.2)
        self.at("relay station")
        self.play(GrowFromCenter(b["lgn"]), run_time=0.6)
        th = T("thalamus", 24, GREY).move_to([-2.9, -0.45, 0])
        self.at("the thalamus")
        self.play(FadeIn(th, shift=UP * 0.1), run_time=0.4)
        full = T("lateral geniculate\nnucleus", 24, TEXT, line_spacing=0.9).move_to([-2.9, -0.6, 0])
        self.at("lateral geniculate nucleus")
        self.play(ReplacementTransform(th, full), run_time=0.6)
        short = lgn_label()
        self.at("the lgn")
        self.play(ReplacementTransform(full, short), run_time=0.7)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        b = brain()
        s = lgn_stack()
        lab = lgn_label()
        rest = brain_base(b) + [b["aR"], b["aL"], lab]
        self.add(*rest, b["lgn"])
        self.play(*[FadeOut(m) for m in rest], Transform(b["lgn"], s["frame"]),
                  FadeIn(s["slabs"], lag_ratio=0.15), FadeIn(s["name"]), run_time=0.8)
        self.at("axons end")
        self.play(LaggedStart(*[Create(m) for m in s["lines"]], lag_ratio=0.2), FadeIn(s["fromR"]), FadeIn(s["fromL"]), run_time=0.9)
        self.at("separate layers")
        self.play(*color_slabs(s), FadeIn(s["tag"]), run_time=0.9)
        self.at("so most")
        self.play(FadeIn(s["cells"], lag_ratio=0.02), run_time=0.8)
        self.at("driven by one eye")
        c0, c1 = s["cells"][3], s["cells"][7 + 3]
        self.play(c0.animate.set_stroke(ORANGE).set_fill(ORANGE, 1.0).scale(1.5), Flash(c0, color=ORANGE, flash_radius=0.5, line_length=0.15), run_time=0.5)
        self.play(c1.animate.set_stroke(BLUE).set_fill(BLUE, 1.0).scale(1.5), Flash(c1, color=BLUE, flash_radius=0.5, line_length=0.15), run_time=0.5)
        self.play(c0.animate.scale(1 / 1.5), c1.animate.scale(1 / 1.5), *color_cells(s, skip=(3, 10)), run_time=0.8)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        b = brain()
        s = lgn_stack()
        for i, c in enumerate(s["slabs"]):
            col = ORANGE if i % 2 == 0 else BLUE
            c.set_stroke(col).set_fill(col, 0.28)
        for i in range(6):
            col = ORANGE if i % 2 == 0 else BLUE
            for j in range(7):
                s["cells"][i * 7 + j].set_stroke(col).set_fill(col, 0.9)
        lab = lgn_label()
        base = brain_base(b)
        v1lab = base[7]
        self.add(s["frame"], s["slabs"], s["lines"], s["cells"], s["name"], s["fromR"], s["fromL"], s["tag"])
        self.play(FadeOut(VGroup(s["slabs"], s["lines"], s["cells"], s["name"], s["fromR"], s["fromL"], s["tag"])),
                  Transform(s["frame"], b["lgn"]),
                  *[FadeIn(m) for m in base], FadeIn(b["aR"]), FadeIn(b["aL"]), FadeIn(lab), run_time=1.0)
        self.at("carry the signal")
        self.play(Create(b["bR"]), Create(b["bL"]), run_time=1.3)
        v1new = v1_label("primary visual cortex", 22)
        self.at("primary visual cortex")
        self.play(ReplacementTransform(v1lab, v1new), Indicate(b["v1"], color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("back of the brain")
        self.play(Indicate(b["back"], color=TEXT, scale_factor=1.3), run_time=0.9)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        b = brain()
        s = lgn_stack()
        lab = lgn_label()
        g = VGroup(*brain_base(b)[:-1], b["aR"], b["aL"], b["lgn"], lab, b["bR"], b["bL"])
        g[7].become(v1_label("primary visual cortex", 22))
        sl = Slab()
        self.add(g, b["key"])
        self.play(FadeOut(g), FadeOut(b["key"]), FadeIn(sl.bands), FadeIn(sl.nums), run_time=0.45)
        ymid = sl.l4mid
        axons = VGroup(*[Line([sl.sx(k), -3.15, 0], [sl.sx(k), ymid, 0], color=ORANGE if k % 2 == 0 else BLUE, stroke_width=6)
                         for k in range(10)])
        frm = T("axons from the LGN", 24, GREY).move_to([0.1, -3.55, 0])
        self.at("end mainly")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.08), FadeIn(frm), run_time=0.7)
        l4 = sl.l4_label()
        self.at("layer 4")
        self.play(sl.bands[3].animate.set_stroke(TEXT, 4), ReplacementTransform(sl.nums[3], l4), run_time=0.6)
        dots = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=ORANGE if k % 2 == 0 else BLUE, fill_opacity=1)
                        .move_to([sl.sx(k), ymid, 0]) for k in range(10)])
        self.at("eyes ending")
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=0.7)
        thin = VGroup(*[r.copy().stretch_to_fit_width(0.12) for r in sl.stripes])
        self.at("alternating stripes")
        self.add(thin)
        self.play(Transform(thin, sl.stripes), run_time=1.1)
        self.bring_to_front(axons, dots)
        self.finish()


def mk08():
    d = {}
    d["dm"], _ = panel("macaque", MAC_C, dim=0.4)
    d["dc"], _ = panel("cat", CAT_C, dim=0.4)
    d["fm"] = Rectangle(width=PW, height=PH, stroke_color=GREY, stroke_width=3).move_to(MAC_C)
    d["fc"] = Rectangle(width=PW, height=PH, stroke_color=GREY, stroke_width=3).move_to(CAT_C)
    d["tm"] = T("macaque layer 4C", 32).move_to([-3.4, 2.95, 0])
    d["tc"] = T("cat layer 4", 32).move_to([3.4, 2.95, 0])
    d["tag"] = T("layer 4 seen from above, schematic", 24, GREY).move_to([0, 3.5, 0])
    xo = MAC_C[0] - PW / 2 + PER / 4 + PER * 2
    xb = xo + PER / 2
    d["xo"], d["xb"] = xo, xb
    d["mcell"] = cell_dot(ORANGE, 0.5, 0.85).move_to([xo, 0.55, 0])
    d["oin"] = arr([xo, -2.3, 0], [xo, 0.02, 0], ORANGE, 12, tip=0.3)
    bd = DashedLine([xb, -2.3, 0], [xo + 0.32, 0.18, 0], color=BLUE, stroke_width=6, dash_length=0.16)
    bd.add_tip(tip_length=0.22)
    d["bin"] = bd
    d["weak"] = halo("weak or none", 26, BLUE).move_to([xb + 1.0, -1.0, 0])
    d["mcap"] = T("mostly one eye", 28, ORANGE).move_to([-3.4, -3.15, 0])
    d["ccell"] = cell_dot(GREY, 0.5, 0.45).move_to([CAT_C[0], 0.55, 0])
    d["oc"] = arr([CAT_C[0] - 1.0, -2.3, 0], [CAT_C[0] - 0.25, 0.05, 0], ORANGE, 9, tip=0.26)
    d["bc"] = arr([CAT_C[0] + 1.0, -2.3, 0], [CAT_C[0] + 0.25, 0.05, 0], BLUE, 9, tip=0.26)
    d["ccap"] = T("more cells hear both", 28, PURPLE).move_to([3.4, -3.15, 0])
    return d


class S07(SpokenScene):
    def construct(self):
        sl = Slab()
        sl.nums[3].become(sl.l4_label())
        sl.bands[3].set_stroke(TEXT, 4)
        b = brain()
        axons = VGroup(*[Line([sl.sx(k), -3.15, 0], [sl.sx(k), sl.l4mid, 0], color=ORANGE if k % 2 == 0 else BLUE, stroke_width=6)
                         for k in range(10)])
        dots = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=ORANGE if k % 2 == 0 else BLUE, fill_opacity=1)
                        .move_to([sl.sx(k), sl.l4mid, 0]) for k in range(10)])
        frm = T("axons from the LGN", 24, GREY).move_to([0.1, -3.55, 0])
        old = VGroup(sl.bands, sl.stripes, sl.nums, axons, dots, frm)
        self.add(old)
        mim, mfr = panel("macaque", MAC_C)
        cim, cfr = panel("cat", CAT_C)
        dcim, _ = panel("cat", CAT_C, dim=0.25)
        ml = T("macaque", 34).move_to([-3.4, 2.95, 0])
        cl = T("cat", 34).move_to([3.4, 2.95, 0])
        tag = T("layer 4 seen from above, schematic", 24, GREY).move_to([0, 3.5, 0])
        self.play(FadeOut(old), FadeIn(mim), FadeIn(mfr), FadeIn(ml), FadeIn(dcim), FadeIn(cfr), FadeIn(cl), FadeIn(tag), run_time=0.7)
        odc = T("ocular dominance columns", 28, TEXT).move_to([-3.4, -3.0, 0])
        self.at("ocular dominance columns")
        self.play(FadeIn(odc, shift=UP * 0.1), run_time=0.5)
        sharp = T("sharp", 28, TEXT).move_to([-3.4, -3.5, 0])
        self.at("are sharp")
        self.play(FadeIn(sharp, shift=UP * 0.1), run_time=0.4)
        self.at("in cats")
        self.play(FadeIn(cim), run_time=0.6)
        reg = T("less regular", 28, TEXT).move_to([3.4, -3.0, 0])
        self.at("less regular")
        self.play(FadeIn(reg, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        d = mk08()
        mim, _ = panel("macaque", MAC_C)
        cim, _ = panel("cat", CAT_C)
        ml = T("macaque", 34).move_to([-3.4, 2.95, 0])
        cl = T("cat", 34).move_to([3.4, 2.95, 0])
        tag = T("layer 4 seen from above, schematic", 24, GREY).move_to([0, 3.5, 0])
        odc = T("ocular dominance columns", 28, TEXT).move_to([-3.4, -3.0, 0])
        sharp = T("sharp", 28, TEXT).move_to([-3.4, -3.5, 0])
        reg = T("less regular", 28, TEXT).move_to([3.4, -3.0, 0])
        self.add(d["dm"], d["dc"], mim, cim, d["fm"], d["fc"], ml, cl, tag, odc, sharp, reg)
        self.bring_to_front(d["fm"], d["fc"])
        self.play(FadeOut(mim), FadeOut(cim), FadeOut(odc), FadeOut(sharp), FadeOut(reg),
                  ReplacementTransform(ml, d["tm"]), ReplacementTransform(cl, d["tc"]), run_time=0.8)
        self.at("most cells")
        self.play(FadeIn(d["mcell"], scale=0.5), run_time=0.5)
        self.at("driven mainly")
        self.play(GrowArrow(d["oin"]), run_time=0.6)
        self.at("by one eye")
        self.play(Create(d["bin"]), FadeIn(d["weak"]), FadeIn(d["mcap"], shift=UP * 0.1), run_time=0.8)
        self.at("cat layer 4")
        self.play(FadeIn(d["ccell"], scale=0.5), run_time=0.5)
        self.at("more cells")
        self.play(GrowArrow(d["oc"]), GrowArrow(d["bc"]), run_time=0.7)
        self.at("hear both")
        self.play(recolor(d["ccell"], PURPLE, 0.85), FadeIn(d["ccap"], shift=UP * 0.1), run_time=0.7)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        d = mk08()
        d["ccell"].set_stroke(PURPLE).set_fill(PURPLE, 0.85)
        old = Group(*[v for k, v in d.items() if k not in ("xo", "xb")])
        sl = Slab(cr=0.36)
        sl.nums[3].become(sl.l4_label())
        sl.bands[3].set_stroke(TEXT, 4)
        sl.stripes.set_opacity(0.45)
        base = Group(sl.bands, sl.nums, sl.stripes)
        self.add(old)
        self.play(FadeOut(old), FadeIn(base), run_time=0.3)
        ab = sl.side_label("above")
        self.at("above and")
        self.play(*[FadeIn(sl.cells[i], scale=0.5) for i in range(3)], FadeIn(ab), run_time=0.4)
        be = sl.side_label("below")
        self.at("below layer")
        self.play(*[FadeIn(sl.cells[i], scale=0.5) for i in (3, 4)], FadeIn(be), run_time=0.4)
        self.at("combine the two streams")
        self.play(LaggedStart(*[GrowArrow(a) for a in sl.inputs], lag_ratio=0.08), run_time=1.4)
        self.at("many cells")
        self.play(*[recolor(c, PURPLE, 0.75) for c in sl.cells], run_time=0.9)
        self.play(*[Flash(c, color=PURPLE, flash_radius=0.7, line_length=0.15) for c in sl.cells], run_time=0.8)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        old, ab, be = slab_end_s09()
        oldnums = VGroup(*[n for i, n in enumerate(old.nums)])
        self.add(old.group, oldnums, ab, be)
        new = Slab(xl=1.2, xr=6.6, ytop=3.05, hs=1.0, cell_col=PURPLE, cell_op=0.75, cr=0.3)
        # eyes, LGN, lanes
        yo, yb_ = 0.75, -0.65
        eo = make_eye(ORANGE, 0.5).move_to([-5.7, yo, 0])
        eb = make_eye(BLUE, 0.5).move_to([-5.7, yb_, 0])
        lgnbox = RoundedRectangle(corner_radius=0.2, width=1.7, height=2.4, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.08).move_to([-2.55, 0.05, 0])
        so = Rectangle(width=1.4, height=0.55, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.35).move_to([-2.55, yo, 0])
        sb = Rectangle(width=1.4, height=0.55, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.35).move_to([-2.55, yb_, 0])
        lo = VGroup(Line([-5.0, yo, 0], [-3.4, yo, 0], color=ORANGE, stroke_width=7), Line([-1.7, yo, 0], [1.15, 0.3, 0], color=ORANGE, stroke_width=7))
        lb = VGroup(Line([-5.0, yb_, 0], [-3.4, yb_, 0], color=BLUE, stroke_width=7), Line([-1.7, yb_, 0], [1.15, -0.12, 0], color=BLUE, stroke_width=7))
        labs = VGroup(T("eyes", 28).move_to([-5.7, 1.65, 0]), T("LGN", 28).move_to([-2.55, 1.65, 0]),
                      T("cortex", 28).move_to([3.9, 3.5, 0]))
        l4 = T("layer 4", 24, TEXT, weight=BOLD).move_to([0.32, new.l4mid + 0.03, 0])
        leader = Line([0.9, new.l4mid + 0.03, 0], [1.17, new.l4mid + 0.03, 0], color=TEXT, stroke_width=3)
        # first the stack shrinks on its own, then the eyes, LGN and lanes appear (no ghosts through the big stack)
        self.play(ReplacementTransform(old.group, new.group), FadeOut(oldnums), FadeOut(ab), FadeOut(be), run_time=1.0)
        self.play(FadeIn(eo), FadeIn(eb), FadeIn(lgnbox), FadeIn(so), FadeIn(sb), FadeIn(labs), Create(lo), Create(lb),
                  run_time=0.7)
        self.play(FadeIn(l4), FadeIn(leader), run_time=0.3)
        self.bring_to_front(eo, eb)
        self.at("first place")
        self.play(Indicate(new.stripes, color=TEXT, scale_factor=1.04), run_time=0.8)
        tag = T("first major site of binocular cells", 26, PURPLE).move_to([3.7, -3.2, 0])
        self.at("many single cells")
        self.play(*[Flash(c, color=PURPLE, flash_radius=0.55, line_length=0.12) for c in new.cells], run_time=0.7)
        self.at("driven by both")
        self.play(FadeIn(tag, shift=UP * 0.1), Indicate(new.cells, color=PURPLE, scale_factor=1.25), run_time=0.9)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        sl, ab, be = slab_end_s09()
        self.add(sl.group, sl.nums, ab, be)
        self.at("compete")
        for d in (0.3, -0.3, 0.0):
            self.play(Transform(sl.stripes, sl.stripes_nudged(d)), run_time=0.22)
        br = Brace(sl.stripes[-1], RIGHT, buff=0.08, color=TEXT)
        terr = T("territory", 24, TEXT, weight=BOLD).move_to([sl.xr + 1.25, sl.l4mid, 0])
        self.at("territory")
        self.play(GrowFromCenter(br), FadeIn(terr, shift=LEFT * 0.1), sl.bands[3].animate.set_stroke(TEXT, 4), run_time=0.5)
        rings = VGroup(*[Circle(radius=0.55, stroke_color=PURPLE, stroke_width=5).move_to(c.get_center()) for c in sl.cells])
        bin_a = T("binocular\ncells", 24, PURPLE, line_spacing=0.9).move_to(ab.get_center())
        bin_b = T("binocular\ncells", 24, PURPLE, line_spacing=0.9).move_to(be.get_center())
        self.at("and", lead=0.6)
        self.play(FadeOut(ab), FadeOut(be), run_time=0.3)
        self.play(FadeIn(rings, scale=1.25), FadeIn(bin_a), FadeIn(bin_b), run_time=0.6)
        self.finish()


def brain_for_recording():
    b = brain()
    left = Intersection(Ellipse(width=12.0, height=6.8).move_to(BC), Rectangle(width=6.2, height=8).move_to([-3.1, -0.5, 0]),
                        stroke_width=0, fill_color=TEXT, fill_opacity=0.14)
    elec = VGroup(Line([-6.5, -1.1, 0], [-4.2, -2.15, 0], color=TEXT, stroke_width=6), Dot([-4.2, -2.15, 0], radius=0.09, color=TEXT))
    return b, left, elec


class S12(SpokenScene):
    def construct(self):
        b, left, elec = brain_for_recording()
        self.add(b["out"], b["mid"], b["eR"], b["eL"], b["v1"], v1_label())
        tagR = T("right eye", 24, ORANGE).move_to([5.0, 3.45, 0])
        tagL = T("left eye", 24, BLUE).move_to([-5.0, 3.45, 0])
        self.at("eye is which")
        self.play(FadeIn(tagR), FadeIn(tagL), run_time=0.5)
        lab = VGroup(T("recorded side:", 24, TEXT), T("left hemisphere", 30, TEXT, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([-2.6, 1.55, 0])
        self.at("where you record")
        self.play(Create(elec[0]), FadeIn(elec[1]), FadeIn(left), FadeIn(lab), run_time=0.9)
        self.at("left hemisphere")
        self.play(Flash(elec[1], color=TEXT, flash_radius=0.6, line_length=0.15), Indicate(lab[1], color=TEXT, scale_factor=1.12), run_time=0.8)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        b, left, elec = brain_for_recording()
        lab = VGroup(T("recorded side:", 24, TEXT), T("left hemisphere", 30, TEXT, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([-2.6, 1.55, 0])
        self.add(b["out"], b["mid"], left, b["eR"], b["eL"], b["v1"], v1_label(), *elec, lab,
                 T("right eye", 24, ORANGE).move_to([5.0, 3.45, 0]), T("left eye", 24, BLUE).move_to([-5.0, 3.45, 0]))
        c1 = T("contralateral", 30, ORANGE, weight=BOLD).move_to([5.35, 3.0, 0])
        c2 = T("(opposite side)", 24, ORANGE).move_to([5.35, 2.52, 0])
        lg = lgn_label()
        self.at("opposite side")
        self.play(Create(b["aR"]), FadeIn(c2), FadeOut(lab, run_time=0.9), GrowFromCenter(b["lgn"]), FadeIn(lg), run_time=0.9)
        self.play(Create(b["bR"]), run_time=0.5)
        self.at("the right eye")
        self.play(Indicate(b["eR"], color=ORANGE, scale_factor=1.25), run_time=0.5)
        self.at("contralateral")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        i1 = T("ipsilateral", 30, BLUE, weight=BOLD).move_to([-5.35, 3.0, 0])
        i2 = T("(same side)", 24, BLUE).move_to([-5.35, 2.52, 0])
        self.at("left eye")
        self.play(Succession(Create(b["aL"], run_time=0.35), Create(b["bL"], run_time=0.35)))
        self.at("same side")
        self.play(Indicate(b["eL"], color=BLUE, scale_factor=1.25), FadeIn(i2), run_time=0.5)
        self.at("ipsilateral")
        self.play(FadeIn(i1, shift=UP * 0.1), run_time=0.5)
        self.finish()


def credit_card():
    box = RoundedRectangle(corner_radius=0.3, width=7.6, height=3.4, stroke_color=GOLD, stroke_width=4,
                           fill_color=GOLD, fill_opacity=0.06)
    n1 = T("David Hubel", 50, TEXT, font=TITLE_FONT)
    n2 = T("Torsten Wiesel", 50, TEXT, font=TITLE_FONT)
    VGroup(n1, n2).arrange(DOWN, buff=0.3).move_to(box.get_center() + UP * 0.25)
    sub = T("Nobel Prize in Physiology or Medicine, 1981", 24, GOLD).move_to(box.get_center() + DOWN * 1.3)
    return box, n1, n2, sub


def compact_card():
    """the credit card after the Nobel line is gone: tight box, names only, parked at the top"""
    box, n1, n2, sub = credit_card()
    box.stretch_to_fit_height(2.5).move_to(n1.get_center() * 0.5 + n2.get_center() * 0.5)
    g = VGroup(box, n1, n2)
    g.scale(0.58).move_to([0, 2.7, 0])
    return g


NR_C, NR_S = (0.0, -1.0), 1.15


class S14(SpokenScene):
    def construct(self):
        box, n1, n2, sub = credit_card()
        card = VGroup(box, n1, n2, sub).move_to([0, 0.3, 0])
        n2.set_opacity(0)
        self.play(FadeIn(box), FadeIn(n1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("torsten wiesel")
        self.play(n2.animate.set_opacity(1), FadeIn(sub), run_time=0.6)
        nr = neuron(NR_C, NR_S)
        small = compact_card()
        self.at("measured")
        self.play(FadeOut(card, scale=0.6), FadeIn(small, scale=1.6), FadeIn(nr), run_time=1.0)
        lab = T("one cortical cell", 28, TEXT).move_to([3.7, -0.2, 0])
        self.at("one cell at a time")
        soma = nr[2]
        ring = Circle(radius=0.85, stroke_color=TEXT, stroke_width=5).move_to(soma.get_center())
        self.play(Create(ring), FadeIn(lab, shift=LEFT * 0.1), run_time=0.7)
        self.play(Flash(soma, color=TEXT, flash_radius=1.1, line_length=0.25), run_time=0.6)
        self.finish()


N15_C, N15_S = (2.4, -0.9), 1.15


class S15(SpokenScene):
    def construct(self):
        n_old = neuron(NR_C, NR_S)
        n_new = neuron(N15_C, N15_S)
        small = compact_card()
        ring = Circle(radius=0.85, stroke_color=TEXT, stroke_width=5).move_to(n_old[2].get_center())
        lab = T("one cortical cell", 28, TEXT).move_to([3.7, -0.2, 0])
        self.add(small, n_old, ring, lab)
        tip = np.array([1.9, -1.4, 0])
        elec = VGroup(Line([-3.8, -3.6, 0], tip, color=TEXT, stroke_width=7), Dot(tip, radius=0.1, color=TEXT))
        self.play(ReplacementTransform(n_old, n_new), FadeOut(ring), FadeOut(lab), FadeOut(small), run_time=0.8)
        lab2 = T("extracellular\nsingle-unit\nrecording", 28, TEXT, line_spacing=0.9).move_to([-3.4, -0.3, 0])
        self.at("electrode")
        self.play(Create(elec[0]), FadeIn(elec[1]), FadeIn(lab2, shift=RIGHT * 0.1), run_time=0.9)
        # first spike straight after the electrode lands
        sp_list = [0.05] + [x for x in poisson(7.0, 11) if x > 0.2]
        tr = trace(-4.6, 6.4, 2.45, 1.0, sp_list, TEXT, 6)
        spl = T("spikes", 32, TEXT, weight=BOLD).move_to([-5.6, 2.45, 0])
        self.at("next to")
        run = 4.0
        flashes = []
        prev = 0.0
        for sfrac in sp_list:
            t_sp = sfrac * run
            flashes += [Wait(max(0.01, t_sp - prev)),
                        AnimationGroup(Indicate(n_new[2], color=GOLD, scale_factor=1.35, run_time=0.18),
                                       Flash(elec[1], color=GOLD, flash_radius=0.55, line_length=0.15, run_time=0.18))]
            prev = t_sp + 0.18
        self.play(Create(tr, rate_func=linear, run_time=run), FadeIn(spl), Succession(*flashes))
        self.finish()


class S16(SpokenScene):
    def construct(self):
        eR = make_eye(ORANGE, 0.75).move_to([-4.3, 1.5, 0])
        eL = make_eye(BLUE, 0.75).move_to([-4.3, -1.5, 0])
        tR = T("right eye", 24, ORANGE).move_to([-4.3, 0.7, 0])
        tL = T("left eye", 24, BLUE).move_to([-4.3, -0.7, 0])
        cell = cell_dot(GREY, 0.8, 0.25, 4).move_to([-0.5, 0, 0])
        aR = arr([-3.45, 1.3, 0], [-1.1, 0.5, 0], ORANGE, 8, tip=0.22)
        aL = arr([-3.45, -1.3, 0], [-1.1, -0.5, 0], BLUE, 8, tip=0.22)
        scR = RoundedRectangle(corner_radius=0.12, width=1.1, height=1.7, stroke_color=GREY, stroke_width=3,
                               fill_color=BG, fill_opacity=1).move_to([-6.15, 1.5, 0])
        scL = scR.copy().move_to([-6.15, -1.5, 0])
        barR = Rectangle(width=0.3, height=1.2, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(scR)
        barL = barR.copy().move_to(scL)
        barR.set_opacity(0)
        barL.set_opacity(0)
        lR = T("right eye", 28, ORANGE).move_to([1.15, 1.5, 0])
        lL = T("left eye", 28, BLUE).move_to([1.15, -1.5, 0])
        # both baselines from the start (flat), the spiking traces draw over them
        baseR = trace(2.3, 6.5, 1.5, 0.9, [], ORANGE, 5)
        baseL = trace(2.3, 6.5, -1.5, 0.9, [], BLUE, 5)
        self.play(FadeIn(VGroup(eR, eL, tR, tL, cell, aR, aL, scR, scL, lR, lL, baseR, baseL)), run_time=0.8)
        an = T("animal anesthetized", 26, GREY).move_to([0.2, 3.45, 0])
        self.at("anesthetized")
        self.play(FadeIn(an, shift=DOWN * 0.1), run_time=0.4)
        # the cover: one grey box with an X, fully in place on the left eye before the bar is shown
        patch = VGroup(RoundedRectangle(corner_radius=0.15, width=1.9, height=1.05, stroke_color=TEXT, stroke_width=3,
                                        fill_color="#3a404d", fill_opacity=1),
                       Line([-0.45, -0.28, 0], [0.45, 0.28, 0], color=TEXT, stroke_width=5),
                       Line([-0.45, 0.28, 0], [0.45, -0.28, 0], color=TEXT, stroke_width=5)).move_to(eL)
        self.at("they showed")
        self.play(FadeIn(patch), aL.animate.set_opacity(0.2), run_time=0.4)
        self.at("bar of light")
        self.play(barR.animate.set_opacity(1), Flash(barR, color=TEXT, flash_radius=0.9, line_length=0.2), run_time=0.6)
        trR = trace(2.3, 6.5, 1.5, 0.9, poisson(8.0, 3), ORANGE, 5)
        trL = trace(2.3, 6.5, -1.5, 0.9, poisson(8.0, 8), BLUE, 5)
        self.at("to one eye")
        self.play(Indicate(aR, color=ORANGE, scale_factor=1.1, run_time=0.6), Create(trR, rate_func=linear, run_time=1.4))
        self.at("with the other")
        self.play(Indicate(patch, color=TEXT, scale_factor=1.08), run_time=0.6)
        self.at("they switched")
        self.play(patch.animate.move_to(eR), aR.animate.set_opacity(0.2), aL.animate.set_opacity(1),
                  barR.animate.set_opacity(0), barL.animate.set_opacity(1), run_time=0.5)
        self.play(Create(trL, rate_func=linear, run_time=1.2), Indicate(aL, color=BLUE, scale_factor=1.1, run_time=0.6))
        self.play(recolor(cell, PURPLE, 0.85), run_time=0.3)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        rects, nums = big_boxes()
        title = T("ocular dominance groups", 38, TEXT, font=TITLE_FONT).move_to([CX, 3.2, 0])
        self.play(LaggedStart(*[FadeIn(VGroup(r, n), shift=UP * 0.15) for r, n in zip(rects, nums)], lag_ratio=0.18), run_time=1.5)
        self.at("ocular dominance")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


def big_state():
    rects, nums = big_boxes()
    title = T("ocular dominance groups", 38, TEXT, font=TITLE_FONT).move_to([CX, 3.2, 0])
    return rects, nums, title


LAB_Y = BIG_Y - BIG_H / 2 - 0.55


class S18(SpokenScene):
    def construct(self):
        rects, nums, title = big_state()
        self.add(rects, nums, title)
        f1, f7 = split_fill(0, 1.0), split_fill(6, 0.0)
        self.at("answers only")
        self.play(FadeIn(f1), run_time=0.6)
        l1 = T("contralateral\neye only", 26, ORANGE, line_spacing=0.9).move_to([HX[0], LAB_Y, 0])
        self.at("contralateral eye")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("group 7")
        self.play(Indicate(nums[6], color=BLUE, scale_factor=1.2), run_time=0.6)
        self.at("answers only", nth=1)
        self.play(FadeIn(f7), run_time=0.6)
        l7 = T("ipsilateral\neye only", 26, BLUE, line_spacing=0.9).move_to([HX[6], LAB_Y, 0])
        self.at("ipsilateral eye")
        self.play(FadeIn(l7, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        rects, nums, title = big_state()
        f1, f7 = split_fill(0, 1.0), split_fill(6, 0.0)
        l1 = T("contralateral\neye only", 26, ORANGE, line_spacing=0.9).move_to([HX[0], LAB_Y, 0])
        l7 = T("ipsilateral\neye only", 26, BLUE, line_spacing=0.9).move_to([HX[6], LAB_Y, 0])
        self.add(rects, f1, f7, nums, title, l1, l7)
        self.play(FadeOut(l1), FadeOut(l7), run_time=0.4)
        self.at("about equally")
        f4 = split_fill(3, 0.5)
        self.play(FadeIn(f4), run_time=0.7)
        both = T("both, equally", 26, PURPLE).move_to([HX[3], LAB_Y, 0])
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.4)
        self.at("the groups between")
        mids = [split_fill(i, FRAC[i]) for i in (1, 2, 4, 5)]
        self.play(LaggedStart(*[FadeIn(m) for m in mids], lag_ratio=0.2), FadeOut(both), run_time=0.8)
        favor = T("favor one eye,\nmore or less", 26, TEXT, line_spacing=0.9).move_to([CX, LAB_Y, 0])
        self.at("favor one eye")
        self.play(FadeIn(favor, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---- the worked cells (s20, s21): eye icons, big traces, readable group boxes
Y_OR, Y_BL = 2.4, 0.55
AMP = 1.25
TX0, TX1 = -4.4, 6.4
CELL_P = np.array([-1.0, -1.2, 0.0])


def ex_labels():
    eo = make_eye(ORANGE, 0.42).move_to([-5.9, Y_OR + 0.1, 0])
    eb = make_eye(BLUE, 0.42).move_to([-5.9, Y_BL + 0.1, 0])
    lo = T("right eye", 24, ORANGE).move_to([-5.9, Y_OR - 0.45, 0])
    lb = T("left eye", 24, BLUE).move_to([-5.9, Y_BL - 0.45, 0])
    tl = VGroup(T("time", 26, GREY), Arrow([0, 0, 0], [1.6, 0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18))
    tl.arrange(RIGHT, buff=0.15).move_to([5.3, -0.1, 0])
    return eo, eb, lo, lb, tl


def ex_traces(orange_active, seed_o=2, seed_b=5):
    tr = trace(TX0, TX1, Y_OR, AMP, poisson(11.0, seed_o) if orange_active else [], ORANGE, 5)
    tb = trace(TX0, TX1, Y_BL, AMP, [] if orange_active else poisson(11.0, seed_b), BLUE, 5)
    return tr, tb


def dot_in_box(i, col):
    return cell_dot(col, 0.28, 0.9, 2).move_to(mid_center(i) + RIGHT * 0.42)


def test_ring(eye, lab):
    """white frame around the eye that is being tested"""
    return RoundedRectangle(corner_radius=0.12, width=1.6, height=1.15, stroke_color=TEXT, stroke_width=4).move_to(
        VGroup(eye, lab).get_center())


class S20(SpokenScene):
    def construct(self):
        rects, nums, title = big_state()
        f1, f7 = split_fill(0, 1.0), split_fill(6, 0.0)
        mids = [split_fill(i, FRAC[i]) for i in (1, 2, 3, 4, 5)]
        favor = T("favor one eye,\nmore or less", 26, TEXT, line_spacing=0.9).move_to([CX, LAB_Y, 0])
        self.add(rects, f1, f7, *mids, nums, title, favor)
        srects, snums = mid_boxes()
        eo, eb, lo, lb, tl = ex_labels()
        tr, tb = ex_traces(True)
        self.play(FadeOut(title), FadeOut(favor), FadeOut(f1), FadeOut(f7), *[FadeOut(m) for m in mids],
                  Transform(rects, srects), Transform(nums, snums),
                  FadeIn(VGroup(eo, eb, lo, lb, tl)), run_time=0.9)
        ring = test_ring(eo, lo)
        self.at("fires to the right eye")
        self.play(FadeIn(ring, run_time=0.2), Create(tr, rate_func=linear, run_time=1.4))
        self.at("not at all")
        self.play(ring.animate.move_to(test_ring(eb, lb).get_center()), run_time=0.25)
        self.play(Create(tb, rate_func=linear), run_time=0.85)
        cell = cell_dot(ORANGE, 0.6, 0.85).move_to(CELL_P)
        self.at("that puts")
        self.play(FadeIn(cell, scale=0.5), FadeOut(ring), run_time=0.4)
        self.at("group one")
        self.play(cell.animate.move_to(mid_center(0) + RIGHT * 0.42).scale(0.28 / 0.6), rects[0].animate.set_fill(ORANGE, 0.55), run_time=0.7)
        self.finish()


def ex_state_s20():
    rects, nums = mid_boxes()
    rects[0].set_fill(ORANGE, 0.55)
    eo, eb, lo, lb, tl = ex_labels()
    tr, tb = ex_traces(True)
    d1 = dot_in_box(0, ORANGE)
    return rects, nums, eo, eb, lo, lb, tl, tr, tb, d1


def unresp_tray():
    tray = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.8, height=1.55, stroke_color=RED, stroke_width=3)
                          .move_to([1.0, CELL_P[1] - 0.05, 0]), num_dashes=56)
    ulab = T("unresponsive", 30, RED, weight=BOLD).move_to([2.2, CELL_P[1] - 0.05, 0])
    return tray, ulab


class S21(SpokenScene):
    def construct(self):
        rects, nums, eo, eb, lo, lb, tl, tr, tb, d1 = ex_state_s20()
        self.add(rects, nums, eo, eb, lo, lb, tl, tr, tb, d1)
        tr2, tb2 = trace(TX0, TX1, Y_OR, AMP, [], ORANGE, 5), trace(TX0, TX1, Y_BL, AMP, poisson(11.0, 5), BLUE, 5)
        ringR, ringL = test_ring(eo, lo), test_ring(eb, lb)
        self.at("fires")
        self.play(FadeOut(tr), FadeOut(tb), run_time=0.3)
        self.at("only to the left")
        self.play(FadeIn(ringR, run_time=0.15), Create(tr2, rate_func=linear, run_time=0.55))
        self.play(FadeOut(ringR, run_time=0.15), FadeIn(ringL, run_time=0.15), Create(tb2, rate_func=linear, run_time=0.65))
        cell = cell_dot(BLUE, 0.6, 0.85).move_to(CELL_P)
        self.at("goes in")
        self.play(FadeIn(cell, scale=0.5), FadeOut(ringL), run_time=0.4)
        self.at("group 7")
        self.play(cell.animate.move_to(mid_center(6) + RIGHT * 0.42).scale(0.28 / 0.6), rects[6].animate.set_fill(BLUE, 0.55), run_time=0.7)
        flat_o, flat_b = trace(TX0, TX1, Y_OR, AMP, [], ORANGE, 5), trace(TX0, TX1, Y_BL, AMP, [], BLUE, 5)
        sil = cell_dot(GREY, 0.6, 0.25, 4).move_to(CELL_P)
        flatlab = T("both traces flat", 28, GREY).move_to(CELL_P + DOWN * 0.0 + RIGHT * 2.45)
        self.at("no eye can drive")
        self.play(FadeOut(tr2), FadeOut(tb2), FadeIn(ringR, run_time=0.15), run_time=0.25)
        self.play(Create(flat_o, rate_func=linear, run_time=0.4), FadeIn(sil, scale=0.5), run_time=0.4)
        self.play(FadeOut(ringR, run_time=0.1), FadeIn(ringL, run_time=0.1), Create(flat_b, rate_func=linear, run_time=0.4), FadeIn(flatlab), run_time=0.4)
        tray, ulab = unresp_tray()
        self.at("counted as")
        self.play(FadeIn(tray), FadeIn(ulab), FadeOut(flatlab), FadeOut(ringL), sil.animate.set_stroke(RED).set_fill(RED, 0.3), run_time=1.0)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        rects, nums, eo, eb, lo, lb, tl, tr, tb, d1 = ex_state_s20()
        rects[6].set_fill(BLUE, 0.5)
        d7 = dot_in_box(6, BLUE)
        flat_o, flat_b = trace(TX0, TX1, Y_OR, AMP, [], ORANGE, 5), trace(TX0, TX1, Y_BL, AMP, [], BLUE, 5)
        sil = cell_dot(RED, 0.6, 0.3, 4).move_to(CELL_P)
        tray, ulab = unresp_tray()
        old = VGroup(eo, eb, lo, lb, tl, flat_o, flat_b, d1, d7, sil, tray, ulab)
        self.add(rects, nums, old)
        ax = axes()
        srects, snums = small_boxes()
        self.play(FadeOut(old), Transform(rects, srects), Transform(nums, snums), FadeIn(ax), FadeIn(T("15 cells", 30, GOLD, weight=BOLD).move_to([5.6, 3.5, 0])), run_time=0.6)
        seen = [0] * 7
        cells, anims = [], []
        for g in ORDER:
            i = g - 1
            c = cell_dot(gcol(i), 0.36, 0.85, 2).move_to([HX[i], 3.0, 0])
            c.set_opacity(0)
            tgt = [HX[i], YB + (seen[i] + 0.5) * UNIT, 0]
            seen[i] += 1
            cells.append(c)
            anims.append(c.animate.move_to(tgt).set_fill(opacity=0.85).set_stroke(opacity=1))
        self.add(*cells)
        self.at("in each group")
        self.play(LaggedStart(*anims, lag_ratio=0.22), run_time=2.2)
        bars = hist_bars()
        ttl = hist_title("ocular dominance histogram")
        self.at("histogram")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(ttl),
                  *[c.animate.set_opacity(0) for c in cells], run_time=1.0)
        self.finish()


def final_hist():
    srects, snums = small_boxes()
    bars = hist_bars()
    return srects, snums, bars, axes()


class S23(SpokenScene):
    def construct(self):
        srects, snums, bars, ax = final_hist()
        ttl = hist_title("ocular dominance histogram")
        total = T("15 cells", 30, GOLD, weight=BOLD).move_to([5.6, 3.5, 0])
        self.add(srects, snums, bars, ax, ttl, total)
        ttl2 = hist_title()
        self.at("normal adult")
        self.play(ReplacementTransform(ttl, ttl2), run_time=0.6)
        curve = hump()
        self.at("a hump")
        self.play(Create(curve), run_time=1.3)
        yb_ = YB + 4.0 * UNIT + 0.2
        brace = Brace(Line([HX[1] - BW / 2, yb_, 0], [HX[4] + BW / 2, yb_, 0]), UP, color=TEXT, buff=0.0)
        mid = T("middle groups", 26, TEXT).next_to(brace, UP, buff=0.1)
        self.at("middle groups")
        self.play(GrowFromCenter(brace), FadeIn(mid, shift=DOWN * 0.1), run_time=0.9)
        arrow = arr([6.2, 0.55, 0], [3.35, 0.55, 0], ORANGE, 9, tip=0.3)
        lab = T("leans toward the\ncontralateral side", 26, ORANGE, line_spacing=0.9).move_to([4.8, 1.55, 0])
        self.at("leaning toward")
        self.play(GrowArrow(arrow), FadeIn(lab, shift=DOWN * 0.1), run_time=0.9)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        tk = T("Takeaway", 36, GOLD, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeIn(tk), run_time=0.4)
        eo = make_eye(ORANGE, 0.5).move_to([-5.9, 1.2, 0])
        eb = make_eye(BLUE, 0.5).move_to([-5.9, -1.2, 0])
        lR = T("right eye", 26, ORANGE).move_to([-5.9, 1.85, 0])
        lL = T("left eye", 26, BLUE).move_to([-5.9, -1.85, 0])
        lo = arr([-5.1, 1.2, 0], [3.4, 0.3, 0], ORANGE, 8, tip=0.26)
        lb = arr([-5.1, -1.2, 0], [3.4, -0.3, 0], BLUE, 8, tip=0.26)
        br = Brace(Line([-4.6, -1.65, 0], [-0.4, -1.65, 0]), DOWN, color=TEXT, buff=0.0)
        sep = T("separate paths", 30, TEXT).next_to(br, DOWN, buff=0.12)
        self.at("the eye's paths")
        self.play(FadeIn(eo), FadeIn(eb), FadeIn(lR), FadeIn(lL), Create(lo), Create(lb), run_time=1.0)
        self.play(GrowFromCenter(br), FadeIn(sep, shift=UP * 0.1), run_time=0.6)
        box = RoundedRectangle(corner_radius=0.3, width=5.3, height=5.4, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                               fill_opacity=0.07).move_to([4.15, -0.1, 0])
        cl = T("cortex", 30, GREY).move_to([4.15, 2.3, 0])
        self.at("until the cortex")
        self.play(FadeIn(box), FadeIn(cl), run_time=0.7)
        cell = cell_dot(GREY, 0.75, 0.25, 4).move_to([4.15, 0.0, 0])
        self.at("shared cells")
        self.play(FadeIn(cell, scale=0.5), run_time=0.5)
        self.bring_to_front(lo, lb)
        sh = T("shared cell", 28, PURPLE).move_to([4.15, -1.35, 0])
        self.at("driven by both")
        self.play(recolor(cell, PURPLE, 0.85), Flash(cell, color=PURPLE, flash_radius=1.1, line_length=0.25), FadeIn(sh, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        srects, snums, bars, ax = final_hist()
        curve = hump()
        ttl = hist_title()
        total = T("15 cells", 30, GOLD, weight=BOLD).move_to([5.6, 3.5, 0])
        self.add(srects, snums, bars, ax, curve, ttl, total)
        q = T("?", 120, GOLD, weight=BOLD).move_to([5.2, 0.55, 0])
        self.at("what sets")
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        eye = make_eye(TEXT, 0.6).move_to([5.2, 2.35, 0])
        self.at("closes one eye")
        self.play(FadeIn(eye), run_time=0.4)
        cap = T("one eye closed", 24, TEXT).move_to([5.2, 1.7, 0])
        self.play(*eye_close(eye), FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        bal = DoubleArrow([-3.0, 2.85, 0], [1.6, 2.85, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25)
        bl = T("balance", 26, GREY).move_to([3.2, 2.85, 0])
        self.at("watches the balance")
        self.play(GrowFromCenter(bal), FadeIn(bl), run_time=0.7)
        self.play(Rotate(bal, angle=0.12, rate_func=there_and_back, run_time=1.0))
        self.finish()


class S26End(EndCard):
    LINE = "The eyes' paths stay apart until the cortex, where cells hear both."
