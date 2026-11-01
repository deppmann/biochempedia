"""Sensitive periods in behavior: windows are tides, not doors  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = the window: how open the young nervous system is to experience (curves, gauges, scores)
  YELLOW = experience that arrives: song heard, patterned light, a tutor
  PURPLE = the memory of the tutor song
  BLUE   = the young bird and its own practice singing
  GREEN  = a normal or good outcome (wild song, native-like scores, a check mark)
  RED    = an abnormal or impaired outcome, or something crossed out
  GREY   = structure, axes, the door, de-emphasized things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bird(scale=1.0, color=BLUE):
    """A sparrow from simple shapes, facing right."""
    body = Ellipse(width=1.5, height=0.95, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([0.62, 0.42, 0])
    beak = Polygon([0.93, 0.5, 0], [1.28, 0.4, 0], [0.93, 0.32, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    tail = Polygon([-0.65, 0.1, 0], [-1.4, 0.35, 0], [-1.3, -0.05, 0], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28)
    eye = Dot([0.72, 0.48, 0], radius=0.05, color=TEXT)
    legs = VGroup(Line([-0.1, -0.45, 0], [-0.1, -0.8, 0], color=color, stroke_width=4),
                  Line([0.2, -0.45, 0], [0.2, -0.8, 0], color=color, stroke_width=4))
    return VGroup(tail, body, head, beak, eye, legs).scale(scale)


def wave(x0, y, L, fn, color, amp=0.4, w=4):
    return ParametricFunction(lambda t: np.array([x0 + t, y + amp * fn(t), 0]), t_range=[0, L, 0.03],
                              color=color, stroke_width=w)


def rich(t):
    return (0.55 + 0.45 * np.sin(2.1 * t)) * np.sin(9.0 * t) + 0.25 * np.sin(23 * t + 1)


def simple(t):
    return 0.55 * np.sin(7.0 * t)


def rambling(t):
    return 0.8 * np.sin(5.0 * t + 0.8) * np.cos(17 * t) + 0.35 * np.sin(31 * t + 2) + 0.2 * np.sin(2.3 * t)


def check(at, color=GREEN, s=0.2):
    c = VMobject(stroke_color=color, stroke_width=7)
    c.set_points_as_corners([[-s, 0, 0], [-s * 0.3, -s * 0.75, 0], [s * 1.1, s * 0.9, 0]])
    return c.move_to(at)


def cross(at, color=RED, s=0.2, w=7):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=w),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=w)).move_to(at)


def axes(x0, y0, w, h):
    return VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY, stroke_width=3),
                  Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3))


def bell(t, c=0.45, s=0.17):
    return float(np.exp(-((t - c) / s) ** 2))


def door_f(t):
    return 1.0 if 0.3 < t < 0.62 else 0.04


def curve_mob(x0, y0, w, h, f, color=TEAL, sw=6, n=140, dashed=False):
    pts = [[x0 + (i / n) * w, y0 + 0.08 + f(i / n) * (h - 0.2), 0] for i in range(n + 1)]
    m = VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)
    return DashedVMobject(m, num_dashes=40) if dashed else m


# The original cards are intentionally retained, as requested in TASK.md.
class S00Title(TitleCard):
    LESSON = "Sensitive periods in behavior"
    TITLE = "When Experience Arrives"


def heading(text):
    return T(text, 34, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])


def link(a, b, color=GREY):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=4, tip_length=0.18)


def window_inputs():
    """Shared position for the genes/experience/window motif."""
    g = chip("genes", GREY, 28).move_to([-4.4, 1.5, 0])
    e = chip("prior experience", YELLOW, 28).move_to([-4.4, -0.4, 0])
    ax = axes(-1.6, -1.3, 6.8, 3.5)
    win = curve_mob(-1.6, -1.3, 6.8, 3.5, lambda t: bell(t, 0.4, 0.23))
    labels = VGroup(T("learning window", 26, TEAL).move_to([1.8, 2.65, 0]),
                    T("developmental age", 24, GREY).move_to([1.8, -1.8, 0]))
    arrows = VGroup(link(g.get_right(), [-1.7, 1.2, 0]),
                    link(e.get_right(), [-1.7, -0.4, 0], YELLOW))
    return g, e, ax, win, labels, arrows


class S01Sparrow(SpokenScene):
    def construct(self):
        chamber = RoundedRectangle(corner_radius=0.25, width=4.4, height=3.1,
                                   stroke_color=GREY, stroke_width=3).move_to([-3.8, -0.15, 0])
        b = bird().move_to(chamber.get_center() + DOWN * 0.1)
        label = T("without adult song", 26, GREY).next_to(chamber, DOWN, buff=0.25)
        adult = wave(-5.8, 2.5, 3.9, rich, YELLOW, 0.3)
        blocked = cross([-3.8, 1.7, 0], RED, 0.22)
        self.at("A young male")
        self.play(Create(chamber), FadeIn(b), FadeIn(label), run_time=0.8)
        self.at("never hears")
        self.play(Create(adult), Create(blocked), run_time=0.7)
        mine = VGroup(T("simple, abnormal song", 26, RED).move_to([3.2, 0.6, 0]),
                      wave(0.9, -0.1, 4.6, simple, RED, 0.35, 5))
        wild = VGroup(T("wild song", 26, GREEN).move_to([3.2, 2.5, 0]),
                      wave(0.9, 1.7, 4.6, rich, GREEN, 0.35, 5))
        self.at("As an adult")
        self.play(FadeIn(mine), FadeIn(wild), run_time=0.9)
        late = T("late tutoring", 26, YELLOW).move_to([-3.8, 3.15, 0])
        incoming = link([-3.8, 2.1, 0], [-3.8, 0.8, 0], YELLOW)
        self.at("Hearing the right song later")
        self.play(FadeOut(blocked), FadeIn(late), GrowArrow(incoming), run_time=0.7)
        little = T("little change", 26, RED).move_to([3.2, -1.1, 0])
        self.at("does little")
        self.play(FadeIn(little), Indicate(mine[1], scale_factor=1.03), run_time=0.6)

        self.at("The same experience")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        h = heading("Same input, different timing")
        timelines = VGroup()
        for y, name, x in [(1.2, "earlier", -2.4), (-1.0, "later", 1.5)]:
            row = VGroup(T(name, 26, GREY).move_to([-5.5, y, 0]),
                         link([-4.4, y, 0], [3.8, y, 0]),
                         Dot([x, y, 0], radius=0.15, color=YELLOW))
            timelines.add(row)
        outcomes = VGroup(T("lasting effect", 26, GREEN).move_to([4.7, 1.8, 0]),
                          T("little effect", 26, GREY).move_to([4.7, -0.4, 0]))
        self.play(FadeIn(h), Create(timelines), run_time=0.7)
        self.at("lasting effect")
        self.play(FadeIn(outcomes[0]), run_time=0.4)
        self.at("little effect at another")
        self.play(FadeIn(outcomes[1]), run_time=0.4)
        self.at("Genes and experience")
        self.play(FadeOut(VGroup(h, timelines, outcomes)), run_time=0.35)
        g, e, ax, win, labels, arrows = window_inputs()
        self.play(FadeIn(g), FadeIn(e), Create(ax), Create(win), FadeIn(labels), Create(arrows), run_time=0.9)
        self.play(Indicate(g, color=TEXT, scale_factor=1.05),
                  Indicate(arrows[0], color=TEXT, scale_factor=1.05), run_time=0.6)
        self.at("experience can even")
        self.play(Indicate(e, color=YELLOW, scale_factor=1.05),
                  Indicate(arrows[1], color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("help close the window")
        narrower = curve_mob(-1.6, -1.3, 6.8, 3.5, lambda t: bell(t, 0.32, 0.16))
        self.play(Transform(win, narrower), Indicate(e, scale_factor=1.05), run_time=0.8)
        q = T("When does input arrive, and what lasts?", 32, TEXT, font=TITLE_FONT).move_to([0, -2.9, 0])
        self.at("Timing matters")
        self.play(FadeIn(q), run_time=0.7)
        cases = VGroup(*[chip(name, BLUE, 24).move_to([3.8, y, 0])
                         for name, y in [("song", 1.65), ("sight", 0.65), ("language", -0.35)]])
        self.at("song and sight")
        self.play(FadeIn(cases[0]), run_time=0.4)
        self.at("sight")
        self.play(FadeIn(cases[1]), run_time=0.4)
        self.at("late language access")
        self.play(FadeIn(cases[2]), run_time=0.6)
        self.finish()


class S02Window(SpokenScene):
    def construct(self):
        g, e, ax, win, labels, arrows = window_inputs()
        self.at("Genes build the circuit")
        self.play(FadeIn(g), Create(ax), Create(win), FadeIn(labels), GrowArrow(arrows[0]), run_time=0.8)
        self.at("Experience supplies")
        self.play(FadeIn(e), GrowArrow(arrows[1]), run_time=0.7)
        self.at("In zebra finches")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        h = heading("Zebra finches: same later age")
        rows = VGroup()
        for y, name in [(1.3, "raised without a tutor"), (-1.3, "raised with a tutor")]:
            rows.add(VGroup(T(name, 26, BLUE).move_to([-3.7, y + 0.7, 0]),
                            bird(0.55).move_to([-5.1, y - 0.35, 0]),
                            link([-3.9, y - 0.35, 0], [2.2, y - 0.35, 0]),
                            Line([1.2, y - 0.65, 0], [1.2, y - 0.05, 0], color=YELLOW, stroke_width=4)))
        tutor = VGroup(T("new tutor", 26, YELLOW).move_to([1.2, 2.0, 0]),
                       wave(0.2, 2.65, 2, rich, YELLOW, 0.22))
        same_age = DashedLine([1.2, -2.25, 0], [1.2, 1.3, 0], color=GREY)
        self.play(FadeIn(h), FadeIn(rows), FadeIn(tutor), Create(same_age), run_time=0.8)
        copied = VGroup(wave(2.8, 0.95, 2.9, rich, GREEN, 0.26),
                        T("copies new song", 24, GREEN).move_to([4.25, 1.75, 0]))
        ignored = VGroup(wave(2.8, -1.65, 2.9, lambda t: rich(t + 0.7), BLUE, 0.26),
                        T("no new copy", 24, GREY).move_to([4.25, -0.85, 0]))
        self.at("can still copy new song")
        self.play(TransformFromCopy(tutor[1], copied[0]), FadeIn(copied[1]), run_time=0.8)
        self.at("have stopped")
        self.play(FadeIn(ignored), run_time=0.6)
        note = T("Prior tutoring helps close the window", 28, TEAL).move_to([0, -2.8, 0])
        self.at("That suggests")
        self.play(FadeIn(note), Indicate(rows[1][0], scale_factor=1.03), run_time=0.8)
        self.at("Age alone")
        self.play(Indicate(same_age, color=YELLOW, scale_factor=1.02), run_time=0.6)
        self.finish()


class S03Song(SpokenScene):
    def construct(self):
        h = heading("Listen, remember, then practice")
        timeline = link([-5.8, 1.9, 0], [5.8, 1.9, 0])
        listen = VGroup(Rectangle(width=3.4, height=0.5, color=YELLOW, fill_opacity=0.2).move_to([-3.8, 2.25, 0]),
                        T("listening", 26, YELLOW).move_to([-3.8, 2.85, 0]))
        practice_bar = VGroup(Rectangle(width=3.4, height=0.5, color=BLUE, fill_opacity=0.2).move_to([3.8, 2.25, 0]),
                              T("practice", 26, BLUE).move_to([3.8, 2.85, 0]))
        self.at("What happens inside")
        self.play(FadeIn(h), run_time=0.6)
        self.at("two phases")
        self.play(FadeOut(h), GrowArrow(timeline), FadeIn(listen), FadeIn(practice_bar), run_time=0.7)
        tutor = wave(-5.8, 0.6, 3.5, rich, YELLOW, 0.35, 5)
        b = bird(0.85).move_to([3.9, 0.3, 0])
        self.at("A young bird listens")
        self.play(Create(tutor), FadeIn(b), run_time=0.7)
        memory = VGroup(chip("tutor memory", PURPLE, 26).move_to([-4.0, -0.8, 0]),
                        wave(-1.7, -0.8, 3.4, rich, PURPLE, 0.3, 5))
        self.at("memorizes the song")
        self.play(FadeOut(tutor), FadeIn(memory[0]), TransformFromCopy(tutor, memory[1]), run_time=0.7)
        own = VGroup(T("own voice", 26, BLUE).move_to([-4.0, -2.3, 0]),
                     wave(-1.7, -2.3, 3.4, rambling, BLUE, 0.3, 5))
        feedback = CurvedArrow([2.1, -2.3, 0], [2.1, -0.8, 0], angle=PI / 2, color=BLUE)
        fb_label = T("hear → compare", 24, BLUE).move_to([4.3, -1.5, 0])
        feedback_group = VGroup(feedback, fb_label)
        self.at("Then it practices")
        self.play(FadeIn(own), Create(feedback_group), run_time=0.8)
        self.at("to match the memory")
        self.play(Transform(own[1], wave(-1.7, -2.3, 3.4, rich, BLUE, 0.3, 5)), run_time=0.9)
        gap = VGroup(DoubleArrow([-1.9, 2.25, 0], [1.9, 2.25, 0], buff=0, color=GREY),
                     T("months apart", 24, GREY).move_to([0, 2.85, 0]))
        self.at("months apart")
        self.play(FadeIn(gap), run_time=0.6)
        deaf = chip("deafened between phases", RED, 24).move_to([0, 0.65, 0])
        self.at("deafened between them")
        self.play(FadeOut(b), FadeIn(deaf), feedback_group.animate.set_opacity(0.2), run_time=0.7)
        self.at("very poor song")
        self.play(Transform(own[1], wave(-1.7, -2.3, 3.4, simple, RED, 0.3, 5)),
                  Transform(own[0], T("very poor song", 26, RED).move_to(own[0])), run_time=0.8)
        need = T("Auditory feedback is needed", 28, BLUE).move_to([0, -3.2, 0])
        self.at("hear itself")
        self.play(FadeIn(need), Indicate(feedback, color=BLUE, scale_factor=1.08), run_time=0.7)

        self.at("The brain has a motor pathway")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        motor_title = heading("Song: motor pathway")
        nodes = [chip(n, BLUE, 26).move_to([x, 1.35, 0]) for n, x in
                 [("HVC", -5.0), ("RA", -1.8), ("brainstem", 1.6), ("syrinx", 5.0)]]
        motor = VGroup(*[link(a.get_right(), b.get_left(), BLUE) for a, b in zip(nodes, nodes[1:])])
        self.play(FadeIn(motor_title), FadeIn(VGroup(*nodes)), Create(motor), run_time=0.9)
        learning_nodes = [chip(n, TEAL, 24).move_to([x, -1.25, 0]) for n, x in
                          [("area X", -5.0), ("thalamus", -1.8), ("LMAN", 1.6)]]
        learning_arrows = VGroup(link(nodes[0].get_bottom(), learning_nodes[0].get_top(), TEAL),
                                 link(learning_nodes[0].get_right(), learning_nodes[1].get_left(), TEAL),
                                 link(learning_nodes[1].get_right(), learning_nodes[2].get_left(), TEAL))
        # Return to RA through a separate lane, clear of the motor chain.
        ret = VMobject(color=TEAL, stroke_width=4).set_points_as_corners([
            learning_nodes[2].get_top(), [1.6, 0.15, 0], [-1.8, 0.15, 0]])
        learning_arrows.add(ret, link([-1.8, 0.15, 0], nodes[1].get_bottom(), TEAL))
        learning_label = T("learning pathway", 28, TEAL).move_to([0, -2.65, 0])
        self.at("Another pathway")
        self.play(FadeIn(VGroup(*learning_nodes)), Create(learning_arrows), FadeIn(learning_label), run_time=1.0)
        self.at("matters while song is learned")
        self.play(Indicate(VGroup(*learning_nodes), scale_factor=1.04), run_time=0.8)
        self.finish()


class S05Sight(SpokenScene):
    def construct(self):
        h = heading("Different abilities, different windows")
        self.at("has different windows")
        self.play(FadeIn(h), run_time=0.6)
        # Reuse the original lens, retina, diffuse light and grating drawing.
        ec = np.array([-3.2, 0.4, 0])
        eye = Circle(radius=1.55, stroke_color=GREY, stroke_width=4).move_to(ec)
        retina = Arc(radius=1.55, start_angle=-PI/3, angle=2*PI/3, color=GREY,
                     stroke_width=10).move_arc_center_to(ec)
        lens = Ellipse(width=0.45, height=1.8, stroke_color=GREY, stroke_width=4,
                       fill_color=GREY, fill_opacity=0.85).move_to(ec + LEFT*0.85)
        rays = VGroup(*[link([-6.0, ec[1]+dy, 0], lens.get_left()+[0, dy*0.55, 0], YELLOW)
                        for dy in (-0.6, 0, 0.6)])
        glow = Ellipse(width=0.9, height=2.1, stroke_width=0, fill_color=YELLOW,
                       fill_opacity=0.28).move_to(ec + RIGHT*0.85)
        lens_label = T("cloudy lens: diffuse light", 24, GREY).move_to([-3.2, -1.8, 0])
        eye_group = VGroup(eye, retina, lens, rays, glow, lens_label)
        self.at("dense cataracts")
        self.play(FadeIn(eye_group), run_time=0.8)
        plot = VGroup(axes(0.5, -1.0, 5.3, 2.9),
                      T("acuity", 24, GREY).move_to([1.2, 2.2, 0]),
                      T("time after treatment", 24, GREY).move_to([3.1, -1.6, 0]))
        baseline = VGroup(DashedLine([0.5, -0.45, 0], [5.8, -0.45, 0], color=GREY),
                          T("newborn level", 24, GREY).move_to([4.45, -0.8, 0]))
        start = Dot([0.5, -0.45, 0], radius=0.12, color=TEAL)
        bars = VGroup(*[Rectangle(width=0.12, height=1.5, stroke_width=0, fill_color=YELLOW,
                                 fill_opacity=0.95).move_to(ec+[0.7+i*0.26, 0, 0]) for i in range(3)])
        self.at("Right after treatment")
        self.play(lens.animate.set_fill(opacity=0), FadeOut(glow), FadeIn(bars),
                  Transform(lens_label, T("pattern reaches the retina", 24, YELLOW).move_to(lens_label)),
                  FadeIn(plot), FadeIn(baseline), FadeIn(start), run_time=0.9)
        def acuity(a, b):
            return VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners([
                [0.5+5.3*t, -0.45+2.0*(1-np.exp(-3*t)), 0] for t in np.linspace(a, b, 50)])
        c1, c2 = acuity(0, 0.14), acuity(0.14, 1)
        hour = T("as little as an hour", 24, TEAL).move_to([3.0, -2.3, 0])
        self.at("as little as an hour")
        self.play(Create(c1), FadeIn(hour), run_time=0.7)
        self.at("Patterned input drives improvement")
        self.play(Create(c2), run_time=0.9)
        self.at("Yet fine acuity")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        h2 = heading("Improvement and lasting deficits")
        fine = VGroup(T("fine acuity", 28, RED).move_to([-3.7, 1.2, 0]),
                      Line([-1.4, 1.2, 0], [3.8, 1.2, 0], color=RED, stroke_width=5),
                      T("deficit persists", 24, RED).move_to([4.9, 1.8, 0]))
        face = VGroup(T("facial-feature\nspacing", 28, RED).move_to([-3.7, -0.3, 0]),
                      Line([-1.4, -0.3, 0], [3.8, -0.3, 0], color=RED, stroke_width=5),
                      T("deficit persists", 24, RED).move_to([4.9, -0.9, 0]))
        self.play(FadeIn(h2), FadeIn(fine), run_time=0.7)
        self.at("spacing of facial features")
        self.play(FadeIn(face), run_time=0.7)
        # Distinct schematic windows; not measured ages or durations.
        early = VGroup(T("early input", 24, YELLOW).move_to([-4.8, -2.35, 0]),
                       Rectangle(width=1.7, height=0.35, color=YELLOW, fill_opacity=0.3).move_to([-2.7, -2.35, 0]),
                       link([-1.65, -2.35, 0], [1.4, -2.35, 0]),
                       T("ability appears later", 24, BLUE).move_to([3.6, -2.35, 0]))
        self.at("Early input can matter")
        self.play(FadeIn(early), run_time=0.8)
        windows = VGroup(curve_mob(-1.4, 0.85, 5.2, 0.65, lambda t: bell(t, 0.25, 0.18), TEAL, sw=3),
                         curve_mob(-1.4, -0.65, 5.2, 0.65, lambda t: bell(t, 0.55, 0.27), TEAL, sw=3))
        self.at("Improvement and lasting loss")
        self.play(FadeOut(fine[1]), FadeOut(face[1]), Create(windows),
                  Transform(h2, heading("Function-specific windows (schematic)")),
                  FadeIn(T("developmental age →", 24, GREY).move_to([1.2, -1.4, 0])), run_time=0.8)
        self.finish()


class S04FirstLanguage(SpokenScene):
    def construct(self):
        h = heading("Access to a first language")
        self.at("For language")
        self.play(FadeIn(h), run_time=0.6)
        rows = VGroup()
        # Care and contact remain explicitly present throughout both comparisons.
        for y, name, x in [(1.2, "early access", -1.8), (-1.35, "delayed access", 0.9)]:
            row = VGroup(T(name, 28, BLUE).move_to([-4.8, y+0.65, 0]),
                         link([-5.9, y, 0], [5.9, y, 0]),
                         chip("signed language", YELLOW, 24).move_to([x, y+0.65, 0]),
                         T("care + social contact", 24, GREY).move_to([-3.9, y-0.55, 0]),
                         Line([x, y-0.2, 0], [x, y+0.2, 0], color=YELLOW, stroke_width=5))
            rows.add(row)
        self.at("access to a first language")
        self.play(FadeIn(rows[0]), run_time=0.7)
        self.at("Some deaf children")
        self.play(FadeIn(rows[1]), run_time=0.7)
        outcomes = VGroup(T("later proficiency", 24, TEXT).move_to([4.4, 2.0, 0]),
                          T("affected proficiency", 24, RED).move_to([4.3, -0.55, 0]))
        self.at("Delayed access affects later proficiency")
        self.play(FadeIn(outcomes), run_time=0.8)
        self.at("care and social contact")
        self.play(Indicate(rows[0][3], color=TEXT, scale_factor=1.05),
                  Indicate(rows[1][3], color=TEXT, scale_factor=1.05), run_time=0.7)
        self.finish()


class S04Language(SpokenScene):
    def construct(self):
        h = heading("Second-language grammar study")
        known = chip("first language already learned", BLUE, 28).move_to([0, 0.5, 0])
        self.at("Learning a second language")
        self.play(FadeIn(h), run_time=0.7)
        self.at("already know a first language")
        self.play(FadeIn(known), run_time=0.7)
        plot = VGroup(axes(-5.5, -1.8, 11, 3.7),
                      T("English grammar score", 24, GREY).move_to([-3.7, 2.3, 0]),
                      T("age of arrival", 24, GREY).move_to([0, -2.4, 0]),
                      T("qualitative illustration", 22, GREY).move_to([4.1, 2.3, 0]))
        self.at("Researchers compared")
        self.play(FadeOut(known), FadeIn(plot), run_time=0.8)
        native = VGroup(DashedLine([-5.5, 1.55, 0], [5.5, 1.55, 0], color=GREEN),
                        T("native speakers", 24, GREEN).move_to([4.2, 1.9, 0]))
        # Small clusters represent the qualitative pattern, not individual study data.
        young = VGroup(*[Dot([x, 1.55+dy, 0], radius=0.1, color=GREEN)
                         for x, dy in [(-5.1, 0), (-4.55, .07), (-3.95, -.06)]])
        middle = VGroup(*[Dot([x, 1.5-0.42*(x+3.7), 0], radius=0.1, color=TEAL)
                          for x in [-3.35, -2.7, -2.0, -1.25, -.5]])
        late = VGroup(*[Dot([x, y, 0], radius=0.1, color=TEAL) for x, y in
                        [(0.5, -.45), (1.2, .2), (1.9, -1.05), (2.6, -.1), (3.3, -.9), (4.0, .35), (4.8, -.6)]])
        self.at("The youngest arrivals")
        self.play(FadeIn(native), FadeIn(young), run_time=0.8)
        puberty = T("about puberty", 24, GREY).move_to([-0.2, -1.45, 0])
        self.at("Scores fell with age")
        self.play(FadeIn(middle), FadeIn(puberty), run_time=0.9)
        self.at("Later arrivals")
        self.play(FadeIn(late), run_time=0.8)
        self.at("The age effect is clear")
        self.play(Indicate(VGroup(young, middle, late), scale_factor=1.02), run_time=0.7)
        self.at("Its cause remains debated")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not h], run_time=0.35)
        q = T("What explains the age effect?", 32, TEXT).move_to([0, 1.9, 0])
        self.play(FadeIn(q), run_time=0.5)
        explanations = [chip("changes in plasticity", TEAL, 28).move_to([0, .6, 0]),
                        chip("established first language", BLUE, 28).move_to([0, -.7, 0]),
                        chip("differences in input", YELLOW, 28).move_to([0, -2.0, 0])]
        self.at("changes in plasticity")
        self.play(FadeIn(explanations[0]), run_time=0.5)
        self.at("established first language")
        self.play(FadeIn(explanations[1]), run_time=0.5)
        self.at("differences in input")
        self.play(FadeIn(explanations[2]), run_time=0.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        # One object per case row, with columns aligned across cases.
        headers = VGroup(*[T(s, 26, TEXT).move_to([x, 2.7, 0]) for s, x in
                           [("input", -3.2), ("timing", 0), ("lasting outcome", 4.0)]])
        rows = VGroup()
        for name, inp, out, y in [("song", "tutor song", "adult song", 1.4),
                                  ("sight", "patterned light", "visual abilities", 0),
                                  ("language", "accessible language", "proficiency", -1.4)]:
            rows.add(VGroup(T(name, 24, BLUE).move_to([-5.8, y, 0]),
                            T(inp, 24, YELLOW).move_to([-3.2, y, 0]),
                            link([-1.2, y, 0], [1.5, y, 0], TEAL),
                            Dot([-.5, y, 0], color=YELLOW, radius=.11),
                            T(out, 24, TEXT).move_to([4.0, y, 0])))
        self.at("Across these cases")
        self.play(FadeIn(headers), FadeIn(rows), run_time=0.7)
        self.at("what input arrives")
        self.play(Indicate(headers[0], color=YELLOW, scale_factor=1.05), run_time=0.4)
        self.at("at what age")
        self.play(Indicate(headers[1], color=TEAL, scale_factor=1.05), run_time=0.4)
        self.at("what lasts")
        self.play(Indicate(headers[2], scale_factor=1.05), run_time=0.4)
        self.at("Experience shapes learning")
        self.play(FadeOut(VGroup(headers, rows)), run_time=0.3)
        title = heading("Zebra finches: experience changes timing")
        raised = VGroup(T("prior tutor", 26, YELLOW).move_to([-4, 1.3, 0]),
                        link([-2.4, 1.3, 0], [1.4, 1.3, 0], TEAL),
                        T("no new copy", 26, GREY).move_to([3.8, 1.3, 0]))
        isolated = VGroup(T("no prior tutor", 26, GREY).move_to([-4, -.3, 0]),
                          link([-2.4, -.3, 0], [1.4, -.3, 0], TEAL),
                          T("copies new tutor", 26, GREEN).move_to([3.8, -.3, 0]))
        same = T("same later age", 24, GREY).move_to([-.5, -1.3, 0])
        rule = T("Experience shapes learning and its timing", 32, TEXT, font=TITLE_FONT).move_to([0, -2.7, 0])
        self.play(FadeIn(title), FadeIn(raised), FadeIn(isolated), FadeIn(same), run_time=0.7)
        self.at("help shape the window itself")
        self.play(FadeIn(rule), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what input arrives, at what age, and what lasts."
