"""Niches and distributions: a missing plant is not a limit  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = natural plants / a population that replaces itself (lambda at least 1)
  YELLOW = plants planted by the researchers (transplants)
  BLUE   = conditions: niche space, the abiotic limit
  ORANGE = other species: neighbours, the biotic limit
  TEAL   = arrival and dispersal: immigrants, the dispersal limit
  RED    = failure: a decline, lambda below 1, a failed planting
  GOLD   = lambda (the finite rate of increase)
  GREY   = the map, the sea, outlines, de-emphasized things
  TEXT   = the northern limit line
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

LAND_X0, LAND_X1 = -4.6, -0.6
MAP_Y0, MAP_Y1 = -3.3, 3.3
EDGE_Y = 0.8


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def coast_x(y):
    return LAND_X0 + 0.14 * np.sin(2.6 * y)


def build_coast():
    """land polygon with a wavy west coast, a 'sea' label and a north arrow."""
    ys = np.linspace(MAP_Y0, MAP_Y1, 40)
    pts = [[coast_x(y), y, 0] for y in ys] + [[LAND_X1, MAP_Y1, 0], [LAND_X1, MAP_Y0, 0]]
    land = Polygon(*pts, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16)
    sea = T("sea", 24, GREY).move_to([-5.55, -1.2, 0])
    north = VGroup(Arrow([-5.55, 1.6, 0], [-5.55, 2.7, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22),
                   T("N", 26, GREY, weight=BOLD).move_to([-5.55, 3.0, 0]))
    return VGroup(land, sea, north)


def edge_line():
    ln = DashedLine([coast_x(EDGE_Y) - 0.05, EDGE_Y, 0], [LAND_X1 + 0.1, EDGE_Y, 0], color=TEXT, stroke_width=4,
                    dash_length=0.18)
    lbl = T("northern limit", 24, TEXT).move_to([LAND_X1 + 0.25 + 1.2, EDGE_Y, 0])
    return VGroup(ln, lbl)


def dot(p, color, r=0.085):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([p[0], p[1], 0])


def natural_dots():
    rng = np.random.RandomState(3)
    out = []
    for i in range(5):
        for j in range(6):
            if rng.rand() < 0.3:
                continue
            x = -4.0 + i * 0.7 + rng.uniform(-0.15, 0.15)
            y = -2.9 + j * 0.55 + rng.uniform(-0.1, 0.1)
            out.append(dot((x, y), GREEN))
    return VGroup(*out)


def planted_positions(n):
    pos = []
    for j in range(3):
        for i in range(6):
            pos.append((-3.55 + i * 0.55, 1.75 + j * 0.45))
    return pos[:n]


def planted(n):
    return VGroup(*[dot(p, YELLOW) for p in planted_positions(n)])


def base_map(with_dots=True):
    land = build_coast()
    edge = edge_line()
    nat = natural_dots() if with_dots else VGroup()
    return land, edge, nat


def bar(x, h, color, w=1.3, base=-2.6, op=0.85):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([x, base + h / 2, 0])


class S00Title(TitleCard):
    LESSON = "Distributions, niches and tolerances"
    TITLE = "A Missing Plant Is Not a Limit"


# ---------------------------------------------------------------------------------------------
class S01Tripled(SpokenScene):
    """coast map, plants stop at the limit; planted dots beyond it grow; a bar more than triples; why not there?"""

    def construct(self):
        land, edge, nat = base_map()
        self.at("coastal dune plant")
        self.play(FadeIn(land), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in nat], lag_ratio=0.04), run_time=1.2)
        self.at("northern limit")
        self.play(Create(edge[0]), FadeIn(edge[1]), run_time=0.9)

        pl4 = planted(4)
        brace = DoubleArrow([-0.55, EDGE_Y + 0.08, 0], [-0.55, 2.6, 0], buff=0, color=GREY, stroke_width=4,
                            tip_length=0.18)
        km = T("about 60 km", 24, GREY).move_to([0.7, 1.7, 0])
        self.at("beyond that limit")
        self.play(FadeIn(pl4, scale=0.4), run_time=0.7)
        self.play(GrowFromCenter(brace), FadeIn(km), run_time=0.7)

        self.at("years later")
        b1 = bar(3.7, 1.2, YELLOW)
        b2 = bar(5.6, 1.2, YELLOW)
        l1 = T("planted", 24, YELLOW).next_to(b1, DOWN, buff=0.15)
        l2 = VGroup(T("12 to 14", 24, YELLOW), T("years later", 24, YELLOW)).arrange(DOWN, buff=0.05).next_to(b2, DOWN, buff=0.15)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2), run_time=0.7)
        pl14 = planted(14)
        self.at("more than tripled")
        b2n = bar(5.6, 4.2, YELLOW)
        tag = T("more than tripled", 26, YELLOW).move_to([4.65, 2.2, 0])
        self.play(Transform(b2, b2n), ReplacementTransform(pl4, pl14), FadeIn(tag), run_time=1.4)

        self.at("can live there")
        self.play(Indicate(pl14, color=YELLOW, scale_factor=1.12), run_time=0.8)
        q_arrow = DashedLine([-2.6, EDGE_Y - 0.3, 0], [-2.6, EDGE_Y + 0.55, 0], color=TEXT, stroke_width=3)
        q = T("?", 44, TEXT, weight=BOLD).move_to([-2.1, 1.27, 0])
        self.at("never got there")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.play(Indicate(q, color=TEXT, scale_factor=1.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Niche(SpokenScene):
    """niche space (axes, region) beside geographic space (map patches); a suitable patch is empty."""

    def construct(self):
        # --- left: niche space ----------------------------------------------------------------
        ox, oy = -5.7, -2.3
        xax = Arrow([ox, oy, 0], [ox + 4.9, oy, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        yax = Arrow([ox, oy, 0], [ox, oy + 4.3, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        xl = T("temperature", 26, BLUE).move_to([ox + 2.5, oy - 0.45, 0])
        yl = T("soil moisture", 26, BLUE).rotate(PI / 2).move_to([ox - 0.5, oy + 2.1, 0])
        blob = Ellipse(width=2.9, height=2.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.28)
        blob.move_to([ox + 2.5, oy + 2.2, 0])
        nlbl = T("niche", 30, BLUE, weight=BOLD).move_to(blob)
        title_n = T("Niche space", 32, BLUE, weight=BOLD).move_to([ox + 2.4, 2.75, 0])

        self.at("The answer starts")
        frame_n = VGroup(xax.copy().set_opacity(0.25), yax.copy().set_opacity(0.25))
        self.play(FadeIn(frame_n), run_time=0.5)
        self.at("set of conditions")
        self.play(GrowFromCenter(blob), FadeIn(nlbl), run_time=0.9)
        self.at("Temperature and soil moisture")
        self.play(ReplacementTransform(frame_n, VGroup(xax, yax)), FadeIn(xl), FadeIn(yl), run_time=0.9)
        self.at("Niche space is")
        self.play(FadeIn(title_n, shift=DOWN * 0.1), run_time=0.5)

        # --- right: geographic space ------------------------------------------------------------
        mx0, mx1, my0, my1 = 0.9, 6.3, -2.9, 2.3
        mp = Rectangle(width=mx1 - mx0, height=my1 - my0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=0.14).move_to([(mx0 + mx1) / 2, (my0 + my1) / 2, 0])
        title_g = T("Geographic space", 32, GREY, weight=BOLD).move_to([(mx0 + mx1) / 2, 2.75, 0])

        def patch(cx, cy, w=1.5, h=1.0, color=GREY):
            return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=0.12).move_to([cx, cy, 0])
        pa, pb, pc, pd = patch(2.0, 1.2), patch(5.0, 0.3), patch(2.3, -1.3), patch(5.1, -1.3, 1.3, 0.9)
        dots_a = VGroup(*[dot((2.0 + dx, 1.2 + dy), GREEN) for dx, dy in [(-0.4, 0.1), (0.0, -0.2), (0.35, 0.15), (0.1, 0.25)]])
        dots_b = VGroup(*[dot((5.0 + dx, 0.3 + dy), GREEN) for dx, dy in [(-0.45, -0.1), (0.1, 0.2), (0.4, -0.15)]])

        self.at("Geographic space")
        self.play(FadeIn(mp), FadeIn(title_g), FadeIn(VGroup(pa, pb, pc, pd)), run_time=0.6)
        self.at("is the map")
        hit = [patch(*p.get_center()[:2], w=p.width, h=p.height, color=BLUE) for p in (pa, pb, pc)]
        self.play(*[Transform(p, h) for p, h in zip((pa, pb, pc), hit)],
                  Indicate(blob, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.play(FadeIn(dots_a), FadeIn(dots_b), run_time=0.5)
        lbl_c = VGroup(T("suitable,", 24, TEAL), T("not reached", 24, TEAL)).arrange(DOWN, buff=0.04).next_to(pc, DOWN, buff=0.2)
        self.at("has not reached it")
        self.play(FadeIn(lbl_c), Indicate(pc, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lambda(SpokenScene):
    """lambda as this-year / next-year bars; a sink is held up by immigrants; presence is not the niche."""

    def construct(self):
        b0x, b1x, base, h0 = -3.2, 0.9, -2.6, 2.8
        lam = T("λ", 44, GOLD, weight=BOLD)
        lam_name = T("lambda: the finite rate of increase", 28, GOLD).move_to([-0.4, 3.1, 0])
        this_bar = bar(b0x, h0, GREEN)
        this_lbl = T("this year", 26, GREY).move_to([b0x, base - 0.4, 0])
        next_lbl = T("next year", 26, GREY).move_to([b1x, base - 0.4, 0])

        self.at("We use lambda")
        self.play(FadeIn(lam_name, shift=DOWN * 0.1), run_time=0.7)
        self.at("multiplies in one year")
        self.play(FadeIn(this_bar, shift=UP * 0.2), FadeIn(this_lbl), run_time=0.7)
        mult = VGroup(Arrow([b0x + 0.85, base + 1.3, 0], [b1x - 0.85, base + 1.3, 0], buff=0, color=GOLD,
                            stroke_width=6, tip_length=0.25), T("× λ", 34, GOLD, weight=BOLD)).arrange(DOWN, buff=0.12)
        mult.move_to([(b0x + b1x) / 2, base + 1.6, 0])
        next_bar = bar(b1x, h0 * 1.3, GREEN)
        self.play(FadeIn(mult), FadeIn(next_lbl), run_time=0.6)
        self.play(GrowFromEdge(next_bar, DOWN), run_time=0.9)

        self.at("one or more")
        verdict = VGroup(T("λ ≥ 1", 40, GREEN, weight=BOLD), T("replaces itself", 28, GREEN)).arrange(DOWN, buff=0.15)
        verdict.move_to([4.9, 0.2, 0])
        self.play(FadeIn(verdict, shift=LEFT * 0.2), run_time=0.7)

        # --- reset for the sink case ------------------------------------------------------------
        self.at("A sink population")
        sink_next = bar(b1x, 2.0, RED)
        self.play(FadeOut(verdict), Transform(next_bar, sink_next), run_time=0.8)
        sink_lbl = VGroup(T("sink population", 32, RED, weight=BOLD), T("λ below 1 on its own", 26, RED)).arrange(DOWN, buff=0.15)
        sink_lbl.move_to([4.9, -0.9, 0])
        self.play(FadeIn(sink_lbl, shift=LEFT * 0.2), run_time=0.5)
        self.at("deaths exceed births")
        self.play(Indicate(next_bar, color=RED, scale_factor=1.05), run_time=0.7)

        topup = Rectangle(width=1.3, height=h0 - 2.0, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                          fill_opacity=0.5).move_to([b1x, base + 2.0 + (h0 - 2.0) / 2, 0])
        imm = VGroup(Arrow([b1x + 0.2, base + h0 + 1.15, 0], [b1x + 0.2, base + h0 + 0.05, 0], buff=0, color=TEAL, stroke_width=6, tip_length=0.22),
                     T("immigrants", 26, TEAL).move_to([b1x + 0.2, base + h0 + 1.5, 0]))
        self.at("immigrants keep it going")
        self.play(GrowFromEdge(topup, DOWN), FadeIn(imm), run_time=0.9)

        # --- presence on a map is not the niche ---------------------------------------------------
        self.at("presence on a map")
        self.play(*[FadeOut(m) for m in (this_bar, this_lbl, next_bar, next_lbl, mult, topup, imm, sink_lbl, lam_name)],
                  run_time=0.6)
        c1 = chip("present on a map", GREEN, size=36).move_to([0, 1.6, 0])
        c2 = chip("where the niche ends", BLUE, size=36).move_to([0, -1.4, 0])
        neq = T("does not show", 34, TEXT).move_to([0, 0.1, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.6)
        self.at("does not show")
        self.play(FadeIn(neq), FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Causes(SpokenScene):
    """the edge, three possible causes beyond it in turn, then the direct test: plant beyond the edge."""

    def construct(self):
        land, edge, nat = base_map()
        self.add(land, edge, nat)

        def cause(name, sub, color):
            c = chip(name, color, size=30)
            s = T(sub, 26, GREY)
            return VGroup(c, s).arrange(DOWN, buff=0.12)
        c1 = cause("conditions", "abiotic limit", BLUE).move_to([4.3, 2.0, 0])
        c2 = cause("other species", "biotic limit", ORANGE).move_to([4.3, 0.2, 0])
        c3 = cause("not arrived", "dispersal limit", TEAL).move_to([4.3, -1.6, 0])

        beyond = Rectangle(width=LAND_X1 - LAND_X0 - 0.1, height=MAP_Y1 - EDGE_Y - 0.1, stroke_width=0, fill_color=BLUE,
                           fill_opacity=0.25).move_to([(LAND_X0 + LAND_X1) / 2 + 0.02, (MAP_Y1 + EDGE_Y) / 2, 0])
        wrong = T("conditions wrong?", 28, BLUE).move_to([-2.6, 2.1, 0])

        self.at("three causes")
        self.play(Indicate(edge[0], color=TEXT, scale_factor=1.0, run_time=0.8))

        self.at("could be wrong")
        self.play(FadeIn(beyond), FadeIn(wrong), FadeIn(c1, shift=LEFT * 0.2), run_time=0.8)

        neigh = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([-3.8 + i * 0.55, 1.5 + (i % 3) * 0.55, 0])
                         for i in range(6)])
        in_way = T("other species in the way?", 26, ORANGE).move_to([-2.6, 3.0, 0])
        self.at("in the way")
        self.play(FadeOut(beyond), FadeOut(wrong), FadeIn(neigh, scale=0.5), FadeIn(c2, shift=LEFT * 0.2), run_time=0.8)

        arrow_up = Arrow([-2.6, EDGE_Y - 1.6, 0], [-2.6, EDGE_Y - 0.1, 0], buff=0, color=TEAL, stroke_width=8, tip_length=0.3)
        stop = Line([-3.2, EDGE_Y + 0.05, 0], [-2.0, EDGE_Y + 0.05, 0], color=TEAL, stroke_width=1)
        hold = T("never arrived?", 26, TEAL).move_to([-2.6, 2.2, 0])
        self.at("not have arrived")
        self.play(FadeOut(neigh), FadeIn(c3, shift=LEFT * 0.2), GrowArrow(arrow_up), FadeIn(hold), run_time=0.9)

        pl = planted(10)
        self.at("plant the species beyond the edge")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(arrow_up), FadeOut(hold), run_time=0.5)
        self.play(FadeIn(pl, scale=0.4), run_time=0.8)
        test = chip("plant beyond the edge", YELLOW, size=30).move_to([4.3, 1.8, 0])
        self.at("follow it")
        self.play(FadeIn(test, shift=LEFT * 0.2), Indicate(pl, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Controls(SpokenScene):
    """same planting inside the range; failed controls; cleared and left plots; the whole life cycle -> lambda."""

    def construct(self):
        land, edge, nat = base_map(with_dots=False)
        self.add(land, edge)
        inside = [(-3.4, -2.4), (-2.6, -1.3), (-1.8, -0.2)]
        beyond_pts = [(-3.2, 1.7), (-2.0, 2.4)]
        sites_in = VGroup(*[Square(side_length=0.36, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y, 0]) for x, y in inside])
        sites_out = VGroup(*[Square(side_length=0.36, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y, 0]) for x, y in beyond_pts])
        in_lbl = T("inside the range", 24, GREY).move_to([-2.6, -2.95, 0])
        same = chip("same handling at every site", YELLOW, size=22).move_to([4.2, 2.6, 0])

        self.at("plants the same way")
        self.play(FadeIn(sites_in, scale=0.5), FadeIn(sites_out, scale=0.5), FadeIn(same, shift=LEFT * 0.2), run_time=0.9)

        crosses = VGroup(*[Cross(s, stroke_color=RED, stroke_width=6, scale_factor=1.3) for s in list(sites_in) + list(sites_out)])
        why = VGroup(T("all fail:", 30, RED, weight=BOLD), T("handling or a bad year", 28, RED)).arrange(DOWN, buff=0.12).move_to([4.2, 0.3, 0])
        self.at("fail too")
        self.play(*[Create(c) for c in crosses], FadeIn(why), run_time=1.0)

        # --- reset: the failure case is cleared before the next idea ------------------------------
        cleared = VGroup(Square(side_length=1.5, stroke_color=YELLOW, stroke_width=3, fill_opacity=0),
                         dot((0, 0), YELLOW, 0.14)).move_to([2.9, -0.2, 0])
        left_sq = VGroup(Square(side_length=1.5, stroke_color=YELLOW, stroke_width=3, fill_opacity=0),
                         dot((0, 0), YELLOW, 0.14),
                         *[Square(side_length=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(p)
                           for p in [(-0.45, 0.45, 0), (0.45, 0.4, 0), (-0.4, -0.45, 0), (0.48, -0.4, 0)]]).move_to([5.5, -0.2, 0])
        cl = VGroup(T("neighbours", 24, ORANGE), T("cleared", 24, ORANGE)).arrange(DOWN, buff=0.04).next_to(cleared, DOWN, buff=0.25)
        ll = VGroup(T("neighbours", 24, ORANGE), T("left", 24, ORANGE)).arrange(DOWN, buff=0.04).next_to(left_sq, DOWN, buff=0.25)
        rnd = VGroup(T("half and half,", 24, GREY), T("chosen at random", 24, GREY)).arrange(DOWN, buff=0.05).move_to([4.2, 1.5, 0])
        self.at("cross the planting")
        self.play(FadeOut(crosses), FadeOut(why), FadeOut(same), run_time=0.5)
        self.play(FadeIn(cleared, scale=0.6), FadeIn(left_sq, scale=0.6), FadeIn(cl), FadeIn(ll), run_time=0.8)
        self.at("chosen at random")
        self.play(FadeIn(rnd), run_time=0.5)

        # --- whole life cycle -----------------------------------------------------------------------
        self.at("whole life cycle")
        self.play(FadeOut(cleared), FadeOut(left_sq), FadeOut(cl), FadeOut(ll), FadeOut(rnd), run_time=0.5)
        stages = [("survival", GREEN), ("growth", GREEN), ("reproduction", GREEN)]
        chips = [chip(n, c, size=26) for n, c in stages]
        grp = VGroup(*chips).arrange(DOWN, buff=0.55).move_to([3.7, 0.2, 0])
        links = [Arrow(chips[i].get_bottom(), chips[i + 1].get_top(), buff=0.05, color=GREY, stroke_width=4, tip_length=0.18) for i in range(2)]
        lam = chip("λ", GOLD, size=40).move_to([5.9, 0.2, 0])
        to_lam = Arrow(grp.get_right() + RIGHT * 0.05, lam.get_left(), buff=0.05, color=GOLD, stroke_width=5, tip_length=0.22)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.3), *[GrowArrow(a) for a in links], run_time=1.0)

        self.at("year growth")
        down = Arrow(chips[1].get_right() + LEFT * 0.0 + RIGHT * 0.2, chips[1].get_right() + RIGHT * 0.2 + DOWN * 0.9, buff=0, color=RED, stroke_width=7, tip_length=0.25)
        self.play(Indicate(chips[1], color=RED, scale_factor=1.1), run_time=0.7)
        self.at("cannot replace itself")
        self.play(Indicate(grp, color=GREY, scale_factor=1.04), run_time=0.7)
        self.at("Estimate lambda")
        self.play(GrowArrow(to_lam), FadeIn(lam, scale=0.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Read(SpokenScene):
    """three outcomes of lambda beyond the range read as dispersal, biotic or abiotic; then the rule."""

    def construct(self):
        def row(l1, l2, name, color, y):
            a = T(l1, 28, TEXT, weight=BOLD)
            b = T(l2, 24, GREY)
            left = VGroup(a, b).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            left.move_to([-6.3 + left.width / 2, y, 0])
            ar = Arrow([left.get_right()[0] + 0.25, y, 0], [left.get_right()[0] + 1.15, y, 0], buff=0, color=color, stroke_width=5, tip_length=0.2)
            res = chip(name, color, size=28).move_to([4.7, y, 0])
            res.shift(RIGHT * 0)
            # keep arrow ending next to the chip
            ar2 = Arrow([res.get_left()[0] - 1.0, y, 0], [res.get_left()[0] - 0.1, y, 0], buff=0, color=color, stroke_width=5, tip_length=0.2)
            return VGroup(left, ar2, res)
        r1 = row("λ at least 1 beyond the range", "with or without neighbours", "dispersal limit", TEAL, 2.3)
        r2 = row("λ below 1 only where neighbours remain", "not where neighbours are cleared", "biotic limit", ORANGE, 0.2)
        r3 = row("λ below 1 in every treatment beyond", "inside controls stay at 1 or above", "abiotic limit", BLUE, -1.9)
        note = T("(dune plant, one site)", 22, TEAL).next_to(r1[2], DOWN, buff=0.12)

        qs = [T("?", 40, GREY, weight=BOLD).move_to(r[2].get_center()) for r in (r1, r2, r3)]
        self.play(*[FadeIn(q, scale=0.6) for q in qs], run_time=0.6)
        self.at("lambda is at least one")
        self.play(FadeIn(r1[0], shift=RIGHT * 0.2), run_time=0.8)
        self.at("Dispersal is the likely limit")
        self.play(GrowArrow(r1[1]), ReplacementTransform(qs[0], r1[2]), run_time=0.7)
        self.at("one site")
        self.play(FadeIn(note), run_time=0.5)

        self.at("lambda falls below one only")
        self.play(FadeIn(r2[0], shift=RIGHT * 0.2), run_time=0.8)
        self.at("biotic limit is implicated")
        self.play(GrowArrow(r2[1]), ReplacementTransform(qs[1], r2[2]), run_time=0.7)

        self.at("every treatment")
        self.play(FadeIn(r3[0], shift=RIGHT * 0.2), run_time=0.8)
        self.at("abiotic limit is the likeliest")
        self.play(GrowArrow(r3[1]), ReplacementTransform(qs[2], r3[2]), run_time=0.7)

        rule = VGroup(T("Absence on a map", 44, TEXT, font=TITLE_FONT),
                      T("does not show where the niche ends.", 44, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.25).move_to([0, 0.1, 0])
        self.at("Keep this rule")
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(r3), FadeOut(note), run_time=0.6)
        self.at("Absence on a map")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Absence on a map does not show where the niche ends."
