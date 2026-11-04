"""Four Factors, Three Kinases (chapter 2 of "Neurotrophins, Trk Receptors and p75")

COLOR MAP (shared with every chapter of this lesson; taken from scenes.old.py, plus SAND for this chapter)
  BLUE   = the neurotrophin (NGF, BDNF, NT-3, NT-4): the dimer, its name chips
  PALE   = a binding face / contact patch on the neurotrophin (light blue)
  PINK   = Trk receptors (TrkA, TrkB, TrkC), their binding domains and kinase domains
  VIOLET = p75
  SAND   = adaptor proteins that dock on phosphotyrosines (new here: teal was too close to the factor blue)
  GREEN  = survival (the two survival branches, the "on" state of a neuron)
  GREY   = membrane, cells, outlines, unknowns, zone labels
  TEXT   = phosphate badges ("P"), tyrosine slots, question marks and the final statement
  (ORANGE pro-domain, YELLOW sortilin, GOLD cutting enzymes, RED death are not used in this chapter.)

Every shape is a labelled cartoon: no molecular structures. The "structure views" are blocks with a PDB tag.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
VIOLET = "#A98BE0"
PALE = "#CFEFFA"
SAND = "#E3B777"

K = 1.4       # scale of the receptor-pair scenes
MYP = 0.6     # membrane height in the receptor-pair scenes
MY1 = -0.5    # membrane height in the first four scenes
D1 = 2.0      # scale of the dimer in the first scene
DB = 4.2      # scale of the big dimer in the dimer close-up (s04)
LX = -3.3     # x of the "outside" / "inside" labels (they sit next to the membrane at the receptor)


# ---------------------------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------------------------
def membrane(y, h=0.5, w=13.2):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, y, 0])


def tint(my):
    """the cell interior below the membrane (a faint tint)."""
    top = my - 0.25
    return Rectangle(width=13.2, height=top + 3.75, stroke_width=0, fill_color=GREY,
                     fill_opacity=0.12).move_to([0, top - (top + 3.75) / 2, 0])


def lab(text, color, x, y, size=28):
    return T(text, size, color).move_to([x, y, 0])


def two_lines(a, b, size, color):
    return VGroup(T(a, size, color), T(b, size, color)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)


def schip(text, color, size=28, pad=0.22):
    """a chip with an opaque background (so a line behind it does not show through)."""
    c = chip(text, color, size, pad=pad)
    bg = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                          fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(bg, c)


def dimer(cx, cy, k=1.0):
    h1, h2 = [Ellipse(width=1.0 * k, height=0.85 * k, stroke_color=BLUE, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.5).move_to([cx + s * 0.5 * k, cy, 0]) for s in (-1, 1)]
    f1, f2 = [Ellipse(width=0.2 * k, height=0.55 * k, stroke_width=0, fill_color=PALE,
                      fill_opacity=0.95).move_to([cx + s * 0.93 * k, cy, 0]) for s in (-1, 1)]
    g = VGroup(h1, h2, f1, f2)
    g.halves = VGroup(h1, h2)
    g.faces = VGroup(f1, f2)
    return g


def badge(pos, k=K):
    c = Circle(radius=max(0.2 * k, 0.3), stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(c, T("P", 26, TEXT)).move_to(pos)


def bracket(x, y1, y2, color, dx=0.2, side=1):
    m = VMobject(stroke_color=color, stroke_width=4)
    m.set_points_as_corners([[x, y1, 0], [x + side * dx, y1, 0], [x + side * dx, y2, 0], [x, y2, 0]])
    return m


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


class Rec:
    """A TrkA cartoon: two binding domains outside, a membrane-spanning bar, a kinase domain inside
    (with one empty tyrosine slot on it). `kin_x` lets the kinase hang away from the receptor's axis."""

    def __init__(self, cx, my, k=1.0, kin_x=None, marks=False):
        self.k, self.cx, self.my = k, cx, my

        def blob(w, h, y):
            return Ellipse(width=w * k, height=h * k, stroke_color=PINK, stroke_width=3,
                           fill_color=PINK, fill_opacity=0.45).move_to([cx, my + y * k, 0])
        self.lo, self.up = blob(1.0, 0.85, 0.85), blob(1.0, 0.85, 1.65)
        self.tm = RoundedRectangle(corner_radius=0.12 * k, width=0.26 * k, height=0.8 * k, stroke_color=PINK,
                                   stroke_width=3, fill_color=PINK, fill_opacity=0.8).move_to([cx, my, 0])
        kx = cx if kin_x is None else kin_x
        self.kb = Ellipse(width=1.3 * k, height=1.0 * k, stroke_color=PINK, stroke_width=3,
                          fill_color=PINK, fill_opacity=0.45).move_to([kx, my - 1.05 * k, 0])
        self.kin = VGroup(self.kb)
        self.mk = None
        if marks:
            self.add_mark()
        self.stalk = Line(self.tm.get_bottom(), self.kb.get_top(), color=PINK, stroke_width=6)
        self.stalk.add_updater(lambda m: m.put_start_and_end_on(self.tm.get_bottom(), self.kb.get_top()))
        self.items = [self.stalk, self.lo, self.up, self.tm, self.kin]

    def add_mark(self):
        """the empty tyrosine slot on the kinase domain (drawn only once the story needs it)."""
        self.mk = Square(side_length=0.22 * self.k, stroke_color=TEXT, stroke_width=2, fill_color=BG,
                         fill_opacity=1).move_to(self.kb.get_bottom() + UP * 0.02)
        self.kin.add(self.mk)
        return self.mk

    def group(self):
        return VGroup(*self.items)

    def badge_pos(self):
        return self.kb.get_bottom() + DOWN * 0.25 * self.k


class Pair:
    """membrane + dimer + two receptors in one of three states: apart, docked, swung (kinases side by side)."""

    def __init__(self, state="docked", my=MYP, k=K, apart_x=4.6, marks=False):
        self.my, self.k = my, k
        x = apart_x if state == "apart" else 1.52 * k
        kx = 0.72 * k if state == "swung" else None
        self.mem = membrane(my)
        self.dim = dimer(0, my + 0.85 * k, k)
        self.L = Rec(-x, my, k, kin_x=None if kx is None else -kx, marks=marks)
        self.R = Rec(x, my, k, kin_x=kx, marks=marks)

    @property
    def items(self):
        return [self.mem] + list(self.dim) + self.L.items + self.R.items

    def add_to(self, scene, faces=True):
        scene.add(self.mem, *self.dim.halves, *(self.dim.faces if faces else []), *self.L.items, *self.R.items)


def adaptor(c, k=K):
    r = 0.42 * k
    bowl = Sector(radius=r, start_angle=PI, angle=PI, arc_center=[c[0], c[1], 0], stroke_color=SAND,
                  stroke_width=3, fill_color=SAND, fill_opacity=0.55)
    body = RoundedRectangle(corner_radius=0.1 * k, width=0.5 * k, height=0.45 * k, stroke_color=SAND,
                            stroke_width=3, fill_color=SAND, fill_opacity=0.55)
    body.move_to([c[0], c[1] - r - 0.2 * k, 0])
    return VGroup(body, bowl)


def neuron(cx, cy, r=1.6, variant="A"):
    cell = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([cx, cy, 0])
    recs = []
    for deg in (55, 90, 125):
        a = np.radians(deg)
        u = np.array([np.cos(a), np.sin(a), 0.0])
        base = np.array([cx, cy, 0.0]) + u * r
        stalk = Line(base, base + u * 0.6, color=PINK, stroke_width=5)
        if variant == "A":
            tip = Ellipse(width=0.55, height=0.55, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.5)
        else:
            tip = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.5, stroke_color=PINK, stroke_width=3,
                                   fill_color=PINK, fill_opacity=0.5).rotate(a - PI / 2)
        tip.move_to(base + u * 0.88)
        recs.append(VGroup(stalk, tip))
    g = VGroup(cell, *recs)
    g.cell, g.recs = cell, VGroup(*recs)
    g.cx, g.cy, g.r = cx, cy, r
    return g


def neuron_on(scene, n, label_holder, run_time=0.5):
    """light a neuron up: green outline and tint, an 'on' label, receptors brighter."""
    on = lab("on", GREEN, n.cx, n.cy, 36)
    label_holder.append(on)
    scene.play(n.cell.animate.set_stroke(GREEN).set_fill(GREEN, 0.3), FadeIn(on),
               *[r[1].animate.set_fill(PINK, 0.95) for r in n.recs], run_time=run_time)


def pulse(group, color=None, sf=1.12):
    """Indicate every member of a group on its own (Indicate on a group would scale the members' spacing too)."""
    kw = {} if color is None else {"color": color}
    return [Indicate(m, scale_factor=sf, **kw) for m in group]


def chain_dots(p0, p1, ts, r=0.12):
    return VGroup(*[Dot(p0 + t * (p1 - p0), radius=r, color=GREEN) for t in ts])


def grow_dot(pos, r=0.15):
    """a green dot that keeps pulsing at the end of a line: the line is still growing, not unfinished."""
    d = Dot(pos, radius=r, color=GREEN)
    d.clk = 0.0

    def upd(m, dt):
        m.clk += dt
        m.set_width(2 * r * (1 + 0.45 * np.sin(m.clk * 6.0)))
        m.move_to(pos)
    d.add_updater(upd)
    return d


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "Four Factors, Three Kinases"


def stage_labels(outside=True):
    out_l = lab("outside", GREY, LX, MY1 + 0.55, 26)
    in_l = lab("inside", GREY, LX, MY1 - 0.55, 26)
    return out_l, in_l


class S01(SpokenScene):
    def construct(self):
        mem, cell = membrane(MY1), tint(MY1)
        out_l, in_l = stage_labels()
        dim = dimer(0, 2.8, D1)
        ngf = lab("NGF", BLUE, 0, 2.2, 40)
        q = lab("?", GREY, 0, -2.0, 190)
        # the membrane comes in with its "inside" label; the factor waits above it
        self.play(FadeIn(mem), FadeIn(cell), FadeIn(in_l), FadeIn(dim.halves), run_time=0.5)
        self.at("lands")
        self.play(dim.halves.animate.move_to([0, MY1 + 0.25 + 0.425 * D1 + 0.06, 0]), run_time=1.0)
        self.at("outside")
        self.play(FadeIn(ngf), FadeIn(out_l), run_time=0.4)
        self.at("how does", lead=0.5)
        self.play(GrowFromCenter(q), run_time=0.6)
        self.at("inside")
        self.play(Indicate(q, color=TEXT, scale_factor=1.1), Indicate(in_l, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        mem, cell = membrane(MY1), tint(MY1)
        out_l, in_l = stage_labels()
        dim = dimer(0, MY1 + 0.25 + 0.425 * D1 + 0.06, D1)
        ngf = lab("NGF", BLUE, 0, 2.2, 40)
        q = lab("?", GREY, 0, -2.0, 190)
        self.add(mem, cell, out_l, in_l, dim.halves, ngf, q)
        self.at("start")
        self.play(FadeOut(dim.halves), FadeOut(ngf), FadeOut(q), run_time=0.5)
        self.at("the receptor")
        r = Rec(0, MY1, 1.6)
        self.play(LaggedStart(FadeIn(r.kin, shift=UP * 0.2), FadeIn(r.stalk), FadeIn(r.tm),
                              FadeIn(r.lo, shift=DOWN * 0.2), FadeIn(r.up, shift=DOWN * 0.2), lag_ratio=0.25),
                  run_time=1.3)
        self.at("a track receptor")
        name = lab("TrkA", PINK, -1.7, MY1 + 1.6 * 1.25, 32)
        self.play(FadeIn(name), run_time=0.4)
        self.at("sits in")
        self.play(Indicate(mem, color=GREY, scale_factor=1.04), run_time=0.8)
        self.finish()


def s03_base():
    mem, cell = membrane(MY1), tint(MY1)
    out_l, in_l = stage_labels()
    r = Rec(0, MY1, 1.6)
    name = lab("TrkA", PINK, -1.7, MY1 + 1.6 * 1.25, 32)
    return mem, cell, out_l, in_l, r, name


class S03(SpokenScene):
    def construct(self):
        mem, cell, out_l, in_l, r, name = s03_base()
        self.add(mem, cell, out_l, in_l, *r.items, name)
        y_top = r.up.get_top()[1]
        y_bot = r.lo.get_bottom()[1]
        self.at("outside")
        b1 = bracket(r.lo.get_right()[0] + 0.2, y_bot, y_top, PINK)
        self.play(Create(b1), Indicate(out_l, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("binds")
        l1 = T("binding domain", 30, PINK).next_to(b1, RIGHT, buff=0.25)
        self.play(FadeIn(l1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("inside")
        b2 = bracket(r.kb.get_right()[0] + 0.15, r.kb.get_bottom()[1], r.kb.get_top()[1], PINK)
        b2.move_to([b2.get_center()[0], r.kb.get_center()[1], 0])
        self.play(Create(b2), Indicate(in_l, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("tyrosine kinase")
        l2 = two_lines("tyrosine kinase", "domain", 30, PINK).next_to(b2, RIGHT, buff=0.25)
        self.play(FadeIn(l2, shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        # the last scene's picture, rebuilt only so that it can fade out while the big dimer fades in
        mem, cell, out_l, in_l, r, name = s03_base()
        b1 = bracket(r.lo.get_right()[0] + 0.2, r.lo.get_bottom()[1], r.up.get_top()[1], PINK)
        l1 = T("binding domain", 30, PINK).next_to(b1, RIGHT, buff=0.25)
        b2 = bracket(r.kb.get_right()[0] + 0.15, r.kb.get_bottom()[1], r.kb.get_top()[1], PINK)
        b2.move_to([b2.get_center()[0], r.kb.get_center()[1], 0])
        l2 = two_lines("tyrosine kinase", "domain", 30, PINK).next_to(b2, RIGHT, buff=0.25)
        self.add(mem, cell, out_l, in_l, *r.items, name, b1, l1, b2, l2)
        d = dimer(0, 0.1, DB)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(d.halves, scale=0.9), run_time=0.8)
        self.at("each neurotrophin")
        ngf = lab("NGF", BLUE, 0, 2.7, 40)
        self.play(FadeIn(ngf), run_time=0.4)
        self.at("a dimer")
        # the dimer turns right round, so both ends are seen
        self.play(Rotate(d.halves, angle=PI, axis=UP, run_time=1.1))
        self.at("two binding")
        tags = VGroup(*[lab(f"face {i + 1}", PALE, s * 3.9, -2.75, 30) for i, s in enumerate((-1, 1))])
        arrows = VGroup(*[arr([s * 3.9, -2.3, 0], [s * 3.9, -1.2, 0], PALE, 4, 0.18) for s in (-1, 1)])
        self.play(FadeIn(d.faces), FadeIn(tags), *[GrowArrow(a) for a in arrows], run_time=0.5)
        self.play(*pulse(d.faces, PALE, 1.4), run_time=0.7)
        self.finish()


def question_text():
    return lab("What can it do to two receptors at once?", TEXT, 0, -3.1, 32)


class S05(SpokenScene):
    def construct(self):
        d = dimer(0, 0.1, DB)
        ngf = lab("NGF", BLUE, 0, 2.7, 40)
        tags = VGroup(*[lab(f"face {i + 1}", PALE, s * 3.9, -2.75, 30) for i, s in enumerate((-1, 1))])
        arrows = VGroup(*[arr([s * 3.9, -2.3, 0], [s * 3.9, -1.2, 0], PALE, 4, 0.18) for s in (-1, 1)])
        self.add(d, ngf, tags, arrows)
        P = Pair("apart", MYP, K)
        self.at("a dimer")
        # a zoom-out: the same dimer shrinks to its place above the membrane
        self.play(d.animate.scale(K / DB).move_to([0, MYP + 0.85 * K, 0]), FadeOut(ngf), FadeOut(tags),
                  FadeOut(arrows), FadeIn(P.mem), run_time=1.0)
        self.at("two faces")
        self.play(*pulse(d.faces, PALE, 1.6), run_time=0.7)
        self.at("what can it")
        q = question_text()
        for rc, s in ((P.L, -1), (P.R, 1)):
            rc.group().shift(RIGHT * 1.0 * -s)
        self.play(FadeIn(P.L.group()), FadeIn(P.R.group()), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("to two receptors")
        self.play(P.L.group().animate.shift(LEFT * 1.0), P.R.group().animate.shift(RIGHT * 1.0), run_time=1.5,
                  rate_func=smooth)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        P = Pair("apart", MYP, K)
        P.add_to(self)
        self.add(question_text())
        think = lab("pause and think", GREY, 0, 3.15, 28)
        self.play(FadeIn(think), run_time=0.4)
        # a slow pulse on the two faces tells the viewer this is a pause, not a frozen picture
        while self.elapsed() < 4.2:
            self.play(*pulse(P.dim.faces, PALE, 1.5), run_time=1.0)
            self.wait(0.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        P = Pair("apart", MYP, K)
        P.add_to(self)
        # grips: pale lines from each binding face out to the receptor's lower binding domain
        gl = Line(P.dim.faces[0].get_left(), P.L.lo.get_right(), color=PALE, stroke_width=7)
        gr = Line(P.dim.faces[1].get_right(), P.R.lo.get_left(), color=PALE, stroke_width=7)
        gl.add_updater(lambda m: m.put_start_and_end_on(P.dim.faces[0].get_left(), P.L.lo.get_right()))
        gr.add_updater(lambda m: m.put_start_and_end_on(P.dim.faces[1].get_right(), P.R.lo.get_left()))
        self.at("hold two")
        self.play(Create(gl), Create(gr), *pulse(P.dim.faces, PALE, 1.6), run_time=0.9)
        self.at("at once")
        self.play(Indicate(P.L.lo, color=PINK, scale_factor=1.15), Indicate(P.R.lo, color=PINK, scale_factor=1.15),
                  run_time=0.5)
        self.at("bring them")
        dx = 4.6 - 1.52 * K
        self.play(P.L.group().animate.shift(RIGHT * dx), P.R.group().animate.shift(LEFT * dx),
                  run_time=1.1, rate_func=smooth)
        gl.clear_updaters()
        gr.clear_updaters()
        self.play(FadeOut(gl), FadeOut(gr), *pulse(P.dim.faces, PALE, 1.5), run_time=0.4)
        self.finish()


# the "structure view": the four blobs redrawn big inside a box (taller than the cartoon blobs, so they fill it)
SVW, SVH, SVY = 2.7, 3.3, 0.1


def sv_shapes():
    def blob(cx, color, op):
        return Ellipse(width=SVW, height=SVH, stroke_color=color, stroke_width=3, fill_color=color,
                       fill_opacity=op).move_to([cx, SVY, 0])
    big = VGroup(blob(-3.95, PINK, 0.45), blob(-1.3, BLUE, 0.5), blob(1.3, BLUE, 0.5), blob(3.95, PINK, 0.45))
    faces = VGroup(*[Ellipse(width=0.5, height=1.5, stroke_width=0, fill_color=PALE,
                             fill_opacity=0.95).move_to([s * 2.65, SVY, 0]) for s in (-1, 1)])
    return big, faces


def sv_frame_tag():
    frame = RoundedRectangle(corner_radius=0.25, width=12.6, height=6.3, stroke_color=GREY, stroke_width=3).move_to([0, 0, 0])
    tag = VGroup(T("crystal structure", 26, GREY), M("PDB 1WWW", 26, GREY)).arrange(RIGHT, buff=0.4).move_to([0, 2.6, 0])
    return frame, tag


def sv_labels():
    dl = lab("NGF dimer", BLUE, 0, -2.35, 30)
    tl = VGroup(*[lab("TrkA domain", PINK, s * 3.95, -2.35, 30) for s in (-1, 1)])
    return dl, tl


class S08(SpokenScene):
    def construct(self):
        P = Pair("docked", MYP, K)
        others = [P.mem, P.L.stalk, P.R.stalk, P.L.tm, P.R.tm, P.L.kin, P.R.kin, P.L.up, P.R.up]
        small = VGroup(P.L.lo, P.dim.halves[0], P.dim.halves[1], P.R.lo)
        self.add(*others, small, P.dim.faces)
        big, bfaces = sv_shapes()
        frame, tag = sv_frame_tag()
        dl, tl = sv_labels()
        self.at("a crystal")
        # the box comes in with its label, and the four blobs grow into it
        self.play(*[FadeOut(m) for m in others], ReplacementTransform(small, big),
                  ReplacementTransform(P.dim.faces, bfaces), Create(frame), FadeIn(tag), run_time=1.3)
        self.at("ngf")
        self.play(FadeIn(dl), run_time=0.4)
        self.at("two track")
        self.play(LaggedStart(*[FadeIn(t) for t in tl], lag_ratio=0.3), run_time=0.7)
        self.at("one on")
        self.play(Indicate(big[0], color=PINK, scale_factor=1.08), run_time=0.7)
        self.at("each side")
        self.play(Indicate(big[3], color=PINK, scale_factor=1.08), run_time=0.7)
        self.finish()


def add_badges(P):
    bl = badge(P.L.badge_pos(), K)
    br = badge(P.R.badge_pos(), K)
    return bl, br


class S09(SpokenScene):
    def construct(self):
        P = Pair("docked", MYP, K)
        others = [P.mem, P.L.stalk, P.R.stalk, P.L.tm, P.R.tm, P.L.kin, P.R.kin, P.L.up, P.R.up]
        small = VGroup(P.L.lo, P.dim.halves[0], P.dim.halves[1], P.R.lo)
        big, bfaces = sv_shapes()
        frame, tag = sv_frame_tag()
        dl, tl = sv_labels()
        # start from the structure view of the last scene, then step back out to the cell
        self.add(frame, tag, dl, tl, big, bfaces)
        self.play(FadeOut(frame), FadeOut(tag), FadeOut(dl), FadeOut(tl), ReplacementTransform(big, small),
                  ReplacementTransform(bfaces, P.dim.faces), *[FadeIn(m) for m in others], run_time=0.6)
        self.at("kinase")
        self.play(Indicate(P.L.kb, color=PINK, scale_factor=1.15), Indicate(P.R.kb, color=PINK, scale_factor=1.15), run_time=0.6)
        self.at("side by side")
        d = 0.72 * K - 1.52 * K
        self.play(P.L.kin.animate.shift(RIGHT * (-d)), P.R.kin.animate.shift(LEFT * (-d)), run_time=1.3, rate_func=smooth)
        self.at("phosphorylate")
        mL, mR = P.L.add_mark(), P.R.add_mark()
        self.play(FadeIn(mL, scale=0.3), FadeIn(mR, scale=0.3), run_time=0.25)
        bl, br = add_badges(P)
        srcL, srcR = P.L.kb.get_center(), P.R.kb.get_center()
        dstL, dstR = P.L.badge_pos(), P.R.badge_pos()
        bl.move_to(srcL).scale(0.4)
        br.move_to(srcR).scale(0.4)
        self.add(bl, br)
        # each kinase puts a phosphate on the OTHER kinase's tyrosine: the two curved arrows cross
        a_lr = ArcBetweenPoints(srcL + DOWN * 0.1, dstR, angle=PI / 1.7)
        a_rl = ArcBetweenPoints(srcR + DOWN * 0.1, dstL, angle=-PI / 1.7)
        a_lr.set_stroke(TEXT, 4)
        a_rl.set_stroke(TEXT, 4)
        a_lr.add_tip(tip_length=0.22)
        a_rl.add_tip(tip_length=0.22)
        self.play(Create(a_lr), Create(a_rl), MoveAlongPath(bl, a_lr), MoveAlongPath(br, a_rl),
                  run_time=0.8, rate_func=smooth)
        self.play(bl.animate.scale(2.5).move_to(dstR), br.animate.scale(2.5).move_to(dstL),
                  FadeOut(a_lr), FadeOut(a_rl), run_time=0.3)
        self.at("on tyrosines")
        tl2 = lab("tyrosines", TEXT, 0, -3.0, 30)
        ln = VGroup(*[Line([s * 0.4, -2.7, 0], [x, -2.3, 0], color=GREY, stroke_width=3)
                      for s, x in ((-1, P.L.badge_pos()[0]), (1, P.R.badge_pos()[0]))])
        self.play(FadeIn(tl2), FadeIn(ln), run_time=0.4)
        self.finish()


def swung_world(scene, with_badges=True, with_adaptors=False):
    P = Pair("swung", MYP, K, marks=True)
    P.add_to(scene)
    extras = []
    ads = []
    if with_adaptors:
        ads = [adaptor(P.L.badge_pos(), K), adaptor(P.R.badge_pos(), K)]
        scene.add(*ads)
    if with_badges:
        bl, br = add_badges(P)
        scene.add(bl, br)
        extras += [bl, br]
    return P, extras, ads


def adaptor_label():
    """beside the adaptor it names, with a leader line (not at the bottom edge)."""
    t = lab("adaptor proteins", SAND, 3.95, -2.45, 30)
    ln = Line([2.1, -2.45, 0], [1.45, -2.45, 0], color=SAND, stroke_width=3)
    return VGroup(t, ln)


class S10(SpokenScene):
    def construct(self):
        P, (bl, br), _ = swung_world(self)
        self.at("docking sites")
        self.play(bl.animate.scale(1.4), br.animate.scale(1.4), run_time=0.35)
        self.play(bl.animate.scale(1 / 1.4), br.animate.scale(1 / 1.4), run_time=0.35)
        self.at("proteins")
        ads = [adaptor(P.L.badge_pos(), K), adaptor(P.R.badge_pos(), K)]
        al = adaptor_label()
        self.play(*[FadeIn(a, shift=UP * 1.0) for a in ads], FadeIn(al), run_time=1.0)
        self.bring_to_front(bl, br)
        self.finish()


TOPY = 2.8   # membrane height once the view has panned down into the cell (S11 on)
SHIFT = TOPY - MYP

_CH = chip("Ras", GREEN, 28)
CHIP_HW = {n: chip(n, GREEN, 28).width / 2 for n in ("Ras", "ERK", "PI3K", "Akt")}
CHIP_HH = _CH.height / 2


def panned_world(scene):
    """the receptor pair as it stands after the view pans down: the outside is gone, the inside fills the frame."""
    P, (bl, br), ads = swung_world(scene, True, True)
    for m in [*P.dim.halves, *P.dim.faces, P.L.lo, P.R.lo, P.L.up, P.R.up]:
        scene.remove(m)
    movers = [P.mem, P.L.stalk, P.R.stalk, P.L.tm, P.R.tm, P.L.kin, P.R.kin, bl, br, *ads]
    return P, bl, br, ads, movers


def branch_geometry(ads):
    """start points under the adaptors, chip centres, and the points where each line meets its chip's edge."""
    sl = ads[0].get_bottom() + DOWN * 0.05
    sr = ads[1].get_bottom() + DOWN * 0.05
    el = np.array([-4.5, -2.7, 0.0])
    er = np.array([4.5, -2.7, 0.0])
    xl = edge_of(el, sl, CHIP_HW["ERK"], CHIP_HH)
    xr = edge_of(er, sr, CHIP_HW["Akt"], CHIP_HH)
    return sl, sr, el, er, xl, xr


def edge_of(center_pt, toward, half_w=0.6, half_h=0.37):
    """where a straight line from `toward` enters a chip centred at center_pt."""
    d = toward - center_pt
    d = d / np.linalg.norm(d)
    t = min(half_w / max(abs(d[0]), 1e-6), half_h / max(abs(d[1]), 1e-6))
    return center_pt + d * t


class S11(SpokenScene):
    def construct(self):
        P, (bl, br), ads = swung_world(self, True, True)
        al = adaptor_label()
        self.add(al)
        out = [*P.dim.halves, *P.dim.faces, P.L.lo, P.R.lo, P.L.up, P.R.up]
        movers = [P.mem, P.L.stalk, P.R.stalk, P.L.tm, P.R.tm, P.L.kin, P.R.kin, bl, br, *ads]
        self.at("start")
        # the view pans down into the cell: the outside (and the dimer) slide up and fade out on purpose
        self.play(*[m.animate.shift(UP * SHIFT).set_opacity(0) for m in out], FadeOut(al),
                  *[m.animate.shift(UP * SHIFT) for m in movers], run_time=1.0, rate_func=smooth)
        sl, sr, el, er, xl, xr = branch_geometry(ads)
        self.at("survival")
        lL = Line(sl, xl, color=GREEN, stroke_width=5, stroke_opacity=0.5)
        lR = Line(sr, xr, color=GREEN, stroke_width=5, stroke_opacity=0.5)
        self.play(Create(lL), Create(lR), run_time=1.0)
        dl, dr = grow_dot(xl), grow_dot(xr)
        self.add(dl, dr)
        self.finish()


def pan_state(scene):
    P, bl, br, ads, movers = panned_world(scene)
    for m in movers:
        m.shift(UP * SHIFT)
    sl, sr, el, er, xl, xr = branch_geometry(ads)
    lL = Line(sl, xl, color=GREEN, stroke_width=5, stroke_opacity=0.5)
    lR = Line(sr, xr, color=GREEN, stroke_width=5, stroke_opacity=0.5)
    scene.add(lL, lR)
    return P, ads, lL, lR, sl, sr, el, er, xl, xr


class S12(SpokenScene):
    def construct(self):
        P, ads, lL, lR, sl, sr, el, er, xl, xr = pan_state(self)
        dl, dr = grow_dot(xl), grow_dot(xr)
        self.add(dl, dr)
        self.at("one runs")
        self.play(lL.animate.set_stroke(opacity=1, width=7), run_time=0.4)
        self.at("ras")
        ras = schip("Ras", GREEN, 28).move_to(sl + 0.30 * (el - sl))
        self.play(FadeIn(ras, scale=0.8), run_time=0.35)
        dots = chain_dots(sl, xl, [0.60, 0.68, 0.76])
        self.at("to")
        erk = schip("ERK", GREEN, 28).move_to(el)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), FadeIn(erk, scale=0.8),
                  FadeOut(dl), run_time=0.6)
        self.finish()


def branch_chips(sl, sr, el, er, xl):
    ras = schip("Ras", GREEN, 28).move_to(sl + 0.30 * (el - sl))
    dots = chain_dots(sl, xl, [0.60, 0.68, 0.76])
    erk = schip("ERK", GREEN, 28).move_to(el)
    pi3k = schip("PI3K", GREEN, 28).move_to(sr + 0.30 * (er - sr))
    akt = schip("Akt", GREEN, 28).move_to(er)
    return ras, dots, erk, pi3k, akt


def survival_bits(erk, akt):
    surv = schip("survival", GREEN, 34).move_to([0, -3.2, 0])
    a1 = arr(erk.get_right() + RIGHT * 0.08 + DOWN * 0.08, surv.get_left() + LEFT * 0.08, GREEN, 5, 0.2)
    a2 = arr(akt.get_left() + LEFT * 0.08 + DOWN * 0.08, surv.get_right() + RIGHT * 0.08, GREEN, 5, 0.2)
    return surv, a1, a2


class S13(SpokenScene):
    def construct(self):
        P, ads, lL, lR, sl, sr, el, er, xl, xr = pan_state(self)
        # the left branch stays lit from the last scene
        lL.set_stroke(opacity=1, width=7)
        ras, dots, erk, pi3k, akt = branch_chips(sl, sr, el, er, xl)
        dr = grow_dot(xr)
        self.add(ras, dots, erk, dr)
        self.at("the other")
        self.play(lR.animate.set_stroke(opacity=1, width=7), run_time=0.4)
        self.at("from p")
        self.play(FadeIn(pi3k, scale=0.8), run_time=0.35)
        self.at("to")
        self.play(FadeIn(akt, scale=0.8), FadeOut(dr), run_time=0.4)
        self.wait(0.15)
        surv, a1, a2 = survival_bits(erk, akt)
        self.play(FadeIn(surv), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.finish()


# four labelled factors for the puzzle card: (x, y, name)
DIMERS4 = [(1.3, -0.1, "NGF"), (4.2, -0.1, "BDNF"), (1.3, -2.0, "NT-4"), (4.2, -2.0, "NT-3")]


def puzzle_card():
    box = RoundedRectangle(corner_radius=0.25, width=10.6, height=2.1, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.1).move_to([0, 2.6, 0])
    t1 = T("PUZZLE 1", 26, GREY).move_to([0, 3.25, 0])
    t2 = T("Which factor is mine?", 56, TEXT, font=TITLE_FONT).move_to([0, 2.3, 0])
    return VGroup(box, t1, t2)


def dimer_with_name(x, y, name):
    d = dimer(x, y, 1.15)
    nm = lab(name, BLUE, x, y - 0.8, 28)
    return d, nm


class S14(SpokenScene):
    def construct(self):
        P, ads, lL, lR, sl, sr, el, er, xl, xr = pan_state(self)
        for l in (lL, lR):
            l.set_stroke(opacity=1, width=7)
        ras, dots, erk, pi3k, akt = branch_chips(sl, sr, el, er, xl)
        surv, a1, a2 = survival_bits(erk, akt)
        self.add(ras, dots, erk, pi3k, akt, surv, a1, a2)
        card = puzzle_card()
        fs = [dimer_with_name(x, y, nm) for x, y, nm in DIMERS4]
        # "Now back": the old picture gives way, the card and the four named factors come in together
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        n = neuron(-3.6, -1.0, 1.9, "A").cell
        qm = lab("?", TEXT, -3.6, -1.0, 120)
        self.play(FadeIn(card, shift=DOWN * 0.15), FadeIn(n), FadeIn(qm),
                  LaggedStart(*[AnimationGroup(FadeIn(d.halves, scale=0.8), FadeIn(nm)) for d, nm in fs],
                              lag_ratio=0.25), run_time=1.3)
        self.at("how does a neuron")
        self.play(Indicate(qm, color=TEXT, scale_factor=1.2), run_time=0.6)
        self.at("which factor")
        self.play(LaggedStart(*[AnimationGroup(*pulse(d.halves, BLUE, 1.2)) for d, nm in fs], lag_ratio=0.15), run_time=1.0)
        self.finish()


TABLE_X0 = -6.0
ROWS4 = [2.9, 1.2, -0.5, -2.2]
TRK_X = 4.5
TRK_Y = [2.9, 0.35, -2.2]


def table_parts():
    names = ["NGF", "BDNF", "NT-4", "NT-3"]
    fs = [chip(n, BLUE, 34) for n in names]
    for f, y in zip(fs, ROWS4):
        f.move_to([TABLE_X0 + f.width / 2, y, 0])
    rs = [chip(n, PINK, 34).move_to([TRK_X, y, 0]) for n, y in zip(["TrkA", "TrkB", "TrkC"], TRK_Y)]
    pairs = [(0, 0, 0.0), (1, 1, 0.13), (2, 1, -0.13), (3, 2, 0.0)]
    arrows = [arr(fs[i].get_right() + RIGHT * 0.15, rs[j].get_left() + LEFT * 0.15 + UP * off, BLUE, 5)
              for i, j, off in pairs]
    return fs, rs, arrows


def table_caption():
    return lab("4 factors, 3 Trk kinases", TEXT, 0, -3.3, 32)


class S15(SpokenScene):
    def construct(self):
        # carry: the puzzle card, neuron and four factors from the last scene; they give way to the table
        card = puzzle_card()
        n = neuron(-3.6, -1.0, 1.9, "A").cell
        qm = lab("?", TEXT, -3.6, -1.0, 120)
        fs0 = [dimer_with_name(x, y, nm) for x, y, nm in DIMERS4]
        self.add(card, n, qm, *[VGroup(d.halves, nm) for d, nm in fs0])
        self.at("each")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        fs, rs, arrows = table_parts()
        self.at("neurotrophin")
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in fs], lag_ratio=0.3), run_time=1.0)
        self.at("particular")
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rs], lag_ratio=0.25), run_time=0.8)
        self.at("track receptors")
        self.play(FadeIn(table_caption(), shift=UP * 0.1), run_time=0.5)
        self.finish()


def dashed_arrow(a, b, color=BLUE, w=5, dash=0.18):
    a, b = np.array(a, float), np.array(b, float)
    u = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - u * 0.15, color=color, stroke_width=w, dash_length=dash)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.16)
    tip.rotate(np.arctan2(u[1], u[0]) - PI / 2).move_to(b - u * 0.14)
    return VGroup(line, tip)


class S16(SpokenScene):
    def construct(self):
        fs, rs, arrows = table_parts()
        cap = table_caption()
        self.add(*fs, *rs, cap)
        self.at("ngf")
        self.play(GrowArrow(arrows[0]), Indicate(fs[0], color=BLUE), Indicate(rs[0], color=PINK), run_time=0.9)
        self.at("bdnf")
        self.play(GrowArrow(arrows[1]), Indicate(fs[1], color=BLUE), Indicate(rs[1], color=PINK), run_time=0.9)
        self.at("nt4")
        self.play(GrowArrow(arrows[2]), Indicate(fs[2], color=BLUE), Indicate(rs[1], color=PINK), run_time=0.9)
        self.at("nt3")
        self.play(GrowArrow(arrows[3]), Indicate(fs[3], color=BLUE), Indicate(rs[2], color=PINK), run_time=0.9)
        self.at("activates")
        # the three strong arrows step back so the weaker ones read clearly
        self.play(*[a.animate.set_opacity(0.18) for a in arrows[:3]], run_time=0.5)
        start = fs[3].get_corner(UR) + RIGHT * 0.08 + UP * 0.04
        dA = dashed_arrow(start, rs[0].get_bottom() + DOWN * 0.08)
        dB = dashed_arrow(start, rs[1].get_bottom() + DOWN * 0.08 + LEFT * 0.35)
        self.at("track a", nth=1)
        self.play(Create(dA[0]), FadeIn(dA[1]), Indicate(rs[0], color=PINK, scale_factor=1.2), run_time=0.9)
        self.at("and track b")
        self.play(Create(dB[0]), FadeIn(dB[1]), Indicate(rs[1], color=PINK, scale_factor=1.2), run_time=0.7)
        self.at("more")
        wk = schip("weaker", BLUE, 30, pad=0.12).move_to(dA[0].get_center())
        self.play(FadeIn(wk), run_time=0.4)
        self.finish()


# s17: one NGF half against the TrkA domain
NG_C, DOM_C = np.array([-1.9, -0.3, 0.0]), np.array([1.9, -0.2, 0.0])


def s17_shapes():
    ngf = Ellipse(width=3.8, height=5.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4).move_to(NG_C)
    dom = Ellipse(width=3.8, height=5.4, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.4).move_to(DOM_C)
    nl = lab("NGF", BLUE, -1.9, -1.2, 44)
    dl = two_lines("TrkA", "domain", 32, PINK).move_to([1.9, -1.2, 0])
    return ngf, dom, nl, dl


def s17_patch():
    patch = Ellipse(width=0.5, height=1.3, stroke_width=0, fill_color=PALE, fill_opacity=0.95).move_to([0.0, -0.25, 0])
    pl = lab("contact surface", PALE, 0, -3.45, 28)
    ln = Line([0, -3.2, 0], [0, -0.9, 0], color=PALE, stroke_width=3)
    return patch, pl, ln


def s17_tail():
    tail = RoundedRectangle(corner_radius=0.14, width=1.5, height=0.3, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.8).move_to([-0.2, 1.6, 0])
    tip = Ellipse(width=0.4, height=0.5, stroke_width=0, fill_color=PALE, fill_opacity=0.95).move_to([0.5, 1.6, 0])
    al = lab("amino terminus", BLUE, -0.1, 3.2, 30)
    ln = Line([-0.1, 2.95, 0], [-0.1, 1.8, 0], color=BLUE, stroke_width=3)
    return tail, tip, al, ln


class S17(SpokenScene):
    def construct(self):
        ngf, dom, nl, dl = s17_shapes()
        patch, pl, pln = s17_patch()
        tail, tip, al, aln = s17_tail()
        # picture is up from the first frame (cross-faded from the last scene's table)
        fs, rs, arrows = table_parts()
        for a in arrows[:3]:
            a.set_opacity(0.18)
        start = fs[3].get_corner(UR) + RIGHT * 0.08 + UP * 0.04
        dA = dashed_arrow(start, rs[0].get_bottom() + DOWN * 0.08)
        dB = dashed_arrow(start, rs[1].get_bottom() + DOWN * 0.08 + LEFT * 0.35)
        wk = schip("weaker", BLUE, 30, pad=0.12).move_to(dA[0].get_center())
        old = [*fs, *rs, *arrows, table_caption(), dA, dB, wk]
        self.add(*old)
        self.play(*[FadeOut(m) for m in old], FadeIn(ngf), FadeIn(dom), FadeIn(nl), FadeIn(dl), run_time=0.8)
        self.at("contact surfaces")
        self.play(FadeIn(patch, scale=0.4), FadeIn(pl), Create(pln), run_time=0.7)
        self.play(Indicate(patch, color=PALE, scale_factor=1.3), run_time=0.7)
        self.at("the factor's")
        self.play(GrowFromEdge(tail, LEFT), run_time=0.5)
        self.play(FadeIn(tip, scale=0.4), run_time=0.3)
        self.at("amino")
        self.play(FadeIn(al), Create(aln), Indicate(tip, color=PALE, scale_factor=1.5), run_time=0.6)
        self.finish()


def panel(cx, ref):
    """one structure panel: four taller blobs (TrkA domain, NGF/NT half, half, domain) inside a box."""
    frame = RoundedRectangle(corner_radius=0.25, width=6.5, height=5.4, stroke_color=GREY, stroke_width=3).move_to([cx, 0, 0])
    by = 0.2

    def blob(dx, color, op):
        return Ellipse(width=1.4, height=2.4, stroke_color=color, stroke_width=3, fill_color=color,
                       fill_opacity=op).move_to([cx + dx, by, 0])
    lo = [blob(-2.1, PINK, 0.45), blob(2.1, PINK, 0.45)]
    halves = VGroup(blob(-0.7, BLUE, 0.5), blob(0.7, BLUE, 0.5))
    faces = VGroup(*[Ellipse(width=0.3, height=1.0, stroke_width=0, fill_color=PALE,
                             fill_opacity=0.95).move_to([cx + s * 1.4, by, 0]) for s in (-1, 1)])
    pdb = M(ref, 26, GREY).move_to([cx, 2.3, 0])
    return frame, halves, faces, lo, pdb


def pair_label(fname, rname, x, y):
    return VGroup(T(fname, 34, BLUE), T("with", 26, GREY), T(rname, 34, PINK)).arrange(RIGHT, buff=0.25).move_to([x, y, 0])


class S18(SpokenScene):
    def construct(self):
        # carry: the last scene's picture cross-fades straight into the first structure panel
        ngf, dom, nl, dl = s17_shapes()
        patch, pl, pln = s17_patch()
        tail, tip, al, aln = s17_tail()
        old = [ngf, dom, nl, dl, patch, pl, pln, tail, tip, al, aln]
        self.add(*old)
        fa, ha, fca, loa, pa = panel(-3.35, "PDB 1WWW")
        la = pair_label("NGF", "TrkA", -3.35, -2.0)
        self.play(*[FadeOut(m) for m in old], Create(fa), FadeIn(ha), FadeIn(fca),
                  *[FadeIn(b) for b in loa], FadeIn(pa), FadeIn(la), run_time=0.8)
        self.at("same")
        self.play(*pulse(ha), *[Indicate(m, scale_factor=1.06) for m in loa], run_time=0.35)
        self.at("another pair")
        fb, hb, fcb, lob, pb = panel(3.35, "PDB 1HCF")
        self.play(Create(fb), FadeIn(hb), FadeIn(fcb), *[FadeIn(b) for b in lob], run_time=0.8)
        self.at("nt4")
        lb = pair_label("NT-4", "TrkB", 3.35, -2.0)
        self.play(FadeIn(lb), run_time=0.4)
        self.at("with track b")
        self.play(FadeIn(pb), run_time=0.4)
        self.finish()


def two_neurons(variant_right="C"):
    nA = neuron(-3.5, -0.9, 1.9, "A")
    nC = neuron(3.5, -0.9, 1.9, variant_right)
    return nA, nC


def neuron_labels():
    return lab("TrkA", PINK, -3.5, -3.45, 34), lab("TrkC", PINK, 3.5, -3.45, 34)


def slots(n):
    """where a factor chip sits when it is held by each of a neuron's three receptors (left, top, right)."""
    out = []
    for deg in (125, 90, 55):
        a = np.radians(deg)
        out.append(np.array([n.cx, n.cy, 0.0]) + np.array([np.cos(a), np.sin(a), 0.0]) * (n.r + 1.5))
    return out


class S19(SpokenScene):
    def construct(self):
        nA, nC = two_neurons()
        self.at("so the answer")
        recs = [(r, np.array(r[0].get_end()) - np.array(r[0].get_start())) for n in (nA, nC) for r in n.recs]
        la, lc = neuron_labels()
        self.play(FadeIn(nA.cell), FadeIn(nC.cell), FadeIn(la), FadeIn(lc),
                  LaggedStart(*[FadeIn(r, shift=d * 0.8) for r, d in recs], lag_ratio=0.1), run_time=1.2)
        self.at("track receptor")
        self.play(*pulse(nA.recs, PINK, 1.15), *pulse(nC.recs, PINK, 1.15), run_time=0.7)
        self.at("makes")
        self.play(Indicate(la, color=PINK, scale_factor=1.2), Indicate(lc, color=PINK, scale_factor=1.2), run_time=0.6)
        self.finish()


def factor_chip(name, p):
    return chip(name, BLUE, 26, pad=0.15).move_to([p[0], p[1], 0])


class S20(SpokenScene):
    def construct(self):
        nA, nC = two_neurons()
        la, lc = neuron_labels()
        self.add(nA, nC, la, lc)
        sA = slots(nA)
        mine = [factor_chip("NGF", [x, 3.45]) for x in (-5.6, -3.5, -1.4)]
        away = [factor_chip("NGF", [x, 3.45]) for x in (2.2, 4.8)]
        # NGF reaches both cells at once; only the TrkA cell's receptors take hold of it
        self.play(*[FadeIn(c, shift=DOWN * 0.2) for c in mine + away], run_time=0.4)
        self.at("makes")
        self.play(*[c.animate.move_to(p) for c, p in zip(mine, sA)],
                  *[c.animate.shift(RIGHT * 3.4).set_opacity(0) for c in away],
                  *pulse(nA.recs, PINK, 1.15), run_time=1.0)
        self.at("switched on")
        holder = []
        neuron_on(self, nA, holder, 0.5)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        nA, nC = two_neurons()
        la, lc = neuron_labels()
        self.add(nA, nC, la, lc)
        sC = slots(nC)
        mine = [factor_chip("NT-3", [x, 3.45]) for x in (1.4, 3.5, 5.6)]
        self.play(*[FadeIn(c, shift=DOWN * 0.2) for c in mine], run_time=0.4)
        self.at("makes")
        self.play(*[c.animate.move_to(p) for c, p in zip(mine, sC)], *pulse(nC.recs, PINK, 1.15), run_time=1.0)
        self.at("switched on")
        holder = []
        neuron_on(self, nC, holder, 0.5)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        nA, nC = two_neurons()
        la, lc = neuron_labels()
        self.add(nA, nC, la, lc)
        sA, sC = slots(nA), slots(nC)
        # NGF and NT-3 float over both cells; each binds only at the cell whose receptor fits, the other chips drift on.
        g1, g2 = factor_chip("NGF", [-5.2, 2.9]), factor_chip("NGF", [-1.8, 2.9])
        n1, n2 = factor_chip("NT-3", [1.8, 2.9]), factor_chip("NT-3", [5.2, 2.9])
        gw = factor_chip("NGF", [3.5, 3.45])      # NGF over the TrkC cell: ignored
        nw = factor_chip("NT-3", [-3.5, 3.45])    # NT-3 over the TrkA cell: ignored
        bd = factor_chip("BDNF", [0, 3.45])       # extra passer-by
        allc = (g1, g2, n1, n2, gw, nw, bd)
        self.at("the factor")
        self.play(*[FadeIn(c, shift=DOWN * 0.2) for c in allc], run_time=0.5)
        self.play(g1.animate.shift(RIGHT * 0.4), g2.animate.shift(LEFT * 0.4), n1.animate.shift(RIGHT * 0.4),
                  n2.animate.shift(LEFT * 0.4), gw.animate.shift(RIGHT * 1.6), nw.animate.shift(LEFT * 1.6),
                  bd.animate.shift(DOWN * 2.2), run_time=1.6, rate_func=smooth)
        self.at("the receptor")
        # the receptors sort them: NGF to the TrkA cell, NT-3 to the TrkC cell; the others drift on
        self.play(g1.animate.move_to(sA[0]), g2.animate.move_to(sA[2]), n1.animate.move_to(sC[0]),
                  n2.animate.move_to(sC[2]), gw.animate.shift(RIGHT * 2.5).set_opacity(0),
                  nw.animate.shift(LEFT * 2.5).set_opacity(0), bd.animate.shift(DOWN * 2.5).set_opacity(0),
                  run_time=0.7, rate_func=smooth)
        self.at("sorts")
        self.play(nA.cell.animate.set_stroke(GREEN).set_fill(GREEN, 0.3), nC.cell.animate.set_stroke(GREEN).set_fill(GREEN, 0.3),
                  *[r[1].animate.set_fill(PINK, 0.95) for n in (nA, nC) for r in n.recs], run_time=0.5)
        self.finish()


# s23/s24: NGF with p75 (PDB 1SG1). p75 lies along the side of the dimer; the TrkA site (from 1WWW) is at the ends.
def p75_objs():
    frame = RoundedRectangle(corner_radius=0.25, width=12.4, height=7.2, stroke_color=GREY, stroke_width=3).move_to([0, 0, 0])
    tag = VGroup(T("structure view", 26, GREY), M("PDB 1SG1", 26, GREY)).arrange(RIGHT, buff=0.35).move_to([-3.6, 3.2, 0])
    d = dimer(0, 0.4, 3.4)
    nl = lab("NGF dimer", BLUE, 1.9, 2.55, 30)
    block = RoundedRectangle(corner_radius=0.25, width=7.0, height=1.8, stroke_color=VIOLET, stroke_width=3,
                             fill_color=VIOLET, fill_opacity=0.5).move_to([0, -1.85, 0])
    pl = lab("p75", VIOLET, 0, -1.85, 44)
    patch = Ellipse(width=5.0, height=0.3, stroke_width=0, fill_color=PALE, fill_opacity=0.95).move_to([0, -1.0, 0])
    site = VGroup(lab("p75 site", PALE, 4.9, -0.2, 28), Line([4.0, -0.2, 0], [2.3, -0.95, 0], color=PALE, stroke_width=3))
    ghosts = VGroup(*[Ellipse(width=0.5, height=1.5, stroke_width=0, fill_color=PALE, fill_opacity=0.3).move_to([s * 3.3, 0.4, 0])
                      for s in (-1, 1)])
    gl = VGroup(*[VGroup(VGroup(T("TrkA site", 28, "#D6DBE2"), T("(from 1WWW)", 28, "#D6DBE2")).arrange(DOWN, buff=0.08).move_to([s * 4.55, 2.05, 0]),
                         Line([s * 4.1, 1.45, 0], [s * 3.5, 0.95, 0], color="#D6DBE2", stroke_width=3)) for s in (-1, 1)])
    return frame, tag, d, nl, block, pl, patch, site, ghosts, gl


class S23(SpokenScene):
    def construct(self):
        frame, tag, d, nl, block, pl, patch, site, ghosts, gl = p75_objs()
        # the box, the NGF dimer and its name come in together
        self.play(Create(frame), FadeIn(d.halves), FadeIn(nl), FadeIn(tag), run_time=0.9)
        self.at("p75")
        bp = VGroup(block, pl)
        bp.shift(DOWN * 0.8)
        self.play(FadeIn(bp, shift=UP * 0.3), run_time=0.7)
        self.at("binds")
        self.play(bp.animate.shift(UP * 0.8), run_time=0.7)
        self.play(FadeIn(patch, scale=0.5), run_time=0.4)
        self.at("a site")
        self.play(FadeIn(site), Indicate(patch, color=PALE, scale_factor=1.15), run_time=0.7)
        self.at("different from")
        self.play(FadeIn(ghosts), FadeIn(gl), run_time=0.6)
        self.at("where")
        self.play(*[Indicate(g, color=PALE, scale_factor=1.3) for g in ghosts], run_time=0.7)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        frame, tag, d, nl, block, pl, patch, site, ghosts, gl = p75_objs()
        self.add(frame, tag, d.halves, nl, block, pl, patch, site, ghosts, gl)
        self.at("what it")
        keep = VGroup(block, pl)
        dim = VGroup(d.halves, nl)
        # the picture of NGF with p75 stays behind, dimmed; p75 is enlarged and named
        self.play(FadeOut(patch), FadeOut(site), FadeOut(ghosts), FadeOut(gl), FadeOut(tag),
                  dim.animate.set_opacity(0.25), d.halves.animate.shift(UP * 0.9), nl.animate.shift(UP * 0.5),
                  keep.animate.scale(1.05).move_to([0, -1.7, 0]), run_time=0.7)
        self.at("that binding")
        name = lab("p75: a second kind of receptor", VIOLET, 0, -3.15, 34)
        self.play(FadeIn(name), run_time=0.12)
        q = lab("?", TEXT, 5.1, -1.7, 220)
        self.at("the rest")
        self.play(FadeIn(q), run_time=0.15)
        self.play(Indicate(keep, color=VIOLET, scale_factor=1.06), run_time=0.7)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        # left: the factor pairs two receptors
        k, my = 1.2, 0.3
        cx = -3.4
        mem = Rectangle(width=6.4, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([cx, my, 0])
        d = dimer(cx, my + 0.85 * k, k)
        ax = 1.52 * k + 0.9
        rl, rr = Rec(cx - ax, my, k), Rec(cx + ax, my, k)
        left = VGroup(mem, *d, *rl.items, *rr.items)
        ngf_l = lab("NGF", BLUE, cx, 2.55, 30)
        cap_l = lab("pairs two receptors", TEXT, cx, -3.1, 28)
        # right: a neuron hears the factor whose receptor it makes
        n = neuron(3.4, -0.8, 1.5, "A")
        s = slots(n)
        ngf = factor_chip("NGF", [s[1][0], 3.3])
        bd = factor_chip("BDNF", [5.9, 1.9])
        trk = lab("TrkA", PINK, 3.4, -2.65, 30)
        cap_r = lab("receptor decides", TEXT, 3.4, -3.3, 28)
        # the left diagram is already up when the narrator starts
        self.play(FadeIn(left), FadeIn(ngf_l), run_time=0.6)
        self.at("the factor pairs")
        dx = ax - 1.52 * k
        self.play(rl.group().animate.shift(RIGHT * dx), rr.group().animate.shift(LEFT * dx),
                  *pulse(d.halves, BLUE, 1.1), run_time=0.9, rate_func=smooth)
        self.play(FadeIn(cap_l), run_time=0.4)
        self.at("and the receptor")
        self.play(FadeIn(n), FadeIn(ngf), FadeIn(bd), FadeIn(trk), run_time=0.8)
        self.at("decides which")
        holder = []
        self.play(ngf.animate.move_to(s[1]), bd.animate.shift(RIGHT * 0.3 + UP * 0.2).set_opacity(0.6), run_time=0.7)
        neuron_on(self, n, holder, 0.5)
        self.play(FadeIn(cap_r), run_time=0.4)
        self.finish()


class S26End(EndCard):
    LINE = "The factor pairs two receptors;\nthe receptor decides which factor is heard."
