"""How to show a gut synapse  (Biochemistrypedia explainer for gut-brain-sensing)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the gut lining (enteroendocrine) cell
  BLUE   = the vagal neuron
  YELLOW = fast transmitter route / glutamate / "synapse"
  PURPLE = hormone route
  TEAL   = light (optogenetic)
  GREEN  = current or firing present
  RED    = blocker, response abolished
  PINK   = modified rabies virus label
  GOLD   = sugar (stimulus, preference)
  GREY   = structure, limits, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88AB4"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def pair(y=-0.3, with_proc=True, with_nerve=True):
    """Gut cell (left) and vagal neuron (right), contact gap between the two bulbs."""
    d = {}
    d["body"] = RoundedRectangle(corner_radius=0.3, width=1.7, height=2.6, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.28).move_to([-4.3, y, 0])
    d["glbl"] = T("gut cell", 24, ORANGE).move_to([-4.3, y + 0.8, 0])
    d["proc"] = Line([-3.45, y, 0], [-1.88, y, 0], color=ORANGE, stroke_width=7)
    d["bulb"] = Circle(radius=0.28, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.9).move_to([-1.6, y, 0])
    d["nbulb"] = Circle(radius=0.28, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.9).move_to([-0.5, y, 0])
    d["axon"] = Line([-0.22, y, 0], [1.6, y, 0], color=BLUE, stroke_width=6)
    d["soma"] = Circle(radius=0.7, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.28).move_to([2.3, y, 0])
    d["axon2"] = Arrow([3.0, y, 0], [5.7, y, 0], buff=0, color=BLUE, stroke_width=6, tip_length=0.25)
    d["nlbl"] = T("vagal neuron", 24, BLUE).move_to([2.3, y - 1.1, 0])
    d["proc_g"] = VGroup(d["proc"], d["bulb"])
    d["nerve_g"] = VGroup(d["nbulb"], d["axon"], d["soma"], d["axon2"], d["nlbl"])
    d["cell_g"] = VGroup(d["body"], d["glbl"])
    return d


class S00Title(TitleCard):
    LESSON = "Sensing the gut"
    TITLE = "How to Show a Gut Synapse"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a gut cell silenced by light weakens sugar preference; two possible routes to the vagal neuron."""

    def construct(self):
        y = -0.3
        p = pair(y)
        tag = chip("mouse", GREY, 24).move_to([-5.6, 3.2, 0])
        bar = Rectangle(width=3.2, height=0.35, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([-4.3, -1.85, 0])
        bar_l = T("lining of the gut", 24, GREY).move_to([-4.3, -2.45, 0])
        pref = chip("mouse prefers sugar", GOLD, 24).move_to([3.4, 3.0, 0])
        self.at("In a mouse")
        self.play(FadeIn(tag), FadeIn(bar), FadeIn(bar_l), FadeIn(p["body"]), FadeIn(p["glbl"]), FadeIn(pref), run_time=0.9)
        beam = arr([-4.3, 3.1, 0], [-4.3, 1.2, 0], TEAL)
        beam_l = T("light silences it", 24, TEAL).move_to([-2.1, 2.3, 0])
        self.at("light can silence")
        self.play(GrowArrow(beam), FadeIn(beam_l), p["body"].animate.set_stroke(GREY).set_fill(GREY, 0.18),
                  p["glbl"].animate.set_color(GREY), run_time=0.8)
        pref2 = chip("sugar preference weaker", GOLD, 24, fill_opacity=0.05).move_to([3.4, 3.0, 0])
        self.at("no longer reliably prefers")
        self.play(ReplacementTransform(pref, pref2), run_time=0.8)
        nn = T("not a neuron", 26, ORANGE).move_to([-4.3, 1.75, 0])
        self.at("not a neuron")
        self.play(FadeOut(beam), FadeOut(beam_l), p["body"].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.28),
                  p["glbl"].animate.set_color(ORANGE), FadeIn(nn), run_time=0.7)
        self.at("reach the nervous system")
        self.play(Create(p["proc"]), FadeIn(p["bulb"]), FadeIn(p["nerve_g"]), run_time=1.2)
        hc = chip("hormone?", PURPLE, 26).move_to([-1.05, 2.0, 0])
        h1 = arr([-3.4, 1.0, 0], hc.get_left() + [-0.05, 0, 0], PURPLE, 4)
        h2 = arr(hc.get_right() + [0.05, 0, 0], [1.9, 0.55, 0], PURPLE, 4)
        self.at("Through a hormone")
        self.play(FadeIn(hc), GrowArrow(h1), GrowArrow(h2), run_time=0.8)
        sc = chip("fast synapse?", YELLOW, 26).move_to([-0.7, -1.9, 0])
        s1 = DashedLine([-1.05, -1.5, 0], [-1.05, -0.5, 0], color=YELLOW, stroke_width=4)
        s2 = arr([-1.32, y, 0], [-0.78, y, 0], YELLOW, 4, tip=0.15)
        self.at("or through a fast synapse")
        self.play(FadeIn(sc), Create(s1), GrowArrow(s2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Contact(SpokenScene):
    """the old hormone-only view, then a process that touches a nerve, then rabies tracing."""

    def construct(self):
        y = -0.3
        p = pair(y)
        old = T("before 2018: passive hormone release", 26, GREY).move_to([0, 3.2, 0])
        sn = T("sensory nerve", 24, BLUE).move_to([2.3, y - 1.1, 0])
        p["nerve_g"] = VGroup(p["nbulb"], p["axon"], p["soma"], p["axon2"], sn)
        self.add(p["cell_g"])
        self.play(FadeIn(old), run_time=0.5)
        self.at("passive hormone release")
        hl = T("hormone", 24, PURPLE).move_to([-1.0, 0.7, 0])
        dots = VGroup(*[Dot([-3.3, y + dy, 0], radius=0.11, color=PURPLE) for dy in (0.5, 0.1, -0.3, -0.7, -1.0)])
        self.play(FadeIn(hl), LaggedStart(*[d.animate.shift([5.6, 0.1 * i - 0.2, 0]).set_opacity(0.15) for i, d in enumerate(dots)],
                                          lag_ratio=0.15), run_time=2.0)
        self.play(FadeOut(dots), FadeOut(hl), FadeOut(old), run_time=0.4)
        plbl = T("process (neuropod)", 24, ORANGE).move_to([-1.6, -1.05, 0])
        self.at("a process on")
        self.play(Create(p["proc"]), FadeIn(p["bulb"]), FadeIn(plbl), run_time=1.0)
        nl = T("mucosal nerve", 24, BLUE).move_to([-1.0, 0.55, 0])
        self.at("touch mucosal nerves")
        self.play(FadeIn(p["nerve_g"]), FadeIn(nl), run_time=1.0)
        vl = T("modified rabies virus", 24, PINK).move_to([-4.3, 2.7, 0])
        v0 = Dot([-4.3, 2.2, 0], radius=0.14, color=PINK)
        self.at("rabies virus")
        self.play(FadeIn(vl), FadeIn(v0), run_time=0.6)
        vin = VGroup(*[Dot([x, y - 0.7 - 0.05 * i, 0], radius=0.1, color=PINK) for i, x in enumerate((-4.7, -4.3, -3.9))])
        self.at("infected the cells")
        self.play(ReplacementTransform(v0, vin), FadeOut(vl), run_time=0.8)
        vout = VGroup(*[Dot([-1.6, y, 0], radius=0.09, color=PINK) for _ in range(3)])
        self.at("cells and then")
        self.play(FadeIn(vout), run_time=0.2)
        self.play(*[vout[i].animate.move_to([2.0 + 0.3 * i, y + (0.2 if i == 1 else -0.1), 0]) for i in range(3)], run_time=1.2)
        mice = VGroup(*[Circle(radius=0.22, stroke_color=GREY, stroke_width=3) for _ in range(5)]).arrange(RIGHT, buff=0.35).move_to([3.4, 2.6, 0])
        ml = T("mice with infected colon nerves", 22, GREY).move_to([3.4, 3.2, 0])
        self.at("infected colon nerves")
        self.play(FadeIn(mice), FadeIn(ml), run_time=0.7)
        vn = T("vagal nodose neuron", 24, BLUE).move_to([2.3, y - 1.1, 0])
        res = T("2 of 5", 26, PINK, weight=BOLD).move_to([3.4, 1.9, 0])
        self.at("reached vagal")
        self.play(mice[0].animate.set_fill(PINK, 0.9).set_stroke(PINK), mice[1].animate.set_fill(PINK, 0.9).set_stroke(PINK),
                  ReplacementTransform(sn, vn), FadeIn(res), run_time=0.8)
        c1 = chip("connectivity: shown", PINK, 26).move_to([-3.0, -2.7, 0])
        self.at("That shows connectivity")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        c2 = chip("transmitter: not shown", YELLOW, 26).move_to([2.6, -2.7, 0])
        self.at("does not show the transmitter")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Speed(SpokenScene):
    """coculture in a dish: light on the gut cell, current in the neuron within 60 to 800 ms."""

    def construct(self):
        y = 0.9
        p = pair(y)
        dish = RoundedRectangle(corner_radius=0.3, width=12.4, height=4.2, stroke_color=GREY, stroke_width=3).move_to([0, 0.8, 0])
        dl = T("coculture in a dish", 24, GREY).move_to([3.8, 3.2, 0])
        self.add(p["cell_g"], p["proc_g"], p["nerve_g"])
        self.at("grew gut cells together")
        self.play(Create(dish), FadeIn(dl), run_time=1.0)
        beam = arr([-4.3, 3.45, 0], [-4.3, 2.35, 0], TEAL)
        bl = T("light", 24, TEAL).move_to([-3.5, 3.3, 0])
        self.at("Light switched on")
        self.play(GrowArrow(beam), FadeIn(bl), p["body"].animate.set_fill(ORANGE, 0.6), run_time=0.6)
        ax = Line([-5.5, -2.4, 0], [5.5, -2.4, 0], color=GREY, stroke_width=3)
        t0 = Line([-5.5, -2.15, 0], [-5.5, -2.65, 0], color=TEAL, stroke_width=4)
        tl0 = T("0", 22, TEAL).move_to([-5.5, -2.85, 0])
        self.at("currents appeared")
        yel = VGroup(*[Dot([-1.6, y + dy, 0], radius=0.07, color=YELLOW) for dy in (0.1, 0.0, -0.1)])
        ring = Circle(radius=0.86, stroke_color=GREEN, stroke_width=6).move_to([2.3, y, 0])
        cur = T("current", 24, GREEN, weight=BOLD).move_to([2.3, y + 1.15, 0])
        self.play(FadeIn(yel, scale=0.5), run_time=0.3)
        self.play(*[yel[i].animate.move_to([-0.5, y + (i - 1) * 0.1, 0]) for i in range(3)], run_time=0.6)
        self.play(FadeOut(yel), Create(ring), FadeIn(cur), FadeOut(beam), FadeOut(bl), run_time=0.5)
        self.at("milliseconds")
        win = Rectangle(width=8.8 - 0.66, height=0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.5).move_to([-5.5 + 0.66 + (8.8 - 0.66) / 2, -2.4, 0])
        t60 = T("60", 22, GREEN).move_to([-4.84, -2.85, 0])
        t800 = T("800 ms", 22, GREEN).move_to([3.3, -2.85, 0])
        wl = T("currents began 60 to 800 ms after the light (schematic window)", 24, GREEN).move_to([-0.9, -3.35, 0])
        self.play(Create(ax), Create(t0), FadeIn(tl0), run_time=0.5)
        self.play(FadeIn(win), FadeIn(t60), FadeIn(t800), FadeIn(wl), run_time=0.8)
        self.at("transcripts for")
        vg = chip("VGLUT1 transcripts", ORANGE, 22).move_to([-4.3, y - 1.75, 0])
        self.play(FadeIn(vg), run_time=0.5)
        gl = chip("glutamate", YELLOW, 24).move_to([-1.6, y + 1.2, 0])
        gdots = DashedLine([-1.6, y + 0.9, 0], [-1.6, y + 0.32, 0], color=YELLOW, stroke_width=4)
        self.at("fits glutamate")
        self.play(FadeIn(gl), FadeIn(gdots), run_time=0.6)
        self.at("fast transmitter")
        self.play(Indicate(VGroup(*gl[1:]), color=YELLOW), Indicate(wl, color=GREEN), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Blocker(SpokenScene):
    """blocker on the neuron: current lamp ON -> OFF -> ON after washout."""

    def construct(self):
        y = 0.4
        p = pair(y)
        lamp = Circle(radius=0.26, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.9).move_to([-1.3, 2.9, 0])
        lab = T("current in the neuron:", 26, GREY).move_to([1.2, 2.9, 0])
        on = T("ON", 28, GREEN, weight=BOLD).move_to([3.9, 2.9, 0])
        self.add(p["cell_g"], p["proc_g"], p["nerve_g"])
        self.play(FadeIn(lamp), FadeIn(lab), FadeIn(on), run_time=0.8)
        self.at("a blocker")
        kc = chip("kynurenic acid", RED, 26).move_to([-0.5, y - 1.8, 0])
        bar = inhib([-0.5, y - 1.45, 0], [-0.5, y - 0.3, 0])
        self.play(FadeIn(kc), run_time=0.5)
        self.at("glutamate receptors")
        self.play(Create(bar), run_time=0.5)
        off = T("OFF", 28, RED, weight=BOLD).move_to([3.9, 2.9, 0])
        self.at("It abolished")
        self.play(lamp.animate.set_fill(GREY, 0.3).set_stroke(GREY), ReplacementTransform(on, off), run_time=0.5)
        wash = T("washout", 26, GREY).move_to([-0.5, y - 1.8, 0])
        self.at("After washout")
        self.play(FadeOut(kc), FadeOut(bar), FadeIn(wash), run_time=0.6)
        on2 = T("ON", 28, GREEN, weight=BOLD).move_to([3.9, 2.9, 0])
        self.at("came back")
        self.play(lamp.animate.set_fill(GREEN, 0.9).set_stroke(GREEN), ReplacementTransform(off, on2), run_time=0.5)
        n4 = chip("4 neurons", GREY, 24).move_to([4.6, y - 1.9, 0])
        self.at("seen in four")
        self.play(FadeIn(n4), run_time=0.5)
        self.at("Recovery matters")
        self.play(Indicate(VGroup(lamp, on2), color=GREEN), run_time=0.8)
        a = chip("blocked receptors", RED, 28).move_to([-3.0, -2.9, 0])
        b = chip("damaged cells", GREY, 28).move_to([3.0, -2.9, 0])
        vs = T("or", 26, GREY).move_to([0, -2.9, 0])
        self.at("separates blocked receptors")
        self.play(FadeIn(a), FadeIn(vs), FadeIn(b), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Mouse(SpokenScene):
    """four manipulations in anaesthetised mice and what vagal firing did."""

    def construct(self):
        head = T("anaesthetised mice, recording from the cervical vagus", 26, GREY).move_to([0, 3.15, 0])
        rows = [("sucrose in the intestine", GOLD, "firing rises within seconds", GREEN),
                ("+ phloridzin, an SGLT1 blocker", RED, "response abolished", RED),
                ("light silences CCK cells", TEAL, "response abolished", RED),
                ("light drives CCK cells", TEAL, "firing rises", GREEN)]
        ys = [1.9, 0.7, -0.5, -1.7]
        items = []
        for (l, lc, r, rc), yy in zip(rows, ys):
            lch = chip(l, lc, 24).move_to([-3.3, yy, 0])
            rch = chip(r, rc, 24).move_to([3.3, yy, 0])
            ar = arr([-0.7, yy, 0], [0.6, yy, 0], GREY)
            items.append((lch, ar, rch))
        self.at("living mouse")
        self.play(FadeIn(head), run_time=0.6)
        self.at("cervical vagus")
        self.play(FadeIn(items[0][0]), run_time=0.5)
        self.at("of sucrose")
        self.play(GrowArrow(items[0][1]), FadeIn(items[0][2], shift=RIGHT * 0.2), run_time=0.6)
        self.at("which blocks")
        self.play(FadeIn(items[1][0]), run_time=0.5)
        self.at("abolished that response")
        self.play(GrowArrow(items[1][1]), FadeIn(items[1][2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("silenced the")
        self.play(FadeIn(items[2][0]), run_time=0.5)
        self.at("abolished it too")
        self.play(GrowArrow(items[2][1]), FadeIn(items[2][2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("drove the same")
        self.play(FadeIn(items[3][0]), run_time=0.5)
        self.at("raised vagal firing")
        self.play(GrowArrow(items[3][1]), FadeIn(items[3][2], shift=RIGHT * 0.2), run_time=0.5)
        nec = T("authors: necessary", 22, GREY).move_to([0.4, ys[2] - 0.45, 0])
        suf = T("authors: sufficient", 22, GREY).move_to([0.4, ys[3] - 0.45, 0])
        self.at("necessary and sufficient")
        self.play(FadeIn(nec), FadeIn(suf), run_time=0.6)
        a = chip("firing within seconds", GREEN, 24)
        b = T("could fit", 24, GREY)
        c = chip("hormone", PURPLE, 24)
        d = T("or", 24, GREY)
        e = chip("synapse", YELLOW, 24)
        ban = VGroup(a, b, c, d, e).arrange(RIGHT, buff=0.25).move_to([0, -3.1, 0])
        self.at("Firing within seconds alone")
        self.play(FadeIn(a), run_time=0.5)
        self.at("hormone or a synapse")
        self.play(FadeIn(b), FadeIn(c), FadeIn(d), FadeIn(e), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the chain of evidence, each link with its limit."""

    def construct(self):
        names = [("rabies\ntracing", PINK), ("speed in\na dish", GREEN), ("blocker,\nwashout", RED), ("silence and\ndrive in mice", TEAL)]
        chain = VGroup(*[chip(n, c, 24) for n, c in names]).arrange(RIGHT, buff=0.7).move_to([0, 1.9, 0])
        links = VGroup(*[arr(chain[i].get_right(), chain[i + 1].get_left(), GREY, 4, tip=0.18) for i in range(3)])
        tag = chip("mouse work", GREY, 24).move_to([-5.4, 3.2, 0])
        self.at("of this is")
        self.play(FadeIn(tag), FadeIn(chain), FadeIn(links), run_time=1.0)
        l1 = T("connectivity only", 22, RED).next_to(chain[0], DOWN, buff=0.3)
        self.at("Tracing shows")
        self.play(FadeIn(l1), run_time=0.5)
        mid = (chain[1].get_center() + chain[2].get_center()) / 2
        l2 = T("in a dish", 22, RED).move_to([mid[0], chain[1].get_bottom()[1] - 0.45, 0])
        self.at("are in a dish")
        self.play(FadeIn(l2), run_time=0.5)
        b1 = chip("18.9% of CCK cells touched sensory fibres (fixed tissue)", ORANGE, 24).move_to([0, -0.4, 0])
        self.at("touched sensory")
        self.play(FadeIn(b1, shift=UP * 0.15), run_time=0.6)
        b2 = chip("human data: glutamate release, organoids of one donor", GREY, 24).move_to([0, -1.25, 0])
        self.at("human data")
        self.play(FadeIn(b2, shift=UP * 0.15), run_time=0.6)
        b3 = chip("serotonin-making gut cell study: fibres not shown to be vagal", GREY, 24).move_to([0, -2.1, 0])
        self.at("gut cells the recorded")
        self.play(FadeIn(b3, shift=UP * 0.15), run_time=0.6)
        beside = T("a synaptic route exists beside hormones", 26, YELLOW).move_to([0, -3.1, 0])
        self.at("not make hormones irrelevant")
        self.play(FadeIn(beside), run_time=0.6)
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(l1, l2, b1, b2, b3, beside, tag)), run_time=0.7)
        rule = T("a chain of evidence, not one result", 36, TEXT, font=TITLE_FONT).move_to([0, -0.3, 0])
        fit(rule, max_w=11.5)
        self.at("chain of evidence")
        self.play(Write(rule), chain.animate.move_to([0, 1.5, 0]), links.animate.move_to(links.get_center() + [0, -0.4, 0]), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "A fast synapse is shown by a chain of evidence."
