"""mTOR and AMPK: two yeses to grow, and low energy can veto them  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the growth-factor path: growth factor, Akt, TSC complex
  YELLOW = Rheb and its GTP
  TEAL   = amino acids and the Rags
  ORANGE = mTORC1 (and its part, Raptor)
  PINK   = energy: ATP, AMP, AMPK
  GOLD   = a phosphate (round "P" badge) and the AND badge
  GREEN  = on / active (the halo round mTORC1, a "yes", a lit lamp)
  RED    = off / veto / ruled out
  GREY   = membrane, labels, parts that are out of action

No molecular structures: everything is a labelled chip, a bar, a badge or an arrow. The one drawn
"shape that acts" is the grip between the Rags and mTORC1: a teal bar that closes on the chip only
when amino acids are there, so delivery to the membrane is something you can see.
The bar chart in scene 5 is computed from the adenylate-kinase equation with the lesson's numbers.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PINK = "#F08BB4"

MEM_Y, MEM_H = -1.9, 0.3
TOPY = MEM_Y + MEM_H / 2
RHEB_X, RAGS_X, DOCK_X = 4.9, -0.9, 1.9
FLOAT = np.array([-3.7, 0.7, 0])
DIM = 0.35


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def sit(m, x):
    """put a chip on top of the membrane bar."""
    return m.move_to([x, TOPY + m.height / 2, 0])


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def pbadge():
    c = Circle(radius=0.22, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def gtp_badge():
    t = T("GTP", 22, BG, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.24, height=t.height + 0.2, stroke_width=0,
                         fill_color=YELLOW, fill_opacity=1)
    return VGroup(r, t.move_to(r))


def cross(m, color=RED):
    return Line(m.get_corner(DL) + [-0.1, -0.05, 0], m.get_corner(UR) + [0.1, 0.05, 0], color=color, stroke_width=7)


def header(text):
    return T(text, 28, GREY, weight=BOLD).move_to([-6.2, 3.3, 0], aligned_edge=LEFT)


def lamp_text(on, word="mTORC1"):
    col = GREEN if on else RED
    lamp = Circle(radius=0.2, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=1 if on else 0.25)
    return VGroup(lamp, T(f"{word} {'on' if on else 'off'}", 30, col, weight=BOLD)).arrange(RIGHT, buff=0.25)


def banner(on):
    return lamp_text(on).move_to([0, -3.2, 0])


class St:
    """The stage: membrane bar, the growth-factor stack on the right, Rheb on the membrane, the Rags,
    mTORC1. Every scene that continues the story rebuilds it in the same place with `fed()`."""

    def __init__(self):
        self.mem = RoundedRectangle(corner_radius=0.1, width=12.4, height=MEM_H, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.35).move_to([0, MEM_Y, 0])
        self.lbl_mem = T("membrane", 24, GREY).move_to([-4.9, -2.45, 0])
        self.lbl_lys = T("lysosome surface", 24, GREY).move_to([-4.3, -2.45, 0])
        self.gf = bchip("Growth factor", BLUE, 28).move_to([4.9, 3.05, 0])
        self.akt = bchip("Akt", BLUE, 28).move_to([4.9, 1.8, 0])
        self.tsc = bchip("TSC complex", BLUE, 28).move_to([4.9, 0.55, 0])
        self.a1 = arr(self.gf.get_bottom(), self.akt.get_top(), BLUE)
        self.a2 = inhib(self.akt.get_bottom() + DOWN * 0.03, self.tsc.get_top() + UP * 0.02, BLUE)
        self.rheb = self.rheb_mob(False)
        self.tinh = inhib(self.tsc.get_bottom() + DOWN * 0.03, [RHEB_X, TOPY + self.rheb.height + 0.02, 0], BLUE)
        self.rags = sit(bchip("Rags", TEAL, 34), RAGS_X)
        self.mt = bchip("mTORC1", ORANGE, 40)
        self.dock = np.array([DOCK_X, TOPY + self.mt.height / 2, 0])
        self.mt.move_to(FLOAT)
        self.link = self.link_mob()
        self.halo = self.halo_mob()

    def rheb_mob(self, on):
        if on:
            m = bchip("Rheb-GTP", YELLOW, 34, fill_opacity=0.45)
        else:
            m = bchip("Rheb", YELLOW, 34).set_opacity(0.45)
        return sit(m, RHEB_X)

    def link_mob(self):
        y = self.rags.get_center()[1]
        x0 = self.rags.get_right()[0]
        x1 = DOCK_X - self.mt.width / 2
        return Line([x0, y, 0], [x1, y, 0], color=TEAL, stroke_width=10)

    def halo_mob(self):
        return RoundedRectangle(corner_radius=0.2, width=self.mt.width + 0.34, height=self.mt.height + 0.34,
                                stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.12
                                ).move_to(self.dock)

    def cs(self, key, bright):
        """a fresh target look for gf / akt / tsc (set_opacity(1) would fill the chip solid)."""
        txt = {"gf": "Growth factor", "akt": "Akt", "tsc": "TSC complex"}[key]
        c = bchip(txt, BLUE, 28)
        if not bright:
            c.set_opacity(DIM)
        return c.move_to(getattr(self, key).get_center())

    def fed(self, lit=False, lysosome=True):
        """The stage as it stands when growth factor and amino acids are both there."""
        self.tsc.set_opacity(DIM)
        self.tinh.set_opacity(DIM)
        self.rheb = self.rheb_mob(True)
        self.mt.move_to(self.dock)
        self.halo = self.halo_mob()
        mobs = [self.mem, self.lbl_lys if lysosome else self.lbl_mem, self.gf, self.akt, self.a1, self.a2,
                self.tsc, self.tinh, self.rheb, self.rags, self.link, self.mt]
        if lit:
            mobs.append(self.halo)
        return mobs


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "mTOR and AMPK: Reading Nutrients and Energy"
    TITLE = "Two Yeses to Grow, One Veto"


class S07End(EndCard):
    LINE = "Two yeses to grow, and low energy can veto them."


# =============================================================================================
class S01Question(SpokenScene):
    def construct(self):
        synth = bchip("protein synthesis", GREY, 34).move_to([3.7, 0.2, 0])
        qmark = T("?", 110, GOLD, weight=BOLD).next_to(synth, UP, buff=0.35)
        self.play(FadeIn(synth), FadeIn(qmark, scale=0.6), run_time=0.8)
        self.at("Growth is expensive")
        self.play(Indicate(synth, color=TEXT, scale_factor=1.1), run_time=0.8)
        self.at("Making protein")
        aa = bchip("amino acids", TEAL, 34).move_to([3.0, 3.0, 0])
        self.play(FadeIn(aa, shift=DOWN * 0.3), run_time=0.5)
        self.play(aa.animate.move_to(synth.get_top() + UP * 0.1).scale(0.5).set_opacity(0), run_time=0.9)
        self.at("much of")
        atp = bchip("ATP", PINK, 34).move_to([3.0, -2.8, 0])
        self.play(FadeIn(atp, shift=UP * 0.3), run_time=0.5)
        self.play(atp.animate.move_to(synth.get_bottom() + DOWN * 0.1).scale(0.5).set_opacity(0), run_time=0.9)
        self.remove(aa, atp)
        self.at("So a kinase")
        self.play(FadeOut(qmark), run_time=0.3)
        mt = bchip("mTORC1", ORANGE, 44).move_to([-0.5, 0.2, 0])
        k = T("kinase", 26, GREY).next_to(mt, DOWN, buff=0.25)
        self.play(FadeIn(mt, scale=0.8), FadeIn(k), run_time=0.7)
        self.at("two questions")
        q1 = bchip("?", GOLD, 56, pad=0.35).move_to([-5.0, 1.9, 0])
        q2 = bchip("?", GOLD, 56, pad=0.35).move_to([-5.0, -1.5, 0])
        a1 = arr(q1.get_right(), mt.get_left() + UP * 0.2, GREY)
        a2 = arr(q2.get_right(), mt.get_left() + DOWN * 0.2, GREY)
        a3 = arr(mt.get_right(), synth.get_left(), GREY)
        self.play(FadeIn(q1, shift=RIGHT * 0.3), FadeIn(q2, shift=RIGHT * 0.3), run_time=0.7)
        self.play(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=0.6)
        self.at("only when both")
        y1 = bchip("yes", GREEN, 44, pad=0.3).move_to(q1)
        y2 = bchip("yes", GREEN, 44, pad=0.3).move_to(q2)
        halo = RoundedRectangle(corner_radius=0.2, width=mt.width + 0.34, height=mt.height + 0.34, stroke_color=GREEN,
                                stroke_width=6, fill_color=GREEN, fill_opacity=0.12).move_to(mt)
        self.play(Transform(q1, y1), Transform(q2, y2), run_time=0.6)
        self.play(FadeIn(halo), synth[1].animate.set_color(GREEN), synth[0].animate.set_stroke(GREEN), run_time=0.7)
        self.finish()


# =============================================================================================
class S02Growth(SpokenScene):
    def construct(self):
        s = St()
        hd = header("1   Has the body said grow?")
        self.add(s.mem, s.lbl_mem, s.mt)
        self.play(FadeIn(hd), run_time=0.6)
        self.at("growth factor")
        self.play(FadeIn(s.gf, shift=DOWN * 0.2), run_time=0.5)
        self.at("switches on")
        self.play(GrowArrow(s.a1), FadeIn(s.akt), run_time=0.6)
        self.play(Indicate(s.akt, color=TEXT, scale_factor=1.12), run_time=0.5)
        self.at("phosphorylates")
        self.play(Create(s.a2), FadeIn(s.tsc), run_time=0.6)
        p = pbadge().move_to(s.akt.get_left() + LEFT * 0.0 + DOWN * 0.0)
        p.move_to(s.akt.get_left() + LEFT * 0.4)
        self.play(FadeIn(p, scale=0.5), run_time=0.3)
        self.play(p.animate.move_to(s.tsc.get_left() + LEFT * 0.4), run_time=0.7)
        self.at("takes the complex")
        self.play(s.tsc.animate.set_opacity(DIM), p.animate.set_opacity(0.0), run_time=0.7)
        self.remove(p)
        self.at("off switch")
        self.play(FadeIn(s.tinh.set_opacity(1.0)), run_time=0.5)
        self.play(s.tinh.animate.set_opacity(DIM), FadeIn(s.rheb), run_time=0.6)
        self.at("stays loaded")
        g = gtp_badge().move_to([2.9, -0.2, 0])
        self.play(FadeIn(g, scale=0.6), run_time=0.4)
        self.play(g.animate.move_to(s.rheb.get_center()).set_opacity(0.0), Transform(s.rheb, s.rheb_mob(True)), run_time=0.8)
        self.remove(g)
        self.at("direct activator")
        self.play(Indicate(s.rheb, color=TEXT, scale_factor=1.12), Indicate(s.mt, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.finish()


# =============================================================================================
class S03Amino(SpokenScene):
    def construct(self):
        s = St()
        # carry-over from scene 2: the growth-factor stack with Rheb loaded, mTORC1 in the cytoplasm
        s.tsc.set_opacity(DIM)
        s.tinh.set_opacity(DIM)
        s.rheb = s.rheb_mob(True)
        old = header("1   Has the body said grow?")
        self.add(s.mem, s.lbl_mem, s.gf, s.akt, s.a1, s.a2, s.tsc, s.tinh, s.rheb, s.mt, old)
        hd = header("2   Are there amino acids?")
        self.play(FadeOut(old), FadeIn(hd), run_time=0.5)
        self.at("was unknown")
        rec = bchip("unknown", GREY, 28).move_to([-4.7, TOPY + 0.45, 0])
        ghost = VGroup(DashedVMobject(rec[1], num_dashes=28).set_color(GREY), rec[2])
        ghost.move_to(rec)
        self.play(FadeIn(ghost, shift=DOWN * 0.2), run_time=0.6)
        self.at("The link was")
        x = cross(ghost)
        self.play(Create(x), run_time=0.4)
        rags_dim = s.rags.copy().set_opacity(0.4)
        self.play(FadeOut(ghost), FadeOut(x), FadeIn(rags_dim, shift=DOWN * 0.2), run_time=0.7)
        self.at("do not raise")
        up = arr(s.mt.get_top() + UP * 0.1, s.mt.get_top() + UP * 1.0, GREY, w=6)
        lab = T("more kinase activity", 22, GREY).next_to(up, UP, buff=0.12)
        self.play(GrowArrow(up), FadeIn(lab), run_time=0.5)
        xx = cross(up.copy().scale(0.6))
        self.play(Create(xx), run_time=0.4)
        self.at("They move it")
        self.play(FadeOut(up), FadeOut(lab), FadeOut(xx), run_time=0.4)
        self.play(Indicate(s.mt, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("spread through")
        self.play(s.mt.animate.move_to([-1.2, 1.6, 0]), run_time=0.8)
        self.play(s.mt.animate.move_to([-4.2, -0.1, 0]), run_time=0.9)
        self.play(s.mt.animate.move_to(FLOAT), run_time=0.7)
        self.at("With them")
        aa = bchip("amino acids", TEAL, 24).move_to([0.3, 2.9, 0])
        sens = bchip("sensors", TEAL, 24).move_to([RAGS_X, 1.5, 0])
        sarr_ = arr(sens.get_bottom(), s.rags.get_top() + UP * 0.02, TEAL)
        self.play(FadeIn(aa, shift=DOWN * 0.3), FadeIn(sens), GrowArrow(sarr_), run_time=0.4)
        self.play(aa.animate.move_to(sens.get_top() + UP * 0.4), run_time=0.4)
        self.at("gathers")
        self.play(FadeOut(aa, scale=0.4), FadeOut(sens), FadeOut(sarr_), Transform(rags_dim, s.rags), run_time=0.4)
        self.play(s.mt.animate.move_to([-0.3, 0.5, 0]), run_time=0.5, rate_func=linear)
        self.play(s.mt.animate.move_to(s.dock), run_time=0.5, rate_func=linear)
        self.play(Create(s.link), run_time=0.4)
        self.at("lysosome")
        self.play(Transform(s.lbl_mem, s.lbl_lys), run_time=0.6)
        self.at("thought to meet")
        tag = T("thought to meet here", 24, GREY).move_to([2.2, -0.3, 0])
        self.play(Indicate(s.rheb, color=TEXT, scale_factor=1.12), Indicate(s.mt, color=TEXT, scale_factor=1.12), FadeIn(tag), run_time=0.9)
        self.finish()


# =============================================================================================
def row(label, color, yes, y):
    lab = T(label, 26, color).move_to([-6.2, y, 0], aligned_edge=LEFT)
    st = T("yes" if yes else "no", 26, GREEN if yes else RED, weight=BOLD).move_to([-3.0, y, 0], aligned_edge=LEFT)
    return lab, st


class S04Gate(SpokenScene):
    def construct(self):
        s = St()
        old = header("2   Are there amino acids?")
        mobs = s.fed(lit=False)
        self.add(*mobs, old)
        synth = bchip("protein synthesis", GREY, 28).move_to([0.9, 1.5, 0])
        sarr = arr(s.mt.get_top() + UP * 0.02, synth.get_bottom() + RIGHT * 0.9, GREY)
        self.play(FadeOut(old), run_time=0.4)
        self.at("activate only")
        self.play(Indicate(s.rheb, color=TEXT, scale_factor=1.12), Indicate(s.mt, color=TEXT, scale_factor=1.12), run_time=0.9)
        self.at("Growth factors set")
        l1, v1 = row("Growth factor", BLUE, True, 3.35)
        self.play(FadeIn(l1), FadeIn(v1), Indicate(s.rheb, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("Amino acids set")
        l2, v2 = row("Amino acids", TEAL, True, 2.55)
        self.play(FadeIn(l2), FadeIn(v2), Indicate(s.rags, color=TEXT, scale_factor=1.15), Indicate(s.link, color=TEXT), run_time=0.8)
        self.at("This is")
        br = VGroup(Line([-2.2, 3.35, 0], [-1.7, 3.35, 0], color=GOLD, stroke_width=5),
                    Line([-1.7, 3.35, 0], [-1.7, 2.55, 0], color=GOLD, stroke_width=5),
                    Line([-2.2, 2.55, 0], [-1.7, 2.55, 0], color=GOLD, stroke_width=5))
        andc = bchip("AND", GOLD, 30).move_to([-0.7, 2.95, 0])
        self.play(Create(br), FadeIn(andc, shift=LEFT * 0.2), run_time=0.8)
        # --- case 1: both yes
        self.at("With both")
        lit = banner(True)
        self.play(FadeIn(s.halo), FadeIn(lit), run_time=0.6)
        self.play(GrowArrow(sarr), FadeIn(synth), run_time=0.5)
        self.play(synth[1].animate.set_stroke(GREEN), synth[2].animate.set_color(GREEN), run_time=0.4)
        # --- case 2: no growth factor.  Clear the old answer in the same beat as the new label.
        self.at("With no growth")
        v1n = row("Growth factor", BLUE, False, 3.35)[1]
        new_rheb = s.rheb_mob(False)
        self.play(FadeOut(s.halo), FadeOut(lit), FadeOut(sarr), FadeOut(synth),
                  Transform(v1, v1n),
                  s.gf.animate.set_opacity(DIM), s.akt.animate.set_opacity(DIM), s.a1.animate.set_opacity(DIM), s.a2.animate.set_opacity(DIM),
                  Transform(s.tsc, s.cs('tsc', True)), s.tinh.animate.set_opacity(1.0),
                  Transform(s.rheb, new_rheb), run_time=0.9)
        self.at("is off")
        self.play(Indicate(s.rheb, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("stays off")
        off1 = banner(False)
        self.play(FadeIn(off1), run_time=0.5)
        # --- case 3: no amino acids
        self.at("With no amino")
        v1y = row("Growth factor", BLUE, True, 3.35)[1]
        v2n = row("Amino acids", TEAL, False, 2.55)[1]
        self.play(FadeOut(off1),
                  Transform(v1, v1y), Transform(v2, v2n),
                  Transform(s.gf, s.cs('gf', True)), Transform(s.akt, s.cs('akt', True)), s.a1.animate.set_opacity(1.0), s.a2.animate.set_opacity(1.0),
                  s.tsc.animate.set_opacity(DIM), s.tinh.animate.set_opacity(DIM),
                  Transform(s.rheb, s.rheb_mob(True)),
                  s.rags.animate.set_opacity(0.4), FadeOut(s.link), run_time=0.9)
        self.at("leaves the lysosome")
        self.play(s.mt.animate.move_to([0.9, 0.6, 0]), run_time=0.6, rate_func=linear)
        self.play(s.mt.animate.move_to(FLOAT), run_time=0.8)
        self.at("stays off", nth=1)
        off2 = banner(False)
        self.play(FadeIn(off2), run_time=0.5)
        self.finish()


# =============================================================================================
class S05Energy(SpokenScene):
    def construct(self):
        hd = header("3   Is there enough energy?")
        self.play(FadeIn(hd), run_time=0.6)
        # numbers from the lesson: K = 0.5; ATP 5.0 -> 4.5 mM; ADP 0.93; AMP = K * ADP^2 / ATP
        K = 0.5
        atp0, adp0 = 5.0, 0.5
        amp0 = K * adp0 ** 2 / atp0
        atp1, adp1 = 4.5, 0.93
        amp1 = K * adp1 ** 2 / atp1
        u = 0.8
        base = -2.4

        def bar(x, rel, color, op=0.9):
            h = rel * u
            return Rectangle(width=0.9, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                             fill_opacity=op).move_to([x, base + h / 2, 0])
        atp_a = bar(-3.9, 1.0, PINK, 0.35)
        atp_b = bar(-2.7, atp1 / atp0, PINK)
        amp_a = bar(0.9, 1.0, PINK, 0.35)
        amp_b = bar(2.1, amp1 / amp0, PINK)
        floor = Line([-5.2, base, 0], [3.4, base, 0], color=GREY, stroke_width=3)
        n_atp = T("ATP", 28, PINK, weight=BOLD).move_to([-3.3, base - 0.9, 0])
        n_amp = T("AMP", 28, PINK, weight=BOLD).move_to([1.5, base - 0.9, 0])
        r1 = T("rest", 22, GREY).move_to([-3.9, base - 0.35, 0])
        r2 = T("after work", 22, GREY).move_to([-2.5, base - 0.35, 0])
        r3 = T("rest", 22, GREY).move_to([0.9, base - 0.35, 0])
        r4 = T("after work", 22, GREY).move_to([2.3, base - 0.35, 0])
        note = T("each bar is compared with its own level at rest", 24, GREY).move_to([-6.2, 2.6, 0], aligned_edge=LEFT)
        self.at("A healthy cell")
        self.play(FadeIn(note), Create(floor), FadeIn(atp_a), FadeIn(amp_a), FadeIn(r1), FadeIn(r3), FadeIn(n_atp), FadeIn(n_amp), run_time=0.9)
        self.at("poor alarm")
        self.play(Indicate(atp_a, color=TEXT, scale_factor=1.04), run_time=0.7)
        self.at("moves most")
        self.play(Indicate(amp_a, color=TEXT, scale_factor=1.04), run_time=0.7)
        self.at("falls by a tenth")
        atp_b.save_state()
        self.play(GrowFromEdge(atp_b, DOWN), FadeIn(r2), run_time=0.8)
        self.at("rises almost")
        self.play(GrowFromEdge(amp_b, DOWN), FadeIn(r4), run_time=1.2)
        self.at("the kinase")
        ampk = bchip("AMPK", PINK, 30).move_to([5.0, 0.2, 0])
        a_ = arr(amp_b.get_top() + UP * 0.05 + RIGHT * 0.2, ampk.get_left() + DOWN * 0.1, PINK)
        self.play(FadeIn(ampk, scale=0.8), GrowArrow(a_), run_time=0.7)
        # --- the stage returns, in the fed state, lit
        s = St()
        mobs = s.fed(lit=True)
        lit = banner(True)
        self.at("Once on")
        gauge = VGroup(note, floor, atp_a, atp_b, amp_a, amp_b, n_atp, n_amp, r1, r2, r3, r4, a_)
        self.play(FadeOut(gauge), FadeOut(hd), run_time=0.5)
        self.play(*[FadeIn(m) for m in mobs], FadeIn(lit), ampk.animate.move_to([0.0, 2.7, 0]), run_time=0.9)
        self.at("makes the")
        aa = arr(ampk.get_right() + RIGHT * 0.05, s.tsc.get_left() + UP * 0.1, PINK, w=6)
        self.play(GrowArrow(aa), run_time=0.5)
        self.play(Transform(s.tsc, s.cs('tsc', True)), s.tinh.animate.set_opacity(1.0), run_time=0.6)
        self.at("That drains")
        self.play(Transform(s.rheb, s.rheb_mob(False)), run_time=0.8)
        self.at("phosphorylates Raptor")
        rap = bchip("Raptor", ORANGE, 28).move_to([DOCK_X, TOPY + s.mt.height + 0.65, 0])
        self.play(FadeIn(rap, shift=DOWN * 0.2), run_time=0.5)
        ai = inhib(ampk.get_bottom() + DOWN * 0.03, rap.get_top() + UP * 0.03, RED)
        self.play(Create(ai), run_time=0.7)
        self.at("inhibits")
        off = banner(False)
        self.play(FadeOut(s.halo), Transform(lit, off), run_time=0.7)
        self.at("Energy can veto")
        self.play(Indicate(ampk, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("even when")
        self.play(Indicate(s.gf, color=TEXT, scale_factor=1.1), Indicate(s.rags, color=TEXT, scale_factor=1.15), run_time=0.9)
        self.finish()


# =============================================================================================
def panel(cx, title, gf, aa, en, out_on, note):
    w, h, cy = 3.95, 6.2, -0.1
    frame = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])
    ttl = T(title, 30, TEXT, weight=BOLD).move_to([cx, 2.35, 0])
    rows = []
    for i, (lab, col, ok) in enumerate([("growth factor", BLUE, gf), ("amino acids", TEAL, aa), ("energy", PINK, en)]):
        y = 1.45 - i * 0.8
        t = T(lab, 24, col).move_to([cx - w / 2 + 0.3, y, 0], aligned_edge=LEFT)
        c = GREEN if ok else RED
        d = Circle(radius=0.17, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=1 if ok else 0.25).move_to([cx + w / 2 - 0.45, y, 0])
        rows.append(VGroup(t, d))
    mt = bchip("mTORC1", ORANGE, 28).move_to([cx, -1.45, 0])
    res = lamp_text(out_on, "").arrange(RIGHT, buff=0.2)
    res = VGroup(Circle(radius=0.2, stroke_color=GREEN if out_on else RED, stroke_width=3,
                        fill_color=GREEN if out_on else RED, fill_opacity=1 if out_on else 0.25),
                 T("on" if out_on else "off", 30, GREEN if out_on else RED, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to([cx, -2.3, 0])
    nt = T(note, 22, GREY).move_to([cx, -2.9, 0])
    halo = RoundedRectangle(corner_radius=0.2, width=mt.width + 0.3, height=mt.height + 0.3, stroke_color=GREEN, stroke_width=6,
                            fill_color=GREEN, fill_opacity=0.12).move_to(mt)
    veto = None
    if gf and aa and not en:
        veto = inhib([cx + 1.45, -0.4, 0], [cx + 0.6, mt.get_top()[1] + 0.03, 0], RED, 6)
    return frame, ttl, rows, mt, res, nt, halo, veto


class S06Predict(SpokenScene):
    def construct(self):
        xs = [-4.2, 0.0, 4.2]
        specs = [("Fed", True, True, True, True, "protein synthesis runs"),
                 ("No amino acids", True, False, True, False, "complex leaves lysosome"),
                 ("No energy", True, True, False, False, "AMPK shuts it off")]
        built = [panel(x, *sp) for x, sp in zip(xs, specs)]
        # panel 1
        self.at("When fed")
        fr, ttl, rows, mt, res, nt, halo, veto = built[0]
        self.play(FadeIn(fr), FadeIn(ttl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), FadeIn(mt), run_time=1.0)
        self.at("protein synthesis")
        self.play(FadeIn(halo), FadeIn(res), FadeIn(nt), run_time=0.6)
        # panel 2
        self.at("With no amino")
        fr, ttl, rows, mt, res, nt, halo, veto = built[1]
        self.play(FadeIn(fr), FadeIn(ttl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), FadeIn(mt), run_time=1.0)
        self.at("leaves the lysosome")
        self.play(FadeIn(res), FadeIn(nt), run_time=0.6)
        # panel 3
        self.at("With no energy")
        fr, ttl, rows, mt, res, nt, halo, veto = built[2]
        self.play(FadeIn(fr), FadeIn(ttl), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), FadeIn(mt), run_time=1.0)
        self.at("shuts")
        self.play(Create(veto), run_time=0.5)
        self.play(FadeIn(res), FadeIn(nt), run_time=0.6)
        self.at("Keep this rule")
        r1 = T("Two yeses to grow.", 48, TEXT, font=TITLE_FONT)
        r2 = T("Low energy can veto them.", 48, TEXT, font=TITLE_FONT)
        rule = VGroup(r1, r2).arrange(DOWN, buff=0.35)
        under = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(rule, DOWN, buff=0.4)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), GrowFromCenter(under), run_time=0.8)
        self.finish()
