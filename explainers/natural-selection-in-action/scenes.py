"""How a Population Changes Colour — natural selection in action.

COLOR MAP
  CREAM: pale moths and quiet plant forms
  BLUE_BLACK: dark moths and selected plant forms
  GREEN: survival and successful reproduction
  RED: predation and removal
  TEAL: deliberate human choice / defined boundaries

The woodland is always rebuilt by ``woodland`` so every carried landmark keeps the
same scale and position. Population rows are schematic; no counts are claimed.
"""
from bp_parts import *  # noqa: F401,F403
import bp_style as _style

# Keep the gated take-home sentence verbatim while retaining the standard EndCard at >=22 pt.
_style.TITLE_FONT = "Avenir Next Condensed"

CREAM = "#E8DDB5"
BLUE_BLACK = "#23364D"
DARK_EDGE = "#78A6D0"
BARK_PALE = "#8A775F"
BARK_DARK = "#332D2A"
LEAF = "#687A58"

MIX = ["pale", "dark", "pale", "dark", "pale", "dark", "pale", "dark"]
MOTH_POS = [(-4.8, 1.1), (-3.25, 0.35), (-1.65, 1.05), (0.0, -0.4),
            (1.55, 1.0), (3.1, 0.25), (4.65, 1.0), (5.25, -0.75)]


def moth(kind="pale", scale=1.0):
    """A large schematic moth icon, never an anatomical claim."""
    fill = CREAM if kind == "pale" else BLUE_BLACK
    edge = "#FFF1C5" if kind == "pale" else DARK_EDGE
    left = Ellipse(0.72, 0.44, fill_color=fill, fill_opacity=1, stroke_color=edge,
                   stroke_width=3).rotate(0.48).shift(LEFT * 0.29 + UP * 0.03)
    right = Ellipse(0.72, 0.44, fill_color=fill, fill_opacity=1, stroke_color=edge,
                    stroke_width=3).rotate(-0.48).shift(RIGHT * 0.29 + UP * 0.03)
    body = Ellipse(0.16, 0.55, fill_color=fill, fill_opacity=1, stroke_color=edge,
                   stroke_width=2)
    g = VGroup(left, right, body).scale(scale)
    g.kind = kind
    return g


def lock_icon(color):
    shackle = Arc(radius=0.15, start_angle=0, angle=PI, color=color, stroke_width=4)
    box = RoundedRectangle(0.05, width=0.42, height=0.32, color=color,
                           fill_color=BG, fill_opacity=0.95, stroke_width=3).shift(DOWN * 0.15)
    return VGroup(shackle, box)


def bird(scale=1.0):
    """A simple bird silhouette with no species-level detail."""
    body = Ellipse(1.25, 0.72, fill_color=BLUE, fill_opacity=1,
                   stroke_color=DARK_EDGE, stroke_width=2)
    head = Circle(0.27, fill_color=BLUE, fill_opacity=1,
                  stroke_color=DARK_EDGE, stroke_width=2).shift(LEFT * 0.62 + UP * 0.2)
    beak = Triangle(fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.13)
    beak.rotate(PI / 2).shift(LEFT * 0.96 + UP * 0.19)
    tail = Triangle(fill_color=BLUE, fill_opacity=1, stroke_width=0).scale(0.22)
    tail.rotate(-PI / 2).shift(RIGHT * 0.72 + DOWN * 0.04)
    eye = Dot(head.get_center() + LEFT * 0.07 + UP * 0.06, radius=0.035, color=TEXT)
    return VGroup(body, head, beak, tail, eye).scale(scale)


def woodland(kind="pale", kinds=MIX, moth_scale=1.05, ambient=True):
    """The carried woodland at its canonical scale and place.

    Returns a group with named ``bark``, ``moths``, and ``leaves`` attributes.
    """
    bg = RoundedRectangle(0.18, width=12.6, height=5.75, stroke_color=GREY,
                          stroke_width=2, fill_color="#172018", fill_opacity=1).shift(UP * 0.15)
    bg.layout_ok = True
    bark_color = BARK_PALE if kind == "pale" else BARK_DARK
    trunk = RoundedRectangle(0.32, width=2.35, height=5.25, stroke_color=CREAM if kind == "pale" else GREY,
                             stroke_width=3, fill_color=bark_color, fill_opacity=1).shift(LEFT * 0.35 + DOWN * 0.05)
    branch = RoundedRectangle(0.25, width=11.2, height=1.32, stroke_color=CREAM if kind == "pale" else GREY,
                              stroke_width=3, fill_color=bark_color, fill_opacity=1).shift(DOWN * 0.38)
    lichen = VGroup()
    if kind == "pale":
        for x, y, s in [(-0.9, 1.5, .42), (.25, 1.0, .34), (-.45, -.95, .36),
                        (-4.4, -.4, .33), (-2.4, -.25, .27), (2.1, -.55, .35), (4.5, -.2, .28)]:
            lichen.add(Circle(s, fill_color=CREAM, fill_opacity=.33, stroke_width=0).move_to([x, y, 0]))
    leaves = VGroup(*[
        Ellipse(.62, .3, fill_color=CREAM if i % 3 == 0 else LEAF, fill_opacity=.8,
                stroke_width=0).rotate((-1) ** i * .45).move_to([x, y, 0])
        for i, (x, y) in enumerate([(-5.5, 2.35), (-4.3, 2.6), (-2.9, 2.3),
                                    (2.55, 2.45), (3.9, 2.65), (5.25, 2.25)])])
    ms = VGroup(*[moth(k, moth_scale).move_to([x, y, 0]) for k, (x, y) in zip(kinds, MOTH_POS)])
    g = VGroup(bg, trunk, branch, lichen, leaves, ms)
    g.bark = VGroup(trunk, branch, lichen)
    g.moths = ms
    g.leaves = leaves
    if ambient:
        for i, leaf in enumerate(leaves):
            bob(leaf, amp=.035, speed=.65 + .08 * i, seed=i)
        for i, m in enumerate(ms):
            bob(m, amp=.025, speed=.8 + .05 * i, seed=i + 2)
    return g


def dark_question_backdrop():
    w = woodland("dark")
    br = bird(.9).move_to([4.85, 2.55, 0])
    bob(br, amp=.04, speed=.8)
    return VGroup(w, br)


def row_moths(kinds, y, scale=.95, xs=None):
    xs = np.linspace(-4.9, 4.9, len(kinds)) if xs is None else xs
    return VGroup(*[moth(k, scale).move_to([x, y, 0]) for k, x in zip(kinds, xs)])


class S00Hook(SpokenScene):
    def construct(self):
        w = woodland("pale")
        self.play(FadeIn(w), run_time=1.1)
        self.at("Peppered moths rest")
        self.play(LaggedStart(*[FadeIn(m, scale=.6) for m in w.moths], lag_ratio=.08), run_time=1.3)
        self.at("Some are pale")
        pale = VGroup(*[m for m, k in zip(w.moths, MIX) if k == "pale"])
        self.play(LaggedStart(*[Indicate(m, color=CREAM, scale_factor=1.15) for m in pale], lag_ratio=.12), run_time=1.2)
        self.at("Others are nearly black")
        dark = VGroup(*[m for m, k in zip(w.moths, MIX) if k == "dark"])
        self.play(LaggedStart(*[Indicate(m, color=DARK_EDGE, scale_factor=1.15) for m in dark], lag_ratio=.12), run_time=1.2)
        self.at("follow them through")
        q = T("?", 92, GOLD, weight=BOLD).move_to([0, 2.45, 0])
        q.layout_ok = True  # deliberate text over the woodland background
        self.play(GrowFromCenter(q), run_time=.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Natural selection in action"
    TITLE = "How a Population Changes Colour"


class S02Population(SpokenScene):
    def construct(self):
        w = woodland("pale")
        boundary = RoundedRectangle(.22, width=12.25, height=5.45, color=TEAL, stroke_width=5).shift(UP * .15)
        self.play(FadeIn(w), Create(boundary), run_time=1.0)
        self.at("form a population")
        pop = T("population", 40, TEAL, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(pop, shift=DOWN * .12), run_time=.6)
        self.at("Each moth keeps")
        locks = VGroup(*[lock_icon(CREAM if k == "pale" else DARK_EDGE).scale(.72).next_to(m, DOWN, buff=.08)
                         for m, k in zip(w.moths, MIX)])
        self.play(LaggedStart(*[FadeIn(x, scale=.6) for x in locks], lag_ratio=.08), run_time=1.2)
        self.at("New variation first appears")
        self.play(FadeOut(locks), run_time=.35)
        sparkle = VGroup(*[Line(LEFT*.25, RIGHT*.25, color=GOLD, stroke_width=5),
                           Line(DOWN*.25, UP*.25, color=GOLD, stroke_width=5)]).move_to([5.7, 1.6, 0])
        chance = T("variation appears by chance", 30, GOLD).move_to([0, -3.2, 0])
        self.play(GrowFromCenter(sparkle), FadeIn(chance), run_time=.7)
        self.at("variation already present")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.1) for m in w.moths], lag_ratio=.08), run_time=1.4)
        self.finish()


class S03Inheritance(SpokenScene):
    def construct(self):
        parents = row_moths(MIX, 1.65)
        p_label = T("parents", 34, GREY).move_to([-5.65, 2.55, 0])
        self.play(FadeIn(p_label), LaggedStart(*[FadeIn(m, shift=UP*.2) for m in parents], lag_ratio=.06), run_time=1.1)
        for i, m in enumerate(parents):
            bob(m, amp=.05, speed=.7 + .04*i, seed=i)
        self.at("offspring usually share")
        young = row_moths(MIX, -1.35, .72)
        paths = VGroup(*[Arrow(p.get_bottom(), y.get_top(), buff=.16, color=CREAM if k == "pale" else DARK_EDGE,
                                   stroke_width=4, tip_length=.18) for p, y, k in zip(parents, young, MIX)])
        y_label = T("offspring", 34, GREEN).move_to([-5.35, -2.45, 0])
        self.play(FadeIn(y_label), LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(y))
                                                 for a, y in zip(paths, young)], lag_ratio=.08), run_time=1.6)
        for i, m in enumerate(young):
            bob(m, amp=.04, speed=.75 + .04*i, seed=i + 3)
        self.at("Real moths receive")
        pair_a = moth("pale", .6).move_to([-1.1, 3.0, 0])
        pair_b = moth("dark", .6).move_to([-.45, 3.0, 0])
        two = T("two parents", 28, TEXT).next_to(VGroup(pair_a, pair_b), RIGHT, buff=.2)
        merge = Arrow([-.75, 2.65, 0], [-.75, 2.15, 0], color=GREEN, buff=.05)
        self.play(FadeIn(pair_a), FadeIn(pair_b), FadeIn(two), GrowArrow(merge), run_time=.8)
        self.at("This picture uses")
        self.play(FadeOut(VGroup(pair_a, pair_b, two, merge)), run_time=.35)
        tag = scope_tag("model simplification")
        self.play(FadeIn(tag), Indicate(paths, color=TEAL, scale_factor=1.02), run_time=1.1)
        self.finish()


class S04Environment(SpokenScene):
    def construct(self):
        w = woodland("pale")
        self.add(w, scope_tag("schematic"))
        self.at("bark darkens with soot")
        dark = woodland("dark")
        self.play(Transform(w, dark), run_time=1.5)
        self.at("environment includes")
        env = T("environment", 38, TEAL, weight=BOLD).move_to([0, 3.35, 0])
        labels = VGroup(*[chip(x, GREY, 28) for x in ("bark", "air", "food", "predators")]).arrange(RIGHT, buff=.22)
        labels.move_to([0, -3.45, 0])
        for c in labels:
            c[1].layout_ok = True  # labels intentionally sit inside their own chips
        self.play(FadeIn(env), run_time=.35)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN*.12) for x in labels], lag_ratio=.18), run_time=1.4)
        self.at("A bird enters")
        br = bird(.95).move_to([6.4, 1.8, 0])
        self.play(br.animate.move_to([4.8, 1.8, 0]), FadeOut(labels), run_time=1.0)
        bob(br, amp=.04, speed=.9)
        self.at("stand out from the background")
        pale = [m for m, k in zip(w.moths, MIX) if k == "pale"]
        rings = VGroup(*[Circle(.58, color=RED, stroke_width=4).move_to(m) for m in pale])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=.12), run_time=1.2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        back = dark_question_backdrop()
        self.add(back)
        self.at("which color will birds")
        creams = VGroup(*[back[0].moths[i] for i, k in enumerate(MIX) if k == "pale"])
        darks = VGroup(*[back[0].moths[i] for i, k in enumerate(MIX) if k == "dark"])
        self.play(LaggedStart(*[Indicate(m, color=CREAM) for m in creams], lag_ratio=.08), run_time=.8)
        self.play(LaggedStart(*[Indicate(m, color=DARK_EDGE) for m in darks], lag_ratio=.08), run_time=.8)
        self.at("Which color will leave")
        q = question_card("Which colour leaves more young?", ["cream", "blue-black"], chips_at=[4.75, -1.75, 0])
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=.65)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which colour leaves more young?"
    OPTIONS = ["cream", "blue-black"]
    CHIPS_AT = [4.75, -1.75, 0]
    SECONDS = 4.5

    def backdrop(self):
        return dark_question_backdrop()


class S07Reveal(SpokenScene):
    def construct(self):
        w = woodland("dark")
        br = bird(.92).move_to([4.9, 2.5, 0])
        self.add(w, br, scope_tag("schematic"))
        pale_i = [i for i, k in enumerate(MIX) if k == "pale"]
        self.at("bird finds more")
        for j, i in enumerate(pale_i[:3]):
            path = ArcBetweenPoints(w.moths[i].get_center(), br.get_center() + DOWN*.35,
                                    angle=(-1)**j * .35, color=RED, stroke_width=5)
            self.play(Create(path), w.moths[i].animate.move_to(br.get_center()+DOWN*.35).set_opacity(0),
                      run_time=.55)
            self.remove(path)
        self.at("Dark moths are missed")
        darks = VGroup(*[m for i, m in enumerate(w.moths) if MIX[i] == "dark"])
        self.play(LaggedStart(*[Indicate(m, color=DARK_EDGE, scale_factor=1.14) for m in darks], lag_ratio=.1), run_time=1.1)
        self.at("survive to reproduce")
        survivors = [m for i, m in enumerate(w.moths) if i not in pale_i[:3]]
        rings = VGroup(*[Circle(.58, color=GREEN, stroke_width=4).move_to(m) for m in survivors])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=.08), run_time=1.2)
        self.at("means to have young")
        cap = caption("reproduce = have young", color=GREEN)
        self.play(FadeIn(cap), run_time=.5)
        self.at("do not become better")
        arrow = Arrow([-1.0, 2.55, 0], [1.0, 2.55, 0], color=RED, stroke_width=5)
        before = moth("dark", .75).next_to(arrow, LEFT, buff=.2)
        after = moth("pale", .75).next_to(arrow, RIGHT, buff=.2)
        slash = Line(arrow.get_corner(UL)+LEFT*.15, arrow.get_corner(DR)+RIGHT*.15, color=RED, stroke_width=8)
        self.play(FadeOut(cap), FadeIn(before), GrowArrow(arrow), FadeIn(after), Create(slash), run_time=.8)
        self.at("already had their color")
        self.play(FadeOut(VGroup(before, arrow, after, slash)), Indicate(darks, color=GREEN), run_time=.8)
        self.finish()


class S08Generation(SpokenScene):
    def construct(self):
        survivor_kinds = ["dark", "dark", "pale", "dark", "dark"]
        parents = row_moths(survivor_kinds, 1.5, 1.0, np.linspace(-4.2, 4.2, 5))
        rings = VGroup(*[Circle(.58, color=GREEN, stroke_width=4).move_to(m) for m in parents])
        self.play(LaggedStart(*[FadeIn(VGroup(m, r), shift=UP*.2) for m, r in zip(parents, rings)], lag_ratio=.1), run_time=1.0)
        for i, m in enumerate(parents):
            bob(m, amp=.045, speed=.72 + .05*i, seed=i)
        pl = T("parents", 34, GREY).move_to([-5.5, 2.35, 0])
        self.play(FadeIn(pl), run_time=.3)
        self.at("offspring fill")
        child_kinds = ["dark", "dark", "pale", "dark", "dark", "dark", "pale", "dark"]
        children = row_moths(child_kinds, -1.25, .75)
        arrows = VGroup(*[Arrow(parents[i % 5].get_bottom(), c.get_top(), buff=.18, color=GREEN,
                                  stroke_width=3, tip_length=.16) for i, c in enumerate(children)])
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in zip(arrows, children)],
                              lag_ratio=.07), run_time=1.5)
        for i, m in enumerate(children):
            bob(m, amp=.035, speed=.75 + .04*i, seed=i + 2)
        self.at("A generation is")
        brace = BraceBetweenPoints([-5.9, 1.25, 0], [-5.9, -1.0, 0], direction=LEFT, color=TEAL)
        gl = T("generation", 30, TEAL).rotate(PI/2).move_to([-6.3, .12, 0])
        self.play(GrowFromCenter(brace), FadeIn(gl), run_time=.7)
        self.at("larger share of dark")
        darks = [m for m, k in zip(children, child_kinds) if k == "dark"]
        self.play(LaggedStart(*[Indicate(m, color=DARK_EDGE, scale_factor=1.14) for m in darks], lag_ratio=.08), run_time=1.2)
        self.at("every individual kept")
        locks = VGroup(*[lock_icon(CREAM if k == "pale" else DARK_EDGE).scale(.65).next_to(m, DOWN, buff=.05)
                         for m, k in zip(children, child_kinds)])
        self.play(LaggedStart(*[FadeIn(x) for x in locks], lag_ratio=.06), run_time=.8)
        self.add(scope_tag("schematic"))
        self.finish()


def population_strip(dark_share=.5, y=0, width=10.8, height=.72):
    border = RoundedRectangle(.12, width=width, height=height, color=GREY, stroke_width=3)
    dark_w = max(.1, width * dark_share)
    pale_w = width - dark_w
    p = Rectangle(width=pale_w, height=height-.08, fill_color=CREAM, fill_opacity=.92, stroke_width=0)
    d = Rectangle(width=dark_w, height=height-.08, fill_color=BLUE_BLACK, fill_opacity=1, stroke_width=0)
    p.move_to([-width/2 + pale_w/2, y, 0]); d.move_to([-width/2 + pale_w + dark_w/2, y, 0])
    border.move_to([0, y, 0])
    return VGroup(p, d, border)


class S09Frequency(SpokenScene):
    def construct(self):
        base = population_strip(.5, 1.45)
        self.play(FadeIn(base), run_time=.6)
        self.at("called trait frequency")
        brace = Brace(base[1], UP, color=TEAL)
        lab = T("trait frequency", 34, TEAL, weight=BOLD).next_to(brace, UP, buff=.12)
        self.play(GrowFromCenter(brace), FadeIn(lab), run_time=.7)
        self.at("Advance the woodland")
        rows = [population_strip(s, y) for s, y in zip((.58, .68, .78), (.45, -.55, -1.55))]
        gen = VGroup(*[T(f"generation {i}", 28, GREY).move_to([-5.65, y, 0])
                       for i, y in enumerate((1.45, .45, -.55, -1.55), 1)])
        for r in rows:
            r.shift(RIGHT*1.05)
        self.play(FadeOut(VGroup(brace, lab)), FadeIn(gen[0]), base.animate.shift(RIGHT*1.05), run_time=.5)
        for i, r in enumerate(rows, 1):
            self.play(FadeIn(r, shift=UP*.18), FadeIn(gen[i]), run_time=.7)
        self.at("dark share usually grows")
        self.play(LaggedStart(*[Indicate(r[1], color=DARK_EDGE, scale_factor=1.02) for r in [base, *rows]], lag_ratio=.16), run_time=1.4)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Reverse(SpokenScene):
    def construct(self):
        w = woodland("dark")
        self.add(w, scope_tag("schematic"))
        self.at("clean the air")
        clean = woodland("pale")
        self.play(Transform(w, clean), run_time=1.5)
        self.at("Dark moths now stand out")
        dark_i = [i for i, k in enumerate(MIX) if k == "dark"]
        rings = VGroup(*[Circle(.58, color=RED, stroke_width=4).move_to(w.moths[i]) for i in dark_i])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=.1), run_time=1.0)
        self.at("birds remove a larger share")
        br = bird(.9).move_to([5.2, 2.5, 0])
        self.play(FadeIn(br), run_time=.35)
        for i in dark_i[:3]:
            self.play(w.moths[i].animate.move_to(br.get_center()+DOWN*.3).set_opacity(0), run_time=.42)
        self.at("direction can reverse")
        strip = population_strip(.78, -2.5, width=8.5)
        strip2 = population_strip(.42, -2.5, width=8.5)
        self.play(FadeOut(rings), FadeIn(strip), run_time=.4)
        self.play(Transform(strip, strip2), run_time=1.0)
        self.at("rarer again in Britain")
        land1 = Polygon([-1.2,.4,0],[-.7,1.0,0],[-.4,.6,0],[-.55,-.1,0],[-1.0,-.35,0],
                        color=TEAL, fill_color=TEAL, fill_opacity=.28).scale(.8).move_to([-3.0,1.7,0])
        land2 = Polygon([.1,.4,0],[1.2,.65,0],[1.7,.2,0],[1.0,-.25,0],[.25,-.1,0],
                        color=TEAL, fill_color=TEAL, fill_opacity=.28).scale(.8).move_to([2.0,1.7,0])
        maps = VGroup(land1, land2, T("Britain", 28, TEXT).next_to(land1, DOWN, buff=.12),
                      T("parts of the United States", 28, TEXT).next_to(land2, DOWN, buff=.12))
        self.play(FadeOut(VGroup(w, br, strip)), FadeIn(maps), run_time=.8)
        self.finish()


class S11Adaptation(SpokenScene):
    def construct(self):
        tp = TwoPanel("sooty bark", "pale bark", colors=(DARK_EDGE, CREAM), top=3.0, bottom=-2.15)
        left_bg = Rectangle(width=5.5, height=3.7, fill_color=BARK_DARK, fill_opacity=1, stroke_width=0)
        right_bg = Rectangle(width=5.5, height=3.7, fill_color=BARK_PALE, fill_opacity=1, stroke_width=0)
        tp.put(left_bg, "left"); tp.put(right_bg, "right")
        ml = moth("dark", 2.15).move_to(left_bg)
        mr = moth("dark", 2.15).move_to(right_bg)
        self.play(FadeIn(tp), FadeIn(left_bg), FadeIn(right_bg), FadeIn(ml), FadeIn(mr), run_time=.8)
        bob(ml, amp=.065, speed=.75, seed=1)
        bob(mr, amp=.065, speed=.82, seed=3)
        self.at("is an adaptation")
        green = Circle(1.05, color=GREEN, stroke_width=7).move_to(ml)
        self.play(Create(green), run_time=.55)
        self.at("not pale bark")
        red = Circle(1.05, color=RED, stroke_width=7).move_to(mr)
        self.play(Create(red), run_time=.5)
        self.at("depends on the environment")
        cap = caption("adaptation depends on environment", color=GREEN)
        self.play(FadeIn(cap), run_time=.55)
        self.at("Moving individuals can pass")
        self.play(FadeOut(VGroup(tp, left_bg, right_bg, ml, mr, green, red, cap)), run_time=.45)
        bounds = VGroup(*[RoundedRectangle(.16, width=5.3, height=4.4, color=TEAL, stroke_width=3)
                          .move_to([x, .25, 0]) for x in (-3.15, 3.15)])
        moving = moth("pale", 1.25).move_to([-3.2, .2, 0])
        self.play(FadeIn(bounds), FadeIn(moving), run_time=.5)
        flow = Arrow([-1.9,.2,0], [1.9,.2,0], color=TEAL, stroke_width=6)
        self.play(GrowArrow(flow), moving.animate.move_to([3.2,.2,0]), run_time=1.2)
        self.at("That is gene flow")
        label = T("gene flow: genes move between populations", 30, TEAL).move_to([0, -2.65, 0])
        self.play(FadeIn(label), run_time=.6)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        w = woodland("dark")
        self.play(FadeIn(w), run_time=.75)
        self.at("This is natural selection")
        title = T("natural selection", 42, TEAL, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(title), run_time=.45)
        self.at("inherited traits suit")
        locks = VGroup(*[lock_icon(CREAM if k == "pale" else DARK_EDGE).scale(.68).next_to(m, DOWN, buff=.06)
                         for m, k in zip(w.moths, MIX)])
        self.play(LaggedStart(*[FadeIn(x) for x in locks], lag_ratio=.06), run_time=.85)
        self.at("survive and reproduce")
        darks = [m for m, k in zip(w.moths, MIX) if k == "dark"]
        rings = VGroup(*[Circle(.58, color=GREEN, stroke_width=4).move_to(m) for m in darks])
        self.play(FadeOut(locks), LaggedStart(*[Create(r) for r in rings], lag_ratio=.08), run_time=1.0)
        self.at("become more common")
        self.play(FadeOut(VGroup(w, rings)), run_time=.4)
        steps = VGroup(chip("inherited variation", DARK_EDGE, 34, pad=.34),
                       chip("different reproduction", GREEN, 34, pad=.34),
                       chip("trait frequency changes", TEAL, 34, pad=.34)).arrange(DOWN, buff=.65)
        arrows = VGroup(*[Arrow(steps[i].get_bottom(), steps[i+1].get_top(), buff=.08, color=TEXT,
                                  stroke_width=5) for i in range(2)])
        self.play(FadeIn(steps[0]), run_time=.35)
        self.play(GrowArrow(arrows[0]), FadeIn(steps[1]), run_time=.65)
        self.play(GrowArrow(arrows[1]), FadeIn(steps[2]), run_time=.65)
        self.at("population not a moth")
        cap = caption("the population changes — each moth keeps its colour", color=GOLD)
        self.play(FadeIn(cap), Indicate(steps[2], color=TEAL), run_time=.8)
        self.finish()


class S13End(EndCard):
    LINE = "Inherited traits that help survival and reproduction become more common over generations."
