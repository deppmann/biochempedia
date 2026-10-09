"""Hermann Kolbe: a scientist profile (Biochemistrypedia, vitalism lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story; the entry has no quotes, so there is no quote scene). The portrait is an
AI-generated engraving-style illustration from The Molecule Hunters; it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Kolbe and what he did: name/dates, "Kolbe's synthesis", the door, "decisive", the closed loophole
  YELLOW = the year (1845)
  RED    = the objection and the escape route: Wöhler's critics, the "?" over the lifeless-to-organic arrow, strikes
  GREEN  = living / organic things: organic sources, organic molecule, "alive", a cell, a seed
  TEAL   = the lifeless chain: charcoal, molten sulfur, carbon disulfide
  AMBER  = the galvanic battery
  LAV    = acetic acid and its acetyl group (BLUE is too close to TEAL to read as a different concept)
  GREY   = labels, his motive, de-emphasized things
No molecular structure is drawn: everything is labelled chips, arrows, a battery circuit symbol and plain dots.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/mission-control/work/explainers/2026-10-09-biochempedia/bio-vitalism-hermann-kolbe/kolbe_crop.png"
CROP_AR = 837 / 944.0
CAPTION = "illustration · AI-generated"
NAME = "Hermann Kolbe"
DATES = "1818–1884"
AMBER = "#E0A458"   # the battery
LAV = "#B39DDB"     # acetic acid / acetyl group

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.4
CX = 1.95           # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame, h=INSET_H):
    nm = T(NAME, size=34, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - h / 2 - 1.3, 0])
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


def at_pos(mob, x, y):
    return mob.move_to([x, y, 0])


def strike(mob, color=RED, extra=0.12, width=5):
    return Line(mob.get_left() + LEFT * extra, mob.get_right() + RIGHT * extra, color=color, stroke_width=width)


def arrow(a, b, color=GREY, w=5, tip=0.3, **kw):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=tip, **kw)


def battery_symbol(cx, cy, color=AMBER):
    """A circuit-symbol battery drawn vertically: stacked plates, long/short alternating. Not a molecule."""
    plates = VGroup()
    for i, wd in enumerate([1.3, 0.65, 1.3, 0.65]):
        plates.add(Line([-wd / 2, 0, 0], [wd / 2, 0, 0], color=color, stroke_width=7 if i % 2 else 4))
    plates.arrange(DOWN, buff=0.17).move_to([cx, cy, 0])
    return plates


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
            ScaleInPlace(grp, 1.07, run_time=3.5, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.5),
                Write(name, run_time=0.9),
                FadeIn(dates, shift=UP * 0.1, run_time=0.5),
                GrowFromCenter(rule, run_time=0.4),
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


# ----------------------------------------------------------------------------- s01 the loophole
class S01Loophole(ProfileScene):
    def construct(self):
        self.add_inset()
        # top row: the critics and their escape route
        self.at("critics")
        crit = lab("Wöhler's critics", RED, 30)
        at_pos(crit, -0.1, 2.85)
        self.play(pop(crit), run_time=0.45)
        self.at("escape route")
        esc = T("an escape route", 30, RED)
        at_pos(esc, 4.6, 2.85)
        route = arrow([crit[0].get_right()[0] + 0.12, 2.85, 0], [esc.get_left()[0] - 0.12, 2.85, 0], RED, 5)
        self.play(GrowArrow(route), pop(esc), run_time=0.5)

        # the provenance row: cyanate  --traced back-->  organic sources
        self.at("ammonium cyanate")
        cy = lab("ammonium cyanate", TEXT, 28)
        at_pos(cy, 4.6, 1.3)
        self.play(pop(cy), run_time=0.45)
        self.at("traced back")
        org = lab("organic sources", GREEN, 28)
        at_pos(org, -0.1, 1.3)
        ar = arrow(cy[0].get_left() + LEFT * 0.08, org[0].get_right() + RIGHT * 0.08, RED, 5)
        tb = T("traced back", 24, RED).next_to(ar, DOWN, buff=0.36)
        self.play(GrowArrow(ar), FadeIn(tb), run_time=0.6)
        self.at("organic sources", nth=0)
        self.play(pop(org), run_time=0.45)

        # perhaps no organic molecule was made from the lifeless world
        self.at("organic molecule")
        om = lab("organic molecule", GREEN, 28)
        at_pos(om, 4.45, -0.55)
        self.play(pop(om), run_time=0.5)
        self.at("the lifeless world", lead=0.35)
        lw = lab("the lifeless world", TEAL, 28)
        at_pos(lw, -0.15, -0.55)
        mid = arrow(lw[0].get_right() + RIGHT * 0.08, om[0].get_left() + LEFT * 0.08, GREY, 4)
        dashed = DashedVMobject(mid, num_dashes=14, dashed_ratio=0.6).set_color(GREY)
        q = T("?", 44, RED, weight=BOLD).next_to(mid, UP, buff=0.12)
        self.play(pop(lw), run_time=0.45)
        self.play(FadeIn(dashed), FadeIn(q), run_time=0.5)

        # 1845: Kolbe slams the door on the escape route
        self.at("1845", lead=0.4)
        yr = M("1845", 44, YELLOW)
        kol = lab("Kolbe's synthesis", GOLD, 30)
        row = VGroup(yr, kol).arrange(RIGHT, buff=0.4).move_to([CX, -2.2, 0])
        self.play(pop(row), run_time=0.6)
        self.at("slammed", lead=0.45)
        door = Rectangle(width=0.4, height=1.15, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1.0)
        dx = (crit[0].get_right()[0] + esc.get_left()[0]) / 2
        door.move_to([dx, 4.7, 0]).set_z_index(5)
        self.play(door.animate.move_to([dx, 2.85, 0]), run_time=0.45, rate_func=rush_into)
        self.play(Flash(door, color=GOLD, flash_radius=0.75, line_length=0.25, num_lines=10, run_time=0.45),
                  esc.animate.set_opacity(0.4), run_time=0.45)
        self.finish()


# ----------------------------------------------------------------------------- s02 the synthesis
class S02Synthesis(ProfileScene):
    def construct(self):
        self.add_inset()
        self.at("carbon disulfide", lead=0.35)
        cs = lab("carbon disulfide", TEAL, 30)
        at_pos(cs, CX, 0.55)
        self.play(pop(cs), run_time=0.5)

        self.at("charcoal")
        ch = lab("charcoal", TEAL, 28)
        at_pos(ch, 0.1, 2.7)
        a1 = arrow(ch[0].get_bottom() + DOWN * 0.06, cs[0].get_top() + UP * 0.06 + LEFT * 0.7, GREY, 4)
        self.play(pop(ch), GrowArrow(a1), run_time=0.6)
        self.at("molten sulfur")
        su = lab("molten sulfur", TEAL, 28)
        at_pos(su, 3.95, 2.7)
        a2 = arrow(su[0].get_bottom() + DOWN * 0.06, cs[0].get_top() + UP * 0.06 + RIGHT * 0.7, GREY, 4)
        self.play(pop(su), GrowArrow(a2), run_time=0.6)

        self.at("nothing alive", lead=0.3)
        nothing = T("nothing", 30, GREY)
        alive = T("alive", 30, GREEN)
        inchain = T("anywhere in the chain", 30, GREY)
        line = VGroup(nothing, alive, inchain).arrange(RIGHT, buff=0.22).move_to([CX, -1.0, 0])
        self.play(FadeIn(nothing), FadeIn(alive), run_time=0.4)
        st_alive = strike(alive, RED, 0.08, 4)
        self.play(Create(st_alive), run_time=0.3)
        self.at("in the chain", lead=0.3)
        chain = VGroup(ch, su, cs, a1, a2)
        box = DashedVMobject(SurroundingRectangle(chain, color=TEAL, buff=0.25, corner_radius=0.2, stroke_width=3),
                             num_dashes=60, dashed_ratio=0.6)
        self.play(FadeIn(inchain), Create(box), run_time=0.7)

        # finished the job: not a cell or a seed, a battery
        self.at("finished the job", lead=0.35)
        self.play(FadeOut(Group(ch, su, a1, a2, box, line, st_alive)), cs.animate.move_to([CX, 2.75, 0]), run_time=0.6)
        self.at("a cell", lead=0.3)
        cell = lab("a cell", GREEN, 28)
        at_pos(cell, 0.5, 1.2)
        self.play(pop(cell), run_time=0.35)
        sc = strike(cell, RED, 0.1, 5)
        self.play(Create(sc), run_time=0.25)
        self.at("a seed", lead=0.3)
        seed = lab("a seed", GREEN, 28)
        at_pos(seed, 3.5, 1.2)
        self.play(pop(seed), run_time=0.35)
        ss = strike(seed, RED, 0.1, 5)
        self.play(Create(ss), run_time=0.25)

        self.at("an ordinary galvanic", lead=0.45)
        down1 = arrow([CX, cs[0].get_bottom()[1] - 0.05, 0], [CX, 0.7, 0], AMBER, 4)
        bat = battery_symbol(CX, 0.25)
        bl = T("galvanic battery", 28, AMBER).next_to(bat, RIGHT, buff=0.55)
        self.play(FadeOut(Group(cell, sc, seed, ss)), run_time=0.3)
        self.play(GrowArrow(down1), Create(bat), run_time=0.7)
        self.at("battery", lead=0.3)
        self.play(FadeIn(bl, shift=LEFT * 0.15), run_time=0.45)

        self.at("leaving pure", lead=0.3)
        down2 = arrow([CX, bat.get_bottom()[1] - 0.1, 0], [CX, -1.35, 0], AMBER, 4)
        aa = lab("pure acetic acid", LAV, 32)
        at_pos(aa, CX, -1.95)
        self.play(GrowArrow(down2), run_time=0.4)
        self.play(pop(aa), run_time=0.5)
        self.at("behind", lead=0.4)
        self.play(Indicate(aa, color=LAV, scale_factor=1.06), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s03 motive vs effect
class S03Effect(ProfileScene):
    def construct(self):
        self.add_inset()
        self.at("motive", lead=0.5)
        mo = lab("his own motive", GREY, 30)
        at_pos(mo, CX, 2.85)
        self.play(pop(mo), run_time=0.45)
        self.at("proving a theory", lead=0.4)
        th = T("proving a theory of how molecules are built", 26, GREY)
        at_pos(th, CX, 2.0)
        self.play(FadeIn(th, shift=UP * 0.1), run_time=0.5)

        self.at("effect", lead=0.3)
        ef = T("the effect:", 34, GREY)
        dec = T("decisive", 56, GOLD, font=TITLE_FONT)
        eff = VGroup(ef, dec).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        at_pos(eff, CX, 0.6)
        self.play(Group(mo, th).animate.set_opacity(0.45), FadeIn(ef, shift=UP * 0.1), run_time=0.4)
        self.at("decisive", lead=0.25)
        ul = Line(dec.get_corner(DL) + DOWN * 0.1, dec.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.play(FadeIn(dec, shift=UP * 0.1), GrowFromEdge(ul, LEFT), run_time=0.6)

        self.at("No organic source", lead=0.35)
        crit = lab("Wöhler's critics", RED, 28)
        at_pos(crit, -0.1, -1.6)
        src = lab("organic source", GREEN, 28)
        at_pos(src, 4.45, -1.6)
        pt = arrow(crit[0].get_right() + RIGHT * 0.08, src[0].get_left() + LEFT * 0.08, RED, 5)
        self.play(pop(crit), pop(src), run_time=0.5)
        self.play(GrowArrow(pt), run_time=0.4)
        self.at("remained", lead=0.2)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=src[0].width, height=src[0].height,
                                                stroke_color=GREEN, stroke_width=2.5).move_to(src[0]),
                               num_dashes=36, dashed_ratio=0.5).set_color(GREEN)
        cross = strike(src[1], RED, 0.12, 4)   # struck through, still legible: no organic source remained
        self.play(src[0].animate.set_stroke(opacity=0).set_fill(opacity=0), src[1].animate.set_opacity(0.7),
                  FadeIn(ghost), run_time=0.4)
        self.play(Create(cross), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s04 the acetyl group
class S04Acetyl(ProfileScene):
    def construct(self):
        self.add_inset()
        hub_c = np.array([CX, 0.25, 0])
        aa = lab("acetic acid", LAV, 30)
        at_pos(aa, hub_c[0], hub_c[1])
        self.add(aa)
        self.at("acetyl group", lead=0.35)
        hub = lab(["acetyl group", "two carbons"], LAV, 30)
        at_pos(hub, hub_c[0], hub_c[1])
        backing = RoundedRectangle(corner_radius=0.14, width=hub[0].width, height=hub[0].height,
                                   stroke_width=0, fill_color=BG, fill_opacity=1).move_to(hub[0]).set_z_index(2)
        hub.set_z_index(3)
        self.play(FadeOut(aa, scale=0.9), FadeIn(backing), FadeIn(hub, scale=0.9), run_time=0.6)

        self.at("now", lead=0.35)
        rx, ry = 3.3, 2.05
        nodes, spokes = [], []
        for k in range(8):
            ang = math.radians(22.5 + 45 * k)
            p = np.array([hub_c[0] + rx * math.cos(ang), hub_c[1] + ry * math.sin(ang), 0])
            nodes.append(Dot(p, radius=0.17, color=GREY))
            spokes.append(Line(hub_c, p, color=GREY, stroke_width=2.5).set_opacity(0.7))
        for s in spokes:
            s.set_z_index(1)
        gold = T("the most-trafficked fragment", 32, GOLD, font=TITLE_FONT).move_to([CX, 3.2, 0])
        self.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=0.04),
                  LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.04), run_time=0.5)
        self.at("most trafficked", lead=0.25)
        self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.3)
        # traffic: dots flowing in and out along the spokes
        movers = []
        anims = []
        for k, s in enumerate(spokes):
            d = Dot(radius=0.12, color=LAV).set_z_index(1.5)
            near = s.get_start() + (s.get_end() - s.get_start()) * 0.2   # slides under the hub chip
            if k % 2 == 0:
                d.move_to(s.get_end()); anims.append(MoveAlongPath(d, Line(s.get_end(), near)))
            else:
                d.move_to(near); anims.append(MoveAlongPath(d, Line(near, s.get_end())))
            movers.append(d)
        self.add(*movers)
        self.play(AnimationGroup(*anims, lag_ratio=0.08), run_time=1.0, rate_func=linear)
        self.at("all of metabolism", lead=0.3)
        ring = DashedVMobject(RoundedRectangle(corner_radius=0.35, width=8.1, height=5.0, stroke_color=GREY,
                                               stroke_width=3).move_to([CX, 0.25, 0]), num_dashes=90, dashed_ratio=0.6)
        met = T("all of metabolism", 28, GREY).move_to([CX, -2.95, 0])
        self.play(Create(ring), FadeIn(met, shift=UP * 0.1), FadeOut(Group(*movers)), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 recap (silent)
class S05Recap(ProfileScene):
    def construct(self):
        self.add_inset()
        X = 0.85
        items = [lab("charcoal + molten sulfur", TEAL, 26), lab("carbon disulfide", TEAL, 26),
                 lab("galvanic battery", AMBER, 26), lab("pure acetic acid", LAV, 26),
                 lab("its acetyl group", LAV, 26)]
        ys = [3.0, 1.6, 0.2, -1.2, -2.6]
        for it, y in zip(items, ys):
            at_pos(it, X, y)
        arrows = [arrow([X, ys[i] - 0.42, 0], [X, ys[i + 1] + 0.42, 0], GREY, 4, tip=0.5) for i in range(3)]
        # the acetyl group is PART of acetic acid, not a further product: a dashed tie, not an arrow
        arrows.append(DashedLine([X, ys[3] - 0.42, 0], [X, ys[4] + 0.42, 0], color=LAV, stroke_width=4,
                                 dash_length=0.08))
        for i, it in enumerate(items):
            grow = ([GrowArrow(arrows[i - 1])] if i < 4 else [Create(arrows[i - 1])]) if i else []
            self.play(pop(it), *grow, run_time=0.55)
            self.wait(0.15)
        brace = Brace(VGroup(items[0], items[1]), RIGHT, color=TEAL, buff=0.15)
        nl = VGroup(T("nothing alive", 26, TEAL), T("in the chain", 26, TEAL)).arrange(DOWN, buff=0.08)
        nl.next_to(brace, RIGHT, buff=0.2)
        self.play(GrowFromCenter(brace), FadeIn(nl, shift=LEFT * 0.1), run_time=0.7)
        done = T("the loophole, closed", 30, GOLD, font=TITLE_FONT).move_to([4.45, -0.95, 0])
        fit(done, max_w=4.4)
        self.play(FadeIn(done, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Built acetic acid from charcoal, sulfur, and a battery, closing vitalism's loophole."

    def construct(self):
        img, frame = portrait_pair(2.5)
        grp = Group(img, frame).move_to([0, 1.95, 0])
        cap = caption_under(frame)
        a = T("Built acetic acid from charcoal, sulfur, and a battery,", size=38, font=TITLE_FONT)
        b = T("closing vitalism's loophole.", size=38, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2)
        fit(line, max_w=11.8)
        line.move_to([0, -0.7, 0])
        sub = T("biochemistrypedia.com", size=24, color=TEAL).move_to([0, -1.75, 0])
        src = T("Source: The Molecule Hunters, Part I · Hermann Kolbe profile", size=22, color=GREY).move_to([0, -2.55, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
