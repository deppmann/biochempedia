"""The Mix Moves the Average: chapter 2 of cell-state-and-disease.

COLOR MAP (same as chapter 1)
  BLUE    normal basal progenitors
  GREEN   differentiating cells
  YELLOW  (gold) Notch1-mutant cells and their descendants
  PURPLE  T cells (new in this chapter)
  GREY    structure;  TEXT  questions and conclusions
All pictures are schematic; no molecular structures are drawn. RNA numbers are made up.
"""
import random
import colorsys
from bp_style import *

GOLDEN = YELLOW
PURPLE = "#B58CE8"
KHAKI = "#B9A96B"
LESSON_NAME = "Cell State and Disease"

# ---------------------------------------------------------------- honeycomb (hook and hand-off)
HR = 0.27
_dx, _dy = HR * 3 ** 0.5, HR * 1.5
HPOS = [np.array([-6.15 + c * _dx + (r % 2) * _dx / 2, -2.4 + r * _dy, 0.0]) for r in range(13) for c in range(16)]


def gold_ids(scale):
    rng = random.Random(7)
    noise = [rng.random() for _ in HPOS]
    seeds = [(-4.6, 1.4, 1.0), (-1.6, -1.3, .9), (0.4, 1.6, .8), (-5.0, -1.6, .7), (-2.7, 2.0, .6), (-0.2, -0.2, .5)]
    ids = []
    for k, p in enumerate(HPOS):
        for sx, sy, sr in seeds:
            if np.hypot(p[0] - sx, p[1] - sy) / (sr * scale) < .75 + .45 * noise[k]:
                ids.append(k)
                break
    return ids


def make_honey(ids):
    gs = set(ids)
    hexes = VGroup()
    for k, p in enumerate(HPOS):
        col = GOLDEN if k in gs else BLUE
        hexes.add(RegularPolygon(6, radius=HR, start_angle=PI / 2, color=col, stroke_width=1.5,
                                 fill_color=col, fill_opacity=.34).move_to(p))
    return hexes


def honey_bars(ids):
    gs = set(ids)
    bars = VGroup()
    for k, p in enumerate(HPOS):
        gold = k in gs
        h = .22 if gold else .11
        bars.add(Rectangle(width=.07, height=h, stroke_width=0, fill_color=GOLDEN if gold else BLUE,
                           fill_opacity=1).move_to(p + DOWN * (.11 - h / 2) + DOWN * 0.0))
    return bars


def shimmer(g, amp=.2, speed=1.4):
    t = [0.0]

    def f(m, dt):
        t[0] += dt
        for k, s in enumerate(m):
            s.set_stroke(opacity=.7 + amp * np.sin(t[0] * speed + k * .35))
    g.add_updater(f)


def breathe(mobs, base=.55, amp=.1, speed=1.3):
    for k, m in enumerate(mobs):
        st = [0.0]

        def f(mm, dt, st=st, k=k):
            st[0] += dt
            mm.set_fill(opacity=base + amp * np.sin(st[0] * speed + k * .8))
        m.add_updater(f)


# ---------------------------------------------------------------- tube and gauge (right panel)
TUBE_X, TUBE_Y0, TUBE_Y1, TUBE_W = 2.55, -2.0, 1.8, 0.9
GC = np.array([4.95, 1.5, 0.0])
GR = 1.25
GLAB = np.array([4.95, 0.55, 0.0])
PANEL_X = 5.0


class Tube(VGroup):
    def __init__(self, level=0.0):
        super().__init__()
        self.level = ValueTracker(level)
        h = TUBE_Y1 - TUBE_Y0
        x = TUBE_X
        out = VMobject(stroke_color=TEXT, stroke_width=4)
        out.set_points_as_corners([[x - TUBE_W / 2, TUBE_Y1, 0], [x - TUBE_W / 2, TUBE_Y0, 0],
                                   [x + TUBE_W / 2, TUBE_Y0, 0], [x + TUBE_W / 2, TUBE_Y1, 0]])
        liquid = Rectangle(width=TUBE_W - .14, height=.01, stroke_width=0, fill_color=KHAKI, fill_opacity=.8)

        def geo():
            sc = out.height / h
            return out.get_center()[0], out.get_bottom()[1], sc

        def fl(m):
            cx, by, sc = geo()
            hh = max(self.level.get_value() * (h - .2) * sc, .001)
            m.become(Rectangle(width=(TUBE_W - .14) * sc, height=hh, stroke_width=0, fill_color=KHAKI,
                               fill_opacity=.8).move_to([cx, by + .07 * sc + hh / 2, 0]))
        liquid.add_updater(fl)
        self.add(liquid, out)
        for k in range(7):
            d = Dot(radius=.05, color="#E3D9A8")
            d.t = k * 1.7

            def f(m, dt, k=k):
                m.t += dt
                cx, by, sc = geo()
                hh = self.level.get_value() * (h - .2)
                if hh < .15:
                    m.set_opacity(0)
                    return
                m.set_opacity(.85)
                m.move_to([cx + (TUBE_W / 2 - .17) * sc * np.sin(m.t * (.9 + .13 * k) + k * 1.3),
                           by + (.07 + hh * (.5 + .38 * np.sin(m.t * (.6 + .07 * k) + k))) * sc, 0])
            d.add_updater(f)
            self.add(d)


class Gauge(VGroup):
    def __init__(self, value=0.0, ticks=(0, 10, 20), center=GC, R=GR):
        super().__init__()
        self.tracker = ValueTracker(value)
        c = np.array(center)
        self.arc = Arc(radius=R, start_angle=0, angle=PI, arc_center=c, stroke_color=GREY, stroke_width=6)
        parts = [self.arc, Line(c + LEFT * R, c + RIGHT * R, color=GREY, stroke_width=3)]
        for v in ticks:
            a = PI * (1 - v / 20)
            u = np.array([np.cos(a), np.sin(a), 0])
            parts.append(Line(c + u * R * .88, c + u * R, color=TEXT, stroke_width=3))
            parts.append(T(str(v), 26).move_to(c + u * (R + .3)))
        self.hub = Dot(c, radius=.09, color=TEXT)
        self.needle = Line(c, c + UP * R * .86, color=TEXT, stroke_width=5)

        def upd(m):
            a = PI * (1 - self.tracker.get_value() / 20)
            b = self.hub.get_center()
            Rr = self.arc.width / 2
            m.put_start_and_end_on(b, b + np.array([np.cos(a), np.sin(a), 0]) * Rr * .86)
        self.needle.add_updater(upd)
        self.add(*parts, self.needle, self.hub)

    def marker(self, v, color=TEXT):
        a = PI * (1 - v / 20)
        u = np.array([np.cos(a), np.sin(a), 0])
        c = self.hub.get_center()
        Rr = self.arc.width / 2
        m = Line(c + u * Rr * .7, c + u * Rr * 1.1, color=color, stroke_width=5)
        self.add(m)
        return m


def cover_box():
    box = RoundedRectangle(width=3.4, height=2.4, corner_radius=.15, stroke_color=GREY,
                           fill_color="#2a2f3a", fill_opacity=1).move_to([GC[0], 2.45, 0])
    return VGroup(box, T("?", 44, GREY).move_to(box))


def glabel(text="copies per\naverage cell"):
    return T(text, 26, line_spacing=.9).move_to(GLAB)


# ---------------------------------------------------------------- the tray of ten cells
TRAY_X = [-5.2, -3.85, -2.5, -1.15, 0.2]
ROW_Y = [0.8, -2.0]
CR = .55
BK = .055
GOLD2 = (2, 6)
GOLD6 = (0, 2, 5, 6, 8, 9)


def tpos(i):
    return np.array([TRAY_X[i % 5], ROW_Y[i // 5], 0.0])


def make_bar(i, col):
    h = (20 if col == GOLDEN else 10) * BK
    return Rectangle(width=.5, height=h, stroke_width=0, fill_color=col, fill_opacity=.9).move_to(
        tpos(i) + UP * (CR + .1 + h / 2))


class Tray:
    def __init__(self, gold, bars=True):
        self.cells, self.bars = [], []
        for i in range(10):
            col = GOLDEN if i in gold else BLUE
            self.cells.append(Circle(radius=CR, stroke_color=col, stroke_width=3, fill_color=col,
                                     fill_opacity=.55).move_to(tpos(i)))
            if bars:
                self.bars.append(make_bar(i, col))
        self.cg = VGroup(*self.cells)
        self.bg = VGroup(*self.bars)

    def ambient(self):
        breathe(self.cells, .55, .08, 1.2)
        breathe(self.bars, .88, .08, 1.5)

    def golds(self, gold):
        return VGroup(*[self.cells[i] for i in gold])


def pulse(g, color=TEXT):
    return g.animate(rate_func=there_and_back).set_fill(color, 1.0)


class World:
    """Tray + tube + gauge, rebuilt at the same place in every scene of the 'bulk' stretch."""

    def __init__(self, scene, gold=GOLD2, bars=True, level=.55, needle=12, marker=False, cover=False,
                 top_label=None, made_up=True):
        self.tray = Tray(gold, bars)
        self.tube = Tube(level)
        self.gauge = Gauge(needle)
        if marker:
            self.gauge.marker(12)
        self.glab = glabel()
        self.cover = cover_box() if cover else None
        self.top = T(top_label, 34).move_to([-1.2, 3.3, 0]) if top_label else None
        self.mu = T("made-up numbers", 28).move_to([-6.4, 3.4, 0], aligned_edge=LEFT) if made_up else None
        items = [self.tray.cg, self.tray.bg, self.tube, self.gauge, self.glab, self.cover, self.top, self.mu]
        scene.add(*[m for m in items if m is not None])
        self.tray.ambient()


def sum_lines(kind):
    if kind == "early":
        rows = [("0.2 × 20 = 4", GOLDEN), ("0.8 × 10 = 8", BLUE), ("= 12 per cell", TEXT)]
    else:
        rows = [("0.6 × 20 = 12", GOLDEN), ("0.4 × 10 = 4", BLUE), ("= 16 per cell", TEXT)]
    out = []
    for (s, c), y in zip(rows, [-0.35, -1.05, -1.8]):
        m = M(s, 28, c)
        fit(m, max_w=3.2)
        out.append(m.move_to([PANEL_X, y, 0]))
    return out


def question_card():
    box = RoundedRectangle(width=3.3, height=1.9, corner_radius=.18, color=TEXT, fill_color=TEXT, fill_opacity=.05)
    return VGroup(box, T("Up, down,\nor the same?", 32, line_spacing=.95).move_to(box)).move_to([PANEL_X, -1.4, 0])


# ---------------------------------------------------------------- clusters
CLOUD_C = {"blue": (-4.0, 1.2), "green": (0.0, 1.2), "purple": (-1.0, -2.3), "gold": (3.9, -0.1)}
CLOUD_COL = {"blue": BLUE, "green": GREEN, "purple": PURPLE, "gold": GOLDEN}
EARLY = {"blue": 6, "green": 5, "gold": 3, "purple": 3}
LATER = {"blue": 5, "green": 4, "gold": 8, "purple": 2}
BAR_H = {"blue": .3, "green": .36, "purple": .5, "gold": .6}


def cloud_pts(name, n):
    cx, cy = CLOUD_C[name]
    rng = random.Random(name)
    pts = []
    for i in range(n):
        a = i * 2.399 + rng.uniform(-.2, .2)
        r = .55 + .65 * np.sqrt(i / 12) + rng.uniform(0, .08)
        pts.append(np.array([cx + r * np.cos(a), cy + r * np.sin(a), 0]))
    return pts


def _mk_dot(p, name):
    d = Dot(p, radius=.2, color=CLOUD_COL[name])
    d.base = p.copy()
    d.ph = random.random() * 6
    d.driven = False
    return d


def off(d):
    return np.array([.09 * np.sin(d.ph * .8), .09 * np.cos(d.ph * .9 + 1), 0])


def make_field(counts):
    f = {}
    for name, n in counts.items():
        f[name] = [_mk_dot(p, name) for p in cloud_pts(name, n)]
    return f


def all_dots(f):
    return VGroup(*[d for ds in f.values() for d in ds])


def dot_breathe(g):
    t = [0.0]

    def fn(m, dt):
        t[0] += dt
        for k, d in enumerate(m):
            d.ph += dt
            d.set_fill(opacity=.75 + .2 * np.sin(t[0] * 1.5 + k * .9))
            if not d.driven:
                d.move_to(d.base + off(d))
    g.add_updater(fn)


def cloud_bar(name):
    cx, cy = CLOUD_C[name]
    h = BAR_H[name]
    return Rectangle(width=.2, height=h, stroke_width=0, fill_color=CLOUD_COL[name], fill_opacity=1).move_to(
        [cx, cy - .3 + h / 2, 0])


def corner(text, side="L", y=3.45):
    m = T(text, 28)
    return m.move_to([-6.4 if side == "L" else 6.4, y, 0], aligned_edge=LEFT if side == "L" else RIGHT)


def clock_face(center, color=TEXT, r=.17, speed=.65):
    face = Circle(radius=r, color=color, stroke_width=2).move_to(center)
    hand = Line(center, center + UP * r * .75, color=color, stroke_width=2.2)
    hand.add_updater(lambda m, dt: m.rotate(-speed * dt, about_point=face.get_center()))
    return VGroup(face, hand)


def hue(k, n=30):
    r, g, b = colorsys.hsv_to_rgb((k / n + .05) % 1, .6, .95)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def dna_chip(stripe=None, w=.36, h=.24):
    box = RoundedRectangle(width=w, height=h, corner_radius=.05, stroke_color=TEAL, stroke_width=2,
                           fill_color=TEAL, fill_opacity=.25)
    st = Rectangle(width=w * .3, height=h, stroke_width=0, fill_color=stripe or GREY, fill_opacity=1 if stripe else 0)
    st.move_to(box.get_left() + RIGHT * w * .15)
    return VGroup(box, st)


# ================================================================= scenes
class S00Hook(SpokenScene):
    def construct(self):
        ids = gold_ids(1.0)
        honey = make_honey(ids)
        tube = Tube(0.0)
        gauge = Gauge(4)
        glab = T("bulk reading", 28).move_to(GLAB)
        where = corner("mouse oesophagus", "L", -3.45)
        sch = corner("schematic", "R", -3.45)
        self.play(FadeIn(honey), FadeIn(gauge), FadeIn(glab), FadeIn(where), FadeIn(sch), run_time=.9)
        self.add(tube)
        shimmer(honey)
        self.play(gauge.tracker.animate(run_time=1.5).set_value(9))
        self.at("did any cell")
        q = T("Did any cell turn it up?", 44).move_to([-0.2, 3.4, 0])
        self.play(FadeIn(q, shift=DOWN * .1), run_time=.6)
        self.at("chapter 1 ended")
        self.play(q.animate.scale(.72), run_time=.8)
        self.at("gold clones spread")
        golds = VGroup(*[honey[k] for k in ids])
        self.play(Indicate(golds, color=GOLDEN, scale_factor=1.04), run_time=1.2)
        self.at("divided no faster")
        self.play(honey.animate(rate_func=there_and_back, run_time=1.6).set_fill(BLUE, .5))
        self.at("grind that lining")
        target = np.array([TUBE_X, -1.0, 0])
        order = sorted(range(len(honey)), key=lambda k: -HPOS[k][0])
        self.play(LaggedStart(*[honey[k].animate.move_to(target).scale(.35).set_color(KHAKI) for k in order],
                              lag_ratio=.008, run_time=2.6),
                  tube.level.animate(run_time=3.2).set_value(.55))
        self.remove(honey)
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON_NAME
    TITLE = "The Mix Moves the Average"

    def construct(self):
        tube = Tube(.55)
        self.add(tube)
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), 24, GREY)
        title = T("The Mix Moves\nthe Average", 54, font=TITLE_FONT, line_spacing=1.0)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=.3).move_to([-2.6, 0, 0])
        self.play(FadeIn(g, shift=UP * .1), run_time=.5)
        self.finish()


class S02Bulk(SpokenScene):
    def construct(self):
        tube = Tube(.55)
        self.add(tube)
        tray = Tray(GOLD2, bars=False)
        gauge = Gauge(0)
        glab = glabel()
        self.play(tube.level.animate(run_time=1.3).set_value(0),
                  FadeIn(tray.cg, lag_ratio=.05), FadeIn(gauge), run_time=1.3)
        tray.ambient()
        mu = corner("made-up numbers")
        self.play(FadeIn(mu), run_time=.5)
        self.at("each gold cell")
        golds = tray.golds(GOLD2)
        self.play(Indicate(golds, color=GOLDEN, scale_factor=1.12), run_time=.8)
        self.at("20")
        gb = [make_bar(i, GOLDEN) for i in GOLD2]
        for b in gb:
            self.add(b)
        self.play(*[GrowFromEdge(b, DOWN) for b in gb], run_time=.9)
        l20 = T("20", 32, GOLDEN).move_to(gb[0].get_top() + UP * .3)
        self.play(FadeIn(l20), run_time=.4)
        self.at("each blue cell")
        blues = VGroup(*[tray.cells[i] for i in range(10) if i not in GOLD2])
        self.play(Indicate(blues, color=BLUE, scale_factor=1.08), run_time=.8)
        self.at("10")
        bb = {i: make_bar(i, BLUE) for i in range(10) if i not in GOLD2}
        for b in bb.values():
            self.add(b)
        self.play(*[GrowFromEdge(b, DOWN) for b in bb.values()], run_time=.9)
        l10 = T("10", 32, BLUE).move_to(bb[0].get_top() + UP * .3)
        self.play(FadeIn(l10), run_time=.4)
        allbars = [gb[0], gb[1]] + list(bb.values())
        breathe(allbars, .88, .08, 1.5)
        self.at("bulk assay")
        self.play(FadeOut(l20), FadeOut(l10), run_time=.2)
        top = np.array([TUBE_X, TUBE_Y1 + .1, 0])
        dots = [Dot(b.get_top(), radius=.1, color=b.get_color()) for b in allbars]
        self.add(*dots)
        self.play(LaggedStart(*[d.animate.move_to(top) for d in dots], lag_ratio=.08, run_time=1.2),
                  tube.level.animate(run_time=1.6).set_value(.55))
        self.remove(*dots)
        self.at("reports copies")
        self.play(FadeIn(glab), run_time=.5)
        self.at("per average")
        self.play(gauge.tracker.animate(run_time=1.3).set_value(12))
        self.finish()


class S03Before(SpokenScene):
    def construct(self):
        w = World(self, GOLD2, bars=True, level=.55, needle=12, top_label=None)
        top = T("early", 34).move_to([-1.2, 3.3, 0])
        self.play(FadeIn(top), run_time=.5)
        self.at("gold cells are")
        self.play(Indicate(w.tray.golds(GOLD2), color=GOLDEN, scale_factor=1.12), run_time=.8)
        L = sum_lines("early")
        self.at("2 tenths")
        self.play(FadeIn(L[0], shift=LEFT * .2), pulse(w.tray.golds(GOLD2), GOLDEN), run_time=.9)
        self.at("8 tenths")
        blues = VGroup(*[w.tray.cells[i] for i in range(10) if i not in GOLD2])
        self.play(FadeIn(L[1], shift=LEFT * .2), Indicate(blues, color=BLUE, scale_factor=1.05), run_time=.9)
        self.at("gives 12")
        self.play(FadeIn(L[2], shift=LEFT * .2), w.gauge.tracker.animate(run_time=.35).set_value(13))
        self.play(w.gauge.tracker.animate(run_time=.35).set_value(12))
        w.gauge.marker(12)
        self.play(Indicate(L[2], color=TEXT), run_time=.7)
        self.finish()


class S04Question(SpokenScene):
    def construct(self):
        w = World(self, GOLD2, bars=True, level=.55, needle=12, marker=True, top_label="early")
        L = sum_lines("early")
        self.add(*L)
        cover = cover_box()
        self.play(FadeOut(VGroup(*L)), FadeIn(cover, shift=DOWN * .2), Transform(w.top, T("later", 34).move_to(w.top)),
                  run_time=.8)
        self.at("clones have spread")
        for i in (0, 5, 8, 9):
            nb = make_bar(i, GOLDEN)
            self.play(w.tray.cells[i].animate.set_color(GOLDEN), Transform(w.tray.bars[i], nb),
                      Flash(w.tray.cells[i], color=GOLDEN, flash_radius=.7, line_length=.15), run_time=.6)
        self.at("no single cell")
        lab = T("no cell changes its level", 28).move_to([-2.5, -3.3, 0])
        self.play(FadeIn(lab), run_time=.5)
        self.at("how much")
        self.play(pulse(w.tray.bg, TEXT), run_time=1.2)
        self.at("does the bulk reading")
        card = question_card()
        self.play(FadeIn(card, shift=LEFT * .2), run_time=.6)
        self.finish()


class S05Pause(SpokenScene):
    def construct(self):
        w = World(self, GOLD6, bars=True, level=.55, needle=12, marker=True, cover=True, top_label="later")
        lab = T("no cell changes its level", 28).move_to([-2.5, -3.3, 0])
        card = question_card()
        self.add(lab, card)
        t = [0.0]

        def f(m, dt):
            t[0] += dt
            m[0].set_stroke(opacity=.55 + .45 * np.sin(t[0] * 2))
        card.add_updater(f)
        self.wait(self.narration_s)


class S06Reveal(SpokenScene):
    def construct(self):
        w = World(self, GOLD6, bars=True, level=.55, needle=12, marker=True, cover=True, top_label="later")
        lab = T("no cell changes its level", 28).move_to([-2.5, -3.3, 0])
        card = question_card()
        self.add(lab, card)
        self.at("goes up")
        self.play(FadeOut(card, shift=RIGHT * .5), FadeOut(w.cover, shift=UP * .4), run_time=.9)
        L = sum_lines("later")
        self.at("six tenths")
        self.play(FadeIn(L[0], shift=LEFT * .2), pulse(w.tray.golds(GOLD6), GOLDEN), run_time=.9)
        self.at("plus four tenths")
        blues = VGroup(*[w.tray.cells[i] for i in range(10) if i not in GOLD6])
        self.play(FadeIn(L[1], shift=LEFT * .2), Indicate(blues, color=BLUE, scale_factor=1.06), run_time=.9)
        self.at("give sixteen")
        self.play(FadeIn(L[2], shift=LEFT * .2), w.gauge.tracker.animate(run_time=1.5).set_value(16))
        self.at("rose by a third")
        R = GR + .18
        a0, a1 = PI * (1 - 16 / 20), PI * (1 - 12 / 20)
        br = Arc(radius=R, start_angle=a0, angle=a1 - a0, arc_center=GC, stroke_color=TEXT, stroke_width=6)
        up = T("up by a third", 28, TEXT).move_to([5.2, 3.55, 0])
        self.play(Create(br), FadeIn(up), run_time=.9)
        self.at("no cell turned")
        self.play(pulse(w.tray.bg, TEXT), run_time=1.3)
        self.at("only the mix")
        self.play(pulse(w.tray.golds(GOLD6), GOLDEN), Indicate(w.tray.golds(GOLD6), color=GOLDEN, scale_factor=1.1),
                  run_time=1.0)
        self.finish()


def mini_icon(gold, scale_bars=1.0):
    g = VGroup()
    for i in range(10):
        col = GOLDEN if i in gold else BLUE
        x = (i % 5 - 2) * .33
        y = [.42, -.42][i // 5]
        c = Circle(radius=.11, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=.6).move_to([x, y, 0])
        h = (20 if col == GOLDEN else 10) * .012 * scale_bars
        b = Rectangle(width=.12, height=h, stroke_width=0, fill_color=col, fill_opacity=.9).move_to(
            [x, y + .13 + h / 2, 0])
        g.add(c, b)
    return g


class S07Idea(SpokenScene):
    def construct(self):
        w = World(self, GOLD6, bars=True, level=.55, needle=16, marker=True, top_label=None, made_up=False)
        left = VGroup(w.tray.cg, w.tray.bg, w.tube)
        self.at("idea of this lesson")
        gcol = VGroup(w.gauge, w.glab)
        self.play(left.animate.scale(.5).move_to([-4.3, 0, 0]),
                  gcol.animate.scale(.85).move_to([5.2, 0.9, 0]), run_time=1.6)
        ia = mini_icon(GOLD6).move_to([-1.2, 1.9, 0])
        ib = mini_icon(GOLD2, 1.33).move_to([-1.2, -1.2, 0])
        la = T("which cells are there", 28).move_to([1.9, 1.9, 0])
        lb = T("how cells behave", 28).move_to([1.9, -1.2, 0])
        self.at("which cells are")
        self.play(FadeIn(ia), FadeIn(la, shift=LEFT * .2), run_time=.9)
        self.at("its cells behave")
        self.play(FadeIn(ib), FadeIn(lb, shift=LEFT * .2), run_time=.9)
        self.at("on its own")
        aa = Arrow([3.9, 1.9, 0], [4.3, 1.4, 0], buff=0, color=TEXT, stroke_width=4)
        ab = Arrow([3.9, -1.0, 0], [4.2, .95, 0], buff=0, color=TEXT, stroke_width=4)
        self.play(GrowArrow(aa), GrowArrow(ab), run_time=.9)
        self.at("cannot tell")
        q = T("?", 56).move_to([5.2, 2.7, 0])
        self.play(FadeIn(q), Indicate(VGroup(aa, ab), color=TEXT, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- single-cell scenes
def sample_layout():
    rng = random.Random(3)
    kinds = ["blue"] * 9 + ["green"] * 8 + ["gold"] * 9 + ["purple"] * 4
    rng.shuffle(kinds)
    base = []
    for k in range(30):
        r, c = divmod(k, 6)
        base.append(np.array([-2.6 + (c - 2.5) * .85, -0.2 + (r - 2) * .85, 0]))
    return kinds, base


def sample_color(kind, k):
    if kind == "green":
        return interpolate_color(ManimColor(BLUE), ManimColor(GREEN), .5 + .5 * ((k % 4) / 3))
    return {"blue": BLUE, "gold": GOLDEN, "purple": PURPLE}[kind]


class S08Scrna(SpokenScene):
    def construct(self):
        kinds, base = sample_layout()
        sep = ValueTracker(0)
        C = np.array([-2.6, -0.2, 0])
        cells = VGroup()
        for k in range(30):
            col = sample_color(kinds[k], k)
            c = Circle(radius=.38, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=.55)
            c.move_to(base[k])
            c.ph = k * 1.7

            def f(m, dt, k=k):
                m.ph += dt
                p = C + (base[k] - C) * (1 + .5 * sep.get_value())
                m.move_to(p + np.array([.07 * np.sin(m.ph * .9), .07 * np.cos(m.ph * 1.1), 0]) * (1 + 1.5 * sep.get_value()))
            c.add_updater(f)
            cells.add(c)
        sch = corner("schematic", "R", -3.45)
        self.play(LaggedStart(*[FadeIn(c, scale=.6) for c in cells], lag_ratio=.04, run_time=1.8), FadeIn(sch))
        self.at("one at a time")
        self.play(LaggedStart(*[Indicate(c, color=TEXT, scale_factor=1.2) for c in cells], lag_ratio=.06,
                              run_time=2.4))
        self.at("single cell RNA sequencing")
        lab = T("single-cell RNA sequencing", 28).move_to([-2.6, 3.4, 0])
        self.play(FadeIn(lab), run_time=.5)
        self.at("separating tissue")
        self.play(sep.animate(run_time=2.4).set_value(1))
        self.at("captured RNA")
        # chips follow their cells
        rnas, dnas = [], []
        for k, c in enumerate(cells):
            for j, off in enumerate([np.array([.3, .3, 0]), np.array([-.3, -.3, 0])]):
                ch = RoundedRectangle(width=.3, height=.2, corner_radius=.04, stroke_color=TEXT, stroke_width=2,
                                      fill_color=TEXT, fill_opacity=.2)
                ch.add_updater(lambda m, dt, c=c, off=off: m.move_to(c.get_center() + off))
                rnas.append(ch)
                d = dna_chip(None, .3, .2)
                d.add_updater(lambda m, dt, c=c, off=off: m.move_to(c.get_center() + off))
                d.set_opacity(0)
                dnas.append(d)
        ex1 = chip("captured RNA", TEXT, 28).move_to([4.6, 1.8, 0])
        arr = Arrow([4.6, 1.1, 0], [4.6, .4, 0], buff=0, color=TEXT, stroke_width=4)
        self.play(LaggedStart(*[FadeIn(r, scale=.5) for r in rnas], lag_ratio=.01, run_time=1.2), FadeIn(ex1), run_time=1.3)
        self.at("copied into DNA")
        ex2 = dna_chip(None, 3.2, .6).move_to([4.6, -.2, 0])
        t2 = T("DNA copy", 28, TEAL).move_to(ex2.get_center() + RIGHT * .5)
        self.add(*dnas)
        self.play(GrowArrow(arr), FadeIn(ex2), FadeIn(t2),
                  *[rr.animate.set_opacity(0) for rr in rnas], *[dd.animate.set_opacity(1) for dd in dnas], run_time=1.3)
        self.at("barcode")
        stripe_cols = [hue(k) for k in range(30)]
        anims = []
        for k in range(30):
            for j in range(2):
                anims.append(dnas[2 * k + j][1].animate.set_fill(stripe_cols[k], 1))
        ex2[1].set_fill("#E0709A", 1)
        bl = T("cell barcode", 28, "#E0709A").move_to([4.6, -1.5, 0])
        ptr = Arrow(bl.get_top(), ex2[1].get_bottom(), buff=.05, color="#E0709A", stroke_width=3)
        self.play(*anims, FadeIn(bl), GrowArrow(ptr), run_time=1.0)
        self.finish()


class S09Matrix(SpokenScene):
    def construct(self):
        cols, rows, sq = 17, 9, .33
        gx, gy = 1.0, -0.15
        types = ["blue"] * 6 + ["green"] * 5 + ["gold"] * 3 + ["purple"] * 3
        rng = random.Random(11)
        prof = {t: [rng.random() for _ in range(rows)] for t in CLOUD_COL}
        xs = [gx + (j - 8) * sq for j in range(cols)]
        ys = [gy + (4 - i) * sq for i in range(rows)]
        hy = ys[0] + sq / 2 + .2
        chips = []
        for j in range(cols):
            ch = dna_chip(hue(j * 5 % 17, 17), .36, .24)
            ch.move_to([rng.uniform(-6.2, -3.8), rng.uniform(-2.2, 2.0), 0])
            chips.append(ch)
        self.play(LaggedStart(*[FadeIn(c, scale=.6) for c in chips], lag_ratio=.05, run_time=.9))
        self.at("count for each gene")
        order = list(range(cols))
        rng.shuffle(order)
        self.play(LaggedStart(*[chips[j].animate.move_to([xs[j], hy, 0]) for j in order], lag_ratio=.1, run_time=2.0))
        colsq = []
        for j in range(cols):
            g = VGroup()
            for i in range(rows):
                v = min(1, max(0, prof[types[j]][i] + rng.uniform(-.18, .18)))
                g.add(Square(side_length=sq * .94, stroke_width=0, fill_color=TEXT, fill_opacity=.08 + .85 * v).move_to([xs[j], ys[i], 0]))
            colsq.append(g)
        self.play(LaggedStart(*[FadeIn(g) for g in colsq], lag_ratio=.12, run_time=2.4))
        self.at("a table")
        title = T("count matrix", 34).move_to([gx, 2.35, 0])
        self.play(FadeIn(title), run_time=.5)
        self.at("one row per gene")
        genes = T("genes", 28).rotate(PI / 2).move_to([gx - 8.5 * sq - .45, gy, 0])
        rowbox = SurroundingRectangle(VGroup(*[g[3] for g in colsq]), buff=.03, color=TEXT, stroke_width=3)
        self.play(FadeIn(genes), Create(rowbox), run_time=.8)
        self.at("one column per")
        cellsl = T("sampled cells", 28).move_to([gx, gy - 4.5 * sq - .45, 0])
        colbox = SurroundingRectangle(colsq[7], buff=.03, color=TEXT, stroke_width=3)
        self.play(FadeOut(rowbox), FadeIn(cellsl), Create(colbox), run_time=.8)
        self.play(FadeOut(colbox), run_time=.4)
        self.at("group cells")
        dots = []
        for j in range(cols):
            d = Dot([xs[j], hy, 0], radius=.12, color=chips[j][1].get_color())
            dots.append(d)
        pos = {n: cloud_pts(n, 12) for n in CLOUD_C}
        idx = {n: 0 for n in CLOUD_C}
        moves = []
        for j in range(cols):
            t = types[j]
            p = pos[t][idx[t]]
            idx[t] += 1
            moves.append(dots[j].animate.move_to(p).set_color(CLOUD_COL[t]))
        self.play(FadeOut(VGroup(*colsq)), FadeOut(title), FadeOut(genes), FadeOut(cellsl),
                  *[ReplacementTransform(chips[j], dots[j]) for j in range(cols)], run_time=.8)
        self.play(LaggedStart(*moves, lag_ratio=.05, run_time=2.4))
        self.at("into clusters")
        self.play(FadeIn(T("clusters", 34).move_to([0, 3.35, 0])), run_time=.5)
        self.finish()


def tag(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


class S10Names(SpokenScene):
    def construct(self):
        f = make_field(EARLY)
        dg = all_dots(f)
        self.add(dg)
        dot_breathe(dg)
        self.add(corner("sampled cells"), corner("schematic", "R"))
        self.at("annotated by comparing")
        t1 = tag("progenitor", -4.0, -0.5, BLUE)
        self.play(FadeIn(t1), run_time=.5)
        t2 = tag("differentiating", 0.0, -0.5, GREEN)
        self.play(FadeIn(t2), run_time=.5)
        self.at("known profiles")
        t3 = tag("T cell", 1.1, -2.3, PURPLE)
        t4 = tag("gold-profile group?", 3.9, -1.9, GOLDEN)
        self.play(FadeIn(t3), run_time=.5)
        self.play(FadeIn(t4), run_time=.5)
        bars = {n: cloud_bar(n) for n in CLOUD_C}
        self.at("shift can be")
        lab = tag("early sample", 0, 3.4, TEXT, 34)
        self.play(FadeIn(lab), FadeIn(VGroup(*bars.values())), run_time=.7)
        self.at("gold profile group")
        self.play(Transform(lab, tag("later sample", 0, 3.4, TEXT, 34)), run_time=.6)
        self.at("more sampled cells")
        newf = make_field(LATER)
        anims = []
        for n in CLOUD_C:
            old, new = f[n], newf[n]
            for k in range(max(len(old), len(new))):
                if k < len(old) and k < len(new):
                    continue
                if k >= len(old):
                    self.add(new[k])
                    anims.append(FadeIn(new[k], scale=.3))
                else:
                    anims.append(FadeOut(old[k]))
        self.play(*anims, run_time=1.6)
        self.at("stays fixed")
        self.play(pulse(VGroup(*bars.values()), TEXT), run_time=1.4)
        self.finish()


class S11Types(SpokenScene):
    def construct(self):
        f = make_field(LATER)
        dg = all_dots(f)
        self.add(dg)
        dot_breathe(dg)
        tags = VGroup(tag("progenitor", -4.0, -0.5, BLUE), tag("differentiating", 0.0, -0.5, GREEN),
                      tag("T cell", 1.1, -2.3, PURPLE), tag("gold-profile group?", 3.9, -1.9, GOLDEN))
        bars = VGroup(*[cloud_bar(n) for n in CLOUD_C])
        self.add(tags, bars, corner("schematic", "R"))
        q = T("?", 56).move_to([3.9, 1.5, 0])
        self.play(FadeOut(tags), FadeOut(bars), FadeIn(q), run_time=.8)
        wd = corner("working definitions", "R", -3.45)
        self.play(FadeIn(wd), run_time=.4)
        self.at("cell type")
        keratin = VGroup(*f["blue"], *f["green"])
        br = Brace(keratin, UP, color=TEXT)
        self.play(Create(br), run_time=.8)
        self.at("keratinocyte")
        kl = T("one type: keratinocyte", 28).move_to([-2.0, 3.3, 0])
        self.play(FadeIn(kl), run_time=.5)
        self.at("t cell")
        br2 = Brace(VGroup(*f["purple"]), RIGHT, color=TEXT)
        tl = T("one type: T cell", 28)
        tl.next_to(br2, RIGHT, buff=.15)
        self.play(Create(br2), FadeIn(tl), run_time=.8)
        self.at("state within one type")
        cx, cy = CLOUD_C["blue"]
        clocks = VGroup()
        for d in f["blue"][:3]:
            clocks.add(clock_face(d.get_center(), TEXT, .17))
        self.play(*[FadeOut(d) for d in f["blue"][:3]], FadeIn(clocks), run_time=.6)
        self.play(clocks.animate.shift(LEFT * .6 + DOWN * .1), run_time=1.0)
        self.at("dividing")
        sd = T("state: dividing", 28).move_to([-4.0, -0.5, 0])
        self.play(FadeIn(sd), run_time=.5)
        self.at("differentiating")
        ds = T("differentiation\nstates here", 28, line_spacing=.9).move_to([0.0, -0.6, 0])
        self.play(FadeIn(ds), run_time=.5)
        self.at("depends on the question")
        self.play(Indicate(br, color=TEXT), Indicate(br2, color=TEXT), run_time=1.2)
        self.finish()


class S12Artifact(SpokenScene):
    def construct(self):
        f = make_field(LATER)
        dg = all_dots(f)
        self.add(dg)
        dot_breathe(dg)
        q = T("?", 56).move_to([3.9, 1.5, 0])
        self.add(q, corner("schematic"))
        self.at("breaking up tissue")
        # dissociation stress: three green dots drift to a red cloud
        st = ValueTracker(0)
        dest = [np.array([-5.5, -1.1, 0]), np.array([-4.9, -1.3, 0]), np.array([-5.2, -0.8, 0])]
        for d, dst in zip(f["green"][:3], dest):
            d.o = d.base.copy()
            d.driven = True

            def fs(m, dt, dst=dst):
                a = st.get_value()
                m.move_to(m.o * (1 - a) + dst * a + off(m))
                m.set_color(interpolate_color(ManimColor(GREEN), ManimColor(RED), min(1, a * 2 + .3 * a * np.sin(a * 40))))
            d.add_updater(fs)
        sl = T("dissociation\nstress", 28, RED, line_spacing=.9).move_to([-5.0, -2.4, 0])
        self.play(FadeIn(sl), st.animate(run_time=2.4).set_value(1))
        self.at("samples processed separately")
        bat = ValueTracker(0)
        halves = f["purple"]
        for k, d in enumerate(halves):
            d.o = d.base.copy()
            d.driven = True
            sgn = 1 if k % 2 == 0 else -1

            def fb(m, dt, sgn=sgn):
                m.move_to(m.o + np.array([sgn * 1.0 * bat.get_value(), 0, 0]) + off(m))
            d.add_updater(fb)
        self.play(bat.animate(run_time=1.6).set_value(1))
        s1 = T("sample 1", 28).move_to([-2.0, -0.8, 0])
        s2 = T("sample 2", 28).move_to([0.0, -0.8, 0])
        bl = T("batch effect", 28).move_to([3.3, -2.4, 0])
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(bl), run_time=.6)
        self.at("clustering resolution")
        res = ValueTracker(0)
        groups = [(f["blue"][:2], np.array([-.55, .4, 0])), (f["blue"][2:4], np.array([.45, .5, 0])),
                  (f["blue"][4:], np.array([-.1, -.6, 0]))]
        for ds, vec in groups:
            for d in ds:
                d.o = d.base.copy()
                d.driven = True

                def fr(m, dt, vec=vec):
                    m.move_to(m.o + vec * res.get_value() + off(m))
                d.add_updater(fr)
        track = Line([4.0, 3.4, 0], [6.4, 3.4, 0], color=GREY, stroke_width=5)
        knob = Dot([4.0, 3.4, 0], radius=.14, color=TEXT)
        knob.add_updater(lambda m, dt: m.move_to([4.0 + 2.4 * res.get_value(), 3.4, 0]))
        rl = T("resolution", 28).move_to([2.5, 3.4, 0])
        self.play(FadeIn(track), FadeIn(knob), FadeIn(rl), run_time=.5)
        self.play(res.animate(run_time=1.5).set_value(1))
        self.at("split or merge")
        self.play(res.animate(run_time=1.0).set_value(0))
        self.finish()


def tile(y, label):
    box = RoundedRectangle(width=5.4, height=1.75, corner_radius=.18, color=TEXT, stroke_width=2,
                           fill_color=TEXT, fill_opacity=.04).move_to([3.95, y, 0])
    lb = T(label, 34).move_to([4.95, y, 0])
    return box, lb


def icon_lineage(x, y):
    p = Circle(radius=.28, color=GOLDEN, fill_color=GOLDEN, fill_opacity=.5).move_to([x - .6, y, 0])
    a = Arrow([x - .25, y, 0], [x + .1, y, 0], buff=0, color=GREY, stroke_width=3, max_tip_length_to_length_ratio=.4)
    k = VGroup(*[Circle(radius=.2, color=GOLDEN, fill_color=GOLDEN, fill_opacity=.5).move_to([x + .45, y + dy, 0])
                 for dy in (.28, -.28)])
    ol = DashedVMobject(SurroundingRectangle(VGroup(p, a, k), buff=.12, color=GOLDEN), num_dashes=24)
    return VGroup(p, a, k, ol)


def icon_perturb(x, y):
    c = Circle(radius=.5, color=BLUE, fill_color=BLUE, fill_opacity=.3).move_to([x, y, 0])
    part = Square(side_length=.3, color=TEXT, stroke_width=2).move_to([x, y, 0])
    cross = VGroup(Line([x - .22, y - .22, 0], [x + .22, y + .22, 0]), Line([x - .22, y + .22, 0], [x + .22, y - .22, 0])).set_color(RED).set_stroke(width=5)
    return VGroup(c, part, cross)


def icon_protein(x, y):
    c = Circle(radius=.45, color=GREEN, fill_color=GREEN, fill_opacity=.3).move_to([x - .25, y, 0])
    mk = Rectangle(width=.18, height=.3, color=TEXT, fill_color=TEXT, fill_opacity=.8).move_to([x + .2, y, 0])
    tg = Dot([x + .6, y, 0], radius=.14, color=TEAL)
    ln = Line([x + .3, y, 0], [x + .5, y, 0], color=TEAL, stroke_width=3)
    return VGroup(c, mk, ln, tg)


FIELD_S = .68
FIELD_SHIFT = np.array([-3.0, .3, 0])


def squeeze(group):
    return group.scale(FIELD_S, about_point=ORIGIN).shift(FIELD_SHIFT)


class S13Return(SpokenScene):
    def construct(self):
        f = make_field(LATER)
        dg = all_dots(f)
        self.add(dg)
        dot_breathe(dg)
        self.at("an observation")
        self.play(Indicate(dg, color=TEXT, scale_factor=1.04), run_time=1.0)
        self.at("hypothesis")
        qs = VGroup(*[T("?", 36).move_to(np.array(CLOUD_C[n] + (0,)) * FIELD_S + FIELD_SHIFT) for n in CLOUD_C])
        for d in dg:
            d.base = d.base * FIELD_S + FIELD_SHIFT
        self.play(dg.animate.scale(FIELD_S, about_point=ORIGIN).shift(FIELD_SHIFT), run_time=1.2)
        self.play(FadeIn(qs), run_time=.6)
        self.at("snapshot cannot")
        self.play(Indicate(qs, color=TEXT, scale_factor=1.3), run_time=1.0)
        self.at("lineage tracing")
        b1, l1 = tile(2.4, "lineage")
        self.play(Create(b1), run_time=.4)
        i1 = icon_lineage(2.5, 2.4)
        self.play(FadeIn(i1), FadeIn(l1), run_time=.8)
        self.at("perturbation tests cause")
        b2, l2 = tile(.25, "perturbation")
        l2.move_to([5.0, .25, 0])
        self.play(Create(b2), run_time=.4)
        i2 = icon_perturb(2.5, .25)
        self.play(FadeIn(i2), FadeIn(l2), run_time=.8)
        self.at("protein can check")
        b3, l3 = tile(-1.9, "protein")
        self.play(Create(b3), run_time=.4)
        i3 = icon_protein(2.5, -1.9)
        self.play(FadeIn(i3), FadeIn(l3), run_time=.8)
        self.finish()


class S14Handoff(SpokenScene):
    def construct(self):
        f = make_field(LATER)
        dg = all_dots(f)
        squeeze(dg)
        qs = VGroup(*[T("?", 36).move_to(np.array(CLOUD_C[n] + (0,)) * FIELD_S + FIELD_SHIFT) for n in CLOUD_C])
        self.add(dg, qs)
        ids = gold_ids(1.6)
        honey = make_honey(ids)
        gset = set(ids)
        gauge = Gauge(12)
        gauge.marker(12)
        glab = T("bulk reading", 28).move_to(GLAB)
        self.at("back in the lining")
        anims = []
        used = set()
        for d in dg:
            want_gold = ManimColor(d.get_color()).to_hex().upper() == ManimColor(GOLDEN).to_hex().upper()
            pick = None
            for k in range(len(HPOS)):
                if k in used:
                    continue
                if (k in gset) == want_gold:
                    pick = k
                    break
            used.add(pick)
            anims.append(ReplacementTransform(d, honey[pick]))
        rest = [honey[k] for k in range(len(HPOS)) if k not in used]
        self.play(FadeOut(qs), FadeIn(gauge), FadeIn(glab), *anims,
                  LaggedStart(*[FadeIn(h) for h in rest], lag_ratio=.004), run_time=2.2)
        shimmer(honey)
        bars = honey_bars(ids)
        self.at("gold cells became common")
        self.play(Indicate(VGroup(*[honey[k] for k in ids]), color=GOLDEN, scale_factor=1.03), FadeIn(bars), run_time=1.2)
        self.at("so the average moved")
        self.play(gauge.tracker.animate(run_time=1.6).set_value(16))
        self.at("no cell made more")
        self.play(pulse(bars, TEXT), run_time=1.5)
        self.at("change the mix")
        self.play(honey.animate(rate_func=there_and_back, run_time=1.4).set_fill(GOLDEN, .6))
        self.at("average moves without")
        self.play(Indicate(gauge, color=TEXT, scale_factor=1.06), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Change the mix, and the average moves without any cell changing."
