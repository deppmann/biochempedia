"""Build a Conditional Test  (tools-for-development, chapter 2, animated 2026-11-11)

COLOR MAP (same as chapter 1)
  BLUE  = observed labels and tracers / measurements     GOLD  = time
  GREEN = inherited mark or reporter                     RED   = intervention (Cre, deletion, target block)
  GREY  = unobserved cells and DNA
All pictures are schematic; no curves are plotted and no molecule is drawn.
"""
import importlib.util
import os
from pathlib import Path as _P

import numpy as np
from bp_style import *  # noqa: F401,F403

_spec = importlib.util.spec_from_file_location("ch1_scenes", str(_P(os.environ["KX_SCRIPT"]).parent.parent / "scenes.py"))
ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ch1)
bob, shimmer, Tree = ch1.bob, ch1.shimmer, ch1.Tree


def motes(scene, seed=1):
    return ch1.motes(scene, n=90, seed=seed)


def schem():
    return T("schematic", 28, TEXT).move_to([0, -3.4, 0])


def mk(text, size=28, color=TEXT):
    return MarkupText(text, font=FONT, font_size=size, color=color)


# ------------------------------------------------------------------ DNA bar with a red block and lox brackets
def dna(cx, cy, w=7.2, h=1.1, bw=2.0, col=RED, brackets=True, label=None):
    bar = Rectangle(width=w, height=h).set_stroke(GREY, 3).set_fill(GREY, 0.45).move_to([cx, cy, 0])
    block = Rectangle(width=bw, height=h).set_stroke(col, 3).set_fill(col, 0.85).move_to([cx, cy, 0])
    br = VGroup()
    if brackets:
        for sx in (-1, 1):
            x = cx + sx * (bw / 2 + 0.1)
            br.add(Line([x, cy - h / 2 - 0.25, 0], [x, cy + h / 2 + 0.25, 0]).set_stroke(RED, 7))
    g = VGroup(bar, block, br)
    g.bar, g.block, g.br = bar, block, br
    if label:
        lb = T(label, 28, TEXT).move_to(block)
        g.add(lb)
        g.lb = lb
    return g


def gauge(cx, cy, tr, w=2.6, h=0.5, col=BLUE):
    box = Rectangle(width=w, height=h).set_stroke(TEXT, 3).set_fill(BG, 1)
    box.move_to([cx, cy, 0])
    fill = Rectangle(width=0.02, height=h - 0.1).set_stroke(width=0).set_fill(col, 0.9)

    def up(m):
        v = max(tr.get_value(), 0.02)
        ww = (w - 0.1) * v
        m.become(Rectangle(width=ww, height=h - 0.1).set_stroke(width=0).set_fill(col, 0.9)
                 .move_to([cx - (w - 0.1) / 2 + ww / 2, cy, 0]))
    fill.add_updater(up)
    up(fill)
    return VGroup(box, fill)


def qmark(pos, size=44, color=TEXT, ph=0.0):
    q = T("?", size, color, weight=BOLD).move_to(pos)
    q._t = 0.0

    def pul(m, dt):
        m._t += dt
        m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 * np.sin(4 * m._t + ph)))
    q.add_updater(pul)
    return q


# ------------------------------------------------------------------ the carried world (hook, question, title)
TREE_C = (-4.4, 0.4)
CELL_C = np.array([1.2, -0.3, 0.0])


def tree(scene, op=1.0):
    t = Tree(TREE_C[0], TREE_C[1], 0.66)
    for i, c in enumerate(t.cells()):
        bob(c, 0.04, 2.6, i)
    if op < 1:
        t.set_opacity(op)
    return t


def gene_cell(center, r=1.6, op=1.0):
    body = Circle(radius=r).set_stroke(GREY, 5).set_fill(GREY, 0.3)
    nuc = Circle(radius=r * 0.5).set_stroke(GREY, 3).set_fill(GREY, 0.5)
    blk = Rectangle(width=r * 0.55, height=r * 0.28).set_stroke(RED, 2).set_fill(RED, 0.9)
    g = VGroup(body, nuc, blk).move_to(center)
    g.body, g.nuc, g.blk = body, nuc, blk
    if op < 1:
        g.set_opacity(op)
    return g


SLOTS = [("target", RED, (1.2, 2.65)), ("place", RED, (4.7, 0.95)), ("time", GOLD, (4.7, -1.75))]


def slot_box(col, pos):
    return DashedVMobject(RoundedRectangle(corner_radius=0.16, width=2.6, height=1.0), num_dashes=36).set_stroke(col, 4).move_to([*pos, 0])


# ====================================================================== S00 hook
class S00Hook(NarratedScene):
    def construct(self):
        motes(self, seed=20)
        t = tree(self)
        cell = gene_cell(np.array([3.0, 0.1, 0.0]), r=1.9)
        bob(cell, 0.05, 3.0)
        lock_b = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.4).set_stroke(RED, 2).set_fill(RED, 1).move_to(cell.blk.get_center() + DOWN * 0.8)
        lock_s = Arc(radius=0.17, start_angle=0, angle=PI, color=RED, stroke_width=5).move_to(lock_b.get_top() + UP * 0.05)
        q = qmark(cell.get_center() + UP * 2.35, 52)
        self.add(t, cell, lock_b, lock_s, q, schem())
        self.wait(self.narration_s + 0.4)


# ====================================================================== S01 question
class S01Question(SpokenScene):
    def construct(self):
        motes(self, seed=21)
        t = tree(self)
        cell = gene_cell(CELL_C)
        bob(cell, 0.04, 3.0)
        self.add(t, cell)
        self.play(Indicate(t.root, scale_factor=1.25, color=GREEN), run_time=1.0)
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.15, color=GREEN) for c in t.g1 + t.g2], lag_ratio=0.2), run_time=1.4)
        self.at("how can we test")
        q = qmark(CELL_C + UP * 1.75 + RIGHT * 0.2, 52)
        self.play(FadeIn(q), Indicate(cell.blk, scale_factor=1.4, color=RED), run_time=1.2)
        self.at("in one cell")
        self.play(Indicate(cell.body, scale_factor=1.08, color=TEXT), run_time=1.0)
        self.at("after birth")
        self.play(Indicate(cell.nuc, scale_factor=1.2, color=GOLD), run_time=1.0)
        self.at("we need to control")
        self.play(FadeOut(q), run_time=0.4)
        boxes, qs, names = [], [], []
        for (nm, col, pos) in SLOTS:
            b = slot_box(col, pos)
            qq = T("?", 44, TEXT, weight=BOLD).move_to([*pos, 0])
            boxes.append(b)
            qs.append(qq)
        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), LaggedStart(*[FadeIn(x) for x in qs], lag_ratio=0.3), run_time=1.6)
        for i, ph in enumerate(["the target", "the place", "the time"]):
            self.at(ph)
            nm, col, pos = SLOTS[i]
            lab = T(nm, 30, col).move_to([*pos, 0])
            self.play(FadeOut(qs[i]), FadeIn(lab, scale=0.8), run_time=0.5)
            self.play(Indicate(boxes[i], scale_factor=1.1, color=col), run_time=0.6)
        self.finish()


# ====================================================================== S02 title
class S02Title(TitleCard):
    LESSON = "Tools for Following Cells and Genes"
    TITLE = "Build a Conditional Test"

    def construct(self):
        super().construct()


# ====================================================================== S03 flox
def flox_row(cy, tag, with_block=True):
    d = dna(-1.0, cy, label="segment")
    tg = T(tag, 28, TEXT).move_to([-4.6, cy + 1.05, 0], aligned_edge=LEFT)
    return d, tg


class S03Flox(SpokenScene):
    def construct(self):
        motes(self, seed=22)
        y1, y2 = 1.7, -1.3
        d1 = dna(-1.0, y1, label="segment")
        bar = d1.bar
        self.play(FadeIn(bar, shift=RIGHT * 0.5), run_time=1.0)
        self.at("the target")
        self.play(FadeIn(d1.block, scale=0.7), FadeIn(d1.lb, scale=0.7), run_time=0.9)
        self.at("place")
        for ln in d1.br:
            ln.shift(UP * 1.5).set_opacity(0)
        self.add(d1.br)
        self.play(*[ln.animate.shift(DOWN * 1.5).set_opacity(1) for ln in d1.br], run_time=1.2)
        self.at("sites")
        lx = [T("loxP", 28, RED).move_to([x, y1 - 1.0, 0]) for x in (-2.1, 0.1)]
        self.play(FadeIn(lx[0], shift=UP * 0.15), FadeIn(lx[1], shift=UP * 0.15), run_time=0.7)
        self.at("gene segment")
        self.play(Indicate(d1.block, scale_factor=1.12, color=RED), run_time=1.0)
        self.at("this floxed")
        tag1 = T("floxed allele", 28, TEXT).move_to([-4.6, y1 + 1.05, 0], aligned_edge=LEFT)
        tr1 = ValueTracker(0)
        g1 = gauge(5.0, y1, tr1)
        q1 = qmark([5.0, y1, 0], 34)
        gl1 = T("output", 28, BLUE).move_to([5.0, y1 + 0.7, 0])
        self.play(FadeIn(tag1), FadeIn(g1), FadeIn(q1), FadeIn(gl1), run_time=1.0)
        self.at("designed to work")
        self.play(Indicate(q1, scale_factor=1.5, color=TEXT), run_time=1.0)
        self.at("until")
        tok = chip("Cre", RED, 28).move_to([-1.0, 3.2, 0])
        self.play(FadeIn(tok, shift=DOWN * 0.3), run_time=0.7)
        self.play(tok.animate.move_to([-1.0, y1 + 0.2, 0]), run_time=1.3)
        self.at("removes")
        ghost = DashedVMobject(Rectangle(width=2.0, height=0.9), num_dashes=20).set_stroke(RED, 3).move_to(d1.block)
        self.play(FadeOut(d1.block), FadeOut(d1.lb), FadeIn(ghost), run_time=0.9)
        self.at("a cre free control")
        self.play(FadeOut(tok, shift=UP * 0.5), run_time=0.4)
        d2 = dna(-1.0, y2, label="segment")
        tag2 = T("Cre-free control", 28, TEXT).move_to([-4.6, y2 + 1.05, 0], aligned_edge=LEFT)
        tr2 = ValueTracker(0)
        g2 = gauge(5.0, y2, tr2)
        q2 = qmark([5.0, y2, 0], 34, ph=1.0)
        lx2 = [T("loxP", 28, RED).move_to([x, y2 - 1.0, 0]) for x in (-2.1, 0.1)]
        self.play(FadeIn(d2, shift=UP * 0.4), FadeIn(tag2), FadeIn(g2), FadeIn(q2), FadeIn(lx2[0]), FadeIn(lx2[1]), run_time=0.8)
        self.at("must test")
        scan = Line([-4.6, y2 - 0.7, 0], [-4.6, y2 + 0.7, 0]).set_stroke(BLUE, 6)
        self.add(scan)
        self.play(scan.animate.move_to([2.6, y2, 0]), run_time=1.4, rate_func=linear)
        self.at("really does work")
        self.play(FadeOut(q2), tr2.animate.set_value(0.9), run_time=1.2)
        wk = T("working", 28, BLUE).move_to([5.0, y2 - 0.7, 0])
        self.play(FadeIn(wk), FadeOut(scan), run_time=0.5)
        self.finish()


# ====================================================================== S04 place
CPOS = [(-4.0, 1.5), (0.0, 1.5), (4.0, 1.5), (-4.0, -1.4), (0.0, -1.4), (4.0, -1.4)]
RING = [1, 2, 4]


def small_cell(pos):
    body = Circle(radius=1.15).set_stroke(GREY, 4).set_fill(GREY, 0.3)
    nuc = Circle(radius=0.5).set_stroke(GREY, 2).set_fill(GREY, 0.5)
    blk = Rectangle(width=0.5, height=0.26).set_stroke(RED, 2).set_fill(RED, 0.9)
    g = VGroup(body, nuc, blk).move_to([*pos, 0])
    g.blk, g.body = blk, body
    return g


class S04Place(SpokenScene):
    def construct(self):
        motes(self, seed=23)
        cells = [small_cell(p) for p in CPOS]
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.2), run_time=1.5)
        for i, c in enumerate(cells):
            bob(c, 0.04, 3.0, i)
        self.at("promoter")
        rings = [DashedVMobject(Circle(radius=1.35), num_dashes=24).set_stroke(RED, 4).move_to(cells[i]) for i in RING]
        cap = T("driver active", 30, RED).move_to([0, 3.3, 0])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(cap), run_time=0.7)
        for r in rings:
            r.add_updater(lambda m, dt: m.rotate(0.25 * dt))
        self.at("supplies")
        toks = [chip("Cre", RED, 26).move_to(cells[i].get_center() + LEFT * 2.0) for i in RING]
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.3) for t in toks], lag_ratio=0.2), run_time=1.0)
        self.at("deletes")
        self.play(FadeOut(cap), *[toks[k].animate.move_to(cells[RING[k]].get_center()) for k in range(3)], run_time=0.8)
        self.play(FadeOut(cells[1].blk), FadeOut(cells[4].blk), Indicate(cells[2].blk, scale_factor=1.5, color=RED), run_time=0.8)
        self.play(*[FadeOut(t) for t in toks], run_time=0.3)
        self.at("largely")
        stray = chip("Cre", RED, 26).move_to([2.0, -1.4, 0])
        self.play(FadeIn(stray, shift=RIGHT * 0.3), run_time=0.5)
        self.play(stray.animate.move_to(cells[5].get_center()), run_time=0.8)
        self.play(FadeOut(cells[5].blk), FadeOut(stray), run_time=0.6)
        self.at("driver's actual")
        scan = Line([-6.0, -2.6, 0], [-6.0, 2.7, 0]).set_stroke(BLUE, 6)
        self.add(scan)
        self.play(scan.animate.move_to([6.0, 0.05, 0]), run_time=2.2, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.2)
        self.at("measured")
        hl = [Circle(radius=1.4).set_stroke(BLUE, 6).move_to(cells[i]) for i in (2, 5)]
        self.play(*[Create(h) for h in hl], run_time=0.8)
        self.at("assumed")
        cap2 = T("measure it, do not assume", 30, BLUE).move_to([0, -3.4, 0])
        self.play(FadeIn(cap2), *[Indicate(h, scale_factor=1.1, color=BLUE) for h in hl], run_time=1.0)
        self.finish()


# ====================================================================== S05 time
class S05Time(SpokenScene):
    def construct(self):
        motes(self, seed=24)
        cc = np.array([0.0, 0.7, 0.0])
        body = Circle(radius=2.0).set_stroke(GREY, 5).set_fill(GREY, 0.25).move_to(cc)
        nucA = Arc(radius=1.0, start_angle=0.6, angle=2 * PI - 1.2).set_stroke(GREY, 6).move_to(cc)
        nucA.move_arc_center_to(cc)
        nucf = Circle(radius=1.0).set_stroke(width=0).set_fill(GREY, 0.45).move_to(cc)
        gate = Arc(radius=1.0, start_angle=-0.6, angle=1.2).set_stroke(GOLD, 11)
        gate.move_arc_center_to(cc)
        blk = Rectangle(width=0.7, height=0.4).set_stroke(RED, 2).set_fill(RED, 0.9).move_to(cc)
        self.play(FadeIn(body), FadeIn(nucf), FadeIn(nucA), FadeIn(blk), run_time=1.2)
        bob(body, 0.04, 3.0)
        ty = -2.8
        line = Line([-6.2, ty, 0], [6.2, ty, 0]).set_stroke(GOLD, 5)
        tb = Line([-5.0, ty - 0.2, 0], [-5.0, ty + 0.2, 0]).set_stroke(GOLD, 5)
        td = Line([1.5, ty - 0.2, 0], [1.5, ty + 0.2, 0]).set_stroke(GOLD, 5)
        lb = T("birth", 28, GOLD).move_to([-5.0, ty - 0.55, 0])
        ld = T("tamoxifen", 28, GOLD).move_to([1.5, ty - 0.55, 0])
        self.play(Create(line), FadeIn(tb), FadeIn(lb), run_time=1.4)
        self.at("creer is designed")
        angs = [90, 150, 210, 270]
        toks = []
        for a in angs:
            p = cc + np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) * 1.5
            toks.append(chip("CreER", RED, 22).move_to(p))
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in toks], lag_ratio=0.2), run_time=1.2)
        for i, t in enumerate(toks):
            bob(t, 0.05, 2.2, i)
        self.at("outside the nucleus")
        self.play(Indicate(nucf, scale_factor=1.05, color=TEXT), run_time=0.9)
        self.at("until")
        head = Dot(radius=0.2, color=GOLD).move_to([-5.0, ty, 0])
        self.add(head)
        self.add(gate)
        self.play(head.animate.move_to([1.5, ty, 0]), FadeIn(td), FadeIn(ld), run_time=1.8, rate_func=linear)
        self.at("a gold time gate")
        self.play(Indicate(gate, scale_factor=1.15, color=GOLD), Flash(head, color=GOLD), run_time=0.8)
        self.at("opens")
        self.play(gate.animate.rotate(0.9, about_point=cc).set_stroke(opacity=0.3), run_time=0.5)
        self.at("after birth")
        gp = cc + np.array([1.0, 0, 0])
        ins = [cc + np.array(v) for v in [(-0.45, 0.5, 0), (0.45, 0.5, 0), (-0.45, -0.5, 0), (0.45, -0.5, 0)]]
        for t in toks:
            t.clear_updaters()
        self.play(*[t.animate.move_to(gp + RIGHT * 0.9 + UP * (0.85 * (i - 1.5))) for i, t in enumerate(toks)], run_time=1.0)
        self.play(*[t.animate.scale(0.55).move_to(ins[i]) for i, t in enumerate(toks)], run_time=1.2)
        self.at("recombination")
        self.play(FadeOut(blk, scale=0.5), run_time=1.0)
        self.play(*[FadeOut(t) for t in toks], run_time=0.6)
        self.at("actual timing")
        q = qmark([3.5, ty + 0.7, 0], 52, GOLD)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


# ====================================================================== S06 genotype
def mouse(cx, cy, w=3.4):
    h = w * 0.5
    body = Ellipse(width=w, height=h).set_stroke(GREY, 4).set_fill(GREY, 0.35).move_to([cx, cy, 0])
    head = Circle(radius=h * 0.38).set_stroke(GREY, 4).set_fill(GREY, 0.35).move_to([cx - w * 0.5, cy + 0.1, 0])
    ear = Circle(radius=h * 0.18).set_stroke(GREY, 3).set_fill(GREY, 0.5).move_to([cx - w * 0.43, cy + h * 0.45, 0])
    eye = Dot(radius=0.06, color=TEXT).move_to([cx - w * 0.6, cy + 0.17, 0])
    tail = CubicBezier([cx + w * 0.5, cy, 0], [cx + w * 0.8, cy + 0.4, 0], [cx + w * 0.7, cy - 0.5, 0], [cx + w * 0.95, cy - 0.1, 0]).set_stroke(GREY, 4)
    return VGroup(tail, body, head, ear, eye)


class S06Genotype(SpokenScene):
    def construct(self):
        motes(self, seed=25)
        y = 1.55
        gl = mk("Avil<sup>Cre</sup>/+", 44, RED).move_to([-2.2, y, 0])
        gr = mk("TrkA<sup>fl</sup>/−", 44, TEXT).move_to([2.4, y, 0])
        semi = T(";", 64, TEXT).move_to([0.1, y - 0.1, 0])
        self.play(FadeIn(gl, shift=RIGHT * 0.3), FadeIn(gr, shift=LEFT * 0.3), FadeIn(semi), run_time=0.8)
        m = mouse(0.0, -2.1)
        self.play(FadeIn(m), run_time=0.8)
        bob(m, 0.05, 2.6)
        self.at("one locus at a time")
        bl = RoundedRectangle(corner_radius=0.16, width=5.2, height=2.4).set_stroke(RED, 4).set_fill(RED, 0.1).move_to([-3.4, y, 0])
        br_ = RoundedRectangle(corner_radius=0.16, width=5.2, height=2.4).set_stroke(GREY, 4).set_fill(GREY, 0.12).move_to([3.4, y, 0])
        al = [chip("Cre", RED, 28).move_to([-4.5, y - 0.6, 0]), chip("+", GREY, 28).move_to([-2.3, y - 0.6, 0])]
        ar = [chip("floxed", RED, 28).move_to([2.4, y - 0.6, 0]), chip("null", GREY, 28).move_to([4.5, y - 0.6, 0])]
        self.play(FadeIn(bl), FadeIn(br_), gl.animate.move_to([-3.4, y + 0.55, 0]), gr.animate.move_to([3.4, y + 0.55, 0]),
                  semi.animate.move_to([0, y - 0.1, 0]), run_time=1.5)
        self.at("avil")
        self.play(FadeIn(al[0], shift=DOWN * 0.2), FadeIn(al[1], shift=DOWN * 0.2), run_time=0.8)
        self.at("one cre driver")
        self.play(Indicate(al[0], scale_factor=1.25, color=RED), run_time=1.0)
        self.at("trk")
        self.play(FadeIn(ar[0], shift=DOWN * 0.2), FadeIn(ar[1], shift=DOWN * 0.2), run_time=0.8)
        self.at("one floxed allele")
        self.play(Indicate(ar[0], scale_factor=1.25, color=RED), run_time=1.0)
        self.at("one null")
        self.play(Indicate(ar[1], scale_factor=1.25, color=GREY), run_time=1.0)
        self.at("the semicolon")
        gl_, gr_ = VGroup(bl, gl, *al), VGroup(br_, gr, *ar)
        self.play(gl_.animate.shift(RIGHT * 0.6), gr_.animate.shift(LEFT * 0.6), Indicate(semi, scale_factor=1.6, color=TEXT), run_time=1.6)
        self.at("joins")
        a1 = Arrow([-2.8, y - 1.2, 0], [-1.2, -1.3, 0], buff=0.05, stroke_width=6, color=RED)
        a2 = Arrow([2.8, y - 1.2, 0], [1.2, -1.3, 0], buff=0.05, stroke_width=6, color=GREY)
        self.play(Create(a1), Create(a2), run_time=1.2)
        self.at("in one mouse")
        self.play(Indicate(m, scale_factor=1.1, color=TEXT), run_time=1.2)
        self.finish()


# ====================================================================== S07 control
CX = [-1.9, 1.1, 4.1]
RY = [2.1, 0.0, -2.1]


def acard(kind, x, y):
    col = {"cre": RED, "fl": GREY, "null": GREY, "plus": GREY}[kind]
    box = RoundedRectangle(corner_radius=0.14, width=2.8, height=1.3).set_stroke(col, 4).set_fill(col, 0.14)
    if kind == "cre":
        parts = [T("Cre", 30, RED)]
    elif kind == "fl":
        parts = [T("TrkA fl", 28, TEXT).shift(UP * 0.18), Rectangle(width=1.1, height=0.2).set_stroke(RED, 2).set_fill(RED, 0.9).shift(DOWN * 0.38)]
    elif kind == "null":
        parts = [T("TrkA null", 28, TEXT)]
    else:
        parts = [T("TrkA +", 28, TEXT)]
    g = VGroup(box, *parts).move_to([x, y, 0])
    g.box = box
    return g


def mrow(y, kinds):
    return VGroup(*[acard(k, x, y) for k, x in zip(kinds, CX)])


class S07Control(SpokenScene):
    def construct(self):
        motes(self, seed=26)
        r0 = mrow(RY[0], ["cre", "fl", "null"])
        t0 = T("Experiment", 28, TEXT).move_to([-5.2, RY[0], 0])
        self.play(FadeIn(r0, shift=RIGHT * 0.3), FadeIn(t0), run_time=1.5)
        self.at("one causal piece")
        self.play(Indicate(r0, scale_factor=1.04, color=TEXT), run_time=1.2)
        self.at("keep the floxed")
        r1 = r0.copy().move_to([r0.get_center()[0], RY[1], 0])
        t1 = T("Control 1", 28, TEXT).move_to([-5.2, RY[1], 0])
        self.play(FadeIn(r1), FadeIn(t1), run_time=1.5)
        self.play(Indicate(r1[1], scale_factor=1.1, color=TEXT), Indicate(r1[2], scale_factor=1.1, color=TEXT), run_time=1.2)
        self.at("but remove")
        hole = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.8, height=1.3), num_dashes=28).set_stroke(TEXT, 3).move_to([CX[0], RY[1], 0])
        self.play(r1[0].animate.shift(UP * 0.5).set_opacity(0), FadeIn(hole), run_time=1.3)
        self.at("that mouse")
        self.play(Indicate(r1[1], scale_factor=1.1, color=GREY), Indicate(r1[2], scale_factor=1.1, color=GREY), run_time=1.4)
        self.at("without triggering")
        self.play(Indicate(hole, scale_factor=1.1, color=TEXT), run_time=1.2)
        self.at("a second control")
        r2 = r0.copy().move_to([r0.get_center()[0], RY[2], 0])
        t2 = T("Control 2", 28, TEXT).move_to([-5.2, RY[2], 0])
        self.play(FadeOut(hole), FadeIn(r2), FadeIn(t2), run_time=1.5)
        self.at("retain")
        self.play(Indicate(r2[0], scale_factor=1.12, color=RED), run_time=1.0)
        self.at("working")
        new = acard("plus", CX[2], RY[2])
        self.play(FadeOut(r2[2]), FadeIn(new), run_time=1.0)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.0, height=1.5), num_dashes=28).set_stroke(TEXT, 3).move_to(new)
        self.play(Create(box), run_time=0.8)
        self.play(Indicate(new, scale_factor=1.1, color=GREY), run_time=1.0)
        self.finish()


# ====================================================================== S08 / S09 predict
def predict_frame(scene, pulse=True):
    cell = Circle(radius=3.3).set_stroke(GREEN, 5).set_fill(GREEN, 0.18)
    if pulse:
        shimmer(cell, 3.0, 0.12, 0.3)
    rep = dna(-1.9, 0.3, w=2.3, h=0.6, bw=0.9, col=GREEN)
    tar = dna(1.9, 0.3, w=2.3, h=0.6, bw=0.9, col=RED)
    lr = T("reporter", 28, GREEN).move_to([-1.9, -0.55, 0])
    lt = T("target", 28, RED).move_to([1.9, -0.55, 0])
    q = T("?", 80, TEXT, weight=BOLD).move_to([0, 0.3, 0])
    return cell, rep, tar, lr, lt, q


class S08Predict(SpokenScene):
    def construct(self):
        motes(self, seed=28)
        cell, rep, tar, lr, lt, q = predict_frame(self)
        self.play(FadeIn(cell, scale=0.85), run_time=2.0)
        self.at("a cell glows")
        self.play(Indicate(cell, scale_factor=1.03, color=GREEN), run_time=1.0)
        self.at("reporter")
        self.play(FadeIn(rep, scale=0.9), FadeIn(lr), run_time=1.2)
        self.at("does that glow")
        self.play(Indicate(rep.block, scale_factor=1.3, color=GREEN), run_time=1.0)
        self.at("the separate")
        self.play(FadeIn(tar, scale=0.9), FadeIn(lt), run_time=1.2)
        self.at("target gene")
        self.play(FadeIn(q, scale=0.6), run_time=0.8)
        self.at("was deleted")
        self.play(Indicate(q, scale_factor=1.3, color=TEXT), run_time=0.9)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        motes(self, seed=29)
        cell, rep, tar, lr, lt, q = predict_frame(self)
        self.add(cell, rep, tar, lr, lt, q)
        ring = Circle(radius=0.62).set_stroke(TEXT, 5).move_to(q).rotate(PI / 2)
        self.play(Create(ring), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


# ====================================================================== S10 reveal
class S10Reveal(SpokenScene):
    def construct(self):
        motes(self, seed=30)
        cell, rep, tar, lr, lt, q = predict_frame(self)
        self.add(cell, rep, tar, lr, lt, q)
        self.play(FadeOut(q, scale=0.5), cell.animate.set_stroke(GREEN, 3), run_time=1.0)
        self.at("the reporter and")
        self.play(Indicate(rep.bar, scale_factor=1.08, color=GREEN), run_time=1.0)
        self.at("separate")
        div = DashedLine([0, 2.6, 0], [0, -2.6, 0], dash_length=0.18).set_stroke(GREY, 4)
        self.play(Create(div), Indicate(tar.bar, scale_factor=1.08, color=RED), run_time=1.2)
        self.at("recombine differently")
        self.play(FadeOut(lr), FadeOut(lt), run_time=0.4)
        tok = chip("Cre", RED, 26).move_to([-1.9, 1.9, 0])
        tok2 = chip("Cre", RED, 26).move_to([1.9, 1.9, 0])
        self.play(FadeIn(tok), FadeIn(tok2), run_time=0.5)
        self.play(tok.animate.move_to(rep.block.get_center() + UP * 0.05), tok2.animate.move_to(tar.block.get_center() + UP * 0.05), run_time=1.0)
        lamp = Circle(radius=0.5).set_stroke(GREEN, 5).set_fill(GREEN, 0.15).move_to([-1.9, 2.3, 0])
        self.play(rep.block.animate.set_fill(GREEN, 1.0), lamp.animate.set_fill(GREEN, 0.9), FadeOut(tok), FadeOut(tok2), run_time=0.9)
        shimmer(lamp, 2.4, 0.5, 0.95)
        tq = qmark([1.9, 1.55, 0], 44, TEXT)
        self.add(tq)
        self.at("old target")
        prot = Rectangle(width=1.4, height=0.5).set_stroke(RED, 3).set_fill(RED, 0.5).move_to([1.9, -1.5, 0])
        pl = T("old protein", 28, RED).move_to([1.9, -2.2, 0])
        self.play(FadeOut(tq), FadeIn(prot, shift=UP * 0.3), FadeIn(pl), run_time=1.2)
        self.at("persist")
        ghost = DashedVMobject(Rectangle(width=0.9, height=0.6), num_dashes=16).set_stroke(RED, 3).move_to(tar.block)
        self.play(FadeOut(tar.block), FadeIn(ghost), Indicate(prot, scale_factor=1.12, color=RED), run_time=1.4)
        self.at("reporter light")
        ll = T("reporter recombined", 28, GREEN).move_to([-1.9, 3.55, 0])
        self.play(FadeIn(ll), Indicate(lamp, scale_factor=1.3, color=GREEN), run_time=1.2)
        self.at("measure")
        self.play(FadeOut(ll), FadeOut(pl), run_time=0.4)
        circ = Circle(radius=0.35).set_stroke(BLUE, 6)
        hand = Line(circ.get_bottom() + RIGHT * 0.25, circ.get_bottom() + RIGHT * 0.7 + DOWN * 0.6).set_stroke(BLUE, 8)
        mag = VGroup(circ, hand).move_to([3.9, -0.4, 0])
        self.play(FadeIn(mag), run_time=0.5)
        self.play(mag.animate.move_to([2.4, -1.5, 0]), run_time=1.0)
        tl = T("target protein", 30, BLUE).move_to([1.9, -2.3, 0])
        self.play(FadeIn(tl), Indicate(prot, scale_factor=1.15, color=BLUE), run_time=1.0)
        self.finish()


# ====================================================================== S11 inference
class S11Inference(SpokenScene):
    def construct(self):
        motes(self, seed=31)
        y1, y2 = 1.7, -1.5
        xs = (-5.2, -2.2, 1.6)
        h1 = T("Remove a gene: necessary?", 30, RED).move_to([-6.5, y1 + 1.1, 0], aligned_edge=LEFT)
        h2 = T("Impose activity: sufficient?", 30, RED).move_to([-6.5, y2 + 1.1, 0], aligned_edge=LEFT)
        gene = chip("gene", RED, 28).move_to([xs[0], y1, 0])
        act = chip("actuator", RED, 28).move_to([xs[0], y2, 0])
        c1 = Circle(radius=0.6).set_stroke(GREY, 4).set_fill(GREY, 0.3).move_to([xs[1], y1, 0])
        c2 = Circle(radius=0.6).set_stroke(GREY, 4).set_fill(GREY, 0.3).move_to([xs[1], y2, 0])
        tr1, tr2 = ValueTracker(0.85), ValueTracker(0.2)
        g1 = gauge(xs[2] + 0.3, y1, tr1, w=3.0, h=0.8)
        g2 = gauge(xs[2] + 0.3, y2, tr2, w=3.0, h=0.8)
        ar = lambda a, b, y: Arrow([a, y, 0], [b, y, 0], buff=0, stroke_width=6, color=TEXT, max_tip_length_to_length_ratio=0.3)
        self.at("interpret")
        self.play(FadeIn(gene, shift=RIGHT * 0.2), FadeIn(c1), FadeIn(g1), Create(ar(-4.1, -3.0, y1)), Create(ar(-1.4, -0.1, y1)), run_time=1.5)
        self.at("outcome")
        self.play(Indicate(g1, scale_factor=1.1, color=BLUE), run_time=1.0)
        self.at("removing a gene")
        self.play(FadeIn(h1), run_time=0.8)
        self.at("necessary")
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=gene.width, height=gene.height), num_dashes=20).set_stroke(RED, 3).move_to(gene)
        self.play(FadeOut(gene, shift=UP * 0.3), FadeIn(ghost), tr1.animate.set_value(0.3), run_time=2.0)
        self.at("imposing activity")
        self.play(FadeIn(h2), FadeIn(act, shift=RIGHT * 0.2), FadeIn(c2), FadeIn(g2), Create(ar(-3.9, -3.0, y2)), Create(ar(-1.4, -0.1, y2)), run_time=1.6)
        self.at("actuator")
        self.play(Indicate(act, scale_factor=1.15, color=RED), c2.animate.set_fill(RED, 0.6).set_stroke(RED, 4), run_time=1.2)
        self.at("sufficient")
        self.play(tr2.animate.set_value(0.8), run_time=1.6)
        self.at("a reporter")
        lamp = Circle(radius=0.5).set_stroke(GREEN, 5).set_fill(GREEN, 0.3).move_to([5.6, 0.1, 0])
        ll = T("reporter", 28, GREEN).move_to([5.6, -0.7, 0])
        self.play(FadeIn(lamp), FadeIn(ll), run_time=0.8)
        shimmer(lamp, 2.4, 0.3, 0.95)
        self.at("observes")
        self.play(Indicate(lamp, scale_factor=1.3, color=GREEN), run_time=1.0)
        self.at("does not impose")
        s1 = DashedLine([5.0, 0.3, 0], [4.1, 1.2, 0], dash_length=0.12).set_stroke(GREEN, 4)
        s2 = DashedLine([5.0, -0.1, 0], [4.1, -1.0, 0], dash_length=0.12).set_stroke(GREEN, 4)
        self.play(Create(s1), Create(s2), run_time=1.0)
        self.wait(1.0)
        self.finish()


# ====================================================================== S12 rule
class S12Rule(SpokenScene):
    def construct(self):
        motes(self, seed=32)
        names = [("genotype", GREY), ("perturbation", RED), ("readout", BLUE), ("claim", TEXT)]
        xs = [-5.025, -1.675, 1.675, 5.025]
        y = 0.9
        py = 2.75
        rail = Line([xs[0], py, 0], [xs[3], py, 0]).set_stroke(GREY, 3)
        self.add(rail)
        blocks = []
        for (nm, col), x in zip(names, xs):
            b = RoundedRectangle(corner_radius=0.2, width=2.9, height=2.8).set_stroke(col, 5).set_fill(col, 0.14).move_to([x, y, 0])
            lab = T(nm, 30, col).move_to(b)
            g = VGroup(b, lab)
            g.b = b
            blocks.append(g)
        self.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in blocks], lag_ratio=0.3), run_time=2.4)
        for i, g in enumerate(blocks):
            bob(g, 0.04, 2.8, i)
        links = [Arrow([xs[i] + 1.5, y, 0], [xs[i + 1] - 1.5, y, 0], buff=0, stroke_width=8, color=TEXT,
                       max_tip_length_to_length_ratio=0.7, max_stroke_width_to_length_ratio=30) for i in range(3)]
        self.add(*links)
        self.at("match")
        pulse = Dot(radius=0.2, color=TEXT).move_to([xs[0], py, 0])
        self.play(FadeIn(pulse), Indicate(blocks[0], scale_factor=1.06, color=GREY), run_time=1.0)
        self.at("perturbation")
        self.play(pulse.animate.move_to([xs[1], py, 0]), Indicate(blocks[1], scale_factor=1.06, color=RED), run_time=1.2)
        self.at("readout")
        self.play(pulse.animate.move_to([xs[2], py, 0]), Indicate(blocks[2], scale_factor=1.06, color=BLUE), run_time=1.2)
        self.at("claim")
        self.play(pulse.animate.move_to([xs[3], py, 0]), Indicate(blocks[3], scale_factor=1.06, color=TEXT), run_time=1.2)
        self.at("check every")
        braces = [Brace(b.b, DOWN, buff=0.15, color=GOLD if False else TEXT) for b in blocks]
        self.play(*[FadeIn(br, shift=UP * 0.2) for br in braces], pulse.animate.move_to([xs[0], py, 0]), run_time=1.4)
        lab = T("a control under every link", 30, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("one weak")
        self.play(links[1].animate.set_stroke(width=2).set_opacity(0.4), run_time=0.6)
        self.play(pulse.animate.move_to([xs[1] + 1.55, py, 0]), run_time=1.0)
        self.at("conclusion")
        self.play(blocks[3].animate.scale(0.75).set_opacity(0.45), Indicate(links[1], scale_factor=1.0, color=RED), run_time=1.4)
        self.finish()


# ====================================================================== S13 end
class S13End(EndCard):
    LINE = "Match genotype to perturbation to readout to claim, and control every link."
