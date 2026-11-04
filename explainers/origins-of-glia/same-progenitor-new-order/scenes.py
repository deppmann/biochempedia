"""Where glia come from, chapter 3: Same Progenitor, New Order  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared with every chapter of this film)
  BLUE   = radial glia / cortical progenitors (the CNS stem cell lineage), the cell body
  GREEN  = astrocytes, GFAP "on", a gate that is open
  TEAL   = oligodendrocyte lineage (not used in this chapter)
  ORANGE = yolk sac and microglia (not used in this chapter)
  PURPLE = neural crest, Schwann cells (not used in this chapter)
  TEXT   = neurons, proneural genes (white)
  PINK   = relay proteins and their binding site (JAK, STAT3, the STAT3 site)
  YELLOW = a signal or a mark passed on (cytokines CNTF / LIF / cardiotrophin-1, the P badge)
  NOTCH  = Notch signal, Notch ligands, Hes, NFIA (periwinkle)
  RECEP  = the receptor subunit gp130 (pale blue)
  RED    = a block or a loss (methyl tag, closed lock, red gate), and the open question "?"
  GREY   = outlines, gates not yet lit;  LG (light grey) = secondary labels and the other receptor parts
  Gate bar: grey = not yet named, white = named, green = open, red = blocked
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58FB4"
NOTCH = "#9FA8FF"
RECEP = "#B8E3F2"
LG = "#C9CEDA"
BARY = 3.3


# ---------------------------------------------------------------- helpers
def wt(scene, t):
    """Wait until t seconds into the scene (for beats the transcript cannot name safely)."""
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tbar(a, b, color=NOTCH, w=6, half=0.3):
    """A line that ends in a flat bar: 'holds down'."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b - n * half, b + n * half, color=color, stroke_width=w + 2))


def glia_astro(pos, s=1.0, op=0.45):
    g = Star(n=7, outer_radius=0.4, inner_radius=0.18, color=GREEN, stroke_width=3,
             fill_color=GREEN, fill_opacity=op)
    return g.scale(s).move_to(pos)


def neuron_ball(pos, r=0.3):
    return Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.85).move_to(pos)


def pbadge(at, r=0.27):
    b = VGroup(Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1),
               T("P", 26, BG, weight=BOLD))
    b[1].move_to(b[0])
    return b.move_to(at)


# ---- gates and the gate bar
GATE_NAMES = ["1  pool", "2  signal", "3  competence"]
GSTATE = {0: (LG, 0.0), 1: (TEXT, 0.16), 2: (GREEN, 0.28), -1: (RED, 0.28)}
_GW = [T(n, 26).width + 0.5 for n in GATE_NAMES]


def bar_chip(i, state):
    col, fo = GSTATE[state]
    label = T(GATE_NAMES[i], 26, col)
    box = RoundedRectangle(corner_radius=0.14, width=_GW[i], height=0.62, stroke_color=col, stroke_width=2.5,
                           fill_color=col, fill_opacity=fo)
    return VGroup(box, label.move_to(box))


def bar_build(states):
    return VGroup(*[bar_chip(i, s) for i, s in enumerate(states)]).arrange(RIGHT, buff=0.35).move_to([0, BARY, 0])


def bar_set(bar, i, state):
    return Transform(bar[i], bar_chip(i, state).move_to(bar[i]))


GX = [-2.9, 0.0, 2.9]
GY = 0.1
GH = 3.0


def gate(cx, cy=GY, h=GH, w=2.0):
    """A thin archway: two posts, a lintel and a see-through door (the route runs behind it)."""
    pw = 0.045
    kw = dict(stroke_width=0, fill_color=GREY, fill_opacity=1)
    return VGroup(Rectangle(width=pw, height=h, **kw).move_to([cx - w / 2, cy, 0]),
                  Rectangle(width=pw, height=h, **kw).move_to([cx + w / 2, cy, 0]),
                  Rectangle(width=w + pw, height=pw, **kw).move_to([cx, cy + h / 2, 0]),
                  Rectangle(width=w - pw, height=h - pw, stroke_width=0, fill_color=GREEN, fill_opacity=0.0).move_to([cx, cy - pw / 2, 0]))


def gate_open(g):
    return AnimationGroup(*[m.animate.set_fill(GREEN, 1) for m in g[:3]], g[3].animate.set_fill(GREEN, 0.22))


# ---- cells
def rg_cell():
    return RoundedRectangle(corner_radius=0.6, width=1.4, height=6.3, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.15).move_to([-5.6, -0.2, 0])


def small_pill(y=0.1):
    return RoundedRectangle(corner_radius=0.5, width=1.0, height=4.2, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.15).move_to([-5.8, y, 0])


def padlock(pos, open_=False, k=1.0):
    col = GREEN if open_ else RED
    body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.5, stroke_color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.55)
    sh = Arc(radius=0.2, start_angle=0, angle=PI, stroke_color=col, stroke_width=5)
    sh.move_to(body.get_top() + UP * (0.1 + (0.22 if open_ else 0.0)))
    return VGroup(body, sh).scale(k).move_to(pos)


# ---- the route stage shared by s02 and s24 (progenitor, route, astrocyte)
def route_stage(astro_op=0.45, y=0.1):
    pill = small_pill(y)
    rg_l = T("radial glia", 26, BLUE).move_to([-5.8, y - 2.45, 0])
    astro = glia_astro([5.7, y, 0], 1.5, op=astro_op)
    a_l = T("astrocytes", 26, GREEN).move_to([5.6, y - 1.1, 0])
    edges = [-5.1, -3.9, -1.9, -1.0, 1.0, 1.9, 3.9, 4.6]
    route = VGroup(*[Line([a + 0.12, y, 0], [b - 0.12, y, 0], color=GREY, stroke_width=3)
                     for a, b in zip(edges[:-1], edges[1:])],
                   arr([4.15, y, 0], [4.9, y, 0], GREY, 3))
    return pill, rg_l, astro, a_l, route


# ---- the early cortical cell scene (s10 - s12)
def dish_parts():
    d = {}
    d["dish"] = RoundedRectangle(corner_radius=0.5, width=11.4, height=4.4, stroke_color=GREY, stroke_width=3).move_to([0, -0.1, 0])
    d["dlabel"] = T("cortical progenitors", 26, BLUE).move_to([-3.7, 1.65, 0])
    d["cntf"] = chip("CNTF", YELLOW, size=26).move_to([-4.3, 0.55, 0])
    dp = [(-5.0, -0.5), (-4.2, -1.0), (-3.5, 0.25), (-3.2, -0.3), (-4.9, 1.05), (-3.9, -1.7), (-2.7, 0.9), (-3.0, -1.2)]
    d["dots"] = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, y, 0]) for x, y in dp])
    d["cell"] = Circle(radius=1.45, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([0.3, -0.1, 0])
    d["rec"] = RoundedRectangle(corner_radius=0.1, width=0.36, height=0.8, stroke_color=RECEP, stroke_width=3,
                                fill_color=RECEP, fill_opacity=0.9).move_to([-1.15, -0.1, 0])
    d["rlabel"] = T("receptor", 26, RECEP).move_to([-2.0, -1.1, 0])
    d["stat"] = chip("STAT3", PINK, size=26).move_to([0.45, -0.1, 0])
    d["badge"] = pbadge(d["stat"].get_corner(UR) + np.array([0.08, 0.12, 0]))
    d["tl"] = VGroup(arr([-5.5, -2.85, 0], [5.5, -2.85, 0], GREY, 4),
                     Circle(radius=0.17, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([-4.6, -2.85, 0]),
                     T("early in neurogenesis", 26, LG).move_to([-2.9, -3.3, 0]))
    d["q"] = T("?", 100, RED, weight=BOLD).move_to([3.9, 0.3, 0])
    return d


# ---- DNA zoom (s12 - s14, s19)
DY = -0.5
SITE = np.array([-3.2, DY, 0])


def dna_parts(labels=True, dy=DY):
    d = {}
    d["prom"] = Rectangle(width=5.6, height=2.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([-3.4, dy, 0])
    d["body"] = Rectangle(width=6.8, height=2.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([3.0, dy, 0])
    d["site"] = Rectangle(width=1.2, height=2.8, stroke_color=PINK, stroke_width=4, fill_color=PINK, fill_opacity=0.35).move_to([-3.2, dy, 0])
    d["slabel"] = T("STAT3 site", 28, PINK).move_to([-3.2, dy - 1.7, 0])
    if labels:
        d["pline"] = Line([-6.2, dy - 2.1, 0], [-0.6, dy - 2.1, 0], color=GREY, stroke_width=3)
        d["plabel"] = T("GFAP promoter", 30, TEXT).move_to([-3.4, dy - 2.6, 0])
        d["gline"] = Line([-0.4, dy - 2.1, 0], [6.4, dy - 2.1, 0], color=GREY, stroke_width=3)
        d["glabel"] = T("GFAP gene", 30, TEXT).move_to([3.0, dy - 2.6, 0])
    return d


def me_tag(dy=DY):
    stem = Line([-3.2, dy + 1.4, 0], [-3.2, dy + 2.0, 0], color=RED, stroke_width=5)
    ball = Circle(radius=0.35, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.85).move_to([-3.2, dy + 2.35, 0])
    return VGroup(stem, ball)


def me_label(dy=DY):
    return T("methyl", 28, RED).move_to([-4.8, dy + 2.35, 0])


def pair_chip(pos):
    c = chip("STAT3 pair", PINK, size=26, fill_opacity=0.3).move_to(pos)
    b1 = pbadge(c.get_corner(UL) + np.array([-0.05, 0.14, 0]))
    b2 = pbadge(c.get_corner(UR) + np.array([0.05, 0.14, 0]))
    return VGroup(c, b1, b2)


REST = np.array([1.0, 1.65, 0.0])      # where the active STAT3 pair waits above the gene (s13, s14)
TAGGED = np.array([-2.5, 0.9, 0.0])  # where it meets the methyl tag


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Where Glia Come From"
    TITLE = "Same Progenitor, New Order"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=26, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=26, color=LG)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        # title done in 1 s, then held in full with the subtitle until the scene ends
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title, shift=UP * 0.1),
                  GrowFromCenter(rule), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s01_end_state():
    cell = rg_cell()
    tag = T("mouse cortex", 30, LG).move_to([2.2, BARY, 0])
    rg_l = T("radial glia", 32, BLUE).move_to([-5.4, 3.4, 0])
    tline = arr([-4.4, -1.0, 0], [6.5, -1.0, 0], GREY, 4)
    t_l = T("time →", 30, LG).move_to([6.0, -1.55, 0])
    early = T("early", 28, LG).move_to([-2.1, -1.6, 0])
    later = T("later", 28, LG).move_to([3.5, -1.6, 0])
    ns = [neuron_ball([x, 0.8, 0], 0.5) for x in (-3.3, -2.1, -0.9)]
    n_l = T("neurons", 30, TEXT).move_to([-2.1, -0.4, 0])
    astros = [glia_astro([x, 0.8, 0], 2.0) for x in (1.9, 3.6, 5.3)]
    a_l = T("astrocytes", 30, GREEN).move_to([3.6, -0.4, 0])
    q = T("?", 90, RED, weight=BOLD).move_to([0.5, 0.8, 0])
    return cell, tag, rg_l, tline, t_l, early, later, ns, n_l, astros, a_l, q


class S01Q(SpokenScene):
    def construct(self):
        cell, tag, rg_l, tline, t_l, early, later, ns, n_l, astros, a_l, q = s01_end_state()
        self.at("mouse cortex")
        self.play(FadeIn(tag), FadeIn(cell), run_time=0.6)
        self.play(GrowArrow(tline), FadeIn(t_l), FadeIn(early), FadeIn(later), run_time=0.5)
        self.at("radial glia")
        self.play(FadeIn(rg_l), run_time=0.4)
        # neurons bud off the radial glial cell one at a time, first
        self.at("make neurons")
        self.add(n_l)
        for n in ns:
            end = n.get_center().copy()
            n.scale(0.35).move_to([-5.35, 0.8, 0])
            self.add(n)
            self.play(n.animate.scale(1 / 0.35).move_to([-4.8, 0.8, 0]),
                      cell.animate.set_fill(BLUE, 0.3), run_time=0.15)
            self.play(n.animate.move_to(end), cell.animate.set_fill(BLUE, 0.15), run_time=0.28)
        self.at("then astrocytes")
        self.add(a_l)
        for a in astros:
            end = a.get_center().copy()
            a.scale(0.35).move_to([-5.35, 2.05, 0])
            self.add(a)
            self.play(a.animate.scale(1 / 0.35).move_to([-4.75, 2.05, 0]),
                      cell.animate.set_fill(BLUE, 0.3), run_time=0.15)
            self.play(a.animate.move_to(end), cell.animate.set_fill(BLUE, 0.15),
                      run_time=0.35, path_arc=-0.25)
        self.at("same progenitors")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("new output")
        self.play(*[Indicate(a, color=GREEN, scale_factor=1.15) for a in astros], run_time=0.9)
        self.at("what changes")
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    def construct(self):
        pill, rg2, astro, a2, route = route_stage()
        title = T("rodent cortex", 32, TEXT).move_to([0, 3.4, 0])
        self.add(pill, rg2, astro, a2, title)
        self.add(route)
        self.at("route to astrocytes")
        self.play(Create(route), run_time=0.9)
        dots = [Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-4.5, 0.1, 0]) for _ in range(3)]
        chipc = chip("cytokines", YELLOW, size=30).move_to([0, 1.2, 0])
        self.at("uses cytokines")
        self.play(FadeIn(chipc, shift=DOWN * 0.2), *[FadeIn(d, scale=0.3) for d in dots], run_time=0.4)
        self.play(LaggedStart(*[d.animate.move_to([4.2 - 0.5 * k, 0.1, 0]) for k, d in enumerate(dots)], lag_ratio=0.25), run_time=1.4)
        gates = [gate(x) for x in GX]
        glabels = [T(n, 28, TEXT).move_to([x, -1.95, 0]) for n, x in zip(GATE_NAMES, GX)]
        fw = T("framework for the cortical cytokine route", 28, LG).move_to([0, 2.75, 0])
        self.at("evidence sorts")
        self.play(FadeOut(chipc), *[FadeOut(d) for d in dots], FadeIn(fw),
                  LaggedStart(*[AnimationGroup(FadeIn(g, shift=DOWN * 0.3), FadeIn(l)) for g, l in zip(gates, glabels)],
                              lag_ratio=0.45), run_time=1.6)
        self.at("three conditions")
        self.play(*[Indicate(l, color=TEXT, scale_factor=1.12) for l in glabels], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
BOX_C = np.array([-0.5, -0.4, 0])
CIRC = [(-2.9, 0.75), (-1.7, 0.75), (-0.5, 0.75)]


def cell_chain():
    """The s03 picture: the progenitor wall (box with three progenitors), proneural chip, push arrow, neuron."""
    box = RoundedRectangle(corner_radius=0.7, width=7.4, height=4.6, stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.12).move_to(BOX_C)
    lab = T("progenitors", 30, BLUE).move_to([-1.7, 1.65, 0])
    circs = VGroup(*[Circle(radius=0.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([x, y, 0])
                     for x, y in CIRC])
    circs.add(Ellipse(width=3.6, height=1.65, stroke_color=BLUE, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.18).move_to([1.0, -0.7, 0]))
    pro = chip("proneural genes", TEXT, size=26).move_to([1.0, -0.6, 0])
    push = arr(pro.get_right() + RIGHT * 0.1, [4.5, -0.6, 0], TEXT, 6)
    neu = neuron_ball([5.45, -0.6, 0], 0.85)
    neu_l = T("neuron", 30, TEXT).move_to([5.45, -1.95, 0])
    return box, lab, circs, pro, push, neu, neu_l


class S03(SpokenScene):
    def construct(self):
        bar = bar_build((1, 0, 0))
        box, lab, circs, pro, push, neu, neu_l = cell_chain()
        self.add(bar, box, circs)
        self.at("a progenitor")
        self.play(FadeIn(lab), run_time=0.4)
        self.at("still be there")
        self.play(Indicate(circs, color=BLUE, scale_factor=1.12), run_time=0.9)
        self.at("genes push", lead=0.2)
        self.play(FadeIn(pro, scale=0.7), run_time=0.5)
        self.at("push dividing")
        self.play(GrowArrow(push), FadeIn(neu), run_time=0.6)
        ghost = circs[2]
        self.add(ghost)
        self.at("become neurons")
        self.remove(neu)
        self.play(Transform(ghost, neu, path_arc=-0.9), FadeIn(neu_l), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s04_parts():
    box, lab, circs, pro, push, neu, neu_l = cell_chain()
    neu = neuron_ball([5.45, -0.6, 0], 0.85)
    notch = chip("Notch", NOTCH, size=28).move_to([-5.7, -0.6, 0])
    hes = chip("Hes", NOTCH, size=28).move_to([-2.6, -0.6, 0])
    hes_l = T("repressors", 26, NOTCH).move_to([-2.6, -1.5, 0])
    a1 = arr([-4.95, -0.6, 0], hes.get_left() + LEFT * 0.08, NOTCH, 5)
    tb = tbar([-2.0, -0.6, 0], [pro.get_left()[0] - 0.12, -0.6, 0], NOTCH)
    return box, lab, circs, pro, push, neu, neu_l, notch, hes, hes_l, a1, tb


class S04(SpokenScene):
    def construct(self):
        bar = bar_build((1, 0, 0))
        box, lab, circs, pro, push, neu, neu_l, notch, hes, hes_l, a1, tb = s04_parts()
        self.add(bar, box, lab, circs, pro, push, neu, neu_l)
        self.at("notch turns on")
        self.play(FadeIn(notch, scale=0.7), run_time=0.5)
        self.at("turns on")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("repressors", lead=0.3)
        self.play(FadeIn(hes, scale=0.6), FadeIn(hes_l), run_time=0.5)
        self.at("which hold")
        self.play(Create(tb), run_time=0.6)
        x = Cross(Rectangle(width=0.6, height=0.6).move_to([3.5, -0.6, 0]), stroke_color=RED, stroke_width=6)
        self.at("down", lead=0.3)
        self.play(pro.animate.set_opacity(0.3), push.animate.set_opacity(0.3), neu.animate.set_opacity(0.25),
                  neu_l.animate.set_opacity(0.25), Create(x), run_time=0.7)
        new_lab = T("they stay progenitors", 30, BLUE).move_to([-1.7, 1.65, 0])
        self.at("the cell stays")
        self.play(FadeOut(lab), FadeIn(new_lab), Indicate(circs, color=BLUE, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        bar = bar_build((1, 0, 0))
        box, lab, circs, pro, push, neu, neu_l, notch, hes, hes_l, a1, tb = s04_parts()
        lab = T("they stay progenitors", 30, BLUE).move_to([-1.7, 1.65, 0])
        pro.set_opacity(0.3); push.set_opacity(0.3); neu.set_opacity(0.25); neu_l.set_opacity(0.25)
        x = Cross(Rectangle(width=0.6, height=0.6).move_to([3.5, -0.6, 0]), stroke_color=RED, stroke_width=6)
        self.add(bar, box, lab, circs, pro, push, neu, neu_l, notch, hes, hes_l, a1, tb, x)
        # part 1: Notch alone does not make astrocytes
        notch2 = chip("Notch", NOTCH, size=30).move_to([-4.7, 0.2, 0])
        ghost = glia_astro([3.9, 0.2, 0], 2.6, op=0.3)
        ghost.set_opacity(0.45)
        g_l = T("astrocytes", 30, GREEN).move_to([3.9, -1.7, 0])
        self.play(FadeOut(VGroup(box, lab, circs, pro, push, neu, neu_l, notch, hes, hes_l, a1, tb, x)),
                  FadeIn(notch2), run_time=0.5)
        a2 = arr([-3.7, 0.2, 0], [2.3, 0.2, 0], NOTCH, 6)
        self.at("make astrocytes")
        self.play(GrowArrow(a2), FadeIn(ghost, scale=0.4), FadeIn(g_l), run_time=0.6)
        cross2 = Cross(Rectangle(width=0.9, height=0.9).move_to([-0.7, 0.2, 0]), stroke_color=RED, stroke_width=7)
        self.at("by itself")
        self.play(Create(cross2), run_time=0.5)
        # part 2: it keeps a reserve while neurons leave
        xs = (-3.4, -2.35, -1.3, -0.25, 0.8, 1.85)
        pills = [RoundedRectangle(corner_radius=0.4, width=0.85, height=4.3, stroke_color=BLUE, stroke_width=3,
                                  fill_color=BLUE, fill_opacity=0.25).move_to([x_, -0.6, 0]) for x_ in xs]
        wall_l = T("reserve of progenitors", 30, BLUE).move_to([-0.8, -3.15, 0])
        a3 = arr([-4.4, -0.6, 0], [-3.95, -0.6, 0], NOTCH, 5)
        notch3 = chip("Notch", NOTCH, size=30).move_to([-5.5, -0.6, 0])
        a3 = arr([-4.6, -0.6, 0], [-3.95, -0.6, 0], NOTCH, 5)
        self.at("keeps a reserve")
        self.play(FadeOut(VGroup(a2, ghost, g_l, cross2)), ReplacementTransform(notch2, notch3),
                  LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pills], lag_ratio=0.1), GrowArrow(a3), run_time=0.8)
        ns = [neuron_ball([2.55, y_, 0], 0.3).scale(0.5) for y_ in (0.6, -0.6, -1.8)]
        n_l = T("neurons leave", 30, TEXT).move_to([4.9, 1.7, 0])
        self.at("reserve of progenitors")
        self.add(*ns)
        self.play(FadeIn(wall_l), FadeIn(n_l),
                  LaggedStart(*[n.animate.scale(2.0).move_to([4.7, y_, 0]) for n, y_ in zip(ns, (0.6, -0.6, -1.8))], lag_ratio=0.3),
                  run_time=1.2)
        self.at("for later")
        self.play(Indicate(VGroup(*pills), color=BLUE, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
MEMY = -1.6
SH = 2.9   # (kept from the first draft; unused)


def membrane_scene(bar_states):
    bar = bar_build(bar_states)
    mem = Rectangle(width=12.4, height=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0, MEMY, 0])
    inner = Rectangle(width=12.4, height=2.0, stroke_width=0, fill_color=BLUE, fill_opacity=0.1).move_to([0, -2.73, 0])
    plab = T("progenitor", 26, BLUE).move_to([-5.2, -3.3, 0])
    return bar, mem, inner, plab


def cyto_shapes(y=1.0):
    c1 = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
    c2 = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.95, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
    c3 = RegularPolygon(6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).scale(0.55)
    return [c1.move_to([-3.6, y, 0]), c2.move_to([0, y, 0]), c3.move_to([3.6, y, 0])]


CYN = ["CNTF", "LIF", "cardiotrophin-1"]


def cyto_labels(y=1.95):
    return [T(n, 28, YELLOW).move_to([x, y, 0]) for n, x in zip(CYN, (-3.6, 0, 3.6))]


class S06(SpokenScene):
    def construct(self):
        bar, mem, inner, plab = membrane_scene((1, 0, 0))
        self.add(bar, mem, inner, plab)
        self.play(bar_set(bar, 1, 1), run_time=0.4)
        first = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to([0, 2.5, 0])
        sig_l = T("signal", 30, YELLOW).move_to([1.5, 1.0, 0])
        self.at("signal must arrive")
        self.play(FadeIn(first, scale=0.4), run_time=0.3)
        self.play(first.animate.move_to([0, 1.0, 0]), FadeIn(sig_l), run_time=0.8)
        shapes = cyto_shapes()
        self.at("family of cytokines")
        self.play(FadeOut(sig_l), ReplacementTransform(first, shapes[1]),
                  FadeIn(shapes[0], shift=RIGHT * 1.2), FadeIn(shapes[2], shift=LEFT * 1.2), run_time=0.9)
        labs = cyto_labels()
        self.at("CNTF")
        self.play(FadeIn(labs[0]), Indicate(shapes[0], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("LIF")
        self.play(FadeIn(labs[1]), Indicate(shapes[1], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("cardiotrophin")
        self.play(FadeIn(labs[2]), Indicate(shapes[2], color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def receptor(cx, my, sc=1.0, text=True):
    """gp130 body across the membrane, a receptor-specific ligand-binding part on top, a JAK hanging below."""
    body = RoundedRectangle(corner_radius=0.14, width=0.8 * sc, height=2.5 * sc, stroke_color=RECEP, stroke_width=3,
                            fill_color=RECEP, fill_opacity=0.9).move_to([cx, my, 0])
    glab = T("gp130", 26, BG, weight=BOLD).rotate(PI / 2).move_to(body)
    lig = RoundedRectangle(corner_radius=0.12, width=(2.7 if text else 2.0) * sc, height=0.7 * sc,
                           stroke_color=LG, stroke_width=3, fill_color=LG, fill_opacity=0.25).move_to([cx, my + 1.6 * sc, 0])
    if text:
        lig = VGroup(lig, T("ligand-binding", 26, LG).move_to(lig))
    jak = chip("JAK", PINK, size=26).move_to([cx, my - 1.9 * sc, 0])
    link = Line(body.get_bottom(), jak.get_top(), color=PINK, stroke_width=3)
    return body, glab, lig, link, jak


S07_MY = -0.6
S07_X = (-3.6, 0.0, 3.6)


def s07_layout():
    mem = Rectangle(width=12.4, height=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0, S07_MY, 0])
    inner = Rectangle(width=12.4, height=2.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.1).move_to([0, -2.2, 0])
    plab = T("progenitor", 26, BLUE).move_to([-5.4, -1.6, 0])
    return mem, inner, plab


class S07(SpokenScene):
    def construct(self):
        bar, mem, inner, plab = membrane_scene((1, 1, 0))
        shapes = cyto_shapes()
        labs = cyto_labels()
        self.add(bar, mem, inner, plab, *shapes, *labs)
        mem2, inner2, plab2 = s07_layout()
        rec = [receptor(x, S07_MY, 0.85) for x in S07_X]
        # the receptors shift to sit with the cytokines: zoom the stage to where the action is
        self.play(Transform(mem, mem2), Transform(inner, inner2), Transform(plab, plab2),
                  *[s.animate.move_to([x, 1.85, 0]) for s, x in zip(shapes, S07_X)],
                  *[l.animate.move_to([x, 2.65, 0]) for l, x in zip(labs, S07_X)], run_time=0.5)
        self.at("shared receptor")
        self.play(*[FadeIn(r[0], shift=UP * 0.3) for r in rec], run_time=0.5)
        self.at("receptor subunit")
        self.play(*[FadeIn(r[2], shift=DOWN * 0.15) for r in rec], run_time=0.5)
        self.play(*[s.animate.shift(DOWN * 0.2) for s in shapes], *[Flash(r[2], color=YELLOW, line_length=0.2, flash_radius=0.6) for r in rec],
                  run_time=0.5)
        cap = T("each has its own binding part; gp130 is shared", 28, TEXT).move_to([0, -3.1, 0])
        self.at("gp130")
        self.add(cap)
        self.play(*[FadeIn(r[1]) for r in rec], *[Indicate(r[0], color=RECEP, scale_factor=1.1) for r in rec], run_time=0.9)
        self.at("activates JAK")
        self.play(*[FadeIn(r[3]) for r in rec], *[FadeIn(r[4], scale=0.6) for r in rec], run_time=0.5)
        badges = [pbadge(r[4].get_corner(UR) + np.array([0.05, 0.1, 0])) for r in rec]
        self.at("JAK kinases", lead=0.25)
        self.play(*[r[4][0].animate.set_fill(PINK, 0.85) for r in rec], *[r[4][1].animate.set_color(BG) for r in rec], *[FadeIn(b, scale=0.4) for b in badges],
                  *[Indicate(r[4], color=PINK, scale_factor=1.2) for r in rec], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
S08_MY = 0.7
S08_X = -5.4


class S08(SpokenScene):
    def construct(self):
        bar = bar_build((1, 1, 0))
        mem2, inner2, plab2 = s07_layout()
        shapes = cyto_shapes()
        labs = cyto_labels()
        rec = [receptor(x, S07_MY, 0.85) for x in S07_X]
        for s, x in zip(shapes, S07_X):
            s.move_to([x, 1.65, 0])
        for l, x in zip(labs, S07_X):
            l.move_to([x, 2.65, 0])
        badges = [pbadge(r[4].get_corner(UR) + np.array([0.05, 0.1, 0])) for r in rec]
        for r in rec:
            r[4][0].set_fill(PINK, 0.85)
            r[4][1].set_color(BG)
        cap = T("each has its own binding part; gp130 is shared", 28, TEXT).move_to([0, -3.1, 0])
        old = VGroup(mem2, inner2, plab2, *shapes, *labs, cap, *[VGroup(*r) for r in rec], *badges)
        self.add(bar, old)

        # the stage rises: one receptor stays in view at reduced size, the cell opens up below it
        mem = Rectangle(width=12.4, height=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0, S08_MY, 0])
        inner = Rectangle(width=12.4, height=4.0, stroke_width=0, fill_color=BLUE, fill_opacity=0.1).move_to([0, -1.43, 0])
        r = receptor(S08_X, S08_MY, 0.9, text=False)
        cyt = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to([S08_X, 2.5, 0])
        bd = pbadge(r[4].get_corner(UR) + np.array([0.05, 0.1, 0]))
        r[4][0].set_fill(PINK, 0.85)
        r[4][1].set_color(BG)
        stat = chip("STAT3", PINK, size=34).move_to([-3.0, -0.9, 0])
        nuc = Ellipse(width=6.8, height=3.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([2.7, -1.4, 0])
        nlab = T("nucleus", 26, LG).move_to([-2.1, -2.2, 0])
        nlead = Line([-1.45, -2.2, 0], [-0.95, -2.1, 0], color=LG, stroke_width=2)
        self.play(FadeOut(old), FadeIn(mem), FadeIn(inner), FadeIn(VGroup(*r)), FadeIn(cyt), FadeIn(bd), FadeIn(stat, scale=0.7), FadeIn(nuc), FadeIn(nlab), FadeIn(nlead), run_time=0.6)
        self.at("phosphorylate")
        dot = Circle(radius=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(bd.get_center())
        self.add(dot)
        self.play(dot.animate.move_to(stat.get_corner(UR) + np.array([0.08, 0.12, 0])), run_time=0.5)
        sbd = pbadge(stat.get_corner(UR) + np.array([0.08, 0.12, 0]))
        self.play(FadeOut(dot), FadeIn(sbd, scale=0.5), Indicate(stat, color=PINK, scale_factor=1.15), run_time=0.3)
        pair = pair_chip([-3.0, -0.9, 0]).scale(1.2)
        self.at("STAT3", nth=1, lead=0.2)
        self.play(FadeOut(VGroup(stat, sbd)), FadeIn(pair, scale=0.7), run_time=0.6)
        genes = [Rectangle(width=1.5, height=1.05, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([x, -2.15, 0])
                 for x in (1.0, 2.7, 4.4)]
        gfap_t = T("GFAP", 30, TEXT, weight=BOLD).move_to(genes[2])
        alab = T("astrocyte genes", 28, TEXT).move_to([2.7, -1.35, 0])
        self.at("switches on")
        self.play(pair.animate.move_to([2.7, -0.35, 0]), run_time=1.0)
        self.at("astrocyte genes")
        self.play(FadeIn(alab), LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in genes], lag_ratio=0.2), FadeIn(gfap_t), run_time=0.65)
        self.at("GFAP", lead=0.2)
        self.play(genes[2].animate.set_fill(GREEN, 0.7).set_stroke(GREEN),
                  Indicate(pair, color=PINK, scale_factor=1.03), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09(SpokenScene):
    def construct(self):
        bar = bar_build((1, 1, 0))
        self.add(bar)
        cell = Circle(radius=2.1, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([1.6, -0.2, 0])
        clab = T("progenitor", 30, BLUE).move_to([1.6, -2.85, 0])
        sig = Circle(radius=0.45, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to([-5.0, -0.2, 0])
        sig_l = T("signal", 30, YELLOW).move_to([-5.0, -1.1, 0])
        a = arr([-4.3, -0.2, 0], [-0.7, -0.2, 0], YELLOW, 6)
        self.add(cell, clab, sig, sig_l, a)
        comp = T("competence", 46, TEXT, font=TITLE_FONT).move_to([-2.8, 1.3, 0])
        self.add(comp)
        self.play(bar_set(bar, 2, 1), run_time=0.4)
        q = T("?", 130, RED, weight=BOLD).move_to([1.6, -0.2, 0])
        self.at("able to read")
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        
        self.at("competence")
        self.play(Indicate(comp, color=TEXT), Indicate(cell, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10(SpokenScene):
    def construct(self):
        bar = bar_build((1, 1, 1))
        d = dish_parts()
        self.add(bar)
        self.play(FadeIn(d["dish"]), run_time=0.4)
        self.at("CNTF", lead=0.2)
        self.play(FadeIn(d["cntf"], scale=0.7), LaggedStart(*[FadeIn(x, scale=0.3) for x in d["dots"]], lag_ratio=0.1), run_time=0.9)
        self.at("cortical progenitors")
        self.play(FadeIn(d["cell"], scale=0.8), FadeIn(d["dlabel"]), run_time=0.7)
        self.at("early in neurogenesis")
        self.play(Create(d["tl"][0]), FadeIn(d["tl"][1]), FadeIn(d["tl"][2]), run_time=0.9)
        self.at("have the receptor")
        self.play(FadeIn(d["rec"], scale=0.5), FadeIn(d["rlabel"]), run_time=0.6)
        dock = [d["dots"][2].copy(), d["dots"][3].copy()]
        self.add(*dock)
        self.play(dock[0].animate.move_to([-1.45, 0.12, 0]), dock[1].animate.move_to([-1.45, -0.32, 0]), run_time=0.8)
        self.at("STAT3 can be")
        self.play(FadeIn(d["stat"], scale=0.7), run_time=0.5)
        self.at("activated")
        self.play(d["stat"][0].animate.set_fill(PINK, 0.5), d["stat"][1].animate.set_color(TEXT), FadeIn(d["badge"], scale=0.5), run_time=0.6)
        self.at("what happens")
        self.play(FadeIn(d["q"], scale=0.4), run_time=0.5)
        self.finish()


def full_dish(with_q=True, dock=True):
    d = dish_parts()
    d["stat"][0].set_fill(PINK, 0.5)
    d["stat"][1].set_color(TEXT)
    ms = [d["dish"], d["dlabel"], d["cntf"], d["dots"], d["cell"], d["rec"], d["rlabel"], d["stat"], d["badge"], d["tl"]]
    if dock:
        # the two docked dots sit on the receptor, as at the end of the cell scene
        d["dock"] = VGroup(d["dots"][2].copy().move_to([-1.45, 0.12, 0]), d["dots"][3].copy().move_to([-1.45, -0.32, 0]))
        ms.append(d["dock"])
    if with_q:
        ms.append(d["q"])
    return d, ms


class S11Pause(SpokenScene):
    def construct(self):
        bar = bar_build((1, 1, 1))
        d, ms = full_dish()
        pp = T("Pause and predict", 28, TEXT, weight=BOLD).move_to([3.6, 1.6, 0])
        self.add(bar, *ms, pp)
        # a visible 5-second countdown: a ring that empties and a number that steps down
        c = np.array([3.9, -1.2, 0.0])
        ring = Circle(radius=0.62, stroke_color=GREY, stroke_width=4).move_to(c)
        prog = ValueTracker(0.0)
        arc = always_redraw(lambda: Arc(radius=0.62, start_angle=PI / 2, angle=-TAU * max(1e-3, 1 - prog.get_value()),
                                        stroke_color=YELLOW, stroke_width=7, arc_center=c) if prog.get_value() < 0.999 else VMobject())
        nums = [T(str(k), 44, TEXT, weight=BOLD).move_to(c) for k in (5, 4, 3, 2, 1)]

        def step(m):
            k = min(4, int(prog.get_value() * 5))
            for i, n in enumerate(nums):
                n.set_opacity(1.0 if i == k else 0.0)
        ring.add_updater(step)
        self.add(ring, arc, *nums)
        self.play(prog.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        bar = bar_build((1, 1, 1))
        d, ms = full_dish()
        self.add(bar, *ms)
        # the answer: a field of cells, few turn into GFAP-positive astrocytes
        field = VGroup(*[Circle(radius=0.34, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25)
                         .move_to([-1.6 + 0.95 * ix, 0.0 + (iy - 1) * 1.0, 0]) for ix in range(5) for iy in range(3)])
        keep = VGroup(d["dish"], d["cntf"], d["dots"])
        gone = VGroup(d["rec"], d["rlabel"], d["stat"], d["badge"], d["q"], d["tl"], d["dock"], d["dlabel"])
        pl = T("progenitors", 28, BLUE).move_to([0.3, 1.8, 0])
        self.at("few", lead=0.0)
        self.play(FadeOut(gone), ReplacementTransform(d["cell"], field), FadeIn(pl), run_time=0.9)
        star = glia_astro([2.2, 0.0, 0], 1.3, op=0.7)
        slab = VGroup(T("GFAP-positive", 26, GREEN), T("astrocyte (few)", 26, GREEN)).arrange(DOWN, buff=0.06).move_to([4.5, 0.0, 0])
        lead_l = Line([2.85, 0.0, 0], [3.2, 0.0, 0], color=GREEN, stroke_width=3)
        self.at("astrocytes")
        self.play(FadeOut(field[13]), FadeIn(star, scale=0.4), FadeIn(slab), FadeIn(lead_l), run_time=0.7)
        early = T("early cells", 28, LG).move_to([5.3, 2.35, 0])
        self.at("early cells")
        self.play(FadeIn(early), FadeOut(VGroup(keep, field, star, slab, lead_l, pl)), run_time=1.0)
        dna = dna_parts()
        self.at("STAT3 site", lead=0.5)
        self.play(FadeIn(dna["prom"]), FadeIn(dna["body"]), run_time=0.6)
        self.play(FadeIn(dna["site"], scale=0.6), FadeIn(dna["slabel"]), run_time=0.4)
        self.at("GFAP promoter", lead=0.3)
        self.play(FadeIn(dna["pline"]), FadeIn(dna["plabel"]), run_time=0.7)
        tag = me_tag(); ml = me_label()
        tag.shift(UP * 0.8)
        self.at("methylated", lead=0.5)
        self.add(tag)
        self.play(tag.animate.shift(DOWN * 0.8), run_time=0.5)
        self.play(FadeIn(ml), bar_set(bar, 2, -1), run_time=0.5)
        self.finish()


def dna_scene_base(bar_states, tag=True):
    bar = bar_build(bar_states)
    dna = dna_parts()
    early = T("early cells", 28, LG).move_to([5.3, 2.35, 0])
    t = me_tag(); ml = me_label()
    mobs = [bar, early, dna["prom"], dna["body"], dna["site"], dna["slabel"], dna["pline"], dna["plabel"]]
    if tag:
        mobs += [t, ml]
    return bar, dna, early, t, ml, mobs


class S13(SpokenScene):
    def construct(self):
        bar, dna, early, tag, ml, mobs = dna_scene_base((1, 1, -1))
        self.add(*mobs)
        pair = pair_chip(REST + np.array([-0.6, 0.1, 0]))   # arrives from just off the rest spot
        self.at("methyl group")
        self.play(Indicate(VGroup(tag, ml), color=RED, scale_factor=1.15), FadeIn(pair, scale=0.7), run_time=0.8)
        self.at("keeps STAT3")
        self.play(pair.animate.move_to(TAGGED), run_time=0.9, rate_func=rush_into)
        self.at("from binding")
        self.play(pair.animate.shift(RIGHT * 0.7), Flash(tag[1], color=RED, line_length=0.3, flash_radius=0.45), run_time=0.7, rate_func=rush_from)
        act = T("active", 28, YELLOW).move_to([4.4, 1.65, 0])
        self.at("STAT3 is active")
        self.play(Indicate(pair, color=YELLOW, scale_factor=1.12), FadeIn(act), run_time=0.8)
        self.at("but the GFAP gene")
        self.play(FadeIn(dna["gline"]), FadeIn(dna["glabel"]), run_time=0.6)
        no = T("no answer", 34, RED).move_to([3.0, -0.5, 0])
        self.at("does not answer")
        self.play(FadeIn(no, shift=DOWN * 0.1), pair.animate.move_to(TAGGED), run_time=0.35)
        self.play(pair.animate.shift(RIGHT * 0.7), Flash(tag[1], color=RED, flash_radius=0.45),
                  run_time=0.45, rate_func=there_and_back)
        self.play(pair.animate.shift(RIGHT * 0.45), run_time=0.25)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        bar, dna, early, tag, ml, mobs = dna_scene_base((1, 1, -1))
        pair = pair_chip(TAGGED + RIGHT * 0.45)
        act = T("active", 28, YELLOW).move_to([4.4, 1.65, 0])
        no = T("no answer", 34, RED).move_to([3.0, -0.5, 0])
        self.add(*mobs, dna["gline"], dna["glabel"], pair, act, no)
        later = T("later", 28, GREEN).move_to([5.3, -2.0, 0])
        self.at("later", lead=0.0)
        self.play(FadeOut(early), FadeIn(later), FadeOut(no), FadeOut(act), run_time=0.6)
        # the methyl tag visibly lifts off, and the process is named
        demeth = T("demethylation", 30, TEXT).move_to([-4.9, DY + 2.35, 0])
        # The aligner spells demethylation "dimethylation"; use the next word's timestamp.
        wt(self, self.t_of("and other") - 0.6)
        self.play(FadeOut(ml), FadeIn(demeth), run_time=0.2)
        self.play(tag.animate.shift(UP * 0.4), run_time=0.6)
        other = T("other changes in the cell", 28, TEXT).move_to([3.3, 2.35, 0])
        self.at("other changes", lead=0)
        self.play(FadeIn(other), tag.animate.shift(UP * 0.25), run_time=0.6)
        self.play(FadeOut(tag), run_time=0.2)
        cy = chip("CNTF", YELLOW, size=28).move_to([4.5, 1.45, 0])
        self.at("same cytokine")
        self.play(FadeIn(cy, shift=LEFT * 0.4), FadeOut(demeth), run_time=0.3)
        self.play(FadeOut(cy), pair.animate.move_to([-3.2, 1.4, 0]), run_time=0.4)
        gon = T("GFAP on", 34, TEXT, weight=BOLD).move_to([3.0, -0.5, 0])
        self.at("switch on")
        self.play(dna["body"].animate.set_fill(GREEN, 0.55).set_stroke(GREEN), bar_set(bar, 2, 2), run_time=0.7)
        self.at("GFAP", lead=0.1)
        self.play(FadeIn(gon), dna["glabel"].animate.set_color(GREEN), run_time=0.5)
        self.finish()


class S15Beat(SpokenScene):
    def construct(self):
        bar, dna, early, tag, ml, mobs = dna_scene_base((1, 1, 2), tag=False)
        later = T("later", 28, GREEN).move_to([5.3, -2.0, 0])
        pair = pair_chip([-3.2, 1.4, 0])
        other = T("other changes in the cell", 28, TEXT).move_to([3.3, 2.35, 0])
        gon = T("GFAP on", 34, TEXT, weight=BOLD).move_to([3.0, -0.5, 0])
        dna["body"].set_fill(GREEN, 0.55).set_stroke(GREEN)
        dna["glabel"].set_color(GREEN)
        mobs = [bar, dna["prom"], dna["body"], dna["site"], dna["slabel"], dna["pline"], dna["plabel"], dna["gline"], dna["glabel"]]
        self.add(*mobs, later, pair, other, gon)
        self.wait(self.narration_s)


# ---------------------------------------------------------------------------------------------
class S16(SpokenScene):
    def construct(self):
        head = T("timed partly inside the cell", 46, font=TITLE_FONT).move_to([0, 3.15, 0])
        sub = T("not only by when the signal shows up", 30, LG).move_to([0, 2.45, 0])
        X0, XM, X1 = -2.6, 1.8, 6.2
        rl2 = T("inside the cell", 28, TEXT).move_to([-4.6, -0.5, 0])
        seg_r = Rectangle(width=XM - X0, height=1.3, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.3).move_to([(X0 + XM) / 2, -0.5, 0])
        seg_g = Rectangle(width=X1 - XM, height=1.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.3).move_to([(XM + X1) / 2, -0.5, 0])
        t_r = T("site methylated", 28, RED).move_to(seg_r)
        t_g = T("site open", 28, GREEN).move_to(seg_g)
        tl = arr([X0, -1.7, 0], [X1 + 0.3, -1.7, 0], GREY, 4)
        t_e = T("early", 30, LG).move_to([(X0 + XM) / 2, -2.35, 0])
        t_l = T("later", 30, LG).move_to([(XM + X1) / 2, -2.35, 0])
        rl1 = T("signal", 28, YELLOW).move_to([-4.6, 1.0, 0])
        seg_y = Rectangle(width=X1 - X0, height=1.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3).move_to([(X0 + X1) / 2, 1.0, 0])
        t_y = T("same cytokine, early and later", 28, YELLOW).move_to(seg_y)
        # the axis is up with the title; the bars build under it as each half of the sentence is spoken
        self.add(head, sub, tl, t_e, t_l, rl2, seg_r, t_r, seg_g, t_g)
        self.at("inside the cell")
        self.play(Indicate(VGroup(seg_r, seg_g), scale_factor=1.02), run_time=0.5)
        self.at("not only by")
        self.play(FadeIn(rl1), FadeIn(seg_y), FadeIn(t_y), run_time=0.8)
        self.at("shows up")
        self.play(Indicate(seg_y, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ligand_pose():
    prog = Circle(radius=2.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([-3.4, -0.3, 0])
    plab = T("progenitor", 28, BLUE).move_to([-3.4, -2.85, 0])
    lock = padlock([-3.4, 2.4, 0], k=1.5)
    llock = T("GFAP site methylated (locked)", 28, RED).move_to([0.9, 2.4, 0])
    neu = Circle(radius=1.6, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.3).move_to([3.5, -0.3, 0])
    nlab = VGroup(T("newly committed", 28, TEXT), T("neuron", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([3.5, -2.75, 0])
    ligs = VGroup()
    for ang in (125, 150, 180, 210, 235):
        a = np.deg2rad(ang)
        base = np.array([3.5 + 1.6 * np.cos(a), -0.3 + 1.6 * np.sin(a), 0])
        tip = base + 0.55 * np.array([np.cos(a), np.sin(a), 0])
        ligs.add(VGroup(Line(base, tip, color=NOTCH, stroke_width=4),
                        Circle(radius=0.14, stroke_color=NOTCH, stroke_width=2, fill_color=NOTCH, fill_opacity=1).move_to(tip)))
    llab = T("Notch ligands", 28, NOTCH).move_to([0.0, 1.45, 0])
    return prog, plab, lock, llock, neu, nlab, ligs, llab


class S17(SpokenScene):
    def construct(self):
        prog, plab, lock, llock, neu, nlab, ligs, llab = ligand_pose()
        self.add(prog, plab, neu)
        self.at("unlocks it")
        self.play(FadeIn(lock, shift=DOWN * 0.15), FadeIn(llock), run_time=0.6)
        self.at("cells that have")
        self.play(Indicate(neu, color=TEXT), FadeIn(nlab), run_time=0.6)
        self.at("notch ligands")
        self.play(LaggedStart(*[FadeIn(l, scale=0.4) for l in ligs], lag_ratio=0.1), FadeIn(llab), run_time=0.9)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        prog, plab, lock, llock, neu, nlab, ligs, llab = ligand_pose()
        self.add(prog, plab, lock, llock, neu, nlab, ligs, llab)
        sig = arr([1.5, -0.3, 0], [-1.35, -0.3, 0], NOTCH, 6)
        self.at("notch signaling")
        self.play(GrowArrow(sig), run_time=0.8)
        new_plab = T("neighbouring progenitor", 28, BLUE).move_to([-3.4, -2.85, 0])
        self.at("neighboring progenitors")
        self.play(FadeOut(plab), FadeIn(new_plab), run_time=0.6)
        sig2 = arr([1.5, -0.3, 0], [-2.0, -0.3, 0], NOTCH, 6)
        self.at("induces")
        self.play(Transform(sig, sig2), run_time=0.6)
        nuc = Circle(radius=1.25, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([-3.6, -0.3, 0])
        nlab2 = T("nucleus", 26, LG).move_to([-3.6, -1.95, 0])
        self.at("transcription factor")
        self.play(FadeIn(nuc), FadeIn(nlab2), run_time=0.6)
        nfia = chip("NFIA", NOTCH, size=34).move_to([-3.6, -0.3, 0])
        self.at("NFIA")
        self.play(FadeIn(nfia, scale=0.6), run_time=0.6)
        self.finish()


S19_DY = 0.8


class S19(SpokenScene):
    def construct(self):
        dy = S19_DY
        dna = dna_parts(labels=False, dy=dy)
        tag = me_tag(dy); ml = me_label(dy)
        lock = padlock([4.2, 2.95, 0], k=1.3)
        llock = T("GFAP site: locked", 28, RED).move_to([1.5, 2.95, 0])
        dna["slabel"].move_to([-0.3, 2.05, 0])
        site_leader = Line([-1.5, 2.05, 0], [-2.6, 2.15, 0], color=PINK, stroke_width=2)
        promoter_label = VGroup(T("GFAP", 28, TEXT), T("promoter", 28, TEXT)).arrange(DOWN, buff=0.05).move_to([-5.0, 0.22, 0])
        self.add(dna["prom"], dna["body"], dna["site"], dna["slabel"], site_leader,
                 promoter_label, tag, ml, lock, llock)
        nfia = chip("NFIA", NOTCH, size=32).move_to([-5.4, dy + 1.0, 0])
        self.at("NFIA")
        self.play(FadeIn(nfia, scale=0.6), run_time=0.4)
        self.at("helps", lead=0.2)
        self.play(nfia.animate.move_to([-2.0, dy + 0.45, 0]), run_time=0.7)
        self.at("remove the methyl")
        self.play(tag.animate.shift(UP * 0.8).set_opacity(0), ml.animate.shift(UP * 0.8).set_opacity(0), run_time=0.8)
        # only now, with the tag gone, the padlock opens
        lock2 = padlock([4.2, 2.95, 0], open_=True, k=1.3)
        llock2 = T("GFAP site: open", 28, GREEN).move_to([1.5, 2.95, 0])
        self.play(Transform(lock, lock2), FadeOut(llock), FadeIn(llock2), run_time=0.6)
        j1 = chip("Notch job 1: held progenitors back", NOTCH, size=30).move_to([0, -1.1, 0])
        self.at("so notch")
        self.play(FadeIn(j1, shift=UP * 0.1), run_time=0.6)
        j2 = chip("Notch job 2: competence", NOTCH, size=32, fill_opacity=0.4).move_to([0, -2.05, 0])
        self.at("a second job")
        self.play(FadeIn(j2, shift=UP * 0.1), j1[0].animate.set_stroke(GREY).set_fill(BG, 0), j1[1].animate.set_color(GREY), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S24Take(SpokenScene):
    def construct(self):
        pill, rg_l, astro, a_l, route = route_stage(astro_op=0.35)
        rg_l2 = T("progenitor", 26, BLUE).move_to(rg_l)
        gates = [gate(x) for x in GX]
        names = ["still there", "given the signal", "able to read it"]
        labs = [T(n, 28, LG).move_to([x, -1.95, 0]) for n, x in zip(names, GX)]
        self.add(route)
        self.play(FadeIn(pill), FadeIn(rg_l2), LaggedStart(*[AnimationGroup(FadeIn(g), FadeIn(l)) for g, l in zip(gates, labs)], lag_ratio=0.2),
                  run_time=0.9)
        self.at("progenitor makes astrocytes")
        self.play(FadeIn(astro, scale=0.4), FadeIn(a_l), Indicate(pill, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("still there")
        self.play(gate_open(gates[0]), labs[0].animate.set_color(GREEN), run_time=0.6)
        self.at("given the signal")
        self.play(gate_open(gates[1]), labs[1].animate.set_color(GREEN), run_time=0.6)
        self.at("able to read it")
        self.play(gate_open(gates[2]), labs[2].animate.set_color(GREEN), astro.animate.set_fill(GREEN, 1.0), run_time=0.8)
        self.finish()


class S25End(EndCard):
    LINE = "Cortical cytokine route:\nprogenitor present, signal received, competence acquired."

    def construct(self):
        line = T(self.LINE, 40, TEXT, font=TITLE_FONT, line_spacing=1.2)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", 26, TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)
        self.finish()
