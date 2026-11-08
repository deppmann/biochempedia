"""Delete One, Count the Survivors (chapter 4 of "Neurotrophins, Trk Receptors and p75")

COLOR MAP (shared with every chapter of this lesson; taken from scenes.old.py)
  BLUE   = the neurotrophins (NGF, BDNF, NT-3, NT-4): their name tags
  PINK   = Trk receptors (TrkA, TrkB, TrkC) and the TrkA-null mouse (graph line, bar, tag)
  GREEN  = survival: the wild type (control) line and bars
  RED    = loss and death: lost neurons, dying cells, the shaded gap between the lines
  GREY   = outlines, mice, cells, ganglion outlines, neurons, axes (LG = lighter grey for small text)
  TEXT   = labels, the question, the "lose" down-arrow
  (ORANGE, TEAL, YELLOW, VIOLET are used here only to tell the four rows of the final grid apart:
   NGF/TrkA orange, BDNF teal, NT-4 yellow, NT-3/TrkC violet. They keep their other meanings
   in the other chapters.)

Every shape is a labelled cartoon: no molecular structures. Curves come from the lesson's numbers
(about 15% fewer at E15.5, 35% at E17.5, 50% at birth, nearly all gone at P9). The wild type is the
100% line; the E13.5 point is "normal"; the P9 value (3%) is drawn as "nearly zero", not measured,
and the line from birth to P9 is dashed because the lesson gives only those two points.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
VIOLET = "#A98BE0"
ORANGE = "#F29E4C"
BRIGHT = "#DDE2EA"
LG = "#B9BFCB"          # lighter grey for ticks, axis titles, citations
ROWCOL = [ORANGE, TEAL, YELLOW, VIOLET]


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def lab(text, color, x, y, size=26, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def dashed_arrow(a, b, color=BLUE, w=4):
    a, b = np.array(a, float), np.array(b, float)
    u = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - u * 0.15, color=color, stroke_width=w, dash_length=0.18, dashed_ratio=0.55)
    tip = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.14)
    tip.rotate(angle_of_vector(u) - PI / 2).move_to(b - u * 0.1)
    return VGroup(line, tip)


def cross(center, size=0.5, color=RED, w=9):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - size, cy - size, 0], [cx + size, cy + size, 0], color=color, stroke_width=w),
                  Line([cx - size, cy + size, 0], [cx + size, cy - size, 0], color=color, stroke_width=w))


def mouse(s=1.0, legs="normal", color=GREY):
    """A side-view mouse cartoon with legs, facing right, centred on its body. legs: 'normal' or 'awkward'."""
    st = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    body = Ellipse(width=1.5 * s, height=0.9 * s, **st)
    head = Ellipse(width=0.85 * s, height=0.65 * s, **st).move_to([0.95 * s, 0.0, 0])
    ear = Circle(radius=0.22 * s, **st).move_to([0.8 * s, 0.42 * s, 0])
    eye = Dot([1.12 * s, 0.1 * s, 0], radius=0.05 * s, color=TEXT)
    nose = Dot([1.4 * s, -0.02 * s, 0], radius=0.06 * s, color=TEXT)
    tail = ArcBetweenPoints([-0.72 * s, 0.0, 0], [-1.5 * s, 0.5 * s, 0], angle=-PI / 2,
                            stroke_color=color, stroke_width=4)

    def leg(pts, w=6, op=1.0):
        m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op)
        m.set_points_as_corners([[x * s, y * s, 0] for x, y in pts])
        return m
    if legs == "normal":
        L = [leg([(0.5, -0.35), (0.55, -0.85)]), leg([(-0.5, -0.35), (-0.55, -0.85)]),
             leg([(0.3, -0.38), (0.33, -0.82)], 5, 0.55), leg([(-0.3, -0.38), (-0.33, -0.82)], 5, 0.55)]
    elif legs == "bent":
        L = [leg([(0.5, -0.35), (0.75, -0.62), (0.6, -0.9)]), leg([(-0.5, -0.35), (-0.78, -0.6), (-0.6, -0.9)]),
             leg([(0.3, -0.38), (0.5, -0.62), (0.38, -0.88)], 5, 0.55), leg([(-0.3, -0.38), (-0.55, -0.62), (-0.4, -0.88)], 5, 0.55)]
    else:
        L = [leg([(0.5, -0.35), (1.15, -0.45)]), leg([(-0.5, -0.35), (-1.05, -0.55), (-0.8, -0.95)]),
             leg([(0.3, -0.38), (0.45, -0.2), (0.85, -0.1)], 5, 0.55),
             leg([(-0.3, -0.38), (-0.7, -0.7), (-0.35, -0.95)], 5, 0.55)]
    return VGroup(*L, tail, body, head, ear, eye, nose)


def ganglion(cx, cy, w, h, n, r=0.17, color=GREY):
    """An outlined ganglion with n neuron dots laid out evenly (sunflower pattern). Returns (outline, dots)."""
    out = Ellipse(width=w, height=h, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.1)
    out.move_to([cx, cy, 0])
    dots = []
    for i in range(n):
        rr = np.sqrt((i + 0.5) / n) * 0.82
        a = i * 2.39996
        dots.append(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.55)
                    .move_to([cx + rr * np.cos(a) * w / 2, cy + rr * np.sin(a) * h / 2, 0]))
    return out, dots


def ghost(c):
    """A dashed red outline where a neuron used to be."""
    return DashedVMobject(Circle(radius=c.width / 2, stroke_color=RED, stroke_width=2, fill_opacity=0)
                          .move_to(c.get_center()), num_dashes=8)


def receptor_cell(cx, cy, r, broken=False):
    """A cell with three round-tipped TrkA receptors on its surface. broken: gapped stalk, dashed tip."""
    cell = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([cx, cy, 0])
    recs = []
    for deg in (55, 90, 125):
        a = np.radians(deg)
        u = np.array([np.cos(a), np.sin(a), 0.0])
        base = np.array([cx, cy, 0.0]) + u * r
        if broken:
            s1 = Line(base, base + u * 0.28, color=PINK, stroke_width=6)
            s2 = Line(base + u * 0.62, base + u * 0.85, color=PINK, stroke_width=6, stroke_opacity=0.5)
            tip = DashedVMobject(Ellipse(width=0.8, height=0.8, stroke_color=PINK, stroke_width=3, fill_opacity=0)
                                 .move_to(base + u * 1.25), num_dashes=10)
            recs.append(VGroup(s1, s2, tip, cross(base + u * 1.25, 0.3, RED, 6)))
        else:
            stalk = Line(base, base + u * 0.85, color=PINK, stroke_width=6)
            tip = Ellipse(width=0.8, height=0.8, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                          fill_opacity=0.5).move_to(base + u * 1.25)
            recs.append(VGroup(stalk, tip))
    return cell, VGroup(*recs)


def countdown(sc, seconds, label, x=1.5, y=-2.3, width=8.0):
    """A quiet 'think now' cue: a bar that drains over `seconds`. Returns the cue's mobjects."""
    tr = ValueTracker(0.0)
    bar = always_redraw(lambda: Rectangle(width=max(width * (1 - tr.get_value()), 0.01), height=0.2, stroke_width=0,
                                          fill_color=YELLOW, fill_opacity=0.85)
                        .move_to([x - width / 2 + max(width * (1 - tr.get_value()), 0.01) / 2, y, 0]))
    track = Rectangle(width=width, height=0.2, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, y, 0])
    txt = lab(label, YELLOW, x, y + 0.55, 30)
    sc.add(track, bar, txt)
    sc.play(tr.animate.set_value(1.0), run_time=seconds, rate_func=linear)
    return track, bar, txt


# ---------------------------------------------------------------------------------------------
# the survival graph (TrkA-null sympathetic ganglion against wild type)
# ---------------------------------------------------------------------------------------------
DAYS = [0, 2, 4, 6, 15]                 # days after E13.5: E13.5, E15.5, E17.5, birth (about E19.5), P9
TICKS = ["E13.5", "E15.5", "E17.5", "birth", "P9"]
MUT = [100, 85, 65, 50, 3]              # TrkA-null cells, percent of wild type


class Graph:
    def __init__(self, ox=-4.3, oy=-2.45, sx=0.68, sy=0.047, compact=False):
        ytop = 106 if compact else 112
        self.ox, self.oy, self.sx, self.sy = ox, oy, sx, sy
        ax = ox - 0.6
        self.ax = ax
        self.yaxis = Line([ax, oy, 0], [ax, self.py(ytop), 0], color=GREY, stroke_width=3)
        xend = self.px(4) + 0.5
        self.xaxis = Line([ax, oy, 0], [xend, oy, 0], color=GREY, stroke_width=3)
        ys = VGroup()
        for p, txt in ((0, "0"), (50, "50%"), (100, "100%")):
            ys.add(T(txt, 26, LG).next_to([ax - 0.08, self.py(p), 0], LEFT, buff=0.1))
        self.ylabs = ys
        if compact:
            self.ylabel = T("% of wild type", 26, LG).rotate(PI / 2).move_to([ax - 1.45, self.py(50), 0])
            self.xtitle = T("age (embryonic day E)", 26, LG).move_to([(ax + xend) / 2, oy - 1.3, 0])
        else:
            self.ylabel = T("cells, % of wild type", 26, LG).rotate(PI / 2).move_to([ax - 1.75, self.py(50) + 0.25, 0])
            self.xtitle = T("age (embryonic day E, postnatal day P)", 26, LG).move_to([(ax + xend) / 2, oy - 1.05, 0])
        xt = VGroup()
        for i in range(5):
            tk = Line([self.px(i), oy - 0.09, 0], [self.px(i), oy + 0.09, 0], color=GREY, stroke_width=3)
            row = -0.42
            if compact and i in (1, 2):
                xt.add(VGroup(tk))
                continue
            xt.add(VGroup(tk, T(TICKS[i], 26 if not compact else 22, LG).move_to([self.px(i), oy + row, 0])))
        self.xticks = xt
        wt = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=GREEN, stroke_width=6), T("wild type", 26, GREEN)).arrange(RIGHT, buff=0.15)
        nl = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=PINK, stroke_width=6), T("TrkA-null", 26, PINK)).arrange(RIGHT, buff=0.15)
        self.legend = VGroup(wt, nl).arrange(RIGHT, buff=0.6).move_to([3.7, 3.4, 0])
        self.cite = T("Fagan and colleagues, 1996", 26, LG).move_to([-4.0, 3.4, 0]).align_to([-6.55, 0, 0], LEFT)
        self.wtlab = T("wild type = 100%", 26, GREEN).move_to([3.7, self.py(100) + 0.42, 0])
        self.cline = Line(self.pt(0, 100), self.pt(4, 100), color=GREEN, stroke_width=6)
        self.cseg = [Line(self.pt(i, 100), self.pt(i + 1, 100), color=GREEN, stroke_width=6) for i in range(4)]
        self.mseg = [Line(self.pt(i, MUT[i]), self.pt(i + 1, MUT[i + 1]), color=PINK, stroke_width=6) for i in range(3)]
        # birth to P9: only two points are given, so the join is dashed and lighter
        self.mseg.append(DashedLine(self.pt(3, MUT[3]), self.pt(4, MUT[4]), color=PINK, stroke_width=5,
                                    dash_length=0.22, dashed_ratio=0.6).set_stroke(opacity=0.6))
        self.cdot0 = Dot(self.pt(0, 100), radius=0.17, color=GREEN)
        self.mdot = [Dot(self.pt(i, MUT[i]), radius=0.1 if i == 0 else 0.12, color=PINK) for i in range(5)]
        pts = [self.pt(i, 100) for i in range(5)] + [self.pt(i, MUT[i]) for i in range(4, -1, -1)]
        self.shade = Polygon(*pts, stroke_width=0, fill_color=RED, fill_opacity=0.22)

    def px(self, i):
        return self.ox + self.sx * DAYS[i]

    def py(self, p):
        return self.oy + self.sy * p

    def pt(self, i, p):
        return np.array([self.px(i), self.py(p), 0.0])

    def base(self, cite=True, legend=True, ticks=True):
        out = [self.yaxis, self.xaxis, self.ylabs, self.ylabel, self.xtitle]
        if ticks:
            out.append(self.xticks)
        if legend:
            out.append(self.legend)
        if cite:
            out.append(self.cite)
        return out

    def data(self, k):
        """lines and dots up to age index k (k = 0: only the E13.5 dots)."""
        out = []
        for i in range(k):
            out += [self.cseg[i], self.mseg[i]]
        out.append(self.cdot0)
        out += self.mdot[:k + 1]
        if k >= 1:
            out.append(self.wtlab)
        return out

    def lost_label(self, text, i):
        """a red label under the curve with a dotted leader to the data point."""
        p = self.pt(i, MUT[i])
        spots = {1: (p[0] - 0.55, 0.35), 2: (p[0] + 0.1, -0.95), 3: (p[0] + 1.2, -1.75), 4: (p[0] - 0.4, -1.0)}
        x, y = spots[i]
        t = T(text, 26, RED, line_spacing=0.8).move_to([x, y, 0])
        if i == 3:
            ldr = DashedLine([p[0] + 0.05, p[1] - 0.15, 0], [x - 0.75, y + t.height / 2 + 0.05, 0],
                             color=LG, stroke_width=2, dash_length=0.1)
        elif i == 4:
            ldr = DashedLine([p[0], p[1] + 0.14, 0], [p[0], y - t.height / 2 - 0.05, 0], color=LG, stroke_width=2, dash_length=0.1)
        else:
            ldr = DashedLine([p[0], p[1] - 0.15, 0], [p[0], y + t.height / 2 + 0.05, 0], color=LG, stroke_width=2, dash_length=0.1)
        return VGroup(ldr, t)


def lost_labels(g, upto):
    texts = {1: "about 15%\nfewer", 2: "about 35%\nfewer", 3: "about 50% fewer", 4: "nearly all\ngone"}
    return [g.lost_label(texts[i], i) for i in range(1, upto + 1)]


# ---------------------------------------------------------------------------------------------
# the grid (genotype rows by neuron-population columns)
# ---------------------------------------------------------------------------------------------
GCOLS = ["sympathetic", "pain and heat\n(small\nsensory)", "vestibular", "nodose-\npetrosal",
         "proprioceptive\n(limb position)"]
GROWS = ["NGF or\nTrkA", "BDNF", "NT-4", "NT-3 or\nTrkC"]
CX = [-4.2, -1.75, 0.3, 2.5, 5.2]
CW = [1.7, 2.3, 1.5, 2.6, 2.4]
RY = [0.85, -0.2, -1.25, -2.3]
RLX = -5.9
HY = 2.05          # header text
BANY = 3.55        # "neurons lost" banner
ICY = 3.42         # icon row
ICW = 2.88          # icon word row
KEYY = -3.45
ZS, ZA, ZD = 1.35, np.array([-6.6, 1.0, 0.0]), np.array([1.8, -1.4, 0.0])   # zoomed view for the first two rows


def canal_icon():
    """a semicircular-canal loop (balance): a looped tube with a swelling at its base, plus a second loop."""
    a = Arc(radius=0.3, start_angle=-PI / 3, angle=PI * 5 / 3, stroke_color=TEXT, stroke_width=5)
    b = Arc(radius=0.2, start_angle=PI, angle=-PI * 4 / 3, stroke_color=TEXT, stroke_width=5).move_to([0.32, -0.12, 0])
    amp = Dot([0.3 * np.cos(-PI / 3), 0.3 * np.sin(-PI / 3), 0], radius=0.09, color=TEXT)
    return VGroup(a, b, amp)


def heart_icon():
    return ParametricFunction(lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t)
                                                  - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) * 0.021,
                              t_range=[0, TAU, 0.05], stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.35)


def lung_icon():
    st = dict(stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3)
    trachea = Line([0, 0.3, 0], [0, 0.05, 0], color=TEXT, stroke_width=4)
    return VGroup(Ellipse(width=0.28, height=0.5, **st).move_to([-0.19, -0.05, 0]),
                  Ellipse(width=0.28, height=0.5, **st).move_to([0.19, -0.05, 0]), trachea)


def gut_icon():
    f = ParametricFunction(lambda t: np.array([t, 0.13 * np.sin(t * 9), 0]), t_range=[-0.4, 0.4, 0.01],
                           color=TEXT, stroke_width=6)
    return f


def limb_icon():
    m = VMobject(stroke_color=TEXT, stroke_width=5)
    m.set_points_as_corners([[-0.3, 0.22, 0], [0.0, 0.0, 0], [0.3, -0.2, 0]])
    return VGroup(m, Dot([0, 0, 0], radius=0.07, color=TEXT), Dot([-0.3, 0.22, 0], radius=0.07, color=TEXT))


def mark_shape(x, y, w, solid, color=RED):
    """a loss mark: outline, fill (half for 'part survives', full for 'nearly all lost') and a down arrow."""
    h = 0.95
    outline = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                               fill_opacity=0).move_to([x, y, 0])
    if solid:
        fill = Rectangle(width=w - 0.06, height=h - 0.06, stroke_width=0, fill_color=color, fill_opacity=0.55).move_to([x, y, 0])
    else:
        fill = Rectangle(width=w - 0.06, height=(h - 0.06) / 2, stroke_width=0, fill_color=color,
                         fill_opacity=0.55).move_to([x, y - (h - 0.06) / 4, 0])
    tri = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.17).rotate(PI).move_to([x, y, 0])
    return VGroup(outline, fill, tri)


class Grid:
    def __init__(self, zoom=False):
        self.zoom = zoom
        self.title = T("mice\nlacking", 26, LG, line_spacing=0.8).move_to([RLX - 0.25, HY, 0])
        self.heads = [T(GCOLS[c], 26, TEXT, line_spacing=0.8).move_to([CX[c], HY + (0.17 if c == 1 else 0), 0]) for c in range(5)]
        self.rl = [T(GROWS[r], 26, TEXT, line_spacing=0.8).move_to([RLX, RY[r], 0]) for r in range(4)]
        self.cell = {(r, c): RoundedRectangle(corner_radius=0.12, width=CW[c], height=0.95, stroke_color=GREY,
                                              stroke_width=2, stroke_opacity=0.6, fill_opacity=0).move_to([CX[c], RY[r], 0])
                     for r in range(4) for c in range(5)}
        self.mark = {}
        for (r, c) in ALLMARKS:
            self.mark[(r, c)] = mark_shape(CX[c], RY[r], CW[c], solid=(r, c) == (0, 0))
        bt = T("neurons lost (fewer)", 28, TEXT)
        btri = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.17).rotate(PI)
        self.banner = VGroup(bt, btri).arrange(RIGHT, buff=0.2).move_to([0, BANY, 0]).align_to([CX[0] - CW[0] / 2, 0, 0], LEFT)

        def icon(ic, word, x):
            return VGroup(ic.scale(1.45).move_to([x, ICY, 0]), T(word, 26, TEXT).move_to([x, ICW, 0]))
        self.icon = {"ear": icon(canal_icon(), "balance", CX[2] + 0.1),
                     "heart": icon(heart_icon(), "heart", CX[3] - 0.75),
                     "lung": icon(lung_icon(), "lungs", CX[3] + 0.35),
                     "gut": icon(gut_icon(), "gut", CX[3] + 1.4),
                     "limb": icon(limb_icon(), "limb", CX[4])}
        if zoom:
            for m in self.everything():
                m.scale(ZS, about_point=ZA).shift(ZD)

    def everything(self):
        out = [self.title, self.banner, *self.heads, *self.rl, *self.cell.values(), *self.mark.values(), *self.icon.values()]
        return out

    def static(self, sc, rows, cols, marks, icons=(), banner=True):
        sc.add(self.title)
        if banner:
            sc.add(self.banner)
        sc.add(*[self.cell[(r, c)] for r in rows for c in cols])
        sc.add(*[self.rl[r] for r in rows], *[self.heads[c] for c in cols])
        sc.add(*[self.mark[m] for m in marks], *[self.icon[i] for i in icons])


ALLMARKS = [(0, 0), (0, 1), (1, 2), (1, 3), (2, 3), (3, 4)]

ST16 = dict(rows=[0], cols=[0], marks=[(0, 0)], icons=[])
ST17 = dict(rows=[0], cols=[0, 1], marks=[(0, 0), (0, 1)], icons=[])
ST18 = dict(rows=[0, 1], cols=[0, 1, 2], marks=[(0, 0), (0, 1), (1, 2)], icons=["ear"])
ST19 = dict(rows=[0, 1], cols=[0, 1, 2, 3], marks=[(0, 0), (0, 1), (1, 2), (1, 3)], icons=["ear", "heart", "lung", "gut"])
ST20 = dict(rows=[0, 1, 2], cols=[0, 1, 2, 3], marks=[(0, 0), (0, 1), (1, 2), (1, 3), (2, 3)],
            icons=["ear", "heart", "lung", "gut"])
ST21 = dict(rows=[0, 1, 2, 3], cols=[0, 1, 2, 3, 4], marks=ALLMARKS, icons=["ear", "heart", "lung", "gut", "limb"])


def gstate(sc, G, st):
    G.static(sc, **st)


def unzoom_anim(mobs):
    """animate the zoomed grid objects back to the normal view."""
    return VGroup(*mobs).animate.shift(-ZD).scale(1 / ZS, about_point=ZA)


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "Delete One, Count the Survivors"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=26, color=LG)
        title = T(self.TITLE, size=58, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        self.add(g)                       # full strength from the first frame
        self.wait(4.0)


class S01(SpokenScene):
    def construct(self):
        c = np.array([-0.9, -0.3, 0.0])
        R = 2.55

        def theta(u):
            return np.radians(80 + 250 * u)

        def wd(u):
            return 1.6 - 1.3 * u ** 2.2

        def pos(u):
            a = theta(u)
            return c + R * np.array([np.cos(a), np.sin(a), 0]), np.array([np.cos(a), np.sin(a), 0])

        outer, inner = [], []
        for k in range(71):
            u = k / 70
            p, d = pos(u)
            outer.append(p + d * wd(u) / 2)
            inner.append(p - d * wd(u) / 2)
        body = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        body.set_points_as_corners(outer + inner[::-1] + [outer[0]])
        p0, _ = pos(0)
        hc = p0 + np.array([0.2, 0.35, 0])
        head = VGroup(Circle(radius=1.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(hc),
                      Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to(hc))
        eye = Dot(hc + np.array([0.45, 0.2, 0]), radius=0.09, color=TEXT)
        pf, df = pos(0.14)
        fore = Ellipse(width=0.7, height=0.32, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        fore.rotate(theta(0.14)).move_to(pf - df * (wd(0.14) / 2 + 0.12))
        ph, dh = pos(0.74)
        hind = Ellipse(width=0.55, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        hind.rotate(theta(0.74)).move_to(ph - dh * (wd(0.74) / 2 + 0.08))
        self.add(fore, hind, body, head, eye)

        def gang(u, side):
            p, d = pos(u)
            q = p + d * side * (wd(u) / 2 - 0.12)
            o, dots = ganglion(q[0], q[1], 1.0, 0.6, 3, r=0.085)
            gr = VGroup(o, *dots)
            gr.rotate(theta(u) + PI / 2)
            return gr, q
        sens = [gang(u, 1) for u in (0.28, 0.40, 0.52, 0.64)]
        symp = [gang(u, -1) for u in (0.34, 0.46, 0.58)]
        allg = [g for g, _ in sens + symp]

        def leader(q, a):
            q = np.array(q)
            a = np.array(a, float)
            u = (a - q) / np.linalg.norm(a - q)
            return Line(a, q + u * 0.55, color=LG, stroke_width=2)
        tag_s = lab("sensory", LG, -6.0, sens[1][1][1] + 0.2, 32)
        tag_y = lab("sympathetic", LG, 3.95, symp[1][1][1] + 0.1, 32)
        ld = [leader(sens[1][1], [-5.1, tag_s.get_center()[1], 0]), leader(symp[1][1], [2.4, tag_y.get_center()[1], 0])]
        self.at("receptor")
        self.play(LaggedStart(*[FadeIn(g) for g in allg], lag_ratio=0.1), run_time=1.0)
        self.play(*[FadeIn(x) for x in (tag_s, tag_y, *ld)], run_time=0.5)
        self.at("which neurons")
        q1 = lab("which neurons?", TEXT, 4.6, 2.9, 40)
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.5)
        self.at("disappear")
        gone = [sens[1][0], symp[1][0]]
        self.play(*[g[1:].animate.set_opacity(0.0) for g in gone],
                  *[g[0].animate.set_stroke(RED, opacity=0.9).set_fill(RED, 0.25) for g in gone], run_time=0.5)
        self.at("and when")
        a = arr([2.8, -2.9, 0], [6.4, -2.9, 0], LG, 6)
        age = lab("age", LG, 4.6, -3.45, 30)
        q2 = lab("when?", TEXT, 4.6, -1.9, 44)
        self.play(GrowArrow(a), FadeIn(age), FadeIn(q2, scale=0.7), run_time=0.7)
        self.finish()


def chromosome():
    cy = -1.0
    bar = RoundedRectangle(corner_radius=0.8, width=12.2, height=1.9, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.22).move_to([0, cy, 0])
    bands = VGroup(*[Line([x, cy - 0.85, 0], [x, cy + 0.85, 0], color=GREY, stroke_width=3, stroke_opacity=0.5)
                     for x in (-4.6, -3.1, -1.6, 4.3, 5.2)])
    gene = Rectangle(width=1.8, height=1.9, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                     fill_opacity=0.6).move_to([1.4, cy, 0])
    return bar, bands, gene


class S02(SpokenScene):
    def construct(self):
        bar, bands, gene = chromosome()
        m = mouse(1.7).move_to([-3.6, 2.15, 0])
        t = lab("knockout mouse", TEXT, 2.3, 2.2, 42)
        self.add(m, t)
        chrom_l = lab("chromosome", LG, -4.6, -2.55, 28)
        glab = lab("one chosen gene", PINK, 1.4, -2.55, 34)
        self.at("one in which")
        self.play(FadeIn(bar), FadeIn(bands), FadeIn(chrom_l), run_time=0.7)
        self.at("chosen gene")
        self.play(FadeIn(gene), FadeIn(glab), run_time=0.5)
        self.at("disrupted")
        x = cross(gene.get_center(), 0.9, RED, 10)
        glab2 = lab("one chosen gene, disrupted", PINK, 1.4, -2.55, 34)
        self.play(Create(x[0]), Create(x[1]), gene.animate.set_fill(PINK, 0.2), ReplacementTransform(glab, glab2),
                  run_time=0.6)
        self.finish()


def s03_cells():
    cell, recs = receptor_cell(0, -0.5, 1.7)
    return cell, recs


class S03(SpokenScene):
    def construct(self):
        cell, recs = s03_cells()
        rl = lab("receptor", PINK, 0, 3.3, 30)
        self.add(cell, recs, rl)
        self.at("no working protein")
        l1 = lab("no working protein", TEXT, 0, -3.0, 30)
        self.play(FadeOut(recs), FadeOut(rl), FadeIn(l1), run_time=0.8)
        self.at("or no working")
        cell2, recs2 = receptor_cell(3.5, -0.5, 1.7, broken=True)
        self.play(VGroup(cell, l1).animate.shift(LEFT * 3.5), FadeIn(cell2), FadeIn(recs2), run_time=0.8)
        self.at("form of one")
        l2 = lab("no working form", TEXT, 3.5, -3.0, 30)
        self.play(FadeIn(l2), run_time=0.5)
        self.finish()


NAMES = [("NGF", BLUE), ("BDNF", BLUE), ("NT-3", BLUE), ("NT-4", BLUE), ("TrkA", PINK), ("TrkB", PINK), ("TrkC", PINK)]
POS = {"NGF": (-4.95, 1.55), "BDNF": (-1.65, 1.55), "NT-3": (1.65, 1.55), "NT-4": (4.95, 1.55),
       "TrkA": (-3.3, -1.55), "TrkB": (0.0, -1.55), "TrkC": (3.3, -1.55)}


def mouse_row():
    """the seven knockout mice with their tags; returns dict name -> (mouse, tag)."""
    out = {}
    for nm, col in NAMES:
        x, y = POS[nm]
        m = mouse(1.05).move_to([x, y, 0])
        tag = T(f"no {nm}", 32, col).move_to([x, y - 1.4, 0])
        out[nm] = (m, tag)
    return out


class S04(SpokenScene):
    def construct(self):
        # carry the two cells from the last scene, then swap them for the mice
        cell, recs = s03_cells()
        cell.shift(LEFT * 3.5)
        cell2, recs2 = receptor_cell(3.5, -0.5, 1.7, broken=True)
        old = VGroup(cell, cell2, recs2, lab("no working protein", TEXT, -3.5, -3.0, 30),
                     lab("no working form", TEXT, 3.5, -3.0, 30))
        self.add(old)
        mice = mouse_row()
        first = [mice[n] for n in ("NGF", "BDNF", "NT-3", "NT-4")]
        second = [mice[n] for n in ("TrkA", "TrkB", "TrkC")]
        self.at("delete each")
        self.play(FadeOut(old), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(VGroup(m, t), shift=UP * 0.15) for m, t in first], lag_ratio=0.25), run_time=1.0)
        self.at("or track")
        self.play(LaggedStart(*[FadeIn(VGroup(m, t), shift=UP * 0.15) for m, t in second], lag_ratio=0.25), run_time=1.0)
        self.at("one at a time")
        self.play(LaggedStart(*[Indicate(t, scale_factor=1.25, color=t.get_color()) for m, t in first + second], lag_ratio=0.3), run_time=1.5)
        self.at("sorts")
        q = lab("which neurons are lost in each?", TEXT, 0, 3.45, 36)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def zoom_bubble():
    bub = Circle(radius=2.7, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([3.7, 0.1, 0])
    o, d = ganglion(3.7, 0.1, 4.0, 2.8, 18, r=0.2)
    return bub, o, d


class S05(SpokenScene):
    def construct(self):
        mice = mouse_row()
        for m, t in mice.values():
            self.add(m, t)
        self.at("track a")
        others = [VGroup(m, t) for nm, (m, t) in mice.items() if nm != "TrkA"]
        m, t = mice["TrkA"]
        self.play(*[FadeOut(o) for o in others], m.animate.scale(1.75).move_to([-3.6, 0.1, 0]),
                  t.animate.move_to([-3.6, -2.35, 0]), run_time=1.0)
        self.at("sympathetic ganglion")
        ring = Circle(radius=0.38, stroke_color=TEXT, stroke_width=4).move_to([-2.35, 0.25, 0])
        p1 = [3.7 + 2.7 * np.cos(np.radians(150)), 0.1 + 2.7 * np.sin(np.radians(150)), 0]
        p2 = [3.7 + 2.7 * np.cos(np.radians(210)), 0.1 + 2.7 * np.sin(np.radians(210)), 0]
        l1 = Line([-2.35 + 0.1, 0.25 + 0.36, 0], p1, color=TEXT, stroke_width=3)
        l2 = Line([-2.35 + 0.1, 0.25 - 0.36, 0], p2, color=TEXT, stroke_width=3)
        bub, o, d = zoom_bubble()
        self.play(Create(ring), Create(l1), Create(l2), FadeIn(bub), FadeIn(o), run_time=0.5)
        lb = lab("sympathetic ganglion", TEXT, 3.7, -3.4, 30)
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in d], lag_ratio=0.03), FadeIn(lb), run_time=0.5)
        self.at("in the neck")
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.5), run_time=0.7)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(g.yaxis, g.xaxis, g.ylabs, g.ylabel, g.xtitle, g.xticks)
        self.at("and colleagues")
        self.play(FadeIn(g.cite), run_time=0.4)
        self.at("counted its")
        self.play(FadeIn(g.legend), run_time=0.5)
        self.at("several ages")
        self.play(LaggedStart(*[Indicate(t[1], color=YELLOW, scale_factor=1.35) for t in g.xticks], lag_ratio=0.25),
                  run_time=1.3)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base())
        self.at("embryonic day")
        box = SurroundingRectangle(g.xticks[0], color=YELLOW, buff=0.08, stroke_width=3)
        self.play(Create(box), run_time=0.5)
        self.at("the count")
        self.play(FadeIn(g.cdot0, scale=0.3), FadeIn(g.mdot[0], scale=0.3), run_time=0.5)
        self.at("was normal")
        nl = lab("count normal", GREEN, -2.4, 1.55, 28)
        self.play(FadeIn(nl, shift=RIGHT * 0.1), run_time=0.5)
        self.finish()


def q_chips():
    head = lab("what should happen next?", TEXT, 1.6, 1.5, 36)
    chips = VGroup(*[chip(t, TEXT, 36) for t in ("counts?", "divisions?", "deaths?")])
    for c, x in zip(chips, (-1.35, 1.95, 5.1)):
        c.move_to([x, 0.2, 0])
    return head, chips


class S08(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(), *g.data(0))
        self.at("needed for")
        c1 = chip("needed for survival", GREEN, 32).move_to([1.6, 1.4, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.at("not for making")
        c2 = chip("not for making the neurons", GREY, 32).move_to([1.6, -0.1, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.5)
        self.at("what should happen")
        head, chips = q_chips()
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(head), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), run_time=0.9)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        g = Graph()
        head, chips = q_chips()
        self.add(*g.base(), *g.data(0), head, chips)
        countdown(self, 4.7, "pause and predict", x=1.6, y=-1.6, width=8.0)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(), *g.data(0))
        self.at("mutant fell")
        self.play(Create(g.cseg[0]), Create(g.mseg[0]), FadeIn(g.mdot[1], scale=0.4), FadeIn(g.wtlab), run_time=0.5)
        self.play(Create(g.cseg[1]), Create(g.mseg[1]), FadeIn(g.mdot[2], scale=0.4), run_time=0.5)
        l1, l2 = lost_labels(g, 2)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(), *g.data(2), *lost_labels(g, 2))
        self.at("birth")
        self.play(Create(g.cseg[2]), Create(g.mseg[2]), FadeIn(g.mdot[3], scale=0.4), run_time=0.7)
        self.at("about half")
        self.play(FadeIn(lost_labels(g, 3)[2]), Indicate(g.mdot[3], color=YELLOW, scale_factor=1.6), run_time=0.8)
        self.at("control ganglia")
        self.play(Indicate(g.cseg[2], color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(), *g.data(3), *lost_labels(g, 3))
        self.at("postnatal day")
        self.play(Create(g.cseg[3]), Create(g.mseg[3]), FadeIn(g.mdot[4], scale=0.4), run_time=1.4)
        self.at("nearly all")
        self.play(FadeIn(lost_labels(g, 4)[3]), run_time=0.6)
        self.finish()


def panel_items():
    """the two embryonic-age panels of s13 (dividing cells; dying cells), each with a y axis and baseline."""
    xl, xr = -3.4, 3.4
    base = -2.1
    P = {}

    def axis(xc):
        ax = xc - 2.3
        line = Line([ax, base, 0], [ax, base + 3.5, 0], color=GREY, stroke_width=3)
        floor = Line([ax, base, 0], [xc + 2.3, base, 0], color=GREY, stroke_width=3)
        yl = T("cells per section", 26, LG).rotate(PI / 2).move_to([ax - 0.4, base + 1.75, 0])
        return VGroup(line, floor, yl)

    def cell_icon(xc, mitotic):
        cell = Circle(radius=0.62, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([xc - 2.0, 2.45, 0])
        if mitotic:
            spindle = Ellipse(width=1.0, height=0.55, stroke_color=LG, stroke_width=2, fill_opacity=0).move_to([xc - 2.0, 2.45, 0])
            inner = VGroup(spindle, *[Dot([xc - 2.0, 2.45 + dy, 0], radius=0.07, color=TEXT) for dy in (-0.3, -0.15, 0, 0.15, 0.3)])
        else:
            inner = Dot([xc - 2.0, 2.45, 0], radius=0.15, color=RED)
        return VGroup(cell, inner)

    def bar(x, h, col):
        return Rectangle(width=1.3, height=h, stroke_color=col, stroke_width=3, fill_color=col,
                         fill_opacity=0.55).move_to([x, base + h / 2, 0])

    P["axl"], P["axr"] = axis(xl), axis(xr)
    P["il"], P["ir"] = cell_icon(xl, True), cell_icon(xr, False)
    P["hl"] = lab("dividing cells", TEXT, xl + 0.9, 2.75, 34)
    P["sl"] = lab("mitotic figures", LG, xl + 0.9, 2.2, 26)
    P["hr"] = lab("dying cells", TEXT, xr + 0.9, 2.75, 34)
    P["sr"] = lab("shrunken nuclei", LG, xr + 0.9, 2.2, 26)
    P["bl"] = [bar(xl - 0.95, 1.5, GREEN), bar(xl + 0.95, 1.5, PINK)]
    P["br"] = [bar(xr - 0.95, 1.0, GREEN), bar(xr + 0.95, 1.95, PINK)]
    P["labs"] = [lab("wild type", GREEN, x, base - 0.4, 26) for x in (xl - 0.95, xr - 0.95)] + \
                [lab("TrkA-null", PINK, x, base - 0.4, 26) for x in (xl + 0.95, xr + 0.95)]
    P["note"] = lab("bar heights are schematic", BRIGHT, 0, -3.1, 28)
    return P


class S13(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(), *g.data(4), *lost_labels(g, 4))
        P = panel_items()
        self.at("embryonic ages")
        banner = lab("over those embryonic ages", TEXT, 0, 3.5, 32)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        self.play(FadeIn(banner), FadeIn(P["axl"]), FadeIn(P["axr"]), run_time=0.4)
        self.at("dividing cells")
        self.play(FadeIn(P["hl"]), FadeIn(P["sl"]), FadeIn(P["il"]), run_time=0.6)
        self.play(*[GrowFromEdge(b, DOWN) for b in P["bl"]], FadeIn(P["labs"][0]), FadeIn(P["labs"][2]), run_time=0.7)
        self.at("no fewer")
        self.play(*[Indicate(b, scale_factor=1.05, color=TEXT) for b in P["bl"]], run_time=0.8)
        self.at("cells with")
        self.play(FadeIn(P["hr"]), FadeIn(P["sr"]), FadeIn(P["ir"]), run_time=0.6)
        self.play(GrowFromEdge(P["br"][0], DOWN), FadeIn(P["labs"][1]), FadeIn(P["labs"][3]), run_time=0.5)
        self.at("increased")
        self.play(GrowFromEdge(P["br"][1], DOWN), FadeIn(P["note"]), run_time=0.8)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        g = Graph()
        self.add(*g.base(cite=False), *g.data(4), *lost_labels(g, 4))
        self.at("were made")
        x0, y0 = g.px(0), g.py(100)
        br = VGroup(Line([x0 - 0.5, y0 + 0.45, 0], [x0 + 0.5, y0 + 0.45, 0], color=TEXT, stroke_width=3),
                    Line([x0 - 0.5, y0 + 0.45, 0], [x0 - 0.5, y0 + 0.28, 0], color=TEXT, stroke_width=3),
                    Line([x0 + 0.5, y0 + 0.45, 0], [x0 + 0.5, y0 + 0.28, 0], color=TEXT, stroke_width=3))
        made = lab("made", TEXT, x0, y0 + 0.9, 34)
        self.play(FadeIn(made, shift=DOWN * 0.1), Create(br), Indicate(g.cdot0, color=YELLOW, scale_factor=1.6),
                  run_time=0.6)
        self.at("then they died")
        self.play(FadeIn(g.shade), run_time=0.7)
        lost = lab("then lost", TEXT, 2.0, 0.65, 42, weight=BOLD)
        self.play(FadeIn(lost, shift=UP * 0.1), run_time=0.5)
        self.finish()


def banner_anim(G):
    return FadeIn(G.banner, shift=DOWN * 0.1)


class S15(SpokenScene):
    def construct(self):
        g = Graph()
        x0, y0 = g.px(0), g.py(100)
        self.add(*g.base(cite=False), *g.data(4), *lost_labels(g, 4), g.shade, lab("made", TEXT, x0, y0 + 0.9, 34),
                 lab("then lost", TEXT, 2.0, 0.65, 42, weight=BOLD))
        G = Grid(zoom=True)
        self.at("other pairs")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(G.title), FadeIn(G.banner), run_time=0.6)
        self.at("lacking NGF")
        self.play(FadeIn(G.rl[0], shift=RIGHT * 0.15), run_time=0.5)
        self.at("sympathetic neurons")
        self.play(FadeIn(G.heads[0]), FadeIn(G.cell[(0, 0)]), run_time=0.5)
        self.play(FadeIn(G.mark[(0, 0)], scale=0.7), run_time=0.5)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        G = Grid(zoom=True)
        gstate(self, G, ST16)
        self.at("small sensory")
        self.play(FadeIn(G.heads[1]), FadeIn(G.cell[(0, 1)]), run_time=0.6)
        self.at("that sense")
        self.play(FadeIn(G.mark[(0, 1)], scale=0.7), run_time=0.6)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        Gz = Grid(zoom=True)
        gstate(self, Gz, ST17)
        existing = list(self.mobjects)
        G = Grid()
        self.at("lacking BDNF")
        self.play(unzoom_anim(existing), FadeIn(G.rl[1], shift=RIGHT * 0.15), FadeIn(G.cell[(1, 0)]),
                  FadeIn(G.cell[(1, 1)]), run_time=0.7)
        self.at("vestibular neurons")
        self.play(FadeIn(G.heads[2]), FadeIn(G.cell[(0, 2)]), FadeIn(G.cell[(1, 2)]), run_time=0.5)
        self.play(FadeIn(G.mark[(1, 2)], scale=0.7), run_time=0.5)
        self.at("balance and head")
        self.play(FadeIn(G.icon["ear"], scale=0.6), run_time=0.5)
        self.play(Indicate(G.icon["ear"], color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST18)
        self.at("petrosal neurons")
        self.play(FadeIn(G.heads[3]), FadeIn(G.cell[(0, 3)]), FadeIn(G.cell[(1, 3)]), run_time=0.5)
        self.play(FadeIn(G.mark[(1, 3)], scale=0.7), run_time=0.5)
        self.at("the heart")
        self.play(FadeIn(G.icon["heart"], scale=0.6), run_time=0.4)
        self.at("lungs")
        self.play(FadeIn(G.icon["lung"], scale=0.6), run_time=0.4)
        self.at("and gut")
        self.play(FadeIn(G.icon["gut"], scale=0.6), run_time=0.4)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST19)
        self.at("lacking")
        self.play(FadeIn(G.rl[2], shift=RIGHT * 0.15), *[FadeIn(G.cell[(2, c)]) for c in range(4)], run_time=0.5)
        self.at("lose")
        self.play(Indicate(G.heads[3], color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("neurons too")
        self.play(FadeIn(G.mark[(2, 3)], scale=0.7), run_time=0.6)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST20)
        self.at("mice lacking")
        self.play(FadeIn(G.rl[3], shift=RIGHT * 0.15), *[FadeIn(G.cell[(3, c)]) for c in range(4)], run_time=0.5)
        self.at("the sensory neurons")
        self.play(FadeIn(G.heads[4]), *[FadeIn(G.cell[(r, 4)]) for r in range(4)], run_time=0.5)
        self.at("that report")
        self.play(FadeIn(G.mark[(3, 4)], scale=0.7), run_time=0.5)
        self.at("a limb is")
        self.play(FadeIn(G.icon["limb"], scale=0.6), run_time=0.4)
        self.play(Indicate(G.icon["limb"], color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST21)
        self.at("these mice")
        m = mouse(2.2, legs="awkward").move_to([0, 0.5, 0])
        tag = lab("lacking NT-3 or TrkC", TEXT, 0, -2.75, 36)
        self.play(*[FadeOut(x) for x in list(self.mobjects)], run_time=0.3)
        self.play(FadeIn(m), FadeIn(tag), run_time=0.4)
        self.at("limbs abnormally")
        self.play(Rotate(m, angle=0.08, about_point=m.get_center()), run_time=0.3)
        self.play(Rotate(m, angle=-0.16, about_point=m.get_center()), run_time=0.4)
        self.play(Rotate(m, angle=0.08, about_point=m.get_center()), run_time=0.3)
        self.finish()


def key_items():
    t1 = T("lose = fewer neurons", 26, TEXT)
    k1 = mark_shape(0, 0, 0.55, False).scale(0.6)
    t2 = T("part survives", 26, TEXT)
    k2 = mark_shape(0, 0, 0.55, True).scale(0.6)
    t3 = T("nearly all lost", 26, TEXT)
    a = VGroup(t1)
    b = VGroup(k1, t2).arrange(RIGHT, buff=0.2)
    c = VGroup(k2, t3).arrange(RIGHT, buff=0.2)
    VGroup(a, b, c).arrange(RIGHT, buff=0.8).move_to([0.2, KEYY, 0])
    return a, b, c


class S22(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST21)
        a, b, c = key_items()
        self.at("lose means")
        self.play(FadeIn(a, shift=DOWN * 0.1), Indicate(G.banner, scale_factor=1.05, color=YELLOW), run_time=0.5)
        self.at("usually part")
        self.play(FadeIn(b, shift=DOWN * 0.1), run_time=0.6)
        self.at("some groups")
        self.play(FadeIn(c, shift=DOWN * 0.1), Indicate(G.mark[(0, 0)], scale_factor=1.12, color=YELLOW), run_time=0.6)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST21)
        a, b, c = key_items()
        self.add(a, b, c)
        self.at("pair has")
        self.play(FadeOut(a), FadeOut(b), FadeOut(c), run_time=0.4)
        anims = []
        for r, col in enumerate(ROWCOL):
            anims.append(G.rl[r].animate.set_color(col))
            for (rr, cc), mk in G.mark.items():
                if rr == r:
                    anims.append(mk[0].animate.set_stroke(col))
                    anims.append(mk[1].animate.set_fill(col, 0.55))
        self.at("own pattern")
        self.play(AnimationGroup(*anims, lag_ratio=0.05), run_time=1.2)
        self.finish()


TRK_W = 2.3
TRK_X = 4.5


def trkchip(name, y):
    lbl = T(name, 44, PINK)
    box = RoundedRectangle(corner_radius=0.14, width=TRK_W, height=lbl.height + 0.5, stroke_color=PINK, stroke_width=2.5,
                           fill_color=PINK, fill_opacity=0.16).move_to([TRK_X, y, 0])
    return VGroup(box, lbl.move_to(box))


def overlap_state():
    nt3 = chip("NT-3", BLUE, 44).move_to([-4.6, 0, 0])
    return nt3, trkchip("TrkC", 0), trkchip("TrkA", 2.5), trkchip("TrkB", -2.5)


def overlap_full():
    nt3, trkc, trka, trkb = overlap_state()
    a = arr([-3.5, 0, 0], [3.2, 0, 0], BLUE, 6)
    pl = lab("prefers", LG, -0.15, 0.45, 28)
    da = dashed_arrow([-3.5, 0.3, 0], [3.2, 2.5, 0])
    db = dashed_arrow([-3.5, -0.3, 0], [3.2, -2.5, 0])
    al = lab("also, weaker", LG, -1.0, 2.15, 28)
    bl = lab("also, weaker", LG, -1.0, -2.15, 28)
    return VGroup(nt3, trkc, trka, trkb, a, pl, da, db, al, bl)


class S24(SpokenScene):
    def construct(self):
        G = Grid()
        gstate(self, G, ST21)
        for r, col in enumerate(ROWCOL):
            G.rl[r].set_color(col)
        for (r, c) in ST21["marks"]:
            G.mark[(r, c)][0].set_stroke(ROWCOL[r])
            G.mark[(r, c)][1].set_fill(ROWCOL[r], 0.55)
        nt3, trkc, trka, trkb = overlap_state()
        self.at("overlaps")
        self.play(*[Indicate(G.mark[m], scale_factor=1.08, color=TEXT) for m in ST21["marks"]], run_time=0.9)
        self.at("NT-3 prefers")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.25)
        self.play(FadeIn(nt3), run_time=0.25)
        self.at("prefers")
        a = arr([-3.5, 0, 0], [3.2, 0, 0], BLUE, 6)
        pl = lab("prefers", LG, -0.15, 0.45, 28)
        self.play(GrowArrow(a), FadeIn(trkc), FadeIn(pl), run_time=0.7)
        self.at("also activates")
        al = lab("also, weaker", LG, -1.0, 2.15, 28)
        self.play(FadeIn(al), run_time=0.3)
        self.at("activates track")
        da = dashed_arrow([-3.5, 0.3, 0], [3.2, 2.5, 0])
        self.play(Create(da[0]), FadeIn(da[1]), FadeIn(trka), run_time=0.6)
        self.at("and track")
        bl = lab("also, weaker", LG, -1.0, -2.15, 28)
        db = dashed_arrow([-3.5, -0.3, 0], [3.2, -2.5, 0])
        self.play(Create(db[0]), FadeIn(db[1]), FadeIn(trkb), FadeIn(bl), run_time=0.6)
        self.finish()


def q25():
    ml = mouse(2.0, legs="bent").move_to([-3.4, 0.55, 0])
    mr = mouse(2.0, legs="bent").move_to([3.4, 0.55, 0])
    tl = lab("no NT-3", BLUE, -3.4, -2.0, 38)
    tr = lab("no TrkC", PINK, 3.4, -2.0, 38)
    q = lab("no NT-3 vs no TrkC: which loses more neurons?", TEXT, 0, 3.3, 36)
    return ml, mr, tl, tr, q


class S25(SpokenScene):
    def construct(self):
        ml, mr, tl, tr, q = q25()
        carry = overlap_full()
        self.add(carry)
        self.at("lacking NT-3")
        self.play(FadeOut(carry), FadeIn(ml), FadeIn(tl), run_time=0.6)
        self.at("lose more")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        self.at("than one")
        self.play(FadeIn(mr), FadeIn(tr), run_time=0.6)
        self.finish()


class S26Pause(NarratedScene):
    def construct(self):
        ml, mr, tl, tr, q = q25()
        self.add(ml, mr, tl, tr, q)
        countdown(self, 4.7, "think: which loses more?", x=0.0, y=-3.5, width=8.0)
        self.finish()


NG = 24
LOST_NT3, LOST_TRKC = 8, 5


def ganglia_pair():
    perm = np.random.RandomState(4).permutation(NG)
    out = {}
    for key, cx in (("L", -3.4), ("R", 3.4)):
        o, d = ganglion(cx, 0.35, 6.0, 4.5, NG, r=0.22)
        lost_n = LOST_NT3 if key == "L" else LOST_TRKC
        lost_idx = set(perm[:lost_n].tolist())
        out[key] = (o, d, [d[i] for i in range(NG) if i in lost_idx])
    return out


def pair_labels():
    hd = lab("same age, same ganglion", TEXT, 0, 3.35, 32)
    ll = lab("no NT-3", BLUE, -3.4, -2.45, 36)
    lr = lab("no TrkC", PINK, 3.4, -2.45, 36)
    sc = lab("schematic: the size of the gap varies", BRIGHT, 0, -3.15, 28)
    return hd, ll, lr, sc


class S27(SpokenScene):
    def construct(self):
        ml, mr, tl, tr, q = q25()
        self.add(ml, mr, tl, tr, q)
        self.at("expect more")
        self.play(Indicate(VGroup(ml, tl), color=YELLOW, scale_factor=1.05), run_time=0.9)
        P = ganglia_pair()
        hd, ll, lr, sc = pair_labels()
        self.at("in many")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.25)
        self.play(FadeIn(P["L"][0]), FadeIn(P["R"][0]), FadeIn(hd), FadeIn(ll), FadeIn(lr), FadeIn(sc), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for k in "LR" for x in P[k][1]], lag_ratio=0.01), run_time=0.5)
        self.at("same age")
        self.play(Indicate(hd, color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("mice lacking nt3")
        self.play(Indicate(ll, color=YELLOW, scale_factor=1.15), run_time=0.5)
        self.at("lose more")
        gh = [ghost(c) for c in P["L"][2]]
        self.play(*[FadeOut(c) for c in P["L"][2]], *[FadeIn(x) for x in gh], run_time=0.9)
        self.at("than mice")
        self.play(Indicate(lr, color=YELLOW, scale_factor=1.15), run_time=0.4)
        self.at("lacking track")
        gh2 = [ghost(c) for c in P["R"][2]]
        self.play(*[FadeOut(c) for c in P["R"][2]], *[FadeIn(x) for x in gh2], run_time=0.8)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        # carry the two ganglia from the last scene
        P = ganglia_pair()
        hd, ll, lr, sc = pair_labels()
        carry = VGroup(P["L"][0], P["R"][0], hd, ll, lr, sc)
        for k in "LR":
            for i, dd in enumerate(P[k][1]):
                if dd in P[k][2]:
                    carry.add(ghost(dd))
                else:
                    carry.add(dd)
        self.add(carry)
        big = Ellipse(width=7.2, height=5.0, stroke_color=RED, stroke_width=4, fill_color=RED,
                      fill_opacity=0.16).move_to([-2.2, 0.15, 0])
        small = Ellipse(width=3.3, height=2.3, stroke_color=PINK, stroke_width=4, fill_color=PINK,
                        fill_opacity=0.3).move_to([-3.75, -1.0, 0])
        lb = lab("lost without NT-3", RED, -1.5, 1.5, 32)
        ls = lab("lost without\nTrkC", PINK, -3.75, -1.0, 26, line_spacing=0.8)
        self.at("fits")
        self.play(FadeOut(carry), run_time=0.3)
        self.play(FadeIn(big), FadeIn(lb), run_time=0.5)
        self.play(FadeIn(small), FadeIn(ls), run_time=0.7)
        self.at("also acting")
        ex = lab("NT-3 also acts\nthrough TrkA and TrkB", BLUE, 4.0, 2.0, 28, line_spacing=0.8)
        lead = DashedLine([2.3, 1.55, 0], [0.9, 1.0, 0], color=BLUE, stroke_width=3, dash_length=0.12)
        self.play(FadeIn(ex), Create(lead), run_time=0.7)
        self.at("size of the gap")
        gl = lab("extra loss\n(the gap)", TEXT, 4.2, -0.45, 28, line_spacing=0.8)
        ga = arr([3.0, -0.45, 0], [-0.4, -0.45, 0], TEXT, 4, 0.2)
        nt = lab("sets need not be exactly nested", TEXT, -2.2, -3.2, 28)
        self.play(FadeIn(gl), GrowArrow(ga), FadeIn(nt), run_time=0.6)
        self.at("depends on")
        dp = lab("varies with the\nganglion and age", BRIGHT, 4.1, -1.55, 28, line_spacing=0.8)
        self.play(FadeIn(dp), run_time=0.6)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        o, d = ganglion(0, 1.85, 6.4, 3.4, 16, r=0.23)
        self.add(o, *d)
        tl = Line([-5.8, -2.3, 0], [5.8, -2.3, 0], color=GREY, stroke_width=5)
        tip = Triangle(color=GREY, fill_opacity=1, stroke_width=0).scale(0.16).rotate(-PI / 2).move_to([5.85, -2.3, 0])
        e1 = lab("early", LG, -5.0, -2.85, 30)
        e2 = lab("later", LG, 5.0, -2.85, 30)
        sch = lab("schematic", BRIGHT, 0, -2.85, 28)
        t1 = Line([-3.6, -2.2, 0], [-3.6, -2.4, 0], color=GREY, stroke_width=3)
        t2 = Line([3.6, -2.2, 0], [3.6, -2.4, 0], color=GREY, stroke_width=3)
        self.at("some populations")
        self.play(Create(tl), FadeIn(tip), FadeIn(e1), FadeIn(e2), FadeIn(sch), FadeIn(t1), FadeIn(t2), run_time=0.8)
        b1 = chip("factor 1", BLUE, 32).move_to([-3.6, -1.05, 0])
        b2 = chip("factor 2", BLUE, 32).move_to([3.6, -1.05, 0])
        a1 = arr([-3.0, -0.55, 0], [-1.9, 0.3, 0], BLUE, 5)
        a2 = arr([3.0, -0.55, 0], [1.9, 0.3, 0], BLUE, 5)
        now = Dot([-3.6, -2.3, 0], radius=0.16, color=YELLOW)
        self.at("more than one")
        self.play(FadeIn(b1, shift=UP * 0.1), GrowArrow(a1), FadeIn(now, scale=0.5), FadeIn(b2.set_opacity(0.4)),
                  run_time=0.6)
        self.at("different stages")
        self.play(b1.animate.set_opacity(0.4), a1.animate.set_opacity(0.2), now.animate.move_to([3.6, -2.3, 0]),
                  run_time=0.7)
        self.play(b2[0].animate.set_fill(BLUE, 0.16).set_stroke(BLUE, opacity=1.0, width=4),
                  b2[1].animate.set_opacity(1.0), GrowArrow(a2), run_time=0.6)
        self.finish()


def mini_grid():
    xs = [-4.7 + 0.8 * c for c in range(5)]
    ys = [2.35 - 0.9 * r for r in range(4)]
    cells = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.7, height=0.72, stroke_color=GREY, stroke_width=2,
                                      stroke_opacity=0.6, fill_opacity=0).move_to([xs[c], ys[r], 0])
                     for r in range(4) for c in range(5)])
    marks = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.7, height=0.72, stroke_color=ROWCOL[r], stroke_width=3,
                                      fill_color=ROWCOL[r], fill_opacity=0.5).move_to([xs[c], ys[r], 0])
                     for (r, c) in ST21["marks"]])
    rls = VGroup(*[T(GROWS[r], 26, ROWCOL[r], line_spacing=0.8).move_to([-5.95, ys[r], 0]) for r in range(4)])
    return cells, marks, rls


class S30(SpokenScene):
    def construct(self):
        hd = lab("the takeaway", GOLD, -3.3, 3.45, 36)
        self.add(hd)
        cells, marks, rls = mini_grid()
        cap = lab("columns: neuron populations", LG, -3.1, -1.25, 26)
        g = Graph(ox=1.9, oy=-2.1, sx=0.28, sy=0.042, compact=True)
        t2 = lab("TrkA-null sympathetic\nganglion: made, then lost", TEXT, 3.5, 3.3, 26, line_spacing=0.85)
        self.at("each factor")
        self.play(FadeIn(cells), FadeIn(rls), FadeIn(cap),
                  *[FadeIn(m) for m in (g.yaxis, g.xaxis, g.ylabs, g.ylabel, g.xtitle, g.xticks)], FadeIn(g.cdot0),
                  FadeIn(g.mdot[0]), FadeIn(t2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m, scale=0.7) for m in marks], lag_ratio=0.2), run_time=0.9)
        self.at("own pattern")
        t1 = lab("each factor and\nreceptor pair has its\nown pattern of loss", TEXT, -3.3, -2.35, 28, line_spacing=0.85)
        self.play(FadeIn(t1), Create(g.cline), *[Create(s_) for s_ in g.mseg], *[FadeIn(dd) for dd in g.mdot[1:]],
                  run_time=1.8)
        self.at("in the sympathetic")
        made = lab("made", GREEN, g.px(0) + 0.5, g.py(100) + 0.42, 28)
        self.play(FadeIn(made), run_time=0.3)
        self.at("neurons were made")
        self.play(Indicate(made, color=GREEN, scale_factor=1.2), run_time=0.6)
        self.at("then lost")
        self.play(FadeIn(g.shade), run_time=0.5)
        lost = lab("then lost", TEXT, 4.1, 0.8, 30, weight=BOLD)
        self.play(FadeIn(lost), run_time=0.4)
        self.finish()


class S31End(EndCard):
    LINE = "Each factor and receptor pair\nhas its own pattern of loss."
