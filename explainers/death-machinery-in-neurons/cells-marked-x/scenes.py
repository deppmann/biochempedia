"""Cells Marked with an X  (chapter 2 of "The Death Machinery in Neurons")  -- fix round

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Cue rule for this round: a picture appears on (at most 0.1 s before) the word that names it.

COLOR MAP (one color per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  BLUE   = a living cell / the neuron (here: C. elegans cells, the worm, surviving tips)
  YELLOW = NGF, the survival signal (not used in this chapter)
  TEAL   = unknown / new gene expression (here: every question mark, every unknown gene or protein)
  ORANGE = pro-death BCL-2 family proteins (here: EGL-1, the BH3-only protein)
  PINK   = cytochrome c (not used in this chapter)
  PURPLE = CED-4 / Apaf-1
  RED    = the killers (CED-3 / caspases) and death itself: every X
  GREEN  = protective: CED-9 / Bcl-2, the brake
  GREY   = lineage branches, timelines, labels, dead or inactive things
  GOLD   = the "eat me" tag (here: ced-1, the engulfment gene)
  WHITE (TEXT) = glowing corpses, rings and highlights
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
GENECOL = {"ced-3": RED, "ced-4": PURPLE, "ced-9": GREEN, "egl-1": ORANGE}


class KS(SpokenScene):
    """SpokenScene whose cues fire 0.1 s before the word (the animation then lands on the word)."""

    def at(self, phrase, lead=0.1, nth=0):
        return super().at(phrase, lead, nth)


# ---------------------------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    g.box, g.label = c[0], c[1]
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=GREEN, w=7, bar=0.32):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * bar, b - perp * bar, color=color, stroke_width=w + 2))


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def gtext(text, size=26, color=TEXT):
    return T(text, size, color, t2c=GENECOL)


def cap(text, color=GREY, size=34, y=-3.5, **kw):
    """A caption at the bottom of the frame."""
    return T(text, size, color, **kw).move_to([0, y, 0])


# ---------------------------------------------------------------------------------------------
# the worm
# ---------------------------------------------------------------------------------------------
def worm_geom(x0, x1, cy, amp, waves, wmax, phase=0.0, n=140):
    t = np.linspace(0, 1, n)
    xs = x0 + (x1 - x0) * t
    ys = cy + amp * np.sin(phase + TAU * waves * t)
    w = wmax * np.power(np.sin(np.pi * t) + 1e-6, 0.4)
    dx, dy = np.gradient(xs), np.gradient(ys)
    L = np.hypot(dx, dy)
    return dict(xs=xs, ys=ys, w=w, nx=-dy / L, ny=dx / L, n=n)


def worm_body(g, color=BLUE, fill=0.9, sw=4):
    z = np.zeros_like(g["xs"])
    top = np.stack([g["xs"] + g["nx"] * g["w"], g["ys"] + g["ny"] * g["w"], z], 1)
    bot = np.stack([g["xs"] - g["nx"] * g["w"], g["ys"] - g["ny"] * g["w"], z], 1)
    return Polygon(*np.vstack([top, bot[::-1]]), stroke_color=color, stroke_width=sw,
                   fill_color=color, fill_opacity=fill)


def worm_gut(g, color=GREY, sw=10):
    i0, i1 = int(0.06 * g["n"]), int(0.94 * g["n"])
    pts = np.stack([g["xs"][i0:i1], g["ys"][i0:i1], np.zeros(i1 - i0)], 1)
    m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=0.55)
    m.set_points_smoothly(pts)
    return m


def worm_len(g):
    return float(np.sum(np.hypot(np.diff(g["xs"]), np.diff(g["ys"]))))


def worm_pt(g, t, off):
    i = int(np.clip(t, 0, 1) * (g["n"] - 1))
    return np.array([g["xs"][i] + g["nx"][i] * g["w"][i] * off, g["ys"][i] + g["ny"][i] * g["w"][i] * off, 0.0])


WG = worm_geom(-5.8, 5.8, 0.4, 0.65, 1.25, 1.45)


def _scatter(g, count, rng, taken, min_d, off_max, t0=0.08, t1=0.92):
    pts = []
    tries = 0
    while len(pts) < count and tries < 6000:
        tries += 1
        p = worm_pt(g, rng.uniform(t0, t1), rng.uniform(-off_max, off_max))
        if all(np.linalg.norm(p - q) > min_d for q in pts + taken):
            pts.append(p)
    return pts


_rng = np.random.default_rng(7)
NUC_POS = _scatter(WG, 26, _rng, [], 0.62, 0.62)
COR_POS = _scatter(WG, 6, _rng, NUC_POS, 0.6, 0.6, 0.12, 0.9)


def dic_nuc(p, r=0.25, relief=False):
    """A nucleus in relief (Nomarski look): dark shadow side, bright rim side, lit dome."""
    p = np.array(p, float)
    sh = Circle(r, stroke_width=0, fill_color="#000000", fill_opacity=0.7).move_to(p + np.array([0.08, -0.08, 0]))
    base = Circle(r, stroke_width=2, stroke_color=GREY, fill_color="#6C7893", fill_opacity=0.95).move_to(p)
    dome = Circle(r * 0.62, stroke_width=0, fill_color="#D5DDEC", fill_opacity=0.6).move_to(p + np.array([-0.06, 0.06, 0]))
    hi = Arc(radius=r * 0.88, start_angle=PI * 0.55, angle=PI * 0.9, arc_center=p, stroke_color=TEXT, stroke_width=4)
    dk = Arc(radius=r * 0.88, start_angle=PI * 1.55, angle=PI * 0.9, arc_center=p, stroke_color="#171B26",
             stroke_width=4)
    if relief:
        # Directional bright/dark crescents make the optical relief explicit.
        sh.scale(1.16).shift([0.035, -0.035, 0]).set_fill(opacity=0.95)
        base.set_fill("#8795AA", 1).set_stroke("#263349", 2)
        hi.set_stroke(TEXT, 7)
        dk.set_stroke("#080D18", 7)
        return VGroup(sh, base, hi, dk)
    g = VGroup(sh, base, dome, hi, dk)
    return g


def corpse(p, r=0.2):
    halo2 = Circle(r * 2.3, stroke_width=0, fill_color=TEXT, fill_opacity=0.14)
    halo1 = Circle(r * 1.6, stroke_width=0, fill_color=TEXT, fill_opacity=0.28)
    core = Circle(r, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.95)
    return VGroup(halo2, halo1, core).move_to(p)


def clear_worm(fill=0.12):
    """The worm as it looks from scene 3 on: see-through body and gut."""
    return worm_body(WG, BLUE, fill), worm_gut(WG)


# ---------------------------------------------------------------------------------------------
# the lineage tree
# ---------------------------------------------------------------------------------------------
DIV = [[0.10], [0.24, 0.21], [0.38, 0.34, 0.42, 0.36], [0.55, 0.50, 0.58, 0.52, 0.60, 0.47, 0.56, 0.53]]
DEATH_U = {1: 0.72, 6: 0.64, 9: 0.86, 14: 0.57}   # the four doomed cells (leaf index -> time of death)
EXTRA = (2, 7, 10, 13)                              # cells that die only when ced-9 is lost


class Tree:
    """16-tip schematic lineage tree.  full=True: every branch runs to the bottom (before any death is shown)."""

    def __init__(self, cx=0.0, width=10.4, ytop=3.3, ybot=-2.5, lw=4.5, dr=0.11, xs=0.22, full=False):
        self.lx = [cx - width / 2 + (i + 0.5) * width / 16 for i in range(16)]
        lx = self.lx
        self.cx, self.ytop, self.ybot = cx, ytop, ybot
        self.Y = lambda u: ytop - u * (ytop - ybot)
        Y = self.Y

        def nx(L, j):
            span = 16 >> L
            return float(np.mean(lx[j * span:(j + 1) * span]))

        self.nx = nx
        mk = lambda a, b, col=GREY: Line([a[0], a[1], 0], [b[0], b[1], 0], color=col, stroke_width=lw)
        self.mk = mk
        self.stages, self.leaf_line = [], {}
        for L in range(5):
            bars, verts = [], []
            if L > 0:
                for j in range(2 ** (L - 1)):
                    u = DIV[L - 1][j]
                    bars.append(mk((nx(L, 2 * j), Y(u)), (nx(L, 2 * j + 1), Y(u))))
            for j in range(2 ** L):
                birth = 0 if L == 0 else DIV[L - 1][j // 2]
                end = DIV[L][j] if L < 4 else (1.0 if full else DEATH_U.get(j, 1.0))
                ln = mk((nx(L, j), Y(birth)), (nx(L, j), Y(end)))
                verts.append(ln)
                if L == 4:
                    self.leaf_line[j] = ln
            self.stages.append(VGroup(*bars, *verts))
        self.lines = VGroup(*[m for s in self.stages for m in s])
        self.dot_of = {i: Dot([lx[i], Y(1.0), 0], radius=dr, color=BLUE) for i in range(16)
                       if full or i not in DEATH_U}
        self.dots = VGroup(*self.dot_of.values())
        self.x_of = {i: xmark([lx[i], Y(u), 0], xs, RED, 7) for i, u in DEATH_U.items()}
        self.xs = VGroup(*self.x_of.values())
        self._lw, self._dr = lw, dr

    def all(self):
        return VGroup(self.lines, self.dots, self.xs)

    def short_line(self, i, col=GREY):
        """leaf i's branch as it is drawn when the cell dies (ends at its X)"""
        top = self.leaf_line[i].get_start()
        return self.mk(top, (self.lx[i], self.Y(DEATH_U[i])), col)

    def tip(self, i, which="x"):
        """position of leaf i's end (x mark) or bottom (dot)"""
        return np.array([self.lx[i], self.Y(DEATH_U[i] if (which == "x" and i in DEATH_U) else 1.0), 0])

    def survive(self, i):
        """extension line and dot for a doomed cell that lives"""
        ext = Line(self.tip(i, "x"), self.tip(i, "dot"), color=GREY, stroke_width=self._lw)
        dot = Dot(self.tip(i, "dot"), radius=self._dr, color=BLUE)
        return ext, dot

    def extra_mark(self, i):
        """an extra death (ced-9 lost): a ringed X, drawn differently from the normal deaths"""
        p = self.tip(i, "dot")
        ring = Circle(0.3, stroke_color=RED, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(p)
        return VGroup(ring, xmark(p, 0.15, RED, 6))


TR = dict(cx=0.0, width=10.4, ytop=3.3, ybot=-2.5)
TR_SMALL = dict(width=4.25, ytop=2.9, ybot=-3.3, lw=3.8, dr=0.09, xs=0.17)


def neuron(p, scale=1.0):
    """A neuron-like cell with a soma and branched neurites reaching downward (about 3x the old glyph)."""
    p = np.array(p, float)
    soma = Circle(0.52 * scale, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.95).move_to(p)
    parts = []
    for a, L in ((198, 1.45), (230, 1.3), (310, 1.3), (342, 1.45)):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        e = p + d * L * scale
        parts.append(Line(p + d * 0.4 * scale, e, color=BLUE, stroke_width=7))
        for da in (-35, 35):
            d2 = np.array([np.cos(np.radians(a + da)), np.sin(np.radians(a + da)), 0])
            parts.append(Line(e - d * 0.25 * scale, e + d2 * 0.2 * scale, color=BLUE, stroke_width=5))
    return VGroup(VGroup(*parts), soma)


def magnifier(p):
    c = Circle(0.4, stroke_color=TEXT, stroke_width=6, fill_color=BG, fill_opacity=0.0)
    h = Line([0.28, -0.28, 0], [0.72, -0.72, 0], color=TEXT, stroke_width=8)
    return VGroup(c, h).shift(np.array(p, float))


def clock(p, r=0.32):
    p = np.array(p, float)
    return VGroup(Circle(r, stroke_color=TEXT, stroke_width=4).move_to(p),
                  Line(p, p + [0, r * 0.7, 0], color=TEXT, stroke_width=4),
                  Line(p, p + [r * 0.5, 0, 0], color=TEXT, stroke_width=4))


# ---------------------------------------------------------------------------------------------
# the genotype table
# ---------------------------------------------------------------------------------------------
LABX = -5.85                      # left edge of the genotype labels (about 80 px in from the frame edge)
COLX = [-3.1, 1.3, 4.5]
ROWY = [2.0, 1.17, 0.34, -0.49, -1.32, -2.15]
ROWS = {"wt": ("wild type", "die", "live"),
        "loss34": ("loss of ced-3 or ced-4", "live", "live"),
        "gain9": ("gain of function in ced-9", "live", "live"),
        "loss9": ("loss of ced-9", "die", "many die"),
        "loss93": ("loss of ced-9 and ced-3", "?", "?"),
        "loss94": ("loss of ced-9 and ced-4", "few die", "few die"),
        "lossegl": ("loss of egl-1", "mostly live", "live")}


def vchip(kind):
    if kind == "die":
        return bchip("dies", RED, 28, pad=0.14)
    if kind == "many die":
        return bchip("many die", RED, 28, pad=0.14)
    if kind == "live":
        return bchip("lives", BLUE, 28, pad=0.14)
    if kind == "few die":
        return bchip("few die", BLUE, 28, pad=0.14)
    if kind == "mostly live":
        return bchip("mostly live", BLUE, 26, pad=0.12)
    return bchip("?", TEAL, 34, pad=0.22)


class Table:
    def __init__(self):
        self.frame = VGroup(Line([-6.2, 2.5, 0], [6.2, 2.5, 0], color=GREY, stroke_width=3),
                            Line([-0.45, 3.55, 0], [-0.45, -2.65, 0], color=GREY, stroke_width=2).set_opacity(0.6),
                            Line([2.9, 3.55, 0], [2.9, -2.65, 0], color=GREY, stroke_width=2).set_opacity(0.6))
        self.head = VGroup(T("genotype", 28, GREY).move_to([COLX[0] - 0.4, 3.05, 0]),
                           T("cells that\nnormally die", 26, GREY).move_to([COLX[1] - 0.2, 3.05, 0]),
                           T("cells that\nnormally live", 26, GREY).move_to([COLX[2] - 0.05, 3.05, 0]))
        self.rows = {}

    def row(self, key, idx, question=False, final=False):
        label, a, b = ROWS[key]
        if final:  # the answer to the double-mutant row
            a = b = "few die"
        y = ROWY[idx]
        lab = gtext(label, 28).move_to([0, y, 0])
        lab.set_x(LABX + lab.width / 2)
        assert lab.get_right()[0] < -0.55, (label, lab.width)
        v2 = vchip("?" if question else a).move_to([COLX[1] - 0.2, y, 0])
        v3 = vchip("?" if question else b).move_to([COLX[2] - 0.05, y, 0])
        g = VGroup(lab, v2, v3)
        g.label, g.v2, g.v3, g.y = lab, v2, v3, y
        self.rows[key] = g
        return g

    def static(self, keys, question_last=False, final_last=False):
        out = []
        for i, k in enumerate(keys):
            last = i == len(keys) - 1
            out.append(self.row(k, i, question=(question_last and last), final=(final_last and last)))
        return out


BASE4 = ["wt", "loss34", "gain9", "loss9"]


def question_text():
    return T("Do the extra deaths still happen?", 38, TEXT).move_to([0, -3.3, 0])


def egg(color=BLUE, s=1.0):
    return Ellipse(width=1.3 * s, height=1.7 * s, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.3)


# ---------------------------------------------------------------------------------------------
# pathway diagram (scenes 22 to 28): CED-9 left, one "killers" box right, EGL-1 above CED-9
# ---------------------------------------------------------------------------------------------
C9 = np.array([-3.0, -0.55, 0.0])
KB = np.array([3.6, -0.55, 0.0])      # centre of the killers box
EGL_Y = 2.35


def c9_chip():
    return bchip("CED-9", GREEN, 60).move_to(C9)


def killers_group():
    """one red box, label 'killers', CED-4 and CED-3 stacked (no left-to-right ranking)"""
    box = RoundedRectangle(corner_radius=0.2, width=4.2, height=3.8, stroke_color=RED, stroke_width=4,
                           fill_color=RED, fill_opacity=0.10).move_to(KB)
    lab = T("killers", 36, RED, weight=BOLD).move_to(KB + [0, 1.4, 0])
    k4 = bchip("CED-4", PURPLE, 52).move_to(KB + [0, 0.45, 0])
    k3 = bchip("CED-3", RED, 52).move_to(KB + [0, -0.9, 0])
    g = VGroup(box, lab, k4, k3)
    g.box, g.lab, g.k4, g.k3 = box, lab, k4, k3
    return g


def brake_bar():
    return inhib(C9 + RIGHT * 1.75, KB + LEFT * 2.15, GREEN, 10)


def egl_chip(size=54):
    return bchip("EGL-1", ORANGE, size).move_to([C9[0], EGL_Y, 0])


def egl_bar():
    """EGL-1 (orange) inhibits CED-9: a short bar from the EGL-1 chip down onto CED-9"""
    return inhib([C9[0], EGL_Y - 0.55, 0], [C9[0], C9[1] + 0.62, 0], ORANGE, 8)


def egl1_shape(width, seg_w, tsize, h, seg_off, name_off, seg_text=None):
    """EGL-1 as one short protein bar; the BH3 domain is a small in-line segment of the bar (not a plug)."""
    body = RoundedRectangle(corner_radius=0.16, width=width, height=h, stroke_color=ORANGE, stroke_width=4,
                            fill_color=ORANGE, fill_opacity=0.2)
    seg = Rectangle(width=seg_w, height=h - 0.02, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                    fill_opacity=0.95).move_to(body.get_center() + RIGHT * seg_off)
    name = T("EGL-1", tsize, ORANGE, weight=BOLD).move_to(body.get_center() + RIGHT * name_off)
    parts = [body, name, seg]
    if seg_text:
        parts.append(T(seg_text, 26, BG, weight=BOLD).move_to(seg))
    g = VGroup(*parts)
    g.body, g.name, g.seg = body, name, seg
    return g


# =============================================================================================
# scenes
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "The Death Machinery in Neurons"
    TITLE = "Cells Marked with an X"


# ---------------------------------------------------------------------------------------------
class S01(KS):
    """The puzzle: a death, and genes and proteins we cannot name."""

    def construct(self):
        title = T("Cells Marked with an X", 46, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        q = fit(T("How do you find the genes for a death?", 50, TEAL), max_w=12.8).move_to([0, 2.05, 0])
        cell = Circle(1.8, stroke_color=GREY, stroke_width=6, fill_color=GREY, fill_opacity=0.25).move_to([-4.3, -0.75, 0])
        x = xmark(cell.get_center(), 1.05, RED, 15)
        dcap = T("a death", 36, GREY).move_to([-4.3, -3.1, 0])
        genes = VGroup(*[bchip("gene ?", TEAL, 38) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to([2.5, 0.45, 0])
        prots = VGroup(*[VGroup(Circle(0.72, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.18),
                                T("?", 48, TEAL, weight=BOLD)) for _ in range(3)]).arrange(RIGHT, buff=0.8)
        for p in prots:
            p[1].move_to(p[0])
        prots.move_to([2.5, -1.35, 0])
        plab = T("which proteins?", 34, TEAL).move_to([2.5, -3.1, 0])

        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(q), FadeIn(cell), Create(x), run_time=0.8)
        self.at("the genes")
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in genes], lag_ratio=0.25), run_time=0.8)
        self.at("death")
        self.play(FadeIn(dcap), Indicate(cell, color=RED, scale_factor=1.06), run_time=0.5)
        self.at("do not know")
        self.play(LaggedStart(*[GrowFromCenter(p) for p in prots], lag_ratio=0.2), run_time=0.6)
        self.at("which proteins")
        self.play(FadeIn(plab), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(KS):
    """A transparent worm, 1 mm long."""

    def construct(self):
        body = worm_body(WG, BLUE, 0.9)
        gut = worm_gut(WG)
        name = T("C. elegans", 52, TEXT, slant=ITALIC).move_to([0, 3.2, 0])
        L = worm_len(WG)
        y = -2.3
        bar = VGroup(Line([-L / 2, y, 0], [L / 2, y, 0], color=TEXT, stroke_width=6),
                     Line([-L / 2, y - 0.2, 0], [-L / 2, y + 0.2, 0], color=TEXT, stroke_width=6),
                     Line([L / 2, y - 0.2, 0], [L / 2, y + 0.2, 0], color=TEXT, stroke_width=6))
        mm = M("1 mm", 42, TEXT, weight=BOLD).move_to([0, y - 0.6, 0])
        clear = T("transparent", 42, TEXT, weight=BOLD).move_to([0, -3.5, 0])
        self.add(gut)
        self.play(FadeIn(body, shift=UP * 0.15), run_time=0.8)
        self.at("elegans")
        self.play(FadeIn(name), run_time=0.5)
        self.at("millimeter")
        self.play(Create(bar), FadeIn(mm), run_time=0.8)
        self.at("transparent", lead=0.2)
        self.play(body.animate.set_fill(BLUE, 0.12).set_stroke(BLUE, 4), FadeIn(clear), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(KS):
    """Nomarski optics: nuclei stand out in relief, no stain."""

    def construct(self):
        body, gut = clear_worm()
        self.add(gut, body)
        c1 = bchip("Nomarski optics", GREY, 40).move_to([0, -3.1, 0])
        c2 = bchip("Nomarski optics, no stain", GREY, 40).move_to([0, -3.1, 0])
        nuclei = VGroup(*[dic_nuc(p, r=0.28, relief=True) for p in NUC_POS])
        VGroup(body, gut, nuclei).scale(1.1, about_point=ORIGIN)
        self.at("optics")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("nuclei")
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in nuclei], lag_ratio=0.06), run_time=1.4)
        self.at("living animal")
        self.play(Indicate(body, color=BLUE, scale_factor=1.02), run_time=0.7)
        self.at("without")
        self.play(ReplacementTransform(c1, c2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(KS):
    """Follow the cells as they divide; the full family tree grows from one large cell."""

    def construct(self):
        body, gut = clear_worm()
        nuclei = VGroup(*[dic_nuc(p) for p in NUC_POS])
        self.add(gut, body, nuclei)
        k = int(np.argmin([abs(p[0]) for p in NUC_POS]))
        ring = Circle(0.4, stroke_color=TEXT, stroke_width=6).move_to(NUC_POS[k])
        big = dic_nuc(NUC_POS[k])
        tree = Tree(full=True, **TR)
        top = np.array([TR["cx"], TR["ytop"] + 0.05, 0])
        label = T("family tree", 36, GREY).move_to([0, -3.5, 0])
        self.at("followed")
        self.play(Create(ring), run_time=0.5)
        self.at("cells")
        self.add(big)
        self.play(FadeOut(VGroup(body, gut, nuclei)),
                  VGroup(big, ring).animate.scale(1.5).move_to(top + DOWN * 0.1), run_time=0.7)
        self.at("divided")
        for L in range(3):
            extra = [FadeOut(VGroup(big, ring))] if L == 1 else []
            self.play(Create(tree.stages[L]), *extra, run_time=0.32)
        self.at("drew")
        for L in (3, 4):
            self.play(Create(tree.stages[L]), run_time=0.3)
        self.at("family tree")
        self.play(FadeIn(label), FadeIn(tree.dots, lag_ratio=0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(KS):
    """Some branches end in a death: the branch stops; then an X is drawn on each."""

    def construct(self):
        tree = Tree(full=True, **TR)
        label = T("family tree", 36, GREY).move_to([0, -3.5, 0])
        self.add(tree.lines, tree.dots, label)
        legend = VGroup(xmark([0, 0, 0], 0.26, RED, 8), T("= a death", 38, TEXT)).arrange(RIGHT, buff=0.25)
        legend.move_to([0, -3.5, 0])
        ids = list(DEATH_U)
        shorts = [tree.short_line(i, GREY) for i in ids]
        self.at("death")
        self.play(*[Transform(tree.leaf_line[i], s) for i, s in zip(ids, shorts)],
                  *[FadeOut(tree.dot_of[i]) for i in ids], FadeOut(label), run_time=0.7)
        self.at("each death")
        self.play(LaggedStart(*[Create(tree.x_of[i]) for i in ids], lag_ratio=0.25),
                  *[tree.leaf_line[i].animate.set_color(GREY) for i in ids],
                  FadeIn(legend, shift=UP * 0.1), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(KS):
    """Three animals, one tree: the Xs line up."""

    def construct(self):
        big = Tree(**TR)
        legend = VGroup(xmark([0, 0, 0], 0.26, RED, 8), T("= a death", 38, TEXT)).arrange(RIGHT, buff=0.25)
        legend.move_to([0, -3.5, 0])
        self.add(big.all(), legend)
        cxs = (-4.5, 0.0, 4.5)
        small = [Tree(cx=cx, **TR_SMALL) for cx in cxs]
        names = [T(f"animal {i + 1}", 40, TEXT).move_to([cx, 3.4, 0]) for i, cx in enumerate(cxs)]
        # Guides sit behind the trees; opaque branch back-strokes mask crossings.
        for t in small:
            t.lines.set_background_stroke(color=BG, width=9, opacity=1)
        # One dashed guide per X row, with generous gaps around the X marks.
        guides = VGroup()
        for i, u in DEATH_U.items():
            y = small[0].Y(u)
            xsx = sorted(t.lx[i] for t in small)
            edges = [-6.7] + [v for x in xsx for v in (x - 0.42, x + 0.42)] + [6.7]
            for a, b in zip(edges[0::2], edges[1::2]):
                if b - a > 0.3:
                    guides.add(DashedLine([a, y, 0], [b, y, 0], color=TEXT, stroke_width=3, dash_length=0.14
                                          ).set_opacity(0.4).set_z_index(-2))
        self.at("same identified")
        self.play(ReplacementTransform(big.all(), small[1].all()), FadeIn(names[1]), FadeOut(legend), run_time=0.9)
        self.at("every animal")
        self.add(small[0].all(), small[2].all())
        self.play(FadeIn(small[0].all(), shift=RIGHT * 0.5), FadeIn(small[2].all(), shift=LEFT * 0.5),
                  FadeIn(names[0]), FadeIn(names[2]), run_time=0.7)
        self.at("at the same place")
        self.play(Create(guides), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(KS):
    """131 of 1,090 somatic cells die."""

    def construct(self):
        small = [Tree(cx=cx, **TR_SMALL) for cx in (-4.5, 0.0, 4.5)]
        trees = VGroup(*[t.all() for t in small])
        self.add(trees)

        cols, n = 50, 1090
        pts = [[-5.88 + (i % cols) * 0.24, 2.15 - (i // cols) * 0.21, 0] for i in range(n)]
        rng = np.random.default_rng(11)
        dead_idx = sorted(rng.choice(n, 131, replace=False).tolist())
        dead_set = set(dead_idx)
        alive_pts = [p for i, p in enumerate(pts) if i not in dead_set]
        dead_pts = [p for i, p in enumerate(pts) if i in dead_set]
        assert len(pts) == 1090 and len(dead_pts) == 131 and len(alive_pts) == 959
        cloud_all = VGroup(*[Dot(p, radius=0.06, color=BLUE, stroke_width=0) for p in pts])
        cloud_dead = VGroup(*[Dot(p, radius=0.1, color=RED, stroke_width=0) for p in dead_pts])
        assert len(cloud_all) == 1090 and len(cloud_dead) == 131
        n131 = M("131", 72, RED, weight=BOLD)
        nof = T("of", 44, GREY)
        n1090 = M("1,090", 72, BLUE, weight=BOLD)
        sub = T("somatic cells", 40, GREY)
        top = VGroup(n131, nof, n1090, sub).arrange(RIGHT, buff=0.35).move_to([0, 3.2, 0])
        c1 = bchip("embryonic lineage", GREY, 28)
        plus = T("+", 40, TEXT)
        c2 = bchip("postembryonic lineage", GREY, 28)
        chips = VGroup(c1, plus, c2).arrange(RIGHT, buff=0.3).move_to([0, -2.9, 0])
        herm = T("hermaphrodite", 28, GREY).move_to([0, -3.6, 0])

        # Clear every X before the dot grid appears; the headline carries the transition.
        self.play(FadeOut(trees), FadeIn(top, shift=DOWN * 0.1), run_time=0.25)
        self.play(FadeIn(cloud_all), run_time=0.35)
        self.at("both lineages")
        self.play(FadeIn(chips, shift=UP * 0.1), run_time=0.5)
        self.at("131")
        self.play(FadeIn(cloud_dead), Indicate(n131, color=RED, scale_factor=1.15), run_time=0.7)
        self.at("hermaphrodite's", lead=0.0)
        self.play(FadeIn(herm), run_time=0.4)
        self.at("1 090")
        self.play(Indicate(n1090, color=BLUE, scale_factor=1.12), run_time=0.6)
        self.at("somatic cells")
        self.play(Indicate(sub, color=TEXT, scale_factor=1.08), run_time=0.5)
        self.at("die")
        self.play(*[Indicate(d, color=TEXT, scale_factor=1.9) for d in cloud_dead], run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08(KS):
    """One X, a named cell, on schedule: a phenotype, and one that can be screened for."""

    def construct(self):
        tree = Tree(**TR)
        self.add(tree.all())
        i = 14
        p = tree.tip(i, "x")
        ring = Circle(0.42, stroke_color=TEXT, stroke_width=6).move_to(p)
        others = VGroup(tree.lines, tree.dots, *[x for j, x in tree.x_of.items() if j != i])
        named = bchip("a named cell", GREY, 32).move_to([p[0], -3.1, 0])
        pointer = Line(p + DOWN * 0.42, named.get_top(), color=TEXT, stroke_width=4)
        sched = VGroup(clock([0, 0, 0]), T("on schedule:\nsame time in every animal", 36, TEXT, line_spacing=0.8)).arrange(RIGHT, buff=0.3)
        sched.move_to([-1.6, -3.1, 0])
        sched.shift([-(sched.get_right()[0] - (named.get_left()[0] - 0.3)), 0, 0])
        pheno = bchip("a phenotype", RED, 40).move_to([-4.7, 3.0, 0])
        mag = magnifier(p)
        scr = cap("a phenotype can be screened for", TEXT, 36)

        self.at("death")
        self.play(others.animate.set_opacity(0.75), Create(ring), run_time=0.6)
        self.at("named cell")
        self.play(FadeIn(named), Create(pointer), run_time=0.5)
        self.at("on schedule")
        self.play(FadeIn(sched, shift=UP * 0.1), run_time=0.6)
        self.at("phenotype")
        self.play(FadeIn(pheno, shift=UP * 0.2), run_time=0.5)
        self.at("can be screened")
        self.play(FadeOut(VGroup(named, pointer, sched)), others.animate.set_opacity(1.0), FadeOut(ring),
                  FadeIn(mag), FadeIn(scr), run_time=0.5)
        for j in (9, 6, 1):
            self.play(mag.animate.shift(tree.tip(j, "x") - mag[0].get_center()), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09(KS):
    """ced-1: corpses are not engulfed, so they stay visible."""

    def construct(self):
        body, gut = clear_worm()
        nuclei = VGroup(*[dic_nuc(p) for p in NUC_POS])
        self.add(gut, body, nuclei)
        top = bchip("Horvitz laboratory", GREY, 34).move_to([0, 3.2, 0])
        c1 = bchip("ced-1", GOLD, 50).move_to([-4.9, -2.25, 0])
        corpses = VGroup(*[corpse(p) for p in COR_POS])
        C = np.array([4.9, -2.3, 0])
        inset = Circle(1.5, stroke_color=GREY, stroke_width=4).move_to(C)
        neigh = Circle(0.5, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to(C + [-0.8, 0, 0])
        cor = corpse(C + [0.78, 0, 0], 0.3)
        ax = DashedLine(C + [-0.28, 0, 0], C + [0.4, 0, 0], color=GREY, stroke_width=5)
        cross = xmark(C + [0.06, 0, 0], 0.22, RED, 8)
        ne = bchip("not engulfed", RED, 34).move_to([1.5, -2.45, 0])
        vis = cap("corpses stay visible", TEXT, 40, y=-3.45).shift([-2.2, 0, 0])

        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.5)
        self.at("mutant called")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("corpses")
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in corpses], lag_ratio=0.1), run_time=0.6)
        self.at("not engulfed")
        self.play(FadeIn(inset), FadeIn(neigh), FadeIn(cor), run_time=0.4)
        self.play(Create(ax), Create(cross), FadeIn(ne), run_time=0.4)
        self.at("stay visible")
        self.play(FadeIn(vis, shift=UP * 0.15), Indicate(corpses, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(KS):
    """A screen: nine worms, one with no corpses."""

    def construct(self):
        rng = np.random.default_rng(5)
        xs, ys = (-4.5, 0.0, 4.5), (2.35, 0.15, -2.05)
        worms, empty = [], None
        for r, y in enumerate(ys):
            for c, x in enumerate(xs):
                g = worm_geom(x - 2.0, x + 2.0, y, 0.18, 1.25, 0.4, phase=rng.uniform(0, 3), n=80)
                b = worm_body(g, BLUE, 0.3, 3)
                no = (r == 2 and c == 1)
                dots = [] if no else [corpse(worm_pt(g, t, rng.uniform(-0.4, 0.4)), 0.13) for t in (0.28, 0.5, 0.72)]
                grp = VGroup(b, *dots)
                worms.append(grp)
                if no:
                    empty = grp
        allw = VGroup(*worms)
        title = bchip("a screen for new mutations", GREY, 32).move_to([0, 3.5, 0])
        scan = Rectangle(width=13.2, height=1.6, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.06)
        scan.move_to([0, ys[0], 0])
        ring = SurroundingRectangle(empty, color=TEXT, buff=0.18, corner_radius=0.2, stroke_width=6)
        tag = bchip("no corpses", TEXT, 34).move_to([0, -3.35, 0])

        self.play(LaggedStart(*[FadeIn(w) for w in allw], lag_ratio=0.04), FadeIn(title), run_time=0.4)
        self.at("searched")
        self.play(FadeIn(scan), run_time=0.2)
        self.play(scan.animate.move_to([0, ys[1], 0]), run_time=0.6)
        self.play(scan.animate.move_to([0, ys[2], 0]), run_time=0.6)
        self.at("never")
        self.play(ReplacementTransform(scan, ring), run_time=0.4)
        self.at("appeared")
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11(KS):
    """1986: ced-3 and ced-4."""

    def construct(self):
        year = M("1986", 130, TEXT, weight=BOLD).move_to([0, 2.4, 0])
        credit = T("Horvitz laboratory reports", 40, GREY).move_to([0, 0.8, 0])
        slots = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.2, height=1.8, stroke_color=TEAL, stroke_width=5,
                                          fill_color=TEAL, fill_opacity=0.08) for _ in range(2)])
        slots.arrange(RIGHT, buff=1.0).move_to([0, -1.75, 0])
        qs = VGroup(*[T("gene ?", 44, TEAL).move_to(s) for s in slots])
        g3 = bchip("ced-3", RED, 72).move_to(slots[0])
        g4 = bchip("ced-4", PURPLE, 72).move_to(slots[1])
        self.at("1986")
        self.play(FadeIn(year, shift=DOWN * 0.2), run_time=0.6)
        self.at("reported")
        self.play(FadeIn(credit), run_time=0.3)
        self.at("two genes")
        self.play(FadeIn(slots), FadeIn(qs), run_time=0.7)
        self.at("said 3")
        self.play(FadeOut(slots[0]), FadeOut(qs[0]), GrowFromCenter(g3), run_time=0.4)
        self.at("said 4")
        self.play(FadeOut(slots[1]), FadeOut(qs[1]), GrowFromCenter(g4), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12(KS):
    """Strong mutants: the X cells live and some grow neurites."""

    def construct(self):
        tree = Tree(**TR)
        self.add(tree.all())
        cap_t = T("strong mutants of", 30, GREY).move_to([4.85, 3.5, 0])
        g3 = bchip("ced-3", RED, 30)
        g4 = bchip("ced-4", PURPLE, 30)
        pair = VGroup(g3, g4).arrange(RIGHT, buff=0.2).move_to([4.85, 2.8, 0])
        surv = {i: tree.survive(i) for i in DEATH_U}
        nA, nB = neuron(tree.tip(1, "dot")), neuron(tree.tip(14, "dot"))
        feat = T("features of neurons", 36, BLUE).move_to([0, -3.3, 0])
        self.at("strong mutants")
        self.play(FadeIn(pair, shift=LEFT * 0.2), FadeIn(cap_t), run_time=0.6)
        self.at("should have died")
        self.play(*[Indicate(x, color=RED, scale_factor=1.7) for x in tree.xs], run_time=0.7)
        self.at("lived")
        self.play(FadeOut(tree.xs), *[Create(e) for e, _ in surv.values()], run_time=0.5)
        self.play(*[FadeIn(d, scale=0.3) for _, d in surv.values()], run_time=0.3)
        self.at("took on")
        self.play(*[Create(n[0]) for n in (nA, nB)], *[FadeIn(n[1]) for n in (nA, nB)], run_time=0.4)
        self.at("features")
        self.play(FadeIn(feat), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13(KS):
    """A third gene, ced-9, that works the other way."""

    def construct(self):
        c3 = bchip("ced-3", RED, 52).move_to([-5.0, 1.6, 0])
        c4 = bchip("ced-4", PURPLE, 52).move_to([-2.3, 1.6, 0])
        a1 = arr([-0.9, 1.6, 0], [2.6, 1.6, 0], RED, 6)
        k1 = T("kills", 38, RED).move_to([0.85, 2.15, 0])
        dead = VGroup(Circle(0.8, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.25),
                      xmark([0, 0, 0], 0.42, RED, 10)).move_to([4.1, 1.6, 0])
        dlab = T("cells die", 32, GREY).move_to([4.1, 0.45, 0])
        c9 = bchip("ced-9", GREEN, 66).move_to([-4.1, -1.6, 0])
        a2 = arr([-2.3, -1.6, 0], [2.6, -1.6, 0], GREEN, 6)
        k2 = T("protects", 38, GREEN).move_to([0.15, -1.05, 0])
        alive = Circle(0.8, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([4.1, -1.6, 0])
        alab = T("cells live", 32, BLUE).move_to([4.1, -2.75, 0])
        self.add(c3, c4, a1, k1, dead, dlab, c9)
        self.at("the other way")
        self.play(Create(a2), FadeIn(k2), FadeIn(alive), FadeIn(alab), run_time=0.8)
        self.at("called")
        self.play(Circumscribe(c9, color=GREEN, buff=0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14(KS):
    """Gain of function in ced-9: doomed cells live."""

    def construct(self):
        tree = Tree(**TR)
        self.add(tree.all())
        ttl = T("gain of function in", 30, GREY).move_to([4.85, 3.45, 0])
        c9 = bchip("ced-9", GREEN, 40).move_to([4.85, 2.75, 0])
        defn = cap("gain of function: the protein stays active", TEXT, 32)
        surv = {i: tree.survive(i) for i in DEATH_U}
        res = T("doomed cells\nsurvive", 34, BLUE).move_to([-4.85, 3.0, 0])
        self.at("gain")
        self.play(FadeIn(ttl), run_time=0.4)
        self.at("mutation")
        self.play(FadeIn(defn, shift=UP * 0.1), run_time=0.5)
        self.at("CED")
        self.play(FadeIn(c9, shift=DOWN * 0.1), run_time=0.4)
        self.at("kept doomed")
        self.play(FadeOut(tree.xs), *[Create(e) for e, _ in surv.values()], run_time=0.5)
        self.play(*[FadeIn(d, scale=0.3) for _, d in surv.values()], run_time=0.3)
        self.at("alive")
        self.play(FadeIn(res), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15(KS):
    """Loss of ced-9: extra deaths (ringed Xs); severe loss: embryos die."""

    def construct(self):
        tree = Tree(**TR)
        self.add(tree.all())
        loss = T("loss of", 30, GREY).move_to([4.85, 3.45, 0])
        c9 = bchip("ced-9", GREEN, 40).move_to([4.85, 2.75, 0])
        self.add(loss, c9)
        extra = [tree.extra_mark(i) for i in EXTRA]
        glyph = VGroup(Circle(0.3, stroke_color=RED, stroke_width=5), xmark([0, 0, 0], 0.15, RED, 6))
        elab = VGroup(glyph, T("extra deaths", 36, TEXT)).arrange(RIGHT, buff=0.3).move_to([0, -3.5, 0])
        sev = T("severe loss of", 30, GREY).move_to([4.85, 3.45, 0])
        e = egg(BLUE, 2.2).move_to([0, 0.2, 0])
        ex = xmark(e.get_center(), 0.8, RED, 14)
        edie = T("dies as an embryo", 40, TEXT).move_to([0, -2.4, 0])
        self.at("killed")
        self.play(*[FadeOut(tree.dot_of[i]) for i in EXTRA], LaggedStart(*[Create(x) for x in extra], lag_ratio=0.2),
                  FadeIn(elab, shift=UP * 0.1), run_time=1.0)
        self.at("severe")
        self.play(Transform(loss, sev), run_time=0.4)
        self.at("worms")
        self.play(FadeOut(tree.all()), FadeOut(VGroup(*extra)), FadeOut(elab), FadeIn(e, scale=0.6), run_time=0.45)
        self.at("die")
        self.play(e.animate.set_stroke(GREY).set_fill(GREY, 0.3), Create(ex), run_time=0.3)
        self.at("embryos")
        self.play(FadeIn(edie, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16(KS):
    """The genotype table builds, one row per genotype."""

    def construct(self):
        tb = Table()
        wt = tb.row("wt", 0)
        l34 = tb.row("loss34", 1)
        g9 = tb.row("gain9", 2)
        l9 = tb.row("loss9", 3)
        self.play(Create(tb.frame), FadeIn(tb.head), run_time=0.8)
        self.at("one genotype")
        self.play(FadeIn(wt.label), run_time=0.4)
        self.at("per row")
        self.play(FadeIn(wt.v2), FadeIn(wt.v3), run_time=0.4)
        self.at("losing")
        self.play(FadeIn(l34.label), run_time=0.5)
        self.at("saves doomed")
        self.play(FadeIn(l34.v2), FadeIn(l34.v3), run_time=0.3)
        self.play(Circumscribe(l34.v2, color=BLUE, buff=0.12, run_time=0.45))
        self.play(FadeIn(g9.label), FadeIn(g9.v2), FadeIn(g9.v3), run_time=0.5)
        self.at("losing", nth=1)
        self.play(FadeIn(l9.label), run_time=0.5)
        self.at("kills extra")
        self.play(FadeIn(l9.v2), FadeIn(l9.v3), run_time=0.4)
        self.play(Circumscribe(l9.v3, color=RED, buff=0.12, run_time=0.6))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17(KS):
    """A new row: ced-9 and ced-3 both removed. Do the extra deaths still happen?"""

    def construct(self):
        tb = Table()
        rows = tb.static(BASE4)
        self.add(tb.frame, tb.head, *rows)
        r5 = tb.row("loss93", 4, question=True)
        q = question_text()
        self.at("remove both")
        self.play(FadeIn(r5.label, shift=RIGHT * 0.2), run_time=0.6)
        self.at("said 3")
        self.play(GrowFromCenter(r5.v2), GrowFromCenter(r5.v3), run_time=0.4)
        self.at("Do the")
        self.play(FadeIn(q), run_time=0.3)
        self.at("extra deaths")
        self.play(Circumscribe(rows[3].v3, color=RED, buff=0.12, run_time=0.6))
        self.finish()


class S18Pause(NarratedScene):
    """5 s of silence: the question stays on screen."""

    def construct(self):
        tb = Table()
        rows = tb.static(BASE4 + ["loss93"], question_last=True)
        self.add(tb.frame, tb.head, *rows, question_text())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(KS):
    """No: few cells die, the embryos survive."""

    def construct(self):
        tb = Table()
        rows = tb.static(BASE4 + ["loss93"], question_last=True)
        q = question_text()
        self.add(tb.frame, tb.head, *rows, q)
        r5 = rows[4]
        a2, a3 = vchip("few die").move_to(r5.v2), vchip("few die").move_to(r5.v3)
        no = T("No.", 52, TEXT, weight=BOLD).move_to([-5.0, -3.3, 0])
        e = egg(BLUE, 0.6).move_to([-0.6, -3.25, 0])
        elab = T("embryos survive", 36, BLUE).next_to(e, RIGHT, buff=0.3)
        self.play(FadeOut(q), FadeIn(no), run_time=0.3)
        self.at("few cells")
        self.play(ReplacementTransform(r5.v2, a2), ReplacementTransform(r5.v3, a3), run_time=0.6)
        self.at("embryos")
        self.play(FadeIn(e, scale=0.5), FadeIn(elab), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20(KS):
    """The same with ced-4 instead of ced-3."""

    def construct(self):
        tb = Table()
        rows = tb.static(BASE4 + ["loss93"], final_last=True)
        self.add(tb.frame, tb.head, *rows)
        r6 = tb.row("loss94", 5)
        note = cap("same result", BLUE, 40, y=-3.3)
        self.at("instead")
        self.play(FadeIn(r6.label, shift=RIGHT * 0.2), run_time=0.5)
        self.at("same result")
        self.play(FadeIn(r6.v2), FadeIn(r6.v3), FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(r6.v2, color=BLUE, scale_factor=1.08),
                  Indicate(r6.v3, color=BLUE, scale_factor=1.08), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S21(KS):
    """The rule: if the killer cancels the loss of the brake, the brake works through the killer."""

    def construct(self):
        def card(text, y, col, size=40):
            t = T(text, size, TEXT, t2c={"killer": RED, "brake": GREEN}, line_spacing=0.9).move_to([0, y, 0])
            r = RoundedRectangle(corner_radius=0.22, width=max(t.width + 1.0, 5.0), height=t.height + 0.7,
                                 stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.1).move_to(t)
            return VGroup(r, t)
        c1 = card("remove the killer", 2.75, RED)
        c2 = card("cancels the effect of\nremoving the brake", 0.5, GREY)
        c3 = card("so the brake works through the killer", -1.75, GREEN, 38)
        a1 = arr([0, 2.1, 0], [0, 1.45, 0], GREY, 6)
        a2 = arr([0, -0.4, 0], [0, -0.95, 0], GREY, 6)
        ex = T("for example: removing ced-3 cancels the loss of ced-9", 32, GREY, t2c=GENECOL).move_to([0, -3.3, 0])
        self.at("removing the killer")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.6)
        self.at("cancels")
        self.play(GrowArrow(a1), FadeIn(c2, shift=DOWN * 0.2), run_time=0.7)
        self.at("works through")
        self.play(GrowArrow(a2), FadeIn(c3, shift=DOWN * 0.2), run_time=0.6)
        self.at("killer", nth=1)
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def axis_group():
    axis = arr([-6.3, 3.0, 0], [6.3, 3.0, 0], GREY, 6)
    alab = T("genetic order", 36, GREY).move_to([0, 3.5, 0])
    up = T("upstream", 32, GREEN).move_to([-5.1, 2.45, 0])
    down = T("downstream", 32, GREY).move_to([5.0, 2.45, 0])
    return axis, alab, up, down


class S22(KS):
    """Genetic order: CED-9 acts upstream, a brake on the two killers (one box, no left-to-right ranking)."""

    def construct(self):
        axis, alab, up, down = axis_group()
        c9 = c9_chip()
        bar = brake_bar()
        bl = T("brake", 40, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        kg = killers_group()
        self.at("genetic order")
        self.play(Create(axis), FadeIn(alab), run_time=0.7)
        self.at("CED")
        self.play(FadeIn(c9, shift=DOWN * 0.2), run_time=0.4)
        self.at("upstream")
        self.play(FadeIn(up), FadeIn(down), run_time=0.5)
        self.at("it is")
        self.play(Create(bar), FadeIn(bl), run_time=0.6)
        self.at("two killers")
        self.play(FadeIn(kg, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23(KS):
    """Caveat: genetic order is not contact.  The line is on screen for the whole scene."""

    def construct(self):
        axis, alab, up, down = axis_group()
        c9 = c9_chip()
        bar = brake_bar()
        bl = T("brake", 40, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        kg = killers_group()
        self.add(axis, alab, up, down, c9, bar, bl, kg)
        note = fit(T("Genetic order does not show which proteins touch.", 34, TEXT), max_w=12.4).move_to([0, -3.4, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.at("touch")
        self.play(Indicate(note, color=TEAL, scale_factor=1.04), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24(KS):
    """EGL-1, one more gene above the brake."""

    def construct(self):
        c9 = c9_chip()
        bar = brake_bar()
        bl = T("brake", 40, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        kg = killers_group()
        self.add(c9, bar, bl, kg)
        slot = RoundedRectangle(corner_radius=0.16, width=3.0, height=1.2, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.08).move_to([C9[0], EGL_Y, 0])
        q = T("gene ?", 38, TEAL).move_to(slot)
        e = egl_chip()
        eb = egl_bar()
        self.at("sits above")
        self.play(FadeIn(slot), FadeIn(q), run_time=0.6)
        self.at("called")
        self.play(FadeOut(slot), FadeOut(q), GrowFromCenter(e), run_time=0.5)
        self.play(Create(eb), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25(KS):
    """EGL-1: a short protein with one marked segment, the BH3 domain."""

    def construct(self):
        c9 = c9_chip()
        bar = brake_bar()
        bl = T("brake", 40, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        kg = killers_group()
        e = egl_chip()
        eb = egl_bar()
        fade = VGroup(c9, bar, bl, kg, eb)
        self.add(fade, e)
        shape = egl1_shape(10.5, 1.8, 76, 2.6, seg_off=3.0, name_off=-1.8).move_to([0, 0.8, 0])
        bh = T("BH3 domain", 56, ORANGE, weight=BOLD).move_to([shape.seg.get_center()[0], -1.75, 0])
        lead = Line(shape.seg.get_bottom() + DOWN * 0.05, bh.get_top() + UP * 0.1, color=ORANGE, stroke_width=4)
        self.play(FadeOut(fade), ReplacementTransform(e, VGroup(shape.body, shape.name)), run_time=1.0)
        self.at("a short")
        self.play(FadeIn(shape.seg, scale=0.5), run_time=0.7)
        self.at("BH3")
        self.play(Create(lead), FadeIn(bh, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S26(KS):
    """EGL-1 binds CED-9 (BH3 docks on it); the brake lifts off the killers, which brighten."""

    def construct(self):
        c9 = c9_chip()
        bar = brake_bar()
        kg = killers_group()
        e = egl1_shape(3.8, 1.1, 36, 0.95, seg_off=1.2, name_off=-0.7, seg_text="BH3")
        # Dock using the BH3 segment itself, rather than the whole group's bounds.
        e.shift([C9[0] - e.seg.get_x(), c9.get_top()[1] + 0.04 - e.seg.get_bottom()[1], 0])
        bl = T("brake", 40, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        diagram = VGroup(c9, bar, bl, kg, e).scale(1.1).move_to([0, 0, 0])
        dock = e.get_center().copy()
        e.shift(UP * 1.1)
        self.add(diagram)
        self.at("binds")
        self.play(e.animate.move_to(dock), run_time=0.7)
        self.play(e.seg.animate.set_stroke(TEXT, 4), run_time=0.2)
        self.at("releases")
        self.play(bar.animate.rotate(PI / 3.0, about_point=bar[0].get_start()).set_opacity(0.45),
                  kg.box.animate.set_stroke(opacity=1).set_fill(RED, 0.4),
                  kg.lab.animate.scale(1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S27(KS):
    """EGL-1 is needed for most somatic cell deaths."""

    def construct(self):
        tb = Table()
        rows = tb.static(BASE4 + ["loss93"], final_last=True)
        self.add(tb.frame, tb.head, *rows)
        # REVIEW FLAG: this narration-supported row is added; it is absent from the lesson table.
        r6 = tb.row("lossegl", 5)

        def card(head, body, col, x):
            tx = T(f"{head} {body}" if "\n" in body else f"{head}\n{body}", 28, TEXT, t2c={head: col}, line_spacing=0.8)
            bx = RoundedRectangle(corner_radius=0.2, width=tx.width + 0.5, height=tx.height + 0.3, stroke_color=col,
                                  stroke_width=3, fill_color=col, fill_opacity=0.1)
            g = VGroup(bx, tx.move_to(bx))
            return g.move_to([x, -3.27, 0])
        c1 = card("EGL-1:", "needed for\nmost somatic cell deaths", ORANGE, -3.0)
        c2 = card("without it,", "most doomed cells live", BLUE, 3.9)
        assert c1.width < 6.0 and c2.width < 5.2, (c1.width, c2.width)
        self.at("needed")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("Without")
        self.play(FadeIn(r6.label, shift=RIGHT * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.at("most doomed")
        self.play(FadeIn(r6.v2), FadeIn(r6.v3), run_time=0.4)
        self.play(Indicate(r6.v2, color=BLUE, scale_factor=1.08), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S28(KS):
    """The core worm pathway: one brake, held by CED-9, released by EGL-1."""

    def construct(self):
        ttl = T("the worm's core pathway", 36, GREY).move_to([0, 3.4, 0])
        c9 = c9_chip()
        bar = brake_bar()
        kg = killers_group()
        one = T("one brake", 34, GREEN).move_to([(bar[0].get_start()[0] + bar[0].get_end()[0]) / 2, C9[1] + 0.6, 0])
        e = egl_chip()
        eb = egl_bar()
        rel = T("releases", 34, ORANGE).next_to(eb, RIGHT, buff=0.25)
        diagram = VGroup(c9, bar, kg, one, e, eb, rel).scale(1.15).move_to([0, -0.05, 0])
        self.play(FadeIn(ttl), run_time=0.4)
        self.at("pathway")
        self.play(FadeIn(c9), FadeIn(kg), run_time=0.6)
        self.at("one")
        self.play(Create(bar), FadeIn(one), run_time=0.6)
        self.at("holds back")
        self.play(FadeIn(e, shift=DOWN * 0.2), Create(eb), FadeIn(rel),
                  Indicate(c9, color=GREEN, scale_factor=1.05), run_time=0.6)
        self.at("releases")
        self.play(kg.box.animate.set_fill(RED, 0.4), run_time=0.5)
        self.finish()


class S29End(EndCard):
    LINE = "One brake: CED-9 holds back the killers; EGL-1 releases it."
