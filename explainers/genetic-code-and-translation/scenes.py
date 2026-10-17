"""The genetic code and translation: one base moves the reading frame  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  TEXT   = bases of the message being read (letters inside a codon box)
  BLUE   = a codon box / a codon read in the right frame (triplet words that are the original words)
  GREEN  = an amino acid in the protein chain
  YELLOW = the base that is changed, added or removed
  RED    = a stop, or a triplet word that is wrong after a frame shift
  GREY   = bases not read (before the start codon, after the stop), notes, unknown "?" answers
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORIG = "GCCAUGGCUUGGAAACCUGACUAGCC"
W = 0.44
N = 27
X0 = -(N * W) / 2 + W / 2
YS = 1.3      # the strip
YC = -0.2     # the amino acid chips
YG = -1.7     # the "before" ghost row
YL = -2.9     # bottom label
FS = 40


def sx(i):
    return X0 + i * W


def L(ch, i, color=TEXT, y=YS, size=FS):
    return M(ch, size, color).move_to([sx(i), y, 0])


def cbox(k, color=BLUE, op=0.1):
    return RoundedRectangle(corner_radius=0.1, width=3 * W - 0.05, height=1.0, stroke_color=color,
                            stroke_width=2.5, fill_color=color, fill_opacity=op).move_to([sx(4 + 3 * k), YS, 0])


def aa(name, k, y=YC):
    color = RED if name == "stop" else (GREY if name == "?" else GREEN)
    return chip(name, color, size=30, pad=0.17).move_to([sx(4 + 3 * k), y, 0])


def tie(k):
    return Line([sx(4 + 3 * k), YS - 0.5, 0], [sx(4 + 3 * k), YC + 0.45, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)


def base_letters(unread=(0, 1, 2, 24, 25)):
    return [L(c, i, GREY if i in unread else TEXT) for i, c in enumerate(ORIG)]


CHAIN = ["Met", "Ala", "Trp", "Lys", "Pro", "Asp", "stop"]


class S00Title(TitleCard):
    LESSON = "The Genetic Code and Translation"
    TITLE = "One Base Moves the Reading Frame"


# ---------------------------------------------------------------------------------------------
class S01Surprise(SpokenScene):
    def construct(self):
        letters = base_letters(unread=())
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in letters], lag_ratio=0.03), run_time=0.9)

        def row(label, y):
            c = chip(label, YELLOW, size=34)
            a = Arrow(LEFT * 0.6, RIGHT * 0.6, color=GREY, stroke_width=5, buff=0)
            q = T("protein ?", 40, GREEN)
            return VGroup(c, a, q).arrange(RIGHT, buff=0.45).move_to([0, y, 0])

        self.at("in a gene")
        new = L("C", 8, YELLOW)
        rowa = row("one base changed", 0.0)
        self.play(Transform(letters[8], new), FadeIn(rowa, shift=RIGHT * 0.3), run_time=0.7)

        self.at("Add one base")
        g = L("G", 6, YELLOW, y=YS + 1.0)
        rowb = row("one base added", -1.5)
        self.play(Transform(letters[8], L("U", 8)), FadeIn(g, shift=DOWN * 0.3), run_time=0.5)
        self.play(g.animate.move_to([sx(6), YS, 0]),
                  *[l.animate.shift(RIGHT * W) for l in letters[6:]], FadeIn(rowb, shift=RIGHT * 0.3), run_time=0.7)

        self.at("one rule")
        self.play(FadeOut(g), *[l.animate.shift(LEFT * W) for l in letters[6:]],
                  FadeOut(rowa), FadeOut(rowb), run_time=0.7)
        self.at("four bases")
        lab = T("messenger RNA", 36, GREY).move_to([0, YS + 1.1, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Triplets(SpokenScene):
    def construct(self):
        def grid(n, color, x, y, sp=0.45):
            dots = VGroup(*[Dot(radius=0.13, color=color).move_to([(i - (n - 1) / 2) * sp, ((n - 1) / 2 - j) * sp, 0])
                            for j in range(n) for i in range(n)])
            return dots.move_to([x, y, 0])

        gl = grid(4, GREY, -4.2, 0.1)
        gr = grid(8, BLUE, 4.0, 0.1)
        ll = T("pairs: 16", 38, GREY).next_to(gl, UP, buff=0.5)
        lr = T("triplets: 64", 38, BLUE).next_to(gr, UP, buff=0.5)
        need = T("20 amino acids", 38, GREEN).move_to([0, 0.1, 0])
        self.at("Pairs of bases")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in gl], lag_ratio=0.03), FadeIn(ll), run_time=0.8)
        self.at("too few")
        toofew = T("too few", 34, RED).next_to(gl, DOWN, buff=0.5)
        self.play(FadeIn(toofew), run_time=0.3)
        self.at("20 amino acids")
        self.play(FadeIn(need, scale=0.9), run_time=0.4)
        self.at("Triplets give")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in gr], lag_ratio=0.01), FadeIn(lr), run_time=1.0)
        self.at("more than enough")
        enough = T("more than enough", 34, BLUE).next_to(gr, DOWN, buff=0.5)
        self.play(FadeIn(enough), run_time=0.3)

        self.at("A codon")
        letters = base_letters(unread=())
        self.play(FadeOut(VGroup(gl, gr, ll, lr, need, toofew, enough)),
                  LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in letters], lag_ratio=0.03), run_time=1.0)
        self.at("three bases")
        boxes = [cbox(k) for k in range(7)]
        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3),
                  *[letters[i].animate.set_color(GREY) for i in (0, 1, 2, 24, 25)], run_time=2.0)
        self.at("Of the")
        cnt = VGroup(T("61 amino acids", 38, GREEN), T("+", 38, GREY), T("3 stop", 38, RED)).arrange(RIGHT, buff=0.35)
        cnt.move_to([0, -1.2, 0])
        self.play(FadeIn(cnt, shift=UP * 0.15), run_time=0.5)
        self.at("stand for")
        self.play(Indicate(cnt[0], color=GREEN, scale_factor=1.15), run_time=0.6)
        self.at("and 3")
        self.play(Indicate(cnt[2], color=RED, scale_factor=1.15), run_time=0.6)
        self.at("usually starts")
        self.play(*[letters[i].animate.set_color(YELLOW) for i in (3, 4, 5)], Indicate(boxes[0], color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("runs on")
        self.play(*[letters[i].animate.set_color(TEXT) for i in (3, 4, 5)],
                  LaggedStart(*[Indicate(b, color=BLUE, scale_factor=1.1) for b in boxes], lag_ratio=0.25), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lookup(SpokenScene):
    def construct(self):
        letters = base_letters()
        boxes = [cbox(k) for k in range(7)]
        self.add(*letters, *boxes)
        self.at("looked up")
        head = T("look up each codon in the genetic code", 36, GREY).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.5)
        chips, ties = [], []
        for name, cue in zip(CHAIN, ["methionine", "alanine", "tryptophan", "lysine", "proline", "aspartate", "a stop"]):
            k = len(chips)
            self.at(cue)
            c = aa(name, k)
            t = tie(k)
            anims = [Create(t), FadeIn(c, shift=DOWN * 0.25)]
            if name == "stop":
                anims += [boxes[k].animate.set_stroke(RED).set_fill(RED, 0.15)]
            else:
                anims += [Indicate(boxes[k], color=BLUE, scale_factor=1.1)]
            self.play(*anims, run_time=0.6)
            chips.append(c); ties.append(t)
        self.at("adds no amino acid")
        self.play(Indicate(chips[6], color=RED), run_time=0.5)
        self.at("six residues")
        br = Brace(VGroup(*chips[:6]), DOWN, color=GREEN, buff=0.15)
        lab = T("6 residues", 40, GREEN).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(lab), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04OneBase(SpokenScene):
    def construct(self):
        letters = base_letters()
        boxes = [cbox(k) for k in range(7)]
        boxes[6].set_stroke(RED).set_fill(RED, 0.15)
        chips = [aa(n, k) for k, n in enumerate(CHAIN)]
        ties = [tie(k) for k in range(7)]
        self.add(*letters, *boxes, *chips, *ties)

        def q(k):
            return aa("?", k)

        label = None
        self.at("change one base")
        head = T("one base changed", 38, YELLOW).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.4)

        # ---- case 1: silent -------------------------------------------------------------
        self.at("First")
        self.play(Transform(letters[8], L("C", 8, YELLOW)), Transform(chips[1], q(1)), run_time=0.5)
        self.at("alanine")
        self.play(Transform(chips[1], aa("Ala", 1)), run_time=0.4)
        self.at("silent")
        lab = T("silent: the protein is the same", 44).move_to([0, -1.9, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)

        # ---- case 2: missense ------------------------------------------------------------
        self.at("Second")
        self.play(Transform(letters[8], L("U", 8)), Transform(letters[6], L("A", 6, YELLOW)),
                  Transform(chips[1], q(1)), FadeOut(lab), run_time=0.5)
        self.at("threonine")
        self.play(Transform(chips[1], aa("Thr", 1)), run_time=0.4)
        self.at("missense")
        lab = T("missense: Ala to Thr", 44).move_to([0, -1.9, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)

        # ---- case 3: nonsense ------------------------------------------------------------
        self.at("Third")
        self.play(Transform(letters[6], L("G", 6)), Transform(letters[11], L("A", 11, YELLOW)),
                  Transform(chips[1], aa("Ala", 1)), Transform(chips[2], q(2)), FadeOut(lab), run_time=0.5)
        self.at("is a stop")
        self.play(Transform(chips[2], aa("stop", 2)), boxes[2].animate.set_stroke(RED).set_fill(RED, 0.15),
                  *[FadeOut(c) for c in chips[3:]], *[FadeOut(t) for t in ties[3:]],
                  *[boxes[k].animate.set_stroke(GREY, opacity=0.5).set_fill(GREY, 0.04) for k in range(3, 7)],
                  *[letters[i].animate.set_color(GREY) for i in range(15, 24)], run_time=0.5)
        self.at("nonsense")
        lab = T("nonsense: the chain ends early", 44).move_to([0, -1.9, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Insert(SpokenScene):
    def construct(self):
        letters = base_letters()
        boxes = [cbox(k) for k in range(7)]
        boxes[6].set_stroke(RED).set_fill(RED, 0.15)
        chips = [aa(n, k) for k, n in enumerate(CHAIN)]
        ties = [tie(k) for k in range(7)]
        self.add(*letters, *boxes, *chips, *ties)

        self.at("add one base")
        g = L("G", 6, YELLOW, y=YS + 1.0)
        self.play(FadeIn(g, shift=DOWN * 0.3), run_time=0.5)
        self.at("right after")
        ghost = VGroup(*[aa(n, k, y=YC).scale(0.85).set_opacity(0.55) for k, n in enumerate(CHAIN)])
        before = T("before", 26, GREY).move_to([-5.2, YC, 0])
        after = T("after", 26, GREEN).move_to([-5.2, YC, 0])
        self.add(ghost)
        self.play(ghost.animate.shift(DOWN * (YC - YG)), FadeIn(before.move_to([-5.2, YG, 0])),
                  FadeIn(after),
                  g.animate.move_to([sx(6), YS, 0]), *[l.animate.shift(RIGHT * W) for l in letters[6:]],
                  *[Transform(chips[k], aa("?", k)) for k in range(1, 6)], FadeOut(chips[6]), FadeOut(ties[6]),
                  boxes[6].animate.set_stroke(BLUE).set_fill(BLUE, 0.1), run_time=0.9)
        self.at("stays")
        self.play(Indicate(VGroup(letters[3], letters[4], letters[5], boxes[0]), color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("slides along")
        self.play(Indicate(VGroup(*letters[6:]), color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("regroup")
        self.play(*[Indicate(boxes[k], color=BLUE, scale_factor=1.08) for k in range(1, 6)], run_time=0.6)
        self.at("methionine")
        self.play(Indicate(chips[0], color=GREEN), run_time=0.4)
        for name, k, cue in [("Gly", 1, "glycine"), ("Leu", 2, "leucine"), ("Glu", 3, "glutamate"), ("Thr", 4, "threonine")]:
            self.at(cue)
            self.play(Transform(chips[k], aa(name, k)), run_time=0.35)
        self.at("a stop")
        self.play(Transform(chips[5], aa("stop", 5)), boxes[5].animate.set_stroke(RED).set_fill(RED, 0.15),
                  boxes[6].animate.set_stroke(GREY, opacity=0.5).set_fill(GREY, 0.04),
                  *[letters[i].animate.set_color(GREY) for i in range(21, 26)], run_time=0.6)
        self.at("early")
        lab = T("frameshift: every codon after it changes", 40).move_to([0, YL, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
        self.at("shorter")
        lab2 = T("frameshift: 5 residues, not 6", 40, YELLOW).move_to([0, YL, 0])
        self.play(Transform(lab, lab2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
SENT = "THEFATCATATETHERAT"
WORDS = {"THE", "FAT", "CAT", "ATE", "RAT"}
W6 = 0.42
M6 = 21


def rx(i):
    return -(M6 * W6) / 2 + W6 / 2 + i * W6


class Row:
    def __init__(self, y, nbox):
        self.y = y
        self.mobs = {}
        self.boxes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=3 * W6 - 0.05, height=0.75, stroke_color=BLUE,
                                               stroke_width=2, fill_color=BLUE, fill_opacity=0.07)
                              .move_to([rx(3 * j + 1), y, 0]) for j in range(nbox)])
        self.nbox = nbox

    def colors(self, seq):
        cols = []
        for i, (idn, ch) in enumerate(seq):
            if str(idn).startswith("q"):
                cols.append(YELLOW)
            elif i >= 3 * self.nbox:
                cols.append(GREY)
            else:
                w = "".join(c for _, c in seq[(i // 3) * 3:(i // 3) * 3 + 3])
                cols.append(BLUE if w in WORDS else RED)
        return cols

    def anims(self, seq):
        out = []
        ids = {s[0] for s in seq}
        for idn in list(self.mobs):
            if idn not in ids:
                out.append(FadeOut(self.mobs.pop(idn)))
        cols = self.colors(seq)
        for i, (idn, ch) in enumerate(seq):
            tgt = [rx(i), self.y, 0]
            if idn in self.mobs:
                out.append(self.mobs[idn].animate.move_to(tgt).set_color(cols[i]))
            else:
                m = M(ch, FS, cols[i]).move_to(tgt)
                self.mobs[idn] = m
                out.append(FadeIn(m, shift=DOWN * 0.35))
        return out


def orig_seq():
    return [(i, c) for i, c in enumerate(SENT)]


def with_q(seq, after_ids, names):
    out = []
    for idn, ch in seq:
        out.append((idn, ch))
        if idn in after_ids:
            out.append((names[after_ids.index(idn)], "Q"))
    return out


class S06PlusMinus(SpokenScene):
    def construct(self):
        y1, y2, y3 = 1.8, 0.3, -1.2
        r1, r2, r3 = Row(y1, 6), Row(y2, 6), Row(y3, 7)

        def tag(text, y, color, left=True):
            t = T(text, 28, color)
            x = rx(0) - 0.2 + t.width / 2 if left else 4.6 - t.width / 2
            return t.move_to([x, y + 0.68, 0])

        self.at("Picture")
        head = T("a sentence of three-letter words", 34, GREY).move_to([0, 3.2, 0])
        s0 = orig_seq()
        self.play(FadeIn(head), FadeIn(r1.boxes), *r1.anims(s0), run_time=0.9)

        self.at("plus with a nearby")
        s1 = with_q(s0, [2], ["q1"])
        t1 = tag("+ : one kind of change", y1, YELLOW)
        self.play(FadeIn(t1), *r1.anims(s1), run_time=0.9)
        self.at("nearby minus")
        self.play(Indicate(r1.mobs[5], color=YELLOW, scale_factor=1.4), run_time=0.5)
        s2 = [s for s in s1 if s[0] != 5]
        t1b = tag("+ and \u2212: opposite kinds of change", y1, YELLOW)
        self.play(Transform(t1, t1b), *r1.anims(s2), run_time=0.9)
        self.at("restored function")
        res1 = tag("often restored", y1, BLUE, left=False)
        self.play(FadeIn(res1, shift=LEFT * 0.2), run_time=0.5)

        self.at("Two pluses")
        t2 = tag("two +", y2, YELLOW)
        self.play(FadeIn(r2.boxes), FadeIn(t2), *r2.anims(s0), run_time=0.3)
        self.play(*r2.anims(with_q(s0, [2, 4], ["q1", "q2"])), run_time=0.45)
        self.at("did not")
        res2 = tag("not restored", y2, RED, left=False)
        self.play(FadeIn(res2, shift=LEFT * 0.2), run_time=0.5)

        self.at("three pluses")
        t3 = tag("three +", y3, YELLOW)
        self.play(FadeIn(r3.boxes[:6]), FadeIn(t3), *r3.anims(s0), run_time=0.3)
        s3 = with_q(s0, [2, 5, 8], ["q1", "q2", "q3"])
        self.play(FadeIn(r3.boxes[6]), *r3.anims(s3), run_time=0.6)
        self.at("wild or nearly wild")
        res3 = tag("wild or nearly wild, as tested", y3, BLUE, left=False)
        self.play(FadeIn(res3, shift=LEFT * 0.2), run_time=0.5)

        self.at("Keep this rule")
        f1 = T("one base more or less moves the frame", 36, YELLOW).move_to([0, -2.6, 0])
        self.play(FadeIn(f1, shift=UP * 0.15), run_time=0.6)
        self.at("frame sets every")
        f2 = T("and the frame sets every codon", 32).move_to([0, -3.2, 0])
        self.play(FadeIn(f2, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "One base more or less moves the frame."
