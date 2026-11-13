"""How bacteria make human insulin.

COLOR MAP
  BLUE   plasmid
  GREEN  intended gene, control DNA, and insulin product
  YELLOW laboratory tools
  RED    selection and warnings
  TEAL   evidence / testing
  GREY   bacteria, readers, and context

All DNA is schematic geometry: blocks and loops, never molecular structure.
"""
from bp_parts import *


PURPLE = "#B58CD9"
LOOP_W = 15


class FilmScene(SpokenScene):
    """SpokenScene whose carried subject visibly settles during narration gaps."""

    def _move_through(self, seconds):
        mob = getattr(self, "moving_subject", None)
        if mob is not None and seconds > 0.35:
            self.play(mob.animate.shift(RIGHT * 0.16), run_time=seconds,
                      rate_func=there_and_back)

    def at(self, phrase, lead=0.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        self._move_through(target - self.elapsed())
        super().at(phrase, lead=lead, nth=nth)

    def finish(self):
        self._move_through(self.narration_s - self.elapsed())
        super().finish()


def arrow(a, b, color=GREY, width=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=0.22, max_tip_length_to_length_ratio=0.35)


def gene_unit(center=ORIGIN, scale=1.0, introns=False, bad_control=False, labels=True):
    """The carried insulin instruction, always rebuilt from this function."""
    control = RoundedRectangle(corner_radius=0.12, width=1.5, height=1.05,
                               stroke_color=RED if bad_control else GREEN, stroke_width=5,
                               fill_color=RED if bad_control else GREEN, fill_opacity=0.16)
    control.move_to(LEFT * 2.55)
    gene = RoundedRectangle(corner_radius=0.14, width=3.6, height=1.3,
                            stroke_color=GREEN, stroke_width=6,
                            fill_color=GREEN, fill_opacity=0.28).move_to(RIGHT * 0.2)
    pieces = VGroup(control, gene)
    if introns:
        for x in (-0.55, 0.7):
            pieces.add(Rectangle(width=0.48, height=1.31, stroke_width=0,
                                 fill_color=GREY, fill_opacity=1).move_to([x, 0, 0]))
    if bad_control:
        stripes = VGroup(*[
            Line([-3.12 + i * 0.28, -0.48, 0], [-2.76 + i * 0.28, 0.48, 0],
                 color=RED, stroke_width=6) for i in range(4)
        ])
        pieces.add(stripes)
    if labels:
        ctl = T("control DNA", 28, RED if bad_control else GREEN).move_to(control)
        ins = T("insulin gene", 32, GREEN, weight=BOLD).move_to(gene)
        ctl.layout_ok = ins.layout_ok = True
        pieces.add(ctl, ins)
    pieces.scale(scale).move_to(center)
    return pieces


def plasmid(center=ORIGIN, radius=2.0, recombinant=True, bad_control=False,
            resistance=False, rotate=0):
    """The carried plasmid loop; green arcs are the inserted instruction."""
    c = np.array(center, dtype=float)
    blue = Arc(radius=radius, start_angle=np.radians(52), angle=np.radians(308),
               arc_center=c, stroke_color=BLUE, stroke_width=LOOP_W)
    parts = VGroup(blue)
    if recombinant:
        green = Arc(radius=radius, start_angle=np.radians(-8), angle=np.radians(60),
                    arc_center=c, stroke_color=GREEN, stroke_width=LOOP_W)
        parts.add(green)
        tab_col = RED if bad_control else GREEN
        tab = RoundedRectangle(corner_radius=0.08, width=0.78, height=0.42,
                               stroke_color=tab_col, stroke_width=4,
                               fill_color=tab_col, fill_opacity=0.55)
        tab.move_to(c + radius * np.array([np.cos(np.radians(52)), np.sin(np.radians(52)), 0]))
        parts.add(tab)
        if bad_control:
            parts.add(Line(tab.get_corner(DL), tab.get_corner(UR), color=RED, stroke_width=6))
    if resistance:
        marker = Arc(radius=radius, start_angle=np.radians(188), angle=np.radians(38),
                     arc_center=c, stroke_color=RED, stroke_width=LOOP_W)
        parts.add(marker)
    if rotate:
        parts.rotate(rotate, about_point=c)
    return parts


def bacterium(center=ORIGIN, width=4.7, height=2.8, with_plasmid=False,
              resistance=False):
    body = RoundedRectangle(corner_radius=height / 2, width=width, height=height,
                            stroke_color=GREY, stroke_width=6,
                            fill_color=GREY, fill_opacity=0.20).move_to(center)
    g = VGroup(body)
    if with_plasmid:
        g.add(plasmid(np.array(center) + LEFT * 0.25, radius=0.72,
                      resistance=resistance))
    return g


def vial(center=ORIGIN, label="insulin", scale=1.0):
    bottle = RoundedRectangle(corner_radius=0.16, width=2.0, height=2.2,
                              stroke_color=GREEN, stroke_width=5,
                              fill_color=GREEN, fill_opacity=0.12)
    cap = Rectangle(width=1.1, height=0.34, stroke_color=GREY, stroke_width=4,
                    fill_color=GREY, fill_opacity=0.25).next_to(bottle, UP, buff=0)
    lab = T(label, 28, GREEN, weight=BOLD).move_to(bottle)
    lab.layout_ok = True
    return VGroup(bottle, cap, lab).scale(scale).move_to(center)


def reader(center=ORIGIN, scale=1.0):
    body = RoundedRectangle(corner_radius=0.22, width=1.35, height=1.75,
                            stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.22)
    eye = Dot(UP * 0.25, radius=0.1, color=TEXT)
    foot = Line(LEFT * 0.42 + DOWN * 0.45, RIGHT * 0.42 + DOWN * 0.45,
                color=GREY, stroke_width=6)
    return VGroup(body, eye, foot).scale(scale).move_to(center)


def predict_world():
    p = plasmid([0, 0.45, 0], radius=2.0, bad_control=True)
    r = reader([-3.6, 0.45, 0], 0.9)
    stop = T("STOP", 30, RED, weight=BOLD).move_to([-3.6, 1.75, 0])
    cell = bacterium([0, 0.45, 0], width=11.0, height=5.4)
    cell.set_z_index(-2)
    return VGroup(p, r, stop, scope_tag("schematic"), cell)


class S01Hook(FilmScene):
    def construct(self):
        cell = bacterium([0, -0.35, 0], width=7.2, height=4.3)
        self.moving_subject = cell
        missing = gene_unit([0, 2.45, 0], 0.63, labels=False)
        missing.set_stroke(opacity=0.55)
        q = T("?", 52, GREEN, weight=BOLD).move_to(missing)
        self.play(FadeIn(cell, scale=0.96), run_time=0.7)
        self.at("human insulin gene")
        self.play(FadeIn(missing), FadeIn(q), run_time=0.65)
        pulse(missing, base=5, amp=2, speed=2.5)
        self.at("How can they")
        prompt = T("How can bacteria make human insulin?", 38, GREEN, font=TITLE_FONT).move_to([0, -3.0, 0])
        self.play(FadeIn(prompt, shift=UP * 0.12), run_time=0.65)
        self.at("Before engineered microbes")
        self.play(FadeOut(VGroup(cell, missing, q, prompt)), run_time=0.45)
        cattle = chip("cattle pancreas", GREY, 32).move_to([-4.7, 0.8, 0])
        pig = chip("pig pancreas", GREY, 32).move_to([-4.7, -0.8, 0])
        old = VGroup(cattle, pig)
        date_old = T("from the 1920s", 30, GREY).move_to([-4.7, 2.25, 0])
        med = vial([0.2, 0, 0], "insulin", 0.9)
        a1, a2 = arrow(cattle.get_right(), med.get_left() + UP * 0.35), arrow(pig.get_right(), med.get_left() + DOWN * 0.35)
        self.play(FadeIn(old, shift=RIGHT * 0.2), FadeIn(date_old), FadeIn(med), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.moving_subject = VGroup(old, med)
        self.at("Then bacteria carrying")
        eng = bacterium([4.45, 0, 0], width=3.4, height=2.45, with_plasmid=True)
        date_new = T("1982 FDA approval", 30, GREEN).move_to([4.35, 2.25, 0])
        self.play(old.animate.shift(LEFT * 0.2).set_opacity(0.35), FadeIn(eng, shift=LEFT * 0.2), FadeIn(date_new), run_time=0.8)
        self.moving_subject = eng
        self.play(Indicate(eng[1], color=GREEN, scale_factor=1.15), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S00Title(TitleCard):
    LESSON = "Genetic engineering"
    TITLE = "How Bacteria Make Human Insulin"


class S02Instruction(FilmScene):
    def construct(self):
        unit = gene_unit([0, 0.2, 0], 1.6, labels=False)
        self.moving_subject = unit
        self.play(FadeIn(unit[1], scale=0.9), run_time=0.7)
        pulse(unit[1], base=6, amp=2.5, speed=2.0)
        self.at("codes for insulin")
        lab = T("insulin gene", 40, GREEN, weight=BOLD).move_to(unit[1])
        lab.layout_ok = True
        self.play(FadeIn(lab), run_time=0.5)
        self.at("same genetic code")
        shared = caption("Nearly all living things use the same genetic code.", color=TEAL)
        self.play(FadeIn(shared), run_time=0.6)
        self.at("most human genes contain introns")
        introns = VGroup(*[Rectangle(width=0.62, height=2.10, stroke_width=0,
                                    fill_color=GREY, fill_opacity=1).move_to([x, 0.2, 0])
                           for x in (-0.75, 0.85)])
        self.play(FadeOut(lab), FadeOut(shared), FadeIn(introns), run_time=0.8)
        ilabs = VGroup(T("intron", 28, GREY).move_to(introns[0]), T("intron", 28, GREY).move_to(introns[1]))
        ilabs[0].layout_ok = ilabs[1].layout_ok = True
        self.play(FadeIn(ilabs), run_time=0.5)
        self.at("human cells cut out")
        self.play(FadeOut(ilabs), FadeOut(introns), unit[1].animate.set_fill(GREEN, 0.34), run_time=0.8)
        self.at("intron -free DNA")
        free = T("intron-free", 36, GREEN).next_to(unit[1], UP, buff=0.35)
        self.play(FadeIn(free), run_time=0.5)
        self.at("bacterial control DNA")
        self.play(FadeIn(unit[0], shift=RIGHT * 0.15), run_time=0.6)
        ctl = T("bacterial control DNA", 30, GREEN).next_to(unit[0], UP, buff=0.25)
        self.play(FadeIn(ctl), run_time=0.5)
        self.at("The gene is the instruction")
        self.play(swap(free, T("instruction", 34, GREEN).move_to(free)), run_time=0.55)
        self.at("control tab helps")
        rd = reader([-5.25, 0.2, 0], 0.78)
        self.play(FadeIn(rd), run_time=0.4)
        self.play(rd.animate.move_to([3.5, 0.2, 0]), run_time=2.2, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Cut(FilmScene):
    def construct(self):
        gene = gene_unit([-3.6, 0.45, 0], 0.72)
        loop = Circle(radius=1.65, color=BLUE, stroke_width=LOOP_W).move_to([3.6, 0.45, 0])
        self.moving_subject = VGroup(gene, loop)
        self.add(gene)
        self.play(Create(loop), run_time=0.7)
        self.at("restriction enzyme")
        tool = chip("restriction enzyme", YELLOW, 30).move_to([0, 2.75, 0])
        self.play(FadeIn(tool, shift=DOWN * 0.2), run_time=0.5)
        marks = VGroup(*[Line([x, 0.05, 0], [x, 0.85, 0], color=YELLOW, stroke_width=7) for x in (-2.5, 3.6)])
        self.at("matching marks")
        self.play(FadeIn(marks), run_time=0.45)
        self.at("Many cuts leave")
        open_loop = Arc(radius=1.65, start_angle=np.radians(18), angle=np.radians(324),
                        arc_center=[3.6, 0.45, 0], stroke_color=BLUE, stroke_width=LOOP_W)
        loose_gene = gene[1].copy().scale(0.88).move_to([-2.85, 0.45, 0])
        self.play(FadeOut(gene), ReplacementTransform(loop, open_loop), Transform(marks[0], loose_gene),
                  FadeOut(marks[1]), tool.animate.move_to([3.6, 2.75, 0]), run_time=0.9)
        self.moving_subject = VGroup(open_loop, loose_gene)
        notches = VGroup(T("⌜", 62, GREEN).move_to(loose_gene.get_left()),
                         T("⌟", 62, GREEN).move_to(loose_gene.get_right()),
                         T("⌞", 62, BLUE).move_to(open_loop.get_start()),
                         T("⌝", 62, BLUE).move_to(open_loop.get_end()))
        notches.layout_ok = True  # complementary notch glyphs intentionally sit on the cut ends
        self.at("sticky ends")
        self.play(FadeIn(notches), FadeOut(tool), run_time=0.6)
        sticky = T("sticky ends", 34, YELLOW).move_to([0, -2.5, 0])
        self.play(FadeIn(sticky), run_time=0.45)
        self.at("shapes show")
        self.play(Indicate(notches, color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.at("do not add information")
        rule = caption("Cuts rearrange information; they do not add it.", color=TEXT)
        self.play(swap(sticky, rule), run_time=0.6)
        bob(loose_gene, amp=0.11, speed=1.6)
        pulse(open_loop, base=LOOP_W, amp=2.5, speed=1.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Join(FilmScene):
    def construct(self):
        open_loop = Arc(radius=2.2, start_angle=np.radians(18), angle=np.radians(324),
                        arc_center=[0, 0.35, 0], stroke_color=BLUE, stroke_width=LOOP_W)
        insert = Arc(radius=2.2, start_angle=np.radians(-18), angle=np.radians(36),
                     arc_center=[0, 1.45, 0], stroke_color=GREEN, stroke_width=LOOP_W)
        self.add(open_loop)
        self.moving_subject = VGroup(open_loop, insert)
        self.play(FadeIn(insert), run_time=0.5)
        self.at("matching ends meet")
        self.play(insert.animate.shift(DOWN * 1.1), run_time=0.9)
        self.at("ligase seals")
        ligase_label = chip("DNA ligase", YELLOW, 32).move_to([-4.4, 2.8, 0])
        ligase_tool = Circle(radius=0.28, color=YELLOW, stroke_width=7,
                             fill_color=YELLOW, fill_opacity=0.25).move_to([0, 3.1, 0])
        self.play(FadeIn(ligase_label), FadeIn(ligase_tool), run_time=0.45)
        self.play(MoveAlongPath(ligase_tool, Circle(radius=2.75).move_to([0, 0.35, 0])), run_time=2.0, rate_func=linear)
        complete = plasmid([0, 0.35, 0], radius=2.2)
        self.play(FadeOut(VGroup(open_loop, insert, ligase_label, ligase_tool)), FadeIn(complete), run_time=0.6)
        self.moving_subject = complete
        self.at("recombinant DNA")
        label = T("recombinant DNA", 42, GREEN, weight=BOLD).move_to([0, -2.65, 0])
        self.play(FadeIn(label, shift=UP * 0.15), run_time=0.55)
        self.at("different sources")
        blue_l = T("plasmid", 30, BLUE).move_to([-4.5, 1.7, 0])
        green_l = T("human gene", 30, GREEN).move_to([4.5, 1.7, 0])
        self.play(FadeIn(blue_l), FadeIn(green_l), run_time=0.55)
        self.at("copy separately")
        copy = complete.copy().scale(0.42).move_to([4.6, -1.0, 0])
        self.play(TransformFromCopy(complete, copy), run_time=1.1)
        self.add(scope_tag("schematic"))
        bob(complete, amp=0.10, speed=1.4)
        self.finish()


class S05Predict(FilmScene):
    def construct(self):
        world = predict_world()
        good = plasmid([0, 0.45, 0], radius=2.0)
        self.add(world[4], good, world[1], scope_tag("schematic"))
        self.moving_subject = VGroup(good, world[1])
        self.at("change one detail")
        self.play(Transform(good, world[0]), FadeIn(world[2]), run_time=0.75)
        pulse(good[1], base=15, amp=3, speed=2.2)
        bob(world[1], amp=0.10, speed=1.4)
        self.at("Predict this")
        q = question_card("Will the cell make insulin?", y=-2.9, size=34)
        self.play(FadeIn(q.question), run_time=0.6)
        self.at("does not work in bacteria")
        self.play(Indicate(good[2:], color=RED, scale_factor=1.25), run_time=0.8)
        self.at("Will the cell")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Will the cell make insulin?"
    SECONDS = 4.5
    CARD = {"y": -2.9, "size": 34}
    RING_AT = (4.4, -3.0, 0)

    def backdrop(self):
        w = predict_world()
        pulse(w[0][1], base=15, amp=3, speed=2.2)
        bob(w[1], amp=0.10, speed=1.4)
        return w


class S07Reveal(FilmScene):
    def construct(self):
        bad = predict_world()
        self.add(bad)
        self.moving_subject = VGroup(bad[0], bad[1])
        self.at("carrying a gene is not enough")
        no = T("NO", 58, RED, weight=BOLD).move_to([4.0, 0.45, 0])
        self.play(FadeIn(no, scale=0.8), run_time=0.55)
        pulse(bad[0][1], base=15, amp=3, speed=1.7)
        self.at("recognize its control DNA")
        self.play(Indicate(bad[0][2:], color=RED, scale_factor=1.25), run_time=0.7)
        self.at("Replace the tab")
        good = plasmid([0, 0.45, 0], radius=2.0)
        self.play(FadeOut(VGroup(no, bad[2])), Transform(bad[0], good), run_time=0.75)
        self.at("reader moves")
        path = ArcBetweenPoints(bad[1].get_center(), [2.9, 0.45, 0], angle=-1.0)
        self.play(MoveAlongPath(bad[1], path), run_time=1.7, rate_func=linear)
        self.at("insulin product block appears")
        product = chip("insulin product", GREEN, 30).move_to([3.6, -1.05, 0])
        dots = DashedLine([2.2, -0.2, 0], product.get_left(), color=GREEN, stroke_width=4)
        self.play(Create(dots), FadeIn(product, shift=RIGHT * 0.2), run_time=0.8)
        vial_obj = vial([5.15, 1.55, 0], "insulin", 0.72)
        self.play(FadeOut(product, shift=UP * 0.2), FadeIn(vial_obj), run_time=0.9)
        self.at("could not direct a product")
        rule = caption("A gene needs control DNA the cell can read.", color=GREEN)
        self.play(FadeIn(rule), run_time=0.55)
        self.finish()


class S08Select(FilmScene):
    def construct(self):
        cells = VGroup(*[bacterium([x, 1.15, 0], width=3.2, height=2.25) for x in (-4.4, 0, 4.4)])
        self.moving_subject = cells
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.18), run_time=0.9)
        self.at("take up a plasmid")
        p = plasmid([0, 1.15, 0], radius=0.62, resistance=True)
        self.play(FadeIn(p, shift=DOWN * 0.3), run_time=0.65)
        self.at("antibiotic -resistance gene")
        marker = T("resistance marker", 30, RED).move_to([0, 2.85, 0])
        self.play(FadeIn(marker), Indicate(p[-1], color=RED, scale_factor=1.3), run_time=0.7)
        self.at("On antibiotic")
        plate = RoundedRectangle(corner_radius=0.35, width=12.1, height=1.25,
                                 stroke_color=RED, stroke_width=5, fill_color=RED,
                                 fill_opacity=0.20).move_to([0, -1.55, 0])
        plate_l = T("antibiotic selection", 32, RED).move_to(plate)
        plate_l.layout_ok = True
        self.play(FadeIn(plate), FadeIn(plate_l), cells.animate.shift(DOWN * 0.75), p.animate.shift(DOWN * 0.75), run_time=0.75)
        self.at("without a plasmid fail to grow")
        self.play(cells[0].animate.set_opacity(0.18), cells[2].animate.set_opacity(0.18), run_time=0.8)
        self.at("Surviving colonies")
        survivors = VGroup(*[bacterium([x, 0.4, 0], width=2.15, height=1.5, with_plasmid=True, resistance=True)
                             for x in (-2.5, 0, 2.5)])
        self.play(FadeOut(cells), FadeOut(p), FadeIn(survivors, scale=0.85), run_time=0.9)
        self.moving_subject = survivors
        self.at("marker travels on the plasmid")
        self.play(Indicate(VGroup(*[s[1][-1] for s in survivors]), color=RED, scale_factor=1.25), run_time=0.8)
        self.at("Insulin itself does not")
        note = caption("Resistance comes from the marker—not insulin.", color=RED)
        self.play(FadeIn(note), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Copy(FilmScene):
    def construct(self):
        parent = bacterium([-4.4, 0.65, 0], width=3.0, height=2.2, with_plasmid=True)
        self.moving_subject = parent
        self.add(parent)
        self.at("bacteria divide")
        daughters = VGroup(bacterium([-4.8, 1.5, 0], 2.5, 1.75, True),
                           bacterium([-2.6, -0.7, 0], 2.5, 1.75, True),
                           bacterium([-5.0, -1.35, 0], 2.5, 1.75, True))
        self.play(ReplacementTransform(parent, daughters), run_time=1.1)
        self.moving_subject = daughters
        self.at("copy the plasmid")
        self.play(LaggedStart(*[Indicate(d[1], color=BLUE, scale_factor=1.2) for d in daughters], lag_ratio=0.18), run_time=1.1)
        on = T("if switched on", 32, GREEN).move_to([0, 2.85, 0])
        self.at("gene is switched on")
        self.play(FadeIn(on), run_time=0.5)
        products = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.55, height=0.34,
                                             stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.55)
                            for _ in range(7)]).arrange(DOWN, buff=0.18).move_to([-0.3, 0.15, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in products], lag_ratio=0.1), run_time=1.2)
        self.at("purify and process")
        funnel = Polygon([-0.8, 1.4, 0], [0.8, 1.4, 0], [0.3, -0.2, 0], [0.3, -1.2, 0],
                         [-0.3, -1.2, 0], [-0.3, -0.2, 0], color=TEAL,
                         stroke_width=5, fill_color=TEAL, fill_opacity=0.08).move_to([2.2, 0.2, 0])
        self.play(products.animate.move_to([2.2, 0.7, 0]), FadeIn(funnel), run_time=0.8)
        medicine = vial([5.0, 0.2, 0], "medicine", 1.05)
        self.at("insulin medicine")
        self.play(FadeOut(products), FadeIn(medicine, shift=RIGHT * 0.2), run_time=0.75)
        self.at("Each daughter can inherit")
        self.play(LaggedStart(*[Indicate(d[1], color=GREEN, scale_factor=1.18) for d in daughters], lag_ratio=0.18), run_time=1.0)
        self.at("with selection")
        keep = caption("Selection helps the colony keep the added instruction.", color=RED)
        self.play(FadeIn(keep), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Rule(FilmScene):
    def construct(self):
        xs = [-5.3, -2.65, 0, 2.65, 5.3]
        tool = chip("cut", YELLOW, 30).move_to([xs[0], 0.4, 0])
        loop = plasmid([xs[1], 0.4, 0], 0.72)
        cell = bacterium([xs[2], 0.4, 0], 2.1, 1.5, True)
        plate = RoundedRectangle(corner_radius=0.18, width=1.9, height=1.0,
                                 stroke_color=RED, fill_color=RED, fill_opacity=0.12).move_to([xs[3], 0.4, 0])
        select_l = T("select", 28, RED).move_to(plate); select_l.layout_ok = True
        product = vial([xs[4], 0.4, 0], "read", 0.65)
        items = [tool, loop, cell, VGroup(plate, select_l), product]
        self.moving_subject = tool
        labels = ["cut", "join", "carry", "select", "read"]
        for i, (item, word) in enumerate(zip(items, labels)):
            if i == 0:
                self.play(FadeIn(item), run_time=0.4)
            else:
                self.at(word)
                self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.35)
            if i in (1, 2, 4):
                bob(item, amp=0.09, speed=1.5, seed=i)
            self.moving_subject = VGroup(*items[:i + 1])
            if i < 4:
                self.play(GrowArrow(arrow([xs[i] + 0.9, 0.4, 0], [xs[i + 1] - 0.9, 0.4, 0], GREY, 3)), run_time=0.25)
        self.at("Each step supports")
        chain = T("each step supports the next", 36, TEAL).move_to([0, 2.55, 0])
        self.play(FadeIn(chain), run_time=0.5)
        self.at("none guarantees")
        uncertain = T("?", 54, TEAL, weight=BOLD).move_to([5.95, 2.25, 0])
        self.play(FadeIn(uncertain, scale=0.8), run_time=0.45)
        self.at("test the effects")
        rule = caption("Engineering changes a cell's DNA; test the effects, judge each use separately.", color=TEAL)
        self.play(FadeIn(rule), run_time=0.55)
        self.play(Indicate(uncertain, color=TEAL, scale_factor=1.25), run_time=0.7)
        self.finish()


class S11End(EndCard):
    LINE = "Engineering changes a cell's DNA; test the effects, judge each use separately."
