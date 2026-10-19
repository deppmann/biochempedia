"""Pharmacological blockade and inhibitors: switching one part off to test it  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the drug or toxin (the probe)
  PURPLE = the target protein (channel, receptor, enzyme)
  YELLOW = the response being measured (trace, bar, count)
  GREEN  = a control or the baseline; "this worked"
  RED    = off-target hits, the pitfall, a blocked path
  ORANGE = the agonist (the known stimulus)
  GREY   = membranes, structure, de-emphasised text
  PINK   = the second eye's input (stripes in the cortex), with TEAL for the first
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FBF"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def membrane(x0, x1, y, holes=(), h=0.3, hole_w=0.8, color=GREY):
    edges = [x0]
    segs = []
    for hx in sorted(holes):
        segs.append((edges[-1], hx - hole_w / 2))
        edges.append(hx + hole_w / 2)
    segs.append((edges[-1], x1))
    g = VGroup()
    for a, b in segs:
        if b - a > 0.02:
            g.add(RoundedRectangle(corner_radius=min(0.08, h / 2), width=b - a, height=h, stroke_color=color,
                                   stroke_width=2.5, fill_color=color, fill_opacity=0.35).move_to([(a + b) / 2, y, 0]))
    return g


class Chan(VGroup):
    """Channel: two posts and a plug. Plug visible = closed/blocked."""

    def __init__(self, x, y, scale=1.0, closed=True):
        pw, h, gap = 0.3 * scale, 0.5 * scale, 0.2 * scale
        l = Rectangle(width=pw, height=h, stroke_color=PURPLE, stroke_width=2.5, fill_color=PURPLE, fill_opacity=0.55)
        r = l.copy()
        l.move_to([x - (gap + pw) / 2, y, 0])
        r.move_to([x + (gap + pw) / 2, y, 0])
        self.plug = Rectangle(width=gap + 0.02, height=h * 0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.95)
        self.plug.move_to([x, y, 0])
        self.plug.set_opacity(1.0 if closed else 0.0)
        self.cx, self.cy = x, y
        super().__init__(l, r, self.plug)


def spikes(x0, x1, yb, amp, ts=(0.2, 0.5, 0.8), flat=False, color=YELLOW, w=5):
    xs = np.linspace(x0, x1, 150)
    t = (xs - x0) / (x1 - x0)
    ys = np.zeros_like(t)
    if not flat:
        for c in ts:
            ys += np.exp(-((t - c) / 0.022) ** 2) - 0.2 * np.exp(-((t - c - 0.05) / 0.035) ** 2)
    return poly([[x, yb + amp * y] for x, y in zip(xs, ys)], color, w)


def bar(cx, base, h, w, color, op=0.7):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([cx, base + h / 2, 0])


def tagbox(text, color=GREY, size=22):
    t = T(text, size, color)
    b = RoundedRectangle(corner_radius=0.1, width=t.width + 0.4, height=t.height + 0.26, stroke_color=color,
                         stroke_width=2, fill_opacity=0)
    return VGroup(b, t.move_to(b))


def xmark(c, s=0.35, color=RED, w=7):
    x, y = c
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def tick(c, s=0.3, color=GREEN, w=7):
    x, y = c
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.8, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.8, 0], [x + s, y + s * 0.8, 0], color=color, stroke_width=w))


def dots(cx, cy, w, h, n, color=BLUE, seed=1, r=0.07):
    rng = np.random.RandomState(seed)
    return VGroup(*[Dot([cx + (rng.rand() - 0.5) * w, cy + (rng.rand() - 0.5) * h, 0], radius=r, color=color)
                    for _ in range(n)])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Switching One Part Off to Test It"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """A part is seen active with an outcome; needed? takes removing it; a drug binds one protein, switches it off, washes out."""

    def construct(self):
        y = 0.2
        px = -0.6
        stim = chip("input", GREY, 30).move_to([-5.0, y, 0])
        part = RoundedRectangle(corner_radius=0.2, width=2.8, height=1.5, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.35).move_to([px, y, 0])
        plbl = T("one part", 30, PURPLE).move_to(part)
        partg = VGroup(part, plbl)
        panel = RoundedRectangle(width=3.4, height=1.9, corner_radius=0.15, stroke_color=GREY,
                                 stroke_width=2.5).move_to([4.7, y, 0])
        tr = spikes(3.1, 6.3, y - 0.45, 1.0)
        a1 = arr([-4.2, y, 0], [-2.1, y, 0], GREY)
        a2 = arr([0.9, y, 0], [2.95, y, 0], GREY)
        part_lbl = lab("part active", 28, PURPLE).move_to([px, y + 1.3, 0])
        out_lbl = lab("outcome", 28, YELLOW).move_to([4.7, y + 1.5, 0])
        dot = Dot([-4.2, y, 0], radius=0.13, color=YELLOW)

        self.at("Watching a cell")
        self.play(FadeIn(stim), FadeIn(partg), FadeIn(panel), GrowArrow(a1), GrowArrow(a2),
                  Create(tr, rate_func=linear), run_time=0.9)
        self.add(dot)
        self.play(MoveAlongPath(dot, Line([-4.2, y, 0], [-2.1, y, 0])), run_time=0.3)
        self.play(MoveAlongPath(dot, Line([0.9, y, 0], [2.95, y, 0])), run_time=0.3)
        self.remove(dot)

        self.at("alongside an outcome")
        self.play(FadeIn(part_lbl), FadeIn(out_lbl), run_time=0.3)
        under = VGroup(Line([px - 1.4, -1.0, 0], [6.4, -1.0, 0], color=GREEN, stroke_width=4),
                       Line([px - 1.4, -1.0, 0], [px - 1.4, -0.75, 0], color=GREEN, stroke_width=4),
                       Line([6.4, -1.0, 0], [6.4, -0.75, 0], color=GREEN, stroke_width=4))
        together = lab("seen together", 28, GREEN).move_to([2.6, -1.5, 0])
        self.play(Create(under), FadeIn(together), run_time=0.5)

        self.at("whether the part is needed")
        need = T("needed?", 60, TEXT, weight=BOLD).move_to([0.0, 2.9, 0])
        self.play(FadeOut(under), FadeOut(together), FadeIn(need, shift=DOWN * 0.2), run_time=0.5)

        self.at("removing the part")
        ghost = DashedVMobject(part.copy().set_fill(opacity=0).set_stroke(PURPLE, 3), num_dashes=40)
        q = T("?", 90, YELLOW, weight=BOLD).move_to([4.7, y, 0])
        self.play(partg.animate.shift(DOWN * 2.7), FadeIn(ghost), FadeOut(part_lbl),
                  tr.animate.set_opacity(0.2), a1.animate.set_opacity(0.25), a2.animate.set_opacity(0.25),
                  FadeIn(q), run_time=0.9)

        self.at("But a sodium current")
        chips = VGroup(chip("sodium current", PURPLE, 26), chip("receptor", PURPLE, 26), chip("enzyme", PURPLE, 26))
        chips.arrange(RIGHT, buff=0.3).move_to([px + 0.3, -1.3, 0])
        self.play(partg.animate.shift(UP * 2.7), FadeOut(ghost), tr.animate.set_opacity(1.0),
                  a1.animate.set_opacity(1.0), a2.animate.set_opacity(1.0), FadeOut(q), FadeOut(need),
                  run_time=0.6)
        self.play(FadeIn(chips, shift=UP * 0.1), run_time=0.5)

        self.at("cannot be pulled out")
        pull = arr([px, y + 0.85, 0], [px, 3.0, 0], GREY, w=6)
        cross = xmark([px, 2.1], 0.3)
        byhand = lab("by hand", 30, RED).move_to([px + 1.5, 2.3, 0])
        self.play(GrowArrow(pull), FadeIn(cross), FadeIn(byhand), run_time=0.6)

        self.at("A drug that binds")
        drug = chip("drug", BLUE, 34).move_to([px, 3.0, 0])
        self.play(FadeOut(pull), FadeOut(cross), FadeOut(byhand), FadeOut(chips), run_time=0.3)
        self.play(FadeIn(drug, shift=DOWN * 0.2), run_time=0.3)
        self.play(drug.animate.move_to([px, y + 1.3, 0]), run_time=0.5)
        off = T("off", 30, GREY).move_to(part)
        self.play(Transform(plbl, off), part.animate.set_fill(GREY, 0.12).set_stroke(GREY, 4),
                  a2.animate.set_opacity(0.25), tr.animate.set_opacity(0.2), FadeIn(q), run_time=0.6)

        self.at("within minutes")
        mins = chip("within minutes", GREY, 28).move_to([3.4, 2.6, 0])
        self.play(FadeIn(mins, shift=DOWN * 0.1), run_time=0.4)

        self.at("washed out")
        on = T("one part", 30, PURPLE).move_to(part)
        self.play(drug.animate.shift(RIGHT * 7.5 + UP * 0.6).set_opacity(0.0), FadeOut(mins),
                  Transform(plbl, on), part.animate.set_fill(PURPLE, 0.35).set_stroke(PURPLE, 4),
                  a2.animate.set_opacity(1.0), tr.animate.set_opacity(1.0), FadeOut(q), run_time=1.0)
        wo = lab("drug washed out", 30, GREEN).move_to([px, -1.3, 0])
        self.play(FadeIn(wo), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fit(SpokenScene):
    """A compound docks on one protein; tetrodotoxin plugs a sodium channel; the spike goes flat, the resting level stays."""

    def construct(self):
        self.camera.frame_center = np.array([0.0, 0.55, 0.0])
        # --- stage 1: a compound fits one protein
        comp = chip("compound", BLUE, 40).move_to([-4.2, 0.2, 0])
        target = RoundedRectangle(corner_radius=0.25, width=3.8, height=2.8, stroke_color=PURPLE, stroke_width=4,
                                  fill_color=PURPLE, fill_opacity=0.3).move_to([2.2, 0.2, 0])
        tl = T("one protein", 40, PURPLE).move_to(target)
        self.at("Choose a compound")
        self.play(FadeIn(comp, shift=RIGHT * 0.2), FadeIn(target), FadeIn(tl), run_time=0.7)
        self.at("high affinity")
        self.play(comp.animate.move_to([-0.1, 0.2, 0]), run_time=0.8)
        aff = lab("binds tightly: high affinity", 32, TEXT).move_to([0.8, -1.8, 0])
        self.play(FadeIn(aff), run_time=0.4)

        # --- stage 2: tetrodotoxin and the sodium channel
        self.at("Tetrodotoxin binds")
        cx = -3.0
        cy = 0.5
        mem = membrane(-6.4, 0.2, cy, holes=[cx], h=0.8, hole_w=2.45)
        ch = Chan(cx, cy, 3.0, closed=False)
        chl = lab("voltage-gated sodium channel", 28, PURPLE).move_to([cx + 0.2, -0.65, 0])
        toxin = chip("tetrodotoxin", BLUE, 34).move_to([cx, 3.0, 0])
        self.play(FadeOut(comp), FadeOut(target), FadeOut(tl), FadeOut(aff), run_time=0.4)
        self.play(FadeIn(mem), FadeIn(ch), FadeIn(chl), FadeIn(toxin, shift=DOWN * 0.2), run_time=0.7)

        self.at("one channel per toxin")
        one = lab("one toxin : one channel", 30, TEXT).move_to([cx + 0.2, -1.35, 0])
        self.play(toxin.animate.move_to([cx, 2.0, 0]), FadeIn(one), run_time=0.6)

        self.at("plugs the pore")
        self.play(toxin.animate.scale(0.45).move_to([cx, cy, 0]).set_opacity(0.0),
                  ch.plug.animate.set_opacity(1.0), run_time=0.7)
        stop = lab("pore plugged: no sodium passes", 28, BLUE).move_to([cx + 0.2, -2.05, 0])
        self.play(FadeIn(stop), run_time=0.3)

        self.at("Curare binds")
        cur = chip("curare", BLUE, 32).move_to([3.7, 2.5, 0])
        rec = chip("muscle acetylcholine receptor", PURPLE, 26).move_to([3.7, 0.5, 0])
        ca = arr([3.7, 2.1, 0], [3.7, 1.05, 0], BLUE)
        self.play(FadeIn(cur), FadeIn(rec), GrowArrow(ca), run_time=0.7)

        self.at("Add tetrodotoxin")
        panel = RoundedRectangle(width=5.5, height=4.4, corner_radius=0.15, stroke_color=GREY,
                                 stroke_width=2.5).move_to([3.7, 0.6, 0])
        pt = lab("membrane voltage", 24, GREY).move_to([2.5, 2.4, 0])
        idl = tagbox("idealised", GREY, 22).move_to([5.5, 2.4, 0])
        base = DashedLine([1.2, -0.3, 0], [6.2, -0.3, 0], color=GREEN, stroke_width=3)
        sp = spikes(1.2, 6.2, -0.3, 2.3, ts=(0.3,))
        toxin2 = chip("tetrodotoxin", BLUE, 34).move_to([cx, 3.0, 0])
        self.play(FadeOut(cur), FadeOut(rec), FadeOut(ca), FadeOut(stop), FadeOut(one),
                  ch.plug.animate.set_opacity(0.0), run_time=0.4)
        self.play(FadeIn(panel), FadeIn(pt), FadeIn(idl), FadeIn(base), FadeIn(toxin2, shift=DOWN * 0.2), run_time=0.5)
        self.play(Create(sp, run_time=1.0, rate_func=linear))

        self.at("action potential is blocked")
        flat = spikes(1.2, 6.2, -0.3, 2.3, ts=(0.3,), flat=True)
        self.play(toxin2.animate.scale(0.45).move_to([cx, cy, 0]).set_opacity(0.0),
                  ch.plug.animate.set_opacity(1.0), Transform(sp, flat), run_time=0.9)
        blk = lab("action potential: blocked", 28, TEXT).move_to([3.7, 1.0, 0])
        self.play(FadeIn(blk), run_time=0.3)

        self.at("The resting potential")
        rp = lab("resting potential: unchanged", 28, GREEN).move_to([3.7, -1.1, 0])
        self.play(FadeIn(rp, shift=UP * 0.1), base.animate.set_stroke(GREEN, 6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Deliver(SpokenScene):
    """Four delivery routes; then a positive control: agonist alone responds, agonist after the drug does not."""

    def construct(self):
        self.camera.frame_center = np.array([0.0, 0.5, 0.0])
        xs = [-4.6, -1.55, 1.55, 4.6]
        pc = 0.5
        frames = VGroup(*[RoundedRectangle(width=2.95, height=5.2, corner_radius=0.18, stroke_color=GREY,
                                           stroke_width=2.5).move_to([x, pc, 0]) for x in xs])
        self.at("Deliver it where")
        self.play(FadeIn(frames, lag_ratio=0.15), run_time=0.8)
        ty = -1.5

        def S(g, x, y):   # scale a drawing around its panel position
            g.scale(1.25, about_point=np.array([x, y, 0]))
            return g
        # 1 bath on a slice
        self.at("bath on a slice")
        x = xs[0]
        dish = RoundedRectangle(width=2.0, height=1.4, corner_radius=0.2, stroke_color=GREY, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.15).move_to([x, 1.1, 0])
        sl = Ellipse(width=1.3, height=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.5).move_to([x, 0.85, 0])
        d1 = dots(x, 1.2, 1.7, 1.0, 9, BLUE, 3)
        g1 = S(VGroup(dish, sl, d1), x, 1.1)
        t1 = lines("bath on", "a slice", size=26, align=ORIGIN).move_to([x, ty, 0])
        self.play(FadeIn(g1), FadeIn(t1), run_time=0.7)

        # 2 ionophoresis at a synapse
        self.at("at a synapse")
        x = xs[1]
        pre = Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([x - 0.68, 0.5, 0])
        post = Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([x + 0.68, 0.5, 0])
        pip = Polygon([x - 0.07, 0.55, 0], [x + 0.07, 0.55, 0], [x + 0.45, 2.5, 0], [x - 0.45, 2.5, 0], stroke_color=BLUE,
                      stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
        d2 = dots(x, 0.65, 0.25, 0.25, 4, BLUE, 5)
        g2 = S(VGroup(pre, post, pip, d2), x, 1.3)
        t2 = lines("ionophoresis", "at a synapse", size=26, align=ORIGIN).move_to([x, ty, 0])
        self.play(FadeIn(g2), FadeIn(t2), run_time=0.7)

        # 3 injection into one eye
        self.at("injection into one eye")
        x = xs[2]
        eye = Circle(radius=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([x - 0.1, 1.0, 0])
        pupil = Circle(radius=0.26, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x - 0.55, 1.0, 0])
        syr = Line([x + 1.05, 2.5, 0], [x + 0.5, 1.4, 0], color=BLUE, stroke_width=9)
        d3 = dots(x + 0.05, 0.95, 0.7, 0.7, 5, BLUE, 7)
        g3 = S(VGroup(eye, pupil, syr, d3), x, 1.1)
        t3 = lines("injection into", "one eye", size=26, align=ORIGIN).move_to([x, ty, 0])
        self.play(FadeIn(g3), FadeIn(t3), run_time=0.7)

        # 4 small injection into one brain area
        self.at("into one brain")
        x = xs[3]
        brain = Ellipse(width=2.2, height=1.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([x, 0.8, 0])
        area = Circle(radius=0.33, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([x + 0.4, 1.1, 0])
        syr2 = Line([x + 0.4, 2.5, 0], [x + 0.4, 1.45, 0], color=BLUE, stroke_width=9)
        d4 = dots(x + 0.4, 1.1, 0.35, 0.35, 4, BLUE, 9, 0.06)
        g4 = S(VGroup(brain, area, syr2, d4), x, 1.1)
        t4 = lines("small injection,", "one brain area", size=26, align=ORIGIN).move_to([x, ty, 0])
        self.play(FadeIn(g4), FadeIn(t4), run_time=0.7)

        # positive control
        self.at("Then show the drug works")
        old = VGroup(frames, g1, t1, g2, t2, g3, t3, g4, t4)
        self.play(FadeOut(old), run_time=0.5)
        pl = RoundedRectangle(width=5.8, height=5.0, corner_radius=0.18, stroke_color=GREY, stroke_width=2.5).move_to([-3.3, 0.5, 0])
        pr = RoundedRectangle(width=5.8, height=5.0, corner_radius=0.18, stroke_color=GREY, stroke_width=2.5).move_to([3.3, 0.5, 0])
        ag1 = chip("known agonist", ORANGE, 26).move_to([-3.3, 2.25, 0])
        bl = -0.4
        ba = DashedLine([-5.8, bl, 0], [-0.8, bl, 0], color=GREY, stroke_width=2.5)
        bump = poly([[-5.8, bl], [-4.6, bl], [-4.2, bl + 1.0], [-3.7, bl + 1.6], [-3.0, bl + 1.3], [-2.2, bl + 0.5], [-1.6, bl], [-0.8, bl]], YELLOW, 6)
        r1 = lab("response", 28, YELLOW).move_to([-3.3, -1.3, 0])
        self.play(FadeIn(pl), FadeIn(ag1), FadeIn(ba), run_time=0.5)
        self.play(Create(bump, run_time=1.0, rate_func=linear), FadeIn(r1))

        self.at("abolishing the response")
        dr = chip("drug first", BLUE, 26).move_to([1.6, 2.25, 0])
        ag2 = chip("known agonist", ORANGE, 26).move_to([4.7, 2.25, 0])
        bb = DashedLine([0.8, bl, 0], [5.8, bl, 0], color=GREY, stroke_width=2.5)
        flat = poly([[0.8, bl], [5.8, bl]], YELLOW, 6)
        r2 = lab("no response", 28, YELLOW).move_to([3.3, -1.3, 0])
        self.play(FadeIn(pr), FadeIn(dr), FadeIn(bb), run_time=0.4)
        self.play(FadeIn(ag2), Create(flat, run_time=0.8, rate_func=linear), FadeIn(r2), run_time=0.8)

        self.at("known agonist")
        ok = tick([3.3, 1.2], 0.4)
        okl = lab("drug works at this dose", 30, GREEN).move_to([3.3, 0.55, 0])
        self.play(FadeIn(ok), FadeIn(okl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Onoff(SpokenScene):
    """Idealised bars: function and baseline, drug off and on. The induced change collapses; baseline stays."""

    def construct(self):
        base = -1.9
        g1, g2 = -3.1, 3.1
        w = 1.5
        axis = Line([-6.2, base, 0], [6.2, base, 0], color=GREY, stroke_width=3)
        idl = tagbox("idealised example", GREY, 22).move_to([-4.6, 3.3, 0])

        self.at("Now measure")
        l1 = lab("function in question", 28, YELLOW).move_to([g1, -3.3, 0])
        self.play(FadeIn(axis), FadeIn(idl), FadeIn(l1), run_time=0.5)
        b1off = bar(g1 - 0.9, base, 3.0, w, YELLOW)
        o1 = lab("drug off", 24, GREY).move_to([g1 - 0.9, -2.45, 0])
        self.play(GrowFromEdge(b1off, DOWN), FadeIn(o1), run_time=0.6)

        self.at("the baseline")
        l2 = lab("baseline", 28, GREEN).move_to([g2, -3.3, 0])
        b2off = bar(g2 - 0.9, base, 1.7, w, GREEN)
        o2 = lab("drug off", 24, GREY).move_to([g2 - 0.9, -2.45, 0])
        self.play(FadeIn(l2), GrowFromEdge(b2off, DOWN), FadeIn(o2), run_time=0.6)

        self.at("drug on and off")
        b1on = bar(g1 + 0.9, base, 3.0, w, YELLOW)
        b2on = bar(g2 + 0.9, base, 1.7, w, GREEN)
        n1 = lab("drug on", 24, BLUE).move_to([g1 + 0.9, -2.45, 0])
        n2 = lab("drug on", 24, BLUE).move_to([g2 + 0.9, -2.45, 0])
        pill1 = chip("drug", BLUE, 24).move_to([g1 + 0.9, 3.0, 0])
        pill2 = chip("drug", BLUE, 24).move_to([g2 + 0.9, 3.0, 0])
        self.play(GrowFromEdge(b1on, DOWN), GrowFromEdge(b2on, DOWN), FadeIn(n1), FadeIn(n2), run_time=0.6)

        self.at("general damage")
        note = lab("the control for general damage", 26, GREEN).move_to([g2, 1.5, 0])
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.5)

        self.at("blocks the induced change")
        self.play(FadeIn(pill1, shift=DOWN * 0.2), run_time=0.3)
        self.play(b1on.animate.stretch_to_fit_height(0.25).move_to([g1 + 0.9, base + 0.125, 0]), run_time=0.8)
        bl = lab("blocked", 28, TEXT).move_to([g1 + 0.9, -1.35, 0])
        self.play(FadeIn(bl), run_time=0.3)

        self.at("leaves baseline alone")
        self.play(FadeIn(pill2, shift=DOWN * 0.2), run_time=0.3)
        ok = lab("unchanged", 28, GREEN).move_to([g2 + 0.9, base + 1.7 + 0.45, 0])
        self.play(FadeIn(ok), run_time=0.4)

        self.at("needed for induction")
        c1 = chip("target needed for induction,\nunder that protocol", YELLOW, 26).move_to([g1, 2.15, 0])
        self.play(FadeOut(pill1), FadeIn(c1, shift=UP * 0.1), run_time=0.5)

        self.at("routine transmission")
        c2 = chip("not for routine transmission", GREEN, 26).move_to([g2, 2.5, 0])
        self.play(FadeOut(pill2), FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """Idealised example: resting heart rate 70; atropine 110; propranolol 62; both 100."""

    def construct(self):
        base = -2.3
        k = 0.03
        xs = [-5.4, -3.4, -1.4, 0.6]
        vals = [70, 110, 62, 100]
        names = ["rest", "atropine", "propranolol", "both"]
        ncol = [GREY, BLUE, BLUE, BLUE]
        axis = Line([-6.4, base, 0], [1.5, base, 0], color=GREY, stroke_width=3)
        ttl = lab("heart rate per minute", 28, GREY).move_to([-2.4, 3.2, 0])
        idl = tagbox("idealised example", GREY, 22).move_to([4.2, 3.2, 0])
        ref = DashedLine([-6.4, base + 70 * k, 0], [1.5, base + 70 * k, 0], color=GREY, stroke_width=2.5)

        def mk(i):
            b = bar(xs[i], base, vals[i] * k, 1.3, GREY if i == 0 else YELLOW)
            v = M(str(vals[i]), 30, TEXT).move_to([xs[i], base + vals[i] * k + 0.38, 0]); v.add_background_rectangle(color=BG, opacity=1.0, buff=0.06)
            n = lab(names[i], 24, ncol[i]).move_to([xs[i], base - 0.45, 0])
            return b, v, n
        bars = [mk(i) for i in range(4)]

        self.at("Here is an")
        self.play(FadeIn(axis), FadeIn(ttl), FadeIn(idl), run_time=0.5)
        self.at("Resting heart rate")
        b, v, n = bars[0]
        self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n), FadeIn(ref), run_time=0.7)
        self.at("After atropine")
        b, v, n = bars[1]
        self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n), run_time=0.7)
        self.at("After propranolol")
        b, v, n = bars[2]
        self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n), run_time=0.7)
        self.at("After both")
        b, v, n = bars[3]
        self.play(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n), run_time=0.7)

        self.at("So parasympathetic")
        note = VGroup(*[T(s, 30, TEXT) for s in ["parasympathetic", "braking dominates", "at rest"]]).arrange(DOWN, buff=0.12)
        box = RoundedRectangle(corner_radius=0.18, width=note.width + 0.6, height=note.height + 0.5, stroke_color=GREEN,
                               stroke_width=3, fill_color=GREEN, fill_opacity=0.12)
        g = VGroup(box, note.move_to(box)).move_to([4.2, 1.5, 0])
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.6)

        self.at("This holds only if")
        cav = VGroup(*[T(s, 26, TEXT) for s in ["only if each drug", "fully blocks only", "its own division,", "at that dose"]]).arrange(DOWN, buff=0.1)
        cb = RoundedRectangle(corner_radius=0.18, width=cav.width + 0.6, height=cav.height + 0.5, stroke_color=RED,
                              stroke_width=3, fill_color=RED, fill_opacity=0.10)
        cg = VGroup(cb, cav.move_to(cb)).move_to([4.2, -1.55, 0])
        self.play(FadeIn(cg, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Off-target hits; lowest working dose; second drug and inactive analogue; the resistant target."""

    def construct(self):
        # ---- A: one drug, several targets
        drug = chip("drug", BLUE, 34).move_to([-5.2, 1.4, 0])
        tgt = chip("intended target", PURPLE, 26).move_to([-1.6, 2.9, 0])
        oth = [chip("another kinase", RED, 26).move_to([-1.6, y, 0]) for y in (1.9, 0.9, -0.1)]
        ars = [arr([-4.6, 1.4, 0], [-3.2, 2.9, 0], BLUE), arr([-4.6, 1.4, 0], [-3.2, 1.9, 0], RED),
               arr([-4.6, 1.4, 0], [-3.2, 0.9, 0], RED), arr([-4.6, 1.4, 0], [-3.2, -0.1, 0], RED)]
        self.at("Many drugs hit")
        self.play(FadeIn(drug), FadeIn(tgt), GrowArrow(ars[0]), run_time=0.6)
        self.play(*[FadeIn(o) for o in oth], *[GrowArrow(a) for a in ars[1:]], run_time=0.8)

        self.at("The authors profiled")
        s1 = VGroup(M("65", 44, TEXT), lab("reported specific inhibitors", 26, GREY)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        s2 = VGroup(M("70 to 80", 44, TEXT), lab("kinases profiled", 26, GREY)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        st = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, 2.4, 0])
        self.play(FadeIn(s1, shift=LEFT * 0.2), run_time=0.5)
        self.at("70 to 80")
        self.play(FadeIn(s2, shift=LEFT * 0.2), run_time=0.5)
        self.at("Many were not")
        cau = lab("many were not specific", 30, RED).move_to([3.5, 0.95, 0])
        self.play(FadeIn(cau, shift=UP * 0.1), run_time=0.4)
        self.at("considerable caution")
        ay = -3.1
        ax = Line([-5.8, ay, 0], [5.8, ay, 0], color=GREY, stroke_width=3)
        xs = np.linspace(-5.5, 5.5, 100)

        def sig(c, s_):
            return 1.0 / (1.0 + np.exp(-(xs - c) / s_))
        cu1 = poly([[x, ay + 1.4 * y] for x, y in zip(xs, sig(-2.6, 0.5))], PURPLE, 5)
        cu2 = poly([[x, ay + 1.4 * y] for x, y in zip(xs, sig(2.2, 0.5)) if x >= -2.6], RED, 5)
        dl = lab("dose", 24, GREY).move_to([5.3, ay - 0.35, 0])
        l1 = lab("target blocked", 24, PURPLE).move_to([-4.4, ay + 0.75, 0])
        l2 = lab("other kinases", 24, RED).move_to([4.4, ay + 1.75, 0])
        idl = tagbox("idealised", GREY, 22).move_to([-4.9, ay + 1.55, 0])
        self.play(FadeIn(ax), FadeIn(dl), FadeIn(idl), Create(cu1), Create(cu2),
                  FadeIn(l1), FadeIn(l2), run_time=1.0)

        self.at("lowest dose")
        lo = DashedLine([-2.6, ay, 0], [-2.6, ay + 1.5, 0], color=GREEN, stroke_width=4)
        lol = lab("lowest dose that works", 26, GREEN).move_to([-1.1, ay + 1.85, 0])
        self.play(Create(lo), FadeIn(lol), run_time=0.5)

        # ---- B: controls
        self.at("Then add controls")
        self.play(*[FadeOut(m) for m in [drug, tgt, *oth, *ars, s1, s2, cau, ax, cu1, cu2, dl, l1, l2, idl, lo, lol]], run_time=0.5)
        rows = [("drug A", BLUE, 2.2), ("drug B: a different chemical series", BLUE, 0.3), ("matched inactive analogue", GREY, -1.6)]
        row_objs = []
        for name, col, y in rows:
            c = chip(name, col, 28).move_to([-3.6, y, 0])
            a = arr([c.get_right()[0] + 0.15, y, 0], [1.2, y, 0], col)
            t = chip("target", PURPLE, 28).move_to([2.1, y, 0])
            row_objs.append((c, a, t, y))
        c, a, t, y = row_objs[0]
        self.play(FadeIn(c), GrowArrow(a), FadeIn(t), run_time=0.6)
        r = tick([4.7, y], 0.28)
        rl = lab("response blocked", 26, GREEN).move_to([5.0, y - 0.55, 0])
        self.play(FadeIn(r), FadeIn(rl), run_time=0.4)

        self.at("second drug")
        c, a, t, y = row_objs[1]
        self.play(FadeIn(c), GrowArrow(a), FadeIn(t), run_time=0.6)
        r = tick([4.7, y], 0.28)
        rl = lab("same result", 26, GREEN).move_to([5.0, y - 0.55, 0])
        self.play(FadeIn(r), FadeIn(rl), run_time=0.4)

        self.at("inactive analog")
        c, a, t, y = row_objs[2]
        x_ = xmark([4.7, y], 0.28, GREY)
        xl = lab("no block", 26, GREY).move_to([5.0, y - 0.55, 0])
        self.play(FadeIn(c), GrowArrow(a), FadeIn(t), FadeIn(x_), FadeIn(xl), run_time=0.6)

        # ---- C: drug-resistant target
        self.at("The best control")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        def cell(cx):
            fr = RoundedRectangle(width=6.0, height=4.3, corner_radius=0.2, stroke_color=GREY, stroke_width=2.5).move_to([cx, 0.3, 0])
            nuc = RoundedRectangle(width=2.5, height=3.2, corner_radius=0.2, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.18).move_to([cx - 1.5, 0.3, 0])
            nl = lab("nucleus", 22, GREY).move_to([cx - 1.5, 1.65, 0])
            cl = lab("cytoplasm", 22, GREY).move_to([cx + 1.9, 1.9, 0])
            crm = chip("CRM1", PURPLE, 28).move_to([cx - 1.5, 0.75, 0])
            return VGroup(fr, nuc, nl, cl), crm
        sk1, crm1 = cell(-3.4)
        sk2, crm2 = cell(3.4)
        t1 = lab("normal CRM1", 28, TEXT).move_to([-3.4, 2.85, 0])
        t2 = lab("one cysteine changed", 28, TEXT).move_to([3.4, 2.85, 0])
        lmb1 = chip("leptomycin B", BLUE, 24).move_to([-3.4 - 1.5, -0.3, 0])
        lmb2 = chip("leptomycin B", BLUE, 24).move_to([3.4 - 1.5, -0.3, 0])
        ex1 = arr([-3.4 - 0.1, 0.75, 0], [-3.4 + 1.9, 0.75, 0], YELLOW, w=7)
        ex2 = arr([3.4 - 0.1, 0.75, 0], [3.4 + 1.9, 0.75, 0], YELLOW, w=7)
        exl1 = lab("export", 24, YELLOW).move_to([-3.4 + 0.9, 1.2, 0])
        exl2 = lab("export", 24, YELLOW).move_to([3.4 + 0.9, 1.2, 0])
        self.play(FadeIn(sk1), FadeIn(crm1), FadeIn(t1), GrowArrow(ex1), FadeIn(exl1), run_time=0.7)
        self.play(FadeIn(lmb1, shift=UP * 0.2), run_time=0.4)
        self.play(ex1.animate.set_opacity(0.2), exl1.animate.set_opacity(0.2), FadeIn(xmark([-3.4 + 0.9, 0.75], 0.3)), run_time=0.5)

        self.at("One changed cysteine")
        self.play(FadeIn(sk2), FadeIn(crm2), FadeIn(t2), FadeIn(lmb2, shift=UP * 0.2), run_time=0.7)

        self.at("stayed normal in")
        self.play(GrowArrow(ex2), FadeIn(exl2), run_time=0.6)
        nes = lab("NES reporter (Rev-NES), fission yeast", 24, GREY).move_to([0.0, -3.0, 0])
        self.play(FadeIn(nes), run_time=0.3)
        ok = lab("resistant target: export continues", 26, GREEN).move_to([3.4, -2.3, 0])
        self.play(FadeIn(ok), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Pair(SpokenScene):
    """Pittman and Oppenheim 1979; Stryker and Harris 1986."""

    def construct(self):
        # ---- Pittman and Oppenheim
        self.at("In 1979")
        tg = lab("Pittman and Oppenheim, 1979", 26, GOLD).move_to([-2.4, 3.3, 0])
        emb = chip("chick embryo", GREY, 30).move_to([-4.3, 2.3, 0])
        self.play(FadeIn(tg), FadeIn(emb), run_time=0.5)
        self.at("curare and three")
        names = ["curare", "alpha-cobratoxin", "alpha-bungarotoxin", "botulinum toxin"]
        chs = VGroup(*[chip(n, BLUE, 24) for n in names]).arrange(DOWN, buff=0.22).move_to([-4.3, -0.2, 0])
        base = -2.0
        ttl = lab("lumbar motoneurons, day 10", 26, GREY).move_to([3.2, 3.3, 0])
        ax = Line([0.0, base, 0], [6.3, base, 0], color=GREY, stroke_width=3)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chs], lag_ratio=0.25), FadeIn(ttl), FadeIn(ax), run_time=1.2)

        bA = bar(1.7, base, 3.3, 1.7, YELLOW)
        bB = bar(4.6, base, 3.3 * 13.5 / 21.0, 1.7, GREY)
        vA = M("about 21,000", 26, TEXT).move_to([1.7, base + 3.3 + 0.35, 0])
        vB = M("13,500", 26, TEXT).move_to([4.6, base + 3.3 * 13.5 / 21.0 + 0.35, 0])
        nA = lab("alpha-cobratoxin", 22, BLUE).move_to([1.7, base - 0.4, 0])
        nB = lines("untreated controls,", "day 10", size=22, color=GREY, align=ORIGIN, buff=0.05).move_to([4.6, base - 0.55, 0])
        self.at("survived to")
        self.play(GrowFromEdge(bA, DOWN), FadeIn(vA), FadeIn(nA), run_time=0.8)
        self.at("versus")
        self.play(GrowFromEdge(bB, DOWN), FadeIn(vB), FadeIn(nB), run_time=0.7)

        self.at("All four")
        ticks = VGroup(*[tick([c.get_right()[0] + 0.45, c.get_center()[1]], 0.18, GREEN, 5) for c in chs])
        eq = lab("about equally effective", 24, GREEN).move_to([-4.3, -2.35, 0])
        self.play(FadeIn(ticks), FadeIn(eq), run_time=0.6)
        self.at("side effect")
        se = lab("argued against one drug's side effect", 26, GREEN).move_to([0.0, -3.2, 0])
        self.play(FadeIn(se, shift=UP * 0.1), run_time=0.5)

        # ---- Stryker and Harris
        self.at("In 1986")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        tg2 = lab("Stryker and Harris, 1986", 26, GOLD).move_to([-2.9, 3.3, 0])
        eyeL = Circle(radius=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([-4.6, 1.9, 0])
        eyeR = Circle(radius=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([-4.6, 0.2, 0])
        pL = Circle(radius=0.2, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([-4.6, 1.9, 0])
        pR = Circle(radius=0.2, stroke_color=PINK, stroke_width=4, fill_opacity=0).move_to([-4.6, 0.2, 0])
        ttxL = chip("TTX", BLUE, 28).move_to([-2.4, 1.9, 0])
        ttxR = chip("TTX", BLUE, 28).move_to([-2.4, 0.2, 0])
        aL = arr([-3.1, 1.9, 0], [-3.9, 1.9, 0], BLUE)
        aR = arr([-3.1, 0.2, 0], [-3.9, 0.2, 0], BLUE)
        kl = lab("both eyes of a kitten", 24, GREY).move_to([-4.0, -0.9, 0])
        self.at("injected")
        self.play(FadeIn(tg2), FadeIn(eyeL), FadeIn(eyeR), FadeIn(pL), FadeIn(pR), FadeIn(kl), run_time=0.6)
        self.play(FadeIn(ttxL), FadeIn(ttxR), GrowArrow(aL), GrowArrow(aR), run_time=0.6)

        cortex = RoundedRectangle(width=6.6, height=2.8, corner_radius=0.2, stroke_color=GREY, stroke_width=3).move_to([3.0, 1.2, 0])
        cl = lab("visual cortex", 24, GREY).move_to([3.0, 3.0, 0])
        self.at("Ocular dominance")
        self.play(FadeIn(cortex), FadeIn(cl), run_time=0.4)
        nocol = lines("no columns formed:", "no eye-specific stripes", size=32, align=ORIGIN).move_to([3.0, 1.2, 0])
        self.play(FadeIn(nocol), run_time=0.5)

        def stripes(cx, cy, w, h, n):
            sw = w / n
            return VGroup(*[Rectangle(width=sw, height=h, stroke_width=0, fill_color=(TEAL if i % 2 == 0 else PINK),
                                      fill_opacity=0.65).move_to([cx - w / 2 + sw * (i + 0.5), cy, 0]) for i in range(n)])
        self.at("Controls for the injection")
        cx_list = [-3.6, 0.1, 3.8]
        names = ["injection procedure", "systemic TTX", "visual deprivation"]
        st = []
        for cx, nm in zip(cx_list, names):
            s = stripes(cx, -1.9, 3.1, 1.3, 8)
            fr = Rectangle(width=3.1, height=1.3, stroke_color=GREY, stroke_width=2.5).move_to([cx, -1.9, 0])
            tx = lab(nm, 22, TEXT).move_to([cx, -3.0, 0])
            st.append(VGroup(s, fr, tx))
        self.play(LaggedStart(*[FadeIn(s) for s in st], lag_ratio=0.35), run_time=1.4)
        self.at("did not block")
        ok = lab("columns still formed", 26, GREEN).move_to([0.1, -0.75, 0])
        self.play(FadeIn(ok), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Rule(SpokenScene):
    """Collingridge, Kehl and McLennan 1983; the rule."""

    def construct(self):
        tg = lab("Collingridge, Kehl and McLennan, 1983", 26, GOLD).move_to([-2.4, 3.3, 0])
        ax = Line([-6.2, -2.3, 0], [2.2, -2.3, 0], color=GREY, stroke_width=3)
        ay = Line([-6.2, -2.3, 0], [-6.2, 2.6, 0], color=GREY, stroke_width=3)
        yl = lab("field synaptic potential", 24, GREY).move_to([-2.0, 2.85, 0])
        xl = lab("time", 24, GREY).move_to([1.6, -2.7, 0])
        idl = tagbox("schematic", GREY, 22).move_to([-5.0, -3.3, 0])
        self.at("In 1983")
        self.play(FadeIn(tg), Create(ax), Create(ay), FadeIn(yl), FadeIn(xl), FadeIn(idl), run_time=0.7)

        by = -0.6
        band = Rectangle(width=8.0, height=0.55, stroke_color=BLUE, stroke_width=2, fill_color=BLUE,
                         fill_opacity=0.25).move_to([-2.0, 2.0, 0])
        bandl = lab("APV, by ionophoresis", 24, BLUE).move_to(band)
        self.at("applied")
        self.play(FadeIn(band), FadeIn(bandl), run_time=0.5)

        self.at("abolished responses")
        agc = chip("NMDA agonist response: abolished", ORANGE, 26).move_to([-2.0, 0.6, 0])
        self.play(FadeIn(agc, shift=UP * 0.1), run_time=0.5)

        self.at("no effect")
        self.play(FadeOut(agc), run_time=0.3)
        rng = np.random.RandomState(4)
        xs = np.linspace(-6.0, -2.4, 50)
        pre = poly([[x, by + 0.04 * rng.randn()] for x in xs], YELLOW, 5)
        self.play(Create(pre, run_time=0.9, rate_func=linear))
        ne = lab("no effect on baseline", 24, GREEN).move_to([-4.2, -1.55, 0])
        self.play(FadeIn(ne), run_time=0.3)

        self.at("it prevented")
        hf = DashedLine([-2.4, -2.3, 0], [-2.4, 1.6, 0], color=ORANGE, stroke_width=3)
        hfl = lab("high-frequency stimulation", 22, ORANGE).move_to([-2.4, -2.72, 0])
        # BG: band spans -6..2; HFS label sits below the band? put label right of line
        xs2 = np.linspace(-2.4, 2.0, 50)
        post = poly([[x, by + 0.04 * rng.randn()] for x in xs2], YELLOW, 5)
        fl = lab("no LTP with APV", 24, YELLOW).move_to([-0.1, -1.15, 0])
        self.play(Create(hf), FadeIn(hfl), Create(post, rate_func=linear), run_time=0.9)
        self.at("term potentiation")
        self.play(FadeIn(fl), run_time=0.4)

        self.at("So the")
        c1 = VGroup(*[T(s, 26, YELLOW) for s in ["NMDA receptor:", "needed to start", "lasting change,", "under that protocol"]]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        b1 = RoundedRectangle(corner_radius=0.18, width=c1.width + 0.5, height=c1.height + 0.4, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.10)
        g1 = VGroup(b1, c1.move_to(b1)).move_to([4.7, 0.9, 0])
        self.play(FadeIn(g1, shift=LEFT * 0.2), run_time=0.6)
        self.at("not for baseline")
        c2 = chip("not for baseline", GREEN, 26).move_to([4.7, -1.1, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)

        self.at("Keep this rule")
        old = VGroup(tg, ax, ay, yl, xl, idl, band, bandl, pre, ne, hf, hfl, post, fl, g1, c2)
        self.play(FadeOut(old), run_time=0.6)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=5).move_to([0, 2.2, 0])
        self.play(GrowFromCenter(rule), run_time=0.4)
        r1 = T("A block shows what is needed", 42, TEXT, font=TITLE_FONT).move_to([0, 0.9, 0])
        r1b = T("here, at this dose.", 42, TEXT, font=TITLE_FONT).move_to([0, 0.15, 0])
        self.at("A block shows")
        self.play(FadeIn(r1, shift=UP * 0.1), FadeIn(r1b, shift=UP * 0.1), run_time=0.6)
        self.at("does not show")
        r2 = T("It does not show what is enough.", 42, YELLOW, font=TITLE_FONT).move_to([0, -1.3, 0])
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A block shows what is needed here, not what is enough."
