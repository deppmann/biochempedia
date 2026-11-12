"""Reading phylogenetic trees: relatedness lives at the nodes (the most recent common ancestor).

ONE WORLD (kept for the whole film): a horizontal tree, root left, five tips right, time arrow below.
COLOUR MAP
  branches        light charcoal      node B   GOLD (trout-human most recent common ancestor)
  node J          GREY-BLUE           nodes R and T   plain
  derived state   TEAL                outgroup   violet
  misreading      RED                 unchanged  GREEN
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

STRUCT = ("R", ["lamprey", ("J", ["shark", ("B", ["trout", ("T", ["frog", "human"])])])])
NX = {"R": -5.8, "J": -4.3, "B": -2.8, "T": -1.3}
TIPX = 0.3
TOP, GAP = 2.7, 1.2
BRC = "#B8BDC9"     # branches
JC = "#7FA3C7"      # node J, grey-blue
ORG = "#B79CED"     # outgroup tint
NODE_COL = {"B": GOLD, "J": JC, "R": TEXT, "T": TEXT}
SP = {"lamprey": "#A9A3C9", "shark": "#8E9AAF", "trout": "#E08A5B", "frog": "#6BBF59", "human": "#E6C9A8"}
PANEL = "#1a1d27"


def icon(name, s=1.0):
    c = SP[name]
    if name == "lamprey":
        body = FunctionGraph(lambda x: 0.09 * np.sin(10 * x), x_range=[-0.45, 0.4], color=c, stroke_width=10)
        g = VGroup(body, Dot([0.4, 0.09 * np.sin(4.0) + 0.04, 0], radius=0.035, color=BG))
    elif name == "shark":
        g = VGroup(Ellipse(width=0.72, height=0.3, fill_color=c, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.06),
                   Polygon([-0.28, 0, 0], [-0.5, 0.17, 0], [-0.5, -0.17, 0], fill_color=c, fill_opacity=1, stroke_width=0),
                   Polygon([-0.02, 0.12, 0], [0.14, 0.12, 0], [0.0, 0.3, 0], fill_color=c, fill_opacity=1, stroke_width=0),
                   Dot([0.3, 0.04, 0], radius=0.035, color=BG))
    elif name == "trout":
        g = VGroup(Ellipse(width=0.64, height=0.32, fill_color=c, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.06),
                   Polygon([-0.24, 0, 0], [-0.46, 0.17, 0], [-0.46, -0.17, 0], fill_color=c, fill_opacity=1, stroke_width=0),
                   Dot([0.26, 0.04, 0], radius=0.035, color=BG),
                   Dot([-0.02, 0.0, 0], radius=0.03, color=BG), Dot([0.1, -0.06, 0], radius=0.03, color=BG),
                   Dot([-0.1, 0.06, 0], radius=0.03, color=BG))
    elif name == "frog":
        g = VGroup(Ellipse(width=0.62, height=0.34, fill_color=c, fill_opacity=1, stroke_width=0),
                   Circle(radius=0.09, fill_color=c, fill_opacity=1, stroke_width=0).move_to([0.14, 0.2, 0]),
                   Circle(radius=0.09, fill_color=c, fill_opacity=1, stroke_width=0).move_to([-0.14, 0.2, 0]),
                   Dot([0.14, 0.21, 0], radius=0.035, color=BG), Dot([-0.14, 0.21, 0], radius=0.035, color=BG),
                   Ellipse(width=0.24, height=0.1, fill_color=c, fill_opacity=1, stroke_width=0).move_to([0.3, -0.18, 0]),
                   Ellipse(width=0.24, height=0.1, fill_color=c, fill_opacity=1, stroke_width=0).move_to([-0.3, -0.18, 0]))
    else:  # human
        g = VGroup(Circle(radius=0.1, fill_color=c, fill_opacity=1, stroke_width=0).move_to([0, 0.23, 0]),
                   RoundedRectangle(corner_radius=0.06, width=0.22, height=0.3, fill_color=c, fill_opacity=1, stroke_width=0).move_to([0, -0.02, 0]),
                   Line([-0.17, 0.08, 0], [-0.17, -0.12, 0], color=c, stroke_width=6), Line([0.17, 0.08, 0], [0.17, -0.12, 0], color=c, stroke_width=6),
                   Line([-0.06, -0.17, 0], [-0.06, -0.33, 0], color=c, stroke_width=6), Line([0.06, -0.17, 0], [0.06, -0.33, 0], color=c, stroke_width=6))
    return g.scale(s)


def rows(n, flips, out):
    if isinstance(n, str):
        out.append(n)
        return
    name, kids = n
    for k in (kids[::-1] if name in flips else kids):
        rows(k, flips, out)


class Tree:
    """Rectangular cladogram. Rotating a node only reorders rows; every part keeps its identity so
    Transform can swing one drawing into the other."""

    def __init__(self, flips=()):
        self.flips = tuple(flips)
        order = []
        rows(STRUCT, set(flips), order)
        self.pos, self.parent = {}, {}
        for i, nm in enumerate(order):
            self.pos[nm] = np.array([TIPX, TOP - i * GAP, 0.0])
        self._internal(STRUCT)
        self.br, self.nd, self.tp, self.kids = {}, {}, {}, {}
        self._build(STRUCT)

    def _internal(self, n):
        if isinstance(n, str):
            return self.pos[n]
        name, kids = n
        ys = []
        for k in kids:
            kn = k if isinstance(k, str) else k[0]
            self.parent[kn] = name
            ys.append(self._internal(k)[1])
        self.pos[name] = np.array([NX[name], (min(ys) + max(ys)) / 2, 0.0])
        return self.pos[name]

    def _build(self, n):
        if isinstance(n, str):
            y = self.pos[n][1]
            ic = icon(n).move_to([TIPX + 0.7, y, 0])
            lab = T(n, 28).move_to([TIPX + 1.4, y, 0], aligned_edge=LEFT)
            self.tp[n] = VGroup(ic, lab)
            return
        name, kids = n
        p = self.pos[name]
        kn = [k if isinstance(k, str) else k[0] for k in kids]
        self.kids[name] = kn
        ys = [self.pos[k][1] for k in kn]
        lines = [Line([p[0], min(ys), 0], [p[0], max(ys), 0])]
        lines += [Line([p[0], self.pos[k][1], 0], [self.pos[k][0], self.pos[k][1], 0]) for k in kn]
        if name == "R":
            lines.append(Line([p[0] - 0.6, p[1], 0], [p[0], p[1], 0]))
        self.br[name] = VGroup(*lines).set_stroke(BRC, 5)
        col = NODE_COL[name]
        self.nd[name] = VGroup(Dot(p, radius=0.15, color=col), T(name, 30, col, weight=BOLD).move_to(p + np.array([-0.33, 0.33, 0])))
        for k in kids:
            self._build(k)

    def mobs(self, nodes=True, tips=True):
        out = list(self.br.values())
        if nodes:
            out += list(self.nd.values())
        if tips:
            out += list(self.tp.values())
        return out

    def bottom(self, n):
        return min(self.pos[k][1] for k in self.kids[n])

    def trace(self, tip, target, color, w=10):
        pts = [self.pos[tip]]
        cur = tip
        while cur != target:
            par = self.parent[cur]
            pts.append(np.array([self.pos[par][0], self.pos[cur][1], 0.0]))
            pts.append(self.pos[par])
            cur = par
        return VMobject().set_points_as_corners(pts).set_stroke(color, w)

    def flip(self, sc, flips, run_time=2.6, arc=0.5, extra=()):
        new = Tree(flips)
        an = [Transform(self.br[k], new.br[k]) for k in self.br]
        an += [Transform(self.nd[k], new.nd[k]) for k in self.nd]
        an += [Transform(self.tp[k], new.tp[k], path_arc=arc) for k in self.tp]
        sc.play(*an, *extra, run_time=run_time)
        self.pos, self.parent, self.flips = new.pos, new.parent, new.flips


def ind(m, scale_factor=1.2, color=TEXT, **kw):
    return Indicate(m, scale_factor=scale_factor, color=color, **kw)


def make_flow(tree, n_per=4, speed=1.8):
    """Slow ambient flow: small dots travel root to tip along every lineage (time runs left to right)."""
    paths = []
    for t in tree.tp:
        chain = [t]
        while chain[-1] != "R":
            chain.append(tree.parent[chain[-1]])
        chain = chain[::-1]
        pts = [np.array([NX["R"] - 0.6, tree.pos["R"][1], 0.0]), tree.pos["R"].copy()]
        for a, b in zip(chain[:-1], chain[1:]):
            pts += [np.array([tree.pos[a][0], tree.pos[b][1], 0.0]), tree.pos[b].copy()]
        P = np.array(pts)
        seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
        paths.append((P, np.concatenate([[0], np.cumsum(seg)])))
    dots, meta = VGroup(), []
    for i, (P, c) in enumerate(paths):
        L = c[-1]
        for k in range(n_per):
            d = Dot(radius=0.09, color=TEXT).set_opacity(0.85)
            dots.add(d)
            meta.append((P, c, L, (k + 0.3 * i) / n_per * L))
    clock = [0.0]

    def upd(g, dt):
        clock[0] += dt
        for d, (P, c, L, ph) in zip(g, meta):
            s_ = (ph + speed * clock[0]) % L
            d.move_to([np.interp(s_, c, P[:, 0]), np.interp(s_, c, P[:, 1]), 0])
    dots.add_updater(upd)
    dots.set_z_index(1)
    return dots


def axis():
    ar = Arrow([-6.2, -3.0, 0], [0.5, -3.0, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25, max_tip_length_to_length_ratio=0.2)
    old = T("older", 28).move_to([-6.4, -3.46, 0], aligned_edge=LEFT)
    now = T("today", 28).move_to([0.7, -3.46, 0], aligned_edge=RIGHT)
    return VGroup(ar, old, now)


def ring(p, color, r=0.32):
    return Circle(radius=r, stroke_color=color, stroke_width=6).move_to(p)


def tick(tree, n, color):
    x = tree.pos[n][0]
    d = DashedLine([x, tree.bottom(n), 0], [x, -3.0, 0], dash_length=0.12, color=color, stroke_width=4)
    t = Line([x, -2.84, 0], [x, -3.16, 0], color=color, stroke_width=8)
    return VGroup(d, t)


def tag(text, at, color=TEXT, leader=None, size=28, edge=LEFT):
    lab = T(text, size, color).move_to(at, aligned_edge=edge)
    g = VGroup(lab)
    if leader is not None:
        g.add(DashedLine(leader[0], leader[1], dash_length=0.1, color=color, stroke_width=3))
    return g


# tag spots next to each node (free regions of the drawing)
def node_tag(tree, n, text, color=TEXT):
    p = tree.pos[n]
    spots = {"R": ([-4.95, 2.12, 0], LEFT, [-4.95 - 0.05, 2.0, 0]),
             "J": ([-4.0, 0.9, 0], LEFT, [-4.05, 0.8, 0]),
             "B": ([-2.55, -0.3, 0], LEFT, [-2.6, -0.3, 0]),
             "T": ([-1.65, -2.4, 0], RIGHT, [-1.6, -2.3, 0])}
    at, edge, lead_end = spots[n]
    return tag(text, at, color, leader=(p + (np.array([-0.0, 0, 0])), np.array(lead_end)), edge=edge)


def card(name, x, y=-0.2):
    box = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.3, stroke_color=GREY, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
    ic = icon(name, 2.4).move_to([x, y + 0.4, 0])
    lab = T(name, 34).move_to([x, y - 1.05, 0])
    return VGroup(box, ic, lab)


def clade_box(tree, color=GOLD):
    ys = [tree.pos[k][1] for k in ("trout", "frog", "human")]
    top, bot = max(ys) + 0.45, min(ys) - 0.45
    return RoundedRectangle(corner_radius=0.25, width=6.8, height=top - bot, stroke_color=color, stroke_width=5).move_to([-0.1, (top + bot) / 2, 0])


def qcard(x=5.0, y=-0.3):
    txt = T("Spin node B.\nDoes trout's\nclosest relative\nchange?", 28, TEXT, line_spacing=0.9)
    box = RoundedRectangle(corner_radius=0.2, width=txt.width + 0.5, height=txt.height + 0.5, stroke_color=GOLD, stroke_width=4, fill_color=PANEL, fill_opacity=1)
    g = VGroup(box, txt)
    return g.move_to([x, y, 0])


def curl(p, color=TEXT, r=0.88):
    a = Arc(radius=r, start_angle=-1.0, angle=2.6, color=color, stroke_width=6).move_to(p)
    a.add_tip(tip_length=0.22)
    return a


class Base(SpokenScene):
    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def put(self, tree, nodes=True, tips=True, flow=True):
        self.add(*tree.mobs(nodes, tips))
        self.flow = None
        if flow:
            self.flow = make_flow(tree)
            self.add(self.flow)

    def flip(self, tr, flips, run_time=2.6, arc=0.5, extra=()):
        """Rotate nodes; the flow dots are paused during the swing and rebuilt on the new drawing."""
        ex = list(extra)
        if self.flow is not None:
            self.flow.clear_updaters()
            ex.append(FadeOut(self.flow))
        tr.flip(self, flips, run_time=run_time, arc=arc, extra=ex)
        self.flow = make_flow(tr)
        self.add(self.flow)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Reading Phylogenetic Trees"
    TITLE = "Relatedness Lives at the Nodes"


# ---------------------------------------------------------------------------------------------
def hook_final():
    cs = {"shark": card("shark", -1.6), "trout": card("trout", 1.6), "human": card("human", 5.0)}
    br = VGroup(Line([-3.1, 1.8, 0], [3.1, 1.8, 0], color=TEXT, stroke_width=5),
                Line([-3.1, 1.8, 0], [-3.1, 1.55, 0], color=TEXT, stroke_width=5),
                Line([3.1, 1.8, 0], [3.1, 1.55, 0], color=TEXT, stroke_width=5))
    lab = T("look alike", 34).move_to([0, 2.45, 0])
    q = T("?", 90, GOLD, weight=BOLD).move_to([5.0, 2.45, 0])
    return cs, br, lab, q


class S01Hook(Base):
    def construct(self):
        cs = {"shark": card("shark", -4.6), "trout": card("trout", 0), "human": card("human", 4.6)}
        self.at("a trout", lead=0.0)
        self.play(FadeIn(cs["trout"], shift=UP * 0.4), run_time=0.8)
        self.at("to a shark")
        self.play(FadeIn(cs["shark"], shift=UP * 0.4), run_time=0.8)
        self.at("or to you")
        self.play(FadeIn(cs["human"], shift=UP * 0.4), run_time=0.8)
        self.at("the two fish look alike")
        self.play(cs["shark"].animate.shift(RIGHT * 3.0), cs["trout"].animate.shift(RIGHT * 1.6),
                  cs["human"].animate.shift(RIGHT * 0.4), run_time=1.4)
        _, br, lab, q = hook_final()
        self.at("look alike", lead=-0.3)
        self.play(Create(br), FadeIn(lab, shift=DOWN * 0.15), run_time=1.0)
        self.at("a tree gives")
        self.play(FadeIn(q, scale=1.8), run_time=0.7)
        self.play(ind(q, scale_factor=1.3, color=GOLD), run_time=0.9)
        self.play(ind(cs["human"][1], scale_factor=1.15), run_time=0.9)
        self.finish()


class S02Tree(Base):
    def construct(self):
        cs, br, lab, q = hook_final()
        tr = Tree()
        self.add(*cs.values(), br, lab, q)
        self.wait(0.3)
        anims = [FadeOut(br), FadeOut(lab), FadeOut(q)]
        for n in ("shark", "trout", "human"):
            c = cs[n]
            anims += [FadeOut(c[0]), ReplacementTransform(c[1], tr.tp[n][0]), ReplacementTransform(c[2], tr.tp[n][1])]
        anims += [FadeIn(tr.tp["lamprey"], shift=LEFT * 3), FadeIn(tr.tp["frog"], shift=LEFT * 3)]
        self.play(*anims, run_time=2.4)
        self.at("a hypothesis about", lead=0.0)
        grown = [VGroup(*[ln.copy().reverse_points() for ln in tr.br[n]]) for n in ["T", "B", "J", "R"]]
        self.play(LaggedStart(*[Create(c) for c in grown], lag_ratio=0.8), run_time=2.8)
        self.remove(*grown)
        self.add(*tr.br.values())
        self.flow = make_flow(tr)
        self.add(self.flow)
        self.at("the living species")
        tl = DashedLine([TIPX, 3.15, 0], [TIPX, -2.5, 0], dash_length=0.12, color=TEXT, stroke_width=3)
        tl_lab = T("tips", 30, TEXT).move_to([TIPX, 3.4, 0])
        dots = VGroup(*[Dot([TIPX, tr.pos[n][1], 0], radius=0.11, color=BRC) for n in tr.tp])
        self.play(Create(tl), FadeIn(tl_lab, shift=DOWN * 0.1), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=1.4)
        self.at("here are five")
        for nm in ["lamprey", "shark", "trout", "frog", "human"]:
            self.at(nm, lead=0.1)
            self.play(ind(tr.tp[nm], scale_factor=1.25), run_time=0.5)
        self.at("nobody watched")
        self.play(FadeOut(tl), FadeOut(tl_lab), run_time=0.4)
        self.at("estimated from characters")
        seq = "".join(np.random.RandomState(4).choice(list("ACGT"), 34))
        strip = M(seq, 30, TEAL).move_to([-2.0, -3.4, 0])
        slab = T("estimated from sequences", 28, TEXT).move_to([-2.0, -2.85, 0])
        self.play(FadeIn(slab, shift=UP * 0.1), FadeIn(strip), run_time=0.8)
        self.at("protein sequences", lead=0.1)
        self.play(ind(slab, scale_factor=1.12, color=TEAL), run_time=0.8)
        self.finish()
        strip.clear_updaters()


class S03Nodes(Base):
    def construct(self):
        tr = Tree()
        self.put(tr, nodes=False)
        self.wait(0.1)
        self.play(GrowFromCenter(tr.nd["R"][0]), FadeIn(tr.nd["R"][1]), run_time=0.5)
        self.at("a branch")
        self.play(GrowFromCenter(tr.nd["J"][0]), FadeIn(tr.nd["J"][1]), run_time=0.5)
        self.at("splits")
        self.play(GrowFromCenter(tr.nd["B"][0]), FadeIn(tr.nd["B"][1]), run_time=0.5)
        self.at("internal node")
        self.play(GrowFromCenter(tr.nd["T"][0]), FadeIn(tr.nd["T"][1]), run_time=0.5)
        self.at("inferred ancestor", lead=0.3)
        t1 = node_tag(tr, "R", "inferred ancestor")
        self.play(FadeIn(t1), run_time=0.5)
        t2 = node_tag(tr, "J", "inferred ancestor")
        self.at("of every lineage", lead=0.9)
        self.play(ReplacementTransform(t1, t2), run_time=0.6)
        self.at("descending from it", lead=0.4)
        t3 = node_tag(tr, "J", "descends from J", JC)
        sub = [tr.br["J"], tr.br["B"], tr.br["T"]]
        self.play(ReplacementTransform(t2, t3), ind(tr.nd["J"][0], scale_factor=2.0, color=JC),
                  *[g.animate.set_stroke(JC, 8) for g in sub], run_time=1.0)
        self.play(*[g.animate.set_stroke(BRC, 5) for g in sub], run_time=1.0)
        self.at("the root", lead=0.3)
        t4 = node_tag(tr, "R", "root")
        self.play(FadeOut(t3), FadeIn(t4), ind(tr.nd["R"][0], scale_factor=2.2, color=TEXT), run_time=1.0)
        self.at("ancestor of everything", lead=0.3)
        self.play(*[g.animate.set_stroke(TEXT, 9) for g in tr.br.values()], run_time=0.8)
        self.play(*[g.animate.set_stroke(BRC, 5) for g in tr.br.values()], run_time=1.0)
        self.play(ind(tr.nd["R"][0], scale_factor=2.2, color=TEXT), run_time=0.8)
        self.finish()


class S04Outgroup(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        self.wait(0.2)
        lamb = tr.br["R"][1]
        self.play(lamb.animate.set_stroke(ORG, 10), tr.tp["lamprey"][1].animate.set_color(ORG), run_time=0.8)
        self.at("out group", lead=0.1)
        tg = tag("outgroup", [-3.2, 3.2, 0], ORG, size=32)
        self.play(FadeIn(tg, shift=DOWN * 0.1), run_time=0.7)
        self.at("assumed to lie outside")
        rect = RoundedRectangle(corner_radius=0.25, width=8.3, height=4.7, stroke_color=GREY, stroke_width=4).move_to([-0.55, -0.28, 0])
        self.play(Create(rect), run_time=1.6)
        self.at("the root tells you")
        ax = axis()
        self.play(FadeOut(rect), FadeOut(tg), lamb.animate.set_stroke(BRC, 5), tr.tp["lamprey"][1].animate.set_color(TEXT), run_time=0.6)
        self.play(Create(ax[0]), run_time=1.4, rate_func=linear)
        self.at("older", lead=0.1)
        self.play(FadeIn(ax[1]), FadeIn(ax[2]), run_time=0.6)
        self.at("so for two nodes")
        tj = tick(tr, "J", JC)
        self.at("nodes", lead=0.0)
        self.play(Create(tj[0]), FadeIn(tj[1]), run_time=0.9)
        tb = tick(tr, "B", GOLD)
        self.at("one lineage", lead=0.1)
        self.play(Create(tb[0]), FadeIn(tb[1]), run_time=0.9)
        self.at("which is more recent")
        self.play(ind(tb[1], scale_factor=1.8, color=GOLD), run_time=0.9)
        self.play(ind(tj[1], scale_factor=1.8, color=JC), run_time=0.9)
        self.play(ind(tb[1], scale_factor=1.8, color=GOLD), run_time=0.9)
        self.finish()


class S05Trace(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        ax = axis()
        self.add(ax)
        self.at("trace trout and shark")
        a, b = tr.trace("trout", "J", JC), tr.trace("shark", "J", JC)
        self.play(Create(a), Create(b), run_time=2.2, rate_func=linear)
        self.at("meet", lead=0.1)
        rj = ring(tr.pos["J"], JC)
        self.play(FadeIn(rj, scale=2.0), run_time=0.6)
        self.at("they meet at node j", lead=0.1)
        self.play(ind(rj, scale_factor=1.5, color=JC), ind(tr.nd["J"][0], scale_factor=2.0, color=JC), run_time=1.2)
        self.at("then trace trout and human", lead=0.2)
        self.play(a.animate.set_stroke(JC, 10, opacity=0.35), b.animate.set_stroke(JC, 10, opacity=0.35), run_time=0.5)
        c, d = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD)
        self.play(Create(c), Create(d), run_time=2.0, rate_func=linear)
        self.at("they meet at node b", lead=0.1)
        rb = ring(tr.pos["B"], GOLD)
        self.play(FadeIn(rb, scale=2.0), run_time=0.6)
        self.play(ind(rb, scale_factor=1.5, color=GOLD), ind(tr.nd["B"][0], scale_factor=2.0, color=GOLD), run_time=1.2)
        self.play(ind(rj, scale_factor=1.4, color=JC), run_time=0.9)
        self.finish()


class S06Mrca(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        ax = axis()
        self.add(ax)
        self.at("node b descends", lead=0.0)
        seg = tr.br["J"][2].copy().set_stroke(JC, 11)
        self.play(ShowPassingFlash(seg, time_width=1.0), run_time=1.0)
        tj = tick(tr, "J", JC)
        self.play(Create(tj[0]), FadeIn(tj[1]), run_time=0.8)
        tb = tick(tr, "B", GOLD)
        self.play(Create(tb[0]), FadeIn(tb[1]), run_time=0.8)
        self.at("so b is more recent")
        mr = T("more recent", 28, TEXT).move_to([-1.9, -3.46, 0])
        self.play(FadeIn(mr, shift=UP * 0.1), ind(tb[1], scale_factor=1.8, color=GOLD), run_time=0.9)
        self.at("b is the most recent common ancestor")
        rb = ring(tr.pos["B"], GOLD)
        ml = T("most recent common ancestor (MRCA)", 28, GOLD).move_to([-2.2, -0.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(rb, scale=2.0), FadeIn(ml, shift=RIGHT * 0.2), run_time=0.9)
        self.at("of trout and human", lead=0.1)
        gt, gh = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD)
        self.play(ShowPassingFlash(gt, time_width=0.8), ShowPassingFlash(gh, time_width=0.8), run_time=1.4)
        self.at("that is the latest node")
        self.play(*[g.animate.set_stroke(GOLD, 9) for g in (tr.br["B"], tr.br["T"])], run_time=0.8)
        self.play(*[g.animate.set_stroke(BRC, 5) for g in (tr.br["B"], tr.br["T"])], run_time=0.9)
        self.play(ind(rb, scale_factor=1.4, color=GOLD), run_time=0.9)
        self.at("shark does not descend")
        self.play(tr.tp["shark"].animate.set_opacity(0.3), tr.br["J"][1].animate.set_stroke(BRC, 5, opacity=0.35), run_time=1.0)
        self.play(ind(tr.nd["J"][0], scale_factor=2.0, color=JC), run_time=0.9)
        self.finish()


class S07Answer(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        self.add(axis())
        self.at("a trout is more closely related")
        gt, gh = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD)
        self.play(Create(gt), Create(gh), run_time=1.6, rate_func=linear)
        self.at("than to a shark", lead=0.1)
        jt, js = tr.trace("trout", "J", JC), tr.trace("shark", "J", JC)
        self.play(gt.animate.set_stroke(GOLD, 10, opacity=0.4), gh.animate.set_stroke(GOLD, 10, opacity=0.4), Create(jt), Create(js), run_time=1.4, rate_func=linear)
        self.at("it is equally close")
        self.play(FadeOut(jt), FadeOut(js), FadeOut(gt), FadeOut(gh), run_time=0.4)
        yf, yh = tr.pos["frog"][1], tr.pos["human"][1]
        brk = VGroup(Line([3.9, yf, 0], [3.9, yh, 0]), Line([3.9, yf, 0], [3.75, yf, 0]), Line([3.9, yh, 0], [3.75, yh, 0])).set_stroke(GOLD, 5)
        eq = T("equally close\nto trout", 28, GOLD, line_spacing=0.9).move_to([5.4, (yf + yh) / 2, 0])
        self.play(Create(brk), FadeIn(eq, shift=LEFT * 0.2), run_time=1.0)
        self.play(ind(tr.tp["frog"], scale_factor=1.15), ind(tr.tp["human"], scale_factor=1.15), run_time=0.9)
        self.at("a clade is an ancestor")
        self.play(FadeOut(brk), FadeOut(eq), run_time=0.4)
        box = clade_box(tr)
        self.play(Create(box), run_time=2.0)
        self.at("all its descendants", lead=0.1)
        self.play(*[ind(tr.tp[n], scale_factor=1.15) for n in ("trout", "frog", "human")], ind(tr.nd["B"][0], scale_factor=2.0, color=GOLD), run_time=1.0)
        self.at("trout frog and human", lead=0.1)
        for n in ("trout", "frog", "human"):
            self.play(ind(tr.tp[n], scale_factor=1.2), run_time=0.5)
        self.at("form one clade")
        cl = T("clade", 40, GOLD, weight=BOLD).move_to([5.3, -0.9, 0])
        self.play(FadeIn(cl, shift=LEFT * 0.2), run_time=0.7)
        self.play(ind(box, scale_factor=1.03, color=GOLD), run_time=0.9)
        self.finish()


class S08Rotate(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        self.add(axis())
        box = clade_box(tr)
        cl = T("clade", 40, GOLD, weight=BOLD).move_to([5.3, -0.9, 0])
        self.add(box, cl)
        self.at("spin node t", lead=0.1)
        arr = curl(tr.pos["T"], TEXT, r=1.35)
        self.play(Create(arr), ind(tr.nd["T"][0], scale_factor=2.0, color=TEXT), run_time=1.0)
        self.at("like one arm of a mobile")
        self.play(Rotate(arr, angle=-2 * PI, about_point=tr.pos["T"]), run_time=2.4)
        self.at("frog and human swap places", lead=0.2)
        cap = T("rotate a node =\nswap the two\nbranches\nleaving it", 28, TEXT, line_spacing=0.9).move_to([5.2, 1.9, 0])
        self.play(FadeIn(cap, shift=LEFT * 0.2), Rotate(arr, angle=-PI, about_point=tr.pos["T"]), run_time=0.6)
        tr.flip(self, ("T",), run_time=2.4, arc=PI * 0.9)
        self.at("every clade keeps its members")
        self.play(ind(box, scale_factor=1.03, color=GOLD), run_time=1.0)
        self.play(*[ind(tr.tp[n], scale_factor=1.15) for n in ("trout", "frog", "human")], run_time=1.0)
        self.at("so nothing about the history")
        gt, gh, gf = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD), tr.trace("frog", "B", GOLD)
        self.play(ShowPassingFlash(gt, time_width=0.8), ShowPassingFlash(gh, time_width=0.8), ShowPassingFlash(gf, time_width=0.8), run_time=1.5)
        self.play(ind(tr.nd["B"][0], scale_factor=2.0, color=GOLD), run_time=0.9)
        self.finish()


class S09Predict(Base):
    def construct(self):
        tr = Tree(("T",))
        self.put(tr)
        self.add(axis())
        self.at("spin node b", lead=0.1)
        arr = curl(tr.pos["B"], GOLD)
        self.play(Create(arr), ind(tr.nd["B"][0], scale_factor=2.0, color=GOLD), run_time=1.2)
        self.play(Rotate(arr, angle=-PI / 2, about_point=tr.pos["B"]), run_time=0.8)
        self.at("shark will no longer")
        self.play(ind(tr.tp["shark"], scale_factor=1.2), run_time=0.8)
        self.at("sit beside trout", lead=0.1)
        self.play(ind(tr.tp["trout"], scale_factor=1.2), run_time=0.8)
        self.play(ind(tr.tp["shark"], scale_factor=1.2), ind(tr.tp["trout"], scale_factor=1.2), run_time=0.9)
        self.at("does trout's closest")
        q = qcard()
        self.play(FadeIn(q, shift=LEFT * 0.3), run_time=0.8)
        self.play(ind(tr.tp["trout"], scale_factor=1.25, color=GOLD), run_time=0.9)
        self.play(ind(arr, scale_factor=1.15, color=GOLD), run_time=0.9)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        tr = Tree(("T",))
        self.add(*tr.mobs(), make_flow(tr), axis(), curl(tr.pos["B"], GOLD).rotate(-PI / 2, about_point=tr.pos["B"]), qcard())
        base = Circle(radius=0.38, stroke_color=GREY, stroke_width=6).move_to([5.9, -2.8, 0])
        prog = Circle(radius=0.38, stroke_color=GOLD, stroke_width=8).move_to([5.9, -2.8, 0]).rotate(PI / 2).flip(axis=RIGHT)
        self.add(base)
        self.play(Create(prog), run_time=4.6, rate_func=linear)
        self.finish()


class S11Reveal(Base):
    def construct(self):
        tr = Tree(("T",))
        self.put(tr)
        self.add(axis())
        q = qcard()
        arr = curl(tr.pos["B"], GOLD).rotate(-PI / 2, about_point=tr.pos["B"])
        self.add(q, arr)
        self.wait(0.3)
        self.play(FadeOut(q), run_time=0.4)
        self.wait(0.2)
        self.flip(tr, ("T", "B"), run_time=1.6, arc=0.5, extra=[Rotate(arr, angle=-PI, about_point=tr.pos["B"])])
        arr.move_to(tr.pos["B"])
        self.at("but the tree did not")
        stamp = VGroup(RoundedRectangle(corner_radius=0.12, width=2.7, height=0.9, stroke_color=GREEN, stroke_width=5),
                       T("same tree", 34, GREEN, weight=BOLD)).move_to([5.1, 2.3, 0]).rotate(0.12)
        self.play(FadeOut(arr), FadeIn(stamp, scale=1.6), run_time=0.7)
        self.at("trout still meets frog and human")
        ga, gb, gc = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD), tr.trace("frog", "B", GOLD)
        self.play(Create(ga), Create(gb), Create(gc), run_time=2.0, rate_func=linear)
        self.at("at node b", lead=0.1)
        rb = ring(tr.pos["B"], GOLD)
        self.play(FadeIn(rb, scale=2.0), run_time=0.5)
        self.at("and shark at node j", lead=0.1)
        self.play(*[g.animate.set_stroke(GOLD, 10, opacity=0.35) for g in (ga, gb, gc)], run_time=0.4)
        jt, js = tr.trace("trout", "J", JC), tr.trace("shark", "J", JC)
        self.play(Create(jt), Create(js), run_time=1.6, rate_func=linear)
        rj = ring(tr.pos["J"], JC)
        self.play(FadeIn(rj, scale=2.0), run_time=0.5)
        self.at("tips side by side")
        self.play(*[FadeOut(m) for m in (jt, js, ga, gb, gc, rb, rj)], run_time=0.4)
        ys, yh = tr.pos["shark"][1], tr.pos["human"][1]
        brk = VGroup(Line([3.3, ys, 0], [3.3, yh, 0]), Line([3.3, ys, 0], [3.15, ys, 0]), Line([3.3, yh, 0], [3.15, yh, 0])).set_stroke(TEXT, 5)
        sl = T("side by side\non the page", 28, TEXT, line_spacing=0.9).move_to([5.1, (ys + yh) / 2, 0])
        self.play(Create(brk), FadeIn(sl, shift=LEFT * 0.2), ind(tr.tp["shark"], scale_factor=1.2), ind(tr.tp["human"], scale_factor=1.2), run_time=1.4)
        self.at("closest relatives", lead=0.3)
        nl = T("not closest\nrelatives", 28, RED, line_spacing=0.9).move_to([5.1, -0.6, 0])
        self.play(FadeIn(nl, shift=LEFT * 0.2), run_time=0.8)
        self.play(ind(nl, scale_factor=1.12, color=RED), run_time=0.9)
        self.finish()


class S12Evolved(Base):
    def construct(self):
        tr = Tree(("T", "B"))
        self.put(tr)
        self.add(axis())
        self.at("one more misreading", lead=0.0)
        self.wait(0.4)
        self.flip(tr, (), run_time=2.4, arc=0.5)
        self.at("human sits at the end")
        self.play(ind(tr.tp["human"], scale_factor=1.3), run_time=1.0)
        self.at("so is it more evolved")
        ev = T("more evolved?", 28, TEXT).move_to([5.0, tr.pos["human"][1], 0])
        self.play(FadeIn(ev, shift=LEFT * 0.2), run_time=0.8)
        self.at("no")
        sk = Line(ev.get_left() + LEFT * 0.1, ev.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(Create(sk), run_time=0.6)
        self.play(FadeOut(ev), FadeOut(sk), run_time=0.5)
        self.at("every living tip")
        tips = ["lamprey", "shark", "trout", "frog", "human"]
        fl = [tr.trace(n, "R", TEXT, 10) for n in tips]
        self.play(*[ShowPassingFlash(f.reverse_points(), time_width=0.5) for f in fl], run_time=1.8)
        self.at("the same time since the root", lead=0.4)
        dm = T("same time since the root", 28, TEXT).move_to([-3.05, -2.62, 0])
        dl = VGroup(Line([-5.8, -2.62, 0], [-5.45, -2.62, 0]), Line([-0.65, -2.62, 0], [0.3, -2.62, 0]),
                    Line([-5.8, -2.78, 0], [-5.8, -2.46, 0]), Line([0.3, -2.78, 0], [0.3, -2.46, 0])).set_stroke(GOLD, 5)
        self.play(Create(dl), FadeIn(dm), run_time=1.2)
        self.play(*[ShowPassingFlash(f, time_width=0.5) for f in [tr.trace(n, "R", TEXT, 10).reverse_points() for n in tips]], run_time=1.6)
        self.at("lampreys lack jaws", lead=0.1)
        self.play(FadeOut(dl), FadeOut(dm), ind(tr.tp["lamprey"], scale_factor=1.3), run_time=1.0)
        self.at("derived features", lead=0.3)
        disc = VGroup(*[Circle(radius=r, stroke_color=TEAL, stroke_width=5) for r in (0.5, 0.33, 0.16)]).move_to([4.1, 2.7, 0])
        dlab = T("its own\nderived\nfeature", 28, TEAL, line_spacing=0.9).move_to([5.75, 2.55, 0])
        self.play(Create(disc), FadeIn(dlab, shift=LEFT * 0.2), run_time=1.2)
        self.play(ind(disc, scale_factor=1.2, color=TEAL), run_time=0.9)
        self.finish()


class S13Rule(Base):
    def construct(self):
        tr = Tree()
        self.put(tr)
        self.add(axis())
        self.at("characters not whole organisms", lead=0.1)
        self.play(*[ind(tr.tp[n][0], scale_factor=1.3) for n in ("lamprey", "shark", "trout", "frog", "human")], run_time=1.2)
        self.at("ancestral or derived", lead=0.3)
        c1 = chip("ancestral", GREY, 30).move_to([5.1, 2.35, 0])
        c2 = chip("derived", TEAL, 30).move_to([5.1, 1.3, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.7)
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)
        self.at("relatedness is read only at the nodes", lead=0.3)
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        rd = T("Read\nrelatedness\nat the nodes.", 32, GOLD, line_spacing=0.9).move_to([5.1, 0.6, 0])
        self.play(FadeIn(rd, shift=LEFT * 0.2), run_time=0.8)
        for n in ("R", "J", "B", "T"):
            self.play(ind(tr.nd[n][0], scale_factor=2.2, color=NODE_COL[n]), run_time=0.5)
        self.at("find the most recent common ancestor", lead=0.1)
        rb = ring(tr.pos["B"], GOLD)
        gt, gh = tr.trace("trout", "B", GOLD), tr.trace("human", "B", GOLD)
        self.play(FadeIn(rb, scale=2.0), Create(gt), Create(gh), run_time=1.6)
        self.play(ind(rb, scale_factor=1.5, color=GOLD), run_time=0.9)
        self.at("ignore how the drawing")
        self.play(FadeOut(gt), FadeOut(gh), FadeOut(rd), *[tr.tp[n].animate.set_opacity(0.4) for n in tr.tp], run_time=0.8)
        dr = T("drawing only", 30, TEXT).move_to([5.1, 0.3, 0])
        self.play(FadeIn(dr, shift=LEFT * 0.2), run_time=0.5)
        self.flip(tr, ("T", "B"), run_time=2.4, arc=0.5, extra=[rb.animate.move_to(Tree(("T", "B")).pos["B"])])
        self.play(ind(rb, scale_factor=1.3, color=GOLD), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Relatedness lives in the most recent common ancestor."
