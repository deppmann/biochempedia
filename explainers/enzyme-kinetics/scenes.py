"""Enzyme kinetics: why enzymes hit a speed limit  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every cue below is looked up in the faster-whisper word timestamps in
_shared/stt/enzyme-kinetics__<clip>.json (self.at("phrase") waits until that phrase starts, minus a lead).

COLOR MAP (one color per concept, whole video)
  BLUE   = the enzyme, and the velocity curve v (the enzyme's output)
  YELLOW = substrate, [S], the cars
  GREEN  = product, and kcat (reactions completed per second)
  RED    = Vmax, the ceiling
  GOLD   = Km, the half-max marker
  GREY   = axes, structure, de-emphasized
  (Km scene only: three substrate curves use BLUE / TEAL / PURPLE as a legend.)
"""
import json
import os
import re
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

# Manim's partial-movie cache reused stale clips here (S01 came out 1.2 s long with cues shifted), so
# every render is from scratch. Cheap at -ql.
config.disable_caching = True

PURPLE = "#B58CD9"
STT_DIR = Path(__file__).resolve().parent.parent / "_shared" / "stt"


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


class Scn(NarratedScene):
    """NarratedScene + at(): wait until a spoken phrase starts (word timestamps from speech-to-text)."""

    def _words(self):
        if not hasattr(self, "_wl"):
            sid = os.environ["KX_SCENE_ID"]
            sc = next(s for s in json.loads(Path(os.environ["KX_SCRIPT"]).read_text())["scenes"] if s["id"] == sid)
            stem = Path(sc["clip"]).stem
            d = json.loads((STT_DIR / f"enzyme-kinetics__{stem}.json").read_text())
            self._wl = [(float(w[0]), _norm(w[2])) for w in d["words"] if _norm(w[2])]
        return self._wl

    def t_of(self, phrase, nth=0):
        toks = [_norm(p) for p in phrase.split() if _norm(p)]
        wl = self._words()
        hits = [wl[i][0] for i in range(len(wl) - len(toks) + 1) if [x[1] for x in wl[i:i + len(toks)]] == toks]
        if len(hits) <= nth:
            raise ValueError(f"phrase not spoken: {phrase!r} (nth={nth})")
        return hits[nth]

    def at(self, phrase, lead=0.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        with open(Path(__file__).parent / "lateness.log", "a") as lg:
            lg.write(f"{os.environ.get('KX_SCENE_ID')}  {phrase[:28]!r:34} spoken {target + lead:5.1f}  "
                     f"now {self.elapsed():5.1f}  late {-rest:+5.1f}\n")
        if rest > 0.02:
            self.wait(rest)

    def step(self, anims, run_time):
        """play() that tolerates an empty animation list."""
        anims = [a for a in anims if a is not None]
        if anims:
            self.play(*anims, run_time=run_time)
        else:
            self.wait(run_time)


def mm(S, V=1.0, K=2.0):
    return V * S / (K + S)


def make_axes(x_max, y_max, w, h, origin, x_step=2, y_step=1):
    ax = Axes(x_range=[0, x_max, x_step], y_range=[0, y_max, y_step], x_length=w, y_length=h,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY,
                           "stroke_width": 3, "tip_width": 0.16, "tip_height": 0.16}, tips=True)
    ax.shift(np.array([origin[0], origin[1], 0]) - ax.c2p(0, 0))
    return ax


def axis_labels(ax, xtext, ytext, size=26, x_dy=0.55, y_dx=0.6):
    xl = T(xtext, size)
    xl.move_to([ax.c2p(0, 0)[0] + ax.x_length / 2, ax.c2p(0, 0)[1] - x_dy, 0])
    yl = T(ytext, size).rotate(PI / 2)
    yl.move_to([ax.c2p(0, 0)[0] - y_dx, ax.c2p(0, 0)[1] + ax.y_length / 2, 0])
    return xl, yl


def curve(ax, V=1.0, K=2.0, x_max=None, color=BLUE, width=6):
    return ax.plot(lambda x: V * x / (K + x), x_range=[0, x_max if x_max else ax.x_range[1]],
                   color=color, stroke_width=width)


def dline(a, b, color=GREY, w=3, **kw):
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.12, **kw)


def vband(ax, a, b, color=YELLOW, op=0.09):
    r = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.y_length, stroke_width=0,
                  fill_color=color, fill_opacity=op)
    r.move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, ax.c2p(0, 0)[1] + ax.y_length / 2, 0])
    return r


def eq_kcat(size=40):
    """kcat = Vmax / [E]T, built by hand (no LaTeX)."""
    kcat = T("kcat", size, GREEN, weight=BOLD)
    eq = T("=", size)
    vmax = T("Vmax", size, RED, weight=BOLD)
    sl = T("/", size)
    e = T("[E]", size, BLUE, weight=BOLD)
    sub = T("T", int(size * 0.6), BLUE, weight=BOLD)
    g = VGroup(kcat, eq, vmax, sl, e).arrange(RIGHT, buff=0.22)
    sub.next_to(e, RIGHT, buff=0.03).align_to(e, DOWN).shift(DOWN * 0.1)
    return VGroup(g, sub), kcat, vmax, e, sub


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Enzyme kinetics"
    TITLE = "Why enzymes hit a speed limit"


# --------------------------------------------------------------------------------------------
class S01Tollbooth(Scn):
    """Spoken: toll booth -> light traffic (v proportional to [S]) -> [S] = Km is half capacity ->
    heavy traffic, saturated, flat out at Vmax -> more cars don't help -> saturation is not stopping."""

    def construct(self):
        K, XM = 2.0, 16
        heading = T("A toll booth is an enzyme", 36, font=TITLE_FONT).to_edge(UP, buff=0.45)

        # --- the toll booth (enzyme, one active site) -------------------------------------
        booth = RoundedRectangle(corner_radius=0.2, width=2.5, height=1.7, stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.14).move_to([-2.6, 0.5, 0])
        slot = RoundedRectangle(corner_radius=0.1, width=0.85, height=0.55, stroke_color=GREY, stroke_width=2.5,
                                fill_opacity=0).move_to(booth)
        booth_lbl = T("toll booth = enzyme", 26, BLUE).next_to(booth, UP, buff=0.22)
        STATE_POS = np.array([-3.8, -1.0, 0])
        cur = [None]

        # --- substrate pool: a grid of waiting cars (more cars = more substrate) -----------
        # queue front sits level with the booth slot (row 4, y = 0.45) so a car rolls straight in and never
        # crosses the state text; columns at 0.58 spacing keep the grid inside the safe frame and clear of the meter
        slots = [np.array([-6.05 + 0.58 * c, -1.55 + 0.5 * r, 0]) for r in (4, 3, 2, 1, 0, 5) for c in (3, 2, 1, 0)]

        def car(color=YELLOW):
            return RoundedRectangle(corner_radius=0.09, width=0.5, height=0.3, stroke_width=0,
                                    fill_color=color, fill_opacity=0.95)

        pool = []
        sub_lbl = T("substrate", 26, YELLOW).move_to([-5.0, -2.35, 0])
        prod_lbl = T("product", 26, GREEN).move_to([-0.55, 1.15, 0])
        exit_pt = np.array([-0.55, 0.5, 0])

        # --- how busy the worker is = v / Vmax = fraction of booth time occupied -------------
        MW = 2.5
        meter_box = RoundedRectangle(corner_radius=0.08, width=MW, height=0.28, stroke_color=GREY,
                                     stroke_width=2.5).move_to([-3.8 + MW / 2, -1.55, 0])
        meter_lbl = T("worker busy (average)", 24, GREY).move_to([-3.8, -2.05, 0], aligned_edge=LEFT)

        def mrect(frac):
            w = max(0.02, (MW - 0.08) * frac)
            return Rectangle(width=w, height=0.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.9
                             ).move_to(meter_box.get_left() + RIGHT * (0.04 + w / 2))

        meter_fill = mrect(0.0)

        def set_meter(frac):
            return Transform(meter_fill, mrect(frac))

        # --- plot: velocity vs substrate ----------------------------------------------------
        ax = make_axes(XM, 1.25, 4.9, 4.3, origin=(1.55, -1.95), x_step=4, y_step=0.5)
        xl, yl = axis_labels(ax, "substrate [S]", "velocity v", size=26, x_dy=0.55, y_dx=0.5)

        def set_state(txt, size=26, bold=False):
            new = T(txt, size, TEXT, weight=BOLD if bold else NORMAL).move_to(STATE_POS, aligned_edge=LEFT)
            old = cur[0]
            cur[0] = new
            if old is None:
                return [FadeIn(new)]
            # old label leaves before the new one arrives, so the two never overlap
            return [AnimationGroup(FadeOut(old), FadeIn(new), lag_ratio=1.0)]

        def add_cars(n):
            new = []
            for _ in range(n):
                if len(pool) >= len(slots):
                    break
                c = car()
                c.move_to(slots[len(pool)])
                pool.append(c)
                new.append(c)
            return [FadeIn(c, scale=0.6) for c in new]

        def shift_pool():
            return [c.animate.move_to(slots[i]) for i, c in enumerate(pool)]

        inside = [None]

        def load(f=1.0, color_busy=0.55):
            c = pool.pop(0)
            inside[0] = c
            self.play(c.animate.move_to(slot.get_center()), booth.animate.set_fill(BLUE, color_busy),
                      *shift_pool(), run_time=0.45 * f)

        def unload(f=1.0, idle_after=True):
            c = inside[0]
            inside[0] = None
            self.play(c.animate.set_fill(GREEN, 1.0), run_time=0.25 * f)
            anims = [c.animate.move_to(exit_pt)]
            if idle_after:
                anims.append(booth.animate.set_fill(BLUE, 0.14))
            self.play(*anims, run_time=0.4 * f)
            self.play(FadeOut(c, scale=0.6), run_time=0.15 * f)

        def serve(f=1.0):
            load(f)
            unload(f)

        def flow(until, f=0.6):
            """Booth works non-stop (queue never empty) until time `until`."""
            if inside[0] is None and pool:
                load(f)
            while pool and self.elapsed() + 1.25 * f + 0.2 < until:
                unload(f, idle_after=False)
                self.step(add_cars(1), 0.2)
                load(f)

        def dot_at(S, color=BLUE, r=0.11):
            return Dot(ax.c2p(S, mm(S, 1.0, K)), radius=r, color=color)

        self.play(FadeIn(heading), FadeIn(booth), FadeIn(slot), FadeIn(booth_lbl), FadeIn(sub_lbl),
                  FadeIn(prod_lbl), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(meter_box), FadeIn(meter_fill),
                  FadeIn(meter_lbl), run_time=1.6)

        # ---- "When traffic is light, low substrate, every car gets processed as fast as it arrives,
        #      so velocity is proportional to substrate."
        self.at("When traffic", 0.1)
        self.play(*add_cars(1), *set_state("light traffic"), set_meter(0.13), run_time=0.5)
        self.at("low substrate", 0.1)
        band_low = vband(ax, 0, 1.2)
        self.play(*set_state("light traffic = low [S]"), FadeIn(band_low), run_time=0.5)
        self.at("every car", 0.15)
        serve(1.0)
        self.at("as fast as", 0.1)
        self.step(add_cars(1), 0.3)
        serve(0.8)
        self.at("velocity", 0.1)
        tan = dline(ax.c2p(0, 0), ax.c2p(1.2, 0.6), GREEN, 5)
        self.play(Create(tan), run_time=0.9)
        self.at("proportional", 0.1)
        prop = T("v ∝ [S]", 28, GREEN, weight=BOLD).next_to(ax.c2p(1.2, 0.6), UP, buff=0.12).shift(RIGHT * 0.5)
        self.play(FadeIn(prop, shift=UP * 0.1), run_time=0.6)

        # ---- "When substrate equals Km, you're at half capacity."
        self.at("When substrate", 0.1)
        full = curve(ax, 1.0, K, XM)
        self.play(FadeOut(VGroup(band_low, tan, prop)), *set_state("[S] = Km"), set_meter(0.5),
                  booth.animate.set_fill(BLUE, 0.35), Create(full), run_time=1.3)
        self.at("km", 0.2)
        km_dot = dot_at(K, GOLD, 0.13)
        km_v = dline(ax.c2p(K, 0), ax.c2p(K, 0.5), GOLD, 3)
        km_h = dline(ax.c2p(0, 0.5), ax.c2p(K, 0.5), GOLD, 3)
        km_lbl = T("Km", 28, GOLD, weight=BOLD).next_to(ax.c2p(K, 0), DOWN, buff=0.12)
        half_lbl = T("½Vmax", 26, GOLD, weight=BOLD).next_to(ax.c2p(K, 0.5), DOWN + RIGHT, buff=0.12).shift(RIGHT * 0.1)
        self.play(Create(km_v), Create(km_h), FadeIn(km_dot, scale=0.5), FadeIn(km_lbl), run_time=0.9)
        self.at("half capacity", 0.1)
        self.play(*set_state("half capacity", 26, True), FadeIn(half_lbl), run_time=0.6)

        # ---- "And when traffic is heavy, high substrate, the booth is saturated, working flat out at Vmax."
        self.at("And when traffic", 0.1)
        self.play(FadeOut(VGroup(km_dot, km_v, km_h, km_lbl, half_lbl)), *set_state("heavy traffic = high [S]"),
                  *add_cars(18), set_meter(0.86), run_time=0.8)
        self.at("high substrate", 0.1)
        band_hi = vband(ax, 10, XM)
        d_hi = dot_at(12)
        self.play(FadeIn(band_hi), FadeIn(d_hi, scale=0.5), run_time=0.5)
        self.at("The booth", 0.1)
        self.play(*set_state("saturated", 28, True), booth.animate.set_fill(BLUE, 0.55), run_time=0.4)
        load(0.6)
        flow(self.t_of("VMAX") - 0.15, 0.6)
        self.at("VMAX", 0.1)
        vmax_line = dline(ax.c2p(0, 1), ax.c2p(XM, 1), RED, 4)
        vmax_lbl = T("Vmax", 28, RED, weight=BOLD).next_to(ax.c2p(XM, 1), UP, buff=0.12).shift(LEFT * 0.7)
        self.play(Create(vmax_line), FadeIn(vmax_lbl), set_meter(1.0), FadeOut(band_hi), run_time=0.7)

        # ---- "Adding more cars doesn't make the worker any faster."
        flow(self.t_of("Adding more") - 0.15, 0.6)
        self.at("Adding more", 0.1)
        da, db = dot_at(8), dot_at(XM)
        arr = Arrow(da.get_center(), db.get_center() + LEFT * 0.12, buff=0.12, color=YELLOW, stroke_width=4,
                    max_tip_length_to_length_ratio=0.2)
        more = T("2x substrate", 26, YELLOW).next_to(ax.c2p(12, 0.5), DOWN, buff=0.05)
        self.play(*set_state("more cars, same speed"), *add_cars(12), FadeIn(da), run_time=0.6)
        self.play(GrowArrow(arr), FadeIn(db), FadeIn(more), run_time=0.9)
        self.at("faster", 0.3)
        same = T("barely faster", 26, BLUE).next_to(more, DOWN, buff=0.1)
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
        flow(self.t_of("Saturation") - 0.15, 0.6)

        # ---- "Saturation doesn't mean the enzyme stops. It means it's already going as fast as it possibly can."
        self.at("Saturation", 0.1)
        self.play(*set_state("saturated ≠ stopped", 28, True), run_time=0.4)
        flow(self.t_of("It means") - 0.15, 0.6)
        self.at("It means", 0.1)
        self.play(*set_state("working flat out: Vmax", 28, True), Indicate(vmax_line, color=RED, scale_factor=1.0),
                  run_time=0.8)
        flow(self.narration_s - 0.5, 0.6)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Curve(Scn):
    """Spoken: Rosetta Stone -> low [S] nearly linear, kcat/Km -> diminishing returns -> high [S] saturated,
    Vmax = kcat times [E] -> Km at the midpoint, v = half Vmax -> Km: how much substrate to get going, not affinity."""

    def construct(self):
        K, VM = 1.5, 1.0
        ax = make_axes(12, 1.25, 10.4, 4.3, origin=(-4.6, -2.0), x_step=2, y_step=0.5)
        xl, yl = axis_labels(ax, "substrate concentration [S]", "initial velocity v₀", size=26, x_dy=1.25, y_dx=0.55)
        yl.rotate(-PI / 2).move_to([ax.c2p(0, 0)[0] + 1.5, ax.c2p(0, 1.25)[1] + 0.3, 0])
        eq = T("v = Vmax·[S] / (Km + [S])", 34, TEXT, font=MONO,
               t2c={"Vmax": RED, "[S]": YELLOW, "Km": GOLD, "v": BLUE}).to_edge(UP, buff=0.5)
        cv = curve(ax, VM, K, 12)

        def region(a, b, label):
            bd = vband(ax, a, b)
            br = Brace(Line(ax.c2p(a, 0), ax.c2p(b, 0)), DOWN, buff=0.08, color=YELLOW)
            tx = T(label, 28, YELLOW).next_to(br, DOWN, buff=0.1)
            return bd, br, tx

        # ---- "This curve is the Rosetta Stone of enzyme kinetics."
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.2)
        self.play(Create(cv), run_time=1.8)
        # ---- "Almost every idea you'll meet maps onto it."
        self.at("Almost every", 0.2)
        self.play(FadeIn(eq, shift=DOWN * 0.15), run_time=0.8)

        # ---- "At low substrate concentration, the rate rises nearly linearly,
        #      and the enzyme's performance depends on kcat over Km."
        self.at("At low substrate", 0.3)
        bd, br, tx = region(0, 1.2, "low [S]")
        self.play(FadeIn(bd), GrowFromCenter(br), FadeIn(tx), run_time=0.8)
        self.at("the rate rises", 0.2)
        tan = dline(ax.c2p(0, 0), ax.c2p(1.65, 1.1), GREEN, 4)
        tip = ax.c2p(1.65, 1.1)
        nl = T("nearly linear", 28, GREEN).next_to(tip, RIGHT, buff=0.15)
        self.play(Create(tan), run_time=1.1)
        self.play(FadeIn(nl, shift=RIGHT * 0.15), run_time=0.5)
        self.at("kcat", 0.3, nth=0)
        kk = T("slope ∝ kcat/Km", 30, GREEN, weight=BOLD).next_to(tip, RIGHT, buff=0.15)
        self.play(ReplacementTransform(nl, kk), run_time=0.7)

        # ---- "Push higher, and you hit diminishing returns."
        self.at("Push higher", 0.3)
        self.play(FadeOut(VGroup(bd, br, tx, tan, kk)), run_time=0.4)
        bd, br, tx = region(1.5, 8.5, "diminishing returns")
        steps = VGroup()
        for a, b in [(1.5, 3.5), (4, 6), (6.5, 8.5)]:
            h = Line(ax.c2p(a, mm(a, 1, K)), ax.c2p(b, mm(a, 1, K)), color=YELLOW, stroke_width=5)
            v = Line(ax.c2p(b, mm(a, 1, K)), ax.c2p(b, mm(b, 1, K)), color=BLUE, stroke_width=9)
            steps.add(h, v)
        self.play(FadeIn(bd), GrowFromCenter(br), run_time=0.5)
        self.at("diminishing", 0.3)
        self.play(FadeIn(tx), LaggedStart(*[Create(m) for m in steps], lag_ratio=0.45), run_time=1.7)

        # ---- "At high substrate, the enzyme is saturated."
        self.at("At high substrate", 0.3)
        self.play(FadeOut(VGroup(bd, br, tx, steps)), run_time=0.4)
        bd, br, tx = region(9.5, 12, "high [S]")
        self.play(FadeIn(bd), GrowFromCenter(br), FadeIn(tx), run_time=0.7)
        self.at("saturated", 0.3)
        tx2 = T("high [S]: saturated", 28, YELLOW).move_to(tx)
        if tx2.get_right()[0] > 6.15:   # keep the wider label inside the safe frame
            tx2.shift(LEFT * (tx2.get_right()[0] - 6.15))
        self.play(Transform(tx, tx2), run_time=0.5)

        # ---- "Adding more barely changes the rate, and you're at Vmax, which equals kcat times the enzyme concentration."
        self.at("Adding more", 0.2)
        s_arr = Arrow(ax.c2p(9.8, 0.55), ax.c2p(11.8, 0.55), buff=0, color=YELLOW, stroke_width=5,
                      max_tip_length_to_length_ratio=0.2)
        s_t1 = T("more [S]", 26, YELLOW).next_to(s_arr, UP, buff=0.1)
        s_t2 = T("barely faster", 26, BLUE).next_to(s_arr, DOWN, buff=0.12)
        s3 = VGroup(s_arr, s_t1, s_t2)
        self.play(Create(s3), run_time=1.1)
        self.at("Vmax", 0.4)
        vline = dline(ax.c2p(0, VM), ax.c2p(12, VM), RED, 4)
        vm_t = T("Vmax", 30, RED, weight=BOLD)
        kc_t = T("= kcat·[E]", 30, GREEN, weight=BOLD)
        vlab = VGroup(vm_t, kc_t).arrange(RIGHT, buff=0.18).next_to(ax.c2p(7.0, VM), UP, buff=0.18)
        self.play(Create(vline), FadeIn(vm_t, shift=DOWN * 0.1), run_time=0.8)
        self.at("kcat", 0.3, nth=1)
        self.play(FadeIn(kc_t, shift=RIGHT * 0.1), run_time=0.7)

        # ---- "Km sits at the midpoint of the curve, where velocity is half of Vmax."
        self.at("Km sits", 0.3)
        self.play(FadeOut(VGroup(bd, br, tx, s3)), run_time=0.4)
        pt = Dot(ax.c2p(K, VM / 2), radius=0.13, color=GOLD)
        vl = dline(ax.c2p(K, 0), ax.c2p(K, VM / 2), GOLD, 3)
        kmlab = T("Km", 30, GOLD, weight=BOLD).next_to(ax.c2p(K, 0), DOWN, buff=0.15)
        self.play(Create(vl), FadeIn(pt, scale=0.5), FadeIn(kmlab), run_time=1.0)
        self.at("where velocity", 0.2)
        hl = dline(ax.c2p(0, VM / 2), ax.c2p(K, VM / 2), GOLD, 3)
        halflab = T("½Vmax", 28, GOLD, weight=BOLD).next_to(ax.c2p(0, VM / 2), LEFT, buff=0.15)
        self.play(Create(hl), FadeIn(halflab), run_time=0.9)

        # ---- "Read it as how much substrate the enzyme needs to get going, not automatically as a measure of affinity."
        self.at("Read it", 0.3)
        note = T("Km: how much substrate the enzyme needs", 30, GOLD).move_to(ax.c2p(7.0, 0.3))
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
        self.at("not automatically", 0.2)
        aff = T("not automatically a measure of affinity", 28, GREY).next_to(note, DOWN, buff=0.25)
        self.play(FadeIn(aff, shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Km(Scn):
    """Spoken: Km is useful -> enzyme prefers one substrate; lowest Km captured most efficiently, half-maximal
    speed at the lowest concentration -> vending machine: quarters, dimes, pennies; same output, quarters most
    smoothly -> Km is usually close to the [S] the enzyme sees in the living cell."""

    def construct(self):
        KM = [0.5, 2.0, 5.0]
        COIN = ["quarter", "dime", "penny"]
        CC = [BLUE, TEAL, PURPLE]
        heading = T("Why Km is so useful", 34, font=TITLE_FONT).to_edge(UP, buff=0.45)

        # ---- "An enzyme can prefer one substrate over another."
        enz = chip("enzyme", BLUE, size=34).move_to([-4.4, 0, 0])
        ys = [1.9, 0.0, -1.9]
        subs = [chip(f"S{i + 1}", YELLOW, size=32).move_to([1.6, y, 0]) for i, y in enumerate(ys)]
        kms = [T(f"Km = {k:g} mM", 28, GOLD).move_to([3.5, y, 0], aligned_edge=LEFT) for y, k in zip(ys, KM)]
        arrows = [Arrow(enz.get_right() + RIGHT * 0.1, s.get_left() + LEFT * 0.1, buff=0.05, color=BLUE,
                        stroke_width=w, max_tip_length_to_length_ratio=0.12)
                  for s, w in zip(subs, [14, 7, 3])]
        self.play(FadeIn(heading), FadeIn(enz, shift=RIGHT * 0.2), run_time=1.2)
        self.at("An enzyme", 0.1)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(s), FadeIn(k)) for s, k in zip(subs, kms)], lag_ratio=0.3),
                  run_time=1.5)
        self.at("one substrate", 0.1)
        self.play(*[GrowArrow(a) for a in arrows], run_time=1.0)
        # ---- "The one with the lowest Km is captured most efficiently,"
        self.at("lowest", 0.1)
        ring = SurroundingRectangle(VGroup(subs[0], kms[0]), color=GOLD, buff=0.2, corner_radius=0.15)
        self.play(Create(ring), run_time=0.8)

        # ---- "reaching half-maximal speed at the lowest concentration."
        self.at("reaching", 1.6)
        ax = make_axes(12, 1.15, 8.0, 4.4, origin=(-5.3, -2.0), x_step=2, y_step=0.5)
        xl, yl = axis_labels(ax, "substrate concentration [S] (mM)", "velocity v₀", size=26, x_dy=0.95, y_dx=0.55)
        legend_y = [1.35, -0.15, -1.65]
        self.play(FadeOut(ring), FadeOut(VGroup(*arrows)), FadeOut(enz),
                  *[s.animate.move_to([4.9, y, 0]).set_color(c) for s, y, c in zip(subs, legend_y, CC)],
                  *[k.animate.move_to([4.9, y - 0.62, 0]) for k, y in zip(kms, legend_y)],
                  Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.9)
        curves = [curve(ax, 1.0, k, 12, c) for k, c in zip(KM, CC)]
        self.play(LaggedStart(*[Create(cv) for cv in curves], lag_ratio=0.3), run_time=1.1)
        self.at("half maximal", 0.1)
        half = dline(ax.c2p(0, 0.5), ax.c2p(12, 0.5), GOLD, 3)
        halflab = T("½Vmax", 28, GOLD, weight=BOLD).next_to(ax.c2p(12, 0.5), UP, buff=0.08, aligned_edge=RIGHT)
        self.play(Create(half), FadeIn(halflab), run_time=0.6)
        self.at("lowest concentration", 0.3)
        marks = VGroup()
        for k in KM:
            marks.add(Dot(ax.c2p(k, 0.5), radius=0.11, color=GOLD), dline(ax.c2p(k, 0), ax.c2p(k, 0.5), GOLD, 3))
        tick_labels = VGroup(*[T(f"{k:g}", 26, GOLD, weight=BOLD).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                               for k in KM])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.2), FadeIn(tick_labels), run_time=1.3)

        # ---- "It's like a vending machine that takes quarters, dimes, and pennies."
        self.at("It's like a vending", 0.2)
        vend = chip("vending machine", BLUE, size=26).move_to([4.6, 2.6, 0])
        self.play(FadeIn(vend, shift=DOWN * 0.1), run_time=0.6)

        def coin(i):
            return chip(COIN[i], CC[i], size=30).move_to([4.9, legend_y[i], 0])
        self.at("quarters", 0.15)
        c0 = coin(0)
        self.play(ReplacementTransform(subs[0], c0), run_time=0.4)
        self.at("dimes", 0.1)
        c1 = coin(1)
        self.play(ReplacementTransform(subs[1], c1), run_time=0.4)
        self.at("pennies", 0.1)
        c2 = coin(2)
        self.play(ReplacementTransform(subs[2], c2), run_time=0.4)

        # ---- "Same output,"
        self.at("Same output", 0.1)
        vline = dline(ax.c2p(0, 1), ax.c2p(12, 1), RED, 4)
        vlab = T("same Vmax", 30, RED, weight=BOLD).next_to(ax.c2p(6, 1), UP, buff=0.15)
        self.play(Create(vline), FadeIn(vlab), run_time=0.7)
        # ---- "but it handles quarters most smoothly."
        self.at("quarters", 0.3, nth=1)
        ring2 = SurroundingRectangle(VGroup(c0, kms[0]), color=GOLD, buff=0.15, corner_radius=0.15)
        self.play(curves[0].animate.set_stroke(width=9), curves[1].animate.set_stroke(opacity=0.3),
                  curves[2].animate.set_stroke(opacity=0.3), Create(ring2), run_time=0.8)

        # ---- "And remarkably, an enzyme's Km is usually close to the substrate concentration it actually
        #      sees inside the living cell."
        self.at("And remarkably", 0.1)
        keep = {id(heading)}
        self.play(*[FadeOut(m) for m in list(self.mobjects) if id(m) not in keep], run_time=0.9)
        line_y = -0.2
        nline = Arrow([-5.4, line_y, 0], [5.4, line_y, 0], buff=0, color=GREY, stroke_width=4,
                      max_tip_length_to_length_ratio=0.03)
        conc = T("substrate concentration", 26, GREY).move_to([-5.4, line_y - 0.5, 0], aligned_edge=LEFT)
        self.at("enzyme's", 0.2)
        self.play(Create(nline), FadeIn(conc), run_time=0.8)
        # Above the line it reads "Km ≈ [S]"; the note under the [S] dot says which [S].
        self.at("km is usually", 0.1)
        gx, yx = -0.9, 0.9
        g_dot = Dot([gx, line_y, 0], radius=0.14, color=GOLD)
        g_lbl = T("Km", 34, GOLD, weight=BOLD).move_to([gx, line_y + 0.6, 0])
        self.play(FadeIn(g_dot, scale=0.5), FadeIn(g_lbl, shift=DOWN * 0.1), run_time=0.6)
        self.at("close to", 0.1)
        approx = T("≈", 44).move_to([(gx + yx) / 2, line_y + 0.6, 0])
        self.play(FadeIn(approx, scale=0.8), run_time=0.4)
        self.at("substrate concentration", 0.3)
        y_dot = Dot([yx, line_y, 0], radius=0.14, color=YELLOW)
        y_lbl = T("[S]", 34, YELLOW, weight=BOLD).move_to([yx, line_y + 0.6, 0])
        self.play(FadeIn(y_dot, scale=0.5), FadeIn(y_lbl, shift=DOWN * 0.1), run_time=0.6)
        self.at("it actually sees", 0.2)
        sees = T("what the enzyme actually sees", 26, YELLOW).move_to([yx - 0.25, line_y - 0.55, 0],
                                                                      aligned_edge=LEFT)
        self.play(FadeIn(sees, shift=UP * 0.1), run_time=0.6)
        self.at("inside the living", 0.1)
        cell = RoundedRectangle(corner_radius=0.5, width=11.6, height=4.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.06).move_to([0, line_y - 0.1, 0])
        cell_lbl = T("inside the living cell", 28, GREY).move_to(cell.get_corner(UL) + RIGHT * 0.5 + DOWN * 0.4,
                                                              aligned_edge=LEFT)
        self.play(Create(cell), FadeIn(cell_lbl), run_time=1.3)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Kcat(Scn):
    """Spoken: Vmax depends on [E] -> use kcat, the turnover number -> reactions per enzyme per second when
    saturated: top speed -> carbonic anhydrase 600,000/s, lysozyme 1 per 2 s -> kcat is only top speed, silent on
    scarce substrate -> that is kcat/Km, the catalytic efficiency."""

    def construct(self):
        heading = T("kcat: the turnover number", 36, font=TITLE_FONT).to_edge(UP, buff=0.45)

        # ================= phase 1: Vmax scales with enzyme; divide it out =================
        def tube(n, cx):
            box = RoundedRectangle(corner_radius=0.15, width=2.2, height=2.6, stroke_color=GREY, stroke_width=3)
            box.move_to([cx, -0.4, 0])
            dots = VGroup(*[Dot(radius=0.14, color=BLUE) for _ in range(n)])
            dots.arrange(RIGHT, buff=0.35).move_to(box.get_center() + DOWN * 0.7)
            return VGroup(box, dots), box, dots

        eq, kcat_t, vmax_t, e_t, sub_t = eq_kcat(40)
        eq.move_to([0, 2.5, 0])
        tA, boxA, dotsA = tube(1, -3.4)
        tB, boxB, dotsB = tube(2, 2.0)
        lblA = T("1 enzyme", 28, BLUE).next_to(boxA, DOWN, buff=0.2)
        lblB = T("2 enzymes", 28, BLUE).next_to(boxB, DOWN, buff=0.2)
        unit = 1.1

        def bar(h, color=RED):
            return Rectangle(width=0.8, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)

        barA, barB = bar(unit), bar(2 * unit)
        barA.next_to(boxA, RIGHT, buff=1.0).align_to(boxA, DOWN)
        barB.next_to(boxB, RIGHT, buff=1.0).align_to(boxB, DOWN)
        vA = T("Vmax", 26, RED, weight=BOLD).next_to(barA, UP, buff=0.12)
        vB = T("2 × Vmax", 26, RED, weight=BOLD).next_to(barB, UP, buff=0.12)

        # "Vmax depends on how much enzyme you added."
        self.play(FadeIn(heading), FadeIn(tA), FadeIn(tB), FadeIn(lblA), FadeIn(lblB), run_time=0.7)
        self.play(GrowFromEdge(barA, DOWN), GrowFromEdge(barB, DOWN), FadeIn(vA), FadeIn(vB), run_time=0.8)
        self.at("how much enzyme", 0.1)
        self.play(Indicate(dotsA, color=BLUE, scale_factor=1.4), Indicate(dotsB, color=BLUE, scale_factor=1.4),
                  run_time=1.0)

        # "So to describe the enzyme molecule itself, we use kcat, the turnover number."
        self.at("So to describe", 0.2)
        div = T("÷ [E]", 30, BLUE, weight=BOLD)
        div.move_to([(barA.get_right()[0] + boxB.get_left()[0]) / 2, 0.8, 0])
        self.play(FadeIn(div, scale=0.7), run_time=0.5)
        self.at("molecule", 0.4)
        newA = bar(unit).move_to(barA, aligned_edge=DOWN)
        newB = bar(unit).move_to(barB, aligned_edge=DOWN)
        vA2 = T("Vmax ÷ [E]", 26, RED, weight=BOLD).next_to(newA, UP, buff=0.12)
        vB2 = T("Vmax ÷ [E]", 26, RED, weight=BOLD).next_to(newB, UP, buff=0.12)
        self.play(Transform(barA, newA), Transform(barB, newB), FadeTransform(vA, vA2), FadeTransform(vB, vB2),
                  run_time=1.2)
        same = T("same for 1 or 2: a property of the molecule", 28, TEXT).move_to([0, -2.85, 0])
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.6)
        self.at("we use kcat", 0.25)
        gA = bar(unit, GREEN).move_to(barA, aligned_edge=DOWN)
        gB = bar(unit, GREEN).move_to(barB, aligned_edge=DOWN)
        nA = T("kcat", 26, GREEN, weight=BOLD).next_to(gA, UP, buff=0.12)
        nB = T("kcat", 26, GREEN, weight=BOLD).next_to(gB, UP, buff=0.12)
        self.play(Transform(barA, gA), Transform(barB, gB), FadeTransform(vA2, nA), FadeTransform(vB2, nB),
                  FadeIn(eq, shift=DOWN * 0.15), run_time=0.8)
        self.at("turnover number", 0.2)
        turn = T("the turnover number", 30, GREEN).next_to(eq, DOWN, buff=0.2)
        self.play(FadeIn(turn, shift=UP * 0.1), run_time=0.6)

        # ================= phase 2: one saturated enzyme, reactions per second =================
        self.at("It's the number", 0.4)
        self.play(FadeOut(VGroup(tA, tB, lblA, lblB, barA, barB, nA, nB, div, same, eq, turn)), run_time=0.5)
        enz = chip("one enzyme", BLUE, size=34, pad=0.35).move_to([-0.6, 0.1, 0])
        feed = VGroup(*[Square(0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95) for _ in range(5)])
        feed.arrange(RIGHT, buff=0.18).next_to(enz, LEFT, buff=0.5)
        sub_lbl = T("substrate waiting", 26, YELLOW).next_to(feed, DOWN, buff=0.35)
        out_pts = [enz.get_right() + RIGHT * 0.5, enz.get_right() + RIGHT * 2.0]
        prod_lbl = T("product", 26, GREEN).move_to([out_pts[1][0] - 0.6, -0.55, 0])
        clock = VGroup(Circle(radius=0.7, color=GREY, stroke_width=4), Dot(radius=0.05, color=GREY))
        hand = Line(ORIGIN, UP * 0.55, color=GREEN, stroke_width=5)
        clock_g = VGroup(clock, hand)
        clock_g.move_to([5.0, 0.1, 0])
        one_s = T("1 second", 26, GREEN).next_to(clock, DOWN, buff=0.25)
        defin = T("reactions per enzyme per second", 30, GREEN).move_to([0, -2.4, 0])
        centre = clock.get_center()
        hand.move_to(centre + UP * 0.275)

        slots_x = [m.get_center().copy() for m in feed]
        queue = list(feed)

        def react(until):
            """One substrate in, one product out, repeatedly (schematic of an enzyme running flat out)."""
            while self.elapsed() + 0.44 <= until:
                front = queue.pop(0)
                newc = Square(0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to(slots_x[-1])
                newc.set_opacity(0)
                queue.append(newc)
                self.add(newc)
                self.play(front.animate.move_to(enz.get_left() + LEFT * 0.05).set_opacity(0),
                          *[q.animate.move_to(slots_x[i]) for i, q in enumerate(queue[:-1])],
                          newc.animate.set_opacity(0.95), run_time=0.22, rate_func=linear)
                self.remove(front)
                p = Square(0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.95).move_to(out_pts[0])
                self.add(p)
                self.play(p.animate(rate_func=linear).move_to(out_pts[1]), run_time=0.22)
                self.remove(p)

        self.at("It's the number", 0.0)
        self.play(FadeIn(enz), FadeIn(feed), FadeIn(sub_lbl), FadeIn(prod_lbl), FadeIn(defin, shift=UP * 0.1),
                  run_time=0.7)
        react(self.t_of("per second", nth=0) - 0.6)
        self.at("per second", 0.5)
        hand.add_updater(lambda m, dt: m.rotate(-TAU * dt / 1.0, about_point=centre))
        self.play(FadeIn(clock_g), FadeIn(one_s), run_time=0.6)
        react(self.t_of("fully saturated") - 0.1)
        self.at("fully saturated", 0.1)
        sat = T("saturated: always waiting", 26, YELLOW).move_to(sub_lbl)
        self.play(Transform(sub_lbl, sat), run_time=0.5)
        react(self.t_of("top speed", nth=0) - 0.45)
        self.at("top speed", 0.35, nth=0)
        top_lbl = T("top speed", 34, GREEN, weight=BOLD).next_to(enz, UP, buff=0.5)
        self.play(FadeIn(top_lbl, shift=DOWN * 0.1), run_time=0.5)
        react(self.t_of("Carbonic") - 0.75)

        # ================= phase 3: log scale, carbonic anhydrase vs lysozyme =================
        # (built below; the swap from phase 2 is one staggered move so "top speed" stays up while it is spoken)
        x0, per = -5.4, 1.55
        pos = lambda v: x0 + (np.log10(v) + 1) * per
        line = Arrow(LEFT * 5.9 + DOWN * 0.7, RIGHT * 6.3 + DOWN * 0.7, buff=0, color=GREY, stroke_width=4,
                     max_tip_length_to_length_ratio=0.04)
        ticks = VGroup()
        for e in range(-1, 7):
            x = x0 + (e + 1) * per
            tk = Line([x, -0.82, 0], [x, -0.58, 0], color=GREY, stroke_width=3)
            lab = M("0.1" if e == -1 else ("1" if e == 0 else ("10" if e == 1 else f"10{'⁰¹²³⁴⁵⁶'[e]}")), 24, GREY)
            lab.move_to([x, -1.2, 0])
            ticks.add(tk, lab)
        axis_name = T("kcat (reactions per second), each tick is 10x faster", 26, GREY).move_to([0, -2.0, 0])
        pin_lz = Dot([pos(0.5), -0.7, 0], radius=0.14, color=GREEN)
        lz_name = T("lysozyme", 28, TEXT, weight=BOLD)
        lz_val = M("~0.5 per second", 26, GREEN)
        lz_note = T("(one every 2 seconds)", 24, GREY)
        lz_lbl = VGroup(lz_name, lz_val, lz_note).arrange(DOWN, buff=0.08).move_to([pos(0.5) + 0.9, 0.7, 0])
        lz_stem = Line(pin_lz.get_center(), [pos(0.5), 0.12, 0], color=GREY, stroke_width=2)
        pin_ca = Dot([pos(6e5), -0.7, 0], radius=0.14, color=GREEN)
        ca_name = T("carbonic anhydrase", 28, TEXT, weight=BOLD)
        ca_val = M("~600,000 per second", 26, GREEN)
        ca_lbl = VGroup(ca_name, ca_val).arrange(DOWN, buff=0.1).move_to([5.9, 0.55, 0])
        ca_lbl.shift(LEFT * (ca_lbl.get_right()[0] - 6.2) if ca_lbl.get_right()[0] > 6.2 else ORIGIN)
        ca_stem = Line(pin_ca.get_center(), [pos(6e5), 0.12, 0], color=GREY, stroke_width=2)
        self.play(AnimationGroup(
            FadeOut(VGroup(enz, VGroup(*queue), sub_lbl, prod_lbl, clock_g, one_s, defin, top_lbl)),
            AnimationGroup(Create(line), FadeIn(ticks), FadeIn(axis_name)), lag_ratio=0.5), run_time=0.7)
        hand.clear_updaters()
        self.at("Carbonic", 0.2)
        self.play(FadeIn(pin_ca, scale=0.4), Create(ca_stem), FadeIn(ca_name, shift=DOWN * 0.1), run_time=0.8)
        self.at("600", 0.1)
        self.play(FadeIn(ca_val, shift=DOWN * 0.1), run_time=0.7)
        self.at("plods", 0.6)
        self.play(FadeIn(pin_lz, scale=0.4), Create(lz_stem), FadeIn(lz_name, shift=DOWN * 0.1), run_time=0.9)
        self.at("one reaction", 0.2)
        self.play(FadeIn(lz_val, shift=DOWN * 0.1), FadeIn(lz_note, shift=DOWN * 0.1), run_time=0.8)
        gap = DoubleArrow([pos(0.5) + 0.2, 2.2, 0], [pos(6e5) - 0.2, 2.2, 0], buff=0, color=GREY,
                          stroke_width=3, tip_length=0.2)
        gap_t = T("about a million-fold apart", 28, GREY).next_to(gap, UP, buff=0.12)
        self.play(GrowFromCenter(gap), FadeIn(gap_t), run_time=0.7)

        # ================= phase 4: kcat is only top speed =================
        self.at("But kcat", 0.0)
        self.play(FadeOut(VGroup(line, ticks, axis_name, pin_lz, lz_lbl, lz_stem, pin_ca, ca_lbl, ca_stem, gap,
                                 gap_t)), run_time=0.3)
        ax = make_axes(12, 1.25, 10.2, 3.9, origin=(-5.4, -2.3), x_step=2, y_step=0.5)
        xl, yl = axis_labels(ax, "substrate concentration [S]", "velocity v", size=26, x_dy=0.55, y_dx=0.55)
        cv = curve(ax, 1.0, 1.5, 12)
        vline = dline(ax.c2p(0, 1), ax.c2p(12, 1), RED, 4)
        top = VGroup(T("top speed", 28, TEXT),
                     VGroup(T("Vmax", 30, RED, weight=BOLD), T("= kcat·[E]", 30, GREEN, weight=BOLD)
                            ).arrange(RIGHT, buff=0.16)
                     ).arrange(DOWN, buff=0.12, aligned_edge=RIGHT).next_to(ax.c2p(12, 1), UP, buff=0.15)
        top.align_to(ax.c2p(12, 1), RIGHT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(cv), run_time=0.6)
        self.at("only top speed", 0.1)
        self.play(Create(vline), FadeIn(top, shift=DOWN * 0.1), run_time=0.9)
        # "It doesn't tell you how the enzyme performs when substrate is scarce."
        self.at("when substrate", 0.2)
        bd = vband(ax, 0, 1.2)
        rare = T("substrate scarce", 28, YELLOW).move_to(ax.c2p(3.6, 0.2))
        self.play(FadeIn(bd), FadeIn(rare), run_time=0.7)
        # "For that, you want kcat over Km, the catalytic efficiency."
        self.at("For that", 0.1)
        tan = dline(ax.c2p(0, 0), ax.c2p(1.65, 1.1), GREEN, 5)
        self.play(Create(tan), run_time=0.9)
        self.at("kcat over", 0.2)
        kk = T("slope ∝ kcat/Km", 30, GREEN, weight=BOLD).next_to(ax.c2p(1.65, 1.1), RIGHT, buff=0.15
                                                                 ).shift(UP * 0.22)
        self.play(FadeIn(kk, shift=RIGHT * 0.15), run_time=0.5)
        self.at("the catalytic", 0.1)
        eff = T("catalytic efficiency", 28, GREEN).next_to(kk, UP, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(eff, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05End(EndCard):
    LINE = "Drag Km and Vmax yourself in the lesson's plotter."
