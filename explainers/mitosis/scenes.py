"""Mitosis and chromosome segregation: the cut that cannot be undone  (Biochemistrypedia explainer)

One idea: anaphase is a one-way chain. Attachment is checked, the APC/C tags securin, separase is
freed and cuts Scc1, the ring opens, and a cut protein cannot be rejoined.

COLOR MAP (one color per concept, whole video)
  BLUE   = sister chromatids (and the sister-to-sister distance)
  ORANGE = kinetochores (and anaphase A, the kinetochore-to-pole distance)
  TEAL   = the cohesin ring and its Scc1 subunit
  YELLOW = spindle poles (and anaphase B, the pole-to-pole distance)
  GREY   = spindle fibres, the cell outline, quiet labels
  RED    = the unattached signal, "inactive", "cannot"
  PURPLE = APC/C-Cdc20 and its ubiquitin tags
  GOLD   = securin
  GREEN  = separase (dimmed while inactive)
  PINK   = the proteasome
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58AB0"
ORANGE = "#F29E4C"
Z = 0.0


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def chrom(cx, cy, s=1.0, ring=True):
    """Two sister bars side by side, a kinetochore on each outer face, a belt-shaped cohesin ring."""
    bw, bh, gap = 0.42 * s, 1.4 * s, 0.08 * s
    off = (bw + gap) / 2
    L = RoundedRectangle(corner_radius=bw / 2, width=bw, height=bh, stroke_color=BLUE, stroke_width=3,
                         fill_color=BLUE, fill_opacity=0.4).move_to([cx - off, cy, 0]).set_z_index(1)
    R = L.copy().move_to([cx + off, cy, 0])
    kr = 0.13 * s
    kL = Circle(radius=kr, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(L.get_left()).set_z_index(2)
    kR = Circle(radius=kr, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(R.get_right()).set_z_index(2)
    parts = [L, R, kL, kR]
    rg = None
    if ring:
        rg = Ellipse(width=1.5 * s, height=0.8 * s, stroke_color=TEAL, stroke_width=4 if s < 1.6 else 6,
                     fill_opacity=0).move_to([cx, cy, 0]).set_z_index(3)
        parts.append(rg)
    g = VGroup(*parts)
    g.L, g.R, g.kL, g.kR, g.ring = L, R, kL, kR, rg
    return g


def pole(x, y=0.0, r=0.2):
    return Dot([x, y, 0], radius=r, color=YELLOW).set_z_index(2)


def fib(p, k, w=2.5, color=GREY, live=False):
    ln = Line(p, k.get_center(), color=color, stroke_width=w)
    if live:
        ln.add_updater(lambda m: m.put_start_and_end_on(p, k.get_center()))
    return ln


def cell_outline(w=12.2, h=6.4, cx=0.0):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                   fill_opacity=0.06).move_to([cx, 0, 0]).set_z_index(-1)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def bchip(text, color, size=30, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def blob(text, color, w, h, size=30, corner=0.45):
    box = RoundedRectangle(corner_radius=corner, width=w, height=h, stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.35)
    back = RoundedRectangle(corner_radius=corner, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1)
    lab = T(text, size, color).move_to(box)
    return VGroup(back, box, lab)


def lv(m, v, f):
    """animations that set a chip/blob (back, box, label) to brightness v without touching its opaque back."""
    return [m[1].animate.set_stroke(opacity=v).set_fill(opacity=f * v), m[2].animate.set_opacity(v)]


def lv_set(m, v, f):
    m[1].set_stroke(opacity=v).set_fill(opacity=f * v)
    m[2].set_opacity(v)
    return m


def ub_badge():
    c = Circle(radius=0.27, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.9)
    return VGroup(c, T("Ub", 22, BG, weight=BOLD).move_to(c)).set_z_index(5)


def bracket(x0, x1, y, color, tick=0.13, w=3):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=w),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Mitosis and chromosome segregation"
    TITLE = "The cut that cannot be undone"


# ---------------------------------------------------------------------------------------------
class S01Pull(SpokenScene):
    """cell, poles, three chromosomes (two sisters + ring each) -> zoom on one -> '?' on the ring."""

    def construct(self):
        P = 5.4
        cell = cell_outline()
        pl, pr = pole(-P), pole(P)
        plab_l = T("pole", 24, YELLOW).move_to([-P, -0.55, 0])
        plab_r = T("pole", 24, YELLOW).move_to([P, -0.55, 0])
        rows = [1.7, 0.0, -1.7]
        chs = [chrom(0, y) for y in rows]
        fibs = []
        for c in chs:
            fibs.append(fib([-P, 0, 0], c.kL, live=True))
            fibs.append(fib([P, 0, 0], c.kR, live=True))
        others = VGroup(chs[0], chs[2], fibs[0], fibs[1], fibs[4], fibs[5])
        mid = chs[1]

        self.at("A cell must")
        self.play(FadeIn(cell), FadeIn(pl), FadeIn(pr), FadeIn(plab_l), FadeIn(plab_r), run_time=0.8)
        self.at("every chromosome")
        self.play(*[FadeIn(c, scale=0.8) for c in chs], *[Create(f) for f in fibs], run_time=1.0)

        # zoom on the middle chromosome
        self.at("two sister copies")
        self.play(FadeOut(others), mid.animate.scale(2.0), run_time=0.9)
        sis = T("two sister copies", 30, BLUE).move_to([0, 1.95, 0])
        self.play(FadeIn(sis, shift=DOWN * 0.1), run_time=0.4)

        self.at("ring called cohesin")
        lead = Line([0, -1.75, 0], [0, -0.8, 0], color=TEAL, stroke_width=3)
        coh = T("cohesin ring", 30, TEAL).move_to([0, -2.1, 0])
        self.play(Create(lead), FadeIn(coh), Indicate(mid.ring, color=TEAL, scale_factor=1.12), run_time=0.9)

        self.at("Each sister has")
        kl = T("kinetochore", 28, ORANGE).move_to([-2.9, -1.35, 0])
        kr_ = T("kinetochore", 28, ORANGE).move_to([2.9, -1.35, 0])
        ll = Line([-2.6, -1.1, 0], mid.kL.get_center() + DL * 0.2, color=ORANGE, stroke_width=3)
        lr = Line([2.6, -1.1, 0], mid.kR.get_center() + DR * 0.2, color=ORANGE, stroke_width=3)
        self.play(FadeIn(kl), FadeIn(kr_), Create(ll), Create(lr), run_time=0.8)

        self.at("opposite poles")
        al = arr([-2.0, 0.55, 0], [-3.7, 0.55, 0], TEXT)
        ar = arr([2.0, 0.55, 0], [3.7, 0.55, 0], TEXT)
        pull = T("pull", 28, TEXT)
        self.play(GrowArrow(al), GrowArrow(ar), run_time=0.7)
        self.play(FadeOut(VGroup(kl, kr_, ll, lr, sis, lead, coh)), FadeOut(VGroup(al, ar)), run_time=0.4)

        self.at("what lets go")
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, 2.1, 0])
        self.play(FadeIn(q, scale=0.6), Indicate(mid.ring, color=TEXT, scale_factor=1.15), run_time=0.8)

        self.at("never take it back")
        self.play(Indicate(mid.ring, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.play(FadeOut(q), mid.animate.scale(0.5), FadeIn(others), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Check(SpokenScene):
    """biorientation under tension; an unattached kinetochore holds back APC/C-Cdc20; attachment releases it."""

    def construct(self):
        cx, hw, s = -2.1, 3.5, 1.0
        cell = cell_outline(2 * hw + 1.3, 5.8, cx)
        xl, xr = cx - hw, cx + hw
        pl, pr = pole(xl), pole(xr)
        rows = [1.45, 0.0, -1.45]
        chs = [chrom(cx, y, s) for y in rows]
        fibs = []
        for i, c in enumerate(chs):
            fibs.append(fib([xl, 0, 0], c.kL))
            if i != 1:
                fibs.append(fib([xr, 0, 0], c.kR))
        top_fibs = VGroup(fibs[0], fibs[1])
        free_fib = fib([xr, 0, 0], chs[1].kR)

        apc = bchip("APC/C–Cdc20", PURPLE, size=32).move_to([4.3, -0.9, 0])
        apc_sub = T("anaphase-promoting complex", 22, PURPLE).move_to([4.3, -1.75, 0])

        self.at("First the cell")
        self.play(FadeIn(cell), FadeIn(pl), FadeIn(pr), *[FadeIn(c) for c in chs],
                  *[Create(f) for f in fibs], run_time=1.0)

        self.at("orientation")
        lab = T("biorientation", 28, TEXT).move_to([cx, 2.55, 0])
        self.play(FadeIn(lab), VGroup(chs[0]).animate.scale(1.12), rate_func=there_and_back, run_time=0.9)

        self.at("under tension")
        lab2 = T("under tension", 28, TEXT).move_to([cx, 2.55, 0])
        self.play(Transform(lab, lab2), top_fibs.animate.set_stroke(color=TEXT, width=5), run_time=0.7)

        self.at("stabilizes")
        lab3 = T("stable", 28, TEXT).move_to([cx, 2.55, 0])
        self.play(Transform(lab, lab3), Indicate(top_fibs, color=TEXT, scale_factor=1.0), run_time=0.7)

        self.at("still unattached")
        self.play(FadeOut(lab), run_time=0.3)
        halo = Circle(radius=0.3, stroke_color=RED, stroke_width=4).move_to(chs[1].kR.get_center()).set_z_index(4)
        unat = T("unattached", 22, RED).move_to([-0.7, 0.42, 0])
        self.play(Create(halo), FadeIn(unat), run_time=0.3)
        self.play(Indicate(halo, color=RED, scale_factor=1.3), run_time=0.4)

        self.at("sends a signal")
        start = chs[1].kR.get_center() + RIGHT * 0.3
        end = apc.get_left() + LEFT * 0.35
        sig = DashedLine(start, end, color=RED, stroke_width=4, dash_length=0.18)
        self.play(Create(sig), FadeIn(apc, shift=LEFT * 0.2), FadeIn(apc_sub), run_time=1.0)

        self.at("holds back")
        bar = inhib(end + LEFT * 0.0, apc.get_left(), RED)
        self.play(Create(bar), *lv(apc, 0.5, 0.16), run_time=0.6)

        self.at("activator")
        self.play(apc.animate.scale(1.1), rate_func=there_and_back, run_time=0.7)

        self.at("every kinetochore is attached")
        self.play(Create(free_fib), FadeOut(halo), FadeOut(unat), run_time=0.9)

        self.at("signal stops")
        self.play(FadeOut(sig), FadeOut(bar), *lv(apc, 1.0, 0.16), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tag(SpokenScene):
    """APC/C tags securin with Ub; securin leaves separase and is destroyed at the proteasome."""

    def construct(self):
        apc = bchip("APC/C–Cdc20", PURPLE, size=38).move_to([4.3, -0.9, 0])
        apc_sub = T("anaphase-promoting complex", 22, PURPLE).move_to([4.3, -1.75, 0])
        self.add(apc, apc_sub)

        self.at("is released")
        self.play(apc.animate.move_to([-4.2, 0.3, 0]), apc_sub.animate.move_to([-4.2, -0.6, 0]), run_time=1.0)

        self.at("tags proteins")
        ubs = VGroup(*[ub_badge() for _ in range(3)])
        for i, u in enumerate(ubs):
            u.move_to([-4.9 + 0.7 * i, 1.55, 0])
        self.play(LaggedStart(*[FadeIn(u, scale=0.5) for u in ubs], lag_ratio=0.25), run_time=0.9)

        self.at("sends them")
        prot = blob("proteasome", PINK, 2.7, 2.6, size=30, corner=0.5).move_to([4.8, 0.3, 0])
        self.play(FadeIn(prot, shift=LEFT * 0.2), run_time=0.8)

        self.at("One target")
        securin = blob("securin", GOLD, 2.2, 1.0, size=32, corner=0.3).move_to([0.5, 2.5, 0])
        self.play(FadeIn(securin, shift=DOWN * 0.2), run_time=0.6)

        self.at("binds an enzyme")
        sep = lv_set(blob("separase", GREEN, 3.8, 2.4, size=36, corner=0.5).move_to([0.5, -0.3, 0]), 0.5, 0.35)
        self.play(FadeIn(sep), securin.animate.move_to([0.5, 1.15, 0]), run_time=0.9)

        self.at("keeps it inactive")
        inact = T("inactive", 32, RED).move_to([0.5, -1.9, 0])
        self.play(FadeIn(inact), run_time=0.5)

        self.at("tagged securin")
        tx = [0.0, 0.5, 1.0]
        self.play(*[u.animate.move_to([0.5 + (i - 1) * 0.6, 1.8, 0]) for i, u in enumerate(ubs)], run_time=0.6)

        self.at("is destroyed")
        tag = VGroup(securin, ubs)
        self.play(tag.animate.move_to([4.8, 0.3, 0]).scale(0.25).set_opacity(0.0), run_time=1.1)

        self.at("Nothing holds")
        act = T("active", 32, GREEN).move_to([0.5, -1.9, 0])
        self.play(*lv(sep, 1.0, 0.35), ReplacementTransform(inact, act), run_time=0.7)

        self.at("is free")
        self.play(sep.animate.scale(1.06), rate_func=there_and_back, run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cut(SpokenScene):
    """separase cuts the Scc1 segment of the ring; ring opens; cut cannot be rejoined; sisters part."""

    def construct(self):
        P = 5.7
        s = 2.4
        cy = -0.3
        a, b = 0.75 * s, 0.4 * s
        A = -1.25
        d = 0.34

        def pt(t):
            return np.array([a * np.cos(t), cy + b * np.sin(t), 0])

        def arc(t0, t1, w, color=TEAL):
            return ParametricFunction(lambda t: pt(t), t_range=[t0, t1], color=color, stroke_width=w).set_z_index(3)

        ch = chrom(0, cy, s, ring=False)
        main = arc(A + d, A - d + TAU, 6)
        seg = arc(A - d, A + d, 13)
        pl, pr = pole(-P, cy), pole(P, cy)
        fl = fib([-P, cy, 0], ch.kL, live=True)
        fr = fib([P, cy, 0], ch.kR, live=True)

        self.at("Separase is")
        coh = T("cohesin ring", 30, TEAL).move_to([-1.0, -2.95, 0])
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(ch), Create(fl), Create(fr), Create(main), Create(seg), FadeIn(coh), run_time=0.5)

        self.at("protease")
        sepb = blob("separase", GREEN, 2.0, 0.95, size=28, corner=0.35).set_z_index(6).move_to([5.0, -2.6, 0])
        self.add(sepb)
        self.play(sepb.animate.move_to([1.2, -1.8, 0]), run_time=1.0)

        self.at("It cuts")
        scc = T("Scc1", 32, TEAL, weight=BOLD).move_to([2.8, -0.85, 0])
        lead = Line([2.3, -0.9, 0], pt(A) + RIGHT * 0.05, color=TEAL, stroke_width=3)
        self.play(FadeIn(scc), Create(lead), Indicate(seg, color=TEAL, scale_factor=1.2), run_time=0.9)

        self.at("ring opens")
        stub1 = arc(A - d, A - 0.2, 13)
        stub2 = arc(A + 0.2, A + d, 13)
        self.play(ReplacementTransform(seg, VGroup(stub1, stub2)), sepb.animate.shift([0.5, 0.0, 0]),
                  FadeOut(VGroup(scc, lead)), run_time=0.7)
        self.play(FadeOut(sepb, shift=RIGHT * 1.6), run_time=0.8)

        self.at("cannot be rejoined")
        c = (pt(A - 0.2) + pt(A + 0.2)) / 2
        x1 = Line(c + [-0.3, -0.3, 0], c + [0.3, 0.3, 0], color=RED, stroke_width=8).set_z_index(7)
        x2 = Line(c + [-0.3, 0.3, 0], c + [0.3, -0.3, 0], color=RED, stroke_width=8).set_z_index(7)
        nore = T("cannot be rejoined", 30, RED).move_to([-1.0, -2.95, 0])
        self.play(Create(x1), Create(x2), ReplacementTransform(coh, nore), run_time=0.7)

        self.at("free to part")
        ring_all = VGroup(main, stub1, stub2)
        self.play(ch.L.animate.shift(LEFT * 2.3), ch.kL.animate.shift(LEFT * 2.3),
                  ch.R.animate.shift(RIGHT * 2.3), ch.kR.animate.shift(RIGHT * 2.3),
                  ring_all.animate.set_stroke(opacity=0.3), run_time=1.1)

        self.at("In budding yeast")
        yeast = VGroup(*[T(x, 24, GREY) for x in ("this experiment was done in", "budding yeast cells held at metaphase")]).arrange(DOWN, buff=0.08)
        yeast_box = SurroundingRectangle(yeast, color=GREY, buff=0.18, corner_radius=0.12, stroke_width=2)
        yeast = VGroup(yeast_box, yeast).move_to([0, 2.75, 0])
        self.play(FadeIn(yeast, shift=DOWN * 0.1), run_time=0.6)

        self.at("enough to separate")
        self.play(Indicate(VGroup(ch.L, ch.R), color=BLUE, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Move(SpokenScene):
    """anaphase A and B, then a live movie with the lesson's worked numbers."""

    def construct(self):
        U, Y = 0.7, 0.85
        tr = ValueTracker(0.0)

        def st():
            t = tr.get_value()
            D = 12.0 + t
            kd = 5.5 - t
            return t, D, kd, D - 2 * kd

        def main():
            t, D, kd, sep = st()
            Pp = D * U / 2
            kx = sep * U / 2
            g = VGroup()
            g.add(Line([-Pp, Y, 0], [-kx, Y, 0], color=GREY, stroke_width=2.5),
                  Line([kx, Y, 0], [Pp, Y, 0], color=GREY, stroke_width=2.5))
            for sg in (-1, 1):
                bar = RoundedRectangle(corner_radius=0.14, width=0.28, height=2.0, stroke_color=BLUE,
                                       stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
                bar.move_to([sg * (kx + 0.14), Y, 0]).set_z_index(1)
                kin = Circle(radius=0.16, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
                kin.move_to([sg * kx, Y, 0]).set_z_index(2)
                g.add(bar, kin, Dot([sg * Pp, Y, 0], radius=0.2, color=YELLOW).set_z_index(2))
            return g

        def brackets():
            t, D, kd, sep = st()
            Pp = D * U / 2
            kx = sep * U / 2
            t = round(t, 1)
            D, kd = 12.0 + t, 5.5 - t
            sep = D - 2 * kd
            g = VGroup(
                bracket(-Pp, Pp, 2.55, YELLOW),
                M(f"poles {D:.1f} μm", 26, YELLOW).move_to([0, 3.05, 0]),
                bracket(-Pp, -kx, -0.5, ORANGE), bracket(kx, Pp, -0.5, ORANGE),
                M(f"{kd:.1f} μm", 26, ORANGE).move_to([-(Pp + kx) / 2, -0.92, 0]),
                M(f"{kd:.1f} μm", 26, ORANGE).move_to([(Pp + kx) / 2, -0.92, 0]),
                bracket(-kx, kx, -1.8, BLUE),
                M(f"sisters {sep:.1f} μm", 26, BLUE).move_to([0, -2.2, 0]),
                M(f"t = {t:.1f} min", 26, TEXT).move_to([-4.9, 3.05, 0]),
            )
            return g

        self.at("Anaphase has")
        spindle = always_redraw(main)
        self.play(FadeIn(spindle), run_time=0.8)

        self.at("moves each chromosome")
        aA = [arr([sg * 0.6, Y, 0], [sg * 1.9, Y, 0], ORANGE, w=7) for sg in (-1, 1)]
        labA = T("anaphase A", 30, ORANGE).move_to([-2.6, 2.5, 0])
        self.play(*[GrowArrow(x) for x in aA], FadeIn(labA), run_time=0.8)

        self.at("separates the poles")
        aB = [arr([sg * 4.55, Y, 0], [sg * 5.55, Y, 0], YELLOW, w=7) for sg in (-1, 1)]
        labB = T("anaphase B", 30, YELLOW).move_to([3.6, 2.5, 0])
        self.play(*[GrowArrow(x) for x in aB], FadeIn(labB), run_time=0.8)

        self.at("illustrative movie")
        self.play(FadeOut(VGroup(*aA, *aB, labA, labB)), run_time=0.5)

        self.at("The poles start")
        br = always_redraw(brackets)
        self.play(FadeIn(br), run_time=0.7)

        self.at("and end")
        rt = max(2.0, self.t_of("The sisters separate") - self.t_of("and end") - 0.1)
        self.play(tr.animate.set_value(4.0), run_time=rt, rate_func=linear)

        self.at("The sisters separate")
        e1 = M("(13.0 - 1.0) / 4.0 = 3.0 μm/min", 28, BLUE).move_to([0, -2.8, 0])
        self.play(FadeIn(e1, shift=UP * 0.1), run_time=0.5)

        self.at("That is twice")
        e2 = M("2(1.0) + 1.0 = 3.0 μm/min", 28, TEXT, t2c={"2(1.0)": ORANGE, "+ 1.0": YELLOW}).move_to([0, -3.25, 0])
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """four boxes in a one-way chain; the way back is crossed out."""

    def construct(self):
        xs = [-4.575, -1.525, 1.525, 4.575]
        cy = 0.7
        boxes = [RoundedRectangle(corner_radius=0.2, width=2.85, height=3.9, stroke_color=GREY, stroke_width=2.5)
                 .move_to([x, cy, 0]) for x in xs]

        def icon1(x):
            c = chrom(x, cy + 0.75, 0.9)
            f1 = Line([x - 1.15, cy + 0.75, 0], c.kL.get_center(), color=GREY, stroke_width=2.5)
            f2 = Line([x + 1.15, cy + 0.75, 0], c.kR.get_center(), color=GREY, stroke_width=2.5)
            return VGroup(c, f1, f2, pole(x - 1.2, cy + 0.75, 0.13), pole(x + 1.2, cy + 0.75, 0.13))

        def icon2(x):
            sepi = blob("", GREEN, 1.7, 0.7, corner=0.3).move_to([x, cy + 0.45, 0])
            sec = blob("", GOLD, 0.9, 0.4, corner=0.2).move_to([x, cy + 1.15, 0])
            k1 = Line(sec.get_center() + [-0.55, -0.35, 0], sec.get_center() + [0.55, 0.35, 0], color=RED, stroke_width=6)
            k2 = Line(sec.get_center() + [-0.55, 0.35, 0], sec.get_center() + [0.55, -0.35, 0], color=RED, stroke_width=6)
            return VGroup(sepi, sec, k1, k2)

        def icon3(x):
            aa, bb = 0.68, 0.36
            yy = cy + 0.75
            g = ParametricFunction(lambda t: np.array([x + aa * np.cos(t), yy + bb * np.sin(t), 0]),
                                   t_range=[0.35 + 0.25, 0.35 - 0.25 + TAU], color=TEAL, stroke_width=5)
            sepi = blob("", GREEN, 0.9, 0.5, corner=0.2).move_to([x + 1.0, yy + 0.55, 0])
            return VGroup(g, sepi)

        def icon4(x):
            yy = cy + 0.75
            c = VGroup()
            for sg in (-1, 1):
                bar = RoundedRectangle(corner_radius=0.1, width=0.22, height=0.9, stroke_color=BLUE, stroke_width=3,
                                       fill_color=BLUE, fill_opacity=0.4).move_to([x + sg * 0.5, yy, 0])
                kin = Circle(radius=0.09, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([x + sg * 0.61, yy, 0])
                c.add(bar, kin, arr([x + sg * 0.75, yy, 0], [x + sg * 1.25, yy, 0], ORANGE, w=5, tip=0.16))
            return c

        icons = [icon1(xs[0]), icon2(xs[1]), icon3(xs[2]), icon4(xs[3])]
        texts = ["every kinetochore\nattached", "securin\ndestroyed", "separase\ncuts Scc1", "chromosomes\nand poles\nmove apart"]
        labels = []
        for x, tx in zip(xs, texts):
            labels.append(T(tx, 22, TEXT, line_spacing=0.8).move_to([x, cy - 1.15, 0]))

        fwd = arr([-6.0, -2.0, 0], [6.0, -2.0, 0], TEXT, w=8, tip=0.3)
        oneway = btext("one way", 30, TEXT).move_to([0, -2.0, 0]).set_z_index(5)

        self.at("So anaphase")
        self.play(GrowArrow(fwd), run_time=1.0)
        self.at("one way through")
        self.play(FadeIn(oneway), run_time=0.5)

        for i, (cue, ) in enumerate([("Every kinetochore",), ("Securin is destroyed",), ("Separase cuts",), ("move apart",)]):
            self.at(cue)
            self.play(Create(boxes[i]), FadeIn(icons[i]), FadeIn(labels[i]), run_time=0.8)

        self.at("cannot be reversed")
        back = arr([6.0, -2.9, 0], [-6.0, -2.9, 0], RED, w=8, tip=0.3)
        x1 = Line([-0.3, -3.2, 0], [0.3, -2.6, 0], color=RED, stroke_width=8).set_z_index(5)
        x2 = Line([-0.3, -2.6, 0], [0.3, -3.2, 0], color=RED, stroke_width=8).set_z_index(5)
        self.play(GrowArrow(back), run_time=0.8)
        self.play(Create(x1), Create(x2), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "A cut protein cannot be rejoined, so anaphase cannot be reversed."
