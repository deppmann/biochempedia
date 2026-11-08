"""Mapping the Cortex: Areas and Arealization, chapter 6: One Rule, and Where It Stops  (Biochemistrypedia chaptered film)

Chapters 1 to 6 share one colour map. The recurring picture in this chapter is the cortex as a bar seen from above,
front on the LEFT, back on the RIGHT, cut into three areas (as in the lesson's first film). In the first half each
experiment is shown ONE AT A TIME, large; finished cases shrink into a strip of thumbnails along the bottom.

COLOR MAP (one color per concept, whole chapter series)
  PURPLE = motor area
  GREEN  = somatosensory (touch) area, and its barrels
  PINK   = visual area (also the orientation patches)
  SAND   = auditory area
  ORANGE = Emx2
  BLUE   = Pax6
  YELLOW = FGF8, the signal from the edge (the lamp), and the level curve it makes
  TEAL   = neurons made by the progenitors, and the cortex's own cells
  TEXT   = thalamus and thalamic axons (the input)
  RED    = a blocker / something removed / a result that is not covered
  GREY   = the sheet, progenitors, labels, de-emphasised things
  WHITE  = an arrow showing which way a border moved, and the dashed ghost of where it was
  GOLD   = the frame around what the rule covers; a tile being talked about
"""
import os
import numpy as np
from pathlib import Path
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
SAND = "#D9B77E"
WHITE = "#FFFFFF"
AREA_COL = [PURPLE, GREEN, PINK]
WT = (0.38, 0.70)          # borders of the normal map, as fractions front to back
CARD = "#151922"
LIGHT = "#E3E6EE"          # progenitor dots (a light GREY so they show on dark and orange)


class SS(SpokenScene):
    """SpokenScene that also logs how the scene's last animation compares with the narration length."""

    def finish(self):
        lim = self.narration_s + 0.4
        with open(Path(os.environ["KX_SCRIPT"]).parent / "sync.log", "a") as lg:
            lg.write(f"{os.environ.get('KX_SCENE_ID')}  END at {self.elapsed():6.2f}  limit {lim:6.2f}  "
                     f"{'OVER' if self.elapsed() > lim + 0.05 else 'ok'}\n")
        super().finish()


# ---------------------------------------------------------------------------------------------
# generic pieces
def areas(cx, cy, w, h, b1, b2, op=0.42, sw=2, cols=AREA_COL):
    x0 = cx - w / 2
    xs = [x0, x0 + b1 * w, x0 + b2 * w, x0 + w]
    g = VGroup()
    for i in range(3):
        g.add(Rectangle(width=max(xs[i + 1] - xs[i], 0.01), height=h, stroke_color=cols[i], stroke_width=sw,
                        fill_color=cols[i], fill_opacity=op).move_to([(xs[i] + xs[i + 1]) / 2, cy, 0]))
    return g


def dots(cx, cy, cols=3, rows=2, sp=0.2, r=0.07, color=GREEN, op=0.9):
    g = VGroup()
    for i in range(cols):
        for j in range(rows):
            g.add(Circle(radius=r, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=op).move_to(
                [cx + (i - (cols - 1) / 2) * sp, cy + (j - (rows - 1) / 2) * sp, 0]))
    return g


def glow(x, y, r=0.1, dim=1.0, color=YELLOW):
    if dim <= 0.03:
        return VGroup()
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=color, stroke_width=2.5, stroke_opacity=dim, fill_color=color,
                 fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


def outline_rect(cx, cy, w, h, color=WHITE, sw=5):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def grad_img(cx, cy, w, h, colfun, N=1280):
    """a smooth horizontal gradient as one picture (no seams). colfun(f array) -> (N,3) rgb in 0..1.
    dithered with fine noise so 8-bit steps cannot show as vertical bands."""
    f = (np.arange(N) + 0.5) / N
    col = np.clip(colfun(f), 0, 1)
    rng = np.random.RandomState(7)
    big = np.tile(col[None, :, :], (64, 1, 1)) * 255 + rng.normal(0.0, 1.1, size=(64, N, 3))
    arr = np.clip(np.rint(big), 0, 255).astype(np.uint8)
    im = ImageMobject(arr)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    im.stretch_to_fit_width(w)
    im.stretch_to_fit_height(h)
    return im.move_to([cx, cy, 0])


def fuzzy_img(cx, cy, w, h, b1, b2, sig, op=0.5):
    rgbs = [np.array(color_to_rgb(c)) for c in AREA_COL]
    bgc = np.array(color_to_rgb(BG))

    def cf(f):
        s1 = 1 / (1 + np.exp(np.clip(-(f - b1) / sig, -60, 60)))
        s2 = 1 / (1 + np.exp(np.clip(-(f - b2) / sig, -60, 60)))
        w1, w3 = 1 - s1, s2
        w2 = np.maximum(0.0, 1 - w1 - w3)
        c = (w1[:, None] * rgbs[0] + w2[:, None] * rgbs[1] + w3[:, None] * rgbs[2]) / (w1 + w2 + w3)[:, None]
        return op * c + (1 - op) * bgc
    return grad_img(cx, cy, w, h, cf)


def jig(seed, n, amp):
    rng = np.random.RandomState(seed)
    return rng.uniform(-amp, amp, size=(n, 2))


def mouse_head(s=1.0, c=(0, 0), color=GREY):
    cx, cy = c
    g = VGroup()
    for sx in (-1, 1):
        g.add(Circle(radius=0.34 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15)
              .move_to([cx + sx * 0.62 * s, cy + 0.55 * s, 0]))
    g.add(Ellipse(width=1.5 * s, height=1.2 * s, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
          .move_to([cx, cy, 0]))
    for sx in (-1, 1):
        g.add(Dot([cx + sx * 0.3 * s, cy + 0.15 * s, 0], radius=0.06 * s, color=TEXT))
    g.add(Dot([cx, cy - 0.22 * s, 0], radius=0.1 * s, color=PINK))
    for sx in (-1, 1):
        for dy in (0.14, -0.02, -0.18):
            g.add(Line([cx + sx * 0.3 * s, cy - 0.28 * s, 0], [cx + sx * 1.15 * s, cy - 0.28 * s + dy * s * 1.4, 0],
                       stroke_color=color, stroke_width=2.5))
    return g


# ---------------------------------------------------------------------------------------------
# the case view (scenes 2 to 8): one experiment at a time, big
BX, BY, BWD, BHT = 0.0, 0.85, 10.4, 3.6      # the big map bar (45% of the frame height)
SPEC = {
    0: dict(grid="FGF8 up", title="FGF8 up", lc=YELLOW, b=(0.50, 0.80)),
    1: dict(grid="FGF8 blocked", title="FGF8 blocked", lc=YELLOW, b=(0.26, 0.58)),
    2: dict(grid="second source", title="second source", lc=YELLOW, b=WT),
    3: dict(grid="Emx2 lost", title="Emx2 lost", lc=ORANGE, b=(0.52, 0.86)),
    4: dict(grid="Emx2 raised", title="Emx2 raised", lc=ORANGE, b=(0.28, 0.58)),
    5: dict(grid="no axons", title="no thalamic axons (Gbx2 mutant)", lc=TEXT, b=WT),
    6: dict(grid="graft", title="graft", lc=TEXT, b=WT),
    7: dict(grid="ferret", title="ferret", lc=TEXT, b=WT),
}


def ccols(k):
    return (PURPLE, SAND, PINK) if k == 7 else AREA_COL


def case_title(k):
    s = SPEC[k]
    return fit(T(s["title"], 36, s["lc"], weight=BOLD), max_w=10.0).move_to([0, 3.5, 0])


def fb_marks():
    return VGroup(T("front", 26, GREY).move_to([BX - BWD / 2 + 0.6, 3.0, 0]),
                  T("back", 26, GREY).move_to([BX + BWD / 2 - 0.5, 3.0, 0]))


def big_bar(b1, b2, k=0, with_dots=True):
    g = VGroup(areas(BX, BY, BWD, BHT, b1, b2, op=0.5, sw=3, cols=ccols(k)))
    g.add(Rectangle(width=BWD, height=BHT, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([BX, BY, 0]))
    if with_dots:
        g.add(big_dots(b1, b2))
    return g


def big_dots(b1, b2):
    return dots(BX - BWD / 2 + (b1 + b2) / 2 * BWD, BY - 0.15, 3, 2, 0.75, 0.21)


def area_names(b1, b2, names=("motor", "touch", "vision")):
    xs = [0, b1, b2, 1]
    g = VGroup()
    for i, n in enumerate(names):
        wd = (xs[i + 1] - xs[i]) * BWD
        t = T(n, 26, TEXT)
        if wd < t.width + 0.25:
            continue
        t.move_to([BX - BWD / 2 + (xs[i] + xs[i + 1]) / 2 * BWD, BY + BHT / 2 - 0.42, 0])
        pill = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.18, stroke_width=0, fill_color=BG,
                                fill_opacity=0.6).move_to(t)
        g.add(VGroup(pill, t))
    return g


def ghost_lines():
    return VGroup(*[DashedLine([BX - BWD / 2 + f * BWD, BY - BHT / 2 - 0.12, 0], [BX - BWD / 2 + f * BWD, BY + BHT / 2 + 0.12, 0],
                               dash_length=0.12, color=WHITE, stroke_width=4) for f in WT])


def move_arrow(dirn, text, y=-1.55, x=0.0, lab_dy=-0.55):
    a, b = (x - 1.2, x + 1.2) if dirn > 0 else (x + 1.2, x - 1.2)
    arr = Arrow([a, y, 0], [b, y, 0], buff=0, color=WHITE, stroke_width=10, tip_length=0.32,
                max_tip_length_to_length_ratio=0.35)
    lab = T(text, 28, WHITE).move_to([x, y + lab_dy, 0])
    return arr, lab


def lamp_at(x, d):
    return glow(x, BY, 0.1 + 0.1 * d, d)


def lamp_label(x, text="FGF8"):
    return T(text, 26, YELLOW, weight=BOLD, line_spacing=0.8).move_to([x, BY - 0.9, 0])


LAMP_L, LAMP_R = -6.05, 5.95


def blocker():
    return Rectangle(width=0.12, height=2.0, stroke_color=RED, stroke_width=2, fill_color=RED,
                     fill_opacity=0.95).move_to([-5.42, BY, 0])


def second_dots():
    return dots(BX - BWD / 2 + 0.86 * BWD, BY - 0.15, 2, 2, 0.75, 0.21)


def ramp_pair():
    x0, x1, y = -5.2, 0.8, -2.15
    old = DashedLine([x0, y - 0.30, 0], [x1, y + 0.18, 0], dash_length=0.14, color=ORANGE, stroke_width=5)
    new = Line([x0, y + 0.02, 0], [x1, y + 0.50, 0], color=ORANGE, stroke_width=8)
    return VGroup(old, new)


def ramp_label():
    return T("Emx2 up, same slope", 28, ORANGE, weight=BOLD).move_to([-2.2, -2.92, 0])


def bracket_total():
    y = -1.3
    x0, x1 = BX - BWD / 2, BX + BWD / 2
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=WHITE, stroke_width=5),
                Line([x0, y, 0], [x0, y + 0.18, 0], color=WHITE, stroke_width=5),
                Line([x1, y, 0], [x1, y + 0.18, 0], color=WHITE, stroke_width=5))
    lab = T("same total size", 32, WHITE, weight=BOLD).move_to([3.0, y - 0.38, 0])
    return br, lab


def marker_bar(b1, b2, lines=True):
    """grey bands with white marker lines: what a marker gene shows, not finished areas."""
    g = VGroup(Rectangle(width=BWD, height=BHT, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.22).move_to([BX, BY, 0]))
    if lines:
        for f in (b1, b2):
            g.add(Line([BX - BWD / 2 + f * BWD, BY - BHT / 2, 0], [BX - BWD / 2 + f * BWD, BY + BHT / 2, 0],
                       color=WHITE, stroke_width=6))
    return g


AXX = (-3.2, 0.4, 3.7)


def axons_blocked():
    arrows = VGroup(*[Arrow([x, -2.1, 0], [x, -1.15, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.22,
                            max_tip_length_to_length_ratio=0.4) for x in AXX])
    cross = VGroup(*[VGroup(Line([x - 0.22, -1.85, 0], [x + 0.22, -1.45, 0], color=RED, stroke_width=8),
                            Line([x - 0.22, -1.45, 0], [x + 0.22, -1.85, 0], color=RED, stroke_width=8)) for x in AXX])
    chipt = chip("thalamus", TEXT, 26).move_to([0.2, -2.6, 0])
    return arrows, cross, chipt


def marker_caption():
    g = VGroup(T("marker borders,", 28, WHITE), T("at birth", 28, WHITE)).arrange(DOWN, buff=0.12)
    return g.move_to([BX - BWD / 2 + (WT[0] + WT[1]) / 2 * BWD, BY, 0])


# two-panel view (graft and ferret)
PNX = (-3.45, 3.45)
PNY, PNW, PNH = 0.85, 6.3, 3.0


def panel_bar(k, cx):
    b = WT if k == 6 else (0.28, 0.72)
    g = VGroup(areas(cx, PNY, PNW, PNH, *b, op=0.5, sw=3, cols=ccols(k)))
    g.add(Rectangle(width=PNW, height=PNH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, PNY, 0]))
    return g


def graft_result(cx):
    blk = Rectangle(width=2.6, height=2.3, stroke_color=PINK, stroke_width=4, fill_color=PINK,
                    fill_opacity=0.6).move_to([cx, PNY, 0])
    return VGroup(blk, dots(cx, PNY, 2, 2, 0.8, 0.22))


def ferret_result(cx):
    ticks = VGroup()
    ang = [0.0, 0.8, 1.6, 2.4, 0.4, 1.2, 2.0, 2.8, 0.9]
    n = 0
    for j in range(3):
        for i in range(3):
            m = Line([-0.26, 0, 0], [0.26, 0, 0], color=PINK, stroke_width=7).rotate(ang[n])
            ticks.add(m.move_to([cx + (i - 1) * 0.72, PNY + (1 - j) * 0.8, 0]))
            n += 1
    return ticks


def panel_arrows(cx):
    arr = VGroup(*[Arrow([cx + dx, -2.45, 0], [cx + dx, -0.8, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.25,
                         max_tip_length_to_length_ratio=0.35) for dx in (-0.6, 0.6)])
    lab = T("thalamic input", 28, TEXT).move_to([cx, -2.85, 0])
    return arr, lab


# thumbnails along the bottom
THY = -3.5


def thumb_x(k):
    return -5.425 + k * 1.55


def thumb(k, state):
    x = thumb_x(k)
    b = SPEC[k]["b"] if state == "done" else WT
    g = VGroup(areas(x, THY, 1.3, 0.5, *b, op=0.5, sw=1.5, cols=ccols(k)))
    if state == "active":
        g.add(RoundedRectangle(corner_radius=0.06, width=1.45, height=0.66, stroke_color=GOLD, stroke_width=3,
                               fill_opacity=0).move_to([x, THY, 0]))
    if state == "pending":
        g.set_opacity(0.3)
    if state == "done" and k == 6:
        g.add(Rectangle(width=0.4, height=0.36, stroke_color=PINK, stroke_width=1.5, fill_color=PINK, fill_opacity=0.6).move_to([x, THY, 0]))
    return g


def thumbs(done, active=()):
    g = VGroup()
    for k in range(8):
        st = "done" if k in done else ("active" if k in active else "pending")
        g.add(thumb(k, st))
    return g


def static_case(k):
    """what case k looks like at the end of its scene. returns (bars, rest): bars shrink to a thumbnail, rest fades."""
    s = SPEC[k]
    rest = VGroup()
    if k in (6, 7):
        bars = VGroup()
        for kk, cx in ((6, PNX[0]), (7, PNX[1])):
            bars.add(panel_bar(kk, cx))
            rest.add(graft_result(cx) if kk == 6 else ferret_result(cx))
            ar, lb = panel_arrows(cx)
            rest.add(ar, lb)
        rest.add(T("graft", 36, TEXT, weight=BOLD).move_to([PNX[0], 3.0, 0]),
                 T("ferret", 36, TEXT, weight=BOLD).move_to([PNX[1], 3.0, 0]))
        return bars, rest
    rest.add(case_title(k), fb_marks())
    if k == 5:
        bars = marker_bar(*WT)
        a, c, ch = axons_blocked()
        rest.add(a, c, ch, marker_caption())
        return bars, rest
    b1, b2 = s["b"]
    bars = big_bar(b1, b2, k)
    rest.add(area_names(b1, b2))
    if k in (0, 1, 3, 4):
        rest.add(ghost_lines())
    if k == 0:
        rest.add(lamp_at(LAMP_L, 1.0), lamp_label(LAMP_L))
        a, l = move_arrow(+1, "borders move back")
        rest.add(a, l)
    if k == 1:
        rest.add(lamp_at(LAMP_L, 0.2), lamp_label(LAMP_L), blocker())
        a, l = move_arrow(-1, "borders move forward")
        rest.add(a, l)
    if k == 2:
        rest.add(lamp_at(LAMP_L, 0.45), lamp_label(LAMP_L), lamp_at(LAMP_R, 1.0), lamp_label(LAMP_R, "second\nsource"))
        bars.add(second_dots())
    if k == 3:
        a, l = move_arrow(+1, "borders move back")
        rest.add(a, l)
    if k == 4:
        br, bl = bracket_total()
        a, l = move_arrow(-1, "forward", y=-2.5, x=4.3, lab_dy=0.42)
        rest.add(ramp_pair(), ramp_label(), br, bl, a, l)
    return bars, rest


def retire(scene, k, active=(), run=0.5, extra=()):
    """the finished case k shrinks into its thumbnail; returns the strip of thumbnails (now holding k as done)."""
    bars, rest = static_case(k)
    strip = VGroup(*[thumb(j, "done" if j < k else ("active" if j in active else "pending")) for j in range(8) if j != k])
    scene.add(strip, bars, rest)
    scene.play(FadeOut(rest), bars.animate.scale(1.3 / BWD).move_to([thumb_x(k), THY, 0]), *extra, run_time=run)
    scene.remove(bars)
    strip.add(thumb(k, "done"))
    return strip


# ---------------------------------------------------------------------------------------------
# the tile grid (scenes 1 and 9 only)
TW, TH = 4.1, 1.95
COLX = [-4.3, 0.0, 4.3]
ROWY = [2.025, -0.045, -2.115]
GBW, GBH, GBDY = 3.3, 0.9, -0.2


def slot(k):
    return np.array([COLX[k % 3], ROWY[k // 3], 0.0])


def gframe(c, active=False):
    return RoundedRectangle(corner_radius=0.12, width=TW, height=TH, stroke_color=GOLD if active else GREY,
                            stroke_width=4 if active else 2, fill_color=CARD, fill_opacity=1).move_to(c)


def gtile(k, done):
    c = slot(k)
    s = SPEC[k]
    g = VGroup(gframe(c))
    g.add(T(s["grid"], 26, s["lc"] if done else GREY).move_to([c[0], c[1] + 0.68, 0]))
    by = c[1] + GBDY
    b1, b2 = (s["b"] if done else WT)
    cols = ccols(k)
    xs = [c[0] - GBW / 2, c[0] - GBW / 2 + b1 * GBW, c[0] - GBW / 2 + b2 * GBW, c[0] + GBW / 2]
    if k == 5 and done:
        g.add(Rectangle(width=GBW, height=GBH, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                        fill_opacity=0.22).move_to([c[0], by, 0]))
    else:
        for i in range(3):
            g.add(Rectangle(width=max(xs[i + 1] - xs[i], 0.01), height=GBH, stroke_color=cols[i], stroke_width=2,
                            fill_color=cols[i], fill_opacity=0.45 if done else 0.3).move_to([(xs[i] + xs[i + 1]) / 2, by, 0]))
    g.add(Rectangle(width=GBW, height=GBH, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([c[0], by, 0]))
    if not done:
        return g
    gx = lambda f: c[0] - GBW / 2 + f * GBW
    if k <= 4:
        g.add(dots(gx((b1 + b2) / 2), by, 3, 2, 0.28, 0.08))
    if k in (0, 1, 3, 4):
        for f in WT:
            g.add(DashedLine([gx(f), by - GBH / 2 - 0.06, 0], [gx(f), by + GBH / 2 + 0.06, 0], dash_length=0.06, color=WHITE,
                             stroke_width=2.5))
        d = +1 if k in (0, 3) else -1
        ax = c[0]
        a, b = (ax - 0.5, ax + 0.5) if d > 0 else (ax + 0.5, ax - 0.5)
        g.add(Arrow([a, c[1] - 0.8, 0], [b, c[1] - 0.8, 0], buff=0, color=WHITE, stroke_width=6, tip_length=0.2,
                    max_tip_length_to_length_ratio=0.4))
    if k == 2:
        g.add(dots(gx(0.86), by, 2, 2, 0.28, 0.08))
    if k == 5:
        for f in WT:
            g.add(Line([gx(f), by - GBH / 2, 0], [gx(f), by + GBH / 2, 0], color=WHITE, stroke_width=3.5))
    if k in (5, 6, 7):
        tx = gx((0.5 if k == 5 else 0.54))
        for dx in ((-0.9, 0.0, 0.9) if k == 5 else (-0.25, 0.25)):
            g.add(Arrow([tx + dx, c[1] - 0.93, 0], [tx + dx, c[1] - 0.62, 0], buff=0, color=TEXT, stroke_width=4,
                        tip_length=0.12, max_tip_length_to_length_ratio=0.5))
    if k == 5:
        for dx in (-0.9, 0.0, 0.9):
            x = gx(0.5) + dx
            g.add(Line([x - 0.1, c[1] - 0.86, 0], [x + 0.1, c[1] - 0.68, 0], color=RED, stroke_width=4),
                  Line([x - 0.1, c[1] - 0.68, 0], [x + 0.1, c[1] - 0.86, 0], color=RED, stroke_width=4))
    if k == 6:
        g.add(Rectangle(width=0.9, height=0.7, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.55).move_to(
            [gx(0.54), by, 0]), dots(gx(0.54), by, 3, 2, 0.24, 0.07))
    if k == 7:
        for i, ang in enumerate((0.0, 0.7, 1.4, 2.1, 2.8)):
            m = Line([-0.12, 0, 0], [0.12, 0, 0], color=PINK, stroke_width=4.5).rotate(ang)
            g.add(m.move_to([gx(0.54) + (i - 2) * 0.19, by + (0.14 if i % 2 else -0.14), 0]))
    return g


def legend():
    c = slot(8)
    g = VGroup()
    for i, (t, col) in enumerate((("motor", PURPLE), ("touch", GREEN), ("vision", PINK), ("auditory", SAND))):
        sw = Rectangle(width=0.45, height=0.28, stroke_color=col, stroke_width=2, fill_color=col,
                       fill_opacity=0.5).move_to([c[0] - 0.95, c[1] + 0.78 - i * 0.4, 0])
        g.add(sw, T(t, 26, TEXT).next_to(sw, RIGHT, buff=0.2))
    g.add(T("left = front", 26, GREY).move_to([c[0], c[1] - 0.82, 0]))
    return g


def question(text, size=34):
    return fit(T(text, size, TEXT), max_w=12.2).move_to([0, 3.42, 0])


def full_grid(done=True):
    return VGroup(*[gtile(k, done) for k in range(8)])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "One Rule, and Where It Stops"


# ---------------------------------------------------------------------------------------------
class S01(SS):
    """eight labelled tiles: a menu of experiments; the question on top."""

    def construct(self):
        tiles = [gtile(k, False) for k in range(8)]
        leg = legend()
        self.at("moved borders")
        self.play(LaggedStart(*[FadeIn(t, scale=0.9) for t in tiles], lag_ratio=0.14), run_time=1.9)
        self.play(FadeIn(leg), run_time=0.5)
        q = question("Can one idea tie the results together?")
        self.at("can one idea")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        self.at("tie the results")
        self.play(*[t[0].animate.set_stroke(GOLD, 4) for t in tiles], run_time=0.5)
        self.play(*[t[0].animate.set_stroke(GREY, 2) for t in tiles], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def start_case(scene, k, prev_k=None, zoom=False):
    """sets up the live pieces of case k (neutral state) and returns a dict of trackers and mobjects."""
    d = {}
    d["b1"], d["b2"] = ValueTracker(WT[0]), ValueTracker(WT[1])
    live_bar = always_redraw(lambda: big_bar(d["b1"].get_value(), d["b2"].get_value(), k, with_dots=False))
    live_names = always_redraw(lambda: area_names(d["b1"].get_value(), d["b2"].get_value()))
    d["dots"] = always_redraw(lambda: big_dots(d["b1"].get_value(), d["b2"].get_value()))
    d["names"] = live_names
    title, fb = case_title(k), fb_marks()
    st_bar, st_names = big_bar(*WT, k=k), area_names(*WT)
    if zoom:
        # the first case: the grid, then its tile zooms to fill the frame
        grid = VGroup(*[gtile(j, False) for j in range(8)])
        scene.add(grid)
        snap = VGroup(st_bar, st_names, title, fb)
        snap.save_state()
        snap.scale(0.3).move_to(slot(k))
        snap.set_opacity(0.0)
        strip = thumbs(done=(), active=(k,))
        scene.play(FadeOut(grid), Restore(snap), FadeIn(strip), run_time=0.8)
        scene.remove(snap)
        scene.add(live_bar, d["dots"], live_names, title, fb)
        d["strip"] = strip
        return d
    d["strip"] = retire(scene, prev_k, active=(k,), extra=(FadeIn(st_bar), FadeIn(st_names), FadeIn(title), FadeIn(fb)))
    scene.remove(st_bar, st_names)
    scene.add(live_bar, d["dots"], live_names)
    return d


def ghost_on(scene, d):
    """the dashed ghost of the old borders, drawn under the area names and the barrels; returns the fade-in animation."""
    gh = ghost_lines()
    gh.set_opacity(0.0)
    scene.add(gh, d["dots"], d["names"])
    return gh.animate.set_opacity(1.0)


class S02(SS):
    def construct(self):
        k = 0
        d = start_case(self, k, zoom=True)
        lf = ValueTracker(0.45)
        lamp = always_redraw(lambda: lamp_at(LAMP_L, lf.get_value()))
        lab = lamp_label(LAMP_L)
        self.add(lamp)
        self.play(FadeIn(lab), run_time=0.3)
        self.at("at the front")
        self.play(lf.animate.set_value(1.0), Indicate(lab, color=YELLOW, scale_factor=1.15), run_time=0.8)
        gha = ghost_on(self, d)
        self.at("the barrel field")
        self.play(gha, d["b1"].animate.set_value(SPEC[k]["b"][0]), d["b2"].animate.set_value(SPEC[k]["b"][1]), run_time=0.9)
        a, l = move_arrow(+1, "borders move back")
        self.at("moved back")
        self.play(GrowArrow(a), FadeIn(l), run_time=0.5)
        self.finish()


class S03(SS):
    def construct(self):
        k = 1
        d = start_case(self, k, prev_k=0)
        lf = ValueTracker(0.45)
        lamp = always_redraw(lambda: lamp_at(LAMP_L, lf.get_value()))
        lab = lamp_label(LAMP_L)
        self.add(lamp)
        self.play(FadeIn(lab), run_time=0.2)
        bl = blocker()
        self.at("blocked")
        self.play(FadeIn(bl, shift=RIGHT * 0.1), lf.animate.set_value(0.2), run_time=0.5)
        gha = ghost_on(self, d)
        self.at("it moved forward")
        self.play(gha, d["b1"].animate.set_value(SPEC[k]["b"][0]), d["b2"].animate.set_value(SPEC[k]["b"][1]), run_time=0.7)
        a, l = move_arrow(-1, "borders move forward")
        self.play(GrowArrow(a), FadeIn(l), run_time=0.4)
        self.finish()


class S04(SS):
    def construct(self):
        k = 2
        d = start_case(self, k, prev_k=1)
        lamp = lamp_at(LAMP_L, 0.45)
        lab = lamp_label(LAMP_L)
        self.add(lamp)
        self.play(FadeIn(lab), run_time=0.2)
        self.at("at the back")
        lb = lamp_at(LAMP_R, 1.0)
        self.play(FadeIn(lb, scale=0.5), FadeIn(lamp_label(LAMP_R, "second\nsource")), run_time=0.6)
        sd = second_dots()
        self.at("a partial second")
        self.play(FadeIn(sd, lag_ratio=0.2), run_time=0.8)
        pl = T("partial second field", 28, GREEN).move_to([3.4, -1.55, 0])
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S05(SS):
    def construct(self):
        k = 3
        d = start_case(self, k, prev_k=2)
        gha = ghost_on(self, d)
        self.at("the front and middle")
        self.play(gha, d["b1"].animate.set_value(SPEC[k]["b"][0]), d["b2"].animate.set_value(SPEC[k]["b"][1]), run_time=1.3)
        a, l = move_arrow(+1, "borders move back")
        self.at("grew back")
        self.play(GrowArrow(a), FadeIn(l), run_time=0.5)
        b1, b2 = SPEC[k]["b"]
        vx = BX - BWD / 2 + (1 + b2) / 2 * BWD
        hl = outline_rect(vx, BY, (1 - b2) * BWD, BHT, PINK, 7)
        self.at("the visual area shrank")
        self.play(Create(hl), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(hl), run_time=0.4)
        self.finish()


class S06(SS):
    def construct(self):
        k = 4
        d = start_case(self, k, prev_k=3)
        rp, rl = ramp_pair(), ramp_label()
        self.at("same slope")
        self.play(Create(rp), FadeIn(rl), run_time=0.9)
        gha = ghost_on(self, d)
        self.at("the visual area grew")
        self.play(gha, d["b1"].animate.set_value(SPEC[k]["b"][0]), d["b2"].animate.set_value(SPEC[k]["b"][1]), run_time=1.0)
        a, l = move_arrow(-1, "forward", y=-2.5, x=4.3, lab_dy=0.42)
        self.play(GrowArrow(a), FadeIn(l), run_time=0.4)
        br, bl = bracket_total()
        self.at("total size unchanged")
        self.play(Create(br), FadeIn(bl), run_time=0.9)
        self.finish()


class S07(SS):
    def construct(self):
        k = 5
        bar = marker_bar(*WT)
        cap = marker_caption()
        title, fb = case_title(k), fb_marks()
        self.add(bar, cap, title, fb, thumbs(done=tuple(range(5)), active=(k,)))
        arrows, cross, chipt = axons_blocked()
        self.at("thalamic axons")
        self.play(FadeIn(chipt), FadeIn(arrows), run_time=0.4)
        self.play(FadeIn(cross, scale=1.4), run_time=0.4)
        lines = bar[1:]
        self.at("marker borders")
        self.play(Indicate(lines, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("in place at birth")
        self.play(Indicate(lines, color=WHITE, scale_factor=1.0), run_time=0.9)
        self.finish()


class S08(SS):
    def construct(self):
        bars = [panel_bar(6, PNX[0]), panel_bar(7, PNX[1])]
        titles = [T("graft", 36, TEXT, weight=BOLD).move_to([PNX[0], 3.0, 0]), T("ferret", 36, TEXT, weight=BOLD).move_to([PNX[1], 3.0, 0])]
        retire(self, 5, active=(6, 7), extra=tuple(FadeIn(m) for m in bars + titles))
        pa = [panel_arrows(PNX[0]), panel_arrows(PNX[1])]
        self.at("input")
        self.play(*[GrowArrow(a) for p in pa for a in p[0]], *[FadeIn(p[1]) for p in pa], run_time=0.6)
        gr = graft_result(PNX[0])
        self.at("barrels in grafted")
        self.play(FadeIn(gr[0], scale=0.7), run_time=0.6)
        self.play(FadeIn(gr[1], lag_ratio=0.15), run_time=0.8)
        fr = ferret_result(PNX[1])
        self.at("and an orientation map")
        self.play(FadeIn(fr, lag_ratio=0.1), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pax_back_card(scale=1.0):
    c = slot(8)
    fr = RoundedRectangle(corner_radius=0.12, width=TW, height=TH, stroke_color=GREY, stroke_width=3,
                          fill_color="#1c2230", fill_opacity=1)
    return VGroup(fr, T("?", 64, GREY, weight=BOLD)).move_to(c)


def think_bar(frac=1.0):
    g = VGroup(Rectangle(width=8.0, height=0.14, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([0.6, -3.5, 0]),
               T("think", 26, GREY).move_to([-4.9, -3.5, 0]))
    if frac > 0.01:
        g.add(Rectangle(width=8.0 * frac, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(
            [0.6 - 4.0 + 4.0 * frac, -3.5, 0]))
    return g


Q2 = "Which factor's loss and gain did not mirror?"


class S09(SS):
    def construct(self):
        grid = full_grid()
        q2 = question(Q2)
        self.play(FadeIn(grid), FadeIn(q2, shift=DOWN * 0.15), run_time=0.5)
        pairs = VGroup(*[gframe(slot(k), True).set_fill(opacity=0) for k in (0, 1, 3, 4)])
        self.at("loss and gain")
        self.play(Create(pairs), run_time=0.6)
        back = pax_back_card()
        self.at("did not mirror")
        self.play(FadeOut(pairs), FadeIn(back, scale=0.7), run_time=0.6)
        self.play(Indicate(back[1], color=TEXT, scale_factor=1.25), run_time=0.7)
        self.finish()


class S10Pause(NarratedScene):
    """the question holds, still, while the viewer thinks: the tiles stay readable, a bar fills over the 5 s."""

    def construct(self):
        self.add(full_grid(), question(Q2), pax_back_card())
        fr = ValueTracker(0.0)
        bar = always_redraw(lambda: think_bar(fr.get_value()))
        self.add(bar)
        self.play(fr.animate.set_value(1.0), run_time=4.6, rate_func=linear)
        self.finish()


def pax_card_back_big():
    fr = RoundedRectangle(corner_radius=0.18, width=12.4, height=6.0, stroke_color=GREY, stroke_width=3,
                          fill_color="#1c2230", fill_opacity=1).move_to([0, -0.05, 0])
    return VGroup(fr, T("?", 130, GREY, weight=BOLD).move_to([0, -0.05, 0]))


PXL, PXG = -3.1, 3.1
PXY, PXW, PXH = 0.25, 5.4, 2.9


def pax_bar(cx, b1, b2, lines=True):
    g = VGroup(Rectangle(width=PXW, height=PXH, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.22).move_to([cx, PXY, 0]))
    for f in (b1, b2):
        g.add(Line([cx - PXW / 2 + f * PXW, PXY - PXH / 2, 0], [cx - PXW / 2 + f * PXW, PXY + PXH / 2, 0], color=WHITE, stroke_width=6))
    g.add(T("markers", 26, WHITE).move_to([cx - PXW / 2 + 0.74, PXY + PXH / 2 - 0.4, 0]))
    return g


class S11(SS):
    def construct(self):
        grid = full_grid()
        q = question(Q2)
        back = pax_back_card()
        tb = think_bar(1.0)
        self.add(grid, q, back, tb)
        big = pax_card_back_big()
        self.play(FadeOut(grid), FadeOut(q), FadeOut(tb), ReplacementTransform(back, big), run_time=0.7)
        frame = RoundedRectangle(corner_radius=0.18, width=12.4, height=6.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=CARD, fill_opacity=1).move_to([0, -0.05, 0])
        label = T("Pax6", 44, BLUE, weight=BOLD).move_to([0, 2.55, 0])
        capL = T("loss", 34, TEXT).move_to([PXL, 2.0, 0])
        capG = T("gain", 34, TEXT).move_to([PXG, 2.0, 0])
        barL, barG = pax_bar(PXL, *WT), pax_bar(PXG, *WT)
        div = Line([0, 2.2, 0], [0, -2.9, 0], color=GREY, stroke_width=1.5)
        front = VGroup(frame, label, capL, capG, barL, barG, div)
        front.stretch(0.02, 0)
        self.play(big.animate.stretch(0.02, 0), run_time=0.3)
        self.remove(big)
        self.add(front)
        self.play(front.animate.stretch(50, 0), run_time=0.4)
        gl = DashedLine([PXL - PXW / 2 + WT[0] * PXW, PXY - PXH / 2 - 0.1, 0], [PXL - PXW / 2 + WT[0] * PXW, PXY + PXH / 2 + 0.1, 0],
                        dash_length=0.1, color=WHITE, stroke_width=3)
        gl2 = DashedLine([PXL - PXW / 2 + WT[1] * PXW, PXY - PXH / 2 - 0.1, 0], [PXL - PXW / 2 + WT[1] * PXW, PXY + PXH / 2 + 0.1, 0],
                         dash_length=0.1, color=WHITE, stroke_width=3)
        newL = pax_bar(PXL, 0.26, 0.58)
        arrowL = Arrow([PXL + 0.9, -1.75, 0], [PXL - 0.9, -1.75, 0], buff=0, color=WHITE, stroke_width=9, tip_length=0.28,
                       max_tip_length_to_length_ratio=0.35)
        txtL = T("markers shifted", 32, WHITE).move_to([PXL, -2.5, 0])
        self.at("losing it shifted")
        self.play(FadeIn(VGroup(gl, gl2)), Transform(barL, newL), GrowArrow(arrowL), run_time=1.0)
        self.play(FadeIn(txtL), run_time=0.4)
        newG = pax_bar(PXG, WT[0] + 0.02, WT[1] + 0.02)
        lineG = Line([PXG - 0.8, -1.75, 0], [PXG + 0.8, -1.75, 0], color=WHITE, stroke_width=8)
        txtG = T("barely moved", 32, WHITE).move_to([PXG, -2.5, 0])
        self.at("raising it")
        self.play(Transform(barG, newG), Create(lineG), FadeIn(txtG), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rule_lines(y1, y2, size=44, c1=TEXT, c2=TEXT):
    l1 = T("Position draws the sketch;", size, c1, font=TITLE_FONT).move_to([0, y1, 0])
    l2 = T("input finishes it.", size, c2, font=TITLE_FONT).move_to([0, y2, 0])
    return l1, l2


class S12(SS):
    def construct(self):
        sig = ValueTracker(0.08)
        cy, w, h = -0.2, 10.4, 3.6
        mp = always_redraw(lambda: fuzzy_img(0, cy, w, h, WT[0], WT[1], sig.get_value(), op=0.55))
        outline = outline_rect(0, cy, w, h, GREY, 3)
        l1, l2 = rule_lines(3.4, 2.75, 38, GREY, GREY)
        l1.set_color(TEXT)
        l2.set_color(TEXT)
        self.add(mp, l1, l2, outline)
        sk = chip("the sketch", GOLD, 30).move_to([0, 1.95, 0])
        self.at("the sketch")
        self.play(Indicate(l1, color=GOLD, scale_factor=1.05), FadeIn(sk, shift=DOWN * 0.1), run_time=0.5)
        thal = chip("thalamus", TEXT, 28).move_to([0, -3.4, 0])
        axons = VGroup(*[Arrow([sx * 0.5, -3.05, 0], [x, cy - h / 2, 0], buff=0, color=TEXT, stroke_width=6,
                               tip_length=0.2, max_tip_length_to_length_ratio=0.25) for sx, x in ((-1, -3.2), (0, 0.0), (1, 3.2))])
        inl = T("input", 30, TEXT).move_to([1.1, -2.45, 0])
        self.at("input finishes it")
        self.play(Indicate(l2, color=GOLD, scale_factor=1.05), FadeIn(thal), FadeIn(inl),
                  LaggedStart(*[GrowArrow(a) for a in axons], lag_ratio=0.2), run_time=0.8)
        self.play(sig.animate.set_value(0.004), run_time=0.85)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the level plot (scenes 13 to 15): two thresholds, three bands, K = 1 / (a fifth of the sheet)
K_DECAY = 5.0
T1, T2 = float(np.exp(-WT[0] * K_DECAY)), float(np.exp(-WT[1] * K_DECAY))
B_SECOND = T2 * 1.0
PX0, PW = -4.2, 9.2
PBASE, PSC, YCAP = -3.15, 3.7, 1.3
BARY, BARH = 3.0, 0.9


def lev(f, A, B=0.0):
    return A * np.exp(-K_DECAY * f) + B * np.exp(-K_DECAY * (1 - f))


def crossings(A, B):
    """returns [(f, threshold_index)] where the level crosses a threshold."""
    fs = np.linspace(0, 1, 1201)
    out = []
    for ti, T_ in enumerate((T1, T2)):
        L = lev(fs, A, B) - T_
        for i in range(1200):
            if (L[i] > 1e-12) != (L[i + 1] > 1e-12):
                out.append((fs[i] + L[i] / (L[i] - L[i + 1]) / 1200, ti))
    return out


def band_of(level):
    return 0 if level > T1 else (1 if level > T2 else 2)


def bands_bar(A, B, cy=BARY, h=BARH):
    edges = [0.0] + sorted(f for f, _ in crossings(A, B)) + [1.0]
    g = VGroup()
    for i in range(len(edges) - 1):
        mid = (edges[i] + edges[i + 1]) / 2
        col = AREA_COL[band_of(lev(mid, A, B))]
        w = (edges[i + 1] - edges[i]) * PW
        g.add(Rectangle(width=max(w, 0.01), height=h, stroke_color=col, stroke_width=2, fill_color=col,
                        fill_opacity=0.5).move_to([PX0 + (edges[i] + edges[i + 1]) / 2 * PW, cy, 0]))
    g.add(Rectangle(width=PW, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([PX0 + PW / 2, cy, 0]))
    return g


def curve(A, B):
    f0 = 0.0
    if A > YCAP:
        f0 = np.log(A / YCAP) / K_DECAY
    fs = np.linspace(f0, 1, 100)
    pts = [[PX0 + f * PW, PBASE + lev(f, A, B) * PSC, 0] for f in fs]
    m = VMobject(stroke_color=YELLOW, stroke_width=6)
    m.set_points_smoothly(pts)
    return m


def cross_marks(A, B):
    g = VGroup()
    for f, ti in crossings(A, B):
        x = PX0 + f * PW
        yt = PBASE + (T1, T2)[ti] * PSC
        g.add(DashedLine([x, yt, 0], [x, BARY - BARH / 2, 0], dash_length=0.12, color=WHITE, stroke_width=2.5))
        g.add(Dot([x, yt, 0], radius=0.11, color=WHITE))
    return g


def plot_static():
    ax = VGroup(
        Line([PX0, PBASE, 0], [PX0 + PW + 0.1, PBASE, 0], color=GREY, stroke_width=3),
        Line([PX0, PBASE, 0], [PX0, PBASE + 4.9, 0], color=GREY, stroke_width=3),
        T("front", 26, GREY).move_to([PX0 + 0.5, PBASE - 0.38, 0]),
        T("back", 26, GREY).move_to([PX0 + PW - 0.45, PBASE - 0.38, 0]),
        T("FGF8 level", 26, YELLOW).rotate(PI / 2).move_to([PX0 - 0.45, PBASE + 2.2, 0]),
    )
    thr = VGroup()
    for T_ in (T1, T2):
        yt = PBASE + T_ * PSC
        thr.add(DashedLine([PX0, yt, 0], [PX0 + PW, yt, 0], dash_length=0.14, color=WHITE, stroke_width=2.5),
                T("threshold", 26, WHITE).move_to([PX0 + PW + 0.92, yt, 0]))
    return ax, thr


def corner_chips(toy=False):
    g = VGroup(chip("working\nmodel", GOLD, 24, pad=0.14).move_to([6.0, 3.0, 0]))
    if toy:
        g.add(chip("toy\nmodel", GOLD, 24, pad=0.14).move_to([6.0, 1.95, 0]))
    return g


LAMPY = -0.8
LAMP1X, LAMP2X = -5.85, 5.85


def lamp1(A):
    return glow(LAMP1X, LAMPY, 0.14 + 0.07 * min(A, 2.2), min(1.0, A / 1.4))


def lamp1_label():
    return T("FGF8\ndose", 26, YELLOW, weight=BOLD, line_spacing=0.8).move_to([LAMP1X, LAMPY - 0.95, 0])


class S13(SS):
    def construct(self):
        x0, w = -4.6, 9.6
        sheet = Rectangle(width=w, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.22).move_to([x0 + w / 2, 3.0, 0])
        fb = VGroup(T("front", 26, GREY).move_to([x0 + 0.5, 2.0, 0]), T("back", 26, GREY).move_to([x0 + w - 0.45, 2.0, 0]))
        prog = VGroup(*[Circle(radius=0.22, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.6).move_to(
            [x0 + (i + 0.5) / 14 * w, 3.0 + (0.22 if i % 2 else -0.22), 0]) for i in range(14)])
        fcur = 0.3
        top = VGroup(sheet, fb, prog)
        c0 = top.get_center().copy()
        top.scale(1.3).move_to([0.2, 0.9, 0])
        self.play(FadeIn(sheet), FadeIn(fb), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in prog], lag_ratio=0.04), run_time=0.7)
        cell = prog[int(fcur * 14)]
        pl = T("this progenitor", 30, WHITE)
        self.at("position")
        self.play(cell.animate.set_fill(WHITE, 1.0).set_stroke(WHITE), run_time=0.4)
        pl.next_to(cell, DOWN, buff=0.55)
        pline = Line(cell.get_bottom(), pl.get_top() + UP * 0.02, color=WHITE, stroke_width=2.5)
        self.play(FadeIn(pl, shift=UP * 0.1), Create(pline), run_time=0.4)
        cx_final = x0 + (int(fcur * 14) + 0.5) / 14 * w
        # gauges
        gb = -2.75
        gxy, gxo = 1.2, 4.5
        slotY = Rectangle(width=1.3, height=2.2, stroke_color=YELLOW, stroke_width=3, fill_opacity=0).move_to([gxy, gb + 1.1, 0])
        slotO = Rectangle(width=1.3, height=2.2, stroke_color=ORANGE, stroke_width=3, fill_opacity=0).move_to([gxo, gb + 1.1, 0])
        cap = T("this cell's levels", 28, TEXT).move_to([3.2, -0.1, 0])
        self.at("recorded as levels")
        self.play(FadeOut(pl), FadeOut(pline), top.animate.scale(1 / 1.3).move_to(c0), run_time=0.6)
        cx = cell.get_center()[0]
        self.play(FadeIn(slotY), FadeIn(slotO), FadeIn(cap), run_time=0.5)
        # the lamp and its strip
        fl = np.exp(-4.5 * fcur)
        sy = 1.35
        ystrip = grad_img(x0 + w / 2, sy, w, 0.65, lambda f: np.array([color_to_rgb(YELLOW)]) * (0.06 + 0.85 * np.exp(-4.5 * f))[:, None]
                          + np.array([color_to_rgb(BG)]) * (1 - (0.06 + 0.85 * np.exp(-4.5 * f)))[:, None])
        ys_out = outline_rect(x0 + w / 2, sy, w, 0.65, GREY, 2)
        lamp = glow(-5.55, sy, 0.22)
        lab_y = T("FGF8", 26, YELLOW, weight=BOLD).move_to([x0 + w + 0.85, sy, 0])
        dotY = Dot([cx, sy, 0], radius=0.12, color=WHITE)
        fillY = Rectangle(width=1.3, height=2.2 * fl, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([gxy, gb + 1.1 * fl, 0])
        nameY = T("FGF8\n(signal)", 26, YELLOW, line_spacing=0.8).move_to([gxy, -3.3, 0])
        self.at("graded signals")
        self.play(FadeIn(lamp, scale=0.5), FadeIn(ystrip), FadeIn(ys_out), FadeIn(lab_y), FadeIn(dotY), run_time=0.6)
        self.play(FadeIn(fillY, shift=UP * 0.2), FadeIn(nameY), run_time=0.5)
        em = 0.05 + 0.85 * fcur
        oy = 0.55
        ostrip = grad_img(x0 + w / 2, oy, w, 0.65, lambda f: np.array([color_to_rgb(ORANGE)]) * (0.05 + 0.85 * f * 0.9)[:, None]
                          + np.array([color_to_rgb(BG)]) * (1 - (0.05 + 0.85 * f * 0.9))[:, None])
        os_out = outline_rect(x0 + w / 2, oy, w, 0.65, GREY, 2)
        lab_o = T("Emx2", 26, ORANGE, weight=BOLD).move_to([x0 + w + 0.85, oy, 0])
        dotO = Dot([cx, oy, 0], radius=0.12, color=WHITE)
        cur = Line([cx, 2.3, 0], [cx, oy - 0.33, 0], color=WHITE, stroke_width=3)
        fillO = Rectangle(width=1.3, height=2.2 * em, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to([gxo, gb + 1.1 * em, 0])
        nameO = T("Emx2\n(transcription factor)", 26, ORANGE, line_spacing=0.8).move_to([gxo, -3.3, 0])
        self.at("transcription factors")
        self.play(FadeIn(ostrip), FadeIn(os_out), FadeIn(lab_o), FadeIn(dotO), Create(cur), run_time=0.7)
        self.play(FadeIn(fillO, shift=UP * 0.2), FadeIn(nameO), run_time=0.5)
        self.finish()


class S14(SS):
    def construct(self):
        A = ValueTracker(1.0)
        ax, thr = plot_static()
        chipw = corner_chips()
        lamp = always_redraw(lambda: lamp1(A.get_value()))
        lamp_lab = lamp1_label()
        cv = always_redraw(lambda: curve(A.get_value(), 0.0))
        bar = always_redraw(lambda: bands_bar(A.get_value(), 0.0))
        cm = always_redraw(lambda: cross_marks(A.get_value(), 0.0))
        bar_names = VGroup(T("front", 26, GREY).move_to([PX0 + 0.5, BARY + 0.68, 0]), T("back", 26, GREY).move_to([PX0 + PW - 0.45, BARY + 0.68, 0]))
        self.add(bar)
        self.play(FadeIn(bar_names), FadeIn(ax), run_time=0.5)
        self.at("working model")
        self.add(cv, lamp)
        self.play(FadeIn(chipw), FadeIn(lamp, scale=0.5), FadeIn(lamp_lab), Create(cv), run_time=1.0)
        self.at("a border falls")
        self.add(cm)
        self.play(FadeIn(thr), FadeIn(cm), run_time=0.9)
        self.at("crosses a threshold")
        self.play(Indicate(cm, color=WHITE, scale_factor=1.0), run_time=0.9)
        # ghost of the first border and an arrow that follows it
        xs0 = PX0 + crossings(1.0, 0.0)[0][0] * PW
        ghost = DashedLine([xs0, BARY - BARH / 2 - 0.05, 0], [xs0, BARY + BARH / 2 + 0.05, 0], dash_length=0.1, color=WHITE, stroke_width=4)
        ay = BARY - BARH / 2 - 0.3

        def arr():
            xn = PX0 + [f for f, ti in crossings(A.get_value(), 0.0) if ti == 0][0] * PW
            if abs(xn - xs0) < 0.12:
                return VGroup()
            return Arrow([xs0, ay, 0], [xn, ay, 0], buff=0, color=WHITE, stroke_width=7, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        ar = always_redraw(arr)
        self.at("change the dose")
        self.add(ar)
        self.play(FadeIn(ghost), A.animate.set_value(0.45), run_time=1.1)
        self.at("the border slides")
        self.play(A.animate.set_value(2.2), run_time=1.3)
        self.finish()


class S15(SS):
    def construct(self):
        B = ValueTracker(0.0)
        ax, thr = plot_static()
        chipw = corner_chips()
        toy = chip("toy\nmodel", GOLD, 24, pad=0.14).move_to([6.0, 1.95, 0])
        lamp = lamp1(1.0)
        lamp_lab = lamp1_label()
        lamp2_lab = T("second\nsource", 26, YELLOW, weight=BOLD, line_spacing=0.8).move_to([LAMP2X - 0.05, LAMPY - 0.95, 0])
        cv = always_redraw(lambda: curve(1.0, B.get_value()))
        bar = always_redraw(lambda: bands_bar(1.0, B.get_value()))
        cm = always_redraw(lambda: cross_marks(1.0, B.get_value()))
        bar_names = VGroup(T("front", 26, GREY).move_to([PX0 + 0.5, BARY + 0.68, 0]), T("back", 26, GREY).move_to([PX0 + PW - 0.45, BARY + 0.68, 0]))
        self.add(ax, thr, chipw, cv, lamp, lamp_lab, bar, cm, bar_names)
        self.play(FadeIn(toy), run_time=0.3)
        self.at("second source")
        lp2 = glow(LAMP2X, LAMPY, 0.14 + 0.03, 0.6)
        self.play(FadeIn(lp2, scale=0.5), FadeIn(lamp2_lab), B.animate.set_value(B_SECOND), run_time=1.3)
        tx0 = PX0 + [f for f, ti in crossings(1.0, B_SECOND) if ti == 1][-1] * PW
        hl = outline_rect((tx0 + PX0 + PW) / 2, BARY, PX0 + PW - tx0, BARH, WHITE, 5)
        self.at("part of the pattern")
        self.play(Create(hl), run_time=0.5)
        self.play(Indicate(cm, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def bracket_h(x0, x1, y, color=WHITE):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4), Line([x0, y, 0], [x0, y - 0.14, 0], color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y - 0.14, 0], color=color, stroke_width=4))


class S16(SS):
    def construct(self):
        cx, cy, w, h = 0.0, 0.85, 10.4, 3.4
        sig = ValueTracker(0.07)
        mp = always_redraw(lambda: fuzzy_img(cx, cy, w, h, WT[0], WT[1], sig.get_value(), op=0.55))
        outline = outline_rect(cx, cy, w, h, GREY, 3)
        tcx = cx - w / 2 + (WT[0] + WT[1]) / 2 * w
        self.add(mp, outline)
        thal = chip("thalamus", TEXT, 28).move_to([0, -3.3, 0])
        bx = [cx - w / 2 + f * w for f in (WT[0] / 2, (WT[0] + WT[1]) / 2, (WT[1] + 1) / 2)]
        axons = VGroup(*[Arrow([(i - 1) * 0.7, -2.95, 0], [x, cy - h / 2, 0], buff=0, color=TEXT, stroke_width=6,
                               tip_length=0.2, max_tip_length_to_length_ratio=0.2) for i, x in enumerate(bx)])
        self.play(FadeIn(thal), LaggedStart(*[GrowArrow(a) for a in axons], lag_ratio=0.25), run_time=1.0)
        halo = VGroup(*[Rectangle(width=1.3, height=h, stroke_width=0, fill_color=WHITE, fill_opacity=0.2).move_to(
            [cx - w / 2 + f * w, cy, 0]) for f in WT])
        self.at("sharpens the sketch")
        self.add(halo)
        self.play(sig.animate.set_value(0.004), Indicate(axons, color=TEXT, scale_factor=1.0), run_time=1.3)
        self.play(FadeOut(halo), run_time=0.5)
        # primary / higher-order split of the visual area
        vx0 = cx - w / 2 + WT[1] * w
        vmid = (vx0 + cx + w / 2) / 2
        veilr = Rectangle(width=cx + w / 2 - vmid, height=h, stroke_width=0, fill_color=BG, fill_opacity=0.4).move_to(
            [(vmid + cx + w / 2) / 2, cy, 0])
        divl = DashedLine([vmid, cy - h / 2, 0], [vmid, cy + h / 2, 0], dash_length=0.12, color=TEXT, stroke_width=4)
        topy = cy + h / 2 + 0.28
        brp = bracket_h(vx0 + 0.05, vmid - 0.05, topy, PINK)
        brh = bracket_h(vmid + 0.05, cx + w / 2 - 0.05, topy, PINK)
        lp = T("primary", 28, PINK, weight=BOLD).move_to([(vx0 + vmid) / 2 - 0.35, topy + 0.38, 0])
        lh = T("higher-order", 28, PINK).move_to([(vmid + cx + w / 2) / 2 + 0.3, topy + 0.38, 0])
        self.at("primary areas")
        self.play(Create(divl), FadeIn(veilr), Create(brp), FadeIn(lp), run_time=0.9)
        self.at("higher order")
        self.play(Create(brh), FadeIn(lh), run_time=0.7)
        # inner maps: dots start scattered, then line up
        loose = jig(3, 12, 0.34)
        d_loose = VGroup(*[Circle(radius=0.15, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.9).move_to(
            [tcx + (i - 1.5) * 0.72 + loose[3 * i + j][0], cy + (j - 1) * 0.78 + loose[3 * i + j][1], 0])
            for i in range(4) for j in range(3)])
        d_tight = VGroup(*[Circle(radius=0.15, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.9).move_to(
            [tcx + (i - 1.5) * 0.72, cy + (j - 1) * 0.78, 0]) for i in range(4) for j in range(3)])
        self.at("helps shape the maps")
        self.play(FadeIn(d_loose, lag_ratio=0.05), run_time=0.7)
        self.play(Transform(d_loose, d_tight), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17(SS):
    def construct(self):
        bw, bh = 5.0, 1.5
        lx, rx = -3.0, 3.6          # bar centres, left column (Emx2) and right column (another factor)
        yl, yg = 1.4, -0.85
        ttl = T("strongest evidence", 40, GOLD, font=TITLE_FONT).move_to([0, 3.5, 0])

        def barrow(cx, y, b):
            return areas(cx, y, bw, bh, *b, sw=3, op=0.5)

        def ghosts(cx, y):
            return VGroup(*[DashedLine([cx - bw / 2 + f * bw, y - bh / 2 - 0.1, 0], [cx - bw / 2 + f * bw, y + bh / 2 + 0.1, 0],
                                       dash_length=0.1, color=WHITE, stroke_width=3) for f in WT])

        def arrow_at(cx, y, d):
            a, e = (cx - 1.3, cx + 1.3) if d > 0 else (cx + 1.3, cx - 1.3)
            return Arrow([a, y - bh / 2 - 0.3, 0], [e, y - bh / 2 - 0.3, 0], buff=0, color=WHITE, stroke_width=9, tip_length=0.3,
                         max_tip_length_to_length_ratio=0.35)

        head1 = T("Emx2", 34, ORANGE, weight=BOLD).move_to([lx, 2.6, 0])
        base1, base2 = barrow(lx, yl, WT), barrow(lx, yg, WT)
        m1, m2 = barrow(lx, yl, (0.52, 0.86)), barrow(lx, yg, (0.28, 0.58))
        l1, l2 = T("loss", 32, TEXT).move_to([-6.1, yl, 0]), T("gain", 32, TEXT).move_to([-6.1, yg, 0])
        a1, a2 = arrow_at(lx, yl, +1), arrow_at(lx, yg, -1)
        g1, g2 = ghosts(lx, yl), ghosts(lx, yg)
        col = VGroup(head1, base1, base2, l1, l2, a1, a2, g1, g2)
        col.shift(RIGHT * 3.5)
        self.at("strongest evidence")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), FadeIn(head1), FadeIn(base1), FadeIn(base2), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.at("loss and gain")
        self.play(Transform(base1, m1.shift(RIGHT * 3.5)), FadeIn(g1), GrowArrow(a1), run_time=0.9)
        self.play(Transform(base2, m2.shift(RIGHT * 3.5)), FadeIn(g2), GrowArrow(a2), run_time=0.9)
        self.at("opposite directions")
        self.play(Indicate(VGroup(a1, a2), color=WHITE, scale_factor=1.15), run_time=0.9)
        # another factor: loss shown, the converse result missing
        head2 = T("another factor", 34, TEXT, weight=BOLD).move_to([rx, 2.6, 0])
        r1, r2 = T("loss", 32, TEXT).move_to([0.1, yl, 0]), T("gain", 32, GREY).move_to([0.1, yg, 0])
        rb1 = barrow(rx, yl, WT)
        rm1 = barrow(rx, yl, (0.46, 0.78))
        hole = DashedVMobject(Rectangle(width=bw, height=bh, stroke_color=GREY, stroke_width=3), num_dashes=44).move_to([rx, yg, 0])
        qm = T("?", 52, GREY, weight=BOLD).move_to([rx, yg, 0])
        self.at("a missing converse")
        self.play(col.animate.shift(LEFT * 3.5), run_time=0.4)
        self.play(FadeIn(head2), FadeIn(rb1), FadeIn(r1), FadeIn(r2), FadeIn(hole), FadeIn(qm), run_time=0.3)
        ra = arrow_at(rx, yl, +1)
        self.play(Transform(rb1, rm1), FadeIn(ghosts(rx, yl)), GrowArrow(ra), run_time=0.5)
        cap2 = T("does not rule a factor out", 34, TEXT).move_to([0, -3.2, 0])
        self.at("does not rule")
        self.play(FadeIn(cap2, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scope frame, scenes 18 to 21
class Scope:
    @staticmethod
    def big():
        d = {}
        d["frame"] = RoundedRectangle(corner_radius=0.2, width=11.8, height=4.7, stroke_color=GOLD, stroke_width=4,
                                      fill_opacity=0).move_to([0, 0.5, 0])
        d["label"] = T("what the rule covers", 26, GOLD).move_to([-3.6, 2.45, 0])
        d["bar"] = VGroup(areas(0, 0.1, 10.4, 2.9, *WT, sw=3, op=0.5), outline_rect(0, 0.1, 10.4, 2.9, GREY, 3))
        d["mouse"] = VGroup(mouse_head(0.42, (3.55, 2.35)), T("mouse", 26, GREY).move_to([4.85, 2.35, 0]))
        return d

    @staticmethod
    def compact():
        d = {}
        d["frame"] = RoundedRectangle(corner_radius=0.2, width=11.0, height=2.5, stroke_color=GOLD, stroke_width=4,
                                      fill_opacity=0).move_to([0, 2.5, 0])
        d["label"] = T("what the rule covers", 26, GOLD).move_to([-3.3, 3.3, 0])
        d["bar"] = VGroup(areas(0, 2.1, 9.0, 1.0, *WT, sw=3, op=0.5), outline_rect(0, 2.1, 9.0, 1.0, GREY, 3))
        d["mouse"] = VGroup(mouse_head(0.33, (3.1, 3.2)), T("mouse", 26, GREY).move_to([4.2, 3.25, 0]))
        return d


def scope_ticks(h0=1.7, h1=-1.5):
    return VGroup(*[Line([-5.2 + f * 10.4, h0, 0], [-5.2 + f * 10.4, h1, 0], color=GOLD, stroke_width=5) for f in WT])


def scope_axis():
    return VGroup(Arrow([-4.2, -2.45, 0], [4.2, -2.45, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25),
                  T("front", 26, GREY).move_to([-5.2, -2.45, 0]), T("back", 26, GREY).move_to([5.0, -2.45, 0]))


class S18(SS):
    def construct(self):
        d = Scope.big()
        self.play(FadeIn(d["bar"]), Create(d["frame"]), run_time=0.9)
        self.at("it covers")
        self.play(FadeIn(d["label"]), run_time=0.6)
        ticks = scope_ticks()
        self.at("primary area borders")
        self.play(Create(ticks), run_time=1.0)
        axis = scope_axis()
        self.at("front to back")
        self.play(FadeIn(axis), run_time=0.7)
        self.at("in the mouse")
        self.play(FadeIn(d["mouse"], scale=0.7), run_time=0.7)
        self.finish()


class S19(SS):
    def construct(self):
        d = Scope.big()
        ticks, axis = scope_ticks(), scope_axis()
        self.add(d["bar"], d["frame"], d["label"], d["mouse"], ticks, axis)
        c = Scope.compact()
        box0 = Rectangle(width=3.2, height=1.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([0, -0.7, 0])
        self.add(box0)
        box0.set_opacity(0)
        self.play(box0.animate.set_stroke(opacity=1).set_fill(opacity=0.25), Transform(d["frame"], c["frame"]), Transform(d["bar"], c["bar"]), Transform(d["label"], c["label"]),
                  Transform(d["mouse"], c["mouse"]), FadeOut(ticks), FadeOut(axis), run_time=0.9)
        box = box0
        lab = T("total cortical growth", 32, TEXT).move_to([0, -3.3, 0])
        up = Arrow([3.9, -1.5, 0], [3.9, 0.1, 0], buff=0, color=WHITE, stroke_width=8, tip_length=0.3)
        self.at("total cortical growth")
        self.play(FadeIn(lab), run_time=0.5)
        self.play(box.animate.scale(1.8), GrowArrow(up), run_time=1.2)
        cross = VGroup(Line([-2.88, -2.14, 0], [2.88, 0.74, 0], color=RED, stroke_width=12), Line([-2.88, 0.74, 0], [2.88, -2.14, 0], color=RED, stroke_width=12))
        nc = T("not covered", 34, RED, weight=BOLD).move_to([-5.0, -0.7, 0])
        self.at("some of these factors")
        self.play(Create(cross, lag_ratio=0), FadeIn(nc), run_time=0.7)
        self.at("also change")
        self.play(box.animate.scale(1.08), run_time=0.4)
        self.play(box.animate.scale(1 / 1.08), run_time=0.4)
        self.finish()


class S20(SS):
    def construct(self):
        big, c = Scope.big(), Scope.big()
        # Keep the mouse map at 35% of frame height above the within-area maps.
        c["frame"] = RoundedRectangle(corner_radius=0.15, width=11.8, height=3.25,
                                      stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([0, 2.0, 0])
        c["bar"] = VGroup(areas(0, 1.85, 10.4, 2.8, *WT, sw=3, op=0.5),
                          outline_rect(0, 1.85, 10.4, 2.8, GREY, 3))
        c["label"].move_to([-3.6, 3.43, 0])
        c["mouse"] = VGroup(mouse_head(0.20, (3.65, 3.43)),
                            T("mouse", 22, GREY).move_to([4.5, 3.43, 0]))
        self.add(big["bar"], big["frame"], big["label"], big["mouse"])
        px, pw, ph, py = 3.9, 4.3, 3.2, -1.65
        bl = RoundedRectangle(corner_radius=0.15, width=pw, height=ph, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                              fill_opacity=0.1).move_to([-px, py, 0])
        br = bl.copy().move_to([px, py, 0])
        lb = T("barrels", 30, TEXT).move_to([-px, py + 1.30, 0])
        lo = T("orientation patches", 30, TEXT)
        fit(lo, max_w=pw - 0.3).move_to([px, py + 1.30, 0])
        barr = dots(-px, py - 0.2, 4, 3, 0.85, 0.26)
        ori = VGroup()
        for i in range(4):
            for j in range(3):
                ang = np.pi * (0.5 + 0.5 * np.sin(0.9 * i + 1.1 * j) * np.cos(0.7 * j - 0.4 * i))
                m = Line([-0.34, 0, 0], [0.34, 0, 0], color=PINK, stroke_width=8).rotate(ang)
                ori.add(m.move_to([px + (i - 1.5) * 0.92, py - 0.2 + (j - 1) * 0.85, 0]))
        cells = VGroup(RoundedRectangle(corner_radius=0.16, width=1.9, height=1.25, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.16),
                       T("cortex's\nown cells", 24, TEAL, line_spacing=0.8)).move_to([0, py - 0.1, 0])
        cells[1].move_to(cells[0])
        t1 = Arrow([-0.97, py - 0.1, 0], [-1.65, py - 0.1, 0], buff=0, color=TEAL, stroke_width=7, tip_length=0.2, max_tip_length_to_length_ratio=0.6)
        t2 = Arrow([0.97, py - 0.1, 0], [1.65, py - 0.1, 0], buff=0, color=TEAL, stroke_width=7, tip_length=0.2, max_tip_length_to_length_ratio=0.6)
        self.at("threshold model")
        self.wait(0.3)
        self.at("maps inside")
        self.play(*[Transform(big[k], c[k]) for k in ("frame", "bar", "label", "mouse")],
                  FadeIn(bl), FadeIn(br), FadeIn(lb), FadeIn(lo), FadeIn(barr, lag_ratio=0.05), FadeIn(ori, lag_ratio=0.05),
                  FadeIn(cells, scale=0.8), GrowArrow(t1), GrowArrow(t2), run_time=1.3)
        thal = chip("thalamus", TEXT, 28).move_to([0, -3.55, 0])
        a1 = Arrow([-1.15, -3.45, 0], [-px - 0.3, py - ph / 2 - 0.05, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.24, max_tip_length_to_length_ratio=0.2)
        a2 = Arrow([1.15, -3.45, 0], [px + 0.3, py - ph / 2 - 0.05, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.24, max_tip_length_to_length_ratio=0.2)
        act = T("activity", 28, TEXT).move_to([0, -2.8, 0])
        self.at("input and activity")
        self.play(FadeIn(thal), GrowArrow(a1), GrowArrow(a2), FadeIn(act), run_time=1.0)
        self.at("own cells")
        self.play(Indicate(cells, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.finish()


def primate_brain(cx, cy, w, h):
    """a lateral brain silhouette (front on the left) with a few sulci. no molecules."""
    pts = [(-0.97, 0.02), (-0.88, 0.32), (-0.6, 0.58), (-0.2, 0.7), (0.25, 0.72), (0.65, 0.58), (0.9, 0.3), (0.97, -0.05),
           (0.85, -0.3), (0.62, -0.4), (0.4, -0.5), (0.1, -0.5), (-0.1, -0.62), (-0.35, -0.5), (-0.55, -0.3), (-0.8, -0.22)]
    P_ = [[cx + x * w / 2, cy + y * h / 2, 0] for x, y in pts]
    body = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.18)
    body.set_points_smoothly(P_ + [P_[0]])
    cb = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    cbp = [(0.45, -0.38), (0.68, -0.42), (0.86, -0.55), (0.76, -0.72), (0.5, -0.74), (0.34, -0.55)]
    cbq = [[cx + x * w / 2, cy + y * h / 2, 0] for x, y in cbp]
    cb.set_points_smoothly(cbq + [cbq[0]])
    stem = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    sp = [(0.02, -0.45), (0.22, -0.5), (0.2, -0.85), (0.02, -0.88), (-0.08, -0.62)]
    sq = [[cx + x * w / 2, cy + y * h / 2, 0] for x, y in sp]
    stem.set_points_smoothly(sq + [sq[0]])
    sul = VGroup()
    curves = [
        [(-0.3, -0.3), (-0.05, -0.18), (0.2, -0.05), (0.5, 0.02)],                     # lateral fissure
        [(0.0, 0.7), (-0.05, 0.45), (0.08, 0.25), (0.0, 0.0)],                         # central sulcus
        [(-0.65, 0.35), (-0.45, 0.4), (-0.3, 0.3), (-0.18, 0.4)],
        [(-0.55, 0.1), (-0.4, 0.18), (-0.25, 0.1), (-0.12, 0.2)],
        [(0.3, 0.55), (0.4, 0.35), (0.55, 0.3), (0.7, 0.4)],
        [(0.3, 0.2), (0.45, 0.1), (0.65, 0.18), (0.8, 0.05)],
        [(0.45, -0.2), (0.6, -0.15), (0.75, -0.22)],
        [(-0.45, -0.1), (-0.3, -0.12), (-0.2, -0.22)],
    ]
    for cv in curves:
        m = VMobject(stroke_color=GREY, stroke_width=3.5, stroke_opacity=0.8)
        m.set_points_smoothly([[cx + x * w / 2, cy + y * h / 2, 0] for x, y in cv])
        sul.add(m)
    return VGroup(cb, stem, body, sul)


class S21(SS):
    def construct(self):
        c = Scope.compact()
        self.add(c["bar"], c["frame"], c["label"], c["mouse"])
        cy, cw, ch = -1.45, 5.6, 4.0
        cm = RoundedRectangle(corner_radius=0.18, width=cw, height=ch, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.06).move_to([-3.4, cy, 0])
        cp = RoundedRectangle(corner_radius=0.18, width=cw, height=ch, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([3.4, cy, 0])
        mouse = VGroup(mouse_head(1.35, (-3.4, cy + 0.15)), T("mouse", 32, GOLD, weight=BOLD).move_to([-3.4, cy - 1.55, 0]))
        brain = primate_brain(3.4, cy + 0.2, 4.6, 2.9)
        lab = T("primate, human", 32, TEXT).move_to([3.4, cy - 1.55, 0])
        self.add(cm, cp, mouse, brain, lab)
        self.at("drawn from mice")
        self.play(cm.animate.set_stroke(GOLD, 9), Indicate(mouse[1], color=GOLD, scale_factor=1.2), run_time=0.8)
        self.play(cm.animate.set_stroke(GOLD, 5), run_time=0.4)
        nc = T("not covered", 30, RED, weight=BOLD).move_to([3.4, cy + 1.62, 0])
        self.at("primates or humans")
        self.play(cp.animate.set_stroke(RED, 6), FadeIn(nc, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ramp_panel(cx, cy, w, h):
    def cf(f):
        a = 0.06 + 0.8 * f
        return np.array([color_to_rgb(ORANGE)]) * a[:, None] + np.array([color_to_rgb(BG)]) * (1 - a)[:, None]
    g = Group(grad_img(cx, cy, w, h, cf))
    return g, outline_rect(cx, cy, w, h, GREY, 3)


def sharp_block(cx, cy, w, h):
    g = VGroup()
    for i, col in enumerate((PURPLE, GREEN)):
        g.add(Rectangle(width=w / 2, height=h, stroke_color=col, stroke_width=3, fill_color=col,
                        fill_opacity=0.45).move_to([cx - w / 4 + i * w / 2, cy, 0]))
    return g


LX, RX, BWID = -3.95, 3.95, 5.4
PCY, PHH = 0.0, 4.0


class Pieces:
    def __init__(self):
        cy, h = PCY, PHH
        self.q = T("?", 120, TEXT, weight=BOLD).move_to([0, cy, 0])
        self.ramp, self.rout = ramp_panel(LX, cy, BWID, h)
        self.lr = T("smooth gradient", 32, TEXT).move_to([LX, cy + h / 2 + 0.45, 0])
        self.blk = sharp_block(RX, cy, BWID, h)
        self.bout = outline_rect(RX, cy, BWID, h, GREY, 3)
        self.lb = T("sharp border", 32, TEXT).move_to([RX, cy + h / 2 + 0.45, 0])
        self.prog = VGroup(*[Circle(radius=0.2, stroke_color=BG, stroke_width=2, fill_color=LIGHT, fill_opacity=0.95).move_to(
            [LX - BWID / 2 + 0.5 + i * (BWID - 1.0) / 7, cy + (0.45 if i % 2 else -0.45), 0]) for i in range(8)])
        self.pl = T("progenitors", 32, LIGHT).move_to([LX, -3.3, 0])
        self.neu = VGroup(*[Circle(radius=0.2, stroke_color=BG, stroke_width=2, fill_color=TEAL, fill_opacity=0.95).move_to(
            [RX - BWID / 2 + 0.5 + i * (BWID - 1.0) / 7, cy + (0.45 if i % 2 else -0.45), 0]) for i in range(8)])
        self.ax = VGroup(*[Arrow([RX - 1.95 + i * 1.3, -2.95, 0], [RX - 1.95 + i * 1.3, cy - h / 2 - 0.02, 0], buff=0, color=TEXT,
                                 stroke_width=6, tip_length=0.2, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        self.nl = T("neurons under input", 32, TEAL).move_to([RX, -3.4, 0])

    def base(self):
        return [*self.ramp, self.rout, self.q, self.lr, self.blk, self.bout, self.lb]


class S22(SS):
    def construct(self):
        p = Pieces()
        self.add(*p.base())
        q = p.q
        q.save_state()
        q.scale(0.2).set_opacity(0.0)
        self.at("one question stays open")
        self.play(Restore(q), run_time=0.9)
        self.at("a gradient is smooth")
        self.play(Indicate(p.lr, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("mature borders are sharp")
        self.play(Indicate(p.lb, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


class S23(SS):
    def construct(self):
        p = Pieces()
        self.add(*p.base())
        self.at("become")
        self.play(Indicate(p.q, color=TEXT, scale_factor=1.25), run_time=1.0)
        self.at("in progenitors")
        self.play(FadeIn(p.prog, lag_ratio=0.1), FadeIn(p.pl), run_time=1.1)
        self.at("neurons under input")
        self.play(FadeIn(p.neu, lag_ratio=0.1), FadeIn(p.nl), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in p.ax], lag_ratio=0.15), run_time=0.8)
        self.finish()


class S24(SS):
    def construct(self):
        p = Pieces()
        extra = VGroup(p.prog, p.neu, p.pl, p.nl, p.ax)
        self.add(*p.base(), extra)
        l1 = T("Position draws the sketch; input finishes it.", 38, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeOut(extra), run_time=0.8)
        self.at("position draws the sketch")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.9)
        ho = outline_rect(LX, PCY, BWID, PHH, ORANGE, 7)
        hr = outline_rect(RX, PCY, BWID, PHH, TEXT, 7)
        self.at("how the sketch becomes")
        self.play(Create(ho), run_time=0.7)
        self.play(Create(hr), run_time=0.7)
        self.at("not yet fully understood")
        self.play(Indicate(p.q, color=TEXT, scale_factor=1.3), FadeOut(ho), FadeOut(hr), run_time=1.2)
        self.finish()


class S25End(EndCard):
    LINE = "Position draws the sketch; input finishes it.\nHow borders sharpen is open."

    def construct(self):
        l1 = T("Position draws the sketch; input finishes it.", 40, TEXT, font=TITLE_FONT)
        l2 = T("How borders sharpen is open.", 40, TEXT, font=TITLE_FONT)
        fit(l1, max_w=11.8)
        sub = T("biochemistrypedia.com", 22, TEAL)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        sub.next_to(g, DOWN, buff=0.5)
        self.play(FadeIn(l1, shift=UP * 0.15), FadeIn(l2, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
