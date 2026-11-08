"""Protein purification: trading yield for purity  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the target protein / the activity you follow
  GREY   = the other proteins (contaminants), structure, de-emphasised text
  BLUE   = apparatus (tubes, columns, beakers, beads, the cuvette) and the enzyme in the assay
  GREEN  = specific activity / purity rising, a control that passes
  RED    = yield / total activity falling, the pitfall
  TEAL   = salt
  ORANGE = a ligand or bait only the target recognizes (and its free competitor)
  PURPLE = the partner protein (arrestin)
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEALS = "#3FB8C0"
GREYS = ["#8B93A1", "#6F7787", "#A3AAB6", "#5E6676"]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def dot(x, y, r=0.1, color=GREY, op=0.9):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def crowd(n, x0, x1, y0, y1, seed, r=0.1):
    """n grey dots in a box (a mixture of many kinds: several greys)."""
    rng = np.random.RandomState(seed)
    return VGroup(*[dot(rng.uniform(x0, x1), rng.uniform(y0, y1), r, GREYS[i % 4], 0.85) for i in range(n)])


def tube(cx, cy, w=1.0, h=2.2, fill=GREY, level=0.75, fop=0.18):
    """Open-top tube: outline + liquid. Returns VGroup(outline, liquid)."""
    out = VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0], color=BLUE, stroke_width=4),
                 Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=BLUE, stroke_width=4),
                 Line([cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=BLUE, stroke_width=4))
    liq = Rectangle(width=w - 0.08, height=h * level, stroke_width=0, fill_color=fill, fill_opacity=fop)
    liq.move_to([cx, cy - h / 2 + h * level / 2 + 0.02, 0])
    return VGroup(out, liq)


def panel_title(text, color=TEXT, size=26):
    return T(text, size, color, weight=BOLD)


def bar(x, y, w, h, frac, color, outline=GREY):
    """Horizontal bar: dashed outline (full) + fill to frac. Returns (outline, fill)."""
    o = Rectangle(width=w, height=h, stroke_color=outline, stroke_width=2, fill_opacity=0)
    o.move_to([x + w / 2, y, 0])
    f = Rectangle(width=max(w * frac, 0.02), height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
    f.move_to([x + max(w * frac, 0.02) / 2, y, 0])
    return o, f


class Score(VGroup):
    """Scoreboard of two vertical bars: specific activity (green, rises) and total activity (red, falls)."""

    def __init__(self, cx, cy, h=3.0):
        self.H = h
        self.cx, self.cy = cx, cy
        self.bw = 0.7
        self.ox = [cx - 0.75, cx + 0.75]
        base = cy - h / 2
        self.base = base
        self.outs = [Rectangle(width=self.bw, height=h, stroke_color=GREY, stroke_width=2, fill_opacity=0)
                     .move_to([x, cy, 0]) for x in self.ox]
        self.fs = [Rectangle(width=self.bw, height=0.1, stroke_width=0, fill_color=c, fill_opacity=0.9)
                   for c in (GREEN, RED)]
        self.l1 = T("specific", 22, GREEN).move_to([self.ox[0], base - 0.35, 0])
        self.l1b = T("activity", 22, GREEN).move_to([self.ox[0], base - 0.65, 0])
        self.l2 = T("total", 22, RED).move_to([self.ox[1], base - 0.35, 0])
        self.l2b = T("activity", 22, RED).move_to([self.ox[1], base - 0.65, 0])
        self.vals = [0.12, 1.0]
        for f, x, v in zip(self.fs, self.ox, self.vals):
            f.stretch_to_fit_height(h * v)
            f.move_to([x, base + h * v / 2, 0])
        super().__init__(*self.outs, *self.fs, self.l1, self.l1b, self.l2, self.l2b)

    def to(self, sa, ta, rt=0.8):
        """Animation setting specific / total activity heights (fractions of full)."""
        anims = []
        for f, x, v in zip(self.fs, self.ox, (sa, ta)):
            g = Rectangle(width=self.bw, height=self.H * v, stroke_width=0, fill_color=f.get_fill_color(),
                          fill_opacity=0.9).move_to([x, self.base + self.H * v / 2, 0])
            anims.append(Transform(f, g))
        return AnimationGroup(*anims, run_time=rt)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Trading Yield for Purity"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a cell's crowd of proteins pours into a tube; which one does the job; can it be held alone?"""

    def construct(self):
        rng = np.random.RandomState(4)
        cell = Circle(radius=1.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([-4.3, 0.4, 0])
        cell_lbl = lab("one cell", 26, GREY).next_to(cell, UP, buff=0.15)
        n = 70
        pos = []
        for i in range(n):
            while True:
                x, y = rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)
                if x * x + y * y < 1.55 ** 2:
                    break
            pos.append((x, y))
        cd = VGroup(*[dot(-4.3 + x, 0.4 + y, 0.1, GREYS[i % 4], 0.85) for i, (x, y) in enumerate(pos)])

        self.at("One human cell")
        self.play(FadeIn(cell), FadeIn(cell_lbl), LaggedStart(*[FadeIn(d, scale=0.5) for d in cd], lag_ratio=0.02),
                  run_time=1.6)
        kinds = chip("about 10,000 kinds", GREY, 28).move_to([-4.3, -2.35, 0])
        self.at("protein molecules")
        self.play(FadeIn(kinds, shift=UP * 0.15), run_time=0.5)

        # pour into the tube
        t1 = tube(0.4, 0.0, w=1.9, h=3.2, level=0.8)
        tl = lab("a tube", 26, BLUE).move_to([0.4, -2.35, 0])
        self.at("You want one")
        target = cd[17]
        self.play(target.animate.set_color(YELLOW).scale(1.8).set_opacity(1.0), run_time=0.5)
        self.play(Indicate(target, color=YELLOW, scale_factor=1.6), run_time=0.5)
        self.at("Which molecule")
        q = T("which molecule does this job?", 32, YELLOW, weight=BOLD).move_to([0.6, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        # move the crowd into the tube (target loses its colour: it cannot be told apart)
        new_pos = [(0.4 + rng.uniform(-0.8, 0.8), rng.uniform(-1.45, 0.9)) for _ in range(n)]
        moves = []
        for d, (x, y) in zip(cd, new_pos):
            moves.append(d.animate.move_to([x, y, 0]))
        moves[17] = target.animate.move_to([new_pos[17][0], new_pos[17][1], 0]).set_color(GREYS[1]).scale(1 / 1.8)
        self.play(FadeIn(t1), FadeIn(tl), FadeOut(cell), FadeOut(cell_lbl), FadeOut(kinds),
                  *moves, run_time=1.6)
        tq = T("?", 54, YELLOW, weight=BOLD).move_to([2.0, 0.2, 0])
        self.play(FadeIn(tq), run_time=0.3)

        self.at("hold it in a tube")
        t2 = DashedVMobject(Rectangle(width=1.9, height=3.2, stroke_color=BLUE, stroke_width=4).move_to([4.9, 0.0, 0]), num_dashes=40)
        free = T("alone, free of\neverything else?", 26, YELLOW).move_to([4.9, -2.6, 0])
        arrow = arr([2.6, 0.0], [3.7, 0.0], GREY, 5, 0.2)
        self.play(GrowArrow(arrow), Create(t2), FadeIn(free), run_time=0.9)

        self.at("leading chemists")
        self.play(FadeOut(q), run_time=0.3)
        c1 = chip("1920s: enzymes are not proteins", RED, 26).move_to([-3.0, 3.25, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Assay(SpokenScene):
    """the assay first (absorbance at 340 falls as the enzyme eats NADH), then homogenate spun at three speeds."""

    def construct(self):
        # ---------- assay
        self.at("Start with an assay")
        head = T("an assay: a way to detect it", 34, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        cuv = tube(-4.2, -0.2, w=1.3, h=2.6, fill=YELLOW, level=0.8, fop=0.35)
        lamp = chip("light", GREY, 24).move_to([-6.0 + 0.0, -0.25, 0]).shift(LEFT * 0.0)
        # lamp left of the cuvette, detector right
        lamp.move_to([-6.1, -0.2, 0])
        det = chip("detector", GREY, 24).move_to([-2.0, -0.2, 0])
        beam1 = Line([-5.45, -0.2, 0], [-4.85, -0.2, 0], color=YELLOW, stroke_width=4)
        beam2 = Line([-3.55, -0.2, 0], [-3.05, -0.2, 0], color=YELLOW, stroke_width=4)
        cuv_lbl = lab("tube of extract", 24, BLUE).move_to([-4.2, -2.1, 0])
        self.play(FadeIn(cuv), FadeIn(lamp), FadeIn(det), FadeIn(beam1), FadeIn(beam2), FadeIn(cuv_lbl), run_time=0.8)

        # axes for the trace
        ax_o = np.array([0.0, -1.7])
        ax_w, ax_h = 5.6, 3.4
        xa = Line([ax_o[0], ax_o[1], 0], [ax_o[0] + ax_w, ax_o[1], 0], color=GREY, stroke_width=3)
        ya = Line([ax_o[0], ax_o[1], 0], [ax_o[0], ax_o[1] + ax_h, 0], color=GREY, stroke_width=3)
        xl = lab("time", 24, GREY).next_to(xa, DOWN, buff=0.12)
        yl = lab("absorbance at 340 nm", 24, YELLOW).move_to([ax_o[0] + 2.9, ax_o[1] + ax_h + 0.35, 0])
        ts = np.linspace(0, 1, 60)
        curve = poly([[ax_o[0] + 0.15 + ax_w * 0.92 * t, ax_o[1] + 0.2 + (ax_h - 0.4) * np.exp(-3.0 * t)] for t in ts], YELLOW, 5)

        self.at("Lactate dehydrogenase")
        ldh = chip("lactate dehydrogenase", BLUE, 24).move_to([-4.2, 2.6, 0])
        self.play(FadeIn(ldh, shift=DOWN * 0.1), run_time=0.5)
        self.at("consumes")
        nadh = chip("NADH", YELLOW, 26).move_to([-4.2, 1.75, 0])
        self.play(FadeIn(nadh, shift=DOWN * 0.1), run_time=0.5)
        self.at("which absorbs light")
        tag340 = lab("NADH absorbs light at 340 nm", 24, YELLOW).move_to([-3.9, -2.65, 0])
        self.play(FadeOut(cuv_lbl), FadeIn(tag340), run_time=0.4)
        self.at("at 340")
        self.play(Create(xa), Create(ya), FadeIn(xl), FadeIn(yl), run_time=0.7)
        self.at("does not")
        nad = chip("NAD+", GREY, 26)
        nad.move_to([-4.2, 1.75, 0])
        self.play(Transform(nadh, nad), FadeIn(lab("NAD+ does not", 24, GREY).move_to([-1.9, 1.75, 0])), run_time=0.5)
        self.at("so absorbance falls")
        liq = cuv[1]
        faded = liq.copy().set_fill(opacity=0.04)
        self.play(Create(curve, run_time=1.6, rate_func=linear), Transform(liq, faded, run_time=1.6, rate_func=linear))

        # ---------- homogenate and spins
        self.at("Then break the cells")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        head2 = T("break the cells, then spin", 34, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        xs = [-5.1, -1.7, 1.7, 5.1]
        h = 2.6
        base_y = -0.4
        tubes = []
        lblx = []
        spec = [("homogenate", None), ("gentle spin", "nuclei"), ("harder", "mitochondria"), ("harder still", "smallest vesicles")]
        t0 = tube(xs[0], base_y, w=1.3, h=h, level=0.8, fop=0.2)
        d0 = crowd(30, xs[0] - 0.5, xs[0] + 0.5, base_y - 1.0, base_y + 0.7, 9, 0.09)
        l0 = lab("homogenate", 24, GREY).move_to([xs[0], base_y - h / 2 - 0.4, 0])
        self.play(FadeIn(head2), FadeIn(t0), FadeIn(d0), FadeIn(l0), run_time=0.7)

        def stage(i, pellet_name, dots_left):
            tb = tube(xs[i], base_y, w=1.3, h=h, level=0.8, fop=0.2)
            pel = Rectangle(width=1.2, height=0.28 + 0.0, stroke_width=0, fill_color=GREYS[1], fill_opacity=0.95)
            pel.move_to([xs[i], base_y - h / 2 + 0.17, 0])
            dd = crowd(dots_left, xs[i] - 0.5, xs[i] + 0.5, base_y - 0.7, base_y + 0.8, 20 + i, 0.09)
            return tb, pel, dd

        prev = (t0, d0, l0)
        for i, (sp, nm) in enumerate(spec[1:], start=1):
            phrase = {1: "A gentle spin", 2: "a harder one mitochondria", 3: "the smallest vesicles"}[i]
            self.at(phrase)
            tb, pel, dd = stage(i, nm, [22, 14, 8][i - 1])
            a = arr([xs[i - 1] + 0.95, base_y], [xs[i] - 0.95, base_y], BLUE, 5, 0.2)
            spl = lab(sp, 24, BLUE).move_to([(xs[i - 1] + xs[i]) / 2, base_y + 0.45, 0])
            pl = lab(nm, 22, GREY)
            pl.move_to([xs[i], base_y - h / 2 - 0.4, 0])
            self.play(GrowArrow(a), FadeIn(spl), FadeIn(tb), FadeIn(dd), run_time=0.6)
            self.play(FadeIn(pel, shift=DOWN * 0.1), FadeIn(pl), run_time=0.5)
        self.wait(0.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Size(SpokenScene):
    """re-assay after each step; scoreboard; salt cut + dialysis; gel filtration (large first)."""

    def construct(self):
        sc = Score(5.4, -0.2, 3.2)
        sc_head = lab("after each step", 24, TEXT).move_to([5.4, 2.1, 0])
        CX = -2.3

        self.at("After each step")
        self.play(FadeIn(sc), FadeIn(sc_head), run_time=0.7)
        self.at("Specific activity is")
        f_top = chip("units of activity", GREEN, 34)
        f_bar = Line(LEFT * 2.6, RIGHT * 2.6, color=TEXT, stroke_width=4)
        f_bot = chip("milligrams of total protein", GREY, 34)
        frac = VGroup(f_top, f_bar, f_bot).arrange(DOWN, buff=0.3).move_to([-1.4, 0.2, 0])
        f_lbl = lab("specific activity =", 30, GREEN).next_to(frac, UP, buff=0.35)
        self.play(FadeIn(f_lbl), FadeIn(f_top, shift=DOWN * 0.1), Create(f_bar), run_time=0.7)
        self.at("milligrams of total")
        self.play(FadeIn(f_bot, shift=UP * 0.1), run_time=0.5)
        self.at("It rises when")
        self.play(sc.to(0.30, 0.82, 1.0))
        # ----- salting out
        self.at("Salting out uses solubility")
        self.play(FadeOut(f_lbl), FadeOut(frac), run_time=0.3)
        t = lab("salting out: solubility", 28, TEXT, weight=BOLD).move_to([CX, 2.3, 0])
        bk = tube(CX, -0.3, w=3.0, h=2.9, level=0.82, fop=0.16)
        rng = np.random.RandomState(31)
        greys = [dot(CX + rng.uniform(-1.2, 1.2), -0.2 + rng.uniform(-0.9, 1.0), 0.1, GREYS[i % 4], 0.85) for i in range(26)]
        targets = [dot(CX + rng.uniform(-1.0, 1.0), -0.2 + rng.uniform(-0.7, 0.9), 0.12, YELLOW, 1.0) for _ in range(4)]
        self.play(FadeIn(t), FadeIn(bk), *[FadeIn(d) for d in greys + targets], run_time=0.7)
        self.at("ammonium sulfate")
        salt = VGroup(*[dot(CX + rng.uniform(-1.3, 1.3), 0.9 + rng.uniform(0.0, 0.8), 0.06, TEALS, 1.0) for _ in range(14)])
        slab = lab("ammonium sulfate", 24, TEALS).move_to([CX + 3.0, 1.3, 0])
        self.play(FadeIn(salt, shift=DOWN * 0.3), FadeIn(slab), run_time=0.6)
        self.at("at different salt concentrations")
        # target + a few greys sink and pack at the bottom (the cut)
        drops = []
        floor = -1.55
        for k, d in enumerate(targets + greys[:5]):
            drops.append(d.animate.move_to([CX - 0.7 + 0.3 * (k % 5), floor + 0.18 * (k // 5), 0]))
        self.play(*drops, salt.animate.set_opacity(0.0), FadeOut(slab), run_time=1.2)
        self.at("leaving many contaminants")
        stay = lab("contaminants left behind", 24, GREY).move_to([CX, 1.75, 0])
        self.play(FadeIn(stay), *[d.animate.shift(UP * 0.0) for d in greys[5:]], run_time=0.5)
        self.play(sc.to(0.45, 0.70, 0.8))
        self.play(*[FadeOut(m) for m in [t, bk, stay] + greys + targets], run_time=0.5)
        # ----- gel filtration
        self.at("Gel filtration uses size")
        t_g = lab("gel filtration: size", 28, TEXT, weight=BOLD).move_to([CX, 2.3, 0])
        col_w, col_h = 1.5, 3.3
        col = Rectangle(width=col_w, height=col_h, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.07)
        col.move_to([CX, -0.2, 0])
        beads = VGroup()
        for r in range(7):
            for c in range(3):
                bx = CX - 0.5 + c * 0.5 + (0.25 if r % 2 else 0.0)
                if bx > CX + 0.72:
                    continue
                beads.add(Circle(radius=0.19, stroke_color=BLUE, stroke_width=2, fill_opacity=0).move_to([bx, 1.15 - r * 0.42, 0]))
        top = -0.2 + col_h / 2
        big = VGroup(*[dot(CX - 0.4 + 0.4 * i, top + 0.22, 0.17, YELLOW, 1.0) for i in range(3)])
        small = VGroup(*[dot(CX - 0.4 + 0.4 * i, top + 0.22 + 0.4, 0.07, GREYS[0], 1.0) for i in range(3)])
        self.play(FadeIn(t_g), FadeIn(col), FadeIn(beads), run_time=0.7)
        self.at("Large proteins cannot enter")
        lg_l = lab("large", 24, YELLOW).move_to([CX - 2.0, 1.2, 0])
        sm_l = lab("small", 24, GREY).move_to([CX - 2.0, 0.65, 0])
        self.play(FadeIn(big), FadeIn(small), FadeIn(lg_l), FadeIn(sm_l), run_time=0.5)
        self.play(big.animate.shift(DOWN * 0.3), small.animate.shift(DOWN * 0.3), run_time=0.3)
        self.at("so take the short path")
        bottom = -0.2 - col_h / 2
        pore_note = lab("pores: only small ones fit in", 22, GREY).move_to([CX + 3.0, 1.4, 0])
        self.play(FadeIn(pore_note), big.animate.move_to([CX, bottom - 0.45, 0]), run_time=0.9)
        first = lab("elute first", 24, YELLOW).move_to([CX + 2.0, bottom - 0.45, 0])
        self.play(FadeIn(first), run_time=0.3)
        self.at("Small ones come last")
        self.play(small.animate.move_to([CX, bottom - 0.45, 0]), run_time=1.2)
        lastl = lab("last", 24, GREY).move_to([CX - 1.5, bottom - 0.45, 0])
        self.play(FadeIn(lastl), sc.to(0.65, 0.55, 0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Charge(SpokenScene):
    """ion exchange (opposites stick, salt releases), affinity (bait beads), then which column first."""

    def construct(self):
        # restore the scoreboard where S03 left it
        sc2 = Score(5.6, 0.0, 3.2)
        sc2.fs[0].stretch_to_fit_height(3.2 * 0.65).move_to([sc2.ox[0], sc2.base + 3.2 * 0.65 / 2, 0])
        sc2.fs[1].stretch_to_fit_height(3.2 * 0.55).move_to([sc2.ox[1], sc2.base + 3.2 * 0.55 / 2, 0])
        self.add(sc2)
        sc = sc2

        # ----- ion exchange: two small panels
        self.at("Ion exchange uses charge")
        h1 = lab("ion exchange: charge", 28, TEXT, weight=BOLD).move_to([-2.0, 3.2, 0])
        self.play(FadeIn(h1), run_time=0.4)

        def bead_row(cx, cy, sign, color, n=5):
            g = VGroup()
            for i in range(n):
                b = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12)
                b.move_to([cx + (i - (n - 1) / 2) * 0.62, cy, 0])
                s = T(sign, 26, color, weight=BOLD).move_to(b)
                g.add(VGroup(b, s))
            return g

        PX = -4.2
        QX = 0.1
        beadsA = bead_row(PX, -1.6, "−", RED)
        beadsB = bead_row(QX, -1.6, "+", GREEN)
        self.play(FadeIn(beadsA), FadeIn(beadsB), run_time=0.6)
        la = lab("negative beads", 22, BLUE).move_to([PX, -2.35, 0])
        lb = lab("positive beads", 22, BLUE).move_to([QX, -2.35, 0])
        self.play(FadeIn(la), FadeIn(lb), run_time=0.4)
        self.at("opposite charges stick")
        # a yellow net-positive protein flies to negative beads
        pa = VGroup(dot(PX, 1.3, 0.24, YELLOW, 1.0), T("+", 26, BG, weight=BOLD).move_to([PX, 1.3, 0]))
        self.play(FadeIn(pa), run_time=0.3)
        self.play(pa.animate.move_to([PX + 0.0, -0.9, 0]), run_time=0.9)
        self.at("Below its")
        cA = chip("below pI: net positive", YELLOW, 22).move_to([PX, 2.2, 0])
        exA = chip("cation exchanger", BLUE, 22).move_to([PX, -3.0, 0])
        self.play(FadeIn(cA, shift=DOWN * 0.1), FadeIn(exA), run_time=0.5)
        self.at("Above it")
        pb = VGroup(dot(QX, 1.3, 0.24, YELLOW, 1.0), T("−", 26, BG, weight=BOLD).move_to([QX, 1.3, 0]))
        self.play(FadeIn(pb), run_time=0.3)
        self.play(pb.animate.move_to([QX, -0.9, 0]), run_time=0.9)
        cB = chip("above pI: net negative", YELLOW, 22).move_to([QX, 2.2, 0])
        exB = chip("anion exchanger", BLUE, 22).move_to([QX, -3.0, 0])
        self.play(FadeIn(cB, shift=DOWN * 0.1), FadeIn(exB), run_time=0.5)
        self.at("Raise the salt")
        salt = VGroup(*[dot(PX - 1.2 + 0.5 * i, 0.4 + 0.15 * (i % 2), 0.07, TEALS, 1.0) for i in range(6)])
        salt2 = salt.copy().shift(RIGHT * (QX - PX))
        sl = lab("salt up, or shift the pH", 24, TEALS).move_to([-2.0, -0.2, 0])
        self.play(FadeIn(salt), FadeIn(salt2), FadeIn(sl), run_time=0.5)
        self.play(pa.animate.move_to([PX, 0.7, 0]), pb.animate.move_to([QX, 0.7, 0]), run_time=1.0)
        self.play(sc.to(0.80, 0.42, 0.8))

        # ----- affinity
        self.at("Affinity uses beads")
        self.play(*[FadeOut(m) for m in [h1, beadsA, beadsB, la, lb, pa, pb, cA, cB, exA, exB, salt, salt2, sl]], run_time=0.5)
        h2 = lab("affinity: what only the target recognizes", 28, TEXT, weight=BOLD).move_to([-1.0, 3.2, 0])
        col = Rectangle(width=1.7, height=3.4, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.07).move_to([-1.0, -0.1, 0])
        bait = VGroup()
        for r in range(6):
            for c in range(3):
                bx = -1.5 + c * 0.5 + (0.22 if r % 2 else 0.0)
                by = 1.2 - r * 0.5
                b = Circle(radius=0.2, stroke_color=BLUE, stroke_width=2, fill_opacity=0).move_to([bx, by, 0])
                k = Square(side_length=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1.0).move_to([bx, by + 0.24, 0])
                bait.add(VGroup(b, k))
        self.play(FadeIn(h2), FadeIn(col), FadeIn(bait), run_time=0.7)
        bl = lab("bait", 24, ORANGE).move_to([-3.2, 1.0, 0])
        self.play(FadeIn(bl))
        self.at("The target binds")
        tgt = VGroup(*[dot(-1.5 + 0.5 * i, 2.35, 0.14, YELLOW, 1.0) for i in range(3)])
        gry = VGroup(*[dot(-1.5 + 0.5 * i + 0.25, 2.75, 0.1, GREYS[i % 4], 0.9) for i in range(3)] +
                     [dot(-1.5 + 0.5 * i, 2.75, 0.1, GREYS[(i + 2) % 4], 0.9) for i in range(3)])
        self.play(FadeIn(tgt), FadeIn(gry), run_time=0.4)
        self.play(tgt.animate.move_to([-1.0, 0.45, 0]).arrange(RIGHT, buff=0.5).move_to([-1.0, 0.45, 0]), run_time=0.7)
        self.at("the rest flows through")
        self.play(gry.animate.move_to([-1.0, -3.3, 0]).arrange(RIGHT, buff=0.12).move_to([-1.0, -3.35, 0]), run_time=0.9)
        thru = lab("flows through", 24, GREY).move_to([2.2, -3.0, 0])
        self.play(FadeIn(thru), run_time=0.3)
        self.at("free ligand displaces it")
        free = VGroup(*[Square(side_length=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=1.0).move_to([-1.0 - 0.6 + 0.4 * i, 2.5, 0])
                        for i in range(4)])
        fl = lab("free ligand", 24, ORANGE).move_to([2.2, 2.3, 0])
        self.play(FadeIn(free), FadeIn(fl), run_time=0.4)
        self.play(free.animate.move_to([-1.0, 0.5, 0]), run_time=0.5)
        self.play(tgt.animate.move_to([-1.0, -2.1, 0]), FadeOut(free), run_time=0.7)
        self.play(sc.to(0.92, 0.30, 0.8))

        # ----- which column first
        self.at("If you know a binding partner")
        self.play(*[FadeOut(m) for m in [h2, col, bait, bl, tgt, gry, thru, fl, sc]], run_time=0.6)
        hh = lab("which column first?", 34, TEXT, weight=BOLD).move_to([0, 1.8, 0])
        rows = [("you know a binding partner", "affinity", ORANGE)]
        grp = []
        for i, (know, col_, c) in enumerate(rows):
            k = chip(know, GREY, 28)
            a = arr([0, 0], [1.2, 0], GREY, 5, 0.2)
            r = chip(col_, c, 30)
            row = VGroup(k, a, r).arrange(RIGHT, buff=0.35)
            row.move_to([0, 1.3 - i * 1.5, 0])
            grp.append(row)
        grp[0].move_to([0, 0.3, 0])
        self.play(FadeIn(hh), FadeIn(grp[0], shift=RIGHT * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Table(SpokenScene):
    """an idealised purification table, then the real Benovic run."""

    def construct(self):
        self.at("Read the purification table")
        head = T("the purification table", 34, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        tag = chip("Idealised example", GOLD, 24).move_to([4.7, 3.25, 0])
        self.play(FadeIn(head), FadeIn(tag), run_time=0.5)
        cx = [-2.4, 1.2, 4.4]
        colh = ["total protein", "total activity", "specific activity"]
        colc = [GREY, RED, GREEN]
        hdrs = [lab(t, 24, c).move_to([x, 2.4, 0]) for t, c, x in zip(colh, colc, cx)]
        ry = [1.3, -0.1, -1.5]
        rl = [lab("crude extract", 24, TEXT), lab("later steps", 24, TEXT), lab("final step", 24, TEXT)]
        for r, y in zip(rl, ry):
            r.move_to([-5.7 + r.width / 2, y, 0])
        hl = Line([-6.3, 2.0, 0], [6.3, 2.0, 0], color=GREY, stroke_width=2)
        self.play(Create(hl), *[FadeIn(h) for h in hdrs], FadeIn(rl[0]), FadeIn(rl[1]), FadeIn(rl[2]), run_time=0.8)
        # total protein / total activity bars; specific activity numbers
        Wb = 2.2
        fr_p = [1.0, 0.45, 0.12]
        fr_a = [1.0, 0.62, 0.33]
        bp, ba = [], []
        for i, y in enumerate(ry):
            o1, f1 = bar(cx[0] - Wb / 2, y, Wb, 0.34, fr_p[i], GREY)
            o2, f2 = bar(cx[1] - Wb / 2, y, Wb, 0.34, fr_a[i], RED)
            bp.append(VGroup(o1, f1))
            ba.append(VGroup(o2, f2))
        self.at("both fall")
        self.play(FadeIn(bp[0]), FadeIn(ba[0]), run_time=0.4)
        self.play(FadeIn(bp[1]), FadeIn(ba[1]), FadeIn(bp[2]), FadeIn(ba[2]), run_time=0.7)
        pct = M("100%", 24, BG, weight=BOLD).move_to([cx[1], ry[0], 0])
        self.play(FadeIn(pct), run_time=0.2)
        self.at("some enzyme with it")
        lost = lab("protein lost, and some enzyme with it", 24, RED).move_to([0.0, -2.35, 0])
        self.play(FadeIn(lost, shift=UP * 0.1), run_time=0.5)
        self.at("Specific activity should rise")
        s0 = M("10 units/mg", 26, GREEN).move_to([cx[2], ry[0], 0])
        s1 = M("···", 30, GREEN).move_to([cx[2], ry[1], 0])
        s2 = M("30,000 units/mg", 26, GREEN).move_to([cx[2], ry[2], 0])
        self.play(FadeOut(lost), FadeIn(s0), run_time=0.4)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        self.at("fold purification")
        ex1 = chip("10 → 30,000 units/mg: 3,000-fold", GREEN, 26).move_to([0, -3.0, 0])
        self.play(FadeIn(ex1, shift=UP * 0.1), run_time=0.6)
        self.at("roughly a third")
        ex2 = chip("last row: yield about a third", RED, 24).move_to([1.2, -2.2, 0])
        self.play(FadeOut(ex1), FadeIn(ex2), run_time=0.5)

        # ----- real case
        self.at("real run")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        h2 = T("the real case", 34, TEXT, weight=BOLD).move_to([-3.8, 3.25, 0])
        src = chip("Benovic 1987", GOLD, 24).move_to([3.0, 3.25, 0])
        self.play(FadeIn(h2), FadeIn(src), run_time=0.5)
        names = ["gel filtration", "DEAE-Sephacel", "CM-Fractogel", "hydroxylapatite"]
        chips = [chip(n, BLUE, 24) for n in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.35).move_to([0, 1.6, 0])
        fit(row, 12.4)
        self.at("four columns gave")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.2), run_time=0.45)
        # bars: fold and recovery
        fo, ff = bar(-2.6, -0.2, 5.2, 0.45, 0.02, GREEN)
        ro, rf = bar(-2.6, -1.55, 5.2, 0.45, 1.0, RED)
        fl = lab("fold purification", 24, GREEN).move_to([0, 0.4, 0])
        rl2 = lab("activity recovered", 24, RED).move_to([0, -0.95, 0])
        self.play(FadeIn(fo), FadeIn(ff), FadeIn(ro), FadeIn(rf), FadeIn(fl), FadeIn(rl2), run_time=0.2)
        self.at("columns gave about")
        f_new = Rectangle(width=5.2, height=0.45, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([0, -0.2, 0])
        self.play(Transform(ff, f_new), run_time=0.6)
        f_lab2 = M("~20,000-fold", 30, BG, weight=BOLD).move_to([0, -0.2, 0])
        self.play(FadeIn(f_lab2), run_time=0.3)
        self.at("with 12")
        r_new = Rectangle(width=5.2 * 0.12, height=0.45, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([-2.6 + 5.2 * 0.06, -1.55, 0])
        r_lab = M("12%", 30, RED).move_to([0, -2.2, 0])
        self.play(Transform(rf, r_new), FadeIn(r_lab), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfall(SpokenScene):
    """purer is not safer: arrestin goes missing; the cure is to test the effect and track total activity."""

    def construct(self):
        self.at("Purity can strip away")
        head = T("purer fraction, missing partner", 34, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(head), run_time=0.5)
        LX = -4.0
        BX0 = 0.9
        BW = 4.6
        # row A
        yA, yB = 1.25, -1.25
        kA = chip("kinase", BLUE, 28).move_to([LX - 1.2, yA, 0])
        aA = chip("arrestin (inferred)", PURPLE, 26).move_to([LX + 1.3, yA, 0])
        tA = lab("purified only 350-fold", 24, GREY).move_to([LX - 0.2, yA + 0.9, 0])
        oA, fA = bar(BX0, yA, BW, 0.5, 1.0, GREEN)
        gA = lab("G-protein activation", 22, GREEN).move_to([BX0 + BW / 2, yA + 0.62, 0])
        self.at("kinase batch")
        self.play(FadeIn(kA), FadeIn(aA), FadeIn(tA), FadeIn(oA), FadeIn(fA), FadeIn(gA), run_time=0.8)
        self.at("by up to")
        nA = Rectangle(width=BW * 0.2, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([BX0 + BW * 0.1, yA, 0])
        cutA = lab("up to 80%", 24, RED).move_to([BX0 + BW / 2 + 0.9, yA - 0.62, 0])
        self.play(Transform(fA, nA), FadeIn(cutA), run_time=0.9)
        # row B
        kB = chip("kinase", BLUE, 28).move_to([LX - 1.2, yB, 0])
        aB = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=aA.width, height=aA.height, stroke_color=PURPLE, stroke_width=2.5)
                            .move_to([LX + 1.3, yB, 0]), num_dashes=30)
        aBl = T("arrestin", 26, PURPLE).move_to([LX + 1.3, yB, 0]).set_opacity(0.35)
        tB = lab("purified 20,000-fold", 24, GREY).move_to([LX - 0.2, yB + 0.9, 0])
        oB, fB = bar(BX0, yB, BW, 0.5, 1.0, GREEN)
        gB = lab("G-protein activation", 22, GREEN).move_to([BX0 + BW / 2, yB + 0.62, 0])
        self.at("pure enzyme cut")
        self.play(FadeIn(kB), FadeIn(tB), FadeIn(oB), FadeIn(fB), FadeIn(gB), run_time=0.7)
        self.at("far less")
        nB = Rectangle(width=BW * 0.96, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([BX0 + BW * 0.48, yB, 0])
        cutB = lab("cut much less", 24, GREEN).move_to([BX0 + BW / 2 + 0.7, yB - 0.62, 0])
        self.play(Transform(fB, nB), FadeIn(cutB), run_time=0.9)
        self.at("because a second protein")
        gone = VGroup(aB, aBl)
        self.play(FadeIn(gone), run_time=0.5)
        why = lab("arrestin: apparently removed", 24, PURPLE).move_to([LX + 1.0, yB - 0.65, 0])
        self.play(FadeIn(why), run_time=0.4)
        # controls
        self.at("So test the pure fraction")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head], run_time=0.6)
        c1 = chip("test the pure fraction on the effect", GREEN, 32).move_to([0, 0.2, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Origins(SpokenScene):
    """Sumner's crystals (1926) and Collip's alcohol steps (1922)."""

    def construct(self):
        LX, RX = -3.4, 3.4
        # ---------- Sumner
        self.at("In 1926")
        hs = T("Sumner, 1926", 30, GOLD, weight=BOLD).move_to([LX, 3.2, 0])
        bean = tube(LX - 2.0, 0.6, w=1.2, h=1.9, fill=GREY, level=0.8, fop=0.3)
        bean_l = T("jack bean\nextract", 22, GREY).move_to([LX - 2.0, 2.0, 0])
        self.play(FadeIn(hs), FadeIn(bean), FadeIn(bean_l), run_time=0.7)
        self.at("Sumner crystallized urease")
        cr = tube(LX + 0.4, 0.6, w=1.2, h=1.9, fill=GREY, level=0.55, fop=0.1)
        crys = VGroup(*[Square(side_length=0.2, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.5)
                        .rotate(0.5 * i).move_to([LX + 0.4 + (i % 3 - 1) * 0.3, -0.25 + (i // 3) * 0.28, 0]) for i in range(6)])
        cr_l = lab("urease crystals", 22, YELLOW).move_to([LX + 0.4, 1.9, 0])
        ar = arr([LX - 1.25, 0.6], [LX - 0.4, 0.6], GREY, 4, 0.18)
        self.play(GrowArrow(ar), FadeIn(cr), FadeIn(crys), FadeIn(cr_l), run_time=1.0)
        self.at("Dissolved")
        dis = tube(LX + 2.4, 0.6, w=1.2, h=1.9, fill=YELLOW, level=0.55, fop=0.25)
        dis_l = lab("in water", 22, BLUE).move_to([LX + 2.4, 1.9, 0])
        ar2 = arr([LX + 1.05, 0.6], [LX + 1.8, 0.6], GREY, 4, 0.18)
        self.play(GrowArrow(ar2), FadeIn(dis), FadeIn(dis_l), run_time=0.8)
        r1 = chip("protein tests: positive", GREEN, 22).move_to([LX + 0.2, -1.5, 0])
        r2 = chip("urease activity: very high", YELLOW, 22).move_to([LX + 0.2, -2.35, 0])
        self.at("tests for protein")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("very high urease activity")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("Enzymes can be proteins")
        r3 = chip("enzymes can be proteins", TEXT, 22).move_to([LX, -3.2, 0])
        fit(r3, 6.0)
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.6)
        # ---------- Collip
        self.at("In January")
        div = Line([0, 3.4, 0], [0, -3.4, 0], color=GREY, stroke_width=1.5)
        hc = T("Collip, 1922", 30, GOLD, weight=BOLD).move_to([RX, 3.2, 0])
        self.play(Create(div), FadeIn(hc), run_time=0.5)
        self.at("raised alcohol")
        lvls = [0.25, 0.5, 0.8]
        bks = VGroup()
        for i, lv in enumerate(lvls):
            b = tube(RX - 2.0 + i * 1.3, 0.6, w=1.0, h=1.9, fill=TEALS, level=lv, fop=0.35)
            bks.add(b)
        al = lab("alcohol, in steps up", 22, TEALS).move_to([RX - 0.7, 1.9, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bks], lag_ratio=0.3), FadeIn(al), run_time=1.2)
        self.at("pure form")
        vial = tube(RX + 2.1, 0.6, w=1.0, h=1.9, fill=YELLOW, level=0.5, fop=0.35)
        ar3 = arr([RX + 0.8, 0.6], [RX + 1.45, 0.6], GREY, 4, 0.18)
        vl = lab("insulin, semipure", 22, YELLOW).move_to([RX + 2.1, 1.9, 0])
        self.play(GrowArrow(ar3), FadeIn(vial), FadeIn(vl), run_time=0.8)
        self.at("Leonard Thompson")
        worked = chip("his extract worked in Leonard Thompson", GREEN, 22).move_to([RX, -2.35, 0])
        fit(worked, 6.0)
        self.play(FadeIn(worked, shift=UP * 0.1), run_time=0.5)
        self.at("Purification made insulin")
        drug = chip("purification made it a drug", GOLD, 24).move_to([RX, -3.2, 0])
        self.play(FadeIn(drug, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Unlocked(SpokenScene):
    """Cohen's EGF column (the receptor is an enzyme); PDK1 needs its lipid; the rule."""

    def construct(self):
        LX, RX = -3.5, 3.5
        self.at("Stanley Cohen's group")
        hc = T("Cohen's group, Nobel lecture 1986", 24, GOLD, weight=BOLD).move_to([-3.4, 3.3, 0])
        col = Rectangle(width=1.2, height=2.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.07).move_to([-5.4, 0.9, 0])
        bait = VGroup(*[Square(side_length=0.13, stroke_width=0, fill_color=ORANGE, fill_opacity=1.0)
                        .move_to([-5.4 - 0.35 + (i % 3) * 0.35, 0.2 + (i // 3) * 0.5, 0]) for i in range(9)])
        col_l = lab("EGF on the beads", 22, ORANGE).move_to([-5.0, 2.45, 0])
        self.play(FadeIn(hc), FadeIn(col), FadeIn(bait), FadeIn(col_l), run_time=0.8)
        self.at("Receptor, kinase")
        ar = arr([-4.6, 1.0], [-4.05, 1.0], GREY, 4, 0.16)
        gel = Rectangle(width=1.3, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([-3.3, 1.0, 0])
        faint = VGroup(*[Rectangle(width=0.9, height=0.06, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([-3.3, y, 0])
                         for y in (1.6, 1.35, 0.6, 0.4)])
        strong = Rectangle(width=0.9, height=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1.0).move_to([-3.3, 1.0, 0])
        kd = lab("150 kDa", 22, YELLOW).move_to([-2.0, 1.0, 0])
        tog = T("receptor, kinase,\nsubstrate together", 22, YELLOW).move_to([-3.3, -0.6, 0])
        self.play(GrowArrow(ar), FadeIn(gel), FadeIn(faint), FadeIn(strong, scale=1.4), FadeIn(kd), FadeIn(tog), run_time=0.9)
        self.at("the kinase phosphorylated tyrosine")
        tyr = chip("tyrosine", GREY, 24).move_to([-0.9, -0.5, 0])
        badge = Circle(radius=0.2, stroke_width=0, fill_color=GREEN, fill_opacity=1.0).next_to(tyr, UR, buff=-0.12)
        bt = T("P", 22, BG, weight=BOLD).move_to(badge)
        self.play(FadeIn(tyr), run_time=0.3)
        self.play(FadeIn(badge, scale=0.4), FadeIn(bt), run_time=0.4)
        self.at("later showed")
        rc = chip("receptor", BLUE, 24)
        kc = chip("kinase", BLUE, 24)
        link = Line(LEFT * 0.3, RIGHT * 0.3, color=ORANGE, stroke_width=5)
        joined = VGroup(rc, link, kc).arrange(RIGHT, buff=0.1).move_to([-3.2, -1.8, 0])
        atp = chip("ATP analogue label, later", ORANGE, 22).move_to([-3.2, -2.8, 0])
        self.play(FadeIn(joined, shift=UP * 0.1), FadeIn(atp), run_time=0.7)
        self.at("is the kinase")
        self.play(link.animate.set_color(GREEN).set_stroke(width=8), run_time=0.4)

        self.at("In 1997")
        div = Line([0.3, 3.5, 0], [0.3, -2.9, 0], color=GREY, stroke_width=1.5)
        ha = T("Alessi et al., 1997", 24, GOLD, weight=BOLD).move_to([3.4, 3.3, 0])
        self.play(Create(div), FadeIn(ha), run_time=0.4)
        self.at("Alessi, Cohen and colleagues")
        k = chip("kinase, 500,000-fold", BLUE, 22).move_to([2.0, 2.3, 0])
        self.play(FadeIn(k, shift=DOWN * 0.1), run_time=0.5)
        self.at("colleagues purified")
        self.at("It activates Akt")
        akt = chip("Akt", GREY, 28).move_to([5.5, 2.3, 0])
        a2 = arr([3.85, 2.3], [4.7, 2.3], GREY, 4, 0.18)
        self.play(GrowArrow(a2), FadeIn(akt), run_time=0.6)
        self.at("only with certain lipids")
        lip1 = chip("lipid", ORANGE, 22)
        lip2 = chip("lipid", ORANGE, 22)
        lip = VGroup(lip1, lip2).arrange(RIGHT, buff=0.3).move_to([3.5, 0.9, 0])
        self.play(FadeIn(lip, shift=DOWN * 0.1), run_time=0.5)
        on = chip("Akt activated", GREEN, 24).move_to([3.5, -0.4, 0])
        self.play(Transform(akt, chip("Akt", GREEN, 28).move_to([5.5, 2.3, 0])), FadeIn(on), run_time=0.7)
        self.at("which a purified system")
        pur = lab("a purified system can test it", 22, TEXT).move_to([3.5, -1.6, 0])
        self.play(FadeIn(pur), run_time=0.5)
        self.at("A pure fraction")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        rule = Text("A pure fraction speaks only\nfor the assay you followed.\nTest it on the biological effect.",
                    font=FONT, font_size=40, color=GOLD, line_spacing=0.9)
        box = SurroundingRectangle(rule, color=GOLD, buff=0.45, corner_radius=0.2, stroke_width=3)
        self.play(Create(box), FadeIn(rule, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A pure fraction speaks only for the assay you followed."
