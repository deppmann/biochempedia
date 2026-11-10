"""The Guest Inside Your Cells: vertical social cut (9:16) of How Your Cells Got Mitochondria.

Same world, colours and objects as the web film (scenes.py), re-staged to run TOP TO BOTTOM for a
tall frame: the guest lives in the upper half of a tall blue cell and the nucleus in the lower half.
Every builder is imported from scenes.py, so both cuts share one look. Only four things are new
here: VRing (a bead ring that can slide along its host, for the division beat), O2Fall (oxygen
dropping in from the top or the sides of the frame instead of from the right), Strip (a close-up
of the yellow row under the bean, so the lower frame is used and oxygen can be seen landing) and
the tall presets.

COLOR MAP (the web film's, unchanged)
  BLUE the host and what is the host's     PINK the guest lineage (and its beads, wherever they go)
  YELLOW energy (the row of blocks, sparks) RED oxygen          GREEN a clue that matches
  GOLD not settled in science ("?")        GREY what did not happen (the digested ghost)

Frame: 8 wide x 14.22 tall. Subject inside x -3.5..3.5, y -3.0..5.4. Nothing is drawn to stay in
y -4.6..-3.2 (burned-in captions). No subtitles, no scrubber, no predict pause, no title card.
Counts: exactly 13 beads in the ring of today and 13 pink tiles; 40 = 15 lost + 12 moved + 13 kept
is schematic and tagged so on screen until the count to 13 starts.
"""
import json
import math
import os
import random
from pathlib import Path

import numpy as np
import bp_style
from bp_style import *
from scenes import (PINK, A13, A40, KEPT_A, LOST, MOVED, PINK_SLOTS, T0, Cell, Guest, Nucleus, Proc, Ring, Shimmer, Sparks,
                    Specks, Tw, circ, flicker, gold_badge, label, lerp, make_backdrop, mix, now, o2_token, poly_pts, pulse,
                    rod_outline, split, star, start_clock)

FW, FH = config.frame_width, config.frame_height
PER = 16.0                                  # seconds for one turn of a bead ring (faster than the web film: a feed is impatient)
DV = 0.04                                   # rings ride a little above the middle, clear of the yellow row
R13V, B13V = 0.21, 0.040                    # the 13-bead ring of today (radius and bead size, in guest heights)
RFV, BFV = 0.25, 0.026                      # the fuller ring of the ancient guest and of its free relative (26 beads)
R40V, B40V = 0.28, 0.0205                   # the schematic 40-bead ring
A26 = [TAU * i / 26 for i in range(26)]
ARMS_TOP = [(70, 1.0, 0.0), (110, 1.0, 2.1), (38, 0.75, 4.0), (142, 0.75, 1.2)]     # four thin arms at the host's top


class VRing(Ring):
    """A bead ring that can also slide along its host (du, in host lengths): used when the ring doubles."""
    du = 0.0

    def geom(self):
        c = self.host.anchor(self.du, self.dv)
        s = self.host.size()
        return c, lerp(self.Rk, self.Rk2, self.tight) * s, lerp(self.brk, self.brk2, self.tight) * s


class O2Fall(Proc):
    """Oxygen arriving on the yellow row; every landing pops a yellow spark. It falls in from the TOP of the
    frame, or (side_in) drops in from the two SIDES below the bean, onto the close-up strip of the row.
    A function of film time (t0), so the fall carries across cuts. stop: film time after which none sets out."""

    def __init__(self, guest, t0, n=6, gap=0.6, travel=1.8, seed=0, z=-3, side_in=False):
        self.g, self.t0, self.n, self.gap, self.travel, self.seed, self.a = guest, t0, n, gap, travel, seed, 1.0
        self.side_in, self.stop = side_in, None
        self.tok = [o2_token(0.34).scale(1.25) for _ in range(n)]
        self.pop = [star(0.19) for _ in range(n)]
        self.h0 = self.tok[0].height
        self.top = FH / 2 + 0.7
        self.mob = VGroup(*self.tok, *self.pop).set_z_index(z)
        for m in self.mob:
            m.set_opacity(0)
        self._ko, self._kp = [None] * n, [None] * n
        self._live()

    def draw(self):
        t = now() - self.t0
        P = self.n * self.gap
        for i in range(self.n):
            tk, pp = self.tok[i], self.pop[i]
            lt = t - i * self.gap
            cyc = math.floor(lt / P) if lt >= 0 else -1
            age = lt - cyc * P if lt >= 0 else -1.0
            if self.stop is not None and self.t0 + i * self.gap + cyc * P > self.stop:
                age = -1.0
            u = (0.37 * (i + 1) + 0.23 * cyc + 0.31 * self.seed) % 1.0
            side = 1.0 if (i + cyc + self.seed) % 2 else -1.0
            land = self.g.rowpoint(0.5 + side * (0.12 + 0.28 * u))
            x0 = side * (2.05 + 1.0 * ((i * 0.61 + cyc * 0.29 + 0.17 * self.seed) % 1.0))
            o = 0.0
            if 0 <= age < self.travel:
                s = age / self.travel
                e = s ** 1.35
                start = np.array([x0, self.top, 0.0])
                ctl = np.array([x0, lerp(self.top, land[1], 0.7), 0.0])
                if self.side_in:
                    u2 = (i * 0.61 + cyc * 0.29 + 0.17 * self.seed) % 1.0
                    start = np.array([side * (FW / 2 + 0.7), land[1] + 0.9 + 0.8 * u2, 0.0])
                    ctl = np.array([side * 3.2, land[1] + 1.25, 0.0])
                p = (1 - e) ** 2 * start + 2 * (1 - e) * e * ctl + e ** 2 * land
                o = round(self.a * min(1.0, (1 - s) / 0.08), 2)
                tk.scale_to_fit_height(self.h0 * (1.0 - 0.6 * max(0.0, (s - 0.7) / 0.3)))
                tk.move_to(p)
            if self._ko[i] != o:
                tk.set_opacity(o)
                tk[0].set_fill(opacity=0.16 * o)
                self._ko[i] = o
            po = 0.0
            if self.travel <= age < self.travel + 1.2:
                s = (age - self.travel) / 1.2
                po = round(self.a * min(1.0, s / 0.08) * min(1.0, (1 - s) / 0.4), 2)
                e = s ** 0.7
                pp.move_to(land + np.array([side * 0.3 * e, (0.25 + 0.5 * self.g.H) * e, 0.0]))
            if self._kp[i] != po:
                pp[0].set_fill(opacity=0.18 * po)
                pp[1].set_fill(opacity=po)
                self._kp[i] = po


class Strip(Proc):
    """The yellow row, close up, under the bean: the same 20 blocks, the same 13 pink tiles and the same running
    spark as on the bean's inner edge, drawn big enough to see oxygen land on it. It opens out of the row
    (open 0..1) and two thin pink lines tie it to the row it magnifies. Schematic blocks: no structure."""

    def __init__(self, guest, x=0.0, y=-1.3, w=6.9, h=1.4, z=-4):
        self.g, self.x, self.y, self.w, self.h, self.a, self.open = guest, x, y, w, h, 0.0, 1.0
        self.H = 1.5                                   # O2Fall reads this: how high a landing spark jumps
        self.ties = VMobject(fill_opacity=0)
        self.panel = VMobject(fill_color="#0B1C2B")
        self.glow = VMobject(fill_opacity=0)
        self.blocks = VMobject(stroke_width=0, fill_color=YELLOW)
        self.hot = VMobject(stroke_width=0, fill_color="#FFF7C2")
        self.tilem = VMobject(stroke_color="#FFE3EC", stroke_width=2, fill_color=PINK)
        self.mob = VGroup(self.ties, self.panel, self.glow, self.blocks, self.hot, self.tilem).set_z_index(z)
        self._c = np.zeros((Guest.NB, 3))
        self._bh = 0.5
        self._live()

    def rowpoint(self, f):
        """A point on top of the close-up row, f in 0..1 from its left end to its right end."""
        f = min(1.0, max(0.0, f)) * (Guest.NB - 1)
        i = min(Guest.NB - 2, int(f))
        return lerp(self._c[i], self._c[i + 1], f - i) + np.array([0.0, self._bh / 2, 0.0])

    def draw(self):
        g, a, k, NB = self.g, max(0.0, self.a) * max(0.0, self.g.a), self.open, Guest.NB
        r0, r1 = g.rowpoint(0.0), g.rowpoint(1.0)
        cx, cy = lerp(0.5 * (r0[0] + r1[0]), self.x, k), lerp(0.5 * (r0[1] + r1[1]), self.y, k)
        w, h = lerp(abs(r1[0] - r0[0]) * 1.1, self.w, k), lerp(0.14 * g.H, self.h, k)
        pitch = w * 0.88 / (NB - 1)
        bw, bh, yb = 0.55 * pitch, 0.42 * h, cy - 0.06 * h
        self._bh = bh
        self._c = np.stack([cx + np.linspace(-0.5, 0.5, NB) * w * 0.88, np.full(NB, yb), np.zeros(NB)], 1)
        if a < 0.01:
            for m in self.mob:
                m.set_stroke(opacity=0)
                m.set_fill(opacity=0)
            return
        box = lambda c, kx=1.0, ky=1.0: np.array([[c[0] - bw / 2 * kx, c[1] - bh / 2 * ky, 0], [c[0] + bw / 2 * kx, c[1] - bh / 2 * ky, 0],
                                                  [c[0] + bw / 2 * kx, c[1] + bh / 2 * ky, 0], [c[0] - bw / 2 * kx, c[1] + bh / 2 * ky, 0],
                                                  [c[0] - bw / 2 * kx, c[1] - bh / 2 * ky, 0]])
        tl, tr = np.array([cx - w / 2, cy + h / 2, 0]), np.array([cx + w / 2, cy + h / 2, 0])
        self.panel.set_points_as_corners([tl, tr, [cx + w / 2, cy - h / 2, 0], [cx - w / 2, cy - h / 2, 0], tl])
        self.panel.set_fill(opacity=0.92 * a)
        self.panel.set_stroke(PINK, width=3.5, opacity=a)
        self.ties.set_points(poly_pts([[r0, tl], [r1, tr]]))
        self.ties.set_stroke(PINK, width=2.5, opacity=0.6 * a * k)
        self.blocks.set_points(poly_pts([box(c) for c in self._c]))
        self.blocks.set_fill(interpolate_color(ManimColor(YELLOW), ManimColor("#FFF7C2"), 0.5 * g.rowglow), opacity=a)
        self.glow.set_points_as_corners(self._c)
        self.glow.set_stroke(YELLOW, width=60 * bh, opacity=0.22 * a * g.rowglow)
        f = ((now() / 2.2 + 0.13 * g.ph) % 1.0) if g.surge < 0 else g.surge       # the same running spark as on the bean
        sa = a * g.chain * (g.spark if g.surge < 0 else 1.0)
        if sa > 0.01:
            j = f * (NB - 1)
            self.hot.set_points(poly_pts([box(self._c[i], 1.2, 1.12) for i in range(NB) if abs(i - j) < 1.3]))
            self.hot.set_fill(opacity=sa)
        else:
            self.hot.set_fill(opacity=0)
        nt = int(round(g.tiles))
        if nt > 0:
            self.tilem.set_points(poly_pts([box(0.5 * (self._c[j] + self._c[j + 1]), 0.58, 0.9) for j in Guest.GAPS[:min(13, nt)]]))
            self.tilem.set_fill(opacity=a)
            self.tilem.set_stroke(opacity=a)
        else:
            self.tilem.set_fill(opacity=0)
            self.tilem.set_stroke(opacity=0)


# ───────────────────────────── presets: the tall world's named states ─────────────────────────────
HOME = dict(    # the modern cell, pulled back: guest above, nucleus below
    cell=dict(x=0.0, y=1.5, w=6.8, h=7.4, arm=0.0, a=1.0, sq=3.0, wob=1.0, warm=0.0),
    nuc=dict(x=0.0, y=-0.75, r=1.2, solid=1.0, sdraw=1.0, dash=0.0, ddraw=1.0, q=0.0, a=1.0),
    nring=dict(a=1.0, pk=0.0),
    g=dict(x=0.0, y=3.1, L=4.6, H=2.4, bean=1.0, fold=0.4, a=1.0, detail=1.0, chain=1.0, spark=1.0, ang=0.0, sil=0.0,
           tiles=0.0, rowglow=0.0, pinch=0.0),
    r13=dict(a=1.0), rfull=dict(a=0.0), rlm=dict(a=0.0), rk=dict(a=0.0, tight=0.0), sparks=dict(a=0.0),
)
BIG = mix(HOME, cell=dict(y=0.0, w=17.0, h=22.0, a=0.55), nuc=dict(y=-12.5, r=2.2), g=dict(y=1.6, L=6.6, H=3.8))   # frame one: no rim in frame
HOME_ROD = mix(HOME, g=dict(bean=0.0, fold=0.0), r13=dict(a=0.0), rfull=dict(a=1.0))                              # the ancestor's shape, held
ANC = mix(HOME, cell=dict(y=-0.45, w=6.2, h=5.0, arm=1.0, sq=2.5),                                             # rewound: two strangers
          nuc=dict(x=-1.15, y=-1.25, r=1.05, solid=0.0, dash=1.0, q=1.0),
          g=dict(y=3.3, L=3.0, H=1.4, bean=0.0, fold=0.0), r13=dict(a=0.0), rfull=dict(a=1.0))
PAIR = mix(ANC, cell=dict(y=1.0, w=6.6, h=7.0, arm=0.3), nuc=dict(x=-1.0, y=-0.7, r=1.15), g=dict(y=2.2, L=3.6, H=1.75))
RIM = dict(x=0.0, y=0.0, w=7.9, h=14.1, arm=0.0, a=0.75, sq=7.0, wob=0.3)                                        # the cell swollen past the frame
MITO, REL = dict(x=0.0, y=3.3, L=5.6, H=2.6), dict(x=0.0, y=-0.55, L=5.2, H=2.2)
PROOF = mix(PAIR, cell=RIM, nuc=dict(x=-7.0), g=dict(bean=1.0, detail=0.0, chain=0.0, spark=0.0, sil=1.0, **MITO), rfull=dict(a=0.0))
HL, HLR, HX, HXR = 5.6 / 2 * 1.04, 5.2 / 2 * 1.04, 1.56, 1.47                                                     # the halves after dividing
GEN = mix(HOME, cell=dict(y=1.15, w=7.0, h=6.8), nuc=dict(x=-0.45, r=1.1), nring=dict(pk=1.0), g=dict(y=2.75, L=5.4, H=3.0),   # room above for the tag
          r13=dict(a=0.0), rlm=dict(a=1.0), rk=dict(a=1.0))
GEN13 = mix(GEN, rlm=dict(a=0.0), rk=dict(tight=1.0))
THIRT = mix(GEN13, cell=RIM, nuc=dict(a=0.0), g=dict(y=2.35, L=7.0, H=4.0))      # pushed in on the bean; the nucleus fades in place; the strip opens below
PAY = mix(THIRT, g=dict(tiles=13.0, rowglow=0.8), sparks=dict(a=1.0))

Y_TOP, Y_MID, Y_FOOT = 5.1, 1.18, -2.75     # label bands: above the subject, between guest and nucleus, under the close-up strip
MAX_W = 6.7                                 # 84% of the frame width: nothing wider (platform buttons sit at the right edge)
END_LINES = ["Your mitochondria descend", "from a bacterium that", "moved in and never left."]


def _audio_dir():
    a = Path(os.environ.get("KX_AUDIO", "audio_social"))
    return a if a.is_absolute() else Path(__file__).resolve().parent / a


def spoken_at(sid, phrase):
    """Seconds into scene `sid` at which a phrase is spoken (to place film-time events from another scene)."""
    try:
        words = json.loads((_audio_dir() / "words.json").read_text())[sid]
    except Exception:
        return 0.0
    wl = [(float(w[0]), bp_style._norm(w[2])) for w in words]
    toks = [bp_style._norm(p) for p in phrase.split()]
    for i in range(len(wl) - len(toks) + 1):
        if [x[1] for x in wl[i:i + len(toks)]] == toks:
            return wl[i][0]
    return 0.0


O2_T0 = T0.get("s04_thirteen", 0.0) + spoken_at("s04_thirteen", "using oxygen") - 0.3     # film time the first oxygen starts to fall
O2_T1 = T0.get("s05_payoff", 0.0) + spoken_at("s05_payoff", "every breath") - 0.2         # ... and when the fall thickens


class VWorld:
    """The carried world, tall: backdrop, specks, host (arms at its top), nucleus, guest and its rings."""

    def __init__(self, scene, preset):
        scene.add(make_backdrop())
        start_clock(scene)
        self.specks = Specks(n=70)
        self.cell = Cell(arms=ARMS_TOP, arm_len=1.25)
        self.shim = Shimmer(self.cell)
        self.nuc = Nucleus()
        half = TAU / 36
        angs = [TAU * i / 18 for i in range(18)] + [TAU * k / 18 + half for k in PINK_SLOTS]
        self.nring = Ring(self.nuc, angs, [BLUE] * 18 + [PINK] * 12, Rk=0.62, brk=0.05, dv=0.0, period=24.0, z=-38,
                          groups=[None] * 18 + ["pk"] * 12)
        self.nring.pk = 0.0
        self.g = Guest(n=150)
        ring = lambda angles, Rk, brk: VRing(self.g, angles, PINK, Rk, brk, dv=DV, period=PER)
        self.r13, self.rfull = ring(A13, R13V, B13V), ring(A26, RFV, BFV)
        self.rlm, self.rk = ring(A40[LOST + MOVED], R40V, B40V), ring(KEPT_A, R40V, B40V)     # 15 lost + 12 moved, and the 13 kept
        self.rk.ang2, self.rk.Rk2, self.rk.brk2 = A13, R13V, B13V
        self.sparks = Sparks(self.g, self.cell, n=14, labels=0)
        self.objs = dict(cell=self.cell, nuc=self.nuc, nring=self.nring, g=self.g, r13=self.r13, rfull=self.rfull, rlm=self.rlm,
                         rk=self.rk, sparks=self.sparks)
        self.set(preset)
        for o in (self.specks, self.cell, self.shim, self.nuc, self.nring, self.g, self.r13, self.rfull, self.rlm, self.rk, self.sparks):
            o.draw()
            scene.add(o.mob)

    def set(self, preset):
        for k, d in preset.items():
            self.objs[k].set(**d)
        return self

    def to(self, preset, rt=1.5, rate=smooth, only=None, skip=()):
        return [self.objs[k].tw(rt, rate, **d) for k, d in preset.items() if (only is None or k in only) and k not in skip]

    def cradle(self):
        """Arms 0 and 1 reach up round the ends of the guest and hook over it; as it is drawn down inside
        they close above it."""
        c, g = self.cell, self.g
        top = lambda: c.y + 0.5 * c.h

        def hug(sign):
            def f():
                e = min(1.0, max(0.0, (top() + 0.7 - g.cy) / 2.0))
                gc = g.center()
                tip = lerp(gc + np.array([sign * 0.18 * g.L, 0.6 * g.H, 0]), np.array([sign * 0.05, top() + 0.2, 0]), e)
                ctl = lerp(gc + np.array([sign * (0.56 * g.L + 0.6), 0.1 * g.H, 0]), np.array([sign * 0.9, top() + 0.45, 0]), e)
                return ctl, tip
            return f
        c.hug[0], c.hug[1] = hug(1), hug(-1)


class VMixin:
    def world(self, preset):
        self.W = VWorld(self, preset)
        return self.W

    def bg(self, f):
        """Run f(scene seconds) every frame without blocking the cue line."""
        m = VMobject()
        m.add_updater(lambda _m, dt: f(self.elapsed()))
        self.add(m)
        return m


class VStage(VMixin, SpokenScene):
    def gap(self, phrase, lead=0.2, nth=0, floor=0.3):
        return max(floor, self.t_of(phrase, nth) - lead - self.elapsed())

    def rest(self, back=0.0):
        return max(0.05, self.narration_s + 0.4 - self.elapsed() - back)


# ───────────────────────────── labels and small parts ─────────────────────────────
ANCESTOR = lambda: label("ancestor: a bacterium", 40, PINK, (0, Y_MID), weight=SEMIBOLD)
STAYED = lambda: label("it stayed", 48, PINK, (0, 3.65), weight=BOLD)
TOP_MITO = lambda: label("mitochondrion", 36, PINK, (0, Y_TOP))
TOP_MOST = lambda: T("most mitochondria", size=36, weight=MEDIUM, t2c={"mitochondria": PINK}).move_to([0, Y_TOP, 0]).set_z_index(20)
FREE_REL = lambda: label("free relative", 36, TEXT, (0, -2.2))
CLUE = lambda text: label(text, 40, TEXT, (0, 1.37), weight=SEMIBOLD)
SCHEM = lambda: fit(label("schematic: not a gene count", 34, TEXT, (0, 5.05)), max_w=MAX_W)      # top of the frame, clear of the captions
NUCL = lambda: label("nucleus", 36, BLUE, (1.85, -0.75), weight=SEMIBOLD)
THIRTEEN = lambda: label("13 proteins", 44, PINK, (0, 5.12), weight=SEMIBOLD)
ENERGY = lambda: label("energy from food", 40, YELLOW, (0, Y_FOOT), weight=SEMIBOLD)
INHERITED = lambda: label("from the ancient guest", 40, PINK, (0, Y_FOOT), weight=SEMIBOLD)
POINTER = lambda: Arrow([0, -2.5, 0], [0, -2.04, 0], buff=0, color=PINK, stroke_width=6, max_tip_length_to_length_ratio=0.45).set_z_index(20)
COUNT_AT = lambda g: g.anchor(0.0, DV)


def link_bar():
    """The green link between the mitochondrion and its free relative, and its three notches (one per clue)."""
    x = -3.3
    bar = VMobject(stroke_color=GREEN, stroke_width=7, fill_opacity=0).set_points_as_corners(
        [[-2.9, MITO["y"], 0], [x, MITO["y"], 0], [x, REL["y"], 0], [-2.72, REL["y"], 0]]).set_z_index(18)
    notches = VGroup(*[Line([x, y, 0], [x + 0.5, y, 0], color=GREEN, stroke_width=10) for y in (2.0, 1.37, 0.74)]).set_z_index(18)
    return bar, notches


def free_relative(**kw):
    return Guest(**{**dict(bean=0.0, detail=0.0, seed=2.3, sil=1.0, **REL), **kw})


def count_texts(pos):
    return VGroup(*[M(str(i + 1), size=60, color=TEXT).move_to(pos).set_opacity(0) for i in range(13)]).set_z_index(20)


# ═════════════════════════════ scenes ═════════════════════════════
class S00Hook(VStage):
    def construct(self):
        W = self.world(mix(BIG, g=dict(L=6.6 * 0.93, H=3.8 * 0.93)))
        g = W.g
        q = T("?", size=120, color=TEXT, weight=BOLD).set_z_index(20)
        q.add_updater(lambda m, dt: m.move_to(g.anchor(0.262, 0.0)))
        pulse(q, 0.09, 1.6)
        q.update(0)
        self.add(q)

        def ease_in(t):                                    # frame one is already moving: the bean swells toward the viewer
            if t < 2.3:
                s = 0.93 + 0.07 * (1 - (1 - t / 2.3) ** 3)
                g.L, g.H = 6.6 * s, 3.8 * s
        mover = self.bg(ease_in)
        lab = label("mitochondrion", 44, PINK, (0, 4.25), weight=SEMIBOLD)
        self.at("your mitochondria")
        self.play(Write(lab, run_time=0.7), g.tw(0.9, there_and_back, lit=0.6))
        self.at("own DNA")
        own = label("its own DNA", 48, PINK, (0, 4.25), weight=SEMIBOLD)
        self.play(W.r13.tw(1.3, there_and_back, lit=1.0), FadeOut(lab, run_time=0.3), Succession(Wait(0.15), FadeIn(own, run_time=0.4)))     # a cross-fade: no scrambled letters
        lab = own
        self.at("Because", lead=0.35)
        self.remove(mover)
        q.clear_updaters()
        self.play(FadeOut(q, scale=0.4, run_time=0.4), FadeOut(lab, shift=UP * 0.4, run_time=0.4), *W.to(HOME, 1.25, only=("cell", "nuc", "g")))
        self.at("free living", lead=0.35)
        anc = ANCESTOR()
        self.play(g.tw(0.6, bean=0.0, fold=0.0), W.r13.tw(0.5, a=0.0), W.rfull.tw(0.5, a=1.0), Write(anc, run_time=0.7))
        self.play(g.tw(1.0, there_and_back, lit=0.7))      # the rod holds to the end of the scene, under its label
        self.finish()


class S01Enclose(VStage):
    def construct(self):
        W = self.world(HOME_ROD)
        g, c = W.g, W.cell
        W.cradle()
        anc = ANCESTOR()
        self.add(anc)
        big = label("larger cell", 36, BLUE, (0.55, 0.95), weight=SEMIBOLD)       # names for a viewer with the sound off
        bac = label("bacterium", 36, PINK, (0, 4.58), weight=SEMIBOLD)
        # the rewind, in one move: the rod (fuller ring) rises out through the top; nucleus to a dashed circle with a gold "?"
        self.play(FadeOut(anc, run_time=0.4), *W.to(ANC, 1.5, only=("cell", "nuc", "g", "r13", "rfull")),
                  Succession(Wait(0.9), AnimationGroup(Write(big, run_time=0.6), Write(bac, run_time=0.6))))
        self.at("somehow")
        how = VGroup(gold_badge(0.3), label("how? one proposed way", 36, GOLD, (0, 0), weight=SEMIBOLD))
        fit(how.arrange(RIGHT, buff=0.18), max_w=MAX_W).move_to([0, 5.32, 0]).set_z_index(20)
        self.play(c.tw(0.75, grab=[1.0, 1.0, 0, 0]), FadeIn(how, shift=DOWN * 0.15, run_time=0.6))
        pulse(how[0])
        self.at("enclose", lead=0.35)
        c.flinch(90, 0.05)
        self.play(g.tw(1.5, y=0.85), Succession(Wait(0.8), c.tw(0.7, linear, sweep=1.0)),
                  FadeOut(big, run_time=0.5), Succession(Wait(0.5), FadeOut(bac, run_time=0.5)))       # the names go as the arms close
        c.sweep = 0.0
        # the arms close and relax; the gold phrase goes (the small "?" stays on the dashed circle); the pair grows
        how[0].clear_updaters()
        self.play(c.tw(0.6, grab=[0, 0, 0, 0]), FadeOut(how, run_time=0.5), *W.to(PAIR, 1.0, only=("cell", "nuc", "g")))
        self.at("a meal", lead=0.45)
        ghost = rod_outline(g.cx, g.cy, g.L, g.H, color="#9AA3B2", width=4)        # the fate that did NOT happen
        ghost[0].set_stroke(GREY, opacity=0.12)
        gp = np.array([1.45, -1.2, 0.0])                                           # lower right, clear of the nucleus and its "?"
        ghost.generate_target()
        ghost.target.scale(0.55).move_to(gp)
        self.add(ghost)
        self.play(MoveToTarget(ghost, run_time=0.7, path_arc=-1.4))
        rng = random.Random(8)
        bits = VGroup(*[Dot(gp + np.array([1.0 * math.cos(a), 0.42 * math.sin(a), 0]), radius=rng.uniform(0.06, 0.11), color=GREY)
                        for a in np.linspace(0, TAU, 18, endpoint=False)]).set_z_index(12)
        self.play(FadeOut(ghost, run_time=0.45), FadeIn(bits, run_time=0.3),
                  *[b.animate(run_time=1.0, rate_func=rush_from).shift([rng.uniform(-0.3, 0.3), rng.uniform(-0.45, -0.05), 0]).scale(0.5) for b in bits])
        self.at("instead", lead=0.2)
        self.play(FadeOut(bits, run_time=0.7), c.tw(1.2, there_and_back, lit=0.4))
        self.at("stayed", lead=0.45)
        self.play(g.tw(1.3, there_and_back, lit=1.0), Write(STAYED(), run_time=0.7))
        self.finish()


class S02Proof(VStage):
    def construct(self):
        W = self.world(PAIR)
        g, c, nuc = W.g, W.cell, W.nuc
        stay = STAYED()
        rel = free_relative(x=7.6)
        A2, B2 = Guest(a=0.0, n=140, seed=3.1), Guest(a=0.0, seed=4.2)
        ring = lambda host: VRing(host, A26, PINK, RFV, BFV, dv=DV, period=PER, a=0.0)
        rA, rB, rA2, rB2 = W.rfull, ring(rel), ring(g), ring(rel)
        self.add(stay, rel.mob, A2.mob, B2.mob, rB.mob, rA2.mob, rB2.mob)
        ml, rl = TOP_MITO(), FREE_REL()
        bar, notches = link_bar()
        # push in: the outline swells past the frame; the guest of long ago is the mitochondrion of today, above its free relative
        self.play(FadeOut(stay, run_time=0.4), *W.to(PROOF, 1.5, only=("cell", "g", "rfull")), nuc.tw(1.2, x=-7.0),
                  rel.tw(1.5, rush_from, x=REL["x"]), Succession(Wait(0.8), Write(ml, run_time=0.6)),
                  Succession(Wait(1.0), FadeIn(rl, shift=UP * 0.15, run_time=0.5)))
        self.play(Create(bar, run_time=0.8))
        self.at("Most mitochondria", lead=0.3)
        self.play(Transform(ml, TOP_MOST(), run_time=0.6), g.tw(0.8, there_and_back, lit=0.4))
        self.at("two membranes")
        w = CLUE("two membranes")
        self.play(g.tw(0.8, detail=1.0, sil=0.25), rel.tw(0.8, detail=1.0, sil=0.25), g.tw(1.2, there_and_back, lit=0.8),
                  rel.tw(1.2, there_and_back, lit=0.8), Write(w, run_time=0.7), Create(notches[0], run_time=0.5))
        self.at("own DNA")
        self.play(rA.tw(0.6, a=1.0), rB.tw(0.6, a=1.0), rA.tw(1.3, there_and_back, lit=1.0), rB.tw(1.3, there_and_back, lit=1.0),
                  Transform(w, CLUE("own DNA"), run_time=0.6), Create(notches[1], run_time=0.5))
        self.at("They even", lead=0.1)
        rA2.a = rB2.a = 1.0                                 # each ring doubles, and the two copies slide apart
        self.play(rA.tw(0.8, du=-0.25), rA2.tw(0.8, du=0.25), rB.tw(0.8, du=-0.25), rB2.tw(0.8, du=0.25),
                  Transform(w, CLUE("divide by pinching"), run_time=0.7))
        self.play(g.tw(0.7, rush_into, pinch=1.0), rel.tw(0.7, rush_into, pinch=1.0))
        split(g, A2)
        split(rel, B2)
        rA2.host, rB2.host = A2, B2
        rA.du = rA2.du = rB.du = rB2.du = 0.0
        self.play(g.tw(0.8, x=-HX), A2.tw(0.8, x=HX), rel.tw(0.8, x=-HXR), B2.tw(0.8, x=HXR), Create(notches[2], run_time=0.5))
        self.play(*[h.tw(0.7, there_and_back, lit=0.5) for h in (g, A2, rel, B2)])
        self.finish()


class S03Genes(VStage):
    def construct(self):
        W = self.world(mix(PROOF, g=dict(x=-HX, L=HL, detail=1.0, sil=0.25), rfull=dict(a=1.0)))
        g, c, nuc, nr, rlm, rk = W.g, W.cell, W.nuc, W.nring, W.rlm, W.rk
        nr.pk = 1.0
        nr.ba[18:30] = 0.0
        half = dict(bean=1.0, detail=1.0, sil=0.25, y=MITO["y"], L=HL, H=MITO["H"])
        A2 = Guest(x=HX, seed=3.1, **half)
        R1 = free_relative(x=-HXR, L=HLR, detail=1.0, sil=0.25)
        R2 = free_relative(x=HXR, L=HLR, detail=1.0, sil=0.25, seed=4.2)
        rings = [VRing(h, A26, PINK, RFV, BFV, dv=DV, period=PER) for h in (A2, R1, R2)]
        bar, notches = link_bar()
        old = VGroup(TOP_MOST(), CLUE("divide by pinching"), FREE_REL(), bar, notches)
        tag = SCHEM()
        fall = gold_badge(0.24).set_z_index(21).set_opacity(0)
        self.add(A2.mob, R1.mob, R2.mob, *[r.mob for r in rings], old, fall)
        nuc.set(solid=1.0, sdraw=0.0, a=0.0, **{k: GEN["nuc"][k] for k in "xyr"})      # it fades in where it belongs: nothing slides across the relatives
        st = {}

        def drop(a):                                        # the gold "?" lets go of the circle as it draws solid
            if not st:
                if a <= 0:
                    return
                st["p"] = nuc.badge.get_center().copy()
                nuc.q = 0.0
            fall.move_to(st["p"] + DOWN * 1.1 * a * a)
            fall.set_opacity(1 - a)
            fall[0].set_fill(opacity=0.14 * (1 - a))
        # pull back: the relatives drop away, one half drifts off, the other is the organelle; the host is back around it
        self.play(FadeOut(old, run_time=0.4), R1.tw(0.9, rush_into, x=-8.5), R2.tw(0.9, rush_into, x=8.5), A2.tw(1.1, rush_into, x=4.5, y=9.0),     # out sideways, never through the caption band
                  *W.to(mix(GEN, g=dict(bean=1.0, sil=0.0, chain=1.0, spark=1.0, detail=1.0)), 1.5, only=("cell", "g")),
                  W.rfull.tw(0.6, a=0.0), Succession(Wait(0.5), AnimationGroup(rlm.tw(0.8, a=1.0), rk.tw(0.8, a=1.0))),
                  Succession(Wait(0.5), nuc.tw(0.4, a=1.0)), Succession(Wait(0.9), AnimationGroup(nuc.tw(0.7, sdraw=1.0), nuc.tw(0.7, dash=0.0), Tw(drop, 0.7, linear))),
                  Succession(Wait(0.8), FadeIn(tag, shift=DOWN * 0.1, run_time=0.6)))
        self.remove(A2.mob, R1.mob, R2.mob, *[r.mob for r in rings], fall)
        self.at("were lost", lead=0.25)

        def lose(i):
            b, s0 = rlm.beads[i], {}

            def f(a):
                if not s0:
                    if a <= 0:
                        return
                    rlm.live[i] = False
                    cc, _, br = rlm.geom()
                    d = b.get_center() - cc
                    s0["p"], s0["d"], s0["r"] = b.get_center(), d / (np.linalg.norm(d) + 1e-9), br
                p = s0["p"] + s0["d"] * 0.75 * (1 - (1 - a) ** 2) + np.array([0.0, -0.3 * a * a, 0.0])
                b.set_points(circ(p, s0["r"] * (1 + 0.8 * min(1.0, a * 4))))
                b.set_fill(interpolate_color(ManimColor(PINK), ManimColor("#A9B1BF"), min(1.0, a * 4)), opacity=min(1.0, 2.5 * (1 - a)))
            return Tw(f, 1.4, linear)
        self.play(LaggedStart(*[lose(i) for i in range(15)], lag_ratio=0.12, run_time=self.gap("others moved", lead=0.2)))
        nl = NUCL()

        def move(i, j):
            b, s0 = rlm.beads[i], {}

            def f(a):
                if not s0:
                    if a <= 0:
                        return
                    rlm.live[i] = False
                    s0["p"] = b.get_center()
                tgt = nr.pos(18 + j)
                p = np.array([lerp(s0["p"][0], tgt[0], smooth(a)), lerp(s0["p"][1], tgt[1], a ** 1.3), 0.0])      # they FALL
                b.set_points(circ(p, lerp(B40V * g.H, nr.geom()[2], a) * (1 + 2.2 * math.sin(PI * a))))
                if a >= 1:
                    b.set_fill(opacity=0)
                    nr.ba[18 + j] = 1.0
            return Tw(f, 1.0, linear)
        self.play(LaggedStart(*[move(15 + j, j) for j in range(12)], lag_ratio=0.1, run_time=self.gap("But it kept", lead=0.4)),
                  Write(nl, run_time=0.7), Succession(Wait(1.2), nuc.tw(1.2, there_and_back, lit=0.6)))
        self.at("small genome", lead=0.35)
        self.play(rk.tw(1.1, tight=1.0), rlm.tw(0.5, a=0.0))
        self.play(rk.tw(1.2, there_and_back, lit=0.45), g.tw(1.2, there_and_back, lit=0.4))
        self.finish()


class S04Thirteen(VStage):
    def construct(self):
        W = self.world(GEN13)
        g, rk = W.g, W.rk
        tag, nl = SCHEM(), NUCL()
        strip = Strip(g)
        strip.open = 0.0
        self.add(tag, nl, strip.mob)
        # push in on the bean; the nucleus fades in place; the row opens out below the bean as a close-up strip
        self.play(FadeOut(nl, run_time=0.4), *W.to(THIRT, 1.25, only=("cell", "g")), W.nuc.tw(0.5, a=0.0),
                  Succession(Wait(0.45), AnimationGroup(strip.tw(0.8, open=1.0), strip.tw(0.4, a=1.0))))
        self.at("that DNA")
        self.play(rk.tw(1.0, there_and_back, lit=0.8))
        self.at("13 proteins", lead=0.4)
        nums = count_texts(COUNT_AT(g))
        self.add(nums)

        def count(a):
            k = min(12, int(a * 13))
            rk.hl[:] = 0
            if a < 1:
                rk.hl[k] = 1.0
            for i, n in enumerate(nums):
                n.set_opacity(1.0 if i == k else 0.0)
        top = THIRTEEN()
        self.play(Tw(count, 1.5, linear), FadeOut(tag, run_time=0.5), Succession(Wait(0.8), Write(top, run_time=0.7)))
        self.at("All 13", lead=0.3)
        tiles = VGroup(*[Rectangle(width=0.1, height=0.3, stroke_color="#FFE3EC", stroke_width=1.5, fill_color=PINK, fill_opacity=1)
                         .move_to(rk.pos(i)).set_z_index(-7) for i in range(13)]).set_opacity(0)
        self.add(tiles)

        def fly(k):
            tile, s0 = tiles[k], {}

            def f(a):
                if not s0:
                    if a <= 0:
                        return
                    s0["p"] = rk.pos(k)
                    rk.hl[k] = 1.0
                    tile.set_opacity(1)
                tile.move_to(s0["p"] + (g.gappos(k) - s0["p"]) * a + np.array([0.3 * math.sin(PI * a), 0, 0]))
                rk.hl[k] = max(0.0, 1 - 2 * a)
                if a >= 1:
                    tile.set_opacity(0)
                    g.tiles = max(g.tiles, k + 1)           # the strip shows the same tile arrive, close up
            return Tw(f, 0.55)
        self.play(LaggedStart(*[fly(k) for k in range(13)], lag_ratio=0.1, run_time=self.gap("energy", lead=0.25)))
        self.at("energy", lead=0.2)
        g.surge = 0.0
        self.play(g.tw(0.8, linear, surge=1.0), g.tw(0.8, rowglow=0.8), W.sparks.tw(0.8, a=1.0), Write(ENERGY(), run_time=0.8))
        g.surge = -1.0
        o2 = O2Fall(strip, O2_T0, side_in=True)
        self.add(o2.mob)
        self.at("using oxygen", lead=0.1)
        self.play(g.tw(1.3, there_and_back, lit=0.35))
        self.finish()


def payoff_world(sc):
    """The bean with its 13 tiles, the close-up strip of its row, and oxygen dropping onto the strip from both sides."""
    W = sc.world(PAY)
    strip = Strip(W.g)
    strip.a = 1.0
    o2, o2b = O2Fall(strip, O2_T0, side_in=True), O2Fall(strip, O2_T1, n=5, gap=0.7, seed=3, side_in=True)
    sc.add(strip.mob, o2.mob, o2b.mob)
    return W, strip, o2, o2b


class S05Payoff(VStage):
    def construct(self):
        W, strip, o2, o2b = payoff_world(self)
        g = W.g
        num = M("13", size=60, color=TEXT).move_to(COUNT_AT(g)).set_z_index(20)
        top, en = THIRTEEN(), ENERGY()
        self.add(num, top, en)
        self.play(*[FadeOut(m, run_time=0.5) for m in (num, top, en)], g.tw(0.6, rowglow=1.0))
        self.at("delivers")
        self.play(g.tw(1.0, there_and_back, lit=0.3))
        self.at("inherited", lead=0.25)
        lab, ptr = INHERITED(), POINTER()
        self.play(Write(lab, run_time=0.9), GrowArrow(ptr, run_time=0.6))
        self.at("ancient guest", lead=0.2)
        self.play(g.tw(1.1, there_and_back, lit=0.45))
        self.at("moved in", lead=0.3)
        rod = rod_outline(g.x, g.y, 6.3, 2.8, width=7)
        self.add(rod)
        self.play(flicker(rod, 1.1))
        self.remove(rod)
        self.at("never left", lead=0.2)
        self.play(g.tw(1.6, there_and_back, lit=1.0))
        self.finish()


class S06End(VMixin, NarratedScene):
    """End card for a tall frame: the take-home line over the still-living bean at 10%. No new oxygen sets out."""

    def construct(self):
        W, strip, o2, o2b = payoff_world(self)
        g = W.g
        g.rowglow = 1.0
        o2.stop = o2b.stop = now() - 0.6
        lab, ptr = INHERITED(), POINTER()
        veil = Rectangle(width=FW + 1, height=FH + 1, stroke_width=0, fill_color=BG, fill_opacity=0).set_z_index(-1)
        self.add(lab, ptr, veil)
        lines = VGroup(*[T(t, size=44, font=TITLE_FONT) for t in END_LINES]).arrange(DOWN, buff=0.3)
        fit(lines, max_w=MAX_W)
        rule = Line(LEFT * 1.1, RIGHT * 1.1, color=GOLD, stroke_width=5)
        sub = T("Free at biochemistrypedia.com", size=34, color=TEAL, weight=SEMIBOLD)
        fit(sub, max_w=MAX_W - 0.3)
        VGroup(lines, rule, sub).arrange(DOWN, buff=0.55).move_to([0, 1.5, 0]).set_z_index(30)
        self.play(veil.animate(run_time=0.5).set_fill(opacity=0.90), FadeOut(lab, run_time=0.35), FadeOut(ptr, run_time=0.35),
                  FadeIn(lines, shift=UP * 0.25, run_time=0.6))
        self.play(GrowFromCenter(rule, run_time=0.4), FadeIn(sub, shift=UP * 0.12, run_time=0.5))
        self.play(sub.animate(run_time=1.2, rate_func=there_and_back).scale(1.04))
        self.finish()
