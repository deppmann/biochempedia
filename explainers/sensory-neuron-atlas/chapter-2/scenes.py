"""When Identity Changes (sensory-neuron-atlas, chapter 2).
COLOR MAP (same as chapter 1): BLUE neuron/type, TEAL RNA profile/badges, GOLD genetic label (neuron outlines), GREEN physiology,
RED injury state, GREY uncertainty. Everything is schematic; positions are hand-placed."""
import numpy as np
from bp_style import *  # noqa: F401,F403

CY = [2.35, 0.2, -1.95]
CX = -2.2
N = 9
SKIN_X = 3.2
ISL = np.array([3.2, 0.3, 0.0])
CUTX = 0.9
INJ = [i for i in range(N) if i % 3 in (0, 1)]
AFF = [i for i in range(N) if i // 3 == 1]


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def clip(x):
    return min(1.0, max(0.0, x))


def home(i):
    b, j = i // 3, i % 3
    a = np.radians(90 + 120 * j)
    return np.array([CX + 0.62 * np.cos(a), CY[b] + 0.62 * np.sin(a), 0.0])


def blob(i):
    b, j = i // 3, i % 3
    return np.array([CX + (j - 1) * 1.0, 0.2 + (1 - b) * 1.0, 0.0])


def island(i):
    k = INJ.index(i)
    a = np.radians(30 + 60 * k)
    return ISL + 0.75 * np.array([np.cos(a), np.sin(a), 0.0])


def injured(i):
    return island(i) if i in INJ else home(i)


def tree_lines(blue=False, op=0.95):
    g = VGroup()
    trunk = Line([-6.0, CY[1], 0], [-4.8, CY[1], 0])
    vert = Line([-4.8, CY[0], 0], [-4.8, CY[2], 0])
    hs = [Line([-4.8, y, 0], [-3.4, y, 0]) for y in CY]
    for m in [trunk, vert]:
        m.set_stroke(TEXT, 12, opacity=op)
    for m in hs:
        m.set_stroke(BLUE if blue else TEXT, 12, opacity=op)
    g.add(trunk, vert, *hs)
    g.hs = hs
    return g


def sch(text="schematic"):
    return T(text, 28, TEXT).move_to([-5.5, 3.45, 0])


class Cells:
    """Nine gold-outlined blue neurons, each with three teal badges above it (the branch's own badge is index i//3)."""

    def __init__(self, sc, pos, d=1.0, amp=0.12, alpha=1.0, red=False):
        self.sc, self.amp = sc, amp
        self.src = [np.array(p, float) for p in pos]
        self.dst = [s.copy() for s in self.src]
        self.p = ValueTracker(1)
        self.c = ValueTracker(1 if red else 0)
        self.d = ValueTracker(d)
        self.aff = ValueTracker(0)
        self.sup = ValueTracker(1 if red else 0)
        self.al = ValueTracker(alpha)
        self.bs = ValueTracker(1)
        self.pf = self.cf = self.sf = None
        rng = np.random.RandomState(5)
        self.w = rng.uniform(0.5, 1.1, (N, 2))
        self.ph = rng.uniform(0, 6.28, (N, 2))
        self.grp = VGroup()
        for i in range(N):
            circ = Circle(radius=0.36, stroke_color=GOLD, stroke_width=5).set_fill(BLUE, 0.8)
            bd = VGroup(*[Square(0.25, stroke_width=0, fill_color=TEAL, fill_opacity=1) for _ in range(3)])
            g = VGroup(circ, *bd)
            g.i = i
            g.add_updater(self._upd)
            circ.move_to(self.src[i])
            self.grp.add(g)
        self.grp.set_z_index(3)

    def _pos(self, i):
        a = self.pf() if self.pf else self.p.get_value()
        return self.src[i] * (1 - a) + self.dst[i] * a

    def center(self, i):
        return self.grp[i][0].get_center()

    def _upd(self, g):
        i = g.i
        t = self.sc.renderer.time
        off = self.amp * np.array([np.sin(self.w[i][0] * t + self.ph[i][0]), np.cos(self.w[i][1] * t + self.ph[i][1]), 0])
        ctr = self._pos(i) + off
        circ = g[0]
        circ.move_to(ctr)
        c = (self.cf() if self.cf else self.c.get_value()) if i in INJ else 0.0
        sup = (self.sf() if self.sf else self.sup.get_value()) if i in INJ else 0.0
        al = self.al.get_value()
        circ.set_fill(interpolate_color(ManimColor(BLUE), ManimColor(RED), c), 0.8 * al)
        circ.set_stroke(GOLD, 5, opacity=al)
        mix = clip((1 - self.d.get_value()) + (0.6 * self.aff.get_value() if i in AFF else 0))
        for k in range(3):
            b = g[1 + k]
            b.move_to(ctr + np.array([(k - 1) * 0.3, 0.6, 0]))
            v = (1.0 if k == i // 3 else mix) * (1 - sup) * al * self.bs.get_value()
            v *= 0.85 + 0.15 * np.sin(2.0 * t + k + i)
            b.set_fill(TEAL, clip(v))

    def prep(self, dst, tint=None):
        cur = [self._pos(i) for i in range(N)]
        self.src = cur
        self.dst = [np.array(x, float) if x is not None else cur[i] for i, x in enumerate(dst)]
        self.p.set_value(0)
        return self.p.animate.set_value(1)

    def halo(self, i, color=GOLD, r=0.5):
        h = Circle(r, stroke_color=color, stroke_width=5)
        h.add_updater(lambda m: (m.move_to(self.center(i)), m.set_stroke(opacity=0.4 + 0.6 * (0.5 + 0.5 * np.sin(3 * self.sc.renderer.time)))))
        return h


class Axons:
    def __init__(self, F, v=1.0, cap=0.0):
        self.F = F
        self.v = ValueTracker(v)
        self.cap = ValueTracker(cap)
        self.vf = None
        self.op = ValueTracker(1)
        order = sorted(range(N), key=lambda i: (-home(i)[1], home(i)[0]))
        self.S = {}
        for r, i in enumerate(order):
            self.S[i] = np.array([SKIN_X, 3.0 - 0.75 * r, 0.0])
        self.ecut = {i: (CUTX - home(i)[0]) / (SKIN_X - home(i)[0]) for i in range(N)}
        self.lines = VGroup()
        for i in range(N):
            ln = Line(home(i), home(i) + RIGHT * 0.1).set_stroke(BLUE, 6)
            ln.i = i
            ln.add_updater(self._upd)
            self.lines.add(ln)
        self.lines.set_z_index(1)

    def e(self, i):
        v = self.vf() if self.vf else self.v.get_value()
        return min(v, 1 - self.cap.get_value() * (1 - self.ecut[i]))

    def _upd(self, ln):
        i = ln.i
        c = self.F.center(i)
        d = self.S[i] - home(i)
        ln.put_start_and_end_on(c, c + d * max(self.e(i), 0.02))
        ln.set_stroke(BLUE, 6, opacity=0.9 * self.op.get_value())

    def tip_home(self, i, e):
        return home(i) + (self.S[i] - home(i)) * e


def skin_mob(label=True):
    r = Rectangle(width=3.4, height=6.4, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to([SKIN_X + 1.7, 0.1, 0])
    g = VGroup(r)
    if label:
        g.add(T("skin", 30, TEXT).move_to([SKIN_X + 1.7, 2.9, 0]))
    return g


def make_world(sc, d=1.0, pos=None, alpha=1.0, blue=True, red=False, amp=0.12):
    F = Cells(sc, pos if pos is not None else [home(i) for i in range(N)], d=d, alpha=alpha, red=red, amp=amp)
    tree = tree_lines(blue=blue)
    return F, tree


def island_mob(op=1.0):
    ring = Circle(1.3, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.10).move_to(ISL)
    ring.add_updater(lambda m: m.set_stroke(width=3 + 2 * np.sin(2.0 * ring._sc.renderer.time)))
    return ring


def flow_dashes(p0, p1, sc, color=GREY, n=6):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    ds = VGroup(*[Line(ORIGIN, RIGHT * 0.01).set_stroke(color, 6) for _ in range(n)])
    L = np.linalg.norm(p1 - p0)
    u = (p1 - p0) / L
    seg = L / n

    def upd(g):
        ph = (sc.renderer.time * 0.5) % 1.0
        for k, m in enumerate(g):
            s = ((k + ph) * seg)
            a = p0 + u * s
            b = p0 + u * min(L, s + seg * 0.55)
            m.put_start_and_end_on(a, b)
    ds.add_updater(upd)
    head = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.18).rotate(np.arctan2(u[1], u[0]) - PI / 2).move_to(p1 - u * 0.1)
    return VGroup(ds, head)


def doors():
    a = chip("new type", TEXT, size=30).move_to([1.5, -2.7, 0])
    b = chip("shared state", TEXT, size=30).move_to([5.0, -2.7, 0])
    return a, b


# ---------------------------------------------------------------------------------------------
class S00Hook(SpokenScene):
    def construct(self):
        F, tree = make_world(self, d=1.0, blue=False)
        F.al.set_value(0)
        self.add(tree, F.grp, sch())
        self.play(F.al.animate.set_value(1), run_time=1.4)
        rings = VGroup(*[Circle(1.15, stroke_color=BLUE, stroke_width=5).move_to([CX, y, 0]) for y in CY])
        self.at("each cluster")
        self.play(Create(rings), run_time=1.2)
        lab = T("candidate type", 34, BLUE).move_to([3.2, 2.35, 0])
        self.at("candidate")
        self.play(FadeIn(lab, shift=LEFT * 0.3), run_time=0.8)
        self.at("But can the same")
        isl = island_mob()
        isl.set_opacity(0)
        isl = Circle(1.3, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.10).move_to(ISL)
        halo = F.halo(3, GOLD, 0.5)
        self.play(FadeOut(lab), FadeOut(rings), Create(isl), FadeIn(halo), run_time=1.2)
        self.at("leave its cluster")
        F.prep([island(1) if i == 3 else None for i in range(N)])
        F.dst[3] = ISL + np.array([0.0, -0.4, 0.0])
        F.p.set_value(0)
        self.play(F.p.animate.set_value(1), run_time=1.8)
        q = T("?", 100, GREY, weight=BOLD).move_to(ISL + UP * 1.0)
        self.at("later return")
        self.play(FadeIn(q, scale=0.4), run_time=0.8)
        self.at("Follow its identity")
        chips = []
        for txt, ph, x in [("development", "development", -4.2), ("injury", "injury", -0.8), ("another species", "another species", 3.0)]:
            c = chip(txt, TEXT, size=30).move_to([x, -3.3, 0])
            self.at(ph, lead=0.2)
            self.play(FadeIn(c, shift=UP * 0.3), run_time=0.5)
            chips.append(c)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Sensory Neurons by Their Genes: the Atlas Era"
    TITLE = "When Identity Changes"

    def construct(self):
        F, tree = make_world(self, d=1.0, blue=False, alpha=0.22)
        F.dst = F.src = [home(i) for i in range(N)]
        F.src[3] = ISL + np.array([0.0, -0.4, 0.0])
        tree.set_stroke(opacity=0.25)
        isl = Circle(1.3, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.04).set_stroke(opacity=0.3).move_to(ISL)
        q = T("?", 100, GREY, weight=BOLD).move_to(ISL + UP * 1.0)
        q.add_updater(lambda m: m.set_opacity(max(0.0, 1 - self.renderer.time / 0.6)))
        self.add(tree, isl, F.grp, q)
        super().construct()


class S02Development(SpokenScene):
    def construct(self):
        F = Cells(self, [blob(i) for i in range(N)], d=0.0)
        F.al.set_value(0)
        F.bs.set_value(0)
        F.pf = lambda: smooth((F.d.get_value() - 0.15) / 0.85)
        F.src = [blob(i) for i in range(N)]
        F.dst = [home(i) for i in range(N)]
        tree = tree_lines(blue=False)
        title = T("mouse development, schematic", 28, TEXT).move_to([3.7, 3.2, 0])
        track = Line([1.2, 2.1, 0], [6.2, 2.1, 0]).set_stroke(TEXT, 6)
        knob = Dot(radius=0.2, color=GOLD)
        knob.add_updater(lambda m: m.move_to([1.2 + 5.0 * F.d.get_value(), 2.1, 0]))
        e1 = T("early", 28, TEXT).move_to([1.5, 1.45, 0])
        e2 = T("late", 28, TEXT).move_to([5.9, 1.45, 0])
        self.add(tree, F.grp)
        self.play(Create(tree), F.al.animate.set_value(1), FadeIn(title), Create(track), FadeIn(knob), FadeIn(e1), FadeIn(e2), run_time=3.0)
        self.at("Early cells")
        self.play(F.bs.animate.set_value(1), run_time=1.5)
        gl = T("TF badges per cell", 30, TEAL).move_to([3.7, 0.1, 0])
        sq = VGroup(*[Square(0.6, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([2.7 + k, -0.9, 0]) for k in range(3)])
        for k, s in enumerate(sq):
            s.add_updater(lambda m, k=k: m.set_fill(TEAL, 1.0 if k == 0 else 1 - 0.85 * F.d.get_value()))
        self.at("several transcription")
        self.play(FadeIn(gl), FadeIn(sq), run_time=1.5)
        self.at("Specialization here")
        sid = chip("subtype identity", BLUE, size=30).move_to([3.7, -2.6, 0])
        self.play(FadeIn(sid, shift=UP * 0.2), run_time=1.0)
        self.at("Over development")
        self.play(FadeOut(sid), run_time=0.6)
        self.play(F.d.animate.set_value(1.0), run_time=8.6, rate_func=linear)
        self.at("distinct blue")
        self.play(*[h.animate.set_stroke(BLUE) for h in tree.hs], run_time=1.2)
        self.finish()


def axon_world(sc, d=1.0, aff=0.0, v=1.0):
    F, tree = make_world(sc, d=d)
    F.aff.set_value(aff)
    A = Axons(F, v=v)
    skin = skin_mob()
    return F, tree, A, skin


class S03Target(SpokenScene):
    def construct(self):
        F, tree, A, skin = axon_world(self, v=0.0)
        self.add(tree, A.lines, F.grp, sch())
        self.play(FadeIn(skin), run_time=0.8)
        self.play(A.v.animate.set_value(1.0), run_time=2.6)
        ngf = T("NGF", 32, TEAL).move_to([SKIN_X + 1.7, 1.2, 0])
        arrows = VGroup()
        for i in AFF:
            tri = Triangle(fill_color=TEAL, fill_opacity=1, stroke_width=0).scale(0.24)
            k = AFF.index(i)

            def upd(m, i=i, k=k):
                s = A.S[i]
                c = F.center(i)
                ph = (self.renderer.time * 0.35 + k / 3.0) % 1.0
                m.move_to(s + (c - s) * ph * 0.95)
                m.set_fill(TEAL, 1.0 if ph < 0.9 else 0.0)
            tri.add_updater(upd)
            tri.rotate(-PI / 2)
            arrows.add(tri)
        arrows.set_z_index(4)
        self.play(FadeIn(arrows), FadeIn(ngf), run_time=0.8)
        self.at("Removing nerve")
        self.play(FadeOut(arrows), FadeOut(ngf), run_time=1.0)
        cnt = chip("9 neurons", BLUE, size=28).move_to([-5.2, -3.3, 0])
        self.play(FadeIn(cnt), run_time=0.6)
        self.at("subtype restricted")
        self.play(F.aff.animate.set_value(1.0), run_time=3.0)
        self.at("Fewer distinct")
        fd = T("fewer distinct\npopulations", 30, TEXT, line_spacing=0.8).move_to([SKIN_X + 1.7, -0.9, 0])
        self.play(FadeIn(fd, shift=UP * 0.2), run_time=1.0)
        self.at("Keeping the affected")
        shield = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=2.9, height=2.5, stroke_color=GOLD, stroke_width=5), num_dashes=40).move_to([CX, CY[1], 0])
        ka = chip("kept alive", GOLD, size=30).move_to([SKIN_X + 1.7, -2.4, 0])
        self.play(FadeOut(fd), FadeIn(shield), FadeIn(ka), run_time=1.2)
        self.at("The signal contributes")
        self.play(Indicate(shield, color=GOLD, scale_factor=1.06), run_time=1.5)
        self.finish()


def build_s04_state(sc, stage):
    """stage 'cut' = after the cut and gather (s04 end / s05)."""
    F, tree = make_world(sc, d=1.0, pos=[injured(i) for i in range(N)], red=True)
    A = Axons(F, v=0.15, cap=1.0)
    return F, tree, A


class S04Predict(SpokenScene):
    def construct(self):
        F, tree, A, skin = axon_world(self)
        self.add(tree, A.lines, F.grp, skin, sch())
        self.at("cut the peripheral")
        cut = DashedLine([CUTX, 3.3, 0], [CUTX, -3.3, 0], color=RED, stroke_width=6)
        cl = T("cut", 34, RED).move_to([CUTX + 0.6, 3.45, 0])
        self.play(Create(cut), FadeIn(cl), run_time=1.0)
        distal = VGroup(*[Line(A.tip_home(i, A.ecut[i]), A.S[i]).set_stroke(BLUE, 4, opacity=0.9) for i in range(N)])
        A.cap.set_value(1.0)
        self.add(distal)
        self.play(FadeOut(distal), FadeOut(skin), FadeOut(cut), FadeOut(cl), run_time=1.6)
        self.at("Several blue types")
        self.play(F.sup.animate.set_value(1.0), run_time=2.0)
        self.at("gather")
        ring = Circle(1.3, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.10).move_to(ISL)
        a = F.prep([island(i) if i in INJ else None for i in range(N)])
        self.play(Create(ring), run_time=0.5)
        self.play(a, F.c.animate.set_value(1.0), A.v.animate.set_value(0.15), run_time=1.8)
        at = T("Atf3-rich", 32, RED).move_to([ISL[0], 2.05, 0])
        self.at("rich")
        self.play(FadeIn(at, shift=DOWN * 0.2), run_time=0.8)
        self.at("Is that cluster")
        qt = T("New permanent type, or shared state?", 28, TEXT).move_to([2.9, 3.4, 0])
        self.play(FadeIn(qt), run_time=0.8)
        d1, d2 = doors()
        self.at("new permanent")
        self.play(FadeIn(d1, shift=UP * 0.3), run_time=0.6)
        self.at("shared state")
        self.play(FadeIn(d2, shift=UP * 0.3), run_time=0.6)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        F, tree, A = build_s04_state(self, "cut")
        ring = island_mob()
        ring._sc = self
        at = T("Atf3-rich", 32, RED).move_to([ISL[0], 2.05, 0])
        qt = T("New permanent type, or shared state?", 28, TEXT).move_to([2.9, 3.4, 0])
        d1, d2 = doors()
        self.add(tree, A.lines, F.grp, sch(), ring, at, qt, d1, d2)
        self.finish()


class S06Injury(SpokenScene):
    def construct(self):
        F, tree, A = build_s04_state(self, "cut")
        ring = island_mob()
        ring._sc = self
        at = T("Atf3-rich", 32, RED).move_to([ISL[0], 2.05, 0])
        qt = T("New permanent type, or shared state?", 28, TEXT).move_to([2.9, 3.4, 0])
        d1, d2 = doors()
        self.add(tree, A.lines, F.grp, ring, at, qt, d1, d2)
        self.play(d1.animate.set_opacity(0.2), d2.animate.scale(1.1), run_time=1.4)
        self.at("Existing neurons")
        halos = VGroup(*[F.halo(i, GOLD, 0.48) for i in INJ])
        self.play(FadeIn(halos), run_time=0.8)
        self.at("The red program")
        reg = T("regeneration", 32, RED).move_to([ISL[0], 2.05, 0])
        self.play(FadeOut(halos), Transform(at, reg), A.v.animate.set_value(0.35), run_time=2.6)
        self.at("suppressing")
        sg = T("signatures suppressed", 30, RED).move_to([ISL[0], 2.05, 0])
        self.play(Transform(at, sg), run_time=1.0)
        self.at("As axons regrow")
        T_ = ValueTracker(0)
        skin = skin_mob(label=False)
        skin[0].add_updater(lambda m: m.set_fill(GREY, 0.12 * clip((T_.get_value() - 0.1) / 0.3)))
        skin[0].set_fill(GREY, 0)
        F.src = [injured(i) for i in range(N)]
        F.dst = [home(i) for i in range(N)]
        F.pf = lambda: smooth((T_.get_value() - 0.5) / 0.5)
        F.cf = lambda: clip(1 - T_.get_value() / 0.8)
        F.sf = lambda: clip(1 - (T_.get_value() - 0.35) / 0.5)
        A.vf = lambda: 0.35 + 0.65 * T_.get_value()
        A.cap.set_value(0)
        ring.add_updater(lambda m: m.set_opacity(clip(1 - T_.get_value() / 0.4)))
        at.add_updater(lambda m: m.set_opacity(clip(1 - T_.get_value() / 0.2)))
        track = Line([1.7, -3.45, 0], [6.4, -3.45, 0]).set_stroke(TEXT, 6)
        knob = Dot(radius=0.2, color=GOLD)
        knob.add_updater(lambda m: m.move_to([1.7 + 4.7 * T_.get_value(), -3.45, 0]))
        rl = T("recovery time", 30, TEXT).move_to([-0.3, -3.45, 0])
        st = T("schematic trajectory", 30, TEXT).move_to([0.9, 3.4, 0])
        self.add(skin)
        self.play(FadeOut(qt), FadeOut(d1), FadeOut(d2), FadeIn(track), FadeIn(knob), FadeIn(rl), FadeIn(st), run_time=0.8)
        self.play(T_.animate.set_value(1.0), run_time=6.8, rate_func=linear)
        self.at("Their fixed gold")
        halos2 = VGroup(*[F.halo(i, GOLD, 0.48) for i in range(N)])
        self.play(FadeIn(halos2), run_time=0.8)
        co = T("continuity", 32, GOLD).move_to([SKIN_X + 1.7, -1.0, 0])
        self.at("continuity")
        self.play(FadeIn(co, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S07Causality(SpokenScene):
    def construct(self):
        F, tree = make_world(self, d=1.0)
        self.add(tree, F.grp)
        self.play(F.al.animate.set_value(0.28), tree.animate.set_stroke(opacity=0.3), run_time=1.0)
        c1 = chip("axon regrowth", TEXT, size=30).move_to([3.8, 2.9, 0])
        c2 = chip("identity returns", TEXT, size=30).move_to([3.8, 0.7, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(c2, shift=DOWN * 0.2), run_time=0.8)
        arrow = flow_dashes([3.8, 2.45, 0], [3.8, 1.15, 0], self)
        self.play(FadeIn(arrow), run_time=0.6)
        self.at("cannot prove")
        q = T("?", 80, GREY, weight=BOLD).move_to([5.1, 1.8, 0])
        q.add_updater(lambda m: m.move_to([5.1, 1.8 + 0.08 * np.sin(2.5 * self.renderer.time), 0]))
        self.play(FadeIn(q, scale=0.4), run_time=0.8)
        self.at("Tracing injured")
        tl = Line([-0.8, -2.7, 0], [6.4, -2.7, 0]).set_stroke(TEXT, 6)
        tk = VGroup(T("1 week", 28, TEXT).move_to([0.2, -3.3, 0]), T("2 months", 28, TEXT).move_to([5.6, -3.3, 0]))
        gl = T("reporter-positive share unchanged", 28, GOLD).move_to([2.7, -1.75, 0])
        self.play(Create(tl), FadeIn(tk), run_time=0.6)
        self.play(FadeIn(gl, shift=UP * 0.2), run_time=0.6)
        self.at("argues against")
        card = chip("selective death", RED, size=30).move_to([3.8, -0.6, 0])
        self.play(FadeIn(card), run_time=0.6)
        strike = Line(card.get_left() + RIGHT * 0.1, card.get_right() + LEFT * 0.1).set_stroke(RED, 6)
        self.play(Create(strike), run_time=0.7)
        res = T("argues against", 32, TEXT).move_to(card)
        self.play(FadeOut(strike), Transform(card, res), run_time=1.0)
        self.at("It still does not")
        self.play(Indicate(c2, color=TEXT, scale_factor=1.08), run_time=1.5)
        self.at("restores identity")
        self.play(Indicate(c1, color=TEXT, scale_factor=1.08), run_time=1.5)
        self.at("Keep the causal")
        self.play(Indicate(arrow, color=TEXT, scale_factor=1.15), run_time=1.5)
        self.finish()


# ---- species trees -------------------------------------------------------------------------
BR = [("C-fibre touch", 2.0), ("Aδ touch", 0.0), ("cold-sensing", -2.0)]
XM, XH = -6.6, 1.2


def half(sc, xL, name, sizes, text):
    """sizes: dict branch index -> badge scale. Returns VGroup parts."""
    lines = VGroup(Line([xL, 0, 0], [xL + 0.7, 0, 0]), Line([xL + 0.7, 2.0, 0], [xL + 0.7, -2.0, 0]))
    cells, labs, badges = [], VGroup(), {}
    for k, (nm, y) in enumerate(BR):
        lines.add(Line([xL + 0.7, y, 0], [xL + 1.7, y, 0]))
        labs.add(T(nm, 28, BLUE).move_to([xL + 2.3, y + 0.68, 0]))
        for j in range(2):
            c = Circle(0.34, stroke_color=GOLD, stroke_width=5).set_fill(BLUE, 0.8)
            hp = np.array([xL + 1.95 + 0.7 * j, y, 0.0])
            c.hp = hp
            c.ph = np.random.RandomState(k * 2 + j).uniform(0, 6.28)
            c.move_to(hp)
            c.add_updater(lambda m: m.move_to(m.hp + 0.07 * np.array([np.sin(0.9 * sc.renderer.time + m.ph), np.cos(0.8 * sc.renderer.time + m.ph), 0])))
            cells.append(c)
    lines.set_stroke(TEXT, 12, opacity=0.95)
    for k, s in sizes.items():
        y = BR[k][1]
        w = 1.5 * s
        h = 0.75 * s
        r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35)
        g = VGroup(r)
        if s >= 1.0:
            g.add(T(text, 26, TEXT).move_to(r))
        g.move_to([xL + 4.5, y, 0])
        badges[k] = g
    head = T(name, 36, TEXT, weight=BOLD).move_to([xL + 2.6, 3.2, 0])
    return lines, VGroup(*cells), labs, badges, head


class S08Species(SpokenScene):
    def construct(self):
        F, tree = make_world(self, d=1.0)
        self.add(tree, F.grp)
        ml, mc, mlab, mb, mh = half(self, XM, "mouse", {0: 1.0}, "Tafa4")
        hl, hc, hlab, hb, hh = half(self, XH, "human", {1: 1.0, 2: 0.55, 0: 0.55}, "TAFA4")
        self.play(F.al.animate.set_value(0), ReplacementTransform(tree, ml), TransformFromCopy(ml, hl), FadeIn(mc), FadeIn(hc),
                  FadeIn(mlab), FadeIn(hlab), FadeIn(mh), FadeIn(hh), run_time=2.6)
        self.at("In mouse")
        self.play(Indicate(mlab[0], color=BLUE, scale_factor=1.12), run_time=1.0)
        self.at("mainly associated")
        self.play(FadeIn(mb[0], scale=0.5), run_time=1.0)
        self.at("In human tissue")
        self.play(Indicate(hh, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.at("strongest")
        self.play(FadeIn(hb[1], scale=0.5), run_time=1.0)
        self.at("It also appeared")
        self.play(Indicate(hlab[2], color=BLUE, scale_factor=1.12), run_time=1.0)
        self.play(FadeIn(hb[2], scale=0.5), run_time=1.0)
        self.at("fiber touch populations")
        self.play(FadeIn(hb[0], scale=0.5), run_time=1.0)
        self.at("The same marker")
        ex = T("expression, not function", 32, TEXT).move_to([-0.2, -3.45, 0])
        self.play(FadeIn(ex, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S09Method(SpokenScene):
    def construct(self):
        ml, mc, mlab, mb, mh = half(self, XM, "mouse", {0: 1.0}, "Tafa4")
        hl, hc, hlab, hb, hh = half(self, XH, "human", {1: 1.0, 2: 0.55, 0: 0.55}, "TAFA4")
        self.add(ml, mc, mlab, hl, hc, hlab, mh, hh, *[b for b in mb.values()], *[b for b in hb.values()])
        panel = RoundedRectangle(corner_radius=0.2, width=2.3, height=1.2, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.2).move_to([-0.1, 0.9, 0])
        lab = T("whole cell", 28, TEXT).move_to(panel)
        pill = RoundedRectangle(corner_radius=0.2, width=1.2, height=0.4, stroke_color=TEXT, stroke_width=3).move_to([-0.1, -0.3, 0])
        kn = Dot(radius=0.14, color=TEAL).move_to([-0.45, -0.3, 0])
        self.play(FadeIn(panel), FadeIn(lab), FadeIn(pill), FadeIn(kn), run_time=1.2)
        self.at("Whole cells")
        lab2 = T("nucleus", 28, TEXT).move_to(panel)
        self.at("nuclei")
        self.play(Transform(lab, lab2), kn.animate.move_to([0.25, -0.3, 0]), hb[2].animate.set_opacity(0.1), mb[0].animate.set_opacity(0.4), run_time=1.4)
        self.at("A missing group")
        gone = VGroup(hc[4], hc[5])
        nc = T("not captured", 28, GREY).move_to([XH + 2.3, -2.0 - 0.7, 0])
        self.play(gone.animate.set_opacity(0.15), FadeIn(nc), run_time=1.4)
        self.at("not biological")
        self.play(Indicate(nc, color=GREY, scale_factor=1.1), run_time=1.5)
        self.at("Integration methods")
        self.play(FadeOut(panel), FadeOut(lab), FadeOut(pill), FadeOut(kn), FadeOut(nc), gone.animate.set_opacity(1.0), hb[2].animate.set_opacity(1.0), mb[0].animate.set_opacity(1.0), run_time=0.8)
        lb = VMobject().set_points_as_corners([[-0.7, 1.3, 0], [-1.0, 1.3, 0], [-1.0, -1.3, 0], [-0.7, -1.3, 0]]).set_stroke(TEAL, 8)
        rb = VMobject().set_points_as_corners([[0.5, 1.3, 0], [0.8, 1.3, 0], [0.8, -1.3, 0], [0.5, -1.3, 0]]).set_stroke(TEAL, 8)
        il = T("integration", 30, TEAL).move_to([-0.1, 2.0, 0])
        self.play(FadeIn(lb), FadeIn(rb), FadeIn(il), run_time=0.8)
        self.play(lb.animate.shift(RIGHT * 0.45), rb.animate.shift(LEFT * 0.45), run_time=2.2)
        self.at("merge real")
        top = VGroup(hc[0], hc[1])
        mid = VGroup(hc[2], hc[3])
        for m in (top, mid):
            for c in m:
                c.clear_updaters()
        self.play(FadeOut(hlab[0]), FadeOut(hlab[1]), run_time=0.4)
        self.play(top.animate.shift(DOWN * 1.0), mid.animate.shift(UP * 1.0 + RIGHT * 1.4), run_time=1.6)
        mg = T("merged", 28, TEAL).move_to([XH + 3.0, 1.9, 0])
        self.play(FadeIn(mg), run_time=0.6)
        self.at("Match preparations")
        self.play(FadeOut(lb), FadeOut(rb), FadeOut(il), run_time=0.6)
        names = [("matched method", -4.3, "Match preparations"), ("tissue validation", -0.1, "validate markers"), ("independent function", 4.3, "seek independent")]
        for nm, x, ph in names:
            c = chip(nm, TEXT, size=28).move_to([x, -3.35, 0])
            tick = VMobject().set_points_as_corners([[-0.15, 0, 0], [-0.03, -0.12, 0], [0.18, 0.15, 0]]).set_stroke(GREEN, 6)
            tick.next_to(c, LEFT, buff=0.1)
            self.at(ph, lead=0.1)
            self.play(FadeIn(c, shift=UP * 0.3), Create(tick), run_time=0.9)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        xs = [-5.1, -1.7, 1.7, 5.1]
        names = ["developing", "adult", "injured", "recovered"]
        frames, cells, labs, bds = VGroup(), VGroup(), VGroup(), VGroup()
        for k, (x, nm) in enumerate(zip(xs, names)):
            fr = RoundedRectangle(corner_radius=0.2, width=3.2, height=3.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.05).move_to([x, 0.2, 0])
            col = RED if k == 2 else BLUE
            c = Circle(0.6, stroke_color=GOLD, stroke_width=6).set_fill(col, 0.8)
            c.hp = np.array([x, 0.0, 0.0])
            c.ph = k * 1.3
            c.move_to(c.hp)
            c.add_updater(lambda m: m.move_to(m.hp + 0.08 * np.array([np.sin(1.0 * self.renderer.time + m.ph), np.cos(0.8 * self.renderer.time + m.ph), 0])))
            nb = {0: 3, 1: 1, 2: 0, 3: 1}[k]
            for q in range(nb):
                sq = Square(0.3, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([x + (q - (nb - 1) / 2) * 0.42, 1.1, 0])
                sq.add_updater(lambda m, q=q: m.set_fill(TEAL, 0.85 + 0.15 * np.sin(2 * self.renderer.time + q)))
                bds.add(sq)
            frames.add(fr)
            cells.add(c)
            labs.add(T(nm, 30, RED if k == 2 else TEXT).move_to([x, -1.9, 0]))
        self.add(frames)
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.25), FadeIn(cells, lag_ratio=0.25), FadeIn(bds), run_time=3.0)
        self.play(FadeIn(labs, lag_ratio=0.2), run_time=1.0)
        self.at("Follow cells through")
        arr = Arrow([-5.1, 2.45, 0], [5.1, 2.45, 0], color=TEXT, stroke_width=6, buff=0)
        tl = T("time", 28, TEXT).move_to([0, 2.95, 0])
        self.play(Create(arr), FadeIn(tl), run_time=1.5)
        self.at("Cross")
        f1 = chip("mouse method", TEAL, size=28).move_to([-2.2, -3.2, 0])
        f2 = chip("human method", TEAL, size=28).move_to([2.2, -3.4, 0])
        self.play(FadeIn(f1), FadeIn(f2), run_time=1.0)
        self.at("matching the view")
        self.play(f2.animate.move_to([2.2, -3.2, 0]), run_time=1.2)
        self.at("Identity is biological")
        self.play(Indicate(cells, color=GOLD, scale_factor=1.15), run_time=1.5)
        self.at("every atlas samples")
        br = VGroup(*[Line(a, b).set_stroke(TEXT, 8) for a, b in [([-6.8, 1.9, 0], [-6.4, 1.9, 0]), ([-6.8, 1.9, 0], [-6.8, 1.5, 0])]])
        view = Rectangle(width=13.4, height=3.6, stroke_color=TEXT, stroke_width=6).move_to([0, 0.2, 0])
        self.play(Create(view), run_time=0.6)
        self.play(view.animate.set(width=3.4, height=3.4).move_to([1.7, 0.2, 0]), run_time=1.0)
        self.play(view.animate.set(width=13.4, height=3.6).move_to([0, 0.2, 0]), run_time=0.9)
        self.finish()


class S11End(EndCard):
    LINE = "Identity is biological, but every atlas samples it."
