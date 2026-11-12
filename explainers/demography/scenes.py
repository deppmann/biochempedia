"""Demography: Survive, Then Give Birth  (Biochemistrypedia film)

COLOR MAP (one colour per concept, whole film)
  TEAL   = living females, l_x bars and tiles (survival)
  GOLD   = daughters, m_x numbers (births); tiles carry a gold edge (l_x x m_x)
  GREY   = a death (dot fades grey), frames, axes
  YELLOW = highlight, the dashed 1 = replacement line, the answer (R0)
  BLUE   = winter / snow
  GREEN  = growth, the check mark; RED = decline, crossed-out things

One world: four age columns (dots on top, bars/tiles underneath), the same x for every age.
"""
import random
from bp_style import *  # noqa: F401,F403

XS = [-5.16, -1.72, 1.72, 5.16]
SP = 0.25
GY0 = 0.4
BASE = -3.55
S = 1.5                 # bar height for 1.0
HY = -0.95              # header slot
LINE_Y = BASE + S       # dashed "1 = replacement"
COUNT_Y = 3.5
AGE_Y = -0.15
N0 = [100, 80, 40, 10]
LX = [1.0, 0.8, 0.4, 0.1]
MXV = [0, 1, 2, 1]
CARD = "#171a23"


def dpos(k, i):
    return np.array([XS[k] + (i % 10 - 4.5) * SP, GY0 + (i // 10) * SP, 0])


def dots(k, n, color=TEAL):
    return [Dot(dpos(k, i), radius=0.09, color=color) for i in range(n)]


def frames():
    return VGroup(*[RoundedRectangle(corner_radius=0.15, width=2.75, height=2.8, stroke_color=GREY,
                                     stroke_width=2, stroke_opacity=0.55).move_to([x, 1.5, 0]) for x in XS])


def age_labels(ks=(0, 1, 2, 3)):
    return VGroup(*[T(f"age {k}", 28, TEXT).move_to([XS[k], AGE_Y, 0]) for k in ks])


def count_lab(k, n, color=TEAL):
    return M(str(n), 34, color).move_to([XS[k], COUNT_Y, 0])


def bar(k, l, w=1.0):
    h = max(l * S, 0.02)
    return Rectangle(width=w, height=h, stroke_color=TEAL, stroke_width=2, fill_color=TEAL,
                     fill_opacity=0.8).move_to([XS[k], BASE + h / 2, 0])


def tile(k, v, y0=BASE):
    h = max(v * S, 0.02)
    return Rectangle(width=1.0, height=h, stroke_color=GOLD, stroke_width=4, fill_color=TEAL,
                     fill_opacity=0.75).move_to([XS[k], y0 + h / 2, 0])


def vlab(k, txt, v, y0=BASE):
    y = y0 + max(v * S, 0.02) + 0.3
    if abs(y - LINE_Y) < 0.2:   # keep the label off the dashed line
        y += 0.32
    return M(txt, 28, TEXT).move_to([XS[k], y, 0])


def stack(vals, x=XS[0]):
    segs, y = [], BASE
    for v in vals:
        t = tile(0, v, y)
        t.move_to([x, y + v * S / 2, 0])
        segs.append(t)
        y += v * S
    return segs


def dashed(color=TEXT, w=3):
    return DashedLine([-6.5, LINE_Y, 0], [6.5, LINE_Y, 0], color=color, stroke_width=w, dash_length=0.2).set_z_index(-1)


def header(text, color=TEXT, x=0.0):
    return T(text, 30, color).move_to([x, HY, 0])


def parents(k):
    n = N0[k]
    top = (n - 1) // 10
    return [top * 10 + c for c in (1, 4, 7) if top * 10 + c < n]


def gold_at(k, j, dx=0.0, op=1.0):
    pi = parents(k)[j]
    return Dot([dpos(k, pi)[0] + dx, 3.05, 0], radius=0.09, color=GOLD).set_opacity(op)


def make_snow(scene, n=12):
    rng = random.Random(7)
    g = VGroup()
    for _ in range(n):
        f = Star(n=6, outer_radius=0.13, inner_radius=0.055, color=BLUE, fill_opacity=0.9, stroke_width=1)
        f.move_to([rng.uniform(-3.75, -3.15), rng.uniform(0.3, 3.0), 0])
        f.v = rng.uniform(0.35, 0.7)
        f.ph = rng.uniform(0, 6)

        def drift(m, dt):
            m.shift(DOWN * m.v * dt)
            m.rotate(0.6 * dt)
            if m.get_y() < 0.25:
                m.shift(UP * 2.8)
        f.add_updater(drift)
        g.add(f)
    scene.add(g)
    return g


def motes(scene):
    rng = random.Random(3)
    g = VGroup()
    for _ in range(14):
        d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0])
        d.v = (rng.uniform(-0.1, 0.1), rng.uniform(0.08, 0.22))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.9:
                m.shift(DOWN * 7.8)
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-10)
    scene.add(g)


def kill(scene, group, rt=0.8):
    group = [d for d in group]
    if not group:
        return
    scene.play(*[d.animate.set_color(GREY) for d in group], run_time=rt * 0.45)
    scene.play(*[FadeOut(d) for d in group], run_time=rt * 0.55)


def check_mark(x, y, color=GREEN):
    return VMobject().set_points_as_corners([[x - 0.3, y, 0], [x - 0.1, y - 0.25, 0], [x + 0.32, y + 0.3, 0]]).set_stroke(color, 9)


def base_state(scene, ns, counts=True, ages=True):
    """Frames, age labels, dots and counts for the four columns; returns dict."""
    fr = frames()
    scene.add(fr)
    d = [dots(k, n) for k, n in enumerate(ns)]
    for g in d:
        scene.add(*g)
    out = {"frames": fr, "dots": d}
    if ages:
        al = age_labels()
        scene.add(al)
        out["ages"] = al
    if counts:
        cl = [count_lab(k, n) for k, n in enumerate(ns)]
        scene.add(*cl)
        out["counts"] = cl
    return out


def lx_state(scene, ks=(0, 1, 2, 3), lvals=LX):
    bars, labs = {}, {}
    for k in ks:
        bars[k] = bar(k, lvals[k])
        labs[k] = vlab(k, f"{lvals[k]:g}" if lvals[k] >= 0.1 else f"{lvals[k]:g}", lvals[k])
        scene.add(bars[k], labs[k])
    return bars, labs


def fmt(v):
    return "1.0" if v == 1 else f"{v:g}"


class S00Title(TitleCard):
    LESSON = "Demography and Survivorship"
    TITLE = "Survive, Then Give Birth"


class S01Question(SpokenScene):
    def construct(self):
        motes(self)
        fr = frames()
        ages = age_labels()
        self.add(fr, ages)
        d0 = dots(0, 100)
        lab = T("100 newborn females", 32, TEAL)
        lab.move_to([-6.7 + lab.width / 2, COUNT_Y, 0])
        self.at("here are a")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in d0], lag_ratio=0.012), FadeIn(lab, shift=UP * 0.1), run_time=2.2)
        self.at("only ten of")
        ghost = VGroup(*[Dot(dpos(3, i), radius=0.09, color=TEAL).set_opacity(0.45) for i in range(10)])
        tag = T("10 reach age 3", 26, YELLOW).move_to([XS[3], 1.7, 0])
        self.play(FadeIn(ghost, scale=0.5), FadeIn(tag, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(ghost, color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.at("can this group")
        q = T("?", 120, YELLOW, weight=BOLD).move_to([0, -1.55, 0])
        qt = T("More than replaces itself?", 40, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.play(Write(qt), run_time=1.3)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S02Cohort(SpokenScene):
    def construct(self):
        motes(self)
        fr = frames()
        ages = age_labels()
        self.add(fr, ages)
        d0 = dots(0, 100)
        self.add(*d0)
        lab = T("100 newborn females", 32, TEAL)
        lab.move_to([-6.7 + lab.width / 2, COUNT_Y, 0])
        self.add(lab)
        c0 = count_lab(0, 100)
        self.play(ReplacementTransform(lab, c0), run_time=0.8)
        self.at("a cohort")
        tag = T("cohort", 30, YELLOW).move_to([XS[0], -0.75, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), fr[0].animate.set_stroke(YELLOW, 4, 1), run_time=0.7)
        self.play(Indicate(VGroup(*d0), color=YELLOW, scale_factor=1.03), run_time=1.0)

        def step(kf, kt, nf, nt, dots_from):
            mv = dots(kf, nf)
            self.add(*mv)
            dx = RIGHT * (XS[kt] - XS[kf])
            return mv, dx

        self.at("follow it")
        mv1 = dots(0, 100)
        self.add(*mv1)
        dx1 = RIGHT * (XS[1] - XS[0])
        self.play(*[d.animate.shift(dx1) for d in mv1], tag.animate.move_to([XS[1], -0.75, 0]),
                  fr[0].animate.set_stroke(GREY, 2, 0.55), fr[1].animate.set_stroke(YELLOW, 4, 1), run_time=1.2)
        self.at("at each age")
        kill(self, mv1[80:], 0.8)
        self.at("count how many")
        c1 = count_lab(1, 80)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("are still alive")
        mv2 = [d.copy() for d in mv1[:80]]
        self.add(*mv2)
        dx2 = RIGHT * (XS[2] - XS[1])
        self.play(*[d.animate.shift(dx2) for d in mv2], tag.animate.move_to([XS[2], -0.75, 0]),
                  fr[1].animate.set_stroke(GREY, 2, 0.55), fr[2].animate.set_stroke(YELLOW, 4, 1), run_time=1.0)
        kill(self, mv2[40:], 0.6)
        c2 = count_lab(2, 40)
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        self.at("those that die")
        mv3 = [d.copy() for d in mv2[:40]]
        self.add(*mv3)
        dx3 = RIGHT * (XS[3] - XS[2])
        self.play(*[d.animate.shift(dx3) for d in mv3], tag.animate.move_to([XS[3], -0.75, 0]),
                  fr[2].animate.set_stroke(GREY, 2, 0.55), fr[3].animate.set_stroke(YELLOW, 4, 1), run_time=1.0)
        self.at("fade to gray")
        kill(self, mv3[10:], 0.7)
        c3 = count_lab(3, 10)
        self.play(FadeIn(c3, shift=UP * 0.1), FadeOut(tag), run_time=0.5)
        self.finish()


class S03Lx(SpokenScene):
    def construct(self):
        motes(self)
        base_state(self, N0)
        self.at("divide each count")
        div = M("n_x / 100", 30, YELLOW).move_to([(XS[0] + XS[1]) / 2, -2.6, 0])
        self.play(FadeIn(div, shift=UP * 0.1), run_time=0.6)
        self.at("starting hundred")
        bars = [bar(k, LX[k]) for k in range(4)]
        labs = [vlab(k, fmt(LX[k]), LX[k]) for k in range(4)]
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=1.6)
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in labs], run_time=0.5)
        self.at("that fraction")
        self.play(FadeOut(div), run_time=0.4)
        self.at("l sub x")
        h = header("l_x = fraction alive at age x", TEAL)
        self.play(Write(h), run_time=1.0)
        self.at("the share of")
        fr = frames()
        for k in range(4):
            self.play(fr[k].animate.set_stroke(TEAL, 5, 1), Indicate(bars[k], color=TEAL, scale_factor=1.08), run_time=0.6)
            self.play(fr[k].animate.set_stroke(GREY, 2, 0.55), run_time=0.2)
        self.at("here it falls")
        self.play(Indicate(bars[0], color=YELLOW, scale_factor=1.1), Indicate(labs[0], color=YELLOW), run_time=0.9)
        self.at("a tenth")
        self.play(Indicate(bars[3], color=YELLOW, scale_factor=1.3), Indicate(labs[3], color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.finish()


class S04Females(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, N0)
        bars, labs = lx_state(self)
        h = header("l_x = fraction alive at age x", TEAL)
        self.add(h)
        golds = []
        rings = []
        self.at("survivors also give")
        for k in (1, 2, 3):
            for j, pi in enumerate(parents(k)):
                r = Circle(radius=0.15, color=GOLD, stroke_width=4).move_to(dpos(k, pi))
                rings.append(r)
        self.play(*[GrowFromCenter(r) for r in rings], run_time=0.8)
        self.at("give birth")
        anims = []
        for k in (1, 2, 3):
            for j, pi in enumerate(parents(k)):
                g = Dot(dpos(k, pi), radius=0.09, color=GOLD)
                self.add(g)
                golds.append(g)
                anims.append(g.animate.move_to([dpos(k, pi)[0], 3.05, 0]))
        self.play(*anims, run_time=1.6)
        self.at("life tables like this")
        self.play(*[Indicate(g, color=GOLD, scale_factor=1.5) for g in golds], run_time=1.2)
        self.at("females only")
        self.play(*[st["dots"][k][0].animate.scale(1.0) for k in range(4)], Indicate(VGroup(*[d for g in st["dots"] for d in g]), color=TEAL, scale_factor=1.02), run_time=1.2)
        self.at("the births we count")
        ban = header("births counted = daughters", GOLD)
        self.play(ReplacementTransform(h, ban), run_time=0.8)
        self.play(*[Indicate(g, color=GOLD, scale_factor=1.6) for g in golds], run_time=1.2)
        self.finish()


def sample_state(scene, doubled=False):
    golds = []
    rings = []
    for k in (1, 2, 3):
        for j, pi in enumerate(parents(k)):
            r = Circle(radius=0.15, color=GOLD, stroke_width=4).move_to(dpos(k, pi))
            rings.append(r)
            dx = -0.12 if (doubled and k == 2) else 0.0
            g = gold_at(k, j, dx)
            golds.append(g)
            scene.add(r, g)
            if doubled and k == 2:
                g2 = gold_at(k, j, 0.12)
                golds.append(g2)
                scene.add(g2)
    return rings, golds


class S05Mx(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, N0)
        bars, labs = lx_state(self)
        h = header("births counted = daughters", GOLD)
        self.add(h)
        rings, golds = sample_state(self)
        self.at("m sub x")
        h2 = header("m_x = average daughters per female", GOLD)
        self.play(ReplacementTransform(h, h2), run_time=0.9)
        self.at("per living female")
        self.play(*[Indicate(r, color=YELLOW, scale_factor=1.4) for r in rings], run_time=1.4)
        self.at("here the averages")
        nums = [M(str(MXV[k]), 44, GOLD).move_to([XS[k] + 1.05, BASE + 0.8, 0]) for k in range(4)]
        self.play(Indicate(h2, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("zero in the first")
        self.play(FadeIn(nums[0], scale=0.5), run_time=0.6)
        self.at("then one")
        self.play(FadeIn(nums[1], scale=0.5), run_time=0.5)
        self.at("two")
        new = [gold_at(2, j, 0.12) for j in range(len(parents(2)))]
        olds = [g for g in golds if abs(g.get_x() - dpos(2, parents(2)[0])[0]) < 0.01 or True]
        g2 = [g for g in golds if g.get_x() > XS[2] - 1.4 and g.get_x() < XS[2] + 1.4]
        for g, nw in zip(g2, new):
            self.add(nw)
        self.play(*[g.animate.shift(LEFT * 0.12) for g in g2], FadeIn(nums[2], scale=0.5),
                  *[nw.animate.scale(1.0) for nw in new], run_time=0.8)
        self.at("and one")
        self.play(FadeIn(nums[3], scale=0.5), run_time=0.5)
        self.finish()


class S06Product(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, N0)
        bars, labs = lx_state(self)
        h = header("m_x = average daughters per female", GOLD)
        self.add(h)
        rings, golds = sample_state(self, doubled=True)
        nums = [M(str(MXV[k]), 44, GOLD).move_to([XS[k] + 1.05, BASE + 0.8, 0]) for k in range(4)]
        self.add(*nums)
        self.at("the key step")
        h2 = header("l_x × m_x", YELLOW)
        self.play(ReplacementTransform(h, h2), run_time=0.8)
        self.at("a newborn female")
        ring = Circle(radius=0.17, color=YELLOW, stroke_width=5).move_to(dpos(0, 90))
        self.play(GrowFromCenter(ring), run_time=0.6)
        self.at("to a given age")
        q = T("?", 44, YELLOW, weight=BOLD).move_to([XS[3], 1.0, 0])
        self.play(ring.animate.move_to(dpos(3, 4)), run_time=1.3)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("her daughters there")
        self.play(FadeOut(q), FadeOut(ring), run_time=0.4)
        self.at("only as far as")
        ops = {1: 0.8, 2: 0.4, 3: 0.1}
        anims = []
        for g in golds:
            k = 1 if g.get_x() < 0 else (2 if g.get_x() < 3.4 else 3)
            anims.append(g.animate.set_opacity(ops[k]))
        self.play(*anims, *[FadeOut(r) for r in rings], run_time=1.6)
        self.at("multiply the share")
        self.play(*[Indicate(bars[k], color=YELLOW, scale_factor=1.06) for k in range(4)], run_time=1.2)
        self.at("by the daughters")
        tiles = [tile(k, LX[k] * MXV[k]) for k in range(4)]
        newl = [vlab(k, fmt(round(LX[k] * MXV[k], 2)), LX[k] * MXV[k]) for k in range(4)]
        self.play(*[Transform(bars[k], tiles[k]) for k in range(4)],
                  *[Transform(labs[k], newl[k]) for k in range(4)],
                  *[nums[k].animate.move_to([XS[k], BASE + max(LX[k] * MXV[k], 0.05) * S / 2, 0]).set_opacity(0) for k in range(4)],
                  *[FadeOut(g) for g in golds], run_time=1.8)
        self.play(*[Indicate(bars[k], color=GOLD, scale_factor=1.1) for k in (1, 2, 3)], run_time=0.9)
        self.at("that is what")
        h3 = header("expected daughters per newborn", YELLOW)
        self.play(ReplacementTransform(h2, h3), run_time=0.8)
        self.at("can expect")
        for k in (1, 2, 3):
            self.play(Indicate(bars[k], color=YELLOW, scale_factor=1.12), Indicate(labs[k], color=YELLOW), run_time=0.9)
        self.finish()


class S07Sum(SpokenScene):
    def construct(self):
        motes(self)
        base_state(self, N0)
        vals = [LX[k] * MXV[k] for k in range(4)]
        tiles = [tile(k, vals[k]) for k in range(4)]
        labs = [vlab(k, fmt(round(vals[k], 2)), vals[k]) for k in range(4)]
        h = header("expected daughters per newborn", YELLOW)
        self.add(*tiles, *labs, h)
        segs = stack(vals[1:])
        self.at("add those pieces")
        self.play(FadeOut(h), FadeOut(labs[0]), FadeOut(tiles[0]), *[FadeOut(l) for l in labs[1:]], run_time=0.3)
        self.play(tiles[1].animate.move_to(segs[0].get_center()), run_time=0.8)
        self.at("across her whole")
        self.play(tiles[2].animate.move_to(segs[1].get_center()), run_time=0.6)
        self.at("whole life")
        self.play(tiles[3].animate.move_to(segs[2].get_center()), run_time=0.9)
        self.at("the total is")
        top = BASE + 1.7 * S
        r0 = M("R0", 32, YELLOW).move_to([XS[0], -0.62, 0])
        self.play(FadeIn(r0, shift=UP * 0.1), Indicate(VGroup(*tiles[1:]), color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.at("daughters left by")
        self.play(Indicate(VGroup(*tiles[1:]), color=YELLOW, scale_factor=1.08), run_time=1.0)
        dl = dashed()
        dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        self.at("average newborn female")
        self.play(Create(dl), FadeIn(dlab), run_time=1.3)
        self.at("here it comes to")
        r0b = M("R0 = 1.7", 32, YELLOW).move_to([XS[0], -0.62, 0])
        eq = M("R0 = 0 + 0.8 + 0.8 + 0.1 = 1.7", 26, TEXT).move_to([1.6, HY, 0])
        self.play(ReplacementTransform(r0, r0b), Write(eq), run_time=1.3)
        chk = T("80 + 80 + 10 = 170 daughters\nfrom 100 founders", 26, GOLD).move_to([1.4, -2.95, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.7)
        self.finish()


def s08_state(scene, with_eq=True):
    segs = stack([0.8, 0.8, 0.1])
    scene.add(*segs)
    r0 = M("R0 = 1.7", 32, YELLOW).move_to([XS[0], -0.62, 0])
    dl = dashed()
    dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
    scene.add(r0, dl, dlab)
    extra = []
    if with_eq:
        eq = M("R0 = 0 + 0.8 + 0.8 + 0.1 = 1.7", 26, TEXT).move_to([1.6, HY, 0])
        chk = T("80 + 80 + 10 = 170 daughters\nfrom 100 founders", 26, GOLD).move_to([1.4, -2.95, 0])
        scene.add(eq, chk)
        extra = [eq, chk]
    return segs, r0, dl, dlab, extra


class S08Rule(SpokenScene):
    def construct(self):
        motes(self)
        base_state(self, N0)
        segs, r0, dl, dlab, extra = s08_state(self)
        self.at("the dashed line marks")
        self.play(*[FadeOut(e) for e in extra], dl.animate.set_stroke(YELLOW, 6), run_time=0.9)
        self.play(Indicate(dlab, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.at("at one each female")
        self.play(Flash(dl.get_center() + RIGHT * 2, color=YELLOW, flash_radius=0.4), Indicate(dlab, color=YELLOW), run_time=1.0)
        self.at("replaces herself")
        rep = T("replacement", 30, YELLOW).move_to([5.0, LINE_Y + 0.33, 0])
        self.play(ReplacementTransform(dlab, rep), run_time=0.7)
        self.at("above it")
        gro = T("growth", 32, GREEN).move_to([5.4, LINE_Y + 0.95, 0])
        garr = Arrow([4.3, LINE_Y + 0.55, 0], [4.3, LINE_Y + 1.25, 0], color=GREEN, buff=0, stroke_width=6)
        glow = Rectangle(width=1.0, height=1.05 * 1, stroke_color=YELLOW, stroke_width=5, fill_opacity=0).move_to([XS[0], LINE_Y + 0.525, 0])
        self.play(FadeIn(gro, shift=UP * 0.1), GrowArrow(garr), Create(glow), run_time=0.9)
        self.at("each generation is larger")
        gens_up = VGroup()
        for i, n in enumerate((2, 3, 4)):
            for j in range(n):
                gens_up.add(Dot([0.2 + i * 1.3 + j * 0.2, LINE_Y + 0.6, 0], radius=0.08, color=TEAL))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in gens_up], lag_ratio=0.1), run_time=2.2)
        self.at("below it")
        dec = T("decline", 32, RED).move_to([5.4, LINE_Y - 0.95, 0])
        darr = Arrow([4.3, LINE_Y - 0.5, 0], [4.3, LINE_Y - 1.3, 0], color=RED, buff=0, stroke_width=6)
        self.play(FadeIn(dec, shift=DOWN * 0.1), GrowArrow(darr), run_time=0.9)
        self.at("each is smaller")
        gens_dn = VGroup()
        for i, n in enumerate((4, 3, 2)):
            for j in range(n):
                gens_dn.add(Dot([0.2 + i * 1.3 + j * 0.2, LINE_Y - 0.7, 0], radius=0.08, color=TEAL))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in gens_dn], lag_ratio=0.1), run_time=1.8)
        self.at("so yes")
        ck = check_mark(-3.3, -0.62)
        self.play(Create(ck), Indicate(r0, color=GREEN, scale_factor=1.15), run_time=1.0)
        self.play(Indicate(VGroup(*segs), color=YELLOW, scale_factor=1.06), run_time=1.2)
        self.finish()


def bars_state(scene, lv):
    bars, labs = {}, {}
    for k in (1, 2, 3):
        bars[k] = bar(k, lv[k])
        labs[k] = vlab(k, fmt(lv[k]), lv[k])
        scene.add(bars[k], labs[k])
    return bars, labs


class S09Predict(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, N0)
        segs, r0, dl, dlab, extra = s08_state(self, with_eq=False)
        dlab2 = T("replacement", 30, YELLOW)
        gro = T("growth", 32, GREEN).move_to([5.4, LINE_Y + 0.95, 0])
        dec = T("decline", 32, RED).move_to([5.4, LINE_Y - 0.95, 0])
        ck = check_mark(-3.3, -0.62)
        self.remove(dlab)
        rep = T("replacement", 30, YELLOW).move_to([5.0, LINE_Y + 0.33, 0])
        self.add(gro, dec, ck, rep)
        dl.set_stroke(YELLOW, 6)
        self.at("now give the cohort")
        self.play(FadeOut(gro), FadeOut(dec), FadeOut(ck), FadeOut(rep), dl.animate.set_stroke(TEXT, 3), run_time=0.4)
        snow = make_snow(self)
        newlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        bars = {k: bar(k, LX[k]) for k in (1, 2, 3)}
        labs = {k: vlab(k, fmt(LX[k]), LX[k]) for k in (1, 2, 3)}
        self.play(FadeIn(newlab), *[FadeIn(bars[k], shift=UP * 0.2) for k in bars], *[FadeIn(labs[k]) for k in labs], run_time=1.0)
        self.at("hard first winter")
        self.play(Indicate(snow, color=BLUE, scale_factor=1.3), run_time=1.4)
        self.at("only half as many")
        dead = st["dots"][1][40:]
        c1 = count_lab(1, 40)
        self.play(*[d.animate.set_color(GREY) for d in dead], run_time=0.5)
        self.play(*[FadeOut(d) for d in dead], ReplacementTransform(st["counts"][1], c1),
                  Transform(bars[1], bar(1, 0.4)), Transform(labs[1], vlab(1, "0.4", 0.4)), run_time=1.1)
        self.at("what happens to")
        q = M("R0 = ?", 32, YELLOW).move_to([XS[0], -0.62, 0])
        self.play(ReplacementTransform(r0, q), run_time=0.7)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


def s10_state(scene):
    st = base_state(scene, [100, 40, 40, 10])
    for k, n in ((1, 80),):
        pass
    segs = stack([0.8, 0.8, 0.1])
    scene.add(*segs)
    q = M("R0 = ?", 32, YELLOW).move_to([XS[0], -0.62, 0])
    dl = dashed()
    dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
    scene.add(q, dl, dlab)
    lv = {1: 0.4, 2: 0.4, 3: 0.1}
    bars, labs = {}, {}
    for k in (1, 2, 3):
        bars[k] = bar(k, lv[k])
        labs[k] = vlab(k, fmt(lv[k]), lv[k])
        scene.add(bars[k], labs[k])
    return st, segs, q, bars, labs


class S10Pause(NarratedScene):
    def construct(self):
        motes(self)
        # the question from the previous scene, held still: snow keeps drifting
        st = base_state(self, [100, 40, 40, 10])
        segs = stack([0.8, 0.8, 0.1])
        self.add(*segs)
        q = M("R0 = ?", 32, YELLOW).move_to([XS[0], -0.62, 0])
        dl = dashed()
        dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        self.add(q, dl, dlab)
        # (dots of column 1 start from 40; the real column keeps its first 40 dots)
        # base_state drew dots from the counts given: columns 1-3 hold 40, 40, 10
        for k, v in ((1, 0.4), (2, 0.4), (3, 0.1)):
            self.add(bar(k, v), vlab(k, fmt(v), v))
        make_snow(self)
        pt = T("Predict: what happens to R0?", 34, YELLOW).move_to([0.6, HY, 0])
        self.play(FadeIn(pt, shift=UP * 0.1), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.2)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.2)
        self.finish()


class S11Reveal(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, [100, 40, 40, 10])
        segs = stack([0.8, 0.8, 0.1])
        self.add(*segs)
        q = M("R0 = ?", 32, YELLOW).move_to([XS[0], -0.62, 0])
        dl = dashed()
        dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        self.add(q, dl, dlab)
        bars = {}
        labs = {}
        for k, v in ((1, 0.4), (2, 0.4), (3, 0.1)):
            bars[k] = bar(k, v)
            labs[k] = vlab(k, fmt(v), v)
            self.add(bars[k], labs[k])
        snow = make_snow(self)
        pt = T("Predict: what happens to R0?", 34, YELLOW).move_to([0.6, HY, 0])
        self.add(pt)
        self.at("keep every later")
        chip_ = chip("later rates unchanged", YELLOW, 28).move_to([1.7, HY, 0])
        self.play(ReplacementTransform(pt, chip_), run_time=0.8)
        self.at("birth rate the same")
        self.play(Indicate(chip_, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("every female alive")
        ic = Star(n=6, outer_radius=0.3, inner_radius=0.13, color=BLUE, fill_opacity=0.9).move_to([-3.44, 3.1, 0])
        arr = Arrow([-3.1, 3.1, 0], [6.4, 3.1, 0], color=BLUE, buff=0, stroke_width=6)
        self.play(FadeIn(ic, scale=0.5), run_time=0.4)
        self.play(GrowArrow(arr), run_time=3.2)
        self.at("so the share alive halves")
        dead2 = st["dots"][2][20:]
        c2 = count_lab(2, 20)
        self.play(*[d.animate.set_color(GREY) for d in dead2], run_time=0.4)
        self.play(*[FadeOut(d) for d in dead2], ReplacementTransform(st["counts"][2], c2),
                  Transform(bars[2], bar(2, 0.2)), Transform(labs[2], vlab(2, "0.2", 0.2)), run_time=1.0)
        self.at("at every later age")
        dead3 = st["dots"][3][5:]
        c3 = count_lab(3, 5)
        self.play(*[d.animate.set_color(GREY) for d in dead3], run_time=0.4)
        self.play(*[FadeOut(d) for d in dead3], ReplacementTransform(st["counts"][3], c3),
                  Transform(bars[3], bar(3, 0.05)), Transform(labs[3], vlab(3, "0.05", 0.05)), run_time=1.0)
        self.at("not just at age one")
        self.play(Indicate(bars[1], color=YELLOW, scale_factor=1.15), Indicate(labs[1], color=YELLOW), run_time=1.2)
        self.finish()


class S12Cut(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, [100, 40, 20, 5])
        segs = stack([0.8, 0.8, 0.1])
        self.add(*segs)
        q = M("R0 = ?", 32, YELLOW).move_to([XS[0], -0.62, 0])
        dl = dashed()
        dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        self.add(q, dl, dlab)
        lv = {1: 0.4, 2: 0.2, 3: 0.05}
        bars, labs = {}, {}
        for k in (1, 2, 3):
            bars[k] = bar(k, lv[k])
            labs[k] = vlab(k, fmt(lv[k]), lv[k])
            self.add(bars[k], labs[k])
        ic = Star(n=6, outer_radius=0.3, inner_radius=0.13, color=BLUE, fill_opacity=0.9).move_to([-3.44, 3.1, 0])
        arr = Arrow([-3.1, 3.1, 0], [6.4, 3.1, 0], color=BLUE, buff=0, stroke_width=6)
        self.add(ic, arr)
        self.at("every piece of")
        h = header("l_x × m_x", YELLOW)
        tv = {1: 0.4, 2: 0.4, 3: 0.05}
        tiles = {k: tile(k, tv[k]) for k in (1, 2, 3)}
        tl = {k: vlab(k, fmt(tv[k]), tv[k]) for k in (1, 2, 3)}
        self.play(FadeOut(ic), FadeOut(arr), FadeIn(h), *[Transform(bars[k], tiles[k]) for k in (1, 2, 3)],
                  *[Transform(labs[k], tl[k]) for k in (1, 2, 3)], run_time=1.6)
        self.at("so r0 halves too")
        newsegs = stack([0.4, 0.4, 0.05])
        r0n = M("R0 = 0.85", 32, YELLOW).move_to([XS[0], -1.5, 0])
        self.play(*[FadeOut(s) for s in segs], *[FadeOut(l) for l in labs.values()], FadeOut(h),
                  *[bars[k].animate.move_to(newsegs[k - 1].get_center()) for k in (1, 2, 3)],
                  ReplacementTransform(q, r0n), run_time=1.5)
        self.at("below the line")
        self.play(Indicate(r0n, color=RED, scale_factor=1.2), VGroup(*[bars[k] for k in (1, 2, 3)]).animate.set_opacity(0.55), run_time=1.2)
        self.at("survival to any age")
        parts = [T("l_3", 34, TEAL), T("=", 34), T("p_0", 34, BLUE), T("×", 34), T("p_1", 34, TEXT), T("×", 34), T("p_2", 34, TEXT)]
        eq = VGroup(*parts).arrange(RIGHT, buff=0.25).move_to([1.0, HY + 0.1, 0])
        self.play(Write(eq), run_time=1.2)
        self.at("product of every year")
        for i, k in zip((2, 4, 6), (1, 2, 3)):
            self.play(Indicate(parts[i], color=YELLOW, scale_factor=1.35),
                      Indicate(VGroup(*st["dots"][k]), color=YELLOW, scale_factor=1.12),
                      st["frames"][k].animate.set_stroke(YELLOW, 5, 1), run_time=0.8)
            self.play(st["frames"][k].animate.set_stroke(GREY, 2, 0.55), run_time=0.2)
        self.at("so a loss early")
        self.play(Indicate(parts[2], color=BLUE, scale_factor=1.6),
                  Indicate(VGroup(*st["dots"][1]), color=BLUE, scale_factor=1.15), run_time=1.0)
        self.play(Indicate(VGroup(*st["dots"][3]), color=BLUE, scale_factor=1.4),
                  Indicate(VGroup(*st["dots"][2]), color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("cuts every later")
        self.play(Wiggle(VGroup(*[bars[k] for k in (1, 2, 3)]), scale_value=1.15, rotation_angle=0.05 * TAU),
                  Indicate(r0n, color=RED, scale_factor=1.25), run_time=1.6)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        motes(self)
        st = base_state(self, [100, 40, 20, 5])
        segs = stack([0.4, 0.4, 0.05])
        for s in segs:
            s.set_opacity(0.55)
        self.add(*segs)
        r0n = M("R0 = 0.85", 32, YELLOW).move_to([XS[0], -1.5, 0])
        dl = dashed()
        dlab = T("1 = replacement", 28, TEXT).move_to([5.0, LINE_Y + 0.33, 0])
        self.add(r0n, dl, dlab)
        self.at("two cautions")
        gone = [st["frames"], st["ages"], *st["counts"], *[d for g in st["dots"] for d in g]]
        cardA = RoundedRectangle(corner_radius=0.2, width=6.2, height=3.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=CARD, fill_opacity=1).move_to([-3.2, 1.35, 0])
        cardB = RoundedRectangle(corner_radius=0.2, width=6.2, height=3.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=CARD, fill_opacity=1).move_to([3.3, 1.35, 0])
        self.play(*[FadeOut(m) for m in gone], FadeIn(cardA, shift=RIGHT * 1.5), FadeIn(cardB, shift=LEFT * 1.5), run_time=1.6)
        self.at("r0 is counted")
        clock = VGroup(Circle(radius=0.6, color=TEXT, stroke_width=5),
                       Line([0, 0, 0], [0, 0.42, 0], color=TEXT, stroke_width=5),
                       Line([0, 0, 0], [0.3, 0.0, 0], color=TEXT, stroke_width=5)).move_to([-3.2, 2.55, 0])
        hand = clock[1]
        hand.add_updater(lambda m, dt: m.rotate(-3.0 * dt, about_point=clock[0].get_center()))
        self.play(FadeIn(clock, scale=0.6), run_time=0.8)
        self.at("per generation")
        self.play(Indicate(r0n, color=YELLOW, scale_factor=1.2), run_time=0.8)
        ta = T("per generation,\nnot per year", 32, YELLOW).move_to([-3.2, 1.05, 0])
        self.play(Write(ta), run_time=1.0)
        self.at("not per year")
        strike = Line([-4.0, 3.1, 0], [-2.4, 2.0, 0], color=RED, stroke_width=8)
        self.play(Create(strike), run_time=0.7)
        self.at("a yearly rate")
        ga = DoubleArrow([-5.4, 0.1, 0], [-1.0, 0.1, 0], color=GOLD, buff=0, stroke_width=6)
        gl = T("length of a generation", 26, GOLD).move_to([-3.2, -0.2, 0])
        self.play(GrowArrow(ga), FadeIn(gl, shift=UP * 0.1), run_time=1.2)
        self.at("and r0 predicts")
        self.play(Indicate(r0n, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("the rates stay fixed")
        fence = Rectangle(width=2.0, height=1.3, stroke_color=YELLOW, stroke_width=6).move_to([3.3, 2.45, 0])
        inside = VGroup(*[Dot([2.75 + (i % 4) * 0.37, 2.2 + (i // 4) * 0.5, 0], radius=0.1, color=TEAL) for i in range(8)])
        tb = T("fixed rates,\nno migration", 32, YELLOW).move_to([3.3, 0.85, 0])
        for i, dd in enumerate(inside):
            dd.ph = i * 0.9
            dd.t = 0.0
            dd.base = dd.get_center().copy()
            dd.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to(m.base + np.array([0.06 * np.sin(2.5 * m.t + m.ph), 0.06 * np.cos(2.1 * m.t + m.ph), 0]))))
        self.play(Create(fence), FadeIn(inside, scale=0.5), Write(tb), run_time=1.4)
        self.at("nobody arrives")
        a_in = Arrow([0.6, 2.45, 0], [2.2, 2.45, 0], color=TEXT, buff=0, stroke_width=6)
        a_out = Arrow([4.4, 2.45, 0], [6.0, 2.45, 0], color=TEXT, buff=0, stroke_width=6)
        x1 = VGroup(Line([1.15, 2.7, 0], [1.65, 2.2, 0]), Line([1.15, 2.2, 0], [1.65, 2.7, 0])).set_stroke(RED, 8)
        x2 = VGroup(Line([4.95, 2.7, 0], [5.45, 2.2, 0]), Line([4.95, 2.2, 0], [5.45, 2.7, 0])).set_stroke(RED, 8)
        self.play(GrowArrow(a_in), GrowArrow(a_out), run_time=0.8)
        self.play(Create(x1), Create(x2), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Survival times births, summed over a life: above one means growth."
