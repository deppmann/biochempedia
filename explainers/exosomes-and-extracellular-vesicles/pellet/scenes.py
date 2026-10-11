"""Exosomes and extracellular vesicles, section film: the pellet is defined by the centrifuge

COLOR MAP (one color per concept, whole video)
  TEAL   = a small vesicle (all vesicles look the same, wherever they came from)
  ORANGE = something else that comes down with the vesicles (contaminant, free protein)
  GREY   = tubes, cells and debris, structure, labels
  PURPLE = cargo and Argonaute (the protein that carries microRNA)
  GOLD   = people and years; the activity being tested
  CELL   = a cell (A or B, told apart by their labels)
  YELLOW = B changes
  RED    = no / not detected / weak
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CELL = "#7C8CF8"
ORANGE = "#F29E4C"


def vdot(pos, r=0.12, color=TEAL):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.55).move_to(pos)


def odot(pos, s=0.14):
    return Square(side_length=s * 2, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE,
                  fill_opacity=0.6).move_to(pos)


def gdot(pos, r=0.17):
    return Circle(radius=r, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.55).move_to(pos)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(c, s=0.3, color=RED, w=7):
    c = np.array(c)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Exosomes and extracellular vesicles"
    TITLE = "The pellet is defined by the centrifuge"


# ---------------------------------------------------------------------------------------------
class S01Spin(SpokenScene):
    XS = [-4.3, 0.0, 4.3]
    TOP, BOT = 2.15, -1.45

    def tube(self, cx):
        return RoundedRectangle(corner_radius=0.35, width=1.7, height=3.6, stroke_color=GREY, stroke_width=3,
                                fill_opacity=0).move_to([cx, 0.35, 0])

    def pellet(self, cx, objs):
        """packed positions at the bottom of a tube"""
        out = []
        for k, _ in enumerate(objs):
            out.append(np.array([cx - 0.62 + 0.31 * (k % 5) + (0.15 if (k // 5) % 2 else 0), -1.27 + 0.27 * (k // 5), 0]))
        return out

    def construct(self):
        X = self.XS
        cells = [(-0.4, 1.7), (0.35, 1.25), (-0.1, 0.5)]
        big = [(0.3, 1.8), (-0.45, 0.9), (0.1, -0.2)]
        small = [(-0.2, 1.45), (0.45, 0.6), (-0.35, 0.1), (0.0, 1.0), (0.4, -0.5), (-0.5, -0.6), (0.15, -0.9)]
        other = [(-0.1, 1.95), (0.5, 0.2), (-0.3, -0.3), (0.2, 0.25)]
        G = lambda f, pts, cx: VGroup(*[f([cx + x, y, 0]) for x, y in pts])
        gc = G(gdot, cells, X[0])
        gb = G(lambda p: vdot(p, 0.14), big, X[0])
        gs = G(lambda p: vdot(p, 0.07), small, X[0])
        go = G(odot, [(x, y) for x, y in other], X[0])
        for o in go:
            o.scale(0.7)
        t1 = self.tube(X[0])
        note = T("idealised, not to scale", 22, GREY).move_to([4.9, 3.3, 0])
        q = T("carries a message?", 30, GOLD).move_to([X[0], 3.0, 0])
        self.play(FadeIn(t1), FadeIn(gc), FadeIn(gb), FadeIn(gs), FadeIn(go), FadeIn(q), FadeIn(note), run_time=0.9)

        l1 = T("slow spin:\ncells and debris", 24, TEXT).move_to([X[0], -2.55, 0])
        self.at("Slow spins")
        self.play(FadeOut(q), FadeIn(l1), run_time=0.4)
        slots = self.pellet(X[0], gc)
        self.play(*[g.animate.move_to(s) for g, s in zip(gc, slots)], run_time=1.3)

        # tube 2
        t2 = self.tube(X[1])
        l2 = T("faster spin:\nlarge vesicles", 24, TEXT).move_to([X[1], -2.55, 0])
        self.at("faster spin")
        gb2, gs2, go2 = [g.copy().shift(RIGHT * (X[1] - X[0])) for g in (gb, gs, go)]
        a1 = arr([X[0] + 1.0, 0.7, 0], [X[1] - 1.0, 0.7, 0], GREY, 4, 0.18)
        self.play(FadeIn(t2), FadeIn(l2), FadeIn(a1), ReplacementTransform(gb, gb2), ReplacementTransform(gs, gs2),
                  ReplacementTransform(go, go2), run_time=1.1)
        self.play(*[g.animate.move_to(s) for g, s in zip(gb2, self.pellet(X[1], gb2))], run_time=1.1)

        # tube 3
        t3 = self.tube(X[2])
        l3 = T("about 100,000 × g,\nan hour or more:\nsmall particles", 24, TEXT).move_to([X[2], -2.6, 0])
        self.at("times gravity")
        gs3, go3 = [g.copy().shift(RIGHT * (X[2] - X[1])) for g in (gs2, go2)]
        a2 = arr([X[1] + 1.0, 0.7, 0], [X[2] - 1.0, 0.7, 0], GREY, 4, 0.18)
        self.play(FadeIn(t3), FadeIn(l3), FadeIn(a2), ReplacementTransform(gs2, gs3), ReplacementTransform(go2, go3),
                  run_time=1.1)
        self.at("brings down")
        allp = VGroup(*gs3, *go3)
        self.play(*[g.animate.move_to(s) for g, s in zip(allp, self.pellet(X[2], allp))], run_time=1.4)
        self.at("small ones")
        self.play(Indicate(allp, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Mixed(SpokenScene):
    def line(self, a, b):
        return Line(a, b, color=GREY, stroke_width=2.5)

    def construct(self):
        box = RoundedRectangle(corner_radius=0.8, width=4.0, height=3.7, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([0, -0.1, 0])
        plab = T("the small pellet", 24, GREY).move_to([0, 2.05, 0])
        note = T("idealised, not to scale", 22, GREY).move_to([4.9, 3.3, 0])
        # members (positions in the pellet)
        fill_t = [(-0.3, 0.85), (0.4, 1.0), (0.2, -0.2), (-0.7, 0.05), (0.7, -1.3), (-1.0, 1.1), (0.0, -0.9)]
        fillers = VGroup(*[vdot([x, y, 0], 0.2) for x, y in fill_t])
        agg_p = (-1.2, 0.6)
        agg = VGroup(*[Circle(radius=0.11, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.6
                              ).move_to([agg_p[0] + dx, agg_p[1] + dy, 0])
                       for dx, dy in [(-0.1, 0), (0.12, 0.08), (0.02, -0.14)]])
        lip = Circle(radius=0.22, stroke_color=ORANGE, stroke_width=5, fill_opacity=0).move_to([-1.2, -0.7, 0])
        vir = RegularPolygon(6, radius=0.26, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE,
                             fill_opacity=0.6).move_to([-0.55, -1.35, 0])
        calf = vdot([1.2, 0.5, 0], 0.25)
        gfv = vdot([1.1, -0.65, 0], 0.25)
        gf = VGroup(*[Dot([1.1 + 0.34 * np.cos(a), -0.65 + 0.34 * np.sin(a), 0], radius=0.06, color=ORANGE)
                      for a in (0.3, 1.0, 3.9)])
        self.play(FadeIn(box), FadeIn(plab), FadeIn(note), run_time=0.5)
        self.at("everything of the right")
        self.play(FadeIn(fillers, lag_ratio=0.15), run_time=1.2)

        def label(text, pos, col=ORANGE):
            return chip(text, col, size=22)

        items = [("protein aggregates", agg, [-4.4, 1.7, 0], "protein aggregates"),
                 ("lipoprotein particles", lip, [-4.4, -0.1, 0], "lipoprotein"),
                 ("viruses", vir, [-4.4, -1.9, 0], "viruses"),
                 ("calf serum vesicles", calf, [4.3, 1.5, 0], "calf serum"),
                 ("soluble growth factors", VGroup(gfv, gf), [4.3, -1.5, 0], "Soluble growth")]
        made = []
        self.at("includes")
        for text, obj, pos, cue in items:
            self.at(cue)
            c = chip(text, ORANGE, size=22).move_to(pos)
            target = obj.get_center()
            edge = c.get_right() if pos[0] < 0 else c.get_left()
            ln = self.line(edge, target + (LEFT if pos[0] > 0 else RIGHT) * 0.0)
            ln.set_z_index(-1)
            self.play(FadeIn(obj, scale=1.5), Create(ln), FadeIn(c), run_time=0.6)
            made += [c, ln]
        self.at("changed conclusions")
        self.play(Indicate(box, color=RED, scale_factor=1.04), run_time=0.8)

        # Coffey
        self.at("In 2019")
        everything = VGroup(box, plab, fillers, agg, lip, vir, calf, gfv, gf, *made)
        att = chip("Robert Coffey's laboratory, 2019", GOLD, size=24).move_to([0, 3.1, 0])
        self.play(FadeOut(VGroup(*made)), FadeIn(att), run_time=0.5)
        small = VGroup(box, plab, fillers, agg, lip, vir, calf, gfv, gf)
        self.play(small.animate.scale(0.65).move_to([-4.4, -0.1, 0]), run_time=0.8)
        self.at("separated such pellets")
        ar = arr([-2.7, -0.1, 0], [-0.7, -0.1, 0], GREY, 5)
        al = T("separated\nfurther", 24, TEXT).next_to(ar, UP, buff=0.15)
        circ = Circle(radius=1.9, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.14
                      ).move_to([3.2, -0.1, 0])
        cl = T("the exosomes", 26, TEAL).move_to([3.2, 2.25, 0])
        self.play(GrowArrow(ar), FadeIn(al), FadeIn(circ), FadeIn(cl), run_time=0.9)
        self.at("which carry")
        ago = chip("Argonaute", PURPLE, size=28).move_to([3.2, 0.3, 0])
        mi = T("carries microRNA", 22, PURPLE).move_to([3.2, -0.7, 0])
        self.play(FadeIn(ago, scale=0.9), FadeIn(mi), run_time=0.6)
        self.at("were not detected")
        nd = T("not detected", 32, RED, weight=BOLD).move_to([3.2, -2.55, 0])
        self.play(Create(cross(ago.get_center(), 0.45, RED, 4)), FadeIn(nd), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Controls(SpokenScene):
    CX = -5.0

    def construct(self):
        cx = self.CX
        shades = VGroup(*[Rectangle(width=1.5, height=0.7, stroke_width=0, fill_color=GREY,
                                    fill_opacity=0.04 + 0.05 * k).move_to([cx, 2.3 - 0.7 * k, 0]) for k in range(8)])
        tube = RoundedRectangle(corner_radius=0.3, width=1.5, height=5.6, stroke_color=GREY, stroke_width=3,
                                fill_opacity=0).move_to([cx, -0.15, 0])
        tl = T("sucrose gradient", 24, TEXT).move_to([cx + 0.5, 3.15, 0])
        note = T("idealised, not to scale", 22, GREY).move_to([-4.2, -3.3, 0])
        self.play(FadeIn(tube), FadeIn(shades), FadeIn(tl), run_time=0.6)
        # pellet loaded low in the tube: teal + orange mixed
        tpos = [(-0.35, -2.25), (0.0, -2.35), (0.35, -2.2), (-0.2, -2.0), (0.2, -1.95)]
        opos = [(-0.4, -1.95), (0.05, -2.1), (0.4, -2.45), (-0.05, -2.55)]
        teals = VGroup(*[vdot([cx + x, y, 0], 0.11) for x, y in tpos])
        oranges = VGroup(*[odot([cx + x, y, 0], 0.09) for x, y in opos])
        self.at("floating the pellet")
        self.play(FadeIn(teals), FadeIn(oranges), run_time=0.6)
        self.play(FadeIn(note), run_time=0.2)
        # band of vesicles
        bandy = 0.9
        band = DashedVMobject(Rectangle(width=1.7, height=0.95, stroke_color=TEAL, stroke_width=3).move_to([cx, bandy, 0]),
                              num_dashes=24)
        up = [(-0.4, 0.75), (-0.1, 1.05), (0.25, 0.8), (0.4, 1.1), (-0.3, 1.1)]
        self.at("Membrane vesicles rise")
        bl = T("vesicles rise to\nabout 1.13 to\n1.19 g/mL", 22, TEAL).move_to([-2.7, 1.0, 0])
        self.play(*[v.animate.move_to([cx + x, y, 0]) for v, (x, y) in zip(teals, up)], FadeIn(band), FadeIn(bl),
                  run_time=1.6)
        self.at("Free protein")
        fl = T("free protein\nstays below", 22, ORANGE).move_to([-2.7, -2.0, 0])
        self.play(FadeIn(fl), Indicate(oranges, color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.at("activity moves")
        act = chip("activity?", GOLD, size=24).move_to([-2.7, -0.3, 0])
        aa = arr([-3.5, -0.0, 0], [-4.1, 0.65, 0], GOLD, 4, 0.18)
        self.play(FadeIn(act), GrowArrow(aa), run_time=0.6)

        def card(y, h):
            return RoundedRectangle(corner_radius=0.2, width=7.2, height=h, stroke_color=GREY, stroke_width=2,
                                    fill_opacity=0).move_to([2.7, y, 0])

        # card A: supernatant
        ca = card(1.6, 1.9)
        tb = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.3, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.25).move_to([-0.4, 1.6, 0])
        ta = T("test the supernatant,\nthe liquid left after the spin", 28, TEXT).move_to([3.4, 1.6, 0])
        self.at("supernatant")
        self.play(Create(ca), FadeIn(tb), FadeIn(ta), run_time=0.7)
        # card B: mock pellet
        cb = card(-0.7, 1.9)
        dish = RoundedRectangle(corner_radius=0.1, width=1.3, height=0.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.2).move_to([0.0, -0.7, 0])
        tbm = T("test a pellet from medium\nthat never saw cells", 28, TEXT).move_to([3.4, -0.7, 0])
        self.at("a pellet from medium")
        self.play(Create(cb), FadeIn(dish), FadeIn(tbm), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Count(SpokenScene):
    def construct(self):
        res = chip("copies per vesicle", TEXT, size=30)
        eq = T("=", 44)
        num = chip("copies of cargo measured", PURPLE, size=30)
        den = chip("particles counted", TEAL, size=30)
        frac_line = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY, stroke_width=4)
        right = VGroup(num, frac_line, den).arrange(DOWN, buff=0.18)
        frac_line.set_width(max(num.width, den.width) + 0.3)
        form = VGroup(res, eq, right).arrange(RIGHT, buff=0.4).move_to([0, 2.2, 0])
        self.at("And count")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.at("cargo copies")
        self.play(FadeIn(eq), FadeIn(num, shift=DOWN * 0.1), Create(frac_line), run_time=0.6)
        self.at("divided by")
        self.play(FadeIn(den, shift=UP * 0.1), run_time=0.6)

        # scale
        ax = Line([-5.5, -0.15, 0], [5.5, -0.15, 0], color=GREY, stroke_width=3)
        tick = Line([2.0, -0.35, 0], [2.0, 0.05, 0], color=TEXT, stroke_width=4)
        one = M("1", 30).move_to([2.0, -0.7, 0])
        zone = Rectangle(width=3.5, height=0.35, stroke_width=0, fill_color=RED, fill_opacity=0.6
                         ).move_to([-3.75, -0.15, 0])
        zl = T("far below one", 26, RED).move_to([-3.75, 0.5, 0])
        self.at("far below one")
        self.play(Create(ax), Create(tick), FadeIn(one), run_time=0.6)
        self.play(FadeIn(zone), FadeIn(zl), run_time=0.6)
        ideal = T("idealised, for example", 22, GREY).move_to([4.7, 0.5, 0])
        # dose bars
        b1 = Rectangle(width=7.0, height=0.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35
                       ).move_to([-5.5 + 3.5, -1.85, 0])
        b2 = Rectangle(width=2.4, height=0.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35
                       ).move_to([-5.5 + 1.2, -2.6, 0])
        l1 = T("vesicles the effect would need", 24, TEXT).next_to(b1, RIGHT, buff=0.25)
        l2 = T("vesicles the donor cells release", 24, TEXT).next_to(b2, RIGHT, buff=0.25)
        self.at("many more vesicles")
        self.play(FadeIn(ideal), GrowFromEdge(b1, LEFT), FadeIn(l1), run_time=0.7)
        self.play(GrowFromEdge(b2, LEFT), FadeIn(l2), run_time=0.7)
        weak = T("the case for signalling is weak", 30, RED, weight=BOLD).move_to([0, -3.35, 0])
        self.at("is weak")
        self.play(FadeIn(weak, shift=UP * 0.1), run_time=0.6)

        # your turn
        self.at("Your turn")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        ca = Circle(radius=1.35, stroke_color=CELL, stroke_width=4, fill_color=CELL, fill_opacity=0.18
                    ).move_to([-4.9, 0.3, 0])
        cat = T("cell type A", 28, CELL).move_to(ca)
        spin = RoundedRectangle(corner_radius=0.3, width=1.3, height=2.4, stroke_color=GREY, stroke_width=3,
                                fill_opacity=0).move_to([-1.4, 0.3, 0])
        pel = Ellipse(width=0.95, height=0.34, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.45
                      ).move_to([-1.4, -0.7, 0])
        a1 = arr([-3.4, 0.3, 0], [-2.3, 0.3, 0], GREY, 5)
        cb = Circle(radius=1.35, stroke_color=CELL, stroke_width=4, fill_color=CELL, fill_opacity=0.18
                    ).move_to([2.0, 0.3, 0])
        cbt = T("cell type B", 28, CELL).move_to(cb)
        a2 = arr([-0.4, 0.3, 0], [0.55, 0.3, 0], GREY, 5)
        self.at("cell type")
        self.play(FadeIn(ca), FadeIn(cat), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(spin), FadeIn(pel), run_time=0.7)
        pl = T("pellet", 24, TEAL).next_to(spin, DOWN, buff=0.25)
        self.at("add the pellet")
        self.play(FadeIn(pl), GrowArrow(a2), FadeIn(cb), FadeIn(cbt), run_time=0.8)
        self.at("changes")
        chg = T("B changes", 28, YELLOW).next_to(cb, DOWN, buff=0.25)
        self.play(cb.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.25), FadeIn(chg), run_time=0.6)
        self.at("Which controls")
        qb = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.7, height=2.4, stroke_color=GOLD, stroke_width=3
                                              ).move_to([5.3, 0.3, 0]), num_dashes=30)
        qt = T("which\ncontrols?", 32, GOLD).move_to([5.3, 0.3, 0])
        self.play(Create(qb), FadeIn(qt), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "So a claim needs controls, and a count."
