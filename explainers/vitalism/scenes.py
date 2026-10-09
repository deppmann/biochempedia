"""How the vital force ran out of places to hide  (Biochemistrypedia, Vitalism interlude)

COLOR MAP (kept for the whole video)
  GREEN   organic / living: cells, yeast, urea, sugar, fats, acetic acid, "organic"
  BLUE    inorganic / lifeless chemistry: rocks, salts, charcoal, sulfur, "ordinary law"
  RED     the vital force, and the claims made on its behalf (spark, fence, vitalist objection, gauge)
  YELLOW  an action or a dated person: heat, "1845 . Kolbe", experimental controls
  TEAL    the enzyme / the soluble agent
  TEXT/GREY  neutral: wall, atom tallies, glassware

No molecular structure is drawn anywhere: chips, blobs, bars, beakers and arrows only.
"""
import json
import math
import random
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(__file__).parent
_SCRIPT = json.loads((HERE / "script.json").read_text())
TEXTS = {s["id"]: s["tts"] for s in _SCRIPT["scenes"] if s.get("tts")}
DUR = json.loads((HERE / "audio" / "durations.json").read_text())

GAUGE_W = 9.0
GAUGE_Y = 2.85


class VS(NarratedScene):
    """Narrated scene with phrase-timed beats. ANCH pins phrase ends to measured silences."""
    SID = None
    ANCH = []

    def _map(self):
        text = TEXTS[self.SID]
        pts = [(0, 0.0)]
        for ph, t in self.ANCH:
            i = text.find(ph)
            assert i >= 0, (self.SID, ph)
            pts.append((i + len(ph), t))
        pts.append((len(text), DUR[self.SID]))
        pts.sort()
        return text, np.array([p[0] for p in pts], float), np.array([p[1] for p in pts], float)

    def t_of(self, phrase, end=False):
        text, xs, ys = self._map()
        i = text.find(phrase)
        assert i >= 0, (self.SID, phrase)
        return float(np.interp(i + (len(phrase) if end else 0), xs, ys))

    def at(self, phrase, end=False, lead=0.0):
        """Wait until the narrator reaches `phrase` (start, or end if end=True)."""
        target = self.t_of(phrase, end) - lead
        d = target - self.elapsed()
        if d > 0:
            self.wait(d)
        elif d < -0.35:
            print(f"[drift] {self.SID}: {phrase!r} late by {-d:.2f}s")

    def at_s(self, secs):
        d = secs - self.elapsed()
        if d > 0:
            self.wait(d)


# ---------- shared pieces ----------

def gauge(frac):
    label = T("ground left for a vital force", 24, GREY).move_to([0, GAUGE_Y + 0.5, 0])
    track = Rectangle(width=GAUGE_W, height=0.3, stroke_color=GREY, stroke_width=2, fill_opacity=0)
    track.move_to([0, GAUGE_Y, 0])
    fill = gauge_fill(frac)
    return VGroup(label, track), fill


def gauge_fill(frac):
    w = max(GAUGE_W * frac, 0.02)
    r = Rectangle(width=w, height=0.3, stroke_width=0, fill_color=RED, fill_opacity=0.9)
    r.move_to([-GAUGE_W / 2 + w / 2, GAUGE_Y, 0])
    return r


def spark(radius=0.17, color=RED):
    return Star(n=4, outer_radius=radius, inner_radius=radius * 0.38, color=color,
                fill_color=color, fill_opacity=1, stroke_width=1)


def arrow(a, b, color=GREY, **kw):
    return Arrow(a, b, buff=0.12, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=8, **kw)


def beaker(w=1.7, h=2.2, level=0.72, liquid=GOLD, fill_op=0.72):
    wall = VMobject(stroke_color=TEXT, stroke_width=4, fill_opacity=0)
    wall.set_points_as_corners([[-w / 2, h / 2, 0], [-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2, 0]])
    liq = Rectangle(width=w - 0.1, height=h * level, stroke_width=0, fill_color=liquid, fill_opacity=fill_op)
    liq.move_to([0, -h / 2 + h * level / 2 + 0.05, 0])
    g = VGroup(liq, wall)
    g.surface_y = -h / 2 + h * level + 0.05
    g.bottom_y = -h / 2 + 0.2
    return g


class Fizz(VGroup):
    """Rising CO2 bubbles for a beaker (positions are relative; call move_to on the beaker first via anchor)."""
    def __init__(self, cx, y_lo, y_hi, width=1.2, n=9, color=GREEN, seed=1):
        super().__init__()
        rnd = random.Random(seed)
        self.cx, self.y_lo, self.y_hi, self.width = cx, y_lo, y_hi, width
        self.ph = [rnd.random() for _ in range(n)]
        self.xs = [rnd.uniform(-width / 2, width / 2) for _ in range(n)]
        self.sp = [rnd.uniform(0.22, 0.38) for _ in range(n)]
        self.rs = [rnd.uniform(0.05, 0.1) for _ in range(n)]
        self.t = 0.0
        for r in self.rs:
            self.add(Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.25))
        self._place()
        self.add_updater(lambda m, dt: m._tick(dt))

    def _place(self):
        for i, b in enumerate(self.submobjects):
            f = (self.t * self.sp[i] + self.ph[i]) % 1.0
            y = self.y_lo + f * (self.y_hi - self.y_lo)
            x = self.cx + self.xs[i] + 0.07 * math.sin(7 * f + i)
            b.move_to([x, y, 0])
            o = min(1.0, f * 6) * min(1.0, (1 - f) * 6)
            b.set_stroke(opacity=o)
            b.set_fill(opacity=0.25 * o)

    def _tick(self, dt):
        self.t += dt
        self._place()


def dashed_wall(x=0.0, y0=-3.2, y1=2.6):
    return DashedLine([x, y0, 0], [x, y1, 0], color=GREY, stroke_width=6, dash_length=0.22, dashed_ratio=0.65)


# ============================================================ scenes

class S00Title(TitleCard):
    LESSON = "Opening interlude · Vitalism"
    TITLE = "The Fall of the Vital Force"


# ------------------------------------------------------------------ 1
class S01Claim(VS):
    SID = "s01_claim"
    ANCH = [("make them.", 7.43), ("vital force.", 11.13), ("drew the line.", 13.76),
            ("rocks and salts,", 17.52), ("ordinary law.", 19.2), ("Organic matter,", 20.57),
            ("living bodies,", 22.4)]

    def construct(self):
        cx = 0.0
        cell = VGroup(Circle(radius=0.88, color=GREEN, fill_color=GREEN, fill_opacity=0.18, stroke_width=3.5),
                      T("living\ncell", 26, GREEN, line_spacing=0.7)).move_to([cx, -1.4, 0])
        cell[1].move_to(cell[0])
        chips = VGroup(*[chip(n, GREEN, 28) for n in ("sugar", "fat", "urea")])
        for c, x in zip(chips, (-2.0, 0.0, 2.0)):
            c.move_to([x, 1.0, 0])
        arrows = VGroup(*[arrow([cx, -0.5, 0], c.get_bottom(), GREEN) for c in chips])

        self.wait(0.3)
        self.play(GrowFromCenter(cell), run_time=1.0)
        self.at("molecules of living things")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c, shift=UP * 0.15))
                                for a, c in zip(arrows, chips)], lag_ratio=0.35), run_time=2.4)
        self.at("to need living things")
        self.play(Indicate(cell, color=GREEN, scale_factor=1.08), run_time=1.3)

        # the vital force: a spark rides each arrow up into each molecule
        self.at("all of it was supposed")
        label = VGroup(spark(0.17), T("vital\nforce", 26, RED, line_spacing=0.7)).arrange(RIGHT, buff=0.15)
        label.next_to(cell, RIGHT, buff=0.3)
        dots = VGroup(*[spark(0.16) for _ in chips])
        for d in dots:
            d.move_to(cell.get_top() + UP * 0.1)
        self.add(dots)
        self.play(FadeIn(label, shift=LEFT * 0.2), run_time=0.7)
        self.play(*[MoveAlongPath(d, Line(cell.get_top() + UP * 0.1, c.get_bottom() + DOWN * 0.02))
                    for d, c in zip(dots, chips)], run_time=1.3)
        self.play(*[c[0].animate.set_stroke(RED, 3.5) for c in chips],
                  *[d.animate.move_to(c.get_corner(UR) + RIGHT * 0.05) for d, c in zip(dots, chips)], run_time=0.8)
        org = VGroup(cell, chips, arrows, label, dots)

        # Berzelius draws the line
        self.at("The chemist Berzelius")
        wall = dashed_wall(0)
        wlabel = T("Berzelius's line", 28, YELLOW).move_to([0, 3.15, 0])
        self.play(org.animate.shift(RIGHT * 3.4), Create(wall), FadeIn(wlabel, shift=DOWN * 0.1), run_time=1.8)

        self.at("Inorganic matter,")
        h_in = T("INORGANIC", 30, BLUE, weight=BOLD).move_to([-3.5, 2.1, 0])
        self.play(FadeIn(h_in, shift=RIGHT * 0.2), run_time=0.7)
        self.at("rocks and salts")
        rocks = chip("rocks", BLUE, 26).move_to([-4.6, 1.0, 0])
        salts = chip("salts", BLUE, 26).move_to([-2.4, 1.0, 0])
        self.play(FadeIn(rocks, shift=UP * 0.15), FadeIn(salts, shift=UP * 0.15), run_time=1.0)
        self.at("obeyed ordinary law")
        law = chip("ordinary law", BLUE, 26).move_to([-3.5, -3.0, 0])
        a1 = arrow(rocks.get_bottom(), law.get_top() + LEFT * 0.6, BLUE)
        a2 = arrow(salts.get_bottom(), law.get_top() + RIGHT * 0.6, BLUE)
        self.play(FadeIn(law, shift=UP * 0.15), GrowArrow(a1), GrowArrow(a2), run_time=1.2)

        self.at("Organic matter,")
        h_org = T("ORGANIC", 30, GREEN, weight=BOLD).move_to([3.4, 2.1, 0])
        self.play(FadeIn(h_org, shift=LEFT * 0.2), run_time=0.7)
        self.at("the chemistry of living bodies")
        ghost = chip("ordinary law", GREY, 26, fill_opacity=0.0).move_to([3.4, -3.0, 0])
        ghost[0].set_stroke(GREY, 2.5).set_stroke(opacity=0.8)
        cross = Line(ghost.get_left() + LEFT * 0.12, ghost.get_right() + RIGHT * 0.12, color=RED, stroke_width=6)
        self.play(FadeIn(ghost, shift=UP * 0.15), run_time=0.7)
        self.at("did not")
        self.play(Create(cross), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ 2
class S02Flask(VS):
    SID = "s02_flask"
    ANCH = [("In February 1828,", 2.17), ("an inorganic salt,", 5.26), ("ammonium cyanate.", 6.88),
            ("dispose of nitrogen.", 13.22), ("in the room.", 15.32), ("same formula:", 17.87),
            ("one carbon,", 18.88), ("connected differently.", 24.33)]

    def construct(self):
        tag = T("Wöhler · February 1828", 32, YELLOW).move_to([0, 3.15, 0])
        cy = chip("ammonium cyanate", BLUE, 32).move_to([-4.1, 0.6, 0])
        ur = chip("urea", GREEN, 32).move_to([4.6, 0.6, 0])
        sub_cy = T("inorganic salt", 26, BLUE).next_to(cy, UP, buff=0.3)
        sub_ur = T("body's nitrogen disposal", 26, GREEN).next_to(ur, UP, buff=0.3).align_to(ur, RIGHT)
        heat = T("heat", 28, YELLOW)
        arr = arrow(cy.get_right(), ur.get_left(), YELLOW)
        heat.next_to(arr, DOWN, buff=0.2)

        self.wait(0.3)
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=1.0)
        self.at("warmed an inorganic salt")
        self.play(FadeIn(cy, shift=UP * 0.15), FadeIn(sub_cy), run_time=1.0)
        self.at("What crystallized")
        self.play(GrowArrow(arr), FadeIn(heat), run_time=1.0)
        self.play(FadeIn(ur, shift=UP * 0.15), run_time=0.9)
        self.at("the molecule the body makes")
        self.play(FadeIn(sub_ur, shift=UP * 0.1), run_time=0.8)

        self.at("There was no kidney")
        kid = chip("kidney", GREEN, 28, fill_opacity=0.0).move_to([0.2, 1.95, 0])
        kid[0].set_stroke(GREEN, 2.5, opacity=0.6)
        kid[1].set_opacity(0.7)
        cross = Line(kid.get_left() + LEFT * 0.15, kid.get_right() + RIGHT * 0.15, color=RED, stroke_width=6)
        self.play(FadeIn(kid, shift=DOWN * 0.1), run_time=0.6)
        self.play(Create(cross), run_time=0.5)

        self.at("Both compounds")
        f1 = M("CH₄N₂O", 32).move_to([-4.3, -0.6, 0])
        f2 = M("CH₄N₂O", 32).move_to([4.6, -0.6, 0])
        eq = M("=", 40, TEXT).move_to([0.2, -0.6, 0])
        self.play(FadeOut(VGroup(kid, cross)), run_time=0.4)
        self.play(FadeIn(f1, shift=UP * 0.1), FadeIn(f2, shift=UP * 0.1), FadeIn(eq), run_time=1.0)

        # atom tallies: identical bars under both
        self.at("one carbon,")
        counts = [("C", 1), ("H", 4), ("N", 2), ("O", 1)]
        unit = 0.32
        base_y = -3.0

        def tally(cx):
            bars, labs, nums = VGroup(), VGroup(), VGroup()
            for i, (el, n) in enumerate(counts):
                x = cx + (i - 1.5) * 0.72
                b = Rectangle(width=0.5, height=n * unit, stroke_width=0, fill_color=TEXT, fill_opacity=0.75)
                b.move_to([x, base_y + n * unit / 2, 0])
                bars.add(b)
                labs.add(M(el, 26, GREY).move_to([x, base_y - 0.33, 0]))
                nums.add(M(str(n), 26, TEXT).move_to([x, base_y + n * unit + 0.28, 0]))
            return bars, labs, nums

        L = tally(-4.3)
        R = tally(4.6)
        base_l = Line([-5.6, base_y, 0], [-3.0, base_y, 0], color=GREY, stroke_width=2)
        base_r = Line([3.3, base_y, 0], [5.9, base_y, 0], color=GREY, stroke_width=2)
        self.play(Create(base_l), Create(base_r), FadeIn(L[1]), FadeIn(R[1]), run_time=0.6)
        self.at("one carbon,")
        for i, ph in enumerate(["one carbon,", "four hydrogens,", "two nitrogens,", "one oxygen."]):
            self.at(ph, lead=0.1)
            self.play(GrowFromEdge(L[0][i], DOWN), GrowFromEdge(R[0][i], DOWN),
                      FadeIn(L[2][i]), FadeIn(R[2][i]), run_time=0.6)

        self.at("Same atoms,")
        same = T("same atoms,\ndifferent connections", 28, TEXT, line_spacing=0.8).move_to([0.2, -2.0, 0])
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.9)
        self.at("Heat rearranged")
        self.play(ShowPassingFlash(Line(cy.get_right(), ur.get_left(), color=YELLOW, stroke_width=10), time_width=0.6),
                  Indicate(heat, color=YELLOW), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------ 3
class S03Retreat(VS):
    SID = "s03_retreat"
    ANCH = [("that afternoon.", 3.39), ("honest objection:", 5.56), ("organic sources.", 9.26),
            ("somewhere to stand.", 12.88), ("in the chain.", 22.05)]

    def construct(self):
        gl, fill = gauge(1.0)
        self.play(FadeIn(gl), FadeIn(fill), run_time=0.8)

        # --- Wohler's row
        cy = chip("ammonium cyanate", BLUE, 30).move_to([-1.9, 0.1, 0])
        ur = chip("urea", GREEN, 30).move_to([3.9, 0.1, 0])
        a_main = arrow(cy.get_right(), ur.get_left(), YELLOW)
        wtag = T("Wöhler · 1828", 28, YELLOW).move_to([1.0, -0.6, 0])
        self.play(FadeIn(cy, shift=UP * 0.1), GrowArrow(a_main), FadeIn(ur, shift=UP * 0.1), FadeIn(wtag), run_time=1.2)
        self.at("did not kill")
        self.play(Transform(fill, gauge_fill(0.92)), run_time=1.2)

        self.at("His critics")
        src = chip("organic source", GREEN, 30).move_to([-1.9, -2.3, 0])
        a_back = DashedLine(cy.get_bottom(), src.get_top(), color=RED, stroke_width=4, dash_length=0.15)
        q = T("inorganic?", 28, RED).next_to(cy, UP, buff=0.25)
        self.at("could be traced back")
        back_lbl = T("traced back", 26, RED).next_to(a_back, RIGHT, buff=0.2)
        self.play(FadeIn(q, shift=DOWN * 0.1), Create(a_back), run_time=1.0)
        self.play(FadeIn(src, shift=UP * 0.15), FadeIn(back_lbl), run_time=0.9)

        self.at("The vital force pulled back")
        self.play(Transform(fill, gauge_fill(0.8)), run_time=1.6)
        self.wait(self.t_of("In 1845") - self.elapsed() - 0.7 if self.t_of("In 1845") - self.elapsed() > 0.7 else 0)
        self.play(FadeOut(VGroup(cy, ur, a_main, wtag, q, a_back, src, back_lbl)), run_time=0.6)

        # --- Kolbe, 1845
        self.at("In 1845")
        ktag = T("1845 · Kolbe", 32, YELLOW).move_to([0, 1.35, 0])
        ac = chip("acetic acid", GREEN, 30).move_to([4.8, -0.5, 0])
        cd = chip("carbon disulfide", BLUE, 30).move_to([-0.5, -0.5, 0])
        charc = chip("charcoal", BLUE, 30).move_to([-4.7, 0.4, 0])
        sulf = chip("molten sulfur", BLUE, 30).move_to([-4.6, -1.4, 0])
        a_ac = arrow(cd.get_right(), ac.get_left(), GREY)
        a_c = arrow(charc.get_right(), cd.get_left() + UP * 0.2, BLUE)
        a_s = arrow(sulf.get_right(), cd.get_left() + DOWN * 0.2, BLUE)
        self.play(FadeIn(ktag, shift=DOWN * 0.1), FadeIn(ac, shift=UP * 0.1), run_time=1.2)
        self.at("from carbon disulfide")
        self.play(FadeIn(cd, shift=RIGHT * 0.15), GrowArrow(a_ac), run_time=1.1)
        self.at("made from charcoal")
        self.play(FadeIn(charc, shift=RIGHT * 0.15), FadeIn(sulf, shift=RIGHT * 0.15), GrowArrow(a_c), GrowArrow(a_s),
                  run_time=1.3)
        self.at("with nothing alive")
        br = Brace(VGroup(charc, sulf, cd), DOWN, color=BLUE, buff=0.2)
        brl = T("nothing alive in the chain", 28, BLUE).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(brl, shift=UP * 0.1), run_time=1.0)
        self.play(Transform(fill, gauge_fill(0.55)), run_time=1.3)
        self.at_s(self.t_of("A decade later") - 0.6)
        self.play(FadeOut(VGroup(ktag, ac, cd, charc, sulf, a_ac, a_c, a_s, br, brl)), run_time=0.6)

        # --- Berthelot
        self.at("A decade later")
        btag = T("a decade later · Berthelot", 32, YELLOW).move_to([0, 1.35, 0])
        fats = chip("fats", GREEN, 30).move_to([4.6, -0.5, 0])
        gly = chip("glycerol", GREEN, 30).move_to([-4.2, 0.4, 0])
        fa = chip("fatty acids", GREEN, 30).move_to([-4.2, -1.4, 0])
        a_g = arrow(gly.get_right(), fats.get_left() + UP * 0.2, GREY)
        a_f = arrow(fa.get_right(), fats.get_left() + DOWN * 0.2, GREY)
        self.play(FadeIn(btag, shift=DOWN * 0.1), FadeIn(fats, shift=UP * 0.1), run_time=1.1)
        self.at("from glycerol")
        self.play(FadeIn(gly, shift=RIGHT * 0.15), FadeIn(fa, shift=RIGHT * 0.15), GrowArrow(a_g), GrowArrow(a_f),
                  Transform(fill, gauge_fill(0.4)), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ 4
class S04Redoubt(VS):
    SID = "s04_redoubt"
    ANCH = [("One redoubt remained.", 1.83), ("living yeast.", 6.24), ("living cell.", 13.64),
            ("forty years.", 16.76), ("inside yeast.", 25.5)]

    def construct(self):
        gl, fill = gauge(0.4)
        self.add(gl, fill)
        cy_ = -0.7
        cell = VGroup(Circle(radius=1.65, color=GREEN, fill_color=GREEN, fill_opacity=0.16, stroke_width=3.5),
                      T("yeast cell", 30, GREEN)).move_to([0, cy_, 0])
        cell[1].move_to(cell[0].get_center() + UP * 0.7)
        sugar = chip("sugar", GREEN, 30).move_to([-4.9, cy_, 0])
        prod = chip("alcohol\n+ CO₂", GREEN, 28).move_to([4.9, cy_, 0])
        a_in = arrow(sugar.get_right(), [-1.75, cy_, 0], GREEN)
        a_out = arrow([1.75, cy_, 0], prod.get_left(), GREEN)

        self.play(Indicate(fill, color=RED, scale_factor=1.0), GrowFromCenter(cell), run_time=1.5)
        self.at("Louis Pasteur")
        ptag = T("Pasteur", 32, YELLOW).move_to([-4.6, 0.55, 0])
        self.play(FadeIn(ptag, shift=DOWN * 0.1), run_time=0.7)
        self.at("fermentation depends")
        self.play(FadeIn(sugar, shift=RIGHT * 0.15), GrowArrow(a_in), run_time=0.9)
        self.play(GrowArrow(a_out), FadeIn(prod, shift=RIGHT * 0.15), run_time=1.0)

        self.at("a stronger line")
        fence = DashedVMobject(Circle(radius=2.1, color=RED, stroke_width=5), num_dashes=40).move_to([0, cy_, 0])
        self.play(Create(fence), run_time=3.0)
        self.at("inseparable")
        flab = T("inseparable from the living cell", 30, RED).move_to([0, -3.3, 0])
        self.play(FadeIn(flab, shift=UP * 0.1), run_time=1.0)

        self.at("That conviction")
        years = chip("forty years", YELLOW, 30).move_to([4.9, 0.6, 0])
        self.play(FadeIn(years, shift=DOWN * 0.1), fence.animate.set_stroke(width=8), run_time=1.0)
        self.play(Indicate(fence, color=RED, scale_factor=1.03), run_time=1.0)

        self.at("In 1877")
        ktag = T("1877 · Kühne", 32, YELLOW).move_to([-4.6, 0.55, 0])
        self.play(FadeOut(years), Transform(ptag, ktag), run_time=0.9)
        self.at("proposed the word enzyme")
        enz = chip("enzyme", TEAL, 32).move_to([0, cy_ - 0.35, 0])
        self.play(FadeIn(enz, scale=0.6), run_time=0.9)
        self.at("from the Greek")
        greek = T("Greek: “in leaven”", 28, TEAL).move_to([4.7, 0.6, 0])
        self.play(FadeIn(greek, shift=DOWN * 0.1), run_time=0.8)
        self.at("soluble agent")
        self.play(Indicate(enz, color=TEAL, scale_factor=1.15), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ 5
class S05Buchner(VS):
    SID = "s05_buchner"
    ANCH = [("no intact cells in it.", 7.93), ("preserve it.", 9.98), ("began to ferment,", 11.54),
            ("dead yeast.", 14.97), ("must have survived.", 18.28), ("two controls.", 20.4),
            ("destructible chemical.", 24.54)]

    def construct(self):
        gl, fill = gauge(0.4)
        self.add(gl, fill)

        yeast = chip("brewer's\nyeast", GREEN, 26).move_to([-5.0, 0.9, 0])
        sand = chip("sand", GREY, 26).move_to([-5.0, -0.8, 0])
        press = chip("grind\n& press", YELLOW, 26).move_to([-1.9, 0.05, 0])
        bk = beaker().move_to([2.4, -0.1, 0])
        a1 = arrow(yeast.get_right(), press.get_left() + UP * 0.2, GREEN)
        a2 = arrow(sand.get_right(), press.get_left() + DOWN * 0.2, GREY)
        a3 = arrow(press.get_right(), [1.35, 0.0, 0], YELLOW)
        jlab = T("clear golden juice", 26, GOLD).move_to([2.4, -1.85, 0])
        nocell = VGroup(Circle(radius=0.2, color=GREEN, stroke_width=3),
                        VGroup(Line(UL, DR), Line(UR, DL)).scale(0.22).set_color(RED).set_stroke(width=5))
        nocell_t = T("no intact\ncells", 26, GREEN, line_spacing=0.7)
        nocell_g = VGroup(nocell, nocell_t).arrange(RIGHT, buff=0.2).move_to([5.45, 0.5, 0])

        self.wait(0.3)
        self.play(FadeIn(yeast, shift=RIGHT * 0.15), FadeIn(sand, shift=RIGHT * 0.15), run_time=1.0)
        self.at("with sand")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(press, scale=0.8), run_time=1.0)
        self.at("pressed out")
        self.play(GrowArrow(a3), FadeIn(bk, shift=LEFT * 0.2), run_time=1.0)
        self.play(FadeIn(jlab, shift=UP * 0.1), run_time=0.7)
        self.at("with no intact cells")
        self.play(FadeIn(nocell_g, shift=LEFT * 0.15), run_time=0.9)

        self.at("He added sugar")
        sg = chip("sugar", GREEN, 26).move_to([2.4, 1.9, 0])
        self.play(FadeIn(sg, shift=DOWN * 0.15), run_time=0.7)
        self.play(sg.animate.move_to([2.4, bk.surface_y - 0.25 - 0.1, 0]).scale(0.7), run_time=1.0)
        self.play(FadeOut(sg, scale=0.5), run_time=0.4)

        self.at("The sugar began to ferment")
        fz = Fizz(2.4, bk.bottom_y - 0.1, bk.surface_y - 0.1, width=1.1, n=9, seed=3)
        self.add(fz)
        self.at("carbon dioxide rising")
        co2 = T("CO₂", 30, GREEN).move_to([2.4, 1.55, 0])
        self.play(FadeIn(co2, shift=DOWN * 0.1), run_time=0.8)
        self.at("a flask of dead yeast")
        self.play(Indicate(jlab, color=GOLD, scale_factor=1.1), run_time=1.0)

        # the vitalist objection
        self.at("Vitalists said", lead=0.2)
        vit = chip("vitalists:\nliving scraps?", RED, 28).move_to([-3.4, 0.2, 0])
        a_v = DashedLine(vit.get_right(), [1.35, 0.1, 0], color=RED, stroke_width=4, dash_length=0.14)
        self.play(FadeOut(VGroup(yeast, sand, press, a1, a2, a3, nocell_g)), FadeIn(vit, shift=RIGHT * 0.15),
                  Create(a_v), run_time=0.9)

        # two controls
        self.at("Büchner ran two controls")
        self.play(FadeOut(VGroup(vit, a_v, co2, jlab)), run_time=0.5)
        ctitle = T("two controls", 32, YELLOW).move_to([0, 1.75, 0])
        bk2 = bk.copy()
        fz.clear_updaters()
        self.play(FadeOut(fz), run_time=0.35)
        self.play(Write(ctitle), bk.animate.move_to([-3.6, -0.3, 0]), run_time=1.2)
        bk2.move_to([3.6, -0.3, 0])
        fz2 = Fizz(3.6, -0.3 + bk.bottom_y - 0.1, -0.3 + bk.surface_y - 0.1, width=1.1, n=9, seed=5)
        lab_b = T("boiled juice", 28, YELLOW).move_to([-3.6, -1.95, 0])
        lab_f = T("filtered juice", 28, YELLOW).move_to([3.6, -1.95, 0])
        funnel = Polygon([-0.7, 0.4, 0], [0.7, 0.4, 0], [0.12, -0.2, 0], [0.12, -0.5, 0], [-0.12, -0.5, 0], [-0.12, -0.2, 0],
                         color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([3.6, 1.25, 0])
        self.play(FadeIn(bk2, shift=LEFT * 0.2), FadeIn(funnel, shift=DOWN * 0.2), FadeIn(lab_b), FadeIn(lab_f), run_time=1.0)

        # boiled: fizz stops
        self.at("Boiled juice")
        waves = VGroup(*[ParametricFunction(lambda t, x0=x0: np.array([x0 + 0.08 * math.sin(6 * t), t, 0]),
                                            t_range=[0, 0.55], color=YELLOW, stroke_width=4)
                         for x0 in (-0.35, 0, 0.35)]).move_to([-3.6, 1.15, 0])
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), run_time=1.0)
        nofizz = T("no fizz", 28, GREY).move_to([-3.6, -2.55, 0])
        self.play(FadeIn(nofizz, shift=UP * 0.1), run_time=0.6)
        self.at("so the agent was")
        agent = chip("destructible chemical", TEAL, 26).move_to([-3.6, -3.25, 0])
        self.play(FadeIn(agent, shift=UP * 0.1), run_time=0.9)

        # filtered: still fizzing
        self.at("Filtered juice still did")
        self.add(fz2)
        t0 = self.elapsed()
        fill.add_updater(lambda m: m.become(gauge_fill(max(0.0, 0.4 * (1 - (self.elapsed() - t0) / 2.2)))))
        self.play(Indicate(lab_f, color=GREEN), run_time=0.9)
        self.at("so no cells", lead=0.3)
        nocell2 = T("no cells needed", 28, GREEN).move_to([3.6, -2.55, 0])
        self.play(FadeIn(nocell2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 6
class S06Course(VS):
    SID = "s06_course"
    ANCH = [("one process at a time.", 7.6), ("law of its own.", 17.46)]

    def construct(self):
        # --- timeline of syntheses
        x0, x1 = -5.5, 5.5
        yr = lambda y: x0 + (y - 1828) / (1897 - 1828) * (x1 - x0)
        N = 40
        line = VGroup(*[Line([x0 + (x1 - x0) * i / N, 0.2, 0], [x0 + (x1 - x0) * (i + 1) / N, 0.2, 0], stroke_width=9,
                             color=interpolate_color(ManimColor(RED), ManimColor(GREY), i / N)).set_opacity(1 - 0.75 * i / N)
                       for i in range(N)])
        vf = VGroup(spark(0.2), T("vital force", 26, RED)).arrange(RIGHT, buff=0.15).move_to([-4.3, -0.55, 0])
        marks = [
            (1828, "urea\n1828", UP, 2.0),
            (1845, "acetic acid\n1845", DOWN, -1.7),
            (1854, "fats\n1854", UP, 2.0),
            (1897, "fermentation\n1897", DOWN, -1.7),
        ]
        items = []
        for y, txt, d, ty in marks:
            x = yr(y)
            tick = Dot([x, 0.2, 0], radius=0.1, color=TEXT)
            cx = min(x, 4.9)
            c = chip(txt, GREEN, 26).move_to([cx, ty, 0])
            stem = Line([x, 0.2, 0], c.get_top() if ty < 0 else c.get_bottom(), color=GREY, stroke_width=2)
            items.append(VGroup(stem, tick, c))

        for g in [line, vf, *items]:
            g.shift(DOWN * 0.5)
        self.wait(0.3)
        self.play(Create(line), FadeIn(vf), run_time=1.3)
        self.at("Seventy years")
        self.play(FadeIn(items[0], shift=UP * 0.1), run_time=0.7)
        self.at("made the vital force")
        # the molecule milestones land early, so the process milestone gets its own moment
        self.play(LaggedStart(FadeIn(items[1], shift=DOWN * 0.1), FadeIn(items[2], shift=UP * 0.1), lag_ratio=0.5),
                  run_time=1.2)
        self.at("one molecule")
        self.play(*[Indicate(it[2], color=GREEN, scale_factor=1.08) for it in items[:3]], run_time=0.9)
        self.at("one process")
        self.play(FadeIn(items[3], shift=DOWN * 0.1), vf.animate.set_opacity(0.15), run_time=0.7)
        self.play(Indicate(items[3][2], color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("What replaced it")
        self.play(FadeOut(VGroup(line, vf, *items)), run_time=0.5)

        # --- the two kingdoms from the start, walled
        self.at("What replaced it")
        rocks = chip("rocks", BLUE, 28).move_to([-4.6, 0.2, 0])
        salts = chip("salts", BLUE, 28).move_to([-2.6, 0.2, 0])
        cell = VGroup(Circle(radius=1.3, color=GREEN, fill_color=GREEN, fill_opacity=0.18, stroke_width=3.5),
                      T("living cell", 26, GREEN)).move_to([3.6, 0.1, 0])
        cell[1].move_to(cell[0].get_center() + UP * 0.6)
        vf2 = VGroup(spark(0.17), T("vital force", 26, RED)).arrange(RIGHT, buff=0.15).move_to([3.6, -1.6, 0])
        wall = dashed_wall(0, -1.6, 1.9)
        self.play(FadeIn(rocks), FadeIn(salts), GrowFromCenter(cell), FadeIn(wall), FadeIn(vf2), run_time=1.4)

        self.at("a living cell obeys")
        self.play(Indicate(cell, color=GREEN, scale_factor=1.1), run_time=1.0)
        self.at("the same chemistry")
        box = RoundedRectangle(corner_radius=0.3, width=12.2, height=4.8, stroke_color=TEXT, stroke_width=3.5,
                               fill_opacity=0).move_to([0, 0.0, 0])
        head = T("the same chemistry", 34, TEXT).move_to([0, 1.9, 0])
        self.play(FadeOut(wall, shift=UP * 0.3), Create(box), FadeIn(head, shift=DOWN * 0.1), run_time=1.6)
        self.at("with no separate law")
        self.play(FadeOut(vf2, shift=DOWN * 0.2), run_time=1.2)

        # --- the enzyme
        self.at("The catalysts")
        enz = chip("enzyme", TEAL, 26).move_to(cell.get_center() + DOWN * 0.45)
        self.play(FadeIn(enz, scale=0.6), run_time=0.8)
        self.at("Kühne named")
        kn = T("named by Kühne", 26, YELLOW).move_to([3.6, -1.9, 0])
        self.play(FadeIn(kn, shift=UP * 0.1), run_time=0.7)
        self.at("Büchner freed")
        bn = T("freed by Büchner", 26, YELLOW).move_to([0.1, -0.65, 0])
        self.play(enz.animate.move_to([0.1, 0.1, 0]), FadeOut(kn), FadeIn(bn), run_time=1.5)
        self.at("ordinary proteins")
        prot = T("ordinary proteins", 36, TEAL).move_to([0, -1.5, 0])
        self.play(FadeIn(prot, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Step through the seventy-year retreat in the lesson's timeline."
