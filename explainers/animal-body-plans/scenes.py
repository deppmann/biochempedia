"""Animal body plans: characters describe, genes test  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the blastopore (first opening of the embryonic gut)
  GREEN  = mouth
  RED    = anus, and a crossed-out prediction
  BLUE   = Spiralia (and the animals in it once regrouped)
  ORANGE = Ecdysozoa (nematodes and arthropods once regrouped)
  TEAL   = independent evidence (genes, chromosomes)
  GOLD   = the film's take-home rule
  GREY   = grades, bins, outlines, de-emphasized labels
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bin_box(w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.07)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=6))


class S00Title(TitleCard):
    LESSON = "Animal body plans"
    TITLE = "Body plans describe, genes test"


# ---------------------------------------------------------------------------------------------
class S01Snail(SpokenScene):
    def construct(self):
        head = T("Slipper snail embryo, Crepidula", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.0)
        # timeline
        line = Arrow([-6.0, -0.2, 0], [6.1, -0.2, 0], color=GREY, stroke_width=4, buff=0, tip_length=0.22)
        t0 = Line([-5.2, -0.45, 0], [-5.2, 0.05, 0], color=GREY, stroke_width=4)
        t1 = Line([3.2, -0.45, 0], [3.2, 0.05, 0], color=GREY, stroke_width=4)
        l0 = T("fertilization", 24, GREY).next_to(t0, DOWN, buff=0.15)
        l1 = T("about 12 days", 24, GREY).next_to(t1, DOWN, buff=0.15)
        self.play(Create(line), FadeIn(t0), FadeIn(l0), run_time=0.7)
        self.at("makes its mouth")
        bl = bchip("first gut opening", YELLOW, 26).move_to([-3.4, 1.9, 0])
        mouth = bchip("mouth", GREEN, 28).move_to([-3.4, 0.5, 0])
        a1 = arr(bl.get_bottom(), mouth.get_top(), YELLOW)
        self.play(FadeIn(bl, shift=DOWN * 0.1), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(mouth), run_time=0.6)
        self.at("anus appears")
        self.play(FadeIn(t1), FadeIn(l1), run_time=0.4)
        anus = bchip("anus", RED, 28).move_to([3.2, 0.5, 0])
        self.play(FadeIn(anus, scale=0.9), run_time=0.5)
        self.at("different set of cells")
        other = bchip("different cells", GREY, 26).move_to([3.2, 1.9, 0])
        a2 = arr(other.get_bottom(), anus.get_top(), GREY)
        self.play(FadeIn(other), GrowArrow(a2), run_time=0.6)
        self.at("two great groups")
        g1 = bchip("protostomes", BLUE, 28).move_to([-2.2, -2.0, 0])
        g2 = bchip("deuterostomes", ORANGE, 28).move_to([2.2, -2.0, 0])
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.7)
        self.at("Does that sorting work")
        q = T("Does that sorting work?", 44, GOLD, font=TITLE_FONT).move_to([0, -3.2, 0])
        self.play(Write(q), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rule(SpokenScene):
    def construct(self):
        head = T("Karl Grobben, 1908: sort bilaterians by the blastopore", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.0)
        self.at("blastopore")
        bl = bchip("blastopore: first gut opening", YELLOW, 28).move_to([0, 0.7, 0])
        self.play(FadeIn(bl, scale=0.9), run_time=0.6)
        # two columns
        colL = T("Protostomes: mouth first", 30, BLUE, weight=BOLD).move_to([-3.4, 2.3, 0])
        colR = T("Deuterostomes: mouth second", 30, ORANGE, weight=BOLD).move_to([3.4, 2.3, 0])
        self.at("In protostomes")
        self.play(FadeIn(colL), run_time=0.6)
        mL = bchip("mouth", GREEN, 30).move_to([-3.4, -1.0, 0])
        aL = arr([-1.6, 0.3, 0], mL.get_top() + UP * 0.05, YELLOW)
        self.at("the blastopore becomes the mouth")
        self.play(GrowArrow(aL), FadeIn(mL), run_time=0.8)
        self.at("In deuterostomes")
        self.play(FadeIn(colR), run_time=0.6)
        mR = bchip("mouth", GREEN, 30).move_to([2.4, -1.0, 0])
        sep = T("forms separately", 24, GREY).next_to(mR, DOWN, buff=0.25)
        self.at("the mouth forms separately")
        self.play(FadeIn(mR), FadeIn(sep), run_time=0.7)
        anR = bchip("anus", RED, 30).move_to([4.7, -1.0, 0])
        aR = arr([1.6, 0.3, 0], anR.get_top() + UP * 0.05, YELLOW)
        often = T("often", 24, YELLOW).next_to(aR, RIGHT, buff=0.1).shift(UP * 0.1)
        self.at("often becomes the anus")
        self.play(GrowArrow(aR), FadeIn(anR), FadeIn(often), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Test(SpokenScene):
    def construct(self):
        head = T("Crepidula fornicata, 2015", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=0.9)
        self.at("checked the rule")
        sn = bchip("slipper snail: Crepidula fornicata", TEAL, 30).move_to([0, 1.2, 0])
        rl = bchip("does the blastopore become the mouth?", YELLOW, 28).move_to([0, -0.4, 0])
        self.play(FadeIn(sn, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.6)
        self.at("injected fluorescent tracers")
        self.play(FadeOut(sn), FadeOut(rl), run_time=0.4)
        tr = bchip("fluorescent tracer", TEAL, 26).move_to([-4.4, 1.6, 0])
        cell = bchip("chosen cell", GREY, 26).move_to([-4.4, 0.0, 0])
        a = arr(tr.get_bottom(), cell.get_top(), TEAL)
        self.play(FadeIn(tr), run_time=0.5)
        self.play(GrowArrow(a), FadeIn(cell), run_time=0.6)
        self.at("followed the descendants")
        desc = bchip("descendants, followed", TEAL, 26).move_to([-4.4, -1.7, 0])
        a2 = arr(cell.get_bottom(), desc.get_top(), TEAL)
        self.play(GrowArrow(a2), FadeIn(desc), run_time=0.7)
        # result
        bl = bchip("blastopore", YELLOW, 26).move_to([0.3, 0.9, 0])
        mouth = bchip("mouth", GREEN, 26).move_to([3.4, 0.9, 0])
        self.at("The blastopore became the mouth")
        self.play(FadeIn(bl), run_time=0.4)
        self.play(GrowArrow(arr(bl.get_right(), mouth.get_left(), YELLOW)), FadeIn(mouth), run_time=0.6)
        self.at("anus formed late")
        oth = bchip("other cells", GREY, 26).move_to([0.3, -1.0, 0])
        anus = bchip("anus, formed late", RED, 26).move_to([3.4, -1.0, 0])
        self.play(FadeIn(oth), run_time=0.4)
        self.play(GrowArrow(arr(oth.get_right(), anus.get_left(), GREY)), FadeIn(anus), run_time=0.6)
        self.at("protostomic by fate map")
        ver = bchip("protostomic by fate map", GOLD, 30).move_to([2.0, -2.6, 0])
        self.play(FadeIn(ver, shift=UP * 0.1), run_time=0.6)
        # hedges: clear the stage
        self.at("does not tell us")
        everything = Group(*[m for m in self.mobjects if m is not head])
        h1 = T("This snail only.", 36, GOLD, font=TITLE_FONT).move_to([0, 0.9, 0])
        h2 = T("Its wider group, the spiralians, is not covered.", 30, TEXT).move_to([0, -0.1, 0])
        self.play(FadeOut(everything), run_time=0.5)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.6)
        self.at("not a reliable test")
        h3 = T("Blastopore fate is not a reliable test of the major clades.", 30, RED).move_to([0, -1.5, 0])
        self.play(FadeIn(h3, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
BIN_X = [-4.4, 0.0, 4.4]


def build_bins():
    """three columns by body cavity; returns (group, dict of chip placements)."""
    names = ["acoelomate", "pseudocoelomate", "coelomate"]
    boxes, labels = [], []
    for x, n in zip(BIN_X, names):
        b = bin_box(4.1, 4.2).move_to([x, -0.4, 0])
        l = T(n, 30, TEXT, weight=BOLD).move_to([x, 1.2, 0])
        boxes.append(b); labels.append(l)
    return boxes, labels


class S04Grades(SpokenScene):
    def construct(self):
        head = T("Libbie Hyman: bilaterians sorted by body cavity", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.0)
        boxes, labels = build_bins()
        sub = [T("tissue fills the space", 22, GREY), T("fluid cavity, partial lining", 22, GREY),
               T("cavity lined by mesoderm", 22, GREY)]
        self.at("volumes")
        bk = bchip("The Invertebrates, volumes 2 and 3 (1951)", GOLD, 30).move_to([0, 0.3, 0])
        self.play(FadeIn(bk, shift=DOWN * 0.1), run_time=0.6)
        self.at("ordered the bilaterians")
        self.play(FadeOut(bk), *[Create(b) for b in boxes], *[FadeIn(l) for l in labels], run_time=0.8)
        self.at("have tissue filling")
        sub[0].move_to([BIN_X[0], 0.55, 0])
        self.play(FadeIn(sub[0]), run_time=0.4)
        c0 = bchip("planarian", GREY, 28).move_to([BIN_X[0], -0.7, 0])
        self.at("a planarian flatworm")
        self.play(FadeIn(c0, shift=DOWN * 0.1), run_time=0.5)
        self.at("without a complete")
        sub[1].move_to([BIN_X[1], 0.55, 0])
        self.play(FadeIn(sub[1]), run_time=0.4)
        c1 = bchip("C. elegans", GREY, 28).move_to([BIN_X[1], -0.7, 0])
        self.at("the nematode")
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.at("have a cavity lined")
        sub[2].move_to([BIN_X[2], 0.55, 0])
        self.play(FadeIn(sub[2]), run_time=0.4)
        c2 = bchip("earthworm", GREY, 28).move_to([BIN_X[2], -0.7, 0])
        self.at("as in the earthworm")
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.5)
        self.at("form a grade")
        g = T("a grade: a shared level of organization", 32, GOLD, font=TITLE_FONT).move_to([0, -3.1, 0])
        self.play(Write(g), run_time=1.0)
        self.finish()


class S05Clade(SpokenScene):
    def construct(self):
        head = T("Grade or clade?", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.add(head)
        boxes, labels = build_bins()
        sub = [T("tissue fills the space", 22, GREY), T("fluid cavity, partial lining", 22, GREY),
               T("cavity lined by mesoderm", 22, GREY)]
        for s, x in zip(sub, BIN_X):
            s.move_to([x, 0.55, 0])
        c0 = bchip("planarian", GREY, 28).move_to([BIN_X[0], -0.7, 0])
        c1 = bchip("C. elegans", GREY, 28).move_to([BIN_X[1], -0.7, 0])
        c2 = bchip("earthworm", GREY, 28).move_to([BIN_X[2], -0.7, 0])
        self.add(*boxes, *labels, *sub, c0, c1, c2)
        self.wait(0.3)
        self.at("A clade is different")
        defn = T("clade: an ancestor and all of its descendants", 32, GOLD, font=TITLE_FONT).move_to([0, -3.1, 0])
        self.play(Write(defn), run_time=1.2)
        self.at("In 1997")
        yr = T("1997: 18S ribosomal RNA gene, many animals", 30, TEAL).move_to([0, -3.1, 0])
        self.play(ReplacementTransform(defn, yr), run_time=0.7)
        self.at("Nematodes grouped with arthropods")
        arth = bchip("arthropod", GREY, 28).move_to([BIN_X[2], -1.9, 0])
        self.play(FadeIn(arth, shift=DOWN * 0.1), run_time=0.5)
        link = CurvedArrow(c1.get_bottom() + DOWN * 0.05, arth.get_left() + LEFT * 0.05, angle=TAU / 6, color=ORANGE, stroke_width=6)
        self.play(Create(link), c1[1].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.16),
                  c1[2].animate.set_color(ORANGE), arth[1].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.16),
                  arth[2].animate.set_color(ORANGE), run_time=0.8)
        self.at("a cuticle so the group")
        mol = T("both moult a cuticle", 28, ORANGE).move_to([0, -3.1, 0])
        self.play(FadeOut(yr), FadeIn(mol, shift=UP * 0.1), run_time=0.5)
        self.at("so the group is called")
        # regroup into two rows
        top_y, bot_y = 1.5, -1.5
        n0 = bchip("flatworm", BLUE, 32).move_to([-1.6, top_y, 0])
        n2 = bchip("annelid", BLUE, 32).move_to([1.4, top_y, 0])
        n1 = bchip("nematode", ORANGE, 32).move_to([-1.6, bot_y, 0])
        n3 = bchip("arthropod", ORANGE, 32).move_to([1.6, bot_y, 0])
        eco = T("Ecdysozoa", 34, ORANGE, weight=BOLD).move_to([-5.1, bot_y, 0])
        old = VGroup(*boxes, *labels, *sub, link, mol, yr)
        self.play(FadeOut(VGroup(*boxes, *labels, *sub, link, mol)), ReplacementTransform(c0, n0), ReplacementTransform(c2, n2),
                  ReplacementTransform(c1, n1), ReplacementTransform(arth, n3), run_time=1.3)
        self.play(FadeIn(eco), run_time=0.5)
        self.at("Flatworms sit inside")
        spi = T("Spiralia", 34, BLUE, weight=BOLD).move_to([-5.1, top_y, 0])
        self.play(FadeIn(spi), run_time=0.5)
        self.at("and molluscs")
        n4 = bchip("mollusc", BLUE, 32).move_to([4.0, top_y, 0])
        self.play(FadeIn(n4, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        head = T("Test the grouping with independent evidence", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.0)
        self.at("body cavity describes a grade")
        g = bchip("body cavity: describes a grade", GREY, 30).move_to([-3.2, 1.8, 0])
        c = bchip("not a clade", RED, 30).move_to([3.2, 1.8, 0])
        self.play(FadeIn(g), run_time=0.6)
        self.play(FadeIn(c), run_time=0.6)
        self.at("secondary simplification")
        fw = bchip("flatworm: acoelomate", BLUE, 28).move_to([-3.2, 0.4, 0])
        note = T("may be a secondary simplification", 26, TEXT).move_to([2.2, 0.7, 0])
        deb = T("ancestral state still debated", 24, GREY).move_to([2.2, 0.05, 0])
        self.play(FadeIn(fw), run_time=0.5)
        self.play(FadeIn(note), FadeIn(deb), run_time=0.7)
        self.at("hundreds of genes")
        self.play(FadeOut(VGroup(g, c, fw, note, deb)), run_time=0.5)
        e1 = bchip("hundreds of genes", TEAL, 28).move_to([-4.0, 1.5, 0])
        e2 = bchip("many species", TEAL, 28).move_to([-4.0, 0.0, 0])
        res = bchip("does the grouping survive?", GOLD, 30).move_to([2.6, 0.8, 0])
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.6)
        self.play(GrowArrow(arr(e1.get_right(), res.get_left() + UP * 0.1, TEAL)),
                  GrowArrow(arr(e2.get_right(), res.get_left() + DOWN * 0.1, TEAL)), FadeIn(res), run_time=0.8)
        self.at("which genes share chromosomes")
        e3 = bchip("which genes share chromosomes", TEAL, 28).move_to([-2.0, -1.2, 0])
        self.play(FadeIn(e3), GrowArrow(arr(e3.get_right(), res.get_bottom() + DOWN * 0.02, TEAL)), run_time=0.8)
        self.at("characters describe animals")
        keep = VGroup(T("Body-plan characters describe animals.", 34, TEXT, font=TITLE_FONT),
                      T("Independent evidence tests their ancestry.", 34, GOLD, font=TITLE_FONT)).arrange(DOWN, buff=0.3).move_to([0, -2.9, 0])
        self.play(FadeIn(keep[0], shift=UP * 0.1), run_time=0.6)
        self.at("Independent evidence tests")
        self.play(FadeIn(keep[1], shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Body-plan characters describe animals; independent evidence tests their ancestry."
