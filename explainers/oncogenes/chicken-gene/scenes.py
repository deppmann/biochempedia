"""Oncogenes, section film: the cancer gene was the chicken's own  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  ORANGE = the virus and its src gene (and the old-infection idea)
  BLUE   = the cell's own DNA (chicken, duck, quail, emu, mammals) and c-src
  YELLOW = the radioactive probe while it searches
  GREEN  = the probe stuck (a match) and the conclusion drawn from it
  GOLD   = the named person
  RED    = no match, a doubt, the altered copy
  GREY   = outlines, notes, de-emphasised
Teeth on the strands are an idealised picture of "matching sequence"; they are not real sequences.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
SRC = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
PADL = [0, 1, 1, 0, 1, 0, 0, 1]
PADR = [1, 1, 0, 0, 1, 0, 1, 1]


def strand(x0, base, prof, tw, h, thick, color, sign=1, fo=0.3, sw=3):
    """A strand with square teeth. sign=+1: body below the base line, teeth rise (a bar).
    sign=-1: body above the base line, teeth hang (a probe)."""
    x1 = x0 + tw * len(prof)
    pts = [(x0, base - sign * thick), (x0, base)]
    cur = base
    for i, p in enumerate(prof):
        top = base + sign * h * p
        xl = x0 + i * tw
        if abs(top - cur) > 1e-9:
            pts.append((xl, top))
        pts.append((xl + tw, top))
        cur = top
    if abs(cur - base) > 1e-9:
        pts.append((x1, base))
    pts.append((x1, base - sign * thick))
    P = Polygon(*[[x, y, 0] for x, y in pts], color=color, stroke_width=sw, fill_color=color, fill_opacity=fo)
    return P


def probe_for(x0, bar_base, prof, tw, h, thick=0.5, color=YELLOW):
    """a probe whose teeth fit the gaps of a bar with teeth `prof`, sitting flush on it."""
    return strand(x0, bar_base + h, [1 - p for p in prof], tw, h, thick, color, sign=-1, fo=0.45, sw=3)


def recolor(m, color, fo=None):
    a = m.animate.set_stroke(color)
    return a.set_fill(color, fo) if fo is not None else a.set_fill(color)


def cross(center, size=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w),
                  Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tag(text, color, size=26):
    return chip(text, color, size=size)


class S00Title(TitleCard):
    LESSON = "Oncogenes: When the Switch Sticks"
    TITLE = "A Gene of the Birds Themselves"


# ---------------------------------------------------------------------------------------------
TW1, H1, TH1 = 0.42, 0.4, 0.7
X0 = -5.45          # left end of the long strands in scenes 1 and 2
BASE1 = -0.6        # bar base line in scenes 1 and 2
PX = X0 + 8 * TW1   # left end of the matching stretch
HOVER = UP * 0.9


class S01Probe(SpokenScene):
    def construct(self):
        # virus: three pieces, the middle one is src
        left = strand(X0, BASE1, PADL, TW1, H1, TH1, GREY, fo=0.25)
        mid = strand(PX, BASE1, SRC, TW1, H1, TH1, ORANGE, fo=0.4)
        right = strand(PX + 10 * TW1, BASE1, PADR, TW1, H1, TH1, GREY, fo=0.25)
        virus = VGroup(left, mid, right)
        lab_l = T("rest of virus", 24, GREY).move_to(left.get_center() + DOWN * 1.0)
        lab_r = T("rest of virus", 24, GREY).move_to(right.get_center() + DOWN * 1.0)
        lab_s = T("src", 28, ORANGE, weight=BOLD).move_to(mid.get_center() + DOWN * 1.0)
        q = T("?", 56, YELLOW, weight=BOLD).move_to(mid.get_center() + UP * 1.4)
        note = T("idealised, not to scale", 22, GREY).move_to([5.2, -3.45, 0])
        self.add(note)
        self.at("Where did a virus")
        self.play(FadeIn(virus, shift=UP * 0.1), FadeIn(lab_l), FadeIn(lab_r), FadeIn(lab_s), run_time=1.0)
        self.play(FadeIn(q, scale=0.8), run_time=0.5)

        head = T("San Francisco: the Bishop and Varmus laboratory", 30, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.at("In San Francisco")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeOut(q), run_time=0.6)

        who = T("Dominique Stehelin, postdoctoral fellow", 28, GOLD).move_to([0, 2.65, 0])
        self.at("postdoctoral fellow")
        self.play(FadeIn(who, shift=DOWN * 0.1), run_time=0.6)

        probe = probe_for(PX, BASE1, SRC, TW1, H1).shift(HOVER + UP * 0.7)
        plab = T("radioactive DNA probe", 26, YELLOW).next_to(probe, UP, buff=0.18)
        self.at("radioactive strand")
        self.play(FadeIn(probe, shift=DOWN * 0.2), FadeIn(plab), run_time=0.7)

        self.at("It matched")
        self.play(FadeOut(plab), probe.animate.shift(DOWN * (0.7 + 0.9)), run_time=0.8)
        self.play(recolor(probe, GREEN, 0.5), recolor(mid, GREEN, 0.4), run_time=0.4)
        mt = T("match", 28, GREEN, weight=BOLD).next_to(probe, UP, buff=0.2)
        self.play(FadeIn(mt), run_time=0.3)

        no1 = VGroup(cross(left.get_center() + UP * 1.0), T("no match", 24, RED).move_to(left.get_center() + UP * 1.55))
        no2 = VGroup(cross(right.get_center() + UP * 1.0), T("no match", 24, RED).move_to(right.get_center() + UP * 1.55))
        self.at("no other part")
        self.play(FadeIn(no1, shift=DOWN * 0.1), FadeIn(no2, shift=DOWN * 0.1), run_time=0.6)

        call = T("one strand sticks to its matching sequence", 28, TEXT).move_to([-1.2, -2.95, 0])
        self.at("A single strand")
        self.play(FadeIn(call, shift=UP * 0.1), run_time=0.6)

        # reset to a neutral state: the probe goes up, the virus leaves, the question is posed
        self.at("So this probe")
        sample = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=10.9, height=1.5, stroke_color=BLUE,
                                                 stroke_width=4), num_dashes=70)
        qm = T("?", 56, BLUE, weight=BOLD)
        sample_g = VGroup(sample, qm).move_to([X0 + 10.9 / 2, BASE1 - 0.15, 0])
        self.play(FadeOut(VGroup(virus, lab_l, lab_r, lab_s, no1, no2, call, mt)),
                  recolor(probe, YELLOW, 0.45), probe.animate.shift(HOVER), run_time=0.7)
        self.at("any sample")
        slab = T("any sample of DNA", 28, BLUE).move_to([0, BASE1 - 1.25, 0])
        self.play(FadeIn(sample_g, scale=0.95), FadeIn(slab), run_time=0.7)
        self.at("relative of")
        ask = T("does it hold a relative of src?", 30, YELLOW).move_to([0, 1.95, 0])
        self.play(FadeIn(ask, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def sample_box():
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=10.9, height=1.5, stroke_color=BLUE,
                                          stroke_width=4), num_dashes=70)
    qm = T("?", 56, BLUE, weight=BOLD)
    return VGroup(box, qm).move_to([X0 + 10.9 / 2, BASE1 - 0.15, 0])


class S02Chicken(SpokenScene):
    def construct(self):
        PROF = PADL + SRC + PADR
        bar = strand(X0, BASE1, PROF, TW1, H1, TH1, BLUE, fo=0.25)
        seg = strand(PX, BASE1, SRC, TW1, H1, TH1, BLUE, fo=0.25, sw=0)
        probe = probe_for(PX, BASE1, SRC, TW1, H1).shift(HOVER)
        # carried over from scene 1: the probe waits over the sample, with its question
        sample_g = sample_box()
        slab = T("any sample of DNA", 28, BLUE).move_to([0, BASE1 - 1.25, 0])
        ask = T("does it hold a relative of src?", 30, YELLOW).move_to([0, 1.95, 0])
        note = T("idealised, not to scale", 22, GREY).move_to([5.2, -3.45, 0])
        self.add(note, sample_g, slab, ask, probe)

        self.at("The probe stuck")
        self.play(FadeOut(sample_g), FadeOut(slab), FadeOut(ask), FadeIn(bar), run_time=0.4)
        self.play(probe.animate.shift(DOWN * 0.9), run_time=0.4)
        self.play(recolor(probe, GREEN, 0.5), run_time=0.2)
        stuck = T("stuck", 30, GREEN, weight=BOLD).next_to(probe, UP, buff=0.2)
        self.play(FadeIn(stuck), run_time=0.3)

        lab = T("DNA from chickens that had never met the virus", 28, BLUE).move_to([0, BASE1 - 1.3, 0])
        self.at("from chickens")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)

        t1 = T("That alone proves little.", 38, YELLOW).move_to([0, 2.9, 0])
        self.at("That alone")
        self.play(FadeIn(t1, shift=DOWN * 0.1), run_time=0.6)

        t2 = T("A leading idea of the day", 34, TEXT).move_to([0, 2.9, 0])
        self.at("A leading idea")
        self.play(ReplacementTransform(t1, t2), FadeOut(stuck), run_time=0.6)

        chipv = tag("old infection", ORANGE, 28).move_to([0, 1.55, 0])
        a = arr([0, 1.2, 0], [0, 0.4, 0], ORANGE)
        self.at("old infections")
        self.play(FadeIn(chipv, shift=DOWN * 0.1), GrowArrow(a), run_time=0.7)

        ql = T("viral genes left behind in chicken chromosomes?", 28, ORANGE).move_to([0, BASE1 - 2.15, 0])
        self.at("So a match")
        self.play(FadeIn(ql, shift=UP * 0.1), run_time=0.6)
        self.at("could still be")
        self.add(seg)
        self.play(recolor(seg, ORANGE, 0.5), recolor(probe, YELLOW, 0.45), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
TW3, H3, TH3 = 0.34, 0.26, 0.45
X3 = -4.2
BASES3 = [2.0, 0.7, -0.6, -1.9]
NAMES3 = ["chicken", "duck", "quail", "emu"]
PROFS3 = [[1, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 0], [0, 0, 1, 1, 0, 1]]
PADS3 = [[0, 1, 1, 0, 1, 0], [1, 0, 1, 0, 0, 1], [0, 0, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0]]


MISS3 = {1: [2, 6], 2: [3, 8], 3: [0, 6]}   # two teeth each: no order among the three birds is drawn


def row3(i, color=BLUE):
    """bar for species i: 6 teeth of its own, the matching stretch, 6 more of its own."""
    mid = list(SRC)
    for k in MISS3.get(i, []):
        mid[k] = 0          # a tooth that does not seat: the match is close, not perfect (idealised)
    prof = PROFS3[i] + mid + PADS3[i]
    bar = strand(X3, BASES3[i], prof, TW3, H3, TH3, color, fo=0.25)
    name = T(NAMES3[i], 30, BLUE).move_to([-5.25, BASES3[i] - 0.15, 0])
    return bar, name


def probe3(i, color=YELLOW):
    return probe_for(X3 + 6 * TW3, BASES3[i], SRC, TW3, H3, thick=0.34, color=color)


class S03Birds(SpokenScene):
    def construct(self):
        bars, names = [], []
        self.add(T("idealised, not to scale", 22, GREY).move_to([5.2, -3.45, 0]))
        for i in range(4):
            b, n = row3(i)
            bars.append(b); names.append(n)
        # carried over: the chicken row with its stuck probe (the probe is green, as scene 2 left it, then settles)
        g0 = probe3(0, GREEN)
        self.add(bars[0], names[0], g0)

        self.at("tried duck")
        self.play(FadeIn(bars[1], shift=RIGHT * 0.2), FadeIn(names[1]), run_time=0.6)
        self.at("quail")
        self.play(FadeIn(bars[2], shift=RIGHT * 0.2), FadeIn(names[2]), run_time=0.6)

        emu_note = T("emu: a flightless bird, at a great evolutionary distance from the chicken", 24, TEXT)
        emu_note.move_to([0, -3.15, 0])
        self.at("flightless bird")
        self.play(FadeIn(bars[3], shift=RIGHT * 0.2), FadeIn(names[3]), FadeIn(emu_note, shift=UP * 0.1), run_time=0.7)

        self.at("stuck to all")
        probes = []
        for i in (1, 2, 3):
            p = probe3(i).shift(UP * 0.4 + RIGHT * 3.2)
            probes.append(p)
        self.play(*[FadeIn(p) for p in probes], run_time=0.3)
        self.play(AnimationGroup(*[p.animate.shift(LEFT * 3.2) for p in probes], lag_ratio=0.25), run_time=1.2)
        self.play(AnimationGroup(*[p.animate.shift(DOWN * 0.4) for p in probes], lag_ratio=0.25), run_time=0.8)
        self.play(*[recolor(p, GREEN, 0.5) for p in probes], run_time=0.4)

        close = T("the matches were close enough to stick", 28, GREEN).move_to([0, -3.15, 0])
        self.at("close enough")
        self.play(FadeOut(emu_note), FadeIn(close, shift=UP * 0.1), run_time=0.6)

        top, bot = BASES3[0] + 0.5, BASES3[3] - 0.5
        br = VGroup(Line([3.75, top, 0], [3.75, bot, 0], color=GREEN, stroke_width=5),
                    Line([3.55, top, 0], [3.75, top, 0], color=GREEN, stroke_width=5),
                    Line([3.55, bot, 0], [3.75, bot, 0], color=GREEN, stroke_width=5))
        bt = VGroup(T("conserved\nfor at least\n100 million\nyears", 26, GREEN),
                    T("Varmus's\njudgement", 22, GREY)).arrange(DOWN, buff=0.2)
        bt.move_to([5.1, (top + bot) / 2, 0])
        if bt.width > 2.5:
            bt.scale(2.5 / bt.width)
        self.at("conserved for")
        self.play(Create(br), FadeIn(bt, shift=LEFT * 0.1), run_time=0.8)

        end = T("older than any infection of chickens", 32, GREEN, weight=BOLD).move_to([0, -3.15, 0])
        self.at("A sequence shared")
        self.play(FadeOut(close), FadeIn(end, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
TW4, H4, TH4 = 0.27, 0.28, 0.55
BASE_TOP = 1.5
BASE_V = -1.2
XB = -6.2
XM = 0.4
XV = -3.5


class S04Own(SpokenScene):
    def construct(self):
        PB = PADL + SRC + PADR[:4]          # 22 teeth, same length as the bird bars
        PB = PADL + SRC + PADR[:4]
        bird = strand(XB, BASE_TOP, PB, TW4, H4, TH4, BLUE, fo=0.25)
        bird_seg = strand(XB + 8 * TW4, BASE_TOP, SRC, TW4, H4, TH4, BLUE, fo=0.4)
        bird_lab = T("birds", 28, BLUE).move_to(bird.get_center() + UP * 1.5)
        csrc = T("c-src", 28, BLUE, weight=BOLD).move_to(bird_seg.get_center() + UP * 0.95)
        mam = strand(XM, BASE_TOP, PADR[::-1] + SRC + PADL[:4], TW4, H4, TH4, BLUE, fo=0.25)
        mam_seg = strand(XM + 8 * TW4, BASE_TOP, SRC, TW4, H4, TH4, BLUE, fo=0.4)
        mam_lab = T("mammals, people included", 28, BLUE).move_to(mam.get_center() + UP * 1.5)
        note = T("idealised, not to scale", 22, GREY).move_to([5.2, -3.45, 0])
        self.add(note)

        self.at("gene of the birds")
        self.play(FadeIn(bird, shift=DOWN * 0.1), FadeIn(bird_lab), run_time=0.7)
        self.play(FadeIn(bird_seg), FadeIn(csrc), run_time=0.5)

        self.at("mammals")
        self.play(FadeIn(mam, shift=DOWN * 0.1), FadeIn(mam_seg), FadeIn(mam_lab), run_time=0.8)

        # the virus, with a gap where the gene will go
        vl = strand(XV, BASE_V, PADL, TW4, H4, TH4, ORANGE, fo=0.25)
        vr = strand(XV + 18 * TW4, BASE_V, PADR, TW4, H4, TH4, ORANGE, fo=0.25)
        slot = DashedVMobject(Rectangle(width=10 * TW4, height=TH4 + H4, stroke_color=ORANGE, stroke_width=3),
                              num_dashes=30).move_to([XV + 8 * TW4 + 5 * TW4, BASE_V - TH4 / 2 + H4 / 2, 0])
        vlab = T("virus", 28, ORANGE).move_to([XV + 13 * TW4, BASE_V - 0.95, 0])
        self.at("picked up")
        self.play(FadeIn(VGroup(vl, vr, slot, vlab)), run_time=0.6)
        copy = bird_seg.copy()
        self.add(copy)
        target = np.array([XV + 8 * TW4 + 5 * TW4, BASE_V + H4 / 2 - 0.0, 0])
        self.play(copy.animate.move_to([target[0], BASE_V - TH4 / 2 + (H4) / 2 + 0.0, 0]), run_time=0.9)
        acc = T("by accident", 28, YELLOW).move_to([2.6, 0.2, 0])
        self.at("by accident")
        self.play(FadeIn(acc, shift=UP * 0.1), recolor(copy, ORANGE, 0.45), FadeOut(slot), run_time=0.6)

        pro = tag("proto-oncogene", BLUE, 28).move_to(bird_seg.get_center() + DOWN * 1.3 + LEFT * 0.0)
        self.at("A normal gene")
        self.play(FadeOut(acc), FadeIn(pro, shift=UP * 0.1), run_time=0.7)

        vsrc = T("v-src: an altered copy", 30, RED, weight=BOLD).move_to([0, BASE_V - 1.85, 0])
        self.at("carries now")
        self.play(copy.animate.set_stroke(RED, width=5), FadeIn(vsrc, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "It was a gene of the birds themselves."
