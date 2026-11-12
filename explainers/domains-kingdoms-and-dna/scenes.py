"""Climbing the Evidence Ladder (domains, kingdoms and DNA), film 2 of the grade 7 course.

COLOUR MAP (the lesson's simulation colours): mushroom PURPLE, oak GREEN, deer BROWN,
paramecium TEAL, bacterium ORANGE, archaeon CRIMSON. GOLD = current rung / cell wall,
BLUE = nucleus, a green oval = chloroplast.  One world: the sorting table at the right,
the evidence ladder at the left (x -6.7..-3.9), carried through every scene.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#8a5a9e"
OAKG = "#2e8b4f"
BROWN = "#a0662b"
TEALC = "#0e7c86"
ORANGE = "#d0701a"
CRIMSON = "#b23b4e"
INK = "#2b2f3a"
PAPER = "#F3F1EA"
PURPLE_L = "#c79ae0"
CHLO = "#7be08f"
WOOD_L = "#e0a860"

ORDER = ["mush", "oak", "deer", "para", "bact", "arch"]
HOME = {"mush": (-0.8, 1.5), "oak": (1.6, 1.5), "deer": (4.0, 1.5),
        "para": (-0.8, -1.6), "bact": (1.6, -1.6), "arch": (4.0, -1.6)}
STRIP = {k: (1.1 + (i - 2.5) * 1.55, 3.05) for i, k in enumerate(ORDER)}


# ------------------------------------------------------------------ cartoons (schematic) --------------
def art_mush(c, ink=INK):
    stalk = Rectangle(width=0.42, height=0.75, stroke_color=ink, stroke_width=3, fill_color="#e8dfd0", fill_opacity=1)
    cap = Sector(radius=0.9, angle=PI, start_angle=0, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1)
    cap.stretch(0.8, 1, about_edge=DOWN)
    cap.next_to(stalk, UP, buff=-0.01)
    spots = VGroup(*[Dot(radius=r, color=WHITE).move_to(cap.get_center() + np.array([dx, dy, 0]))
                     for dx, dy, r in [(-0.35, 0.05, 0.09), (0.1, 0.17, 0.12), (0.4, 0.0, 0.07)]])
    return VGroup(stalk, cap, spots)


def art_oak(c, ink=INK):
    trunk = Rectangle(width=0.3, height=0.85, stroke_width=0, fill_color="#6b4a2b", fill_opacity=1).move_to([0, -0.15, 0])
    cs = VGroup(*[Circle(radius=r, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1).move_to([x, y, 0])
                  for x, y, r in [(-0.4, 0.35, 0.45), (0.4, 0.35, 0.45), (0, 0.75, 0.5)]])
    return VGroup(trunk, cs)


def art_deer(c, ink=INK):
    body = Ellipse(width=1.2, height=0.55, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1)
    neck = Line([0.4, 0.1, 0], [0.62, 0.55, 0], stroke_color=c, stroke_width=16)
    head = Ellipse(width=0.42, height=0.3, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1).rotate(0.5).move_to([0.72, 0.62, 0])
    legs = VGroup(*[Line([x, -0.15, 0], [x, -0.72, 0], stroke_color=ink, stroke_width=5) for x in (-0.45, -0.3, 0.3, 0.45)])
    ant = VGroup(Line([0.68, 0.75, 0], [0.6, 1.1, 0]), Line([0.64, 0.95, 0], [0.4, 1.05, 0]),
                 Line([0.76, 0.75, 0], [0.92, 1.1, 0]), Line([0.86, 0.95, 0], [1.06, 1.0, 0])).set_stroke(ink, 4)
    return VGroup(legs, ant, body, neck, head)


def art_para(c, ink=INK):
    e = Ellipse(width=1.7, height=0.7, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=0.6)
    cil = VGroup()
    for t in np.linspace(0, 2 * PI, 26, endpoint=False):
        p = np.array([0.85 * np.cos(t), 0.35 * np.sin(t), 0])
        n = np.array([np.cos(t) / 0.85, np.sin(t) / 0.35, 0])
        n = n / np.linalg.norm(n)
        cil.add(Line(p, p + 0.13 * n, stroke_color=ink, stroke_width=2))
    dots = VGroup(Dot(radius=0.07, color=WHITE).move_to([-0.3, 0.05, 0]), Dot(radius=0.07, color=WHITE).move_to([0.25, -0.08, 0]))
    g = VGroup(cil, e, dots)
    g.rotate(0.45)
    return g


def art_bact(c, ink=INK):
    b = RoundedRectangle(width=1.3, height=0.6, corner_radius=0.3, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1)
    tail = ParametricFunction(lambda t: np.array([0.65 + 0.5 * t, 0.12 * np.sin(7 * t), 0]), t_range=[0, 1, 0.02],
                              stroke_color=ink, stroke_width=3)
    return VGroup(tail, b)


def art_arch(c, ink=INK):
    return RoundedRectangle(width=1.3, height=0.6, corner_radius=0.3, stroke_color=ink, stroke_width=3, fill_color=c, fill_opacity=1)


SPEC = {"mush": ("mushroom", PURPLE, art_mush), "oak": ("oak", OAKG, art_oak), "deer": ("deer", BROWN, art_deer),
        "para": ("paramecium", TEALC, art_para), "bact": ("bacterium", ORANGE, art_bact), "arch": ("archaeon", CRIMSON, art_arch)}


def card(key, pos, s=0.8, named=True):
    name, col, fn = SPEC[key]
    w, h = 2.5 * s, 2.7 * s
    bg = Rectangle(width=w, height=h, stroke_width=0, fill_color=PAPER, fill_opacity=1)
    bar = Rectangle(width=0.2 * s, height=h, stroke_width=0, fill_color=col, fill_opacity=1).align_to(bg, LEFT)
    art = fn(col)
    bw, bh = w * 0.72, (h * 0.5 if named else h * 0.66)
    art.scale(min(bw / art.width, bh / art.height))
    art.move_to(bg.get_center() + RIGHT * 0.1 * s + UP * (h * 0.15 if named else 0))
    parts = [bg, bar, art]
    if named:
        parts.append(T(name, 22, INK).move_to(bg.get_bottom() + UP * 0.3 + RIGHT * 0.1 * s))
    g = VGroup(*parts)
    g.key = key
    g.move_to([pos[0], pos[1], 0])
    return g


def speck(key, pos):
    col = SPEC[key][1]
    g = VGroup(Circle(radius=0.34, stroke_width=0, fill_color=col, fill_opacity=0.22), Dot(radius=0.12, color=col).set_opacity(0.8))
    g.move_to([pos[0], pos[1], 0])
    g.key = key
    return g


def bob(m, amp=0.05, per=2.6, ph=0.0):
    m._bt = ph
    w = 2 * np.pi / per

    def u(mm, dt):
        a = mm._bt
        mm._bt += dt
        mm.shift(UP * amp * (np.sin(w * mm._bt) - np.sin(w * a)))
    m.add_updater(u)
    return m


def sway(m, amp=0.05, per=3.2, ph=0.0):
    base = m.get_bottom()
    m._sw = ph
    m._ang = 0.0

    def u(mm, dt):
        mm._sw += dt
        a = amp * np.sin(2 * np.pi * mm._sw / per)
        mm.rotate(a - mm._ang, about_point=base)
        mm._ang = a
    m.add_updater(u)
    return m


# ------------------------------------------------------------------ the evidence ladder ----------------
RUNGS = ["eyes", "microscope", "cell chemistry", "DNA"]
RY = [-1.5, -0.3, 0.9, 2.1]
LX = -5.25


def build_ladder():
    rails = VGroup(Line([-6.55, -2.1, 0], [-6.55, 2.8, 0]), Line([-3.95, -2.1, 0], [-3.95, 2.8, 0])).set_stroke(TEXT, 5)
    rungs = []
    for t, y in zip(RUNGS, RY):
        box = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.14, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.1)
        lab = T(t, 28, TEXT)
        if lab.width > 2.2:
            lab.scale(2.2 / lab.width)
        rungs.append(VGroup(box, lab).move_to([LX, y, 0]))
    L = VGroup(rails, *rungs)
    L.rails = rails
    L.rungs = rungs
    return L


def _pulse(b):
    b._pt = 0.0

    def u(m, dt):
        m._pt += dt
        m.set_stroke(width=3.5 + 2.2 * np.sin(m._pt * 3))
    b.add_updater(u)


def lad_set(L, i):
    for k, r in enumerate(L.rungs):
        r[0].clear_updaters()
        on = k == i
        r[0].set_stroke(GOLD if on else GREY, 3).set_fill(GOLD if on else GREY, 0.5 if on else 0.1)
    if i is not None:
        _pulse(L.rungs[i][0])


def go_rung(sc, L, i, rt=0.7):
    anims = []
    for k, r in enumerate(L.rungs):
        r[0].clear_updaters()
        on = k == i
        anims.append(r[0].animate.set_stroke(GOLD if on else GREY, 3).set_fill(GOLD if on else GREY, 0.5 if on else 0.1))
    sc.play(*anims, run_time=rt)
    _pulse(L.rungs[i][0])


def tick(x, y, color=CHLO):
    return VMobject().set_points_as_corners([[x - 0.17, y, 0], [x - 0.05, y - 0.15, 0], [x + 0.2, y + 0.17, 0]]).set_stroke(color, 9)


def nogo(x, y):
    return VGroup(Circle(radius=0.2, stroke_color=RED, stroke_width=6), Line([-0.14, -0.14, 0], [0.14, 0.14, 0], stroke_color=RED, stroke_width=6)).move_to([x, y, 0])


def cellc(r=0.85, wcol=GREY, mcol=GREY):
    mem = Circle(radius=r, stroke_color=mcol, stroke_width=4, fill_color=mcol, fill_opacity=0.3)
    wall = Circle(radius=r + 0.13, stroke_color=wcol, stroke_width=7)
    g = VGroup(wall, mem)
    g.wall, g.mem = wall, mem
    return g


class Film(SpokenScene):
    """Adds the card dictionary and helpers shared by the scenes."""

    def put(self, key, pos, s=0.8, named=True):
        c = card(key, pos, s, named)
        self.add(c)
        bob(c, ph=hash(key) % 7)
        self.cd = getattr(self, "cd", {})
        self.cd[key] = c
        return c

    def morph(self, specs, rt=1.2, extra=()):
        """specs: list of (key, pos, s, named) -> cards replaced by new cards at the new place."""
        anims, news = [], []
        for key, pos, s, named in specs:
            new = card(key, pos, s, named)
            anims.append(ReplacementTransform(self.cd[key], new))
            news.append((key, new))
        self.play(*anims, *extra, run_time=rt)
        for key, new in news:
            self.cd[key] = new
            bob(new, ph=hash(key) % 7)


def lad_scene(sc, i, add=True):
    L = build_ladder()
    lad_set(L, i)
    if add:
        sc.add(L)
    return L


# ================================================================== scenes ==============================
class S00Title(TitleCard):
    LESSON = "Domains, Kingdoms and DNA"
    TITLE = "Climbing the Evidence Ladder"


class S01Hook(Film):
    def construct(self):
        log = RoundedRectangle(width=11, height=1.0, corner_radius=0.4, stroke_color=WOOD_L, stroke_width=3,
                               fill_color=BROWN, fill_opacity=0.6).move_to([0.6, -3.0, 0])
        mush = art_mush(PURPLE_L, TEXT).set_height(3.4).move_to([-2.4, -2.5 + 1.7, 0])
        oak = art_oak(OAKG, TEXT).set_height(4.2).move_to([3.2, -2.5 + 2.1, 0])
        wind = VGroup(*[Line([x, y, 0], [x + 1.0, y, 0], stroke_color=TEXT, stroke_width=3).set_opacity(0.35)
                        for x, y in [(-6, 1.6), (-1, 0.6), (2, 2.4)]])
        for m in wind:
            def u(mm, dt):
                mm.shift(RIGHT * 1.4 * dt)
                if mm.get_x() > 7.5:
                    mm.shift(LEFT * 15)
            m.add_updater(u)
        self.play(FadeIn(log), FadeIn(mush, shift=UP * 0.3), FadeIn(oak, shift=UP * 0.3), run_time=self.beat(0.08))
        sway(mush, 0.04, 3.0)
        sway(oak, 0.07, 3.6, 1.0)
        self.at("so why")
        q = chip("Why not a plant?", GOLD, 40)
        q.move_to([0.6, 3.1, 0])
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=self.beat(0.05))
        self.at("the answer")
        self.play(q[0].animate.set_fill(GOLD, 0.45), run_time=self.beat(0.1))
        self.finish()


class S02Cards(Film):
    def construct(self):
        slots = VGroup(*[RoundedRectangle(width=2.0, height=2.16, corner_radius=0.1, stroke_color=GREY, stroke_width=3)
                         .set_stroke(opacity=0.6).move_to([*HOME[k], 0]) for k in ORDER])
        self.play(FadeIn(slots), run_time=self.beat(0.05))
        for k, ph in zip(ORDER, ["mushroom", "oak", "deer", "paramecium", "bacterium", "archaeon"]):
            self.at(ph)
            c = card(k, HOME[k])
            self.cd = getattr(self, "cd", {})
            self.cd[k] = c
            self.play(FadeIn(c, shift=DOWN * 0.7), run_time=0.6)
            bob(c, ph=hash(k) % 7)
        L = build_ladder()
        self.at("scientists sort")
        self.play(Create(L.rails), run_time=0.8)
        for r, ph in zip(L.rungs, ["things with", "several kinds", "of evidence", "evidence"]):
            self.at(ph)
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.5)
        self.at("this latter")
        self.play(*[r[0].animate.set_stroke(GOLD, 5) for r in L.rungs], run_time=0.5)
        self.play(*[r[0].animate.set_stroke(GREY, 3) for r in L.rungs], run_time=0.5)
        self.at("it is not")
        tag = VGroup(T("kinds of evidence", 22), T("a model,", 22), T("not a timeline", 22)).arrange(DOWN, buff=0.08).move_to([LX, -3.0, 0])
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S03Eyes(Film):
    def construct(self):
        L = lad_scene(self, None)
        for k in ORDER:
            self.put(k, HOME[k])
        go_rung(self, L, 0, 0.8)
        eye = VGroup(Ellipse(width=1.2, height=0.62, stroke_color=TEXT, stroke_width=5), Circle(radius=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1))
        eye.move_to([-0.8, 3.35, 0])
        self.at("eyes")
        self.play(FadeIn(eye, scale=0.6), run_time=0.6)
        self.at("the mushroom")
        self.play(eye.animate.move_to([1.6, 3.35, 0]), run_time=1.6)
        self.at("so it")
        self.morph([("mush", (-0.8, 0.7), 0.8, True), ("oak", (1.6, 0.7), 0.8, True)], rt=1.0)
        hp = T("Plants", 32).move_to([0.4, 2.35, 0])
        bp = Line([-1.8, 1.95, 0], [2.6, 1.95, 0], stroke_color=OAKG, stroke_width=6)
        self.at("with the plants")
        self.play(FadeIn(hp, shift=DOWN * 0.1), Create(bp), run_time=0.7)
        self.at("the deer")
        self.play(eye.animate.move_to([4.0, 3.35, 0]), run_time=1.4)
        self.at("walks away")
        d = self.cd["deer"]
        self.play(d.animate.shift(RIGHT * 0.5), run_time=1.0)
        self.at("so it goes")
        self.morph([("deer", (4.2, 0.7), 0.8, True)], rt=0.9)
        ha = T("Animals", 32).move_to([4.2, 2.35, 0])
        ba = Line([3.0, 1.95, 0], [5.4, 1.95, 0], stroke_color=BROWN, stroke_width=6)
        self.at("the animals")
        self.play(FadeIn(ha, shift=DOWN * 0.1), Create(ba), run_time=0.7)
        self.at("the three tiny")
        pile = {"para": (1.0, -2.0), "bact": (1.65, -1.75), "arch": (2.3, -2.1)}
        self.play(FadeOut(eye), *[ReplacementTransform(self.cd[k], speck(k, p)) for k, p in pile.items()], run_time=2.0)
        self.at("too small")
        lab = T("too small to make out", 28).move_to([1.65, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.7)
        self.at("many scientists")
        m = self.cd["mush"]
        self.play(Indicate(m, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.at("with plants")
        self.play(bp.animate.set_stroke(GOLD, 9), run_time=0.5)
        self.play(bp.animate.set_stroke(OAKG, 6), run_time=0.5)
        self.finish()


def eyes_end(sc):
    """Rebuild the end of s03: sorted by eye, specks in a pile."""
    L = lad_scene(sc, 0)
    for k, p in {"mush": (-0.8, 0.7), "oak": (1.6, 0.7), "deer": (4.2, 0.7)}.items():
        sc.put(k, p)
    hp = T("Plants", 32).move_to([0.4, 2.35, 0])
    bp = Line([-1.8, 1.95, 0], [2.6, 1.95, 0], stroke_color=OAKG, stroke_width=6)
    ha = T("Animals", 32).move_to([4.2, 2.35, 0])
    ba = Line([3.0, 1.95, 0], [5.4, 1.95, 0], stroke_color=BROWN, stroke_width=6)
    pile = {"para": (1.0, -2.0), "bact": (1.65, -1.75), "arch": (2.3, -2.1)}
    sc.sp = VGroup(*[speck(k, p) for k, p in pile.items()])
    lab = T("too small to make out", 28).move_to([1.65, -3.2, 0])
    sc.add(hp, bp, ha, ba, sc.sp, lab)
    return L, VGroup(hp, bp, ha, ba, lab)


def icon_nuc(s=1.0):
    return VGroup(Circle(radius=0.5, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2),
                  Circle(radius=0.19, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.85).shift(UP * 0.05)).scale(s)


def icon_parts(s=1.0):
    g = VGroup(Circle(radius=0.5, stroke_color=GOLD, stroke_width=8, fill_color=GREY, fill_opacity=0.2))
    for x, y in [(-0.2, -0.17), (0.2, -0.17), (0.0, 0.2)]:
        g.add(Ellipse(width=0.3, height=0.17, stroke_width=0, fill_color=CHLO, fill_opacity=1).move_to([x, y, 0]))
    return g.scale(s)


def icon_many(s=1.0):
    one = Circle(radius=0.3, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([-0.7, 0, 0])
    many = VGroup(*[Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([0.45 + dx, dy, 0])
                    for dx, dy in [(-0.2, 0.2), (0.2, 0.2), (-0.2, -0.2), (0.2, -0.2)]])
    return VGroup(one, many).scale(s)


def icon_sunleaf():
    sun = VGroup(Circle(radius=0.17, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                 *[Line([0.25 * np.cos(a), 0.25 * np.sin(a), 0], [0.4 * np.cos(a), 0.4 * np.sin(a), 0], stroke_color=GOLD, stroke_width=4)
                   for a in np.linspace(0, 2 * PI, 8, endpoint=False)]).move_to([-0.45, 0.1, 0])
    leaf = Ellipse(width=0.55, height=0.3, stroke_width=0, fill_color=CHLO, fill_opacity=1).rotate(0.7).move_to([0.35, -0.05, 0])
    return VGroup(sun, leaf)


def icon_mouth():
    return VGroup(Ellipse(width=0.8, height=0.45, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.35),
                  Line([-0.32, 0, 0], [0.32, 0, 0], stroke_color=RED, stroke_width=4))


def microscope():
    base = RoundedRectangle(width=1.4, height=0.2, corner_radius=0.08, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([0, -1.0, 0])
    arm = Line([-0.45, -0.95, 0], [-0.45, 0.5, 0], stroke_color=TEAL, stroke_width=14)
    stage = Rectangle(width=0.95, height=0.1, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([0.1, -0.5, 0])
    tube = Rectangle(width=0.36, height=1.15, stroke_width=0, fill_color=TEXT, fill_opacity=1).rotate(-0.35).move_to([0.05, 0.4, 0])
    eyep = Rectangle(width=0.22, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=1).rotate(-0.35).move_to([0.28, 1.05, 0])
    lens = Circle(radius=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([-0.22, -0.2, 0])
    return VGroup(base, arm, stage, tube, eyep, lens)


class S04Microscope(Film):
    def construct(self):
        L, junk = eyes_end(self)
        go_rung(self, L, 1, 0.8)
        mic = microscope().set_height(2.2).move_to([5.7, -1.8, 0])
        self.play(FadeIn(mic, shift=DOWN * 0.4), run_time=1.0)
        self.at("it answers")
        pile = {"para": (0.5, -2.0), "bact": (1.6, -2.0), "arch": (2.7, -2.0)}
        news = [(k, card(k, p, 0.5, False)) for k, p in pile.items()]
        self.play(FadeOut(junk), *[ReplacementTransform(self.sp[i], n) for i, (k, n) in enumerate(news)], run_time=1.0)
        for k, n in news:
            self.cd[k] = n
        self.morph([(k, STRIP[k], 0.5, False) for k in ORDER], rt=1.3, extra=(FadeOut(mic),))
        lens = Ellipse(width=9.4, height=3.7, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.06).move_to([1.6, 0.2, 0])
        mlab = T("microscope", 28, TEAL).move_to([1.6, 1.55, 0])
        self.play(Create(lens), FadeIn(mlab), run_time=1.0)
        cols = [-1.3, 1.6, 4.5]
        self.at("does each")
        i1 = icon_nuc().move_to([cols[0], 0.55, 0])
        l1 = T("nucleus?", 28).move_to([cols[0], -0.45, 0])
        self.play(FadeIn(i1, scale=0.6), FadeIn(l1, shift=UP * 0.1), run_time=0.7)
        self.at("the part")
        self.play(i1[1].animate.scale(1.5), run_time=0.5)
        self.play(i1[1].animate.scale(1 / 1.5), run_time=0.5)
        self.at("which cell")
        i2 = icon_parts().move_to([cols[1], 0.55, 0])
        l2 = T("cell parts?", 28).move_to([cols[1], -0.45, 0])
        self.play(FadeIn(i2, scale=0.6), FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        self.at("does it have one")
        i3 = icon_many().move_to([cols[2], 0.55, 0])
        l3 = T("one or many?", 28).move_to([cols[2], -0.45, 0])
        self.play(FadeIn(i3, scale=0.6), FadeIn(l3, shift=UP * 0.1), run_time=0.7)
        self.at("a fourth")
        tag = chip("other tests", GOLD, 22).move_to([5.6, -2.35, 0])
        self.play(FadeIn(tag, shift=LEFT * 0.2), run_time=0.7)
        self.at("does it make")
        i4 = icon_sunleaf().move_to([0.0, -2.35, 0])
        orr = T("or", 28).move_to([1.6, -2.35, 0])
        i5 = icon_mouth().move_to([3.2, -2.35, 0])
        l4 = T("makes food or takes it in?", 28).move_to([1.6, -3.45, 0])
        self.play(FadeIn(i4, scale=0.6), FadeIn(l4, shift=UP * 0.1), run_time=0.7)
        self.at("take food")
        self.play(FadeIn(orr), FadeIn(i5, scale=0.6), run_time=0.7)
        self.finish()


def strip_end(sc):
    L = lad_scene(sc, 1)
    for k in ORDER:
        sc.put(k, STRIP[k], 0.5, False)
    return L


class S05Split(Film):
    def construct(self):
        L = strip_end(self)
        big = icon_nuc(2.2).move_to([1.6, 0.3, 0])
        bl = T("nucleus?", 40).move_to([1.6, -1.6, 0])
        self.play(FadeIn(big, scale=0.5), FadeIn(bl), run_time=0.8)
        self.at("splits the")
        div = Line([1.55, 3.3, 0], [1.55, -3.3, 0], stroke_color=GOLD, stroke_width=5)
        self.play(Create(div), run_time=0.9)
        self.at("four of them")
        hl = T("nucleus", 32).move_to([-1.15, 2.7, 0])
        left = {"mush": (-2.3, 0.9), "oak": (0.0, 0.9), "deer": (-2.3, -1.5), "para": (0.0, -1.5)}
        self.play(FadeOut(big), FadeOut(bl), run_time=0.5)
        self.morph([(k, p, 0.8, True) for k, p in left.items()], rt=1.6)
        self.play(FadeIn(hl), run_time=0.4)
        self.at("the bacterium and")
        hr = T("no nucleus", 32).move_to([4.4, 2.7, 0])
        self.morph([("bact", (3.2, 0.9), 0.8, True), ("arch", (5.6, 0.9), 0.8, True)], rt=1.4)
        self.play(FadeIn(hr), run_time=0.4)
        self.at("under the")
        c1 = cellc(0.7).move_to([3.2, -1.6, 0])
        c2 = cellc(0.7).move_to([5.6, -1.6, 0])
        sch = T("schematic", 22).move_to([4.4, -2.85, 0])
        self.play(FadeIn(c1, scale=0.5), FadeIn(c2, scale=0.5), FadeIn(sch), run_time=0.9)
        self.play(Indicate(c1, color=GOLD, scale_factor=1.1), Indicate(c2, color=GOLD, scale_factor=1.1), run_time=1.0)
        self.finish()


def check_row(y, txt):
    return T(txt, 28).move_to([1.65, y, 0])


class S06Mushroom(Film):
    def construct(self):
        L = lad_scene(self, 1)
        self.put("mush", (-2.3, 0.9))
        self.put("oak", (0.0, 0.9))
        self.play(self.cd["oak"].animate.move_to([5.3, 0.9, 0]), run_time=0.6)
        mc = (-1.9, 0.2)
        mcell = cellc(1.1, BG, PURPLE)
        mcell.wall.set_stroke(opacity=0)
        mcell.move_to([*mc, 0])
        self.play(ReplacementTransform(self.cd["mush"], mcell.mem), run_time=self.beat(0.12))
        t1 = T("mushroom cell", 28).move_to([-1.9, -1.95, 0])
        self.play(FadeIn(t1), run_time=0.5)
        ocell = cellc(1.1, GOLD, OAKG)
        ocell.move_to([5.3, 0.2, 0])
        self.at("its cells")
        nuc = Circle(radius=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.85).move_to([mc[0], mc[1] + 0.35, 0])
        r1 = check_row(1.15, "nucleus")
        self.play(GrowFromCenter(nuc), FadeIn(r1), run_time=0.7)
        self.play(FadeIn(tick(-0.2, 1.15)), run_time=0.4)
        self.at("and a cell")
        mwall = Circle(radius=1.23, stroke_color=GOLD, stroke_width=7).move_to([*mc, 0])
        r2 = check_row(0.1, "cell wall")
        self.play(Create(mwall), FadeIn(r2), run_time=0.9)
        self.play(FadeIn(tick(-0.2, 0.1)), run_time=0.4)
        self.at("like a")
        onuc = Circle(radius=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.85).move_to([5.3, 0.55, 0])
        t2 = T("oak leaf cell", 28).move_to([5.2, -1.95, 0])
        self.play(ReplacementTransform(self.cd["oak"], ocell), FadeIn(onuc), FadeIn(t2), run_time=1.0)
        self.play(FadeIn(tick(3.6, 1.15)), FadeIn(tick(3.6, 0.1)), run_time=0.5)
        self.at("but they have")
        r3 = check_row(-0.95, "chloroplasts")
        self.play(FadeIn(r3), run_time=0.5)
        pos = [(-0.4, -0.35), (0.4, -0.35), (0.0, -0.75)]
        chl = VGroup(*[Ellipse(width=0.5, height=0.28, stroke_width=0, fill_color=CHLO, fill_opacity=1).move_to([5.3 + dx, 0.2 + dy, 0]) for dx, dy in pos])
        redc = DashedVMobject(Circle(radius=0.3, color=RED, stroke_width=6), num_dashes=10).move_to([mc[0], mc[1] - 0.6, 0])
        self.play(FadeIn(chl, scale=0.6), Create(redc), FadeIn(nogo(-0.2, -0.95)), FadeIn(tick(3.6, -0.95)), run_time=1.0)
        self.at("the green parts")
        self.play(Indicate(chl, color=CHLO, scale_factor=1.25), run_time=1.2)
        sch = T("schematic", 22).move_to([1.65, -3.2, 0])
        self.play(FadeIn(sch), Indicate(chl, color=CHLO, scale_factor=1.25), run_time=1.2)
        self.finish()


class S07Feed(Film):
    def construct(self):
        L = lad_scene(self, 1)
        log = RoundedRectangle(width=9.6, height=3.0, corner_radius=0.3, stroke_color=WOOD_L, stroke_width=3,
                               fill_color=BROWN, fill_opacity=0.55).move_to([1.65, -1.0, 0])
        mush = art_mush(PURPLE_L, TEXT).set_height(2.3).move_to([1.65, 0.5 + 1.15, 0])
        a = np.array([1.65, 0.45, 0])
        ends = [(-1.4, -0.9), (0.0, -1.8), (1.65, -2.1), (3.3, -1.7), (4.9, -0.9)]
        hy = VGroup(*[CubicBezier(a, a + np.array([(e[0] - 1.65) * 0.1, -1.0, 0]), np.array([e[0] - (e[0] - 1.65) * 0.25, e[1] + 0.9, 0]),
                                  np.array([e[0], e[1], 0]), stroke_color=PURPLE_L, stroke_width=5) for e in ends])
        self.play(FadeIn(log), FadeIn(mush, shift=UP * 0.3), run_time=1.0)
        sway(mush, 0.03, 3.0)
        self.play(Create(hy), run_time=2.2)
        self.at("it releases")
        drops = VGroup(*[Dot(radius=0.11, color=PURPLE_L).move_to([e[0] + dx, e[1] + dy, 0]) for e in ends for dx, dy in [(0.15, 0.1), (-0.15, -0.1)]])
        self.play(FadeIn(drops, scale=0.4), run_time=0.8)
        rng = np.random.RandomState(3)
        self.play(*[d.animate.shift([rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3), 0]) for d in drops], run_time=3.0)
        self.at("they break")
        dots = VGroup(*[Dot(radius=0.05, color=WOOD_L).move_to([rng.uniform(-2.3, 5.6), rng.uniform(-2.3, -0.2), 0]) for _ in range(40)])
        self.play(log.animate.set_fill(BROWN, 0.12), FadeIn(dots, scale=0.3), FadeOut(drops), run_time=2.0)
        self.at("and the mushroom takes")
        tgt = []
        for d in dots:
            best = min((hy[i].point_from_proportion(t) for i in range(5) for t in np.linspace(0.3, 1, 8)), key=lambda p: np.linalg.norm(p - d.get_center()))
            tgt.append(best)
        self.play(LaggedStart(*[d.animate.move_to(p).set_opacity(0) for d, p in zip(dots, tgt)], lag_ratio=0.03), run_time=2.2)
        self.at("most plants")
        self.play(FadeOut(log), FadeOut(mush), FadeOut(hy), FadeOut(dots), run_time=0.6)
        pbox = RoundedRectangle(width=5.2, height=4.8, corner_radius=0.2, stroke_color=OAKG, stroke_width=4, fill_color=OAKG, fill_opacity=0.07).move_to([-0.6, 0.15, 0])
        plab = T("Plants", 32).move_to([-0.6, 1.95, 0])
        m = card("mush", (0.7, 0.3), 0.8)
        o = card("oak", (-1.9, 0.3), 0.8)
        self.cd = {"mush": m, "oak": o}
        self.play(FadeIn(pbox), FadeIn(plab), FadeIn(m, shift=UP * 0.2), FadeIn(o, shift=UP * 0.2), run_time=0.9)
        bob(m)
        bob(o, ph=2)
        food = icon_sunleaf().move_to([-0.6, -1.3, 0])
        ftxt = T("makes own food", 28).move_to([-0.6, -1.85, 0])
        self.play(FadeIn(food, scale=0.6), FadeIn(ftxt), run_time=0.8)
        self.at("so the mushroom slides")
        fbox = RoundedRectangle(width=3.4, height=4.8, corner_radius=0.2, stroke_color=PURPLE_L, stroke_width=4, fill_color=PURPLE, fill_opacity=0.12).move_to([3.7, 0.15, 0])
        flab = T("Fungi", 32).move_to([3.7, 1.95, 0])
        pbox2 = RoundedRectangle(width=3.4, height=4.8, corner_radius=0.2, stroke_color=OAKG, stroke_width=4, fill_color=OAKG, fill_opacity=0.07).move_to([-0.5, 0.15, 0])
        self.play(ReplacementTransform(pbox, pbox2), plab.animate.move_to([-0.5, 1.95, 0]), FadeIn(fbox), FadeIn(flab),
                  m.animate.move_to([3.7, 0.3, 0]), o.animate.move_to([-0.5, 0.3, 0]), food.animate.move_to([-0.5, -1.3, 0]),
                  ftxt.animate.move_to([-0.5, -1.85, 0]), run_time=1.8)
        self.at("later")
        tag = T("later: kingdom Fungi", 28, PURPLE_L).move_to([3.7, -2.95, 0])
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.8)
        self.finish()


def bact_arch_row(sc, pos_b, pos_a, s, cy, r):
    sc.put("bact", pos_b, s)
    sc.put("arch", pos_a, s)
    c1 = cellc(r).move_to([pos_b[0], cy, 0])
    c2 = cellc(r).move_to([pos_a[0], cy, 0])
    sc.add(c1, c2)
    return c1, c2


class S08Chem(Film):
    def construct(self):
        L = lad_scene(self, 1)
        c1, c2 = bact_arch_row(self, (3.2, 0.9), (5.6, 0.9), 0.8, -1.6, 0.7)
        go_rung(self, L, 2, 0.8)
        self.morph([("bact", (1.5, 1.3), 0.9, True), ("arch", (4.9, 1.3), 0.9, True)], rt=1.4,
                   extra=(c1.animate.scale(0.8 / 0.7).move_to([1.5, -1.2, 0]), c2.animate.scale(0.8 / 0.7).move_to([4.9, -1.2, 0])))
        self.at("the bacterium and")
        mag = VGroup(Circle(radius=0.85, stroke_color=GOLD, stroke_width=8), Line([0.6, -0.6, 0], [1.3, -1.3, 0], stroke_color=GOLD, stroke_width=10))
        mag.move_to([1.5, -1.2, 0])
        sch = T("schematic", 22).move_to([3.2, -2.75, 0])
        self.play(FadeIn(mag, scale=0.6), FadeIn(sch), run_time=0.6)
        self.play(mag.animate.move_to([4.9, -1.2, 0]), run_time=2.2)
        self.at("under a")
        self.play(mag.animate.move_to([1.5, -1.2, 0]), run_time=1.8)
        self.play(FadeOut(mag), run_time=0.4)
        self.at("are they")
        q = chip("Same kind?", GOLD, 34).move_to([-1.55, 0.0, 0])
        self.play(FadeIn(q, shift=RIGHT * 0.3), run_time=0.8)
        self.play(q[0].animate.set_fill(GOLD, 0.4), run_time=0.6)
        self.finish()


def s08_end(sc):
    L = lad_scene(sc, 2)
    c1, c2 = bact_arch_row(sc, (1.5, 1.3), (4.9, 1.3), 0.9, -1.2, 0.8)
    q = chip("Same kind?", GOLD, 34).move_to([-1.55, 0.0, 0])
    q[0].set_fill(GOLD, 0.4)
    sc.add(q)
    sch = T("schematic", 22).move_to([3.2, -2.75, 0])
    sc.add(sch)
    return L, c1, c2, q, sch


class S09Pause(Film):
    def construct(self):
        L, c1, c2, q, sch = s08_end(self)
        ring0 = Circle(radius=0.4, stroke_color=GREY, stroke_width=5).move_to([6.0, -3.1, 0])
        arc = Arc(radius=0.4, start_angle=PI / 2, angle=-TAU, stroke_color=GOLD, stroke_width=8).move_to([6.0, -3.1, 0])
        self.add(ring0)
        self.play(Create(arc), run_time=self.narration_s - 0.4, rate_func=linear)
        self.finish()


def gene_strip(pattern, col):
    return VGroup(*[Square(side_length=0.3, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=1 if b else 0.0) for b in pattern]).arrange(RIGHT, buff=0.06)


class S10Reveal(Film):
    def construct(self):
        L, c1, c2, q, sch = s08_end(self)
        self.play(Transform(q, chip("No", RED, 40).move_to(q.get_center())), run_time=0.8)
        self.at("the chemicals")
        lab = T("different chemicals", 28).move_to([3.2, -3.55, 0])
        self.play(FadeOut(sch), FadeIn(lab), c1.wall.animate.set_stroke(ORANGE, 9), c1.mem.animate.set_fill(ORANGE, 0.75).set_stroke(ORANGE),
                  c2.wall.animate.set_stroke(CRIMSON, 9), c2.mem.animate.set_fill(CRIMSON, 0.75).set_stroke(CRIMSON), run_time=2.4)
        sc2 = T("schematic", 22).move_to([3.2, -2.8, 0])
        self.play(FadeIn(sc2), FadeOut(q), run_time=0.6)
        self.at("their genes")
        s1 = gene_strip([1, 1, 0, 1, 0, 1], ORANGE).move_to([1.5, -2.6, 0])
        s2 = gene_strip([0, 1, 1, 0, 1, 0], CRIMSON).move_to([4.9, -2.6, 0])
        lab2 = T("genes differ (top rung)", 28).move_to([3.2, -3.55, 0])
        self.play(FadeOut(lab), FadeOut(sc2), FadeIn(s1, shift=UP * 0.2), FadeIn(s2, shift=UP * 0.2), FadeIn(lab2),
                  L.rungs[3][0].animate.set_stroke(GOLD, 6).set_fill(GOLD, 0.5), run_time=1.0)
        self.play(L.rungs[3][0].animate.set_stroke(GREY, 3).set_fill(GREY, 0.1), run_time=1.0)
        self.at("so scientists split")
        bb = RoundedRectangle(width=3.1, height=5.9, corner_radius=0.2, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.06).move_to([1.5, -0.2, 0])
        ba = RoundedRectangle(width=3.1, height=5.9, corner_radius=0.2, stroke_color=CRIMSON, stroke_width=4, fill_color=CRIMSON, fill_opacity=0.06).move_to([4.9, -0.2, 0])
        self.play(Create(bb), Create(ba), FadeOut(lab2), run_time=1.4)
        self.at("bacteria")
        tb = T("Bacteria", 34).move_to([1.5, 3.25, 0])
        self.play(FadeIn(tb, shift=DOWN * 0.1), run_time=0.5)
        self.at("archaea")
        ta = T("Archaea", 34).move_to([4.9, 3.25, 0])
        self.play(FadeIn(ta, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


def dom_groups(sc):
    """Rebuild the end of s10 as two groups (Bacteria, Archaea)."""
    L = lad_scene(sc, 2)
    out = []
    for key, x, col in [("bact", 1.5, ORANGE), ("arch", 4.9, CRIMSON)]:
        box = RoundedRectangle(width=3.1, height=5.9, corner_radius=0.2, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.06).move_to([x, -0.2, 0])
        lab = T("Bacteria" if key == "bact" else "Archaea", 34).move_to([x, 3.25, 0])
        cd = card(key, (x, 1.3), 0.9)
        cl = cellc(0.8, col, col)
        cl.mem.set_fill(col, 0.75)
        cl.move_to([x, -1.2, 0])
        st = gene_strip([1, 1, 0, 1, 0, 1] if key == "bact" else [0, 1, 1, 0, 1, 0], col).move_to([x, -2.6, 0])
        g = VGroup(box, lab, cd, cl, st)
        g.box, g.lab = box, lab
        sc.add(g)
        out.append(g)
    return L, out


def kingdom_slots():
    return {"mush": (2.85, 1.05), "oak": (5.25, 1.05), "deer": (2.85, -1.8), "para": (5.25, -1.8)}


class S11Three(Film):
    def construct(self):
        L, (gb, ga) = dom_groups(self)
        self.at("every living")
        self.play(gb[2][3].animate.set_opacity(0), ga[2][3].animate.set_opacity(0), gb.animate.scale(0.7).move_to([-2.25, -0.2, 0]), ga.animate.scale(0.7).move_to([0.15, -0.2, 0]), run_time=1.6)
        slots = kingdom_slots()
        cards = {k: card(k, (p[0], p[1] - 0.25), 0.55, False) for k, p in slots.items()}
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cards.values()], lag_ratio=0.25), run_time=1.6)
        for c in cards.values():
            bob(c, ph=hash(c.key) % 7)
        self.at("in a third")
        ebox = RoundedRectangle(width=5.2, height=6.0, corner_radius=0.2, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.06).move_to([4.05, -0.3, 0])
        self.play(Create(ebox), run_time=1.2)
        self.at("eukarya")
        et = T("Eukarya", 34).move_to([4.05, 3.25, 0])
        self.play(FadeIn(et, shift=DOWN * 0.1), run_time=0.6)
        self.at("so life")
        boxes = [gb.box, ga.box, ebox]
        self.play(*[b.animate.set_stroke(GOLD, 8) for b in boxes], run_time=0.5)
        self.play(*[b.animate.set_stroke(c, 4) for b, c in zip(boxes, [ORANGE, CRIMSON, TEAL])], run_time=0.5)
        self.at("kingdoms sit")
        kcol = {"mush": PURPLE_L, "oak": OAKG, "deer": BROWN}
        kb = {}
        for k in ["mush", "oak", "deer"]:
            kb[k] = RoundedRectangle(width=2.3, height=2.7, corner_radius=0.15, stroke_color=kcol[k], stroke_width=4, fill_color=kcol[k], fill_opacity=0.08).move_to([*slots[k], 0])
            self.play(Create(kb[k]), run_time=0.7)
            self.wait(0.3)
        for k, ph, nm in [("mush", "fungi plants", "Fungi"), ("oak", "plants and", "Plants"), ("deer", "animals are", "Animals")]:
            self.at(ph)
            self.play(FadeIn(T(nm, 28).move_to([slots[k][0], slots[k][1] + 1.0, 0]), shift=DOWN * 0.1), run_time=0.5)
        self.at("the paramecium")
        q = T("?", 60, GOLD).move_to([slots["para"][0] + 0.9, slots["para"][1] + 0.9, 0])
        self.play(Indicate(cards["para"], color=GOLD, scale_factor=1.2), FadeIn(q, scale=0.5), run_time=1.0)
        self.at("you will")
        self.play(q.animate.scale(1.4), run_time=0.5)
        self.play(q.animate.scale(1 / 1.4), run_time=0.5)
        self.finish()


def mini(c, x, y, s=0.46):
    return Square(side_length=s, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x, y, 0])


class S12Rule(Film):
    def construct(self):
        L = lad_scene(self, 2)
        cx = [-1.85, 1.5, 4.85]
        frames = [RoundedRectangle(width=3.1, height=3.4, corner_radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, -0.1, 0]) for x in cx]
        caps = [T(t, 28).move_to([x, -2.2, 0]) for t, x in zip(["eyes", "microscope", "cell chemistry"], cx)]
        # thumbnails: coordinates are relative to each frame centre (y offset -0.1)
        y0 = -0.1
        t1 = VGroup(mine := mini(PURPLE, cx[0] - 0.75, y0 + 0.85), mini(OAKG, cx[0] - 0.15, y0 + 0.85), mini(BROWN, cx[0] + 0.95, y0 + 0.85),
                    Line([cx[0] - 1.05, y0 + 0.5, 0], [cx[0] + 0.15, y0 + 0.5, 0], stroke_color=OAKG, stroke_width=5),
                    Line([cx[0] + 0.65, y0 + 0.5, 0], [cx[0] + 1.25, y0 + 0.5, 0], stroke_color=BROWN, stroke_width=5),
                    *[Dot(radius=0.09, color=c).move_to([cx[0] + dx, y0 - 0.9, 0]) for dx, c in [(-0.3, TEALC), (0.0, ORANGE), (0.3, CRIMSON)]])
        t2 = VGroup(mini(PURPLE, cx[1] - 0.95, y0 + 0.85), mini(OAKG, cx[1] - 0.35, y0 + 0.85), mini(BROWN, cx[1] - 0.95, y0 + 0.25), mini(TEALC, cx[1] - 0.35, y0 + 0.25),
                    Line([cx[1] + 0.2, y0 + 1.3, 0], [cx[1] + 0.2, y0 - 1.3, 0], stroke_color=GOLD, stroke_width=4),
                    mini(ORANGE, cx[1] + 0.85, y0 + 0.85), mini(CRIMSON, cx[1] + 0.85, y0 + 0.25))
        t3 = VGroup(mini(ORANGE, cx[2] - 1.0, y0 + 0.85), mini(CRIMSON, cx[2] - 1.0, y0 + 0.25),
                    Rectangle(width=1.7, height=2.3, stroke_color=TEAL, stroke_width=3).move_to([cx[2] + 0.5, y0 + 0.1, 0]),
                    mini(PURPLE, cx[2] + 0.2, y0 + 0.85), mini(OAKG, cx[2] + 0.8, y0 + 0.85), mini(BROWN, cx[2] + 0.2, y0 + 0.25), mini(TEALC, cx[2] + 0.8, y0 + 0.25))
        self.at("look back")
        for f, t, cp in zip(frames, [t1, t2, t3], caps):
            self.play(FadeIn(f), FadeIn(t, shift=UP * 0.1), FadeIn(cp), run_time=0.8)
            self.wait(0.5)
        self.at("the evidence")
        txt = T("same living things, new evidence", 36).move_to([1.5, 3.3, 0])
        self.play(FadeIn(txt, shift=DOWN * 0.1), run_time=0.8)
        self.at("new evidence")
        p1 = np.array([cx[0] - 0.75, y0 + 1.15, 0])
        p2 = np.array([cx[2] + 0.2, y0 + 1.15, 0])
        arrow = CurvedArrow(p1, p2, angle=-1.0, color=PURPLE_L, stroke_width=8)
        self.play(Create(arrow), run_time=1.8)
        self.play(Indicate(mine, color=PURPLE_L, scale_factor=1.5), run_time=1.0)
        self.finish()


class S13Dna(Film):
    def construct(self):
        L = lad_scene(self, 2)
        go_rung(self, L, 3, 0.8)
        self.put("mush", (1.6, 1.9), 0.9)
        self.put("oak", (-0.5, -1.9), 0.9)
        self.put("deer", (3.7, -1.9), 0.9)
        self.at("scientists compare")
        strips = [gene_strip([1, 0, 1, 1, 0], PURPLE_L).move_to([3.8, 1.9, 0]),
                  gene_strip([1, 1, 0, 1, 0], OAKG).move_to([-2.8, -1.9, 0]),
                  gene_strip([1, 0, 1, 0, 0], BROWN).move_to([5.85, -1.9, 0])]
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in strips], lag_ratio=0.4), run_time=2.2)
        self.at("will the")
        l1 = DashedLine([1.2, 0.65, 0], [-0.2, -0.6, 0], stroke_color=GOLD, stroke_width=6)
        q1 = T("?", 60, GOLD).move_to([-0.2, -0.05, 0]).shift(LEFT * 0.5)
        self.at("oaks or")
        self.play(Create(l1), FadeIn(q1, scale=0.5), run_time=1.0)
        l2 = DashedLine([2.0, 0.65, 0], [3.4, -0.6, 0], stroke_color=GOLD, stroke_width=6)
        q2 = T("?", 60, GOLD).move_to([3.4, -0.05, 0]).shift(RIGHT * 0.5)
        self.at("deers more")
        self.play(Create(l2), FadeIn(q2, scale=0.5), run_time=1.0)
        self.play(q1.animate.scale(1.3), q2.animate.scale(1.3), run_time=0.5)
        self.play(q1.animate.scale(1 / 1.3), q2.animate.scale(1 / 1.3), run_time=0.5)
        self.finish()


class S14End(EndCard):
    LINE = "New evidence can move a living thing to a new group."
