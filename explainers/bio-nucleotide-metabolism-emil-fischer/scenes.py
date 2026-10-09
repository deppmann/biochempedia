"""Emil Fischer: a scientist profile (Biochemistrypedia, nucleotide-metabolism lesson).

Narration is the lesson entry's `story`, verbatim (three sentences = three spoken scenes). Everything on
screen comes from that entry (name, dates, contribution, story, quote). The portrait is an AI-generated
engraving-style illustration from The Molecule Hunters (public/scientists/emil-fischer.png, cropped to the
figure); it is captioned "illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and Fischer himself: his name, dates, the 1898 / 1902 markers, the Nobel medal
  BLUE   = shape (the lock-and-key idea)
  TEAL   = the purines: the class, purine itself, the ~130 derivatives, caffeine, uric acid
  PINK   = the genetic code: "genetic alphabet", the bases read as its letters, heredity
  GREEN  = sugars; a key that fits
  YELLOW = the count (~130)
  LOCK   = pale slate: the lock
  RED    = rejection (the key that does not fit)
  ORANGE / VIOLET = energy / signaling (hub scene only)
  GREY   = axes, neutral keys, de-emphasized labels
No molecular structure is drawn: derivatives are plain tiles, the lock and keys are schematic blocks.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

from pathlib import Path
import os

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "fischer_crop.png")
CAPTION = "illustration · AI-generated"
NAME = "Emil Fischer"
DATES = "1852–1919"
LOCK = "#CFD6E4"         # the lock: pale slate, distinct from the grey keys
ORANGE = "#F28C4B"       # energy (hub scene)
PINK = "#E88AB0"         # the genetic code: alphabet, bases, heredity
VIOLET = "#B39DDB"       # signaling (hub scene)

INSET_C = np.array([-4.6, 1.2, 0.0])
INSET_H = 3.0
PANEL_C = 1.95


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


def dashed_lab(lines, color, size):
    c = lab(lines, color, size, fill=0.0)
    return VGroup(DashedVMobject(c[0], num_dashes=36).set_color(color), c[1])


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


def cross(center, color=RED, r=0.22, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color) \
        .set_stroke(width=w).move_to(center)


# lock / key geometry (schematic, shared by s03 and the quote scene)
CAV, DEPTH, WALL, BASE = 1.6, 1.125, 0.9, 0.45
KEY_W, KEY_H = 1.46, 0.95


def lock_shape(cx=0.0, color=LOCK):
    hw = CAV / 2 + WALL
    pts = [(-hw, -DEPTH - BASE), (hw, -DEPTH - BASE), (hw, 0), (CAV / 2, 0), (CAV / 2, -DEPTH),
           (-CAV / 2, -DEPTH), (-CAV / 2, 0), (-hw, 0)]
    p = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.22)
    p.set_stroke(opacity=1)
    return p.shift(RIGHT * cx + UP * 0.0)      # rim at y=0 relative; caller shifts to place


def key_a(color=GREY):
    return Rectangle(width=KEY_W, height=KEY_H, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)


def key_b(color=GREY):
    pts = [(-1.1, KEY_H / 2), (1.1, KEY_H / 2), (0.3, -KEY_H / 2), (-0.3, -KEY_H / 2)]
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.5)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.1)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.6)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=2.6, rate_func=linear),
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


# ----------------------------------------------------------------------------- s01 the purines
class S01Purines(ProfileScene):
    COLS, ROWS, PITCH = 13, 10, 0.3
    GX, GY = -2.0, 1.2          # centre of the top-left tile

    def tile_pos(self, r, c):
        return np.array([self.GX + self.PITCH * c, self.GY - self.PITCH * r, 0.0])

    def construct(self):
        self.add_inset()
        ay = 2.15
        axis = Arrow([-2.2, ay, 0], [3.05, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.05)
        time_lab = T("time", 24, GREY).move_to([2.55, ay - 0.35, 0])
        alph = dashed_lab(["genetic alphabet", "understood"], PINK, 24).move_to([4.7, ay, 0])

        self.play(Create(axis), run_time=0.4)
        self.at("genetic alphabet")
        self.play(pop(alph), FadeIn(time_lab), run_time=0.5)

        # Fischer on the timeline, charting the purines
        fx = -1.4
        fdot = Dot([fx, ay, 0], radius=0.12, color=GOLD)
        flab = T("Fischer", 30, GOLD, weight=BOLD).move_to([fx, ay + 0.5, 0])
        self.at("Fisher had already charted")
        self.play(FadeIn(fdot, scale=2), FadeIn(flab, shift=UP * 0.1), run_time=0.5)

        pur = lab("purines", TEAL, 30).move_to([-1.0, 0.8, 0])
        a1 = Arrow([fx, ay - 0.15, 0], [fx, pur.get_top()[1] + 0.05, 0], color=GOLD, stroke_width=4, buff=0.05,
                   max_tip_length_to_length_ratio=0.3)
        charted = T("charted", 24, GREY).next_to(a1, RIGHT, buff=0.15)
        self.at("charted")
        self.play(GrowArrow(a1), FadeIn(charted), run_time=0.45)
        self.at("the purines")
        self.play(pop(pur), run_time=0.5)

        named = T("named by Fischer", 26, GOLD).next_to(pur, DOWN, buff=0.4)
        self.at("gave the class its name")
        self.play(FadeIn(named, shift=UP * 0.1), Indicate(pur, color=GOLD, scale_factor=1.08), run_time=0.7)

        synth = lab(["purine itself,", "synthesized"], TEAL, 28).move_to([1.45, 0.8, 0])
        self.at("synthesized purine itself")
        self.play(pop(synth), run_time=0.5)

        dx = 1.45
        ddot = Dot([dx, ay, 0], radius=0.12, color=GOLD)
        dlab = T("1898", 36, GOLD, weight=BOLD).move_to([dx, ay + 0.5, 0])
        link = DashedLine([dx, ay - 0.12, 0], [dx, synth.get_top()[1] + 0.05, 0], color=GOLD, stroke_width=3,
                          dash_length=0.1)
        self.at("1898")
        self.play(FadeIn(ddot, scale=2), FadeIn(dlab, shift=UP * 0.1), Create(link), run_time=0.6)

        # ~130 derivatives: a grid of tiles filling in
        row2 = VGroup(pur, a1, charted, named, synth, link)
        self.at("and prepared")
        self.play(FadeOut(row2), run_time=0.4)

        tiles = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                t = RoundedRectangle(corner_radius=0.04, width=0.24, height=0.24, stroke_color=TEAL, stroke_width=2,
                                     fill_color=TEAL, fill_opacity=0.28).move_to(self.tile_pos(r, c))
                tiles.append(t)
        n = ValueTracker(0)

        def counter():
            v = int(round(n.get_value()))
            num = M(str(v), 44, YELLOW, weight=BOLD)
            word = T("derivatives", 30, GREY)
            g = VGroup(num, word).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
            return g.move_to([self.GX + 1.9, -2.5, 0])

        cnt = always_redraw(counter)
        self.add(cnt)
        self.at("on the order of")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.012),
                  n.animate.set_value(130), run_time=1.7, rate_func=linear)
        cnt.clear_updaters()
        final = VGroup(M("~130", 44, YELLOW, weight=BOLD), T("derivatives", 30, GREY)) \
            .arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to(cnt)
        self.play(FadeOut(cnt), FadeIn(final), run_time=0.01)

        # caffeine, uric acid, the bases
        def hi(r, c, color=TEAL):
            t = tiles[r * self.COLS + c]
            return t, t.animate.set_fill(color, 0.95).set_stroke(TEXT, 3)

        def side(lines, color, y, size=24):
            ch = lab(lines, color, size)
            ch.move_to([3.0 + ch.width / 2, y, 0])
            return ch

        specs = [(1, 12, ["caffeine"], TEAL, 1.0), (4, 12, ["uric acid", "of gout"], TEAL, -0.25),
                 (7, 12, ["bases later read as", "letters of the code"], PINK, -1.85)]
        chips, arrows = [], []
        for (r, c, lines, color, y) in specs:
            ch = side(lines, color, y)
            tp = self.tile_pos(r, c)
            ar = Arrow(ch.get_left() + LEFT * 0.05, tp + RIGHT * 0.2, color=color, stroke_width=4, buff=0.04,
                       max_tip_length_to_length_ratio=0.15)
            chips.append(ch)
            arrows.append(ar)

        def reveal(i):
            r, c, _, color, _ = specs[i]
            t, anim = hi(r, c, color)
            self.play(anim, pop(chips[i]), GrowArrow(arrows[i]), run_time=0.6)

        self.at("derivatives—caffeine", lead=-1.15)   # "caffeine" starts ~13.9 s, after the dash pause
        reveal(0)
        self.at("uric acid of gout")
        reveal(1)
        self.at("the bases later read")
        reveal(2)
        # the code's alphabet, understood later: the dashed chip fills in
        solid = lab(["genetic alphabet", "understood"], PINK, 24).move_to(alph)
        self.at("letters of the code")
        self.play(FadeOut(alph[0]), FadeIn(solid[0]), run_time=0.4)
        self.play(Indicate(VGroup(solid[0], alph[1]), color=PINK, scale_factor=1.06), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 the Nobel Prize
class S02Nobel(ProfileScene):
    def construct(self):
        self.add_inset()
        pur = lab("purines", TEAL, 32).move_to([-0.9, 1.5, 0])
        sug = lab("sugars", GREEN, 32).move_to([-0.9, -0.3, 0])
        self.play(pop(pur), run_time=0.5)
        self.at("his sugars")
        self.play(pop(sug), run_time=0.5)

        mc = np.array([3.7, 0.7, 0.0])
        medal = Circle(radius=0.95, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.18).move_to(mc)
        ring = Circle(radius=0.78, stroke_color=GOLD, stroke_width=2).move_to(mc).set_stroke(opacity=0.6)
        yr = M("1902", 40, GOLD, weight=BOLD).move_to(mc)
        a1 = Arrow(pur.get_right() + RIGHT * 0.1, mc + np.array([-1.05, 0.35, 0]), color=TEAL, stroke_width=4, buff=0,
                   max_tip_length_to_length_ratio=0.18)
        a2 = Arrow(sug.get_right() + RIGHT * 0.1, mc + np.array([-1.05, -0.35, 0]), color=GREEN, stroke_width=4, buff=0,
                   max_tip_length_to_length_ratio=0.18)
        self.at("won him")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("1902")
        self.play(FadeIn(medal, scale=0.6), Create(ring), FadeIn(yr, scale=1.3), run_time=0.7)

        n1 = T("Nobel Prize", 34, GOLD, weight=BOLD).next_to(medal, DOWN, buff=0.3)
        n2 = T("in Chemistry", 34, GOLD).next_to(n1, DOWN, buff=0.12)
        self.at("Nobel Prize")
        self.play(pop(n1), run_time=0.5)
        self.at("in Chemistry")
        self.play(pop(n2), run_time=0.5)

        # second ever awarded
        c1 = VGroup(Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12),
                    T("1st", 26, GREY)).move_to([2.3, -2.3, 0])
        c2 = VGroup(Circle(radius=0.42, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.3),
                    T("2nd", 26, GOLD, weight=BOLD)).move_to([3.7, -2.3, 0])
        step = Arrow(c1.get_right() + RIGHT * 0.05, c2.get_left() + LEFT * 0.05, color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.3)
        cap = T("second ever awarded", 26, GOLD).move_to([3.0, -3.05, 0])
        self.at("the second ever")
        self.play(pop(c1), run_time=0.4)
        self.play(GrowArrow(step), pop(c2), FadeIn(cap), run_time=0.5)
        self.play(Indicate(c2, color=GOLD, scale_factor=1.15), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 lock and key
class S03Lockkey(ProfileScene):
    CX = 2.3
    KEY_Y = 1.45
    RIM_Y = -0.2

    def construct(self):
        self.add_inset()
        cx, ky, rim = self.CX, self.KEY_Y, self.RIM_Y
        lock = lock_shape().shift(RIGHT * cx + UP * rim)
        lock_lab = T("lock", 34, LOCK).move_to([-0.7, rim - 0.9, 0])
        seat_y = rim - DEPTH + KEY_H / 2                          # key A seated on the floor of the cavity
        stuck_y = rim - 0.58 + KEY_H / 2                          # key B jammed by its shoulders on the rim

        self.at("lock")
        self.play(FadeIn(lock), FadeIn(lock_lab), run_time=0.5)

        A = VGroup(key_a(GREEN), VGroup()).move_to([cx, ky, 0])
        key_lab = T("key", 34, GREEN).move_to([cx, ky + 0.95, 0])
        self.at("key")
        self.play(FadeIn(A, shift=DOWN * 0.2), FadeIn(key_lab), run_time=0.35)
        self.at("principle")
        self.play(A.animate.move_to([cx, seat_y, 0]), key_lab.animate.move_to([cx + 2.25, seat_y, 0]),
                  run_time=0.65, rate_func=smooth)
        self.play(Flash([cx, seat_y, 0], color=GREEN, flash_radius=1.0, line_length=0.2), run_time=0.3)

        # a molecule's shape, not just its formula
        a_rect = A[0]
        B = VGroup(key_b(GREY), VGroup()).move_to([4.3, ky, 0])
        tagA = T("formula", 26, TEXT)
        tagB = T("formula", 26, TEXT)
        self.at("a molecule's shape")
        self.play(a_rect.animate.set_stroke(GREY).set_fill(GREY, 0.22), FadeOut(key_lab),
                  FadeIn(B, shift=DOWN * 0.2), run_time=0.2)
        self.play(A.animate.move_to([0.3, ky, 0]), run_time=0.4, rate_func=smooth)
        shape_lab = T("shape", 38, BLUE, weight=BOLD).move_to([cx, 2.8, 0])
        self.at("shape")
        self.play(a_rect.animate.set_stroke(BLUE, 6), B[0].animate.set_stroke(BLUE, 6), pop(shape_lab), run_time=0.5)

        tagA.move_to(A[0].get_center())
        tagB.move_to(B[0].get_center() + UP * 0.12)
        eq = M("=", 48, TEXT).move_to([cx - 0.2, ky, 0])
        self.at("formula")
        self.play(FadeIn(tagA), FadeIn(tagB), FadeIn(eq, scale=1.3), run_time=0.5)

        # shape decides what it can do: B jams, A fits
        A.add(tagA), B.add(tagB)
        self.at("decides")
        self.play(FadeOut(eq), B.animate.move_to([cx, ky, 0]), run_time=0.35, rate_func=smooth)
        self.play(B.animate.move_to([cx, stuck_y, 0]), run_time=0.35, rate_func=smooth)
        x = cross([cx, rim + 0.8, 0])
        self.play(B[0].animate.set_stroke(RED, 6).set_fill(RED, 0.3), FadeIn(x, scale=1.5), run_time=0.3)
        self.play(B.animate.move_to([4.3, ky, 0]), FadeOut(x), run_time=0.4, rate_func=smooth)
        self.play(A.animate.move_to([cx, ky, 0]), run_time=0.3, rate_func=smooth)
        self.play(A.animate.move_to([cx, seat_y, 0]), run_time=0.4, rate_func=smooth)
        self.play(A[0].animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.3),
                  Flash([cx, seat_y, 0], color=GREEN, flash_radius=1.0, line_length=0.2), run_time=0.4)

        # every drug in this chapter
        drug = T("drug", 28, GREEN, weight=BOLD).move_to(tagA)
        self.at("every drug")
        self.play(Transform(tagA, drug), FadeOut(B), run_time=0.5)
        self.remove(*B.get_family())   # tagB was also added on its own; FadeOut(B) alone restores it
        pairs = VGroup()
        for i in range(5):
            p = VGroup(lock.copy(), A[0].copy()).scale(0.3)
            p.move_to([0.0 + 1.3 * i, -2.5, 0])
            pairs.add(p)
        cap = T("every drug in this chapter", 26, GREY).move_to([2.6, -3.15, 0])
        self.at("in this chapter")
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pairs], lag_ratio=0.2), FadeIn(cap), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------- s04 the ring system hub (silent)
class S04Hub(ProfileScene):
    def construct(self):
        self.add_inset()
        center = lab(["purine", "ring system"], TEAL, 36).move_to([0.2, 0.2, 0])
        mapped = T("mapped by Fischer", 28, GOLD).next_to(center, DOWN, buff=0.4)
        head = T("sits at the center of", 28, GREY).move_to([4.5, 2.9, 0])
        sats = [lab("energy", ORANGE, 34).move_to([4.5, 1.8, 0]),
                lab("signaling", VIOLET, 34).move_to([4.5, 0.2, 0]),
                lab("heredity", PINK, 34).move_to([4.5, -1.4, 0])]
        lines = [Line(center.get_right() + RIGHT * 0.05, s.get_left() + LEFT * 0.05, color=GREY, stroke_width=3)
                 for s in sats]
        self.wait(0.3)
        self.play(pop(center), run_time=0.6)
        self.play(FadeIn(mapped, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.4)
        for ln, s in zip(lines, sats):
            self.play(Create(ln), pop(s), run_time=0.6)
            self.wait(0.25)
        self.play(Indicate(center, color=TEAL, scale_factor=1.08), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 the quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Enzyme and glucoside must", "fit together like a", "lock and key.”"]
        q = VGroup(*[T(l, 40, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— Emil Fischer", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([PANEL_C, 1.45, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
            self.wait(0.3)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)

        # the schematic echoes the quote: a key drops into its lock
        s = 0.8
        lk = lock_shape().scale(s).move_to([PANEL_C, -2.45, 0])
        rim = lk.get_top()[1]
        ky = key_a(GREEN)
        ky.scale(s)
        seat = rim - DEPTH * s + KEY_H * s / 2
        ky.move_to([PANEL_C, rim + 0.65, 0])
        self.wait(0.3)
        self.play(FadeIn(lk), FadeIn(ky), run_time=0.6)
        self.play(ky.animate.move_to([PANEL_C, seat, 0]), run_time=0.9, rate_func=smooth)
        self.play(Flash([PANEL_C, seat, 0], color=GREEN, flash_radius=0.7, line_length=0.15), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Named the purines and synthesized the parent compound."

    def construct(self):
        img, frame = portrait_pair(2.3)
        img.move_to([0, 2.0, 0])
        frame.move_to(img)
        cap = T(CAPTION, 22, GREY).next_to(frame, DOWN, buff=0.15)
        a = T("Named the purines and", size=40, font=TITLE_FONT)
        b = T("synthesized the parent compound.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.75, 0])
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -2.0, 0])
        src = T("Source: The Molecule Hunters (v10) · Emil Fischer profile", 22, GREY).move_to([0, -2.7, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
