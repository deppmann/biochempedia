"""Who puts the potassium back: neurons and glia at work (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The one idea: potassium that leaks out of firing neurons shifts E_K, and astrocytes pass it from where
it is high to where it is low (spatial buffering, largely through Kir4.1). Every number on screen is the
lesson's own illustrative worked problem; nothing is a recording.

COLOR MAP (one color per concept, whole video)
  YELLOW = neurons (outline; filled when firing)
  BLUE   = potassium: K+ dots, outside potassium, the E_K marker
  GREEN  = astrocytes and their Kir4.1 channel (the redistribution route)
  TEAL   = the sodium-potassium ATPase (net uptake, the separate mechanism) and gap junctions
  ORANGE = oligodendrocytes
  RED    = problem: the 37 mV shift, a deleted channel, a poor result
  GREY   = membranes, axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
NEUR, KC, ASTRO, PUMP, OLIG, BAD = YELLOW, BLUE, GREEN, TEAL, ORANGE, RED


def ek(size=28, color=KC):
    return MarkupText("E<sub>K</sub>", font=FONT, font_size=size, color=color)


def kdot(p, r=0.1):
    return Dot(np.array([p[0], p[1], 0.0]), radius=r, color=KC)


def scatter(n, xr, yr, seed, gap=0.34):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = (rng.uniform(*xr), rng.uniform(*yr))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > gap ** 2 for q in pts):
            pts.append(p)
    return VGroup(*[kdot(p) for p in pts])


def blob(cx, cy, w, h, color, label=None, size=28, fill=0.1, sw=4):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill).move_to([cx, cy, 0])
    g = VGroup(e)
    if label:
        g.add(T(label, size, color).move_to(e))
    return g


def arr(a, b, color=GREY, w=7, tip=0.28):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def mbar(x0, x1, y, h=0.34, color=GREY):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def bchip(text, color, size=28):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def xmark(c, s=0.3, color=BAD, w=8):
    c = np.array([c[0], c[1], 0.0])
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Neurons and Glia at Work"
    TITLE = "Who Puts the Potassium Back"


# ------------------------------------------------------------------------------------------------
class S01Pileup(SpokenScene):
    def construct(self):
        L = blob(-3.3, 0.0, 5.4, 5.6, NEUR, "neuron", 30)
        R = blob(3.3, 0.0, 5.4, 5.6, NEUR, "neuron", 30)
        self.play(FadeIn(L), FadeIn(R), run_time=self.beat(0.06))
        allk = scatter(30, (-0.4, 0.4), (-2.45, 2.45), 3, 0.36)
        g1, g2, g3 = VGroup(*allk[:8]), VGroup(*allk[8:19]), VGroup(*allk[19:])

        def fire():
            return [L[0].animate.set_fill(NEUR, 0.5), R[0].animate.set_fill(NEUR, 0.5)]

        def rest():
            return [L[0].animate.set_fill(NEUR, 0.1), R[0].animate.set_fill(NEUR, 0.1)]

        self.at("lets potassium out")
        self.play(*fire(), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=(RIGHT if d.get_x() < 0 else LEFT) * 0.5) for d in g1], lag_ratio=0.12),
                  *rest(), run_time=1.6)
        self.at("fires hard")
        self.play(*fire(), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=(RIGHT if d.get_x() < 0 else LEFT) * 0.5) for d in g2], lag_ratio=0.1),
                  *rest(), run_time=1.8)
        self.at("space between brain cells")
        lab = T("narrow space between the cells", 26, GREY).move_to([0, 3.25, 0])
        br = VGroup(Line([-0.5, 2.85, 0], [-0.5, 2.7, 0], color=GREY, stroke_width=3),
                    Line([0.5, 2.85, 0], [0.5, 2.7, 0], color=GREY, stroke_width=3),
                    Line([-0.5, 2.85, 0], [0.5, 2.85, 0], color=GREY, stroke_width=3))
        self.play(FadeIn(lab), Create(br), run_time=0.7)
        self.at("build up there")
        self.play(*fire(), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=(RIGHT if d.get_x() < 0 else LEFT) * 0.5) for d in g3], lag_ratio=0.08),
                  *rest(), run_time=1.6)
        up = T("potassium builds up outside the cells", 26, KC).move_to([0, -3.25, 0])
        self.play(FadeIn(up), run_time=0.5)
        self.at("resting voltage depends")
        up2 = T("resting voltage depends largely on potassium", 26, TEXT).move_to([0, -3.25, 0])
        self.play(FadeOut(lab), FadeOut(br), Transform(up, up2), run_time=0.6)
        self.at("put it back")
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
YA = lambda v: -3.0 + (v + 110.0) * 0.1     # mV -> y on the E_K axis (-110..-50 mV)
AXX = 0.9


class S02Ek(SpokenScene):
    def construct(self):
        # left: the membrane, outside above, inside below
        mem = mbar(-5.9, -1.6, 0.15, 0.4)
        out_l = T("outside", 24, GREY).move_to([-5.0, 3.05, 0])
        in_l = T("inside", 24, GREY).move_to([-4.7, -3.05, 0])
        ins = scatter(22, (-5.7, -1.8), (-2.35, -0.55), 5, 0.62)
        self.play(FadeIn(mem), FadeIn(out_l), FadeIn(in_l), run_time=0.5)
        self.at("illustrative neuron")
        tag = T("illustrative values", 24, GREY).move_to([-3.25, 3.45, 0])
        # leave the tag out of the outside label's way
        out_l.move_to([-5.0, 2.7, 0])
        tag.move_to([-3.2, 3.4, 0])
        in_n = M("[K+]i = 140 mM", 26, KC).move_to([-3.25, -3.05, 0])
        in_l.move_to([-5.2, -3.1, 0]); in_n.move_to([-2.6, -3.1, 0])
        self.play(FadeIn(tag), LaggedStart(*[FadeIn(d) for d in ins], lag_ratio=0.03), FadeIn(in_n), run_time=1.6)
        self.at("sits outside")
        o3 = scatter(3, (-5.5, -2.0), (1.0, 2.0), 11, 1.4)
        o_n = M("[K+]o = 3 mM", 26, KC).move_to([-2.9, 2.7, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in o3], lag_ratio=0.2), FadeIn(o_n), run_time=1.0)
        # right: the E_K axis
        ax = Line([AXX, YA(-110), 0], [AXX, YA(-50), 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in (-100, -80, -60):
            ticks.add(Line([AXX - 0.12, YA(v), 0], [AXX + 0.12, YA(v), 0], color=GREY, stroke_width=3))
            ticks.add(M(f"{v}", 22, GREY).next_to(np.array([AXX - 0.2, YA(v), 0]), LEFT, buff=0.08))
        ulab = M("mV", 22, GREY).move_to([AXX, YA(-50) + 0.3, 0])
        self.play(FadeIn(ax), FadeIn(ticks), FadeIn(ulab), run_time=0.8)
        self.at("then minus")
        m1 = Dot([AXX, YA(-102.6), 0], radius=0.15, color=KC)
        l1 = VGroup(ek(30, KC), M("= −102.6 mV", 28, KC)).arrange(RIGHT, buff=0.12).next_to(m1, RIGHT, buff=0.3)
        self.play(FadeIn(m1, scale=1.6), FadeIn(l1), run_time=0.7)
        self.at("after intense firing")
        # more potassium outside: 3 dots -> 12 dots
        o12 = scatter(12, (-5.7, -1.8), (0.95, 2.0), 4, 0.7)
        o_n2 = M("[K+]o = 12 mM", 26, KC).move_to([-2.9, 2.7, 0])
        self.play(FadeOut(o3), FadeIn(o12), Transform(o_n, o_n2), run_time=1.2)
        self.at("becomes minus")
        m2 = Dot([AXX, YA(-65.6), 0], radius=0.15, color=BAD)
        l2 = VGroup(ek(30, BAD), M("= −65.6 mV", 28, BAD)).arrange(RIGHT, buff=0.12).next_to(m2, RIGHT, buff=0.3)
        self.play(FadeIn(m2, scale=1.6), FadeIn(l2), run_time=0.7)
        self.at("more positive")
        a = arr([AXX + 0.25, YA(-102.6) + 0.4, 0], [AXX + 0.25, YA(-65.6) - 0.4, 0], BAD, 9)
        # keep arrow clear of the two labels: place it left of the axis ticks? draw at the right edge
        a.move_to([5.8, (YA(-102.6) + YA(-65.6)) / 2, 0])
        a_l = VGroup(VGroup(ek(28, BAD), T(" shift", 28, BAD)).arrange(RIGHT, buff=0.05), M("+37.0 mV", 30, BAD)).arrange(DOWN, buff=0.12).next_to(a, LEFT, buff=0.15)
        a_l.shift(LEFT * 0.0)
        self.play(GrowArrow(a), FadeIn(a_l), run_time=0.8)
        self.at("voltage moves less")
        t = T("resting voltage moves less,\nsame direction", 24, TEXT).move_to([AXX + 2.9, YA(-50) - 0.5, 0])
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S03Buffer(SpokenScene):
    def construct(self):
        neur = blob(-3.9, 2.75, 4.6, 1.25, NEUR, "firing neurons", 26, fill=0.4)
        high = scatter(13, (-5.7, -2.1), (0.95, 1.75), 8, 0.5)
        lowd = VGroup(kdot((3.4, 1.3)), kdot((4.7, 1.0)))
        hl = T("high outside K+", 26, KC).move_to([-3.9, -3.2, 0])
        ll = T("low outside K+", 26, KC).move_to([3.0, -3.2, 0])
        self.play(FadeIn(neur), LaggedStart(*[FadeIn(d) for d in high], lag_ratio=0.04), FadeIn(lowd), run_time=1.0)
        self.at("kind of glial cell")
        A = blob(-3.0, -0.7, 5.8, 2.1, ASTRO, "astrocyte", 28, fill=0.18)
        B = blob(3.0, -0.7, 5.8, 2.1, ASTRO, "astrocyte", 28, fill=0.18)
        self.play(FadeIn(A, shift=UP * 0.2), FadeIn(B, shift=UP * 0.2), run_time=1.0)
        self.at("spatial buffering")
        sb = T("spatial buffering", 32, ASTRO).move_to([3.4, 2.8, 0])
        self.play(FadeIn(sb, scale=1.2), FadeIn(hl), FadeIn(ll), run_time=0.8)
        self.at("enters an astrocyte")
        d = high[len(high) // 2]
        d.set_z_index(5)
        self.play(d.animate.move_to([-3.6, -0.4, 0]), run_time=1.0)
        self.at("travels through that astrocyte")
        self.play(d.animate.move_to([-0.35, -0.7, 0]), run_time=1.2)
        self.at("gap junctions")
        gj = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.2, height=0.34, stroke_color=PUMP, stroke_width=3,
                                       fill_color=PUMP, fill_opacity=0.5).move_to([0, -0.7 + k * 0.42, 0]) for k in (-1, 0, 1)])
        gl = T("gap junctions", 26, PUMP).move_to([0, -2.35, 0])
        self.play(FadeIn(gj), FadeIn(gl), d.animate.move_to([0.35, -0.7, 0]), run_time=1.0)
        self.play(d.animate.move_to([3.6, -0.5, 0]), run_time=0.6)
        self.at("leaves where")
        self.play(d.animate.move_to([3.9, 1.3, 0]), run_time=1.0)
        self.at("think of a sponge")
        paths = []
        for dd, dx in ((high[2], 0), (high[8], 0), (high[10], 0)):
            dd.set_z_index(5)
        pl = [lambda x0: [(x0, 0.2), (x0 + 0.5, -0.6), (-0.3, -0.7), (0.3, -0.7), (3.0, -0.6), (4.3, 0.7), (4.5, 1.5)]]
        anims = []
        for dd in (high[2], high[8], high[10]):
            x0 = dd.get_x()
            pts = [(x0, 0.2), (x0 + 0.4, -0.5), (-0.3, -0.7), (0.3, -0.7), (3.0, -0.6), (4.4, 0.6), (4.7, 1.7)]
            pm = VMobject().set_points_as_corners([np.array([a, b, 0.0]) for a, b in pts])
            anims.append(MoveAlongPath(dd, pm, rate_func=linear))
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=4.0)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S04Channel(SpokenScene):
    def construct(self):
        y0 = 0.1
        mL, mR = mbar(-5.9, -0.5, y0), mbar(0.5, 5.9, y0)
        oL = T("outside", 24, GREY).move_to([-4.9, 2.4, 0]); oR = T("outside", 24, GREY).move_to([1.5, 2.4, 0])
        iL = T("inside astrocyte", 24, GREY).move_to([-3.9, -2.4, 0]); iR = T("inside astrocyte", 24, GREY).move_to([2.5, -2.4, 0])
        self.play(FadeIn(mL), FadeIn(mR), FadeIn(oL), FadeIn(oR), FadeIn(iL), FadeIn(iR), run_time=0.5)
        self.at("entry channel")
        kir = bchip("Kir4.1", ASTRO, 32).move_to([-3.2, y0, 0]); kir.set_z_index(5)
        self.play(FadeIn(kir, scale=1.3), run_time=0.7)
        self.at("inwardly rectifying")
        kd = VGroup(*[kdot((-3.2 + dx, 1.5 + dy)) for dx, dy in ((-0.5, 0.2), (0.0, 0.5), (0.5, 0.1))])
        tl = T("inwardly rectifying potassium channel", 24, ASTRO).move_to([-3.2, 3.2, 0])
        self.play(FadeIn(tl), FadeIn(kd), run_time=0.6)
        self.play(*[d.animate.move_to([-3.2 + (k - 1) * 0.45, -1.4, 0]) for k, d in enumerate(kd)], run_time=1.6)
        self.at("separately")
        atp = bchip("sodium-potassium ATPase", PUMP, 22).move_to([3.2, y0, 0]); atp.set_z_index(5)
        self.play(FadeIn(atp, scale=1.3), run_time=0.7)
        self.at("brings potassium into")
        kd2 = VGroup(*[kdot((3.2 + dx, 1.5 + dy)) for dx, dy in ((-0.5, 0.2), (0.0, 0.5), (0.5, 0.1))])
        tr = T("brings potassium into glia", 24, PUMP).move_to([3.2, 3.2, 0])
        self.play(FadeIn(tr), FadeIn(kd2), run_time=0.6)
        self.play(*[d.animate.move_to([3.2 + (k - 1) * 0.45, -1.4, 0]) for k, d in enumerate(kd2)], run_time=1.4)
        self.at("redistribution and net")
        rl = T("redistribution", 32, ASTRO).move_to([-3.2, -3.2, 0])
        nl = T("net uptake", 32, PUMP).move_to([3.2, -3.2, 0])
        self.play(FadeIn(rl, shift=UP * 0.15), FadeIn(nl, shift=UP * 0.15), run_time=0.8)
        self.at("distinct mechanisms")
        sep = DashedLine([0, 3.5, 0], [0, -3.5, 0], color=GREY, stroke_width=3)
        self.play(Create(sep), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S05Knockout(SpokenScene):
    def construct(self):
        pl_x, pr_x = -3.6, 2.0
        self.at("tested the channel")
        A = blob(pl_x, -0.6, 4.4, 3.4, ASTRO, "astrocyte", 28, fill=0.18)
        kirL = bchip("Kir4.1", ASTRO, 28).move_to([pl_x, 1.1, 0]); kirL.set_z_index(5)
        hL = T("Kir4.1 present", 28, ASTRO).move_to([pl_x, 3.2, 0])
        self.play(FadeIn(A), FadeIn(kirL), FadeIn(hL), run_time=0.8)
        self.at("with genetics")
        # a stream of potassium into the intact cell
        def stream(x, n):
            out = []
            for i in range(n):
                p = VMobject().set_points_as_corners([np.array([x + (i - 1) * 0.5, 2.2, 0]), np.array([x + (i - 1) * 0.1, 1.1, 0]),
                                                      np.array([x + (i - 1) * 0.3, -1.1, 0])])
                d = kdot((x + (i - 1) * 0.5, 2.2)); d.set_z_index(4)
                out.append((d, p))
            return out
        sl = stream(pl_x, 3)
        for d, _ in sl:
            self.add(d)
        self.play(LaggedStart(*[MoveAlongPath(d, p, rate_func=linear) for d, p in sl], lag_ratio=0.25), run_time=1.6)
        self.at("deleted")
        B = blob(pr_x, -0.6, 4.4, 3.4, ASTRO, "astrocyte", 28, fill=0.18)
        kirR = bchip("Kir4.1", ASTRO, 28).move_to([pr_x, 1.1, 0]); kirR.set_z_index(5)
        hR = T("Kir4.1 deleted from glia", 28, BAD).move_to([pr_x + 0.4, 3.2, 0])
        self.play(FadeIn(B), FadeIn(kirR), FadeIn(hR), run_time=0.8)
        x = xmark([pr_x, 1.1]); x.set_z_index(6)
        self.play(Create(x), kirR.animate.set_opacity(0.35), run_time=0.7)
        self.at("hippocampal slices from mice")
        note = T("hippocampal slices, mice 15 to 20 days old", 24, GREY).move_to([0, -3.15, 0])
        note.shift(DOWN * 0.0)
        self.play(FadeIn(note), run_time=0.6)
        self.at("took up potassium poorly")
        rl = T("takes up K+", 26, ASTRO).move_to([pl_x, -2.6, 0])
        rr = T("took up K+ poorly", 26, BAD).move_to([pr_x, -2.6, 0])
        sr = stream(pr_x, 1)
        d = sr[0][0]; d.set_z_index(4); self.add(d)
        pth = VMobject().set_points_as_corners([np.array([pr_x, 2.2, 0]), np.array([pr_x, -1.1, 0])])
        self.play(FadeIn(rl), FadeIn(rr), MoveAlongPath(d, pth, rate_func=linear), run_time=1.2)
        self.at("also reached oligodendrocytes")
        O = blob(5.3, -0.6, 2.1, 2.1, OLIG, None)
        ol = T("oligodendrocyte", 22, OLIG).move_to([5.1, -1.95, 0])
        ox = T("also hit by\nthe deletion", 22, OLIG).move_to([5.3, -0.6, 0]); xo = VGroup()
        self.play(FadeIn(O), FadeIn(ol), FadeIn(ox), run_time=0.9)
        self.at("cannot be pinned")
        cap = T("cannot be pinned on mature astrocytes alone", 26, TEXT).move_to([0, -3.15, 0])
        self.play(FadeOut(note), FadeIn(cap), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        c1 = chip("neurons\nfire hard", NEUR, 30)
        c2 = chip("outside K+ can build up\nEK becomes more positive", KC, 28)
        c3 = chip("astrocytes pass it\nfrom high to low", ASTRO, 28)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.95).move_to([0, 1.6, 0])
        fit(row, max_w=12.4)
        a1 = arr(c1.get_right() + RIGHT * 0.08, c2.get_left() + LEFT * 0.08, GREY, 6, 0.25)
        a2 = arr(c2.get_right() + RIGHT * 0.08, c3.get_left() + LEFT * 0.08, GREY, 6, 0.25)
        self.at("keep this rule")
        self.play(FadeIn(c1), run_time=0.6)
        self.at("fire hard")
        self.play(GrowArrow(a1), FadeIn(c2, shift=RIGHT * 0.3), run_time=0.9)
        self.at("toward threshold")
        note = T("real resting voltage: same way, but less", 26, TEXT).move_to([c2.get_center()[0], 2.85, 0])
        self.play(FadeIn(note, shift=DOWN * 0.15), run_time=0.7)
        self.at("astrocytes pass that")
        self.play(GrowArrow(a2), FadeIn(c3, shift=RIGHT * 0.3), run_time=0.9)
        self.at("from where it is high")
        hl = VGroup(T("high", 28, KC), Arrow(LEFT, RIGHT, buff=0, color=ASTRO, stroke_width=8), T("low", 28, KC)).arrange(RIGHT, buff=0.3)
        hl.move_to([4.0, c3.get_bottom()[1] - 0.6, 0])
        self.play(FadeIn(hl), run_time=0.7)
        self.at("that is redistribution")
        rd = T("redistribution", 32, ASTRO).move_to([0, -0.5, 0])
        br = Brace(row, DOWN, color=ASTRO, buff=0.15)
        self.play(FadeOut(hl), GrowFromCenter(br), FadeIn(rd), run_time=0.8)
        self.at("net uptake by")
        sep = DashedLine([-6.0, -1.5, 0], [6.0, -1.5, 0], color=GREY, stroke_width=3)
        nu = chip("net uptake: sodium-potassium ATPase", PUMP, 28).move_to([0, -2.4, 0])
        self.play(Create(sep), FadeIn(nu, shift=UP * 0.2), run_time=0.9)
        self.at("separate mechanism")
        sm = T("a separate mechanism", 28, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(sm), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Astrocytes move potassium from where it is high to where it is low."
