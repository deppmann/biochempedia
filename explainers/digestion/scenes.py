"""Digestion: the master switch of digestion  (Biochemistrypedia explainer)

Timed to the SPOKEN words of the lesson's own slide clips (word timestamps in audio/words.json).

COLOR MAP (one color per concept, whole video)
  GREY   = a zymogen: dormant, inactive precursor (chip with a small "pro" tab); also frames and labels
  BLUE   = an active enzyme (protease, pepsin, chymotrypsin, elastase ...)
  GOLD   = trypsin, the master switch (the only gold thing besides the title rule)
  GREEN  = protein / substrate: the thing that gets cut
  YELLOW = the bond that is about to be broken (cut site)
  WATER  = water (periwinkle) and the H and OH it donates
  TRIG   = a trigger that wakes a zymogen (pink: low pH, enteropeptidase)
  RED    = damage, a missing piece, a lock
No molecular structures are drawn: chips, bars, arrows and compartments only.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

WATER = "#9AA8FF"   # periwinkle: distinct from the cyan of BLUE enzymes
TRIG = "#E57BC4"    # pink: the trigger that wakes a zymogen


# --------------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------------
def tab_for(box):
    """The little pro-piece that keeps a zymogen dormant (sits on the top edge, right side)."""
    t = RoundedRectangle(corner_radius=0.05, width=0.42, height=0.17, stroke_width=0,
                         fill_color=GREY, fill_opacity=1)
    return t.move_to(box.get_top() + RIGHT * (box.width / 2 - 0.5))


def solid(c, color):
    """Make a chip's box opaque (the 16% tint blended onto the background) so things behind it are hidden."""
    c[0].set_fill(interpolate_color(ManimColor(BG), ManimColor(color), 0.16), 1)
    return c


class Node:
    """A labelled chip that can be a dormant zymogen (grey, with a pro-tab) or an active enzyme."""

    def __init__(self, name, color=GREY, size=24, zymogen=True, anchor=None, pad=0.22):
        self.size, self.anchor, self.pad = size, anchor, pad
        c = solid(chip(name, color, size, pad=pad), color)
        self.box, self.label = c[0], c[1]
        self.tab = tab_for(self.box) if zymogen else None

    @property
    def group(self):
        return VGroup(*[m for m in (self.box, self.label, self.tab) if m is not None])

    def place(self, x, y):
        self.group.shift(np.array([x, y, 0]) - self.box.get_center())
        return self

    def place_left(self, x_left, y):
        self.group.shift(np.array([x_left - self.box.get_left()[0], y - self.box.get_center()[1], 0]))
        return self

    def _new_chip(self, name, color):
        new = solid(chip(name, color, self.size, pad=self.pad), color).move_to(self.box.get_center())
        if self.anchor == "left":
            new.align_to(self.box, LEFT)
        return new

    def to_active(self, name, color=BLUE):
        """Pro-tab pops off, chip turns on. Returns the animations."""
        new = self._new_chip(name, color)
        anims = [Transform(self.box, new[0]), FadeOut(self.label), FadeIn(new[1])]
        self.label = new[1]
        if self.tab is not None:
            anims.append(self.tab.animate.shift(UP * 0.55 + RIGHT * 0.45).set_opacity(0))
        return anims

    def to_zymogen(self, name):
        """Back to a dormant zymogen (grey, tab on)."""
        new = self._new_chip(name, GREY)
        anims = [Transform(self.box, new[0]), FadeOut(self.label), FadeIn(new[1])]
        self.label = new[1]
        newtab = tab_for(new[0])
        if self.tab is not None:
            anims.append(FadeOut(self.tab))
        anims.append(FadeIn(newtab))
        self.tab = newtab
        return anims


def pulse(n, color, s=1.1):
    """Emphasise a Node without flooding its opaque box with color (Indicate would hide the label):
    the outline thickens and the label takes the color, then both return."""
    c = n.box.get_center()
    anims = [n.box.animate(rate_func=there_and_back).scale(s, about_point=c).set_stroke(color, width=5),
             n.label.animate(rate_func=there_and_back).scale(s, about_point=c).set_color(color)]
    if n.tab is not None:
        anims.append(n.tab.animate(rate_func=there_and_back).scale(s, about_point=c))
    return AnimationGroup(*anims)


def arr(a, b, color=GOLD, w=4.5):
    return Arrow(np.array(a), np.array(b), buff=0.06, color=color, stroke_width=w,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.2, max_stroke_width_to_length_ratio=12)


def bar(n=4, seg_w=0.4, h=0.3, color=GREEN):
    """A protein shown as a segmented bar (blocks in a row, not a structure)."""
    segs = VGroup(*[RoundedRectangle(corner_radius=0.06, width=seg_w, height=h, stroke_width=0,
                                     fill_color=color, fill_opacity=0.9) for _ in range(n)])
    return segs.arrange(RIGHT, buff=0.04)


def spread(b, k=0.2):
    """A copy of a bar with its segments pulled apart and tilted (it has been cut up)."""
    c = b.copy()
    n = len(c)
    for j, s in enumerate(c):
        s.shift(RIGHT * (j - (n - 1) / 2) * k + UP * (0.13 if j % 2 else -0.13))
        s.rotate(0.3 if j % 2 else -0.3)
    return c


def lock_icon(color=RED, s=1.5):
    body = RoundedRectangle(corner_radius=0.03, width=0.3 * s, height=0.22 * s, stroke_width=0,
                            fill_color=color, fill_opacity=1)
    sh = Arc(radius=0.09 * s, start_angle=0, angle=PI, color=color, stroke_width=3.5).next_to(body, UP, buff=-0.01)
    return VGroup(sh, body)


def ghost_of(node, color=RED):
    """Dashed red outline + cross where a missing protein would be."""
    r = RoundedRectangle(corner_radius=0.14, width=node.box.width, height=node.box.height,
                         stroke_color=color, stroke_width=3, fill_opacity=0).move_to(node.box)
    d = DashedVMobject(r, num_dashes=28)
    x = Cross(r, stroke_color=color, stroke_width=6, scale_factor=0.85)
    return VGroup(d, x)


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Digestion"
    TITLE = "The master switch of digestion"


# --------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """How do you make a shredder without shredding the factory?  Zymogens."""

    def construct(self):
        head = T("The self-digestion problem", 38, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.at("Here is the central puzzle")
        self.play(Write(head), run_time=1.2)

        # --- the enzymes really can tear protein apart -------------------------------------------
        food = bar(7, 0.5, 0.34).move_to([3.5, -0.3, 0])
        food_lbl = T("dietary protein", 26, GREEN).next_to(food, DOWN, buff=0.3)
        prot = chip("protease", BLUE, 26).move_to([3.5, 1.3, 0])
        self.at("Your digestive enzymes are powerful enough")
        self.play(FadeIn(food), FadeIn(food_lbl), FadeIn(prot, shift=DOWN * 0.2), run_time=0.8)
        self.at("tear proteins apart")
        self.play(prot.animate.move_to([3.5, 0.45, 0]), run_time=0.35)
        self.play(Transform(food, spread(food, 0.3)), run_time=0.7)

        # --- ...but the cell that makes them is itself protein -----------------------------------
        self.at("yet the cells that make them")
        self.play(FadeOut(food), FadeOut(food_lbl), FadeOut(prot), run_time=0.4)
        cell = Ellipse(width=5.6, height=3.9, color=GREY, stroke_width=5).move_to([-3.3, -0.35, 0])
        cell.set_fill(GREY, 0.06)
        cell_lbl = T("pancreatic cell", 28).move_to([-3.3, 2.05, 0])
        bars_in = VGroup(*[bar(4, 0.38, 0.3).move_to(p) for p in
                           [[-4.35, 0.75, 0], [-2.3, 0.75, 0], [-4.35, -1.6, 0], [-2.3, -1.6, 0]]])
        bars_ok = bars_in.copy()
        self.play(Create(cell), FadeIn(cell_lbl), FadeIn(bars_in, lag_ratio=0.2), run_time=1.3)
        self.at("built from protein")
        tag = T("built from protein", 28, GREEN).move_to([-3.3, -2.85, 0])
        self.play(FadeIn(tag), Indicate(bars_in, color=GREEN, scale_factor=1.06), run_time=1.0)

        # --- the cell makes shredders: it digests itself ------------------------------------------
        self.at("manufacture")
        self.play(FadeOut(tag), run_time=0.3)
        shred = [Node("protease", BLUE, 22, zymogen=False).place(x, -0.45) for x in (-5.05, -3.3, -1.55)]
        self.play(*[FadeIn(n.group, scale=0.5) for n in shred], lag_ratio=0.3, run_time=0.8)
        self.at("molecular shredder")
        self.play(*[pulse(n, BLUE, 1.12) for n in shred], run_time=0.8)
        self.at("without shredding the factory")
        hurt = T("the cell digests itself", 28, RED).move_to([-3.3, -2.85, 0])
        self.play(Transform(bars_in, spread(bars_in, 0.22)), cell.animate.set_stroke(RED, 5),
                  FadeIn(hurt), run_time=1.1)

        # --- the answer: zymogens ----------------------------------------------------------------
        self.at("The answer is the zymogen")
        self.play(Transform(bars_in, bars_ok), cell.animate.set_stroke(GREY, 5), FadeOut(hurt),
                  *sum([n.to_zymogen("zymogen") for n in shred], []), run_time=1.0)
        self.at("an inactive precursor")
        defn = T("zymogen: an inactive precursor", 34, t2c={"zymogen": GREY}, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(defn, shift=UP * 0.15), run_time=0.7)
        self.at("folded but dormant form")
        self.play(*[pulse(n, TEXT, 1.12) for n in shred], run_time=0.9)

        # --- ship it out; switch it on at the destination ----------------------------------------
        self.at("ships it out")
        lumen = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.4, height=4.0, color=GREY, stroke_width=3),
                               num_dashes=60).move_to([3.5, -0.05, 0])
        lumen_lbl = T("gut lumen", 26, GREY).move_to([3.5, 1.68, 0])
        food2 = bar(7, 0.5, 0.34).move_to([3.5, -1.1, 0])
        food2_lbl = T("dietary protein", 24, GREEN).move_to([3.5, -1.72, 0])
        self.play(FadeIn(lumen), FadeIn(lumen_lbl), FadeIn(food2), FadeIn(food2_lbl), run_time=0.4)
        targets = [(2.05, 0.75), (4.95, 0.75), (3.5, -0.1)]
        self.play(*[n.group.animate.shift(np.array([tx, ty, 0]) - n.box.get_center())
                    for n, (tx, ty) in zip(shred, targets)], run_time=0.8)
        self.at("switches it on")
        self.play(*sum([n.to_active("protease", BLUE) for n in shred], []), run_time=0.9)
        self.at("where digestion should happen")
        self.play(Transform(food2, spread(food2, 0.2)), *[pulse(n, BLUE) for n in shred],
                  run_time=1.2)

        # --- the design principle recurs ----------------------------------------------------------
        self.at("This single design principle")
        everything = Group(*[m for m in self.mobjects])
        self.play(FadeOut(everything), run_time=0.8)
        dp = T("design principle", 26, GREY).move_to([0, 2.0, 0])
        self.play(FadeIn(dp), run_time=0.5)
        self.at("activation only where and when needed")
        main = T("activation only\nwhere and when needed", 50, t2c={"where": BLUE, "when": BLUE},
                 line_spacing=0.9).move_to([0, 0.55, 0])
        self.play(Write(main), run_time=1.6)
        self.at("recurs everywhere in physiology")
        rec = T("the same principle recurs", 30, GREY).move_to([0, -0.9, 0])
        self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.6)
        self.at("blood clotting")
        c1 = Node("blood clotting", GREY, 28, zymogen=False).place(-2.5, -1.9)
        self.play(FadeIn(c1.group, shift=UP * 0.15), run_time=0.6)
        self.at("apoptosis")
        c2 = Node("apoptosis", GREY, 28, zymogen=False).place(2.5, -1.9)
        self.play(FadeIn(c2.group, shift=UP * 0.15), run_time=0.6)
        self.at("Keep it in mind")
        self.play(Indicate(main, color=BLUE, scale_factor=1.06), run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------------------------
CX = 1.9   # centre of the substrate pair in each row


def hrow(y, enz, a, b, bond):
    e = chip(enz, BLUE, 26)
    e.move_to([-6.25 + e.width / 2, y, 0])
    A = chip(a, GREEN, 24)
    A.move_to([CX - 0.85 - A.width / 2, y, 0])
    B = chip(b, GREEN, 24)
    B.move_to([CX + 0.85 + B.width / 2, y, 0])
    link = Line(A.get_right(), B.get_left(), color=YELLOW, stroke_width=8)
    lbl = T(bond, 22, YELLOW).move_to([CX, y - 0.62, 0])
    return dict(y=y, e=e, A=A, B=B, link=link, lbl=lbl)


class S02Water(SpokenScene):
    """Hydrolysis: one reaction, three bond types."""

    def construct(self):
        head = T("One chemical trick, three times", 38, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.at("Notice that digestion is really one chemical trick")
        self.play(Write(head), run_time=1.3)

        # --- generic demonstration of the idea ---------------------------------------------------
        self.at("Hydrolysis means breaking a bond")
        word = T("hydrolysis", 44, font=TITLE_FONT, t2c={"hydro": WATER}).move_to([0, 2.2, 0])
        gA = chip("A", GREEN, 36, pad=0.3).move_to([-1.7, 0.2, 0])
        gB = chip("B", GREEN, 36, pad=0.3).move_to([1.7, 0.2, 0])
        gl = Line(gA.get_right(), gB.get_left(), color=YELLOW, stroke_width=9)
        gl_lbl = T("a bond", 24, YELLOW).move_to([0, -0.5, 0])
        self.play(FadeIn(word, shift=UP * 0.1), FadeIn(gA), FadeIn(gB), Create(gl), FadeIn(gl_lbl), run_time=0.7)
        self.at("breaking a bond")
        self.play(Indicate(gl, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("by inserting water")
        gw = solid(chip("H₂O", WATER, 28), WATER).move_to([0, 1.25, 0])
        self.play(FadeIn(gw), run_time=0.2)
        self.play(gw.animate.move_to([0, 0.2, 0]), FadeOut(gl_lbl), run_time=0.6)
        gH = chip("H", WATER, 28).move_to([-0.55, 0.2, 0])
        gOH = chip("OH", WATER, 28).move_to([0.55, 0.2, 0])
        self.play(FadeOut(gw), FadeIn(gH), FadeIn(gOH), FadeOut(gl), run_time=0.25)
        self.play(gA.animate.shift(LEFT * 0.9), gB.animate.shift(RIGHT * 0.9),
                  gH.animate.move_to([-1.55, 0.2, 0]), gOH.animate.move_to([1.4, 0.2, 0]), run_time=0.7)
        self.at("Proteases attack the peptide bond")
        self.play(FadeOut(VGroup(word, gA, gB, gH, gOH)), run_time=0.3)

        # --- the three rows ---------------------------------------------------------------------
        r1 = hrow(1.75, "proteases", "amino acid", "amino acid", "peptide bond")
        r2 = hrow(0.15, "disaccharidases", "glucose", "glucose", "glycosidic bond")
        r3 = hrow(-1.45, "lipases", "glycerol", "fatty acid", "ester bond")
        rows = [r1, r2, r3]

        def show(r):
            return [FadeIn(r["e"], shift=RIGHT * 0.2), FadeIn(r["A"]), FadeIn(r["B"]), Create(r["link"]),
                    FadeIn(r["lbl"])]

        self.play(*show(r1), run_time=0.7)
        self.at("peptide bond")
        self.play(Indicate(r1["link"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("disaccharidase attack the glycosidic bond")
        self.play(*show(r2), run_time=0.8)
        self.at("glycosidic bond")
        self.play(Indicate(r2["link"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("and lipases attack the ester bond")
        self.play(*show(r3), run_time=0.8)
        self.at("ester bond")
        self.play(Indicate(r3["link"], color=TEXT, scale_factor=1.0), run_time=0.7)

        # --- water caps both ends ---------------------------------------------------------------
        self.at("In every case")
        for r in rows:
            r["water"] = solid(chip("H₂O", WATER, 24), WATER).move_to([CX, r["y"] + 0.75, 0])
        self.play(*[FadeOut(r["lbl"]) for r in rows], *[FadeIn(r["water"]) for r in rows], run_time=0.3)
        self.play(*[r["water"].animate.move_to([CX, r["y"], 0]) for r in rows], run_time=0.7)
        self.at("water donates a hydrogen")
        for r in rows:
            r["H"] = chip("H", WATER, 24).move_to([CX - 0.45, r["y"], 0])
            r["OH"] = r["water"]
            r["A_to"] = r["A"].get_right()[0] - 0.7      # new right edge of A
            r["B_to"] = r["B"].get_left()[0] + 0.7       # new left edge of B
        self.play(*[Transform(r["water"], chip("OH", WATER, 24).move_to([CX + 0.4, r["y"], 0])) for r in rows],
                  *[FadeIn(r["H"]) for r in rows], *[FadeOut(r["link"]) for r in rows], run_time=0.4)
        self.play(*[r["A"].animate.shift(LEFT * 0.7) for r in rows],
                  *[r["H"].animate.move_to([r["A_to"] + 0.12 + r["H"].width / 2, r["y"], 0]) for r in rows],
                  run_time=0.7)
        self.at("and a hydroxyl to the other")
        self.play(*[r["B"].animate.shift(RIGHT * 0.7) for r in rows],
                  *[r["OH"].animate.move_to([r["B_to"] - 0.12 - 0.45, r["y"], 0]) for r in rows], run_time=0.8)
        self.at("capping both freshly broken ends")
        self.play(*[Indicate(r[k], color=WATER, scale_factor=1.25) for r in rows for k in ("H", "OH")], run_time=1.0)

        # --- same logic, different parts ----------------------------------------------------------
        self.at("The substrates look different")
        self.play(*[Indicate(r[k], color=GREEN, scale_factor=1.1) for r in rows for k in ("A", "B")], run_time=0.9)
        self.at("the enzymes are different")
        self.play(*[Indicate(r["e"], color=BLUE, scale_factor=1.1) for r in rows], run_time=0.9)
        self.at("but the logic is identical")
        capbox = SurroundingRectangle(VGroup(*[r[k] for r in rows for k in ("H", "OH")]), color=WATER,
                                      buff=0.06, stroke_width=3, corner_radius=0.15)
        self.play(Create(capbox), *[Indicate(r[k], color=WATER, scale_factor=1.15) for r in rows for k in ("H", "OH")],
                  run_time=1.0)
        self.at("If you understand one row")
        row1_box = SurroundingRectangle(VGroup(r1["e"], r1["A"], r1["B"]), color=GREY, buff=0.2, stroke_width=3,
                                        corner_radius=0.15)
        self.play(FadeOut(capbox), Create(row1_box), run_time=0.7)
        self.at("you understand all three")
        all_box = SurroundingRectangle(VGroup(*[r[k] for r in rows for k in ("e", "A", "B")]), color=GREY,
                                       buff=0.2, stroke_width=3, corner_radius=0.15)
        self.play(Transform(row1_box, all_box), run_time=0.8)

        # --- bottom summary -----------------------------------------------------------------------
        self.at("That bottom summary")
        summ = T("Water provides the H and the OH that cap each broken end", 31,
                 t2c={"Water": WATER, "OH": WATER, " H ": WATER}).move_to([0, -3.15, 0])
        self.play(FadeOut(row1_box), run_time=0.3)
        self.play(FadeIn(summ, shift=UP * 0.15), run_time=0.8)
        self.at("Water provides the H and the OH")
        self.play(*[Indicate(r[k], color=WATER, scale_factor=1.25) for r in rows for k in ("H", "OH")],
                  Indicate(summ, color=WATER, scale_factor=1.04), run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Cascade(SpokenScene):
    """The activation map: pepsinogen by acid; trypsin turns on the rest."""

    def construct(self):
        pan_a = RoundedRectangle(corner_radius=0.2, width=12.6, height=1.85, stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.04).move_to([0, 2.62, 0])
        pan_b = RoundedRectangle(corner_radius=0.2, width=12.6, height=4.85, stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.04).move_to([0, -1.08, 0])
        lab_a = T("stomach", 26, GREY).move_to([-6.0, 2.45, 0], aligned_edge=LEFT)
        lab_b = T("small intestine · pancreatic zymogens", 22, GREY).move_to([-6.0, 0.98, 0], aligned_edge=LEFT)
        self.at("This is the activation map")
        self.play(FadeIn(pan_a), FadeIn(pan_b), FadeIn(lab_a), FadeIn(lab_b), run_time=1.2)

        # --- stomach: low pH switches pepsinogen on ---------------------------------------------
        self.at("In the stomach")
        pepsinogen = Node("pepsinogen", GREY, 26).place(-2.2, 2.45)
        self.play(FadeIn(pepsinogen.group, shift=UP * 0.1), run_time=0.6)
        self.at("low pH converts")
        a1 = arr([-0.8, 2.45, 0], [2.6, 2.45, 0], TRIG)
        ph = chip("low pH", TRIG, 26).move_to([0.9, 3.05, 0])
        self.play(Create(a1), FadeIn(ph, shift=DOWN * 0.1), run_time=0.7)
        self.at("into active pepsin")
        pepsin = chip("pepsin", BLUE, 26).move_to([3.9, 2.45, 0])
        self.play(FadeIn(pepsin, shift=RIGHT * 0.5), run_time=0.9)

        # --- intestine: a family of zymogens ---------------------------------------------------
        self.at("In the small intestine")
        tryp = Node("trypsinogen", GREY, 26).place(0, 0.25)
        chy = Node("chymotrypsinogen", GREY, 26).place(-4.0, -1.6)
        pro = Node("procarboxypeptidase", GREY, 26).place(0.0, -1.6)
        pre = Node("proelastase", GREY, 26).place(4.2, -1.6)
        zs = [tryp, chy, pro, pre]
        self.at("the pancreas delivers")
        self.play(*[FadeIn(n.group, shift=UP * 0.15) for n in zs], lag_ratio=0.35, run_time=2.4)

        # --- trypsin: the master switch -----------------------------------------------------------
        self.at("Watch what trypsin does")
        self.play(pulse(tryp, GOLD), run_time=0.9)
        self.at("switched on")
        self.play(*tryp.to_active("trypsin", GOLD), run_time=0.8)
        fan = []
        for node, nm, pt, phrase in [(chy, "chymotrypsin", chy, "It activates chymotrypsinogen"),
                                     (pro, "carboxypeptidase", pro, "the procarboxypeptidase"),
                                     (pre, "elastase", pre, "and prolastase")]:
            self.at(phrase)
            a = arr([tryp.box.get_center()[0] + (node.box.get_center()[0] - tryp.box.get_center()[0]) * 0.18,
                     tryp.box.get_bottom()[1], 0],
                    [node.box.get_center()[0], node.box.get_top()[1] + 0.02, 0], GOLD)
            fan.append(a)
            self.play(Create(a), run_time=0.5)
            self.play(*node.to_active(nm, BLUE), run_time=0.7)
        self.at("Trypsin is the master switch")
        self.play(pulse(tryp, GOLD, 1.12), run_time=0.7)
        self.at("master switch")
        ms = T("master switch", 28, GOLD).move_to([2.3, 0.25, 0])
        self.play(FadeIn(ms, shift=LEFT * 0.15), run_time=0.6)
        self.at("That single arrow pattern")
        self.play(*[Indicate(a, color=GOLD, scale_factor=1.15) for a in fan], run_time=1.2)
        self.at("one activated enzyme turning on all the others")
        self.play(pulse(tryp, GOLD), *[pulse(n, BLUE, 1.08) for n in (chy, pro, pre)], run_time=1.3)

        # --- the note --------------------------------------------------------------------------
        self.at("the note at the bottom")
        note = T("Note: trypsin activates the others.", 28, t2c={"trypsin": GOLD}).move_to([0, -2.85, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)

        self.at("previews a clinical point")
        self.play(pulse(tryp, GOLD, 1.12), run_time=1.0)

        # --- what if trypsin is missing --------------------------------------------------------
        self.at("Knock out the ability to make trypsin")
        x = Cross(tryp.box, stroke_color=RED, stroke_width=7, scale_factor=0.9)
        self.play(FadeOut(ms), tryp.box.animate.set_stroke(RED, 4), Create(x), run_time=0.8)
        self.at("and the entire downstream cascade never fires")
        resets = (chy.to_zymogen("chymotrypsinogen") + pro.to_zymogen("procarboxypeptidase")
                  + pre.to_zymogen("proelastase"))
        self.play(*resets, *[a.animate.set_opacity(0.18) for a in fan], run_time=1.3)
        self.at("no matter how much of the other zymogens")
        stacks = []
        for n in (chy, pro, pre):
            for k in (1, 2):
                c = n.box.copy().shift(np.array([0.12, -0.12, 0]) * k)
                c.set_z_index(-k)
                stacks.append(c)
        self.play(*[FadeIn(c) for c in stacks], run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
PX = 3.225   # panel centre


def build_tree(cx):
    """enteropeptidase -> trypsinogen -> four zymogens, all dormant. Returns a dict of mobjects."""
    d = {}
    d["panel"] = RoundedRectangle(corner_radius=0.2, width=6.15, height=6.9, stroke_color=GREY, stroke_width=2.5,
                                  fill_color=GREY, fill_opacity=0.03).move_to([cx, 0.05, 0])
    d["ep"] = chip("enteropeptidase", TRIG, 22, pad=0.13).move_to([cx - 1.7, 2.2, 0])
    d["try"] = Node("trypsinogen", GREY, 22, pad=0.13).place(cx - 2.0, -0.45)
    ys = [0.75, -0.05, -0.85, -1.65]
    names = [("chymotrypsinogen", "chymotrypsin"), ("procarboxypeptidase", "carboxypeptidase"),
             ("proelastase", "elastase"), ("procolipase", "colipase")]
    d["tg"] = [Node(z, GREY, 22, anchor="left", pad=0.13).place_left(cx - 0.55, y) for (z, _), y in zip(names, ys)]
    d["act"] = [a for _, a in names]
    d["zy"] = [z for z, _ in names]
    d["ep_arrow"] = arr([cx - 2.0, d["ep"].get_bottom()[1], 0], [cx - 2.0, d["try"].box.get_top()[1] + 0.2, 0], TRIG)
    d["fan"] = [arr([d["try"].box.get_right()[0], d["try"].box.get_center()[1], 0],
                    [t.box.get_left()[0], t.box.get_center()[1], 0], GOLD, w=3.5) for t in d["tg"]]
    return d


class S04Deficiency(SpokenScene):
    """Normal tree versus missing trypsinogen."""

    def construct(self):
        q = T("What if the master switch is missing?", 40, font=TITLE_FONT, t2c={"master switch": GOLD}).move_to([0, 0.3, 0])
        self.at("Put the cascade idea to the test")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)

        # --- left: the normal tree ---------------------------------------------------------------
        self.at("On the left")
        L = build_tree(-PX)
        tl = T("Normal cascade", 30).move_to([-PX, 3.05, 0])
        self.play(FadeOut(q), FadeIn(L["panel"]), FadeIn(tl), run_time=0.8)
        self.at("normal activation tree")
        self.play(FadeIn(L["ep"], shift=DOWN * 0.1), FadeIn(L["try"].group),
                  *[FadeIn(t.group, shift=LEFT * 0.1) for t in L["tg"]], lag_ratio=0.2, run_time=1.8)
        self.at("Enteropeptidase switches on trypsin")
        self.play(Create(L["ep_arrow"]), run_time=0.5)
        self.play(*L["try"].to_active("trypsin", GOLD), run_time=0.7)
        L_arrows = []
        for i, phrase in enumerate(["activates chymotrypsin", "the carboxypeptidases", "elastase",
                                    "and procolipase"]):
            self.at(phrase)
            self.play(Create(L["fan"][i]), run_time=0.4)
            self.play(*L["tg"][i].to_active(L["act"][i], BLUE), run_time=0.6)
            L_arrows.append(L["fan"][i])
        # lipase is secreted already active; colipase is its partner (nothing here shows lipase being activated)
        self.at("the partner lipase")
        lipL = Node("lipase", BLUE, 22, zymogen=False, anchor="left", pad=0.13).place_left(-PX - 0.55, -2.6)
        linkL = Line([-PX - 0.15, L["tg"][3].box.get_bottom()[1], 0], [-PX - 0.15, lipL.box.get_top()[1], 0],
                     color=BLUE, stroke_width=3.5)
        self.play(Create(linkL), FadeIn(lipL.group, shift=UP * 0.1), run_time=0.8)
        self.at("to digest fat")
        helper = T("digests fat", 24, GREY).next_to(lipL.box, RIGHT, buff=0.25)
        self.play(FadeIn(helper, shift=LEFT * 0.1), pulse(lipL, BLUE, 1.12), run_time=0.8)

        # --- right: trypsinogen removed -----------------------------------------------------------
        self.at("On the right")
        R = build_tree(PX)
        tr = T("Trypsinogen deficiency", 30).move_to([PX, 3.05, 0])
        self.play(FadeIn(R["panel"]), FadeIn(tr), FadeIn(R["ep"]), FadeIn(R["try"].group),
                  *[FadeIn(t.group) for t in R["tg"]], run_time=1.2)
        self.at("remove the ability")
        self.play(pulse(R["try"], RED), run_time=0.8)
        self.at("make trypsinogen")
        g = ghost_of(R["try"])
        dash_fan = VGroup(*[Line([R["try"].box.get_right()[0], R["try"].box.get_center()[1], 0],
                                  [t.box.get_left()[0] - 0.42, t.box.get_center()[1], 0],
                                  color=GREY, stroke_width=3).set_opacity(0.3) for t in R["tg"]])
        self.play(FadeOut(R["try"].group), FadeIn(g), FadeIn(dash_fan), run_time=0.8)
        self.at("Now the master switch is gone")
        cap = T("master switch gone", 26, RED).move_to([PX, -3.2, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.at("every downstream zymogen stays locked")
        locks = [lock_icon(s=1.2).move_to([t.box.get_left()[0] - 0.22, t.box.get_center()[1] + 0.02, 0]).set_z_index(5) for t in R["tg"]]
        self.play(*[FadeIn(l, scale=0.5) for l in locks], lag_ratio=0.2, run_time=1.2)
        self.at("no matter how abundant it is")
        stacks = []
        for t in R["tg"]:
            for k in (1, 2):
                c = t.box.copy().shift(np.array([0.11, -0.11, 0]) * k)
                c.set_z_index(-k)
                stacks.append(c)
        self.play(*[FadeIn(c) for c in stacks], run_time=1.0)

        # --- compare: lose one branch / lose trypsin ----------------------------------------------
        self.at("trypsinogen deficiency")
        self.play(R["panel"].animate.set_stroke(RED, 4), run_time=0.7)
        self.at("losing any single other zymogen")
        gl = ghost_of(L["tg"][2])
        self.play(FadeOut(L["tg"][2].group), FadeOut(L["fan"][2]), FadeIn(gl), run_time=0.8)
        self.at("Lose one branch")
        cap1 = T("lose one branch, lose one enzyme", 24).move_to([-PX, -3.2, 0])
        self.play(FadeIn(cap1, shift=UP * 0.1), run_time=0.6)
        self.at("Lose trypsin")
        self.play(FadeOut(cap), Indicate(g, color=RED, scale_factor=1.15), run_time=0.8)
        self.at("protein digestion collapses")
        cap2 = T("protein digestion collapses", 24, RED).move_to([PX, -3.2, 0])
        self.play(FadeIn(cap2, shift=UP * 0.1), *[pulse(t, RED, 1.08) for t in R["tg"][:3]], run_time=1.3)
        # fat digestion: lipase is still active, so it is impaired (not abolished) without colipase
        self.at("while fat digestion")
        lipR = Node("lipase", BLUE, 22, zymogen=False, anchor="left", pad=0.13).place_left(PX - 0.55, -2.6)
        self.play(FadeIn(lipR.group, shift=UP * 0.1), run_time=0.9)
        self.at("falters without colipase")
        tagR = T("slower", 24, RED).next_to(lipR.box, RIGHT, buff=0.25)
        cap3 = T("fat digestion falters", 24, RED).move_to([PX, -3.2, 0])
        self.play(FadeOut(cap2), FadeIn(cap3, shift=UP * 0.1), FadeIn(tagR), pulse(R["tg"][3], RED, 1.1),
                  run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05End(EndCard):
    LINE = "One master switch wakes the whole digestive cascade."
