"""New Neighbours (Biochemistrypedia explainer, animal development, chapter 2).

COLOUR MAP (same as chapter 1): egg cytoplasm pale cream; inherited material PURPLE dots; signals GREEN;
ectoderm BLUE, mesoderm RED, endoderm YELLOW; calcium wave bright white-cyan.
One world: the embryo sits at EC with radius R (chapter 1's place); labels live in the right panel at RX.
All cartoons are schematic.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *  # noqa: F401,F403

_here = Path(globals().get("__file__", "scenes.py")).resolve().parent
_spec = importlib.util.spec_from_file_location("film1_scenes", _here.parent / "scenes.py")
_f1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_f1)
R, EC, RX = _f1.R, _f1.EC, _f1.RX
CREAM, PURPLE, CYAN = _f1.CREAM, _f1.PURPLE, _f1.CYAN
put, lab, make_motes, make_outline = _f1.put, _f1.lab, _f1.make_motes, _f1.make_outline
cells_k, patch_dots, PURPLE_CELLS, STAGES, PATCH = _f1.cells_k, _f1.patch_dots, _f1.PURPLE_CELLS, _f1.STAGES, _f1.PATCH
to3, ring_timer = _f1.to3, _f1.ring_timer
EggScene = _f1.EggScene

PALE = "#F6F1E7"
DARKC = "#8A5A3C"
NBEAD = 36
LAYER = {0: (2.4, 1.0, BLUE), 1: (1.65, 0.75, RED), 2: (0.85, 0.5, YELLOW)}
BANDS = [(2.03, 2.8, BLUE), (1.27, 2.0, RED), (0.5, 1.2, YELLOW)]


def bead(pos, r=0.4, color=CREAM, sw=4):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=BG, stroke_width=sw)
    c.move_to(pos)
    c.set_z_index(2)
    return c


def rpos(i, rad, n=NBEAD):
    a = TAU * i / n
    return np.array([EC[0] + rad * np.cos(a), EC[1] + rad * np.sin(a), 0.0])


def blastula():
    return VGroup(*[bead(rpos(i, 2.4), 0.39) for i in range(NBEAD)])


def band(i, op=0.3):
    a, b, col = BANDS[i]
    m = Annulus(inner_radius=a, outer_radius=b, color=col, fill_opacity=op, stroke_width=0).move_to(EC)
    m.set_z_index(0)
    return m


def layered():
    """The three-layer embryo as s03 leaves it."""
    g = VGroup()
    for i in range(3):
        g.add(band(i))
    for i in range(NBEAD):
        rad, sc, col = LAYER[i % 3]
        g.add(bead(rpos(i, rad), 0.39 * sc, col))
    return g


def leader(label, target, color=TEXT):
    a = Line(label.get_left() + LEFT * 0.1, target, color=color, stroke_width=3)
    a.set_z_index(8)
    return a


def shimmer(g, seed=0):
    t = {"v": 0.0}

    def f(m, dt):
        t["v"] += dt
        for i, d in enumerate(m):
            d.set_fill(opacity=0.8 + 0.2 * np.sin(2.5 * t["v"] + i + seed))
    g.add_updater(f)


def swatches(y1=0.8, y2=-0.4):
    a = Square(0.6, fill_color=PALE, fill_opacity=1, stroke_width=0).move_to([RX - 2.3, y1, 0])
    b = Square(0.6, fill_color=DARKC, fill_opacity=1, stroke_width=0).move_to([RX - 2.3, y2, 0])
    la = lab("pale (graft)").move_to([RX + 0.4, y1, 0])
    lb = lab("dark (host)").move_to([RX + 0.4, y2, 0])
    return VGroup(a, la), VGroup(b, lb)


def axis_slots(cx, cy, cols=9, rows=3, dx=0.62, dy=0.6):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(np.array([cx + (c - (cols - 1) / 2) * dx, cy + (r - (rows - 1) / 2) * dy, 0]))
    return out


def capsule(cx, cy, w, h, color=GREY, op=0.35):
    m = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=op).move_to([cx, cy, 0])
    return m


AX_C = (-2.5, 0.4)
GRAFT_COLS = {3, 4, 5}


def axis_cells(scale=1.0, cx=AX_C[0], cy=AX_C[1]):
    """Returns (graft beads, host beads) in axis slots."""
    slots = axis_slots(cx, cy, dx=0.62 * scale, dy=0.6 * scale)
    g, h = VGroup(), VGroup()
    for k, p in enumerate(slots):
        col = k % 9
        if col in GRAFT_COLS:
            g.add(bead(p, 0.26 * scale, PALE, 3))
        else:
            h.add(bead(p, 0.26 * scale, DARKC, 3))
    return g, h


# ================================================================= scenes
class S00Title(TitleCard):
    TITLE = "New Neighbours"
    LESSON = "Animal development"


class S01Hook(SpokenScene):
    def construct(self):
        cells = blastula()
        motes = make_motes(10, seed=4, origin=EC, rad=1.4)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.02), run_time=0.9)
        self.add(motes)
        self.at("A ball of cells")
        bl = put(lab("blastula", weight=BOLD, color=CREAM, size=38), EC[0], EC[1] + 0.05)
        self.play(FadeIn(bl), run_time=0.7)
        TC = np.array([RX + 0.1, 0.3, 0])
        self.at("a body with an outside")
        outer = Circle(radius=2.0, color=GREY, stroke_width=5).move_to(TC)
        self.play(Create(outer), run_time=1.0)
        lo = put(lab("outside"), TC[0], TC[1] + 2.35)
        self.play(FadeIn(lo), run_time=0.5)
        self.at("a middle")
        mid = Circle(radius=1.3, color=GREY, stroke_width=5).move_to(TC)
        lm = put(lab("middle"), TC[0], TC[1] + 1.65)
        self.play(Create(mid), FadeIn(lm), run_time=0.9)
        self.at("and a gut")
        gut = Circle(radius=0.6, color=GREY, stroke_width=5).move_to(TC)
        lg = put(lab("gut"), TC[0], TC[1], max_w=1.0)
        self.play(Create(gut), FadeIn(lg), run_time=0.6)
        self.at("How do surface cells")
        ar = Arrow(EC + RIGHT * 3.0 + UP * 0.2, [TC[0] - 2.1, 0.3, 0], color=GREY, buff=0.1, stroke_width=5)
        q = Text("?", font=TITLE_FONT, font_size=120, color=YELLOW).move_to([0.9, 1.4, 0])
        self.play(GrowArrow(ar), FadeIn(q, scale=0.6), run_time=0.9)
        t = {"v": 0.0}
        q.add_updater(lambda m, dt: (t.__setitem__("v", t["v"] + dt), m.set_opacity(0.7 + 0.3 * np.sin(4 * t["v"])))[0])
        self.at("does it matter whom")
        self.play(Indicate(cells[0:6], color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.finish()


class S02Link(EggScene):
    def construct(self):
        self.start_egg(0, outline=True, motes=False)
        self.at("cleavage cutting the egg")
        for k in range(1, 6):
            self.split_to(k, run=0.5)
            self.wait(0.15)
        self.at("Purple marked")
        dots = patch_dots(1.0)
        po = self.purple_outline()
        self.play(FadeIn(dots), Create(po), run_time=1.2)
        self.at("what a cell inherits")
        self.play(Indicate(dots, color=PURPLE, scale_factor=1.05), run_time=1.0)
        l1 = put(lab("cleavage partitions the egg", weight=BOLD, size=36), RX, 1.7, max_w=6.2)
        self.at("Cleavage makes new contacts")
        edges = VGroup()
        for c in STAGES[5]:
            e = Polygon(*[to3(p) for p in c["pts"]], stroke_color=TEXT, stroke_width=5, fill_opacity=0)
            e.set_z_index(5)
            edges.add(e)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.04), FadeIn(l1), run_time=2.0)
        self.play(FadeOut(edges), run_time=0.5)
        self.at("does not rearrange")
        g1 = lab("gastrulation:", color=YELLOW, weight=BOLD, size=36)
        g2 = lab("large-scale movement", color=YELLOW, size=34)
        gl = VGroup(g1, g2).arrange(DOWN, buff=0.15)
        put(gl, RX, -0.7, max_w=6.2)
        gl.set_opacity(0)
        self.add(gl)
        self.play(gl.animate.set_opacity(0.4), run_time=0.8)
        self.play(Indicate(self.outline, color=TEXT), run_time=1.0)
        self.play(gl.animate.set_opacity(1.0), run_time=0.8)
        self.finish()


class S03Layers(SpokenScene):
    def construct(self):
        cells = blastula()
        self.add(cells)
        motes = make_motes(10, seed=4, origin=EC, rad=1.4)
        self.add(motes)
        cap = put(lab("gastrulation", color=YELLOW, weight=BOLD, size=40), RX, 3.2)
        self.play(FadeIn(cap), run_time=0.6)
        self.at("Cells travel from the surface")
        self.play(FadeOut(motes), run_time=0.4)
        anims = []
        for i, c in enumerate(cells):
            rad, sc, col = LAYER[i % 3]
            if i % 3 != 0:
                anims.append(c.animate.move_to(rpos(i, rad)).scale(sc))
        self.play(LaggedStart(*anims, lag_ratio=0.04), run_time=3.0)
        self.at("and sort into three germ layers")
        self.play(Indicate(cells, color=CREAM, scale_factor=1.03), run_time=1.0)
        self.at("Ectoderm in blue")
        outer = VGroup(*[c for i, c in enumerate(cells) if i % 3 == 0])
        b0 = band(0)
        self.play(FadeIn(b0), *[c.animate.set_fill(BLUE) for c in outer], run_time=1.0)
        l0 = put(lab("ectoderm", color=BLUE, weight=BOLD), RX, 2.0, max_w=4.0)
        ld0 = leader(l0, EC + np.array([2.4 * np.cos(0.6), 2.4 * np.sin(0.6), 0]), BLUE)
        self.play(FadeIn(l0), Create(ld0), run_time=0.8)
        self.at("stays outside")
        self.play(Indicate(b0, color=BLUE, scale_factor=1.02), run_time=1.0)
        self.at("Mesoderm in red")
        mid = VGroup(*[c for i, c in enumerate(cells) if i % 3 == 1])
        b1 = band(1)
        self.play(FadeIn(b1), *[c.animate.set_fill(RED) for c in mid], run_time=1.0)
        l1 = put(lab("mesoderm", color=RED, weight=BOLD), RX, 0.6, max_w=4.0)
        ld1 = leader(l1, EC + np.array([1.65 * np.cos(0.3), 1.65 * np.sin(0.3), 0]), RED)
        self.play(FadeIn(l1), Create(ld1), run_time=0.8)
        self.at("forms the middle")
        self.play(Indicate(b1, color=RED, scale_factor=1.02), run_time=1.0)
        self.at("Endoderm in yellow")
        inn = VGroup(*[c for i, c in enumerate(cells) if i % 3 == 2])
        b2 = band(2)
        self.play(FadeIn(b2), *[c.animate.set_fill(YELLOW) for c in inn], run_time=1.0)
        l2 = put(lab("endoderm", color=YELLOW, weight=BOLD), RX, -0.8, max_w=4.0)
        ld2 = leader(l2, EC + np.array([0.85 * np.cos(0.0), 0.85 * np.sin(0.0), 0]), YELLOW)
        self.play(FadeIn(l2), Create(ld2), run_time=0.8)
        self.at("lines the inside")
        self.play(Indicate(b2, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.finish()


def sheet_cells(n, x0, x1, y, r=0.36, color=CREAM):
    xs = np.linspace(x0, x1, n)
    return xs, [bead([x, y, 0], r, color) for x in xs]


class S04Invag(SpokenScene):
    def construct(self):
        n = 11
        xs, cs = sheet_cells(n, -5.6, 0.4, 0.9)
        g = VGroup(*cs)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cs], lag_ratio=0.05), run_time=0.9)
        d = ValueTracker(0)
        xc = -2.6

        def upd(m):
            for x, c in zip(xs, m):
                u = x - xc
                c.move_to([x, 0.9 - d.get_value() * np.exp(-(u / 0.95) ** 2), 0])
        g.add_updater(upd)
        self.at("Embryos get cells inside")
        self.play(Indicate(g, color=CREAM, scale_factor=1.04), run_time=0.8)
        self.at("In invagination")
        self.play(d.animate.set_value(1.9), run_time=2.8, rate_func=smooth)
        lb1 = put(lab("invagination", color=YELLOW, weight=BOLD, size=40), -2.6, -2.0, max_w=6)
        lb2 = put(lab("sea urchin gut begins this way", size=28), -2.6, -2.8, max_w=7)
        self.play(FadeIn(lb1), FadeIn(lb2), run_time=0.7)
        self.at("like a finger pushed")
        BC = np.array([RX + 0.5, 0.4, 0])
        bd = ValueTracker(0)

        def ball():
            th = np.linspace(0, TAU, 160)
            rr = 1.4 - bd.get_value() * np.exp(-((th - PI / 2) ** 2) / 0.12)
            pts = [BC + np.array([r_ * np.cos(t), r_ * np.sin(t), 0]) for r_, t in zip(rr, th)]
            m = VMobject().set_points_as_corners(pts + [pts[0]])
            m.set_stroke(CREAM, 5).set_fill(CREAM, 0.5)
            return m

        bm = always_redraw(ball)
        fing = always_redraw(lambda: RoundedRectangle(corner_radius=0.22, width=0.44, height=1.3, stroke_color=GREY,
                                                      stroke_width=3, fill_color=GREY, fill_opacity=0.35)
                             .move_to(BC + np.array([0, 1.4 - bd.get_value() + 0.65, 0])))
        self.add(bm, fing)
        self.play(bd.animate.set_value(0.8), run_time=2.4, rate_func=smooth)
        self.play(bd.animate.set_value(0.4), run_time=1.0)
        self.finish()


class S05Invol(SpokenScene):
    def construct(self):
        spacing = 0.62
        LX0, LX1 = -5.6, -0.6
        yt, yb, rr = 1.5, 0.2, 0.65
        arc_len = PI * rr
        top_len = LX1 - LX0
        total = top_len + arc_len + top_len

        def path(s):
            if s < top_len:
                return np.array([LX0 + s, yt, 0])
            s2 = s - top_len
            if s2 < arc_len:
                a = PI / 2 - s2 / rr
                return np.array([LX1 + rr * np.cos(a) * 0 + rr * np.cos(a) - 0.0, (yt + yb) / 2 + rr * np.sin(a), 0]) \
                    if False else np.array([LX1 + 0.65 * np.cos(a), (yt + yb) / 2 + 0.65 * np.sin(a), 0])
            s3 = s2 - arc_len
            return np.array([LX1 - s3, yb, 0])

        N = 22
        off = ValueTracker(0)
        cs = VGroup(*[bead(path(0), 0.3, CREAM, 3) for _ in range(N)])

        def upd(m):
            for i, c in enumerate(m):
                s = i * spacing - 4.0 + off.get_value()
                if s < 0 or s > total:
                    c.set_opacity(0)
                else:
                    c.move_to(path(s))
                    c.set_fill(CREAM, 1)
                    c.set_stroke(BG, 3, 1)
        cs.add_updater(upd)
        self.add(cs)
        self.play(off.animate.set_value(2.0), run_time=1.0, rate_func=linear)
        self.at("In involution")
        self.play(off.animate.set_value(6.5), run_time=3.0, rate_func=linear)
        arr = Arc(radius=0.95, start_angle=PI / 2, angle=-PI, color=TEXT, stroke_width=5).move_to([LX1 + 0.0, (yt + yb) / 2, 0])
        arr.add_tip(tip_length=0.25)
        arr.shift(RIGHT * 0.5)
        lb = put(lab("involution", color=YELLOW, weight=BOLD, size=40), -3.0, -1.0, max_w=6)
        self.play(Create(arr), FadeIn(lb), run_time=0.8)
        self.at("In a frog")
        FC = np.array([RX + 0.5, 1.5, 0])
        emb = Circle(radius=1.4, fill_color=CREAM, fill_opacity=1, stroke_width=0).move_to(FC)
        cres = Arc(radius=0.9, start_angle=-2.5, angle=1.9, color=BG, stroke_width=22).move_to(FC + DOWN * 0.25)
        lipm = Arc(radius=1.0, start_angle=-2.5, angle=1.9, color=TEXT, stroke_width=4).move_to(FC + DOWN * 0.0)
        self.play(FadeIn(emb), FadeIn(cres), run_time=1.0)
        self.add(lipm)
        self.play(off.animate.set_value(9.0), run_time=1.5, rate_func=linear)
        self.at("the blastopore")
        bl = put(lab("blastopore", color=TEXT, weight=BOLD), RX + 0.3, -0.7, max_w=3.6)
        ba = Arrow(bl.get_top(), FC + DOWN * 1.05, color=TEXT, buff=0.1, stroke_width=4)
        self.play(FadeIn(bl), GrowArrow(ba), run_time=0.8)
        self.at("over the lip")
        ll = put(lab("lip", color=YELLOW, weight=BOLD), RX + 2.6, -0.1, max_w=1.2)
        la = Arrow(ll.get_left() + LEFT * 0.05, FC + np.array([1.0, -0.55, 0]), color=YELLOW, buff=0.1, stroke_width=4)
        self.play(FadeIn(ll), GrowArrow(la), run_time=0.8)
        self.play(off.animate.set_value(11.5), run_time=2.2, rate_func=linear)
        self.finish()


class S06Ingress(SpokenScene):
    def construct(self):
        n = 11
        xs, cs = sheet_cells(n, -5.6, 0.4, 1.0)
        g = VGroup(*cs)
        self.play(FadeIn(g), run_time=0.6)
        self.at("In ingressin")
        lb = put(lab("ingression", color=YELLOW, weight=BOLD, size=40), -2.6, -2.6, max_w=6)
        self.play(FadeIn(lb), run_time=0.6)
        self.at("single cells leave the sheet")
        for k, (idx, dy) in enumerate([(2, -1.4), (5, -1.8), (8, -1.3)]):
            self.play(cs[idx].animate.shift(DOWN * dy + RIGHT * 0.25 * (k - 1)), run_time=1.0)
        self.at("one at a time")
        self.play(*[cs[i].animate.shift(DOWN * 0.3) for i in (2, 5, 8)], run_time=0.8)
        self.at("Embryos combine")
        # merge into the one layered embryo with three movement markers
        emb = layered()
        sheet = VGroup(g, lb)
        self.play(FadeOut(sheet), FadeIn(emb), run_time=1.6)
        t1 = put(lab("a bend", color=TEXT), RX, 2.4, max_w=4.5)
        t2 = put(lab("a roll", color=TEXT), RX, 1.2, max_w=4.5)
        t3 = put(lab("single cells", color=TEXT), RX, 0.0, max_w=4.5)
        self.play(LaggedStart(FadeIn(t1), FadeIn(t2), FadeIn(t3), lag_ratio=0.5), run_time=1.6)
        cap = put(lab("embryos combine movements", color=YELLOW, weight=BOLD, size=36), RX, -1.8, max_w=6.2)
        self.play(FadeIn(cap), run_time=0.6)
        for lbm in (t1, t2, t3):
            self.play(Indicate(lbm, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.finish()


class S07Neighbours(SpokenScene):
    def construct(self):
        rowy = 1.5
        blues = VGroup(*[bead([x, rowy, 0], 0.6, BLUE) for x in np.linspace(-5.0, 0.0, 5)])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in blues], lag_ratio=0.08), run_time=0.8)
        reds = VGroup(*[bead([x, rowy, 0], 0.6, RED) for x in (1.3, 2.6)])
        self.play(FadeIn(reds), run_time=0.3)
        self.at("Moving inside")
        r1 = reds[0]
        self.play(r1.animate.move_to([-2.5, rowy - 1.2, 0]), run_time=2.0)
        self.at("Cells now sit next to cells")
        self.play(reds[1].animate.move_to([-1.0, rowy - 1.2, 0]), run_time=1.6)
        self.at("never touched before")
        tp = np.array([-2.5, rowy - 0.6, 0])
        for _ in range(2):
            fl = Circle(radius=0.12, color=TEXT, fill_opacity=0.9, stroke_width=0).move_to(tp).set_z_index(9)
            self.play(fl.animate.scale(3).set_opacity(0), run_time=0.7)
        nc = put(lab("new contact", color=TEXT, size=36), RX, 1.2, max_w=4.5)
        self.play(FadeIn(nc), run_time=0.6)
        self.at("Can a neighbor change")
        ar = Arrow([-2.5, rowy - 0.65, 0], [-2.5, rowy - 1.0 + 0.5, 0], color=GREEN, buff=0, stroke_width=0)
        ar = Arrow([-1.8, rowy - 1.3, 0], [-1.8, rowy - 0.35, 0], color=GREEN, buff=0.0, stroke_width=8)
        ar.shift(LEFT * 0.0)
        q = Text("?", font=TITLE_FONT, font_size=100, color=GREEN).move_to([-1.0, rowy - 3.0, 0]) if False else \
            Text("?", font=TITLE_FONT, font_size=110, color=GREEN).move_to([-3.5, rowy - 1.5, 0])
        self.play(GrowArrow(ar), FadeIn(q, scale=0.6), run_time=1.0)
        t = {"v": 0.0}
        q.add_updater(lambda m, dt: (t.__setitem__("v", t["v"] + dt), m.set_opacity(0.7 + 0.3 * np.sin(4 * t["v"])))[0])
        self.play(Indicate(blues[1], color=GREEN, scale_factor=1.12), run_time=1.0)
        self.play(Indicate(blues[2], color=GREEN, scale_factor=1.12), run_time=1.0)
        self.finish()


def newt_embryo(color):
    emb = Circle(radius=2.4, fill_color=color, fill_opacity=1, stroke_width=0).move_to(EC)
    cres = Arc(radius=1.5, start_angle=PI + 0.5, angle=1.6, color=BG, stroke_width=26).move_to(EC + DOWN * 0.15)
    return emb, cres


class S08Mangold(SpokenScene):
    def construct(self):
        emb, cres = newt_embryo(PALE)
        self.add(emb, cres)
        self.at("Hilda Mangold")
        c1 = put(lab("Hilde Mangold", weight=BOLD, size=40), RX, 2.9, max_w=6.2)
        c2 = put(lab("newt embryos", size=36), RX, 2.2, max_w=6.2)
        c3 = lab("published with", size=28)
        c4 = lab("Hans Spemann, 1924", size=28)
        cc = VGroup(c3, c4).arrange(DOWN, buff=0.1)
        put(cc, RX, 1.2, max_w=6.2)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(cc), run_time=0.7)
        self.at("the dorsal lip of the blastopore")
        lip_pt = EC + np.array([-1.05 * 0 + 1.5 * np.cos(PI + 1.3), -0.15 + 1.5 * np.sin(PI + 1.3), 0])
        glow = Circle(radius=0.35, color=YELLOW, fill_opacity=0.6, stroke_width=0).move_to(lip_pt).set_z_index(6)
        dl = put(lab("dorsal lip", color=YELLOW, weight=BOLD), RX, -0.8, max_w=4)
        da = Arrow(dl.get_left() + LEFT * 0.05, lip_pt + RIGHT * 0.2, color=YELLOW, buff=0.1, stroke_width=4)
        self.play(FadeIn(glow), FadeIn(dl), GrowArrow(da), run_time=0.7)
        self.at("She cut out a piece")
        tool = Line(lip_pt + np.array([0.9, 1.4, 0]), lip_pt + np.array([0.15, 0.2, 0]), color=GREY, stroke_width=5).set_z_index(7)
        self.play(Create(tool), run_time=0.5)
        piece = RoundedRectangle(corner_radius=0.15, width=0.7, height=0.45, fill_color=PALE, fill_opacity=1,
                                 stroke_color=YELLOW, stroke_width=4).move_to(lip_pt).set_z_index(8)
        self.play(FadeOut(glow), FadeIn(piece), run_time=0.4)
        self.play(piece.animate.move_to([0.5, 2.2, 0]).rotate(0.4), tool.animate.shift(UP * 0.6 + RIGHT * 0.3), run_time=1.6)
        self.at("on the future backside")
        self.play(Indicate(piece, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.finish()


class S09Graft(SpokenScene):
    def construct(self):
        emb, cres = newt_embryo(DARKC)
        piece = RoundedRectangle(corner_radius=0.15, width=0.7, height=0.45, fill_color=PALE, fill_opacity=1,
                                 stroke_color=YELLOW, stroke_width=4).move_to([0.5, 2.2, 0]).rotate(0.4).set_z_index(8)
        self.add(piece)
        self.play(FadeIn(emb), run_time=0.8)
        self.at("The donor came from a pale newt")
        lp = put(lab("pale donor species", color=PALE, weight=BOLD), RX + 0.4, 2.3, max_w=5.6)
        self.play(FadeIn(lp), Indicate(piece, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("She grafted the piece")
        self.play(piece.animate.move_to(EC + DOWN * 2.45).rotate(-0.4), run_time=2.0)
        vl = put(lab("belly side", color=TEXT, size=34), RX + 0.4, -1.8, max_w=4.5)
        self.play(FadeIn(vl), run_time=0.5)
        self.at("of a darker embryo")
        ld = put(lab("dark host species", color=DARKC, weight=BOLD), RX + 0.4, 1.0, max_w=5.6)
        self.play(FadeIn(ld), Indicate(emb, color=DARKC, scale_factor=1.04), run_time=1.2)
        self.at("The host grew a second")
        body = capsule(AX_C[0], 0.4, 6.2, 2.4, DARKC, 0.9).set_z_index(1)
        head = Circle(radius=0.8, fill_color=DARKC, fill_opacity=0.9, stroke_width=0).move_to([AX_C[0] - 3.3, 0.7, 0])
        larva = VGroup(body, head)
        self.play(FadeOut(VGroup(emb, cres, piece, lp, ld, vl)), FadeIn(larva), run_time=1.6)
        a1 = Line([AX_C[0] - 3.0, 1.2, 0], [AX_C[0] + 2.8, 1.2, 0], color=TEXT, stroke_width=6)
        l1 = put(lab("host axis", size=34), RX + 0.4, 1.5, max_w=4.5)
        self.play(Create(a1), FadeIn(l1), run_time=1.2)
        a2 = DashedVMobject(Line([AX_C[0] - 1.8, -0.4, 0], [AX_C[0] + 2.6, -0.4, 0], color=YELLOW, stroke_width=7), num_dashes=14)
        l2 = put(lab("second axis", color=YELLOW, weight=BOLD, size=36), RX + 0.4, -0.5, max_w=4.5)
        l3 = put(lab("schematic", size=28), RX + 0.4, -1.3, max_w=4.5)
        self.play(Create(a2), FadeIn(l2), FadeIn(l3), run_time=1.4)
        self.play(Indicate(a2, color=YELLOW), run_time=1.0)
        self.finish()


def predict_frame(scene, with_timer=False):
    cap = capsule(AX_C[0], AX_C[1], 6.2, 2.0, GREY, 0.45)
    stripes = VGroup(*[Line([x, AX_C[1] - 0.8, 0], [x, AX_C[1] + 0.8, 0], color=GREY, stroke_width=3)
                       for x in np.linspace(AX_C[0] - 2.4, AX_C[0] + 2.4, 9)])
    sa, sb = swatches(0.8, -0.4)
    card = chip("What colour is the new axis?", color=YELLOW, size=34)
    put(card, RX - 0.5, 2.4, max_w=6.0)
    scene.add(cap, stripes, sa, sb, card)
    return cap, stripes, sa, sb, card


class S10Predict(SpokenScene):
    def construct(self):
        cap = capsule(AX_C[0], AX_C[1], 6.2, 2.0, GREY, 0.45)
        self.add(cap)
        stripes = VGroup(*[Line([x, AX_C[1] - 0.8, 0], [x, AX_C[1] + 0.8, 0], color=GREY, stroke_width=3)
                           for x in np.linspace(AX_C[0] - 2.4, AX_C[0] + 2.4, 9)])
        self.play(Create(stripes), run_time=0.8)
        self.at("If the graft built")
        sa, sb = swatches(0.8, -0.4)
        self.play(FadeIn(sa), FadeIn(sb), run_time=0.8)
        self.at("only from its own inherited")
        dots = VGroup(*[Dot(axis_slots(AX_C[0], AX_C[1])[k], radius=0.08, color=PURPLE) for k in range(0, 27, 2)])
        self.play(FadeIn(dots), run_time=0.8)
        self.play(FadeOut(dots), run_time=0.6)
        self.at("what color would")
        card = chip("What colour is the new axis?", color=YELLOW, size=34)
        put(card, RX - 0.5, 2.4, max_w=6.0)
        self.play(FadeIn(card, scale=0.9), run_time=0.8)
        self.play(Indicate(cap, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.finish()


class S11Pause(SpokenScene):
    def construct(self):
        predict_frame(self)
        tr, base, arc = ring_timer(6.2, -3.1, 0.4)
        self.add(base, arc)
        self.play(tr.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        cap = capsule(AX_C[0], AX_C[1], 6.2, 2.0, GREY, 0.3)
        sa, sb = swatches(0.8, -0.4)
        self.add(cap, sa, sb)
        g, h = axis_cells()
        # host cells wait loosely around the axis
        rng = np.random.RandomState(3)
        slots = [c.get_center().copy() for c in h]
        for c, p in zip(h, slots):
            c.move_to(p + np.array([rng.uniform(-0.5, 0.5), rng.choice([-1, 1]) * rng.uniform(1.6, 2.2), 0]))
        self.play(FadeIn(g), FadeIn(h), run_time=0.7)
        self.at("It was not all pale")
        self.play(Indicate(g, color=PALE, scale_factor=1.1), run_time=1.0)
        self.at("Dark host cells were part")
        self.play(*[c.animate.move_to(p) for c, p in zip(h, slots)], run_time=2.6)
        self.at("The graft had recruited")
        arrows = VGroup()
        for hc in h:
            src = g[4].get_center()
            d = hc.get_center() - src
            n = np.hypot(d[0], d[1])
            arrows.add(Arrow(src + d / n * 0.3, hc.get_center() - d / n * 0.3, color=GREEN, buff=0, stroke_width=5,
                             max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12).set_z_index(6))
        arrows.set_z_index(6)
        lb = put(lab("graft recruits host cells", color=GREEN, weight=BOLD, size=34), RX + 0.4, 2.2, max_w=6.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), FadeIn(lb), run_time=2.0)
        self.at("It told host cells")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.2) for c in h], run_time=1.2)
        sc = put(lab("schematic proportions", size=28), RX + 0.4, -2.0, max_w=6.2)
        self.play(FadeIn(sc), FadeOut(arrows), run_time=0.8)
        self.finish()


class S13Colour(SpokenScene):
    def construct(self):
        div = Line([0, -3.4, 0], [0, 3.4, 0], color=GREY, stroke_width=3)
        self.add(div)
        LC = np.array([-3.4, 0.3, 0])
        egg = Circle(radius=2.2, fill_color=CREAM, fill_opacity=1, stroke_width=0).move_to(LC)
        dots = VGroup(*[Dot(LC + np.array([(p[0] + 0.48 * 2.8 * 0), p[1], 0]) * 0.78 + np.array([0.0, 0.0, 0]),
                            radius=0.07, color=PURPLE) for p in PATCH])
        self.play(FadeIn(egg), run_time=0.8)
        self.at("Remember the crescent")
        self.play(FadeIn(dots), run_time=0.8)
        shimmer(dots)
        self.at("colour showed where")
        lw = put(lab("where it goes", color=PURPLE, weight=BOLD, size=36), LC[0], -2.9, max_w=5.6)
        self.play(FadeIn(lw), Indicate(dots, color=PURPLE, scale_factor=1.1), run_time=1.2)
        self.at("not what it did")
        self.play(Indicate(egg, color=CREAM, scale_factor=1.03), run_time=1.2)
        self.at("Here color still only traced")
        g, h = axis_cells(0.8, 3.4, 1.4)
        cap = capsule(3.4, 1.4, 5.2, 1.7, GREY, 0.3)
        self.play(FadeIn(cap), FadeIn(g), FadeIn(h), run_time=1.2)
        shimmer(g, 1)
        shimmer(h, 2)
        self.at("The graft was the test")
        t1 = put(lab("graft = the test", color=YELLOW, weight=BOLD, size=34), 3.4, -0.4, max_w=5.6)
        self.play(FadeIn(t1), Indicate(g, color=PALE, scale_factor=1.1), run_time=1.2)
        self.at("and color showed host cells")
        t2 = put(lab("colour = who built what", color=TEXT, weight=BOLD, size=34), 3.4, -1.3, max_w=5.6)
        self.play(FadeIn(t2), Indicate(h, color=DARKC, scale_factor=1.1), run_time=1.2)
        tick = VMobject().set_points_as_corners([[2.5, -2.2, 0], [3.0, -2.75, 0], [4.1, -1.8, 0]]).set_stroke(GREEN, 10)
        self.play(Create(tick), run_time=0.8)
        self.finish()


class S14Induction(SpokenScene):
    def construct(self):
        C = np.array([-2.7, 0.3, 0])
        graft = VGroup(*[bead(C + np.array([dx, 0, 0]), 0.45, PALE) for dx in (-0.8, 0.0, 0.8)])
        nb = VGroup(*[bead(C + np.array([3.0 * np.cos(a), 2.3 * np.sin(a), 0]), 0.4, DARKC)
                      for a in np.linspace(0, TAU, 11)[:-1]])
        self.add(graft)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in nb], lag_ratio=0.05), run_time=0.9)
        self.at("A signal from one group")
        arrows = VGroup()
        for c in nb:
            d = c.get_center() - C
            n = np.hypot(d[0], d[1])
            arrows.add(Arrow(C + d / n * 1.4 if abs(d[0]) < 1.2 else C + np.array([np.sign(d[0]) * 1.4, 0, 0]),
                             c.get_center() - d / n * 0.5, color=GREEN, buff=0, stroke_width=5,
                             max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=12))
        arrows.set_z_index(6)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), run_time=1.4)
        self.at("changes the fate")
        self.play(*[c.animate.set_stroke(GREEN, 8) for c in nb], run_time=0.8)
        self.at("is called induction")
        li = put(lab("induction", color=GREEN, weight=BOLD, size=42), RX, 2.0, max_w=5.5)
        self.play(FadeIn(li), run_time=0.7)
        self.play(*[Indicate(a, color=GREEN) for a in arrows], run_time=1.2)
        self.at("The grafted tissue")
        self.play(Indicate(graft, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("the organizer")
        lo = put(lab("organizer", color=PALE, weight=BOLD, size=42), RX, 0.8, max_w=3.6)
        self.play(FadeIn(lo), run_time=0.8)
        self.play(Indicate(graft, color=PALE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S15Both(SpokenScene):
    def construct(self):
        C = np.array([-2.5, 0.3, 0])
        cell = Circle(radius=1.5, fill_color=CREAM, fill_opacity=1, stroke_color=BG, stroke_width=4).move_to(C)
        nbs = VGroup(*[bead(C + np.array([2.7 * np.cos(a), 2.3 * np.sin(a), 0]), 0.5, DARKC)
                       for a in np.linspace(0.4, TAU + 0.4, 7)[:-1]])
        self.play(FadeIn(cell, scale=0.8), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in nbs], lag_ratio=0.1), run_time=1.2)
        self.at("two sources")
        self.play(Indicate(cell, color=CREAM, scale_factor=1.06), run_time=1.0)
        self.at("Purple")
        pd = VGroup(*[Dot(C + np.array([0.5 * np.cos(a) * r, 0.5 * np.sin(a) * r, 0]) * 1.5, radius=0.09, color=PURPLE)
                      for a, r in zip(np.linspace(0, TAU, 12)[:-1], [1.0, 0.6] * 6)]).set_z_index(5)
        shimmer(pd)
        self.play(FadeIn(pd), run_time=0.8)
        li = put(lab("inherits", color=PURPLE, weight=BOLD, size=42), RX + 0.4, 2.0, max_w=5.5)
        self.play(FadeIn(li), run_time=0.7)
        self.play(Indicate(pd, color=PURPLE, scale_factor=1.15), run_time=1.0)
        self.at("Green")
        arrows = VGroup()
        for c in nbs:
            d = c.get_center() - C
            n = np.hypot(d[0], d[1])
            arrows.add(Arrow(c.get_center() - d / n * 0.6, C + d / n * 1.55, color=GREEN, buff=0, stroke_width=5,
                             max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12))
        arrows.set_z_index(6)
        lt = put(lab("is told", color=GREEN, weight=BOLD, size=42), RX + 0.4, 0.4, max_w=5.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(lt), run_time=1.8)
        self.play(*[Indicate(a, color=GREEN) for a in arrows], run_time=1.0)
        self.at("Most embryos studied closely")
        cp = put(lab("most embryos studied closely use both", color=YELLOW, weight=BOLD, size=34), 0, -3.4, max_w=11.5)
        self.play(FadeIn(cp), run_time=0.8)
        self.play(Indicate(pd, color=PURPLE, scale_factor=1.2), Indicate(arrows, color=GREEN), run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "Fate follows from what a cell inherits and what it is told."
