"""Lipids as anchors and addresses: two weak grips make one strong hold  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the protein (Ras) and the receptor
  ORANGE = a fatty chain on the protein (farnesyl, palmitate): the lipid grip
  TEAL   = the patch of positive charge (lysines): the charge grip
  PINK   = negative charge (the lipids of the inner face, the charge a phosphate adds)
  GOLD   = a phosphate (the round "P" badge)
  PURPLE = an enzyme that edits the grip (the attaching enzyme, protein kinase C, a thioesterase)
  YELLOW = the growth signal
  GREEN  = held, tighter, comfortable
  RED    = weak, uncomfortable, let go, or ruled out
  GREY   = the membrane, labels, parts not yet known

No molecular structures: the protein is a labelled blob, a fatty chain is a plain capsule, the lysine
patch is a pad with plus signs, charge is a plus or minus sign, a membrane is a bar, a bond is a ring.

One picture, kept the whole film: the membrane across the top, the protein hanging from it by its
chain or chains. The size of the protein and the height of the membrane are set for each scene so the
action fills the frame (use(k, mem_y)): scenes 1 to 4 hang a protein 1.6 times its base size,
scenes 5 and 6 draw it at 1.8, and scene 4 splits the frame (proteins left, the numbers right).
Scene 1 starts lower on the screen and slides up at its end to the position scene 2 starts from.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
PINK = "#F08BB4"

MEM_H = 0.6                               # thickness of the membrane bar
LAY = {"k": 1.6, "mem_y": 2.6}            # protein scale and membrane height, set per scene by use()


def use(k, mem_y):
    LAY["k"], LAY["mem_y"] = k, mem_y


def my():
    return LAY["mem_y"]


def mem_bot():
    """the inner face of the membrane."""
    return LAY["mem_y"] - MEM_H / 2


def bound_y(k=None):
    """body centre of a protein whose chain runs up to the middle of the membrane."""
    return LAY["mem_y"] - 1.55 * (k or LAY["k"])


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.2, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def pop(m, s=1.2):
    """swell and settle, without recolouring."""
    return m.animate(rate_func=there_and_back).scale(s)


def shake(m, amp=0.09, n=3):
    """jiggle sideways and come back to rest."""
    return m.animate(rate_func=lambda t: np.sin(t * TAU * n) * (1 - t)).shift(RIGHT * amp)


def minus(c, s=0.2, color=PINK, w=4.5):
    c = np.array(c, float)
    return Line(c + LEFT * s / 2, c + RIGHT * s / 2, color=color, stroke_width=w)


def plus(c, s=0.2, color=TEAL, w=4.5):
    c = np.array(c, float)
    return VGroup(Line(c + LEFT * s / 2, c + RIGHT * s / 2, color=color, stroke_width=w),
                  Line(c + DOWN * s / 2, c + UP * s / 2, color=color, stroke_width=w))


def pbadge(k=1.0):
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def membrane():
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, my(), 0])


def sides():
    out = T("outside", 24, GREY).move_to([-5.45, my() + 0.75, 0])
    cyt = T("cytosol", 24, GREY).move_to([-5.5, -3.15, 0])
    return out, cyt


def minus_row(anchor, left=15, right=4, step=0.6):
    """the negative lipids of the inner face: minus signs along the underside of the membrane."""
    return VGroup(*[minus([anchor + step * j, mem_bot() + 0.17, 0], 0.3, PINK, 6) for j in range(-left, right + 1)])


# the protein -------------------------------------------------------------------------------
def chain_at(x, body_top, k, color=ORANGE):
    """a fatty chain: a plain capsule rising from the top of the protein."""
    w, h = 0.24 * k, 1.0 * k
    return RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.9).move_to([x, body_top - 0.05 * k + h / 2, 0])


def ras(cx, name="Ras", y=None, chain=True, size=30):
    """a labelled blob; its farnesyl chain on the left. [chain, back, body, label]"""
    k = LAY["k"]
    y = bound_y() if y is None else y
    c = np.array([cx, y, 0.0])
    top = y + 0.6 * k
    back = RoundedRectangle(corner_radius=0.4 * k, width=2.1 * k, height=1.2 * k, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c)
    body = RoundedRectangle(corner_radius=0.4 * k, width=2.1 * k, height=1.2 * k, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.25).move_to(c)
    lbl = T(name, size * k, BLUE, weight=BOLD).move_to(c)
    g = VGroup()
    g.k, g.tails = k, []
    if chain:
        t = chain_at(cx - 0.55 * k, top, k)
        g.tails.append(t)
        g.add(t)
    g.add(back, body, lbl)
    g.back, g.body, g.lbl = back, body, lbl
    return g


def new_chain(g):
    """the second chain, on the right."""
    return chain_at(g.body.get_center()[0] + 0.55 * g.k, g.body.get_top()[1], g.k)


def new_patch(g):
    """the pad of lysines, on the top edge of the body. pg.pad is the pad, pg.centre where it sits."""
    k, c, top = g.k, g.body.get_center(), g.body.get_top()[1]
    pc = np.array([c[0] + 0.15 * k, top + 0.04 * k, 0])
    pad = RoundedRectangle(corner_radius=0.1 * k, width=0.72 * k, height=0.34 * k, stroke_color=TEAL, stroke_width=2,
                           fill_color=TEAL, fill_opacity=0.95).move_to(pc)
    pg = VGroup(pad, *[plus(pc + np.array([dx * k, 0, 0]), 0.17 * k, BG, 3.5) for dx in (-0.22, 0.0, 0.22)])
    pg.pad, pg.centre = pad, pc
    return pg


def pulls(pg, k):
    """dashed lines from the patch to the negative lipids above it (two of the minus signs)."""
    c = pg.centre
    return VGroup(*[DashedLine([c[0] + dx, c[1] + 0.2 * k, 0], [c[0] + dx, mem_bot() + 0.06, 0], color=TEAL,
                               stroke_width=4, dash_length=0.09) for dx in (-0.3, 0.3)])


def relabel(scene, g, name, size=28, run_time=0.4):
    """swap the protein's name; the old label fades, the new one joins the group."""
    new = T(name, size * g.k, BLUE, weight=BOLD).move_to(g.body)
    scene.play(g.lbl.animate.set_opacity(0), FadeIn(new), run_time=run_time)
    scene.remove(new)
    g.add(new)
    g.lbl = new


def slot(x, body_top, k):
    """a dashed outline where a chain used to be."""
    w, h = 0.24 * k, 1.0 * k
    shape = RoundedRectangle(corner_radius=w / 2, width=w, height=h).move_to([x, body_top - 0.05 * k + h / 2, 0])
    return DashedVMobject(shape, num_dashes=22).set_color(ORANGE).set_stroke(width=3)


class Film(SpokenScene):
    def outro(self, *anims, then=None, after=None, run_time=0.38):
        """hold until the narration ends, clear what the next scene does not inherit, then (optionally)
        move the pieces the next scene starts from (`then`) and bring in what is new (`after`)."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
        if after:
            self.play(*after, run_time=0.45)
        if then or after:
            self.wait(0.15)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Lipids as Anchors and Addresses"
    TITLE = "Two weak grips make one strong hold"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(Film):
    """Ras sits under the membrane with nothing holding it; a fatty chain is the answer."""

    def construct(self):
        use(1.6, 1.5)
        k = 1.6
        mem = membrane()
        out, cyt = sides()
        R = ras(0.7, "Ras", chain=False)
        top = R.body.get_top()[1]
        tx = 0.7 - 0.55 * k                                  # where the chain will grow
        band = (mem_bot() + top) / 2                         # the gap between Ras and the inner face

        # the stretch that would cross the membrane, rising from Ras: it is not there
        tm = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.38, height=2.72).move_to([1.5, top + 1.36, 0]),
                            num_dashes=32).set_color(BLUE).set_stroke(width=3)
        tm_lbl = T("crosses the membrane", 26, GREY).move_to([4.1, my() + 0.95, 0])
        xm = VGroup(Line([1.05, my() - 0.45, 0], [1.95, my() + 0.45, 0], color=RED, stroke_width=9),
                    Line([1.05, my() + 0.45, 0], [1.95, my() - 0.45, 0], color=RED, stroke_width=9))
        none = T("Ras has none", 30, RED, weight=BOLD).move_to([4.4, -0.1, 0])
        face = T("inner face", 26, GREY).move_to([3.7, band, 0])

        # the receptor, and the signal it relays inward to Ras
        rec = bchip("receptor", BLUE, 26, pad=0.18).move_to([-3.6, my(), 0])
        sig = bchip("growth signal", YELLOW, 26, pad=0.15).move_to([-3.6, my() + 1.35, 0])
        down = Arrow([-3.6, my() + 1.0, 0], [-3.6, my() + 0.42, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.2)
        relay = Arrow([-3.6, my() - 0.4, 0], [-1.2, top - 0.5, 0], buff=0.04, color=YELLOW, stroke_width=7, tip_length=0.26)

        # the unknown that holds Ras
        qbox = RoundedRectangle(corner_radius=0.14, width=0.75, height=0.85)
        q = VGroup(qbox.copy().set_stroke(width=0).set_fill(BG, 1).move_to([tx, band, 0]),
                   DashedVMobject(qbox.copy().move_to([tx, band, 0]), num_dashes=22).set_color(GREY),
                   T("?", 40, TEXT, weight=BOLD).move_to([tx, band, 0]))

        self.play(FadeIn(mem), FadeIn(out), FadeIn(cyt), run_time=0.4)
        self.play(FadeIn(R, shift=UP * 0.2), run_time=0.5)

        self.at("inner face")
        self.play(FadeIn(face, shift=RIGHT * 0.1), Indicate(mem, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.play(pop(R, 1.05), run_time=0.5)

        self.at("no stretch")
        self.play(Create(tm), FadeIn(tm_lbl, shift=DOWN * 0.1), run_time=0.8)
        self.at("that crosses")
        self.play(Create(xm), run_time=0.4)
        self.play(FadeIn(none, shift=LEFT * 0.1), run_time=0.4)

        self.at("what holds")
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.play(pop(q, 1.3), run_time=0.5)

        self.at("growth signal")
        self.play(FadeIn(rec), FadeIn(sig, shift=DOWN * 0.2), GrowArrow(down), run_time=0.7)
        self.at("inward")
        self.play(GrowArrow(relay), run_time=0.6)
        self.at("where it sits")
        self.play(pop(R, 1.05), pop(q, 1.3), run_time=0.6)

        # the answer: the question box becomes a chain that runs up into the membrane
        self.at("The answer")
        self.play(pop(q, 1.3), run_time=0.5)
        tail = chain_at(tx, top, k)
        fc = T("fatty chain", 28, ORANGE).next_to(tail, LEFT, buff=0.25).set_y(band + 0.2)
        self.at("fatty chain")
        self.play(FadeOut(q), GrowFromEdge(tail, DOWN), run_time=0.7)
        self.play(FadeIn(fc, shift=RIGHT * 0.1), run_time=0.4)
        self.remove(tail)
        R.add(tail)
        R.tails.append(tail)
        # clear the puzzle, then slide the picture up to where the next scene starts
        self.outro(FadeOut(VGroup(tm, tm_lbl, xm, none, face, rec, sig, down, relay, fc)),
                   then=[m.animate.shift(UP * 1.1) for m in (mem, out, R)])


# ---------------------------------------------------------------------------------------------
class S02Weak(Film):
    """one short chain is a weak grip: the protein visits the membrane and leaves."""

    def construct(self):
        use(1.6, 2.6)
        k = 1.6
        mem = membrane()
        out, cyt = sides()
        R = ras(0.7, "Ras")
        self.add(mem, out, cyt, R)
        tail = R.tails[0]
        top = R.body.get_top()[1]
        band = (mem_bot() + top) / 2
        joint = np.array([tail.get_center()[0], top, 0])
        low, high = -2.0, bound_y()

        enz = bchip("enzyme", PURPLE, 26).move_to([-3.2, band, 0])
        link = DashedLine(enz.get_right(), joint + LEFT * 0.1, color=PURPLE, stroke_width=4, dash_length=0.1)
        self.at("attach fatty")
        self.play(Indicate(tail, color=TEXT, scale_factor=1.12), run_time=0.6)
        self.at("dedicated enzymes")
        self.play(FadeIn(enz, shift=RIGHT * 0.2), Create(link), run_time=0.6)
        self.play(Flash(joint, color=PURPLE, line_length=0.25, flash_radius=0.35, num_lines=10), run_time=0.6)

        name = T("farnesyl", 28, ORANGE).next_to(tail, LEFT, buff=0.25).set_y(band)
        self.at("is called")
        self.play(FadeOut(enz), FadeOut(link), run_time=0.3)
        self.play(FadeIn(name, shift=RIGHT * 0.1), run_time=0.4)

        # in a membrane the chain is comfortable; in water it is not
        good = T("comfortable", 26, GREEN).next_to(tail, RIGHT, buff=0.3).set_y(band)
        self.at("long chain")
        self.play(Indicate(tail, color=TEXT, scale_factor=1.2), run_time=0.6)
        self.at("comfortable buried")
        self.play(tail.animate.set_stroke(GREEN, 4), FadeIn(good, shift=LEFT * 0.1), run_time=0.6)
        loose = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=1.5, height=0.36).move_to([-3.8, -0.4, 0]),
                               num_dashes=28).set_color(ORANGE).set_stroke(width=3)
        bad = T("uncomfortable in water", 26, RED).move_to([-3.6, -1.15, 0])
        self.at("uncomfortable in")
        self.play(FadeIn(loose, shift=UP * 0.1), FadeIn(bad, shift=UP * 0.1), run_time=0.6)

        # one chain is a weak grip: it pops out
        weak = T("a weak grip", 28, RED, weight=BOLD).next_to(tail, RIGHT, buff=0.3).set_y(band)
        self.at("one short chain")
        self.play(pop(tail, 1.4), run_time=0.6)
        self.at("weak grip")
        self.play(FadeOut(loose), FadeOut(bad), FadeOut(good), tail.animate.set_stroke(ORANGE, 2.5),
                  FadeIn(weak, shift=LEFT * 0.1), run_time=0.5)
        self.play(shake(R, 0.1, 3), run_time=0.7)
        self.at("pop out")
        R.body.set_stroke(RED, 4)
        self.play(R.animate.shift(DOWN * (high - low)), FadeOut(name), run_time=0.9)
        # the protein visits the membrane, then leaves
        self.at("visits a")
        R.body.set_stroke(BLUE, 3)
        self.play(R.animate.shift(UP * (high - low)), run_time=1.0)
        self.at("leaves it")
        R.body.set_stroke(RED, 4)
        self.play(R.animate.shift(DOWN * (high - low)), run_time=1.0)
        self.at("still tied")
        self.play(Indicate(tail, color=TEXT, scale_factor=1.2), run_time=0.7)
        self.outro(FadeOut(weak))


# ---------------------------------------------------------------------------------------------
class S03Second(Film):
    """a second signal of one of two kinds: a second fatty chain (H-Ras) or a patch of positive charge (K-Ras4B)."""

    def construct(self):
        use(1.6, 2.6)
        k = 1.6
        mem = membrane()
        out, cyt = sides()
        R = ras(0.7, "Ras", y=-2.0)
        self.add(mem, out, cyt, R)
        self.at("cells add")
        self.play(R.animate.shift(UP * (bound_y() - (-2.0))), run_time=1.0)

        # one protein becomes two, to show the two kinds
        H, K = ras(0.7, "Ras"), ras(0.7, "Ras")
        band = (mem_bot() + H.body.get_top()[1]) / 2
        self.at("one of two")
        self.remove(R)
        self.add(H, K)
        self.play(H.animate.shift(LEFT * 4.3), K.animate.shift(RIGHT * 2.9), run_time=1.0)

        # kind one: a second fatty chain
        c2 = new_chain(H)
        h1 = T("a second fatty chain", 28, ORANGE).move_to([-3.6, -1.75, 0])
        self.at("second fatty chain")
        self.play(GrowFromEdge(c2, DOWN), FadeIn(h1, shift=UP * 0.1), run_time=0.7)
        self.remove(c2)
        H.add(c2)
        self.at("as in")
        relabel(self, H, "H-Ras", 26)
        fH = T("farnesyl", 26, ORANGE).next_to(H.tails[0], LEFT, buff=0.15).set_y(band)
        pH = T("palmitate", 26, ORANGE).next_to(c2, RIGHT, buff=0.15).set_y(band)
        self.at("which carries")
        self.play(FadeIn(fH, shift=RIGHT * 0.1), run_time=0.4)
        self.at("plus")
        self.play(FadeIn(pH, shift=LEFT * 0.1), pop(c2, 1.3), run_time=0.6)

        # kind two: a patch of positive charge
        pg = new_patch(K)
        h2 = T("a patch of positive charge", 28, TEAL).move_to([3.6, -1.75, 0])
        self.at("The other kind")
        self.play(pop(K, 1.05), run_time=0.6)
        self.at("patch of positive")
        self.play(FadeIn(pg, scale=0.6), FadeIn(h2, shift=UP * 0.1), run_time=0.7)
        self.remove(pg)
        K.add(pg)
        self.at("positive charge")
        self.play(pop(pg, 1.25), run_time=0.5)
        fK = T("farnesyl", 26, ORANGE).next_to(K.tails[0], LEFT, buff=0.15).set_y(band)
        self.at("carries", nth=1)
        relabel(self, K, "K-Ras4B", 26)
        self.play(FadeIn(fK, shift=RIGHT * 0.1), run_time=0.4)
        lys = T("lysines", 26, TEAL).move_to([5.5, band + 0.1, 0])
        lead = Line([4.78, band + 0.05, 0], [pg.centre[0] + 0.45, pg.centre[1] + 0.05, 0], color=TEAL, stroke_width=3)
        self.at("a run of")
        self.play(FadeIn(lys, shift=LEFT * 0.1), Create(lead), run_time=0.5)

        # they are drawn to the negative lipids of the inner face
        row = minus_row(pg.centre[0] - 0.3)
        lines = pulls(pg, k)
        self.at("Those lysines")
        self.play(pop(pg, 1.18), run_time=0.6)
        self.at("attracted to")
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in row], lag_ratio=0.04), Create(lines), run_time=1.2)
        neg = T("negative lipids", 26, PINK).move_to([0.0, -0.25, 0])
        up = Arrow([0, 0.1, 0], [0, mem_bot() - 0.05, 0], buff=0, color=PINK, stroke_width=5, tip_length=0.22)
        self.at("negative lipids")
        self.play(FadeIn(neg, shift=UP * 0.1), GrowArrow(up), run_time=0.6)
        self.play(*[Indicate(m, color=TEXT, scale_factor=1.3) for m in row[::2]], run_time=0.7)

        # hand over to the next scene: H-Ras is the two-chain protein, a plain one-chain protein joins it
        A = ras(-4.6, "Ras")
        self.outro(FadeOut(VGroup(h1, h2, fH, pH, fK, lys, lead, row, lines, neg, up, K)),
                   then=[H.animate.shift(RIGHT * 2.8)], after=[FadeIn(A)])


# ---------------------------------------------------------------------------------------------
class S04Multiply(Film):
    """free energies add, affinities multiply; one hook falls off when bumped, two hold."""

    def construct(self):
        use(1.6, 2.6)
        k = 1.6
        mem = membrane()
        A = ras(-4.6, "Ras")
        B = ras(-0.8, "H-Ras", size=26)
        c2 = new_chain(B)
        B.add(c2)
        self.add(mem, A, B)

        e1 = T("free energy:  first + second", 28, TEXT, t2c={"free energy:": GREY})
        e2 = T("affinity:  first × second", 28, TEXT, t2c={"affinity:": GREY})
        e1.move_to([1.3, 1.5, 0], aligned_edge=LEFT)
        e2.move_to([1.3, 0.85, 0], aligned_edge=LEFT)

        base_y, ymax = -2.7, 2.3
        axis = Line([1.5, base_y, 0], [1.5, base_y + ymax + 0.1, 0], color=GREY, stroke_width=3)
        floor = Line([1.5, base_y, 0], [6.0, base_y, 0], color=GREY, stroke_width=3)
        aff = T("affinity", 24, GREY).move_to([2.0, -0.05, 0])
        sbar = Rectangle(width=1.2, height=0.23, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                         fill_opacity=0.8).move_to([2.2, base_y + 0.115, 0])
        slab = T("one grip", 26, ORANGE).move_to([2.2, -3.1, 0])
        ghost = DashedVMobject(Rectangle(width=1.2, height=ymax).move_to([4.5, base_y + ymax / 2, 0]),
                               num_dashes=40).set_color(GREEN).set_stroke(width=3)
        klab = T("extra 1.4 kcal/mol", 26, GREY).move_to([4.6, -3.1, 0])
        tbar = Rectangle(width=1.2, height=ymax, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                         fill_opacity=0.7).move_to([4.5, base_y + ymax / 2, 0])
        tlab = T("about 10× tighter", 28, GREEN, weight=BOLD).move_to([4.5, -0.05, 0])

        self.at("free energies add")
        self.play(FadeIn(e1, shift=LEFT * 0.2), run_time=0.6)
        self.at("affinities multiply")
        self.play(FadeIn(e2, shift=LEFT * 0.2), run_time=0.6)
        self.at("Each extra")
        self.play(Create(axis), Create(floor), GrowFromEdge(sbar, DOWN), FadeIn(slab), FadeIn(aff), run_time=0.8)
        self.at("per mole")
        self.play(FadeIn(klab, shift=UP * 0.1), Create(ghost), run_time=0.7)
        self.at("makes binding")
        self.play(GrowFromEdge(tbar, DOWN), FadeOut(ghost), run_time=1.0)
        self.at("times tighter")
        self.play(FadeIn(tlab, shift=DOWN * 0.1), run_time=0.6)

        # two weak grips make one strong grip
        la = T("one grip", 26, ORANGE).next_to(A.body, DOWN, buff=0.25)
        lb = T("two grips", 26, ORANGE).next_to(B.body, DOWN, buff=0.25)
        self.at("two weak grips")
        self.play(FadeIn(la, shift=UP * 0.1), FadeIn(lb, shift=UP * 0.1), *[pop(t, 1.3) for t in B.tails], run_time=0.7)
        self.at("strong grip")
        self.play(Indicate(B.body, color=GREEN, scale_factor=1.04), *[pop(t, 1.3) for t in B.tails], run_time=0.8)
        self.at("Think of hooks")
        self.play(*[pop(t, 1.3) for t in A.tails + B.tails], run_time=0.8)
        self.at("One hook holds")
        self.play(pop(A.tails[0], 1.4), run_time=0.6)

        # one hook, bumped, lets go; two hooks hold
        arrows = VGroup(*[Arrow([x, -1.95, 0], [x, -1.0, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.28)
                          for x in (A.body.get_center()[0], B.body.get_center()[0])])
        bump = T("bump", 28, GREY).next_to(arrows[0], RIGHT, buff=0.15)
        self.at("someone bumps")
        self.play(FadeOut(la), FadeOut(lb), GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(bump), run_time=0.4)
        self.play(shake(A, 0.12, 3), shake(B, 0.12, 3), run_time=0.5)
        A.body.set_stroke(RED, 4)
        lose = T("lets go", 28, RED, weight=BOLD).move_to([A.body.get_center()[0], A.body.get_bottom()[1] - 1.5 - 0.4, 0])
        self.play(FadeOut(arrows), FadeOut(bump), A.animate.shift(DOWN * 1.5), FadeIn(lose, shift=UP * 0.1), run_time=0.8)
        self.at("two hooks hold")
        B.body.set_stroke(GREEN, 4)
        hold = T("holds", 28, GREEN, weight=BOLD).next_to(B.body, DOWN, buff=0.25)
        self.play(FadeIn(hold, shift=UP * 0.1), pop(B, 1.05), run_time=0.6)
        self.outro(FadeOut(VGroup(e1, e2, axis, floor, aff, sbar, slab, klab, tbar, tlab, lose, hold, A, B)))


# ---------------------------------------------------------------------------------------------
class S05Switch(Film):
    """the second signal is a handle: a phosphate beside the lysines cancels their pull and K-Ras4B lets go."""

    def construct(self):
        use(1.8, 2.6)
        k = 1.8
        mem = membrane()
        K = ras(0.0, "K-Ras4B", size=26)
        pg = new_patch(K)
        K.add(pg)
        row = minus_row(pg.centre[0] - 0.3, left=9, right=9)
        lines = pulls(pg, k)
        band = (mem_bot() + K.body.get_top()[1]) / 2
        low, high = -2.1, bound_y()
        self.add(mem)
        self.play(FadeIn(row), FadeIn(lines), FadeIn(K, shift=UP * 0.15), run_time=0.7)

        fK = T("farnesyl", 28, ORANGE).next_to(K.tails[0], LEFT, buff=0.2).set_y(band)
        lys = T("lysines", 28, TEAL).move_to([3.4, band, 0])
        lead = Line([2.7, band - 0.05, 0], [pg.centre[0] + 0.5 * k, pg.centre[1] + 0.05, 0], color=TEAL, stroke_width=3)
        self.at("handle for control")
        self.play(pop(pg, 1.2), FadeIn(fK, shift=RIGHT * 0.1), FadeIn(lys, shift=LEFT * 0.1), Create(lead), run_time=0.7)
        # remove the handle and the protein sags
        cross = VGroup(Line(pg.centre + [-0.55 * k, -0.3 * k, 0], pg.centre + [0.55 * k, 0.3 * k, 0], color=RED, stroke_width=7),
                       Line(pg.centre + [-0.55 * k, 0.3 * k, 0], pg.centre + [0.55 * k, -0.3 * k, 0], color=RED, stroke_width=7))
        self.at("remove it")
        self.play(Create(cross), run_time=0.4)
        self.at("drops off")
        self.play(K.animate.shift(DOWN * 0.3), FadeOut(lines), run_time=0.6)
        self.at("In")
        self.play(FadeOut(cross), K.animate.shift(UP * 0.3), FadeIn(lines), FadeOut(fK), FadeOut(lys), FadeOut(lead),
                  run_time=0.7)

        # protein kinase C puts a phosphate beside the lysines
        top = K.body.get_top()[1]
        tgt = np.array([pg.centre[0] + 0.36 * k + 0.55, top + 0.22 * k, 0])
        pkc = bchip("protein kinase C", PURPLE, 26).move_to([4.6, 0.3, 0])
        P = pbadge(k).move_to(pkc.get_left() + LEFT * 0.5)
        self.at("protein kinase")
        self.play(FadeIn(pkc, shift=LEFT * 0.3), FadeIn(P, shift=LEFT * 0.3), run_time=0.7)
        self.at("puts a phosphate")
        self.play(P.animate(path_arc=1.2).move_to(tgt), run_time=0.9)
        self.at("next to the")
        self.play(pop(P, 1.5), pop(pg, 1.15), run_time=0.7)
        self.remove(P)
        K.add(P)
        minuses = VGroup(minus(tgt + [0.7, 0.0, 0], 0.26 * k), minus(tgt + [1.2, 0.0, 0], 0.26 * k))
        self.at("The phosphate adds")
        self.play(pop(P, 1.4), run_time=0.5)
        self.at("negative charge")
        self.play(FadeOut(pkc), LaggedStart(*[FadeIn(m, scale=0.4) for m in minuses], lag_ratio=0.3), run_time=0.8)
        self.remove(minuses)
        K.add(minuses)
        self.at("positive patch")
        self.play(pop(pg, 1.2), run_time=0.6)

        # the pull weakens and K-Ras4B is released
        weaker = T("weaker pull", 28, RED).move_to([3.9, band + 0.1, 0])
        self.at("attraction to")
        self.play(FadeIn(weaker, shift=RIGHT * 0.1), lines.animate.set_stroke(opacity=0.35), run_time=0.7)
        self.at("weakens")
        self.play(FadeOut(lines), run_time=0.5)
        K.body.set_stroke(RED, 4)
        self.at("is released")
        rel = T("released", 30, RED, weight=BOLD).move_to([K.body.get_right()[0] + 0.5 + 0.8, K.body.get_center()[1] - (high - low), 0])
        self.play(FadeOut(weaker), K.animate.shift(DOWN * (high - low)), FadeIn(rel, shift=LEFT * 0.1), run_time=1.1)
        sw = bchip("farnesyl-electrostatic switch", TEXT, 30).move_to([3.4, 0.7, 0])
        self.at("This is called")
        self.play(FadeIn(sw, shift=UP * 0.15), run_time=0.7)
        self.outro(FadeOut(VGroup(sw, rel, row, K)))


# ---------------------------------------------------------------------------------------------
class S06Palmitate(Film):
    """palmitate is the one chain that can be put on and taken off; the whole rule replayed on one protein."""

    def construct(self):
        use(1.8, 2.6)
        k = 1.8
        mem = membrane()
        H = ras(0.0, "H-Ras", size=26)
        c2 = new_chain(H)
        H.add(c2)
        self.add(mem)
        self.play(FadeIn(H, shift=UP * 0.15), run_time=0.6)
        top = H.body.get_top()[1]
        band = (mem_bot() + top) / 2
        x2 = c2.get_center()[0]
        low, high = -2.1, bound_y()
        fH = T("farnesyl", 28, ORANGE).next_to(H.tails[0], LEFT, buff=0.2).set_y(band)
        pH = T("palmitate", 28, ORANGE).next_to(c2, RIGHT, buff=0.2).set_y(band)

        self.at("second fatty chain")
        self.play(Indicate(c2, color=TEXT, scale_factor=1.2), FadeIn(fH, shift=RIGHT * 0.1), FadeIn(pH, shift=LEFT * 0.1),
                  run_time=0.8)

        # the bond that joins palmitate is easily cut
        joint = np.array([x2, top, 0])
        ring = DashedVMobject(Circle(radius=0.48).move_to(joint), num_dashes=20).set_color(RED).set_stroke(width=5)
        bond = T("easily cut bond", 28, RED).move_to([4.3, 0.55, 0])
        blead = Line([2.55, 0.6, 0], joint + [0.38, -0.05, 0], color=RED, stroke_width=3)
        self.at("joined by")
        self.play(Indicate(c2, color=TEXT, scale_factor=1.15), run_time=0.5)
        self.at("easily cut")
        self.play(Create(ring), FadeIn(bond, shift=LEFT * 0.1), Create(blead), run_time=0.8)

        # thioesterases cut it
        thio = bchip("thioesterase", PURPLE, 28).move_to([4.3, -0.55, 0])
        self.at("Enzymes called")
        self.play(FadeIn(thio, shift=LEFT * 0.3), run_time=0.6)
        cut = Line(joint + [-0.45, 0.35, 0], joint + [0.45, -0.35, 0], color=RED, stroke_width=8)
        gh = slot(x2, top, k)
        self.at("cut that bond")
        self.play(Create(cut), run_time=0.3)
        H.remove(c2)
        self.add(c2)
        self.play(c2.animate.shift(RIGHT * 0.9).set_opacity(0), FadeIn(gh), FadeOut(thio), FadeOut(cut), FadeOut(bond),
                  FadeOut(blead), FadeOut(ring), run_time=0.7)
        self.remove(c2)
        c2.shift(LEFT * 0.9).set_opacity(1)

        # put on and take off
        self.at("so palmitate")
        self.play(pop(pH, 1.2), pop(gh, 1.2), run_time=0.5)
        on = T("put on", 30, GREEN, weight=BOLD).move_to([4.4, band, 0])
        off = T("take off", 30, RED, weight=BOLD).move_to([4.4, band, 0])
        self.at("put on")
        self.play(FadeIn(on, shift=UP * 0.1), FadeIn(c2, shift=LEFT * 0.4), FadeOut(gh), run_time=0.6)
        self.at("take off")
        self.play(FadeOut(on), FadeIn(off, shift=UP * 0.1), FadeOut(c2, shift=RIGHT * 0.4), FadeIn(gh), run_time=0.6)

        # without it the grip weakens and H-Ras drifts away
        self.at("Once it is gone")
        self.play(FadeOut(off), FadeOut(pH), pop(gh, 1.2), run_time=0.6)
        self.at("grip weakens")
        self.play(shake(H, 0.1, 3), run_time=0.7)
        H.body.set_stroke(RED, 4)
        self.at("drifts away")
        self.play(H.animate.shift(LEFT * 3.4 + DOWN * (high - low)), FadeOut(gh), FadeOut(fH), run_time=1.3)
        H.body.set_stroke(BLUE, 3)

        # the rule, acted out on the same protein
        r1 = T("one chain visits", 36, ORANGE, weight=BOLD)
        r2 = T("a second signal holds", 36, GREEN, weight=BOLD)
        r3 = T("removing it releases", 36, RED, weight=BOLD)
        VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.0, 0.3, 0])
        rise = high - low
        self.at("one chain visits")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), H.animate.shift(UP * rise), run_time=0.8)
        self.play(H.animate.shift(DOWN * rise), run_time=0.8)
        # a second chain is put on, and the protein stays
        c3 = chain_at(H.body.get_center()[0] + 0.55 * k, H.body.get_top()[1], k)
        self.at("a second signal")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), GrowFromEdge(c3, DOWN), run_time=0.6)
        self.remove(c3)
        H.add(c3)
        H.body.set_stroke(GREEN, 4)
        self.play(H.animate.shift(UP * rise), run_time=0.8)
        self.at("removing that signal")
        H.remove(c3)
        self.add(c3)
        H.body.set_stroke(RED, 4)
        self.play(FadeIn(r3, shift=RIGHT * 0.2), FadeOut(c3, shift=RIGHT * 0.3), run_time=0.5)
        self.play(H.animate.shift(DOWN * rise), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "One chain visits. A second signal holds. Removing it releases the protein."
