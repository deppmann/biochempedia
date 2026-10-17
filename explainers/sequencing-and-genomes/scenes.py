"""Sequencing and genomes: depth cannot fix a repeat  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = the genome as a whole (a bar), axes, de-emphasized
  BLUE   = a short read
  YELLOW = a long read
  RED    = unread bases, gaps, the break, what cannot be placed
  ORANGE = the repeat
  TEAL   = unique flanking sequence next to a repeat
  GREEN  = resolved: a copy pinned to its flanks
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEAL_ = "#3FB8C0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def rect(x0, x1, y, h=0.3, color=GREY, op=0.35, sw=2.5):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=sw,
                     fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def read(x0, x1, y, color=BLUE, h=0.2):
    r = RoundedRectangle(corner_radius=0.07, width=max(x1 - x0, 0.15), height=h, stroke_color=color,
                         stroke_width=2, fill_color=color, fill_opacity=0.75)
    return r.move_to([(x0 + x1) / 2, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def xmark(c, color=RED, s=0.22, w=6):
    c = np.array(c, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


# the repeat map used in the last three scenes: flank A, repeat, flank B ... flank C, repeat, flank D
SEG = {"A": (-5.7, -3.9), "R1": (-3.9, -2.3), "B": (-2.3, -0.5),
       "C": (0.5, 2.3), "R2": (2.3, 3.9), "D": (3.9, 5.7)}
BAR_H = 0.9


def repeat_map(y):
    parts = {}
    for k, (x0, x1) in SEG.items():
        isr = k.startswith("R")
        col = ORANGE if isr else TEAL_
        blk = rect(x0, x1, y, BAR_H, col, 0.35)
        lab = T("repeat" if isr else k, 30, col).move_to(blk)
        parts[k] = VGroup(blk, lab)
    dots = T("· · ·", 30, GREY).move_to([0, y, 0])
    parts["dots"] = dots
    return parts


def mini(label, color, w=0.85):
    b = rect(0, w, 0, 0.6, color, 0.35)
    return VGroup(b, T(label, 28, color).move_to(b))


def hyp_row(seq, y):
    """seq like ['A','R','B','C','R','D'] -> two linked triplets."""
    items = []
    for s in seq:
        items.append(mini("repeat" if s == "R" else s, ORANGE if s == "R" else TEAL_, 1.35 if s == "R" else 0.8))
    g1 = VGroup(*items[:3]).arrange(RIGHT, buff=0.0)
    g2 = VGroup(*items[3:]).arrange(RIGHT, buff=0.0)
    row = VGroup(g1, g2).arrange(RIGHT, buff=1.2).move_to([0, y, 0])
    return row


class S00Title(TitleCard):
    LESSON = "Sequencing and Genomes"
    TITLE = "Depth cannot fix a repeat"


# ---------------------------------------------------------------------------------------------
class S01Pieces(SpokenScene):
    """two drafts / gapless -> one read is tiny against a chromosome -> pieces -> how to join?"""

    def construct(self):
        x0, x1 = -5.8, 5.8
        # 2001 draft: pieces with gaps
        cuts = [-5.8, -3.6, -3.4, -1.0, -0.7, 1.9, 2.2, 5.8]
        draft = VGroup()
        for a, b in zip(cuts[0::2], cuts[1::2]):
            pass
        segs = [(-5.8, -3.6), (-3.4, -1.0), (-0.7, 1.9), (2.2, 5.8)]
        draft = VGroup(*[rect(a, b, 2.2, 0.8, GREY, 0.4) for a, b in segs])
        gapmarks = VGroup(*[xmark([(b + c) / 2, 2.2, 0], RED, 0.22, 5) for (_, b), (c, _) in zip(segs[:-1], segs[1:])])
        lab1 = T("first drafts, with gaps", 28, GREY).next_to(draft, UP, buff=0.3).align_to(draft, LEFT)
        full = rect(x0, x1, -0.2, 0.8, GREY, 0.4)
        lab2 = T("no gaps, all but one chromosome", 28, GREY).next_to(full, UP, buff=0.3).align_to(full, LEFT)
        self.at("Two drafts")
        self.play(FadeIn(lab1), Create(draft), run_time=0.9)
        self.play(FadeIn(gapmarks), run_time=0.4)
        self.at("The first assembly")
        self.play(FadeIn(lab2), Create(full), run_time=0.9)
        q = T("why the wait?", 48, TEXT, weight=BOLD).move_to([0, -1.9, 0])
        self.at("so why the")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)

        # one pass cannot read a chromosome
        self.at("No instrument reads")
        chrom = rect(x0, x1, 1.0, 0.9, GREY, 0.4)
        chrom_lab = T("a chromosome", 28, GREY).next_to(chrom, UP, buff=0.3).align_to(chrom, LEFT)
        self.play(FadeOut(VGroup(draft, gapmarks, lab1, lab2, q)), ReplacementTransform(full, chrom),
                  FadeIn(chrom_lab), run_time=0.8)
        one = read(x0, x0 + 0.6, 1.0, BLUE, 0.9)
        one_lab = T("one read", 28, BLUE).next_to(one, DOWN, buff=0.45).align_to(one, LEFT)
        self.play(FadeIn(one, scale=0.8), FadeIn(one_lab), run_time=0.6)

        # pieces
        self.at("Every method reads pieces")
        rng = np.random.RandomState(4)
        pieces = VGroup()
        for i in range(12):
            a = x0 + i * (x1 - x0 - 0.7) / 11
            pieces.add(read(a, a + 0.7, 1.0, BLUE, 0.9))
        self.play(FadeOut(one_lab), ReplacementTransform(one, pieces[0]), FadeIn(pieces[1:]), run_time=0.6)
        self.wait(0.2)
        scat = []
        order = list(range(12))
        rng.shuffle(order)
        for k, p in enumerate(pieces):
            tx = -5.2 + order.index(k) * 0.95 + rng.uniform(-0.1, 0.1)
            ty = -1.6 + rng.uniform(-0.45, 0.45)
            scat.append(p.animate.move_to([tx, ty, 0]).rotate(rng.uniform(-0.5, 0.5)))
        self.play(*scat, chrom.animate.set_opacity(0.2), run_time=1.1)

        self.at("put back together")
        qm = T("?", 90, TEXT, weight=BOLD).move_to([0, -0.0, 0])
        up = arr([-2.5, -0.85, 0], [-2.5, 0.4, 0], GREY)
        up2 = arr([2.5, -0.85, 0], [2.5, 0.4, 0], GREY)
        self.play(FadeIn(qm, scale=0.8), GrowArrow(up), GrowArrow(up2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Depth(SpokenScene):
    """reads stack over a genome bar -> depth -> C = N x L / G -> the lesson's numbers."""

    def construct(self):
        bx0, bx1, by = -5.5, 5.5, -2.9
        bar = rect(bx0, bx1, by, 0.34, GREY, 0.4)
        blab = T("genome, length G", 24, GREY).next_to(bar, DOWN, buff=0.15).align_to(bar, LEFT)
        self.at("count the pieces")
        self.play(Create(bar), FadeIn(blab), run_time=0.7)

        # one read
        rl = 1.8
        r1 = read(-4.6, -4.6 + rl, by + 0.45, BLUE, 0.28)
        r1lab = T("one read, length L", 24, BLUE).next_to(r1, UP, buff=0.12)
        self.at("A read is")
        self.play(FadeIn(r1, shift=DOWN * 0.3), FadeIn(r1lab), run_time=0.7)

        # stack
        rng = np.random.RandomState(11)
        starts = np.sort(rng.uniform(bx0, bx1 - rl, 18))
        rng.shuffle(starts)
        lanes = []
        placed = []
        for s in starts:
            for li, end in enumerate(lanes):
                if s > end + 0.08:
                    lanes[li] = s + rl
                    break
            else:
                li = len(lanes)
                lanes.append(s + rl)
            placed.append((s, li))
        stack = VGroup(*[read(s, s + rl, by + 0.45 + li * 0.34, BLUE, 0.27) for s, li in placed])
        self.at("Coverage is how many")
        self.play(FadeOut(r1lab), FadeIn(stack, lag_ratio=0.06), FadeOut(r1), run_time=1.6)
        xd = 0.4
        dash = DashedLine([xd, by + 0.2, 0], [xd, by + 0.45 + len(lanes) * 0.34 + 0.05, 0], color=TEXT, stroke_width=3)
        over = [m for m, (s, _) in zip(stack, placed) if s <= xd <= s + rl]
        dlab = T("reads over this base", 26, TEXT).next_to(dash, UP, buff=0.12)
        self.at("on average")
        self.play(Create(dash), FadeIn(dlab), *[m.animate.set_fill(BLUE, 1.0) for m in over],
                  *[m.animate.set_opacity(0.3) for m in stack if m not in over], run_time=0.9)

        # formula
        f = VGroup(M("C", 46), M("=", 46), M("N", 46), M("x", 46), M("L", 46), M("/", 46), M("G", 46)).arrange(RIGHT, buff=0.35)
        f.move_to([0, 2.9, 0])
        self.at("Coverage equals")
        self.play(FadeIn(f[0:2]), FadeOut(dlab), run_time=0.5)
        slot = T("coverage, the mean depth", 26, TEXT).move_to([0, 1.95, 0])
        self.play(FadeIn(slot), run_time=0.3)
        steps = [("times", "N: the number of reads", BLUE, f[2:3]),
                 ("read length", "L: the read length", BLUE, f[3:5]),
                 ("genome length", "G: the genome length", GREY, f[5:7])]
        for word, txt, col, parts in steps:
            self.at(word)
            new = T(txt, 26, col).move_to([0, 1.95, 0])
            self.play(ReplacementTransform(slot, new), FadeIn(parts), run_time=0.5)
            slot = new
        self.at("For a human genome")
        n0 = M("N = C x G / L", 40).move_to([0, 2.95, 0])
        self.play(FadeOut(slot), ReplacementTransform(f, n0), run_time=0.7)
        n1 = M("= 30 x 3.1 x 10^9 / 150", 40).move_to([0, 2.05, 0])
        self.at("fold coverage")
        self.play(FadeIn(n1, shift=UP * 0.15), run_time=0.6)
        n2 = M("= 620 million reads", 40, GREEN).move_to([0, 1.15, 0])
        self.at("needs about")
        self.play(FadeIn(n2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Gaps(SpokenScene):
    """random starts leave unread bases: e^-C, drawn, with three bars showing how much stays unread."""

    def construct(self):
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1, 0.25], x_length=5.6, y_length=4.6,
                  tips=False, axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True,
                                           "include_numbers": False}).move_to([-2.9, -0.35, 0])
        xt = VGroup(*[M(str(i), 22, GREY).next_to(ax.c2p(i, 0), DOWN, buff=0.15) for i in range(0, 7)])
        yt = VGroup(*[M(s, 22, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15) for s, v in [("0", 0), ("0.5", 0.5), ("1", 1)]])
        xl = T("coverage C", 26, TEXT).next_to(ax, DOWN, buff=0.55)
        yl = T("fraction unread", 26, TEXT).move_to([-4.3, 2.55, 0])
        self.at("Reads start")
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=1.2)

        curve = ax.plot(lambda c: float(np.exp(-c)), x_range=[0, 6], color=RED, stroke_width=6)
        self.at("Poisson model")
        self.play(Create(curve), run_time=2.0)
        form = M("e^-C", 44, RED).move_to(ax.c2p(2.2, 0.55))
        self.at("e to the minus")
        self.play(FadeIn(form, scale=0.9), run_time=0.5)

        cx, cw = 4.0, 4.4

        def row(y, title, stripes):
            t = T(title, 26, TEXT).move_to([cx, y + 0.55, 0])
            base = rect(cx - cw / 2, cx + cw / 2, y, 0.32, GREY, 0.45)
            reds = VGroup(*[Rectangle(width=w, height=0.32, stroke_width=0, fill_color=RED, fill_opacity=1)
                            .move_to([cx - cw / 2 + p + w / 2, y, 0]) for p, w in stripes])
            return VGroup(t, base, reds)

        r1 = row(1.9, "1-fold: 37% unread", [(0.3, 0.5), (1.3, 0.4), (2.2, 0.3), (3.0, 0.25), (3.7, 0.18)])
        r2 = row(0.2, "5-fold: about 21 million\nbases unread", [(2.1, 0.04)])
        r3 = row(-1.7, "30-fold: far less than\none base unread", [])
        r2[0].move_to([cx, 0.2 + 0.75, 0])
        r3[0].move_to([cx, -1.7 + 0.75, 0])
        d1 = Dot(ax.c2p(1, np.exp(-1)), radius=0.11, color=TEXT)
        d5 = Dot(ax.c2p(5, np.exp(-5)), radius=0.11, color=TEXT)
        self.at("At one")
        self.play(FadeIn(d1, scale=1.6), FadeIn(r1), run_time=0.7)
        self.at("At five")
        self.play(FadeIn(d5, scale=1.6), FadeIn(r2), run_time=0.7)
        self.at("At 30")
        edge = Arrow(ax.c2p(5.4, 0.1), ax.c2p(6.0, 0.02), color=TEXT, buff=0, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(r3), GrowArrow(edge), run_time=0.7)
        self.at("more depth shrinks")
        self.play(Indicate(curve, color=RED, scale_factor=1.0), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Repeat(SpokenScene):
    """two identical repeats; a short read fits both; nothing links a repeat to its own flanks."""

    def construct(self):
        y = 0.3
        mp = repeat_map(y)
        allm = VGroup(*[mp[k] for k in ("A", "R1", "B", "dots", "C", "R2", "D")])
        self.play(*[FadeIn(mp[k], shift=UP * 0.1) for k in ("A", "R1", "B", "dots", "C", "R2", "D")],
                  run_time=1.0)
        nts = T("not to scale", 22, GREY).move_to([4.9, -3.35, 0])
        len_lab = T("6 kilobases", 22, ORANGE).next_to(mp["R1"], DOWN, buff=0.15)
        uni = T("unique", 22, TEAL_).next_to(mp["A"], DOWN, buff=0.15)
        self.at("identical copies")
        link = ArcBetweenPoints([-3.1, y + 0.55, 0], [3.1, y + 0.55, 0], angle=-PI / 3.2, color=ORANGE, stroke_width=4)
        eq = T("identical", 28, ORANGE).move_to([0, y + 1.6, 0])
        self.play(Create(link), FadeIn(eq), Indicate(mp["R1"], color=ORANGE), Indicate(mp["R2"], color=ORANGE),
                  FadeIn(len_lab), FadeIn(nts), run_time=1.0)

        rd = read(-0.35, 0.35, y + 2.5, BLUE, 0.28)  # above the arc
        rd_lab = T("read from inside the repeat", 26, BLUE).next_to(rd, RIGHT, buff=0.2)
        self.play(FadeOut(eq), run_time=0.2)
        self.at("A read from inside")
        self.play(FadeIn(rd, shift=DOWN * 0.2), FadeIn(rd_lab), run_time=0.7)
        a1 = arr([-0.3, y + 2.3, 0], [-3.1, y + 0.55, 0], BLUE)
        a2 = arr([0.3, y + 2.3, 0], [3.1, y + 0.55, 0], BLUE)
        self.at("fits both copies")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)

        # edges
        self.at("Reads at its edges")
        e1 = read(-4.45, -3.95, y + 0.7, BLUE, 0.26)
        e2 = read(-2.25, -1.75, y + 0.7, BLUE, 0.26)
        e3 = read(2.25, 2.75, y + 0.7, BLUE, 0.26)
        e4 = read(3.85, 4.35, y + 0.7, BLUE, 0.26)
        self.play(FadeOut(VGroup(rd, rd_lab, a1, a2, link)), FadeIn(VGroup(e1, e2, e3, e4)),
                  FadeIn(uni), run_time=0.8)

        # pair cannot reach across
        self.at("But no read")
        pa = read(-4.5, -4.05, y + 1.25, BLUE, 0.26)
        pb = read(-3.75, -3.3, y + 1.25, BLUE, 0.26)
        pl = Line([-4.05, y + 1.25, 0], [-3.75, y + 1.25, 0], color=BLUE, stroke_width=3)
        pair_lab = T("pair from a 400-base fragment", 26, BLUE).next_to(pa, UP, buff=0.35).align_to(pa, LEFT)
        self.play(FadeIn(VGroup(pa, pb, pl)), FadeIn(pair_lab), run_time=0.7)
        span = DashedLine([-3.9, y + 1.25, 0], [-2.3, y + 1.25, 0], color=RED, stroke_width=4)
        self.at("reaches across")
        self.play(Create(span), run_time=0.7)
        xm = xmark([-2.3, y + 1.25, 0])
        self.play(FadeIn(xm), run_time=0.3)

        # two joinings
        self.at("So the assembler")
        self.play(FadeOut(VGroup(pa, pb, pl, pair_lab, span, xm, e1, e2, e3, e4, uni, len_lab, nts)), allm.animate.shift(UP * 1.9), run_time=0.7)
        h1 = hyp_row(["A", "R", "B", "C", "R", "D"], -0.5)
        h2 = hyp_row(["A", "R", "D", "C", "R", "B"], -2.3)
        orl = T("or", 32, TEXT).move_to([0, -1.4, 0])
        self.at("cannot tell")
        self.play(FadeIn(h1, shift=UP * 0.15), run_time=0.6)
        self.at("which flanking")
        self.play(FadeIn(orl), FadeIn(h2, shift=UP * 0.15), run_time=0.7)
        self.at("belong together")
        qm = T("?", 72, RED, weight=BOLD).move_to([5.6, -1.4, 0])
        self.play(FadeIn(qm, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05More(SpokenScene):
    """more reads: still ambiguous; the repeats collapse into one, or the contig breaks."""

    def construct(self):
        y = -0.6
        mp = repeat_map(y)
        allm = VGroup(*[mp[k] for k in ("A", "R1", "B", "dots", "C", "R2", "D")])
        self.add(allm)
        self.at("Deeper coverage")
        rng = np.random.RandomState(5)
        stacks = VGroup()
        for k, (x0, x1) in (("R1", SEG["R1"]), ("R2", SEG["R2"])):
            for i in range(8):
                a = x0 + 0.1 + (i % 2) * 0.15 + rng.uniform(0, 0.2)
                stacks.add(read(a, a + 0.6, y + 0.75 + i * 0.3, BLUE, 0.24))
        self.play(FadeIn(stacks, lag_ratio=0.1), run_time=2.0)
        same = T("every read fits both copies", 32, BLUE).move_to([0, 3.0, 0])
        self.at("Every new read")
        self.play(FadeIn(same), run_time=0.5)

        self.at("collapses the two copies")
        self.play(FadeOut(VGroup(stacks, same, allm)), run_time=0.5)
        R = VGroup(rect(-1.0, 1.0, 0.0, 0.8, ORANGE, 0.35), T("repeat", 26, ORANGE))
        R[1].move_to(R[0])
        chips = {}
        for k, (x, yy) in {"A": (-4.2, 1.5), "C": (-4.2, -1.5), "B": (4.2, 1.5), "D": (4.2, -1.5)}.items():
            chips[k] = VGroup(rect(x - 0.45, x + 0.45, yy, 0.6, TEAL_, 0.35), T(k, 26, TEAL_).move_to([x, yy, 0]))
        lines = VGroup(*[Line([-3.75 if k in "AC" else 3.75, chips[k][0].get_center()[1], 0],
                              [-1.0 if k in "AC" else 1.0, 0, 0], color=GREY, stroke_width=4) for k in chips])
        lab = T("one block, four flanks", 28, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(R, scale=0.8), FadeIn(VGroup(*chips.values())), Create(lines), FadeIn(lab), run_time=1.2)

        self.at("it breaks the")
        self.play(FadeOut(VGroup(R, lines, lab, *chips.values())), run_time=0.5)
        yy = 0.4
        pa = VGroup(rect(-4.2, -2.0, yy, 0.9, TEAL_, 0.35), T("A", 30, TEAL_).move_to([-3.1, yy, 0]))
        pr = VGroup(rect(-1.0, 1.0, yy, 0.9, ORANGE, 0.35), T("repeat", 30, ORANGE).move_to([0, yy, 0]))
        pb = VGroup(rect(2.0, 4.2, yy, 0.9, TEAL_, 0.35), T("B", 30, TEAL_).move_to([3.1, yy, 0]))
        brk = VGroup(xmark([-1.5, yy, 0]), xmark([1.5, yy, 0]))
        bl = T("contig broken", 36, RED).move_to([0, -1.4, 0])
        self.play(FadeIn(VGroup(pa, pr, pb)), run_time=0.5)
        self.play(FadeIn(brk), FadeIn(bl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Long(SpokenScene):
    """a 15-kilobase read holds a whole repeat with unique sequence on both sides, pinning it."""

    def construct(self):
        y = 0.7
        mp = repeat_map(y)
        allm = VGroup(*[mp[k] for k in ("A", "R1", "B", "dots", "C", "R2", "D")])
        self.add(allm)
        # 6 kb = 1.6 units, so 15 kb = 4.0 units: 1.2 of unique sequence each side of the copy
        lr = read(-5.1, -1.1, y + 0.95, YELLOW, 0.34)
        lr_lab = T("a 15-kilobase read", 32, YELLOW).next_to(lr, UP, buff=0.15)
        self.at("Now try")
        self.play(FadeIn(lr, shift=DOWN * 0.2), FadeIn(lr_lab), run_time=0.8)
        hold = SurroundingRectangle(mp["R1"], color=ORANGE, buff=0.06, stroke_width=5)
        r6 = T("6 kilobases", 24, ORANGE).move_to([-3.1, y - 0.7, 0])
        self.at("hold a whole")
        self.play(Create(hold), FadeIn(r6), run_time=0.6)
        ua = Line([-5.1, y - 1.2, 0], [-3.9, y - 1.2, 0], color=TEAL_, stroke_width=6)
        ub = Line([-2.3, y - 1.2, 0], [-1.1, y - 1.2, 0], color=TEAL_, stroke_width=6)
        ulab = T("unique on each side", 26, TEAL_).move_to([-3.1, y - 1.7, 0])
        self.at("unique sequence")
        self.play(Create(ua), Create(ub), FadeIn(ulab), run_time=0.8)
        self.at("pins the copy")
        pin = rect(-5.1, -1.1, y, BAR_H + 0.1, GREEN, 0.0, 5)
        self.play(FadeIn(pin), hold.animate.set_color(GREEN), run_time=0.7)
        lr2 = read(1.1, 5.1, y + 0.95, YELLOW, 0.34)
        pin2 = rect(1.1, 5.1, y, BAR_H + 0.1, GREEN, 0.0, 5)
        self.at("Long reads span")
        self.play(FadeIn(lr2, shift=DOWN * 0.2), FadeOut(VGroup(ua, ub, ulab, r6)), run_time=0.6)
        self.play(FadeIn(pin2), run_time=0.5)
        r1 = T("A repeat longer than your reads cannot be placed.", 34, TEXT)
        r2 = T("More depth does not help.", 34, RED)
        rule = VGroup(r1, r2).arrange(DOWN, buff=0.2).move_to([0, -2.3, 0])
        self.at("Keep this rule")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.7)
        self.at("more depth")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A repeat longer than your reads cannot be placed."
