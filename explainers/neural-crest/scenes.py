"""Neural crest: shared ancestry, regional fates and migration.

COLOR MAP (original concept colors retained)
  YELLOW = neural crest cells and their population ancestry
  BLUE   = Eph B receptor (reserved; not shown in this narration)
  RED    = exclusion / failed development (ephrin B in the original film)
  GREEN  = permitted route (reserved)
  TEAL   = dorsal root ganglia and peripheral neural derivatives
  GREY   = embryonic structures and labels
  GOLD   = explanatory highlights; pigment and skeleton use neutral TEXT
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

CX = [-5.2 + 2.0 * i for i in range(5)]      # somite centres
TUBE_Y = 2.5
ROW_Y = -1.6


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def crest_cell(r=0.17):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.9)


def make_tube():
    return RoundedRectangle(corner_radius=0.3, width=10.0, height=0.9, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.2).move_to([-1.2, TUBE_Y, 0])


def tube_label(txt="neural tube"):
    return T(txt, 24, GREY).move_to([5.2, TUBE_Y - 0.35, 0])


def top_cells(n=9):
    xs = np.linspace(-5.7, 3.3, n)
    return VGroup(*[crest_cell().move_to([x, TUBE_Y + 0.27, 0]) for x in xs])


def pop(group, color, k=1.15):
    return LaggedStart(*[Indicate(m, color=color, scale_factor=k) for m in group], lag_ratio=0.1)


def lane_dots(cx, rostral=True):
    x0 = cx - 0.475 if rostral else cx + 0.475
    return [crest_cell(0.15).move_to([x0 + (j - 1) * 0.34, TUBE_Y + 0.27, 0]) for j in range(3)]


def somite(cx):
    outer = Rectangle(width=1.9, height=3.8, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([cx, -0.4, 0])
    scl = Rectangle(width=1.9, height=2.9, stroke_width=0, fill_color=TEXT, fill_opacity=0.08).move_to([cx, -0.85, 0])
    div = DashedLine([cx, 0.6, 0], [cx, -2.3, 0], color=GREY, stroke_width=2, dash_length=0.12)
    return VGroup(outer, scl, div)


def half(cx, rostral=True, color=GREEN, op=0.2):
    x = cx - 0.475 if rostral else cx + 0.475
    return Rectangle(width=0.95, height=2.9, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([x, -0.85, 0])


def ganglion(x, y=ROW_Y, w=1.0, h=0.75, color=TEAL):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45).move_to([x, y, 0])


def qmark(x, y):
    q = T("?", 56, GOLD, weight=BOLD)
    back = Circle(radius=0.42, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, q).move_to([x, y, 0])


def tab(color, w=0.34, h=0.5):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.55)


class S00Title(TitleCard):
    LESSON = "The Neural Crest: Cells That Leave Home"
    TITLE = "Neural Crest: One Origin, Many Tissues"


def label(txt, x, y, size=26, color=TEXT):
    return T(txt, size, color, line_spacing=0.85).move_to([x, y, 0])


def arrow(a, b, color=YELLOW):
    return Arrow(a, b, buff=0.14, color=color, stroke_width=3)


def population(x=0, y=1.9):
    cells = VGroup(*[crest_cell(0.18).move_to([x+(i-1)*0.5, y, 0]) for i in range(3)])
    return VGroup(cells, label("crest population", x, y+0.6, color=YELLOW))


def axial_map():
    # A schematic embryo silhouette, with head, neck, trunk and caudal landmarks.
    head = Circle(0.62, color=GREY, fill_opacity=0.12).move_to([-4.8, 2.0, 0])
    body = RoundedRectangle(width=1.4, height=4.2, corner_radius=0.5,
                            color=GREY, fill_opacity=0.12).move_to([-4.8, -0.65, 0])
    axis = Line([-4.8, 1.3, 0], [-4.8, -2.3, 0], color=GREY)
    levels = VGroup(*[crest_cell(0.15).move_to([-4.8, y, 0]) for y in [2, 0.95, -0.55, -2.3]])
    names = VGroup(label("head", -2.9, 2), label("vagal", -2.9, 0.95),
                   label("trunk", -2.9, -0.55), label("sacral", -2.9, -2.3))
    return VGroup(head, body, axis, levels, names)


class S01Row(SpokenScene):
    def construct(self):
        origin = population(-4.5, 0.7)
        self.at("The neural crest")
        self.play(FadeIn(origin), run_time=0.6)
        targets = VGroup()
        for phrase, txt, y, col in [
            ("nerve cells outside", "peripheral neurons", 2.1, TEAL),
            ("glia that wrap", "nerve-wrapping glia", 0.8, TEAL),
            ("pigment cells", "melanocytes", -0.5, TEXT),
            ("bone and cartilage", "facial bone / cartilage", -1.8, TEXT)]:
            node = chip(txt, col, size=26).move_to([2.5, y, 0])
            link = arrow([-3.45, 0.7, 0], node.get_left())
            targets.add(VGroup(link, node))
            self.at(phrase)
            self.play(GrowArrow(link), FadeIn(node), run_time=0.65)
        self.at("share an embryonic ancestor")
        self.play(Indicate(origin, color=YELLOW, scale_factor=1.08), run_time=0.8)
        plate = RoundedRectangle(width=5, height=2.8, corner_radius=0.25, color=GREY,
                                 fill_color=GREY, fill_opacity=0.2).move_to([-2.8, 0, 0])
        border = Line([-0.3, -1.3, 0], [-0.3, 1.3, 0], color=YELLOW, stroke_width=7)
        cells = VGroup(*[crest_cell(0.19).move_to([-0.3, y, 0]) for y in [-0.9, 0, 0.9]])
        pl = label("neural plate", -2.8, 0)
        bl = label("crest at the border", 2.7, 1.6, color=YELLOW)
        self.at("Crest cells form")
        self.play(FadeOut(origin), FadeOut(targets), run_time=0.25)
        self.play(FadeIn(plate), FadeIn(pl), Create(border), FadeIn(bl), run_time=0.45)
        self.at("then leave and migrate")
        self.play(ReplacementTransform(border, cells), run_time=0.35)
        self.play(*[c.animate.shift(RIGHT*3.2) for c in cells], run_time=1.2)
        self.at("That shared origin")
        shared = population(-4.5, 0.7)
        tissues = VGroup(*[chip(t, TEAL if i == 0 else TEXT, size=25).move_to([2.2, y, 0])
                            for i, (t, y) in enumerate([
                                ("gut wall neurons", 1.8), ("hair melanocytes", 0.2),
                                ("inner-ear melanocytes", -1.4)])])
        links = VGroup(*[arrow([-3.45, 0.7, 0], t.get_left()) for t in tissues])
        self.play(*[FadeOut(m) for m in (plate, pl, cells, bl)], FadeIn(shared),
                  FadeIn(tissues), Create(links), run_time=0.7)
        hearing = label("support hearing", 2.2, -2.3, size=24)
        self.at("and hearing")
        self.play(FadeIn(hearing), Indicate(tissues[2], scale_factor=1.04), run_time=0.6)
        self.at("Where along the body")
        self.play(*[FadeOut(m) for m in (shared, tissues, links, hearing)],
                  FadeIn(axial_map()), FadeIn(label("Origin along the body", 1.8, 2.6, color=YELLOW)),
                  run_time=0.8)
        self.finish()


class S01Derivatives(SpokenScene):
    def construct(self):
        embryo = axial_map()
        self.at("In the head")
        self.play(FadeIn(embryo), run_time=0.5)
        facial = chip("facial bone / cartilage", TEXT, size=26).move_to([2.3, 2, 0])
        headlink = arrow([-2, 2, 0], facial.get_left())
        self.at("facial bone and cartilage")
        self.play(GrowArrow(headlink), FadeIn(facial), run_time=0.65)
        gut = chip("gut wall: neurons + glia", TEAL, size=26).move_to([2.3, 0.8, 0])
        # Route the sacral contribution below, then around the trunk derivatives.
        sacral_path = VMobject(color=YELLOW, stroke_width=3).set_points_as_corners([
            [-2, -2.3, 0], [6.2, -2.3, 0], [6.2, 0.8, 0]])
        gutlinks = VGroup(arrow([-2, 0.95, 0], gut.get_left()), sacral_path,
                           arrow([6.2, 0.8, 0], gut.get_right()))
        self.at("Vagal and sacral")
        self.play(Create(gutlinks), FadeIn(gut), run_time=0.8)
        trunk_text = T("sensory + sympathetic neurons\nSchwann cells: nerve-wrapping glia\nmelanocytes",
                       24, TEAL, line_spacing=1.2)
        trunk_box = RoundedRectangle(width=trunk_text.width + 0.8, height=trunk_text.height + 0.6,
                                     corner_radius=0.14, stroke_color=TEAL, stroke_width=2.5,
                                     fill_color=TEAL, fill_opacity=0.16)
        trunk = VGroup(trunk_box, trunk_text).move_to([2.3, -1.1, 0])
        trunklink = arrow([-2, -0.55, 0], trunk.get_left())
        self.at("Trunk crest gives")
        self.play(GrowArrow(trunklink), FadeIn(trunk), run_time=0.75)
        restriction = label("Birds + mammals: trunk crest\ndoes not normally make skeleton",
                            2.3, -2.85, size=24, color=RED)
        self.at("In birds and mammals")
        self.play(FadeIn(restriction), run_time=0.8)
        self.finish()


class S02Leave(SpokenScene):
    def construct(self):
        identity = label("crest identity", 0, 2.9, color=YELLOW)
        self.at("First")
        self.play(FadeIn(identity), run_time=0.5)
        proposed = label("one proposed network", 0, 2.1, size=24, color=GREY)
        sig = chip("BMP · Wnt · FGF", TEXT, size=26).move_to([-4.3, 0.6, 0])
        border = chip("border genes", TEXT, size=26).move_to([0, 0.6, 0])
        crest = chip("crest genes", YELLOW, size=26).move_to([4.1, 0.6, 0])
        self.at("In one proposed network")
        self.play(FadeIn(proposed), FadeIn(sig), run_time=0.7)
        self.at("turn on border genes")
        a = arrow(sig.get_right(), border.get_left(), GREY)
        self.play(GrowArrow(a), FadeIn(border), run_time=0.7)
        self.at("then crest genes")
        b = arrow(border.get_right(), crest.get_left(), GREY)
        self.play(GrowArrow(b), FadeIn(crest), run_time=0.6)
        output = chip("adhesion · movement · fate", TEXT, size=26).move_to([0, -1.6, 0])
        c = arrow(crest.get_bottom(), output.get_top(), GREY)
        self.at("These control adhesion")
        self.play(GrowArrow(c), FadeIn(output), run_time=0.7)
        # Reuse the original film's epithelial rectangles and rounding/departure action.
        cells = VGroup(*[RoundedRectangle(corner_radius=0.18, width=1.25, height=2.7,
                            stroke_color=YELLOW if i == 2 else GREY, stroke_width=3,
                            fill_color=YELLOW if i == 2 else GREY, fill_opacity=0.28)
                            .move_to([(i-2)*1.25, 0.9, 0]) for i in range(5)])
        basement = VGroup(Line([-4, -0.65, 0], [-0.8, -0.65, 0], color=GREY, stroke_width=5),
                          Line([-0.8, -0.65, 0], [0.8, -0.65, 0], color=GREY, stroke_width=5),
                          Line([0.8, -0.65, 0], [4, -0.65, 0], color=GREY, stroke_width=5))
        bm = label("basement membrane", -3.7, -1.3, size=24, color=GREY)
        polarity = DoubleArrow([0, 1.95, 0], [0, -0.1, 0], buff=0, color=TEXT)
        polabel = label("top-to-bottom polarity", 0, 3, size=24)
        self.at("Crest cells loosen")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(cells), Create(basement),
                  FadeIn(bm), GrowArrow(polarity), FadeIn(polabel), run_time=0.6)
        self.play(*[cells[i].animate.shift(RIGHT*(i-2)*0.23) for i in range(5)], run_time=0.8)
        self.at("lose their top")
        circ = crest_cell(0.58).move_to(cells[2])
        self.play(FadeOut(polarity), FadeOut(polabel), ReplacementTransform(cells[2], circ), run_time=0.7)
        self.at("break through the basement")
        self.play(FadeOut(basement[1]), circ.animate.move_to([0, -0.6, 0]), run_time=0.8)
        self.at("and crawl away")
        path = CubicBezier(circ.get_center(), [0, -2, 0], [1.8, -2, 0], [3.3, -1.8, 0])
        self.play(MoveAlongPath(circ, path), run_time=1.15)
        sheet = label("cell in a sheet", -2.3, 2.8, size=26, color=GREY)
        free = label("free mesenchymal cell", 3.3, -2.75, size=24, color=YELLOW)
        self.at("from a cell in a sheet")
        self.play(FadeIn(sheet), run_time=0.5)
        self.at("a free mesenchymal cell")
        self.play(FadeIn(free), run_time=0.6)
        emt = label("epithelial-to-mesenchymal transition", 0, -3.45, size=26, color=GOLD)
        self.at("transition")
        self.play(FadeIn(emt), run_time=0.5)
        self.at("EMT")
        self.play(Transform(emt, label("EMT", 0, -3.45, size=30, color=GOLD)), run_time=0.5)
        self.finish()


class S03Route(SpokenScene):
    def construct(self):
        title = label("Chick trunk · cross-section", 0, 3.15, color=GREY)
        tube = Circle(0.7, color=GREY, fill_opacity=0.18).move_to([-3, 1.2, 0])
        tl = label("neural tube", -4.9, 1.2, size=24, color=GREY)
        skin = ArcBetweenPoints([-5.8, 2.2, 0], [0.7, 2.2, 0], angle=-0.3, color=GREY)
        sl = label("skin", -5.5, 2.8, size=24, color=GREY)
        blocks = VGroup(*[RoundedRectangle(width=1.25, height=1.6, corner_radius=0.12,
                           color=GREY, fill_opacity=0.15).move_to([x, -0.35, 0]) for x in [-4.65, -1.35]])
        bl = label("somites", -3, -1.55, size=24, color=GREY)
        anatomy = VGroup(title, tube, tl, skin, sl, blocks, bl)
        cells = VGroup(*[crest_cell().move_to([-3+(i-1)*0.4, 2.05, 0]) for i in range(3)])
        self.at("Migration depends")
        self.play(FadeIn(anatomy), FadeIn(cells), run_time=0.75)
        vm = VMobject(color=YELLOW, stroke_width=4).set_points_smoothly([
            [-2.6, 2.05, 0], [-1.35, 1.2, 0], [-1.35, -0.4, 0], [-2, -2.3, 0]])
        vl = label("ventromedial", -3, -2.8, size=24, color=YELLOW)
        self.at("through the somites")
        self.play(Create(vm), FadeIn(vl), run_time=0.6)
        self.play(MoveAlongPath(cells[0], vm), run_time=1.5)
        gang = ganglion(3.25, y=-0.4, w=4.9, h=3.5)
        derivatives = label("dorsal root sensory ganglia\nsympathetic ganglia\nadrenal medulla", 3.25, -0.4, size=25, color=TEAL)
        link = arrow([-1.6, -1.6, 0], [0.7, -0.6, 0])
        self.at("It gives sensory")
        self.play(GrowFromCenter(gang), FadeIn(derivatives), GrowArrow(link), run_time=0.85)
        dl = VMobject(color=YELLOW, stroke_width=4).set_points_smoothly([
            [-3, 2.05, 0], [-1.3, 1.9, 0], [0.3, 1.85, 0]])
        pigment = chip("mostly melanocytes", TEXT, size=24).move_to([3.3, 2.05, 0])
        dlab = label("later: dorsolateral", -0.4, 2.7, size=24, color=YELLOW)
        self.at("A later")
        self.play(Create(dl), FadeIn(dlab), run_time=0.5)
        self.play(MoveAlongPath(cells[1], dl), run_time=0.8)
        self.at("mostly melanocytes")
        self.play(FadeIn(pigment), run_time=0.6)
        self.finish()


class S04Collective(SpokenScene):
    def construct(self):
        title = label("Crest cells steer each other", 0, 3, color=YELLOW)
        a, b = crest_cell(0.6).move_to([-3, 0.4, 0]), crest_cell(0.6).move_to([3, 0.4, 0])
        self.at("Crest cells")
        self.play(FadeIn(title), FadeIn(a), FadeIn(b), run_time=0.6)
        species = label("frog + zebrafish", 0, 2.15, size=26, color=GREY)
        incoming = VGroup(arrow([-3, -0.7, 0], [-1.3, -0.7, 0]), arrow([3, -0.7, 0], [1.3, -0.7, 0]))
        self.at("In frog and zebrafish")
        self.play(FadeIn(species), Create(incoming), a.animate.move_to([-0.6, 0.4, 0]),
                  b.animate.move_to([0.6, 0.4, 0]), run_time=1.2)
        contact = label("contact inhibition of locomotion", 0, -2, size=28, color=GOLD)
        self.at("cells that touch")
        self.play(FadeOut(incoming), FadeIn(contact), run_time=0.5)
        self.at("head off in new directions")
        self.play(a.animate.move_to([-2.4, 1, 0]), b.animate.move_to([2.4, -0.5, 0]), run_time=1.0)
        group = VGroup(*[crest_cell(0.32).move_to([x, y, 0]) for x, y in
                        [(-3.5, 0.7), (-2.2, 0.9), (-3.4, -0.7), (-2, -0.6)]])
        frog = label("frog cranial crest", 0, 2.6, color=GREY)
        self.at("In frog cranial crest")
        self.play(FadeOut(a), FadeOut(b), FadeOut(contact), FadeOut(title),
                  ReplacementTransform(species, frog), FadeIn(group), run_time=0.65)
        mutual = label("mutual attraction", -2.6, 1.55, color=YELLOW)
        self.at("mutual attraction")
        self.play(group.animate.arrange_in_grid(rows=2, buff=0.17).move_to([-2.6, 0, 0]),
                  FadeIn(mutual), run_time=0.8)
        cue = chip("Sdf1", TEXT, size=28).move_to([4.6, 0, 0])
        gradient = VGroup(*[Rectangle(width=0.45, height=2.6, stroke_width=0,
                             fill_color=TEXT, fill_opacity=0.04+0.035*i).move_to([0.5+i*0.65, 0, 0])
                             for i in range(6)])
        guide = label("chemotaxis toward the cue", 2.6, -1.85, size=24)
        self.at("a chemical cue")
        self.play(FadeIn(gradient), FadeIn(cue), FadeIn(guide),
                  group.animate.shift(RIGHT*1.8), mutual.animate.shift(RIGHT*1.8), run_time=1.1)
        limit = label("Bird + mammal trunk crest: how far this applies is less clear",
                      0, -3, size=25, color=GREY)
        self.at("How far this applies")
        self.play(FadeIn(limit), run_time=0.75)
        self.finish()


class S06Clinic(SpokenScene):
    def construct(self):
        origin = population(0, 1.8)
        self.at("When crest development fails")
        self.play(FadeIn(origin), run_time=0.65)
        gut = RoundedRectangle(width=8, height=1.2, corner_radius=0.35,
                               color=GREY, fill_opacity=0.12).move_to([0, -0.1, 0])
        neurons = VGroup(*[ganglion(x, y=0.4, w=0.28, h=0.28) for x in [-3.4, -2.6, -1.8, -1]])
        distal = Line([0.4, 0.55, 0], [3.6, 0.55, 0], color=RED, stroke_width=6)
        gl = label("Hirschsprung disease", 0, -1.4, size=30)
        missing = label("distal gut: no wall neurons", 1.6, -2.3, size=25, color=RED)
        self.at("In Hirschsprung disease")
        self.play(FadeIn(gut), FadeIn(neurons), FadeIn(gl), run_time=0.7)
        self.at("the distal gut")
        self.play(Create(distal), FadeIn(missing), run_time=0.6)
        wa = label("Waardenburg syndrome", 0, 2.9, size=30)
        pigment = chip("pigment changes", TEXT, size=28).move_to([-3, 0, 0])
        hearing = chip("hearing loss", TEXT, size=28).move_to([3, 0, 0])
        self.at("syndrome")
        self.play(*[FadeOut(m) for m in (gut, neurons, distal, gl, missing, origin)],
                  FadeIn(wa), run_time=0.5)
        self.at("pigment changes")
        self.play(FadeIn(pigment), run_time=0.5)
        self.at("and hearing loss")
        self.play(FadeIn(hearing), run_time=0.5)
        # A neutral patient silhouette combines the named clinical findings.
        person = VGroup(Circle(0.4, color=GREY, fill_opacity=0.25).move_to([0, 0.8, 0]),
                        RoundedRectangle(width=1.15, height=1.6, corner_radius=0.3,
                                         color=GREY, fill_opacity=0.25).move_to([0, -0.45, 0]))
        both = label("gut wall neurons absent", 0, -2, size=26, color=RED)
        one = label("some patients: one gene mutation", 0, 2.9, size=28, color=YELLOW)
        self.at("Some patients have both")
        self.play(ReplacementTransform(wa, one), FadeIn(person), FadeIn(both), run_time=0.8)
        self.at("Their different symptoms")
        shared = population(0, 1.8)
        nodes = VGroup(*[chip(t, c, size=24).move_to([x, -1, 0]) for t, c, x in
                         [("gut neurons", TEAL, -4.2), ("hair pigment", TEXT, 0),
                          ("inner-ear pigment", TEXT, 4.2)]])
        links = VGroup(*[arrow([0, 1.4, 0], n.get_top()) for n in nodes])
        rule = label("shared developmental ancestry", 0, -2.7, size=30, color=YELLOW)
        self.play(*[FadeOut(m) for m in (one, person, both, pigment, hearing)],
                  FadeIn(shared), FadeIn(nodes), Create(links), run_time=0.9)
        self.at("a shared developmental ancestry")
        self.play(FadeIn(rule), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "One origin: neural crest gives nerves, glia, pigment cells and facial bone."
