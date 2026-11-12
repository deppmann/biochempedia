"""Divided, Not Grown (Biochemistrypedia explainer, animal development)

COLOUR MAP: egg cytoplasm pale cream; inherited material (determinant) PURPLE dots; signals GREEN;
ectoderm BLUE, mesoderm RED, endoderm YELLOW; calcium wave bright white-cyan; yolk pale tan.
One world: the egg sits at the same place and scale (centre EC, radius R) in every scene.
Cleavage geometry is schematic (a cross-section cut by axis-aligned furrows); numbers on screen are computed.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

CREAM = "#F2E8C8"
TAN = "#C9A96A"
PURPLE = "#A66DFF"
CYAN = "#7FF0FF"
NUC = "#1B2A4A"
R = 2.8
EC = np.array([-2.7, -0.1, 0.0])
RX = 3.5          # centre x of the right-hand panel


# ---------------------------------------------------------------- geometry (convex clipping)
def _clip(pts, axis, val, keep_hi):
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        ina = (a[axis] >= val) if keep_hi else (a[axis] <= val)
        inb = (b[axis] >= val) if keep_hi else (b[axis] <= val)
        if ina:
            out.append(a)
        if ina != inb:
            t = (val - a[axis]) / (b[axis] - a[axis])
            out.append(a + t * (b - a))
    return out


def _build():
    th = np.linspace(0, 2 * np.pi, 96, endpoint=False)
    disc = [np.array([R * np.cos(t), R * np.sin(t)]) for t in th]
    stages = [[{"pts": disc, "rect": (-R, R, -R, R)}]]
    for k in range(5):
        new = []
        for c in stages[-1]:
            xs = [p[0] for p in c["pts"]]
            ys = [p[1] for p in c["pts"]]
            w, h = max(xs) - min(xs), max(ys) - min(ys)
            vertical = w > h * 1.05 or (abs(w - h) <= 0.05 * h and k % 2 == 0)
            x0, x1, y0, y1 = c["rect"]
            if vertical:
                m = (min(xs) + max(xs)) / 2
                new.append({"pts": _clip(c["pts"], 0, m, False), "rect": (x0, m, y0, y1)})
                new.append({"pts": _clip(c["pts"], 0, m, True), "rect": (m, x1, y0, y1)})
            else:
                m = (min(ys) + max(ys)) / 2
                new.append({"pts": _clip(c["pts"], 1, m, False), "rect": (x0, x1, y0, m)})
                new.append({"pts": _clip(c["pts"], 1, m, True), "rect": (x0, x1, m, y1)})
        stages.append(new)
    return stages


STAGES = _build()


def _centroid(c):
    P = np.array(c["pts"])
    return P.mean(axis=0)


def to3(p, origin=None):
    o = EC if origin is None else origin
    return np.array([p[0] + o[0], p[1] + o[1], 0.0])


def cell_mob(c, color=CREAM, origin=None, scale=1.0, shift=0.0):
    pts = [to3(p * scale, origin) + shift for p in c["pts"]]
    m = Polygon(*pts, stroke_color=BG, stroke_width=5, fill_color=color, fill_opacity=1.0)
    m.set_z_index(1)
    return m


def cells_k(k, color=CREAM):
    return [cell_mob(c, color) for c in STAGES[k]]


# purple patch: fixed dots in egg coordinates (anchored)
def _patch():
    rng = np.random.RandomState(7)
    pts = []
    cx, cy, rr = -0.48 * R, -0.38 * R, 0.36 * R
    tries = 0
    while len(pts) < 30 and tries < 4000:
        tries += 1
        a = rng.uniform(0, 2 * np.pi)
        r = rr * np.sqrt(rng.uniform())
        p = np.array([cx + r * np.cos(a), cy + r * np.sin(a)])
        if np.hypot(*p) > R - 0.15:
            continue
        if all(np.hypot(*(p - q)) > 0.19 for q in pts):
            pts.append(p)
    return pts


PATCH = _patch()


def inside(c, p):
    x0, x1, y0, y1 = c["rect"]
    return x0 <= p[0] < x1 and y0 <= p[1] < y1


PURPLE_CELLS = [i for i, c in enumerate(STAGES[5]) if any(inside(c, p) for p in PATCH)]
PLAIN_CELLS = [i for i in range(32) if i not in PURPLE_CELLS]


def patch_dots(opacity=1.0):
    g = VGroup(*[Dot(to3(p), radius=0.085, color=PURPLE) for p in PATCH])
    g.set_z_index(6)
    g.set_opacity(opacity)
    t = {"v": 0.0}
    for i, d in enumerate(g):
        d.ph = i * 0.7

    def shimmer(m, dt):
        t["v"] += dt
        for d in m:
            d.set_opacity(0.75 + 0.25 * np.sin(2.2 * t["v"] + d.ph))
    g.add_updater(shimmer)
    return g


def make_motes(n=16, seed=1, origin=None, rad=None, color="#D9C58A"):
    o = EC if origin is None else origin
    rr = (R - 0.2) if rad is None else rad
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        a = rng.uniform(0, 2 * np.pi)
        r = rr * np.sqrt(rng.uniform())
        d = Dot(o + np.array([r * np.cos(a), r * np.sin(a), 0]), radius=0.045, color=color)
        d.set_opacity(0.8)
        d.v = np.array([rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35), 0])

        def drift(m, dt, o=o, rr=rr):
            m.shift(m.v * dt)
            rel = m.get_center() - o
            if np.hypot(rel[0], rel[1]) > rr:
                m.v = -m.v
                m.shift(m.v * dt * 2)
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(2)
    return g


def make_outline(color=GREY, dashes=48):
    o = DashedVMobject(Circle(radius=R + 0.14, color=color, stroke_width=3.5), num_dashes=dashes)
    o.move_to(EC)
    o.set_z_index(3)
    o.add_updater(lambda m, dt: m.rotate(0.15 * dt, about_point=EC))
    return o


def nuclei_for(k, color=NUC):
    g = VGroup()
    for c in STAGES[k]:
        d = Dot(to3(_centroid(c)), radius=0.12, color=color)
        d.set_stroke(TEXT, 1.5)
        g.add(d)
    g.set_z_index(4)
    return g


def put(m, x, y, max_w=6.0):
    if m.width > max_w:
        m.scale(max_w / m.width)
    return m.move_to([x, y, 0])


def lab(text, size=30, color=TEXT, **kw):
    return T(text, size=max(size, 33), color=color, **kw)


def ring_timer(x=6.0, y=-3.1, r=0.4):
    tr = ValueTracker(0)
    base = Circle(radius=r, color=GREY, stroke_width=4).move_to([x, y, 0])
    arc = always_redraw(lambda: Arc(radius=r, start_angle=PI / 2, angle=-max(0.001, tr.get_value()) * TAU,
                                    color=TEAL, stroke_width=7).move_to([x, y, 0]))
    return tr, base, arc


class EggScene(SpokenScene):
    """Carries the cleavage state of one egg in the same place every scene."""

    def start_egg(self, k=0, outline=True, motes=True, seed=1):
        self.k = k
        self.cm = cells_k(k)
        self.cells = VGroup(*self.cm)
        self.add(self.cells)
        self.outline = None
        self.motes = None
        if outline:
            self.outline = make_outline()
            self.add(self.outline)
        if motes:
            self.motes = make_motes(seed=seed)
            self.add(self.motes)

    def split_to(self, k, run=0.8):
        """Cut every cell in two (stage k-1 -> k): each parent turns into its two children."""
        parents = self.cm
        kids = cells_k(k)
        anims = [ReplacementTransform(parents[i], VGroup(kids[2 * i], kids[2 * i + 1])) for i in range(len(parents))]
        self.play(*anims, run_time=run)
        self.cm = kids
        self.k = k
        self.cells = VGroup(*kids)

    def reset_egg(self, run=0.8):
        """Back to one cell (the cells fade into the single egg)."""
        new = cells_k(0)
        self.play(FadeOut(VGroup(*self.cm)), FadeIn(new[0]), run_time=run)
        self.cm = new
        self.k = 0
        self.cells = VGroup(*new)

    def purple_outline(self):
        g = VGroup()
        for i in PURPLE_CELLS:
            c = STAGES[5][i]
            m = Polygon(*[to3(p) for p in c["pts"]], stroke_color=PURPLE, stroke_width=7, fill_opacity=0)
            m.set_z_index(5)
            g.add(m)
        return g


# ================================================================= scenes
class S00Title(TitleCard):
    TITLE = "Divided, Not Grown"
    LESSON = "Animal development"


class S01Hook(EggScene):
    def construct(self):
        self.start_egg(0)
        self.play(FadeIn(self.cells), run_time=0.6)
        l1 = put(lab("frog egg: one cell"), RX, 2.0)
        a1 = Arrow([RX - 2.2, 1.7, 0], [EC[0] + R * 0.8, 0.9, 0], color=GREY, buff=0.1, stroke_width=4)
        self.play(FadeIn(l1), GrowArrow(a1), run_time=0.4)
        self.at("thousands of cells")
        cnt = put(lab("1 cell → thousands of cells", color=YELLOW), RX, 0.2)
        self.add(cnt)
        for k in range(1, 6):
            self.split_to(k, run=0.2)
        self.at("without growing at all")
        o2 = DashedVMobject(Circle(radius=R + 0.14, color=TEXT, stroke_width=4.5), num_dashes=48).move_to(EC)
        o2.set_z_index(3)
        ng = put(lab("no growth", color=TEXT, weight=BOLD, size=36), RX, -1.4)
        self.play(Create(o2), FadeIn(ng), run_time=0.9)
        self.play(Indicate(ng, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("So where do the cells")
        q = Text("?", font=TITLE_FONT, font_size=170, color=YELLOW).move_to([RX, -0.5, 0])
        self.play(FadeOut(VGroup(*self.cm)), FadeOut(o2), FadeOut(ng), FadeOut(cnt), run_time=0.8)
        one = cells_k(0)
        self.cm = one
        self.play(FadeIn(one[0]), FadeIn(q, scale=0.6), run_time=0.8)
        self.at("what does each one get")
        t = {"v": 0.0}
        q.add_updater(lambda m, dt: (t.__setitem__("v", t["v"] + dt), m.set_opacity(0.75 + 0.25 * np.sin(4 * t["v"])))[0])
        self.finish()


class S02Fert(EggScene):
    def construct(self):
        self.start_egg(0)
        P = np.array([0.96, 2.63])                      # point of sperm entry (egg coordinates)
        tgt = to3(P)

        def sperm(head, angle=0.0):
            h = Ellipse(width=0.6, height=0.4, color=TEXT, fill_opacity=1, stroke_width=0).move_to(head)
            tail = ParametricFunction(lambda s: np.array([s, 0.12 * np.sin(8 * s), 0]), t_range=[0, 1.5], color=TEXT, stroke_width=6)
            tail.move_to(head + RIGHT * (0.3 + 0.75))
            g = VGroup(h, tail)
            return g.rotate(angle, about_point=head)
        ttl = put(lab("fertilization", color=TEAL, size=36, weight=BOLD), RX, 3.1)
        self.play(FadeIn(ttl), run_time=0.6)
        self.at("A sperm fuses")
        s1 = sperm(tgt + np.array([1.9, 0.5, 0]), 0.0)
        self.play(FadeIn(s1), run_time=0.4)
        self.play(s1.animate.shift(np.array([-1.75, -0.45, 0])), run_time=1.1, rate_func=smooth)
        flash = Circle(radius=0.1, color=CYAN, fill_opacity=0.9, stroke_width=0).move_to(tgt)
        self.play(FadeOut(s1), flash.animate.scale(3).set_opacity(0), run_time=0.5)
        self.remove(flash)
        self.at("a wave of calcium")
        tr = ValueTracker(0.02)

        def ring():
            r = tr.get_value()
            th = np.linspace(0, TAU, 260)
            pts = P + r * np.stack([np.cos(th), np.sin(th)], 1)
            ok = np.hypot(pts[:, 0], pts[:, 1]) <= R - 0.07
            g = VGroup()
            run = []
            for p, o in zip(pts, ok):
                if o:
                    run.append(to3(p))
                elif run:
                    if len(run) > 1:
                        g.add(VMobject().set_points_as_corners(run).set_stroke(CYAN, 14))
                    run = []
            if len(run) > 1:
                g.add(VMobject().set_points_as_corners(run).set_stroke(CYAN, 14))
            g.set_z_index(7)
            return g
        w = always_redraw(ring)
        w.set_z_index(7)
        self.add(w)
        cw = put(lab("calcium wave", color=CYAN, size=34), RX, 2.2)
        self.play(tr.animate.set_value(2 * R + 0.2), FadeIn(cw), run_time=2.7, rate_func=linear)
        self.remove(w)
        self.at("A frog egg was paused")
        m1 = put(lab("frog egg: paused in meiosis", color=TEXT), RX, 0.9)
        self.play(FadeIn(m1), run_time=0.6)
        self.at("and the calcium wakes it")
        m2 = put(lab("frog egg: restarted", color=GREEN), RX, 0.9)
        glow = Circle(radius=R, color=CYAN, stroke_width=8, fill_opacity=0).move_to(EC).set_z_index(7)
        self.play(FadeOut(m1, shift=UP * 0.2), FadeIn(m2, shift=UP * 0.2), FadeIn(glow), run_time=0.6)
        self.play(FadeOut(glow), run_time=0.8)
        self.at("Only one sperm should get in")
        extras = VGroup()
        for ang in (-0.45, -0.95):
            surf = EC + R * np.array([np.cos(ang), np.sin(ang), 0])
            sp = sperm(surf + np.array([1.7, -0.1, 0]) + 0.0)
            extras.add(sp)
        self.play(FadeIn(extras), run_time=0.4)
        for i, ang in enumerate((-0.45, -0.95)):
            surf = EC + R * np.array([np.cos(ang), np.sin(ang), 0])
        anims = []
        for sp, ang in zip(extras, (-0.45, -0.95)):
            surf = EC + R * np.array([np.cos(ang), np.sin(ang), 0])
            head = sp[0].get_center()
            anims.append(sp.animate.shift(surf + np.array([0.3, 0, 0]) - head))
        self.play(*anims, run_time=1.6)
        for sp in extras:
            tt = {"v": 0.0}
            sp.add_updater(lambda m, dt: m[1].shift(UP * 0.0))
        self.at("keeps the rest out")
        ex = put(lab("extra sperm kept out", color=TEXT), 3.9, -2.9)
        ax = Arrow(ex.get_left() + LEFT * 0.05, extras[1].get_right() + RIGHT * 0.9, color=GREY, buff=0.1, stroke_width=4)
        self.play(FadeIn(ex), run_time=0.5)
        self.play(Indicate(extras, color=TEXT, scale_factor=1.05), run_time=1.2)
        self.finish()


class S03Cleave(EggScene):
    def construct(self):
        self.start_egg(0)
        cnt = {"n": 1}
        c_lab = M("cells: 1", size=40, color=YELLOW).move_to([RX, 2.8, 0])
        self.add(c_lab)

        def setcount(n):
            new = M(f"cells: {n}", size=40, color=YELLOW).move_to(c_lab)
            return Transform(c_lab, new)
        t1 = put(lab("cleavage", color=TEAL, size=38, weight=BOLD), RX, 1.5)
        self.at("Next comes cleavage")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("a run of divisions")
        o2 = DashedVMobject(Circle(radius=R + 0.14, color=TEXT, stroke_width=4.5), num_dashes=48).move_to(EC).set_z_index(3)
        ng = put(lab("no growth between"), RX, 0.5)
        self.play(FadeIn(ng), Create(o2), run_time=0.9)
        self.at("Each new cell")
        self.split_to(1, run=0.8)
        self.play(setcount(2), run_time=0.3)
        self.at("blastomere")
        tag = put(lab("blastomere", color=TEAL, size=36), RX, -0.8)
        c0 = self.cm[1]
        arr_ = Arrow(tag.get_left() + LEFT * 0.1, [EC[0] + 1.2, EC[1] - 0.3, 0], color=TEAL, buff=0.1, stroke_width=5)
        arr_.set_z_index(8)
        self.play(FadeIn(tag), GrowArrow(arr_), run_time=0.7)
        self.play(Indicate(c0, color=TEAL, scale_factor=1.03), run_time=0.6)
        self.at("then four")
        self.play(FadeOut(tag), FadeOut(arr_), FadeOut(ng), run_time=0.3)
        self.split_to(2, run=0.7)
        self.play(setcount(4), run_time=0.3)
        self.at("then eight")
        self.split_to(3, run=1.0)
        self.play(setcount(8), run_time=0.3)
        self.play(Indicate(c_lab, color=YELLOW), run_time=0.8)
        self.finish()


class S04Fixed(EggScene):
    def construct(self):
        self.start_egg(3, outline=False)
        o = DashedVMobject(Circle(radius=R + 0.14, color=TEXT, stroke_width=4.5), num_dashes=48).move_to(EC).set_z_index(3)
        o.add_updater(lambda m, dt: m.rotate(0.15 * dt, about_point=EC))
        self.add(o)
        BARW = 5.2
        ref = Rectangle(width=BARW, height=0.32, stroke_color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([RX, 1.2, 0])
        refl = put(lab("egg's width"), RX, 1.8)
        tr = ValueTracker(8 ** (-1 / 3))

        def bar():
            w = BARW * tr.get_value()
            b = Rectangle(width=w, height=0.32, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.8)
            b.move_to([RX - BARW / 2 + w / 2, -0.2, 0])
            return b
        cb = always_redraw(bar)
        cl = put(lab("one cell's width", color=YELLOW), RX, 0.4)
        self.at("Watch the outline")
        self.play(Indicate(o, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.at("It never gets bigger")
        self.play(FadeIn(ref), FadeIn(refl), FadeIn(cb), FadeIn(cl), run_time=0.8)
        self.at("Each division cuts")
        self.split_to(4, run=0.9)
        self.play(tr.animate.set_value(16 ** (-1 / 3)), run_time=0.9)
        self.split_to(5, run=0.9)
        self.play(tr.animate.set_value(32 ** (-1 / 3)), run_time=0.9)
        self.at("The egg is divided")
        cap = put(lab("divided, not grown", color=TEXT, size=40, weight=BOLD), RX, -1.5)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(o, color=TEXT, scale_factor=1.03), run_time=1.2)
        self.finish()


def ruler(x0, x1, y, color=TEXT):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x0, y - 0.15, 0], [x0, y + 0.15, 0], color=color, stroke_width=4),
                  Line([x1, y - 0.15, 0], [x1, y + 0.15, 0], color=color, stroke_width=4))


TINY = np.array([RX, -2.81, 0])


class S05Predict(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        top = put(lab("model: 5 equal divisions → 32 cells", color=YELLOW), 0, 3.4, max_w=11)
        self.at("Suppose every division is equal")
        self.play(FadeIn(top), run_time=0.6)
        self.at("After five divisions")
        self.play(Indicate(self.cells, color=CREAM, scale_factor=1.02), run_time=1.0)
        self.at("Is each cell")
        rl = ruler(EC[0] - R, EC[0] + R, -3.15)
        rt = put(lab("egg's width"), EC[0], -3.55)
        self.play(Create(rl), FadeIn(rt), run_time=0.8)
        tiny = Circle(radius=0.09, color=TEXT, stroke_width=3).move_to(TINY)
        tiny = DashedVMobject(tiny, num_dashes=12)
        tl = put(lab("1/32 of the width?"), RX, -1.9)
        ta = Arrow(tl.get_bottom(), TINY + UP * 0.15, color=GREY, buff=0.08, stroke_width=4)
        card = chip("Is each cell 1/32 as wide?", color=YELLOW, size=34)
        put(card, RX, 0.6, max_w=6.2)
        self.play(FadeIn(tiny), FadeIn(tl), GrowArrow(ta), FadeIn(card, scale=0.9), run_time=1.0)
        self.finish()


class S06Pause(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        self.add(put(lab("model: 5 equal divisions → 32 cells", color=YELLOW), 0, 3.4, max_w=11))
        self.add(ruler(EC[0] - R, EC[0] + R, -3.15), put(lab("egg's width"), EC[0], -3.55))
        self.add(DashedVMobject(Circle(radius=0.09, color=TEXT, stroke_width=3).move_to(TINY), num_dashes=12))
        self.add(put(lab("1/32 of the width?"), RX, -1.9))
        self.add(Arrow(put(lab("1/32 of the width?"), RX, -1.9).get_bottom(), TINY + UP * 0.15, color=GREY, buff=0.08, stroke_width=4))
        self.add(put(chip("Is each cell 1/32 as wide?", color=YELLOW, size=34), RX, 0.6, max_w=6.2))
        tr, base, arc = ring_timer(RX, -0.9 + 0.0, 0.0)
        tr, base, arc = ring_timer(6.2, 2.0, 0.4)
        self.add(base, arc)
        crd = self.mobjects[-4] if False else None
        self.play(tr.animate.set_value(1.0), Indicate(self.cells, color=CREAM, scale_factor=1.015, run_time=2.4), run_time=4.8, rate_func=linear)
        self.finish()


class S07Reveal(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        top = put(lab("model: 5 equal divisions → 32 cells", color=YELLOW), 0, 3.4, max_w=11)
        rl = ruler(EC[0] - R, EC[0] + R, -3.15)
        rt = put(lab("egg's width"), EC[0], -3.55)
        tiny = DashedVMobject(Circle(radius=0.09, color=TEXT, stroke_width=3).move_to(TINY), num_dashes=12)
        tl = put(lab("1/32 of the width?"), RX, -1.9)
        ta = Arrow(tl.get_bottom(), TINY + UP * 0.15, color=GREY, buff=0.08, stroke_width=4)
        card = put(chip("Is each cell 1/32 as wide?", color=YELLOW, size=34), RX, 0.6, max_w=6.2)
        self.add(top, rl, rt, tiny, tl, ta, card)
        rb = R / 3.17
        self.at("each cell holds one")
        blast = Circle(radius=rb, color=CREAM, fill_color=CREAM, fill_opacity=1, stroke_width=0).move_to([RX, -2.9 + rb, 0])
        vol = put(lab("volume ÷ 32", color=GREEN, size=44, weight=BOLD), RX, 2.6)
        self.play(FadeOut(card), FadeOut(tl), FadeOut(ta), FadeOut(top), ReplacementTransform(tiny, blast), run_time=1.2)
        self.play(FadeIn(vol, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(blast, color=CREAM, scale_factor=1.12), run_time=1.0)
        self.at("three dimensions")
        O = np.array([2.8, -0.3, 0])
        ax_l = Arrow(O, O + RIGHT * 1.5, color=CYAN, buff=0, stroke_width=6)
        tl_ = lab("length", color=CYAN, size=30).next_to(ax_l, RIGHT, buff=0.12)
        self.play(GrowArrow(ax_l), FadeIn(tl_), run_time=0.7)
        self.at("width")
        ax_w = Arrow(O, O + UP * 1.4, color=CYAN, buff=0, stroke_width=6)
        tw_ = lab("width", color=CYAN, size=30).next_to(ax_w, UP, buff=0.1)
        self.play(GrowArrow(ax_w), FadeIn(tw_), run_time=0.7)
        self.at("and depth")
        ax_d = Arrow(O, O + np.array([0.9, 0.9, 0]), color=CYAN, buff=0, stroke_width=6)
        td_ = lab("depth", color=CYAN, size=30).next_to(ax_d, UR, buff=0.05)
        self.play(GrowArrow(ax_d), FadeIn(td_), run_time=0.7)
        self.at("So each cell is about")
        self.play(FadeOut(VGroup(ax_l, tl_, ax_w, tw_, ax_d, td_)), run_time=0.5)
        wtxt = VGroup(lab("width ÷ 32", color=YELLOW, size=36),
                      T("1/3", size=24, color=YELLOW),
                      lab("  ≈ 3.17", color=YELLOW, size=36))
        wtxt[1].next_to(wtxt[0], RIGHT, buff=0.03).shift(UP * 0.14)
        wtxt[2].next_to(wtxt[1], RIGHT, buff=0.05).align_to(wtxt[0], DOWN)
        wtxt = VGroup(*wtxt)
        put(wtxt, RX, 1.2)
        self.play(FadeIn(wtxt), run_time=0.7)
        r2 = ruler(RX - rb, RX + rb, -3.15)
        t2 = put(lab("≈ 39 µm", color=TEXT), RX, -3.55)
        t1 = put(lab("≈ 124 µm (1 nL model egg)", size=28), EC[0], -3.55, max_w=5.4)
        self.play(Create(r2), FadeIn(t2), Transform(rt, t1), run_time=1.0)
        self.finish()


class S08Nuclei(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        BARW = 5.2
        ncount = ValueTracker(1)
        nl = always_redraw(lambda: M(f"nuclei: {int(round(ncount.get_value()))}", size=42, color=NUC if False else TEXT).move_to([RX, 2.7, 0]))
        self.at("There are now 32 nuclei")
        nuc = nuclei_for(5)
        self.add(nl)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in nuc], lag_ratio=0.04), ncount.animate.set_value(32), run_time=2.4)
        self.at("but no new cytoplasm")
        cl = put(lab("cytoplasm: unchanged", color=CREAM), RX, 1.5)
        cbar = Rectangle(width=BARW, height=0.42, stroke_color=CREAM, fill_color=CREAM, fill_opacity=0.9).move_to([RX, 0.95, 0])
        self.play(FadeIn(cl), FadeIn(cbar), run_time=0.8)
        self.at("Each nucleus has")
        pl = put(lab("cytoplasm per nucleus", color=TEAL), RX, -0.1)
        pr = ValueTracker(1.0)

        def pbar():
            w = max(0.03, BARW * pr.get_value())
            return Rectangle(width=w, height=0.42, stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.9).move_to([RX - BARW / 2 + w / 2, -0.65, 0])
        pb = always_redraw(pbar)
        frame = Rectangle(width=BARW, height=0.42, stroke_color=GREY, stroke_width=2).move_to([RX, -0.65, 0])
        self.play(FadeIn(pl), FadeIn(frame), FadeIn(pb), run_time=0.6)
        self.play(pr.animate.set_value(1 / 32), run_time=3.5, rate_func=smooth)
        end = put(lab("1/32 each", color=TEAL), RX, -1.45)
        self.play(FadeIn(end), run_time=0.5)
        self.finish()


class S09Patch(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        self.at("Now suppose the egg is not")
        self.reset_egg(run=1.0)
        self.play(Indicate(self.cells, color=CREAM, scale_factor=1.02), run_time=1.0)
        self.at("Mark one region in purple")
        dots = patch_dots(0.0)
        self.add(dots)
        dots.set_opacity(0)
        self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in dots], lag_ratio=0.04), run_time=1.8)
        self.at("This stands for inherited material")
        lb = put(lab("drawn in purple:", color=PURPLE), RX, 1.0)
        lb2 = put(lab("inherited material", color=PURPLE, size=36, weight=BOLD), RX, 0.3)
        arrow = Arrow([RX - 2.7, 0.3, 0], to3(np.array([-0.3 * R, -0.2 * R])), color=PURPLE, buff=0.1, stroke_width=5).set_z_index(8)
        self.play(FadeIn(lb), FadeIn(lb2), GrowArrow(arrow), run_time=0.9)
        self.at("placed in the egg")
        self.play(Indicate(lb2, color=PURPLE, scale_factor=1.08), run_time=1.2)
        self.finish()


class S10Share(EggScene):
    def construct(self):
        self.start_egg(0, outline=True)
        dots = patch_dots(1.0)
        self.add(dots)
        self.at("Suppose the purple is anchored")
        tag = put(lab("model: purple anchored,", color=PURPLE, size=30), RX, 2.6)
        tag2 = put(lab("does not drift", color=PURPLE, size=30), RX, 2.05)
        self.play(FadeIn(tag), FadeIn(tag2), run_time=0.7)
        self.at("The furrows cut through")
        for k, rt in ((1, 0.55), (2, 0.55), (3, 0.5), (4, 0.45), (5, 0.45)):
            self.split_to(k, run=rt)
            self.wait(0.1)
        self.at("After a few divisions")
        self.play(Indicate(dots, color=PURPLE, scale_factor=1.05), run_time=0.8)
        self.at("only some cells hold it")
        po = self.purple_outline()
        self.play(LaggedStart(*[Create(m) for m in po], lag_ratio=0.1), run_time=1.4)
        self.at("Their neighbors have none")
        plain = VGroup(*[self.cm[i] for i in PLAIN_CELLS])
        self.play(plain.animate.set_opacity(0.5), run_time=0.8)
        self.play(plain.animate.set_opacity(1.0), run_time=0.8)
        self.finish()


class S11Inherit(EggScene):
    def construct(self):
        self.start_egg(5, outline=True)
        dots = patch_dots(1.0)
        self.add(dots)
        po = self.purple_outline()
        self.add(po)
        # pick the purple cell with most dots and a plain neighbour that touches it
        counts = [sum(1 for p in PATCH if inside(STAGES[5][i], p)) for i in PURPLE_CELLS]
        pi = PURPLE_CELLS[int(np.argmax(counts))]
        pc = STAGES[5][pi]

        def touch(a, b):
            ax0, ax1, ay0, ay1 = a["rect"]
            bx0, bx1, by0, by1 = b["rect"]
            return (abs(ax1 - bx0) < 1e-6 or abs(bx1 - ax0) < 1e-6) and ay0 < by1 and by0 < ay1 or \
                   (abs(ay1 - by0) < 1e-6 or abs(by1 - ay0) < 1e-6) and ax0 < bx1 and bx0 < ax1
        ni = [i for i in PLAIN_CELLS if touch(pc, STAGES[5][i])]
        nc = STAGES[5][ni[0] if ni else PLAIN_CELLS[0]]
        self.at("That is what a cell inherits")
        # large copies side by side
        cp = _centroid(pc)
        cn = _centroid(nc)
        S = 3.2
        big_p = cell_mob(pc, origin=np.array([-2.9, 0.0]) - cp * S, scale=S)
        big_n = cell_mob(nc, origin=np.array([2.9, 0.0]) - cn * S, scale=S)
        bd = VGroup(*[Dot(to3(p * S, np.array([-2.9, 0.0]) - cp * S), radius=0.14, color=PURPLE) for p in PATCH if inside(pc, p)]).set_z_index(6)
        big_p.set_stroke(PURPLE, 8)
        self.play(FadeOut(self.cells), FadeOut(po), FadeOut(dots), FadeOut(self.outline), FadeOut(self.motes),
                  FadeIn(big_p), FadeIn(big_n), FadeIn(bd), run_time=1.4)
        mo = make_motes(10, seed=3, origin=np.array([2.9, 0, 0]), rad=0.9)
        self.add(mo)
        t = {"v": 0.0}
        bd.add_updater(lambda m, dt: (t.__setitem__("v", t["v"] + dt), [d.set_opacity(0.7 + 0.3 * np.sin(3 * t["v"] + i)) for i, d in enumerate(m)])[0])
        inh = put(lab("inherits", color=PURPLE, size=40, weight=BOLD), -2.9, 3.0)
        self.play(FadeIn(inh, shift=DOWN * 0.2), run_time=0.7)
        self.at("the slice of egg")
        sl = put(lab("its slice of the egg", size=30), -2.9, -3.2, max_w=5.6)
        self.play(FadeIn(sl), run_time=0.6)
        self.at("If an anchored molecule")
        self.play(FadeOut(sl), run_time=0.3)
        c1 = put(lab("cytoplasmic determinant", color=PURPLE, size=38, weight=BOLD), 0, -2.75, max_w=11)
        c2 = put(lab("a localized molecule that helps set cell fate", size=30), 0, -3.4, max_w=11)
        self.at("cytoplasmic determinant")
        self.play(FadeIn(c1), run_time=0.6)
        self.play(FadeIn(c2), run_time=0.6)
        self.finish()


def sub_cell_stage(cx, cy, scale):
    return None


class S12Yolk(EggScene):
    def construct(self):
        self.start_egg(0, outline=True)
        self.at("Yolk changes the cutting")
        # yolk fills the lower half of the carried egg
        ys = []
        for t in np.linspace(np.pi, 2 * np.pi, 40):
            ys.append(to3(np.array([R * np.cos(t), R * np.sin(t) + 0.0])))
        yolk_pts = [to3(np.array([R * np.cos(t), R * np.sin(t)])) for t in np.linspace(np.pi, 2 * np.pi, 48)]
        yolk = Polygon(*yolk_pts, stroke_width=0, fill_color=TAN, fill_opacity=0.95).set_z_index(1.5)
        yl = put(lab("yolk: stored food", color=TAN, size=36, weight=BOLD), RX, 1.5)
        self.at("Yolk is stored food")
        self.play(FadeIn(yolk), FadeIn(yl), run_time=1.0)
        self.at("and it slows the furrows")
        self.play(Indicate(yolk, color=TAN, scale_factor=1.04), run_time=1.0)
        self.at("A frog egg divides completely")
        self.play(FadeOut(self.motes), FadeOut(yl), FadeOut(self.outline), run_time=0.4)
        # frog panel: egg shrinks to the left column
        Rf = 2.0
        cxs = [-4.5, 0.0, 4.5]
        cy = 0.35
        frog = VGroup()
        small = []
        # frog: cells small on top (cream), large below (tan-tinted)
        def disc_part(c0, r, a0, a1, color, n=40):
            pts = [np.array([c0[0], c0[1], 0])] + [np.array([c0[0] + r * np.cos(t), c0[1] + r * np.sin(t), 0]) for t in np.linspace(a0, a1, n)]
            return Polygon(*pts, stroke_color=BG, stroke_width=4, fill_color=color, fill_opacity=1)
        fc = np.array([cxs[0], cy])
        # top half in 4 small cells, bottom half in 2 large cells
        for a0 in np.linspace(0, np.pi, 5)[:-1]:
            frog.add(disc_part(fc, Rf, a0, a0 + np.pi / 4, CREAM))
        frog.add(disc_part(fc, Rf, np.pi, 3 * np.pi / 2, "#D8C58C"))
        frog.add(disc_part(fc, Rf, 3 * np.pi / 2, 2 * np.pi, "#D8C58C"))
        self.play(FadeOut(VGroup(*self.cm)), FadeOut(yolk), FadeIn(frog), run_time=1.2)
        fl = put(lab("frog", size=36, weight=BOLD), cxs[0], 2.85)
        fl2 = put(lab("bigger cells in", size=28), cxs[0], -2.0, max_w=4.2)
        fl3 = put(lab("the yolky half", size=28), cxs[0], -2.55, max_w=4.2)
        self.play(FadeIn(fl), run_time=0.5)
        self.at("with bigger cells")
        self.play(FadeIn(fl2), FadeIn(fl3), run_time=0.7)
        self.at("A chick divides only a disc")
        cc = np.array([cxs[1], cy])
        chick_yolk = Circle(radius=Rf, stroke_color=BG, stroke_width=4, fill_color=TAN, fill_opacity=1).move_to([cc[0], cc[1], 0])
        disc_cells = VGroup()
        for i in range(5):
            x = cc[0] - 0.9 + i * 0.45
            disc_cells.add(RoundedRectangle(corner_radius=0.1, width=0.42, height=0.38, stroke_color=BG, stroke_width=3,
                                            fill_color=CREAM, fill_opacity=1).move_to([x, cc[1] + Rf - 0.22, 0]))
        cl = put(lab("chick", size=36, weight=BOLD), cxs[1], 2.85)
        self.play(FadeIn(chick_yolk), FadeIn(cl), run_time=0.8)
        self.play(FadeIn(disc_cells), run_time=0.8)
        cl2 = put(lab("only the top disc", size=28), cxs[1], -2.0, max_w=4.2)
        cl3 = put(lab("divides", size=28), cxs[1], -2.55, max_w=4.2)
        self.play(FadeIn(cl2), FadeIn(cl3), run_time=0.5)
        self.at("A fly first divides its nuclei")
        fe = Ellipse(width=2 * 2.1, height=2 * 1.3, stroke_color=BG, stroke_width=4, fill_color=CREAM, fill_opacity=1).move_to([cxs[2], cy, 0])
        fe.set_z_index(0)
        # fly yolk blob in the middle, nuclei in the cytoplasm around it
        fy = Ellipse(width=2 * 1.2, height=2 * 0.6, stroke_width=0, fill_color=TAN, fill_opacity=0.9).move_to([cxs[2], cy, 0])
        fly_l = put(lab("fly", size=36, weight=BOLD), cxs[2], 2.85)
        nuc = VGroup()
        rng = np.random.RandomState(4)
        for i in range(14):
            a = rng.uniform(0, TAU)
            rr = rng.uniform(0.2, 0.9)
            p = np.array([cxs[2] + 1.8 * rr * np.cos(a), cy + 1.05 * rr * np.sin(a), 0])
            d = Dot(p, radius=0.1, color=NUC)
            d.set_stroke(TEXT, 1.5)
            d.v = np.array([rng.uniform(-0.25, 0.25), rng.uniform(-0.15, 0.15), 0])

            def drift(m, dt, cx=cxs[2]):
                m.shift(m.v * dt)
                x, y = m.get_center()[0] - cx, m.get_center()[1] - cy
                if (x / 1.85) ** 2 + (y / 1.1) ** 2 > 1:
                    m.v = -m.v
                    m.shift(m.v * dt * 2)
            d.add_updater(drift)
            nuc.add(d)
        self.play(FadeIn(fe), FadeIn(fly_l), run_time=0.7)
        self.play(FadeIn(fy), LaggedStart(*[FadeIn(d, scale=0.3) for d in nuc], lag_ratio=0.08), run_time=1.6)
        self.at("with no membranes")
        fl2_ = put(lab("shared cytoplasm,", size=28), cxs[2], -2.0, max_w=4.2)
        fl3_ = put(lab("no membranes", size=28), cxs[2], -2.55, max_w=4.2)
        self.play(FadeIn(fl2_), FadeIn(fl3_), run_time=0.7)
        self.finish()


class S13Conklin(EggScene):
    def construct(self):
        self.start_egg(0, outline=True)
        cap = put(lab("Edwin Conklin, 1905; sea squirt (Styela)", size=30), 0, 3.4, max_w=11)
        self.at("Edwin Conklin watched")
        self.play(FadeIn(cap), run_time=0.7)
        # crescent: purple band on the right side of the egg
        self.at("Part of its cytoplasm is yellow")
        ang = np.linspace(-1.0, 1.0, 40)
        outer = [to3(np.array([R * 0.97 * np.cos(a), R * 0.97 * np.sin(a)])) for a in ang]
        inner = [to3(np.array([(R * 0.97 - 0.55 * np.cos(a * 0.9)) * np.cos(a), (R * 0.97 - 0.55 * np.cos(a * 0.9)) * np.sin(a)])) for a in ang[::-1]]
        cres = Polygon(*(outer + inner), stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).set_z_index(5)
        self.play(FadeIn(cres, scale=0.9), run_time=1.0)
        cl = put(lab("yellow crescent, drawn", color=PURPLE, size=30), 3.6, 0.6, max_w=5.8)
        cl2 = put(lab("in purple: inherited material", color=PURPLE, size=30), 3.6, -0.1, max_w=5.8)
        self.at("and it gathers into a crescent")
        self.play(FadeIn(cl), FadeIn(cl2), run_time=0.7)
        self.at("He followed it cell by cell")
        self.play(FadeOut(cl), FadeOut(cl2), run_time=0.4)
        for k in (1, 2, 3):
            self.split_to(k, run=0.6)
        # outline the crescent cells at 8 cells
        crest_cells = [i for i, c in enumerate(STAGES[3]) if c["rect"][1] > 0.4 * R and abs((c["rect"][2] + c["rect"][3]) / 2) < 0.6 * R]
        ol = VGroup()
        for i in crest_cells:
            ol.add(Polygon(*[to3(p) for p in STAGES[3][i]["pts"]], stroke_color=PURPLE, stroke_width=7, fill_opacity=0).set_z_index(6))
        self.play(Create(ol), run_time=0.6)
        self.at("It ended up mainly")
        # larva: head circle + tail with muscle band
        hx, hy = 2.0, 0.2
        head = Ellipse(width=1.7, height=1.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([hx, hy, 0])
        tail = Polygon([hx + 0.7, hy + 0.5, 0], [6.5, hy + 0.12, 0], [6.5, hy - 0.12, 0], [hx + 0.7, hy - 0.5, 0],
                       stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25)
        muscle = Polygon([hx + 1.05, hy + 0.36, 0], [6.1, hy + 0.1, 0], [6.1, hy - 0.1, 0], [hx + 1.05, hy - 0.36, 0],
                         stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.45)
        larva = VGroup(head, tail)
        self.play(FadeIn(larva, shift=LEFT * 0.3), run_time=0.9)
        self.at("tail muscle")
        self.play(FadeIn(muscle), run_time=0.7)
        ml = put(lab("tail muscle", color=RED, size=32), 4.4, hy - 1.0)
        path = DashedLine([EC[0] + R * 0.95, EC[1] + 0.2, 0], [hx - 0.8, hy, 0], color=PURPLE, stroke_width=5).set_z_index(8)
        path2 = DashedLine([hx + 0.85, hy, 0], [hx + 1.1, hy, 0], color=PURPLE, stroke_width=5)
        self.play(FadeIn(ml), Create(path), run_time=1.2)
        self.play(Indicate(muscle, color=RED, scale_factor=1.04), run_time=1.0)
        self.finish()


class S14Limit(EggScene):
    def construct(self):
        # carried: the egg, crescent cells and larva from the previous scene fade into two panels
        self.start_egg(3, outline=False, motes=False)
        self.play(FadeOut(VGroup(*self.cm)), run_time=0.2)
        self.at("But following a color")
        pl = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.0, stroke_color=GREY, stroke_width=3).move_to([-3.3, -0.1, 0])
        pr = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.0, stroke_color=GREY, stroke_width=3).move_to([3.3, -0.1, 0])
        l1 = put(lab("where it goes", color=GREEN, size=36, weight=BOLD), -3.3, 1.9, max_w=5.5)
        l2 = put(lab("what it does", color=YELLOW, size=36, weight=BOLD), 3.3, 1.9, max_w=5.5)
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(l1), FadeIn(l2), run_time=0.9)
        # left: crescent -> muscle, dotted path ticked
        e = Circle(radius=0.7, color=CREAM, fill_color=CREAM, fill_opacity=1, stroke_width=0).move_to([-5.0, 0.2, 0])
        cr = Arc(radius=0.7, start_angle=-0.8, angle=1.6, color=PURPLE, stroke_width=14).move_to([-4.65, 0.2, 0])
        cr.move_to(e.get_center() + RIGHT * 0.6)
        mus = RoundedRectangle(corner_radius=0.1, width=1.3, height=0.5, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.45).move_to([-1.9, 0.2, 0])
        dp = DashedLine([-4.0, 0.2, 0], [-2.7, 0.2, 0], color=PURPLE, stroke_width=5)
        tick = Text("✓", font_size=90, color=GREEN).move_to([-3.3, -1.3, 0])
        self.play(FadeIn(e), FadeIn(cr), run_time=0.4)
        self.play(Create(dp), FadeIn(mus), run_time=0.8)
        self.play(FadeIn(tick, scale=0.5), run_time=0.4)
        self.at("not what it does")
        q = Text("?", font=TITLE_FONT, font_size=150, color=YELLOW).move_to([3.3, 0.2, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.8)
        self.at("Does the crescent make muscle")
        o1 = chip("makes muscle?", color=PURPLE, size=30)
        o2 = chip("just rides along?", color=PURPLE, size=30)
        o1.move_to([3.3, -0.9, 0])
        o2.move_to([3.3, -1.95, 0])
        self.play(FadeOut(q, shift=UP * 0.3), run_time=0.4)
        q2 = Text("?", font=TITLE_FONT, font_size=90, color=YELLOW).move_to([3.3, 0.3, 0])
        self.play(FadeIn(q2), FadeIn(o1), run_time=0.7)
        self.at("or just ride along")
        self.play(FadeIn(o2), run_time=0.7)
        t = {"v": 0.0}
        q2.add_updater(lambda m, dt: (t.__setitem__("v", t["v"] + dt), m.set_opacity(0.7 + 0.3 * np.sin(4 * t["v"])))[0])
        self.at("That takes a different test")
        cap = put(lab("a fate map is not a cause", color=TEXT, size=36, weight=BOLD), 0, -3.3, max_w=11)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S15Rule(EggScene):
    def construct(self):
        self.start_egg(0, outline=True)
        dots = patch_dots(1.0)
        self.add(dots)
        self.at("So cleavage shares out")
        for k in range(1, 6):
            self.split_to(k, run=0.55)
            self.wait(0.12)
        self.at("Each cell gets its own slice")
        po = self.purple_outline()
        self.play(LaggedStart(*[Create(m) for m in po], lag_ratio=0.1), run_time=1.2)
        self.at("and anchored material")
        a = put(lab("anchored material", color=PURPLE, size=36, weight=BOLD), RX, 1.2)
        b = put(lab("comes with the slice", color=PURPLE, size=36), RX, 0.5)
        ar = Arrow([RX - 2.2, 1.0, 0], to3(np.array([-0.35 * R, -0.3 * R])), color=PURPLE, buff=0.1, stroke_width=5).set_z_index(8)
        self.play(FadeIn(a), FadeIn(b), GrowArrow(ar), run_time=0.8)
        self.play(Indicate(dots, color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "The egg is divided, not grown: each cell inherits its own slice."
