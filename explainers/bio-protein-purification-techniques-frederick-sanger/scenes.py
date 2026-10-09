"""Frederick Sanger: scientist profile video (Biochemistrypedia, protein-purification-techniques lesson)

The portrait (public/scientists/frederick-sanger.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed inset on
the left while the right side animates the story's beats as the narrator reaches them.
Narration is this lesson entry's `story`, verbatim (one sentence dropped: "He described two of the
century's great discoveries the same modest way ..."). Every cue is a self.at("spoken words") lookup in
audio/words.json (word timestamps of the real audio). Nothing on screen adds a fact that is not in the
entry (name, dates, contribution, story, quotes). No molecular structure is drawn: amino acids are plain
coloured tiles in a row (a sequence), fragments are bars, everything else is labels and arrows.

COLOR MAP (one color per concept, whole video)
  GOLD   = Sanger himself and his own words, the portrait frame, "settled", the knighthood
  YELLOW = years and counts (12 years, 1943)
  BLUE   = amino acids / the chain (PINK, ORANGE, VIOLET are just other residue types, to tell tiles apart)
  RED    = doubt and dead ends: the unknown, "not trusted", the two killed theories
  GREEN  = cross-checks: overlapping fragments, the several directions, "believed"
  TEAL   = the institution (the genome center at Hinxton)
  TEXT/GREY = labels, his convictions (conscientious objector, not wanting to be different), the war
"""
import os
import random
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

VIOLET = "#9D86E9"
PINK = "#E27DA5"
ORANGE = "#E8935A"
RES = [BLUE, PINK, ORANGE, VIOLET]

CX = 1.9            # centre of the content area to the right of the portrait column
PORT_X = -4.6       # portrait column centre
PORT_H = 3.3
PORT_Y = 1.3
CROP_AR = 860 / 780.0   # sanger_crop.png: the engraving cropped to the figure (from public/scientists/frederick-sanger.png)
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "sanger_crop.png"
NAME = "Frederick Sanger"
DATES = "1918–2013"
CAPTION = "illustration · AI-generated"


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    img.set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def column_labels():
    """Caption plus name and dates under the inset portrait."""
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
    nm = VGroup(T(NAME, 30, TEXT, font=TITLE_FONT), T(DATES, 26, GOLD)).arrange(DOWN, buff=0.12)
    nm.move_to([PORT_X, y - 1.25, 0])
    return cap, nm


def tint(color, k=0.3):
    """Opaque dim version of a colour (so lines behind a tile do not show through it)."""
    return ManimColor(BG).interpolate(ManimColor(color), k)


def tile(color=BLUE, size=0.42, fill=0.28):
    return RoundedRectangle(corner_radius=size * 0.2, width=size, height=size, stroke_color=color,
                            stroke_width=2.5, fill_color=tint(color, fill), fill_opacity=1)


def tile_row(idx, size=0.42, pitch=0.54, fill=0.3, palette=RES):
    row = VGroup(*[tile(palette[i % len(palette)], size, fill) for i in idx])
    row.arrange(RIGHT, buff=pitch - size)
    return row


def check_mark(color=GREEN, s=0.28):
    return VGroup(Line([-s, 0, 0], [-s * 0.3, -s * 0.8, 0]), Line([-s * 0.3, -s * 0.8, 0], [s, s * 0.9, 0])) \
        .set_color(color).set_stroke(width=8)


def cross_mark(color=RED, s=0.26):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])).set_color(color).set_stroke(width=8)


def pop(mob, d=UP * 0.12):
    return FadeIn(mob, shift=d)


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        cap, nm = column_labels()
        self.add(img, border, cap, nm)
        self.img, self.border = img, border

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c


# ----------------------------------------------------------------------------------------- s00 title
class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 4.0
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.8, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.8 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        name.move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.2, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.9, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.35)
        # slow push-in while the name and dates arrive
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.4, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.3)
        # hand over to the inset layout used by every later scene
        cap2, nm = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       FadeIn(nm)),
            run_time=0.75))
        self.finish()


# ----------------------------------------------------------------------------------------- s01 twelve years
class S01Years(BioScene):
    def construct(self):
        self.add_column()
        # --- Twelve years
        blocks = VGroup(*[Square(0.34, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(12)])
        blocks.arrange(RIGHT, buff=0.1).move_to([CX + 1.0, 2.75, 0])
        n12 = M("12", 54, YELLOW)
        yrs = T("years", 32, YELLOW)
        lab12 = VGroup(n12, yrs).arrange(RIGHT, buff=0.2, aligned_edge=DOWN).move_to([-0.9, 2.75, 0])
        self.at("12 years")
        self.play(FadeIn(lab12, shift=UP * 0.1), LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.15),
                  run_time=1.2)

        # --- insulin
        self.at("insulin")
        ins = self.chip_at("insulin", BLUE, CX, 1.4, 34)
        self.play(pop(ins), run_time=0.5)
        self.at("cost")
        arr = Arrow([CX, 2.42, 0], [CX, ins.get_top()[1] + 0.06, 0], buff=0, color=GREY, stroke_width=5,
                    max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(arr), run_time=0.4)

        self.at("Frederick Sanger")
        self.play(Indicate(self.border, color=GOLD, scale_factor=1.05), run_time=0.7)

        # --- 51 amino acids: three rows of 17 plain tiles
        rows = VGroup()
        for r in range(3):
            row = VGroup(*[tile(BLUE, 0.28, 0.16) for _ in range(17)]).arrange(RIGHT, buff=0.09)
            rows.add(row)
        rows.arrange(DOWN, buff=0.09).move_to([CX, 0.2, 0])
        flat = [t for row in rows for t in row]
        lab51 = T("51 amino acids", 32, BLUE).move_to([CX, -0.78, 0])
        self.at("51 amino acids")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in flat], lag_ratio=0.02), FadeIn(lab51), run_time=1.6)

        # --- read one position at a time
        cur = Square(0.38, color=TEXT, stroke_width=4).move_to(rows[0][0]).set_z_index(5)
        pos_lab = T("one stubborn position at a time", 30, TEXT).move_to([CX, -1.6, 0])
        self.at("read one stubborn")
        self.play(Create(cur), run_time=0.2)
        for k in range(3):
            self.play(rows[0][k].animate.set_fill(BLUE, 0.95), cur.animate.move_to(rows[0][k]), run_time=0.2)
        self.at("position at a time")
        self.play(rows[0][3].animate.set_fill(BLUE, 0.95), cur.animate.move_to(rows[0][3]), FadeIn(pos_lab, shift=UP * 0.1),
                  run_time=0.3)
        for k in range(4, 9):
            self.play(rows[0][k].animate.set_fill(BLUE, 0.95), cur.animate.move_to(rows[0][k]), run_time=0.2)

        # --- nobody knew whether it would mean anything
        self.at("nobody knew")
        q = T("?", 120, RED, font=TITLE_FONT).move_to([5.7, 0.15, 0])
        self.play(FadeOut(cur), FadeIn(q, scale=1.4), run_time=0.5)
        self.at("whether reading them")
        mean = T("would it mean anything?", 34, RED, font=TITLE_FONT).move_to([CX, -2.5, 0])
        self.play(pop(mean), run_time=0.5)
        self.at("mean anything")
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------- s02 1943
class S021943(BioScene):
    def construct(self):
        self.add_column()
        rng = random.Random(7)
        yr = M("1943", 54, YELLOW).move_to([-0.6, 2.85, 0])
        self.at("in 1943")
        self.play(FadeIn(yr, shift=UP * 0.1), run_time=0.5)
        knew = T("the field knew", 32, GREY).next_to(yr, RIGHT, buff=0.5).align_to(yr, DOWN).shift(UP * 0.02)
        self.at("the field knew")
        self.play(pop(knew), run_time=0.4)

        # a chain of amino acids
        chain = tile_row([0, 1, 2, 1, 3, 0, 2, 3, 1, 0, 2], 0.5, 0.64).move_to([CX, 1.6, 0])
        link = Line(chain[0].get_center(), chain[-1].get_center(), color=GREY, stroke_width=4).set_z_index(-1)
        chain_lab = T("a chain of amino acids", 32, BLUE).move_to([CX, 0.9, 0])
        self.at("a chain of amino acids")
        self.play(Create(link), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in chain], lag_ratio=0.15),
                  FadeIn(chain_lab), run_time=1.3)

        # the twenty-odd letters of the alphabet
        alpha = VGroup(*[tile(RES[i % 4], 0.38, 0.3) for i in range(22)])
        alpha.arrange_in_grid(rows=2, cols=11, buff=0.12).move_to([CX, -0.6, 0])
        alpha_lab = T("the twenty-odd letters", 32, TEXT).move_to([CX, -1.65, 0])
        self.at("20 odd letters")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in alpha], lag_ratio=0.04), run_time=1.1)
        self.play(FadeIn(alpha_lab, shift=UP * 0.1), run_time=0.4)

        # what nobody knew
        self.at("what nobody knew")
        nobody = T("what nobody knew", 32, RED)
        nobody.move_to(knew, aligned_edge=LEFT)
        self.play(FadeOut(chain), FadeOut(link), FadeOut(chain_lab), ReplacementTransform(knew, nobody), run_time=0.6)

        def panel(cx, rows_idx, color):
            frame = RoundedRectangle(corner_radius=0.2, width=4.0, height=2.7, stroke_color=color, stroke_width=3,
                                     fill_color=color, fill_opacity=0.05)
            rs = VGroup(*[tile_row(r, 0.44, 0.54, 0.3) for r in rows_idx]).arrange(DOWN, buff=0.26)
            g = VGroup(frame, rs)
            rs.move_to(frame)
            g.move_to([cx, 0.85, 0])
            return g, frame, rs

        word_seq = [0, 1, 2, 1, 3, 0, 2]
        word, word_f, word_rows = panel(-0.15, [word_seq] * 3, GREY)
        rnd = lambda: [rng.randrange(4) for _ in range(7)]
        r1, r2 = [rnd() for _ in range(3)], [rnd() for _ in range(3)]
        rand, rand_f, rand_rows = panel(4.15, r1, GREY)
        word_lab = T("spelled a word", 28, TEXT).move_to([-0.15, -0.9, 0])
        rand_lab = T("a different random draw", 26, TEXT).move_to([4.15, -0.9, 0])

        self.at("letters spelled a word")
        self.play(FadeOut(alpha), FadeOut(alpha_lab), run_time=0.25)
        self.play(FadeIn(word_f), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in word_rows], lag_ratio=0.25), FadeIn(word_lab),
                  run_time=0.9)
        self.at("or whether each protein")
        self.play(FadeIn(rand_f), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rand_rows], lag_ratio=0.25), FadeIn(rand_lab),
                  run_time=0.9)
        self.at("a different random draw")
        # each row is a fresh draw
        anims = []
        for row, new in zip(rand_rows, r2):
            for t, i in zip(row, new):
                anims.append(t.animate.set_color(RES[i]).set_fill(tint(RES[i], 0.3), 1))
        self.play(*anims, run_time=0.9)

        self.at("Sanger settled it")
        settled = T("Sanger settled it.", 46, GOLD, font=TITLE_FONT).move_to([CX, -2.2, 0])
        self.play(word_f.animate.set_stroke(GOLD, width=5), word_lab.animate.set_color(GOLD),
                  rand.animate.set_opacity(0.3), rand_lab.animate.set_opacity(0.3),
                  FadeIn(settled, shift=UP * 0.12), run_time=0.9)
        self.play(Indicate(self.border, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------- s03 the sentence
class S03Sentence(BioScene):
    def construct(self):
        self.add_column()
        rng = random.Random(11)
        seq = [0, 1, 2, 1, 3, 0, 2, 3, 1, 0, 2, 1]
        row = tile_row(seq, 0.42, 0.54).move_to([CX, 2.8, 0])
        seq_lab = T("the sequence", 30, BLUE).move_to([CX, 2.15, 0])
        self.at("the sequence")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in row], lag_ratio=0.1), FadeIn(seq_lab), run_time=1.3)

        # what he wrote
        wrote = T("he wrote:", 28, GREY).move_to(seq_lab)
        self.at("he wrote")
        self.play(ReplacementTransform(seq_lab, wrote), run_time=0.4)
        l1 = T("proteins are definite chemical substances", 32, GOLD, font=TITLE_FONT).move_to([CX, 1.3, 0])
        fit(l1, max_w=8.6)
        self.at("definite chemical substances", lead=0.3)
        self.play(Write(l1), run_time=1.5)
        l2 = T("possessing a unique structure", 32, GOLD, font=TITLE_FONT).move_to([CX, 0.55, 0])
        self.at("unique structure", lead=0.3)
        self.play(Write(l2), run_time=1.2)

        # each position in the chain
        nums = VGroup(*[M(str(i + 1), 24, GREY).next_to(row[i], DOWN, buff=0.14) for i in range(12)])
        slots = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.54, height=0.54, stroke_color=GREY,
                                                         stroke_width=2).move_to(t), num_dashes=16) for t in row])
        self.at("each position in the chain")
        self.play(FadeOut(wrote), FadeIn(slots), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.08), run_time=1.1)
        one = VGroup(T("each position:", 30, BLUE), T("one and only one amino acid residue", 30, BLUE)).arrange(DOWN, buff=0.12)
        one.move_to([CX, -1.0, 0])
        self.at("occupied by")
        self.play(AnimationGroup(
            LaggedStart(*[Indicate(t, color=TEXT, scale_factor=1.25) for t in row], lag_ratio=0.2),
            Succession(Wait(0.9), FadeIn(one, shift=UP * 0.1)),
        ), run_time=3.0)

        # a single sentence
        one_s = T("one sentence", 46, GOLD, font=TITLE_FONT).move_to([CX, 2.6, 0])
        ul = Line(one_s.get_corner(DL) + DOWN * 0.1, one_s.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.at("single sentence")
        self.play(FadeOut(Group(row, slots, nums, one, l1, l2)), run_time=0.5)
        self.play(FadeIn(one_s, shift=UP * 0.1), Create(ul), run_time=0.6)

        def frame_at(cx):
            return RoundedRectangle(corner_radius=0.2, width=4.0, height=2.7, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.05).move_to([cx, -0.15, 0])

        def fill_card(frame, rows_idx, title):
            rs = VGroup(*[tile_row(r, 0.44, 0.54, 0.3) for r in rows_idx]).arrange(DOWN, buff=0.26).move_to(frame)
            lab = T(title, 30, TEXT)
            lab.move_to([frame.get_center()[0], frame.get_top()[1] + 0.45, 0])  # same y for both cards
            return rs, lab

        f1, f2 = frame_at(-0.15), frame_at(4.15)
        p_rows, p_lab = fill_card(f1, [[0, 1, 2, 0, 1, 2, 0], [1, 2, 0, 1, 2, 0, 1], [2, 0, 1, 2, 0, 1, 2]], "periodic pattern")
        m_rows, m_lab = fill_card(f2, [[rng.randrange(4) for _ in range(7)] for _ in range(3)], "random mixture")
        self.at("killed both")
        self.play(FadeIn(f1), FadeIn(f2), run_time=0.5)
        self.at("periodic pattern theory")
        self.play(FadeIn(p_lab, shift=UP * 0.1), FadeIn(p_rows, shift=UP * 0.1), run_time=0.7)
        self.at("random mixture theory")
        self.play(FadeIn(m_lab, shift=UP * 0.1), FadeIn(m_rows, shift=UP * 0.1), run_time=0.7)
        self.at("at once")
        x1 = cross_mark(RED, 0.55).move_to(f1).set_z_index(5)
        x2 = cross_mark(RED, 0.55).move_to(f2).set_z_index(5)
        self.play(Create(x1), Create(x2), f1.animate.set_stroke(RED, width=4), f2.animate.set_stroke(RED, width=4),
                  p_rows.animate.set_opacity(0.35), m_rows.animate.set_opacity(0.35), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------- s04 cross-checking
class S04Checks(BioScene):
    def construct(self):
        self.add_column()
        # he did not trust a result he could check only one way
        nt = T("did not trust", 36, RED, font=TITLE_FONT).move_to([CX, 2.7, 0])
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.5)
        res = self.chip_at("a result", GREY, -0.2, 1.3, 32)
        self.at("a result")
        self.play(pop(res), run_time=0.5)
        one = self.chip_at("one check", GREEN, 4.2, 1.3, 30)
        a1 = Arrow(one.get_left() + LEFT * 0.08, res.get_right() + RIGHT * 0.08, buff=0, color=GREEN, stroke_width=5,
                   max_tip_length_to_length_ratio=0.3)
        self.at("check only one way")
        self.play(FadeIn(one, shift=LEFT * 0.2), GrowArrow(a1), run_time=0.7)
        only = T("only one way", 32, RED).move_to([CX + 0.9, 0.3, 0])
        self.at("one way")
        self.play(pop(only), run_time=0.4)
        self.at("because as he put it", lead=0.3)
        self.play(FadeOut(Group(nt, res, one, a1, only)), run_time=0.4)

        # the methods used were new and were qualitative rather than quantitative
        asit = T("as he put it:", 28, GREY).move_to([CX, 2.7, 0])
        self.at("as he put it")
        self.play(pop(asit), run_time=0.4)
        q1 = T("“the methods used were new", 36, GOLD, font=TITLE_FONT)
        q2 = T("and were qualitative", 36, GOLD, font=TITLE_FONT)
        q3 = T("rather than quantitative”", 36, GOLD, font=TITLE_FONT)
        qg = VGroup(q1, q2, q3)
        for i, q in enumerate(qg):          # fixed line pitch, so descenders do not make the gaps uneven
            q.move_to([0, 1.75 - 0.72 * i, 0], aligned_edge=LEFT)
        qg.move_to([CX, 1.1, 0])
        self.at("the methods used were new")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.7)
        self.at("were qualitative")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.7)
        self.at("rather than quantitative")
        self.play(FadeIn(q3, shift=UP * 0.1), run_time=0.8)

        # far more overlapping fragments than the bare logic required
        chain = tile_row([i % 4 for i in [0, 1, 2, 1, 3, 0, 2, 3, 1, 0, 2, 1, 3, 0]], 0.44, 0.54).move_to([CX, -0.1, 0])
        up_y = lambda lvl: -0.1 + 0.42 + 0.3 * lvl
        dn_y = lambda lvl: -0.1 - 0.42 - 0.3 * lvl
        spans = {  # (band, level): [(first tile, last tile), ...]; fragments in one row never overlap each other,
                   # neighbouring rows are offset so that the fragments overlap across rows
            ("up", 0): [(0, 4), (5, 9), (10, 13)],
            ("up", 1): [(2, 6), (7, 11)],
            ("up", 2): [(0, 3), (4, 8), (9, 13)],
            ("down", 0): [(0, 5), (6, 10), (11, 13)],
            ("down", 1): [(0, 2), (3, 7), (8, 12)],
            ("down", 2): [(1, 5), (6, 9), (10, 13)],
        }

        def make_bars(key):
            band, lvl = key
            out = []
            for a_, b_ in spans[key]:
                x0, x1 = chain[a_].get_left()[0], chain[b_].get_right()[0]
                r = RoundedRectangle(corner_radius=0.07, width=x1 - x0, height=0.2, stroke_color=BG, stroke_width=2,
                                     fill_color=GREEN, fill_opacity=0.65)
                r.move_to([(x0 + x1) / 2, up_y(lvl) if band == "up" else dn_y(lvl), 0])
                out.append(r)
            return out

        first = make_bars(("up", 0))
        rest1 = make_bars(("down", 0)) + make_bars(("up", 1)) + make_bars(("down", 1))
        rest2 = make_bars(("up", 2)) + make_bars(("down", 2))
        bars = first + rest1 + rest2
        frag_lab = T("overlapping fragments", 30, GREEN).move_to([CX, 2.4, 0])
        more_lab = T("far more than the bare logic required", 28, GREY).move_to([CX, -2.55, 0])
        self.at("He gathered", lead=0.6)
        self.play(FadeOut(Group(asit, qg)),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in chain], lag_ratio=0.05), run_time=0.6)
        self.at("far more")
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in first], lag_ratio=0.25), run_time=0.7)
        self.at("overlapping fragments")
        self.play(pop(frag_lab), LaggedStart(*[GrowFromEdge(b, LEFT) for b in rest1], lag_ratio=0.12), run_time=1.0)
        self.at("than the bare logic required")
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in rest2], lag_ratio=0.12), pop(more_lab, UP * 0.1), run_time=1.0)

        # cross-checking every conclusion from several directions
        self.at("cross checking", lead=0.15)
        self.play(FadeOut(Group(chain, frag_lab, more_lab, *bars)), run_time=0.4)
        concl = self.chip_at("a conclusion", GOLD, 4.2, 0.4, 32)
        self.at("every conclusion")
        self.play(pop(concl), run_time=0.5)
        dirs = [self.chip_at(f"direction {i + 1}", GREEN, -0.5, y, 28) for i, y in enumerate([1.8, 0.4, -1.0])]
        arrs = [Arrow(d.get_right() + RIGHT * 0.08, concl.get_left() + LEFT * 0.08 + UP * dy, buff=0, color=GREEN,
                      stroke_width=4, tip_length=0.2) for d, dy in zip(dirs, [0.16, 0.0, -0.16])]
        self.at("from several directions")
        self.play(LaggedStart(*[AnimationGroup(pop(d, RIGHT * 0.15), GrowArrow(a)) for d, a in zip(dirs, arrs)],
                              lag_ratio=0.4), run_time=1.3)
        self.at("believe it")
        done = self.chip_at("a conclusion", GREEN, 4.2, 0.4, 32)
        tick = check_mark(GREEN, 0.3).move_to([3.5, -0.75, 0])
        believed = T("believed", 30, GREEN).next_to(tick, RIGHT, buff=0.25)
        self.play(Transform(concl, done), Create(tick), FadeIn(believed), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------- s05 modest
class S05Modest(BioScene):
    def construct(self):
        self.add_column()
        # his own cheerful admission
        own = T("his own cheerful admission", 30, GREY).move_to([CX, 2.6, 0])
        self.at("cheerful admission")
        self.play(pop(own), run_time=0.5)
        nb = T("“academically not brilliant”", 42, GOLD, font=TITLE_FONT)
        fit(nb, max_w=8.4)
        nb.move_to([CX, 1.3, 0])
        self.at("academically not brilliant", lead=0.3)
        self.play(Write(nb), run_time=0.8)

        # scrubbed hospital floors as a conscientious objector during the war
        floor_lab = self.chip_at("hospital floors", GREY, CX, 2.3, 30)
        floor = Rectangle(width=6.6, height=0.28, stroke_width=0, fill_color=GREY, fill_opacity=0.45).move_to([CX, 0.9, 0])
        x_left = CX - 3.3
        brush = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.5, stroke_color=TEXT, stroke_width=3,
                                 fill_color=TEXT, fill_opacity=0.2).move_to([x_left + 0.35, 1.2, 0])
        self.at("He scrubbed", lead=0.2)
        self.play(FadeOut(Group(own, nb)), FadeIn(floor), FadeIn(brush), run_time=0.4)
        tr = ValueTracker(0.0)

        def make_clean():
            w = max(0.01, 0.7 + tr.get_value() * 5.9)
            return Rectangle(width=w, height=0.28, stroke_width=0, fill_color=TEXT, fill_opacity=0.5).move_to(
                [x_left + w / 2, 0.9, 0])

        clean = always_redraw(make_clean)
        brush.add_updater(lambda m: m.move_to([x_left + 0.35 + tr.get_value() * 5.9, 1.2, 0]))
        self.add(clean)
        self.play(tr.animate.set_value(1.0), Succession(Wait(0.55), FadeIn(floor_lab, shift=DOWN * 0.1)),
                  run_time=1.3, rate_func=linear)
        clean.clear_updaters(); brush.clear_updaters()
        self.at("conscientious objector", lead=0.1)
        co = self.chip_at("conscientious objector", TEXT, CX, -0.55, 30)
        self.play(pop(co), run_time=0.5)
        self.at("during the war")
        war = T("during the war", 30, GREY).move_to([CX, -1.55, 0])
        self.play(pop(war), run_time=0.5)

        # declined a knighthood
        self.at("declined a knighthood", lead=0.35)
        self.play(FadeOut(Group(floor_lab, floor, clean, brush, co, war)), run_time=0.35)
        kn = self.chip_at("a knighthood", GOLD, CX - 1.5, 1.5, 34)
        self.at("declined")
        self.play(pop(kn), run_time=0.5)
        self.at("knighthood")
        strike = Line(kn.get_left() + LEFT * 0.15, kn.get_right() + RIGHT * 0.15, color=RED, stroke_width=6)
        declined = T("declined", 34, RED, font=TITLE_FONT).next_to(kn, RIGHT, buff=0.5)
        self.play(Create(strike), FadeIn(declined, shift=LEFT * 0.15), run_time=0.6)
        diff = T("he did not want to be different", 36, TEXT, font=TITLE_FONT).move_to([CX, -0.3, 0])
        fit(diff, max_w=8.4)
        self.at("did not want to be different")
        self.play(Write(diff), run_time=1.4)

        # Hinxton
        self.at("When the Great Genome", lead=0.4)
        self.play(FadeOut(Group(kn, strike, declined, diff)), run_time=0.35)
        gc = self.chip_at("the great genome center", TEAL, CX, 2.55, 30)
        self.play(pop(gc), run_time=0.5)
        self.at("Kingston")                      # the transcriber hears "Hinxton" as "Kingston"
        hx = self.chip_at("Hinxton", TEAL, CX, 1.55, 34)
        self.play(pop(hx), run_time=0.5)
        plate = VGroup(RoundedRectangle(corner_radius=0.1, width=3.6, height=0.8, stroke_color=GOLD, stroke_width=3,
                                        fill_color=GOLD, fill_opacity=0.14), T(NAME, 30, GOLD, font=TITLE_FONT))
        plate[1].move_to(plate[0])
        plate.move_to([CX, -0.1, 0])
        up = Arrow(plate.get_top() + UP * 0.05, hx.get_bottom() + DOWN * 0.05, buff=0, color=GOLD, stroke_width=4, tip_length=0.2)
        self.at("asked to take his name")
        self.play(FadeIn(plate, shift=UP * 0.2), run_time=0.5)
        self.play(GrowArrow(up), run_time=0.5)
        cond = T("one condition", 34, TEXT, font=TITLE_FONT).move_to([CX, -1.2, 0])
        self.at("he made one condition")
        self.play(pop(cond), run_time=0.5)
        good = T("it had better be good", 46, GOLD, font=TITLE_FONT).move_to([CX, -2.3, 0])
        self.at("It had better be good")
        self.play(Write(good), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------- s06 quote
class S06Quote(BioScene):
    def construct(self):
        self.add_column()
        mark = T("“", 120, GOLD, font=TITLE_FONT)
        lines = [T("Practically nothing was known about", 36, TEXT, font=TITLE_FONT),
                 T("the relative order in which these residues", 36, TEXT, font=TITLE_FONT),
                 T("were arranged in the molecules.”", 36, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines)
        for i, ln in enumerate(lines):      # fixed line pitch
            ln.move_to([0, -0.66 * i, 0], aligned_edge=LEFT)
        fit(qg, max_w=8.4)
        qg.move_to([CX + 0.2, 0.7, 0])
        mark.scale(0.7).next_to(lines[0], LEFT, buff=0.12).align_to(lines[0], UP).shift(UP * 0.12)
        att = T("Frederick Sanger, Nobel lecture", 28, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.5)
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.8)
            self.wait(0.35)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------- s07 end card
class S07End(BioScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.05))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.05 - 1.15 - 0.3, 0])
        l1 = T("Read insulin, the first protein sequence;", 38, font=TITLE_FONT)
        l2 = T("made DNA sequencing routine; two Nobels.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Frederick Sanger profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
