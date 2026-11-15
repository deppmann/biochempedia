"""One Tag, Different Destinations.

COLOR MAP (kept from chapter 1)
  YELLOW = ubiquitin
  GREY   = protein targets and membranes
  GREEN  = E3 ligases and ubiquitin readers
  GOLD   = auxin / signal
  RED    = proteasome / destruction
"""
from bp_parts import *  # noqa: F401,F403


LESSON = "Ubiquitin and Regulated Proteolysis as Signals"


def route_arrow(a, b, color=GREY, dashed=False):
    cls = DashedLine if dashed else Arrow
    kw = {"color": color, "stroke_width": 4}
    if dashed:
        kw["dash_length"] = 0.16
    else:
        kw.update(buff=0.08, tip_length=0.22)
    return cls(a, b, **kw)


def ub(at=ORIGIN, scale=1.0):
    return boxed_label("Ub", YELLOW, size=28, pad=0.18, fill_opacity=0.32).scale(scale).move_to(at)


def target(at=ORIGIN, text="target", w=2.5):
    return boxed_label(text, GREY, size=28, box=(w, 0.9), fill_opacity=0.42).move_to(at)


def proteasome(at=(4.9, 0, 0), height=3.5, label=True):
    """Large red barrel; the target travels through its open centre."""
    body = RoundedRectangle(corner_radius=0.55, width=2.15, height=height,
                            stroke_color=RED, stroke_width=7, fill_color=RED,
                            fill_opacity=0.32).move_to(at)
    ribs = VGroup(*[
        Line(body.get_left() + RIGHT * 0.2 + UP * y,
             body.get_right() + LEFT * 0.2 + UP * y,
             color=RED, stroke_width=3)
        for y in (-height * 0.27, height * 0.27)
    ])
    opening = RoundedRectangle(corner_radius=0.25, width=0.92, height=height - 0.45,
                               stroke_color=RED, stroke_width=3, fill_color=BG,
                               fill_opacity=1).move_to(at)
    g = VGroup(body, ribs, opening)
    if label:
        lab = T("proteasome", 28, RED).next_to(body, DOWN, buff=0.18)
        g.add(lab)
    g.body = body
    g.opening = opening
    return g


def receptor(at=(0, 0.25, 0), scale=1.0, with_ub=True):
    """A membrane-spanning receptor with one cytosolic ubiquitin."""
    c = np.array(at, dtype=float)
    membrane = VGroup(
        Line(c + [-3.2 * scale, 0.45 * scale, 0], c + [3.2 * scale, 0.45 * scale, 0], color=GREY, stroke_width=7),
        Line(c + [-3.2 * scale, 0.12 * scale, 0], c + [3.2 * scale, 0.12 * scale, 0], color=GREY, stroke_width=7),
    )
    stem = RoundedRectangle(corner_radius=0.18, width=0.75 * scale, height=2.8 * scale,
                            stroke_color=GREY, stroke_width=4, fill_color=GREY,
                            fill_opacity=0.44).move_to(c + [0, 0.30 * scale, 0])
    head = RoundedRectangle(corner_radius=0.25, width=1.55 * scale, height=0.8 * scale,
                            stroke_color=GREY, stroke_width=4, fill_color=GREY,
                            fill_opacity=0.42).move_to(c + [0, 1.55 * scale, 0])
    lab = T("receptor", 28, GREY).next_to(head, UP, buff=0.12)
    g = VGroup(membrane, stem, head, lab)
    if with_ub:
        u = ub(c + [1.15 * scale, -1.25 * scale, 0], 1.0)
        tether = Line(stem.get_right() + DOWN * 0.88, u.get_left(), color=YELLOW, stroke_width=4)
        g.add(tether, u)
        g.ub = u
    g.membrane, g.stem, g.head = membrane, stem, head
    return g


def soluble_chain(linkage="lysine 48", angled=False, at=(-2.0, 0.2, 0)):
    tgt = target(at, "protein", 2.65)
    offsets = ([(-1.0, 1.15), (-0.2, 1.75), (0.7, 1.2), (1.3, 2.0)] if angled
               else [(-0.95, 1.15), (-0.32, 1.72), (0.31, 2.29), (0.94, 2.86)])
    blocks = VGroup(*[ub(np.array(at) + [x, y, 0], 0.78) for x, y in offsets])
    links = VGroup()
    for a, b in zip(blocks[:-1], blocks[1:]):
        links.add(Line(a.get_right(), b.get_left(), color=YELLOW, stroke_width=4))
    lab = boxed_label(linkage, YELLOW, size=26, fill_opacity=0.12)
    lab.move_to(np.array(at) + [-2.55, 2.35, 0])
    return VGroup(tgt, links, blocks, lab)


def vesicle(at=(-4.65, 0.0, 0), r=1.2, label="vesicle"):
    ring = Circle(radius=r, color=TEAL, stroke_width=6, fill_color=TEAL,
                  fill_opacity=0.15).move_to(at)
    lab = T(label, 28, TEAL).next_to(ring, DOWN, buff=0.16)
    return VGroup(ring, lab)


def prediction_world():
    """Carried prediction frame used by s05 and s06 at exactly the same coordinates."""
    rec = receptor((0, 0.7, 0), 0.72)
    ves = vesicle((-4.9, 0.65, 0), 1.0, "vesicle route")
    pro = proteasome((4.95, 0.65, 0), 2.5)
    left = route_arrow(rec.get_left() + LEFT * 0.1, ves[0].get_right() + RIGHT * 0.08, dashed=True)
    right = route_arrow(rec.get_right() + RIGHT * 0.1, pro.body.get_left() + LEFT * 0.08, dashed=True)
    return VGroup(ves, pro, left, right, rec)


def prediction_question():
    return question_card("Is one Ub enough to commit it to the proteasome?",
                         y=-3.15, max_w=10.9, size=30)


def reader_cup(at, color=GREEN, scale=1.0):
    outer = RoundedRectangle(corner_radius=0.3, width=1.7, height=1.25,
                             stroke_color=color, stroke_width=5, fill_color=color,
                             fill_opacity=0.42)
    notch = Circle(radius=0.32).move_to(outer.get_bottom())
    shape = Difference(outer, notch).set_stroke(color, 5).set_fill(color, 0.42)
    return shape.scale(scale).move_to(at)


def auxin_interface(closed=False, at=(0, 0.15, 0), scale=1.0):
    """The persistent TIR1–Aux/IAA interface used in s09–s11."""
    c = np.array(at, dtype=float)
    gap = 0.15 if closed else 1.0
    tir_shape = RoundedRectangle(corner_radius=0.45, width=4.4, height=2.8,
                                 stroke_color=GREEN, stroke_width=6, fill_color=GREEN,
                                 fill_opacity=0.38)
    pocket = Circle(radius=0.42).move_to(tir_shape.get_right())
    tir_shape = Difference(tir_shape, pocket).set_stroke(GREEN, 6).set_fill(GREEN, 0.38)
    tir_shape.move_to(c + [-2.2 - gap / 2, 0, 0])
    tir_lab = T("TIR1 · E3", 30, GREEN).move_to(tir_shape)

    rep_shape = RoundedRectangle(corner_radius=0.45, width=4.0, height=2.8,
                                 stroke_color=GREY, stroke_width=6, fill_color=GREY,
                                 fill_opacity=0.38)
    bump = Circle(radius=0.42).move_to(rep_shape.get_left())
    rep_shape = Union(rep_shape, bump).set_stroke(GREY, 6).set_fill(GREY, 0.38)
    rep_shape.move_to(c + [2.0 + gap / 2, 0, 0])
    rep_lab = T("Aux/IAA repressor", 28, GREY).move_to(rep_shape.get_center() + RIGHT * 0.18)
    g = VGroup(tir_shape, tir_lab, rep_shape, rep_lab).scale(scale)
    g.tir, g.rep = VGroup(tir_shape, tir_lab), VGroup(rep_shape, rep_lab)
    g.gap = c
    return g


def destination_icon(kind, at):
    if kind == "move":
        return VGroup(vesicle(at, 0.95, "move"))
    if kind == "destroy":
        return proteasome(at, 2.15)
    beads = VGroup(*[Square(0.65, color=YELLOW, stroke_width=3, fill_color=YELLOW,
                            fill_opacity=0.45) for _ in range(3)]).arrange(RIGHT, buff=0.24).move_to(at)
    cups = VGroup(*[Arc(radius=0.34, start_angle=PI, angle=PI, color=GREEN,
                        stroke_width=4).next_to(b, UP, buff=0.08) for b in beads])
    lab = T("assemble", 28, GREEN).next_to(beads, DOWN, buff=0.18)
    return VGroup(beads, cups, lab)


class S00Hook(SpokenScene):
    def construct(self):
        e3 = reader_cup((-2.7, 0.0, 0), GREEN, 1.25)
        e3_lab = T("E3", 30, GREEN).move_to(e3)
        tgt = target((0.25, 0, 0), "recognized target", 3.3)
        one = ub((0.2, 1.15, 0), 0.9)
        self.play(FadeIn(e3), FadeIn(e3_lab), FadeIn(tgt), run_time=0.9)
        bob(tgt, amp=0.035, speed=1.5)
        self.at("oxygen changing")
        self.play(GrowFromCenter(one), run_time=0.6)
        self.at("Why does one")
        dest = VGroup(destination_icon("move", (-4.6, -1.35, 0)),
                      destination_icon("assemble", (0, -1.4, 0)),
                      destination_icon("destroy", (4.65, -1.25, 0)))
        self.play(FadeOut(VGroup(e3, e3_lab, tgt, one)), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in dest], lag_ratio=0.22), run_time=1.4)
        bob(dest, amp=0.065, speed=1.05, seed=1)
        q = fit_text("One tag — which destination?", 8.0, 38, GOLD).move_to([0.3, 3.18, 0])
        self.play(Write(q), run_time=0.8)
        self.at("Keep the same")
        key = VGroup(T("Ub", 26, YELLOW), T("targets", 26, GREY),
                     T("E3", 26, GREEN), T("proteasome", 26, RED)).arrange(RIGHT, buff=0.55)
        key.move_to([0, -3.3, 0])
        self.play(FadeIn(key), run_time=0.8)
        pulse(one[0], base=3.0, amp=1.0, speed=2.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON
    TITLE = "One Tag, Different Destinations"


class S02Single(SpokenScene):
    def construct(self):
        rec = receptor((-1.15, 0.35, 0), 1.02)
        pro = proteasome((5.15, 0.0, 0), 3.0)
        self.play(FadeIn(rec.membrane), FadeIn(rec.stem), FadeIn(rec.head), FadeIn(rec[3]), run_time=0.8)
        self.at("one ubiquitin attached")
        self.play(Create(rec[4]), GrowFromCenter(rec.ub), run_time=0.7)
        self.play(rec.ub.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=2.2)
        self.at("seldom sends")
        self.play(FadeIn(pro), pro.animate.set_opacity(0.32), run_time=0.7)
        self.play(pro.animate.set_opacity(0.48), rate_func=there_and_back, run_time=3.8)
        self.at("more often changes")
        move_lab = boxed_label("changes location", TEAL, size=30).move_to([-4.7, -2.35, 0])
        self.play(FadeIn(move_lab), run_time=0.5)
        self.play(rec.head.animate.stretch(1.08, 0), rate_func=there_and_back, run_time=3.4)
        self.at("readers can help")
        readers = VGroup(*[reader_cup((-3.5 + i * 0.9, -1.55, 0), GREEN, 0.58) for i in range(3)])
        self.play(FadeOut(move_lab), LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in readers], lag_ratio=0.2), run_time=0.8)
        self.at("pull the receptor")
        bowl = Arc(radius=2.1, start_angle=PI * 1.05, angle=PI * 0.9,
                   color=GREY, stroke_width=8, arc_center=[-1.15, 0.55, 0])
        self.play(FadeOut(rec[3]), FadeOut(rec.ub[1]), ReplacementTransform(rec.membrane, bowl),
                  VGroup(rec.stem, rec.head, rec[4], rec.ub[0], readers).animate.shift(DOWN * 1.0),
                  run_time=1.8)
        self.at("by endocytosis")
        ves = Circle(radius=1.65, color=TEAL, stroke_width=6, fill_color=TEAL,
                     fill_opacity=0.07).move_to([-1.15, -0.45, 0])
        self.play(ReplacementTransform(bowl, ves), run_time=0.9)
        pulse(ves, base=6, amp=1.2, speed=2)
        self.finish()


class S03K48(SpokenScene):
    def construct(self):
        base = target((-2.4, -0.25, 0), "protein", 2.7)
        blocks = VGroup(*[ub((-4.4 + i * 1.15, 1.0, 0), 0.78) for i in range(4)])
        self.play(FadeIn(base), LaggedStart(*[FadeIn(x) for x in blocks], lag_ratio=0.15), run_time=0.9)
        self.at("reconnect the yellow")
        model = soluble_chain("lysine 48", False, (-2.4, -0.25, 0))
        self.play(*[b.animate.move_to(model[2][i]) for i, b in enumerate(blocks)], run_time=1.0)
        self.play(Create(model[1]), FadeIn(model[3]), run_time=0.6)
        chain = VGroup(base, model[1], blocks, model[3])
        length = counter("chain length  {:.0f}", ValueTracker(4), at=[3.9, 2.8, 0], size=28, color=YELLOW)
        self.play(FadeIn(length), run_time=0.4)
        self.at("usual proteasome signal")
        pro = proteasome((4.65, -0.15, 0), 4.5)
        path = route_arrow(chain.get_right() + RIGHT * 0.12, pro.body.get_left() + LEFT * 0.12, RED)
        self.play(FadeIn(pro), GrowArrow(path), run_time=0.9)
        pulse(pro.body, base=7, amp=1.4, speed=1.5)
        self.at("red barrel engages")
        payload = RoundedRectangle(corner_radius=0.12, width=0.8, height=1.8,
                                   stroke_color=GREY, stroke_width=4, fill_color=GREY,
                                   fill_opacity=0.45).move_to(chain)
        self.play(FadeOut(path), FadeOut(chain), FadeIn(payload), run_time=0.5)
        self.play(payload.animate.move_to(pro.opening), run_time=1.0)
        self.at("breaks it down")
        peptides = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.52, height=0.3,
                                             stroke_color=GREY, fill_color=GREY, fill_opacity=0.5)
                            for _ in range(6)]).arrange_in_grid(2, 3, buff=0.22).move_to([2.1, -1.9, 0])
        self.play(FadeOut(payload, scale=0.3), LaggedStart(*[FadeIn(p, shift=LEFT * 0.3) for p in peptides], lag_ratio=0.12), run_time=1.2)
        self.at("classic destruction")
        cap = caption("classic destruction route", 32, RED)
        self.play(FadeIn(cap), run_time=0.5)
        bob(peptides, amp=0.04, speed=1.6)
        self.finish()


class S04K63(SpokenScene):
    def construct(self):
        pro = proteasome((4.85, 0, 0), 4.0)
        old = soluble_chain("lysine 48", False, (-2.3, -0.2, 0))
        self.add(pro, old)
        self.at("another linkage")
        new = soluble_chain("lysine 63", True, (-1.0, -0.5, 0))
        self.play(FadeOut(pro, shift=RIGHT * 0.4), FadeOut(old), run_time=0.6)
        self.play(FadeIn(new), run_time=0.8)
        self.at("binding domains clamp")
        cups = VGroup(reader_cup((-4.75, -0.15, 0), GREEN, 0.75),
                      reader_cup((0.6, 2.65, 0), GREEN, 0.75),
                      reader_cup((2.7, 0.35, 0), GREEN, 0.75))
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.35) for c in cups], lag_ratio=0.22), run_time=1.4)
        self.at("Several proteins")
        proteins = VGroup(boxed_label("reader", GREEN, 28), boxed_label("signaling protein", GREEN, 28),
                          boxed_label("repair protein", GREEN, 28))
        for p, pos in zip(proteins, ([-4.5, -1.45, 0], [-0.5, -2.45, 0], [4.55, -1.15, 0])):
            p.move_to(pos)
        self.play(LaggedStart(*[FadeIn(p) for p in proteins], lag_ratio=0.2), run_time=1.1)
        self.at("around one scaffold")
        whole = VGroup(new, cups, proteins)
        self.play(whole.animate.shift(DOWN * 0.08), run_time=0.8)
        self.at("damaged DNA")
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.4)
        bob(whole, amp=0.035, speed=1.25)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = prediction_world()
        self.at("receptor carrying")
        self.play(FadeIn(world[-1]), run_time=0.7)
        self.at("single mark enough")
        self.play(FadeIn(VGroup(*world[:-1])), run_time=0.9)
        self.at("Choose a destination")
        q = prediction_question()
        self.play(FadeIn(q.question), run_time=0.6)
        bob(world[-1], amp=0.035, speed=1.4)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Is one Ub enough to commit it to the proteasome?"
    CARD = {"y": -3.15, "max_w": 10.9, "size": 30}
    SECONDS = 4.5

    def backdrop(self):
        w = prediction_world()
        bob(w[-1], amp=0.035, speed=1.4)
        return w


class S07Reveal(SpokenScene):
    def construct(self):
        world = prediction_world()
        q = prediction_question()
        self.add(world, q)
        self.at("Not usually")
        no = T("not usually", 34, TEAL).move_to([3.9, 2.85, 0])
        self.play(FadeOut(VGroup(world[1], world[3])), FadeIn(no), run_time=0.8)
        self.at("helps route")
        rec = world[-1]
        mini = VGroup(RoundedRectangle(corner_radius=0.1, width=0.5, height=1.0,
                                      stroke_color=GREY, fill_color=GREY, fill_opacity=0.45),
                      Square(0.35, color=YELLOW, fill_color=YELLOW, fill_opacity=0.65).shift(RIGHT * 0.48))
        mini.move_to(rec)
        self.play(FadeOut(q), FadeOut(world[2]), FadeOut(rec), FadeIn(mini), run_time=0.5)
        self.play(mini.animate.move_to(world[0][0]), run_time=1.0)
        self.at("destruction can still cooperate")
        lys = boxed_label("lysosome", RED, size=30, box=(2.8, 1.2), fill_opacity=0.18).move_to([4.5, -0.7, 0])
        path = route_arrow(world[0][0].get_right() + RIGHT * 0.1, lys.get_left() + LEFT * 0.1, TEAL, dashed=True)
        self.play(FadeIn(lys), Create(path), run_time=0.9)
        self.at("carried to lysosomes")
        ves2 = Circle(radius=0.75, color=TEAL, stroke_width=5).move_to(world[0][0])
        self.play(FadeOut(mini), FadeIn(ves2), run_time=0.4)
        self.play(ves2.animate.move_to([2.15, -0.7, 0]), run_time=1.6)
        self.at("suggests an outcome")
        note = boxed_label("typical here, not guaranteed", GOLD, 28).move_to([0.3, 2.85, 0])
        self.play(FadeOut(no), FadeIn(note), run_time=0.6)
        pulse(lys[0], base=2.5, amp=1.0, speed=2.0)
        self.finish()


class S08Context(SpokenScene):
    def construct(self):
        head = T("typical outcomes", 36, GOLD).move_to([-0.5, 3.18, 0])
        xs = (-4.25, 0, 4.25)
        colors = (TEAL, RED, GREEN)
        titles = ("one Ub · movement", "lysine 48 · destruction", "lysine 63 · assembly")
        frames = VGroup(*[RoundedRectangle(corner_radius=0.18, width=3.75, height=3.35,
                                           stroke_color=c, stroke_width=2.5, fill_color=c,
                                           fill_opacity=0.07).move_to([x, 0.95, 0])
                          for x, c in zip(xs, colors)])
        labels = VGroup(*[fit_text(t, 3.25, 26, c, max_lines=2).move_to([x, 2.15, 0])
                          for x, t, c in zip(xs, titles, colors)])
        move = VGroup(Circle(radius=0.65, color=TEAL, stroke_width=5).move_to([-4.25, 0.45, 0]),
                      Square(0.55, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5).move_to([-4.25, 0.45, 0]))
        destroy = VGroup(*[Square(0.48, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5)
                           for _ in range(4)]).arrange(DOWN, buff=0.13).move_to([0, 0.65, 0])
        destroy.add(Arrow([0.75, 0.65, 0], [1.35, 0.65, 0], color=RED, buff=0, tip_length=0.18))
        assemble = VGroup(*[Square(0.48, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5)
                            for _ in range(3)]).arrange(RIGHT, buff=0.2).move_to([4.25, 0.65, 0])
        assemble.add(*[Arc(radius=0.32, start_angle=PI, angle=PI, color=GREEN, stroke_width=4).next_to(b, UP, buff=0.08)
                       for b in assemble[:3]])
        self.play(FadeIn(head), FadeIn(frames), FadeIn(labels), FadeIn(move), FadeIn(destroy), FadeIn(assemble), run_time=1.2)
        bob(move, amp=0.08, speed=1.1, seed=1)
        bob(destroy, amp=0.08, speed=1.1, seed=2)
        bob(assemble, amp=0.08, speed=1.1, seed=3)
        self.at("context dependent")
        context = VGroup(*[boxed_label(x, c, 26, fill_opacity=0.12) for x, c in
                           (("linkage", YELLOW), ("length", YELLOW), ("branching", YELLOW),
                            ("target", GREY), ("readers", GREEN))]).arrange(RIGHT, buff=0.22)
        fit(context, max_w=11.8)
        context.move_to([0, -1.5, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in context], lag_ratio=0.13), run_time=1.2)
        self.at("simple lookup table")
        uncertain = T("not a lookup table", 30, GOLD).move_to([0, -2.35, 0])
        self.play(FadeIn(uncertain), run_time=0.5)
        self.at("mark its reader")
        trio = VGroup(ub((-1.5, -3.15, 0), 1.0), boxed_label("reader", GREEN, 26),
                      boxed_label("target", GREY, 26)).arrange(RIGHT, buff=0.35).move_to([0, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(x) for x in trio], lag_ratio=0.2), run_time=0.8)
        pulse(head, base=1.0, amp=0.5, speed=1.6)
        self.finish()


class S09AuxinSetup(SpokenScene):
    def construct(self):
        pair = auxin_interface(False)
        bob(pair.tir, amp=0.055, speed=1.15, seed=2)
        self.at("change recognition")
        self.play(FadeIn(pair.tir), run_time=0.7)
        self.at("In plants")
        plant = boxed_label("plant cell", GREEN, 28).move_to([-4.7, 2.8, 0])
        self.play(FadeIn(plant), run_time=0.5)
        self.at("green E3 receptor")
        self.play(Indicate(pair.tir, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.at("repressor rests nearby")
        self.play(FadeIn(pair.rep, shift=LEFT * 0.2), run_time=0.8)
        weak = VGroup(*[DashedLine([-0.22, y, 0], [0.22, y, 0], color=GREY, dash_length=0.09)
                        for y in (-0.5, 0.5)])
        self.play(Create(weak), run_time=0.5)
        self.at("contact is weak")
        lab = T("weak contact", 30, GREY).move_to([0, -1.65, 0])
        self.play(FadeIn(lab), pair.rep.animate.shift(RIGHT * 0.28), run_time=0.7)
        waiting = VGroup(Square(0.48, color=YELLOW, fill_color=YELLOW, fill_opacity=0.5).move_to([3.8, -2.8, 0]),
                         proteasome((5.65, -2.65, 0), 1.25, False)).set_opacity(0.4)
        self.play(FadeIn(waiting), run_time=0.5)
        bob(pair.rep, amp=0.07, speed=1.4)
        self.finish()



def ripple_loop(mob, color=GOLD, period=1.6, n=2, r0=0.3, r1=1.1):
    """Looping expanding rings around mob (motion for long holds)."""
    rings = [Circle(radius=r0, color=color, stroke_width=3).move_to(mob.get_center()) for _ in range(n)]
    for i, ring in enumerate(rings):
        ring.phase = i / n
        def upd(m, dt, st={"t": 0.0}, i=i):
            st["t"] += dt
            p = ((st["t"] / period) + m.phase) % 1.0
            m.become(Circle(radius=r0 + (r1 - r0) * p, color=color, stroke_width=3)
                     .move_to(mob.get_center()).set_stroke(opacity=0.7 * (1 - p)))
        ring.add_updater(upd)
    return VGroup(*rings)


def stream_loop(a, b, color=GREY, n=4, period=3.0, size=0.14):
    """Small tokens drifting from a to b on loop (motion for long holds)."""
    dots = []
    for i in range(n):
        d = Square(size * 2, color=color, fill_color=color, fill_opacity=0.8, stroke_width=1)
        d.phase = i / n
        def upd(m, dt, st={"t": 0.0}):
            st["t"] += dt
            p = ((st["t"] / period) + m.phase) % 1.0
            m.move_to(a + (b - a) * p).set_opacity(min(1, 4 * p, 4 * (1 - p)))
        d.add_updater(upd)
        dots.append(d)
    return VGroup(*dots)


class S10Glue(SpokenScene):
    def construct(self):
        open_pair = auxin_interface(False)
        bob(open_pair, amp=0.15, speed=1.3, seed=3)
        self.add(open_pair)
        signal = Circle(radius=0.38, color=GOLD, stroke_width=4, fill_color=GOLD,
                        fill_opacity=0.95).move_to([0, 2.8, 0])
        self.at("fits into a pocket")
        self.play(FadeIn(signal), signal.animate.move_to([0, 0.15, 0]), run_time=1.3)
        self.at("small gold signal")
        aux_lab = boxed_label("auxin", GOLD, 28).move_to([0, 2.55, 0])
        self.play(FadeIn(aux_lab), run_time=0.5)
        self.at("grip tightens")
        open_pair.clear_updaters()
        open_pair.rep.clear_updaters()
        closed = auxin_interface(True)
        self.play(Transform(open_pair, closed), run_time=1.3)
        bob(open_pair, amp=0.18, speed=1.0, seed=4)
        self.at("without building")
        direct = T("one direct binding step", 30, TEXT).move_to([0, -1.7, 0])
        self.play(FadeIn(direct), run_time=0.6)
        self.at("molecular glue")
        glue = boxed_label("molecular glue", GOLD, 32).move_to([0, -2.75, 0])
        self.play(FadeIn(glue), Indicate(signal, color=GOLD, scale_factor=1.35), run_time=0.8)
        pulse(signal, base=4, amp=1.2, speed=2.1)
        self.add(ripple_loop(signal, r0=0.3, r1=0.7))
        self.finish()


class S11AuxinFate(SpokenScene):
    def construct(self):
        pair = auxin_interface(True, (-1.4, 0.8, 0), 1.0)
        signal = Circle(radius=0.26, color=GOLD, fill_color=GOLD, fill_opacity=0.95).move_to([-1.4, 0.9, 0])
        self.add(pair, signal)
        self.at("ligase now ubiquitinates")
        chain = VGroup(*[Square(0.45, color=YELLOW, fill_color=YELLOW, fill_opacity=0.55)
                         .move_to([0.25 + i * 0.55, 2.15 + i * 0.28, 0]) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in chain], lag_ratio=0.18), run_time=1.0)
        self.at("proteasome removes")
        pro = proteasome((4.9, 0.65, 0), 3.9)
        self.play(FadeIn(pro), run_time=0.7)
        payload = RoundedRectangle(corner_radius=0.12, width=0.8, height=1.5,
                                   stroke_color=GREY, fill_color=GREY, fill_opacity=0.45).move_to(pair.rep)
        self.play(FadeOut(pair.rep), FadeOut(chain), FadeIn(payload), run_time=0.5)
        self.play(payload.animate.move_to(pro.opening), run_time=0.9)
        self.play(FadeOut(payload, scale=0.2), run_time=0.6)
        bob(pair.tir, amp=0.2, speed=1.2, seed=5)
        self.add(stream_loop(np.array([-0.6, 0.65, 0]), np.array([3.0, 0.65, 0]), color=YELLOW, n=5, period=3.0))
        self.at("genes are released")
        off = T("genes repressed", 32, RED).move_to([-3.9, -2.3, 0])
        on = T("genes active", 32, GREEN).move_to(off)
        self.add(off)
        self.play(FadeOut(off), run_time=0.35)
        self.play(FadeIn(on), run_time=0.55)
        self.at("one binding step")
        one = boxed_label("detection + recruitment", GOLD, 28).move_to([0, -2.35, 0])
        self.play(FadeIn(one), run_time=0.6)
        self.at("tightening an E3 grip")
        rule = caption("signal tightens E3 grip → destruction", 30, GOLD)
        self.play(FadeIn(rule), FadeIn(scope_tag("schematic")), run_time=0.7)
        pulse(on[0], base=2.5, amp=1.0, speed=1.8)
        self.add(ripple_loop(pro, color=RED, period=2.0, r0=0.6, r1=1.6))
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        left = VGroup(reader_cup((-3.55, 1.55, 0), GREEN, 1.15),
                      target((-1.25, 1.55, 0), "target", 2.0))
        q1 = T("Which target?", 34, GREEN).move_to([-2.7, 3.0, 0])
        right = VGroup(ub((1.35, 1.55, 0), 0.9), reader_cup((3.25, 1.55, 0), GREEN, 0.9))
        q2 = T("Which readers?", 34, YELLOW).move_to([2.4, 3.0, 0])
        pulse(left[0], base=5, amp=1.2, speed=1.35)
        pulse(right[1], base=5, amp=1.2, speed=1.35)
        self.play(FadeIn(left), FadeIn(right), run_time=0.9)
        self.at("two ideas work together")
        self.play(FadeIn(q1), FadeIn(q2), run_time=0.7)
        self.at("E3 chooses")
        self.play(left[1].animate.next_to(left[0], RIGHT, buff=0.35), run_time=0.7)
        self.at("mark recruits")
        self.play(right[1].animate.next_to(right[0], RIGHT, buff=0.12), run_time=0.7)
        dest = VGroup(destination_icon("move", (-4.2, -0.95, 0)),
                      destination_icon("assemble", (0, -1.0, 0)),
                      destination_icon("destroy", (4.35, -0.85, 0)))
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in dest], lag_ratio=0.2), run_time=1.2)
        bob(dest, amp=0.065, speed=1.1, seed=6)
        self.at("Ubiquitin marks route")
        rule1 = fit_text("Ubiquitin marks route proteins;", 11.0, 38, YELLOW).move_to([0, -2.65, 0])
        self.play(FadeIn(rule1), run_time=0.6)
        self.at("Molecular glues change")
        rule2 = fit_text("molecular glues change what an E3 grips.", 11.0, 38, GOLD).move_to([0, -3.25, 0])
        self.play(FadeIn(rule2), run_time=0.7)
        self.at("Follow both questions")
        self.play(FadeOut(VGroup(left, right, q1, q2, dest)), run_time=0.8)
        pulse(rule1, base=1.0, amp=0.4, speed=1.5)
        pulse(rule2, base=1.0, amp=0.4, speed=1.5)
        self.finish()


class S13End(EndCard):
    LINE = "Ubiquitin marks route proteins; molecular glues change what an E3 grips."
