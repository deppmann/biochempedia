"""Block one anchor, Ras finds another: the farnesyltransferase inhibitor story  (section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film; the same as the lesson's opening film)
  BLUE   = the protein (Ras)
  ORANGE = a fatty chain on the protein (farnesyl, geranylgeranyl): the lipid anchor
  PURPLE = an enzyme (farnesyltransferase, geranylgeranyltransferase I)
  RED    = the drug, blocked, cannot, disappointed
  GREEN  = anchored at the membrane, signaling, worked
  YELLOW = the Phase III badge
  GREY   = the membrane, labels, the cysteine mark
No molecular structures: a protein is a labelled blob, a chain is a plain capsule, the drug a chip.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"

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


def membrane():
    return RoundedRectangle(corner_radius=0.1, width=12.6, height=MEM_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, my(), 0])


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



# ---------------------------------------------------------------------------------------------
# helpers for this film
# ---------------------------------------------------------------------------------------------
DRUG = TEAL


def chipn(lines, color, size=24, pad=0.2):
    """a bchip that may hold two lines of text."""
    c = chip(lines, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def blocker(a, b, color=RED, w=6):
    """a bar that stops an arrow, from a toward b (the bar sits at b)."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 2))


def cross(c, s=0.34, color=RED, w=8):
    c = np.array(c, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def tick(c, s=0.3, color=GREEN, w=8):
    c = np.array(c, float)
    return VGroup(Line(c + [-s, 0.02, 0], c + [-s * 0.3, -s * 0.8, 0], color=color, stroke_width=w),
                  Line(c + [-s * 0.3, -s * 0.8, 0], c + [s, s * 0.9, 0], color=color, stroke_width=w))


def long_chain(x, body_top, k, color=ORANGE, mult=1.5):
    """a geranylgeranyl chain: the same capsule as the farnesyl one, drawn longer (not to scale)."""
    w, h = 0.24 * k, 1.0 * k * mult
    return RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.9).move_to([x, body_top - 0.05 * k + h / 2, 0])


def ring(c, r=0.13, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_opacity=0).move_to(c)


class S00Title(TitleCard):
    LESSON = "Lipids as Anchors and Addresses"
    TITLE = "Block one anchor, Ras finds another"


# ---------------------------------------------------------------------------------------------
class S01Block(Film):
    """a drug blocks the enzyme that puts farnesyl on Ras; a Ras with no chain stays off the membrane."""

    def construct(self):
        use(1.6, 2.9)
        k = 1.6
        mem = membrane()
        A = ras(-3.9, "Ras")                                     # held on the membrane by its farnesyl chain
        self.play(FadeIn(mem), FadeIn(A, shift=UP * 0.2), run_time=0.6)
        topA = A.body.get_top()[1]
        fa = T("farnesyl", 28, ORANGE).next_to(A.tails[0], LEFT, buff=0.2).set_y((mem_bot() + topA) / 2)

        self.at("chain to work")
        self.play(FadeIn(fa, shift=RIGHT * 0.1), Indicate(A.tails[0], color=TEXT, scale_factor=1.2), run_time=0.7)

        # a second Ras, still without its chain, and the enzyme that would attach one
        B = ras(2.9, "Ras", y=-0.7, chain=False)
        topB = B.body.get_top()[1]
        sx = 2.9 - 0.55 * k
        sl = slot(sx, topB, k)
        enz = bchip("enzyme", PURPLE, 26).move_to([-0.2, topB + 0.15, 0])
        link = DashedLine(enz.get_right(), [sx - 0.15, topB + 0.1, 0], color=PURPLE, stroke_width=4, dash_length=0.1)
        self.at("block the enzyme")
        self.play(FadeIn(B, shift=UP * 0.2), FadeIn(sl), FadeIn(enz, shift=RIGHT * 0.2), Create(link), run_time=0.8)

        drug = bchip("inhibitor", DRUG, 28).move_to([-0.2, 1.5, 0])
        stop = blocker(drug.get_bottom() + DOWN * 0.04, enz.get_top() + UP * 0.04)
        self.at("that attaches")
        self.play(FadeIn(drug, shift=DOWN * 0.15), Create(stop), run_time=0.6)
        xl = cross((link.get_start() + link.get_end()) / 2)
        self.play(Create(xl), enz.animate.set_opacity(0.8), link.animate.set_opacity(0.4), run_time=0.5)
        self.at("idea behind")
        self.play(pop(drug, 1.15), run_time=0.6)

        # roughly one in five human cancers carry a mutated Ras gene
        tiles = VGroup(*[Square(0.5, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([-5.7 + 0.7 * j, -3.0, 0])
                         for j in range(5)])
        self.at("Ras genes")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.15), run_time=0.9)
        lab = T("roughly 1 in 5 human cancers", 28, TEXT).move_to([-0.4, -2.85, 0]).align_to([-2.0, 0, 0], LEFT)
        self.at("human cancers")
        self.play(tiles[0].animate.set_fill(BLUE, 0.9).set_stroke(BLUE), FadeIn(lab, shift=LEFT * 0.1), run_time=0.7)
        lab2 = T("Ras gene mutated", 26, BLUE).next_to(lab, DOWN, buff=0.12).align_to(lab, LEFT)
        self.play(FadeIn(lab2), run_time=0.4)

        # a Ras with no chain stays off the membrane
        up = DashedLine([2.9, topB + 0.2, 0], [2.9, mem_bot() - 0.15, 0], color=GREY, stroke_width=4, dash_length=0.14)
        xu = cross([2.9, (topB + mem_bot()) / 2 + 0.3, 0], 0.3)
        self.at("cannot reach")
        self.play(Create(up), run_time=0.5)
        self.play(Create(xu), run_time=0.4)
        no = T("cannot signal", 30, RED, weight=BOLD).move_to([2.9, -2.1, 0])
        self.at("cannot signal")
        self.play(FadeIn(no, shift=UP * 0.1), run_time=0.5)
        self.outro(FadeOut(VGroup(mem, A, fa, B, sl, enz, link, xl, drug, stop, tiles, lab, lab2, up, xu, no)))


# ---------------------------------------------------------------------------------------------
class S02Ranking(Film):
    """the drugs (a class) worked as drugs yet disappointed against K-Ras, the most mutated Ras; N-Ras is not ranked."""

    def construct(self):
        cls = bchip("farnesyltransferase inhibitors", DRUG, 36, pad=0.26).move_to([0, 2.95, 0])
        drug = bchip("tipifarnib", DRUG, 36, pad=0.26).move_to([-2.4, 1.6, 0])
        phase = bchip("Phase III trials", YELLOW, 32, pad=0.22).move_to([2.6, 1.6, 0])
        one = T("one of these drugs", 26, GREY).move_to([-2.4, 0.85, 0])
        self.at("One of these")
        self.play(FadeIn(cls, scale=0.85), run_time=0.5)
        self.at("these drugs")
        self.play(FadeIn(drug, shift=UP * 0.15), FadeIn(one), run_time=0.6)
        self.at("reached Phase")
        self.play(FadeIn(phase, shift=LEFT * 0.2), run_time=0.6)

        pre = T("the drugs", 32, DRUG, weight=BOLD)
        ok = VGroup(pre, tick([0, 0, 0], 0.24), T("worked as drugs", 32, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to([0, 0.15, 0])
        self.at("worked as drugs")
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.6)
        pre2 = T("the drugs", 28, DRUG, weight=BOLD)
        bad = VGroup(pre2, cross([0, 0, 0], 0.22, RED, 7), T("disappointed against the Ras that matters most", 28, RED, weight=BOLD)
                     ).arrange(RIGHT, buff=0.28).move_to([0, 0.15, 0])
        self.at("disappointed")
        self.play(ReplacementTransform(ok, bad), run_time=0.7)

        def blob(name, w, h, size, color=BLUE):
            r = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=3,
                                 fill_color=color, fill_opacity=0.25)
            return VGroup(r, T(name, size, color, weight=BOLD).move_to(r))
        K = blob("K-Ras", 3.4, 1.8, 42).move_to([-4.0, -1.35, 0])
        N = blob("N-Ras", 2.2, 1.2, 30, GREY).move_to([0.0, -1.35, 0])
        H = blob("H-Ras", 2.0, 1.0, 28).move_to([4.0, -1.35, 0])
        q = VGroup(RoundedRectangle(corner_radius=0.3, width=3.4, height=1.8, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.12).move_to(K),
                   T("?", 56, TEXT, weight=BOLD).move_to(K))
        self.at("matters most")
        self.play(FadeIn(q, scale=0.8), run_time=0.5)
        self.at("by far")
        self.play(ReplacementTransform(q, K), run_time=0.6)
        most = T("by far the most\ncommonly mutated", 28, TEXT, line_spacing=0.8).move_to([-4.0, -2.95, 0])
        self.at("most commonly mutated")
        self.play(FadeIn(most, shift=UP * 0.1), run_time=0.5)
        unr = T("not ranked here", 24, GREY).move_to([0.6, -2.3, 0])
        self.at("three Ras genes")
        self.play(FadeIn(N, shift=LEFT * 0.2), FadeIn(H, shift=LEFT * 0.2), FadeIn(unr), run_time=0.7)
        least = T("the least", 28, TEXT).move_to([4.0, -2.5, 0])
        self.at("is the least")
        self.play(pop(H, 1.2), FadeIn(least, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(T("not to scale", 22, GREY).move_to([4.0, -3.0, 0])), run_time=0.4)
        self.outro(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------------------------
class S03Catch(Film):
    """with farnesylation blocked, a second enzyme puts a geranylgeranyl group on the same cysteine of K-Ras and N-Ras."""

    def construct(self):
        use(1.6, 3.0)
        k = 1.6
        mem = membrane()
        K = ras(-4.0, "K-Ras", y=-1.0, chain=False, size=28)
        N = ras(4.0, "N-Ras", y=-1.0, chain=False, size=28)
        top = K.body.get_top()[1]
        self.play(FadeIn(mem), FadeIn(K, shift=UP * 0.2), FadeIn(N, shift=UP * 0.2), run_time=0.7)

        ft = chipn("farnesyl-\ntransferase", PURPLE, 26).move_to([0, 1.7, 0])
        drug = bchip("inhibitor", DRUG, 26).move_to([0, 0.35, 0])
        stop = blocker(drug.get_top() + UP * 0.04, ft.get_bottom() + DOWN * 0.04)
        self.at("farnesylation is blocked")
        self.play(FadeIn(ft), FadeIn(drug, shift=UP * 0.15), run_time=0.5)
        self.play(Create(stop), ft.animate.set_opacity(0.55), run_time=0.5)
        self.at("can be picked up")
        self.play(pop(K, 1.06), pop(N, 1.06), run_time=0.7)

        # a second enzyme
        gg = chipn("geranylgeranyl-\ntransferase I", PURPLE, 26).move_to([0, 0.3, 0])
        sxk, sxn = -4.0 + 0.55 * k, 4.0 - 0.55 * k           # the chains go on the sides facing the enzyme
        mid = top + 0.5
        lk = DashedLine(gg.get_left(), [sxk + 0.18, mid - 0.3, 0], color=PURPLE, stroke_width=4, dash_length=0.1)
        ln = DashedLine(gg.get_right(), [sxn - 0.18, mid - 0.3, 0], color=PURPLE, stroke_width=4, dash_length=0.1)
        self.at("second enzyme")
        self.play(FadeOut(VGroup(ft, drug, stop)), run_time=0.3)
        self.play(FadeIn(gg, scale=0.85), Create(lk), Create(ln), run_time=0.7)
        self.at("It is")
        self.play(pop(gg, 1.1), run_time=0.5)
        self.at("It puts")
        self.play(*[Flash(p, color=PURPLE, line_length=0.2, flash_radius=0.3, num_lines=8) for p in ([sxk + 0.1, mid - 0.3, 0], [sxn - 0.1, mid - 0.3, 0])], run_time=0.6)

        # a longer chain goes on
        ck = long_chain(sxk, top, k)
        cn = long_chain(sxn, top, k)
        gl = T("geranylgeranyl", 26, ORANGE).move_to([0, -1.55, 0])
        self.play(GrowFromEdge(ck, DOWN), GrowFromEdge(cn, DOWN), FadeIn(gl, shift=UP * 0.1), run_time=0.8)
        K.add(ck); N.add(cn)
        note = T("drawn longer, not to scale", 24, GREY).next_to(gl, DOWN, buff=0.12)
        self.at("a longer chain")
        self.play(FadeIn(note), pop(ck, 1.06), pop(cn, 1.06), run_time=0.5)

        # on the same cysteine
        rk, rn = ring([sxk, top, 0]), ring([sxn, top, 0])
        ck_lab = T("same cysteine", 26, GREY).move_to([-4.9, top + 0.75, 0])
        cn_lab = T("same cysteine", 26, GREY).move_to([4.9, top + 0.75, 0])
        lead_k = Line(rk.get_top() + UP * 0.02, ck_lab.get_right() + LEFT * 0.35 + DOWN * 0.15, color=GREY, stroke_width=3)
        lead_n = Line(rn.get_top() + UP * 0.02, cn_lab.get_left() + RIGHT * 0.35 + DOWN * 0.15, color=GREY, stroke_width=3)
        self.at("same cysteine")
        self.play(Create(rk), Create(rn), FadeIn(ck_lab), FadeIn(cn_lab), Create(lead_k), Create(lead_n), run_time=0.8)

        # the proteins keep an anchor and rise to the membrane
        rise = (mem_bot() + 0.2 - (top + 1.0 * k * 1.5 - 0.05 * k)) * -1
        K_all = VGroup(K, rk, ck_lab, lead_k)
        N_all = VGroup(N, rn, cn_lab, lead_n)
        self.at("keeps its anchor")
        self.play(FadeOut(VGroup(gg, lk, ln, gl, note)), run_time=0.3)
        shift = 3.0 - (top + 1.5 * k - 0.05 * k)           # chain top to the middle of the membrane
        self.play(K_all.animate.shift(UP * shift), N_all.animate.shift(UP * shift), run_time=1.0)
        self.at("keeps signaling")
        sig_k = T("signaling", 28, GREEN, weight=BOLD).move_to([-4.0, K.body.get_bottom()[1] - 0.4, 0])
        sig_n = T("signaling", 28, GREEN, weight=BOLD).move_to([4.0, N.body.get_bottom()[1] - 0.4, 0])
        self.play(K.body.animate.set_stroke(GREEN, 4), N.body.animate.set_stroke(GREEN, 4),
                  FadeIn(sig_k, shift=UP * 0.1), FadeIn(sig_n, shift=UP * 0.1), run_time=0.7)
        self.outro(FadeOut(Group(*self.mobjects)))


# ---------------------------------------------------------------------------------------------
class S04Hras(Film):
    """H-Ras is not rescued; tipifarnib is tested in mutant H-Ras cancers; the rule."""

    def construct(self):
        use(1.6, 3.0)
        k = 1.6
        mem = membrane()
        H = ras(-4.0, "H-Ras", y=-1.0, chain=False, size=28)
        top = H.body.get_top()[1]
        sx = -4.0 + 0.55 * k
        sl = slot(sx, top, k)
        gg = chipn("geranylgeranyl-\ntransferase I", PURPLE, 26).move_to([-0.2, 0.3, 0])
        self.add(mem, H, sl)
        self.at("H Ras is not")
        self.play(FadeIn(gg, shift=RIGHT * 0.2), run_time=0.5)
        link = DashedLine(gg.get_left(), [sx + 0.18, top + 0.2, 0], color=PURPLE, stroke_width=4, dash_length=0.1)
        self.play(Create(link), run_time=0.4)
        xl = cross((gg.get_left() + np.array([sx + 0.18, top + 0.2, 0])) / 2 + UP * 0.05)
        no = T("not rescued", 30, RED, weight=BOLD).move_to([-4.0, -2.45, 0])
        self.at("rescued this way")
        self.play(Create(xl), FadeIn(no, shift=UP * 0.1), gg.animate.set_opacity(0.5), link.animate.set_opacity(0.4), run_time=0.6)

        self.at("logic has not died")
        self.play(pop(H, 1.06), run_time=0.7)

        drug = bchip("tipifarnib", DRUG, 30).move_to([3.7, 1.7, 0])
        tgt = chipn("cancers driven by\nmutant H-Ras", BLUE, 28).move_to([3.7, -0.3, 0])
        arr_ = Arrow(drug.get_bottom(), tgt.get_top(), buff=0.08, color=DRUG, stroke_width=5, tip_length=0.22)
        tested = T("tested", 28, GREY).next_to(arr_, RIGHT, buff=0.2)
        self.at("has been tested")
        self.play(FadeIn(drug, shift=DOWN * 0.15), run_time=0.5)
        self.at("tested in")
        self.play(GrowArrow(arr_), FadeIn(tgt, shift=UP * 0.1), FadeIn(tested), run_time=0.7)

        # the rule
        r1 = T("Block farnesyl:", 40, TEXT, font=TITLE_FONT)
        r2 = T("K-Ras and N-Ras can switch anchors.", 36, GREEN, weight=BOLD)
        r3 = T("H-Ras cannot.", 36, RED, weight=BOLD)
        rule = VGroup(r1, r2, r3).arrange(DOWN, buff=0.4)
        self.at("keep this rule")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("can switch anchors")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.at("but H Ras cannot")
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "Block farnesyl: K-Ras and N-Ras can switch anchors; H-Ras cannot."
