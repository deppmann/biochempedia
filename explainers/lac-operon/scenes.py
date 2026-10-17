"""The lac operon: two signals switch the lactose genes on  (Biochemistrypedia genetics explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the lacZ, lacY, lacA genes and the permease they encode
  RED    = the lac repressor (and its gene, lacI); also "blocked"
  GOLD   = the operator
  YELLOW = lactose and allolactose (the inducer signal)
  ORANGE = glucose and its transport protein
  TEAL   = CAP (the activator) and the CAP site
  TEXT   = the cyclic AMP badge
  PURPLE = RNA polymerase
  GREEN  = messenger RNA, and "transcription on"
  GREY   = DNA bar, promoter, membrane, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

DY = -0.4                 # y of the DNA bar
YR = DY + 0.8            # y of the polymerase and the mRNA
MY = 2.9                  # y of the cell membrane
X = dict(lacI=-5.5, cap=-3.8, prom=-2.5, op=-1.3, Z=0.4, Y=2.0, A=3.6)
RNA_X0 = -2.0             # where the mRNA starts


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def box(x, w, color, h=0.8):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.3).move_to([x, DY, 0])


def gene(name, x, color=BLUE, w=1.5):
    b = box(x, w, color, h=0.95)
    return VGroup(b, T(name, 28, color).move_to(b))


def under(text, x, row=1, color=GREY):
    return T(text, 24, color).move_to([x, DY - 0.72 - 0.5 * (row - 1), 0])


def dna_line():
    return Line([-6.2, DY, 0], [4.6, DY, 0], color=GREY, stroke_width=6)


def parts():
    """every fixed piece of the DNA bar; scenes add the ones they need."""
    p = {}
    p["line"] = dna_line()
    p["lacI"] = gene("lacI", X["lacI"], RED, w=1.0)
    p["capsite"] = VGroup(box(X["cap"], 0.7, TEAL), under("CAP site", X["cap"], 1, TEAL))
    p["prom"] = VGroup(box(X["prom"], 1.0, GREY), under("promoter", X["prom"], 2))
    p["op"] = VGroup(box(X["op"], 0.6, GOLD), under("operator", X["op"], 1, GOLD))
    p["Z"] = gene("lacZ", X["Z"])
    p["Y"] = gene("lacY", X["Y"])
    p["A"] = gene("lacA", X["A"])
    return p


def poly_blob(color=PURPLE):
    blob = RoundedRectangle(corner_radius=0.25, width=1.0, height=0.7, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.5).move_to([0, YR, 0])
    lab = T("RNA\npolymerase", 24, color, line_spacing=0.7).next_to(blob, UP, buff=0.2).shift(LEFT * 0.7)
    return VGroup(blob, lab)


class Poly:
    """RNA polymerase at x = tracker value; the label travels with it and can fade (lab_op)."""

    def __init__(self, x):
        self.px = ValueTracker(x)
        self.lab_op = ValueTracker(1.0)
        self.g = poly_blob()
        blob, lab = self.g[0], self.g[1]
        off = lab.get_center() - blob.get_center()

        def upd(m):
            blob.move_to([self.px.get_value(), YR, 0])
            lab.move_to(blob.get_center() + off)
            lab.set_opacity(self.lab_op.get_value())
        self.g.add_updater(upd)
        upd(self.g)

    @property
    def blob(self):
        return self.g[0]


def mrna(ex, w, col=GREEN, op=1.0):
    """a line from RNA_X0 to the tracker ex, stroke width from tracker w."""
    def f():
        e, wd = ex.get_value(), w.get_value()
        if e - RNA_X0 < 0.04 or wd < 0.05:
            return Line([RNA_X0, YR, 0], [RNA_X0 + 0.01, YR, 0], stroke_width=0, stroke_opacity=0)
        return Line([RNA_X0, YR, 0], [e, YR, 0], color=col, stroke_width=wd, stroke_opacity=op)
    return always_redraw(f)


class Rep:
    """the repressor: two lobes that grip the operator. Closed = holds; open = has changed shape."""
    OPEN = 0.3

    def __init__(self, x=X["op"]):
        by = DY + 0.4
        mk = lambda dx: RoundedRectangle(corner_radius=0.14, width=0.5, height=1.3, stroke_color=RED, stroke_width=3,
                                         fill_color=RED, fill_opacity=0.4).move_to([x + dx, by + 0.65, 0])
        self.L, self.R = mk(-0.25), mk(0.25)
        self.anchor = Dot([x, by, 0], radius=0.001).set_opacity(0)
        self.lobes = VGroup(self.L, self.R)
        self.lab = T("repressor", 24, RED).next_to(self.lobes, RIGHT, buff=0.6)
        self.g = VGroup(self.lobes, self.lab, self.anchor)

    def pl(self):
        return self.anchor.get_center() + LEFT * 0.25

    def pr(self):
        return self.anchor.get_center() + RIGHT * 0.25

    def open_now(self):
        self.L.rotate(self.OPEN, about_point=self.pl())
        self.R.rotate(-self.OPEN, about_point=self.pr())

    def open_anim(self):
        return [self.L.animate.rotate(self.OPEN, about_point=self.pl()),
                self.R.animate.rotate(-self.OPEN, about_point=self.pr())]

    def close_anim(self):
        return [self.L.animate.rotate(-self.OPEN, about_point=self.pl()),
                self.R.animate.rotate(self.OPEN, about_point=self.pr())]

    def top(self):
        return self.anchor.get_center() + UP * 1.4


PARK = np.array([0.7, 0.95, 0.0])      # shift from the operator to the parking place


def lactose(pos, label=True):
    c = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to(pos)
    if not label:
        return VGroup(c)
    return VGroup(c, T("lactose", 24, YELLOW).next_to(c, RIGHT, buff=0.15))


def allolactose(pos):
    d = Square(side_length=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).rotate(PI / 4).move_to(pos)
    return d


def membrane(gaps=(2.6,)):
    segs, x0 = [], -6.3
    for gx in gaps:
        segs.append((x0, gx - 0.4))
        x0 = gx + 0.4
    segs.append((x0, 6.3))
    return VGroup(*[RoundedRectangle(corner_radius=0.08, width=b - a, height=0.26, stroke_color=GREY, stroke_width=3,
                                     fill_color=GREY, fill_opacity=0.35).move_to([(a + b) / 2, MY, 0]) for a, b in segs])


def permease(x=2.6):
    return RoundedRectangle(corner_radius=0.12, width=0.55, height=0.5, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.45).move_to([x, MY, 0])


def cap_blob(x=X["cap"]):
    b = RoundedRectangle(corner_radius=0.2, width=1.2, height=0.75, stroke_color=TEAL, stroke_width=3,
                         fill_color=TEAL, fill_opacity=0.45).move_to([x, YR, 0])
    return VGroup(b, T("CAP", 28, TEAL).move_to(b))


def camp_badge(cap):
    return chip("cAMP", TEXT, size=24, pad=0.1).next_to(cap, UP + LEFT, buff=0.0).shift(UP * 0.05)


def at_t(scene, t):
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


class S00Title(TitleCard):
    LESSON = "The lac operon"
    TITLE = "Two signals switch lactose genes on"


# ---------------------------------------------------------------------------------------------
class S01Choice(SpokenScene):
    """glucose then lactose with a pause; the choice is made by three genes and two signals."""

    def construct(self):
        broth = RoundedRectangle(corner_radius=0.25, width=6.2, height=1.5, stroke_color=GREY, stroke_width=3).move_to([-1.9, 2.55, 0])
        blabel = T("medium", 22, GREY).move_to([-5.7, 2.55, 0])
        rng = np.random.RandomState(4)
        gl, la = [], []
        for i in range(6):
            gl.append(Dot([-4.7 + i * 1.0 + rng.uniform(-.2, .2), 2.55 + (0.35 if i % 2 else -0.3), 0], radius=0.17, color=ORANGE))
            la.append(Dot([-4.2 + i * 1.0 + rng.uniform(-.2, .2), 2.55 + (-0.3 if i % 2 else 0.35), 0], radius=0.17, color=YELLOW))
        gl, la = VGroup(*gl), VGroup(*la)
        leg = VGroup(Dot(radius=0.14, color=ORANGE), T("glucose", 22, ORANGE), Dot(radius=0.14, color=YELLOW), T("lactose", 22, YELLOW)).arrange(RIGHT, buff=0.18)
        leg.move_to([-1.9, 1.55, 0])
        cell = RoundedRectangle(corner_radius=0.5, width=2.6, height=1.1, stroke_color=TEXT, stroke_width=3).move_to([4.6, 2.55, 0])
        cl = T("E. coli", 28, TEXT).move_to(cell)
        self.play(FadeIn(broth), FadeIn(blabel), FadeIn(gl), FadeIn(la), FadeIn(leg), FadeIn(cell), FadeIn(cl), run_time=1.3)

        axis = Arrow([-5.4, -0.05, 0], [5.0, -0.05, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        tl = T("time", 22, GREY).move_to([5.5, -0.05, 0])
        self.at("both at once")
        self.play(Create(axis), FadeIn(tl), run_time=0.7)
        bar1 = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.3).move_to([-3.2, 0.6, 0])
        t1 = T("eats glucose", 28, ORANGE).move_to(bar1)
        self.at("uses up the glucose")
        self.play(GrowFromEdge(bar1, LEFT), LaggedStart(*[FadeOut(d) for d in gl], lag_ratio=0.1), FadeIn(t1), run_time=1.2)
        pause = T("pause", 28, GREY).move_to([-0.4, -0.55, 0])
        q = T("?", 56, GREY, weight=BOLD).move_to([-0.4, 0.6, 0])
        self.at("pauses")
        self.play(FadeIn(pause), FadeIn(q, scale=0.7), run_time=0.5)
        bar2 = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3).move_to([2.4, 0.6, 0])
        t2 = T("eats lactose", 28, YELLOW).move_to(bar2)
        self.at("only then")
        self.play(GrowFromEdge(bar2, LEFT), LaggedStart(*[FadeOut(d) for d in la], lag_ratio=0.1), FadeIn(t2), run_time=1.2)
        self.at("How does one")
        self.play(q.animate.set_color(TEXT).scale(1.4), run_time=0.5)
        self.play(q.animate.scale(1 / 1.4), run_time=0.3)

        # --- the answer is in the DNA -----------------------------------------------------
        line = dna_line()
        Z, Y, A = (gene("lacZ", X["Z"]), gene("lacY", X["Y"]), gene("lacA", X["A"]))
        self.at("The answer is")
        self.play(FadeOut(VGroup(broth, blabel, leg, cell, cl, axis, tl, bar1, t1, bar2, t2, pause, q, gl, la)), run_time=0.6)
        self.play(Create(line), run_time=0.9)
        self.at("Three genes")
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.15) for g in (Z, Y, A)], lag_ratio=0.35), run_time=1.4)
        s1 = chip("lactose here?", YELLOW, 28).move_to([-0.6, 1.4, 0])
        s2 = chip("glucose here?", ORANGE, 28).move_to([3.6, 1.4, 0])
        a1 = Arrow(s1.get_bottom(), [1.2, DY + 0.55, 0], buff=0.1, color=YELLOW, stroke_width=5)
        a2 = Arrow(s2.get_bottom(), [2.8, DY + 0.55, 0], buff=0.1, color=ORANGE, stroke_width=5)
        self.at("two separate signals")
        self.play(FadeIn(s1, shift=DOWN * 0.2), GrowArrow(a1), run_time=0.7)
        self.play(FadeIn(s2, shift=DOWN * 0.2), GrowArrow(a2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Genes(SpokenScene):
    """one mRNA from three genes; the repressor on the operator blocks the polymerase."""

    def construct(self):
        p = parts()
        self.add(p["line"], p["Z"], p["Y"], p["A"])
        # the three genes, one by one
        t1, t2 = self.t_of("called"), self.t_of("One promoter")
        for k, key in enumerate("ZYA"):
            at_t(self, t1 + (t2 - t1) * (0.15 + 0.3 * k))
            self.play(Indicate(p[key], color=BLUE, scale_factor=1.15), run_time=0.6)
        self.at("One promoter")
        self.play(FadeIn(p["prom"]), run_time=0.5)
        ex, w = ValueTracker(RNA_X0), ValueTracker(5)
        poly = Poly(X["prom"])
        rna = mrna(ex, w)
        self.at("RNA polymerase")
        self.add(rna)
        self.play(FadeIn(poly.g), run_time=0.5)
        self.at("reads them")
        self.play(poly.px.animate.set_value(4.1), ex.animate.set_value(3.6), run_time=1.3, rate_func=linear)
        one = T("one mRNA", 28, GREEN).move_to([1.2, YR + 0.55, 0])
        self.at("single messenger")
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)

        # --- the fourth gene and its repressor --------------------------------------------
        rep = Rep()
        rep.g.shift(LEFT * 4.2 + UP * 1.5)       # born above lacI (x about -5.5)
        self.at("fourth gene")
        self.play(FadeIn(p["lacI"], shift=DOWN * 0.15), run_time=0.6)
        self.at("It makes")
        self.play(FadeIn(rep.g, shift=DOWN * 0.3), run_time=0.7)
        # clear the old run; a fresh polymerase waits at the promoter
        self.at("The repressor binds")
        poly.px.set_value(X["prom"])
        self.play(FadeOut(one), w.animate.set_value(0), FadeOut(poly.g), run_time=0.5)
        self.remove(rna)
        poly = Poly(X["prom"])
        self.play(FadeIn(poly.g), run_time=0.4)
        self.at("operator")
        self.play(FadeIn(p["op"]), run_time=0.5)
        self.play(rep.g.animate.shift(UP * 0.5), run_time=0.4)
        self.play(rep.g.animate.shift(RIGHT * 4.2), run_time=0.7)
        self.play(rep.g.animate.shift(DOWN * 2.0), run_time=0.5)
        self.at("Bound there")
        self.play(Indicate(rep.lobes, color=RED, scale_factor=1.1), run_time=0.6)
        self.at("keeps")
        bar = Line([-1.9, DY + 0.45, 0], [-1.9, DY + 1.45, 0], color=RED, stroke_width=7)
        self.play(poly.px.animate.set_value(X["prom"] + 0.18), run_time=0.3)
        self.play(poly.px.animate.set_value(X["prom"]), Create(bar), run_time=0.4)
        self.play(Wiggle(poly.g, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Release(SpokenScene):
    """lactose -> allolactose; allolactose opens the repressor, which lets go of the operator."""

    def construct(self):
        p = parts()
        for k in ("line", "lacI", "prom", "op", "Z", "Y", "A"):
            self.add(p[k])
        rep = Rep()
        poly = Poly(X["prom"])
        self.add(rep.g, poly.g)
        mem = membrane()
        perm = permease()
        plab = T("permease", 24, BLUE).move_to([4.15, 2.4, 0])
        self.at("Lactose enters")
        self.play(FadeIn(mem), FadeIn(perm), run_time=0.6)
        lac = lactose([2.6, 3.3, 0])
        self.play(FadeIn(lac, shift=DOWN * 0.2), run_time=0.4)
        self.at("called the permease")
        self.play(FadeIn(plab), lac.animate.move_to([2.6, 1.9, 0]), run_time=1.3)
        # the lactose label stays to the right of its circle
        arr = Arrow([2.25, 1.9, 0], [1.0, 1.9, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.2)
        enz = T("β-galactosidase", 24, GREY).move_to([1.3, 2.4, 0])
        self.at("An enzyme")
        self.play(GrowArrow(arr), FadeIn(enz), run_time=0.6)
        allo = allolactose([0.55, 1.9, 0])
        allo_l = T("allolactose", 24, YELLOW).move_to([0.55, 1.4, 0])
        self.at("into allolactose")
        self.play(FadeIn(allo, scale=0.5), FadeIn(allo_l), run_time=0.6)
        self.at("itself")
        cross = VGroup(Line(lac[0].get_corner(UL), lac[0].get_corner(DR), color=RED, stroke_width=6),
                       Line(lac[0].get_corner(UR), lac[0].get_corner(DL), color=RED, stroke_width=6))
        self.play(Create(cross), lac[1].animate.set_opacity(0.4), run_time=0.5)
        self.at("Allolactose is")
        self.play(Indicate(VGroup(allo, allo_l), color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.at("binds the repressor")
        self.play(FadeOut(allo_l), FadeOut(VGroup(lac, cross)), FadeOut(arr), FadeOut(enz),
                  allo.animate.move_to(rep.top() + UP * 0.1), run_time=1.0)
        self.at("changes its shape")
        self.play(*rep.open_anim(), allo.animate.move_to(rep.top() + UP * 0.05), run_time=0.8)
        self.at("more weakly")
        self.play(Indicate(rep.lobes, color=RED, scale_factor=1.05), run_time=0.5)
        self.at("comes off")
        grp = VGroup(rep.g, allo)
        self.play(grp.animate.shift(PARK), run_time=1.0)
        # transcription starts: a thin mRNA
        ex, w = ValueTracker(RNA_X0), ValueTracker(3.5)
        rna = mrna(ex, w, op=0.7)
        self.add(rna)
        self.at("transcription starts")
        self.play(poly.lab_op.animate.set_value(0), run_time=0.25)
        self.play(poly.px.animate.set_value(4.1), ex.animate.set_value(3.6), run_time=2.75, rate_func=linear)
        self.play(FadeOut(poly.g), FadeOut(plab), run_time=0.4)
        poly2 = Poly(X["prom"])
        self.play(FadeIn(poly2.g), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Activator(SpokenScene):
    """CAP with cyclic AMP docks on the CAP site, grips the polymerase; the mRNA gets much stronger."""

    def construct(self):
        p = parts()
        for k in ("line", "lacI", "prom", "op", "Z", "Y", "A"):
            self.add(p[k])
        mem, perm = membrane(), permease()
        self.add(mem, perm)
        rep = Rep()
        rep.open_now()
        allo = allolactose(rep.top() + UP * 0.05)
        VGroup(rep.g, allo).shift(PARK)
        poly = Poly(X["prom"])
        ex0, w0 = ValueTracker(3.6), ValueTracker(3.5)
        weak = mrna(ex0, w0, op=0.7)
        self.add(rep.g, allo, poly.g, weak)

        self.at("weak on its own")
        self.play(Indicate(p["prom"], color=GREY, scale_factor=1.15), run_time=0.7)
        cap = cap_blob()
        cap.shift(LEFT * 0.55)
        badge = camp_badge(cap)
        self.at("activator called")
        self.play(FadeIn(cap, shift=RIGHT * 0.2), run_time=0.7)
        self.at("bound to")
        self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.5)
        self.at("attaches just")
        self.play(FadeIn(p["capsite"]), run_time=0.4)
        self.play(VGroup(cap, badge).animate.shift(RIGHT * 0.55), run_time=0.9)
        link = Line(cap[0].get_right() + LEFT * 0.05, poly.blob.get_left() + RIGHT * 0.05, color=TEAL, stroke_width=16)
        self.at("contacts RNA")
        self.play(Create(link), Indicate(poly.blob, color=PURPLE, scale_factor=1.15), run_time=0.7)
        ex, w = ValueTracker(RNA_X0), ValueTracker(9)
        strong = mrna(ex, w)
        self.add(strong)
        self.at("helps it")
        self.play(FadeOut(link), run_time=0.2)
        self.play(poly.lab_op.animate.set_value(0), run_time=0.25)
        self.play(poly.px.animate.set_value(4.1), ex.animate.set_value(3.6), run_time=2.75, rate_func=linear)
        self.play(FadeOut(poly.g), run_time=0.4)
        poly2 = Poly(X["prom"])
        self.play(FadeIn(poly2.g), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Glucose(SpokenScene):
    """glucose lowers cAMP (CAP lets go) and its transport protein plugs the permease (repressor returns)."""

    def construct(self):
        p = parts()
        for k in ("line", "lacI", "prom", "op", "Z", "Y", "A", "capsite"):
            self.add(p[k])
        mem, perm = membrane(), permease()
        self.add(mem, perm)
        rep = Rep()
        rep.open_now()
        allo = allolactose(rep.top() + UP * 0.05)
        VGroup(rep.g, allo).shift(PARK)
        poly = Poly(X["prom"])
        cap = cap_blob()
        badge = camp_badge(cap)
        ex0, w0 = ValueTracker(3.6), ValueTracker(3.5)
        weak = mrna(ex0, w0, op=0.7)
        ex, w = ValueTracker(3.6), ValueTracker(9)
        strong = mrna(ex, w)
        self.add(rep.g, allo, poly.g, weak, strong, cap, badge)

        # meters: glucose and cyclic AMP (levels only)
        def meter(name, y, color, level):
            lab = T(name, 24, color).move_to([4.5 - 0.15, y, 0])
            lab.move_to([4.45 - lab.width / 2, y, 0])
            track = Line([4.6, y, 0], [6.2, y, 0], color=GREY, stroke_width=14, stroke_opacity=0.4)
            lv = ValueTracker(level)
            fill = always_redraw(lambda: Line([4.6, y, 0], [4.6 + 1.6 * lv.get_value(), y, 0], color=color, stroke_width=14)
                                 if lv.get_value() > 0.02 else Line([4.6, y, 0], [4.61, y, 0], stroke_width=0, stroke_opacity=0))
            return lab, track, fill, lv
        gl_lab, gl_tr, gl_fill, gl_lv = meter("glucose", 2.15, ORANGE, 0.06)
        cm_lab, cm_tr, cm_fill, cm_lv = meter("cyclic AMP", 1.65, TEXT, 0.9)
        self.at("Now add")
        key = T("bars show order only", 22, GREY).move_to([6.2 - 1.45, 1.2, 0])
        self.play(FadeIn(VGroup(gl_lab, gl_tr, cm_lab, cm_tr, key)), run_time=0.5)
        self.add(gl_fill, cm_fill)
        self.at("is higher")
        self.play(Indicate(VGroup(cm_lab, cm_tr), color=TEXT, scale_factor=1.05), run_time=0.6)
        self.at("is scarce")
        self.play(Indicate(VGroup(gl_lab, gl_tr), color=ORANGE, scale_factor=1.08), run_time=0.6)
        self.at("is active")
        self.play(Indicate(cap, color=TEAL, scale_factor=1.15), run_time=0.6)
        # glucose plentiful: cAMP falls, CAP lets go
        self.at("plentiful")
        self.play(gl_lv.animate.set_value(0.95), run_time=0.8)
        self.at("is lower")
        self.play(cm_lv.animate.set_value(0.3), FadeOut(badge, shift=UP * 0.2),
                  cap[0].animate.set_stroke(GREY).set_fill(GREY, 0.2), cap[1].animate.set_color(GREY), run_time=0.6)
        self.play(w.animate.set_value(5), run_time=0.7)
        deb = T("how much this matters is debated", 24, GREY).move_to([3.7, 0.85, 0])
        self.at("Scientists debate")
        self.play(FadeIn(deb), run_time=0.5)

        # second effect: the transport protein plugs the permease
        self.at("second effect")
        self.play(FadeOut(VGroup(gl_lab, gl_tr, gl_fill, cm_lab, cm_tr, cm_fill, deb, key)), run_time=0.6)
        tp = RoundedRectangle(corner_radius=0.15, width=0.7, height=0.4, stroke_color=ORANGE, stroke_width=3,
                              fill_color=ORANGE, fill_opacity=0.6).move_to([-4.2, MY, 0])
        tpl = T("transport protein", 24, ORANGE).move_to([-4.2, 2.4, 0])
        gdots = VGroup(*[Dot([-4.2 + dx, 3.4 + dy, 0], radius=0.15, color=ORANGE) for dx, dy in ((-0.3, 0), (0.0, 0.35), (0.3, 0))])
        self.at("glucose is taken")
        self.play(FadeIn(tp), FadeIn(gdots), run_time=0.4)
        self.play(gdots.animate.shift(DOWN * 1.2), run_time=0.7)
        self.play(FadeOut(gdots, shift=DOWN * 0.3), run_time=0.3)
        self.at("a transport protein")
        self.play(FadeIn(tpl), Indicate(tp, color=ORANGE, scale_factor=1.3), run_time=0.7)
        self.at("binds the permease")
        self.play(FadeOut(tpl), tp.animate.move_to([2.6, MY - 0.4, 0]), run_time=1.2)
        tpl.move_to([3.9, 1.9, 0])
        self.play(FadeIn(tpl), run_time=0.3)
        lac = lactose([2.6, 3.5, 0], label=False)
        bar = Line([2.2, MY + 0.3, 0], [3.0, MY + 0.3, 0], color=RED, stroke_width=7)
        self.at("blocks lactose")
        self.play(lac.animate.move_to([2.6, 3.1, 0]), run_time=0.5)
        self.play(Create(bar), lac.animate.shift(UP * 0.6 + RIGHT * 0.5), run_time=0.5)
        self.play(FadeOut(lac), run_time=0.3)
        self.at("means less")
        self.play(FadeOut(allo), FadeOut(VGroup(tpl)), run_time=0.7)
        self.at("so more")
        self.play(w.animate.set_value(3.5), run_time=0.3)
        grp = rep.g
        self.play(grp.animate.shift(-PARK), run_time=1.0)
        self.play(*rep.close_anim(), rep.lobes.animate.set_opacity(0.45), rep.lab.animate.set_opacity(0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """a two-by-two grid: lactose against glucose -> very low, very low, reduced, high."""

    def construct(self):
        cols = [-1.5, 3.3]
        rows = [0.85, -1.55]
        cw, ch = 4.6, 2.1
        col_h = [T("glucose present", 30, ORANGE).move_to([cols[0], 2.85, 0]), T("glucose scarce", 30, ORANGE).move_to([cols[1], 2.85, 0])]
        row_h = [T("lactose\nabsent", 30, YELLOW, line_spacing=0.8).move_to([-5.3, rows[0], 0]),
                 T("lactose\npresent", 30, YELLOW, line_spacing=0.8).move_to([-5.3, rows[1], 0])]
        cells = {}
        for r in range(2):
            for c in range(2):
                cells[(r, c)] = RoundedRectangle(corner_radius=0.15, width=cw, height=ch, stroke_color=GREY, stroke_width=2.5).move_to([cols[c], rows[r], 0])
        self.at("Put the two")
        self.play(LaggedStart(*[FadeIn(h) for h in col_h + row_h], lag_ratio=0.15), run_time=1.0)
        self.play(*[Create(c) for c in cells.values()], run_time=0.8)

        def fill(rc, word, level, color=GREEN):
            cell = cells[rc]
            txt = T(word, 38, TEXT, weight=BOLD).move_to(cell.get_center() + UP * 0.38)
            x0 = cell.get_left()[0] + 0.5
            track = Line([x0, cell.get_center()[1] - 0.5, 0], [x0 + 3.6, cell.get_center()[1] - 0.5, 0], color=GREY, stroke_width=16, stroke_opacity=0.35)
            bar = Line([x0, cell.get_center()[1] - 0.5, 0], [x0 + 3.6 * level, cell.get_center()[1] - 0.5, 0], color=color, stroke_width=16)
            return txt, track, bar

        self.at("With no lactose")
        self.play(Indicate(row_h[0], color=YELLOW, scale_factor=1.15), Indicate(col_h[0], color=ORANGE, scale_factor=1.1), run_time=0.8)
        txt, tr, bar = fill((0, 0), "very low", 0.06)
        self.at("very low")
        self.play(FadeIn(txt), FadeIn(tr), GrowFromEdge(bar, LEFT), run_time=0.6)
        self.at("That holds even")
        self.play(Indicate(col_h[1], color=ORANGE, scale_factor=1.1), run_time=0.7)
        txt2, tr2, bar2 = fill((0, 1), "very low", 0.06)
        self.play(FadeIn(txt2), FadeIn(tr2), GrowFromEdge(bar2, LEFT), run_time=0.6)
        self.at("lactose and glucose together")
        self.play(Indicate(row_h[1], color=YELLOW, scale_factor=1.15), Indicate(col_h[0], color=ORANGE, scale_factor=1.1), run_time=0.8)
        txt3, tr3, bar3 = fill((1, 0), "reduced", 0.4)
        self.at("reduced")
        self.play(FadeIn(txt3), FadeIn(tr3), GrowFromEdge(bar3, LEFT), run_time=0.6)
        self.at("Lactose present and")
        self.play(Indicate(row_h[1], color=YELLOW, scale_factor=1.15), Indicate(col_h[1], color=ORANGE, scale_factor=1.1), run_time=0.8)
        txt4, tr4, bar4 = fill((1, 1), "high", 1.0)
        self.at("gives high")
        self.play(FadeIn(txt4), FadeIn(tr4), GrowFromEdge(bar4, LEFT), cells[(1, 1)].animate.set_stroke(GREEN, 5), run_time=0.7)
        self.at("The genes switch on")
        self.play(*[VGroup(txt, tr, bar).animate.set_opacity(0.35) for txt, tr, bar in ((txt, tr, bar), (txt2, tr2, bar2), (txt3, tr3, bar3))],
                  Indicate(VGroup(txt4, tr4, bar4), color=GREEN, scale_factor=1.05), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "On only when lactose is present and glucose is scarce."
