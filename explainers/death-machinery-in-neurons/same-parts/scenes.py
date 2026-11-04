"""The Same Parts in Us  (chapter 3 of "The Death Machinery in Neurons")

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, same as the other chapters)
  BLUE   = a living cell (the cell outline, the cell that is taken apart)
  RED    = the killers: CED-3 and the caspases (grey while inactive, red when lit)
  GREEN  = protective: CED-9 / Bcl-2 (the brake, the shield)
  ORANGE = pro-death BCL-2 family proteins (Bax, Bak, Bim, EGL-1); in the family lineup the effectors
           (Bax, Bak) and the BH3-only regulators (Bim, EGL-1) are told apart by drawing and by tags
  PURPLE = CED-4 / Apaf-1
  PINK   = cytochrome c
  GOLD   = credits (the year of a discovery) and the highlighted residue or domain (cysteine, aspartate, BH3)
  GREY   = inactive things, structure, labels, platform, mitochondrion outline
  TEAL   = the unknown (question marks)
  PROT   = (pale blue-grey) ordinary cellular proteins
  YELLOW = the survival signal (only on the closing idea card)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
PROT = "#A9B8D0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Sc(SpokenScene):
    def until(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    g.box, g.label = c[0], c[1]
    return g


def fchip(text, color, size, w, h=0.92):
    """a chip of a fixed width (so a table column is not ragged)"""
    label = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, box, label.move_to(box))
    g.box, g.label = box, label
    return g


def dim_chip(c, o=0.35):
    c.box.set_stroke(opacity=o).set_fill(opacity=0.16 * o)
    c.label.set_opacity(o)


def undim_chip(c):
    return [c.box.animate.set_stroke(opacity=1).set_fill(opacity=0.16), c.label.animate.set_opacity(1)]


def ML(text, size=26, color=TEXT, weight=NORMAL, buff=0.1):
    """multi-line text, every line centred"""
    return VGroup(*[T(l, size, color, weight=weight) for l in text.split("\n")]).arrange(DOWN, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def lab(text, size=26, color=GREY, **kw):
    return T(text, size, color, **kw)


def panel(cx, cy, w, h, header, size=28):
    frame = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                             stroke_opacity=0.55, fill_opacity=0)
    frame.move_to([cx, cy, 0])
    if not header:
        g = VGroup(frame)
        g.frame = frame
        return g
    head = lab(header, size, GREY, weight=BOLD).move_to([cx, cy + h / 2 - 0.45, 0])
    g = VGroup(frame, head)
    g.frame, g.head = frame, head
    return g


def shield(w=1.6, h=1.9, color=GREEN, fill=0.28):
    pts = [(-w / 2, h / 2), (w / 2, h / 2), (w / 2, h * 0.05), (0, -h / 2), (-w / 2, h * 0.05)]
    s = Polygon(*[np.array([x, y, 0.0]) for x, y in pts]).round_corners(0.22 * min(1.0, w / 1.6 + 0.2))
    s.set_stroke(color, 5).set_fill(color, fill)
    return s


def dashed_box(w, h, color=GREY, sw=3):
    return DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=sw),
                          num_dashes=max(26, int(2 * (w + h) * 3.2)))


def plain_cell(r=1.3, color=BLUE):
    body = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.28)
    nuc = Circle(radius=r * 0.32, stroke_width=0, fill_color=color, fill_opacity=0.55)
    return VGroup(body, nuc)


def failbar(text, size=34):
    t = lab(text, size, TEXT, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 0.8, height=t.height + 0.42, stroke_color=GOLD,
                           stroke_width=3, fill_color=BG, fill_opacity=0.96)
    return VGroup(box, t.move_to(box)).move_to([0, -3.15, 0])


def rolelab(text):
    return lab(text, 30, GREY, weight=BOLD).move_to([0, 3.45, 0])


# --- the caspase cartoon: a block with an active-site pocket and a lid -----------------------------
def caspase(s=1.0, color=RED, mode="id"):
    w, h = 1.6 * s, 1.3 * s
    nw, nd = 0.42 * s, 0.5 * s
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (nw, h / 2), (0, h / 2 - nd), (-nw, h / 2), (-w / 2, h / 2)]
    body = Polygon(*[np.array([x, y, 0.0]) for x, y in pts]).round_corners(0.14 * min(s, 1.3))
    lid = RoundedRectangle(corner_radius=0.05, width=2 * nw + 0.2 * s, height=0.15 * s + 0.04, stroke_width=0,
                           fill_color=GREY, fill_opacity=0.95).move_to([0, h / 2, 0])
    g = VGroup(body, lid)
    g.body, g.lid, g.s, g.w, g.h, g.nd, g.nw, g.ccol = body, lid, s, w, h, nd, nw, color
    g.lift = 0.5 * s
    if mode == "closed":
        body.set_stroke(GREY, 3).set_fill(GREY, 0.2)
    elif mode == "lit":
        body.set_stroke(color, 4).set_fill(color, 0.5)
        lid.shift(UP * g.lift).set_opacity(0)
    else:  # identity: coloured, not lit
        body.set_stroke(color, 3.5).set_fill(color, 0.22)
        lid.shift(UP * g.lift).set_opacity(0)
    return g


def put(g, x, y):
    return g.shift(np.array([x, y, 0.0]) - g.body.get_center())


def mv(g, x, y):
    return g.animate.shift(np.array([x, y, 0.0]) - g.body.get_center())


def scl(g, k, x, y):
    c0 = g.body.get_center()
    return g.animate.scale(k, about_point=c0).shift(np.array([x, y, 0.0]) - c0)


def c_close(g):
    return [g.body.animate.set_stroke(GREY, 3).set_fill(GREY, 0.2),
            g.lid.animate.shift(DOWN * g.lift).set_opacity(0.95)]


def c_light(g):
    return [g.body.animate.set_stroke(g.ccol, 4).set_fill(g.ccol, 0.5),
            g.lid.animate.shift(UP * g.lift).set_opacity(0)]


def notch_bottom(g):
    return g.body.get_center() + np.array([0, g.h / 2 - g.nd, 0])


def top_y(g):
    return g.body.get_center()[1] + g.h / 2


# --- gene strips (illustrative letters, not real sequences) ---------------------------------------
_rng = random.Random(11)
SEQS = ["".join(_rng.choice("ACGT") for _ in range(90)) for _ in range(4)]
WIN = 15
STRIP_X = -4.2
STRIP_SIZE = 30


def strip_static(i, y, k, color):
    return M(SEQS[i][k:k + WIN], STRIP_SIZE, color).move_to([STRIP_X, y, 0], aligned_edge=LEFT)


# --- the worm pathway (scene 1) ---------------------------------------------------------------------
WX = -3.6
SY = (2.5, 0.4, -2.0)  # releaser, brake, killers
KX = 1.5


def worm_set():
    egl = bchip("EGL-1", ORANGE, 42).move_to([WX, SY[0], 0])
    c9 = bchip("CED-9", GREEN, 42).move_to([WX, SY[1], 0])
    c4 = bchip("CED-4", PURPLE, 42).move_to([WX - KX, SY[2], 0])
    c3 = bchip("CED-3", RED, 42).move_to([WX + KX, SY[2], 0])
    b_e = inhib(egl.get_bottom() + DOWN * 0.04, c9.get_top() + UP * 0.02, ORANGE, 7)
    b_4 = inhib(c9.get_bottom() + LEFT * 0.5 + DOWN * 0.03, c4.get_top() + UP * 0.02, GREEN, 7)
    b_3 = inhib(c9.get_bottom() + RIGHT * 0.5 + DOWN * 0.03, c3.get_top() + UP * 0.02, GREEN, 7)
    hdr = lab("worm", 32, GREY, weight=BOLD).move_to([WX, 3.5, 0])
    roles = [lab("releases the brake", 28, TEXT).move_to([-0.1, SY[0], 0]),
             lab("brake", 28, TEXT).move_to([-0.1, SY[1], 0]),
             lab("killers", 28, TEXT).move_to([-0.1, SY[2], 0])]
    return dict(egl=egl, c9=c9, c4=c4, c3=c3, b_e=b_e, b_4=b_4, b_3=b_3, hdr=hdr, roles=roles)


def mammal_qs():
    boxes = []
    for x, y, w in ((-WX, SY[0], 2.6), (-WX, SY[1], 2.6), (-WX - KX, SY[2], 2.6), (-WX + KX, SY[2], 2.6)):
        d = dashed_box(w, 1.3, GREY)
        q = T("?", 52, TEAL, weight=BOLD)
        g = VGroup(d, q).move_to([x, y, 0])
        boxes.append(g)
    hdr = lab("mammal", 32, GREY, weight=BOLD).move_to([-WX, 3.5, 0])
    return boxes, hdr


STACK_Y = [2.45, 0.85, -0.75, -2.35]
STACK_X = -5.5
STACK_COL = [ORANGE, GREEN, PURPLE, RED]
STACK_NAME = ["EGL-1", "CED-9", "CED-4", "CED-3"]
QX = 5.0  # x of the mammal question boxes in scene 2


def stack_chips():
    return [bchip(n, c, 38).move_to([STACK_X, y, 0]) for n, c, y in zip(STACK_NAME, STACK_COL, STACK_Y)]


def s02_pieces():
    qs = [VGroup(dashed_box(2.4, 1.2, GREY), T("?", 52, TEAL, weight=BOLD)).move_to([QX, y, 0]) for y in STACK_Y]
    hdr = lab("worm gene sequences (illustrative letters)", 26, GREY).move_to([-1.4, 3.5, 0])
    big = arr([1.2, 0.05, 0], [3.2, 0.05, 0], GREY, 8, 0.32)
    cl = lab("cloned", 30, TEXT, weight=BOLD).move_to([2.2, 0.62, 0])
    return qs, hdr, big, cl


# --- the table ---------------------------------------------------------------------------------------
COLX = dict(role=-5.1, worm=-1.9, mam=0.9, fail=4.5)
CW = dict(worm=2.2, mam=2.4)
HEAD_Y = 3.45
ROWS = [
    ("killer", ("CED-3", RED), ("caspases", RED), "main worm caspase;\nmammals split roles"),
    ("activator of\nthe killer", ("CED-4", PURPLE), ("Apaf-1", PURPLE), "Apaf-1 needs\ncytochrome c"),
    ("brake", ("CED-9", GREEN), ("Bcl-2", GREEN), "guards the\nmitochondria instead"),
    ("releases\nthe brake", ("EGL-1", ORANGE), ("BH3-only", ORANGE), "only the BH3\ndomain matches"),
    ("gate in the\nouter membrane", None, ("Bax", ORANGE), "no worm counterpart"),
]
FH_OP = 0.7


def row_y(r):
    return 2.35 - 1.25 * r


def _head(t, x, color=GREY):
    m = lab(t, 28, color, weight=BOLD)
    return m.move_to([x, 0, 0]).align_to([0, HEAD_Y - 0.2, 0], DOWN)


def head_mobs():
    return VGroup(_head("role", COLX["role"]), _head("worm", COLX["worm"]), _head("mammal", COLX["mam"]))


def fail_head(op=1.0):
    m = _head("where the match fails", COLX["fail"], TEXT)
    m.set_opacity(op)
    return m


def row_mobs(r, fail_op=1.0):
    y = row_y(r)
    role, wk, (mn, mc), ftxt = ROWS[r]
    ro = ML(role, 26, GREY, buff=0.05).move_to([COLX["role"], y, 0])
    if wk is None:
        wo = VGroup(dashed_box(2.5, 1.0, GREY), ML("no clear\ncounterpart", 26, TEXT, buff=0.04)).move_to([COLX["worm"], y, 0])
    else:
        wo = fchip(wk[0], wk[1], 36, CW["worm"]).move_to([COLX["worm"], y, 0])
    mo = fchip(mn, mc, 36, CW["mam"]).move_to([COLX["mam"], y, 0])
    fo = ML(ftxt, 26, TEXT).move_to([COLX["fail"], y, 0]) if ftxt else VGroup()
    fo.set_opacity(fail_op)
    g = VGroup(ro, wo, mo, fo)
    g.role, g.worm, g.mam, g.fail = ro, wo, mo, fo
    return g


def slot_mob():
    d = dashed_box(8.6, 1.0, GREY)
    return d.move_to([(-6.7 + 2.1) / 2, row_y(4), 0])


def question_card():
    t = ML("Which mammalian part\nhas no clear counterpart\nin the worm?", 26, TEXT)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 0.6, height=t.height + 0.4, stroke_color=GOLD,
                           stroke_width=3, fill_color=BG, fill_opacity=0.95)
    return VGroup(box, t.move_to(box)).move_to([4.5, -0.8, 0])


def table_state(rows=4, bax=False, slot=False, question=False, fh=FH_OP, fails=0.0):
    """everything in the table as it stands; returns (list of mobs, dict of named pieces)"""
    parts = {"head": head_mobs(), "fh": fail_head(fh)}
    parts["rows"] = [row_mobs(r, fails) for r in range(rows + (1 if bax else 0))]
    if slot:
        parts["slot"] = slot_mob()
    if question:
        parts["q"] = question_card()
    flat = [parts["head"], parts["fh"], *parts["rows"]] + [parts[k] for k in ("slot", "q") if k in parts]
    return flat, parts


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The death machinery in neurons"
    TITLE = "The Same Parts in Us"


# ---------------------------------------------------------------------------------------------
class S01(Sc):
    """The worm pathway, drawn large down the left; the mammal side is a column of question marks."""

    def construct(self):
        w = worm_set()
        boxes, mhdr = mammal_qs()
        self.at("The worm")
        self.play(FadeIn(w["hdr"]), run_time=0.4)
        self.at("two killers")
        self.play(FadeIn(w["c4"], shift=UP * 0.15), FadeIn(w["c3"], shift=UP * 0.15), FadeIn(w["roles"][2]), run_time=0.6)
        self.at("break")
        self.play(FadeIn(w["c9"], shift=DOWN * 0.15), Create(w["b_4"]), Create(w["b_3"]), FadeIn(w["roles"][1]), run_time=0.7)
        self.at("protein that")
        self.play(FadeIn(w["egl"], shift=DOWN * 0.15), Create(w["b_e"]), FadeIn(w["roles"][0]), run_time=0.7)
        self.at("Does a mammal")
        self.play(FadeIn(mhdr), LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes], lag_ratio=0.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(Sc):
    """The worm stack, a gene strip scrolling beside each protein, and 'cloned' pointing at the mammal question."""

    def construct(self):
        w = worm_set()
        boxes, mhdr = mammal_qs()
        order = [w["egl"], w["c9"], w["c4"], w["c3"]]
        self.add(w["hdr"], *order, w["b_e"], w["b_4"], w["b_3"], *w["roles"], mhdr, *boxes)
        qs, hdr, big, cl = s02_pieces()
        gone = [w["b_e"], w["b_4"], w["b_3"], *w["roles"], mhdr, *boxes, w["hdr"]]
        moves = [m.animate.move_to([STACK_X, y, 0]) for m, y in zip(order, STACK_Y)]
        self.play(*[FadeOut(g) for g in gone], *moves, FadeIn(VGroup(*qs)), run_time=0.8)
        self.at("genes")
        tr = ValueTracker(0)
        strips = []
        for i, (y, col) in enumerate(zip(STACK_Y, STACK_COL)):
            s = always_redraw(lambda i=i, y=y, col=col: M(SEQS[i][int(tr.get_value()):int(tr.get_value()) + WIN], STRIP_SIZE, col)
                              .move_to([STRIP_X, y, 0], aligned_edge=LEFT))
            strips.append(s)
        self.add(*strips)
        self.play(FadeIn(hdr), tr.animate.set_value(24), run_time=1.0, rate_func=linear)
        self.at("answer")
        self.play(GrowArrow(big), FadeIn(cl), run_time=0.5)
        match = lab("match found", 26, GOLD, weight=BOLD).move_to([2.2, -0.55, 0])
        self.play(FadeIn(match, scale=1.1), run_time=0.25)
        self.play(FadeOut(match), run_time=0.25)
        self.finish()


def s02_end():
    chips = stack_chips()
    strips = [strip_static(i, y, 24, c) for i, (y, c) in enumerate(zip(STACK_Y, STACK_COL))]
    qs, hdr, big, cl = s02_pieces()
    return chips, strips, qs, hdr, big, cl


# ---------------------------------------------------------------------------------------------
def s03_objs():
    d = {}
    d["year"] = T("1993", 80, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
    d["pw"] = panel(-3.6, -0.5, 5.0, 4.9, "worm")
    d["pm"] = panel(3.6, -0.5, 5.0, 4.9, "mammal")
    d["c3"] = put(caspase(1.7, RED, "id"), -3.6, -0.15)
    d["c3l"] = bchip("CED-3", RED, 34).move_to([-3.6, -1.95, 0])
    d["mp"] = put(caspase(1.7, RED, "id"), 3.6, -0.15)
    d["mpl"] = lab("mammalian protease", 28, TEXT).move_to([3.6, -1.95, 0])
    d["link"] = DoubleArrow([-1.0, -0.15, 0], [1.0, -0.15, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
    d["rs"] = lab("resembles", 26, GREY).move_to([0, 0.4, 0])
    return d


class S03(Sc):
    """1993: CED-3 resembles a mammalian protease (two similar caspase cartoons side by side)."""

    def construct(self):
        chips, strips, qs, hdr, big, cl = s02_end()
        self.add(*chips, *strips, *qs, hdr, big, cl)
        d = s03_objs()
        self.at("In 1993")
        self.play(FadeOut(VGroup(*strips, *qs, hdr, big, cl)), FadeOut(chips[0]), FadeOut(chips[1]), FadeOut(chips[2]),
                  chips[3].animate.move_to([-3.6, -1.95, 0]), run_time=0.5)
        self.play(FadeIn(d["year"], shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(d["pw"]), FadeIn(d["c3"], scale=0.9), run_time=0.7)
        self.at("CED 3")
        self.play(Indicate(chips[3], color=RED, scale_factor=1.15), run_time=0.6)
        self.at("resemble")
        self.play(FadeIn(d["pm"]), GrowFromCenter(d["link"]), FadeIn(d["rs"]), run_time=0.7)
        self.at("mammalian protease")
        self.play(FadeIn(d["mp"], scale=0.9), FadeIn(d["mpl"]), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def fam_objs():
    ring = DashedVMobject(Ellipse(width=12.2, height=6.0, stroke_color=GREY, stroke_width=3), num_dashes=46).move_to([0, -0.5, 0])
    sib = [put(caspase(1.2, RED, "id"), *p) for p in ([-3.7, 0.5], [3.7, 0.5], [-2.6, -2.0], [2.6, -2.0])]
    label = T("caspases", 52, RED, weight=BOLD).move_to([0, 3.3, 0])
    center = put(caspase(1.7, RED, "id"), 0, -0.5)
    return ring, sib, label, center


class S04(Sc):
    """The mammalian protease is one of a family: caspases."""

    def construct(self):
        d = s03_objs()
        self.add(*[v for v in d.values()])
        ring, sib, label, center = fam_objs()
        self.play(FadeOut(VGroup(d["year"], d["pw"], d["pm"], d["c3"], d["c3l"], d["link"], d["rs"], d["mpl"])),
                  mv(d["mp"], 0, -0.5), run_time=0.9)
        self.at("belongs to")
        self.play(Create(ring), run_time=0.7)
        self.at("family")
        self.play(LaggedStart(*[FadeIn(s, scale=0.8) for s in sib], lag_ratio=0.2), run_time=1.0)
        self.at("named Caspases")
        self.play(FadeIn(label, shift=DOWN * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
BIG_S = 3.6
BIG_Y = -0.75


def big_caspase():
    g = put(caspase(BIG_S, RED, "id"), 0, BIG_Y)
    nb = notch_bottom(g)
    cys = Dot(radius=0.3, color=GOLD).move_to(nb + UP * 0.3)
    cysl = lab("cysteine", 36, GOLD, weight=BOLD).move_to(nb + DOWN * 0.5)
    return g, cys, cysl


class S05(Sc):
    """A caspase, large; the cysteine in the active site."""

    def construct(self):
        ring, sib, label, center = fam_objs()
        self.add(ring, *sib, label, center)
        g, cys, cysl = big_caspase()
        asl = lab("active site", 36, TEXT).move_to([0, 3.35, 0])
        asll = Line(asl.get_bottom() + DOWN * 0.08, notch_bottom(g) + UP * 1.1, color=TEXT, stroke_width=3, stroke_opacity=0.8)
        self.play(FadeOut(ring), FadeOut(label), *[FadeOut(s) for s in sib], scl(center, BIG_S / 1.7, 0, BIG_Y),
                  run_time=0.8)
        self.at("cut with")
        self.play(FadeIn(cys, scale=2.0), FadeIn(cysl), run_time=0.5)
        self.at("active site")
        self.play(FadeIn(asl), Create(asll), Indicate(cys, color=GOLD, scale_factor=1.5), run_time=0.7)
        self.finish()


def peptide(g, cut=False):
    """a short chain of blocks draped into the pocket; block 3 (gold) is the aspartate, right above the cysteine."""
    top = top_y(g)
    nb = notch_bottom(g)
    pos = [(-3.35, top + 0.6), (-1.95, top + 0.55), (0.0, nb[1] + 1.0), (1.95, top + 0.55), (3.35, top + 0.6)]
    blocks = VGroup(*[Square(0.65, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
                      .move_to([x, y, 0]) for x, y in pos])
    links = VGroup(*[Line(blocks[i].get_center(), blocks[i + 1].get_center(), color=GREY, stroke_width=4).set_z_index(-1)
                     for i in range(4)])
    blocks.set_z_index(1)
    blocks[2].set_stroke(GOLD, 4).set_fill(GOLD, 0.6)
    right = VGroup(blocks[3], blocks[4], links[3])
    if cut:
        right.shift([0.6, 0.7, 0]).rotate(-0.15)
        links[2].set_opacity(0.0)
    return blocks, links, right


def cut_mark(blocks):
    """a red double tick across the link just after the gold square"""
    a, b = blocks[2].get_center(), blocks[3].get_center()
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    c = a + d * 0.95
    return VGroup(*[Line(c + d * o - perp * 0.32, c + d * o + perp * 0.32, color=RED, stroke_width=7) for o in (-0.09, 0.09)])


def pep_labels(g, blocks):
    asp = lab("aspartate", 36, GOLD, weight=BOLD).move_to([0, top_y(g) + 1.65, 0])
    aspl = Line(asp.get_bottom() + DOWN * 0.08, blocks[2].get_top() + UP * 0.04, color=GOLD, stroke_width=3)
    tl = lab("target", 32, TEXT).move_to([-5.7, top_y(g) + 0.6, 0])
    return asp, aspl, tl


class S06(Sc):
    """A peptide target drops into the pocket; the aspartate sits right above the cysteine; the cut falls just after it."""

    def construct(self):
        g, cys, cysl = big_caspase()
        asl = lab("active site", 36, TEXT).move_to([0, 3.35, 0])
        asll = Line(asl.get_bottom() + DOWN * 0.08, notch_bottom(g) + UP * 1.1, color=TEXT, stroke_width=3, stroke_opacity=0.8)
        self.add(g, cys, cysl, asl, asll)
        blocks, links, right = peptide(g)
        asp, aspl, tl = pep_labels(g, blocks)
        mark = cut_mark(blocks)
        pep = VGroup(blocks, links)
        self.play(FadeOut(asl), FadeOut(asll), FadeIn(pep, shift=DOWN * 1.3), run_time=0.7)
        self.at("after")
        self.play(FadeIn(asp), Create(aspl), Indicate(blocks[2], color=GOLD, scale_factor=1.25), run_time=0.6)
        self.at("aspartate")
        self.play(Create(mark), run_time=0.2)
        self.play(right.animate.shift([0.6, 0.7, 0]).rotate(-0.15), links[2].animate.set_opacity(0),
                  mark.animate.shift([0.3, 0.35, 0]), run_time=0.5)
        self.at("their target")
        self.play(FadeIn(tl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
GS = 1.4
GRID_X = [-3.6, 0.0, 3.6]
TOP_Y, BOT_Y = 1.5, -1.8
INIT_X = [-2.6, 0.0, 2.6]
PLAT_Y = 2.85


def closed_rows():
    top = [put(caspase(GS, RED, "closed"), x, TOP_Y) for x in GRID_X]
    bot = [put(caspase(GS, RED, "closed"), x, BOT_Y) for x in GRID_X]
    return top, bot


def lit_now(c):
    c.body.set_stroke(c.ccol, 4).set_fill(c.ccol, 0.5)
    c.lid.shift(UP * c.lift).set_opacity(0)


def platform_objs():
    plat = RoundedRectangle(corner_radius=0.12, width=8.0, height=0.5, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, PLAT_Y, 0])
    pl = lab("platform", 26, TEXT).move_to(plat)
    init = lab("initiator caspases", 32, RED, weight=BOLD).move_to([0, 3.45, 0])
    return plat, pl, init


class S07(Sc):
    """Caspases are made inactive: lid shut, grey."""

    def construct(self):
        g, cys, cysl = big_caspase()
        blocks, links, right = peptide(g, cut=True)
        asp, aspl, tl = pep_labels(g, blocks)
        pep = VGroup(blocks, links, asp, aspl, tl)
        self.add(g, cys, cysl, pep)
        self.at("Caspases")
        self.play(FadeOut(pep), FadeOut(cys), FadeOut(cysl), run_time=0.4)
        self.at("made as")
        self.play(*c_close(g), run_time=0.4)
        top, bot = closed_rows()
        others = (top + bot)[1:]
        self.at("inactive")
        t = lab("inactive precursors", 36, GREY).move_to([0, -0.15, 0])
        self.play(scl(g, GS / BIG_S, GRID_X[0], TOP_Y),
                  LaggedStart(*[FadeIn(o, scale=0.8) for o in others], lag_ratio=0.1), FadeIn(t), run_time=0.7)
        self.finish()


class S08(Sc):
    """Initiators gather on a platform and light up."""

    def construct(self):
        top, bot = closed_rows()
        t = lab("inactive precursors", 36, GREY).move_to([0, -0.15, 0])
        self.add(*top, *bot, t)
        plat, pl, init = platform_objs()
        self.at("Initiator")
        self.play(FadeOut(t), FadeIn(plat, shift=UP * 0.2), FadeIn(pl), run_time=0.6)
        self.at("switch on")
        self.play(FadeIn(init), run_time=0.4)
        self.at("when they are")
        self.play(*[mv(c, x, TOP_Y) for c, x in zip(top, INIT_X)], run_time=0.9)
        self.at("platform")
        self.play(*[a for c in top for a in c_light(c)], run_time=0.7)
        self.finish()


def s08_end():
    top, bot = closed_rows()
    for c, x in zip(top, INIT_X):
        put(c, x, TOP_Y)
        lit_now(c)
    plat, pl, init = platform_objs()
    return top, bot, plat, pl, init


class S09(Sc):
    """Initiators cut executioners, which light up; the arrows start at the initiators."""

    def construct(self):
        top, bot, plat, pl, init = s08_end()
        self.add(*top, *bot, plat, pl, init)
        y0 = TOP_Y - GS * 0.65 - 0.05
        y1 = BOT_Y + GS * 0.65 + 0.2
        arrows = [arr([x, y0, 0], [bx, y1, 0], RED, 7) for x, bx in zip(INIT_X, GRID_X)]
        self.at("cut and")
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)
        self.at("activate")
        self.play(*[a for c in bot for a in c_light(c)], *[FadeOut(a) for a in arrows], run_time=0.6)
        ex = lab("executioner caspases", 32, RED, weight=BOLD).move_to([0, -3.35, 0])
        self.at("executioner")
        self.play(FadeIn(ex), run_time=0.4)
        self.finish()


# --- the cell that is taken apart ----------------------------------------------------------------------
CELL_A, CELL_B = 5.2, 2.95


def cell_objs():
    a, b = CELL_A, CELL_B
    fill = Ellipse(width=2 * a, height=2 * b, stroke_width=0, fill_color=BLUE, fill_opacity=0.07).move_to([0, 0, 0])
    arcs = VGroup(*[Arc(radius=1, start_angle=k * TAU / 10, angle=TAU / 10, stroke_color=BLUE, stroke_width=5)
                    for k in range(10)])
    arcs.stretch(a, 0).stretch(b, 1).move_to([0, 0, 0])
    prots = []
    for ri, y in enumerate((2.2, 1.45, -1.45, -2.2)):
        xs = np.arange(-4.5, 4.51, 1.05) + (0.5 if ri % 2 else 0.0)
        for x in xs:
            if (x / (a - 0.7)) ** 2 + (y / (b - 0.45)) ** 2 < 1.0:
                l_ = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.28, stroke_width=0,
                                      fill_color=PROT, fill_opacity=0.9).move_to([x - 0.16, y, 0])
                r_ = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.28, stroke_width=0,
                                      fill_color=PROT, fill_opacity=0.9).move_to([x + 0.16, y, 0])
                pr = VGroup(l_, r_)
                pr.l, pr.r = l_, r_
                prots.append(pr)
    return fill, arcs, prots


def cut_state(prots):
    """each protein cut in two (halves slightly apart)"""
    for p in prots:
        p.l.shift(LEFT * 0.13 + UP * 0.05).rotate(0.3)
        p.r.shift(RIGHT * 0.13 + DOWN * 0.05).rotate(-0.3)


def broken_targets(arcs, prots):
    """copies of arcs and proteins at the end of the break-up (arcs fly out, proteins drift out, all dimmed)"""
    outs, drifts = [], []
    for k, ar in enumerate(arcs):
        ang = (k + 0.5) * TAU / 10
        d = np.array([np.cos(ang) * 1.0, np.sin(ang) * 0.6, 0])
        t = ar.copy().shift(d).rotate(0.25).set_stroke(GREY, 4, opacity=0.5)
        outs.append(t)
    for p in prots:
        c = p.get_center()
        dvec = c / (np.linalg.norm(c) + 1e-6) * 0.7
        t = p.copy().shift(dvec).set_opacity(0.35)
        drifts.append(t)
    return outs, drifts


class S10(Sc):
    """Executioners cut many proteins; the cell comes apart."""

    def construct(self):
        top, bot, plat, pl, init = s08_end()
        for c in bot:
            lit_now(c)
        ex = lab("executioner caspases", 32, RED, weight=BOLD).move_to([0, -3.35, 0])
        self.add(*top, *bot, plat, pl, init, ex)
        fill, arcs, prots = cell_objs()
        prot_all = VGroup(*prots)
        plabel = lab("cellular proteins", 30, PROT).move_to([0, 3.45, 0])

        self.at("Executioners")
        self.play(FadeOut(VGroup(*top, plat, pl, init, ex)),
                  *[scl(c, 0.75, x, 0.0) for c, x in zip(bot, (-2.5, 0.0, 2.5))],
                  FadeIn(fill), Create(arcs), FadeIn(prot_all, lag_ratio=0.02), run_time=1.0)
        self.at("cut hundreds")
        cuts = [AnimationGroup(p.l.animate.shift(LEFT * 0.13 + UP * 0.05).rotate(0.3),
                               p.r.animate.shift(RIGHT * 0.13 + DOWN * 0.05).rotate(-0.3)) for p in prots]
        self.play(LaggedStart(*cuts, lag_ratio=0.03), run_time=0.9)
        self.at("cellular proteins")
        self.play(FadeIn(plabel), run_time=0.4)
        self.at("and take")
        outs, drifts = broken_targets(arcs, prots)
        self.play(*[Transform(a, t) for a, t in zip(arcs, outs)], *[Transform(p, t) for p, t in zip(prots, drifts)],
                  fill.animate.set_fill(GREY, 0.0), FadeOut(plabel), run_time=2.2)
        self.finish()


def s10_end_mobs():
    top, bot, plat, pl, init = s08_end()
    for c in bot:
        lit_now(c)
    cs = [scl_now(c, 0.75, x, 0.0) for c, x in zip(bot, (-2.5, 0.0, 2.5))]
    fill, arcs, prots = cell_objs()
    cut_state(prots)
    outs, drifts = broken_targets(arcs, prots)
    return cs + outs + drifts


def scl_now(g, k, x, y):
    c0 = g.body.get_center()
    g.scale(k, about_point=c0)
    g.shift(np.array([x, y, 0.0]) - c0)
    return g


# ---------------------------------------------------------------------------------------------
def pairpanels(lw, rw, lname, rname, lcol, rcol, rel, sizec=66, cy=-0.3):
    """a worm-left / mammal-right panel pair with two big chips and a link between them"""
    pl = panel(-3.8, cy, 4.8, 5.0, lname)
    pr = panel(3.8, cy, 4.8, 5.0, rname)
    cl = bchip(lw, lcol, sizec).move_to([-3.8, cy - 0.2, 0])
    cr = bchip(rw, rcol, sizec).move_to([3.8, cy - 0.2, 0])
    link = DoubleArrow([-1.25, cy - 0.2, 0], [1.25, cy - 0.2, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.26)
    rl = lab(rel, 28, GREY).move_to([0, cy + 0.35, 0])
    return pl, pr, cl, cr, link, rl


class S11(Sc):
    def construct(self):
        # the cell of the last scene is still breaking up: fade it out while the year and the CED-9 chip come in
        self.add(*s10_end_mobs())
        year = T("1994", 80, GOLD, font=TITLE_FONT).move_to([0, 3.05, 0])
        pl, pr, cl, cr, link, rl = pairpanels("CED-9", "Bcl-2", "worm", "mammal", GREEN, GREEN, "relative of")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(year, shift=DOWN * 0.2), FadeIn(pl), FadeIn(cl, scale=0.9),
                  run_time=0.8)
        self.at("CED 9")
        self.play(Indicate(cl, color=GREEN, scale_factor=1.12), run_time=0.6)
        self.at("relative")
        self.play(FadeIn(pr), GrowFromCenter(link), FadeIn(rl), run_time=0.7)
        self.at("BCL2")
        self.play(FadeIn(cr, scale=0.9), run_time=0.6)
        self.finish()


class S12(Sc):
    """Bcl-2 as a shield over a plain cell, on screen from the start."""

    def construct(self):
        year = T("1994", 80, GOLD, font=TITLE_FONT).move_to([0, 3.05, 0])
        pl, pr, cl, cr, link, rl = pairpanels("CED-9", "Bcl-2", "worm", "mammal", GREEN, GREEN, "relative of")
        self.add(year, pl, pr, cl, cr, link, rl)
        sh = shield(5.6, 6.4).move_to([0, -0.4, 0])
        cell = plain_cell(1.3).move_to([0, -0.05, 0])
        self.play(*[FadeOut(m) for m in (year, pl, pr, cl, link, rl)], cr.animate.scale(0.7).move_to([0, 2.15, 0]),
                  FadeIn(sh), FadeIn(cell, scale=0.8), run_time=0.7)
        self.at("keeps cells")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("alive")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.15), run_time=0.6)
        self.finish()


MITO_Y = -0.3


def s13_pieces():
    xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
    mito = RoundedRectangle(corner_radius=1.4, width=12.0, height=4.3, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.14).move_to([0, MITO_Y, 0])
    top = MITO_Y + 2.15
    by = top + 0.08 + 0.55
    mem = []
    first = RoundedRectangle(corner_radius=0.22, width=1.9, height=1.1, stroke_color=GREEN, stroke_width=3.5,
                             fill_color=GREEN, fill_opacity=0.3).move_to([xs[0], by, 0])
    first_l = lab("Bcl-2", 28, GREEN, weight=BOLD).move_to(first)
    mem.append(VGroup(first, first_l))
    for x in xs[1:]:
        mem.append(RoundedRectangle(corner_radius=0.22, width=1.9, height=1.1, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.3).move_to([x, by, 0]))
    fam = lab("BCL-2 family", 38, TEXT, weight=BOLD).move_to([0, 3.5, 0])
    dots = VGroup(*[Dot([x, MITO_Y + 0.2, 0], radius=0.3, color=PINK) for x in (-2.4, -1.2, 0.0, 1.2, 2.4)])
    cyt = lab("cytochrome c", 32, PINK).move_to([0, MITO_Y - 0.55, 0])
    mlab = lab("mitochondrion", 28, GREY).move_to([-4.0, MITO_Y - 1.5, 0])
    rel = arr([6.0, MITO_Y, 0], [6.0, -2.85, 0], PINK, 7)
    relq = lab("released?", 30, PINK).move_to([4.3, -2.7, 0])
    return dict(mito=mito, mem=mem, fam=fam, dots=dots, cyt=cyt, mlab=mlab, rel=rel, relq=relq, first=first)


class S13(Sc):
    """BCL-2 family members sit on the mitochondrion's surface; they decide whether cytochrome c leaves."""

    def construct(self):
        d = s13_pieces()
        # s12's picture: the shield with the plain cell and the Bcl-2 chip
        sh = shield(5.6, 6.4).move_to([0, -0.4, 0])
        cell = plain_cell(1.3).move_to([0, -0.05, 0])
        chip_ = bchip("Bcl-2", GREEN, 66).scale(0.7).move_to([0, 2.15, 0])
        self.add(sh, cell, chip_)
        self.play(FadeOut(cell), FadeOut(chip_), FadeOut(sh), FadeIn(d["mem"][0], scale=0.9), run_time=0.9)
        self.at("BCL2 family")
        self.play(FadeIn(d["fam"]), run_time=0.4)
        self.at("family")
        self.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in d["mem"][1:]], lag_ratio=0.2), run_time=0.9)
        self.at("Its")
        self.play(FadeIn(d["mito"]), run_time=0.6)
        self.at("whether")
        self.play(FadeIn(d["dots"], lag_ratio=0.15), FadeIn(d["cyt"]), run_time=0.7)
        self.at("mitochondria")
        self.play(FadeIn(d["mlab"]), run_time=0.4)
        self.at("release")
        self.play(Create(d["rel"]), FadeIn(d["relq"]), run_time=0.5)
        self.at("cytochrome")
        self.play(Indicate(d["cyt"], color=PINK, scale_factor=1.05), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
BCOL = ORANGE  # BH3-only regulators; the effectors Bax/Bak share it but are tagged


def fam_bar(n_blocks, color, x, y, bw=0.8, gap=0.05, h=0.85):
    blocks = VGroup(*[RoundedRectangle(corner_radius=0.08, width=bw, height=h, stroke_color=color, stroke_width=3,
                                       fill_color=color, fill_opacity=0.25) for _ in range(n_blocks)])
    blocks.arrange(RIGHT, buff=gap)
    return blocks.move_to([x, y, 0])


def bh3_only_bar(x, y, line_w, blk_pos):
    """a thin line with one gold BH3 block; blk_pos is the fraction along the line"""
    line = Line([0, 0, 0], [line_w, 0, 0], color=ORANGE, stroke_width=8)
    blk = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.85, stroke_color=GOLD, stroke_width=3,
                           fill_color=GOLD, fill_opacity=0.7)
    line.move_to([x, y, 0])
    blk.move_to([line.get_left()[0] + blk_pos * line_w, y, 0])
    g = VGroup(line, blk)
    g.line, g.blk = line, blk
    return g


class S14(Sc):
    def construct(self):
        px = [-4.4, 0.0, 4.4]
        pans = [panel(x, 0.35, 4.2, 5.8, "") for x in px]
        hy = 2.5
        hd = [ML("some members\nprotect", 30, GREEN, BOLD).move_to([px[0], hy, 0]),
              ML("others\npromote death", 30, ORANGE, BOLD).move_to([px[1], hy, 0]),
              ML("BH3-only members\npromote death too", 30, ORANGE, BOLD).move_to([px[2], hy, 0])]
        tags = [None, lab("effectors", 32, TEXT, weight=BOLD).move_to([px[1], -2.15, 0]),
                lab("BH3-only regulators", 29, TEXT, weight=BOLD).move_to([px[2], -2.15, 0])]
        ry = [0.75, -1.15]
        bcl = fam_bar(4, GREEN, px[0], 0.0)
        bcl_n = lab("Bcl-2", 36, GREEN, weight=BOLD).next_to(bcl, UP, buff=0.3)
        VGroup(bcl, bcl_n).move_to([px[0], 0.0, 0])
        bax = fam_bar(4, ORANGE, px[1], ry[0])
        bax_n = lab("Bax", 36, ORANGE, weight=BOLD).next_to(bax, UP, buff=0.25)
        bak = fam_bar(4, ORANGE, px[1], ry[1])
        bak_n = lab("Bak", 36, ORANGE, weight=BOLD).next_to(bak, UP, buff=0.25)
        bim = bh3_only_bar(px[2], ry[0], 3.5, 0.66)
        bim_n = lab("Bim", 36, ORANGE, weight=BOLD).next_to(bim, UP, buff=0.25)
        egl = bh3_only_bar(px[2], ry[1], 2.9, 0.32)
        egl_n = lab("EGL-1", 36, ORANGE, weight=BOLD).next_to(egl, UP, buff=0.25)
        legend = bchip("BH3 domain", GOLD, 28).move_to([0, -3.1, 0])

        self.add(*pans)
        self.play(FadeIn(hd[0]), run_time=0.4)
        self.play(FadeIn(bcl, shift=UP * 0.15), FadeIn(bcl_n), run_time=0.5)
        self.at("such as")
        self.play(FadeIn(hd[1]), FadeIn(tags[1]), run_time=0.4)
        self.play(FadeIn(bax, shift=UP * 0.15), FadeIn(bax_n), run_time=0.5)
        self.at("promote death")
        self.play(FadeIn(bak, shift=UP * 0.15), FadeIn(bak_n), run_time=0.5)
        self.at("The BH3")
        self.play(FadeIn(hd[2]), FadeIn(tags[2]), run_time=0.5)
        self.at("only members")
        self.play(FadeIn(bim, shift=UP * 0.15), FadeIn(bim_n), run_time=0.5)
        self.at("like EGL1")
        self.play(FadeIn(egl, shift=UP * 0.15), FadeIn(egl_n), run_time=0.5)
        self.at("That short domain")
        gold = [bcl[2], bax[2], bak[2]]
        self.play(*[b.animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.7) for b in gold],
                  Indicate(bim.blk, color=GOLD, scale_factor=1.3), Indicate(egl.blk, color=GOLD, scale_factor=1.3),
                  FadeIn(legend), run_time=0.9)
        self.at("only shared")
        dim = [b.animate.set_fill(opacity=0.08).set_stroke(opacity=0.4) for bar in (bcl, bax, bak)
               for i, b in enumerate(bar) if i != 2]
        self.play(*dim, run_time=0.8)
        self.finish()


class S15(Sc):
    def construct(self):
        pl, pr, cl, cr, link, rl = pairpanels("CED-4", "Apaf-1", "worm", "mammal", PURPLE, PURPLE, "related", cy=0.0)
        self.at("CED4")
        self.play(FadeIn(pl), FadeIn(cl, scale=0.9), run_time=0.7)
        self.at("related to")
        self.play(FadeIn(pr), GrowFromCenter(link), FadeIn(rl), run_time=0.7)
        self.at("PAF1", lead=0.4)
        self.play(FadeIn(cr, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16(Sc):
    """The table fills its first three columns, row by row; the fourth column's header waits, ghosted."""

    def construct(self):
        head = head_mobs()
        fh = fail_head(0.0)
        self.add(fh)
        self.at("So each")
        self.play(FadeIn(head), run_time=0.4)
        rows = [row_mobs(r, 0.0) for r in range(4)]
        self.at("worm part")
        self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("has a")
        self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("counterpart")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.2), run_time=0.5)
        self.until(2.7)
        self.play(FadeIn(rows[3], shift=RIGHT * 0.2), run_time=0.5)
        self.at("where the")
        self.play(fh.animate.set_opacity(FH_OP), run_time=0.5)
        self.finish()


class S17(Sc):
    def construct(self):
        flat, parts = table_state(4)
        self.add(*flat)
        slot = slot_mob()
        q = question_card()
        self.at("question")
        self.play(Create(slot), run_time=0.6)
        self.at("Which mammalian")
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S18Pause(NarratedScene):
    """silent: the question stays on screen, still; a ring traces the empty row over the five seconds, as a thinking timer."""

    def construct(self):
        flat, parts = table_state(4, slot=True, question=True)
        self.add(*flat)
        s = slot_mob()
        ring = RoundedRectangle(corner_radius=0.14, width=8.6, height=1.0, stroke_color=GOLD, stroke_width=5).move_to(s)
        think = lab("think for a moment", 30, GOLD).move_to([4.5, row_y(4), 0])
        self.add(think)
        self.play(Create(ring), run_time=self.narration_s - 0.4, rate_func=linear)
        self.finish()


class S19(Sc):
    def construct(self):
        flat, parts = table_state(4, slot=True, question=True)
        self.add(*flat)
        slot, q = parts["slot"], parts["q"]
        r4 = row_mobs(4)
        fails = [parts["rows"][r].fail for r in range(4)]
        for f in fails:
            f.set_opacity(0.0)
        self.at("Backs")
        self.play(FadeOut(q), FadeOut(slot), FadeIn(r4.mam, scale=0.8), run_time=0.7)
        self.at("gate")
        self.play(FadeIn(r4.role), run_time=0.5)
        self.at("The worm has")
        self.play(FadeIn(r4.worm), run_time=0.6)
        self.until(5.9)
        self.play(*[f.animate.set_opacity(0.5) for f in fails], run_time=0.6)
        self.finish()


class S20(Sc):
    """The full four-column table; the fourth column is read at full brightness."""

    def construct(self):
        flat, parts = table_state(4, bax=True, fails=0.5)
        self.add(*flat)
        self.at("where the")
        self.play(parts["fh"].animate.set_opacity(1.0), *[line.animate.set_opacity(1.0) for r in parts["rows"] for line in r.fail],
                  run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pan(cy=0.25, h=4.9):
    return panel(-3.45, cy, 6.2, h, "worm"), panel(3.45, cy, 6.2, h, "mammal")


C9_Y = 1.0
C4_Y21 = -0.55


def big_chip(text, color, w=3.3):
    return fchip(text, color, 54, w, 1.38)


def pic21():
    d = {}
    d["pw"], d["pm"] = pan()
    d["c9"] = big_chip("CED-9", GREEN).move_to([-3.45, C9_Y, 0])
    d["c4"] = big_chip("CED-4", PURPLE).move_to([-3.45, C4_Y21, 0])
    gap_y = (d["c9"].get_bottom()[1] + d["c4"].get_top()[1]) / 2
    d["grip"] = Line([-3.45 - 0.8, gap_y, 0], [-3.45 + 0.8, gap_y, 0], color=GREEN, stroke_width=10)
    d["hold"] = lab("holds CED-4 directly", 28, GREEN).move_to([-3.45, -1.75, 0])
    d["mito"] = RoundedRectangle(corner_radius=0.8, width=5.2, height=1.6, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.15).move_to([3.45, -1.3, 0])
    d["dots"] = VGroup(*[Dot([3.45 + dx, -1.1, 0], radius=0.22, color=PINK) for dx in (-1.5, -0.5, 0.5, 1.5)])
    d["mlab"] = lab("mitochondrion", 26, GREY).move_to([3.45, -1.8, 0])
    d["sh"] = shield(2.4, 2.3, GREEN, 0.35).move_to([3.45, 0.55, 0])
    d["shl"] = lab("Bcl-2", 34, GREEN, weight=BOLD).move_to([3.45, 0.7, 0])
    return d


class S21(Sc):
    """CED-9 holds CED-4 directly; Bcl-2 guards the mitochondria. Table chips settle into the two panels."""

    def construct(self):
        flat, parts = table_state(4, bax=True, fails=1.0, fh=1.0)
        self.add(*flat)
        d = pic21()
        rl = rolelab("brake")
        row = parts["rows"][2]
        c9t = row.worm
        bclt = row.mam
        others = [m for m in flat if m is not row] + [row.role, row.fail]
        # the two brake chips travel into their panels; everything else in the table fades
        self.play(*[FadeOut(o) for o in others], FadeIn(d["pw"]), FadeIn(d["pm"]), FadeIn(rl),
                  c9t.animate.scale(1.5).move_to([-3.45, C9_Y, 0]), bclt.animate.scale(1.5).move_to([3.45, C9_Y, 0]),
                  run_time=0.7)
        self.at("CED4")
        self.play(FadeIn(d["c4"], shift=UP * 0.15), Create(d["grip"]), run_time=0.6)
        self.at("directly")
        self.play(FadeIn(d["hold"]), run_time=0.5)
        self.at("mammalian", lead=0.4)
        fb = failbar("guards the mitochondria instead")
        self.play(FadeIn(fb, shift=UP * 0.15), FadeIn(d["mito"]), FadeIn(d["dots"]), FadeIn(d["mlab"]), run_time=0.7)
        self.at("guards")
        self.play(FadeOut(bclt), FadeIn(d["sh"], shift=DOWN * 0.2), FadeIn(d["shl"]), run_time=0.6)
        self.finish()


def pic21_end():
    d = pic21()
    return [d[k] for k in ("pw", "pm", "c9", "c4", "grip", "hold", "mito", "dots", "mlab", "sh", "shl")] + \
           [rolelab("brake"), failbar("guards the mitochondria instead")]


APAF_Y = 1.0
DOCK = np.array([3.45, 0.12, 0.0])


def pic22():
    d = {}
    d["pw"], d["pm"] = pan()
    d["c4"] = big_chip("CED-4", PURPLE).move_to([-3.45, APAF_Y, 0])
    d["apaf"] = big_chip("Apaf-1", PURPLE).move_to([3.45, APAF_Y, 0])
    o = pic21()
    d["mito"], d["mlab"], d["dots"] = o["mito"], o["mlab"], o["dots"]
    d["slot"] = DashedVMobject(Circle(radius=0.26, stroke_color=PINK, stroke_width=4), num_dashes=14).move_to([-3.45, -0.65, 0])
    d["q"] = T("?", 36, TEAL, weight=BOLD).move_to(d["slot"])
    d["nr"] = lab("no clear role", 28, TEXT).move_to([-3.45, -1.25, 0])
    d["cytl"] = lab("cytochrome c", 28, PINK).move_to([3.45, -0.3, 0])
    return d


class S22(Sc):
    """Apaf-1 needs cytochrome c (a dot leaves the mitochondrion and docks); CED-4 has an empty slot and a question mark."""

    def construct(self):
        old = pic21()
        for k in ("pw", "pm", "c9", "c4", "grip", "hold", "mito", "dots", "mlab", "sh", "shl"):
            self.add(old[k])
        rl_old = rolelab("brake")
        fb_old = failbar("guards the mitochondria instead")
        self.add(rl_old, fb_old)
        d = pic22()
        old["dots"][1].set_z_index(3)
        rl = rolelab("activator of the killer")
        fb = failbar("Apaf-1 needs cytochrome c")
        self.play(FadeOut(old["c9"]), FadeOut(old["grip"]), FadeOut(old["hold"]), FadeOut(old["sh"]), FadeOut(old["shl"]),
                  FadeOut(rl_old), FadeOut(fb_old), old["c4"].animate.move_to([-3.45, APAF_Y, 0]),
                  FadeIn(d["apaf"], shift=UP * 0.15), FadeIn(rl), run_time=0.7)
        dot = old["dots"][1]
        self.at("needs")
        self.play(dot.animate.move_to(DOCK), run_time=0.5)
        self.at("cytochrome")
        self.play(FadeIn(d["cytl"]), run_time=0.4)
        self.at("There is no")
        self.play(FadeIn(fb, shift=UP * 0.15), run_time=0.6)
        self.at("no clear")
        self.play(Create(d["slot"]), FadeIn(d["q"]), FadeIn(d["nr"]), run_time=0.7)
        self.finish()


def pic22_end():
    """every mobject of the picture at the end of s22 (for the start of s23)"""
    d = pic22()
    old = pic21()
    dots = old["dots"]
    dots[1].move_to(DOCK).set_z_index(3)
    mobs = [d["pw"], d["pm"], d["c4"], d["apaf"], d["mito"], d["mlab"], dots, d["slot"], d["q"], d["nr"], d["cytl"],
            rolelab("activator of the killer"), failbar("Apaf-1 needs cytochrome c")]
    return mobs


def pic23():
    y_e, y_b = 1.55, -0.85
    x0 = -3.9
    egl = Line([x0, y_e, 0], [x0 + 7.0, y_e, 0], color=ORANGE, stroke_width=10)
    bim = Line([x0, y_b, 0], [x0 + 9.4, y_b, 0], color=ORANGE, stroke_width=10)
    ge = RoundedRectangle(corner_radius=0.1, width=1.3, height=1.1, stroke_color=GOLD, stroke_width=4,
                          fill_color=GOLD, fill_opacity=0.75).move_to([x0 + 2.4, y_e, 0])
    gb = RoundedRectangle(corner_radius=0.1, width=1.3, height=1.1, stroke_color=GOLD, stroke_width=4,
                          fill_color=GOLD, fill_opacity=0.75).move_to([x0 + 6.2, y_b, 0])
    ne = lab("EGL-1", 38, ORANGE, weight=BOLD).move_to([-5.75, y_e, 0])
    nb = lab("Bim", 38, ORANGE, weight=BOLD).move_to([-5.75, y_b, 0])
    bhl_e = lab("BH3", 30, BG, weight=BOLD).move_to(ge)
    bhl_b = lab("BH3", 30, BG, weight=BOLD).move_to(gb)
    mid = (y_e + y_b) / 2
    join = DashedLine(ge.get_bottom() + DOWN * 0.03, gb.get_top() + UP * 0.03, color=GOLD, stroke_width=5)
    nm1 = lab("no match", 28, GREY).move_to([-3.4, mid, 0])
    nm2 = lab("no match", 28, GREY).move_to([4.6, mid + 0.0, 0])
    return dict(egl=egl, bim=bim, ge=ge, gb=gb, ne=ne, nb=nb, join=join, bhl_e=bhl_e, bhl_b=bhl_b, nm1=nm1, nm2=nm2)


class S23(Sc):
    def construct(self):
        self.add(*pic22_end())
        d = pic23()
        rl = rolelab("releases the brake")
        fb = failbar("only the BH3 domain matches")
        everything = list(self.mobjects)
        self.play(*[FadeOut(m) for m in everything], FadeIn(rl), FadeIn(d["ne"]), FadeIn(d["egl"]), FadeIn(d["ge"]),
                  FadeIn(d["bhl_e"]), run_time=0.6)
        self.at("BH3 only proteins")
        self.play(FadeIn(d["nb"]), Create(d["bim"]), FadeIn(d["gb"]), FadeIn(d["bhl_b"]), run_time=0.7)
        self.at("such as", lead=0.5)
        self.play(FadeIn(fb, shift=UP * 0.15), run_time=0.5)
        self.at("only in")
        self.play(Create(d["join"]), run_time=0.6)
        self.at("domain")
        self.play(FadeIn(d["nm1"]), FadeIn(d["nm2"]), run_time=0.6)
        self.finish()


def pic23_end():
    d = pic23()
    return [rolelab("releases the brake"), failbar("only the BH3 domain matches"), *d.values()]


class S24(Sc):
    def construct(self):
        mobs = pic23_end()
        self.add(*mobs)
        d = pic23()
        fc = bchip("functional counterpart", GOLD, 40).move_to([0, -2.05, 0])
        self.at("So EGL1")
        self.play(Indicate(VGroup(d["ne"], d["egl"], d["ge"]), color=ORANGE, scale_factor=1.05), run_time=0.6)
        self.at("functional counterpart")
        self.play(FadeIn(fc, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S25(Sc):
    """CED-3 maps onto caspase-9 (initiator) and caspase-3 (executioner): dashed grey 'maps to' arrows, targets first."""

    def construct(self):
        old = pic23_end()
        fc = bchip("functional counterpart", GOLD, 40).move_to([0, -2.05, 0])
        self.add(*old, fc)
        c3 = put(caspase(2.2, RED, "lit"), -4.1, 0.4)
        c3l = bchip("CED-3", RED, 34).move_to([-4.1, -1.95, 0])
        c9 = put(caspase(1.5, RED, "lit"), 1.2, 1.55)
        c3m = put(caspase(1.5, RED, "lit"), 1.2, -1.15)
        l9 = VGroup(lab("caspase-9", 36, RED, weight=BOLD), lab("initiator", 30, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        l9.move_to([3.0, 1.55, 0], aligned_edge=LEFT)
        l3 = VGroup(lab("caspase-3", 36, RED, weight=BOLD), lab("executioner", 30, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        l3.move_to([3.0, -1.15, 0], aligned_edge=LEFT)
        a1 = DashedLine([-2.1, 0.9, 0], [-0.25, 1.5, 0], color=GREY, stroke_width=7, dash_length=0.18).add_tip(tip_length=0.3).add_tip(at_start=True, tip_length=0.3)
        a2 = DashedLine([-2.1, -0.1, 0], [-0.25, -1.1, 0], color=GREY, stroke_width=7, dash_length=0.18).add_tip(tip_length=0.3).add_tip(at_start=True, tip_length=0.3)
        rl = rolelab("killer")
        fb = failbar("main worm caspase; mammals split the roles")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(rl), run_time=0.5)
        self.at("main caspase")
        self.play(FadeIn(c3, scale=0.9), run_time=0.5)
        self.at("CED 3")
        self.play(FadeIn(c3l), run_time=0.4)
        self.at("maps onto")
        self.play(FadeIn(c9, scale=0.9), FadeIn(c3m, scale=0.9), run_time=0.6)
        self.play(Create(a1), Create(a2), run_time=0.5)
        self.at("mammalian caspases")
        self.play(FadeIn(VGroup(l9[0], l3[0])), run_time=0.4)
        self.at("Mammals split", lead=0.2)
        self.play(FadeIn(fb, shift=UP * 0.15), run_time=0.5)
        self.at("initiator")
        self.play(FadeIn(l9[1]), run_time=0.4)
        self.at("executioner")
        self.play(FadeIn(l3[1]), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S26(Sc):
    def construct(self):
        year = T("2002", 90, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        prize = T("Nobel Prize in Physiology or Medicine", 40, TEXT, font=TITLE_FONT).move_to([0, 1.7, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).move_to([0, 1.15, 0])
        names = lab("Sydney Brenner, H. Robert Horvitz, John Sulston", 28, GREY).move_to([0, 0.55, 0])
        genetic = lab("the genetic regulation of", 36, GOLD).move_to([0, -0.4, 0])
        organ = bchip("organ development", BLUE, 34)
        pcd = bchip("programmed cell death", RED, 34)
        both = VGroup(organ, pcd).arrange(RIGHT, buff=0.6).move_to([0, -2.4, 0])
        bx0, bx1 = -5.2, 5.2
        brace = VGroup(Line([bx0, -1.05, 0], [bx1, -1.05, 0], color=GOLD, stroke_width=3),
                       Line([bx0, -1.05, 0], [bx0, -1.45, 0], color=GOLD, stroke_width=3),
                       Line([bx1, -1.05, 0], [bx1, -1.45, 0], color=GOLD, stroke_width=3))
        self.at("In 2002")
        self.play(FadeIn(year, shift=DOWN * 0.2), run_time=0.6)
        self.at("Nobel", lead=0.7)
        self.play(FadeIn(prize), GrowFromCenter(rule), run_time=0.8)
        self.at("honored")
        self.play(FadeIn(names), run_time=0.6)
        self.at("discoveries")
        self.play(FadeIn(genetic), Create(brace), run_time=0.8)
        self.at("organ development")
        self.play(FadeIn(organ, shift=UP * 0.2), run_time=0.6)
        self.at("programmed cell death")
        self.play(FadeIn(pcd, shift=UP * 0.2), run_time=0.6)
        self.finish()


def idea_card():
    box = RoundedRectangle(corner_radius=0.3, width=12.6, height=6.9, stroke_color=GOLD, stroke_width=4,
                           fill_color=GOLD, fill_opacity=0.05).move_to([0, 0, 0])
    hdr = T("THIS LESSON'S ONE IDEA", 34, GOLD, weight=BOLD).move_to([0, 2.75, 0])
    return box, hdr


class S27(Sc):
    def construct(self):
        box, hdr = idea_card()
        part = T("Part 1", 96, GOLD, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.at("Here is")
        self.play(FadeIn(box), FadeIn(hdr, shift=DOWN * 0.15), run_time=0.6)
        self.at("first part")
        self.play(FadeIn(part, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


def s28_parts():
    box, hdr = idea_card()
    part = T("Part 1", 96, GOLD, font=TITLE_FONT).move_to([0, 0.2, 0])
    l1 = T("The killers are already built;", 46, TEXT, font=TITLE_FONT).move_to([0, 1.1, 0])
    l2 = T("a survival signal keeps brakes on them.", 46, TEXT, font=TITLE_FONT).move_to([0, 0.2, 0])
    sig = bchip("survival signal", YELLOW, 36).move_to([-4.0, -2.0, 0])
    brk = bchip("brakes", GREEN, 36).move_to([0.1, -2.0, 0])
    kil = bchip("killers", RED, 36).move_to([4.5, -2.0, 0])
    a1 = arr(sig.get_right(), brk.get_left(), YELLOW, 5)
    a2 = inhib(brk.get_right() + RIGHT * 0.04, kil.get_left() + LEFT * 0.02, GREEN, 6)
    return box, hdr, part, l1, l2, sig, brk, kil, a1, a2


class S28(Sc):
    def construct(self):
        box, hdr, part, l1, l2, sig, brk, kil, a1, a2 = s28_parts()
        self.add(box, hdr, part)
        self.at("The killers")
        self.play(part.animate.scale(0.3).move_to([0, 2.15, 0]), FadeIn(l1, shift=UP * 0.15), FadeIn(kil, scale=0.9),
                  run_time=0.7)
        self.at("A survival")
        self.play(FadeIn(l2, shift=UP * 0.15), FadeIn(sig, scale=0.9), run_time=0.6)
        self.at("keeps brakes")
        self.play(FadeIn(brk, scale=0.9), GrowArrow(a1), Create(a2), run_time=0.7)
        self.finish()


class S29End(EndCard):
    """The idea card's line stays where it is while the card, the chips and the arrows fade; then the pointer to chapter 4."""
    LINE = "The killers are already built; a survival signal keeps brakes on them."

    def construct(self):
        box, hdr, part, l1, l2, sig, brk, kil, a1, a2 = s28_parts()
        part.scale(0.3).move_to([0, 2.15, 0])
        self.add(box, hdr, part, l1, l2, sig, brk, kil, a1, a2)
        site = T("biochemistrypedia.com", 26, color=TEAL).move_to([0, -3.2, 0])
        nxt = VGroup(T("next:", 34, GREY), T("the first brake", 44, GOLD, font=TITLE_FONT)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        nxt.move_to([0, -1.2, 0])
        self.play(*[FadeOut(m) for m in (box, hdr, part, sig, brk, kil, a1, a2)], l1.animate.move_to([0, 0.75, 0]),
                  l2.animate.move_to([0, -0.15, 0]), run_time=0.8)
        self.play(FadeIn(nxt, shift=UP * 0.15), FadeIn(site), run_time=0.7)
        self.finish()
