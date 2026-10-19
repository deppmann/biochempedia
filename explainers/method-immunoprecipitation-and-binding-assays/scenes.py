"""Binding assays: catching partners that bind (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the bait: the protein we hold (also the DNA-binding protein in a gel shift)
  ORANGE = the partner: the protein that comes with the bait (prey)
  PURPLE = antibody
  PINK   = the GST tag
  TEAL   = DNA
  GREY   = beads, resin, gels, other proteins in the extract, structure
  GREEN  = a control (what catches the pitfall)
  RED    = a pitfall or artifact
  YELLOW = the question, a band that is read
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#EE8FBF"


def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def blk(text, color, w=1.8, h=0.9, size=26, op=0.22):
    """A protein as a labelled block."""
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=op)
    g = VGroup(box)
    if text:
        g.add(T(text, size, color).move_to(box))
    g.box = box
    return g


def at(m, x, y):
    return m.move_to([x, y, 0])


def antibody(p, u, color=PURPLE):
    """A Y drawn with three lines. p = base point, u = unit direction the arms point."""
    p = np.array([p[0], p[1], 0.0]); u = np.array([u[0], u[1], 0.0])
    e = p + u * 0.7
    def rot(v, a):
        c, s = np.cos(a), np.sin(a)
        return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])
    a1 = e + rot(u, 0.7) * 0.55
    a2 = e + rot(u, -0.7) * 0.55
    return VGroup(Line(p, e, color=color, stroke_width=6), Line(e, a1, color=color, stroke_width=6),
                  Line(e, a2, color=color, stroke_width=6))


def dna(w=4.0, h=0.4, label=None, color=TEAL):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.55)
    g = VGroup(r)
    g.bar = r
    return g


def band(x, y, w=1.7, h=0.24, color=YELLOW, op=0.9):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def xmark(p, size=34):
    return T("✕", size, RED, weight=BOLD).move_to(p)


def qmark(p, size=56):
    return T("?", size, YELLOW, weight=BOLD).move_to(p)


class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Catching Partners That Bind"


# ------------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """The question: do two molecules bind, which parts, which sequence? Ste5 had no known chemistry."""

    def construct(self):
        # A, B: two proteins and a question
        A = blk("protein A", BLUE, 3.6, 2.4, 34).move_to([-3.6, 0.2, 0])
        B = blk("protein B", ORANGE, 3.6, 2.4, 34).move_to([3.6, 0.2, 0])
        q = qmark([0, 0.2, 0], 110)
        ask = lab("do they physically bind?", 32, TEXT).move_to([0, -2.4, 0])
        self.at("Do two molecules")
        self.play(FadeIn(A, shift=RIGHT * 0.3), FadeIn(B, shift=LEFT * 0.3), run_time=0.7)
        self.play(FadeIn(q, scale=0.5), FadeIn(ask), run_time=0.5)

        # Ste5: essential, no known chemistry
        ste = blk("Ste5", BLUE, 3.4, 2.0, 40).move_to([0, 0.5, 0])
        ess = lab("essential, but no known chemistry", 30, TEXT).move_to([0, 2.8, 0])
        self.at("could be essential")
        self.play(FadeOut(A), FadeOut(B), FadeOut(q), FadeOut(ask), run_time=0.4)
        self.play(FadeIn(ste, scale=0.8), FadeIn(ess), run_time=0.6)
        add = VGroup(blk("P", GREEN, 1.2, 1.2, 36), lab("adds a phosphate", 28, GREY)).arrange(DOWN, buff=0.15)
        add.move_to([-4.6, 0.0, 0])
        rem = VGroup(blk("P", GREEN, 1.2, 1.2, 36), lab("takes one off", 28, GREY)).arrange(DOWN, buff=0.15)
        rem.move_to([4.6, 0.0, 0])
        a1 = arr([-1.9, 0.5, 0], [-3.5, 0.5, 0], GREY)
        a2 = arr([3.5, 0.5, 0], [1.9, 0.5, 0], GREY)
        self.at("never put a phosphate")
        self.play(FadeIn(add), GrowArrow(a1), run_time=0.5)
        x1 = xmark([-2.7, 1.1, 0], 52)
        self.play(FadeIn(x1), run_time=0.3)
        self.at("took one off")
        self.play(FadeIn(rem), GrowArrow(a2), run_time=0.5)
        x2 = xmark([2.7, 1.1, 0], 52)
        self.play(FadeIn(x2), run_time=0.3)
        self.at("So what did it do")
        qq = qmark([0, -2.0, 0], 90)
        what = lab("what does it do?", 32, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(qq, scale=0.5), FadeIn(what), run_time=0.5)

        # which parts bind
        pA = VGroup(*[blk("", BLUE, 1.05, 1.9, op=0.22) for _ in range(3)]).arrange(RIGHT, buff=0.0)
        pB = VGroup(*[blk("", ORANGE, 1.05, 1.9, op=0.22) for _ in range(3)]).arrange(RIGHT, buff=0.0)
        pA.move_to([-3.6, 0.7, 0]); pB.move_to([3.6, 0.7, 0])
        qs = VGroup(*[qmark([x, 0.7, 0], 40) for x in (-4.65, -3.6, -2.55, 2.55, 3.6, 4.65)])
        pa_l = lab("protein A", 28, BLUE).next_to(pA, DOWN, buff=0.25)
        pb_l = lab("protein B", 28, ORANGE).next_to(pB, DOWN, buff=0.25)
        parts = lab("which parts do the binding?", 32, TEXT).move_to([0, -2.4, 0])
        self.at("Which parts do the binding")
        self.play(*[FadeOut(m) for m in [ste, ess, add, rem, a1, a2, x1, x2, qq, what]], run_time=0.4)
        self.play(FadeIn(pA), FadeIn(pB), FadeIn(pa_l), FadeIn(pb_l), run_time=0.5)
        self.play(FadeIn(qs), FadeIn(parts), run_time=0.5)

        # protein and DNA: which sequence
        d = Rectangle(width=11.6, height=0.7, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.5).move_to([0, -1.2, 0])
        ticks = VGroup(*[Line([x, -1.55, 0], [x, -0.85, 0], color=TEAL, stroke_width=1.5) for x in np.linspace(-5.6, 5.6, 29)])
        dl = lab("DNA", 30, TEAL).move_to([-5.9, -2.1, 0])
        box = DashedVMobject(Rectangle(width=1.6, height=1.3, stroke_color=YELLOW, stroke_width=4).move_to([1.8, -1.2, 0]))
        qd = qmark([1.8, -0.1, 0], 64)
        seq = lab("at which sequence?", 32, TEXT).move_to([1.8, -2.5, 0])
        self.at("at which sequence")
        self.play(*[FadeOut(m) for m in [pB, pb_l, qs, parts]], pA.animate.move_to([-3.6, 1.8, 0]),
                  pa_l.animate.move_to([-3.6, 0.55, 0]), run_time=0.6)
        self.play(FadeIn(d), FadeIn(ticks), FadeIn(dl), run_time=0.5)
        self.play(Create(box), FadeIn(qd), FadeIn(seq), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S02Ip(SpokenScene):
    """Immunoprecipitation: antibody beads pull the bait, and its partner, out of the extract."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.3, width=7.2, height=6.2, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.07).move_to([-3.4, -0.2, 0])
        tl = lab("extract: not heated", 28, TEXT).move_to([-3.4, 3.4, 0])
        greys = VGroup(*[blk("", GREY, w, 0.7, op=0.25).move_to([x, y, 0]) for x, y, w in
                         [(-5.4, 1.9, 1.3), (-2.9, 2.0, 1.2), (-1.0, 1.1, 1.0), (-5.6, -1.6, 1.2),
                          (-3.3, -1.9, 1.4), (-1.5, -1.3, 1.1), (-4.3, 0.9, 0.9), (-1.7, -2.2, 0.9)]])
        bait = blk("bait", BLUE, 1.5, 0.9, 26).move_to([-3.0, 0.0, 0])
        part = blk("partner", ORANGE, 1.5, 0.9, 24).move_to([-4.5, 0.0, 0])
        other = lab("other proteins", 24, GREY).move_to([-3.4, -3.0, 0])
        self.at("Immunoprecipitation starts")
        self.play(FadeIn(box), FadeIn(tl), run_time=0.5)
        self.play(FadeIn(greys), FadeIn(bait), FadeIn(part), run_time=0.7)

        R = 1.2
        c0 = np.array([5.2, 0.0, 0.0])
        bead = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4).move_to(c0)
        abs_ = VGroup(*[antibody([c0[0] - R + 0.02, dy], [-1, 0]) for dy in (-1.05, 0.0, 1.05)])
        beadg = VGroup(bead, abs_)
        bl = lab("protein A or G beads", 24, GREY).move_to([5.0, -1.9, 0])
        al = lab("antibody", 26, PURPLE).move_to([3.4, 1.9, 0])
        self.at("An antibody fixed")
        self.play(FadeIn(beadg), FadeIn(bl), FadeIn(al), run_time=0.7)
        self.at("pulls its protein")
        dock = np.array([-2.3 + 1.12 + R, 0.0, 0.0])
        self.play(FadeOut(bl), FadeOut(al), beadg.animate.shift(dock - c0), run_time=0.7)
        self.play(bait.box.animate.set_stroke(YELLOW, 5), run_time=0.2)
        self.at("out of the mixture")
        shift = np.array([5.2, 1.0, 0.0]) - dock
        self.play(beadg.animate.shift(shift), bait.animate.shift(shift), part.animate.shift(shift),
                  FadeOut(other), run_time=1.0)
        stay = lab("other proteins stay", 26, GREY).move_to([-3.4, -3.0, 0])
        self.add(stay)
        self.at("Partners bound to that")
        cp = lab("partner comes out with it", 28, ORANGE).move_to([3.9, 2.95, 0])
        self.play(FadeIn(cp), part.box.animate.set_stroke(YELLOW, 5), run_time=0.5)

        def mini(kind, cx):
            b = blk("", BLUE, 0.7, 0.5, op=0.35); p = blk("", ORANGE, 0.7, 0.5, op=0.35)
            g = blk("", GREY, 0.7, 0.5, op=0.35)
            if kind == 0:
                grp = VGroup(b, p).arrange(RIGHT, buff=0)
            elif kind == 1:
                grp = VGroup(b, g, p).arrange(RIGHT, buff=0)
            else:
                p2 = blk("", ORANGE, 0.7, 0.5, op=0.35); g2 = blk("", GREY, 0.7, 0.5, op=0.35)
                grp = VGroup(VGroup(b, p).arrange(RIGHT, buff=0), VGroup(g, g2, p2).arrange(RIGHT, buff=0)).arrange(DOWN, buff=0.0)
            return grp
        m1 = mini(0, 0).move_to([1.3, -1.9, 0]); m2 = mini(1, 0).move_to([3.3, -1.9, 0]); m3 = mini(2, 0).move_to([5.6, -2.0, 0])
        l1 = lab("directly", 24, GREY).move_to([1.3, -3.0, 0])
        l2 = lab("indirectly", 24, GREY).move_to([3.3, -3.0, 0])
        l3 = lab("larger complex", 24, GREY).move_to([5.6, -3.0, 0])
        self.at("bound directly")
        self.play(FadeIn(m1), FadeIn(l1), run_time=0.4)
        self.at("bound indirectly")
        self.play(FadeIn(m2), FadeIn(l2), run_time=0.4)
        self.at("larger complex")
        self.play(FadeIn(m3), FadeIn(l3), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S03Pulldown(SpokenScene):
    """Pull-down: GST-tagged bait on glutathione resin; only the tagged protein sticks; lysate partners stick too."""

    def construct(self):
        X = -1.4
        tagb = blk("GST", PINK, 1.8, 0.8, 28).move_to([X, 0.7, 0])
        bait = blk("bait", BLUE, 3.2, 1.1, 32).move_to([X, 1.65, 0])
        fused = VGroup(tagb, bait)
        tl = lines("tag fused", "to the protein", size=26, color=PINK, align=ORIGIN, buff=0.06).move_to([-5.4, 1.2, 0])
        self.at("A pull-down uses a tag")
        self.play(FadeIn(fused, shift=DOWN * 0.2), FadeIn(tl), run_time=0.7)

        resin = Circle(radius=1.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4).move_to([X, -4.6, 0])
        rl = lab("glutathione resin", 28, TEXT).move_to([X, -1.5, 0])
        self.at("run it over")
        self.play(FadeOut(tl), resin.animate.move_to([X, -1.5, 0]), run_time=0.9)
        rl.move_to([X, -1.5, 0])
        self.play(FadeIn(rl), run_time=0.3)

        gs = VGroup(*[blk("", GREY, 1.2, 0.7, op=0.3).move_to([-7.5 - 1.8 * i, 2.9, 0]) for i in range(3)])
        un = lab("untagged proteins pass by", 26, GREY).move_to([3.8, 3.5, 0])
        self.at("Only the tagged protein sticks")
        self.play(FadeIn(un), run_time=0.2)
        self.play(*[g.animate.shift(RIGHT * 16.0) for g in gs], run_time=2.0, rate_func=linear)

        lys = RoundedRectangle(corner_radius=0.3, width=4.6, height=3.8, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.07).move_to([4.4, -0.9, 0])
        lt = lab("lysate", 28, TEXT).move_to([4.4, 0.45, 0])
        part = blk("partner", ORANGE, 1.9, 1.0, 26).move_to([3.5, -0.4, 0])
        oth = VGroup(blk("", GREY, 1.1, 0.7, op=0.3).move_to([5.4, -0.2, 0]),
                     blk("", GREY, 1.3, 0.7, op=0.3).move_to([4.2, -1.5, 0]),
                     blk("", GREY, 0.9, 0.7, op=0.3).move_to([5.7, -1.7, 0]))
        self.at("Add a lysate")
        self.play(FadeOut(un), FadeIn(lys), FadeIn(lt), FadeIn(part), FadeIn(oth), run_time=0.7)
        self.at("partners can stick")
        self.play(FadeOut(oth), FadeOut(lys), FadeOut(lt), part.animate.move_to([X + 1.6 + 0.95, 1.65, 0]), run_time=1.0)
        self.play(part.box.animate.set_stroke(YELLOW, 5), run_time=0.3)

        dom = blk("domain", BLUE, 1.7, 0.9, 28).move_to([X, 1.55, 0])
        dl = lab("bait: an isolated domain", 28, BLUE).move_to([X, 3.1, 0])
        self.at("isolated domain")
        self.play(ReplacementTransform(bait, dom), FadeIn(dl), part.animate.move_to([X + 0.85 + 0.95, 1.55, 0]), run_time=0.8)
        self.at("western blot")
        strip = Rectangle(width=3.0, height=2.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([4.8, -1.4, 0])
        bnd = band(4.8, -1.4, 2.2, 0.34, ORANGE, 0.9)
        dt = lab("detect: western blot", 28, TEXT).move_to([4.8, 0.4, 0])
        exs = lab("example data", 22, GREY).move_to([4.8, -3.0, 0])
        self.play(FadeIn(strip), FadeIn(bnd), FadeIn(dt), FadeIn(exs), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S04Gelshift(SpokenScene):
    """Gel shift: protein + labelled DNA, native gel, bound DNA runs slower; bound and free in one lane."""

    def construct(self):
        P = blk("protein", BLUE, 2.8, 1.5, 34).move_to([-3.6, 0.3, 0])
        D = dna(5.0, 0.7).move_to([2.6, 0.3, 0])
        dl = lab("labelled DNA", 32, TEAL).move_to([2.6, 1.3, 0])
        ml = lab("mix", 34, TEXT).move_to([0, 2.8, 0])
        self.at("A gel shift handles")
        self.play(FadeIn(P, shift=RIGHT * 0.3), FadeIn(D), FadeIn(dl), run_time=0.7)
        self.at("Mix the protein")
        self.play(FadeIn(ml), P.animate.move_to([2.6, 1.1, 0]).scale(0.55), dl.animate.move_to([2.6, -0.7, 0]), run_time=1.0)

        # gel
        gx0, gx1, gy0, gy1 = -6.3, 0.9, -3.15, 2.5
        gel = Rectangle(width=gx1 - gx0, height=gy1 - gy0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
        gel.move_to([(gx0 + gx1) / 2, (gy0 + gy1) / 2, 0])
        L1, L2 = -4.7, -1.8
        wells = VGroup(*[Rectangle(width=2.0, height=0.3, stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([x, 2.1, 0]) for x in (L1, L2)])
        gl = lab("native gel", 28, TEXT).move_to([-2.7, 3.2, 0])
        n1 = lab("free DNA", 24, TEAL).move_to([L1, -3.5, 0])
        n2 = lab("DNA + protein", 24, TEXT).move_to([L2, -3.5, 0])
        self.at("run it on a native gel")
        self.play(FadeOut(P), FadeOut(D), FadeOut(dl), FadeOut(ml), run_time=0.4)
        self.play(FadeIn(gel), FadeIn(wells), FadeIn(gl), FadeIn(n1), FadeIn(n2), run_time=0.7)

        def comp(x, y, w=1.7, op=0.9):
            return VGroup(band(x, y, w, 0.26, TEAL, op), Rectangle(width=w * 0.5, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=op).move_to([x, y + 0.23, 0]))
        free1 = band(L1, 1.8, 1.7, 0.26, TEAL, 0.9)
        free2 = band(L2, 1.8, 1.7, 0.26, TEAL, 0.35)
        bound2 = comp(L2, 1.8, 1.7, 0.95)
        self.play(FadeIn(free1), FadeIn(free2), FadeIn(bound2), run_time=0.4)
        rt = lab("idealised", 22, GREY).move_to([5.7, 3.25, 0])
        self.play(FadeIn(rt), run_time=0.2)
        self.at("migrate more slowly")
        self.play(free1.animate.shift(DOWN * 4.5), free2.animate.shift(DOWN * 4.5), bound2.animate.shift(DOWN * 2.3),
                  run_time=3.2, rate_func=linear)
        fl = lab("free DNA runs farther", 28, TEAL).move_to([4.0, -2.7, 0])
        bl = lab("protein-bound DNA: slower", 28, BLUE).move_to([3.7, -0.5, 0])
        fa = arr([1.05, -2.7, 0], [0.55, -2.7, 0], TEAL, 3, 0.15)
        ba = arr([1.05, -0.5, 0], [0.55, -0.5, 0], BLUE, 3, 0.15)
        self.play(FadeIn(bl), FadeIn(ba), FadeIn(fl), FadeIn(fa), run_time=0.5)
        br = Rectangle(width=2.3, height=3.4, stroke_color=YELLOW, stroke_width=4).move_to([L2, -1.45, 0])
        one = lab("both measured in one lane", 28, YELLOW).move_to([4.0, 1.3, 0])
        self.at("one lane")
        self.play(Create(br), FadeIn(one), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """Reading an example blot and an example gel shift."""

    def construct(self):
        lx, rx = -3.6, 3.4
        ht = lab("IP, then blot for the partner", 28, TEXT).move_to([lx, 3.3, 0])
        strip = Rectangle(width=3.6, height=4.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([lx, 1.0, 0])
        bnd = band(lx, 1.0, 2.6, 0.42, ORANGE, 0.95)
        ex1 = lab("example data", 22, GREY).move_to([lx, -1.25, 0])
        pl = lab("partner band", 30, ORANGE).move_to([lx, -2.0, 0])
        pl2 = lab("the two were in one complex", 26, TEXT).move_to([lx, -2.75, 0])
        ht2 = lab("gel shift", 28, TEXT).move_to([rx, 3.3, 0])
        gel = Rectangle(width=5.2, height=4.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([rx, 1.0, 0])
        L1, L2 = rx - 1.3, rx + 1.3
        f1 = band(L1, -0.7, 2.0, 0.28, TEAL, 0.9)
        f2 = band(L2, -0.7, 2.0, 0.28, TEAL, 0.3)
        b2 = VGroup(band(L2, 1.3, 2.0, 0.32, TEAL, 0.95),
                    Rectangle(width=1.0, height=0.24, stroke_width=0, fill_color=BLUE, fill_opacity=0.95).move_to([L2, 1.58, 0]))
        n1 = lab("DNA", 24, TEAL).move_to([L1, -1.25, 0])
        n2 = lab("DNA + protein", 24, TEXT).move_to([L2, -1.25, 0])
        ex2 = lab("example data", 22, GREY).move_to([rx, 3.3 - 0.0, 0]); ex2.move_to([rx + 2.2, -1.25 - 0.55, 0]); ex2.move_to([rx, -1.7, 0])
        sl = lab("slower band: a DNA-binding factor", 26, BLUE).move_to([rx, -2.3, 0])
        sl2 = lab("its strength: how much is active", 26, TEXT).move_to([rx, -2.95, 0])
        self.at("The catch from")
        self.play(FadeIn(ht), FadeIn(strip), run_time=0.5)
        self.at("blotted for a suspected partner")
        self.play(FadeIn(ex1), run_time=0.3)
        self.at("A band there")
        self.play(FadeIn(bnd, scale=0.6), FadeIn(pl), run_time=0.5)
        self.at("one complex")
        self.play(FadeIn(pl2), run_time=0.5)
        self.at("On a gel shift")
        self.play(FadeIn(ht2), FadeIn(gel), FadeIn(n1), FadeIn(n2), FadeIn(f1), FadeIn(f2), FadeIn(b2), FadeIn(ex2), run_time=0.7)
        self.at("a slower band")
        self.play(Create(SurroundingRectangle(b2, color=YELLOW, stroke_width=4, buff=0.12)), FadeIn(sl), run_time=0.6)
        self.at("how much of it")
        self.play(FadeIn(sl2), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Three ways a lysate result misleads, and the control under each."""

    def construct(self):
        cx = [-4.6, 0.0, 4.6]
        pw, ph = 4.3, 7.0
        frames = VGroup(*[RoundedRectangle(corner_radius=0.2, width=pw, height=ph, stroke_color=GREY, stroke_width=2,
                                           fill_color=GREY, fill_opacity=0.05).move_to([x, 0, 0]) for x in cx])
        hd = [lab(t, 32, RED, weight=BOLD).move_to([x, 3.05, 0]) for t, x in
              zip(["indirect?", "after lysis?", "sticky resin?"], cx)]

        # panel 1: bait - grey - partner, stacked
        b = blk("bait", BLUE, 2.4, 0.9, 28)
        g = blk("", GREY, 1.0, 0.9, op=0.3)
        p = blk("partner", ORANGE, 2.4, 0.9, 28)
        stack = VGroup(b, g, p).arrange(DOWN, buff=0.0).move_to([cx[0], 1.35, 0])
        c1 = lab("direct or indirect?", 28, TEXT).move_to([cx[0], -0.8, 0])
        k1 = lines("test with", "purified parts", size=28, color=GREEN, align=ORIGIN, buff=0.1).move_to([cx[0], -2.4, 0])
        # panel 2: compartments
        room = Rectangle(width=3.7, height=2.8, stroke_color=GREY, stroke_width=2).move_to([cx[1], 1.2, 0])
        wall = Line([cx[1], 2.6, 0], [cx[1], -0.2, 0], color=GREY, stroke_width=6)
        b2 = blk("", BLUE, 1.1, 1.0).move_to([cx[1] - 1.2, 1.2, 0])
        p2 = blk("", ORANGE, 1.1, 1.0).move_to([cx[1] + 1.2, 1.2, 0])
        c2 = lab("never meet in a cell", 26, RED).move_to([cx[1], -0.8, 0])
        # panel 3: sticky resin
        bead = Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4).move_to([cx[2], 0.7, 0])
        stuck = blk("syntaxin", ORANGE, 1.9, 0.7, 24, op=0.3).move_to([cx[2], 2.2, 0])
        c3 = lab("bound the resin itself", 26, RED).move_to([cx[2], -0.8, 0])
        k3 = lines("control IPs with", "other antibodies", "mock IPs", "in a pull-down:", "GST alone",
                   size=24, color=GREEN, align=ORIGIN, buff=0.12).move_to([cx[2], -2.1, 0])

        self.at("Binding in a lysate")
        self.play(FadeIn(frames), run_time=0.4)
        self.at("does not say direct")
        self.play(FadeIn(hd[0]), FadeIn(stack), FadeIn(c1), run_time=0.7)
        self.at("Lysis removes compartments")
        self.play(FadeIn(hd[1]), FadeIn(room), FadeIn(wall), FadeIn(b2), FadeIn(p2), run_time=0.6)
        self.at("proteins that never meet")
        self.play(FadeOut(wall), FadeOut(room), b2.animate.move_to([cx[1] - 0.58, 1.2, 0]), p2.animate.move_to([cx[1] + 0.58, 1.2, 0]), FadeIn(c2), run_time=0.9)
        self.at("resin can be sticky")
        self.play(FadeIn(hd[2]), FadeIn(bead), run_time=0.5)
        self.at("which bound the resin")
        self.play(FadeIn(stuck, shift=DOWN * 0.4), FadeIn(c3), run_time=0.6)
        self.at("Control IPs")
        self.play(FadeIn(k3[0]), FadeIn(k3[1]), run_time=0.5)
        self.at("mock IPs")
        self.play(FadeIn(k3[2]), run_time=0.4)
        self.at("can serve as")
        self.play(FadeIn(k3[3]), FadeIn(k3[4]), run_time=0.5)
        self.at("purified parts")
        self.play(FadeIn(k1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S07Found(SpokenScene):
    """Two findings: SH2 domains alone bind receptors only after stimulation (1990); Bax with Bcl-2 (1993)."""

    def construct(self):
        lx, rx = -3.6, 3.6
        div = Line([0, 3.5, 0], [0, -3.5, 0], color=GREY, stroke_width=2)
        y1 = T("1990", 44, GOLD, font=TITLE_FONT).move_to([lx, 3.1, 0])
        y2 = T("1993", 44, GOLD, font=TITLE_FONT).move_to([rx, 3.1, 0])
        # left: SH2 (row B first: binds; then row A: no stimulation)
        t1 = lab("made alone in bacteria", 28, BLUE).move_to([lx, 2.2, 0])
        sB = blk("SH2 domain", BLUE, 2.7, 1.1, 28)
        rB = blk("receptor", ORANGE, 2.7, 1.1, 28)
        rowB = VGroup(sB, rB).arrange(RIGHT, buff=0.0).move_to([lx, -0.8, 0])
        labB = lab("after stimulation: binds", 28, GREEN).move_to([lx, -1.9, 0])
        sA = blk("SH2 domain", BLUE, 2.7, 1.1, 28)
        rA = blk("receptor", ORANGE, 2.7, 1.1, 28)
        rowA = VGroup(sA, rA).arrange(RIGHT, buff=1.0).move_to([lx, 1.2, 0])
        xx = xmark([lx, 1.2, 0], 44)
        labA = lab("no stimulation: no binding", 28, RED).move_to([lx, 0.2, 0])
        tag1 = lab("Anderson, Pawson & colleagues, 1990", 22, GREY).move_to([lx, -3.1, 0])
        # right: Bcl-2 / Bax
        bcl = blk("Bcl-2", BLUE, 2.9, 2.0, 38).move_to([rx - 1.7, 0.7, 0])
        bax = blk("Bax", ORANGE, 2.3, 2.0, 38).move_to([rx + 1.9, 0.7, 0])
        bax[1].set_opacity(0)
        kd = lab("21 kDa", 30, ORANGE).move_to([rx + 1.9, 2.15, 0])
        qb = qmark([rx + 0.1, 0.7, 0], 64)
        asc = lab("associated with Bcl-2", 30, TEXT).move_to([rx, -1.0, 0])
        het = lab("heterodimers, in vivo", 30, ORANGE).move_to([rx, -1.0, 0])
        tag2 = lab("Oltvai, Milliman & Korsmeyer, 1993", 22, GREY).move_to([rx, -3.1, 0])

        self.at("In 1990")
        self.play(FadeIn(div), FadeIn(y1), run_time=0.5)
        self.at("Anderson")
        s0 = blk("SH2 domain", BLUE, 2.7, 1.1, 28).move_to([lx, 0.6, 0])
        self.play(FadeIn(s0), run_time=0.4)
        self.at("alone in bacteria")
        self.play(FadeIn(t1), run_time=0.4)
        self.at("bound growth factor receptors")
        lbox = RoundedRectangle(corner_radius=0.25, width=6.6, height=5.0, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.06).move_to([lx, -0.05, 0])
        llab = lab("cell lysate", 28, TEXT).move_to([lx, 2.2, 0])
        self.play(FadeOut(t1), FadeOut(s0), FadeIn(lbox), FadeIn(llab), FadeIn(rowB), run_time=0.5)
        self.at("only after stimulation")
        self.play(FadeIn(rowA), FadeIn(xx), FadeIn(labA), FadeIn(labB), run_time=0.6)
        self.at("on its own")
        self.play(FadeIn(tag1), sB.box.animate.set_stroke(YELLOW, 5), run_time=0.5)
        self.at("In 1993")
        self.play(FadeIn(y2), FadeIn(bcl), run_time=0.6)
        self.at("kilodalton protein")
        self.play(FadeIn(bax), FadeIn(kd), FadeIn(qb), run_time=0.5)
        self.at("associated with")
        self.play(FadeIn(asc), FadeIn(tag2), run_time=0.5)
        self.at("and reported", lead=1.0)
        self.play(bax[1].animate.set_opacity(1), run_time=0.4)
        self.at("forms heterodimers", lead=0.5)
        self.play(FadeOut(qb), run_time=0.2)
        self.play(bcl.animate.move_to([rx - 1.3, 0.7, 0]), bax.animate.move_to([rx + 1.3, 0.7, 0]), kd.animate.move_to([rx + 1.3, 2.15, 0]), run_time=0.7)
        self.play(FadeOut(asc), FadeIn(het), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S08Rule(SpokenScene):
    """Idealised gel shift: NF-kB binding activity appears with protein synthesis blocked; then the rule."""

    def construct(self):
        gx0, gx1, gy0, gy1 = -6.6, 1.0, -3.0, 2.6
        gel = Rectangle(width=gx1 - gx0, height=gy1 - gy0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18)
        gel.move_to([(gx0 + gx1) / 2, (gy0 + gy1) / 2, 0])
        xs = [-5.2, -2.8, -0.4]
        wells = VGroup(*[Rectangle(width=1.7, height=0.28, stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=1).move_to([x, 2.2, 0]) for x in xs])
        names = [lines("no", "LPS", size=22, color=TEXT, align=ORIGIN, buff=0.04),
                 lines("LPS", size=22, color=TEXT, align=ORIGIN, buff=0.04),
                 lines("LPS, protein", "synthesis blocked", size=22, color=TEXT, align=ORIGIN, buff=0.04)]
        for n, x in zip(names, xs):
            n.move_to([x, -3.55, 0])
        names[0].move_to([xs[0], -3.55, 0])
        ex = lab("schematic", 30, TEXT).move_to([5.9, 3.3, 0])
        top = lab("pre-B cells, DNA-binding activity", 28, TEXT).move_to([-2.8, 3.3, 0])
        def cplx(x, y=-0.2):
            return VGroup(band(x, y, 1.5, 0.26, TEAL, 0.95), Rectangle(width=0.75, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.95).move_to([x, y + 0.23, 0]))
        free = [band(x, -2.3, 1.5, 0.24, TEAL, 0.9) for x in xs]
        c2, c3 = cplx(xs[1]), cplx(xs[2]).scale(1.15)
        bl = lab("slower band appears", 28, BLUE).move_to([4.0, -0.2, 0])
        al = lines("even with protein", "synthesis blocked", size=26, color=TEXT, align=ORIGIN, buff=0.06).move_to([4.0, -1.0, 0])
        so = lines("so the factor had", "to exist already", size=26, color=ORANGE, align=ORIGIN, buff=0.06).move_to([4.0, -2.1, 0])
        tg = lab("Sen & Baltimore, 1986", 24, GOLD).move_to([4.0, 1.6, 0])

        self.at("A gel shift showed")
        self.play(FadeIn(gel), FadeIn(wells), FadeIn(top), FadeIn(ex), *[FadeIn(n) for n in names], *[FadeIn(f) for f in free], run_time=0.7)
        self.at("activity appear")
        self.play(FadeIn(c2, shift=DOWN * 0.3), run_time=0.5)
        self.play(FadeIn(bl), run_time=0.4)
        self.at("even with protein synthesis")
        self.play(FadeIn(c3, shift=DOWN * 0.3), FadeIn(al), run_time=0.6)
        self.at("So the factor had")
        self.play(FadeIn(so), run_time=0.5)
        self.at("Sen and Baltimore")
        self.play(FadeIn(tg), run_time=0.4)
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("Binding in a lysate may be", "indirect, or happen only", "after lysis.", size=44, color=TEXT, buff=0.22, align=ORIGIN)
        rb = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.5, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(rb, UP, buff=0.25)
        self.play(FadeIn(head), Create(rb), run_time=0.5)
        self.at("binding in a lysate")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S09End(EndCard):
    LINE = "Binding in a lysate may be indirect, or happen only after lysis."
