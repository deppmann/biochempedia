"""One Patch, Two Relationships.

COLOR MAP: fungus BLUE; alga/cyanobacterium GREEN; tree/plant GOLD;
sugar YELLOW; water pale BLUE; minerals TEAL; harm RED; unaffected GREY.
Help is always a white plus badge.  All biology is a labelled cartoon.
"""
from bp_parts import *  # noqa: F401,F403


LICHEN = "#A8B8A0"
WATER = "#9ADCF2"
BROWN = "#76513B"
SKIN = "#C89569"


def alive(mob, amp=.012, speed=2.6, phase=0.0):
    """A gentle whole-subject breath; large enough to register as continued life."""
    mob._alive_t = phase
    mob._alive_s = 1.0
    center = mob.get_center().copy()

    def update(m, dt):
        m._alive_t += dt
        target = 1.0 + amp * np.sin(speed * m._alive_t)
        m.scale(target / m._alive_s, about_point=center)
        m._alive_s = target
    return mob.add_updater(update)


def help_badge(label=None, at=ORIGIN, scale=1.0):
    c = Circle(radius=0.34 * scale, color=TEXT, stroke_width=4,
               fill_color=TEXT, fill_opacity=0.12).move_to(at)
    p = T("+", 34 * scale, TEXT, weight=BOLD).move_to(c)
    g = VGroup(c, p)
    if label:
        g.add(T(label, 28, TEXT).next_to(c, RIGHT, buff=0.18))
    g.layout_ok = True
    return g


def neutral_badge(label=None, at=ORIGIN, scale=1.0):
    c = Circle(radius=0.34 * scale, color=GREY, stroke_width=4,
               fill_color=GREY, fill_opacity=0.10).move_to(at)
    m = Line(c.get_left() + RIGHT * 0.13, c.get_right() + LEFT * 0.13,
             color=GREY, stroke_width=6)
    g = VGroup(c, m)
    if label:
        g.add(T(label, 28, GREY).next_to(c, RIGHT, buff=0.18))
    g.layout_ok = True
    return g


def harm_badge(label=None, at=ORIGIN, scale=1.0):
    c = Circle(radius=0.34 * scale, color=RED, stroke_width=4,
               fill_color=RED, fill_opacity=0.12).move_to(at)
    m = T("−", 34 * scale, RED, weight=BOLD).move_to(c)
    g = VGroup(c, m)
    if label:
        g.add(T(label, 28, RED).next_to(c, RIGHT, buff=0.18))
    g.layout_ok = True
    return g


def tree_world(patch_center=(-1.5, 0.15, 0), patch_scale=1.0, width=7.0):
    """The carried bark-and-patch picture, always at the same coordinates."""
    trunk = RoundedRectangle(corner_radius=0.32, width=width, height=7.0,
                             stroke_color=GOLD, stroke_width=4,
                             fill_color=GOLD, fill_opacity=0.12).move_to([-1.5, 0, 0])
    grain = VGroup(*[
        ArcBetweenPoints([-4.55 + 0.18 * (i % 2), y, 0],
                         [1.55 - 0.18 * ((i + 1) % 2), y + 0.22, 0],
                         angle=0.08 * (-1) ** i, color=GOLD, stroke_width=2,
                         stroke_opacity=0.25)
        for i, y in enumerate(np.linspace(-2.8, 2.7, 7))
    ])
    pc = np.array(patch_center, dtype=float)
    lobes = VGroup(
        Ellipse(width=3.55, height=2.6),
        Ellipse(width=2.4, height=2.0).shift(LEFT * 1.15 + UP * 0.22),
        Ellipse(width=2.25, height=1.75).shift(RIGHT * 1.2 + DOWN * 0.28),
    ).set_stroke(LICHEN, width=4).set_fill(LICHEN, opacity=0.48)
    lobes.scale(patch_scale).move_to(pc)
    trunk.layout_ok = grain.layout_ok = lobes.layout_ok = True
    return VGroup(trunk, grain, lobes)


def lichen_cutaway(center=(-1.4, 0.15, 0), scale=1.0, labels=True):
    """The one shared lichen cutaway, rebuilt unchanged in continuing scenes."""
    c = np.array(center, dtype=float)
    shell = RoundedRectangle(corner_radius=0.45, width=8.0, height=5.1,
                             stroke_color=LICHEN, stroke_width=4,
                             fill_color=LICHEN, fill_opacity=0.14).scale(scale).move_to(c)
    threads = VGroup()
    for i in range(7):
        x = c[0] + scale * (-3.15 + i * 1.05)
        threads.add(CubicBezier([x - .35 * scale, c[1] - 1.8 * scale, 0],
                                [x + .35 * scale, c[1] - .55 * scale, 0],
                                [x - .42 * scale, c[1] + .65 * scale, 0],
                                [x + .28 * scale, c[1] + 1.8 * scale, 0],
                                color=BLUE, stroke_width=8 * scale))
    cells = VGroup(*[
        Circle(radius=.28 * scale, color=GREEN, stroke_width=4,
               fill_color=GREEN, fill_opacity=.35).move_to(
                   c + scale * np.array([x, y, 0]))
        for x, y in [(-2.55, .75), (-1.45, -.55), (-.35, .78),
                     (.75, -.48), (1.85, .62), (2.65, -.72)]
    ])
    g = VGroup(shell, threads, cells)
    if labels:
        fl = T("fungus", 30, BLUE, weight=BOLD).move_to(c + scale * np.array([-2.75, 2.05, 0]))
        al = T("alga or cyanobacterium", 28, GREEN, weight=BOLD).move_to(c + scale * np.array([1.25, -2.05, 0]))
        fl.layout_ok = al.layout_ok = True
        g.add(fl, al)
    g.shell, g.threads, g.cells = shell, threads, cells
    shell.layout_ok = threads.layout_ok = cells.layout_ok = True
    return g


def outcome_meter(selected=None):
    title = T("tree outcome", 30, GOLD, weight=BOLD).move_to([4.2, 2.45, 0])
    line = Line([4.2, 1.35, 0], [4.2, -1.35, 0], color=GREY, stroke_width=6)
    ys = [1.35, 0, -1.35]
    labs = VGroup(T("helped", 28, TEXT), T("unaffected", 28, GREY), T("harmed", 28, RED))
    for lab, y in zip(labs, ys):
        lab.move_to([5.65, y, 0])
    dots = VGroup(*[Dot([4.2, y, 0], radius=.12, color=c) for y, c in zip(ys, [TEXT, GREY, RED])])
    needle = VGroup()
    if selected is not None:
        y = ys[selected]
        needle = VGroup(Arrow([3.35, y, 0], [4.03, y, 0], buff=0, color=[TEXT, GREY, RED][selected],
                              stroke_width=6, tip_length=.22))
    tag = scope_tag("schematic")
    return VGroup(title, line, dots, labs, needle, tag)


def ripple(center=(-2.7, .15, 0), w=2.6, h=1.9, period=1.8):
    """A slow lichen ripple: a ring that grows and fades again and again (visible, steady motion)."""
    r = Ellipse(width=w, height=h, color=LICHEN, stroke_width=5).move_to(center)
    r.layout_ok = True
    r._t = 0.0

    def up(m, dt):
        m._t += dt
        a = (m._t % period) / period
        m.become(Ellipse(width=w * (1 + .75 * a), height=h * (1 + .75 * a), color=LICHEN,
                         stroke_width=5, stroke_opacity=.7 * (1 - a)).move_to(center))
        m.layout_ok = True
    return r.add_updater(up)


def prediction_world(selected=None, question=True):
    world = tree_world(patch_center=(-2.7, .15, 0), patch_scale=.70, width=5.4)
    plus = help_badge("lichen helped", at=[-2.7, -2.25, 0], scale=.85)
    meter = outcome_meter(selected)
    g = VGroup(world, plus, meter)
    if question:
        g.add(question_card("What does the tree gain or lose?", y=-2.3, size=30, max_w=4.3, left=2.45))
    return g


def outcome_row(name, left_badge, right_badge, y, color=TEXT):
    card = RoundedRectangle(corner_radius=.14, width=6.55, height=1.0,
                            stroke_color=GREY, stroke_width=1.5,
                            fill_color=GREY, fill_opacity=.22).move_to([2.45, y, 0])
    card.layout_ok = True
    label = T(name, 30, color, weight=BOLD).move_to([4.15, y, 0])
    left_badge.move_to([-.2, y, 0])
    right_badge.move_to([1.05, y, 0])
    arrow = Arrow([1.55, y, 0], [2.45, y, 0], buff=0, color=GREY,
                  stroke_width=4, tip_length=.18)
    return VGroup(card, left_badge, right_badge, arrow, label)


def outcome_board(include_other=False):
    title = T("outcomes → relationship", 34, TEXT, weight=BOLD).move_to([2.05, 2.55, 0])
    rows = VGroup(
        outcome_row("mutualism", help_badge(scale=.72), help_badge(scale=.72), 1.35),
        outcome_row("commensalism", help_badge(scale=.72), neutral_badge(scale=.72), 0.0),
        outcome_row("parasitism", help_badge(scale=.72), harm_badge(scale=.72), -1.35, RED),
    )
    g = VGroup(title, rows)
    if include_other:
        rule = Line([-.6, -2.15, 0], [5.8, -2.15, 0], color=GREY, stroke_width=2)
        other = T("other pairs: not these taught kinds", 26, GREY).move_to([2.6, -2.65, 0])
        g.add(rule, other)
    return g


def tick_deer(center=(0, 0, 0), scale=1.0, labels=True):
    c = np.array(center, dtype=float)
    skin = RoundedRectangle(corner_radius=.5, width=10.3, height=3.25,
                            stroke_color=SKIN, stroke_width=4,
                            fill_color=SKIN, fill_opacity=.25).scale(scale).move_to(c + DOWN * .6 * scale)
    tick_body = Ellipse(width=1.25, height=.9, color=BROWN, stroke_width=5,
                        fill_color=BROWN, fill_opacity=.75).scale(scale).move_to(c + UP * 1.25 * scale)
    legs = VGroup()
    for dx in (-.42, -.15, .15, .42):
        x = c[0] + dx * scale
        legs.add(Line([x, c[1] + .95 * scale, 0], [x - .28 * np.sign(dx) * scale, c[1] + .42 * scale, 0],
                      color=BROWN, stroke_width=4))
    drops = VGroup(*[Dot(c + np.array([x, .22 + .24 * i, 0]) * scale,
                             radius=.12 * scale, color=RED)
                     for i, x in enumerate((-.35, 0, .35))])
    g = VGroup(skin, tick_body, legs, drops)
    if labels:
        tl = T("blacklegged tick", 30, "#D9A877", weight=BOLD).move_to(c + np.array([2.6, 1.95, 0]) * scale)
        dl = T("deer skin", 30, SKIN, weight=BOLD).move_to(c + np.array([-3.6, -1.55, 0]) * scale)
        g.add(tl, dl)
    skin.layout_ok = tick_body.layout_ok = legs.layout_ok = drops.layout_ok = True
    return g


def long_arrow(center, color=TEXT, label="survive • reproduce"):
    ring = Arc(radius=1.05, start_angle=.2, angle=TAU * .88, arc_center=center,
               color=color, stroke_width=6)
    tip = Triangle(color=color, fill_color=color, fill_opacity=1).scale(.12).rotate(-.3).move_to(ring.get_end())
    lab = T(label, 28, color).next_to(ring, DOWN, buff=.18)
    return VGroup(ring, tip, lab)


class S01Hook(SpokenScene):
    def construct(self):
        world = tree_world(patch_center=(-1.5, .1, 0), patch_scale=.18)
        patch = world[-1]
        pulse(patch, base=4, amp=1.4, speed=2.0)
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=.8)
        self.at("single gray green patch")
        self.play(FadeIn(patch), patch.animate.scale(5.2), run_time=3.1, rate_func=smooth)
        q = T("?", 92, TEXT, weight=BOLD).move_to([3.6, .5, 0])
        self.at("different kinds of symbiosis")
        self.play(GrowFromCenter(q), run_time=.7)
        self.at("look closely inside")
        self.play(world.animate.scale(1.22).shift(RIGHT * 1.0), q.animate.scale(1.18), run_time=1.5)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Living together: symbiosis"
    TITLE = "One Patch, Two Relationships"

    def construct(self):
        world = tree_world(patch_scale=1.0)
        world.set_opacity(.35)
        pulse(world[-1], base=4, amp=1.2, speed=2)
        title = fit_text(self.TITLE, max_w=10.8, size=54, font=TITLE_FONT, weight=BOLD)
        lesson = T(self.LESSON.upper(), 24, GOLD).next_to(title, UP, buff=.35)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=.35)
        VGroup(title, lesson, rule).shift(UP * .8)
        self.add(world)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.35)
        self.finish()


class S03Inside(SpokenScene):
    def construct(self):
        patch = tree_world(patch_scale=.82)[-1]
        pulse(patch, base=4, amp=1, speed=2)
        self.add(patch)
        self.at("This patch is a lichen")
        cut = lichen_cutaway(labels=False)
        self.play(ReplacementTransform(patch, cut.shell), run_time=1.0)
        self.at("main partners are a fungus")
        self.play(LaggedStart(*[Create(t) for t in cut.threads], lag_ratio=.08), run_time=1.5)
        fl = T("fungus", 30, BLUE, weight=BOLD).move_to([-4.3, 2.5, 0])
        self.play(FadeIn(fl), run_time=.4)
        self.at("and an alga")
        self.play(LaggedStart(*[FadeIn(c, scale=.6) for c in cut.cells], lag_ratio=.12), run_time=1.5)
        al = T("alga or cyanobacterium", 28, GREEN, weight=BOLD).move_to([2.25, -2.45, 0])
        self.play(FadeIn(al), run_time=.45)
        self.at("remain different species")
        sp1 = chip("species 1", BLUE, 26).move_to([-4.7, -2.45, 0])
        sp2 = chip("species 2", GREEN, 26).move_to([-2.55, -2.45, 0])
        self.play(FadeIn(sp1), FadeIn(sp2), run_time=.7)
        self.at("sharing a common body")
        brace = Brace(cut.shell, RIGHT, color=TEXT)
        body = T("one lichen body", 30, TEXT).next_to(brace, RIGHT, buff=.2)
        self.play(GrowFromCenter(brace), FadeIn(body), run_time=.8)
        self.at("close relationship is symbiosis")
        cap = caption("different species + long close relationship = symbiosis", color=TEXT)
        self.play(FadeOut(sp1), FadeOut(sp2), FadeOut(al), FadeOut(fl), FadeIn(cap), run_time=.8)
        self.finish()


class S04Exchange(SpokenScene):
    def construct(self):
        cut = lichen_cutaway(center=(-1.2, .2, 0), scale=.88)
        alive(cut, amp=.012, speed=2.8)
        pulse(cut.shell, base=4, amp=1.0, speed=1.8)
        self.add(cut)
        self.at("Watch what moves")
        sun = VGroup(Circle(radius=.38, color=GOLD, fill_color=GOLD, fill_opacity=.35),
                     *[Line(.55 * np.array([np.cos(a), np.sin(a), 0]), .82 * np.array([np.cos(a), np.sin(a), 0]),
                            color=GOLD, stroke_width=4) for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([4.9, 2.35, 0])
        self.play(FadeIn(sun, scale=.7), run_time=.5)
        self.at("partner makes sugar")
        sugars = VGroup(*[Dot(c.get_center(), radius=.11, color=YELLOW) for c in cut.cells[::2]])
        self.play(Indicate(cut.cells, color=GREEN), FadeIn(sugars), run_time=.9)
        self.at("feeds both partners")
        targets = [cut.threads[1].get_center(), cut.cells[1].get_center(), cut.threads[5].get_center()]
        self.play(*[s.animate.move_to(t) for s, t in zip(sugars, targets)], run_time=1.4)
        self.at("threads shelter those cells")
        self.play(Indicate(cut.threads, color=BLUE, scale_factor=1.02), run_time=1.1)
        self.at("Rainwater spreads")
        drops = VGroup(*[Dot([x, 3.0, 0], radius=.13, color=WATER) for x in (-3.4, -1.2, 1.0)])
        self.play(FadeIn(drops), run_time=.3)
        self.play(*[d.animate.move_to(cut.cells[i * 2 + 1].get_center() + UP * .4) for i, d in enumerate(drops)], run_time=1.6)
        self.at("Each partner gains")
        p1 = help_badge("fungus", [-3.7, -2.55, 0], .8)
        p2 = help_badge("photosynthetic partner", [.1, -2.55, 0], .8)
        strip = caption("both helped", color=TEXT)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(strip), run_time=.8)
        self.finish()


class S04Boundary(SpokenScene):
    def construct(self):
        panels = TwoPanel("long close contact", "brief meeting", colors=(LICHEN, GOLD))
        alive(panels, amp=.006, speed=2.8)
        cut = lichen_cutaway(scale=.55, labels=False)
        panels.put(cut, "left")
        pulse(cut.shell, base=4, amp=1, speed=2)
        self.play(FadeIn(panels), FadeIn(cut), run_time=.8)
        self.at("Close contact matters")
        loop = Arrow([-5.2, -1.8, 0], [-1.4, -1.8, 0], color=LICHEN, stroke_width=5, tip_length=.22)
        self.play(GrowArrow(loop), run_time=.7)
        self.at("bird may eat a seed")
        bird = VGroup(ArcBetweenPoints([2.1, .6, 0], [2.8, .6, 0], angle=-1.2, color=GOLD, stroke_width=6),
                      ArcBetweenPoints([2.8, .6, 0], [3.5, .6, 0], angle=1.2, color=GOLD, stroke_width=6))
        seed = Dot([4.6, -.1, 0], radius=.16, color=GOLD)
        self.play(Create(bird), FadeIn(seed), run_time=.7)
        self.at("fly away")
        path = DashedLine([3.0, .6, 0], [5.8, 1.7, 0], color=GREY, stroke_width=3)
        self.play(Create(path), bird.animate.move_to([5.6, 1.7, 0]), FadeOut(seed), run_time=1.2)
        self.at("not symbiosis")
        cross = T("×", 72, GREY, weight=BOLD).move_to([3.6, -.8, 0])
        self.play(GrowFromCenter(cross), run_time=.6)
        self.at("remain together")
        self.play(Indicate(cut, color=LICHEN, scale_factor=1.02), loop.animate.set_color(TEXT), run_time=1.1)
        self.finish()


class S05Mutualism(SpokenScene):
    def construct(self):
        cut = lichen_cutaway(scale=.75, labels=False)
        alive(cut, amp=.012, speed=2.8)
        self.add(cut)
        self.at("all partners benefit")
        a = help_badge("fungus", [-3.4, -2.4, 0], .8)
        b = help_badge("alga", [-.3, -2.4, 0], .8)
        self.play(FadeIn(a), FadeIn(b), run_time=.7)
        self.at("relationship is mutualism")
        cap = caption("mutualism inside the lichen", color=TEXT)
        self.play(FadeIn(cap), run_time=.7)
        self.at("zoom back out")
        target = prediction_world(question=False)
        alive(target[0][-1], amp=.018, speed=2.8)
        self.play(FadeOut(a), FadeOut(b), FadeOut(cap), ReplacementTransform(cut, target[0]), run_time=1.4)
        self.add(target[1], target[2])
        self.at("lichen gains a place")
        self.play(FadeIn(target[1]), run_time=.7)
        self.at("tree gain or lose")
        self.play(FadeIn(target[2]), run_time=.8)
        q = question_card("What does the tree gain or lose?", y=-2.3, size=30, max_w=4.3, left=2.45)
        self.play(FadeIn(q), run_time=.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What does the tree gain or lose?"
    SECONDS = 4.5
    CARD = {"y": -2.3, "size": 30, "max_w": 4.3, "left": 2.45}
    RING_AT = (3.6, -3.3, 0)

    def backdrop(self):
        return VGroup(prediction_world(question=False), ripple())


class S07Commensalism(SpokenScene):
    def construct(self):
        world = prediction_world(selected=None, question=False)
        alive(world[0][-1], amp=.018, speed=2.8)
        self.add(world)
        self.add(ripple())
        self.at("tree seems unaffected")
        chosen = prediction_world(selected=1, question=False)
        alive(chosen[0][-1], amp=.018, speed=2.8)
        self.play(ReplacementTransform(world, chosen), run_time=1.0)
        seems = T("seems unaffected", 34, GREY, weight=BOLD).move_to([4.45, -2.15, 0])
        self.play(FadeIn(seems), run_time=.45)
        self.at("almost never harm")
        self.play(Indicate(seems, color=TEXT, scale_factor=1.06), run_time=1.1)
        self.at("partner benefits")
        bracket = Brace(VGroup(chosen[1], chosen[2]), DOWN, color=TEXT)
        self.play(GrowFromCenter(bracket), run_time=.7)
        self.at("relationship is commensalism")
        name = fit_text("commensalism: lichen helped, tree unaffected", max_w=4.7, size=28, color=TEXT, max_lines=3).move_to([4.5, -2.45, 0])
        self.play(FadeOut(seems), FadeIn(name), run_time=.9)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        patch = tree_world(patch_center=(-1.5, .1, 0), patch_scale=.48, width=3.3)
        patch.scale(.7).move_to([-5.0, -.4, 0])
        pulse(patch[-1], base=4, amp=1, speed=2)
        self.add(patch)
        self.at("Sort symbiosis")
        rule = fit_text("Sort by what each partner gains or loses", max_w=11.5, size=38,
                        color=TEXT, weight=BOLD).move_to([.5, 3.18, 0])
        self.play(Write(rule), run_time=1.1)
        board = outcome_board()
        board.scale(.9).move_to([2.25, -.25, 0])
        alive(board[0], amp=.01, speed=2.8)
        for i, row in enumerate(board[1]):
            alive(row, amp=.009, speed=2.8, phase=i * .8)
        self.at("rule separates the relationships")
        self.play(FadeIn(board[0]), FadeIn(board[1][0]), run_time=.8)
        self.play(FadeIn(board[1][1]), run_time=.7)
        self.at("harmful partnerships")
        self.play(FadeIn(board[1][2]), run_time=.8)
        self.at("live together closely")
        self.play(Indicate(patch[-1], color=LICHEN, scale_factor=1.04), run_time=1.0)
        self.finish()


class S09Parasitism(SpokenScene):
    def construct(self):
        pair = tick_deer()
        alive(pair[0], amp=.012, speed=2.8)
        alive(pair[1], amp=.018, speed=3.1, phase=.7)
        bob(pair[1], amp=.035, speed=2.4)
        self.at("black legged tick")
        self.play(FadeIn(pair[0]), FadeIn(pair[1]), FadeIn(pair[2]), run_time=.9)
        self.at("drink blood for days")
        self.play(FadeIn(pair[3]), pair[3].animate.shift(UP * .55), run_time=1.4)
        self.play(FadeIn(pair[4]), FadeIn(pair[5]), run_time=.5)
        self.at("tick gains food")
        plus = help_badge("tick", [-4.4, 2.5, 0], .8)
        self.play(FadeIn(plus), run_time=.6)
        self.at("deer loses blood")
        harm = harm_badge("deer", [2.3, -2.6, 0], .8)
        self.play(FadeIn(harm), run_time=.7)
        self.at("helped harmed pattern")
        link = Arrow([-3.9, 1.9, 0], [1.5, -2.6, 0], color=GREY, stroke_width=4, tip_length=.2)
        self.play(GrowArrow(link), run_time=.7)
        self.at("is parasitism")
        cap = caption("parasitism", size=38, color=RED)
        self.play(FadeIn(cap), run_time=.7)
        self.finish()


class S09Compare(SpokenScene):
    def construct(self):
        panels = TwoPanel("long close feeding", "brief attack", colors=(RED, GOLD))
        alive(panels, amp=.006, speed=2.8)
        tick = tick_deer(scale=.48, labels=False)
        panels.put(tick, "left")
        hawk = VGroup(T("hawk", 30, GOLD, weight=BOLD), Arrow(LEFT, RIGHT, color=GOLD, stroke_width=6)).arrange(DOWN, buff=.3)
        mouse = T("mouse", 30, GREY, weight=BOLD).next_to(hawk, RIGHT, buff=.5)
        predator = VGroup(hawk, mouse)
        panels.put(predator, "right")
        self.play(FadeIn(panels), FadeIn(tick), run_time=.8)
        self.at("not the same as a predator")
        self.play(FadeIn(predator), run_time=.7)
        self.at("brief attack")
        short = Line([1.3, -1.7, 0], [3.0, -1.7, 0], color=GOLD, stroke_width=8)
        self.play(GrowFromEdge(short, LEFT), hawk.animate.shift(RIGHT * 1.0), run_time=1.0)
        self.at("feeds for days or longer")
        long = Line([-5.8, -1.7, 0], [-.7, -1.7, 0], color=RED, stroke_width=8)
        self.play(GrowFromEdge(long, LEFT), run_time=1.5)
        self.at("without killing its host")
        names = VGroup(T("parasite", 36, RED, weight=BOLD).move_to([-3.25, -2.05, 0]),
                       T("predator", 36, GOLD, weight=BOLD).move_to([3.25, -2.05, 0]))
        self.play(FadeIn(names), run_time=.7)
        self.finish()


class S10Purpose(SpokenScene):
    def construct(self):
        panels = TwoPanel("lichen partners", "tick and deer", colors=(LICHEN, RED))
        alive(panels, amp=.006, speed=2.8)
        cut = lichen_cutaway(scale=.45, labels=False)
        pair = tick_deer(scale=.46, labels=False)
        panels.put(cut, "left"); panels.put(pair, "right")
        self.add(panels, cut, pair)
        self.at("chooses kindness or harm")
        thought = chip("kind?", GREY, 32).move_to([-3.2, 1.7, 0])
        self.play(FadeIn(thought), run_time=.5)
        self.play(FadeOut(thought, shift=UP * .2), run_time=.5)
        self.at("support survival and reproduction")
        lloop = long_arrow([-3.25, -.2, 0], LICHEN)
        rloop = long_arrow([3.25, -.2, 0], RED)
        self.play(Create(lloop[0]), FadeIn(lloop[1:]), Create(rloop[0]), FadeIn(rloop[1:]), run_time=1.8)
        self.at("Mutualism can support both")
        lp = VGroup(help_badge(scale=.7), help_badge(scale=.7)).arrange(RIGHT, buff=.25).move_to([-3.25, 2.0, 0])
        self.play(FadeIn(lp), run_time=.7)
        self.at("support the parasite")
        rp = help_badge("tick", [2.5, 2.0, 0], .7)
        self.play(FadeIn(rp), run_time=.6)
        self.at("harming its host")
        rh = harm_badge("deer", [4.35, 2.0, 0], .7)
        self.play(FadeIn(rh), run_time=.7)
        self.finish()


class S10Patterns(SpokenScene):
    def construct(self):
        board = outcome_board(include_other=True)
        for part in (board[1], board[2], board[3]):
            part.shift(DOWN * .3)
        alive(board[0], amp=.01, speed=2.8)
        for i, row in enumerate(board[1]):
            alive(row, amp=.01, speed=2.8, phase=i * .8)
        self.at("names describe outcomes")
        self.play(FadeIn(board[0]), run_time=.7)
        sub = T("not personalities", 30, GREY).next_to(board[0], DOWN, buff=.22)
        self.at("not personalities")
        self.play(FadeIn(sub), run_time=.5)
        self.at("Mutualism is")
        self.play(FadeIn(board[1][0]), run_time=.9)
        self.at("Commensalism is")
        self.play(FadeIn(board[1][1]), run_time=.9)
        self.at("Parasitism is")
        self.play(FadeIn(board[1][2]), run_time=.9)
        self.at("Other outcome pairs")
        self.play(Create(board[2]), FadeIn(board[3]), run_time=.9)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        patch = tree_world(patch_center=(-4.7, .45, 0), patch_scale=.42, width=3.2)
        inside = lichen_cutaway(center=(-4.7, .45, 0), scale=.28, labels=False)
        pair = tick_deer(center=[-4.7, -2.25, 0], scale=.27, labels=False)
        self.add(patch[0], patch[1], inside, pair)
        pulse(inside.shell, base=4, amp=1, speed=2)
        stops = VGroup(chip("name partners", TEXT, 28), chip("trace outcomes", TEXT, 28),
                       chip("choose kind", TEXT, 28)).arrange(DOWN, buff=.75).move_to([2.25, .2, 0])
        arrows = VGroup(Arrow(stops[0].get_bottom(), stops[1].get_top(), color=TEXT, buff=.08, tip_length=.18),
                        Arrow(stops[1].get_bottom(), stops[2].get_top(), color=TEXT, buff=.08, tip_length=.18))
        self.at("begin with partners")
        self.play(FadeIn(stops[0]), run_time=.7)
        self.at("what each receives")
        self.play(GrowArrow(arrows[0]), FadeIn(stops[1]), run_time=1.0)
        self.at("whether either is harmed")
        self.play(Indicate(pair, color=RED, scale_factor=1.04), run_time=1.0)
        self.at("name follows")
        self.play(GrowArrow(arrows[1]), FadeIn(stops[2]), run_time=.9)
        self.at("outcomes you can support")
        q = T("?", 78, GOLD, weight=BOLD).move_to(stops[2])
        self.play(ReplacementTransform(stops[2], q), run_time=.8)
        self.finish()


class S12End(EndCard):
    LINE = "Sort symbiosis by what each partner gains or loses."
