"""Touch and pain: two pathways, two crossings (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
One flat box-and-lane schematic, no body outline and no cord cross-section: the patient's RIGHT side is
the upper half, the patient's LEFT side the lower half, the midline is the dashed line between them, and
the lanes run left to right from the dorsal root toward the brain. Facts are the lesson's own: fine touch
crosses in the caudal medulla, pain and temperature cross in the cord within a segment or two; a right
hemisection at T10 takes fine touch, vibration, position sense and strength on the right below T10 and
pain and temperature on the left from about T11 to T12 down.

COLOR MAP (one color per concept, whole video)
  BLUE   = the fine touch / vibration / position sense pathway (dorsal column - medial lemniscus)
  ORANGE = the pain and temperature pathway (spinothalamic)
  YELLOW = the moving signal and the point where a pathway crosses the midline
  RED    = the cut, and the words "right half" that name it
  GREEN  = weakness (corticospinal tract)
  GREY   = structure: midline, side tags, dorsal root and thalamus boxes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TOUCH, PAIN, CUT, SIG, STRUCT, WEAK = BLUE, ORANGE, RED, YELLOW, GREY, GREEN

YT, YP = 1.95, 1.0        # lane heights on the patient's right side (negated for the left side)
XS = -4.35                # where the two lanes leave the dorsal root
CUT_X = -0.85             # the cut sits here in the right half
CROSS_P = (-1.6, 0.0)     # pain lane crosses the midline here (in the cord)
CROSS_T = (2.25, 0.0)     # touch lane crosses the midline here (in the medulla)


def bchip(text, color=BLUE, size=22, pad=0.2):
    """chip with an opaque backing; '\\n' makes a centred two-line label."""
    label = VGroup(*[T(l, size, color) for l in text.split("\n")]).arrange(DOWN, buff=0.07)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    g = VGroup(back, box, label.move_to(box))
    g.set_z_index(6)
    return g


def btext(text, size=22, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    g = VGroup(back, t)
    g.set_z_index(6)
    return g


class Track(VGroup):
    """A lane: a polyline with an arrow tip and a background-coloured halo so crossings read as bridges."""

    def __init__(self, pts, color, z, tip=True, w=6):
        super().__init__()
        self.pts = [np.array([x, y, 0.0]) for x, y in pts]
        self.halo = VMobject(stroke_color=BG, stroke_width=w + 12).set_points_as_corners(self.pts)
        self.line = VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(self.pts)
        d = self.pts[-1] - self.pts[-2]
        ang = np.arctan2(d[1], d[0])
        L, W = 0.24, 0.15
        tri = Polygon([0, 0, 0], [-L, W, 0], [-L, -W, 0], stroke_width=0, fill_color=color, fill_opacity=1)
        tri.rotate(ang, about_point=ORIGIN).shift(self.pts[-1])
        self.tip = tri if tip else VMobject()
        self.halo.set_z_index(z - 1)
        self.line.set_z_index(z)
        self.tip.set_z_index(z)
        self.add(self.halo, self.line, self.tip)

    def split(self, xc):
        """(before, after) as point lists, cut at x = xc."""
        pts = [(p[0], p[1]) for p in self.pts]
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            if x0 <= xc <= x1 and x1 > x0:
                y = y0 + (y1 - y0) * (xc - x0) / (x1 - x0)
                return pts[:i + 1] + [(xc, y)], [(xc, y)] + pts[i + 1:]
        raise ValueError("no crossing")


def lane_path(*tracks):
    pts = []
    for t in tracks:
        pts += [tuple(p[:2]) for p in t.pts]
    m = VMobject().set_points_as_corners([np.array([x, y, 0.0]) for x, y in pts])
    return m


class Net:
    """Every piece of the schematic, built once per scene; the scene adds what it needs."""

    def __init__(self):
        self.mid = DashedLine([-6.25, 0, 0], [6.25, 0, 0], color=GREY, stroke_width=2.5, dash_length=0.15)
        self.mid.set_z_index(0)
        self.mid_lbl = btext("midline", 22, GREY).move_to([5.55, 0, 0])
        self.tag = {1: T("PATIENT'S RIGHT SIDE", 22, GREY).move_to([-6.2, 2.5, 0], aligned_edge=LEFT),
                    -1: T("PATIENT'S LEFT SIDE", 22, GREY).move_to([-6.2, -2.5, 0], aligned_edge=LEFT)}
        self.root, self.dh, self.nuc, self.thal, self.ctx = {}, {}, {}, {}, {}
        self.tA, self.tB, self.tC, self.pA, self.pB = {}, {}, {}, {}, {}
        for s in (1, -1):
            r = bchip("skin nerve,\ndorsal root", STRUCT)
            r.next_to(np.array([XS, s * 1.475, 0]), LEFT, buff=0)
            self.root[s] = r
            self.dh[s] = bchip("dorsal horn", PAIN).move_to([-2.9, s * YP, 0])
            self.nuc[s] = bchip("gracile or\ncuneate nucleus", TOUCH).move_to([0.75, s * YT, 0])
            box = RoundedRectangle(corner_radius=0.14, width=1.5, height=1.95, stroke_color=STRUCT, stroke_width=2.5,
                                   fill_color=STRUCT, fill_opacity=0.12).move_to([3.75, s * 1.475, 0])
            lab = T("thalamus", 22, STRUCT).move_to(box)
            self.thal[s] = VGroup(box, lab)
            self.ctx[s] = bchip("cortex", TOUCH).move_to([5.6, s * YT, 0])
        TH_L, TH_R = 3.0, 4.5
        for s in (1, -1):
            nl, nr = self.nuc[s][1].get_left()[0], self.nuc[s][1].get_right()[0]
            dl, dr = self.dh[s][1].get_left()[0], self.dh[s][1].get_right()[0]
            cl = self.ctx[-s][1].get_left()[0]
            self.tA[s] = Track([(XS, s * YT), (nl, s * YT)], TOUCH, 2)
            self.tB[s] = Track([(nr, s * YT), (2.55, -s * YT), (TH_L, -s * YT)], TOUCH, 2)
            self.tC[s] = Track([(TH_R, -s * YT), (cl, -s * YT)], TOUCH, 2)
            self.pA[s] = Track([(XS, s * YP), (dl, s * YP)], PAIN, 4)
            self.pB[s] = Track([(dr, s * YP), (-1.2, -s * YP), (TH_L, -s * YP)], PAIN, 4)

    def base(self):
        return [self.mid, self.mid_lbl, self.tag[1], self.tag[-1]]


def _cache(m):
    if not hasattr(m, "_o0"):
        m._o0 = (m.get_fill_opacity(), m.get_stroke_opacity())


def op(mob, f):
    """set overall opacity to f x the original, leaving unfilled shapes unfilled."""
    for m in mob.family_members_with_points():
        _cache(m)
        m.set_fill(opacity=m._o0[0] * f)
        m.set_stroke(opacity=m._o0[1] * f)
    return mob


def fade_to(mob, f0, f1, rt=0.5):
    return UpdateFromAlphaFunc(mob, lambda m, a: op(m, f0 + (f1 - f0) * a), run_time=rt)


def pulse(scene, mob, k=1.08, rt=0.5):
    scene.play(mob.animate.scale(k), run_time=rt / 2, rate_func=smooth)
    scene.play(mob.animate.scale(1 / k), run_time=rt / 2, rate_func=smooth)


def ring(p, r=0.26):
    c = Circle(radius=r, stroke_color=SIG, stroke_width=5, fill_opacity=0).move_to([p[0], p[1], 0])
    c.set_z_index(9)
    return c


def dot():
    d = Dot(radius=0.13, color=SIG)
    d.set_z_index(9)
    return d


def fly(d, path, rt):
    return MoveAlongPath(d, path, rate_func=linear, run_time=rt)


def draw(scene, tr, rt=0.7):
    scene.play(Create(tr.halo, rate_func=linear), Create(tr.line, rate_func=linear), run_time=rt)
    scene.play(FadeIn(tr.tip), run_time=0.12)


class S00Title(TitleCard):
    LESSON = "Touch and Pain"
    TITLE = "Two Pathways, Two Crossings"


# ---------------------------------------------------------------------------------------------
class S01Cut(SpokenScene):
    """the question, then the side tags and midline, then one dorsal root with touch and pain leaving it."""

    def construct(self):
        n = Net()
        q1 = T("Cut the right half of the spinal cord at T10.", 38, font=TITLE_FONT, t2c={"right half": RED})
        q2 = T("What is lost, and on which side?", 38, font=TITLE_FONT)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.45)
        fit(q, max_w=12.0)
        q1.move_to(q.get_center())
        self.play(Write(q1), run_time=self.beat(0.16))
        self.at("What is lost")
        q2.next_to(q1, DOWN, buff=0.45)
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.7)
        self.at("The answer depends")
        self.play(FadeOut(q1), FadeOut(q2), FadeIn(n.mid), FadeIn(n.mid_lbl), run_time=0.8)
        self.play(FadeIn(n.tag[1]), FadeIn(n.tag[-1]), run_time=0.6)
        self.at("two pathways")
        q1m, q2m = ring(CROSS_P), ring(CROSS_T)
        qm1 = T("?", 26, SIG, weight=BOLD).move_to(q1m)
        qm2 = T("?", 26, SIG, weight=BOLD).move_to(q2m)
        self.play(Create(q1m), Create(q2m), FadeIn(qm1), FadeIn(qm2), run_time=0.8)
        self.at("same dorsal root")
        self.play(FadeIn(n.root[1], shift=RIGHT * 0.2), run_time=0.6)
        lt = btext("touch", 24, TOUCH).move_to([-2.0, 2.4, 0])
        lp = btext("pain", 24, PAIN).move_to([-2.0, 0.55, 0])
        self.at("part company")
        t, p = n.tA[1], n.pA[1]
        stub_t = Track([(XS, YT), (-2.2, YT)], TOUCH, 2)
        stub_p = Track([(XS, YP), (-2.2, YP)], PAIN, 4)
        self.play(Create(stub_t.halo), Create(stub_t.line), Create(stub_p.halo), Create(stub_p.line), run_time=0.9)
        self.play(FadeIn(stub_t.tip), FadeIn(stub_p.tip), FadeIn(lt), FadeIn(lp), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Touch(SpokenScene):
    """the dorsal column - medial lemniscus lane: same side up the cord, synapse in the medulla, cross, thalamus, cortex."""

    def construct(self):
        n = Net()
        self.add(*n.base(), n.root[1])
        lbl = VGroup(*[T(s, 22, TOUCH) for s in ("fine touch, vibration,", "position sense")]).arrange(DOWN, buff=0.05)
        lbl.move_to([-2.75, 1.45, 0])
        stub = Track([(XS, YT), (-3.2, YT)], TOUCH, 2)
        self.add(stub)
        self.play(FadeIn(lbl), run_time=0.6)
        d = dot().move_to([XS, YT, 0])
        a = n.tA[1]
        # --- up the cord on the same side, no synapse ---------------------------------
        self.at("climbs on the same side")
        self.play(FadeOut(stub), run_time=0.01)
        self.play(Create(a.halo), Create(a.line), FadeIn(d), run_time=0.9)
        self.play(FadeIn(a.tip), run_time=0.1)
        self.at("does not synapse")
        ns = btext("no synapse", 22, GREY).move_to([-2.0, 2.4, 0])
        self.play(FadeIn(ns), run_time=0.5)
        self.play(d.animate.move_to([-0.6, YT, 0]), run_time=0.9, rate_func=linear)
        # --- synapse in the nucleus -----------------------------------------------------
        self.at("gracile")
        self.play(FadeOut(ns), FadeIn(n.nuc[1], scale=0.9), run_time=0.6)
        pulse(self, n.nuc[1], 1.08, 0.5)
        # --- cross the midline --------------------------------------------------------------
        self.at("cross the midline")
        self.play(FadeIn(n.thal[-1]), run_time=0.4)
        b = n.tB[1]
        self.play(Create(b.halo, rate_func=linear), Create(b.line, rate_func=linear), fly(d, lane_path(b), 0.9), run_time=0.9)
        self.play(FadeIn(b.tip), run_time=0.12)
        cr = ring(CROSS_T)
        self.play(Create(cr), run_time=0.3)
        # --- thalamus and cortex ----------------------------------------------------------------
        self.at("climb to the thalamus")
        pulse(self, n.thal[-1], 1.05, 0.4)
        self.at("relays to the cortex")
        c = n.tC[1]
        self.play(Create(c.halo, rate_func=linear), Create(c.line, rate_func=linear), fly(d, lane_path(c), 0.7), run_time=0.7)
        self.play(FadeIn(c.tip), FadeIn(n.ctx[-1], scale=0.9), FadeOut(d), run_time=0.5)
        self.at("crosses in the medulla")
        xl = btext("crosses in the medulla", 24, SIG).move_to([-0.05, 0, 0])
        self.play(FadeIn(xl), Indicate(cr, color=SIG, scale_factor=1.5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Pain(SpokenScene):
    """the spinothalamic lane: synapse in the dorsal horn, cross in the cord, climb the opposite side to the thalamus."""

    def construct(self):
        n = Net()
        touch = VGroup(n.tA[1], n.nuc[1], n.tB[1], n.tC[1], n.ctx[-1])
        self.add(*n.base(), n.root[1], n.thal[-1], touch)
        op(touch, 0.2)
        op(n.thal[-1], 0.5)
        lp = VGroup(*[T(s, 22, PAIN) for s in ("pain, temperature",)])
        lp.move_to([-5.1, 0.42, 0])
        d = dot().move_to([XS, YP, 0])
        self.play(FadeIn(lp), run_time=0.6)
        a = n.pA[1]
        self.at("first axon synapses")
        self.play(Create(a.halo), Create(a.line), FadeIn(d), run_time=0.8)
        self.play(FadeIn(a.tip), FadeIn(n.dh[1], scale=0.9), run_time=0.4)
        pulse(self, n.dh[1], 1.08, 0.5)
        self.at("second axon crosses")
        b = n.pB[1]
        self.play(Create(b.halo, rate_func=linear), Create(b.line, rate_func=linear), fly(d, lane_path(b), 1.3), run_time=1.3)
        cr = ring(CROSS_P)
        xl = btext("crosses in the spinal cord", 24, SIG).move_to([-3.6, -0.05, 0])
        self.play(Create(cr), FadeIn(xl), run_time=0.6)
        self.at("anterior white commissure")
        self.play(Indicate(cr, color=SIG, scale_factor=1.5), run_time=0.8)
        self.at("opposite side")
        self.play(FadeIn(b.tip), run_time=0.12)
        self.play(fade_to(n.thal[-1], 0.5, 1.0, 0.4), FadeOut(d))
        pulse(self, n.thal[-1], 1.05, 0.4)
        self.at("crosses in the spinal cord")
        self.play(Indicate(cr, color=SIG, scale_factor=1.5), xl.animate.scale(1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Hemi(SpokenScene):
    """the cut across the right half: the right touch lane and the left pain lane both run into it."""

    def construct(self):
        n = Net()
        self.add(*n.base(), n.root[1])
        tb, ta_after = n.tA[1].split(CUT_X)
        t1 = Track(tb, TOUCH, 2, tip=False)
        t2 = Track(ta_after, TOUCH, 2)
        beyond_t = VGroup(t2, n.nuc[1], n.tB[1], n.thal[-1], n.tC[1], n.ctx[-1])
        self.add(t1, beyond_t)
        pb1p, pb2p = n.pB[-1].split(CUT_X)
        p1 = Track(pb1p, PAIN, 4, tip=False)
        p2 = Track(pb2p, PAIN, 4)
        beyond_p = VGroup(p2, n.thal[1])
        cut = Line([CUT_X, 2.7, 0], [CUT_X, 0.45, 0], color=CUT, stroke_width=11)
        cut.set_z_index(8)
        cut_lbl = T("cut: right half, T10", 24, CUT).move_to([CUT_X, 3.05, 0])
        self.at("Now make the cut")
        self.play(Create(cut), run_time=0.7)
        self.play(FadeIn(cut_lbl), run_time=0.4)
        # --- touch from the right side ------------------------------------------------------------
        self.at("right side of the body")
        nc = T("not yet crossed", 24, TOUCH).move_to([-2.2, 1.5, 0])
        d = dot().move_to([XS, YT, 0])
        self.play(FadeIn(nc), FadeIn(d), run_time=0.4)
        self.play(fly(d, lane_path(t1), 1.8), run_time=1.8)
        self.at("so the cut severs")
        self.play(Flash(Dot([CUT_X, YT, 0]), color=CUT, flash_radius=0.45, line_length=0.18), FadeOut(d),
                  fade_to(beyond_t, 1.0, 0.18, 0.8), run_time=0.8)
        # --- pain from the left side -------------------------------------------------------------------
        self.at("left side of the body")
        self.play(FadeIn(n.root[-1]), FadeIn(n.pA[-1]), FadeIn(n.dh[-1]), run_time=0.6)
        op(beyond_p, 0.18)
        self.play(FadeIn(p1), FadeIn(beyond_p), run_time=0.01)
        d2 = dot().move_to([XS, -YP, 0])
        self.play(FadeIn(d2), run_time=0.2)
        self.at("already crossed")
        pc = btext("already crossed", 24, PAIN).move_to([-3.6, 0.0, 0])
        self.play(FadeIn(pc), fly(d2, lane_path(n.pA[-1], p1), 2.0), run_time=2.0)
        self.at("severs those")
        self.play(Flash(Dot([CUT_X, YP, 0]), color=CUT, flash_radius=0.45, line_length=0.18), FadeOut(d2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Lost(SpokenScene):
    """what is lost on each side, and where the left loss begins (a head-to-feet level strip under each block)."""

    def construct(self):
        n = Net()
        self.add(n.mid, n.mid_lbl)
        x0 = -5.9
        SX0, SX1 = -4.9, 5.0       # level strip: head at the left end, feet at the right end
        XT10, XT11 = -0.6, 0.5     # schematic positions of T10 and of "about T11 to T12"

        def line(txt, color, size=28, weight=NORMAL):
            return T(txt, size, color, weight=weight).move_to([0, 0, 0])

        def put(m, y):
            m.align_to([x0, 0, 0], LEFT).set_y(y)
            return m

        def strip(y):
            frame = RoundedRectangle(corner_radius=0.1, width=SX1 - SX0, height=0.5, stroke_color=GREY, stroke_width=2.5)
            frame.move_to([(SX0 + SX1) / 2, y, 0])
            hd = T("head", 22, GREY).next_to(frame, LEFT, buff=0.15)
            ft = T("feet", 22, GREY).next_to(frame, RIGHT, buff=0.15)
            return VGroup(frame, hd, ft)

        def lost(x_from, x_to, y, a=0.6):
            r = Rectangle(width=x_to - x_from, height=0.5, stroke_width=0, fill_color=CUT, fill_opacity=a)
            return r.move_to([(x_from + x_to) / 2, y, 0])

        h1 = put(line("Patient's right side, below T10", TEXT, 28, BOLD), 3.0)
        r1 = put(line("Fine touch, vibration, position sense: lost", TOUCH), 2.45)
        r2 = put(line("Weakness (corticospinal tract)", WEAK), 1.9)
        su = strip(1.2)
        lu = lost(XT10, SX1, 1.2)
        tu = T("T10", 22, TEXT).move_to([XT10, 0.7, 0])
        h2 = put(line("Patient's left side, from about T11 to T12 down", TEXT, 28, BOLD), -0.6)
        l1 = put(line("Pain and temperature: lost", PAIN), -1.15)
        l2 = put(line("Some fibres cross above the cut and escape it", GREY, 24), -1.65)
        sl = strip(-2.4)
        ramp = lost(XT11, XT11 + 0.8, -2.4, 0.25)
        ll = lost(XT11 + 0.8, SX1, -2.4)
        tl = T("about T11 to T12", 22, TEXT).move_to([XT11 + 0.4, -2.9, 0])
        t10l = DashedLine([XT10, -2.15, 0], [XT10, -2.65, 0], color=GREY, stroke_width=2.5)
        t10u = Line([XT10, 0.95, 0], [XT10, 1.45, 0], color=CUT, stroke_width=5)

        self.play(FadeIn(h1, shift=RIGHT * 0.2), FadeIn(su), run_time=0.7)
        self.at("fine touch")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), Create(t10u), FadeIn(tu), run_time=0.6)
        self.play(GrowFromEdge(lu, LEFT), run_time=0.8)
        self.at("lost on the left")
        self.play(FadeIn(h2, shift=RIGHT * 0.2), FadeIn(sl), run_time=0.6)
        self.play(FadeIn(l1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("a little lower")
        self.play(FadeIn(t10l), FadeIn(ramp), GrowFromEdge(ll, LEFT), FadeIn(tl), run_time=1.0)
        self.at("cross above the cut")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), run_time=0.7)
        self.at("Weakness is")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """touch and strength on one side, pain on the other; the rule of the two crossings."""

    def construct(self):
        head = T("Brown-Séquard pattern", 42, font=TITLE_FONT)
        sub = T("touch and strength lost on one side, pain on the other", 30, TEXT)
        hs = VGroup(head, sub).arrange(DOWN, buff=0.3).move_to([0, 2.5, 0])
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.9)
        self.at("pattern")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        note = T("major routes, not the whole of touch or pain processing", 26, GREY).move_to([0, -3.0, 0])
        self.at("major routes")
        self.play(FadeIn(note), run_time=0.7)
        ct = bchip("fine touch, vibration,\nposition sense", TOUCH, 28)
        cp = bchip("pain, temperature", PAIN, 28)
        xt = bchip("crosses in\nthe medulla", SIG, 30)
        xp = bchip("crosses in the\nspinal cord", SIG, 30)
        YA, YB = 0.55, -1.2
        ct.move_to([0, YA, 0]).align_to([-0.3, 0, 0], RIGHT).set_y(YA)
        cp.align_to([-0.3, 0, 0], RIGHT).set_y(YB)
        at_ = Arrow([-0.1, YA, 0], [0.9, YA, 0], color=GREY, buff=0, stroke_width=5)
        ap_ = Arrow([-0.1, YB, 0], [0.9, YB, 0], color=GREY, buff=0, stroke_width=5)
        xt.align_to([1.1, 0, 0], LEFT).set_y(YA)
        xp.align_to([1.1, 0, 0], LEFT).set_y(YB)
        d1, d2 = dot().move_to(ct.get_right()), dot().move_to(cp.get_right())
        self.at("Where each one crosses")
        self.play(FadeIn(ct, shift=RIGHT * 0.2), FadeIn(cp, shift=RIGHT * 0.2), run_time=0.8)
        self.at("crosses in the medulla")
        self.play(GrowArrow(at_), FadeIn(d1), run_time=0.4)
        self.play(d1.animate.move_to(xt.get_left()), FadeIn(xt, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeOut(d1), run_time=0.2)
        self.at("crosses in the spinal cord")
        self.play(GrowArrow(ap_), FadeIn(d2), run_time=0.4)
        self.play(d2.animate.move_to(xp.get_left()), FadeIn(xp, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeOut(d2), run_time=0.2)
        self.finish()


class S07End(EndCard):
    LINE = "Fine touch crosses in the medulla; pain crosses in the spinal cord."
