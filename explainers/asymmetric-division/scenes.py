"""Asymmetric division: one protein makes sisters different (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = Numb (the crescent, and the protein in a daughter)
  TEAL   = Notch (receptor bars) and the signal passing between the sisters
  RED    = block (Numb switching Notch off in a daughter)
  VIOLET = inner fate: neuron and sheath (Notch off)
  ORANGE = outer fate: hair and socket (Notch on)
  GREY   = cells, outlines, "no Numb", unknown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
VIOLET = "#A98BE0"  # inner fate, kept apart from Notch teal
CY = 0.5          # vertical centre of the cells
DX = 2.4          # daughters sit at +-DX
DR = 2.3         # daughter radius
MR = 2.8          # mother radius
SY = 0.95         # signal arrow offset from CY


def cell(c, r, color=GREY, op=0.14):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(c)


def crescent(center, r, span, w=14):
    return Arc(radius=r, start_angle=PI - span / 2, angle=span, arc_center=center, color=YELLOW, stroke_width=w)


def arr(a, b, color=TEAL, w=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def block(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 2))


def bar(x, color=TEAL):
    return RoundedRectangle(corner_radius=0.08, width=0.26, height=1.3, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.55).move_to([x, CY, 0])


def label(text, color, x, y, size=26):
    t = T(text, size, color)
    return t.move_to([x, y, 0])


def fate_chip(kind, x, y=-3.2):
    txt, col = ("neuron + sheath", VIOLET) if kind == "in" else ("hair + socket", ORANGE)
    return chip(txt, col, size=28).move_to([x, y, 0])


def fate(c, color):
    return c.animate.set_stroke(color).set_fill(color, 0.38)


# signal geometry
UP_A = ([-1.8, CY + SY, 0], [1.8, CY + SY, 0])      # left cell speaks, right cell hears
DN_A = ([1.8, CY - SY, 0], [-1.8, CY - SY, 0])      # right cell speaks, left cell hears


class S00Title(TitleCard):
    LESSON = "Asymmetric division: Numb"
    TITLE = "How Neural Stem Cells Keep Making Cells"


def split(scene, mother, extras=(), rt=1.0):
    """stretch the mother, then cross-fade into two daughters. returns (L, R)."""
    L = cell([-DX, CY, 0], DR)
    R = cell([DX, CY, 0], DR)
    g = VGroup(mother, *extras)
    scene.play(g.animate.stretch(1.45, 0), run_time=rt * 0.5)
    scene.play(FadeOut(mother), FadeIn(L), FadeIn(R), run_time=rt * 0.5)
    return L, R


# Additional concepts retain the old palette for bristle fates and signalling.
# BLUE = neuroblast / renewal; GREEN = differentiating neural output
# GOLD = apical polarity; TEXT = Prospero / Brat cargo; RED = inhibition / failed control


def head(text):
    return label(text, TEXT, 0, 3.35, 30)


def basal(center, r, color=YELLOW):
    # Separate cortical patches: Numb with its adaptor, Miranda with Prospero / Brat.
    return VGroup(Arc(radius=r, start_angle=PI * 1.2, angle=PI * .28,
                      arc_center=center, color=color, stroke_width=14),
                  Arc(radius=r, start_angle=PI * 1.52, angle=PI * .28,
                      arc_center=center, color=TEXT, stroke_width=14))


def spindle(center=(-2, 0, 0), vertical=True):
    c = np.array(center, float)
    a = UP if vertical else (UP + RIGHT) / np.sqrt(2)
    p, q = c + 1.35*a, c - 1.35*a
    across = np.array([a[1], -a[0], 0])
    return VGroup(*[VGroup(Line(p, c + across*d, color=GREY, stroke_width=2),
                           Line(c + across*d, q, color=GREY, stroke_width=2))
                    for d in (-.55, 0, .55)],
                  Dot(p, radius=.09, color=TEXT), Dot(q, radius=.09, color=TEXT))


def neural_pair():
    return cell([-2, 1, 0], 1.5, BLUE), cell([-2, -1.8, 0], .8, GREEN)


def bristle_rig():
    L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
    cres = crescent([-DX, CY, 0], DR, 2)
    return L, R, cres


class S01Question(SpokenScene):
    def construct(self):
        mother = cell([-2, 0, 0], 2.2, BLUE)
        title = head("Two jobs for one stem cell")
        self.at("A neural stem cell")
        self.play(FadeIn(mother), FadeIn(title), run_time=.6)
        renew = chip("stay a stem cell", BLUE, size=28).move_to([3.1, 1.1, 0])
        output = chip("differentiate", GREEN, size=28).move_to([3.1, -1.1, 0])
        self.at("stay a stem cell")
        self.play(FadeIn(renew), run_time=.5)
        self.at("make cells that differentiate")
        self.play(FadeIn(output), run_time=.5)
        self.at("Asymmetric division")
        nb, gmc = neural_pair()
        self.play(mother.animate.stretch(1.2, 1), run_time=.4)
        self.play(ReplacementTransform(mother, nb), FadeIn(gmc), run_time=.7)
        self.at("In the fly")
        self.play(ReplacementTransform(title, head("Fly neuroblast · type I")), run_time=.4)
        self.at("the large daughter")
        n = label("neuroblast", BLUE, 2.8, 1.9, 30)
        axis = VGroup(label("apical", GREY, -5, 2, 24),
                      arr([-5, 1.4, 0], [-5, -1.4, 0], GREY, 3),
                      label("basal", GREY, -5, -2, 24))
        self.play(FadeOut(renew), FadeIn(n), FadeIn(axis), Indicate(nb, color=BLUE), run_time=.6)
        self.at("The small daughter")
        g = label("ganglion mother cell", GREEN, 2.8, -1.8, 28)
        self.play(FadeOut(output), FadeIn(g), Indicate(gmc, color=GREEN), run_time=.6)
        self.at("It divides once more")
        daughters = VGroup(cell([.5, -1.8, 0], .55, GREEN), cell([2.1, -1.8, 0], .55, GREEN))
        self.play(FadeOut(g), ReplacementTransform(gmc, daughters), run_time=.8)
        out = label("2 neurons or glia", GREEN, 1.3, -3, 28)
        self.play(FadeIn(out), run_time=.4)
        self.at("keeps making new cells")
        fresh = cell([-2, -1.8, 0], .8, GREEN)
        self.play(nb.animate.stretch(1.13, 1), run_time=.3)
        self.play(nb.animate.stretch(1/1.13, 1), FadeIn(fresh, shift=DOWN*.3), run_time=.7)
        self.finish()


class S02Crescent(SpokenScene):
    def construct(self):
        mother = cell([-2, 0, 0], 2.2)
        title = head("Fly neuroblast · sorting the daughters")
        self.add(mother, title)
        self.at("Polarity marks")
        axes = VGroup(label("apical", GOLD, -5.4, 2.2, 24), label("basal", GREY, -5.4, -2.2, 24))
        self.play(FadeIn(axes), run_time=.5)
        top = Arc(radius=2.2, start_angle=PI*.3, angle=PI*.4,
                  arc_center=[-2, 0, 0], color=GOLD, stroke_width=14)
        par = chip("Par + Inscuteable", GOLD, size=26).move_to([3.1, 2.25, 0])
        self.at("Par proteins")
        self.play(Create(top), FadeIn(par), run_time=.6)
        pins = chip("Pins", GOLD, size=26).move_to([3.1, 1.2, 0])
        link1 = arr([3.1, 1.8, 0], [3.1, 1.65, 0], GOLD, 3)
        self.at("recruits pins")
        self.play(FadeIn(pins), GrowArrow(link1), run_time=.5)
        sp = spindle(vertical=False)
        mud = label("Mud → spindle microtubules", GREY, 3.1, .2, 28)
        tether = Line([-.7, 1.8, 0], [-1.05, .95, 0], color=GOLD, stroke_width=4)
        self.at("including mud")
        self.play(FadeIn(mud), Create(sp), Create(tether), run_time=.5)
        self.at("lines the spindle")
        self.play(Transform(sp, spindle()), Transform(tether, Line([-1.3, 2, 0], [-2, 1.35, 0], color=GOLD)), run_time=.8)
        apkc = chip("aPKC", GOLD, size=26).move_to([3.1, 1.65, 0])
        numb = chip("Numb", YELLOW, size=26).move_to([-2, -2.75, 0])
        apical_numb = VGroup(
            Arc(radius=2.2, start_angle=PI*.23, angle=PI*.1,
                arc_center=[-2, 0, 0], color=YELLOW, stroke_width=14),
            label("Numb", YELLOW, .35, 2.35, 24),
            Line([.1, 2.1, 0], [-.55, 1.65, 0], color=YELLOW, stroke_width=2),
        ).set_opacity(.45)
        veto = block([2.45, 1.65, 0], [-.55, 1.65, 0], w=4)
        self.at("The protein")
        self.play(FadeOut(par), FadeOut(pins), FadeOut(link1), FadeOut(mud), run_time=.25)
        self.play(FadeIn(apkc), FadeIn(numb), Create(apical_numb), run_time=.25)
        self.at("keeps numb off")
        self.play(Create(veto), run_time=.8)
        cres = basal([-2, 0, 0], 2.2)
        cargo = VGroup(chip("Numb · own adaptor", YELLOW, size=24),
                       chip("Miranda: Prospero + Brat", TEXT, size=24)).arrange(DOWN, buff=.3).move_to([3.1, -1.55, 0])
        self.at("end up at the bottom")
        self.play(FadeOut(numb), FadeOut(veto), FadeOut(apical_numb),
                  Create(cres), FadeIn(cargo), run_time=.7)
        self.at("Division hands this cargo")
        nb, gmc = neural_pair()
        gcres = basal([-2, -1.8, 0], .8)
        self.play(FadeOut(sp), FadeOut(tether), FadeOut(top), FadeOut(apkc),
                  ReplacementTransform(mother, nb), FadeIn(gmc), ReplacementTransform(cres, gcres), run_time=.8)
        nucleus = cell([-2, -1.8, 0], .48, GREY, .05)
        pro = label("Prospero", TEXT, .2, -1.8, 24)
        genes = VGroup(label("self-renewal genes", TEXT, 3.3, .25, 26),
                       label("division genes", TEXT, 3.3, -.45, 26))
        self.at("Prospero enters the nucleus")
        self.play(FadeOut(cargo), FadeIn(nucleus), FadeIn(pro), FadeIn(genes), run_time=.4)
        # A dot represents the named protein; the full label remains outside the small nucleus.
        marker = Dot([-.8, -2.3, 0], color=TEXT, radius=.12)
        self.add(marker)
        self.play(marker.animate.move_to(nucleus.get_center()),
                  pro.animate.move_to([.4, -2.6, 0]), run_time=.7)
        self.at("shuts down genes")
        self.play(genes.animate.set_opacity(.25), run_time=.6)
        self.finish()


class S03Notch(SpokenScene):
    def construct(self):
        mother = cell([0, CY, 0], 2.5)
        title = head("Fly sensory organ precursor · bristle")
        self.at("shows how inherited cargo")
        self.play(FadeIn(mother), FadeIn(title), run_time=.6)
        axis = VGroup(label("head", GREY, -5.7, -2.8, 24),
                      arr([-4.7, -2.8, 0], [4.7, -2.8, 0], GREY, 3),
                      label("tail", GREY, 5.7, -2.8, 24),
                      label("within the epithelial plane", GREY, 0, -3.4, 24))
        self.at("Take the fly")
        self.play(FadeIn(axis), run_time=.5)
        cres = crescent([0, CY, 0], 2.5, 1.8)
        self.at("forms a crescent")
        self.play(Create(cres), run_time=.5)
        self.at("passes to one daughter")
        L, R = cell([-DX, CY, 0], DR), cell([DX, CY, 0], DR)
        cres2 = crescent([-DX, CY, 0], DR, 2)
        self.play(FadeOut(mother), FadeIn(L), FadeIn(R), ReplacementTransform(cres, cres2), run_time=.6)
        nl = label("Numb", YELLOW, -DX, .1, 28)
        self.play(FadeIn(nl), run_time=.3)
        bl, br = bar(-.32, GREY), bar(.32)
        # The flat end touches only the Numb daughter's grey receptor.
        blk = block(nl.get_right() + RIGHT*.15, [-.45, .1, 0])
        self.at("it blocks notch")
        self.play(FadeIn(bl), FadeIn(br), Create(blk), run_time=.5)
        notch = label("Notch", TEAL, 0, 2.4, 28)
        self.at("a receptor")
        self.play(FadeIn(notch), run_time=.5)
        self.at("The sister can still hear")
        self.play(GrowArrow(arr(*UP_A)), run_time=.6)
        self.finish()


class S04Fates(SpokenScene):
    def construct(self):
        title = head("Bristle · simplified branches")
        self.add(title)
        left = VGroup(label("inner branch", VIOLET, -3.2, 2.55, 28),
                      chip("Numb + / Notch off", YELLOW, size=26).move_to([-3.2, 1.8, 0]))
        right = VGroup(label("outer branch", ORANGE, 3.2, 2.55, 28),
                       chip("no Numb / Notch on", TEAL, size=26).move_to([3.2, 1.8, 0]))
        def branch(x, color):
            return VGroup(Line([x, 1.3, 0], [x, .4, 0], color=color),
                          Line([x, .4, 0], [x-1, -.7, 0], color=color),
                          Line([x, .4, 0], [x+1, -.7, 0], color=color))
        inner = branch(-3.2, VIOLET)
        outer = branch(3.2, ORANGE)
        a = VGroup(chip("neuron", VIOLET, size=24).move_to([-4.2, -1.2, 0]),
                   chip("sheath", VIOLET, size=24).move_to([-2.2, -1.2, 0]))
        b = VGroup(chip("hair", ORANGE, size=24).move_to([2.2, -1.2, 0]),
                   chip("socket", ORANGE, size=24).move_to([4.2, -1.2, 0]))
        self.at("The numb daughter")
        self.play(FadeIn(left), run_time=.4)
        self.at("the inner branch")
        self.play(Create(inner), run_time=.5)
        self.at("the neuron and sheath")
        self.play(FadeIn(a), run_time=.5)
        self.at("Its sister")
        self.play(FadeIn(right), run_time=.4)
        self.at("the outer branch")
        self.play(Create(outer), run_time=.5)
        self.at("the hair and socket")
        self.play(FadeIn(b), run_time=.5)
        both = label("Both branches differentiate", TEXT, 0, -2.8, 30)
        self.at("both branches differentiate")
        self.play(FadeIn(both), run_time=.6)
        self.at("Notch chooses")
        self.play(Indicate(right, color=TEAL), Indicate(left, color=YELLOW), run_time=.6)
        self.finish()


class S05Tests(SpokenScene):
    def construct(self):
        title = head("Bristle · test the branch choice")
        self.add(title)
        def panel(x, name, color):
            return VGroup(label(name, color, x, 2.3, 28),
                          cell([x-1, 1, 0], .65), cell([x+1, 1, 0], .65))
        left = panel(-3.2, "No Numb", GREY)
        right = panel(3.2, "Numb in both", YELLOW)
        self.at("Remove num")
        self.play(FadeIn(left), run_time=.6)
        branches1 = VGroup(*[arr([x, .3, 0], [x, -.6, 0], ORANGE, 4) for x in (-4.2, -2.2)])
        self.at("both daughters take the outer fate")
        self.play(fate(left[1], ORANGE), fate(left[2], ORANGE), Create(branches1), run_time=.7)
        sockets = VGroup(*[cell([x, -1.2, 0], .28, ORANGE, .38) for x in (-4.7, -3.7, -2.7, -1.7)],
                         label("4 outer support cells", ORANGE, -3.2, -2, 24),
                         label("outer fate · sockets", ORANGE, -3.2, -2.55, 24))
        self.at("four outer support cells")
        self.play(FadeIn(sockets), run_time=.6)
        absent1 = label("no neuron or sheath", GREY, -3.2, -3.2, 24)
        self.at("no neuron or sheath")
        self.play(FadeIn(absent1), run_time=.4)
        self.at("Give num to both daughters")
        nc = VGroup(crescent([2.2, 1, 0], .65, 2, 8), crescent([4.2, 1, 0], .65, 2, 8))
        self.play(FadeIn(right), Create(nc), run_time=.6)
        branches2 = VGroup(*[arr([x, .3, 0], [x, -.6, 0], VIOLET, 4) for x in (2.2, 4.2)])
        self.at("both take the inner branch")
        self.play(fate(right[1], VIOLET), fate(right[2], VIOLET), Create(branches2), run_time=.6)
        inner = VGroup(label("neurons + sheath cells", VIOLET, 3.2, -1.5, 24),
                       label("no hair or socket", GREY, 3.2, -2.3, 24))
        self.at("Neurons and sheath cells")
        self.play(FadeIn(inner), run_time=.6)
        self.at("no bristle")
        self.play(FadeIn(label("no bristle", VIOLET, 3.2, -3.2, 26)), run_time=.4)
        self.finish()


class S08Overgrowth(SpokenScene):
    def construct(self):
        title = head("Fly brain · failed fate control")
        c = cell([0, 0, 0], 1.3, GREY)
        self.at("Back in the fly brain")
        self.play(FadeIn(title), FadeIn(c), run_time=.6)
        clones = VGroup(*[cell([x, y, 0], .65, RED, .25)
                           for x, y in ((-1, .8), (1, .8), (-1, -.8), (1, -.8))])
        self.at("may keep behaving like a stem cell")
        self.play(ReplacementTransform(c, clones), run_time=.9)
        cases = VGroup(label("Prospero loss", RED, -3.3, 2.1, 28),
                       label("Brat loss · mainly type II", RED, 3.3, 2.1, 26))
        self.at("guard different cells")
        self.play(FadeOut(clones), FadeIn(cases), run_time=.6)
        gmc = chip("ganglion mother cell", GREEN, size=24).move_to([-3.3, .8, 0])
        tumor1 = VGroup(*[cell([-4+i*.7, -1, 0], .3, RED, .35) for i in range(3)],
                        label("tumour growth", RED, -3.3, -2, 26))
        self.at("Without prospero")
        self.play(FadeIn(gmc), run_time=.4)
        self.at("tumors arise")
        self.play(FadeIn(tumor1, scale=.4), GrowArrow(arr([-3.3, .3, 0], [-3.3, -.5, 0], RED, 4)), run_time=.8)
        ip = VGroup(chip("intermediate progenitor", GREY, size=22),
                    label("fails to mature", RED, 0, -.7, 24)).arrange(DOWN, buff=.2).move_to([3.3, .7, 0])
        tumor2 = VGroup(*[cell([2.6+i*.7, -1, 0], .3, RED, .35) for i in range(3)],
                        label("tumour growth", RED, 3.3, -2, 26))
        self.at("Without brat")
        self.play(FadeIn(ip), run_time=.5)
        self.at("mainly from intermediate progenitors")
        self.play(FadeIn(tumor2, scale=.4), GrowArrow(arr([3.3, -.05, 0], [3.3, -.5, 0], RED, 4)), run_time=.7)
        # Swap to the normal sequence so mutant proliferation cannot be mistaken for normal output.
        self.at("These progenitors normally")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.4)
        normal = VGroup(head("Fly type II lineage"), label("normal", GREY, -3.2, 2.5, 26))
        nb = chip("neuroblast", BLUE, size=26).move_to([-4.7, 1.5, 0])
        progen = chip("intermediate progenitor", GREY, size=24).move_to([-3.2, .1, 0])
        failed = VGroup(label("Brat loss", RED, 3.2, 2.5, 26),
                        label("failed maturation", RED, 3.2, 1.5, 24))
        expansion = VGroup(*[cell([x, y, 0], .4, RED, .3)
                            for x, y in ((2.4, .2), (4, .2), (2.4, -1), (4, -1))])
        self.play(FadeIn(normal), FadeIn(nb), FadeIn(progen), FadeIn(failed),
                  FadeIn(expansion, scale=.5),
                  GrowArrow(arr([-4.7, 1, 0], [-3.2, .6, 0], GREY, 4)), run_time=.5)
        lineage = VGroup()
        self.at("divide several times")
        for x in (-5, -3.2, -1.4):
            node = cell([x, -1.8, 0], .4, GREEN)
            path = arr([-3.2, -.4, 0], [x, -1.3, 0], GREY, 3)
            lineage.add(node, path)
            self.play(FadeIn(node), GrowArrow(path), Indicate(progen, color=GREY, scale_factor=1.05), run_time=.35)
        self.at("each time making")
        self.play(FadeIn(label("ganglion mother cells", GREEN, -3.2, -2.8, 26)),
                  FadeIn(label("self-renewing expansion", RED, 3.2, -2.8, 24)),
                  expansion.animate.scale(1.1), run_time=.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        boundary = VGroup(head("Mammals"), label("division plane → fate?", GREY, 0, .7, 36),
                          label("less reliable", TEXT, 0, -.5, 32))
        self.at("In mammals")
        self.play(FadeIn(boundary), run_time=.6)
        mother = cell([-2, 0, 0], 2.2, BLUE)
        title = head("Fly neuroblast · type I")
        self.at("The fly rule")
        self.play(FadeOut(boundary), FadeIn(mother), FadeIn(title), run_time=.6)
        sp = spindle()
        cres = basal([-2, 0, 0], 2.2)
        polar = VGroup(label("apical", GOLD, -5.2, 2.2, 24), label("basal", GREY, -5.2, -2.2, 24))
        cargo = chip("basal cargo", TEXT, size=28).move_to([3, -1.6, 0])
        self.at("Polarity and spindle alignment")
        self.play(Create(sp), Create(cres), FadeIn(polar), FadeIn(cargo), run_time=.7)
        nb, gmc = neural_pair()
        self.at("One daughter keeps")
        self.play(FadeOut(sp), ReplacementTransform(mother, nb), FadeIn(gmc),
                  ReplacementTransform(cres, basal([-2, -1.8, 0], .8)),
                  ReplacementTransform(cargo, chip("renewal", BLUE, size=30).move_to([3, 1, 0])), run_time=.8)
        self.at("The other moves")
        daughters = VGroup(cell([.8, -1.8, 0], .5, GREEN), cell([2.4, -1.8, 0], .5, GREEN))
        self.play(GrowArrow(arr([-1, -1.8, 0], [.1, -1.8, 0], GREEN, 4)), FadeIn(daughters),
                  FadeIn(label("neurons or glia", GREEN, 2, -3, 26)), run_time=.8)
        self.finish()


class S07End(EndCard):
    LINE = ("Asymmetric division keeps\na neural stem cell while producing\n"
            "differentiating progeny.")
