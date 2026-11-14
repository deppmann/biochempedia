"""Synthetic scenes for the layout check's regression suite (run_tests.py).

One FAIL scene per defect class the 2026-11-13 frame checkers found by eye, each with a clean PASS
twin that differs only in the fix the frame checker made. run_tests.py lists what each must report.
"""
from bp_parts import *  # noqa: F401,F403


class Base(NarratedScene):
    def hold(self, *mobs, t=1.0):
        self.add(*mobs)
        self.wait(t)


# ---- a label crossed by a non-text outline (cell membrane through 'cytoplasm')
class FailCovered(Base):
    def construct(self):
        cell = Ellipse(width=6, height=3.4, color=BLUE, stroke_width=5)
        self.hold(cell, T("cytoplasm", 30, BLUE).move_to([0, -1.7, 0]))


class PassCovered(Base):
    def construct(self):
        cell = Ellipse(width=6, height=3.4, color=BLUE, stroke_width=5)
        self.hold(cell, T("cytoplasm", 30, BLUE).move_to([0, -1.0, 0]))


# ---- a label inside a big ring is fine (the old bounding-box worry)
class PassInsideRing(Base):
    def construct(self):
        self.hold(Circle(radius=2.2, color=GREY, stroke_width=6), T("nucleus", 34).move_to(ORIGIN))


# ---- a chip straddles a panel border (letters clear, box on the line)
class FailStraddle(Base):
    def construct(self):
        panel = RoundedRectangle(width=8, height=4.5, corner_radius=0.2, stroke_color=TEAL, stroke_width=3)
        c = chip("matching", GOLD, 28).move_to(panel.get_top() + DOWN * 0.05 + LEFT * 1.5)
        self.hold(panel, c)


class PassStraddle(Base):
    def construct(self):
        panel = RoundedRectangle(width=8, height=4.5, corner_radius=0.2, stroke_color=TEAL, stroke_width=3)
        c = chip("matching", GOLD, 28).move_to(panel.get_top() + DOWN * 0.7 + LEFT * 1.5)
        self.hold(panel, c)


# ---- an arrow starts inside a chip, running into its letters' box
class FailArrowIntoChip(Base):
    def construct(self):
        c = chip("carbon compounds", BLUE, 28).move_to([-3, 1, 0])
        a = Arrow(c.get_center() + RIGHT * 0.9, [2, 1, 0], buff=0, color=GOLD)
        self.hold(c, a)


class PassArrowIntoChip(Base):
    def construct(self):
        c = chip("carbon compounds", BLUE, 28).move_to([-3, 1, 0])
        a = Arrow(c.get_right() + RIGHT * 0.1, [2, 1, 0], buff=0, color=GOLD)
        self.hold(c, a)


# ---- two chips overlap
class FailChipChip(Base):
    def construct(self):
        a = chip("PLANTS", GREEN, 28).move_to([-0.7, 0, 0])
        b = chip("FUNGI", GOLD, 28).next_to(a, RIGHT, buff=-0.15)
        self.hold(a, b)


class PassChipChip(Base):
    def construct(self):
        a = chip("PLANTS", GREEN, 28).move_to([-0.7, 0, 0])
        b = chip("FUNGI", GOLD, 28).next_to(a, RIGHT, buff=0.3)
        self.hold(a, b)


# ---- text wider than its pill
class FailOverflow(Base):
    def construct(self):
        pill = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.35, stroke_color=GREEN, stroke_width=3)
        self.hold(pill, T("people choose", 30, GREEN))


class PassOverflow(Base):
    def construct(self):
        pill = RoundedRectangle(width=3.4, height=0.7, corner_radius=0.35, stroke_color=GREEN, stroke_width=3)
        self.hold(pill, T("people choose", 30, GREEN))


# ---- a label past the frame edge
class FailEdge(Base):
    def construct(self):
        self.hold(T("CHEMOAUTOTROPH", 34).move_to([6.4, 2, 0]))


class PassEdge(Base):
    def construct(self):
        self.hold(T("CHEMOAUTOTROPH", 34).move_to([3.8, 2, 0]))


# ---- a picture shape cut by the frame edge (warning)
class FailShapeEdge(Base):
    def construct(self):
        self.hold(RoundedRectangle(width=2.5, height=1.2, stroke_color=BLUE).move_to([-6.6, -1, 0]))


class PassShapeEdge(Base):
    def construct(self):
        self.hold(RoundedRectangle(width=2.5, height=1.2, stroke_color=BLUE).move_to([-5.2, -1, 0]))


# ---- a label scaled below 22 pt with its group
class FailSmall(Base):
    def construct(self):
        g = VGroup(Square(2, color=GREEN), T("model", 28).shift(DOWN * 1.4)).scale(0.55)
        self.hold(g)


class PassSmall(Base):
    def construct(self):
        sq = Square(2, color=GREEN).scale(0.55)
        self.hold(sq, T("model", 28).next_to(sq, DOWN, buff=0.2))


# ---- an end-card line auto-shrunk below 22 pt
class FailEndCard(EndCard):
    LINE = "Genes that sort independently turn four sex-cell types into nine three three one chances every time."


class PassEndCard(EndCard):
    LINE = "Genes that sort independently make\nfour kinds of sex cell."


# ---- a shape poking out of its panel (fill below the glass)
class FailOutside(Base):
    def construct(self):
        glass = Rectangle(width=2, height=3.5, stroke_color=GREY, stroke_width=4)
        fill = Rectangle(width=1.8, height=2.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.7)
        fill.align_to(glass, DOWN).shift(DOWN * 0.35)
        self.hold(glass, fill)


class PassOutside(Base):
    def construct(self):
        glass = Rectangle(width=2, height=3.5, stroke_color=GREY, stroke_width=4)
        fill = Rectangle(width=1.8, height=2.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.7)
        fill.align_to(glass, DOWN).shift(UP * 0.08)
        self.hold(glass, fill)


# ---- poor contrast (gold on pale snow)
class FailContrast(Base):
    def construct(self):
        snow = Rectangle(width=9, height=3, stroke_width=0, fill_color="#F4F1EA", fill_opacity=1)
        self.hold(snow, T("harder or easier to spot?", 32, YELLOW))


class PassContrast(Base):
    def construct(self):
        snow = Rectangle(width=9, height=3, stroke_width=0, fill_color="#F4F1EA", fill_opacity=1).shift(DOWN * 1.5)
        self.hold(snow, T("harder or easier to spot?", 32, YELLOW).move_to([0, 2.4, 0]))


# ---- labels touching (near) and overlapping
class FailNear(Base):
    def construct(self):
        a = T("few blue cards", 30).move_to([0, 0, 0])
        b = T("shows in this individual", 30).next_to(a, DOWN, buff=0.02)
        self.hold(a, b)


class PassNear(Base):
    def construct(self):
        a = T("few blue cards", 30).move_to([0, 0, 0])
        b = T("shows in this individual", 30).next_to(a, DOWN, buff=0.3)
        self.hold(a, b)


class FailTextOverlap(Base):
    def construct(self):
        a = T("water gradient", 32).move_to([0, 0, 0])
        self.hold(a, T("wetter", 32).move_to(a.get_right() + DOWN * 0.1))


# ---- a cross-fade: the old caption has not gone before the new one arrives
class FailCrossfade(Base):
    def construct(self):
        old = T("1977 -> 1990", 32)
        new = T("Evidence changed the tree.", 32)
        self.add(old)
        self.wait(0.5)
        self.play(FadeOut(old), FadeIn(new), run_time=1.6)
        self.wait(0.5)


class PassCrossfade(Base):
    def construct(self):
        old = T("1977 -> 1990", 32)
        new = T("Evidence changed the tree.", 32)
        self.add(old)
        self.wait(0.5)
        self.play(swap(old, new, run_time=1.6))
        self.wait(0.5)


# ---- a token parked on a label for seconds while it moves (and comes to rest clear)
class FailMovingToken(Base):
    def construct(self):
        lab = T("host machinery", 30)
        dot = Dot([-3, 0, 0], radius=0.22, color=RED)
        self.add(lab, dot)
        self.play(dot.animate.move_to([3, 0, 0]), run_time=4, rate_func=linear)


class PassMovingToken(Base):
    def construct(self):
        lab = T("host machinery", 30)
        dot = Dot([-3, 0.8, 0], radius=0.22, color=RED)
        self.add(lab, dot)
        self.play(dot.animate.move_to([3, 0.8, 0]), run_time=4, rate_func=linear)


# ---- layout_ok: the same crossing, opted out on purpose, is not counted (it is listed as suppressed)
class PassLayoutOk(Base):
    def construct(self):
        lab = T("need does not change traits", 30)
        strike = Line(lab.get_left(), lab.get_right(), color=RED, stroke_width=5)
        strike.layout_ok = True
        self.hold(lab, strike)


# ---- a letter drawn in its block's own colour (hidden on purpose) is not checked
class PassHiddenLetter(Base):
    def construct(self):
        block = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
        self.hold(Line(LEFT * 3, RIGHT * 3, color=GREY, stroke_width=4), block, T("G", 28, PURPLE))


# ---- the boxed_label component cannot overflow: the fixed box that overflowed above grows to fit
class PassBoxedLabel(Base):
    def construct(self):
        self.hold(boxed_label("people choose", GREEN, size=30, box=(2.4, 0.7)))


# ---- tiles set edge to edge on purpose (a base pair) and a highlight frame on a grid cell are fine
class PassTiles(Base):
    def construct(self):
        a = boxed_label("A", GOLD, box=(0.6, 0.5))
        t = boxed_label("T", GOLD, box=(0.6, 0.5)).next_to(a, RIGHT, buff=0)
        cell = boxed_label("pp", TEXT, box=(1.2, 1.0)).move_to([3, 0, 0])
        hi = cell.box.copy().set_stroke(TEAL, 6)
        self.hold(a, t, cell, hi)
