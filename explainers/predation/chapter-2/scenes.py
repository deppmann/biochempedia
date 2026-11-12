"""Fifteen to Eight: Paine's sea-star removal and the keystone idea (Biochemistrypedia explainer, film 2 of Predation).

Timed to the SPOKEN words: every self.at cue uses audio/words.json.

COLOUR MAP (same as film 1, whole film)
  TEAL   = prey: here the mussels (the dominant prey / competitor), ledger, mussel tiles
  ORANGE = predators: Pisaster the sea star, its arrows, the predator ledger
  GREY   = other species (acorn and gooseneck barnacles, algae, chitons, limpets, snails: distinct grey
           neutral tiles), frames, the competitor ledger
  TEXT   = labels                GOLD = highlight (glowing grid edge, pin, countdown)
Rock-tile grids are SCHEMATIC; only the counts 15 and 8 are from Paine's 1966 paper.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BARE = "#2B313D"
KCOL = {"M": TEAL, "A": "#8B93A1", "G": "#C4C9D2", "E": "#5E6878", "C": "#A89A8C", "L": "#CFC5AE", "S": "#9C94AE", ".": BARE}

# ---------------------------------------------------------------- schematic tile patterns
BIG = ["MACLSEMG", "EMGSACLM", "LCMEGMSA", "SALMCGEM", "MEGACLSG", "CMSGMALE"]          # 8 x 6, the whole shore
MIX = ["MACLSM", "EMGSAC", "LCMEGM", "SALMCG", "MEGALS"]                                  # 6 x 5, a patch
FIN = ["MMMMGM", "MMMGMM", "AMMMMM", "MMGAMM", "MMMMAM"]                                  # removal patch, years on
ALLM = ["MMMMMM", "MMMMMM", "MMMGMM", "MMMMMM", "MMMMGM"]                                 # mussels took the rock
CHI = ["MACLSC", "EMGSAC", "LGMEMC", "SALMGC", "MEGALM"]                                  # chitons still present
ALGAE = [(0, 1), (1, 0), (2, 2), (3, 4), (4, 1), (1, 5)]                                  # algae tiles in the replay

CELL = 0.82
GXC, GXR, GY = -3.45, 3.45, -0.3          # control and removal grids, one place the whole film


class Grid:
    def __init__(self, cx, cy, pattern, cell=CELL):
        self.rows, self.cols, self.cell, self.cx, self.cy = len(pattern), len(pattern[0]), cell, cx, cy
        self.tiles = {}
        for r, row in enumerate(pattern):
            for c, k in enumerate(row):
                t = Square(cell * 0.9, stroke_width=0, fill_color=KCOL[k], fill_opacity=0.95).move_to(self.pos(r, c))
                t.kind = k
                self.tiles[(r, c)] = t
        self.g = VGroup(*self.tiles.values())

    def pos(self, r, c):
        return np.array([self.cx + (c - (self.cols - 1) / 2) * self.cell, self.cy - (r - (self.rows - 1) / 2) * self.cell, 0.0])

    def ctr(self, r, c):
        return self.tiles[(r, c)].get_center()

    def set(self, r, c, k):
        t = self.tiles[(r, c)]
        t.kind = k
        return t.animate.set_fill(KCOL[k], 0.95)

    def find(self, k):
        return [rc for rc, t in self.tiles.items() if t.kind == k]

    def frame(self, color=GOLD, w=6, pad=0.1):
        return Rectangle(width=self.g.width + pad, height=self.g.height + pad, stroke_color=color, stroke_width=w, fill_opacity=0).move_to(self.g)


def shimmer(grid):
    """Slow ambient motion for a held grid: the tiles' brightness drifts."""
    grid._t = 0.0

    def upd(m, dt):
        grid._t += dt
        for i, t in enumerate(m.submobjects):
            t.set_fill(opacity=0.86 + 0.09 * np.sin(1.4 * grid._t + i * 0.9))
    grid.g.add_updater(upd)


def still(grid):
    grid.g.clear_updaters()
    for t in grid.g.submobjects:
        t.set_fill(opacity=0.95)


def pulse_on(m, amp=0.10, speed=3.4, phase=0.0):
    m._ph, m._f = 0.0, 1.0

    def u(mm, dt):
        mm._ph += dt
        f = 1 + amp * np.sin(speed * mm._ph + phase)
        mm.scale(f / mm._f)
        mm._f = f
    m.add_updater(u)


def pulse_off(m):
    m.clear_updaters()
    if hasattr(m, "_f"):
        m.scale(1 / m._f)
        m._f = 1.0


def sea_star(r=0.55):
    s = Star(n=5, outer_radius=r, inner_radius=r * 0.5, color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.97)
    dots = VGroup(*[Dot(s.get_center() + 0.52 * r * np.array([np.cos(PI / 2 + k * TAU / 5), np.sin(PI / 2 + k * TAU / 5), 0]), radius=0.04, color="#FFE0B8") for k in range(5)])
    core = Circle(radius=r * 0.2, stroke_width=0, fill_color="#FFD7A8", fill_opacity=0.7)
    m = VGroup(s, core, dots)
    m.set_z_index(4)
    return m


def hand():
    skin = "#D9B8A0"
    palm = RoundedRectangle(corner_radius=0.12, width=0.62, height=0.55, stroke_width=0, fill_color=skin, fill_opacity=1)
    fingers = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.12, height=0.42, stroke_width=0, fill_color=skin, fill_opacity=1)
                       .move_to([-0.24 + 0.16 * i, -0.45, 0]) for i in range(4)])
    thumb = RoundedRectangle(corner_radius=0.06, width=0.13, height=0.36, stroke_width=0, fill_color=skin, fill_opacity=1).rotate(0.9).move_to([0.38, -0.14, 0])
    wrist = Rectangle(width=0.42, height=1.5, stroke_width=0, fill_color=skin, fill_opacity=1).move_to([0, 1.0, 0])
    h = VGroup(wrist, palm, fingers, thumb)
    h.shift(-h.get_bottom())
    h.set_z_index(8)
    return h


def hand_to(h, p):
    return h.animate.shift(np.array([p[0], p[1], 0.0]) - h.get_bottom())


def waves(tr, y=3.35):
    def mk(off, col, op):
        def f():
            xs = np.linspace(-6.9, 6.9, 60)
            pts = [np.array([x, y + 0.14 * np.sin(1.1 * x + 1.6 * tr.get_value() + off), 0.0]) for x in xs]
            m = VMobject().set_points_as_corners(pts)
            m.set_stroke(col, 5, opacity=op)
            m.set_fill(opacity=0)
            return m
        return always_redraw(f)
    return VGroup(mk(0.0, GREY, 0.55), mk(2.1, GREY, 0.3))


def badge(sign, color, at, r=0.3, size=44):
    c = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=1)
    t = T(sign, size, color, weight=BOLD)
    return VGroup(c, t.move_to(c)).move_to(at).set_z_index(6)


def swatch_row(kind, text, x, y, size=30, col=None):
    sw = Square(0.34, stroke_width=0, fill_color=KCOL[kind], fill_opacity=0.95).move_to([x, y, 0])
    tx = T(text, size, col or TEXT).next_to(sw, RIGHT, buff=0.22)
    return VGroup(sw, tx)


class Ledger:
    """The film-1 ledger (same drawing), here without a gauge."""

    def __init__(self, color, name, cx, cy=0.3, w=3.5, h=4.3, tsize=28):
        self.color, self.cx, self.cy, self.w, self.h = color, cx, cy, w, h
        top = cy + h / 2
        self.top = top
        box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22).move_to([cx, cy, 0])
        div = Line([cx, top - 0.75, 0], [cx, cy - h / 2 + 0.2, 0], color=color, stroke_width=2).set_opacity(0.6)
        rule = Line([cx - w / 2 + 0.15, top - 0.72, 0], [cx + w / 2 - 0.15, top - 0.72, 0], color=color, stroke_width=2).set_opacity(0.6)
        self.title = T(name, tsize, color, weight=BOLD).move_to([cx, top - 0.38, 0])
        self.h_b = T("births", 26, TEXT).move_to([cx - w / 4, top - 1.05, 0])
        self.h_d = T("deaths", 26, TEXT).move_to([cx + w / 4, top - 1.05, 0])
        self.base = VGroup(box, div, rule, self.title, self.h_b, self.h_d)
        self.entries = []

    def slot(self, kind, i):
        x = self.cx - self.w / 4 if kind == "b" else self.cx + self.w / 4
        return np.array([x, self.top - 1.7 - 0.5 * i, 0.0])

    def fill_static(self, nb, nd):
        for i in range(nb):
            self.entries.append(T("+", 44, self.color, weight=BOLD).move_to(self.slot("b", i)))
        for i in range(nd):
            self.entries.append(T("−", 44, self.color, weight=BOLD).move_to(self.slot("d", i)))

    def mobs(self):
        return VGroup(self.base, *self.entries)


def chain(x1, x2, y, c1, c2, n=5):
    links = VGroup()
    for i in range(n):
        f = i / (n - 1)
        col = interpolate_color(ManimColor(c1), ManimColor(c2), f)
        m = Ellipse(width=0.56 if i % 2 == 0 else 0.3, height=0.3, stroke_color=col, stroke_width=5)
        links.add(m.move_to([x1 + (x2 - x1) * f, y, 0]))
    return links


class Base(SpokenScene):
    def clock(self, rate=1.0):
        tr = ValueTracker(0.0)
        tr.add_updater(lambda m, dt: m.increment_value(dt * rate))
        self.add(tr)
        return tr


def headers(ctrl=True, rem=True):
    g = VGroup()
    if ctrl:
        g.add(T("adjacent control", 30, TEXT, weight=BOLD).move_to([GXC, 2.75, 0]))
    if rem:
        g.add(T("removal patch", 30, TEXT, weight=BOLD).move_to([GXR, 2.75, 0]))
    return g


def counter(tr, x=GXR, y=-2.7, size=30):
    return always_redraw(lambda: T(f"species on the rock: {int(round(tr.get_value()))}", size, TEXT).move_to([x, y, 0]))


def updown_tags():
    up = VGroup(Triangle(stroke_width=0, fill_color=GOLD, fill_opacity=1).scale(0.18).move_to([1.85, 2.23, 0]),
                T("up?", 34, TEXT, weight=BOLD).move_to([2.65, 2.2, 0]))
    dn = VGroup(Triangle(stroke_width=0, fill_color=GOLD, fill_opacity=1).scale(0.18).rotate(PI).move_to([3.95, 2.17, 0]),
                T("down?", 34, TEXT, weight=BOLD).move_to([4.95, 2.2, 0]))
    return up, dn


# ============================================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Predation and Community Effects"
    TITLE = "Fifteen to Eight"


# --------------------------------------------------------------- 1: the third ledger
XO, XT, XG, LCY = -4.6, 0.0, 4.6, 0.55


def ledgers3():
    Lo = Ledger(ORANGE, "predator ledger", XO, LCY)
    Lt = Ledger(TEAL, "prey ledger", XT, LCY)
    Lg = Ledger(GREY, "competitors", XG, LCY)
    Lo.fill_static(2, 2)
    Lt.fill_static(3, 2)
    Lg.fill_static(2, 1)
    return Lo, Lt, Lg


class S01Link(Base):
    def construct(self):
        Lo, Lt, Lg = ledgers3()
        self.play(FadeIn(Lo.mobs(), shift=RIGHT * 0.3), FadeIn(Lt.mobs(), shift=LEFT * 0.3), run_time=1.3)
        ch = chain(XO + 1.95, XT - 1.95, LCY, ORANGE, TEAL, n=4)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in ch], lag_ratio=0.25), run_time=0.9)
        trk = ValueTracker(0.0)
        trk.add_updater(lambda m, dt: m.increment_value(dt * 0.45))
        self.add(trk)
        dot = always_redraw(lambda: Dot([XO + 1.95 + 1.1 * (trk.get_value() % 1.0), LCY, 0], radius=0.12, color=TEXT).set_z_index(7))
        self.add(dot)
        # the dotted arrow from the predator ledger, through the prey ledger, to the third ledger
        yy = -2.35
        line = DashedLine([XO, yy, 0], [XG - 0.15, yy, 0], dash_length=0.16, stroke_width=7, color=TEXT)
        tip = Triangle(stroke_width=0, fill_color=TEXT, fill_opacity=1).scale(0.17).rotate(-PI / 2).move_to([XG, yy, 0])
        ticks = VGroup(*[Line([x, yy, 0], [x, LCY - 2.15, 0], color=c, stroke_width=5) for x, c in [(XO, ORANGE), (XT, TEAL)]])
        self.at("Now follow")
        self.play(Create(ticks[0]), run_time=0.6)
        self.at("kills one link")
        self.play(Create(line), Create(ticks[1]), run_time=1.1, rate_func=linear)
        self.at("to the species")
        self.play(FadeIn(Lg.mobs(), shift=LEFT * 0.4), FadeIn(tip), run_time=1.1)
        lab = T("species the prey\ncompete with", 28, TEXT, line_spacing=1.1).move_to([XG - 0.3, -3.1, 0])
        self.at("compete with")
        self.play(FadeIn(lab, shift=UP * 0.12), run_time=0.7)
        self.finish()


# --------------------------------------------------------------- 2: the question
BIGY = -0.85


class S02Question(Base):
    def construct(self):
        tr = self.clock(1.0)
        wv = waves(tr)
        gr = Grid(0, BIGY, BIG, 0.74)
        star = sea_star(0.62).move_to(gr.pos(2, 4))
        star.add_updater(lambda m, dt: m.rotate(0.25 * dt))
        self.add(wv)
        self.play(FadeIn(gr.g), FadeIn(star, scale=1.4), run_time=1.3)
        shimmer(gr)
        self.at("to do better")
        pulsers = [(0, 0), (1, 1), (2, 2), (3, 3), (5, 1)]
        for rc in pulsers:
            pulse_on(gr.tiles[rc], 0.09, 4.0, rc[0] + rc[1])
        h = hand()
        h.move_to([star.get_x(), 3.6, 0])
        self.add(h)
        self.at("without it", lead=0.5)
        sp = star.get_center()
        self.play(hand_to(h, sp + UP * 0.1), run_time=1.0)
        star.clear_updaters()
        self.play(hand_to(h, np.array([sp[0], 2.55, 0])), star.animate.move_to([sp[0], 2.45, 0]), run_time=1.4)
        self.at("So what happens")
        q = T("?", 150, TEXT, weight=BOLD).move_to([0, BIGY + 0.2, 0]).set_z_index(9)
        for rc in pulsers:
            pulse_off(gr.tiles[rc])
        self.play(FadeIn(q, scale=0.3), run_time=1.2)
        self.at("gone?")
        self.play(FadeOut(h, shift=UP * 0.6), FadeOut(star, shift=UP * 0.4), run_time=1.2)
        self.finish()


# --------------------------------------------------------------- 3: space is the limiting resource
class S03Space(Base):
    def construct(self):
        tr = self.clock(1.0)
        wv = waves(tr)
        gr = Grid(0, BIGY, BIG, 0.74)
        self.add(wv, gr.g)
        shimmer(gr)
        self.wait(1.3)
        self.at("space on the rock")
        fr = gr.frame(GOLD, 6, 0.14)
        self.play(Create(fr), run_time=1.0)
        fr._ph = 0.0

        def glow(m, dt):
            m._ph += dt
            m.set_stroke(GOLD, 6 + 4 * np.sin(2.6 * m._ph))
        fr.add_updater(glow)
        lab1 = T("limiting resource: space on the rock", 32, GOLD, weight=BOLD).move_to([0, 2.0, 0])
        self.at("limiting resource")
        self.play(FadeIn(lab1, shift=DOWN * 0.15), run_time=0.8)
        self.at("supply caps")
        self.play(Indicate(fr, color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("Muscles are")
        self.play(FadeOut(lab1), run_time=0.4)
        for rc in gr.find("M"):
            pulse_on(gr.tiles[rc], 0.11, 3.6, rc[0] * 2 + rc[1])
        lab2 = T("strongest competitors for space", 32, TEAL, weight=BOLD).move_to([0, 2.0, 0])
        self.play(FadeIn(lab2, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


# --------------------------------------------------------------- 4: the sea star and its prey
class S04Star(Base):
    def construct(self):
        tr = self.clock(1.0)
        wv = waves(tr)
        gr = Grid(0, BIGY, BIG, 0.74)
        self.add(wv, gr.g)
        shimmer(gr)
        base = np.array([0.7, 2.45, 0.0])
        star = sea_star(0.6).move_to(base)
        star.add_updater(lambda m, dt: m.move_to(base + np.array([0.45 * np.sin(0.8 * tr.get_value()), 0.12 * np.sin(1.3 * tr.get_value()), 0])))
        self.play(gr.g.animate.shift(LEFT * 2.35), FadeIn(star, scale=1.5), run_time=1.0)
        name = T("Pisaster ochraceus", 32, ORANGE, slant=ITALIC, weight=BOLD).move_to([3.9, 2.45, 0])
        self.add(star)
        self.at("pisaster")
        self.play(FadeIn(name, shift=LEFT * 0.15), run_time=0.8)
        used = []

        def pick(kind):
            cands = [rc for rc in gr.find(kind) if rc not in used]
            cands.sort(key=lambda rc: np.linalg.norm(gr.ctr(*rc) - base))
            rc = cands[0]
            used.append(rc)
            return rc

        rows = [("M", "mussels", "eats mussels"), ("A", "barnacles", "barnacles"), ("C", "chitons", "chitins"),
                ("L", "limpets", "limpets"), ("S", "snails", "snails")]
        arrows = []
        for i, (k, nm, cue) in enumerate(rows):
            rc = pick(k)
            tgt = gr.tiles[rc]
            a = always_redraw(lambda tgt=tgt: Arrow(star.get_center(), tgt.get_center(), buff=0.42, color=ORANGE, stroke_width=6, tip_length=0.24, max_tip_length_to_length_ratio=0.5))
            arrows.append(tgt)
            row = swatch_row(k, nm, 3.5, 1.35 - 0.95 * i, 32)
            self.at(cue)
            ring = Square(CELL * 0.98, stroke_color=ORANGE, stroke_width=6, fill_opacity=0).move_to(tgt)
            self.play(Create(a), FadeIn(ring), FadeIn(row, shift=LEFT * 0.2), run_time=0.7)
            self.add(ring)
            ring.add_updater(lambda m, dt, tgt=tgt: m.move_to(tgt))
        self.at("Follow the")
        clk = self.clock(0.5)
        dots = VGroup()
        for j, tgt in enumerate(arrows):
            d = always_redraw(lambda j=j, tgt=tgt: Dot(star.get_center() + (tgt.get_center() - star.get_center()) * ((clk.get_value() + 0.2 * j) % 1.0), radius=0.1, color="#FFE0B8").set_z_index(7))
            dots.add(d)
        self.add(dots)
        self.wait(0.5)
        self.finish()


# --------------------------------------------------------------- 5: Paine's design
def two_grids(ctrl_pat=MIX, rem_pat=MIX):
    return Grid(GXC, GY, ctrl_pat), Grid(GXR, GY, rem_pat)


STAR_RC = [(1, 2), (3, 4)]


def pin_label():
    pin = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([0, 0.18, 0]),
                 Triangle(stroke_width=0, fill_color=GOLD, fill_opacity=1).scale(0.16).rotate(PI).move_to([0, -0.08, 0]),
                 Dot([0, 0.18, 0], radius=0.07, color=BG))
    t = T("Mukkaw Bay, Washington", 34, TEXT, weight=BOLD)
    g = VGroup(pin, t.next_to(pin, RIGHT, buff=0.25)).move_to([0, 3.45, 0])
    return g


class S05Design(Base):
    def construct(self):
        gc, gr = two_grids()
        self.play(FadeIn(gc.g), FadeIn(gr.g), run_time=1.2)
        shimmer(gc)
        shimmer(gr)
        sc = [sea_star(0.34).move_to(gc.ctr(*rc)) for rc in STAR_RC]
        sr = [sea_star(0.34).move_to(gr.ctr(*rc)) for rc in STAR_RC]
        self.at("Robert")
        self.play(*[FadeIn(s, scale=1.8) for s in sc + sr], run_time=0.8)
        for s in sc:
            s.add_updater(lambda m, dt: m.rotate(0.3 * dt))
        h = hand()
        h.move_to([GXR, 3.6, 0])
        self.add(h)
        self.at("keeping")
        for i, s in enumerate(sr):
            self.play(hand_to(h, gr.ctr(*STAR_RC[i]) + UP * 0.05), run_time=0.5)
            self.play(hand_to(h, [GXR + 2.0, 3.3, 0]), s.animate.move_to([GXR + 2.0, 3.2, 0]), run_time=0.6)
            self.remove(s)
        hr = T("removal patch", 30, TEXT, weight=BOLD).move_to([GXR, 2.75, 0])
        self.play(FadeOut(h, shift=UP * 0.4), FadeIn(hr, shift=DOWN * 0.1), run_time=0.5)
        self.at("Muckal")
        pl = pin_label()
        self.play(FadeIn(pl, shift=DOWN * 0.2), run_time=0.9)
        self.at("neighboring")
        hc = T("adjacent control", 30, TEXT, weight=BOLD).move_to([GXC, 2.75, 0])
        self.play(FadeIn(hc, shift=DOWN * 0.1), run_time=0.7)
        self.at("surveyed")
        cnt = ValueTracker(15)
        cn = counter(cnt)
        lines = VGroup()
        for g in (gc, gr):
            for r in (1, 3):
                y = g.ctr(r, 0)[1]
                lines.add(DashedLine([g.cx - 2.45, y, 0], [g.cx + 2.45, y, 0], color=GOLD, dash_length=0.16, stroke_width=5).set_z_index(5))
        self.play(Create(lines), FadeIn(cn), run_time=1.2)
        self.at("transects")
        lt = T("line transects", 30, GOLD, weight=BOLD).move_to([GXC, -2.7, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), run_time=0.7)
        self.finish()


def predict_frame(scene):
    gc, gr = two_grids()
    for s in [sea_star(0.34).move_to(gc.ctr(*rc)) for rc in STAR_RC]:
        s.add_updater(lambda m, dt: m.rotate(0.3 * dt))
        scene.add(s)
    shimmer(gc)
    shimmer(gr)
    hs = headers()
    cnt = ValueTracker(15)
    cn = counter(cnt)
    scene.add(gc.g, gr.g, hs, cn)
    return gc, gr, hs, cnt, cn


class S06Predict(Base):
    def construct(self):
        gc, gr, hs, cnt, cn = predict_frame(self)
        self.at("predator is gone", lead=0.1)
        gh = sea_star(0.5).move_to(gr.ctr(2, 2))
        self.play(FadeIn(gh, scale=1.2), run_time=0.4)
        self.play(gh.animate.shift(UP * 1.6).set_opacity(0.0), run_time=1.4)
        up, dn = updown_tags()
        self.at("Will the number")
        self.play(Indicate(cn, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.at("go up")
        self.play(FadeIn(up, shift=UP * 0.15), run_time=0.7)
        self.at("down")
        self.play(FadeIn(dn, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S07Pause(Base):
    def construct(self):
        gc, gr, hs, cnt, cn = predict_frame(self)
        up, dn = updown_tags()
        self.add(up, dn)
        cap = T("Predict: species on the rock, up or down?", 32, GOLD, weight=BOLD).move_to([0, -3.3, 0])
        bg = Rectangle(width=6.0, height=0.24, stroke_color=GOLD, stroke_width=4).move_to([0, -3.7, 0])
        cd = ValueTracker(1.0)
        bar = always_redraw(lambda: Rectangle(width=max(0.01, 6.0 * cd.get_value()), height=0.24, stroke_width=0, fill_color=GOLD,
                                              fill_opacity=0.9).move_to([-3.0 + max(0.01, 6.0 * cd.get_value()) / 2, -3.7, 0]))
        self.add(cap, bg, bar)
        self.play(cd.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.finish()


# --------------------------------------------------------------- 8: down, fifteen to eight
class S08Reveal(Base):
    def construct(self):
        gc, gr, hs, cnt, cn = predict_frame(self)
        up, dn = updown_tags()
        self.add(up, dn)
        self.at("Down.", lead=0.0)
        self.play(FadeOut(up), Indicate(dn, color=GOLD, scale_factor=1.25), run_time=1.0)
        self.at("By his")
        sch = T("grids schematic; counts from Paine 1966", 26, TEXT).move_to([0, -3.5, 0])
        self.play(FadeOut(dn), FadeIn(sch, shift=UP * 0.1), run_time=0.7)
        self.at("removal patch")
        still(gr)
        rng = random.Random(8)
        order = [rc for rc in gr.tiles if gr.tiles[rc].kind != FIN[rc[0]][rc[1]]]
        rng.shuffle(order)
        anims = [gr.set(r, c, FIN[r][c]) for r, c in order]
        self.play(LaggedStart(*anims, lag_ratio=0.12), cnt.animate.set_value(8), run_time=2.6, rate_func=linear)
        self.at("instead of")
        tag = T("15 → 8, Paine 1966", 38, GOLD, weight=BOLD).move_to([GXR, 2.2, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.8)
        self.at("The control")
        nl = T("no comparable loss", 30, TEXT, weight=BOLD).move_to([GXC, -2.7, 0])
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------- 9: how the patch filled
class S09Fill(Base):
    def construct(self):
        gc, gr = two_grids(MIX, FIN)
        hs = headers()
        self.add(gc.g, gr.g, hs)
        cx, cy, sc = -1.9, -0.2, 1.25
        # the removal patch comes to the middle, bigger, the control steps aside
        self.play(FadeOut(gc.g), FadeOut(hs), gr.g.animate.scale(sc).move_to([cx, cy, 0]), run_time=1.0)
        gr.cx, gr.cy, gr.cell = cx, cy, CELL * sc
        # rewind to open rock with the algae still there
        rng = random.Random(9)
        order = list(gr.tiles)
        rng.shuffle(order)
        anims = [gr.set(r, c, "E" if (r, c) in ALGAE else ".") for r, c in order]
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=1.8)
        tg = T("schematic sequence", 26, TEXT).move_to([cx, -3.5, 0])
        self.add(tg)
        self.at("Acorn barnacles")
        non_algae = [rc for rc in order if rc not in ALGAE]
        r1 = swatch_row("A", "acorn barnacles", 2.55, 1.9, 30)
        r1b = T("within months", 30, TEXT, weight=BOLD).move_to([4.2, 1.25, 0])
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.6)
        self.play(LaggedStart(*[gr.set(r, c, "A") for r, c in non_algae], lag_ratio=0.1), FadeIn(r1b, shift=LEFT * 0.2), run_time=2.6)
        self.at("small mussels")
        r2 = swatch_row("M", "mussels", 2.55, 0.25, 30, TEAL)
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.3)
        m_tiles = [rc for rc in non_algae if FIN[rc[0]][rc[1]] == "M"]
        self.play(LaggedStart(*[gr.set(r, c, "M") for r, c in m_tiles], lag_ratio=0.12), run_time=1.2)
        self.at("gooseneck")
        r3 = swatch_row("G", "gooseneck barnacles", 2.55, -0.55, 28)
        g_tiles = [rc for rc in non_algae if FIN[rc[0]][rc[1]] == "G"]
        self.play(FadeIn(r3, shift=LEFT * 0.2), LaggedStart(*[gr.set(r, c, "G") for r, c in g_tiles], lag_ratio=0.3), run_time=1.4)
        self.at("Algae lost")
        r4 = swatch_row("E", "algae", 2.55, -1.35, 30)
        self.play(FadeIn(r4, shift=LEFT * 0.2), run_time=0.5)
        for _ in range(2):
            self.play(*[gr.tiles[rc].animate.set_fill(opacity=0.2) for rc in ALGAE], run_time=0.25)
            self.play(*[gr.tiles[rc].animate.set_fill(opacity=0.95) for rc in ALGAE], run_time=0.25)
        self.play(LaggedStart(*[gr.set(r, c, FIN[r][c]) for r, c in ALGAE], lag_ratio=0.15), run_time=1.2)
        self.finish()


# --------------------------------------------------------------- 10: why richness rose
class S10Mechanism(Base):
    def construct(self):
        gc = Grid(GXC, GY, MIX)
        gr = Grid(GXR, GY, FIN)
        cx, cy, sc = -1.9, -0.2, 1.25
        gr.g.scale(sc).move_to([cx, cy, 0])
        self.add(gr.g)
        hs = headers()
        self.play(gr.g.animate.scale(1 / sc).move_to([GXR, GY, 0]), FadeIn(gc.g), FadeIn(hs), run_time=1.1)
        star = sea_star(0.34).move_to(gc.ctr(1, 2))
        self.play(FadeIn(star, scale=1.6), run_time=0.4)
        shimmer(gc)
        # first mussel eaten, then a weaker competitor settles in the gap
        self.play(star.animate.move_to(gc.ctr(1, 1)), run_time=0.8)
        self.play(gc.tiles[(1, 1)].animate.set_fill(BARE, 0.95), run_time=0.3)
        self.at("space kept")
        pulse_on(gc.tiles[(1, 1)], 0.12, 4.5)
        self.wait(0.3)
        self.at("weaker")
        pulse_off(gc.tiles[(1, 1)])
        gc.tiles[(1, 1)].kind = "A"
        self.play(gc.tiles[(1, 1)].animate.set_fill(KCOL["A"], 0.95), run_time=0.5)
        self.play(star.animate.move_to(gc.ctr(3, 3)), run_time=0.7)
        self.play(gc.tiles[(3, 3)].animate.set_fill(BARE, 0.95), run_time=0.3)
        pulse_on(gc.tiles[(3, 3)], 0.12, 4.5)
        self.wait(0.2)
        pulse_off(gc.tiles[(3, 3)])
        gc.tiles[(3, 3)].kind = "G"
        self.play(gc.tiles[(3, 3)].animate.set_fill(KCOL["G"], 0.95), run_time=0.5)
        self.at("Without it")
        rng = random.Random(10)
        order = [rc for rc in gr.tiles if gr.tiles[rc].kind != ALLM[rc[0]][rc[1]]]
        rng.shuffle(order)
        self.play(LaggedStart(*[gr.set(r, c, ALLM[r][c]) for r, c in order], lag_ratio=0.2), run_time=2.4)
        self.at("raised richness")
        lab = T("richness = number of species on the rock", 32, GOLD, weight=BOLD).move_to([0, -3.35, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.9)
        self.at("freeing space")
        self.play(Indicate(gc.tiles[(1, 1)], color=GOLD, scale_factor=1.35), Indicate(gc.tiles[(3, 3)], color=GOLD, scale_factor=1.35), run_time=1.2)
        self.finish()


# --------------------------------------------------------------- 11: one chiton, two routes
class S11Chiton(Base):
    def construct(self):
        STAR = np.array([-5.0, -0.2, 0.0])
        CHI_ = np.array([5.0, -0.2, 0.0])
        MUS = np.array([-1.8, 2.0, 0.0])
        CHP = np.array([2.75, 2.0, 0.0])
        chit = Square(2.4, stroke_width=0, fill_color=KCOL["C"], fill_opacity=0.95).move_to([0, 0.2, 0])
        clab = T("chiton", 32, TEXT, weight=BOLD).move_to([0, -1.7, 0])
        self.play(FadeIn(chit, scale=0.4), run_time=1.0)
        self.play(FadeIn(clab, shift=UP * 0.1), run_time=0.6)
        self.play(chit.animate.scale(1.4 / 2.4).move_to(CHI_), clab.animate.move_to(CHI_ + DOWN * 1.2), run_time=1.0)
        star = sea_star(0.62).move_to(STAR)
        star.add_updater(lambda m, dt: m.rotate(0.2 * dt))
        self.at("Pisaster eats")
        self.play(FadeIn(star, scale=1.5), run_time=0.5)
        direct = Arrow(STAR + RIGHT * 0.9, CHI_ + LEFT * 0.95, buff=0, color=ORANGE, stroke_width=8, tip_length=0.3)
        bd = badge("−", ORANGE, [0, -0.2, 0])
        self.play(Create(direct), run_time=0.7)
        self.play(FadeIn(bd, scale=0.4), run_time=0.3)
        dl = T("direct: eaten", 32, ORANGE, weight=BOLD).move_to([0, -0.95, 0])
        self.at("so the sea star")
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.7)
        self.at("costs it")
        self.play(chit.animate.scale(0.8), run_time=0.4)
        self.play(chit.animate.scale(1 / 0.8), run_time=0.4)
        self.at("But the sea star")
        mus = Square(1.3, stroke_width=0, fill_color=TEAL, fill_opacity=0.95).move_to(MUS)
        mlab = T("mussels", 30, TEAL, weight=BOLD).move_to(MUS + DOWN * 1.1)
        self.play(FadeIn(mus, scale=0.5), FadeIn(mlab), run_time=0.8)
        a1 = Arrow(STAR + UP * 0.55 + RIGHT * 0.5, MUS + LEFT * 0.75, buff=0, color=ORANGE, stroke_width=8, tip_length=0.28)
        b1 = badge("−", ORANGE, (a1.get_start() + a1.get_end()) / 2)
        self.at("keeps mussels")
        self.play(Create(a1), run_time=0.8)
        self.play(FadeIn(b1, scale=0.4), run_time=0.3)
        self.at("off the rock")
        self.play(mus.animate.scale(0.55).set_opacity(0.45), run_time=1.0)
        self.at("which keeps")
        _t = T("space and food", 32, TEXT, weight=BOLD)
        chip_ = VGroup(RoundedRectangle(corner_radius=0.14, width=_t.width + 0.5, height=_t.height + 0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25), _t).move_to(CHP)
        a2 = Arrow(MUS + RIGHT * 0.75, CHP + LEFT * 1.65, buff=0, color=TEAL, stroke_width=8, tip_length=0.28)
        b2 = badge("−", TEAL, (a2.get_start() + a2.get_end()) / 2)
        self.play(FadeIn(chip_, scale=0.6), Create(a2), FadeIn(b2, scale=0.4), run_time=0.8)
        self.at("chiton space")
        a3 = Arrow(CHP + DOWN * 0.5 + RIGHT * 0.9, CHI_ + UP * 0.85 + LEFT * 0.2, buff=0, color=GREY, stroke_width=11, tip_length=0.32)
        b3 = badge("+", TEXT, (a3.get_start() + a3.get_end()) / 2)
        self.play(Create(a3), run_time=0.6)
        self.play(FadeIn(b3, scale=0.4), run_time=0.2)
        self.at("food")
        il = T("indirect: space and food freed from mussels", 32, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        self.play(FadeIn(il, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------- 12: two arrows, opposite signs
class S12TwoArrows(Base):
    def construct(self):
        ax, bx, y0 = -5.1, -3.0, -0.6
        a_dir = Arrow([ax, y0, 0], [ax, y0 - 1.3, 0], buff=0, color=ORANGE, stroke_width=14, tip_length=0.36)
        a_ind = Arrow([bx, y0, 0], [bx, y0 + 3.1, 0], buff=0, color=GREY, stroke_width=22, tip_length=0.5)
        s_dir = T("−", 70, ORANGE, weight=BOLD).move_to([ax, y0 + 0.65, 0])
        s_ind = T("+", 70, TEXT, weight=BOLD).move_to([bx, y0 + 3.5, 0])
        l_dir = T("direct", 36, ORANGE, weight=BOLD).move_to([ax, y0 - 1.95, 0])
        l_ind = T("indirect", 36, TEXT, weight=BOLD).move_to([bx, y0 - 0.55, 0])
        self.play(Create(a_dir), Create(a_ind), run_time=1.1)
        self.at("opposite signs", lead=0.5)
        self.play(FadeIn(s_dir, scale=0.4), FadeIn(s_ind, scale=0.4), FadeIn(l_dir), FadeIn(l_ind), run_time=0.9)
        gr = Grid(3.35, 0.0, CHI)
        self.play(FadeIn(gr.g), run_time=1.0)
        shimmer(gr)
        self.at("Without the sea star")
        chs = [(r, 5) for r in range(4)]
        for rc in chs:
            pulse_on(gr.tiles[rc], 0.1, 4.0, rc[0])
        self.at("left the", lead=0.0)
        for rc in chs:
            pulse_off(gr.tiles[rc])
        self.play(LaggedStart(*[gr.tiles[rc].animate.shift(RIGHT * 1.2).set_opacity(0.0) for rc in chs], lag_ratio=0.2), run_time=1.1)
        self.at("lack of")
        for rc in chs:
            gr.tiles[rc].move_to(gr.pos(*rc))
        tg = T("left: lack of space and food", 30, TEXT, weight=BOLD).move_to([3.35, -2.6, 0])
        self.play(*[gr.tiles[rc].animate.set_fill(BARE, 0.95).set_opacity(0.95) for rc in chs], FadeIn(tg, shift=UP * 0.1), run_time=1.0)
        self.at("indirect help")
        cap = T("net effect = direct + indirect (in this patch)", 32, GOLD, weight=BOLD).move_to([0, -3.45, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), Indicate(a_ind, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.at("outweighed")
        self.play(a_ind.animate.scale(1.12, about_point=a_ind.get_start()), s_ind.animate.shift(UP * 0.2), a_dir.animate.scale(0.8, about_point=a_dir.get_start()), run_time=1.2)
        self.finish()


# --------------------------------------------------------------- 13: the keystone
class S13Keystone(Base):
    def construct(self):
        C = np.array([0.0, -1.2, 0.0])
        blocks = []
        for k in range(7):
            ro = 2.9 if k != 3 else 3.08
            b = AnnularSector(inner_radius=1.9, outer_radius=ro, angle=PI / 7, start_angle=k * PI / 7, arc_center=C,
                              stroke_color=BG, stroke_width=4, fill_color=KCOL["A"], fill_opacity=0.9)
            blocks.append(b)
        pil = [Rectangle(width=1.0, height=1.5, stroke_color=BG, stroke_width=4, fill_color=KCOL["A"], fill_opacity=0.9).move_to([sx * 2.4, -1.95, 0]) for sx in (-1, 1)]
        key = blocks[3]
        others = [b for i, b in enumerate(blocks) if i != 3]
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.8) for m in pil + others], lag_ratio=0.25), run_time=2.7)
        self.at("Payne used")
        self.play(FadeIn(key, shift=DOWN * 0.9), run_time=0.7)
        self.play(key.animate.set_fill(ORANGE, 1.0), run_time=0.6)
        lab = T("keystone", 44, ORANGE, weight=BOLD).move_to([0, 2.55, 0])
        note = T("(Paine, 1969, per the PNAS memorial)", 26, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), FadeIn(note), run_time=0.8)
        self.at("A keystone species")
        defn = T("keystone species: effect large relative to abundance", 32, TEXT, weight=BOLD).move_to([0, -3.45, 0])
        self.play(FadeIn(defn, shift=UP * 0.15), run_time=0.9)
        self.at("effect")
        el = T("effect", 44, ORANGE, weight=BOLD).move_to(lab)
        self.play(Transform(lab, el), FadeOut(note), key.animate.scale(1.05), run_time=0.8)
        pulse_on(key, 0.05, 4.0)
        self.at("abundance")
        ab = T("abundance", 40, TEXT, weight=BOLD).move_to([-4.9, 0.7, 0])
        ln = Line([-3.7, 0.7, 0], blocks[5].get_center() + LEFT * 0.3, color=TEXT, stroke_width=4)  # blocks run from the right, so 5 is the left-side stone beside the label
        self.play(FadeIn(ab, shift=RIGHT * 0.15), Create(ln), run_time=0.9)
        self.finish()


# --------------------------------------------------------------- 14: keystone predation, one patch
class S14Process(Base):
    def construct(self):
        gc = Grid(GXC, GY, MIX)
        gr = Grid(GXR, GY, FIN)
        star = sea_star(0.34).move_to(gc.ctr(1, 2))
        self.add(gc.g, gr.g, star)
        shimmer(gc)
        self.at("dominant")
        a = Arrow(gc.ctr(1, 2), gc.ctr(2, 2), buff=0.28, color=ORANGE, stroke_width=7, tip_length=0.2)
        l1 = T("dominant competitor", 30, TEAL, weight=BOLD).move_to([GXC, -2.7, 0])
        self.play(Create(a), FadeIn(l1, shift=UP * 0.1), Indicate(gc.tiles[(2, 2)], color=GOLD, scale_factor=1.3), run_time=0.9)
        self.at("weaker")
        l2 = T("weaker ones gain", 30, TEXT, weight=BOLD).move_to([GXC, -3.3, 0])
        weak = [(0, 1), (3, 1), (4, 3), (2, 5)]
        self.play(FadeIn(l2, shift=UP * 0.1), *[Indicate(gc.tiles[rc], color=GOLD, scale_factor=1.3) for rc in weak], run_time=1.2)
        self.at("keystone predation")
        t1 = T("keystone predation", 44, ORANGE, weight=BOLD).move_to([0, 3.15, 0])
        t2 = T("eat the dominant competitor, weaker ones gain", 30, TEXT).move_to([0, 2.5, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.15), FadeIn(t2, shift=DOWN * 0.1), run_time=1.0)
        self.at("But this was")
        gc.g.clear_updaters()
        pair = VGroup(gc.g, gr.g, star, a)
        cl = [(4.5, 3.4), (3.7, 2.2), (4.3, 1.2), (3.5, 0.1), (4.2, -1.0), (3.4, -2.0), (4.0, -3.2)]
        coast = VMobject().set_points_smoothly([np.array([x, y, 0.0]) for x, y in cl]).set_stroke(GREY, 6)
        land = Polygon(*[np.array([x, y, 0.0]) for x, y in cl], [6.7, -3.2, 0], [6.7, 3.4, 0], stroke_width=0, fill_color=GREY, fill_opacity=0.2)
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(t1), FadeOut(t2), FadeIn(land), Create(coast),
                  pair.animate.scale(0.5).move_to([-3.5, 0.1, 0]), run_time=1.0)
        self.at("one removal patch")
        nt = T("n = 1 removal, 1 control", 32, TEXT, weight=BOLD).move_to([-3.5, -1.8, 0])
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.8)
        self.at("strong local")
        pin = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1), Circle(radius=0.38, stroke_color=ORANGE, stroke_width=4)).move_to([3.55, 0.1, 0])
        ln = Line([-0.7, 0.1, 0], [3.1, 0.1, 0], color=ORANGE, stroke_width=4)
        self.play(FadeIn(pin, scale=2.0), Create(ln), run_time=0.6)
        qs = VGroup(*[T("?", 52, TEXT, weight=BOLD).move_to([x, y, 0]) for x, y in [(5.0, 2.6), (5.6, 1.2), (4.9, -0.9), (5.7, -2.0), (5.0, -3.0), (4.6, 0.9)]])
        self.play(LaggedStart(*[FadeIn(q, scale=0.4) for q in qs], lag_ratio=0.2), run_time=1.2)
        self.at("not yet a general")
        self.play(*[Indicate(q, color=GOLD, scale_factor=1.3) for q in qs], run_time=1.2)
        self.finish()


# --------------------------------------------------------------- 15: the rule, in the ledgers
class S15Rule(Base):
    def construct(self):
        Lo, Lt, Lg = ledgers3()
        yy = -2.35
        ticks = VGroup(*[Line([x, yy, 0], [x, LCY - 2.15, 0], color=c, stroke_width=5) for x, c in [(XO, ORANGE), (XT, TEAL)]])
        dotted = DashedLine([XO, yy, 0], [XG - 0.15, yy, 0], dash_length=0.16, stroke_width=7, color=TEXT)
        tip = Triangle(stroke_width=0, fill_color=TEXT, fill_opacity=1).scale(0.17).rotate(-PI / 2).move_to([XG, yy, 0])
        self.add(Lo.mobs(), Lt.mobs(), Lg.mobs(), ticks, dotted, tip)
        self.wait(0.3)
        self.at("effects can run")
        solid1 = Line([XO, yy, 0], [XT, yy, 0], color=ORANGE, stroke_width=9)
        self.play(Create(solid1), run_time=1.2)
        self.at("species it eats")
        self.play(Indicate(Lt.base, color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("to the species they")
        solid2 = Line([XT, yy, 0], [XG - 0.15, yy, 0], color=TEAL, stroke_width=9)
        names = VGroup(*[swatch_row(k, n, XG - 1.4, LCY + 0.55 - 0.85 * i, 30) for i, (k, n) in enumerate([("A", "barnacles"), ("E", "algae"), ("C", "chitons")])])
        self.play(Create(solid2), FadeOut(VGroup(*Lg.entries)), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(n, shift=LEFT * 0.15) for n in names], lag_ratio=0.3), run_time=1.2)
        self.at("On Payne's")
        tag = T("Paine's shore; size and sign vary by community", 30, TEXT, weight=BOLD).move_to([0, -3.35, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.8)
        self.at("they did")
        self.play(Indicate(Lg.base, color=GREY, scale_factor=1.04), run_time=0.8)
        self.finish()


class S16End(EndCard):
    LINE = "A predator's effects can run through the species it eats."
