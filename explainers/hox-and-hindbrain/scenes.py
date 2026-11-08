"""Chapter 1 of "Head to Tail: Hox Genes, Retinoic Acid and Rhombomeres": Two Segments, Two Jobs.

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by all chapters; taken from scenes.old.py, extended)
  ORANGE = retinoic acid (the signal, the gradient, the dose)
  GREEN  = made / switched on (Raldh2, a gene that is on, the right dose)
  RED    = destroyed / harmful (Cyp26, the wrong dose)
  BLUE   = the retinoic acid receptors (RAR, RXR)
  PURPLE = Hox genes and the Hox code (every Hox dot is one purple; the seven MIX shades are each
           rhombomere's own combination, light = more anterior code, dark = more posterior code)
  GOLD   = tracer dye and labelled cells (clones), exit stubs, card outlines
  TEAL   = trigeminal identity (V, jaw muscles)
  YELLOW = facial identity (VII, second-arch muscles; face in mammals)
  PINK   = glossopharyngeal identity (IX, swallowing)
  WHITE (TEXT) = segment genes (Krox20, MafB) and neutral highlights
  GREY   = bulges (rhombomeres), labels, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB0"
MIX = ["#EDE2FA", "#D7C1F0", "#C1A0E6", "#AB80DB", "#9461CC", "#7C46B5", "#64339A"]

# the hindbrain row (map scenes): r1..r7 centres
SX = [-4.8 + 1.6 * i for i in range(7)]
SW = 1.4


class Sc(SpokenScene):
    def until(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)


def bulge(i, fill=GREY, op=0.15, stroke=GREY, sw=3, h=3.2, y=0.6, w=SW):
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=stroke, stroke_width=sw,
                            fill_color=fill, fill_opacity=op).move_to([SX[i], y, 0])


def strip(h=3.2, y=0.6, **kw):
    return VGroup(*[bulge(i, h=h, y=y, **kw) for i in range(7)])


def rlabels(bs, color=GREY, size=26):
    return VGroup(*[T(f"r{i + 1}", size, color).move_to(b.get_top() + DOWN * 0.34) for i, b in enumerate(bs)])


def fill_to(b, color, op=0.25, sw=5):
    return b.animate.set_stroke(color, sw).set_fill(color, op)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def species(txt):
    """Persistent species tag, top-left corner."""
    m = chip(txt, GREY, 28, pad=0.14, fill_opacity=0.06)
    return m.move_to([-6.65 + m.width / 2, 3.36, 0])


# ---- icons (outlines of muscles, plain shapes) -----------------------------------------------------
def jaw_icon(color=GREY, sw=5):
    xs = np.linspace(-1, 1, 25)
    outer = VMobject(stroke_color=color, stroke_width=sw)
    outer.set_points_smoothly([np.array([x, 0.9 * x * x - 0.55, 0]) for x in xs])
    teeth = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.17, height=0.2, stroke_width=0,
                                      fill_color=color, fill_opacity=0.9)
                     .move_to([t, 0.75 * t * t - 0.3, 0]) for t in np.linspace(-0.8, 0.8, 7)])
    return VGroup(outer, teeth).scale(1.15)


def face_icon(color=GREY, sw=5, r=0.72):
    return VGroup(Circle(r, color=color, stroke_width=sw),
                  Dot([-0.25, 0.15, 0], radius=0.06, color=color),
                  Dot([0.25, 0.15, 0], radius=0.06, color=color),
                  Arc(radius=0.36, start_angle=PI * 1.2, angle=PI * 0.6, color=color, stroke_width=sw)
                  .move_to([0, -0.2, 0]))


def throat_icon(color=GREY, sw=5):
    tube = RoundedRectangle(corner_radius=0.35, width=0.9, height=1.6, stroke_color=color, stroke_width=sw)
    bolus = Circle(0.2, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([0, -0.15, 0])
    return VGroup(tube, bolus)


def neuron(color=TEXT, r=0.14, ln=0.4):
    """Cell body with an axon to the right."""
    return VGroup(Circle(r, color=color, fill_color=color, fill_opacity=1, stroke_width=0),
                  Line([r, 0, 0], [r + ln, 0, 0], color=color, stroke_width=4))


def neuron_trail(color=TEXT, r=0.18, ln=0.5):
    """Cell body at the right, axon trailing to the left (it is moving right)."""
    return VGroup(Circle(r, color=color, fill_color=color, fill_opacity=1, stroke_width=0),
                  Line([-ln, 0, 0], [-r, 0, 0], color=color, stroke_width=5))


def gold_cell(x, y, r=0.2):
    return VGroup(Circle(r * 1.8, stroke_color=GOLD, stroke_width=3, fill_opacity=0).set_stroke(opacity=0.6),
                  Circle(r, stroke_width=0, fill_color=GOLD, fill_opacity=1)).move_to([x, y, 0])


# ---- title and end cards ----------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Head to Tail: Hox Genes, Retinoic Acid and Rhombomeres"
    TITLE = "Two Segments, Two Jobs"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), 22, GREY)
        fit(lesson, max_w=12.0)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        chap = T("Chapter 1 of 3", 24, GREY)
        g = VGroup(brand, lesson, title, rule, chap).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(Write(title), GrowFromCenter(rule), FadeIn(chap), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


# ---- s01: the puzzle --------------------------------------------------------------------------------
PX = 2.2


def big_bulge(x, y=0.0):
    return RoundedRectangle(corner_radius=0.5, width=2.6, height=5.2, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to([x, y, 0])


def sized(m, s=0.85):
    return m.scale(s)


class S01Q(Sc):
    def construct(self):
        L, R = big_bulge(-PX), big_bulge(PX)
        self.at("Two hindbrain")
        self.play(FadeIn(L), FadeIn(R), run_time=0.9)
        self.at("One builds")
        aL = arr([-3.6, 0, 0], [-4.5, 0, 0], TEAL, 7)
        self.play(fill_to(L, TEAL, 0.3, 6), GrowArrow(aL), run_time=0.7)
        self.at("the jaw")
        jaw = sized(jaw_icon(TEAL)).move_to([-5.7, 0.35, 0])
        jl = T("jaw", 32, TEAL).move_to([-5.7, -0.55, 0])
        self.play(FadeIn(jaw, scale=0.8), FadeIn(jl), run_time=0.6)
        self.at("Another builds")
        aR = arr([3.6, 0, 0], [4.5, 0, 0], YELLOW, 7)
        self.play(fill_to(R, YELLOW, 0.3, 6), GrowArrow(aR), run_time=0.7)
        self.at("the face")
        face = sized(face_icon(YELLOW)).move_to([5.7, 0.35, 0])
        fl = T("face", 32, YELLOW).move_to([5.7, -0.55, 0])
        self.play(FadeIn(face, scale=0.8), FadeIn(fl), run_time=0.6)
        self.at("What tells")
        q = T("?", 140, TEXT, weight=BOLD).move_to([0, 0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


# ---- s02: the row of bulges -------------------------------------------------------------------------
P2 = [(i - 4.5) * 1.25 for i in range(10)]  # cap, r1..r8, cap
B2W, B2H = 1.1, 5.4
B2Y = -0.2


def b2(i, op=0.15, so=1.0):
    r = RoundedRectangle(corner_radius=0.3, width=B2W, height=B2H, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=op).move_to([P2[i], B2Y, 0])
    r.set_stroke(opacity=so)
    return r


class S02Bulges(Sc):
    def construct(self):
        capL = RoundedRectangle(corner_radius=0.3, width=B2W, height=4.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.05).move_to([P2[0], B2Y, 0]).set_stroke(opacity=0.4)
        capR = capL.copy().move_to([P2[9], 0, 0])
        ml = T("midbrain", 26, GREY).move_to([P2[0], 2.95, 0])
        sl = T("spinal cord", 26, GREY).move_to([P2[9] - 0.2, 2.95, 0])
        view = T("seen from above", 28, GREY).move_to([0, -3.8, 0])
        self.at("From above")
        self.play(FadeIn(capL), FadeIn(capR), FadeIn(ml), FadeIn(sl), FadeIn(view), run_time=0.6)
        bs = VGroup(*[b2(i) for i in range(1, 8)])
        self.at("hindbrain")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in bs], lag_ratio=0.4), run_time=1.6)
        self.at("called")
        title = T("rhombomeres", 40, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        labs = VGroup(*[T(f"r{i + 1}", 26, GREY).move_to(bs[i].get_top() + DOWN * 0.34) for i in range(7)])
        self.at("They run")
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.25), run_time=1.5)
        r8 = b2(8, 0.06, 0.45)
        l8 = T("r8", 26, GREY).set_opacity(0.45).move_to(r8.get_top() + DOWN * 0.34)
        self.play(FadeIn(r8), FadeIn(l8), run_time=0.5)
        self.at("front to back")
        a = arr([-4.0, -3.3, 0], [4.0, -3.3, 0], GREY, 6)
        fr = T("front", 28, GREY).move_to([-5.15, -3.3, 0])
        bk = T("back", 28, GREY).move_to([5.0, -3.3, 0])
        self.play(GrowArrow(a), FadeIn(fr), FadeIn(bk), run_time=0.8)
        self.finish()


# ---- shared geometry for s03 to s05 -----------------------------------------------------------------
MSY, MSH = 0.6, 3.2          # map strip: centre y and height (-1.0 .. 2.2)
ICON_Y = -2.15
ICON_X = [(SX[1] + SX[2]) / 2, (SX[3] + SX[4]) / 2, (SX[5] + SX[6]) / 2]
HEAD_Y = 3.4
LAB_Y = -3.15


def mstrip():
    return strip(h=MSH, y=MSY)


def icons(colors=(GREY, GREY, GREY)):
    out = [jaw_icon(colors[0]).scale(0.9).move_to([ICON_X[0], ICON_Y, 0]),
           face_icon(colors[1]).scale(0.9).move_to([ICON_X[1], ICON_Y, 0]),
           throat_icon(colors[2]).scale(0.9).move_to([ICON_X[2], ICON_Y, 0])]
    return out


def mdots():
    return VGroup(*[Dot([SX[i], MSY - 0.75, 0], radius=0.17, color=TEXT) for i in range(1, 7)])


NERVES = [  # idx, colour, numeral, heading text, icon label lines
    ((1, 2), TEAL, "V", "V trigeminal", ["jaw muscles"]),
    ((3, 4), YELLOW, "VII", "VII facial", ["second-arch muscles", "(face, in mammals)"]),
    ((5, 6), PINK, "IX", "IX glossopharyngeal", ["swallowing"]),
]
HEAD_X = [ICON_X[0], ICON_X[1], 4.3]
LOW_X = [ICON_X[0], ICON_X[1], 4.4]


def nerve_bits(k, ic):
    """Everything a nerve adds: heading, icon label lines, numerals, arrows."""
    idx, c, num, head, lab = NERVES[k]
    h = T(head, 26, c, weight=BOLD).move_to([HEAD_X[k], HEAD_Y, 0])
    labs = VGroup(*[T(s, 26, c).move_to([ICON_X[k], LAB_Y - 0.4 * j, 0]) for j, s in enumerate(lab)])
    nums = [T(num, 36, c, weight=BOLD).move_to([SX[i], MSY + 0.1, 0]) for i in idx]
    arrs = [arr([SX[i], MSY - MSH / 2, 0],
                [ICON_X[k] + (-0.25 if i == idx[0] else 0.25), ic[k].get_top()[1] + 0.05, 0], c, 5, 0.18)
            for i in idx]
    return h, labs, nums, arrs


def apply_nerve_state(k, bs, ic):
    idx, c = NERVES[k][0], NERVES[k][1]
    for i in idx:
        bs[i].set_stroke(c, 5).set_fill(c, 0.25)
    ic[k].set_color(c)


def exit_stubs():
    return VGroup(*[Line([SX[i], MSY + MSH / 2, 0], [SX[i], MSY + MSH / 2 + 0.55, 0], color=GOLD, stroke_width=11)
                    for i in (1, 3, 5)])


class S03Map(Sc):
    def construct(self):
        bs = mstrip()
        labs = rlabels(bs)
        ic = icons()
        self.add(bs, labs)
        year = T("1989", 40, TEXT, weight=BOLD)
        names = T("Lumsden and Keynes", 36, TEXT)
        VGroup(year, names).arrange(RIGHT, buff=0.45).move_to([0, 3.3, 0])
        self.play(FadeIn(year), run_time=0.4)
        self.at("Andrew")
        self.play(FadeIn(names, shift=RIGHT * 0.1), run_time=0.5)
        self.at("mapped where")
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in ic], lag_ratio=0.25), run_time=1.2)
        self.at("motor neurons")
        dots = mdots()
        kd = Dot([-5.4, MSY + MSH / 2 + 0.45, 0], radius=0.17, color=TEXT)
        kt = T("= motor neurons", 28, TEXT)
        kt.move_to([-5.15 + kt.width / 2, MSY + MSH / 2 + 0.45, 0])
        self.play(FadeIn(kd), FadeIn(kt), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.12),
                  run_time=1.0)
        self.at("chick")
        self.play(FadeIn(species("chick embryo")), run_time=0.5)
        self.finish()


def map_base():
    bs = mstrip()
    labs = rlabels(bs)
    ic = icons()
    return bs, labs, ic, mdots()


class S04Pairs(Sc):
    def construct(self):
        bs, labs, ic, dots = map_base()
        tag = species("chick")
        self.add(bs, labs, *ic, dots, tag)
        h, lb, nums, arrs = nerve_bits(0, ic)
        self.at("Trigeminal")
        self.play(FadeIn(h), run_time=0.4)
        self.at("jaw muscles")
        self.play(ic[0].animate.set_color(TEAL), FadeIn(lb), run_time=0.5)
        self.at("came from")
        self.play(fill_to(bs[1], TEAL), fill_to(bs[2], TEAL), *[FadeIn(n) for n in nums], run_time=0.6)
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.5)
        h2, lb2, nums2, arrs2 = nerve_bits(1, ic)
        self.at("Facial")
        self.play(FadeIn(h2), run_time=0.4)
        self.at("came from", nth=1)
        self.play(fill_to(bs[3], YELLOW), fill_to(bs[4], YELLOW), *[FadeIn(n) for n in nums2],
                  ic[1].animate.set_color(YELLOW), FadeIn(lb2), run_time=0.6)
        self.play(*[GrowArrow(a) for a in arrs2], run_time=0.5)
        self.finish()


class S05Pairs3(Sc):
    def construct(self):
        bs, labs, ic, dots = map_base()
        tag = species("chick")
        self.add(bs, labs, *ic, dots, tag)
        for k in (0, 1):
            apply_nerve_state(k, bs, ic)
            h, lb, nums, arrs = nerve_bits(k, ic)
            self.add(h, lb, *nums, *arrs)
        h3, lb3, nums3, arrs3 = nerve_bits(2, ic)
        self.at("Swallowing")
        self.play(ic[2].animate.set_color(PINK), FadeIn(h3), FadeIn(lb3), run_time=0.5)
        self.at("came from")
        self.play(fill_to(bs[5], PINK), fill_to(bs[6], PINK), *[FadeIn(n) for n in nums3],
                  *[GrowArrow(a) for a in arrs3], run_time=0.6)
        stubs = exit_stubs()
        lab = T("axons exit here", 26, GOLD)
        lab.move_to([-3.55 - lab.width / 2, MSY + MSH / 2 + 0.45, 0])
        self.play(LaggedStart(*[Create(s) for s in stubs], lag_ratio=0.2), FadeIn(lab), run_time=0.7)
        self.finish()


# ---- s06 / s07: the prediction ----------------------------------------------------------------------
AY, BY, QH = 1.55, -1.05, 1.9
CELL_X = SX[2]


def predict_parts(with_cells=True):
    heading = T("Are the bulges real units?", 36, TEXT).move_to([0, 3.55, 0])
    tube = RoundedRectangle(corner_radius=0.5, width=SX[6] - SX[0] + SW, height=QH, stroke_color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([0, AY, 0])
    bsB = strip(h=QH, y=BY)
    labB = rlabels(bsB)
    A = gold_cell(CELL_X, AY - 0.25)
    B = gold_cell(CELL_X, BY - 0.25)
    capA = T("before boundaries appear", 30, GOLD).move_to([-5.7, AY + QH / 2 + 0.3, 0])
    capA.move_to([-5.7 + capA.width / 2, AY + QH / 2 + 0.33, 0])
    capB = T("after boundaries appear", 30, GOLD)
    capB.move_to([-5.7 + capB.width / 2, BY + QH / 2 + 0.33, 0])
    q = T("?", 64, GOLD, weight=BOLD).move_to([1.0, BY + QH / 2 + 0.4, 0])
    ask = T("Where do their descendants go?", 36, TEXT).move_to([0, -2.95, 0])
    return heading, tube, bsB, labB, A, B, capA, capB, q, ask


class S06Predict(Sc):
    def construct(self):
        heading, tube, bsB, labB, A, B, capA, capB, q, ask = predict_parts()
        self.at("Are the bulges")
        self.play(FadeIn(heading), FadeIn(bsB), FadeIn(labB), FadeIn(tube), run_time=0.8)
        self.at("Label one cell")
        self.play(FadeIn(A, scale=0.5), run_time=0.5)
        self.at("before boundaries")
        self.play(FadeIn(capA), run_time=0.4)
        self.at("and one")
        self.play(FadeIn(B, scale=0.5), FadeIn(capB), run_time=0.6)
        self.at("Where do")
        self.play(FadeIn(ask), FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        heading, tube, bsB, labB, A, B, capA, capB, q, ask = predict_parts()
        self.add(heading, tube, bsB, labB, A, B, capA, capB, q, ask)
        pp = T("Pause and predict", 32, TEXT, weight=BOLD).move_to([-1.3, -3.6, 0])
        self.add(pp)
        for n in (5, 4, 3, 2, 1):
            num = M(str(n), 44, GOLD, weight=BOLD).move_to([1.9, -3.6, 0])
            self.add(num)
            self.wait(1.0)
            self.remove(num)
        self.finish()


# ---- s08: the tracer-dye result -------------------------------------------------------------------
PCY = -0.15
PH = 4.0
CXL, CXR = -3.25, 3.25
BW = 2.7
EARLY_DX = [(0.35, 0.6), (0.95, 0.25), (1.55, -0.3), (2.0, 0.5), (1.9, -0.55), (1.25, -0.85), (0.25, -0.6), (1.4, 0.85)]
LATE_DX = [(-0.65, 0.55), (0.1, 0.85), (0.7, 0.4), (0.75, -0.3), (0.4, -0.8), (-0.2, -0.85), (-0.7, -0.6), (-0.8, 0.0)]


def clone_dots(ox, oy, offs):
    return VGroup(*[Dot([ox + dx, oy + dy, 0], radius=0.15, color=GOLD) for dx, dy in offs])


class S08Reveal(Sc):
    def construct(self):
        self.add(species("chick"))
        year = T("1990", 40, TEXT, weight=BOLD)
        names = T("Fraser, Keynes and Lumsden", 34, TEXT)
        VGroup(year, names).arrange(RIGHT, buff=0.45).move_to([0, 3.5, 0])
        sp = T("chick embryo", 26, GREY).move_to([0, 3.05, 0])
        self.play(FadeIn(year), FadeIn(sp), run_time=0.4)
        tubeL = RoundedRectangle(corner_radius=0.5, width=5.6, height=PH, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.15).move_to([CXL, PCY, 0])
        divL = DashedLine([CXL, PCY - PH / 2 + 0.1, 0], [CXL, PCY + PH / 2 - 0.1, 0], color=GREY, stroke_width=3,
                          dash_length=0.12)
        divL.set_opacity(0.55)
        r3L = T("r3", 26, GREY).move_to([CXL - 1.4, PCY + 1.5, 0])
        r4L = T("r4", 26, GREY).move_to([CXL + 1.4, PCY + 1.5, 0])
        bR3 = RoundedRectangle(corner_radius=0.4, width=BW, height=PH, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.15).move_to([CXR - 1.45, PCY, 0])
        bR4 = bR3.copy().move_to([CXR + 1.45, PCY, 0])
        r3R = T("r3", 26, GREY).move_to([CXR - 1.45, PCY + 1.5, 0])
        r4R = T("r4", 26, GREY).move_to([CXR + 1.45, PCY + 1.5, 0])
        self.play(FadeIn(tubeL), FadeIn(divL), FadeIn(r3L), FadeIn(r4L), FadeIn(bR3), FadeIn(bR4),
                  FadeIn(r3R), FadeIn(r4R), run_time=0.8)
        self.at("Scott")
        self.play(FadeIn(names, shift=RIGHT * 0.1), run_time=0.5)
        self.at("tracer")
        sx0, sy0 = CXL - 1.4, PCY - 0.35
        cellL = gold_cell(sx0, sy0)
        td = T("tracer dye", 28, GOLD).move_to([sx0 + 0.2, PCY - 1.65, 0])
        tda = arr([sx0, PCY - 1.35, 0], [sx0, sy0 - 0.45, 0], GOLD, 4, 0.16)
        self.play(FadeIn(cellL, scale=0.5), FadeIn(td), GrowArrow(tda), run_time=0.5)
        self.at("Clones labeled early")
        hL = T("labelled early", 30, GOLD, weight=BOLD).move_to([CXL, PCY + PH / 2 + 0.38, 0])
        self.play(FadeIn(hL), run_time=0.4)
        self.at("could span")
        dots = clone_dots(sx0, sy0, [(0, 0)] * len(EARLY_DX))
        self.add(dots)
        self.play(FadeOut(td), FadeOut(tda),
                  LaggedStart(*[d.animate.move_to([sx0 + dx, sy0 + dy, 0]) for d, (dx, dy) in zip(dots, EARLY_DX)],
                              lag_ratio=0.1), run_time=1.5)
        resL = T("spans the boundary", 28, TEXT).move_to([CXL, PCY - PH / 2 - 0.4, 0])
        self.play(FadeIn(resL), run_time=0.4)
        self.at("Clones labeled after")
        hR = T("labelled after boundaries", 30, GOLD, weight=BOLD).move_to([CXR, PCY + PH / 2 + 0.38, 0])
        rx0, ry0 = CXR - 1.45, PCY - 0.35
        cellR = gold_cell(rx0, ry0)
        self.play(FadeIn(hR), FadeIn(cellR, scale=0.5), run_time=0.5)
        self.at("stayed inside")
        dots2 = clone_dots(rx0, ry0, [(0, 0)] * len(LATE_DX))
        self.add(dots2)
        self.play(LaggedStart(*[d.animate.move_to([rx0 + dx, ry0 + dy, 0]) for d, (dx, dy) in zip(dots2, LATE_DX)],
                              lag_ratio=0.1), run_time=1.2)
        resR = T("stays inside one", 28, TEXT).move_to([CXR, PCY - PH / 2 - 0.4, 0])
        self.play(FadeIn(resR), run_time=0.4)
        self.finish()


# ---- s09: compartments ----------------------------------------------------------------------------
CSY, CSH = 0.4, 3.4          # compartment strip y and height (-1.1 .. 1.9)
CLUSTER = [(-0.35, -0.1), (0.2, -0.3), (0.35, 0.1), (-0.1, 0.2), (-0.25, -0.5)]


def cstrip(bright=True):
    bs = strip(h=CSH, y=CSY, sw=5 if bright else 3, stroke=TEXT if bright else GREY, op=0.12)
    return bs


def clusters():
    return VGroup(*[VGroup(*[Dot([SX[i] + dx, CSY - 0.2 + dy, 0], radius=0.12, color=GOLD) for dx, dy in CLUSTER])
                    for i in range(7)])


class S09Compart(Sc):
    def construct(self):
        self.add(species("chick"))
        bs = cstrip(False)
        labs = rlabels(bs)
        self.add(bs, labs)
        prog = clusters()
        self.at("Each")
        self.play(FadeIn(prog), run_time=0.6)
        self.at("compartment")
        comp = T("compartment", 36, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        brace = Brace(Rectangle(width=11.4, height=CSH).move_to([0, CSY, 0]), UP, color=TEXT, buff=0.1)
        self.play(*[b.animate.set_stroke(TEXT, 5).set_fill(TEXT, 0.12) for b in bs], FadeIn(comp), FadeIn(brace),
                  run_time=0.8)
        self.at("progenitors")
        pl = T("progenitors", 28, GOLD).move_to([SX[1], -2.1, 0])
        pa = arr([SX[1], -1.77, 0], [SX[1], CSY - 0.62, 0], GOLD, 4, 0.16)
        self.play(FadeIn(pl), GrowArrow(pa), run_time=0.4)
        self.at("do not cross")
        wallx = SX[2] + SW / 2 - 0.05
        d = prog[2][2]
        y0 = d.get_center()[1]
        self.play(d.animate.move_to([wallx - 0.15, y0, 0]), run_time=0.5)
        x = VGroup(Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=TEXT, stroke_width=9),
                   Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=TEXT, stroke_width=9)).move_to([wallx + 0.12, y0, 0])
        self.play(FadeIn(x, scale=0.5), d.animate.move_to([wallx - 0.7, y0 - 0.2, 0]), run_time=0.45)
        self.play(FadeOut(x), run_time=0.3)
        self.at("Some neurons")
        nrn = neuron_trail(TEXT, 0.24, 0.7).move_to([SX[3], CSY + 0.6, 0])
        ring = Circle(0.42, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(nrn[0].get_center())
        lab = T("later neurons can migrate", 36, TEXT).move_to([0.5, -3.05, 0])
        self.play(FadeIn(nrn, scale=0.5), FadeIn(ring), FadeIn(lab), run_time=0.6)
        self.play(Indicate(ring, color=TEXT, scale_factor=1.25), run_time=0.7)
        self.at("migrate")
        bx = nrn[0].get_center()[0]
        trail = DashedLine([bx + 0.3, CSY + 0.6, 0], [bx + 3.2, CSY + 0.6, 0], color=TEXT, stroke_width=3,
                           dash_length=0.12).set_opacity(0.6)
        self.add(trail)
        self.play(nrn.animate.shift(RIGHT * 3.2), ring.animate.shift(RIGHT * 3.2), run_time=1.2)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        bs = cstrip(True)
        labs = rlabels(bs)
        prog = clusters()
        nrn = neuron_trail(TEXT, 0.24, 0.7).move_to([SX[3], CSY + 0.6, 0]).shift(RIGHT * 3.2)
        ring = Circle(0.42, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(nrn[0].get_center())
        lab = T("later neurons can migrate", 36, TEXT).move_to([0.5, -3.05, 0])
        self.add(bs, labs, prog, nrn, ring, lab, species("chick"))
        self.wait(2.0)
        self.play(FadeOut(lab), FadeOut(labs), FadeOut(nrn), FadeOut(ring), run_time=0.5)
        self.finish()


# ---- s11: the label ---------------------------------------------------------------------------------
TAGY = -2.95
CSY11, CSH11 = -0.15, 3.5


def empty_tag(i, y=TAGY):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.2, height=1.1, stroke_color=GREY, stroke_width=3),
                         num_dashes=30)
    return VGroup(box, T("?", 44, GREY)).move_to([SX[i], y, 0])


class S11Label(Sc):
    def construct(self):
        self.add(species("mouse"))
        bs = strip(h=CSH11, y=CSY11, sw=5, stroke=TEXT, op=0.12)
        labs = rlabels(bs)
        self.add(bs, labs)
        tags = VGroup(*[empty_tag(i) for i in range(7)])
        self.at("need a label")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.12), run_time=1.2)
        self.at("a set of")
        l1 = T("a set of transcription factors,", 42, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.6)
        self.at("Hox")
        l2 = T("mostly Hox genes", 42, PURPLE, weight=BOLD).move_to([0, 2.35, 0])
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---- s12 / s13: the code grid -----------------------------------------------------------------------
GXS = [-3.0 + 1.3 * i for i in range(7)]
ROWS = [  # label, colour, columns on (0 = r1), is_hox
    ("Hoxa2", PURPLE, [1, 2, 3, 4, 5, 6], True),
    ("Hoxb2", PURPLE, [2, 3, 4, 5, 6], True),
    ("Hoxb1", PURPLE, [3], True),
    ("Hoxa3, b3", PURPLE, [4, 5, 6], True),
    ("Hoxb4, d4", PURPLE, [6], True),
    ("Krox20", TEXT, [2, 4], False),
    ("MafB", TEXT, [4, 5], False),
]
GY = [2.45 - 0.62 * k for k in range(7)]
HEADY = 3.0
GTAGY = -2.1
FOOTY = -3.55


def grid_static():
    heads = VGroup(*[T(f"r{i + 1}", 26, GREY).move_to([GXS[i], HEADY, 0]) for i in range(7)])
    rlab = VGroup(*[T(r[0], 26, r[1]).move_to([-3.75, GY[k], 0], aligned_edge=RIGHT) for k, r in enumerate(ROWS)])
    for k, m in enumerate(rlab):
        m.move_to([-3.75 - m.width / 2, GY[k], 0])
    rules = VGroup(*[Line([-6.3, GY[k] - 0.31, 0], [5.5, GY[k] - 0.31, 0], color=GREY, stroke_width=1).set_opacity(0.2)
                     for k in range(7)])
    return heads, rlab, rules


def grid_dots():
    d = {}
    for k, (name, col, cols, hox) in enumerate(ROWS):
        for c in cols:
            d[(k, c)] = Circle(0.2, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([GXS[c], GY[k], 0])
    return d


def boundary_lines():
    return VGroup(*[DashedLine([GXS[c] - 0.65, GY[6] - 0.31, 0], [GXS[c] - 0.65, HEADY + 0.2, 0], color=GREY,
                               stroke_width=2, dash_length=0.1).set_opacity(0.4) for c in range(1, 7)])


def front_bars():
    bars = []
    for k, (name, col, cols, hox) in enumerate(ROWS):
        if hox:
            x = GXS[cols[0]] - 0.65
            bars.append(Line([x, GY[k] - 0.25, 0], [x, GY[k] + 0.25, 0], color=TEXT, stroke_width=7))
    return VGroup(*bars)


def gtag(i, h=0.7):
    return RoundedRectangle(corner_radius=0.1, width=1.1, height=h, stroke_color=PURPLE, stroke_width=3,
                            fill_color=MIX[i], fill_opacity=0.95).move_to([GXS[i], GTAGY, 0])


def tag_label():
    m = T("segment's code", 26, PURPLE)
    return m.move_to([-3.75 - m.width / 2, GTAGY, 0])


def foot():
    return T("simplified early mouse code; levels and later changes left out", 26, GREY).move_to([0, FOOTY, 0])


class S12Code(Sc):
    def construct(self):
        heads, rlab, rules = grid_static()
        dots = grid_dots()
        bars = front_bars()
        bl = boundary_lines()
        tags = VGroup(*[gtag(i) for i in range(7)])
        tl = tag_label()
        self.add(species("mouse"))
        self.play(FadeIn(heads), FadeIn(rlab), FadeIn(rules), run_time=0.4)
        hox_dots = [dots[(k, c)] for (k, c) in dots if ROWS[k][3]]
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in hox_dots], lag_ratio=0.07), run_time=1.3)
        self.at("front edges")
        fe = T("front edge", 26, TEXT).move_to([GXS[1] - 0.65, 3.55, 0])
        fea = arr([GXS[1] - 0.65, 3.33, 0], [GXS[1] - 0.65, GY[0] + 0.3, 0], TEXT, 4, 0.16)
        self.play(FadeIn(bars[0], scale=1.5), FadeIn(fe), GrowArrow(fea), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, scale=1.5) for b in bars[1:]], lag_ratio=0.4), run_time=0.9)
        self.at("boundaries")
        self.play(FadeIn(bl), run_time=0.6)
        self.at("Read the code")
        seg = [dots[(k, c)] for (k, c) in dots if not ROWS[k][3]]
        self.play(*[FadeIn(d, scale=0.5) for d in seg], FadeIn(foot()), FadeIn(tl), run_time=0.4)
        self.at("column by column")
        rect = Rectangle(width=1.2, height=6.0, stroke_color=TEXT, stroke_width=4, fill_color=TEXT,
                         fill_opacity=0.07).move_to([GXS[0], 0.3, 0])
        self.play(FadeIn(rect), FadeIn(tags[0], shift=UP * 0.1), run_time=0.2)
        for i in range(1, 6):
            self.play(rect.animate.move_to([GXS[i], 0.3, 0]), FadeIn(tags[i], shift=UP * 0.1), run_time=0.2)
            self.wait(0.03)
        self.at("Every")
        self.play(rect.animate.move_to([GXS[6], 0.3, 0]), FadeIn(tags[6], shift=UP * 0.1), run_time=0.3)
        self.play(FadeOut(rect), run_time=0.3)
        self.finish()


def s13_base():
    heads, rlab, rules = grid_static()
    dots = grid_dots()
    bars = front_bars()
    bl = boundary_lines()
    tags = VGroup(*[gtag(i) for i in range(7)])
    return heads, rlab, rules, dots, bars, bl, tags


def cell_box(k, c, color=TEXT, w=1.0, h=0.5, sw=5):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_opacity=0).move_to([GXS[c], GY[k], 0])


class S13R3r4(Sc):
    def construct(self):
        heads, rlab, rules, dots, bars, bl, tags = s13_base()
        tl = tag_label()
        expl = T("each segment's code (mix of the rows above)", 26, PURPLE).move_to([0.6, -2.95, 0])
        self.add(heads, rlab, rules, bl, bars, tags, tl, foot(), *dots.values(), species("mouse"))
        self.play(FadeIn(expl), run_time=0.4)
        colH = 5.75
        cy = 0.35
        rect3 = Rectangle(width=1.2, height=colH, stroke_color=TEAL, stroke_width=5, fill_color=TEAL,
                          fill_opacity=0.1).move_to([GXS[2], cy, 0])
        rect4 = Rectangle(width=1.2, height=colH, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW,
                          fill_opacity=0.1).move_to([GXS[3], cy, 0])
        vjaw = T("V (with r2)", 28, TEAL, weight=BOLD).move_to([GXS[2] - 0.45, 3.58, 0])
        vii = T("VII", 28, YELLOW, weight=BOLD).move_to([GXS[3] + 0.1, 3.58, 0])
        dim = [d for (k, c), d in dots.items() if c not in (2, 3)]
        self.at("r3")
        self.play(FadeIn(rect3), FadeIn(vjaw), *[d.animate.set_opacity(0.25) for d in dim],
                  *[t.animate.set_opacity(0.3) for i, t in enumerate(tags) if i not in (2, 3)], run_time=0.6)
        self.at("r4")
        self.play(FadeIn(rect4), FadeIn(vii), run_time=0.5)
        self.at("a2")
        p0 = cell_box(0, 2, w=2.4, h=0.5).set_x((GXS[2] + GXS[3]) / 2)
        self.play(Create(p0), run_time=0.5)
        self.at("b2")
        p1 = cell_box(1, 2, w=2.4, h=0.5).set_x((GXS[2] + GXS[3]) / 2)
        self.play(Create(p1), run_time=0.5)
        self.at("separates them")
        self.play(*[p.animate.set_stroke(opacity=0.2) for p in (p0, p1)], run_time=0.4)
        self.until(self.t_of("separates them") + 0.85)
        kb = cell_box(5, 2, w=0.9, h=0.5)
        sg = Brace(Rectangle(width=0.1, height=1.24).move_to([-4.95, (GY[5] + GY[6]) / 2, 0]), LEFT,
                   color=TEXT, buff=0.05)
        sgt = T("segment\ngenes", 26, TEXT, line_spacing=0.8).move_to([-6.1, (GY[5] + GY[6]) / 2, 0])
        self.play(Create(kb), FadeIn(sg), FadeIn(sgt),
                  *[dots[kc].animate.set_opacity(0.95) for kc in ((5, 4), (6, 4), (6, 5))], run_time=0.6)
        self.at("and later")
        hb = cell_box(2, 3, w=0.95, h=0.56)
        st = T("later: strong", 28, TEXT).move_to([GXS[3] + 0.7, GY[2], 0], aligned_edge=LEFT)
        st.move_to([GXS[3] + 0.75 + st.width / 2, GY[2], 0])
        self.play(kb.animate.set_stroke(opacity=0.25), Create(hb), dots[(2, 3)].animate.scale(1.3),
                  FadeIn(st), run_time=0.6)
        self.finish()


# ---- s14 to s16: the idea ----------------------------------------------------------------------------
class S14Idea(Sc):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=12.2, height=6.6, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.05).move_to(ORIGIN)
        head = T("ONE IDEA TO CARRY THROUGH", 30, GOLD, weight=BOLD).move_to([0, 2.7, 0])
        c1 = chip("more early retinoic acid", ORANGE, 44).move_to([0, 1.4, 0])
        c2 = chip("a more posterior code", PURPLE, 44).move_to([0, -0.1, 0])
        c3 = chip("helps set the neurons", TEXT, 44).move_to([0, -1.6, 0])
        a1 = arr([0, c1.get_bottom()[1] - 0.05, 0], [0, c2.get_top()[1] + 0.05, 0], GREY, 5)
        a2 = arr([0, c2.get_bottom()[1] - 0.05, 0], [0, c3.get_top()[1] + 0.05, 0], GREY, 5)
        pr = T("(a direction, over the range tested)", 26, GREY).move_to([0, -2.75, 0])
        self.play(FadeIn(card), FadeIn(head), run_time=0.6)
        self.at("more early")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("more posterior")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.at("the code helps")
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.1), run_time=0.6)
        self.at("neurons")
        self.play(FadeIn(pr), run_time=0.5)
        self.finish()


I15Y, I15H = 1.2, 2.3
T15 = -0.7


def mtag(i, shade=None, y=T15, h=0.8, w=1.2):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=PURPLE, stroke_width=3,
                            fill_color=MIX[i if shade is None else shade], fill_opacity=0.95).move_to([SX[i], y, 0])


class S15Idea2(Sc):
    def construct(self):
        bs = strip(h=I15H, y=I15Y)
        labs = rlabels(bs)
        tags = VGroup(*[mtag(i) for i in range(7)])
        fb = arr([-4.3, -1.95, 0], [4.3, -1.95, 0], GREY, 6)
        fr = T("front", 28, GREY).move_to([-5.35, -1.95, 0])
        bk = T("back", 28, GREY).move_to([5.2, -1.95, 0])
        # key
        sw1 = Rectangle(width=0.7, height=0.4, stroke_color=PURPLE, stroke_width=3, fill_color=MIX[0], fill_opacity=0.95)
        sw2 = Rectangle(width=0.7, height=0.4, stroke_color=PURPLE, stroke_width=3, fill_color=MIX[6], fill_opacity=0.95)
        k1 = T("light tag: more anterior code", 28, TEXT)
        k2 = T("dark tag: more posterior code", 28, TEXT)
        sw1.move_to([-6.45, -2.5, 0])
        k1.move_to([-6.0 + k1.width / 2, -2.5, 0])
        sw2.move_to([0.0, -2.5, 0])
        k2.move_to([0.45 + k2.width / 2, -2.5, 0])
        note1 = T("code shifts toward the back: a direction, not a count of Hox genes", 28, TEXT)
        note2 = T("schematic, not a measured profile", 28, GREY)
        note1.move_to([0, -3.15, 0])
        note2.move_to([0, -3.65, 0])
        dk = T("tags one shade darker", 26, ORANGE).move_to([(SX[1] + SX[3]) / 2, -1.38, 0])
        self.play(FadeIn(bs), FadeIn(labs), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.08),
                  GrowArrow(fb), FadeIn(fr), FadeIn(bk), run_time=1.0)
        self.play(FadeIn(sw1), FadeIn(k1), FadeIn(sw2), FadeIn(k2), run_time=0.5)
        self.at("more retinoic")
        chp = chip("more early retinoic acid", ORANGE, 30).move_to([-2.0, 3.3, 0])
        self.play(FadeIn(chp, shift=DOWN * 0.1), run_time=0.5)
        self.at("vitamin")
        sub = T("(a vitamin A product)", 28, ORANGE)
        sub.move_to([chp.get_right()[0] + 0.3 + sub.width / 2, 3.3, 0])
        self.play(FadeIn(sub), run_time=0.4)
        self.at("pushes")
        oa = VGroup(*[arr([SX[i], chp.get_bottom()[1] - 0.02, 0], [SX[i], I15Y + I15H / 2 + 0.03, 0], ORANGE, 5, 0.15)
                      for i in (1, 2, 3)])
        self.play(LaggedStart(*[GrowArrow(a) for a in oa], lag_ratio=0.15),
                  *[bs[i].animate.set_stroke(ORANGE, 5).set_fill(ORANGE, 0.15) for i in (1, 2, 3)],
                  *[Transform(tags[i], mtag(i, shade=i + 1).set_stroke(ORANGE, 5)) for i in (1, 2, 3)], FadeIn(dk), run_time=0.9)
        self.at("posterior")
        self.play(FadeIn(note1), FadeIn(note2), run_time=0.6)
        self.finish()


S16Y, S16H = 1.75, 2.2
S16T = -0.45
S16COLS = {1: TEAL, 2: TEAL, 3: YELLOW, 4: YELLOW, 5: PINK, 6: PINK}


def s16_base():
    bs = strip(h=S16H, y=S16Y)
    labs = rlabels(bs)
    tags = VGroup(*[mtag(i, y=S16T, h=0.75) for i in range(7)])
    tl = T("the code", 26, PURPLE)
    tl.move_to([-6.4 + tl.width / 2, 0.28, 0])
    return bs, labs, tags, tl


def s16_tag():
    return species("schematic: chick map + mouse code")


def s16_sg():
    return T("sharpened by segment genes", 30, TEXT).move_to([3.3, 3.4, 0])


def s16_lower():
    arrs = VGroup(*[arr([SX[i], -0.9, 0], [SX[i], -1.6, 0], S16COLS[i], 4, 0.16) for i in range(1, 7)])
    nrs = VGroup(*[neuron(S16COLS[i], 0.2, 0.4).move_to([SX[i] - 0.1, -1.95, 0]) for i in range(1, 7)])
    names = VGroup()
    for k, (idx, c, num, head, lab) in enumerate(NERVES):
        lines = [head] + lab
        for j, s in enumerate(lines):
            names.add(T(s, 26, c, weight=BOLD if j == 0 else NORMAL).move_to([LOW_X[k], -2.6 - 0.4 * j, 0]))
    return arrs, nrs, names


def s16_krox():
    return VGroup(*[T("Krox20", 26, TEXT).move_to([SX[i], S16Y - 0.2, 0]) for i in (2, 4)])


class S16Idea3(Sc):
    def construct(self):
        bs, labs, tags, tl = s16_base()
        self.add(bs, labs, tags, tl, s16_tag())
        self.play(*[t.animate.set_stroke(TEXT, 5) for t in tags], run_time=0.4)
        self.play(*[t.animate.set_stroke(PURPLE, 3) for t in tags], run_time=0.4)
        self.at("sharpened by")
        sg = s16_sg()
        self.play(FadeIn(sg, shift=DOWN * 0.1), run_time=0.6)
        self.at("such as")
        self.wait(0.45)
        kx = s16_krox()
        self.play(FadeIn(kx, scale=0.7), run_time=0.4)
        arrs, nrs, names = s16_lower()
        self.at("helps decide")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.1), run_time=0.7)
        self.at("motor neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in nrs], lag_ratio=0.1), FadeIn(names), run_time=1.0)
        self.finish()


class S17Beat(NarratedScene):
    def construct(self):
        bs, labs, tags, tl = s16_base()
        arrs, nrs, names = s16_lower()
        sg = s16_sg()
        allm = VGroup(bs, labs, tags, tl, sg, s16_tag(), s16_krox(), arrs, nrs, names)
        self.add(allm)
        self.wait(2.2)
        self.play(FadeOut(allm), run_time=0.5)
        self.finish()


# ---- s18: the takeaway; s19: end card ---------------------------------------------------------------
class S18Take(Sc):
    def construct(self):
        BX, BYY = 1.6, 0.75
        def box(x):
            return RoundedRectangle(corner_radius=0.5, width=2.4, height=4.0, stroke_color=GREY, stroke_width=4,
                                    fill_color=GREY, fill_opacity=0.15).move_to([x, BYY, 0])
        L, R = box(-BX), box(BX)
        l3 = T("r3", 28, GREY).move_to([-BX, BYY + 1.65, 0])
        l4 = T("r4", 28, GREY).move_to([BX, BYY + 1.65, 0])
        jaw = sized(jaw_icon(GREY)).move_to([-4.9, BYY + 0.35, 0])
        face = sized(face_icon(GREY)).move_to([4.9, BYY + 0.35, 0])
        jl = T("jaw muscles", 26, GREY).move_to([-4.9, BYY - 0.6, 0])
        fl = VGroup(T("second-arch muscles", 26, GREY).move_to([4.9, BYY - 0.6, 0]),
                    T("(face, in mammals)", 26, GREY).move_to([4.9, BYY - 0.95, 0]))
        self.add(L, R, l3, l4, jaw, face, jl, fl)
        nL = T("V", 60, GREY, weight=BOLD).move_to([-BX, BYY + 0.7, 0])
        nR = T("VII", 60, GREY, weight=BOLD).move_to([BX, BYY + 0.7, 0])
        tL = mtag(0, shade=2, w=1.8, h=0.8).move_to([-BX, BYY - 0.55, 0])
        tR = mtag(0, shade=3, w=1.8, h=0.8).move_to([BX, BYY - 0.55, 0])
        cL = T("code", 26, PURPLE).move_to([-BX, BYY - 1.2, 0])
        cR = T("code", 26, PURPLE).move_to([BX, BYY - 1.2, 0])
        c1 = T("Lookalike segments,", 38, TEXT)
        c2 = T("different codes, different neurons", 38, TEXT)
        cap = VGroup(c1, c2).arrange(DOWN, buff=0.15).move_to([0, -2.95, 0])
        self.at("lookalike")
        self.play(Indicate(L, color=TEXT, scale_factor=1.04), Indicate(R, color=TEXT, scale_factor=1.04),
                  FadeIn(nL), FadeIn(nR), FadeIn(tL, shift=UP * 0.1), FadeIn(tR, shift=UP * 0.1),
                  FadeIn(cL), FadeIn(cR), FadeIn(c1), run_time=0.8)
        self.at("not alike")
        self.play(fill_to(L, TEAL, 0.25, 6), fill_to(R, YELLOW, 0.25, 6),
                  nL.animate.set_color(TEAL), nR.animate.set_color(YELLOW),
                  jaw.animate.set_color(TEAL), face.animate.set_color(YELLOW),
                  jl.animate.set_color(TEAL), fl.animate.set_color(YELLOW), FadeIn(c2), run_time=0.7)
        self.finish()


class S19End(EndCard):
    LINE = "Lookalike segments are not alike. Each carries its own code."

    def construct(self):
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        nxt = T("Next: Remove One Letter", 26, GREY)
        sub = T("biochemistrypedia.com", 22, TEAL)
        g = VGroup(line, nxt, sub).arrange(DOWN, buff=0.4)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(nxt), FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
