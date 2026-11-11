"""Delete Here, Learn Where  (Biochemistrypedia explainer, re-paced 2026-11-11)

ONE WORLD: skin with hairs | gold sensory neuron | teal spinal cord | blue brain | red movement gauge.
COLOR MAP
  GOLD  = the Advillin-targeted sensory neuron (and its gene badge)
  TEAL  = resident spinal cord cells        BLUE = resident brain cells
  RED   = movement gauge (schematic), lethality/memory/motor tiles (not rescued)
  GREEN = rescued tiles, control marker      ORANGE = outcome tiles after deletion
  WHITE = the air puff and the travelling pulse
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PTS = [(-4.3, 0.0), (-2.9, 0.0), (0.4, 0.0), (1.8, 0.0), (3.3, 0.0), (4.6, 1.2)]
GY0, GH = -2.6, 2.4          # gauge bottom and height
GX = 5.4


def P(x, y):
    return np.array([x, y, 0.0])


def badge(color, at):
    return RoundedRectangle(corner_radius=0.06, width=0.34, height=0.34, stroke_color=TEXT, stroke_width=2,
                            fill_color=color, fill_opacity=0.95).move_to(P(*at))


class World:
    def __init__(s, scene, badges=("gold", "teal", "blue"), labels=(), gauge=0.35, pulse=True, gauge_lbl=True):
        s.sc = scene
        s.t, s.g, s.bend = ValueTracker(0), ValueTracker(gauge), ValueTracker(0)
        s.pulse_on = pulse
        scene.add(s.t)
        s.t.add_updater(lambda m, dt: m.increment_value(dt))
        s.skin = RoundedRectangle(corner_radius=0.12, width=2.2, height=2.6, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.15).move_to(P(-5.4, -0.2))
        s.hairs = VGroup(*[Line(P(x, 1.1), P(x, 2.1), color=TEXT, stroke_width=5) for x in (-5.95, -5.4, -4.85)])
        s.cord = RoundedRectangle(corner_radius=0.14, width=3.6, height=2.6, stroke_color=TEAL, stroke_width=3,
                                  fill_color=TEAL, fill_opacity=0.12).move_to(P(1.5, 0))
        s.brain = RoundedRectangle(corner_radius=0.14, width=2.4, height=2.2, stroke_color=BLUE, stroke_width=3,
                                   fill_color=BLUE, fill_opacity=0.12).move_to(P(5.4, 1.6))
        s.link = DashedLine(P(3.3, 0.4), P(4.2, 1.0), color=GREY, stroke_width=4)
        axon = Line(P(-4.3, 0), P(0.4, 0), color=GOLD, stroke_width=6)
        stem = Line(P(-2.9, 0), P(-2.9, 0.6), color=GOLD, stroke_width=6)
        s.soma = Circle(radius=0.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25).move_to(P(-2.9, 1.1))
        s.ending = Dot(P(-4.3, 0), radius=0.14, color=GOLD)
        s.term = Ellipse(width=0.8, height=0.55, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.35).move_to(P(0.4, 0))
        s.neuron = VGroup(axon, stem, s.soma, s.ending, s.term)
        s.gout = Rectangle(width=1.0, height=GH, stroke_color=GREY, stroke_width=3).move_to(P(GX, GY0 + GH / 2))
        s.gfill = Rectangle(width=0.94, height=0.1, stroke_width=0, fill_color=RED, fill_opacity=0.75)
        s.gauge = VGroup(s.gout, s.gfill)
        s.pulse = Dot(P(-4.3, 0), radius=0.15, color=WHITE).set_opacity(0)
        s.gold_b = VGroup(badge(GOLD, (-2.9, 1.1)), badge(GOLD, (0.4, 0)))
        s.teal_b = VGroup(badge(TEAL, (0.9, -0.8)), badge(TEAL, (1.9, 0.8)), badge(TEAL, (2.7, -0.6)))
        s.blue_b = VGroup(badge(BLUE, (4.8, 1.1)), badge(BLUE, (5.4, 1.5)), badge(BLUE, (6.0, 1.1)))
        s.lbl = {
            "neuron": T("sensory neuron", 28, GOLD).move_to(P(-0.9, 1.55)),
            "cord": T("spinal cord", 28, TEAL).move_to(P(2.0, 1.75)),
            "brain": T("brain", 30, BLUE).move_to(P(5.4, 2.2)),
            "gauge": T("movement\nschematic", 24, RED, line_spacing=0.6).move_to(P(GX, -3.2)),
        }
        parts = [s.skin, s.hairs, s.cord, s.brain, s.link, s.neuron, s.gauge, s.pulse]
        for b in badges:
            parts.append(getattr(s, b + "_b"))
        for k in labels:
            if k != "gauge" or gauge_lbl:
                parts.append(s.lbl[k])
        s.body = VGroup(*parts)
        s._set_gauge()

    def _set_gauge(s):
        h = max(0.03, GH * float(np.clip(s.g.get_value() + 0.012 * np.sin(3 * s.t.get_value()), 0, 1)))
        s.gfill.stretch_to_fit_height(h)
        s.gfill.move_to(P(GX, GY0 + h / 2 + 0.03))

    def start(s):
        t = s.t
        for i, h in enumerate(s.hairs):
            base = h.get_start()
            h.add_updater(lambda m, b=base, i=i: m.put_start_and_end_on(
                b, b + P(0.07 * np.sin(2.1 * t.get_value() + i) + 0.4 * s.bend.get_value(), 0.98 - 0.12 * s.bend.get_value())))
        s.gfill.add_updater(lambda m: s._set_gauge())
        cum = np.cumsum([0] + [np.hypot(PTS[i + 1][0] - PTS[i][0], PTS[i + 1][1] - PTS[i][1]) for i in range(len(PTS) - 1)])
        xs, ys = [p[0] for p in PTS], [p[1] for p in PTS]

        def pul(m):
            ph = (t.get_value() % 3.0) / 3.0
            if s.pulse_on and ph < 0.9:
                d = ph / 0.9 * cum[-1]
                m.move_to(P(np.interp(d, cum, xs), np.interp(d, cum, ys)))
                m.set_opacity(1)
            else:
                m.set_opacity(0)
        s.pulse.add_updater(pul)
        s.cord.add_updater(lambda m: m.set_fill(TEAL, opacity=0.12 + 0.05 * np.sin(1.3 * t.get_value())))
        s.brain.add_updater(lambda m: m.set_fill(BLUE, opacity=0.12 + 0.05 * np.sin(1.1 * t.get_value() + 1)))
        s.soma.add_updater(lambda m: m.set_fill(GOLD, opacity=0.25 + 0.1 * np.sin(1.7 * t.get_value())))

    def show(s):
        s.sc.add(s.body)
        s.start()

    def puff(s):
        return VGroup(*[Arrow(P(x, 3.4), P(x, 2.35), buff=0, color=TEXT, stroke_width=6, tip_length=0.22,
                              max_tip_length_to_length_ratio=0.4) for x in (-5.95, -5.4, -4.85)])


def pop(group, color):
    return AnimationGroup(*[Indicate(b, color=color, scale_factor=1.5) for b in group])


def lock():
    body = RoundedRectangle(corner_radius=0.06, width=0.55, height=0.42, stroke_color=TEXT, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.3)
    sh = Arc(radius=0.18, start_angle=0, angle=PI, color=TEXT, stroke_width=4).move_to(body.get_top() + UP * 0.1)
    return VGroup(sh, body)


def tile(text, color, size=24):
    return chip(text, color, size=size, pad=0.14)


def question(text="After deletion, what changes?"):
    return T(text, 40, TEXT).move_to(P(-1.5, -3.3))


class SelectorMix:
    pass


def selector(x=-4.0):
    bar = Rectangle(width=0.18, height=2.4, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.35)
    bar.move_to(P(x, 0.2))
    lbl = T("Advillin-Cre", 28, TEXT).move_to(P(x, -1.75))
    return VGroup(bar, lbl)


# ---------------------------------------------------------------------------------------------
class S00Hook(SpokenScene):
    def construct(self):
        w = World(self, badges=(), gauge=0.12, pulse=False, labels=())
        self.play(FadeIn(w.body), run_time=1.6)
        w.start()
        self.at("can changing the first touch neuron")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.04), run_time=1.4)
        self.at("a gentle air puff")
        puff = w.puff()
        self.play(FadeIn(puff, shift=DOWN * 0.3), run_time=0.8)
        self.at("bends hairs")
        self.play(w.bend.animate.set_value(1), run_time=1.0)
        self.at("a gold sensory neuron")
        w.pulse_on = True
        self.play(FadeOut(puff), w.bend.animate.set_value(0), FadeIn(w.lbl["neuron"]), run_time=0.8)
        self.at("a teal spinal cord")
        self.play(FadeIn(w.lbl["cord"]), Indicate(w.cord, color=TEAL, scale_factor=1.03), run_time=1.0)
        self.at("a blue brain")
        self.play(FadeIn(w.lbl["brain"]), Indicate(w.brain, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("the mouse's movement")
        self.play(FadeIn(w.lbl["gauge"]), w.g.animate.set_value(0.8), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Readout(SpokenScene):
    def construct(self):
        w = World(self, badges=(), gauge=0.8, labels=("neuron", "cord", "brain", "gauge"))
        w.show()
        puff = w.puff()
        lk = lock().move_to(P(-3.9, 2.9))
        fl = T("fixed stimulus", 28, TEXT).move_to(P(-1.9, 2.9))
        self.at("a fixed air puff")
        self.play(FadeIn(puff, shift=DOWN * 0.3), w.bend.animate.set_value(1), run_time=0.9)
        self.play(FadeIn(lk), FadeIn(fl), w.bend.animate.set_value(0), run_time=0.8)
        self.at("measured movement")
        self.play(Indicate(w.gout, color=RED, scale_factor=1.06), run_time=1.2)
        self.at("the puff stays constant")
        self.play(Indicate(puff, color=TEXT, scale_factor=1.1), w.bend.animate.set_value(1), w.g.animate.set_value(0.45), run_time=1.2)
        self.play(w.bend.animate.set_value(0), run_time=0.5)
        self.at("movement gauge changes")
        self.play(Indicate(puff, color=TEXT, scale_factor=1.1), w.bend.animate.set_value(1), w.g.animate.set_value(0.85), run_time=1.2)
        self.play(w.bend.animate.set_value(0), run_time=0.5)
        self.at("detection threshold")
        self.play(Indicate(lk, color=GOLD, scale_factor=1.2), run_time=1.2)
        self.at("it also cannot tell us")
        bub = RoundedRectangle(corner_radius=0.2, width=1.8, height=1.1, stroke_color=GREY, stroke_width=4).move_to(P(-5.4, -2.6))
        q = T("?", 44, GREY).move_to(bub)
        self.play(FadeIn(VGroup(bub, q)), run_time=0.8)
        self.at("experiences touch")
        cross = VGroup(Line(bub.get_corner(UL), bub.get_corner(DR), color=RED, stroke_width=7),
                       Line(bub.get_corner(UR), bub.get_corner(DL), color=RED, stroke_width=7))
        self.play(Create(cross), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Restrict(SpokenScene):
    def construct(self):
        w = World(self, badges=(), gauge=0.55, labels=("neuron", "cord", "brain", "gauge"))
        w.show()
        self.at("gene badge")
        allb = VGroup(w.gold_b, w.teal_b, w.blue_b)
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in list(w.gold_b) + list(w.teal_b) + list(w.blue_b)], lag_ratio=0.25), run_time=2.0)
        self.at("advilin cre")
        sel = selector(-4.0)
        self.play(FadeIn(sel, shift=RIGHT * 0.3), run_time=0.8)
        self.at("removes")
        self.play(sel.animate.shift(RIGHT * 1.1), run_time=1.1)
        self.play(FadeOut(w.gold_b[0], scale=0.3), Indicate(w.soma, color=GOLD), run_time=0.8)
        self.at("dorsal root")
        self.play(Indicate(sel[0], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.at("trigeminal")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.2)
        self.at("the driver")
        chp = chip("sympathetic ganglion", GOLD, size=26).move_to(P(-1.4, -2.9))
        self.play(FadeIn(chp, shift=UP * 0.2), run_time=0.8)
        self.at("resident spinal")
        self.play(FadeOut(chp), pop(w.teal_b, TEAL), pop(w.blue_b, BLUE), run_time=1.5)
        self.at("the sensory")
        self.play(sel.animate.shift(RIGHT * 3.3), run_time=1.4)
        self.at("central terminal")
        self.play(FadeOut(w.gold_b[1], scale=0.3), Indicate(w.term, color=GOLD, scale_factor=1.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Predict(SpokenScene):
    def construct(self):
        w = World(self, badges=("gold", "teal", "blue"), gauge=0.12, labels=("gauge",))
        w.show()
        sel = selector(-2.9)
        q = T("?", 64, RED).move_to(P(GX, GY0 + GH / 2))
        self.add(sel, q)
        self.at("deleting mecp2")
        c1 = chip("Mecp2", GOLD, size=30).move_to(P(-5.5, 3.2))
        self.play(FadeIn(c1), run_time=0.4)
        self.play(c1.animate.move_to(P(-2.9, 2.2)), run_time=0.7)
        self.play(FadeOut(c1, scale=0.3), FadeOut(w.gold_b, scale=0.3), run_time=0.5)
        self.at("or g")
        self.play(FadeIn(w.gold_b), run_time=0.3)
        c2 = chip("Gabrb3", GOLD, size=30).move_to(P(-5.5, 3.2))
        self.play(FadeIn(c2), run_time=0.3)
        self.play(c2.animate.move_to(P(-2.9, 2.2)), run_time=0.6)
        self.play(FadeOut(c2, scale=0.3), FadeOut(w.gold_b, scale=0.3), run_time=0.5)
        self.at("targeted population")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("resident's central")
        self.play(pop(w.teal_b, TEAL), pop(w.blue_b, BLUE), run_time=1.6)
        self.at("if the first neuron")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), Indicate(q, color=RED), run_time=1.4)
        self.at("what should happen")
        self.play(FadeIn(question(), shift=UP * 0.2), run_time=0.8)
        self.finish()


class S04Pause(NarratedScene):
    def construct(self):
        w = World(self, badges=("teal", "blue"), gauge=0.12, labels=("gauge",))
        w.show()
        sel = selector(-2.9)
        q = T("?", 64, RED).move_to(P(GX, GY0 + GH / 2))
        self.add(sel, q, question())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05DeleteReveal(SpokenScene):
    def construct(self):
        w = World(self, badges=("teal", "blue"), gauge=0.35, labels=("gauge",))
        w.show()
        ctrl = DashedLine(P(GX - 0.65, GY0 + GH * 0.35), P(GX + 0.65, GY0 + GH * 0.35), color=GREY, stroke_width=4)
        ctl = T("control", 24, GREY).move_to(P(3.6, GY0 + GH * 0.35))
        self.add(ctrl, ctl)
        puff = w.puff()
        self.at("the response")
        self.play(FadeIn(puff, shift=DOWN * 0.3), w.bend.animate.set_value(1), run_time=0.8)
        self.play(w.g.animate.set_value(0.88), run_time=1.4)
        tiles = [tile("air-puff response", ORANGE), tile("texture task", ORANGE), tile("selected assays", ORANGE)]
        row = VGroup(*tiles).arrange(RIGHT, buff=0.25).move_to(P(-2.0, -2.9))
        self.play(FadeOut(puff), w.bend.animate.set_value(0), GrowFromPoint(tiles[0], P(GX, GY0 + 1.0)), run_time=0.9)
        self.at("texture discrimination")
        self.play(GrowFromPoint(tiles[1], P(GX, GY0 + 1.0)), run_time=1.0)
        self.at("tactile")
        self.play(Indicate(tiles[0], color=ORANGE, scale_factor=1.08), run_time=1.0)
        self.at("selected anxiety")
        self.play(GrowFromPoint(tiles[2], P(GX, GY0 + 1.0)), run_time=1.0)
        self.at("gene loss")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.04), run_time=1.3)
        self.at("sufficient for")
        stamp = T("sufficient for\nthese outcomes", 28, GOLD, line_spacing=0.7).move_to(P(-2.75, -0.9))
        self.play(FadeIn(stamp, scale=1.3), run_time=0.8)
        self.at("sufficient does")
        ne = T("not exclusive", 28, ORANGE).move_to(P(-2.75, -1.95))
        self.play(FadeIn(ne, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s06_tiles():
    g = VGroup(tile("tactile", GREEN), tile("anxiety-like", GREEN), tile("social", GREEN)).arrange(RIGHT, buff=0.25)
    g.move_to(P(0, -2.35)).align_to(P(-6.6, 0), LEFT)
    r = VGroup(tile("lethality", RED), tile("memory", RED), tile("motor", RED)).arrange(RIGHT, buff=0.25)
    r.move_to(P(0, -3.3)).align_to(P(-6.6, 0), LEFT)
    return g, r


class S06Restore(SpokenScene):
    def construct(self):
        w = World(self, badges=("teal", "blue"), gauge=0.88, labels=("gauge",))
        w.show()
        w.gold_b.set_opacity(0)
        self.add(w.gold_b)
        ctrl_y = GY0 + GH * 0.35
        ctrl = DashedLine(P(GX - 0.65, ctrl_y), P(GX + 0.65, ctrl_y), color=GREY, stroke_width=4)
        self.add(ctrl)
        self.at("otherwise null")
        self.play(*[b.animate.set_opacity(0.2) for b in list(w.teal_b) + list(w.blue_b) + list(w.gold_b)], run_time=1.2)
        self.at("researchers restored")
        self.play(*[b.animate.set_opacity(1) for b in w.gold_b], run_time=0.8)
        self.play(pop(w.gold_b, GOLD), run_time=1.0)
        self.at("mainly in the")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.4)
        green, red = s06_tiles()
        lab = T("assay outcomes", 26, TEXT).move_to(P(2.4, -3.3))
        marker = VGroup(DashedLine(P(3.7, -2.7), P(3.7, -1.95), color=GREEN, stroke_width=4), T("control", 24, GREEN).move_to(P(3.7, -1.65)))
        self.at("tactile sensitivity")
        self.play(FadeIn(green[0], shift=UP * 0.2), FadeIn(lab), run_time=0.8)
        self.at("anxiety like")
        self.play(FadeIn(green[1], shift=UP * 0.2), run_time=0.8)
        self.at("social measures")
        self.play(FadeIn(green[2], shift=UP * 0.2), FadeIn(marker), run_time=0.8)
        self.at("shifted toward control")
        dx = 3.3 - green.get_right()[0]
        self.play(green.animate.shift(RIGHT * dx), w.g.animate.set_value(0.42), run_time=2.2)
        self.at("lethality")
        self.play(FadeIn(red[0], shift=UP * 0.2), run_time=0.8)
        self.at("memory deficits")
        self.play(FadeIn(red[1], shift=UP * 0.2), run_time=0.8)
        self.at("motor deficits")
        self.play(FadeIn(red[2], shift=UP * 0.2), run_time=0.8)
        self.at("did not")
        self.play(Indicate(red, color=RED, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Bounds(SpokenScene):
    def construct(self):
        w = World(self, badges=("teal", "blue", "gold"), gauge=0.42, labels=())
        w.show()
        green, red = s06_tiles()
        dx = 3.3 - green.get_right()[0]
        green.shift(RIGHT * dx)
        marker = VGroup(DashedLine(P(3.7, -2.7), P(3.7, -1.95), color=GREEN, stroke_width=4), T("control", 24, GREEN).move_to(P(3.7, -1.65)))
        lab = T("assay outcomes", 26, TEXT).move_to(P(2.4, -3.3))
        self.add(green, red, marker, lab)
        self.at("restoring mecp2")
        self.play(pop(w.gold_b, GOLD), run_time=1.2)
        self.at("rescued selected outcomes")
        b1 = RoundedRectangle(corner_radius=0.15, width=5.2, height=2.5, stroke_color=GOLD, stroke_width=6).move_to(P(-1.6, 0.6))
        b2 = SurroundingRectangle(green, color=GOLD, buff=0.12, stroke_width=6, corner_radius=0.15)
        self.play(Create(b1), Create(b2), run_time=1.6)
        self.at("left others unchanged")
        self.play(Indicate(red, color=RED, scale_factor=1.05), run_time=1.2)
        self.at("draws a boundary")
        self.play(Indicate(b1, color=GOLD, scale_factor=1.03), Indicate(b2, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("peripheral sensory")
        br = Brace(b1, UP, color=GOLD, buff=0.08)
        bl = T("one contribution", 30, GOLD).next_to(br, UP, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(bl, shift=UP * 0.15), run_time=1.2)
        self.at("does not explain every")
        self.play(Indicate(w.brain, color=BLUE, scale_factor=1.04), Indicate(w.cord, color=TEAL, scale_factor=1.03), run_time=1.4)
        self.at("same mechanism in people")
        hx, hy = 5.4, -1.5
        human = VGroup(Circle(radius=0.3, color=TEXT, stroke_width=4).move_to(P(hx, hy + 0.9)),
                       Line(P(hx, hy + 0.6), P(hx, hy - 0.4), color=TEXT, stroke_width=4),
                       Line(P(hx - 0.55, hy + 0.3), P(hx + 0.55, hy + 0.3), color=TEXT, stroke_width=4),
                       Line(P(hx, hy - 0.4), P(hx - 0.4, hy - 1.2), color=TEXT, stroke_width=4),
                       Line(P(hx, hy - 0.4), P(hx + 0.4, hy - 1.2), color=TEXT, stroke_width=4))
        gap = DashedLine(P(4.4, -0.5), P(4.4, -2.8), color=GREY, stroke_width=4)
        nt = T("not tested here", 26, TEXT).move_to(P(5.4, -3.3))
        self.play(FadeOut(w.gauge), FadeIn(human), Create(gap), FadeIn(nt), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Takeaways(SpokenScene):
    def construct(self):
        w = World(self, badges=("gold", "teal", "blue"), gauge=0.6, labels=("neuron", "cord", "brain"))
        w.show()
        self.at("now gather")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("a restricted manipulation")
        l1 = T("restricted cells", 32, GOLD).move_to(P(-2.4, 2.9))
        self.play(FadeIn(l1, shift=DOWN * 0.15), run_time=0.9)
        self.at("locate one contribution")
        self.play(pop(w.gold_b, GOLD), run_time=1.2)
        self.at("without explaining the whole")
        l2 = T("selected outcomes", 32, RED).move_to(P(1.2, -2.3))
        self.play(FadeIn(l2, shift=UP * 0.15), Indicate(w.gout, color=RED, scale_factor=1.06), run_time=1.0)
        self.at("keep the full pathway")
        l3 = T("bounded inference", 32, TEXT).move_to(P(1.2, -3.2))
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=1.0)
        self.at("ask exactly which cells")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.03), pop(w.teal_b, TEAL),
                  pop(w.blue_b, BLUE), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Scope(SpokenScene):
    def construct(self):
        w = World(self, badges=("gold", "teal", "blue"), gauge=0.6, labels=("brain",))
        w.show()
        self.at("whether the brain")
        self.play(Indicate(w.brain, color=BLUE, scale_factor=1.05), run_time=1.2)
        self.at("one targeted population")
        ring = RoundedRectangle(corner_radius=0.15, width=5.4, height=2.5, stroke_color=GOLD, stroke_width=6).move_to(P(-1.6, 0.6))
        self.play(Create(ring), run_time=1.2)
        self.at("one measured outcome")
        gring = SurroundingRectangle(w.gauge, color=RED, buff=0.12, stroke_width=6, corner_radius=0.12)
        self.play(Create(gring), run_time=1.2)
        self.at("other cells remain")
        self.play(pop(w.teal_b, TEAL), pop(w.blue_b, BLUE), run_time=1.4)
        words = ["cells", "assay", "species", "time"]
        xs = [-4.8, -2.0, 0.8, 3.6]
        labs = [T(wd, 32, TEXT).move_to(P(x, 3.2)) for wd, x in zip(words, xs)]
        for i, lb in enumerate(labs):
            base = lb.get_center().copy()
            lb.add_updater(lambda m, b=base, i=i: m.move_to(b + P(0.18 * np.cos(0.8 * w.t.get_value() + i * 1.6), 0.12 * np.sin(0.8 * w.t.get_value() + i * 1.6))))
        self.at("the cells")
        self.play(FadeIn(labs[0]), run_time=0.6)
        self.at("assay")
        self.play(FadeIn(labs[1]), run_time=0.6)
        self.at("species")
        self.play(FadeIn(labs[2]), run_time=0.6)
        self.at("developmental schedule")
        self.play(FadeIn(labs[3]), run_time=0.6)
        self.finish()


class S10End(EndCard):
    LINE = "A restricted test locates one contribution, not the whole phenotype."
