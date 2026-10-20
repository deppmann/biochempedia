"""How microbes multiply: copies are made by cells  (Biochemistrypedia explainer, high school Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a bacterium / a host cell (the outline of the cell)
  TEAL   = the cell's own DNA (chromosome), drawn as a bar
  PURPLE = a virus: phage, viral DNA, viral parts, the herpes virus
  ORANGE = a plasmid (small extra DNA)
  GREEN  = calculated model numbers and the model line ("not a count")
  YELLOW = the time / the count to read (20 minutes, the question)
  RED    = what stops or ends: wastes, food runs low, the cell bursts and dies
  PINK   = the cold sore on the skin
  GREY   = outlines, axes, the skin and nerve-cell blocks, de-emphasised text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FA8"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cellbox(w, h, color=BLUE, fill=0.14):
    return RoundedRectangle(corner_radius=min(w, h) * 0.42, width=w, height=h, stroke_color=color,
                            stroke_width=4, fill_color=color, fill_opacity=fill)


def dnabar(w, color=TEAL, h=0.26):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.9)


def lab(text, size=26, color=GREY, **kw):
    return T(text, size, color, **kw)


def phage(s=1.0):
    head = Square(side_length=0.8 * s, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35)
    tail = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.7 * s, color=PURPLE, stroke_width=5)
    foot = Line(tail.get_end() + LEFT * 0.3 * s, tail.get_end() + RIGHT * 0.3 * s, color=PURPLE, stroke_width=5)
    g = VGroup(head, tail, foot)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=7),
                  Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=7))


def banner(text, color=GREY, size=34):
    return T(text, size, color, font=TITLE_FONT).to_edge(UP, buff=0.45)


class S00Title(TitleCard):
    LESSON = "How microbes multiply"
    TITLE = "Copies made by cells"


# ---------------------------------------------------------------------------------------------
class S01Two(SpokenScene):
    """a bacterium splits on a 20-minute clock; a cold sore heals and comes back; the two questions."""

    def construct(self):
        LX, RX, Y = -3.4, 3.5, 0.7
        hdrL = T("a bacterium", 32, BLUE, weight=BOLD).move_to([LX, 3.05, 0])
        hdrR = T("a cold sore", 32, PINK, weight=BOLD).move_to([RX, 3.05, 0])
        # --- left: one cell splits ---
        c0 = cellbox(3.6, 2.2).move_to([LX, Y, 0])
        b0 = dnabar(2.0).move_to(c0)
        one = VGroup(c0, b0)
        one_lbl = lab("one E. coli cell", 28, BLUE).move_to([LX, Y - 1.6, 0])
        self.at("best laboratory")
        best = lab("best laboratory conditions", 24, GREY).move_to([LX, Y + 1.75, 0])
        self.play(FadeIn(hdrL), FadeIn(best), run_time=0.6)
        self.at("coli cell")
        self.play(FadeIn(one, scale=0.9), FadeIn(one_lbl), run_time=0.6)
        c1 = cellbox(2.7, 2.2).move_to([LX - 1.5, Y, 0]); b1 = dnabar(1.5).move_to(c1)
        c2 = cellbox(2.7, 2.2).move_to([LX + 1.5, Y, 0]); b2 = dnabar(1.5).move_to(c2)
        two_lbl = lab("two cells", 28, BLUE).move_to([LX, Y - 1.6, 0])
        self.at("split into two")
        self.play(ReplacementTransform(one, VGroup(c1, b1, c2, b2)), ReplacementTransform(one_lbl, two_lbl), run_time=0.9)
        clock = chip("about every 20 minutes", YELLOW, size=26).move_to([LX, Y - 2.5, 0])
        self.at("20 minutes")
        self.play(FadeIn(clock, shift=UP * 0.15), run_time=0.6)
        # --- right: skin block, sore appears, heals, returns ---
        skin = Rectangle(width=5.2, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.25).move_to([RX, Y, 0])
        skin_lbl = lab("skin", 28, GREY).move_to([RX, Y - 1.6, 0])
        sore = Ellipse(width=1.6, height=0.9, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                       fill_opacity=0.85).move_to([RX + 0.8, Y + 0.2, 0])
        self.at("A cold sore")
        state = lab("sore", 26, PINK).move_to([RX, Y - 2.5, 0])
        self.play(FadeIn(hdrR), FadeIn(skin), FadeIn(skin_lbl), FadeIn(sore, scale=0.6), FadeIn(state), run_time=0.7)
        healed = lab("healed", 26, GREY).move_to([RX, Y - 2.5, 0])
        self.at("can heal")
        self.play(sore.animate.set_opacity(0.0).set_stroke(opacity=0.0), ReplacementTransform(state, healed), run_time=0.8)
        back = lab("comes back", 26, PINK).move_to([RX, Y - 2.5, 0])
        self.at("come back later")
        self.play(sore.animate.set_opacity(0.85).set_stroke(opacity=1.0), ReplacementTransform(healed, back), run_time=0.8)
        spot = chip("same spot", YELLOW, size=24).move_to([RX + 0.8, Y + 1.85, 0])
        pt = arr(spot.get_bottom(), sore.get_top() + UP * 0.05, YELLOW, w=4)
        self.at("same spot")
        self.play(FadeIn(spot), GrowArrow(pt), run_time=0.5)
        # --- the questions ---
        self.at("How do bacteria")
        self.play(FadeOut(VGroup(best, clock, spot, pt, back, skin_lbl, two_lbl)), run_time=0.5)
        q1 = T("How do bacteria and viruses make more of themselves?", 32, YELLOW)
        fit(q1, max_w=12.2)
        q1.move_to([0, -2.3, 0])
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.8)
        q2 = T("Why do some infections come back years later?", 32, PINK)
        fit(q2, max_w=12.2)
        q2.move_to([0, -3.1, 0])
        self.at("years later")
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Split(SpokenScene):
    """binary fission in steps, then conjugation: a plasmid moves, still two cells."""

    def construct(self):
        title = banner("binary fission", BLUE)
        self.at("binary fission")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        Y = -0.2
        big0 = cellbox(5.0, 3.0).move_to([0, Y, 0])
        bar0 = dnabar(2.8).move_to(big0)
        dna_lbl = lab("DNA", 26, TEAL).next_to(bar0, DOWN, buff=0.25)
        self.play(FadeIn(big0), FadeIn(bar0), FadeIn(dna_lbl), run_time=0.7)
        # grows
        big1 = cellbox(8.6, 3.0).move_to([0, Y, 0])
        self.at("One cell grows")
        self.play(Transform(big0, big1), bar0.animate.become(dnabar(3.0).move_to([0, Y, 0])),
                  dna_lbl.animate.move_to([0, Y - 0.55, 0]), run_time=1.0)
        # copies
        bL = dnabar(2.8).move_to([-2.2, Y + 0.05, 0]); bR = dnabar(2.8).move_to([2.2, Y + 0.05, 0])
        copy_lbl = lab("DNA copied", 26, TEAL).move_to([0, Y - 2.1, 0])
        self.at("copies its")
        self.play(ReplacementTransform(bar0, VGroup(bL, bR)), FadeOut(dna_lbl), FadeIn(copy_lbl), run_time=0.8)
        # splits
        c1 = cellbox(4.1, 3.0).move_to([-2.25, Y, 0]); c2 = cellbox(4.1, 3.0).move_to([2.25, Y, 0])
        n2 = lab("two cells", 28, BLUE).move_to([0, Y - 2.1, 0])
        self.at("splits into two")
        self.play(ReplacementTransform(big0, VGroup(c1, c2)), ReplacementTransform(copy_lbl, n2), run_time=0.9)
        # complete copy
        self.at("complete copy")
        self.play(Indicate(bL, color=TEAL, scale_factor=1.1), Indicate(bR, color=TEAL, scale_factor=1.1), run_time=0.8)
        comp = lab("each gets a complete copy", 28, TEAL).move_to([0, Y + 2.1, 0])
        self.play(FadeIn(comp), run_time=0.4)
        same = lab("usually identical", 28, YELLOW).move_to([0, Y - 2.8, 0])
        self.at("usually identical")
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
        # conjugation
        self.at("Conjugation is different")
        t2 = banner("conjugation", ORANGE)
        self.play(FadeOut(VGroup(comp, same, n2)), ReplacementTransform(title, t2), run_time=0.6)
        self.play(VGroup(c1, bL).animate.shift(LEFT * 0.0), run_time=0.01)
        pl = dnabar(1.0, ORANGE, 0.28).move_to([-2.25, Y - 0.85, 0])
        pl_lbl = lab("plasmid", 28, ORANGE).move_to([-2.25, Y - 2.1, 0])
        self.at("passes a plasmid")
        self.play(FadeIn(pl, scale=0.7), FadeIn(pl_lbl), run_time=0.5)
        self.at("small extra")
        self.play(pl_lbl.animate.become(lab("plasmid: small extra DNA", 26, ORANGE).move_to([-2.25, Y - 2.1, 0])), run_time=0.4)
        self.at("to another")
        self.play(pl.animate.move_to([2.25, Y - 0.85, 0]), pl_lbl.animate.move_to([0, Y - 2.1, 0]), run_time=1.1)
        self.at("still two cells")
        two = lab("still two cells", 30, BLUE).move_to([0, Y + 2.1, 0])
        self.play(FadeIn(two), run_time=0.4)
        self.at("new genes")
        ng = lab("new genes", 28, ORANGE).move_to([2.25, Y + 1.05, 0])
        self.play(c2.animate.set_stroke(ORANGE), FadeIn(ng), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Double(SpokenScene):
    """model population doubling every 20 minutes: bars computed from 100 x 2^n; then one cell, 21 doublings."""

    def construct(self):
        title = banner("doubling time: a model", GREEN)
        self.at("Doubling time")
        dc = cellbox(2.4, 1.5).move_to([-3.2, 0.3, 0])
        d1 = cellbox(2.0, 1.5).move_to([2.4, 0.3, 0]); d2 = cellbox(2.0, 1.5).move_to([4.5, 0.3, 0])
        dar = arr([-1.6, 0.3, 0], [1.1, 0.3, 0], GREY)
        dlab = chip("doubles: ×2", YELLOW, size=30).move_to([-0.3, 1.3, 0])
        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(dc), run_time=0.5)
        self.at("to double")
        self.play(GrowArrow(dar), FadeIn(dlab), ReplacementTransform(dc.copy(), VGroup(d1, d2)), run_time=0.8)
        vals = [100 * 2 ** n for n in range(7)]
        base_y, top_h = -2.1, 3.7
        xs = [-5.4 + 1.8 * i for i in range(7)]
        axis = Line([-6.2, base_y, 0], [6.2, base_y, 0], color=GREY, stroke_width=3)
        bars, nums, ticks = [], [], []
        for i, (v, x) in enumerate(zip(vals, xs)):
            h = max(0.08, top_h * v / vals[-1])
            b = Rectangle(width=1.1, height=h, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.45)
            b.move_to([x, base_y + h / 2, 0])
            n = M(f"{v:,}", 24, TEXT).next_to(b, UP, buff=0.12)
            tk = M(f"{20 * i}", 22, GREY).move_to([x, base_y - 0.35, 0])
            bars.append(b); nums.append(n); ticks.append(tk)
        unit = lab("minutes", 24, GREY).move_to([0, base_y - 0.85, 0])
        self.at("model population")
        self.play(FadeOut(VGroup(dc, d1, d2, dar, dlab)), run_time=0.3)
        self.play(Create(axis), FadeIn(bars[0]), FadeIn(nums[0]), FadeIn(ticks[0]), FadeIn(unit), run_time=0.8)
        self.at("doubles every")
        self.play(*[FadeIn(t) for t in ticks[1:]], run_time=0.6)
        self.at("Two hours is")
        six = chip("6 doublings in 2 hours", YELLOW, size=26).move_to([-3.4, 2.35, 0])
        self.play(FadeIn(six), run_time=0.4)
        for i in range(1, 7):
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(nums[i], shift=UP * 0.1), run_time=0.3)
        self.at("100 cells become")
        self.play(Indicate(nums[-1], color=YELLOW, scale_factor=1.25), run_time=0.8)
        # one E. coli cell
        self.at("From one")
        grp = VGroup(axis, *bars, *nums, *ticks, unit, six)
        self.play(FadeOut(grp), run_time=0.5)
        start = chip("1 cell", BLUE, size=36).move_to([-5.2, 0.4, 0])
        mid = VGroup(chip("21 doublings", YELLOW, size=30), chip("7 hours", YELLOW, size=30)).arrange(DOWN, buff=0.3).move_to([-0.7, 0.4, 0])
        end = chip("2,097,152 cells", GREEN, size=36).move_to([3.9, 0.4, 0])
        a1 = arr([-4.4, 0.4, 0], [-2.9, 0.4, 0], GREY)
        a2 = arr([1.5, 0.4, 0], [2.0, 0.4, 0], GREY)
        self.play(FadeIn(start), run_time=0.4)
        self.at("21 doublings")
        self.play(GrowArrow(a1), FadeIn(mid[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("hours give")
        self.play(FadeIn(mid[1], shift=RIGHT * 0.2), run_time=0.4)
        self.at("more than")
        self.play(GrowArrow(a2), FadeIn(end, shift=RIGHT * 0.2), run_time=0.6)
        self.at("calculated numbers")
        note = lab("calculated by the model, not counted", 32, GREEN).move_to([0, -1.6, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Levels(SpokenScene):
    """sketch: endless-doubling model line vs a real-culture curve with lag, fast growth, levelling off."""

    def construct(self):
        title = banner("a sketch, not data", GREY)
        ax_o = np.array([-5.6, -2.5, 0])
        W, H = 11.0, 5.0
        xax = Line(ax_o, ax_o + [W, 0, 0], color=GREY, stroke_width=3)
        yax = Line(ax_o, ax_o + [0, H, 0], color=GREY, stroke_width=3)
        xl = lab("time", 26, GREY).move_to(ax_o + [W - 0.5, -0.4, 0])
        yl = lab("number of cells", 26, GREY).move_to(ax_o + [1.5, H + 0.15, 0])
        unit = lab("relative units, in this sketch", 24, GREY).move_to(ax_o + [W / 2 - 1.5, -0.4, 0])

        def P(t, y):
            return ax_o + [W * t, H * y, 0]
        N0, r = 0.012, 0.0

        K = 0.80
        n0 = 0.012
        rr = 7.0
        def model(t):
            return n0 * np.exp(rr * t)
        def real(t):
            return K / (1 + (K / n0 - 1) * np.exp(-rr * t))
        tm = np.log(0.97 / n0) / rr
        mline = ParametricFunction(lambda t: P(t, model(t)), t_range=[0, tm], color=GREEN, stroke_width=5)
        mline = DashedVMobject(mline, num_dashes=40)
        rline = ParametricFunction(lambda t: P(t, real(t)), t_range=[0, 1.0], color=BLUE, stroke_width=6)
        self.add(title, xax, yax, xl, yl, unit)
        self.at("The model assumes")
        mlab = lab("model: endless food", 26, GREEN).move_to(P(0.34, 0.8))
        self.play(Create(mline), FadeIn(mlab), run_time=2.0)
        self.at("Real cultures differ")
        rlab = lab("real culture", 26, BLUE).move_to(P(0.9, 0.5) + [0, 0.0, 0])
        self.play(Create(rline), run_time=0.9)
        self.play(FadeOut(mline), FadeOut(mlab), run_time=0.01)
        # stage zones
        t_lag, t_fast_end = 0.42, 0.72
        d1 = DashedLine(P(t_lag, 0), P(t_lag, 0.9), color=GREY, stroke_width=2)
        d2 = DashedLine(P(t_fast_end, 0), P(t_fast_end, 0.9), color=GREY, stroke_width=2)
        self.at("First comes a lag")
        lag = chip("lag", YELLOW, size=28).move_to(P(0.2, 0.3))
        self.play(FadeIn(lag), FadeIn(d1), run_time=0.5)
        self.at("barely rises")
        self.play(Indicate(lag, color=YELLOW), run_time=0.6)
        self.at("fast growth")
        fast = chip("fast growth", YELLOW, size=28).move_to(P(0.60, 0.10))
        self.play(FadeIn(fast), FadeIn(d2), run_time=0.5)
        self.at("food runs low")
        low = chip("food runs low", RED, size=28).move_to(P(0.86, 0.96))
        self.play(FadeIn(low, shift=DOWN * 0.1), run_time=0.5)
        self.at("wastes build up")
        waste = chip("wastes build up", RED, size=28).move_to(P(0.86, 0.48))
        self.play(FadeIn(waste, shift=DOWN * 0.1), run_time=0.5)
        self.at("levels off")
        lv = lab("growth levels off", 30, BLUE, weight=BOLD).move_to(P(0.86, 0.30))
        self.play(FadeIn(lv, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Lytic(SpokenScene):
    """a virus cannot copy itself; the lytic cycle in four steps inside a host cell."""

    def construct(self):
        ph = phage(1.6).move_to([-4.6, 0.6, 0])
        ph_lbl = lab("virus", 32, PURPLE, weight=BOLD).next_to(ph, UP, buff=0.3)
        self.play(FadeIn(ph, scale=0.9), FadeIn(ph_lbl), run_time=0.7)
        # cannot split, grow, make
        items = []
        for i, w in enumerate(["split", "grow", "make anything"]):
            c = chip(w, GREY, size=30).move_to([0.6, 2.2 - 1.3 * i, 0])
            x = cross(c.get_right() + [0.6, 0, 0], 0.25)
            items.append((c, x))
        self.at("cannot split")
        self.play(FadeIn(items[0][0]), run_time=0.3)
        self.play(Create(items[0][1]), run_time=0.3)
        self.at("grow")
        self.play(FadeIn(items[1][0]), run_time=0.3)
        self.play(Create(items[1][1]), run_time=0.3)
        self.at("make anything")
        self.play(FadeIn(items[2][0]), run_time=0.3)
        self.play(Create(items[2][1]), run_time=0.3)
        t_own = lab("on its own", 30, GREY).move_to([0.6, -1.5, 0])
        self.at("on its own")
        self.play(FadeIn(t_own), run_time=0.3)
        # host cell
        self.at("host cell")
        gone = VGroup(*[m for c, x in items for m in (c, x)], t_own)
        self.play(FadeOut(gone), ph.animate.move_to([-5.4, 0.2, 0]), ph_lbl.animate.move_to([-5.4, 1.9, 0]), run_time=0.6)
        host = cellbox(6.8, 4.0, BLUE).move_to([1.5, 0.45, 0])
        hdna = dnabar(2.4).move_to([1.5, -0.95, 0])
        hlab = lab("host cell", 32, BLUE, weight=BOLD).move_to([1.5, 2.85, 0])
        hdl = lab("host DNA", 24, TEAL).next_to(hdna, UP, buff=0.12)
        self.play(FadeIn(host), FadeIn(hdna), FadeIn(hdl), FadeIn(hlab), run_time=0.8)
        # phage named
        self.at("bacteriophage")
        name = lab("bacteriophage\n(phage)", 26, PURPLE, line_spacing=0.8).move_to([-5.4, 2.0, 0])
        self.play(ReplacementTransform(ph_lbl, name), run_time=0.5)
        # lytic cycle
        step_y = -3.3
        def step(n, text):
            return chip(f"{n}  {text}", PURPLE, size=24)
        s1 = step(1, "inject DNA"); s2 = step(2, "copy + build"); s3 = step(3, "assemble"); s4 = step(4, "burst")
        row = VGroup(s1, s2, s3, s4).arrange(RIGHT, buff=0.3).move_to([1.4, step_y, 0])
        self.at("lytic cycle")
        ttl = lab("lytic cycle", 30, PURPLE, weight=BOLD).move_to([-4.9, step_y, 0])
        self.play(FadeIn(ttl), run_time=0.4)
        # move phage to cell edge, inject
        self.at("injects")
        self.play(ph.animate.rotate(PI / 2).move_to([-2.0, 0.7, 0]), name.animate.move_to([-4.6, 1.6, 0]), run_time=0.7)
        vdna = dnabar(1.0, PURPLE, 0.24).move_to([-1.0, 0.7, 0])
        self.play(FadeIn(s1), FadeIn(vdna), run_time=0.4)
        self.play(vdna.animate.move_to([1.2, 0.9, 0]), run_time=0.8)
        # copy and build parts
        self.at("copies it")
        copies = VGroup(*[dnabar(1.0, PURPLE, 0.24) for _ in range(3)]).arrange(RIGHT, buff=0.3).move_to([1.5, 1.8, 0])
        self.play(FadeIn(s2), ReplacementTransform(vdna, copies), run_time=0.7)
        self.at("builds viral parts")
        parts = VGroup(*[Square(side_length=0.35, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.5)
                         for _ in range(6)]).arrange_in_grid(2, 3, buff=0.18).move_to([1.5, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in parts], lag_ratio=0.12), run_time=0.9)
        pl = lab("viral parts", 24, PURPLE).move_to([3.6, 0.6, 0])
        self.play(FadeIn(pl), run_time=0.3)
        # assemble
        self.at("assembled")
        new = VGroup(*[phage(0.6) for _ in range(4)]).arrange(RIGHT, buff=0.55).move_to([1.5, 0.9, 0])
        self.play(FadeIn(s3), FadeOut(pl), ReplacementTransform(VGroup(parts, copies), new), run_time=0.9)
        # burst
        self.at("cell bursts")
        self.play(FadeIn(s4), host.animate.set_stroke(RED).set_fill(RED, 0.08), run_time=0.5)
        pos = [[4.6, 2.5, 0], [5.8, 0.4, 0], [4.8, -1.6, 0], [-0.2, -2.15, 0]]
        self.at("new phages escape")
        self.play(*[p.animate.move_to(q) for p, q in zip(new, pos)], FadeOut(hdna), FadeOut(hdl), run_time=1.0)
        dies = lab("host cell dies", 32, RED, weight=BOLD).move_to([1.5, 2.85, 0])
        self.at("host cell dies")
        self.play(FadeOut(hlab), host.animate.set_stroke(RED, opacity=0.5), FadeIn(dies), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Hidden(SpokenScene):
    """lysogenic: viral DNA joins the chromosome, copied at each division, can switch; herpes; the rule."""

    def construct(self):
        title = banner("lysogenic cycle", PURPLE)
        host = cellbox(7.0, 3.6, BLUE).move_to([0, 0.1, 0])
        hdna = dnabar(3.8, TEAL, 0.32).move_to([-0.4, 0.1, 0])
        vdna = dnabar(1.1, PURPLE, 0.32).move_to([-4.6, 2.0, 0])
        vlab = lab("viral DNA", 26, PURPLE).next_to(vdna, UP, buff=0.2)
        self.at("In the lysogenic")
        self.play(FadeIn(title), FadeIn(host), FadeIn(hdna), FadeIn(vdna), FadeIn(vlab), run_time=0.8)
        # joins
        self.at("joins the")
        join_to = hdna.get_right() + RIGHT * 0.55
        self.play(vdna.animate.move_to(join_to), FadeOut(vlab), run_time=0.9)
        # prophage
        self.at("called a prophage")
        pro = lab("prophage", 32, PURPLE, weight=BOLD).next_to(vdna, DOWN, buff=0.45)
        pr_arr = arr(pro.get_top(), vdna.get_bottom(), PURPLE, w=4)
        host_lab = lab("host chromosome", 26, TEAL).next_to(hdna, UP, buff=0.3).shift(LEFT * 0.4)
        self.play(FadeIn(pro), GrowArrow(pr_arr), FadeIn(host_lab), run_time=0.6)
        # divides
        self.at("the bacterium divides")
        self.play(FadeOut(VGroup(pro, pr_arr, host_lab)), run_time=0.3)
        c1 = cellbox(5.0, 3.2, BLUE).move_to([-3.0, 0.1, 0]); c2 = cellbox(5.0, 3.2, BLUE).move_to([3.0, 0.1, 0])

        def chrom(cx):
            h = dnabar(2.6, TEAL, 0.32).move_to([cx - 0.55, 0.1, 0])
            v = dnabar(0.9, PURPLE, 0.32).next_to(h, RIGHT, buff=0)
            return VGroup(h, v)
        k1, k2 = chrom(-3.0), chrom(3.0)
        self.play(ReplacementTransform(VGroup(host, hdna, vdna), VGroup(c1, c2, k1, k2)), run_time=0.9)
        self.at("both daughter cells")
        both = lab("both cells carry a copy", 30, PURPLE).move_to([0, -2.2, 0])
        self.play(FadeIn(both), Indicate(k1[1], color=PURPLE), Indicate(k2[1], color=PURPLE), run_time=0.8)
        # damage -> switch
        self.at("damage to the")
        dmg = chip("DNA damage", RED, size=28).move_to([-3.0, 2.55, 0])
        da = arr(dmg.get_bottom(), c1.get_top() + DOWN * 0.1, RED, w=4)
        self.play(FadeOut(both), FadeIn(dmg), GrowArrow(da), run_time=0.5)
        self.at("switch the prophage")
        lyt = chip("lytic cycle", PURPLE, size=30).move_to([-3.0, -2.5, 0])
        sa = arr(k1[1].get_bottom(), lyt.get_top(), PURPLE, w=5)
        self.play(GrowArrow(sa), FadeIn(lyt), Indicate(k1[1], color=PURPLE, scale_factor=1.2), run_time=0.7)
        # herpes
        self.at("The herpes virus")
        self.play(FadeOut(VGroup(c1, c2, k1, k2, dmg, da, sa, lyt, title)), run_time=0.6)
        nerve = Rectangle(width=4.8, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([-3.5, 0.4, 0])
        nerve_lbl = lab("sensory nerve cells", 28, GREY).move_to([-3.5, -1.0, 0])
        hv = Circle(radius=0.34, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.9).move_to([-3.5, 0.4, 0])
        hv_lbl = lab("herpes virus", 28, PURPLE).move_to([-3.5, 2.1, 0])
        self.play(FadeIn(nerve), FadeIn(hv, scale=0.6), FadeIn(hv_lbl), run_time=0.6)
        self.at("sensory nerve cells")
        self.play(FadeIn(nerve_lbl), run_time=0.4)
        skin = Rectangle(width=4.4, height=1.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([3.7, 0.4, 0])
        skin_lbl = lab("skin", 28, GREY).move_to([3.7, -0.7, 0])
        sore = Ellipse(width=1.4, height=0.7, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.85).move_to([4.4, 0.6, 0])
        self.at("active again")
        self.play(FadeIn(skin), FadeIn(skin_lbl), hv.animate.move_to([2.8, 0.6, 0]), hv_lbl.animate.move_to([3.7, 2.1, 0]), run_time=0.8)
        self.play(FadeIn(sore, scale=0.5), run_time=0.3)
        # rule
        self.at("A virus never divides")
        self.play(FadeOut(VGroup(nerve, nerve_lbl, hv, hv_lbl, skin, skin_lbl, sore)), run_time=0.5)
        r1 = T("A virus never divides.", 50, PURPLE, font=TITLE_FONT).move_to([0, 1.2, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.6)
        self.at("A host cell builds it")
        r2 = T("A host cell builds it.", 50, BLUE, font=TITLE_FONT).move_to([0, -0.1, 0])
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.at("right away or later")
        ch = VGroup(chip("right away: lytic", PURPLE, 32), chip("or later: lysogenic", PURPLE, 32)).arrange(RIGHT, buff=0.5).move_to([0, -1.7, 0])
        self.play(FadeIn(ch, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A virus never divides. A host cell builds it."
