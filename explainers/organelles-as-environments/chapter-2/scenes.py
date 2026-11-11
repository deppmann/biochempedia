"""Follow the Markers: organelles as environments, chapter 2.

COLOR MAP (kept from chapter 1): PROTON = red-orange dots; pumps = GOLD; leaks/walls = GREY;
cytosol reference = white dashed. New here: unknown protein = MAGENTA, histone H3 = LAVENDER,
cathepsin D = PROTON, pyruvate kinase = white, substrate = GREEN, product = YELLOW.
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

PROTON = "#FF7043"
MAGENTA = "#E040FB"
LAVENDER = "#B39DDB"
DETERGENT = "#7FDBFF"
CELL_X = 2.55
LADDER_X = -5.25
CYTO_PH = 7.2


# ---------------------------------------------------------------- shared helpers
class FilmScene(SpokenScene):
    """A living field of slow protons behind everything, so a held frame is never dead."""

    def setup(self):
        super().setup()
        rng = np.random.default_rng(sum(map(ord, os.environ.get("KX_SCENE_ID", "scene"))))
        field = VGroup()
        for _ in range(60):
            d = Dot([rng.uniform(-6.8, 6.8), rng.uniform(-3.65, 3.65), 0], radius=.06,
                    color=PROTON).set_opacity(.3)
            d.speed = rng.uniform(.6, .9)
            d.add_updater(lambda m, dt: m.shift(RIGHT * m.speed * dt) if m.get_x() < 6.9
                          else m.move_to([-6.8, m.get_y(), 0]))
            field.add(d)
        field.set_z_index(-20)
        self.add(field)


def arrow(a, b, color=GREY, width=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=0.22)


class Poly(VMobject):
    """An open polyline: opacity changes touch only the stroke (never a fill)."""
    def set_opacity(self, opacity, family=True):
        return self.set_stroke(opacity=opacity, family=family)


def poly(pts, color, w=5):
    return Poly().set_points_as_corners([np.array(p, dtype=float) for p in pts]).set_stroke(color, w).set_fill(opacity=0)


def drift(m, amp=.06, speed=1.0, seed=0):
    m._b = m.get_center().copy()
    m._t = seed * 7.1

    def f(mm, dt):
        mm._t += dt * speed
        mm.move_to(mm._b + np.array([amp * np.sin(mm._t * 1.3 + seed), amp * np.cos(mm._t * .9 + seed * 2), 0]))
    m.add_updater(f)
    return m


def ph_y(p):
    return -2.75 + (p - 4.0) * (5.5 / 4.5)


def proton(pos, r=0.075, opacity=1):
    return Dot(pos, radius=r, color=PROTON).set_opacity(opacity)


def ladder():
    x = LADDER_X
    axis = Line([x, -2.75, 0], [x, 2.75, 0], color=GREY, stroke_width=4)
    title = T("pH", 30, TEXT, weight=BOLD).move_to([x, 3.15, 0])
    ticks, labels = VGroup(), VGroup()
    for p in (4, 5, 6, 7, 8):
        y = ph_y(p)
        ticks.add(Line([x - .13, y, 0], [x + .13, y, 0], color=GREY, stroke_width=3))
        labels.add(M(str(p), 28, GREY).move_to([x - .48, y, 0]))
    cy = DashedLine([x - .75, ph_y(CYTO_PH), 0], [x + 1.65, ph_y(CYTO_PH), 0], color=TEXT, stroke_width=4)
    cyt = T("cytosol 7.2", 28, TEXT).move_to([x + 1.25, ph_y(CYTO_PH) + .32, 0])
    return VGroup(axis, title, ticks, labels, cy, cyt)


def marker(p, label, color=PROTON):
    d = Dot([LADDER_X + .2, ph_y(p), 0], radius=.12, color=color)
    t = T(label, 28, color).next_to(d, RIGHT, buff=.18)
    return VGroup(d, t)


def cell_world(labels=("lysosome", "nucleus")):
    """Chapter 1's cutaway at the same scale and place: [cell, lyso, golgi, er, nucleus, mito, labels, dots]."""
    cell = Ellipse(width=7.1, height=6.05, stroke_color=GREY, stroke_width=5,
                   fill_color=GREY, fill_opacity=.13).move_to([CELL_X, -.05, 0])
    lyso = Circle(radius=.68, color=PROTON, stroke_width=4, fill_color=PROTON,
                  fill_opacity=.12).move_to([1.45, 1.45, 0])
    golgi = VGroup(*[Arc(radius=.72 + .17 * i, start_angle=-1.15, angle=2.3,
                         color=PROTON, stroke_width=5) for i in range(3)]).move_to([3.25, 1.35, 0])
    er = VGroup(*[Arc(radius=.75 + .24 * i, start_angle=2.75, angle=2.75,
                      color=TEAL, stroke_width=5) for i in range(3)]).move_to([1.25, -.65, 0])
    nucleus = Circle(radius=1.0, color=TEXT, stroke_width=4, fill_color=TEXT,
                     fill_opacity=.035).move_to([3.45, -.55, 0])
    mito = RoundedRectangle(width=2.0, height=.92, corner_radius=.45, color=BLUE,
                            stroke_width=4, fill_color=BLUE, fill_opacity=.06).rotate(-.16).move_to([4.55, -2.05, 0])
    spec = {"lysosome": T("lysosome", 28, PROTON).next_to(lyso, UP, .12).shift(RIGHT * .3),
            "Golgi": T("Golgi", 28, PROTON).next_to(golgi, UP, .12),
            "ER": T("ER", 28, TEAL).next_to(er, LEFT, .12),
            "nucleus": T("nucleus", 28, TEXT).move_to(nucleus),
            "mitochondrion": T("mitochondrion", 28, BLUE).move_to([1.95, -2.4, 0])}
    labs = VGroup(*[spec[k] for k in labels])
    dots = VGroup(*[proton([x, y, 0], .045, .5) for x, y in
                    [(.2, 2.1), (2.5, 2.5), (4.8, 1.7), (5.1, -.2), (.25, -2.0), (2.2, -2.5)]])
    return VGroup(cell, lyso, golgi, er, nucleus, mito, labs, dots)


def star(pos, r=.32, color=MAGENTA):
    return Star(n=5, outer_radius=r, inner_radius=r * .45, color=color, stroke_width=2,
                fill_color=color, fill_opacity=1).move_to(pos)


# ---------------------------------------------------------------- fractionation world
TUBE_X = [-4.95, -1.65, 1.65, 4.95]
TUBE_Y, TUBE_W, TUBE_H = 1.0, 1.1, 3.0
SLOT_Y, SLOT_W, SLOT_H = -2.35, .95, 1.3
ROW_Y, K = .9, 3.0
COMP = {0: dict(n=4, l=1, h=1), 1: dict(n=1, l=2, h=2), 2: dict(n=0, l=6, h=2), 3: dict(n=0, l=1, h=15)}
_LAY = {}


def layout(i):
    if i in _LAY:
        return _LAY[i]
    rng = np.random.default_rng(100 + i)
    kinds = ["n"] * COMP[i]["n"] + ["l"] * COMP[i]["l"] + ["h"] * COMP[i]["h"]
    mind = {"n": .30, "l": .19, "h": .11}
    out = []
    for k in kinds:
        for _ in range(300):
            u, v = rng.uniform(-1, 1), rng.uniform(0, 1)
            p = np.array([u * SLOT_W * .4, v * SLOT_H * .62])
            if all(np.linalg.norm(p - np.array([q[1] * SLOT_W * .4, q[2] * SLOT_H * .62])) >
                   (mind[k] + mind[q[0]]) / 2 + .02 for q in out):
                break
        out.append((k, u, v))
    _LAY[i] = out
    return out


def fpos(i, u, v, cy=SLOT_Y, k=1.0):
    return np.array([TUBE_X[i] + u * SLOT_W * .4 * k, cy - SLOT_H * k / 2 + .1 * k + v * SLOT_H * .62 * k, 0])


def make_item(kind, s=1.0):
    if kind == "n":
        return Circle(radius=.14 * s, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.12)
    if kind == "l":
        return Dot(radius=.075 * s, color=PROTON)
    return Dot(radius=.04 * s, color=TEXT).set_opacity(.5)


def tube(cx, cy, w, h, level=.85):
    out = RoundedRectangle(width=w, height=h, corner_radius=min(.3, w * .4), color=TEXT, stroke_width=4,
                           fill_opacity=0).move_to([cx, cy, 0])
    lh = (h - .1) * level
    liq = RoundedRectangle(width=w - .1, height=lh, corner_radius=min(.25, w * .35), stroke_width=0,
                           fill_color=GREY, fill_opacity=.22).move_to([cx, cy - h / 2 + .05 + lh / 2, 0])
    return VGroup(liq, out)


def slot_tube(i, cy=SLOT_Y, k=1.0):
    return tube(TUBE_X[i], cy, SLOT_W * k, SLOT_H * k, .9)


def build_row(item_scale=1.7):
    """The four collected fractions, enlarged into a row (the end of s03, all of s03b). Returns fracs, labels."""
    fracs, labs = [], VGroup()
    for i in range(4):
        g = VGroup(slot_tube(i, ROW_Y, K))
        for kind, u, v in layout(i):
            it = make_item(kind, item_scale)
            it.move_to(fpos(i, u, v, ROW_Y, K))
            g.add(it)
        fracs.append(g)
        labs.add(T(f"F{i + 1}", 34, TEXT, weight=BOLD).move_to([TUBE_X[i], ROW_Y - SLOT_H * K / 2 - .42, 0]))
    return fracs, labs


# ---------------------------------------------------------------- marker chart
CH_X = [-3.9, -1.3, 1.3, 3.9]
OFFS = [-.72, 0, .72]
Y0, HS = -2.2, 4.2
MARKS = [("histone H3", LAVENDER, [.80, .10, .05, .05], "nucleus"),
         ("cathepsin D", PROTON, [.05, .20, .60, .15], "lysosome"),
         ("pyruvate kinase", TEXT, [.05, .05, .10, .80], "cytosol")]
UNK = [.72, .14, .08, .06]


def bar(j, i, op=.75):
    v = MARKS[j][2][i]
    return Rectangle(width=.62, height=HS * v, stroke_width=0, fill_color=MARKS[j][1], fill_opacity=op) \
        .move_to([CH_X[i] + OFFS[j], Y0 + HS * v / 2, 0])


def line_pts(vals, j):
    return [[CH_X[i] + OFFS[j], Y0 + HS * vals[i], 0] for i in range(4)]


def small_tubes():
    g = VGroup()
    for i in range(4):
        t = tube(CH_X[i], -2.95, 1.5, .9, .8)
        g.add(VGroup(t, T(f"F{i + 1}", 30, TEXT, weight=BOLD).move_to([CH_X[i], -2.95, 0])))
    return g


def axes_parts():
    xa = Line([-5.4, Y0, 0], [5.4, Y0, 0], color=GREY, stroke_width=4)
    ya = Line([-5.4, Y0, 0], [-5.4, Y0 + HS, 0], color=GREY, stroke_width=4)
    yl = T("share of protein", 28, TEXT).rotate(PI / 2).move_to([-6.4, Y0 + HS / 2 - .3, 0])
    t1 = T("1", 28, GREY).move_to([-5.7, Y0 + HS, 0])
    t0 = T("0", 28, GREY).move_to([-5.7, Y0, 0])
    return VGroup(xa, ya, yl, t1, t0)


def legend_row(j):
    name, col, _, zone = MARKS[j]
    txt = {0: "nucleus (histone H3)", 1: "lysosome (cathepsin D)", 2: "cytosol (pyruvate kinase)"}[j]
    sq = Square(.26, stroke_width=0, fill_color=col, fill_opacity=1)
    return VGroup(sq, T(txt, 26, col)).arrange(RIGHT, buff=.2)


def legend_group():
    g = VGroup(*[legend_row(j) for j in range(3)]).arrange(DOWN, aligned_edge=LEFT, buff=.2)
    return g.move_to([-.3, 2.15, 0])


def chart(dim=False, tubes=True, legend=True):
    """Final state of the s04 chart, rebuilt identically where a later scene needs it."""
    d = {}
    d["axes"] = axes_parts()
    d["tubes"] = small_tubes() if tubes else VGroup()
    d["bars"] = [VGroup(*[bar(j, i, .42 if dim else .75) for i in range(4)]) for j in range(3)]
    d["lines"] = [poly(line_pts(MARKS[j][2], j), MARKS[j][1], 4).set_opacity(.6 if dim else .9) for j in range(3)]
    d["legend"] = legend_group() if legend else VGroup()
    return d


def chart_all(d):
    return VGroup(d["axes"], d["tubes"], *d["bars"], *d["lines"], d["legend"])


# ---------------------------------------------------------------- latency world
CY = -.3


def bouncer(dot, ring, tubebox, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0, TAU)
    dot.v = np.array([np.cos(a), np.sin(a)]) * rng.uniform(.8, 1.3)

    def f(m, dt):
        c = ring.get_center()[:2]
        R = ring.width / 2
        l, r, b, t = tubebox.get_left()[0], tubebox.get_right()[0], tubebox.get_bottom()[1], tubebox.get_top()[1]
        p = m.get_center()[:2] + m.v * dt
        if p[0] < l + .2 or p[0] > r - .2:
            m.v[0] *= -1
        if p[1] < b + .2 or p[1] > t - .2:
            m.v[1] *= -1
        dd = p - c
        dist = np.linalg.norm(dd)
        if dist < R + .13:
            n = dd / max(dist, 1e-6)
            m.v = m.v - 2 * np.dot(m.v, n) * n
            p = c + n * (R + .14)
        m.move_to([p[0], p[1], 0])
    dot.add_updater(f)
    return dot


def make_unit(cx, side="L", level=.12, ndots=9, seed=1, name_label=None):
    tb = RoundedRectangle(width=4.4, height=5.6, corner_radius=.35, color=GREY, stroke_width=5,
                          fill_color=BLUE, fill_opacity=.05).move_to([cx, CY, 0])
    ring = Circle(radius=1.7, color=GREY, stroke_width=10, fill_color=PROTON, fill_opacity=.08).move_to([cx, CY, 0])
    enz = chip("acid\nphosphatase", GOLD, 28).move_to([cx, CY, 0])
    mx = cx - 3.0 if side == "L" else cx + 3.0
    tr = ValueTracker(level)
    mbox = Rectangle(width=.55, height=2.4, color=GREY, stroke_width=4).move_to([mx, CY, 0])

    def mk():
        h = max(.02, 2.3 * tr.get_value())
        c = mbox.get_center()
        return Rectangle(width=.45, height=h, stroke_width=0, fill_color=GOLD, fill_opacity=.9) \
            .move_to([c[0], c[1] - 1.2 + .05 + h / 2, 0])
    fill = always_redraw(mk)
    mlab = T("activity", 28, TEXT).move_to([mx, CY + 1.2 + .38, 0])
    rng = np.random.default_rng(seed)
    dots = []
    while len(dots) < ndots:
        p = np.array([cx + rng.uniform(-1.9, 1.9), CY + rng.uniform(-2.5, 2.5)])
        if np.linalg.norm(p - np.array([cx, CY])) > 1.95:
            d = Dot([p[0], p[1], 0], radius=.09, color=GREEN)
            dots.append(bouncer(d, ring, tb, seed * 31 + len(dots)))
    body = VGroup(tb, ring, enz, mbox, fill, mlab, *dots)
    return dict(body=body, tube=tb, ring=ring, enz=enz, mbox=mbox, tr=tr, dots=dots, cx=cx)


def flow_dots(unit, n=7, color=GREEN, to_enz=True, seed=3):
    """Dots that loop forever between the tube side and the enzyme (substrate in) or out (product)."""
    rng = np.random.default_rng(seed)
    cx = unit["cx"]
    E = np.array([cx, CY])
    out = []
    for k in range(n):
        a = rng.uniform(0, TAU)
        A = E + np.array([np.cos(a), np.sin(a) * 1.15]) * 2.0
        A[0] = np.clip(A[0], cx - 2.0, cx + 2.0)
        ph = k / n
        d = Dot([A[0], A[1], 0], radius=.085, color=color)
        d.ph, d.A = ph, A

        def f(m, dt, E=E):
            m.ph = (m.ph + dt * .33) % 1.0
            fr = m.ph
            s = fr * fr * (3 - 2 * fr)
            P = (m.A + (E - m.A) * s * .42) if to_enz else (E + (m.A - E) * (.42 + .58 * s))
            m.move_to([P[0], P[1], 0])
            m.set_opacity(min(1, fr * 6, (1 - fr) * 6))
        d.add_updater(f)
        out.append(d)
    return out


def dropper(tip, bulb):
    body = Line(tip, bulb, color=GREY, stroke_width=22)
    nozzle = Line(tip, tip + (np.array(bulb) - np.array(tip)) * .0 + np.array([0, -.22, 0]), color=TEXT, stroke_width=8)
    bb = Circle(radius=.34, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.5).move_to(bulb)
    return VGroup(body, nozzle, bb)


# =============================================================== scenes
class S00Link(FilmScene):
    def construct(self):
        l = ladder().set_opacity(.35)
        world = cell_world(("lysosome", "nucleus"))
        for m in (world[2], world[3], world[5]):
            m.set_opacity(.35)
        pump_in = arrow([.1, 1.45, 0], [.72, 1.45, 0], GOLD, 7)
        pump_out = arrow([4.5, -1.7, 0], [4.5, -1.05, 0], GOLD, 7).set_opacity(.45)
        st = star([-.15, 2.8, 0])
        slab = T("protein ?", 28, MAGENTA).move_to([-1.75, 2.8, 0])
        q = T("Which compartment holds it?", 32, TEXT, weight=BOLD).move_to([2.55, 3.5, 0])
        for k, d in enumerate(world[7]):
            drift(d, .12, .8, k)
        self.play(FadeIn(l), Create(world[0]), FadeIn(world[1:7]), FadeIn(world[7]),
                  FadeIn(pump_in), FadeIn(pump_out), FadeIn(st, shift=DOWN * .3), FadeIn(slab), FadeIn(q), run_time=1.2)
        drift(st, .1, 1.2, 1)
        self.at("which compartment")
        self.play(Indicate(st, color=MAGENTA, scale_factor=1.3), run_time=.9)
        self.at("chapter 1")
        self.play(Indicate(pump_in, color=GOLD), Indicate(pump_out, color=GOLD), run_time=1.1)
        self.at("pumps and leaks")
        self.play(Indicate(world[1], color=PROTON, scale_factor=1.15), run_time=1.0)
        self.at("distinct chemistries")
        glow = DashedLine([LADDER_X - .8, ph_y(7.2), 0], [-3.4, ph_y(7.2), 0], color=TEXT, stroke_width=7)
        self.play(ShowPassingFlash(glow, time_width=.6), l.animate.set_opacity(.6), run_time=1.2)
        self.at("to relate that chemistry")
        self.play(Indicate(st, color=MAGENTA, scale_factor=1.4), run_time=1.0)
        self.at("first find")
        tg = [([.9, 1.85, 0], [.15, 2.4, 0]), ([2.85, .2, 0], [.4, 2.42, 0]), ([.1, .6, 0], [.1, 2.4, 0])]
        ars = []
        for tip, st_ in tg:
            a = DashedLine(st_, tip, color=MAGENTA, stroke_width=4, dash_length=.12).add_tip(tip_length=.2)
            ars.append(a)
            self.play(Create(a), run_time=.55)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Organelles as environments"
    TITLE = "Follow the Markers"


class S02Look(FilmScene):
    def construct(self):
        world = cell_world(())
        lc = np.array([1.45, 1.45, 0])
        C = np.array([0, -.1, 0])
        R = 2.3
        self.play(FadeIn(world), run_time=.5)
        self.play(world.animate.scale(3.4, about_point=lc).shift(C - lc), run_time=1.3)
        ring = Circle(radius=R, color=GREY, stroke_width=12, fill_color=PROTON, fill_opacity=.07).move_to(C)
        self.play(FadeIn(ring), FadeOut(world), run_time=.5)
        self.at("at the lysosome")
        lab = T("imaging: at the lysosome", 30, MAGENTA, weight=BOLD).move_to([0, 3.15, 0])
        rng = np.random.default_rng(4)
        stars = VGroup(*[star([rng.uniform(-3, 3), rng.uniform(-2.6, 2.4), 0], .16) for _ in range(7)])
        glow = Circle(radius=.8, stroke_width=0, fill_color=MAGENTA, fill_opacity=.25).move_to(C + RIGHT * R)
        angs = np.linspace(-.6, .6, 7)
        self.play(FadeIn(lab), FadeIn(stars), run_time=.3)
        self.play(*[s.animate.move_to(C + np.array([np.cos(a), np.sin(a), 0]) * R) for s, a in zip(stars, angs)],
                  FadeIn(glow), run_time=1.2)
        self.play(Indicate(glow, color=MAGENTA), run_time=.6)
        self.at("but that is not inside")
        r2 = 1.95
        L, Rr = np.array([-3.45, -.1, 0]), np.array([3.45, -.1, 0])
        ringL, ringR = ring.copy(), ring.copy()
        self.add(ringL, ringR)
        self.remove(ring)
        starsR = stars.copy()
        self.add(starsR)
        tl = []
        for k, a in enumerate(angs):
            tl.append(stars[k].animate.move_to(L + np.array([np.cos(a), np.sin(a), 0]) * (r2 + .22)))
        tr = []
        for k, s in enumerate(starsR):
            a = angs[k]
            tr.append(s.animate.move_to(Rr + np.array([np.cos(a), np.sin(a), 0]) * (r2 * .55)))
        self.play(FadeOut(lab), FadeOut(glow), ringL.animate.scale(r2 / R).move_to(L),
                  ringR.animate.scale(r2 / R).move_to(Rr), *tl, *tr, run_time=1.3)
        tags = VGroup(T("on it", 32, MAGENTA, weight=BOLD).move_to([-3.45, -2.85, 0]),
                      T("in it", 32, MAGENTA, weight=BOLD).move_to([3.45, -2.85, 0]))
        self.play(FadeIn(tags), run_time=.5)
        self.at("that image alone")
        gl = Circle(radius=.75, stroke_width=0, fill_color=MAGENTA, fill_opacity=.4).move_to(L + RIGHT * r2)
        gr = gl.copy().move_to(Rr + RIGHT * r2)
        qm = T("?", 90, TEXT, weight=BOLD).move_to([0, -.1, 0])
        sch = T("schematic blur", 28, GREY).move_to([0, -3.4, 0])
        self.play(FadeIn(gl), FadeIn(gr), stars.animate.set_opacity(.25), starsR.animate.set_opacity(.25),
                  FadeIn(qm, scale=1.3), FadeIn(sch), run_time=1.0)
        self.at("which side")
        self.play(Indicate(qm, color=TEXT, scale_factor=1.25), gl.animate.scale(1.15), gr.animate.scale(1.15), run_time=1.2)
        self.play(gl.animate.scale(1 / 1.15), gr.animate.scale(1 / 1.15), Indicate(qm), run_time=1.2)
        self.finish()


class S03Spin(FilmScene):
    def construct(self):
        rng = np.random.default_rng(33)
        world = cell_world(())
        l = ladder().set_opacity(.35)
        items, dest = [], []
        for i in range(4):
            for kind, u, v in layout(i):
                it = make_item(kind)
                it.dest, it.lay = i, (u, v)
                a = rng.uniform(0, TAU)
                rr = np.sqrt(rng.uniform(0, 1))
                it.move_to([CELL_X + 3.0 * rr * np.cos(a), -.05 + 2.5 * rr * np.sin(a), 0])
                items.append(it)
        rng.shuffle(items)
        itg = VGroup(*items)
        tubes = [tube(TUBE_X[i], TUBE_Y, TUBE_W, TUBE_H, .85) for i in range(4)]
        self.play(FadeIn(world), FadeIn(l), FadeIn(itg), run_time=.6)
        self.at("cells apart")
        # contents move into one homogenate tube; the ladder slides away
        tpos = []
        for it in items:
            tpos.append([TUBE_X[0] + rng.uniform(-.38, .38), TUBE_Y + rng.uniform(-1.2, 1.7), 0])
        self.play(FadeOut(world), l.animate.shift(LEFT * 2).set_opacity(0), FadeIn(tubes[0]),
                  *[it.animate.move_to(p) for it, p in zip(items, tpos)], run_time=1.7)
        self.at("they break cells")
        homo = T("homogenate", 30, TEXT, weight=BOLD).move_to([TUBE_X[0] + .4, 3.0, 0])
        self.play(FadeIn(homo), run_time=.5)
        self.at("and separate the pieces")
        arr = arrow([-3.6, 3.15, 0], [3.8, 3.15, 0], GREY, 6)
        alab = T("stronger spins", 28, TEXT).move_to([0, 3.55, 0])
        self.play(FadeIn(arr), FadeIn(alab), FadeOut(homo), run_time=.4)

        slots = [slot_tube(i) for i in range(4)]
        for i in range(4):
            mine = [it for it in items if it.dest == i]
            rest = [it for it in items if it.dest > i]
            if i < 3:
                g = VGroup(*[arrow([TUBE_X[i] + s * .78, TUBE_Y + 1.1, 0], [TUBE_X[i] + s * .78, TUBE_Y - .1, 0],
                                   GREY, 5 + 2 * i) for s in (-1, 1)])
                pel = []
                for it in mine:
                    u, v = it.lay
                    pel.append([TUBE_X[i] + u * .36, TUBE_Y - TUBE_H / 2 + .2 + v * .45, 0])
                self.play(FadeIn(g, shift=DOWN * .2), *[it.animate.move_to(p) for it, p in zip(mine, pel)], run_time=.4)
                self.play(FadeIn(slots[i]), FadeOut(g),
                          *[it.animate.move_to(fpos(i, *it.lay)) for it in mine], run_time=.45)
                dx = TUBE_X[i + 1] - TUBE_X[i]
                self.play(FadeOut(tubes[i]), FadeIn(tubes[i + 1]),
                          *[it.animate.shift(RIGHT * dx) for it in rest], run_time=.4)
            else:
                self.play(FadeIn(slots[i]), FadeOut(tubes[i]),
                          *[it.animate.move_to(fpos(i, *it.lay)) for it in mine], run_time=.7)
        self.at("overlap across")
        fr = []
        for i in range(4):
            g = VGroup(slots[i], *[it for it in items if it.dest == i])
            fr.append(g)
        anims = []
        for i in range(4):
            anims.append(slots[i].animate.scale(K).move_to([TUBE_X[i], ROW_Y, 0]))
            for it in items:
                if it.dest == i:
                    anims.append(it.animate.scale(1.7).move_to(fpos(i, *it.lay, cy=ROW_Y, k=K)))
        self.play(FadeOut(arr), FadeOut(alab), *anims, run_time=1.1)
        labs = VGroup(*[T(f"F{i + 1}", 34, TEXT, weight=BOLD).move_to([TUBE_X[i], ROW_Y - SLOT_H * K / 2 - .42, 0])
                        for i in range(4)])
        self.at("crude fractions")
        self.play(FadeIn(labs), run_time=.5)
        self.at("no fraction")
        npure = T("no fraction assumed pure", 34, TEXT, weight=BOLD).move_to([-.5, -2.75, 0])
        tag = T("schematic", 28, GREY).move_to([5.3, -3.45, 0])
        self.play(FadeIn(npure, shift=UP * .15), FadeIn(tag), run_time=.7)
        self.play(*[slots[i].animate.shift(UP * .08) for i in range(4)], run_time=.8, rate_func=there_and_back)
        self.finish()


class S03bSettle(FilmScene):
    def construct(self):
        fracs, labs = build_row()
        npure = T("no fraction assumed pure", 34, TEXT, weight=BOLD).move_to([-.5, -2.75, 0])
        tag = T("schematic", 28, GREY).move_to([5.3, -3.45, 0])
        self.add(*fracs, labs, npure, tag)
        for rep in range(2):
            sgn = 1 if rep == 0 else -1
            self.play(*[Rotate(f, angle=.05 * sgn * (1 if i % 2 else -1), about_point=f.get_bottom())
                        for i, f in enumerate(fracs)], run_time=.7, rate_func=there_and_back)
        self.finish()


class S04Markers(FilmScene):
    def construct(self):
        fracs, labs = build_row()
        npure = T("no fraction assumed pure", 34, TEXT, weight=BOLD).move_to([-.5, -2.75, 0])
        tag = T("schematic", 28, GREY).move_to([5.3, -3.45, 0])
        self.add(*fracs, labs, npure, tag)
        small = small_tubes()
        ax = axes_parts()
        tg = T("practice numbers from the lesson", 28, GREY).move_to([0, 3.5, 0])
        tubes_big = [f[0] for f in fracs]
        anims = []
        for i in range(4):
            anims.append(Transform(tubes_big[i], small[i][0]))
            for it in fracs[i][1:]:
                anims.append(FadeOut(it))
            anims.append(labs[i].animate.move_to([CH_X[i], -2.95, 0]))
        self.play(FadeOut(npure), FadeOut(tag), *anims, run_time=1.6)
        self.at("measure markers")
        self.play(Create(ax[0]), Create(ax[1]), FadeIn(ax[2:]), run_time=1.1)
        self.at("proteins whose home")
        self.play(FadeIn(tg), run_time=.6)
        self.at("already known")
        self.play(LaggedStart(*[Indicate(t, color=TEXT) for t in tubes_big], lag_ratio=.25), run_time=1.4)
        bars, lines, leg = [], [], []
        starts = [5.8, 9.1, 12.3]
        names = ["histone h3", "cathepsin d", "pyruvate kinase"]
        for j in range(3):
            t0 = starts[j]
            rest = t0 - self.elapsed()
            if rest > 0:
                self.wait(rest)
            g = VGroup(*[bar(j, i) for i in range(4)])
            lr = legend_row(j)
            lr.move_to(legend_group()[j].get_center())
            self.play(*[GrowFromEdge(b, DOWN) for b in g], FadeIn(lr), run_time=1.2)
            ln = poly(line_pts(MARKS[j][2], j), MARKS[j][1], 4)
            self.play(Create(ln), run_time=.6)
            self.at(names[j]) if False else None
            self.play(ShowPassingFlash(ln.copy().set_stroke(width=9), time_width=.6), Indicate(lr, color=MARKS[j][1]),
                      run_time=.8)
            bars.append(g)
            lines.append(ln)
            leg.append(lr)
        self.at("each marker spreads")
        self.play(LaggedStart(*[Indicate(ln, color=MARKS[j][1], scale_factor=1.04) for j, ln in enumerate(lines)],
                              lag_ratio=.5), run_time=2.4)
        self.play(*[b.animate.set_opacity(.55) for b in bars], *[ln.animate.set_opacity(.75) for ln in lines],
                  run_time=.8)
        self.finish()


class S05Rule(FilmScene):
    def construct(self):
        d = chart(dim=True)
        tag = T("schematic", 28, GREY).move_to([5.3, 3.5, 0])
        self.add(d["axes"], d["tubes"], *d["bars"], *d["lines"], d["legend"], tag)
        unk_lab = VGroup(Line([-6.1, 3.55, 0], [-5.55, 3.55, 0], color=MAGENTA, stroke_width=6),
                         T("unknown", 28, MAGENTA).move_to([-4.65, 3.55, 0]))
        shift0 = UP * 1.8
        unk = poly([np.array(p) + shift0 for p in line_pts(UNK, 0)], MAGENTA, 6)
        self.play(FadeIn(unk, shift=DOWN * .4), FadeIn(unk_lab), run_time=1.2)
        self.play(unk.animate.shift(DOWN * .3), run_time=1.0, rate_func=there_and_back)
        self.at("an unknown")
        order = [1, 2, 0]
        starts = ["an unknown", "provisionally", "full profile"]
        gap = None
        for k, j in enumerate(order):
            if k:
                self.at(starts[k])
            pts_m = line_pts(MARKS[j][2], j)
            pts_u = line_pts(UNK, j)
            tgt = poly(pts_u, MAGENTA, 6)
            self.play(Transform(unk, tgt), run_time=.6)
            gp = Polygon(*[np.array(p) for p in pts_m], *[np.array(p) for p in reversed(pts_u)], stroke_width=0,
                         fill_color=GREY, fill_opacity=.55 if j else .15)
            self.play(FadeIn(gp), run_time=.3)
            if j == 0:
                break
            self.wait(.15)
            self.play(FadeOut(gp), run_time=.2)
            if k == 1:
                rule = T("compare full profiles", 34, TEXT, weight=BOLD).move_to([0, 3.5, 0])
                self.play(FadeIn(rule, shift=DOWN * .15), run_time=.5)
        self.at("most closely")
        edge = poly(line_pts(UNK, 0), LAVENDER, 12).set_opacity(.8)
        self.add(edge)
        self.bring_to_front(unk)
        pn = T("provisional: nuclear", 32, TEXT, weight=BOLD).move_to([4.35, 2.7, 0])
        ar = arrow([2.15, 2.7, 0], [1.4, 2.75, 0], TEXT, 5)
        self.play(FadeIn(edge), FadeIn(pn, shift=LEFT * .2), GrowArrow(ar), d["lines"][0].animate.set_opacity(1), run_time=.9)
        self.play(Indicate(pn, color=MAGENTA), run_time=.9)
        self.finish()


def wall_tiles():
    rng = np.random.default_rng(6)
    cols, rows = 17, 9
    xs = np.linspace(-6.2, 6.2, cols)
    ys = np.linspace(-3.3, 1.65, rows)
    shapes = {"early": [.9, .3, .15, .1], "mid": [.15, .7, .9, .3], "late": [.1, .15, .3, .9],
              "mid2": [.2, .8, .4, .2]}
    cols_ = [PROTON, TEAL, BLUE, GREEN]
    tiles = VGroup()
    for y in ys:
        for x in xs:
            r = rng.uniform()
            if r < .18:
                v, c, o = shapes["early"], TEXT, .35
            elif r < .36:
                v, c, o = shapes["late"], TEXT, .35
            elif r < .9:
                kind = rng.choice(["mid", "mid2"])
                v, c, o = shapes[kind], cols_[rng.integers(0, 4)], .6
            else:
                v, c, o = list(rng.uniform(.2, .6, 4)), GREY, .55
            v = np.clip(np.array(v) + rng.normal(0, .08, 4), .05, 1)
            pts = [[x - .24 + .16 * i, y - .14 + .3 * v[i], 0] for i in range(4)]
            tiles.add(poly(pts, c, 4).set_opacity(o))
    return tiles


class S06Scale(FilmScene):
    def construct(self):
        d = chart(dim=True)
        allc = chart_all(d)
        tag = T("schematic", 28, GREY).move_to([5.3, -3.5, 0])
        self.add(allc)
        tiles = wall_tiles()
        bgp = RoundedRectangle(width=2.3, height=1.5, corner_radius=.15, stroke_color=GREY, stroke_width=2,
                               fill_color=BG, fill_opacity=1).move_to([-5.45, 3.0, 0])
        self.play(allc.animate.scale(.18).move_to([-5.45, 3.0, 0]), FadeIn(bgp), run_time=1.2)
        self.bring_to_front(allc)
        self.at("with mass spectrometry")
        order = list(range(len(tiles)))
        np.random.default_rng(9).shuffle(order)
        self.play(LaggedStart(*[FadeIn(tiles[k], scale=.6) for k in order], lag_ratio=.012), run_time=2.9)
        self.at("reported localization")
        val = ValueTracker(0)
        cnt = always_redraw(lambda: M(f"{int(val.get_value()):,}", 44, TEXT, weight=BOLD).move_to([-1.9, 3.2, 0]))
        hl = T("HeLa proteins", 36, TEXT).move_to([1.6, 3.2, 0])
        panel = RoundedRectangle(width=8.4, height=1.45, corner_radius=.15, stroke_width=0, fill_color=BG,
                                 fill_opacity=.9).move_to([-.5, 3.05, 0])
        self.add(panel, cnt)
        self.bring_to_front(allc)
        self.play(FadeIn(hl), val.animate.set_value(8710), run_time=3.8, rate_func=linear)
        lab = T("localization information, 2016", 28, GREY).move_to([-.5, 2.45, 0])
        self.play(FadeIn(lab), run_time=.5)
        self.at("curated markers")
        pick = [tiles[k] for k in (20, 47, 74, 101, 128, 35, 90)]
        mk = T("curated markers", 30, TEXT, weight=BOLD).move_to([5.0, 2.45, 0])
        self.play(FadeIn(mk), LaggedStart(*[Indicate(t, color=TEXT, scale_factor=1.8) for t in pick], lag_ratio=.15),
                  run_time=2.2)
        self.play(FadeOut(mk), run_time=.4)
        self.at("split between")
        mixed = VGroup()
        sel = [tiles[k] for k in (22, 41, 63, 85, 110, 133)]
        tgt = []
        for n, t in enumerate(sel):
            pts = [[0, 0, 0], [.1, .5, 0], [.2, 0, 0], [.3, .55, 0]]
            tgt.append(poly([[4.2 + .65 * (n % 3) + p[0] * 1.4 - .2, 3.35 - .75 * (n // 3) + p[1] * 1.0 - .2, 0]
                             for p in pts], GREY, 5))
        self.play(*[Transform(t, g) for t, g in zip(sel, tgt)], run_time=1.5)
        ml = T("mixed / uncertain", 30, TEXT, weight=BOLD).move_to([4.8, 2.05, 0])
        self.play(FadeIn(ml), FadeIn(tag), run_time=.6)
        self.play(LaggedStart(*[Indicate(t, color=TEXT) for t in sel], lag_ratio=.1), run_time=1.5)
        self.finish()


class S07Confirm(FilmScene):
    def construct(self):
        d = chart(dim=True, legend=False)
        edge = poly(line_pts(UNK, 0), LAVENDER, 12).set_opacity(.8)
        unk = poly(line_pts(UNK, 0), MAGENTA, 6)
        self.add(d["axes"], d["tubes"], *d["bars"], *d["lines"], edge, unk)
        d["lines"][0].set_opacity(1)
        stamp = T("provisional", 40, TEXT, weight=BOLD).rotate(.12).move_to([0, 3.15, 0])
        self.play(FadeIn(stamp, scale=1.5), run_time=.7)
        self.at("a second marker")
        # checklist rows, left-aligned in the free upper-centre area
        rows = VGroup()
        for n, txt in enumerate(["second marker", "repeat fractionation", "imaging check"]):
            bx = Square(.38, color=TEXT, stroke_width=4)
            rows.add(VGroup(bx, T(txt, 30, TEXT)).arrange(RIGHT, buff=.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=.28).move_to([1.0, 1.55, 0])
        for r in rows:
            r.set_opacity(0)

        def tick(r):
            b = r[0]
            c = b.get_center()
            return VGroup(Line(c + [-.14, 0, 0], c + [-.04, -.12, 0], color=GREEN, stroke_width=8),
                          Line(c + [-.04, -.12, 0], c + [.18, .16, 0], color=GREEN, stroke_width=8))
        self.play(FadeIn(rows[0]), run_time=.5)
        rows[0].set_opacity(1)
        second = poly(line_pts([.76, .12, .06, .06], 1), LAVENDER, 5)
        second.shift(UP * 1.6)
        self.play(FadeIn(second), run_time=.3)
        self.play(second.animate.shift(DOWN * 1.6), run_time=.7)
        self.at("agrees")
        t1 = tick(rows[0])
        self.play(Create(t1), run_time=.4)
        self.at("repeated fractionations")
        rows[1].set_opacity(1)
        self.play(FadeIn(rows[1]), *[Indicate(t, color=TEXT) for t in d["tubes"]], run_time=.9)
        self.play(*[b.animate.stretch(1.04, 1, about_edge=DOWN) for g in d["bars"] for b in g], run_time=.4)
        self.play(*[b.animate.stretch(1 / 1.04, 1, about_edge=DOWN) for g in d["bars"] for b in g], run_time=.4)
        t2 = tick(rows[1])
        self.play(Create(t2), run_time=.4)
        self.at("imaging check")
        rows[2].set_opacity(1)
        cellm = Ellipse(width=2.0, height=1.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.13).move_to([5.2, 2.5, 0])
        nuc = Circle(radius=.35, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.1).move_to([5.3, 2.5, 0])
        self.play(FadeIn(rows[2]), FadeIn(cellm), FadeIn(nuc), run_time=.7)
        self.play(nuc.animate.set_color(MAGENTA).set_fill(MAGENTA, .7), run_time=.5)
        self.at("intact cells")
        t3 = tick(rows[2])
        self.play(Create(t3), Indicate(nuc, color=MAGENTA), run_time=.6)
        self.finish()


class S08Latency(FilmScene):
    def construct(self):
        u = make_unit(0, "L", level=.1, ndots=9, seed=2)
        body = u["body"]
        self.play(FadeIn(u["tube"]), run_time=.8)
        self.play(FadeIn(u["ring"]), run_time=.8)
        self.play(FadeIn(u["enz"]), run_time=.8)
        self.at("enclosed by a membrane")
        self.play(Indicate(u["ring"], color=TEXT, scale_factor=1.04), run_time=.9)
        self.at("1951 report")
        lab1 = T("1951: fresh fractions", 32, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        self.add(u["mbox"], u["body"][4], u["body"][5], *u["dots"])
        self.play(FadeIn(lab1), FadeIn(u["mbox"]), FadeIn(u["body"][5]), run_time=.8)
        sch = T("schematic", 28, GREY).move_to([0, -3.55, 0])
        self.play(FadeIn(sch), u["tr"].animate.set_value(.14), run_time=.6)
        self.at("acid phosphatase")
        self.play(Indicate(u["enz"], color=GOLD), run_time=.9)
        self.at("less than expected")
        self.play(u["tr"].animate.set_value(.06), run_time=1.0)
        self.play(u["tr"].animate.set_value(.12), run_time=1.0)
        self.at("more activity")
        u2 = make_unit(2.8, "R", level=.12, ndots=5, seed=5)
        self.play(body.animate.shift(LEFT * 2.8), lab1.animate.shift(LEFT * 2.8), sch.animate.shift(LEFT * 0), run_time=1.0)
        lab2 = T("damaged particles", 32, TEXT, weight=BOLD).move_to([2.8, 3.4, 0])
        self.play(FadeIn(u2["body"]), FadeIn(lab2), run_time=.8)
        self.at("particles were damaged")
        # crack the second container
        ring2 = u2["ring"]
        gap = Arc(radius=1.7, start_angle=-.3, angle=.6, color=BG, stroke_width=14).move_to(ring2.get_center() + RIGHT * 0)
        gap = Arc(radius=1.7, start_angle=-.3, angle=.6, color=BG, stroke_width=16, arc_center=[2.8, CY, 0])
        crack = VGroup(Line([4.35, CY + .4, 0], [4.55, CY + .1, 0], color=TEXT, stroke_width=4),
                       Line([4.55, CY + .1, 0], [4.4, CY - .15, 0], color=TEXT, stroke_width=4),
                       Line([4.4, CY - .15, 0], [4.55, CY - .45, 0], color=TEXT, stroke_width=4))
        self.play(FadeIn(gap), FadeIn(crack), run_time=.5)
        fl = flow_dots(u2, 3, GREEN, True, seed=8)
        for f in fl:
            f.set_opacity(0)
        self.add(*fl)
        self.play(u2["tr"].animate.set_value(.8), run_time=1.6)
        self.finish()


def unit_s09(cx=-2.8, level=.12, seed=2):
    return make_unit(cx, "L", level=level, ndots=9, seed=seed)


class S09Predict(FilmScene):
    def construct(self):
        u = unit_s09()
        self.add(u["body"])
        lab = T("1951: fresh fractions", 32, TEXT, weight=BOLD).move_to([-2.8, 3.4, 0])
        self.add(lab)
        self.wait(.4)
        self.at("picture the enzyme")
        self.play(FadeOut(lab), Indicate(u["enz"], color=GOLD), run_time=1.0)
        self.at("substrate outside")
        self.play(Indicate(u["ring"], color=TEXT, scale_factor=1.04), run_time=1.0)
        self.at("detergent")
        dr = dropper(np.array([-2.4, 3.0, 0]), np.array([-.7, 3.5, 0]))
        dl = T("detergent", 30, DETERGENT, weight=BOLD).move_to([.9, 3.05, 0])
        self.play(FadeIn(dr, shift=DOWN * .3), FadeIn(dl), run_time=.8)
        self.play(Rotate(dr, angle=.12, about_point=dr[2].get_center()), run_time=.8)
        self.at("what happens")
        q = T("Detergent:\nactivity up or down?", 40, TEXT, weight=BOLD, line_spacing=.9).move_to([3.1, -.3, 0])
        qm = T("?", 60, TEXT, weight=BOLD).move_to([-5.8, 2.0, 0])
        up_ = arrow([-5.25, .5, 0], [-5.25, .95, 0], GREY, 5).set_opacity(.6)
        dn_ = arrow([-5.25, -.45, 0], [-5.25, -.9, 0], GREY, 5).set_opacity(.6)
        self.play(FadeIn(q), FadeIn(qm), FadeIn(up_), FadeIn(dn_),
                  u["tr"].animate.set_value(.2), run_time=.8)
        self.play(Indicate(qm, color=TEXT), u["tr"].animate.set_value(.08), run_time=1.0)
        self.finish()


class S10Pause(FilmScene):
    def construct(self):
        u = unit_s09()
        self.add(u["body"])
        dr = dropper(np.array([-2.4, 3.0, 0]), np.array([-.7, 3.5, 0]))
        dr.rotate(.12, about_point=dr[2].get_center())
        dl = T("detergent", 30, DETERGENT, weight=BOLD).move_to([.9, 3.05, 0])
        q = T("Detergent:\nactivity up or down?", 40, TEXT, weight=BOLD, line_spacing=.9).move_to([3.1, -.3, 0])
        qm = T("?", 60, TEXT, weight=BOLD).move_to([-5.8, 2.0, 0])
        up_ = arrow([-5.25, .5, 0], [-5.25, .95, 0], GREY, 5).set_opacity(.6)
        dn_ = arrow([-5.25, -.45, 0], [-5.25, -.9, 0], GREY, 5).set_opacity(.6)
        self.add(dr, dl, q, qm, up_, dn_)
        for _ in range(3):
            self.play(u["tr"].animate.set_value(.18), qm.animate.scale(1.1), run_time=.7)
            self.play(u["tr"].animate.set_value(.08), qm.animate.scale(1 / 1.1), run_time=.7)
        self.finish()


class S11Reveal(FilmScene):
    def construct(self):
        u = unit_s09(level=.1)
        self.add(u["body"])
        dr = dropper(np.array([-2.4, 3.0, 0]), np.array([-.7, 3.5, 0]))
        dr.rotate(.12, about_point=dr[2].get_center())
        dl = T("detergent", 30, DETERGENT, weight=BOLD).move_to([.9, 3.05, 0])
        self.add(dr, dl)
        drop = Dot([-2.4, 2.75, 0], radius=.11, color=DETERGENT)
        self.play(FadeIn(drop), run_time=.2)
        self.play(drop.animate.move_to([-2.8, 1.2, 0]), run_time=.5, rate_func=rush_into)
        self.play(FadeOut(drop), FadeOut(dr), FadeOut(dl), run_time=.3)
        # membrane opens into fragments
        R = 1.7
        c = np.array([-2.8, CY, 0])
        frags = VGroup(*[Arc(radius=R, start_angle=k * TAU / 12 + .05, angle=TAU / 12 - .1, color=GREY,
                            stroke_width=10, arc_center=c) for k in range(12)])
        self.remove(u["ring"])
        self.add(frags)
        lumen = Circle(radius=R, stroke_width=0, fill_color=PROTON, fill_opacity=.08).move_to(c)
        self.add(lumen)
        self.play(*[f.animate.shift(np.array([np.cos(k * TAU / 12 + TAU / 24), np.sin(k * TAU / 12 + TAU / 24), 0]) * .45)
                    .set_opacity(.3) for k, f in enumerate(frags)], FadeOut(lumen), run_time=1.3)
        self.at("the substrate can now reach")
        for d in u["dots"]:
            d.clear_updaters()
        self.play(*[FadeOut(d) for d in u["dots"]], run_time=.3)
        sub = flow_dots(u, 8, GREEN, True, seed=4)
        prod = flow_dots(u, 6, YELLOW, False, seed=12)
        self.add(*sub, *prod)
        self.play(u["tr"].animate.set_value(.85), run_time=2.2)
        self.at("activity hidden")
        sealed = tube(2.0, -1.0, .9, 1.2)
        opened = tube(4.1, -1.0, .9, 1.2)
        ringm = Circle(radius=.3, color=GREY, stroke_width=5).move_to([2.0, -1.0, 0])
        arcs = VGroup(*[Arc(radius=.3, start_angle=k * TAU / 6 + .15, angle=TAU / 6 - .3, color=GREY, stroke_width=4,
                            arc_center=[4.1, -1.0, 0]).shift(np.array([np.cos(k), np.sin(k), 0]) * .08) for k in range(6)])
        ms = VGroup(Rectangle(width=.25, height=.9, color=GREY, stroke_width=3).move_to([2.75, -1.0, 0]),
                    Rectangle(width=.18, height=.12, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([2.75, -1.39, 0]),
                    Rectangle(width=.25, height=.9, color=GREY, stroke_width=3).move_to([4.85, -1.0, 0]),
                    Rectangle(width=.18, height=.75, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([4.85, -1.07, 0]))
        sl = T("sealed", 28, TEXT).move_to([2.35, -2.2, 0])
        ol = T("opened", 28, TEXT).move_to([4.45, -2.2, 0])
        mini = VGroup(sealed, opened, ringm, arcs, ms, sl, ol)
        mini.scale(1.5).move_to([3.3, -.9, 0])
        self.play(FadeIn(mini), run_time=.9)
        self.at("latency")
        lat = T("latency = membrane-hidden activity", 34, TEXT, weight=BOLD).move_to([1.9, 3.35, 0])
        self.play(FadeIn(lat, shift=DOWN * .15), run_time=.7)
        self.play(Indicate(lat, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


class S11bProduct(FilmScene):
    def construct(self):
        u = unit_s09(level=.85)
        for d in u["dots"]:
            d.clear_updaters()
            d.set_opacity(0)
        self.remove(u["ring"])
        self.add(u["body"])
        c = np.array([-2.8, CY, 0])
        frags = VGroup(*[Arc(radius=1.7, start_angle=k * TAU / 12 + .05, angle=TAU / 12 - .1, color=GREY,
                            stroke_width=10, arc_center=c).shift(np.array([np.cos(k * TAU / 12 + TAU / 24),
                                                                           np.sin(k * TAU / 12 + TAU / 24), 0]) * .45)
                         .set_opacity(.3) for k in range(12)])
        self.add(frags)
        self.remove(u["ring"])
        sub = flow_dots(u, 8, GREEN, True, seed=4)
        prod = flow_dots(u, 6, YELLOW, False, seed=12)
        self.add(*sub, *prod)
        sealed = tube(2.0, -1.0, .9, 1.2)
        opened = tube(4.1, -1.0, .9, 1.2)
        ringm = Circle(radius=.3, color=GREY, stroke_width=5).move_to([2.0, -1.0, 0])
        arcs = VGroup(*[Arc(radius=.3, start_angle=k * TAU / 6 + .15, angle=TAU / 6 - .3, color=GREY, stroke_width=4,
                            arc_center=[4.1, -1.0, 0]).shift(np.array([np.cos(k), np.sin(k), 0]) * .08) for k in range(6)])
        ms = VGroup(Rectangle(width=.25, height=.9, color=GREY, stroke_width=3).move_to([2.75, -1.0, 0]),
                    Rectangle(width=.18, height=.12, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([2.75, -1.39, 0]),
                    Rectangle(width=.25, height=.9, color=GREY, stroke_width=3).move_to([4.85, -1.0, 0]),
                    Rectangle(width=.18, height=.75, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([4.85, -1.07, 0]))
        sl = T("sealed", 28, TEXT).move_to([2.35, -2.2, 0])
        ol = T("opened", 28, TEXT).move_to([4.45, -2.2, 0])
        lat = T("latency = membrane-hidden activity", 34, TEXT, weight=BOLD).move_to([1.9, 3.35, 0])
        sch = T("schematic", 28, GREY).move_to([3.5, -3.4, 0])
        mini = VGroup(sealed, opened, ringm, arcs, ms, sl, ol)
        mini.scale(1.5).move_to([3.3, -.9, 0])
        self.add(mini, lat, sch)
        for _ in range(2):
            self.play(u["tr"].animate.set_value(.78), run_time=.7)
            self.play(u["tr"].animate.set_value(.88), run_time=.8)
        self.finish()


class S12Lysosome(FilmScene):
    def construct(self):
        # opened tube shrinks back into the fraction rack
        d = chart(dim=True, legend=False)
        for b in d["bars"]:
            b.set_opacity(0)
        for ln in d["lines"]:
            ln.set_opacity(0)
        c = np.array([-2.8, CY, 0])
        tb = tube(-2.8, CY, 4.4, 5.6, .85)
        self.add(tb)
        tg = T("fractions", 28, TEXT)
        self.play(tb.animate.scale(.22).move_to([0, -2.95, 0]).set_opacity(0), FadeIn(d["tubes"], shift=DOWN * .3), run_time=1.3)
        self.play(Create(d["axes"][0]), run_time=.6)
        vals = [[.05, .22, .55, .18], [.04, .25, .5, .21], [.08, .18, .52, .22]]
        gl = []
        for n, v in enumerate(vals):
            ln = poly([[CH_X[i], Y0 + HS * v[i] + .0, 0] for i in range(4)], GOLD, 5).set_opacity(.9 - .15 * n)
            gl.append(ln)
        hid = T("hidden enzymes peak together", 32, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.play(LaggedStart(*[Create(g) for g in gl], lag_ratio=.4), FadeIn(hid), run_time=2.0)
        self.at("propose the lysosome")
        blk = Circle(radius=.6, color=GOLD, stroke_width=6, fill_color=PROTON, fill_opacity=.3).move_to([0, 0, 0])
        self.play(*[Transform(g, blk.copy()) for g in gl], FadeOut(hid), FadeOut(d["axes"]),
                  run_time=1.0)
        self.remove(*gl)
        self.add(blk)
        world = cell_world(())
        world.remove(world[1])
        lyso_target = np.array([1.45, 1.45, 0])
        small_tubes_g = d["tubes"]
        self.play(FadeIn(world), small_tubes_g.animate.scale(.5).move_to([-4.3, -.8, 0]),
                  blk.animate.scale(.68 / .6).move_to(lyso_target), run_time=1.5)
        lab = T("lysosome proposed, 1955", 32, TEXT, weight=BOLD).move_to([2.55, 3.45, 0])
        self.play(FadeIn(lab, shift=DOWN * .15), run_time=.6)
        self.at("1974 nobel prize")
        y74 = M("1974", 56, TEXT, weight=BOLD).move_to([-4.3, 1.7, 0])
        nb = T("Nobel Prize", 34, TEXT).move_to([-4.3, .8, 0])
        self.play(FadeIn(y74, shift=UP * .2), FadeIn(nb), run_time=.8)
        self.play(Indicate(y74, color=TEXT), run_time=1.0)
        self.finish()


class S13Return(FilmScene):
    def construct(self):
        l = ladder()
        world = cell_world(("lysosome", "nucleus", "mitochondrion"))
        lm = marker(4.7, "lysosome", PROTON)
        pump_in = arrow([.1, 1.45, 0], [.72, 1.45, 0], GOLD, 7)
        pump_out = arrow([4.5, -1.7, 0], [4.5, -1.05, 0], GOLD, 7)
        for k, dd in enumerate(world[7]):
            drift(dd, .12, .8, k)
        tile = RoundedRectangle(width=2.3, height=1.5, corner_radius=.15, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=.1).move_to([-2.6, .3, 0])
        mini = VGroup(*[poly([[-2.6 - .9 + .6 * i, -.15 + .8 * v, 0] for i, v in enumerate(vals)], col, 4)
                        for vals, col in (([.8, .1, .05, .05], LAVENDER), ([.05, .2, .6, .15], PROTON),
                                          ([.05, .05, .1, .8], TEXT))])
        rule = T("Whole profile,\nthen confirm", 28, TEXT, weight=BOLD, line_spacing=.9).move_to([-2.6, -.98, 0])
        tg = T("schematic", 28, GREY).move_to([-1.95, -1.98, 0])
        st = star([-.15, 2.8, 0])
        qm = T("?", 40, MAGENTA, weight=BOLD).move_to([-.75, 2.8, 0])
        self.play(FadeIn(world), FadeIn(l), FadeIn(lm), FadeIn(pump_in), FadeIn(pump_out), FadeIn(st), FadeIn(qm),
                  FadeIn(tile), FadeIn(mini), run_time=.8)
        drift(st, .1, 1.2, 1)
        self.at("the wall")
        self.play(Indicate(world[1], color=PROTON, scale_factor=1.15), run_time=1.0)
        self.at("place the protein first")
        self.play(FadeIn(rule), FadeIn(tg), run_time=.7)
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.05) for m in mini], lag_ratio=.3), run_time=1.5)
        self.play(Indicate(world[1], color=PROTON, scale_factor=1.12), Indicate(st, color=MAGENTA), run_time=1.5)
        self.at("then ask what")
        self.play(Indicate(pump_in, color=GOLD), Indicate(pump_out, color=GOLD), run_time=1.0)
        self.at("chemistry does")
        hook = T("Which compartment holds it?", 32, TEXT, weight=BOLD).move_to([2.55, 3.5, 0]).set_opacity(.55)
        self.play(Indicate(lm, color=PROTON, scale_factor=1.3), FadeIn(hook), run_time=1.2)
        self.play(FadeOut(hook), run_time=1.2)
        self.finish()


class S14End(EndCard):
    LINE = "Place a protein by its whole profile, then confirm it."
