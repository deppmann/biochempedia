"""Island biogeography: same count, different species  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = species present on the island (and richness, S)
  GREEN  = immigration / a newly arrived species
  RED    = extinction / a species that was lost
  YELLOW = the equilibrium (the crossing, S*) and the unknown ("?")
  TEAL   = the Jaccard comparison (shared, in either)
  GREY   = axes, island outlines, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class RatePlot:
    """Rate against richness, I(S)=10(1-S/100), E(S)=0.1S. Sizes of text do not depend on the plot size."""

    def __init__(self, xl, yl, center):
        self.ax = Axes(x_range=[0, 100, 50], y_range=[0, 11, 5], x_length=xl, y_length=yl, tips=False,
                       axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}).move_to(center)
        ax = self.ax
        ticks = VGroup(
            M("0", 22, GREY).next_to(ax.c2p(0, 0), DOWN, 0.18),
            M("100", 22, GREY).next_to(ax.c2p(100, 0), DOWN, 0.18),
            M("0", 22, GREY).next_to(ax.c2p(0, 0), LEFT, 0.18),
            M("5", 22, GREY).next_to(ax.c2p(0, 5), LEFT, 0.18),
            M("10", 22, GREY).next_to(ax.c2p(0, 10), LEFT, 0.18),
        )
        xlab = T("species on the island, S", 22, GREY).next_to(ax.c2p(50, 0), DOWN, 0.62)
        ylab = T("species per day", 22, GREY).next_to(ax.c2p(0, 11), UP, 0.12).align_to(ax.c2p(0, 0), LEFT)
        self.base = VGroup(ax, ticks, xlab, ylab)

    def p(self, s, y):
        return self.ax.c2p(s, y)

    def I(self):
        return self.ax.plot(lambda s: 10 * (1 - s / 100), x_range=[0, 100], color=GREEN, stroke_width=6)

    def E(self):
        return self.ax.plot(lambda s: 0.1 * s, x_range=[0, 100], color=RED, stroke_width=6)

    def star(self):
        d = DashedLine(self.p(50, 0), self.p(50, 5), color=YELLOW, stroke_width=3)
        lab = M("S* = 50", 22, YELLOW).next_to(self.p(50, 0), DOWN, 0.18)
        return d, lab


def sketch_tag():
    return T("in this sketch", 22, GREY).move_to([5.3, 3.2, 0])


def island_outline(w, h, center):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to(center)


def dot(color, r=0.2):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.85)


def grid_pts(cx, cy, cols, rows, dx, dy):
    return [np.array([cx + (c - (cols - 1) / 2) * dx, cy + ((rows - 1) / 2 - r) * dy, 0])
            for r in range(rows) for c in range(cols)]


def legend(items, y=-3.2):
    g = VGroup()
    for color, text in items:
        g.add(VGroup(dot(color, 0.14), T(text, 22, color)).arrange(RIGHT, buff=0.15))
    g.arrange(RIGHT, buff=0.7).move_to([0, y, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Island biogeography"
    TITLE = "Same count, different species"


# ---------------------------------------------------------------------------------------------
class S01Empty(SpokenScene):
    """island of species dots -> emptied -> ? -> count back, but some species lost and some new."""
    LOST = [1, 4, 6, 11]

    def construct(self):
        centre = np.array([0, -0.2, 0])
        isl = island_outline(7.6, 4.6, centre)
        pts = grid_pts(0, -0.2, 4, 3, 1.2, 1.15)
        dots = VGroup(*[dot(BLUE, 0.33).move_to(p) for p in pts])
        tag = T("before", 26, GREY).move_to([0, 2.85, 0])
        self.at("Empty an island")
        self.play(FadeIn(isl), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.05), FadeIn(tag), run_time=0.9)
        self.at("every insect and spider")
        self.play(*[d.animate.set_color(RED).scale(0.3).set_opacity(0) for d in dots], FadeOut(tag), run_time=1.1)
        empty = T("emptied", 26, GREY).move_to([0, 2.85, 0])
        q = T("?", 120, YELLOW, weight=BOLD).move_to(centre)
        self.play(FadeIn(empty), run_time=0.4)
        self.at("How many species")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("In the Florida Keys")
        place = T("small mangrove island, Florida Keys", 26, GREY).move_to([0, 2.85, 0])
        self.play(ReplacementTransform(empty, place), run_time=0.6)
        self.at("Within about")
        new_dots = VGroup(*[dot(BLUE, 0.33).move_to(p) for p in pts])
        self.play(FadeOut(q), LaggedStart(*[GrowFromCenter(d) for d in new_dots], lag_ratio=0.25),
                  run_time=max(2.0, self.t_of("untreated islands") - self.elapsed() - 0.3))
        self.at("untreated islands")
        same = T("about as many species", 26, BLUE).move_to([0, -3.05, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("not all the ones")
        # split into a "before" island on the left and the refilled island on the right
        left_isl = island_outline(6.0, 4.0, [-3.3, -0.2, 0])
        left_pts = grid_pts(-3.3, -0.2, 4, 3, 1.0, 0.95)
        left_dots = VGroup(*[dot(BLUE, 0.26).move_to(p) for p in left_pts])
        right_pts = grid_pts(3.3, -0.2, 4, 3, 1.0, 0.95)
        lt = T("before", 26, GREY).move_to([-3.3, 2.3, 0])
        rt = T("after", 26, GREY).move_to([3.3, 2.3, 0])
        right_dots = VGroup(*[dot(BLUE, 0.26).move_to(p) for p in right_pts])
        self.play(FadeOut(isl), FadeOut(place), FadeOut(same),
                  FadeOut(new_dots), FadeIn(left_isl), FadeIn(left_dots), FadeIn(lt),
                  FadeIn(island_outline(6.0, 4.0, [3.3, -0.2, 0])), FadeIn(right_dots), FadeIn(rt), run_time=1.2)
        lg = legend([(BLUE, "still there"), (RED, "lost"), (GREEN, "new")], y=-2.95)
        sch = T("schematic dots: 12 species, 4 lost, 4 new", 22, GREY).move_to([0, -3.4, 0])
        self.add(sch)
        self.play(*[left_dots[i].animate.set_color(RED) for i in self.LOST],
                  *[right_dots[i].animate.set_color(GREEN) for i in self.LOST], FadeIn(lg), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Arrive(SpokenScene):
    """immigration curve: falls from 10 per day to 0 as the island fills toward the pool of 100."""

    def construct(self):
        rp = RatePlot(10.4, 4.5, [0.4, -0.35, 0])
        self.at("two rates")
        self.play(FadeIn(rp.base), run_time=0.8)
        curve = rp.I()
        chip_i = chip("immigration", GREEN, size=26).move_to(rp.p(38, 8.9))
        self.at("The first is immigration")
        self.play(Create(curve), FadeIn(chip_i), FadeIn(sketch_tag()), run_time=1.2)
        self.at("every arriving species is new")
        d = Dot(rp.p(0, 10), radius=0.13, color=GREEN)
        call = T("S = 0: every arrival is new", 22, GREEN).move_to(rp.p(70, 10.0))
        self.play(FadeIn(d, scale=2), FadeIn(call), run_time=0.6)
        self.at("As the island fills")
        seg = Line(rp.p(0, 0), rp.p(0, 0), color=BLUE, stroke_width=10)
        tr = ValueTracker(0)
        seg.add_updater(lambda m: m.put_start_and_end_on(rp.p(0, 0), rp.p(tr.get_value(), 0)))
        d.add_updater(lambda m: m.move_to(rp.p(tr.get_value(), 10 * (1 - tr.get_value() / 100))))
        self.add(seg)
        call2 = T("more arrivals are already here", 22, BLUE).move_to(rp.p(70, 10.0))
        run = max(2.0, self.t_of("reaches zero") - self.elapsed() - 0.4)
        self.play(ReplacementTransform(call, call2), tr.animate.set_value(100).set_rate_func(linear), run_time=run)
        self.at("reaches zero")
        d.clear_updaters()
        pool = T("pool: 100 species", 22, BLUE).move_to(rp.p(78, 4.8))
        self.play(Indicate(d, color=GREEN, scale_factor=2), FadeIn(pool), run_time=0.7)
        self.at("invented numbers")
        inv = T("invented numbers", 22, GREY).move_to([5.3, 2.75, 0])
        self.play(FadeIn(inv), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Leave(SpokenScene):
    """add the extinction line; the two curves cross at S* = 50."""

    def construct(self):
        rp = RatePlot(10.4, 4.5, [0.4, -0.35, 0])
        curve = rp.I()
        chip_i = chip("immigration", GREEN, size=26).move_to(rp.p(38, 8.9))
        tag = sketch_tag()
        inv = T("invented numbers", 22, GREY).move_to([5.3, 2.75, 0])
        self.add(rp.base, curve, chip_i, tag, inv)
        self.at("The second rate")
        line = rp.E()
        chip_e = chip("extinction", RED, size=26).move_to(rp.p(76, 10.0))
        self.play(Create(line), FadeIn(chip_e), run_time=1.0)
        self.at("local extinction")
        call = T("loss of a species from that island", 22, RED).move_to(rp.p(45, 1.0))
        self.play(FadeIn(call), run_time=0.5)
        self.at("rises in proportion")
        self.play(Indicate(line, color=RED, scale_factor=1.0), run_time=0.9)
        self.at("Draw both curves")
        self.play(FadeOut(call), run_time=0.4)
        self.at("cross at one point")
        x = Dot(rp.p(50, 5), radius=0.2, color=YELLOW)
        self.play(FadeIn(x, scale=3), run_time=0.6)
        self.at("That is the equilibrium")
        self.play(Indicate(x, color=YELLOW, scale_factor=1.8), run_time=0.8)
        d, lab = rp.star()
        self.at("In our example")
        self.play(Create(d), FadeIn(lab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Settle(SpokenScene):
    """stability from both sides, then richness against time from an empty island."""

    def construct(self):
        big = RatePlot(10.4, 4.5, [0.4, -0.35, 0])
        small = RatePlot(4.9, 3.3, [-3.55, -0.3, 0])

        def full(rp):
            d, lab = rp.star()
            x = Dot(rp.p(50, 5), radius=0.17, color=YELLOW)
            return VGroup(rp.base, rp.I(), rp.E(), d, lab, x)

        A = full(big)
        tag = sketch_tag()
        inv = T("invented numbers", 22, GREY).move_to([5.3, 2.75, 0])
        self.add(A, tag, inv)
        mk = Dot(big.p(80, 0), radius=0.18, color=BLUE)
        self.at("Above it")
        ar1 = Arrow(big.p(80, 0.0), big.p(62, 0.0), buff=0.05, color=BLUE, stroke_width=7)
        t1 = T("richness falls", 22, BLUE).move_to(big.p(81, 5))
        self.play(FadeIn(mk, scale=2), GrowArrow(ar1), FadeIn(t1), run_time=0.8)
        self.at("Below it")
        mk2 = Dot(big.p(20, 0), radius=0.18, color=BLUE)
        ar2 = Arrow(big.p(20, 0.0), big.p(38, 0.0), buff=0.05, color=BLUE, stroke_width=7)
        t2 = T("richness rises", 22, BLUE).move_to(big.p(19, 5))
        self.play(FadeOut(mk), FadeOut(ar1), FadeOut(t1), FadeIn(mk2, scale=2), GrowArrow(ar2), FadeIn(t2), run_time=0.8)
        self.at("empty island")
        B = full(small)
        ax2 = Axes(x_range=[0, 25, 5], y_range=[0, 60, 10], x_length=4.9, y_length=3.3, tips=False,
                   axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}).move_to([3.55, -0.3, 0])
        tk = VGroup(M("0", 22, GREY).next_to(ax2.c2p(0, 0), DOWN, 0.18), M("20", 22, GREY).next_to(ax2.c2p(20, 0), DOWN, 0.18),
                    M("0", 22, GREY).next_to(ax2.c2p(0, 0), LEFT, 0.18), M("50", 22, GREY).next_to(ax2.c2p(0, 50), LEFT, 0.18))
        xl2 = T("days", 22, GREY).next_to(ax2.c2p(12.5, 0), DOWN, 0.62)
        yl2 = T("species, S", 22, GREY).next_to(ax2.c2p(0, 60), UP, 0.12).align_to(ax2.c2p(0, 0), LEFT)
        dash50 = DashedLine(ax2.c2p(0, 50), ax2.c2p(25, 50), color=YELLOW, stroke_width=3)
        self.play(FadeOut(mk2), FadeOut(ar2), FadeOut(t2), ReplacementTransform(A, B),
                  FadeOut(inv), tag.animate.move_to([0, 3.2, 0]),
                  FadeIn(VGroup(ax2, tk, xl2, yl2, dash50)), run_time=1.2)
        tr = ValueTracker(0)
        f = lambda t: 50 * (1 - np.exp(-0.2 * t))
        curve = always_redraw(lambda: ax2.plot(f, x_range=[0, max(tr.get_value(), 0.02)], color=BLUE, stroke_width=6))
        mover = always_redraw(lambda: Dot(small.p(f(tr.get_value()), 0), radius=0.14, color=BLUE))
        head = always_redraw(lambda: Dot(ax2.c2p(tr.get_value(), f(tr.get_value())), radius=0.12, color=BLUE))
        self.add(curve, mover, head)
        self.at("climbs fast")
        self.play(tr.animate.set_value(25).set_rate_func(linear), run_time=min(5.0, max(2.5, self.t_of("reaches") - self.elapsed() - 0.3)))
        mover.clear_updaters(); head.clear_updaters(); curve.clear_updaters()
        self.at("It reaches")
        px, py = 11.5, 45
        lines = VGroup(DashedLine(ax2.c2p(px, 0), ax2.c2p(px, py), color=YELLOW, stroke_width=3),
                       DashedLine(ax2.c2p(0, py), ax2.c2p(px, py), color=YELLOW, stroke_width=3))
        mk3 = Dot(ax2.c2p(px, py), radius=0.15, color=YELLOW)
        lab = VGroup(T("45 species", 22, YELLOW), T("at 11.5 days", 22, YELLOW)).arrange(DOWN, buff=0.1).move_to(ax2.c2p(17, 25))
        self.play(Create(lines), FadeIn(mk3, scale=2), FadeIn(lab), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Turnover(SpokenScene):
    """fifty dots; five green arrive, five blue leave; count holds, membership changes."""

    def construct(self):
        cy = 0.55
        isl = island_outline(7.4, 4.1, [0, cy, 0])
        pts = grid_pts(0, cy, 10, 5, 0.6, 0.58)
        dots = [dot(BLUE, 0.17).move_to(p) for p in pts]
        group = VGroup(*dots)
        count = M("50 species", 34, BLUE).move_to([0, 2.95, 0])
        self.at("At the crossing")
        self.play(FadeIn(isl), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.01), run_time=0.7)
        mlab = T("model island (S* = 50)", 22, GREY).move_to([-4.6, 2.95, 0])
        self.add(mlab)
        lg = legend([(BLUE, "there at the start"), (GREEN, "arrived since"), (RED, "went extinct")], y=-1.95)
        self.add(lg)
        rng = np.random.RandomState(4)
        order = list(rng.permutation(50))
        used = []

        def pick(n):
            out = []
            for i in order:
                if i not in used and len(out) < n and dots[i].get_color() is not None:
                    out.append(i)
            used.extend(out)
            return out

        slots1 = pick(5)
        chip_in = chip("5 arrive", GREEN, size=22).move_to([5.3, cy + 0.9, 0])
        chip_out = chip("5 go extinct", RED, size=22).move_to([-5.1, cy + 0.9, 0])
        waiting1 = [dot(GREEN, 0.17).move_to([4.05, cy + 0.9 - 0.45 * (k - 2), 0]) for k in range(5)]
        self.at("five species arrive")
        self.play(FadeIn(chip_in, shift=LEFT * 0.2), *[GrowFromCenter(w) for w in waiting1], run_time=0.7)
        self.at("go extinct")
        self.play(FadeIn(chip_out, shift=RIGHT * 0.2),
                  *[dots[i].animate.set_color(RED) for i in slots1], run_time=0.4)
        anims = []
        for i, w in zip(slots1, waiting1):
            anims.append(dots[i].animate.move_to([-4.35, cy + 0.9 - 0.45 * (slots1.index(i) - 2), 0]).set_opacity(0))
            anims.append(w.animate.move_to(pts[i]))
        self.play(*anims, run_time=1.2)
        for i, w in zip(slots1, waiting1):
            dots[i] = w
        net = M("+5  -5  =  0 per day", 30, TEXT).move_to([0, -2.6, 0])
        self.at("Net change")
        self.play(FadeIn(net), run_time=0.5)
        self.at("the count holds")
        self.play(FadeIn(count), run_time=0.5)
        self.at("But the species are changing")
        self.play(*[Indicate(dots[i], color=GREEN, scale_factor=1.6) for i in slots1], run_time=0.8)
        self.at("replaced every day")
        slots2 = [i for i in order if i not in used][:5]
        used.extend(slots2)
        waiting2 = [dot(GREEN, 0.17).move_to([4.05, cy + 0.9 - 0.45 * (k - 2), 0]) for k in range(5)]
        self.play(*[GrowFromCenter(w) for w in waiting2], *[dots[i].animate.set_color(RED) for i in slots2], run_time=0.5)
        anims = []
        for k, (i, w) in enumerate(zip(slots2, waiting2)):
            anims.append(dots[i].animate.move_to([-4.35, cy + 0.9 - 0.45 * (k - 2), 0]).set_opacity(0))
            anims.append(w.animate.move_to(pts[i]))
        self.play(*anims, run_time=1.2)
        for i, w in zip(slots2, waiting2):
            dots[i] = w
        self.at("the second year")
        note = VGroup(T("Real census, Florida Keys, second year:", 24, GREY),
                      T("species numbers changed little; immigrations and extinctions continued", 24, GREY)).arrange(DOWN, buff=0.12).move_to([0, -2.5, 0])
        self.play(FadeOut(net), FadeOut(lg), FadeIn(note), isl.animate.set_opacity(0.3), *[d.animate.set_opacity(0.3) for d in dots], FadeOut(count), run_time=0.6)
        self.at("dynamic equilibrium")
        ce = chip("dynamic equilibrium", YELLOW, size=30).move_to([0, -2.7, 0])
        self.play(ReplacementTransform(note, ce), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Jaccard(SpokenScene):
    """two species lists on one island: richness 2 and 2, shared 1, in either 3, similarity 1/3."""

    def construct(self):
        r = 2.3
        cl, cr = np.array([-1.3, 0.3, 0]), np.array([1.3, 0.3, 0])
        c1 = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to(cl)
        c2 = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to(cr)

        def sp(name, color, pos):
            return T(name, 24, color, slant=ITALIC).move_to(pos)

        amb = sp("Amblyseius", BLUE, [-2.35, 0.3, 0])
        bde = sp("Bdella", BLUE, [0, 0.3, 0])
        car = sp("Carpoglyphus", BLUE, [2.35, 0.3, 0])
        self.at("does not say")
        sub = T("a selection of three mite groups, one mangrove island", 26, GREY).move_to([0, 0.3, 0])
        self.play(FadeIn(sub), run_time=0.5)
        self.at("Take a selection")
        self.play(sub.animate.move_to([0, 3.3, 0]), FadeIn(c1), FadeIn(c2), run_time=0.9)
        h1 = T("before treatment", 24, GREY).move_to([-3.0, 2.85, 0])
        h2 = T("a year later", 24, GREY).move_to([3.0, 2.85, 0])
        self.at("Before treatment")
        n1 = M("2 present", 24, BLUE).move_to([-2.4, -2.35, 0])
        self.play(FadeIn(h1), FadeIn(amb), FadeIn(bde), FadeIn(n1), FadeOut(sub), run_time=0.7)
        self.at("A year later")
        n2 = M("2 present", 24, BLUE).move_to([2.4, -2.35, 0])
        self.play(FadeIn(h2), FadeIn(car), FadeIn(n2), run_time=0.7)
        inter = Intersection(c1, c2, fill_color=TEAL, fill_opacity=0.28, stroke_width=0)
        self.at("both lists")
        sh = M("shared: 1", 24, TEAL).move_to([0, -2.35, 0])
        self.play(FadeIn(inter), FadeIn(sh), run_time=0.7)
        self.at("found in either")
        uni = Union(c1, c2, stroke_color=TEAL, stroke_width=5, fill_opacity=0).set_stroke(TEAL, 5)
        eth = M("in either: 3", 24, TEAL).move_to([0, 3.0, 0])
        self.play(Create(uni), FadeIn(eth), run_time=0.9)
        self.at("divide the species")
        frm = T("shared / in either", 32, TEAL).move_to([0, -3.15, 0])
        self.play(FadeIn(frm, shift=UP * 0.15), run_time=0.6)
        self.at("That is the")
        frm2 = T("Jaccard similarity  =  shared / in either", 32, TEAL).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(frm, frm2), run_time=0.6)
        self.at("Here it is")
        frm3 = T("Jaccard similarity  =  1 / 3  =  0.33", 32, TEAL).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(frm2, frm3), run_time=0.6)
        self.at("A steady count")
        lost = T("lost", 22, RED).next_to(amb, DOWN, 0.15)
        new = T("new", 22, GREEN).next_to(car, DOWN, 0.15)
        self.play(amb.animate.set_color(RED), car.animate.set_color(GREEN), FadeIn(lost), FadeIn(new), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A steady count can hide a changing list of species."
