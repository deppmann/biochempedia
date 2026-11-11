"""Vesicle traffic, chapter 2: Reading Where Cargo Stops.
Same world and colour map as chapter 1 (../scenes.py is loaded for its world, packet and label helpers):
GREY membranes; ORANGE cargo; YELLOW vesicles; BLUE coat; TEAL Rab/tethers; PURPLE SNARE/SM;
GREEN GTP/success; RED temperature/block; GOLD ATP. All protein shapes are labelled schematic symbols.
Word cues match audio/words.json.
"""
import importlib.util
from pathlib import Path
from bp_style import *

_ch1_path = Path(__file__).resolve().parent.parent / "scenes.py"
_spec = importlib.util.spec_from_file_location("vt_ch1_scenes", _ch1_path)
_ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ch1)
TrafficScene, packet, label = _ch1.TrafficScene, _ch1.packet, _ch1.label
ORANGE, PURPLE, PINK = _ch1.ORANGE, _ch1.PURPLE, _ch1.PINK

LESSON_TITLE = "Vesicle Budding, Targeting and Fusion"
PILE = [(1.05, -.55), (1.25, .15), (1.7, .75), (1.9, -.4), (2.4, .25), (2.5, -.85), (1.6, -1.2), (2.2, 1.25)]


def unlit(lamp):
    return lamp.animate.set_color(GREY).set_fill(BG, opacity=1)


def lit(lamp, color=GREEN):
    return lamp.animate.set_color(color).set_fill(color, opacity=1).set_stroke(width=3)


class C2(TrafficScene):
    """Chapter 2 helpers on top of chapter 1's carried world."""

    def wobble(self, mobs, amp=.05, speed=1.0):
        for i, m in enumerate(mobs):
            m.clear_updaters()
            anchor = m.get_center().copy()
            m.ph = i * .83
            m.add_updater(lambda x, dt, a=anchor: (setattr(x, 'ph', x.ph + dt * speed),
                                                    x.move_to(a + [amp * np.sin(x.ph * 1.3), amp * np.cos(x.ph), 0])))

    def spin(self, packets):
        for p in packets:
            p[1].clear_updaters()
            p[1].add_updater(lambda m, dt, p=p: m.rotate(dt * .35, about_point=p[0].get_center()))

    def a_to_b(self, ok=True):
        pass

    def world(self, hot=False, pile=False, lamps=False):
        super().world(hot=hot, pile=pile, lamps=lamps)
        # keep the ER and surface labels off the cell outline
        for m in self.mobjects:
            if isinstance(m, Text) and m.text == 'ER' and abs(m.get_center()[1] + 1.65) < .05:
                m.shift(UP * .3)
            elif isinstance(m, Text) and m.text == 'surface' and abs(m.get_center()[1] + 2.1) < .05:
                m.move_to([3.95, -2.2, 0])

    # ---- the small cell used from s02 to s04 (rebuilt identically each time) ----
    def small_world(self, hot=True, pile=True, animate=False):
        self.world(hot=hot, pile=pile, lamps=animate)
        texts = [m for m in self.mobjects if isinstance(m, Text)]
        grp = VGroup(self.cell, self.surface, self.er, self.golgi, self.pile)
        for m in grp.get_family():
            m.clear_updaters()
        tgt = grp.copy().scale(.7, about_point=ORIGIN).shift([-2.57, -.23, 0])
        t_er, t_gol, t_sur = tgt[2], tgt[3], tgt[1]
        self.sl = [label('ER', t_er.get_center()[0], t_er.get_bottom()[1] - .32, TEXT, 28),
                   label('Golgi', t_gol.get_center()[0], t_gol.get_bottom()[1] - .55, TEXT, 28),
                   label('surface', t_sur.get_center()[0] + .1, t_sur.get_bottom()[1] - .45, TEXT, 28)]
        if animate:
            self.play(grp.animate.scale(.7, about_point=ORIGIN).shift([-2.57, -.23, 0]),
                      FadeOut(self.gauge), FadeOut(self.lamps), FadeOut(self.lamp_names), *[FadeOut(t) for t in texts],
                      *[FadeIn(t) for t in self.sl], run_time=1.8)
        else:
            self.remove(self.gauge, self.lamps, self.lamp_names, *texts)
            grp.scale(.7, about_point=ORIGIN).shift([-2.57, -.23, 0])
            self.add(*self.sl)
        self.wobble(self.er, .04)
        self.wobble(self.golgi, .04)
        self.wobble(self.pile, .05)
        self.spin(self.pile)

    def bins(self):
        self.in_bin = RoundedRectangle(width=3.4, height=.9, corner_radius=.12, stroke_color=ORANGE, stroke_width=3).move_to([-3.2, -3.1, 0])
        self.out_bin = RoundedRectangle(width=1.6, height=1.6, corner_radius=.12, stroke_color=ORANGE, stroke_width=3).move_to([1.5, -.3, 0])
        self.in_lab = label('inside', -5.95, -3.1, ORANGE, 28)
        self.out_lab = label('outside', 1.5, .85, ORANGE, 28)
        self.in_pos = [[-4.6 + .4 * i, -3.1, 0] for i in range(8)]
        self.out_pos = [[1.1 + .4 * (i % 3), -.7 + .4 * (i // 3), 0] for i in range(9)]
        return VGroup(self.in_bin, self.out_bin, self.in_lab, self.out_lab)

    def tally(self, n_in, n_out):
        a = [Dot(p, radius=.11, color=ORANGE) for p in self.in_pos[:n_in]]
        b = [Dot(p, radius=.11, color=ORANGE) for p in self.out_pos[:n_out]]
        return a, b

    # ---- the test tube used in s09 and s10 ----
    def tube(self):
        t = RoundedRectangle(width=5.6, height=5.4, corner_radius=.9, stroke_color=GREY, stroke_width=5,
                             fill_color=GREY, fill_opacity=.04).move_to([-1.4, -.15, 0])
        d = DashedVMobject(RoundedRectangle(width=6.3, height=6.2, corner_radius=1.1), num_dashes=60).set_color(GREY).move_to([-1.4, -.15, 0])
        lab = label('cell-free', -1.4, 3.45, TEXT, 28)
        return t, d, lab

    def dial(self):
        c = [4.9, .6, 0]
        ring = Circle(radius=.95, color=GREY, stroke_width=4).move_to(c)
        hand = Line(c, [4.9, 1.45, 0], color=TEXT, stroke_width=5)
        sch = label('schematic', 4.9, -.8, TEXT, 28)
        return ring, hand, sch, c

    def lamps_right(self):
        l1 = Circle(radius=.18, color=GREY, fill_color=BG, fill_opacity=1, stroke_width=3).move_to([3.5, 1.3, 0])
        l2 = Circle(radius=.18, color=GREY, fill_color=BG, fill_opacity=1, stroke_width=3).move_to([3.5, .2, 0])
        n1 = label('targeting', 4.0, 1.3, TEXT, 28).next_to(l1, RIGHT, buff=.2)
        n2 = label('fusion', 4.0, .2, TEXT, 28).next_to(l2, RIGHT, buff=.2)
        return l1, l2, n1, n2

    # ---- NSF units (s06 to s08) ----
    def nsf_unit(self, x, red=False):
        col = RED if red else TEXT
        chip_ = chip('NSF', col, size=28).move_to([x, 1.75, 0])
        chip_[0].set_fill(interpolate_color(ManimColor(BG), ManimColor(col), .16), opacity=1)  # solid, so the outline never crosses the letters
        rope = VGroup(*[Line([x - .5, 1.3 + dy, 0], [x + .5, 1.3 + dy, 0], color=PURPLE, stroke_width=6) for dy in (-.12, -.04, .04, .12)])
        return chip_, rope

    def er_dots(self, n=6):
        pts = [(-4.9, .5), (-4.5, .1), (-4.2, .6), (-4.7, -.4), (-4.1, -.2), (-4.6, -.8),
               (-4.95, -.1), (-4.0, .25), (-4.45, .75), (-4.3, -.6), (-4.8, .85), (-4.05, -.65), (-4.55, -.1), (-3.85, .5), (-4.9, -.6)]
        return VGroup(*[Dot([x, y, 0], radius=.11, color=ORANGE) for x, y in pts[:n]])


# ---------------------------------------------------------------------------------------------
class S00Link(C2):
    def construct(self):
        self.world(hot=False, pile=False, lamps=True)
        v = packet(-.4, 0)
        self.play(FadeIn(v, scale=.4), run_time=.5)
        self.play(v.animate.move_to([1.3, 0, 0]), run_time=2.4)
        self.at('bud')
        self.play(lit(self.lamps[0]), v.animate.move_to([1.9, 0, 0]), run_time=.35)
        v2 = packet(-3.55, 0)
        self.at('catch')
        tether = Line([2.1, 0, 0], [4.25, 0, 0], color=TEAL, stroke_width=7)
        self.play(lit(self.lamps[1]), v.animate.move_to([3.3, 0, 0]), Create(tether), FadeIn(v2), run_time=.4)
        self.at('fuse')
        self.play(v.animate.move_to([4.25, 0, 0]), FadeOut(tether), v2.animate.move_to([-1.65, 0, 0]), run_time=.5)
        self.play(FadeOut(v[0]), v[1].animate.shift(RIGHT * .8), lit(self.lamps[2]), v2.animate.move_to([-.4, 0, 0]), run_time=.6)
        self.play(FadeOut(v[1]), FadeOut(v2), run_time=.6)
        self.at('how did anyone put')
        self.play(*[unlit(l) for l in self.lamps], run_time=.7)
        self.temperature(True)
        self.at('those handoffs')
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * .5) for p in self.pile], lag_ratio=.18),
                  self.level.animate.set_value(6), run_time=1.8)
        self.at('what can a pile')
        card = chip('What does a pile tell you?', TEXT, size=30).move_to([.3, 3.2, 0])
        self.play(FadeIn(card, shift=DOWN * .2), Indicate(self.pile, color=YELLOW), run_time=1.0)
        self.finish()


class S01Title(TitleCard, C2):
    TITLE = 'Reading Where Cargo Stops'
    LESSON = LESSON_TITLE

    def construct(self):
        self.world(hot=True, pile=True, lamps=True)
        overlay = Rectangle(width=14.1, height=7.9, fill_color=BG, fill_opacity=.68, stroke_width=0)
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).move_to([0, 1.3, 0])
        title = fit(T(self.TITLE, size=54, font=TITLE_FONT), max_w=12.5).move_to([0, .2, 0])
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4).move_to([0, -.45, 0])
        les = label(self.LESSON, 0, -1.1, TEXT, 28)
        self.add(overlay, brand, title, rule, les)
        self.wait(2)


class S02Measure(C2):
    def construct(self):
        self.small_world(hot=True, pile=True, animate=True)
        pl = [p.get_center() for p in self.pile]
        bins = self.bins()
        inside = [Dot(pl[i] + [.0, .0, 0], radius=.11, color=ORANGE) for i in range(8)]
        outside = [Dot([.55, .95, 0], radius=.11, color=ORANGE), Dot([.5, -1.2, 0], radius=.11, color=ORANGE)]
        self.play(FadeIn(bins), run_time=.9)
        self.at('yeasts secrete')
        self.play(*[FadeIn(d, scale=2) for d in inside + outside], run_time=.8)
        self.wobble(inside + outside, .04, 1.4)
        self.at('invertase')
        anims = []
        for d, p in zip(inside + outside, self.in_pos[:8] + self.out_pos[:2]):
            d.clear_updaters()
            anims.append(d.animate.move_to(p))
        self.play(LaggedStart(*anims, lag_ratio=.1), run_time=1.6)
        self.wobble(inside + outside, .02, 1.2)
        self.at('the fraction secreted')
        num = label('outside', 4.7, 2.85, ORANGE, 30)
        bar = Line([3.0, 2.45, 0], [6.4, 2.45, 0], color=TEXT, stroke_width=3)
        den = label('outside + inside', 4.7, 2.05, ORANGE, 30)
        fl = label('fraction secreted', 4.7, 1.3, TEXT, 30)
        base = Line([2.7, -2.0, 0], [6.6, -2.0, 0], color=GREY, stroke_width=4)
        b1 = Rectangle(width=.95, height=2.1, stroke_width=0, fill_color=GREEN, fill_opacity=.85).move_to([3.6, -2.0 + 1.05, 0])
        b2 = Rectangle(width=.95, height=.5, stroke_width=0, fill_color=RED, fill_opacity=.85).move_to([5.7, -2.0 + .25, 0])
        t1 = label('wild type', 3.6, -2.45, TEXT, 28)
        t2 = label('sec mutant', 5.7, -2.45, TEXT, 28)
        t3 = label('37 °C', 5.7, -2.9, RED, 28)
        sch = label('schematic', 4.9, 0.55, TEXT, 28)
        self.play(FadeIn(fl, shift=UP * .15), FadeIn(base), FadeIn(t1), FadeIn(t2), FadeIn(t3), FadeIn(sch),
                  GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), run_time=1.6)
        self.at('enzyme outside')
        self.play(FadeIn(num, shift=DOWN * .15), Indicate(self.out_bin, color=ORANGE), run_time=.7)
        self.at('divided by all of it')
        self.play(Create(bar), FadeIn(den, shift=UP * .15), run_time=.8)
        self.finish()


class S03Deliverable(C2):
    def construct(self):
        self.small_world(hot=True, pile=True)
        self.bins()
        a, b = self.tally(8, 2)
        self.add(self.in_bin, self.out_bin, self.in_lab, self.out_lab, *a, *b)
        self.wobble(a + b, .02, 1.2)
        self.play(Indicate(self.pile, color=YELLOW), run_time=1.4)
        self.at('only waiting')
        self.play(Indicate(VGroup(*a), color=ORANGE), run_time=1.2)
        self.at('return the cells')
        self.temperature(False)
        self.at('with new protein synthesis blocked')
        blk = label('protein synthesis blocked', -.9, 2.3, RED, 28)
        self.play(FadeIn(blk, shift=DOWN * .15), run_time=.6)
        self.at('if the trapped enzyme')
        anims = []
        for p in self.pile:
            p.clear_updaters()
            anims.append(Succession(p.animate(run_time=.5).move_to([-.02, p.get_y(), 0]),
                                    AnimationGroup(FadeOut(p[0]), p[1].animate.shift(RIGHT * .5), run_time=.3),
                                    FadeOut(p[1], run_time=.2)))
        moves = []
        for i, d in enumerate(a[2:]):
            d.clear_updaters()
            moves.append(Succession(d.animate(run_time=.6).move_to([-1.0 + .0, -3.1, 0]),
                                    d.animate(run_time=1.0).move_to(self.out_pos[2 + i])))
        self.play(LaggedStart(*anims, lag_ratio=.15), LaggedStart(*moves, lag_ratio=.2), run_time=2.6)
        self.at('it was waiting')
        path = VGroup(Line([-1.45, -3.1, 0], [1.5, -3.1, 0], color=GREY, stroke_width=5),
                      Line([1.5, -3.1, 0], [1.5, -1.15, 0], color=GREY, stroke_width=5))
        same = label('same amount', .1, -2.62, TEXT, 28)
        self.play(Create(path), FadeIn(same), run_time=1.0)
        self.at('delivered')
        res = chip('deliverable, not dead', GREEN, size=30).move_to([.3, 3.2, 0])
        self.play(FadeIn(res, shift=DOWN * .2), run_time=.7)
        self.finish()


class Cell4(C2):
    def small_cells(self):
        return None

    def cartoon(self, kind, x, y, w=2.6, h=3.0):
        out = Ellipse(width=w, height=h, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.05).move_to([x, y, 0])
        inner = VGroup()
        if kind == 'er':
            for dy in (-.9, -.3, .3, .9):
                inner.add(VMobject().set_points_smoothly([[x - .85, y + dy, 0], [x - .4, y + dy + .18, 0], [x + .1, y + dy - .15, 0], [x + .5, y + dy + .15, 0], [x + .85, y + dy, 0]]).set_stroke(GREY, 7))
        elif kind == 'golgi':
            for cx in (-.55, .55):
                for k in range(3):
                    inner.add(ArcBetweenPoints([x + cx - .4, y - .85 + .6 * k, 0], [x + cx + .4, y - .85 + .6 * k + .12, 0], angle=.55, color=GREY, stroke_width=8))
        else:
            rng = np.random.RandomState(3)
            pts = [(-.7, .8), (0, 1.0), (.7, .8), (-.9, 0), (-.3, .25), (.35, .15), (.9, 0), (-.6, -.7), (.1, -.65), (.75, -.8), (0, -.2)]
            for px, py in pts:
                c = Circle(radius=.16, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=.12).move_to([x + px, y + py * .9, 0])
                inner.add(VGroup(c, Dot(c.get_center(), radius=.05, color=ORANGE)))
        return VGroup(out, inner)


class S04Screen(Cell4):
    def construct(self):
        self.thermo = chip('37 °C', RED, size=28).move_to([-5.25, 2.55, 0])
        self.add(self.thermo)
        tube = RoundedRectangle(width=2.0, height=6.5, corner_radius=.25, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.05).move_to([-3.2, -.35, 0])
        tl = label('density', -5.4, .6, TEXT, 28)
        tl2 = label('gradient', -5.4, .15, TEXT, 28)
        self.add(tube, tl, tl2)
        rng = np.random.RandomState(7)
        normal, dense = [], []
        for i in range(14):
            c = Ellipse(width=.5, height=.32, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.15).move_to([-3.2 + rng.uniform(-.7, .7), 2.7 + rng.uniform(0, .3), 0])
            c.target_y = rng.uniform(.5, 1.7)
            normal.append(c)
        for i in range(8):
            c = Ellipse(width=.5, height=.32, color=GREY, stroke_width=3, fill_color=ORANGE, fill_opacity=.45).move_to([-3.2 + rng.uniform(-.7, .7), 2.7 + rng.uniform(0, .3), 0])
            c.target_y = rng.uniform(-2.95, -2.1)
            dense.append(c)
        allc = normal + dense
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * .2) for c in allc], lag_ratio=.05), run_time=1.8)
        self.at('secretion blocked')
        self.play(*[c.animate.move_to([c.get_x(), c.target_y, 0]) for c in allc], run_time=3.4, rate_func=smooth)
        self.wobble(allc, .04, 1.1)
        self.at('in 1980')
        yr = chip('1980', TEXT, size=30).move_to([1.6, 3.3, 0])
        self.play(FadeIn(yr, shift=DOWN * .2), run_time=.7)
        self.at('enrich new mutants')
        band = Rectangle(width=2.0, height=1.2, stroke_color=ORANGE, stroke_width=4, fill_opacity=0).move_to([-3.2, -2.55, 0])
        dl = label('dense', -5.4, -2.3, ORANGE, 28)
        dl2 = label('mutants', -5.4, -2.75, ORANGE, 28)
        self.play(Create(band), FadeIn(dl), FadeIn(dl2), run_time=1.0)
        self.at('electron microscopy')
        cart = [self.cartoon('er', -.4, .8), self.cartoon('golgi', 2.4, .8), self.cartoon('ves', 5.4, .8)]
        picks = dense[:3]
        self.play(*[ReplacementTransform(c.copy(), cart[i][0]) for i, c in enumerate(picks)], FadeOut(yr), run_time=1.6)
        self.at('showed what each one')
        self.play(*[FadeIn(cart[i][1]) for i in range(3)], run_time=1.0)
        names = [label('ER', -.4, -1.1, TEXT, 28), label('Golgi-like stacks', 2.4, -1.1, TEXT, 28), label('vesicles', 5.4, -1.1, YELLOW, 28)]
        self.play(*[FadeIn(n, shift=UP * .1) for n in names], run_time=.8)
        for cc in cart:
            self.wobble([cc[1]], .04, 1.0)
        self.finish()


class S05Order(Cell4):
    def construct(self):
        self.thermo = chip('37 °C', RED, size=28).move_to([-5.25, 2.55, 0])
        self.add(self.thermo)
        tube = RoundedRectangle(width=2.0, height=6.5, corner_radius=.25, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.05).move_to([-3.2, -.35, 0])
        cart = [self.cartoon('er', -.4, .8), self.cartoon('golgi', 2.4, .8), self.cartoon('ves', 5.4, .8)]
        names = [label('ER', -.4, -1.1, TEXT, 28), label('Golgi-like stacks', 2.4, -1.1, TEXT, 28), label('vesicles', 5.4, -1.1, YELLOW, 28)]
        self.add(*cart, *names)
        # the tube and screen leave; the three pictures keep their places for a moment, then slide onto the route
        route = Arrow([-6.3, -1.9, 0], [6.4, -1.9, 0], color=GREY, stroke_width=5, buff=0, stroke_opacity=.9)
        route = DashedLine([-6.3, -1.9, 0], [6.0, -1.9, 0], color=GREY, stroke_width=5)
        tip = Triangle(color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=1).scale(.16).rotate(-PI / 2).move_to([6.3, -1.9, 0])
        self.play(FadeOut(self.thermo), Create(route), FadeIn(tip), run_time=1.0)
        self.at('on a linear route')
        tx = [-4.3, 0.0, 4.3]
        self.play(*[VGroup(cart[i], names[i]).animate.shift([tx[i] - [-.4, 2.4, 5.4][i], 0, 0]) for i in range(3)], run_time=1.6)
        # new names for the route
        newn = [label('ER', -4.3, -1.1, TEXT, 28), label('Golgi', 0, -1.1, TEXT, 28), label('vesicles', 4.3, -1.1, YELLOW, 28)]
        self.play(Transform(names[1], newn[1]), run_time=.5)
        for cc in cart:
            self.wobble([cc[1]], .04, 1.0)
        self.at('cargo piles up')
        rule = label('pile = last place reached', -1.6, -2.75, TEXT, 30)
        self.play(FadeIn(rule, shift=UP * .15), run_time=.8)
        self.play(*[Indicate(c[1], color=ORANGE) for c in cart], run_time=1.2)
        self.at('in 1981')
        card = chip('1981: double mutants', TEXT, size=28).move_to([4.2, -2.75, 0])
        self.play(FadeIn(card, shift=DOWN * .15), run_time=.8)
        self.at('put the blocks')
        self.play(LaggedStart(*[Indicate(c[0], color=TEXT, scale_factor=1.06) for c in cart], lag_ratio=.4), run_time=2.0)
        self.finish()


class NsfScene(C2):
    def nsf_state(self, with_card=True, dots=6):
        self.world(hot=True, pile=False, lamps=False)
        self.remove(self.lamps)
        self.units = []
        for x in (-4.1, -1.4, 3.1):
            c, r = self.nsf_unit(x, red=True)
            self.units.append((c, r))
            self.add(c, r)
        self.dots = self.er_dots(dots)
        self.add(self.dots)
        self.wobble(self.dots, .06, 1.6)
        self.card = chip('NSF fails at 37 °C. Where does cargo pile up?', TEXT, size=30)
        fit(self.card, max_w=8.4)
        self.card.move_to([.3, 3.2, 0])
        if with_card:
            self.add(self.card)
        for c, r in self.units:
            c.ph = 0
            c.add_updater(lambda m, dt: (setattr(m, 'ph', m.ph + dt), m.set_stroke(opacity=.55 + .45 * np.sin(m.ph * 2.2))))


class S06Predict(C2):
    def construct(self):
        self.world(hot=False, pile=False, lamps=False)
        self.remove(self.lamps)
        v0 = packet(-3.55, 0)
        self.play(FadeIn(v0, scale=.4), v0.animate.move_to([-1.65, 0, 0]), run_time=1.2)
        self.play(FadeOut(v0), run_time=.2)
        self.at('an enzyme called')
        c, r = self.nsf_unit(-1.4)
        self.play(FadeIn(r, shift=UP * .2), FadeIn(c, shift=DOWN * .2), run_time=.9)
        self.at('resets snares')
        splay = VGroup(*[Line([-1.9, 1.3 + dy, 0], [-.9, 1.3 + dy * 4, 0], color=PURPLE, stroke_width=6) for dy in (-.12, -.04, .04, .12)])
        self.play(Transform(r, splay), c.animate.shift(DOWN * .2), run_time=.9)
        self.play(Transform(r, self.nsf_unit(-1.4)[1]), c.animate.shift(UP * .2), run_time=.9)
        self.at('at many steps')
        c2, r2 = self.nsf_unit(-4.1)
        c3, r3 = self.nsf_unit(3.1)
        self.play(FadeIn(c2, shift=DOWN * .2), FadeIn(r2, shift=UP * .2), run_time=.7)
        self.play(FadeIn(c3, shift=DOWN * .2), FadeIn(r3, shift=UP * .2), run_time=.7)
        self.at('where would')
        self.temperature(True)
        red_fill = interpolate_color(ManimColor(BG), ManimColor(RED), .16)
        self.play(*[a for m in (c, c2, c3) for a in (m[0].animate.set_stroke(RED).set_fill(red_fill, opacity=1), m[1].animate.set_color(RED))], run_time=.8)
        self.at('mutant')
        card = chip('NSF fails at 37 °C. Where does cargo pile up?', TEXT, size=30)
        fit(card, max_w=8.4)
        card.move_to([.3, 3.2, 0])
        self.play(FadeIn(card, shift=DOWN * .2), run_time=.7)
        for u in (c, c2, c3):
            u.ph = 0
            u.add_updater(lambda m, dt: (setattr(m, 'ph', m.ph + dt), m.set_stroke(opacity=.55 + .45 * np.sin(m.ph * 2.2))))
        self.finish()


class S07Think(NsfScene):
    def construct(self):
        self.nsf_state()
        self.wait(self.beat(1.0))
        self.finish()


class S08Reveal(NsfScene):
    def construct(self):
        self.nsf_state()
        self.at('earliest block')
        self.play(Indicate(self.units[0][0], color=RED, scale_factor=1.15), run_time=1.2)
        self.at('classical sec18')
        lab = label('sec18 = yeast NSF', -.9, -3.3, TEXT, 30)
        self.play(FadeIn(lab, shift=UP * .15), run_time=.7)
        self.at('er and small')
        more = self.er_dots(15)[6:]
        for d in more:
            d.set_opacity(0)
        ves = VGroup(*[Circle(radius=.14, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=.12).move_to([x, y, 0])
                       for x, y in [(-3.4, .9), (-3.2, .3), (-3.45, -.35), (-3.1, -.9), (-3.0, .8)]])
        for v in ves:
            v.add(Dot(v.get_center(), radius=.045, color=ORANGE))
        self.add(*more)
        self.play(*[d.animate.set_opacity(1) for d in more], LaggedStart(*[FadeIn(v, scale=.3) for v in ves], lag_ratio=.15), run_time=2.0)
        self.wobble(list(more), .06, 1.6)
        self.wobble(list(ves), .05, 1.3)
        self.at('piled up')
        self.play(Indicate(VGroup(self.dots, *more, ves), color=ORANGE, scale_factor=1.08), run_time=1.0)
        self.at('not late')
        ghost = VGroup(*[Circle(radius=.24, color=GREY, stroke_width=3, stroke_opacity=.7) for _ in PILE])
        for g, (x, y) in zip(ghost, PILE):
            g.move_to([x, y, 0])
        self.play(FadeIn(ghost), run_time=.8)
        cr = Cross(ghost, stroke_color=RED, stroke_width=7)
        no = label('not here', 1.2, -1.9, RED, 28)
        self.play(Create(cr), FadeIn(no), run_time=.9)
        self.at('a pile shows')
        new = chip('earliest block wins', GREEN, size=30).move_to(self.card)
        self.play(ReplacementTransform(self.card, new), run_time=.9)
        self.at('not when')
        self.play(Indicate(new, color=GREEN), run_time=1.0)
        self.finish()


class S09Tubes(C2):
    def construct(self):
        tube, dashed, cf = self.tube()
        self.add(self.make_bg())
        self.play(Create(tube), run_time=2.4)
        self.at('cell free')
        self.play(Create(dashed), FadeIn(cf), run_time=1.2)
        self.at('donor')
        donor = VMobject().set_points_smoothly([[-3.2 + .12 * np.sin(k * 1.4), y, 0] for k, y in enumerate(np.linspace(-1.5, 1.5, 9))]).set_stroke(GREY, 8)
        dl = label('donor', -3.2, -2.05, TEXT, 28)
        self.play(FadeIn(donor, shift=DOWN * .6), FadeIn(dl), run_time=.9)
        self.at('and acceptor')
        acc = VMobject().set_points_smoothly([[.2 + .12 * np.sin(k * 1.4), y, 0] for k, y in enumerate(np.linspace(-1.5, 1.5, 9))]).set_stroke(GREY, 8)
        al = label('acceptor', .2, -2.05, TEXT, 28)
        self.play(FadeIn(acc, shift=DOWN * .6), FadeIn(al), run_time=.9)
        self.at('cytosol')
        cyt = Ellipse(width=3.2, height=1.1, stroke_width=0, fill_color=BLUE, fill_opacity=.18).move_to([-1.3, 1.9, 0])
        cl = label('cytosol', -1.3, 1.9, BLUE, 28)
        self.play(FadeIn(cyt, shift=DOWN * .6), FadeIn(cl), run_time=.8)
        self.at('atp')
        atp = chip('ATP', GOLD, size=28).move_to([-1.3, -1.9, 0])
        self.play(FadeIn(atp, shift=DOWN * .6), run_time=.7)
        self.at('then each step')
        self.vesicles = self.shuttle()
        ring, hand, sch, c = self.dial()
        self.play(Create(ring), Create(hand), FadeIn(sch), run_time=.9)
        hand.add_updater(lambda m, dt: m.rotate(-dt * .8, about_point=np.array(c)))
        self.at('removed or rebuilt')
        self.play(Indicate(atp, color=GOLD), run_time=.9)
        self.finish()

    def make_bg(self):
        return VGroup()

    def shuttle(self):
        vs = []
        for i in range(3):
            v = packet(-2.8, 0, r=.22)
            v.t = i * 1.3
            v.row = [.9, 0, -.9][i]

            def upd(m, dt):
                m.t += dt
                f = (m.t % 4.0) / 4.0
                m.move_to([-2.8 + 2.9 * f, m.row + .12 * np.sin(m.t * 2.0), 0])
                m.set_opacity(min(1, f * 8, (1 - f) * 8))
            v.add_updater(upd)
            self.add(v)
            vs.append(v)
        return vs


class S10Hops(C2):
    Y = -.3

    def construct(self):
        Y = self.Y
        tube, dashed, cf = self.tube()
        mem = lambda x: VMobject().set_points_smoothly([[x + .12 * np.sin(k * 1.4), y, 0] for k, y in enumerate(np.linspace(-1.5, 1.5, 9))]).set_stroke(GREY, 8)
        old = VGroup(mem(-3.2), mem(.2), label('donor', -3.2, -2.05, TEXT, 28), label('acceptor', .2, -2.05, TEXT, 28),
                     Ellipse(width=3.2, height=1.1, stroke_width=0, fill_color=BLUE, fill_opacity=.18).move_to([-1.3, 1.9, 0]),
                     label('cytosol', -1.3, 1.9, BLUE, 28), chip('ATP', GOLD, size=28).move_to([-1.3, -1.9, 0]))
        ring, hand, sch, c = self.dial()
        self.add(tube, dashed, cf, old, ring, hand, sch)
        hand.add_updater(lambda m, dt: m.rotate(-dt * .8, about_point=np.array(c)))
        self.l1, self.l2, n1, n2 = self.lamps_right()
        self.lamps = VGroup(self.l1, self.l2)
        sph = lambda x: Circle(radius=.6, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.12).move_to([x, Y, 0])
        left, right = sph(-2.9), sph(.1)
        self.at('catching enough')
        self.play(FadeOut(old), FadeOut(ring), FadeOut(hand), FadeOut(sch), run_time=.5)
        self.play(FadeIn(self.lamps), FadeIn(n1), FadeIn(n2), run_time=.5)
        self.at('yeast hop')
        self.play(FadeIn(left, scale=.5), FadeIn(right, scale=.5), run_time=.8)
        self.wobble([left, right], .04, 1.1)
        flags = self.flags(-2.9, .1)
        self.at('a tether')
        hops = self.hops_tether('HOPS')
        self.play(FadeIn(hops, shift=UP * .15), run_time=.7)
        self.at('binds the rab')
        self.play(FadeIn(flags), run_time=.7)
        snares = self.snares()
        self.play(lit(self.l1), Create(snares), run_time=.8)
        merged = Ellipse(width=2.2, height=1.3, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.12).move_to([-1.4, Y, 0])
        left.clear_updaters(); right.clear_updaters()
        self.play(ReplacementTransform(VGroup(left, right), merged), FadeOut(snares), FadeOut(hops), lit(self.l2), run_time=1.0)
        self.at('separate forms')
        left, right = sph(-2.9), sph(.1)
        self.play(FadeOut(merged), FadeIn(left), FadeIn(right), unlit(self.l1), unlit(self.l2), run_time=.8)
        self.wobble([left, right], .04, 1.1)
        t1 = VGroup(label('Vps11 beta propeller', 4.65, 2.75, TEXT, 28), label('missing', 4.65, 2.3, TEXT, 28))
        self.at('propeller of')
        self.play(FadeIn(t1, shift=DOWN * .15), run_time=.5)
        self.at('vps 11')
        h1 = self.hops_tether('HOPS')
        self.play(FadeIn(h1, shift=UP * .15), lit(self.l1), run_time=.6)
        sn = self.snares(stub=True)
        self.play(Create(sn), lit(self.l2, RED), run_time=.6)
        self.at('or vps 18')
        t2 = VGroup(label('Vps18 beta propeller', 4.65, 2.75, TEXT, 28), label('missing', 4.65, 2.3, TEXT, 28))
        self.play(FadeOut(h1), FadeOut(sn), unlit(self.l1), unlit(self.l2), Transform(t1, t2), run_time=.6)
        h2 = self.hops_tether('HOPS')
        self.play(FadeIn(h2, shift=UP * .15), lit(self.l1), run_time=.6)
        sn2 = self.snares(stub=True)
        self.play(Create(sn2), lit(self.l2, RED), run_time=.6)
        self.at('still tethered')
        self.play(Indicate(h2, color=TEAL), run_time=.8)
        self.at('lipid spheres')
        self.play(Indicate(VGroup(left, right), color=TEXT, scale_factor=1.08), run_time=.8)
        self.wait(.4)
        self.at('but they failed')
        cn = label('caught is not fused', 4.65, -1.3, RED, 30)
        self.play(FadeIn(cn, shift=UP * .15), Indicate(self.l2, color=RED, scale_factor=1.6), run_time=1.0)
        self.finish()

    def flags(self, xa, xb):
        Y = self.Y
        g = VGroup()
        for x in (xa, xb):
            pole = Line([x, Y + .6, 0], [x, Y + 1.2, 0], color=TEAL, stroke_width=6)
            gtp = chip('GTP', GREEN, size=28).move_to([x, Y + 1.55, 0])
            rab = chip('Ypt7', TEAL, size=28).move_to([x, Y + 2.15, 0])
            g.add(pole, gtp, rab)
        return g

    def hops_tether(self, name):
        Y = self.Y
        blocks = VGroup(*[RoundedRectangle(width=.4, height=.25, corner_radius=.06, color=TEAL, fill_color=TEAL, fill_opacity=.55).move_to([x, Y, 0])
                          for x in (-2.0, -1.6, -1.2, -.8)])
        lab = label(name, -1.4, Y - 1.2, TEAL, 28)
        return VGroup(blocks, lab)

    def snares(self, stub=False):
        Y = self.Y
        g = VGroup()
        for y in (Y + .3, Y - .3):
            g.add(Line([-2.3, y, 0], [-1.5 if not stub else -1.75, y, 0], color=PURPLE, stroke_width=6))
            g.add(Line([-.5, y, 0], [-1.3 if not stub else -1.05, y, 0], color=PURPLE, stroke_width=6))
        return g


class S11Return(C2):
    def construct(self):
        self.world(hot=False, pile=False, lamps=True)
        self.remove(self.gauge)
        tube, dashed, cf = self.tube()
        panel = Rectangle(width=14.1, height=7.9, fill_color=BG, fill_opacity=1, stroke_width=0)
        merged = Ellipse(width=2.2, height=1.3, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=.12).move_to([-1.4, 0, 0])
        big = VGroup(panel, tube, dashed, merged)
        self.add(big)
        self.play(big.animate.scale(.2, about_point=ORIGIN).shift([5.7, .2, 0]), run_time=1.0)
        self.play(FadeOut(panel), run_time=.2)
        self.remove(panel)
        self.at('stuck cargo')
        v = packet(-1.65, 0)
        self.play(FadeIn(v, scale=.4), v.animate.move_to([1.5, 0, 0]), run_time=1.6)
        self.at('where cargo stops')
        self.temperature(True)
        route = DashedLine([-4.0, -1.1, 0], [3.3, -1.1, 0], color=TEXT, stroke_width=3)
        self.play(FadeOut(v), Create(route), LaggedStart(*[FadeIn(p, shift=LEFT * .4) for p in self.pile], lag_ratio=.08), run_time=.9)
        self.at('gives the order')
        self.play(*[FadeOut(p, shift=RIGHT * .4) for p in self.pile], FadeOut(route), run_time=.6)
        self.temperature(False)
        self.lamp_names[0].set_opacity(0)
        self.at('test tubes')
        br = self.bracket()
        self.play(Create(br), run_time=.5)
        self.at('split catch')
        a = VGroup(Line([-.6, -3.45, 0], [1.9, -3.45, 0], color=RED), Line([-.6, -3.45, 0], [-.6, -3.25, 0], color=RED),
                   Line([1.9, -3.45, 0], [1.9, -3.25, 0], color=RED), label('?', .65, -3.64, RED, 28))
        b = VGroup(Line([2.8, -3.45, 0], [4.8, -3.45, 0], color=RED), Line([2.8, -3.45, 0], [2.8, -3.25, 0], color=RED),
                   Line([4.8, -3.45, 0], [4.8, -3.25, 0], color=RED), label('?', 3.8, -3.64, RED, 28))
        self.play(ReplacementTransform(br, VGroup(a, b)), run_time=1.2)
        self.lamp_names[0].set_opacity(1)
        self.finish()


class S12End(EndCard):
    LINE = 'Where cargo stops gives the order; test tubes split catch from fuse.'
