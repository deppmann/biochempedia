"""Classification changes: when new evidence moves the groups  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = ribosomal RNA, the molecule compared; new evidence
  BAC    = Bacteria (typical bacteria)
  TEAL   = Archaea (methane-making microbes)
  GREEN  = Eukarya, and "closer relatives" / a match
  ORANGE = fungi
  GOLD   = years (1977, 1990, 1993)
  RED    = a claim that needs fixing; what the microscope cannot show
  TEXT   = groups, claims (nested boxes, the classification claim)
  GREY   = outlines, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BAC = "#7D8CFF"   # Bacteria (periwinkle, distinct from teal)


def bchip(text, color=BAC, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def microbe(color=GREY, w=1.5, h=0.8):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18)


def year(text, size=36):
    return M(text, size, GOLD)


class S00Title(TitleCard):
    LESSON = "Classification changes"
    TITLE = "When New Evidence Moves the Groups"


# ---------------------------------------------------------------------------------------------
class S01Look(SpokenScene):
    def construct(self):
        lens = Circle(radius=2.2, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.06).move_to([0, 0.5, 0])
        lens_lbl = T("under a microscope", 28, GREY).next_to(lens, UP, buff=0.15)
        a = microbe().move_to([-0.95, 0.5, 0])
        b = microbe().move_to([0.95, 0.5, 0])
        la = T("typical bacterium", 26, GREY).move_to([-3.9, 0.9, 0])
        lb = T("methane-making microbe", 26, GREY).move_to([4.2, 0.9, 0])
        la.set_x(-4.8); lb.set_x(5.0)
        la = T("typical\nbacterium", 26, GREY, line_spacing=0.8).next_to(lens, LEFT, buff=0.35)
        lb = T("methane-making\nmicrobe", 26, GREY, line_spacing=0.8).next_to(lens, RIGHT, buff=0.35)
        alike = T("look just alike", 34, TEXT, weight=BOLD).move_to([0, -2.3, 0])
        self.at("Some microbes that make methane")
        self.play(Create(lens), FadeIn(lens_lbl), run_time=0.7)
        self.play(FadeIn(a, scale=0.9), FadeIn(b, scale=0.9), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.at("look just like bacteria")
        self.play(FadeIn(alike, shift=UP * 0.15), run_time=0.5)

        yr = year("1977").move_to([-5.6, 3.1, 0])
        self.at("In 1977")
        self.play(FadeIn(yr, shift=DOWN * 0.15), run_time=0.5)
        # one molecule inside each microbe
        da = Dot(radius=0.13, color=YELLOW).move_to(a.get_center())
        db = Dot(radius=0.13, color=YELLOW).move_to(b.get_center())
        mol = T("one molecule inside", 30, YELLOW).move_to([0, -2.3, 0])
        self.at("compared one molecule")
        self.play(FadeOut(alike), FadeIn(da, scale=2), FadeIn(db, scale=2), FadeIn(mol), run_time=0.7)

        # split into separate branches
        root = Dot(radius=0.07, color=GREY).move_to([0, -0.6, 0])
        ta, tb = np.array([-2.6, 1.3, 0]), np.array([2.6, 1.3, 0])
        lna = Line(root.get_center(), ta, color=BAC, stroke_width=6)
        lnb = Line(root.get_center(), tb, color=TEAL, stroke_width=6)
        a2 = microbe(BAC).move_to(ta + UP * 0.55)
        b2 = microbe(TEAL).move_to(tb + UP * 0.55)
        la2 = T("typical bacterium", 26, BAC).next_to(a2, UP, buff=0.12)
        lb2 = T("methane-making microbe", 26, TEAL).next_to(b2, UP, buff=0.12)
        sep = T("a separate line of descent", 32, TEAL, weight=BOLD).move_to([0, -1.3, 0])
        self.at("separate line of descent")
        self.play(FadeOut(lens), FadeOut(lens_lbl), FadeOut(la), FadeOut(lb), FadeOut(mol), FadeOut(da), FadeOut(db),
                  FadeOut(yr), ReplacementTransform(a, a2), ReplacementTransform(b, b2),
                  FadeIn(root), Create(lna), Create(lnb), FadeIn(la2), FadeIn(lb2), run_time=1.2)
        self.play(FadeIn(sep, shift=UP * 0.1), run_time=0.5)

        q1 = T("How has DNA changed the way we classify life?", 32, TEXT, weight=BOLD)
        q2 = T("Why is it fine for science to change its mind?", 32, YELLOW, weight=BOLD)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.3).move_to([0, -2.7, 0])
        self.at("How has DNA")
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
        self.at("why is it fine")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Groups(SpokenScene):
    def construct(self):
        head = bchip("classification: sorting living things into groups", TEXT, 28).to_edge(UP, buff=0.5)
        outer = RoundedRectangle(corner_radius=0.2, width=7.0, height=4.6, stroke_color=TEXT, stroke_width=4,
                                 fill_color=TEXT, fill_opacity=0.05).move_to([0, -0.4, 0])
        mid = RoundedRectangle(corner_radius=0.2, width=4.8, height=2.6, stroke_color=TEXT, stroke_width=4,
                               fill_color=TEXT, fill_opacity=0.08).move_to([0, -0.9, 0])
        inner = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to([0, -1.5, 0])
        dom_l = T("domain: the largest group", 28, TEXT, weight=BOLD).move_to(outer.get_top() + DOWN * 0.45)
        king_l = T("kingdom: a large group", 28, TEXT, weight=BOLD).move_to(mid.get_top() + DOWN * 0.4)
        in_l = T("smaller group", 24, GREY).move_to(inner)
        nest = T("nested, like folders inside folders", 28, GREY).move_to([0, -3.35, 0])
        self.at("Classification is the sorting")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)
        self.at("The groups are nested")
        self.play(FadeIn(inner), FadeIn(mid), FadeIn(outer), FadeIn(in_l), FadeIn(nest), run_time=0.8)
        self.at("A kingdom is a large group")
        self.play(FadeIn(king_l), run_time=0.5)
        self.at("A domain is the largest")
        self.play(FadeIn(dom_l), run_time=0.5)
        self.at("above kingdom")
        self.play(Indicate(dom_l, color=TEXT, scale_factor=1.08), run_time=0.8)

        boxes = VGroup(outer, mid, inner, dom_l, king_l, in_l)
        self.at("A microscope shows")
        self.play(FadeOut(nest), FadeOut(head), run_time=0.4)
        self.play(boxes.animate.scale(0.8).move_to([-3.5, 0.0, 0]), run_time=0.9)
        lens = Circle(radius=1.9, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.06).move_to([3.4, 1.3, 0])
        lens_l = T("microscope", 26, GREY).next_to(lens, UP, buff=0.12)
        shape = T("shape  ✓", 34, GREEN, weight=BOLD).move_to([3.4, 1.6, 0])
        size = T("size  ✓", 34, GREEN, weight=BOLD).move_to([3.4, 0.9, 0])
        anc = T("ancestry  ✗", 38, RED, weight=BOLD).move_to([3.4, -2.0, 0])
        self.play(Create(lens), FadeIn(lens_l), run_time=0.6)
        self.play(FadeIn(shape, shift=RIGHT * 0.2), FadeIn(size, shift=RIGHT * 0.2), run_time=0.6)
        self.at("not ancestry")
        self.play(FadeIn(anc, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def block_row(n, y, x0, w=0.62, color=YELLOW, diff=(), diff_color=TEXT):
    row = VGroup()
    for i in range(n):
        c = diff_color if i in diff else color
        op = 0.95 if i in diff else 0.5
        r = Rectangle(width=w, height=0.5, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=op)
        r.move_to([x0 + i * (w + 0.05), y, 0])
        row.add(r)
    return row


class S03Molecule(SpokenScene):
    def construct(self):
        specs = [("Bacteria", BAC, -4.3), ("Archaea", TEAL, 0.0), ("Eukarya", GREEN, 4.3)]
        cells, ribs, rlabs, nlabs = [], [], [], []
        for name, col, x in specs:
            cell = Circle(radius=1.15, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.1).move_to([x, 1.5, 0])
            ribos = VGroup(*[Dot(radius=0.1, color=GREY).move_to([x + dx, 1.5 + dy, 0])
                             for dx, dy in [(-0.45, 0.35), (0.4, 0.45), (0.05, -0.1), (-0.35, -0.5), (0.5, -0.45)]])
            nl = T(name, 26, col).next_to(cell, UP, buff=0.12)
            cells.append(cell); ribs.append(ribos); nlabs.append(nl)
        self.at("Every cell builds proteins")
        self.play(*[FadeIn(c) for c in cells], *[FadeIn(n) for n in nlabs], *[FadeIn(r) for r in ribs], run_time=0.9)
        rib_l = T("ribosomes", 26, GREY).move_to([0, -0.35, 0])
        self.play(FadeIn(rib_l), run_time=0.4)
        self.at("Ribosomal RNA is")
        rr = T("ribosomal RNA", 30, YELLOW, weight=BOLD).move_to([0, -0.35, 0])
        self.play(*[r.animate.set_color(YELLOW) for r in ribs], ReplacementTransform(rib_l, rr), run_time=0.7)
        self.at("Because every cell has it")
        self.play(*[Indicate(r, color=YELLOW, scale_factor=1.25) for r in ribs], run_time=0.9)
        cmp_l = T("compared across all cellular life", 28, TEXT)
        arrs = VGroup(Line([-3.0, -0.35, 0], [-1.9, -0.35, 0], color=GREY, stroke_width=4),
                      Line([1.9, -0.35, 0], [3.0, -0.35, 0], color=GREY, stroke_width=4))
        self.play(FadeOut(rr), run_time=0.3)
        cmp_l.move_to([0, -0.35, 0])
        self.play(FadeIn(cmp_l), run_time=0.5)

        self.at("Its sequence changes slowly")
        top = block_row(14, -1.5, -4.2)
        bot = block_row(14, -2.15, -4.2, diff=(3, 8, 11))
        t_l = T("A", 24, GREY).move_to([-5.1, -1.5, 0])
        b_l = T("B", 24, GREY).move_to([-5.1, -2.15, 0])
        self.play(FadeOut(cmp_l), FadeIn(top), FadeIn(bot), FadeIn(t_l), FadeIn(b_l), run_time=0.8)
        shared = T("mostly shared", 26, YELLOW).move_to([0, -0.85, 0])
        self.play(FadeIn(shared), run_time=0.4)
        self.at("Shared does not mean identical")
        self.play(*[Indicate(bot[i], color=TEXT, scale_factor=1.25) for i in (3, 8, 11)], run_time=0.8)
        ev = T("the small differences are the evidence", 32, TEXT, weight=BOLD).move_to([0, -3.1, 0])
        self.at("The small differences")
        self.play(FadeIn(ev, shift=UP * 0.12), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def piece_list(widths, x, y0, color, gap=0.55):
    g = VGroup()
    for i, w in enumerate(widths):
        g.add(Rectangle(width=w, height=0.38, stroke_color=color, stroke_width=3, fill_color=color,
                        fill_opacity=0.3).move_to([x, y0 - i * gap, 0]))
    return g


class S04Score(SpokenScene):
    def construct(self):
        yr = year("1977").to_edge(UP, buff=0.4).set_x(-5.2)
        who = T("Woese and Fox", 30, TEXT).next_to(yr, RIGHT, buff=0.3)
        bar = Rectangle(width=7.0, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                        fill_opacity=0.3).move_to([0, 2.55, 0])
        bar_l = T("ribosomal RNA", 28, YELLOW).next_to(bar, DOWN, buff=0.15)
        self.play(FadeIn(yr), FadeIn(who), FadeIn(bar), FadeIn(bar_l), run_time=0.7)

        wa = [1.3, 0.8, 1.7, 1.0, 1.5]
        wbm = [1.3, 0.8, 1.7, 1.0, 1.5]
        wbb = [0.7, 1.4, 1.7, 1.3, 0.9]  # only the middle piece matches
        # cut into pieces: bar becomes a row of pieces
        self.at("cut ribosomal RNA")
        tot = 7.0
        row = VGroup()
        xs = 0.0
        ws = [w / sum(wa) * (tot - 0.4 * 4) for w in wa]
        pos = -tot / 2
        for w in ws:
            row.add(Rectangle(width=w, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                              fill_opacity=0.3).move_to([pos + w / 2, 2.55, 0]))
            pos += w + 0.4
        self.play(ReplacementTransform(bar, row), run_time=0.9)

        LA, LB = -3.6, 3.6
        la = piece_list(wa, LA, 1.1, TEAL)
        lb = piece_list(wbm, LB, 1.1, TEAL)
        ta = T("organism A", 26, GREY).move_to([LA, 1.85, 0])
        tb = T("organism B", 26, GREY).move_to([LB, 1.85, 0])
        self.at("listed them")
        self.play(FadeOut(row), FadeOut(bar_l), FadeIn(la), FadeIn(lb), FadeIn(ta), FadeIn(tb), run_time=0.9)
        for g in (la, lb):
            g.set_color(GREY)
            for r in g:
                r.set_fill(GREY, 0.3)

        gauge = Line([-2.0, -2.6, 0], [3.4, -2.6, 0], color=GREY, stroke_width=6)
        g0 = T("0  no overlap", 26, GREY).next_to(gauge.get_left(), DOWN, buff=0.3).shift(RIGHT * 0.9)
        g1 = T("1  the same", 26, GREY).next_to(gauge.get_right(), DOWN, buff=0.3).shift(LEFT * 0.6)
        sc_l = T("score", 30, TEXT, weight=BOLD).next_to(gauge, LEFT, buff=0.5)
        marker = Triangle(color=GREY, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI)
        marker.move_to([-2.0, -2.25, 0])
        self.at("scored how much")
        links = VGroup(*[Line(la[i].get_right(), lb[i].get_left(), color=GREEN, stroke_width=4) for i in range(5)])
        self.play(FadeIn(links), run_time=0.7)
        self.play(FadeOut(links), run_time=0.4)
        self.at("The score runs from zero")
        self.play(Create(gauge), FadeIn(g0), FadeIn(g1), FadeIn(sc_l), FadeIn(marker), run_time=0.9)

        # methane maker vs methane maker
        ta2 = T("methane maker", 26, TEAL).move_to([LA, 1.85, 0])
        tb2 = T("methane maker", 26, TEAL).move_to([LB, 1.85, 0])
        links = VGroup(*[Line(la[i].get_right(), lb[i].get_left(), color=GREEN, stroke_width=4) for i in range(5)])
        self.at("scored high")
        self.play(ReplacementTransform(ta, ta2), ReplacementTransform(tb, tb2),
                  *[r.animate.set_color(TEAL).set_fill(TEAL, 0.3) for g in (la, lb) for r in g], run_time=0.6)
        self.play(FadeIn(links), marker.animate.move_to([0.7, -2.25, 0]).set_color(GREEN), run_time=0.9)
        high = T("high", 30, GREEN, weight=BOLD).next_to(marker, UP, buff=0.12)
        self.play(FadeIn(high), run_time=0.3)

        # vs typical bacterium
        tb3 = T("typical bacterium", 26, BAC).move_to([LB, 1.85, 0])
        newb = piece_list(wbb, LB, 1.1, BAC)
        keep = Line(la[2].get_right(), newb[2].get_left(), color=GREEN, stroke_width=4)
        self.at("low with typical bacteria")
        self.play(FadeOut(links), FadeOut(high), ReplacementTransform(tb2, tb3), ReplacementTransform(lb, newb),
                  marker.animate.move_to([-1.46, -2.25, 0]).set_color(RED), run_time=1.0)
        self.play(FadeIn(keep), run_time=0.4)
        low = T("low", 30, RED, weight=BOLD).next_to(marker, UP, buff=0.12)
        self.play(FadeIn(low), run_time=0.3)

        # three lines of descent
        self.at("three major lines of descent")
        old = VGroup(la, newb, ta2, tb3, keep, gauge, g0, g1, sc_l, marker, low)
        self.play(FadeOut(old), run_time=0.6)
        root = Dot(radius=0.07, color=GREY).move_to([0, -2.2, 0])
        tips = [(-4.2, BAC, "typical bacteria"), (0.0, TEAL, "methane makers"), (4.2, GREEN, "yeast, duckweed")]
        lines = VGroup(); labs = VGroup()
        for x, col, name in tips:
            lines.add(Line(root.get_center(), [x, 0.9, 0], color=col, stroke_width=7))
            labs.add(T(name, 28, col).move_to([x, 1.4, 0]))
        three = T("three major lines of descent", 36, TEXT, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(root), *[Create(l) for l in lines], run_time=0.9)
        self.play(*[FadeIn(l) for l in labs], FadeIn(three), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Domains(SpokenScene):
    def construct(self):
        def dbox(name, col, x):
            bx = RoundedRectangle(corner_radius=0.2, width=3.7, height=2.0, stroke_color=col, stroke_width=4,
                                  fill_color=col, fill_opacity=0.12).move_to([x, 0.8, 0])
            return VGroup(bx, T(name, 40, col, weight=BOLD).move_to(bx))
        yr = year("1990").to_edge(UP, buff=0.45)
        rank = T("the rank of domain, above kingdom", 30, TEXT).next_to(yr, DOWN, buff=0.2)
        self.at("In 1990")
        self.play(FadeIn(yr, shift=DOWN * 0.15), FadeIn(rank), run_time=0.7)
        dB, dA, dE = dbox("Bacteria", BAC, -4.2), dbox("Archaea", TEAL, 0.0), dbox("Eukarya", GREEN, 4.2)
        self.at("The three domains are")
        self.at("Bacteria")
        self.play(FadeIn(dB, scale=0.9), run_time=0.5)
        self.at("Archaea and")
        self.play(FadeIn(dA, scale=0.9), run_time=0.5)
        self.at("Eukarya")
        self.play(FadeIn(dE, scale=0.9), run_time=0.5)

        self.at("differ from bacteria")
        diff = T("differ from bacteria in\ntheir RNA and membranes", 26, TEAL, line_spacing=0.85).move_to([0, -1.1, 0])
        self.play(FadeIn(diff), run_time=0.6)
        self.at("whose cells have a nucleus")
        cell = Circle(radius=0.8, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.08).move_to([4.2, -1.4, 0])
        nuc = Circle(radius=0.28, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to(cell)
        nuc_l = T("nucleus", 26, GREEN).next_to(cell, DOWN, buff=0.15)
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(nuc_l), run_time=0.6)

        # zoom to Eukarya
        self.at("Fungi grow in place")
        self.play(FadeOut(VGroup(dB, dA, diff, yr, rank, cell, nuc, nuc_l)),
                  dE.animate.scale(0.8).move_to([0, 2.4, 0]), run_time=0.8)
        pl = bchip("plants", GREEN, 30).move_to([-3.7, 0.3, 0])
        fu = bchip("fungi", ORANGE, 30).move_to([-1.55, 0.3, 0])
        an = bchip("animals", GREEN, 30).move_to([3.9, 0.3, 0])
        self.play(FadeIn(pl), FadeIn(an), FadeIn(fu), run_time=0.6)
        look = T("Fungi grow in place and have cell walls,\nso they look plant-like.", 26, GREY, line_spacing=0.85)
        br = Rectangle(width=4.5, height=0.95, stroke_color=GREY, stroke_width=3).move_to([-2.62, 0.3, 0])
        br.set_stroke(opacity=0.9)
        look.move_to([-2.62, -0.75, 0])
        self.play(Create(br), FadeIn(look), run_time=0.7)

        self.at("But in 1993")
        ev = bchip("1993: a survey of 25 proteins", YELLOW, 28).move_to([0, -2.2, 0])
        self.play(FadeIn(ev, shift=UP * 0.15), FadeOut(look), run_time=0.6)
        self.at("strongly supported fungi")
        new_fu = bchip("fungi", ORANGE, 30).move_to([2.0, 0.3, 0])
        self.play(fu.animate.move_to([1.65, 0.3, 0]), FadeOut(br), run_time=0.9)
        br2 = Rectangle(width=4.2, height=0.95, stroke_color=GREEN, stroke_width=4).move_to([2.78, 0.3, 0])
        cl = T("closer relatives", 30, GREEN, weight=BOLD).move_to([2.78, -0.65, 0])
        self.at("closer to animals")
        self.play(Create(br2), FadeIn(cl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = T("Why is it fine for science to change its mind?", 36, YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
        self.at("So why is it fine")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        claim = bchip("a classification is a claim about ancestry", TEXT, 32).move_to([0, 1.5, 0])
        self.at("A classification is a claim")
        self.play(FadeIn(claim, scale=0.92), run_time=0.7)
        test = bchip("test it with evidence", YELLOW, 30).move_to([-4.0, -0.7, 0])
        a1 = arr(claim.get_bottom() + LEFT * 1.5, test.get_top(), GREY)
        self.at("can be tested")
        self.play(GrowArrow(a1), FadeIn(test, shift=DOWN * 0.1), run_time=0.8)
        fix = bchip("needs fixing", RED, 30).move_to([3.6, -0.7, 0])
        a2 = arr(test.get_right(), fix.get_left(), GREY)
        self.at("some tests show")
        self.play(GrowArrow(a2), FadeIn(fix), run_time=0.8)
        self.at("needs fixing")
        self.play(Indicate(VGroup(*fix[1:]), color=RED, scale_factor=1.1), run_time=0.7)

        old = T("reasonable for the evidence of their time", 26, GREY).next_to(claim, DOWN, buff=0.2).set_x(2.0)
        self.at("The older groups were reasonable")
        self.play(FadeIn(old), run_time=0.6)

        new_ev = bchip("new DNA and RNA evidence", YELLOW, 30).move_to([-3.2, -2.25, 0])
        new_claim = bchip("revised groups", GREEN, 30).move_to([3.6, -2.25, 0])
        a3 = arr(new_ev.get_right(), new_claim.get_left(), GREEN)
        self.at("New DNA and RNA")
        self.play(FadeIn(new_ev, shift=UP * 0.1), run_time=0.6)
        self.at("changed the groups")
        self.play(GrowArrow(a3), FadeIn(new_claim, scale=0.9), run_time=0.7)
        self.at("Classification changes when")
        rule = T("evidence changes, so the groups change", 34, TEXT, weight=BOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Classification changes when the evidence changes."
