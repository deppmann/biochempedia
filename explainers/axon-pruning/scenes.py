"""Where Support Is Lost (chapter 1 of Pruning Without Dying: Axons That Cut Themselves Back)

COLOR MAP (one colour per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = the neuron (cell body, axons, branches)
  YELLOW = NGF (the dots, and every "no NGF" tag)
  VIOLET = caspases (scissors icon)
  ORANGE = Apaf-1 and the apoptosome it builds (later chapters)
  RED    = degeneration, death, lost branches
  GREEN  = survival (the neuron lives, branches stay intact)
  GREY   = dish, target tissue, structure
  TEAL   = a signal or route travelling back along the axon, and the PREDICT cue
  CLAY   = the sculptor's clay (analogy only)
  TEXT   = labels (bright, 26 pt or larger)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403
from kx_manim import BG  # noqa: F401

VIOLET = "#A98BE0"
ORANGE = "#F29E4C"
CLAY = "#C9A27A"
SIGNAL = TEAL
SOFT = "#C5CAD6"   # secondary label colour, still high contrast on the dark ground


def P(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------------------------------------
# generic helpers
# ------------------------------------------------------------------------------------------------
def branch(p0, p1, w=6, color=BLUE, k=1.5):
    c = CubicBezier(p0, p0 + P(k, 0), p1 - P(k, 0), p1)
    c.set_fill(opacity=0).set_stroke(color, w)
    return c


def dendrite(center, ang, r, length=0.75):
    a = np.radians(ang)
    u = P(np.cos(a), np.sin(a))
    s = center + u * r
    e = s + u * length
    parts = [Line(s, e)]
    for d in (35, -35):
        b = np.radians(ang + d)
        parts.append(Line(e, e + P(np.cos(b), np.sin(b)) * 0.35))
    g = VGroup(*parts)
    g.set_stroke(BLUE, 5)
    return g


YS7 = [-2.55, -1.7, -0.85, 0.0, 0.85, 1.7, 2.55]


class Neuron:
    """soma + (dendrites) + trunk + fan of branches, each branch is curve + tip dot."""

    def __init__(self, soma=(-4.6, 0.0), trunk_end=(-2.4, 0.0), tip_x=3.9, ys=YS7, r=0.7, dend=True, w=6):
        sp = P(*soma)
        self.soma_pt = sp
        self.body = Circle(radius=r, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35).move_to(sp)
        self.dends = [dendrite(sp, a, r) for a in (120, 180, 240)] if dend else []
        self.trunk = Line(sp + P(r, 0), P(*trunk_end), color=BLUE, stroke_width=w + 2)
        self.curves = [branch(P(*trunk_end), P(tip_x, y), w) for y in ys]
        self.tipdots = [Dot(P(tip_x, y), radius=0.1, color=BLUE) for y in ys]
        self.branches = [VGroup(c, t) for c, t in zip(self.curves, self.tipdots)]
        self.tip_pts = [P(tip_x, y) for y in ys]

    def all(self):
        return VGroup(self.body, *self.dends, self.trunk, *self.branches)

    def core(self):
        return VGroup(self.body, *self.dends, self.trunk)

    def branch_group(self):
        return VGroup(*self.branches)


def mini(cx, cy, k=1.0, ys=(1.9, 0.0, -1.9), w=6):
    """A small neuron for the panel scenes, scaled by k around (cx, cy)."""
    return Neuron(soma=(cx - 2.5 * k, cy), trunk_end=(cx - 1.2 * k, cy), tip_x=cx + 2.6 * k,
                  ys=[cy + y * k for y in ys], r=0.55 * k + 0.05, dend=False, w=w)


def target_block():
    return RoundedRectangle(corner_radius=0.3, width=2.1, height=6.1, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to(P(5.55, 0))


def target_label():
    return T("target", 28, TEXT).move_to(P(5.55, 3.42))


def target_dots_at(x=5.7, ys=YS7):
    return VGroup(*[Dot(P(x, y), radius=0.11, color=YELLOW) for y in ys])


def pieces_of(vm, n):
    out = []
    for i in range(n):
        p = VMobject()
        p.pointwise_become_partial(vm, i / n, (i + 1) / n)
        p.match_style(vm)
        out.append(p)
    return out


def frag_targets(pcs, seed, spread=0.25):
    rng = random.Random(seed)
    tg = []
    for p in pcs:
        t = p.copy()
        t.shift(P(rng.uniform(-0.1, 0.1), rng.uniform(-spread, spread))).rotate(rng.uniform(-0.5, 0.5)).scale(0.75)
        t.set_color(RED).set_opacity(0.6)
        tg.append(t)
    return tg


def shatter(scene, originals, pcs, seed, rt=1.2, spread=0.25, extra=()):
    """Swap `originals` for same-place `pcs`, then break the pieces apart and dim them red."""
    if originals:
        scene.remove(*originals)
    scene.add(*pcs)
    tg = frag_targets(pcs, seed, spread)
    scene.play(*[Transform(p, t) for p, t in zip(pcs, tg)], *extra, run_time=rt)


def frag_now(pcs, seed, spread=0.25):
    for p, t in zip(pcs, frag_targets(pcs, seed, spread)):
        p.become(t)


def qmark(x, y, size=44, color=TEXT):
    return T("?", size, color, weight=BOLD).move_to(P(x, y))


def scissors(cx, cy, s=1.0):
    a = Line(P(0.9, 0.2), P(-0.45, -0.2))
    b = Line(P(0.9, -0.2), P(-0.45, 0.2))
    r1 = Circle(radius=0.17, stroke_width=4, fill_opacity=0).move_to(P(-0.62, -0.27))
    r2 = Circle(radius=0.17, stroke_width=4, fill_opacity=0).move_to(P(-0.62, 0.27))
    g = VGroup(a, b, r1, r2)
    g.set_stroke(VIOLET, 6)
    r1.set_stroke(VIOLET, 4)
    r2.set_stroke(VIOLET, 4)
    g.scale(s)
    return g.move_to(P(cx, cy))


def legend(x=5.75, y=3.35):
    d = Dot(P(x - 0.55, y), radius=0.1, color=YELLOW)
    t = T("NGF", 26, YELLOW).move_to(P(x + 0.3, y))
    return VGroup(d, t)


def no_ngf(x, y, text="no NGF"):
    return T(text, 26, YELLOW, weight=BOLD).move_to(P(x, y))


def drain(group, rt=1.1):
    return LaggedStart(*[d.animate.shift(UP * 0.35).set_opacity(0) for d in group], lag_ratio=0.1, run_time=rt)


def fill_dots(group, rt=1.3):
    return LaggedStart(*[FadeIn(d, scale=0.3) for d in group], lag_ratio=0.06, run_time=rt)


# ------------------------------------------------------------------------------------------------
# Campenot dish (seen from above): about 80% of the frame height, the same size in every dish scene
# ------------------------------------------------------------------------------------------------
DY, CHH, DXE = -0.25, 3.2, 6.3
ROWS = [1.45, -0.25, -1.95]
WALLX = 2.4
TIPX = 5.7
NS = 6
SOMA_R = 0.42
RT_SEED = 11
SIDE_CX = (DXE + WALLX + 0.15) / 2
STRIP_Y = 3.35


class Dish:
    def __init__(self):
        self.outline = RoundedRectangle(corner_radius=0.2, width=2 * DXE, height=2 * CHH, stroke_color=GREY,
                                        stroke_width=4, fill_opacity=0).move_to(P(0, DY))
        self.walls = VGroup()
        for wx in (-WALLX, WALLX):
            ys = [DY + CHH] + [v for r in ROWS for v in (r + 0.13, r - 0.13)] + [DY - CHH]
            for i in range(0, len(ys), 2):
                top, bot = ys[i], ys[i + 1]
                self.walls.add(Rectangle(width=0.3, height=top - bot, stroke_width=0, fill_color=GREY,
                                         fill_opacity=0.5).move_to(P(wx, (top + bot) / 2)))
        h = 2 * CHH - 0.1
        sw = (DXE - 0.1) - (WALLX + 0.15)
        self.tint = VGroup(
            Rectangle(width=sw, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.10)
            .move_to(P(-((DXE - 0.1) + (WALLX + 0.15)) / 2, DY)),
            Rectangle(width=2 * (WALLX - 0.15) - 0.1, height=h, stroke_width=0, fill_color=GREY,
                      fill_opacity=0.10).move_to(P(0, DY)),
            Rectangle(width=sw, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.10)
            .move_to(P(((DXE - 0.1) + (WALLX + 0.15)) / 2, DY)))
        self.center_rect = Rectangle(width=2 * (WALLX - 0.15), height=2 * CHH, stroke_color=TEXT, stroke_width=4,
                                     fill_opacity=0).move_to(P(0, DY))
        self.bodies = VGroup(*[Circle(radius=SOMA_R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                      fill_opacity=0.35).move_to(P(0, y)) for y in ROWS])
        wx = WALLX + 0.15
        self.inner, self.outer, self.tips, self.dots = {}, {}, {}, {}
        # two separate branches leave each cell body, from different points (upper left, lower right)
        self.inner[-1] = []
        self.inner[1] = []
        for y in ROWS:
            sl = P(-0.364, y + 0.21)
            self.inner[-1].append(self._curve(sl, P(-wx, y), -1))
            sr = P(0.364, y - 0.21)
            self.inner[1].append(self._curve(sr, P(wx, y), 1))
        for sd in (-1, 1):
            xs = np.linspace(wx, TIPX, NS + 1)
            self.outer[sd] = [[Line(P(sd * xs[i], y), P(sd * xs[i + 1], y), color=BLUE, stroke_width=6)
                               for i in range(NS)] for y in ROWS]
            self.tips[sd] = VGroup(*[Dot(P(sd * TIPX, y), radius=0.11, color=BLUE) for y in ROWS])
            pts = [(sd * x, y) for x in (3.2, 4.3, 5.4) for y in (1.95, 0.6, -1.1)]
            self.dots[sd] = VGroup(*[Dot(P(*p), radius=0.1, color=YELLOW) for p in pts])
        cpts = [(x, y) for x in (-1.5, -0.85, 0.85, 1.5) for y in (0.6, -1.1)]
        self.dots[0] = VGroup(*[Dot(P(*p), radius=0.1, color=YELLOW) for p in cpts])

    @staticmethod
    def _curve(a, b, sd):
        c = CubicBezier(a, a + P(sd * 0.9, 0), b - P(sd * 0.9, 0), b)
        c.set_fill(opacity=0).set_stroke(BLUE, 6)
        return c

    def outer_segs(self, sd):
        return [s for row in self.outer[sd] for s in row]

    def core(self, scene):
        """Everything physical in the dish, healthy."""
        scene.add(self.tint, self.outline, self.walls, *self.inner[-1], *self.inner[1], *self.outer_segs(-1),
                  *self.outer_segs(1), self.tips[-1], self.tips[1], self.bodies)


def dish_labels():
    ll = T("side compartment", 26, TEXT).move_to(P(-SIDE_CX, 2.55))
    lr = T("side compartment", 26, TEXT).move_to(P(SIDE_CX, 2.55))
    lc = VGroup(T("central compartment:", 26, TEXT), T("cell bodies", 26, BLUE, weight=BOLD)).arrange(DOWN, buff=0.08)
    lc.move_to(P(0, 2.42))
    return ll, lc, lr


def culture_note():
    g = VGroup(T("in culture, during the", 26, SOFT), T("NGF-dependent window", 26, SOFT)).arrange(DOWN, buff=0.06)
    return g.move_to(P(0, -3.05))


def strip(text, predict=False, color=TEXT, x=-0.6):
    t = T(text, 28, color)
    if predict:
        c = chip("PREDICT", TEAL, size=24, pad=0.14)
        g = VGroup(c, t).arrange(RIGHT, buff=0.3)
    else:
        g = VGroup(t)
    return g.move_to(P(x, STRIP_Y))


def swap(scene_play, old, new, rt=0.45):
    scene_play(FadeOut(old), FadeIn(new, shift=DOWN * 0.08), run_time=rt)


def ring_bodies(D):
    return VGroup(*[Circle(radius=SOMA_R + 0.14, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(b.get_center())
                    for b in D.bodies])


def body_qs(D):
    return VGroup(*[qmark(0, y, 40) for y in ROWS])


def right_qs():
    return VGroup(*[qmark(4.4, y + 0.5, 44) for y in ROWS])


def out_chip(text, color, x, y=-3.0):
    return chip(text, color, size=26, pad=0.16).move_to(P(x, y))


# ------------------------------------------------------------------------------------------------
# dish states, so each scene starts exactly where the last one ended
# ------------------------------------------------------------------------------------------------
def state_s05_end(scene, D):
    scene.add(D.outline, D.walls)
    ll, lc, lr = dish_labels()
    scene.add(D.bodies, ll, lc, lr)
    st = strip("a divided dish, seen from above", color=SOFT)
    scene.add(st)
    return dict(ll=ll, lc=lc, lr=lr, st=st)


def state_s06_end(scene, D):
    D.core(scene)
    ll, lc, lr = dish_labels()
    lg = legend()
    scene.add(ll, lc, lr, D.dots[-1], D.dots[0], D.dots[1], lg)
    st = strip("Campenot, 1977 and 1982", color=SOFT)
    scene.add(st)
    return dict(ll=ll, lc=lc, lr=lr, st=st, lg=lg)


def state_q1(scene, D, with_q=True, strip_mode="predict"):
    """Dish after NGF was removed from the right compartment only (end of scene 7)."""
    D.core(scene)
    ll, lc, _ = dish_labels()
    tag = no_ngf(SIDE_CX, 2.55)
    lg = legend()
    note = culture_note()
    scene.add(ll, lc, tag, D.dots[-1], D.dots[0], lg, note)
    if strip_mode == "predict":
        st = strip("Which branches degenerate?", predict=True)
    else:
        st = strip("NGF removed from the right compartment only")
    scene.add(st)
    qs = right_qs()
    if with_q:
        scene.add(qs)
    return dict(ll=ll, lc=lc, tag=tag, lg=lg, note=note, st=st, qs=qs)


def state_q2(scene, D):
    """Fresh dish, NGF removed from every compartment, question on the cell bodies (end of scene 11)."""
    D.core(scene)
    tags = [no_ngf(-SIDE_CX, 2.55), no_ngf(0, 2.55), no_ngf(SIDE_CX, 2.55)]
    lg = legend()
    note = culture_note()
    rings = ring_bodies(D)
    qs = body_qs(D)
    st = strip("What happens to the neuron?", predict=True)
    scene.add(*tags, lg, note, rings, qs, st)
    return dict(tags=tags, lg=lg, note=note, rings=rings, qs=qs, st=st)


# ------------------------------------------------------------------------------------------------
# scenes
# ------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Pruning Without Dying: Axons That Cut Themselves Back"
    TITLE = "Where Support Is Lost"


class S01Q(SpokenScene):
    def construct(self):
        N = Neuron()
        tgt = target_block()
        tl = target_label()
        self.add(tgt, tl)
        self.at("A young neuron")
        self.play(FadeIn(N.body, scale=0.7), *[Create(d) for d in N.dends], Create(N.trunk), run_time=0.8)
        self.at("grows more branches")
        self.play(LaggedStart(*[Create(b) for b in N.branches], lag_ratio=0.12), run_time=1.1)
        self.at("than it keeps")
        self.wait(0.2)
        self.at("Who decides")
        qs = VGroup(*[qmark(4.25, y, 44, TEXT) for y in YS7])
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.08), run_time=0.7)
        self.at("which branch goes")
        self.play(LaggedStart(*[Indicate(c, color=TEXT, scale_factor=1.0) for c in N.curves], lag_ratio=0.12),
                  run_time=1.2)
        self.finish()


class S02Define(SpokenScene):
    def construct(self):
        N = Neuron()
        tgt = target_block()
        self.add(tgt, target_label(), N.all())
        self.at("Pruning removes")
        cap = VGroup(T("Pruning removes an axon branch or a dendrite", 26, TEXT),
                     T("from a neuron that survives.", 26, TEXT)).arrange(DOWN, buff=0.08).move_to(P(-0.5, -3.2))
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.at("an axon branch")
        victim = N.branches[5]
        self.play(Indicate(victim, color=RED, scale_factor=1.0), run_time=0.5)
        self.play(victim.animate.set_color(RED), run_time=0.3)
        self.play(FadeOut(victim), run_time=0.5)
        self.at("or a dendrite")
        dv = N.dends[0]
        self.play(dv.animate.set_color(RED), run_time=0.3)
        self.play(FadeOut(dv), run_time=0.5)
        self.at("from a neuron")
        self.play(Indicate(N.body, color=GREEN, scale_factor=1.15), run_time=0.5)
        self.at("that survives")
        ch = chip("the neuron survives", GREEN, size=26).move_to(P(-3.6, -2.4))
        self.play(FadeIn(ch, shift=UP * 0.1), N.body.animate.set_stroke(GREEN), run_time=0.6)
        self.finish()


def clay_lump(cx, s=0.82):
    rng = random.Random(5)
    pts = []
    n = 14
    for i in range(n):
        a = TAU * i / n
        rr = 1.0 + rng.uniform(-0.14, 0.14)
        pts.append(P(cx + 2.05 * s * rr * np.cos(a), 2.25 * s * rr * np.sin(a)))
    pts.append(pts[0])
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_stroke(CLAY, 4).set_fill(CLAY, 0.5)
    return m


def clay_figure(cx, s=0.82):
    right = [(0, 2.2), (0.45, 2.05), (0.62, 1.6), (0.45, 1.15), (0.22, 0.95), (0.2, 0.75), (0.5, 0.6), (0.8, 0.0),
             (1.05, -1.0), (1.2, -1.9), (1.3, -2.2)]
    left = [(-x, y) for x, y in reversed(right)]
    pts = [P(cx + x * s, y * s) for x, y in right] + [P(cx, -2.25 * s)] + [P(cx + x * s, y * s) for x, y in left[1:]]
    pts.append(pts[0])
    m = VMobject()
    m.set_points_smoothly(pts)
    m.set_stroke(CLAY, 4).set_fill(CLAY, 0.5)
    return m


class S03Draft(SpokenScene):
    def construct(self):
        # the same neuron as scenes 1 and 2, drawn before pruning, moved to the right half
        N = Neuron(soma=(0.2, 0.0), trunk_end=(1.8, 0.0), tip_x=6.1, ys=YS7, r=0.6, dend=True)
        cx = -4.4
        lump = clay_lump(cx)
        fig = clay_figure(cx)
        lab_n = T("the same neuron, before pruning", 28, TEXT, weight=BOLD).move_to(P(3.2, 3.3))
        lab_c = T("the sculptor's clay", 28, CLAY, weight=BOLD).move_to(P(cx, 3.3))
        self.at("Development first builds")
        self.play(FadeIn(lump, scale=0.7), FadeIn(N.body, scale=0.7), *[Create(d) for d in N.dends], Create(N.trunk),
                  LaggedStart(*[Create(b) for b in N.branches], lag_ratio=0.12),
                  FadeIn(lab_n, shift=DOWN * 0.1), FadeIn(lab_c, shift=DOWN * 0.1), run_time=1.5)
        self.at("rough draft")
        lab = T("rough draft", 32, TEXT, weight=BOLD).move_to(P(0.8, -3.3))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.2)
        self.at("then carves it")
        rng = random.Random(8)
        chips_ = VGroup()
        for i in range(8):
            a = rng.uniform(0, TAU)
            c = Square(side_length=0.24, stroke_width=0, fill_color=CLAY, fill_opacity=0.8)
            c.move_to(P(cx + 1.7 * np.cos(a), 1.8 * np.sin(a))).rotate(rng.uniform(0, 3))
            chips_.add(c)
        pile = [(-6.2, -2.6), (-5.9, -2.62), (-5.6, -2.6), (-6.05, -2.35), (-3.2, -2.6), (-2.9, -2.62),
                (-2.6, -2.6), (-3.05, -2.35)]
        drop = [Transform(lump, fig)]
        self.add(chips_)
        for c, p in zip(chips_, pile):
            drop.append(c.animate.move_to(P(*p)))
        gone = [N.branches[i] for i in (0, 2, 4, 6)]
        lab2 = T("carved", 32, TEXT, weight=BOLD).move_to(P(0.8, -3.3))
        self.play(*drop, *[b.animate.set_color(RED) for b in gone], run_time=0.9)
        self.remove(lab)
        self.add(lab2)
        self.play(*[FadeOut(b) for b in gone], run_time=0.6)
        self.at("Think of a sculptor")
        self.play(Indicate(lab_c, color=CLAY, scale_factor=1.12), run_time=0.8)
        self.at("piles up too much clay")
        self.play(Indicate(chips_, color=CLAY, scale_factor=1.25), run_time=1.0)
        self.finish()


class S04Ngf(SpokenScene):
    def construct(self):
        N = Neuron()
        tgt = target_block()
        tl = target_label()
        note = T("the same neuron, before pruning", 26, SOFT).move_to(P(-3.2, -3.3))
        self.add(tgt, tl, N.all(), note)
        self.at("Sympathetic neurons")
        self.play(Indicate(N.body, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("need NGF")
        d = target_dots_at(5.7)
        lab = T("NGF", 36, YELLOW, weight=BOLD).move_to(P(-5.2, 3.4))
        self.play(FadeIn(lab, shift=DOWN * 0.1), LaggedStart(*[FadeIn(x, scale=0.3) for x in d], lag_ratio=0.08),
                  run_time=1.0)
        self.at("a growth factor")
        sub = T("nerve growth factor, a trophic factor", 28, TEXT).next_to(lab, RIGHT, buff=0.3, aligned_edge=DOWN)
        self.play(FadeIn(sub, shift=LEFT * 0.1), run_time=0.6)
        self.at("supplied by")
        self.play(*[x.animate.move_to(P(4.2, y)) for x, y in zip(d, YS7)], run_time=0.9)
        self.at("their target")
        self.play(Indicate(tgt, color=TEXT, scale_factor=1.03), Indicate(tl, color=TEXT, scale_factor=1.2), run_time=0.8)
        self.finish()


class S05Dish(SpokenScene):
    def construct(self):
        D = Dish()
        st = strip("a divided dish, seen from above", color=SOFT)
        self.play(FadeIn(D.outline), FadeIn(st), run_time=0.4)
        ll, lc, lr = dish_labels()
        self.at("divided into compartments")
        self.play(FadeIn(D.walls), FadeIn(ll, shift=DOWN * 0.1), FadeIn(lr, shift=DOWN * 0.1), run_time=0.8)
        self.at("cell bodies")
        self.play(FadeIn(D.bodies, scale=0.6), FadeIn(lc, shift=DOWN * 0.1), run_time=0.7)
        self.at("one compartment")
        self.play(Create(D.center_rect), run_time=0.9)
        self.play(FadeOut(D.center_rect), run_time=0.4)
        self.finish()


class S06Cross(SpokenScene):
    def construct(self):
        D = Dish()
        S = state_s05_end(self, D)
        self.at("Their branches cross")
        self.play(*[Create(l) for sd in (-1, 1) for l in D.inner[sd]], run_time=1.0)
        self.at("into side compartments")
        cred = strip("Campenot, 1977 and 1982", color=SOFT)
        rows = [Succession(*[Create(s) for s in row]) for sd in (-1, 1) for row in D.outer[sd]]
        self.play(AnimationGroup(*rows), FadeIn(D.tips[-1]), FadeIn(D.tips[1]), FadeOut(S["st"]), FadeIn(cred),
                  run_time=1.5)
        self.at("The fluids")
        self.play(FadeIn(D.tint), run_time=0.6)
        self.at("stay apart")
        self.play(Indicate(D.walls, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("NGF")
        lg = legend()
        self.play(FadeIn(lg, shift=DOWN * 0.1), fill_dots(D.dots[-1]), fill_dots(D.dots[0]), fill_dots(D.dots[1]),
                  run_time=1.4)
        self.finish()


class S07Q1(SpokenScene):
    def construct(self):
        D = Dish()
        S = state_s06_end(self, D)
        self.at("NGF")
        self.play(Indicate(D.dots[1], color=YELLOW, scale_factor=1.0), run_time=0.7)
        self.at("one side compartment")
        tag = no_ngf(SIDE_CX, 2.55)
        case = strip("NGF removed from the right compartment only")
        note = culture_note()
        self.play(drain(D.dots[1], 1.1), FadeOut(S["lr"]), FadeIn(tag, shift=DOWN * 0.1), FadeOut(S["st"]),
                  FadeIn(case, shift=DOWN * 0.08), FadeIn(note), run_time=1.1)
        self.at("Which branches degenerate")
        qs = right_qs()
        pred = strip("Which branches degenerate?", predict=True)
        segs = VGroup(*D.outer_segs(1))
        self.play(FadeIn(qs, scale=0.5), Indicate(segs, color=TEXT, scale_factor=1.0), FadeOut(case),
                  FadeIn(pred, shift=DOWN * 0.08), run_time=1.0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        D = Dish()
        state_q1(self, D)
        self.finish()


class S09R1(SpokenScene):
    def construct(self):
        D = Dish()
        S = state_q1(self, D)
        segs = D.outer_segs(1)
        case = strip("NGF removed from the right compartment only")
        self.at("Only the branches")
        shatter(self, [], segs, RT_SEED, rt=0.8,
                extra=[FadeOut(S["qs"]), FadeOut(D.tips[1]), FadeOut(S["st"]), FadeIn(case, shift=DOWN * 0.08)])
        chip_a = out_chip("degenerate", RED, SIDE_CX)
        self.play(FadeIn(chip_a, shift=UP * 0.1), run_time=0.3)
        self.at("in that compartment")
        self.play(Indicate(D.tint[2], color=RED, scale_factor=1.0), run_time=0.8)
        self.at("Branches of the same neuron")
        mid = VGroup(D.bodies[1], D.inner[-1][1], D.inner[1][1], *D.outer[-1][1])
        self.play(Indicate(mid, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.at("next door")
        self.play(Indicate(D.tint[0], color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("still in NGF")
        self.play(Indicate(D.dots[-1], color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.at("stay")
        chip_b = out_chip("stay intact", GREEN, -SIDE_CX)
        self.play(FadeIn(chip_b, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        D = Dish()
        S = state_q1(self, D, with_q=False, strip_mode="case")
        self.remove(D.tips[1])
        segs = D.outer_segs(1)
        self.remove(*segs)
        self.add(*segs)
        frag_now(segs, RT_SEED)
        self.add(out_chip("degenerate", RED, SIDE_CX), out_chip("stay intact", GREEN, -SIDE_CX))
        self.finish()


class S11Q2(SpokenScene):
    def construct(self):
        D = Dish()
        # a new dish with the same neurons: fade the old picture in as a fresh one, and say so
        ll, lc, lr = dish_labels()
        lg = legend()
        fresh = chip("new dish, same neurons", TEAL, size=28, pad=0.16).move_to(P(-0.6, STRIP_Y))
        note = culture_note()
        everything = VGroup(D.tint, D.outline, D.walls, *D.inner[-1], *D.inner[1], *D.outer_segs(-1),
                            *D.outer_segs(1), D.tips[-1], D.tips[1], D.bodies, ll, lc, lr, D.dots[-1], D.dots[0],
                            D.dots[1], lg, note)
        self.play(FadeIn(everything), FadeIn(fresh), run_time=0.45)
        self.at("from every compartment")
        tags = [no_ngf(-SIDE_CX, 2.55), no_ngf(0, 2.55), no_ngf(SIDE_CX, 2.55)]
        case = strip("NGF removed from every compartment")
        self.play(drain(D.dots[-1], 1.1), drain(D.dots[0], 1.1), drain(D.dots[1], 1.1),
                  *[FadeOut(x) for x in (ll, lc, lr)], *[FadeIn(t, shift=DOWN * 0.1) for t in tags],
                  FadeOut(fresh), FadeIn(case, shift=DOWN * 0.08), run_time=1.1)
        self.at("What happens to the neuron")
        rings = ring_bodies(D)
        qs = body_qs(D)
        pred = strip("What happens to the neuron?", predict=True)
        self.play(Create(rings), FadeIn(qs, scale=0.5), FadeOut(case), FadeIn(pred, shift=DOWN * 0.08), run_time=0.9)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        D = Dish()
        state_q2(self, D)
        self.finish()


class S13R2(SpokenScene):
    def construct(self):
        D = Dish()
        S = state_q2(self, D)
        self.at("The neuron")
        self.wait(0.1)
        self.at("dies")
        ch = chip("the neuron dies", RED, size=28, pad=0.16).move_to(P(-0.6, STRIP_Y))
        self.play(FadeOut(S["rings"]), FadeOut(S["qs"]), FadeOut(S["st"]),
                  *[b.animate.set_stroke(RED, opacity=0.35).set_fill(RED, 0.18).scale(0.7) for b in D.bodies],
                  FadeIn(ch, shift=DOWN * 0.1), run_time=0.7)
        self.at("its axons")
        outer = [s for sd in (-1, 1) for s in D.outer_segs(sd)]
        inner_orig = list(D.inner[-1]) + list(D.inner[1])
        inner_pcs = [p for c in inner_orig for p in pieces_of(c, 4)]
        shatter(self, inner_orig, inner_pcs + outer, 3, rt=1.0,
                extra=[FadeOut(D.tips[-1]), FadeOut(D.tips[1]),
                       *[b.animate.set_stroke(opacity=0.08).set_fill(opacity=0.03) for b in D.bodies]])
        self.finish()


# ---------------------------------------------------------------------------------------------
def rule_lines(size=46):
    a = T("Where support is lost", size, TEXT, font=TITLE_FONT)
    b = T("decides what is lost.", size, GOLD, font=TITLE_FONT)
    return VGroup(a, b).arrange(DOWN, buff=0.3)


def rule_one_line(size=32):
    return T("Where support is lost decides what is lost.", size, GOLD, font=TITLE_FONT).move_to(P(0, 3.3))


class S14Rule(SpokenScene):
    def construct(self):
        r = rule_lines().move_to(P(0, 0.3))
        self.at("Here is the one idea")
        tag = T("THE ONE IDEA", 26, TEAL, weight=BOLD).move_to(P(0, 2.0))
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        self.at("where support is lost")
        self.play(Write(r[0]), run_time=1.1)
        self.at("decides what is lost")
        self.play(Write(r[1]), run_time=1.1)
        cond = T("in culture, during the NGF-dependent window", 28, SOFT).move_to(P(0, -1.3))
        self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.6)
        self.finish()


class Strip:
    """One neuron laid out as a strip for the rule card: soma, one axon, three forks, NGF dots at both ends."""

    def __init__(self, y, k=1.0, x0=-5.2, xf=-1.6, xt=1.3):
        self.y, self.k = y, k
        r = 0.72 * k
        self.r = r
        self.soma = Circle(radius=r, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35).move_to(P(x0, y))
        main = Line(P(x0 + r, y), P(xf, y), color=BLUE, stroke_width=9)
        d = 1.5 * k
        self.ds = (d, 0.0, -d)
        forks = [branch(P(xf, y), P(xt, y + dd), w=8, k=0.9) for dd in self.ds]
        mp = pieces_of(main, 4)
        fp = [pieces_of(f, 3) for f in forks]
        # the first piece of each fork overlaps the others at the fork point, so it stays put (dimmed red) and
        # only the outer pieces break apart: nothing tangles
        self.stems = [p[0] for p in fp]
        self.movers = mp + [q for p in fp for q in p[1:]]
        self.parts = mp + [q for p in fp for q in p]
        self.tipdots = VGroup(*[Dot(P(xt, y + dd), radius=0.11, color=BLUE) for dd in self.ds])
        self.dots_tip = VGroup(*[Dot(P(xt + 0.5, y + dd), radius=0.1, color=YELLOW) for dd in self.ds])
        self.dots_soma = VGroup(*[Dot(P(x0 + dx, y + dy), radius=0.1, color=YELLOW)
                                  for dx, dy in [(-0.4, r + 0.35), (0.4, r + 0.35), (0.0, -r - 0.35)]])
        self.x0, self.xt = x0, xt

    def body(self):
        return VGroup(self.soma, *self.parts, self.tipdots)

    def lab_tip(self, text="no NGF here"):
        return T(text, 28, YELLOW, weight=BOLD).move_to(P(self.xt + 0.25, self.y - self.ds[0] - 0.6)).set_opacity(1)

    def lab_soma(self, text="NGF here"):
        return T(text, 26, YELLOW, weight=BOLD).move_to(P(self.x0, self.y - self.r - 1.0))


class S15Rule2(SpokenScene):
    def construct(self):
        r = rule_lines().move_to(P(0, 0.3))
        tag = T("THE ONE IDEA", 26, TEAL, weight=BOLD).move_to(P(0, 2.0))
        cond = T("in culture, during the NGF-dependent window", 28, SOFT).move_to(P(0, -1.3))
        self.add(r, tag, cond)
        S = Strip(-0.25, 1.5)
        top = rule_one_line()
        self.at("Lose support")
        self.play(FadeOut(r), FadeOut(tag), FadeOut(cond), FadeIn(top), FadeIn(S.soma, scale=0.7),
                  *[Create(a) for a in S.parts], FadeIn(S.tipdots), FadeIn(S.dots_soma), FadeIn(S.dots_tip), run_time=1.0)
        self.at("at the axons")
        cap = T("axons lose support, the cell body keeps it", 28, TEXT).move_to(P(0, 2.55))
        lt = S.lab_tip()
        self.play(drain(S.dots_tip, 1.0), FadeIn(lt, shift=DOWN * 0.1, run_time=0.2),
                  FadeIn(cap, shift=DOWN * 0.1, run_time=0.2))
        self.at("cell body keeps it")
        ls = S.lab_soma()
        self.play(Indicate(S.dots_soma, color=YELLOW, scale_factor=1.25), Indicate(S.soma, color=GREEN, scale_factor=1.12),
                  FadeIn(ls, shift=UP * 0.1), run_time=0.9)
        self.at("the axons degenerate")
        chip_a = chip("axons degenerate", RED, size=26, pad=0.16).move_to(P(4.6, 0.45))
        chip_a[1].set_color(TEXT)
        shatter(self, [], S.movers, 6, rt=1.0, spread=0.2,
                extra=[FadeIn(chip_a, shift=LEFT * 0.1), *[st.animate.set_color(RED).set_opacity(0.6) for st in S.stems]])
        self.at("the neuron lives")
        chip_b = chip("neuron lives", GREEN, size=26, pad=0.16).move_to(P(4.6, -0.85))
        chip_b[1].set_color(TEXT)
        self.play(FadeIn(chip_b, shift=LEFT * 0.1), S.soma.animate.set_stroke(GREEN), run_time=0.2)
        self.finish()


class S16Rule3(SpokenScene):
    def construct(self):
        top = rule_one_line()
        self.add(top)
        # the surviving neuron from scene 15, redrawn smaller on the upper half
        A = Strip(1.2, 0.7)
        A.soma.set_stroke(GREEN)
        frag_now(A.movers, 6, 0.15)
        for st in A.stems:
            dim_red(st)
        ca = chip("axons degenerate", RED, size=26, pad=0.16).move_to(P(4.6, 1.75))
        cb = chip("neuron lives", GREEN, size=26, pad=0.16).move_to(P(4.6, 0.65))
        ca[1].set_color(TEXT)
        cb[1].set_color(TEXT)
        capA = T("axons lose support, the cell body keeps it", 26, TEXT).move_to(P(-0.6, 2.7))
        # the neuron that loses support everywhere
        B = Strip(-1.75, 0.7)
        self.at("Lose it everywhere")
        self.play(FadeIn(A.soma), FadeIn(VGroup(*A.parts)), FadeIn(ca), FadeIn(cb), FadeIn(capA),
                  FadeIn(B.soma, scale=0.7), *[Create(a) for a in B.parts], FadeIn(B.tipdots), FadeIn(B.dots_soma),
                  FadeIn(B.dots_tip), run_time=0.45)
        self.at("everywhere")
        lb = T("no NGF anywhere", 28, YELLOW, weight=BOLD).move_to(P(-2.6, -2.95))
        self.play(drain(B.dots_soma, 0.6), drain(B.dots_tip, 0.6), FadeIn(lb, shift=UP * 0.1, run_time=0.15))
        self.at("the neuron dies")
        chip_c = chip("neuron dies", RED, size=26, pad=0.16).move_to(P(4.6, -1.75))
        shatter(self, [], B.movers, 9, rt=0.6, spread=0.15,
                extra=[*[st.animate.set_color(RED).set_opacity(0.6) for st in B.stems],
                       B.soma.animate.set_stroke(RED, opacity=0.5).set_fill(RED, 0.25), FadeIn(chip_c, shift=LEFT * 0.1)])
        self.finish()


# ---------------------------------------------------------------------------------------------
def break_mark(x, y):
    cut = Rectangle(width=0.55, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(P(x, y))
    l1 = Line(P(x - 0.27 - 0.12, y - 0.3), P(x - 0.27 + 0.12, y + 0.3), color=TEXT, stroke_width=4)
    l2 = Line(P(x + 0.27 - 0.12, y - 0.3), P(x + 0.27 + 0.12, y + 0.3), color=TEXT, stroke_width=4)
    return VGroup(cut, l1, l2)


class S17Scale(SpokenScene):
    def construct(self):
        # the cell body sits far from the target: long trunk with a break in it
        N = Neuron(soma=(-5.7, 0.0), trunk_end=(-1.2, 0.0), tip_x=3.9, r=0.7, dend=False)
        tgt = target_block()
        tl = target_label()
        brk = break_mark(-3.3, 0.0)
        self.add(tgt, tl, N.all(), brk)
        self.at("In the animal")
        lab = T("in the animal", 30, TEXT, weight=BOLD).move_to(P(-4.6, 3.4))
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.at("target NGF")
        d = target_dots_at(5.7)
        ng = T("NGF", 28, YELLOW, weight=BOLD).move_to(P(5.55, -3.42))
        taken = T("NGF taken up at the axon tips", 26, YELLOW).move_to(P(1.6, 3.4))
        sig_lab = T("signal to the cell body", 28, SIGNAL, weight=BOLD).move_to(P(-3.0, -0.85))
        self.play(FadeIn(ng), FadeIn(d), run_time=0.25)
        self.play(*[x.animate.move_to(P(4.2, y)) for x, y in zip(d, YS7)],
                  FadeIn(taken, shift=DOWN * 0.1, run_time=0.2), run_time=0.55)
        self.at("normally reaches")
        self.play(FadeIn(sig_lab, shift=UP * 0.1), run_time=0.25)
        self.at("the cell body")
        cb = T("cell body", 26, TEXT, weight=BOLD).move_to(P(-5.7, 1.2))
        far = T("far from the target", 26, SOFT).move_to(P(-3.0, 0.85))
        self.play(Indicate(N.body, color=TEXT, scale_factor=1.2), FadeIn(cb, shift=DOWN * 0.1),
                  FadeIn(far, shift=DOWN * 0.1), run_time=0.9)
        self.at("signals")
        movers = []
        for c, tp, dd in zip(N.curves, N.tip_pts, d):
            rev = c.copy().reverse_points()
            tr = N.trunk.copy().reverse_points()
            path = VMobject()
            path.append_points(Line(dd.get_center(), tp).points)
            path.append_points(rev.points)
            path.append_points(tr.points)
            movers.append((dd, path))
        main = T("the main route of target-derived support", 26, SIGNAL).move_to(P(-1.4, -3.35))

        def mk(path):
            def f(m, a):
                m.move_to(path.point_from_proportion(a))
                k = min(1.0, a * 10)
                m.set_fill(interpolate_color(ManimColor(YELLOW), ManimColor(SIGNAL), k), opacity=1)
                m.set_stroke(TEXT, 3 * k)
                m.set_width(0.2 + 0.18 * k)
            return f
        self.play(*[UpdateFromAlphaFunc(dd, mk(pth), run_time=3.0, rate_func=linear) for dd, pth in movers],
                  FadeOut(taken, run_time=0.4),
                  Succession(Wait(1.15), FadeIn(main, shift=UP * 0.1, run_time=0.6)))
        self.finish()


# ---------------------------------------------------------------------------------------------
PCX_L, PCX_R, PCY, PK = -3.3, 3.5, 1.25, 0.85
LOST_STACK_L = -2.2


def panel_parts():
    """Branch bases stay put (they overlap at the fork); only the outer pieces break apart, so nothing tangles."""
    L = mini(PCX_L, PCY, k=PK)
    R = mini(PCX_R, PCY, k=PK)
    pl = pieces_of(L.curves[2], 6)
    stem_l, pcs_l = pl[0], pl[1:]
    stems_r, pcs_r = [], []
    for c in R.curves:
        pr = pieces_of(c, 6)
        stems_r.append(pr[0])
        pcs_r += pr[1:]
    return L, R, stem_l, pcs_l, stems_r, pcs_r


def death_panel_targets(pcs):
    targets = []
    for i, part in enumerate(pcs):
        row, col = divmod(i, 5)
        t = part.copy().scale(0.62)
        t.shift(P(0.12 + 0.035 * col, (1 - row) * 0.12))
        t.set_color(RED).set_opacity(0.6)
        targets.append(t)
    return targets


def death_stem_targets(stems):
    return [s.copy().scale(0.45).shift(P(0.04, (1 - i) * 0.12)).set_color(RED).set_opacity(0.6)
            for i, s in enumerate(stems)]


def dim_red(m):
    m.set_color(RED).set_opacity(0.6)
    return m


def panel_dots(L):
    soma = L.soma_pt
    ds = [Dot(P(soma[0], PCY + 0.9), radius=0.1, color=YELLOW), Dot(P(soma[0] - 0.4, PCY - 0.9), radius=0.1, color=YELLOW)]
    ds += [Dot(L.tip_pts[i] + P(0.38, 0), radius=0.1, color=YELLOW) for i in (0, 1)]
    return VGroup(*ds)


def panel_titles():
    tl = T("pruning: one branch lost", 28, TEXT).move_to(P(PCX_L, 3.3))
    tr = T("death: the whole neuron lost", 28, TEXT).move_to(P(PCX_R, 3.3))
    return tl, tr


def route_stack(x, text, y_tag=-0.95, y_chip=-2.05):
    """tag 'no NGF' -> arrow -> route chip, drawn in the colours of the colour map."""
    ar = Arrow(P(x, y_tag - 0.27), P(x, y_chip + 0.45), color=SIGNAL, buff=0, stroke_width=5,
               max_tip_length_to_length_ratio=0.4)
    ch = chip(text, SIGNAL, size=26, pad=0.16).move_to(P(x, y_chip))
    return ar, ch


class S18Scale2(SpokenScene):
    def construct(self):
        L, R, stem_l, pcs_l, stems_r, pcs_r = panel_parts()
        div = DashedLine(P(0, -2.85), P(0, 3.5), color=GREY, stroke_width=2)
        dl = panel_dots(L)
        self.add(div, L.core(), R.core(), *L.curves, *L.tipdots, *R.curves, *R.tipdots, dl)
        self.at("pruning")
        tl, tr = panel_titles()
        tag_l = no_ngf(LOST_STACK_L, -0.95)
        self.remove(L.curves[2])
        self.add(stem_l, *pcs_l)
        tg = frag_targets(pcs_l, 21, 0.2)
        self.play(*[Transform(p, t) for p, t in zip(pcs_l, tg)], FadeOut(L.tipdots[2]),
                  FadeIn(tl, shift=DOWN * 0.1), FadeIn(tag_l, shift=DOWN * 0.1), run_time=0.5)
        self.at("death")
        tag_r = no_ngf(PCX_R, -0.95, "no NGF anywhere")
        self.remove(*R.curves)
        self.add(*stems_r, *pcs_r)
        tg = death_panel_targets(pcs_r)
        self.play(*[Transform(p, t) for p, t in zip(pcs_r, tg)], FadeOut(VGroup(*R.tipdots)),
                  *[Transform(s_, t) for s_, t in zip(stems_r, death_stem_targets(stems_r))],
                  R.trunk.animate.set_color(RED).set_opacity(0.6),
                  R.body.animate.set_stroke(RED, opacity=0.5).set_fill(RED, 0.25).scale(0.8),
                  FadeIn(tr, shift=DOWN * 0.1), FadeIn(tag_r, shift=DOWN * 0.1), run_time=0.8)
        self.at("same rule")
        sr = T("same rule", 30, TEXT, weight=BOLD).move_to(P(0, -3.4))
        self.play(FadeIn(sr, shift=UP * 0.1), run_time=0.6)
        self.at("wired differently")
        ar_l, ch_l = route_stack(LOST_STACK_L, "local route")
        ar_r, ch_r = route_stack(PCX_R, "whole-cell route")
        full = T("same rule, differently wired routes", 30, TEXT, weight=BOLD).move_to(P(0, -3.4))
        self.play(GrowArrow(ar_l), GrowArrow(ar_r), FadeIn(ch_l, shift=UP * 0.1), FadeIn(ch_r, shift=UP * 0.1),
                  run_time=0.8)
        self.play(FadeOut(sr), run_time=0.2)
        self.remove(sr)
        self.play(FadeIn(full), run_time=0.3)
        self.finish()


def panels_state(scene):
    L, R, stem_l, pcs_l, stems_r, pcs_r = panel_parts()
    div = DashedLine(P(0, -2.85), P(0, 3.5), color=GREY, stroke_width=2)
    dl = panel_dots(L)
    R.trunk.set_color(RED).set_opacity(0.6)
    scene.add(div, L.core(), R.core(), L.curves[0], L.curves[1], L.tipdots[0], L.tipdots[1], dl)
    for s_, t in zip(stems_r, death_stem_targets(stems_r)):
        s_.become(t)
    scene.add(stem_l, *pcs_l, *stems_r, *pcs_r)
    frag_now(pcs_l, 21, 0.2)
    for p, t in zip(pcs_r, death_panel_targets(pcs_r)):
        p.become(t)
    R.body.set_stroke(RED, opacity=0.5).set_fill(RED, 0.25).scale(0.8)
    tl, tr = panel_titles()
    tag_l = no_ngf(LOST_STACK_L, -0.95)
    tag_r = no_ngf(PCX_R, -0.95, "no NGF anywhere")
    ar_l, ch_l = route_stack(LOST_STACK_L, "local route")
    ar_r, ch_r = route_stack(PCX_R, "whole-cell route")
    full = T("same rule, differently wired routes", 30, TEXT, weight=BOLD).move_to(P(0, -3.4))
    scene.add(tl, tr, tag_l, tag_r, ar_l, ar_r, ch_l, ch_r, full)
    return L, R, full


class S19Casp(SpokenScene):
    def construct(self):
        L, R, full = panels_state(self)
        self.at("Both use caspases")
        yS = -3.15
        sl = scissors(LOST_STACK_L - 0.95, yS, 0.9)
        sr = scissors(PCX_R - 0.95, yS, 0.9)
        cl = T("caspases", 26, VIOLET, weight=BOLD).move_to(P(LOST_STACK_L + 0.65, yS))
        cr = T("caspases", 26, VIOLET, weight=BOLD).move_to(P(PCX_R + 0.65, yS))
        al = Arrow(P(LOST_STACK_L, -2.5), P(LOST_STACK_L, -2.8), color=SIGNAL, buff=0, stroke_width=5,
                   max_tip_length_to_length_ratio=0.5)
        ar = Arrow(P(PCX_R, -2.5), P(PCX_R, -2.8), color=SIGNAL, buff=0, stroke_width=5,
                   max_tip_length_to_length_ratio=0.5)
        self.play(FadeOut(full), FadeIn(sl, scale=0.6), FadeIn(sr, scale=0.6), FadeIn(cl, shift=LEFT * 0.1),
                  FadeIn(cr, shift=LEFT * 0.1), GrowArrow(al), GrowArrow(ar), run_time=1.0)
        self.at("the enzymes of cell death")
        self.play(Indicate(VGroup(sl, cl), color=VIOLET, scale_factor=1.15),
                  Indicate(VGroup(sr, cr), color=VIOLET, scale_factor=1.15), run_time=1.0)
        self.at("So how can")
        q = qmark(0.6, -3.0, 64, TEXT)
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.at("use them")
        self.play(Indicate(VGroup(sl, cl), color=VIOLET, scale_factor=1.15), run_time=0.5)
        self.at("and the neuron live")
        self.play(Indicate(L.body, color=GREEN, scale_factor=1.25), L.body.animate.set_stroke(GREEN), run_time=0.9)
        self.finish()


class S20Scope(SpokenScene):
    def construct(self):
        CXL, CXR, CY = -3.3, 3.3, -0.45
        rule = T("Where support is lost decides what is lost.", 30, GOLD, font=TITLE_FONT).move_to(P(0, 3.1))
        card_l = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.9, stroke_color=GREEN, stroke_width=3,
                                  fill_opacity=0).move_to(P(CXL, CY))
        hl = T("after support is lost", 28, TEXT).move_to(P(CXL, 1.95))
        YS = (2.4, 0.0, -2.4)
        NL = mini(CXL, -0.9, k=0.85, ys=YS)
        dl = VGroup(*[Dot(P(CXL + 2.6 * 0.85 + 0.45, -0.9 + y * 0.85), radius=0.1, color=YELLOW) for y in YS])
        card_r = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.9, stroke_color=GREY, stroke_width=3,
                                  fill_opacity=0).move_to(P(CXR, CY))
        hr = T("on a fixed program", 28, TEXT).move_to(P(CXR, 1.95))
        NR = mini(CXR, -0.9, k=0.85, ys=YS)
        fc = P(CXR - 2.3, 1.1)
        face = Circle(radius=0.5, stroke_color=TEXT, stroke_width=4, fill_opacity=0).move_to(fc)
        ticks = VGroup(*[Line(fc + P(np.cos(a), np.sin(a)) * 0.38, fc + P(np.cos(a), np.sin(a)) * 0.5, color=TEXT,
                              stroke_width=3) for a in (0, PI / 2, PI, 3 * PI / 2)])
        hand = Line(fc, fc + P(0, 0.36), color=TEXT, stroke_width=5)
        clock = VGroup(face, ticks, hand)
        card_r.set_stroke(opacity=0.5)
        hr.set_opacity(0.55)
        self.at("This rule covers")
        self.play(FadeIn(rule, shift=DOWN * 0.1), Create(card_l), FadeIn(hl, shift=DOWN * 0.1), FadeIn(NL.all()),
                  FadeIn(dl), FadeIn(card_r), FadeIn(hr), FadeIn(NR.all()), FadeIn(clock), run_time=0.9)
        self.at("branches lost")
        self.play(Indicate(NL.branch_group(), color=GREEN, scale_factor=1.0), run_time=0.8)
        self.at("after support")
        self.play(drain(dl, 0.9))
        self.at("is lost")
        pcs = pieces_of(NL.curves[2], 5)
        shatter(self, [NL.curves[2]], pcs, 31, rt=0.9, spread=0.2, extra=[FadeOut(NL.tipdots[2])])
        self.at("Some branches go")
        self.play(card_r.animate.set_stroke(opacity=1.0), hr.animate.set_opacity(1.0), run_time=0.6)
        self.at("fixed program")
        self.play(Rotate(hand, angle=-TAU, about_point=fc, rate_func=linear), run_time=1.3)
        pcr = pieces_of(NR.curves[2], 5)
        shatter(self, [NR.curves[2]], pcr, 32, rt=0.8, spread=0.2, extra=[FadeOut(NR.tipdots[2])])
        self.at("Those come later")
        later = chip("comes later", TEXT, size=28, pad=0.16).move_to(P(CXR + 0.1, 1.2))
        self.play(FadeIn(later, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


class S21Take(SpokenScene):
    def construct(self):
        a = T("To predict what is lost,", 52, TEXT, font=TITLE_FONT)
        b = T("ask where support was lost.", 52, TEXT, font=TITLE_FONT, t2c={"where support was lost": GOLD})
        g = VGroup(a, b).arrange(DOWN, buff=0.4).move_to(P(0, 0))
        fit(g, max_w=12.0)
        self.at("to predict")
        self.play(Write(g[0]), run_time=1.3)
        self.at("first ask")
        self.play(Write(g[1]), run_time=1.5)
        self.finish()


class S22End(EndCard):
    LINE = "To predict what is lost, ask where support was lost."
