"""Chapter 5: The Receptor That Can Kill (Neurotrophins, Trk Receptors and p75)

COLOR MAP (shared with every chapter of this lesson; taken from scenes.old.py)
  BLUE   = the neurotrophin (NGF) itself, mature or precursor body; column headings naming a factor
  ORANGE = the pro-domain (the extra front stretch of proNGF)
  PINK   = Trk receptors (TrkA) and their kinase feet
  VIOLET = p75
  YELLOW = sortilin (only sortilin)
  ENZ    = the cutting enzymes: pale blue-grey scissors, plasmin, matrix metalloproteinase, cut-site bands
  GREEN  = survival
  RED    = death (apoptosis)
  GREY   = membrane, cells, myelin, outlines, scope notes
  LG     = light grey for small captions (readable on the dark ground)
  TEXT   = the question marks, locks, the final statement, highlights and names
  (TEAL partner hexagons are not used in this chapter.)

Every shape is a labelled cartoon: no molecular structures.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
ORANGE = "#F29E4C"
VIOLET = "#A98BE0"
ENZ = "#BFC9DD"
LG = "#C5CBD6"
MY = -0.6  # default membrane height
YM = -1.2  # membrane height in the ligand scenes
ECD = 2.6  # standard p75 outside height
ICD = 1.1  # standard p75 inside height


# ---------------------------------------------------------------- helpers
class SS(SpokenScene):
    def rel(self, phrase, dt, nth=0):
        """wait until `dt` seconds after the narrator starts `phrase` (for names a transcriber may misspell)."""
        target = self.t_of(phrase, nth) + dt - 0.2
        rest = target - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


def lab(text, color, x, y, size=26, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def leader(a, b, color=TEXT, w=3):
    return Line(a, b, color=color, stroke_width=w)


def membrane(y=MY):
    return Rectangle(width=14.3, height=0.36, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, y, 0])


def inside(y=MY):
    top = y - 0.18
    h = top + 4.1
    return Rectangle(width=14.3, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to([0, top - h / 2, 0])


def tails_of(cx, cy, s):
    return VGroup(*[RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=0.8 * s, stroke_color=ORANGE,
                                     stroke_width=3, fill_color=ORANGE, fill_opacity=0.7)
                    .move_to([cx + sx * 0.5 * s, cy + 0.695 * s, 0]) for sx in (-1, 1)])


def dimer(cx, cy, s=1.0, tails=False, color=BLUE):
    bodies = [Ellipse(width=0.95 * s, height=0.75 * s, stroke_color=color, stroke_width=3,
                      fill_color=color, fill_opacity=0.5).move_to([cx + sx * 0.5 * s, cy, 0]) for sx in (-1, 1)]
    g = VGroup(*bodies)
    g.bodies = VGroup(*bodies)
    g.tails = tails_of(cx, cy, s)
    if tails:
        g.add(*g.tails)
    return g


def glow(mob, color=ORANGE, w=14, op=0.35):
    """a soft halo copy behind a shape."""
    return mob.copy().set_stroke(color, w, opacity=op).set_fill(opacity=0)


def cell(x, y, r=0.6, color=GREY, op=0.14, sw=4):
    body = Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    nuc = Circle(radius=r * 0.36, stroke_width=0, fill_color=color, fill_opacity=0.45)
    g = VGroup(body, nuc).move_to([x, y, 0])
    g.body, g.nuc = body, nuc
    return g


def trk(x, y=MY, ecd=2.0, icd=1.0, w=0.7):
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=ecd + icd, stroke_color=PINK, stroke_width=3,
                           fill_color=PINK, fill_opacity=0.55).move_to([x, y + (ecd - icd) / 2, 0])
    foot = Circle(radius=0.45, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.4).move_to([x, y - icd - 0.3, 0])
    g = VGroup(bar, foot)
    g.bar, g.foot = bar, foot
    return g


def stalk(x, y=MY, ecd=ECD, icd=ICD, color=VIOLET, op=0.55, w=0.8):
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=ecd + icd, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=op).move_to([x, y + (ecd - icd) / 2, 0])
    g = VGroup(bar)
    g.bar = bar
    return g


# ---- p75 + sortilin + ligand geometry: p75 under the left lobe, sortilin touching p75 under the right lobe,
#      sortilin's arm climbing outside the right lobe to grip the right pro-domain.
def sort_parts(px, ym, s, ecd=ECD, icd=ICD, arm=True):
    sx = px + 0.8
    bar = RoundedRectangle(corner_radius=0.2, width=0.8, height=ecd + icd, stroke_color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.5).move_to([sx, ym + (ecd - icd) / 2, 0])
    g = VGroup(bar)
    g.bar = bar
    g.arm = VGroup()
    g.cup = VGroup()
    if arm:
        yt = ym + ecd
        r = 0.12 * s + 0.3
        cx = px + s
        path = Line([sx + 0.3, yt - 0.02, 0], [cx, yt + 0.3 - r + 0.02, 0], color=YELLOW, stroke_width=9)
        cup = Arc(radius=r, start_angle=PI, angle=PI, stroke_color=YELLOW, stroke_width=9, arc_center=[cx, yt + 0.3, 0])
        g.arm, g.cup = path, cup
        g.add(path, cup)
    return g


def p75_cup(px, ym, s, ecd=ECD):
    yt = ym + ecd
    r = 0.12 * s + 0.3
    return Arc(radius=r, start_angle=PI, angle=PI, stroke_color=VIOLET, stroke_width=9, arc_center=[px, yt + 0.3, 0])


def ligand(px, ym, s, ecd=ECD, tails=False):
    cy = ym + ecd + 0.375 * s
    return dimer(px + 0.5 * s, cy, s, tails=tails), cy


ENZ_COL = ENZ


def scissors(x, y, s=1.0):
    a = Line([-0.55 * s, -0.32 * s, 0], [0.85 * s, 0.2 * s, 0], color=ENZ, stroke_width=6)
    b = Line([-0.55 * s, 0.32 * s, 0], [0.85 * s, -0.2 * s, 0], color=ENZ, stroke_width=6)
    h = VGroup(*[Circle(radius=0.17 * s, stroke_color=ENZ, stroke_width=5).move_to([-0.62 * s, sy * 0.33 * s, 0]) for sy in (-1, 1)])
    g = VGroup(a, b, h).move_to([x, y, 0])
    g.a, g.b = a, b
    return g


def snip(scene, sc, t=0.15):
    """Close and reopen the scissors blades in place."""
    sa, ea = sc.a.get_start(), sc.a.get_end()
    sb, eb = sc.b.get_start(), sc.b.get_end()
    mid = (ea + eb) / 2
    scene.play(sc.a.animate.put_start_and_end_on(sa, mid + DOWN * 0.01), sc.b.animate.put_start_and_end_on(sb, mid + UP * 0.01), run_time=t)
    scene.play(sc.a.animate.put_start_and_end_on(sa, ea), sc.b.animate.put_start_and_end_on(sb, eb), run_time=t)


def cut_tail(scene, sc, tail, s_sc, approach=0.25, y_off=None, drift=0.8, run=0.3, snip_t=0.12):
    """move the scissors to the base of `tail`, snip, and let the tail drift off."""
    tx, ty = tail.get_center()[0], tail.get_center()[1]
    yb = ty - 0.18 * tail.height if y_off is None else y_off
    scene.play(sc.animate.move_to([tx - 0.3 * s_sc, yb, 0]), run_time=approach)
    snip(scene, sc, snip_t)
    scene.play(tail.animate.shift(UP * drift).set_opacity(0), run_time=run)


def lock(x, y, s=1.0):
    body = RoundedRectangle(corner_radius=0.04 * s, width=0.3 * s, height=0.24 * s, stroke_color=TEXT, stroke_width=2,
                            fill_color=TEXT, fill_opacity=0.95)
    sh = Arc(radius=0.085 * s, start_angle=0, angle=PI, stroke_color=TEXT, stroke_width=4).move_to([0, 0.12 * s + 0.04 * s, 0])
    return VGroup(sh, body).move_to([x, y, 0])


def cut_marks(cx, cy, s):
    """pale bands across the base of each pro-domain: the sites a protease cuts."""
    return VGroup(*[Rectangle(width=0.4 * s, height=0.11 * s, stroke_width=0, fill_color=ENZ, fill_opacity=0.95)
                    .move_to([cx + sx * 0.5 * s, cy + 0.6 * s, 0]) for sx in (-1, 1)])


def cross(center, size=0.28, color=RED, w=7):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - size, cy - size, 0], [cx + size, cy + size, 0], color=color, stroke_width=w),
                  Line([cx - size, cy + size, 0], [cx + size, cy - size, 0], color=color, stroke_width=w))


def ghost_trk(x, y=MY, ecd=2.0, icd=1.0, w=0.7):
    """the absent TrkA: a dashed outline."""
    bar = RoundedRectangle(corner_radius=0.2, width=w, height=ecd + icd).move_to([x, y + (ecd - icd) / 2, 0])
    foot = Circle(radius=0.45).move_to([x, y - icd - 0.3, 0])
    g = VGroup(DashedVMobject(bar.set_stroke(GREY, 3), num_dashes=26), DashedVMobject(foot.set_stroke(GREY, 3), num_dashes=14))
    return g


# ---- oligodendrocyte dish: three cells, each with two arms ending in a myelin sheath; nothing overlaps
_OL = [((-1.3, 0.8), [(-0.8, 0.5), (0.1, -1.0)]),
       ((1.3, 0.8), [(0.8, 0.5), (-0.1, -1.0)]),
       ((0.0, -1.6), [(-1.15, -0.3), (1.15, -0.3)])]


def myelin_cell(x, y, spots, k):
    arms, sheaths = [], []
    for dx, dy in spots:
        p0, p1 = np.array([x, y, 0.0]), np.array([x + dx * k, y + dy * k, 0.0])
        arms.append(Line(p0, p1, color=GREY, stroke_width=3))
        arms.append(Line(p1 + np.array([-0.5 * k, 0, 0]), p1 + np.array([0.5 * k, 0, 0]), color=GREY, stroke_width=2))
        sheaths.append(RoundedRectangle(corner_radius=0.08 * k, width=0.7 * k, height=0.3 * k, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.6).move_to(p1))
    body = Circle(radius=0.38 * k, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([x, y, 0])
    g = VGroup(body)
    g.body, g.arms, g.sheaths = body, VGroup(*arms), VGroup(*sheaths)
    return g


def oligo_dish(x, y, r):
    k = r / 3.0
    d = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to([x, y, 0])
    cells = [myelin_cell(x + cx * k, y + cy * k, spots, k) for (cx, cy), spots in _OL]
    g = VGroup(d)
    g.dish, g.cells = d, cells
    g.bodies = VGroup(*[c.body for c in cells])
    g.arms = VGroup(*[c.arms for c in cells])
    g.sheaths = VGroup(*[c.sheaths for c in cells])
    return g


def retina(x, y, w=10.0, h=4.0, cols=8, rows=3):
    fr = RoundedRectangle(corner_radius=0.6, width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])
    xs = np.linspace(x - w / 2 + 0.8, x + w / 2 - 0.8, cols)
    ys = np.linspace(y + h / 2 - 0.7, y - h / 2 + 0.7, rows)
    dots = VGroup(*[Circle(radius=0.23, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([a, b, 0])
                    for b in ys for a in xs])
    g = VGroup(fr, dots)
    g.frame, g.dots = fr, dots
    return g


# ---------------------------------------------------------------- the results table (scenes 15 to 22)
CX = [-1.8, 1.6, 5.0]
BW = 3.2
LAYOUTS = {1: (3.7, [-0.3]), 2: (2.1, [0.8, -1.5])}
ROW_TXT = ["p75 + sortilin,\nlittle TrkA", "sympathetic\nneurons"]


def locked_dimer(x, y, s):
    d = dimer(x, y, s, tails=True)
    ls = VGroup(*[lock(x + sx * 0.5 * s, y + 0.62 * s, 1.0 + 1.0 * s) for sx in (-1, 1)])
    return VGroup(d, ls)


def head(c):
    y_icon, y_txt = 3.2, 2.35
    x = CX[c]
    if c == 0:
        icon = dimer(x, y_icon, 0.55)
        txt = "mature\nNGF"
    elif c == 1:
        icon = locked_dimer(x, y_icon - 0.1, 0.55)
        txt = "uncleavable\nproNGF"
    else:
        d = locked_dimer(x - 0.5, y_icon - 0.1, 0.55)
        blk = RoundedRectangle(corner_radius=0.06, width=0.22, height=0.6, stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.55).move_to([x + 0.95, y_icon, 0])
        icon = VGroup(d, blk, cross([x + 0.95, y_icon], 0.19, TEXT, 4))
        txt = "uncleavable proNGF,\np75 blocked"
    t = T(txt, 22 if c == 2 else 24, BLUE, line_spacing=0.7).move_to([x, y_txt, 0])
    return VGroup(icon, t)


def row_label(r, ry, h):
    big = h > 3
    sc = 3.0 if big else 2.2
    if big:
        cx, iy = -5.1, ry + 0.1
    else:
        cx, iy = -6.0, ry + 0.05
    body = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15)
    if r == 0:
        bars = [(-0.2, VIOLET, 0.42, 0.55), (0.0, YELLOW, 0.34, 0.55), (0.22, PINK, 0.16, 0.5)]
    else:
        bars = [(-0.1, VIOLET, 0.42, 0.55), (0.1, PINK, 0.42, 0.55)]
    rs = [RoundedRectangle(corner_radius=0.04, width=0.1, height=hh, stroke_color=col, stroke_width=2, fill_color=col,
                           fill_opacity=op).move_to([dx, 0.28 + hh / 2 - 0.1, 0]) for dx, col, hh, op in bars]
    ic = VGroup(body, *rs).scale(sc).move_to([cx, iy, 0])
    if big:
        txt = T(ROW_TXT[r], 22, LG, line_spacing=0.7).move_to([cx, ry - 1.9, 0])
    else:
        txt = T(ROW_TXT[r], 20, LG, line_spacing=0.7).move_to([-4.5, iy - 0.2, 0])
    g = VGroup(ic, txt)
    if r == 0:
        lt = T("little", 22, PINK)
        lt.next_to(ic[3], UP, buff=0.12)
        g.add(lt)
    return g


def cells6(cx, cy, k, kinds):
    out = []
    for i, kd in enumerate(kinds):
        col, row = i % 3, i // 3
        x = cx + (col - 1) * 0.62 * k
        y = cy - (row - 0.5) * 0.55 * k
        base = {"g": GREEN, "r": RED, "n": GREY}[kd]
        rad = 0.2 * k * (0.6 if kd == "r" else 1.0)
        out.append(Circle(radius=rad, stroke_color=base, stroke_width=4, fill_color=base, fill_opacity=0.3).move_to([x, y, 0]))
    return VGroup(*out)


def res_geom(h):
    return h / 2.35


def res_cells(cx, y, h, kind):
    k = res_geom(h)
    kinds = {"n": "nnnnnn", "ok": "gggggg", "die": "rrrrgg"}[kind]
    return cells6(cx, y + 0.12 * h, k, kinds)


def res_text(cx, y, h, kind, dy=0.0):
    sz = 26 if h > 3 else 24
    ty = y - 0.28 * h + dy
    if kind == "ok":
        return T("no added death", sz, GREEN).move_to([cx, ty, 0])
    if kind == "die":
        return T("more cells die", sz, RED).move_to([cx, ty, 0])
    if kind == "surv":
        return T("survive", sz, GREEN).move_to([cx, ty, 0])
    raise ValueError(kind)


def res_q(cx, y):
    return T("?", 64, TEXT).move_to([cx, y, 0])


class Tab:
    """The results table. states[r][c] in {None, 'box', 'q', 'ok', 'die', 'surv'}."""

    def __init__(self, layout, states):
        self.h, self.ys = LAYOUTS[layout][0], LAYOUTS[layout][1]
        self.layout = layout
        self.heads = [head(c) for c in range(3)]
        self.rows, self.boxes, self.cont = [], {}, {}
        for r, row in enumerate(states):
            self.rows.append(row_label(r, self.ys[r], self.h))
            for c, st in enumerate(row):
                if st is None:
                    continue
                y = self.ys[r]
                self.boxes[(r, c)] = RoundedRectangle(corner_radius=0.15, width=BW, height=self.h, stroke_color=GREY,
                                                     stroke_width=3).move_to([CX[c], y, 0])
                self.cont[(r, c)] = self.content(st, CX[c], y)

    def content(self, st, cx, y):
        if st == "box":
            return VGroup()
        if st == "q":
            return VGroup(res_q(cx, y))
        if st == "surv":
            return VGroup(res_cells(cx, y, self.h, "ok"), res_text(cx, y, self.h, "surv"))
        return VGroup(res_cells(cx, y, self.h, st), res_text(cx, y, self.h, st))

    def row_pieces(self, r):
        out = [self.rows[r]]
        for c in range(3):
            if (r, c) in self.boxes:
                out += [self.boxes[(r, c)], self.cont[(r, c)]]
        return out

    def pieces(self, rows=None):
        rows = range(len(self.rows)) if rows is None else rows
        out = list(self.heads)
        for r in rows:
            out += self.row_pieces(r)
        return out

    def group(self, rows=None):
        return VGroup(*self.pieces(rows))


def q_states():
    return [["q", "q", "q"]]


def reveal_ok(scene, tab, r, c, rt=0.6):
    """swap a question mark for 'no added death' (all cells green)."""
    x, y, h = CX[c], tab.ys[r], tab.h
    new = VGroup(res_cells(x, y, h, "ok"), res_text(x, y, h, "ok"))
    scene.play(FadeOut(tab.cont[(r, c)]), FadeIn(new), run_time=rt)
    tab.cont[(r, c)] = new
    return new


def reveal_die(scene, tab, r, c, rt1=0.4, rt2=0.9):
    x, y, h = CX[c], tab.ys[r], tab.h
    neutral = res_cells(x, y, h, "n")
    scene.play(FadeOut(tab.cont[(r, c)]), FadeIn(neutral), run_time=rt1)
    dead = res_cells(x, y, h, "die")
    txt = res_text(x, y, h, "die")
    scene.play(Transform(neutral, dead), FadeIn(txt), run_time=rt2)
    tab.cont[(r, c)] = VGroup(neutral, txt)


def final_row1():
    return ["ok", "die", "ok"]


def bracket(x0, x1, y):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=LG, stroke_width=4),
                  Line([x0, y, 0], [x0, y + 0.25, 0], color=LG, stroke_width=4),
                  Line([x1, y, 0], [x1, y + 0.25, 0], color=LG, stroke_width=4))


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "The Receptor That Can Kill"


class S01(SS):
    def construct(self):
        ym = -1.0
        mem, cyt = membrane(ym), inside(ym)
        p = stalk(0, ym, ecd=3.2, icd=1.3, w=0.9)
        pl = lab("p75", VIOLET, -1.7, 1.2, 46)
        self.play(FadeIn(cyt), FadeIn(mem), FadeIn(p), FadeIn(pl), run_time=0.5)
        self.at("neurotrophin")
        s = 1.8
        top = ym + 3.2
        d = dimer(0.5 * s, top + 0.375 * s, s)
        d.shift(RIGHT * 4.4)
        nl = lab("neurotrophin", BLUE, 2.9, 1.2, 38)
        self.play(FadeIn(d), FadeIn(nl), run_time=0.5)
        self.at("binds")
        self.play(d.animate.shift(LEFT * 4.4), run_time=0.9)
        self.at("what does")
        q = lab("?", TEXT, 0.0, -3.2, 100)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("on its own")
        self.play(FadeOut(d, shift=UP * 0.6), FadeOut(nl, shift=UP * 0.6), Indicate(p.bar, color=VIOLET, scale_factor=1.06), run_time=0.9)
        self.finish()


class S02(SS):
    def construct(self):
        date = lab("mid-1990s", TEXT, 0, 2.6, 84)
        tl = Line([-5.5, 1.2, 0], [5.5, 1.2, 0], color=LG, stroke_width=4)
        ticks = VGroup(*[Line([x, 1.05, 0], [x, 1.35, 0], color=LG, stroke_width=4) for x in (-5.0, 0, 5.0)])
        tkl = VGroup(*[lab(t, LG, x, 0.7, 28) for t, x in (("1990", -5.0), ("1995", 0), ("2000", 5.0))])
        dot = Circle(radius=0.18, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([0, 1.2, 0])
        self.play(FadeIn(date, shift=UP * 0.2), Create(tl), FadeIn(ticks), FadeIn(tkl), FadeIn(dot, scale=0.3), run_time=0.7)
        self.at("two groups")
        g1 = chip("Barde's group", TEXT, 38).move_to([-3.4, -0.5, 0])
        g2 = chip("Chao's group", TEXT, 38).move_to([3.4, -0.5, 0])
        self.play(FadeIn(g1, shift=UP * 0.2), FadeIn(g2, shift=UP * 0.2), run_time=0.6)
        self.at("can kill")
        k = chip("p75 can kill", RED, 46).move_to([0, -3.0, 0])
        a1 = arr([-3.0, -1.2, 0], [-1.0, -2.3, 0], RED, 6)
        a2 = arr([3.0, -1.2, 0], [1.0, -2.3, 0], RED, 6)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(k), run_time=0.7)
        self.at("group showed")
        ret = retina(0, -0.55, 12.2, 4.4, cols=8, rows=3)
        bg = chip("Barde's group", TEXT, 30).move_to([-4.9, 3.3, 0])
        self.play(FadeOut(g2), FadeOut(a1), FadeOut(a2), FadeOut(k), FadeOut(g1), FadeOut(tl), FadeOut(ticks), FadeOut(tkl), FadeOut(dot), FadeIn(bg),
                  date.animate.scale(0.4).move_to([5.2, 3.3, 0]), FadeIn(ret), run_time=0.7)
        ds = VGroup(*[dimer(x, 2.55, 0.5) for x in (-3.4, 0, 3.4)])
        ars = VGroup(*[arr([x, 2.1, 0], [x, 1.7, 0], BLUE, 5) for x in (-3.4, 0, 3.4)])
        nl = lab("NGF", BLUE, -5.3, 2.4, 32)
        self.play(FadeIn(ds, lag_ratio=0.2), FadeIn(ars, lag_ratio=0.2), FadeIn(nl), run_time=0.5)
        self.at("developing")
        dying = [ret.dots[i] for i in (1, 4, 6, 9, 11, 14, 17, 20, 22)]
        self.play(*[d.animate.set_color(RED).set_fill(RED, 0.7).scale(1.15) for d in dying], run_time=0.5)
        self.at("chick")
        claim = lab("NGF kills through p75", TEXT, 0, 3.4, 36)
        bar = Line([-3.2, 3.05, 0], [3.2, 3.05, 0], color=RED, stroke_width=5)
        self.play(*[FadeOut(d, scale=0.3) for d in dying], FadeIn(claim), Create(bar), run_time=0.5)
        self.at("retina")
        rl = lab("developing chick retina", LG, 0, -3.3, 30)
        self.play(FadeIn(rl), run_time=0.4)
        self.finish()


class S03(SS):
    def construct(self):
        cy = -0.2
        r = 2.95
        chao = chip("Chao's group", TEXT, 30).move_to([-4.8, 3.3, 0])
        dish = oligo_dish(0, cy, r)
        self.play(FadeIn(chao), FadeIn(dish.dish), FadeIn(dish.bodies), run_time=0.6)
        self.at("NGF")
        ds = VGroup(*[dimer(x, 3.25, 0.5) for x in (-1.6, 0, 1.6)])
        ars = VGroup(*[arr([x, 2.95, 0], [x, 2.62, 0], BLUE, 5) for x in (-1.6, 0, 1.6)])
        nl = lab("NGF", BLUE, 3.3, 3.25, 36)
        self.play(FadeIn(ds, lag_ratio=0.2), FadeIn(ars, lag_ratio=0.2), FadeIn(nl), run_time=0.6)
        self.at("kills")
        self.play(*[b.animate.set_color(RED).set_fill(RED, 0.5) for b in dish.bodies], run_time=0.6)
        self.at("cultured")
        cl = lab("cultured rat", LG, 0, -3.55, 30)
        self.play(FadeIn(cl), run_time=0.4)
        self.at("oligodendrocytes")
        cl2 = lab("cultured rat oligodendrocytes", LG, 0, -3.55, 30)
        self.play(FadeIn(dish.arms), FadeIn(dish.sheaths), Transform(cl, cl2), run_time=0.9)
        self.finish()


def oligo_surface():
    ym = -0.9
    mem, cyt = membrane(ym), inside(ym)
    p = stalk(-2.2, ym)
    pl = lab("p75", VIOLET, -3.7, 0.7, 40)
    cap = lab("oligodendrocyte surface", LG, 0, -3.5, 28)
    g = ghost_trk(2.4, ym, ecd=ECD, icd=ICD, w=0.8)
    gl = lab("TrkA absent", LG, 2.4, 2.2, 32)
    cr = cross([2.4, 0.5], 0.4, GREY, 8)
    return cyt, mem, p, pl, cap, g, gl, cr, ym


class S04(SS):
    def construct(self):
        od = oligo_dish(-1.8, -0.2, 2.95)
        cl = lab("oligodendrocytes", LG, -1.8, -3.55, 30)
        self.add(od, od.bodies, od.arms, od.sheaths, cl)
        self.at("myelin")
        ml = lab("myelin", TEXT, 3.6, 1.9, 38)
        tgt = od.cells[1].sheaths[0].get_center() + RIGHT * 0.45
        ln = leader([3.0, 1.75, 0], tgt)
        self.play(FadeIn(ml), Create(ln), *[Indicate(s, color=TEXT) for s in od.sheaths], run_time=0.9)
        self.at("brain")
        b = chip("brain", LG, 34).move_to([4.8, 0.2, 0])
        self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.4)
        self.at("spinal")
        sp = chip("spinal cord", LG, 34).move_to([4.8, -1.2, 0])
        self.play(FadeIn(sp, shift=LEFT * 0.2), run_time=0.4)
        self.at("they", lead=0.6)
        cyt, mem, p, pl, cap, g, gl, cr, ym = oligo_surface()
        self.play(*[FadeOut(m) for m in (od, od.bodies, od.arms, od.sheaths, cl, ml, ln, b, sp)], FadeIn(cyt), FadeIn(mem), FadeIn(p), FadeIn(pl), FadeIn(cap), run_time=0.7)
        self.at("lack", lead=0.1)
        self.play(Create(g), run_time=0.3)
        self.at("track", lead=0.0)
        self.play(FadeIn(gl), FadeIn(cr), run_time=0.4)
        self.finish()


class S05(SS):
    def construct(self):
        cyt, mem, p, pl, cap, g, gl, cr, ym = oligo_surface()
        self.add(cyt, mem, p, pl, cap, g, gl, cr)
        self.at("stay alive")
        st = chip("stay alive", GREEN, 32).move_to([2.4, 3.15, 0])
        self.play(FadeIn(st, shift=DOWN * 0.2), run_time=0.5)
        xx = cross([4.45, 3.15], 0.3, GREY, 8)
        self.play(FadeIn(xx), run_time=0.3)
        self.at("p75 can read")
        s = 1.6
        d, cyd = ligand(-2.2, ym, s)
        d.shift(UP * 1.6)
        nl = lab("NGF", BLUE, -4.9, cyd + 0.1, 36)
        self.play(FadeIn(d), FadeIn(nl), Indicate(p.bar, color=VIOLET, scale_factor=1.06), run_time=0.5)
        self.play(d.animate.shift(DOWN * 1.6), run_time=0.6)
        self.at("die")
        ar = arr([-2.2, ym - ICD - 0.05, 0], [-2.2, -2.6, 0], RED, 6)
        die = chip("die", RED, 32).move_to([-2.2, -3.1, 0])
        self.play(GrowArrow(ar), FadeIn(die), cyt.animate.set_fill(RED, 0.16), FadeOut(cap), run_time=0.7)
        capn = lab("no Trk, so p75 can read die", TEXT, 1.9, -3.1, 30)
        self.play(FadeIn(capn), run_time=0.4)
        self.finish()


def drip(scene, arrows, n=2, rt=0.5):
    for _ in range(n):
        scene.play(LaggedStart(*[Indicate(a, color=BLUE, scale_factor=1.5) for a in arrows], lag_ratio=0.25), run_time=rt * 2)


class S05b(SS):
    def construct(self):
        self.at("oligodendrocyte")
        od = oligo_dish(-3.7, -0.4, 2.8)
        ol = lab("oligodendrocyte culture", LG, -3.7, -3.65, 26).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(od), FadeIn(od.bodies), FadeIn(od.arms), FadeIn(od.sheaths), FadeIn(ol), run_time=0.8)
        self.at("nanomolar")
        xs = [-5.7, -4.7, -3.7, -2.7, -1.7]
        ds = VGroup(*[dimer(x, 3.0, 0.38) for x in xs])
        ars = VGroup(*[arr([x, 2.82, 0], [x, 2.55, 0], BLUE, 4) for x in xs])
        nl = lab("NGF added: nanomolar", BLUE, -3.7, 3.55, 26)
        self.play(FadeIn(ds, lag_ratio=0.2), FadeIn(ars, lag_ratio=0.2), FadeIn(nl), run_time=0.9)
        drip(self, ars, 1)
        self.at("retina")
        ret = retina(4.0, -0.4, 5.4, 5.8, cols=5, rows=4)
        rl = lab("retina", LG, 6.2, -3.65, 26)
        self.play(FadeIn(ret), FadeIn(rl), run_time=0.8)
        self.at("tissue")
        xs2 = [3.2, 4.8]
        ds2 = VGroup(*[dimer(x, 3.0, 0.38) for x in xs2])
        ars2 = VGroup(*[arr([x, 2.62, 0], [x, 2.85, 0], BLUE, 4) for x in xs2])
        nl2 = lab("NGF the tissue makes", BLUE, 4.0, 3.55, 26)
        self.play(FadeIn(ars2, lag_ratio=0.2), FadeIn(ds2, lag_ratio=0.2), FadeIn(nl2), run_time=0.8)
        drip(self, ars2, 1)
        self.at("chapter")
        ch = chip("Chapter 6:\nwhy dose\nmatters", TEXT, 22, pad=0.14).move_to([0.15, -0.4, 0])
        self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.6)
        self.finish()


S6 = 1.4
PX6 = 1.0


class S06(SS):
    def construct(self):
        ym, s, px = YM, S6, PX6
        mem, cyt = membrane(ym), inside(ym)
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.5, 0.6, 38)
        self.add(cyt, mem, p, pl)
        d, cy = ligand(px, ym, s, tails=False)
        d.shift(UP * 1.5)
        cap = lab("low-affinity contact", TEXT, px + 1.2, -3.4, 30)
        self.play(FadeIn(d), run_time=0.2)
        self.play(d.animate.shift(DOWN * 1.5), FadeIn(cap), run_time=0.6)
        self.at("mature NGF")
        mn = lab("mature NGF", BLUE, px - 3.4, cy, 34)
        self.play(FadeIn(mn), run_time=0.5)
        self.at("pro domain")
        tails = tails_of(px + 0.5 * s, cy, s)
        pdl = lab("pro-domain", ORANGE, px - 3.1, 3.2, 34)
        ln = leader([px - 1.6, 3.15, 0], [px - 0.25, 2.95, 0], ORANGE)
        pn = lab("proNGF", BLUE, px - 3.4, cy, 34)
        self.play(*[GrowFromEdge(t, DOWN) for t in tails], FadeIn(pdl), Create(ln), Transform(mn, pn), run_time=0.7)
        self.play(*[Indicate(t, color=ORANGE, scale_factor=1.25) for t in tails], run_time=0.4)
        self.at("sorta")
        so = sort_parts(px, ym, s)
        so.shift(RIGHT * 1.1)
        sl = lab("sortilin", YELLOW, px + 0.8, -2.7, 32)
        self.play(FadeIn(so), FadeIn(sl), run_time=0.5)
        self.at("grips")
        self.play(so.animate.shift(LEFT * 1.1), run_time=0.4)
        self.play(Indicate(so.cup, color=YELLOW, scale_factor=1.4), run_time=0.3)
        self.at("so a")
        self.play(Indicate(p.bar, color=VIOLET, scale_factor=1.08), run_time=0.5)
        self.at("pair can")
        self.play(Indicate(p.bar, color=VIOLET, scale_factor=1.08), Indicate(so.bar, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("hold it tightly")
        tl = lab("p75 + sortilin: tight hold", TEXT, px + 1.2, -3.4, 30)
        self.play(Transform(cap, tl), run_time=0.5)
        self.finish()


def generic(x, y, k=1.0):
    b = Ellipse(width=0.8 * k, height=0.6 * k, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])
    t = RoundedRectangle(corner_radius=0.07 * k, width=0.2 * k, height=0.5 * k, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.5).move_to([x - 0.15 * k, y + 0.5 * k, 0])
    return VGroup(b, t)


BIG = 2.6
BIG_Y = -1.0
BIG_LY = -3.2


class S07(SS):
    def construct(self):
        self.at("secreted")
        gs = VGroup(*[generic(x, -0.4, 2.6) for x in (-4.0, 0, 4.0)])
        gl = lab("most secreted proteins", LG, 0, 3.0, 38)
        self.play(FadeIn(gs, lag_ratio=0.25), FadeIn(gl), run_time=0.9)
        self.at("NGF")
        d = dimer(0, BIG_Y, BIG)
        nm = lab("NGF", BLUE, 0, BIG_LY, 44)
        self.play(FadeOut(gs), FadeOut(gl), FadeIn(d, scale=0.6), FadeIn(nm), run_time=0.8)
        self.at("longer chain")
        self.play(*[GrowFromEdge(t, DOWN) for t in d.tails], run_time=0.9)
        self.at("pro")
        pn = lab("proNGF", BLUE, 0, BIG_LY, 44)
        self.play(Transform(nm, pn), run_time=0.5)
        self.finish()


class S08(SS):
    def construct(self):
        d = dimer(0, BIG_Y, BIG, tails=True)
        nm = lab("proNGF", BLUE, 0, BIG_LY, 44)
        self.add(d, nm)
        self.at("extra stretch")
        gl = VGroup(*[glow(t) for t in d.tails])
        self.play(FadeIn(gl), *[Indicate(t, color=ORANGE, scale_factor=1.15) for t in d.tails], run_time=0.8)
        self.at("pro domain")
        ty = BIG_Y + 0.695 * BIG
        pd = lab("pro-domain", ORANGE, 4.4, ty + 0.5, 46)
        ln = leader([2.5, ty + 0.4, 0], [0.5 * BIG + 0.2, ty + 0.1, 0], ORANGE, 4)
        self.play(FadeIn(pd), Create(ln), run_time=0.5)
        self.finish()


class S09(SS):
    def construct(self):
        d = dimer(0, BIG_Y, BIG, tails=True)
        nm = lab("proNGF", BLUE, 0, BIG_LY, 44)
        self.add(d, nm)
        self.at("accepted view")
        cl = Circle(radius=3.1, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([0, -0.5, 0])
        small = dimer(0, -1.2, 2.0, tails=True)
        tag = lab("the accepted view", TEXT, 0, 3.45, 38)
        self.play(FadeOut(nm), run_time=0.25)
        self.play(FadeIn(cl), Transform(d, small), FadeIn(tag), run_time=0.9)
        self.at("pro domain")
        sc = scissors(-2.55, 0.15, 1.1)
        self.play(FadeIn(sc), run_time=0.25)
        tl, tr = d[2], d[3]
        cut_tail(self, sc, tl, 1.1, approach=0.1, y_off=0.1, run=0.15, snip_t=0.06)
        cut_tail(self, sc, tr, 1.1, approach=0.12, y_off=0.1, run=0.15, snip_t=0.06)
        self.play(sc.animate.shift(RIGHT * 1.0).set_opacity(0), run_time=0.15)
        self.at("inside")
        il = chip("inside the cell", LG, 30, pad=0.14).move_to([0, -2.75, 0])
        self.play(FadeIn(il), run_time=0.4)
        self.at("cell")
        self.play(Indicate(cl, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.finish()


class S10(SS):
    def construct(self):
        self.at("2001")
        yr = lab("2001", TEXT, -4.4, 3.0, 78)
        cl = Circle(radius=2.2, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([2.6, -0.5, 0])
        inn = dimer(2.6, -1.0, 1.1, tails=False)
        sc = scissors(2.0, -0.3, 0.7)
        av = lab("the accepted view", LG, 2.6, 2.3, 28)
        self.play(FadeIn(yr, shift=UP * 0.2), FadeIn(cl), FadeIn(inn), FadeIn(av), FadeIn(sc), run_time=0.7)
        names = ["Ramee Lee", "Pouneh Kermani", "Kenneth Teng", "Barbara Hempstead"]
        ys = [1.5, 0.4, -0.7, -1.8]
        mobs = [T(n, 48, TEXT).move_to([0, y, 0]).align_to([-6.6, 0, 0], LEFT) for n, y in zip(names, ys)]
        self.at("lee")
        self.play(FadeIn(mobs[0], shift=RIGHT * 0.3), run_time=0.5)
        self.rel("lee", 0.8)
        self.play(FadeIn(mobs[1], shift=RIGHT * 0.3), run_time=0.5)
        self.at("kenneth")
        self.play(FadeIn(mobs[2], shift=RIGHT * 0.3), run_time=0.5)
        self.at("barbara")
        self.play(FadeIn(mobs[3], shift=RIGHT * 0.3), run_time=0.5)
        self.at("added to that")
        out = dimer(2.6, -0.2, 0.8, tails=True)
        out.shift(DOWN * 0.0)
        self.play(FadeIn(out), run_time=0.3)
        self.play(out.animate.shift(RIGHT * 3.0 + UP * 0.2), run_time=1.0)
        ul = lab("uncut proNGF", BLUE, 5.2, 1.5, 28)
        self.play(FadeIn(ul), run_time=0.4)
        self.finish()


class S11(SS):
    def construct(self):
        s = 1.2
        cl = Circle(radius=2.7, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([-3.8, -0.3, 0])
        dA = dimer(-4.5, 0.55, s, tails=True)
        dB = dimer(-3.7, -1.3, s, tails=True)
        self.play(FadeIn(cl), FadeIn(dA), FadeIn(dB), run_time=0.5)
        self.at("secrete")
        out = lab("outside the cell", LG, 3.9, 3.4, 30)
        self.play(dA.animate.shift(RIGHT * 5.5 + UP * 0.3), dB.animate.shift(RIGHT * 6.6 + UP * 0.1), FadeIn(out), run_time=1.4)
        self.at("uncut")
        ul = lab("proNGF, uncut", BLUE, 3.4, -2.75, 32)
        self.play(FadeIn(ul), *[Indicate(t, color=ORANGE, scale_factor=1.3) for t in (dA.tails, dB.tails)], run_time=0.9)
        self.at("enzymes")
        sc = scissors(5.9, 0.2, 1.0)
        el = lab("enzymes", ENZ, 5.9, -0.7, 32)
        self.play(FadeIn(sc, shift=DOWN * 0.2), FadeIn(el), run_time=0.6)
        self.at("cut it")
        cut_tail(self, sc, dB.tails[1], 1.0, approach=0.4, run=0.3)
        self.finish()


class S12(SS):
    def construct(self):
        sd, yD = 2.2, -0.95
        dA = dimer(-3.2, yD, sd, tails=True)
        dB = dimer(3.8, yD, sd, tails=True)
        ol = lab("outside the cell", LG, 0.3, -3.45, 28)
        self.add(dA, dB, ol)
        self.at("plasmin")
        pc = chip("plasmin", ENZ, 30, pad=0.14).move_to([-3.2, 2.35, 0])
        sc = scissors(-5.6, 0.2, 1.3)
        lk = always_redraw(lambda: DashedLine(pc.get_bottom() + DOWN * 0.03, sc.get_top() + UP * 0.05, color=ENZ, stroke_width=3))
        self.add(lk)
        self.play(FadeIn(pc, shift=DOWN * 0.2), FadeIn(sc), run_time=0.3)
        cut_tail(self, sc, dA.tails[0], 1.3, approach=0.12, y_off=0.15, run=0.18, snip_t=0.06)
        cut_tail(self, sc, dA.tails[1], 1.3, approach=0.15, y_off=0.15, run=0.18, snip_t=0.06)
        self.play(sc.animate.shift(RIGHT * 0.8).set_opacity(0), run_time=0.2)
        self.remove(lk)
        self.at("protease")
        pl = lab("protease", ENZ, -1.4, 2.35, 28)
        self.play(FadeIn(pl), run_time=0.3)
        self.at("blood")
        bl = lab("blood protein", LG, 0.1, 3.4, 26)
        self.play(FadeIn(bl), run_time=0.3)
        self.at("plasminogen")
        pg = chip("plasminogen", LG, 28, pad=0.12).move_to([-3.2, 3.4, 0])
        ag = arr([-3.2, 3.02, 0], [-3.2, 2.76, 0], LG, 4)
        self.play(FadeIn(pg, shift=DOWN * 0.2), GrowArrow(ag), run_time=0.4)
        self.at("so can")
        mm = chip("matrix metalloproteinase", ENZ, 26, pad=0.14).move_to([3.8, 2.5, 0])
        sc2 = scissors(1.6, 0.2, 1.3)
        lk2 = always_redraw(lambda: DashedLine(mm.get_bottom() + DOWN * 0.03, sc2.get_top() + UP * 0.05, color=ENZ, stroke_width=3))
        self.add(lk2)
        self.play(FadeIn(mm, shift=DOWN * 0.2), FadeIn(sc2), run_time=0.3)
        cut_tail(self, sc2, dB.tails[0], 1.3, approach=0.12, y_off=0.15, run=0.18, snip_t=0.06)
        cut_tail(self, sc2, dB.tails[1], 1.3, approach=0.15, y_off=0.15, run=0.18, snip_t=0.06)
        self.play(sc2.animate.shift(RIGHT * 0.8).set_opacity(0), run_time=0.2)
        self.remove(lk2)
        self.finish()


class S13(SS):
    def construct(self):
        d = dimer(0, BIG_Y, BIG, tails=True)
        self.play(FadeIn(d, scale=0.9), run_time=0.6)
        self.at("precursor")
        nm = lab("proNGF", BLUE, 0, BIG_LY, 44)
        self.play(FadeIn(nm), run_time=0.4)
        self.at("cut sites")
        marks = cut_marks(0, BIG_Y, BIG)
        yy = BIG_Y + 0.6 * BIG
        ml = lab("cut sites", ENZ, 4.4, yy + 0.4, 38)
        ln = leader([3.1, yy + 0.35, 0], [0.5 * BIG + 0.3, yy + 0.05, 0], ENZ)
        self.play(FadeIn(marks), FadeIn(ml), Create(ln), run_time=0.7)
        self.at("so proteases")
        sc = scissors(-4.6, yy + 0.7, 1.3)
        self.play(FadeIn(sc), run_time=0.4)
        self.at("cannot")
        locks = VGroup(*[lock(sx * 0.5 * BIG, yy, 2.4) for sx in (-1, 1)])
        self.play(Transform(marks, locks), FadeOut(ml), FadeOut(ln), run_time=0.6)
        self.at("trim")
        self.play(sc.animate.shift(RIGHT * 1.7), run_time=0.35)
        self.play(sc.animate.shift(LEFT * 0.6), run_time=0.3)
        un = lab("uncleavable proNGF", BLUE, 0, BIG_LY, 44)
        self.play(Transform(nm, un), FadeOut(sc), run_time=0.5)
        self.finish()


class S14(SS):
    def construct(self):
        cl = RoundedRectangle(corner_radius=1.3, width=10.4, height=3.6, stroke_color=GREY, stroke_width=5,
                              fill_color=GREY, fill_opacity=0.12).move_to([0, -2.0, 0])
        cll = lab("cultured cell", LG, 0, -2.7, 36)
        self.play(FadeIn(cl), run_time=0.4)
        self.at("cultured")
        self.play(FadeIn(cll), run_time=0.4)

        def bar(x, top, color, op, w=0.8):
            bot = -1.35
            return RoundedRectangle(corner_radius=0.2, width=w, height=top - bot, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=op).move_to([x, (top + bot) / 2, 0])
        self.at("p75")
        pb = bar(-3.0, 2.3, VIOLET, 0.55)
        pl = lab("p75", VIOLET, -3.0, 2.75, 40)
        self.play(FadeIn(pb, shift=UP * 0.3), FadeIn(pl), run_time=0.5)
        self.at("sordilin")
        sb = bar(0.0, 2.3, YELLOW, 0.5)
        sl = lab("sortilin", YELLOW, 0.0, 2.75, 40)
        self.play(FadeIn(sb, shift=UP * 0.3), FadeIn(sl), run_time=0.5)
        self.at("little")
        tb = bar(3.2, 0.3, PINK, 0.3)
        tl = lab("little TrkA", PINK, 3.2, 0.9, 38)
        self.play(FadeIn(tb, shift=UP * 0.2), FadeIn(tl), run_time=0.5)
        self.finish()


class S15(SS):
    def construct(self):
        tab = Tab(1, [["box", "box", "box"]])
        yb = -2.5
        self.play(FadeIn(tab.rows[0]), run_time=0.6)
        self.at("mature NGF")
        self.play(FadeIn(tab.heads[0]), FadeIn(tab.boxes[(0, 0)]), run_time=0.5)
        self.at("uncleavable")
        self.play(FadeIn(tab.heads[1]), FadeIn(tab.boxes[(0, 1)]), run_time=0.5)
        self.at("same concentration")
        br = bracket(CX[0] - 1.5, CX[1] + 1.5, yb)
        sc = lab("same concentration", TEXT, (CX[0] + CX[2]) / 2, -2.95, 28)
        self.play(Create(br), FadeIn(sc), run_time=0.7)
        self.at("block")
        br2 = bracket(CX[0] - 1.5, CX[2] + 1.5, yb)
        self.play(FadeIn(tab.heads[2]), FadeIn(tab.boxes[(0, 2)]), Transform(br, br2), run_time=0.7)
        self.at("predict")
        q0 = res_q(CX[0], tab.ys[0])
        q1 = res_q(CX[1], tab.ys[0])
        q2 = res_q(CX[2], tab.ys[0])
        pr = lab("Predict each result.", TEXT, (CX[0] + CX[2]) / 2, -3.5, 30)
        self.play(FadeIn(q0, scale=0.5), FadeIn(pr), run_time=0.3)
        self.at("each")
        self.play(FadeIn(q1, scale=0.5), run_time=0.3)
        self.at("result")
        self.play(FadeIn(q2, scale=0.5), run_time=0.3)
        self.finish()


def table_footer_s15():
    yb = -2.5
    br = bracket(CX[0] - 1.5, CX[2] + 1.5, yb)
    sc = lab("same concentration", TEXT, (CX[0] + CX[2]) / 2, -2.95, 28)
    return br, sc


class S16Pause(NarratedScene):
    def construct(self):
        tab = Tab(1, q_states())
        br, sc = table_footer_s15()
        pr = lab("Pause and predict", TEXT, (CX[0] + CX[2]) / 2, -3.5, 34)
        self.add(tab.group(), br, sc, pr)
        self.wait(0.6)
        self.play(*[Indicate(tab.cont[(0, c)], color=TEXT, scale_factor=1.15) for c in range(3)], run_time=1.0)
        self.finish()


class S17(SS):
    def construct(self):
        tab = Tab(1, q_states())
        self.add(tab.group())
        self.at("worked example")
        n1 = lab("worked example after Lee et al., 2001, and Nykjær et al., 2004", "#E3E7EE", 1.0, -2.7, 26)
        self.play(FadeIn(n1), run_time=0.5)
        self.at("low dose")
        n2 = lab("p75 and sortilin cells, little TrkA; same low dose of each form", "#E3E7EE", 1.0, -3.2, 26)
        self.play(FadeIn(n2), run_time=0.5)
        self.at("no death")
        reveal_ok(self, tab, 0, 0)
        self.at("killed")
        reveal_die(self, tab, 0, 1)
        self.finish()


class S18(SS):
    def construct(self):
        tab = Tab(1, [["ok", "die", "q"]])
        self.add(tab.group())
        self.at("antibody")
        n1 = chip("anti-p75 antibody", VIOLET, 24, pad=0.06).move_to([CX[2], -2.6, 0])
        self.play(FadeIn(n1, shift=UP * 0.2), run_time=0.5)
        self.at("prevented")
        reveal_ok(self, tab, 0, 2)
        self.at("mice")
        n2 = chip("p75-null cells", VIOLET, 24, pad=0.06).move_to([CX[2], -3.2, 0])
        self.play(FadeIn(n2, shift=UP * 0.2), run_time=0.5)
        self.at("lacking")
        self.play(Indicate(tab.cont[(0, 2)], color=GREEN, scale_factor=1.08), run_time=0.8)
        self.finish()


class S19(SS):
    def construct(self):
        ym, s, px = YM, 1.4, 0.0
        mem, cyt = membrane(ym), inside(ym)
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.5, 0.6, 40)
        self.play(FadeIn(cyt), FadeIn(mem), FadeIn(p), FadeIn(pl), run_time=0.3)
        d, cy = ligand(px, ym, s, tails=True)
        d.shift(LEFT * 3.9 + UP * 0.6)
        dl = lab("uncut proNGF", BLUE, 4.3, cy + 0.2, 34)
        self.at("precursor")
        self.play(FadeIn(d, shift=RIGHT * 0.3), run_time=0.4)
        self.at("kills")
        self.play(d.animate.shift(RIGHT * 3.9 + DOWN * 0.6), FadeIn(dl), run_time=0.6)
        self.at("through")
        a2 = arr([px, ym - ICD - 0.05, 0], [px, -2.95, 0], RED, 7)
        dd = chip("death", RED, 34, pad=0.14).move_to([px, -3.4, 0])
        self.play(GrowArrow(a2), FadeIn(dd), cyt.animate.set_fill(RED, 0.14), Indicate(p.bar, color=VIOLET, scale_factor=1.06), run_time=0.7)
        self.at("without being")
        gl = VGroup(*[glow(t) for t in d.tails])
        self.play(FadeIn(gl), Indicate(d.tails, color=ORANGE, scale_factor=1.2), run_time=0.9)
        self.finish()


class S20(SS):
    def construct(self):
        t2 = Tab(2, [final_row1(), ["box", "box", None]])
        row2_lab = t2.rows[1]
        self.add(*[m for m in t2.pieces([0])], t2.boxes[(1, 0)], t2.boxes[(1, 1)])
        self.at("uncut")
        self.play(Indicate(t2.heads[1], color=BLUE, scale_factor=1.1), run_time=0.7)
        self.at("also")
        self.play(FadeIn(row2_lab), run_time=0.5)
        self.at("apoptosis")
        reveal_die(self, t2, 1, 1)
        self.at("sympathetic")
        self.play(Indicate(row2_lab, color=TEXT, scale_factor=1.1), run_time=0.8)
        self.finish()


def sym_stage():
    ym = YM
    mem, cyt = membrane(ym), inside(ym)
    return cyt, mem, ym


class S21(SS):
    def construct(self):
        cyt, mem, ym = sym_stage()
        s, px = 1.4, -2.6
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.5, 0.6, 38)
        head_ = lab("sympathetic neurons", LG, 0.0, -3.5, 30)
        self.play(FadeIn(cyt), FadeIn(mem), FadeIn(p), FadeIn(pl), FadeIn(head_), run_time=0.3)
        d, cy = ligand(px, ym, s, tails=True)
        dl = lab("uncut\nproNGF", BLUE, px - 2.0, cy + 0.3, 30, line_spacing=0.7)
        d.shift(UP * 1.2)
        self.at("bound")
        self.play(FadeIn(d), FadeIn(dl), run_time=0.2)
        self.play(d.animate.shift(DOWN * 1.2), run_time=0.6)
        self.at("tightly")
        tg = lab("tight hold", TEXT, px + 2.4, 0.9, 32)
        ln = leader([px + 1.2, 0.95, 0], [px + 0.5, 1.4, 0], TEXT)
        self.play(FadeIn(tg), Create(ln), Indicate(p.bar, color=VIOLET, scale_factor=1.1), run_time=0.6)
        self.at("activated")
        t = trk(3.8, ym, ecd=ECD, icd=ICD, w=0.8)
        tl = lab("TrkA", PINK, 3.8, 1.8, 36)
        self.play(FadeIn(t), FadeIn(tl), run_time=0.5)
        self.at("very little")
        gl = Circle(radius=0.3, stroke_width=0, fill_color=PINK, fill_opacity=0.35).move_to(t.foot.get_center())
        bl = lab("barely active", PINK, 5.55, -2.6, 26)
        self.play(FadeIn(gl), FadeIn(bl), run_time=0.6)
        self.finish()


class S22(SS):
    def construct(self):
        t2 = Tab(2, [final_row1(), ["box", "die", None]])
        self.at("mature")
        self.play(FadeIn(t2.group()), run_time=0.5)
        self.at("kept")
        self.play(Indicate(t2.heads[0], color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("alive")
        x, y, h = CX[0], t2.ys[1], t2.h
        cells_ = res_cells(x, y, h, "ok")
        txt = res_text(x, y, h, "surv", dy=0.2)
        self.play(FadeIn(cells_), FadeIn(txt), run_time=0.6)
        self.at("through")
        via = lab("through TrkA", PINK, x, y - 0.8, 24)
        self.play(FadeIn(via), run_time=0.4)
        self.finish()


class S23(SS):
    def construct(self):
        ym = YM
        mem, cyt = membrane(ym), inside(ym)
        px = 2.9
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.2, 0.6, 38)
        self.at("2004")
        yr = lab("2004", TEXT, -4.6, 3.0, 78)
        self.play(FadeIn(yr, shift=UP * 0.2), FadeIn(cyt), FadeIn(mem), FadeIn(p), FadeIn(pl), run_time=0.7)
        self.at("anders")
        n1 = T("Anders Nykjær", 46, TEXT).move_to([0, 1.5, 0]).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(n1, shift=RIGHT * 0.3), run_time=0.5)
        self.rel("anders", 1.0)
        n2 = T("Claus Munck Petersen", 46, TEXT).move_to([0, 0.4, 0]).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(n2, shift=RIGHT * 0.3), run_time=0.5)
        self.at("colleagues")
        n3 = T("and colleagues", 40, LG).move_to([0, -0.6, 0]).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(n3, shift=RIGHT * 0.3), run_time=0.5)
        self.at("missing partner")
        sx = px + 0.8
        gh = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=0.8, height=ECD + ICD).move_to([sx, ym + (ECD - ICD) / 2, 0]).set_stroke(LG, 3), num_dashes=30)
        q = lab("?", TEXT, sx, 0.4, 80)
        ml = lab("the missing\npartner", LG, sx + 1.9, 0.4, 30, line_spacing=0.75)
        self.play(FadeIn(gh), FadeIn(q), FadeIn(ml), run_time=0.7)
        self.finish()


S24PX = -0.8


class S24(SS):
    def construct(self):
        ym, px = YM, S24PX
        mem, cyt = membrane(ym), inside(ym)
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.5, 0.6, 40)
        self.add(cyt, mem, p, pl)
        self.at("needs")
        so = sort_parts(px, ym, 1.4, arm=False)
        so.shift(RIGHT * 3.6)
        self.play(FadeIn(so), run_time=0.3)
        self.play(so.animate.shift(LEFT * 3.6), run_time=0.9)
        sl = lab("sortilin", YELLOW, px + 2.6, 0.6, 38)
        sln = leader([px + 1.65, 0.6, 0], [px + 1.25, 0.6, 0], YELLOW)
        self.play(FadeIn(sl), Create(sln), run_time=0.4)
        self.at("deliver")
        a = arr([px + 0.4, ym - ICD - 0.05, 0], [px + 0.4, -2.95, 0], RED, 7)
        dd = chip("die", RED, 34, pad=0.14).move_to([px + 0.4, -3.4, 0])
        dsl = lab("death signal", RED, px + 2.6, -2.6, 32)
        self.play(GrowArrow(a), FadeIn(dd), FadeIn(dsl), cyt.animate.set_fill(RED, 0.12), run_time=0.7)
        self.finish()


class S25(SS):
    def construct(self):
        ym, px, s = YM, S24PX, 1.2
        mem, cyt = membrane(ym), inside(ym)
        p = stalk(px, ym)
        pl = lab("p75", VIOLET, px - 1.5, 0.6, 40)
        so = sort_parts(px, ym, s, arm=True)
        solid = VGroup(so.bar)
        sl = lab("sortilin", YELLOW, px + 0.8, -2.7, 34)
        self.add(cyt, mem, p, pl, solid, sl)
        d, cy = ligand(px, ym, s, tails=True)
        d.shift(UP * 1.5)
        self.play(FadeIn(d), run_time=0.1)
        self.play(d.animate.shift(DOWN * 1.5), run_time=0.5)
        self.at("grips")
        self.play(Create(so.arm), Create(so.cup), run_time=0.6)
        self.at("pro domain")
        pd = lab("pro-domain", ORANGE, px + 0.6, 3.5, 32)
        pdl = VGroup()
        self.play(Indicate(d.tails[1], color=ORANGE, scale_factor=1.3), FadeIn(pd), Create(pdl), run_time=0.8)
        self.at("p75")
        ml = lab("mature part", TEXT, px - 3.0, cy + 0.2, 36)
        mln = leader([px - 1.5, cy + 0.1, 0], [px - 0.7, cy, 0], TEXT)
        self.play(FadeIn(ml), Create(mln), run_time=0.4)
        self.at("grips", nth=1)
        pc = p75_cup(px, ym, s)
        self.play(Create(pc), Indicate(p.bar, color=VIOLET, scale_factor=1.06), run_time=0.8)
        self.finish()


def scope_tile(kind, x, y):
    w, h = 4.3, 5.2
    ic_y = y + 0.95
    box = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3)
    if kind == "culture":
        ic = VGroup(Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07),
                    *[Circle(radius=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([dx, dy, 0])
                      for dx, dy in ((-0.5, 0.4), (0.45, 0.5), (0.0, -0.5), (0.55, -0.25))]).move_to([x, ic_y, 0])
        t1 = T("in culture", 34, TEXT).move_to([x, y - 0.65, 0])
        t2 = T("cultured neurons and\noligodendrocyte lineage", 24, LG, line_spacing=0.75).move_to([x, y - 1.55, 0])
        grp = VGroup(box.move_to([x, y, 0]), ic, t1, t2)
    elif kind == "injury":
        tis = RoundedRectangle(corner_radius=0.25, width=2.8, height=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2)
        zz = VMobject(stroke_color=RED, stroke_width=7)
        zz.set_points_as_corners([[-0.25, 0.85, 0], [0.15, 0.25, 0], [-0.2, -0.15, 0], [0.25, -0.85, 0]])
        ic = VGroup(tis, zz).move_to([x, ic_y, 0])
        t1 = T("rodent injury\nmodels", 34, TEXT, line_spacing=0.75).move_to([x, y - 0.85, 0])
        t2 = VGroup()
        grp = VGroup(box.move_to([x, y, 0]), ic, t1, t2)
    else:
        box = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=LG, stroke_width=3).move_to([x, y, 0]), num_dashes=64)
        em = DashedVMobject(Ellipse(width=2.6, height=1.7, stroke_color=LG, stroke_width=4), num_dashes=28)
        cs = VGroup(*[Circle(radius=0.17, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([dx, dy, 0])
                      for dx, dy in ((-0.65, 0.1), (0.1, 0.35), (0.65, -0.2))])
        ic = VGroup(em, cs).move_to([x, ic_y, 0])
        t1 = T("normal\ndevelopment", 34, TEXT, line_spacing=0.75).move_to([x, y - 0.85, 0])
        t2 = VGroup()
        grp = VGroup(box, ic, t1, t2)
    return grp


class S26(SS):
    def construct(self):
        hd = lab("where the killing was shown", LG, 0, 3.4, 32)
        a = scope_tile("culture", -2.4, -0.15)
        self.play(FadeIn(hd), FadeIn(a), run_time=0.5)
        self.at("rodent")
        b = scope_tile("injury", 2.4, -0.15)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S27(SS):
    def construct(self):
        hd = lab("where the killing was shown", LG, 0, 3.4, 32)
        a = scope_tile("culture", -2.4, -0.15)
        b = scope_tile("injury", 2.4, -0.15)
        self.add(hd, a, b)
        c = scope_tile("dev", 4.4, -0.15)
        self.at("normal")
        self.play(a.animate.shift(LEFT * 2.0), b.animate.shift(LEFT * 2.4), hd.animate.shift(LEFT * 1.0), run_time=0.6)
        self.play(FadeIn(c), run_time=0.6)
        self.at("less clear")
        q = lab("?", TEXT, 5.7, 1.65, 80)
        lc = lab("less clear", TEXT, 4.4, -2.05, 34)
        self.play(FadeIn(q, scale=0.6), FadeIn(lc), run_time=0.7)
        self.finish()


class S28(SS):
    def construct(self):
        ym = -0.9
        mem, cyt = membrane(ym), inside(ym)
        TX = 0.0
        s = 1.4
        t = trk(TX, ym, ecd=2.2, icd=ICD, w=0.8)
        tl = lab("TrkA", PINK, TX - 1.4, 0.7, 38)
        t.bar.set_stroke(PINK, 3, opacity=0.45).set_fill(PINK, 0.22)
        t.foot.set_stroke(PINK, 3, opacity=0.45).set_fill(PINK, 0.15)
        self.add(cyt, mem, t, tl)
        self.at("another group")
        ag = chip("another group", LG, 30).move_to([-4.6, 3.3, 0])
        self.play(FadeIn(ag), run_time=0.5)
        self.at("uncleavable")
        top = ym + 2.2
        cyd = top + 0.375 * s
        d = dimer(TX + 0.5 * s - 0.5 * s, cyd, s, tails=True)
        locks = VGroup(*[lock(TX + sx * 0.5 * s, cyd + 0.62 * s, 2.2) for sx in (-1, 1)])
        dl = lab("uncleavable proNGF", BLUE, 4.2, cyd + 0.4, 34)
        self.play(FadeIn(d, shift=DOWN * 0.2), FadeIn(locks), FadeIn(dl), run_time=0.7)
        self.at("neurons")
        nl = lab("sympathetic neuron", LG, 4.6, -1.5, 32)
        self.play(FadeIn(nl), run_time=0.4)
        self.at("alive")
        al = chip("survives", GREEN, 32, pad=0.14).move_to([3.8, -2.4, 0]).align_to([2.1, 0, 0], LEFT)
        ar = arr([0.65, -2.4, 0], [1.95, -2.4, 0], GREEN, 6)
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.6)
        self.at("through")
        gl = Circle(radius=0.62, stroke_width=0, fill_color=PINK, fill_opacity=0.1).move_to(t.foot.get_center())
        self.play(FadeIn(gl), t.foot.animate.set_fill(PINK, 0.22), run_time=0.6)
        self.at("did so", lead=0.5)
        wk = chip("survives, less well", GREEN, 32, pad=0.14).move_to([3.95, -2.4, 0])
        wk[0].set_stroke(GREEN, 2).set_fill(GREEN, 0.07)
        wk[1].set_color("#A9D49A")
        wk.align_to([2.1, 0, 0], LEFT)
        self.play(Transform(al, wk), run_time=0.6)
        self.finish()


class S29(SS):
    def construct(self):
        ym, s = -0.4, 1.2
        ecd = 2.2
        mem, cyt = membrane(ym), inside(ym)
        self.add(cyt, mem)
        pxL = -4.0
        p = stalk(pxL, ym, ecd=ecd)
        pl = lab("p75", VIOLET, pxL - 1.3, 0.6, 36)
        self.play(FadeIn(p), FadeIn(pl), run_time=0.4)
        self.at("takeaway")
        tag = lab("The takeaway", TEXT, -3.6, 3.65, 34)
        dsh = DashedLine([-1.2, 3.3, 0], [-1.2, -3.7, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(tag), Create(dsh), run_time=0.5)
        self.at("can read")
        cap1 = lab("in a cell with no Trk,\np75 can read a neurotrophin as die", TEXT, -3.95, -3.4, 22, line_spacing=0.7)
        self.play(FadeIn(cap1), run_time=0.4)
        self.at("neurotrophin")
        dL, cyL = ligand(pxL, ym, s, ecd=ecd)
        dL.shift(UP * 1.2)
        self.play(FadeIn(dL), run_time=0.3)
        self.play(dL.animate.shift(DOWN * 1.2), run_time=0.6)
        nl = lab("neurotrophin", BLUE, -3.6, 3.05, 28)
        self.play(FadeIn(nl), run_time=0.3)
        self.at("as", lead=-0.1)
        a1 = arr([pxL, ym - ICD - 0.05, 0], [pxL, -2.2, 0], RED, 8)
        o1 = chip("die", RED, 34, pad=0.14, fill_opacity=0.45).move_to([pxL, -2.65, 0])
        self.play(GrowArrow(a1), FadeIn(o1), run_time=0.6)
        self.at("with")
        pxR = 0.5
        pR = stalk(pxR, ym, ecd=ecd)
        so = sort_parts(pxR, ym, s, ecd=ecd, arm=True)
        sl = lab("sortilin", YELLOW, pxR + 3.0, -1.2, 30)
        sln = leader([pxR + 2.2, -1.2, 0], [pxR + 1.25, -1.2, 0], YELLOW)
        pl3 = lab("p75", VIOLET, pxR - 1.0, 0.6, 36)
        self.play(FadeIn(pR), FadeIn(so), FadeIn(sl), FadeIn(sln), FadeIn(pl3), run_time=0.7)
        self.at("uncut precursor")
        dR, cyR = ligand(pxR, ym, s, ecd=ecd, tails=True)
        ul = lab("uncut proNGF", BLUE, pxR + 4.2, cyR + 0.3, 30)
        cap2 = lab("with sortilin, p75 reads the\nuncut precursor as die", TEXT, 2.9, -3.4, 22, line_spacing=0.7)
        dR.shift(UP * 1.0)
        a3 = arr([pxR, ym - ICD - 0.05, 0], [pxR, -2.2, 0], RED, 8)
        o3 = chip("die", RED, 34, pad=0.14, fill_opacity=0.45).move_to([pxR, -2.65, 0])
        self.play(FadeIn(dR), FadeIn(ul), FadeIn(cap2), dR.animate.shift(DOWN * 1.0), run_time=0.45)
        self.play(GrowArrow(a3), FadeIn(o3), cyt.animate.set_fill(RED, 0.1), run_time=0.5)
        self.finish()


class S30End(EndCard):
    LINE = "p75 can read neurotrophins as die,\nand with sortilin, uncut proNGF too."
