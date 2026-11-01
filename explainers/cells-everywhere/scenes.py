"""Cells are everywhere: too small to see, still alive  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = cells and tiny living things
  TEAL   = microscopes and their lenses
  ORANGE = size limits (the eye's limit, the light microscope's limit)
  YELLOW = vocabulary words as they are defined
  GREEN  = results, totals, the cell theory, the answer
  RED    = the crossed-out "guess"
  GREY   = outlines, axes, neutral structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def vocab(text, size=36):
    return T(text, size, YELLOW, weight=BOLD)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell_shape(w=1.2, h=0.8, x=0, y=0, color=BLUE, op=0.18):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def wander(mob, base, ax, ay, w1, w2, p, clock):
    base = np.array(base, float)
    mob.add_updater(lambda m, dt: m.move_to(base + np.array([ax * np.sin(w1 * clock() + p), ay * np.cos(w2 * clock() + 1.7 * p), 0])))


# Drawing helpers retain the old film's outlined cells, lenses and theory cards.
def person(x=0, y=0):
    head = Circle(0.28, color=GREY, stroke_width=4).shift(UP * 1.2)
    body = RoundedRectangle(width=0.72, height=1.15, corner_radius=0.15,
                            color=GREY, stroke_width=4).shift(UP * 0.25)
    limbs = VGroup(Line([-0.3, 0.65, 0], [-0.8, -0.1, 0], color=GREY),
                   Line([0.3, 0.65, 0], [0.8, -0.1, 0], color=GREY),
                   Line([-0.2, -0.3, 0], [-0.5, -1.1, 0], color=GREY),
                   Line([0.2, -0.3, 0], [0.5, -1.1, 0], color=GREY))
    return VGroup(head, body, limbs).move_to([x, y, 0])


def oak(x=0, y=0):
    trunk = Rectangle(width=0.35, height=1.5, color=GREY, stroke_width=4).shift(DOWN * 0.55)
    crown = VGroup(*[Circle(0.65, color=GREY, fill_color=GREY, fill_opacity=0.08)
                     .move_to([dx, dy, 0]) for dx, dy in [(-0.45, 0.45), (0.45, 0.45), (0, 1)]])
    return VGroup(trunk, crown).move_to([x, y, 0])


def tiles(cols=2, rows=2, w=0.42, h=0.35):
    return VGroup(*[RoundedRectangle(width=w, height=h, corner_radius=0.06,
                    stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.2)
                   for _ in range(cols * rows)]).arrange_in_grid(rows, cols, buff=0.04)


def card_state(card, on, dur=0.4):
    box, n, lab = card
    return [box.animate.set_fill(GREEN, 0.35 if on else 0.08).set_stroke(GREEN, opacity=1 if on else 0.4),
            n.animate.set_opacity(1 if on else 0.4), lab.animate.set_opacity(1 if on else 0.45)]


def theory_cards():
    texts = ["All living things are made of\none or more cells",
             "The cell is the basic\nunit of life",
             "All cells come from cells\nthat already exist"]
    cards = VGroup()
    for i, text in enumerate(texts):
        box = RoundedRectangle(corner_radius=0.14, width=6.4, height=1.5,
                               stroke_color=GREEN, stroke_width=3,
                               fill_color=GREEN, fill_opacity=0.12)
        n = T(str(i + 1), 40, GREEN, weight=BOLD).move_to(box.get_left() + RIGHT * 0.5)
        lab = T(text, 27, TEXT).move_to(box.get_left() + RIGHT * (1 + T(text, 27).width / 2))
        cards.add(VGroup(box, n, lab))
    return cards.arrange(DOWN, buff=0.35).move_to([-3.2, -0.35, 0])


def daughters(x=3.65, y=0.5):
    return VGroup(cell_shape(1.25, 1.15, x - 0.8, y),
                  cell_shape(1.25, 1.15, x + 0.8, y))


class S00Title(TitleCard):
    LESSON = "Cells are everywhere"
    TITLE = "Too Small to See, Still Alive"


class S01Drop(SpokenScene):
    def construct(self):
        drop = Circle(radius=1.4, stroke_color=GREY, stroke_width=4,
                      fill_color=GREY, fill_opacity=0.06).move_to([-4.4, 0.25, 0])
        label = T("pond-water drop", 28).move_to([-4.4, -2, 0])
        clear = T("looks clear", 30, GREY).move_to([-4.4, 2.4, 0])
        self.at("A drop of pond water")
        self.play(FadeIn(drop), FadeIn(label), run_time=0.55)
        self.at("completely clear")
        self.play(FadeIn(clear), run_time=0.45)

        view = Circle(radius=1.65, stroke_color=TEAL, stroke_width=5,
                      fill_color=TEAL, fill_opacity=0.05).move_to(drop)
        mic = T("microscope view", 28, TEAL).move_to(clear)
        blobs = VGroup(cell_shape(0.9, 0.5, -4.9, 0.9),
                       cell_shape(0.7, 0.48, -3.7, 0.4), cell_shape(0.85, 0.55, -4.6, -0.5))
        self.at("tiny living things")
        self.play(Transform(drop, view), ReplacementTransform(clear, mic), FadeIn(blobs), run_time=0.6)

        onion = VGroup(cell_shape(1.9, 2.2, 0, 0.25, color=GREY),
                       Line([0, 1.3, 0], [0.15, 1.85, 0], color=GREY, stroke_width=4),
                       T("onion", 28).move_to([0, -2, 0]))
        human = VGroup(person(4.4, 0.3), T("you", 28).move_to([4.4, -2, 0]))
        self.at("an onion")
        self.play(FadeIn(onion), run_time=0.4)
        self.at("and you")
        self.play(FadeIn(human), run_time=0.3)
        patches = VGroup(tiles(2, 3).move_to([0, 0.25, 0]),
                         tiles(2, 2, 0.24, 0.28).move_to([4.4, 0.55, 0]))
        self.at("all made of cells")
        self.play(FadeIn(patches), *[Indicate(b, color=BLUE, scale_factor=1.1) for b in blobs], run_time=0.55)
        self.finish()


class S05Theory(SpokenScene):
    def construct(self):
        cell = cell_shape(4.0, 2.7, 0, 0.5)
        label = T("smallest unit\nof life", 32, BLUE).move_to([0, -1.7, 0])
        self.at("A cell is")
        self.play(FadeIn(cell), run_time=0.5)
        self.at("smallest unit")
        self.play(FadeIn(label), run_time=0.5)
        head = vocab("cell theory", 40).move_to([0, 3.15, 0])
        self.at("The cell theory")
        self.play(FadeIn(head), cell.animate.scale(0.7).move_to([3.65, 0.5, 0]),
                  label.animate.move_to([3.65, -1.3, 0]), run_time=0.65)
        cards = theory_cards()
        self.at("All living things")
        self.play(FadeIn(cards[0]), Indicate(cell, color=BLUE), run_time=0.6)
        self.at("The cell is the basic")
        self.play(FadeIn(cards[1]), run_time=0.6)
        self.at("All cells come")
        existing = T("an existing cell", 30, BLUE).move_to([3.65, -1.3, 0])
        self.play(FadeIn(cards[2]), ReplacementTransform(label, existing), run_time=0.45)
        self.at("cells that already exist")
        # The original cell deforms into two; new cells do not appear from empty space.
        pair = daughters()
        pinch = VGroup(cell_shape(1.55, 1.5, 3.05, 0.5), cell_shape(1.55, 1.5, 4.25, 0.5))
        self.play(ReplacementTransform(cell, pinch), run_time=0.45)
        self.play(Transform(pinch, pair), ReplacementTransform(existing,
                  T("new cells", 30, BLUE).move_to(existing)), run_time=0.55)
        self.finish()


class S05Organisms(SpokenScene):
    def construct(self):
        para = cell_shape(1.85, 3.15, 0, 0.25).rotate(-0.25)
        self.at("Some organisms")
        self.play(FadeIn(para), run_time=0.6)
        uni = vocab("unicellular", 32).move_to([0, 2.65, 0])
        self.at("They are unicellular")
        self.play(FadeIn(uni), run_time=0.5)
        pl = T("Paramecium\none cell", 28, BLUE).move_to([0, -2.1, 0])
        self.at("A paramecium")
        self.play(FadeIn(pl), Indicate(para, color=BLUE), run_time=0.6)
        human = VGroup(person(0, 0.25), T("you", 28).move_to([0, -2, 0]))
        tree = VGroup(oak(4.2, 0.25), T("oak tree", 28).move_to([4.2, -2, 0]))
        multi = vocab("multicellular", 32).move_to([2.1, 2.65, 0])
        self.at("You and an oak tree")
        self.play(para.animate.scale(0.76).move_to([-4.4, 0.25, 0]),
                  uni.animate.move_to([-4.4, 2.65, 0]), pl.animate.move_to([-4.4, -2, 0]),
                  FadeIn(human), FadeIn(tree), run_time=0.6)
        self.at("are multicellular")
        self.play(FadeIn(multi), run_time=0.5)
        patches = VGroup(tiles(2, 2, 0.24, 0.28).move_to([0, 0.5, 0]),
                         tiles(3, 2, 0.35, 0.35).move_to([4.2, 0.75, 0]))
        self.at("made of many cells")
        self.play(FadeIn(patches), run_time=0.5)

        small = cell_shape(0.35, 0.2, -3.8, 0)
        pond_label = T("tiny pond animal", 28, BLUE).move_to([-3.8, -1.3, 0])
        question = T("Tiny does not always mean one cell", 32).move_to([0, 2.8, 0])
        self.at("Tiny does not always")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(small),
                  FadeIn(pond_label), FadeIn(question), run_time=0.55)
        animal = VGroup(cell_shape(3.1, 1.9, 2.5, 0), tiles(4, 2, 0.48, 0.52).move_to([2.5, 0, 0]))
        link = arr([-3.3, 0, 0], [0.7, 0, 0], TEAL)
        enlarged = T("enlarged: many cells", 28, BLUE).move_to([2.5, -1.6, 0])
        self.at("Some tiny pond animals")
        self.play(GrowArrow(link), TransformFromCopy(small, animal), FadeIn(enlarged), run_time=0.75)
        self.finish()


class S06Answer(SpokenScene):
    def construct(self):
        th = vocab("theory", 44).move_to([0, 2.65, 0])
        definition = T("a well-tested explanation\nbacked by a great deal of evidence", 34).move_to([0, 0.6, 0])
        self.at("In science")
        self.play(FadeIn(th), run_time=0.5)
        self.at("a well")
        self.play(FadeIn(definition), run_time=0.6)

        scope = chip("better microscopes", TEAL, size=28).move_to([-4.2, 1.9, 0])
        obs = chip("observations", GREEN, size=28).move_to([0.1, 1.9, 0])
        theory = chip("cell theory", GREEN, size=30).move_to([4.4, 1.9, 0])
        links = VGroup(arr(scope.get_right(), obs.get_left(), TEAL), arr(obs.get_right(), theory.get_left(), GREEN))
        self.at("The cell theory grew")
        self.play(FadeOut(th), FadeOut(definition), FadeIn(theory), run_time=0.55)
        self.at("better microscopes")
        self.play(FadeIn(scope), run_time=0.5)
        self.at("gave new evidence")
        self.play(FadeIn(obs), *[GrowArrow(a) for a in links], run_time=0.6)
        plants = VGroup(tiles(3, 2, 0.6, 0.55).move_to([-3.5, -0.5, 0]),
                        T("plant cells", 28, BLUE).move_to([-3.5, -1.7, 0]))
        animals = VGroup(VGroup(*[cell_shape(0.8, 0.55) for _ in range(4)])
                         .arrange_in_grid(2, 2, buff=0.15).move_to([0, -0.5, 0]),
                         T("animal cells", 28, BLUE).move_to([0, -1.7, 0]))
        observed = arr([-1.7, -0.4, 0], [0.1, 1.3, 0], GREEN)
        self.at("Scientists found cells")
        self.play(FadeIn(plants), FadeIn(animals), GrowArrow(observed), run_time=0.7)

        old = VGroup(T("old idea", 28, RED).move_to([-3.4, 0, 0]),
                     T("clear fluid → new cells", 28, GREY).move_to([-3.4, -0.8, 0]))
        self.at("thought new cells")
        self.play(FadeOut(plants), FadeOut(animals), FadeOut(observed), FadeIn(old), run_time=0.55)
        cell = cell_shape(2.2, 1.5, 3.65, -0.75)
        existing = T("an existing cell", 28, BLUE).move_to([3.65, -2.1, 0])
        cross = VGroup(Line([-6.05, -1.1, 0], [-0.75, -0.5, 0], color=RED, stroke_width=6),
                       Line([-6.05, -0.5, 0], [-0.75, -1.1, 0], color=RED, stroke_width=6))
        self.at("More observations")
        self.play(Create(cross), FadeIn(cell), FadeIn(existing), run_time=0.6)
        self.at("when a cell divides")
        pair = daughters(3.65, -0.75)
        self.play(ReplacementTransform(cell, pair), ReplacementTransform(existing,
                  T("new cells", 28, BLUE).move_to(existing)), run_time=0.8)
        statements = ["All living things\nare made of one\nor more cells",
                      "The cell is the\nbasic unit of life",
                      "All cells come from\ncells that already\nexist"]
        cards = VGroup()
        for x, statement in zip([-4.35, 0, 4.35], statements):
            box = RoundedRectangle(width=4.05, height=2.05, corner_radius=0.14,
                                   color=GREEN, fill_color=GREEN, fill_opacity=0.12)
            cards.add(VGroup(box, T(statement, 25).move_to(box)).move_to([x, 0.9, 0]))
        evidence = T("supported by observations", 32, GREEN).move_to([0, -2.3, 0])
        arrows = VGroup(*[arr([x, -1.75, 0], [x, -0.25, 0], GREEN) for x in [-4.35, 0, 4.35]])
        self.at("The theory dropped")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(cards), run_time=0.55)
        self.at("and kept the rest")
        self.play(FadeIn(evidence), *[GrowArrow(a) for a in arrows], run_time=0.6)
        self.finish()


class S02Limit(SpokenScene):
    def construct(self):
        head = T("Most cells need help to be seen", 36).move_to([0, 2.8, 0])
        cells = VGroup(cell_shape(0.9, 0.6, -4.6, 0.8), cell_shape(0.6, 0.4, -2.8, 0.8),
                       cell_shape(0.8, 0.52, -1, 0.8))
        axis = arr([-5.8, -0.25, 0], [5.8, -0.25, 0], GREY)
        smaller = T("smaller details", 28, BLUE).move_to([-3, -1.25, 0])
        note = T("schematic • not to scale", 22, GREY).move_to([0, -2.8, 0])
        self.at("Most cells")
        self.play(FadeIn(head), FadeIn(cells), GrowArrow(axis), FadeIn(smaller), FadeIn(note), run_time=0.7)
        eye = Line([2, -0.5, 0], [2, 1.8, 0], color=ORANGE, stroke_width=5)
        limit = T("eye limit\nabout 100 µm", 32, ORANGE).move_to([3.5, 1, 0])
        self.at("Your eye can")
        self.play(Create(eye), run_time=0.6)
        self.at("about 100")
        self.play(FadeIn(limit), run_time=0.6)

        mic = vocab("microscope", 38).move_to([0, 2.8, 0])
        sample = Square(0.5, stroke_color=BLUE, stroke_width=4,
                        fill_color=BLUE, fill_opacity=0.3).move_to([-4.6, 0.2, 0])
        sl = T("sample", 28).move_to([-4.6, -1.9, 0])
        lens = Ellipse(width=0.9, height=3.2, stroke_color=TEAL, stroke_width=5,
                       fill_color=TEAL, fill_opacity=0.2).move_to([0, 0.2, 0])
        ll = T("lenses", 28, TEAL).move_to([0, -1.9, 0])
        self.at("A microscope uses lenses")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(mic), FadeIn(sample),
                  FadeIn(sl), FadeIn(lens), FadeIn(ll), run_time=0.65)
        image = Square(2.6, stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.3).move_to([4.6, 0.2, 0])
        il = T("larger image", 28, BLUE).move_to([4.6, -1.9, 0])
        links = VGroup(arr([-3.8, 0.2, 0], [-0.7, 0.2, 0], TEAL),
                       arr([0.7, 0.2, 0], [2.9, 0.2, 0], TEAL))
        self.at("look larger")
        self.play(*[GrowArrow(a) for a in links], TransformFromCopy(sample, image), FadeIn(il), run_time=0.6)
        mag = vocab("magnification", 40).move_to(mic)
        definition = T("how many times larger the image looks", 30).move_to([0, -3.1, 0])
        self.at("Magnification tells us")
        self.play(ReplacementTransform(mic, mag), FadeIn(definition), run_time=0.6)
        self.finish()


class S04Light(SpokenScene):
    def construct(self):
        title = T("Seeing fine detail", 38).move_to([0, 2.9, 0])
        # An unresolved patch stays unresolved when enlarged.
        patch = cell_shape(1.2, 0.9, -4, 0.5, op=0.55).set_stroke(width=0)
        larger = cell_shape(2.6, 1.95, 0, 0.5, op=0.55).set_stroke(width=0)
        link = arr([-3.1, 0.5, 0], [-1.65, 0.5, 0], GREY)
        labels = VGroup(T("enlarged", 28, YELLOW).move_to([0, -1.3, 0]),
                        T("same unresolved detail", 28, GREY).move_to([0, -2.2, 0]))
        self.at("Seeing fine detail")
        self.play(FadeIn(title), FadeIn(patch), GrowArrow(link), TransformFromCopy(patch, larger),
                  FadeIn(labels), run_time=0.75)
        lm = T("best light microscopes", 34, TEAL).move_to([0, 2.9, 0])
        limit = M("finest detail: about 0.2 µm", 30, ORANGE).move_to([0, 1.5, 0])
        self.at("The best light microscopes")
        self.play(FadeOut(patch), FadeOut(larger), FadeOut(link), FadeOut(labels),
                  ReplacementTransform(title, lm), run_time=0.6)
        self.at("show details down")
        marker = Line([-4.7, 0.6, 0], [4.7, 0.6, 0], color=ORANGE, stroke_width=4)
        fine = VGroup(Dot([-0.4, -0.2, 0], radius=0.24, color=BLUE),
                      Dot([0.4, -0.2, 0], radius=0.24, color=BLUE),
                      T("fine detail", 28, BLUE).move_to([0, -1.1, 0]))
        self.play(FadeIn(limit), Create(marker), FadeIn(fine), run_time=0.6)
        school = T("school microscope", 30, TEAL).move_to([-3.7, -0.35, 0])
        whole = VGroup(cell_shape(1.7, 1.15, -4.5, -1.9), cell_shape(1.4, 1.1, -2.55, -1.9))
        whole_label = T("most whole cells", 26, BLUE).move_to([-3.6, -3.1, 0])
        self.at("A school microscope")
        self.play(FadeOut(fine), FadeIn(school), run_time=0.5)
        self.at("shows most whole cells")
        self.play(FadeIn(whole), FadeIn(whole_label), run_time=0.6)
        electron = T("electron microscope", 30, TEAL).move_to([3.5, -0.35, 0])
        beam = T("electrons", 26, TEAL).move_to([3.5, -1.05, 0])
        self.at("Electron microscopes")
        self.play(FadeIn(electron), run_time=0.5)
        self.at("use electrons")
        self.play(FadeIn(beam), run_time=0.5)
        detail = VGroup(cell_shape(2.3, 1.2, 3.5, -2.05),
                        VGroup(*[Rectangle(width=0.32, height=0.12, color=BLUE, fill_color=BLUE,
                                 fill_opacity=0.5) for _ in range(3)]).arrange(DOWN, buff=0.15).move_to([3.5, -2.05, 0]))
        detail_label = T("finer cell parts", 26, BLUE).move_to([3.5, -3.1, 0])
        self.at("They showed cell parts")
        self.play(FadeIn(detail), FadeIn(detail_label), run_time=0.65)
        self.finish()


class S06Shapes(SpokenScene):
    def construct(self):
        title = T("Shape and size depend on job and organism", 34).move_to([0, 2.95, 0])
        note = T("not to scale", 24, GREY).move_to([0, -3.25, 0])
        varied = VGroup(cell_shape(3.2, 1.4, -3.6, 0.4), cell_shape(1.5, 2.4, 3.5, 0.4))
        self.at("Cells differ")
        self.play(FadeIn(title), FadeIn(note), FadeIn(varied), run_time=0.6)
        self.at("depending on their job")
        self.play(varied[0].animate.stretch(1.3, 1), varied[1].animate.stretch(1.3, 0), run_time=0.8)
        face = VGroup(cell_shape(2.15, 2.0, -4.6, 0.4, op=0.32),
                      cell_shape(1.0, 0.85, -4.6, 0.4, op=0.05))
        face_label = T("face-on", 26, GREY).move_to([-4.6, -1.35, 0])
        rbc = T("red blood cell", 30, BLUE).move_to([-3.3, 1.95, 0])
        self.at("A red blood cell")
        self.play(ReplacementTransform(varied[0], face), FadeOut(varied[1]),
                  FadeIn(face_label), FadeIn(rbc), run_time=0.6)
        # A biconcave profile shows both depressed faces, with thick rims.
        edge = VMobject(stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25)
        edge.set_points_smoothly([[-1.25, 0, 0], [-1, 0.4, 0], [-0.55, 0.3, 0],
                                 [0, 0.14, 0], [0.55, 0.3, 0], [1, 0.4, 0], [1.25, 0, 0],
                                 [1, -0.4, 0], [0.55, -0.3, 0], [0, -0.14, 0],
                                 [-0.55, -0.3, 0], [-1, -0.4, 0], [-1.25, 0, 0]])
        edge.move_to([-1.6, 0.4, 0])
        edge_label = T("edge-on", 26, GREY).move_to([-1.6, -1.35, 0])
        self.at("pressed in on both faces")
        self.play(FadeIn(edge), FadeIn(edge_label), run_time=0.7)
        body = cell_shape(0.9, 0.85, 2, 0.3)
        branches = VGroup()
        paths = [[(2.4, 0.3), (3.3, 0.4), (4.7, 0.8), (6, 0.7)],
                 [(4.6, 0.78), (5, 1.4), (5.6, 1.65)],
                 [(4, 0.6), (4.8, -0.4), (5.7, -0.65)],
                 [(1.7, 0.6), (1.2, 1.1), (0.95, 1.65)],
                 [(1.7, 0.05), (1.15, -0.8), (1.4, -1.35)]]
        for pts in paths:
            branch = VMobject(color=BLUE, stroke_width=4)
            branch.set_points_as_corners([[x, y, 0] for x, y in pts])
            branches.add(branch)
        nerve_label = T("nerve cell", 30, BLUE).move_to([3.5, -2.1, 0])
        self.at("A nerve cell")
        self.play(FadeIn(body), FadeIn(nerve_label), run_time=0.5)
        self.at("long thin branches")
        self.play(*[Create(b) for b in branches], run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "All living things are made of cells, even ones too small to see."