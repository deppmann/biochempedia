"""RNAi and antisense knockdown: turning one protein down, not off  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = DNA / the gene, cells and animals, axes, de-emphasised text
  PINK   = messenger RNA (the cell's own, the target)
  PURPLE = protein (the thing that is turned down)
  BLUE   = the knockdown reagent (double-stranded RNA, siRNA guide, shRNA, morpholino)
  ORANGE = the cutting machinery (Dicer, RISC, Argonaute)
  YELLOW = what is measured, matched or highlighted
  GREEN  = a control or a rescue
  RED    = the problem (alarm, off-target, mistargeting, a block)
  GOLD   = dates, the idealised tag and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL = "#E58FC0"   # messenger RNA (pink, to stay apart from the blue reagent)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.12, align=LEFT, colors=None, weight=NORMAL):
    g = VGroup(*[T(t, size, (colors[i] if colors else color), weight=weight) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def gene_bar(x, y, w=3.4, label="gene (DNA)", lsize=24):
    bar = RoundedRectangle(corner_radius=0.1, width=w, height=0.34, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])
    lb = lab(label, lsize, GREY).move_to([x, y + 0.5, 0]) if label else VGroup()
    return VGroup(bar, lb)


def rna(x0, x1, y, color=TEAL, w=9):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w)


def dsrna(x0, x1, y, color=BLUE, w=5, gap=0.16):
    return VGroup(Line([x0, y + gap / 2, 0], [x1, y + gap / 2, 0], color=color, stroke_width=w),
                  Line([x0, y - gap / 2, 0], [x1, y - gap / 2, 0], color=color, stroke_width=w))


def dots(cx, cy, n=12, cols=4, color=PURPLE, r=0.13, gap=0.42):
    rows = int(np.ceil(n / cols))
    g = VGroup()
    for i in range(n):
        rr, cc = divmod(i, cols)
        g.add(Dot(radius=r, color=color).move_to([cx + (cc - (cols - 1) / 2) * gap, cy + ((rows - 1) / 2 - rr) * gap, 0]))
    return g


def xmark(c, s=0.35, color=RED, w=6):
    return VGroup(Line([c[0] - s, c[1] - s, 0], [c[0] + s, c[1] + s, 0], color=color, stroke_width=w),
                  Line([c[0] - s, c[1] + s, 0], [c[0] + s, c[1] - s, 0], color=color, stroke_width=w))


def cell(c, r=1.2, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.10).move_to([c[0], c[1], 0])


def worm(x, y, w=3.2, h=0.7, tint=False, text="worm", tsize=22):
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=BLUE if tint else GREY, fill_opacity=0.30 if tint else 0.12).move_to([x, y, 0])
    g = VGroup(body)
    if text:
        g.add(lab(text, tsize, GREY).move_to(body))
    return g


def tag(text, color=GREY, size=22):
    return T(text, size, color)


def two_line_chip(a, b, color, size=22, pad=0.2):
    t = lines(a, b, size=size, color=color, buff=0.08, align=ORIGIN)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, t.move_to(box))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Turning One Protein Down, Not Off"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """knockout edits the DNA; knockdown lowers protein with the gene intact; antisense in worms, sense control silenced too."""

    def construct(self):
        q = lab("what does this protein do?", 30, YELLOW).move_to([0, 3.15, 0])

        def row(y):
            g = gene_bar(-3.4, y)
            a = arr([-1.3, y, 0], [0.4, y, 0])
            d = dots(2.6, y, 12)
            pl = lab("protein", 24, PURPLE).move_to([2.6, y - 0.95, 0])
            return g, a, d, pl

        gA, aA, dA, pA = row(1.55)
        gB, aB, dB, pB = row(-1.35)
        notch = Rectangle(width=0.2, height=0.7, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([-3.4, 1.55, 0])
        ko = lab("knockout: the DNA is altered", 26, RED).move_to([-3.4, 0.75, 0])
        kd = lab("knockdown: the gene is intact", 26, TEXT).move_to([-3.4, -2.15, 0])

        self.at("To learn what")
        self.play(FadeIn(q), FadeIn(gA), FadeIn(aA), FadeIn(dA), FadeIn(pA), run_time=0.8)
        self.at("A knockout alters")
        self.play(FadeIn(notch, scale=1.5), dA.animate.set_opacity(0.12), FadeIn(ko), run_time=0.7)
        self.at("A knockdown lowers")
        self.play(FadeIn(gB), FadeIn(aB), FadeIn(dB), FadeIn(pB), run_time=0.8)
        self.at("how much protein")
        self.play(*[m.animate.set_opacity(0.12) for m in list(dB)[3:]], run_time=0.8)
        self.at("leaves the gene intact")
        self.play(FadeIn(kd), run_time=0.5)

        w1y, w2y = 1.05, -2.0
        wa = worm(-3.8, w1y)
        wb = worm(-3.8, w2y)
        ca = chip("antisense RNA", BLUE, 28).move_to([-3.8, w1y + 1.55, 0])
        cb = chip("sense RNA: the control", BLUE, 28).move_to([-3.8, w2y + 1.55, 0])
        na = Line([-3.8, w1y + 1.15, 0], [-3.8, w1y + 0.4, 0], color=BLUE, stroke_width=5)
        nb = Line([-3.8, w2y + 1.15, 0], [-3.8, w2y + 0.4, 0], color=BLUE, stroke_width=5)
        ra = arr([-1.9, w1y, 0], [0.2, w1y, 0])
        rb = arr([-1.9, w2y, 0], [0.2, w2y, 0])
        ta = lab("gene silenced", 32, TEXT).move_to([3.0, w1y, 0])
        tb = lines("gene silenced too,", "in some experiments", size=30, color=RED, align=ORIGIN).move_to([3.0, w2y, 0])

        self.at("Before double")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.at("worm biologists")
        self.play(FadeIn(wa), FadeIn(wb), run_time=0.5)
        self.at("silenced genes")
        self.play(FadeIn(ca, shift=UP * 0.1), Create(na), run_time=0.5)
        self.at("injecting antisense")
        self.play(ca.animate.shift(DOWN * 0.2), na.animate.shift(DOWN * 0.1), GrowArrow(ra), FadeIn(ta), run_time=0.7)
        self.at("with sense")
        self.play(FadeIn(cb, shift=UP * 0.1), Create(nb), run_time=0.5)
        self.play(GrowArrow(rb), run_time=0.4)
        self.at("silenced the gene")
        self.play(FadeIn(tb), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Inject(SpokenScene):
    """dsRNA beats either strand; a few molecules, amplification; DNA unchanged, mRNA the target."""

    def construct(self):
        wm = worm(-3.0, 0.2, w=5.0, h=0.9, text="C. elegans", tsize=24)
        nd = Line([-3.0, 2.25, 0], [-3.0, 0.68, 0], color=BLUE, stroke_width=5)
        ch = chip("double-stranded RNA", BLUE, 26).move_to([-3.0, 2.7, 0])
        base = Line([1.8, -2.4, 0], [6.4, -2.4, 0], color=GREY, stroke_width=3)
        b1 = Rectangle(width=1.0, height=4.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.8).move_to([2.7, -2.4 + 2.1, 0])
        b2 = Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([4.2, -2.4 + 0.4, 0])
        b3 = Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([5.7, -2.4 + 0.4, 0])
        l1 = lab("double", 22).move_to([2.7, -2.8, 0])
        l2 = lab("sense", 22).move_to([4.2, -2.8, 0])
        l3 = lab("antisense", 22).move_to([5.75, -2.8, 0])
        hd = lab("silencing effect", 26, TEXT).move_to([4.2, 2.3, 0])
        sch = lab("schematic, no values", 22, GOLD).move_to([-3.0, -2.2, 0])

        self.at("Fire")
        self.play(FadeIn(wm), FadeIn(ch, shift=DOWN * 0.1), Create(nd), run_time=0.8)
        self.play(wm[0].animate.set_fill(BLUE, opacity=0.30), run_time=0.6)
        self.at("substantially more effective")
        self.play(FadeIn(base), FadeIn(hd), FadeIn(l1), GrowFromEdge(b1, DOWN), FadeIn(sch), run_time=0.9)
        self.at("either single strand")
        self.play(FadeIn(b2), FadeIn(b3), FadeIn(l2), FadeIn(l3), run_time=0.6)

        self.at("Only a few molecules")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        fan_dot = Dot(radius=0.3, color=BLUE).move_to([-4.6, 0.3, 0])
        few_l = lines("a few molecules", "per affected cell", size=28, color=TEXT, buff=0.08, align=ORIGIN).move_to([-4.7, -1.0, 0])
        bars = VGroup(*[rna(0.0, 3.0, y, TEAL, 10) for y in (1.7, 0.3, -1.1)])
        fans = VGroup(*[arr([-4.2, 0.3, 0], [-0.3, y, 0], BLUE, w=4, tip=0.18) for y in (1.7, 0.3, -1.1)])
        chp = chip("a catalytic or amplifying step?", YELLOW, 28).move_to([3.4, 0.3, 0])
        chp = fit(chp, max_w=3.0)
        chp = two_line_chip("a catalytic or", "amplifying step?", YELLOW, 26).move_to([4.9, 0.3, 0])
        self.play(FadeIn(fan_dot, scale=1.5), FadeIn(few_l), run_time=0.6)
        self.at("suggested a catalytic")
        self.play(FadeIn(bars), *[GrowArrow(f) for f in fans], run_time=0.8)
        self.play(FadeIn(chp, shift=LEFT * 0.2), run_time=0.5)

        self.at("Montgomery")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        g = gene_bar(-3.5, 0.9, w=4.0, label="DNA sequence", lsize=28)
        gl = lab("no evidence of change", 28, TEXT).move_to([-3.5, 0.0, 0])
        ar = arr([-1.2, 0.9, 0], [0.5, 0.9, 0])
        m = rna(1.0, 6.0, 0.9, TEAL, 14)
        ml = lab("messenger RNA", 28, TEAL).move_to([3.5, 1.7, 0])
        tgt = DashedVMobject(Rectangle(width=5.4, height=0.95, stroke_color=YELLOW, stroke_width=4).move_to([3.5, 0.9, 0]))
        tl = lab("the target", 30, YELLOW, weight=BOLD).move_to([3.5, -0.1, 0])
        self.play(FadeIn(g), FadeIn(ar), FadeIn(m), run_time=0.7)
        self.at("no evidence of change")
        self.play(FadeIn(gl), run_time=0.5)
        self.at("Their data supported")
        self.play(FadeIn(ml), run_time=0.5)
        self.at("as the target")
        self.play(Create(tgt), FadeIn(tl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cut(SpokenScene):
    """Dicer cuts dsRNA; short pieces; RISC holds the guide; Argonaute cuts the matching mRNA; less protein."""

    def construct(self):
        cx = -2.0
        ds_y = 2.5
        ds = dsrna(cx - 2.75, cx + 2.75, ds_y)
        ds_l = lines("double-stranded", "RNA", size=24, color=BLUE, buff=0.05).move_to([4.2, ds_y, 0])
        dicer = chip("Dicer", ORANGE, 24).move_to([cx - 2.2, 3.2, 0])
        xs_ = [cx - 2.75 + 5.5 * k / 5 for k in range(0, 6)]
        pieces = VGroup(*[dsrna(xs_[k] + 0.12, xs_[k + 1] - 0.12, ds_y) for k in range(5)])
        pc_l = lines("21 to 22 nucleotides:", "sequence-specific mediators", size=24, color=YELLOW, buff=0.05).move_to([4.15, ds_y, 0])
        si_l = lab("siRNA", 26, BLUE, weight=BOLD).move_to([4.15, ds_y - 0.9, 0])

        r_y = 0.55
        rect = RoundedRectangle(corner_radius=0.2, width=5.6, height=0.85, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.16).move_to([cx, r_y, 0])
        r_t = lab("RISC: Argonaute-family proteins", 24, ORANGE).move_to(rect)
        guide = Line([cx - 1.0, 0, 0], [cx + 1.0, 0, 0], color=BLUE, stroke_width=5).move_to([cx, r_y - 0.62, 0])
        m_y = -1.5
        mrna = rna(cx - 3.6, cx + 3.6, m_y, TEAL, 11)
        guide_l = lines("one strand of", "the siRNA", size=22, color=BLUE, buff=0.05).move_to([4.15, r_y - 0.62, 0])
        m_l = lab("messenger RNA", 24, TEAL).move_to([4.15, m_y, 0])
        hd = lab("mammalian cells: Argonaute2 supplies the cutting", 26, ORANGE).move_to([cx, -2.45, 0])

        self.at("An enzyme called Dicer")
        self.play(FadeIn(ds), FadeIn(ds_l), FadeIn(dicer, shift=DOWN * 0.1), run_time=0.7)
        self.at("cuts double")
        cuts = VGroup()
        for k in range(1, 5):
            x = xs_[k]
            self.play(dicer.animate.move_to([x, 3.2, 0]), run_time=0.25)
            c = Line([x, ds_y + 0.4, 0], [x, ds_y - 0.4, 0], color=ORANGE, stroke_width=4)
            cuts.add(c)
            self.add(c)
        self.play(FadeOut(ds), FadeOut(cuts), FadeIn(pieces), run_time=0.5)
        self.play(dicer.animate.move_to([cx, 3.2, 0]), run_time=0.3)
        self.at("Pieces")
        self.play(FadeOut(ds_l), FadeIn(pc_l), run_time=0.5)
        self.at("We call them")
        self.play(FadeIn(si_l), run_time=0.4)
        self.at("A complex called")
        self.play(FadeOut(dicer), FadeIn(rect), FadeIn(r_t), run_time=0.6)
        self.at("holds the")
        pc = pieces[2].copy()
        self.play(Transform(pc, guide), FadeIn(guide_l), run_time=0.8)
        self.add(guide)
        self.remove(pc)
        self.at("pairs with matching")
        self.play(FadeIn(mrna), FadeIn(m_l), FadeOut(guide_l), FadeOut(pc_l), FadeOut(si_l), FadeOut(pieces), run_time=0.6)
        match = Rectangle(width=2.0, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.35).move_to([cx, m_y + 0.0, 0])
        self.at("matching messenger")
        self.play(FadeIn(match), run_time=0.5)
        self.at("In mammalian cells")
        self.play(FadeIn(hd), Indicate(r_t, color=ORANGE), run_time=0.6)
        self.at("is cut")
        left = rna(cx - 3.6, cx + 0.1, m_y, TEAL, 11)
        right = rna(cx + 0.5, cx + 3.6, m_y, TEAL, 11)
        scar = Line([cx + 0.3, m_y - 0.35, 0], [cx + 0.3, m_y + 0.35, 0], color=ORANGE, stroke_width=5)
        self.play(FadeOut(mrna), FadeIn(left), FadeIn(right), Create(scar), run_time=0.6)
        d_pro = dots(cx + 1.2, -3.15, 8, 8, gap=0.4)
        p_l = lab("protein", 26, PURPLE).move_to([cx - 1.8, -3.15, 0])
        self.play(FadeIn(d_pro), FadeIn(p_l), run_time=0.5)
        self.at("makes less protein")
        self.play(*[m.animate.set_opacity(0.12) for m in list(d_pro)[3:]], left.animate.shift(LEFT * 0.35),
                  right.animate.shift(RIGHT * 0.35), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Reagents(SpokenScene):
    """long dsRNA alarms mammalian cells -> short siRNA; shRNA made inside; morpholino binds RNA."""

    def construct(self):
        xs = [-4.3, 0.0, 4.3]
        cy = 0.9
        heads = [lab(t, 32, BLUE, weight=BOLD).move_to([x, 3.35, 0]) for t, x in zip(["siRNA", "shRNA", "morpholino"], xs)]
        head_long = lab("long double-stranded RNA", 24, BLUE, weight=BOLD).move_to([xs[0] + 0.2, 3.35, 0])
        cells = [cell([x, cy], 1.45) for x in xs]

        long_ds = dsrna(xs[0] - 1.95, xs[0] + 1.95, 2.75, BLUE, 7)
        alarm = VGroup(*[Line([xs[0] + 1.65 * np.cos(a), cy + 1.65 * np.sin(a), 0], [xs[0] + 2.05 * np.cos(a), cy + 2.05 * np.sin(a), 0],
                              color=RED, stroke_width=5) for a in [0.0, 0.12 * np.pi, 0.88 * np.pi, np.pi, 1.12 * np.pi, 1.88 * np.pi]])
        alarm_t = lines("broad antiviral", "responses", size=26, color=RED, buff=0.08, align=ORIGIN).move_to([xs[0], -1.55, 0])
        short_ds = dsrna(xs[0] - 0.55, xs[0] + 0.55, cy, BLUE, 5)
        t1 = lines("short synthetic", "duplexes", size=26, color=TEXT, buff=0.08, align=ORIGIN).move_to([xs[0], -1.55, 0])

        ring = Circle(radius=0.28, stroke_color=GREY, stroke_width=4).move_to([xs[1] - 0.62, cy, 0])
        hp = poly([[xs[1] + 0.35, cy + 0.35], [xs[1] + 0.35, cy - 0.25], [xs[1] + 0.52, cy - 0.38], [xs[1] + 0.7, cy - 0.25],
                   [xs[1] + 0.7, cy + 0.35]], BLUE, 5)
        pr = arr([xs[1] - 0.25, cy, 0], [xs[1] + 0.2, cy, 0], GREY, w=4, tip=0.15)
        t2 = lines("a hairpin, usually made", "inside the cell, from an", "RNA polymerase III", "promoter", size=28, color=TEXT, buff=0.1,
                   align=ORIGIN).move_to([xs[1], -1.95, 0])
        mr = rna(xs[2] - 0.85, xs[2] + 0.85, cy, TEAL, 10)
        mo = Rectangle(width=1.0, height=0.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to([xs[2] - 0.1, cy + 0.2, 0])
        t3 = lines("binds its target RNA,", "prevents translation", "or splicing", size=26, color=TEXT, buff=0.08,
                   align=ORIGIN).move_to([xs[2], -1.75, 0])

        self.at("In many mammalian")
        self.play(FadeIn(head_long), FadeIn(cells[0]), run_time=0.6)
        self.play(FadeIn(long_ds, shift=DOWN * 0.1), run_time=0.5)
        self.at("sets off")
        self.play(FadeIn(alarm), FadeIn(alarm_t), run_time=0.6)
        self.at("short synthetic")
        self.play(FadeOut(long_ds), FadeOut(alarm), FadeOut(alarm_t), FadeOut(head_long), run_time=0.5)
        self.play(FadeIn(heads[0]), FadeIn(short_ds), FadeIn(t1), run_time=0.6)
        self.at("a hairpin")
        self.play(FadeIn(heads[1]), FadeIn(cells[1]), FadeIn(ring), run_time=0.6)
        self.at("transcribed inside")
        self.play(GrowArrow(pr), Create(hp), FadeIn(t2), run_time=0.8)
        self.at("A morpholino")
        self.play(FadeIn(heads[2]), FadeIn(cells[2]), FadeIn(mr), run_time=0.6)
        self.at("binds its target")
        self.play(FadeIn(mo, shift=DOWN * 0.2), FadeIn(t3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """check the knockdown (transcript, protein), then one idealised blot + migration example."""

    def construct(self):
        top = chip("check the knockdown itself", YELLOW, 34).move_to([0, 2.6, 0])
        c1 = two_line_chip("transcript:", "quantitative RT-PCR", TEAL, 30).move_to([-3.4, 0.2, 0])
        c2 = two_line_chip("protein:", "Western analysis", PURPLE, 30).move_to([3.4, 0.2, 0])

        self.at("Check the knockdown")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.6)
        self.at("transcript by")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at("protein by Western")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)

        self.at("example")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        tg = lab("IDEALISED EXAMPLE", 26, GOLD, weight=BOLD).move_to([0, 3.2, 0])
        slab = RoundedRectangle(corner_radius=0.15, width=5.0, height=2.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.10).move_to([-3.4, 1.2, 0])
        band1 = Rectangle(width=1.8, height=0.6, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to([-4.6, 1.2, 0])
        band2 = Rectangle(width=1.8, height=0.6, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to([-2.2, 1.2, 0])
        ln1 = lab("without siRNA", 22).move_to([-4.6, -0.2, 0])
        ln2 = lab("with siRNA", 22).move_to([-2.2, -0.2, 0])
        px = lab("protein X on a blot", 26, PURPLE).move_to([-3.4, 2.7, 0])
        self.play(FadeIn(tg), FadeIn(slab), FadeIn(band1), FadeIn(band2), FadeIn(ln1), FadeIn(ln2), FadeIn(px), run_time=0.8)
        self.at("lowers protein X")
        pct = M("80% lower", 32, YELLOW).move_to([-3.4, -0.9, 0])
        self.play(band2.animate.set_fill(PURPLE, opacity=0.2), FadeIn(pct), run_time=0.8)
        self.at("cells migrate more slowly")
        mh = lab("migration", 26, TEXT).move_to([3.6, 2.7, 0])
        am1 = arr([0.9, 1.5, 0], [6.1, 1.5, 0], GREY, 6)
        am2 = arr([0.9, 0.2, 0], [3.3, 0.2, 0], YELLOW, 6)
        al1 = lab("without siRNA", 22).move_to([3.5, 2.0, 0])
        al2 = lab("with siRNA: slower", 22, YELLOW).move_to([2.4, 0.7, 0])
        self.play(FadeIn(mh), FadeIn(al1), GrowArrow(am1), run_time=0.5)
        self.play(FadeIn(al2), GrowArrow(am2), run_time=0.7)
        self.at("That is an association")
        assoc = chip("an association with reduced protein", YELLOW, 30).move_to([0, -2.2, 0])
        self.play(FadeIn(assoc, shift=UP * 0.15), run_time=0.6)
        self.at("It does not show")
        no = chip("not shown: X is dispensable or essential", RED, 28).move_to([0, -3.05, 0])
        self.play(FadeIn(no, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """siRNA seed off-targets; morpholino mistargeting; three controls; a rescue still has a limit."""

    def construct(self):
        lx = -3.4
        h1 = lab("An siRNA hits other genes", 26, TEXT, weight=BOLD).move_to([lx, 3.35, 0])
        gw = 4.8
        g0 = lx - gw / 2
        guide = Rectangle(width=gw, height=0.3, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.5).move_to([lx, 2.55, 0])
        seed = Rectangle(width=gw * 6 / 21, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to(
            [g0 + gw * 4 / 21, 2.55, 0])
        gl = lab("guide", 22, BLUE).move_to([g0 + 0.45, 2.95, 0])
        sl = lab("positions 2 to 7", 22, YELLOW).move_to([g0 + gw * 4 / 21 + 0.7, 1.95, 0])
        other = rna(g0, g0 + gw, 1.05, TEAL, 10)
        box = DashedVMobject(Rectangle(width=gw * 6 / 21 + 0.1, height=0.55, stroke_color=RED, stroke_width=3).move_to(
            [g0 + gw * 4 / 21, 1.05, 0]))
        ol = lab("off-target three-prime untranslated region", 22, RED)
        ol = fit(ol, max_w=5.4).move_to([lx, 0.45, 0])
        five = lab("5′", 22, BLUE).move_to([g0 - 0.3, 2.55, 0])
        comp = lab("complementary", 22, RED).move_to([lx + 1.2, 1.5, 0])
        conn = VGroup(*[DashedLine([g0 + gw * a / 21, 2.38, 0], [g0 + gw * a / 21, 1.35, 0], color=YELLOW, stroke_width=2) for a in (1, 7)])

        rx = 3.7
        h2 = lab("A morpholino mistargets", 26, TEXT, weight=BOLD).move_to([rx, 3.35, 0])
        emb = cell([rx + 1.5, 2.2], 0.75)
        eml = lab("zebrafish embryo", 22).move_to([rx + 1.5, 1.2, 0])
        mo = chip("morpholino", BLUE, 24).move_to([rx - 1.4, 2.2, 0])
        mar = arr([rx - 0.5, 2.2, 0], [rx + 0.65, 2.2, 0], BLUE)
        mis = lab("mistargeting", 22, RED).move_to([rx - 1.0, 1.55, 0])
        death = lines("p53-dependent neural", "cell death", size=22, color=RED, buff=0.06, align=ORIGIN).move_to([rx + 0.6, 0.5, 0])

        for m_ in (h1, guide, seed, gl, sl, other, box, ol, conn, five, comp, h2, emb, eml, mo, mar, mis, death):
            m_.shift(DOWN * 0.3)
        sep = Line([-6.2, -0.7, 0], [6.2, -0.7, 0], color=GREY, stroke_width=1.5)
        hd = lab("THREE CONTROLS", 26, GREEN, weight=BOLD).move_to([0, -1.1, 0])
        c1 = two_line_chip("measure the", "target protein", GREEN, 24).move_to([-4.4, -2.2, 0])
        c2 = two_line_chip("two non-overlapping", "reagents, same gene", GREEN, 24).move_to([0, -2.2, 0])
        c3 = two_line_chip("rescue: a resistant transgene,", "silent changes in target site", GREEN, 24)
        c3 = fit(c3, max_w=4.3).move_to([4.4, -2.2, 0])
        lim = lines("Even a good rescue does not formally exclude a phenotype", "that also needs an off-target effect", size=24,
                    color=GREY, buff=0.06, align=ORIGIN).move_to([0, -3.3, 0])

        self.at("Two things mislead")
        self.play(FadeIn(h1), FadeIn(guide), FadeIn(gl), FadeIn(five), run_time=0.6)
        self.at("other genes")
        self.play(FadeIn(other), run_time=0.4)
        self.at("In HeLa profiling")
        self.play(FadeIn(ol), run_time=0.5)
        self.at("complementary to")
        self.play(FadeIn(seed), FadeIn(sl), Create(box), FadeIn(conn), FadeIn(comp), run_time=0.9)
        self.at("And morpholino")
        self.play(FadeIn(h2), FadeIn(emb), FadeIn(eml), FadeIn(mo), run_time=0.6)
        self.at("could induce")
        self.play(GrowArrow(mar), FadeIn(mis), FadeIn(death), run_time=0.7)
        self.at("Three controls catch this")
        self.play(FadeIn(sep), FadeIn(hd), run_time=0.5)
        self.at("Measure the target")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("Use two")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("Rescue with")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.5)
        self.at("Even a good")
        self.play(FadeIn(lim), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Origin(SpokenScene):
    """1998 method = finding; 2006 Nobel; 2010 Piezo1."""

    def row(self, year, text_lines, tagtext, icon, y, ycolor=GOLD):
        yr = M(year, 36, ycolor, weight=BOLD).move_to([-5.45, y, 0])
        icon.move_to([-3.3, y, 0])
        txt = lines(*text_lines, size=32, color=TEXT, buff=0.1)
        grp = VGroup(txt) if not tagtext else VGroup(txt, tag(tagtext)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        grp = fit(grp, max_w=8.4, max_h=2.1)
        grp.move_to([-1.9 + grp.width / 2, y, 0])
        return yr, icon, grp

    def construct(self):
        ic98 = VGroup(dsrna(-0.45, 0.45, 0.0), arr([0.55, 0, 0], [0.95, 0, 0], GREY, 4, 0.14))
        g98 = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.3, stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=0.12).move_to([1.4, 0, 0])
        ic98 = VGroup(ic98, g98).scale(0.8)
        ic06 = VGroup(Circle(radius=0.55, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25),
                      Circle(radius=0.38, stroke_color=GOLD, stroke_width=2))
        cand = VGroup(*[Square(side_length=0.4, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.2) for _ in range(4)]
                      ).arrange(RIGHT, buff=0.14)
        cand[2].set_stroke(YELLOW, 3.5).set_fill(YELLOW, 0.5)

        cl = lines("candidate genes,", "one required", size=22, color=GREY, buff=0.04, align=ORIGIN).move_to([-3.5, -3.2, 0])
        r98 = self.row("1998", ["Double-stranded RNA silences", "matching genes in C. elegans"], "Fire, Mello et al., 1998", ic98, 2.7)
        r06 = self.row("2006", ["Nobel Prize in Physiology", "or Medicine, shared by Fire and Mello"], None, ic06, 0.2)
        r10 = self.row("2010", ["siRNA knockdown of candidate genes:", "Piezo1 required for mechanically", "activated current"],
                       "Coste, Patapoutian et al., 2010", cand, -2.4)

        self.at("The method was the finding")
        yr, ic, tx = r98
        self.play(FadeIn(yr), FadeIn(ic), run_time=0.6)
        self.at("In 1998")
        self.play(FadeIn(tx), run_time=0.6)
        self.at("Fire and Mello shared")
        yr, ic, tx = r06
        self.play(FadeIn(yr), FadeIn(ic), FadeIn(tx), run_time=0.8)
        self.at("In 2010")
        yr, ic, tx = r10
        self.play(FadeIn(yr), FadeIn(ic), FadeIn(tx), FadeIn(cl), run_time=0.8)
        self.at("required for")
        self.play(Indicate(ic, color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked(SpokenScene):
    """Snail2 morpholino (2007); clathrin RNAi and rescue (2005); the rule."""

    def construct(self):
        lx, rx = -3.3, 3.3
        h1 = lab("Snail2 and cadherin6B", 26, TEXT, weight=BOLD).move_to([lx, 3.35, 0])
        mo = chip("morpholino", BLUE, 26).move_to([lx, 2.45, 0])
        sn = chip("Snail2", PURPLE, 30).move_to([lx, 1.0, 0])
        cd = chip("cadherin6B", PURPLE, 30).move_to([lx, -1.3, 0])
        rep = Line([lx, 0.55, 0], [lx, -0.75, 0], color=RED, stroke_width=5)
        bar = Line([lx - 0.35, -0.77, 0], [lx + 0.35, -0.77, 0], color=RED, stroke_width=7)
        blk = Line([lx, 2.05, 0], [lx, 1.78, 0], color=BLUE, stroke_width=4)
        cross = Line([lx - 0.45, 1.78, 0], [lx + 0.45, 1.78, 0], color=BLUE, stroke_width=8)
        t30 = lab("derepressed within 30 minutes", 26, YELLOW).move_to([lx, -2.35, 0])
        tg1 = tag("Taneyhill, Coles & Bronner-Fraser, 2007").move_to([lx, -3.3, 0])

        h2 = lab("Clathrin and mitosis", 26, TEXT, weight=BOLD).move_to([rx, 3.35, 0])
        ri = chip("RNAi: clathrin depleted", BLUE, 26).move_to([rx, 2.45, 0])
        n_l = lab("normal mitosis", 22).move_to([rx - 0.7, 1.55, 0])
        n_b = Rectangle(width=1.8, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([rx - 2.3 + 0.9, 1.15, 0])
        p_l = lab("after RNAi: prolonged", 22, RED).move_to([rx - 0.35, 0.45, 0])
        p_b = Rectangle(width=4.2, height=0.3, stroke_width=0, fill_color=RED, fill_opacity=0.7).move_to([rx - 2.3 + 2.1, 0.05, 0])
        sch = lab("schematic", 22, GOLD).move_to([rx + 2.4, 1.15, 0])
        r_ok = chip("clathrin triskelia: rescued", GREEN, 26).move_to([rx, -1.2, 0])
        r_no = chip("N-terminal domain: not rescued", RED, 26)
        r_no = fit(r_no, max_w=5.8).move_to([rx, -2.3, 0])
        tl2 = lab("Royle, Bright & Lagnado, 2005", 22, GREY).move_to([rx, -3.3, 0])

        self.at("In 2007")
        self.play(FadeIn(h1), FadeIn(sn), FadeIn(cd), FadeIn(rep), FadeIn(bar), run_time=0.8)
        self.at("blocked Snail")
        self.play(FadeIn(mo, shift=DOWN * 0.1), run_time=0.4)
        self.play(Create(blk), FadeIn(cross), sn.animate.set_opacity(0.35), run_time=0.5)
        self.at("repressed within")
        self.play(FadeOut(rep), FadeOut(bar), cd[0].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.3), cd[1].animate.set_color(YELLOW),
                  run_time=0.6)
        self.at("30 minutes")
        self.play(FadeIn(t30), FadeIn(tg1), run_time=0.5)
        self.at("In 2005")
        self.play(FadeIn(h2), FadeIn(ri), run_time=0.6)
        self.at("mitosis was prolonged")
        self.play(FadeIn(n_l), FadeIn(n_b), FadeIn(sch), run_time=0.5)
        self.play(FadeIn(p_l), GrowFromEdge(p_b, LEFT), FadeIn(tl2), run_time=0.8)
        self.at("Clathrin triskelia")
        self.play(FadeIn(r_ok, shift=UP * 0.1), run_time=0.5)
        self.at("domain did not")
        self.play(FadeIn(r_no, shift=UP * 0.1), run_time=0.5)

        self.at("knockdown phenotype", lead=0.5)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("A knockdown phenotype is an", "association with reduced protein.", size=42, color=TEXT, buff=0.2, align=ORIGIN)
        rule_box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.5, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(rule_box, UP, buff=0.25)
        VGroup(rule, rule_box, head).move_to([0, 0, 0])
        self.play(FadeIn(head), Create(rule_box), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A knockdown phenotype is an association with reduced protein."
