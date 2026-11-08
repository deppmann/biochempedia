"""Predation and community effects: a predator that protects its prey's rivals (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = Pisaster, the predator (the sea star)
  BLUE   = mussels, the strong competitor for rock
  GREEN  = the other species on the shore (each green dot is one species)
  PURPLE = space on the rock (the limiting resource)
  WHITE  = the line transects (survey lines)
  RED    = removal: the fence, the crossed-out ideas, space lost
  YELLOW = the species count (15 and 8)
  GREY   = the rock, the control patch, structure and de-emphasized things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"   # space on the rock
COLS = [-3.6 + 1.2 * i for i in range(7)]
Y_TOP, Y_MID, Y_MUS = 0.95, -0.1, -1.4


def star(r=0.5, label=None, lsize=24):
    s = Star(n=5, outer_radius=r, inner_radius=r * 0.45, stroke_color=ORANGE, stroke_width=3,
             fill_color=ORANGE, fill_opacity=0.85)
    if label:
        return VGroup(s, T(label, lsize, ORANGE).next_to(s, DOWN, buff=0.12))
    return VGroup(s)


def sdot(r=0.2):
    return Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.85)


def mussel(w=0.9, h=0.62):
    return Ellipse(width=w, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6)


def rock(w=9.2, h=4.2, center=(0, -0.4)):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.18).move_to([center[0], center[1], 0])


class World:
    """The shore patch: 14 green dots (14 other species) + mussels = 15 species."""

    def __init__(self, scale=1.0, center=(0, -0.4), mid_dots=True, top_dots=True):
        self.c = np.array([center[0], center[1], 0.0])
        self.s = scale
        self.rock = rock(center=(0, -0.4)).copy()
        self.top = VGroup(*[sdot().move_to([x, Y_TOP, 0]) for x in COLS])
        self.mid = VGroup(*[sdot().move_to([x, Y_MID, 0]) for x in COLS])
        self.mus = VGroup(RoundedRectangle(corner_radius=0.3, width=8.4, height=0.75, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6).move_to([0, Y_MUS, 0]))
        self.all = VGroup(self.rock, self.mus, self.mid, self.top)
        self.all.shift(self.c - np.array([0, -0.4, 0]))
        self.all.scale(scale, about_point=self.c)

    def pos(self, x, y):
        return self.c + (np.array([x, y, 0]) - np.array([0, -0.4, 0])) * self.s


def fence(mob, color=RED, buff=0.25):
    r = SurroundingRectangle(mob, buff=buff, corner_radius=0.3, color=color, stroke_width=4)
    return DashedVMobject(r, num_dashes=60)


def barred(star_mob):
    """a red slash over a star: 'kept out'."""
    c = star_mob[0].get_center()
    return Line(c + np.array([-0.6, 0.6, 0]), c + np.array([0.6, -0.6, 0]), color=RED, stroke_width=7)


def bchip(text, color=BLUE, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


class S00Title(TitleCard):
    LESSON = "Predation and community effects"
    TITLE = "A predator that protects its prey's rivals"


# ---------------------------------------------------------------------------------------------
class S01Patch(SpokenScene):
    def construct(self):
        w = World()
        w.top.set_z_index(3); w.mid.set_z_index(3)
        self.at("Marine ecology")
        self.play(FadeIn(w.rock), LaggedStart(*[FadeIn(d, scale=0.5) for d in [*w.top, *w.mid]], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(m, scale=0.5) for m in w.mus], lag_ratio=0.05), run_time=1.6)
        lab = T("a shore community", 28, GREY).next_to(w.rock, UP, buff=0.3)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("who ate whom")
        links = VGroup(arr(w.top[1].get_center(), w.mid[1].get_center(), GREY, 3),
                       arr(w.mid[3].get_center(), np.array([COLS[3], Y_MUS + 0.4, 0]), GREY, 3),
                       arr(w.top[5].get_center(), w.mid[4].get_center(), GREY, 3),
                       arr(w.mid[6].get_center(), np.array([COLS[6], Y_MUS + 0.4, 0]), GREY, 3))
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.3), run_time=1.5)
        self.at("kept one species")
        st = star(0.45, "Pisaster", 22).move_to([-5.6, 2.75, 0])
        fz = fence(w.rock)
        self.play(FadeOut(links), FadeOut(lab), FadeIn(st, shift=RIGHT * 0.2), Create(fz), run_time=1.0)
        bar = barred(st)
        self.play(Create(bar), run_time=0.4)
        n8 = M("8", 64, YELLOW, weight=BOLD)
        sp = T("species", 30, YELLOW)
        inst = T("instead of", 26, GREY)
        n15 = M("15", 56, GREY)
        cnt = VGroup(n8, sp, inst, n15).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([0.9, 3.1, 0])
        self.at("Bay Washington")
        place = T("Mukkaw Bay, Washington", 30, TEXT).move_to([0, 2.3, 0])
        self.play(FadeIn(place, shift=DOWN * 0.1), run_time=0.6)
        self.at("he began doing")
        when = T("early 1960s: Pisaster kept out", 28, RED).move_to([0, 2.3, 0])
        self.play(FadeOut(place), FadeIn(when), run_time=0.6)
        self.at("By his")
        rep = T("1966 report", 30, TEXT).move_to([0, 2.3, 0])
        self.play(FadeOut(when), FadeIn(rep), run_time=0.6)
        self.at("held eight")
        self.play(FadeIn(VGroup(n8, sp), shift=UP * 0.1),
                  LaggedStart(*[d.animate.set_stroke(RED, opacity=0.9).set_fill(RED, 0.1) for d in w.mid], lag_ratio=0.06),
                  run_time=1.2)
        self.at("instead of")
        self.play(FadeIn(inst), FadeIn(n15), run_time=0.6)
        self.at("fewer kinds")
        self.play(FadeOut(VGroup(*w.mid)), FadeOut(rep), run_time=0.8)
        qs = VGroup(*[T("?", 40, RED, weight=BOLD).move_to(d.get_center()) for d in w.mid])
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.06), run_time=0.8)
        self.at("How can a species")
        eat = arr(st[0].get_center() + np.array([0.6, 0.0, 0]), [-4.6, 0.7, 0], ORANGE, 6)
        self.play(Indicate(st[0], color=ORANGE, scale_factor=1.25), GrowArrow(eat), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Design(SpokenScene):
    def construct(self):
        st = star(1.0, "Pisaster ochraceus", 28).move_to([-4.2, 0.2, 0])
        self.at("The sea star was")
        self.play(FadeIn(st, scale=0.7), run_time=0.8)
        names = [("mussels", BLUE), ("barnacles", GREEN), ("chitons", GREEN), ("limpets", GREEN), ("snails", GREEN)]
        chips, arrows = [], []
        for i, (nm, col) in enumerate(names):
            y = 2.4 - 1.15 * i
            c = bchip(nm, col, 30).move_to([2.2, y, 0])
            a = arr(st[0].get_center() + np.array([1.05, 0, 0]), [c.get_left()[0], y, 0], ORANGE)
            chips.append(c); arrows.append(a)
        for (nm, _), c, a in zip(names, chips, arrows):
            self.at("It ate" if nm == "mussels" else nm)
            self.play(GrowArrow(a), FadeIn(c, shift=LEFT * 0.2), run_time=0.5)
        self.at("what would happen")
        self.play(Indicate(st, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("taken out")
        self.play(FadeOut(VGroup(*chips, *arrows)), FadeOut(st), run_time=0.9)
        # two adjacent patches
        ctl = rock(5.8, 4.4, (-3.2, -0.5))
        rem = rock(5.8, 4.4, (3.2, -0.5))
        self.at("kept")
        rl = T("removal patch", 30, RED).next_to(rem, UP, buff=0.25)
        self.play(FadeIn(rem), FadeIn(rl), run_time=0.5)
        fz = fence(rem, RED, 0.15)
        st_out = star(0.5).move_to([5.5, 2.95, 0])
        self.play(Create(fz), FadeIn(st_out), run_time=0.7)
        bar = barred(st_out)
        self.play(Create(bar), run_time=0.4)
        self.at("left an adjacent stretch alone")
        cl = T("control", 30, GREY).next_to(ctl, UP, buff=0.25)
        st_in = star(0.5).move_to(ctl.get_center())
        self.play(FadeIn(ctl), FadeIn(cl), FadeIn(st_in, scale=0.6), run_time=0.9)
        self.at("surveyed both along")
        lines = VGroup()
        for y in (0.6, -1.6):
            for x0 in (-5.7, 0.7):
                ln = DashedLine([x0, y, 0], [x0 + 5.0, y, 0], color=TEXT, stroke_width=3.5, dash_length=0.2)
                lines.add(ln)
        self.play(Create(lines), run_time=1.0)
        tl = T("line transects", 28, TEXT).move_to([0, -3.4, 0])
        self.at("line transects")
        self.play(FadeIn(tl), run_time=0.4)
        self.at("remove a species")
        self.play(Indicate(rem, color=RED, scale_factor=1.03), run_time=0.8)
        self.at("measure the community")
        self.play(Indicate(lines, color=TEXT, scale_factor=1.02), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Space(SpokenScene):
    def construct(self):
        w = World()
        self.at("Why would the shore change")
        st = star(0.45, "Pisaster", 22).move_to(w.pos(-5.6, -1.4)[:])
        self.play(FadeIn(w.rock), FadeIn(w.top), FadeIn(w.mid), FadeIn(w.mus), FadeIn(st), run_time=1.0)
        self.at("competition for space")
        sp = T("space on the rock", 30, PURPLE).move_to([0, 2.6, 0])
        self.play(w.rock.animate.set_stroke(PURPLE, width=6), FadeIn(sp), run_time=0.8)
        self.at("limiting resource")
        lim = T("the limiting resource", 26, PURPLE).next_to(sp, DOWN, buff=0.1)
        self.play(FadeIn(lim), run_time=0.5)
        self.at("light in a forest")
        lf = T("as limiting as light in a forest", 26, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(lf), run_time=0.6)
        self.at("are strong competitors")
        mlab = T("mussels: strong competitors for rock", 26, BLUE).move_to([0, -3.3, 0])
        self.play(FadeOut(lf), FadeOut(lim), run_time=0.3)
        self.play(FadeIn(mlab), LaggedStart(*[Indicate(m, color=BLUE, scale_factor=1.2) for m in w.mus], lag_ratio=0.08), run_time=1.4)
        self.at("With")
        self.play(FadeOut(st[1]), run_time=0.3)
        NOTCH = "#252830"

        def bite(x, star_from):
            tgt = np.array([x, Y_MUS, 0])
            self.play(st.animate.move_to(tgt + np.array([-0.9, 0.0, 0])), run_time=0.6)
            notch = Circle(radius=0.5, stroke_width=0, fill_color=NOTCH, fill_opacity=1).move_to(tgt).set_z_index(2)
            self.play(st.animate.move_to(tgt + np.array([-0.2, 0, 0])), GrowFromCenter(notch), run_time=0.6)
            gap = DashedVMobject(Circle(radius=0.5, color=PURPLE, stroke_width=4).move_to(tgt), num_dashes=16).set_z_index(3)
            return tgt, notch, gap
        st.set_z_index(5)
        tgt, notch, gap = bite(COLS[2], None)
        self.at("space kept opening")
        self.play(Create(gap), st.animate.move_to(tgt + np.array([-1.3, 0, 0])), run_time=0.5)
        wc = sdot(0.14).move_to(tgt).set_z_index(4)
        wl = T("a weaker competitor", 24, GREEN).move_to([tgt[0], -2.85, 0])
        self.play(FadeIn(wc, scale=0.3), FadeOut(mlab), run_time=0.5)
        self.play(wc.animate.scale(2.2), FadeIn(wl), run_time=0.9)
        t2, notch2, gap2 = bite(COLS[5], None)
        wc2 = sdot(0.14).move_to(t2).set_z_index(4)
        self.play(Create(gap2), FadeIn(wc2, scale=0.3), st.animate.move_to(t2 + np.array([-1.3, 0, 0])), run_time=0.5)
        self.play(wc2.animate.scale(2.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Spread(SpokenScene):
    def construct(self):
        w = World()
        w.top.set_z_index(3); w.mid.set_z_index(3)
        st = star(0.55, "Pisaster").move_to(w.pos(-5.7, 2.2))
        self.at("Now take the sea star away")
        self.play(FadeIn(w.rock), FadeIn(w.top), FadeIn(w.mid), FadeIn(w.mus), FadeIn(st), run_time=0.8)
        fz = fence(w.rock)
        self.play(Create(fz), run_time=0.7)
        bar = barred(st)
        self.play(Create(bar), run_time=0.4)
        self.at("spread over the rock")
        self.play(w.mus[0].animate.stretch_to_fit_height(1.5).move_to([0, -1.0, 0]), run_time=2.0)
        self.at("won the competition")
        sp = T("competition for space", 28, PURPLE).move_to([0, 2.95, 0])
        self.play(FadeIn(sp), w.mus[0].animate.stretch_to_fit_height(2.2).move_to([0, -0.7, 0]), run_time=1.6)
        self.at("lost their footing")
        self.play(LaggedStart(*[d.animate.set_stroke(RED).set_fill(RED, 0.2) for d in w.mid], lag_ratio=0.1), run_time=1.0)
        self.at("The patch lost species")
        self.play(LaggedStart(*[d.animate.scale(0.05) for d in w.mid], lag_ratio=0.25), run_time=2.0)
        self.play(FadeOut(w.mid), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Count(SpokenScene):
    def construct(self):
        w = World(0.7, (-3.2, -0.7))
        mus_big = VGroup(RoundedRectangle(corner_radius=0.3, width=8.4, height=2.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6).scale(0.7).move_to(w.pos(0, -0.7)))
        mus_big.set_z_index(1)
        row = VGroup(*[Circle(radius=0.18, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85) for _ in range(15)]).arrange(RIGHT, buff=0.2).move_to([-1.3, 2.7, 0])
        n15 = VGroup(M("15", 48, YELLOW, weight=BOLD), T("species", 30, YELLOW)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).next_to(row, RIGHT, buff=0.5)
        n8 = VGroup(M("8", 48, YELLOW, weight=BOLD), T("species", 30, YELLOW)).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to(n15)
        self.at("Count the species")
        fz = fence(w.rock, RED, 0.15)
        tag = T("removal patch", 26, RED).next_to(w.rock, DOWN, buff=0.4)
        self.play(FadeIn(w.rock), FadeIn(w.top), FadeIn(mus_big), run_time=0.6)
        self.play(Create(fz), FadeIn(tag), LaggedStart(*[FadeIn(d, scale=0.4) for d in row], lag_ratio=0.05), FadeIn(n15), run_time=1.4)
        self.at("holding space")
        gone = VGroup(*row[8:])
        self.play(LaggedStart(*[d.animate.set_fill(opacity=0.0).set_stroke(opacity=0.3) for d in gone], lag_ratio=0.08), ReplacementTransform(n15, n8), run_time=1.4)
        self.at("The control")
        ctl = rock(4.4, 2.94, (3.9, -0.7))
        sti = star(0.45).move_to(ctl.get_center())
        ctag = T("control", 26, GREY).next_to(ctl, DOWN, buff=0.4)
        ctxt = T("did not lose species\nin the same way", 24, GREY, line_spacing=0.8).next_to(ctl, UP, buff=0.2)
        self.play(FadeIn(ctl), FadeIn(sti), FadeIn(ctag), FadeIn(ctxt), run_time=0.8)
        self.at("So the sea star did not")
        self.play(FadeOut(VGroup(w.rock, w.top, mus_big, fz, tag, ctl, sti, ctag, ctxt, row, n8)), run_time=0.7)
        stm = star(1.0, "Pisaster", 28).move_to([-4.6, 0, 0])
        harm = bchip("species that harmed the rest", GREY, 30).move_to([2.6, 0, 0])
        ar = arr([-3.3, 0, 0], harm.get_left() + LEFT * 0.1, ORANGE)
        self.play(FadeIn(stm), GrowArrow(ar), FadeIn(harm), run_time=0.6)
        self.at("harmed the others")
        x1 = Line(harm.get_corner(UL) + LEFT * 0.2, harm.get_corner(DR) + RIGHT * 0.2, color=RED, stroke_width=8)
        x2 = Line(harm.get_corner(UR) + RIGHT * 0.2, harm.get_corner(DL) + LEFT * 0.2, color=RED, stroke_width=8)
        self.play(Create(x1), Create(x2), run_time=0.5)
        self.at("freeing space")
        self.play(FadeOut(VGroup(harm, ar, x1, x2)), stm.animate.move_to([-4.6, 0.4, 0]), run_time=0.4)
        mu = mussel(1.6, 1.2).move_to([0.2, 0.4, 0])
        mlab = T("mussels", 28, BLUE).next_to(mu, DOWN, buff=0.15)
        ih = inhib(stm[0].get_center() + np.array([1.0, 0, 0]), mu.get_left() + LEFT * 0.05, RED)
        gp = DashedVMobject(Circle(radius=0.75, color=PURPLE, stroke_width=4).move_to([3.8, 0.4, 0]), num_dashes=20)
        gl = T("free space", 28, PURPLE).next_to(gp, DOWN, buff=0.15)
        wk = sdot(0.15).move_to([3.8, 0.4, 0])
        self.play(FadeIn(mu), FadeIn(mlab), Create(ih), run_time=0.5)
        self.play(Create(gp), FadeIn(gl), FadeIn(wk, scale=0.3), run_time=0.5)
        self.play(wk.animate.scale(3.2), run_time=0.5)
        self.at("strong local experiment")
        self.play(FadeOut(VGroup(stm, mu, mlab, ih, gp, gl, wk)), run_time=0.5)
        a = rock(5.2, 3.6, (-3.2, -0.2)); b = rock(5.2, 3.6, (3.2, -0.2))
        al = T("one removal patch", 30, RED).next_to(a, DOWN, buff=0.4)
        bl = T("one control", 30, GREY).next_to(b, DOWN, buff=0.4)
        fa = fence(a, RED, 0.12)
        self.play(FadeIn(a), FadeIn(b), Create(fa), FadeIn(al), FadeIn(bl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Keystone(SpokenScene):
    def construct(self):
        self.at("Ecologists call this")
        s = star(1.0, "Pisaster", 30).move_to([-4.9, 0.3, 0])
        mu = mussel(2.0, 1.4).move_to([0.0, 0.3, 0])
        ml = T("mussels", 30, BLUE).next_to(mu, DOWN, buff=0.2)
        wk = sdot(0.5).move_to([4.7, 0.3, 0])
        wl = T("weaker species", 30, GREEN).next_to(wk, DOWN, buff=0.2)
        self.play(FadeIn(s), FadeIn(mu), FadeIn(ml), FadeIn(wk), FadeIn(wl), run_time=1.0)
        kp = T("keystone predation", 40, ORANGE, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(kp), run_time=1.0)
        self.at("prefers to eat a strong competitor")
        ea = arr(s[0].get_center() + np.array([1.15, 0, 0]), mu.get_left() + LEFT * 0.1, ORANGE)
        self.play(GrowArrow(ea), Indicate(mu, color=BLUE), run_time=0.9)
        self.at("indirectly benefits")
        ih = inhib(mu.get_right() + RIGHT * 0.1, wk.get_left() + LEFT * 0.1, BLUE)
        ben = ArcBetweenPoints(np.array([-4.9, -1.6, 0]), np.array([4.7, -1.3, 0]), angle=TAU / 8, color=GREEN, stroke_width=5)
        ben.add_tip(tip_length=0.25)
        self.play(Create(ih), Create(ben), Indicate(wk, color=GREEN, scale_factor=1.3), run_time=1.4)
        bl = T("indirect benefit", 28, GREEN).move_to([0, -3.0, 0])
        self.play(FadeIn(bl), run_time=0.4)
        self.wait(0.5)
        self.at("A keystone species")
        self.play(FadeOut(VGroup(s, mu, ml, wk, wl, ea, ih, ben, bl, kp)), run_time=0.7)
        note = T("a diagram of the definition, not data", 28, GREY).move_to([0, 3.4, 0])
        self.play(FadeIn(note), run_time=0.4)

        def card(cx, title, col):
            c = RoundedRectangle(corner_radius=0.25, width=5.8, height=4.9, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.06).move_to([cx, -0.3, 0])
            t = T(title, 30, col).move_to([cx, 1.65, 0])
            return c, t
        c1, t1 = card(-3.2, "a keystone species", ORANGE)
        c2, t2 = card(3.2, "the most common species", BLUE)
        ab1 = Circle(radius=0.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([-5.0, -0.1, 0])
        ef1 = Circle(radius=1.2, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.5).move_to([-2.4, -0.1, 0])
        ab1l = T("abundance", 26, GREY).move_to([-5.0, -1.8, 0]); ef1l = T("effect", 26, ORANGE).move_to([-2.4, -1.8, 0])
        ab2 = Circle(radius=1.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([1.75, -0.1, 0])
        ef2 = DashedVMobject(Circle(radius=0.75, color=GREY, stroke_width=4).move_to([4.8, -0.1, 0]), num_dashes=20)
        q = T("?", 56, GREY, weight=BOLD).move_to([4.8, -0.1, 0])
        ab2l = T("abundance", 26, GREY).move_to([1.75, -1.8, 0]); ef2l = T("effect", 26, GREY).move_to([4.8, -1.8, 0])
        self.at("large relative")
        self.play(FadeIn(c1), FadeIn(t1), run_time=0.5)
        self.play(GrowFromCenter(ab1), FadeIn(ab1l), run_time=0.5)
        self.play(GrowFromCenter(ef1), FadeIn(ef1l), run_time=0.8)
        self.at("The most common species")
        self.play(FadeIn(c2), FadeIn(t2), run_time=0.5)
        self.play(GrowFromCenter(ab2), FadeIn(ab2l), run_time=0.7)
        self.play(Create(ef2), FadeIn(q), FadeIn(ef2l), run_time=0.6)
        self.at("by default")
        nk = T("not a keystone by default", 30, RED).move_to([3.2, -3.4, 0])
        self.play(FadeIn(nk), run_time=0.5)
        self.at("judge a species")
        self.play(FadeOut(VGroup(c1, t1, c2, t2, ab1, ef1, ab1l, ef1l, ab2, ef2, q, ab2l, ef2l, nk, note)), run_time=0.6)
        rule = VGroup(T("Judge a species by its effect,", 44, TEXT, font=TITLE_FONT), T("not by its numbers.", 44, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Judge a species by its effect, not its numbers."
