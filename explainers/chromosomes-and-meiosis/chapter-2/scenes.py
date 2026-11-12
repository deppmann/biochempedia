"""What Holds the Pair, and What Lets Go (chromosomes and meiosis, chapter 2)  (Biochemistrypedia explainer)

Same world as chapter 1 (../scenes.py): dark ground, rounded chromosome rods with one white centromere dot.
COLOR MAP (same as chapter 1)
  BLUE / ORANGE   = first homolog pair (no allele letters in this chapter)
  TEAL            = names of stages (prophase I, anaphase I ...) and shugoshin
  YELLOW          = cohesin rings; also what is being asked
  WHITE (TEXT)    = centromere dot; the white outline marks CENTROMERE cohesin (arm rings are plain yellow)
  GREY            = the synaptonemal complex (ladder), spindle, cell outline
  RED             = what goes wrong
Cohesin is drawn as yellow rings around the two sister chromatids of one homolog.
"""
import numpy as np
import random
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
XC = 1.65         # x of the crossover (chiasma)
HL = 4.2          # half length of a chromosome in the pair world
TH = 0.40         # chromatid thickness
GS = 0.46         # distance between the two sisters' centre lines
SW = 40           # stroke width that draws a 0.40-thick rod
S0 = 1.1          # half distance between the homologs' inner chromatids when zipped
PW = 1.15         # width of the pinch at the crossover
POLE_Y = 2.8
ARM_X = [-3.5, -2.55, -1.6, 2.55, 3.4]
CEN_X = [-0.58, 0.58]
RH = 1.25         # ring height round two sisters


# ------------------------------------------------------------------ small helpers
class Ch:
    """A chromosome (as in chapter 1): one chromatid or two sisters, one centromere dot."""

    def __init__(s, color, length, rep=True, th=TH, x=0.0, y=0.0):
        s.color, s.length, s.rep, s.th = color, length, rep, th
        gap = th + 0.05
        offs = [gap / 2, -gap / 2] if rep else [0.0]
        s.rods = VGroup(*[RoundedRectangle(corner_radius=th / 2, width=length, height=th, stroke_color=color, stroke_width=3,
                                           fill_color=color, fill_opacity=0.6).move_to([0, o, 0]) for o in offs])
        r = th * (0.75 if rep else 0.34)
        s.dots = VGroup(Circle(radius=r, stroke_width=0, fill_color=TEXT, fill_opacity=1))
        s.g = VGroup(s.rods, s.dots).shift([x, y, 0])


def drift(m, amp=0.05, w=1.3, ph=0.0):
    m.dt_ = ph

    def f(mm, dt):
        mm.dt_ += dt
        mm.shift(UP * amp * w * np.cos(w * mm.dt_) * dt)
    m.add_updater(f)


def head(text, color=TEAL, size=34):
    return T(text, size, color, weight=BOLD).move_to([-4.9, 3.45, 0])


def cap(text, color=TEXT, size=32, y=-3.45, x=0.0):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def pole(p):
    return Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.9).move_to(p)


def ring_static(x, y, outlined=False, h=0.9, w=0.28):
    r = Ellipse(width=w, height=h, stroke_color=YELLOW, stroke_width=6, fill_opacity=0).move_to([x, y, 0])
    if outlined:
        o = Ellipse(width=w + 0.1, height=h + 0.1, stroke_color=TEXT, stroke_width=11, fill_opacity=0).move_to([x, y, 0])
        return VGroup(o, r)
    return r


class W(SpokenScene):
    """SpokenScene plus a faint slow field of drifting motes so a held frame is never dead."""

    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        ms = VGroup()
        for _ in range(16):
            d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY])).set_opacity(rng.uniform(0.15, 0.3))
            d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
            d.v = (rng.uniform(-0.12, 0.12), rng.uniform(0.08, 0.22))

            def f(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.0:
                    m.shift(DOWN * 8.0)
            d.add_updater(f)
            ms.add(d)
        ms.set_z_index(-10)
        self.add(ms)


def mute(c):
    return interpolate_color(ManimColor(c), ManimColor(BG), 0.15)


def curve(fn, a, b, colfn, op=1.0):
    """A thick rounded line y = fn(x) for x in [a, b], redrawn every frame (so trackers can reshape it)."""
    n = max(4, int((b - a) / 0.12))
    xs = np.linspace(a, b, n)
    m = VMobject()
    m.set_points_as_corners([[x, fn(x), 0] for x in xs])
    m.set_stroke(mute(colfn()), SW, opacity=op)
    try:
        m.set_cap_style(CapStyleType.ROUND)
        m.joint_type = LineJointType.ROUND
    except Exception:
        pass

    def upd(mm):
        mm.set_points_as_corners([[x, fn(x), 0] for x in xs])
        mm.set_stroke(color=mute(colfn()), opacity=mm.get_stroke_opacity())
    m.add_updater(upd)
    return m


class Bival:
    """The pair world: blue homolog above, orange below, each two sisters, with cohesin rings, the grey ladder and
    the crossover.  Trackers: S = half distance between the homologs' inner chromatids, P = how strongly the
    crossover pinches them together, W_ = how far the crossover has swapped the ends (0 none, 1 swapped)."""

    def __init__(s, S=S0, P=0.0, swp=0.0):
        s.S, s.P, s.W_ = ValueTracker(S), ValueTracker(P), ValueTracker(swp)
        cb, co = ManimColor(BLUE), ManimColor(ORANGE)
        x0, x1 = -HL + 0.15, HL - 0.15
        inner = s.inner
        s.bo = curve(lambda x: inner(x) + GS, x0, x1, lambda: BLUE)
        s.bil = curve(lambda x: inner(x), x0, XC, lambda: BLUE)
        s.bir = curve(lambda x: inner(x), XC, x1, lambda: interpolate_color(cb, co, s.W_.get_value()))
        s.oo = curve(lambda x: -inner(x) - GS, x0, x1, lambda: ORANGE)
        s.oil = curve(lambda x: -inner(x), x0, XC, lambda: ORANGE)
        s.oir = curve(lambda x: -inner(x), XC, x1, lambda: interpolate_color(co, cb, s.W_.get_value()))
        s.rods = VGroup(s.oo, s.oil, s.oir, s.bo, s.bil, s.bir)
        s.dot_b = Dot(radius=0.3, color=TEXT)
        s.dot_o = Dot(radius=0.3, color=TEXT)
        s.dot_b.add_updater(lambda m: m.move_to([0, inner(0) + GS / 2, 0]))
        s.dot_o.add_updater(lambda m: m.move_to([0, -inner(0) - GS / 2, 0]))
        s.dot_b.move_to([0, inner(0) + GS / 2, 0])
        s.dot_o.move_to([0, -inner(0) - GS / 2, 0])
        s.dots = VGroup(s.dot_b, s.dot_o)
        # cohesin
        s.arm_rings, s.cen_rings = VGroup(), VGroup()
        s.dist_rings = VGroup()
        for sg in (1, -1):
            for x in ARM_X:
                r = Ellipse(width=0.36, height=RH, stroke_color=YELLOW, stroke_width=7, fill_opacity=0)
                r.add_updater(lambda m, x=x, sg=sg: m.move_to([x, sg * (inner(x) + GS / 2), 0]))
                r.move_to([x, sg * (inner(x) + GS / 2), 0])
                s.arm_rings.add(r)
                if x > XC:
                    s.dist_rings.add(r)
            for x in CEN_X:
                o = Ellipse(width=0.5, height=RH + 0.12, stroke_color=TEXT, stroke_width=12, fill_opacity=0)
                r = Ellipse(width=0.36, height=RH, stroke_color=YELLOW, stroke_width=7, fill_opacity=0)
                g = VGroup(o, r)
                g.add_updater(lambda m, x=x, sg=sg: m.move_to([x, sg * (inner(x) + GS / 2), 0]))
                g.move_to([x, sg * (inner(x) + GS / 2), 0])
                s.cen_rings.add(g)
        # grey ladder
        s.rungs = VGroup()
        for x in np.arange(-3.6, 3.61, 0.36):
            ln = Line([x, 0.8, 0], [x, -0.8, 0], color=GREY, stroke_width=6)
            ln.add_updater(lambda m, x=x: m.put_start_and_end_on([x, inner(x) - 0.2, 0], [x, -(inner(x) - 0.2), 0]))
            s.rungs.add(ln)

    def inner(s, x):
        S = s.S.get_value()
        return S - (S - 0.2) * s.P.get_value() * np.exp(-((x - XC) / PW) ** 2)

    def trk(s):
        return Group(s.S, s.P, s.W_)

    def path(s, x_from=0.0, x_to=XC, n=24):
        """Centre line of the blue homolog from x_from to x_to, then the orange homolog back (for the link trace)."""
        i = s.inner
        up = [[x, i(x) + GS / 2, 0] for x in np.linspace(x_from, x_to, n)]
        dn = [[x, -(i(x) + GS / 2), 0] for x in np.linspace(x_to, x_from, n)]
        return up + [[x_to, 0.0, 0]] + dn


def spindle(b):
    """Cell outline, equator, poles and fibres for the pair world."""
    cell = RoundedRectangle(corner_radius=2.8, width=12.4, height=6.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
    eq = DashedLine([-6.0, 0, 0], [6.0, 0, 0], color=GREY, stroke_width=2, dash_length=0.18)
    pt, pb = pole([0, POLE_Y, 0]), pole([0, -POLE_Y, 0])
    f1 = Line(pt.get_center(), b.dot_b.get_center(), color=GREY, stroke_width=3)
    f2 = Line(pb.get_center(), b.dot_o.get_center(), color=GREY, stroke_width=3)
    f1.add_updater(lambda m: m.put_start_and_end_on(pt.get_center(), b.dot_b.get_center()))
    f2.add_updater(lambda m: m.put_start_and_end_on(pb.get_center(), b.dot_o.get_center()))
    return cell, eq, pt, pb, f1, f2


def equator_stage(sc, S=1.7, P=1.0, swp=1.0, glow=True):
    """Metaphase I as left by chapter-2 scene s07, rebuilt in the same place."""
    b = Bival(S, P, swp)
    cell, eq, pt, pb, f1, f2 = spindle(b)
    sc.add(b.trk(), cell, eq, pt, pb, f1, f2, b.rods, b.dots, b.arm_rings, b.cen_rings, head("meiosis I"))
    if glow:
        for r in b.dist_rings:
            r.set_stroke(width=11)
    return b, cell, eq, pt, pb, f1, f2


ZL, ZT = 10.5, 0.8


def zoom_chrom(yc=0.0):
    return Ch(BLUE, ZL, True, ZT, 0.0, yc)


def zoom_rings(ch, outlined_only=False, arm=True):
    """Cohesin rings round the two sisters of a zoomed chromosome."""
    th = ch.th
    yc = ch.g.get_center()[1]
    h = th * 2 + 0.05 + 0.5
    arms, cens = VGroup(), VGroup()
    if arm:
        for x in (-4.3, -3.2, -2.1, 2.1, 3.2, 4.3):
            arms.add(ring_static(x, yc, False, h, 0.5))
    for x in (-1.1, 1.1):
        cens.add(ring_static(x, yc, True, h, 0.5))
    for r in list(arms) + [c[1] for c in cens]:
        r.set_stroke(width=9)
    for c in cens:
        c[0].set_stroke(width=15)
    return arms, cens


def breathe(b, base, amp=0.04):
    b.S.t_ = 0.0

    def f(m, dt):
        m.t_ += dt
        m.set_value(base + amp * np.sin(1.6 * m.t_))
    b.S.add_updater(f)


def scissors(sc=1.5):
    ha = Circle(radius=0.2, stroke_color=TEXT, stroke_width=6).move_to([0.9, 0.3, 0])
    hb = Circle(radius=0.2, stroke_color=TEXT, stroke_width=6).move_to([0.9, -0.3, 0])
    ba = Line([0.9, 0.3, 0], [-1.2, -0.12, 0], color=TEXT, stroke_width=9)
    bb = Line([0.9, -0.3, 0], [-1.2, 0.12, 0], color=TEXT, stroke_width=9)
    pv = Dot([-0.6, 0.0, 0], radius=0.07, color=RED)
    return VGroup(ha, hb, ba, bb, pv).scale(sc)


def shield(cx=0.0, cy=0.0, sc=1.25):
    pts = [(-1.05, 1.3), (1.05, 1.3), (1.05, 0.25), (0, -1.3), (-1.05, 0.25)]
    p = Polygon(*[[x, y, 0] for x, y in pts]).round_corners(0.25)
    p.set_stroke(TEAL, 6).set_fill(TEAL, 0.35)
    return p.scale(sc).move_to([cx, cy, 0])


def split_chrom(sc, ch, dy, run=2.0, small=0.2):
    """Sisters part: the single centromere dot becomes one dot per sister; returns the animations."""
    r0, r1 = ch.rods[0], ch.rods[1]
    d1 = Dot(radius=small, color=TEXT).move_to(r0.get_center()).set_opacity(0)
    d2 = Dot(radius=small, color=TEXT).move_to(r1.get_center()).set_opacity(0)
    sc.add(d1, d2)
    return [r0.animate.shift(UP * dy), r1.animate.shift(DOWN * dy), ch.dots.animate.set_opacity(0),
            d1.animate.set_opacity(1).shift(UP * dy), d2.animate.set_opacity(1).shift(DOWN * dy)], VGroup(d1, d2)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Chromosomes and meiosis"
    TITLE = "What Holds the Pair, and What Lets Go"


class S01Puzzle(W):
    def construct(self):
        divider = Line([0, -3.3, 0], [0, 3.0, 0], color=GREY, stroke_width=2)
        hm, hi = T("mitosis", 38, TEAL, weight=BOLD).move_to([-3.5, 3.3, 0]), T("meiosis I", 38, TEAL, weight=BOLD).move_to([3.5, 3.3, 0])
        eql = DashedLine([-6.6, 0, 0], [-0.4, 0, 0], color=GREY, stroke_width=2, dash_length=0.18)
        eqr = DashedLine([0.4, 0, 0], [6.6, 0, 0], color=GREY, stroke_width=2, dash_length=0.18)
        rb = Ch(BLUE, 4.6, True, 0.5, 3.6, 0.75)
        ro = Ch(ORANGE, 4.6, True, 0.5, 3.6, -0.75)
        mb = Ch(BLUE, 2.8, True, 0.5, -5.1, 0.0)
        mo = Ch(ORANGE, 2.8, True, 0.5, -1.9, 0.0)
        self.play(FadeIn(divider), FadeIn(hi), FadeIn(eqr), FadeIn(rb.g), FadeIn(ro.g), run_time=1.2)
        self.at("part homologs")
        self.play(rb.g.animate.shift(UP * 1.5), ro.g.animate.shift(DOWN * 1.5), run_time=1.6)
        self.at("not sisters")
        q = T("?", 110, TEXT, weight=BOLD).move_to([3.6, 0.0, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.at("in mitosis")
        self.play(FadeIn(hm), FadeIn(eql), FadeIn(mb.g), FadeIn(mo.g), run_time=1.3)
        self.at("do not synapse")
        self.play(Indicate(mb.g, color=BLUE, scale_factor=1.05), Indicate(mo.g, color=ORANGE, scale_factor=1.05), run_time=1.3)
        self.at("each chromosome lines up")
        self.play(Indicate(mb.g, color=TEXT, scale_factor=1.08), run_time=0.9)
        self.play(Indicate(mo.g, color=TEXT, scale_factor=1.08), run_time=0.9)
        self.at("its sisters part")
        a1, dd1 = split_chrom(self, mb, 1.5)
        a2, dd2 = split_chrom(self, mo, 1.5)
        self.play(*a1, *a2, run_time=2.0)
        self.finish()


class S02QuestionFrame(W):
    def construct(self):
        b = Bival()
        self.add(b.trk())
        self.play(FadeIn(b.rods), FadeIn(b.dots), run_time=1.0)
        self.at("sisters stay")
        br_s = Brace(VGroup(b.bo, b.bil), LEFT, color=TEXT)
        lab_s = T("sisters", 32, TEXT, weight=BOLD).next_to(br_s, LEFT, buff=0.15)
        self.play(GrowFromCenter(br_s), FadeIn(lab_s), run_time=1.0)
        self.at("homologues part")
        br_h = Brace(VGroup(b.bo, b.oo), RIGHT, color=TEXT)
        lab_h = T("homologs", 32, TEXT, weight=BOLD).next_to(br_h, RIGHT, buff=0.15)
        self.play(GrowFromCenter(br_h), FadeIn(lab_h), run_time=1.0)
        self.at("something must tie")
        self.play(FadeOut(VGroup(br_s, lab_s, br_h, lab_h)), run_time=0.6)
        yb = S0 + GS / 2
        d1 = DashedVMobject(Ellipse(width=0.55, height=RH, stroke_color=YELLOW, stroke_width=7, fill_opacity=0), num_dashes=14).move_to([-2.4, yb, 0])
        d2 = DashedLine([2.4, S0 - 0.2, 0], [2.4, -(S0 - 0.2), 0], color=YELLOW, stroke_width=7, dash_length=0.14)
        q1 = T("?", 60, YELLOW, weight=BOLD).move_to([-2.4, 2.45, 0])
        q2 = T("?", 60, YELLOW, weight=BOLD).move_to([2.9, 0.0, 0])
        self.play(FadeIn(d1), FadeIn(q1), run_time=0.9)
        self.play(FadeIn(d2), FadeIn(q2), run_time=0.9)
        self.at("let go in the right order")
        self.play(Indicate(q1, color=YELLOW, scale_factor=1.3), Indicate(q2, color=YELLOW, scale_factor=1.3), run_time=1.4)
        self.finish()


class S03Cohesin(W):
    def construct(self):
        ch = Ch(BLUE, ZL, True, ZT, 0.0, 0.3)
        self.play(FadeIn(ch.g), run_time=1.0)
        arms, cens = zoom_rings(ch)
        tl = Line([-4.8, -2.8, 0], [4.8, -2.8, 0], color=GREY, stroke_width=4)
        mark = Dot([-2.0, -2.8, 0], radius=0.16, color=TEAL)
        sp = T("S phase", 34, TEAL, weight=BOLD).next_to(mark, DOWN, buff=0.15)
        self.at("from")
        both = VGroup(*arms, *cens)
        self.play(FadeIn(tl), FadeIn(mark), FadeIn(sp), LaggedStart(*[GrowFromCenter(r) for r in both], lag_ratio=0.22), run_time=3.0)
        self.at("called cohesin")
        lab = T("cohesin", 46, YELLOW, weight=BOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.8)
        self.at("along the arms")
        ta1 = T("arms", 34, TEXT, weight=BOLD).move_to([-3.2, -1.4, 0])
        ta2 = T("arms", 34, TEXT, weight=BOLD).move_to([3.2, -1.4, 0])
        self.play(FadeIn(ta1), FadeIn(ta2), LaggedStart(*[Indicate(r, color=TEXT, scale_factor=1.25) for r in arms], lag_ratio=0.12), run_time=1.8)
        self.at("around the centromere")
        tc = T("centromere", 34, TEXT, weight=BOLD).move_to([0, -1.4, 0])
        self.play(FadeIn(tc), Indicate(cens, color=TEXT, scale_factor=1.15), run_time=1.4)
        self.finish()


class S04Zip(W):
    def construct(self):
        b = Bival(2.0, 0.0, 0.0)
        hp = head("prophase I")
        self.add(b.trk())
        self.play(FadeIn(b.rods), FadeIn(b.dots), FadeIn(b.arm_rings), FadeIn(b.cen_rings), FadeIn(hp), run_time=1.0)
        self.at("pair along")
        self.play(b.S.animate.set_value(S0), run_time=2.0)
        self.at("a protein structure")
        self.play(LaggedStart(*[FadeIn(r) for r in b.rungs], lag_ratio=0.06), run_time=2.6)
        self.at("complex zips")
        lab = T("synaptonemal complex", 34, TEXT, weight=BOLD)
        box = SurroundingRectangle(lab, buff=0.15, corner_radius=0.1, stroke_color=TEXT, stroke_width=3).set_fill(BG, 0.92)
        chipg = VGroup(box, lab).move_to([0, 0, 0])
        self.play(FadeIn(chipg), run_time=0.9)
        self.at("together")
        br = Brace(VGroup(b.oo, b.oil), DOWN, color=TEXT)
        br.shift(DOWN * 0.3)
        tag = T("4 chromatids", 34, TEXT, weight=BOLD).next_to(br, DOWN, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(tag), run_time=1.2)
        self.finish()


class S05Swap(W):
    def construct(self):
        b = Bival(S0, 0.0, 0.0)
        hp = head("prophase I")
        self.add(b.trk(), b.rods, b.dots, b.arm_rings, b.cen_rings, b.rungs, hp)
        b.arm_rings.set_stroke(opacity=0.3)
        for g in b.cen_rings:
            g.set_stroke(opacity=0.3)
        b.rungs.set_stroke(opacity=0.5)
        sch = T("schematic", 26, TEXT).move_to([5.7, -3.5, 0])
        self.add(sch)
        self.at("crossing over happens")
        c1 = cap("crossing over", YELLOW, 38, 2.75)
        self.play(FadeIn(c1), run_time=0.8)
        self.at("non sister")
        c2 = cap("non-sister chromatids", TEXT, 36, 2.75)
        o1 = RoundedRectangle(corner_radius=0.3, width=2 * HL + 0.3, height=0.62, stroke_color=TEXT, stroke_width=4).move_to([0, S0, 0])
        o2 = RoundedRectangle(corner_radius=0.3, width=2 * HL + 0.3, height=0.62, stroke_color=TEXT, stroke_width=4).move_to([0, -S0, 0])
        self.play(ReplacementTransform(c1, c2), Create(o1), Create(o2), run_time=1.6)
        self.at("one from each")
        self.play(Indicate(o1, color=BLUE, scale_factor=1.03), Indicate(o2, color=ORANGE, scale_factor=1.03), run_time=1.4)
        self.at("a deliberate break")
        gap = Rectangle(width=0.24, height=0.5, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([XC, S0, 0])
        c3 = cap("one break", TEXT, 38, 2.75)
        self.play(FadeOut(o1), FadeOut(o2), FadeIn(gap, scale=1.5), ReplacementTransform(c2, c3), run_time=1.0)
        halo = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=5).move_to(gap.get_center())
        self.play(Create(halo), run_time=0.6)
        self.at("the repair copies")
        self.play(gap.animate.stretch_to_fit_width(0.5), FadeOut(halo), run_time=0.6)
        c4 = cap("copies from the homolog", TEXT, 36, 2.75)
        thread = VMobject().set_points_as_corners([[XC + 0.26, S0 - 0.12, 0], [XC + 0.36, 0.0, 0], [XC + 0.5, -S0 + 0.12, 0]]).set_stroke(BLUE, 8)
        cpy = Line([XC - 0.1, -S0, 0], [XC + 1.3, -S0, 0], color=TEXT, stroke_width=8)
        self.play(ReplacementTransform(c3, c4), Create(thread), run_time=1.0)
        self.play(Create(cpy), run_time=0.8)
        self.at("can end in a swap")
        c5 = cap("crossing over", YELLOW, 40, 2.75)
        self.play(FadeOut(gap), FadeOut(thread), FadeOut(cpy), ReplacementTransform(c4, c5), b.W_.animate.set_value(1.0), run_time=1.6)
        self.play(Indicate(c5, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S06Chiasma(W):
    def construct(self):
        b = Bival(S0, 0.0, 1.0)
        hp = head("prophase I")
        self.add(b.trk(), b.rods, b.dots, b.arm_rings, b.cen_rings, b.rungs, hp)
        b.arm_rings.set_stroke(opacity=0.3)
        for g in b.cen_rings:
            g.set_stroke(opacity=0.3)
        b.rungs.set_stroke(opacity=0.5)
        self.at("zipper comes apart")
        self.play(LaggedStart(*[FadeOut(r) for r in b.rungs], lag_ratio=0.05), b.arm_rings.animate.set_stroke(opacity=1.0),
                  *[g.animate.set_stroke(opacity=1.0) for g in b.cen_rings], run_time=1.8)
        self.at("pull slightly away")
        self.play(b.S.animate.set_value(1.4), b.P.animate.set_value(1.0), run_time=2.4)
        self.at("stay joined")
        halo = Circle(radius=0.6, stroke_color=TEXT, stroke_width=5).move_to([XC, 0, 0])
        self.play(Create(halo), run_time=0.9)
        self.at("chiasma")
        lab = T("chiasma", 44, TEXT, weight=BOLD).move_to([3.7, 0.0, 0])
        arr = Arrow([2.75, 0, 0], [2.35, 0, 0], color=TEXT, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(lab, shift=LEFT * 0.2), FadeIn(arr), run_time=1.0)
        self.finish()


class S07Link(W):
    def construct(self):
        b = Bival(1.4, 1.0, 1.0)
        hp = head("prophase I")
        self.add(b.trk(), b.rods, b.dots, b.arm_rings, b.cen_rings, hp)
        self.at("now look")
        self.play(Indicate(hp, color=TEAL, scale_factor=1.1), run_time=1.0)
        self.at("the crossover")
        halo = Circle(radius=0.6, stroke_color=TEXT, stroke_width=5).move_to([XC, 0, 0])
        self.play(Create(halo), run_time=0.9)
        self.at("on the arms")
        self.play(*[r.animate.set_stroke(width=12) for r in b.dist_rings], FadeOut(halo), run_time=0.7)
        self.play(LaggedStart(*[Indicate(r, color=TEXT, scale_factor=1.4) for r in b.dist_rings], lag_ratio=0.12), run_time=1.0)
        self.at("holds the two")
        pts = b.path(0.0, XC)
        path = VMobject().set_points_as_corners(pts).set_stroke(TEXT, 12, opacity=0.95)
        glow = VMobject().set_points_as_corners(pts).set_stroke(TEXT, 28, opacity=0.25)
        self.play(Create(glow), Create(path), run_time=3.0, rate_func=linear)
        self.at("in most organisms")
        cell, eq, pt, pb, f1, f2 = spindle(b)
        hm = head("meiosis I")
        self.play(FadeIn(cell), FadeIn(eq), FadeIn(pt), FadeIn(pb), ReplacementTransform(hp, hm), run_time=1.4)
        self.at("the spindle pulls")
        self.play(FadeOut(path), FadeOut(glow), FadeIn(f1), FadeIn(f2), run_time=0.8)
        self.play(b.S.animate.set_value(1.7), run_time=2.4)
        self.finish()


def ask_card():
    card = T("What must be cut to let the homologs go?", 26, TEXT, weight=BOLD)
    cbox = SurroundingRectangle(card, buff=0.1, corner_radius=0.1, stroke_color=YELLOW, stroke_width=3).set_fill(BG, 0.92)
    return VGroup(cbox, card).move_to([0, -3.43, 0])


class S08Question(W):
    def construct(self):
        b, cell, eq, pt, pb, f1, f2 = equator_stage(self)
        breathe(b, 1.7)
        self.at("what must")
        card = ask_card()
        self.play(FadeIn(card, shift=UP * 0.15), run_time=0.7)
        self.at("cell cut")
        self.play(Indicate(b.dist_rings[0], color=TEXT, scale_factor=1.8), run_time=1.0)
        self.at("homologues go")
        self.play(Indicate(b.cen_rings[0], color=TEXT, scale_factor=1.5), run_time=1.0)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        b, cell, eq, pt, pb, f1, f2 = equator_stage(self)
        breathe(b, 1.7)
        card = ask_card()
        g1 = SurroundingRectangle(b.dist_rings[0], buff=0.18, corner_radius=0.2, stroke_color=TEXT, stroke_width=4)
        g2 = SurroundingRectangle(b.cen_rings[0], buff=0.14, corner_radius=0.2, stroke_color=TEXT, stroke_width=4)
        for g, tgt in ((g1, b.dist_rings[0]), (g2, b.cen_rings[0])):
            g.tg = 1.5 if g is g2 else 0.0

            def pulse(m, dt, tgt=tgt):
                m.tg += dt
                m.set_stroke(opacity=0.5 + 0.5 * np.sin(2.4 * m.tg))
                m.move_to(tgt.get_center())
            g.add_updater(pulse)
        self.add(card, g1, g2)
        self.finish()


class S10Reveal(W):
    def construct(self):
        b, cell, eq, pt, pb, f1, f2 = equator_stage(self)
        card = cap("anaphase I: arm cohesin cut", TEAL, 34, -3.5)
        self.add(card)
        self.at("cohesin on the arms")
        self.play(LaggedStart(*[FadeOut(r, scale=1.8) for r in b.arm_rings], lag_ratio=0.08), run_time=1.8)
        self.at("no longer ties")
        self.play(b.P.animate.set_value(0.0), run_time=1.8)
        self.at("homologues part")
        self.play(b.S.animate.set_value(1.9), run_time=2.4)
        self.at("two sisters")
        self.play(Indicate(b.cen_rings, color=TEXT, scale_factor=1.2), run_time=1.4)
        self.finish()


class S11Guard(W):
    def construct(self):
        ch = Ch(BLUE, ZL, True, ZT, 0.0, 0.0)
        arms, cens = zoom_rings(ch, arm=False)
        hd = head("anaphase I")
        self.add(hd)
        self.play(FadeIn(ch.g), FadeIn(cens), run_time=0.8)
        self.at("centromeres")
        self.play(Indicate(cens, color=TEXT, scale_factor=1.2), run_time=0.9)
        self.at("has to survive")
        self.play(Indicate(cens, color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.at("called shugoshin")
        sh = shield(0.0, 0.0)
        lab = T("shugoshin", 46, TEAL, weight=BOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(sh, scale=1.4), FadeIn(lab), run_time=1.2)
        self.at("protects it")
        sc = scissors()
        sc.move_to([7.5, 0.0, 0])
        self.add(sc)
        self.play(sc.animate.move_to([3.1, 0.0, 0]), run_time=1.3)
        spark = Flash(np.array([1.4, 0.0, 0]), color=TEAL, line_length=0.4, flash_radius=0.5, run_time=0.6)
        self.play(spark, sc.animate.rotate(0.25).shift(RIGHT * 0.4), run_time=0.6)
        self.play(sc.animate.move_to([6.0, 0.4, 0]).rotate(-0.25), FadeOut(sc), run_time=0.8)
        self.at("brings an enzyme")
        pp = chip("PP2A", TEAL, 36)
        pp.move_to([-6.0, 1.9, 0])
        self.play(FadeIn(pp), run_time=0.3)
        self.play(pp.animate.move_to([3.2, 1.9, 0]), run_time=2.2)
        self.at("removing phosphate")
        th = T("thought to: removes phosphate", 32, TEXT, weight=BOLD).move_to([0, -2.4, 0])
        self.play(FadeIn(th, shift=UP * 0.1), run_time=1.0)
        self.at("shield cohesin")
        self.play(Indicate(sh, color=TEAL, scale_factor=1.1), Indicate(cens, color=YELLOW, scale_factor=1.1), run_time=1.6)
        self.finish()


class S12AnaphaseTwo(W):
    def construct(self):
        ch = Ch(BLUE, ZL, True, ZT, 0.0, 0.0)
        arms, cens = zoom_rings(ch, arm=False)
        sh = shield(0.0, 0.0)
        lab = T("shugoshin", 46, TEAL, weight=BOLD).move_to([0, 2.6, 0])
        hd = head("anaphase I")
        self.add(ch.g, cens, sh, lab, hd)
        self.at("joined into")
        hd2 = head("meiosis II")
        self.play(ReplacementTransform(hd, hd2), Indicate(cens, color=YELLOW, scale_factor=1.15), run_time=1.4)
        self.at("anaphase")
        self.play(FadeOut(sh), FadeOut(lab), run_time=1.0)
        self.at("centromere")
        sc = scissors()
        sc.move_to([7.5, 0.0, 0])
        self.add(sc)
        self.play(sc.animate.move_to([2.6, 0.0, 0]), run_time=1.0)
        self.play(LaggedStart(*[FadeOut(c, scale=1.6) for c in cens], lag_ratio=0.2), sc.animate.move_to([1.2, 0.0, 0]), run_time=0.7)
        self.play(sc.animate.move_to([6.0, 0.4, 0]), FadeOut(sc), run_time=0.4)
        cp = cap("anaphase II: centromere cohesin cut", TEAL, 32, -3.55)
        ptop, pbot = pole([0, 2.95, 0]), pole([0, -2.95, 0])
        self.play(FadeIn(cp), FadeIn(ptop), FadeIn(pbot), run_time=0.5)
        self.at("sisters part")
        anims, dd = split_chrom(self, ch, 1.7, small=0.3)
        self.play(*anims, run_time=2.4)
        self.finish()


def yeast_icon(x, y):
    body = Circle(radius=1.0, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.15).move_to([x, y, 0])
    bud = Circle(radius=0.55, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.15).move_to([x + 1.2, y + 0.85, 0])
    return VGroup(body, bud)


def mouse_icon(x, y):
    k = 1.8
    body = Ellipse(width=1.5 * k, height=0.9 * k, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.15).move_to([x, y, 0])
    head_ = Circle(radius=0.34 * k, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.15).move_to([x - 0.85 * k, y + 0.12 * k, 0])
    ear1 = Circle(radius=0.17 * k, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.15).move_to([x - 0.78 * k, y + 0.5 * k, 0])
    ear2 = Circle(radius=0.17 * k, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.15).move_to([x - 0.98 * k, y + 0.46 * k, 0])
    tail = ParametricFunction(lambda t: np.array([x + 0.75 * k + 0.7 * k * t, y + 0.12 * k + 0.28 * k * np.sin(5 * t), 0]), t_range=[0, 1], color=TEXT, stroke_width=6)
    eye = Dot([x - 0.97 * k, y + 0.2 * k, 0], radius=0.07, color=TEXT)
    return VGroup(body, head_, ear1, ear2, tail, eye)


class S13Scope(W):
    def construct(self):
        tl = Arrow([-5.8, -0.9, 0], [5.8, -0.9, 0], color=GREY, buff=0, stroke_width=7)
        n1 = Dot([-3.2, -0.9, 0], radius=0.26, color=TEAL)
        n2 = Dot([3.2, -0.9, 0], radius=0.26, color=TEAL)
        self.at("two step")
        self.play(Create(tl), FadeIn(n1), FadeIn(n2), run_time=1.6)
        self.at("yeast and mammals")
        yi, mi = yeast_icon(-3.4, 2.05), mouse_icon(2.6, 2.05)
        ty = T("yeast", 34, TEXT, weight=BOLD).move_to([-3.0, 0.5, 0])
        tm = T("mouse", 34, TEXT, weight=BOLD).move_to([2.6, 0.5, 0])
        self.play(FadeIn(yi, scale=0.7), FadeIn(ty), FadeIn(mi, scale=0.7), FadeIn(tm), run_time=1.6)
        self.at("as studied")
        note = cap("as studied in yeast and mammals", YELLOW, 34, -3.4)
        self.play(FadeIn(note), run_time=0.9)
        self.at("one cut frees")
        l1 = T("anaphase I: arms", 34, TEAL, weight=BOLD).move_to([-3.2, -1.6, 0])
        s1 = T("frees the homologs", 30, TEXT).move_to([-3.2, -2.3, 0])
        self.play(Indicate(n1, color=YELLOW, scale_factor=1.8), FadeIn(l1), FadeIn(s1), run_time=1.4)
        self.at("a later cut")
        l2 = T("anaphase II: centromeres", 34, TEAL, weight=BOLD).move_to([3.0, -1.6, 0])
        s2 = T("frees the sisters", 30, TEXT).move_to([3.0, -2.3, 0])
        self.play(Indicate(n2, color=YELLOW, scale_factor=1.8), FadeIn(l2), FadeIn(s2), run_time=1.4)
        self.finish()


class S14Failure(W):
    def construct(self):
        b, cell, eq, pt, pb, f1, f2 = equator_stage(self, glow=False)
        hd = [m for m in self.mobjects if isinstance(m, Text)][-1]
        self.at("in mouse eggs")
        hd_new = head("mouse eggs")
        self.play(ReplacementTransform(hd, hd_new), run_time=0.7)
        self.at("lost too early")
        lost = cap("centromere cohesin lost too early", RED, 32, -3.5)
        self.play(FadeIn(lost), LaggedStart(*[FadeOut(c, scale=1.6) for c in b.cen_rings], lag_ratio=0.15), run_time=1.6)
        self.at("reach meiosis")
        hd2 = head("meiosis II")
        s1 = Ch(BLUE, 4.4, False, 0.5, -2.4, 0.9)
        s2 = Ch(BLUE, 4.4, False, 0.5, 2.2, -0.8)
        self.play(FadeOut(VGroup(b.rods, b.dots, b.arm_rings, f1, f2, lost)), FadeOut(hd_new), FadeIn(hd2), FadeIn(s1.g), FadeIn(s2.g), run_time=1.5)
        drift(s1.g, 0.05, 1.5)
        drift(s2.g, 0.05, 1.5, 2.0)
        self.at("either pole")
        self.play(s1.g.animate.shift(UP * 0.2 + RIGHT * 0.3), s2.g.animate.shift(DOWN * 0.15 + LEFT * 0.3), run_time=0.5)
        self.play(s1.g.animate.shift(DOWN * 0.3), s2.g.animate.shift(UP * 0.3), run_time=0.5)
        self.at("at random")
        self.play(s1.g.animate.move_to([-1.2, 1.95, 0]), s2.g.animate.move_to([1.4, 1.35, 0]), run_time=1.8)
        self.at("eggs can")
        left = Ellipse(width=5.6, height=4.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-3.4, 0.3, 0])
        right = Ellipse(width=5.6, height=4.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([3.4, 0.3, 0])
        p1 = Ch(BLUE, 3.4, False, 0.5, -3.4, 0.8)
        p2 = Ch(BLUE, 3.4, False, 0.5, -3.4, -0.2)
        self.play(FadeOut(VGroup(cell, eq, pt, pb, s1.g, s2.g, hd2)), FadeIn(left), FadeIn(right), FadeIn(p1.g), FadeIn(p2.g), run_time=1.2)
        self.at("too many")
        tm = T("too many", 40, RED, weight=BOLD).move_to([-3.4, -2.35, 0])
        self.play(FadeIn(tm), run_time=0.5)
        self.at("too few")
        tf = T("too few", 40, RED, weight=BOLD).move_to([3.4, -2.35, 0])
        self.play(FadeIn(tf), run_time=0.5)
        self.finish()


class S15Takeaway(W):
    def construct(self):
        top = T("as studied in yeast and mammals", 30, TEXT).move_to([0, 3.55, 0])
        hl = T("anaphase I", 38, TEAL, weight=BOLD).move_to([-3.4, 2.95, 0])
        hr = T("anaphase II", 38, TEAL, weight=BOLD).move_to([3.4, 2.95, 0])
        divider = Line([0, -3.3, 0], [0, 3.3, 0], color=GREY, stroke_width=2)
        lb = Ch(BLUE, 5.0, True, 0.5, -3.4, 1.2)
        lo = Ch(ORANGE, 5.0, True, 0.5, -3.4, -1.2)
        rb = Ch(BLUE, 5.0, True, 0.5, 3.4, 0.0)
        arm_l = VGroup(*[ring_static(x, y, False, 1.3, 0.3) for y in (1.2, -1.2) for x in (-5.3, -1.5)])
        cen_l = VGroup(*[ring_static(x, y, True, 1.3, 0.3) for y in (1.2, -1.2) for x in (-4.02, -2.78)])
        cen_r = VGroup(*[ring_static(x, 0.0, True, 1.3, 0.3) for x in (3.4 - 0.62, 3.4 + 0.62)])
        for r in list(arm_l) + [c[1] for c in cen_l] + [c[1] for c in cen_r]:
            r.set_stroke(width=8)
        self.play(FadeIn(top), FadeIn(divider), FadeIn(lb.g), FadeIn(lo.g), FadeIn(rb.g), FadeIn(arm_l), FadeIn(cen_l), FadeIn(cen_r), run_time=1.6)
        self.at("two links")
        self.play(FadeIn(hl), FadeIn(hr), run_time=1.0)
        self.at("goes at anaphase")
        ca = T("arm cohesin cut", 32, YELLOW, weight=BOLD).move_to([-3.4, -3.0, 0])
        self.play(LaggedStart(*[FadeOut(r, scale=1.8) for r in arm_l], lag_ratio=0.12), FadeIn(ca), run_time=1.6)
        self.at("homologues part")
        self.play(lb.g.animate.shift(UP * 0.6), lo.g.animate.shift(DOWN * 0.6), cen_l[0:2].animate.shift(UP * 0.6), cen_l[2:4].animate.shift(DOWN * 0.6), run_time=2.0)
        self.at("goes at anaphase", nth=1)
        cc = T("centromere cohesin cut", 32, YELLOW, weight=BOLD).move_to([3.4, -3.0, 0])
        self.play(FadeOut(cen_r, scale=1.8), FadeIn(cc), run_time=1.4)
        self.at("sisters part")
        a, dd = split_chrom(self, rb, 1.0, small=0.26)
        self.play(*a, run_time=2.0)
        self.finish()


class S16End(EndCard):
    LINE = "Cutting arm cohesin frees homologs;\ncentromere cohesin holds sisters until anaphase II."
