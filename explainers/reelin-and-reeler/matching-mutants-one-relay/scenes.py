"""Reelin and the reeler mouse, chapter 2: Matching Mutants, One Relay  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film; same map as chapter 1 / scenes.old.py)
  ORANGE = the first-born neurons          BLUE  = the next-born neurons        GREEN = the last-born neurons
  YELLOW = Reelin and the Cajal-Retzius cells that make it
  TEAL   = the two receptors (ApoER2, VLDLR)
  PURPLE = Dab1, the adaptor
  PINK   = the Src-family kinases (Fyn, Src)
  GOLD   = a phosphate group (the little "P" badge) and the "Predict" card
  RED    = the reeler problem: a block, a stop, a missing runner, a bad result
  TAN    = Cullin 5 and its destruction tag (new in this chapter)
  GREY   = tissue, membranes, outlines, labels, cultured neurons, the dish
  WHITE  = the baton in the relay picture
  TEXT   = the antibody (a Y-shaped cartoon) and plain text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E8789F"
TAN = "#C9A06A"

SL_W, SL_H = 4.4, 5.7
TOP, BOT = 2.85, -2.85
DR = 0.17
LA = [-1.8, -1.08, -0.36, 0.36, 1.08, 1.8]
LB = [-1.44, -0.72, 0.0, 0.72, 1.44]
LSUB = [-1.44, 0.0, 1.44]
Y_CR, Y_LATE, Y_EARLY, Y_SUB = 2.58, 1.45, 0.35, -0.8
Y_START = -2.55
SLX = -3.9

SAFE_X, SAFE_Y = 6.8, 3.8


# ---------------------------------------------------------------- diagnostics base class
class Sc(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        if target > self.elapsed() + 0.02:
            self.wait(target - self.elapsed())

    def after(self, phrase, off, nth=0, lead=0.2):
        target = self.t_of(phrase, nth) + off - lead
        if target > self.elapsed() + 0.02:
            self.wait(target - self.elapsed())


# ---------------------------------------------------------------- shared drawing helpers
def neuron(x, y, color, r=DR):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.65).move_to([x, y, 0])


def wave(cx, lanes, y, color):
    return VGroup(*[neuron(cx + l, y, color) for l in lanes])


def slab(cx, with_vz=True):
    body = Rectangle(width=SL_W, height=SL_H, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([cx, 0, 0])
    g = VGroup(body)
    if with_vz:
        g.add(Rectangle(width=SL_W, height=0.55, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([cx, BOT + 0.275, 0]))
    return g


def lab(text, color=GREY, size=26):
    return T(text, size, color)


def left_of(mob, x, y):
    return mob.move_to([x, y, 0]).align_to([x, 0, 0], LEFT)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 26, BG, weight=BOLD).move_to(c))


def normal_final(cx, tint_cr=True):
    cr = VGroup(*[neuron(cx + LA[i], Y_CR, YELLOW if tint_cr else ORANGE) for i in (0, 2, 4)])
    late = wave(cx, LA, Y_LATE, GREEN)
    early = wave(cx, LB, Y_EARLY, BLUE)
    sub = wave(cx, LSUB, Y_SUB, ORANGE)
    return cr, late, early, sub


def disordered(cx, y, color, lanes=LA):
    rng = np.random.RandomState(int((y + 4) * 100))
    return VGroup(*[neuron(cx + x + rng.uniform(-.12, .12), y + rng.uniform(-.42, .42), color) for x in lanes])


def cortex(cx, kind, s=1.0, cy=0.0):
    """a whole cortex slab with its rows, built at the origin, then scaled and moved."""
    parts = [slab(0)]
    if kind == "normal":
        parts += list(normal_final(0, False))
    elif kind == "reeler":
        parts += [disordered(0, 2.1, ORANGE), disordered(0, 1.1, BLUE, LB), disordered(0, -.1, GREEN)]
    elif kind == "cul":
        cr, late, early, sub = normal_final(0, False)
        parts += [cr, early, sub, wave(0, LA, 2.05, GREEN), wave(0, LB, 1.72, GREEN)]
    return VGroup(*parts).scale(s, about_point=ORIGIN).shift([cx, cy, 0])


def antibody(h=1.6, color=TEXT):
    """a Y-shaped cartoon, arms up. h is its height."""
    s = h / 1.2
    stem = Line([0, -0.6 * s, 0], [0, 0, 0], color=color, stroke_width=9)
    a1 = Line([0, 0, 0], [-0.5 * s, 0.6 * s, 0], color=color, stroke_width=9)
    a2 = Line([0, 0, 0], [0.5 * s, 0.6 * s, 0], color=color, stroke_width=9)
    t1 = Dot([-0.5 * s, 0.6 * s, 0], radius=0.09 * s, color=color)
    t2 = Dot([0.5 * s, 0.6 * s, 0], radius=0.09 * s, color=color)
    return VGroup(stem, a1, a2, t1, t2)


def dim(c, o=0.3):
    return c.animate.set_opacity(o)


# ---- the genotype table (chapter 2's running device)
COLX = {"m": -4.5, "r": -1.1, "o": 1.95, "c": 5.0}
COLW = {"m": 4.3, "r": 2.5, "o": 3.5, "c": 3.3}
ROWY = [1.75, 0.65, -0.45, -1.55, -2.65]
HDRY = 2.85
ROWS = [
    ("reeler", TEXT, ("broken", RED), ("none", GREY), ("reeler", RED)),
    ("scrambler, yotari", TEXT, ("normal", TEXT), ("Dab1: adaptor", PURPLE), ("reeler-like", RED)),
    ("Dab1 knockout", TEXT, ("normal", TEXT), ("Dab1", PURPLE), ("reeler-like", RED)),
    ("both receptors lost", TEXT, ("normal", TEXT), ("ApoER2 + VLDLR", TEAL), ("close to reeler", RED)),
    ("one receptor lost", TEXT, ("normal", TEXT), ("ApoER2 or VLDLR", TEAL), ("milder", RED)),
]


def table_head(dy=0.0):
    heads = VGroup(*[T(t, 26, GREY).move_to([COLX[k], HDRY + dy, 0]) for k, t in
                     (("m", "Mutant"), ("r", "Reelin gene"), ("o", "Other gene hit"), ("c", "Cortex"))])
    rule = Line([-6.65, 2.3 + dy, 0], [6.65, 2.3 + dy, 0], color=GREY, stroke_width=2)
    return VGroup(heads, rule)


def tcell(col, i, text, color, chipped=False, dy=0.0):
    m = chip(text, color, 26, pad=0.12) if chipped else T(text, 26, color)
    m.move_to([COLX[col], ROWY[i] + dy, 0])
    assert m.width < COLW[col] - 0.1, (text, m.width)
    return m


def tab_row(i, dy=0.0):
    """the pieces of row i, as a dict (some may be missing). dy lifts or drops the whole table."""
    name, ncol, rg, og, cx = ROWS[i]
    d = {"m": tcell("m", i, name, ncol, False, dy)}
    if rg:
        d["r"] = tcell("r", i, rg[0], rg[1], False, dy)
    if og:
        d["o"] = tcell("o", i, og[0], og[1], True, dy)
    d["c"] = tcell("c", i, cx[0], cx[1], False, dy)
    d["line"] = Line([-6.65, ROWY[i] - 0.55 + dy, 0], [6.65, ROWY[i] - 0.55 + dy, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.6)
    return d


def table_parts(n, dy=0.0, skip=()):
    """flat list of the mobjects of the header and the first n rows (skipping dict keys given as (row, key))."""
    out = [table_head(dy)]
    for i in range(n):
        for k, v in tab_row(i, dy).items():
            if (i, k) not in skip:
                out.append(v)
    return out





# ---- the relay's runner (a stick figure, feet on y = yf)
def runner(color, x, yf, h=3.0):
    s = h
    P = lambda dx, dy: np.array([x + dx * s, yf + dy * s, 0])
    head = Circle(radius=0.09 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=1).move_to(P(0.03, 0.88))
    pts = [
        (P(0.03, 0.78), P(-0.02, 0.44)),      # torso
        (P(0.02, 0.74), P(0.20, 0.60)),       # front arm (holds the baton)
        (P(0.02, 0.74), P(-0.18, 0.62)),      # back arm
        (P(-0.02, 0.44), P(0.17, 0.24)),      # front thigh
        (P(0.17, 0.24), P(0.12, 0.0)),        # front shin
        (P(-0.02, 0.44), P(-0.2, 0.2)),       # back thigh
        (P(-0.2, 0.2), P(-0.34, 0.04)),       # back shin
    ]
    lines = [Line(a, b, color=color, stroke_width=2.6 * s) for a, b in pts]
    g = VGroup(head, *lines)
    g.hand = P(0.22, 0.60)
    return g


def baton(at):
    return RoundedRectangle(corner_radius=0.06, width=0.5, height=0.15, stroke_color=WHITE, fill_color=WHITE,
                            fill_opacity=1).move_to(at).rotate(0.4)


# ---- membrane view used by chapters' receptor scenes
MEM_Y = 0.3


def membrane(y=MEM_Y):
    return RoundedRectangle(corner_radius=0.1, width=13.2, height=0.36, stroke_color=GREY, fill_color=GREY,
                            fill_opacity=0.35).move_to([0, y, 0])


def receptor(x, y=MEM_Y, k=1.0):
    body = RoundedRectangle(corner_radius=0.25 * k, width=0.6 * k, height=1.5 * k, stroke_color=TEAL, stroke_width=4,
                            fill_color=TEAL, fill_opacity=0.35).move_to([x, y, 0])
    head = Circle(radius=0.62 * k, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.3).move_to([x, y + 1.35 * k, 0])
    tail = Line([x, y - 0.75 * k, 0], [x, y - 1.5 * k, 0], color=TEAL, stroke_width=6)
    return VGroup(body, head, tail)


# ---- the Predict frame (shared by the predict, pause, reveal and beat scenes)
CELLX = (-0.5, 4.0)
CELLY = -0.15


def predict_frame(filled):
    """returns (group, parts). parts: cells, q1, q2 (questions) or the filled arrows and words."""
    title = T("Predict", 44, GOLD, weight=BOLD).move_to([-4.6, 3.1, 0])
    rowlab = VGroup(T("reeler", 40, RED), T("no Reelin", 28, GREY)).arrange(DOWN, buff=0.15).move_to([-4.7, CELLY, 0])
    heads = VGroup(T("Dab1 protein", 32, PURPLE).move_to([CELLX[0], 3.1, 0]),
                   T("Dab1 phosphorylated", 32, PURPLE).move_to([CELLX[1] + 0.1, 3.1, 0]))
    cells = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.3, height=5.5, stroke_color=PURPLE, stroke_width=3,
                                      fill_color=PURPLE, fill_opacity=0.07).move_to([x, CELLY, 0]) for x in CELLX])
    parts = {"title": title, "rowlab": rowlab, "heads": heads, "cells": cells}
    if not filled:
        parts["q"] = VGroup(*[T("?", 130, GOLD, weight=BOLD).move_to([x, CELLY, 0]) for x in CELLX])
    else:
        up = arr([CELLX[0], 0.0, 0], [CELLX[0], 1.4, 0], PURPLE, w=10, tip=0.4)
        dn = arr([CELLX[1], 1.4, 0], [CELLX[1], 0.0, 0], PURPLE, w=10, tip=0.4)
        w1 = T("more than normal", 32, TEXT).move_to([CELLX[0], -0.85, 0])
        w2 = T("less than normal", 32, TEXT).move_to([CELLX[1], -0.85, 0])
        parts["a1"], parts["a2"], parts["w1"], parts["w2"] = up, dn, w1, w2
    g = VGroup(*parts.values())
    return g, parts


def dish(cx, cy, r=2.4):
    return Circle(radius=r, stroke_color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])


def clock(cx, cy, r=0.9):
    face = Circle(radius=r, stroke_color=TEXT, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    ticks = VGroup(*[Line([cx + 0.8 * r * np.sin(a), cy + 0.8 * r * np.cos(a), 0], [cx + 0.95 * r * np.sin(a), cy + 0.95 * r * np.cos(a), 0],
                          color=TEXT, stroke_width=3) for a in np.arange(12) * PI / 6])
    hand = Line([cx, cy, 0], [cx, cy + 0.7 * r, 0], color=GOLD, stroke_width=6)
    return VGroup(face, ticks), hand


# =============================================================== scenes
class S00Title(TitleCard):
    LESSON = "Reelin and the reeler mouse"
    TITLE = "Matching Mutants, One Relay"
    def construct(self):
        title = T("Matching Mutants,\nOne Relay", 56, font=TITLE_FONT, line_spacing=1.2)
        lesson = T(self.LESSON, 28, GREY).move_to([0, 2.5, 0])
        rule = Line([-2,-1.9,0],[2,-1.9,0],color=GOLD,stroke_width=4)
        self.add(title, lesson, rule)
        self.wait(self.narration_s)


class S01Q(Sc):
    def construct(self):
        cell = Circle(radius=2.65, color=GREY, fill_opacity=0.1).move_to([1,-0.3,0])
        box = chip("?", TEAL, 64).move_to([-1.65,-0.3,0])
        self.add(cell, box)
        self.at("outside a cell")
        dots = VGroup(*[Dot([x,y,0],radius=.16,color=YELLOW) for x,y in [(-5.3,1.9),(-4.7,.5),(-5.8,-1.3)]])
        sig = chip("signal",YELLOW,36).move_to([-4.8,3,0])
        self.play(FadeIn(dots),FadeIn(sig),run_time=.35)
        self.play(*[d.animate.shift(RIGHT*1.9) for d in dots],run_time=.7)
        self.at("a reader inside")
        inside = T("reader inside?",34,TEAL).move_to([1,-.3,0])
        self.play(FadeIn(inside),run_time=.35)
        self.at("where does")
        self.play(ReplacementTransform(sig,chip("Reelin",YELLOW,36).move_to(sig)),run_time=.35)
        self.at("what reads")
        self.play(Indicate(box,color=TEAL),run_time=.6)
        self.finish()


class S02Clone(Sc):
    def construct(self):
        credit = T("D’Arcangelo, Curran and colleagues, 1995",28,GREY).move_to([0,3.35,0])
        gene = Rectangle(width=11.6,height=1.05,color=GREY,fill_opacity=.25).move_to([0,1.55,0])
        label = T("Reelin gene",38,TEXT).move_to(gene)
        # The full-width gene and its protein output share one readable stage.
        segs = VGroup(*[Rectangle(width=1.25,height=1.2,color=YELLOW,fill_opacity=.25) for _ in range(9)]).arrange(RIGHT,buff=.02).move_to([0,-1.5,0])
        proteinlab = T("protein encoded by this gene",30,GREY).move_to([0,-2.8,0])
        self.add(credit,gene,label,segs,proteinlab,arr([0,.8,0],[0,-.7,0]))
        self.at("cloned the gene")
        self.play(Indicate(gene),run_time=.4)
        self.at("broken in")
        broken = T("broken in reeler",30,RED).move_to([3.7,.4,0])
        self.play(FadeIn(broken),run_time=.35)
        self.at("very large")
        self.play(GrowFromEdge(segs,LEFT),ReplacementTransform(proteinlab,T("Reelin — a very large protein",38,YELLOW).move_to(proteinlab)),run_time=.75)
        self.wait(2)
        self.finish()


class S03Cr50(Sc):
    def construct(self):
        cr,late,early,sub=normal_final(0)
        ctx=VGroup(slab(0),cr,late,early,sub)
        self.add(ctx,T("Ogawa, Mikoshiba and colleagues, 1995",26,GREY).move_to([0,-3.45,0]))
        mz=T("marginal zone",28,YELLOW).move_to([-4.65,2.4,0])
        leader=Line([-3.1,2.4,0],[-2.25,2.4,0],color=YELLOW)
        self.add(mz,leader)
        self.at("an antibody")
        ab=antibody(1.5).rotate(PI/2).move_to([4.5,.7,0])
        abl=T("CR-50 antibody",28,TEXT).move_to([4.6,-.6,0])
        self.play(FadeIn(ab),FadeIn(abl),run_time=.4)
        self.at("that stained")
        self.play(ab.animate.move_to([3.3,2,0]),run_time=.5)
        glow=VGroup(*[Circle(radius=.34,stroke_width=0,fill_color=YELLOW,fill_opacity=.35).move_to(c) for c in cr])
        self.play(FadeIn(glow),FadeIn(T("Cajal-Retzius (CR) cells",30,YELLOW).move_to([0,3.35,0])),run_time=.4)
        self.finish()


class S04Cult(Sc):
    def construct(self):
        cr,late,early,sub=normal_final(-3)
        tissue=VGroup(slab(-3),late,early,sub)
        cap=T("normal cortical tissue",28,TEXT).move_to([-3,-3.3,0])
        cell=neuron(2.4,2.2,YELLOW,.5)
        cl=T("Cajal-Retzius cell",28,YELLOW).move_to([3.5,3.2,0])
        rel=chip("Reelin",YELLOW,32).move_to([2.4,.6,0])
        ab=antibody(1).rotate(PI/2).move_to([5.5,.6,0])
        self.add(tissue,cap,cell,cl,rel,ab,T("Culture experiments, 1997",26,GREY).move_to([-3,3.35,0]))
        self.at("it made")
        self.play(rel.animate.move_to([1,.6,0]),ab.animate.move_to([2.2,.6,0]),run_time=.45)
        self.at("organize")
        self.play(ReplacementTransform(cap,T("with antibody",30,RED).move_to(cap)),
                  late.animate.set_y(.7).rotate(.12),early.animate.set_y(.1).rotate(-.15),
                  sub.animate.set_y(-.5).rotate(.18),run_time=.55)
        caveat=T("In culture:\ndisturbed layering,\nlike reeler",30,RED,line_spacing=1.2).move_to([3,-2.2,0])
        self.play(FadeIn(caveat),run_time=.3)
        self.at("it recognizes")
        self.play(Indicate(VGroup(ab,rel)),run_time=.5)
        self.at("secreted protein")
        drops=VGroup(*[Dot([2.4,1.8-i*.3,0],radius=.12,color=YELLOW) for i in range(3)])
        self.play(FadeIn(drops),run_time=.25)
        self.play(drops.animate.shift(DOWN*.6+LEFT*.6),run_time=.5)
        self.finish()


class S05Geom(Sc):
    def construct(self):
        cr,late,early,sub=normal_final(0)
        self.add(slab(0),cr,early,sub)
        self.at("is made at")
        haze=VGroup(*[Rectangle(width=4.35,height=.3,stroke_width=0,fill_color=YELLOW,fill_opacity=o).move_to([0,y,0]) for y,o in [(2.65,.3),(2.35,.2),(2.05,.1)]])
        self.play(FadeIn(haze),FadeIn(T("Reelin",36,YELLOW).move_to([-4.5,2.5,0])),run_time=.35)
        self.add(T("marginal zone",28,YELLOW).move_to([4.5,2.5,0]),Line([2.25,2.5,0],[3.1,2.5,0],color=YELLOW))
        self.at("each new wave")
        late.set_y(Y_START)
        self.add(late)
        self.play(late.animate.set_y(Y_LATE),run_time=.65)
        self.at("should stop")
        stop=T("new wave stops here",30,GREEN).move_to([4.4,1.3,0])
        self.play(FadeIn(stop),run_time=.3)
        self.finish()


class S06Scr(Sc):
    def construct(self):
        dy = -1.5
        head, r0, r1 = table_head(dy), tab_row(0, dy), tab_row(1, dy)
        self.play(FadeIn(head), FadeIn(VGroup(*r0.values())), run_time=0.6)
        self.at("scrambler")
        self.play(FadeIn(r1["m"]), FadeIn(r1["line"]), run_time=0.5)
        self.at("looked like")
        self.play(FadeIn(r1["c"], shift=LEFT * 0.2), run_time=0.5)
        self.at("a normal")
        self.play(FadeIn(r1["r"], scale=0.9), Indicate(r1["r"], color=TEXT), run_time=0.7)
        self.finish()


class S07Dab(Sc):
    def construct(self):
        dy = -1.5
        credit = lab("1997", GREY, 28).move_to([0, 2.75, 0])
        r1 = tab_row(1, dy)
        moving = table_parts(2, dy, skip=((1, "o"),))
        self.play(*[FadeIn(m) for m in moving], FadeIn(credit), run_time=0.5)
        self.at("mutations")
        dab = tcell("o", 1, "Dab1", PURPLE, True, dy)
        self.play(FadeIn(dab, scale=0.8), run_time=0.5)
        self.at("protein")
        self.play(ReplacementTransform(dab, r1["o"]), run_time=0.6)
        moving.append(r1["o"])
        self.at("knockout")
        r2 = tab_row(2, dy + 0.5)
        self.play(*[m.animate.shift(UP * 0.5) for m in moving], FadeIn(r2["m"]), FadeIn(r2["line"]), FadeIn(r2["o"]), FadeIn(r2["r"]), run_time=0.7)
        self.at("same picture")
        self.play(FadeIn(r2["c"], shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S08Rec(Sc):
    def construct(self):
        # Keep the receptor heads below their names and the historical credit.
        rl,rr=receptor(-2.8,-.25,1.15),receptor(2.8,-.25,1.15)
        self.add(membrane(-.25),rl,rr,T("Herz laboratory, 1999",28,GREY).move_to([0,3.55,0]),T("inside the cell",28,GREY).move_to([0,-3.25,0]))
        self.at("removed two",lead=0)
        self.play(Create(cross([-2.8,.1,0],.5)),Create(cross([2.8,.1,0],.5)),rl.animate.set_opacity(.5),rr.animate.set_opacity(.5),run_time=.4)
        self.at("lipoprotein receptors")
        self.add(T("two lipoprotein receptors",30,TEAL).move_to([0,-2.65,0]))
        self.at("ApoER2")
        self.play(FadeIn(T("ApoER2",38,TEAL).move_to([-2.8,2.65,0])),run_time=.3)
        self.at("VLDLR")
        self.play(FadeIn(T("VLDLR",38,TEAL).move_to([2.8,2.65,0])),run_time=.3)
        self.wait(1)
        self.finish()


class S09Recres(Sc):
    def construct(self):
        self.add(*table_parts(3))
        r3,r4=tab_row(3),tab_row(4)
        self.play(FadeIn(VGroup(*[v for k,v in r3.items() if k!='c'])),run_time=.25)
        self.at("close to")
        self.play(FadeIn(r3['c']),run_time=.3)
        self.at("without one")
        self.play(FadeIn(VGroup(*[v for k,v in r4.items() if k!='c'])),run_time=.3)
        self.at("was milder")
        self.play(FadeIn(r4['c']),run_time=.3)
        self.add(T("Single losses differ by brain region",26,GREY).move_to([0,-3.5,0]))
        self.wait(2)
        self.finish()


def relay_three(h=3.4, yf=-1.7, xs=(-4.6, 0.0, 4.6), lsize=32):
    names = [("Reelin", YELLOW), ("receptors", TEAL), ("Dab1", PURPLE)]
    out = []
    for (n, c), x in zip(names, xs):
        r = runner(c, x, yf, h)
        label = lab(n, c, lsize).move_to([x, yf - 0.6, 0])
        g = VGroup(r, label)
        g.hand = r.hand
        out.append(g)
    return out


class S10Relay(Sc):
    def construct(self):
        rs=relay_three(4,-1.9)
        self.add(*rs,Line([-6.5,-1.95,0],[6.5,-1.95,0],color=GREY))
        bt=baton(rs[0].hand)
        self.add(bt)
        self.at("relay race")
        self.play(bt.animate.move_to(rs[1].hand),run_time=.45)
        self.play(bt.animate.move_to(rs[2].hand),run_time=.45)
        self.play(bt.animate.move_to(rs[0].hand),run_time=.3)
        self.at("remove a runner")
        self.play(rs[1][0].animate.set_opacity(.2),Create(cross([0,.4,0],.6)),run_time=.4)
        self.at("the baton")
        self.play(bt.animate.move_to([-1.6,.5,0]),run_time=.5)
        self.at("never arrives")
        self.play(FadeIn(T("the baton stops at the gap",38,RED).move_to([0,3.1,0])),run_time=.3)
        self.finish()


class S11Two(Sc):
    def construct(self):
        rl=runner(YELLOW,-5,-1,3.2); rd=runner(PURPLE,5,-1,3.2)
        up=runner(TEAL,0,.8,2.1); lo=runner(TEAL,0,-2.6,2.1)
        ul=T("ApoER2",30,TEAL).move_to([0,.3,0]); ll=T("VLDLR",30,TEAL).move_to([0,-3.15,0])
        self.add(rl,rd,T("Reelin",32,YELLOW).move_to([-5,-1.6,0]),T("Dab1",32,PURPLE).move_to([5,-1.6,0]))
        bt=baton(rl.hand); self.add(bt)
        self.at("two runners")
        # End every route at a hand, never through a runner's body.
        routes=VGroup(*[Line(a,b,color=GREY,stroke_width=3) for a,b in [(rl.hand,[-.378,2.102,0]),(rl.hand,[-.378,-1.298,0]),(up.hand,[4.424,.984,0]),(lo.hand,[4.424,.984,0])]])
        routes.set_z_index(-1)
        self.play(FadeIn(up),FadeIn(lo),FadeIn(ul),FadeIn(ll),FadeIn(routes),run_time=.45)
        self.at("partly overlapping")
        self.play(Indicate(up,color=TEAL),Indicate(lo,color=TEAL),run_time=.4)
        self.at("lose one")
        res=T("milder than reeler",36,RED).move_to([0,3.4,0])
        self.play(up.animate.set_opacity(.25),Create(cross([0,1.9,0],.45)),FadeIn(res),run_time=.35)
        self.at("some signal")
        self.play(bt.animate.move_to(lo.hand),run_time=.4)
        self.at("gets through")
        self.play(bt.animate.move_to(rd.hand),run_time=.4)
        self.at("lose both")
        self.play(FadeOut(res),lo.animate.set_opacity(.25),Create(cross([0,-1.5,0],.45)),bt.animate.move_to(rl.hand),run_time=.35)
        self.at("close to")
        self.play(routes.animate.set_opacity(.2),FadeIn(T("close to reeler",38,RED).move_to([0,3.4,0])),run_time=.4)
        self.wait(3)
        self.finish()


class S12Order(Sc):
    def construct(self):
        cs = VGroup(*[cortex(x, "reeler", 0.85, -0.3) for x in (-4.5, 0, 4.5)])
        ls = VGroup(*[T(t, 28, RED).move_to([x, 3.3, 0]) for t, x in (("no Reelin", -4.5), ("no Dab1", 0), ("no receptors", 4.5))])
        self.play(FadeIn(cs), FadeIn(ls), run_time=0.6)
        self.at("one relay")
        rs = relay_three(3.7, -2.0)
        track = Line([-6.5, -2.05, 0], [6.5, -2.05, 0], color=GREY, stroke_width=6)
        self.play(FadeOut(cs), FadeOut(ls), FadeIn(track), *[FadeIn(r) for r in rs], run_time=0.35)
        self.at("do not give")
        self.play(Swap(rs[0], rs[1], path_arc=-PI / 2), run_time=0.4)
        self.play(Swap(rs[1], rs[2], path_arc=-PI / 2), run_time=0.4)
        self.at("its order")
        q = T("?", 120, GOLD, weight=BOLD).move_to([0, 2.7, 0])
        ol = lab("order?", GOLD, 38).move_to([2.2, 2.7, 0])
        self.play(Write(q), FadeIn(ol), Swap(rs[0], rs[2], path_arc=-PI / 2), run_time=0.7)
        self.finish()


class S13Predict(Sc):
    def construct(self):
        g, p = predict_frame(False)
        self.play(FadeIn(p["title"]), FadeIn(p["rowlab"]), FadeIn(p["cells"]), run_time=0.5)
        self.at("without")
        self.play(Indicate(p["rowlab"], color=RED, scale_factor=1.12), run_time=0.6)
        self.at("is there more")
        self.play(FadeIn(p["heads"][0]), FadeIn(p["q"][0], scale=0.7), run_time=0.5)
        self.at("or less")
        self.play(Indicate(p["q"][0], color=GOLD, scale_factor=1.15), run_time=0.5)
        self.at("and is more")
        self.play(FadeIn(p["heads"][1]), FadeIn(p["q"][1], scale=0.7), run_time=0.5)
        self.at("or less", nth=1)
        self.play(Indicate(p["q"][1], color=GOLD, scale_factor=1.15), run_time=0.5)
        self.finish()


class S14Pause(NarratedScene):
    def construct(self):
        g,_=predict_frame(False); self.add(g)
        for n in range(5,0,-1):
            cue=T("Think  "+str(n),30,GOLD).move_to([-.3,-3.4,0])
            self.add(cue); self.wait(1); self.remove(cue)


class S15Reveal(Sc):
    def construct(self):
        g, p = predict_frame(True)
        q = VGroup(*[T("?", 130, GOLD, weight=BOLD).move_to([x, CELLY, 0]) for x in CELLX])
        base = VGroup(p["title"], p["rowlab"], p["heads"], p["cells"])
        self.add(base, q)
        self.wait(0.2)
        self.at("is more")
        self.play(FadeOut(q[0]), FadeIn(p["a1"]), FadeIn(p["w1"]), run_time=0.7)
        self.at("but less")
        self.play(FadeOut(q[1]), FadeIn(p["a2"]), FadeIn(p["w2"]), run_time=0.7)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        g, _ = predict_frame(True)
        self.add(g)
        self.wait(self.narration_s)


class S17Logic(Sc):
    def construct(self):
        r=chip("Reelin",YELLOW,52).move_to([-3.8,1.3,0]); d=chip("Dab1",PURPLE,52).move_to([3.8,1.3,0])
        q=T("Which acts first?",46,GOLD).move_to([0,-1.3,0])
        self.add(r,d,q,DoubleArrow(r.get_right(),d.get_left(),color=GREY,buff=.15))
        self.at("so add")
        self.clear()
        plate=dish(-3.4,-.3,2.8)
        cells=VGroup(*[chip("Dab1",PURPLE,28).move_to([x,y,0]) for x,y in [(-4.5,.5),(-2.4,.5),(-3.4,-1.2)]])
        r=chip("Reelin",YELLOW,34).move_to([-3.4,3,0])
        face,hand=clock(3.6,.4,1.5)
        neurons=VGroup(*[Circle(radius=.75,color=GREY,fill_opacity=.1).move_to(c) for c in cells])
        self.add(T("cultured neurons",26,GREY).move_to([-3.4,-2.5,0]))
        self.add(plate,neurons,cells,r,face,hand,T("minutes",38,GOLD).move_to([3.6,-1.55,0]),T("Cooper laboratory, 1999",26,GREY).move_to([0,-3.45,0]))
        drops=VGroup(*[Dot([-3.9+i*.5,2.5,0],radius=.13,color=YELLOW) for i in range(3)])
        self.play(FadeIn(drops),run_time=.2)
        self.play(drops.animate.shift(DOWN*1.1),run_time=.6)
        self.at("is phosphorylated")
        for c in cells:
            pb=pbadge(.23).move_to(c.get_right()+RIGHT*.2)
            self.play(Rotate(hand,-PI/2,about_point=[3.6,.4,0]),FadeIn(pb),run_time=.35)
        self.at("within minutes")
        self.play(FadeIn(T("Reelin → Dab1",38,YELLOW).move_to([3.6,2.8,0])),run_time=.3)
        self.add(T("Reelin is upstream of Dab1",30,YELLOW).move_to([2.8,-2.6,0]))
        self.wait(.7)
        self.finish()


class S18Bind(Sc):
    def construct(self):
        my=.65
        rl,rr=receptor(-3,my,.9),receptor(3,my,.9)
        dabs=VGroup(*[chip("Dab1",PURPLE,38).move_to([x,-1.25,0]) for x in [-3,3]])
        self.add(membrane(my),rl,rr,dabs,T("ApoER2",30,TEAL).move_to([-5,1.9,0]),T("VLDLR",30,TEAL).move_to([5,1.9,0]),T("cytoplasm",28,GREY).move_to([-5,-2.9,0]))
        rel=chip("Reelin",YELLOW,40).move_to([0,3.1,0])
        self.at("binds both")
        self.play(FadeIn(rel),Create(Line(rel.get_left(),rl[1].get_top(),color=YELLOW)),Create(Line(rel.get_right(),rr[1].get_top(),color=YELLOW)),run_time=.6)
        self.at("then the kinases")
        kin=VGroup(chip("Fyn",PINK,32).move_to([-1,-2.9,0]),chip("Src",PINK,32).move_to([1,-2.9,0]))
        self.play(FadeIn(kin),run_time=.3)
        self.play(kin[0].animate.move_to([-3,-2.5,0]),kin[1].animate.move_to([3,-2.5,0]),run_time=.5)
        self.at("add phosphate")
        ps=VGroup(*[pbadge(.25).move_to(k.get_top()+UP*.3) for k in kin])
        self.play(FadeIn(ps),run_time=.25)
        self.play(*[pb.animate.move_to(d.get_right()+RIGHT*.25) for pb,d in zip(ps,dabs)],run_time=.6)
        self.add(T("on tyrosine (Y)",30,GOLD).move_to([0,-3.4,0]))
        self.finish()


class S19Off(Sc):
    def construct(self):
        title=T("One explanation for the build-up",36,TEXT).move_to([0,3.55,0])
        bucket=VGroup(Line([-5.9,2.05,0],[-5.9,-2.9,0],color=PURPLE,stroke_width=6),Line([-5.9,-2.9,0],[-.2,-2.9,0],color=PURPLE,stroke_width=6),Line([-.2,-2.9,0],[-.2,2.05,0],color=PURPLE,stroke_width=6))
        signal=chip("Reelin signal",YELLOW,28,pad=.16).move_to([-3.1,2.95,0])
        dab=chip("Dab1",PURPLE,40).move_to([-3.1,1.5,0])
        balls=VGroup(*[Dot([x,-1.5,0],radius=.28,color=PURPLE) for x in [-4.7,-3.1,-1.5]])
        note=T("Schematic, not measured amounts",28,TEXT).move_to([0,-3.5,0])
        self.add(title,bucket,signal,dab,balls,note)
        self.at("phosphorylated")
        pb=pbadge(.28).move_to(dab.get_right()+RIGHT*.32)
        self.play(FadeIn(pb),run_time=.3)
        self.at("destroyed through")
        cul=chip("Cullin 5 ligase",TAN,34).move_to([3.1,1.5,0])
        tag=chip("tag",TAN,28).move_to([-3.1,.35,0])
        link=arr(cul.get_left(),tag.get_right(),TAN)
        attachment=Line(dab.get_bottom(),tag.get_top(),color=TAN,stroke_width=4)
        self.play(FadeIn(cul),run_time=.2)
        self.play(GrowArrow(link),FadeIn(tag),Create(attachment),run_time=.3)
        self.wait(.2)
        self.play(FadeOut(dab),FadeOut(pb),FadeOut(tag),FadeOut(attachment),FadeOut(link),run_time=.2)
        # Large Dab1 balls visibly exit the open bucket before breaking apart.
        self.play(balls.animate.set_y(2.35),run_time=.35)
        self.play(balls.animate.set_x(3.1),run_time=.35)
        self.play(balls.animate.set_y(-.5),run_time=.2)
        fragments=VGroup(*[Dot([2.1+(i%4)*.65,-.5-(i//4)*.55,0],radius=.15,color=PURPLE) for i in range(12)])
        broken=T("breakdown",32,TAN).move_to([3.1,-2.5,0])
        self.play(ReplacementTransform(balls,fragments),FadeIn(broken),run_time=.25)
        self.wait(.25)
        self.at("and without")
        off=T("without Reelin",32,RED).move_to(signal)
        self.play(ReplacementTransform(signal,off),FadeOut(cul),FadeOut(fragments),FadeOut(broken),run_time=.3)
        self.at("less of it")
        less=T("less phosphorylation\n↓\nless breakdown",32,GOLD,line_spacing=1.1).move_to([3.2,.8,0])
        self.play(FadeIn(less),run_time=.3)
        pile=VGroup(*[Dot([-5.2+(i%7)*.7,-2.45+(i//7)*.7,0],radius=.25,color=PURPLE) for i in range(28)])
        self.play(LaggedStart(*[FadeIn(d,shift=DOWN*.5) for d in pile],lag_ratio=.025),run_time=.8)
        self.add(T("unphosphorylated\nDab1 accumulates",32,PURPLE).move_to([3.2,-1.7,0]))
        self.wait(3)
        self.finish()


class S20Cul(Sc):
    def construct(self):
        cr,late,early,sub=normal_final(0)
        late.set_y(Y_START)
        self.add(slab(0),cr,early,sub,late,T("Cooper laboratory, 2007",26,GREY).move_to([0,3.5,0]))
        cul=chip("Cullin 5",TAN,36).move_to([-4.5,1.5,0])
        self.add(cul)
        self.at("knock down")
        self.play(Create(cross([-4.5,.45,0],.4)),FadeIn(T("knocked down",28,RED).move_to([-4.5,-.4,0])),run_time=.4)
        self.at("active")
        dab=chip("active Dab1",PURPLE,32).move_to([4.5,-.7,0])
        self.play(FadeIn(dab),run_time=.3)
        self.at("builds up")
        ps=VGroup(*[pbadge(.24).move_to([3.7+i*.55,.25,0]) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(pb) for pb in ps],lag_ratio=.15),run_time=.5)
        stop=DashedLine([-2.2,1.6,0],[2.2,1.6,0],color=TEXT)
        self.add(stop,T("normal stop",28,TEXT).move_to([4.5,1.6,0]))
        self.at("neurons migrate")
        self.play(late.animate.set_y(1.45),run_time=.5)
        self.at("too far")
        extra=wave(0,LB,Y_START,GREEN); self.add(extra)
        self.play(late.animate.set_y(2.17),extra.animate.set_y(1.88),run_time=.65)
        self.add(T("pile-up at top",30,GREEN).move_to([4.5,2.65,0]))
        self.wait(3)
        self.finish()


class S21Sym(Sc):
    def construct(self):
        # All three states are present for the entire comparison.
        for x,kind,label,col in [(-4.5,'reeler','no Reelin',RED),(0,'normal','normal',TEXT),(4.5,'cul','Cullin 5 knocked down',TAN)]:
            ctx=cortex(0,kind)
            ctx.stretch(.78,0).stretch(.94,1).move_to([x,-.25,0])
            self.add(ctx,T(label if kind!='cul' else 'Cullin 5\nknocked down',28,col).move_to([x,3.25,0]))
        self.add(T("new below old",27,RED).move_to([-4.5,-3.4,0]),T("inside-out",28,TEXT).move_to([0,-3.4,0]),T("pile-up at top",27,GREEN).move_to([4.5,-3.4,0]))
        self.at("normal positioning")
        self.at("the signal")
        self.at("and its")
        self.finish()
        self.wait(1)


class S22Take(Sc):
    def construct(self):
        defs=[('Reelin',YELLOW),('ApoER2 /\nVLDLR',TEAL),('Fyn / Src',PINK),('Dab1',PURPLE),('Cullin 5',TAN)]
        positions=[[-5.15,1.15,0],[-2.65,.1,0],[0,-1,0],[2.65,-1.85,0],[5.15,-2.7,0]]
        nodes=VGroup(*[chip(n,c,38).move_to(pos) for (n,c),pos in zip(defs,positions)])
        arrows=VGroup(*[arr(a.get_right(),b.get_left(),defs[i][1],w=5) for i,(a,b) in enumerate(zip(nodes,nodes[1:]))])
        self.add(T("Matching mutants suggest one relay",38,GOLD).move_to([0,3.35,0]),nodes,arrows)
        self.at("adding")
        self.play(Indicate(nodes[0],color=YELLOW),run_time=.5)
        self.at("watching")
        # Badge sits beside Dab1; the ordering bracket ends at the box itself.
        pb=pbadge(.28).move_to(nodes[3].get_right()+RIGHT*.32)
        self.play(FadeIn(pb),run_time=.4)
        self.at("puts")
        bracket=VGroup(DashedLine([-5.15,2.25,0],[2.65,2.25,0],color=YELLOW),
                       DashedLine([-5.15,2.25,0],nodes[0].get_top(),color=YELLOW),
                       arr([2.65,2.25,0],nodes[3].get_top(),YELLOW,w=4))
        self.play(Create(bracket),FadeIn(T("ordered by adding Reelin",30,YELLOW).move_to([-1.25,2.7,0])),run_time=.5)
        self.at("the binding studies")
        binding=T("receptors placed\nby binding studies",30,TEAL).move_to([-3.8,-2.65,0])
        lead=Line(nodes[1].get_bottom(),[-2.65,-2.05,0],color=TEAL)
        self.play(Create(lead),FadeIn(binding),run_time=.5)
        self.at("between them")
        self.play(Indicate(nodes[1],color=TEAL,scale_factor=1.08),run_time=.5)
        self.finish()


class S23End(EndCard):
    LINE = "Matching mutants suggest one relay, with Reelin upstream of Dab1."
    def construct(self):
        line=T("Matching mutants suggest one relay,\nwith Reelin upstream of Dab1.",46,font=TITLE_FONT,line_spacing=1.3)
        self.add(line,T("biochemistrypedia.com",28,TEAL).move_to([0,-2,0]))
        self.wait(self.narration_s)
