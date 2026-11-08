"""Reading phylogenetic trees: relatedness lives in the most recent common ancestor.

COLOR MAP (one color per concept, whole video)
  BLUE   = branches of the tree
  TEAL   = internal nodes (inferred ancestors) and their letters
  YELLOW = the thing being traced / the most recent common ancestor ring
  GREEN  = unchanged (rotation changes nothing)
  RED    = a misreading (crossed out)
  GREY   = outgroup tag, added fish, page-position remarks
  TEXT   = species labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

STRUCT = ("R", ["lamprey", ("J", ["shark", ("B", ["trout", ("T", ["frog", "human"])])])])
XS = {"R": -5.0, "J": -3.7, "B": -2.4, "T": -1.1}
TIPX = 0.7


class Tree:
    """Rectangular cladogram with level tips. Rotating a node (flips) only reorders rows."""

    def __init__(self, struct=STRUCT, flips=(), xs=XS, tipx=TIPX, top=2.2, gap=1.1, shift=-0.6,
                 letters=("R", "J", "B", "T"), tip_names=None, tip_color=None):
        self.pos, self.parent, self.tipx, self.nd = {}, {}, tipx, {}
        order = []
        self._rows(struct, set(flips), order)
        for i, nm in enumerate(order):
            self.pos[nm] = np.array([tipx + shift, top - i * gap, 0.0])
        self._internal(struct, xs, shift)
        parts = []
        self._build(struct, parts, xs, shift, letters, tip_names or {}, tip_color or {})
        self.g = VGroup(*parts)

    def _rows(self, n, flips, order):
        if isinstance(n, str):
            order.append(n); return
        name, kids = n
        for k in (kids[::-1] if name in flips else kids):
            self._rows(k, flips, order)

    def _internal(self, n, xs, shift):
        if isinstance(n, str):
            return self.pos[n]
        name, kids = n
        ys = []
        for k in kids:
            self.parent[k if isinstance(k, str) else k[0]] = name
            ys.append(self._internal(k, xs, shift)[1])
        self.pos[name] = np.array([xs[name] + shift, (min(ys) + max(ys)) / 2, 0.0])
        return self.pos[name]

    def _build(self, n, parts, xs, shift, letters, tip_names, tip_color):
        if isinstance(n, str):
            p = self.pos[n]
            dot = Dot(p, radius=0.08, color=TEXT)
            lab = T(tip_names.get(n, n), 26, tip_color.get(n, TEXT)).move_to(p + RIGHT * 0.25, aligned_edge=LEFT)
            parts.extend([dot, lab])
            return
        name, kids = n
        p = self.pos[name]
        ys = [self.pos[k if isinstance(k, str) else k[0]][1] for k in kids]
        parts.append(Line([p[0], min(ys), 0], [p[0], max(ys), 0], color=BLUE, stroke_width=5))
        for k in kids:
            kn = k if isinstance(k, str) else k[0]
            q = self.pos[kn]
            parts.append(Line([p[0], q[1], 0], [q[0], q[1], 0], color=BLUE, stroke_width=5))
        dot = Dot(p, radius=0.11 if name in letters else 0.07, color=TEAL)
        lab = T(name if name in letters else "", 24 if name in letters else 22, TEAL, weight=BOLD)
        if name in letters:
            lab.move_to(p + np.array([-0.32, 0.3, 0]))
        else:
            lab = Dot(p, radius=0.001, color=BG)
        if name == "R":
            parts.append(Line([p[0] - 0.35, p[1], 0], [p[0], p[1], 0], color=BLUE, stroke_width=5))
        self.nd[name] = dot
        parts.extend([dot, lab])
        for k in kids:
            self._build(k, parts, xs, shift, letters, tip_names, tip_color)

    def trace(self, tip, target, color=YELLOW, w=9):
        pts = [self.pos[tip]]
        cur = tip
        while cur != target:
            par = self.parent[cur]
            pts.append(np.array([self.pos[par][0], self.pos[cur][1], 0]))
            pts.append(self.pos[par])
            cur = par
        m = VMobject(stroke_color=color, stroke_width=w)
        m.set_points_as_corners(pts)
        return m


def ring(p, color=YELLOW, r=0.3):
    return Circle(radius=r, stroke_color=color, stroke_width=5).move_to(p)


def tag(text, color=GREY, size=24):
    return T(text, size, color)


def clade_box(t, color):
    l, r = t.pos["T"][0] - 0.4, t.pos["frog"][0] + 1.45
    ys = [t.pos["frog"][1], t.pos["human"][1]]
    h = abs(ys[0] - ys[1]) + 0.8
    return RoundedRectangle(corner_radius=0.2, width=r - l, height=h, stroke_color=color, stroke_width=4).move_to([(l + r) / 2, sum(ys) / 2, 0])


def strike(m, color=RED):
    return Line(m.get_left() + LEFT * 0.08, m.get_right() + RIGHT * 0.08, color=color, stroke_width=5).move_to(m)


class S00Title(TitleCard):
    LESSON = "Reading phylogenetic trees"
    TITLE = "Relatedness lives in the common ancestor"


# ---------------------------------------------------------------------------------------------
class S01Trout(SpokenScene):
    def construct(self):
        y = -0.4
        trout = VGroup(Dot(radius=0.2, color=TEXT), T("trout", 30)).arrange(DOWN, buff=0.2).move_to([-3.6, y, 0])
        shark = VGroup(Dot(radius=0.2, color=TEXT), T("shark", 30)).arrange(DOWN, buff=0.2).move_to([0.2, y, 0])
        human = VGroup(Dot(radius=0.2, color=TEXT), T("human", 30)).arrange(DOWN, buff=0.2).move_to([4.2, y, 0])
        self.at("A trout")
        self.play(FadeIn(trout, scale=0.8), FadeIn(human, scale=0.8), run_time=0.7)
        arc = ArcBetweenPoints(trout[0].get_top() + UP * 0.15, human[0].get_top() + UP * 0.15, angle=-1.6)
        link = DashedVMobject(arc, num_dashes=40).set_color(YELLOW).set_stroke(width=5)
        self.play(Create(link), run_time=0.8)
        self.at("than to a shark")
        self.play(FadeIn(shark, scale=0.8), run_time=0.6)
        self.at("both look like fish")
        br = VGroup(Line([-3.6, -1.1, 0], [-3.6, -1.35, 0]), Line([-3.6, -1.35, 0], [0.2, -1.35, 0]), Line([0.2, -1.35, 0], [0.2, -1.1, 0]))
        br.set_color(GREY).set_stroke(width=5)
        lk = tag("look alike", GREY, 28).next_to(br, DOWN, buff=0.06)
        self.play(Create(br), FadeIn(lk), run_time=0.8)
        self.at("how can a tree show it")
        q = T("?", 80, YELLOW, weight=BOLD).move_to([1.5, 2.1, 0])
        ql = tag("closer kin?", YELLOW, 28).next_to(q, LEFT, buff=0.3)
        self.play(FadeIn(q, scale=0.6), FadeIn(ql), run_time=0.6)
        self.at("branching diagram")
        tree = chip("phylogenetic tree: hypothesized ancestry", TEAL, 30).move_to([0, -3.1, 0])
        self.play(FadeIn(tree, shift=UP * 0.2), run_time=0.7)
        self.at("the living species")
        tips = tag("living species sit at the tips", TEXT, 26).move_to([0, -2.4, 0])
        self.play(FadeIn(tips), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Nodes(SpokenScene):
    def construct(self):
        tr = Tree()
        self.at("rooted tree")
        self.play(Create(VGroup(*[m for m in tr.g if isinstance(m, Line)]), lag_ratio=0.12), run_time=2.0)
        self.play(FadeIn(VGroup(*[m for m in tr.g if not isinstance(m, Line)])), run_time=0.8)
        self.at("assumed to lie outside")
        lam = tr.pos["lamprey"]
        og = tag("outgroup", GREY, 28).move_to([1.9, lam[1], 0], aligned_edge=LEFT)
        oa = Arrow(og.get_left() + LEFT * 0.05, lam + RIGHT * 1.5, buff=0.1, color=GREY, stroke_width=4)
        self.play(FadeIn(og), GrowArrow(oa), run_time=0.7)
        self.at("branch splits")
        for nm in ["T", "B", "J", "R"]:
            self.play(ring(tr.pos[nm], YELLOW, 0.32).animate if False else Indicate(tr.nd[nm], color=YELLOW, scale_factor=2.5), run_time=0.35)
        self.at("inferred common ancestor")
        nd = tag("node = inferred\ncommon ancestor", TEAL, 26).move_to([1.9, 0.0, 0], aligned_edge=LEFT)
        rg = ring(tr.pos["B"], YELLOW, 0.32)
        self.play(Create(rg), FadeIn(nd), run_time=0.7)
        self.at("the root is")
        rt = tag("← root", TEAL, 28).move_to(tr.pos["R"] + np.array([1.0, 0, 0]))
        self.play(FadeOut(rg), FadeOut(nd), FadeIn(rt), Indicate(tr.nd["R"], color=YELLOW, scale_factor=2.5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Meet(SpokenScene):
    def construct(self):
        tr = Tree()
        self.add(tr.g)
        self.at("trace each one back")
        t1, t2 = tr.trace("trout", "B"), tr.trace("human", "B")
        self.play(Create(t1), Create(t2), run_time=1.0)
        self.at("Trout and human meet")
        rg = ring(tr.pos["B"], YELLOW, 0.34)
        a = tag("trout + human meet at B", YELLOW, 26).move_to([1.9, 0.9, 0], aligned_edge=LEFT)
        self.play(Create(rg), FadeIn(a), run_time=0.6)
        self.at("Trout and shark meet")
        t3 = tr.trace("shark", "J")
        t4 = tr.trace("trout", "J")
        rg2 = ring(tr.pos["J"], YELLOW, 0.34)
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(rg), t3.animate if False else Create(t3), Create(t4), run_time=0.9)
        self.play(Create(rg2), run_time=0.4)
        b = tag("trout + shark meet at J", YELLOW, 26).move_to([1.9, -0.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(b), run_time=0.4)
        self.at("is older")
        old = tag("J is older: ancestral to B", GREY, 24).move_to([1.9, -1.0, 0], aligned_edge=LEFT)
        ar = Arrow(tr.pos["B"] + UP * 0.2, tr.pos["B"] + UP * 0.2, buff=0)
        self.play(FadeIn(old), run_time=0.5)
        self.at("the latest node")
        self.play(FadeOut(t3), FadeOut(t4), FadeOut(rg2), FadeOut(b), FadeOut(old), FadeOut(a), run_time=0.5)
        t1, t2 = tr.trace("trout", "B"), tr.trace("human", "B")
        rg = ring(tr.pos["B"], YELLOW, 0.34)
        mr = tag("most recent\ncommon ancestor", YELLOW, 26).move_to([1.9, 1.0, 0], aligned_edge=LEFT)
        self.play(Create(t1), Create(t2), Create(rg), FadeIn(mr), run_time=0.8)
        self.at("more closely related to human")
        t5 = tr.trace("frog", "T", w=9)
        t6 = tr.trace("T", "B", w=9)
        self.play(Create(t5), Create(t6), run_time=0.6)
        self.at("equally to frog")
        res = tag("trout is equally close\nto frog and human", GREEN, 26).move_to([1.9, -0.9, 0], aligned_edge=LEFT)
        self.play(FadeIn(res), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Spin(SpokenScene):
    def construct(self):
        tr = Tree()
        self.add(tr.g)
        self.at("Now spin")
        tt = Tree(flips={"T"})
        self.play(Transform(tr.g, tt.g), run_time=1.4)
        ok = tag("no change:\nsame relationships", GREEN, 26).move_to([1.9, 1.6, 0], aligned_edge=LEFT)
        self.at("same two descendants")
        d1, d2 = tt.trace("frog", "T"), tt.trace("human", "T")
        self.play(Indicate(tr.nd["T"], color=YELLOW, scale_factor=2.5), Create(d1), Create(d2), run_time=0.8)
        self.at("A clade")
        cl = clade_box(tt, GREEN)
        self.play(FadeOut(d1), FadeOut(d2), Create(cl), run_time=0.7)
        self.at("same members")
        self.play(FadeIn(ok), Indicate(cl, color=GREEN, scale_factor=1.06), run_time=0.8)
        self.at("have not changed")
        self.play(FadeOut(cl), run_time=0.4)
        self.at("as well")
        t2 = Tree(flips={"T", "B"})
        self.play(Transform(tr.g, t2.g), run_time=1.5)
        self.at("side by side")
        t3 = Tree(flips={"T"})
        self.play(Transform(tr.g, t3.g), FadeOut(ok), run_time=1.2)
        bx = t3.pos["shark"][0] + 1.45
        ys, yt = t3.pos["shark"][1], t3.pos["trout"][1]
        bk = VGroup(Line([bx - 0.12, ys, 0], [bx, ys, 0]), Line([bx, ys, 0], [bx, yt, 0]), Line([bx, yt, 0], [bx - 0.12, yt, 0]))
        bk.set_color(RED).set_stroke(width=5)
        bad = tag("side by side,\nnot closest kin", RED, 26).move_to([bx + 0.25, (ys + yt) / 2, 0], aligned_edge=LEFT)
        self.play(Create(bk), FadeIn(bad), run_time=0.6)
        self.at("sister group")
        fb = clade_box(t3, YELLOW)
        sis = tag("trout's sister group", YELLOW, 26).move_to([1.9, (t3.pos["human"][1] + t3.pos["frog"][1]) / 2, 0], aligned_edge=LEFT)
        self.play(FadeOut(bk), FadeOut(bad), Create(fb), FadeIn(sis), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
EXT = ("R", ["lamprey", ("J", ["shark", ("B", [
    ("N1", ["fish1", ("N2", ["fish2", ("N3", ["fish3", ("N4", ["fish4", ("N5", ["fish5", "trout"])])])])]),
    ("T", ["frog", "human"])])])])
EXS = {"R": -5.0, "J": -4.3, "B": -3.6, "N1": -3.0, "N2": -2.5, "N3": -2.0, "N4": -1.5, "N5": -1.0, "T": -1.2}


class S05Count(SpokenScene):
    def construct(self):
        tr = Tree(flips={"T", "B"})
        self.add(tr.g)
        self.at("Do not count nodes")
        nc = tag("counting nodes?", RED, 28).move_to([1.9, 1.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(nc), run_time=0.5)
        self.at("number of nodes")
        p1, p2 = tr.trace("trout", "B", w=7), tr.trace("human", "B", w=7)
        self.play(Create(p1), Create(p2), Indicate(tr.nd["T"], color=YELLOW, scale_factor=2.5), run_time=0.9)
        self.at("which other species")
        dep = tag("depends on which\nspecies are sampled", YELLOW, 26).move_to([1.9, 0.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(dep), run_time=0.5)
        self.at("five more fish")
        names = {f"fish{i}": "fish" for i in range(1, 6)}
        colors = {f"fish{i}": GREY for i in range(1, 6)}
        ex = Tree(EXT, xs=EXS, top=2.8, gap=0.62, tip_names=names, tip_color=colors)
        self.play(FadeOut(tr.g), FadeOut(nc), FadeOut(p1), FadeOut(p2), FadeOut(dep), FadeIn(ex.g), run_time=1.2)
        rg = ring(ex.pos["B"], YELLOW, 0.3)
        t1, t2 = ex.trace("trout", "B", w=7), ex.trace("human", "B", w=7)
        self.at("the count between")
        self.play(Create(t1), Create(t2), run_time=0.8)
        self.play(*[Indicate(ex.nd[n], color=YELLOW, scale_factor=2.5) for n in ("N5", "N4", "N3", "N2", "N1")], run_time=0.8)
        rs = tag("more nodes between them", YELLOW, 26).move_to([1.9, 0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(rs), run_time=0.4)
        self.at("has not moved")
        self.play(Create(rg), run_time=0.5)
        mm = tag("same ancestor: B", YELLOW, 26).move_to([1.9, -0.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(mm), run_time=0.4)
        self.at("more evolved")
        t0 = Tree()
        self.play(FadeOut(ex.g), FadeOut(t1), FadeOut(t2), FadeOut(rg), FadeOut(rs), FadeOut(mm), FadeIn(t0.g), run_time=0.8)
        me = tag("more evolved", RED, 28).move_to([1.9, t0.pos["human"][1], 0], aligned_edge=LEFT)
        self.play(FadeIn(me), Create(strike(me)), run_time=0.6)
        self.at("each been evolving")
        pb, pt = t0.pos["B"], t0.pos
        a1 = Arrow([pb[0], pt["trout"][1], 0], [pt["trout"][0] - 0.1, pt["trout"][1], 0], buff=0, color=YELLOW, stroke_width=6)
        a2 = Arrow([pb[0], pt["human"][1], 0], [pt["human"][0] - 0.1, pt["human"][1], 0], buff=0, color=YELLOW, stroke_width=6)
        since = tag("same time since B", YELLOW, 26).move_to([1.9, 0.3, 0], aligned_edge=LEFT)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(since), run_time=0.9)
        self.at("primitive animals")
        lam = t0.pos["lamprey"]
        pr = tag("primitive", RED, 28).move_to([1.9, lam[1], 0], aligned_edge=LEFT)
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(since), FadeIn(pr), Create(strike(pr)), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        tr = Tree()
        rg = ring(tr.pos["B"], YELLOW, 0.34)
        self.add(tr.g)
        self.at("hypothesis")
        hyp = tag("a tree is a hypothesis about ancestry", TEAL, 28).move_to([0, 3.3, 0])
        self.play(FadeIn(hyp), run_time=0.6)
        self.at("Nobody watched")
        nw = tag("nobody watched the lineages split", GREY, 26).move_to([0, -3.2, 0])
        self.play(FadeIn(nw), *[Indicate(tr.nd[n], color=YELLOW, scale_factor=2.5) for n in ("R", "J", "B", "T")], run_time=1.4)
        self.at("estimated from characters")
        tst = tag("estimated from sequences; testable", GREY, 24).next_to(hyp, DOWN, buff=0.15)
        self.play(FadeIn(tst), run_time=0.6)
        self.at("keep one rule")
        self.play(FadeOut(hyp), FadeOut(tst), FadeOut(nw), run_time=0.4)
        self.at("Find the most recent")
        self.play(Create(rg), run_time=0.6)
        rule = tag("find the most recent common ancestor", YELLOW, 30).move_to([0, -3.2, 0])
        self.play(FadeIn(rule), run_time=0.5)
        self.at("how the tips sit")
        cur = tr
        for fl in [{"R"}, {"R", "J", "T"}, {"J", "B"}]:
            nt = Tree(flips=fl)
            self.play(Transform(tr.g, nt.g), rg.animate.move_to(nt.pos["B"]), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Judge relatedness by the most recent common ancestor."
