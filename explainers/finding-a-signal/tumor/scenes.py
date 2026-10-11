"""Finding a signal: a tumor that reaches nerves without touching them (Biochemistrypedia explainer, section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PINK   = the mouse tumor
  BLUE   = the chick embryo (outline)
  PURPLE = the sympathetic ganglion and its nerve fibers
  GOLD   = the chorioallantoic membrane
  ORANGE = blood, and the something soluble the tumor puts into it
  YELLOW = the question being asked (and the contact explanation under test)
  GREEN  = ruled in / the result that holds
  RED    = ruled out
  GREY   = eggshell, labels

No anatomy beyond what the lesson names: the embryo is an oval, the tumor and ganglion are blobs,
nerve fibers are lines, the membrane and eggshell are rings, blood is a set of curves.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F08BB4"
TEAL_G = "#B58CD9"
ORANGE = "#F2994A"

E = np.array([-2.2, -0.1, 0.0])           # centre of the embryo, in every scene
EA, EB = 2.65, 2.05                       # embryo half-width, half-height
GAN = E + np.array([0.3, -0.55, 0])       # ganglion centre
TUM_IN = E + np.array([-1.0, 0.4, 0])     # tumor inside the embryo
PX = 4.35                                 # centre of the right-hand panel
QY = 2.5                                  # the question box
CAMA, CAMB = 3.75, 3.05                   # membrane half sizes
SHA, SHB = 4.05, 3.35


def ep(a, b, deg, c=E):
    r = np.radians(deg)
    return c + np.array([a * np.cos(r), b * np.sin(r), 0])


TUM_CAM = ep(CAMA, CAMB, 5)   # tumor grafted on the membrane (inside it)


def blob(w, h, color, op=0.35):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op)


def qbox(text, color=YELLOW, size=26):
    t = T(text, size, color)
    r = RoundedRectangle(corner_radius=0.14, width=3.7, height=t.height + 0.4, stroke_color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=0.12).move_to([PX, QY, 0])
    return VGroup(r, t.move_to(r))


def tumor(at):
    return blob(0.9, 0.8, PINK, 0.4).move_to(at)


def tum_label(at):
    return T("mouse tumor", 22, PINK).move_to(at)


def fibers():
    ts = TUM_IN + np.array([0.35, -0.2, 0])
    out = VGroup()
    for off in [-0.22, -0.07, 0.08, 0.23]:
        a = GAN + np.array([-0.3, 0.1 + off * 0.6, 0])
        b = ts + np.array([0.0, off * 0.9, 0])
        out.add(ArcBetweenPoints(a, b, angle=0.25, stroke_color=TEAL_G, stroke_width=3.5))
    return out


def ganglion(scale=1.0):
    return blob(0.55, 0.38, TEAL_G, 0.5).move_to(GAN).scale(scale)


def cells():
    return VGroup(*[Dot(GAN + np.array([dx, dy, 0]), radius=0.06, color=TEAL_G) for dx, dy in
                    [(-0.3, 0.1), (-0.1, -0.15), (0.1, 0.12), (0.3, -0.08), (0.0, 0.0), (-0.2, 0.0)]])


def embryo():
    e = Ellipse(width=2 * EA, height=2 * EB, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.06).move_to(E)
    lab = T("chick embryo", 22, BLUE).move_to(E + np.array([0.95, 1.25, 0]))
    return VGroup(e, lab)


def cam():
    return Ellipse(width=2 * CAMA, height=2 * CAMB, stroke_color=GOLD, stroke_width=3.5).move_to(E)


def shell():
    return Ellipse(width=2 * SHA, height=2 * SHB, stroke_color=GREY, stroke_width=5).move_to(E)


def vessels():
    out = VGroup()
    for d in (-78, -52, 105, 160, -30):
        a = ep(CAMA, CAMB, d)
        b = ep(EA, EB, d)
        mid = (a + b) / 2 + np.array([0.12, 0.0, 0])
        out.add(VMobject(stroke_color=ORANGE, stroke_width=4).set_points_smoothly([a, mid, b]))
    return out


def cam_tumor_label():
    t = T("mouse tumor", 22, PINK).move_to([PX, -0.2, 0])
    return t, leader(t.get_left() + LEFT * 0.08, TUM_CAM + RIGHT * 0.45, PINK)


def nts():
    return T("not to scale", 22, GREY).move_to(GAN + np.array([0.0, -0.95, 0]))


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=2)


def memb_labels():
    cl = T("chorioallantoic\nmembrane", 22, GOLD, line_spacing=0.8).move_to([PX, 0.65, 0])
    ld1 = leader(cl.get_left() + LEFT * 0.08, ep(CAMA, CAMB, 40), GOLD)
    sl = T("eggshell", 22, GREY).move_to([3.5, -3.05, 0])
    ld2 = leader(sl.get_left() + LEFT * 0.08, ep(SHA, SHB, -58), GREY)
    return cl, ld1, sl, ld2


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.4):
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Finding a Signal: NGF, EGF and the Bioassay"
    TITLE = "A tumor that reaches nerves without touching"


# ---------------------------------------------------------------------------------------------
class S01Swell(Film):
    """a tumor graft makes the ganglia swell: the question."""

    def construct(self):
        emb = embryo()
        gan = ganglion()
        tum = tumor([3.6, 0.6, 0])
        tl = tum_label([3.6, -0.1, 0])
        self.at("A mouse tumor")
        self.play(FadeIn(emb[0]), FadeIn(emb[1]), FadeIn(tum), FadeIn(tl), run_time=0.7)
        self.at("grafted into")
        self.play(tum.animate.move_to(TUM_IN), tl.animate.move_to(TUM_IN + np.array([0.0, 0.95, 0])), run_time=1.0)
        fib = fibers()
        self.at("own nerve fibers")
        self.play(FadeIn(gan), run_time=0.4)
        self.play(Create(fib), run_time=1.1)
        gl = T("ganglion", 22, TEAL_G).move_to(GAN + np.array([0.0, -0.8, 0]))
        self.at("Sympathetic ganglia")
        self.play(FadeIn(gl), Indicate(gan, color=TEAL_G, scale_factor=1.3), run_time=0.7)

        base = -2.65
        title = T("ganglion size", 24, GREY).move_to([PX, 0.45, 0])
        b1 = Rectangle(width=0.9, height=0.4, stroke_color=TEAL_G, stroke_width=3, fill_color=TEAL_G, fill_opacity=0.25)
        b1.move_to([PX - 0.85, base + 0.2, 0])
        b2 = Rectangle(width=0.9, height=2.4, stroke_color=TEAL_G, stroke_width=3, fill_color=TEAL_G, fill_opacity=0.6)
        b2.move_to([PX + 0.85, base + 1.2, 0])
        l1 = T("control", 22, GREY).move_to([PX - 0.85, base - 0.35, 0])
        l2 = T("graft", 22, GREY).move_to([PX + 0.85, base - 0.35, 0])
        six = T("about 6×", 26, TEAL_G, weight=BOLD).next_to(b2, UP, buff=0.15)
        self.at("about six times")
        self.play(FadeIn(title), FadeIn(b1), FadeIn(l1), FadeIn(l2), run_time=0.4)
        self.play(GrowFromEdge(b2, DOWN), gan.animate.scale(2.4), FadeIn(nts()), run_time=1.0)
        self.play(FadeIn(six), run_time=0.3)
        self.at("cluster of nerve cells")
        self.play(FadeIn(cells()), Transform(gl, T("cluster of\nnerve cells", 22, TEAL_G, line_spacing=0.8).move_to(E + np.array([1.3, 0.55, 0]))), run_time=0.8)
        q = qbox("Why do they swell?")
        self.at("Why do they swell")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        self.outro(FadeOut(VGroup(title, b1, b2, l1, l2, six)))


# ---------------------------------------------------------------------------------------------
def start_graft_inside():
    emb = embryo()
    gan = ganglion(2.4)
    tum = tumor(TUM_IN)
    tl = tum_label(TUM_IN + np.array([0.0, 0.95, 0]))
    fib = fibers()
    gl = T("cluster of\nnerve cells", 22, TEAL_G, line_spacing=0.8).move_to(E + np.array([1.3, 0.55, 0]))
    return emb, gan, tum, tl, fib, gl


class S02Contact(Film):
    """the simplest explanation, contact, and the question it raises."""

    def construct(self):
        emb, gan, tum, tl, fib, gl = start_graft_inside()
        q = qbox("Why do they swell?")
        ns = nts()
        self.add(emb, fib, gan, cells(), tum, tl, gl, q, ns)

        ring = DashedVMobject(Circle(radius=0.62, color=YELLOW, stroke_width=4).move_to(TUM_IN), num_dashes=24)
        ch = chip("contact", YELLOW, size=28).move_to([PX, 0.9, 0])
        self.at("simplest explanation")
        self.play(FadeIn(ch, shift=DOWN * 0.1), run_time=0.6)
        self.at("pressed against")
        self.play(Create(ring), run_time=0.7)
        pr = T("pressed against its tissues", 22, YELLOW).move_to([PX, 0.1, 0])
        self.play(FadeIn(pr), run_time=0.4)
        fav = T("a favorable field\nfor fibers to grow into", 22, GREY, line_spacing=0.8).move_to([PX, -0.95, 0])
        self.at("favorable field")
        self.play(FadeIn(fav), run_time=0.5)
        q2 = qbox("Does the tumor need\nto touch the embryo?")
        self.at("Does the tumor need")
        self.play(FadeOut(q), FadeIn(q2), run_time=0.5)
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.outro(FadeOut(VGroup(ch, ring, pr, fav, ns)))


# ---------------------------------------------------------------------------------------------
class S03Move(Film):
    """move the tumor out to the membrane inside the eggshell: it touches no internal tissue."""

    def construct(self):
        emb, gan, tum, tl, fib, gl = start_graft_inside()
        q2 = qbox("Does the tumor need\nto touch the embryo?")
        self.add(emb, fib, gan, cells(), tum, tl, gl, q2)
        # the cells dots are a separate group in this scene: keep a handle so they can leave with the fibers
        dots = self.mobjects[3] if False else None

        park = np.array([PX, -0.45, 0])
        gl2 = T("ganglion", 22, TEAL_G).move_to(GAN + np.array([0.0, -0.8, 0]))
        names = T("Levi-Montalcini\nand Hamburger", 24, TEXT, line_spacing=0.8).move_to([PX, 1.5, 0])
        self.at("Levi Montalcini")
        self.play(FadeIn(names), run_time=0.5)
        self.at("moved the tumor")
        cellgrp = [m for m in self.mobjects if isinstance(m, VGroup) and len(m) == 6]
        self.play(tum.animate.move_to(park), tl.animate.move_to(park + np.array([0, -0.65, 0])),
                  FadeOut(fib), *[FadeOut(m) for m in cellgrp], Transform(gan, ganglion(1.0)), Transform(gl, gl2),
                  run_time=1.2)

        c = cam()
        cl, ld1, sl, ld2 = memb_labels()
        self.at("thin sheet")
        self.play(Create(c), FadeIn(cl), Create(ld1), run_time=1.2)
        sh = shell()
        self.at("inside of the eggshell")
        self.play(Create(sh), FadeIn(sl), Create(ld2), run_time=1.0)
        ves = vessels()
        self.at("blood circulation")
        self.play(Create(ves), run_time=1.0)
        bl = T("blood", 22, ORANGE).move_to([PX - 0.6, -2.45, 0])
        ld3 = leader(bl.get_left() + LEFT * 0.08, ep(CAMA - 0.5, CAMB - 0.5, -78), ORANGE)
        self.play(FadeIn(bl), Create(ld3), run_time=0.4)
        nc = T("no contact with the\nembryo's tissue", 22, YELLOW, line_spacing=0.8).move_to([PX, -1.7, 0])
        gap = DoubleArrow([0.55, 0.17, 0], [1.05, 0.17, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.12)
        self.at("touches none")
        self.play(Indicate(emb[0], color=YELLOW, scale_factor=1.03), FadeIn(nc), GrowFromCenter(gap), run_time=0.7)
        self.at("grafted the tumor")
        tl2, tld = cam_tumor_label()
        self.play(tum.animate.move_to(TUM_CAM), Transform(tl, tl2), FadeOut(names), run_time=1.3)
        self.play(Create(tld), run_time=0.3)
        self.outro(FadeOut(nc), FadeOut(gap))


# ---------------------------------------------------------------------------------------------
class S04Ruled(Film):
    """the ganglia swell just as before: contact ruled out, something that travels ruled in."""

    def construct(self):
        emb = embryo()
        gan = ganglion(1.0)
        gl = T("ganglion", 22, TEAL_G).move_to(GAN + np.array([0.0, -0.8, 0]))
        c, sh, ves = cam(), shell(), vessels()
        cl, ld1, sl, ld2 = memb_labels()
        bl = T("blood", 22, ORANGE).move_to([PX - 0.6, -2.45, 0])
        ld3 = leader(bl.get_left() + LEFT * 0.08, ep(CAMA - 0.5, CAMB - 0.5, -78), ORANGE)
        tum = tumor(TUM_CAM)
        tl, tld = cam_tumor_label()
        q2 = qbox("Does the tumor need\nto touch the embryo?")
        self.add(emb, ves, c, sh, gan, gl, cl, ld1, sl, ld2, bl, ld3, tum, tl, tld, q2)

        res = chip("ganglion swells", GREEN, size=26).move_to([PX, -0.95, 0])
        self.at("swelled just as before")
        self.play(gan.animate.scale(2.4), FadeIn(res, shift=DOWN * 0.1), run_time=1.0)
        self.at("Only blood connected")
        self.play(*[Indicate(v, color=ORANGE, scale_factor=1.0) for v in ves], run_time=0.8)
        v = ves[4]
        pts = [v.point_from_proportion(p) for p in np.linspace(0, 1, 8)]
        path = VMobject().set_points_as_corners([tum.get_center()] + pts + [GAN])
        sol = VGroup(*[Dot(radius=0.1, color=ORANGE).move_to(tum.get_center()) for _ in range(3)])
        stl = T("something soluble", 22, ORANGE).move_to([PX, -1.75, 0])
        self.at("something soluble")
        self.play(FadeIn(sol), FadeIn(stl), run_time=0.3)
        self.play(*[MoveAlongPath(d, path, rate_func=lambda t, k=k: smooth(min(1, max(0, t * 1.3 - k * 0.15))))
                    for k, d in enumerate(sol)], FadeOut(res), FadeOut(q2), run_time=1.2)

        out = chip("touching", RED, size=26).move_to([PX - 0.9, 2.75, 0])
        x1 = Line(out.get_left() + LEFT * 0.1, out.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        ro = T("ruled out", 26, RED).move_to([PX + 1.2, 2.75, 0])
        self.at("Contact is ruled out")
        self.play(FadeIn(out), run_time=0.3)
        self.play(Create(x1), FadeIn(ro), run_time=0.4)
        trav = chip("a substance that travels:\nruled in", GREEN, size=24).move_to([PX, 1.8, 0])
        self.at("A substance that travels")
        self.play(FadeIn(trav, shift=DOWN * 0.1), run_time=0.6)
        qm = T("what is it?", 24, YELLOW).move_to([PX, -1.75, 0])
        self.at("but not what")
        self.play(FadeIn(qm), FadeOut(stl), *[d.animate.scale(1.6) for d in sol], run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "Only blood connected the two, so something soluble must travel."
