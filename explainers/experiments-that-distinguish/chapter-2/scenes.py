"""Two Jobs, One Protein (chapter 2 of Experiments That Distinguish Mechanisms).

COLOR MAP (identical to chapter 1)
  TEAL   = Model 1 / mitosis-itself twin
  ORANGE = Model 2 / endocytosis-only twin
  PURPLE = protein (clathrin), resistant copies, job tags
  GOLD   = intervention, labelled cohort, decisive result, overshoot of the timer
  GREY   = shared structure, unchanged result, neutral single cell
  WHITE  = questions, hairpin, spindle fibres, cargo

Every bar and curve is schematic and says so; no value is plotted as data.
"""
from bp_style import *  # noqa: F401,F403
import numpy as np
from manim import Succession, Wait

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def label(text, x=0, y=0, color=TEXT, size=30, **kw):
    return T(text, size=size, color=color, **kw).move_to([x, y, 0])


def protein_blob(x, y=0.15, scale=1.0):
    return Ellipse(width=0.76 * scale, height=0.54 * scale, color=PURPLE,
                   stroke_width=3, fill_color=PURPLE, fill_opacity=0.85).move_to([x, y, 0])


def strand(x, y, color=PURPLE, width=3.5):
    pts = [np.array([x - width / 2 + width * i / 36, y + 0.16 * np.sin(i * 0.75), 0]) for i in range(37)]
    return VMobject(color=color, stroke_width=6).set_points_smoothly(pts)


def hairpin(x, y):
    return VGroup(Arc(radius=.45, start_angle=-PI / 2, angle=PI, color=TEXT, stroke_width=5),
                  Arc(radius=.45, start_angle=PI / 2, angle=PI, color=TEXT, stroke_width=5)).scale(.65).move_to([x, y, 0])


def creep(tracker, rate, cap):
    """Slow, endless division: the furrow deepens a little every second."""
    tracker.add_updater(lambda m, dt: m.set_value(min(cap, m.get_value() + rate * dt)))
    return tracker


def div_cell(cx, cy, r, color, S):
    """A cell as two overlapping circles driven by tracker S: S=0 one round cell, S=1 two touching daughters."""
    def mk():
        s = S.get_value()
        d, rr = s * .72 * r, r * (1 - .28 * s)
        return VGroup(*[Circle(rr, stroke_color=color, stroke_width=6, fill_color=color, fill_opacity=.1)
                        .move_to([cx + sg * d, cy, 0]) for sg in (-1, 1)])
    return always_redraw(mk)


def dim_chip(text, size=26):
    t = T(text, size=size, color=GREY).set_opacity(.55)
    box = DashedVMobject(RoundedRectangle(corner_radius=.14, width=t.width + .44, height=t.height + .44,
                                          stroke_color=GREY, stroke_width=2.5), num_dashes=22)
    return VGroup(box, t.move_to(box))


def make_tag(blob, text, lit, side, size=26):
    m = chip(text, PURPLE, size, fill_opacity=.3) if lit else dim_chip(text, size)
    m._t = side * 1.7

    def orb(mob, dt):
        mob._t += dt
        a = mob._t * 1.1
        mob.move_to(blob.get_center() + np.array([.25 * np.cos(a), side * .8 + .1 * np.sin(a), 0]))
    m.add_updater(orb)
    orb(m, 0)
    return m


def unit(cx, cy, lit2=True, scale=1.0):
    """The protein blob with its two job tags orbiting it; everything drifts gently."""
    blob = protein_blob(cx, cy, scale)
    blob._t, blob._o = cx * .3, np.zeros(3)

    def dr(m, dt):
        m._t += dt
        o = np.array([.16 * np.sin(.9 * m._t), .11 * np.cos(1.2 * m._t), 0])
        m.shift(o - m._o)
        m._o = o
    blob.add_updater(dr)
    t1, t2 = make_tag(blob, "job 1", True, 1), make_tag(blob, "job 2", lit2, -1)
    g = VGroup(blob, t1, t2)
    g.blob, g.t1, g.t2 = blob, t1, t2
    return g


def retag(u, which, lit):
    """Swap one job tag for a lit or dashed version; returns (old, new) to animate."""
    old = u.t1 if which == 1 else u.t2
    new = make_tag(u.blob, "job %d" % which, lit, 1 if which == 1 else -1)
    new._t = old._t
    if which == 1:
        u.t1 = new
    else:
        u.t2 = new
    return old, new


def drift(m, ax=.12, ay=.09, w=.8, ph=0.0):
    m._t, m._o = ph, np.zeros(3)

    def f(mob, dt):
        mob._t += dt
        o = np.array([ax * np.sin(w * mob._t + ph), ay * np.cos(1.3 * w * mob._t + ph), 0])
        mob.shift(o - mob._o)
        mob._o = o
    m.add_updater(f)
    return m


def rule_bar(pointer_x=0.0):
    box = RoundedRectangle(width=11.8, height=0.76, corner_radius=0.12, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.13).move_to([0, -3.18, 0])
    same = label("SAME", -2.85, -3.18, GREY, 30, weight=BOLD)
    diff = label("DIFFERENT", 2.85, -3.18, GOLD, 30, weight=BOLD)
    divider = Line([0, -3.52, 0], [0, -2.84, 0], color=TEXT, stroke_width=2)
    pointer = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.12).rotate(PI).move_to([pointer_x, -2.73, 0])
    return VGroup(box, same, diff, divider, pointer), pointer, same, diff


def timer(cx, y, w, V, ctrl=.4, h=.42):
    """Schematic 'time in mitosis' bar: grey up to the dashed control mark, gold beyond it."""
    x0 = cx - w / 2
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, y, 0])
    f1 = always_redraw(lambda: Rectangle(width=max(.001, min(V.get_value(), ctrl) * w), height=h - .08, stroke_width=0,
                                         fill_color=GREY, fill_opacity=.85).move_to(
        [x0 + max(.001, min(V.get_value(), ctrl) * w) / 2, y, 0]))
    f2 = always_redraw(lambda: Rectangle(width=max(.001, (V.get_value() - ctrl) * w), height=h - .08, stroke_width=0,
                                         fill_color=GOLD, fill_opacity=.9).move_to(
        [x0 + ctrl * w + max(.001, (V.get_value() - ctrl) * w) / 2, y, 0]))
    mark = DashedLine([x0 + ctrl * w, y - h / 2 - .12, 0], [x0 + ctrl * w, y + h / 2 + .12, 0], color=TEXT, stroke_width=3)
    return VGroup(frame, f1, f2, mark)


def check_mark(x, y, color=GREEN):
    return VGroup(Line([x - .22, y, 0], [x - .06, y - .18, 0], color=color, stroke_width=9),
                  Line([x - .06, y - .18, 0], [x + .26, y + .24, 0], color=color, stroke_width=9))


# ---------------------------------------------------------------------------------------------------
class S00Hook(TitleCard, SpokenScene):
    LESSON = "Experiments That Distinguish Mechanisms"
    TITLE = "Two Jobs, One Protein"

    def construct(self):
        Sl, Sr = creep(ValueTracker(.08), .012, .3), creep(ValueTracker(.08), .012, .3)
        self.add(Sl, Sr)
        dl, dr_ = div_cell(-3.15, .15, 2.05, TEAL, Sl), div_cell(3.15, .15, 2.05, ORANGE, Sr)
        ul, ur = unit(-3.15, .15), unit(3.15, .15)
        q = label("Which job did the cell miss?", 0, 3.3, TEXT, 38, weight=BOLD)
        self.play(FadeIn(dl), FadeIn(dr_), FadeIn(q), run_time=.9)
        self.play(FadeIn(ul), FadeIn(ur), run_time=.8)
        self.at("which job")
        self.play(*[Indicate(m, color=GOLD, scale_factor=1.2) for m in (ul.t1, ur.t1, ul.t2, ur.t2)], run_time=1.0)
        self.at("losing it")
        self.play(FadeOut(ul), FadeOut(ur), run_time=.9)
        self.at("rule can help")
        bar, pointer, same, diff = rule_bar(0)
        self.play(FadeIn(bar), run_time=.8)
        self.at("twins disagree")
        self.play(pointer.animate.move_to([2.85, -2.73, 0]), Indicate(diff, color=GOLD), run_time=.9)
        self.play(pointer.animate.move_to([0, -2.73, 0]), run_time=.8)
        self.at("put the protein")
        rl, rr = strand(-3.15, -2.55, PURPLE, 2.6), strand(3.15, -2.55, PURPLE, 2.6)
        labs = VGroup(label("resistant copy", -3.15, 2.8, PURPLE, 28), label("resistant copy", 3.15, 2.8, PURPLE, 28))
        self.play(FadeIn(labs), rl.animate.shift(UP * 1.35), rr.animate.shift(UP * 1.35), FadeIn(rl), FadeIn(rr), run_time=1.4)
        self.at("division recovered")
        self.play(FadeIn(ul), FadeIn(ur), FadeOut(rl), FadeOut(rr), FadeOut(labs), run_time=.7)
        Sl.clear_updaters(), Sr.clear_updaters()
        extra = VGroup(protein_blob(-1.7, .15), protein_blob(4.6, .15))
        self.play(Sl.animate.set_value(1), Sr.animate.set_value(1), ul.animate.shift(LEFT * 1.4), ur.animate.shift(LEFT * 1.4),
                  FadeIn(extra), run_time=1.6)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        Sl, Sr = creep(ValueTracker(.1), .02, .3), creep(ValueTracker(.1), .02, .3)
        self.add(Sl, Sr)
        cells = VGroup(div_cell(-3.15, -.35, 2.05, TEAL, Sl), div_cell(3.15, -.35, 2.05, ORANGE, Sr))
        ul, ur = unit(-3.15, -.35), unit(3.15, -.35)
        title = T("Two Jobs, One Protein", size=50, font=TITLE_FONT, color=TEXT, weight=BOLD).move_to([0, 3.0, 0])
        rule = Line([-2.0, 2.58, 0], [2.0, 2.58, 0], color=GOLD, stroke_width=4)
        self.add(cells, ul, ur)
        self.play(FadeIn(title, shift=DOWN * .12), GrowFromCenter(rule), run_time=.7)
        self.wait(1.3)


class S02Clathrin(SpokenScene):
    def construct(self):
        Y0 = 1.55
        xs = [-3.9, 0.0, 3.9]
        Dm = [ValueTracker(0) for _ in xs]
        Dc = [ValueTracker(0) for _ in xs]
        Vt = [ValueTracker(0) for _ in xs]
        Gt = [ValueTracker(0) for _ in xs]
        self.add(*Dm, *Dc, *Vt, *Gt)

        def ym(x):
            return Y0 - sum(1.3 * Dm[i].get_value() * np.exp(-((x - xs[i]) / .55) ** 2) for i in range(3))

        def pts():
            return [np.array([x, ym(x), 0]) for x in np.linspace(-6.8, 6.8, 160)]

        membrane = always_redraw(lambda: VMobject(stroke_color=TEAL, stroke_width=9).set_points_smoothly(pts()))
        interior = always_redraw(lambda: Polygon(np.array([-6.8, -3.8, 0]), *pts(), np.array([6.8, -3.8, 0]),
                                                 stroke_width=0, fill_color=TEAL, fill_opacity=.12).set_z_index(-1))
        self.add(interior, membrane)
        rng = np.random.RandomState(7)
        dxs = [-.55, -.2, .2, .55]
        sites = []
        for i, x0 in enumerate(xs):
            blobs = VGroup()
            for j, dx in enumerate(dxs):
                start = np.array([x0 + rng.uniform(-1.5, 1.5), Y0 - rng.uniform(.6, 2.3), 0])
                b = protein_blob(0, 0, .75)
                b._t = rng.uniform(0, 6)

                def place(m, dt, i=i, x0=x0, dx=dx, start=start):
                    m._t += dt
                    g = Gt[i].get_value()
                    wob = np.array([.14 * np.sin(.9 * m._t), .1 * np.cos(1.2 * m._t), 0]) * (1 - g)
                    coat = np.array([x0 + dx, ym(x0 + dx) - .24, 0])
                    m.move_to((1 - g) * start + g * coat + wob)
                b.add_updater(place)
                place(b, 0)
                blobs.add(b)
            dots = VGroup()
            for j, (dx, dy) in enumerate([(-.16, .1), (.12, 0), (0, .24)]):
                d = Dot(radius=.075, color=TEXT)

                def dplace(m, dt, i=i, x0=x0, dx=dx, dy=dy):
                    m.move_to([x0 + dx, Y0 - 1.3 * Dc[i].get_value() - 2.2 * Vt[i].get_value() + .32 + dy, 0])
                d.add_updater(dplace)
                dplace(d, 0)
                dots.add(d)
            ves = Circle(.4, stroke_color=PURPLE, stroke_width=8, fill_color=PURPLE, fill_opacity=.2)
            ves.add_updater(lambda m, dt, i=i, x0=x0: m.move_to([x0, Y0 - 1.3 * Dc[i].get_value() - 2.2 * Vt[i].get_value() + .45, 0]))
            ves.update(0)
            sites.append((blobs, dots, ves))
            self.add(blobs)

        def cycle(i):
            blobs, dots, ves = sites[i]
            return Succession(
                AnimationGroup(Gt[i].animate.set_value(1), FadeIn(dots), run_time=1.0),
                AnimationGroup(Dm[i].animate.set_value(1), Dc[i].animate.set_value(1), run_time=1.5),
                AnimationGroup(FadeOut(blobs), FadeIn(ves), Dm[i].animate.set_value(0), run_time=.6),
                Vt[i].animate.set_value(1).set_run_time(1.6))

        tag = label("schematic", 5.3, -3.45, GREY, 24)
        self.add(tag)
        self.wait(.4)
        self.at("clathrin")
        cl = label("clathrin", -3.9, -1.9, PURPLE, 34, weight=BOLD)
        self.play(FadeIn(cl), run_time=.7)
        self.at("more than one task")
        self.play(FadeOut(cl), cycle(0))
        self.at("endocytosis")
        self.play(FadeIn(label("endocytosis", -3.9, 3.0, TEXT, 38, weight=BOLD)), run_time=.7)
        self.at("coats small pockets")
        self.play(AnimationGroup(cycle(1), Succession(Wait(2.2), cycle(2)), lag_ratio=0))
        self.finish()


class S03Defect(SpokenScene):
    def construct(self):
        cy = .55
        S = creep(ValueTracker(0), 0, 0)
        V = ValueTracker(.1)
        self.add(S, V)
        cell = div_cell(0, cy, 2.0, GREY, S)
        msg = strand(0, cy + .75, PURPLE, 3.0)
        blobs = VGroup(*[drift(protein_blob(-1.1 + i * .73, cy - .5 + (.25 if i % 2 else 0), .65), ph=i) for i in range(4)])
        self.play(FadeIn(cell), Create(msg), LaggedStart(*[FadeIn(b) for b in blobs], lag_ratio=.12), run_time=1.3)
        self.at("silenced clathrin")
        hair = hairpin(3.6, cy + .75)
        hl = label("interference", 3.6, cy + 2.4, TEXT, 28)
        self.play(FadeIn(hair), FadeIn(hl), run_time=.5)
        self.play(hair.animate.move_to([.55, cy + .75, 0]), hl.animate.move_to([1.3, cy + 2.4, 0]), run_time=.8)
        frags = VGroup(*[Line([-.9 + i * .45, cy + .7, 0], [-.65 + i * .45, cy + .87, 0], color=PURPLE, stroke_width=5) for i in range(4)])
        self.play(ReplacementTransform(msg, frags), FadeOut(blobs), run_time=.7)
        self.play(FadeOut(hair), FadeOut(hl), frags.animate.set_opacity(.35), run_time=.5)
        self.at("dish")
        corner = label("Royle, Bright and Lagnado, 2005", 0, 3.5, GOLD, 28)
        self.play(FadeIn(corner), run_time=.6)
        self.at("mitosis")
        tm = timer(0, -2.55, 9.0, V, .33)
        tl = label("time in mitosis", -2.9, -3.3, TEXT, 28)
        ctl = label("control", -1.5, -2.0, TEXT, 26)
        sch = label("schematic", 5.0, -3.3, GREY, 24)
        self.play(FadeIn(tm), FadeIn(tl), FadeIn(ctl), FadeIn(sch), run_time=.8)
        creep(S, .12, .6)
        V.add_updater(lambda m, dt: m.set_value(min(.62, m.get_value() + .114 * dt)))
        self.at("took longer")
        self.wait(.2)
        self.at("clathrin matters")
        S.clear_updaters(), V.clear_updaters()
        self.play(S.animate.set_value(1), run_time=1.1)
        self.at("how")
        q = label("?", 0, 2.55, TEXT, 64, weight=BOLD)
        self.play(FadeIn(q, shift=DOWN * .2), run_time=.6)
        self.finish()


def twin_world(S1, S2, cy=.55, r=2.0):
    return VGroup(div_cell(-3.15, cy, r, TEAL, S1), div_cell(3.15, cy, r, ORANGE, S2))


class S04Models(SpokenScene):
    def construct(self):
        cy = .5
        S1, S2 = creep(ValueTracker(.05), .012, .3), creep(ValueTracker(.05), .012, .3)
        self.add(S1, S2)
        cells = twin_world(S1, S2, cy, 2.0)
        m1, m2 = label("Model 1", -3.15, 3.15, TEAL, 32), label("Model 2", 3.15, 3.15, ORANGE, 32)
        self.play(FadeIn(cells), FadeIn(m1), FadeIn(m2), run_time=.9)
        self.at("teal twin")
        p1, p2 = np.array([-3.15 - 1.3, cy, 0]), np.array([-3.15 + 1.3, cy, 0])
        fibres = VGroup(*[ArcBetweenPoints(p1, p2, angle=a, color=TEXT, stroke_width=3).set_stroke(opacity=.8) for a in (-1.0, -.5, 0.0001, .5, 1.0)])
        poles = VGroup(Dot(p1, radius=.1, color=TEXT), Dot(p2, radius=.1, color=TEXT))
        lb = VGroup(*[protein_blob(-3.15 + dx, cy + dy, .5) for dx, dy in [(-.8, 1.1), (-.3, -1.1), (.4, 1.2), (.9, -1.0)]])
        self.play(Create(fibres), FadeIn(poles), FadeIn(lb), run_time=1.0)
        self.at("clathrin works")
        fpts = [fibres[k].point_from_proportion(t) for k, t in [(0, .3), (1, .5), (3, .5), (4, .7)]]
        self.play(*[b.animate.move_to(p) for b, p in zip(lb, fpts)], run_time=.9)
        for b in lb:
            drift(b, .06, .05, 1.0, np.random.rand() * 5)
        self.at("mitosis itself")
        mit = chip("mitosis", TEAL, 30).move_to([-3.15, -2.45, 0])
        a1 = Arrow([-3.15, cy - 1.55, 0], [-3.15, -2.0, 0], buff=0, color=TEAL, stroke_width=5)
        self.play(GrowArrow(a1), FadeIn(mit), run_time=.9)
        self.at("orange twin")
        rim = [np.array([3.15 + 1.78 * np.cos(np.radians(th)), cy + 1.78 * np.sin(np.radians(th)), 0]) for th in (150, 90, 30)]
        rb = VGroup(*[protein_blob(p[0], p[1], .5) for p in rim])
        self.play(FadeIn(rb), run_time=.7)
        self.at("helps only through")
        ves = VGroup()
        for k, p in enumerate(rim):
            v = Circle(.13, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.3)
            v._t = k * .33
            c = np.array([3.15, cy, 0])

            def mv(m, dt, p=p, c=c):
                m._t = (m._t + dt * .3) % 1
                m.move_to(p + (c - p) * .38 * m._t)
                m.set_opacity(1 - m._t * .9)
                m.set_stroke(opacity=1 - m._t * .9)
            v.add_updater(mv)
            mv(v, 0)
            ves.add(v)
        self.add(ves)
        self.at("endocytosis")
        endo = chip("endocytosis", ORANGE, 30).move_to([2.0, -2.45, 0])
        mit2 = chip("mitosis", ORANGE, 30).move_to([5.5, -2.45, 0])
        a2 = Arrow([3.15, cy - 1.55, 0], [2.3, -2.0, 0], buff=0, color=ORANGE, stroke_width=5)
        self.play(GrowArrow(a2), FadeIn(endo), run_time=.9)
        self.at("division suffers")
        link = Arrow(endo.get_right() + RIGHT * .05, mit2.get_left() + LEFT * .05, buff=0, color=ORANGE, stroke_width=4)
        self.play(GrowArrow(link), FadeIn(mit2), run_time=.9)
        self.at("indirectly")
        self.play(Indicate(VGroup(endo, link, mit2), color=ORANGE, scale_factor=1.06), run_time=.9)
        self.at("over a few days")
        day = label("day 1", 0, -3.4, TEXT, 30, weight=BOLD)
        self.play(FadeIn(day), link.animate.set_stroke(width=6), run_time=.7)
        self.at("few days")
        d2 = label("day 2", 0, -3.4, TEXT, 30, weight=BOLD)
        self.play(Transform(day, d2), link.animate.set_stroke(width=9), run_time=.7)
        self.at("route")
        d3 = label("day 3", 0, -3.4, TEXT, 30, weight=BOLD)
        self.play(Transform(day, d3), link.animate.set_stroke(width=13), run_time=.8)
        self.finish()


def two_cells_timer(self_, cy=.75, r=1.85, S1v=.3, v0=.15):
    S1, S2 = creep(ValueTracker(S1v), .012, .3), creep(ValueTracker(S1v), .012, .3)
    V1, V2 = ValueTracker(v0), ValueTracker(v0)
    self_.add(S1, S2, V1, V2)
    cells = twin_world(S1, S2, cy, r)
    bars = VGroup(timer(-3.15, -1.75, 4.4, V1), timer(3.15, -1.75, 4.4, V2))
    labs = VGroup(label("time in mitosis", -3.15, -2.38, TEXT, 28), label("time in mitosis", 3.15, -2.38, TEXT, 28))
    return S1, S2, V1, V2, cells, bars, labs


def four_blobs(cx, cy):
    return VGroup(*[drift(protein_blob(cx + dx, cy - .3 + dy, .65), ph=dx + cx)
                    for dx, dy in [(-.7, 0), (-.2, -.5), (.35, .1), (.75, -.45)]])


class S05RescuePredict(SpokenScene):
    def construct(self):
        cy = .75
        S1, S2, V1, V2, cells, bars, labs = two_cells_timer(self, cy)
        strands = VGroup(strand(-3.15, cy + .6, PURPLE, 2.6), strand(3.15, cy + .6, PURPLE, 2.6))
        ul, ur = four_blobs(-3.15, cy), four_blobs(3.15, cy)
        self.play(FadeIn(cells), FadeIn(bars), FadeIn(labs), Create(strands), FadeIn(ul), FadeIn(ur), run_time=1.4)
        self.at("silence clathrin")
        hairs = VGroup(hairpin(-1.3, cy + 1.2), hairpin(5.0, cy + 1.2))
        self.play(FadeIn(hairs), run_time=.4)
        self.play(hairs[0].animate.move_to([-3.6, cy + .6, 0]), hairs[1].animate.move_to([2.7, cy + .6, 0]), run_time=.9)
        frags = VGroup(*[Line([c - .9 + i * .45, cy + .55, 0], [c - .65 + i * .45, cy + .72, 0], color=PURPLE, stroke_width=5)
                         for c in (-3.15, 3.15) for i in range(4)])
        self.play(ReplacementTransform(strands, frags), FadeOut(ul), FadeOut(ur),
                  V1.animate.set_value(.92), V2.animate.set_value(.92), run_time=1.3)
        self.play(frags.animate.set_opacity(.3), run_time=.2)
        self.at("put back the whole protein")
        rs = VGroup(strand(-3.15, -.75, PURPLE, 2.8), strand(3.15, -.75, PURPLE, 2.8))
        rlab = VGroup(label("full-length, resistant", -3.15, 3.0, PURPLE, 28), label("full-length, resistant", 3.15, 3.0, PURPLE, 28))
        self.play(FadeIn(rlab), FadeIn(rs), rs.animate.shift(UP * .35), run_time=1.2)
        self.at("interference cannot")
        self.play(hairs[0].animate.move_to([-3.15, cy + .1, 0]), hairs[1].animate.move_to([3.15, cy + .1, 0]), run_time=.6)
        self.play(hairs[0].animate.move_to([-6.0, cy - .4, 0]), hairs[1].animate.move_to([6.2, cy - .4, 0]), run_time=.5)
        self.at("touch")
        ul2, ur2 = four_blobs(-3.15, cy), four_blobs(3.15, cy)
        self.play(FadeOut(hairs), FadeOut(frags), FadeIn(ul2), FadeIn(ur2), run_time=.8)
        self.at("returns to normal")
        self.play(FadeOut(rs), FadeOut(rlab), run_time=.7)
        self.at("does that choose")
        q = label("Does rescue choose?", 0, 3.4, TEXT, 40, weight=BOLD)
        self.play(FadeIn(q, shift=DOWN * .15), run_time=.8)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        cy = .75
        S1, S2, V1, V2, cells, bars, labs = two_cells_timer(self, cy, 1.85, .2, .92)
        ul, ur = four_blobs(-3.15, cy), four_blobs(3.15, cy)
        q = label("Does rescue choose?", 0, 3.4, TEXT, 40, weight=BOLD)
        self.add(cells, bars, labs, ul, ur, q)
        self.wait(4.5)


class S07Same(SpokenScene):
    def construct(self):
        cy = .75
        S1, S2, V1, V2, cells, bars, labs = two_cells_timer(self, cy, 1.85, .2, .92)
        ul, ur = unit(-3.15, cy, True), unit(3.15, cy, True)
        q = label("Does rescue choose?", 0, 3.4, TEXT, 40, weight=BOLD)
        self.add(cells, bars, labs, ul.blob, ur.blob, q)
        self.at("cannot")
        self.play(FadeOut(q), run_time=.6)
        self.at("whole protein")
        self.play(FadeIn(ul.t1), FadeIn(ur.t1), run_time=.7)
        self.at("both jobs")
        self.play(FadeIn(ul.t2), FadeIn(ur.t2), run_time=.7)
        self.at("both twins predict")
        sb = RoundedRectangle(width=11.8, height=.76, corner_radius=.12, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.4).move_to([0, -3.18, 0])
        st = label("SAME: both rescue", 0, -3.18, TEXT, 32, weight=BOLD)
        self.play(V1.animate.set_value(.4), V2.animate.set_value(.4), FadeIn(sb), FadeIn(st), run_time=1.6)
        self.at("did rescue mitosis")
        tick = check_mark(-4.3, 3.45)
        cl = label("Royle and colleagues, 2005", 0, 3.45, GOLD, 28)
        self.play(Create(tick), FadeIn(cl), run_time=.9)
        self.at("which job")
        qm = label("?", 0, cy, TEXT, 70, weight=BOLD)
        self.play(FadeIn(qm, scale=1.3), run_time=.7)
        self.finish()


class S08Fragment(SpokenScene):
    def construct(self):
        cy = .6
        S = creep(ValueTracker(.05), .012, .3)
        V = ValueTracker(.62)
        self.add(S, V)
        cell = div_cell(-2.3, cy, 2.0, GREY, S)
        tm = timer(0, -2.55, 9.0, V, .33)
        tl = label("time in mitosis", -2.9, -3.3, TEXT, 28)
        ctl = label("control", -1.5, -2.0, TEXT, 26)
        sch = label("schematic", 5.0, -3.3, GREY, 24)
        self.play(FadeIn(cell), FadeIn(tm), FadeIn(tl), FadeIn(ctl), FadeIn(sch), run_time=1.0)
        self.at("front part")
        st = strand(-2.3, -1.0, PURPLE, 1.6)
        lab = label("front part only", -2.3, 3.1, PURPLE, 30)
        self.play(FadeIn(st), FadeIn(lab), st.animate.shift(UP * 1.3), run_time=.8)
        self.at("clathrin")
        half = VGroup(*[drift(protein_blob(-3.0 + i * .7, cy - .35 + (.3 if i % 2 else 0), .38), ph=i) for i in range(3)])
        self.play(FadeIn(half), run_time=.8)
        self.at("not rescue")
        self.play(Indicate(tm[2], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("hard to read")
        boxes = VGroup(*[Square(.46, stroke_color=TEXT, stroke_width=4).move_to([2.9, y, 0]) for y in (1.9, .75, -.4)])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=.3), run_time=1.5)
        self.at("wrong level")
        l1 = label("amount", 4.55, 1.9, TEXT, 30)
        self.play(FadeIn(l1), Indicate(boxes[0], color=GOLD), run_time=.8)
        self.at("fold badly")
        l2 = label("folded", 4.55, .75, TEXT, 30)
        self.play(FadeIn(l2), Indicate(boxes[1], color=GOLD), run_time=.8)
        self.at("wrong place")
        l3 = label("place", 4.55, -.4, TEXT, 30)
        self.play(FadeIn(l3), Indicate(boxes[2], color=GOLD), run_time=.8)
        self.finish()


class S09Separation(SpokenScene):
    def construct(self):
        cy = .95
        S1, S2 = creep(ValueTracker(.05), .012, .3), creep(ValueTracker(.05), .012, .3)
        self.add(S1, S2)
        cells = twin_world(S1, S2, cy, 1.8)
        ul, ur = unit(-3.15, cy, True), unit(3.15, cy, True)
        bar, pointer, same, diff = rule_bar(-2.85)
        self.play(FadeIn(cells), FadeIn(ul), FadeIn(ur), FadeIn(bar), run_time=1.1)
        self.at("change the protein itself")
        self.play(Indicate(ul.blob, color=GOLD, scale_factor=1.25), Indicate(ur.blob, color=GOLD, scale_factor=1.25), run_time=1.0)
        self.at("resistant copy")
        rs = VGroup(strand(-3.15, -1.0, PURPLE, 2.4), strand(3.15, -1.0, PURPLE, 2.4))
        rlab = VGroup(label("one job only", -3.15, 3.1, PURPLE, 30), label("one job only", 3.15, 3.1, PURPLE, 30))
        self.play(FadeIn(rlab), FadeIn(rs), rs.animate.shift(UP * .35), run_time=1.3)
        self.at("loses the other")
        o1, n1 = retag(ul, 2, False)
        o2, n2 = retag(ur, 2, False)
        self.play(FadeOut(o1), FadeOut(o2), FadeIn(n1), FadeIn(n2), FadeOut(rs), run_time=1.0)
        self.at("separation of function")
        self.play(Indicate(rlab, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.at("one job still works")
        c1 = label("job 1 works", -2.4, -1.55, GREEN, 30, weight=BOLD)
        self.play(FadeIn(c1), run_time=.7)
        self.at("other does not")
        c2 = label("job 2 lost", 2.4, -1.55, RED, 30, weight=BOLD)
        self.play(FadeIn(c2), FadeOut(rlab), pointer.animate.move_to([2.85, -2.73, 0]), run_time=.9)
        self.play(Indicate(diff, color=GOLD), run_time=.5)
        self.at("then check")
        c3 = label("amount · folding · location", 0, -2.15, TEXT, 30)
        self.play(FadeIn(c3), run_time=.8)
        self.finish()


class S10Handoff(SpokenScene):
    def construct(self):
        cy = -.1
        S1, S2 = creep(ValueTracker(.05), .012, .3), creep(ValueTracker(.05), .012, .3)
        self.add(S1, S2)
        cells = twin_world(S1, S2, cy, 2.2)
        ul, ur = unit(-3.15, cy, False), unit(3.15, cy, False)
        corner = label("Royle and Lagnado, 2006", -3.7, 3.58, GOLD, 26)
        self.play(FadeIn(cells), FadeIn(ul), FadeIn(ur), FadeIn(corner), run_time=1.2)
        self.at("what does each twin")
        q = label("What does each twin predict?", 0, 2.95, TEXT, 38, weight=BOLD)
        self.play(FadeIn(q, shift=DOWN * .15), run_time=.8)
        self.at("text below")
        arrow = Arrow([0, -2.5, 0], [0, -3.65, 0], buff=0, color=GOLD, stroke_width=10)
        arrow._t = 0.0

        def bob(m, dt):
            m._t += dt
            m.shift(DOWN * .006 * np.sin(m._t * 4))
        arrow.add_updater(bob)
        self.play(GrowArrow(arrow), run_time=.8)
        self.finish()


def mini_panel(cx, cy, title, status, color):
    frame = RoundedRectangle(width=5.8, height=2.55, corner_radius=.15, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=.07).move_to([cx, cy, 0])
    t = label(title, cx, cy + .95, TEXT, 28, weight=BOLD)
    cs = VGroup(Circle(.5, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.15).move_to([cx - 1.4, cy + .1, 0]),
                Circle(.5, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=.15).move_to([cx + 1.4, cy + .1, 0]),
                protein_blob(cx - 1.4, cy + .1, .55), protein_blob(cx + 1.4, cy + .1, .55))
    sb = RoundedRectangle(width=4.6, height=.6, corner_radius=.1, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=.18).move_to([cx, cy - .85, 0])
    st = label(status, cx, cy - .85, color, 28, weight=BOLD)
    return VGroup(frame, t, cs, sb, st)


class S11Return(SpokenScene):
    def construct(self):
        S1, S2 = creep(ValueTracker(.05), .012, .3), creep(ValueTracker(.05), .012, .3)
        self.add(S1, S2)
        cells = twin_world(S1, S2, 2.05, 1.35)
        bl = VGroup(drift(protein_blob(-3.15, 2.05, .8), .1, .08), drift(protein_blob(3.15, 2.05, .8), .1, .08, 1.0, 2))
        self.play(FadeIn(cells), FadeIn(bl), run_time=.3)
        self.at("rescue answers")
        p1 = mini_panel(-3.2, -1.55, "full-length rescue", "SAME", GREY)
        p1.shift(LEFT * 7)
        dim = RoundedRectangle(width=5.8, height=2.55, corner_radius=.15, stroke_width=0, fill_color=BG, fill_opacity=0).move_to([-3.2, -1.55, 0])
        self.play(FadeIn(p1), p1.animate.shift(RIGHT * 7), run_time=1.1)
        self.add(dim)
        self.at("cause the defect")
        self.play(Indicate(p1, color=TEXT, scale_factor=1.04), run_time=.9)
        self.at("which job")
        p2 = mini_panel(3.2, -1.55, "one job only", "DIFFERENT", GOLD)
        p2.shift(RIGHT * 7)
        self.play(FadeIn(p2), p2.animate.shift(LEFT * 7), dim.animate.set_fill(BG, opacity=.65), run_time=1.1)
        self.play(Indicate(p2, color=GOLD, scale_factor=1.04), run_time=.8)
        self.at("write down")
        cards = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=.5, corner_radius=.08, stroke_color=TEXT, stroke_width=3,
                                                 fill_color=TEXT, fill_opacity=.08).move_to([x, .2, 0]),
                                Line([x - 1.0, .2, 0], [x + 1.0, .2, 0], color=GREY, stroke_width=2))
                         for x in (-3.15, 3.15)])
        self.play(FadeIn(cards, shift=UP * .15), run_time=.8)
        self.at("rescue supports")
        self.play(dim.animate.set_fill(BG, opacity=0), *[Flash(c, color=TEXT, flash_radius=1.6, line_length=.3) for c in (np.array([-3.15, 2.05, 0]), np.array([3.15, 2.05, 0]))],
                  run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Rescue supports the protein's role; split its jobs to learn which."
