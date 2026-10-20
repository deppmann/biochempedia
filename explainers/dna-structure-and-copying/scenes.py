"""DNA: Structure and Copying: Base pairing lets DNA copy itself  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = base A      ORANGE = base T      GREEN = base C      PURPLE = base G
  GREY   = old sugar-phosphate backbone, outlines, de-emphasized labels
  GOLD   = backbone of a NEW strand
  TEXT   = hydrogen bonds (dashed rungs), plain labels, the long DNA line
  TEAL   = a vocabulary term label, shown the moment it is spoken
  PINK   = an enzyme
  YELLOW = what is highlighted; a count or estimate
  RED    = a wrong base
DNA is drawn only as a ladder of labelled blocks (two parallel bars with blocks between them).
No atoms, no rings, no helix model. The 6-letter piece is a model, not a real gene.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CF0"
PINK = "#E86FB0"
BASECOL = {"A": BLUE, "T": ORANGE, "C": GREEN, "G": PURPLE}
COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}
TOP = "ATGCCA"
BOT = "".join(COMP[c] for c in TOP)      # TACGGT


def P(x, y):
    return np.array([x, y, 0.0])


def term(text, size=26):
    return chip(text, TEAL, size=size)


def block(letter, w, h, fs):
    letter = letter if letter in BASECOL else ""
    col = BASECOL.get(letter, TEXT)
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=col, stroke_width=3,
                         fill_color=col, fill_opacity=0.35 if letter else 0.0)
    if letter:
        return VGroup(r, T(letter, fs, TEXT, weight=BOLD).move_to(r))
    return VGroup(r)


def seg(w, bt, col):
    return RoundedRectangle(corner_radius=0.05, width=w, height=bt, stroke_color=col, stroke_width=2,
                            fill_color=col, fill_opacity=0.6)


class Dims:
    def __init__(self, sp, bw, bh, bt, rg, fs):
        self.sp, self.bw, self.bh, self.bt, self.rg, self.fs = sp, bw, bh, bt, rg, fs

    def xs(self, n=6, cx=0.0):
        return [cx + (i - (n - 1) / 2) * self.sp for i in range(n)]


BIG = Dims(1.45, 1.2, 0.8, 0.26, 0.9, 34)
SMALL = Dims(1.3, 0.9, 0.64, 0.2, 0.5, 28)
MINI = Dims(0.76, 0.64, 0.52, 0.15, 0.32, 24)


def strand(seq, dm, cx, block_cy, bar_above, col=GREY):
    """A strand: a row of backbone segments (one per nucleotide) with a base block under (or over) each.
    bar_above=True: backbone above the blocks (a top strand). Returns (group, segs, blocks)."""
    segs, blocks = [], []
    off = dm.bh / 2 + 0.04 + dm.bt / 2
    by = block_cy + (off if bar_above else -off)
    for x, ch in zip(dm.xs(len(seq), cx), seq):
        s = seg(dm.sp - 0.07, dm.bt, col).move_to(P(x, by))
        b = block(ch, dm.bw, dm.bh, dm.fs).move_to(P(x, block_cy))
        segs.append(s)
        blocks.append(b)
    return VGroup(*segs, *blocks), segs, blocks


def rung(top_b, bot_b, w=3):
    return DashedLine(top_b.get_bottom(), bot_b.get_top(), dash_length=0.09, color=TEXT, stroke_width=w)


class Ladder:
    def __init__(self, top_seq, bot_seq, dm, cx, cy, top_col=GREY, bot_col=GREY, live=False):
        self.dm = dm
        tcy = cy + dm.rg / 2 + dm.bh / 2
        bcy = cy - dm.rg / 2 - dm.bh / 2
        self.top, self.tsegs, self.tblocks = strand(top_seq, dm, cx, tcy, True, top_col)
        self.bot, self.bsegs, self.bblocks = strand(bot_seq, dm, cx, bcy, False, bot_col)
        if live:
            self.rungs = VGroup(*[always_redraw(lambda a=a, b=b: rung(a, b)) for a, b in zip(self.tblocks, self.bblocks)])
        else:
            self.rungs = VGroup(*[rung(a, b) for a, b in zip(self.tblocks, self.bblocks)])
        self.all = VGroup(self.top, self.bot, self.rungs)


def banner(text, size=30, color=TEXT, y=-3.0):
    return T(text, size, color).move_to(P(0, y))


class S00Title(TitleCard):
    LESSON = "DNA: Structure and Copying"
    TITLE = "Base Pairing Lets DNA Copy Itself"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """The puzzle: nearly 2 metres of DNA in a tiny nucleus, copied almost perfectly."""

    def construct(self):
        nuc = Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(P(0, 0.2))
        nlab_a = T("nucleus", 26, GREY).move_to(P(0, -1.3))
        bar = Line(P(-5.0, 2.55), P(5.0, 2.55), color=TEXT, stroke_width=8)
        blab = T("nearly 2 metres of DNA (not to scale)", 28, TEXT).move_to(P(0, 3.15))
        pts = []
        ys = np.linspace(-0.8, 0.8, 9)
        for k, yy in enumerate(ys):
            half = np.sqrt(max(1.0 - (yy / 1.0) ** 2, 0.02)) * 0.92
            xs_ = [-half, half] if k % 2 == 0 else [half, -half]
            for xx in xs_:
                pts.append(P(xx, 0.2 + yy))
        tangle = VMobject(color=TEXT, stroke_width=5)
        tangle.set_points_as_corners(pts)

        self.at("with a nucleus")
        self.play(FadeIn(nuc, scale=0.8), FadeIn(nlab_a), run_time=0.7)
        self.at("holds nearly")
        self.play(Create(bar), FadeIn(blab, shift=DOWN * 0.1), run_time=1.0)
        self.at("packed into")
        nlab_b = T("nucleus: about 0.005 to 0.010 mm across", 26, GREY).move_to(P(0, -1.3))
        self.play(ReplacementTransform(bar, tangle), FadeOut(blab), run_time=1.2)
        self.at("only about")
        self.play(ReplacementTransform(nlab_a, nlab_b), run_time=0.6)
        self.at("cell divides")
        self.wait(0.3)
        self.at("base pairs")
        b1 = banner("roughly 6 billion base pairs copied", 32, YELLOW, -2.45)
        self.play(FadeIn(b1, shift=UP * 0.15), run_time=0.6)
        self.at("almost every one")
        b2 = banner("almost every one right", 32, GREEN, -3.1)
        self.play(FadeIn(b2, shift=UP * 0.15), run_time=0.6)
        self.at("How can the structure")
        q1 = banner("How can the structure of DNA", 34, YELLOW, -2.45)
        q2 = banner("store information and copy itself almost perfectly?", 34, YELLOW, -3.1)
        self.play(FadeOut(b1), FadeOut(b2), run_time=0.4)
        self.play(FadeIn(q1, shift=UP * 0.15), FadeIn(q2, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Parts(SpokenScene):
    """A nucleotide: sugar, phosphate and base. Four bases."""

    def construct(self):
        dm = SMALL
        neutral, segs, blocks = strand("......", dm, 0.0, 1.75, True)
        # neutral blocks have no letter
        neutral = VGroup(*segs, *blocks)
        self.at("long chain")
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in neutral], lag_ratio=0.05), run_time=1.4)
        self.at("small repeating units")
        self.play(*[Indicate(s, color=GREY, scale_factor=1.1) for s in segs], run_time=0.8)
        self.at("Each unit is a nucleotide")
        unit = VGroup(segs[0], blocks[0])
        rect = SurroundingRectangle(unit, color=YELLOW, buff=0.1, stroke_width=3)
        nlab = term("nucleotide", 28).move_to(P(rect.get_center()[0], 3.2))
        self.play(Create(rect), FadeIn(nlab, shift=DOWN * 0.1), run_time=0.7)
        self.at("three parts")
        lead = Arrow(rect.get_bottom(), P(rect.get_center()[0] + 1.8, 0.6), buff=0.08, color=GREY, stroke_width=4)
        self.play(GrowArrow(lead), run_time=0.5)
        sugar = chip("sugar: deoxyribose", GREY, 26)
        phos = chip("phosphate group", GREY, 26)
        base = chip("base", TEXT, 26)
        row = VGroup(sugar, phos, base).arrange(RIGHT, buff=0.5).move_to(P(0.3, 0.0))
        self.at("sugar called")
        self.play(FadeIn(sugar, shift=UP * 0.2), run_time=0.6)
        self.at("phosphate group")
        self.play(FadeIn(phos, shift=UP * 0.2), run_time=0.6)
        self.at("and a base")
        self.play(FadeIn(base, shift=UP * 0.2), run_time=0.6)
        self.at("carries information")
        info = T("carries information", 26, YELLOW).move_to(P(base.get_center()[0], -0.95))
        self.play(Indicate(base, color=YELLOW), FadeIn(info, shift=UP * 0.1), run_time=0.8)
        legend = []
        for i, (ch, nm) in enumerate([("A", "adenine"), ("T", "thymine"), ("C", "cytosine"), ("G", "guanine")]):
            legend.append(chip(f"{ch}  {nm}", BASECOL[ch], 24))
        VGroup(*legend).arrange(RIGHT, buff=0.3).move_to(P(0, -2.5))
        for nm, c in zip(["adenine", "thymine", "cytosine", "guanine"], legend):
            self.at(nm)
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.5)
        self.at("We write them")
        newb = []
        anims = []
        for b, ch, x in zip(blocks, TOP, dm.xs(6)):
            nb = block(ch, dm.bw, dm.bh, dm.fs).move_to(b)
            newb.append(nb)
            anims.append(ReplacementTransform(b, nb))
        self.play(*anims, FadeOut(rect), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Pairs(SpokenScene):
    """Backbone, hydrogen bonds, base pairing."""

    def construct(self):
        dm = BIG
        L = Ladder(TOP, BOT, dm, 0.0, 0.3)
        self.at("A covalent bond")
        cov = term("covalent bond", 28).move_to(P(-2.4, 2.95))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in L.top], lag_ratio=0.04),
                  FadeIn(cov, shift=DOWN * 0.1), run_time=1.4)
        topbar_y = L.tsegs[0].get_center()[1]
        jx = (dm.xs()[1] + dm.xs()[2]) / 2
        self.at("strong bond")
        strong = T("strong: atoms share electrons", 24, GREY).move_to(P(2.6, 2.95))
        self.play(FadeIn(strong, shift=DOWN * 0.1), run_time=0.6)
        self.at("joins each sugar")
        mark = Rectangle(width=0.5, height=0.5, color=YELLOW, stroke_width=4).move_to(P(jx, topbar_y))
        arrow = Arrow(cov.get_bottom(), mark.get_top(), buff=0.05, color=YELLOW, stroke_width=4)
        self.play(Create(mark), GrowArrow(arrow), run_time=0.8)
        self.at("face each other")
        self.play(FadeOut(cov), FadeOut(strong), FadeOut(mark), FadeOut(arrow), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in L.bot], lag_ratio=0.04), run_time=1.2)
        self.at("bases inside")
        self.play(*[Indicate(b, color=YELLOW, scale_factor=1.1) for b in L.tblocks + L.bblocks], run_time=0.8)
        self.at("A hydrogen bond")
        hb = term("hydrogen bond", 28).move_to(P(-4.2, -2.5))
        self.play(FadeIn(hb, shift=UP * 0.1), run_time=0.5)
        self.at("weak attraction")
        weak = T("weak", 24, GREY).move_to(P(-4.2, -3.05))
        self.play(FadeIn(weak), run_time=0.4)
        self.at("hold each pair")
        self.play(LaggedStart(*[Create(r) for r in L.rungs], lag_ratio=0.12), run_time=1.0)
        self.at("Base pairing is the rule")
        bp = term("base pairing", 28).move_to(P(0.0, -2.5))
        self.play(FadeIn(bp, shift=UP * 0.1), run_time=0.5)
        self.at("A always pairs")
        at = T("A with T", 30, YELLOW).move_to(P(-1.9, -3.1))
        self.play(FadeIn(at, shift=UP * 0.1),
                  *[Indicate(VGroup(L.tblocks[i], L.bblocks[i]), color=YELLOW, scale_factor=1.12) for i in (0, 1, 5)],
                  run_time=0.9)
        self.at("C always pairs")
        cg = T("C with G", 30, YELLOW).move_to(P(1.9, -3.1))
        self.play(FadeIn(cg, shift=UP * 0.1),
                  *[Indicate(VGroup(L.tblocks[i], L.bblocks[i]), color=YELLOW, scale_factor=1.12) for i in (2, 3, 4)],
                  run_time=0.9)
        self.at("twist into")
        dh = term("double helix", 28).move_to(P(4.4, -2.5))
        note = T("(drawn untwisted)", 22, GREY).move_to(P(4.4, -3.05))
        self.play(FadeIn(dh, shift=UP * 0.1), FadeIn(note), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Unzip(SpokenScene):
    """The enzyme unzips the ladder: rungs break, backbones stay whole."""

    def construct(self):
        dm = SMALL
        L = Ladder(TOP, BOT, dm, 0.0, 0.0, live=True)
        self.at("Because of base pairing")
        self.play(FadeIn(L.top), FadeIn(L.bot), run_time=0.9)
        self.add(L.rungs)
        self.at("each strand holds")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.06) for m in L.top], run_time=0.9)
        self.at("rebuild its partner")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.06) for m in L.bot], run_time=0.9)
        self.at("An enzyme is")
        enz = chip("enzyme", PINK, 28).move_to(P(-5.0, 0.0))
        self.play(FadeIn(enz, shift=RIGHT * 0.3), run_time=0.6)
        self.at("speeds up a reaction")
        defn = T("enzyme: a protein that speeds up a reaction without being used up", 24, PINK).move_to(P(0, -1.95))
        fit(defn, max_w=11.8)
        self.play(FadeIn(defn, shift=UP * 0.1), run_time=0.7)
        self.at("unzips it")
        self.play(FadeOut(defn),
                  L.top.animate.shift(UP * 1.58), L.bot.animate.shift(DOWN * 1.58), run_time=1.5)
        self.at("hydrogen bonds between")
        brk0 = T("hydrogen bonds break", 30, TEXT).move_to(P(0.0, 0.0))
        bgr = Rectangle(width=brk0.width + 0.4, height=brk0.height + 0.3, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(brk0)
        brk = VGroup(bgr, brk0)
        ghost = VGroup(*[rung(a, b) for a, b in zip(L.tblocks, L.bblocks)])
        self.remove(L.rungs)
        self.add(ghost)
        self.play(FadeOut(ghost), FadeIn(brk, scale=1.1), run_time=0.6)
        self.at("backbones stay whole")
        t1 = T("backbone stays whole", 26, GREY).move_to(P(0, 3.2))
        t2 = T("backbone stays whole", 26, GREY).move_to(P(0, -3.2))
        self.play(FadeOut(brk), FadeIn(t1, shift=DOWN * 0.1), FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Copy(SpokenScene):
    """Templates, free nucleotides pair, polymerase joins them: two molecules."""

    def construct(self):
        dm = SMALL
        old_t, ots, otb = strand(TOP, dm, 0.0, 2.15, True)
        old_b, obs, obb = strand(BOT, dm, 0.0, -2.15, False)
        self.add(old_t, old_b)
        self.at("old strand now")
        tc1 = term("template", 26).move_to(P(5.05, 2.15))
        tc2 = term("template", 26).move_to(P(5.05, -2.15))
        self.play(FadeIn(tc1, shift=LEFT * 0.2), FadeIn(tc2, shift=LEFT * 0.2),
                  *[Indicate(m, color=YELLOW, scale_factor=1.05) for m in (old_t, old_b)], run_time=0.9)
        # free nucleotides: 12 loose blocks in the middle gap
        need = [COMP[c] for c in TOP] + [COMP[c] for c in BOT]   # for top template then bottom template
        order = [3, 8, 0, 10, 5, 1, 11, 6, 2, 9, 4, 7]           # fixed shuffle of which target each loose block serves
        lw, lh = 0.7, 0.5
        loose = []
        for k in range(12):
            tgt = order[k]
            x = (k - 5.5) * 0.8
            b = block(need[tgt], lw, lh, 22).move_to(P(x, 0.0))
            b.tgt = tgt
            loose.append(b)
        self.at("Free nucleotides")
        fl = T("free nucleotides float nearby", 26, GREY).move_to(P(0, -3.35))
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in loose], lag_ratio=0.05), FadeIn(fl), run_time=1.0)
        self.at("Each one pairs")
        sc = dm.bw / lw
        targets = []
        for b in loose:
            t = b.tgt
            if t < 6:
                pos = P(dm.xs()[t], 2.15 - dm.bh - dm.rg)       # under the top template
            else:
                pos = P(dm.xs()[t - 6], -2.15 + dm.bh + dm.rg)  # over the bottom template
            targets.append(pos)
        self.play(FadeOut(fl), FadeOut(tc1), FadeOut(tc2),
                  *[b.animate.scale(sc).move_to(p) for b, p in zip(loose, targets)], run_time=2.4)
        rungs = VGroup()
        for b in loose:
            t = b.tgt
            tmpl = otb[t] if t < 6 else obb[t - 6]
            r = DashedLine(tmpl.get_bottom() if t < 6 else tmpl.get_top(), b.get_top() if t < 6 else b.get_bottom(),
                           dash_length=0.09, color=TEXT, stroke_width=3)
            rungs.add(r)
        self.play(Create(rungs), run_time=0.3)
        self.at("A with T")
        rule = T("A with T,  C with G", 30, YELLOW).move_to(P(0, -3.35))
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.at("polymerase")
        pol = chip("DNA polymerase", PINK, 22, pad=0.1).move_to(P(0, 0.0))
        self.play(FadeIn(pol, scale=0.9), run_time=0.6)
        self.at("joins the new nucleotides")
        new_top, new_bot = [], []
        for t in range(6):
            new_top.append(seg(dm.sp - 0.07, dm.bt, GOLD).move_to(P(dm.xs()[t], 2.15 - dm.bh - dm.rg - dm.bh / 2 - 0.04 - dm.bt / 2)))
            new_bot.append(seg(dm.sp - 0.07, dm.bt, GOLD).move_to(P(dm.xs()[t], -2.15 + dm.bh + dm.rg + dm.bh / 2 + 0.04 + dm.bt / 2)))
        self.play(FadeOut(rule), LaggedStart(*[GrowFromEdge(s, LEFT) for s in new_top + new_bot], lag_ratio=0.04), run_time=1.4)
        cb = T("covalent bonds", 26, TEAL).move_to(P(0, -3.35))
        self.play(FadeIn(cb, shift=UP * 0.1), run_time=0.5)
        self.at("result is")
        m1 = T("molecule 1", 24, TEXT).move_to(P(5.05, 1.4))
        m2 = T("molecule 2", 24, TEXT).move_to(P(5.05, -1.4))
        self.play(FadeOut(pol), FadeOut(cb), FadeIn(m1), FadeIn(m2), run_time=0.7)
        self.at("one old strand")
        olds = [T("old", 26, GREY).move_to(P(-5.2, y)) for y in (2.6, -2.6)]
        self.play(*[FadeIn(o, shift=RIGHT * 0.1) for o in olds], run_time=0.5)
        self.at("one new strand")
        news = [T("new", 26, GOLD).move_to(P(-5.2, y)) for y in (0.55, -0.55)]
        self.play(*[FadeIn(o, shift=RIGHT * 0.1) for o in news], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """Same base order; one correct partner; proofreading; the textbook estimate."""

    def construct(self):
        dm = MINI
        orig = Ladder(TOP, BOT, dm, -3.7, 0.65)
        c1 = Ladder(TOP, BOT, dm, 3.7, 1.85, GREY, GOLD)
        c2 = Ladder(TOP, BOT, dm, 3.7, -0.6, GOLD, GREY)
        ol = T("original", 24, GREY).move_to(P(-3.7, 1.95))
        l1 = T("copy 1", 24, TEXT).move_to(P(2.0, 3.0))
        l2 = T("copy 2", 24, TEXT).move_to(P(2.0, 0.5))
        self.add(orig.all, ol)
        self.at("Both new molecules")
        a1 = Arrow(P(-1.0, 1.0), P(1.0, 1.8), buff=0.05, color=GREY, stroke_width=5, tip_length=0.2)
        a2 = Arrow(P(-1.0, 0.5), P(1.0, -0.4), buff=0.05, color=GREY, stroke_width=5, tip_length=0.2)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(c1.all, shift=LEFT * 0.3), FadeIn(c2.all, shift=LEFT * 0.3),
                  FadeIn(l1), FadeIn(l2), run_time=1.4)
        self.at("same base order")
        so = banner("same base order as the original", 30, YELLOW, -2.5)
        hi = [Indicate(g.top, color=YELLOW, scale_factor=1.03) for g in (orig, c1)]
        self.play(FadeIn(so, shift=UP * 0.1), *hi, Indicate(c2.bot, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("order of the bases is")
        s2 = banner("the order of the bases is the information", 30, YELLOW, -2.5)
        self.play(ReplacementTransform(so, s2), run_time=0.6)
        self.at("copying keeps it")
        s3 = banner("copying keeps it", 30, GREEN, -3.15)
        self.play(FadeIn(s3, shift=UP * 0.1), run_time=0.5)
        self.at("only one correct partner")
        col = 2
        hl = SurroundingRectangle(VGroup(c1.tblocks[col], c1.bblocks[col]), color=YELLOW, buff=0.08, stroke_width=4)
        s4 = banner("one correct partner at each spot", 30, YELLOW, -2.5)
        self.play(FadeOut(s2), FadeOut(s3), FadeIn(s4, shift=UP * 0.1), Create(hl), run_time=0.8)
        self.at("each spot")
        self.play(FadeOut(s4), FadeOut(hl), run_time=0.4)
        self.at("Proofreading")
        wrong = block("A", dm.bw, dm.bh, dm.fs).move_to(c1.bblocks[3])
        wrong[0].set_stroke(RED, 5)
        wl = T("wrong base", 24, RED).move_to(P(5.0, 3.0))
        pr = term("proofreading", 28).move_to(P(0, -2.5))
        self.play(ReplacementTransform(c1.bblocks[3], wrong), FadeIn(wl), FadeIn(pr, shift=UP * 0.1), run_time=0.5)
        self.at("most wrong")
        right = block("G", dm.bw, dm.bh, dm.fs).move_to(wrong)
        tag = T("most are caught", 24, GREEN).move_to(P(5.0, 3.0))
        self.play(ReplacementTransform(wrong, right), ReplacementTransform(wl, tag), run_time=0.8)
        self.at("textbook estimate")
        e1 = banner("about 1 uncorrected mistake", 30, YELLOW, -2.5)
        e2 = banner("for every billion bases copied (a textbook estimate)", 28, YELLOW, -3.15)
        self.play(FadeOut(pr), FadeIn(e1, shift=UP * 0.1), FadeIn(e2, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Each strand holds what is needed to rebuild its partner."
