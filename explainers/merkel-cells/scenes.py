"""A skin cell that feels force  (Biochemistrypedia explainer, Sensory Systems: Merkel cells)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the Merkel cell (epidermal cell)
  PURPLE = the SA1 afferent ending and its fibre
  BLUE   = Piezo2, the force-gated channel, and the Merkel-cell current
  YELLOW = afferent spikes
  GREEN  = light that depolarizes; an unchanged / similar result
  RED    = light that hyperpolarizes; a loss, a deletion, a crossed-out claim
  TEAL   = a candidate transmitter
  GOLD   = a caution or the rule to keep
  GREY   = epidermal neighbours, axes, held touch, neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def pair(cx=0.0, cy=0.0, s=1.0, cell_color=ORANGE, fibre=2.0):
    """A Merkel cell sitting on the disc-like contact of one afferent ending (schematic, side view)."""
    body = RoundedRectangle(corner_radius=0.55 * s, width=2.0 * s, height=1.7 * s, stroke_color=cell_color,
                            stroke_width=4, fill_color=cell_color, fill_opacity=0.22).move_to([cx, cy, 0])
    disc = RoundedRectangle(corner_radius=0.08 * s, width=1.5 * s, height=0.22 * s, stroke_width=0,
                            fill_color=PURPLE, fill_opacity=1).move_to([cx, cy - 0.85 * s - 0.13 * s, 0])
    line = Line(disc.get_bottom(), disc.get_bottom() + DOWN * fibre * s, color=PURPLE, stroke_width=7 * max(s, 0.6))
    g = VGroup(body, line, disc)
    g.body, g.line, g.disc = body, line, disc
    return g


def neighbours(cx=0.0, cy=0.0, s=1.0):
    """Grey epidermal cells either side of the Merkel cell (centre at cx, cy)."""
    cells = VGroup()
    for dx in (-4.05, -2.05, 2.05, 4.05):
        cells.add(RoundedRectangle(corner_radius=0.45 * s, width=1.8 * s, height=1.5 * s, stroke_color=GREY,
                                   stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([cx + dx * s, cy, 0]))
    return cells


def spike_run(pr, n=3, dt=0.45, run=0.55):
    """yellow impulses running up the fibre of a pair, as one animation."""
    anims = []
    for i in range(n):
        d = Dot(radius=0.11, color=YELLOW).move_to(pr.disc.get_bottom())
        anims.append(Succession(FadeIn(d, run_time=0.05),
                                d.animate(run_time=run, rate_func=linear).move_to(pr.line.get_end()),
                                FadeOut(d, run_time=0.05)))
    return LaggedStart(*anims, lag_ratio=dt / (run + 0.1))


def ticks(xs, y, h=0.55, color=YELLOW, w=4):
    return VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=color, stroke_width=w) for x in xs])


def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so shapes behind it do not show through its label."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross(mob, color=RED, w=7, pad=0.0):
    r = mob.get_width() / 2 + pad
    h = mob.get_height() / 2 + pad
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, h, 0]), c + np.array([r, -h, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-r, -h, 0]), c + np.array([r, h, 0]), color=color, stroke_width=w))


def spike_times():
    """One afferent sketch: dense at onset (dynamic), sparse and irregular after (static). In this sketch."""
    rng = np.random.default_rng(7)
    ts, t = [], 0.15
    for i in range(9):
        ts.append(t)
        t += 0.11 + 0.025 * i
    t = ts[-1] + 0.55
    while t < 8.8:
        ts.append(t)
        t += float(rng.gamma(1.2, 0.5)) + 0.12
    return ts


class S00Title(TitleCard):
    LESSON = "Merkel cells"
    TITLE = "A skin cell that feels force"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """The puzzle: neuron or skin cell? Then named, placed, and traced to the epidermis."""

    def construct(self):
        nb = neighbours(0, 0.9)
        pr = pair(0, 0.9, 1.0, cell_color=GREY, fibre=3.0)
        q = T("?", 64, YELLOW, weight=BOLD).move_to(pr.body)
        self.play(FadeIn(nb), FadeIn(pr), run_time=0.8)
        self.at("not a neuron")
        asku = chip("neuron or skin cell?", YELLOW, size=28).move_to([0, 2.95, 0])
        self.play(FadeIn(q, scale=0.7), FadeIn(asku, shift=DOWN * 0.15), run_time=0.6)
        self.at("keep firing")
        self.play(spike_run(pr, 4, 0.5), run_time=2.4)
        self.at("This is the")
        mk = T("Merkel cell", 30, ORANGE, weight=BOLD).move_to([0, 2.95, 0])
        self.play(pr.body.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.22), FadeOut(q), ReplacementTransform(asku, mk),
                  run_time=0.8)
        self.at("In mouse skin")
        ms = T("in mouse skin", 26, GREY).to_corner(UL, buff=0.5)
        self.play(FadeIn(ms), run_time=0.4)
        self.at("basal epidermis")
        be = T("basal epidermis", 26, GREY).move_to([-4.0, 2.05, 0])
        brk = Line([-5.0, 1.82, 0], [-3.1, 1.82, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(be), Create(brk), run_time=0.5)
        self.at("slowly adapting")
        sa1 = T("SA1 afferent", 26, PURPLE).move_to([2.0, -1.3, 0])
        self.play(FadeIn(sa1), Indicate(pr.disc, color=PURPLE, scale_factor=1.15), run_time=0.8)
        self.at("Lineage tracing")
        prog = chip("epidermal progenitor", GREY, size=24).move_to([-4.0, -1.9, 0])
        neu = chip("neuron", GREY, size=24).move_to([4.6, -1.9, 0])
        self.play(FadeIn(prog), FadeIn(neu), run_time=0.6)
        self.at("epidermal progenitors")
        arrow = Arrow(prog.get_top() + UP * 0.05, [-0.95, 0.35, 0], buff=0.08, color=ORANGE, stroke_width=5,
                      max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.at("not from neurons")
        self.play(Create(cross(neu, RED, 6, 0.05)), neu[0].animate.set_stroke(RED), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Channel(SpokenScene):
    """Pressed cultured cell: Piezo2 current peaks then falls to steady state; without Piezo2, 0 of 13 respond."""

    def construct(self):
        cell = pair(-4.0, 0.0, 1.55, ORANGE, fibre=0.0)
        body = cell.body
        mem = RoundedRectangle(corner_radius=0.1, width=body.width * 0.9, height=0.26, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to(body.get_top() + DOWN * 0.1)
        pz = bchip("Piezo2", BLUE, size=26).move_to(mem)
        lab = T("Merkel cell", 26, ORANGE).next_to(body, DOWN, buff=0.35)
        cult = T("cultured, young mice", 22, GREY).next_to(lab, DOWN, buff=0.15)
        self.play(FadeIn(body), FadeIn(mem), FadeIn(pz), FadeIn(lab), FadeIn(cult), run_time=0.8)

        # axes: t 0..40 ms -> x 1.4..6.2 ; I 0..400 pA -> y -2.0..2.4
        X0, X1, Y0, Y1 = 1.4, 6.2, -2.0, 2.4
        fx = lambda t: X0 + (X1 - X0) * t / 40.0
        fy = lambda i: Y0 + (Y1 - Y0) * i / 400.0
        xa = Line([X0, Y0, 0], [X1 + 0.1, Y0, 0], color=GREY, stroke_width=3)
        ya = Line([X0, Y0, 0], [X0, Y1 + 0.2, 0], color=GREY, stroke_width=3)
        xt = VGroup(*[T(str(v), 22, GREY).move_to([fx(v), Y0 - 0.32, 0]) for v in (0, 20, 40)])
        yt = VGroup(*[T(str(v), 22, GREY).move_to([X0 - 0.4, fy(v), 0]) for v in (0, 200, 400)])
        xu = T("ms", 22, GREY).move_to([X1 + 0.1, Y0 - 0.65, 0])
        yu = T("pA", 22, GREY).move_to([X0 - 0.1, Y1 + 0.55, 0])
        axes = VGroup(xa, ya, xt, yt, xu, yu)
        title = T("group means, in this sketch", 22, GREY).move_to([3.9, 3.35, 0])
        pts = [np.array([fx(t), fy(20 + 350 * np.exp(-t / 8.0)), 0]) for t in np.linspace(0, 40, 80)]
        curve = VMobject(color=BLUE, stroke_width=6).set_points_smoothly(pts)

        self.at("pressing")
        press = Arrow([-4.0, 3.5, 0], mem.get_top() + UP * 0.05, buff=0.02, color=TEXT, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        pl = T("press", 24, TEXT).next_to(press, RIGHT, buff=0.15)
        self.play(GrowArrow(press), FadeIn(pl), FadeIn(axes), FadeIn(title), run_time=0.7)
        self.play(Create(curve, run_time=1.8, rate_func=linear), pz[1].animate.set_stroke(BLUE, 5), pz[2].animate.set_color(BLUE),
                  Flash(pz, color=BLUE, line_length=0.2, flash_radius=0.7), run_time=1.8)
        self.at("at its peak")
        pk = Dot(pts[0], radius=0.1, color=YELLOW)
        pkl = T("peak 370 pA", 24, BLUE).move_to([3.7, 2.35, 0])
        self.play(FadeIn(pk, scale=2), FadeIn(pkl), run_time=0.5)
        self.at("At steady state")
        dash = DashedLine([X0, fy(20), 0], [X1, fy(20), 0], color=BLUE, stroke_width=3, dash_length=0.12)
        stl = T("steady 20 pA", 24, BLUE).move_to([5.0, fy(20) + 0.45, 0])
        self.play(Create(dash), FadeIn(stl), run_time=0.7)
        self.at("of the peak")
        ratio = T("20/370 = 5.4% of the peak", 24, TEXT).move_to([4.5, 0.6, 0])
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.5)
        self.at("skin epithelium")
        self.play(FadeOut(VGroup(axes, curve, pk, pkl, dash, stl, ratio, title)), FadeOut(press), FadeOut(pl), run_time=0.5)
        x = cross(pz, RED, 7, 0.0)
        self.play(Create(x), pz[1].animate.set_stroke(RED), pz[2].animate.set_color(RED), run_time=0.5)
        dots = VGroup(*[Circle(radius=0.2, stroke_color=RED, stroke_width=3, fill_opacity=0) for _ in range(13)])
        dots.arrange_in_grid(rows=2, cols=7, buff=0.28).move_to([3.0, 0.3, 0])
        hd = T("Piezo2 deleted from epithelium", 24, RED).move_to([3.0, 2.5, 0])
        hd2 = T("cultured Merkel cells", 22, GREY).move_to([3.0, 1.9, 0])
        self.play(FadeIn(hd), FadeIn(hd2), LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.12), run_time=1.4)
        self.at("detectable current")
        none = T("0 of 13 with a current", 30, TEXT, weight=BOLD).move_to([3.0, -1.5, 0])
        self.play(FadeIn(none, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Phases(SpokenScene):
    """In this sketch: a brief cell current under a held touch drives sustained, irregular spikes. Dynamic vs static."""

    def construct(self):
        XL, XR = -2.9, 6.1
        fx = lambda t: XL + (XR - XL) * t / 9.0
        rows = {"touch": 2.5, "cur": 0.7, "spk": -1.35}
        labs = [("touch held", GREY, rows["touch"]), ("Merkel-cell current", BLUE, rows["cur"]),
                ("afferent spikes", YELLOW, rows["spk"])]
        lab_m = VGroup(*[T(t, 26, c).move_to([-5.0, y, 0]) for t, c, y in labs])
        lab_m[0].align_to([-6.2, 0, 0], LEFT); lab_m[1].align_to([-6.2, 0, 0], LEFT); lab_m[2].align_to([-6.2, 0, 0], LEFT)
        base = {k: Line([XL, y - 0.5, 0], [XR, y - 0.5, 0], color=GREY, stroke_width=2, stroke_opacity=0.5) for k, y in rows.items()}
        note = T("in this sketch", 22, GREY).move_to([0.6, -3.65, 0])
        self.play(FadeIn(lab_m[0]), FadeIn(note), run_time=0.5)
        # held touch: a step
        step = VMobject(color=TEXT, stroke_width=5).set_points_as_corners(
            [[XL, rows["touch"] - 0.4, 0], [fx(0.0), rows["touch"] - 0.4, 0], [fx(0.0), rows["touch"] + 0.4, 0],
             [fx(9.0), rows["touch"] + 0.4, 0]])
        self.at("mostly brief")
        self.play(Create(step), FadeIn(lab_m[1]), run_time=0.8)
        ts = np.linspace(0, 9, 90)
        cp = [np.array([fx(t), rows["cur"] - 0.5 + 1.0 * (0.054 + 0.946 * np.exp(-t / 0.35)), 0]) for t in ts]
        cur = VMobject(color=BLUE, stroke_width=6).set_points_smoothly(cp)
        self.play(Create(cur), run_time=1.0)
        self.at("fires for as long")
        st = spike_times()
        tk = ticks([fx(t) for t in st], rows["spk"], 0.8, YELLOW, 4)
        self.play(FadeIn(lab_m[2]), LaggedStart(*[Create(k) for k in tk], lag_ratio=0.12), run_time=3.2)
        self.at("dynamic phase")
        d_end = fx(st[8] + 0.2)
        by = rows["spk"] - 0.6
        b1 = Line([fx(0.0), by, 0], [d_end, by, 0], color=TEAL, stroke_width=6)
        l1 = T("dynamic", 26, TEAL).next_to(b1, DOWN, buff=0.12).align_to(b1, LEFT)
        self.play(Create(b1), FadeIn(l1), tk[:9].animate.set_stroke(width=7), run_time=0.7)
        self.at("static phase")
        b2 = Line([d_end + 0.15, by, 0], [fx(9.0), by, 0], color=GOLD, stroke_width=6)
        l2 = T("static", 26, GOLD).next_to(b2, DOWN, buff=0.12)
        self.play(Create(b2), FadeIn(l2), tk[9:].animate.set_stroke(width=7), run_time=0.7)
        self.at("irregular intervals")
        self.play(Indicate(tk[9:], color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("How a brief")
        qa = DashedLine([5.0, rows["cur"] - 0.3, 0], [5.0, rows["spk"] + 0.55, 0], color=GREY, stroke_width=4)
        qm = bchip("how?", YELLOW, size=30).move_to([5.0, -0.3, 0])
        self.play(Create(qa), FadeIn(qm, scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Light(SpokenScene):
    """Optogenetics, ex vivo: light that depolarizes Merkel cells drives spikes; light that hyperpolarizes thins them tenfold."""

    def construct(self):
        pr = pair(-4.2, 0.6, 1.35, ORANGE, fibre=1.5)
        lab = T("Merkel cell", 24, ORANGE).move_to([-1.75, 0.6, 0])
        pre = T("ex vivo mouse skin-nerve", 24, GREY).move_to([0.5, 3.45, 0])
        self.play(FadeIn(pr), FadeIn(lab), run_time=0.6)
        self.at("ex vivo")
        self.play(FadeIn(pre), run_time=0.5)

        LX0, LX1 = -0.4, 6.2
        fx = lambda t: LX0 + (LX1 - LX0) * t / 10.0
        # lane A: light depolarizes, spikes
        self.at("depolarizes only")
        la = T("light depolarizes Merkel cells", 24, GREEN).move_to([2.9, 2.55, 0])
        lbar = Rectangle(width=fx(9.0) - fx(0.5), height=0.16, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        lbar.move_to([(fx(0.5) + fx(9.0)) / 2, 2.1, 0])
        beam = Arrow([-4.2, 3.5, 0], pr.body.get_top() + UP * 0.08, buff=0.02, color=GREEN, stroke_width=6, max_tip_length_to_length_ratio=0.35)
        bl = T("light", 22, GREEN).next_to(beam, RIGHT, buff=0.15)
        self.play(FadeIn(la), GrowArrow(beam), FadeIn(bl), FadeIn(lbar), pr.body.animate.set_stroke(GREEN), run_time=0.7)
        ra = np.random.default_rng(11)
        tA = np.cumsum(0.4 + ra.gamma(1.5, 0.3, 9)) - 0.2
        tkA = ticks([fx(t) for t in tA if t < 9.0], 1.4, 0.6, YELLOW, 4)
        self.play(spike_run(pr, 3, 0.45), LaggedStart(*[Create(k) for k in tkA], lag_ratio=0.2), run_time=2.4)

        # lane B: touch held, light hyperpolarizes
        self.at("hyperpolarizes them")
        lb = T("touch held, cells silenced by light", 24, RED).move_to([2.9, 0.4, 0])
        tbar = Rectangle(width=fx(10.0) - fx(0.0), height=0.16, stroke_width=0, fill_color=TEXT, fill_opacity=0.7)
        tbar.move_to([(fx(0.0) + fx(10.0)) / 2, -0.05, 0])
        tl = T("touch", 22, TEXT).move_to([fx(0.0) - 0.0, -0.4, 0]).align_to([LX0, 0, 0], LEFT)
        rbar = Rectangle(width=fx(10.0) - fx(5.2), height=0.16, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        rbar.move_to([(fx(5.2) + fx(10.0)) / 2, -0.8, 0])
        rl = T("light", 22, RED).move_to([fx(7.6), -1.2, 0])
        tB1 = [0.3 + 0.5 * i for i in range(10)]
        note = T("in this sketch", 22, GREY).move_to([2.9, -3.5, 0])
        tkB = ticks([fx(t) for t in tB1], -2.0, 0.6, YELLOW, 4)
        tkB2 = ticks([fx(8.0)], -2.0, 0.6, YELLOW, 4)
        self.add(note)
        self.play(FadeOut(beam), FadeOut(bl), pr.body.animate.set_stroke(ORANGE), VGroup(la, lbar, tkA).animate.set_opacity(0.3), FadeIn(lb), FadeIn(tbar), FadeIn(tl),
                  LaggedStart(*[Create(k) for k in tkB], lag_ratio=0.1), run_time=1.5)
        self.at("suppressed the sustained")
        self.play(FadeIn(rbar), FadeIn(rl), pr.body.animate.set_stroke(RED), run_time=0.5)
        self.play(Create(tkB2), run_time=0.3)
        self.at("reported experiment")
        rep = T("reported experiment, 3 units", 24, GREY).move_to([2.9, -2.95, 0])
        self.play(FadeIn(rep), run_time=0.4)
        self.at("tenfold")
        self.play(FadeOut(rep), run_time=0.2)
        res = T("median firing fell tenfold (3 units)", 26, TEXT, weight=BOLD).move_to([2.9, -2.95, 0])
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Split(SpokenScene):
    """Two-receptor model, with its two deletion results and the limit of the developmental one."""

    def construct(self):
        pr = pair(-4.2, 1.2, 1.35, ORANGE, fibre=1.6)
        mem = RoundedRectangle(corner_radius=0.1, width=pr.body.width * 0.9, height=0.22, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to(pr.body.get_top() + DOWN * 0.08)
        pz = bchip("Piezo2", BLUE, size=24).move_to(mem)
        own = chip("ending's own sensor", PURPLE, size=24).move_to([-1.9, -1.0, 0])
        join = Line(pr.line.get_center() + RIGHT * 0.05, own.get_left(), color=PURPLE, stroke_width=3)
        cl = T("Merkel cell", 24, ORANGE).move_to([-4.2, 3.45, 0])
        self.play(FadeIn(pr), FadeIn(mem), FadeIn(pz), FadeIn(cl), run_time=0.4)
        self.at("two receptor model")
        self.wait(0.1)
        self.at("shapes the sustained")
        sus = T("sustained firing", 24, GOLD).move_to([-1.0, 1.2, 0])
        sarr = Arrow(sus.get_left() + LEFT * 0.05, pr.body.get_right() + RIGHT * 0.05, buff=0.05, color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(sus), GrowArrow(sarr), run_time=0.7)
        self.at("keeps its own")
        self.play(FadeIn(own), Create(join), Indicate(pr.disc, color=PURPLE, scale_factor=1.2), run_time=0.8)

        # epithelial Piezo2 deletion result
        self.at("deleted from epithelium")
        hd = T("Piezo2 deleted from epithelium", 24, RED).move_to([3.3, 2.9, 0])
        x = cross(pz, RED, 6, 0.0)
        self.play(Create(x), pz[1].animate.set_stroke(RED), pz[2].animate.set_color(RED), FadeIn(hd), run_time=0.6)
        self.at("dynamic responses")
        r1 = chip("dynamic: similar to controls", GREEN, size=24).move_to([3.3, 1.7, 0])
        self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("sustained firing was lost")
        r2 = chip("normal sustained firing: lost", RED, size=24).move_to([3.3, 0.4, 0])
        self.play(FadeIn(r2, shift=RIGHT * 0.15), run_time=0.5)

        # developmental deletion
        self.at("mice without")
        tbl = VGroup(hd, r1, r2)
        self.play(FadeOut(tbl), FadeOut(x), FadeOut(sus), FadeOut(sarr), FadeOut(pr.body), FadeOut(mem), FadeOut(pz),
                  FadeOut(cl), run_time=0.7)
        gone = T("no Merkel cells", 24, RED).move_to([-4.2, 2.3, 0])
        self.play(FadeIn(gone), run_time=0.3)
        self.at("still respond to touch")
        self.play(spike_run(pr, 2, 0.5), run_time=1.4)
        # bars
        BX, BY = 1.7, -1.9
        sc = 0.0105
        ax = Line([BX, BY, 0], [6.3, BY, 0], color=GREY, stroke_width=3)
        ay = Line([BX, BY, 0], [BX, BY + 3.0, 0], color=GREY, stroke_width=3)
        yt = VGroup(*[T(str(v), 22, GREY).move_to([BX - 0.42, BY + v * sc, 0]) for v in (0, 100, 200)])
        yu = T("Hz", 22, GREY).move_to([BX - 0.1, BY + 3.35, 0])
        b1 = Rectangle(width=1.3, height=238 * sc, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([3.1, BY + 238 * sc / 2, 0])
        b2 = Rectangle(width=1.3, height=79 * sc, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).move_to([5.2, BY + 79 * sc / 2, 0])
        v1 = T("238", 26, TEXT, weight=BOLD).next_to(b1, UP, buff=0.1)
        v2 = T("79", 26, TEXT, weight=BOLD).next_to(b2, UP, buff=0.1)
        x1 = T("control", 22, GREY).move_to([3.1, BY - 0.35, 0])
        x2 = T("no cells", 22, GREY).move_to([5.2, BY - 0.35, 0])
        ttl = T("peak SA1 firing, group means", 22, GREY).move_to([3.9, 3.35, 0])
        self.at("peak firing")
        self.play(FadeIn(VGroup(ax, ay, yt, yu, x1, x2, ttl)), GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=0.8)
        self.at("to 79")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), run_time=0.6)
        self.at("group means")
        fall = T("66.8% fall", 28, GOLD, weight=BOLD).move_to([4.1, 2.2, 0])
        fa = Arrow([3.5, BY + 238 * sc + 0.75, 0], [4.8, BY + 79 * sc + 0.85, 0], buff=0.0, color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(fall), GrowArrow(fa), run_time=0.6)
        self.at("cannot say through")
        cav = chip("developmental: mechanism unknown", GOLD, size=24).move_to([-2.4, -3.1, 0])
        self.play(FadeIn(cav, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Synapse(SpokenScene):
    """Three candidate transmitters, each in its own preparation; none settled; the rule to keep."""

    def column(self, cx, name, prep):
        cell = RoundedRectangle(corner_radius=0.5, width=2.0, height=1.35, stroke_color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=0.22).move_to([cx, 1.7, 0])
        disc = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.24, stroke_width=0, fill_color=PURPLE,
                                fill_opacity=1).move_to([cx, 0.15, 0])
        line = Line(disc.get_bottom(), [cx, -0.85, 0], color=PURPLE, stroke_width=7)
        nm = T(name, 28, TEAL, weight=BOLD)
        pp = T(prep, 22, GREY)
        txt = VGroup(nm, pp).arrange(DOWN, buff=0.12).move_to([cx, -1.75, 0])
        dots = VGroup(*[Dot(radius=0.12, color=TEAL).move_to([cx + dx, 0.95, 0]) for dx in (-0.4, 0.0, 0.4)])
        col = VGroup(cell, disc, line)
        return col, dots, txt

    def construct(self):
        qm = chip("what crosses the gap?", YELLOW, size=28).move_to([0, 3.25, 0])
        self.play(FadeIn(qm), run_time=0.5)
        specs = [(-4.2, "noradrenaline", "mouse touch domes"), (0.0, "serotonin", "mouse whisker\nMerkel cells"),
                 (4.2, "protons on\nASIC channels", "rodent whisker\nfollicles")]
        cols = [self.column(*s) for s in specs]
        self.at("Three accounts")
        self.play(*[FadeIn(c[0]) for c in cols], run_time=0.7)
        shown = []
        for key, (col, dots, txt) in zip(("Noradrenaline in", "Serotonin", "Protons acting"), cols):
            self.at(key)
            self.play(FadeIn(txt, shift=UP * 0.1),
                      LaggedStart(*[Succession(FadeIn(d, run_time=0.05), d.animate(run_time=0.6, rate_func=linear).shift(DOWN * 0.6),
                                               FadeOut(d, run_time=0.05)) for d in dots], lag_ratio=0.3), run_time=1.4)
            shown.append(txt)
        self.at("adrenergic account")
        self.play(Indicate(shown[0], color=TEAL, scale_factor=1.15), run_time=0.8)
        self.at("settled")
        st = chip("settled", GREY, size=26).move_to([-1.6, -3.1, 0])
        rf = chip("refuted", GREY, size=26).move_to([1.6, -3.1, 0])
        self.play(FadeIn(st), FadeIn(rf), run_time=0.4)
        cs = cross(st, RED, 6, 0.05)
        self.play(Create(cs), st[0].animate.set_stroke(RED), run_time=0.4)
        self.at("refuted")
        cr = cross(rf, RED, 6, 0.05)
        self.play(Create(cr), rf[0].animate.set_stroke(RED), run_time=0.4)
        self.at("Keep this")
        a = chip("in mouse skin: senses force", GREEN, size=26).move_to([-3.0, -3.1, 0])
        b = chip("transmitter: still open", GOLD, size=26).move_to([3.0, -3.1, 0])
        self.play(FadeOut(st), FadeOut(rf), FadeOut(cs), FadeOut(cr), run_time=0.4)
        self.play(FadeIn(a, shift=UP * 0.1), FadeIn(b, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "In mouse skin, a skin cell senses force; its transmitter is open."
