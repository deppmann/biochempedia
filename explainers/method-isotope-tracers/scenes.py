"""Isotope tracers: following one atom through the cell  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = a radioactive label (marker with rays, hot spots, counts, the signal)
  PURPLE = a stable heavy label (nitrogen-15) and what the mass readout shows
  BLUE   = the detector (film, counter, mass spectrometer)
  GREY   = structure, natural unlabelled things, de-emphasised text
  ORANGE = protein (virus coat) and hot methanol (the solution that stops the cells)
  PINK   = DNA
  TEAL   = time
  GREEN  = the answer, a control, an identified compound
  RED    = leak, loss, the pitfall
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58CB5"


# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def rect(w, h, color=GREY, fill=0.10, sw=3, r=0.12, at=(0, 0)):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([at[0], at[1], 0])


def marker(kind, at, s=1.0):
    """A label marker: grey ring = natural atom, yellow disc with rays = radioactive, purple disc = stable heavy."""
    x, y = at
    if kind == "nat":
        return VGroup(Circle(radius=0.14 * s, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x, y, 0]))
    if kind == "heavy":
        return VGroup(Circle(radius=0.21 * s, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                             fill_opacity=0.95).move_to([x, y, 0]))
    g = VGroup(Circle(radius=0.13 * s, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, y, 0]))
    for k in range(8):
        a = k * np.pi / 4
        d = np.array([np.cos(a), np.sin(a), 0.0])
        g.add(Line(np.array([x, y, 0]) + d * 0.2 * s, np.array([x, y, 0]) + d * 0.34 * s, color=YELLOW, stroke_width=3))
    return g


def _p(p):
    return np.array([p[0], p[1], 0.0])


def DSH(a, b, **kw):
    return DashedLine(_p(a), _p(b), **kw)


def LN(a, b, **kw):
    return Line(_p(a), _p(b), **kw)


def chip2(l1, l2, color, size=26, pad=0.22):
    t = VGroup(T(l1, size, color), T(l2, size, color)).arrange(DOWN, buff=0.12)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, t.move_to(box))


def dot(at, r=0.1, color=YELLOW, op=1.0):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([at[0], at[1], 0])


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=6))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Following One Atom Through the Cell"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """The questions are about the fate of atoms; the isotope trick answers them: labelled A in, labelled B out."""

    def construct(self):
        px = [-4.45, 0.0, 4.45]
        pan = [rect(4.0, 5.6, GREY, 0.05, 2.5, 0.2, (x, 0.2)) for x in px]

        # panel 1: which molecule first
        c1 = [chip("start", GREY, 30), chip("?", YELLOW, 40), chip("?", YELLOW, 40), chip("?", YELLOW, 40)]
        g1 = VGroup(*c1).arrange(DOWN, buff=0.3).move_to([px[0], -0.35, 0])
        t1 = lab("made first?", 30, YELLOW).move_to([px[0], 2.4, 0])
        # panel 2: where a virus part ends up
        coat = chip("coat", ORANGE, 30)
        dna = chip("DNA", PINK, 30)
        virus = VGroup(coat, dna).arrange(RIGHT, buff=0.25).move_to([px[1], 1.4, 0])
        cellq = Circle(radius=1.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([px[1], -1.0, 0])
        qq = T("?", 56, YELLOW, weight=BOLD).move_to(cellq)
        a2 = arr([px[1], 0.85], [px[1], 0.2], GREY)
        t2 = lab("where does it end up?", 24, YELLOW).move_to([px[1], 2.4, 0])
        # panel 3: replaced?
        old = chip("body protein", GREY, 28)
        new = chip("?", YELLOW, 40)
        g3 = VGroup(old, new).arrange(DOWN, buff=1.1).move_to([px[2], 0.2, 0])
        a3 = arr([px[2], old.get_bottom()[1] - 0.1], [px[2], new.get_top()[1] + 0.1], GREY)
        t3 = lab("replaced?", 30, YELLOW).move_to([px[2], 2.4, 0])

        self.at("Which molecule")
        self.play(FadeIn(pan[0]), FadeIn(t1), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(c) for c in c1], lag_ratio=0.25), run_time=1.2)
        self.at("Where does part")
        self.play(FadeIn(pan[1]), FadeIn(t2), FadeIn(virus), run_time=0.5)
        self.play(FadeIn(cellq), FadeIn(a2), FadeIn(qq), run_time=0.6)
        self.at("Are the proteins")
        self.play(FadeIn(pan[2]), FadeIn(t3), FadeIn(old), run_time=0.5)
        self.play(GrowArrow(a3), FadeIn(new), run_time=0.6)

        self.at("These are questions")
        everything = VGroup(*pan, t1, g1, t2, virus, cellq, qq, a2, t3, g3, a3)
        self.play(FadeOut(everything), run_time=0.5)
        fate = T("the fate of atoms", 64, YELLOW, weight=BOLD).move_to([0, 0.9, 0])
        amt = T("amounts", 52, GREY).move_to([0, -1.3, 0])
        self.play(FadeIn(fate, shift=UP * 0.2), run_time=0.6)
        self.at("not about amounts")
        self.play(FadeIn(amt), run_time=0.4)
        x = cross(amt)
        self.play(Create(x), run_time=0.5)

        self.at("The answer is")
        self.play(FadeOut(fate), FadeOut(amt), FadeOut(x), run_time=0.4)
        ttl = T("the isotope trick", 40, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        A = chip("compound A", GREY, 48)
        B = chip("compound B", GREY, 48)
        A.move_to([-4.3, 0.2, 0])
        B.move_to([4.3, 0.2, 0])
        mid = [chip("?", GREY, 40).move_to([-1.2 + 2.4 * i, 0.2, 0]) for i in range(2)]
        self.play(FadeIn(ttl), run_time=0.4)
        self.at("Feed a")
        mA = marker("rad", [A.get_right()[0] - 0.35, A.get_top()[1] + 0.35], 1.4)
        self.play(FadeIn(A), run_time=0.4)
        self.play(FadeIn(mA, scale=1.5), run_time=0.5)
        self.play(*[FadeIn(m) for m in mid], run_time=0.5)
        self.at("Later isolate")
        self.play(FadeIn(B), run_time=0.4)
        mB = marker("rad", [B.get_right()[0] - 0.35, B.get_top()[1] + 0.35], 1.4)
        self.play(FadeIn(mB, scale=1.5), run_time=0.5)
        self.at("Then the conversion")
        ar = arr([A.get_right()[0] + 0.15, 0.2], [B.get_left()[0] - 0.15, 0.2], GREEN, 7, 0.32)
        ok = lab("conversion A to B established", 34, GREEN).move_to([0, -1.6, 0])
        self.play(FadeOut(VGroup(*mid)), run_time=0.3)
        self.play(GrowArrow(ar), run_time=0.8)
        self.at("is established")
        self.play(FadeIn(ok), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Label(SpokenScene):
    """One atom swapped for a radioactive or a stable heavy version; the cell cannot tell; a detector can."""

    def construct(self):
        # one compound chip with a marker slot
        def labelled(kind, x, y, name="compound"):
            c = chip(name, GREY, 34)
            c.move_to([x, y, 0])
            m = marker(kind, [c.get_right()[0] + 0.45, y], 1.5)
            return c, m

        c0, m0 = labelled("nat", 0, 1.9)
        self.at("Pick an isotope")
        self.play(FadeIn(c0, shift=DOWN * 0.2), FadeIn(m0), run_time=0.6)
        t0 = lab("one atom of an element it contains", 28, GREY).move_to([0, 3.1, 0])
        self.play(FadeIn(t0), run_time=0.4)

        self.at("radioactive")
        cr, mr = labelled("rad", -4.3, 1.9)
        self.play(c0.animate.shift(LEFT * 0), FadeIn(cr), FadeIn(mr, scale=1.6), run_time=0.7)
        tr = lab("radioactive", 28, YELLOW).next_to(cr, DOWN, buff=0.35).shift(RIGHT * 0.3)
        tr2 = lab("carbon-14, phosphorus-32", 22, GREY).next_to(tr, DOWN, buff=0.1)
        self.play(FadeIn(tr), FadeIn(tr2), run_time=0.4)

        self.at("stable and heavy")
        ch, mh = labelled("heavy", 3.7, 1.9)
        self.play(FadeIn(ch), FadeIn(mh, scale=1.6), run_time=0.7)
        th = lab("stable, heavy", 28, PURPLE).next_to(ch, DOWN, buff=0.35).shift(RIGHT * 0.3)
        th2 = lab("nitrogen-15", 22, GREY).next_to(th, DOWN, buff=0.1)
        self.play(FadeIn(th), FadeIn(th2), run_time=0.4)

        # the cell treats them the same
        self.at("The cell should treat")
        self.play(FadeOut(VGroup(t0, tr, tr2, th, th2)), run_time=0.3)
        cellbox = rect(12.4, 2.7, GREY, 0.08, 3, 0.5, (0, 0.15))
        celllab = lab("the cell", 28, GREY).move_to([-5.4, 1.75, 0])
        starts = [(-4.3, cr, mr), (0, c0, m0), (3.7, ch, mh)]
        anims = [FadeIn(cellbox), FadeIn(celllab)]
        moved = VGroup()
        for x, c, m in starts:
            anims += [c.animate.shift(DOWN * 1.2), m.animate.shift(DOWN * 1.2)]
        self.play(*anims, run_time=1.0)
        same = lab("treated like the natural molecule", 32, TEXT).move_to([0, -0.5, 0])
        self.play(FadeIn(same), run_time=0.4)

        self.at("essentially indistinguishable")
        eq = lab("essentially indistinguishable by the methods then used", 28, GREY).move_to([0, -1.75, 0])
        self.play(FadeIn(eq), run_time=0.5)

        self.at("could still be traced")
        self.play(FadeOut(eq), run_time=0.3)
        tell = lab("only the label shows", 30, BLUE).move_to([0, -1.75, 0])
        self.play(FadeIn(tell), run_time=0.3)
        det = chip("detector", BLUE, 36).move_to([0, -3.0, 0])
        beams = VGroup(arr([-1.3, -2.8], [-4.2, -1.3], BLUE, 5, 0.22), arr([1.3, -2.8], [4.2, -1.3], BLUE, 5, 0.22))
        self.play(FadeIn(det), FadeIn(beams), run_time=0.5)
        self.play(Indicate(mr, color=YELLOW, scale_factor=1.4), Indicate(mh, color=PURPLE, scale_factor=1.4), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PAPER_C = (0.0, -0.1)
PAPER_S = 5.7


def build_paper():
    """Chromatography paper with solvent arrows and spots (positions fixed, so the next scene can rebuild it)."""
    sheet = rect(PAPER_S, PAPER_S, TEXT, 0.12, 3, 0.06, PAPER_C)
    spots = VGroup()
    pts = [(-1.7, -1.6), (-0.3, -1.3), (-1.1, -0.2), (0.8, -0.6), (1.5, 0.5), (0.1, 0.8), (-1.5, 1.2), (1.2, 1.7), (-0.4, 1.9)]
    for (dx, dy) in pts:
        spots.add(dot([PAPER_C[0] + dx * 1.0, PAPER_C[1] + dy * 1.0 - 0.1], 0.17, YELLOW, 0.95))
    return sheet, spots


class S03Feed(SpokenScene):
    """Feed label, stop the cells at set times in hot methanol, then spread the extract on paper."""

    def construct(self):
        # flask of algae
        flask = Polygon([-5.0, 3.2, 0], [-5.0, 1.9, 0], [-6.5, -0.9, 0], [-3.5, -0.9, 0], [-4.5, 1.9, 0], [-4.5, 3.2, 0],
                        stroke_color=GREY, stroke_width=4, fill_color=TEAL, fill_opacity=0.10)
        cells = VGroup(*[Circle(radius=0.2, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.25)
                         .move_to([-5.65 + 0.42 * (i % 4) + 0.18 * (i // 4), -0.55 + 0.42 * (i // 4), 0]) for i in range(8)])
        fl = VGroup(lab("cells in", 26, GREY), lab("a flask", 26, GREY)).arrange(DOWN, buff=0.05).move_to([-5.0, -1.55, 0])
        tick_x = [-1.2, 1.9, 5.0]

        self.at("Feed the")
        self.play(FadeIn(flask), FadeIn(cells), FadeIn(fl), run_time=0.6)
        food = chip("labelled compound", YELLOW, 26).move_to([-5.0, 3.7, 0])
        self.play(FadeIn(food), run_time=0.4)
        self.play(food.animate.move_to([-5.0, 1.0, 0]).scale(0.6), run_time=0.7)
        self.play(FadeOut(food), run_time=0.5)

        # timeline
        self.at("Then stop")
        tl = LN([-6.4, -3.0, 0], [6.4, -3.0, 0], color=TEAL, stroke_width=4)
        tlab = lab("time", 26, TEAL).move_to([6.0, -3.45, 0])
        ticks = VGroup(*[LN([x, -2.85, 0], [x, -3.15, 0], color=TEAL, stroke_width=4) for x in tick_x])
        tnames = VGroup(*[lab(t, 26, TEAL).move_to([x, -3.45, 0]) for x, t in zip(tick_x, ["first", "next", "last"])])
        self.play(Create(tl), FadeIn(ticks), FadeIn(tlab), FadeIn(tnames), run_time=0.8)

        self.at("Calvin's group")
        fl2 = VGroup(lab("algae +", 26, YELLOW), lab("labelled carbon dioxide", 24, YELLOW)).arrange(DOWN, buff=0.05).move_to([-5.0, -1.55, 0])
        self.play(Transform(fl, fl2), run_time=0.5)
        pulse = LN([-6.4, -3.0, 0], [-6.4, -3.0, 0], color=YELLOW, stroke_width=10)
        pulse_t = lab("labelled pulse", 24, YELLOW).move_to([-3.8, -2.5, 0])
        fall = [dot([-5.5 + 0.55 * i, 3.9 + 0.35 * (i % 2), 0], 0.14, YELLOW) for i in range(6)]
        self.add(*fall)
        self.play(LaggedStart(*[d.animate.move_to([d.get_center()[0], 0.2, 0]) for d in fall], lag_ratio=0.25),
                  cells.animate.set_fill(YELLOW, 0.55), FadeIn(pulse_t),
                  Transform(pulse, LN([-6.4, -3.0, 0], [-1.2, -3.0, 0], color=YELLOW, stroke_width=10)), run_time=3.6)
        self.play(*[FadeOut(d) for d in fall], run_time=0.3)

        self.at("They took samples")
        beakers = VGroup()
        samples = []
        for x in tick_x:
            beakers.add(rect(2.2, 3.0, ORANGE, 0.06, 3, 0.12, (x, -0.7)))
        self.play(FadeIn(beakers), run_time=0.5)
        sl = lab("hot methanol", 28, ORANGE).move_to([tick_x[1], 1.1, 0])
        self.play(FadeIn(sl), run_time=0.3)
        self.at("short exposures")
        for i, x in enumerate(tick_x):
            d = dot([-3.9, 2.4], 0.22, YELLOW)
            self.add(d)
            self.play(d.animate.move_to([x, 2.4, 0]), run_time=0.45, rate_func=smooth)
            self.play(d.animate.move_to([x, 0.1, 0]), run_time=0.35)
            self.play(d.animate.scale(2.4).set_opacity(0.45), run_time=0.25)
            samples.append(d)

        self.at("which stopped")
        stop = lab("all enzyme reactions stop", 30, ORANGE).move_to([0.9, 3.3, 0])
        self.play(FadeIn(stop), run_time=0.5)

        # paper
        self.at("Then they separated")
        everything = VGroup(flask, cells, fl, tl, tlab, ticks, tnames, beakers, sl, stop, pulse, pulse_t, *samples)
        self.play(FadeOut(everything), run_time=0.5)
        sheet, spots = build_paper()
        a_bot = arr([PAPER_C[0] - 2.9, PAPER_C[1] - 3.15 + 0.15 + 0.0], [PAPER_C[0] + 2.9, PAPER_C[1] - 3.15 + 0.15], BLUE, 5)
        a_left = arr([PAPER_C[0] - 3.15, PAPER_C[1] - 2.85], [PAPER_C[0] - 3.15, PAPER_C[1] + 2.85], BLUE, 5)
        self.play(FadeIn(sheet), run_time=0.4)
        l1 = lab("solvent 1", 24, BLUE).next_to(a_bot, RIGHT, buff=0.15)
        self.play(GrowArrow(a_bot), FadeIn(l1), run_time=0.6)
        self.at("dimensional paper")
        l2 = lab("solvent 2", 24, BLUE).rotate(PI / 2).next_to(a_left, LEFT, buff=0.15)
        self.play(GrowArrow(a_left), FadeIn(l2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in spots], lag_ratio=0.15), run_time=1.6)
        pl = lab("each spot: one product", 28, TEXT).move_to([5.0, 1.0, 0])
        sch = lab("schematic", 26, GREY).move_to([5.0, 2.3, 0])
        self.play(FadeIn(pl), FadeIn(sch), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Detect(SpokenScene):
    """Three readouts: film (autoradiography), counter, mass spectrometer."""

    def construct(self):
        px = [-4.45, 0.0, 4.45]
        pan = [rect(4.1, 5.9, BLUE, 0.04, 2.5, 0.2, (x, -0.15)) for x in px]
        hdr = [lab(t, 28, BLUE).move_to([x, 2.5, 0]) for x, t in zip(px, ["film", "counter", "mass"])]

        self.at("Now find")
        self.play(*[FadeIn(p) for p in pan], run_time=0.5)
        self.play(*[FadeIn(h) for h in hdr], run_time=0.4)

        # panel 1: paper over film
        film = rect(3.4, 1.9, BLUE, 0.35, 3, 0.06, (px[0], -1.0))
        film_lab = lab("X-ray film", 24, BLUE).move_to([px[0], -2.3, 0])
        sheet = rect(3.4, 1.9, TEXT, 0.12, 3, 0.06, (px[0], 1.15))
        sp = [(-0.9, 0.35), (0.2, -0.3), (0.9, 0.45), (-0.2, 0.55)]
        spots = VGroup(*[dot([px[0] + dx, 1.15 + dy], 0.14, YELLOW) for dx, dy in sp])
        self.at("Radioactive decay")
        self.play(FadeIn(sheet), FadeIn(spots), FadeIn(film), FadeIn(film_lab), run_time=0.6)
        rays = VGroup()
        for dx, dy in sp:
            for k in (-1, 1):
                rays.add(arr([px[0] + dx, 1.15 + dy - 0.2], [px[0] + dx + 0.18 * k, 1.15 + dy - 0.9], YELLOW, 3, 0.12))
        self.play(FadeIn(rays), run_time=0.5)
        self.at("Lay the paper")
        self.play(FadeOut(rays), VGroup(sheet, spots).animate.shift(DOWN * 2.15), run_time=0.8)
        self.at("darkens the developed")
        # developed film shows the same spots, bright where label was
        dev = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color="#06080c", fill_opacity=0.95)
                       .move_to([px[0] + dx, -1.0 + dy, 0]) for dx, dy in sp])
        self.play(FadeOut(sheet), FadeOut(spots), film.animate.set_fill("#d5dbe3", 0.95), FadeIn(dev), run_time=0.8)
        dl = lab("a dark spot per product", 24, TEXT).move_to([px[0], -2.8, 0])
        self.play(FadeIn(dl), run_time=0.3)

        # panel 2: counter
        self.at("Or count")
        tube = chip("purified fraction", YELLOW, 24).move_to([px[1], 1.3, 0])
        counter = rect(3.3, 1.9, BLUE, 0.12, 3, 0.15, (px[1], -1.0))
        cl = lab("counter", 24, BLUE).move_to([px[1], -1.0, 0])
        a = arr([px[1], 0.75], [px[1], -0.0], GREY, 4)
        self.play(FadeIn(tube), run_time=0.4)
        self.play(GrowArrow(a), FadeIn(counter), FadeIn(cl), run_time=0.5)
        self.at("scintillation counter")
        cnt = M("counts 0", 30, YELLOW).move_to([px[1], -2.35, 0])
        self.play(FadeIn(cnt), run_time=0.3)
        for v in (112, 340, 586):
            self.play(Transform(cnt, M(f"counts {v}", 30, YELLOW).move_to([px[1], -2.35, 0])), run_time=0.3)
        ex = lab("example", 22, GREY).move_to([px[1], -2.85, 0])
        self.play(FadeIn(ex), run_time=0.2)

        # panel 3: mass
        self.at("A stable isotope")
        base = LN([px[2] - 1.5, -1.7, 0], [px[2] + 1.5, -1.7, 0], color=GREY, stroke_width=3)
        self.play(Create(base), run_time=0.4)
        self.at("Nitrogen 15")
        gas = chip("sample's nitrogen", PURPLE, 24).move_to([px[2], 1.7, 0])
        self.play(FadeIn(gas), run_time=0.4)
        self.at("into")
        gas2 = chip("N2 gas", PURPLE, 28).move_to([px[2], 1.7, 0])
        self.play(Transform(gas, gas2), run_time=0.6)
        self.at("mass 28")
        ms = lab("mass spectrometer", 24, BLUE).move_to([px[2], 0.95, 0])
        exm = lab("example", 22, GREY).move_to([px[2], -2.85, 0])
        self.play(FadeIn(ms), FadeIn(exm), run_time=0.4)
        b28 = Rectangle(width=0.7, height=2.2, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.55) \
            .move_to([px[2] - 0.95, -1.7 + 1.1, 0])
        l28 = VGroup(M("14N14N", 20, GREY), lab("mass 28", 20, GREY)).arrange(DOWN, buff=0.04).move_to([px[2] - 0.95, -2.2, 0])
        self.play(GrowFromEdge(b28, DOWN), FadeIn(l28), run_time=0.6)
        self.at("with mass 29")
        b29 = Rectangle(width=0.7, height=1.1, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.7) \
            .move_to([px[2] + 0.95, -1.7 + 0.55, 0])
        l29 = VGroup(M("14N15N", 20, PURPLE), lab("mass 29", 20, PURPLE)).arrange(DOWN, buff=0.04).move_to([px[2] + 0.95, -2.2, 0])
        self.play(GrowFromEdge(b29, DOWN), FadeIn(l29), run_time=0.6)
        self.at("in a mass spectrometer")
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """Spots and counts show label, not total; then Shemin's red-cell time course."""

    def construct(self):
        strip = rect(10.4, 2.4, BLUE, 0.9, 3, 0.1, (0, 1.4)).set_fill("#d5dbe3", 0.92)
        shades = [0.3, 1.0, 0.62]
        sx = [-3.4, 0.0, 3.4]
        spots = VGroup(*[Circle(radius=0.62, stroke_width=0, fill_color="#06080c", fill_opacity=o).move_to([x, 1.4, 0])
                         for x, o in zip(sx, shades)])
        names = VGroup(*[lab(t, 30, YELLOW).move_to([x, -0.2, 0]) for x, t in zip(sx, ["a little label", "a lot of label", "some label"])])
        bars = VGroup(*[Rectangle(width=0.5, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
                        .move_to([x, -1.3 - (2.0 - h) / 2 + 0.0, 0]) for x, h in zip(sx, [0.5, 1.7, 0.95])])
        self.at("A dark spot")
        self.play(FadeIn(strip), FadeIn(spots), run_time=0.5)
        self.at("high count")
        self.play(FadeIn(bars), FadeIn(names), run_time=0.7)
        self.at("Its intensity")
        key = lab("intensity tracks how much label", 34, YELLOW).move_to([0, -3.2, 0])
        self.play(FadeIn(key), run_time=0.5)
        self.at("not how much")
        self.play(Transform(key, lab("not the total amount of the molecule", 34, GREY).move_to([0, -3.2, 0])), run_time=0.6)

        # Shemin
        self.at("Here is")
        self.play(FadeOut(VGroup(strip, spots, names, bars, key)), run_time=0.5)
        x0, y0 = -5.4, -2.5
        xs = lambda d: x0 + 10.4 * d / 160.0
        ya = arr([x0, y0], [x0, 2.9], GREY, 4)
        xa = arr([x0, y0], [x0 + 11.2, y0], GREY, 4)
        xl = lab("time", 26, GREY).move_to([x0 + 9.8, y0 - 0.45, 0])
        yl = lab("15N label in heme", 26, PURPLE).move_to([-3.7, 3.45, 0])
        ex = lab("schematic", 26, GREY).move_to([4.6, 3.45, 0])
        self.play(GrowArrow(ya), GrowArrow(xa), FadeIn(xl), FadeIn(yl), FadeIn(ex), run_time=0.7)
        top = 1.9
        t_exp = lab("took nitrogen-15 glycine for 3 days", 28, PURPLE).move_to([-0.3, 0.6, 0])
        self.at("for three days")
        self.play(FadeIn(t_exp), run_time=0.4)
        self.at("rose to a maximum")
        ds = np.linspace(0, 20, 30)
        rise = poly([[xs(d), y0 + (top - y0) * (1 - np.exp(-4.0 * d / 20)) / (1 - np.exp(-4.0))] for d in ds], PURPLE, 6)
        self.play(Create(rise, rate_func=linear), run_time=1.3)
        self.at("stayed nearly level")
        flat = poly([[xs(20), top], [xs(100), top]], PURPLE, 6)
        self.play(Create(flat, rate_func=linear), run_time=1.1)
        br = BraceBetweenPoints([xs(100), top + 0.15, 0], [xs(20), top + 0.15, 0], color=PURPLE)
        brl = lab("nearly level for months", 26, PURPLE).next_to(br, UP, buff=0.1)
        self.play(FadeIn(br), FadeIn(brl), FadeOut(t_exp), run_time=0.5)
        self.at("then fell")
        ds = np.linspace(100, 142, 30)
        fall = poly([[xs(d), y0 + (top - y0) * (1 - ((d - 100) / 42) ** 1.6 * 0.97)] for d in ds], PURPLE, 6)
        self.play(Create(fall, rate_func=linear), run_time=1.0)
        self.at("That gave")
        res = chip2("red-cell life span:", "about 127 days (average)", GREEN, 30).move_to([-1.3, -0.4, 0])
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Label spreads into another compound (control: identify it); half-life limits timing."""

    def construct(self):
        # left: Hokin and Hokin
        ttl = lab("label followed into RNA", 30, YELLOW).move_to([-0.2, 3.2, 0])
        base = LN([-3.0, -1.7, 0], [2.8, -1.7, 0], color=GREY, stroke_width=3)
        H = 3.4
        b1 = Rectangle(width=1.5, height=H, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.8) \
            .move_to([-2.0, -1.7 + H / 2, 0])
        n1 = lab("counts in RNA", 24, YELLOW).move_to([-2.0, -2.1, 0])
        b2 = Rectangle(width=1.5, height=0.01, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.8) \
            .move_to([1.3, -1.7 + 0.005, 0])
        n2 = lab("discarded", 24, RED).move_to([1.3, -2.1, 0])

        self.at("A label marks")
        self.play(FadeIn(ttl), Create(base), GrowFromEdge(b1, DOWN), FadeIn(n1), run_time=0.8)
        anyc = VGroup(*[chip(t, GREY, 22) for t in ("molecule", "molecule", "molecule")]).arrange(RIGHT, buff=0.75).move_to([-0.2, 2.2, 0])
        mks = VGroup(*[marker("rad", [c.get_right()[0] + 0.3, c.get_center()[1]], 0.8) for c in anyc])
        self.at("anything that")
        self.play(FadeIn(anyc), run_time=0.4)
        self.play(*[FadeIn(m, scale=1.5) for m in mks], run_time=0.6)
        self.at("tried to follow")
        self.play(FadeOut(anyc), FadeOut(mks), run_time=0.3)
        self.at("vanishing in purification")
        pur = lab("purification", 22, GREY).move_to([-0.35, -0.2, 0])
        ar = arr([-1.0, -0.6], [0.3, -0.6], GREY, 4)
        self.play(FadeIn(pur), GrowArrow(ar), run_time=0.4)
        b1b = Rectangle(width=1.5, height=1.1, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.8) \
            .move_to([-2.0, -1.7 + 0.55, 0])
        b2b = Rectangle(width=1.5, height=H - 1.1, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.8) \
            .move_to([1.3, -1.7 + (H - 1.1) / 2, 0])
        self.play(Transform(b1, b1b), Transform(b2, b2b), FadeIn(n2), run_time=1.2)
        self.at("phospholipid")
        pl = chip("phospholipid", RED, 28).move_to([1.3, 1.3, 0])
        self.play(FadeIn(pl, shift=DOWN * 0.2), run_time=0.5)
        self.at("So identify")
        ctl = chip2("control: run the labelled compound", "beside an authentic standard", GREEN, 26).move_to([-0.2, -3.0, 0])
        self.play(FadeIn(ctl, shift=UP * 0.2), run_time=0.6)

        # right: half-life
        self.at("life is part")
        left = VGroup(ttl, base, b1, b2, n1, n2, pur, ar, pl, ctl)
        self.play(left.animate.shift(LEFT * 3.2), run_time=0.7)
        ox, oy = 1.3, -2.0
        xa = arr([ox, oy], [ox + 5.2, oy], GREY, 4)
        ya = arr([ox, oy], [ox, 2.9], GREY, 4)
        xl = lab("time", 24, GREY).move_to([ox + 4.6, oy - 0.4, 0])
        yl = lab("activity left", 24, YELLOW).move_to([ox + 1.2, 3.2, 0])
        self.play(GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl), run_time=0.6)
        tf = lambda t: [ox + 0.1 + 4.6 * t / 43.0, oy + 4.6 * 2 ** (-t / 14.3) * 0.82]
        tt = np.linspace(0, 43, 40)
        curve = poly([tf(t) for t in tt], YELLOW, 6)
        self.play(Create(curve, rate_func=linear), run_time=1.0)
        self.at("loses half")
        p1 = tf(14.3)
        hline = DSH([ox, p1[1], 0], [p1[0], p1[1], 0], color=GREY, stroke_width=2)
        vline = DSH([p1[0], oy, 0], [p1[0], p1[1], 0], color=GREY, stroke_width=2)
        half = lab("half", 26, GREY).move_to([ox - 0.45, p1[1], 0])
        self.play(Create(hline), Create(vline), FadeIn(half), run_time=0.6)
        self.at("about 14 days")
        d14 = lab("about 14 days", 26, YELLOW).move_to([p1[0], oy - 0.45, 0])
        ex = lab("idealised, phosphorus-32", 22, GREY).move_to([ox + 3.2, 1.6, 0])
        self.play(FadeIn(d14), FadeIn(ex), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Calvin(SpokenScene):
    """Calvin pulse: first product appears first; Schoenheimer: body constituents are renewed."""

    def construct(self):
        # row 1
        tag1 = lab("Calvin, Benson, Bassham  |  Berkeley, late 1940s to 1953", 26, GOLD).move_to([0, 3.3, 0])
        px = [-4.3, 0.0, 4.3]
        plates = VGroup(*[rect(3.7, 1.8, BLUE, 0.2, 3, 0.08, (x, 1.75)) for x in px])
        cap = VGroup(*[lab(t, 24, TEAL).move_to([x, 0.6, 0]) for x, t in zip(px, ["shortest exposure", "longer", "longer still"])])
        spot_sets = [
            [(0.0, 0.0), (-1.1, 0.45), (1.15, -0.4)],
            [(-0.9, 0.0), (0.5, 0.45), (0.9, -0.35), (0.2, -0.45)],
            [(0.0, 0.0), (-1.0, 0.4), (1.0, -0.3), (-0.5, -0.4), (0.6, 0.45), (-1.3, -0.25), (1.3, 0.35), (-0.2, 0.55)],
        ]
        sizes = [[0.3, 0.07, 0.07], [0.2, 0.22, 0.2, 0.2], [0.12] * 8]
        sp = VGroup(*[VGroup(*[dot([x + dx, 1.75 + dy], r, YELLOW, (0.28 if (k > 0 and ii == 0) else 1.0)) for k, ((dx, dy), r) in enumerate(zip(st, sz))])
                      for ii, (x, st, sz) in enumerate(zip(px, spot_sets, sizes))])
        pga = VGroup(lab("PGA", 22, GREEN).move_to([px[0] + 0.85, 1.75, 0]), lab("PGA", 22, GREEN).move_to([px[1] - 0.9, 2.25, 0]))
        first = chip("3-phosphoglyceric acid (PGA): first stable product", GREEN, 24).move_to([-2.4, -0.2, 0])

        self.play(FadeIn(tag1), FadeIn(plates[0]), FadeIn(cap[0]), FadeIn(sp[0]), run_time=0.6)
        self.at("In a fraction")
        self.play(FadeIn(pga[0]), FadeIn(first, shift=UP * 0.2), Indicate(sp[0][0], color=GREEN, scale_factor=1.6), run_time=0.7)
        self.at("A short pulse")
        self.play(FadeIn(plates[1]), FadeIn(cap[1]), FadeIn(sp[1]), FadeIn(pga[1]), run_time=0.6)
        self.play(FadeIn(plates[2]), FadeIn(cap[2]), FadeIn(sp[2]), run_time=0.6)
        ordr = chip("schematic", GOLD, 30).move_to([5.0, -0.2, 0])
        self.play(FadeIn(ordr), run_time=0.4)

        # row 2
        self.at("found that many")
        tag2 = lab("Schoenheimer and Rittenberg  |  from 1935", 26, GOLD).move_to([0, -1.05, 0])
        self.play(FadeIn(tag2), run_time=0.4)
        chips = VGroup(*[chip("body", GREY, 28) for _ in range(6)]).arrange(RIGHT, buff=0.35).move_to([0, -2.1, 0])
        self.play(FadeIn(chips), run_time=0.5)
        self.at("constant renewal")
        order = [2, 0, 4, 1, 5, 3]
        for k in order[:3]:
            self.play(chips[k][0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.45),
                      chips[k][1].animate.set_color(PURPLE), run_time=0.35)
        self.at("Only a label")
        for k in order[3:5]:
            self.play(chips[k][0].animate.set_stroke(PURPLE).set_fill(PURPLE, 0.45),
                      chips[k][1].animate.set_color(PURPLE), run_time=0.3)
        leg = VGroup(chip("old", GREY, 24), chip("new, labelled", PURPLE, 24)).arrange(RIGHT, buff=0.5).move_to([0, -3.15, 0])
        self.play(FadeIn(leg), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Hershey(SpokenScene):
    """Hershey and Chase: DNA enters, coat stays outside; then the rule."""

    def construct(self):
        tag = lab("Hershey and Chase, 1952", 28, GOLD).move_to([0, 3.3, 0])
        coat = chip("protein coat", ORANGE, 32).move_to([-4.6, 1.2, 0])
        dna = chip("DNA", PINK, 32).move_to([-4.6, -0.9, 0])
        vlab = lab("T2 phage, two parts", 26, GREY).move_to([-4.6, 2.35, 0])
        bact = Circle(radius=2.45, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to([3.1, -0.25, 0])
        blab = lab("bacterium", 28, GREY).move_to([3.1, -3.15, 0])

        self.at("Hershey and Chase")
        self.play(FadeIn(tag), FadeIn(coat), FadeIn(dna), FadeIn(vlab), run_time=0.7)
        self.play(FadeIn(bact), FadeIn(blab), run_time=0.5)
        self.at("marks protein")
        mS = marker("rad", [coat.get_right()[0] + 0.5, coat.get_center()[1]], 1.4)
        sl = lab("sulfur-35", 24, YELLOW).next_to(mS, RIGHT, buff=0.15)
        self.play(FadeIn(mS, scale=1.6), FadeIn(sl), run_time=0.6)
        self.at("ends up mostly")
        mP = marker("rad", [dna.get_right()[0] + 0.5, dna.get_center()[1]], 1.4)
        pl = lab("phosphorus-32", 24, YELLOW).next_to(mP, RIGHT, buff=0.15)
        self.play(FadeIn(mP, scale=1.6), FadeIn(pl), run_time=0.6)

        self.at("Most phage DNA")
        self.play(FadeOut(sl), FadeOut(pl), FadeOut(vlab), run_time=0.3)
        gdna = VGroup(dna, mP)
        left_dot = dot([-4.3, -1.7], 0.2, YELLOW)
        left_lab = lab("a little stays outside", 22, GREY).move_to([-3.9, -2.15, 0])
        self.play(FadeIn(left_dot), FadeIn(left_lab), run_time=0.3)
        most_in = lab("most enters", 26, PINK).move_to([3.1, -1.2, 0])
        self.play(gdna.animate.move_to([3.1, -0.6, 0]), run_time=1.3)
        self.play(FadeIn(most_in), run_time=0.3)
        self.at("Most of the")
        gcoat = VGroup(coat, mS)
        self.play(gcoat.animate.move_to([-1.55, 1.2, 0]), run_time=1.0)
        outl = lab("most stays outside", 26, ORANGE).move_to([-1.55, 0.35, 0])
        cross_dot = VGroup(Rectangle(width=0.32, height=0.24, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([0.05, 1.2, 0]), dot([0.38, 1.2], 0.2, YELLOW))
        self.play(FadeIn(outl), FadeIn(cross_dot), run_time=0.4)
        cross_lab = lab("a little crosses", 22, GREY).move_to([3.1, -2.15, 0])
        self.play(cross_dot.animate.shift([2.0, -2.95, 0]), FadeIn(cross_lab), run_time=1.0)
        self.at("The cells still")
        kids = VGroup(*[chip("new phage", GREEN, 24) for _ in range(2)]).arrange(DOWN, buff=0.2).move_to([3.1, 0.95, 0])
        self.play(LaggedStart(*[FadeIn(k, scale=0.6) for k in kids], lag_ratio=0.3), run_time=0.9)
        self.at("The authors warned")
        warn = lab("no further chemical inferences", 26, GREY).move_to([-3.4, -2.9, 0])
        self.play(FadeIn(warn), run_time=0.5)

        self.at("Keep this rule")
        everything = VGroup(tag, coat, dna, mS, mP, bact, blab, outl, kids, warn, left_dot, cross_dot, left_lab, cross_lab, most_in)
        r1 = T("A label shows where atoms went.", 48, GOLD, font=TITLE_FONT)
        r2 = T("Identify the compound before you conclude.", 40, TEXT, font=TITLE_FONT)
        g = VGroup(r1, r2).arrange(DOWN, buff=0.5).move_to([0, 0.2, 0])
        box = rect(g.width + 0.9, g.height + 0.9, GOLD, 0.06, 3, 0.2, (0, 0.2))
        who = lab("Hershey and Chase, 1952", 26, GOLD).next_to(box, DOWN, buff=0.3)
        self.play(FadeOut(everything), FadeIn(box), FadeIn(who), run_time=0.5)
        self.at("A label shows")
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.6)
        self.at("Identify the compound")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S09End(EndCard):
    LINE = "A label shows where atoms went. Identify the compound before you conclude."
