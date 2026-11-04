"""The Second Brake: Competence to Die  (Biochemistrypedia explainer, chapter 5 of 6,
"The Death Machinery in Neurons").  Timed to the SPOKEN words: every self.at("...") waits for that phrase
in audio/words.json.

COLOR MAP (one colour per concept, shared with the other chapters; taken from scenes.old.py)
  BLUE   = the neuron / a living cell, and every "survives / lives / alive" outcome
  YELLOW = NGF, the survival signal, and the brakes it applies (brake 2, the unknown block)
  TEAL   = new gene expression / new protein, the drug that blocks protein synthesis
  ORANGE = pro-death BCL-2 family proteins (Bax)
  PINK   = cytochrome c
  PURPLE = Apaf-1 and the apoptosome wheel
  RED    = the killers (caspases), death, "removed / crossed out"
  GREEN  = XIAP and the caspase inhibitor only (never an outcome)
  GREY   = mitochondrion outline, labels, dead or inactive things (all debris), clock, control injection
  WHITE  = the gate bar, the microglial cell, plain emphasis (as in chapter 4)
  GOLD   = the "eat me" signal (phosphatidylserine)
  INDIGO = (new in chapter 5) Smac, the mitochondrial protein that removes inhibitors from caspases
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B070E8"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
WHITE = TEXT
INDIGO = "#6E8BFF"
LIVE = BLUE


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, pad=0.22, **kw):
    label = T(text, size=size, color=color, line_spacing=1.05)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(box)
    return VGroup(back, box, label.move_to(box))


def dim(m, f=0.3):
    """scale every stroke and fill opacity of m by f (set_opacity would brighten faint fills)"""
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * f)
        sm.set_fill(opacity=sm.get_fill_opacity() * f)
    return m


def dimmed(m, f=0.3):
    return dim(m.copy(), f)


def dimchip(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def litchip(c, color, fill=0.38):
    return [c[1].animate.set_stroke(color, opacity=1).set_fill(color, fill), c[2].animate.set_color(color).set_opacity(1)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def pulse(mobs, color, f=1.08):
    """Indicate each mobject on its own (Indicate on a VGroup scales about the group centre and spreads the parts)"""
    return AnimationGroup(*[Indicate(m, color=color, scale_factor=f) for m in mobs])


def P3(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# the neuron with its mitochondrion and gate (scales with R)
# ---------------------------------------------------------------------------------------------
C0 = P3(-1.7, -0.3)
R0 = 2.6


def cellview(c=C0, R=R0, gate_color=WHITE):
    """neuron body, four stubs, mitochondrion with cytochrome c inside, and the gate bar on its top edge."""
    c = np.array(c, float)
    k = R / 2.6
    body = Circle(radius=R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to(c)
    stubs = VGroup()
    for ang in (150, 210, 30, 330):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(c + v * R, c + v * (R + 0.3 * max(k, 0.7)), color=BLUE, stroke_width=4))
    mc = c + P3(0, -0.45 * R)
    mito = RoundedRectangle(corner_radius=0.22 * R, width=1.4 * R, height=0.5 * R, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to(mc)
    cyt = VGroup(*[Dot(mc + P3(dx * R, dy * R), radius=0.065 * R, color=PINK)
                   for dx, dy in [(-0.45, 0.09), (0, 0.09), (0.45, 0.09), (-0.45, -0.09), (0, -0.09), (0.45, -0.09)]])
    gx, gy = c[0] - 0.23 * R, mc[1] + 0.25 * R
    gate = Line([gx - 0.17 * R, gy, 0], [gx + 0.17 * R, gy, 0], color=gate_color, stroke_width=max(7, 10 * k))
    g = VGroup(body, stubs, mito, cyt, gate)
    g.body, g.stubs, g.mito, g.cyt, g.gate = body, stubs, mito, cyt, gate
    return g


def gate_xy(c=C0, R=R0):
    return P3(c[0] - 0.23 * R, c[1] - 0.45 * R + 0.25 * R)


def site(c=C0, R=R0):
    """where injected material sits in the cytoplasm"""
    return np.array(c, float) + P3(0.28 * R, 0.45 * R)


def needle(tip, top):
    tip, top = np.array(tip, float), np.array(top, float)
    d = (top - tip) / np.linalg.norm(top - tip)
    p = np.array([-d[1], d[0], 0])
    pts = [top + p * 0.2, top - p * 0.2, tip + d * 0.55 - p * 0.05, tip, tip + d * 0.55 + p * 0.05]
    return Polygon(*pts, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.3)


def main_needle():
    s = site()
    return needle(s + P3(0, 0.62), s + P3(0, 2.85))


def drops(center, color=PINK, r=0.11, n=6):
    offs = [(-0.38, 0.12), (0.0, 0.34), (0.38, 0.1), (-0.2, -0.2), (0.22, -0.24), (0.0, 0.0)][:n]
    return VGroup(*[Dot(np.array(center, float) + P3(dx, dy), radius=r, color=color) for dx, dy in offs])


def ngf_ring(c=C0, R=R0, n=12, dr=0.55, color=YELLOW, r=0.12):
    c = np.array(c, float)
    return VGroup(*[Dot(c + (R + dr) * P3(np.cos(a), np.sin(a)), radius=r, color=color)
                    for a in np.arange(n) * TAU / n + np.radians(10)])


def frags(c, R, color=GREY, n=7):
    c = np.array(c, float)
    g = VGroup()
    dirs = []
    for i in range(n):
        a = TAU * i / n + 0.4
        u = P3(np.cos(a), np.sin(a))
        dirs.append(u)
        g.add(Circle(radius=R * (0.17 + 0.07 * (i % 3)), stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.3).move_to(c + u * R * 0.42))
    g.dirs = dirs
    return g


def broken(c, R):
    """the debris of a dead neuron, in its final (spread) position"""
    fr = frags(c, R)
    for f, u in zip(fr, fr.dirs):
        f.shift(u * 0.3 * R)
    return fr


def break_up(scene, fade, c, R, run=0.5, color=GREY, extra=(), extra2=(), run2=0.8):
    fr = frags(c, R, color)
    scene.play(FadeOut(fade), LaggedStart(*[FadeIn(f, scale=0.6) for f in fr], lag_ratio=0.08), *extra, run_time=run)
    scene.play(*[f.animate.shift(u * 0.3 * R) for f, u in zip(fr, fr.dirs)], *extra2, run_time=run2)
    return fr


def clock(c, r=0.75):
    c = np.array(c, float)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(c)
    ticks = VGroup(*[Line(c + 0.8 * r * u, c + 0.97 * r * u, color=GREY, stroke_width=3) for u in (UP, DOWN, LEFT, RIGHT)])
    hand = Line(c, c + 0.68 * r * UP, color=TEXT, stroke_width=5)
    g = VGroup(face, ticks, hand)
    g.hand, g.c = hand, c
    return g


def spin(g, turns=1.0):
    return Rotate(g.hand, angle=-TAU * turns, about_point=g.c, rate_func=linear)


def caspase(c, w=2.6, h=2.0, with_cap=True, fill=0.3):
    """a labelled-cartoon caspase: a rounded block with a notch (the active site); XIAP is a green cap that plugs it."""
    c = np.array(c, float)
    body = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=RED, stroke_width=4,
                            fill_color=RED, fill_opacity=fill).move_to(c)
    nw, nh = 0.36 * w, 0.26 * h
    top = c[1] + h / 2
    cut = Rectangle(width=nw, height=nh, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([c[0], top - nh / 2 + 0.02, 0])
    edge = VGroup(Line([c[0] - nw / 2, top, 0], [c[0] - nw / 2, top - nh, 0], color=RED, stroke_width=4),
                  Line([c[0] - nw / 2, top - nh, 0], [c[0] + nw / 2, top - nh, 0], color=RED, stroke_width=4),
                  Line([c[0] + nw / 2, top - nh, 0], [c[0] + nw / 2, top, 0], color=RED, stroke_width=4))
    cap = RoundedRectangle(corner_radius=0.16, width=nw + 0.3, height=nh + 0.28, stroke_color=GREEN, stroke_width=4,
                           fill_color=GREEN, fill_opacity=0.55).move_to([c[0], top - nh / 2 + 0.12, 0])
    g = VGroup(body, cut, edge, cap)
    g.body, g.cap = body, cap
    if not with_cap:
        cap.set_opacity(0)
    return g


def wheel(c, R=1.0, ghost=False):
    """an apoptosome: a plain ring of seven Apaf-1 chips (the lesson's seven-spoked wheel)"""
    c = np.array(c, float)
    ring = [c + R * P3(np.cos(a), np.sin(a)) for a in np.linspace(0, TAU, 7, endpoint=False) + np.pi / 2]
    if ghost:
        subs = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.12, width=0.58 * R, height=0.58 * R, stroke_color=GREY,
                                                        stroke_width=3, fill_opacity=0).move_to(p), num_dashes=14) for p in ring])
    else:
        subs = VGroup(*[RoundedRectangle(corner_radius=0.12, width=0.58 * R, height=0.58 * R, stroke_color=PURPLE, stroke_width=3.5,
                                         fill_color=PURPLE, fill_opacity=0.4).move_to(p) for p in ring])
    return subs


def mito_box(c, w=3.8, h=2.4, cyt=True, gate=False):
    c = np.array(c, float)
    body = RoundedRectangle(corner_radius=0.55, width=w, height=h, stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.15).move_to(c)
    g = VGroup(body)
    g.body = body
    if cyt:
        g.cyt = VGroup(*[Dot(c + P3(dx * w, dy * h), radius=0.15, color=PINK)
                         for dx, dy in [(-0.28, 0.12), (0, 0.12), (0.28, 0.12), (-0.28, -0.14), (0, -0.14), (0.28, -0.14)]])
        g.add(g.cyt)
    if gate:
        g.gate = Line(c + P3(-0.7, h / 2), c + P3(0.7, h / 2), color=WHITE, stroke_width=12)
        g.add(g.gate)
    return g


# ---------------------------------------------------------------------------------------------
# scene-spanning states, written once so that a held question is rebuilt identically
# ---------------------------------------------------------------------------------------------
CARD_X = 4.4


def q1_state():
    """experiment 1: the injected neuron in NGF, and the question card"""
    P = {}
    P["cell"] = cellview()
    P["ring"] = ngf_ring()
    P["nlab"] = T("NGF", 26, YELLOW, weight=BOLD).move_to([1.15, 2.65, 0])
    P["needle"] = main_needle()
    P["dots"] = drops(site() + P3(0, -0.15))
    P["head"] = T("Experiment 1", 26, GREY).move_to([CARD_X, 3.2, 0])
    P["c_inj"] = bchip("cytochrome c injected", PINK, 26).move_to([CARD_X + 0.3, 2.1, 0])
    P["c_ngf"] = bchip("kept in NGF", YELLOW, 26).move_to([CARD_X, 0.95, 0])
    P["q"] = T("If the gate is the\nonly brake, what\nshould happen?", 30, TEXT, line_spacing=0.9).move_to([CARD_X, -1.2, 0])
    return P


Q2C = P3(-2.6, -0.3)


def q2_state():
    """the Smac test: NGF present, inhibitor removed, plus cytochrome c (pipette and dots drawn in the cell)"""
    c = Q2C
    st = site(c, R0)
    P = {}
    P["cell"] = cellview(c, R0)
    P["ring"] = ngf_ring(c, R0)
    P["needle"] = needle(st + P3(0, 0.62), st + P3(0, 2.85))
    P["dots"] = drops(st + P3(0, -0.15))
    P["head"] = T("A test", 26, GREY).move_to([CARD_X + 0.9, 3.2, 0])
    P["c_ngf"] = bchip("NGF present", YELLOW, 26).move_to([CARD_X + 0.9, 2.2, 0])
    P["c_x"] = bchip("no XIAP", GREEN, 26).move_to([CARD_X + 0.9, 1.05, 0])
    P["c_cyt"] = bchip("cytochrome c\ninjected", PINK, 26).move_to([CARD_X + 0.9, -0.3, 0])
    P["q"] = T("?", 100, TEXT, weight=BOLD).move_to([CARD_X + 0.9, -2.0, 0])
    return P


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Death Machinery in Neurons"
    TITLE = "The Second Brake: Competence to Die"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    """a neuron with a closed gate; cytochrome c is injected; would it die, even in NGF?"""

    def construct(self):
        cell = cellview()
        glab = T("gate", 26, WHITE).move_to(gate_xy() + P3(0, 0.38))
        brake = T("brake", 26, YELLOW, weight=BOLD).move_to(gate_xy() + P3(0.0, 0.8))
        dots = drops(site() + P3(0, -0.15))
        clab = T("cytochrome c", 26, PINK).move_to([3.7, 1.2, 0])
        lead = Line([2.45, 1.2, 0], site() + P3(0.5, -0.15), color=PINK, stroke_width=3)
        exp = bchip("should die", RED, 30).move_to([4.2, 0.0, 0])
        ring = ngf_ring()
        nlab = T("NGF", 26, YELLOW, weight=BOLD).move_to([1.15, 2.65, 0])
        q = T("?", 110, TEXT, weight=BOLD).move_to([4.2, -1.8, 0])

        self.add(cell)
        self.at("the gate")
        self.play(FadeIn(glab), Flash(cell.gate.get_center(), color=WHITE, flash_radius=0.6, line_length=0.15), run_time=0.6)
        self.at("were the only")
        self.play(FadeIn(brake, shift=DOWN * 0.1), cell.gate.animate.set_color(YELLOW), run_time=0.6)
        self.at("injected cytochrome")
        self.play(FadeIn(dots, shift=DOWN * 0.5), run_time=0.7)
        self.play(FadeIn(clab), Create(lead), run_time=0.5)
        self.at("should kill")
        self.play(FadeIn(exp, shift=UP * 0.15), run_time=0.6)
        self.at("even in")
        self.play(FadeIn(ring, lag_ratio=0.05), FadeIn(nlab), run_time=0.9)
        self.at("does it")
        self.play(FadeOut(exp), FadeIn(q, scale=0.6), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    """Deshmukh tested this directly with cultured sympathetic neurons"""

    def construct(self):
        cell = cellview()
        ring = ngf_ring()
        nlab = T("NGF", 26, YELLOW, weight=BOLD).move_to([1.15, 2.65, 0])
        self.add(cell, ring, nlab)
        cred = bchip("Deshmukh, 1998", WHITE, 32).move_to([4.3, 1.6, 0])
        lab = T("cultured sympathetic\nneurons", 28, BLUE, line_spacing=0.9).move_to([4.3, -0.3, 0])
        lead = Line([2.7, -0.3, 0], [0.55, -0.3, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(cred, shift=DOWN * 0.15), run_time=0.7)
        self.at("cultured")
        self.play(FadeIn(lab), Create(lead), run_time=0.7)
        self.play(Indicate(cell.body, color=BLUE, scale_factor=1.03), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """a glass needle injects cytochrome c into the cytoplasm"""

    def construct(self):
        cell = cellview()
        ring = ngf_ring()
        nlab = T("NGF", 26, YELLOW, weight=BOLD).move_to([1.15, 2.65, 0])
        self.add(cell, ring, nlab)
        nd = main_needle()
        nlabel = T("glass needle", 26, WHITE).move_to([2.2, 3.2, 0])
        nline = Line([1.0, 3.2, 0], site() + P3(0.3, 2.4), color=WHITE, stroke_width=3)
        dots = drops(site() + P3(0, -0.15))
        clab = T("cytochrome c", 26, PINK).move_to([3.7, 0.9, 0])
        lead = Line([2.45, 0.9, 0], site() + P3(0.5, -0.15), color=PINK, stroke_width=3)
        cyto = T("cytoplasm", 26, GREY).move_to([3.7, -0.3, 0])
        ca = arr([2.5, -0.3, 0], [0.4, -0.25, 0], GREY, 4, 0.2)
        self.at("fine glass")
        self.play(FadeIn(nd, shift=DOWN * 1.2), run_time=0.9)
        self.play(FadeIn(nlabel), Create(nline), run_time=0.4)
        self.at("injected")
        self.play(FadeIn(dots, shift=DOWN * 0.4), run_time=0.7)
        self.play(FadeIn(clab), Create(lead), run_time=0.4)
        self.at("straight into")
        self.play(FadeIn(cyto), GrowArrow(ca), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    """the injection skips the gate; the injected neuron glows with dye"""

    def construct(self):
        cell = cellview()
        ring = ngf_ring()
        nlab = T("NGF", 26, YELLOW, weight=BOLD).move_to([1.15, 2.65, 0])
        nd = main_needle()
        dots = drops(site() + P3(0, -0.15))
        glab = T("gate", 26, WHITE).move_to(gate_xy() + P3(0, 0.38))
        glow = Circle(radius=R0 - 0.02, stroke_width=0, fill_color=TEXT, fill_opacity=0.0).move_to(C0)
        halo = Circle(radius=R0 + 0.1, stroke_color=TEXT, stroke_width=0, fill_opacity=0).move_to(C0)
        self.add(glow, cell, ring, nlab, nd, dots, halo)
        dye = T("dye marks the\ninjected neuron", 28, TEXT, line_spacing=0.9).move_to([4.4, 1.6, 0])
        by = ArcBetweenPoints(P3(-0.45, 0.62), P3(2.2, -1.3), angle=-TAU / 6, color=PINK, stroke_width=7)
        by.add_tip(tip_length=0.28)
        skip = T("gate skipped", 34, WHITE, weight=BOLD).move_to([4.5, -1.3, 0])
        self.play(glow.animate.set_fill(TEXT, 0.4), halo.animate.set_stroke(TEXT, width=10, opacity=0.65), FadeIn(dye), run_time=0.6)
        self.at("skips the")
        self.play(Create(by), FadeIn(skip), FadeIn(glab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    """experiment 1: kept in NGF; if the gate is the only brake, what should happen?"""

    def construct(self):
        Q = q1_state()
        self.add(Q["cell"], Q["ring"], Q["nlab"], Q["needle"], Q["dots"], Q["head"])
        self.at("inject neurons")
        self.play(FadeIn(Q["c_inj"], shift=LEFT * 0.2), run_time=0.5)
        self.at("kept in")
        self.play(FadeIn(Q["c_ngf"], shift=LEFT * 0.2), Indicate(Q["ring"], color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("if the gate")
        self.play(FadeIn(Q["q"], shift=UP * 0.1), run_time=1.0)
        self.at("what should happen")
        self.play(Indicate(Q["q"], color=TEXT, scale_factor=1.06), run_time=0.7)
        self.finish()


class S06Pause(NarratedScene):
    """silent pause: the question stays on screen, still"""

    def construct(self):
        Q = q1_state()
        self.add(*Q.values())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(SpokenScene):
    """they should die; they survived"""

    def construct(self):
        Q = q1_state()
        self.add(*Q.values())
        die = T("should\ndie", 40, RED, weight=BOLD, line_spacing=0.9).move_to(Q["q"])
        ok = T("survived", 44, LIVE, weight=BOLD).move_to(Q["q"])
        self.at("should die")
        self.play(FadeOut(Q["q"]), FadeIn(die, scale=0.9), run_time=0.5)
        self.at("survived")
        self.play(ReplacementTransform(die, ok), Indicate(Q["cell"].body, color=LIVE, scale_factor=1.03), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
CELL2 = P3(1.2, -0.3)
R2 = 2.5
LEFT_X = -4.4


def left_mini():
    c = P3(-4.6, 0.5)
    g = cellview(c, 1.4)
    ring = ngf_ring(c, 1.4, n=10, dr=0.4, r=0.1)
    l1 = T("in NGF", 26, YELLOW).move_to([-4.6, -1.8, 0])
    l2 = T("survives", 30, LIVE, weight=BOLD).move_to([-4.6, -2.35, 0])
    return VGroup(g, ring, l1, l2)


class S08(SpokenScene):
    """second panel: no NGF for about a day, gate held shut"""

    def construct(self):
        Q = q1_state()
        self.add(*Q.values())
        ok = T("survived", 44, LIVE, weight=BOLD).move_to(Q["q"])
        self.remove(Q["q"])
        self.add(ok)
        mini = left_mini()
        cell2 = cellview(CELL2, R2)
        ring2 = ngf_ring(CELL2, R2)
        clk = clock([5.6, 2.2, 0], 0.7)
        clab = T("about a day", 26, GREY).move_to([5.6, 1.1, 0])
        old = VGroup(*[v for k, v in Q.items() if k != "q"], ok)
        self.play(FadeOut(old), FadeIn(mini), FadeIn(cell2), FadeIn(ring2), run_time=0.4)
        self.at("take")
        self.play(*[d.animate.shift((d.get_center() - CELL2) * 0.35).set_opacity(0) for d in ring2], run_time=0.7)
        self.at("away for about")
        self.play(FadeIn(clk), FadeIn(clab), run_time=0.4)
        self.play(spin(clk, 1.0), run_time=1.3)
        self.at("but keep each")
        gl = T("gate held shut", 26, WHITE).move_to(cell2.gate.get_center() + P3(0.35, 0.42))
        self.play(FadeIn(gl), Flash(cell2.gate.get_center(), color=WHITE, flash_radius=0.7, line_length=0.18), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s09_objs():
    O = {}
    O["cell"] = cellview(CELL2, R2)
    O["clk"] = clock([5.6, 2.2, 0], 0.7)
    O["clab"] = T("about a day", 26, GREY).move_to([5.6, 1.1, 0])
    O["gl"] = T("gate held shut", 26, WHITE).move_to(O["cell"].gate.get_center() + P3(0.35, 0.42))
    O["head"] = T("two ways to\nkeep it shut", 26, GREY, line_spacing=0.9).move_to([LEFT_X, 2.7, 0])
    O["w1"] = bchip("protein synthesis\nblocked", TEAL, 26).move_to([LEFT_X, 1.0, 0])
    O["or"] = T("or", 26, GREY).move_to([LEFT_X, -0.1, 0])
    O["w2"] = bchip("no Bax", ORANGE, 28).move_to([LEFT_X, -1.0, 0])
    O["nd"] = needle(site(CELL2, R2) + P3(0, 0.62), site(CELL2, R2) + P3(0, 2.85))
    O["dots"] = drops(site(CELL2, R2) + P3(0, -0.15))
    O["alive"] = T("alive", 36, LIVE, weight=BOLD).move_to([5.1, -0.7, 0])
    return O


class S09(SpokenScene):
    """two ways to keep the gate shut; the deprived neurons were alive when injected"""

    def construct(self):
        mini = left_mini()
        O = s09_objs()
        self.add(mini, O["cell"], O["clk"], O["clab"], O["gl"])
        self.play(FadeOut(mini), FadeIn(O["head"]), run_time=0.6)
        self.at("blocking protein")
        self.play(FadeIn(O["w1"], shift=RIGHT * 0.2), run_time=0.6)
        self.at("or by using")
        self.play(FadeIn(O["or"]), FadeIn(O["w2"], shift=RIGHT * 0.2), run_time=0.7)
        self.at("these neurons were")
        self.play(FadeIn(O["nd"], shift=DOWN * 1.0), run_time=0.7)
        self.at("alive when")
        self.play(FadeIn(O["alive"], shift=UP * 0.15), run_time=0.5)
        self.at("injected")
        self.play(FadeIn(O["dots"], shift=DOWN * 0.4), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
PX = [-4.5, 0.0, 4.5]
PY = 0.45
PR = 1.8
LAB1, LAB2, RES = -1.95, -2.4, -3.1


def inhib_dots(px):
    return VGroup(*[Dot(P3(px - 0.55 + 0.37 * i, PY + 0.35 + (0.24 if i % 2 else -0.05)), radius=0.11, color=GREEN) for i in range(3)])


def panel_needle(px, tip_dx=0.4):
    tip = P3(px + tip_dx, PY + 1.0)
    return needle(tip, tip + P3(0.9, 1.5))


def panel_dots(px, color):
    return drops(P3(px + 0.4, PY + 0.65), color, 0.11, 4)


def panel_head():
    return T("no NGF for about a day, gate held shut", 28, TEXT).move_to([0, 3.4, 0])


def p2_parts():
    return dict(cell=cellview(P3(PX[1], PY), PR), nd=panel_needle(PX[1]), dots=panel_dots(PX[1], GREY),
                lab=T("control injection", 26, GREY).move_to([PX[1], LAB1, 0]),
                lab2=T("(no cytochrome c)", 26, GREY).move_to([PX[1], LAB2, 0]),
                res=T("lives", 36, LIVE, weight=BOLD).move_to([PX[1], RES, 0]))


def p3_parts():
    return dict(cell=cellview(P3(PX[2], PY), PR), nd=panel_needle(PX[2]), dots=panel_dots(PX[2], PINK), inh=inhib_dots(PX[2]),
                lab=T("cytochrome c", 26, PINK).move_to([PX[2], LAB1, 0]),
                lab2=T("+ caspase inhibitor", 26, GREEN).move_to([PX[2], LAB2, 0]),
                res=T("lives", 36, LIVE, weight=BOLD).move_to([PX[2], RES, 0]))


def p1_final():
    return VGroup(broken(P3(PX[0], PY), PR),
                  T("cytochrome c", 26, PINK).move_to([PX[0], LAB1, 0]),
                  T("dies within hours", 32, RED, weight=BOLD).move_to([PX[0], RES, 0]))


class S10(SpokenScene):
    """three injections: cytochrome c kills; control does not; with a caspase inhibitor it lives"""

    def construct(self):
        O = s09_objs()
        self.add(O["cell"], O["clk"], O["clab"], O["gl"], O["head"], O["w1"], O["or"], O["w2"], O["nd"], O["dots"], O["alive"])
        cell2, nd, dots = O["cell"], O["nd"], O["dots"]
        head = panel_head()
        n1 = panel_needle(PX[0])
        d1 = panel_dots(PX[0], PINK)
        l1 = T("cytochrome c", 26, PINK).move_to([PX[0], LAB1, 0])
        # 1. re-flow to panel 1 and settle
        k = PR / R2
        self.play(FadeOut(VGroup(O["clk"], O["clab"], O["gl"], O["head"], O["w1"], O["or"], O["w2"], O["alive"], nd, dots)),
                  cell2.animate.scale(k, about_point=CELL2).shift(P3(PX[0], PY) - CELL2),
                  FadeIn(head), FadeIn(n1, shift=DOWN * 0.3), FadeIn(d1), FadeIn(l1), run_time=0.8)
        # 2. panel 1 breaks up
        self.at("killed")
        res1 = T("dies within hours", 32, RED, weight=BOLD).move_to([PX[0], RES, 0])
        break_up(self, VGroup(cell2, n1, d1), P3(PX[0], PY), PR, run=0.4, extra=[FadeIn(res1, shift=UP * 0.15)], run2=0.8)
        # 3. control
        self.at("a control")
        P2 = p2_parts()
        self.play(FadeIn(P2["cell"]), FadeIn(P2["lab"]), FadeIn(P2["lab2"]), FadeIn(P2["nd"], shift=DOWN * 0.5), run_time=0.7)
        self.at("injection did")
        self.play(FadeIn(P2["dots"], shift=DOWN * 0.3), run_time=0.5)
        self.at("not")
        self.play(FadeIn(P2["res"], shift=UP * 0.15), Indicate(P2["cell"].body, color=LIVE, scale_factor=1.03), run_time=0.5)
        # 4. inhibitor
        self.at("caspase inhibitor")
        P3_ = p3_parts()
        self.play(FadeIn(P3_["cell"]), FadeIn(P3_["lab"]), FadeIn(P3_["lab2"]), FadeIn(P3_["nd"], shift=DOWN * 0.5),
                  FadeIn(P3_["dots"]), FadeIn(P3_["inh"]), run_time=0.8)
        self.at("prevented the")
        self.play(FadeIn(P3_["res"], shift=UP * 0.15), Indicate(P3_["cell"].body, color=LIVE, scale_factor=1.03), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
CH_Y = 0.1
BAR_X = -1.9
BAR_H = 3.6


def chain():
    P = {}
    P["c1"] = bchip("cytochrome c\nreleased", PINK, 30).move_to([-4.7, CH_Y, 0])
    P["c2"] = bchip("caspases\nactive", RED, 30).move_to([1.7, CH_Y, 0])
    P["c3"] = bchip("cell\ndies", GREY, 30).move_to([5.3, CH_Y, 0])
    P["a1"] = arr(P["c1"].get_right(), P["c2"].get_left(), GREY, 6)
    P["a2"] = arr(P["c2"].get_right(), P["c3"].get_left(), GREY, 6)
    return P


def barrier(x=BAR_X, color=YELLOW, label="?"):
    r = Rectangle(width=0.6, height=BAR_H, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.45).move_to([x, CH_Y, 0])
    t = T(label, 54, TEXT, weight=BOLD).move_to(r)
    g = VGroup(r, t)
    g.r, g.t = r, t
    return g


NGF_Y = 2.95


def keeps_arrow():
    return arr(P3(BAR_X, NGF_Y - 0.5), P3(BAR_X, CH_Y + BAR_H / 2 + 0.02), YELLOW, 6, 0.24)


class S11(SpokenScene):
    """a second, unknown block below cytochrome c release; NGF loss removes it"""

    def construct(self):
        P2, P3_ = p2_parts(), p3_parts()
        panels = VGroup(panel_head(), p1_final(), *P2.values(), *P3_.values())
        self.add(panels)
        ch = chain()
        bar = barrier()
        blab = T("unknown block", 28, YELLOW).move_to([BAR_X, CH_Y - BAR_H / 2 - 0.4, 0])
        ngf = bchip("NGF", YELLOW, 32).move_to([BAR_X, NGF_Y, 0])
        keeps = T("keeps in place", 24, YELLOW).move_to([0.45, 2.55, 0])
        self.play(FadeOut(panels), *[FadeIn(ch[k]) for k in ("c1", "c2", "c3", "a1", "a2")],
                  FadeIn(bar), FadeIn(blab), run_time=0.35)
        self.at("something below")
        self.at("cytochrome c release")
        self.play(Circumscribe(ch["c1"], color=PINK, buff=0.12), run_time=0.8)
        self.at("also changes")
        self.play(Indicate(bar, color=YELLOW, scale_factor=1.08), run_time=0.6)
        self.at("when NGF")
        self.play(FadeIn(ngf, shift=DOWN * 0.15), FadeIn(keeps), run_time=0.6)
        self.at("is taken away")
        self.play(FadeOut(keeps), ngf[1].animate.set_stroke(opacity=0.3), ngf[2].animate.set_opacity(0.3),
                  Create(xmark(ngf.get_center(), 0.3, RED, 6)), run_time=0.5)
        self.play(FadeOut(bar), FadeOut(blab), run_time=0.5)
        self.play(ch["a1"].animate.set_color(RED), *litchip(ch["c2"], RED, 0.5), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
PY0, PY1 = -2.7, 2.85
HX0 = -5.0
HS = 0.43


def hx(h):
    return HX0 + HS * h


def frac(h):
    """schematic share of injected neurons that die: a logistic rise across 15 to 20 hours, short of the ceiling"""
    return 0.85 / (1 + np.exp(-(h - 17.5) / 2.6))


def hpt(h):
    return P3(hx(h), PY0 + (PY1 - PY0 - 0.2) * frac(h))


def plot_parts():
    P = {}
    P["ax"] = Arrow([HX0, PY0, 0], [6.1, PY0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    P["ay"] = Arrow([HX0, PY0, 0], [HX0, PY1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    P["title"] = T("neurons dying after cytochrome c injection (gate held shut)", 26, GREY).move_to([-6.4, 3.45, 0], aligned_edge=LEFT)
    P["xl0"] = T("NGF removed", 26, GREY).move_to([HX0 + 1.0, PY0 - 0.42, 0])
    P["xl1"] = T("about a day", 26, GREY).move_to([hx(24) - 0.2, PY0 - 0.42, 0])
    P["t1"] = Line([hx(24), PY0 - 0.12, 0], [hx(24), PY0 + 0.12, 0], color=GREY, stroke_width=4)
    P["band"] = Rectangle(width=hx(20) - hx(15), height=PY1 - PY0 - 0.1, stroke_width=0, fill_color=RED, fill_opacity=0.12)\
        .move_to([(hx(15) + hx(20)) / 2, (PY0 + PY1) / 2 - 0.05, 0])
    P["xl15"] = T("15 to 20 hours", 26, RED).move_to([(hx(15) + hx(20)) / 2, PY0 - 0.42, 0])
    P["seg1"] = ParametricFunction(lambda h: hpt(h), t_range=[0, 14, 0.1], color=RED, stroke_width=7)
    P["seg2"] = ParametricFunction(lambda h: hpt(h), t_range=[14, 24, 0.1], color=RED, stroke_width=7)
    P["sch"] = T("schematic", 26, GREY).move_to([5.6, 3.45, 0])
    return P


def plot_state(P):
    return [P[k] for k in ("ax", "ay", "title", "xl0", "xl1", "t1", "band", "xl15", "seg1", "seg2", "sch")]


class S12(SpokenScene):
    """the share of injected neurons that die rises gradually over about a day (schematic)"""

    def construct(self):
        # carry in the end of s11
        ch = chain()
        ngf = bchip("NGF", YELLOW, 32).move_to([BAR_X, NGF_Y, 0])
        ngf[1].set_stroke(opacity=0.3)
        ngf[2].set_opacity(0.3)
        old = VGroup(ch["c1"], ch["c2"], ch["c3"], ch["a1"], ch["a2"], ngf, xmark(ngf.get_center(), 0.3, RED, 6))
        old.save_state()
        ch["a1"].set_color(RED)
        c2 = ch["c2"]
        c2[1].set_stroke(RED, opacity=1).set_fill(RED, 0.5)
        c2[2].set_color(RED).set_opacity(1)
        self.add(old)
        P = plot_parts()
        tracer = Dot(hpt(0), radius=0.14, color=TEXT)
        self.play(FadeOut(old), Create(P["ax"]), Create(P["ay"]), FadeIn(P["title"]), FadeIn(P["sch"]), FadeIn(P["xl0"]), run_time=0.7)
        self.at("gradually")
        self.add(tracer)
        self.play(MoveAlongPath(tracer, P["seg1"].copy()), Create(P["seg1"]), run_time=1.3, rate_func=linear)
        self.at("over about")
        self.play(FadeIn(P["xl1"]), FadeIn(P["t1"]), FadeIn(P["band"]), FadeIn(P["xl15"]), run_time=0.5)
        self.play(MoveAlongPath(tracer, P["seg2"].copy()), Create(P["seg2"]), run_time=2.0, rate_func=smooth)
        self.at("more and more")
        self.play(Indicate(P["seg2"], color=RED, scale_factor=1.0), run_time=1.0)
        self.play(FadeOut(tracer), run_time=0.3)
        self.finish()


class S13(SpokenScene):
    """the label on the plot: competence to die"""

    def construct(self):
        P = plot_parts()
        self.add(*plot_state(P))
        acq = T("acquired susceptibility", 28, GREY).move_to([-2.0, 0.6, 0])
        pa = arr([-0.2, 0.45, 0], hpt(19.2) + P3(-0.1, 0.1), GREY, 4, 0.2)
        comp = bchip("competence-to-die", RED, 40).move_to([-2.0, 2.0, 0])
        self.at("acquired susceptibility")
        self.play(FadeIn(acq), GrowArrow(pa), run_time=0.8)
        self.at("competence to die")
        self.play(FadeIn(comp, shift=DOWN * 0.15), run_time=0.7)
        self.play(Circumscribe(comp, color=RED, buff=0.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX, RX = -3.5, 3.5
GPY, GPR = 0.45, 2.3
CHIP_Y = -2.4
CONC_Y = -3.3


def gate_shut_panels():
    cl = cellview(P3(LX, GPY), GPR)
    cr = cellview(P3(RX, GPY), GPR)
    chl = bchip("protein synthesis blocked", TEAL, 26).move_to([LX, CHIP_Y, 0])
    chr_ = bchip("no Bax", ORANGE, 28).move_to([RX, CHIP_Y, 0])
    return cl, cr, chl, chr_


class S14(SpokenScene):
    """what does the change need? look again at how these neurons were kept alive"""

    def construct(self):
        P = plot_parts()
        acq = T("acquired susceptibility", 28, GREY).move_to([-2.0, 0.6, 0])
        pa = arr([-0.2, 0.45, 0], hpt(19.2) + P3(-0.1, 0.1), GREY, 4, 0.2)
        comp = bchip("competence-to-die", RED, 40).move_to([-2.0, 2.0, 0])
        self.add(*plot_state(P), acq, pa, comp)
        needs = T("needs ?", 40, TEXT, weight=BOLD).move_to([3.4, 3.3, 0])
        cl, cr, chl, chr_ = gate_shut_panels()
        self.play(FadeOut(P["title"]), FadeOut(P["sch"]), FadeOut(acq), FadeOut(pa),
                  *[m.animate.set_opacity(0.2) for m in plot_state(P) if m not in (P["title"], P["sch"], P["band"])],
                  P["band"].animate.set_opacity(0.05), comp.animate.move_to([-1.2, 3.3, 0]), run_time=0.7)
        self.at("need")
        self.play(FadeIn(needs, shift=LEFT * 0.15), run_time=0.5)
        self.at("look again")
        self.play(*[FadeOut(m) for m in plot_state(P) if m not in (P["title"], P["sch"])], FadeIn(cl), FadeIn(cr), run_time=0.8)
        self.play(FadeIn(chl), FadeIn(chr_), run_time=0.6)
        self.at("kept alive")
        self.play(Flash(cl.gate.get_center(), color=WHITE, flash_radius=0.7, line_length=0.18),
                  Flash(cr.gate.get_center(), color=WHITE, flash_radius=0.7, line_length=0.18), run_time=0.7)
        self.finish()


def p_needle(px):
    tip = P3(px + 0.55, GPY + 1.1)
    return needle(tip, tip + P3(0.8, 1.3))


def p_drops(px):
    return drops(P3(px + 0.55, GPY + 0.65), PINK, 0.11, 5)


def tag_nongf(px):
    return T("no NGF, about a day", 28, YELLOW).move_to([px, 3.3, 0])


class S15(SpokenScene):
    """panel 1: protein synthesis blocked, deprived, injected: the neuron dies, so the change needs no new protein"""

    def construct(self):
        comp = bchip("competence-to-die", RED, 40).move_to([-1.2, 3.3, 0])
        needs = T("needs ?", 40, TEXT, weight=BOLD).move_to([3.4, 3.3, 0])
        cl, cr, chl, chr_ = gate_shut_panels()
        self.add(comp, needs, cl, cr, chl, chr_)
        nd = p_needle(LX)
        dr = p_drops(LX)
        tag = tag_nongf(LX)
        res = T("dies: still competent", 30, RED, weight=BOLD).move_to([LX, 3.3, 0])
        stmt = T("the change needs no new protein", 34, TEAL, weight=BOLD).move_to([0, CONC_Y, 0])
        self.play(FadeOut(comp), FadeOut(needs), FadeIn(tag), Transform(cr, dimmed(cr)), Transform(chr_, dimmed(chr_)), run_time=0.5)
        self.at("made no new")
        self.play(Circumscribe(chl, color=TEAL, buff=0.12), run_time=0.8)
        self.at("yet they became")
        self.play(FadeIn(nd, shift=DOWN * 0.8), FadeIn(dr), run_time=0.6)
        self.at("competent")
        break_up(self, VGroup(cl, nd, dr), P3(LX, GPY), GPR, run=0.4, extra=[ReplacementTransform(tag, res)], run2=0.7)
        self.at("so the change")
        self.play(FadeIn(stmt, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S16(SpokenScene):
    """panel 2: Bax-null, deprived, injected: the neuron dies, so the change needs no Bax"""

    def construct(self):
        cr = cellview(P3(RX, GPY), GPR)
        chl = bchip("protein synthesis blocked", TEAL, 26).move_to([LX, CHIP_Y, 0])
        chr_ = bchip("no Bax", ORANGE, 28).move_to([RX, CHIP_Y, 0])
        fl = broken(P3(LX, GPY), GPR)
        res1 = T("dies: still competent", 30, RED, weight=BOLD).move_to([LX, 3.3, 0])
        stmt1 = T("the change needs no new protein", 34, TEAL, weight=BOLD).move_to([0, CONC_Y, 0])
        old = VGroup(fl, chl, res1)
        self.add(old, stmt1, cr, chr_)
        nd = p_needle(RX)
        dr = p_drops(RX)
        tag = tag_nongf(RX)
        res = T("dies: still competent", 30, RED, weight=BOLD).move_to([RX, 3.3, 0])
        stmt = T("it needs no Bax", 34, ORANGE, weight=BOLD).move_to([0, CONC_Y, 0])
        # Clear the preceding case and establish the injection before the result.
        self.play(FadeOut(old), FadeOut(stmt1), FadeIn(tag), FadeIn(nd, shift=DOWN * 0.5), run_time=0.35)
        self.at("lacking")
        self.play(FadeIn(dr, shift=DOWN * 0.5), run_time=0.35)
        self.wait(0.6)
        self.at("competent")
        break_up(self, VGroup(cr, nd, dr), P3(RX, GPY), GPR, run=0.4, extra=[ReplacementTransform(tag, res)], run2=0.7)
        self.at("so", lead=0.3)
        self.play(FadeIn(stmt), run_time=0.15)
        self.finish()


# ---------------------------------------------------------------------------------------------
def brake_chain():
    ch = chain()
    b1 = bchip("brake 1: the gate", WHITE, 26).move_to([-4.7, NGF_Y, 0])
    h1 = inhib(b1.get_bottom(), ch["c1"].get_top(), WHITE, 5)
    return ch, b1, h1


def change_card():
    label = T("This change needs\nno new protein and no Bax", 30, TEXT,
              weight=BOLD, line_spacing=0.9)
    panel = RoundedRectangle(width=8.6, height=1.15, corner_radius=0.12,
                             stroke_color=YELLOW, stroke_width=2.5,
                             fill_color=BG, fill_opacity=1).move_to([0, -3.0, 0])
    return VGroup(panel, label.move_to(panel))


class S17(SpokenScene):
    """deprivation removes brake 2 before the caspase arrow activates"""

    def construct(self):
        ch, b1, h1 = brake_chain()
        bar = barrier(label="")
        b2lab = T("brake 2", 30, YELLOW, weight=BOLD).move_to([BAR_X, -2.0, 0])
        ngf = bchip("NGF", YELLOW, 30).move_to([BAR_X, NGF_Y, 0])
        card = change_card()
        self.add(*ch.values(), b1, h1, bar, b2lab, ngf, card)
        self.at("a separate")
        self.play(Indicate(bar, color=YELLOW, scale_factor=1.04), run_time=0.45)
        self.at("deprivation removes")
        self.play(ngf[1].animate.set_stroke(opacity=0.3), ngf[2].animate.set_opacity(0.3),
                  Create(xmark(ngf.get_center(), 0.3, RED, 6)), run_time=0.35)
        self.play(FadeOut(bar), FadeOut(b2lab), run_time=0.5)
        # Separate plays guarantee the barrier is gone before any red appears.
        self.play(ch["a1"].animate.set_color(RED), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
CASP_X = [-4.4, 0.0, 4.4]
CASP_Y = -0.2
CW, CHH = 3.6, 3.0


def tiles(with_cap=True):
    return [caspase(P3(x, CASP_Y), CW, CHH, with_cap=with_cap) for x in CASP_X]


class S18(SpokenScene):
    """brake 2 is XIAP, a caspase inhibitor sitting on active caspases"""

    def construct(self):
        ch, b1, h1 = brake_chain()
        card = change_card()
        ngf = bchip("NGF", YELLOW, 30).move_to([BAR_X, NGF_Y, 0])
        ngf[1].set_stroke(opacity=0.3)
        ngf[2].set_opacity(0.3)
        ch["a1"].set_color(RED)
        chain_all = VGroup(*[ch[k] for k in ("c1", "c2", "c3", "a1", "a2")], b1, h1, card, ngf, xmark(ngf.get_center(), 0.3, RED, 6))
        # Carry the removed brake into the identification scene without restoring it.
        self.add(chain_all)
        blocks = tiles(with_cap=False)
        caps = VGroup(*[tiles()[i].cap for i in range(3)])
        lab = T("active caspases", 30, RED).move_to([0, -2.5, 0])
        xl = T("XIAP", 40, GREEN, weight=BOLD).move_to([0, 2.5, 0])
        xlead = Line([0, 2.15, 0], [0, CASP_Y + CHH / 2 + 0.2, 0], color=GREEN, stroke_width=4)
        self.at("identified")
        self.play(Circumscribe(card, color=YELLOW, buff=0.08), run_time=0.8)
        self.at("caspase inhibitor")
        self.play(FadeOut(chain_all), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in blocks], lag_ratio=0.15), FadeIn(lab), run_time=0.5)
        self.at("called")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.5) for c in caps], lag_ratio=0.15), run_time=0.7)
        self.wait(0.45)
        self.play(FadeIn(xl, shift=DOWN * 0.1), Create(xlead), pulse(caps, GREEN), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    """XIAP levels fall during NGF deprivation"""

    def construct(self):
        blocks = tiles()
        lab = T("active caspases", 30, RED).move_to([0, -2.5, 0])
        self.add(*blocks, lab)
        BX, BY0, BH = -2.0, -2.35, 5.0
        frame = Rectangle(width=2.2, height=BH, stroke_color=GREY, stroke_width=3).move_to([BX, BY0 + BH / 2, 0])
        high_level = BH - 0.3
        tr = ValueTracker(high_level)
        bar = always_redraw(lambda: Rectangle(width=2.2, height=max(tr.get_value(), 0.03), stroke_color=GREEN, stroke_width=2,
                                              fill_color=GREEN, fill_opacity=0.8).move_to([BX, BY0, 0], aligned_edge=DOWN))
        xl = T("XIAP level", 34, GREEN, weight=BOLD).move_to([BX, -2.95, 0])
        hi = T("high", 26, GREY).move_to([BX - 2.0, BY0 + BH - 0.3, 0])
        lo = T("low", 26, GREY).move_to([BX - 2.0, BY0 + 0.3, 0])
        sch = T("schematic", 26, GREY).move_to([5.3, -3.3, 0])
        clk = clock([3.4, 0.9, 0], 1.4)
        c0 = T("0 h", 28, GREY).move_to([3.4, -1.0, 0])
        c1 = T("about a day", 28, GREY).move_to([3.4, -1.0, 0])
        cl = T("without NGF", 28, GREY).move_to([3.4, -1.6, 0])
        ngf = bchip("NGF removed", YELLOW, 28).move_to([3.4, 3.0, 0])
        self.play(FadeOut(VGroup(*blocks, lab)), FadeIn(frame), FadeIn(bar), FadeIn(xl), FadeIn(hi), FadeIn(lo), FadeIn(sch), run_time=0.6)
        self.at("fall")
        self.play(FadeIn(clk), FadeIn(c0), FadeIn(cl), FadeIn(ngf), run_time=0.4)
        self.wait(0.45)
        # The zero-hour reading belongs only to the high starting state.
        self.play(FadeOut(c0), run_time=0.15)
        self.play(tr.animate.set_value(0.5), spin(clk, 1.0), run_time=1.6, rate_func=linear)
        self.play(FadeIn(c1), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20(SpokenScene):
    """XIAP holds caspases off, partly because the neurons have little Apaf-1"""

    def construct(self):
        blocks = tiles()
        lab = T("active caspases", 30, RED).move_to([0, -2.5, 0])
        self.add(*blocks, lab)
        WY = 0.95
        WR = 1.1
        small = [caspase(P3(x, -1.95), 2.0, 1.3, with_cap=True) for x in (-1.7, 1.7)]
        w_live = [wheel(P3(x, WY), WR) for x in (-1.7, 1.7)]
        w_ghost = [wheel(P3(x, WY), WR, ghost=True) for x in (-5.0, 5.0)]
        arrows = [arr(P3(x, WY - WR - 0.4), P3(x, -1.18), PURPLE, 5, 0.22) for x in (-1.7, 1.7)]
        wl = T("Apaf-1 wheel (apoptosome)", 30, PURPLE, weight=BOLD).move_to([-1.7, 3.1, 0])
        wlead = Line([-1.7, 2.75, 0], [-1.7, WY + WR + 0.45, 0], color=PURPLE, stroke_width=3)
        few = T("few wheels built:\nlittle Apaf-1", 28, PURPLE, line_spacing=0.9).move_to([4.6, 3.1, 0])
        xl = T("XIAP covers the small caspase output", 28, GREEN).move_to([0, -3.3, 0])
        self.at("hold caspases")
        self.play(pulse([b.cap for b in blocks], GREEN), run_time=0.8)
        self.at("partly because")
        self.play(FadeOut(VGroup(*blocks, lab)), *[FadeIn(s) for s in small], run_time=0.5)
        self.play(LaggedStart(*[FadeIn(w, scale=0.8) for w in w_live], lag_ratio=0.2), FadeIn(wl), Create(wlead), run_time=0.7)
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(xl), run_time=0.4)
        self.at("little")
        self.play(*[FadeIn(g) for g in w_ghost], FadeIn(few, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S21(SpokenScene):
    """the test: NGF present, inhibitor removed, plus cytochrome c: what should happen?"""

    def construct(self):
        Q = q2_state()
        cell = Q["cell"]
        self.add(cell, Q["head"])
        self.at("keep NGF")
        self.play(FadeIn(Q["ring"], lag_ratio=0.05), FadeIn(Q["c_ngf"], shift=LEFT * 0.2), run_time=0.9)
        self.at("remove the")
        self.play(FadeIn(Q["c_x"], shift=LEFT * 0.2), run_time=0.5)
        self.at("what should cytochrome")
        self.play(FadeIn(Q["c_cyt"], shift=LEFT * 0.2), FadeIn(Q["needle"], shift=DOWN * 0.8), FadeIn(Q["dots"]), run_time=0.7)
        self.play(FadeIn(Q["q"], scale=0.7), run_time=0.6)
        self.finish()


class S22Pause(NarratedScene):
    """silent pause: the question stays on screen, still"""

    def construct(self):
        Q = q2_state()
        self.add(*Q.values())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23(SpokenScene):
    """Smac, a mitochondrial protein, pulls XIAP off the caspases"""

    def construct(self):
        mc = P3(-3.9, 0.2)
        mito = mito_box(mc, 5.0, 3.6, cyt=False)
        mlab = T("mitochondrion", 28, GREY).move_to([-3.9, -2.2, 0])
        smacs = VGroup(*[Dot(mc + P3(dx, dy), radius=0.28, color=INDIGO) for dx, dy in [(-1.0, 0.45), (1.0, 0.45), (0.0, -0.65)]])
        sm = T("Smac", 44, INDIGO, weight=BOLD).move_to([-3.9, 2.65, 0])
        blk = caspase(P3(3.7, -0.3), 4.2, 3.3, with_cap=True)
        xl = T("XIAP", 32, GREEN, weight=BOLD).move_to([3.7, 2.2, 0])
        cl = T("caspase", 30, RED).move_to([3.7, -2.5, 0])
        self.play(FadeIn(smacs, lag_ratio=0.2), FadeIn(sm, scale=0.8), run_time=0.7)
        self.at("mitochondrial")
        self.play(FadeIn(mito), FadeIn(mlab), run_time=0.6)
        self.at("protein that")
        self.play(FadeIn(blk, scale=0.9), FadeIn(xl), FadeIn(cl), run_time=0.6)
        self.at("removes")
        grab = smacs[1]
        self.play(grab.animate.move_to(blk.cap.get_center() + P3(-1.4, 0.1)), run_time=0.5)
        self.at("inhibitors")
        lift = UP * 1.0 + RIGHT * 0.2
        self.play(blk.cap.animate.shift(lift), xl.animate.shift(lift), grab.animate.shift(lift), run_time=0.6)
        self.at("from caspases")
        self.play(blk.body.animate.set_fill(RED, 0.65), Indicate(blk.body, color=RED, scale_factor=1.04), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24(SpokenScene):
    """cytochrome c plus Smac, injected into a neuron kept in NGF: it breaks up"""

    def construct(self):
        c = Q2C
        cell = cellview(c, R0)
        ring = ngf_ring(c, R0)
        self.add(cell, ring)
        st = site(c, R0)
        nd = needle(st + P3(0, 0.62), st + P3(0, 2.85))
        dpink = drops(st + P3(0, -0.15))
        dind = VGroup(*[Dot(st + P3(dx, dy), radius=0.14, color=INDIGO) for dx, dy in [(-0.55, -0.5), (0.5, -0.55), (0.0, -0.7)]])
        l1 = T("cytochrome c", 30, PINK).move_to([4.2, 1.4, 0])
        l2 = T("+ Smac", 30, INDIGO, weight=BOLD).move_to([4.2, 0.7, 0])
        l3 = T("kept in NGF", 30, YELLOW).move_to([4.2, -0.4, 0])
        dies = T("dies", 46, RED, weight=BOLD).move_to([4.2, -1.8, 0])
        self.at("injected")
        self.play(FadeIn(nd, shift=DOWN * 1.0), FadeIn(dpink), FadeIn(l1), run_time=0.8)
        self.at("with")
        self.play(FadeIn(dind, shift=DOWN * 0.3), FadeIn(l2), run_time=0.6)
        self.at("killed")
        break_up(self, VGroup(cell, nd, dpink, dind), c, R0, run=0.4, extra=[FadeIn(dies, shift=UP * 0.15)], run2=0.6)
        self.at("kept in")
        self.play(FadeIn(l3), Indicate(ring, color=YELLOW, scale_factor=1.03), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S25(SpokenScene):
    """every result against the two brakes: the table"""

    def construct(self):
        bx = [-6.4, -1.5, 0.6, 3.3, 6.4]
        xs = [(bx[i] + bx[i + 1]) / 2 for i in range(4)]
        RH = 1.0
        TOP = 2.5
        ys = [TOP - RH * (i + 0.5) for i in range(6)]
        hy = 3.0
        rows = [("NGF present,\ncytochrome c injected", "skipped", "on", "lives"),
                ("no NGF, gate held shut,\ncytochrome c injected", "skipped", "off", "dies"),
                ("NGF present, cytochrome c\n+ Smac injected", "skipped", "removed\nby Smac", "dies"),
                ("no NGF, protein synthesis\nblocked, not injected", "stays\nshut", "off", "death\ndelayed"),
                ("no NGF, no Bax,\nnot injected", "stays\nshut", "off", "lives"),
                ("no NGF, nothing blocked,\nnot injected", "opens", "off", "dies")]
        heads = [T("gate\n(brake 1)", 26, WHITE, line_spacing=0.8).move_to([xs[1], hy, 0]),
                 T("XIAP\n(brake 2)", 26, GREEN, line_spacing=0.8).move_to([xs[2], hy, 0]),
                 T("outcome", 28, TEXT).move_to([xs[3], hy, 0])]
        grid = VGroup()
        for i in range(7):
            grid.add(Line([bx[0], TOP - RH * i, 0], [bx[-1], TOP - RH * i, 0], color=GREY, stroke_width=2, stroke_opacity=0.6))
        for x in bx[1:-1]:
            grid.add(Line([x, 3.5, 0], [x, TOP - RH * 6, 0], color=GREY, stroke_width=2, stroke_opacity=0.6))
        cells = []
        for (a, b, c_, d), y in zip(rows, ys):
            ta = T(a, 26, TEXT, line_spacing=0.75).move_to([bx[0] + 0.15, y, 0], aligned_edge=LEFT)
            tb = T(b, 26, TEXT, line_spacing=0.8).move_to([xs[1], y, 0])
            col = GREEN if c_ == "on" else (INDIGO if "Smac" in c_ else GREY)
            tc = T(c_, 26, col, line_spacing=0.8).move_to([xs[2], y, 0])
            td = T(d, 26, RED if d == "dies" else LIVE, weight=BOLD, line_spacing=0.8).move_to([xs[3], y, 0])
            cells.append((ta, tb, tc, td))

        def box(col, row, color, o=0.18):
            w = bx[col + 1] - bx[col] - 0.12
            return Rectangle(width=w, height=RH - 0.1, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=o).move_to([xs[col], ys[row], 0])

        self.play(FadeIn(grid), *[FadeIn(h) for h in heads], run_time=0.4)
        # All six results settle before the narration compares the brakes.
        self.play(*[FadeIn(m) for row in cells for m in row], run_time=0.6)
        self.at("dies by apoptosis")
        dies_b = [box(3, i, RED) for i, r in enumerate(rows) if r[3] == "dies"]
        self.play(*[FadeIn(b) for b in dies_b], run_time=0.5)
        self.at("the gate is open")
        gate_b = [box(1, i, WHITE) for i, r in enumerate(rows) if r[1] in ("opens", "skipped")]
        self.play(*[FadeIn(b) for b in gate_b], run_time=0.6)
        self.at("and the")
        off_b = [box(2, i, GREEN) for i, r in enumerate(rows) if r[2] != "on" and r[1] in ("opens", "skipped")]
        self.play(*[FadeIn(b) for b in off_b], run_time=0.6)
        self.at("is off")
        self.play(*[Indicate(m, color=RED, scale_factor=1.0) for m in dies_b], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
MB_Y0, MB_Y1 = -1.25, 1.25      # the band: inner face at the bottom, outer face at the top
IN_Y, OUT_Y = -0.72, 0.72       # rows of lipid heads: inner leaflet, outer leaflet
PS_X = [-3.5, -2.0, -0.5, 1.0, 2.5, 4.0]
CASP_XS = [-3.5, -0.5, 2.5]
CASP_Y2 = -2.75


def membrane_parts():
    P = {}
    P["band"] = Rectangle(width=12.6, height=MB_Y1 - MB_Y0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.12).move_to([0, (MB_Y0 + MB_Y1) / 2, 0])
    xs = np.arange(-6.0, 6.01, 0.5)
    P["heads"] = VGroup(*[Dot([x, y, 0], radius=0.14, color=GREY) for y in (IN_Y, OUT_Y) for x in xs
                          if not (y == IN_Y and any(abs(x - px) < 0.01 for px in PS_X))])
    P["out"] = T("outside the cell", 26, GREY).move_to([-4.6, 1.75, 0])
    P["in"] = T("inside the cell", 26, GREY).move_to([-2.0, -1.8, 0])
    return P


class S26(SpokenScene):
    """caspases expose phosphatidylserine on the outer face: an eat-me signal"""

    def construct(self):
        P = membrane_parts()
        casp = VGroup(*[caspase(P3(x, CASP_Y2), 1.7, 1.2, with_cap=False) for x in CASP_XS])
        cl = T("active\ncaspases", 28, RED, line_spacing=0.9).move_to([5.2, CASP_Y2, 0])
        beads = VGroup(*[Dot(P3(x, IN_Y), radius=0.26, color=GOLD) for x in PS_X])
        push = VGroup(*[arr(P3(x, CASP_Y2 + 0.7), P3(x, IN_Y - 0.4), RED, 6, 0.24) for x in CASP_XS])
        sig = VGroup(*[arr(P3(x, MB_Y1 + 0.1), P3(x, MB_Y1 + 1.0), GOLD, 5, 0.22) for x in (-1.5, 0.0, 1.5)])
        siglab = T("signal to be eaten", 30, GOLD).move_to([0, 2.55, 0])
        pl = T("phosphatidylserine", 30, GOLD, weight=BOLD).move_to([3.5, 2.7, 0])
        pl_lead = Line([2.9, 2.35, 0], P3(2.5, OUT_Y + 0.3), color=GOLD, stroke_width=3)
        where = bchip("where studied", GREY, 26).move_to([-3.6, 3.2, 0])
        eat = T("eat me", 60, GOLD, weight=BOLD).move_to([-1.6, 2.6, 0])
        self.add(P["band"], P["heads"])
        self.play(FadeIn(casp, lag_ratio=0.15), FadeIn(cl), run_time=0.6)
        self.play(pulse(casp, RED, 1.12), run_time=0.9)
        self.at("signals to be")
        self.play(LaggedStart(*[GrowArrow(a) for a in sig], lag_ratio=0.2), FadeIn(siglab), run_time=0.9)
        self.at("where this has")
        self.play(FadeIn(P["out"]), FadeIn(P["in"]), FadeOut(siglab), FadeOut(sig), FadeIn(where), run_time=0.6)
        self.at("expose")
        self.play(FadeIn(beads, lag_ratio=0.1, scale=1.6), LaggedStart(*[GrowArrow(a) for a in push], lag_ratio=0.15), run_time=0.9)
        self.at("phosphatidylserine")
        self.play(FadeIn(pl, shift=DOWN * 0.1), FadeIn(pl_lead), FadeOut(where), run_time=0.6)
        self.at("outer face")
        self.play(LaggedStart(*[b.animate.move_to([b.get_center()[0], OUT_Y, 0]) for b in beads], lag_ratio=0.1), run_time=1.1)
        self.at("it works as", lead=0.5)
        self.play(FadeIn(eat, scale=0.8), pulse(beads, GOLD, 1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
NC = P3(-2.6, 0.1)
NR = 1.9
MR = 2.85


def dying_neuron(c=NC, R=NR):
    body = Circle(radius=R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2).move_to(c)
    stubs = VGroup()
    for ang in (150, 210, 30, 330):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(c + v * R, c + v * (R + 0.28), color=BLUE, stroke_width=4))
    inner = VGroup(*[Dot(c + P3(dx, dy), radius=0.12, color=RED) for dx, dy in [(-0.6, 0.5), (0.5, 0.6), (0.0, -0.3), (-0.5, -0.6), (0.6, -0.25)]])
    beads = VGroup(*[Dot(c + R * P3(np.cos(a), np.sin(a)), radius=0.16, color=GOLD) for a in np.arange(12) * TAU / 12 + 0.2])
    g = VGroup(body, stubs, inner, beads)
    g.body, g.inner, g.beads = body, inner, beads
    return g


def microglia(c, R):
    c = np.array(c, float)
    body = Circle(radius=R, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0).move_to(c)
    pr = VGroup()
    for ang in (20, 80, 140, 200, 260, 320):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        pr.add(Line(c + v * R, c + v * (R + 0.3), color=WHITE, stroke_width=4))
    g = VGroup(body, pr)
    g.body = body
    return g


MGC = P3(3.9, 0.1)
MGR = 2.0


class S27(SpokenScene):
    """a microglial cell binds the exposed signal and engulfs the neuron"""

    def construct(self):
        nr = dying_neuron()
        mg = microglia(MGC, MGR)
        ml = T("microglia", 30, WHITE, weight=BOLD).move_to([MGC[0], MGC[1] + MGR + 0.5, 0])
        other = microglia(P3(5.9, -2.6), 0.6)
        ol = T("other phagocytes", 26, WHITE).move_to([3.3, -3.1, 0])
        contents = T("contents", 28, RED, weight=BOLD).move_to([-5.3, -2.65, 0])
        cl = VMobject(color=RED, stroke_width=3).set_points_as_corners(
            [P3(-5.3, -2.3), P3(-5.3, -0.5), NC + P3(-0.5, -0.6)])
        bead_ids = (11, 0, 1)
        arms = VGroup(*[Line(MGC + P3(-MGR + 0.05, dy), nr.beads[i].get_center() + P3(0.18, 0), color=WHITE, stroke_width=5)
                        for i, dy in zip(bead_ids, (-0.45, 0.0, 0.45))])
        self.add(nr, contents, cl)
        self.play(FadeIn(mg, shift=LEFT * 0.4), FadeIn(ml), run_time=0.9)
        self.at("and other")
        self.play(FadeIn(other), FadeIn(ol), run_time=0.6)
        self.at("recognize")
        self.play(FadeOut(other), FadeOut(ol), Create(arms), run_time=0.7)
        self.play(Indicate(VGroup(*[nr.beads[i] for i in bead_ids]), color=GOLD, scale_factor=1.5), run_time=0.6)
        self.at("eat the")
        mg3 = microglia(NC, MR)
        self.remove(contents, cl)
        self.play(FadeOut(arms), Transform(mg, mg3), ml.animate.move_to([NC[0], NC[1] + MR + 0.4, 0]), run_time=1.1)
        self.finish()


class S28(SpokenScene):
    """eaten before the membrane fails: contents do not spill, no inflammation"""

    def construct(self):
        nr = dying_neuron()
        mg = microglia(NC, MR)
        ml = T("microglia", 30, WHITE, weight=BOLD).move_to([NC[0], NC[1] + MR + 0.4, 0])
        self.add(mg, nr, ml)
        tl = Arrow([1.3, 2.2, 0], [6.4, 2.2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        tlab = T("time", 26, GREY).move_to([6.0, 1.75, 0])
        e1 = Dot([2.3, 2.2, 0], radius=0.14, color=GOLD)
        e1l = T("eaten", 28, GOLD).move_to([2.3, 2.8, 0])
        e2 = Dot([5.0, 2.2, 0], radius=0.14, color=GREY)
        e2l = T("membrane fails", 26, GREY).move_to([5.0, 2.8, 0])
        nospill = T("normally\nno spill", 38, WHITE, weight=BOLD, line_spacing=0.9).move_to([3.9, 0.3, 0])
        flame = T("normally\nno inflammation", 38, WHITE, weight=BOLD, line_spacing=0.9).move_to([3.9, -1.6, 0])
        self.at("normally")
        self.play(Create(tl), FadeIn(tlab), FadeIn(e1), FadeIn(e1l), run_time=0.6)
        self.at("its membrane")
        self.play(FadeIn(e2), FadeIn(e2l), run_time=0.5)
        self.play(Indicate(nr.body, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.at("so its contents")
        self.play(Indicate(nr.inner, color=RED, scale_factor=1.2), FadeIn(nospill, shift=UP * 0.15), run_time=0.9)
        self.at("the tissue")
        self.play(FadeIn(flame, shift=UP * 0.15), run_time=0.6)
        self.at("inflamed")
        self.play(Indicate(flame, color=WHITE, scale_factor=1.05), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
LCX, RCX = -3.4, 3.4
CY = 0.2
LIFT = RIGHT * 1.3 + UP * 0.95


def idea_card(brake2_on=True):
    P = {}
    P["t1"] = T("Brake 1: the gate", 34, YELLOW, weight=BOLD).move_to([LCX, 3.45, 0])
    P["m"] = mito_box(P3(LCX, CY), 5.4, 3.4, cyt=True, gate=True)
    P["g1"] = T("opened by new gene expression", 26, TEAL).move_to([LCX, -2.0, 0])
    P["t2"] = T("Brake 2: on the caspases", 34, YELLOW, weight=BOLD).move_to([RCX, 3.45, 0])
    P["k"] = caspase(P3(RCX, CY), 3.8, 3.2, with_cap=brake2_on)
    return P


def ngf_x():
    c = bchip("NGF", YELLOW, 28).move_to([RCX, -3.15, 0])
    c[1].set_stroke(opacity=0.3)
    c[2].set_opacity(0.3)
    return c, xmark(c.get_center(), 0.28, RED, 6)


class S29(SpokenScene):
    """brake 2 is on the caspases; deprivation lifts it without new protein"""

    def construct(self):
        P = idea_card()
        self.add(P["t1"], P["m"], P["g1"])
        ngf = bchip("NGF", YELLOW, 28).move_to([RCX, -3.15, 0])
        line1 = T("lifted by deprivation,", 28, YELLOW).move_to([RCX, -1.95, 0])
        line2 = T("no new protein needed", 28, TEAL).move_to([RCX, -2.45, 0])
        self.play(FadeIn(P["t2"], shift=DOWN * 0.1), FadeIn(P["k"], scale=0.9), run_time=0.8)
        self.at("is on")
        self.play(Indicate(P["k"].cap, color=GREEN, scale_factor=1.1), run_time=0.6)
        self.at("deprivation lifts")
        self.play(FadeIn(ngf, shift=UP * 0.1), FadeIn(line1), run_time=0.4)
        self.play(ngf[1].animate.set_stroke(opacity=0.3), ngf[2].animate.set_opacity(0.3), Create(xmark(ngf.get_center(), 0.28, RED, 6)),
                  P["k"].cap.animate.shift(LIFT).set_opacity(0.3), run_time=0.7)
        self.at("without new")
        self.play(FadeIn(line2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S30(SpokenScene):
    """this apoptotic route needs both brakes off"""

    def construct(self):
        P = idea_card(brake2_on=True)
        P["k"].cap.shift(LIFT).set_opacity(0.3)
        ngf, xs1 = ngf_x()
        line1 = T("lifted by deprivation,", 28, YELLOW).move_to([RCX, -1.95, 0])
        line2 = T("no new protein needed", 28, TEAL).move_to([RCX, -2.45, 0])
        self.add(P["t1"], P["m"], P["g1"], P["t2"], P["k"], ngf, xs1, line1, line2)
        goal = bchip("apoptosis", RED, 38).move_to([0, -3.1, 0])
        a1 = arr(P3(LCX, CY - 1.8), goal.get_left() + P3(-0.2, 0.1), RED, 5)
        a2 = arr(P3(RCX, CY - 1.7), goal.get_right() + P3(0.2, 0.1), RED, 5)
        self.play(FadeOut(ngf), FadeOut(xs1), FadeOut(line1), FadeOut(line2), FadeOut(P["g1"]), run_time=0.4)
        self.at("route")
        self.play(FadeIn(goal, shift=UP * 0.1), run_time=0.5)
        self.at("needs both")
        self.play(P["m"].gate.animate.shift(RIGHT * 2.0).set_opacity(0.2),
                  Flash(P["m"].gate.get_center(), color=WHITE, flash_radius=0.7, line_length=0.18), run_time=0.8)
        self.at("off")
        self.play(GrowArrow(a1), GrowArrow(a2), *litchip(goal, RED, 0.5), P["k"].body.animate.set_fill(RED, 0.65), run_time=0.7)
        self.finish()


class S31End(EndCard):
    LINE = "This apoptotic route needs both brakes off."
