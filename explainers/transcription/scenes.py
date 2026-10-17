"""Transcription: which strand does the polymerase read, and which way does it go? (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the template strand (the DNA strand the polymerase reads)
  YELLOW = the coding strand (the DNA strand with the RNA's sequence, T for U)
  GREEN  = the RNA
  PURPLE = RNA polymerase
  RED    = "not found / no answer" (the top strand has no match, the bare duplex says nothing)
  GREY   = strand ends (5' and 3'), pairing ticks, structure, de-emphasised
  TEXT   = DNA letters not yet assigned to a role
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

TOP = "TACGGATCCATGAAACGT"   # written 5' -> 3', left to right (the lesson's sequence problem)
BOT = "ATGCCTAGGTACTTTGCA"   # written 3' -> 5', left to right
RNA = "ACGUUUCAUGG"          # 5' -> 3'
DX = 0.62
FS = 42
P0 = 7                       # first column (0-based) covered by the RNA; columns 7..17
T3, B3 = 2.45, 1.45          # top / bottom strand rows in scene 3
TY, BY = 1.3, 0.3            # top / bottom strand rows from scene 4 on
RY = 2.4                     # RNA row (above the top strand)
DROP = -1.4                  # row where the displaced coding strand sits in the bubble


def X(i):
    return (i - 8.5) * DX


def mk_row(seq, y, color=TEXT, size=FS, cols=None, xf=X):
    cols = range(len(seq)) if cols is None else cols
    return [M(seq[i], size, color).move_to([xf(i), y, 0]) for i in cols]


def lab(txt, x, y, color=GREY, size=24, weight=NORMAL):
    return T(txt, size, color, weight=weight).move_to([x, y, 0])


def tick(i, y1, y2, color=GREY, xf=X, w=2.5):
    return Line([xf(i), y1 - 0.3, 0], [xf(i), y2 + 0.3, 0], color=color, stroke_width=w)


def tag(text, color, size=26):
    return chip(text, color, size=size, pad=0.16)


def harrow(x0, x1, y, color, w=6):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.5)


def blob(cx, y0, y1, w):
    r = RoundedRectangle(corner_radius=0.55, width=w, height=y1 - y0, stroke_color=PURPLE, stroke_width=3,
                         fill_color=PURPLE, fill_opacity=0.16)
    r.move_to([cx, (y0 + y1) / 2, 0]).set_z_index(-1)
    return r


def setc(mobs, color):
    return [m.animate.set_color(color) for m in mobs]


class S00Title(TitleCard):
    LESSON = "Transcription: from DNA to RNA"
    TITLE = "Which strand does the polymerase read?"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a bare duplex, a 'template?' tag that cannot settle, a direction that cannot settle, empty RNA slots."""

    def construct(self):
        ty, by = 1.2, -0.3
        top = mk_row(TOP, ty)
        bot = mk_row(BOT, by)
        ticks = [Line([X(i), ty - 0.4, 0], [X(i), by + 0.4, 0], color=GREY, stroke_width=2.5) for i in range(18)]
        ends = VGroup(lab("5'", -6.0, ty), lab("3'", 6.0, ty), lab("3'", -6.0, by), lab("5'", 6.0, by))
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.15) for m in top], lag_ratio=0.03), FadeIn(ends), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in bot], lag_ratio=0.03),
                  LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.03), run_time=0.8)
        duplex = VGroup(*top, *bot)
        self.at("base pairs long")
        br = Brace(VGroup(*bot), DOWN, color=GREY, buff=0.15)
        brl = T("18 base pairs", 26, GREY).next_to(br, DOWN, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.7)

        slots = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.5, height=0.62,
                                                          stroke_color=GREEN, stroke_width=2.5), num_dashes=16)
                         .move_to([X(i), -2.7, 0]) for i in range(P0, 18)])
        rna_lbl = T("RNA", 30, GREEN, weight=BOLD).move_to([X(P0) - 1.1, -2.7, 0])
        self.at("copies part of it")
        self.play(FadeOut(br), FadeOut(brl), run_time=0.4)
        self.play(FadeIn(slots, shift=UP * 0.1), FadeIn(rna_lbl), run_time=0.7)

        self.at("Which strand")
        box = SurroundingRectangle(VGroup(*top), color=BLUE, buff=0.1, stroke_width=3.5, corner_radius=0.12)
        tg = tag("template?", BLUE, 28).move_to([-4.3, 2.3, 0])
        self.play(Create(box), FadeIn(tg, shift=DOWN * 0.1), run_time=0.6)
        self.wait(0.3)
        box2 = SurroundingRectangle(VGroup(*bot), color=BLUE, buff=0.1, stroke_width=3.5, corner_radius=0.12)
        tg2 = tag("template?", BLUE, 28).move_to([-4.3, -1.35, 0])
        self.play(ReplacementTransform(box, box2), ReplacementTransform(tg, tg2), run_time=0.8)
        self.at("which way does it go")
        dl = harrow(-0.45, -1.9, 3.2, GREY)
        dr = harrow(0.45, 1.9, 3.2, GREY)
        dq = T("which way?", 28, TEXT)
        dq.move_to([0, 3.2, 0])
        dl.shift(LEFT * 0.65); dr.shift(RIGHT * 0.65)
        self.play(GrowArrow(dl), GrowArrow(dr), FadeIn(dq), run_time=0.7)
        self.at("Nothing in it says")
        self.play(ReplacementTransform(box2, box), ReplacementTransform(tg2, tg), run_time=0.5)
        self.play(ReplacementTransform(box, box2), ReplacementTransform(tg2, tg2.copy().move_to(tg2)), run_time=0.5)
        self.at("the RNA that was made")
        self.play(Indicate(slots, color=GREEN, scale_factor=1.06), Indicate(rna_lbl, color=GREEN), run_time=1.0)
        self.finish()


def rcol(m, y, x=2.9):
    """put a mobject in the right-hand label column, left edge at x."""
    m.move_to([0, y, 0])
    m.align_to([x, 0, 0], LEFT)
    return m


# ---------------------------------------------------------------------------------------------
class S02Rules(SpokenScene):
    """a small duplex opens under a polymerase, the guide strand is the template, RNA pairs and grows 5' to 3'."""

    def construct(self):
        S = 0.95
        OFF = -1.4
        xf = lambda j: (j - 2.5) * S + OFF
        tseq, oseq = "CTAGAA", "GATCTT"
        rseq = {5: "U", 4: "U", 3: "C", 2: "U"}      # column -> RNA letter, antiparallel to the template
        ry, ty, oy, dy = 2.2, 1.0, -0.2, -1.2
        FS2 = 56
        top = mk_row(tseq, ty, size=FS2, xf=xf)
        oth = mk_row(oseq, oy, size=FS2, xf=xf)
        ticks = [tick(j, ty, oy, xf=xf) for j in range(6)]
        e_t = [lab("5'", xf(0) - 0.85, ty, size=28), lab("3'", xf(5) + 0.85, ty, size=28)]
        e_o = [lab("3'", xf(0) - 0.85, oy, size=28), lab("5'", xf(5) + 0.85, oy, size=28)]
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in top + oth], lag_ratio=0.05),
                  *[Create(t) for t in ticks], *[FadeIn(e) for e in e_t + e_o], run_time=1.4)

        ex = rcol(T("example sequence", 24, GREY), oy)
        self.play(FadeIn(ex), run_time=0.5)
        pol = blob(xf(3.5), -1.75, 2.85, 3.7)
        pol_l = T("RNA polymerase", 26, PURPLE).move_to([xf(3.5), -2.25, 0])
        self.at("opens a short stretch")
        self.play(*[oth[j].animate.move_to([xf(j), dy, 0]) for j in range(2, 6)],
                  *[FadeOut(ticks[j]) for j in range(2, 6)],
                  e_o[1].animate.move_to([xf(5) + 0.85, dy, 0]), FadeIn(pol), FadeIn(pol_l), run_time=1.0)

        self.at("template strand")
        tpl = rcol(tag("template strand", BLUE, 24), ty)
        self.play(*setc(top, BLUE), FadeIn(tpl), run_time=0.6)

        rna = {j: M(rseq[j], FS2, GREEN).move_to([xf(j), ry, 0]) for j in rseq}
        rt = {j: tick(j, ry, ty, xf=xf, color=GREEN) for j in rseq}
        self.at("base pairing")
        self.play(FadeIn(rna[5], shift=DOWN * 0.3), Create(rt[5]), run_time=0.5)
        uo = rcol(tag("U opposite A", GREEN, 24), ry)
        self.play(FadeIn(uo), Indicate(top[5], color=BLUE, scale_factor=1.25), run_time=0.7)

        self.at("joins each new letter")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(rna[j], shift=DOWN * 0.3), Create(rt[j])) for j in (4, 3, 2)],
                              lag_ratio=0.5), run_time=1.6)
        end3 = lab("3'", xf(2) - 0.85, ry, GREEN, 28)
        end5 = lab("5'", xf(5) + 0.85, ry, GREEN, 28)
        self.play(FadeIn(end3), FadeIn(end5), run_time=0.5)

        self.at("So the RNA grows")
        ar = harrow(xf(5), xf(2), 3.2, GREEN)
        arl = rcol(T("RNA grows 5' to 3'", 24, GREEN), 3.2)
        self.play(GrowArrow(ar), FadeIn(arl), run_time=0.7)

        self.at("RNA is anti")
        self.play(Indicate(VGroup(e_t[0], e_t[1], end3, end5), color=YELLOW, scale_factor=1.3), run_time=1.0)

        self.at("reads the template")
        rd = harrow(xf(5), xf(2), -2.95, BLUE)
        rdl = rcol(T("reads 3' to 5'", 24, BLUE), -2.95)
        self.play(GrowArrow(rd), FadeIn(rdl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Coding(SpokenScene):
    """read the bottom strand right to left, line it up under the RNA, T for U, it matches: coding strand."""

    def construct(self):
        top = mk_row(TOP, T3)
        bot = mk_row(BOT, B3)
        ticks = [tick(i, T3, B3) for i in range(18)]
        ends = VGroup(lab("5'", -6.0, T3), lab("3'", 6.0, T3), lab("3'", -6.0, B3), lab("5'", 6.0, B3))
        self.add(*top, *bot, *ticks, ends)

        # the real RNA, written 5' -> 3', centred under the duplex
        ro_x = lambda k: (k - 5) * DX
        ry = -1.25
        rna = mk_row(RNA, ry, GREEN, xf=ro_x, cols=range(11))
        rl = lab("RNA", -4.6, ry, GREEN, 30, BOLD)
        r5 = lab("5'", ro_x(0) - 0.6, ry)
        r3 = lab("3'", ro_x(10) + 0.6, ry)
        self.at("real RNA")
        self.play(FadeIn(rl), FadeIn(r5), FadeIn(r3), run_time=0.6)
        wl = self._words()
        i_reads = [i for i, w in enumerate(wl) if w[1] == "reads"][0]
        for k in range(11):
            tk = wl[i_reads + 1 + k][0] - 0.1
            if tk - self.elapsed() > 0.02:
                self.wait(tk - self.elapsed())
            self.play(FadeIn(rna[k], shift=UP * 0.2), run_time=0.3)

        self.at("in place of")
        us = [rna[k] for k in range(11) if RNA[k] == "U"]
        note = T("U where DNA has T", 28, TEXT).move_to([0, ry - 0.75, 0])
        self.play(*[Indicate(u, color=YELLOW, scale_factor=1.35) for u in us], FadeIn(note), run_time=1.1)

        self.at("look for that sequence")
        self.play(Indicate(VGroup(*rna), color=GREEN, scale_factor=1.05), FadeOut(note), run_time=0.8)

        # read the bottom strand right to left into the readout row
        yo = -0.15
        read_lbl = T("bottom strand\nread 5' to 3'", 22, YELLOW, line_spacing=0.8).move_to([-4.9, yo, 0])
        read = []
        self.at("from right to left")
        arrow = harrow(X(17) + 0.2, X(7) - 0.2, B3 - 0.62, YELLOW, 5)
        self.play(GrowArrow(arrow), FadeIn(read_lbl), run_time=0.6)
        i_sp = [i for i, w in enumerate(wl) if w[1] == "spells"][0]
        n = 11
        for k in range(n):
            src = bot[17 - k]
            cp = M(BOT[17 - k], FS, YELLOW).move_to(src)
            read.append(cp)
            self.add(cp)
            tk = wl[i_sp + 1 + k][0] - 0.2
            if tk - self.elapsed() > 0.02:
                self.wait(tk - self.elapsed())
            self.play(Indicate(src, color=YELLOW, scale_factor=1.3), cp.animate.move_to([ro_x(k), yo, 0]),
                      run_time=0.45)

        self.at("That matches")
        eq = [Line([ro_x(k), yo - 0.32, 0], [ro_x(k), ry + 0.32, 0], color=GREEN, stroke_width=2.5) for k in range(11)]
        self.play(LaggedStart(*[Create(e) for e in eq], lag_ratio=0.05), run_time=0.8)
        diffs = [k for k in range(11) if RNA[k] == "U"]
        self.play(*[Indicate(VGroup(read[k], rna[k]), color=YELLOW, scale_factor=1.25) for k in diffs], run_time=0.9)

        self.at("does not contain it")
        nm = tag("no match", RED, 24).move_to([-4.3, 3.15, 0])
        scan = SurroundingRectangle(VGroup(*top[0:11]), color=RED, buff=0.1, stroke_width=3.5, corner_radius=0.1)
        self.play(Create(scan), run_time=0.25)
        self.play(scan.animate.shift(RIGHT * 7 * DX), run_time=0.6)
        self.play(*setc(top, RED), FadeIn(nm), run_time=0.4)
        self.play(*setc(top, TEXT), FadeOut(scan), run_time=0.4)

        self.at("So the bottom strand")
        cs = tag("coding strand", YELLOW, 26).move_to([-4.2, -0.25, 0])
        self.play(FadeOut(nm), FadeOut(VGroup(*read, *eq, arrow, read_lbl)), *setc(bot, YELLOW), FadeIn(cs), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class Sim:
    """the strands, the RNA and a small moving bubble. Position c is the column the polymerase is copying;
    the open window is columns c-1..c+1, the RNA is paired only inside it and peels off above behind it."""

    PEEL = 0.7

    def __init__(self, top_c=BLUE, bot_c=YELLOW):
        self.top = mk_row(TOP, TY, top_c)
        self.bot = mk_row(BOT, BY, bot_c)
        self.tk = {i: tick(i, TY, BY) for i in range(18)}
        self.rna, self.rt = {}, {}
        for k in range(11):
            i = 17 - k
            self.rna[i] = M(RNA[k], FS, GREEN).move_to([X(i), RY, 0]).set_opacity(0)
            self.rt[i] = tick(i, RY, TY, color=GREEN).set_stroke(opacity=0)
        self.r3 = lab("3'", X(17) - 0.6, RY, GREEN, 24).set_opacity(0)
        self.r5 = lab("5'", 6.0, RY, GREEN, 24).set_opacity(0)
        self.ends = VGroup(lab("5'", -6.0, TY), lab("3'", 6.0, TY), lab("3'", -6.0, BY), lab("5'", 6.0, BY))
        self.blob = blob(X(16.5), DROP - 0.45, RY + 0.35, 2.0).set_opacity(0)
        self.bl = T("RNA polymerase", 26, PURPLE).move_to([X(16.5), DROP - 0.95, 0]).set_opacity(0)

    def group(self):
        return VGroup(*self.top, *self.bot, *self.tk.values(), *self.rna.values(), *self.rt.values(),
                      self.r3, self.r5, self.ends, self.blob, self.bl)

    def plan(self, c):
        """list of (mobject, position or None, opacity, kind) for state c (None: nothing happening)."""
        out = []
        lo, hi = (1, 0) if c is None else (max(P0, c - 1), min(17, c + 1))
        for i in range(P0, 18):
            op = c is not None and lo <= i <= hi
            made = c is not None and i >= c
            hyb = made and op
            out.append((self.bot[i], [X(i), DROP if op else BY, 0], 1, "m"))
            out.append((self.tk[i], None, 0 if op else 1, "l"))
            out.append((self.rna[i], [X(i), RY if hyb else RY + self.PEEL, 0], 1 if made else 0, "m"))
            out.append((self.rt[i], None, 1 if hyb else 0, "l"))
        if c is None:
            out.append((self.blob, None, 0, "b"))
            out.append((self.bl, [X(16.5), DROP - 0.95, 0], 0, "t"))
            out.append((self.r3, [X(17) - 0.6, RY, 0], 0, "t"))
            out.append((self.r5, [6.0, RY, 0], 0, "t"))
        else:
            cx = X((lo + hi) / 2)
            out.append((self.blob, [cx, (DROP - 0.45 + RY + 0.35) / 2, 0], 1, "b"))
            out.append((self.bl, [cx, DROP - 0.95, 0], 1, "t"))
            out.append((self.r3, [X(c) - 0.6, RY, 0], 1, "t"))
            out.append((self.r5, [6.0, RY if (c <= 17 and min(17, c + 1) >= 17) else RY + self.PEEL, 0], 1, "t"))
        return out

    def _w(self, c):
        lo, hi = (1, 0) if c is None else (max(P0, c - 1), min(17, c + 1))
        return (hi - lo) * DX + 0.9

    def anims(self, c, top_color=None, bot_color=None, noblob=False):
        res = []
        for m, p, op, kind in self.plan(c):
            if noblob and m in (self.blob, self.bl):
                continue
            if kind == "l":
                res.append(m.animate.set_stroke(opacity=op))
            elif kind == "b":
                if c is None:
                    res.append(m.animate.set_opacity(0))
                else:
                    cx, w = p[0], self._w(c)
                    new = blob(cx, DROP - 0.45, RY + 0.35, w)
                    res.append(Transform(m, new))
            else:
                a = m.animate
                if p is not None:
                    a = a.move_to(p)
                a = a.set_opacity(op)
                if bot_color is not None and m in self.bot:
                    a = a.set_color(bot_color)
                res.append(a)
        if top_color is not None:
            res += [m.animate.set_color(top_color) for m in self.top]
        if bot_color is not None:
            res += [m.animate.set_color(bot_color) for m in self.bot[:P0]]
        return res


# ---------------------------------------------------------------------------------------------
class S04Template(SpokenScene):
    """the polymerase and its small bubble step left; the RNA pairs with the top strand inside the bubble."""

    def construct(self):
        sim = Sim(top_c=TEXT)
        cs = tag("coding strand", YELLOW, 26).move_to([-4.2, -0.25, 0])
        grp = sim.group()
        grp.shift(UP * (T3 - TY))
        self.add(grp, cs)
        self.play(grp.animate.shift(DOWN * (T3 - TY)), cs.animate.move_to([-4.2, DROP, 0]), run_time=0.5)

        self.at("other strand")
        tp = tag("template strand", BLUE, 26).move_to([-4.2, RY, 0])
        self.play(*setc(sim.top, BLUE), FadeIn(tp), run_time=0.7)

        self.at("Check it by pairing")
        self.play(FadeIn(sim.blob), FadeIn(sim.bl), run_time=0.01)
        self.play(*sim.anims(17), run_time=0.8)

        self.at("lies anti")
        self.play(Indicate(VGroup(sim.r3, sim.r5), color=GREEN, scale_factor=1.4), run_time=0.8)

        self.at("first RNA letter")
        self.play(Indicate(VGroup(sim.rna[17], sim.top[17]), color=YELLOW, scale_factor=1.3), run_time=0.8)

        self.at("C pairs with")
        self.play(*sim.anims(16), run_time=0.5)
        self.play(*sim.anims(15), run_time=0.5)

        self.at("and so on leftward")
        t_end = self.t_of("Every letter pairs") - 0.2
        per = max(0.18, (t_end - self.elapsed()) / 8)
        for c in range(14, 6, -1):
            self.play(*sim.anims(c), run_time=per * 0.9)
            self.wait(per * 0.1)

        self.at("Every letter pairs")
        self.play(Indicate(VGroup(sim.rna[7], sim.rna[8], sim.top[7], sim.top[8]), color=GREEN, scale_factor=1.2),
                  run_time=0.8)
        self.at("is the template")
        self.play(Indicate(VGroup(tp, *sim.top), color=BLUE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Direction(SpokenScene):
    """cleared and replayed: the polymerase slides right to left, the bubble moves with it, the RNA grows at its 3' tip."""

    def construct(self):
        sim = Sim()
        tp = tag("template strand", BLUE, 26).move_to([-4.2, RY, 0])
        cs = tag("coding strand", YELLOW, 26).move_to([-4.2, DROP, 0])
        self.add(sim.group(), tp, cs)
        # start from the end of scene 4
        for m, p, op, kind in sim.plan(7):
            if kind == "l":
                m.set_stroke(opacity=op)
            elif kind == "b":
                m.become(blob(p[0], DROP - 0.45, RY + 0.35, sim._w(7)))
            else:
                if p is not None:
                    m.move_to(p)
                m.set_opacity(op)

        self.at("Now watch the enzyme")
        self.play(*sim.anims(None), FadeOut(cs), run_time=1.0)
        self.at("reads the template")
        self.play(FadeIn(sim.blob), FadeIn(sim.bl), run_time=0.01)
        self.play(*sim.anims(17), run_time=0.8)
        self.at("is at the right")
        self.play(Indicate(sim.ends[1], color=BLUE, scale_factor=1.5), run_time=0.8)

        self.at("moves right to left")
        dr = harrow(4.0, -1.5, -2.95, PURPLE)
        drl = T("polymerase moves right to left", 24, PURPLE).move_to([1.2, -3.33, 0])
        self.play(GrowArrow(dr), FadeIn(drl), run_time=0.5)
        t_end = self.t_of("Its") - 0.3
        per = max(0.25, (t_end - self.elapsed()) / 10)
        for c in range(16, 6, -1):
            self.play(*sim.anims(c), run_time=per * 0.9)
            self.wait(per * 0.1)
        self.at("Its")
        self.play(FadeOut(sim.blob), FadeOut(sim.bl), FadeOut(dr), FadeOut(drl), run_time=0.5)
        self.at("toward the right")
        self.play(Indicate(sim.r5, color=GREEN, scale_factor=1.5), run_time=0.8)
        self.finish()


def rule_line(a, ac, mid, b, bc, size=34):
    return VGroup(T(a, size, ac, weight=BOLD), T(mid, size, TEXT), T(b, size, bc, weight=BOLD)).arrange(RIGHT, buff=0.2)


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the finished picture; antiparallel; a bare duplex says nothing; find the RNA; the rule."""

    def construct(self):
        sim = Sim()
        self.add(sim.group())
        for m, p, op, kind in sim.plan(7):
            if kind == "l":
                m.set_stroke(opacity=op)
            elif kind == "b":
                m.set_opacity(0)
            elif m is sim.bl:
                m.set_opacity(0)
            else:
                if p is not None:
                    m.move_to(p)
                m.set_opacity(op)
        self.wait(0.3)

        self.at("must be anti")
        ap = tag("antiparallel", GREY, 26).move_to([-4.2, 1.85, 0])
        self.play(FadeIn(ap), Indicate(VGroup(sim.ends[0], sim.ends[1], sim.r3, sim.r5), color=YELLOW, scale_factor=1.35),
                  run_time=1.1)

        self.at("a bare duplex")
        self.play(FadeOut(ap), *sim.anims(None, top_color=TEXT, bot_color=TEXT, noblob=True), run_time=1.0)
        bare = tag("bare duplex: no answer", RED, 26).move_to([0, 3.0, 0])
        self.at("no RNA")
        self.play(FadeIn(bare, shift=DOWN * 0.1), run_time=0.6)

        self.at("So find the RNA")
        self.play(FadeOut(bare), *sim.anims(7, top_color=BLUE, bot_color=YELLOW, noblob=True), run_time=1.2)

        self.at("Keep this rule")
        l1 = rule_line("RNA", GREEN, "matches the", "coding strand", YELLOW).move_to([0, -2.4, 0])
        l2 = rule_line("RNA", GREEN, "pairs with the", "template", BLUE).move_to([0, -3.1, 0])
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The RNA matches the coding strand and pairs with the template."
