"""Paying to Go Uphill (crossing-the-membrane, film 2)  (Biochemistrypedia explainer, high school Biology)

Same world and COLOUR MAP as film 1 (../scenes.py, whose helpers are reused so the look is identical):
  WATER = BLUE dots   SODIUM Na+ = ORANGE   POTASSIUM K+ = PURPLE   DYE = RED   ATP = YELLOW token
  MEMBRANE = grey heads, pale cream tails, one vertical membrane at x = 0   PROTEINS = TEAL blocks
THE WORLD: OUTSIDE the cell on the left, INSIDE on the right. Teal leak channels at y = +-1.85, the
sodium-potassium pump at y = 0. Meter panel (schematic) top left, counter box top right.
"""
import importlib.util
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

def _load_film1():
    here = Path(globals().get("__file__", "")).resolve().parent if globals().get("__file__") else None
    cands = []
    if here:
        cands.append(here.parent / "scenes.py")
    if os.environ.get("KX_SCRIPT"):
        cands.append(Path(os.environ["KX_SCRIPT"]).resolve().parent.parent / "scenes.py")
    for p in cands:
        if p.exists():
            spec = importlib.util.spec_from_file_location("film1_scenes", str(p))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise RuntimeError("film 1 scenes.py not found")


F1 = _load_film1()
NA, WATER, DYE, TAILC, HEAD, PROT, ATP = F1.NA, F1.WATER, F1.DYE, F1.TAILC, F1.HEAD, F1.PROT, F1.ATP
lab, P3, Swarm, token, arr, make_membrane, ROWS = F1.lab, F1.P3, F1.Swarm, F1.token, F1.arr, F1.make_membrane, F1.ROWS
tanks = F1.tanks


_lab_raw = lab


def lab(*a, **k):  # framecheck: labels draw above drifting ions
    m = _lab_raw(*a, **k)
    m.set_z_index(20)
    return m

KC = "#B388EB"   # potassium, purple

LBOX = (-6.3, -0.95, -3.2, 1.7)
RBOX = (0.95, 6.3, -3.2, 1.7)
YNA, YK = 1.85, -1.85
SLAB_W, SLAB_H = 1.25, 0.3
STEADY = dict(nao=2.8, nai=0.5, kio=2.8, koi=0.5)


# ------------------------------------------------------------------ membrane with slots
def membrane(slots=("na", "k", "pump")):
    mem = make_membrane()
    ycs = {"na": (YNA, 0.6), "k": (YK, 0.6), "pump": (0.0, 1.0)}
    for y in list(mem.rows):
        if y > 2.6:
            mem.remove(mem.rows[y])
            del mem.rows[y]
    mem.slot_rows = {}
    for s, (yc, hh) in ycs.items():
        mem.slot_rows[s] = [mem.rows[y] for y in mem.rows if abs(y - yc) < hh]
        if s in slots:
            for g in mem.slot_rows[s]:
                mem.remove(g)
    return mem


def slab(yc):
    g = VGroup()
    for dy in (0.5, -0.5):
        g.add(RoundedRectangle(corner_radius=0.1, width=SLAB_W, height=SLAB_H, stroke_color=PROT, stroke_width=4,
                               fill_color=PROT, fill_opacity=0.6).move_to(P3(0, yc + dy)))
    return g


class Pump(VGroup):
    def __init__(self, side=1):
        self.block = RoundedRectangle(corner_radius=0.18, width=1.7, height=1.9, stroke_color=PROT, stroke_width=4,
                                      fill_color=PROT, fill_opacity=0.6).move_to(P3(0, 0))
        self.pocket = Rectangle(width=0.6, height=1.1, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(P3(0.55 * side, 0))
        super().__init__(self.block, self.pocket)
        self.side = side


# ------------------------------------------------------------------ flow through a leak channel
class Flow(VGroup):
    def __init__(self, color, y, direction, n=4, x0=-2.7, x1=2.7, v=1.2, r=0.13, seed=0, on=True):
        super().__init__()
        self.d, self.x0, self.x1, self.v, self.t, self.y, self.on = direction, x0, x1, v, 0.0, y, on
        rng = np.random.RandomState(seed)
        span = x1 - x0
        self.pos = [x0 + span * (i / n) for i in range(n)]
        self.ph = [rng.uniform(0, 6) for _ in range(n)]
        self.speed = ValueTracker(1.0 if on else 0.0)
        for x in self.pos:
            self.add(Dot(P3(x, y), radius=r, color=color))
        self.add_updater(self._step)

    def _step(self, _, dt):
        if dt <= 0:
            return
        self.t += dt
        sp = self.speed.get_value()
        span = self.x1 - self.x0
        for i, d in enumerate(self.submobjects):
            self.pos[i] = (self.pos[i] - self.x0 + self.d * self.v * sp * dt) % span + self.x0
            x = self.pos[i]
            fade = min(1.0, (x - self.x0) / 0.7, (self.x1 - x) / 0.7) * min(1.0, sp * 3)
            d.move_to(P3(x, self.y + 0.07 * np.sin(2.3 * self.t + self.ph[i])))
            d.set_fill(opacity=max(fade, 0))


# ------------------------------------------------------------------ meters (schematic) and tally
class Meters(VGroup):
    X0, W = -4.7, 2.7
    ROWS_Y = dict(nao=3.55, nai=3.17, koi=2.79, kio=2.41)

    def __init__(self, vals=None):
        super().__init__()
        v = dict(STEADY) if vals is None else dict(vals)
        self.tr = {k: ValueTracker(x) for k, x in v.items()}
        self.rate, self.goal = {}, {}
        self.na_g, self.k_g = VGroup(), VGroup()
        self.bars = {}
        for key, col, grp in (("nao", NA, self.na_g), ("nai", NA, self.na_g), ("koi", KC, self.k_g), ("kio", KC, self.k_g)):
            y = self.ROWS_Y[key]
            tag = T("out" if key in ("nao", "koi") else "in", 22, TEXT).move_to(P3(-5.35, y))
            bar = Rectangle(width=1, height=0.26, stroke_width=0, fill_color=col, fill_opacity=0.95)
            bar.set_z_index(3)
            self.bars[key] = bar
            bar.add_updater(self._mk(key))
            self._mk(key)(bar)
            grp.add(tag, bar)
        self.na_g.add(lab("Na+", 30, NA, weight=BOLD).move_to(P3(-6.2, 3.36)))
        self.k_g.add(lab("K+", 30, KC, weight=BOLD).move_to(P3(-6.2, 2.6)))
        self.note = T("meters: schematic", 22, TEXT).move_to(P3(-4.2, 2.03))
        self.add(self.na_g, self.k_g, self.note)
        self.add_updater(self._drift)

    def _mk(self, key):
        def f(b):
            w = max(self.tr[key].get_value(), 0.02) * (self.W / 2.8)
            b.stretch_to_fit_width(w)
            b.move_to(P3(self.X0 + w / 2, self.ROWS_Y[key]))
        return f

    def drift(self, dur, **goals):
        for k, g in goals.items():
            self.goal[k] = g
            self.rate[k] = (g - self.tr[k].get_value()) / dur

    def _drift(self, _, dt):
        for k in list(self.goal):
            cur = self.tr[k].get_value()
            nxt = cur + self.rate[k] * dt
            if (self.rate[k] > 0 and nxt >= self.goal[k]) or (self.rate[k] <= 0 and nxt <= self.goal[k]):
                nxt = self.goal[k]
                del self.goal[k]
            self.tr[k].set_value(nxt)


class Tally(VGroup):
    def __init__(self, a=0, n=0, k=0):
        box = RoundedRectangle(corner_radius=0.12, width=4.5, height=1.55, stroke_color=GREY, stroke_width=3,
                               fill_color=BG, fill_opacity=0.95).move_to(P3(4.15, 3.0))
        super().__init__(box)
        self.vals = dict(a=a, n=n, k=k)
        self.nums = {}
        spec = (("a", "ATP spent", ATP, 3.45), ("n", "Na+ out", NA, 3.0), ("k", "K+ in", KC, 2.55))
        for key, name, col, y in spec:
            self.add(T(name, 26, col).move_to(P3(2.5, y), aligned_edge=LEFT).align_to(P3(2.1, y), LEFT))
            self.nums[key] = (None, y, col)
        self._shown = {}
        self.add_updater(lambda m, dt: self._upd())
        self._upd()

    def _upd(self):
        for key, (cur, y, col) in list(self.nums.items()):
            v = self.vals[key]
            if self._shown.get(key) != v:
                self._shown[key] = v
                new = M(str(v), 28, col).set_stroke(BG, 4, background=True)
                new.move_to(P3(6.0, y), aligned_edge=RIGHT).align_to(P3(6.1, y), RIGHT)
                if cur is not None:
                    self.remove(cur)
                self.add(new)
                self.nums[key] = (new, y, col)

    def add_to(self, key, d):
        self.vals[key] += d


def zones():
    g = VGroup()
    for x0, x1 in ((-6.8, -0.72), (0.72, 6.8)):
        g.add(Rectangle(width=x1 - x0, height=7.6, stroke_width=0, fill_color=WATER, fill_opacity=0.16)
              .move_to(P3((x0 + x1) / 2, 0)))
    g.set_z_index(-5)
    return g


# ------------------------------------------------------------------ the world
class World:
    pass


def build_world(sc, slots=("na", "k", "pump"), swarms=True, meters=False, flows=True, pump_side=1, tally=None, labels=True,
                dim=1.0, mvals=None):
    W = World()
    W.zones = zones()
    sc.add(W.zones)
    W.mem = membrane(slots)
    sc.add(W.mem)
    W.slabs = {}
    for s, yc in (("na", YNA), ("k", YK)):
        if s in slots:
            W.slabs[s] = slab(yc)
            sc.add(W.slabs[s])
    W.pump = None
    if "pump" in slots:
        W.pump = Pump(pump_side)
        sc.add(W.pump)
    W.sw = []
    if swarms:
        W.naL = Swarm(NA, 13, LBOX, sig=1.5, r=0.13, seed=11)
        W.naR = Swarm(NA, 3, RBOX, sig=1.5, r=0.13, seed=12)
        W.kR = Swarm(KC, 13, RBOX, sig=1.5, r=0.13, seed=13)
        W.kL = Swarm(KC, 3, LBOX, sig=1.5, r=0.13, seed=14)
        W.sw = [W.naL, W.naR, W.kR, W.kL]
        for s in W.sw:
            s.op.set_value(dim)
        sc.add(*W.sw)
    W.flows = []
    if flows:
        fa = Flow(NA, YNA, +1, n=4, seed=1)
        fk = Flow(KC, YK, -1, n=4, seed=2)
        W.flows = [fa, fk]
        sc.add(*W.flows)
    W.labels = None
    if labels:
        W.labels = VGroup(lab("OUTSIDE", 30, TEXT, weight=BOLD).move_to(P3(-3.6, -3.55)),
                          lab("INSIDE", 30, TEXT, weight=BOLD).move_to(P3(3.6, -3.55)))
        sc.add(W.labels)
    W.met = None
    if meters:
        W.met = Meters(mvals)
        sc.add(W.met)
    W.tally = None
    if tally is not None:
        W.tally = Tally(*tally)
        sc.add(W.tally)
    return W


def dim_to(W, v, rt=0.5):
    return [s.op.animate.set_value(v).set_run_time(rt) for s in W.sw]


# ------------------------------------------------------------------ one pump cycle
def pump_cycle(sc, W, sp=1.0, token_from=(3.0, -1.9)):
    pump, tally = W.pump, W.tally
    slotsy = (0.3, 0.0, -0.3)
    na = VGroup(*[Dot(P3(2.5 + 0.2 * (i % 2), y * 2.2), radius=0.13, color=NA) for i, y in enumerate(slotsy)])
    na.set_z_index(12)
    tk = token(0.28).move_to(P3(*token_from))
    tk.set_z_index(12)
    na.set_opacity(0)
    sc.add(na)
    sc.play(na.animate.set_opacity(1), FadeIn(tk), run_time=0.15 * sp)
    sc.play(*[d.animate.move_to(P3(0.55, y)) for d, y in zip(na, slotsy)], tk.animate.move_to(P3(1.05, -0.8)),
            run_time=0.5 * sp)
    sc.play(tk.animate.scale(1.8).set_opacity(0), pump.block.animate.set_stroke(ATP, 6), run_time=0.25 * sp)
    sc.remove(tk)
    if tally:
        tally.add_to("a", 1)
    sc.play(pump.pocket.animate.shift(LEFT * 1.1), na.animate.shift(LEFT * 1.1), run_time=0.5 * sp)
    sc.play(na.animate.shift(LEFT * 1.0).set_opacity(0), run_time=0.4 * sp)
    sc.remove(na)
    if tally:
        tally.add_to("n", 3)
    k = VGroup(*[Dot(P3(-2.5, y), radius=0.13, color=KC) for y in (0.5, -0.5)])
    k.set_z_index(12)
    k.set_opacity(0)
    sc.add(k)
    sc.play(k.animate.set_opacity(1), run_time=0.1 * sp)
    sc.play(*[d.animate.move_to(P3(-0.55, y)) for d, y in zip(k, (0.2, -0.2))], run_time=0.4 * sp)
    sc.play(pump.pocket.animate.shift(RIGHT * 1.1), k.animate.shift(RIGHT * 1.1),
            pump.block.animate.set_stroke(PROT, 4), run_time=0.5 * sp)
    sc.play(k.animate.shift(RIGHT * 1.0).set_opacity(0), run_time=0.4 * sp)
    sc.remove(k)
    if tally:
        tally.add_to("k", 2)


def bin_with_tokens(n=4, center=(4.6, -1.8)):
    box = RoundedRectangle(corner_radius=0.15, width=2.6, height=1.3, stroke_color=ATP, stroke_width=4,
                           fill_color=BG, fill_opacity=0.85).move_to(P3(*center))
    toks = VGroup(*[token(0.26) for _ in range(n)])
    toks.arrange(RIGHT, buff=0.12).move_to(box)
    g = VGroup(box, toks)
    g.box, g.toks = box, toks
    g.set_z_index(10)
    return g


def hill_ramp(x0, y0, x1, y1, color=GREY):
    return Line(P3(x0, y0), P3(x1, y1), color=color, stroke_width=8)


# ======================================================================================================
class S00Title(TitleCard):
    LESSON = "Crossing the Membrane"
    TITLE = "Paying to Go Uphill"


# ------------------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        lL, lR = ValueTracker(1.3), ValueTracker(1.3)
        frame = RoundedRectangle(corner_radius=0.2, width=8.4, height=4.4, stroke_color=GREY, stroke_width=4,
                                 fill_color=BG, fill_opacity=1).move_to(P3(0, 0.9))
        tk = VGroup()
        ups = []
        for x0, x1, tr in ((-3.6, -0.25, lL), (0.25, 3.6, lR)):
            out = VMobject(stroke_color=GREY, stroke_width=5)
            out.set_points_as_corners([P3(x0, 2.7), P3(x0, -0.8), P3(x1, -0.8), P3(x1, 2.7)])
            fl = Rectangle(width=x1 - x0, height=1, stroke_width=0, fill_color=WATER, fill_opacity=0.25)
            sf = Line(P3(x0, 0), P3(x1, 0), color=WATER, stroke_width=4)
            g = VGroup(fl, sf)

            def u(m, x0=x0, x1=x1, tr=tr, fl=fl, sf=sf):
                lv = tr.get_value()
                fl.become(Rectangle(width=x1 - x0, height=lv + 0.8, stroke_width=0, fill_color=WATER, fill_opacity=0.25)
                          .move_to(P3((x0 + x1) / 2, -0.8 + (lv + 0.8) / 2)))
                sf.put_start_and_end_on(P3(x0, lv), P3(x1, lv))
            g.add_updater(u)
            u(g)
            ups.append(g)
            tk.add(g, out)
        thumb = VGroup(frame, tk)
        line = VGroup(lab("Whatever can cross runs downhill for free;", 32, TEXT),
                      lab("water runs toward trapped solute.", 32, WATER)).arrange(DOWN, buff=0.15).move_to(P3(0, -2.35))
        self.play(FadeIn(thumb), run_time=0.8)
        self.at("whatever could cross")
        self.play(FadeIn(line, shift=UP * 0.1), run_time=0.6)
        self.at("ran downhill")
        self.play(lL.animate.set_value(2.1), lR.animate.set_value(0.3), run_time=1.8)
        self.at("so how does a cell keep")
        for g in ups:
            g.clear_updaters()
        zn = zones()
        self.add(zn)
        mem = membrane(slots=())
        self.play(thumb.animate.scale(0.15).move_to(P3(-6.2, 3.3)).set_opacity(0), FadeOut(line),
                  LaggedStart(*[FadeIn(g) for g in mem], lag_ratio=0.03, run_time=1.0), run_time=1.0)
        self.add(mem)
        outl = lab("OUTSIDE", 30, TEXT, weight=BOLD).move_to(P3(-3.6, -3.55))
        inl = lab("INSIDE", 30, TEXT, weight=BOLD).move_to(P3(3.6, -3.55))
        self.play(FadeIn(outl), FadeIn(inl), run_time=0.4)
        naL = Swarm(NA, 13, LBOX, sig=1.5, r=0.13, seed=11)
        naL.op.set_value(0)
        self.add(naL)
        self.at("so much sodium outside")
        q1 = lab("?", 90, NA, weight=BOLD).move_to(P3(-3.4, 2.7))
        self.play(naL.op.animate.set_value(1), GrowFromCenter(q1), run_time=0.9)
        kR = Swarm(KC, 13, RBOX, sig=1.5, r=0.13, seed=13)
        kR.op.set_value(0)
        self.add(kR)
        self.at("so much potassium")
        q2 = lab("?", 90, KC, weight=BOLD).move_to(P3(3.4, 2.7))
        self.play(kR.op.animate.set_value(1), GrowFromCenter(q2), run_time=0.9)
        self.play(q1.animate.scale(1.12), q2.animate.scale(1.12), run_time=0.5)
        self.play(q1.animate.scale(1 / 1.12), q2.animate.scale(1 / 1.12), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S02Meters(SpokenScene):
    def construct(self):
        mem = membrane(slots=())
        outl = lab("OUTSIDE", 30, TEXT, weight=BOLD).move_to(P3(-3.6, -3.55))
        inl = lab("INSIDE", 30, TEXT, weight=BOLD).move_to(P3(3.6, -3.55))
        self.add(zones(), mem, outl, inl)
        naL = Swarm(NA, 13, LBOX, sig=1.5, r=0.13, seed=11)
        naR = Swarm(NA, 3, RBOX, sig=1.5, r=0.13, seed=12)
        kR = Swarm(KC, 13, RBOX, sig=1.5, r=0.13, seed=13)
        kL = Swarm(KC, 3, LBOX, sig=1.5, r=0.13, seed=14)
        for s in (naL, naR, kR, kL):
            s.op.set_value(0)
        self.add(naL, naR, kR, kL)
        met = Meters(vals=dict(nao=0.0, nai=0.0, kio=0.0, koi=0.0))
        met.na_g.set_opacity(0)
        met.k_g.set_opacity(0)
        met.note.set_opacity(0)
        self.add(met)
        self.play(Indicate(mem, color=TEXT, scale_factor=1.03), run_time=1.4)
        self.at("sodium shown in orange")
        self.play(naL.op.animate.set_value(1), naR.op.animate.set_value(1), run_time=0.9)
        met.na_g.set_opacity(1)
        met.note.set_opacity(1)
        self.at("much higher outside")
        self.play(met.tr["nao"].animate.set_value(2.8), met.tr["nai"].animate.set_value(0.5), run_time=1.6)
        self.at("potassium shown in purple")
        self.play(kR.op.animate.set_value(1), kL.op.animate.set_value(1), run_time=0.9)
        met.k_g.set_opacity(1)
        self.at("much higher inside")
        self.play(met.tr["kio"].animate.set_value(2.8), met.tr["koi"].animate.set_value(0.5), run_time=1.6)
        self.at("each ion sits at the top")
        self.play(Indicate(met.bars["nao"], color=NA), Indicate(met.bars["kio"], color=KC), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S03Leaks(SpokenScene):
    def construct(self):
        W = build_world(self, slots=(), meters=True, flows=False)
        W.pump = None
        self.wait(0.6)
        self.at("channels in the membrane leak")
        s_na, s_k = slab(YNA), slab(YK)
        self.play(*[FadeOut(g) for g in W.mem.slot_rows["na"] + W.mem.slot_rows["k"]],
                  FadeIn(s_na), FadeIn(s_k), run_time=1.2)
        self.at("sodium trickles in")
        fa = Flow(NA, YNA, +1, n=4, seed=1, on=False)
        self.add(fa)
        fa.speed.set_value(0.0)
        self.play(fa.speed.animate.set_value(1.0), run_time=1.0)
        arrow = arr(P3(-2.4, 2.65), P3(-1.2, 2.65), NA, 8)
        self.at("potassium trickles out")
        fk = Flow(KC, YK, -1, n=4, seed=2, on=False)
        self.add(fk)
        fk.speed.set_value(0.0)
        self.play(fk.speed.animate.set_value(1.0), run_time=1.0)
        self.at("each ion runs downhill")
        d1 = arr(P3(-2.2, 1.85 + 0.0), P3(-1.2, 1.85), NA, 9)
        self.play(Indicate(s_na, color=NA), Indicate(s_k, color=KC), run_time=1.2)
        self.at("the two differences")
        W.met.drift(3.0, nao=2.2, nai=1.1, kio=2.2, koi=1.1)
        self.wait(1.4)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S04ChannelVsPump(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k"), meters=False, dim=0.5)
        W.pump = None
        pump = Pump(1)
        self.at("a leak channel is an open tunnel")
        self.play(Indicate(W.slabs["na"], color=PROT, scale_factor=1.15), run_time=1.2)
        self.at("pass through it only downhill")
        cl = lab("channel: downhill only", 34, PROT, weight=BOLD).move_to(P3(-3.7, 0.7))
        d1 = arr(P3(-2.2, 1.85), P3(-1.1, 1.85), NA, 9)
        self.play(FadeIn(cl), GrowArrow(d1), run_time=0.8)
        self.at("for ions the hill also depends")
        v1 = lab("membrane voltage", 34, GOLD, weight=BOLD).move_to(P3(3.7, 1.0))
        self.play(FadeIn(v1, shift=UP * 0.1), run_time=0.7)
        self.at("biology 2 covers")
        v2 = lab("covered in Biology 2", 30, GOLD).move_to(P3(3.7, 0.4))
        self.play(FadeIn(v2), run_time=0.6)
        self.at("a pump is different")
        self.play(FadeOut(v1), FadeOut(v2), FadeOut(d1), cl.animate.set_opacity(0.0), run_time=0.6)
        self.remove(cl)
        self.play(*[FadeOut(g) for g in W.mem.slot_rows["pump"]], GrowFromCenter(pump), run_time=1.1)
        pl = VGroup(lab("pump:", 32, PROT, weight=BOLD), lab("grabs, changes shape,", 32, PROT, weight=BOLD),
                    lab("spends energy", 32, PROT, weight=BOLD)).arrange(DOWN, buff=0.12).move_to(P3(4.0, 0.0))
        pl2 = VGroup()
        self.at("it grabs ions")
        ion = VGroup(*[Dot(P3(2.4, y), radius=0.13, color=NA) for y in (0.5, 0.0)]).set_z_index(12)
        self.add(ion)
        self.play(FadeIn(pl), FadeIn(pl2), run_time=0.5)
        self.play(*[d.animate.move_to(P3(0.55, y)) for d, y in zip(ion, (0.2, -0.2))], run_time=0.7)
        self.at("changes shape")
        self.play(pump.pocket.animate.shift(LEFT * 1.1), ion.animate.shift(LEFT * 1.1), run_time=1.0)
        self.at("and spends energy")
        tk = token(0.3).move_to(P3(1.3, -1.0))
        self.play(FadeIn(tk), run_time=0.4)
        self.play(tk.animate.scale(1.8).set_opacity(0), pump.block.animate.set_stroke(ATP, 6), run_time=0.5)
        self.remove(tk)
        self.at("carry them uphill")
        up = lab("uphill", 36, ATP, weight=BOLD).move_to(P3(-3.6, -0.5))
        self.play(ion.animate.shift(LEFT * 1.6), FadeIn(up), pump.block.animate.set_stroke(PROT, 4), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S05BindNa(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=False, dim=0.5, tally=(0, 0, 0))
        pump = W.pump
        self.at("watch one cycle")
        self.play(Indicate(pump, color=PROT, scale_factor=1.08), run_time=1.2)
        self.at("three sodium ions bind")
        nl = lab("3 Na+", 34, NA, weight=BOLD).move_to(P3(3.2, 0.0))
        self.play(FadeIn(nl), run_time=0.5)
        ys = (0.3, 0.0, -0.3)
        starts = [(2.6, 0.9), (3.0, -0.6), (2.2, -1.0)]
        dots = VGroup(*[Dot(P3(*s), radius=0.13, color=NA) for s in starts]).set_z_index(12)
        self.add(dots)
        for d, y in zip(dots, ys):
            self.play(d.animate.move_to(P3(0.55, y)), run_time=0.75)
        self.at("inside of the cell")
        self.play(Indicate(W.labels[1], color=TEXT, scale_factor=1.2), run_time=1.0)
        self.wait(0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S06Atp(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=False, dim=0.5, tally=(0, 0, 0))
        pump, tally = W.pump, W.tally
        ys = (0.3, 0.0, -0.3)
        dots = VGroup(*[Dot(P3(0.55, y), radius=0.13, color=NA) for y in ys]).set_z_index(12)
        nl = lab("3 Na+", 34, NA, weight=BOLD).move_to(P3(3.2, 0.0))
        self.add(dots, nl)
        tk = token(0.34).move_to(P3(3.4, -1.7)).set_z_index(12)
        self.play(FadeIn(tk), run_time=0.4)
        self.at("one ATP")
        self.play(tk.animate.move_to(P3(1.15, -0.85)), run_time=0.9)
        self.play(tk.animate.scale(1.8).set_opacity(0), pump.block.animate.set_stroke(ATP, 6), run_time=0.5)
        self.remove(tk)
        tally.add_to("a", 1)
        self.at("the molecule that carries")
        el = lab("ATP: usable energy", 32, ATP, weight=BOLD).move_to(P3(3.9, -0.95))
        self.play(FadeIn(el), run_time=0.6)
        self.play(Indicate(pump.block, color=ATP, scale_factor=1.05), run_time=1.6)
        self.at("the pump changes shape", lead=0.0)
        self.play(FadeOut(el), FadeOut(nl), run_time=0.4)
        self.play(pump.pocket.animate.shift(LEFT * 1.1), dots.animate.shift(LEFT * 1.1), run_time=1.3)
        self.at("releases the three sodium")
        self.play(dots.animate.shift(LEFT * 1.3), run_time=1.0)
        self.play(dots.animate.shift(LEFT * 0.5).set_opacity(0), pump.block.animate.set_stroke(PROT, 4), run_time=0.8)
        tally.add_to("n", 3)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S07K(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=False, dim=0.5, tally=(1, 3, 0), pump_side=-1)
        pump, tally = W.pump, W.tally
        self.wait(0.5)
        self.at("two potassium ions bind")
        kl = lab("2 K+", 34, KC, weight=BOLD).move_to(P3(-3.2, 0.0))
        self.play(FadeIn(kl), run_time=0.5)
        k = VGroup(*[Dot(P3(*s), radius=0.13, color=KC) for s in ((-2.6, 0.8), (-2.4, -0.8))]).set_z_index(12)
        self.add(k)
        for d, y in zip(k, (0.2, -0.2)):
            self.play(d.animate.move_to(P3(-0.55, y)), run_time=0.9)
        self.at("changes shape again")
        self.play(FadeOut(kl), run_time=0.3)
        self.play(pump.pocket.animate.shift(RIGHT * 1.1), k.animate.shift(RIGHT * 1.1), run_time=1.3)
        self.at("carries them in")
        self.play(k.animate.shift(RIGHT * 1.6).set_opacity(0), run_time=1.4)
        tally.add_to("k", 2)
        self.at("both trips went uphill")
        r1 = hill_ramp(-5.3, -2.3, -2.4, -0.7)
        r2 = hill_ramp(2.4, -2.3, 5.3, -0.7)
        b1 = Dot(P3(-5.2, -2.1), radius=0.14, color=NA).set_z_index(12)
        b2 = Dot(P3(2.5, -2.1), radius=0.14, color=KC).set_z_index(12)
        u1 = lab("uphill", 34, ATP, weight=BOLD).move_to(P3(-3.6, -0.15))
        u2 = lab("uphill", 34, ATP, weight=BOLD).move_to(P3(3.6, -0.15))
        self.play(Create(r1), Create(r2), FadeIn(b1), FadeIn(b2), run_time=0.8)
        self.play(FadeIn(u1), FadeIn(u2), b1.animate.move_to(P3(-2.6, -0.95)), b2.animate.move_to(P3(5.1, -0.95)),
                  run_time=2.0)
        self.wait(0.4)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S08Steady(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.5, tally=(1, 3, 2))
        W.met.na_g.set_opacity(1)
        ratio = VGroup(lab("1 ATP", 24, ATP, weight=BOLD), lab(":", 24, TEXT, weight=BOLD),
                       lab("3 Na+ out", 24, NA, weight=BOLD), lab(":", 24, TEXT, weight=BOLD),
                       lab("2 K+ in", 24, KC, weight=BOLD)).arrange(RIGHT, buff=0.12).move_to(P3(4.2, 1.95))
        for m in ratio:
            m.set_opacity(0)
        self.add(ratio)
        tms = [self.t_of("1 ATP spent") - 0.2, self.t_of("3 sodium out") - 0.2, self.t_of("2 potassium in") - 0.2]
        parts = [[0], [1, 2], [3, 4]]
        state = {"i": 0}

        def reveal(_m):
            while state["i"] < 3 and self.elapsed() >= tms[state["i"]]:
                for j in parts[state["i"]]:
                    ratio[j].set_opacity(1)
                state["i"] += 1
        ratio.add_updater(reveal)
        pump_cycle(self, W, sp=0.75)
        pump_cycle(self, W, sp=0.7)
        pump_cycle(self, W, sp=0.7)
        self.at("the meters hold steady", lead=0.0)
        self.play(Indicate(W.met.na_g, color=NA, scale_factor=1.05), Indicate(W.met.k_g, color=KC, scale_factor=1.05), run_time=1.2)
        self.at("the leaks never close", lead=0.0)
        self.play(Indicate(W.slabs["na"], color=PROT), Indicate(W.slabs["k"], color=PROT), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S09Define(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.5, tally=(3, 9, 6))
        self.wait(0.3)
        gone = [m for m in (W.zones, W.mem, W.pump, W.labels, W.met, W.tally, *W.slabs.values(), *W.flows)]
        self.play(*[FadeOut(g) for g in gone], *dim_to(W, 0.0, 0.5), run_time=0.5)
        for s in W.sw:
            self.remove(s)
        div = Line(P3(0, -3.6), P3(0, 3.6), color=GREY, stroke_width=3)
        cardL = Rectangle(width=6.6, height=7.6, stroke_width=0, fill_color=ATP, fill_opacity=0.12).move_to(P3(-3.4, 0))
        cardR = Rectangle(width=6.6, height=7.6, stroke_width=0, fill_color=WATER, fill_opacity=0.16).move_to(P3(3.4, 0))
        cardL.set_z_index(-5)
        cardR.set_z_index(-5)
        self.add(cardL, cardR, div)
        # active column
        pump = Pump(1)
        pump.scale(1.5).move_to(P3(-3.8, 0.6))
        pump_tk = token(0.45).move_to(P3(-1.5, -0.35))
        self.play(FadeIn(pump), FadeIn(pump_tk), run_time=0.4)
        self.at("uses the cell's energy")
        l1 = lab("uses energy, often ATP", 32, ATP, weight=BOLD).move_to(P3(-3.4, -1.6))
        self.play(FadeIn(l1), run_time=0.6)
        self.at("is active transport")
        h1 = lab("ACTIVE TRANSPORT", 38, TEXT, weight=BOLD).move_to(P3(-3.4, 3.1))
        self.play(FadeIn(h1, shift=DOWN * 0.1), run_time=0.7)
        self.play(pump.pocket.animate.shift(LEFT * 1.65), run_time=1.0)
        self.at("against its gradient")
        l2 = lab("can go uphill", 32, TEXT, weight=BOLD).move_to(P3(-3.4, -2.2))
        up = arr(P3(-3.6, -0.9), P3(-3.6, 0.0), NA, 8)
        self.play(FadeIn(l2), run_time=0.6)
        self.play(pump.pocket.animate.shift(RIGHT * 1.65), run_time=1.0)
        # passive column
        self.at("diffusion and osmosis")
        sl = slab(0.6).scale(1.6).move_to(P3(3.6, 0.6))
        fd = Flow(DYE, 0.88, +1, n=3, x0=0.9, x1=6.3, v=1.1, r=0.16, seed=3)
        fw = Flow(WATER, 0.32, +1, n=4, x0=0.9, x1=6.3, v=1.4, r=0.12, seed=4)
        self.play(FadeIn(sl), run_time=0.4)
        self.add(fd, fw)
        dl = lab("dye", 34, DYE, weight=BOLD).move_to(P3(1.8, 2.0))
        wl = lab("water", 34, WATER, weight=BOLD).move_to(P3(5.2, 2.0))
        self.play(FadeIn(dl), FadeIn(wl), run_time=0.6)
        self.at("passive transport")
        h2 = lab("PASSIVE TRANSPORT", 38, TEXT, weight=BOLD).move_to(P3(3.5, 3.1))
        self.play(FadeIn(h2, shift=DOWN * 0.1), run_time=0.7)
        self.at("no energy from the cell")
        l3 = lab("no energy from the cell", 32, TEXT, weight=BOLD).move_to(P3(3.5, -1.5))
        l4 = lab("downhill", 32, WATER, weight=BOLD).move_to(P3(3.5, -2.2))
        self.play(FadeIn(l3), run_time=0.6)
        self.play(FadeIn(l4), run_time=0.6)
        self.wait(0.4)
        self.finish()


# ------------------------------------------------------------------------------------------------------
def predict_marks():
    q1 = lab("?", 64, NA, weight=BOLD).move_to(P3(-1.2, 3.36))
    q2 = lab("?", 64, KC, weight=BOLD).move_to(P3(-1.2, 2.6))
    return q1, q2


class S10Predict(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.55)
        W.met.na_g.set_opacity(1)
        bn = bin_with_tokens(4)
        self.add(bn)
        self.at("the cell runs out")
        for t in list(bn.toks):
            self.play(t.animate.set_opacity(0), run_time=0.45)
        nl = lab("ATP: none left", 32, ATP, weight=BOLD).move_to(P3(4.6, -0.65))
        self.play(FadeIn(nl), run_time=0.5)
        self.at("the leak channels stay open")
        self.play(Indicate(W.slabs["na"], color=PROT), Indicate(W.slabs["k"], color=PROT), run_time=1.4)
        q1, q2 = predict_marks()
        self.at("which way will sodium")
        self.play(GrowFromCenter(q1), Indicate(W.slabs["na"], color=NA, scale_factor=1.2), run_time=1.0)
        self.at("which way will potassium")
        self.play(GrowFromCenter(q2), Indicate(W.slabs["k"], color=KC, scale_factor=1.2), run_time=1.0)
        self.at("pause and predict")
        title = lab("Pause and predict", 40, GOLD, weight=BOLD).move_to(P3(3.9, 3.2))
        self.play(FadeIn(title), run_time=0.5)
        self.play(Indicate(title, color=GOLD, scale_factor=1.1), run_time=1.0)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.55)
        W.met.na_g.set_opacity(1)
        bn = bin_with_tokens(4)
        bn.toks.set_opacity(0)
        self.add(bn)
        nl = lab("ATP: none left", 32, ATP, weight=BOLD).move_to(P3(4.6, -0.65))
        q1, q2 = predict_marks()
        title = lab("Pause and predict", 40, GOLD, weight=BOLD).move_to(P3(3.9, 3.2))
        self.add(nl, q1, q2, title)
        self.wait(2.0)
        self.play(Indicate(q1, color=NA, scale_factor=1.2), run_time=1.2)
        self.play(Indicate(q2, color=KC, scale_factor=1.2), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S12Reveal(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.55, flows=True)
        W.met.na_g.set_opacity(1)
        pump = W.pump
        self.at("the pump freezes")
        self.play(pump.block.animate.set_fill(GREY, 0.2).set_stroke(GREY, 4), run_time=0.9)
        fz = lab("pump frozen", 32, GREY if False else TEXT, weight=BOLD).move_to(P3(3.6, 0.0))
        self.play(FadeIn(fz), run_time=0.4)
        for f in W.flows:
            f.speed.set_value(1.0)
        self.at("sodium leaks in")
        self.play(Indicate(W.slabs["na"], color=NA, scale_factor=1.2), run_time=1.0)
        self.at("and potassium leaks out")
        self.play(Indicate(W.slabs["k"], color=KC, scale_factor=1.2), run_time=1.0)
        self.at("both downhill")
        self.play(FadeOut(fz), run_time=0.3)
        self.at("the two differences")
        dl = VGroup(lab("differences shrinking", 32, GOLD, weight=BOLD), lab("(schematic)", 28, TEXT)).arrange(DOWN, buff=0.1).move_to(P3(3.9, 3.0))
        self.play(FadeIn(dl), run_time=0.5)
        W.met.drift(4.5, nao=1.9, nai=1.5, kio=1.9, koi=1.5)
        self.at("the first film's rule")
        r = hill_ramp(2.2, -0.3, 5.8, -2.1)
        ball = Dot(P3(2.2, -0.0), radius=0.2, color=WATER).set_z_index(12)
        rl = lab("downhill: free", 32, WATER, weight=BOLD).move_to(P3(4.0, -2.75))
        self.play(Create(r), FadeIn(ball), FadeIn(rl), run_time=0.8)
        self.play(ball.animate.move_to(P3(5.5, -1.75)), rate_func=rate_functions.ease_in_sine, run_time=2.0)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S13Cost(SpokenScene):
    def construct(self):
        W = build_world(self, slots=("na", "k", "pump"), meters=True, dim=0.55,
                        mvals=dict(nao=1.9, nai=1.5, kio=1.9, koi=1.5))
        W.met.na_g.set_opacity(1)
        pump = W.pump
        pump.block.set_fill(GREY, 0.2).set_stroke(GREY, 4)
        W.met.drift(10.0, nao=1.5, nai=1.8, kio=1.5, koi=1.8)
        one = lab("not a one-time payment", 34, GOLD, weight=BOLD).move_to(P3(3.9, 3.1))
        self.add(one)
        self.at("one time payment")
        self.play(Indicate(one, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.at("the leaks")
        self.play(Indicate(W.slabs["na"], color=NA, scale_factor=1.2), Indicate(W.slabs["k"], color=KC, scale_factor=1.2),
                  run_time=1.4)
        self.at("the pump must keep spending")
        W.met.goal.clear()
        W.met.drift(4.6, nao=2.8, nai=0.5, kio=2.8, koi=0.5)
        bn = bin_with_tokens(4)
        tally = Tally(0, 0, 0)
        W.tally = tally
        self.play(FadeOut(one), FadeIn(bn), FadeIn(tally),
                  pump.block.animate.set_fill(PROT, 0.6).set_stroke(PROT, 4), run_time=0.8)
        for i in range(3):
            tok = bn.toks[i]
            tfrom = tok.get_center()
            tok.set_opacity(0)
            pump_cycle(self, W, sp=0.36, token_from=(tfrom[0], tfrom[1]))
        self.at("stop paying", lead=0.0)
        W.met.goal.clear()
        W.met.drift(2.2, nao=2.0, nai=1.3, kio=2.0, koi=1.3)
        nl = lab("ATP: none left", 32, ATP, weight=BOLD).move_to(P3(4.6, -0.65))
        self.play(pump.block.animate.set_fill(GREY, 0.2).set_stroke(GREY, 4), FadeIn(nl), run_time=0.8)
        self.wait(1.6)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S14Test(SpokenScene):
    def construct(self):
        self.wait(0.8)
        self.at("one test for a substance")
        t = lab("Crossing on its own?", 40, GOLD, weight=BOLD).move_to(P3(0, 3.2))
        self.play(FadeIn(t), run_time=0.7)
        self.at("is it going downhill")
        ra = VGroup(Polygon(P3(-6.2, 2.4), P3(-0.9, -1.5), P3(-6.2, -1.5), stroke_width=0, fill_color=GREY, fill_opacity=0.18),
                    hill_ramp(-6.2, 2.4, -0.9, -1.5))
        ang = np.arctan2(-3.9, 5.3)
        nrm = np.array([-np.sin(ang), np.cos(ang), 0.0])
        a0 = P3(-6.2, 2.4) + nrm * 0.3
        a1 = P3(-0.9, -1.5) + nrm * 0.3
        ball = Dot(a0, radius=0.3, color=WATER).set_z_index(12)
        self.play(Create(ra), FadeIn(ball), run_time=0.9)
        self.play(ball.animate.move_to(a1), rate_func=rate_functions.ease_in_sine, run_time=1.8)
        self.at("passive and free")
        dl = lab("downhill: passive, free", 36, WATER, weight=BOLD).move_to(P3(-3.4, -2.7))
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.7)
        self.at("is it going uphill")
        rb = VGroup(Polygon(P3(0.9, -1.5), P3(6.2, 2.4), P3(6.2, -1.5), stroke_width=0, fill_color=GREY, fill_opacity=0.18),
                    hill_ramp(0.9, -1.5, 6.2, 2.4))
        ang2 = np.arctan2(3.9, 5.3)
        nrm2 = np.array([-np.sin(ang2), np.cos(ang2), 0.0])
        b0 = P3(0.9, -1.5) + nrm2 * 0.3
        b1 = P3(6.2, 2.4) + nrm2 * 0.3
        ball2 = Dot(b0 + (b1 - b0) * 0.06, radius=0.3, color=WATER).set_z_index(12)
        tk = token(0.45).move_to(b0 - nrm2 * 1.0 + (b1 - b0) * 0.06).set_z_index(12)
        self.play(Create(rb), FadeIn(ball2), FadeIn(tk), run_time=0.9)
        self.play(ball2.animate.move_to(b0 + (b1 - b0) * 0.8), tk.animate.move_to(b0 - nrm2 * 1.0 + (b1 - b0) * 0.8),
                  run_time=2.2)
        self.at("the cell is paying")
        ul = lab("uphill: the cell pays", 36, ATP, weight=BOLD).move_to(P3(3.4, -2.7))
        self.play(FadeIn(ul, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(tk, color=ATP, scale_factor=1.2), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------------------
class S15End(EndCard):
    LINE = "Downhill is free; uphill costs energy, every cycle."
