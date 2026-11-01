"""How the cerebellum learns from error (Biochemistrypedia neuroscience explainer)

Timed to the SPOKEN words (self.at cues read audio/words.json). Circuits are drawn as labelled boxes
and simple neurons; no brain section is drawn. The recording and the prism bars are computed from the
lesson's own numbers (130 simple spikes and 2 complex spikes in 2 s; E0 = 20 cm, k = 0.30).

COLOR MAP (one color per concept, whole video)
  BLUE   = mossy fibres, granule cells, parallel fibres (the context input)
  ORANGE = climbing fibre, inferior olive, complex spike, and the landing error (the error/teacher signal)
  GREEN  = Purkinje cell and its simple spikes
  TEAL   = deep nuclei and their output
  RED    = a weakened (depressed) synapse, and "no" in the evidence
  YELLOW = the movement itself: hand path, target, learned correction after the prisms
  GREY   = frames, axes, labels, ghost neighbours
Arrow styles: arrowhead = excites; flat bar = inhibits.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CTX, ERR, PUR, NUC, WEAK, MOVE = BLUE, ORANGE, GREEN, TEAL, RED, YELLOW


# ---------------------------------------------------------------- generic helpers
def P(x, y):
    return np.array([x, y, 0.0])


def exc(a, b, color, w=5):
    return Arrow(P(*a), P(*b), buff=0, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def inh(a, b, color, w=5, bar=0.22):
    """inhibitory arrow: a line ending in a flat bar across its end (works for any direction)."""
    a, b = P(*a), P(*b)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b - n * bar, b + n * bar, color=color, stroke_width=w + 1))


def box(text, color, cx, cy, w, size=24, op=0.16):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=0.62, stroke_color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=op).move_to(P(cx, cy))
    t = T(text, size, color).move_to(r)
    return VGroup(r, t)


def poly(pts, color, w=4, op=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op)
    m.set_points_as_corners([P(*p) for p in pts])
    return m


def legend(cx, cy):
    a = exc((cx - 1.55, cy), (cx - 1.0, cy), GREY, 4)
    ta = T("excites", 22, GREY).next_to(a, RIGHT, buff=0.12)
    b = inh((cx + 0.35, cy), (cx + 0.9, cy), GREY, 4, 0.15)
    tb = T("inhibits", 22, GREY).next_to(b, RIGHT, buff=0.12)
    return VGroup(a, ta, b, tb)


# ---------------------------------------------------------------- the circuit (one standard layout, rebuilt per scene)
GX = [-3.8, -2.8, -1.8]            # granule cell x
PFY = [2.55, 2.15, 1.75]           # parallel fibre y, one per granule cell
GY = -0.95
AX = 0.35                          # Purkinje cell (main) x
BX = 5.3                           # faint neighbour x
SY = 0.35
NUC_Y = -3.0


def fan(x, color, op=1.0):
    pts = [[(x, SY + 0.3), (x, 1.2)], [(x, 1.2), (x - 0.85, 2.7)], [(x, 1.2), (x - 0.3, 2.75)],
           [(x, 1.2), (x + 0.3, 2.75)], [(x, 1.2), (x + 0.85, 2.7)]]
    return VGroup(*[poly(p, color, 4, op) for p in pts])


def build_circuit():
    C = {}
    C["mossy_box"] = box("mossy fibres", CTX, -3.4, -3.0, 3.5)
    C["mossy_arrows"] = VGroup(*[exc((x, -2.68), (x, GY - 0.25), CTX) for x in GX])
    C["granule"] = VGroup(*[Circle(radius=0.2, color=CTX, fill_color=CTX, fill_opacity=0.5, stroke_width=3).move_to(P(x, GY)) for x in GX])
    C["glabel"] = T("granule cells", 22, CTX).move_to(P(-5.3, GY))
    C["pf"] = VGroup(*[poly([(x, GY + 0.2), (x, y), (6.2, y)], CTX, 4) for x, y in zip(GX, PFY)])
    C["pflabel"] = T("parallel fibres", 22, CTX).move_to(P(-1.7, 3.1))
    C["pur"] = VGroup(fan(AX, PUR), Circle(radius=0.3, color=PUR, fill_color=PUR, fill_opacity=0.45, stroke_width=3).move_to(P(AX, SY)))
    C["ghost"] = VGroup(fan(BX, GREY, 0.45), Circle(radius=0.3, color=GREY, fill_color=GREY, fill_opacity=0.2, stroke_width=3).move_to(P(BX, SY)).set_stroke(opacity=0.5))
    C["plabel"] = T("Purkinje\ncell", 22, PUR, line_spacing=0.8).move_to(P(1.85, SY))
    C["nuc_box"] = box("deep nuclei", NUC, 1.5, NUC_Y, 3.0)
    C["pur_axon"] = inh((AX, SY - 0.3), (AX, NUC_Y + 0.31), PUR)
    # climbing fibres: one per Purkinje cell
    C["olive"] = box("inferior olive", ERR, 5.0, NUC_Y, 2.5, size=22)
    C["cf"] = poly([(4.5, NUC_Y + 0.31), (4.5, -1.6), (2.9, -1.6), (2.9, 1.0), (AX + 0.05, 1.0)], ERR, 5)
    C["cf_ghost"] = poly([(5.75, NUC_Y + 0.31), (5.75, 1.0), (BX + 0.05, 1.0)], ERR, 4, 0.45)
    C["cflabel"] = T("climbing fibre", 22, ERR).move_to(P(4.35, -0.7))
    # synapses: where the first two parallel fibres cross the dendrites
    C["syn"] = VGroup(*[Dot(P(AX + dx, y), radius=0.1, color=CTX) for (dx, y) in [(-0.54, 2.55), (-0.27, 2.15), (0.15, 1.75)]])
    return C


def add_all(scene, C, keys):
    scene.add(*[C[k] for k in keys])


def pulse(scene, path_mob, color, run=1.0, r=0.11):
    d = Dot(path_mob.get_start(), radius=r, color=color)
    scene.play(MoveAlongPath(d, path_mob), run_time=run, rate_func=linear)
    scene.remove(d)


# ================================================================ s00
class S00Title(TitleCard):
    LESSON = "The Cerebellum"
    TITLE = "How the Cerebellum Learns from Error"


# ================================================================ s01 the miss
NPT = 200


def smooth(x):
    return 3 * x * x - 2 * x ** 3


def reach_path():
    start, target = P(-5.0, -2.0), P(3.0, 1.0)
    d = target - start
    L = np.linalg.norm(d)
    u = d / L
    nrm = np.array([-u[1], u[0], 0.0])
    pts = []
    for t in np.linspace(0, 1, NPT):
        if t < 0.55:
            q = t / 0.55
            along, lat = 1.25 * smooth(q), 0.45 * np.sin(np.pi * q)
        else:
            q = (t - 0.55) / 0.45
            along, lat = 1.25 - 0.25 * q, 0.55 * np.sin(2 * np.pi * 3 * q) * (0.15 + 0.85 * q)
        pts.append(start + u * L * along + nrm * lat)
    return pts, start, target


class S01Miss(SpokenScene):
    def construct(self):
        pts, start, target = reach_path()
        cup = VGroup(Circle(radius=0.42, color=MOVE, stroke_width=4), Circle(radius=0.16, color=MOVE, stroke_width=4)).move_to(target)
        tl = T("the cup", 24, MOVE).next_to(cup, DOWN, buff=0.45)
        sd = Dot(start, radius=0.14, color=GREY)
        sl = T("start", 22, GREY).next_to(sd, DOWN, buff=0.2)
        schem = T("schematic, hand seen from above", 22, GREY).move_to(P(4.0, -3.4))
        self.play(FadeIn(sd), FadeIn(sl), FadeIn(cup), FadeIn(tl), FadeIn(schem), run_time=self.beat(0.08))
        self.at("a person is not")
        n1 = chip("not paralysed", GREEN, 28).move_to(P(-3.7, 3.0))
        self.play(FadeIn(n1, shift=DOWN * 0.1), run_time=0.5)
        self.at("move badly")
        n2 = chip("moves badly", RED, 28).next_to(n1, RIGHT, buff=0.4)
        self.play(FadeIn(n2, shift=DOWN * 0.1), run_time=0.5)
        self.at("Reaches overshoot")
        ov = int(NPT * 0.55)
        full = poly([(p[0], p[1]) for p in pts], MOVE, 5)
        hand = Dot(pts[0], radius=0.14, color=MOVE)
        self.add(hand)
        tr = ValueTracker(0)
        path_part = lambda k: poly([(p[0], p[1]) for p in pts[:max(2, int(k))]], MOVE, 5)
        trail = always_redraw(lambda: path_part(tr.get_value()))
        hd = always_redraw(lambda: Dot(pts[min(len(pts) - 1, max(0, int(tr.get_value())))], radius=0.14, color=MOVE))
        self.remove(hand)
        self.add(trail, hd)
        self.play(tr.animate.set_value(ov + 6), run_time=1.6, rate_func=linear)
        peak = max(range(ov - 12, ov + 12), key=lambda i: np.dot(pts[i] - start, target - start))
        olab = T("overshoot", 24, MOVE).move_to(pts[peak] + P(0.3, -0.75))
        self.play(FadeIn(olab), run_time=0.4)
        self.at("The hand shakes")
        self.play(tr.animate.set_value(NPT - 1), run_time=2.6, rate_func=linear)
        shk = T("shakes near the cup", 24, MOVE).move_to(P(4.3, -0.7))
        self.play(FadeIn(shk), run_time=0.4)
        self.at("makes movements accurate")
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(olab), FadeOut(shk), run_time=0.5)
        acc = chip("cerebellum: accurate movements", PUR, 28).move_to(P(-1.0, 3.0))
        self.play(FadeIn(acc, shift=DOWN * 0.1), run_time=0.5)
        self.at("learns to keep them accurate")
        acc2 = chip("learns to keep them accurate", PUR, 28).next_to(acc, DOWN, buff=0.3)
        self.play(FadeIn(acc2, shift=DOWN * 0.1), run_time=0.5)
        self.at("How does it learn")
        q = T("How does it learn?", 44, TEXT, font=TITLE_FONT).move_to(P(-0.2, -2.7))
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ================================================================ s02 the circuit
class S02Circuit(SpokenScene):
    def construct(self):
        C = build_circuit()
        lg = legend(4.7, 3.3)
        self.play(FadeIn(lg), run_time=0.2)
        self.at("Here is the circuit")
        self.wait(0.3)
        self.at("Mossy")
        self.play(FadeIn(C["mossy_box"]), run_time=0.5)
        self.play(*[GrowArrow(a) for a in C["mossy_arrows"]], run_time=0.7)
        self.play(FadeIn(C["granule"]), FadeIn(C["glabel"]), run_time=0.6)
        self.at("Each granule cell sends")
        axons = [poly([(x, GY + 0.2), (x, y)], CTX, 4) for x, y in zip(GX, PFY)]
        self.play(*[Create(a) for a in axons], run_time=1.2)
        self.at("along the fold")
        self.remove(*axons)
        self.play(*[Create(p) for p in C["pf"]], FadeIn(C["pflabel"]), run_time=1.6)
        self.at("pass through the dendrites")
        self.play(FadeIn(C["pur"]), FadeIn(C["plabel"]), run_time=0.7)
        self.play(FadeIn(C["ghost"]), run_time=0.6)
        self.at("only output")
        self.play(Indicate(C["pur"][1], color=PUR, scale_factor=1.35), run_time=0.9)
        self.at("They release GABA")
        gl = chip("GABA", PUR, 24).move_to(P(1.55, -1.5))
        self.play(FadeIn(C["nuc_box"]), run_time=0.4)
        self.play(Create(C["pur_axon"]), FadeIn(gl), run_time=1.0)
        self.at("inhibit the deep")
        self.play(Indicate(C["nuc_box"], color=NUC, scale_factor=1.06), run_time=0.9)
        self.finish()


# ================================================================ s03 two kinds of spike
SIMPLE_T = None


def simple_times():
    rng = np.random.default_rng(7)
    base = (np.arange(130) + 0.5) * (2.0 / 130)
    return np.clip(base + rng.normal(0, 0.004, 130), 0.003, 1.997)


COMPLEX_T = [0.62, 1.41]
RX0, RX1 = -5.2, 5.2


def tx(t):
    return RX0 + (t / 2.0) * (RX1 - RX0)


class S03TwoSpikes(SpokenScene):
    def construct(self):
        C = build_circuit()
        keys = ["mossy_box", "mossy_arrows", "granule", "glabel", "pf", "pflabel", "pur", "ghost", "plabel", "nuc_box", "pur_axon"]
        add_all(self, C, keys)
        self.wait(0.2)
        self.at("The second input")
        self.play(FadeIn(C["olive"]), run_time=0.5)
        self.play(Create(C["cf"]), Create(C["cf_ghost"]), FadeIn(C["cflabel"]), run_time=1.4)
        self.at("receives one")
        self.play(Indicate(C["cf"], color=ERR, scale_factor=1.0), run_time=0.9)
        self.at("Simple spikes are")
        grp = VGroup(*[C[k] for k in keys + ["olive", "cf", "cf_ghost", "cflabel"]])
        self.play(FadeOut(grp), run_time=0.6)
        # recording panel
        y1, y2 = 1.3, -0.5
        ax = VGroup(Line(P(RX0, -1.35), P(RX1, -1.35), color=GREY, stroke_width=3))
        ticks = VGroup(*[VGroup(Line(P(tx(t), -1.35), P(tx(t), -1.45), color=GREY, stroke_width=3), M(f"{t} s", 22, GREY).move_to(P(tx(t), -1.8)))
                         for t in (0, 1, 2)])
        for t in (0, 1, 2):
            pass
        cap = T("made-up recording, 2 s", 24, GREY).move_to(P(0, 3.15))
        l1 = T("simple spikes", 24, PUR).move_to(P(-4.4, y1 + 0.85))
        l2 = T("complex spikes", 24, ERR).move_to(P(-4.2, y2 + 1.1))
        self.play(FadeIn(ax), FadeIn(ticks), FadeIn(cap), run_time=0.5)
        st = simple_times()
        sticks = VGroup(*[Line(P(tx(t), y1 - 0.25), P(tx(t), y1 + 0.25), color=PUR, stroke_width=3) for t in st])
        base1 = Line(P(RX0, y1 - 0.25), P(RX1, y1 - 0.25), color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        base2 = Line(P(RX0, y2 - 0.7), P(RX1, y2 - 0.7), color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        self.add(base1, base2)
        self.play(FadeIn(l1), LaggedStart(*[Create(s) for s in sticks], lag_ratio=0.012), run_time=2.4)
        self.at("A complex spike")
        cticks = VGroup(*[Line(P(tx(t), y2 - 0.7), P(tx(t), y2 + 0.65), color=ERR, stroke_width=7) for t in COMPLEX_T])
        self.play(FadeIn(l2), *[Create(c) for c in cticks], run_time=1.0)
        self.at("In a made up recording")
        c1 = VGroup(M("130 / 2 s = 65 Hz", 30, PUR)).move_to(P(-2.6, -2.75))
        self.play(Write(c1), run_time=1.2)
        self.at("Two complex spikes")
        c2 = M("2 / 2 s = 1 Hz", 30, ERR).move_to(P(2.8, -2.75))
        self.play(Write(c2), run_time=1.0)
        self.finish()


# ================================================================ s04 the teacher
class S04Teacher(SpokenScene):
    def construct(self):
        C = build_circuit()
        keys = ["mossy_box", "mossy_arrows", "granule", "glabel", "pf", "pur", "ghost", "plabel", "nuc_box",
                "pur_axon", "olive", "cf", "cf_ghost", "cflabel"]
        add_all(self, C, keys)
        self.add(C["syn"])
        self.wait(0.2)
        self.at("Mar")
        teach = chip("teacher", ERR, 26).move_to(P(3.95, 0.8))
        self.play(FadeIn(teach, shift=DOWN * 0.1), run_time=0.5)
        self.at("fires together")
        glow = [Line(P(x, y), P(6.2, y), color=YELLOW, stroke_width=6) for x, y in list(zip(GX, PFY))[:2]]
        cfglow = C["cf"].copy().set_color(YELLOW).set_stroke(width=9)
        self.play(*[Create(g) for g in glow], Create(cfglow), Indicate(C["olive"], color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.play(*[Flash(s, color=YELLOW, line_length=0.18, flash_radius=0.3) for s in C["syn"][:2]], run_time=0.8)
        self.remove(cfglow)
        self.remove(*glow)
        self.at("those synapses change")
        self.play(*[s.animate.set_color(YELLOW).scale(1.7) for s in C["syn"][:2]], run_time=0.7)
        self.at("Ito and Kano")
        rab = T("in rabbits: pairing both inputs", 24, GREY).move_to(P(-3.3, 3.4))
        self.play(FadeIn(rab), run_time=0.5)
        self.at("depressed for a long time")
        self.play(*[s.animate.set_color(WEAK).scale(0.5) for s in C["syn"][:2]], run_time=1.0)
        self.at("long term depression")
        ltd = chip("long-term depression (LTD)", WEAK, 26).move_to(P(2.2, 3.35))
        self.play(FadeIn(ltd, shift=DOWN * 0.1), run_time=0.6)
        self.at("A weaker synapse")
        self.play(C["pur"][1].animate.set_fill(PUR, opacity=0.12), run_time=0.7)
        fl = T("fires less", 22, PUR).move_to(P(1.6, SY))
        self.play(FadeOut(C["plabel"]), FadeIn(fl), run_time=0.4)
        self.at("inhibits its nuclear target less")
        thin = inh((AX, SY - 0.3), (AX, NUC_Y + 0.31), PUR, w=1.5, bar=0.12)
        self.play(Transform(C["pur_axon"], thin), run_time=0.8)
        self.at("so the nuclear output")
        self.play(C["nuc_box"][0].animate.set_fill(NUC, opacity=0.6), run_time=0.8)
        up = T("output rises", 22, NUC).move_to(P(1.95, -2.15))
        self.play(FadeIn(up), run_time=0.4)
        self.finish()


# ================================================================ s05 prisms
E0, K = 20.0, 0.30
ZY, SC = 0.2, 0.15       # zero line y; scene units per cm
BX0, BDX = -4.2, 0.95


def bx(n):
    return BX0 + BDX * n


def errv(n):
    return E0 * (1 - K) ** n


class S05Prisms(SpokenScene):
    def construct(self):
        axis = Line(P(-5.0, ZY), P(5.6, ZY), color=GREY, stroke_width=3)
        yl = T("landing error, cm: up is right of the target (thrower's right)", 22, GREY).move_to(P(1.3, 3.45))
        up = VGroup()
        dn = T("down is left of the target", 22, GREY).move_to(P(-3.6, -1.5))
        self.at("Try it with prism")
        self.play(FadeIn(axis), FadeIn(yl), FadeIn(up), FadeIn(dn), run_time=0.7)
        tk = VGroup(*[M(str(n), 22, GREY).move_to(P(bx(n), ZY - 0.3)) for n in range(8)])
        # tick labels for corrections sit on the zero line's upper side, bars hang up
        def bar(n, val, color):
            h = abs(val) * SC
            r = Rectangle(width=0.55, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.55)
            r.move_to(P(bx(n), ZY + (h / 2 if val >= 0 else -h / 2)))
            return r
        bars = [bar(n, errv(n), ERR) for n in range(8)]
        self.at("first throw lands")
        lab0 = M("20", 24, ERR).next_to(bars[0], UP, buff=0.1)
        self.play(GrowFromEdge(bars[0], DOWN), FadeIn(lab0), run_time=0.8)
        nlab = T("corrections", 22, GREY).move_to(P(bx(3.5), ZY - 0.7))
        self.at("Each throw corrects")
        kl = M("k = 0.30", 30, TEXT).move_to(P(3.9, 2.3))
        self.play(FadeIn(kl), run_time=0.5)
        self.at("The error falls")
        labs = {1: "14.0", 2: "9.8", 3: "6.86"}
        for n in (1, 2, 3):
            self.play(Transform(bars[0].copy(), bars[n]) if False else GrowFromEdge(bars[n], DOWN), FadeIn(M(labs[n], 22, ERR).next_to(bars[n], UP, buff=0.1)), run_time=0.7)
            self.wait(0.15)
        self.play(*[GrowFromEdge(bars[n], DOWN) for n in (4, 5, 6)], run_time=0.9)
        self.at("After seven corrections")
        lab7 = M("1.65", 24, ERR).next_to(bars[7], UP, buff=0.1)
        self.play(GrowFromEdge(bars[7], DOWN), FadeIn(lab7), run_time=0.7)
        self.play(FadeIn(tk), FadeIn(nlab), run_time=0.4)
        self.at("Now remove the prisms")
        off = chip("prisms removed", TEXT, 26).move_to(P(4.5, 1.05))
        self.play(FadeIn(off, shift=DOWN * 0.1), run_time=0.6)
        self.at("lands about")
        val = -(E0 - errv(7))
        ab = bar(8, val, MOVE).move_to(P(5.0, ZY - abs(val) * SC / 2))
        lab8 = M("18.4 cm left", 24, MOVE).next_to(ab, DOWN, buff=0.1)
        self.play(GrowFromEdge(ab, UP), run_time=1.0)
        self.play(FadeIn(lab8), run_time=0.4)
        self.at("recalibrated")
        rc = T("eye-hand mapping was recalibrated", 28, MOVE).move_to(P(-1.0, -3.3))
        self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ================================================================ s06 limits and the rule
def tick(c, color=GREEN, s=0.2):
    return VGroup(Line(c + P(-s, 0), c + P(-s * 0.3, -s * 0.8), color=color, stroke_width=6),
                  Line(c + P(-s * 0.3, -s * 0.8), c + P(s, s * 0.9), color=color, stroke_width=6))


def crossm(c, color=RED, s=0.17):
    return VGroup(Line(c + P(-s, -s), c + P(s, s), color=color, stroke_width=6),
                  Line(c + P(-s, s), c + P(s, -s), color=color, stroke_width=6))


class S06Limits(SpokenScene):
    def construct(self):
        # left card: monkeys
        c1 = RoundedRectangle(corner_radius=0.2, width=5.9, height=3.4, stroke_color=GREY, stroke_width=2.5).move_to(P(-3.2, 1.65))
        h1 = T("in two monkeys", 26, TEXT).move_to(P(-3.2, 2.95))
        r1 = T("gain-increase learning:", 22, TEXT).move_to(P(-3.2, 2.4))
        r1b = T("complex spike predicted", 22, TEXT).move_to(P(-3.2, 2.0))
        r1c = T("the next trial's output change", 22, TEXT).move_to(P(-3.2, 1.6))
        r2 = T("gain-decrease learning:", 22, TEXT).move_to(P(-3.2, 0.95))
        r2b = T("it did not", 22, TEXT).move_to(P(-3.2, 0.55))
        # right card: mice
        c2 = RoundedRectangle(corner_radius=0.2, width=5.9, height=3.4, stroke_color=GREY, stroke_width=2.5).move_to(P(3.2, 1.65))
        h2 = VGroup(T("in three mouse lines", 26, TEXT), T("no LTD in standard slice tests", 22, GREY)).arrange(DOWN, buff=0.08).move_to(P(3.2, 2.85))
        m = [T("vestibulo-ocular reflex", 24, TEXT).move_to(P(2.6, 1.95)),
             T("eyeblink conditioning", 24, TEXT).move_to(P(2.6, 1.4)),
             T("stepping task", 24, TEXT).move_to(P(2.6, 0.85))]
        # model strip
        s1 = box("climbing fibre", ERR, -3.9, -2.1, 2.9)
        s2 = box("weakened synapse", WEAK, 0.0, -2.1, 3.4)
        s3 = box("Purkinje cell", PUR, 3.9, -2.1, 2.8)
        a1 = exc((-2.4, -2.1), (-1.8, -2.1), TEXT, 5)
        a2 = exc((1.8, -2.1), (2.4, -2.1), TEXT, 5)
        ml = T("in the model", 24, GREY).move_to(P(0, -3.15))
        self.wait(0.3)
        self.at("The teacher idea has limits")
        self.play(Create(c1), Create(c2), run_time=0.7)
        self.at("In two monkeys")
        self.play(FadeIn(h1), run_time=0.4)
        self.at("complex spike predicted")
        self.play(FadeIn(r1), FadeIn(r1b), FadeIn(r1c), run_time=0.8)
        self.at("but not during")
        self.play(FadeIn(r2), FadeIn(r2b), run_time=0.8)
        self.at("Three mouse lines")
        self.play(FadeIn(h2), run_time=0.4)
        self.play(*[FadeIn(x) for x in m], run_time=0.8)
        self.at("learned all three")
        tk = [tick(P(5.5, y)) for y in (1.95, 1.4, 0.85)]
        self.play(*[FadeIn(x) for x in tk], run_time=0.8)
        lt = T("learned normally", 24, GREEN).move_to(P(3.2, 0.3))
        self.play(FadeIn(lt), run_time=0.4)
        self.at("is gated")
        g = chip("the effect is gated", ERR, 26).move_to(P(-3.2, -0.55))
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.5)
        self.at("remains a model")
        mdl = chip("Marr-Albus-Ito: a model", TEXT, 26).move_to(P(3.2, -0.55))
        self.play(FadeIn(mdl, shift=UP * 0.1), run_time=0.5)
        self.at("Keep this rule")
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(s3), FadeIn(ml), run_time=0.8)
        self.at("teaches")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("by weakening")
        self.play(GrowArrow(a2), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "In the model, the climbing fibre teaches by weakening synapses."
