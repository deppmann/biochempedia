"""One hair, three kinds of touch neuron  (Biochemistrypedia explainer, Sensory Systems: the LTMR classes)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = Abeta RA-LTMR endings and label
  YELLOW = Adelta-LTMR endings and label
  ORANGE = C-LTMR endings and label
  TEAL   = Abeta SA1 (Merkel-associated) endings in the touch dome
  PURPLE = terminal Schwann cell (non-neuronal)
  GREEN  = the one neuron with an arbor (field-LTMR), last scene only
  RED    = "no" (not a neuron count)
  GREY   = hair, follicle sheath, skin line, axis, neutral labels
  GOLD   = the rule to keep
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CLS = {"RA": BLUE, "AD": YELLOW, "C": ORANGE, "SA1": TEAL}
CNAME = {"RA": "Aβ RA", "AD": "Aδ", "C": "C", "SA1": "Aβ SA1"}


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def follicle(s=1.0, kind="awl", tails=False, dome=False):
    """Schematic hair follicle (side view): sheath, shaft, skin line, lanceolate pickets along the shaft.
    Built about the origin; caller moves the group."""
    top = {"guard": 2.5, "awl": 2.2, "zig": 1.9}[kind]
    pat = {"guard": ["RA"], "awl": ["RA", "AD", "C"], "zig": ["AD", "C"]}[kind]
    sw = max(2.0, 4 * s)
    sheath = RoundedRectangle(corner_radius=0.3 * s, width=1.5 * s, height=2.6 * s, stroke_color=GREY,
                              stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    if kind == "zig":
        pts = [(0, -1.0), (0, 1.3), (0.2, 1.45), (-0.2, 1.6), (0.0, top)]
        shaft = VMobject(stroke_color=GREY, stroke_width=3 + 4 * s, stroke_opacity=0.85)
        shaft.set_points_as_corners([np.array([x * s, y * s, 0]) for x, y in pts])
    else:
        shaft = Line([0, -1.0 * s, 0], [0, top * s, 0], color=GREY, stroke_width=3 + 4 * s, stroke_opacity=0.85)
    half = (2.2 if dome else 1.3) * s
    skin = Line([-1.3 * s, 1.3 * s, 0], [half, 1.3 * s, 0], color=GREY, stroke_width=3)
    n = len(pat)
    pk, tl = [], []
    for i, c in enumerate(pat):
        x = (i - (n - 1) / 2) * 0.32 * s if n > 1 else -0.3 * s
        p = RoundedRectangle(corner_radius=0.05 * s, width=0.16 * s, height=2.0 * s, stroke_width=0,
                             fill_color=CLS[c], fill_opacity=0.95).move_to([x, 0.0, 0])
        pk.append((c, p))
        if tails:
            tl.append((c, Line([x, -1.0 * s, 0], [x, -1.75 * s, 0], color=CLS[c], stroke_width=4)))
    parts = [skin, sheath, shaft] + [p for _, p in pk] + [t for _, t in tl]
    extra = []
    if dome:
        cx = 1.45 * s
        d = Sector(radius=0.5 * s, angle=PI, start_angle=0, stroke_color=TEAL, stroke_width=3,
                   fill_color=TEAL, fill_opacity=0.28).move_to([cx, 1.3 * s + 0.25 * s, 0])
        e = RoundedRectangle(corner_radius=0.05 * s, width=0.12 * s, height=1.0 * s, stroke_width=0,
                             fill_color=TEAL, fill_opacity=0.95).move_to([cx, 1.3 * s - 0.5 * s, 0])
        extra = [d, e]
        parts += extra
    g = VGroup(*parts)
    g.pk, g.tl, g.sheath, g.shaft, g.skin, g.s, g.extra = pk, tl, sheath, shaft, skin, s, extra
    g.pickets = VGroup(*[p for _, p in pk])
    return g


def place(f, x, y):
    """move a follicle so the centre of its SHEATH (not the whole group) sits at (x, y)."""
    f.shift(np.array([x, y, 0.0]) - f.sheath.get_center())
    return f


def schwann(f, s):
    b = Ellipse(width=1.7 * s, height=1.1 * s, stroke_color=PURPLE, stroke_width=3,
                fill_color=PURPLE, fill_opacity=0.3)
    b.move_to(f.sheath.get_center() + UP * 0.2 * s)
    b.set_z_index(-1)
    return b


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def label_line(a, b, color=GREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w)


def cls_text(c, size=30):
    return T(CNAME[c], size, CLS[c], weight=BOLD)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The low-threshold mechanoreceptors"
    TITLE = "One hair, three kinds of touch neuron"


# ---------------------------------------------------------------------------------------------
class S01Fence(SpokenScene):
    """follicle fades in; three colours of pickets; signals run down the tails at different speeds."""

    def construct(self):
        s = 1.35
        fx, fy = -2.2, 0.15
        f = place(follicle(s, "awl", tails=True), fx, fy)
        place_t = T("mouse trunk skin", 28, GREY).move_to([4.3, 2.9, 0])
        self.at("mouse's back")
        self.play(FadeIn(f.skin), FadeIn(f.sheath), Create(f.shaft), FadeIn(place_t), run_time=1.2)
        self.at("three kinds of touch neuron")
        first = [p for c, p in f.pk[:3]]
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in first], lag_ratio=0.4), run_time=0.9)
        self.play(*[Create(t) for c, t in f.tl], run_time=0.8)
        name = chip("awl/auchene hair", GREY, size=26).move_to([4.3, 1.4, 0])
        ln = label_line([name.get_left()[0] - 0.05, 1.4, 0], [fx + 0.06, fy + 1.95 * s, 0], GREY)
        self.at("It is called")
        self.play(FadeIn(name), Create(ln), run_time=0.6)
        arr_ = arr([fx, fy - 1.75 * s - 0.15, 0], [fx, fy - 1.75 * s - 0.75, 0], GREY)
        sc = T("to the spinal cord", 26, GREY).next_to(arr_, RIGHT, buff=0.25)
        self.at("its own signal")
        dots, anims = [], []
        for (c, p), (_, t) in zip(f.pk, f.tl):
            x = p.get_center()[0]
            d = Dot(radius=0.08, color=WHITE).move_to([x, fy + 1.0 * s, 0])
            dots.append(d)
            dur = {"RA": 0.9, "AD": 1.7, "C": 2.9}[c]
            anims.append(d.animate(run_time=dur, rate_func=linear).move_to([x, fy - 1.75 * s, 0]))
        note = T("speeds not to scale", 22, GREY).move_to([4.3, -2.3, 0])
        self.play(FadeIn(arr_), FadeIn(sc), FadeIn(note), *[FadeIn(d) for d in dots], run_time=0.4)
        self.play(AnimationGroup(*anims))
        self.play(*[FadeOut(d) for d in dots], run_time=0.3)
        self.at("Why build a sense")
        self.play(Indicate(f.pickets, color=WHITE, scale_factor=1.04), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pickets(SpokenScene):
    """lanceolate ending = picket; terminal Schwann cell between; the three classes named."""

    def construct(self):
        s = 1.4
        fx, fy = -2.6, 0.0
        f = place(follicle(s, "awl", tails=True), fx, fy)
        self.add(f)
        lab_x = 0.6
        pick = f.pk[2][1]
        px = pick.get_center()[0]
        self.at("axon branch running")
        hl = SurroundingRectangle(pick, color=WHITE, buff=0.05, stroke_width=3)
        yl = fy + 0.55 * s
        t1 = T("lanceolate ending", 30, WHITE).move_to([lab_x + 1.55, yl, 0])
        l1 = label_line([t1.get_left()[0] - 0.12, yl, 0], [pick.get_right()[0] + 0.1, yl, 0], WHITE)
        self.play(Create(hl), FadeIn(t1), Create(l1), run_time=0.7)
        self.at("parallel to the hair shaft")
        top_y = fy + 2.1 * s
        ext = DashedLine([px, fy + 1.0 * s, 0], [px, top_y, 0], color=WHITE, dash_length=0.14, stroke_width=3)
        tp = T("hair shaft", 26, GREY).move_to([fx - 2.9, fy + 1.9 * s, 0])
        lp = label_line([tp.get_right()[0] + 0.1, fy + 1.9 * s, 0], [fx - 0.08, fy + 1.9 * s, 0], GREY)
        self.play(Create(ext), FadeIn(tp), Create(lp), run_time=0.9)
        self.at("one picket in a fence")
        self.play(FadeOut(ext), LaggedStart(*[Indicate(p, color=WHITE, scale_factor=1.15) for _, p in f.pk],
                                            lag_ratio=0.15), run_time=1.4)
        self.play(FadeOut(hl), FadeOut(t1), FadeOut(l1), FadeOut(tp), FadeOut(lp), run_time=0.4)
        self.at("terminal Schwann cells")
        sch = schwann(f, s)
        ys = fy - 0.9
        t2 = T("terminal Schwann cell", 30, PURPLE).move_to([lab_x + 1.95, ys, 0])
        l2 = label_line([t2.get_left()[0] - 0.12, ys, 0], [sch.get_right()[0] - 0.12, ys, 0], PURPLE)
        self.play(FadeIn(sch), FadeIn(t2), Create(l2), run_time=0.8)
        self.at("interleave")
        self.play(Indicate(sch, color=PURPLE, scale_factor=1.06), run_time=1.0)
        self.at("neuronal cells")
        t3 = T("non-neuronal", 26, GREY).move_to([lab_x + 1.0, ys - 0.55, 0])
        self.play(FadeIn(t3), run_time=0.5)
        self.at("three classes")
        self.play(FadeOut(t3), run_time=0.3)
        chips = {c: chip(CNAME[c], CLS[c], size=28) for c in ("RA", "AD", "C")}
        row = VGroup(*chips.values()).arrange(RIGHT, buff=0.4).move_to([lab_x + 3.2, -2.7, 0])
        for c in ("RA", "AD", "C"):
            self.at({"RA": "beta", "AD": "delta", "C": "and C"}[c])
            self.play(FadeIn(chips[c], shift=UP * 0.15),
                      Indicate(VGroup(*[p for cc, p in f.pk if cc == c]), color=CLS[c], scale_factor=1.25),
                      run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Speed(SpokenScene):
    """follicle shrinks left; mean conduction velocity bars grow to scale (the lesson's numbers)."""

    def construct(self):
        s = 0.95
        f = place(follicle(s, "awl", tails=True), -4.9, 0.0)
        self.add(f)
        x0, k = -1.0, 0.32     # axis origin and units per m/s
        head = T("mean conduction velocity", 30, TEXT).move_to([2.0, 3.1, 0])
        sub = T("mouse hairy skin, ex vivo preparation", 24, GREY).move_to([2.0, 2.55, 0])
        ay = -2.0
        axis = Line([x0, ay, 0], [x0 + 15 * k, ay, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[Line([x0 + v * k, ay, 0], [x0 + v * k, ay + 0.1, 0], color=GREY, stroke_width=3) for v in (0, 5, 10, 15)])
        tl = VGroup(*[M(str(v), 22, GREY).move_to([x0 + v * k, ay - 0.4, 0]) for v in (0, 5, 10, 15)])
        unit = T("m/s", 22, GREY).move_to([x0 + 15 * k + 0.6, ay - 0.4, 0])
        self.at("differ in speed")
        self.play(FadeIn(head), FadeIn(sub), Create(axis), FadeIn(ticks), FadeIn(tl), FadeIn(unit), run_time=0.9)
        rows = [("RA", 13.6, "13.6 ± 2.7", 1.2), ("AD", 5.8, "5.8 ± 0.9", 0.0), ("C", 0.58, "0.58 ± 0.02", -1.2)]
        bars = {}
        for c, v, txt, y in rows:
            w = max(v * k, 0.04)
            bar = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=CLS[c], fill_opacity=0.9)
            bar.move_to([x0 + w / 2, y, 0])
            lab = cls_text(c, 32).move_to([x0 - 0.3, y, 0]).align_to([x0 - 0.3, 0, 0], RIGHT)
            val = M(txt, 28, CLS[c]).next_to(bar, RIGHT, buff=0.2)
            bars[c] = (bar, lab, val)
        cues = {"RA": "RA neurons conduct", "AD": "The A delta neurons", "C": "The C neurons"}
        for c, v, txt, y in rows:
            bar, lab, val = bars[c]
            self.at(cues[c])
            self.play(FadeIn(lab), Indicate(VGroup(*[p for cc, p in f.pk if cc == c]), color=CLS[c], scale_factor=1.4),
                      GrowFromEdge(bar, LEFT), run_time=1.0)
            self.play(FadeIn(val), run_time=0.4)
        self.at("by far the slowest")
        self.play(Indicate(VGroup(*bars["C"]), color=ORANGE, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Map(SpokenScene):
    """label -> record -> image whole mounts; then three hair types, each with its own mix."""

    def construct(self):
        steps = [chip(t, GREY, size=26, pad=0.12) for t in ("genetic label", "recording", "SA1: Merkel stain", "whole mounts")]
        sa = lambda: arr([0, 0, 0], [0.55, 0, 0], GREY)
        row = VGroup(steps[0], sa(), steps[1], sa(), steps[2], sa(), steps[3]).arrange(RIGHT, buff=0.12)
        row.scale_to_fit_width(min(row.width, 12.2))
        row.move_to([0, 0.0, 0])
        q = T("which endings belong to which neurons?", 34, TEXT).move_to([0, 1.9, 0])
        self.at("How did anyone learn")
        self.play(FadeIn(q), run_time=0.8)
        self.at("labeled the")
        self.play(FadeIn(steps[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("confirmed their identity")
        self.play(GrowArrow(row[1]), FadeIn(steps[1], shift=RIGHT * 0.2), run_time=0.6)
        self.at("Merkel cells")
        self.play(GrowArrow(row[3]), FadeIn(steps[2], shift=RIGHT * 0.2), run_time=0.6)
        self.at("whole mounts")
        self.play(GrowArrow(row[5]), FadeIn(steps[3], shift=RIGHT * 0.2), run_time=0.6)
        self.wait(self.beat(0.03))
        s = 0.95
        cy = 0.95
        xs = [-4.4, 0.0, 4.2]
        kinds = ["guard", "awl", "zig"]
        names = ["guard hair", "awl/auchene hair", "zigzag hair"]
        fl, nm = [], []
        for x, k, n in zip(xs, kinds, names):
            f = place(follicle(s, k, dome=(k == "guard")), x, cy)
            fl.append(f)
            nm.append(T(n, 28, TEXT).move_to([x, cy - 1.3 * s - 0.4, 0]))
        chips = [
            [("RA", "Aβ RA"), ("SA1", "Aβ SA1, touch dome")],
            [("RA", "Aβ RA"), ("AD", "Aδ"), ("C", "C")],
            [("AD", "Aδ"), ("C", "C")],
        ]
        stacks = []
        for x, lst in zip(xs, chips):
            cs = [chip(t, CLS[c], size=24, pad=0.1) for c, t in lst]
            g = VGroup(*cs).arrange(DOWN, buff=0.1).move_to([x, -2.35, 0])
            g.align_to([0, -1.35, 0], UP)
            stacks.append(g)
        self.play(FadeOut(q), FadeOut(row), run_time=0.5)
        for i, cue in enumerate(["Guard hairs carry", "keen hairs carry", "Zigzag hairs carry"]):
            self.at(cue)
            f = fl[i]
            self.play(FadeIn(f.skin), FadeIn(f.sheath), Create(f.shaft), FadeIn(nm[i]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p) for _, p in f.pk], lag_ratio=0.15), run_time=0.7)
            if i == 0:
                self.play(FadeIn(stacks[0][0], shift=UP * 0.1), run_time=0.4)
                self.at("touch dome")
                self.play(*[FadeIn(m) for m in f.extra], FadeIn(stacks[0][1], shift=UP * 0.1), run_time=0.7)
            else:
                self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in stacks[i]], lag_ratio=0.35), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Count(SpokenScene):
    """idealized 100-follicle patch: 1 : 23 : 76; associations per class; total 223."""

    def construct(self):
        tag = T("idealized patch of 100 follicles, approximate ratio", 26, GREY).move_to([0, 3.1, 0])
        ch = {k: chip(t, GREY, size=30) for k, t in (("g", "1 guard"), ("a", "23 awl/auchene"), ("z", "76 zigzag"))}
        top = VGroup(ch["g"], ch["a"], ch["z"]).arrange(RIGHT, buff=0.6).move_to([0, 2.1, 0])
        self.at("Now count")
        self.play(FadeIn(tag), run_time=0.6)
        self.at("three hair types")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in ch.values()], lag_ratio=0.3), run_time=1.6)
        specs = [("RA", "guard + awl/auchene", "1 + 23 = 24", ("g", "a"), 0.8),
                 ("SA1", "guard only", "1", ("g",), 0.0),
                 ("AD", "awl/auchene + zigzag", "23 + 76 = 99", ("a", "z"), -0.8),
                 ("C", "awl/auchene + zigzag", "23 + 76 = 99", ("a", "z"), -1.6)]
        cues = ["found at 24", "beta SA1 is", "A delta is found", "C is found"]
        for (c, hw, eq, hl, y), cue in zip(specs, cues):
            a = cls_text(c, 32).move_to([-5.2, y, 0]).align_to([-6.0, 0, 0], LEFT)
            b = T(hw, 26, GREY).move_to([-1.9, y, 0]).align_to([-3.3, 0, 0], LEFT)
            e = M(eq, 32, CLS[c]).move_to([4.0, y, 0]).align_to([2.4, 0, 0], LEFT)
            self.at(cue)
            self.play(FadeIn(a), FadeIn(b), *[Indicate(ch[h], color=CLS[c], scale_factor=1.12) for h in hl], run_time=0.8)
            self.play(Write(e), run_time=0.6)
        bar = Line([-6.0, -2.2, 0], [6.0, -2.2, 0], color=GREY, stroke_width=2)
        tot_l = T("associations", 32, TEXT).move_to([-5.2, -2.85, 0]).align_to([-6.0, 0, 0], LEFT)
        tot_e = M("24 + 1 + 99 + 99 = 223", 34, TEXT).move_to([3.0, -2.85, 0])
        self.at("The total is")
        self.play(Create(bar), FadeIn(tot_l), Write(tot_e), run_time=1.2)
        self.play(Indicate(tot_e, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mini_fol(x, y):
    sheath = RoundedRectangle(corner_radius=0.22, width=0.8, height=1.6, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    shaft = Line([x, y - 0.65, 0], [x, y + 1.3, 0], color=GREY, stroke_width=6, stroke_opacity=0.85)
    skin = Line([x - 0.7, y + 0.8, 0], [x + 0.7, y + 0.8, 0], color=GREY, stroke_width=3)
    r = Ellipse(width=1.2, height=0.5, stroke_color=GREEN, stroke_width=4).move_to([x, y - 0.05, 0])
    return VGroup(skin, sheath, shaft), r


class S06Rule(SpokenScene):
    """223 is not a neuron count; one neuron reaches many follicles; the rule."""

    def construct(self):
        q1 = M("223", 54, TEXT)
        q2 = T("a count of neurons?", 34, TEXT)
        qg = VGroup(q1, q2).arrange(RIGHT, buff=0.35).move_to([-3.3, 3.0, 0])
        self.at("Is 223")
        self.play(FadeIn(qg, shift=DOWN * 0.1), run_time=0.7)
        no = T("No", 40, RED, weight=BOLD).next_to(qg, RIGHT, buff=0.5)
        self.at("No")
        self.play(FadeIn(no, scale=1.2), qg.animate.set_opacity(0.55), run_time=0.5)
        xs = [-2.2, -0.4, 1.4, 3.2, 5.0]
        y = -0.15
        soma = Circle(radius=0.4, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.3).move_to([-5.4, -1.8, 0])
        bus = Line([-5.0, -1.8, 0], [5.0, -1.8, 0], color=GREEN, stroke_width=4)
        fols, rings, brs = [], [], []
        for x in xs:
            body, r = mini_fol(x, y)
            fols.append(body); rings.append(r)
            brs.append(Line([x, -1.8, 0], [x, y - 0.8, 0], color=GREEN, stroke_width=4))
        dots = T("…", 40, GREEN).move_to([6.0, -1.4, 0])
        lab = VGroup(T("circumferential endings of one mouse field-LTMR", 26, GREEN),
                     T("reached 20 to 180 follicles", 26, GREEN)).arrange(DOWN, buff=0.12).move_to([0.2, -2.85, 0])
        self.at("One neuron contacts")
        self.play(FadeIn(soma), *[FadeIn(b) for b in fols], run_time=0.8)
        self.play(Create(bus), LaggedStart(*[Create(b) for b in brs], lag_ratio=0.2),
                  LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(dots), run_time=1.8)
        self.at("A single mouse field")
        self.play(FadeIn(lab), run_time=0.7)
        ratio = M("1 : 23 : 76", 36, GREY).move_to([3.1, 3.0, 0])
        rl = T("hairs", 28, GREY).next_to(ratio, RIGHT, buff=0.3)
        self.at("the ratio counts hairs")
        self.play(FadeIn(ratio), FadeIn(rl), run_time=0.7)
        self.at("how often each class")
        self.play(Indicate(qg, color=TEXT, scale_factor=1.05), run_time=0.8)
        rule = T("Endings at a hair are not a count of neurons", 36, GOLD, font=TITLE_FONT)
        fit(rule, max_w=12.0)
        rule.move_to([0, 2.7, 0])
        self.at("Keep this rule")
        self.play(FadeOut(no), FadeOut(qg), FadeOut(ratio), FadeOut(rl), FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Endings at a hair are not a count of neurons."
