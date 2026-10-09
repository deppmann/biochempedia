"""Stanford Moore & William Stein: scientist profile video (Biochemistrypedia, protein-purification-techniques lesson)

The portrait (public/scientists/moore-stein.png, an AI-generated engraving-style illustration from
The Molecule Hunters, cropped to the two figures as ms_crop.png) is the anchor: the title scene pushes in on it,
then it stays as a framed inset on the left while the right side animates the story's beats as the narrator
reaches them. Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quotes).

The portrait is NOT split into per-face highlights or per-face name labels: the entry never says which engraved
face is Moore and which is Stein, so the video does not claim it. The names live in the text panel instead.

Narration = the entry's `story` verbatim, minus ONE sentence (the Exeter sentence, which is shown instead as the
silent quote scene, attributed to Stein as the story itself does).

COLOR MAP (one color per concept, whole video)
  GOLD   = the pair: Moore & Stein, equality, the portrait frame, perseverance ("neither stopped"), the quote
  YELLOW = numbers and tools (124, valves, turntables)
  GREEN  = amino acids, the protein's sequence
  PINK   = the ninhydrin color change and what it detects (the recorder peaks)
  BLUE   = the protein: ribonuclease (the enzyme) and the protein's three-dimensional shape
  RED    = illness and obstacles (Guillain-Barre, ALS, the blocked touch, the rejected "discovery to discovery")
  TEAL   = places (the lab, the apartment) and the brand
  GREY   = structure, apparatus, de-emphasised things
No molecular structure is drawn: amino acids are dots and tiles, the protein is a blob, the analyzer is boxes and a trace.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PINK = "#E8749A"
CX = 2.25            # centre of the panel to the right of the portrait column
PORT_X, PORT_Y, PORT_H = -4.3, 1.35, 2.2
CROP_AR = 1072 / 600.0
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "ms_crop.png"
NAME = "Stanford Moore & William Stein"
DATES = "Moore: 1913–1982 · Stein: 1911–1980"
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
    """Caption under the portrait, then the names and dates (not tied to either face)."""
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.3, 0])
    names = VGroup(T("Stanford Moore", 30, TEXT, font=TITLE_FONT),
                   T("& William Stein", 30, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.1).move_to([PORT_X, y - 1.25, 0])
    dates = VGroup(T("Moore: 1913–1982", 24, GOLD), T("Stein: 1911–1980", 24, GOLD)).arrange(DOWN, buff=0.1)
    dates.move_to([PORT_X, y - 2.35, 0])
    return cap, names, dates


def lab(lines, color=BLUE, size=26, pad=0.2, fill=0.16, dashed=False):
    """Chip with one or more centered lines."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    if dashed:
        box = DashedVMobject(box, num_dashes=40, dashed_ratio=0.55).set_color(color)
        box.set_fill(opacity=0)
        return VGroup(box, txt.move_to(box.get_center()))
    return VGroup(box, txt.move_to(box))


def pop(m, d=UP * 0.12):
    return FadeIn(m, shift=d)


def arr(a, b, color=GREY, w=4, tip=0.3):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=tip)


def xmark(center, color=RED, s=0.26, w=8):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])).set_color(color).set_stroke(width=w).move_to(center)


def check(center, color=GOLD, s=0.3, w=7):
    return VGroup(Line([-s * 0.6, 0, 0], [-s * 0.15, -s * 0.5, 0]), Line([-s * 0.15, -s * 0.5, 0], [s * 0.7, s * 0.6, 0])) \
        .set_color(color).set_stroke(width=w).move_to(center)


def peaks(x0, x1, base, hts, mus, sig=0.035, color=PINK, w=4):
    """A pen-recorder style trace: baseline plus Gaussian peaks (real equation exp(-(x-mu)^2 / 2 sigma^2))."""
    def f(u):
        return sum(h * np.exp(-((u - m) ** 2) / (2 * sig ** 2)) for h, m in zip(hts, mus))
    us = np.linspace(0, 1, 260)
    pts = [[x0 + (x1 - x0) * u, base + f(u), 0] for u in us]
    line = VMobject(color=color, stroke_width=w)
    line.set_points_as_corners(pts)
    return line


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        cap, names, dates = column_labels()
        rule = Line([-1.95, -3.2, 0], [-1.95, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
        self.add(img, border, cap, names, dates, rule)


class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 3.6
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.85, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.85 - big_h / 2 - 0.42, 0])
        name = T(NAME, 50, font=TITLE_FONT)
        fit(name, max_w=11.5)
        name.move_to([0, -2.1, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -2.95, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        cap2, names, dts = column_labels()
        rule2 = Line([-1.95, -3.2, 0], [-1.95, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(names), FadeIn(dts), FadeIn(rule2))),
            run_time=0.8))
        self.finish()


# ----------------------------------------------------------------------------- s01: equal partners
class S01Equal(BioScene):
    def construct(self):
        self.add_column()
        # --- papers with alternating author order
        orders = [("Moore", "Stein"), ("Stein", "Moore"), ("Moore", "Stein")]
        cards = []
        for i, (a, b) in enumerate(orders):
            body = Rectangle(width=2.35, height=1.7, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.1)
            first = T(a, 26, GOLD, weight=BOLD)
            sep = T("·", 26, GREY)
            second = T(b, 26, GREY)
            head = VGroup(first, sep, second).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            head.move_to(body.get_top() + DOWN * 0.38)
            bars = VGroup(*[Line(LEFT * 0.85, RIGHT * (0.85 - 0.3 * (j == 2)), color=GREY, stroke_width=4).set_opacity(0.55)
                            for j in range(3)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            bars.move_to(body.get_center() + DOWN * 0.3)
            c = VGroup(body, head, bars).move_to([CX + (i - 1) * 2.75, 2.2, 0])
            cards.append(c)
        # the first-listed name is highlighted: the order alternates
        self.play(pop(cards[0]), run_time=0.45)
        self.at("name came first")
        self.play(pop(cards[1]), run_time=0.45)
        self.at("on the papers")
        self.play(pop(cards[2]), run_time=0.45)

        # --- balance: exactly equal
        th = ValueTracker(0.16)
        pivot = np.array([CX, -0.9, 0.0])
        half = 2.4

        def ends():
            a = th.get_value()
            return (pivot + np.array([-half * np.cos(a), half * np.sin(a) + 0.35, 0]),
                    pivot + np.array([half * np.cos(a), -half * np.sin(a) + 0.35, 0]))

        beam = always_redraw(lambda: Line(ends()[0], ends()[1], color=GREY, stroke_width=7))
        tri = Polygon(pivot + np.array([0, 0.35, 0]), pivot + np.array([-0.45, -0.55, 0]), pivot + np.array([0.45, -0.55, 0]),
                      color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25)
        chm = chip("Moore", GOLD, 28)
        chs = chip("Stein", GOLD, 28)
        chm.add_updater(lambda m: m.move_to(ends()[0] + UP * 0.5))
        chs.add_updater(lambda m: m.move_to(ends()[1] + UP * 0.5))
        self.at("to signal")
        self.add(beam)
        self.play(FadeIn(tri), FadeIn(chm), FadeIn(chs), run_time=0.5)
        self.at("exactly equal")
        self.play(th.animate.set_value(0.0), run_time=0.8, rate_func=smooth)
        eq = T("exactly equal", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.3, 0])
        self.play(pop(eq), run_time=0.5)
        beam.clear_updaters(); chm.clear_updaters(); chs.clear_updaters()

        # --- argued every sentence
        self.at("Stanford Moore", lead=0.9)
        self.play(FadeOut(Group(*cards, beam, tri, chm, chs, eq)), run_time=0.4)
        page = Rectangle(width=3.2, height=3.0, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.08)
        page.move_to([CX, 0.45, 0])
        bars = VGroup(*[Line(LEFT * 1.2, RIGHT * (1.2 - 0.5 * (j % 3 == 2)), color=GREY, stroke_width=6).set_opacity(0.5)
                        for j in range(6)]).arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to(page.get_center())
        chm2 = chip("Moore", GOLD, 28).move_to([CX - 3.2, 0.45, 0])
        chs2 = chip("Stein", GOLD, 28).move_to([CX + 3.2, 0.45, 0])
        self.play(FadeIn(page), FadeIn(bars), run_time=0.3)
        self.at("Stanford Moore")
        self.play(pop(chm2, RIGHT * 0.2), run_time=0.4)
        self.at("William Stein")
        self.play(pop(chs2, LEFT * 0.2), run_time=0.4)
        a1 = DoubleArrow(chm2.get_right() + RIGHT * 0.05, page.get_left() + LEFT * 0.05, buff=0, color=GOLD, stroke_width=4, tip_length=0.18)
        a2 = DoubleArrow(chs2.get_left() + LEFT * 0.05, page.get_right() + RIGHT * 0.05, buff=0, color=GOLD, stroke_width=4, tip_length=0.18)
        self.at("argued")
        self.play(GrowFromCenter(a1), GrowFromCenter(a2), run_time=0.4)
        self.at("every sentence")
        self.play(LaggedStart(*[b.animate.set_color(GOLD).set_opacity(1.0) for b in bars], lag_ratio=0.35), run_time=1.0)
        self.at("a finding", lead=0.1)
        find = T("a finding", 26, GREY).move_to([CX - 0.5, 2.6, 0])
        self.play(pop(find), run_time=0.3)
        self.at("vetted to perfection")
        ck = check([CX + 0.55, 2.6, 0], GOLD)
        vet = T("vetted", 26, GOLD).next_to(ck, RIGHT, buff=0.15)
        self.play(Create(ck), pop(vet), Indicate(page, color=GOLD, scale_factor=1.03), run_time=0.6)

        # --- a single intellectual entity
        self.at("a colleague", lead=0.1)
        col = chip("a colleague", GREY, 26).move_to([CX, 2.65, 0])
        self.play(FadeOut(Group(find, ck, vet)), FadeOut(Group(page, bars, a1, a2)),
                  chm2.animate.move_to([CX - 1.0, 0.7, 0]), chs2.animate.move_to([CX + 1.0, 0.7, 0]), pop(col), run_time=0.6)
        self.at("single", lead=0.15)
        both = lab("Moore & Stein", GOLD, 40, fill=0.22).move_to([CX, 0.7, 0])
        ring = Ellipse(width=both.width + 1.0, height=both.height + 1.1, color=GOLD, stroke_width=3).move_to(both)
        self.play(ReplacementTransform(VGroup(chm2, chs2), both), Create(ring), run_time=0.7)
        one = T("a single intellectual entity", 34, GOLD, font=TITLE_FONT).move_to([CX, -1.35, 0])
        self.at("intellectual entity", lead=0.1)
        self.play(pop(one), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02: the analyzer
class S02Analyzer(BioScene):
    def construct(self):
        self.add_column()
        AY = 0.35
        title = lab("automated analyzer", GOLD, 30).move_to([CX, 2.75, 0])
        frame = RoundedRectangle(corner_radius=0.2, width=7.95, height=4.0, stroke_color=GOLD, stroke_width=2.5,
                                 fill_opacity=0).move_to([CX - 0.07, 0.3, 0]).set_stroke(opacity=0.55)
        self.at("automated analyzer", lead=0.0)
        self.play(pop(title), Create(frame), run_time=0.7)

        # synthetic resin column
        tx0, tx1 = -1.5, 1.1
        tube = RoundedRectangle(corner_radius=0.3, width=tx1 - tx0, height=1.6, stroke_color=GREY, stroke_width=4)
        tube.move_to([(tx0 + tx1) / 2, AY, 0])
        beads = VGroup(*[Circle(radius=0.05, stroke_width=0, fill_color=GREY, fill_opacity=0.5)
                         .move_to([tx0 + 0.25 + 0.2 * i, AY + dy, 0]) for i in range(12) for dy in (-0.5, -0.25, 0.0, 0.25, 0.5)])
        resin = T("synthetic resins", 26, GREY).move_to([(tx0 + tx1) / 2, AY - 1.45, 0])
        self.at("synthetic resins")
        self.play(Create(tube), FadeIn(beads), pop(resin), run_time=0.7)

        # amino acids: a mixture, then separated into bands
        rng = np.random.default_rng(4)
        groups = []
        for j in range(4):
            groups.append(VGroup(*[Dot(radius=0.1, color=GREEN) for _ in range(3)]))
        k = 0
        for g in groups:
            for d in g:
                d.move_to([tx0 + 0.3 + rng.random() * 0.8, AY - 0.5 + rng.random() * 1.0, 0]); k += 1
        aa = T("amino acids", 26, GREEN).move_to([(tx0 + tx1) / 2, AY + 1.6, 0])
        self.at("synthetic resins", nth=0, lead=-0.7)
        self.play(FadeIn(Group(*groups)), run_time=0.4)
        self.at("separate the")
        band_x = [-1.1, -0.45, 0.2, 0.85]
        moves = []
        for g, bx in zip(groups, band_x):
            for i, d in enumerate(g):
                moves.append(d.animate.move_to([bx, AY - 0.4 + 0.4 * i, 0]))
        self.play(LaggedStart(*moves, lag_ratio=0.05), pop(aa), run_time=1.4)

        # the readout side: recorder; the ninhydrin box
        rx0, rx1 = 3.45, 6.05
        rec = Rectangle(width=rx1 - rx0, height=2.3, stroke_color=GREY, stroke_width=3).move_to([(rx0 + rx1) / 2, AY, 0])
        rbase = AY - 1.15 + 0.35
        base = Line([rx0 + 0.15, rbase, 0], [rx1 - 0.15, rbase, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        det = T("each one detected", 24, PINK).move_to([(rx0 + rx1) / 2 - 0.2, AY - 1.45, 0])
        self.at("then detected")
        self.play(Create(rec), Create(base), run_time=0.5)
        self.at("each one")
        self.play(pop(det), run_time=0.4)
        nbox = RoundedRectangle(corner_radius=0.14, width=1.75, height=1.6, stroke_color=PINK, stroke_width=2.5,
                                fill_color=PINK, fill_opacity=0.14).move_to([2.28, AY, 0])
        nlab = T("ninhydrin", 26, PINK).move_to([2.28, AY + 0.45, 0])
        nin = VGroup(nbox, nlab)
        a_in = arr([tx1 + 0.03, AY, 0], [nbox.get_left()[0] - 0.02, AY, 0], GREY, 4, 0.5)
        a_out = arr([nbox.get_right()[0] + 0.02, AY, 0], [rx0 - 0.03, AY, 0], GREY, 4, 0.5)
        cc = T("color-changing", 24, PINK).move_to([2.12, AY + 1.12, 0])
        self.at("color changing")
        self.play(pop(cc), run_time=0.4)
        self.at("ninhydrin")
        self.play(FadeIn(nin, scale=0.9), GrowArrow(a_in), GrowArrow(a_out), run_time=0.5)

        # bands flow through ninhydrin, turn pink, and register as peaks
        mus = [0.2, 0.42, 0.64, 0.85]
        hts = [0.9, 1.5, 0.7, 1.2]
        trace = peaks(rx0 + 0.15, rx1 - 0.15, rbase, hts, mus, sig=0.035)
        self.at("reaction", lead=0.4)
        flows = []
        for g in reversed(groups):
            t1 = g.copy()
            for i, d in enumerate(t1):
                d.move_to([2.28 - 0.3 + 0.3 * i, AY - 0.4, 0])
            t2 = t1.copy().set_color(PINK)
            t3 = t2.copy()
            for i, d in enumerate(t3):
                d.move_to([rx0 + 0.6 + 0.3 * i, rbase + 0.1, 0]).set_opacity(0.0)
            flows.append(Succession(Transform(g, t1, run_time=0.6), Transform(g, t2, run_time=0.3),
                                    Transform(g, t3, run_time=0.6)))
        self.play(LaggedStart(*flows, lag_ratio=0.4, run_time=2.2), Create(trace, run_time=2.2, rate_func=linear))

        # --- ribonuclease
        self.at("ribonuclease", lead=0.55)
        self.play(FadeOut(Group(title, frame, tube, beads, resin, aa, rec, base, det, nin, a_in, a_out, cc, trace, *groups)), run_time=0.4)
        rib = lab("ribonuclease", BLUE, 40).move_to([CX, 2.3, 0])
        self.at("ribonuclease")
        self.play(FadeIn(rib, scale=0.9), run_time=0.5)

        # 124 amino acids as a chain of tiles
        rows, per = 4, 31
        s, gap = 0.2, 0.025
        tiles = VGroup()
        for r in range(rows):
            for c in range(per):
                t = Square(s, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
                t.move_to([CX - (per - 1) * (s + gap) / 2 + c * (s + gap), 0.95 - r * (s + gap), 0])
                tiles.add(t)
        for t in tiles:
            t.set_opacity(0)
        n = ValueTracker(0)
        w1 = M("124", 60, YELLOW).width
        aa2 = T("amino acids", 38, GREEN)
        x_start = CX - (w1 + 0.3 + aa2.width) / 2
        cnt = always_redraw(lambda: M(f"{int(round(n.get_value()))}", 60, YELLOW).move_to([x_start + w1 / 2, -0.7, 0]))
        aa2.move_to([x_start + w1 + 0.3 + aa2.width / 2, -0.72, 0])
        self.at("an enzyme of")
        self.add(cnt)
        self.at("124")
        self.play(LaggedStart(*[t.animate.set_fill(GREEN, 0.85) for t in tiles], lag_ratio=1 / 124),
                  n.animate.set_value(124), run_time=1.5, rate_func=linear)
        cnt.clear_updaters()
        self.play(pop(aa2), run_time=0.4)
        self.at("the first enzyme")
        endlab = T("the first enzyme read end to end", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.0, 0])
        self.play(pop(endlab), run_time=0.4)
        self.at("end to end", lead=1.2)
        self.play(LaggedStart(*[t.animate.set_fill(GOLD, 1.0) for t in tiles], lag_ratio=1 / 124), run_time=1.5, rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------- s03: coded message
class S03Message(BioScene):
    def construct(self):
        self.add_column()
        moore = chip("Moore", GOLD, 28).move_to([CX - 3.0, 2.85, 0])
        comp = T("compared", 26, GREY).next_to(moore, RIGHT, buff=0.25)
        self.play(pop(moore), pop(comp), run_time=0.5)

        n, s, gap = 10, 0.62, 0.1
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.09, width=s, height=s, stroke_color=GREEN, stroke_width=3,
                                          fill_color=GREEN, fill_opacity=0.18) for _ in range(n)]).arrange(RIGHT, buff=gap)
        tiles.move_to([CX, 1.4, 0])
        l1 = T("a protein's sequence", 30, GREEN).move_to([CX, 2.2, 0])
        self.at("protein sequence")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.1), pop(l1), run_time=1.0)
        l2 = T("a coded message", 34, GOLD, font=TITLE_FONT).move_to([CX, 2.2, 0])
        self.at("a coded message")
        self.play(ReplacementTransform(l1, l2), FadeOut(comp), FadeOut(moore), run_time=0.6)

        # dictates -> three-dimensional shape and function
        a_l = arr([CX - 0.4, 0.95, 0], [CX - 1.6, 0.15, 0], GOLD, 5, 0.4)
        dic = T("dictates", 26, GOLD).move_to([CX, 0.4, 0])
        self.at("dictates")
        self.play(GrowArrow(a_l), pop(dic), run_time=0.5)
        blob = VMobject(color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.18)
        ts = np.linspace(0, 2 * np.pi, 9)[:-1]
        pts = [[(0.95 + 0.28 * np.sin(3 * t + 0.6)) * np.cos(t) * 1.15, (0.95 + 0.25 * np.cos(2 * t)) * np.sin(t) * 0.8, 0] for t in ts]
        blob.set_points_smoothly([*pts, pts[0]])
        blob.move_to([CX - 1.6, -0.85, 0])
        shape = T("three-dimensional shape", 26, BLUE).next_to(blob, DOWN, buff=0.2)
        self.at("three dimensional")
        self.play(FadeIn(blob, scale=0.6), run_time=0.5)
        self.play(pop(shape), run_time=0.4)
        fn = lab("function", GOLD, 30).move_to([CX + 2.2, -0.85, 0])
        a_r = arr([CX + 0.4, 0.95, 0], [CX + 2.2, -0.3, 0], GOLD, 5, 0.35)
        self.at("function")
        self.play(GrowArrow(a_r), FadeIn(fn, scale=0.9), run_time=0.5)
        br = Brace(VGroup(blob, shape, fn), DOWN, color=GREY, buff=0.15)
        mach = T("the biological machine", 28, GREY).next_to(br, DOWN, buff=0.1)
        self.at("biological machine")
        self.play(GrowFromCenter(br), pop(mach), run_time=0.6)

        # now they could read it: a reading bar sweeps the code
        self.at("now they could")
        bar = Rectangle(width=s + 0.12, height=s + 0.3, stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to(tiles[0])
        rd = T("now they could read it", 28, GOLD, font=TITLE_FONT).move_to([CX, 2.95, 0])
        self.play(Create(bar), FadeOut(l2), run_time=0.3)
        self.play(pop(rd), run_time=0.3)
        self.at("read it", lead=0.1)
        self.play(bar.animate.move_to(tiles[-1]), run_time=0.8, rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------- s04: Stein
class S04Stein(BioScene):
    def construct(self):
        self.add_column()
        cm = chip("Moore", GOLD, 30).move_to([CX - 1.5, 1.7, 0])
        cs = chip("Stein", GOLD, 30).move_to([CX + 1.5, 1.7, 0])
        self.play(pop(cm), pop(cs), run_time=0.5)
        self.at("failed them")
        bodies = T("their bodies failed", 30, RED).move_to([CX, 0.7, 0])
        self.play(cm[0].animate.set_color(RED), cs[0].animate.set_color(RED), cm[1].animate.set_color(RED),
                  cs[1].animate.set_color(RED), pop(bodies), run_time=0.6)
        self.at("neither stopped")
        a1 = arr([CX - 1.5, 0.25, 0], [CX - 1.5, -0.95, 0], GOLD, 6, 0.3)
        a2 = arr([CX + 1.5, 0.25, 0], [CX + 1.5, -0.95, 0], GOLD, 6, 0.3)
        ns = T("neither stopped", 34, GOLD, font=TITLE_FONT).move_to([CX, -1.7, 0])
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.play(pop(ns), run_time=0.5)

        # --- Guillain-Barre, Stein
        self.at("Guillain", lead=0.5)
        self.play(FadeOut(Group(cm, cs, bodies, a1, a2, ns)), run_time=0.4)
        gb = lab("Guillain-Barré", RED, 32).move_to([CX - 2.4, 2.45, 0])
        self.at("Guillain")
        self.play(pop(gb), run_time=0.5)
        quad = lab(["Stein:", "quadriplegic"], RED, 28).move_to([CX + 2.5, 2.45, 0])
        a = arr(gb.get_right() + RIGHT * 0.1, quad.get_left() + LEFT * 0.1, RED, 5, 0.3)
        self.at("left Stein")
        self.play(GrowArrow(a), pop(quad), run_time=0.6)

        # he kept working
        kept = T("he kept going", 30, GOLD, font=TITLE_FONT).move_to([CX, 1.15, 0])
        self.at("He kept")
        self.play(pop(kept), run_time=0.4)
        c1 = lab("guiding his lab", GOLD, 28).move_to([CX - 2.3, 0.0, 0])
        c2 = lab("editing manuscripts", GOLD, 28).move_to([CX + 2.2, 0.0, 0])
        self.at("guiding his lab")
        self.play(pop(c1), run_time=0.45)
        self.at("editing manuscripts")
        self.play(pop(c2), run_time=0.45)
        gr = T("with gracious detail", 26, GOLD).next_to(c2, DOWN, buff=0.22)
        self.at("with gracious detail")
        self.play(pop(gr), run_time=0.4)
        c3 = lab("hosting seminars", GOLD, 28).move_to([CX - 2.3, -1.9, 0])
        home = lab("his apartment", TEAL, 28).move_to([CX + 2.2, -1.9, 0])
        fr = arr(c3.get_right() + RIGHT * 0.1, home.get_left() + LEFT * 0.1, GREY, 4, 0.3)
        frl = T("from", 24, GREY).next_to(fr, UP, buff=0.08)
        self.at("hosting seminars")
        self.play(pop(c3), run_time=0.45)
        self.at("from his apartment")
        self.play(GrowArrow(fr), pop(frl), pop(home), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s05: Moore, the mantra
class S05Moore(BioScene):
    def construct(self):
        self.add_column()
        als = lab("ALS", RED, 32).move_to([CX - 3.2, 2.85, 0])
        self.at("ALS", lead=0.0)
        self.play(pop(als), run_time=0.4)
        hands = lab("Moore's hands", RED, 32).move_to([CX + 0.3, 2.85, 0])
        took = arr(als.get_right() + RIGHT * 0.1, hands.get_left() + LEFT * 0.1, RED, 5, 0.3)
        self.at("took Moore's")
        self.play(GrowArrow(took), pop(hands), run_time=0.6)

        # once vs now
        hdr_l = T("once", 32, YELLOW, font=TITLE_FONT).move_to([CX - 2.1, 1.75, 0])
        hdr_r = T("now", 32, RED, font=TITLE_FONT).move_to([CX + 2.1, 1.75, 0])
        mid = Line([CX, 1.45, 0], [CX, -1.6, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.at("the same hands", lead=0.1)
        self.play(pop(hdr_l), pop(hdr_r), Create(mid), run_time=0.5)
        v = lab(["machined", "solenoid valves"], YELLOW, 28).move_to([CX - 2.1, 0.65, 0])
        self.at("machined")
        self.play(pop(v), run_time=0.45)
        tt = lab(["tuned gear-driven", "turntables"], YELLOW, 28).move_to([CX - 2.1, -0.9, 0])
        self.at("tuned")
        self.play(pop(tt), run_time=0.45)
        rest = lab(["resting in", "his lap"], RED, 28).move_to([CX + 2.1, 0.65, 0])
        self.at("now resting")
        self.play(pop(rest), run_time=0.45)
        still = lab(["an unwilling", "stillness"], RED, 28).move_to([CX + 2.1, -0.9, 0])
        self.at("unwilling stillness")
        self.play(pop(still), run_time=0.45)

        # --- the pen recorder
        self.at("while in the lab", lead=0.6)
        self.play(FadeOut(Group(als, took, hands, hdr_l, hdr_r, mid, v, tt, rest, still)), run_time=0.4)
        lab_box = RoundedRectangle(corner_radius=0.2, width=7.95, height=5.4, stroke_color=TEAL, stroke_width=2.5,
                                   fill_opacity=0).move_to([CX - 0.07, 0.4, 0]).set_stroke(opacity=0.55)
        lab_chip = lab("in the lab", TEAL, 28).move_to([-0.6, 2.4, 0])
        self.at("while in the lab", lead=0.0)
        self.play(Create(lab_box), pop(lab_chip), run_time=0.5)
        rx0, rx1, ry = 2.3, 6.0, 0.3
        rec = Rectangle(width=rx1 - rx0, height=3.4, stroke_color=GREY, stroke_width=3).move_to([(rx0 + rx1) / 2, ry, 0])
        base = Line([rx0 + 0.2, ry - 1.15, 0], [rx1 - 0.2, ry - 1.15, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        pen = T("pen recorder", 28, GREY).move_to([(rx0 + rx1) / 2, ry + 2.15, 0])
        self.at("a pen recorder")
        self.play(Create(rec), Create(base), pop(pen), run_time=0.6)
        tr = peaks(rx0 + 0.2, rx1 - 0.2, ry - 1.15, [1.1, 1.8, 0.85, 1.45, 0.65, 1.2], [0.1, 0.28, 0.45, 0.6, 0.76, 0.91], sig=0.03)
        self.at("traced peaks")
        self.play(Create(tr), run_time=1.1, rate_func=linear)
        logic = T("a molecular logic", 30, PINK, font=TITLE_FONT).move_to([(rx0 + rx1) / 2, ry - 1.95, 0])
        self.at("molecular logic")
        self.play(pop(logic), run_time=0.5)
        mh = lab("Moore's hands", RED, 28).move_to([-0.1, ry - 1.15, 0])
        reach = DashedLine(mh.get_right() + RIGHT * 0.05, [rx0 - 0.05, ry - 1.15, 0], color=RED, stroke_width=4, dash_length=0.12)
        self.at("could no longer")
        self.play(pop(mh), Create(reach), run_time=0.6)
        xm = xmark(reach.get_center(), RED)
        self.at("physically touch")
        self.play(FadeIn(xm, scale=1.5), run_time=0.3)

        # --- the mantra
        self.at("He lived by", lead=0.35)
        self.play(FadeOut(Group(lab_box, lab_chip, rec, base, pen, tr, logic, mh, reach, xm)), run_time=0.4)
        mant = T("his own quiet mantra", 36, GOLD, font=TITLE_FONT).move_to([CX, 2.95, 0])
        self.at("He lived by")
        self.play(pop(mant), run_time=0.6)
        mul = Line(mant.get_corner(DL) + DOWN * 0.1, mant.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=3)
        self.at("quiet")
        self.play(Create(mul), run_time=0.8)
        self.at("mantra")
        self.play(Indicate(mant, color=GOLD, scale_factor=1.06), run_time=0.7)
        inv = lab("the investigator", GREY, 28).move_to([CX, 1.8, 0])
        self.at("The investigator")
        self.play(pop(inv), run_time=0.45)
        d1 = lab("discovery", GREY, 30).move_to([CX - 1.9, 0.4, 0])
        d2 = lab("discovery", GREY, 30).move_to([CX + 1.9, 0.4, 0])
        da = arr(d1.get_right() + RIGHT * 0.1, d2.get_left() + LEFT * 0.1, GREY, 4, 0.3)
        self.at("move from discovery")
        self.play(pop(d1), run_time=0.4)
        self.at("to discovery")
        self.play(GrowArrow(da), pop(d2), run_time=0.5)
        cr = xmark(da.get_center(), RED, 0.3, 9)
        self.at("discovery", nth=1, lead=-0.1)
        self.play(FadeIn(cr, scale=1.5), d1.animate.set_opacity(0.5), d2.animate.set_opacity(0.5), da.animate.set_opacity(0.5), run_time=0.4)
        mv = T("he moves", 28, GOLD).move_to([CX, -0.75, 0])
        p1 = lab("problem", GOLD, 30).move_to([CX - 1.9, -1.8, 0])
        p2 = lab("problem", GOLD, 30).move_to([CX + 1.9, -1.8, 0])
        pa = arr(p1.get_right() + RIGHT * 0.1, p2.get_left() + LEFT * 0.1, GOLD, 6, 0.3)
        self.at("He moves")
        self.play(pop(mv), run_time=0.4)
        self.at("problem")
        self.play(pop(p1), run_time=0.4)
        self.at("to problem")
        self.play(GrowArrow(pa), pop(p2), run_time=0.5)
        self.play(Indicate(p2, color=GOLD, scale_factor=1.08), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s06: the quote
class S06Quote(BioScene):
    def construct(self):
        self.add_column()
        mark = T("“", 120, GOLD, font=TITLE_FONT)
        lines = [T("It was at Exeter that I was introduced", 32, TEXT, font=TITLE_FONT),
                 T("to standards of precision of writing, and of", 32, TEXT, font=TITLE_FONT),
                 T("work generally which I think has stood", 32, TEXT, font=TITLE_FONT),
                 T("me in very good stead.”", 32, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        fit(qg, max_w=7.2)
        qg.move_to([CX + 0.35, 0.45, 0])
        mark.scale(0.7).next_to(lines[0], LEFT, buff=0.1).align_to(lines[0], UP).shift(UP * 0.12)
        att = T("William Stein", 30, GOLD).next_to(qg, DOWN, buff=0.55).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.5)
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.8)
            self.wait(0.3)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s07: end card
class S07End(BioScene):
    def construct(self):
        img, border = portrait(height=2.0, center=(0, 2.1))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.1 - 1.0 - 0.3, 0])
        l1 = T("First automated amino acid analyzer; first complete", 38, font=TITLE_FONT)
        l2 = T("enzyme sequence, ribonuclease.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.35, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.55, 0])
        src = T("Source: The Molecule Hunters (v10) · Moore & Stein profile", 22, GREY).move_to([0, -2.4, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
