"""One receptor gene, chosen in steps  (Biochemistrypedia explainer, Sensory Systems)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a receptor gene (a small tile) before it is chosen; also "a different receptor" in the tracing sketch
  RED    = repressive marks, silencing, heterochromatin, "unidentified"
  GREEN  = the chosen, active gene / copy; the stable endpoint
  TEAL   = enhancers and enhancer hubs
  ORANGE = receptor RNA / receptor expressed
  PURPLE = the stress pathway and its feedback (PERK, ATF5, Adcy3)
  GOLD   = the lineage mark (a ring); title rule
  GREY   = nucleus, chromosomes, outlines, labels
Everything is a labelled schematic. Tiles are genes; the counts drawn are not data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.06
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def tile(color=BLUE, s=0.46, op=0.35):
    return RoundedRectangle(corner_radius=0.08, width=s, height=s, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=op)


def dot(color=RED, r=0.08):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def mark_on(t):
    return dot().move_to(t.get_corner(UR) + np.array([-0.02, -0.02, 0]))


def nucleus(w=11.2, h=4.9, y=0.05):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([0, y, 0])


def grid_pos():
    pts = []
    for r in range(7):
        y = 0.05 + (r - 3) * 0.6
        for c in range(13):
            x = (c - 6) * 0.78
            if (x / 5.0) ** 2 + ((y - 0.05) / 2.0) ** 2 <= 1.0:
                pts.append((x, y))
    return pts


GRID = grid_pos()
CHOSEN = min(range(len(GRID)), key=lambda i: (GRID[i][0] - 0.8) ** 2 + (GRID[i][1] - 0.3) ** 2)


def make_tiles():
    ts = [tile().move_to([x, y, 0]) for (x, y) in GRID]
    return ts


def head(text, y=3.2, size=26):
    return T(text, size, GREY).move_to([0, y, 0])


class S00Title(TitleCard):
    LESSON = "One receptor per neuron"
    TITLE = "One Receptor Gene, Chosen in Steps"


# ---------------------------------------------------------------------------------------------
class S01Choice(SpokenScene):
    """a thousand tiles, one lights up, one copy of it, then the question."""

    def construct(self):
        nuc = nucleus()
        hd = head("Inside one mouse olfactory neuron")
        ts = make_tiles()
        tg = VGroup(*ts)
        lab = T("about a thousand receptor genes (a few drawn)", 24, BLUE).move_to([0, -3.0, 0])
        self.play(FadeIn(hd), FadeIn(nuc), run_time=0.5)
        self.at("carries about")
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in ts], lag_ratio=0.02), FadeIn(lab), run_time=2.0)

        self.at("just one gene")
        ch = ts[CHOSEN]
        lab2 = T("a mature neuron: one gene transcribed", 24, GREEN).move_to([0, -3.0, 0])
        self.play(ch.animate.set_stroke(GREEN).set_fill(GREEN, 0.7).scale(1.35), FadeOut(lab), FadeIn(lab2), run_time=0.7)
        self.play(Indicate(ch, color=GREEN, scale_factor=1.5), run_time=0.7)

        self.at("just one copy")
        tg.save_state()
        nuc.save_state()
        bar1 = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.1, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.5).move_to([-2.7, 0.5, 0])
        bar2 = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.1, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.18).move_to([2.7, 0.5, 0])
        l1 = T("this copy: transcribed", 26, GREEN).next_to(bar1, DOWN, buff=0.3)
        l2 = T("other copy: not transcribed", 26, GREY).next_to(bar2, DOWN, buff=0.3)
        zt = T("the same gene, two copies", 26, TEXT).move_to([0, 1.7, 0])
        self.play(FadeOut(lab2), tg.animate.set_opacity(0), nuc.animate.set_stroke(opacity=0.2).set_fill(opacity=0.0), run_time=0.5)
        self.play(FadeIn(bar1), FadeIn(bar2), FadeIn(l1), FadeIn(l2), FadeIn(zt), run_time=0.8)

        self.at("singular choice")
        sc = bchip("singular choice", GOLD, 32).move_to([0, -1.5, 0])
        self.play(FadeIn(sc, scale=0.9), run_time=0.6)

        self.at("How does a cell")
        q = T("?", 160, YELLOW, weight=BOLD).move_to([0, 0.1, 0])
        self.play(FadeOut(VGroup(bar1, bar2, l1, l2, zt, sc)), Restore(tg), Restore(nuc), run_time=0.6)
        self.play(FadeIn(q, scale=0.6), tg.animate.set_stroke(opacity=0.3).set_fill(opacity=0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Silence(SpokenScene):
    """marks land on nearly every tile; one stays open; heterochromatin; silencing before expression."""

    def construct(self):
        nuc = nucleus()
        hd = head("Inside one mouse olfactory neuron")
        ts = make_tiles()
        tg = VGroup(*ts)
        self.add(nuc, hd, tg)
        self.wait(0.3)

        self.at("Start with silence")
        t0 = T("silence comes first", 28, RED).move_to([0, -3.0, 0])
        self.play(FadeIn(t0), run_time=0.4)

        self.at("chained shut")
        dots = [mark_on(t) for i, t in enumerate(ts) if i != CHOSEN]
        anims = [t.animate.set_stroke(RED).set_fill(RED, 0.25) for i, t in enumerate(ts) if i != CHOSEN]
        self.play(LaggedStart(*[AnimationGroup(a, FadeIn(d, scale=0.3)) for a, d in zip(anims, dots)], lag_ratio=0.012),
                  run_time=1.2)

        self.at("one is left open")
        ch = ts[CHOSEN]
        self.play(ch.animate.set_stroke(GREEN).set_fill(GREEN, 0.7).scale(1.35), run_time=0.5)
        self.play(Indicate(ch, color=GREEN, scale_factor=1.5), run_time=0.7)

        self.at("repressive marks")
        leg = VGroup(dot(RED, 0.11), T("repressive mark", 24, RED)).arrange(RIGHT, buff=0.2).move_to([4.55, 2.7, 0])
        self.play(FadeIn(leg), FadeOut(t0), run_time=0.5)

        self.at("heterochromatin")
        het = bchip("heterochromatin: tightly packed, silenced", RED, 26).move_to([0, -3.0, 0])
        self.play(FadeIn(het, shift=UP * 0.1), run_time=0.5)
        self.play(*[t.animate.scale(0.9) for i, t in enumerate(ts) if i != CHOSEN], run_time=0.6)
        self.play(*[t.animate.scale(1 / 0.9) for i, t in enumerate(ts) if i != CHOSEN], run_time=0.4)

        self.at("The data")
        a = bchip("silencing", RED, 26).move_to([-3.4, -3.0, 0])
        self.play(FadeOut(het), FadeIn(a), run_time=0.5)
        self.at("comes before")
        b = bchip("expression detectable", GREEN, 26).move_to([2.6, -3.0, 0])
        ar = arr(a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05, GREY)
        self.play(GrowArrow(ar), run_time=0.5)
        self.at("expression can be")
        self.play(FadeIn(b, scale=0.9), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Compare(SpokenScene):
    """P2: active copy with fewer marks than its partner; a comparison, not a cause."""

    def construct(self):
        hd = head("Receptor P2 in sorted mouse olfactory neurons", y=3.4)
        self.play(FadeIn(hd), run_time=0.5)
        W = 4.6
        bx_a, bx_b, by = -3.3, 3.3, 1.5
        act = RoundedRectangle(corner_radius=0.14, width=W, height=0.9, stroke_color=GREEN, stroke_width=4,
                               fill_color=GREEN, fill_opacity=0.45).move_to([bx_a, by, 0])
        ina = RoundedRectangle(corner_radius=0.14, width=W, height=0.9, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([bx_b, by, 0])
        la = T("active P2 copy", 28, GREEN).next_to(act, DOWN, buff=0.22)
        lb = T("inactive partner copy", 28, BLUE).next_to(ina, DOWN, buff=0.22)

        def marks(cx, n):
            xs = np.linspace(cx - W / 2 + 0.45, cx + W / 2 - 0.45, 8)
            return VGroup(*[dot(RED, 0.13).move_to([xs[k], by + 0.68, 0]) for k in range(n)])

        ma, mb = marks(bx_a, 2), marks(bx_b, 7)

        self.at("mouse neurons labeled")
        self.play(FadeIn(act), FadeIn(ina), FadeIn(la), FadeIn(lb), run_time=0.8)

        self.at("the active copy")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in ma], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d in mb], lag_ratio=0.12), run_time=2.0)
        key = VGroup(dot(RED, 0.11), T("repressive mark (in this sketch)", 22, RED)).arrange(RIGHT, buff=0.2).move_to([0, 2.8, 0])
        self.play(FadeIn(key), run_time=0.4)

        self.at("So the chosen copy")
        less = bchip("chosen copy: less repressed", GREEN, 28).move_to([0, -0.45, 0])
        self.play(FadeIn(less, shift=UP * 0.1), run_time=0.6)

        self.at("only a comparison")
        cmp_ = T("a comparison of two copies", 24, GREY).move_to([0, -1.15, 0])
        self.play(FadeIn(cmp_), run_time=0.5)

        row = VGroup(*[tile(RED, 0.5, 0.25).move_to([-5.0 + 1.0 * k, -2.0, 0]) for k in range(11)])
        rd = VGroup(*[mark_on(t) for t in row])
        rl = T("the other receptor genes", 26, RED).move_to([0, -2.85, 0])
        self.at("silenced the others")
        start = np.array([-5.0, by - 0.5, 0])
        end = np.array([-5.0, -1.55, 0])
        path = DashedLine(start, end, color=GREY, stroke_width=5, dash_length=0.18)
        tipp = arr(end + UP * 0.3, end, GREY)
        x = VGroup(Line([-5.35, -0.85, 0], [-4.65, -0.15, 0], color=RED, stroke_width=8),
                   Line([-5.35, -0.15, 0], [-4.65, -0.85, 0], color=RED, stroke_width=8))
        self.play(FadeIn(row), FadeIn(rd), FadeIn(rl), run_time=0.6)
        self.play(Create(path), GrowArrow(tipp), run_time=0.6)
        self.play(FadeIn(x, scale=0.5), run_time=0.4)

        self.at("already there")
        al = T("already silenced", 26, RED, weight=BOLD).move_to([0, -2.85, 0])
        self.play(Transform(rl, al), Indicate(row, color=RED, scale_factor=1.06), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Hubs(SpokenScene):
    """enhancers on different chromosomes meet in hubs; hubs compete; one wins; its RNA suppresses rivals."""

    def construct(self):
        nuc = Ellipse(width=11.8, height=5.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([0, -0.1, 0])
        HX = [-3.2, 0.0, 3.2]
        caps, genes, enhs = [], [], []
        for hx in HX:
            for cy in (1.75, -1.95):
                cap = RoundedRectangle(corner_radius=0.16, width=2.0, height=0.32, stroke_color=GREY, stroke_width=3,
                                       fill_color=GREY, fill_opacity=0.35).move_to([hx, cy, 0])
                g = tile(BLUE, 0.34, 0.45).move_to([hx - 0.5, cy, 0])
                e = Circle(radius=0.17, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.85).move_to([hx + 0.5, cy, 0])
                caps.append(cap); genes.append(g); enhs.append(e)
        capg = VGroup(*caps)
        hd = head("a developing mouse olfactory neuron (schematic)", y=3.3)
        note = T("six chromosomes drawn; clusters come from 18", 22, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(hd), FadeIn(nuc), run_time=0.4)
        self.play(FadeIn(capg), *[FadeIn(g) for g in genes], *[FadeIn(e) for e in enhs], FadeIn(note), run_time=0.7)

        gl_ = T("gene", 24, BLUE).move_to([genes[1].get_center()[0] - 0.2, genes[1].get_center()[1] + 0.55, 0])
        self.play(FadeIn(gl_), run_time=0.3)
        self.at("An enhancer is")
        el = T("enhancer", 26, TEAL).move_to([enhs[1].get_center() + np.array([1.3, 0.55, 0])])
        elc = Line(el.get_bottom() + DOWN * 0.04, enhs[1].get_center() + np.array([0.12, 0.12, 0]), color=TEAL, stroke_width=3)
        self.play(FadeIn(el), Create(elc), Indicate(enhs[1], color=TEAL, scale_factor=1.8), run_time=0.8)

        self.at("raises the transcription")
        ca = arr(enhs[1].get_left() + LEFT * 0.02, genes[1].get_right() + RIGHT * 0.02, TEAL, w=4, tip=0.15)
        self.play(GrowArrow(ca), run_time=0.6)

        self.at("receptor gene clusters")
        self.play(Indicate(note, color=TEAL, scale_factor=1.08), run_time=0.7)

        self.at("contact one another")
        self.play(FadeOut(el), FadeOut(elc), FadeOut(ca), FadeOut(gl_), run_time=0.3)
        offs = {0: (-0.42, 0.34, 0.42, 0.34), 1: (-0.42, -0.34, 0.42, -0.34)}
        tethers = []
        anims = []
        hubs = []
        for k, hx in enumerate(HX):
            hub = Circle(radius=0.95, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08).move_to([hx, -0.1, 0])
            hubs.append(hub)
            for j in (0, 1):
                idx = 2 * k + j
                gx, gy, ex, ey = offs[j]
                anims.append(genes[idx].animate.move_to([hx + gx, -0.1 + gy, 0]))
                anims.append(enhs[idx].animate.move_to([hx + ex, -0.1 + ey, 0]))
        for idx in range(6):
            for obj, base in ((genes[idx], -0.5), (enhs[idx], 0.5)):
                cc = caps[idx].get_center() + np.array([base, 0, 0])
                tethers.append(always_redraw(lambda o=obj, cc=cc: DashedLine(cc, o.get_center(), color=TEAL, stroke_width=2, dash_length=0.12)))
        for t in tethers:
            self.add(t)
        self.play(*anims, *[FadeIn(h) for h in hubs], run_time=1.6)
        for t in tethers:
            t.clear_updaters()
        self.remove(*tethers)
        tth = [DashedLine(caps[i].get_center() + np.array([b, 0, 0]), o.get_center(), color=TEAL, stroke_width=2, dash_length=0.12)
               for i in range(6) for o, b in ((genes[i], -0.5), (enhs[i], 0.5))]
        tg_ = VGroup(*tth)
        self.add(tg_)
        self.wait(0.2)

        self.at("several competing hubs")
        cm = bchip("hubs compete", TEAL, 26).move_to([0, -3.35, 0])
        self.play(FadeOut(note), FadeIn(cm), run_time=0.3)
        for k in (0, 1, 2, 0, 2):
            self.play(Indicate(hubs[k], color=TEAL, scale_factor=1.12), run_time=0.5)

        self.at("before one gene dominates")
        win = genes[2]    # hub 1, top gene
        self.play(FadeOut(tg_), FadeOut(cm), run_time=0.4)
        self.play(win.animate.set_stroke(GREEN).set_fill(GREEN, 0.8).scale(1.5), hubs[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.12), run_time=0.7)

        self.at("further step")
        rna = bchip("receptor RNA", ORANGE, 24).move_to([0, 1.22, 0])
        a_up = arr(win.get_top() + UP * 0.02, rna.get_bottom() + LEFT * 0.4 + DOWN * 0.02, ORANGE, w=4)
        self.play(FadeIn(rna, shift=UP * 0.1), GrowArrow(a_up), run_time=0.7)

        self.at("suppresses the competing receptors")
        i1 = inhib(rna.get_left() + LEFT * 0.04, hubs[0].get_center() + np.array([0.85, 0.55, 0]), RED)
        i2 = inhib(rna.get_right() + RIGHT * 0.04, hubs[2].get_center() + np.array([-0.85, 0.55, 0]), RED)
        self.play(Create(i1), Create(i2),
                  hubs[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.02), hubs[2].animate.set_stroke(opacity=0.3).set_fill(opacity=0.02),
                  *[genes[i].animate.set_opacity(0.3) for i in (0, 1, 4, 5)], *[enhs[i].animate.set_opacity(0.3) for i in (0, 1, 4, 5)],
                  run_time=0.9)

        self.at("still unidentified")
        qs = [T("?", 44, RED, weight=BOLD).move_to(m) for m in (
            (i1.get_center() + np.array([0, 0.45, 0])), (i2.get_center() + np.array([0, 0.45, 0])))]
        um = T("machinery unidentified", 26, RED).move_to([0, -3.35, 0])
        self.play(*[FadeIn(q, scale=0.5) for q in qs], FadeIn(um), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Feedback(SpokenScene):
    """chosen gene -> receptor expressed -> PERK -> ATF5 -> Adcy3 -> feedback; lineage tracing shows more switching without Adcy3."""

    def construct(self):
        Y = 0.15
        g = tile(GREEN, 0.7, 0.7).move_to([-5.45, Y, 0])
        gl = T("chosen gene", 22, GREEN).next_to(g, UP, buff=0.18)
        rc = bchip("receptor made", ORANGE, 28).move_to([-3.15, Y, 0])
        pk = bchip("PERK", PURPLE, 28).move_to([-0.55, Y, 0])
        at = bchip("ATF5", PURPLE, 28).move_to([1.6, Y, 0])
        ad = bchip("Adcy3", PURPLE, 28).move_to([4.0, Y, 0])
        a1 = arr(g.get_right(), rc.get_left(), GREY, w=4)
        a2 = arr(rc.get_right(), pk.get_left(), PURPLE, w=4)
        a3 = arr(pk.get_right(), at.get_left(), PURPLE, w=4)
        a4 = arr(at.get_right(), ad.get_left(), PURPLE, w=4)
        by = Y + 0.62
        brx0, brx1 = pk.get_left()[0] - 0.1, at.get_right()[0] + 0.1
        brk = VGroup(Line([brx0, by, 0], [brx1, by, 0], color=PURPLE, stroke_width=3),
                     Line([brx0, by, 0], [brx0, by - 0.15, 0], color=PURPLE, stroke_width=3),
                     Line([brx1, by, 0], [brx1, by - 0.15, 0], color=PURPLE, stroke_width=3))
        bl = T("unfolded protein response", 24, PURPLE).move_to([(brx0 + brx1) / 2 - 0.3, by + 0.4, 0])
        up = Line(ad.get_top() + UP * 0.02, [ad.get_top()[0], by, 0], color=RED, stroke_width=4)
        lf = inhib([ad.get_top()[0], by, 0], [brx1 + 0.05, by, 0], RED, w=4)
        rl = T("relieves stress", 22, RED).move_to([(ad.get_top()[0] + brx1) / 2 + 0.55, by + 0.38, 0])
        dev = T("in developing mouse neurons", 24, GREY).move_to([0.2, Y - 1.3, 0])
        chain = VGroup(g, gl, rc, pk, at, ad, a1, a2, a3, a4, brk, bl, up, lf, rl)
        self.add(g, gl)
        self.wait(0.3)

        self.at("Receptor expression engages")
        self.play(GrowArrow(a1), FadeIn(rc, shift=RIGHT * 0.1), run_time=0.7)
        self.at("unfolded protein response")
        self.play(Create(brk), FadeIn(bl), run_time=0.7)
        self.at("In developing mouse neurons")
        self.play(FadeIn(dev), run_time=0.5)
        self.at("kinase called")
        self.play(GrowArrow(a2), FadeIn(pk, shift=RIGHT * 0.1), run_time=0.7)
        self.at("promotes the gene")
        self.play(GrowArrow(a3), FadeIn(at, shift=RIGHT * 0.1), GrowArrow(a4), FadeIn(ad, shift=RIGHT * 0.1), run_time=1.0)

        self.at("That enzyme")
        self.play(Create(up), run_time=0.3)
        self.play(Create(lf), FadeIn(rl), run_time=0.6)

        # lineage panel: lift the chain, bring the tracing rows in below it
        self.at("lineage tracing")
        self.play(FadeOut(dev), chain.animate.shift(UP * 1.9), run_time=0.7)
        ptitle = T("Lineage tracing of one receptor, young mice", 26, GREY).move_to([0, 0.2, 0])
        xs = [-2.9, -1.6, -0.3, 1.0, 2.3, 3.6]
        ya, yb = -0.7, -1.85

        def cell(x, y, color):
            return Circle(radius=0.42, stroke_color=GOLD, stroke_width=6, fill_color=color, fill_opacity=0.6).move_to([x, y, 0])

        la = T("with Adcy3", 26, TEXT).move_to([-5.15, ya, 0])
        lb = T("without Adcy3", 26, TEXT).move_to([-5.15, yb, 0])
        rowa = VGroup(*[cell(x, ya, GREEN) for x in xs])
        rowb = VGroup(*[cell(x, yb, GREEN) for x in xs])
        leg = VGroup(
            Circle(radius=0.14, stroke_color=GOLD, stroke_width=4, fill_opacity=0), T("marked: once chose the receptor", 22, GOLD),
            Circle(radius=0.14, stroke_width=0, fill_color=GREEN, fill_opacity=0.8), T("still that receptor", 22, GREEN),
            Circle(radius=0.14, stroke_width=0, fill_color=BLUE, fill_opacity=0.8), T("switched", 22, BLUE)).arrange(RIGHT, buff=0.18)
        leg.move_to([0.4, -2.85, 0])
        sk = T("sketch, not data", 22, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(ptitle), FadeIn(la), FadeIn(lb), FadeIn(rowa), FadeIn(rowb), FadeIn(leg), FadeIn(sk), run_time=0.9)
        self.at("more switching")
        self.play(rowa[1].animate.set_fill(BLUE, 0.6), rowa[4].animate.set_fill(BLUE, 0.6),
                  rowb[1].animate.set_fill(BLUE, 0.6), rowb[3].animate.set_fill(BLUE, 0.6), rowb[4].animate.set_fill(BLUE, 0.6), rowb[5].animate.set_fill(BLUE, 0.6),
                  run_time=0.9)

        self.at("So the feedback")
        gy = g.get_center()[1]
        fy = gy - 0.85
        last = DashedLine([g.get_center()[0], fy, 0], [g.get_center()[0], g.get_bottom()[1] - 0.02, 0], color=GREEN, stroke_width=4, dash_length=0.12)
        last.add_tip(ArrowTriangleFilledTip(color=GREEN, length=0.2, width=0.2))
        fb = VGroup(DashedLine([ad.get_bottom()[0], ad.get_bottom()[1] - 0.02, 0], [ad.get_bottom()[0], fy, 0], color=GREEN, stroke_width=4, dash_length=0.12),
                    DashedLine([ad.get_bottom()[0], fy, 0], [g.get_center()[0], fy, 0], color=GREEN, stroke_width=4, dash_length=0.12),
                    last)
        fl = T("helps stabilize the choice", 24, GREEN).move_to([-0.5, fy - 0.3, 0])
        self.play(Create(fb), FadeIn(fl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """three stages in a row; singular expression only at the end."""

    def construct(self):
        PW, PH, py = 3.8, 4.0, 0.2
        px = [-4.3, 0.0, 4.3]

        def panel(x, color):
            return RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=0.06).move_to([x, py, 0])

        p1, p2, p3 = panel(px[0], RED), panel(px[1], TEAL), panel(px[2], PURPLE)
        # panel 1: marked grid, one open
        t1 = []
        for r in range(3):
            for c in range(5):
                t = tile(RED, 0.42, 0.25).move_to([px[0] + (c - 2) * 0.62, py - 0.15 + (1 - r) * 0.55 + 0.1, 0])
                t1.append(t)
        op = t1[7]
        op.set_stroke(GREEN).set_fill(GREEN, 0.7)
        d1 = [mark_on(t) for t in t1 if t is not op]
        g1 = VGroup(*t1, *d1)
        # panel 2: hubs
        hubs2 = [Circle(radius=0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.1).move_to(
            [px[1] + dx, py - 0.1 + dy, 0]) for dx, dy in ((-0.95, -0.3), (0.0, 0.4), (0.95, -0.3))]
        win2 = tile(GREEN, 0.3, 0.8).move_to(hubs2[1].get_center())
        g2 = VGroup(*hubs2)
        for h in (hubs2[0], hubs2[2]):
            h.set_stroke(opacity=0.35).set_fill(opacity=0.03)
        hubs2[1].set_stroke(GREEN).set_fill(GREEN, 0.15)
        # panel 3: chosen gene with a feedback loop
        g3t = tile(GREEN, 0.7, 0.75).move_to([px[2], py + 0.05, 0])
        loop = Arc(radius=0.85, start_angle=PI * 0.15, angle=PI * 1.7, color=PURPLE, stroke_width=5).move_to([px[2], py + 0.05, 0])
        loop.add_tip(ArrowTriangleFilledTip(color=PURPLE, length=0.25, width=0.25))
        g3 = VGroup(g3t, loop)
        for gg, x, k in ((g1, px[0], 1.1), (g2, px[1], 1.15), (g3, px[2], 1.1)):
            gg.scale(k, about_point=np.array([x, py, 0]))

        n1 = T("1  silence", 28, RED).move_to([px[0], py + PH / 2 + 0.4, 0])
        n2 = T("2  hubs compete", 28, TEAL).move_to([px[1], py + PH / 2 + 0.4, 0])
        n3 = T("3  feedback", 28, PURPLE).move_to([px[2], py + PH / 2 + 0.4, 0])
        ar12 = arr([px[0] + PW / 2 + 0.03, py, 0], [px[1] - PW / 2 - 0.03, py, 0], GREY, w=4)
        ar23 = arr([px[1] + PW / 2 + 0.03, py, 0], [px[2] - PW / 2 - 0.03, py, 0], GREY, w=4)
        lab_y = py - PH / 2 - 0.45
        tags = [T("singular expression", 24, GREY).move_to([x, lab_y, 0]) for x in px]
        tags[2].set_color(GREEN)

        self.at("First comes silence")
        self.play(FadeIn(p1), FadeIn(n1), FadeIn(g1), run_time=0.8)
        self.at("several hubs compete")
        self.play(GrowArrow(ar12), FadeIn(p2), FadeIn(n2), FadeIn(g2), run_time=0.8)
        self.at("one gene dominates")
        self.play(FadeIn(win2, scale=0.5), run_time=0.5)
        self.at("feedback helps hold")
        self.play(GrowArrow(ar23), FadeIn(p3), FadeIn(n3), FadeIn(g3), run_time=0.9)
        self.at("ordered but incomplete")
        inc = T("mouse model: ordered, still incomplete", 24, GREY).move_to([0, -3.35, 0])
        self.play(FadeIn(inc), run_time=0.5)
        self.at("of a sequence")
        self.play(FadeIn(tags[2], shift=UP * 0.1), Indicate(p3, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("not a property")
        s1 = Line(tags[0].get_left(), tags[0].get_right(), color=RED, stroke_width=4)
        s2 = Line(tags[1].get_left(), tags[1].get_right(), color=RED, stroke_width=4)
        self.play(FadeIn(tags[0]), FadeIn(tags[1]), run_time=0.4)
        self.play(Create(s1), Create(s2), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Singular expression is the endpoint of a sequence, not every stage."
