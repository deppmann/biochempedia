"""Two Ways Parent of Origin Matters — chapter 2 teaching film."""
from bp_parts import *

# COLOUR MAP (shared with chapter 1)
# maternal chromosomes + organelles = TEAL; paternal chromosomes + allele tags = GOLD
# white-eye allele = WHITE; red-eye allele = RED; Y + inactive marks = GREY
# expressed output = GREEN


LESSON_NAME = "Sex Linkage, Dosage Compensation and Non-Mendelian Inheritance"
QUESTION = "Who can continue the organelle lineage through eggs?"


def stage_board():
    """The shared dark family-board surface carried through every spoken scene."""
    b = RoundedRectangle(corner_radius=.28, width=13.15, height=7.15,
                         stroke_opacity=0, fill_color="#17242D", fill_opacity=1)
    upper = RoundedRectangle(corner_radius=.2, width=12.7, height=2.65,
                             stroke_opacity=0, fill_color=TEAL, fill_opacity=.18).move_to([0, 1.55, 0])
    lower = RoundedRectangle(corner_radius=.2, width=12.7, height=2.65,
                             stroke_opacity=0, fill_color=GOLD, fill_opacity=.16).move_to([0, -1.45, 0])
    g = VGroup(b, upper, lower)
    g.set_z_index(-20)
    return g


def lane_flow():
    """A quiet moving wash through both carried inheritance lanes."""
    bars = VGroup(Rectangle(width=.9, height=2.5, stroke_opacity=0,
                            fill_color=TEAL, fill_opacity=.12).move_to([-6.0, 1.55, 0]),
                  Rectangle(width=.9, height=2.5, stroke_opacity=0,
                            fill_color=GOLD, fill_opacity=.1).move_to([-6.0, -1.45, 0]))
    bars.set_z_index(-19)

    def move(m, dt):
        m.shift(RIGHT * dt * .9)
        if m.get_left()[0] > 6.6:
            m.shift(LEFT * 13.2)
    return bars.add_updater(move)


def drift(mob, amp=.09, speed=.75):
    """Continuous gentle movement of the lesson's subject during spoken reasoning."""
    mob._drift_t, mob._drift_last = 0.0, 0.0

    def update(m, dt):
        m._drift_t += dt
        now = amp * np.sin(speed * m._drift_t)
        m.shift(RIGHT * (now - m._drift_last))
        m._drift_last = now
    return mob.add_updater(update)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(stage_board(), lane_flow())


def heading(text, color=TEXT):
    return fit_text(text, max_w=12.2, size=38, color=color, max_lines=1).move_to([0, 3.3, 0])


def lane_frame(label, y, color, width=12.4, height=2.35):
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                           stroke_color=color, stroke_width=3, fill_color=color,
                           fill_opacity=0.09).move_to([0, y, 0])
    lab = T(label, 28, color, weight=BOLD).move_to([-5.55, y + 0.78, 0], aligned_edge=LEFT)
    return VGroup(box, lab)


def organelle(kind="mitochondrion", scale=1.0, color=TEAL):
    """A labelled schematic organelle; the drawing is intentionally non-molecular."""
    if kind == "chloroplast":
        body = RoundedRectangle(corner_radius=0.24, width=2.15, height=1.1,
                                stroke_color=color, stroke_width=4,
                                fill_color=color, fill_opacity=0.13)
        marks = VGroup(*[Line([-0.55 + i * 0.36, -0.22, 0], [-0.55 + i * 0.36, 0.22, 0],
                                  color=color, stroke_width=3) for i in range(4)])
        label = T("chloroplast", 24, TEXT).next_to(body, DOWN, buff=0.12)
    else:
        body = Ellipse(width=2.15, height=1.08, stroke_color=color, stroke_width=4,
                       fill_color=color, fill_opacity=0.13)
        marks = VGroup(*[Arc(radius=0.22, start_angle=-PI / 2, angle=PI,
                             arc_center=[-0.48 + i * 0.48, 0, 0], color=color,
                             stroke_width=3) for i in range(3)])
        label = T("mitochondrion", 24, TEXT).next_to(body, DOWN, buff=0.12)
    g = VGroup(body, marks, label).scale(scale)
    return g


def mini_organelle(radius=0.16, color=TEAL):
    return Ellipse(width=radius * 2.3, height=radius * 1.35, color=color,
                   stroke_width=3, fill_color=color, fill_opacity=0.28)


def egg(center=(-2.8, 0, 0), radius=1.65, count=12, label=True):
    c = np.array(center, dtype=float)
    shell = Circle(radius=radius, color=TEAL, stroke_width=5,
                   fill_color=TEAL, fill_opacity=0.06).move_to(c)
    nucleus = Circle(radius=0.43, color=GREY, stroke_width=3,
                     fill_color=GREY, fill_opacity=0.12).move_to(c + RIGHT * 0.25)
    pts = [(-0.95, .65), (-.45, 1.0), (.35, .92), (.9, .55),
           (-1.12, .05), (-.72, -.42), (-.15, -.88), (.58, -.77),
           (1.04, -.22), (-.32, .43), (.72, .18), (-.98, -.78)]
    organs = VGroup(*[mini_organelle(0.17).move_to(c + np.array([x, y, 0]) * radius / 1.65)
                       for x, y in pts[:count]])
    g = VGroup(shell, nucleus, organs)
    if label:
        g.add(T("egg", 30, TEAL, weight=BOLD).next_to(shell, DOWN, buff=0.14))
    g.shell, g.nucleus, g.organelles = shell, nucleus, organs
    return g


def sperm(center=(3.4, 0, 0), label=True, with_organelle=True):
    c = np.array(center, dtype=float)
    head = Ellipse(width=1.2, height=0.82, color=GOLD, stroke_width=5,
                   fill_color=GOLD, fill_opacity=0.08).move_to(c)
    nucleus = Ellipse(width=0.72, height=0.48, color=GOLD, stroke_width=3,
                      fill_color=GOLD, fill_opacity=0.18).move_to(c)
    tail = CubicBezier(c + RIGHT * .58, c + RIGHT * 1.35 + UP * .65,
                       c + RIGHT * 1.9 + DOWN * .65, c + RIGHT * 2.7,
                       color=GOLD, stroke_width=4)
    o = mini_organelle(0.14, GOLD).move_to(c + LEFT * 0.68)
    g = VGroup(head, nucleus, tail, o if with_organelle else VGroup())
    if label:
        g.add(T("sperm", 30, GOLD, weight=BOLD).next_to(head, DOWN, buff=0.2))
    g.head, g.nucleus, g.tail, g.organelle = head, nucleus, tail, o
    return g


def allele_block(color, text, center, width=2.35):
    r = RoundedRectangle(corner_radius=0.16, width=width, height=0.78,
                         stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.12).move_to(center)
    t = T(text, 27, color).move_to(r)
    return VGroup(r, t)


def two_lane_world():
    upper = lane_frame("TRANSMISSION", 1.45, TEAL)
    lower = lane_frame("EXPRESSION", -1.28, GOLD)
    return VGroup(upper, lower)


def route_map(scale=1.0, at=(-4.9, 1.75, 0)):
    x1 = Line(UL * .8, DR * .8, color=TEAL, stroke_width=8)
    x2 = Line(DL * .8, UR * .8, color=TEAL, stroke_width=8)
    y = VGroup(Line([-.55, .78, 0], [0, 0, 0], color=GREY, stroke_width=7),
               Line([.55, .78, 0], [0, 0, 0], color=GREY, stroke_width=7),
               Line([0, 0, 0], [0, -.78, 0], color=GREY, stroke_width=7))
    g = VGroup(VGroup(x1, x2), y).arrange(RIGHT, buff=.45).scale(scale).move_to(at)
    return g


def nuclear_pair(center=(0, -0.35, 0), tagged=True):
    c = np.array(center, dtype=float)
    maternal = allele_block(TEAL, "maternal", c + LEFT * 1.15, 2.0)
    paternal = allele_block(GOLD, "paternal", c + RIGHT * 1.15, 2.0)
    arrows = VGroup(Arrow(maternal.get_bottom(), c + LEFT * .65 + DOWN * 1.25,
                          buff=.12, color=GREEN, stroke_width=6),
                    Arrow(paternal.get_bottom(), c + RIGHT * .65 + DOWN * 1.25,
                          buff=.12, color=GREY, stroke_width=5))
    outputs = VGroup(T("output", 29, GREEN).move_to(c + LEFT * .65 + DOWN * 1.55),
                     T("silent", 28, GREY).move_to(c + RIGHT * .65 + DOWN * 1.55))
    tag = chip("parent-of-origin mark", GREY, 24).scale(.9)
    tag.move_to(c + RIGHT * 2.25 + DOWN * 1.15)
    g = VGroup(maternal, paternal, arrows, outputs)
    if tagged:
        g.add(tag)
    g.maternal, g.paternal, g.arrows, g.outputs, g.tag = maternal, paternal, arrows, outputs, tag
    return g


def child_node(label, center, shape="circle"):
    body = (Circle(radius=.58) if shape == "circle" else Square(side_length=1.16))
    body.set_stroke(TEXT, width=4).set_fill(BG, opacity=.85).move_to(center)
    lab = T(label, 28, TEXT).next_to(body, DOWN, buff=.16)
    badge = mini_organelle(.22).move_to(body)
    g = VGroup(body, badge, lab)
    g.body, g.badge, g.label = body, badge, lab
    return g


def lineage_world(blank_next=True):
    mother = child_node("mother", [-4.5, 1.55, 0], "circle")
    daughter = child_node("daughter", [-1.55, .1, 0], "circle")
    son = child_node("son", [1.55, .1, 0], "square")
    links = VGroup(Arrow(mother.body.get_right() + DOWN * .05, daughter.body.get_top(),
                         buff=.16, color=TEAL, stroke_width=6),
                   Arrow(mother.body.get_right() + DOWN * .05, son.body.get_top(),
                         buff=.16, color=TEAL, stroke_width=6))
    egg_slot = Circle(radius=.62, color=GREY, stroke_width=3).move_to([-1.55, -1.95, 0])
    sperm_slot = Ellipse(width=1.25, height=.75, color=GREY, stroke_width=3).move_to([1.55, -1.95, 0])
    slots = VGroup(egg_slot, sperm_slot,
                   T("next eggs", 28, GREY).next_to(egg_slot, DOWN, buff=.13),
                   T("sperm", 28, GREY).next_to(sperm_slot, DOWN, buff=.2))
    g = VGroup(mother, links, daughter, son, slots)
    g.mother, g.daughter, g.son = mother, daughter, son
    g.egg_slot, g.sperm_slot, g.slots = egg_slot, sperm_slot, slots
    board = RoundedRectangle(corner_radius=.22, width=11.8, height=6.0,
                             stroke_opacity=0, fill_color=GREY,
                             fill_opacity=.11).move_to([0, .15, 0])
    board.set_z_index(-2)
    g.add(board)
    return g


def predict_backdrop():
    w = lineage_world()
    # Leave the bottom band free for the question; lift and slightly shrink the lineage.
    w.scale(.82).move_to([0, .65, 0])
    neutral = T("EXPRESSION — neutral", 28, GREY).move_to([0, -2.12, 0])
    pulse(w[-1], base=2, amp=.8, speed=1.0)
    drift(w)
    return VGroup(w, neutral)


class S00Title(TitleCard):
    LESSON = LESSON_NAME
    TITLE = "Two Ways Parent of Origin Matters"


class S01Hook(FilmScene):
    def construct(self):
        route = route_map(.65, (-5.25, 2.15, 0))
        self.play(FadeIn(route, shift=RIGHT * .2), run_time=.7)
        self.at("Can parent of origin")
        e, s = egg((-1.7, .65, 0), 1.25, 8), sperm((2.0, .65, 0))
        s.scale(.85)
        self.play(GrowFromCenter(e), FadeIn(s, shift=LEFT), run_time=1.0)
        self.at("It can")
        q1 = chip("Which DNA arrives?", TEAL, 31).move_to([-3.2, -2.05, 0])
        q2 = chip("Which allele acts?", GOLD, 31).move_to([3.2, -2.05, 0])
        self.play(FadeIn(q1, shift=DOWN * .2), run_time=.7)
        self.play(FadeIn(q2, shift=DOWN * .2), run_time=.7)
        self.at("The key is")
        self.play(Indicate(q1, color=TEAL), Indicate(q2, color=GOLD), run_time=1.3)
        self.finish()


class S02TwoLanes(FilmScene):
    def construct(self):
        world = two_lane_world()
        pulse(world[0][0], base=3, amp=1.2, speed=1.1)
        pulse(world[1][0], base=3, amp=1.2, speed=1.1)
        self.play(FadeIn(world), run_time=.7)
        self.at("organelle inheritance")
        orgs = VGroup(*[mini_organelle(.24).move_to([-3.9 + i * 1.35, 1.25, 0]) for i in range(6)])
        self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * .35) for o in orgs], lag_ratio=.12), run_time=1.5)
        self.play(orgs.animate.shift(RIGHT * 1.35), run_time=1.0)
        self.at("genomic imprinting")
        pair = VGroup(allele_block(TEAL, "maternal copy", [-2.2, -1.45, 0], 2.95),
                      allele_block(GOLD, "paternal copy", [1.0, -1.45, 0], 2.95))
        self.play(FadeIn(pair[0], shift=RIGHT), FadeIn(pair[1], shift=LEFT), run_time=1.1)
        out = Arrow([2.65, -1.45, 0], [4.7, -1.45, 0], color=GREEN, stroke_width=7)
        self.play(GrowArrow(out), run_time=.8)
        self.at("Keep transmission")
        self.play(Indicate(world[0], color=TEAL), Indicate(world[1], color=GOLD), run_time=1.2)
        self.at("Both mechanisms")
        cap = caption("Same parent effect • different physical reason", 31, TEXT)
        self.play(FadeIn(cap), run_time=.7)
        self.play(orgs.animate.shift(RIGHT * .45), pair.animate.shift(RIGHT * .18), run_time=1.0)
        self.finish()


class S03Organelles(FilmScene):
    def construct(self):
        title = heading("Organelle DNA starts outside the nucleus", TEAL)
        mito = organelle("mitochondrion", .9).move_to([-2.2, 1.55, 0])
        chloro = organelle("chloroplast", .9).move_to([2.2, 1.55, 0])
        self.play(FadeIn(mito), FadeIn(chloro), run_time=.9)
        self.play(FadeIn(title), run_time=.5)
        self.at("An egg supplies")
        self.play(FadeOut(VGroup(mito, chloro, title)), run_time=.5)
        e = egg((-2.6, .2, 0), 2.05, 12)
        pulse(e.shell, base=5, amp=1.4, speed=1.2)
        self.play(GrowFromCenter(e.shell), FadeIn(e.nucleus), run_time=.8)
        self.play(LaggedStart(*[FadeIn(o) for o in e.organelles], lag_ratio=.08), run_time=1.2)
        self.at("A male gamete")
        s = sperm((2.4, .25, 0))
        self.play(FadeIn(s, shift=LEFT * .5), run_time=1.0)
        self.at("That difference")
        count_e = T("many organelles", 32, TEAL).move_to([-2.6, 2.72, 0])
        count_s = T("far less cytoplasm", 30, GOLD).move_to([2.6, 2.72, 0])
        self.play(FadeIn(count_e), FadeIn(count_s), run_time=.7)
        self.play(Indicate(e.organelles, color=TEAL), run_time=1.3)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Maternal(FilmScene):
    def construct(self):
        e = egg((-4.7, 1.2, 0), 1.0, 7, label=False)
        s = sperm((-1.9, 1.2, 0), label=False).scale(.62)
        pulse(e.shell, base=5, amp=1.4, speed=1.2)
        self.add(e, s, scope_tag("schematic"))
        self.at("exclude")
        words = ["excluded", "depleted", "destroyed"]
        panels = VGroup(*[chip(w, GREY, 27).move_to([-3.2 + i * 3.1, -.15, 0]) for i, w in enumerate(words)])
        paternal = VGroup(*[mini_organelle(.18, GOLD).move_to(p.get_top() + UP * .45) for p in panels])
        self.play(LaggedStart(*[FadeIn(VGroup(p, o), shift=DOWN * .15) for p, o in zip(panels, paternal)], lag_ratio=.16), run_time=1.3)
        self.play(*[o.animate.set_opacity(.12).shift(DOWN * .25) for o in paternal], run_time=.8)
        self.at("Organelle genomes")
        rule = caption("generally maternal; exceptions occur", 31, TEAL)
        self.play(FadeOut(panels), FadeOut(paternal), FadeIn(rule), run_time=.6)
        self.at("mother's organelle pattern")
        daughter = child_node("daughter", [2.2, 1.25, 0], "circle")
        son = child_node("son", [4.55, 1.25, 0], "square")
        a1 = Arrow(e.get_right(), daughter.body.get_left(), buff=.15, color=TEAL, stroke_width=6)
        a2 = Arrow(e.get_right(), son.body.get_left(), buff=.15, color=TEAL, stroke_width=6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=.8)
        self.play(FadeIn(daughter), FadeIn(son), run_time=.8)
        self.at("Some species")
        exception = chip("paternal or biparental", GOLD, 27).move_to([3.55, -.55, 0])
        self.play(FadeIn(exception), run_time=.7)
        self.play(exception.animate.shift(UP * .12), run_time=.8, rate_func=there_and_back)
        self.finish()


class S05Lineage(FilmScene):
    def construct(self):
        w = lineage_world()
        pulse(w[-1], base=2, amp=.8, speed=1.0)
        self.play(FadeIn(w.mother), run_time=.5)
        self.at("Both sexes")
        self.play(LaggedStart(*[GrowArrow(a) for a in w[1]], lag_ratio=.15), run_time=1.0)
        self.play(FadeIn(w.daughter), FadeIn(w.son), run_time=.8)
        self.at("Each child")
        self.play(Indicate(w.daughter.badge, color=TEAL), Indicate(w.son.badge, color=TEAL), run_time=1.0)
        self.at("But carrying")
        self.play(FadeIn(w.slots), run_time=.7)
        gap = T("?", 54, GOLD).move_to([0, -1.95, 0])
        self.play(FadeIn(gap), run_time=.5)
        self.play(w.daughter.animate.shift(UP * .05), w.son.animate.shift(UP * .05), run_time=.8, rate_func=there_and_back)
        self.finish()


class S06Imprint(FilmScene):
    def construct(self):
        title = heading("EXPRESSION", GOLD)
        self.play(FadeIn(title), run_time=.6)
        self.at("An imprinted gene")
        nucleus = Circle(radius=3.0, color=GREY, stroke_width=4,
                         fill_color=GREY, fill_opacity=.035).move_to([0, -.05, 0])
        pulse(nucleus, base=4, amp=1.2, speed=1.0)
        self.play(GrowFromCenter(nucleus), run_time=.8)
        self.at("Both parents")
        pair = nuclear_pair((0, .75, 0), tagged=False)
        pair.tag.move_to([-4.7, -1.65, 0])
        self.play(FadeIn(pair.maternal, shift=RIGHT), FadeIn(pair.paternal, shift=LEFT), run_time=1.0)
        self.at("only one parental")
        self.play(GrowArrow(pair.arrows[0]), FadeIn(pair.outputs[0]), run_time=.8)
        self.play(GrowArrow(pair.arrows[1]), FadeIn(pair.outputs[1]), run_time=.7)
        self.at("parent of origin mark")
        self.play(FadeIn(pair.tag, shift=UP * .15), run_time=.7)
        self.play(Indicate(pair.tag, color=GREY), run_time=.8)
        self.at("does not change")
        same = T("same DNA\nsequence", 30, TEXT).move_to([-4.9, 1.2, 0])
        self.play(FadeIn(same), Indicate(pair.maternal[0], color=TEAL),
                  Indicate(pair.paternal[0], color=GOLD), run_time=1.0)
        self.at("marks are set")
        cycle = CurvedArrow([3.6, -1.6, 0], [3.6, 1.65, 0], angle=PI / 1.6,
                            color=GREY, stroke_width=5)
        reset = T("set in gametes\nreset next generation", 27, GREY).move_to([4.65, -2.35, 0])
        self.play(Create(cycle), FadeIn(reset), run_time=1.1)
        self.play(Rotate(pair.tag, angle=.15), run_time=.8, rate_func=there_and_back)
        self.finish()


class S07Predict(FilmScene):
    def construct(self):
        back = predict_backdrop()
        pulse(back[0][-1], base=2, amp=.8, speed=1.0)
        self.play(FadeIn(back[0]), run_time=.8)
        self.at("Each carries it")
        w = back[0]
        self.play(Indicate(w[2].badge, color=TEAL), Indicate(w[3].badge, color=TEAL), run_time=1.0)
        self.at("Which child")
        q = question_card(QUESTION, y=-3.08, size=30, max_w=10.6)
        self.play(FadeIn(back[1]), FadeIn(q), run_time=.8)
        self.at("Trace the lineage")
        self.play(Indicate(w.egg_slot, color=TEAL), run_time=1.0)
        self.at("question is about")
        tag = T("TRANSMISSION", 28, TEAL, weight=BOLD).move_to([4.65, 2.65, 0])
        self.play(FadeIn(tag), run_time=.6)
        self.play(Indicate(tag, color=TEAL), run_time=.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = QUESTION
    SECONDS = 4.5
    CARD = {"y": -3.08, "size": 30, "max_w": 10.6}

    def setup(self):
        super().setup()
        self.add(stage_board(), lane_flow())

    def backdrop(self):
        return VGroup(predict_backdrop(),
                      T("TRANSMISSION", 28, TEAL, weight=BOLD).move_to([4.65, 2.65, 0]))


class S09Reveal(FilmScene):
    def construct(self):
        w = lineage_world()
        pulse(w[-1], base=2, amp=.8, speed=1.0)
        drift(w, amp=.1, speed=.8)
        self.add(w)
        self.at("daughter can usually")
        path_d = CurvedArrow(w.daughter.body.get_right(), w.egg_slot.get_right(),
                             angle=-PI / 2.2, color=TEAL, stroke_width=7)
        egg_badge = mini_organelle(.22).move_to(w.egg_slot)
        self.play(Create(path_d), run_time=.7)
        self.play(FadeIn(egg_badge), w.egg_slot.animate.set_stroke(TEAL, width=5), run_time=.7)
        self.at("son can carry")
        self.play(Indicate(w.son.badge, color=TEAL), run_time=.7)
        self.at("his sperm usually")
        short = ArcBetweenPoints(w.son.body.get_right(), w.sperm_slot.get_right() + UP * .35,
                                 angle=-PI / 2.2, color=TEAL, stroke_width=7)
        pulse(short, base=7, amp=1.3, speed=1.2)
        self.play(Create(short), run_time=.7)
        end_dot = Dot(short.get_end(), radius=.12, color=TEAL)
        self.play(FadeIn(end_dot), run_time=.4)
        self.at("children can therefore")
        rule = T("usual maternal pattern; exceptions occur", 30, TEAL).move_to([2.1, 3.25, 0])
        self.play(FadeIn(rule), run_time=.6)
        self.play(Indicate(path_d, color=TEAL), Indicate(short, color=GREY), run_time=1.1)
        self.finish()


class S10Compare(FilmScene):
    def construct(self):
        tp = TwoPanel("Which DNA arrives?", "Which allele acts?", colors=(TEAL, GOLD), top=3.0, bottom=-2.5)
        self.play(FadeIn(tp), run_time=.7)
        self.at("Organel inheritance")
        e = egg((0, 0, 0), 1.15, 8, label=False)
        tp.put(e, "left")
        inlet = Arrow(e.get_left() + LEFT * .65, e.get_left(), buff=.04, color=TEAL, stroke_width=7)
        self.play(FadeIn(e), GrowArrow(inlet), run_time=1.0)
        transmitted = T("organelle DNA enters", 28, TEAL).next_to(e, DOWN, buff=.15)
        self.play(FadeIn(transmitted), run_time=.6)
        self.at("Imprinting transmits")
        pair = VGroup(allele_block(TEAL, "maternal", [0, .5, 0]),
                      allele_block(GOLD, "paternal", [0, -.5, 0])).scale(.82)
        tp.put(pair, "right")
        self.play(FadeIn(pair, shift=DOWN * .15), run_time=.8)
        self.at("filters expression")
        arrow = Arrow(pair.get_bottom(), pair.get_bottom() + DOWN * .75, buff=.08,
                      color=GREEN, stroke_width=7)
        output = T("one output", 29, GREEN).next_to(arrow, DOWN, buff=.1)
        self.play(GrowArrow(arrow), FadeIn(output), run_time=.8)
        self.at("These mechanisms")
        cap = caption("Different filters → different pedigrees", 31, TEXT)
        self.play(FadeIn(cap), run_time=.6)
        self.play(Indicate(tp.left_head, color=TEAL), Indicate(tp.right_head, color=GOLD), run_time=1.0)
        self.finish()


class S11Scope(FilmScene):
    def construct(self):
        rows = [("allele identity", "which variant?", WHITE),
                ("chromosome location", "where is it?", GOLD),
                ("parental origin", "which parent?", TEAL)]
        ledger = Ledger(rows, top_left=(-5.8, 2.25), title="READ THE PEDIGREE", row_h=.88,
                        key_w=3.6, width=8.0, size=30)
        self.play(FadeIn(ledger), run_time=.6)
        self.at("allele identity")
        self.play(ledger.reveal(0), run_time=.6)
        self.at("chromosome location")
        self.play(ledger.reveal(1), run_time=.6)
        self.at("parental origin")
        self.play(ledger.reveal(2), run_time=.6)
        self.play(ledger.mark(2, TEAL), run_time=.5)
        self.at("parent of origin can")
        branches = VGroup(chip("transmission", TEAL, 29), chip("expression", GOLD, 29)).arrange(DOWN, buff=.45).move_to([4.35, .45, 0])
        fork = VGroup(Arrow([2.1, .55, 0], branches[0].get_left(), buff=.15, color=TEAL, stroke_width=5),
                      Arrow([2.1, .3, 0], branches[1].get_left(), buff=.15, color=GOLD, stroke_width=5))
        self.play(Create(fork), FadeIn(branches), run_time=1.0)
        self.at("Most nuclear genes")
        broad = RoundedRectangle(corner_radius=.18, width=7.6, height=.72, color=GREY,
                                 fill_color=GREY, fill_opacity=.1).move_to([1.8, -1.75, 0])
        broad.layout_ok = "covered"  # intentional row enclosing its label
        broad_t = T("most nuclear genes: both copies used", 28, TEXT).move_to(broad)
        subset = chip("imprinted subset", GOLD, 25).move_to([3.7, -2.75, 0])
        self.play(FadeIn(VGroup(broad, broad_t)), run_time=.7)
        self.play(FadeIn(subset), run_time=.5)
        self.finish()


class S12Close(FilmScene):
    def construct(self):
        parent = Circle(radius=.42, color=TEAL, stroke_width=4).move_to([0, 1.65, 0])
        daughter = Circle(radius=.38, color=TEXT, stroke_width=4).move_to([-1.0, .35, 0])
        son = Square(side_length=.76, color=TEXT, stroke_width=4).move_to([1.0, .35, 0])
        pedigree = VGroup(parent, daughter, son,
                          Line(parent.get_bottom(), daughter.get_top(), color=TEAL, stroke_width=5),
                          Line(parent.get_bottom(), son.get_top(), color=TEAL, stroke_width=5))
        self.play(FadeIn(pedigree), run_time=.7)
        self.at("ask what is moving")
        glass = VGroup(Circle(radius=.85, color=GOLD, stroke_width=5),
                       Line([.58, -.58, 0], [1.25, -1.25, 0], color=GOLD, stroke_width=6)).move_to([0, .8, 0])
        self.play(FadeIn(glass), run_time=.5)
        tp = TwoPanel("organelle DNA", "nuclear alleles", colors=(TEAL, GOLD), top=2.8, bottom=-2.5)
        pulse(tp.left_frame, base=2.5, amp=.8, speed=1.0)
        pulse(tp.right_frame, base=2.5, amp=.8, speed=1.0)
        self.play(FadeOut(pedigree), FadeOut(glass), FadeIn(tp), run_time=.7)
        self.at("organelle DNA")
        e = egg((0, 0, 0), 1.25, 8, label=False)
        tp.put(e, "left")
        lab1 = chip("transmitted", TEAL, 29).move_to([-3.2, -1.85, 0])
        self.play(FadeIn(e), run_time=.8)
        self.play(FadeIn(lab1), run_time=.5)
        self.at("both nuclear alleles")
        pair = VGroup(allele_block(TEAL, "maternal", [0, .55, 0]),
                      allele_block(GOLD, "paternal", [0, -.55, 0])).scale(.88)
        tp.put(pair, "right")
        mark = chip("parental mark", GREY, 24).move_to([4.55, 1.45, 0])
        lab2 = chip("expressed", GOLD, 29).move_to([3.2, -1.85, 0])
        self.play(FadeIn(pair), run_time=.8)
        self.at("parental mark")
        self.play(FadeIn(mark), FadeIn(lab2), run_time=.8)
        self.play(Indicate(lab1, color=TEAL), Indicate(lab2, color=GOLD), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "Parent of origin can decide which DNA arrives or which allele acts."
