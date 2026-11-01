"""Ras to MAPK: from membrane to genes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = growth factors (EGF, NGF): the signal outside the cell
  BLUE   = Ras, the GTP switch
  PINK   = SOS, the protein that loads Ras with GTP
  PURPLE = the kinases Raf, MEK, ERK
  GOLD   = a phosphate (the round "P" badge)
  GREEN  = on / active (the GTP tag, an active kinase's outline, ERK activity, the open window)
  RED    = feedback and stopping (feedback arrows, the phosphatase, the closing edge of a window)
  ORANGE = the cell's answer (a dividing cell, a cell with fibres)
  GREY   = membrane, outlines, labels, and parts not yet known

No molecular structures: Ras is a mouth on the membrane, Raf is a block with a lid that folds over it,
MEK and ERK are blocks with labelled site tabs, a phosphate is a "P" badge, DNA is a bar.

Original BASE/ZOOM helpers are retained. New scenes use close-ups and a shared overview.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"


# ---------------------------------------------------------------------------------------------
# framings: BASE coordinates are used to place everything; a View maps them to the screen
# ---------------------------------------------------------------------------------------------
class View:
    def __init__(self, k=1.0, ox=0.0, oy=0.0, sx=0.0, sy=0.0):
        self.k, self.ox, self.oy, self.sx, self.sy = k, ox, oy, sx, sy
        self.sw = 3 * k ** 0.5

    def p(self, x, y):
        return np.array([self.sx + self.k * (x - self.ox), self.sy + self.k * (y - self.oy), 0.0])


BASE = View(k=1.2)
ZOOM = View(k=2.0, ox=-5.1, oy=1.2, sx=-4.9, sy=0.0)

MEM_X = -5.1
RAS_X, RAS_Y, RAS_R = -4.1, 1.2, 0.9
RAFA = (-1.9, 1.2)
RAFB = (-1.9, 0.15)
SOS_XY = (-4.35, -0.12)
MEK_XY = (1.4, -1.0)
ERK_XY = (3.7, -2.2)
RAF_W, RAF_H, LID_W, LID_H = 1.9, 0.9, 0.7, 0.55
KIN_W, KIN_H = 1.7, 1.2


def ZP(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24, color=GREY):
    """a dashed chip: something that is not there, or not yet there."""
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(k=1.0):
    """a phosphate."""
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.35):
    """swell and settle, without recolouring (Indicate would hide the P on a badge)."""
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    """flash each mobject in place (one animation each: a new VGroup would re-add them on top)."""
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


def bez(a, c1, c2, b):
    return CubicBezier(np.array(a, float), np.array(c1, float), np.array(c2, float), np.array(b, float))


def tail_bar(curve_pts, color=RED, w=6, half=0.26):
    """the flat end of an inhibition arrow, across the direction of the last stretch."""
    a, b = np.array(curve_pts[0], float), np.array(curve_pts[1], float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return Line(b + perp * half, b - perp * half, color=color, stroke_width=w)


def fb_curve(a, c1, c2, b, color=RED, w=5):
    """a curved inhibition arrow: [curve, end bar]."""
    cv = bez(a, c1, c2, b)
    cv.set_stroke(color, w)
    return VGroup(cv, tail_bar((c2, b), color, w + 1))


def clock(center, r=0.45):
    center = np.array(center, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4).move_to(center)
    ticks = VGroup(*[Line(center + (r - 0.11) * v, center + r * v, color=GREY, stroke_width=4) for v in (UP, RIGHT, DOWN, LEFT)])
    hand = Line(center, center + UP * (r - 0.15), color=TEXT, stroke_width=5)
    pin = Dot(center, radius=0.05, color=TEXT)
    g = VGroup(face, ticks, hand, pin)
    g.hand, g.c = hand, center
    return g


def bracket(x, y0, y1, side=1, color=GREY, w=4, d=0.14):
    """a square bracket on a vertical span; side=+1 opens to the left (sits on the right)."""
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w),
                  Line([x, y0, 0], [x - side * d, y0, 0], color=color, stroke_width=w),
                  Line([x, y1, 0], [x - side * d, y1, 0], color=color, stroke_width=w))


# ---- the cell's answers (S01, S05, S06) ----
def cell_icon(c, r=0.5, color=ORANGE):
    c = np.array(c, float)
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15).move_to(c),
                  Dot(c, radius=r * 0.22, color=GREY))


def dividing_icon(c, r=0.5, color=ORANGE):
    """a cell that has split in two."""
    c = np.array(c, float)
    rr = r * 0.72
    return VGroup(cell_icon(c + LEFT * rr * 0.95, rr, color), cell_icon(c + RIGHT * rr * 0.95, rr, color))


def fibres_icon(c, r=0.5, length=0.75, color=ORANGE):
    """a cell with long fibres growing from it."""
    c = np.array(c, float)
    fib = VGroup()
    for a, wob in ((25, 1), (75, -1), (140, 1), (200, -1), (255, 1), (320, -1)):
        t = np.radians(a)
        u = np.array([np.cos(t), np.sin(t), 0])
        v = np.array([-np.sin(t), np.cos(t), 0])
        p0 = c + u * r
        p1 = c + u * (r + length * 0.5) + v * 0.1 * wob
        p2 = c + u * (r + length) - v * 0.06 * wob
        f = VMobject(stroke_color=color, stroke_width=4).set_points_smoothly([p0, p1, p2])
        fib.add(VGroup(f, Dot(p2, radius=0.06, color=color)))
    return VGroup(fib, cell_icon(c, r, color))


# ---------------------------------------------------------------------------------------------
# the parts of the chain
# ---------------------------------------------------------------------------------------------
def membrane(V):
    return RoundedRectangle(corner_radius=0.1, width=0.3 * V.k, height=6.9, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([V.p(MEM_X, 0)[0], 0, 0])


def pac_points(c, R, mouth_deg, n=72):
    a = np.radians(mouth_deg) / 2
    angs = np.linspace(a, TAU - a, n)
    return [c] + [c + R * np.array([np.cos(t), np.sin(t), 0]) for t in angs]


def ras_body(V, mouth, on):
    c, R = V.p(RAS_X, RAS_Y), RAS_R * V.k
    col = GREEN if on else BLUE
    return Polygon(*pac_points(c, R, mouth), stroke_color=col, stroke_width=V.sw + (1 if on else 0),
                   fill_color=BLUE, fill_opacity=0.32 if on else 0.16)


def ras(V, mouth=18, on=False):
    """Ras: a mouth on the membrane. Slack with GDP, open with GTP."""
    c, R = V.p(RAS_X, RAS_Y), RAS_R * V.k
    body = ras_body(V, mouth, on)
    lbl = T("Ras", 30 * V.k, BLUE, weight=BOLD).move_to(c + LEFT * 0.3 * R)
    g = VGroup(body, lbl)
    g.body, g.lbl = body, lbl
    return g


def nt_tag(V, text, color):
    """the nucleotide Ras is holding, on top of it."""
    return bchip(text, color, 22 * V.k, pad=0.14 * V.k).move_to(V.p(RAS_X, RAS_Y + RAS_R + 0.38))


def sos_chip(V):
    return bchip("SOS", PINK, 24 * V.k, pad=0.18 * V.k).move_to(V.p(*SOS_XY))


def raf(V, x, y, open_=False, active=False):
    """Raf: a block (the kinase) and a lid (its front half). Folded shut the lid lies over the block;
    open, it swings out to the left, where Ras can hold it. [body, lid[back, box], label]"""
    k = V.k
    c = V.p(x, y)
    col = GREEN if active else PURPLE
    body = RoundedRectangle(corner_radius=0.2 * k, width=RAF_W * k, height=RAF_H * k, stroke_color=col,
                            stroke_width=V.sw + (1.5 if active else 0), fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    H = V.p(x - RAF_W / 2, y)
    lc = H + (LEFT if open_ else RIGHT) * LID_W * k / 2
    back = RoundedRectangle(corner_radius=0.12 * k, width=LID_W * k, height=LID_H * k, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(lc)
    box = RoundedRectangle(corner_radius=0.12 * k, width=LID_W * k, height=LID_H * k, stroke_color=col, stroke_width=V.sw,
                           fill_color=PURPLE, fill_opacity=0.55).move_to(lc)
    lid = VGroup(back, box)
    lbl = T("Raf", 28 * k, PURPLE, weight=BOLD).move_to(c + RIGHT * 0.35 * k)
    g = VGroup(body, lid, lbl)
    g.body, g.lid, g.lbl, g.H = body, lid, lbl, H
    return g


def kinase(V, name, x, y, tabs, w=KIN_W, h=KIN_H):
    """MEK or ERK: a block with site tabs stacked on its left edge. [back, body, label, tab, tab]"""
    k = V.k
    c = V.p(x, y)
    back = RoundedRectangle(corner_radius=0.24 * k, width=w * k, height=h * k, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.24 * k, width=w * k, height=h * k, stroke_color=PURPLE, stroke_width=V.sw,
                            fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    lbl = T(name, 30 * k, PURPLE, weight=BOLD).move_to(c)
    th, gap = 0.46, 0.04
    n = len(tabs)
    y0 = y + (n * th + (n - 1) * gap) / 2 - th / 2
    tab_g, sites = [], []
    for i, t in enumerate(tabs):
        ty = y0 - i * (th + gap)
        tx = x - w / 2 - 0.33
        rect = Rectangle(width=0.66 * k, height=th * k, stroke_color=PURPLE, stroke_width=V.sw, fill_color=PURPLE,
                         fill_opacity=0.3).move_to(V.p(tx, ty))
        tab_g.append(VGroup(rect, T(t, 22 * k, PURPLE).move_to(V.p(tx, ty))))
        sites.append(V.p(x - w / 2 - 0.66 - 0.2, ty))
    g = VGroup(back, body, lbl, *tab_g)
    g.body, g.lbl, g.tabs, g.sites = body, lbl, tab_g, sites
    return g


def go_on(g, extra=()):
    """animations: this kinase is active (green outline)."""
    anims = [g.body.animate.set_stroke(GREEN, 4.5)]
    for t in extra:
        anims.append(t.animate.set_stroke(GREEN))
    return anims


def go_quiet(g):
    return [g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.12), g.lbl.animate.set_color(GREY)]


def raf_on(g):
    return [g.body.animate.set_stroke(GREEN, 4.5), g.lid[1].animate.set_stroke(GREEN)]


def raf_weak(g):
    return [g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.12), g.lid[1].animate.set_stroke(GREY).set_fill(GREY, 0.3),
            g.lbl.animate.set_color(GREY)]


def stage(V, ras_on=True, rafs_on=True):
    """the membrane, Ras (holding GTP), SOS and the Raf pair, as they stand at the end of scene 2."""
    mem = membrane(V)
    r = ras(V, 70, ras_on)
    tag = nt_tag(V, "GTP", GREEN)
    sos = sos_chip(V)
    a = raf(V, *RAFA, open_=True, active=rafs_on)
    b = raf(V, *RAFB, open_=True, active=rafs_on)
    return mem, r, tag, sos, a, b


def reframe(old, new):
    """morph each piece into the same piece of another framing."""
    return [Transform(a, b) for a, b in zip(old, new)]


X0, X_HR, X_END = -3.7, -0.7, 3.9
YT, YB, AMP = 0.55, -2.3, 1.9


def chain_on(V):
    """the whole chain, every part on: [mem, ras, tag, sos, rafA, rafB, mek, erk, P x4 (MEK sites, ERK sites)]"""
    mem, r, tag, sos, rA, rB = stage(V)
    mek = kinase(V, "MEK", *MEK_XY, tabs=("Ser", "Ser"))
    erk = kinase(V, "ERK", *ERK_XY, tabs=("Thr", "Tyr"))
    for g in (mek, erk):
        g.body.set_stroke(GREEN, 4.5)
    ps = [pbadge(V.k).move_to(s) for s in mek.sites + erk.sites]
    return mem, r, tag, sos, rA, rB, mek, erk, ps

def egf_curve(x0=X0, x1=X_HR, y0=YT, amp=AMP):
    """ERK activity after EGF: rises and falls back to nothing within about an hour (schematic)."""
    f = lambda t: (t / 0.15) * np.exp(1 - t / 0.15)
    return ParametricFunction(lambda t: np.array([x0 + (x1 - x0) * t, y0 + amp * f(t), 0]), t_range=[0, 1, 0.01],
                              color=GREEN, stroke_width=6)

def plateau_curve(x0=X0, x1=X_END, y0=YB, amp=AMP, color=GREEN, rise=0.12, run=2.6):
    """ERK activity after NGF: climbs to a plateau that lasts (schematic)."""
    f = lambda t: 1 - np.exp(-t / rise)
    return ParametricFunction(lambda t: np.array([x0 + (x1 - x0) * t / run, y0 + amp * f(t), 0]), t_range=[0, run, 0.01],
                              color=color, stroke_width=6)

def axes_row(x0, x1, y0, h):
    ya = Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3)
    xa = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3)
    return VGroup(ya, xa)

# The old drawing primitives above are retained; new layouts follow the new narration.
def label(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


def node(text, x, y, color=PURPLE, size=28):
    return bchip(text, color, size).move_to([x, y, 0])


def link(a, b, color=GREY):
    return arr(a.get_right(), b.get_left(), color, w=3)


def overview():
    # Five stations and two outputs; the arrows are part of each relay station.
    names = [('receptor', GREY), ('Ras–GTP', BLUE), ('Raf', PURPLE), ('MEK', PURPLE), ('ERK', PURPLE)]
    ns = [node(n, x, 1.25, c, 26) for (n, c), x in zip(names, [-5.1, -2.4, 0, 2.2, 4.5])]
    ls = [link(a, b) for a, b in zip(ns, ns[1:])]
    cyt = node('cytoplasmic proteins', 3.9, -0.5, ORANGE, 24)
    nuc = VGroup(node('transcription factors', 0.6, -2.0, PURPLE, 24), label('nucleus', 0.6, -1.25, GREY, 24))
    branches = VGroup(arr(ns[-1].get_bottom(), cyt.get_top(), PURPLE, w=3),
                      VGroup(VMobject(stroke_color=PURPLE, stroke_width=3).set_points_as_corners(
                          [[4.0, 1.1, 0], [1.8, 0.3, 0], [1.8, -1.1, 0]]),
                          arr([1.8, -1.1, 0], [1.4, -1.7, 0], PURPLE, w=3)))
    return ns, ls, cyt, nuc, branches


class S00Title(TitleCard):
    LESSON = 'Ras to MAPK: The Kinase Cascade'
    TITLE = 'Ras to MAPK: From Membrane to Genes'


class S01Puzzle(SpokenScene):
    def construct(self):
        ns, ls, cyt, nuc, branches = overview()
        mem = RoundedRectangle(width=0.26, height=2.5, corner_radius=0.1, color=GREY,
                               fill_color=GREY, fill_opacity=0.3).move_to([-5.1, 1.25, 0])
        gf = node('growth factor', -5.1, 3.1, YELLOW, 24)
        self.at('A growth factor')
        self.play(FadeIn(mem), FadeIn(ns[0]), FadeIn(gf), run_time=0.5)
        self.at('binds a receptor')
        self.play(gf.animate.move_to([-5.1, 2.35, 0]), ns[0][1].animate.set_stroke(GREEN), run_time=0.65)
        self.at('switches on')
        self.play(FadeIn(ns[1]), GrowArrow(ls[0]), run_time=0.6)
        self.at('three kinases')
        self.play(LaggedStart(*[AnimationGroup(FadeIn(n), GrowArrow(a)) for n, a in zip(ns[2:], ls[1:])], lag_ratio=0.5), run_time=1.4)
        self.at('acts on proteins')
        self.play(FadeIn(cyt), GrowArrow(branches[0]), run_time=0.6)
        self.at('transcription factors')
        self.play(FadeIn(nuc), Create(branches[1]), run_time=0.6)
        gene = node('genes', -3.4, -2.0, ORANGE, 26)
        ga = arr(nuc[0].get_left(), gene.get_right(), GREEN, w=3)
        response = label('cell response', 0, -3.2, ORANGE, 28)
        self.at('That changes gene expression')
        self.play(FadeIn(gene), GrowArrow(ga), FadeIn(response), run_time=0.75)
        self.at('This is how')
        self.play(LaggedStart(*[Indicate(n[1], color=GREEN) for n in ns], lag_ratio=0.2), run_time=1.3)
        stuck = label('stuck ON → cancer', 1.2, 2.8, RED, 28)
        self.at('Mutations that hold')
        self.play(FadeOut(gf), FadeIn(stuck), *[n[1].animate.set_stroke(GREEN, 4) for n in ns[1:]], run_time=0.7)
        self.at('So first learn')
        self.play(FadeOut(stuck), run_time=0.4)
        self.finish()


class S02Catch(SpokenScene):
    def construct(self):
        V = View(k=1.15, ox=RAS_X, oy=RAS_Y, sx=-3.4, sy=0)
        mem = membrane(V).shift(LEFT * 0.25)
        r = ras(V)
        r.lbl.shift(LEFT * 0.16 + UP * 0.2)
        tag = nt_tag(V, 'GDP', GREY)
        rec = node('receptor', -4.6, 2.8, GREY, 26)
        grb = node('Grb2', -2.3, 2.8, GREY, 26)
        sos = node('SOS', -0.3, 2.8, PINK, 28)
        self.at('The active receptor')
        self.play(FadeIn(mem), FadeIn(r), FadeIn(tag), FadeIn(rec), run_time=0.55)
        self.at('recruits')
        recruitment = VGroup(link(rec, grb), link(grb, sos))
        self.play(FadeIn(grb, shift=LEFT*0.3), FadeIn(sos, shift=LEFT*0.3), Create(recruitment), run_time=0.7)
        self.at('makes')
        self.play(sos.animate.move_to([-1.3, 0, 0]), FadeOut(recruitment), run_time=0.6)
        self.at('release GDP')
        self.play(tag.animate.shift(RIGHT*2).set_opacity(0), run_time=0.65)
        gtp = nt_tag(V, 'GTP', GREEN).shift(RIGHT*2)
        self.at('so GTP can bind')
        self.play(FadeIn(gtp), run_time=0.2)
        self.play(gtp.animate.shift(LEFT*2), Transform(r.body, ras_body(V, 70, True)), run_time=0.65)
        notkin = label('Ras: contact, not phosphorylation', 0, -2.8, BLUE, 28)
        self.at('is not a kinase')
        self.play(FadeOut(rec), FadeOut(grb), FadeOut(sos), FadeIn(notkin), run_time=0.5)
        a = raf(View(), 2.2, 0)
        self.at('It catches')
        self.play(FadeIn(a), run_time=0.4)
        self.at('brings it to the membrane')
        self.play(a.animate.shift(LEFT*3.65), run_time=0.85)
        closed = label('recruited ≠ open', 2, 1.5, GREY, 28)
        self.at('Binding alone')
        self.play(FadeIn(closed), run_time=0.5)
        lipid = label('lipid contact', -3.2, -1.65, GREY, 24)
        steps = label('+ further steps', 1.6, -1.65, GREY, 26)
        self.at('Contact with membrane lipids')
        self.play(FadeIn(lipid), mem.animate.set_stroke(YELLOW, 4), run_time=0.5)
        self.at('and further steps')
        self.play(FadeIn(steps), run_time=0.4)
        self.at('help it open')
        opened = raf(View(), -1.45, 0, open_=True)
        self.play(Transform(a, opened), FadeOut(closed), run_time=0.7)
        b = raf(View(), 2.4, -1.05, open_=True)
        self.at('Two RAF molecules')
        self.play(FadeOut(lipid), FadeOut(steps), FadeOut(notkin), FadeIn(b), run_time=0.5)
        self.at('then pair')
        self.play(b.animate.shift(LEFT*3.85), run_time=0.7)
        active = label('pairing → normal activation', 1.6, -2.8, GREEN, 28)
        self.at('normal activation')
        self.play(*raf_on(a), *raf_on(b), FadeIn(active), run_time=0.6)
        self.finish()


class S03Relay(SpokenScene):
    def construct(self):
        V = View()
        a = raf(V, -4.8, 1.5, open_=True, active=True)
        m = kinase(V, 'MEK', -0.7, 1.5, ('Ser', 'Ser'))
        e = kinase(V, 'ERK', 4.4, 1.5, ('Thr', 'Tyr'))
        # The intervening residue is a text schematic, not a drawn molecular structure.
        gap = label('Thr – X – Tyr', 4.0, 3.0, GREY, 24)
        ps = [pbadge().move_to(a.body.get_right()) for _ in range(2)]
        self.at('adds phosphates')
        self.play(FadeIn(a), FadeIn(m), *[FadeIn(p) for p in ps], run_time=0.5)
        self.at('two serines')
        self.play(*[p.animate.move_to(s) for p, s in zip(ps, m.sites)], *go_on(m), run_time=0.65)
        p1 = pbadge().move_to(m.body.get_right())
        p2 = pbadge().move_to(m.body.get_right())
        self.at('adds one')
        self.play(FadeIn(e), FadeIn(gap), FadeIn(p1), run_time=0.4)
        self.at('a threonine')
        self.play(p1.animate.move_to(e.sites[0]), run_time=0.5)
        self.at('a tyrosine')
        self.play(FadeIn(p2), run_time=0.15)
        self.play(p2.animate.move_to(e.sites[1]), run_time=0.5)
        self.at('needs both')
        self.play(*go_on(e), pop(p1), pop(p2), run_time=0.6)
        targets = VGroup(*[node('protein', x, -0.7, PURPLE, 24) for x in [-4.6, -1.9, 0.8]])
        fan = VGroup(*[arr(e.get_bottom(), t.get_top(), PURPLE, w=3) for t in targets])
        cytoplasm = label('cytoplasm', -2.0, -1.5, GREY, 24)
        self.at('wide fan of targets')
        self.play(FadeOut(a), FadeOut(m), *[FadeOut(p) for p in ps], FadeOut(gap), FadeIn(targets), FadeIn(cytoplasm), Create(fan), run_time=0.7)
        elk = node('Elk-1', 3.9, -1.2, PURPLE, 28)
        nucl = label('nucleus', 5.5, -0.5, GREY, 24)
        ea = arr(e.get_bottom(), elk.get_top()+UP*0.12, GOLD, w=3)
        pp = pbadge().move_to(e.get_bottom())
        self.at('In the nucleus')
        self.play(FadeIn(elk), FadeIn(nucl), run_time=0.4)
        self.at('phosphorylates')
        self.play(GrowArrow(ea), FadeIn(pp), run_time=0.25)
        self.play(pp.animate.move_to(elk.get_right()+RIGHT*0.3), run_time=0.6)
        gene = node('c-fos', 0.3, -2.8, ORANGE, 28)
        ga = arr(elk.get_bottom(), gene.get_right(), GREEN, w=3)
        self.at('helps switch on')
        self.play(FadeIn(gene), GrowArrow(ga), run_time=0.6)
        self.finish()


class S08Cancer(SpokenScene):
    def construct(self):
        title = label('Cancer: relay held ON', 0, 3.1, RED, 32)
        context = label('B-Raf V600E', 0, 2.0, PURPLE, 30)
        mutant = node('B-Raf V600E', -3.5, 0.4, PURPLE, 28)
        mek = node('MEK', 0, 0.4)
        erk = node('ERK', 3.5, 0.4)
        edges = VGroup(link(mutant, mek, GREEN), link(mek, erk, GREEN))
        output = label('ERK output ON', 3.5, -1.0, GREEN, 28)
        self.at('In cancer')
        self.add(title, context, mutant, mek, erk, edges, output)
        mutant[1].set_stroke(GREEN, 4)
        mek[1].set_stroke(GREEN, 4)
        erk[1].set_stroke(GREEN, 4)
        self.at('BRAF V600E')
        self.play(Indicate(context, color=GREEN, scale_factor=1.05), run_time=0.6)
        independent = label('without Ras–GTP', -3.5, -1.0, GREY, 24)
        self.play(FadeIn(independent), run_time=0.3)
        drug = node('Raf inhibitor', -3.5, 1.45, RED, 24)
        self.at('A RAF inhibitor')
        self.play(FadeIn(drug, shift=DOWN*0.3), run_time=0.4)
        self.at('can block it')
        self.play(edges.animate.set_color(GREY), Transform(output, label('ERK output OFF', 3.5, -1, GREY, 28)),
                  mutant[1].animate.set_stroke(RED), run_time=0.6)
        self.at('But with normal')
        self.play(*[FadeOut(o) for o in [context, mutant, mek, erk, edges, output, independent, drug]], run_time=0.35)
        context = label('Normal B-Raf + active Ras', 0, 2.0, BLUE, 30)
        a = raf(View(), -3.4, 0.7, open_=True)
        b = raf(View(), -3.4, -0.35, open_=True)
        ras_tag = node('Ras–GTP', -3.6, -2.0, BLUE, 26)
        drug = node('drug-bound', -0.6, 0.7, RED, 24)
        free = label('drug-free partner', -0.2, -0.65, PURPLE, 24)
        mek = node('MEK', 3.6, -0.4)
        erk = node('ERK', 3.6, -2.15)
        outedge = arr(mek.get_bottom(), erk.get_top(), GREY, w=3)
        self.play(FadeIn(context), FadeIn(a), FadeIn(b), FadeIn(ras_tag), FadeIn(mek), FadeIn(erk), FadeIn(outedge), run_time=0.5)
        self.at('drug bound')
        self.play(FadeIn(drug), a.body.animate.set_stroke(RED), run_time=0.4)
        self.at('can activate')
        partner = arr(a.body.get_right(), b.body.get_right()+RIGHT*0.35, GREEN, w=3)
        self.play(GrowArrow(partner), *raf_on(b), FadeIn(free), run_time=0.55)
        signal = arr(b.body.get_right(), mek.get_left(), GREEN, w=3)
        self.at('activity then rises')
        rising = label('ERK activity ↑', 3.6, -3.1, GREEN, 26)
        self.play(GrowArrow(signal), outedge.animate.set_color(GREEN), mek[1].animate.set_stroke(GREEN), erk[1].animate.set_stroke(GREEN), FadeIn(rising), run_time=0.6)
        self.at('A MEK inhibitor')
        md = node('MEK inhibitor', 3.6, 0.9, RED, 24)
        self.play(FadeIn(md), run_time=0.4)
        self.at('holds MEK inactive')
        self.play(mek[1].animate.set_stroke(RED), outedge.animate.set_color(GREY), erk[1].animate.set_stroke(GREY), FadeOut(rising), run_time=0.6)
        self.at('effect depends')
        self.play(Indicate(context, scale_factor=1.05), run_time=0.6)
        self.finish()


class S04Feedback(SpokenScene):
    def construct(self):
        sos = node('SOS', -4.1, 1.6, PINK)
        rafc = node('Raf', 0, 1.6)
        erk = kinase(View(), 'ERK', 4.0, 0.2, ('Thr', 'Tyr'))
        erk.body.set_stroke(GREEN)
        ps = [pbadge().move_to(s) for s in erk.sites]
        fast = label('fast feedback', -1.5, 3.05, RED, 30)
        self.at('The relay also')
        self.play(FadeIn(sos), FadeIn(rafc), FadeIn(erk), *[FadeIn(p) for p in ps], run_time=0.5)
        f1 = fb_curve([3.7, 0.9, 0], [4, 2.8, 0], [0, 2.9, 0], [0, 2.05, 0])
        f2 = fb_curve([3, 0.2, 0], [0, -0.5, 0], [-4.1, -0.5, 0], [-4.1, 1.1, 0])
        self.at('ERK weakens')
        self.play(Create(f1), Create(f2), FadeIn(fast), run_time=0.6)
        self.at('by phosphorylation')
        pp = [pbadge().move_to([0, 2.4, 0]), pbadge().move_to([-4.1, 0.7, 0])]
        self.play(*[FadeIn(p) for p in pp], sos[1].animate.set_stroke(GREY), rafc[1].animate.set_stroke(GREY), run_time=0.5)
        gene = node('phosphatase genes', -3.8, -1.8, ORANGE, 24)
        ga = arr(erk.get_bottom(), gene.get_right(), GREEN, w=3)
        self.at('It turns on genes')
        self.play(FadeOut(f1), FadeOut(f2), FadeOut(fast), *[FadeOut(p) for p in pp], FadeOut(sos), FadeOut(rafc), FadeIn(gene), GrowArrow(ga), run_time=0.6)
        ghost = ghost_chip('phosphatase', 26, RED).move_to([0, -2.6, 0])
        self.at('for phosphatases')
        self.play(FadeIn(ghost), run_time=0.4)
        ck = clock([-0.5, 1.8, 0], 0.55)
        delay = label('protein-production delay', -0.6, 2.8, GREY, 26)
        self.at('That takes longer')
        self.play(FadeIn(ck), FadeIn(delay), run_time=0.4)
        self.play(Rotate(ck.hand, -TAU, about_point=ck.c), run_time=0.9)
        ph = node('phosphatase', 0, -2.6, RED, 26)
        self.at('a protein must be made')
        self.play(FadeOut(ghost), FadeIn(ph), run_time=0.5)
        self.play(*[p.animate.move_to(ph).set_opacity(0) for p in ps], *go_quiet(erk), run_time=0.7)
        self.at('Signal duration')
        self.play(*[FadeOut(o) for o in [gene, ga, ph, erk, ck, delay]], run_time=0.4)
        factors = VGroup(*[label(t, -4.0, y, GREY, 28) for t, y in [('stimulus', 1.8), ('cell type', 0.3), ('dose', -1.2)]])
        window = Rectangle(width=5.5, height=2.4, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.15).move_to([2, 0.3, 0])
        span = DoubleArrow([-0.75, -1.6, 0], [4.75, -1.6, 0], color=GREEN, buff=0)
        dur = label('duration window', 2, 2.0, GREEN, 30)
        time = label('time', 2, -2.3, GREY, 24)
        self.play(FadeIn(factors), GrowFromEdge(window, LEFT), FadeIn(dur), GrowFromCenter(span), FadeIn(time), run_time=0.8)
        self.at('Timing helps')
        self.play(window.animate.stretch(0.7, 0, about_edge=LEFT), run_time=0.7)
        self.finish()


class S09Modules(SpokenScene):
    def construct(self):
        left = VGroup(*[node(n, -3.3, y, PURPLE, 30) for n, y in [('Raf', 2.0), ('MEK', 0.1), ('ERK', -1.8)]])
        arrows = VGroup(*[arr(a.get_bottom(), b.get_top(), GREEN, w=w) for a, b, w in zip(left, left[1:], [3, 7])])
        title = label('amplification', -3.3, 3.1, GREEN, 30)
        self.at('Three kinase tiers')
        self.play(FadeIn(left), Create(arrows), run_time=0.6)
        self.at('give amplification')
        pulses = VGroup(*[Dot([-4.5+i*0.35, -2.6, 0], radius=0.08, color=GREEN) for i in range(8)])
        self.play(FadeIn(title), LaggedStart(*[FadeIn(p) for p in pulses], lag_ratio=0.1), run_time=0.65)
        controls = VGroup(*[VGroup(Line([-5.5,y,0],[-4.5,y,0], color=RED), Line([-4.5,y-0.2,0],[-4.5,y+0.2,0], color=RED)) for y in [2,0.1,-1.8]])
        self.at('separate control points')
        self.play(Create(controls), run_time=0.6)
        right = VGroup(*[node(n, 2.7, y, GREY, 28) for n,y in [('kinase A',2),('kinase B',0.1),('kinase C',-1.8)]])
        ra = VGroup(*[arr(a.get_bottom(), b.get_top(), GREY, w=3) for a,b in zip(right,right[1:])])
        other = label('another MAPK module', 2.7, 3.1, GREY, 26)
        self.at('Other MAP kinase pathways')
        self.play(FadeOut(controls), FadeOut(pulses), FadeIn(right), Create(ra), FadeIn(other), run_time=0.7)
        frames = VGroup(*[RoundedRectangle(width=3.1,height=5.6,corner_radius=0.3,stroke_color=GREY,stroke_width=3).move_to([x,0.1,0]) for x in [-3.3,2.7]])
        scaffold = label('scaffolds', -0.3, -3.3, GREY, 26)
        self.at('Scaffolds hold')
        self.play(Create(frames), FadeIn(scaffold), run_time=0.7)
        self.at('mainly to each other')
        self.play(Indicate(arrows, color=GREEN), Indicate(ra, color=GREEN), run_time=0.6)
        loc = VGroup(Circle(radius=0.22,color=YELLOW), Dot(radius=0.06,color=YELLOW)).move_to([5.2,-2.9,0])
        address = label('location', 5.2, -3.45, GREY, 24)
        self.at('where the cascade runs')
        self.play(FadeIn(loc), FadeIn(address), frames[1].animate.set_stroke(YELLOW), run_time=0.7)
        self.finish()


class S10Development(SpokenScene):
    def construct(self):
        head = label('Mild pathway over-activation', 0, 2.9, GREEN, 32)
        cells = VGroup(*[cell_icon([x,0.3,0],0.65) for x in [-4,0,4]])
        tissues = VGroup(*[label(t,x,-1.0,ORANGE,28) for t,x in [('face',-4),('heart',0),('growth',4)]])
        self.at('Milder overactivation')
        self.play(FadeIn(head), FadeIn(cells), run_time=0.5)
        origin = label('inherited  /  new at conception', 0, 1.7, GREY, 28)
        self.at('Mutations inherited')
        self.play(FadeIn(origin), run_time=0.6)
        syndrome = label('RASopathies', 0, -2.4, TEXT, 36)
        self.at('developmental syndromes')
        self.play(FadeIn(syndrome), FadeIn(tissues), run_time=0.6)
        self.at('Their effects differ')
        self.play(LaggedStart(*[Indicate(c, color=ORANGE, scale_factor=1.08) for c in cells],lag_ratio=0.3), run_time=1)
        self.at('The relay carries')
        self.play(*[FadeOut(o) for o in [head,cells,tissues,origin,syndrome]], run_time=0.35)
        ns, ls, cyt, nuc, branches = overview()
        self.play(*[FadeIn(n) for n in ns], Create(VGroup(*ls)), FadeIn(cyt), FadeIn(nuc), Create(branches), run_time=0.65)
        genes = node('genes', -3.5, -2, ORANGE, 26)
        ga = arr(nuc[0].get_left(), genes.get_right(),GREEN,w=3)
        scaffold = bracket(5.7,0.7,1.8,side=1)
        sc = label('scaffold', 4.9, 2.6, GREY, 24)
        feedback = fb_curve([4.5,1.7,0],[4.5,3.5,0],[0,3.5,0],[0,1.8,0])
        self.at('but its control')
        self.play(Create(feedback), Create(scaffold), FadeIn(sc), FadeIn(genes), GrowArrow(ga), run_time=0.6)
        context = label('cell context → response', 0, -3.25, ORANGE, 28)
        self.at('shape the answer')
        self.play(FadeIn(context), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = 'Ras, Raf, MEK and ERK relay a surface signal to genes.'
