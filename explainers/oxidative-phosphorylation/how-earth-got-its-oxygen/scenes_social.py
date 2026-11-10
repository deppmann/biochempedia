"""Earth's Oceans Once Rained Rust (social cut, 9:16).

The web film's world turned on end for a tall frame, so the format does the work: bubbles go up,
rust comes down. Sky (with the O2 bar) above the sea, the sea above the sea floor. Everything is
drawn in world coordinates and the camera moves (close on the water for the hook and the stripes,
full height for the rest); the sea floor is held at screen y = -3.0 in every framing, so the band
y -4.6..-3.2 is always plain rock for the burned-in captions.

COLOR MAP: the web film's (scenes.py), unchanged. BLUE free oxygen, YELLOW electrons, GREEN
cyanobacteria, GREY takers that have not met oxygen, RED rust (only iron turns red), TEAL water,
GOLD sunlight. No PURPLE: the old microbes are not in this cut.

Honesty: the bar is schematic and says so whenever it is on screen; no cause is drawn for the rise;
the bar cross-fades to "today" (no sweep); today's sea has no dissolved-iron discs and no falling
flakes; two droplets, four electrons, one bubble; four iron discs to one bubble.

The builders (pip, iron_disc, hero_bubble, rust_flake, droplet, cyano_cell, pick_icon, bracket,
band_stack, soft_glow, plate, LBL, Zoom) and the palette are imported from scenes.py, so both cuts
share one look. Ambient motion is closed-form in film time and runs on across scene cuts.
"""
import json
import math
import os
import random
from pathlib import Path

import numpy as np
from bp_style import *
from scenes import (P, lerp, clip01, ease, hsh, band_stack, soft_glow, poly, pip, iron_disc, hero_bubble, rust_flake,
                    droplet, cyano_cell, bracket, pick_icon, plate, LBL, ochip, Zoom, SOCKET_ANG,
                    SKY_TOP, SKY_LOW, SEA_TOP, ROCK, ROCK_HI, LAND, SILICA)

_HERE = Path(__file__).resolve().parent
FW, FH = 8.0, 8.0 * 16 / 9

# ----------------------------------------------------------------------------- film clock
try:
    _IDS = [s["id"] for s in json.loads((_HERE / "social.json").read_text())["scenes"]]
    _DUR = json.loads((_HERE / "audio_social" / "durations.json").read_text())
except Exception:
    _IDS, _DUR = [], {}
T0, _t = {}, 0.0
for _k in _IDS:
    T0[_k] = _t
    _t += _DUR.get(_k, 0.0) + 0.4          # each segment is its narration + the 0.4 s tail

# ----------------------------------------------------------------------------- world geometry
SEA_Y, FLOOR_Y, LEDGE_Y = 2.6, -3.0, 0.75
XL, XR, YB, YT = -4.9, 4.9, -8.0, 12.8       # wide and tall enough for the pulled-back and tilted-up framings
STRIPE_H, N_STRIPE = 0.23, 7
SUN = P(3.1, 3.52)
SEA_MID = "#0A2A36"
LEDGE_TIP = -0.55
MAT_X0, MAT_X1 = -2.75, -0.72              # the whole mat is inside the safe width in the opening framing
WALL = [(XL, SEA_Y), (-2.2, SEA_Y), (-2.9, 2.1), (-3.3, 1.5), (-3.5, LEDGE_Y), (LEDGE_TIP, LEDGE_Y), (LEDGE_TIP + 0.24, LEDGE_Y - 0.2),
        (LEDGE_TIP - 0.1, LEDGE_Y - 0.6), (-1.5, LEDGE_Y - 0.85), (-2.9, LEDGE_Y - 0.9), (-3.5, LEDGE_Y - 1.5), (-3.8, -1.6),
        (-3.95, FLOOR_Y), (XL, FLOOR_Y)]
LANDPTS = [(XL, SEA_Y - 0.05), (XL, 3.74), (-3.4, 3.7), (-2.9, 3.35), (-2.2, SEA_Y - 0.05)]
BLOCKS = [P(-2.33, 3.0)]                        # land rock on the shore


def cam(z):
    """Framing at zoom z with the sea floor held at screen y = -3.0 (captions sit on plain rock below it)."""
    return (P(0, FLOOR_Y + 3.0 / z), FW / z)


FULL, DEEP, CLOSE = cam(1.0), cam(1.25), cam(1.5)
HOOK = cam(1.25)
# s05/s06: pulled back a little and tilted up, so the sky is about twice as tall on screen (surface at screen y = 1.6)
# and the sea floor is still above the caption band
SKY_Z = 0.85
SKYCAM = (P(0, 2.6 - 1.6 / SKY_Z), FW / SKY_Z)
# "Leftovers" and the end card: tilted up until the sky fills the upper half; the caption band is plain water
SKYEND = (P(0, 2.6 + 1.2 / SKY_Z), FW / SKY_Z)

# the O2 bar and its labels (world coordinates; read at the FULL framing)
G_X0, G_X1, G_Y, G_H, G_TICK = -3.45, 3.45, 4.66, 0.42, 2.85
G_IN = G_X0 + 0.06
G_SLIVER, G_LOW = 0.012, 0.14
ROW_A, ROW_B, ROW_C = 5.2, 4.1, 3.55
R3, RGOE, RNOW = "about 3 billion years ago", "about 2.4–2.1 billion years ago", "today"

N_FLAKE, N_IRON, N_BUB, N_PIP, N_LUMP = 72, 30, 16, 24, 15
N_HIGH = 44                                # pips of the high sky: seen only at "today", when the view tilts up
SWELL_C = P(0.0, 6.2)
PB = 4.2                                   # seconds for one bubble's trip
PIP_HOMES = [P(-2.05, 3.62), P(-1.3, 2.98), P(-0.2, 3.04), P(0.95, 2.96), P(2.4, 3.3), P(0.4, 2.93)]

STAGE0 = dict(cam=HOOK, hud=False, readout=None, tag2=False, arrow=False, blocks=False, dull=0,
              gauge=G_LOW, gauge2=0.0, pips=4.0, pips2=0.0, swell=0.0, flakes=1.0, iron=0.0, mat=1.0, bub=1.0, leak=0.25, stack=0.4,
              veil=0.0, veil2=0.0, pinned=True)
ST1 = dict(cam=FULL, hud=True, readout=R3, gauge=G_SLIVER, pips=0.0, flakes=0.0, iron=1.0, mat=0.0, bub=0.0, leak=0.0, stack=0.12)
ST2 = dict(ST1, mat=1.0, bub=1.0)
ST3 = dict(ST2, flakes=0.72)       # the hook shows the rain at full strength; with the iron discs on screen it is thinned
ST4 = dict(ST3, blocks=True, stack=float(N_STRIPE), cam=DEEP)
ST5 = dict(ST4, cam=SKYCAM, readout=RGOE, gauge=G_LOW, pips=5.0, tag2=True, arrow=True, leak=0.5, dull=1)
ST6 = dict(ST5, cam=SKYEND, hud=False, readout=RNOW, gauge2=1.0, pips=float(N_PIP), pips2=1.0, swell=1.0, iron=0.0, flakes=0.0, tag2=False,
           arrow=False, leak=1.0)


# ----------------------------------------------------------------------------- small helpers
def sw_scale(mob, s):
    """Scale a mobject about ORIGIN, strokes too."""
    mob.scale(s, about_point=ORIGIN)
    for fm in mob.get_family():
        w = fm.get_stroke_width()
        if w:
            fm.set_stroke(width=float(w) * s, family=False)
    return mob


def prep(m):
    """Remember a mobject's own opacities so seta() can fade it as a whole."""
    m._fam = [(f, float(f.get_fill_opacity()), float(f.get_stroke_opacity())) for f in m.family_members_with_points()]
    m._a = None
    return m


def seta(m, a):
    a = clip01(a)
    if m._a is not None and abs(m._a - a) < 0.004:
        return
    m._a = a
    for f, fo, so in m._fam:
        f.set_fill(opacity=fo * a, family=False)
        f.set_stroke(opacity=so * a, family=False)


def put(m, p):
    d = np.array(p, dtype=float) - m.get_center()
    if abs(d[0]) > 1e-6 or abs(d[1]) > 1e-6:
        m.shift(d)


def pill(text, size=34):
    t = T(text, size=size)
    box = RoundedRectangle(width=t.width + 0.36, height=0.56, corner_radius=0.2, stroke_color=TEXT, stroke_width=2.5,
                           fill_color=BG, fill_opacity=0.7)
    return VGroup(box, t.move_to(box))


def rewind_glyph():
    tri = lambda x: poly([(x + 0.3, 0.22), (x + 0.3, -0.22), (x, 0.0)], TEXT)
    return VGroup(tri(0.0), tri(0.36))


def bar_arrow():
    """The gap between the low level and today's, drawn inside the bar."""
    x0 = G_IN + G_LOW * (G_TICK - G_IN) + 0.16
    return DoubleArrow(P(x0, G_Y), P(G_TICK - 0.1, G_Y), color=TEXT, stroke_width=5, buff=0, tip_length=0.2,
                       max_tip_length_to_length_ratio=0.2).set_z_index(17)


def static_world():
    """Everything that never moves: sky, sun, sea, sea floor, the left wall with its ledge, the shore."""
    g = VGroup()
    g.add(Rectangle(width=XR - XL, height=YT - 7.6, stroke_width=0, fill_color=SKY_TOP, fill_opacity=1).move_to(P(0, (YT + 7.6) / 2)))
    g.add(band_stack(XL, XR, 7.7, SEA_Y - 0.2, SKY_TOP, SKY_LOW, n=24, power=1.3))
    g.add(soft_glow(SUN, 0.3, 1.7, GOLD, n=14, peak=0.07))
    g.add(Circle(radius=0.27, stroke_width=0, fill_color="#F6DC8C", fill_opacity=1).move_to(SUN))
    g.add(band_stack(XL, XR, SEA_Y - 0.1, FLOOR_Y - 0.1, SEA_TOP, SEA_MID, n=34, power=0.85))
    g.add(poly([(XL, YB), (XL, FLOOR_Y), (XR, FLOOR_Y), (XR, YB)], ROCK))
    rng = random.Random(5)
    for y, c in [(-3.45, "#252330"), (-4.05, "#27252F"), (-4.6, "#252330"), (-5.15, "#2A2732"), (-5.75, "#2D2A36"), (-6.4, "#2A2732"),
                 (-7.0, "#2D2A36")]:       # faint strata; nothing else is ever drawn in the caption band
        pts = [P(x, y + 0.05 * math.sin(1.3 * x + y * 7)) for x in np.linspace(XL, XR, 30)]
        g.add(VMobject(stroke_color=c, stroke_width=3).set_points_smoothly(pts))
    g.add(poly(WALL, ROCK))
    for _ in range(26):
        x, y = rng.uniform(-3.9, -0.9), rng.uniform(-0.05, 0.6)
        if x < -3.3:
            y = rng.uniform(-2.8, 2.2)
        elif y < LEDGE_Y - 0.72:
            continue
        w = rng.uniform(0.07, 0.16)
        g.add(poly([(x - w, y), (x - w * 0.2, y + w * 0.5), (x + w, y + w * 0.15), (x + w * 0.5, y - w * 0.4)], "#35323E", 0.7))
    edge = VMobject(stroke_color=ROCK_HI, stroke_width=3)
    edge.set_points_as_corners([P(*p) for p in WALL[1:-1]])
    g.add(edge)
    g.add(Line(P(-3.95, FLOOR_Y), P(XR, FLOOR_Y), stroke_color=ROCK_HI, stroke_width=3))
    g.add(poly(LANDPTS, LAND))
    rim = VMobject(stroke_color="#5A5136", stroke_width=3)
    rim.set_points_as_corners([P(*p) for p in LANDPTS[1:]])
    g.add(rim)
    g.set_z_index(-100)
    return g


def land_block(dull=False):
    b = RoundedRectangle(width=0.8, height=0.55, corner_radius=0.09, stroke_color="#C2C8D2", stroke_width=3,
                         fill_color=("#4A4F59" if dull else GREY), fill_opacity=1).rotate(-0.85)
    g = VGroup(b)
    if not dull:
        g.add(Dot(P(0.3, 0.28), radius=0.1, color=YELLOW))
    return g


# ----------------------------------------------------------------------------- the carried world
class VWorld:
    """The carried world of the tall frame. Build it at the stage the last scene left it; change numbers
    with ramp(); one clock updater drives every ambient motion from film time."""

    def __init__(self, scene, sid, **stage):
        self.sc = scene
        self.v = dict(STAGE0)
        self.v.update(stage)
        self.t0 = T0.get(sid, 0.0)
        self.ts, self.t = 0.0, self.t0
        self.pre, self.fns = [], []
        self.hud, self.pinned = [], bool(self.v["pinned"])     # the bar and its labels are fixed to the frame, whatever the camera does
        self.s, self.c = 1.0, P(0, 0)
        self.tau_fn, self.conv, self.born = None, None, {}
        self.fl_pos = [P(0, 0)] * N_FLAKE
        c, w = self.v["cam"]
        fr = scene.camera.frame
        fr.stretch_to_fit_width(FW)
        fr.stretch_to_fit_height(FH)
        fr.scale(w / FW).move_to(c)
        scene.add(static_world())
        self.clock = Mobject()
        self.clock.add_updater(lambda m, dt: self.tick())
        scene.add(self.clock)
        self._build()
        self._build_hud()
        self.tick()

    # ---- helpers for scenes
    def ramp(self, k, target, dur, delay=0.0):
        """Ease one world number to a target over `dur` seconds, starting `delay` from now (on the clock)."""
        t_start, st = self.ts + delay, {}

        def fn(ts):
            if ts < t_start:
                return
            if "v0" not in st:
                st["v0"] = self.v[k]
            u = clip01((ts - t_start) / dur) if dur > 0 else 1.0
            self.v[k] = lerp(st["v0"], target, ease(u))
            if u >= 1 and fn in self.pre:
                self.pre.remove(fn)
        self.pre.append(fn)

    def start_rewind(self, t_stop=0.1, t_rev=0.5, t_end=3.0, speed=3.2):
        """Run the rust clock backward (scene time): the flakes stop, rise, and stop again."""
        st = dict(tau=self.t0, last=0.0)

        def rate(ts):
            if ts < t_stop:
                return 1.0
            if ts < t_rev:
                return lerp(1.0, 0.0, (ts - t_stop) / (t_rev - t_stop))
            if ts < t_rev + 0.5:
                return lerp(0.0, -speed, (ts - t_rev) / 0.5)
            if ts < t_end:
                return -speed
            if ts < t_end + 0.5:
                return lerp(-speed, 0.0, (ts - t_end) / 0.5)
            return 0.0

        def fn(ts):
            st["tau"] += rate(ts) * (ts - st["last"])
            st["last"] = ts
            return st["tau"]
        self.tau_fn = fn

    # ---- build
    def _build(self):
        sc, v = self.sc, self.v
        rng = random.Random(7)
        # shafts of sunlight and soft bands of light under the surface (slow, never still)
        self.rays = VGroup(*[VMobject(stroke_width=0, fill_color=GOLD, fill_opacity=0.055) for _ in range(3)]).set_z_index(1)
        self.caus = VGroup(*[VMobject(stroke_color="#8FE8EA", stroke_width=[9, 12, 14, 16][k]).set_stroke(opacity=0.07) for k in range(4)]).set_z_index(1.2)
        self.cx = [np.linspace(x0, XR, 44) for x0 in (-2.4, -2.7, -3.25, -0.1)]
        self.cd = [0.3, 0.75, 1.3, 2.7]
        # the striped stack on the sea floor
        self.stripes = VGroup(*[Rectangle(width=XR - XL, height=0.01, stroke_width=0, fill_color=(RED if j % 2 == 0 else SILICA),
                                          fill_opacity=1.0 if j % 2 == 0 else 0.85) for j in range(N_STRIPE)]).set_z_index(2)
        self._stack_last = None
        # rust flakes: three in four fall the open column, one in four falls under the ledge
        self.flakes = VGroup().set_z_index(3)
        self.trails = VGroup().set_z_index(2.8)        # a short streak above each falling flake
        self.fl_spec = []
        for k in range(N_FLAKE):
            size = 0.19 + 0.1 * hsh(k, 5)
            if k % 4 == 3:
                x0, ys = lerp(-2.9, -0.8, hsh(k, 1)), lerp(-0.95, -0.5, hsh(k, 2))
            else:
                x0, ys = lerp(-0.15, 3.8, hsh(k, 1)), lerp(1.35, 2.25, hsh(k, 2))
            speed = lerp(0.5, 0.78, hsh(k, 3))
            m = prep(rust_flake(size))
            m._ang = 0.0
            self.flakes.add(m)
            self.trails.add(prep(Line(ORIGIN, UP * (0.3 + 0.9 * size), stroke_color=RED, stroke_width=3).set_stroke(opacity=0.38)))
            self.fl_spec.append((x0, ys, (ys - FLOOR_Y) / speed, hsh(k, 4), size, lerp(0.3, 0.9, hsh(k, 6)) * (1 if k % 2 else -1), 6.28 * hsh(k, 8)))
        # dissolved iron: grey discs, each on its own slow path
        self.iron = VGroup().set_z_index(4)
        homes = []
        for i in range(N_IRON):
            for _ in range(4000):
                if i % 4 == 3:
                    p = P(rng.uniform(-3.3, -0.4), rng.uniform(-2.55, -1.35))
                else:
                    p = P(rng.uniform(0.05, 3.55), rng.uniform(-2.55, 2.1))
                if all(np.linalg.norm(p - h) > 0.78 for h in homes):
                    break
            homes.append(p)
        self.iron_spec = []
        for i, h in enumerate(homes):
            g = iron_disc(0.17)
            g[0].set_stroke(width=1.5)
            g[1].scale(1.3)
            prep(g)
            g._ang = 0.0
            self.iron.add(g)
            self.iron_spec.append((h, rng.uniform(0.16, 0.34), rng.uniform(0.1, 0.22), rng.uniform(0.25, 0.5), rng.uniform(0.2, 0.42),
                                   rng.uniform(0, 6.28), rng.uniform(0, 6.28), rng.uniform(0.35, 0.8) * rng.choice([-1, 1])))
        # the mat: GREEN lumps on the ledge that breathe
        self.matglow = prep(VGroup(*[Ellipse(width=(MAT_X1 - MAT_X0) * (1.05 + 0.1 * i), height=0.6 + 0.35 * i, stroke_width=0, fill_color=GREEN,
                                             fill_opacity=0.06).move_to(P((MAT_X0 + MAT_X1) / 2, LEDGE_Y + 0.14)) for i in range(3)])).set_z_index(9.5)
        self.mat = VGroup().set_z_index(10)
        self.lump_x = np.linspace(MAT_X0 + 0.1, MAT_X1 - 0.1, N_LUMP)
        for j, x in enumerate(self.lump_x):
            e = prep(Ellipse(width=0.36, height=0.25 + 0.07 * hsh(j, 9), stroke_width=0, fill_color=[GREEN, "#6FAE58", "#93D174"][j % 3], fill_opacity=1))
            e.move_to(P(x, LEDGE_Y + 0.09))
            e._d = abs(x - CELL_X) / 1.45
            self.mat.add(e)
        # oxygen bubbles from the mat
        self.bub = VGroup().set_z_index(11)
        self.bub_spec = []
        for k in range(N_BUB):
            m = prep(VGroup(Dot(ORIGIN, radius=0.17, color=BLUE).set_opacity(0.16), Dot(ORIGIN, radius=0.085, color=BLUE)))
            self.bub.add(m)
            j = (k * 7) % N_LUMP
            x0 = self.lump_x[j]
            dx = min(lerp(0.7, 3.3, hsh(k, 11)), 3.4 - x0)
            self.bub_spec.append((j, x0, dx, lerp(1.75, 2.3, hsh(k, 12)), (k + 0.5 * hsh(k, 13)) / N_BUB, hsh(k, 5)))
        # oxygen pips in the air
        self.pips = VGroup().set_z_index(13)
        homes = list(PIP_HOMES)
        tries = 0
        while len(homes) < N_PIP and tries < 8000:
            tries += 1
            p = P(rng.uniform(-2.3, 3.45), rng.uniform(2.95, 3.82))
            if np.linalg.norm(p - SUN) < 0.55:
                continue
            if all(np.linalg.norm(p - h) > 0.44 for h in homes):
                homes.append(p)
        n_low = len(homes)
        tries = 0
        while len(homes) < n_low + N_HIGH and tries < 20000:
            tries += 1
            p = P(rng.uniform(-4.1, 4.1), rng.uniform(4.0, 10.2))
            if all(np.linalg.norm(p - h) > 0.8 for h in homes):
                homes.append(p)
        self.n_low = n_low
        self.pip_spec, self.pip_big = [], []
        for k, h in enumerate(homes):
            g = prep(pip(0.1))
            g._f = 1.0
            self.pip_big.append(lerp(0.5, 2.1, hsh(k, 33)))
            self.pips.add(g)
            self.pip_spec.append((h, rng.uniform(0.06, 0.12), rng.uniform(0.03, 0.06), rng.uniform(0.3, 0.6), rng.uniform(0.25, 0.5),
                                  rng.uniform(0, 6.28), rng.uniform(0, 6.28)))
        # the travelling sea surface
        self.sx = np.linspace(-2.22, XR, 80)
        self.skin = VMobject(stroke_width=0, fill_color=SEA_TOP, fill_opacity=1).set_z_index(14)
        self.surf = VMobject(stroke_color="#A9E7EA", stroke_width=3.5).set_z_index(14.2)
        self.glints = VGroup(*[Line(ORIGIN, RIGHT * 0.3, stroke_color=WHITE, stroke_width=3.5) for _ in range(7)]).set_z_index(14.4)
        for m in self.glints:
            prep(m)
        # land rock (GREY blocks; the ones that have met oxygen are dull and have no dot)
        self.blocks = VGroup(*[land_block(dull=(v["dull"] > 0)).move_to(b) for k, b in enumerate(BLOCKS)]).set_z_index(15)
        # the dimming layer for close-ups and the end card
        self.veil = Rectangle(width=XR - XL, height=SEA_Y + 0.07 - FLOOR_Y, stroke_width=0, fill_color="#02030A", fill_opacity=0
                              ).move_to(P(0, (SEA_Y + 0.07 + FLOOR_Y) / 2)).set_z_index(18)       # close-ups: the sea dims, the sky does not
        self.veil2 = Rectangle(width=XR - XL, height=YT - YB, stroke_width=0, fill_color="#02030A", fill_opacity=0
                               ).move_to(P(0, (YT + YB) / 2)).set_z_index(18.5)   # end card: the whole world, top of the sky included
        self.veil._a = self.veil2._a = -1.0
        sc.add(self.rays, self.caus, self.stripes, self.trails, self.flakes, self.iron, self.matglow, self.mat, self.bub, self.pips,
               self.skin, self.surf, self.glints, self.veil, self.veil2)
        if v["blocks"]:
            sc.add(self.blocks)

    def _build_hud(self):
        v = self.v
        z = 16
        self.g_bar = RoundedRectangle(width=G_X1 - G_X0, height=G_H, corner_radius=0.1, stroke_color=TEXT, stroke_width=3,
                                      fill_color="#080B12", fill_opacity=0.8).move_to(P((G_X0 + G_X1) / 2, G_Y)).set_z_index(z)
        self.g_fill = Rectangle(width=0.1, height=G_H - 0.12, stroke_width=0, fill_color=BLUE, fill_opacity=1).set_z_index(z + 0.2)
        self.g_cap = prep(Line(P(0, G_Y - G_H / 2 + 0.06), P(0, G_Y + G_H / 2 - 0.06), stroke_color="#D8F4FB", stroke_width=3)).set_z_index(z + 0.4)
        self.g_fill2 = prep(Rectangle(width=G_TICK - G_IN, height=G_H - 0.12, stroke_width=0, fill_color=BLUE, fill_opacity=1)
                            .move_to(P((G_TICK + G_IN) / 2, G_Y))).set_z_index(z + 0.3)
        # the "today" tick ends at the bottom of the bar (it used to run on down through the readout)
        self.g_tick = DashedLine(P(G_TICK, G_Y - G_H / 2), P(G_TICK, G_Y + 0.36), dash_length=0.09, stroke_color=TEXT, stroke_width=3.5).set_z_index(z + 0.6)
        self.g_head = T("O₂ in air", size=34)
        self.g_head.move_to(P(G_X0 + self.g_head.width / 2, ROW_A)).set_z_index(z)
        self.g_today = T("today", size=34)
        self.g_today.move_to(P(G_X1 - self.g_today.width / 2, ROW_A)).set_z_index(z)
        self.g_tag = pill("schematic").move_to(P((self.g_head.get_right()[0] + self.g_today.get_left()[0]) / 2, ROW_A)).set_z_index(z)
        # "levels uncertain" sits under the left end of the readout, clear of the pips and of the sun
        self.g_tag2 = pill("levels uncertain")
        self.g_tag2.move_to(P(G_X0 + self.g_tag2.width / 2, ROW_C - 0.13)).set_z_index(z)
        self.arrow = bar_arrow()
        self.hud_bg = VGroup(*[Rectangle(width=XR - XL, height=7.3 - yb, stroke_width=0, fill_color=SKY_TOP, fill_opacity=0).move_to(P(0, (7.3 + yb) / 2))
                               for yb in (3.9, 3.8, 3.7)]).set_z_index(15.6)
        self.hud_bg._a = 0.0
        self.sc.add(self.hud_bg)
        for m in (self.hud_bg, self.g_bar, self.g_fill2, self.g_tick, self.g_head, self.g_today, self.g_tag, self.g_tag2, self.arrow):
            self.pin(m)
        self.readout = None
        self.hud_on = False
        if v["hud"]:
            self.show_hud()
            if v["readout"]:
                self.readout = self.readout_text(v["readout"])
                self.sc.add(self.readout)
            if v["tag2"]:
                self.sc.add(self.g_tag2)
            if v["arrow"]:
                self.sc.add(self.arrow)

    def show_hud(self):
        """Put the bar on screen. Returns its parts, for a scene that wants to draw them on."""
        self.hud_on = True
        self.sc.add(self.g_bar, self.g_fill, self.g_fill2, self.g_cap, self.g_tick, self.g_head, self.g_today, self.g_tag)
        self._t_hud()
        return dict(bar=self.g_bar, tick=self.g_tick, head=self.g_head, today=self.g_today, tag=self.g_tag)

    def readout_text(self, text):
        m = fit(T(text, size=34), max_w=G_X1 - G_X0)
        return self.pin(m.move_to(P(G_X0 + m.width / 2, ROW_B)).set_z_index(16))

    def set_readout(self, text, rt=0.45):
        new = self.readout_text(text)
        old, self.readout = self.readout, new
        anims = [FadeIn(new, shift=UP * 0.14 * self.s)]
        if old is not None:
            self.unpin(old)
            anims.append(FadeOut(old, shift=UP * 0.14 * self.s))
        self.sc.play(*anims, run_time=rt)             # camera at rest

    # ---- closed-form positions
    def flake_at(self, k, tau):
        x0, ys, per, phi, size, spin, sph = self.fl_spec[k]
        u = (tau / per + phi) % 1.0
        top = FLOOR_Y + self.v["stack"] * STRIPE_H
        return P(x0 + 0.14 * math.sin(0.8 * tau + sph), lerp(ys, top + 0.2 * size, u)), clip01(u / 0.07) * clip01((1 - u) / 0.035)

    def iron_at(self, i, t):
        h, ax, ay, wx, wy, p1, p2, _ = self.iron_spec[i]
        return h + P(ax * math.sin(wx * t + p1), ay * math.sin(wy * t + p2))

    def pip_at(self, k, t):
        h, ax, ay, wx, wy, p1, p2 = self.pip_spec[k]
        return h + P(ax * math.sin(wx * t + p1), ay * math.sin(wy * t + p2))

    def lump_a(self, j):
        return clip01((self.v["mat"] * 1.25 - self.mat[j]._d) / 0.2)

    # ---- the clock
    def tick(self):
        self.ts = ts = self.sc.renderer.time
        self.t = t = self.t0 + ts
        fr = self.sc.camera.frame
        self.s, self.c = fr.width / FW, fr.get_center()
        for fn in list(self.pre):
            fn(ts)
        if self.pinned:
            for m in self.hud:
                self._pin_one(m)
        v = self.v
        tau = self.tau_fn(ts) if self.tau_fn else t
        # surface
        ys = SEA_Y + 0.045 * np.sin(1.9 * self.sx - 0.9 * t) + 0.022 * np.sin(4.3 * self.sx + 1.3 * t)
        pts = np.column_stack([self.sx, ys, np.zeros_like(self.sx)])
        self.surf.set_points_as_corners(pts)
        self.skin.set_points_as_corners(np.vstack([pts, [[XR, SEA_Y - 0.16, 0], [self.sx[0], SEA_Y - 0.16, 0], pts[0]]]))
        for k, m in enumerate(self.glints):
            x = -1.8 + 0.9 * k + 0.35 * math.sin(0.23 * t + k)
            y = SEA_Y + 0.045 * math.sin(1.9 * x - 0.9 * t) + 0.022 * math.sin(4.3 * x + 1.3 * t)
            put(m, P(x, y + 0.015))
            seta(m, 0.75 * max(0.0, math.sin(1.1 * t + 2.1 * k)) ** 2)
        for k, m in enumerate(self.caus):
            xs = self.cx[k]
            yy = SEA_Y - self.cd[k] + 0.06 * np.sin(1.2 * xs + 0.5 * t + 1.7 * k) + 0.03 * np.sin(2.9 * xs - 0.8 * t)
            m.set_points_as_corners(np.column_stack([xs, yy, np.zeros_like(xs)]))
        for k, m in enumerate(self.rays):
            xt = [0.3, 1.5, 2.7][k] + 0.12 * math.sin(0.31 * t + 2.0 * k)
            sway = 0.2 * math.sin(0.23 * t + 1.3 * k)
            m.set_points_as_corners([P(xt, SEA_Y - 0.12), P(xt + 0.45, SEA_Y - 0.12), P(xt - 1.5 + sway, -1.9), P(xt - 2.4 + sway, -1.9), P(xt, SEA_Y - 0.12)])
        # the striped stack
        if self._stack_last is None or abs(v["stack"] - self._stack_last) > 1e-4:
            self._stack_last = v["stack"]
            for j, r in enumerate(self.stripes):
                h = clip01(v["stack"] - j) * STRIPE_H
                r.stretch_to_fit_height(max(h, 0.004))
                r.move_to(P(0, FLOOR_Y + j * STRIPE_H + max(h, 0.004) / 2))
                r.set_fill(opacity=(0.0 if h <= 0.001 else (1.0 if j % 2 == 0 else 0.85)))
        # rust flakes
        fa = v["flakes"]
        for k, m in enumerate(self.flakes):
            a = clip01((fa * 1.15 - hsh(k, 7)) / 0.15)
            if self.conv is not None:
                a *= 1.0 - clip01((ts - self.conv[k]) / 0.45)
            if a <= 0.004:
                seta(m, 0.0)
                seta(self.trails[k], 0.0)
                continue
            p, ua = self.flake_at(k, tau)
            self.fl_pos[k] = p
            tr = self.trails[k]
            put(tr, p + UP * (tr.height / 2 + 0.08))
            seta(tr, a * ua * clip01((p[1] - FLOOR_Y - v["stack"] * STRIPE_H) / 0.6) * (1.0 - clip01(ts / 0.3) if self.tau_fn else 1.0))
            ang = self.fl_spec[k][5] * tau
            m.rotate(ang - m._ang)
            m._ang = ang
            put(m, p)
            seta(m, a * ua)
        # dissolved iron
        ia = v["iron"]
        for i, g in enumerate(self.iron):
            a = ia
            if a <= 0.004:
                seta(g, 0.0)
                continue
            p = self.iron_at(i, t)
            if self.conv is not None:
                c = self.conv[i]
                if ts < c:
                    seta(g, 0.0)
                    continue
                if i not in self.born:
                    self.born[i] = self.fl_pos[i].copy()
                p = lerp(self.born[i], p, ease((ts - c) / 1.9))
                a *= clip01((ts - c) / 0.4)
            a *= clip01((p[1] - FLOOR_Y - v["stack"] * STRIPE_H - 0.05) / 0.3)      # the rising stack buries the lowest water
            ang = self.iron_spec[i][7] * t
            g.rotate(ang - g._ang)
            g._ang = ang
            put(g, p)
            seta(g, a)
        # the mat and its bubbles
        seta(self.matglow, clip01(v["mat"]))
        for j, e in enumerate(self.mat):
            a = self.lump_a(j)
            seta(e, a)
            if a > 0:
                put(e, P(self.lump_x[j], LEDGE_Y + 0.09 + 0.018 * math.sin(1.4 * t + 0.9 * j)))
        for k, m in enumerate(self.bub):
            j, x0, dx, ye, phi, lk = self.bub_spec[k]
            on = clip01((v["bub"] * 1.15 - hsh(k, 14)) / 0.15) * self.lump_a(j)
            if on <= 0.004:
                seta(m, 0.0)
                continue
            u = (t / PB + phi) % 1.0
            uu = clip01(u / 0.62)
            x = x0 + dx * uu ** 1.2 + 0.05 * math.sin(12 * u + k)
            y = lerp(LEDGE_Y + 0.3, ye, uu ** 0.85)
            a = clip01(u / 0.06)
            if lk < v["leak"]:
                if u > 0.62:
                    w = (u - 0.62) / 0.38
                    y = lerp(ye, SEA_Y + 0.62, w)
                    x += 0.15 * w
                a *= clip01((1 - u) / 0.1)
            else:
                a *= clip01((0.72 - u) / 0.14)
            put(m, P(x, y))
            seta(m, a * on)
        # pips (at "Leftovers" they swell and spread a little, as if drifting toward the viewer, at full blue)
        sw = v["swell"]
        for k, g in enumerate(self.pips):
            a = clip01(v["pips"] - k) if k < self.n_low else clip01(v["pips2"] * 1.4 - 0.4 * hsh(k, 31))
            seta(g, a)
            if a > 0:
                p = self.pip_at(k, t)
                f = 1.0 + sw * self.pip_big[k]
                if sw > 0:
                    p = p + sw * 0.1 * self.pip_big[k] * (p - SWELL_C)
                if abs(f - g._f) > 0.003:
                    g.scale(f / g._f)
                    g._f = f
                put(g, p)
        # veil
        for m, k in ((self.veil, "veil"), (self.veil2, "veil2")):
            if abs(v[k] - m._a) > 0.003:
                m._a = v[k]
                m.set_fill(opacity=v[k])
        if self.hud_on:
            self._t_hud()
        for fn in list(self.fns):
            fn(ts)

    def pin(self, m):
        """Keep a mobject that was built in screen coordinates fixed on screen while the camera moves."""
        for fm in m.get_family():
            fm._bsw = float(fm.get_stroke_width())
        m._s, m._c = 1.0, P(0, 0)
        if m not in self.hud:
            self.hud.append(m)
        if self.pinned:
            self._pin_one(m)
        return m

    def unpin(self, m):
        if m in self.hud:
            self.hud.remove(m)

    def _pin_one(self, m):
        s, c = self.s, self.c
        if abs(s - m._s) > 1e-9 or abs(c[0] - m._c[0]) > 1e-9 or abs(c[1] - m._c[1]) > 1e-9:
            m.scale(s / m._s, about_point=m._c)
            m.shift(c - m._c)
            for fm in m.get_family():
                if getattr(fm, "_bsw", 0.0):
                    fm.set_stroke(width=fm._bsw * s, family=False)
            m._s, m._c = s, c.copy()

    def _t_hud(self):
        s, c = (self.s, self.c) if self.pinned else (1.0, P(0, 0))
        W_ = lambda x, y: c + s * P(x, y)
        w = max(0.02, self.v["gauge"] * (G_TICK - G_IN))
        y0, y1 = G_Y - G_H / 2 + 0.06, G_Y + G_H / 2 - 0.06
        self.g_fill.set_points_as_corners([W_(G_IN, y0), W_(G_IN + w, y0), W_(G_IN + w, y1), W_(G_IN, y1), W_(G_IN, y0)])
        self.g_cap.put_start_and_end_on(W_(G_IN + w, y0), W_(G_IN + w, y1))
        self.g_cap.set_stroke(width=3 * s, family=False)
        seta(self.g_fill2, self.v["gauge2"])
        seta(self.g_cap, 1.0 - self.v["gauge2"])
        # a dark backing behind the bar's rows whenever the camera has left the full framing (so nothing passes behind the words)
        off = clip01(max(abs(self.s - 1.0) / 0.06, float(np.hypot(self.c[0], self.c[1])) / 0.15)) if self.pinned else 0.0
        if abs(off - self.hud_bg._a) > 0.01:
            self.hud_bg._a = off
            for r, o in zip(self.hud_bg, (0.5, 0.3, 0.2)):
                r.set_fill(opacity=o * off * 1.9 if o == 0.5 else o * off)


# ----------------------------------------------------------------------------- takers of oxygen in the air
class Take:
    """One oxygen pip gets out of the sea and is taken: a taker (volcanic puff, methane ring or land rock)
    meets it, its YELLOW dot jumps to the pip, and the pip is gone. Runs on the world clock."""

    def __init__(self, W, kind, tj, block=None):
        self.W, self.kind, self.tj = W, kind, tj
        if kind == "puff":                    # in from the left, inside the safe width, to the middle of the sky
            self.spot, self.rise = P(-0.1, 4.25), P(0.1, SEA_Y + 0.05)
            self.a, self.b, self.lead = P(-3.3, 4.45), self.spot + P(-0.95, 0.05), 1.6
            self.taker = VGroup(*[Circle(radius=r, stroke_width=0, fill_color="#9AA1AE", fill_opacity=0.9).shift(P(x, y))
                                  for x, y, r in [(-0.3, 0.0, 0.34), (0.14, 0.11, 0.39), (0.2, -0.2, 0.28)]])
            self.off = P(0.45, 0.0)
        elif kind == "ring":                  # up from the sea floor, on the right
            self.spot, self.rise = P(1.0, 3.5), P(1.15, SEA_Y + 0.05)       # well clear of the sun
            self.a, self.b, self.lead = P(2.95, FLOOR_Y + W.v["stack"] * STRIPE_H + 0.3), self.spot + P(0.72, -0.06), 2.3
            self.taker = Circle(radius=0.33, stroke_color="#C2C8D2", stroke_width=6, fill_color=GREY, fill_opacity=0.3)
            self.off = P(-0.33, 0.0)
        else:                                 # the rock on the shore, on the left
            self.block = W.blocks[0]
            c = self.block[0].get_center()
            self.dot_home = self.block[1].get_center().copy()
            self.spot, self.rise = c + P(0.72, 0.5), P(-1.45, SEA_Y + 0.05)
            self.taker, self.lead = None, 0.0
        self.pip = prep(pip(0.18)).set_z_index(13.5)
        self.pop = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=6).set_z_index(13.7)
        self.pop._r = 0.2
        prep(self.pop)
        if self.taker is not None:
            prep(self.taker).set_z_index(14.6)
            self.dot = Dot(ORIGIN, radius=0.1, color=YELLOW).set_z_index(14.7)
            W.sc.add(self.taker, self.dot)
            seta(self.taker, 0.0)
        else:
            self.dot = self.block[1].set_z_index(15.5)
        prep(self.dot)
        W.sc.add(self.pip, self.pop)
        seta(self.pip, 0.0)
        seta(self.pop, 0.0)
        self.done = False
        W.fns.append(self.update)
        self.update(W.ts)

    def update(self, ts):
        r = ts - self.tj                      # seconds from the jump
        # the pip leaves the sea and stands in the air
        u = clip01((r + 1.3) / 0.75)
        pp = lerp(self.rise, self.spot, ease(u)) + P(0.03 * math.sin(2.1 * ts), 0.02 * math.sin(1.7 * ts + 1))
        put(self.pip, pp)
        seta(self.pip, clip01((r + 1.3) / 0.2) * (1.0 - clip01((r - 0.28) / 0.25)))
        # the taker comes to it
        if self.taker is not None:
            w = clip01((r + self.lead) / (self.lead - 0.15))
            tp = lerp(self.a, self.b, ease(w) * 0.5 + w * 0.5)
            if self.kind == "ring":
                tp = tp + P(0.14 * math.sin(5.0 * w), 0)
            if r > 0:
                tp = tp + (P(0.25, 0.12) if self.kind == "puff" else P(0.05, 0.4)) * r
            put(self.taker, tp)
            seta(self.taker, clip01((r + self.lead) / 0.3) * (1.0 if r < 0.3 else 0.45) * (1.0 - clip01((r - 0.6) / 0.8)))
            dp = tp + self.off
        else:
            dp = self.dot_home
            if r > 0.3 and not self.done:
                self.done = True
                self.block[0].set_fill("#4A4F59")
        # the electron jumps, and the pip is gone
        j = clip01(r / 0.3)
        if j > 0:
            dp = lerp(dp, pp, ease(j)) + P(0, 0.16 * math.sin(math.pi * j))
        put(self.dot, dp)
        da = (1.0 - clip01((r - 0.28) / 0.25))
        if self.taker is not None:
            da *= clip01((r + self.lead) / 0.3)
        seta(self.dot, da)
        q = clip01((r - 0.28) / 0.45)
        if 0 < q < 1:
            R = lerp(0.2, 1.1, q)
            self.pop.scale(R / self.pop._r)
            self.pop._r = R
            put(self.pop, pp)
            seta(self.pop, 1.0 - q)
        else:
            seta(self.pop, 0.0)


class Resize(Animation):
    """Scale a mobject by `factor` about its centre while moving its centre to `to`, strokes too."""

    def __init__(self, mob, factor, to, **kw):
        self.factor, self.to = float(factor), np.array(to, dtype=float)
        super().__init__(mob, **kw)

    def begin(self):
        self.k = 1.0
        self.p0 = self.mobject.get_center().copy()
        self.sw = [(f, float(f.get_stroke_width())) for f in self.mobject.get_family() if f.get_stroke_width()]
        super().begin()

    def interpolate_mobject(self, alpha):
        k = self.factor ** self.rate_func(alpha)
        self.mobject.scale(k / self.k)
        self.k = k
        for f, w in self.sw:
            f.set_stroke(width=w * k, family=False)
        self.mobject.move_to(self.p0 + (self.to - self.p0) * ((k - 1) / (self.factor - 1)))


# ----------------------------------------------------------------------------- scenes
class VScene(SpokenScene, MovingCameraScene):
    """A scene in the tall world. self.world(**stage) builds it; self.zoom(framing) moves the camera."""

    def world(self, **stage):
        self.W = VWorld(self, os.environ.get("KX_SCENE_ID", ""), **stage)
        return self.W

    def zoom(self, framing, **kw):
        c, w = framing
        return Zoom(self.camera.frame, c, w, **kw)

    def scr(self, mob, sx, sy, framing, z=22):
        """Place a mobject designed in screen units at a screen point of the given framing."""
        c, w = framing
        sw_scale(mob, w / FW)
        mob.move_to(c + (w / FW) * P(sx, sy))
        return mob.set_z_index(z)

    def hold(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def left(self, pad=0.38):
        """Seconds left in the scene (narration + tail), less a small pad."""
        return max(0.2, self.narration_s + pad - self.elapsed())

    def ripple(self, pt, color=TEXT, r=0.25, z=24, sw=4):
        ring = Circle(radius=r, stroke_color=color, stroke_width=sw).move_to(pt).set_z_index(z)
        self.add(ring)
        return FadeOut(ring, scale=2.6)


class S00Hook(VScene):
    """Rust falls the whole height of the frame from the first frame; then the view tilts up to the air."""

    def construct(self):
        W = self.world(pinned=False)          # the bar is drawn on in world coordinates as the view arrives at the full framing
        t_up = self.t_of("in your lungs") - 0.55
        self.play(self.zoom(cam(1.18)), run_time=t_up, rate_func=linear)
        W.v["gauge"] = 0.0
        hud = W.show_hud()
        W.ramp("gauge", G_LOW, 1.0, delay=0.75)
        self.play(self.zoom(FULL, rate_func=smooth),
                  LaggedStart(Create(hud["bar"]), FadeIn(hud["head"], shift=DOWN * 0.15), Create(hud["tick"]), FadeIn(hud["today"], shift=DOWN * 0.15),
                              FadeIn(hud["tag"], scale=0.8), lag_ratio=0.3), run_time=1.7)
        self.play(self.ripple(P(G_IN + 0.5 * G_LOW * (G_TICK - G_IN), G_Y), BLUE, r=0.3), run_time=0.6)
        self.finish()


class S01World(VScene):
    """The hook picture runs backward: flakes rise and loosen into grey iron; the bar drains."""

    def construct(self):
        W = self.world(cam=FULL, hud=True)
        W.start_rewind()
        W.conv = [0.75 + 2.1 * hsh(k, 21) for k in range(N_FLAKE)]
        W.v["iron"] = 1.0
        W.ramp("bub", 0.0, 0.5, delay=0.1)
        W.ramp("leak", 0.0, 0.3)
        W.ramp("mat", 0.0, 1.8, delay=0.4)
        W.ramp("stack", 0.12, 2.0, delay=0.6)
        gl = rewind_glyph().scale(1.1).move_to(P(2.36, ROW_B + 0.04)).set_z_index(16)       # after the readout, left of the sun
        self.play(FadeIn(gl, scale=1.6), run_time=0.3)
        self.play(gl.animate.shift(LEFT * 0.1), run_time=0.4, rate_func=there_and_back)
        W.set_readout(R3, rt=0.4)
        for _ in range(4):
            self.play(gl.animate.shift(LEFT * 0.1), run_time=0.45, rate_func=there_and_back)
        self.play(FadeOut(gl, shift=LEFT * 0.3), run_time=0.35)
        # the air held almost no oxygen: the bar drains to a sliver and the pips wink out
        self.at("almost no oxygen", lead=0.5)
        W.ramp("gauge", G_SLIVER, 1.1)
        W.ramp("pips", 0.0, 1.1)
        halo = W.g_bar.copy().set_fill(opacity=0).set_stroke(WHITE, width=8, opacity=0.9).set_z_index(17)
        self.play(FadeIn(halo), run_time=0.3)
        self.play(FadeOut(halo, scale=1.04), run_time=0.8)
        self.play(self.ripple(P(G_IN + 0.05, G_Y), BLUE, r=0.26), run_time=0.7)
        # the sea held dissolved iron: the label lands after the discs have settled
        self.at("dissolved iron", lead=0.0)
        lab = ochip("dissolved iron", size=34).move_to(IRON_LBL).set_z_index(22)
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.4)
        self.finish()


IRON_LBL = P(1.75, 0.35)
CELL_K = 0.72                       # the cell centre stage: 4.3 units long
CELL_C = P(0.0, 0.3)
CELL_X = -2.05                      # where it sits on the ledge
TINY = 0.13                         # its size on the ledge, as a fraction of centre stage


def cpt(x, y):
    """A point in the hero cell's own (mirrored) design coordinates -> world, centre stage."""
    return CELL_C + CELL_K * P(x, y)


def hero_cell():
    """The web film's cyanobacterium, mirrored so its mouth faces the open water, built centre stage."""
    c = cyano_cell()
    c.remove(c.food)                 # this cut does not say what the electrons build
    c.flip(UP, about_point=ORIGIN)
    sw_scale(c, CELL_K)
    c.shift(CELL_C)
    c.hinge_pt, c.mouth_pt, c.vent_pt = cpt(2.02, 1.3), cpt(1.62, 1.3), cpt(-1.62, 1.8)
    return c.set_z_index(20)


def cyano_label():
    return ochip("cyanobacteria", size=34, color=GREEN).move_to(CELL_C + DOWN * 1.55).set_z_index(22)


class S02Trick(VScene):
    """One tiny cell on the ledge, then close up: two droplets in, four electrons kept, one bubble out. Then a mat."""

    def construct(self):
        W = self.world(**ST1)
        lab0 = ochip("dissolved iron", size=34).move_to(IRON_LBL).set_z_index(22)
        self.add(lab0)
        cell = hero_cell()
        stage = cell.get_center().copy()
        sw_scale(cell.shift(-stage), TINY)
        home = P(CELL_X, LEDGE_Y + 0.03 + cell.height / 2)
        cell.move_to(home + P(0.9, 1.1)).rotate(0.5)
        self.play(FadeOut(lab0), run_time=0.4)
        # on "tiny cells" a tiny cell drifts down and settles on the ledge (seen before it is named)
        self.at("tiny cells", lead=0.35)
        self.play(FadeIn(cell), run_time=0.25)
        self.play(cell.animate(path_arc=-0.6).rotate(-0.5).move_to(home), run_time=0.6)
        self.play(self.ripple(home, GREEN, r=0.25), run_time=0.2)
        # push in on it
        W.ramp("veil", 0.6, 0.9, delay=0.1)
        self.play(Resize(cell, 1 / TINY, stage), run_time=max(0.6, self.t_of("cyanobacteria") - 0.15 - self.elapsed()))
        name = cyano_label()
        self.play(FadeIn(name, shift=UP * 0.12), run_time=0.4)
        # two droplets of water drift in from the open sea, each holding two electrons
        d1, d2 = droplet(0.27).set_z_index(21), droplet(0.27).set_z_index(21)
        d1.move_to(P(3.3, 2.0))
        d2.move_to(P(4.4, 1.3))
        dots = list(d1[2]) + list(d2[2])
        for e in dots:
            e._o = P(0, 0)

        def jitter(ts):
            for k, e in enumerate(dots):
                o = 0.03 * P(math.sin(9 * ts + 1.7 * k), math.cos(11 * ts + 2.3 * k))
                e.shift(o - e._o)
                e._o = o
        W.fns.append(jitter)
        self.add(d1, d2)
        H1, H2 = cell.mouth_pt + P(0.3, 0.6), cell.mouth_pt + P(1.2, 0.2)
        self.play(d1.animate.move_to(H1), d2.animate.move_to(H2), run_time=max(0.5, self.t_of("pull electrons") - 0.35 - self.elapsed()), rate_func=rush_from)
        # pull electrons out of water: the mouth opens and both droplets go in
        self.play(Rotate(cell.lid, -1.25, about_point=cell.hinge_pt), run_time=0.25)
        I1, I2 = cpt(0.55, 0.0), cpt(1.6, 0.0)
        self.play(d1.animate(path_arc=0.5).move_to(I1), run_time=0.4)
        self.play(d2.animate(path_arc=0.5).move_to(I2), run_time=0.4)
        self.play(d1.animate.shift(UP * 0.06), d2.animate.shift(DOWN * 0.06), run_time=max(0.2, self.t_of("using sunlight") - 0.3 - self.elapsed()), rate_func=there_and_back)
        # using sunlight: a GOLD ray strikes the cell and the four electrons are pulled out and kept
        ytop = cpt(0, 1.3)[1]
        ray = VGroup(poly([(SUN[0] - 0.3, SUN[1] - 0.1), (SUN[0] + 0.1, SUN[1] - 0.3), (cpt(2.6, 0)[0], ytop), (cpt(-2.4, 0)[0], ytop)], GOLD, 0.3),
                     poly([(SUN[0] - 0.16, SUN[1] - 0.16), (SUN[0] + 0.0, SUN[1] - 0.24), (cpt(1.2, 0)[0], ytop), (cpt(-0.6, 0)[0], ytop)], "#FFE9A8", 0.35)
                     ).set_z_index(19)
        flash = sw_scale(RoundedRectangle(width=6.0, height=2.6, corner_radius=1.28, stroke_width=0, fill_color="#D9FFB0", fill_opacity=0.0), CELL_K
                         ).shift(CELL_C).set_z_index(20.5)
        self.add(flash)
        self.play(FadeIn(ray), flash.animate.set_fill(opacity=0.5), run_time=0.3)
        W.fns.remove(jitter)
        for d in (d1, d2):
            d.remove(d[2])
        self.add(*dots)
        for e in dots:
            e.set_z_index(21.5)
        kept = [cpt(-1.95, 0.4), cpt(-1.15, 0.4), cpt(-1.95, -0.4), cpt(-1.15, -0.4)]
        halos = [Dot(e.get_center(), radius=0.2, color=YELLOW).set_opacity(0.0).set_z_index(21.2) for e in dots]
        self.add(*halos)
        self.play(flash.animate.set_fill(opacity=0.0), d1[0].animate.set_fill(BLUE, opacity=0.7), d2[0].animate.set_fill(BLUE, opacity=0.7),
                  *[e.animate(path_arc=1.0).move_to(q) for e, q in zip(dots, kept)],
                  *[h.animate(path_arc=1.0).move_to(q).set_opacity(0.3) for h, q in zip(halos, kept)], run_time=0.9)
        self.remove(flash)
        pairs = VGroup(*halos, *dots)
        self.play(pairs.animate.scale(1.12), ray.animate.set_opacity(0.14), run_time=max(0.3, self.t_of("Their waste") - 0.5 - self.elapsed()), rate_func=there_and_back_with_pause)
        # their waste was oxygen: what is left of the water leaves the vent as one BLUE bubble
        bub = VGroup(Circle(radius=0.32, stroke_color="#BFEAF5", stroke_width=4, fill_color=BLUE, fill_opacity=0.95),
                     Arc(radius=0.2, start_angle=2.0, angle=0.9, stroke_color=WHITE, stroke_width=4).set_stroke(opacity=0.6)).set_z_index(21)
        bub.move_to(cell.vent_pt + UP * 0.3)
        self.play(ReplacementTransform(VGroup(d1, d2), bub), run_time=0.6)
        self.play(bub.animate.scale(1.12), run_time=0.4, rate_func=there_and_back)
        self.play(bub.animate.shift(UP * 0.24 + LEFT * 0.1), FadeOut(ray), FadeOut(name), run_time=0.45, rate_func=rush_from)
        # back on the ledge the cell becomes a mat, and the bubble the first of a steady stream
        W.ramp("veil", 0.0, 0.8)
        W.ramp("mat", 1.0, 1.0, delay=0.45)
        W.ramp("bub", 1.0, 0.8, delay=0.7)
        grp = VGroup(cell, pairs)
        self.play(Resize(grp, TINY, home), FadeOut(bub, shift=RIGHT * 0.4, scale=0.5), run_time=0.75)
        self.play(grp.animate.set_opacity(0), run_time=self.left(0.36))
        self.remove(grp)
        self.finish()


HB = P(0.15, 0.45)           # where the one bubble is met, in mid-water
HB_R = 1.25


class S03Twist(VScene):
    """The air does not fill: one bubble, four sockets, four iron discs, one flake. Then it is everywhere."""

    def construct(self):
        W = self.world(**ST2)
        # the air did not fill: the bar's sliver does not move
        self.at("did not fill", lead=0.3)
        halo = W.g_bar.copy().set_fill(opacity=0).set_stroke(WHITE, width=8, opacity=0.9).set_z_index(17)
        for _ in range(2):
            self.play(FadeIn(halo), self.ripple(P(G_IN + 0.05, G_Y), BLUE, r=0.26), run_time=0.35)
            self.play(FadeOut(halo), run_time=0.4)
        # push in on one bubble
        hb = hero_bubble(HB_R)
        glow, disc, socks, _ = hb
        socks.set_opacity(0)
        k0 = 0.07
        start = P(-1.0, LEDGE_Y + 0.4)
        hb.scale(k0).move_to(start).set_z_index(20)
        self.add(hb)
        W.ramp("veil", 0.62, 1.3, delay=0.5)
        self.play(hb.animate.shift(P(0.5, 0.45)), self.ripple(start, BLUE, r=0.2), run_time=0.6)
        self.play(hb.animate.scale(1 / k0).move_to(HB), run_time=max(0.8, self.t_of("strongly pulls in") - 0.55 - self.elapsed()))
        # oxygen strongly pulls in electrons: four empty sockets, each tugging at the water
        for sk in socks:
            sk[0].set_fill(opacity=0.95)
            sk[1].set_stroke(opacity=1)
        socks.set_opacity(0)
        self.play(*[sk[0].animate.set_fill(opacity=0.95) for sk in socks], *[sk[1].animate.set_stroke(opacity=1.0) for sk in socks], run_time=0.45)
        dirs = [P(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in SOCKET_ANG]
        motes = VGroup(*[Dot(ORIGIN, radius=0.05, color=TEXT).set_opacity(0) for _ in range(16)]).set_z_index(19.5)
        self.add(motes)
        tug = dict(on=1.0)

        def pull(ts):
            for i, m in enumerate(motes):
                k = i % 4
                u = (0.8 * ts + i * 0.27) % 1.0
                side = P(-dirs[k][1], dirs[k][0]) * (0.3 * math.sin(i * 2.4)) * (1 - u)
                m.move_to(HB + HB_R * (dirs[k] * lerp(1.75, 0.62, u * u) + side))
                m.set_fill(opacity=tug["on"] * 0.85 * math.sin(math.pi * u) ** 0.7)
        W.fns.append(pull)
        for sk in socks:
            self.play(sk[1].animate.set_stroke(YELLOW, width=6).scale(1.25), run_time=0.17)
            self.play(sk[1].animate.set_stroke(TEXT, width=3).scale(1 / 1.25), run_time=0.17)
        # that iron had electrons to give: four grey discs close in, yellow dots first
        self.at("that iron", lead=0.1)
        irons, idots, grp = [], [], []
        for d in dirs:
            c = HB + d * (HB_R + 0.72)
            g = iron_disc(0.5, dot=False).set_z_index(21)
            g[0].set_stroke(width=3)
            g.move_to(c)
            e = Dot(c - 0.5 * d, radius=0.15, color=YELLOW).set_z_index(21.5)
            pair = VGroup(g, e).shift(RIGHT * 3.6 * (1 if d[0] > 0 else -1))
            irons.append(g)
            idots.append(e)
            grp.append(pair)
        self.add(*grp)
        self.play(*[pr.animate.shift(LEFT * 3.6 * (1 if d[0] > 0 else -1)) for pr, d in zip(grp, dirs)], run_time=1.5, rate_func=rush_from)
        self.play(*[pr.animate.shift(0.13 * d) for pr, d in zip(grp, dirs)], run_time=max(0.3, self.t_of("handed them over") - 0.6 - self.elapsed()), rate_func=there_and_back)
        # the iron handed them over: four jumps; each disc turns RED as its dot leaves
        tug["on"] = 0.5
        for k in range(4):
            grp[k].remove(idots[k])
            self.add(idots[k])
            tgt = socks[k][0].get_center()
            self.play(idots[k].animate(path_arc=0.8).move_to(tgt), irons[k][0].animate.set_fill(RED).set_stroke("#FFB3AA"), run_time=0.3)
            self.play(self.ripple(tgt, YELLOW, r=0.3, z=23), run_time=0.14)
        tug["on"] = 0.0
        # turned into a kind of rust: the four red discs pull into one flake; the bubble is used up
        self.at("turned into", lead=0.0)
        flake = rust_flake(1.5).move_to(HB).set_z_index(21)
        self.play(ReplacementTransform(VGroup(*irons), flake), FadeOut(VGroup(glow, disc, socks, *idots), scale=0.2), FadeOut(motes), run_time=0.5)
        W.fns.remove(pull)
        lab = ochip("rust-like mineral", size=34, color=RED).move_to(HB + UP * 1.55).set_z_index(22)
        W.ramp("flakes", ST3["flakes"], 1.6, delay=0.2)
        self.play(FadeIn(lab, shift=UP * 0.12), flake.animate.rotate(0.25), run_time=0.3)
        self.play(flake.animate.rotate(-0.35), run_time=max(0.2, self.t_of("and sank") - 0.1 - self.elapsed()), rate_func=there_and_back)
        # and sank: it is happening everywhere, the whole height of the frame
        W.ramp("veil", 0.0, 1.0, delay=0.2)
        self.play(flake.animate.shift(DOWN * 1.9).scale(0.2).rotate(0.6), run_time=0.85, rate_func=rush_into)
        self.play(flake.animate.shift(DOWN * 0.7).rotate(0.4).set_opacity(0), FadeOut(lab), run_time=self.left(0.36), rate_func=linear)
        self.remove(flake)
        self.finish()


class S04Bands(VScene):
    """Ride the rust down to the sea floor: seven stripes stack up; we still mine them."""

    def construct(self):
        W = self.world(**ST3)
        self.play(self.zoom(CLOSE), run_time=max(0.5, self.t_of("helped build") - 0.1))
        W.ramp("stack", float(N_STRIPE), 2.4)
        self.wait(1.3)
        lab = self.scr(ochip("banded iron formation", size=34), 0.0, 1.6, CLOSE)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        # we still mine them: a bracket closes on the stack and a pick taps it
        self.at("still mine them", lead=0.45)
        top = (FLOOR_Y + N_STRIPE * STRIPE_H - CLOSE[0][1]) * 1.5          # screen y of the top of the stack
        hgt = top + 3.0 + 0.16
        b1 = self.scr(bracket(hgt, w=0.2, left=True, sw=6), -3.3, (top - 3.0) / 2, CLOSE)
        b2 = self.scr(bracket(hgt, w=0.2, left=False, sw=6), 3.3, (top - 3.0) / 2, CLOSE)
        pick = self.scr(pick_icon(2.3), 1.0, top + 0.72, CLOSE)
        s = CLOSE[1] / FW
        b1.shift(LEFT * 0.5 * s)
        b2.shift(RIGHT * 0.5 * s)
        self.play(b1.animate.shift(RIGHT * 0.5 * s), b2.animate.shift(LEFT * 0.5 * s), FadeIn(pick), run_time=0.4)
        tip = pick.get_corner(DL)
        for _ in range(2):
            self.play(Rotate(pick, 0.7, about_point=tip), run_time=0.2, rate_func=rush_into)
            self.play(Rotate(pick, -0.7, about_point=tip), self.ripple(tip + P(0.02, -0.02), TEXT, r=0.1), run_time=0.3)
        # the view starts back up the column
        self.play(self.zoom(DEEP), FadeOut(VGroup(b1, b2, pick, lab)), FadeIn(W.blocks), run_time=self.left(0.36))     # the land rock, for the next scene
        self.finish()


class S05Rise(VScene):
    """Other takers in the air; then oxygen rose, wavered, and stayed, still far below today's level."""

    def construct(self):
        W = self.world(**ST4)
        W.ramp("leak", 0.25, 0.4)
        # the readout's row is lent to the one label of this beat (the date comes back, changed, on "between about")
        ro = W.readout
        prep(ro)
        fade = lambda ts: seta(ro, 1.0 - clip01(ts / 0.5))
        W.fns.append(fade)
        for kind, tj in [("puff", 1.25), ("ring", 2.3), ("rock", 3.35), ("puff", 5.2), ("ring", 6.6), ("puff", 8.3)]:
            Take(W, kind, tj)
        # pull back and tilt up: the sky is twice as tall, and the three takers act across its width
        self.play(self.zoom(SKYCAM), run_time=1.1)
        self.at("took oxygen", lead=0.3)
        also = ochip("also took oxygen", size=34, pad=0.1)
        W.pin(also.move_to(P(0, ROW_B - 0.08)).set_z_index(16.5))
        self.play(FadeIn(also, shift=UP * 0.12 * W.s), run_time=0.35)
        self.at("between about", lead=0.75)
        W.unpin(also)
        self.play(FadeOut(also), run_time=0.3)
        W.fns.remove(fade)
        W.set_readout(RGOE, rt=0.45)
        # oxygen rose: pips that break the surface now stay and the bar climbs (no cause is drawn)
        self.at("oxygen rose", lead=0.2)
        W.ramp("leak", 0.5, 0.5)
        W.ramp("pips", 5.0, 1.1)
        W.ramp("gauge", 0.17, 1.0)
        self.at("wavered", lead=0.2)
        W.ramp("gauge", 0.05, 0.4)
        W.ramp("pips", 1.6, 0.4)
        self.wait(0.42)
        W.ramp("gauge", G_LOW, 0.45)
        W.ramp("pips", 5.0, 0.45)
        # and stayed: a low, steady level
        self.at("and stayed", lead=-0.05)
        self.play(FadeIn(W.g_tag2, shift=UP * 0.1 * W.s), self.ripple(W.c + W.s * P(G_IN + G_LOW * (G_TICK - G_IN), G_Y), BLUE, r=0.28 * W.s), run_time=0.5)
        # still far below today's level: the gap opens along the bar
        self.at("far below", lead=0.35)
        self.play(GrowFromCenter(W.arrow), run_time=0.6)
        halo = W.g_tick.copy().set_stroke(WHITE, width=7 * W.s).set_z_index(17.5)
        self.play(FadeIn(halo), W.g_today.animate.scale(1.12), run_time=0.4, rate_func=there_and_back)
        self.remove(halo)
        self.finish()


TRACE = [(-0.95, LEDGE_Y + 0.33), (0.25, 1.4), (0.95, 2.0), (0.62, SEA_Y)]      # then on to the sixth pip's place
FE_AT = P(1.2, 1.55)


class S06Payoff(VScene):
    """The air keeps what nothing else takes first. Then the clock reads today: your breath is what was left."""

    def construct(self):
        W = self.world(**ST5)
        Take(W, "ring", 3.2)
        hs = lambda x, y: W.c + W.s * P(x, y)          # a point of the bar (screen coordinates) under this framing
        t_arr = self.t_of("only keeps") - 0.35 + 1.8
        end = W.pip_at(5, W.t0 + t_arr)
        path = VMobject(stroke_color=BLUE, stroke_width=6).set_points_smoothly([P(*p) for p in TRACE] + [end]).set_z_index(19)
        fe = iron_disc(0.2).set_z_index(21)
        fe[0].set_stroke(width=1.5)
        fe[1].scale(1.3)
        fe.move_to(FE_AT + RIGHT * 1.2)
        self.add(fe)
        self.play(FadeOut(W.arrow), fe.animate.move_to(FE_AT), run_time=max(0.2, self.t_of("only keeps") - 0.35))
        # one bubble is traced from the mat, past the iron, through the surface, into the air
        b1 = pip(0.15).move_to(path.get_start()).set_z_index(21)
        self.add(b1)
        self.play(MoveAlongPath(b1, path), Create(path), run_time=1.8, rate_func=linear)
        W.v["pips"] = 6.0
        self.remove(b1)
        # a second bubble on the same path is taken by the iron half-way up
        half = VMobject().pointwise_become_partial(path, 0.0, 0.42)
        b2 = pip(0.15).move_to(path.get_start()).set_z_index(21)
        self.add(b2)
        self.play(MoveAlongPath(b2, half), fe.animate.move_to(half.get_end() + P(0.3, -0.12)), run_time=0.85, rate_func=linear)
        e = fe[1]
        fe.remove(e)
        self.add(e)
        e.set_z_index(22)
        self.play(e.animate(path_arc=1.0).move_to(b2.get_center()), fe[0].animate.set_fill(RED).set_stroke("#FFB3AA"), run_time=0.3)
        fl = rust_flake(0.32).move_to(fe.get_center()).set_z_index(21)
        self.play(FadeOut(b2, scale=0.3), FadeOut(e, scale=0.3), ReplacementTransform(fe, fl), run_time=0.3)
        prep(fl)
        t_f, p_f = W.ts, fl.get_center().copy()

        def sink(ts):
            u = ts - t_f
            put(fl, p_f + P(0.1 * math.sin(1.5 * u), -0.75 * u))
            seta(fl, clip01(1.6 - u * 0.7))
        W.fns.append(sink)
        # your next breath: the clock reads today
        self.at("your next breath", lead=0.35)
        W.ramp("iron", 0.0, 0.9)
        W.ramp("flakes", 0.0, 1.0)
        W.ramp("gauge2", 1.0, 1.0)
        W.ramp("pips", float(N_PIP), 1.5, delay=0.2)
        W.ramp("leak", 1.0, 0.5)
        new = W.readout_text(RNOW)
        old, W.readout = W.readout, new
        W.unpin(old)
        self.play(FadeOut(old, shift=UP * 0.14 * W.s), FadeIn(new, shift=UP * 0.14 * W.s), FadeOut(W.g_tag2), FadeOut(path), run_time=0.5)
        self.play(W.g_today.animate.scale(1.15), self.ripple(hs(G_TICK, G_Y), BLUE, r=0.3 * W.s), run_time=0.7, rate_func=there_and_back)
        # the view tilts up until the sky fills the upper half, and the bar is left behind. The move is over before the last
        # word, so the caption "Leftovers." sits on plain water
        W.fns.remove(sink)
        self.remove(fl)
        W.pinned = False
        W.hud_on = False                      # the bar stays where it is in the world and fades as the view leaves it
        W.ramp("pips2", 1.0, 0.9, delay=0.15)
        gone = [W.hud_bg, W.g_bar, W.g_fill, W.g_fill2, W.g_tick, W.g_head, W.g_today, W.g_tag, W.readout]
        self.play(self.zoom(SKYEND, run_time=1.15), *[FadeOut(m, run_time=0.45) for m in gone])
        # Leftovers: the pips of the whole sky drift toward the viewer and swell, at full blue, while the striped stack still
        # sits on the sea floor far below
        self.at("Leftovers", lead=0.25)
        W.ramp("swell", 1.0, 1.3)
        self.wait(self.left(0.36))
        self.finish()


class S07End(VScene):
    """End card over the dimmed, still-moving sky and sea as they stand today. The sentence and the address arrive
    together and hold for three seconds."""

    def construct(self):
        W = self.world(**ST6)
        W.ramp("veil2", 0.74, 0.45)
        a = Text("Every breath is oxygen", font=TITLE_FONT, font_size=48, color=TEXT, t2c={"oxygen": BLUE})
        b = Text("that nothing else", font=TITLE_FONT, font_size=48, color=TEXT)
        c = Text("took first.", font=TITLE_FONT, font_size=48, color=TEXT)
        line = fit(VGroup(a, b, c).arrange(DOWN, buff=0.3), max_w=7.0)
        sub = fit(T("Free at biochemistrypedia.com", size=34, color=TEAL), max_w=6.9)
        card = VGroup(line, sub).arrange(DOWN, buff=0.75)
        self.scr(card, 0.0, 1.2, SKYEND, z=41)
        self.play(FadeIn(card, shift=UP * 0.18), run_time=0.45)
        self.finish()
