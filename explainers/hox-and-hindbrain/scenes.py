"""Hox genes and the hindbrain: a gradient writes the address  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = retinoic acid (the drug, the drops, the gradient, the dose)
  GREEN  = made / switched on (Raldh2, a gene that is on, the right dose)
  RED    = destroyed / harmful (Cyp26, the wrong dose)
  BLUE   = the retinoic acid receptors (RAR, RXR)
  PURPLE = Hox genes and the Hox code (four shades = four gene groups; seven abstract shades = each rhombomere's mix)
  GOLD   = the short DNA stretch the receptor pair binds
  TEAL   = trigeminal identity (jaw, chewing)
  YELLOW = facial identity (face, facial expression)
  GREY   = bulges, DNA, nucleus, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
HOX = ["#DCC8F4", "#C39EE6", "#A573CF", "#8650B8"]   # four Hox gene groups, 3' to 5'

# one shared hindbrain strip, same place in every scene that shows it
SX = [-4.8 + 1.6 * i for i in range(7)]   # bulge centres
SY, SH, SW = 0.0, 3.0, 1.5
TAGY = -2.3


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bulge(i, fill=GREY, op=0.15, h=SH, y=SY):
    return RoundedRectangle(corner_radius=0.3, width=SW, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=fill, fill_opacity=op).move_to([SX[i], y, 0])


def strip(op=0.15, h=SH, y=SY):
    return VGroup(*[bulge(i, op=op, h=h, y=y) for i in range(7)])


def rlabels(bs, size=24):
    return VGroup(*[T(f"r{i + 1}", size, GREY).move_to(b.get_top() + DOWN * 0.38) for i, b in enumerate(bs)])


def front_back(y):
    f = T("front", 24, GREY).move_to([SX[0], y, 0])
    b = T("back", 24, GREY).move_to([SX[6], y, 0])
    return VGroup(f, b)


def tag(i, y=TAGY, pat=None):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.15, height=0.8, stroke_color=GREY, stroke_width=2.5),
                         num_dashes=30)
    g = VGroup(box)
    if pat is None:
        g.add(T("?", 34, GREY))
    else:
        for j, on in enumerate(pat):
            sq = Square(0.24, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9 if on else 0.0)
            g.add(sq.move_to([-0.34 + 0.34 * j, 0, 0]))
    return g.move_to([SX[i], y, 0])


# Abstract "mix" tags: each rhombomere gets its own purple shade. The shades stand for
# "a different combination", not for any particular set of Hox genes.
MIX = ["#EDE2FA", "#D7C1F0", "#C1A0E6", "#AB80DB", "#9461CC", "#7C46B5", "#64339A"]


def pat_tag(i, shade_of=None, y=TAGY):
    k = i if shade_of is None else shade_of
    box = RoundedRectangle(corner_radius=0.12, width=1.15, height=0.8, stroke_color=PURPLE, stroke_width=2.5,
                           fill_color=MIX[k], fill_opacity=0.9)
    return box.move_to([SX[i], y, 0])


def drop(color=ORANGE, r=0.14):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def curve_pts(x0=-5.55, x1=5.55, base=1.9, peak=3.3, power=1.8, n=40):
    xs = np.linspace(x0, x1, n)
    t = (xs - x0) / (x1 - x0)
    return [np.array([x, base + (peak - base) * tt ** power, 0]) for x, tt in zip(xs, t)]


def curve_mobs(pts, base=1.9):
    line = VMobject(stroke_color=ORANGE, stroke_width=6)
    line.set_points_smoothly(pts)
    poly = Polygon(*([np.array([pts[0][0], base, 0])] + pts + [np.array([pts[-1][0], base, 0])]),
                   stroke_width=0, fill_color=ORANGE, fill_opacity=0.22)
    return line, poly


class S00Title(TitleCard):
    LESSON = "Hox genes and the hindbrain"
    TITLE = "A gradient writes the address"


# ---------------------------------------------------------------------------------------------
class S01Pill(SpokenScene):
    def construct(self):
        # pill -> face, with a question
        half1 = RoundedRectangle(corner_radius=0.3, width=0.9, height=0.6, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.9)
        half2 = RoundedRectangle(corner_radius=0.3, width=0.9, height=0.6, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.25).next_to(half1, RIGHT, buff=0)
        pill = VGroup(half1, half2).scale(1.7).rotate(PI / 7).move_to([-4.3, 0.6, 0])
        face = VGroup(Circle(radius=1.5, stroke_color=YELLOW, stroke_width=5),
                      Dot([-0.5, 0.35, 0], radius=0.1, color=YELLOW), Dot([0.5, 0.35, 0], radius=0.1, color=YELLOW),
                      Arc(radius=0.6, start_angle=PI * 1.2, angle=PI * 0.6, stroke_color=YELLOW, stroke_width=5).shift([0, -0.2, 0]))
        face.move_to([4.0, 0.6, 0])
        acne = T("acne", 26, ORANGE).next_to(pill, DOWN, buff=0.45)
        self.at("pill taken")
        self.play(FadeIn(pill, shift=RIGHT * 0.3), FadeIn(acne), run_time=0.7)
        self.at("change how a baby's face forms")
        self.play(FadeIn(face, scale=0.9), run_time=0.7)
        link = arr([-2.4, 0.6, 0], [2.2, 0.6, 0], GREY)
        q = T("?", 80, YELLOW, weight=BOLD).move_to([0, 1.7, 0])
        self.at("How can a drug")
        self.play(GrowArrow(link), FadeIn(q, scale=0.6), run_time=0.8)
        self.wait(self.beat(0.05))

        # to the hindbrain strip
        bs = strip()
        labs = rlabels(bs)
        self.at("Look at the")
        self.play(FadeOut(VGroup(pill, acne, face, link, q)), run_time=0.5)
        self.at("row of small")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bs], lag_ratio=0.12), run_time=1.1)
        title = T("rhombomeres", 32, GREY).move_to([0, 2.55, 0])
        self.at("called")
        self.play(FadeIn(title), FadeIn(labs), run_time=0.6)
        self.at("much alike")
        self.play(LaggedStart(*[Indicate(b, color=GREY, scale_factor=1.04) for b in bs], lag_ratio=0.08), run_time=1.0)
        self.at("Yet")
        self.play(bs[1].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.3), bs[3].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3),
                  run_time=0.6)
        jaw = T("jaw", 34, TEAL, weight=BOLD).move_to(bs[1].get_center())
        fce = T("face", 34, YELLOW, weight=BOLD).move_to(bs[3].get_center())
        self.at("the jaw")
        self.play(FadeIn(jaw, shift=UP * 0.15), run_time=0.4)
        self.at("move the face")
        self.play(FadeIn(fce, shift=UP * 0.15), run_time=0.4)
        tags = VGroup(*[tag(i) for i in range(7)])
        self.at("Each bulge")
        self.play(FadeIn(tags, shift=UP * 0.2, lag_ratio=0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Bath(SpokenScene):
    def construct(self):
        bs = strip()
        labs = rlabels(bs)
        fb = front_back(-1.85)
        self.add(bs, labs)
        self.play(FadeIn(fb), run_time=0.4)

        self.at("vitamin")
        ra = T("retinoic acid", 32, ORANGE, weight=BOLD).move_to([0, 3.15, 0])
        ra_drop = drop(r=0.26).move_to([0, 2.7, 0]).shift(LEFT * 2.2)
        self.play(FadeIn(ra, shift=DOWN * 0.1), FadeIn(ra_drop, scale=0.5), run_time=0.7)
        self.play(FadeOut(ra_drop), run_time=0.3)

        tap = bchip("Raldh2", GREEN, 28).move_to([4.1, -2.9, 0])
        self.at("makes it")
        self.play(FadeIn(tap, shift=UP * 0.2), run_time=0.6)
        up = arr(tap.get_top() + UP * 0.02, [4.1, -1.2, 0], GREEN)
        self.play(GrowArrow(up), run_time=0.4)

        drain = bchip("Cyp26", RED, 28).move_to([-4.1, -2.9, 0])
        self.at("destroy")
        self.play(FadeIn(drain, shift=UP * 0.2), run_time=0.6)
        dn = arr([-4.1, -1.2, 0], drain.get_top() + UP * 0.02, RED)
        self.play(GrowArrow(dn), run_time=0.4)

        # drops flow from tap to drain
        path = VMobject().set_points_as_corners([np.array([4.1, -1.2, 0]), np.array([3.6, -0.9, 0]),
                                                 np.array([-3.6, -0.9, 0]), np.array([-4.1, -1.2, 0])])
        drops = []
        for k in range(5):
            d = drop().move_to(path.get_start())
            drops.append(Succession(FadeIn(d, run_time=0.2),
                                    MoveAlongPath(d, path, run_time=2.2, rate_func=linear),
                                    FadeOut(d, run_time=0.2)))
        self.play(LaggedStart(*drops, lag_ratio=0.3), run_time=3.8)

        # gradient
        pts = curve_pts()
        line, poly = curve_mobs(pts)
        self.at("ends up high")
        self.play(Create(line), FadeIn(poly),
                  *[bs[i].animate.set_fill(ORANGE, 0.06 + 0.09 * i) for i in range(7)], run_time=1.3)
        hi = T("high", 28, ORANGE).move_to([SX[6] - 0.9, 2.55, 0])
        lo = T("low", 28, ORANGE).move_to([SX[0] + 0.1, 2.5, 0])
        self.play(FadeIn(hi), FadeIn(lo), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Read(SpokenScene):
    def construct(self):
        nuc = Ellipse(width=11.6, height=5.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([0, 0.0, 0])
        nlab = T("nucleus", 24, GREY).move_to([0, -2.55, 0])
        self.play(FadeIn(nuc), FadeIn(nlab), run_time=0.6)

        d = drop(r=0.3).move_to([-5.7, 2.9, 0])
        self.at("small and oily")
        self.play(FadeIn(d), run_time=0.3)
        self.at("reaches the nucleus")
        self.play(d.animate.move_to([-3.4, 1.4, 0]), run_time=1.0)

        rar = bchip("RAR", BLUE, 30).move_to([-1.3, 1.4, 0])
        self.at("receptor called")
        self.play(FadeIn(rar, shift=LEFT * 0.2), run_time=0.5)
        self.play(d.animate.next_to(rar, LEFT, buff=0.12), run_time=0.6)
        self.play(rar[1].animate.set_fill(BLUE, 0.4), run_time=0.3)

        rxr = bchip("RXR", BLUE, 30).move_to([2.3, 1.4, 0])
        self.at("pairs with")
        self.play(FadeIn(rxr, shift=RIGHT * 0.2), run_time=0.5)
        self.play(rxr.animate.next_to(rar, RIGHT, buff=0.04), run_time=0.6)
        pair = VGroup(d, rar, rxr)

        # DNA line, genes, binding stretches
        dna = Line([-4.9, -1.2, 0], [4.9, -1.2, 0], color=GREY, stroke_width=6)
        dlab = T("DNA", 24, GREY).move_to([0.3, -1.75, 0])
        site_a = Rectangle(width=0.7, height=0.36, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).move_to([-3.1, -1.2, 0])
        site_b = Rectangle(width=0.7, height=0.36, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).move_to([1.7, -1.2, 0])
        self.at("short stretch")
        self.play(Create(dna), FadeIn(dlab), FadeIn(site_a, scale=0.6), run_time=0.8)
        ga = bchip("Hoxa1", PURPLE, 28).move_to([-1.4, -1.2, 0])
        gb = bchip("Hoxb1", PURPLE, 28).move_to([3.4, -1.2, 0])
        self.at("such stretches")
        self.play(FadeIn(ga), FadeIn(gb), FadeIn(site_b, scale=0.6), run_time=0.7)
        self.play(Indicate(site_a, color=GOLD, scale_factor=1.25), Indicate(site_b, color=GOLD, scale_factor=1.25), run_time=0.7)
        self.at("When the pair")
        self.play(pair.animate.move_to([site_a.get_x() + 0.2, -0.45, 0]), run_time=0.8)
        on = T("on", 26, GREEN, weight=BOLD)
        self.at("comes on")
        self.play(*recolor(ga, GREEN), run_time=0.5)
        on.next_to(ga, DOWN, buff=0.25)
        self.play(FadeIn(on), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Order(SpokenScene):

    def construct(self):
        # one cluster on a chromosome
        cy = 3.0
        chrom = Line([-5.6, cy, 0], [5.6, cy, 0], color=GREY, stroke_width=5)
        clab = T("chromosome", 22, GREY).move_to([-4.6, cy + 0.55, 0])
        p3 = T("3′", 30, GREY, weight=BOLD).move_to([-5.9, cy, 0])
        p5 = T("5′", 30, GREY, weight=BOLD).move_to([5.9, cy, 0])
        xs = [-3.9, -1.3, 1.3, 3.9]
        chips = [bchip(f"Hox {k + 1}", HOX[k], 26).move_to([xs[k], cy, 0]) for k in range(4)]
        self.at("sit in a row")
        self.play(Create(chrom), FadeIn(clab), FadeIn(p3), FadeIn(p5), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.2), run_time=1.0)

        # a plain head-to-tail axis (schematic, not the rhombomere strip)
        ay = 1.0
        axis = Arrow([-5.6, ay, 0], [5.6, ay, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.3)
        fb = VGroup(T("front", 26, GREY).move_to([-5.0, ay + 0.5, 0]), T("back", 26, GREY).move_to([4.9, ay + 0.5, 0]))
        self.at("Their order")
        self.play(GrowArrow(axis), FadeIn(fb), run_time=0.7)
        bars, guides = [], []
        edge_x = [-4.4, -2.0, 0.4, 2.8]
        end_x = 5.3
        rows = [0.1, -0.65, -1.4, -2.15]
        for k in range(4):
            bar = Rectangle(width=end_x - edge_x[k], height=0.45, stroke_width=0, fill_color=HOX[k], fill_opacity=0.95)
            bar.move_to([(edge_x[k] + end_x) / 2, rows[k], 0])
            g = DashedLine([edge_x[k], ay - 0.1, 0], [edge_x[k], rows[k] + 0.25, 0], color=HOX[k], stroke_width=3)
            bars.append(bar); guides.append(g)
        self.at("front edges")
        self.play(LaggedStart(*[AnimationGroup(Create(g), GrowFromEdge(b, LEFT)) for g, b in zip(guides, bars)], lag_ratio=0.35), run_time=2.2)
        self.at("prime end")
        self.play(Indicate(chips[0], color=HOX[0], scale_factor=1.15), Indicate(bars[0], color=HOX[0], scale_factor=1.0), run_time=0.9)
        self.at("prime end", nth=1)
        self.play(Indicate(chips[3], color=HOX[3], scale_factor=1.15), Indicate(bars[3], color=HOX[3], scale_factor=1.0), run_time=0.9)

        # dose: all on at full signal, only the 3' gene at low signal
        self.at("In cells in a dish")
        lvl_w = 9.0
        frame = Rectangle(width=lvl_w, height=0.9, stroke_color=ORANGE, stroke_width=3).move_to([0, -1.0, 0])
        fill = Rectangle(width=lvl_w, height=0.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).move_to(frame)
        glab = T("retinoic acid", 28, ORANGE).next_to(frame, DOWN, buff=0.3)
        self.play(FadeOut(VGroup(axis, fb, *bars, *guides)),
                  *[c.animate.shift(DOWN * 1.1) for c in chips], chrom.animate.shift(DOWN * 1.1),
                  clab.animate.shift(DOWN * 1.1), p3.animate.shift(DOWN * 1.1), p5.animate.shift(DOWN * 1.1), run_time=0.7)
        frame.move_to([0, -0.9, 0]); fill.move_to(frame); glab.next_to(frame, DOWN, buff=0.3)
        self.play(FadeIn(frame), FadeIn(fill), FadeIn(glab), run_time=0.5)
        self.play(*[x for c in chips for x in recolor(c, GREEN)], run_time=0.5)
        self.at("lower doses")
        low = Rectangle(width=lvl_w * 0.22, height=0.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8)
        low.align_to(frame, LEFT).match_y(frame)
        self.play(Transform(fill, low),
                  *[x for c, col in zip(chips[1:], HOX[1:]) for x in recolor(c, col)], run_time=1.2)
        self.at("where the signal is lower")
        self.play(Indicate(frame, color=ORANGE, scale_factor=1.04), Indicate(chips[0], color=GREEN, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Code(SpokenScene):
    def construct(self):
        bs = strip()
        labs = rlabels(bs)
        self.add(bs, labs)
        tags = VGroup(*[tag(i) for i in range(7)])
        self.play(FadeIn(tags), run_time=0.5)
        self.at("its own mix")
        new = [pat_tag(i) for i in range(7)]
        self.play(LaggedStart(*[Transform(tags[i], new[i]) for i in range(7)], lag_ratio=0.15), run_time=1.6)
        addr = T("a different mix in each, with segment genes", 30, PURPLE, weight=BOLD).move_to([0, -3.3, 0])
        self.at("its address")
        self.play(FadeIn(addr, shift=UP * 0.1), Indicate(tags, color=PURPLE, scale_factor=1.05), run_time=0.9)

        chick = T("chick", 24, GREY).move_to([5.7, 3.3, 0])
        self.at("In the chick")
        self.play(FadeIn(chick), run_time=0.4)
        t_lab = T("trigeminal nerve", 28, TEAL, weight=BOLD).move_to([-3.2, 2.9, 0])
        t_sub = T("chewing", 24, TEAL).next_to(t_lab, DOWN, buff=0.12)
        f_lab = T("facial nerve", 28, YELLOW, weight=BOLD).move_to([1.6, 2.9, 0])
        f_sub = T("facial expression", 24, YELLOW).next_to(f_lab, DOWN, buff=0.12)
        n_t = Line([SX[1], SY + SH / 2, 0], [SX[1], 2.25, 0], color=TEAL, stroke_width=6)
        n_f = Line([SX[3], SY + SH / 2, 0], [SX[3], 2.25, 0], color=YELLOW, stroke_width=6)
        t_lab.move_to([(SX[1] + SX[2]) / 2, 3.1, 0]); f_lab.move_to([(SX[3] + SX[4]) / 2 + 0.3, 3.1, 0])
        t_sub.move_to([t_lab.get_center()[0], 2.6, 0]); f_sub.move_to([f_lab.get_center()[0], 2.6, 0])
        n_t = Line([SX[1], SY + SH / 2, 0], [SX[1], 2.25, 0], color=TEAL, stroke_width=6)
        n_f = Line([SX[3], SY + SH / 2, 0], [SX[3], 2.25, 0], color=YELLOW, stroke_width=6)
        self.at("trigeminal nerve")
        self.play(bs[1].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.3), bs[2].animate.set_stroke(TEAL, 5).set_fill(TEAL, 0.3),
                  Create(n_t), FadeIn(t_lab), run_time=0.8)
        self.at("chewing")
        self.play(FadeIn(t_sub), run_time=0.4)
        self.at("the facial nerve")
        self.play(bs[3].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3), bs[4].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3),
                  Create(n_f), FadeIn(f_lab), run_time=0.8)
        self.at("for facial expression")
        self.play(FadeIn(f_sub), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Dose(SpokenScene):
    def construct(self):
        bs = strip()
        for i in (1, 2):
            bs[i].set_stroke(TEAL, 5).set_fill(TEAL, 0.3)
        for i in (3, 4):
            bs[i].set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3)
        labs = rlabels(bs)
        tags = VGroup(*[pat_tag(i) for i in range(7)])
        self.add(bs, labs, tags)

        # the gradient from before, raised by extra signal
        pts = curve_pts(base=1.9, peak=3.0)
        line, poly = curve_mobs(pts)
        ra = T("retinoic acid", 28, ORANGE, weight=BOLD).move_to([-3.9, 3.0, 0])
        self.play(Create(line), FadeIn(poly), FadeIn(ra), run_time=0.7)
        self.at("extra retinoic acid early")
        pts2 = curve_pts(base=1.9, peak=3.3, power=0.8)
        line2, poly2 = curve_mobs(pts2)
        extra = T("extra", 28, ORANGE, weight=BOLD).move_to([-0.6, 3.25, 0])
        self.play(Transform(line, line2), Transform(poly, poly2), FadeIn(extra), run_time=1.0)
        self.at("Hox domains changed")
        new = [pat_tag(i) for i in range(7)]
        new[1] = pat_tag(1, 3); new[2] = pat_tag(2, 4)
        self.play(Transform(tags[1], new[1]), Transform(tags[2], new[2]), run_time=0.9)
        self.at("transformed toward")
        self.play(bs[1].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3), bs[2].animate.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.3),
                  run_time=1.0)
        self.at("The address follows")
        self.play(Indicate(tags, color=PURPLE, scale_factor=1.04), run_time=0.9)

        # the dose window
        self.at("In early pregnancy")
        self.play(FadeOut(VGroup(bs, labs, tags, line, poly, ra, extra)), run_time=0.6)
        zw = 3.4
        z_lo = Rectangle(width=zw, height=1.3, stroke_width=0, fill_color=RED, fill_opacity=0.45)
        z_ok = Rectangle(width=zw, height=1.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.5)
        z_hi = Rectangle(width=zw, height=1.3, stroke_width=0, fill_color=RED, fill_opacity=0.45)
        bar = VGroup(z_lo, z_ok, z_hi).arrange(RIGHT, buff=0).move_to([0, 0.2, 0])
        outline = Rectangle(width=zw * 3, height=1.3, stroke_color=GREY, stroke_width=3).move_to(bar)
        title = T("retinoic acid dose", 32, ORANGE, weight=BOLD).move_to([0, 1.9, 0])
        l_lo = T("too little", 28, RED).next_to(z_lo, DOWN, buff=0.35)
        l_ok = T("right dose", 28, GREEN).next_to(z_ok, DOWN, buff=0.35)
        l_hi = T("extra", 28, RED).next_to(z_hi, DOWN, buff=0.35)
        mk = Triangle(color=ORANGE, fill_color=ORANGE, fill_opacity=1, stroke_width=0).scale(0.28).rotate(PI)
        mk.move_to([z_ok.get_center()[0], bar.get_top()[1] + 0.3, 0])
        self.play(FadeIn(bar), FadeIn(outline), FadeIn(title), FadeIn(mk), FadeIn(l_ok), run_time=0.8)
        self.at("extra retinoic acid shifts")
        self.play(FadeIn(l_hi), mk.animate.move_to([z_hi.get_center()[0], bar.get_top()[1] + 0.3, 0]), run_time=0.8)
        self.at("Too little vitamin")
        self.play(FadeIn(l_lo), mk.animate.move_to([z_lo.get_center()[0], bar.get_top()[1] + 0.3, 0]), run_time=0.9)
        self.at("right in both")
        self.play(mk.animate.move_to([z_ok.get_center()[0], bar.get_top()[1] + 0.3, 0]), Indicate(z_ok, color=GREEN, scale_factor=1.05),
                  run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "The dose has to be right in both directions."
