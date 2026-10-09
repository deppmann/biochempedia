"""Søren Sørensen: a scientist profile (Biochemistrypedia, water-weak-bonds lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size. The plots are schematic (labelled as such): no measured value is shown.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and the person: name/dates, the portrait frame
  YELLOW = the notation: pH, the logarithm, the highlighted line on the page, the pH axis
  GREEN  = hydrogen ions / free protons
  RED    = trouble: the columns of decimals, the bottleneck, leaky results, "no pH scale"
  BLUE   = enzymes: invertase, enzyme activity
  APPAR (orange) = measuring apparatus: electrode, indicator (TEAL is too close to BLUE)
  PLACE (lavender) = the brewery (place of work)
  GREY   = pages, axes, structure, de-emphasized things
No molecular structure is drawn: ions are plain dots, apparatus is chips, plots are schematic curves.
"""
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(__file__).resolve().parent
PORTRAIT = str(HERE / "sorensen_crop.png")      # figure cropped from public/scientists/soren-sorensen.png
CAPTION = "illustration · AI-generated"
NAME = "Søren Sørensen"
DATES = "1868–1939"
PLACE = "#B39DDB"       # places and institutions
PANEL_BG = "#161B26"
APPAR = "#F0A35E"      # measuring apparatus (electrode, indicator)

INSET_C = np.array([-4.6, 1.1, 0.0])
INSET_H = 3.4
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


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
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def xmark(center, color=RED, s=0.26, w=8):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])).set_color(color) \
        .set_stroke(width=w).move_to(center)


def scatter(n, center, w, h, seed, min_d=0.42):
    """n well-separated points inside a w x h box around center (deterministic)."""
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        p = np.array([rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2), 0.0])
        if all(np.linalg.norm(p - q) >= min_d for q in pts):
            pts.append(p)
    return [np.array(center) + p for p in pts]


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
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.4)
        self.play(
            ScaleInPlace(grp, 1.06, run_time=1.7, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.35),
                Write(name, run_time=0.65),
                FadeIn(dates, shift=UP * 0.1, run_time=0.4),
                GrowFromCenter(rule, run_time=0.3),
            ),
        )
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.55,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 a typographic fix
class S01Notation(ProfileScene):
    def construct(self):
        self.add_inset()

        # --- notation: pH
        ph = T("pH", 120, YELLOW, font=TITLE_FONT).move_to([PANEL_C, 1.2, 0])
        notation = T("notation", 34, GREY).next_to(ph, DOWN, buff=0.3)
        self.play(FadeIn(ph, scale=0.8), run_time=0.7)
        self.at("notation")
        self.play(FadeIn(notation, shift=UP * 0.1), run_time=0.5)
        fix = lab("a typographic fix", GREY, 30).move_to([PANEL_C, -1.3, 0])
        self.at("typographic")
        self.play(pop(fix), run_time=0.5)

        # --- measuring hydrogen ions
        self.at("Measuring", lead=0.7)
        self.play(FadeOut(ph), FadeOut(notation), FadeOut(fix), run_time=0.45)
        box = RoundedRectangle(corner_radius=0.15, width=1.7, height=1.7, stroke_color=GREEN, stroke_width=3,
                               fill_color=GREEN, fill_opacity=0.06).move_to([-0.7, 1.2, 0])
        ions = VGroup(*[Dot(p, radius=0.11, color=GREEN) for p in scatter(8, box.get_center(), 1.2, 1.2, 3, 0.4)])
        ions_lab = T("hydrogen ions", 26, GREEN).next_to(box, DOWN, buff=0.2)
        self.at("Measuring")
        self.play(FadeIn(box), LaggedStart(*[FadeIn(d, scale=0.4) for d in ions], lag_ratio=0.08),
                  FadeIn(ions_lab), run_time=0.9)

        # --- columns of decimals, written out
        zeros = [6, 8, 7, 9, 7]
        rows = VGroup(*[M("0." + "0" * z + "…", 26, RED) for z in zeros])
        for i, r in enumerate(rows):
            r.move_to([1.55 + r.width / 2, 2.35 - 0.5 * i, 0])
        feed = Arrow([0.2, 1.35, 0], [0.85, 1.35, 0], color=GREY, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.35)
        self.at("columns of decimals")
        self.play(GrowArrow(feed), LaggedStart(*[Write(r) for r in rows], lag_ratio=0.45), run_time=2.0)

        # --- recompared
        cmp_arrows = VGroup(*[
            DoubleArrow([1.3, rows[i].get_center()[1] - 0.04, 0], [1.3, rows[i + 1].get_center()[1] + 0.04, 0],
                        color=TEXT, stroke_width=4, buff=0, tip_length=0.14)
            for i in range(len(rows) - 1)])
        self.at("compared")
        self.play(LaggedStart(*[Create(a) for a in cmp_arrows], lag_ratio=0.25), run_time=1.0)

        # --- the bookkeeping becomes the bottleneck
        book = T("bookkeeping", 28, RED).move_to([5.15, 2.75, 0])
        lw = VGroup(Line([4.2, 2.35, 0], [4.9, 1.4, 0]), Line([4.9, 1.4, 0], [4.9, 0.3, 0]))
        rw = VGroup(Line([6.2, 2.35, 0], [5.5, 1.4, 0]), Line([5.5, 1.4, 0], [5.5, 0.3, 0]))
        funnel = VGroup(lw, rw).set_color(RED).set_stroke(width=5)
        jam = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.55, height=0.22, stroke_color=RED, stroke_width=2,
                                        fill_color=RED, fill_opacity=0.35).move_to(p)
                       for p in ([4.75, 2.1, 0], [5.65, 2.05, 0], [5.2, 1.75, 0], [5.2, 1.4, 0], [5.2, 1.0, 0])])
        self.at("bookkeeping")
        self.play(FadeIn(book, shift=UP * 0.1), Create(funnel), run_time=0.8)
        bneck = T("bottleneck", 28, RED).move_to([5.2, -0.1, 0])
        self.at("bottleneck")
        self.play(LaggedStart(*[FadeIn(j, shift=DOWN * 0.15) for j in jam], lag_ratio=0.15), FadeIn(bneck), run_time=0.8)
        self.play(Flash([5.2, 1.4, 0], color=RED, flash_radius=0.5, line_length=0.18), run_time=0.5)

        # --- a brewery chemist compresses the mess into a logarithm
        chem = lab("brewery chemist", PLACE, 28).move_to([-0.5, -1.8, 0])
        self.at("brewery chemist")
        self.play(pop(chem), run_time=0.5)
        logc = lab("logarithm", YELLOW, 34).move_to([3.8, -1.8, 0])
        arrow = Arrow(chem.get_right() + RIGHT * 0.1, logc.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        self.at("compressed")
        self.play(FadeTransform(rows, logc), GrowArrow(arrow),
                  FadeOut(box), FadeOut(ions), FadeOut(ions_lab), FadeOut(feed), FadeOut(cmp_arrows),
                  FadeOut(funnel), FadeOut(jam), FadeOut(book), FadeOut(bneck), run_time=1.4)

        # --- he did not think he had discovered anything
        disc = lab("a discovery", GREY, 34).move_to([PANEL_C, 0.7, 0])
        self.at("He did not think")
        self.play(pop(disc), run_time=0.5)
        st = Line(disc.get_left() + RIGHT * 0.05, disc.get_right() - RIGHT * 0.05, color=RED, stroke_width=6)
        self.at("discovered")
        self.play(Create(st), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s02 160 pages, one line
def page(cx, cy, w=1.6, h=2.0, bars=6, color=GREY, fill=PANEL_BG):
    rect = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    lines = VGroup(*[Line([-w / 2 + 0.55, h / 2 - 0.3 - 0.27 * i, 0],
                          [w / 2 - 0.2 - (0.35 if i % 3 == 2 else 0.0), h / 2 - 0.3 - 0.27 * i, 0],
                          color=GREY, stroke_width=3).set_opacity(0.55) for i in range(bars)])
    g = VGroup(rect, lines)
    g.move_to([cx, cy, 0])
    return g


class S02Pages(ProfileScene):
    STACK = np.array([-0.3, 0.95, 0.0])

    def construct(self):
        self.add_inset()
        n = 7
        pages = [page(self.STACK[0] + (i - 3) * 0.4, self.STACK[1]) for i in range(n)]
        for i, p in enumerate(pages):
            p.set_z_index(i)

        # --- more than 160 pages
        v = ValueTracker(0)

        def counter():
            c = int(round(v.get_value()))
            m = M(f"{c}" + ("+" if c >= 160 else ""), 52, TEXT, weight=BOLD)
            m.move_to([self.STACK[0] - 0.4, 2.85, 0])
            return m

        cnt = always_redraw(counter)
        pages_lab = T("pages", 36, GREY).move_to([self.STACK[0] + 1.65, 2.85, 0])
        self.at("more than")
        self.add(cnt)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.25) for p in pages], lag_ratio=0.12),
                  v.animate.set_value(160), run_time=1.5, rate_func=smooth)
        self.play(FadeIn(pages_lab), run_time=0.3)
        cnt.clear_updaters()

        # --- electrode by electrode, indicator by indicator
        e1 = lab("electrode", APPAR, 24).move_to([3.0, 1.85, 0])
        e2 = lab("electrode", APPAR, 24).move_to([5.4, 1.85, 0])
        i1 = lab("indicator", APPAR, 24).move_to([3.0, 0.5, 0])
        i2 = lab("indicator", APPAR, 24).move_to([5.4, 0.5, 0])
        by1 = T("by", 24, GREY).move_to([4.2, 1.85, 0])
        by2 = T("by", 24, GREY).move_to([4.2, 0.5, 0])
        self.at("electrode")
        self.play(pop(e1), run_time=0.4)
        self.at("by electrode")
        self.play(FadeIn(by1), pop(e2), run_time=0.4)
        self.at("indicator")
        self.play(pop(i1), run_time=0.4)
        self.at("by indicator")
        self.play(FadeIn(by2), pop(i2), run_time=0.4)

        # --- the choice that would outlast him appears exactly once
        hero = pages[3]
        self.at("the choice", lead=0.3)
        self.play(*[FadeOut(m) for m in (e1, e2, i1, i2, by1, by2)], run_time=0.4)
        mark = Line(hero[0].get_left() + RIGHT * 0.2 + UP * 0.3, hero[0].get_right() + LEFT * 0.55 + UP * 0.3,
                    color=YELLOW, stroke_width=6).set_z_index(10)
        choice = lab("the choice", YELLOW, 30).move_to([4.3, 2.12, 0])
        link = Arrow(choice.get_left() + LEFT * 0.1, [self.STACK[0] + 0.88, 2.12, 0], color=YELLOW, stroke_width=4,
                     buff=0, max_tip_length_to_length_ratio=0.3)
        hero.set_z_index(9)
        self.play(pop(choice), GrowArrow(link), hero.animate.shift(UP * 0.3), run_time=0.7)
        mark.shift(UP * 0.3)
        self.play(hero[0].animate.set_stroke(color=YELLOW, width=4), Create(mark), run_time=0.5)
        once = M("× 1", 64, YELLOW, weight=BOLD).move_to([4.3, 0.75, 0])
        once_l = T("exactly once", 30, YELLOW).next_to(once, DOWN, buff=0.2)
        self.at("exactly once")
        self.play(FadeIn(once, scale=1.3), FadeIn(once_l, shift=UP * 0.1), run_time=0.6)
        plain = lab("no emphasis", GREY, 28).move_to([4.3, -1.2, 0])
        self.at("without emphasis")
        self.play(pop(plain), run_time=0.5)

        # --- the quote: the page opens up
        card_rect = RoundedRectangle(corner_radius=0.12, width=7.4, height=3.3, stroke_color=YELLOW, stroke_width=3,
                                     fill_color=PANEL_BG, fill_opacity=1).move_to([PANEL_C, 0.3, 0]).set_z_index(9)
        others = [p for p in pages if p is not hero]
        self.at("For the number", lead=0.9)
        hero_rect_home = hero[0].copy()
        self.play(*[FadeOut(m) for m in (*others, cnt, pages_lab, choice, link, once, once_l, plain, mark)],
                  hero[1].animate.set_opacity(0), Transform(hero[0], card_rect), run_time=0.8)
        qs = []
        specs = [("“For the number representing the", "For"), ("exponent of this power, I have", "exponent"),
                 ("chosen the symbol", "chosen")]
        left_x = PANEL_C - 3.4
        for k, (txt, cue) in enumerate(specs):
            t = T(txt, 32, TEXT, font=TITLE_FONT)
            t.move_to([left_x + t.width / 2, 1.2 - 0.85 * k, 0]).set_z_index(11)
            qs.append(t)
        self.at("For", lead=0.1)
        self.play(FadeIn(qs[0], shift=RIGHT * 0.15), run_time=0.5)
        self.at("exponent")
        self.play(FadeIn(qs[1], shift=RIGHT * 0.15), run_time=0.5)
        self.at("chosen")
        self.play(FadeIn(qs[2], shift=RIGHT * 0.15), run_time=0.5)
        ph_q = T("pH.”", 32, YELLOW, font=TITLE_FONT).set_z_index(11)
        ph_q.next_to(qs[2], RIGHT, buff=0.16).align_to(qs[2], DOWN)
        self.at("pH", lead=0.15)
        self.play(FadeIn(ph_q, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Indicate(ph_q, color=YELLOW, scale_factor=1.25), run_time=0.5)

        # --- two letters, buried
        big = T("pH", 78, YELLOW, font=TITLE_FONT).move_to([PANEL_C - 0.7, 2.75, 0])
        two = T("two letters", 32, GREY).next_to(big, RIGHT, buff=0.35).align_to(big, DOWN)
        self.at("Two")
        self.play(FadeIn(big, scale=0.6), FadeIn(two, shift=LEFT * 0.1), run_time=0.6)
        buried = T("buried", 36, GREY).move_to([self.STACK[0], -0.55, 0])
        self.at("buried", lead=0.9)
        self.play(*[FadeOut(m) for m in (*qs, ph_q, big, two)], Transform(hero[0], hero_rect_home),
                  *[FadeIn(p) for p in others], hero[1].animate.set_opacity(0.55), run_time=0.7)
        hero[0].set_stroke(color=GREY)
        self.at("buried", lead=0.15)
        self.play(FadeIn(buried, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s03 free protons, not total acid
class S03Protons(ProfileScene):
    def construct(self):
        self.add_inset()
        C = np.array([0.4, 0.5, 0.0])
        box = RoundedRectangle(corner_radius=0.18, width=4.2, height=2.6, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.05).move_to(C)
        pts = scatter(23, C, 3.6, 2.0, 11, 0.5)
        free = VGroup(*[Dot(p, radius=0.13, color=GREEN) for p in pts[:6]])
        rest = VGroup(*[Dot(p, radius=0.11, color=GREY).set_opacity(0.85) for p in pts[6:]])
        self.at("measurements")
        self.play(FadeIn(box), LaggedStart(*[FadeIn(d, scale=0.4) for d in [*rest, *free]], lag_ratio=0.04),
                  run_time=1.2)

        self.at("underline")
        self.play(*[Indicate(d, color=TEXT, scale_factor=2.2) for d in free], run_time=0.9)

        enz = lab("enzymes", BLUE, 30).move_to([5.15, 0.5, 0])
        self.at("enzymes")
        self.play(pop(enz), run_time=0.5)

        ignore = DashedLine([4.05, 0.5, 0], [2.75, 0.5, 0], color=GREY, stroke_width=4, dash_length=0.12)
        ignore.add_tip(tip_length=0.2)
        cross = xmark([3.4, 0.5, 0], RED, 0.22, 7)
        self.at("do not care")
        self.play(Create(ignore), FadeIn(cross, scale=1.5), run_time=0.6)
        brace = Brace(box, DOWN, color=GREY, buff=0.15)
        total = T("total acid", 30, GREY).next_to(brace, DOWN, buff=0.15)
        self.at("how much acid")
        self.play(GrowFromCenter(brace), FadeIn(total, shift=UP * 0.1), run_time=0.7)

        self.at("only")
        take = Arrow([4.05, 0.5, 0], [2.75, 0.5, 0], color=GREEN, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3)
        self.play(FadeOut(ignore), FadeOut(cross), GrowArrow(take),
                  rest.animate.set_opacity(0.22), *[d.animate.scale(1.4) for d in free], run_time=0.7)
        fl = T("free protons", 34, GREEN).move_to([C[0], 2.55, 0])
        ul = Line(fl.get_corner(DL) + DOWN * 0.1, fl.get_corner(DR) + DOWN * 0.1, color=GREEN, stroke_width=4)
        self.at("free protons")
        self.play(FadeIn(fl, shift=DOWN * 0.1), run_time=0.4)
        self.play(Create(ul), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s04 the peak
def pH_to_x(p, x0, L):
    return x0 + (p - 2.0) / 6.0 * L


PK1, PK2 = 4.9, 5.1   # illustrative pKa pair (not shown on screen)
_AMAX = 1.0 / (1.0 + 10 ** (PK1 - 5.0) + 10 ** (5.0 - PK2))


def activity(p):
    """Normalized pH-activity bell from the diprotic ionization model: v ∝ 1 / (1 + 10^(pK1-pH) + 10^(pH-pK2))."""
    return float(1.0 / (1.0 + 10 ** (PK1 - p) + 10 ** (p - PK2)) / _AMAX)


class S04Peak(ProfileScene):
    def construct(self):
        self.add_inset()

        # --- same invertase reaction that had defeated Victor Henri
        inv = lab("invertase reaction", BLUE, 26).move_to([-0.1, 2.5, 0])
        self.at("same")
        self.play(pop(inv), run_time=0.5)
        henri = lab("Victor Henri", TEXT, 26).move_to([5.0, 2.5, 0])
        defeat = Arrow(inv.get_right() + RIGHT * 0.1, henri.get_left() + LEFT * 0.1, color=RED, stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.2)
        dlab = T("defeated", 24, RED).next_to(defeat, UP, buff=0.12)
        self.at("defeated")
        self.play(GrowArrow(defeat), FadeIn(dlab), run_time=0.5)
        self.at("Victor Henri")
        self.play(pop(henri), run_time=0.5)

        # --- earlier results were leaky
        res = lab("earlier results", RED, 26, fill=0.0).move_to([5.0, 1.0, 0])
        res_box = DashedVMobject(res[0], num_dashes=34).set_color(RED)
        res_txt = res[1]
        self.at("earlier results")
        self.play(Create(res_box), FadeIn(res_txt), run_time=0.6)
        self.at("leaky")
        drips = VGroup(*[Dot([4.4 + 0.6 * k, 0.45, 0], radius=0.07, color=RED) for k in range(3)])
        self.add(drips)
        self.play(*[d.animate.shift(DOWN * 0.9).set_opacity(0.0) for d in drips], run_time=0.8, rate_func=linear)
        drips = VGroup(*[Dot([4.4 + 0.6 * k, 0.45, 0], radius=0.07, color=RED) for k in range(3)])
        self.add(drips)

        # --- no pH scale yet existed
        ruler = VGroup(DashedLine([-1.9, 0.75, 0], [1.9, 0.75, 0], color=GREY, stroke_width=3, dash_length=0.12),
                       *[Line([-1.9 + 0.76 * k, 0.75, 0], [-1.9 + 0.76 * k, 0.95, 0], color=GREY, stroke_width=3)
                         for k in range(6)]).set_opacity(0.55)
        ruler_l = T("pH scale", 28, YELLOW).move_to([0.0, 1.4, 0])
        self.at("because no")
        self.play(Create(ruler), FadeIn(ruler_l), run_time=0.6)
        self.at("yet existed", lead=0.4)
        x2 = xmark([0.0, 0.8, 0], RED, 0.3, 8)
        self.play(FadeIn(x2, scale=1.5), run_time=0.35)

        # --- the acidity that nothing fixed
        acid = lab("acidity", GREEN, 28).move_to([-0.3, -1.0, 0])
        wob = DoubleArrow([1.45, -1.55, 0], [1.45, -0.45, 0], color=GREEN, stroke_width=4, buff=0, tip_length=0.2)
        self.at("fix the acidity", lead=0.3)
        self.play(pop(acid), FadeIn(wob), run_time=0.4)
        self.play(wob.animate.shift(UP * 0.2), run_time=0.22, rate_func=smooth)
        self.play(wob.animate.shift(DOWN * 0.4), run_time=0.3, rate_func=smooth)
        self.play(wob.animate.shift(UP * 0.2), run_time=0.22, rate_func=smooth)

        # --- plotted on the new logarithmic axis
        self.at("Plotted", lead=0.55)
        self.play(*[FadeOut(m) for m in (inv, henri, defeat, dlab, res_box, res_txt, drips, ruler, ruler_l, x2,
                                         acid, wob)], run_time=0.45)
        x0, L = -1.0, 7.0
        y0, H = -2.3, 4.0
        xaxis = Arrow([x0 - 0.2, y0, 0], [x0 + L + 0.3, y0, 0], color=GREY, stroke_width=3, buff=0,
                      max_tip_length_to_length_ratio=0.03)
        yaxis = Arrow([x0 - 0.2, y0, 0], [x0 - 0.2, y0 + H + 0.45, 0], color=GREY, stroke_width=3, buff=0,
                      max_tip_length_to_length_ratio=0.04)
        ylab = T("enzyme activity", 28, BLUE).rotate(PI / 2).move_to([x0 - 0.75, y0 + H / 2 + 0.2, 0])
        schem = T("schematic", 24, GREY).move_to([x0 + L - 0.55, y0 - 0.5, 0])
        self.at("Plotted", lead=0.15)
        self.play(Create(xaxis), Create(yaxis), FadeIn(ylab), FadeIn(schem), run_time=0.8)
        xl = T("pH · logarithmic axis", 28, YELLOW).move_to([x0 + L / 2, y0 - 0.5, 0])
        self.at("new logarithmic")
        self.play(Write(xl), run_time=0.7)

        ps = [2.0 + 0.375 * k for k in range(17)]
        new_pts = [np.array([pH_to_x(p, x0, L), y0 + 0.12 + activity(p) * H, 0]) for p in ps]
        # old units: the raw hydrogen-ion concentration, 10^-pH, on a linear axis (pH 2 -> 1 ... pH 8 -> 1e-6)
        old_pts = [np.array([x0 + 0.1 + (L - 0.2) * 10.0 ** (-(p - 2.0)), y0 + 0.12 + activity(p) * H, 0]) for p in ps]
        dots = VGroup(*[Dot(p, radius=0.11, color=BLUE) for p in new_pts])
        self.at("the data")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.05), run_time=1.0)

        def curve_fn(t):
            return np.array([pH_to_x(t, x0, L), y0 + 0.12 + activity(t) * H, 0])

        curve = ParametricFunction(curve_fn, t_range=[2.0, 8.0, 0.02], color=BLUE, stroke_width=5)
        self.at("sharp activity")
        self.play(Create(curve), run_time=0.6)
        apex = curve_fn(5.0)
        peak = T("sharp peak", 30, BLUE).next_to(apex, RIGHT, buff=0.5).shift(UP * 0.2)
        self.at("peak")
        self.play(FadeIn(peak, shift=LEFT * 0.1), Flash(apex, color=YELLOW, flash_radius=0.4, line_length=0.15),
                  run_time=0.4)

        # --- the old units had hidden it
        xl_old = T("old units", 28, GREY).move_to(xl)
        self.at("old units", lead=0.5)
        self.play(FadeOut(curve), FadeOut(peak), FadeOut(xl), FadeIn(xl_old),
                  *[d.animate.move_to(p) for d, p in zip(dots, old_pts)], run_time=1.0, rate_func=smooth)
        pile = VGroup(*[d for d, p in zip(dots, ps) if p >= 3.1])
        hid = SurroundingRectangle(pile, color=RED, buff=0.2, stroke_width=4)
        hid_l = T("hidden", 32, RED, weight=BOLD).next_to(hid, RIGHT, buff=0.3)
        self.at("hidden", lead=0.1)
        self.play(Create(hid), FadeIn(hid_l, shift=LEFT * 0.1), run_time=0.5)
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.4) for d in pile], run_time=0.8)
        self.wait(0.5)      # let the payoff land before the silent quote
        self.finish()


# ----------------------------------------------------------------------------- s05 the quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“It might be said that the hydrogen", "ion concentration is the factor which,",
                 "above all others, determines the", "course of enzymatic processes.”"]
        q = VGroup(*[T(l, 36, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— " + NAME, 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.75)
        self.wait(0.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Invented the pH scale (1909): free protons, not total acid, govern enzymes."

    def construct(self):
        a = T("Invented the pH scale (1909):", size=42, font=TITLE_FONT)
        b = T("free protons, not total acid, govern enzymes.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
