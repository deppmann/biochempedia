"""Neuromuscular junction, chapter 3: Agrin protects, acetylcholine disperses (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept; same map as the whole series)
  BLUE   = acetylcholine receptors and their clusters (a cluster is drawn as a tight triad of blue dots)
  PURPLE = the motor neuron: axon and nerve terminal (and the enzyme ChAT inside it)
  YELLOW = agrin (the nerve's clustering signal)
  ORANGE = Lrp4 (the agrin receptor on the muscle)
  GREEN  = MuSK and "protect / stays" (the shield, the wider-band arrow)
  RED    = acetylcholine, dispersal, "lost / not there"
  SALMON = the acetylcholine receptor chip in the pathway diagram (a protein chip, not a cluster)
  GREY   = muscle sheet and fibre, basal lamina, ghost outlines, labels
  GOLD   = highlight borders and the date tag (used sparingly)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F2A154"
SALMON = "#E8907F"
LIGHT = "#B8BEC9"       # brighter grey for hedges and small labels

NERVE, RECEPTOR, AGRIN, LRP4, MUSK, ACH = PURPLE, BLUE, YELLOW, ORANGE, GREEN, RED


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cluster(x, y, s=1.0, color=RECEPTOR):
    """A receptor cluster: a tight clump of three dots."""
    r, off = 0.10 * s, 0.17 * s
    pts = [(-off, -off * 0.6), (off, -off * 0.6), (0, off * 0.9)]
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x + a, y + b, 0])
                    for a, b in pts])


def ghost(x, y, s=1.0):
    """The faded outline of a cluster that is gone."""
    r, off = 0.10 * s, 0.17 * s
    pts = [(-off, -off * 0.6), (off, -off * 0.6), (0, off * 0.9)]
    return VGroup(*[Circle(radius=r, stroke_color=GREY, stroke_width=2, fill_opacity=0).set_stroke(opacity=0.7)
                    .move_to([x + a, y + b, 0]) for a, b in pts])


def nosign(x, y, r=0.3, color=RED, w=6):
    """A 'none' sign: ring with a slash, placed BESIDE the thing that is absent."""
    ring = Circle(radius=r, stroke_color=color, stroke_width=w, fill_opacity=0).move_to([x, y, 0])
    sl = Line([x - r * 0.7, y + r * 0.7, 0], [x + r * 0.7, y - r * 0.7, 0], color=color, stroke_width=w)
    return VGroup(ring, sl)


def arr(a, b, color=GREY, w=7, tip=0.28):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def sheet(w, h, corner=0.25):
    return RoundedRectangle(corner_radius=corner, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12)


def shield_arc(cx, cy, r, start, angle, w=10):
    return Arc(radius=r, start_angle=start, angle=angle, color=MUSK, stroke_width=w).move_arc_center_to([cx, cy, 0])


def dome(cx, cy, r, w=10):
    """The shield: an upper arc over a cluster whose centre is (cx, cy)."""
    return shield_arc(cx, cy, r, np.radians(20), np.radians(140), w)


def terminal(x=0.0, bulb_y=0.95, bw=2.8, bh=1.0, top=3.9):
    line = Line([x, top, 0], [x, bulb_y + bh / 2 - 0.1, 0], color=NERVE, stroke_width=14)
    bulb = Ellipse(width=bw, height=bh, stroke_color=NERVE, stroke_width=3, fill_color=NERVE,
                   fill_opacity=0.55).move_to([x, bulb_y, 0])
    return VGroup(line, bulb)


def fibre_bar(y=-1.8, h=3.0, w=13.0):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([0, y, 0])


def scatter(c, seed=3, spread=0.9):
    rng = np.random.RandomState(seed)
    return [d.animate.shift([rng.uniform(-spread, spread), rng.uniform(-spread * 0.6, spread * 0.6), 0]).set_opacity(0.0)
            for d in c]


def dot_positions(n, seed, sigma, xmax, y0, y1, mind=0.3):
    rng = np.random.RandomState(seed)
    pts = []
    guard = 0
    while len(pts) < n and guard < 5000:
        guard += 1
        x = float(np.clip(rng.normal(0, sigma), -xmax, xmax))
        y = float(rng.uniform(y0, y1))
        if all((x - a) ** 2 + (y - b) ** 2 > mind ** 2 for a, b in pts):
            pts.append((x, y))
    return pts


def ach_dot(x, y, r=0.1):
    return Circle(radius=r, stroke_width=0, fill_color=ACH, fill_opacity=0.95).move_to([x, y, 0])


def pause_ui(tx, ty, bx0, by, bw):
    """'Pause and predict' cue with a shrinking timer bar. Returns (text, track, bar)."""
    t = T("Pause and predict", 26, LIGHT).move_to([tx, ty, 0])
    track = Rectangle(width=bw, height=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.25)
    track.move_to([bx0 + bw / 2, by, 0])
    bar = Rectangle(width=bw, height=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
    bar.move_to([bx0 + bw / 2, by, 0])
    return t, track, bar


def run_timer(scene, bar, secs):
    scene.play(bar.animate(rate_func=linear, run_time=secs).stretch(0.001, 0, about_edge=LEFT))


# ---------------------------------------------------------------------------------------------
# diaphragm sheets (scenes 1-2): 12 early clusters in a central band; 3 survive at birth
# ---------------------------------------------------------------------------------------------
SURV = [1, 6, 10]
LOST = [i for i in range(12) if i not in SURV]
DW, DH = 5.6, 4.8


def dia_pts():
    rng = np.random.RandomState(3)
    out = []
    for u in np.linspace(-0.3, 0.3, 3):
        for v in np.linspace(-0.72, 0.72, 4):
            out.append((u + rng.uniform(-0.03, 0.03), v + rng.uniform(-0.04, 0.04)))
    return out


def dia_clusters(cx, cy, k, s, idx=None, ghosts=False):
    pts = dia_pts()
    sel = range(12) if idx is None else idx
    f = ghost if ghosts else cluster
    return [f(cx + pts[i][0] * DW * k / 2, cy + pts[i][1] * DH * k / 2, s) for i in sel]


def dia_band(cx, cy, k=1.0):
    return Rectangle(width=2.55 * k, height=4.15 * k, stroke_width=0, fill_color=BLUE, fill_opacity=0.09).move_to([cx, cy, 0])


DL, DR, DYC = (-3.6, -0.15), (3.6, -0.15), -0.15


def dia_labels():
    lt_l = T("early, no agrin", 30, GREY, t2c={"agrin": AGRIN}).move_to([DL[0], 2.78, 0])
    lt_r = T("at birth, no agrin", 30, GREY, t2c={"agrin": AGRIN}).move_to([DR[0], 2.78, 0])
    sb_l = T("diaphragm (schematic)", 24, LIGHT).move_to([DL[0], -3.0, 0])
    sb_r = T("diaphragm (schematic)", 24, LIGHT).move_to([DR[0], -3.0, 0])
    return lt_l, lt_r, sb_l, sb_r


class S00Title(TitleCard):
    LESSON = "Building the Neuromuscular Junction: Agrin, Lrp4 and MuSK"
    TITLE = "Agrin Protects, Acetylcholine Disperses"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """Two schematic diaphragms: the early band without agrin, then few small clusters at birth."""

    def construct(self):
        sl = sheet(DW, DH).move_to([*DL, 0])
        sr = sheet(DW, DH).move_to([*DR, 0])
        lt_l, lt_r, sb_l, sb_r = dia_labels()
        band_bg = dia_band(*DL)
        band = VGroup(*dia_clusters(*DL, 1.0, 1.3))
        surv = VGroup(*dia_clusters(*DR, 1.0, 1.0, idx=SURV))
        self.add(sl, sb_l)
        self.play(FadeIn(lt_l), run_time=0.4)
        self.at("builds its band")
        self.play(FadeIn(band_bg), LaggedStart(*[FadeIn(c, scale=0.4) for c in band], lag_ratio=0.07), run_time=0.9)
        self.at("mice lacking agrin")
        self.play(FadeIn(sr), FadeIn(lt_r), FadeIn(sb_r), run_time=0.6)
        self.at("end up")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in surv], lag_ratio=0.25), run_time=0.8)
        arrow = arr([-0.55, -1.2, 0], [0.55, -1.2, 0], GREY, w=6)
        q = T("?", 100, TEXT, weight=BOLD).move_to([0, -0.15, 0])
        self.at("so few clusters")
        self.play(GrowArrow(arrow), FadeIn(q, scale=1.4), run_time=0.5)
        self.play(Indicate(surv, color=RECEPTOR, scale_factor=1.2), run_time=0.7)
        self.finish()


class S02Remove(SpokenScene):
    """The at-birth diaphragm grows to fill the frame; faded outlines mark where early clusters were."""

    def construct(self):
        sl = sheet(DW, DH).move_to([*DL, 0])
        sr = sheet(DW, DH).move_to([*DR, 0])
        lt_l, lt_r, sb_l, sb_r = dia_labels()
        band_bg = dia_band(*DL)
        band = VGroup(*dia_clusters(*DL, 1.0, 1.3))
        surv = VGroup(*dia_clusters(*DR, 1.0, 1.0, idx=SURV))
        arrow = arr([-0.55, -1.2, 0], [0.55, -1.2, 0], GREY, w=6)
        q = T("?", 100, TEXT, weight=BOLD).move_to([0, -0.15, 0])
        self.add(sl, sr, lt_l, lt_r, sb_l, sb_r, band_bg, band, surv, arrow, q)
        k = 1.15
        C = np.array([0, -0.15, 0])
        right = VGroup(sr, surv)
        R = np.array([*DR, 0])
        rl2 = T("at birth, no agrin (schematic)", 30, GREY, t2c={"agrin": AGRIN}).move_to([0, 3.3, 0])
        self.play(FadeOut(VGroup(sl, lt_l, band_bg, band, arrow, q, lt_r, sb_l, sb_r)), FadeIn(rl2),
                  right.animate.scale(k, about_point=R).shift(C - R), run_time=0.9)
        gh = VGroup(*dia_clusters(0, -0.15, k, 1.3 * 1.0, idx=LOST, ghosts=True))
        gl = T("outlines: where the early clusters were", 26, LIGHT).move_to([0, -3.3, 0])
        self.at("removing the clusters")
        self.play(LaggedStart(*[FadeIn(g) for g in gh], lag_ratio=0.05), FadeIn(gl), run_time=0.75)
        self.at("the muscle made")
        self.play(Indicate(gh, color=GREY, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the fibre scenes (3-6): one terminal over a long fibre; the same geometry every time
# ---------------------------------------------------------------------------------------------
CL0 = (0.0, -1.7)                                          # the cluster under the terminal
DISTANT = [(-4.9, -1.9), (-2.7, -2.1), (2.8, -2.1), (4.9, -1.9)]
CS = 2.4                                                   # cluster glyph size in the fibre scenes


def fibreA():
    fib = fibre_bar()
    flab = T("muscle fibre", 22, GREY).move_to([-5.5, -3.62, 0])
    cls = [cluster(*CL0, CS)] + [cluster(x, y, CS) for x, y in DISTANT]
    term = terminal(0.0)
    tl = T("nerve terminal", 26, NERVE).move_to([-3.6, 0.95, 0])
    return fib, flab, cls, term, tl


def sig_box():
    lbl = T("second signal?", 30, GREY).move_to([4.3, 1.9, 0])
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=lbl.width + 0.5, height=0.95, stroke_color=GREY,
                                          stroke_width=3), num_dashes=44).move_to(lbl)
    link = DashedLine([1.45, 1.1, 0], [2.4, 1.7, 0], color=GREY, stroke_width=3, dash_length=0.12)
    return VGroup(box, lbl), link


class S03Q(SpokenScene):
    """A nerve terminal over the fibre, with an empty label: second signal?"""

    def construct(self):
        fib, flab, cls, term, tl = fibreA()
        box, link = sig_box()
        self.add(fib, flab, *cls)
        self.at("the nerve")
        self.play(Create(term[0]), run_time=0.35)
        self.play(FadeIn(term[1], scale=0.8), FadeIn(tl), run_time=0.3)
        self.at("removes clusters")
        self.play(Create(link), FadeIn(box, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S04Pause(NarratedScene):
    """The question held still, with a shrinking timer."""

    def construct(self):
        fib, flab, cls, term, tl = fibreA()
        box, link = sig_box()
        t, track, bar = pause_ui(-4.2, 3.4, -6.2, 2.95, 4.0)
        self.add(fib, flab, *cls, term, tl, link, box, t, track, bar)
        self.wait(0.3)
        run_timer(self, bar, 4.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# agrin patch and shield (shared look in scene 5)
# ---------------------------------------------------------------------------------------------
def patchA(x=0.0, y=-0.12, w=2.0, h=0.22):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_width=0, fill_color=AGRIN,
                            fill_opacity=0.95).move_to([x, y, 0])


class S05Ach(SpokenScene):
    """Agrin patch and shield first; then acetylcholine released everywhere; unprotected clusters fade."""

    def construct(self):
        fib, flab, cls, term, tl = fibreA()
        box, link = sig_box()
        self.add(fib, flab, *cls, term, tl, link, box)
        patch = patchA()
        shield = dome(CL0[0], CL0[1] - 0.05, 1.05)
        agl = T("agrin", 26, AGRIN).move_to([-2.1, -0.65, 0])
        agl_line = Line([-1.6, -0.55, 0], [-1.05, -0.2, 0], color=AGRIN, stroke_width=3)
        shl = T("shield", 26, MUSK).move_to([2.1, -0.65, 0])
        shl_line = Line([1.6, -0.55, 0], [0.95, -1.0, 0], color=MUSK, stroke_width=3)
        al = T("acetylcholine", 30, ACH).move_to([4.3, 1.9, 0])
        dots = [ach_dot(x, y) for x, y in dot_positions(26, 4, 2.8, 5.8, 0.1, 0.32, 0.3)]
        rng = np.random.RandomState(5)
        starts = [[rng.uniform(-0.8, 0.8), 0.52, 0] for _ in dots]
        dg = VGroup(*dots)
        finals = [d.get_center().copy() for d in dots]
        for d, s in zip(dots, starts):
            d.move_to(s)
        ul = [T("unprotected", 24, LIGHT).move_to([x, -3.0, 0]) for x, _ in DISTANT]
        self.at("second signal")
        self.play(Indicate(box, color=TEXT, scale_factor=1.06), run_time=0.6)
        self.wait(0.05)
        self.play(FadeIn(patch, shift=DOWN * 0.2), Create(shield), FadeIn(agl), FadeIn(agl_line), FadeIn(shl),
                  FadeIn(shl_line), run_time=0.8)
        self.at("Acetylcholine")
        self.play(FadeOut(box), FadeOut(link), FadeIn(al), run_time=0.5)
        self.at("released")
        self.play(FadeIn(dg, scale=0.5), run_time=0.25)
        self.play(*[d.animate.move_to(f) for d, f in zip(dots, finals)],
                  Succession(Wait(0.55), AnimationGroup(*[FadeIn(u, shift=UP * 0.1) for u in ul], run_time=0.5)),
                  run_time=1.3)
        self.at("disperses")
        anims = []
        for k, c in enumerate(cls[1:]):
            anims += scatter(c, seed=k + 3)
        self.play(*anims, FadeOut(VGroup(*ul)), run_time=1.1)
        pl = T("protected", 26, MUSK).move_to([0, -3.0, 0])
        self.at("agrin does not protect")
        self.play(FadeIn(pl), Indicate(shield, color=MUSK, scale_factor=1.08), Indicate(patch, color=AGRIN, scale_factor=1.1),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Chat(SpokenScene):
    """A motor neuron's terminal whose acetylcholine-making enzyme is missing."""

    def construct(self):
        fib = fibre_bar()
        flab = T("muscle fibre", 22, GREY).move_to([-5.5, -3.62, 0])
        term = terminal(0.0)
        top = T("mice lacking ChAT", 30, NERVE).move_to([-4.3, 3.35, 0])
        mn = T("motor neuron", 26, NERVE).move_to([2.2, 3.35, 0])
        self.add(fib, flab, term, top, mn)
        none_dots = VGroup(*[DashedVMobject(Circle(radius=0.12, stroke_color=ACH, stroke_width=3), num_dashes=10)
                             .move_to([-0.9 + 0.6 * i, 0.12 + (0.06 if i % 2 else -0.04), 0]) for i in range(4)])
        nl = T("no acetylcholine released", 26, ACH).move_to([4.3, 0.1, 0])
        chat = bchip("ChAT", NERVE, 28).move_to([3.3, 0.95, 0])
        lead = Line([1.42, 0.95, 0], [chat.get_left()[0] - 0.05, 0.95, 0], color=NERVE, stroke_width=3)
        enz = T("choline acetyltransferase", 24, NERVE).move_to([4.3, 1.7, 0])
        ns = nosign(chat.get_right()[0] + 0.55, 0.95, 0.3)
        self.play(Indicate(term[1], color=NERVE, scale_factor=1.06), run_time=0.7)
        self.at("no acetylcholine")
        self.play(LaggedStart(*[FadeIn(d) for d in none_dots], lag_ratio=0.15), FadeIn(nl), run_time=0.9)
        self.at("lack the enzyme")
        self.play(Create(lead), FadeIn(chat, scale=0.8), FadeIn(enz), run_time=0.6)
        self.at("that makes it")
        self.play(Create(ns), chat.animate.set_opacity(0.75), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# scenes 7-9: one terminal, one fibre, the same triad glyph; narrow band, then a wider band
# ---------------------------------------------------------------------------------------------
BS = 1.2
BROWS = [-1.0, -1.85, -2.7]
NARROW_X = [-0.55, 0.55]
WIDE_X = [x * s for x in (3.85, 2.75, 1.65, 0.55) for s in (-1, 1)]
WIDE_X = sorted(WIDE_X)


def band_clusters(xs):
    return [cluster(x, y, BS) for x in xs for y in BROWS]


def band_base():
    fib = fibre_bar()
    flab = T("muscle fibre", 22, GREY).move_to([-5.5, -3.62, 0])
    term = terminal(0.0)
    top = T("mice lacking ChAT", 30, NERVE).move_to([-4.3, 3.35, 0])
    return fib, flab, term, top


def ghost_band():
    rect = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=2.3, height=2.5, stroke_color=LIGHT, stroke_width=3),
                          num_dashes=40).move_to([0, -1.85, 0])
    lab = T("normal band", 24, LIGHT).move_to([0, -3.62, 0])
    return rect, lab


def wide_arrow():
    da = DoubleArrow([-4.4, 0.1, 0], [4.4, 0.1, 0], color=GREEN, stroke_width=6, buff=0, tip_length=0.25)
    wl = T("wider band", 28, GREEN).move_to([5.75, 0.1, 0])
    return da, wl


class S07Inducer(SpokenScene):
    """Fibre from a mouse lacking ChAT: clusters under the terminal. Acetylcholine is not the inducer."""

    def construct(self):
        fib, flab, term, top = band_base()
        self.add(fib, flab, top)
        self.add(term)
        cl = band_clusters(NARROW_X)
        self.play(Indicate(term[1], color=NERVE, scale_factor=1.05), run_time=0.3)
        self.at("receptors still cluster")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cl], lag_ratio=0.12), run_time=1.0)
        self.at("under the nerve")
        self.play(Indicate(VGroup(*cl), color=RECEPTOR, scale_factor=1.15), run_time=0.8)
        lbl = T("acetylcholine: not the inducer", 32, ACH).move_to([0.8, -3.6, 0])
        self.at("not what starts clusters")
        self.play(FadeIn(lbl, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S08Wider(SpokenScene):
    """Same fibre, lacking ChAT: the normal narrow band as a ghost; more clusters over a wider band."""

    def construct(self):
        fib, flab, term, top = band_base()
        old = band_clusters(NARROW_X)
        lbl = T("acetylcholine: not the inducer", 32, ACH).move_to([0.8, -3.6, 0])
        self.add(fib, flab, top, term, *old, lbl)
        grect, glab = ghost_band()
        new_x = [x for x in WIDE_X if x not in NARROW_X]
        new = band_clusters(new_x)
        da, wl = wide_arrow()
        self.play(FadeOut(lbl), FadeIn(grect), FadeIn(glab), run_time=0.5)
        self.at("more clusters")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in new], lag_ratio=0.03), run_time=1.3)
        self.at("wider band")
        self.play(GrowFromCenter(da), FadeIn(wl), run_time=0.6)
        self.finish()


def wide_state():
    fib, flab, term, top = band_base()
    cl = band_clusters(WIDE_X)
    grect, glab = ghost_band()
    da, wl = wide_arrow()
    return [fib, flab, term, top, *cl, grect, glab, da, wl]


# ---------------------------------------------------------------------------------------------
# the 2 x 2 grid (scenes 9-15)
# ---------------------------------------------------------------------------------------------
XS = [-1.7, 3.9]
YS = [1.45, -1.75]
CW, CH = 5.4, 2.8
MS = 0.7                      # mini triad size
MROWS = [0.45, 0.0, -0.45]
MCOLS = {"narrow": [-0.29, 0.29], "early": [-0.87, -0.29, 0.29, 0.87],
         "wide": [x * s for x in (2.03, 1.45, 0.87, 0.29) for s in (-1, 1)]}
MCOLS["wide"] = sorted(MCOLS["wide"])


def cell_rect(c, r):
    return RoundedRectangle(corner_radius=0.12, width=CW, height=CH, stroke_color=GREY, stroke_width=2.5,
                            fill_opacity=0).move_to([XS[c], YS[r], 0])


def fib_c(c, r):
    return [XS[c], YS[r] + 0.3]


def mini_sheet(c, r):
    return sheet(4.8, 1.55, 0.15).move_to([*fib_c(c, r), 0])


def mini_cl(kind, c, r, s=MS, idx=None, ghosts=False):
    fx, fy = fib_c(c, r)
    pts = [(fx + x, fy + y) for x in MCOLS[kind] for y in MROWS]
    sel = range(len(pts)) if idx is None else idx
    f = ghost if ghosts else cluster
    return [f(pts[i][0], pts[i][1], s) for i in sel]


MSURV = [1, 6, 10]
MLOST = [i for i in range(12) if i not in MSURV]


def cap(text, c, r, color=TEXT, size=26):
    return T(text, size, color).move_to([XS[c], YS[r] - 0.95, 0])


def col_head(c):
    return T(["agrin present", "agrin absent"][c], 28, AGRIN).move_to([XS[c], 3.35, 0])


def row_head(r):
    return T(["acetylcholine\npresent", "acetylcholine\nabsent"][r], 24, ACH, line_spacing=0.8).move_to([-5.65, YS[r], 0])


def grid_shell():
    rects = VGroup(*[cell_rect(c, r) for r in (0, 1) for c in (0, 1)])
    heads = VGroup(col_head(0), col_head(1), row_head(0), row_head(1))
    return rects, heads


def prog_chip(c=1, r=1):
    return bchip("muscle's MuSK program", MUSK, 24, pad=0.12).move_to([XS[c], YS[r] - 0.95, 0])


def cell_fill(c, r, prog=False):
    """(objects, caption) for a filled cell, the final look used in every scene."""
    if (c, r) == (0, 0):
        return VGroup(mini_sheet(c, r), *mini_cl("narrow", c, r)), cap("narrow band", c, r)
    if (c, r) == (1, 0):
        return (VGroup(mini_sheet(c, r), *mini_cl("early", c, r, MS, MLOST, True), *mini_cl("early", c, r, 0.5, MSURV)),
                cap("most are lost", c, r, RED))
    if (c, r) == (0, 1):
        return VGroup(mini_sheet(c, r), *mini_cl("wide", c, r)), cap("more clusters, wider band", c, r)
    cp = prog_chip() if prog else cap("clusters return", c, r)
    return VGroup(mini_sheet(c, r), *mini_cl("wide", c, r)), cp


def grid_state(filled=(True, True, True, True), q=False, prog=False):
    rects, heads = grid_shell()
    parts = [rects, heads]
    for i, (c, r) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        if filled[i]:
            g, cp = cell_fill(c, r, prog)
            parts += [g, cp]
    qm = None
    if q:
        rects[3].set_stroke(GOLD, 6).set_fill(GOLD, 0.07)
        qm = T("?", 120, TEXT, weight=BOLD).move_to([XS[1], YS[1], 0])
        parts.append(qm)
    return parts, rects, heads, qm


class S09Grid(SpokenScene):
    """The empty 2 x 2 grid and its four headings; it starts drawing on the first word."""

    def construct(self):
        old = wide_state()
        self.add(*old)
        rects, heads = grid_shell()
        self.play(FadeOut(VGroup(*old)), LaggedStart(*[Create(r) for r in rects], lag_ratio=0.15), run_time=1.0)
        self.at("agrin present")
        self.play(FadeIn(heads[0], shift=DOWN * 0.15), run_time=0.4)
        self.at("or absent")
        self.play(FadeIn(heads[1], shift=DOWN * 0.15), run_time=0.4)
        self.at("acetylcholine present")
        self.play(FadeIn(heads[2], shift=RIGHT * 0.15), run_time=0.4)
        self.at("or absent", nth=1)
        self.play(FadeIn(heads[3], shift=RIGHT * 0.15), run_time=0.4)
        self.finish()


class S10Two(SpokenScene):
    """The two acetylcholine-present cells fill in."""

    def construct(self):
        rects, heads = grid_shell()
        self.add(rects, heads)
        sh0, cp0 = cell_fill(0, 0)
        self.at("Normal mice")
        self.play(FadeIn(sh0[0]), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in sh0[1:]], lag_ratio=0.15), run_time=0.9)
        self.at("narrow band")
        self.play(FadeIn(cp0), run_time=0.4)
        sheet1 = mini_sheet(1, 0)
        early = mini_cl("early", 1, 0, MS)
        self.at("early clusters")
        self.play(FadeIn(sheet1), LaggedStart(*[FadeIn(c, scale=0.4) for c in early], lag_ratio=0.06), run_time=0.9)
        capE = cap("early clusters form", 1, 0)
        self.play(FadeIn(capE), run_time=0.4)
        lost_g = mini_cl("early", 1, 0, MS, MLOST, True)
        small = mini_cl("early", 1, 0, 0.5, MSURV)
        capL = cap("most are lost", 1, 0, RED)
        self.at("most are lost")
        self.play(*[ReplacementTransform(early[i], g) for i, g in zip(MLOST, lost_g)],
                  *[ReplacementTransform(early[i], s) for i, s in zip(MSURV, small)],
                  FadeOut(capE), FadeIn(capL), run_time=1.0)
        self.finish()


class S11Three(SpokenScene):
    """The agrin-present, acetylcholine-absent cell fills in."""

    def construct(self):
        rects, heads = grid_shell()
        self.add(rects, heads)
        for c, r in [(0, 0), (1, 0)]:
            g, cp = cell_fill(c, r)
            self.add(g, cp)
        rect = rects[2]
        self.at("Without acetylcholine")
        self.play(rect.animate.set_stroke(GOLD, 6), Indicate(heads[3], color=ACH, scale_factor=1.12), run_time=0.7)
        g, cp = cell_fill(0, 1)
        self.at("more clusters")
        self.play(FadeIn(g[0]), LaggedStart(*[FadeIn(c, scale=0.4) for c in g[1:]], lag_ratio=0.04), run_time=1.0)
        self.at("wider band")
        self.play(FadeIn(cp), run_time=0.4)
        self.play(rect.animate.set_stroke(GREY, 2.5), run_time=0.4)
        self.finish()


class S12Q(SpokenScene):
    """Predict the last cell."""

    def construct(self):
        parts, rects, heads, _ = grid_state((True, True, True, False))
        self.add(*parts)
        qm = T("?", 120, TEXT, weight=BOLD).move_to([XS[1], YS[1], 0])
        self.at("last cell")
        self.play(rects[3].animate.set_stroke(GOLD, 6).set_fill(GOLD, 0.07), FadeIn(qm, scale=1.5), run_time=0.7)
        self.at("remove both")
        self.play(Indicate(heads[1], color=AGRIN, scale_factor=1.15), Indicate(heads[3], color=ACH, scale_factor=1.15),
                  run_time=0.8)
        self.at("what happens")
        self.play(Indicate(qm, color=GOLD, scale_factor=1.3), run_time=0.8)
        self.finish()


class S13Pause(NarratedScene):
    """The prediction held still, with a shrinking timer."""

    def construct(self):
        parts, *_ = grid_state((True, True, True, False), q=True)
        t, track, bar = pause_ui(-3.0, -3.55, -0.9, -3.55, 7.0)
        self.add(*parts, t, track, bar)
        self.wait(0.3)
        run_timer(self, bar, 4.4)
        self.finish()


class S14Return(SpokenScene):
    """The last cell fills in with clusters; the grid stays; a small date tag below."""

    def construct(self):
        parts, rects, heads, qm = grid_state((True, True, True, False), q=True)
        self.add(*parts)
        g, cp = cell_fill(1, 1)
        prog = prog_chip()
        self.at("Clusters return")
        self.play(FadeOut(qm), rects[3].animate.set_stroke(GREY, 2.5).set_fill(GOLD, 0.0), FadeIn(g[0]),
                  LaggedStart(*[FadeIn(c, scale=0.4) for c in g[1:]], lag_ratio=0.05), run_time=1.1)
        self.play(FadeIn(cp), run_time=0.3)
        self.at("built by the")
        self.play(FadeOut(cp), FadeIn(prog), run_time=0.5)
        self.play(Indicate(prog, color=MUSK, scale_factor=1.08), run_time=0.6)
        t1 = T("two mouse studies,", 28, GOLD)
        t2 = M("2005", 30, GOLD, weight=BOLD)
        tag = VGroup(t1, t2).arrange(RIGHT, buff=0.25).move_to([0, -3.55, 0])
        self.at("two mouse studies")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("in 2005")
        self.play(FadeIn(t2, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15Logic(SpokenScene):
    """The bottom row stays highlighted until the sentence is done; then agrin against acetylcholine."""

    def construct(self):
        parts, rects, heads, _ = grid_state(prog=True)
        t1 = T("two mouse studies,", 28, GOLD)
        t2 = M("2005", 30, GOLD, weight=BOLD)
        tag = VGroup(t1, t2).arrange(RIGHT, buff=0.25).move_to([0, -3.55, 0])
        grid = VGroup(*parts, tag)
        self.add(grid)
        hl = RoundedRectangle(corner_radius=0.15, width=13.5, height=3.0, stroke_color=GOLD, stroke_width=5,
                              fill_opacity=0).move_to([0, YS[1], 0])
        self.at("Without acetylcholine")
        self.play(Create(hl), run_time=0.8)
        self.at("without agrin")
        self.play(Indicate(heads[1], color=AGRIN, scale_factor=1.15), run_time=0.7)
        # agrin versus acetylcholine
        cl = cluster(0, -1.6, 5.4)
        sh = dome(0, -1.6, 2.5, 12)
        ag = bchip("agrin", AGRIN, 40).move_to([0, 3.1, 0])
        g_arrow = arr([0, 2.5, 0], [0, 1.1, 0], MUSK, w=16)
        gl = T("protects", 30, MUSK).move_to([1.6, 1.8, 0])
        ach = bchip("acetylcholine", ACH, 28).move_to([5.25, -0.9, 0])
        r_arrow = arr([3.65, -0.9, 0], [2.5, -0.9, 0], ACH, w=14)
        self.at("So a major")
        self.play(FadeOut(grid), FadeOut(hl), FadeIn(cl, scale=0.6), run_time=0.8)
        self.at("job of agrin")
        self.play(FadeIn(ag, shift=DOWN * 0.2), run_time=0.6)
        self.at("protect clusters")
        self.play(GrowArrow(g_arrow), FadeIn(gl), Create(sh), run_time=0.9)
        self.at("from acetylcholine")
        self.play(FadeIn(ach, shift=LEFT * 0.2), GrowArrow(r_arrow), run_time=0.8)
        self.play(Indicate(sh, color=MUSK, scale_factor=1.05), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# close-up of one junction (scenes 17-20)
# ---------------------------------------------------------------------------------------------
CC = (0.0, -2.5)                                       # central cluster (under the terminal)
CCS = 3.4
FAR = [(-5.6, -2.2), (-3.4, -2.6), (3.4, -2.6), (5.6, -2.2)]
FARS = 2.4


def closeup_base():
    fib = fibre_bar(-1.9, 3.2, 13.0)
    flab = T("muscle fibre", 22, GREY).move_to([-5.5, -3.65, 0])
    term = terminal(0.0, bulb_y=2.0, bw=5.0, bh=1.7, top=3.9)
    tl = T("nerve terminal", 26, NERVE).move_to([-4.6, 2.0, 0])
    cl = cluster(*CC, CCS)
    far = [cluster(x, y, FARS) for x, y in FAR]
    return fib, flab, term, tl, cl, far


CPOS = dot_positions(24, 11, 1.9, 3.8, 0.4, 1.0, 0.32)


def close_dots():
    return [ach_dot(x, y) for x, y in CPOS]


def lamina_patch():
    patch = RoundedRectangle(corner_radius=0.08, width=2.4, height=0.3, stroke_width=0, fill_color=AGRIN,
                             fill_opacity=0.95).move_to([0, 0.0, 0])
    lam = DashedLine([-6.4, 0.0, 0], [6.4, 0.0, 0], color=GREY, stroke_width=3, dash_length=0.18)
    laml = T("basal lamina", 24, LIGHT).move_to([-5.3, 0.37, 0])
    agl = T("agrin", 26, AGRIN).move_to([-2.1, -0.6, 0])
    return patch, lam, laml, agl


def close_shield():
    return dome(CC[0], CC[1] + 0.05, 1.6)


class S17Q(SpokenScene):
    """Zoom to one junction: the terminal releases acetylcholine onto the cluster below; why does it survive?"""

    def construct(self):
        fib, flab, term, tl, cl, far = closeup_base()
        self.add(fib, flab, cl, *far)
        dots = close_dots()
        dg = VGroup(*dots)
        al = T("acetylcholine", 26, ACH).move_to([5.3, 1.45, 0])
        rng = np.random.RandomState(12)
        finals = [d.get_center().copy() for d in dots]
        for d in dots:
            d.move_to([rng.uniform(-0.9, 0.9), 1.15, 0])
        q = T("?", 64, TEXT, weight=BOLD).move_to([0, -0.95, 0])
        self.play(Create(term[0]), FadeIn(q), run_time=0.5)
        self.play(FadeIn(term[1], scale=0.8), FadeIn(tl), run_time=0.4)
        self.at("cluster under")
        self.play(Indicate(cl, color=RECEPTOR, scale_factor=1.15), run_time=0.8)
        self.at("most acetylcholine")
        self.play(FadeIn(dg, scale=0.5), FadeIn(al), run_time=0.3)
        self.play(*[d.animate.move_to(f) for d, f in zip(dots, finals)], run_time=1.3)
        self.at("Why does it survive")
        self.play(Indicate(q, scale_factor=1.12), Indicate(cl, color=RECEPTOR, scale_factor=1.08), run_time=0.8)
        self.finish()


class S18Reach(SpokenScene):
    """Agrin as a fixed patch in the basal lamina; a shield over the cluster beneath."""

    def construct(self):
        fib, flab, term, tl, cl, far = closeup_base()
        dots = close_dots()
        al = T("acetylcholine", 26, ACH).move_to([5.3, 1.45, 0])
        self.add(fib, flab, term, tl, cl, *far, *dots, al)
        patch, lam, laml, agl = lamina_patch()
        ag = bchip("agrin", AGRIN, 28).move_to([-4.6, 1.1, 0])
        self.at("two forces")
        self.play(FadeIn(ag, shift=DOWN * 0.2), Indicate(al, color=ACH, scale_factor=1.1), run_time=0.7)
        self.at("differ in reach")
        self.play(Indicate(ag, color=AGRIN, scale_factor=1.12), Indicate(al, color=ACH, scale_factor=1.1), run_time=0.8)
        self.at("Agrin is anchored")
        self.play(ReplacementTransform(ag, patch), FadeIn(agl), run_time=0.8)
        self.at("basal lamina")
        self.play(Create(lam), FadeIn(laml), run_time=0.9)
        shield = close_shield()
        sl = T("protection", 24, MUSK).move_to([-3.0, -1.15, 0])
        self.at("its protection")
        self.play(Create(shield), FadeIn(sl), run_time=0.6)
        self.at("stays under")
        self.play(Indicate(shield, color=MUSK, scale_factor=1.06), Indicate(patch, color=AGRIN, scale_factor=1.1),
                  run_time=0.8)
        self.finish()


STRIP_X0, STRIP_W, STRIP_N = 1.65, 0.23, 21


def wave_strips():
    """Schematic dispersing effect along the fibre surface, fading with distance. Nearest first."""
    right, left = [], []
    for i in range(STRIP_N):
        x = STRIP_X0 + STRIP_W * i + STRIP_W / 2
        op = 0.30 * np.exp(-i / 14.0)
        for side, bucket in ((1, right), (-1, left)):
            bucket.append(Rectangle(width=STRIP_W, height=3.0, stroke_width=0, fill_color=ACH, fill_opacity=op)
                          .move_to([side * x, -1.9, 0]))
    return right, left


def spread_x(x):
    return float(np.clip(np.sign(x) * (abs(x) * 1.7 + 0.6), -6.3, 6.3))


def broad_end():
    """The state at the end of scene 19, rebuilt for scene 20."""
    fib, flab, term, tl, cl, far = closeup_base()
    patch, lam, laml, agl = lamina_patch()
    shield = close_shield()
    sl = T("protection", 24, MUSK).move_to([-3.0, -1.15, 0])
    rs, ls = wave_strips()
    dots = [ach_dot(spread_x(x), y) for x, y in CPOS]
    gh = [ghost(x, y, FARS) for x, y in FAR]
    title = T("dispersing effect (schematic)", 26, ACH).move_to([-4.0, 3.35, 0])
    return [fib, flab, term, tl, cl, patch, lam, shield, *rs, *ls, *dots, *gh, title]


class S19Broad(SpokenScene):
    """The dispersing effect spreads from the terminal along the fibre; distant clusters fade, the shielded one stays."""

    def construct(self):
        fib, flab, term, tl, cl, far = closeup_base()
        patch, lam, laml, agl = lamina_patch()
        shield = close_shield()
        sl = T("protection", 24, MUSK).move_to([-3.0, -1.15, 0])
        dots = close_dots()
        al = T("acetylcholine", 26, ACH).move_to([5.3, 1.45, 0])
        self.add(fib, flab, term, tl, cl, *far, patch, lam, laml, agl, shield, sl, *dots, al)
        rs, ls = wave_strips()
        title = T("dispersing effect (schematic)", 26, ACH).move_to([-4.0, 3.35, 0])
        spread = [d.animate.move_to([spread_x(d.get_center()[0]), d.get_center()[1], 0]) for d in dots]
        self.at("dispersing effect")
        self.play(FadeIn(title), FadeOut(al), FadeOut(agl), FadeOut(sl), FadeOut(laml), *spread, run_time=1.2)
        self.at("acetylcholine reaches")
        wave = Succession(*[AnimationGroup(FadeIn(r, rate_func=linear), FadeIn(l, rate_func=linear))
                            for r, l in zip(rs, ls)])
        dim = [c.animate(rate_func=linear).set_opacity(0.55) for c in far]
        self.play(wave, *dim, run_time=2.6)
        self.play(*[Indicate(c, color=ACH, scale_factor=1.12) for c in far], run_time=0.8)
        self.at("away from the terminal")
        self.play(Indicate(term[1], color=NERVE, scale_factor=1.04), run_time=0.7)
        gh = [ghost(x, y, FARS) for x, y in FAR]
        self.at("they lack")
        anims = []
        for k, c in enumerate(far):
            anims += scatter(c, seed=k + 20)
        self.play(*anims, *[FadeIn(g) for g in gh], run_time=0.8)
        self.at("strong protection")
        self.play(Indicate(shield, color=MUSK, scale_factor=1.06), Indicate(cl, color=RECEPTOR, scale_factor=1.12),
                  run_time=0.8)
        self.finish()


class S20Hedge(SpokenScene):
    """The wave front carries the hedge: mechanism not settled."""

    def construct(self):
        self.add(*broad_end())
        # Soft travelling halos avoid unexplained vertical bars at the fibre ends.
        glows = [Ellipse(width=1.4, height=3.0, stroke_width=0, fill_color=ACH,
                         fill_opacity=0.25).move_to([side * 1.9, -1.9, 0]) for side in (1, -1)]
        ml = T("mechanism\nnot settled", 28, TEXT, line_spacing=0.8).move_to([3.0, -0.85, 0])
        lead = DashedLine([3.0, -1.45, 0], [1.9, -1.85, 0], color=TEXT, stroke_width=3, dash_length=0.1)
        end_lead = DashedLine([4.9, -1.45, 0], [5.8, -1.85, 0], color=TEXT, stroke_width=3, dash_length=0.1)
        qr = T("?", 48, TEXT, weight=BOLD).move_to([6.1, -1.0, 0])
        ql = T("?", 48, TEXT, weight=BOLD).move_to([-6.1, -1.0, 0])
        self.at("How that effect")
        self.play(FadeIn(ml), Create(lead), *[FadeIn(g) for g in glows], run_time=0.3)
        self.play(glows[0].animate.move_to([5.8, -1.9, 0]),
                  glows[1].animate.move_to([-5.8, -1.9, 0]),
                  ml.animate.shift(RIGHT * 1.9), Transform(lead, end_lead), run_time=2.1, rate_func=linear)
        self.at("not fully settled")
        self.play(FadeIn(qr), FadeIn(ql), *[FadeOut(g) for g in glows], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the two pathways (scenes 21-22)
# ---------------------------------------------------------------------------------------------
BOXC = (0.0, -0.6)
YY = [2.8, 0.9, -1.0]
LX, RX = -5.0, 5.1


def dial_parts():
    d = {}
    d["fib"] = RoundedRectangle(corner_radius=0.25, width=3.8, height=3.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.12).move_to([*BOXC, 0])
    d["cl"] = cluster(BOXC[0], BOXC[1], 3.6)
    d["agrin"] = bchip("agrin", AGRIN, 28).move_to([LX, YY[0], 0])
    d["lrp"] = bchip("Lrp4", LRP4, 28).move_to([LX, YY[1], 0])
    d["musk"] = bchip("MuSK", MUSK, 28).move_to([LX, YY[2], 0])
    d["lrp_c"] = T("Lrp4:\nagrin receptor", 22, LIGHT, line_spacing=0.8).move_to([-3.3, YY[1], 0])
    d["ach"] = bchip("acetylcholine", ACH, 28).move_to([RX, YY[0], 0])
    d["rec"] = bchip("acetylcholine\nreceptor", SALMON, 24).move_to([RX, YY[1], 0])
    d["cdk"] = bchip("Cdk5\n(in mice)", ACH, 26).move_to([RX, YY[2], 0])
    d["a1"] = arr([LX, 2.35, 0], [LX, 1.35, 0], AGRIN, w=6, tip=0.22)
    d["a2"] = arr([LX, 0.5, 0], [LX, -0.55, 0], LRP4, w=6, tip=0.22)
    d["b1"] = arr([RX, 2.35, 0], [RX, 1.5, 0], ACH, w=6, tip=0.22)
    d["b2"] = DashedLine([RX, 0.35, 0], [RX, -0.45, 0], color=SALMON,
                             stroke_width=4, dash_length=0.12).add_tip(tip_length=0.18)
    d["cdk_name"] = T("Cdk5 link:\nin mice", 22, LIGHT, line_spacing=0.8).move_to([3.2, -2.05, 0])
    d["stay"] = arr([-4.15, YY[2], 0], [-1.98, YY[2], 0], MUSK, w=14)
    d["disp"] = arr([4.1, YY[2], 0], [1.98, YY[2], 0], ACH, w=14)
    d["stay_l"] = T("stays", 28, MUSK).move_to([-3.05, YY[2] + 0.5, 0])
    d["disp_l"] = T("disperses", 28, ACH).move_to([3.05, YY[2] + 0.5, 0])
    d["title"] = T("Does a cluster stay?", 36, TEXT).move_to([0, 3.15, 0])
    vm = VMobject().set_points_as_corners([[LX, -1.45, 0], [LX, -2.95, 0], [RX, -2.95, 0], [RX, -1.55, 0]])
    d["link"] = DashedVMobject(vm, num_dashes=70).set_stroke(GREY, 3)
    qm = T("?", 56, TEXT, weight=BOLD)
    qb = Rectangle(width=qm.width + 0.4, height=0.7, stroke_width=0, fill_color=BG, fill_opacity=1)
    d["q"] = VGroup(qb, qm).move_to([0, -2.95, 0])
    d["hedge"] = T("whether acetylcholine acts on MuSK itself is not settled", 24, LIGHT).move_to([0, -3.55, 0])
    return d


class S21Dial(SpokenScene):
    """Two pathways converge on one cluster."""

    def construct(self):
        d = dial_parts()
        self.add(d["fib"], d["cl"])
        self.at("two forces")
        self.play(FadeIn(d["agrin"], shift=DOWN * 0.15), FadeIn(d["ach"], shift=DOWN * 0.15), run_time=0.6)
        self.at("Does a cluster stay")
        self.play(FadeIn(d["title"], shift=DOWN * 0.15), run_time=0.5)
        self.at("agrin acting")
        self.play(GrowArrow(d["a1"]), FadeIn(d["lrp"]), FadeIn(d["lrp_c"]), run_time=0.5)
        self.at("through musk")
        self.play(GrowArrow(d["a2"]), FadeIn(d["musk"]), run_time=0.5)
        self.at("holds it")
        self.play(GrowArrow(d["stay"]), FadeIn(d["stay_l"]), run_time=0.6)
        self.at("Acetylcholine's pathway")
        self.play(GrowArrow(d["b1"]), FadeIn(d["rec"]), run_time=0.3)
        self.play(Create(d["b2"]), FadeIn(d["cdk"]), FadeIn(d["cdk_name"]), run_time=0.3)
        self.at("pulls it apart")
        self.play(GrowArrow(d["disp"]), FadeIn(d["disp_l"]), run_time=0.5)
        self.play(Create(d["link"]), FadeIn(d["q"]), FadeIn(d["hedge"], shift=UP * 0.1), run_time=0.7)
        self.finish()


KEYS_FULL = ["fib", "cl", "agrin", "lrp", "musk", "lrp_c", "ach", "rec", "cdk", "a1", "a2", "b1", "b2", "stay", "disp",
             "stay_l", "disp_l", "title", "link", "q", "hedge", "cdk_name"]


class S22Lrp4(SpokenScene):
    """Without agrin: Lrp4 gives MuSK a little activity; thin arrow, 'some activity'; then a few small clusters."""

    def construct(self):
        d = dial_parts()
        self.add(*[d[k] for k in KEYS_FULL])
        ns = nosign(LX - 1.35, YY[0], 0.3)
        thin_a2 = arr([LX, 0.5, 0], [LX, -0.55, 0], LRP4, w=3, tip=0.2)
        thin_stay = arr([-4.15, YY[2], 0], [-1.98, YY[2], 0], MUSK, w=4, tip=0.2)
        act = T("some activity", 28, "#A7E88D").move_to([-3.3, YY[2] - 0.5, 0])
        self.play(Create(ns), d["agrin"][1].animate.set_stroke(opacity=0.6).set_fill(opacity=0.08), d["agrin"][2].animate.set_opacity(0.7), FadeOut(d["a1"]), FadeOut(d["title"]),
                  FadeOut(d["link"]), FadeOut(d["q"]), FadeOut(d["hedge"]), run_time=0.7)
        self.at("LRP4")
        self.play(Indicate(d["lrp"], color=LRP4, scale_factor=1.12), run_time=0.7)
        self.at("give musk some activity")
        self.play(Transform(d["a2"], thin_a2), Transform(d["stay"], thin_stay), FadeIn(act),
                  d["stay_l"].animate.scale(0.85), d["cl"].animate.scale(0.5), run_time=0.7)
        small = VGroup(*[cluster(BOXC[0] + x, BOXC[1] + y, 1.5) for x, y in [(-0.7, 0.35), (0.1, -0.5), (0.75, 0.3)]])
        self.at("a few small clusters")
        self.play(FadeOut(d["cl"], scale=1.3), FadeIn(small, scale=0.5), run_time=0.8)
        self.play(Indicate(small, color=RECEPTOR, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Raise(SpokenScene):
    """Raise MuSK along the whole fibre in a mouse lacking agrin: the stays arrows grow; synapses appear."""

    def construct(self):
        fib = fibre_bar(-1.9, 3.2, 13.0)
        top = T("mice lacking agrin", 32, TEXT, t2c={"agrin": AGRIN}).move_to([0, 3.4, 0])
        self.add(fib, top)
        xs = np.linspace(-5.4, 5.4, 13)
        blocks = [RoundedRectangle(corner_radius=0.06, width=0.62, height=0.26, stroke_width=0, fill_color=MUSK,
                                   fill_opacity=0.9).move_to([x, -0.62, 0]) for x in xs]
        more = T("more MuSK,\nhigh expression", 26, MUSK, line_spacing=0.8).move_to([-4.65, 0.15, 0])
        SX = [-2.0, 2.0]
        thin = [arr([x, -0.92, 0], [x, -1.75, 0], MUSK, w=3, tip=0.2) for x in SX]
        big = [arr([x, -0.92, 0], [x, -1.75, 0], MUSK, w=16, tip=0.4) for x in SX]
        stl = [T("stays", 26, MUSK).move_to([x + (1.0 if x > 0 else -1.0), -1.3, 0]) for x in SX]
        cls = [cluster(x, -2.55, 2.6) for x in SX]
        terms = [terminal(x, bulb_y=0.55, bw=2.0, bh=0.9, top=2.6) for x in SX]
        tl = T("nerve terminal", 24, NERVE).move_to([4.7, 0.55, 0])
        sy = VGroup(*[T("synapse", 28, TEXT).move_to([x, -3.25, 0]) for x in SX])
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.03), FadeIn(more),
                  *[GrowArrow(a) for a in thin], run_time=1.0)
        self.at("enough another way")
        self.play(*[Transform(a, b) for a, b in zip(thin, big)], *[FadeIn(s) for s in stl], run_time=0.7)
        self.at("synapses can form")
        self.play(*[FadeIn(c, scale=0.5) for c in cls], *[Create(t[0]) for t in terms],
                  *[FadeIn(t[1], scale=0.8) for t in terms], FadeIn(tl), FadeIn(sy), run_time=1.0)
        self.at("lacking agrin")
        self.play(Indicate(top, color=AGRIN, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24Scope(SpokenScene):
    """Scope card, centred, then the one-line rule."""

    def construct(self):
        head = T("This rule is for", 32, GREY).move_to([0, 2.55, 0])
        c1 = bchip("receptor clusters", RECEPTOR, 46, pad=0.3).move_to([0, 1.3, 0])
        c2 = bchip("developing mouse muscle", GREY, 46, pad=0.3).move_to([0, -0.1, 0])
        rule = Line([-5.5, -1.15, 0], [5.5, -1.15, 0], color=GOLD, stroke_width=3)
        p = bchip("the muscle proposes", RECEPTOR, 36, pad=0.28).move_to([-3.2, -2.35, 0])
        n = bchip("the nerve disposes", NERVE, 36, pad=0.28).move_to([3.2, -2.35, 0])
        self.add(head)
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("receptor clusters")
        self.play(Indicate(c1, scale_factor=1.03), run_time=0.5)
        self.at("developing mouse muscle")
        self.play(Indicate(c2, scale_factor=1.03), run_time=0.5)
        self.play(GrowFromCenter(rule), run_time=0.4)
        self.at("the muscle proposes")
        self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.6)
        self.at("the nerve disposes")
        self.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S25Take(SpokenScene):
    """Closing card: agrin protects; acetylcholine disperses; the muscle proposes, the nerve disposes."""

    def construct(self):
        head = T("Takeaway", 32, GOLD).move_to([0, 3.45, 0])
        div = Line([0, 3.0, 0], [0, -2.2, 0], color=GREY, stroke_width=2)
        ag = bchip("agrin", AGRIN, 40).move_to([-3.4, 2.45, 0])
        ach = bchip("acetylcholine", ACH, 40).move_to([3.4, 2.45, 0])
        a1 = arr([-3.4, 1.95, 0], [-3.4, 1.2, 0], MUSK, w=12)
        a2 = arr([3.4, 1.95, 0], [3.4, 1.2, 0], ACH, w=12)
        lcl = cluster(-3.4, -0.75, 4.2)
        dm = dome(-3.4, -0.7, 1.75, 10)
        pl = T("protects", 30, MUSK).move_to([-5.45, 1.6, 0])
        rcl = VGroup(*[cluster(x, y, 2.6) for x, y in [(1.95, -0.1), (3.4, -1.2), (4.9, -0.3)]])
        dl = T("disperses", 30, ACH).move_to([5.2, 1.6, 0])
        foot = T("the muscle proposes; the nerve disposes", 34, TEXT, font=TITLE_FONT).move_to([0, -3.1, 0])
        self.add(head, ag, lcl, a1, pl, div)
        self.at("agrin protects")
        self.play(Create(dm), run_time=0.7)
        self.at("beneath it")
        self.play(Indicate(lcl, color=RECEPTOR, scale_factor=1.15), run_time=0.7)
        self.at("Acetylcholine")
        self.play(FadeIn(ach, shift=DOWN * 0.15), FadeIn(rcl, scale=0.6), GrowArrow(a2), FadeIn(dl), run_time=0.8)
        self.at("the rest")
        self.play(*[c.animate.set_opacity(0.3) for c in rcl], run_time=0.8)
        self.play(FadeIn(foot, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S25End(EndCard):
    LINE = "Agrin protects the clusters beneath it. Acetylcholine disperses the rest."
