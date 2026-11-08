"""Correlation, Not Just Spikes (chapter 3 of Activity Before Experience: Spontaneous Retinal Waves)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept; same look as the other chapters, taken from scenes.old.py)
  BLUE   = cells and axons of one eye (the retina, the frog's own eye)
  ORANGE = cells and axons of the other eye (the frog's extra eye)
  YELLOW = firing: a spike, a burst, a wave (and a depolarized membrane)
  PURPLE = the target cell or target tissue (tectum, the receptor's cell)
  TEAL   = labelled ganglion cells and their axon endings (the termination zone)
  PINK   = the beta2 subunit / the knockout mice
  RED    = APV, the blocker
  GOLD   = calcium entering
  WHITE  = glutamate and the key message (TEXT colour), magnesium is GREY with a white outline
  GREEN  = strengthened / kept
  GREY   = structure, outlines, silence
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#FF9CC2"
BLUE_D = "#2B7A92"
LIGHT = "#C5CBD6"


# ------------------------------------------------------------------ helpers
def cell(x, y, color=BLUE, r=0.3):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    return c.move_to([x, y, 0])


def make_raster(cx, cy, w, h, kind, seed=1, nrows=5, color=YELLOW):
    """A spike raster computed from a rule.
    corr    : three sweeps, every row fires a short burst as the sweep passes (small delay row to row)
    scatter : every row fires at independent random times (more spikes than 'corr')
    altered : weaker, slower, partial sweeps (only some rows join, bigger row delay) plus stray spikes
    """
    rng = np.random.RandomState(seed)
    frame = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2.5).move_to([cx, cy, 0])
    x0, x1 = cx - w / 2 + 0.35, cx + w / 2 - 0.35
    rowh = (h - 0.5) / nrows
    ys = [cy + h / 2 - 0.25 - rowh * (i + 0.5) for i in range(nrows)]
    ticks = VGroup()
    for i, y in enumerate(ys):
        if kind == "corr":
            ts = [tc + i * 0.02 + 0.026 * k + rng.uniform(-0.004, 0.004) for tc in (0.08, 0.40, 0.72) for k in range(3)]
        elif kind == "scatter":
            ts = list(rng.uniform(0.01, 0.99, 12))
        else:  # altered
            ts = []
            for tc, rows in ((0.10, (0, 1, 2)), (0.43, (1, 2, 3)), (0.74, (2, 3, 4))):
                if i in rows:
                    k0 = rows.index(i)
                    t0 = tc + 0.065 * k0
                    ts += [t0, t0 + 0.022, t0 + 0.044]
            ts += list(rng.uniform(0.01, 0.99, 1))
        for t in ts:
            x = x0 + t * (x1 - x0)
            ticks.add(Line([x, y - rowh * 0.33, 0], [x, y + rowh * 0.33, 0], color=color, stroke_width=4))
    cells = T("cells", 26, GREY).rotate(PI / 2).move_to([cx - w / 2 - 0.38, cy, 0])
    tlab = T("time", 26, GREY).move_to([cx + w / 2 - 0.55, cy - h / 2 - 0.32, 0])
    return SimpleNamespace(frame=frame, ticks=ticks, all=VGroup(frame, ticks), cx=cx, cy=cy, w=w, h=h, x0=x0, x1=x1,
                           cells=cells, time=tlab)


def band_on(ticks, tr, halfw=0.3, dim=0.4):
    for ln in ticks:
        def upd(m, x=ln.get_x()):
            on = abs(x - tr.get_value()) < halfw
            m.set_stroke(opacity=1.0 if on else dim, width=7 if on else 3)
        ln.add_updater(upd)


def band_off(ticks):
    for ln in ticks:
        ln.clear_updaters()
        ln.set_stroke(opacity=1.0, width=4)


def band_rect(tr, halfw, cy, h):
    b = Rectangle(width=2 * halfw, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.14)
    b.add_updater(lambda m: m.move_to([tr.get_value(), cy, 0]))
    return b


def sc_panel(cx, cy, w, h, top=0.9, bot=1.95, ylab=True):
    """a collicular outline with a plotting area and axis labels; zones are computed Gaussians (schematic).
    Returns box, axes, labels (axon endings, position in colliculus)."""
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
    ax_w, ax_h = w - 0.9, h - top - bot
    ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 1], x_length=ax_w, y_length=ax_h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 2.5})
    ax.move_to([cx - w / 2 + 0.45 + ax_w / 2, cy - h / 2 + bot + ax_h / 2, 0])
    parts = []
    if ylab:
        yl = T("axon endings", 26, GREY).move_to([0, 0, 0]).align_to([cx - w / 2 + 0.3, 0, 0], LEFT)
        yl.set_y(cy + h / 2 - top / 2 - 0.05 + 0.0)
        yl.set_y(ax.c2p(0, 1.1)[1] + 0.35)
        parts.append(yl)
    xl = T("position in colliculus", 26, GREY).move_to([ax.get_center()[0], cy - h / 2 + 0.38, 0])
    parts.append(xl)
    return box, ax, VGroup(*parts)


def zone(ax, sigma, peak, color=TEAL):
    g = ax.plot(lambda x: peak * np.exp(-((x - 5) ** 2) / (2 * sigma ** 2)), x_range=[0, 10], color=color, stroke_width=6)
    area = ax.get_area(g, x_range=[0, 10], color=color, opacity=0.32)
    return g, area


def width_bracket(ax, sigma, label, color=TEXT, size=26):
    """full width at half height, drawn just under the baseline, with its label under that."""
    half = 1.1775 * sigma
    y0 = ax.c2p(0, 0)[1] - 0.3
    a, b = ax.c2p(5 - half, 0)[0], ax.c2p(5 + half, 0)[0]
    br = DoubleArrow([a, y0, 0], [b, y0, 0], buff=0, color=color, stroke_width=4, tip_length=0.15)
    lab = T(label, size, color).move_to([(a + b) / 2, y0 - 0.38, 0])
    return br, lab


def credit(text, y=3.4, size=28):
    return T(text, size, TEXT).move_to([0, y, 0])


def legend_eyes(y=-3.5):
    return VGroup(Dot(radius=0.14, color=BLUE), T("the eye", 26, BLUE), Dot(radius=0.14, color=ORANGE), T("the extra eye", 26, ORANGE)
                  ).arrange(RIGHT, buff=0.2).move_to([0, y, 0])


# ------------------------------------------------------------------ the frog (a cartoon, not a structure)
FOFF = np.array([0.0, -0.3, 0.0])


def frog_parts():
    d = {}
    # Dorsal head: paired protruding eye sockets, broad snout, tapered jaw.
    pts = [(-6.2, 0.0), (-5.9, 1.0), (-5.1, 1.4), (-4.9, 2.35),
           (-4.0, 2.7), (-3.1, 2.15), (-1.5, 2.0), (2.8, 1.75),
           (5.9, 0.8), (6.2, -0.6), (5.0, -2.2), (1.8, -2.8),
           (-1.6, -2.75), (-3.1, -2.1), (-4.0, -2.55),
           (-4.9, -2.2), (-5.2, -1.3), (-6.0, -0.8)]
    body = VMobject()
    body.set_points_smoothly([np.array([x, y, 0.0]) + FOFF for x, y in pts + [pts[0]]])
    body.set_stroke(LIGHT, 4).set_fill(GREY, 0.12)
    mouth = VMobject()
    mouth.set_points_smoothly([np.array([x, y, 0.0]) + FOFF for x, y in
                             [(-6.0, -0.25), (-5.3, -0.6), (-4.4, -0.55), (-3.1, -0.2)]])
    mouth.set_stroke(LIGHT, 4).set_fill(opacity=0)
    nostrils = VGroup(*[Ellipse(width=0.18, height=0.3, color=LIGHT, fill_opacity=0.7)
                           .move_to(np.array([-5.45, y, 0.0]) + FOFF) for y in (0.45, -0.85)])
    far_eye = VGroup(Circle(radius=0.58, stroke_color=LIGHT, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.3),
                     Ellipse(width=0.16, height=0.65, color=LIGHT, fill_opacity=1))
    far_eye.move_to(np.array([-4.05, -1.65, 0]) + FOFF)
    d["head"] = VGroup(body, mouth, nostrils, far_eye)
    eye_pos = np.array([-4.05, 1.65, 0]) + FOFF
    d["eyeA"] = VGroup(Circle(radius=0.65, stroke_color=BLUE, stroke_width=4,
                             fill_color=BLUE, fill_opacity=0.4),
                       Ellipse(width=0.18, height=0.72, color=TEXT, fill_opacity=1)).move_to(eye_pos)
    d["eyeB"] = VGroup(Circle(radius=0.65, stroke_color=ORANGE, stroke_width=4,
                             fill_color=ORANGE, fill_opacity=0.4),
                       Ellipse(width=0.18, height=0.72, color=TEXT, fill_opacity=1))
    d["eyeB"].move_to(np.array([-0.6, 2.1, 0]) + FOFF)
    d["tect"] = RoundedRectangle(corner_radius=0.6, width=4.8, height=3.2, stroke_color=PURPLE, stroke_width=4,
                                 fill_color=PURPLE, fill_opacity=0.25).move_to(np.array([2.9, -0.1, 0]) + FOFF)
    d["lt"] = T("optic tectum", 28, PURPLE).move_to(np.array([2.9, -2.2, 0]) + FOFF)
    d["la"] = T("eye", 26, BLUE).move_to(np.array([-4.0, 2.95, 0]) + FOFF)
    d["lb"] = T("extra eye", 26, ORANGE).move_to(np.array([-0.6, 3.15, 0]) + FOFF)
    d["lh"] = T("frog", 28, LIGHT).move_to(np.array([-1.6, -1.8, 0]) + FOFF)
    d["axA"] = VGroup(*[Line(np.array([-3.4, 1.45, 0]) + FOFF, np.array([0.5, y, 0]) + FOFF,
                             color=BLUE, stroke_width=4) for y in (0.8, 0.4, 0.0)])
    d["axB"] = VGroup(*[Line(np.array([-0.2, 1.5, 0]) + FOFF, np.array([0.5, y, 0]) + FOFF,
                             color=ORANGE, stroke_width=4) for y in (0.6, 0.2, -0.2)])
    return d


# the big tectum used from s14 to s19: same box everywhere
BOX_C = np.array([0.0, -0.05, 0.0])
BOX_W, BOX_H = 9.2, 4.2


def big_tect(wobble=True):
    tect = RoundedRectangle(corner_radius=0.4, width=BOX_W, height=BOX_H, stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=0.12).move_to(BOX_C)
    n = 10
    rng = np.random.RandomState(5)
    wid = rng.uniform(0.8, 1.2, n)
    wid = wid / wid.sum() * (BOX_W - 0.4)
    edges = np.concatenate([[0], np.cumsum(wid)]) + (BOX_C[0] - (BOX_W - 0.4) / 2)
    ytop, ybot = BOX_C[1] + (BOX_H - 0.4) / 2, BOX_C[1] - (BOX_H - 0.4) / 2
    ys = np.linspace(ybot, ytop, 14)
    ph = rng.uniform(0, 6.28, n + 1)

    def bx(k, y):
        if k in (0, n):
            return edges[k]
        return edges[k] + 0.09 * np.sin(2.3 * y + ph[k])
    stripes = VGroup()
    for i in range(n):
        left = [[bx(i, y), y, 0] for y in ys]
        right = [[bx(i + 1, y), y, 0] for y in ys[::-1]]
        stripes.add(Polygon(*(left + right), stroke_width=0, fill_color=(BLUE if i % 2 == 0 else ORANGE), fill_opacity=0.62))
    return tect, stripes


def striped_still():
    tect, stripes = big_tect()
    lab = T("optic tectum", 26, PURPLE).move_to([-4.0, 2.95, 0])
    return tect, stripes, lab


def sheet_parts():
    slab = Rectangle(width=BOX_W - 0.3, height=0.4, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.45
                     ).move_to([BOX_C[0], BOX_C[1] + BOX_H / 2 + 0.22, 0])
    lab = T("polymer sheet with APV", 26, RED).move_to([2.7, 2.95, 0])
    return slab, lab


# ------------------------------------------------------------------ the two-panel zone frame (s06-s08)
PX = (-3.45, 3.45)
PY, PW, PH = 0.0, 6.4, 5.0


def two_panels():
    d = {}
    d["bn"], d["an"], d["ln"] = sc_panel(PX[0], PY, PW, PH)
    d["bk"], d["ak"], d["lk"] = sc_panel(PX[1], PY, PW, PH)
    d["tn"] = T("normal", 30, TEXT, weight=BOLD).move_to([PX[0], 2.95, 0])
    d["tk"] = T("beta2 knockout", 30, PINK, weight=BOLD).move_to([PX[1], 2.95, 0])
    d["day"] = T("postnatal day 8", 26, LIGHT).move_to([0, 3.4, 0])
    d["note"] = T("schematic", 26, LIGHT).move_to([-5.6, -3.3, 0])
    d["gn"], d["fn"] = zone(d["an"], 0.8, 1.0)
    d["gk"], d["fk"] = zone(d["ak"], 2.4, 1.0 / 3.0)
    d["q"] = T("?", 120, TEXT, weight=BOLD).move_to([PX[1], PY + 0.3, 0])
    d["chips"] = VGroup(chip("small", LIGHT, 26), chip("broad", LIGHT, 26)).arrange(RIGHT, buff=0.8).move_to([0, -3.3, 0])
    return d


def pq1_static(scene, d):
    scene.add(d["bn"], d["bk"], d["an"], d["ak"], d["ln"], d["lk"], d["tn"], d["tk"], d["note"], d["gn"], d["fn"], d["day"], d["q"], d["chips"])


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Activity Before Experience: Spontaneous Retinal Waves"
    TITLE = "Correlation, Not Just Spikes"


class S01Q(SpokenScene):
    def construct(self):
        top = make_raster(0.45, 1.75, 10.8, 2.6, "corr", seed=3)
        bot = make_raster(0.45, -1.45, 10.8, 2.6, "scatter", seed=8)
        lt = T("neighbouring cells fire in sweeps", 26, TEXT).move_to([0.45, 3.4, 0])
        lb = T("scattered firing", 26, TEXT).move_to([-3.9, -3.2, 0])
        sch = T("schematic", 26, LIGHT).move_to([2.2, -3.2, 0])
        self.play(FadeIn(top.frame), FadeIn(bot.frame), FadeIn(lt), FadeIn(lb), FadeIn(sch), FadeIn(top.cells), FadeIn(bot.cells),
                  FadeIn(bot.time), run_time=0.5)
        self.at("full of spikes")
        self.play(FadeIn(top.ticks, lag_ratio=0.01), FadeIn(bot.ticks, lag_ratio=0.01), run_time=0.85)
        self.at("still fail")
        self.play(Indicate(bot.ticks, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        lx, rx = -3.6, 3.7
        l_title = T("which eye", 34, TEXT, weight=BOLD).move_to([lx, 3.3, 0])
        l_sub = T("in the LGN", 26, LIGHT).move_to([lx, 2.72, 0])
        bands = VGroup(*[Rectangle(width=4.8, height=0.4, stroke_width=0, fill_color=(BLUE if i % 2 == 0 else ORANGE),
                                   fill_opacity=0.55).move_to([lx, 1.75 - 0.4 * i, 0]) for i in range(9)])
        l_box = SurroundingRectangle(bands, buff=0.0, color=GREY, stroke_width=3)
        key = VGroup(Dot(radius=0.14, color=BLUE), T("one eye", 26, BLUE), Dot(radius=0.14, color=ORANGE), T("other eye", 26, ORANGE)
                     ).arrange(RIGHT, buff=0.2).move_to([lx, -2.55, 0])
        left = VGroup(l_title, l_sub, bands, l_box, key)
        r_title = T("where in the eye", 34, TEXT, weight=BOLD).move_to([rx, 3.3, 0])
        n = 8
        xs = [rx - 2.45 + 0.7 * i for i in range(n)]

        def shade(i):
            return interpolate_color(ManimColor("#9FDDF0"), ManimColor(BLUE_D), i / (n - 1))
        dots = VGroup(*[Dot([x, 1.7, 0], radius=0.24, color=shade(i)) for i, x in enumerate(xs)])
        boxes = VGroup(*[Rectangle(width=0.62, height=0.62, stroke_width=0, fill_color=shade(i), fill_opacity=0.9).move_to([x, -1.55, 0])
                         for i, x in enumerate(xs)])
        links = VGroup(*[Line([x, 1.4, 0], [x, -1.2, 0], color=GREY, stroke_width=3) for x in xs])
        l_eye = T("eye", 26, BLUE).move_to([rx, 2.4, 0])
        l_col = T("in the superior colliculus", 26, LIGHT).move_to([rx, -2.45, 0])
        self.play(FadeIn(left), run_time=0.9)
        self.at("different map")
        self.play(FadeIn(dots), FadeIn(l_eye), Create(links), FadeIn(boxes), FadeIn(l_col), run_time=0.9)
        self.at("Not which eye")
        self.play(left.animate.set_opacity(0.4), run_time=0.5)
        self.at("where in the eye")
        self.play(FadeIn(r_title), Indicate(dots, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.finish()


class S03Label(SpokenScene):
    def construct(self):
        rc = np.array([-4.3, 0.1, 0.0])
        outline = Circle(radius=2.3, stroke_color=GREY, stroke_width=3).move_to(rc)
        pts = []
        for j in range(-4, 5):
            for i in range(-4, 5):
                p = rc + np.array([i * 0.62 + (0.31 if j % 2 else 0), j * 0.54, 0])
                if np.linalg.norm(p - rc) < 1.95:
                    pts.append(p)
        cells = VGroup(*[cell(p[0], p[1], BLUE, 0.17) for p in pts])
        ang = np.radians(35)
        target = rc + 1.75 * np.array([np.cos(ang), np.sin(ang), 0])
        rim = [k for k in range(len(pts)) if np.linalg.norm(pts[k] - rc) > 1.5]
        near = sorted(rim, key=lambda k: np.linalg.norm(pts[k] - target))[:4]
        patch = [cells[k] for k in near]
        retina_l = T("retina", 26, LIGHT).move_to([-4.3, -2.75, 0])
        top_cell = max(near, key=lambda k: pts[k][1])
        lab = T("labelled ganglion cells", 26, TEAL).move_to([-3.0, 3.15, 0])
        lab_line = Line([pts[top_cell][0], 2.9, 0], pts[top_cell] + np.array([0, 0.22, 0]), color=TEAL, stroke_width=2)

        box, ax, axl = sc_panel(3.4, -0.1, 6.4, 5.4)
        sc_l = T("superior colliculus", 26, LIGHT).move_to([3.4, 3.15, 0])
        mid_l = T("midbrain", 26, LIGHT).move_to([3.4, -3.2, 0])
        starts = [pts[k] + np.array([0.2, 0, 0]) for k in near]
        starts.sort(key=lambda p: -p[1])
        ends = [ax.c2p(5 + d, 0.02) for d in (-0.9, -0.3, 0.3, 0.9)]
        axons = VGroup(*[CubicBezier(s, s + RIGHT * 2.6, e + LEFT * 2.6, e, color=TEAL, stroke_width=4) for s, e in zip(starts, ends)])
        g, area = zone(ax, 0.8, 1.0)
        br, brl = width_bracket(ax, 0.8, "small zone", TEAL)

        self.play(FadeIn(box), FadeIn(ax), FadeIn(outline), FadeIn(cells, lag_ratio=0.01), FadeIn(retina_l), run_time=1.3)
        self.at("ganglion cells")
        self.play(*[c.animate.set_fill(TEAL, 1.0).set_stroke(TEAL) for c in patch], FadeIn(lab), Create(lab_line), run_time=0.9)
        self.at("In the superior colliculus")
        self.play(FadeIn(sc_l), FadeIn(axl), run_time=0.7)
        self.at("in the midbrain")
        self.play(FadeIn(mid_l), run_time=0.5)
        self.at("their axons")
        self.play(Create(axons, lag_ratio=0.1), run_time=0.7)
        self.at("end in a zone")
        self.play(Create(g), FadeIn(area), run_time=0.9)
        self.at("small if the map")
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.8)
        self.finish()


class S04Ko(SpokenScene):
    def construct(self):
        names = ["Todd McLaughlin", "Christine Torborg", "Marla Feller", "Dennis O'Leary"]
        lines = VGroup(*[T(n, 50, TEXT) for n in names]).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        lines.move_to([0, 0.75, 0])
        yr = T("2003", 38, LIGHT).next_to(lines, DOWN, buff=0.5).align_to(lines, LEFT)
        ko = T("beta2 knockout mice", 48, PINK, weight=BOLD).move_to([0, -2.9, 0])
        self.at("Todd")
        self.play(FadeIn(lines[0], shift=RIGHT * 0.2), run_time=0.45)
        self.at("Christine")
        self.play(FadeIn(lines[1], shift=RIGHT * 0.2), run_time=0.45)
        self.at("Marla")
        self.play(FadeIn(lines[2], shift=RIGHT * 0.2), run_time=0.45)
        self.at("Dennis")
        self.play(FadeIn(lines[3], shift=RIGHT * 0.2), run_time=0.45)
        self.at("studied")
        self.play(FadeIn(yr), run_time=0.5)
        self.at("mice")
        self.play(FadeIn(ko, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S05Spikes(SpokenScene):
    def construct(self):
        R = make_raster(0.45, 0.1, 10.8, 5.0, "scatter", seed=21, nrows=8)
        head = T("beta2 knockout mice", 30, PINK, weight=BOLD).move_to([-3.4, 3.4, 0])
        nowaves = T("no waves", 32, LIGHT, weight=BOLD).move_to([3.6, 3.4, 0])
        when = T("first postnatal week, in one study", 26, LIGHT).move_to([-2.4, -3.2, 0])
        many = T("many spikes, not in step", 26, YELLOW).move_to([3.3, -3.2, 0])
        self.play(FadeIn(R.frame), FadeIn(head), FadeIn(when), FadeIn(R.cells), run_time=0.5)
        self.play(FadeIn(R.ticks, lag_ratio=0.01), run_time=1.2)
        self.at("no waves")
        self.play(FadeIn(nowaves), run_time=0.5)
        self.at("fired often")
        self.play(Indicate(R.ticks, color=YELLOW, scale_factor=1.02), run_time=0.8)
        self.at("without correlation")
        self.play(FadeIn(many), run_time=0.5)
        self.finish()


class S06Pq1(SpokenScene):
    def construct(self):
        d = two_panels()
        self.at("Predict")
        self.play(FadeIn(d["bn"]), FadeIn(d["bk"]), FadeIn(d["an"]), FadeIn(d["ak"]), FadeIn(d["ln"]), FadeIn(d["lk"]), FadeIn(d["tn"]),
                  FadeIn(d["tk"]), FadeIn(d["note"]), run_time=0.9)
        self.play(Create(d["gn"]), FadeIn(d["fn"]), run_time=0.8)
        self.at("By day")
        self.play(FadeIn(d["day"]), run_time=0.5)
        self.at("mutant zones")
        self.play(FadeIn(d["q"], scale=1.3), run_time=0.5)
        self.at("small")
        self.play(FadeIn(d["chips"][0]), run_time=0.4)
        self.at("broad")
        self.play(FadeIn(d["chips"][1]), run_time=0.4)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        d = two_panels()
        pq1_static(self, d)
        self.finish()


class S08Rev1(SpokenScene):
    def construct(self):
        d = two_panels()
        pq1_static(self, d)
        brn, lbn = width_bracket(d["an"], 0.8, "small", GREEN, 26)
        brk, lbk = width_bracket(d["ak"], 2.4, "broad", RED, 26)
        self.at("Broad")
        self.play(FadeOut(d["q"]), FadeOut(d["chips"]), Create(d["gk"]), FadeIn(d["fk"]), run_time=1.5)
        self.at("Normal mice")
        self.play(Indicate(d["gn"], color=TEXT, scale_factor=1.04), run_time=0.7)
        self.at("small zones")
        self.play(GrowFromCenter(brn), FadeIn(lbn), run_time=0.7)
        self.at("the mutant stayed")
        self.play(Indicate(d["gk"], color=TEXT, scale_factor=1.04), run_time=0.6)
        self.at("stayed broad")
        self.play(GrowFromCenter(brk), FadeIn(lbk), run_time=0.7)
        self.finish()


class S09Late(SpokenScene):
    def construct(self):
        y = 2.95
        axis = Arrow([-6.5, y - 0.75, 0], [6.5, y - 0.75, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        ax_l = T("time", 26, GREY).move_to([6.0, y - 1.15, 0])

        def block(x0, x1, label, color):
            r = Rectangle(width=x1 - x0, height=0.9, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18
                          ).move_to([(x0 + x1) / 2, y, 0])
            t = T(label, 26, color).move_to(r)
            return VGroup(r, t)
        b1 = block(-6.5, -3.3, "first week", GREY)
        b2 = block(-3.1, 1.9, "glutamatergic waves", GREY)
        b3 = block(2.1, 6.5, "eye opening", GREY)
        box, ax, axl = sc_panel(0, -1.0, 11.4, 4.4, top=0.9, bot=1.3)
        gk, fk = zone(ax, 2.4, 1.0 / 3.0)
        mut = T("mutant zone, day 8", 26, PINK).move_to([ax.c2p(10, 1.1)[0] - 1.6, ax.c2p(0, 1.1)[1] + 0.35, 0])
        mut.align_to([ax.c2p(10, 1.1)[0], 0, 0], RIGHT)
        broad = T("zone stays broad", 26, TEXT).move_to(ax.c2p(5, 0.33) + UP * 0.9)
        brk = Brace(b1, DOWN, color=TEXT, buff=0.08)
        win = T("an early window", 28, TEXT, weight=BOLD)

        self.play(FadeIn(b1), Create(axis), FadeIn(ax_l), run_time=0.6)
        self.at("waves")
        self.play(FadeIn(b2, shift=RIGHT * 0.2), run_time=0.3)
        self.at("and vision")
        self.play(FadeIn(b3, shift=RIGHT * 0.2), run_time=0.3)
        self.at("did not fix")
        self.play(FadeIn(box), FadeIn(ax), FadeIn(axl), Create(gk), FadeIn(fk), FadeIn(mut), run_time=0.9)
        self.play(FadeIn(broad), run_time=0.4)
        self.at("which points to")
        win.next_to(brk, DOWN, buff=0.1)
        win.align_to(b1, LEFT)
        self.play(b1[0].animate.set_stroke(TEXT, 5).set_fill(TEXT, 0.35), b1[1].animate.set_color(TEXT), GrowFromCenter(brk), run_time=0.5)
        self.play(FadeIn(win), run_time=0.5)
        self.finish()


def lack_static(top_ticks_only=False):
    top = make_raster(0.45, 1.9, 10.8, 2.3, "corr", seed=3)
    bot = make_raster(0.45, -1.5, 10.8, 2.3, "scatter", seed=8)
    lt = T("normal: neighbouring cells fire in sweeps", 26, TEXT).move_to([0.45, 3.4, 0])
    lb = T("mutant: scattered firing", 26, TEXT).move_to([0.45, 0.2, 0])
    sch = T("schematic, spike counts not matched in the experiment", 26, LIGHT).move_to([0.0, -3.5, 0])
    return top, bot, lt, lb, sch


class S10Lack(SpokenScene):
    def construct(self):
        top, bot, lt, lb, sch = lack_static()
        bot.time.move_to([5.5, -3.0, 0])
        tr = ValueTracker(top.x0 - 0.3)
        halfw = 0.3
        band = band_rect(tr, halfw, top.cy, top.h - 0.15)
        ck = VGroup(Line([-0.3, 0.0, 0], [-0.08, -0.3, 0]), Line([-0.08, -0.3, 0], [0.4, 0.34, 0])).set_color(GREEN).set_stroke(width=10)
        ck.scale(0.75).move_to([4.25, 3.38, 0])
        corr = T("correlated", 26, GREEN, weight=BOLD).next_to(ck, RIGHT, buff=0.18)
        lt.scale(0.85).move_to([-1.25, 3.4, 0])
        self.add(top.all, bot.all, lt, lb, sch, top.cells, bot.cells, bot.time)
        self.at("plenty of spikes", lead=0)
        self.play(Indicate(top.ticks, color=YELLOW, scale_factor=1.03), Indicate(bot.ticks, color=YELLOW, scale_factor=1.03), run_time=0.9)
        self.at("the normal", lead=0)
        band_on(top.ticks, tr, halfw, 0.4)
        self.add(band)
        self.play(tr.animate.set_value(top.x1 + 0.3), run_time=1.0, rate_func=linear)
        self.remove(band)
        band_off(top.ticks)
        self.at("between neighbors", lead=0)
        self.play(Create(ck), FadeIn(corr), run_time=0.3)
        self.finish()


class S11Hedge(SpokenScene):
    def construct(self):
        R = make_raster(0.45, 0.85, 10.8, 3.4, "altered", seed=14, nrows=5)
        head = T("later labs: the mutant's waves", 30, TEXT).move_to([0.45, 3.2, 0])
        absent = T("absent", 36, GREY).move_to([-2.4, -1.65, 0])
        cross = Line(absent.get_left() + LEFT * 0.15, absent.get_right() + RIGHT * 0.15, color=RED, stroke_width=5)
        altered = T("altered", 36, YELLOW, weight=BOLD).move_to([2.9, -1.65, 0])
        card = Rectangle(width=10.6, height=2.9, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.1).move_to([0, 0.2, 0])
        c1 = T("the safe claim", 44, TEXT, weight=BOLD).move_to([0, 0.85, 0])
        c2 = T("normal patterning, not spiking alone", 38, YELLOW).move_to([0, -0.15, 0])
        arr_l = Arrow([-6.4, 0.2, 0], [-5.45, 0.2, 0], buff=0, color=TEXT, stroke_width=6)
        arr_r = Arrow([6.4, 0.2, 0], [5.45, 0.2, 0], buff=0, color=TEXT, stroke_width=6)
        narr = T("narrower", 36, TEXT).move_to([0, -2.0, 0])

        # Visible scaffold at the cut, with the rest fading in immediately.
        R.ticks.set_opacity(0.4)
        self.add(R.frame, head, R.ticks)
        sweeps = VGroup()
        rowh = (R.h - 0.5) / 5
        for tc, rows in ((0.10, (0, 1, 2)), (0.43, (1, 2, 3)), (0.74, (2, 3, 4))):
            pts = [[R.x0 + (tc + 0.065 * k + 0.022) * (R.x1 - R.x0),
                    R.cy + R.h / 2 - 0.25 - rowh * (i + 0.5), 0]
                   for k, i in enumerate(rows)]
            sweeps.add(VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 12, opacity=0.22))
        self.play(R.ticks.animate.set_opacity(1), FadeIn(sweeps), FadeIn(R.cells), FadeIn(R.time), run_time=0.45)
        self.at("altered")
        self.play(FadeIn(altered), run_time=0.4)
        self.at("not absent")
        self.play(FadeIn(absent), run_time=0.3)
        self.play(Create(cross), run_time=0.4)
        self.at("safe claim", lead=0)
        self.play(FadeOut(VGroup(head, R.all, R.cells, R.time, sweeps, absent, cross, altered)), FadeIn(card), FadeIn(c1), run_time=0.5)
        self.play(FadeIn(c2), run_time=0.4)
        self.at("narrower")
        self.play(GrowArrow(arr_l), GrowArrow(arr_r), FadeIn(narr), run_time=0.7)
        self.finish()


class S11bClaim(SpokenScene):
    def construct(self):
        R = make_raster(-3.7, 1.45, 5.2, 2.4, "corr", seed=3)
        lab1 = T("normally patterned activity", 26, YELLOW).move_to([-3.7, 3.0, 0])
        R2 = make_raster(-3.7, -1.85, 5.2, 2.4, "scatter", seed=8)
        R2.ticks.set_color(LIGHT)
        lab2 = T("spiking alone", 26, TEXT).move_to([-3.7, -3.4, 0])
        b1, a1, l1 = sc_panel(3.75, 1.45, 5.6, 3.0, top=0.8, bot=1.0)
        b2, a2, l2 = sc_panel(3.75, -1.85, 5.6, 3.0, top=0.8, bot=1.0)
        g1, f1 = zone(a1, 0.8, 1.0)
        g2, f2 = zone(a2, 2.4, 1.0 / 3.0)
        t1 = T("sharp map", 26, TEXT, weight=BOLD).move_to([a1.c2p(10, 1.1)[0] - 0.8, a1.c2p(0, 1.1)[1] + 0.35, 0])
        t2 = T("broad map", 26, TEXT, weight=BOLD).move_to([a2.c2p(10, 1.1)[0] - 0.8, a2.c2p(0, 1.1)[1] + 0.35, 0])
        ar1 = Arrow([-0.95, 1.45, 0], [0.8, 1.45, 0], buff=0, color=YELLOW, stroke_width=6)
        ar2 = Arrow([-0.95, -1.85, 0], [0.8, -1.85, 0], buff=0, color=LIGHT, stroke_width=6)
        need = chip("patterned activity needed early", TEXT, 26).move_to([3.7, 3.45, 0])
        for t in (l1, l2):
            pass

        self.play(FadeIn(R.frame), FadeIn(R.cells), FadeIn(lab1), run_time=0.3)
        self.play(FadeIn(R.ticks, lag_ratio=0.02), run_time=0.8)
        self.at("not just")
        self.play(FadeIn(R2.frame), FadeIn(R2.cells), FadeIn(R2.ticks, lag_ratio=0.01), FadeIn(lab2), run_time=0.7)
        self.at("is needed early")
        self.play(GrowArrow(ar1), FadeIn(b1), FadeIn(a1), FadeIn(l1), Create(g1), FadeIn(f1), FadeIn(t1), FadeIn(need), run_time=1.0)
        self.at("for the map")
        self.play(GrowArrow(ar2), FadeIn(b2), FadeIn(a2), FadeIn(l2), Create(g2), FadeIn(f2), FadeIn(t2), run_time=1.0)
        self.finish()


def build_frog_still(p, with_b=False):
    items = [p["head"], p["eyeA"], p["la"], p["tect"], p["lt"], p["axA"], p["lh"]]
    if with_b:
        items += [p["eyeB"], p["lb"], p["axB"]]
    return items


class S12Frog(SpokenScene):
    def construct(self):
        p = frog_parts()
        self.play(FadeIn(p["head"]), FadeIn(p["lh"]), run_time=0.9)
        self.at("A frog's")
        self.play(FadeIn(p["tect"]), FadeIn(p["lt"]), run_time=0.8)
        self.at("axons")
        self.play(FadeIn(p["eyeA"]), FadeIn(p["la"]), run_time=0.5)
        self.at("from one")
        self.play(Create(p["axA"], lag_ratio=0.2), run_time=0.9)
        self.finish()


class S13Third(SpokenScene):
    def construct(self):
        p = frog_parts()
        cr = credit("Constantine-Paton and Law, 1978", 3.5)
        lh2 = T("frog embryo", 28, LIGHT).move_to(p["lh"].get_center())
        self.add(*build_frog_still(p))
        self.play(FadeIn(cr), run_time=0.6)
        self.at("frog embryos")
        self.play(ReplacementTransform(p["lh"], lh2), run_time=0.5)
        self.at("an extra eye")
        self.play(FadeIn(p["eyeB"], scale=1.4), FadeIn(p["lb"]), run_time=0.8)
        self.at("so two eyes")
        self.play(Create(p["axB"], lag_ratio=0.2), run_time=0.9)
        self.at("shared one")
        self.play(Indicate(p["tect"], color=PURPLE, scale_factor=1.06), run_time=0.8)
        self.finish()


class S14Stripes(SpokenScene):
    def construct(self):
        p = frog_parts()
        tect, stripes, lab = striped_still()
        lab_a = T("alternating stripes", 30, TEXT).move_to([0, 3.45, 0])
        lab_n = T("alternating stripes, where none normally exist", 30, TEXT).move_to([0, 3.45, 0])
        leg = legend_eyes(-2.95)
        lh2 = T("frog embryo", 28, LIGHT).move_to(p["lh"].get_center())
        gone = VGroup(p["head"], p["eyeA"], p["eyeB"], p["la"], p["lb"], p["axA"], p["axB"], lh2, p["lt"])
        self.add(*build_frog_still(p, True), lh2)
        self.remove(p["lh"])
        self.at("The two projections")
        self.play(FadeOut(gone), ReplacementTransform(p["tect"], tect), FadeIn(lab), FadeIn(leg), run_time=1.3)
        self.at("alternating stripes")
        self.play(FadeIn(stripes, lag_ratio=0.12), FadeIn(lab_a), run_time=1.4)
        self.at("where none")
        self.play(ReplacementTransform(lab_a, lab_n), run_time=0.6)
        self.finish()


class S15Apv(SpokenScene):
    def construct(self):
        tect, stripes, lab = striped_still()
        leg = legend_eyes(-2.95)
        cr = credit("Cline, Debski and Constantine-Paton, 1987", 3.5)
        slab, slab_l = sheet_parts()
        ant = T("an NMDA receptor antagonist", 28, RED).move_to([0, -3.55, 0])
        self.add(tect, stripes, lab, leg)
        self.play(FadeIn(cr), run_time=0.6)
        self.at("laid")
        self.play(FadeIn(slab, shift=DOWN * 0.8), run_time=0.7)
        self.at("a pv")
        self.play(FadeIn(slab_l), run_time=0.5)
        self.at("it blocks")
        self.play(FadeIn(ant), run_time=0.6)
        self.finish()


class S16Nmda(SpokenScene):
    def construct(self):
        cy = 0.0
        memL = Rectangle(width=4.2, height=1.4, stroke_width=0, fill_color=GREY, fill_opacity=0.45).move_to([-4.5, cy, 0])
        memR = Rectangle(width=4.2, height=1.4, stroke_width=0, fill_color=GREY, fill_opacity=0.45).move_to([4.5, cy, 0])
        bl = RoundedRectangle(corner_radius=0.2, width=1.9, height=3.6, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                              fill_opacity=0.32).move_to([-1.45, cy, 0])
        br = RoundedRectangle(corner_radius=0.2, width=1.9, height=3.6, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                              fill_opacity=0.32).move_to([1.45, cy, 0])
        out_l = T("outside", 26, LIGHT).move_to([-5.6, 1.5, 0])
        in_l = T("inside", 26, LIGHT).move_to([-5.6, -1.5, 0])
        rec_l = T("NMDA receptor", 30, PURPLE).move_to([-4.3, 2.8, 0])
        rec_ln = Line([-3.0, 2.55, 0], [-2.3, 1.8, 0], color=PURPLE, stroke_width=2)
        pore_l = T("pore", 26, LIGHT).move_to([0, -2.2, 0])
        pore_ln = Line([0, -1.95, 0], [0, -1.3, 0], color=LIGHT, stroke_width=2)
        mg = VGroup(Circle(radius=0.4, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.95), T("Mg", 26, TEXT))
        mg[1].move_to(mg[0])
        mg.move_to([0, cy + 0.0, 0])
        glu = [Dot([x, 3.4, 0], radius=0.3, color=TEXT) for x in (-1.45, 1.45)]
        glu_l = T("glutamate bound", 28, TEXT).move_to([4.5, 2.7, 0])
        little = T("little current", 28, LIGHT).move_to([4.5, 2.0, 0])
        depol = T("membrane depolarized", 26, YELLOW).move_to([4.7, -1.2, 0])
        ca = [Dot([0.0, 3.0 + 0.55 * k, 0], radius=0.2, color=GOLD) for k in range(3)]
        ca_l = T("calcium enters", 28, GOLD).move_to([3.4, -2.4, 0])
        coin = chip("a coincidence detector", PURPLE, 32).move_to([0, -3.45, 0])

        self.play(FadeIn(memL), FadeIn(memR), FadeIn(bl), FadeIn(br), FadeIn(out_l), FadeIn(in_l), FadeIn(rec_l), FadeIn(rec_ln), run_time=0.9)
        self.at("pass little current")
        self.play(FadeIn(mg, scale=1.4), FadeIn(pore_l), FadeIn(pore_ln), run_time=0.7)
        self.at("unless glutamate")
        self.add(*glu)
        self.play(glu[0].animate.move_to([-1.45, 2.2, 0]), glu[1].animate.move_to([1.45, 2.2, 0]), run_time=0.8)
        self.play(FadeIn(glu_l), run_time=0.4)
        self.at("is bound")
        self.play(FadeIn(little), run_time=0.4)
        self.at("the membrane")
        self.play(memL.animate.set_fill(YELLOW, 0.55), memR.animate.set_fill(YELLOW, 0.55), FadeIn(depol), run_time=0.8)
        self.at("already depolarized")
        self.play(mg.animate.move_to([0, 1.1, 0]), FadeOut(little), FadeOut(pore_l), FadeOut(pore_ln), run_time=0.5)
        self.play(mg.animate.move_to([0.9, 3.3, 0]).set_opacity(0.0), run_time=0.5)
        self.add(*ca)
        self.play(*[c.animate.move_to([0.0, -1.55 - 0.45 * k, 0]) for k, c in enumerate(ca)], FadeIn(ca_l), run_time=0.9, lag_ratio=0.2)
        self.at("so they can")
        self.play(FadeIn(coin), run_time=0.6)
        self.finish()


def question_parts():
    q = T("What happens to the stripes while APV is on?", 32, TEXT).move_to([0, -2.6, 0])
    chips = VGroup(chip("stripes kept", GREEN, 26), chip("stripes lost", RED, 26)).arrange(RIGHT, buff=0.9).move_to([0, -3.4, 0])
    return q, chips


def apv_state(scene, leg=False):
    tect, stripes, lab = striped_still()
    slab, slab_l = sheet_parts()
    scene.add(tect, stripes, lab, slab, slab_l)
    return tect, stripes, lab, slab, slab_l


class S17Pq2(SpokenScene):
    def construct(self):
        apv_state(self)
        q, chips = question_parts()
        self.at("what happens")
        self.play(FadeIn(q), run_time=0.6)
        self.at("a pv")
        self.play(FadeIn(chips[0]), run_time=0.4)
        self.play(FadeIn(chips[1]), run_time=0.4)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        apv_state(self)
        q, chips = question_parts()
        self.add(q, chips)
        self.finish()


class S19Rev2(SpokenScene):
    def construct(self):
        tect, stripes, lab, slab, slab_l = apv_state(self)
        q, chips = question_parts()
        self.add(q, chips)
        blue_mix = interpolate_color(ManimColor(BLUE), ManimColor(ORANGE), 0.4)
        orange_mix = interpolate_color(ManimColor(ORANGE), ManimColor(BLUE), 0.4)
        ya, yb = BOX_C[1] + 0.35, BOX_C[1] - 0.35
        x_in = BOX_C[0] - BOX_W / 2
        axa = Line([-6.7, ya, 0], [x_in + 0.05, ya, 0], color=BLUE, stroke_width=5)
        axb = Line([-6.7, yb, 0], [x_in + 0.05, yb, 0], color=ORANGE, stroke_width=5)
        resp = T("retinal\naxons still\nrespond", 26, TEXT).move_to([-5.75, ya + 1.15, 0])
        back = T("stripes return within two weeks", 30, GREEN).move_to([0, -2.8, 0])

        self.play(FadeOut(q), FadeOut(chips), run_time=0.3)
        self.play(*[s.animate.set_fill(blue_mix if i % 2 == 0 else orange_mix, 0.55) for i, s in enumerate(stripes)], run_time=1.1)
        self.at("while the retinal")
        self.play(FadeIn(axa), FadeIn(axb), FadeIn(resp), run_time=0.6)
        self.at("still responded")
        d1 = Dot(axa.get_start(), radius=0.15, color=YELLOW)
        d2 = Dot(axb.get_start(), radius=0.15, color=YELLOW)
        self.add(d1, d2)
        self.play(d1.animate.move_to(axa.get_end()), d2.animate.move_to(axb.get_end()), run_time=0.7, rate_func=linear)
        self.remove(d1, d2)
        self.at("After")
        self.play(FadeOut(axa), FadeOut(axb), FadeOut(resp), FadeOut(slab, shift=UP * 0.8), FadeOut(slab_l), run_time=0.8)
        self.at("the stripes returned")
        self.play(*[s.animate.set_fill(BLUE if i % 2 == 0 else ORANGE, 0.62) for i, s in enumerate(stripes)], FadeIn(back), run_time=1.0)
        self.finish()


class S20Scope(SpokenScene):
    def construct(self):
        lx, rx = -3.5, 3.5
        cy = 0.3
        pw, ph = 6.0, 5.6
        ltb = RoundedRectangle(corner_radius=0.3, width=pw, height=ph, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                               fill_opacity=0.12).move_to([lx, cy, 0])
        n = 8
        sw = (pw - 0.5) / n
        lst = VGroup(*[Rectangle(width=sw, height=ph - 0.5, stroke_width=0, fill_color=(BLUE if i % 2 == 0 else ORANGE), fill_opacity=0.6
                                 ).move_to([lx - (pw - 0.5) / 2 + sw * (i + 0.5), cy, 0]) for i in range(n)])
        l_title = T("frog tectum", 34, PURPLE, weight=BOLD).move_to([lx, 3.5, 0])
        l_text = T("NMDA receptors needed\nto keep the stripes", 28, TEXT).move_to([lx, -3.05, 0])
        rtb = RoundedRectangle(corner_radius=0.3, width=pw, height=ph, stroke_color=GREY, stroke_width=4).move_to([rx, cy, 0])
        rst = VGroup(*[Rectangle(width=sw, height=ph - 0.5, stroke_width=0, fill_color=(BLUE if i % 2 == 0 else ORANGE), fill_opacity=0.6
                                 ).move_to([rx - (pw - 0.5) / 2 + sw * (i + 0.5), cy, 0]) for i in range(n)])
        r_title = T("mammalian LGN", 34, LIGHT, weight=BOLD).move_to([rx, 3.5, 0])
        r_text = T("eye segregation:\ndetector unresolved", 28, TEXT).move_to([rx, -3.05, 0])
        det = chip("detector?", YELLOW, 28).move_to([rx, cy, 0])
        det[0].set_fill(BG, opacity=0.98)

        self.add(ltb, lst, l_title, l_text, rtb, rst, r_title)
        self.at("which detector", lead=0)
        self.play(FadeIn(det, scale=1.2), run_time=0.6)
        self.at("mammalian thalamus")
        self.play(FadeIn(r_text), run_time=0.7)
        self.at("is less clear")
        self.play(Indicate(det, color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.finish()


class S21Take(SpokenScene):
    def construct(self):
        l1 = T("Timing is\nthe address", 44, TEXT, font=TITLE_FONT)
        l2 = T("In the models,\ninputs compete", 32, TEXT)
        l3 = T("Patterned firing, not just\nspike count, matters for\nwhich inputs stay", 32, YELLOW)
        col = VGroup(l1, l2, l3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        col.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT)
        l2.set_opacity(0)
        l3.set_opacity(0)
        # the stage on the right: three inputs, one target cell
        tgt = Circle(radius=0.95, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.28).move_to([5.6, 0, 0])
        tgt_l = T("target cell", 26, PURPLE).move_to([5.6, 1.5, 0])
        ys = [1.9, 0.0, -1.9]
        ins = VGroup(*[cell(3.0, y, BLUE, 0.4) for y in ys])
        names = VGroup(*[T(n, 26, TEXT).move_to([3.0, y, 0]) for n, y in zip("ABC", ys)])
        in_l = T("inputs", 26, BLUE).move_to([3.0, 3.2, 0])
        ends = ([4.75, 0.6, 0], [4.65, 0.0, 0], [4.75, -0.6, 0])
        wires = VGroup(*[Line([3.4, y, 0], e, color=BLUE, stroke_width=4) for y, e in zip(ys, ends)])
        # spike ticks beside each input: A and B in step, C off the beat
        t_step = [0.55, 1.05, 1.55]
        t_off = [0.8, 1.3, 1.85]
        ticks = VGroup()
        for y, ts in zip(ys, (t_step, t_step, t_off)):
            for x in ts:
                ticks.add(Line([x + 0.4, y - 0.3, 0], [x + 0.4, y + 0.3, 0], color=YELLOW, stroke_width=5))
        firing_l = T("firing", 26, YELLOW).move_to([1.7, 3.2, 0])

        self.add(tgt, ins, names, in_l, wires, tgt_l)
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.8)
        self.at("In the models")
        self.play(l2.animate.set_opacity(1), run_time=0.6)
        self.at("inputs compete")
        self.play(Indicate(wires, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("the evidence")
        self.play(l3.animate.set_opacity(1), run_time=0.8)
        self.at("patterned firing")
        self.play(FadeIn(firing_l), FadeIn(ticks, lag_ratio=0.1), run_time=1.2)
        self.play(Indicate(tgt, color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.at("matters for")
        stay = T("stay", 30, GREEN, weight=BOLD).move_to([3.95, 0.6, 0])
        self.play(wires[0].animate.set_stroke(GREEN, width=9), wires[1].animate.set_stroke(GREEN, width=9),
                  wires[2].animate.set_stroke(GREY, width=2, opacity=0.6), FadeIn(stay), run_time=0.9)
        self.finish()


class S22End(EndCard):
    LINE = "Patterned firing, not just spike count, matters for which inputs stay."
