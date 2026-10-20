"""Germs, vaccines and antibiotics: how we learned microbes cause disease (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  RED    = pathogen / microbe / bacterium / virus, and the disease or deaths it causes
  BLUE   = immune system: antibodies, memory cells, the antibody curve
  YELLOW = antigen, and the open question mark
  GREEN  = vaccine
  ORANGE = antibiotic
  TEAL   = ribosomes
  PURPLE = resistant bacteria
  GOLD   = chlorine handwashing (and the title rule)
  GREY   = frames, outlines, axes, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=ORANGE, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def cross_over(mob, color=TEXT):
    c = mob.get_center()
    w, h = mob.width * 0.5, mob.height * 0.5
    return VGroup(Line(c + [-w, h, 0], c + [w, -h, 0], color=color, stroke_width=6),
                  Line(c + [-w, -h, 0], c + [w, h, 0], color=color, stroke_width=6))


def dots(center, offsets, color=TEAL, r=0.11):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(np.array([center[0] + dx, center[1] + dy, 0.0]))
                    for dx, dy in offsets])


# ---------------------------------------------------------------------------------------------
# clinics (scenes 1 and 2)
# ---------------------------------------------------------------------------------------------
BASE = -1.9
H_FIRST, H_SECOND, H_FALL = 3.2, 0.9, 0.75


def clinic_frames():
    f1 = Rectangle(width=2.6, height=3.6, stroke_color=GREY, stroke_width=3).move_to([-3.2, BASE + 1.8, 0])
    f2 = Rectangle(width=2.6, height=3.6, stroke_color=GREY, stroke_width=3).move_to([3.2, BASE + 1.8, 0])
    n1 = T("First Clinic", 30).move_to([-3.2, -2.4, 0])
    n2 = T("Second Clinic", 30).move_to([3.2, -2.4, 0])
    ns = T("(not to scale)", 22, GREY).move_to([0, -2.4, 0])
    return f1, f2, n1, n2, ns


def col(x, h):
    return Rectangle(width=2.0, height=h, stroke_color=RED, stroke_width=3, fill_color=RED,
                     fill_opacity=0.4).move_to([x, BASE + h / 2, 0])


# ---------------------------------------------------------------------------------------------
# antibody-level sketch (scenes 3 and 4)
# ---------------------------------------------------------------------------------------------
T_FIRST, T_SECOND = 0.6, 9.5


def _g(s, tau):
    return 0.0 if s <= 0 else (s / (2 * tau)) ** 2 * float(np.exp(2 - s / tau))


def level(t):
    return 1.0 * _g(t - T_FIRST, 1.6) + 2.55 * _g(t - T_SECOND, 0.5)


def make_axes():
    ax = Axes(x_range=[0, 15, 1], y_range=[0, 3, 1], x_length=10.6, y_length=4.2, tips=False,
              axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3})
    ax.move_to([0.4, -0.35, 0])
    ylab = T("antibody level (relative units)", 22, GREY).rotate(PI / 2).move_to([ax.c2p(0, 1.5)[0] - 0.55, ax.c2p(0, 1.5)[1], 0])
    xlab = T("time, in this sketch", 22, GREY).move_to([ax.c2p(7.5, 0)[0], ax.c2p(0, 0)[1] - 0.4, 0])
    return ax, ylab, xlab


def marker(ax, t, color, text):
    x = ax.c2p(t, 0)[0]
    line = DashedLine([x, ax.c2p(0, 0)[1], 0], [x, 2.05, 0], color=color, stroke_width=3)
    c = bchip(text, color, 22)
    c.move_to([x - 0.2 + c.width / 2, 2.4, 0])
    return line, c


class S00Title(TitleCard):
    LESSON = "Germs, Vaccines and Antibiotics"
    TITLE = "How we learned microbes cause disease"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        f1, f2, n1, n2, ns = clinic_frames()
        self.at("had two")
        self.play(Create(f1), Create(f2), FadeIn(n1), FadeIn(n2), run_time=0.9)
        c1, c2 = col(-3.2, H_FIRST), col(3.2, H_SECOND)
        l1 = T("much larger share died", 24, RED).move_to([-3.2, 2.05, 0])
        l2 = T("smaller share died", 24, RED).move_to([3.2, 2.05, 0])
        self.at("much larger share")
        self.play(GrowFromEdge(c1, DOWN), GrowFromEdge(c2, DOWN), FadeIn(ns), run_time=1.0)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        fever = bchip("childbed fever: a serious infection", RED, 26).move_to([0, 3.0, 0])
        self.at("serious infection")
        self.play(FadeIn(fever, shift=DOWN * 0.15), run_time=0.6)
        why = T("Why?", 72, YELLOW, weight=BOLD).move_to([0, 0.1, 0])
        self.at("figure out why")
        self.play(FadeIn(why, scale=0.6), run_time=0.6)
        self.play(Indicate(why, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Germ(SpokenScene):
    def construct(self):
        f1, f2, n1, n2, ns = clinic_frames()
        c1, c2 = col(-3.2, H_FIRST), col(3.2, H_SECOND)
        l1 = T("much larger share died", 24, RED).move_to([-3.2, 2.05, 0])
        l2 = T("smaller share died", 24, RED).move_to([3.2, 2.05, 0])
        self.add(f1, f2, n1, n2, ns, c1, c2, l1, l2)
        r1 = T("doctors and medical students", 22, TEXT).move_to([-3.2, -2.85, 0])
        r1b = T("often worked with bodies", 22, TEXT).move_to([-3.2, -3.2, 0])
        r2 = T("midwives", 22, TEXT).move_to([3.2, -2.85, 0])
        self.at("The First Clinic trained doctors")
        self.play(FadeIn(r1), run_time=0.5)
        self.at("worked with bodies")
        self.play(FadeIn(r1b), run_time=0.5)
        self.at("The Second Clinic trained midwives")
        self.play(FadeIn(r2), run_time=0.5)

        chl = bchip("chlorine handwashing, 1847", GOLD, 24).move_to([-3.2, 3.0, 0])
        a = arr([-3.2, 2.65, 0], [-3.2, 2.3, 0], GOLD, 5, 0.18)
        self.at("washing hands in chlorine")
        self.play(FadeOut(l1), FadeIn(chl, shift=DOWN * 0.15), GrowArrow(a), run_time=0.7)
        fell = T("death ratio fell", 26, TEXT).move_to([-3.2, 1.95, 0])
        self.at("the death ratio")
        self.play(Transform(c1, col(-3.2, H_FALL)), FadeIn(fell), run_time=1.0)
        self.at("share of mothers")
        self.play(Indicate(fell, color=TEXT, scale_factor=1.1), run_time=0.6)

        # --- clear the clinics, show germ theory -----------------------------------------------
        head = T("germ theory", 54, font=TITLE_FONT).move_to([0, 3.0, 0])
        blob = Circle(radius=1.15, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.3).move_to([-3.8, 0.4, 0])
        blob_l = T("microbe", 38, RED).next_to(blob, UP, buff=0.25)
        dis = bchip("disease", RED, 42).move_to([3.9, 0.4, 0])
        link = arr([-2.5, 0.4, 0], [2.0, 0.4, 0], RED, 8, 0.3)
        gone = VGroup(f1, f2, n1, n2, ns, c1, c2, l2, r1, r1b, r2, chl, a, fell)
        self.at("Germ theory later")
        self.play(FadeOut(gone), run_time=0.5)
        self.play(Write(head), run_time=0.7)
        self.at("many diseases")
        self.play(FadeIn(blob, scale=0.7), FadeIn(blob_l), run_time=0.6)
        self.play(GrowArrow(link), FadeIn(dis), run_time=0.7)
        small = T("too small to see\nwithout a microscope", 28, TEXT, line_spacing=0.9).move_to([-3.8, -1.7, 0])
        self.at("too small to see")
        self.play(FadeIn(small), run_time=0.5)
        patho = T("pathogen", 46, RED, weight=BOLD).move_to([-0.3, 1.2, 0])
        self.at("microbe that causes disease")
        self.play(FadeIn(patho, shift=DOWN * 0.1), Indicate(link, color=RED), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Vaccine(SpokenScene):
    def construct(self):
        imm = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.0, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.1).move_to([4.0, 0.3, 0])
        imm_l = T("immune system", 28, BLUE).move_to([4.0, 1.4, 0])
        vac = bchip("vaccine", GREEN, 30).move_to([0, 2.75, 0])
        va = arr([1.0, 2.7, 0], [3.3, 1.85, 0], GREEN, 5, 0.2)
        self.at("A vaccine")
        self.play(FadeIn(vac, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(imm), FadeIn(imm_l), GrowArrow(va), run_time=0.8)

        cB = np.array([-4.2, 0.4, 0])
        blob = Circle(radius=1.1, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.3).move_to(cB)
        blob_l = T("pathogen", 28, RED).move_to([-4.2, -1.2, 0])
        self.at("recognize a pathogen")
        self.play(FadeIn(blob, scale=0.7), FadeIn(blob_l), run_time=0.6)

        full = bchip("full disease", RED, 28).move_to([0, -2.3, 0])
        xx = Line(full.get_left() + LEFT * 0.15, full.get_right() + RIGHT * 0.15, color=TEXT, stroke_width=6)
        self.at("full disease")
        self.play(FadeIn(full), run_time=0.4)
        self.play(Create(xx), run_time=0.5)

        angs = [60, 10, -40]
        sq_pos = [cB + 1.1 * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in angs]
        squares = VGroup(*[Square(0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(p) for p in sq_pos])
        ag_l = T("antigen", 28, YELLOW).move_to([-4.6, 2.1, 0])
        ag_a = arr([-4.1, 1.95, 0], [sq_pos[0][0] - 0.02, sq_pos[0][1] + 0.2, 0], YELLOW, 4, 0.16)
        self.at("an antigen")
        self.play(FadeIn(squares, scale=0.5), FadeIn(ag_l), GrowArrow(ag_a), run_time=0.7)

        starts = [[3.0, 0.8, 0], [3.0, 0.35, 0], [3.0, -0.1, 0]]
        bars = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.6, height=0.26, stroke_color=BLUE, stroke_width=2,
                                         fill_color=BLUE, fill_opacity=0.9).move_to(p) for p in starts])
        ab_l = T("antibodies", 28, BLUE).move_to([4.0, -0.75, 0])
        self.at("antibodies")
        self.play(FadeIn(bars), FadeIn(ab_l), run_time=0.6)
        self.at("stick to one antigen")
        targets = [p + [0.14 + 0.32, 0, 0] for p in sq_pos]
        self.play(*[b.animate.move_to(t) for b, t in zip(bars, targets)], ab_l.animate.move_to([-1.6, 1.0, 0]), run_time=1.4)

        diag = VGroup(imm, imm_l, vac, va, blob, blob_l, full, xx, squares, ag_l, ag_a, bars, ab_l)
        ax, ylab, xlab = make_axes()
        line1, chip1 = marker(ax, T_FIRST, GREEN, "vaccine: first meeting")
        curve1 = ax.plot(level, x_range=[0, T_SECOND], color=BLUE, stroke_width=6)
        self.at("The first time")
        self.play(FadeOut(diag), run_time=0.5)
        self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), run_time=0.8)
        self.play(Create(line1), FadeIn(chip1), run_time=0.5)
        self.at("is slow")
        self.play(Create(curve1, rate_func=linear), run_time=3.2)
        lab = T("slow, small first rise", 22, BLUE).move_to([ax.c2p(T_FIRST + 3.2, 1.0)[0] + 0.3, ax.c2p(0, 1.0)[1] + 0.5, 0])
        self.play(FadeIn(lab), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Memory(SpokenScene):
    def construct(self):
        ax, ylab, xlab = make_axes()
        line1, chip1 = marker(ax, T_FIRST, GREEN, "vaccine: first meeting")
        curve1 = ax.plot(level, x_range=[0, T_SECOND], color=BLUE, stroke_width=6)
        lab = T("slow, small first rise", 22, BLUE).move_to([ax.c2p(T_FIRST + 3.2, 1.0)[0] + 0.3, ax.c2p(0, 1.0)[1] + 0.5, 0])
        self.add(ax, ylab, xlab, line1, chip1, curve1, lab)

        mem = bchip("memory cells", BLUE, 28).move_to([ax.c2p(7.0, 0)[0], ax.c2p(0, 2.3)[1], 0])
        stay = T("stay in the body", 22, BLUE).next_to(mem, DOWN, buff=0.15)
        self.at("become memory cells")
        self.play(FadeIn(mem, scale=0.8), run_time=0.6)
        self.at("stay in the body")
        self.play(FadeIn(stay), run_time=0.5)

        line2, chip2 = marker(ax, T_SECOND, RED, "real pathogen")
        self.at("On a later exposure")
        self.play(Create(line2), FadeIn(chip2), run_time=0.6)
        curve2 = ax.plot(level, x_range=[T_SECOND, 15], color=BLUE, stroke_width=6)
        self.at("quickly make large amounts")
        self.play(Create(curve2, rate_func=linear), run_time=1.8)
        lab2 = T("faster, taller second rise", 22, BLUE).move_to([ax.c2p(13.0, 2.6)[0], ax.c2p(0, 2.55)[1] + 0.35, 0])
        self.play(FadeIn(lab2), run_time=0.4)
        self.at("gave the first meeting")
        self.play(Indicate(VGroup(*chip1[1:]), color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("meets the faster response")
        self.play(Indicate(VGroup(lab2), color=BLUE, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Antibiotic(SpokenScene):
    def construct(self):
        ab = bchip("antibiotic", ORANGE, 32).move_to([0, 2.9, 0])
        wall = RoundedRectangle(corner_radius=0.8, width=4.6, height=2.6, stroke_color=RED, stroke_width=9,
                                fill_color=RED, fill_opacity=0.12).move_to([-3.7, -0.1, 0])
        inner = RoundedRectangle(corner_radius=0.6, width=4.0, height=2.0, stroke_color=RED, stroke_width=2).move_to(wall)
        bact = VGroup(wall, inner)
        bact_l = T("bacterium", 28, RED).move_to([-4.6, -1.75, 0])
        cell_wall_l = T("cell wall", 26, RED).move_to([-3.9, 1.7, 0])
        offs = [(-1.2, 0.3), (-0.5, -0.4), (0.2, 0.5), (0.8, -0.2), (-0.9, -0.6), (0.4, -0.55), (-0.2, 0.05)]
        rib_b = dots([-3.7, -0.1], [(dx - 0.1, dy) for dx, dy in offs])
        rib_b_l = T("ribosomes", 26, TEAL).move_to([-2.4, -1.75, 0])

        self.at("An antibiotic")
        self.play(FadeIn(ab, shift=DOWN * 0.15), FadeIn(bact, scale=0.9), FadeIn(bact_l), run_time=0.8)
        self.at("kills bacteria")
        self.play(Indicate(bact, color=RED, scale_factor=1.04), run_time=0.7)
        self.at("stops them growing")
        self.play(Indicate(bact, color=RED, scale_factor=1.04), run_time=0.7)
        hit_wall = inhib([-0.4, 2.55, 0], [-2.0, 1.25, 0], ORANGE)
        self.at("Many antibiotics block")
        self.play(FadeIn(cell_wall_l), Create(hit_wall), run_time=0.8)
        hit_rib = inhib([-0.2, 2.55, 0], [-2.7, 0.1, 0], ORANGE)
        self.at("jam bacterial ribosomes")
        self.play(FadeIn(rib_b), FadeIn(rib_b_l), Create(hit_rib), run_time=0.8)
        dead = T("killed or stopped", 24, TEXT).move_to([-3.7, -2.3, 0])
        self.at("make proteins")
        self.play(bact.animate.set_opacity(0.35), rib_b.animate.set_opacity(0.35), FadeIn(dead), run_time=0.7)

        host = RoundedRectangle(corner_radius=0.6, width=4.8, height=2.8, stroke_color=GREY, stroke_width=4).move_to([3.9, -0.1, 0])
        host_l = T("cell it infects", 26, GREY).move_to([3.9, -1.8, 0])
        vir = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.8, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.3).move_to([2.9, 0.2, 0])
        vir_l = T("virus", 26, RED).move_to([2.9, 0.8, 0])
        none_l = T("no cell wall, no ribosomes", 22, TEXT).move_to([3.9, -2.4, 0])
        none_l2 = T("of its own", 22, TEXT).move_to([3.9, -2.75, 0])
        self.at("A virus")
        self.play(FadeIn(host), FadeIn(host_l), FadeIn(vir, scale=0.7), FadeIn(vir_l), run_time=0.8)
        self.at("no cell wall")
        self.play(FadeIn(none_l), FadeIn(none_l2), run_time=0.6)
        rib_h = dots([4.5, -0.15], [(-0.5, 0.4), (0.3, 0.5), (0.5, -0.3), (-0.4, -0.5), (0.0, 0.0)])
        rib_h_l = T("ribosomes", 24, TEAL).move_to([4.7, 0.9, 0])
        use = arr([3.4, 0.2, 0], [4.0, 0.0, 0], GREY, 4, 0.18)
        self.at("uses the ribosomes")
        self.play(FadeIn(rib_h), FadeIn(rib_h_l), GrowArrow(use), run_time=0.8)
        hit_v = inhib([0.6, 2.55, 0], [2.8, 1.4, 0], ORANGE)
        no_t = T("no target", 28, ORANGE, weight=BOLD).move_to([5.2, 1.9, 0])
        self.at("do not treat")
        self.play(Create(hit_v), FadeIn(no_t), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Resistance(SpokenScene):
    def construct(self):
        title = bchip("antibiotic resistance", PURPLE, 30).move_to([0, 3.0, 0])
        self.at("Antibiotic resistance")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)

        box = RoundedRectangle(corner_radius=0.2, width=9.8, height=3.6, stroke_color=GREY, stroke_width=3).move_to([0, 0.3, 0])
        xs = [-3.75, -2.25, -0.75, 0.75, 2.25, 3.75]
        ys = [1.3, 0.3, -0.7]
        slots = [np.array([x, y, 0]) for y in ys for x in xs]
        resistant_idx = [4, 8, 15]
        pop = []
        for i, p in enumerate(slots):
            if i in resistant_idx:
                d = Circle(radius=0.25, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8)
            else:
                d = Circle(radius=0.25, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.35)
            pop.append(d.move_to(p))
        sens = VGroup(*[d for i, d in enumerate(pop) if i not in resistant_idx])
        resi = VGroup(*[pop[i] for i in resistant_idx])
        sens_l = T("sensitive bacteria", 24, RED).move_to([-3.0, -1.95, 0])
        resi_l = T("resistant: carry a gene", 24, PURPLE).move_to([3.0, -1.95, 0])
        sch = T("(schematic, not to scale)", 22, GREY).move_to([0, -2.6, 0])
        self.at("some bacteria")
        self.play(Create(box), FadeIn(VGroup(*pop), lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(sens_l), FadeIn(sch), run_time=0.4)
        self.at("large population")
        self.play(Indicate(box, color=GREY, scale_factor=1.03), run_time=0.8)
        self.at("a few may already carry a gene")
        self.play(FadeIn(resi_l), Indicate(resi, color=PURPLE, scale_factor=1.5), run_time=1.0)

        ab = bchip("antibiotic", ORANGE, 30).move_to([0, 3.0, 0])
        self.at("The antibiotic kills")
        self.play(ReplacementTransform(title, ab), run_time=0.5)
        self.play(LaggedStart(*[FadeOut(d, scale=0.2) for d in sens], lag_ratio=0.06), run_time=1.6)

        # resistant ones multiply into every emptied slot
        newdots = []
        anims = []
        for i, p in enumerate(slots):
            if i in resistant_idx:
                continue
            src = slots[min(resistant_idx, key=lambda j: np.linalg.norm(slots[j] - p))]
            d = Circle(radius=0.25, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8).move_to(src)
            newdots.append(d)
            anims.append(d.animate.move_to(p))
        self.at("left to multiply")
        self.add(*newdots)
        self.play(LaggedStart(*anims, lag_ratio=0.05), FadeOut(sens_l), run_time=2.0)

        ns = bchip("natural selection", GOLD, 30).move_to([0, 3.0, 0])
        self.at("natural selection")
        self.play(ReplacementTransform(ab, ns), run_time=0.5)

        c1 = bchip("Vaccines do not work perfectly in everyone", GREEN, 26).move_to([0, -2.1, 0])
        c2 = bchip("Resistant bacteria survive the drug", PURPLE, 26).move_to([0, -3.05, 0])
        self.at("not always succeed")
        self.play(FadeOut(resi_l), FadeOut(sch), run_time=0.4)
        self.at("Vaccines do not work")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("resistant bacteria survive")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Vaccines build memory. Antibiotics do not work on viruses."
