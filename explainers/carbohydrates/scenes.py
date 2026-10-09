"""Carbohydrates: one bond decides fuel or fiber.

COLOR MAP (one color per concept, whole video)
  BLUE   = glucose / the monomer "brick" (cells, blocks, ring disc)
  RED    = the carbonyl carbon C1 -> the anomeric carbon (reactive end)
  YELLOW = a hydroxyl (OH): the one that differs, the C5 OH that attacks, the free ends of glycogen
  GREEN  = alpha linkage / storage / digestible fuel
  TEAL   = beta linkage / structure / fiber
  PURPLE = enzyme
  GREY   = neutral labels, hydrogen-bond dashes
  TEXT   = reaction products, plain text
No molecular structures are drawn: sugars are numbered tiles, discs and blocks; bonds between monomers are plain links.
"""
import json
import os
import math
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CE0"


# ----------------------------------------------------------------------------- helpers
class BP(NarratedScene):
    """NarratedScene + phrase-timed beats: self.at("phrase") waits until that phrase is being spoken."""

    def setup(self):
        super().setup()
        self.narr = ""
        try:
            sid, sp = os.environ["KX_SCENE_ID"], os.environ["KX_SCRIPT"]
            for s in json.load(open(sp))["scenes"]:
                if s["id"] == sid:
                    self.narr = s.get("narration", "")
        except Exception:
            pass

    def t_of(self, phrase):
        i = self.narr.find(phrase)
        if i < 0:
            raise ValueError(f"phrase not in narration: {phrase!r}")
        return i / len(self.narr) * self.narration_s

    def at(self, phrase, lead=0.5):
        d = max(0.0, self.t_of(phrase) - lead) - self.elapsed()
        if d > 0:
            self.wait(d)

    def until(self, phrase, lead=0.5):
        """seconds from now until `phrase` is spoken (for run_time)."""
        return max(0.4, self.t_of(phrase) - lead - self.elapsed())


def cell(label, color, filled=False, size=0.62, fs=24, dashed=False):
    sq = RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=0.95 if filled else 0.14)
    if dashed:
        sq = DashedVMobject(RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color,
                                             stroke_width=3, fill_opacity=0), num_dashes=16)
    t = M(label, fs, BG if filled else color)
    return VGroup(sq, t.move_to(sq.get_center()))


def block(size=0.42, color=BLUE):
    return RoundedRectangle(corner_radius=0.07, width=size, height=size, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.9)


def link(a, b, color, width=5, dashed=False):
    cls = DashedLine if dashed else Line
    return always_redraw(lambda: cls(a.get_center(), b.get_center(), color=color, stroke_width=width).set_z_index(-1))


# ----------------------------------------------------------------------------- ring-closure kit (s02, s03)
RING_C = np.array([0.0, 0.3, 0])
RING_R = 1.8
L_POS = [np.array([0.0, 2.5 - 1.0 * i, 0]) for i in range(6)]
# The chain bends into an OPEN horseshoe (C1..C5 on an arc with a wide gap on the right), never a closed ring of
# atoms: the C5 hydroxyl tag swings across the gap to C1, then the whole tape collapses into the plain "ring" disc.
_ANG = [35, 95, 155, 215, 275]
R_POS = [RING_C + RING_R * np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0]) for a in _ANG]
R_POS.append(RING_C + 3.1 * np.array([math.cos(math.radians(262)), math.sin(math.radians(262)), 0]))
OH_L = np.array([1.2, -1.5, 0])
OH_R = R_POS[0] + np.array([0.75, -0.75, 0])   # the C5 hydroxyl ends up touching C1


class Tape:
    """Six numbered tiles (C1..C6) that curl from a vertical chain into a ring of five, plus the C5 hydroxyl tag.
    The disc stays invisible until collapse() turns the bent tape into one plain "ring" object."""

    def __init__(self, scene):
        self.scene = scene
        self.cells = [cell(str(i + 1), RED if i == 0 else BLUE, size=0.78, fs=30) for i in range(6)]
        self.t = ValueTracker(0)
        self.disc = Circle(radius=RING_R, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0)
        self.disc.set_stroke(opacity=0).move_to(RING_C)
        for i, c in enumerate(self.cells):
            c.move_to(L_POS[i])
            c.add_updater(lambda m, i=i: m.move_to(self.pos(i)))
        oh = chip("OH", YELLOW, size=30, pad=0.14)
        lab = T("on C5", 26, YELLOW)
        self.oh = VGroup(oh, lab.next_to(oh, RIGHT, buff=0.15))
        self.oh.shift(OH_L - oh.get_center())
        self.oh.add_updater(lambda m: m.shift(self._oh_pos() - m[0].get_center()))
        self.group = VGroup(*self.cells)

    def _e(self):
        return self.t.get_value()

    def _oh_pos(self):
        e = self._e()
        return OH_L * (1 - e) + OH_R * e

    def pos(self, i):
        t = self._e()
        p = L_POS[i] * (1 - t) + R_POS[i] * t
        if i == 0:   # the carbonyl end swings out around the others instead of cutting through
            p = p + math.sin(math.pi * t) * np.array([0.9, 0.7, 0])
        return p

    def collapse_anims(self):
        return [FadeOut(VGroup(*self.cells), scale=0.5), FadeOut(self.oh, scale=0.5),
                self.disc.animate.set_fill(BLUE, opacity=0.2).set_stroke(BLUE, opacity=1)]

    def freeze(self):
        for m in [*self.cells, self.oh, self.disc]:
            m.clear_updaters()


def ring_token(center, tag, r=1.25):
    """Disc with red C1 dot on the right rim and a yellow OH tag above (beta) or below (alpha) the ring."""
    disc = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2)
    lab = T("ring", 30, BLUE)
    dot = Circle(radius=0.2, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(RIGHT * r)
    s = 1 if tag == "up" else -1
    stalk = Line(RIGHT * r + UP * s * 0.18, RIGHT * r + UP * s * 0.75, color=YELLOW, stroke_width=4)
    oh = chip("OH", YELLOW, size=30, pad=0.13).move_to(RIGHT * r + UP * s * 1.08)
    return VGroup(disc, lab, dot, stalk, oh).shift(center)


# ============================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Carbohydrates"
    TITLE = "One bond decides fuel or fiber"


class S01Cast(BP):
    def construct(self):
        CS = 0.58

        def strip(n, red_idx, yellow_idx=None, dashed_idx=None):
            cs = []
            for i in range(1, n + 1):
                if i == red_idx:
                    cs.append(cell(str(i), RED, filled=True, size=CS, fs=26))
                elif i == yellow_idx:
                    cs.append(cell(str(i), YELLOW, filled=True, size=CS, fs=26))
                elif i == dashed_idx:
                    cs.append(cell(str(i), YELLOW, size=CS, fs=26, dashed=True))
                else:
                    cs.append(cell(str(i), GREY, size=CS, fs=26))
            return VGroup(*cs).arrange(RIGHT, buff=0.07)

        def group(name, color, st, x, y_chip):
            c = chip(name, color, size=32).move_to([x, y_chip, 0])
            st.move_to([x, y_chip - 0.85, 0])
            return c, st

        TY, BY = 2.5, -0.85
        rib_c, rib_s = group("ribose", GREY, strip(5, 1), -4.75, TY)
        dox_c, dox_s = group("deoxyribose", GREY, strip(5, 1, dashed_idx=2), -0.95, TY)
        fru_c, fru_s = group("fructose", GREY, strip(6, 2), 4.3, TY)
        glc_c, glc_s = group("glucose", BLUE, strip(6, 1), -4.3, BY)
        man_c, man_s = group("mannose", GREY, strip(6, 1, 2), 0.0, BY)
        gal_c, gal_s = group("galactose", GREY, strip(6, 1, 4), 4.3, BY)

        pent_lab = T("PENTOSES  ·  5 carbons", 26, GREY).move_to([-2.85, 3.3, 0])
        hex_lab = T("HEXOSES  ·  6 carbons", 26, GREY).move_to([0, 0.15, 0])
        ket_lab = T("KETOSE", 26, GREY).move_to([4.3, 3.3, 0])
        divider = DashedLine([2.25, 3.55, 0], [2.25, 0.75, 0], color=GREY, stroke_width=2)

        cap_dox = T("one OH missing at C2", 26, YELLOW).move_to([-0.95, 1.05, 0])
        cap_man = T("epimer at C2", 26, YELLOW).move_to([0, -2.3, 0])
        cap_gal = T("epimer at C4", 26, YELLOW).move_to([4.3, -2.3, 0])
        cap_fru = T("carbonyl at C2", 26, RED).move_to([4.3, 1.05, 0])
        cap_glc = T("the reference", 26, BLUE).move_to([-4.3, -2.3, 0])

        lg1 = cell("", RED, filled=True, size=0.34)
        lg1t = T("carbonyl carbon", 26, RED)
        lg2 = cell("", YELLOW, filled=True, size=0.34)
        lg2t = T("the hydroxyl that differs", 26, YELLOW)
        legend = VGroup(VGroup(lg1, lg1t).arrange(RIGHT, buff=0.2), VGroup(lg2, lg2t).arrange(RIGHT, buff=0.2)) \
            .arrange(RIGHT, buff=0.9).move_to([0, -3.3, 0])

        self.play(FadeIn(pent_lab), FadeIn(hex_lab), FadeIn(ket_lab), Create(divider), run_time=0.8)
        self.at("The pentoses", 0.3)
        self.play(FadeIn(rib_c, shift=UP * 0.15), FadeIn(dox_c, shift=UP * 0.15), run_time=0.6)
        self.play(LaggedStart(FadeIn(rib_s), FadeIn(dox_s), lag_ratio=0.3), FadeIn(legend), run_time=1.0)
        self.at("the only difference", 0.3)
        self.play(FadeIn(cap_dox, shift=UP * 0.1), Indicate(dox_s[1], color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.at("The hexoses", 0.3)
        self.play(FadeIn(glc_c, shift=UP * 0.15), FadeIn(man_c, shift=UP * 0.15), FadeIn(gal_c, shift=UP * 0.15),
                  run_time=0.7)
        self.play(LaggedStart(FadeIn(glc_s), FadeIn(man_s), FadeIn(gal_s), lag_ratio=0.25), FadeIn(cap_glc),
                  run_time=1.2)
        self.at("mannose at C2", 0.4)
        self.play(FadeIn(cap_man, shift=UP * 0.1), Indicate(man_s[1], color=YELLOW, scale_factor=1.35), run_time=1.0)
        self.at("galactose at C4", 0.2)
        self.play(FadeIn(cap_gal, shift=UP * 0.1), Indicate(gal_s[3], color=YELLOW, scale_factor=1.35), run_time=1.0)
        self.at("And fructose", 0.3)
        self.play(FadeIn(fru_c, shift=UP * 0.15), FadeIn(fru_s), run_time=0.9)
        self.at("a ketose", 0.2)
        self.play(FadeIn(cap_fru, shift=UP * 0.1), Indicate(fru_s[1], color=RED, scale_factor=1.35), run_time=1.0)
        self.at("Six sugars", 0.4)
        six = VGroup(rib_c, dox_c, glc_c, man_c, gal_c, fru_c)
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.08) for c in six], run_time=1.4)
        self.finish()


class S02Ring(BP):
    def construct(self):
        tape = Tape(self)
        carb = T("carbonyl", 30, RED).next_to(tape.cells[0], LEFT, buff=0.4)
        cap = T("open-chain glucose", 30, GREY).move_to([0, -3.35, 0])

        # a. sugars are chains
        self.add(tape.disc)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in tape.cells], lag_ratio=0.15), run_time=1.6)
        self.play(FadeIn(carb), FadeIn(tape.oh), FadeIn(cap), run_time=0.8)
        self.wait(self.until("The chemistry"))

        # b. the two reactions
        self.play(FadeOut(tape.group), FadeOut(carb), FadeOut(tape.oh), FadeOut(cap), run_time=0.7)

        def row(a, b, c, y, ax=-4.3):
            a.move_to([ax, y, 0])
            plus = T("+", 40, GREY).move_to([-2.55, y, 0])
            b.move_to([-1.15, y, 0])
            arr = Arrow([0.3, y, 0], [1.6, y, 0], color=GREY, buff=0, stroke_width=6)
            c.move_to([3.45, y, 0])
            return VGroup(a, plus, b, arr, c)

        r1 = row(chip("aldehyde", RED, size=36), chip("alcohol", YELLOW, size=36), chip("hemiacetal", TEXT, size=36), 1.1)
        r2 = row(chip("ketone", RED, size=36), chip("alcohol", YELLOW, size=36), chip("hemiketal", TEXT, size=36), -1.1)
        self.play(FadeIn(r1[0]), FadeIn(r1[1]), FadeIn(r1[2]), run_time=0.9)
        self.play(GrowArrow(r1[3]), FadeIn(r1[4], shift=RIGHT * 0.2), run_time=0.9)
        self.at("and a ketone", 0.3)
        self.play(FadeIn(r2[0]), FadeIn(r2[1]), FadeIn(r2[2]), run_time=0.9)
        self.play(GrowArrow(r2[3]), FadeIn(r2[4], shift=RIGHT * 0.2), run_time=0.9)
        self.at("In a hexose", 0.2)
        self.play(FadeOut(VGroup(r1, r2)), run_time=0.6)

        # c. the ring closes
        self.play(FadeIn(tape.group), FadeIn(carb), FadeIn(tape.oh), run_time=0.8)
        self.at("swings around", 0.9)
        self.play(FadeOut(carb), run_time=0.3)
        self.play(tape.t.animate.set_value(1), run_time=3.8, rate_func=smooth)
        flash = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=6).move_to((R_POS[0] + OH_R) / 2)
        self.play(Create(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.3)
        enz = chip("enzyme", PURPLE, size=34)
        cross = VGroup(Line(UL * 0.5, DR * 0.5, color=RED, stroke_width=8), Line(UR * 0.5, DL * 0.5, color=RED, stroke_width=8))
        ne = VGroup(enz, cross.move_to(enz)).move_to([-4.6, 0.3, 0])
        ne_lab = T("not needed", 30, PURPLE).next_to(ne, DOWN, buff=0.3)
        self.at("no enzyme needed", 0.3)
        self.play(FadeIn(ne), FadeIn(ne_lab), run_time=0.7)

        # d. anomeric carbon
        self.at("That ring-closure", 0.2)
        tape.freeze()
        ringlab = T("ring", 34, BLUE).move_to(RING_C)
        dot = Circle(radius=0.24, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(R_POS[0])
        self.play(*tape.collapse_anims(), FadeIn(ringlab), FadeOut(ne), FadeOut(ne_lab), run_time=1.0)
        self.play(FadeIn(dot, scale=2), run_time=0.5)
        ac = T("anomeric carbon", 36, RED).move_to([4.5, 0.3, 0])
        arrow = Arrow(ac.get_left() + LEFT * 0.05, R_POS[0] + RIGHT * 0.35, color=RED, buff=0.05, stroke_width=5)
        self.play(FadeIn(ac, shift=LEFT * 0.2), GrowArrow(arrow), run_time=0.8)
        self.play(Indicate(dot, color=RED, scale_factor=1.6), run_time=0.9)
        self.finish()


class S03Anomers(BP):
    def construct(self):
        tape = Tape(self)
        cap = T("open-chain glucose", 30, GREY).move_to([0, -3.35, 0])
        self.add(tape.disc)
        self.play(LaggedStart(*[FadeIn(c) for c in tape.cells], lag_ratio=0.1), FadeIn(tape.oh), FadeIn(cap),
                  run_time=1.2)
        self.at("The open-chain aldehyde folds", 0.3)
        self.play(tape.t.animate.set_value(1), FadeOut(cap), run_time=min(4.2, self.until("The old carbonyl", 0.5)),
                  rate_func=smooth)
        tape.freeze()
        ringlab = T("ring", 34, BLUE).move_to(RING_C)
        self.play(*tape.collapse_anims(), FadeIn(ringlab), run_time=0.9)
        ring0 = VGroup(tape.disc, ringlab)

        # anomeric carbon
        self.at("The old carbonyl", 0.3)
        dot = Circle(radius=0.24, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(R_POS[0])
        ac = T("anomeric carbon", 36, RED).move_to([4.5, 0.6, 0])
        nc = T("a brand-new chiral center", 28, GREY).next_to(ac, DOWN, buff=0.2)
        arrow = Arrow(ac.get_left() + LEFT * 0.05, R_POS[0] + RIGHT * 0.35, color=RED, buff=0.05, stroke_width=5)
        self.play(FadeIn(dot, scale=2), run_time=0.5)
        self.play(FadeIn(ac, shift=LEFT * 0.2), GrowArrow(arrow), run_time=0.7)
        self.play(FadeIn(nc), Indicate(dot, color=RED, scale_factor=1.6), run_time=1.0)

        # two ways
        self.at("it can point two ways", 0.3)
        self.play(FadeOut(ac), FadeOut(nc), FadeOut(arrow), run_time=0.5)
        ring_all = VGroup(ring0, dot)
        tokA = ring_token(np.array([-3.8, 1.0, 0]), "down")
        tokB = ring_token(np.array([3.8, 1.0, 0]), "up")
        base_a = VGroup(*[m for m in tokA[:3]])
        base_b = VGroup(*[m for m in tokB[:3]])
        self.play(ReplacementTransform(VGroup(tape.disc.copy(), dot.copy()), VGroup(tokA[0], tokA[2])),
                  ReplacementTransform(VGroup(tape.disc, dot), VGroup(tokB[0], tokB[2])),
                  FadeOut(ringlab), FadeIn(tokA[1]), FadeIn(tokB[1]), run_time=1.3)
        labA = VGroup(M("α", 34, GREEN), T("·  OH below the ring", 30, GREEN)).arrange(RIGHT, buff=0.18).move_to([-3.8, -1.3, 0])
        labB = VGroup(M("β", 34, TEAL), T("·  OH above the ring", 30, TEAL)).arrange(RIGHT, buff=0.18).move_to([3.8, -1.3, 0])
        self.at("the alpha form", 0.1)
        self.play(FadeIn(tokA[3]), FadeIn(tokA[4]), FadeIn(labA), run_time=0.8)
        self.at("the beta form", 0.1)
        self.play(FadeIn(tokB[3]), FadeIn(tokB[4]), FadeIn(labB), run_time=0.8)

        # interconversion + ratio
        self.at("In solution", 0.3)
        mid = chip("open chain", BLUE, size=32).move_to([0, 1.0, 0])
        aL = DoubleArrow([-2.2, 1.0, 0], mid.get_left() + LEFT * 0.1, color=GREY, buff=0, stroke_width=6)
        aR = DoubleArrow(mid.get_right() + RIGHT * 0.1, [2.5, 1.0, 0], color=GREY, buff=0, stroke_width=6)
        self.play(FadeIn(mid), GrowFromCenter(aL), GrowFromCenter(aR), run_time=1.0)
        self.at("settling near", 0.3)
        W, H, X0, Y = 10.0, 0.8, -5.0, -2.75
        p = ValueTracker(0.5)

        def seg_a():
            w = W * p.get_value()
            return Rectangle(width=w, height=H, stroke_width=0, fill_color=GREEN, fill_opacity=0.95).move_to(
                [X0 + w / 2, Y, 0])

        def seg_b():
            w = W * (1 - p.get_value())
            return Rectangle(width=w, height=H, stroke_width=0, fill_color=TEAL, fill_opacity=0.95).move_to(
                [X0 + W - w / 2, Y, 0])

        sa, sb = always_redraw(seg_a), always_redraw(seg_b)
        ta = always_redraw(lambda: M("α ~ 1/3", 30, BG, weight=BOLD).move_to([X0 + W * p.get_value() / 2, Y, 0]))
        tb = always_redraw(lambda: M("β ~ 2/3", 30, BG, weight=BOLD).move_to(
            [X0 + W * p.get_value() + W * (1 - p.get_value()) / 2, Y, 0]))
        self.play(FadeIn(sa), FadeIn(sb), FadeIn(ta), FadeIn(tb), run_time=0.6)
        self.play(p.animate.set_value(0.36), run_time=2.2, rate_func=smooth)
        self.finish()


class S04Bond(BP):
    def construct(self):
        N = 12
        gap = 0.46
        BS = 0.3
        lane_l, lane_r, y0 = -3.5, 3.5, 1.9

        def row_pos(x):
            return [np.array([x + (i - (N - 1) / 2) * gap, y0, 0]) for i in range(N)]

        L = [block(BS) for _ in range(N)]
        R = [block(BS) for _ in range(N)]
        for b, p in zip(L, row_pos(lane_l)):
            b.move_to(p)
        for b, p in zip(R, row_pos(lane_r)):
            b.move_to(p)
        eq = T("=", 44, GREY).move_to([0, y0, 0])
        same = T("identical glucose monomers", 30, BLUE).move_to([0, y0 + 0.9, 0])

        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in L + R], lag_ratio=0.04), FadeIn(eq), run_time=1.8)
        self.play(FadeIn(same), run_time=0.6)

        # alpha: link and coil
        self.at("Link them with", 0.3)
        la = [link(L[i], L[i + 1], GREEN) for i in range(N - 1)]
        alab = M("α-1,4", 32, GREEN).move_to([lane_l, y0 + 0.75, 0])
        self.play(FadeOut(same), LaggedStart(*[Create(x) for x in la], lag_ratio=0.1), FadeIn(alab), run_time=1.4)
        self.at("the chain coils", 0.5)
        # coil targets: a flat spiral (a chain wound on itself), blocks evenly spaced along it
        pos_list = []
        th = 0.3
        a_, b_ = 0.32, 0.13
        while len(pos_list) < N:
            r = a_ + b_ * th
            pt = np.array([r * math.cos(th), r * math.sin(th), 0])
            if not pos_list or np.linalg.norm(pt - pos_list[-1]) >= 0.62:
                pos_list.append(pt)
            th += 0.005
        pos_list = pos_list[::-1]   # chain winds inward
        mc = (np.max(pos_list, axis=0) + np.min(pos_list, axis=0)) / 2
        spiral = [np.array([lane_l, -0.55, 0]) + p - mc for p in pos_list]
        self.play(FadeOut(alab), *[b.animate.move_to(p) for b, p in zip(L, spiral)], run_time=2.4, rate_func=smooth)
        capl1 = T("starch · glycogen", 30, GREEN, weight=BOLD).move_to([lane_l, -2.75, 0])
        capl2 = T("compact, digestible storage", 26, GREEN).next_to(capl1, DOWN, buff=0.15)
        self.play(FadeIn(capl1, shift=UP * 0.1), FadeIn(capl2, shift=UP * 0.1), run_time=0.9)

        # beta: link, lie flat, stack, H-bond
        self.at("Link the very same", 0.4)
        lb = [link(R[i], R[i + 1], TEAL) for i in range(N - 1)]
        blab = M("β-1,4", 32, TEAL).move_to([lane_r, y0 + 0.75, 0])
        self.play(FadeOut(eq), LaggedStart(*[Create(x) for x in lb], lag_ratio=0.1), FadeIn(blab), run_time=1.4)
        self.at("the chains lie flat", 0.4)
        rows = [R]
        extra = []
        for k in (1, 2):
            rowk = [block(BS) for _ in range(N)]
            for b, p in zip(rowk, row_pos(lane_r)):
                b.move_to(p + DOWN * 1.05 * k)
            lk = [link(rowk[i], rowk[i + 1], TEAL) for i in range(N - 1)]
            extra.append(VGroup(*rowk, *lk))
            rows.append(rowk)
        self.play(FadeOut(blab), LaggedStart(*[FadeIn(e, shift=UP * 0.5) for e in extra], lag_ratio=0.4), run_time=1.6)
        self.at("hydrogen-bond", 0.4)
        hb = VGroup()
        for k in range(2):
            for i in range(0, N, 2):
                hb.add(DashedLine(rows[k][i].get_bottom(), rows[k + 1][i].get_top(), color=GREY, stroke_width=3,
                                  dash_length=0.08))
        hb_lab = T("hydrogen bonds between chains", 26, GREY).move_to([lane_r, -1.0, 0])
        self.play(Create(hb), FadeIn(hb_lab), run_time=1.2)
        capr1 = T("cellulose", 30, TEAL, weight=BOLD).move_to([lane_r, -2.75, 0])
        capr2 = T("rigid fibers, indigestible", 26, TEAL).next_to(capr1, DOWN, buff=0.15)
        self.play(FadeIn(capr1, shift=UP * 0.1), FadeIn(capr2, shift=UP * 0.1), run_time=0.9)

        # punchline
        self.at("One bond geometry", 0.3)
        allb = L + rows[0] + rows[1] + rows[2]
        self.play(*[Indicate(b, color=BLUE, scale_factor=1.25) for b in allb], run_time=1.6)
        self.at("The wood in your pencil", 0.2)
        self.play(FadeOut(capl1), FadeOut(capl2), FadeOut(capr1), FadeOut(capr2), FadeOut(hb_lab), run_time=0.5)
        wl1 = T("glucose in your blood", 28, GREEN, weight=BOLD).move_to([lane_l - 0.3, -2.75, 0])
        wl2 = T("wood in your pencil", 28, TEAL, weight=BOLD).move_to([lane_r + 0.3, -2.75, 0])
        mid = VGroup(block(0.42), T("same brick", 28, BLUE, weight=BOLD)).arrange(DOWN, buff=0.18).move_to([0, -2.5, 0])
        self.play(FadeIn(wl1, shift=UP * 0.1), FadeIn(wl2, shift=UP * 0.1), run_time=0.9)
        self.at("are the same brick", 0.3)
        self.play(FadeIn(mid, shift=UP * 0.1), run_time=0.7)
        self.at("laid a different way", 0.3)
        self.play(*[Indicate(b, color=BLUE, scale_factor=1.25) for b in allb + [mid[0]]], run_time=1.4)
        self.finish()


def glycogen_tree(center, scale=1.0):
    """Schematic glycogen particle: three chains from a core, each ending in two children, five tiers.
    Returns (segments VGroup by tier, tip points)."""
    lengths = [1.0, 0.85, 0.7, 0.58, 0.48]
    spreads = [None, 38, 32, 28, 24]
    tiers = [[] for _ in lengths]
    tips = []

    def grow(p, ang, depth):
        d = lengths[depth] * scale
        q = p + d * np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0])
        tiers[depth].append(Line(p, q, color=GREEN, stroke_width=4 - 0.5 * depth))
        if depth == len(lengths) - 1:
            tips.append((q, ang))
            return
        for s in (-1, 1):
            grow(q, ang + s * spreads[depth + 1], depth + 1)

    for a0 in (90, 210, 330):
        grow(center, a0, 0)
    return [VGroup(*t) for t in tiers], tips


class S05Glycogen(BP):
    def construct(self):
        # a. one branch every ~10 units
        n = 12
        sp = 0.75
        blocks = [block(0.5) for _ in range(n)]
        for i, b in enumerate(blocks):
            b.move_to([-4.2 + i * sp, -0.9, 0])
        main_links = [link(blocks[i], blocks[i + 1], GREEN) for i in range(n - 1)]
        br_dir = np.array([0.5, 0.86, 0])
        branch = [block(0.5) for _ in range(4)]
        for j, b in enumerate(branch):
            b.move_to(blocks[9].get_center() + br_dir * sp * (j + 1))
        br_links = [link(blocks[9] if j == 0 else branch[j - 1], branch[j], GREEN, width=7) for j in range(4)]
        l14 = VGroup(M("α-1,4", 32, GREEN), T("chain", 32, GREEN)).arrange(RIGHT, buff=0.15).move_to([-2.4, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in blocks], lag_ratio=0.1),
                  LaggedStart(*[Create(x) for x in main_links], lag_ratio=0.1), run_time=2.0)
        self.play(FadeIn(l14), run_time=0.6)
        self.at("an α-1,6 branch", 0.4)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b, scale=0.6), Create(x)) for b, x in zip(branch, br_links)],
                              lag_ratio=0.3), run_time=1.6)
        l16 = VGroup(M("α-1,6", 32, GREEN, weight=BOLD), T("branch", 32, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.15)
        l16.next_to(branch[-1], LEFT, buff=0.5)
        brace = Brace(VGroup(*blocks[:10]), DOWN, color=GREY, buff=0.1)
        bl = T("about every ten units", 30, GREY).next_to(brace, DOWN, buff=0.12)
        self.play(FadeIn(l16), GrowFromCenter(brace), FadeIn(bl), run_time=1.0)
        self.wait(self.until("Stack that up", 0.6))

        # b. stack up: tree + counters
        motif = VGroup(*blocks, *branch, l14, l16, brace, bl)
        for m in main_links + br_links:
            m.clear_updaters()
        motif_all = VGroup(motif, *main_links, *br_links)
        center = np.array([-3.0, 0.1, 0])
        tiers, tips = glycogen_tree(center, scale=0.8)
        self.play(FadeOut(motif_all), run_time=0.6)
        core = Circle(radius=0.14, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(center)
        self.play(FadeIn(core), run_time=0.3)
        for tr in tiers:
            self.play(Create(tr), run_time=0.55)
        tip_dots = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(q)
                            for q, _ in tips])
        tree_note = T("schematic", 24, GREY).move_to([-3.0, -3.45, 0])
        units, ends = ValueTracker(0), ValueTracker(0)
        u_num = always_redraw(lambda: M(f"{int(units.get_value()):,}", 60, BLUE).move_to([4.2, 1.9, 0]))
        u_lab = T("glucose units", 30, BLUE).move_to([4.2, 1.15, 0])
        e_num = always_redraw(lambda: M(f"{int(ends.get_value()):,}", 60, YELLOW).move_to([4.2, -0.2, 0]))
        e_lab = T("non-reducing ends", 30, YELLOW).move_to([4.2, -0.95, 0])
        self.at("a single liver glycogen", 0.2)
        self.add(u_num)
        self.play(FadeIn(u_lab), units.animate.set_value(55000), FadeIn(tree_note), run_time=2.0)
        self.at("about 2,100", 0.5)
        self.add(e_num)
        self.play(FadeIn(e_lab), ends.animate.set_value(2100), FadeIn(tip_dots, lag_ratio=0.02),
                  run_time=2.0)
        self.wait(self.until("Why does that matter", 0.4))

        # c. enzymes work at the ends
        self.at("Enzymes only pull", 0.3)
        enz_pts = [tips[i] for i in range(0, len(tips), 2)]
        enz = VGroup()
        for q, ang in enz_pts:
            d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0])
            e = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.26, stroke_color=PURPLE, stroke_width=2,
                                 fill_color=PURPLE, fill_opacity=0.9).move_to(q + d * 0.28)
            enz.add(e)
        enz_lab = T("enzyme", 30, PURPLE).move_to([4.2, -2.0, 0])
        self.play(FadeIn(enz[0], scale=1.5), FadeIn(enz_lab), run_time=0.8)
        self.at("so 2,100 ends", 0.3)
        self.play(LaggedStart(*[FadeIn(e, scale=1.5) for e in enz[1:]], lag_ratio=0.06), run_time=1.6)
        # glucose peels off
        peel = []
        for (q, ang), e in zip(enz_pts, enz):
            d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0])
            g = block(0.22).move_to(e.get_center() + d * 0.25)
            peel.append((g, d))
        self.add(*[g for g, _ in peel])
        many = T("thousands of enzymes\nat once", 30, PURPLE, line_spacing=0.8).move_to([4.2, -3.0, 0])
        self.play(FadeIn(many), *[g.animate.shift(d * 0.9).set_opacity(0) for g, d in peel], run_time=1.6)
        self.wait(self.until("Branching is parallel", 0.4))

        # d. parallel processing: bar race
        self.at("Branching is parallel", 0.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        title = T("glucose released while you sprint", 38, TEXT).move_to([0, 2.7, 0])
        lab1 = T("one end", 32, GREY).move_to([-4.6, 1.0, 0])
        lab2 = T("2,100 ends", 32, YELLOW).move_to([-4.4, -0.6, 0])
        x0, w, h = -2.6, 8.4, 0.8
        frame1 = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2).move_to([x0 + w / 2, 1.0, 0])
        frame2 = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2).move_to([x0 + w / 2, -0.6, 0])
        f1, f2 = ValueTracker(0), ValueTracker(0)
        bar1 = always_redraw(lambda: Rectangle(width=max(0.04, w * f1.get_value()), height=h, stroke_width=0,
                                               fill_color=GREEN, fill_opacity=0.9).move_to(
            [x0 + max(0.04, w * f1.get_value()) / 2, 1.0, 0]))
        bar2 = always_redraw(lambda: Rectangle(width=max(0.01, w * f2.get_value()), height=h, stroke_width=0,
                                               fill_color=GREEN, fill_opacity=0.9).move_to(
            [x0 + max(0.01, w * f2.get_value()) / 2, -0.6, 0]))
        note = T("same rate per end  →  2,100× the glucose", 26, GREY).move_to([0, -1.7, 0])
        tiny = M("1/2,100", 26, GREY).next_to(frame1.get_left(), RIGHT, buff=0.3)
        fast = T("parallel processing for energy", 40, GREEN, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(title), FadeIn(VGroup(lab1, lab2, frame1, frame2, bar1, bar2)), FadeIn(note), run_time=0.8)
        self.play(FadeIn(fast, shift=UP * 0.1), run_time=0.8)
        self.at("it's what lets you mobilize", 0.4)
        race = max(3.0, self.narration_s - self.elapsed() - 0.8)
        self.play(f1.animate.set_value(1 / 2100), f2.animate.set_value(1.0), FadeIn(tiny, run_time=1.0),
                  run_time=race, rate_func=linear)
        self.finish()


class S06End(EndCard):
    LINE = "Open the polymer sandbox: pick the bond, watch glucose change role."
