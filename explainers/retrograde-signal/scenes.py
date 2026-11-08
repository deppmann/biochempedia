"""Still On When It Gets There (chapter 1 of "The Signal from the Target Travels Home")  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
(sync.log: "now" is the time the scene reached the cue; when it is earlier than "at", the scene waits, so a
label never lands before its word. Only "late" values above zero are real lateness.)

COLOR MAP (one color per concept, the same in every chapter; taken from scenes.old.py, two hues separated in the fix round)
  YELLOW = NGF, the target's factor (and the target that makes it)
  ORANGE = a phosphate badge (was GOLD: too close to NGF yellow). NT-3 later chapters: draw it in another hue, not orange.
  BLUE   = TrkA, the receptor (TRKA below is a deeper blue so it is not confused with the teal vesicle)
  TEAL   = the carried signal: the signaling endosome, the vehicle, the trip
  PINK   = dynein, the motor
  PURPLE = the nucleus
  GREEN  = a signal that is able to signal (switched on, lit); dimmed green = on but weaker
  RED    = bad outcome only: too slow, switched off, crossed out, death genes, the phosphatase
  GREY   = the neuron's outline, axes, labels, microtubule, a switched-off molecule
  TEXT   = the diffusion curve and neutral marks
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB8"
TRKA = "#6C8CFF"
PHOS = ORANGE
LBL = "#C9CED8"          # label grey: brighter than GREY so labels read on the dark ground
SOLID = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.17)
DIMG = interpolate_color(ManimColor(BG), ManimColor(GREEN), 0.45)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def V(x, y=0.0):
    return np.array([x, y, 0.0])


def clip01(a):
    return float(min(max(a, 0.0), 1.0))


def dot(pos, color, r=0.17, op=1.0):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(pos)


def hal(pos, color, r=0.4, op=0.28):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to(pos)


def lit(pos, color=GREEN, r=0.17):
    """A glowing molecule: two soft halos and a bright core. Returns VGroup(halo1, halo2, core)."""
    return VGroup(hal(pos, color, r * 2.7, 0.16), hal(pos, color, r * 1.7, 0.28), dot(pos, color, r))


def set_lit(m, g, color=GREEN, off=GREY):
    """Dim a lit() molecule: g=1 fully lit, g=0 switched off (core in `off`, no halo)."""
    g = clip01(g)
    col = interpolate_color(ManimColor(off), ManimColor(color), g)
    m[0].set_fill(color, 0.16 * g)
    m[1].set_fill(color, 0.28 * g)
    m[2].set_stroke(col, 2).set_fill(col, 0.7 + 0.3 * g)


def tick(c, color=GREEN, s=0.4, w=9):
    c = np.array(c, float)
    return VMobject(color=color, stroke_width=w).set_points_as_corners(
        [c + V(-s * 0.9, 0), c + V(-s * 0.3, -s * 0.7), c + V(s * 1.0, s * 0.8)])


def cross(c, color=RED, s=0.4, w=9):
    c = np.array(c, float)
    return VGroup(Line(c + V(-s, -s), c + V(s, s), color=color, stroke_width=w),
                  Line(c + V(-s, s), c + V(s, -s), color=color, stroke_width=w))


def pbadge(pos, r=0.3):
    c = Circle(radius=r, stroke_color=PHOS, stroke_width=3, fill_color=PHOS, fill_opacity=1).move_to(pos)
    return VGroup(c, T("P", 26, BG, weight=BOLD).move_to(c))


def dash_arrow(a, b, color=TEXT, w=4, n=26):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    ang = np.arctan2(d[1], d[0])
    line = DashedVMobject(Line(a, b - d * 0.1), num_dashes=n, dashed_ratio=0.55).set_stroke(color, w)
    tip = Triangle(fill_opacity=1, color=color, stroke_width=0).scale(0.17).rotate(ang - PI / 2).move_to(b - d * 0.14)
    return VGroup(line, tip)


def qmark(pos, color=TEXT, r=0.5, size=56):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(pos)
    return VGroup(c, T("?", size, color, weight=BOLD).move_to(c))


def leader(a, b, color=LBL, w=2.5):
    return Line(np.array(a, float), np.array(b, float), color=color, stroke_width=w)


def lab(text, pos, size=26, color=LBL, edge=None, **kw):
    t = T(text, size, color, **kw)
    return t.move_to(pos, aligned_edge=edge) if edge is not None else t.move_to(pos)


def clock_tracker(scene):
    """A ValueTracker that counts scene seconds from the moment it is added."""
    c = ValueTracker(0.0)
    c.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(c)
    return c


# ---------------------------------------------------------------------------------------------
# the neuron: cell body at left, long axon with a break marker, three terminals reaching an organ at right.
# Scaled by S so the cell body and the organ sit inside the safe frame (x within +-6.3).
# ---------------------------------------------------------------------------------------------
SC = [(6.0, 1.9), (6.45, 1.0), (6.0, 0.5), (6.45, -0.4), (6.0, -1.2), (6.45, -1.9)]    # scattered in the organ


class Rig:
    S = 0.92

    def __init__(self, cy=0.0):
        self.cy = cy
        S = self.S
        R = lambda x, y=0.0: np.array([x, y, 0.0])
        parts = [Circle(radius=1.4).move_to(R(-5.3)),
                 RoundedRectangle(corner_radius=0.575, width=8.6, height=1.15).move_to(R(-1.0))]
        self.ends = [(4.5, 1.65), (4.7, 0.0), (4.5, -1.65)]
        for ex, ey in self.ends:
            a, b = np.array([3.3, 0.0]), np.array([ex, ey])
            v = b - a
            br = RoundedRectangle(corner_radius=0.21, width=float(np.linalg.norm(v)), height=0.42)
            br.rotate(float(np.arctan2(v[1], v[0]))).move_to(R((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
            parts += [br, Circle(radius=0.34).move_to(R(ex, ey))]
        cell = Union(*parts).set_stroke(GREY, 3).set_fill(SOLID, 1)
        bx = -0.9
        poly = Polygon(R(bx - 0.2, -0.8), R(bx + 0.05, 0.8), R(bx + 0.45, 0.8), R(bx + 0.2, -0.8),
                       stroke_width=0, fill_color=BG, fill_opacity=1)
        brk = VGroup(poly, Line(R(bx - 0.2, -0.8), R(bx + 0.05, 0.8), color=GREY, stroke_width=3),
                     Line(R(bx + 0.2, -0.8), R(bx + 0.45, 0.8), color=GREY, stroke_width=3))
        nuc = Circle(radius=0.78, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to(R(-5.3))
        block = RoundedRectangle(corner_radius=0.15, width=0.9, height=4.8, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.14).move_to(R(6.25))
        self.cell, self.brk, self.nuc, self.block = [
            m.scale(S, about_point=ORIGIN).shift(UP * cy) for m in (cell, brk, nuc, block)]
        self.blk_lbl = T("target\norgan", 26, YELLOW, line_spacing=0.8).move_to(self.P(6.25, -3.15))

    def P(self, x, y=0.0):
        return np.array([self.S * x, self.cy + self.S * y, 0.0])

    def tips(self):
        return [self.P(x, y) for x, y in self.ends]

    def dots(self, gathered=False):
        if gathered:      # two NGF dots at each terminal tip
            pts = [(ex + 0.55, ey + dy) for ex, ey in self.ends for dy in (0.2, -0.2)]
        else:
            pts = SC
        return VGroup(*[dot(self.P(x, y), YELLOW, 0.14) for x, y in pts])

    def add_to(self, scene, block=True, label=True, nuc=True):
        if block:
            scene.add(self.block)
            if label:
                scene.add(self.blk_lbl)
        scene.add(self.cell, self.brk)
        if nuc:
            scene.add(self.nuc)


def endo(pos, sc=1.0, glow=1.0):
    """A signaling endosome icon: teal bubble holding a receptor bar and the factor. VGroup(halo, bubble, bar, dot)."""
    halo = hal(pos, TEAL, 0.75 * sc, 0.22 * glow)
    bubble = Circle(radius=0.42 * sc, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.18).move_to(pos)
    bar = RoundedRectangle(corner_radius=0.07 * sc, width=0.2 * sc, height=0.52 * sc, stroke_color=TRKA, stroke_width=2,
                           fill_color=TRKA, fill_opacity=0.9).move_to(pos + V(-0.1 * sc, 0))
    d = dot(pos + V(0.13 * sc, 0.02 * sc), YELLOW, 0.11 * sc)
    return VGroup(halo, bubble, bar, d)


def cell_icon(pos, r=1.0, alive=False):
    body = Circle(radius=r, stroke_color=GREEN if alive else GREY, stroke_width=4, fill_color=SOLID, fill_opacity=1).move_to(pos)
    nuc = Circle(radius=r * 0.42, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to(pos)
    return VGroup(body, nuc)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Signal from the Target Travels Home"
    TITLE = "Still On When It Gets There"


# ---------------------------------------------------------------------------------------------
QY = 1.4     # height of the arrow and question mark above the axon


class S01Q(SpokenScene):
    """The picture of the puzzle: a neuron with a very long axon, a signal at the far end, no known path home."""

    def construct(self):
        r = Rig(0.0)
        P = r.P
        dots = r.dots()
        self.at("a neuron", lead=0.0)
        self.play(DrawBorderThenFill(r.cell), FadeIn(r.block), FadeIn(r.blk_lbl), FadeIn(r.brk), FadeIn(r.nuc), run_time=1.0)
        self.at("survival signal")
        sl = T("survival\nsignal", 26, YELLOW, line_spacing=0.8).move_to(P(6.25, 3.0))
        self.play(FadeIn(dots, scale=0.6), FadeIn(sl), run_time=0.7)
        self.at("far end")
        self.play(*[Flash(p, color=YELLOW, flash_radius=0.65, line_length=0.2, run_time=0.6) for p in r.tips()])
        self.at("axon")
        axl = lab("axon", P(-2.8, -1.05), 28, LBL)
        self.play(FadeIn(axl), run_time=0.4)
        self.at("how does the message")
        arr = dash_arrow(P(3.6, QY), P(-4.0, QY), TEXT)
        self.play(Create(arr), run_time=0.7, rate_func=linear)
        q = qmark(P(-0.2, QY))
        self.play(FadeIn(q, scale=0.6), run_time=0.3)
        self.at("get home")
        nts = lab("not to scale", P(0.0, -1.05), 26, LBL)
        self.play(FadeIn(nts), Indicate(r.nuc, color=PURPLE, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s01_end(scene, r):
    """Rebuild the last frame of s01 (carried into s02). Returns the dots, the NGF caption and the labels to clear."""
    P = r.P
    r.add_to(scene)
    dots = r.dots()
    sl = T("survival\nsignal", 26, YELLOW, line_spacing=0.8).move_to(P(6.25, 3.0))
    axl = lab("axon", P(-2.8, -1.05), 28, LBL)
    nts = lab("not to scale", P(0.0, -1.05), 26, LBL)
    arr = dash_arrow(P(3.6, QY), P(-4.0, QY), TEXT)
    q = qmark(P(-0.2, QY))
    scene.add(dots, sl, axl, nts, arr, q)
    return dots, sl, VGroup(axl, nts, arr, q)


def s02_labels(r):
    P = r.P
    sym = lab("sympathetic neuron", P(-1.8, 1.45), 28, TEXT)
    tl = VGroup(lab("axon terminals", P(2.7, 2.75), 26, LBL), leader(P(3.5, 2.5), P(4.3, 1.95)))
    cb = lab("cell body", P(-5.3, -2.35), 28, LBL)
    return sym, tl, cb


def s02_bar(r):
    P = r.P
    bar = DoubleArrow(P(-4.1, -1.25), P(3.3, -1.25), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
    cm = T("centimetres: 1 to a few cm", 28, TEXT).move_to(P(-0.4, -1.95))
    return bar, cm


class S02Tip(SpokenScene):
    """NGF gathers at the axon terminals; a scale bar says the axon is centimetres long."""

    def construct(self):
        r = Rig(0.0)
        P = r.P
        dots, sl, old = s01_end(self, r)
        self.play(FadeOut(old), run_time=0.4)
        sym, tl, cb = s02_labels(r)
        self.at("a sympathetic neuron", lead=0.0)
        self.play(FadeIn(sym, shift=DOWN * 0.1), run_time=0.5)
        self.at("ngf")
        ngf = T("NGF", 32, YELLOW, weight=BOLD).move_to(P(6.25, 3.0))
        gathered = r.dots(True)
        self.play(ReplacementTransform(sl, ngf),
                  *[d.animate.move_to(g.get_center()) for d, g in zip(dots, gathered)], run_time=1.1)
        self.at("axon terminals")
        self.play(*[Flash(p, color=YELLOW, flash_radius=0.6, line_length=0.2, run_time=0.9) for p in r.tips()],
                  FadeIn(tl), run_time=0.9)
        self.at("centimeters")
        bar, cm = s02_bar(r)
        self.play(GrowFromCenter(bar), FadeIn(cm), run_time=0.9)
        self.at("cell body")
        self.play(FadeIn(cb), Indicate(r.nuc, color=PURPLE, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s02_end(scene, r):
    P = r.P
    r.add_to(scene)
    dots = r.dots(True)
    ngf = T("NGF", 32, YELLOW, weight=BOLD).move_to(P(6.25, 3.0))
    sym, tl, cb = s02_labels(r)
    bar, cm = s02_bar(r)
    scene.add(dots, ngf, sym, tl, cb, bar, cm)
    return dots, ngf, VGroup(bar, cm), VGroup(sym, tl, cb)


def switch(r, knob_x=0.5):
    P = r.P
    track = RoundedRectangle(corner_radius=0.25, width=2.6, height=0.5, stroke_color=GREY, stroke_width=3,
                             fill_color=SOLID, fill_opacity=1).move_to(P(-5.2, 2.3))
    die = T("die", 28, RED, weight=BOLD).move_to(P(-6.0, 2.95))
    live = T("live", 28, GREEN, weight=BOLD).move_to(P(-4.4, 2.95))
    knob = Circle(radius=0.3, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=1).move_to(
        P(-6.0 + 1.6 * knob_x, 2.3))
    link = DashedVMobject(Line(P(-5.2, 0.7), P(-5.2, 2.0)), num_dashes=6).set_stroke(PURPLE, 3)
    return VGroup(track, die, live, link), knob


class S03Decide(SpokenScene):
    """The terminal hears the factor, but the nucleus decides: a live-or-die switch beside it."""

    def construct(self):
        r = Rig(0.0)
        P = r.P
        dots, ngf, old, keep = s02_end(self, r)
        self.play(FadeOut(old), run_time=0.5)
        self.at("the terminal hears", lead=0.0)
        self.play(*[Flash(p, color=YELLOW, flash_radius=0.7, line_length=0.25, run_time=1.2) for p in r.tips()])
        self.at("nucleus")
        halo = hal(P(-5.3), PURPLE, 1.05, 0.3)
        self.add(halo)
        self.bring_to_front(r.nuc)
        self.play(FadeIn(halo, scale=0.5), Indicate(r.nuc, color=PURPLE, scale_factor=1.25), run_time=0.5)
        self.at("decides")
        sw, knob = switch(r)
        self.play(FadeIn(sw), FadeIn(knob), run_time=0.4)
        self.at("whether the cell lives")
        self.play(knob.animate.move_to(P(-4.4, 2.3)), run_time=0.7)
        self.play(knob.animate.move_to(P(-6.0, 2.3)), run_time=0.7)
        self.play(knob.animate.move_to(P(-5.2, 2.3)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Genes(SpokenScene):
    """Dying needs new genes switched on in the nucleus, so the survival signal must reach the cell body."""

    def construct(self):
        r = Rig(0.0)
        P = r.P
        r.add_to(self)
        dots = r.dots(True)
        ngf = T("NGF", 32, YELLOW, weight=BOLD).move_to(P(6.25, 3.0))
        halo = hal(P(-5.3), PURPLE, 1.05, 0.3)
        sw, knob = switch(r)
        sym, tl, cb = s02_labels(r)
        self.add(dots, ngf, halo, sw, knob, tl, cb)
        self.bring_to_front(r.nuc)
        self.play(FadeOut(VGroup(sw, knob)), run_time=0.4)
        self.at("in these young neurons", lead=0.0)
        scope = T("young sympathetic neurons, NGF at the axon tips", 28, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(scope, shift=DOWN * 0.1), run_time=0.6)
        self.at("new genes")
        genes = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.11, height=0.42, stroke_color=GREY, stroke_width=2,
                                          fill_color=GREY, fill_opacity=0.6).move_to(P(-5.3 + dx, dy))
                         for dx, dy in [(-0.34, 0.12), (-0.17, -0.1), (0.0, 0.14), (0.17, -0.1), (0.34, 0.12)]])
        self.play(FadeIn(genes), run_time=0.5)
        self.at("switched on")
        gl = T("death genes switched on", 28, RED).move_to(P(-4.5, 2.45))
        self.play(*[g.animate.set_stroke(RED).set_fill(RED, 1) for g in genes], FadeIn(gl),
                  halo.animate.set_color(RED), run_time=0.8)
        self.at("so a survival signal")
        self.play(*[Flash(p, color=YELLOW, flash_radius=0.6, line_length=0.2, run_time=0.8) for p in r.tips()])
        self.at("from the tip")
        arr = dash_arrow(P(3.6, QY), P(-4.0, QY), TEXT)
        self.play(Create(arr), run_time=1.3, rate_func=linear)
        self.at("act on")
        q = qmark(P(-0.2, QY))
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("cell body")
        self.play(Indicate(r.cell, color=TEXT, scale_factor=1.03), Indicate(r.nuc, color=PURPLE, scale_factor=1.3),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
RULE_Y = (3.45, 2.65, 1.95, 1.25)      # heading, line1, line2, line3
PY = -0.85                             # y of the pictogram


def rule_lines():
    h = T("The idea to carry through", 28, TEAL).move_to([0, RULE_Y[0], 0])
    l1 = T("A target keeps a neuron alive", 38, TEXT, font=TITLE_FONT).move_to([0, RULE_Y[1], 0])
    l2 = T("only if its signal makes the trip home", 38, TEAL, font=TITLE_FONT).move_to([0, RULE_Y[2], 0])
    l3 = T("and is able to signal when it gets there", 38, GREEN, font=TITLE_FONT).move_to([0, RULE_Y[3], 0])
    return h, l1, l2, l3


def pictogram(alive=False):
    blk = RoundedRectangle(corner_radius=0.14, width=1.2, height=2.6, stroke_color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.14).move_to(V(-5.3, PY))
    bl = T("target", 28, YELLOW).move_to(V(-5.3, PY - 1.75))
    icon = cell_icon(V(4.7, PY), 1.25, alive)
    il = T("kept alive" if alive else "neuron", 28, GREEN if alive else LBL).move_to(V(4.7, PY - 1.75))
    path = Arrow(V(-4.5, PY), V(3.2, PY), buff=0, color=GREY, stroke_width=4, tip_length=0.24)
    return blk, bl, icon, il, path


class S05Rule(SpokenScene):
    """The rule, first half: a target keeps a neuron alive only if its signal makes the trip home."""

    def construct(self):
        h, l1, l2, l3 = rule_lines()
        blk, bl, icon, il, path = pictogram()
        self.at("here is the idea", lead=0.0)
        self.play(FadeIn(h, shift=DOWN * 0.1), FadeIn(blk), FadeIn(bl), FadeIn(icon), FadeIn(il), run_time=0.7)
        self.at("target keeps")
        self.play(FadeIn(l1, shift=UP * 0.1), Indicate(blk, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("alive")
        il2 = T("kept alive", 28, GREEN).move_to(il)
        self.play(icon[0].animate.set_stroke(GREEN), FadeOut(il), FadeIn(il2), run_time=0.6)
        self.at("only if")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        self.at("its signal")
        sig = lit(V(-3.8, PY), YELLOW, 0.22)
        self.play(Create(path), FadeIn(sig, scale=0.6), run_time=0.5)
        self.at("makes the trip")
        self.play(sig.animate.move_to(V(2.9, PY)), run_time=max(1.0, self.t_of("home") + 0.6 - self.elapsed()),
                  rate_func=linear)
        self.finish()


class S06Rule2(SpokenScene):
    """The rule, second half: able to signal when it gets there; binding at the tip is not enough."""

    def construct(self):
        h, l1, l2, l3 = rule_lines()
        blk, bl, icon, il, path = pictogram(True)
        self.add(h, l1, l2, blk, bl, icon, il, path)
        sig = lit(V(2.9, PY), YELLOW, 0.22)
        self.add(sig)
        self.at("it must be able", lead=0.0)
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.7)
        self.at("gets there")
        self.play(*[sig[i].animate.set_color(GREEN) for i in range(3)], run_time=0.5)
        self.at("on when it arrives")
        on = T("ON when it arrives", 30, GREEN, weight=BOLD).move_to(V(1.0, PY - 1.8))
        tk = tick(V(2.9, PY + 0.62), GREEN, 0.28, 8)
        self.play(FadeIn(on), Create(tk), run_time=0.6)
        self.at("not necessarily")
        # a replay of the trip: not on every second (dimmed, still green), but lit again at the end
        self.play(FadeOut(sig), FadeOut(on), FadeOut(tk), run_time=0.3)
        mover = lit(V(-3.8, PY), GREEN, 0.22)
        self.add(mover)

        def pattern(m, a):
            m.move_to(V(-3.8 + 6.7 * a, PY))
            on_ = a < 0.18 or a > 0.82 or (0.5 < a < 0.62)
            set_lit(m, 1.0 if on_ else 0.0, GREEN, DIMG)
        self.play(UpdateFromAlphaFunc(mover, pattern), run_time=2.9, rate_func=linear)
        tk2 = tick(V(2.9, PY + 0.62), GREEN, 0.28, 8)
        on2 = T("ON when it arrives", 30, GREEN, weight=BOLD).move_to(V(1.0, PY - 1.8))
        self.play(FadeIn(on2), Create(tk2), run_time=0.4)
        self.at("binding at the tip")
        chp = chip("binding at the tip", YELLOW, 26).move_to(V(-2.1, PY - 1.1))
        self.play(FadeIn(chp, shift=DOWN * 0.1), run_time=0.5)
        self.at("not enough")
        # Strike the full box from edge to edge, so the rejection reads at draft size.
        xm = VGroup(Line(chp.get_corner(DL), chp.get_corner(UR), color=RED, stroke_width=7),
                    Line(chp.get_corner(UL), chp.get_corner(DR), color=RED, stroke_width=7))
        self.play(Create(xm), chp[0].animate.set_stroke(RED), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
ZK = 1.9    # zoom of s07 on the terminal
ZTIP = V(3.0, 0.0)   # where the centre terminal tip sits in the zoomed frame


def zoom_rig():
    r = Rig(0.0)
    p0 = r.P(4.7, 0.0)
    for m in (r.cell, r.brk, r.nuc, r.block):
        m.scale(ZK, about_point=p0).shift(ZTIP - p0)
    return r


def random_walk(seed, n=50, step=0.42):
    """A reflecting random walk, in frame coordinates, starting at the terminal tip and staying inside the cell."""
    rng = np.random.default_rng(seed)
    x, y = ZTIP[0] + 0.1, 0.0
    pts = [V(x, y)]
    for i in range(n):
        a = rng.uniform(0, 2 * np.pi)
        nx, ny = x + step * np.cos(a) - (0.05 if x > 0.9 else 0.0), y + step * np.sin(a)
        lim = 0.28 if nx > 0.9 else 0.8
        ny = float(np.clip(ny, -lim, lim))
        nx = float(min(nx, ZTIP[0] + 0.35))
        x, y = nx, ny
        pts.append(V(x, y))
    return pts


class S07Q(SpokenScene):
    """A single glowing molecule at the terminal starts a random walk (zoomed in on the terminal and the first axon)."""

    def construct(self):
        r = zoom_rig()
        self.add(r.block, r.cell, r.brk)
        self.at("could the signal", lead=0.0)
        mol = lit(ZTIP, GREEN, 0.3)
        self.play(FadeIn(mol, scale=0.5), run_time=0.5)
        tl = VGroup(lab("terminal", V(3.4, -1.15), 28, LBL), lab("axon", V(-3.5, 0.0), 28, LBL),
                    dash_arrow(V(-0.2, -2.1), V(-6.0, -2.1), LBL), lab("to the cell body, centimetres away", V(-3.1, -2.7), 26, LBL))
        self.add(tl)
        self.at("drift home")
        q1 = T("drift home", 46, TEXT).move_to(V(-3.3, 2.5))
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.4)
        pts = random_walk(seed=3)
        trail = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 3, opacity=0.65)
        self.add(trail)
        walk = VMobject().set_points_as_corners(pts)
        q2 = T("by diffusion?", 46, TEXT).next_to(q1, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(MoveAlongPath(mol, walk, run_time=2.0, rate_func=linear),
                  Create(trail, run_time=2.0, rate_func=linear),
                  Succession(Wait(0.7), FadeIn(q2, shift=UP * 0.1, run_time=0.4)))
        self.finish()


# ---------------------------------------------------------------------------------------------
def eq_group(size=44, y=3.3):
    a = M("time ≈", size, TEXT)
    b = M("distance²", size, TEAL)
    c = M("/ (2 × D)", size, TEXT)
    return VGroup(a, b, c).arrange(RIGHT, buff=0.3).move_to([0, y, 0])


def dline(y=2.5):
    return VGroup(M("D ≈ 10 µm²/s", 32, TEXT), T("diffusion coefficient, soluble protein", 26, LBL)).arrange(
        RIGHT, buff=0.4).move_to([0, y, 0])


class S08Rule(SpokenScene):
    """Diffusion time grows with the square of the distance: the formula and the curve computed from it."""

    def construct(self):
        eq = eq_group()
        dl = dline()
        self.at("diffusion time", lead=0.0)
        self.play(FadeIn(eq, shift=DOWN * 0.1), FadeIn(dl, shift=DOWN * 0.1), run_time=0.7)
        self.at("grows with")
        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 10.5, 1], x_length=10.4, y_length=4.7,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 4,
                               "tip_length": 0.22}).move_to([0.4, -0.6, 0])
        xt = VGroup(*[VGroup(Line(ax.c2p(d, 0) + DOWN * 0.1, ax.c2p(d, 0) + UP * 0.1, color=GREY, stroke_width=4),
                             T(f"{d} cm", 28, LBL).move_to(ax.c2p(d, 0) + DOWN * 0.45)) for d in (1, 2, 3)])
        xl = T("distance", 28, LBL).move_to(ax.c2p(3.0, 0) + UP * 0.45)
        yl = T("time", 28, LBL).next_to(ax.y_axis, UP, buff=0.12)
        sc = T("schematic: time ∝ distance²", 26, LBL).move_to(ax.c2p(0.12, 8.6), aligned_edge=LEFT)
        self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), run_time=0.4)
        curve = ax.plot(lambda d: d * d, x_range=[0, 3.2], color=TEXT, stroke_width=7)
        self.play(Create(curve), FadeIn(sc), run_time=0.6, rate_func=linear)
        self.at("square of the distance")
        self.play(Indicate(eq[1], color=TEAL, scale_factor=1.15), run_time=0.7)
        marks = VGroup()
        for d, s in ((1, "×1"), (2, "×4")):
            p = ax.c2p(d, d * d)
            marks.add(DashedLine(ax.c2p(d, 0), p, color=GREY, stroke_width=3),
                      DashedLine(ax.c2p(0, d * d), p, color=GREY, stroke_width=3), dot(p, TEXT, 0.12),
                      T(s, 28, TEXT, weight=BOLD).move_to(ax.c2p(0, d * d) + LEFT * 0.5))
        self.play(Create(marks), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def clock(c, r=1.1):
    c = V(*c) if not isinstance(c, np.ndarray) else c
    face = Circle(radius=r, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(c)
    ticks = VGroup(*[Line(c + 0.78 * r * V(np.cos(a), np.sin(a)), c + 0.95 * r * V(np.cos(a), np.sin(a)),
                          color=GREY, stroke_width=3) for a in np.arange(0, 2 * np.pi, np.pi / 6)])
    hour = Line(c, c + 0.45 * r * V(0.5, 0.87), color=TEXT, stroke_width=6)
    minute = Line(c, c + 0.74 * r * V(0, 1), color=TEXT, stroke_width=5)
    return VGroup(face, ticks, hour, minute)


CLK = V(-4.6, -2.35)


def s09_parts():
    eq = eq_group()
    dchip = dline()
    tube = RoundedRectangle(corner_radius=0.3, width=11.6, height=1.0, stroke_color=GREY, stroke_width=3,
                            fill_color=SOLID, fill_opacity=1).move_to([0, 1.1, 0])
    bx = -0.9
    y0, y1 = 0.6, 1.6
    brk = VGroup(Polygon(V(bx - 0.2, y0), V(bx + 0.05, y1), V(bx + 0.45, y1), V(bx + 0.2, y0), stroke_width=0,
                         fill_color=BG, fill_opacity=1),
                 Line(V(bx - 0.2, y0), V(bx + 0.05, y1), color=GREY, stroke_width=3),
                 Line(V(bx + 0.2, y0), V(bx + 0.45, y1), color=GREY, stroke_width=3))
    dim = DoubleArrow(V(-5.8, 0.3), V(5.8, 0.3), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
    dl = T("1 cm = 10,000 micrometres", 38, TEXT).move_to([0, -0.4, 0])
    clk = clock(CLK)
    qm = T("?", 100, TEXT, weight=BOLD).move_to(CLK + V(1.7, 0.0))
    return eq, dchip, VGroup(tube, brk), dim, dl, clk, qm


def option_chips():
    c1 = chip("seconds", TEXT, 30)
    c2 = chip("hours", TEXT, 30)
    c3 = chip("much longer", TEXT, 30)
    g = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.4)
    g.move_to(V(2.3, CLK[1]))
    return g


class S09Ask(SpokenScene):
    """The question: a typical protein, an axon one centimetre long, how long would the trip take?"""

    def construct(self):
        eq, dchip, axon, dim, dl, clk, qm = s09_parts()
        self.add(eq, dchip)
        self.at("typical soluble protein", lead=0.0)
        self.play(Indicate(dchip, color=TEAL, scale_factor=1.1), run_time=0.7)
        self.at("an axon")
        self.play(DrawBorderThenFill(axon[0]), FadeIn(axon[1]), run_time=0.8)
        self.at("centimeter long")
        self.play(GrowFromCenter(dim), FadeIn(dl), run_time=0.8)
        self.at("how long would the trip take")
        self.play(FadeIn(clk, scale=0.7), run_time=0.5)
        self.play(Rotate(clk[3], angle=-2 * PI, about_point=clk[0].get_center(), rate_func=smooth), FadeIn(qm, scale=0.6),
                  run_time=1.2)
        self.finish()


class S10Pause(NarratedScene):
    """The question held for five seconds: the three options and a slow clock hand, so it reads as 'think now'."""

    def construct(self):
        eq, dchip, axon, dim, dl, clk, qm = s09_parts()
        self.add(eq, dchip, axon, dim, dl, clk, qm)
        chips = option_chips()
        self.play(Rotate(clk[3], angle=-2 * PI, about_point=clk[0].get_center(), rate_func=linear, run_time=4.6),
                  Succession(Wait(0.3),
                             LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.5, run_time=1.2),
                             Indicate(chips[0], color=TEAL, scale_factor=1.12, run_time=0.8),
                             Indicate(chips[1], color=TEAL, scale_factor=1.12, run_time=0.8),
                             Indicate(chips[2], color=TEAL, scale_factor=1.12, run_time=0.8)))
        self.finish()


# ---------------------------------------------------------------------------------------------
def week_tiles():
    tiles = VGroup()
    for i in range(8):
        rr, cc = divmod(i, 4)
        box = RoundedRectangle(corner_radius=0.1, width=1.85, height=0.95, stroke_color=GREY, stroke_width=2.5,
                               fill_color=RED, fill_opacity=0.0).move_to(V(-3.0 + cc * 2.0, 0.55 - rr * 1.15))
        tiles.add(VGroup(box, T(f"week {i + 1}", 26, TEXT).move_to(box)))
    return tiles


def calc_lines():
    c1 = M("10,000² / 20", 44, TEXT).move_to([0, 3.3, 0])
    c2 = M("≈ 5 million seconds", 36, TEXT).move_to([0, 2.55, 0])
    c3 = T("≈ two months", 52, RED, weight=BOLD).move_to([0, 1.75, 0])
    return c1, c2, c3


BAR_ROWS = [(0.45, 1, "1 cm"), (-0.55, 4, "2 cm"), (-1.55, 9, "3 cm")]
BAR_X0, BW, BH = -4.0, 0.7, 0.7
BAR_NOTE = ["≈ 2 months", "× 4  ≈ 8 months", "× 9  ≈ 18 months"]


def bar_rows():
    """The three rows of the time-grows-with-distance-squared bars. Each block is one 'two months' unit."""
    rows = []
    for (y, n, name), note in zip(BAR_ROWS, BAR_NOTE):
        blocks = VGroup(*[Rectangle(width=BW, height=BH, stroke_color=BG, stroke_width=3, fill_color=RED,
                                    fill_opacity=0.5).move_to(V(BAR_X0 + BW * (i + 0.5), y)) for i in range(n)])
        nm = T(name, 30, TEXT).move_to(V(-5.3, y))
        nt = T(note, 28, TEXT).move_to(V(BAR_X0 + BW * n + 0.3, y), aligned_edge=LEFT)
        rows.append((blocks, nm, nt))
    return rows


class S11Reveal(SpokenScene):
    """Roughly two months: the numbers, a calendar of eight weeks, then 2 cm is four times and 3 cm nine times as long."""

    def construct(self):
        eq, dchip, axon, dim, dl, clk, qm = s09_parts()
        self.add(eq, dchip, axon, dim, dl, clk, qm)
        c1, c2, c3 = calc_lines()
        self.play(FadeOut(VGroup(dchip, axon, dim, dl, clk, qm)), ReplacementTransform(eq, c1),
                  FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        self.at("roughly two months", lead=0.0)
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.4)
        tiles = week_tiles()
        self.add(tiles)
        self.play(LaggedStart(*[t[0].animate.set_fill(RED, 0.45) for t in tiles], lag_ratio=1.0), run_time=1.1)
        rows = bar_rows()
        self.at("over a few")
        self.play(VGroup(c1, c2, c3).animate.set_opacity(0.3),
                  ReplacementTransform(tiles, rows[0][0]), FadeIn(rows[0][1]), FadeIn(rows[0][2]), run_time=0.6)
        self.at("centimeters")
        self.play(GrowFromEdge(rows[1][0], LEFT), FadeIn(rows[1][1]), GrowFromEdge(rows[2][0], LEFT), FadeIn(rows[2][1]),
                  run_time=0.5)
        self.play(FadeIn(rows[1][2], shift=RIGHT * 0.15), FadeIn(rows[2][2], shift=RIGHT * 0.15), run_time=0.3)
        self.at("many months")
        mm = T("many months", 46, RED, weight=BOLD).move_to([0, -2.9, 0])
        self.play(FadeIn(mm, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        c1, c2, c3 = calc_lines()
        VGroup(c1, c2, c3).set_opacity(0.3)
        self.add(c1, c2, c3)
        for blocks, nm, nt in bar_rows():
            self.add(blocks, nm, nt)
        self.add(T("many months", 46, RED, weight=BOLD).move_to([0, -2.9, 0]))
        self.finish()


# ---------------------------------------------------------------------------------------------
PC = V(-1.6, -0.2)    # centre of the signal protein in the zoom inset
PTAG = PC + V(1.45, 1.2)    # where the phosphate sits on it


def inset():
    fr = RoundedRectangle(corner_radius=0.3, width=12.4, height=6.9, stroke_color=GREY, stroke_width=2.5).move_to([0, 0.1, 0])
    bar = VGroup(Line(V(-5.9, -2.85), V(0.1, -2.85), color=GREY, stroke_width=4),
                 Line(V(-5.9, -2.7), V(-5.9, -3.0), color=GREY, stroke_width=4),
                 Line(V(0.1, -2.7), V(0.1, -3.0), color=GREY, stroke_width=4))
    bl = T("10 nm", 28, LBL).move_to(V(1.3, -2.85))
    return VGroup(fr, bar, bl)


def protein(on=True):
    body = Ellipse(width=4.4, height=2.8, stroke_color=GREEN if on else GREY, stroke_width=4,
                   fill_color=GREEN if on else GREY, fill_opacity=0.22 if on else 0.14).move_to(PC)
    lbl = T("signal protein", 30, TEXT).move_to(PC)
    return VGroup(body, lbl)


def phos_tag():
    return VGroup(hal(PTAG, PHOS, 0.85, 0.25), pbadge(PTAG, 0.38))


class S13Worse(SpokenScene):
    """Zoomed in: a protein carrying a phosphate, and a phosphatase that removes it."""

    def construct(self):
        ins = inset()
        self.add(ins)
        self.at("worse", lead=0.0)
        prot = protein(False)
        self.play(FadeIn(prot, scale=0.8), run_time=0.7)
        self.at("carrying a phosphate")
        pt = phos_tag()
        self.play(FadeIn(pt, shift=DOWN * 0.5, scale=0.5), prot[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.22),
                  run_time=0.8)
        self.at("phosphate", nth=0)
        pl = VGroup(T("phosphate", 28, PHOS), leader(V(-1.2, 2.5), PTAG + V(-0.1, 0.4), PHOS))
        pl[0].move_to(V(-2.3, 2.7))
        self.play(FadeIn(pl), run_time=0.4)
        self.at("enzymes called phosphatases")
        ph = VGroup(Ellipse(width=3.0, height=1.7, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.2),
                    T("phosphatase", 28, TEXT)).move_to(V(4.0, 1.0))
        self.play(FadeIn(ph, shift=LEFT * 0.4), run_time=0.7)
        self.at("keep removing it")
        self.play(ph.animate.move_to(V(1.95, 1.05)), run_time=0.7)
        self.at("removing")
        self.play(Flash(PTAG, color=RED, flash_radius=0.7, line_length=0.2, run_time=0.6),
                  pt.animate.shift(UP * 1.5 + RIGHT * 0.5).set_opacity(0.35), FadeOut(pl),
                  prot[0].animate.set_stroke(GREY).set_fill(GREY, 0.14), run_time=0.9)
        self.play(ph.animate.shift(RIGHT * 1.0), run_time=0.7)
        self.finish()


class S14Suppose(SpokenScene):
    """Suppose a phosphate lasts about ten seconds (illustrative)."""

    def construct(self):
        ins = inset()
        prot = protein(False)
        self.add(ins, prot)
        self.at("a phosphate lasts", lead=0.0)
        pt = phos_tag()
        self.play(FadeIn(pt, scale=0.4), prot[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.22), run_time=0.5)
        self.at("about 10 seconds")
        cc = V(3.9, 0.3)
        ring0 = Circle(radius=1.35, stroke_color=GREY, stroke_width=4).move_to(cc)
        lab10 = M("10 s", 52, TEXT).move_to(cc)
        self.play(FadeIn(ring0), FadeIn(lab10), run_time=0.3)
        prog = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=1.35, start_angle=PI / 2, angle=2 * PI * prog.get_value(),
                                        arc_center=cc, stroke_color=PHOS, stroke_width=9))
        self.add(arc)
        ill = T("illustrative rate", 28, LBL).move_to([3.9, -1.7, 0])
        self.play(prog.animate.set_value(0.001), FadeIn(ill), run_time=1.3, rate_func=linear)
        self.play(pt.animate.shift(UP * 0.9 + RIGHT * 0.9).set_opacity(0),
                  prot[0].animate.set_stroke(GREY).set_fill(GREY, 0.14), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TX0, SPAN = 5.0, 10.8          # x of the tip (0 um) and the width of 40 um
TUBE_Y = 2.8
PL_BASE, PL_TOP = -2.75, 0.0


def dx(d_um):
    return TX0 - SPAN * d_um / 40.0


def yv(d_um):
    return PL_BASE + (PL_TOP - PL_BASE) * np.exp(-d_um / 10.0)


def tube():
    return RoundedRectangle(corner_radius=0.2, width=SPAN, height=1.0, stroke_color=GREY, stroke_width=3,
                            fill_color=SOLID, fill_opacity=1).move_to(V(TX0 - SPAN / 2, TUBE_Y))


def cloud(k):
    """Glowing active signal along the tube: brightness exp(-d/10 µm), revealed out to k * 40 µm from the tip."""
    n = 96
    bars = VGroup()
    w = SPAN / n
    for i in range(n):
        xc = TX0 - w * (i + 0.5)
        bars.add(Rectangle(width=w + 0.005, height=0.9, stroke_width=0, fill_color=GREEN, fill_opacity=0).move_to(V(xc, TUBE_Y)))
    kk = ValueTracker(k)

    def upd(g):
        for i, b in enumerate(g):
            d = (i + 0.5) / n * 40
            op = 0.9 * np.exp(-d / 10.0) if d <= kk.get_value() * 40 else 0.0
            b.set_fill(GREEN, op)
    bars.add_updater(upd)
    upd(bars)
    return bars, kk


def fade_curve():
    pts = [V(dx(d), yv(d)) for d in np.linspace(0, 40, 120)]
    return VMobject().set_points_smoothly(pts).set_stroke(GREEN, 6)


def plot_frame():
    base = Line(V(TX0 + 0.1, PL_BASE), V(dx(40) - 0.1, PL_BASE), color=GREY, stroke_width=4)
    yax = Line(V(TX0 + 0.1, PL_BASE), V(TX0 + 0.1, PL_TOP + 0.45), color=GREY, stroke_width=4)
    ticks = VGroup(*[Line(V(dx(d), PL_BASE - 0.1), V(dx(d), PL_BASE + 0.1), color=GREY, stroke_width=4) for d in (0, 10, 20, 30)])
    nums = VGroup(*[T(s, 26, LBL).move_to(V(dx(d), PL_BASE - 0.42)) for d, s in [(0, "0"), (10, "10"), (20, "20"), (30, "30 µm")]])
    cap = T("distance from the tip", 28, LBL).move_to(V(0.0, PL_BASE - 0.95))
    ylab = VGroup(T("1", 26, LBL).move_to(V(TX0 + 0.5, PL_TOP)), T("0", 26, LBL).move_to(V(TX0 + 0.5, PL_BASE)))
    ytitle = T("active signal (fraction of tip level)", 26, GREEN).move_to(V(6.2, PL_TOP + 0.9), aligned_edge=RIGHT)
    return VGroup(base, yax, ticks, nums, cap, ylab, ytitle)


def third_marks():
    return VGroup(DashedLine(V(dx(10), PL_BASE), V(dx(10), yv(10)), color=TEXT, stroke_width=3),
                  DashedLine(V(dx(0), yv(10)), V(dx(10), yv(10)), color=TEXT, stroke_width=3),
                  dot(V(dx(10), yv(10)), TEXT, 0.12))


def third_label():
    return T("about a third", 28, TEXT).move_to(V(dx(5), yv(10) - 0.42))


def bracket():
    y = TUBE_Y - 0.8
    br = VGroup(Line(V(dx(0), y), V(dx(10), y), color=TEXT, stroke_width=4),
                Line(V(dx(0), y + 0.13), V(dx(0), y - 0.13), color=TEXT, stroke_width=4),
                Line(V(dx(10), y + 0.13), V(dx(10), y - 0.13), color=TEXT, stroke_width=4))
    bl = T("10 µm", 28, TEXT).move_to(V(dx(5), y - 0.4))
    return br, bl


def fade_note():
    return VGroup(T("fade distance about 10 µm", 28, TEXT), T("illustrative rates", 26, LBL)).arrange(
        DOWN, buff=0.15, aligned_edge=LEFT).move_to(V(-3.0, -0.75))


class S15Fade(SpokenScene):
    """The active signal falls to about a third every ten micrometres: a glowing cloud and the curve computed from it."""

    def construct(self):
        tb = tube()
        self.add(tb)
        tipl = T("tip", 28, LBL).move_to(V(TX0 + 0.55, TUBE_Y))
        self.add(tipl)
        self.at("active signal", lead=0.0)
        bars, kk = cloud(0.04)
        self.add(bars)
        al = T("active signal", 28, GREEN).move_to(V(3.0, TUBE_Y - 0.95))
        self.play(FadeIn(al, shift=DOWN * 0.1), run_time=0.5)
        self.at("falls")
        pf = plot_frame()
        crv = fade_curve()
        self.play(kk.animate.set_value(1.0).set_rate_func(smooth), FadeOut(al),
                  Succession(Create(pf, run_time=0.25), Create(crv, run_time=0.6, rate_func=linear)), run_time=0.95)
        self.at("about a third")
        mk = third_marks()
        gl = third_label()
        self.play(Create(mk), FadeIn(gl), run_time=0.6)
        self.at("every 10 micrometers")
        br, bl = bracket()
        self.play(Create(br), FadeIn(bl), run_time=0.6)
        self.at("from the tip")
        fl = fade_note()
        self.play(FadeIn(fl), run_time=0.5)
        self.finish()


def s15_end(scene):
    tb = tube()
    tipl = T("tip", 28, LBL).move_to(V(TX0 + 0.55, TUBE_Y))
    bars, kk = cloud(1.0)
    scene.add(tb, tipl, bars)
    pf, crv, mk, gl = plot_frame(), fade_curve(), third_marks(), third_label()
    br, bl = bracket()
    fl = fade_note()
    scene.add(pf, crv, mk, gl, br, bl, fl)
    return VGroup(tb, tipl, bars), VGroup(pf, crv, mk, gl, br, bl, fl)


# ---------------------------------------------------------------------------------------------
# the axon as a long bar (s16 to s18): cell body at left, the organ at right, tip at AX1
# ---------------------------------------------------------------------------------------------
AXY = 1.4
AX0, AX1 = -4.6, 5.4


def strip_neuron():
    axon = RoundedRectangle(corner_radius=0.4, width=AX1 - AX0, height=1.2, stroke_color=GREY, stroke_width=3,
                            fill_color=SOLID, fill_opacity=1).move_to(V((AX0 + AX1) / 2, AXY))
    bx = 0.9
    poly = Polygon(V(bx - 0.2, AXY - 0.62), V(bx + 0.05, AXY + 0.62), V(bx + 0.45, AXY + 0.62), V(bx + 0.2, AXY - 0.62),
                   stroke_width=0, fill_color=BG, fill_opacity=1)
    brk = VGroup(poly, Line(V(bx - 0.2, AXY - 0.62), V(bx + 0.05, AXY + 0.62), color=GREY, stroke_width=3),
                 Line(V(bx + 0.2, AXY - 0.62), V(bx + 0.45, AXY + 0.62), color=GREY, stroke_width=3))
    cell = Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=SOLID, fill_opacity=1).move_to(V(-5.3, AXY))
    nuc = Circle(radius=0.42, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to(V(-5.3, AXY))
    block = RoundedRectangle(corner_radius=0.12, width=0.7, height=3.2, stroke_color=YELLOW, stroke_width=3,
                             fill_color=YELLOW, fill_opacity=0.14).move_to(V(5.85, AXY))
    return VGroup(block, axon, brk, cell, nuc)


def ruler_parts(full=False):
    y = 0.1
    line = Line(V(AX1, y), V(AX0, y), color=TEXT, stroke_width=3)
    ends = VGroup(Line(V(AX1, y - 0.2), V(AX1, y + 0.2), color=TEXT, stroke_width=4),
                  Line(V(AX0, y - 0.2), V(AX0, y + 0.2), color=TEXT, stroke_width=4))
    comb = VGroup(*[Line(V(AX1 - (AX1 - AX0) * i / 100, y - 0.13), V(AX1 - (AX1 - AX0) * i / 100, y + 0.13), color=TEXT,
                         stroke_width=2) for i in range(1, 100)])
    l0 = T("tip: 0", 28, LBL).move_to(V(AX1 - 0.3, y - 0.5))
    l1 = T("10,000 µm", 28, LBL).move_to(V(AX0 + 0.6, y - 0.5))
    return VGroup(line, ends), comb, VGroup(l0, l1)


def speck_callout():
    sp = VGroup(hal(V(AX1 - 0.12, AXY), GREEN, 0.3, 0.3), dot(V(AX1 - 0.12, AXY), GREEN, 0.07))
    lb = VGroup(leader(V(AX1 - 0.12, AXY + 0.15), V(AX1 - 0.85, 2.85), GREEN),
                T("signal drops to a third every 10 µm", 28, GREEN).move_to(V(AX1 - 1.0, 3.2), aligned_edge=RIGHT))
    return sp, lb


class S16Frac(SpokenScene):
    """Zoom out: the faded cloud is a speck at the tip of a one-centimetre axon, a thousand fade distances long."""

    def construct(self):
        strip, rest = s15_end(self)
        nr = strip_neuron()
        self.at("a centimeter is", lead=0.0)
        tip = V(AX1 - 0.12, AXY)
        # Pull both the cloud and its axon back together: the ratio is visible in motion.
        nr.scale(5.0, about_point=tip)
        self.add(nr)
        self.play(FadeOut(rest), nr.animate.scale(0.2, about_point=tip),
                  strip.animate.scale(0.02).move_to(tip), run_time=0.9)
        sp, call = speck_callout()
        self.play(FadeOut(strip), FadeIn(sp), run_time=0.1)
        rl, comb, rlab = ruler_parts()
        d1 = T("1 cm = 10,000 µm", 40, TEXT).move_to([0, -1.25, 0])
        self.play(FadeIn(call), Create(rl), FadeIn(rlab), FadeIn(d1), run_time=0.5)
        self.at("thousand of those steps")
        d2 = T("1 cm = 1,000 fade distances", 40, TEXT).move_to([0, -1.25, 0])
        note = T("each tick = 10 fade distances (100 ticks drawn)", 26, LBL).move_to([0, -2.0, 0])
        self.play(Create(comb, lag_ratio=0.02), FadeOut(d1), FadeIn(d2), FadeIn(note), run_time=1.3)
        self.at("the rates are illustrative")
        il = T("illustrative rates, not TrkA measurements", 28, LBL).move_to([0, -3.0, 0])
        self.play(FadeIn(il), run_time=0.5)
        self.at("conclusion holds")
        self.play(Flash(tip, color=GREEN, flash_radius=0.5, line_length=0.15, run_time=0.8),
                  Indicate(call[1], color=GREEN, scale_factor=1.06), run_time=0.8)
        self.finish()


def s16_neuron(scene):
    nr = strip_neuron()
    scene.add(nr)
    return nr


SLOTS = [-4.15, -3.55, -2.95, -2.35]


def grey_dot(x):
    d = lit(V(x, AXY), GREEN, 0.25)
    set_lit(d, 0.0)
    return d


class S17Line(SpokenScene):
    """Lit molecules leave the tip, lose their glow en route, and reach the body grey."""

    def construct(self):
        nr = strip_neuron().shift(DOWN * AXY)
        self.add(nr)
        self.at("it does not arrive late", lead=0.0)
        mols = [lit(V(AX1 - 0.3, 0), GREEN, 0.32) for _ in SLOTS]
        self.add(*mols)
        # Explicit animation keeps the whole green-to-grey journey in this short sentence.
        def journey(m, a, k):
            p = clip01((a - 0.05 * k) / (1.0 - 0.05 * k))
            m.move_to(V(AX1 - 0.3 + (SLOTS[k] - (AX1 - 0.3)) * p, 0))
            set_lit(m, 1.0 - clip01((p - 0.12) / 0.65))
        self.play(*[UpdateFromAlphaFunc(m, lambda mob, a, k=k: journey(mob, a, k))
                    for k, m in enumerate(mols)], run_time=2.5, rate_func=linear)
        self.at("switched", lead=0.0)
        so = T("switched off", 42, RED, weight=BOLD).move_to(V(0, -1.65))
        # An extinguished halo and a cross at arrival make the state visible as well as named.
        xm = cross(V(-4.35, -0.85), RED, 0.22, 7)
        self.play(FadeIn(so, shift=UP * 0.1), Create(xm), run_time=0.4)
        self.finish()


class S18Beat(NarratedScene):
    def construct(self):
        self.add(strip_neuron().shift(DOWN * AXY))
        mols = [lit(V(x, 0), GREEN, 0.32) for x in SLOTS]
        for m in mols:
            set_lit(m, 0.0)
        self.add(*mols, T("switched off", 42, RED, weight=BOLD).move_to(V(0, -1.65)),
                 cross(V(-4.35, -0.85), RED, 0.22, 7))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Needs(SpokenScene):
    """Two needs: a vehicle or a relay for the trip, and still able to signal on arrival."""

    def construct(self):
        nr = strip_neuron().shift(DOWN * AXY)
        mols = [lit(V(x, 0), GREEN, 0.32) for x in SLOTS]
        for m in mols:
            set_lit(m, 0.0)
        so = VGroup(T("switched off", 42, RED, weight=BOLD).move_to(V(0, -1.65)),
                    cross(V(-4.35, -0.85), RED, 0.22, 7))
        self.add(nr, *mols, so)
        y1, y2, y3 = 1.4, -0.3, -2.1
        head = T("What the signal needs", 32, TEAL).move_to([0, 3.2, 0])

        def num(n, y, faint=False):
            c = Circle(radius=0.34, stroke_color=TEXT, stroke_width=3, fill_opacity=0)
            t = T(str(n), 32, TEXT, weight=BOLD)
            g = VGroup(c, t).move_to(V(-5.9, y))
            return g
        n1, n2, n3 = num(1, y1), num(2, y2), num(3, y3)
        ic1 = VGroup(DashedLine(V(-5.3, y1), V(-4.35, y1), color=TEXT, stroke_width=4), Triangle(
            fill_opacity=1, color=TEXT, stroke_width=0).scale(0.15).rotate(-PI / 2).move_to(V(-4.25, y1)))
        ic2 = lit(V(-4.7, y2), GREEN, 0.28)
        t1 = T("a vehicle", 44, TEAL).move_to(V(-3.5, y1), aligned_edge=LEFT)
        t1b = T("or a relay", 44, TEAL).next_to(t1, RIGHT, buff=0.3)
        t2 = T("able to signal", 44, GREEN).move_to(V(-3.5, y2), aligned_edge=LEFT)
        t2b = T("when it arrives", 44, GREEN).next_to(t2, RIGHT, buff=0.3)
        ghost = VGroup(t1, t1b, t2, t2b, ic1).set_opacity(0.22)
        self.play(FadeOut(VGroup(nr, *mols, so)), FadeIn(head), FadeIn(VGroup(n1, n2, ghost)), run_time=0.5)
        self.at("so the signal needs", lead=0.0)
        self.at("a vehicle")
        self.play(t1.animate.set_opacity(1), ic1.animate.set_opacity(1), Indicate(n1, color=TEAL, scale_factor=1.2), run_time=0.5)
        self.at("or a relay")
        self.play(t1b.animate.set_opacity(1), run_time=0.4)
        self.at("able to signal")
        self.play(t2.animate.set_opacity(1), FadeIn(ic2, scale=0.6), Indicate(n2, color=GREEN, scale_factor=1.2), run_time=0.5)
        self.at("when it arrives")
        self.play(t2b.animate.set_opacity(1), run_time=0.5)
        self.wait(0.3)
        t3 = T("the target's message kept distinct from other signals", 28, LBL).move_to(V(-3.5, y3 + 0.2), aligned_edge=LEFT)
        t3b = T("helpful, not shown to be required", 26, GREY).move_to(V(-3.5, y3 - 0.35), aligned_edge=LEFT)
        self.play(FadeIn(n3), FadeIn(t3), FadeIn(t3b), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# The membrane stage: receptors and NGF at the tip, pinching into a signaling endosome. Drawn from one function so the
# pose, the zoom and the camera height can be animated together. Local units: membrane at y = 0, outside up; RV = cup radius.
# ---------------------------------------------------------------------------------------------
RV = 1.2


class Stage:
    def __init__(self, z=2.1, yc=-0.57, xo=0.0):
        self.p = ValueTracker(0.0)      # pinch progress: 0 flat membrane, 1 closed vesicle
        self.ro = ValueTracker(0.0)     # opacity of the teal vesicle ring
        self.sl = ValueTracker(0.0)     # the closed vesicle slides away from the membrane
        self.gl = ValueTracker(0.0)     # glow of the kinase tails
        self.mo = ValueTracker(1.0)     # membrane opacity
        self.zt, self.yt, self.xt = ValueTracker(z), ValueTracker(yc), ValueTracker(xo)
        self.rs = ValueTracker(0.45)    # half separation of the receptors
        self.ny = ValueTracker(1.1)     # NGF height above the receptor base
        self.no = ValueTracker(1.0)     # NGF opacity
        self.rop = ValueTracker(1.0)    # receptor opacity

    def geom(self):
        p, z, yc, xo = self.p.get_value(), self.zt.get_value(), self.yt.get_value(), self.xt.get_value()
        closed = p >= 0.999
        if closed:
            beta, base = PI, -2 * RV - self.sl.get_value()
        else:
            beta = float(np.arccos(np.clip(1 - 2 * p, -1, 1)))
            base = -RV * (1 - np.cos(beta))
        return dict(z=z, yc=yc, xo=xo, base=base, closed=closed, beta=beta)

    def S(self, g, lx, ly):
        return V(g["xo"] + lx * g["z"], g["yc"] + ly * g["z"])

    def anchor(self, name):
        g = self.geom()
        b, rs = g["base"], self.rs.get_value()
        if name == "dimer":
            return self.S(g, 0.0, b + self.ny.get_value())
        if name == "dimer_r":
            return self.S(g, 0.45, b + self.ny.get_value()) + V(0.3 * g["z"] + 0.08, 0)
        if name == "body_r":
            return self.S(g, rs, b + 0.32) + V(0.15 * g["z"] + 0.05, 0)
        if name == "tail_r":
            return self.S(g, rs, b - 0.45) + V(0.05, 0)
        if name == "ring":
            return self.S(g, 0.0, b + RV)
        if name == "ring_l":
            return self.S(g, -RV, b + RV)
        if name == "membrane_y":
            return V(0, g["yc"])

    def build(self):
        g = self.geom()
        z, yc, xo, base, beta = g["z"], g["yc"], g["xo"], g["base"], g["beta"]
        S = lambda lx, ly: self.S(g, lx, ly)
        out = VGroup()
        mo = self.mo.get_value()
        if mo > 0.01:
            if g["closed"] or beta < 0.02:
                mem = Line(V(-7.3, yc), V(7.3, yc))
            else:
                cy = RV * np.cos(beta)
                xe = RV * np.sin(beta)
                th = np.linspace(-beta, beta, 70)
                arc = [S(RV * np.sin(t), cy - RV * np.cos(t)) for t in th]
                left = [V(x, yc) for x in np.linspace(-7.3, xo - xe * z, 7)[:-1]]
                right = [V(x, yc) for x in np.linspace(xo + xe * z, 7.3, 7)[1:]]
                mem = VMobject().set_points_as_corners(left + arc + right)
            out.add(mem.set_stroke(GREY, 10, opacity=mo))
        ro = self.ro.get_value()
        if g["closed"] and ro > 0.01:
            out.add(Circle(radius=RV * z, stroke_color=TEAL, stroke_width=8, stroke_opacity=ro, fill_color=TEAL,
                           fill_opacity=0.08 * ro).move_to(S(0, base + RV)))
        gl, rop, rs = self.gl.get_value(), self.rop.get_value(), self.rs.get_value()
        tcol = interpolate_color(ManimColor(TRKA), ManimColor(GREEN), gl)
        if rop > 0.01:
            for sg in (-1, 1):
                x = sg * rs
                body = RoundedRectangle(corner_radius=0.1 * z, width=0.3 * z, height=0.95 * z, stroke_color=TRKA, stroke_width=3,
                                        stroke_opacity=rop, fill_color=TRKA, fill_opacity=0.85 * rop).move_to(S(x, base + 0.32))
                tail = Line(S(x, base - 0.15), S(x, base - 0.75), color=tcol, stroke_width=6, stroke_opacity=rop)
                knob = dot(S(x, base - 0.78), tcol, 0.13 * z, rop)
                if gl > 0.01:
                    out.add(hal(S(x, base - 0.78), GREEN, 0.4 * z, 0.3 * gl))
                out.add(body, tail, knob)
        no = self.no.get_value()
        if no > 0.01:
            c = S(0, base + self.ny.get_value())
            out.add(Line(c + V(-0.45 * z, 0), c + V(0.45 * z, 0), color=YELLOW, stroke_width=9, stroke_opacity=no),
                    dot(c + V(-0.45 * z, 0), YELLOW, 0.3 * z, no), dot(c + V(0.45 * z, 0), YELLOW, 0.3 * z, no))
        return out

    def mob(self):
        return always_redraw(self.build)


Z0, Z1 = 2.1, 1.7
YC0, YC1 = -0.57, 2.75


def side_labels(st, op=None):
    """'outside the cell' above and 'inside the cell' below the membrane, following it."""
    def build():
        y = st.yt.get_value()
        return VGroup(lab("outside the cell", V(-4.7, y + 0.5), 28, LBL), lab("inside the cell", V(-4.7, y - 0.5), 28, LBL))
    return always_redraw(build)


class S20Cand(SpokenScene):
    """At the tip, NGF (a pair) binds two TrkA receptors that sit in the terminal membrane."""

    def construct(self):
        st = Stage(Z0, YC0)
        st.rs.set_value(1.35)
        st.ny.set_value(1.55)
        # Establish the complete candidate with the opening words.
        mob = st.mob()
        sl = side_labels(st)
        tl = lab("axon tip membrane", V(4.5, -2.85), 28, LBL)
        ng = always_redraw(lambda: VGroup(
            lab("NGF", st.anchor("dimer") + V(2.6, 0), 32, YELLOW, edge=LEFT, weight=BOLD),
            leader(st.anchor("dimer") + V(2.5, 0), st.anchor("dimer_r"), YELLOW)))
        self.add(mob, sl, tl, ng)
        self.at("one candidate", lead=0.0)
        self.at("at the tip")
        self.play(Indicate(tl, color=TEXT, scale_factor=1.04), run_time=0.4)
        self.at("ngf binds")
        self.play(st.ny.animate.set_value(1.1), st.rs.animate.set_value(0.45), run_time=0.45)
        self.at("its receptor")
        self.play(*[Flash(st.anchor("body_r") * np.array([sg, 1.0, 1.0]) + V(sg * -0.1, 0), color=TRKA, flash_radius=0.7, line_length=0.2,
                          run_time=0.7) for sg in (-1, 1)])
        self.at("track a")
        tk = always_redraw(lambda: VGroup(
            lab("TrkA", st.anchor("body_r") + V(2.55, -0.2), 32, TRKA, edge=LEFT, weight=BOLD),
            leader(st.anchor("body_r") + V(2.45, -0.2), st.anchor("body_r"), TRKA)))
        self.play(FadeIn(tk), run_time=0.5)
        self.finish()


def endo_labels(st, txt, lop):
    """NGF, TrkA and tail labels that follow the stage; txt holds their words, lop their opacity."""
    def build():
        o = lop.get_value()
        out = VGroup()
        d = st.anchor("dimer")
        out.add(lab(txt["ngf"], V(2.5, d[1]), 30, YELLOW, edge=LEFT, weight=BOLD),
                leader(V(2.4, d[1]), st.anchor("dimer_r"), YELLOW))
        b = st.anchor("body_r")
        out.add(lab(txt["trka"], V(2.5, b[1] - 0.2), 28, TRKA, edge=LEFT, weight=BOLD), leader(V(2.4, b[1] - 0.2), b, TRKA))
        if txt.get("tail"):
            t = st.anchor("tail_r")
            out.add(lab(txt["tail"], V(2.5, t[1] - 0.05), 28, GREEN if st.gl.get_value() > 0.5 else LBL, edge=LEFT),
                    leader(V(2.4, t[1] - 0.05), t, GREEN if st.gl.get_value() > 0.5 else LBL))
        return out.set_opacity(o)
    return always_redraw(build)


class S21Endo(SpokenScene):
    """The membrane pinches in around NGF on TrkA: a signaling endosome whose kinase tails still signal."""

    def construct(self):
        st = Stage(Z0, YC0)
        txt = {"ngf": "NGF", "trka": "TrkA", "tail": None}
        lop = ValueTracker(1.0)
        mob = st.mob()
        sl = side_labels(st)
        tl = lab("axon tip membrane", V(4.5, -2.85), 28, LBL)
        labs = endo_labels(st, txt, lop)
        self.add(mob, sl, tl, labs)
        self.play(FadeOut(tl), run_time=0.3)
        self.at("ligand", lead=0.0)
        txt["ngf"] = "NGF, the ligand"
        self.play(Flash(st.anchor("dimer"), color=YELLOW, flash_radius=1.2, line_length=0.3, run_time=0.7))
        self.at("active receptor")
        txt["trka"] = "TrkA, the\nactive receptor"
        self.play(*[Flash(st.anchor("body_r") * np.array([sg, 1.0, 1.0]) + V(sg * -0.1, 0), color=TRKA, flash_radius=0.8, line_length=0.2,
                          run_time=0.7) for sg in (-1, 1)])
        self.at("pulled into the cell")
        pe = 0.99
        self.play(st.p.animate.set_value(pe), st.zt.animate.set_value(Z0 - (Z0 - Z1) * pe),
                  st.yt.animate.set_value(YC0 + (YC1 - YC0) * pe), run_time=1.7, rate_func=smooth)
        self.at("a vesicle called")
        st.p.set_value(1.0)
        st.zt.set_value(Z1)
        st.yt.set_value(YC1)
        txt["ngf"] = "NGF inside"
        self.play(st.ro.animate.set_value(1.0), st.sl.animate.set_value(0.35), run_time=0.6)
        self.at("signaling endosome")
        ring_l = st.anchor("ring_l")
        chp = chip("signaling endosome", TEAL, 28, pad=0.18).move_to(V(-4.3, ring_l[1]))
        lead = leader(V(-2.55, ring_l[1]), ring_l, TEAL, 3)
        self.play(Create(lead), FadeIn(chp, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.6)
        txt["tail"] = "kinase tails outside"
        self.play(Flash(st.anchor("tail_r"), color=TRKA, flash_radius=0.7, line_length=0.2, run_time=0.7))
        self.at("keep signaling")
        txt["tail"] = "kinase tails signal"
        self.play(st.gl.animate.set_value(1.0),
                  *[Flash(st.anchor("tail_r") * np.array([sg, 1.0, 1.0]), color=GREEN, flash_radius=0.7, line_length=0.18, run_time=0.9)
                    for sg in (-1, 1)])
        self.finish()


class S22Dynein(SpokenScene):
    """Dynein, the motor, walks the endosome along a microtubule toward the cell body."""

    def construct(self):
        st = Stage(Z1, YC1)
        st.p.set_value(1.0)
        st.ro.set_value(1.0)
        st.sl.set_value(0.35)
        st.gl.set_value(1.0)
        txt = {"ngf": "NGF inside", "trka": "TrkA", "tail": "kinase tails signal"}
        lop = ValueTracker(1.0)
        mob = st.mob()
        sl = side_labels(st)
        labs = endo_labels(st, txt, lop)
        ring_l = st.anchor("ring_l")
        chp = chip("signaling endosome", TEAL, 28, pad=0.18).move_to(V(-4.3, ring_l[1]))
        lead = leader(V(-2.55, ring_l[1]), ring_l, TEAL, 3)
        self.add(mob, sl, labs, chp, lead)
        TY = -3.0
        mt = Line(V(-6.3, TY), V(6.3, TY), color=LBL, stroke_width=8)
        ticks = VGroup(*[Line(V(x, TY + 0.12), V(x, TY - 0.12), color=BG, stroke_width=3) for x in np.arange(-6.0, 6.1, 0.7)])
        zc, yct = 1.45, 3.05
        self.play(FadeOut(sl), FadeOut(chp), FadeOut(lead), lop.animate.set_value(0.0), st.mo.animate.set_value(0.0),
                  st.zt.animate.set_value(zc), st.yt.animate.set_value(yct), st.xt.animate.set_value(1.8),
                  FadeIn(mt), FadeIn(ticks), run_time=0.6)
        self.remove(labs)
        clk = clock_tracker(self)
        T0, DUR, X0, X1 = 1.0, 3.3, 1.8, -1.8
        xp = lambda: X0 + (X1 - X0) * clip01((clk.get_value() - T0) / DUR)
        st.xt.add_updater(lambda m: m.set_value(xp()))
        self.add(st.xt)
        self.at("motor protein", lead=0.0)

        def cen():
            return st.anchor("ring")

        def legs():
            c = cen()
            out = VGroup()
            for sg in (-1, 1):
                a = clk.get_value() * 5.0 + (0 if sg < 0 else PI)
                # Cargo adaptor at the outer vesicle surface, clear of the receptor tails.
                radius = RV * st.zt.get_value()
                top = c + radius * V(0.85 * sg, -np.sqrt(1.0 - 0.85 ** 2))
                foot = V(c[0] + 1.6 * sg + 0.25 * np.sin(a), TY + 0.07 + 0.15 * max(0.0, np.cos(a)))
                out.add(Line(top, foot, color=PINK, stroke_width=7),
                        dot(top, PINK, 0.13), dot(foot, PINK, 0.11))
            return out
        lg = always_redraw(legs)

        def dyn_label():
            c = cen()
            return VGroup(lab("dynein", V(c[0] + 3.2, c[1] - 2.0), 30, PINK, weight=BOLD),
                          leader(V(c[0] + 2.55, c[1] - 2.0), V(c[0] + 1.14, c[1] - 2.0), PINK, 3))
        dl = always_redraw(dyn_label)
        self.play(FadeIn(lg), FadeIn(dl), run_time=0.6)
        self.at("drags it")
        self.at("along microtubules")
        ml = VGroup(lab("microtubule", V(-4.8, TY + 0.55), 32, TEXT), leader(V(-5.6, TY + 0.3), V(-5.9, TY + 0.1), TEXT, 3))
        self.play(FadeIn(ml), run_time=0.4)
        self.at("toward the cell body")
        ar = Arrow(V(2.0, 2.95), V(-5.6, 2.95), buff=0, color=LBL, stroke_width=7, tip_length=0.3)
        al = lab("toward the cell body", V(-1.8, 3.4), 30, TEXT)
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Speed(SpokenScene):
    """Pull back to the whole neuron: about a micrometre per second means a few hours for a centimetre."""

    def construct(self):
        r = Rig(0.9)
        P = r.P
        r.add_to(self, label=False)
        self.at("at roughly", lead=0.0)
        ev = endo(P(4.7, 0.0), 0.8)
        self.play(FadeIn(ev, scale=0.6), run_time=0.4)
        t0 = {"t": 0.0}

        def go(m, dt):
            t0["t"] += dt
            a = clip01(t0["t"] / 4.5)
            m.move_to(P(4.7 + (-4.0 - 4.7) * a, 0.0))
        ev.add_updater(go)
        self.at("micrometer")
        l1 = T("about 1 µm per second", 44, TEAL).move_to([0, -1.55, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("each second")
        el = lab("endosome", ev.get_center() + V(0.0, 0.95), 26, TEAL)
        self.add(el)
        el.add_updater(lambda m: m.move_to(ev.get_center() + V(0.0, 0.95)))
        self.at("a centimeter takes")
        a = T("1 cm = 10,000 µm = 10,000 s", 40, TEXT)
        b = T("≈ 3 hours", 46, TEAL, weight=BOLD)
        row = VGroup(a, b).arrange(RIGHT, buff=0.35).move_to([0, -2.6, 0])
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.5)
        self.at("few hours")
        self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
LANES = [2.1, 0.1, -1.9]
X_START, X_END = 4.9, -3.5
HALF_MIN = [5.0, 60.0, 600.0]            # the lesson's table: halves every 5 minutes, 1 hour, 10 hours
LIFE_TXT = ["halves every 5 minutes", "halves every hour", "halves every 10 hours"]
OUT_TXT = ["essentially none", "one in eight", "about four in five"]
TRIP_MIN = 180.0                          # a 3-hour trip


def able(k, p):
    """Fraction still able to signal after a fraction p of the 3-hour trip, for a complex that halves every HALF_MIN[k] minutes."""
    return 2.0 ** (-(TRIP_MIN * p) / HALF_MIN[k])


def set_glow(e, g):
    g = float(np.clip(g, 0.0, 1.0)) ** 0.6
    col = lambda c: interpolate_color(ManimColor(GREY), ManimColor(c), g)
    e[0].set_fill(TEAL, 0.22 * g)
    e[1].set_stroke(col(TEAL), 4).set_fill(col(TEAL), 0.18)
    e[2].set_stroke(col(TRKA), 2).set_fill(col(TRKA), 0.9)
    e[3].set_stroke(col(YELLOW), 2).set_fill(col(YELLOW), 1)


def lanes_static():
    body = RoundedRectangle(corner_radius=0.3, width=1.8, height=6.0, stroke_color=GREY, stroke_width=3, fill_color=SOLID,
                            fill_opacity=1).move_to(V(-5.8, 0.1))
    nuc = Circle(radius=0.6, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to(V(-5.8, 0.1))
    cbl = lab("cell body", V(-5.8, -3.4), 28, LBL)
    tracks = VGroup(*[Line(V(6.1, y), V(-4.9, y), color=LBL, stroke_width=6) for y in LANES])
    return body, nuc, cbl, tracks


class S24Life(SpokenScene):
    """Three endosomes set off on a 3-hour trip; one loses its glow within minutes, one dims, one is still bright."""

    def construct(self):
        body, nuc, cbl, tracks = lanes_static()
        evs = [endo(V(X_START, y), 1.0) for y in LANES]
        tx = lambda k, x: V(float(np.clip(x, -2.4, 4.4)), LANES[k] + 0.8)
        labs = [lab(LIFE_TXT[k], tx(k, X_START), 26, LBL) for k in range(3)]
        il = lab("illustrative lifetimes", V(4.0, -3.4), 26, LBL)
        self.add(body, nuc, cbl, tracks)
        self.add(*evs, *labs, il)
        clk = clock_tracker(self)
        TT = 4.0
        prog = lambda: clip01(clk.get_value() / TT)
        for k, e in enumerate(evs):
            def upd(m, dt, k=k):
                p = prog()
                m.move_to(V(X_START + (X_END - X_START) * p, LANES[k]))
                set_glow(m, able(k, p))
            e.add_updater(upd)
            labs[k].add_updater(lambda m, k=k: m.move_to(tx(k, evs[k][1].get_center()[0])))
        timer = always_redraw(lambda: T(f"trip time: {3.0 * prog():.1f} hours", 34, TEAL).move_to(V(-0.8, -3.4)))
        self.add(timer)
        self.at("so what arrives", lead=0.0)
        self.at("carrying alone")
        marks = VGroup(cross(V(-4.4, LANES[0]), RED, 0.22, 7),
                       tick(V(-4.4, LANES[1]), GREEN, 0.26, 7).set_stroke(opacity=0.5),
                       tick(V(-4.4, LANES[2]), GREEN, 0.26, 7))
        res = ["essentially none able", "one in eight still able", "about four in five still able"]
        cols = [RED, TEXT, GREEN]
        outs = VGroup(*[VGroup(lab(LIFE_TXT[k], V(-2.4, LANES[k] + 1.2), 26, LBL), lab(res[k], V(-2.4, LANES[k] + 0.74), 26, cols[k]))
                        for k in range(3)])
        for k in range(3):
            labs[k].clear_updaters()
        self.play(Create(marks), FadeOut(VGroup(*labs)), FadeIn(outs), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25Hold(SpokenScene):
    """The model is favoured, not proven: hold the question."""

    def construct(self):
        self.at("this model", lead=0.0)
        cell = cell_icon(V(-4.9, 1.8), 1.1)
        mt = Line(V(-3.6, 0.6), V(4.3, 0.6), color=GREY, stroke_width=6)
        e = endo(V(0.3, 1.8), 1.5)
        lg = VGroup(*[Line(V(0.3 + 0.18 * sg, 1.15), V(0.3 + 0.5 * sg, 0.62), color=PINK, stroke_width=7) for sg in (-1, 1)])
        tip = RoundedRectangle(corner_radius=0.12, width=0.9, height=2.4, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.14).move_to(V(5.5, 1.8))
        arrow = Arrow(V(3.3, 3.2), V(-3.3, 3.2), buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        self.play(FadeIn(VGroup(cell, mt, tip)), run_time=0.5)
        self.play(FadeIn(e, scale=0.7), FadeIn(lg), GrowArrow(arrow), run_time=0.6)
        self.at("favored")
        fav = T("favoured", 50, GREEN, weight=BOLD)
        self.play(FadeIn(fav.move_to(V(-1.6, -0.5)), shift=UP * 0.1), run_time=0.5)
        self.at("but is it proven")
        nop = T(", not proven", 50, RED, weight=BOLD).next_to(fav, RIGHT, buff=0.05, aligned_edge=DOWN)
        q = T("?", 190, TEXT, weight=BOLD).move_to(V(0, -2.3))
        self.play(FadeIn(nop, shift=UP * 0.1), FadeIn(q, scale=0.6), run_time=0.7)
        self.at("hold that question")
        self.play(Indicate(q, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S26Take(SpokenScene):
    """Act out the takeaway; s27 alone prints the complete sentence."""

    def construct(self):
        self.at("take away", lead=0.0)
        tl = T("Takeaway", 34, TEAL, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(tl, shift=DOWN * 0.1), run_time=0.4)
        self.at("a survival signal")
        tipb = RoundedRectangle(corner_radius=0.12, width=1.0, height=2.4, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.14).move_to(V(5.6, 0.0))
        cell = cell_icon(V(-4.8, 0.0), 1.25)
        path = Arrow(V(4.9, 0.0), V(-3.4, 0.0), buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        sig = lit(V(4.6, 0.0), YELLOW, 0.28)
        self.play(FadeIn(tipb), FadeIn(cell), Create(path), FadeIn(sig, scale=0.6), run_time=0.8)
        self.at("must make it home")
        self.play(sig.animate.move_to(V(-3.3, 0.0)), run_time=0.7)
        self.at("still able to signal")
        arrived = tick(V(-3.3, -0.95), GREEN, 0.4, 9)
        self.play(*[sig[i].animate.set_color(GREEN) for i in range(3)], cell[0].animate.set_stroke(GREEN),
                  Create(arrived), run_time=0.5)
        self.finish()


class S27End(EndCard):
    """The clean end card: the line is simply there (no slow fade in from black)."""
    LINE = "A survival signal must make it home still able to signal."

    def construct(self):
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.add(g)
        self.play(FadeIn(g), run_time=0.2)
        self.finish()
