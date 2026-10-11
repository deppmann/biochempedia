"""Rapamycin needs a partner: section film for the mTOR and AMPK lesson.

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = rapamycin (the drug)
  BLUE   = FKBP12 and its yeast version, the FPR1 gene
  PURPLE = TOR / mTOR (the kinase) and its domains
  GREEN  = living, growing yeast and cells
  RED    = killed, stopped, crossed out, "the poison"
  TEAL   = ATP
  GREY   = places, people, structure, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def cross(mob, color=RED, w=7):
    r = mob.get_corner(UR); l = mob.get_corner(DL); r2 = mob.get_corner(UL); l2 = mob.get_corner(DR)
    return VGroup(Line(l, r, color=color, stroke_width=w), Line(l2, r2, color=color, stroke_width=w))


def tag(text, y=-3.25):
    return T(text, 22, GREY).move_to([0, y, 0])


class S00Title(TitleCard):
    LESSON = "mTOR and AMPK: how a cell decides to grow"
    TITLE = "Rapamycin Needs a Partner"


# ---------------------------------------------------------------------------------------------
class S01Soil(SpokenScene):
    def construct(self):
        # stage A: island -> soil -> Montreal -> fungi
        date = T("December 1964 to February 1965", 26, GREY).move_to([-3.2, 3.2, 0])
        island = Ellipse(width=4.2, height=2.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([-3.6, 0.3, 0])
        isl_lbl = T("Rapa Nui (Easter Island)", 26, TEXT).next_to(island, DOWN, buff=0.25)
        self.at("In December")
        self.play(FadeIn(date, shift=DOWN * 0.1), FadeIn(island), FadeIn(isl_lbl), run_time=0.9)
        who = chip("Georges Nogrady", GREY, 24)
        who.move_to([-3.6, 2.2, 0])
        self.at("One member")
        self.play(FadeIn(who, shift=DOWN * 0.1), run_time=0.6)
        soil = chip("soil", GREY, 26).move_to(island.get_center())
        self.at("collected soil")
        self.play(FadeIn(soil, scale=0.6), run_time=0.5)
        mont = chip("Ayerst, Montreal", BLUE, 28).move_to([1.4, 0.3, 0])
        self.at("In Montreal")
        self.play(soil.animate.move_to([0.4, 0.3, 0]).scale(0.9), FadeIn(mont, shift=LEFT * 0.2), run_time=1.0)
        bact = chip("a bacterium", GREEN, 28).move_to([1.4, -1.6, 0])
        self.at("a bacterium")
        self.play(FadeOut(soil), FadeIn(bact, shift=UP * 0.2), run_time=0.7)
        fungi = chip("fungi", GREEN, 28).move_to([5.3, 0.3, 0])
        kill = arr([2.6, -1.2, 0], [4.5, 0.0, 0], RED)
        self.at("kill fungi")
        self.play(GrowArrow(kill), FadeIn(fungi), run_time=0.6)
        x = T("killed", 26, RED).next_to(fungi, DOWN, buff=0.25)
        self.play(FadeIn(x, shift=UP * 0.1), run_time=0.5)
        # stage B: Sehgal isolates and names rapamycin
        stageA = VGroup(date, island, isl_lbl, who, mont, bact, kill, fungi, x)
        self.at("In 1972")
        self.play(FadeOut(stageA), run_time=0.6)
        yr = T("1972", 36, GREY, font=MONO).move_to([0, 2.0, 0])
        seh = chip("Suren Sehgal", GREY, 30).move_to([-4.0, 0.2, 0])
        rapa = chip("rapamycin", YELLOW, 36).move_to([4.2, 0.2, 0])
        iso = arr([-2.0, 0.2, 0], [2.7, 0.2, 0], GREY)
        iso_l = T("isolated the compound", 26, GREY).next_to(iso, UP, buff=0.2)
        self.play(FadeIn(yr), FadeIn(seh), run_time=0.5)
        self.at("isolated the compound")
        self.play(GrowArrow(iso), FadeIn(iso_l), run_time=0.6)
        self.at("named it")
        self.play(FadeIn(rapa, scale=0.7), run_time=0.6)
        nm = T("named after the island", 24, GREY).next_to(rapa, DOWN, buff=0.3)
        self.play(FadeIn(nm), run_time=0.4)
        # stage C: the question
        self.at("But why does")
        self.play(FadeOut(VGroup(yr, seh, iso, iso_l, nm)), rapa.animate.move_to([-3.6, 0.2, 0]), run_time=0.7)
        cell = chip("cells growing", GREEN, 36).move_to([3.8, 0.2, 0])
        stop = inhib([-1.7, 0.2, 0], [1.6, 0.2, 0], RED)
        q = T("?", 96, RED, weight=BOLD).move_to([0, 1.9, 0])
        self.at("also stop cells")
        self.play(FadeIn(cell, shift=LEFT * 0.2), Create(stop), run_time=0.6)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def yeast_plate():
    rng = np.random.default_rng(7)
    disc = Circle(radius=2.45, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    dots = VGroup()
    pts = []
    while len(pts) < 44:
        p = rng.uniform(-2.0, 2.0, 2)
        if np.hypot(*p) < 2.0 and all(np.hypot(*(p - q)) > 0.42 for q in pts):
            pts.append(p)
    for p in pts:
        dots.add(Dot([p[0], p[1], 0], radius=0.1, color=GREEN))
    return disc, dots


class S02Screen(SpokenScene):
    def construct(self):
        disc, dots = yeast_plate()
        g = VGroup(disc, dots).move_to([-3.4, -0.1, 0])
        head = T("yeast on plates with rapamycin", 26, GREY).move_to([-3.4, 3.0, 0])
        lab = VGroup(T("Hall lab, Basel", 24, GREY), T("Joseph Heitman", 26, TEXT)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([3.0, 1.8, 0])
        self.at("In Michael")
        self.play(FadeIn(lab[0], shift=DOWN * 0.1), run_time=0.6)
        self.at("Joseph")
        self.play(FadeIn(lab[1], shift=DOWN * 0.1), run_time=0.5)
        self.at("spread yeast")
        self.play(FadeIn(disc), FadeIn(head), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), run_time=1.4)
        self.at("rapamycin")
        rap = chip("rapamycin", YELLOW, 24).move_to([-3.4, -3.1, 0])
        self.play(FadeIn(rap, shift=UP * 0.15), run_time=0.5)
        keep_ids = [3, 17, 29, 38]
        keep = VGroup(*[dots[i] for i in keep_ids])
        rest = VGroup(*[d for i, d in enumerate(dots) if i not in keep_ids])
        self.at("kept the rare")
        self.play(rest.animate.set_color(RED).set_opacity(0.0), run_time=0.6)
        rings = VGroup(*[Circle(radius=0.24, stroke_color=GREEN, stroke_width=4).move_to(d) for d in keep])
        self.at("rare mutants")
        self.play(Create(rings), *[d.animate.scale(1.6) for d in keep], run_time=0.8)
        kept_l = T("the rare mutants that grew", 26, GREEN).move_to([3.0, 1.0, 0])
        self.play(FadeIn(kept_l), run_time=0.5)
        # split bar: most FPR1, the rest
        barw = 5.0
        most = Rectangle(width=barw * 0.62, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3)
        rest_b = Rectangle(width=barw * 0.38, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
        bar = VGroup(most, rest_b).arrange(RIGHT, buff=0).move_to([3.0, -0.5, 0])
        bar_l = T("mutants (not to scale)", 22, GREY).next_to(bar, UP, buff=0.12)
        most_l = T("most", 24, BLUE).move_to(most)
        self.at("Most had mutations")
        self.play(FadeIn(bar), FadeIn(bar_l), FadeIn(most_l), run_time=0.6)
        fpr = chip("FPR1 gene", BLUE, 28).move_to([1.7, -1.8, 0])
        fl = T("yeast version of FKBP12", 24, BLUE).move_to([3.0, -2.7, 0])
        self.at("gene for")
        self.play(FadeIn(fpr, shift=UP * 0.15), run_time=0.5)
        self.at("yeast version")
        self.play(FadeIn(fl), run_time=0.5)
        # the pair
        self.at("So rapamycin")
        self.play(FadeOut(VGroup(disc, dots, head, rap, rings, lab, kept_l, bar, bar_l, most_l, fpr, fl)), run_time=0.7)
        r = chip("rapamycin", YELLOW, 34).move_to([-3.0, 0.4, 0])
        al = T("alone: nothing", 28, GREY).next_to(r, DOWN, buff=0.4)
        self.play(FadeIn(r, scale=0.8), run_time=0.5)
        self.at("does nothing alone")
        self.play(FadeIn(al), run_time=0.5)
        fk = chip("FKBP12", BLUE, 34).move_to([3.0, 0.4, 0])
        self.at("It must first")
        self.play(FadeIn(fk, shift=LEFT * 0.2), run_time=0.5)
        self.at("bind")
        self.play(FadeOut(al), r.animate.move_to([-1.0, 0.4, 0]), fk.animate.move_to([1.55, 0.4, 0]), run_time=0.9)
        box = SurroundingRectangle(VGroup(r, fk), buff=0.3, corner_radius=0.2, stroke_color=RED, stroke_width=5)
        pl = T("the pair is the poison", 34, RED).next_to(box, DOWN, buff=0.45)
        self.at("the pair")
        self.play(Create(box), FadeIn(pl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tor(SpokenScene):
    def construct(self):
        barw = 8.4
        most = Rectangle(width=barw * 0.62, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3)
        rest_b = Rectangle(width=barw * 0.38, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
        bar = VGroup(most, rest_b).arrange(RIGHT, buff=0).move_to([0, 2.6, 0])
        bar_l = T("mutants that grew (not to scale)", 22, GREY).next_to(bar, UP, buff=0.12)
        most_l = T("most: FPR1", 24, BLUE).move_to(most)
        rest_l = T("the remaining", 24, GREY).move_to(rest_b)
        self.play(FadeIn(bar), FadeIn(bar_l), FadeIn(most_l), FadeIn(rest_l), run_time=0.5)
        t1 = chip("TOR1", PURPLE, 34).move_to([2.2, 0.5, 0])
        t2 = chip("TOR2", PURPLE, 34).move_to([4.6, 0.5, 0])
        l1 = Line(rest_b.get_bottom(), t1.get_top(), color=PURPLE, stroke_width=3)
        l2 = Line(rest_b.get_bottom(), t2.get_top(), color=PURPLE, stroke_width=3)
        self.at("two new genes")
        self.play(rest_b.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.3), rest_l.animate.set_color(PURPLE),
                  Create(l1), Create(l2), FadeIn(t1, shift=DOWN * 0.15), FadeIn(t2, shift=DOWN * 0.15), run_time=0.9)
        tl = T("target of rapamycin", 28, PURPLE).move_to([3.4, -0.5, 0])
        self.at("target of rapamycin")
        self.play(FadeIn(tl, shift=UP * 0.1), run_time=0.6)
        # timeline
        line = Line([-6.0, -1.9, 0], [6.0, -1.9, 0], color=GREY, stroke_width=3)
        x91, x94 = -3.6, 2.4
        k91 = VGroup(Line([x91, -1.75, 0], [x91, -2.05, 0], color=TEXT, stroke_width=4), M("1991", 28, TEXT).move_to([x91, -1.4, 0]))
        c91 = T("the screen is published", 24, GREY).move_to([x91, -2.5, 0])
        self.at("The screen was published")
        self.play(Create(line), FadeIn(k91), run_time=0.6)
        self.play(FadeIn(c91), run_time=0.4)
        k94 = VGroup(Line([x94, -1.75, 0], [x94, -2.05, 0], color=TEXT, stroke_width=4), M("1994-95", 28, TEXT).move_to([x94, -1.4, 0]))
        c94 = T("the mammalian protein is found", 24, GREY).move_to([x94 + 0.3, -2.5, 0])
        self.at("several laboratories")
        self.play(FadeIn(k94), FadeIn(c94), run_time=0.6)
        # clear, dock
        self.at("the pair binds")
        self.play(FadeOut(VGroup(bar, bar_l, most_l, rest_l, l1, l2, t1, t2, tl, line, k91, c91, k94, c94)), run_time=0.4)
        prot = RoundedRectangle(corner_radius=0.5, width=4.6, height=2.8, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.22).move_to([2.6, 0.0, 0])
        pl = T("mammalian protein", 30, PURPLE).move_to(prot)
        r = chip("rapamycin", YELLOW, 30)
        fk = chip("FKBP12", BLUE, 30)
        pair = VGroup(fk, r).arrange(RIGHT, buff=0.0).move_to([-4.8, 0.0, 0])
        self.play(FadeIn(prot), FadeIn(pl), FadeIn(pair), run_time=0.5)
        self.play(pair.animate.next_to(prot, LEFT, buff=0.0), run_time=0.7)
        self.at("Its name is")
        nm = T("mTOR", 56, PURPLE, weight=BOLD).move_to(prot)
        self.play(ReplacementTransform(pl, nm), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Glue(SpokenScene):
    def construct(self):
        body = RoundedRectangle(corner_radius=0.3, width=5.4, height=3.2, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.2).move_to([-1.5, 0.2, 0])
        kd = T("kinase domain", 28, PURPLE).move_to([-0.6, -1.0, 0])
        name = T("mTOR", 44, PURPLE, weight=BOLD).move_to([-1.5, 2.45, 0])
        self.at("large kinase")
        self.play(FadeIn(body), FadeIn(kd), FadeIn(name), run_time=0.8)
        site = Circle(radius=0.32, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([-3.0, 0.4, 0])
        site_l = T("active site", 24, TEXT).move_to([-3.0, -0.35, 0])
        frb = chip("FRB", PURPLE, 32).move_to([2.7, 0.2, 0])
        link = Line(body.get_right(), frb.get_left(), color=PURPLE, stroke_width=4)
        self.at("small domain called")
        self.play(FadeIn(site), FadeIn(site_l), Create(link), FadeIn(frb, shift=LEFT * 0.2), run_time=0.8)
        sub = chip("substrate", GREEN, 24).move_to([-5.3, 0.4, 0])
        path = arr(sub.get_right(), [-3.4, 0.4, 0], GREEN, w=14, tip=0.3)
        fk = chip("FKBP12", BLUE, 32).move_to([2.7, 2.0, 0])
        glue = Rectangle(width=fk.width, height=0.22, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
        glue.move_to([2.7, (frb.get_top()[1] + fk.get_bottom()[1]) / 2, 0])
        gl = T("rapamycin", 28, YELLOW).next_to(glue, RIGHT, buff=0.15)
        self.at("Rapamycin sits between")
        self.play(FadeIn(fk, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(glue, scale=0.6), FadeIn(gl), run_time=0.5)
        self.at("like glue")
        self.play(Indicate(glue, color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.at("The bound")
        self.play(FadeIn(sub), GrowArrow(path), run_time=0.6)
        thin = arr(sub.get_right(), [-3.4, 0.4, 0], GREEN, w=4, tip=0.2)
        nl = T("narrower path", 22, GREEN).next_to(sub, DOWN, buff=0.3)
        self.at("narrows the")
        self.play(Transform(path, thin), FadeIn(nl), run_time=0.9)
        sch = tag("schematic, not to scale", -3.35)
        self.play(FadeIn(sch), run_time=0.3)
        atp = chip("competes with ATP", TEAL, 30).move_to([-1.5, -2.35, 0])
        xa = Line(atp.get_left() + LEFT * 0.1, atp.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.at("does not compete")
        self.play(FadeIn(atp, shift=DOWN * 0.1), run_time=0.5)
        self.play(Create(xa), run_time=0.5)
        self.at("is allosteric")
        self.play(FadeOut(VGroup(atp, xa, nl, sub, path, name)), run_time=0.5)
        al = T("allosteric inhibitor", 38, YELLOW, weight=BOLD).move_to([-1.5, 2.45, 0])
        self.play(FadeIn(al, shift=DOWN * 0.1), run_time=0.5)
        dsite = T("drug site", 24, YELLOW).move_to([2.7, -0.6, 0])
        self.at("a site other")
        ring_s = Circle(radius=0.48, stroke_color=TEXT, stroke_width=4).move_to(site)
        ring_d = SurroundingRectangle(VGroup(fk, glue, gl, frb, dsite), buff=0.2, corner_radius=0.2, stroke_color=YELLOW, stroke_width=3)
        self.play(Create(ring_s), Create(ring_d), FadeIn(dsite), run_time=0.7)
        self.finish()


class S05End(EndCard):
    LINE = "Rapamycin works only with its partner, FKBP12."
