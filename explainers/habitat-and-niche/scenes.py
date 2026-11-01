"""Habitat and niche: different niches let many kinds share one place  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the organisms (warblers, squirrel, earthworm, "species")
  GREEN  = habitat (the place: spruce forest, oak forest)
  PURPLE = niche (the role: its circles, ovals and the list of what it includes)
  YELLOW = resources and food (insects, acorns, leaves, water, shelter, space)
  RED    = competition
  TEAL   = biodiversity
  GREY   = outlines, notes
All shapes are schematic and not to scale. No measured numbers appear: the only numbers are the five kinds
of warblers (lesson text) and the oak/spruce forests named in the lesson.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORG = BLUE
HAB = GREEN
NICHE = "#B58CD9"
RES = YELLOW
COMP = RED
BIO = TEAL


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(color, r=0.17, op=0.7):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op)


def spruce(cx, base_y=-2.9):
    """a spruce as three stacked triangles and a trunk: a labelled schematic, not a drawing of a real tree."""
    tiers = [(2.9, 1.1, 2.2), (1.6, -0.4, 3.2), (0.2, -2.1, 4.2)]
    parts = []
    for apex, base, w in tiers:
        parts.append(Polygon([cx, apex, 0], [cx - w / 2, base, 0], [cx + w / 2, base, 0],
                             stroke_color=HAB, stroke_width=3, fill_color=HAB, fill_opacity=0.12))
    trunk = Rectangle(width=0.4, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
    trunk.move_to([cx, -2.5, 0])
    return VGroup(trunk, *parts)


def habitat_box(cx, cy, w, h):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=HAB, stroke_width=3.5,
                            fill_color=HAB, fill_opacity=0.07).move_to([cx, cy, 0])


class S00Title(TitleCard):
    LESSON = "Habitat and niche"
    TITLE = "Different Niches Let Many Kinds Share"


# ---------------------------------------------------------------------------------------------
class S01Warblers(SpokenScene):
    def construct(self):
        cx = -3.7
        tree = spruce(cx)
        offs = [(0, 1.9), (-0.5, 0.6), (0.6, 0.2), (-0.85, -1.3), (0.85, -1.3)]
        birds = VGroup(*[dot(ORG, 0.17, 0.85).move_to([cx + dx, dy, 0]) for dx, dy in offs])
        ins_off = [(0.35, 1.25), (-0.3, 1.4), (0.2, 0.3), (-0.2, -0.3), (0.9, -0.7), (-1.1, -0.5), (0.15, -1.6),
                   (-0.1, -0.8), (1.3, -1.7), (-1.4, -1.7), (0.5, 0.9), (-0.9, 0.2)]
        bugs = VGroup(*[dot(RES, 0.075, 0.95).move_to([cx + dx, dy, 0]) for dx, dy in ins_off])
        t1 = VGroup(T("5 kinds of warblers", 40, ORG, weight=BOLD), T("small birds", 28, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t2 = VGroup(T("spruce forests", 40, HAB, weight=BOLD), T("Maine and Vermont, in summer", 28, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t3 = VGroup(T("they eat mostly insects", 40, RES, weight=BOLD), T("picked from the trees", 28, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        right = VGroup(t1, t2, t3).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([3.3, 0.1, 0])
        note = T("a sketch, not to scale", 22, GREY).move_to([cx, -3.35, 0])
        self.at("Five kinds")
        self.play(FadeIn(tree, scale=0.95), FadeIn(note), run_time=0.9)
        self.play(FadeIn(birds, lag_ratio=0.25, scale=0.5), FadeIn(t1, shift=LEFT * 0.2), run_time=1.5)
        self.at("spruce forests")
        self.play(FadeIn(t2, shift=LEFT * 0.2), Indicate(tree, color=HAB, scale_factor=1.03), run_time=0.9)
        self.at("mostly insects")
        self.play(FadeIn(bugs, lag_ratio=0.1, scale=0.5), FadeIn(t3, shift=LEFT * 0.2), run_time=1.2)
        q = T("How can so many kinds\nof animals share one place\nwithout running out of food?", 40, TEXT,
              font=TITLE_FONT, line_spacing=0.85)
        fit(q, max_w=6.6, max_h=3.6)
        q.move_to([3.3, 0.1, 0])
        self.at("How can so many")
        self.play(FadeOut(right), run_time=0.6)
        self.play(Write(q), run_time=2.2)
        self.play(Indicate(birds, color=ORG, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Words(SpokenScene):
    def construct(self):
        box = habitat_box(0, 0.2, 7.2, 3.9)
        hlab = T("habitat: the place where it lives", 36, HAB, weight=BOLD).move_to([0, 2.85, 0])
        forest = chip("spruce forest", HAB, size=32).move_to([-1.3, 1.1, 0])
        self.at("A habitat is")
        self.play(FadeIn(box), Write(hlab), run_time=1.3)
        self.at("A spruce forest is")
        self.play(FadeIn(forest, scale=0.9), run_time=0.7)
        # niche
        oval = Ellipse(width=3.8, height=1.6, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.14).move_to([0.9, -0.55, 0])
        org = dot(ORG, 0.2, 0.85).move_to([-0.2, -0.55, 0])
        nlab = T("niche: its role in the habitat", 36, NICHE, weight=BOLD).move_to([0, -2.45, 0])
        self.at("A niche is")
        self.play(FadeIn(org, scale=0.5), Create(oval), Write(nlab), run_time=1.5)
        addr = chip("address", HAB, size=32).move_to([-5.2, 0.9, 0])
        job = chip("job", NICHE, size=32).move_to([5.2, -0.55, 0])
        a1 = arr(addr.get_right(), [-3.65, 0.9, 0], HAB, w=5)
        a2 = arr(job.get_left(), [2.85, -0.55, 0], NICHE, w=5)
        self.at("as an address")
        self.play(FadeIn(addr, shift=RIGHT * 0.2), GrowArrow(a1), Indicate(box, color=HAB, scale_factor=1.02), run_time=1.0)
        self.at("as a job")
        self.play(FadeIn(job, shift=LEFT * 0.2), GrowArrow(a2), Indicate(oval, color=NICHE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Oak(SpokenScene):
    def construct(self):
        head = T("a niche is more than one job", 40, NICHE, font=TITLE_FONT).move_to([0, 3.0, 0])
        items = [chip("what it eats", NICHE, size=32), chip("where and when it feeds", NICHE, size=32),
                 chip("the space it uses", NICHE, size=32), chip("what eats it", NICHE, size=32)]
        stack = VGroup(*items).arrange(DOWN, buff=0.38).move_to([0, -0.3, 0])
        self.at("more than one job")
        self.play(Write(head), run_time=1.2)
        self.at("what the organism eats")
        self.play(FadeIn(items[0], shift=UP * 0.15), run_time=0.6)
        self.at("where and when it feeds")
        self.play(FadeIn(items[1], shift=UP * 0.15), run_time=0.6)
        self.at("the space it uses")
        self.play(FadeIn(items[2], shift=UP * 0.15), run_time=0.6)
        self.at("what eats it")
        self.play(FadeIn(items[3], shift=UP * 0.15), run_time=0.6)
        # oak forest
        box = habitat_box(0, -0.2, 12.0, 5.5)
        hlab = T("habitat: Virginia oak forest", 34, HAB, weight=BOLD).move_to([0, 1.95, 0])
        sq = chip("gray squirrel", ORG, size=32).move_to([-4.0, 0.6, 0])
        ew = chip("earthworm", ORG, size=32).move_to([-4.0, -1.0, 0])
        f1 = chip("acorns and nuts", RES, size=32).move_to([1.2, 0.6, 0])
        f2 = chip("dead leaves and soil", RES, size=32).move_to([1.2, -1.0, 0])
        e1 = arr(sq.get_right(), f1.get_left(), GREY, w=5)
        e2 = arr(ew.get_right(), f2.get_left(), GREY, w=5)
        lab1 = T("eats", 26, GREY).next_to(e1, UP, buff=0.05)
        lab2 = T("eats", 26, GREY).next_to(e2, UP, buff=0.05)
        self.at("Take a Virginia oak forest")
        self.play(FadeOut(head), FadeOut(stack), run_time=0.5)
        self.play(FadeIn(box), Write(hlab), run_time=1.0)
        self.at("A gray squirrel")
        self.play(FadeIn(sq, scale=0.9), FadeIn(ew, scale=0.9), run_time=0.8)
        self.at("The squirrel eats")
        self.play(GrowArrow(e1), FadeIn(lab1), FadeIn(f1, shift=LEFT * 0.2), run_time=0.9)
        self.at("The earthworm eats")
        self.play(GrowArrow(e2), FadeIn(lab2), FadeIn(f2, shift=LEFT * 0.2), run_time=0.9)
        r1 = RoundedRectangle(corner_radius=0.2, width=11.2, height=1.3, stroke_color=NICHE, stroke_width=4).move_to([0, 0.6, 0])
        r2 = RoundedRectangle(corner_radius=0.2, width=11.2, height=1.3, stroke_color=NICHE, stroke_width=4).move_to([0, -1.0, 0])
        nl = T("different niches", 34, NICHE, weight=BOLD).move_to([0, -2.4, 0])
        self.at("They share a habitat")
        self.play(Indicate(box, color=HAB, scale_factor=1.015), run_time=0.9)
        self.at("their niches")
        self.play(Create(r1), Create(r2), FadeIn(nl, shift=UP * 0.1), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Resource(SpokenScene):
    def construct(self):
        names = ["food", "water", "shelter", "space"]
        chips = VGroup(*[chip(n, RES, size=30) for n in names]).arrange(RIGHT, buff=0.35).move_to([0, 2.55, 0])
        head = T("resources", 38, RES, font=TITLE_FONT, weight=BOLD).move_to([0, 3.15, 0])
        cy = -0.55
        box = habitat_box(0, cy, 11.4, 4.4)
        an = dot(ORG, 0.22, 0.9).move_to([-2.0, cy, 0])
        pts = [(-2.0 + 0.7, cy + 0.5), (-2.0 - 0.8, cy + 0.2), (-2.0 + 0.2, cy - 0.8), (-2.0 - 0.3, cy + 0.9),
               (-2.0 + 0.9, cy - 0.3), (-2.0 - 0.7, cy - 0.7), (3.4, cy + 0.4), (1.4, cy - 1.4),
               (4.2, cy - 1.5), (2.6, cy + 1.3), (0.9, cy + 1.2), (4.5, cy + 1.2)]
        dots = VGroup(*[dot(RES, 0.1, 0.95).move_to([x, y, 0]) for x, y in pts])
        keep = [0, 6]
        circ = Circle(radius=1.35, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.12).move_to(an)
        clab = T("where it feeds", 28, NICHE).move_to([-2.0, cy - 1.85, 0])
        sk4 = T("a sketch, not to scale", 24, TEXT).move_to([3.5, cy - 1.75, 0])
        anl = T("an animal", 24, TEXT).next_to(an, UP, buff=0.12)
        defl = T("something a living thing needs and takes", 28, TEXT).move_to([0, 2.55, 0])
        self.at("A resource is")
        self.play(Write(head), FadeIn(defl, shift=UP * 0.1), run_time=0.9)
        self.at("takes from its habitat")
        self.play(FadeIn(box), FadeIn(an, scale=0.5), FadeIn(anl), run_time=0.9)
        self.at("Food, water")
        self.play(FadeOut(defl), FadeIn(chips, lag_ratio=0.35, shift=DOWN * 0.15), run_time=1.6)
        self.at("Part of an")
        self.play(FadeIn(dots, lag_ratio=0.05), FadeOut(anl), run_time=0.8)
        self.play(Create(circ), FadeIn(clab), FadeIn(sk4), run_time=1.0)
        gone = VGroup(*[d for i, d in enumerate(dots) if i not in keep])
        less = T("less food", 32, RES, weight=BOLD).move_to([3.6, cy - 0.45, 0])
        self.at("runs short")
        self.play(FadeOut(gone), FadeOut(clab), FadeIn(less, shift=UP * 0.1), run_time=1.0)
        wide = Circle(radius=2.05, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.12).move_to([-0.35, cy, 0])
        clab2 = T("searches more places", 28, NICHE).move_to([3.55, cy - 1.3, 0])
        self.at("search more places")
        self.play(Transform(circ, wide), FadeIn(clab2), an.animate.move_to([-0.35, cy, 0]), run_time=1.4)
        shift = T("so the niche can shift", 34, NICHE, weight=BOLD).move_to([0, -3.25, 0])
        self.at("So a niche can shift")
        self.play(FadeOut(chips), FadeOut(head), run_time=0.4)
        self.play(FadeIn(shift, shift=DOWN * 0.1), Indicate(circ, color=NICHE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Overlap(SpokenScene):
    def construct(self):
        one = chip("a species: one kind of living thing", ORG, size=34).move_to([0, 0.4, 0])
        self.at("A species is")
        self.play(FadeIn(one, scale=0.9), run_time=0.9)
        a = chip("species A", ORG, size=34).move_to([-3.6, 1.5, 0])
        b = chip("species B", ORG, size=34).move_to([3.6, 1.5, 0])
        res = chip("the same limited resource", RES, size=34).move_to([0, -0.6, 0])
        ar1 = arr(a.get_bottom(), res.get_left() + UP * 0.1, GREY, w=5)
        ar2 = arr(b.get_bottom(), res.get_right() + UP * 0.1, GREY, w=5)
        self.at("two species need")
        self.play(FadeOut(one), FadeIn(a, shift=RIGHT * 0.2), FadeIn(b, shift=LEFT * 0.2), run_time=0.8)
        self.play(FadeIn(res, scale=0.9), GrowArrow(ar1), GrowArrow(ar2), run_time=0.9)
        comp = T("they compete", 44, COMP, weight=BOLD).move_to([0, -1.9, 0])
        self.at("they compete")
        self.play(FadeIn(comp, scale=0.9), Indicate(res, color=COMP, scale_factor=1.06), run_time=0.9)
        defn = T("competition: a struggle for resources\nthat are in short supply", 34, COMP, line_spacing=0.85).move_to([0, -2.3, 0])
        self.at("Competition is a struggle")
        self.play(FadeOut(comp), FadeIn(defn, shift=UP * 0.1), run_time=0.8)
        # niche circles
        self.at("niches that overlap a lot")
        self.play(FadeOut(res), FadeOut(ar1), FadeOut(ar2), FadeOut(defn), FadeOut(a), FadeOut(b), run_time=0.4)
        ca = Circle(radius=1.9, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.14).move_to([-1.0, 0.5, 0])
        cb = Circle(radius=1.9, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.14).move_to([1.0, 0.5, 0])
        la = chip("species A", ORG, size=30).move_to([-3.4, 3.0, 0])
        lb = chip("species B", ORG, size=30).move_to([3.4, 3.0, 0])
        nl = T("their niches", 30, NICHE).move_to([0, 3.0, 0])
        track = RoundedRectangle(corner_radius=0.15, width=7.0, height=0.4, stroke_color=GREY, stroke_width=2.5).move_to([-0.8, -2.2, 0])
        clab = T("competition", 30, COMP, weight=BOLD).next_to(track, RIGHT, buff=0.35)
        skt = T("a sketch, not measured", 26, TEXT).move_to([0, -3.1, 0])
        self.play(Create(ca), Create(cb), FadeIn(la), FadeIn(lb), FadeIn(nl), FadeIn(track), FadeIn(clab), FadeIn(skt), run_time=0.9)
        food = VGroup(*[dot(RES, 0.1, 0.95).move_to([x, y, 0]) for x, y in ((0, 1.0), (0, 0.5), (0, 0.0), (-0.2, 0.75), (0.2, 0.25))])
        fill = Rectangle(width=0.01, height=0.4, stroke_width=0, fill_color=COMP, fill_opacity=0.85).move_to(track.get_left() + RIGHT * 0.005)
        fill.align_to(track, LEFT)
        big = Rectangle(width=5.6, height=0.4, stroke_width=0, fill_color=COMP, fill_opacity=0.85).align_to(track, LEFT).move_to(track.get_left() + RIGHT * 2.8)
        self.at("they compete a lot")
        self.play(FadeIn(food, scale=0.5), Transform(fill, big), run_time=1.2)
        most = T("one possible result", 28, TEXT).move_to([4.95, -0.6, 0])
        self.at("One may get most")
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(list(food)[:4], ((-1.7, 1.0), (-1.4, 0.5), (-1.8, 0.0), (-1.2, 0.8)))],
                  cb.animate.set_stroke(opacity=0.35).set_fill(opacity=0.04), FadeIn(most), run_time=1.2)
        small = Rectangle(width=1.4, height=0.4, stroke_width=0, fill_color=COMP, fill_opacity=0.85).align_to(track, LEFT).move_to(track.get_left() + RIGHT * 0.7)
        self.at("If their niches")
        self.play(FadeOut(food), FadeOut(most), run_time=0.4)
        self.play(ca.animate.move_to([-2.9, 0.5, 0]), cb.animate.move_to([2.9, 0.5, 0]).set_stroke(opacity=1).set_fill(opacity=0.14), Transform(fill, small), run_time=1.5)
        self.at("compete less")
        self.play(Indicate(clab, color=COMP, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = T("How can so many kinds of animals share one place?", 36, TEXT, font=TITLE_FONT)
        fit(q, max_w=12.2, max_h=1.0)
        q.move_to([0, 3.1, 0])
        box = habitat_box(0, 0.0, 11.4, 4.5)
        hl = T("one habitat", 30, HAB, weight=BOLD).move_to([-4.3, 1.75, 0])
        pos = [(-3.5, 0.55), (0.0, 0.55), (3.5, 0.55), (-1.75, -1.0), (1.75, -1.0)]
        ovals = VGroup(*[Ellipse(width=3.9, height=1.6, stroke_color=NICHE, stroke_width=4, fill_color=NICHE, fill_opacity=0.12).move_to([x, y, 0]) for x, y in pos])
        birds = VGroup(*[dot(ORG, 0.17, 0.85).move_to([x, y, 0]) for x, y in pos])
        self.at("So how can so many")
        self.play(Write(q), run_time=1.8)
        self.play(FadeIn(box), FadeIn(hl), run_time=0.8)
        cap = T("different niches", 34, NICHE, weight=BOLD).move_to([0, -2.85, 0])
        self.at("Different niches help")
        self.play(LaggedStart(*[Create(o) for o in ovals], lag_ratio=0.2), FadeIn(birds, lag_ratio=0.2, scale=0.5), FadeIn(cap), run_time=2.0)
        less = T("less competition", 34, COMP, weight=BOLD).move_to([0, -2.85, 0])
        self.at("compete less")
        self.play(FadeOut(cap), FadeIn(less, shift=UP * 0.1), run_time=0.7)
        more = T("more kinds of living things in one place", 32, BLUE, weight=BOLD).move_to([0, -2.85, 0])
        self.at("more kinds of living things")
        self.play(FadeOut(less), FadeIn(more, shift=UP * 0.1), Indicate(birds, color=ORG, scale_factor=1.12), run_time=1.0)
        bio = chip("biodiversity: the variety of living things in a place", BIO, size=28).move_to([0, -2.85, 0])
        self.at("The variety of living things")
        self.play(FadeOut(more), FadeIn(bio, scale=0.95), run_time=0.8)
        spots = [(-1.85, 0.5), (1.85, 0.5), (-0.9, -0.2), (0.9, -0.2)]
        # lens centres between neighbouring ovals (they overlap a little)
        lens = [(-1.75, 0.55), (1.75, 0.55), (-0.9, -0.2), (0.9, -0.2)]
        marks = VGroup(*[dot(COMP, 0.1, 0.9).move_to([x, y, 0]) for x, y in lens])
        some = T("some competition stays", 32, COMP, weight=BOLD).move_to([0, -2.85, 0])
        self.at("Using a place differently")
        self.play(FadeOut(bio), FadeIn(marks, scale=0.4), FadeIn(some), run_time=0.9)
        helps = T("but it helps", 34, NICHE, weight=BOLD).move_to([0, -2.85, 0])
        self.at("But it helps")
        self.play(FadeOut(some), FadeIn(helps, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Different niches let more kinds share one place."
