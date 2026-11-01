"""Counting signs around the brake: the basal ganglia as a signed loop (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The whole film is one flat box-and-arrow circuit of the classic rate model (no brain outline, no
section). Box brightness is a qualitative activity level "in this sketch"; no firing rate is drawn.
Only the lesson's links and signs are drawn.

COLOR MAP (one color per concept, whole video)
  GREEN  = excitatory link and its sign (+1); "cortical drive up"
  RED    = inhibitory link and its sign (-1); "cortical drive down"; the brake; akinesia
  GOLD   = modulatory dopamine link and SNc (dashed)
  BLUE   = a population (box); its fill brightness is its activity level in this sketch
  YELLOW = the thing that moves or is highlighted (spikes, outline of the box in play)
  GREY   = legend, key, notes, de-emphasised text
  TEXT   = the product being multiplied
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

EXC, INH, MOD, POP, HI = GREEN, RED, GOLD, BLUE, YELLOW
LOW, MID, HIGH = 0.07, 0.30, 0.66
DIM = 0.22
MINUS = "−"

# centre, (half width, half height)
POS = {"ctx": (-2.9, 2.30), "thal": (4.9, 2.30), "gpi": (4.9, 0.45), "gpe": (-0.6, -1.95),
       "stn": (2.6, -1.95), "snc": (-5.45, -1.95), "str": (-2.9, 0.10), "D1": (-2.9, 0.45), "D2": (-2.9, -0.50)}
HALF = {"ctx": (1.0, 0.4), "thal": (1.0, 0.4), "gpi": (0.8, 0.4), "gpe": (0.8, 0.4), "stn": (0.8, 0.4),
        "snc": (0.8, 0.4), "str": (1.45, 1.225), "D1": (1.2, 0.31), "D2": (1.2, 0.31)}
NAMES = {"ctx": "Cortex", "thal": "Thalamus", "gpi": "GPi", "gpe": "GPe", "stn": "STN", "snc": "SNc"}

# name: (from, to, kind)
LINKS = {"c_s": ("ctx", "str", "exc"), "s_gpi": ("D1", "gpi", "inh"), "s_gpe": ("D2", "gpe", "inh"),
         "gpe_stn": ("gpe", "stn", "inh"), "stn_gpi": ("stn", "gpi", "exc"), "gpi_t": ("gpi", "thal", "inh"),
         "t_c": ("thal", "ctx", "exc"), "da1": ("snc", "D1", "mod"), "da2": ("snc", "D2", "mod")}
KCOL = {"exc": EXC, "inh": INH, "mod": MOD}
# sign label offsets from link midpoint
LOFF = {"c_s": (0.5, 0.0), "s_gpi": (0.0, 0.33), "s_gpe": (0.8, 0.05), "gpe_stn": (0.0, 0.33),
        "stn_gpi": (0.55, 0.0), "gpi_t": (0.55, 0.0), "t_c": (0.0, 0.33)}
SIGN = {"c_s": 1, "s_gpi": -1, "s_gpe": -1, "gpe_stn": -1, "stn_gpi": 1, "gpi_t": -1, "t_c": 1}
DIRECT = ["c_s", "s_gpi", "gpi_t", "t_c"]
INDIRECT = ["c_s", "s_gpe", "gpe_stn", "stn_gpi", "gpi_t", "t_c"]
STRIP_Y = 3.22
KEY_Y = -3.2


def P(name):
    x, y = POS[name]
    return np.array([x, y, 0.0])


def edge(src, dst, gap=0.07):
    c, d = P(src), P(dst)
    v = d - c
    hw, hh = HALF[src]
    t = min(hw / abs(v[0]) if abs(v[0]) > 1e-6 else 1e9, hh / abs(v[1]) if abs(v[1]) > 1e-6 else 1e9)
    u = v / np.linalg.norm(v)
    return c + v * t + u * gap


EP = {("snc", "D1"): ((-5.7, -1.56, 0.0), (-4.15, 0.42, 0.0)), ("snc", "D2"): ((-5.2, -1.56, 0.0), (-4.15, -0.5, 0.0))}


def make_link(a, b, kind):
    p, q = edge(a, b), edge(b, a)
    if (a, b) in EP:
        p, q = np.array(EP[(a, b)][0]), np.array(EP[(a, b)][1])
    col = KCOL[kind]
    u = (q - p) / np.linalg.norm(q - p)
    if kind == "inh":
        shaft = Line(p, q - u * 0.02, color=col, stroke_width=5)
        n = np.array([-u[1], u[0], 0.0])
        mark = Line(q + n * 0.2, q - n * 0.2, color=col, stroke_width=7)
    else:
        tip = q - u * 0.2
        shaft = (DashedLine(p, tip, color=col, stroke_width=4.5, dash_length=0.13) if kind == "mod"
                 else Line(p, tip, color=col, stroke_width=5))
        mark = Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.15)
        mark.rotate(np.arctan2(u[1], u[0]) - PI / 2).move_to(q - u * 0.1)
    return VGroup(shaft, mark)


def make_node(name, text, size=26):
    hw, hh = HALF[name]
    rect = RoundedRectangle(corner_radius=0.12, width=2 * hw, height=2 * hh, stroke_color=POP, stroke_width=3,
                            fill_color=POP, fill_opacity=MID).move_to(P(name))
    lab = T(text, size=size, color=TEXT).move_to(rect)
    return VGroup(rect, lab)


class Diag:
    """The circuit. Rebuilt identically at the start of each scene."""

    def __init__(self, links=(), nodes=("ctx", "thal", "gpi", "gpe", "stn", "snc", "str"), lv=None, op=1.0):
        self.node = {}
        for n in ("ctx", "thal", "gpi", "gpe", "stn", "snc"):
            self.node[n] = make_node(n, NAMES[n])
        out = RoundedRectangle(corner_radius=0.16, width=2 * HALF["str"][0], height=2 * HALF["str"][1],
                               stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to(P("str"))
        slab = T("Striatum", 24, TEXT).move_to(P("str") + UP * 0.93)
        self.node["str"] = VGroup(out, slab)
        self.node["D1"] = make_node("D1", "D1 · direct", 22)
        self.node["D2"] = make_node("D2", "D2 · indirect", 22)
        self.node["snc"][0].set_stroke(MOD).set_fill(MOD, opacity=MID)
        self.names = list(nodes) + ["D1", "D2"] if "str" in nodes else list(nodes)
        self.link = {k: make_link(*v) for k, v in LINKS.items()}
        self.lab = {}
        for k, off in LOFF.items():
            s = SIGN[k]
            m = LinesOff = None
            t = M(("+1" if s > 0 else MINUS + "1"), 26, EXC if s > 0 else INH, weight=BOLD)
            mid = (edge(LINKS[k][0], LINKS[k][1]) + edge(LINKS[k][1], LINKS[k][0])) / 2
            t.move_to(mid + np.array([off[0], off[1], 0.0]))
            self.lab[k] = t
        self.lv = {n: MID for n in ("ctx", "thal", "gpi", "gpe", "stn", "snc", "D1", "D2")}
        if lv:
            self.lv.update(lv)
        for n, v in self.lv.items():
            self.node[n][0].set_fill(opacity=v)
        self.shown = list(links)
        for k in self.link:
            self.link[k].set_opacity(op if k in self.shown else 0)
        for k in self.lab:
            self.lab[k].set_opacity(0)

    def mobs(self):
        g = [self.node[n] for n in self.names]
        return g

    def everything(self):
        return VGroup(*self.link.values(), *self.lab.values(), *self.node.values())

    def level(self, name, v, **kw):
        self.lv[name] = v
        return self.node[name][0].animate.set_fill(opacity=v)

    def only(self, keys, others=DIM):
        return [self.link[k].animate.set_opacity(1.0 if k in keys else others) for k in self.link
                if k in self.shown and not k.startswith("da")]


def legend():
    items = []
    for kind, text in (("exc", "excitatory +1"), ("inh", "inhibitory " + MINUS + "1"), ("mod", "modulatory")):
        col = KCOL[kind]
        if kind == "inh":
            a = VGroup(Line(LEFT * 0.3, RIGHT * 0.25, color=col, stroke_width=5),
                       Line(RIGHT * 0.3 + UP * 0.15, RIGHT * 0.3 + DOWN * 0.15, color=col, stroke_width=7))
        elif kind == "exc":
            a = VGroup(Line(LEFT * 0.3, RIGHT * 0.15, color=col, stroke_width=5),
                       Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.13)
                       .rotate(-PI / 2).move_to(RIGHT * 0.25))
        else:
            a = VGroup(DashedLine(LEFT * 0.3, RIGHT * 0.15, color=col, stroke_width=4.5, dash_length=0.12),
                       Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.13)
                       .rotate(-PI / 2).move_to(RIGHT * 0.25))
        items.append(VGroup(a, T(text, 22, GREY)).arrange(RIGHT, buff=0.15))
    g = VGroup(*items).arrange(RIGHT, buff=0.5)
    g.move_to([-6.25 + g.width / 2, KEY_Y, 0])
    return g


def model_tag():
    t = T("classic rate model, a sketch", 22, GREY)
    t.move_to([6.25 - t.width / 2, KEY_Y, 0])
    return t


def dop_note():
    t = T("dopamine: + on D1 (direct), " + MINUS + " on D2 (indirect), in this model", 22, MOD)
    return t.move_to([0.9, -2.72, 0])


def strip(tokens, size=30):
    """tokens: list of (text, color). Returns a centred row, each token separate."""
    g = VGroup(*[M(t, size, c) for t, c in tokens]).arrange(RIGHT, buff=0.22)
    fit(g, max_w=12.0)
    return g.move_to([0, STRIP_Y, 0])


def product_tokens(keys):
    toks = []
    for i, k in enumerate(keys):
        if i:
            toks.append(("×", TEXT))
        s = SIGN[k]
        toks.append((("+1" if s > 0 else MINUS + "1"), EXC if s > 0 else INH))
    res = int(np.prod([SIGN[k] for k in keys]))
    toks += [("=", TEXT), (("+1" if res > 0 else MINUS + "1"), EXC if res > 0 else INH)]
    return toks


class Base(SpokenScene):
    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def times(self, n, start_phrase, end_phrase, s_nth=0, e_nth=0, pad_s=0.0, pad_e=0.3):
        a = self.t_of(start_phrase, s_nth) + pad_s
        b = self.t_of(end_phrase, e_nth) - pad_e
        return [a + (b - a) * i / n for i in range(n)]


# -------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Descending Control and the Basal Ganglia"
    TITLE = "Counting Signs Around the Brake"


# -------------------------------------------------------------------------------------------------
class S01Brake(Base):
    def construct(self):
        d = Diag(links=[])
        key = T("The classic rate model. Brighter box = more active, in this sketch.", 24, GREY).move_to([0, STRIP_Y, 0])
        note = T("The basal ganglia do not project to the spinal cord.", 24, GREY).move_to([0, KEY_Y, 0])
        self.at("Deep nuclei")
        boxes = [d.node[n] for n in ("ctx", "str", "D1", "D2", "gpe", "stn", "gpi", "thal", "snc")]
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes], lag_ratio=0.05, run_time=0.9),
                  FadeIn(key, run_time=0.9))
        self.at("never reach")
        faint = [d.link[k] for k in LINKS if k not in ("gpi_t", "t_c", "da1", "da2")]
        for l in faint:
            l.set_opacity(0.35)
        self.play(FadeIn(note, shift=UP * 0.1), *[FadeIn(l) for l in faint], run_time=0.8)
        self.at("Their output neurons")
        self.play(d.node["gpi"][0].animate.set_stroke(HI, width=6).set_fill(opacity=HIGH),
                  d.node["gpi"][1].animate.set_color(TEXT), run_time=0.6)
        d.lv["gpi"] = HIGH
        self.at("fire steadily")
        d.link["gpi_t"].set_opacity(1)
        d.link["t_c"].set_opacity(1)
        ph = [0.0]
        p0, q0 = edge("gpi", "thal"), edge("thal", "gpi")
        dd = VGroup(*[Dot(p0, radius=0.075, color=HI) for _ in range(4)])

        def adv(m, dt):
            ph[0] += dt * 0.55
            for i, dot in enumerate(m):
                dot.move_to(p0 + (q0 - p0) * ((ph[0] + i / 4) % 1.0))
        adv(dd, 0)
        dd.add_updater(adv)
        self.add(dd)
        self.play(FadeIn(d.link["gpi_t"]), d.node["thal"][0].animate.set_fill(opacity=LOW), run_time=1.0)
        d.lv["thal"] = LOW
        self.at("hold the thalamus")
        self.at("foot resting")
        brake = chip("brake", INH, size=26).move_to([3.4, 1.4, 0])
        self.play(FadeIn(brake, shift=RIGHT * 0.2), run_time=0.6)
        self.at("needs")
        dd.remove_updater(adv)
        self.play(FadeOut(dd), FadeOut(brake),
                  d.node["gpi"][0].animate.set_fill(opacity=LOW).set_stroke(POP, width=3),
                  d.node["thal"][0].animate.set_fill(opacity=HIGH),
                  FadeIn(d.link["t_c"]), run_time=1.4)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S02Direct(Base):
    def construct(self):
        d = Diag(links=list(LINKS.keys() - {"da1", "da2"}), op=DIM)
        leg, tag = legend(), model_tag()
        self.add(*d.node.values(), *d.link.values(), *d.lab.values(), leg, tag)
        self.at("roots")
        self.play(*[d.link[k].animate.set_opacity(0.5) for k in d.shown], run_time=0.6)
        self.at("direct pathway")
        self.play(*d.only(["s_gpi"], 0.5), d.node["D1"][0].animate.set_stroke(HI, width=5), run_time=0.6)
        self.at("inhibit")
        self.play(Indicate(d.link["s_gpi"], color=INH, scale_factor=1.0), run_time=0.8)
        self.at("Give each excitatory")
        self.play(Indicate(leg[0], color=EXC), run_time=0.9)
        self.at("each inhibitory")
        self.play(Indicate(leg[1], color=INH), run_time=0.9)
        self.at("Then multiply")
        toks = product_tokens(DIRECT)
        row = strip(toks)
        tt = self.times(4, "multiply", "The product", pad_s=0.5, pad_e=0.55)
        self.play(*d.only(DIRECT, 0.2), d.node["D1"][0].animate.set_stroke(POP, width=3), run_time=0.5)
        shown = 0
        for i, k in enumerate(DIRECT):
            self.until(tt[i])
            parts = [row[2 * i]] + ([row[2 * i - 1]] if i else [])
            self.play(*[FadeIn(p, shift=UP * 0.1) for p in parts], d.lab[k].animate.set_opacity(1),
                      Indicate(d.link[k], color=KCOL[LINKS[k][2]], scale_factor=1.0), run_time=0.5)
        self.at("The product")
        self.play(FadeIn(row[-2]), FadeIn(row[-1], scale=1.3), run_time=0.7)
        self.at("Two inhibitions")
        verdict = T("brake lifted: cortical drive up", 26, EXC).move_to([1.5, 1.3, 0])
        self.play(d.level("D1", HIGH), d.level("gpi", LOW), d.level("thal", HIGH),
                  FadeIn(verdict), run_time=1.6)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S03Indirect(Base):
    def construct(self):
        d = Diag(links=list(LINKS.keys() - {"da1", "da2"}), op=0.5)
        leg, tag = legend(), model_tag()
        self.add(*d.node.values(), *d.link.values(), *d.lab.values(), leg, tag)
        self.at("The indirect")
        self.play(*d.only(["s_gpe", "gpe_stn", "stn_gpi"], 0.5), run_time=0.5)
        self.at("receptors inhibit")
        self.play(d.node["D2"][0].animate.set_stroke(HI, width=5), Indicate(d.link["s_gpe"], color=INH,
                  scale_factor=1.0), run_time=0.8)
        self.at("inhibits the")
        self.play(Indicate(d.link["gpe_stn"], color=INH, scale_factor=1.0), d.node["stn"][0].animate.set_stroke(HI, width=5),
                  run_time=0.8)
        self.at("excites")
        self.play(Indicate(d.link["stn_gpi"], color=EXC, scale_factor=1.0), run_time=0.8)
        self.at("Multiply again")
        toks = product_tokens(INDIRECT)
        row = strip(toks)
        tt = self.times(6, "again", "The product", pad_s=0.4, pad_e=0.4)
        self.play(*d.only(INDIRECT, 0.2), d.node["D2"][0].animate.set_stroke(POP, width=3),
                  d.node["stn"][0].animate.set_stroke(POP, width=3), run_time=0.5)
        for i, k in enumerate(INDIRECT):
            self.until(tt[i])
            parts = [row[2 * i]] + ([row[2 * i - 1]] if i else [])
            self.play(*[FadeIn(p, shift=UP * 0.1) for p in parts], d.lab[k].animate.set_opacity(1),
                      Indicate(d.link[k], color=KCOL[LINKS[k][2]], scale_factor=1.0), run_time=0.45)
        self.at("The product")
        self.play(FadeIn(row[-2]), FadeIn(row[-1], scale=1.3), run_time=0.7)
        self.at("ends up")
        verdict = T("brake pressed: cortical drive down", 26, INH).move_to([1.5, 1.3, 0])
        self.play(d.level("D2", HIGH), d.level("gpe", LOW), d.level("stn", HIGH), d.level("gpi", HIGH),
                  d.level("thal", LOW), FadeIn(verdict), run_time=1.8)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S04Dopamine(Base):
    def construct(self):
        d = Diag(links=list(LINKS.keys()), op=0.5)
        leg, tag = legend(), model_tag()
        for k in ("da1", "da2"):
            d.link[k].set_opacity(0)
        self.add(*d.node.values(), *d.link.values(), *d.lab.values(), leg, tag)
        dop = T("dopamine", 22, MOD).move_to(P("snc") + DOWN * 0.7)
        s1 = M("+", 48, EXC, weight=BOLD).move_to([-5.3, -0.35, 0])
        s2 = M(MINUS, 48, INH, weight=BOLD).move_to([-4.0, -1.4, 0])
        self.at("Now add dopamine")
        self.play(d.node["snc"][0].animate.set_stroke(HI, width=5).set_fill(opacity=HIGH), FadeIn(dop), run_time=0.8)
        self.at("In the classic")
        self.play(d.link["da1"].animate.set_opacity(1), d.link["da2"].animate.set_opacity(1), d.node["snc"][0].animate.set_stroke(MOD, width=3),
                  run_time=0.9)
        self.at("excites the")
        note = dop_note()
        self.play(FadeIn(note), FadeIn(s1, scale=1.4), d.level("D1", HIGH), Indicate(d.link["da1"], color=EXC, scale_factor=1.0),
                  run_time=0.9)
        self.at("inhibits the")
        self.play(FadeIn(s2, scale=1.4), d.level("D2", LOW), Indicate(d.link["da2"], color=INH, scale_factor=1.0),
                  run_time=0.9)
        self.at("Exciting a")
        r1 = strip([("excite a", TEXT), ("+1", EXC), ("route:", TEXT), ("drive up", EXC)], 30)
        self.play(*d.only(DIRECT, 0.2), FadeIn(r1, shift=UP * 0.1), run_time=0.7)
        self.at("Inhibiting a")
        r2 = strip([("inhibit a", TEXT), (MINUS + "1", INH), ("route:", TEXT), ("drive up", EXC)], 30)
        self.play(*d.only(INDIRECT, 0.2), FadeOut(r1), FadeIn(r2, shift=UP * 0.1), run_time=0.7)
        self.at("Both actions")
        r3 = strip([("both push toward movement", EXC)], 32)
        self.play(*d.only(DIRECT + INDIRECT, 0.8), FadeOut(r2), FadeIn(r3, shift=UP * 0.1), run_time=0.8)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S05Loss(Base):
    def construct(self):
        d = Diag(links=list(LINKS.keys()), op=0.5, lv={"D1": HIGH, "D2": LOW})
        leg, tag = legend(), model_tag()
        s1 = M("+", 48, EXC, weight=BOLD).move_to([-5.3, -0.35, 0])
        s2 = M(MINUS, 48, INH, weight=BOLD).move_to([-4.0, -1.4, 0])
        dop = T("dopamine", 22, MOD).move_to(P("snc") + DOWN * 0.7)
        d.node["snc"][0].set_fill(opacity=MID)
        d.link["da1"].set_opacity(1); d.link["da2"].set_opacity(1)
        note = dop_note()
        self.add(*d.node.values(), *d.link.values(), *d.lab.values(), leg, tag, s1, s2, dop, note)
        self.at("losing dopamine")
        gone = T("dopamine lost", 22, RED).move_to(P("snc") + DOWN * 0.7)
        self.play(FadeOut(d.link["da1"]), FadeOut(d.link["da2"]), FadeOut(s1), FadeOut(s2), FadeOut(dop),
                  FadeOut(note), run_time=0.5)
        self.play(FadeIn(gone), d.level("snc", LOW), d.node["snc"][0].animate.set_stroke(RED, width=3), run_time=0.6)
        self.at("direct route weakens")
        self.play(d.level("D1", LOW), run_time=0.8)
        self.at("indirect route strengthens")
        self.play(d.level("D2", HIGH), run_time=0.8)
        self.at("more inhibited")
        self.play(d.level("gpe", LOW), run_time=0.8)
        self.at("is released")
        self.play(d.level("stn", HIGH), run_time=0.8)
        self.at("fires more")
        self.play(d.level("gpi", HIGH), run_time=0.8)
        self.at("held down")
        self.play(d.level("thal", LOW), run_time=0.9)
        self.at("The model predicts")
        r = strip([("model prediction: akinesia", RED)], 32)
        self.play(FadeIn(r, shift=UP * 0.1), run_time=0.8)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S06Limits(Base):
    def construct(self):
        d = Diag(links=list(LINKS.keys() - {"da1", "da2"}), op=0.5)
        leg, tag = legend(), model_tag()
        self.add(*d.node.values(), *d.link.values(), *d.lab.values(), leg, tag)
        self.at("a way to reason")
        r1 = strip([("a way to reason about the direction of a change", TEXT)], 28)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.8)
        self.at("not a measured law")
        r2 = strip([("not a measured law of how firing rates add", GOLD)], 28)
        self.play(FadeOut(r1), FadeIn(r2, shift=UP * 0.1), run_time=0.7)
        self.at("In mice")
        n1 = chip("in mice: both rise at action start", YELLOW, size=22).move_to([1.5, 1.3, 0])
        self.play(FadeIn(n1, shift=DOWN * 0.1), d.level("D1", HIGH), d.level("D2", HIGH), run_time=1.2)
        self.at("rest tremor")
        n2 = chip("rest tremor: no account", RED, size=22).move_to([1.5, -0.65, 0])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.8)
        self.at("Keep the rule")
        r3 = strip([("multiply the signs to predict direction. It is a model.", TEXT)], 28)
        self.play(FadeOut(r2), FadeOut(n1), FadeOut(n2), FadeIn(r3, shift=UP * 0.1),
                  d.level("D1", MID), d.level("D2", MID), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Multiply the signs to predict direction; remember it is a model."
