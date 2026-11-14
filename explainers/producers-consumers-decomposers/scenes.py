"""The Leaf Pile That Stops Growing.

COLOR MAP
  GREEN  producers / oak
  ORANGE consumers / deer, mouse, fox
  PURPLE decomposers / fungus threads, bacteria
  GOLD   matter carried in leaves, bodies, soil, and air
  YELLOW energy / sunlight / heat
  BLUE_GREY tub and structural outlines

All recurring forest geometry is rebuilt by ``forest_world`` at the same coordinates.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BROWN = "#9A6B45"
BLUE_GREY = "#91A4B7"


def arrow(a, b, color=GOLD, width=6, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def gold_dots(points, radius=0.07):
    return VGroup(*[Dot(p, radius=radius, color=GOLD) for p in points])


def leaf(at=ORIGIN, scale=1.0, holes=False):
    body = Ellipse(width=1.0 * scale, height=0.46 * scale, color=BROWN,
                   stroke_width=3, fill_color=BROWN, fill_opacity=0.72).move_to(at).rotate(-0.18)
    vein = Line(body.get_left() + RIGHT * 0.08, body.get_right() + LEFT * 0.08,
                color=GOLD, stroke_width=2)
    matter = gold_dots([body.get_center() + np.array([x, y, 0]) * scale
                        for x, y in [(-.25, .03), (0, -.08), (.25, .05)]], .045 * scale)
    g = VGroup(body, vein, matter)
    if holes:
        g.add(*[Circle(radius=.07 * scale, color=BG, fill_color=BG, fill_opacity=1,
                       stroke_width=0).move_to(body.get_center() + np.array(p) * scale)
                for p in [(-.12, .08, 0), (.18, -.05, 0)]])
    return g


def oak():
    trunk = Polygon([-4.75, -2.15, 0], [-4.28, -2.15, 0], [-4.42, .55, 0],
                    [-4.62, .55, 0], color=BROWN, stroke_width=4,
                    fill_color=BROWN, fill_opacity=.72)
    branches = VGroup(Line([-4.52, -.1, 0], [-5.25, 1.0, 0], color=BROWN, stroke_width=8),
                      Line([-4.5, .05, 0], [-3.72, 1.18, 0], color=BROWN, stroke_width=8))
    crown = VGroup(*[Circle(radius=r, color=GREEN, stroke_width=4, fill_color=GREEN,
                           fill_opacity=.32).move_to(p)
                     for p, r in [((-4.55, 1.65, 0), 1.2), ((-5.25, 1.25, 0), .83),
                                  ((-3.82, 1.35, 0), .9), ((-4.5, 2.45, 0), .75)]])
    roots = VGroup(Line([-4.52, -2.05, 0], [-5.35, -2.72, 0], color=BROWN, stroke_width=5),
                   Line([-4.5, -2.05, 0], [-4.4, -2.88, 0], color=BROWN, stroke_width=5),
                   Line([-4.48, -2.05, 0], [-3.55, -2.72, 0], color=BROWN, stroke_width=5))
    g = VGroup(roots, branches, trunk, crown)
    g.crown, g.roots = crown, roots
    return g


def tub():
    outline = VMobject(color=BLUE_GREY, stroke_width=6)
    outline.set_points_as_corners([[-2.8, -.65, 0], [-2.45, -2.45, 0],
                                   [5.6, -2.45, 0], [5.95, -.65, 0]])
    rim = VGroup(Line([-3.05, -.65, 0], [-2.55, -.65, 0], color=BLUE_GREY, stroke_width=6),
                 Line([5.7, -.65, 0], [6.2, -.65, 0], color=BLUE_GREY, stroke_width=6))
    drain = VGroup(Circle(radius=.26, color=BLUE_GREY, stroke_width=5,
                          fill_color=BG, fill_opacity=1).move_to([1.55, -2.45, 0]),
                   Line([1.35, -2.45, 0], [1.75, -2.45, 0], color=BLUE_GREY, stroke_width=4))
    g = VGroup(outline, rim, drain)
    g.outline, g.drain = outline, drain
    return g


def leaf_pile(n=2):
    layers = VGroup()
    for k in range(n):
        y = -2.18 + .29 * k
        layers.add(RoundedRectangle(corner_radius=.12, width=6.9, height=.27,
                                    color=BROWN, stroke_width=2, fill_color=BROWN,
                                    fill_opacity=.62).move_to([1.55, y, 0]))
    return layers


def forest_world(layers=2, with_tub=True):
    soil = Rectangle(width=12.6, height=.72, color=BLUE_GREY, stroke_width=0,
                     fill_color=BLUE_GREY, fill_opacity=.16).move_to([0, -2.83, 0])
    surface = Line([-6.3, -2.46, 0], [6.3, -2.46, 0], color=BLUE_GREY, stroke_width=3)
    tr, pile = oak(), leaf_pile(layers)
    g = VGroup(soil, surface, tr, pile)
    tb = tub()
    if with_tub:
        g.add(tb)
    g.tree, g.pile, g.tub, g.soil = tr, pile, tb, soil
    return g


def falling_leaves(n=7, y0=3.1):
    xs = [-5.1, -4.3, -3.6, -2.1, -.3, 1.4, 3.0][:n]
    return VGroup(*[leaf([x, y0 + .23 * (i % 3), 0], .52) for i, x in enumerate(xs)])


def animal(kind, at, scale=.8):
    # Flat, labelled silhouettes: enough anatomy to read as animals, never photorealistic.
    body = Ellipse(width=1.6 * scale, height=.75 * scale, color=ORANGE, stroke_width=4,
                   fill_color=ORANGE, fill_opacity=.28).move_to(at)
    head = Circle(radius=.34 * scale, color=ORANGE, stroke_width=4,
                  fill_color=ORANGE, fill_opacity=.28).next_to(body, RIGHT, buff=-.08 * scale)
    legs = VGroup(*[Line(body.get_center() + np.array([x, -.28, 0]) * scale,
                         body.get_center() + np.array([x, -.78, 0]) * scale,
                         color=ORANGE, stroke_width=4) for x in (-.48, .35)])
    tail = Line(body.get_left(), body.get_left() + np.array([-.35, .28 if kind == "fox" else .1, 0]) * scale,
                color=ORANGE, stroke_width=4)
    label = T(kind, 28, ORANGE).next_to(body, DOWN, buff=.35 * scale)
    return VGroup(body, head, legs, tail, label)


def fungus_field():
    threads = VGroup()
    for x in np.linspace(-4.9, 2.9, 8):
        threads.add(CubicBezier([x, -2.15, 0], [x-.35, -.9, 0], [x+.5, .6, 0],
                                [x+.15, 2.35, 0], color=PURPLE, stroke_width=5))
    bacteria = VGroup(*[Dot([x, y, 0], radius=.105, color=PURPLE)
                        for x, y in [(-3.8, 1.6), (-2.5, .65), (-.8, 1.85),
                                     (.5, .55), (2.2, 1.45), (3.5, -.2)]])
    return VGroup(threads, bacteria)


def balance_picture():
    stand = VGroup(Line([0, -1.65, 0], [0, 1.15, 0], color=BLUE_GREY, stroke_width=6),
                   Line([-2.75, 1.15, 0], [2.75, 1.15, 0], color=BLUE_GREY, stroke_width=6),
                   Triangle(color=BLUE_GREY, fill_color=BLUE_GREY, fill_opacity=.35).scale(.28).move_to([0, 1.15, 0]))
    pan = RoundedRectangle(corner_radius=.18, width=3.2, height=.3, color=BLUE_GREY,
                           fill_color=BLUE_GREY, fill_opacity=.18).move_to([-1.15, -.15, 0])
    strings = VGroup(Line([-2.55, 1.15, 0], [-2.55, -.15, 0], color=BLUE_GREY),
                     Line([.25, 1.15, 0], [.25, -.15, 0], color=BLUE_GREY))
    lf = leaf([-1.15, .15, 0], 1.55)
    return VGroup(stand, strings, pan, lf)


def predict_backdrop():
    pic = balance_picture().scale(.9).shift(LEFT * 2.25 + UP * .55)
    read = chip("55–60% left", GOLD, size=32).move_to([3.25, 1.25, 0])
    year = T("about 1 year · Weimer Run leaf bags", 28, BLUE_GREY).move_to([2.65, .35, 0])
    note = T("a balance shows how much, not where", 28, BLUE_GREY).move_to([2.45, -.45, 0])
    down = arrow([2.3, -.8, 0], [2.3, -1.9, 0], GOLD)
    up = arrow([4.1, -.8, 0], [4.1, -1.9, 0], GOLD)
    dl = T("soil?", 30, GOLD).next_to(down, DOWN, buff=.12)
    ul = T("air?", 30, GOLD).next_to(up, DOWN, buff=.12)
    return VGroup(pic, read, year, note, down, up, dl, ul)


class LivingScene(SpokenScene):
    """Keep the current subject gently alive during word-synchronisation holds."""
    def wait(self, duration=1, *args, **kwargs):
        if duration > .35 and self.mobjects:
            candidates = [m for m in self.mobjects if not isinstance(m, (Text, MarkupText))
                          and m.width > .25 and m.height > .25]
            if candidates:
                subject = max(candidates, key=lambda m: m.width * m.height)
                return self.play(subject.animate.scale(1.018), run_time=duration,
                                 rate_func=there_and_back)
        return super().wait(duration, *args, **kwargs)


class S00Title(TitleCard):
    LESSON = "Producers, consumers and decomposers"
    TITLE = "The Leaf Pile That Stops Growing"


class S01Hook(LivingScene):
    def construct(self):
        w = forest_world(1, False)
        self.play(FadeIn(w.soil), FadeIn(w.tree), FadeIn(w.pile), run_time=.8)
        fall = falling_leaves()
        bob(w.tree.crown, amp=.035, speed=1.1)
        self.at("New leaves land")
        self.play(LaggedStart(*[FadeIn(x) for x in fall], lag_ratio=.08), run_time=.7)
        self.play(*[x.animate.move_to([-.7 + i*.55, -1.7, 0]) for i, x in enumerate(fall)], run_time=2.1)
        self.at("year after year")
        stack = VGroup(*[RoundedRectangle(corner_radius=.1, width=3.3, height=.3,
                                          color=BROWN, stroke_width=2).move_to([1.15, -1.9+k*.34, 0])
                         for k in range(13)])
        stack.set_stroke(opacity=.48)
        tag = T("if every autumn stayed?", 30, BROWN).move_to([3.75, 2.8, 0])
        sch = scope_tag("schematic")
        self.play(FadeOut(fall), LaggedStart(*[Create(x) for x in stack], lag_ratio=.05), FadeIn(tag), FadeIn(sch), run_time=2.2)
        self.at("So why")
        q = T("?", 76, GOLD).move_to([1.5, .25, 0])
        self.play(FadeOut(stack), FadeOut(tag), FadeIn(q, scale=.4), run_time=.8)
        pulse(q, base=0, amp=0)
        self.finish()


class S02Tub(LivingScene):
    def construct(self):
        w = forest_world(2, False)
        self.add(w)
        tb = w.tub
        self.at("as a bathtub")
        self.play(Create(tb.outline), FadeIn(tb[1]), FadeIn(tb.drain), run_time=1.4)
        fall = falling_leaves(6)
        self.at("new layer")
        self.play(FadeIn(fall, lag_ratio=.08), run_time=.6)
        new = leaf_pile(3)[2]
        self.play(*[x.animate.move_to([-.2+i*.55, -1.55, 0]) for i, x in enumerate(fall)], run_time=1.5)
        self.play(ReplacementTransform(fall, new), run_time=.55)
        tag = chip("+1 autumn", GOLD, size=30).move_to([4.35, 1.7, 0])
        self.play(FadeIn(tag, shift=DOWN*.15), run_time=.4)
        self.at("pile stays low")
        self.play(Indicate(VGroup(w.pile, new), color=GOLD), run_time=1.0)
        self.at("draining it")
        q = T("?", 54, PURPLE).move_to([1.55, -.95, 0])
        self.play(FadeOut(tag), FadeIn(q, scale=.5), tb.drain.animate.set_color(PURPLE), run_time=.7)
        pulse(tb.drain)
        self.finish()


class S03Producer(LivingScene):
    def construct(self):
        w = forest_world(2)
        self.add(w)
        self.at("The oak is")
        self.play(w.tree.crown.animate.set_fill(GREEN, .58), run_time=.75)
        lab = chip("producer = the tap", GREEN, size=30).move_to([-1.2, 2.75, 0])
        self.play(FadeIn(lab, shift=LEFT*.15), run_time=.45)
        sun = Circle(radius=.48, color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=.65).move_to([-6, 3, 0])
        ray = arrow(sun.get_center()+RIGHT*.4, [-5.05, 2.25, 0], YELLOW, 7)
        self.at("captures energy")
        self.play(FadeIn(sun, scale=.5), GrowArrow(ray), run_time=.85)
        sugar = chip("sugar", GOLD, size=28).move_to([-3.35, .2, 0])
        self.at("stores it")
        self.play(FadeIn(sugar, shift=DOWN*.2), run_time=.55)
        co2 = T("carbon dioxide", 28, GOLD).move_to([2.0, 1.65, 0])
        water = T("water", 28, GOLD).move_to([-5.65, -3.12, 0])
        nutrients = T("nutrients", 28, GOLD).move_to([-3.25, -3.12, 0])
        air_dots = gold_dots([(1.5,1.2,0),(2.0,1.05,0),(2.5,1.2,0)], .08)
        soil_dots = gold_dots([(-5.3,-2.75,0),(-4.5,-2.78,0),(-3.7,-2.76,0)], .08)
        self.at("carbon dioxide")
        self.play(FadeIn(co2), FadeIn(air_dots), run_time=.6)
        self.play(air_dots.animate.move_to(w.tree.crown.get_center()), run_time=1.0)
        self.at("water and nutrients")
        self.play(FadeIn(water), FadeIn(nutrients), FadeIn(soil_dots), run_time=.6)
        self.play(soil_dots.animate.move_to([-4.5,-.5,0]), run_time=1.1)
        self.finish()


class S04Consumers(LivingScene):
    def construct(self):
        w = forest_world(2)
        self.add(w)
        deer = animal("deer", [2.25, .65, 0], .9)
        acorns = gold_dots([(1.0,-.05,0),(1.3,-.2,0),(1.55,-.02,0)], .11)
        self.at("A deer eats")
        self.play(FadeIn(acorns), FadeIn(deer, shift=RIGHT*.3), run_time=.8)
        self.play(acorns.animate.move_to(deer[0].get_center()), run_time=.8)
        first = chip("first-order consumer", ORANGE, size=28).move_to([3.7, 2.6, 0])
        self.at("first order consumer")
        self.play(FadeIn(first, shift=DOWN*.15), run_time=.6)
        self.at("A mouse eats")
        self.play(FadeOut(deer), FadeOut(first), run_time=.35)
        mouse = animal("mouse", [.1, .3, 0], .55)
        seeds = gold_dots([(-1.2,-.1,0),(-.9,.05,0)], .1)
        fox = animal("fox", [3.45, .6, 0], .9)
        self.play(FadeIn(seeds), FadeIn(mouse, shift=RIGHT*.25), run_time=.55)
        self.play(seeds.animate.move_to(mouse[0].get_center()), run_time=.55)
        self.at("fox eats")
        self.play(FadeIn(fox, shift=RIGHT*.35), run_time=.65)
        moving = gold_dots([(0,.45,0),(.25,.35,0),(.45,.5,0)], .08)
        self.add(moving)
        self.play(moving.animate.move_to(fox[0].get_center()), mouse.animate.move_to([2.5,.45,0]).set_opacity(.15), run_time=.9)
        second = chip("second-order consumer", ORANGE, size=28).move_to([3.65, 2.6, 0])
        self.at("second order consumer")
        self.play(FadeIn(second, shift=DOWN*.15), run_time=.6)
        bob(fox, amp=.035)
        self.finish()


class S05Carry(LivingScene):
    def construct(self):
        w = forest_world(2)
        deer = animal("deer", [1.0, .8, 0], .72)
        fox = animal("fox", [4.3, .8, 0], .72)
        self.add(w, deer, fox)
        path1 = CurvedArrow([-3.7, .45, 0], [.25, .7, 0], angle=-.25, color=GOLD, stroke_width=5)
        path2 = CurvedArrow([1.55, .4, 0], [3.55, .65, 0], angle=-.25, color=GOLD, stroke_width=5)
        self.at("carry some matter")
        self.play(Create(path1), Create(path2), run_time=1.0)
        dots = gold_dots([(-3.5,.55,0),(-3.2,.62,0),(-2.9,.68,0)], .085)
        self.play(FadeIn(dots), dots.animate.move_to([3.8,.75,0]), run_time=1.5)
        self.at("every animal dies")
        self.play(FadeOut(deer), FadeOut(fox), FadeOut(path1), FadeOut(path2), run_time=.7)
        dead = animal("mouse", [1.45, -1.45, 0], .55).rotate(.12)
        dead.remove(dead[-1])
        eyes = VGroup(T("×", 26, ORANGE), T("×", 26, ORANGE)).arrange(RIGHT, buff=.08).move_to([1.78,-1.35,0])
        eyes.layout_ok = True  # deliberate cartoon eyes sit on the animal's head
        self.play(FadeIn(dead, shift=UP*.3), FadeIn(eyes), run_time=.65)
        self.at("joins the dead leaves")
        self.play(dead.animate.shift(DOWN*.38), eyes.animate.shift(DOWN*.38), run_time=.75)
        bob(w.tree.crown, amp=.03, speed=1)
        self.finish()


class S06Drain(LivingScene):
    def construct(self):
        bg = RoundedRectangle(corner_radius=.3, width=12, height=5.4, color=BROWN,
                              fill_color=BROWN, fill_opacity=.12).move_to([0,-.15,0])
        bg.layout_ok = True  # deliberate tinted close-up field behind all labels
        leaves = VGroup(*[leaf([x,y,0], 1.15, holes=i%2==0) for i,(x,y) in enumerate(
            [(-4.8,2.1),(-2.2,1.7),(.5,2.1),(3.2,1.6),(-3.7,-.7),(-.8,-.4),(2.2,-.8),(4.6,-.3)])])
        self.play(FadeIn(bg), FadeIn(leaves, lag_ratio=.08), run_time=1.0)
        fungi = fungus_field()
        self.at("Fungus threads spread")
        self.play(LaggedStart(*[Create(x) for x in fungi[0]], lag_ratio=.08), run_time=1.3)
        bact_lab = T("bacteria · enlarged, schematic", 28, PURPLE).move_to([2.9, -2.52, 0])
        self.at("Bacteria")
        self.play(FadeIn(fungi[1], lag_ratio=.1), FadeIn(bact_lab), run_time=.8)
        title = chip("decomposers = the drain", PURPLE, size=32).move_to([-3.0, 3.35, 0])
        self.at("These are decomposers")
        self.play(FadeIn(title, shift=DOWN*.15), run_time=.55)
        self.at("break down dead plants")
        self.play(leaves.animate.set_opacity(.45), fungi[0].animate.set_stroke(width=7), run_time=1.1)
        self.at("A fungus has no mouth")
        self.play(FadeOut(bact_lab), FadeOut(fungi[1]), FadeOut(title), FadeOut(leaves[1:]), run_time=.65)
        focus_leaf = leaves[0]
        self.play(focus_leaf.animate.scale(1.8).move_to([-3,0,0]), fungi[0][0].animate.scale(1.35).move_to([3,0,0]), run_time=.85)
        sparks = VGroup(*[Dot([1.35,y,0], radius=.1, color=PURPLE) for y in (-.45,0,.45)])
        self.at("releases chemicals")
        self.play(FadeIn(sparks), sparks.animate.shift(LEFT*2.1), run_time=1.1)
        bits = VGroup(*[Square(.32, color=BROWN, fill_color=BROWN, fill_opacity=.65).move_to([-3.8+i*.55,-.2+(i%2)*.55,0]) for i in range(6)])
        self.at("break the leaf down")
        self.play(FadeOut(sparks), ReplacementTransform(focus_leaf, bits), run_time=.9)
        outside = T("outside the fungus", 30, PURPLE).move_to([0,-2.5,0])
        self.at("outside its body")
        self.play(FadeIn(outside), run_time=.45)
        self.at("takes in")
        self.play(*[b.animate.move_to([2.2+(i%3)*.45,-.35+(i//3)*.55,0]).scale(.55) for i,b in enumerate(bits)], run_time=1.3)
        self.finish()


class S07Predict(LivingScene):
    def construct(self):
        start = balance_picture().scale(.9).shift(LEFT*2.25+UP*.55)
        self.play(FadeIn(start), run_time=.7)
        hundred = chip("100%", GOLD, size=36).move_to([3.25,1.25,0])
        self.at("fallen leaves lost")
        self.play(FadeIn(hundred), run_time=.45)
        left = chip("55–60% left", GOLD, size=32).move_to(hundred)
        self.play(swap(hundred, left), start[-1].animate.scale(.73), run_time=1.25)
        year = T("about 1 year · Weimer Run leaf bags", 28, BLUE_GREY).move_to([2.65,.35,0])
        note = T("a balance shows how much, not where", 28, BLUE_GREY).move_to([2.45,-.45,0])
        self.play(FadeIn(year), FadeIn(note), run_time=.65)
        self.at("where does much")
        down = arrow([2.3,-.8,0],[2.3,-1.9,0],GOLD)
        up = arrow([4.1,-.8,0],[4.1,-1.9,0],GOLD)
        dl, ul = T("soil?",30,GOLD).next_to(down,DOWN,.12), T("air?",30,GOLD).next_to(up,DOWN,.12)
        self.play(GrowArrow(down), GrowArrow(up), FadeIn(dl), FadeIn(ul), run_time=.8)
        self.at("Into the soil")
        q = question_card("Into the soil, or into the air? Decide.", y=-3.25, size=30)
        self.play(FadeIn(q.question), run_time=.55)
        pulse(up); pulse(down)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Into the soil, or into the air? Decide."
    CARD = {"y": -3.25, "size": 30}
    RING_AT = (6.0, -3.2, 0)
    def backdrop(self):
        return predict_backdrop()


class S09Reveal(LivingScene):
    def construct(self):
        w = forest_world(2)
        fungi = VGroup(*[CubicBezier([x,-2.15,0],[x-.2,-1.6,0],[x+.2,-1.1,0],[x,-.75,0], color=PURPLE, stroke_width=5)
                         for x in (-1.6,-.4,.8,2.0,3.2)])
        lf = leaf([1.0,-1.35,0],2.2)
        self.add(w, fungi, lf)
        bob(fungi, amp=.09, speed=1.35)
        air = arrow([2.4,-.7,0],[2.4,2.5,0],GOLD,8)
        self.at("goes into the air")
        self.play(GrowArrow(air), run_time=.8)
        stream = gold_dots([(1.7,-.6,0),(2.1,-.3,0),(2.45,0,0),(2.3,.35,0),(2.5,.7,0)], .1)
        self.play(FadeIn(stream), stream.animate.shift(UP*1.55), lf.animate.scale(.82), run_time=1.4)
        lab = fit_text("carbon dioxide and water · respiration", 5.2, 30, GOLD).move_to([3.35,2.9,0])
        self.at("by respiration")
        self.play(FadeIn(lab, shift=DOWN*.15), run_time=.6)
        self.at("gives off carbon")
        self.play(stream.animate.shift(UP*.55).set_opacity(.25), lf.animate.scale(.83), run_time=1.0)
        stay = gold_dots([(-.8,-1.4,0),(.2,-1.5,0)],.1)
        self.at("Some matter stays")
        self.play(FadeIn(stay), fungi.animate.set_stroke(width=7), run_time=.65)
        rain = VGroup(*[Line([x,1.0,0],[x-.15,.45,0],color=BLUE_GREY,stroke_width=4) for x in (-3.0,-2.5,-2.0)])
        soil_dots = gold_dots([(-3,-.1,0),(-2.55,-.15,0),(-2.1,-.1,0)],.09)
        self.at("rain washes")
        self.play(FadeIn(rain), FadeIn(soil_dots), run_time=.5)
        self.play(rain.animate.shift(DOWN*2.3), soil_dots.animate.shift(DOWN*2.15), run_time=1.2)
        self.add(scope_tag("general process · not measured in the bags"))
        self.finish()


class S10Nutrients(LivingScene):
    def construct(self):
        w = forest_world(2)
        fungi = VGroup(*[Line([x,-2.1,0],[x+.2,-1.25,0],color=PURPLE,stroke_width=5) for x in (-.8,.2,1.2,2.2)])
        self.add(w, fungi)
        bob(w.tree.crown, amp=.09, speed=1.2)
        bob(fungi, amp=.07, speed=1.45, seed=2)
        dots = gold_dots([(-.5,-1.7,0),(.1,-1.75,0),(.7,-1.7,0)],.1)
        self.at("Nutrients")
        lab = T("nutrients",30,GOLD).move_to([1.0,-3.1,0])
        self.play(FadeIn(dots), FadeIn(lab), run_time=.55)
        self.play(dots.animate.shift(DOWN*.9), run_time=.9)
        self.at("roots take them up")
        path = CurvedArrow([.2,-2.75,0],[-4.2,-1.2,0],angle=-.35,color=GOLD,stroke_width=6)
        self.play(Create(path), dots.animate.move_to([-4.45,-1.1,0]), run_time=1.15)
        spring = VGroup(*[Ellipse(width=.4,height=.2,color=GREEN,fill_color=GREEN,fill_opacity=.7).move_to([-5.0+i*.3,2.0+(i%2)*.35,0]) for i in range(5)])
        self.at("build new leaves")
        self.play(FadeIn(spring, lag_ratio=.1), w.tree.crown.animate.set_fill(GREEN,.55), run_time=.8)
        loop = CurvedArrow([-3.7,2.6,0],[2.7,-1.65,0],angle=-1.65,color=GOLD,stroke_width=7)
        back = CurvedArrow([2.5,-2.3,0],[-4.4,-1.7,0],angle=-.55,color=GOLD,stroke_width=7)
        self.at("all the way around")
        self.play(Create(loop), Create(back), run_time=1.1)
        cap = caption("matter goes around", 34, GOLD)
        self.play(FadeOut(lab), FadeIn(cap), run_time=.5)
        self.finish()


class S11Energy(LivingScene):
    def construct(self):
        w = forest_world(2)
        deer = animal("deer", [.1,.65,0],.65)
        fox = animal("fox", [3.2,.65,0],.65)
        fungi = VGroup(*[Line([x,-2.15,0],[x+.1,-1.45,0],color=PURPLE,stroke_width=5) for x in (.2,1.1,2.0)])
        self.add(w,deer,fox,fungi)
        sun = Circle(radius=.45,color=YELLOW,stroke_width=5,fill_color=YELLOW,fill_opacity=.65).move_to([-6,3,0])
        ray = arrow([-5.6,2.75,0],[-4.9,2.2,0],YELLOW,7)
        self.at("comes in as sunlight")
        self.play(FadeIn(sun), GrowArrow(ray), run_time=.8)
        transfers = VGroup(arrow([-3.6,.7,0],[-.7,.7,0],YELLOW,4), arrow([.7,.7,0],[2.4,.7,0],YELLOW,4))
        self.play(LaggedStart(*[GrowArrow(a) for a in transfers],lag_ratio=.2), run_time=1.0)
        self.at("gives some of it")
        heats = VGroup(*[CurvedArrow(p,p+np.array([.45,1.05,0]),angle=.3,color=YELLOW,stroke_width=5)
                         for p in [(-4.3,1.2,0),(.1,1.15,0),(3.2,1.15,0),(1.2,-1.2,0)]])
        self.play(LaggedStart(*[Create(a) for a in heats],lag_ratio=.15), run_time=1.1)
        heat = T("heat",30,YELLOW).move_to([5.1,2.4,0])
        self.play(FadeIn(heat), heats.animate.shift(UP*.45).set_opacity(.35), run_time=.75)
        self.at("does not go around")
        cap = caption("energy: in as light, out as heat", 34, YELLOW)
        self.play(FadeIn(cap), FadeOut(transfers), run_time=.65)
        self.finish()


class S12Level(LivingScene):
    def construct(self):
        tb = tub()
        self.play(FadeIn(tb), run_time=.6)
        self.add(scope_tag("simple model · schematic"))
        level = ValueTracker(.25)
        fill = always_redraw(lambda: Rectangle(width=7.8,height=max(.12,level.get_value()*2.8),stroke_width=0,
                                                fill_color=BROWN,fill_opacity=.62).move_to([1.55,-2.35+level.get_value()*1.4,0]))
        gauge = always_redraw(lambda: Line([5.95,-2.35,0],[5.95,-2.35+level.get_value()*2.8,0],color=GOLD,stroke_width=12))
        self.add(fill,gauge)
        autumn = chip("+1 autumn",GOLD,size=30).move_to([-4.6,2.5,0])
        self.at("same leaf fall")
        self.play(FadeIn(autumn), level.animate.set_value(.58), run_time=1.1)
        self.at("drain the same share")
        self.play(tb.drain.animate.set_color(PURPLE), level.animate.set_value(.41), run_time=1.15)
        for high,low in [(.74,.54),(.84,.66),(.9,.73)]:
            self.play(level.animate.set_value(high), run_time=.65)
            self.play(level.animate.set_value(low), run_time=.65)
        self.at("as much as falls in")
        equal = T("drain = leaf fall",34,GOLD).move_to([0,2.6,0])
        self.play(FadeOut(autumn), FadeIn(equal), level.animate.set_value(.86), run_time=.8)
        self.play(level.animate.set_value(.74), run_time=.65)
        self.at("Then it stops")
        self.play(level.animate.set_value(.86), run_time=.65)
        self.play(level.animate.set_value(.74), run_time=.65)
        label = fit_text("levels off when drain = leaf fall",6.5,30,GOLD).move_to([2.1,1.75,0])
        self.at("real forest floor")
        self.play(FadeIn(label,shift=DOWN*.15), run_time=.65)
        pulse(tb.drain)
        self.finish()


class S13Takehome(LivingScene):
    def construct(self):
        w = forest_world(2)
        self.add(w)
        fill = chip("FILL",GREEN,size=34).move_to([-3.0,2.7,0])
        self.at("Producers fill")
        self.play(w.tree.crown.animate.set_fill(GREEN,.58), FadeIn(fill), run_time=.75)
        animals = VGroup(animal("deer",[.1,.65,0],.62), animal("fox",[3.4,.65,0],.62))
        carry = chip("CARRY",ORANGE,size=34).move_to([1.6,2.7,0])
        self.at("Consumers carry")
        self.play(FadeIn(animals,lag_ratio=.15), FadeIn(carry), run_time=.85)
        fungi = VGroup(*[Line([x,-2.15,0],[x+.1,-1.25,0],color=PURPLE,stroke_width=6) for x in (-.3,.7,1.7,2.7)])
        drain = chip("DRAIN",PURPLE,size=34).move_to([5.0,2.7,0])
        self.at("Decomposers drain")
        self.play(FadeIn(fungi,lag_ratio=.1), FadeIn(drain), w.tub.drain.animate.set_color(PURPLE), run_time=.85)
        loop = CurvedArrow([-3.6,1.7,0],[2.7,-1.45,0],angle=-1.55,color=GOLD,stroke_width=7)
        back = CurvedArrow([2.6,-2.2,0],[-4.4,-1.7,0],angle=-.55,color=GOLD,stroke_width=7)
        self.at("matter goes around")
        self.play(Create(loop), Create(back), run_time=1.1)
        self.finish()


class S14End(EndCard):
    LINE = "Decomposers drain the leaf pile, so the matter goes around again."
