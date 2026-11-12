"""Reading phylogenetic trees, film 2: change lives on the branches.

ONE WORLD (same as film 1): horizontal tree, root left, five tips right, time arrow below.
COLOUR MAP (film 1's, plus states)
  branches        light charcoal      node B   GOLD (trout-human most recent common ancestor)
  node J          GREY-BLUE           nodes R and T   plain
  derived state   TEAL (gain tick)    ancestral / absent state   GREY (loss tick)
  outgroup        violet              convergence / labels   TEXT
"""
import importlib.util
import os
from pathlib import Path
import numpy as np
from bp_style import *  # noqa: F401,F403


def _film1():
    here = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
    spec = importlib.util.spec_from_file_location("film1_scenes", here.parent / "scenes.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


F1 = _film1()
Tree, icon, make_flow, axis, ind, tag, ring = F1.Tree, F1.icon, F1.make_flow, F1.axis, F1.ind, F1.tag, F1.ring
BRC, JC, ORG, NODE_COL, SP, PANEL, TIPX = F1.BRC, F1.JC, F1.ORG, F1.NODE_COL, F1.SP, F1.PANEL, F1.TIPX
BX = 3.6      # badge column
RC = 5.45     # right column centre


# ---------------------------------------------------------------------------------------------
def jaw_glyph(r, col):
    up = Arc(radius=r * 0.62, start_angle=0.45, angle=PI - 0.9, color=col, stroke_width=5).shift(UP * r * 0.12)
    lo = Arc(radius=r * 0.62, start_angle=PI + 0.45, angle=PI - 0.9, color=col, stroke_width=5).shift(DOWN * r * 0.12)
    return VGroup(up, lo)


def badge(state, kind="x", r=0.3, fs=28):
    """state True = derived (TEAL), False = ancestral/absent (GREY), None = neutral ring."""
    col = TEXT if state is None else (TEAL if state else GREY)
    c = Circle(radius=r, stroke_color=col, stroke_width=4 if state is None else 0.01,
               fill_color=col, fill_opacity=0 if state is None else 1)
    gc = col if state is None else BG
    g = jaw_glyph(r, gc) if kind == "jaw" else T("X", fs, gc, weight=BOLD)
    s = Line([-r * .62, -r * .62, 0], [r * .62, r * .62, 0], color=BG, stroke_width=6)
    s.set_opacity(1 if state is False else 0)
    b = VGroup(c, g, s)
    b.set_z_index(3)
    return b


def tally(txt, w=2.6):
    t = M(txt, 28, TEXT)
    box = RoundedRectangle(corner_radius=0.15, width=max(w, t.width + 0.5), height=0.8, stroke_color=GREY,
                           stroke_width=3, fill_color=PANEL, fill_opacity=1)
    g = VGroup(box, t.move_to(box))
    g.set_z_index(6)
    return g


class Geo:
    """Maps the film-1 tree into the full frame (x0=None) or into a small panel starting at x0."""

    def __init__(self, tr, x0=None):
        self.tr, self.x0, self.mini = tr, x0, x0 is not None
        self.r, self.fs = (0.24, 22) if self.mini else (0.3, 28)
        self.ew, self.tw, self.tl = (6, 6, 0.32) if self.mini else (9, 8, 0.32)

    def f(self, p):
        if not self.mini:
            return np.array([p[0], p[1], 0.0])
        return np.array([self.x0 + (p[0] + 6.4) * 0.42, 0.4 + (p[1] - 0.3) * 0.7, 0.0])

    @property
    def bx(self):
        return self.x0 + 5.45 if self.mini else BX

    def P(self, n):
        return self.f(self.tr.pos[n])

    def mid(self, c):
        return (self.tr.pos[self.tr.parent[c]][0] + self.tr.pos[c][0]) / 2

    def edge(self, c, col, part="all", cut=None):
        tr = self.tr
        p = tr.parent[c]
        px, py = tr.pos[p][0], tr.pos[p][1]
        cx, cy = tr.pos[c][0], tr.pos[c][1]
        if part == "all":
            pts = [(px, py), (px, cy), (cx, cy)]
        elif part == "pre":
            pts = [(px, py), (px, cy), (cut, cy)]
        else:
            pts = [(cut, cy), (cx, cy)]
        m = VMobject().set_points_as_corners([self.f(np.array([x, y, 0.0])) for x, y in pts]).set_stroke(col, self.ew)
        m.set_z_index(1)
        return m

    def tick(self, c, col):
        x, y = self.mid(c), self.tr.pos[c][1]
        m = Line(self.f(np.array([x, y - self.tl, 0.0])), self.f(np.array([x, y + self.tl, 0.0])), color=col, stroke_width=self.tw)
        m.set_z_index(3)
        return m

    def trace(self, tip, target, col, w=None):
        tr = self.tr
        pts = [tr.pos[tip]]
        cur = tip
        while cur != target:
            par = tr.parent[cur]
            pts.append(np.array([tr.pos[par][0], tr.pos[cur][1], 0.0]))
            pts.append(tr.pos[par])
            cur = par
        m = VMobject().set_points_as_corners([self.f(p) for p in pts]).set_stroke(col, w or self.ew + 2)
        m.set_z_index(1)
        return m

    def badge(self, tip, state, kind="x"):
        return badge(state, kind, self.r, self.fs).move_to([self.bx, self.P(tip)[1], 0])


def mini_parts(tr, g):
    out = {"br": {}, "nd": {}, "tp": {}}
    for n, grp in tr.br.items():
        out["br"][n] = VGroup(*[Line(g.f(l.get_start()), g.f(l.get_end())).set_stroke(BRC, 3.5) for l in grp])
    for n in tr.nd:
        p, col = g.P(n), NODE_COL[n]
        out["nd"][n] = (Dot(p, radius=0.11, color=col), T(n, 24, col, weight=BOLD).move_to(p + np.array([-0.24, 0.26, 0])))
    for n in tr.tp:
        p = g.P(n)
        out["tp"][n] = (icon(n, 0.8).move_to(p + RIGHT * 0.5), T(n, 22).move_to(p + RIGHT * 0.95, aligned_edge=LEFT))
    return out


def parts_items(parts):
    return [*parts["br"].values(), *[x for v in parts["nd"].values() for x in v], *[x for v in parts["tp"].values() for x in v]]


def mini_flow(tr, g, n_per=4, speed=2.2):
    fl = make_flow(tr, n_per=n_per, speed=speed)
    for d in fl:
        d.scale(1.0)
    fl.add_updater(lambda grp: [d.move_to(g.f(d.get_center())) for d in grp])
    return fl


DATA_X = {"lamprey": False, "shark": False, "trout": True, "frog": False, "human": True}
TIPS = ["lamprey", "shark", "trout", "frog", "human"]


def xbadges(g):
    return {t: g.badge(t, DATA_X[t]) for t in TIPS}


def marks(g, kind):
    d = {}
    if kind == "A":
        d["gain"] = g.tick("B", TEAL)
        d["eB"] = g.edge("B", TEAL, "post", g.mid("B"))
        d["etr"] = g.edge("trout", TEAL)
        d["eT"] = g.edge("T", TEAL)
        d["efr"] = g.edge("frog", TEAL, "pre", g.mid("frog"))
        d["ehu"] = g.edge("human", TEAL)
        d["loss"] = g.tick("frog", GREY)
        d["efp"] = g.edge("frog", GREY, "post", g.mid("frog"))
    elif kind == "B":
        d["t_tr"] = g.tick("trout", TEAL)
        d["e_tr"] = g.edge("trout", TEAL, "post", g.mid("trout"))
        d["t_hu"] = g.tick("human", TEAL)
        d["e_hu"] = g.edge("human", TEAL, "post", g.mid("human"))
    elif kind == "C":
        d["gain"] = g.tick("J", TEAL)
        d["eJ"] = g.edge("J", TEAL, "post", g.mid("J"))
        d["esh"] = g.edge("shark", TEAL, "pre", g.mid("shark"))
        d["eB"] = g.edge("B", TEAL)
        d["etr"] = g.edge("trout", TEAL)
        d["eT"] = g.edge("T", TEAL)
        d["efr"] = g.edge("frog", TEAL, "pre", g.mid("frog"))
        d["ehu"] = g.edge("human", TEAL)
        d["l_sh"] = g.tick("shark", GREY)
        d["l_fr"] = g.tick("frog", GREY)
        d["eshp"] = g.edge("shark", GREY, "post", g.mid("shark"))
        d["efrp"] = g.edge("frog", GREY, "post", g.mid("frog"))
    return d


def jaws_marks(g):
    d = {"gain": g.tick("J", TEAL), "eJ": g.edge("J", TEAL, "post", g.mid("J"))}
    for c in ("shark", "B", "trout", "T", "frog", "human"):
        d["e_" + c] = g.edge(c, TEAL)
    return d


def jaw_badges(g):
    return {t: g.badge(t, t != "lamprey", "jaw") for t in TIPS}


def scale_parts(pivot, half, drop, pans, theta=0.0, hh=1.9):
    th = ValueTracker(theta)
    pv = np.array([pivot[0], pivot[1], 0.0])

    def end(s):
        return pv + half * np.array([s * np.cos(th.get_value()), s * np.sin(th.get_value()), 0.0])

    beam = Line(end(-1), end(1), color=TEXT, stroke_width=8)
    beam.add_updater(lambda m: m.put_start_and_end_on(end(-1), end(1)))
    strings = []
    for s, pan in zip((-1, 1), pans):
        ln = Line(end(s), end(s) + DOWN * drop, color=GREY, stroke_width=4)
        ln.add_updater(lambda m, s=s, pan=pan: m.put_start_and_end_on(end(s), end(s) + DOWN * drop))
        pan.add_updater(lambda m, s=s: m.move_to(end(s) + DOWN * (drop + m.height / 2)))
        pan.move_to(end(s) + DOWN * (drop + pan.height / 2))
        strings.append(ln)
    post = Polygon(pv, pv + np.array([-0.6, -hh, 0]), pv + np.array([0.6, -hh, 0]), color=TEXT, stroke_width=5,
                   fill_color=PANEL, fill_opacity=1)
    base = Line(pv + np.array([-1.1, -hh, 0]), pv + np.array([1.1, -hh, 0]), color=TEXT, stroke_width=7)
    dot = Dot(pv, radius=0.12, color=GOLD)
    for m in (beam, post, base, dot, *strings):
        m.set_z_index(4)
    return th, VGroup(post, base), beam, VGroup(*strings), dot


def tick_cluster(n, col=TEAL):
    return VGroup(*[Line([i * 0.3, -0.25, 0], [i * 0.3, 0.25, 0], color=col, stroke_width=7) for i in range(n)]).move_to(ORIGIN)


def bal_card(txt, n, faded=False):
    box = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    tk = tick_cluster(n).move_to(box.get_center() + UP * 0.35)
    lab = T(txt, 28, TEXT).move_to(box.get_center() + DOWN * 0.38)
    g = VGroup(box, tk, lab)
    if faded:
        g.set_opacity(0.45)
    return g


class B2(F1.Base):
    def full(self, flow=True, ax=True):
        tr = Tree()
        self.tr, self.g = tr, Geo(tr)
        self.put(tr, flow=flow)
        for n in tr.nd.values():
            n.set_z_index(2)
        for n in tr.tp.values():
            n.set_z_index(2)
        self.axs = None
        if ax:
            self.axs = axis()
            self.add(self.axs)

    def panels(self, tallies="? changes", flows=True):
        tr = Tree()
        self.tr = tr
        P = {}
        for key, x0 in (("A", -6.6), ("B", 0.5)):
            g = Geo(tr, x0)
            parts = mini_parts(tr, g)
            for m in parts_items(parts):
                m.set_z_index(2)
            mk, bd = marks(g, key), xbadges(g)
            title = T("A: one origin" if key == "A" else "B: two origins", 30, TEXT).move_to([x0 + 2.85, 3.0, 0])
            tal = tally(tallies, 2.4).move_to([x0 + 2.85, -2.0, 0])
            allv = VGroup(*parts_items(parts), *mk.values(), *bd.values(), title, tal)
            self.add(allv)
            P[key] = dict(g=g, parts=parts, mk=mk, bd=bd, title=title, tal=tal, all=allv)
            if flows:
                P[key]["flow"] = mini_flow(tr, g)
                self.add(P[key]["flow"])
        self.P = P
        return P


def pause_world_mobs():
    return


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Reading Phylogenetic Trees"
    TITLE = "Change Lives on the Branches"


class S01Link(B2):
    def construct(self):
        self.full()
        tr = self.tr
        self.wait(0.2)
        for n in ("R", "J", "B", "T"):
            self.play(ind(tr.nd[n][0], 2.2, NODE_COL[n]), run_time=0.5)
        self.at("features", lead=0.6)
        self.play(*[ind(tr.tp[n][0], 1.3) for n in tr.tp], run_time=1.0)
        ys, yh = tr.pos["shark"][1], tr.pos["human"][1]
        js = badge(None, "jaw").move_to([BX, ys, 0])
        jh = badge(None, "jaw").move_to([BX, yh, 0])
        self.at("sharks", lead=0.3)
        self.play(FadeIn(js, scale=1.6), run_time=0.35)
        self.at("humans", lead=0.0)
        self.play(FadeIn(jh, scale=1.6), run_time=0.5)
        self.at("did they get", lead=0.2)
        arc = DashedVMobject(ArcBetweenPoints([BX + 0.3, ys, 0], [BX + 0.3, yh, 0], angle=-1.2), num_dashes=16).set_color(GOLD)
        q = T("?", 80, GOLD, weight=BOLD).move_to([RC + 0.3, (ys + yh) / 2, 0])
        self.play(Create(arc), FadeIn(q, scale=1.8), run_time=1.2)
        self.at("one ancestor", lead=0.1)
        self.play(ind(q, 1.3, GOLD), run_time=0.8)
        self.at("twice", lead=0.2)
        self.play(ind(js, 1.4, TEXT), ind(jh, 1.4, TEXT), run_time=0.8)
        self.finish()


class S02Terms(B2):
    def construct(self):
        self.full()
        tr = self.tr
        ys, yh = tr.pos["shark"][1], tr.pos["human"][1]
        js = badge(None, "jaw").move_to([BX, ys, 0])
        jh = badge(None, "jaw").move_to([BX, yh, 0])
        self.add(js, jh)
        self.wait(0.2)
        lab = T("character:\njaws", 28, TEXT, line_spacing=0.9).move_to([RC, 2.1, 0])
        self.play(FadeIn(lab, shift=LEFT * 0.3), run_time=0.8)
        self.at("like jaws", lead=0.3)
        self.play(ind(js, 1.4, TEXT), ind(jh, 1.4, TEXT), run_time=0.9)
        self.at("its forms", lead=0.1)
        self.play(ind(lab, 1.1, TEXT), run_time=0.7)
        self.at("jaws present", lead=0.3)
        c1 = chip("jaws present", TEAL, 24).move_to([RC + 0.1, 1.0, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.3), Transform(js, badge(True, "jaw").move_to(js)),
                  Transform(jh, badge(True, "jaw").move_to(jh)), run_time=0.9)
        self.at("jaws absent", lead=0.3)
        c2 = chip("jaws absent", GREY, 24).move_to([RC + 0.1, 0.2, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.8)
        self.play(ind(c2, 1.1, GREY), run_time=0.7)
        self.at("a change of state", lead=0.2)
        cl = T("change on a branch", 28, TEXT).move_to([-1.9, 0.9, 0])
        mk = Line([-4.0, 1.2, 0], [-4.0, 1.8, 0], color=TEAL, stroke_width=8).set_z_index(3)
        self.play(FadeIn(cl, shift=UP * 0.1), FadeIn(mk, scale=1.5), run_time=0.7)
        self.play(mk.animate.shift(RIGHT * 4.0), run_time=2.6, rate_func=linear)
        self.play(ind(mk, 1.6, TEAL), run_time=0.8)
        self.finish()


def add_lamprey_start(sc, tr, g):
    wash = g.trace("lamprey", "R", GREY, 11)
    bl = g.badge("lamprey", False, "jaw")
    return wash, bl


class S03Outgroup(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        ys, yh = tr.pos["shark"][1], tr.pos["human"][1]
        js, jh = g.badge("shark", True, "jaw"), g.badge("human", True, "jaw")
        c1 = chip("jaws present", TEAL, 24).move_to([RC + 0.1, 1.0, 0])
        c2 = chip("jaws absent", GREY, 24).move_to([RC + 0.1, 0.2, 0])
        self.add(js, jh, c1, c2)
        self.wait(0.3)
        self.play(ind(tr.nd["R"][0], 2.2, GOLD), run_time=0.8)
        self.play(ind(tr.nd["R"][0], 2.2, GOLD), run_time=0.8)
        self.at("take the out group", lead=0.1)
        lamb = tr.br["R"][1]
        tg = tag("outgroup", [-3.2, 3.2, 0], ORG, size=32)
        self.play(lamb.animate.set_stroke(ORG, 10), tr.tp["lamprey"][1].animate.set_color(ORG), FadeIn(tg, shift=DOWN * 0.1), run_time=0.9)
        self.at("starting point", lead=0.3)
        self.play(ind(tr.nd["R"][0], 2.2, GOLD), run_time=0.8)
        self.at("lamprey has no jaws", lead=0.1)
        bl = g.badge("lamprey", False, "jaw")
        self.play(FadeOut(tg), lamb.animate.set_stroke(BRC, 5), tr.tp["lamprey"][1].animate.set_color(TEXT), FadeIn(bl, scale=1.6), run_time=0.8)
        self.at("so absence", lead=0.1)
        wash = g.trace("lamprey", "R", GREY, 11)
        self.play(Create(wash), run_time=1.6, rate_func=linear)
        self.at("ancestral state", lead=0.2)
        sl = T("starting state (from the outgroup)", 28, TEXT).move_to([-3.0, 3.35, 0])
        self.play(FadeIn(sl, shift=DOWN * 0.1), run_time=0.7)
        self.at("that is an assumption", lead=0.2)
        ch = chip("assumption", GOLD, 28).move_to([RC, -0.8, 0])
        self.play(FadeIn(ch, shift=LEFT * 0.3), run_time=0.7)
        self.at("lineage can change", lead=0.3)
        mk = Line([-5.5, 2.4, 0], [-5.5, 3.0, 0], color=GOLD, stroke_width=8).set_z_index(3)
        self.play(FadeIn(mk, scale=1.4), run_time=0.4)
        self.play(mk.animate.shift(RIGHT * 4.5), run_time=2.2, rate_func=linear)
        self.play(ind(ch, 1.15, GOLD), run_time=0.8)
        self.finish()


def jaws_state(sc, g, tr, with_wash=True):
    """Adds the end-of-s04 picture (jaws mapped) and returns every mobject in it."""
    items = []
    jm = jaws_marks(g)
    jb = jaw_badges(g)
    wash = g.trace("lamprey", "R", GREY, 11)
    items = [*jm.values(), *jb.values()] + ([wash] if with_wash else [])
    sc.add(*items)
    return jm, jb, wash, items


class S04Jaws(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        wash = g.trace("lamprey", "R", GREY, 11)
        bl = g.badge("lamprey", False, "jaw")
        c1 = chip("jaws present", TEAL, 24).move_to([RC + 0.1, 1.0, 0])
        c2 = chip("jaws absent", GREY, 24).move_to([RC + 0.1, 0.2, 0])
        self.add(wash, bl, c1, c2)
        jm, jb = jaws_marks(g), jaw_badges(g)
        for t in ("shark", "trout", "frog", "human"):
            self.at(t, lead=0.1)
            self.play(FadeIn(jb[t], scale=1.6), run_time=0.35)
        tal = tally("1 change").move_to([RC, 3.2, 0])
        self.at("one gain", lead=0.2)
        self.play(GrowFromCenter(jm["gain"]), FadeIn(tal, shift=DOWN * 0.2), run_time=0.8)
        self.at("node j", lead=0.2)
        self.play(ind(tr.nd["J"][0], 2.2, JC), run_time=0.8)
        self.at("explains", lead=0.2)
        order = ["eJ", "e_shark", "e_B", "e_trout", "e_T", "e_frog", "e_human"]
        self.play(LaggedStart(*[Create(jm[k]) for k in order], lag_ratio=0.45), run_time=2.6)
        self.at("jaws in sharks", lead=0.2)
        self.play(ind(jb["shark"], 1.5, TEAL), ind(jb["human"], 1.5, TEAL), run_time=1.0)
        self.at("homologous", lead=0.1)
        hl = T("homology:\none origin", 28, TEXT, line_spacing=0.9).move_to([RC, -1.6, 0])
        self.play(FadeIn(hl, shift=LEFT * 0.3), run_time=0.8)
        self.at("single origin", lead=0.3)
        self.play(ind(jm["gain"], 1.8, TEAL), run_time=0.9)
        self.at("common ancestor", lead=0.3)
        self.play(ind(tr.nd["J"][0], 2.4, JC), ind(jm["gain"], 1.8, TEAL), run_time=0.9)
        self.finish()


class S05Parsimony(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        jm, jb, wash, items = jaws_state(self, g, tr)
        tal = tally("1 change").move_to([RC, 3.2, 0])
        self.add(tal)
        world = [*tr.mobs(), self.axs, *items]
        self.wait(0.3)
        self.at("mapping", lead=0.3)
        self.play(ind(jm["gain"], 1.8, TEAL), run_time=0.9)
        self.at("fewest", lead=0.3)
        pl = bal_card("1 change", 1)
        pr = bal_card("several", 5, faded=True)
        th, fulc, beam, strs, dot = scale_parts([0, 1.4], 3.0, 0.7, [pl, pr])
        lab = T("parsimony", 44, GOLD, weight=BOLD).move_to([0, 3.2, 0])
        self.remove(self.flow)
        self.play(*[FadeOut(m) for m in world], FadeOut(tal),
                  FadeIn(fulc), FadeIn(beam), FadeIn(strs), FadeIn(dot), FadeIn(lab), run_time=1.0)
        self.add(beam, strs, pl, pr)
        self.play(th.animate.set_value(0.2), run_time=1.4)
        clock = [0.0]
        th.add_updater(lambda m, dt: (clock.__setitem__(0, clock[0] + dt), m.set_value(0.2 + 0.03 * np.sin(clock[0] * 2.2))))
        self.at("rule for choosing", lead=0.3)
        t1 = T("a rule for choosing", 34, GOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.7)
        self.at("does not claim", lead=0.2)
        t2 = T("not a law of evolution", 34, RED).move_to([0, -3.3, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        self.wait(1.0)
        self.finish()
        th.clear_updaters()


class S06X(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        jm, jb, wash, items = jaws_state(self, g, tr)
        tal = tally("1 change").move_to([RC, 3.2, 0])
        self.add(tal)
        self.wait(0.2)
        t0 = tally("0 changes").move_to([RC, 3.2, 0])
        self.play(*[FadeOut(m) for m in items], Transform(tal, t0), run_time=0.9)
        self.at("called x", lead=0.5)
        lab = T("character X\n(made up)", 28, TEXT, line_spacing=0.9).move_to([RC, 2.0, 0])
        self.play(FadeIn(lab, shift=LEFT * 0.3), run_time=0.8)
        bd = xbadges(g)
        self.at("trout", lead=0.1)
        self.play(FadeIn(bd["trout"], scale=1.6), run_time=0.35)
        self.at("human", lead=0.1)
        self.play(FadeIn(bd["human"], scale=1.6), run_time=0.35)
        self.at("have it", lead=0.2)
        c1 = chip("X present", TEAL, 24).move_to([RC + 0.1, 1.0, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.3), run_time=0.7)
        for t in ("lamprey", "shark", "frog"):
            self.at(t, lead=0.1)
            self.play(FadeIn(bd[t], scale=1.6), run_time=0.35)
        self.at("do not", lead=0.1)
        c2 = chip("X absent", GREY, 24).move_to([RC + 0.1, 0.2, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.7)
        self.at("absence", lead=0.2)
        wash = g.trace("lamprey", "R", GREY, 11)
        sl = T("starting state: X absent", 28, TEXT).move_to([-3.0, 3.35, 0])
        self.play(Create(wash), FadeIn(sl, shift=DOWN * 0.1), run_time=1.6, rate_func=linear)
        self.play(ind(bd["lamprey"], 1.4, GREY), run_time=0.8)
        self.finish()


def x_state_full(sc, g):
    bd = xbadges(g)
    wash = g.trace("lamprey", "R", GREY, 11)
    sc.add(*bd.values(), wash)
    return bd, wash


class S07One(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        bd, wash = x_state_full(self, g)
        tal = tally("? changes").move_to([RC, 3.2, 0])
        self.add(tal)
        mk = marks(g, "A")
        self.wait(0.2)
        self.at("one mapping", lead=0.2)
        lab = T("A: one origin", 30, TEXT).move_to([RC, 2.0, 0])
        self.play(FadeIn(lab, shift=LEFT * 0.3), run_time=0.8)
        self.at("x is gained", lead=0.2)
        self.play(GrowFromCenter(mk["gain"]), run_time=0.6)
        self.at("node b", lead=0.2)
        self.play(ind(tr.nd["B"][0], 2.2, GOLD), run_time=0.5)
        self.play(LaggedStart(*[Create(mk[k]) for k in ("eB", "etr", "eT", "efr", "ehu")], lag_ratio=0.4), run_time=2.0)
        self.at("lost", lead=0.2)
        self.play(GrowFromCenter(mk["loss"]), run_time=0.6)
        self.play(Create(mk["efp"]), run_time=0.8)
        self.at("one origin", lead=0.2)
        self.play(ind(mk["gain"], 1.8, TEAL), run_time=0.9)
        self.at("trout and humans share", lead=0.1)
        hl = T("shared by\nhomology", 28, TEXT, line_spacing=0.9).move_to([RC, -1.3, 0])
        rb = ring(tr.pos["B"], GOLD)
        self.play(ind(bd["trout"], 1.5, TEAL), ind(bd["human"], 1.5, TEAL), FadeIn(hl, shift=LEFT * 0.3), FadeIn(rb, scale=2.0), run_time=1.2)
        self.play(ind(rb, 1.4, GOLD), run_time=0.9)
        self.finish()


class S08Two(B2):
    def construct(self):
        tr = Tree()
        self.tr = tr
        g = Geo(tr)
        self.put(tr, flow=False)
        for n in tr.nd.values():
            n.set_z_index(2)
        for n in tr.tp.values():
            n.set_z_index(2)
        bdF, washF = x_state_full(self, g)
        mkF = marks(g, "A")
        self.add(*mkF.values())
        labF = T("A: one origin", 30, TEXT).move_to([RC, 2.0, 0])
        talF = tally("? changes").move_to([RC, 3.2, 0])
        self.add(labF, talF)
        ax = axis()
        self.add(ax)
        self.wait(0.2)
        # shrink full tree into panel A (left) and build panel B
        gA, gB = Geo(tr, -6.6), Geo(tr, 0.5)
        pA, pB = mini_parts(tr, gA), mini_parts(tr, gB)
        mkA, bdA = marks(gA, "A"), xbadges(gA)
        washA = gA.trace("lamprey", "R", GREY, 8)
        mkB, bdB = marks(gB, "B"), xbadges(gB)
        washB = gB.trace("lamprey", "R", GREY, 8)
        titleA = T("A: one origin", 30, TEXT).move_to([-3.75, 3.0, 0])
        titleB = T("B: two origins", 30, TEXT).move_to([3.35, 3.0, 0])
        talA = tally("? changes", 2.4).move_to([-3.75, -2.0, 0])
        talB = tally("? changes", 2.4).move_to([3.35, -2.0, 0])
        anims = []
        for n in tr.br:
            anims.append(Transform(tr.br[n], pA["br"][n]))
        for n in tr.nd:
            anims += [Transform(tr.nd[n][0], pA["nd"][n][0]), Transform(tr.nd[n][1], pA["nd"][n][1])]
        for n in tr.tp:
            anims += [Transform(tr.tp[n][0], pA["tp"][n][0]), Transform(tr.tp[n][1], pA["tp"][n][1])]
        for k in mkF:
            anims.append(Transform(mkF[k], mkA[k]))
        for k in bdF:
            anims.append(Transform(bdF[k], bdA[k]))
        anims += [Transform(washF, washA), Transform(labF, titleA), Transform(talF, talA), FadeOut(ax)]
        itemsB = [*parts_items(pB), *bdB.values(), washB, titleB, talB]
        self.play(*anims, FadeIn(VGroup(*itemsB)), run_time=1.6)
        for m in parts_items(pB):
            m.set_z_index(2)
        self.add(*mkB.values())
        fA, fB = mini_flow(tr, gA), mini_flow(tr, gB)
        self.add(fA, fB)
        self.at("x is gained twice", lead=0.2)
        self.play(ind(titleB, 1.15, TEXT), run_time=0.8)
        self.at("branch to trout", lead=0.3)
        self.play(GrowFromCenter(mkB["t_tr"]), run_time=0.6)
        self.play(Create(mkB["e_tr"]), run_time=0.8)
        self.at("human", lead=0.3)
        self.play(GrowFromCenter(mkB["t_hu"]), run_time=0.6)
        self.play(Create(mkB["e_hu"]), run_time=0.8)
        self.at("convergence", lead=0.2)
        cv = T("convergence", 34, TEXT, weight=BOLD).move_to([3.35, -2.85, 0])
        self.play(FadeIn(cv, shift=UP * 0.1), run_time=0.7)
        self.at("independently", lead=0.2)
        self.play(ind(mkB["t_tr"], 1.8, TEAL), run_time=0.7)
        self.play(ind(mkB["t_hu"], 1.8, TEAL), run_time=0.7)
        self.at("separate lineages", lead=0.2)
        self.play(ind(mkB["t_tr"], 1.8, TEAL), ind(mkB["t_hu"], 1.8, TEAL), run_time=0.9)
        self.finish()


class S09Predict(B2):
    def construct(self):
        P = self.panels("? changes")
        self.wait(0.3)
        self.at("parsimony", lead=0.2)
        self.play(ind(P["A"]["title"], 1.15), ind(P["B"]["title"], 1.15), run_time=0.9)
        self.at("count the marks", lead=0.2)
        for m in (P["A"]["mk"]["gain"], P["A"]["mk"]["loss"], P["B"]["mk"]["t_tr"], P["B"]["mk"]["t_hu"]):
            self.play(ind(m, 2.0, GOLD), run_time=0.5)
        self.at("what is the fewest", lead=0.2)
        q = T("Fewest changes for X?", 40, TEXT)
        card = RoundedRectangle(corner_radius=0.2, width=q.width + 0.7, height=1.0, stroke_color=GOLD, stroke_width=4,
                                fill_color=PANEL, fill_opacity=1)
        qc = VGroup(card, q.move_to(card)).move_to([0, -3.0, 0])
        self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.8)
        self.play(ind(qc, 1.06, GOLD), run_time=0.9)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        sc = B2.__new__(B2)
        sc = self
        tr = Tree()
        P = {}
        for key, x0 in (("A", -6.6), ("B", 0.5)):
            g = Geo(tr, x0)
            parts = mini_parts(tr, g)
            for m in parts_items(parts):
                m.set_z_index(2)
            mk, bd = marks(g, key), xbadges(g)
            title = T("A: one origin" if key == "A" else "B: two origins", 30, TEXT).move_to([x0 + 2.85, 3.0, 0])
            tal = tally("? changes", 2.4).move_to([x0 + 2.85, -2.0, 0])
            wash = g.trace("lamprey", "R", GREY, 8)
            self.add(*parts_items(parts), *mk.values(), *bd.values(), wash, title, tal, mini_flow(tr, g))
        q = T("Fewest changes for X?", 40, TEXT)
        card = RoundedRectangle(corner_radius=0.2, width=q.width + 0.7, height=1.0, stroke_color=GOLD, stroke_width=4,
                                fill_color=PANEL, fill_opacity=1)
        self.add(VGroup(card, q.move_to(card)).move_to([0, -3.0, 0]))
        base = Circle(radius=0.38, stroke_color=GREY, stroke_width=6).move_to([6.1, -3.0, 0])
        prog = Circle(radius=0.38, stroke_color=GOLD, stroke_width=8).move_to([6.1, -3.0, 0]).rotate(PI / 2).flip(axis=RIGHT)
        self.add(base)
        self.play(Create(prog), run_time=max(1.0, self.narration_s - 0.4), rate_func=linear)
        self.finish()


class S11Reveal(B2):
    def construct(self):
        P = self.panels("? changes")
        tr = self.tr
        q = T("Fewest changes for X?", 40, TEXT)
        card = RoundedRectangle(corner_radius=0.2, width=q.width + 0.7, height=1.0, stroke_color=GOLD, stroke_width=4,
                                fill_color=PANEL, fill_opacity=1)
        qc = VGroup(card, q.move_to(card)).move_to([0, -3.0, 0])
        self.add(qc)
        self.wait(0.2)
        t2a = tally("2 changes", 2.4).move_to(P["A"]["tal"])
        t2b = tally("2 changes", 2.4).move_to(P["B"]["tal"])
        self.play(FadeOut(qc), Transform(P["A"]["tal"], t2a), Transform(P["B"]["tal"], t2b), run_time=0.9)
        self.play(ind(P["A"]["tal"], 1.15, GOLD), ind(P["B"]["tal"], 1.15, GOLD), run_time=0.6)
        mn = T("minimum = 2", 40, GOLD, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(mn, shift=UP * 0.1), run_time=0.6)
        gB = P["B"]["g"]
        self.at("no single branch", lead=0.1)
        steps = [("B", ["trout", "frog", "human"]), ("T", ["frog", "human"]), ("trout", ["trout"]), ("human", ["human"])]
        cur = []
        for c, tips in steps:
            if cur:
                self.play(*[FadeOut(m) for m in cur], run_time=0.25)
            e = gB.edge(c, GOLD)
            e.set_stroke(GOLD, 9).set_z_index(5)
            rs = [Circle(radius=0.34, stroke_color=GOLD, stroke_width=5).move_to(P["B"]["bd"][t]) for t in tips]
            cur = [e, *rs]
            self.play(*[Create(e)] + [FadeIn(r, scale=1.5) for r in rs], run_time=0.7)
            self.wait(0.5)
        self.at("so one change", lead=0.3)
        self.play(*[FadeOut(m) for m in cur], run_time=0.3)
        self.at("a gain on the branch into node j", lead=0.3)
        cardC = RoundedRectangle(corner_radius=0.25, width=7.0, height=5.6, stroke_color=GOLD, stroke_width=4,
                                 fill_color=PANEL, fill_opacity=1).move_to([0, 0.2, 0])
        gC = Geo(tr, -2.85)
        gC.f0 = gC.f
        partsC = mini_parts(tr, gC)
        mkC, bdC = marks(gC, "C"), {t: gC.badge(t, DATA_X[t]) for t in TIPS}
        lbC = T("C", 36, GOLD, weight=BOLD).move_to([-3.0, 2.65, 0])
        allC = VGroup(cardC, *parts_items(partsC), *bdC.values(), lbC)
        for m in allC:
            m.set_z_index(12)
        for m in mkC.values():
            m.set_z_index(14)
        self.play(FadeIn(allC), run_time=0.6)
        self.play(GrowFromCenter(mkC["gain"]), run_time=0.5)
        self.add(*mkC.values())
        self.play(LaggedStart(*[Create(mkC[k]) for k in ("eJ", "esh", "eB", "etr", "eT", "efr", "ehu")], lag_ratio=0.35), run_time=1.6)
        self.at("with two losses", lead=0.2)
        self.play(GrowFromCenter(mkC["l_sh"]), Create(mkC["eshp"]), run_time=0.6)
        self.play(GrowFromCenter(mkC["l_fr"]), Create(mkC["efrp"]), run_time=0.6)
        self.at("would need three", lead=0.2)
        t3 = tally("3 changes", 2.4).move_to([0.9, 2.65, 0]).set_z_index(15)
        self.play(FadeIn(t3, scale=1.3), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(allC), FadeOut(t3), *[FadeOut(m) for m in mkC.values()], run_time=0.5)
        self.finish()


class S12Tie(B2):
    def construct(self):
        P = self.panels("2 changes")
        tr = self.tr
        self.wait(0.2)
        for k in "AB":
            self.remove(P[k]["flow"])
        dx = {"A": 0.6, "B": -0.6}
        self.play(*[P[k]["all"].animate.shift(RIGHT * dx[k]) for k in "AB"], run_time=1.2)
        for k in "AB":
            P[k]["g"].x0 += dx[k]
            P[k]["flow"] = mini_flow(tr, P[k]["g"])
            self.add(P[k]["flow"])
        pl = VGroup(Arc(radius=0.45, start_angle=PI + 0.3, angle=PI - 0.6, color=TEXT, stroke_width=6))
        pr = VGroup(Arc(radius=0.45, start_angle=PI + 0.3, angle=PI - 0.6, color=TEXT, stroke_width=6))
        th, fulc, beam, strs, dot = scale_parts([0, -1.7], 1.2, 0.35, [pl, pr], hh=0.0)
        self.at("tie", lead=0.3)
        tie = T("tie", 52, GOLD, weight=BOLD).move_to([0, -2.85, 0])
        th.set_value(0.12)
        self.add(fulc, beam, strs, dot, pl, pr)
        self.play(FadeIn(tie, scale=1.3), th.animate.set_value(0.0), run_time=0.9)
        clock = [0.0]
        th.add_updater(lambda m, dt: (clock.__setitem__(0, clock[0] + dt), m.set_value(0.025 * np.sin(clock[0] * 2.0))))
        self.at("between one origin", lead=0.2)
        self.play(ind(P["A"]["title"], 1.15), run_time=0.8)
        self.at("and two", lead=0.2)
        self.play(ind(P["B"]["title"], 1.15), run_time=0.8)
        self.at("homology or convergence", lead=0.2)
        oq = T("homology or convergence?", 32, TEXT).move_to([0, -3.5, 0])
        self.play(FadeIn(oq, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)
        self.play(ind(oq, 1.08, GOLD), run_time=0.9)
        self.finish()
        th.clear_updaters()


def card_box(w=4.4, h=3.9):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=PANEL, fill_opacity=1)


class S13More(B2):
    def construct(self):
        P = self.panels("2 changes")
        tr = self.tr
        for k in "AB":
            self.remove(P[k]["flow"])
            P[k]["all"].shift(RIGHT * (0.6 if k == "A" else -0.6))
        tie = T("tie", 52, GOLD, weight=BOLD).move_to([0, -2.85, 0])
        self.add(tie)
        self.wait(0.4)
        self.at("you need more evidence", lead=0.2)
        self.play(FadeOut(P["A"]["all"]), FadeOut(P["B"]["all"]), tie.animate.move_to([0, 3.2, 0]).scale(0.8), run_time=1.0)
        b1 = card_box().move_to([-3.4, -0.2, 0])
        b2 = card_box().move_to([3.4, -0.2, 0])
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.8)
        self.at("how x develops", lead=0.2)
        egg = Ellipse(width=1.5, height=1.9, color=GREY, stroke_width=5).move_to(b1.get_center() + UP * 0.9)
        emb = Arc(radius=0.5, start_angle=0.6, angle=4.6, color=SP["human"], stroke_width=10).move_to(egg)
        hd = Circle(radius=0.18, fill_color=SP["human"], fill_opacity=1, stroke_width=0).move_to(egg.get_center() + RIGHT * 0.35 + UP * 0.28)
        strip = M("ATGCCGTAGC", 30, TEAL).move_to(b1.get_center() + DOWN * 0.2)
        lb1 = T("development\nand genes", 28, TEXT, line_spacing=0.9).move_to(b1.get_center() + DOWN * 1.2)
        c1 = VGroup(b1, egg, emb, hd, strip, lb1)
        self.play(FadeIn(VGroup(egg, emb, hd, strip, lb1), shift=UP * 0.2), run_time=0.9)
        gd = Dot(radius=0.1, color=GOLD).set_z_index(5)
        ck = [0.0]

        def mv(d, dt):
            ck[0] += dt
            u = (ck[0] * 0.35) % 1.0
            d.move_to([strip.get_left()[0] + u * strip.width, strip.get_top()[1] + 0.15, 0])
        gd.add_updater(mv)
        self.add(gd)
        self.at("or what genes", lead=0.2)
        self.play(ind(strip, 1.15, TEAL), run_time=0.9)
        self.at("fossils with", lead=0.2)
        slab = RoundedRectangle(corner_radius=0.15, width=2.6, height=1.6, fill_color="#2b2f3b", fill_opacity=1, stroke_color=GREY, stroke_width=3).move_to(b2.get_center() + UP * 0.8)
        sx = slab.get_center()
        spine = Line(sx + LEFT * 0.8, sx + RIGHT * 0.6, color=SP["shark"], stroke_width=6)
        ribs = VGroup(*[Line(sx + RIGHT * x + UP * 0.35, sx + RIGHT * x + DOWN * 0.35, color=SP["shark"], stroke_width=4) for x in (-0.55, -0.3, -0.05, 0.2, 0.42)])
        skull = Circle(radius=0.22, color=SP["shark"], stroke_width=5).move_to(sx + RIGHT * 0.85)
        fos = VGroup(spine, ribs, skull)
        lb2 = T("fossils with\nintermediate\nstates", 28, TEXT, line_spacing=0.9).move_to(b2.get_center() + DOWN * 1.05)
        c2 = VGroup(b2, slab, fos, lb2)
        self.play(FadeIn(VGroup(slab, fos, lb2), shift=UP * 0.2), run_time=0.9)
        c3 = [0.0]
        fos.add_updater(lambda m, dt: (c3.__setitem__(0, c3[0] + dt), m.set_stroke(opacity=0.65 + 0.35 * np.sin(c3[0] * 2.5))))
        self.play(ind(fos, 1.1, SP["shark"]), run_time=1.2)
        self.at("or more taxa", lead=0.4)
        gd.clear_updaters()
        fos.clear_updaters()
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(gd), FadeOut(tie), run_time=0.5)
        self.full()
        g = self.g
        yb = 0.9
        dl = DashedLine([-4.3, yb, 0], [0.4, yb, 0], dash_length=0.12, color=GREY, stroke_width=4)
        slot = DashedVMobject(Circle(radius=0.3, color=GREY, stroke_width=4).move_to([1.0, yb, 0]), num_dashes=14)
        sl = T("more taxa", 28, TEXT).move_to([1.6, yb, 0], aligned_edge=LEFT)
        self.play(Create(dl), FadeIn(slot, scale=1.5), FadeIn(sl, shift=LEFT * 0.2), run_time=1.2)
        self.play(ind(slot, 1.3, GREY), run_time=0.9)
        self.finish()


class S14Rule(B2):
    def construct(self):
        self.full()
        tr, g = self.tr, self.g
        jm, jb, wash, items = jaws_state(self, g, tr)
        self.wait(0.2)
        self.at("map every change", lead=0.2)
        self.play(ind(jm["gain"], 2.0, TEAL), run_time=0.9)
        self.play(ind(jm["gain"], 2.0, TEAL), run_time=0.9)
        self.at("two taxes share", lead=0.2)
        self.play(ind(jb["shark"], 1.5, TEAL), ind(jb["human"], 1.5, TEAL), run_time=0.9)
        self.at("inherit it", lead=0.3)
        fl = [g.trace(t, "R", TEAL, 12).reverse_points() for t in ("shark", "human")]
        self.play(*[ShowPassingFlash(f, time_width=0.5) for f in fl], run_time=2.0)
        self.at("a shared branch", lead=0.2)
        t1 = T("one gain on a\nshared branch\n= one origin", 28, TEXT, line_spacing=0.9).move_to([RC, 0.6, 0])
        self.play(FadeIn(t1, shift=LEFT * 0.3), ind(jm["eJ"], 1.0, TEAL), run_time=1.0)
        self.at("other lineages", lead=0.2)
        bd, wash2 = None, None
        mk = marks(g, "A")
        bdx = xbadges(g)
        self.play(*[FadeOut(m) for m in items], run_time=0.5)
        self.add(wash, *bdx.values())
        self.play(FadeIn(VGroup(*bdx.values())), run_time=0.4)
        self.add(*mk.values())
        self.play(FadeIn(mk["gain"], scale=1.5), LaggedStart(*[Create(mk[k]) for k in ("eB", "etr", "eT", "efr", "ehu")], lag_ratio=0.3), run_time=1.6)
        self.at("lose it", lead=0.4)
        t2 = T("later losses\nallowed", 28, TEXT, line_spacing=0.9).move_to([RC, -1.0, 0])
        self.play(GrowFromCenter(mk["loss"]), Create(mk["efp"]), FadeIn(t2, shift=LEFT * 0.3), run_time=1.0)
        self.at("separate gains", lead=0.3)
        mkb = marks(g, "B")
        t3 = T("separate gains\n= convergence", 28, TEXT, line_spacing=0.9).move_to([RC, -2.3, 0])
        self.play(*[FadeOut(m) for m in mk.values()], FadeOut(t2), run_time=0.5)
        self.add(*mkb.values())
        self.play(GrowFromCenter(mkb["t_tr"]), GrowFromCenter(mkb["t_hu"]), Create(mkb["e_tr"]), Create(mkb["e_hu"]), FadeIn(t3, shift=LEFT * 0.3), run_time=1.0)
        self.play(ind(mkb["t_tr"], 1.8, TEAL), ind(mkb["t_hu"], 1.8, TEAL), run_time=0.9)
        self.finish()


class S15End(EndCard):
    LINE = "Homology means one gain on a shared branch; separate gains mean convergence."
