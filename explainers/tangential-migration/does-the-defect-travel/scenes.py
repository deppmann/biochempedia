"""Tangential migration, chapter 2: Does the Defect Travel with the Cell?

COLOR MAP (one color per concept, shared by every chapter of this film)
  ORANGE = inhibitory interneuron (the travelling cell)
  BLUE   = excitatory pyramidal neuron and its dividing progenitors
  YELLOW = a label that marks cells: dye, genetic reporter, graft label
  RED    = mutant / knockout / missing
  TEXT   = normal tissue (pale outline)
  GREY   = tissue: cortex, eminences, slices
  GREEN  = result tick
  TEAL / PURPLE = chemokine and its receptor (reserved for chapter 3)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0.12, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

# ---------------------------------------------------------------- shapes
def cell(color=ORANGE, r=0.2, stroke=None, sw=2, op=0.9):
    return Circle(radius=r, stroke_color=stroke or color, stroke_width=sw, fill_color=color, fill_opacity=op)


def tri(color=BLUE, s=0.24):
    return Triangle(stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).scale(s)


def ghost(r=0.2):
    return DashedVMobject(Circle(radius=r, color=RED, stroke_width=2.5), num_dashes=10)


def tick(s=0.4, c=GREEN):
    return VGroup(Line([-s * .8, 0, 0], [-s * .25, -s * .6, 0], color=c, stroke_width=10),
                  Line([-s * .25, -s * .6, 0], [s * .9, s * .7, 0], color=c, stroke_width=10))


def crossx(s=0.4, c=RED):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=c, stroke_width=10),
                  Line([-s, s, 0], [s, -s, 0], color=c, stroke_width=10))


def qmark(size=90, color=TEXT):
    return T("?", size, color, weight=BOLD)


def tag(text, color=TEXT):
    t = T(text, 30, color, weight=BOLD)
    return t.move_to([-6.6 + t.width / 2, 3.45, 0])


def tint(kind):
    return TEXT if kind == "normal" else RED


# ---------------------------------------------------------------- forebrain schematic
CX0, CX1, CY0, CY1 = -2.0, 6.4, -3.0, 3.2
LAT_C = np.array([-4.1, -0.5, 0])
MED_C = np.array([-4.9, -2.6, 0])


def cortex_rect(x0=CX0, x1=CX1, y0=CY0, y1=CY1):
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=GREY, stroke_width=3,
                     fill_color=GREY, fill_opacity=0.10).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def blob(c, w=3.2, h=2.2):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.22).move_to(c)


def forebrain():
    g = VGroup(cortex_rect(), blob(LAT_C), blob(MED_C))
    g.cx, g.lat, g.med = g[0], g[1], g[2]
    return g


def lab(text, pos, size=28, color=TEXT):
    return T(text, max(28, size), color).move_to(pos)


# ---------------------------------------------------------------- icons for the three methods
def icon_eye():
    return VGroup(Ellipse(width=2.2, height=1.1, stroke_color=TEXT, stroke_width=6),
                  Circle(radius=0.38, stroke_color=TEXT, stroke_width=5),
                  Dot(radius=0.16, color=TEXT))


def icon_scissors():
    return VGroup(Line([-0.8, -0.5, 0], [1.0, 0.4, 0], color=TEXT, stroke_width=7),
                  Line([-0.8, 0.5, 0], [1.0, -0.4, 0], color=TEXT, stroke_width=7),
                  Circle(radius=0.28, stroke_color=TEXT, stroke_width=5).move_to([-1.05, -0.62, 0]),
                  Circle(radius=0.28, stroke_color=TEXT, stroke_width=5).move_to([-1.05, 0.62, 0]))


def icon_swap():
    return VGroup(Arrow([-1.0, 0.38, 0], [1.0, 0.38, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.3),
                  Arrow([1.0, -0.38, 0], [-1.0, -0.38, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.3))


TILE_X = (-4.3, 0.0, 4.3)


def tiles():
    out = []
    for x, f in zip(TILE_X, (icon_eye, icon_scissors, icon_swap)):
        box = RoundedRectangle(corner_radius=0.2, width=3.8, height=4.6, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([x, 0, 0])
        ic = f().move_to([x, 0.7, 0])
        out.append(VGroup(box, ic))
    return out


# ---------------------------------------------------------------- the donor / host grid
X_DON, X_HOST, X_RES = -4.6, 0.7, 5.1
ROWS = [1.25, -1.55]
KIND = [("normal", "mutant"), ("mutant", "normal")]
DOT_OFF = [(-0.3, 0.05), (-0.1, 0.2), (0.1, -0.1), (0.25, 0.1), (0.0, 0.0)]
DOT_END = [(0.5, 0.35), (1.0, -0.1), (1.5, 0.3), (1.9, -0.2), (0.9, 0.55)]


def graft_pos(i):
    return np.array([X_HOST - 1.3, ROWS[i] - 0.4, 0])


class Row:
    """One row of the graft grid. stage 0: piece waiting; 1: piece placed in host; 2: result in."""

    def __init__(self, i, stage=0, q=True):
        y = ROWS[i]
        dk, hk = KIND[i]
        self.i, self.y, self.dk, self.hk = i, y, dk, hk
        self.donor = Ellipse(width=1.4, height=1.0, stroke_color=YELLOW if dk == "normal" else RED, stroke_width=4, fill_color=tint(dk),
                             fill_opacity=0.35 if dk == "normal" else 0.5).move_to([X_DON, y + 0.1, 0])
        self.dlab = T(f"{dk} piece", 28, tint(dk)).move_to([X_DON, y - 0.85, 0])
        self.arrow = Arrow([X_DON + 1.0, y + 0.1, 0], [X_HOST - 2.35, y + 0.1, 0], buff=0, color=GREY, stroke_width=4,
                           tip_length=0.2)
        self.host = Rectangle(width=4.8, height=2.4, stroke_color=tint(hk), stroke_width=3, fill_color=tint(hk),
                              fill_opacity=0.10).move_to([X_HOST, y, 0])
        hl = T(f"{hk} slice", 28, tint(hk))
        self.hlab = hl.move_to([X_HOST - 2.0 + 0.15 + hl.width / 2, y + 0.72, 0])
        self.blob = Ellipse(width=1.5, height=0.9, stroke_color=GREY, stroke_width=2, fill_color=tint(hk),
                            fill_opacity=0.2).move_to(graft_pos(i))
        self.clab = T("cortex", 28, TEXT).move_to([X_HOST + 1.5, y - 0.78, 0])
        self.dots = VGroup(*[cell(YELLOW if dk == "normal" else RED, 0.14, YELLOW, 3, 1) for _ in DOT_OFF])
        self.mark = None
        self.parts = [self.host, self.hlab, self.blob, self.clab, self.donor, self.dlab, self.arrow]
        gp = graft_pos(i)
        for d, o in zip(self.dots, DOT_OFF):
            d.move_to(gp + np.array([o[0], o[1], 0]))
        if stage >= 1:
            self.donor.scale(0.75).move_to(gp)
            self.parts.append(self.donor.copy().scale(1/.75).move_to([X_DON,y+.1,0]))
        if stage >= 2:
            if i == 0:
                for d, e in zip(self.dots, DOT_END):
                    d.move_to([X_HOST + e[0], y + e[1], 0])
            self.parts.append(self.dots)
            self.mark = result_mark(i)
            self.parts.append(self.mark)
        elif q:
            self.mark = qmark().move_to([X_RES, y, 0])
            self.parts.append(self.mark)
        self.group = VGroup(*self.parts)


def result_mark(i):
    symbol = tick(.3) if i == 0 else crossx(.3)
    text = T("migrated" if i == 0 else "stayed\nno migration", 26, GREEN if i == 0 else RED)
    return VGroup(symbol, text).arrange(DOWN, buff=.25).move_to([X_RES, ROWS[i], 0])


def grid_headers(result=True):
    hs = [T("donor", 28, TEXT).move_to([X_DON, 3.2, 0]), T("host", 28, TEXT).move_to([X_HOST, 3.2, 0])]
    if result:
        hs.append(T("result", 28, TEXT).move_to([X_RES, 3.2, 0]))
    hs.extend([tag("swap", GOLD),
               VGroup(cell(YELLOW,.14),T("normal donor cell",26,TEXT)).arrange(RIGHT,buff=.15).move_to([-3.3,-3.0,0]),
               VGroup(cell(RED,.14,YELLOW,3),T("mutant donor cell",26,TEXT)).arrange(RIGHT,buff=.15).move_to([3.2,-3.0,0])])
    return VGroup(*hs)


# ---------------------------------------------------------------- the normal / mutant cortex pair
PX = (-3.4, 3.4)
PY0, PY1 = -2.25, 2.6
O_POS = [(-2.0, 1.5), (-1.0, 0.8), (0.1, 1.5), (1.1, 0.7), (2.0, 1.4), (-1.6, 0.2), (0.2, 0.2), (2.1, 0.3)]
B_POS = [(-1.6, 1.0), (-0.5, 1.2), (0.9, 1.4), (1.5, 0.2), (-0.6, 0.2)]
SURV = (1, 6)


def at_(cx, d, y0=0.0):
    return [cx + d[0], d[1] + y0, 0]


class Panels:
    def __init__(self):
        self.legend = VGroup(
            VGroup(cell(ORANGE, 0.18), T("inhibitory", 28, ORANGE)).arrange(RIGHT, buff=0.2).move_to([-2.5, 3.5, 0]),
            VGroup(tri(BLUE, 0.22), T("pyramidal", 28, BLUE)).arrange(RIGHT, buff=0.2).move_to([2.5, 3.5, 0]))
        self.rect, self.blobs, self.hdr, self.tris, self.prog = [], [], [], [], []
        for k, cx in enumerate(PX):
            self.rect.append(Rectangle(width=5.7, height=PY1 - PY0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                       fill_opacity=0.10).move_to([cx, (PY0 + PY1) / 2, 0]))
            self.blobs.append(Ellipse(width=2.4, height=1.2, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                      fill_opacity=0.22).move_to([cx - 1.5, -2.95, 0]))
            self.hdr.append(T("normal" if k == 0 else "Dlx1/2 mutant", 28, TEXT if k == 0 else RED, weight=BOLD)
                            .move_to([cx, 2.95, 0]))
            self.tris.append(VGroup(*[tri().move_to(at_(cx, p)) for p in B_POS]))
            pr = VGroup()
            for dx in (-1.0, 0.0, 1.0):
                pr.add(VGroup(cell(BLUE, 0.18).move_to([cx + dx - 0.23, -1.7, 0]),
                              cell(BLUE, 0.18).move_to([cx + dx + 0.23, -1.7, 0])))
            self.prog.append(pr)
        self.norm_o = VGroup(*[cell().move_to(at_(PX[0], p)) for p in O_POS])
        self.mut_o = VGroup(*[cell().move_to(at_(PX[1], O_POS[i])) for i in SURV])
        self.ghosts = VGroup(*[ghost().move_to(at_(PX[1], p)) for i, p in enumerate(O_POS) if i not in SURV])
        self.cover = Rectangle(width=5.7, height=PY1 - PY0, stroke_color=GREY, stroke_width=3, fill_color=BG,
                               fill_opacity=0.96).move_to([PX[1], (PY0 + PY1) / 2, 0])
        self.q = qmark(130).move_to([PX[1], (PY0 + PY1) / 2, 0])
        self.neo = T("neocortex", 28, TEXT).move_to([PX[1], 2.2, 0])
        self.vf = T("ventral\nforebrain", 28, TEXT).move_to([PX[1]+1.7, -2.95, 0])
        self.arr = DashedLine([PX[1] - 1.5, -2.5, 0], [PX[1] - 1.3, -1.0, 0], color=GREY, stroke_width=4,
                              dash_length=0.12).add_tip(tip_length=0.2)
        self.xm = crossx(0.28).move_to([PX[1] - 1.4, -2.0, 0])
        self.few = T("few GABA cells", 28, ORANGE).move_to([PX[1]+.9, -1.15, 0])
        self.proglab = VGroup(*[T("dorsal progenitors", 28, BLUE).move_to([cx, -1.15, 0]) for cx in PX])

    def q_frame(self):
        return VGroup(self.legend, self.rect[0], self.blobs[0], self.hdr[0], self.norm_o, 
                      self.rect[1], self.blobs[1], self.hdr[1], self.cover, self.q)

    def reveal_frame(self, prog=False):
        g = VGroup(self.legend, self.rect[0], self.blobs[0], self.hdr[0], self.norm_o, 
                   self.rect[1], self.blobs[1], self.hdr[1], self.mut_o, self.ghosts, VGroup(ghost(), T("missing", 28, TEXT)).arrange(RIGHT).move_to([-2.0,-3.1,0]),
                   self.neo, self.vf, self.arr, self.xm, self.few)
        if prog:
            g.remove(self.few, self.xm, self.arr)
            g.add(self.tris[0], self.tris[1], self.prog[0], self.prog[1], self.proglab)
        return g


# =============================================================== scenes
class S00Title(TitleCard):
    LESSON = "Tangential Migration: Interneurons and the Long Way Round"
    TITLE = "Does the Defect Travel with the Cell?"

    def construct(self):
        title = T("Does the Defect Travel\nwith the Cell?", 52, TEXT, font=TITLE_FONT, line_spacing=1.2)
        lesson = T("Tangential migration · follow, remove, swap", 28, TEAL).move_to([0, 2.4, 0])
        rule = Line([-2, -1.8, 0], [2, -1.8, 0], color=GOLD, stroke_width=4)
        self.add(title, lesson, rule)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        box = cortex_rect(-6.2, 6.2, -2.8, 2.7)
        n = cell(ORANGE, 0.85).move_to([0, 0, 0])
        left = T("where from?", 38, TEXT).move_to([-3.7, 1.6, 0])
        right = T("what does it need?", 34, TEXT).move_to([3.2, 1.6, 0])
        self.add(box, n)
        self.at("where a neuron")
        arrow = Arrow([-2.5, 1.1, 0], [-0.9, 0.3, 0], color=TEXT, buff=0.1)
        self.play(FadeIn(left), GrowArrow(arrow), run_time=0.45)
        self.at("what it needs")
        self.play(FadeIn(right), run_time=0.35)
        self.at("three ways")
        methods = VGroup(*[f().scale(.55).move_to([x, -1.9, 0])
                           for x, f in zip((-3.8, 0, 3.8), (icon_eye, icon_scissors, icon_swap))])
        self.play(FadeIn(methods), run_time=0.35)
        self.finish()

class S02Three(SpokenScene):
    def construct(self):
        ts = tiles()
        self.add(*ts)
        names = ["follow", "remove", "swap"]
        labs = [T(nm, 40, TEXT, weight=BOLD).move_to([x, -1.5, 0]) for nm, x in zip(names, TILE_X)]
        self.at("follow")
        self.play(FadeIn(labs[0], shift=UP * 0.2), run_time=0.5)
        self.at("remove")
        self.play(FadeIn(labs[1], shift=UP * 0.2), run_time=0.5)
        self.at("swap")
        self.play(FadeIn(labs[2], shift=UP * 0.2), run_time=0.5)
        self.at("which one")
        self.play(Indicate(ts[2], color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.finish()


P0 = [(-4.8, -0.3), (-4.1, 0.05), (-3.5, -0.3), (-4.5, -0.55), (-3.7, -0.55)]
PE = [(-0.6, 1.4), (1.0, 0.6), (2.6, 1.3), (3.8, 0.0), (1.9, -0.7)]


class S03Follow(SpokenScene):
    def construct(self):
        fb = forebrain()
        self.add(lab("cortex", [2.4, 2.6, 0], 36), lab("medial\neminence", [-4.9, -2.6, 0], 32))
        self.play(FadeIn(fb), run_time=0.7)
        self.at("follow")
        tg = tag("follow")
        self.play(FadeIn(tg), run_time=0.4)
        self.at("in 1996")
        credit = VGroup(T("de Carlos, López-Mascaraque", 32, TEXT), T("and Valverde, 1996", 32, TEXT)).arrange(DOWN, buff=.15).move_to([2.2, -2.2, 0])
        self.play(FadeIn(credit), run_time=0.4)
        self.at("dye placed")
        patch = Circle(radius=0.55, stroke_width=0, fill_color=YELLOW, fill_opacity=0.5).move_to([-4.1, -0.1, 0])
        dyel = lab("dye", [-4.1, 1.1, 0], 24, YELLOW)
        self.play(FadeIn(patch, scale=0.4), FadeIn(dyel), run_time=0.6)
        self.at("lateral eminence")
        ll = lab("lateral\neminence", [-4.4, 2.0, 0], 32)
        self.play(FadeIn(ll), Indicate(fb.lat, color=GREY, scale_factor=1.05), run_time=0.7)
        self.at("cultured rat embryos")
        emb = lab("cultured rat embryo", [2.2, 3.55, 0])
        self.play(FadeIn(emb), run_time=0.4)
        self.at("marked cells")
        cells = VGroup(*[cell(YELLOW, 0.28, YELLOW, 4, 0.7).move_to([p[0], p[1], 0]) for p in P0])
        self.play(FadeIn(cells, scale=0.4), run_time=0.4)
        self.at("cells that")
        self.play(*[c.animate.move_to([e[0], e[1], 0]) for c, e in zip(cells, PE)], FadeOut(patch), FadeOut(dyel),
                  run_time=1.8)
        self.finish()


class S04Limit(SpokenScene):
    def construct(self):
        fb = forebrain()
        tg = tag("follow")
        ll = lab("lateral\neminence", [-4.4, 2.0, 0], 32)
        cells = VGroup(*[cell(YELLOW, 0.28, YELLOW, 4, 0.7).move_to([e[0], e[1], 0]) for e in PE])
        self.add(fb, tg, ll, cells, lab("cortex", [2.4, 2.6, 0], 36), lab("medial\neminence", [-4.9, -2.6, 0], 32))
        self.at("dye fades")
        self.play(*[c.animate.set_fill(GREY, opacity=.6).set_stroke(GREY, width=2, opacity=0.9) for c in cells], run_time=0.9)
        self.at("does not say")
        rl = T("route, not identity", 36, TEXT, weight=BOLD).move_to([2.4, -2.1, 0])
        self.play(FadeIn(rl, shift=UP * 0.15), run_time=0.5)
        self.at("what a cell becomes")
        qs = VGroup(*[qmark(30).move_to([e[0], e[1], 0]) for e in PE])
        self.play(FadeIn(qs, scale=0.5), run_time=0.5)
        self.finish()


BIG_C = np.array([0.8, -0.2, 0])
BIG_X = (-1.0, 1.1, 3.2)


def big_med():
    return blob([0, -0.5, 0], 8.4, 5.6)


def big_label():
    return lab("medial eminence", [0, -2.5, 0], 32)


def reporter_frame(off=False, daughters=False):
    gene = chip("Nkx2.1 off" if off else "Nkx2.1 on", GREY if off else TEXT, 36).move_to([-3.2, 2.4, 0])
    rep = chip("reporter on", YELLOW, 36).move_to([3.0, 2.4, 0])
    cells = VGroup(*[cell(YELLOW, .5, YELLOW, 4, 1).move_to([x, 0, 0]) for x in (-2.2, 0, 2.2)])
    if daughters:
        cells = VGroup(*[cell(YELLOW, .43, YELLOW, 4, 1).move_to([x, y, 0]) for x in (-2.4, 0, 2.4) for y in (-.6, .6)])
    pre = blob([5.1, -1.3, 0], 2.7, 2.3)
    pc = VGroup(*[cell(YELLOW, .32, YELLOW, 3, 1).move_to([x, -1.2, 0]) for x in (4.6, 5.6)])
    pl = lab("preoptic area", [5.1, -2.9, 0], 28)
    g = VGroup(big_med(), big_label(), gene, rep, cells, pre, pc, pl)
    if off:
        g.add(Line(gene.get_corner(UL), gene.get_corner(DR), color=RED, stroke_width=5))
    return g


class S05Cre(SpokenScene):
    def construct(self):
        full = reporter_frame()
        med, ml, gene, rep, cells, pre, pc, pl = full
        self.add(med, ml, pre, pl, tag("genetic label", YELLOW))
        cells.set_fill(GREY, opacity=.65).set_stroke(TEXT)
        pc.set_fill(GREY, opacity=.65).set_stroke(TEXT)
        self.at("cells that")
        self.play(FadeIn(cells), FadeIn(pc), run_time=.45)
        self.at("switch on")
        self.play(FadeIn(gene), run_time=.4)
        self.at("medial eminence")
        self.play(Indicate(med, color=TEXT, scale_factor=1.02), run_time=.5)
        self.at("turn on")
        self.play(cells.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW),
                  pc.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW), FadeIn(rep), run_time=.5)
        self.finish()


class S05bKeep(SpokenScene):
    def construct(self):
        g = reporter_frame()
        self.add(g)
        self.at("every descendant")
        new = reporter_frame(daughters=True)
        self.play(ReplacementTransform(g[4], new[4]), run_time=.7)
        self.at("keeps the reporter")
        self.play(Indicate(new[4], color=YELLOW, scale_factor=1.1), run_time=.45)
        self.at("gene turns off")
        off = reporter_frame(off=True, daughters=True)
        self.play(ReplacementTransform(g[2], off[2]), Create(off[-1]), run_time=.4)
        self.wait(2)
        self.finish()


class S06CreResult(SpokenScene):
    def construct(self):
        self.add(reporter_frame(off=True, daughters=True))
        self.at("mature mouse cortex")
        self.clear()
        wide = cortex_rect(-6.4, 6.4, -3.0, 2.7)
        cl = lab("mature mouse cortex", [0, 2.3, 0], 24)
        self.add(wide)
        self.play(FadeIn(cl), run_time=0.3)
        rnd = random.Random(11)
        pts = []
        while len(pts) < 13:
            p = (rnd.uniform(-5.7, 5.7), rnd.uniform(-2.5, 1.5))
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 1.3 for q in pts):
                pts.append(p)
        marked = VGroup(*[cell(YELLOW, 0.3, YELLOW, 4, 0.9).move_to([p[0], p[1], 0]) for p in pts])
        self.at("many marked cells")
        mk = chip("marked cell", YELLOW, 24).move_to([-3.2, 3.4, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in marked], lag_ratio=0.06), FadeIn(mk), run_time=1.0)
        self.at("inhibitory")
        ic = chip("inhibitory interneuron", ORANGE, 24).move_to([2.6, 3.4, 0])
        self.play(*[c.animate.set_fill(ORANGE, opacity=0.95) for i, c in enumerate(marked) if i % 13 not in (2, 5, 8, 11)],
                  FadeIn(ic), run_time=0.8)
        self.finish()


class S07Remove(SpokenScene):
    def construct(self):
        fb = forebrain()
        dish = lab("culture dish", [2.2, 1.8, 0], 36)
        cr = VGroup(T("Anderson, Eisenstat, Shi", 32, TEXT), T("and Rubenstein, 1997", 32, TEXT)).arrange(DOWN).move_to([2.2, 0, 0])
        vf = lab("ventral\nforebrain", [-4.5, 2.2, 0], 34)
        self.add(fb, dish, vf, lab("cortex", [2.4, 2.6, 0], 36),
                 lab("lateral\neminence", [-4.1, -.5, 0], 32),
                 lab("medial\neminence", [-4.9, -2.6, 0], 32))
        self.at("remove")
        self.play(FadeIn(tag("remove")), run_time=.3)
        self.at("in 1997")
        self.play(FadeIn(cr), run_time=.4)
        self.at("cut mouse cortex", lead=0)
        blade = Polygon([-2.6, 2.3, 0], [-2.1, 2.7, 0], [-2.1, 1.1, 0], [-2.6, .5, 0], color=TEXT, fill_opacity=.9)
        cut = DashedLine([-2.35, 2.6, 0], [-2.35, -2.9, 0], color=RED, stroke_width=5)
        cut_label = lab("cut", [-3.25, 1.0, 0], 34, RED)
        self.play(FadeIn(blade), FadeIn(cut_label), Create(cut), FadeOut(cr), run_time=.5)
        self.at("away from")
        self.play(fb.cx.animate.shift(RIGHT*.3), FadeOut(blade), FadeOut(cut_label), run_time=.45)
        self.at("ventral forebrain")
        self.play(Indicate(vf, color=TEXT, scale_factor=1.05), run_time=.4)
        self.finish()


DOTS8 = [(-0.8, 1.9), (0.6, 0.9), (1.9, 2.0), (3.2, 1.0), (4.5, 1.9), (5.6, 0.6), (0.2, -0.6), (2.0, -0.7), (3.8, -0.4),
         (5.2, -1.4)]
KEEP = (1, 5, 8)


class S08Cut(SpokenScene):
    def construct(self):
        cx = cortex_rect().shift(RIGHT * 0.3)
        em = VGroup(blob(LAT_C + LEFT * 0.3), blob(MED_C + LEFT * 0.3))
        bl = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([-2.95, -0.5, 0])
        br = Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([-1.85, -0.5, 0])
        tg = tag("remove")
        cl = lab("cortex", [5.7, 2.75, 0], 24)
        self.add(cx, em, bl, br, tg, cl,
                 lab("ventral forebrain", [-4.3, 2.5, 0]),
                 lab("lateral eminence", [-4.4, -.5, 0]), lab("medial\neminence", [-4.9, -2.6, 0], 32),
                 VGroup(cell(ORANGE), T("GABA cell", 28, ORANGE)).arrange(RIGHT).move_to([.1, 3.55, 0]),
                 VGroup(ghost(), T("missing", 28, TEXT)).arrange(RIGHT).move_to([4.4, 3.55, 0]))
        self.at("isolated")
        self.play(em.animate.set_opacity(0.3), bl.animate.set_opacity(0.3), Indicate(cx, color=GREY, scale_factor=1.02),
                  run_time=0.6)
        self.at("ended up")
        dots = VGroup(*[cell(ORANGE, 0.2).move_to([p[0] + 0.3, p[1], 0]) for p in DOTS8])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.05), run_time=0.7)
        self.at("fewer cells")
        gh = VGroup(*[ghost().move_to(d) for i, d in enumerate(dots) if i not in KEEP])
        gone = VGroup(*[d for i, d in enumerate(dots) if i not in KEEP])
        self.play(FadeOut(gone), FadeIn(gh), run_time=0.7)
        self.at("GABA")
        gl = T("cells containing GABA", 32, ORANGE, weight=BOLD).move_to([2.7, -2.5, 0])
        self.play(FadeIn(gl), run_time=0.5)
        self.finish()


class S09Ko(SpokenScene):
    def construct(self):
        title = T("knockout", 60, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.add(title)
        self.at("knockout")
        self.play(Indicate(title, scale_factor=1.02), run_time=0.4)
        self.at("a mouse with")
        xs, ys = (-4.95, -1.65, 1.65, 4.95), (0.8, -1.8)
        cells = VGroup()
        bars = VGroup()
        for y in ys:
            for x in xs:
                cells.add(Circle(radius=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15)
                          .move_to([x, y, 0]))
                bars.add(RoundedRectangle(corner_radius=0.08, width=0.9, height=0.24, stroke_color=TEXT, stroke_width=2,
                                          fill_color=TEXT, fill_opacity=0.8).move_to([x, y + 0.1, 0]))
        gl = T("gene", 28, TEXT).move_to([xs[0], ys[0] - 0.3, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.06), FadeIn(bars), FadeIn(gl),
                  run_time=1.0)
        self.at("disrupted")
        xmarks = [crossx(0.3).move_to([b.get_center()[0], b.get_center()[1], 0]) for b in bars]
        self.play(Create(xmarks[0]), run_time=0.4)
        self.at("in every cell")
        txt = T("a gene disrupted in every cell", 32, RED, weight=BOLD).move_to([0, -3.4, 0])
        self.play(LaggedStart(*[Create(m) for m in xmarks[1:]], lag_ratio=0.1), FadeIn(txt), run_time=1.0)
        self.finish()


class S10Dlx(SpokenScene):
    def construct(self):
        sub = blob([0, -.3, 0], 12.2, 6.2)
        title = T("subpallium", 42, TEXT, weight=BOLD).move_to([0, -2.7, 0])
        c1 = chip("Dlx1", TEXT, 50).move_to([-2.8, 1.4, 0])
        c2 = chip("Dlx2", TEXT, 50).move_to([2.8, 1.4, 0])
        tf = chip("transcription factors", TEXT, 38).move_to([0, -.9, 0])
        arrows = VGroup(*[Arrow(c.get_bottom(), tf.get_top()+RIGHT*x, color=TEXT, buff=.15) for c,x in ((c1,-.8),(c2,.8))])
        self.add(sub, title, c1, c2)
        self.at("both")
        self.play(Indicate(VGroup(c1,c2), color=YELLOW, scale_factor=1.08), run_time=.5)
        self.at("encode", lead=.25)
        self.play(FadeIn(tf), Create(arrows), run_time=.4)
        self.at("made in")
        self.play(Indicate(title, scale_factor=1.05), run_time=.4)
        self.at("subpallium")
        xs = VGroup(*[Line(c.get_corner(UL),c.get_corner(DR),color=RED,stroke_width=7) for c in (c1,c2)])
        self.play(FadeOut(arrows), tf.animate.set_opacity(.25), run_time=.2)
        self.play(FadeIn(xs), run_time=.25)
        self.finish()

class S11Q(SpokenScene):
    def construct(self):
        p = Panels()
        self.play(FadeIn(VGroup(p.legend, p.rect[0], p.blobs[0], p.hdr[0], p.norm_o)), run_time=0.4)
        self.at("mutant cortex")
        self.play(FadeIn(VGroup(p.rect[1], p.blobs[1], p.hdr[1])), run_time=0.6)
        self.at("which neurons")
        self.play(FadeIn(p.cover), FadeIn(p.q, scale=0.6), run_time=0.6)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(Panels().q_frame(), T("pause: predict", 40, YELLOW, weight=BOLD).move_to([-1.5,-3.25,0]))
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        p = Panels()
        self.add(p.q_frame())
        self.at("inhibitory ones")
        missing = VGroup(ghost(), T("missing", 28, TEXT)).arrange(RIGHT).move_to([-2.0,-3.1,0])
        self.play(FadeOut(p.cover), FadeOut(p.q), FadeIn(p.mut_o), FadeIn(p.ghosts), FadeIn(missing), run_time=0.8)
        self.play(Indicate(p.legend[0], color=ORANGE, scale_factor=1.2), run_time=0.6)
        self.at("No migration")
        self.play(Create(p.arr), run_time=0.6)
        self.at("ventral forebrain")
        self.play(FadeIn(p.vf), run_time=0.4)
        self.at("into the neocortex")
        self.play(FadeIn(p.neo), run_time=0.4)
        self.at("detected")
        self.play(Create(p.xm), run_time=0.5)
        self.at("few cells")
        self.play(FadeIn(p.few), Indicate(p.mut_o, color=ORANGE, scale_factor=1.4), run_time=0.8)
        self.finish()


class S14Pyr(SpokenScene):
    def construct(self):
        p = Panels()
        self.add(p.reveal_frame())
        self.remove(p.few, p.xm, p.arr)
        self.at("pyramidal neurons")
        self.add(p.tris[0], p.tris[1])
        self.play(Indicate(p.tris[0], color=BLUE, scale_factor=1.3), Indicate(p.tris[1], color=BLUE, scale_factor=1.3),
                  Indicate(p.legend[1], color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("their progenitors", lead=0)
        self.play(FadeIn(p.prog[0], scale=0.5), FadeIn(p.prog[1], scale=0.5), FadeIn(p.proglab), run_time=0.8)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        self.add(Panels().reveal_frame(prog=True))
        self.finish()


class S16Doubt(SpokenScene):
    def construct(self):
        road = RoundedRectangle(width=12.4,height=5.5,corner_radius=.3,stroke_color=GREY,fill_color=GREY,fill_opacity=.18).move_to([0,-.2,0])
        line = DashedLine([-5.8,-.4,0],[5.8,-.4,0],color=GREY)
        dot = cell(ORANGE,1).move_to([-2.7,-.3,0])
        self.add(road,line,dot,lab("travelling cell",[-2.7,-2.3,0],32),lab("tissue (the road)",[3,-2.3,0],32))
        self.at("lacks the genes")
        self.play(road.animate.set_stroke(RED,width=5),dot.animate.set_stroke(RED,width=6),
                  FadeIn(chip("mutant cell",RED,28).move_to([-3.1,3.2,0])),
                  FadeIn(chip("mutant tissue",RED,28).move_to([3.1,3.2,0])),run_time=.5)
        self.at("in the travelers",lead=0)
        self.play(FadeIn(qmark(90).move_to([-2.7,1.6,0])),run_time=.3)
        self.at("or in the road",lead=0)
        self.play(FadeIn(qmark(90).move_to([3,1.6,0])),run_time=.3)
        self.finish()

class S17Swap(SpokenScene):
    def construct(self):
        tg = tag("swap")
        self.add(tg)
        yr = T("2001", 100, TEXT, font=TITLE_FONT).move_to([0, 1.9, 0])
        self.add(yr, icon_swap().scale(1.6).move_to([0,-.3,0]))
        self.at("2001")
        self.play(Indicate(yr, scale_factor=1.02), run_time=.4)
        self.at("same group")
        cr = T("Anderson, Marín, Horn, Jennings and Rubenstein, 2001", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(cr), run_time=0.4)
        self.at("answered with")
        sw = icon_swap().scale(1.6).move_to([0, -0.3, 0])
        gl = T("grafts", 56, TEXT, font=TITLE_FONT).move_to([0, -1.9, 0])
        self.play(FadeIn(gl), run_time=0.6)
        self.finish()


class S18Graft(SpokenScene):
    def construct(self):
        tg = tag("swap")
        sl = Rectangle(width=11.8, height=5.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=0.10).move_to([0, -0.5, 0])
        eb = blob([-2.6, -1.6, 0], 2.8, 1.8)
        self.add(tg, sl, eb, lab("forebrain slice",[2.5,1.7,0],32))
        self.at("pieces")
        piece = Ellipse(width=1.2, height=0.8, stroke_color=YELLOW, stroke_width=4, fill_color=GREY,
                        fill_opacity=0.5).move_to([-2.6, 2.9, 0])
        pl = T("labelled piece", 28, YELLOW).move_to([-0.35, 2.9, 0])
        self.play(FadeIn(piece, scale=0.5), FadeIn(pl), run_time=0.5)
        self.at("into")
        self.play(piece.animate.move_to([-2.6, -1.6, 0]), FadeOut(pl), run_time=0.8)
        self.at("slices")
        sll = lab("forebrain slice", [2.5, 1.7, 0], 32)
        self.play(FadeIn(sll), run_time=0.4)
        self.at("crossing")
        hd = grid_headers(result=False)
        self.clear()
        self.play(FadeIn(hd), run_time=0.3)
        self.at("normal")
        r1 = Row(0, 0, q=False)
        self.play(FadeIn(r1.group), run_time=0.5)
        self.at("mutant tissue")
        r2 = Row(1, 0, q=False)
        self.play(FadeIn(r2.group), run_time=0.5)
        self.at("both ways")
        self.play(Indicate(r1.arrow, color=YELLOW), Indicate(r2.arrow, color=YELLOW), run_time=0.8)
        self.finish()


def q_grid():
    return VGroup(grid_headers(), Row(0, 0, True).group, Row(1, 0, True).group)


class S19Q(SpokenScene):
    def construct(self):
        hd = grid_headers(result=False)
        r1, r2 = Row(0, 0, q=False), Row(1, 0, q=False)
        self.add(hd, r1.group, r2.group)
        self.at("normal piece")
        self.play(Indicate(r1.donor, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.at("mutant slice")
        self.play(Indicate(r1.host, color=RED, scale_factor=1.04), run_time=0.6)
        self.at("mutant piece")
        self.play(Indicate(r2.donor, color=RED, scale_factor=1.2), run_time=0.6)
        self.at("normal slice")
        self.play(Indicate(r2.host, color=TEXT, scale_factor=1.04), run_time=0.6)
        self.at("which fails")
        rh = T("result", 28, TEXT).move_to([X_RES, 3.2, 0])
        q1, q2 = qmark().move_to([X_RES, ROWS[0], 0]), qmark().move_to([X_RES, ROWS[1], 0])
        self.play(FadeIn(rh), FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.6)
        self.finish()


class S20Pause(NarratedScene):
    def construct(self):
        self.add(q_grid(), T("pause: predict", 32, YELLOW).move_to([0,-3.65,0]))
        self.finish()


class S21R1(SpokenScene):
    def construct(self):
        hd = grid_headers()
        r1, r2 = Row(0, 0, True), Row(1, 0, True)
        self.add(hd, r1.group, r2.group)
        self.add(r1.donor.copy())
        self.play(r1.donor.animate.scale(0.75).move_to(graft_pos(0)), run_time=0.9)
        self.at("migrated")
        self.add(r1.dots)
        self.play(*[d.animate.move_to([X_HOST + e[0], ROWS[0] + e[1], 0]) for d, e in zip(r1.dots, DOT_END)],
                  run_time=1.5)
        self.at("of mutant slices")
        t = result_mark(0)
        self.play(ReplacementTransform(r1.mark, t), run_time=0.5)
        self.finish()


class S22R2(SpokenScene):
    def construct(self):
        hd = grid_headers()
        r1, r2 = Row(0, 2), Row(1, 0, True)
        self.add(hd, r1.group, r2.group)
        self.add(r2.donor.copy())
        self.play(r2.donor.animate.scale(0.75).move_to(graft_pos(1)), run_time=0.8)
        self.at("failed to")
        self.add(r2.dots)
        gp = graft_pos(1)
        self.play(FadeIn(r2.dots, scale=0.5), run_time=0.4)
        self.at("migrate")
        self.play(*[d.animate.shift(RIGHT * 0.25 + UP * 0.1) for d in r2.dots], run_time=0.5)
        self.play(*[d.animate.shift(LEFT * 0.25 + DOWN * 0.1) for d in r2.dots], run_time=0.5)
        self.at("of normal slices")
        x = result_mark(1)
        self.play(ReplacementTransform(r2.mark, x), run_time=0.5)
        self.finish()


def final_grid():
    return VGroup(grid_headers(), Row(0, 2).group, Row(1, 2).group)


def caption():
    return T("The defect travelled with the cells.", 32, TEXT, weight=BOLD).move_to([0, -3.4, 0])


class S23Travel(SpokenScene):
    def construct(self):
        hd, r1, r2 = grid_headers(), Row(0, 2), Row(1, 2)
        self.add(hd, r1.group, r2.group)
        cp = caption()
        self.at("with the cells", lead=.3)
        self.play(FadeIn(cp), run_time=0.3)
        self.at("with the cells")
        self.play(Indicate(r2.dots, color=RED, scale_factor=1.6), run_time=0.9)
        self.finish()


class S24Beat(NarratedScene):
    def construct(self):
        self.add(final_grid(), caption())
        self.finish()


class S25Inside(SpokenScene):
    def construct(self):
        sl = Rectangle(width=11.8,height=6.1,stroke_color=GREY,fill_color=GREY,fill_opacity=.1).move_to([0,-.1,0])
        eb = blob([-3.8,-1.3,0],3,2)
        labels = VGroup(lab("forebrain slice",[0,2.35,0],32),lab("eminence",[-3.8,-2.7,0],28))
        dot = cell(ORANGE,.45,YELLOW,4).move_to([-3.8,-1.2,0])
        highlight = Rectangle(width=12.1,height=6.4,stroke_color=GOLD,stroke_width=6).move_to(sl)
        trip = DashedLine([-2.8,-.9,0],[4.3,.8,0],color=TEXT,stroke_width=3).add_tip()
        self.add(sl,eb,labels,dot)
        self.at("whatever")
        self.play(Create(highlight),run_time=.4)
        self.at("do for the trip")
        self.play(Create(trip),dot.animate.move_to([3,.6,0]),run_time=.9)
        self.at("they do it")
        ring = Circle(radius=.7,color=GOLD,stroke_width=6).move_to(dot)
        self.play(ReplacementTransform(highlight,ring),run_time=.35)
        self.at("inside",lead=0)
        self.play(FadeOut(VGroup(sl,eb,labels,trip)),VGroup(dot,ring).animate.scale(3.7).move_to([0,.3,0]),run_time=.6)
        dlx = chip("Dlx",TEXT,36).move_to([0,.3,0])
        self.play(FadeIn(dlx),FadeIn(lab("needed inside the cell",[0,-3.15,0],36)),run_time=.35)
        self.wait(2.2)
        self.finish()


class S26How(SpokenScene):
    def construct(self):
        cards = []
        for x, color, title, detail in ((-3.25,GREEN,"where the\nneed lies","answered"),(3.25,TEXT,"how the\ngenes act","open")):
            box = RoundedRectangle(width=5.9,height=6.1,corner_radius=.25,stroke_color=color,fill_color=color,fill_opacity=.08).move_to([x,0,0])
            label = T(title,40,TEXT,line_spacing=1.2).move_to([x,1.15,0])
            answer = T(detail,40,color).move_to([x,-.9,0])
            symbol = (tick(.5) if x<0 else qmark(80)).move_to([x,-2.1,0])
            cards.append(VGroup(box,label,answer,symbol))
        self.add(*cards)
        self.at("where the need")
        self.play(Indicate(cards[0],scale_factor=1.02),run_time=.4)
        self.at("how the genes")
        self.play(Indicate(cards[1],scale_factor=1.02),run_time=.4)
        self.finish()

class S27Take(SpokenScene):
    def construct(self):
        top = T("For Dlx, the swap gives a clear answer.",40,TEXT,font=TITLE_FONT).move_to([0,2.8,0])
        road = Arrow([-5.7,-.5,0],[5.7,-.5,0],buff=0,color=GREY,stroke_width=5)
        dot = cell(ORANGE,1).move_to([-4,-.5,0])
        defect = chip("defect",RED,36).move_to([-4,1.2,0])
        badge = chip("swap: where the need lies",GOLD,32).move_to([0,-2.8,0])
        self.add(top,road,dot,defect,badge)
        self.at("travels")
        self.play(dot.animate.move_to([3.8,-.5,0]),defect.animate.move_to([3.8,1.2,0]),run_time=1.3)
        self.finish()

class S28End(EndCard):
    LINE = "For Dlx, the defect travels with the cell."
