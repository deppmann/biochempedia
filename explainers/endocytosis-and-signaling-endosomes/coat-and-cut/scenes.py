"""Section film: a coat, a reader, and a cut (endocytosis lesson, section on the clathrin-coated pit)

COLOR MAP (one colour per concept, whole film)
  BLUE   = the receptor (a bar through the membrane; head up and outside, longer tail down in the cytosol)
  ORANGE = the way in: clathrin (three-legged pinwheels), the adaptor AP2, the tail sequence, dynamin
  TEAL   = the lipid PIP2
  YELLOW = LDL particles
  RED    = what is absent or broken (crossed gaps, the swapped residue, no uptake)
  GREEN  = the changed-residue label is NOT green; green is unused
  GREY   = membranes, labels, structure
No molecular structures: receptor = bar, membrane = thick line, clathrin = three short spokes, adaptor and dynamin
= blocks, LDL = disc.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
MEMC = "#9AA3B2"


def V(x=0.0, y=0.0):
    return np.array([x, y, 0.0])


def pinwheel(c, size=0.4, rot=0.0, color=ORANGE, sw=5):
    g = VGroup()
    for a in (90, 210, 330):
        d = np.radians(a) + rot
        g.add(Line(c, c + size * V(np.cos(d), np.sin(d)), color=color, stroke_width=sw,
                   cap_style=CapStyleType.ROUND))
    return g


def cage_row(xs, ys, size=0.4):
    return VGroup(*[pinwheel(V(x, y), size, rot=0.35 * i) for i, (x, y) in enumerate(zip(xs, ys))])


def receptor(x, ym, k=1.0, tail_col=BLUE):
    """a bar through the membrane at height ym: head up 0.45k, tail down 1.35k."""
    head = Line(V(x, ym), V(x, ym + 0.45 * k), color=BLUE, stroke_width=11, cap_style=CapStyleType.ROUND)
    tail = Line(V(x, ym), V(x, ym - 1.35 * k), color=tail_col, stroke_width=11, cap_style=CapStyleType.ROUND)
    return VGroup(tail, head)


def membrane(y, x0=-6.2, x1=6.2, col=MEMC):
    return Line(V(x0, y), V(x1, y), color=col, stroke_width=9)


# shared layout for scenes 1 and 2
YM = 1.7                              # membrane height
CAGE_X = np.linspace(-4.2, 4.2, 11)
CAGE_Y = -2.5 + 0.055 * CAGE_X ** 2 - 0.0


def base_scene(self, rec=True):
    m = membrane(YM)
    r = receptor(0, YM)
    cage = cage_row(CAGE_X, CAGE_Y)
    return m, r, cage


class S00Title(TitleCard):
    LESSON = "Endocytosis and Signaling Endosomes"
    TITLE = "A Coat, a Reader, and a Cut"


class S01Cage(SpokenScene):
    def construct(self):
        m, r, cage = base_scene(self)
        one = pinwheel(V(0, -0.5), 0.9, color=ORANGE, sw=9)
        name = T("clathrin", size=32, color=ORANGE).next_to(one, RIGHT, buff=0.6)
        self.at("Clathrin is a protein")
        self.play(FadeIn(one, scale=0.6), FadeIn(name), run_time=min(self.beat(0.08), 1.0))
        self.play(Rotate(one, angle=2 * PI / 3, about_point=V(0, -0.5)), run_time=min(self.beat(0.1), 1.0))
        self.at("Many copies lock")
        self.play(FadeOut(name), FadeOut(one), FadeIn(cage, lag_ratio=0.12), run_time=min(self.beat(0.18), 1.0))
        mlab = T("membrane", size=26, color=GREY).move_to(V(-4.6, YM + 0.55))
        clab = T("clathrin cage, inner face", size=26, color=ORANGE).move_to(V(0, -3.35))
        self.at("curved cage")
        self.play(Create(m), FadeIn(mlab), FadeIn(r), FadeIn(clab), run_time=min(self.beat(0.12), 1.0))
        # gaps: crossed
        self.at("Yet clathrin touches neither")
        g1 = DashedLine(V(-2.6, YM - 0.15), V(-2.6, -1.55), color=RED, stroke_width=4)
        x1 = VGroup(*[Line(V(-2.6, -0.1) + d, V(-2.6, -0.1) - d, color=RED, stroke_width=6)
                      for d in (V(0.22, 0.22), V(0.22, -0.22))])
        g2 = DashedLine(V(0, YM - 1.45), V(0, -1.7), color=RED, stroke_width=4)
        x2 = VGroup(*[Line(V(0, -0.45) + d, V(0, -0.45) - d, color=RED, stroke_width=6)
                      for d in (V(0.22, 0.22), V(0.22, -0.22))])
        l1 = T("not touching membrane", size=24, color=RED).next_to(x1, LEFT, buff=0.2)
        l2 = T("not touching cargo", size=24, color=RED).next_to(x2, RIGHT, buff=0.2)
        self.play(Create(g1), FadeIn(x1), FadeIn(l1), run_time=min(self.beat(0.1), 1.0))
        self.at("nor the cargo")
        self.play(Create(g2), FadeIn(x2), FadeIn(l2), run_time=min(self.beat(0.1), 1.0))
        q = chip("what does?", color=YELLOW, size=34).move_to(V(4.3, 0.6))
        self.at("So what does")
        self.play(FadeIn(q, scale=0.6), run_time=min(self.beat(0.08), 1.0))
        self.finish()


class S02Adaptor(SpokenScene):
    def construct(self):
        m, r, cage = base_scene(self)
        mlab = T("membrane", size=26, color=GREY).move_to(V(-4.6, YM + 0.55))
        clab = T("clathrin cage", size=26, color=ORANGE).move_to(V(0, -3.35))
        tick = Line(V(0, YM - 1.35), V(0, YM - 0.95), color=ORANGE, stroke_width=17, cap_style=CapStyleType.ROUND)
        self.add(m, mlab, r, cage, clab)
        # PIP2 lipid: teal dots in the membrane, inner face
        pip = VGroup(*[Dot(V(x, YM - 0.12), radius=0.12, color=TEAL) for x in (-1.3, 1.3)])
        pip_lab = T("PIP2", size=26, color=TEAL).move_to(V(2.3, YM - 0.55))
        seq_lab = T("tail sequence", size=26, color=ORANGE).move_to(V(-2.6, YM - 1.2))
        ada = VGroup(RoundedRectangle(corner_radius=0.15, width=1.5, height=0.8, stroke_color=ORANGE,
                                      stroke_width=3, fill_color=ORANGE, fill_opacity=0.28),
                     T("AP2", size=30, color=ORANGE)).move_to(V(0, -0.85))
        ada[1].move_to(ada[0])
        self.at("proteins do")
        self.play(FadeIn(ada, scale=0.7, shift=UP * 0.4), run_time=min(self.beat(0.1), 1.0))
        self.at("lipid")
        self.play(FadeIn(pip), FadeIn(pip_lab), run_time=0.4)
        grip1 = Line(ada.get_top() + RIGHT * 0.5, V(1.3, YM - 0.22), color=TEAL, stroke_width=5)
        grip1b = Line(ada.get_top() + RIGHT * 0.5, V(1.3, YM - 0.22), color=TEAL, stroke_width=5)
        self.play(Create(grip1), run_time=0.4)
        self.at("a short sequence")
        self.play(FadeIn(tick), FadeIn(seq_lab), run_time=min(self.beat(0.06), 1.0))
        grip2 = Line(ada.get_top() + LEFT * 0.4, V(-0.12, YM - 1.2), color=ORANGE, stroke_width=5)
        self.play(Create(grip2), run_time=min(self.beat(0.06), 1.0))
        self.at("and clathrin")
        grip3 = Line(ada.get_bottom(), V(0, -2.3), color=ORANGE, stroke_width=5)
        self.play(Create(grip3), run_time=min(self.beat(0.07), 1.0))
        self.at("So a receptor enters")
        box = RoundedRectangle(corner_radius=0.2, width=11.0, height=0.8, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.10).move_to(V(0, 3.05))
        txt = T("the adaptor reads the tail sequence", size=30, color=YELLOW).move_to(box)
        self.play(FadeIn(box), FadeIn(txt), Indicate(tick, color=YELLOW), run_time=min(self.beat(0.12), 1.0))
        self.finish()


class S03Jd(SpokenScene):
    def construct(self):
        YS = 0.3
        xs = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
        m = membrane(YS, -6.3, 6.3)
        recs = VGroup(*[receptor(x, YS, 0.8) for x in xs])
        ldls = VGroup(*[Dot(V(x, YS + 1.25), radius=0.26, color=YELLOW) for x in xs])
        ldl_lab = T("LDL", size=28, color=YELLOW).next_to(ldls[5], RIGHT, buff=0.15)
        who = T("Brown and Goldstein", size=34, color=TEXT).move_to(V(-3.3, 3.2))
        pat = chip("patient J.D.", color=GREY, size=30).move_to(V(3.2, 3.2))
        self.at("Brown and Goldstein")
        self.play(FadeIn(who), run_time=min(self.beat(0.07), 1.0))
        self.at("a patient known")
        self.play(FadeIn(pat), Create(m), FadeIn(recs, lag_ratio=0.15), run_time=min(self.beat(0.1), 1.0))
        # bind
        up = [Dot(V(x, YS + 2.0), radius=0.26, color=YELLOW) for x in xs]
        self.at("could bind")
        for d, x in zip(up, xs):
            d.move_to(V(x, YS + 2.0))
        self.add(*up)
        self.play(*[d.animate.move_to(V(x, YS + 0.72)) for d, x in zip(up, xs)], run_time=min(self.beat(0.1), 1.0))
        lab = T("LDL", size=28, color=YELLOW).next_to(up[5], RIGHT, buff=0.15)
        self.play(FadeIn(lab), run_time=min(self.beat(0.03), 1.0))
        # scattered
        self.at("scattered over the surface")
        br = Line(V(-5.6, YS - 1.75), V(5.6, YS - 1.75), color=GREY, stroke_width=3)
        brl = T("scattered over the surface", size=28, color=GREY).move_to(V(0, YS - 2.15))
        self.play(Create(br), FadeIn(brl), run_time=min(self.beat(0.08), 1.0))
        # no pits
        self.at("instead of gathering")
        pit = VGroup(); pit_x = VGroup()
        pl = T("not gathered into pits", size=28, color=RED).move_to(V(0, YS - 2.15))
        self.play(FadeOut(brl), FadeIn(pl), br.animate.set_color(RED), run_time=0.6)
        self.at("could not take")
        n = T("cells could not take LDL in", size=30, color=RED).move_to(V(0, YS - 2.15))
        self.play(FadeOut(pl), FadeIn(n), run_time=min(self.beat(0.05), 1.0))
        self.at("The fault was later")
        keep = VGroup(m, recs, *up, lab, br, n)
        self.play(FadeOut(keep), run_time=0.6)
        big_tail = Line(V(-1.6, 1.3), V(-1.6, -2.3), color=BLUE, stroke_width=24, cap_style=CapStyleType.ROUND)
        tl = T("receptor tail", size=30, color=BLUE).next_to(big_tail, LEFT, buff=0.35)
        self.play(Create(big_tail), FadeIn(tl), run_time=0.8)
        self.at("one tyrosine")
        tyr = chip("tyrosine", color=ORANGE, size=34).move_to(V(1.3, -0.5))
        link = Line(V(-1.45, -0.5), tyr.get_left(), color=ORANGE, stroke_width=4)
        self.play(FadeIn(tyr, shift=LEFT * 0.3), Create(link), run_time=0.6)
        self.at("replaced by cysteine")
        cys = chip("cysteine", color=RED, size=34).move_to(V(1.3, -0.5))
        cap = T("one residue changed", size=28, color=RED).next_to(cys, DOWN, buff=0.35)
        link2 = Line(V(-1.45, -0.5), cys.get_left(), color=RED, stroke_width=4)
        self.play(Transform(tyr, cys), Transform(link, link2), FadeIn(cap), run_time=0.8)
        self.finish()


def pit_points(d, ncirc=48):
    """membrane polyline (left flat, pit, right flat). d=0 shallow dome, d=1 flask on a thin neck."""
    R, nh = 1.5, 0.45
    cy = 0.5 - np.sqrt(R * R - nh * nh)
    # deep pit path (left neck top -> down -> circle ccw -> up)
    dp = [V(-nh, 2.0), V(-nh, 1.5), V(-nh, 1.0), V(-nh, 0.5)]
    a0 = np.arctan2(0.5 - cy, -nh)
    a1 = np.arctan2(0.5 - cy, nh) + 2 * np.pi
    for a in np.linspace(a0, a1, ncirc)[1:-1]:
        dp.append(V(R * np.cos(a), cy + R * np.sin(a)))
    dp += [V(nh, 0.5), V(nh, 1.0), V(nh, 1.5), V(nh, 2.0)]
    n = len(dp)
    # shallow path with the same count
    xs = np.linspace(-2.2, 2.2, n)
    sh = [V(x, 2.0 - 0.45 * max(0, 1 - (x / 2.2) ** 2) ** 0.8) for x in xs]
    pts = [(1 - d) * np.array(s) + d * np.array(p) for s, p in zip(sh, dp)]
    left = [V(x, 2.0) for x in np.linspace(-6.4, pts[0][0] - 0.01, 6)[:-1]]
    right = [V(x, 2.0) for x in np.linspace(pts[-1][0] + 0.01, 6.4, 6)[1:]]
    return left + pts + right, cy


def pit_mob(d):
    pts, cy = pit_points(d)
    return VMobject(color=MEMC, stroke_width=9).set_points_as_corners(pts)


class S04Cut(SpokenScene):
    def construct(self):
        R = 1.5
        _, cy = pit_points(1)
        pit0 = pit_mob(0.0)
        # coat: pinwheels along the outer face of the flask
        shell_c = V(0, cy)
        coat = VGroup()
        angs = np.linspace(np.radians(130), np.radians(410), 11)
        for i, a in enumerate(angs):
            coat.add(pinwheel(shell_c + (R + 0.42) * V(np.cos(a), np.sin(a)), 0.3, rot=0.4 * i))
        shallow_coat = coat.copy()
        # a few pinwheels on the shallow dome at start
        sh_cage = cage_row(np.linspace(-1.6, 1.6, 5), [1.5 - 0.45 * max(0, 1 - (x / 2.2) ** 2) ** 0.8 - 0.55 for x in np.linspace(-1.6, 1.6, 5)], 0.3)
        self.at("A pit deepens")
        self.add(pit0)
        self.play(FadeIn(sh_cage), run_time=min(self.beat(0.05), 1.0))
        pit1 = pit_mob(1.0)
        self.play(Transform(pit0, pit1), Transform(sh_cage, coat), run_time=min(self.beat(0.2), 1.0))
        self.at("thin neck")
        nlab = T("thin neck", size=28, color=GREY).move_to(V(2.6, 1.0))
        narr = Arrow(nlab.get_left() + LEFT * 0.05, V(0.55, 1.0), buff=0.1, color=GREY, stroke_width=3,
                     max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(nlab), Create(narr), run_time=min(self.beat(0.05), 1.0))
        # dynamin
        self.at("Dynamin")
        dl = chip("dynamin", color=ORANGE, size=28).move_to(V(-3.3, 2.9))
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.34, stroke_color=ORANGE,
                                           stroke_width=3, fill_color=ORANGE, fill_opacity=0.5)
                          for _ in range(4)])
        starts = [V(-1.9, 1.3), V(-1.9, 0.7), V(1.9, 1.3), V(1.9, 0.7)]
        for b, p in zip(blocks, starts):
            b.move_to(p)
        self.play(FadeIn(dl), FadeIn(blocks), FadeOut(nlab), FadeOut(narr), run_time=min(self.beat(0.07), 1.0))
        self.at("collar around the neck")
        ends = [V(-0.75, 1.35), V(-0.75, 0.95), V(0.75, 1.35), V(0.75, 0.95)]
        self.play(*[b.animate.move_to(p) for b, p in zip(blocks, ends)], run_time=min(self.beat(0.1), 1.0))
        self.at("hydrolyzes")
        gtp = chip("GTP", color=YELLOW, size=30).move_to(V(3.2, 2.9))
        self.play(FadeIn(gtp), run_time=min(self.beat(0.04), 1.0))
        self.at("the neck is cut")
        flat = VMobject(color=MEMC, stroke_width=9).set_points_as_corners([V(-6.4, 2.0), V(6.4, 2.0)])
        ring = Circle(radius=R, color=MEMC, stroke_width=9).move_to(shell_c)
        self.remove(pit0)
        self.add(flat, ring)
        self.play(FadeOut(gtp), FadeOut(blocks), FadeOut(dl),
                  run_time=min(self.beat(0.1), 1.0))
        # coat stripped
        self.at("coat is then stripped")
        self.play(*[p.animate.shift(unit_out(p.get_center() - shell_c) * 1.6).set_opacity(0) for p in sh_cage],
                  run_time=min(self.beat(0.1), 1.0))
        bare = T("bare vesicle", size=28, color=GREY).move_to(V(-3.4, cy))
        self.at("bare vesicle")
        self.play(FadeIn(bare), run_time=min(self.beat(0.04), 1.0))
        target = Circle(radius=1.9, color=MEMC, stroke_width=9).move_to(V(4.5, cy))
        tlab = T("its target", size=28, color=GREY).move_to(V(4.5, cy))
        self.at("fuse with its target")
        self.play(FadeIn(target), FadeIn(tlab), FadeOut(bare), run_time=0.6)
        self.play(ring.animate.shift(RIGHT * 1.1), run_time=1.0)
        self.finish()


def unit_out(v):
    return v / (np.linalg.norm(v) + 1e-9)


class S05End(EndCard):
    LINE = "A receptor enters a pit because an adaptor reads its tail."
