"""Otto Meyerhof: a scientist profile (Biochemistrypedia, glycolysis lesson).

Narration is the lesson entry's `story`, verbatim (7 sentences, 5 spoken scenes). Everything on screen comes
from that entry (name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is on
screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Meyerhof himself, the portrait frame, recognition (Nobel, "oxygen debt", the notes and library)
  YELLOW = years / dates, the stimulus pulses
  RED    = illness, exhaustion, entropy, what he turned down (food), what was ruled out
  AMBER  = lactic acid
  GREEN  = glycogen
  ORANGE = the part that burned for energy
  PINK   = muscle (incl. the frog legs)
  BLUE   = oxygen / air
  TEAL   = ATP, the new molecule
  PLACE (lavender) = places and institutions (France, Marseille, Pennsylvania, the laboratory)
  TEXT (white) = other people and things he read or wrote (poetry, thesis, Lohmann)
  GREY   = labels, axes, the abandoned theory
No molecular structure is drawn: lactic acid and glycogen are piles of plain blocks, ATP is a chip.
"""
import math
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "otto-meyerhof.png")
CAPTION = "illustration · AI-generated"
NAME = "Otto Meyerhof"
DATES = "1884–1951"
PLACE = "#B39DDB"
AMBER = "#E0A458"
ORANGE = "#F28C38"
PINK = "#E58AA0"

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # panel spans x -2.4 .. 6.3


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T(NAME, size=34, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def at_(mob, x, y):
    return mob.move_to([x, y, 0])


def arrow(a, b, color=GREY, w=4, tip=0.3):
    return Arrow(a, b, color=color, stroke_width=w, buff=0, max_tip_length_to_length_ratio=tip)


def cross_out(mob, color=RED, pad=0.1, w=5):
    """A single strike-through across the middle of a chip (the text stays readable)."""
    y = mob.get_center()[1]
    return Line([mob.get_left()[0] - pad, y, 0], [mob.get_right()[0] + pad, y, 0], color=color, stroke_width=w)


def dim_chip(chip_, on=True):
    """Animations that dim (or restore) a chip without touching its fill alpha convention."""
    box, txt = chip_[0], chip_[1]
    if on:
        return [box.animate.set_stroke(opacity=0.45).set_fill(opacity=0.06), txt.animate.set_opacity(0.45)]
    return [box.animate.set_stroke(opacity=1.0).set_fill(opacity=0.16), txt.animate.set_opacity(1.0)]


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=2.0, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.4),
                Write(name, run_time=0.7),
                FadeIn(dates, shift=UP * 0.1, run_time=0.4),
                GrowFromCenter(rule, run_time=0.3),
            ),
        )
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.7,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 the unlikely road
class S01Road(ProfileScene):
    def construct(self):
        self.add_inset()
        ry = 2.55
        x0, x1 = -1.9, 3.3
        road = ParametricFunction(
            lambda s: np.array([x0 + (x1 - x0) * s, ry + 0.28 * math.sin(s * 3 * math.pi), 0]),
            t_range=[0, 1, 0.01], color=GREY, stroke_width=5)
        start = Dot([x0, ry, 0], radius=0.14, color=GOLD)
        who = T("Meyerhof", 28, GOLD).next_to(start, UP, buff=0.18).align_to(start, LEFT).shift(LEFT * 0.12)
        bio = lab("biochemistry", TEAL, 30).move_to([4.75, ry, 0])
        self.play(FadeIn(start, scale=2), FadeIn(who, shift=UP * 0.1), run_time=0.4)
        self.at("reached biochemistry")
        self.play(pop(bio), run_time=0.4)
        self.play(Create(road), run_time=1.5, rate_func=smooth)
        unl = T("an unlikely road", 26, GREY).move_to([(x0 + x1) / 2, ry - 0.7, 0])
        self.at("unlikely road")
        self.play(FadeIn(unl, shift=UP * 0.1), run_time=0.4)

        bed = lab("bedridden for months", RED, 28).move_to([-0.1, 0.95, 0])
        self.at("bedridden for months")
        self.play(pop(bed), run_time=0.45)
        kid = lab("kidney ailment", RED, 28).move_to([4.35, 0.95, 0])
        a1 = arrow([bed.get_right()[0] + 0.1, 0.95, 0], [kid.get_left()[0] - 0.1, 0.95, 0], RED, 4)
        self.at("kidney ailment")
        self.play(GrowArrow(a1), pop(kid), run_time=0.5)
        tw = T("in his twenties", 26, YELLOW).move_to([4.35, 0.25, 0])
        self.at("his 20s")
        self.play(pop(tw), run_time=0.4)

        poetry = lab("read poetry", TEXT, 28).move_to([-0.7, -0.85, 0])
        self.at("read poetry")
        self.play(pop(poetry), run_time=0.45)
        thesis = lab("doctoral thesis", TEXT, 28).move_to([3.5, -0.85, 0])
        self.at("doctoral thesis")
        self.play(pop(thesis), run_time=0.45)
        psy = T("psychology of mental illness", 26, TEXT).move_to([3.5, -1.65, 0])
        self.at("psychology of mental illness")
        self.play(pop(psy), run_time=0.5)

        life = lab("life itself", GOLD, 28).move_to([-0.9, -2.7, 0])
        law = lab(["the language of", "physical law"], GOLD, 28).move_to([3.9, -2.65, 0])
        wr = arrow([life.get_right()[0] + 0.1, -2.7, 0], [law.get_left()[0] - 0.1, -2.7, 0], GOLD, 5)
        wl = T("written in", 24, GREY).next_to(wr, UP, buff=0.12)
        self.at("life itself")
        self.play(pop(life), run_time=0.45)
        self.at("language of physical law", lead=0.55)
        self.play(GrowArrow(wr), FadeIn(wl), pop(law), run_time=0.7)
        self.play(Indicate(bio, color=GOLD, scale_factor=1.08), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 1913 habilitation
class S02Energetics(ProfileScene):
    def construct(self):
        self.add_inset()
        yr = M("1913", 44, YELLOW).move_to([-0.9, 2.75, 0])
        self.at("1913")
        self.play(Write(yr), run_time=0.5)
        hab = lab("habilitation", GREY, 28).move_to([2.2, 2.75, 0])
        self.at("habilitation")
        self.play(pop(hab), run_time=0.45)
        t1 = T("“The Energetics of Living Cells,”", 38, GOLD, font=TITLE_FONT).move_to([PANEL_C, 1.55, 0])
        fit(t1, max_w=8.4)
        self.at("The Energetics of Living Cells")
        self.play(Write(t1), run_time=2.0)

        bx, by = 1.0, -0.55
        body = lab(["a body", "thermodynamic system"], TEAL, 28, pad=0.3).move_to([bx, by, 0])
        self.at("a body")
        self.play(pop(body), run_time=0.5)
        self.at("thermodynamic system")
        self.play(Indicate(body, color=TEAL, scale_factor=1.05), run_time=0.6)

        bw, bh = body.width, body.height
        ins = [
            arrow([bx, by + bh / 2 + 0.95, 0], [bx, by + bh / 2 + 0.12, 0], RED, 6, 0.4),
            arrow([bx, by - bh / 2 - 0.95, 0], [bx, by - bh / 2 - 0.12, 0], RED, 6, 0.4),
            arrow([bx - bw / 2 - 1.0, by, 0], [bx - bw / 2 - 0.12, by, 0], RED, 6, 0.4),
            arrow([bx + bw / 2 + 1.0, by, 0], [bx + bw / 2 + 0.12, by, 0], RED, 6, 0.4),
        ]
        self.at("holding itself")
        self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.2), run_time=1.0)
        ent = T("entropy", 30, RED).next_to(ins[3], RIGHT, buff=0.15)
        self.at("against entropy")
        self.play(pop(ent), body[0].animate.set_stroke(width=6), run_time=0.5)

        proved = T("proved it", 32, GOLD, font=TITLE_FONT).move_to([4.7, -1.55, 0])
        self.at("proved it")
        self.play(pop(proved), run_time=0.4)
        frog = lab("frog legs", PINK, 30).move_to([4.7, -2.55, 0])
        self.at("frog legs")
        self.play(pop(frog), run_time=0.45)
        self.play(Indicate(frog, color=PINK, scale_factor=1.08), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 oxygen debt
class S03Debt(ProfileScene):
    def construct(self):
        self.add_inset()
        # ---- apparatus: detached muscle, stimulus pulses
        mx, my = -0.6, 1.9
        muscle = lab("detached muscle", PINK, 30).move_to([mx, my, 0])
        top = my + muscle.height / 2

        def bolt(x):
            pts = [[x, top + 0.75, 0], [x - 0.12, top + 0.5, 0], [x + 0.12, top + 0.38, 0], [x, top + 0.1, 0]]
            return VMobject(color=YELLOW, stroke_width=5).set_points_as_corners(pts)
        bolts = VGroup(bolt(mx - 0.7), bolt(mx + 0.7))
        self.play(pop(muscle), FadeIn(bolts), run_time=0.5)
        self.play(Indicate(muscle, color=YELLOW, scale_factor=1.05), run_time=0.5)

        exh = lab("exhaustion", RED, 28).move_to([-1.1, 0.7, 0])
        self.at("exhaustion")
        self.play(pop(exh), *dim_chip(muscle), FadeOut(bolts), run_time=0.5)
        oxy = lab("oxygen", BLUE, 28).move_to([1.7, 0.7, 0])
        xo = cross_out(oxy)
        self.at("without oxygen")
        self.play(pop(oxy), Create(xo), run_time=0.6)

        # ---- the lactic acid pile (plain blocks)
        px, py0, bs = 4.4, 1.55, 0.4
        blocks = VGroup(*[Square(bs, stroke_width=0, fill_color=AMBER, fill_opacity=0.9) for _ in range(8)])
        for i, b in enumerate(blocks):
            r, c = divmod(i, 4)
            b.move_to([px + (c - 1.5) * (bs + 0.08), py0 + r * (bs + 0.08), 0])
        pile_lab = T("lactic acid", 28, AMBER).move_to([px, py0 - 0.7, 0])
        a_la = arrow([mx + muscle.width / 2 + 0.1, my, 0], [px - 1.15, my - 0.1, 0], AMBER, 4)
        self.at("lactic acid")
        self.play(GrowArrow(a_la), pop(pile_lab), run_time=0.5)
        self.at("pile up")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in blocks], lag_ratio=0.2), run_time=1.3)

        # ---- air readmitted
        air = lab("air readmitted", BLUE, 28).move_to([-0.3, 0.45, 0])
        a_air = arrow([-0.3, 0.45 + 0.45, 0], [-0.3, my - muscle.height / 2 - 0.08, 0], BLUE, 5)
        self.at("readmitted air")
        self.play(FadeOut(exh), FadeOut(oxy), FadeOut(xo), pop(air), GrowArrow(a_air),
                  *dim_chip(muscle, False), run_time=0.7)

        # ---- a quarter burns, the rest rebuilt
        energy_lab = T("about a quarter", 28, ORANGE).move_to([-0.8, -0.45, 0])
        e_pos = [[-1.0, -1.45, 0], [-0.5, -1.45, 0]]
        self.at("only about a quarter")
        self.play(pop(energy_lab), *[blocks[i].animate.move_to(e_pos[i]).set_fill(ORANGE, 0.9) for i in (0, 1)],
                  run_time=0.9)
        energy = lab("burned for energy", ORANGE, 28).move_to([-0.75, -2.5, 0])
        self.at("burned for energy")
        self.play(pop(energy), run_time=0.5)
        rest_lab = T("the rest", 28, GREEN).move_to([4.4, -0.45, 0])
        g_pos = [[3.75 + 0.48 * (i % 3), -1.25 - 0.48 * (i // 3), 0] for i in range(6)]
        self.at("the rest")
        self.play(pop(rest_lab), FadeOut(a_la), FadeOut(pile_lab),
                  LaggedStart(*[blocks[2 + i].animate.move_to(g_pos[i]) for i in range(6)], lag_ratio=0.06),
                  run_time=0.8)
        gly = lab("glycogen", GREEN, 28).move_to([4.4, -2.5, 0])
        self.at("rebuilt into glycogen")
        self.play(pop(gly), *[blocks[2 + i].animate.set_fill(GREEN, 0.9) for i in range(6)], run_time=0.7)

        # ---- phase 2: the recovery loop
        phase1 = VGroup(muscle, blocks, air, a_air, energy_lab, energy, rest_lab, gly)
        self.at("That recovery loop", lead=0.45)
        self.play(FadeOut(phase1), run_time=0.4)
        la = lab("lactic acid", AMBER, 30).move_to([-0.6, 2.0, 0])
        gl = lab("glycogen", GREEN, 30).move_to([4.2, 2.0, 0])
        a_up = arrow([la.get_right()[0] + 0.08, 2.25, 0], [gl.get_left()[0] - 0.08, 2.25, 0], BLUE, 5)
        a_dn = arrow([gl.get_left()[0] - 0.08, 1.75, 0], [la.get_right()[0] + 0.08, 1.75, 0], RED, 5)
        l_up = T("with air", 24, BLUE).move_to([(la.get_right()[0] + gl.get_left()[0]) / 2, 2.85, 0])
        l_dn = T("without oxygen", 24, RED).move_to([(la.get_right()[0] + gl.get_left()[0]) / 2, 1.2, 0])
        self.play(pop(la), pop(gl), run_time=0.4)
        self.play(GrowArrow(a_up), FadeIn(l_up), GrowArrow(a_dn), FadeIn(l_dn), run_time=0.8)

        mus = lab("the muscle", PINK, 30).move_to([-0.7, -0.05, 0])
        self.at("the muscle repaying")
        self.play(pop(mus), run_time=0.4)
        rep = arrow([0.75, -0.05, 0], [1.95, -0.05, 0], GOLD, 5)
        rl = T("repaying", 24, GREY).move_to([1.35, -0.5, 0])
        debt = T("“oxygen debt”", 44, GOLD, font=TITLE_FONT).move_to([4.3, -0.05, 0])
        self.play(GrowArrow(rep), FadeIn(rl), run_time=0.4)
        self.at("oxygen debt")
        self.play(Write(debt), run_time=0.9)

        medal = VGroup(Circle(radius=0.55, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.2),
                       T("Nobel", 22, GOLD, weight=BOLD))
        share = T("a share of", 30, TEXT)
        y22 = M("1922", 44, YELLOW)
        prize = T("Nobel Prize", 34, GOLD, font=TITLE_FONT)
        row = VGroup(medal, share, y22, prize).arrange(RIGHT, buff=0.3).move_to([PANEL_C, -2.15, 0])
        fit(row, max_w=8.5)
        self.at("won him")
        self.play(GrowFromCenter(medal), run_time=0.35)
        self.at("a share")
        self.play(pop(share), run_time=0.4)
        self.at("1922")
        self.play(Write(y22), run_time=0.5)
        self.at("Nobel Prize")
        self.play(pop(prize), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s04 ATP
class S04Atp(ProfileScene):
    def construct(self):
        self.add_inset()
        theory = lab("his theory", GOLD, 30).move_to([-0.7, 2.6, 0])
        elegant = T("elegant", 30, GOLD, font=TITLE_FONT).move_to([2.2, 2.6, 0])
        self.at("The theory was elegant", lead=0.0)
        self.play(pop(theory), run_time=0.5)
        self.at("elegant")
        self.play(FadeIn(elegant, shift=RIGHT * 0.15), Indicate(theory, color=GOLD, scale_factor=1.06), run_time=0.6)
        self.at("did not cling", lead=0.1)
        ghost = lab("his theory", GREY, 30).move_to(theory)
        ghost_d = VGroup(DashedVMobject(ghost[0], num_dashes=34, dashed_ratio=0.55).set_color(GREY), ghost[1])
        self.play(FadeOut(elegant), FadeOut(theory), FadeIn(ghost_d), run_time=0.6)
        self.play(ghost_d.animate.set_opacity(0.45), run_time=0.4)

        lohm = lab("Karl Lohmann", TEXT, 30).move_to([-0.7, 1.05, 0])
        self.at("his assistant")
        asst = T("his assistant", 24, GREY).next_to(lohm, DOWN, buff=0.12)
        self.play(pop(lohm), FadeIn(asst), run_time=0.5)
        atp = lab("ATP", TEAL, 34).move_to([2.9, 1.05, 0])
        a1 = arrow([lohm.get_right()[0] + 0.1, 1.05, 0], [atp.get_left()[0] - 0.1, 1.05, 0], TEAL, 5)
        iso = T("isolated", 24, GREY).next_to(a1, UP, buff=0.1)
        self.at("isolated ATP", lead=0.3)
        self.play(GrowArrow(a1), FadeIn(iso), pop(atp), run_time=0.7)
        y29 = M("1929", 40, YELLOW).move_to([5.3, 1.05, 0])
        self.at("1929")
        self.play(Write(y29), run_time=0.5)

        mus = lab("muscle contracts", PINK, 30).move_to([-0.4, -0.65, 0])
        self.at("muscle was soon shown")
        self.play(pop(mus), run_time=0.5)
        la = lab("lactic acid", AMBER, 30).move_to([3.7, -0.65, 0])
        xla = cross_out(la)
        self.at("no lactic acid")
        self.play(pop(la), Create(xla), run_time=0.6)
        atall = T("at all", 28, RED).next_to(la, RIGHT, buff=0.25)
        self.at("at all")
        self.play(FadeIn(atall), run_time=0.3)

        lab_c = lab("whole laboratory", PLACE, 30).move_to([-0.2, -2.3, 0])
        atp2 = lab("ATP", TEAL, 34).move_to([4.3, -2.3, 0])
        a2 = arrow([lab_c.get_right()[0] + 0.1, -2.3, 0], [atp2.get_left()[0] - 0.1, -2.3, 0], PLACE, 5)
        ret = T("retooled", 26, PLACE).next_to(a2, UP, buff=0.1)
        self.at("retooled", lead=0.3)
        self.play(FadeOut(ghost_d), pop(lab_c), run_time=0.5)
        self.play(GrowArrow(a2), FadeIn(ret), run_time=0.6)
        self.at("around the new molecule", lead=0.0)
        new = T("the new molecule", 24, TEAL).next_to(atp2, DOWN, buff=0.15)
        self.play(pop(atp2), FadeIn(new), run_time=0.45)
        self.play(Indicate(atp2, color=TEAL, scale_factor=1.12), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s05 Marseille
class S05France(ProfileScene):
    def construct(self):
        self.add_inset()
        fr = lab("France", PLACE, 30).move_to([-0.6, 2.6, 0])
        y40 = M("1940", 44, YELLOW).move_to([2.6, 2.6, 0])
        marseille = lab("Marseille hotel lobby", PLACE, 30).move_to([1.4, 0.9, 0])
        flee = arrow([fr.get_bottom()[0] - 0.1, fr.get_bottom()[1] - 0.1, 0],
                     [marseille.get_top()[0] - 1.0, marseille.get_top()[1] + 0.1, 0], GREY, 5)
        fl = T("fleeing", 26, GREY).next_to(flee, LEFT, buff=0.15)
        self.play(pop(fr), run_time=0.45)
        self.play(GrowArrow(flee), FadeIn(fl), run_time=0.5)
        self.at("1940")
        self.play(Write(y40), run_time=0.5)
        self.at("found in a Marseille", lead=0.15)
        self.play(pop(marseille), run_time=0.5)

        ask = T("asked what he needed", 28, GREY).move_to([1.4, 0.1, 0])
        self.at("asked what he needed")
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)

        food = lab("food", RED, 30).move_to([-1.1, -1.1, 0])
        xf = cross_out(food)
        self.at("not for food")
        self.play(pop(food), Create(xf), run_time=0.6)
        notes = lab("his notes", GOLD, 30).move_to([1.6, -1.1, 0])
        self.at("his notes")
        self.play(pop(notes), run_time=0.45)
        lib = lab("his library", GOLD, 30).move_to([4.5, -1.1, 0])
        self.at("his library")
        self.play(pop(lib), run_time=0.45)

        penn = lab("Pennsylvania", PLACE, 34).move_to([3.0, -2.75, 0])
        mid = (notes.get_center()[0] + lib.get_center()[0]) / 2
        join = VGroup(Line([notes.get_center()[0], notes.get_bottom()[1] - 0.08, 0], [notes.get_center()[0], -1.85, 0], color=GOLD, stroke_width=4),
                      Line([lib.get_center()[0], lib.get_bottom()[1] - 0.08, 0], [lib.get_center()[0], -1.85, 0], color=GOLD, stroke_width=4),
                      Line([notes.get_center()[0], -1.85, 0], [lib.get_center()[0], -1.85, 0], color=GOLD, stroke_width=4))
        down = arrow([mid, -1.85, 0], [mid, penn.get_top()[1] + 0.08, 0], GOLD, 5, 0.5)
        penn.move_to([mid, -2.75, 0])
        self.at("carried both")
        self.play(Create(join), GrowArrow(down), run_time=0.6)
        self.at("Pennsylvania", lead=0.35)
        self.play(pop(penn), run_time=0.5)
        self.play(Indicate(penn, color=PLACE, scale_factor=1.08), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s06 quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        q = T("“The Energetics of Living Cells”", 44, TEXT, font=TITLE_FONT)
        fit(q, max_w=8.4)
        who = T("Otto Meyerhof, 1913 habilitation", 30, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.2, 0])
        q.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.5)
        self.play(q.animate.set_opacity(1.0), run_time=1.0)
        self.wait(1.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Supplied glycolysis's energetics with frog muscle; abandoned his theory for ATP."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 2.0, 0])
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.15)
        a = T("Supplied glycolysis’s energetics with frog muscle;", 40, font=TITLE_FONT)
        b = T("abandoned his theory for ATP.", 40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Embden–Meyerhof–Parnas profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
