"""Sensory neuron atlas: how many kinds of sensory neuron?  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every dot map is a labelled sketch: dots stand for neurons and clusters are placed by hand.
None of it is data.

COLOR MAP (one color per concept, whole video)
  BLUE   = neurofilament-rich classes (NF)
  GREEN  = non-peptidergic classes (NP)
  YELLOW = peptidergic classes (PEP)
  ORANGE = the TH class
  RED    = injury state (the Atf3 group)
  PURPLE = anchors: the independent measures that tie a cluster to a job
  TEAL   = "in this sketch" tag, resolution, questions and cautions
  TEXT   = neurons not yet assigned a class (plain dots)
  GREY   = frames, tree lines, de-emphasised structure
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
NF, NP, PEP, TH = BLUE, GREEN, YELLOW, ORANGE
DOT = 0.075


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cluster_pts(center, n, spread, rng):
    """n points in a soft disc around center (deterministic)."""
    pts = []
    while len(pts) < n:
        p = rng.normal(0, spread / 2.0, 2)
        if np.hypot(*p) < spread:
            pts.append(np.array([center[0] + p[0], center[1] + p[1], 0.0]))
    return pts


def dots(pts, color=TEXT, r=DOT, op=0.95):
    return VGroup(*[Dot(p, radius=r, color=color, fill_opacity=op) for p in pts])


def sketch_tag(x=4.2, y=-3.5):
    return T("in this sketch: not real data", 22, TEAL).move_to([x, y, 0])


def arr(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def frame_rect(w, h, cx=0.0, cy=0.0, color=GREY):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_opacity=0).move_to([cx, cy, 0])


class S00Title(TitleCard):
    LESSON = "The sensory neuron atlas"
    TITLE = "How Many Kinds of Sensory Neuron?"


# ---------------------------------------------------------------------------------------------
class S01Count(SpokenScene):
    """three dot maps with 11, 17 and 18 clusters; a question over the three counts."""

    def panel(self, cx, n_clusters, seed, number, caption):
        rng = np.random.default_rng(seed)
        w, h = 3.9, 4.3
        fr = frame_rect(w, h, cx, 0.35)
        cols = 4
        rows = int(np.ceil(n_clusters / cols))
        cells = [(i % cols, i // cols) for i in range(n_clusters)]
        pts = []
        for (c, r) in cells:
            x = cx - w / 2 + 0.55 + c * (w - 1.1) / (cols - 1) + rng.uniform(-0.1, 0.1)
            y = 0.35 + h / 2 - 0.55 - r * (h - 1.1) / (rows - 1) + rng.uniform(-0.1, 0.1)
            pts += cluster_pts((x, y), 5, 0.2, rng)
        d = dots(pts)
        num = M(str(number), 64, TEXT, weight=BOLD).move_to([cx, -2.35, 0])
        cap = T(caption, 24, GREY).move_to([cx, -3.1, 0])
        return fr, d, num, cap

    def construct(self):
        P = [self.panel(-4.4, 11, 1, 11, "one mouse data set"),
             self.panel(0.0, 17, 2, 17, "larger, 3 years later"),
             self.panel(4.4, 18, 3, 18, "31 data sets, six species")]
        tag = sketch_tag(0.0, -3.7)
        self.at("One mouse")
        self.play(FadeIn(tag), FadeIn(P[0][0]), LaggedStart(*[GrowFromCenter(x) for x in P[0][1]], lag_ratio=0.01),
                  run_time=1.2)
        self.at("kinds")
        self.play(FadeIn(P[0][2], scale=0.8), FadeIn(P[0][3]), run_time=0.6)
        self.at("A larger one")
        self.play(FadeIn(P[1][0]), LaggedStart(*[GrowFromCenter(x) for x in P[1][1]], lag_ratio=0.01), run_time=1.0)
        self.play(FadeIn(P[1][2], scale=0.8), FadeIn(P[1][3]), run_time=0.5)
        self.at("settled on")
        self.play(FadeIn(P[2][0]), LaggedStart(*[GrowFromCenter(x) for x in P[2][1]], lag_ratio=0.01), run_time=1.0)
        self.play(FadeIn(P[2][2], scale=0.8), FadeIn(P[2][3]), run_time=0.5)
        self.at("Which number is right")
        q = T("Which number is right?", 36, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.5)
        self.at("none is final")
        self.play(Indicate(q, color=TEAL, scale_factor=1.05), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cluster(SpokenScene):
    """622 neurons sorted by an unsupervised method into eleven classes: 5 NF, 3 NP, 2 PEP, 1 TH."""

    def construct(self):
        rng = np.random.default_rng(7)
        mapfr = frame_rect(12.2, 5.5, 0, 0.05)
        head = T("Usoskin et al., 2015: mouse dorsal root ganglion neurons", 26, TEXT).move_to([0, 3.5, 0])
        tag = sketch_tag(3.9, -3.5)
        # layout of the 11 class centres
        row1 = [("NF1", NF, -4.7, 1.0), ("NF2", NF, -2.9, 1.0), ("NF3", NF, -1.1, 1.0), ("NF4", NF, 0.7, 1.0),
                ("NF5", NF, 2.5, 1.0), ("TH", TH, 4.6, 1.0)]
        row2 = [("NP1", NP, -4.7, -0.9), ("NP2", NP, -2.9, -0.9), ("NP3", NP, -1.1, -0.9),
                ("PEP1", PEP, 1.6, -0.9), ("PEP2", PEP, 3.4, -0.9)]
        spec = row1 + row2
        targets, groups = [], []
        for (nm, col, x, y) in spec:
            pts = cluster_pts((x, y), 9, 0.42, rng)
            targets.append(pts)
        # start: the same 99 dots scattered over the map
        scat = [np.array([rng.uniform(-5.6, 5.6), rng.uniform(-2.2, 2.4), 0.0]) for _ in range(99)]
        D = dots(scat)
        n = T("622 neurons", 28, TEXT).move_to([-4.6, -3.5, 0])

        self.play(FadeIn(head), FadeIn(mapfr), FadeIn(tag), run_time=0.6)
        self.at("cell bodies")
        self.play(FadeIn(D, lag_ratio=0.01), run_time=1.5)
        self.at("single neurons")
        self.play(FadeIn(n), run_time=0.5)
        self.at("grouped them")
        anims = []
        k = 0
        for pts in targets:
            for p in pts:
                anims.append(D[k].animate.move_to(p))
                k += 1
        self.play(LaggedStart(*anims, lag_ratio=0.008), run_time=2.6)
        self.at("classes came out")
        cnt = M("11 classes", 30, TEXT, weight=BOLD).move_to([-4.6, -3.5, 0])
        self.play(ReplacementTransform(n, cnt), run_time=0.6)
        # labels under each cluster (ids from the lesson)
        labs = {}
        for (nm, col, x, y) in spec:
            labs[nm] = T(nm, 22, col).move_to([x, y - 0.75, 0])
        # NF
        self.at("Five were")
        k0 = 0
        grp_nf = VGroup(*[D[i] for i in range(0, 45)])
        bk = Line([-5.2, 2.0, 0], [3.0, 2.0, 0], color=NF, stroke_width=3)
        bt = T("neurofilament-rich (5)", 24, NF).move_to([-1.1, 2.4, 0])
        self.play(grp_nf.animate.set_color(NF), FadeIn(bk), FadeIn(bt),
                  *[FadeIn(labs[f"NF{i}"]) for i in range(1, 6)], run_time=0.8)
        self.at("three were")
        grp_np = VGroup(*[D[i] for i in range(54, 81)])
        bk2 = Line([-5.2, -1.95, 0], [-0.6, -1.95, 0], color=NP, stroke_width=3)
        bt2 = T("non-peptidergic (3)", 24, NP).move_to([-2.9, -2.35, 0])
        self.play(grp_np.animate.set_color(NP), FadeIn(bk2), FadeIn(bt2),
                  *[FadeIn(labs[f"NP{i}"]) for i in range(1, 4)], run_time=0.8)
        self.at("two were")
        grp_pep = VGroup(*[D[i] for i in range(81, 99)])
        bk3 = Line([1.0, -1.95, 0], [4.0, -1.95, 0], color=PEP, stroke_width=3)
        bt3 = T("peptidergic (2)", 24, PEP).move_to([2.5, -2.35, 0])
        self.play(grp_pep.animate.set_color(PEP), FadeIn(bk3), FadeIn(bt3),
                  FadeIn(labs["PEP1"]), FadeIn(labs["PEP2"]), run_time=0.8)
        self.at("tyrosine hydroxylase")
        grp_th = VGroup(*[D[i] for i in range(45, 54)])
        bt4 = T("tyrosine\nhydroxylase", 22, TH, line_spacing=0.8).move_to([4.6, 2.25, 0])
        self.play(grp_th.animate.set_color(TH), FadeIn(bt4), FadeIn(labs["TH"]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Resolution(SpokenScene):
    """one tree read at two resolutions: 3 broad classes, then 8 + 6 + 3 = 17 types."""

    def construct(self):
        ybr = {"pep": 2.3, "np": 0.0, "nf": -2.3}
        col = {"pep": PEP, "np": NP, "nf": NF}
        name = {"pep": "peptidergic", "np": "non-peptidergic", "nf": "neurofilament"}
        count = {"pep": 8, "np": 6, "nf": 3}
        root = bchip("sensory neurons", GREY, size=26).move_to([-5.0, 0, 0])
        mids, edges = {}, []
        for k in ("pep", "np", "nf"):
            m = bchip(name[k], col[k], size=28).move_to([-1.5, ybr[k], 0])
            mids[k] = m
            edges.append(VMobject().set_points_as_corners(
                [root.get_right() + RIGHT * 0.05, [-3.4, 0, 0], [-3.4, ybr[k], 0], m.get_left() + LEFT * 0.05]
            ).set_stroke(GREY, 3))
        # tips
        tips, tipedges = {}, []
        for k in ("pep", "np", "nf"):
            n = count[k]
            per = 4 if k == "pep" else 3
            pts = []
            for i in range(n):
                r, c = divmod(i, per)
                pts.append([1.1 + c * 0.85, ybr[k] + (0.4 if r == 0 else -0.4) * (1 if n > 3 else 0), 0])
            tips[k] = VGroup(*[Dot(p, radius=0.22, color=col[k], fill_opacity=0.95) for p in pts])
            for p in pts:
                tipedges.append(Line(mids[k].get_right() + RIGHT * 0.05, [p[0] - 0.25, p[1], 0], stroke_width=1.8,
                                     color=GREY, stroke_opacity=0.55))
        cnum = M("3", 110, TEXT, weight=BOLD).move_to([5.3, 0.5, 0])
        clab = T("broad classes", 26, GREY).move_to([5.3, -0.7, 0])
        tag = sketch_tag(4.3, -3.6)
        hb = T("broad classes", 26, TEAL).move_to([-1.5, 3.5, 0])
        hf = T("finer types", 26, TEAL).move_to([2.4, 3.5, 0])

        self.at("Think of a map")
        self.play(FadeIn(root), FadeIn(tag), run_time=0.6)
        self.play(*[Create(e) for e in edges], *[FadeIn(mids[k], shift=RIGHT * 0.2) for k in mids], run_time=0.9)
        self.play(FadeIn(cnum), FadeIn(clab), run_time=0.5)
        self.at("country level")
        self.play(FadeIn(hb, shift=DOWN * 0.1), run_time=0.5)
        self.at("county level")
        self.play(FadeIn(hf, shift=DOWN * 0.1), run_time=0.5)
        self.at("differ in resolution")
        self.play(Indicate(hb, color=TEXT, scale_factor=1.1), Indicate(hf, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.at("Xycel")
        zl = T("Zeisel et al., 2018", 24, GREY).move_to([5.3, -1.6, 0])
        self.play(FadeIn(zl), run_time=0.5)
        self.at("eight peptidergic")
        self.play(*[Create(tipedges[i]) for i in range(8)], FadeIn(tips["pep"], lag_ratio=0.1), run_time=0.9)
        self.at("six")
        self.play(*[Create(tipedges[i]) for i in range(8, 14)], FadeIn(tips["np"], lag_ratio=0.1), run_time=0.8)
        self.at("three neurofilament")
        self.play(*[Create(tipedges[i]) for i in range(14, 17)], FadeIn(tips["nf"], lag_ratio=0.1), run_time=0.7)
        self.at("That makes")
        c2 = M("17", 110, TEXT, weight=BOLD).move_to([5.3, 0.5, 0])
        l2 = T("types", 26, GREY).move_to([5.3, -0.7, 0])
        self.play(ReplacementTransform(cnum, c2), ReplacementTransform(clab, l2), run_time=0.7)
        self.at("finer clustering setting")
        self.play(Indicate(VGroup(*tips.values()), color=TEXT, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Merge(SpokenScene):
    """31 data sets merge into one 18-subtype reference; one group is red, the Atf3 group."""

    def construct(self):
        rng = np.random.default_rng(11)
        mcx, mcy, mw, mh = 2.2, 0.0, 8.0, 5.4
        mapfr = frame_rect(mw, mh, mcx, mcy)
        head = T("one reference: 18 DRG subtypes", 26, TEXT).move_to([mcx, 3.5, 0])
        tag = sketch_tag(mcx + 0.0, -3.5)
        # 31 data sets as small squares
        sq = VGroup(*[Square(side_length=0.26, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35)
                      for _ in range(31)])
        sq.arrange_in_grid(rows=4, cols=8, buff=0.07)
        sq.move_to([-4.3, 2.55, 0])
        cap = T("31 data sets,\nsix mammalian species", 24, GREY, line_spacing=0.9).next_to(sq, DOWN, buff=0.25)
        # 18 clusters
        cells = [(i % 6, i // 6) for i in range(18)]
        pts, cent = [], []
        for (c, r) in cells:
            x = mcx - mw / 2 + 0.75 + c * (mw - 1.5) / 5 + rng.uniform(-0.08, 0.08)
            y = mcy + mh / 2 - 0.8 - r * (mh - 1.6) / 2 + rng.uniform(-0.08, 0.08)
            cent.append((x, y))
            pts.append(cluster_pts((x, y), 7, 0.3, rng))
        atf = 8  # which cluster is the Atf3 group
        D = [dots(p, r=0.09) for p in pts]
        allD = VGroup(*D)
        chips = [bchip("preparation", TEAL, 24), bchip("sequencing depth", TEAL, 24), bchip("analysis", TEAL, 24)]
        for i, c in enumerate(chips):
            c.move_to([-4.3, -0.55 - i * 0.85, 0])
        chead = T("change the count", 24, TEAL).move_to([-4.3, 0.35, 0])

        self.at("merged")
        self.play(FadeIn(sq, lag_ratio=0.03), FadeIn(cap), FadeIn(mapfr), FadeIn(head), FadeIn(tag), run_time=1.2)
        self.at("one reference")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in D], lag_ratio=0.08), run_time=2.0)
        self.at("It holds")
        self.play(Indicate(head, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("preparation")
        self.play(FadeIn(chead), FadeIn(chips[0]), run_time=0.5)
        self.at("sequencing depth")
        self.play(FadeIn(chips[1]), run_time=0.4)
        self.at("analysis")
        self.play(FadeIn(chips[2]), run_time=0.4)
        self.at("how many subtypes")
        self.play(Indicate(head, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("One group is")
        x, y = cent[atf]
        self.play(D[atf].animate.set_color(RED), run_time=0.7)
        self.at("transcription factors")
        ring = Circle(radius=0.55, color=RED, stroke_width=3).move_to([x, y, 0])
        self.play(Create(ring), run_time=0.5)
        self.at("AF -3")
        lab = bchip("Atf3 group", RED, 24).move_to([x, y - 1.05, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.at("types with states")
        q = T("type or state?", 26, TEAL).move_to([x, y + 1.05, 0])
        qb = Rectangle(width=q.width + 0.2, height=q.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(q)
        self.play(FadeIn(qb), FadeIn(q, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Injury(SpokenScene):
    """after nerve injury, type dots lose colour and gather in a red state zone; identity returns."""

    def construct(self):
        rng = np.random.default_rng(5)
        zL = frame_rect(3.5, 4.6, -4.55, 0.2, GREY)
        zR = frame_rect(3.5, 4.6, 4.55, 0.2, RED)
        lL = T("subtype identity", 24, GREY).move_to([-4.55, 2.85, 0])
        lR = T("Atf3-rich state", 24, RED).move_to([4.55, 2.85, 0])
        head = T("in mice, after nerve injury", 26, TEXT).move_to([-2.4, 3.6, 0])
        types = [("subtype 1", NF, 1.45), ("subtype 2", NP, 0.2), ("subtype 3", PEP, -1.05)]
        home, away, D, labs = [], [], [], []
        for (nm, col, y) in types:
            hp = cluster_pts((-4.55, y), 7, 0.5, rng)
            ap = cluster_pts((4.55, y), 7, 0.5, rng)
            home.append(hp)
            away.append(ap)
            D.append(dots(hp, col, r=0.1))
            labs.append(T(nm, 22, col).move_to([-4.55, y - 0.68, 0]))
        tag = sketch_tag(4.2, 3.6)
        # timeline
        tl = Line([-5.8, -2.85, 0], [5.8, -2.85, 0], color=GREY, stroke_width=3)
        tl_a = T("injury", 24, TEXT).move_to([-5.0, -3.35, 0])
        tl_b = T("axons regrow to their targets", 24, TEXT).move_to([3.7, -3.35, 0])
        mark = Dot([-5.8, -2.85, 0], radius=0.11, color=RED)
        out_arr = arr([-2.5, 0.6, 0], [2.5, 0.6, 0], RED)
        back_arr = arr([2.5, -0.6, 0], [-2.5, -0.6, 0], GREEN)
        warn = bchip("timing alone is not proof", TEAL, 24).move_to([0, -1.6, 0])

        self.at("Can a state")
        self.play(FadeIn(zL), FadeIn(lL), run_time=0.5)
        self.play(*[FadeIn(d, lag_ratio=0.1) for d in D], *[FadeIn(l) for l in labs], FadeIn(tag), run_time=0.9)
        self.at("cut or crushed")
        self.play(FadeIn(zR), FadeIn(lR), FadeIn(head), run_time=0.6)
        self.play(FadeIn(tl), FadeIn(tl_a), FadeIn(mark), run_time=0.5)
        self.at("single nuclei")
        sn = bchip("single nuclei sequenced", GREY, 24).move_to([0, 1.7, 0])
        self.play(FadeIn(sn, shift=DOWN * 0.1), run_time=0.5)
        self.at("lost much of")
        self.play(FadeOut(sn), run_time=0.3)
        self.play(Create(out_arr),
                  *[d[j].animate.move_to(away[i][j]).set_color(GREY) for i, d in enumerate(D) for j in range(len(d))],
                  run_time=2.0)
        self.at("time course")
        gap = max(2.0, self.t_of("identity") - self.t_of("time course") - 0.3)
        self.play(FadeIn(tl_b), mark.animate.move_to([5.8, -2.85, 0]).set_color(GREEN), run_time=gap, rate_func=linear)
        self.at("identity")
        self.play(Create(back_arr),
                  *[d[j].animate.move_to(home[i][j]).set_color(types[i][1]) for i, d in enumerate(D) for j in range(len(d))],
                  run_time=2.4)
        self.at("Timing alone")
        self.play(FadeIn(warn, scale=0.9), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """a cluster becomes a type: recurs across data sets, has an independent anchor; read with state and resolution."""

    def construct(self):
        rng = np.random.default_rng(3)
        cx, cy = -4.1, 0.2
        zone = Circle(radius=1.75, color=GREY, stroke_width=3).move_to([cx, cy, 0])
        D = dots(cluster_pts((cx, cy), 18, 1.2, rng), r=0.1)
        lab = T("a cluster", 28, TEXT).move_to([cx, cy - 2.3, 0])
        tag = sketch_tag(-4.1, 3.6)
        rec = bchip("recurs across data sets", TEXT, 28).move_to([-4.1, 2.85, 0])
        anchors = [bchip(t, PURPLE, 28) for t in ("an ending", "a physiology", "a target", "behaviour after manipulation")]
        A = VGroup(*anchors).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.3, 0.3, 0])
        ahead = T("an independent anchor", 28, PURPLE).next_to(A, UP, buff=0.3)
        links = [Line([cx + 1.8, cy, 0], a.get_left() + LEFT * 0.05, color=PURPLE, stroke_width=2, stroke_opacity=0.7)
                 for a in anchors]
        st = bchip("state", RED, 28).move_to([0.4, -3.1, 0])
        rs = bchip("resolution", TEAL, 28).move_to([3.2, -3.1, 0])
        ds = bchip("data set", GREY, 28).move_to([-2.2, -3.1, 0])

        self.at("So what is a type")
        self.play(Create(zone), FadeIn(D, lag_ratio=0.05), FadeIn(lab), FadeIn(tag), run_time=1.0)
        self.at("recurs across")
        self.play(FadeIn(rec, shift=DOWN * 0.1), run_time=0.6)
        self.at("independent anchor")
        self.play(FadeIn(ahead), run_time=0.4)
        self.at("such as an ending")
        self.play(*[Create(l) for l in links], run_time=0.5)
        self.play(LaggedStart(*[FadeIn(a, shift=LEFT * 0.2) for a in anchors], lag_ratio=0.25), run_time=1.6)
        self.at("with its state")
        self.play(FadeIn(st, shift=UP * 0.15), run_time=0.5)
        self.at("and its resolution")
        self.play(FadeIn(rs, shift=UP * 0.15), run_time=0.5)
        self.at("Read each count")
        self.play(FadeIn(ds, shift=UP * 0.15), run_time=0.5)
        self.play(Indicate(VGroup(ds, st, rs), color=TEXT, scale_factor=1.08), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Read each count with its data set, resolution and state."
