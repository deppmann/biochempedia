"""Wnt: a signal that plugs the drain  (Biochemistrypedia explainer)

One idea: beta-catenin is made all the time and destroyed all the time, so a signal can raise it by
stopping the destruction. Timed to the SPOKEN words: every self.at("...") cue waits for that phrase
in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = beta-catenin (the discs, the bar, the water level)
  YELLOW = the Wnt signal (the ghost "signal", the Wnt blob, the plug that closes the drain)
  BLUE   = the receptor side: Frizzled, LRP, Dishevelled
  PURPLE = the destruction complex: Axin and its two kinases
  GOLD   = a phosphate (the little "P" badge)
  RED    = destruction and "off": the drain, the reader beta-TrCP, SCF, ubiquitin, the proteasome,
           Groucho, the gene reading OFF
  GREEN  = made and switched on: the tap, the source of new protein, the gene reading ON
  ORANGE = TCF on the DNA
  GREY   = tank walls, pipes, membranes, DNA, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BETA = TEAL           # beta-catenin
BASE = 0.4            # the resting water level in the tank (1x)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def pulse(c, color, s=1.1, **kw):
    """Indicate a bchip without recoloring its opaque backing (which would hide the label)."""
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def pbadge(r=0.23):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def disc(r=0.17, color=BETA):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95)


def ghost(text, color=YELLOW, size=26):
    """a dashed, unfilled chip: something that is not there yet / not named yet."""
    lab = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.44, height=lab.height + 0.44)
    return VGroup(DashedVMobject(box, num_dashes=30, dashed_ratio=0.55).set_color(color), lab)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, s=0.28, color=RED, w=8):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w))


def smooth_path(pts):
    p = VMobject()
    p.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
    return p


def arch(cx, base_y, half_w, height=1.0, leg=0.35, color=RED, n=36, p=3.0, w=9):
    """the 'reader': an arch that fits over two phosphate badges (a shape that acts, not a structure)."""
    pts = [[cx - half_w, base_y, 0], [cx - half_w, base_y + leg, 0]]
    for t in np.linspace(np.pi, 0, n + 2)[1:-1]:
        c, s = np.cos(t), np.sin(t)
        pts.append([cx + half_w * np.sign(c) * abs(c) ** (2 / p), base_y + leg + height * abs(s) ** (2 / p), 0])
    pts += [[cx + half_w, base_y + leg, 0], [cx + half_w, base_y, 0]]
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_smoothly([np.array(q, float) for q in pts])
    return m


def pile_positions(n, c=(-1.8, -2.4), rx=2.4, ry=0.55, seed=5, gap=0.4):
    rng = np.random.RandomState(seed)
    out = []
    tries = 0
    while len(out) < n and tries < 4000:
        tries += 1
        a, r = rng.uniform(0, 2 * np.pi), np.sqrt(rng.uniform(0, 1))
        p = np.array([c[0] + rx * r * np.cos(a), c[1] + ry * r * np.sin(a), 0])
        if all(np.linalg.norm(p - q) > gap for q in out):
            out.append(p)
    return out


# ---------------------------------------------------------------------------------------------
# the tank: a tap, a tank and a drain. Motion is computed, not scripted:
#   drops fall on a clock; the water level follows  dL/dt = c (BASE - k L)  (exact step), so the
#   steady level is BASE / k: slow the drain (k) ten-fold and the level rises ten-fold.
# ---------------------------------------------------------------------------------------------
class Tank:
    C = 4.0
    PIPE = 0.5
    N = 8

    def __init__(self, cx, cy, w, h, level=BASE, k=1.0, gate_color=RED, out_len=1.9, tap_len=2.0):
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        self.L, self.R = cx - w / 2, cx + w / 2
        self.floor, self.top = cy - h / 2, cy + h / 2
        self.lvl, self.k = ValueTracker(level), ValueTracker(k)
        self.tap_on, self.out_on = ValueTracker(0.0), ValueTracker(0.0)
        self.live = False
        self.out_len = out_len
        self.nozzle_x = cx - w / 4
        self.tap_y = self.top + 0.6
        self.dclock = self.oclock = 0.0

        # static parts -------------------------------------------------------------------------
        left = VMobject(stroke_color=GREY, stroke_width=6)
        left.set_points_as_corners([[self.L, self.top, 0], [self.L, self.floor, 0],
                                    [self.R + out_len, self.floor, 0]])
        right = VMobject(stroke_color=GREY, stroke_width=6)
        right.set_points_as_corners([[self.R, self.top, 0], [self.R, self.floor + self.PIPE, 0],
                                     [self.R + out_len, self.floor + self.PIPE, 0]])
        self.walls = VGroup(left, right)
        x0 = self.L - tap_len
        pipe = RoundedRectangle(corner_radius=0.1, width=self.nozzle_x + 0.25 - x0, height=0.3,
                                stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        pipe.move_to([(x0 + self.nozzle_x + 0.25) / 2, self.tap_y, 0])
        nozzle = Rectangle(width=0.34, height=0.24, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                           fill_opacity=0.35).move_to([self.nozzle_x, self.tap_y - 0.22, 0])
        self.tap = VGroup(pipe, nozzle)
        self.tap_x0 = x0

        # live parts ---------------------------------------------------------------------------
        def water_fn():
            lv = max(self.lvl.get_value(), 0.02)
            body = Rectangle(width=self.w - 0.1, height=lv, stroke_width=0, fill_color=BETA, fill_opacity=0.28)
            body.move_to([self.cx, self.floor + 0.03 + lv / 2, 0])
            top = Line([self.L + 0.05, self.floor + 0.03 + lv, 0], [self.R - 0.05, self.floor + 0.03 + lv, 0],
                       color=BETA, stroke_width=4)
            return VGroup(body, top)

        def gate_fn():
            op = self.PIPE * self.k.get_value()
            g = Rectangle(width=0.24, height=1.0, stroke_width=0, fill_color=gate_color, fill_opacity=0.95)
            return g.move_to([self.R, self.floor + op + 0.5, 0])

        self.water = always_redraw(water_fn)
        self.gate = always_redraw(gate_fn)

        self.drops = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=BETA, fill_opacity=0) for _ in range(self.N)])
        self.out = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=BETA, fill_opacity=0) for _ in range(self.N)])
        self.ctrl = Mobject()

        def drops_upd(m, dt):
            self.dclock += dt
            surf = self.floor + 0.03 + self.lvl.get_value()
            y0 = self.tap_y - 0.4
            on = self.tap_on.get_value()
            for i, d in enumerate(m):
                p = (self.dclock * 0.85 + i / self.N) % 1
                d.move_to([self.nozzle_x, y0 + (surf - y0) * p ** 1.5, 0])
                d.set_fill(BETA, opacity=on * min(1.0, p * 10))

        def out_upd(m, dt):
            self.oclock += dt
            flow = min(1.0, self.k.get_value() * self.lvl.get_value() / BASE) * self.out_on.get_value()
            xa, xb = self.R + 0.18, self.R + self.out_len - 0.2
            for i, d in enumerate(m):
                p = (self.oclock * 0.85 + i / self.N) % 1
                d.move_to([xa + (xb - xa) * p, self.floor + 0.25, 0])
                vis = max(0.0, min(1.0, flow * self.N - i))
                fade = 1.0 if p < 0.85 else (1 - p) / 0.15
                d.set_fill(interpolate_color(ManimColor(BETA), ManimColor(RED), min(1.0, p * 1.4)),
                           opacity=vis * min(1.0, p * 8) * fade)

        def ctrl_upd(m, dt):
            if self.live:
                k = max(self.k.get_value(), 1e-3)
                ss = BASE / k
                lv = ss + (self.lvl.get_value() - ss) * np.exp(-self.C * k * dt)
                self.lvl.set_value(min(lv, self.h - 0.45))

        self.drops.add_updater(drops_upd)
        self.out.add_updater(out_upd)
        self.ctrl.add_updater(ctrl_upd)

    def live_parts(self):
        return [self.water, self.gate, self.drops, self.out, self.ctrl]

    def marks(self, mults=(1, 10)):
        g = VGroup()
        for m in mults:
            y = self.floor + 0.03 + BASE * m
            g.add(DashedLine([self.L + 0.06, y, 0], [self.R - 0.06, y, 0], color=GREY, stroke_width=2.5,
                             dash_length=0.12),
                  T(f"{m}×", 24, GREY).move_to([self.L + 0.5, y + 0.26, 0]))
        return g


def big_tank(**kw):
    return Tank(1.6, -0.1, 4.2, 5.0, out_len=1.9, tap_len=2.0, **kw)


class S00Title(TitleCard):
    LESSON = "Wnt: Beta-Catenin and Planar Polarity"
    TITLE = "Wnt Plugs the Drain"


# ---------------------------------------------------------------------------------------------
class S01Waste(SpokenScene):
    """a tap pours beta-catenin in and a drain takes it out: made all day, destroyed soon after."""

    def construct(self):
        tank = big_tank()
        self.at("Why would")
        self.play(Create(tank.walls), FadeIn(tank.tap), run_time=0.9)
        self.add(*tank.live_parts())

        tap_lbl = T("made all day", 26, GREEN).move_to([-3.85, tank.tap_y, 0])
        self.at("make a protein")
        self.play(tank.tap_on.animate.set_value(1), FadeIn(tap_lbl, shift=RIGHT * 0.15), run_time=0.6)

        out_lbl = T("destroyed", 26, RED).move_to([tank.R + tank.out_len - 0.35, tank.floor - 0.45, 0])
        self.at("destroy it")
        self.play(tank.out_on.animate.set_value(1), FadeIn(out_lbl, shift=UP * 0.1), run_time=0.6)

        icon = disc().move_to([1.25, 2.0, 0])
        legend = T("β-catenin", 26, BETA).next_to(icon, RIGHT, buff=0.2)
        self.at("a protein called")
        self.play(FadeIn(icon, scale=0.5), FadeIn(legend, shift=RIGHT * 0.1), run_time=0.5)

        sig = ghost("signal", YELLOW, 26).move_to([4.95, 0.1, 0])
        stop = inhib([4.95, -0.4, 0], [4.7, -1.78, 0], YELLOW, 5)
        self.at("Unless a signal")
        self.play(FadeIn(sig, shift=DOWN * 0.15), run_time=0.6)
        self.at("tells them to stop")
        self.play(Create(stop), run_time=0.6)

        # one drop followed from the tap to the drain: soon after it is made
        tr = disc(0.17).move_to([tank.nozzle_x, tank.tap_y - 0.4, 0])
        tr.set_stroke(GOLD, 4)
        self.at("free copies")
        self.add(tr)
        self.play(tr.animate.move_to([tank.nozzle_x, tank.floor + 0.35, 0]), run_time=0.7, rate_func=rush_into)
        self.play(tr.animate.move_to([tank.R + 0.2, tank.floor + 0.25, 0]), run_time=0.45, rate_func=linear)
        self.play(tr.animate.move_to([tank.R + tank.out_len - 0.3, tank.floor + 0.25, 0]).set_fill(RED, 0.95).set_stroke(RED, 4),
                  run_time=0.4, rate_func=linear)
        self.play(FadeOut(tr, scale=0.4), run_time=0.15)

        waste = T("waste?", 58, RED, font=TITLE_FONT).move_to([-3.4, 0.1, 0])
        self.at("looks like waste")
        self.play(FadeIn(waste, shift=UP * 0.15), run_time=0.5)
        design = T("a design", 58, TEXT, font=TITLE_FONT).move_to([-3.4, 0.1, 0])
        under = Line(design.get_corner(DL) + DOWN * 0.12, design.get_corner(DR) + DOWN * 0.12, color=GOLD, stroke_width=5)
        self.at("a design")
        self.play(ReplacementTransform(waste, design), Create(under), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tub(SpokenScene):
    """the same tank; level = synthesis / destruction; slow the drain ten-fold and the level rises ten-fold."""

    def construct(self):
        tank = big_tank()
        tank.tap_on.set_value(1)
        tank.out_on.set_value(1)
        tap_lbl = T("made all day", 26, GREEN).move_to([-3.85, tank.tap_y, 0])
        out_lbl = T("destroyed", 26, RED).move_to([tank.R + tank.out_len - 0.35, tank.floor - 0.45, 0])
        icon = disc().move_to([1.25, 2.0, 0])
        legend = T("β-catenin", 26, BETA).next_to(icon, RIGHT, buff=0.2)
        design = T("a design", 58, TEXT, font=TITLE_FONT).move_to([-3.4, 0.1, 0])
        under = Line(design.get_corner(DL) + DOWN * 0.12, design.get_corner(DR) + DOWN * 0.12, color=GOLD, stroke_width=5)
        self.add(tank.walls, tank.tap, *tank.live_parts(), tap_lbl, out_lbl, icon, legend, design, under)

        self.at("Picture a bathtub")
        self.play(FadeOut(VGroup(design, under)), run_time=0.5)
        self.at("the tap running")
        self.play(Indicate(tank.tap, color=GREEN, scale_factor=1.04), pulse_text(tap_lbl, GREEN), run_time=0.8)
        self.at("the drain open")
        self.play(Indicate(tank.gate, color=RED, scale_factor=1.3), pulse_text(out_lbl, RED), run_time=0.8)
        self.at("depends on both")
        self.play(Indicate(tank.water, color=BETA, scale_factor=1.03), run_time=0.8)

        lv = T("steady level", 32, BETA)
        eq = T("=", 34, TEXT)
        num = T("rate of synthesis", 28, GREEN)
        den = T("rate constant of destruction", 28, RED)
        bar = Line(LEFT * (den.width + 0.3) / 2, RIGHT * (den.width + 0.3) / 2, color=TEXT, stroke_width=3)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.16)
        block = VGroup(lv, eq, frac).arrange(DOWN, buff=0.3).move_to([-3.45, 0.15, 0])
        self.at("The steady level")
        self.play(FadeIn(lv, shift=RIGHT * 0.15), FadeIn(eq), run_time=0.5)
        self.at("rate of synthesis")
        self.play(FadeIn(num, shift=DOWN * 0.15), run_time=0.5)
        self.at("divided by")
        self.play(Create(bar), run_time=0.4)
        self.at("rate constant")
        self.play(FadeIn(den, shift=UP * 0.15), run_time=0.5)

        marks = tank.marks()
        self.at("Slow the destruction")
        tank.live = True
        self.play(tank.k.animate.set_value(0.1), FadeIn(marks), run_time=1.6, rate_func=smooth)
        self.at("level rises")
        self.play(Indicate(marks[3], color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("no change")
        self.play(Indicate(tank.tap, color=GREEN, scale_factor=1.04), pulse_text(tap_lbl, GREEN), run_time=0.9)
        self.finish()


def pulse_text(t, color, s=1.12):
    return Indicate(t, color=color, scale_factor=s)


# ---------------------------------------------------------------------------------------------
class S03Drain(SpokenScene):
    """inside the drain: the destruction complex marks beta-catenin, a reader grips two phosphates,
    SCF adds ubiquitin, the proteasome destroys it."""

    def construct(self):
        SITES = {33: -1.95, 37: -0.65, 41: 0.65, 45: 1.95}
        BAR_Y, RING_Y = 0.6, 1.45

        # --- state label: a cell that receives no signal ---------------------------------------
        sig = ghost("signal", YELLOW, 26).move_to([5.0, 3.0, 0])
        no = T("no", 26, RED, weight=BOLD).next_to(sig, LEFT, buff=0.2)
        self.at("receives no signal")
        self.play(FadeIn(sig, shift=DOWN * 0.1), FadeIn(no, shift=DOWN * 0.1), run_time=0.5)

        # --- beta-catenin bar with four sites ----------------------------------------------------
        bar = RoundedRectangle(corner_radius=0.2, width=5.6, height=0.9, stroke_color=BETA, stroke_width=3,
                               fill_color=BETA, fill_opacity=0.25).move_to([0, BAR_Y, 0])
        bar_lbl = T("β-catenin", 28, BETA).move_to(bar)
        rings, nums, stems = VGroup(), VGroup(), VGroup()
        for n, x in SITES.items():
            ring = DashedVMobject(Circle(radius=0.23), num_dashes=12, dashed_ratio=0.55).set_color(GOLD)
            ring.set_stroke(opacity=0.7).move_to([x, RING_Y, 0])
            stems.add(Line([x, BAR_Y + 0.45, 0], [x, RING_Y - 0.23, 0], color=BETA, stroke_width=3))
            rings.add(ring)
            nums.add(T(str(n), 22, GREY).move_to([x, BAR_Y - 0.8, 0]))
        marked = VGroup(bar, bar_lbl, stems, rings, nums)
        self.at("Every free copy")
        self.play(FadeIn(marked, shift=RIGHT * 0.5), run_time=0.8)

        # --- the destruction complex: box, Axin scaffold, two kinase slots ------------------------
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=11.4, height=2.5), num_dashes=70,
                             dashed_ratio=0.6).set_color(PURPLE).move_to([0, -1.85, 0])
        box_lbl = btext("destruction complex", 24, PURPLE).move_to([-3.75, -0.6, 0])
        axin = Rectangle(width=10.2, height=0.5, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                         fill_opacity=0.3).move_to([0, -2.55, 0])
        axin_lbl = T("Axin", 24, PURPLE).move_to([-1.3, -2.55, 0])
        stalk = Rectangle(width=0.22, height=BAR_Y - 0.45 + 2.3, stroke_width=0, fill_color=PURPLE, fill_opacity=0.5)
        stalk.move_to([0, ((BAR_Y - 0.45) + (-2.3)) / 2, 0])
        slot_l = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=1.8, height=0.78), num_dashes=22,
                                dashed_ratio=0.55).set_color(PURPLE).move_to([-4.0, -1.55, 0])
        slot_r = slot_l.copy().move_to([4.0, -1.55, 0])
        self.at("the destruction complex")
        self.play(Create(box), FadeIn(box_lbl), run_time=0.8)
        self.at("the scaffold")
        self.play(FadeIn(axin, shift=UP * 0.1), FadeIn(axin_lbl), GrowFromEdge(stalk, DOWN), run_time=0.8)
        self.at("holds two")
        self.play(Create(slot_l), Create(slot_r), run_time=0.6)

        ck1 = bchip("CK1", PURPLE, 26).move_to([4.0, -1.55, 0])
        gsk = bchip("GSK3", PURPLE, 26).move_to([-4.0, -1.55, 0])
        self.at("beside it")
        self.play(FadeOut(slot_r), FadeIn(ck1, scale=0.8), run_time=0.5)

        def path_to(start, site_x, side):
            top_y = 2.15
            sx = start[0] + side * 0.55
            return smooth_path([(start[0], start[1]), (sx, 0.3), (sx - side * 0.2, 1.9), (min(max(site_x, -2.4), 2.4) + 0.0, top_y),
                                (site_x, RING_Y)])

        badges = {}
        for n in SITES:
            b = pbadge().set_z_index(6)
            badges[n] = b

        self.at("puts a phosphate")
        b45 = badges[45].move_to(ck1.get_center())
        self.add(b45)
        self.play(MoveAlongPath(b45, path_to(ck1.get_center(), SITES[45], +1)), run_time=1.0, rate_func=smooth)
        self.at("which primes")
        self.play(FadeOut(slot_l), FadeIn(gsk, scale=0.8), run_time=0.5)
        self.play(pulse(gsk, PURPLE, 1.12), run_time=0.5)

        self.at("add three more")
        flights = []
        for j, n in enumerate((41, 37, 33)):
            b = badges[n].move_to(gsk.get_center())
            self.add(b)
            flights.append(MoveAlongPath(b, path_to(gsk.get_center(), SITES[n], -1)))
        self.play(LaggedStart(*flights, lag_ratio=0.3), run_time=1.5, rate_func=smooth)

        # --- the reader: an arch that closes over the phosphates at 37 and 33 ----------------------
        cx_arch = (SITES[33] + SITES[37]) / 2
        open_arch = arch(cx_arch, 1.12, 1.45).shift(UP * 0.9)
        closed_arch = arch(cx_arch, 1.12, 1.22)
        tr_lbl = T("β-TrCP", 28, RED).move_to([cx_arch - 2.75, 1.95, 0])
        self.at("A protein called")
        self.play(VGroup(box, box_lbl, axin, axin_lbl, stalk, ck1, gsk).animate.set_opacity(0.22),
                  FadeIn(open_arch), FadeIn(tr_lbl, shift=RIGHT * 0.15), run_time=0.9)
        self.at("reads the phosphates")
        self.play(open_arch.animate.shift(DOWN * 0.9), run_time=0.5)
        self.play(Transform(open_arch, closed_arch), run_time=0.35)
        self.at("on serines")
        self.play(Indicate(VGroup(badges[33], badges[37]), color=GOLD, scale_factor=1.3), run_time=0.9)

        # --- SCF adds ubiquitin ---------------------------------------------------------------------
        scf = bchip("SCF ligase", RED, 26).move_to([cx_arch, 3.05, 0])
        link = Line([cx_arch, 2.48, 0], [cx_arch, 2.72, 0], color=RED, stroke_width=6)
        self.at("belongs to")
        self.play(FadeIn(scf, shift=DOWN * 0.15), Create(link), run_time=0.6)

        chain_pts = [(0.5, 3.05), (1.4, 2.8), (2.3, 2.4)]
        ubs = VGroup()
        for x, y in chain_pts:
            c = Circle(radius=0.27, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.25).move_to([x, y, 0])
            ubs.add(VGroup(c, T("Ub", 22, RED).move_to(c)))
        links = VGroup(Line(scf.get_right(), ubs[0].get_left(), color=RED, stroke_width=3),
                       Line(ubs[0].get_center() + [0.2, -0.1, 0], ubs[1].get_center() + [-0.2, 0.08, 0], color=RED, stroke_width=3),
                       Line(ubs[1].get_center() + [0.2, -0.1, 0], ubs[2].get_center() + [-0.2, 0.08, 0], color=RED, stroke_width=3),
                       Line(ubs[2].get_center() + [0.1, -0.25, 0], [2.65, BAR_Y + 0.5, 0], color=RED, stroke_width=3))
        self.at("adds a chain")
        self.play(Create(links[0]), FadeIn(ubs[0], scale=0.5), run_time=0.4)
        self.play(Create(links[1]), FadeIn(ubs[1], scale=0.5), run_time=0.4)
        self.play(Create(links[2]), FadeIn(ubs[2], scale=0.5), Create(links[3]), run_time=0.4)

        # --- the proteasome ---------------------------------------------------------------------------
        pbox = RoundedRectangle(corner_radius=0.25, width=7.4, height=1.5, stroke_color=RED, stroke_width=4,
                                fill_color=RED, fill_opacity=0.14).move_to([0, -2.35, 0])
        plbl = T("proteasome", 32, RED).move_to(pbox)
        group_marked = VGroup(marked, *badges.values(), ubs, *links[1:])
        self.at("and the proteasome")
        self.play(FadeOut(VGroup(box, box_lbl, axin, axin_lbl, stalk, ck1, gsk, open_arch, tr_lbl, scf, link, links[0], sig, no)),
                  run_time=0.5)
        self.play(FadeIn(pbox, shift=UP * 0.3), FadeIn(plbl), run_time=0.6)
        self.at("destroys the protein")
        self.play(group_marked.animate.scale(0.3).move_to(pbox.get_top() + DOWN * 0.1).set_opacity(0),
                  run_time=1.3, rate_func=rush_into)
        self.play(Indicate(VGroup(pbox, plbl), color=RED, scale_factor=1.04), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
SRC_X, LANE_Y = -5.0, -2.07
CPLX0 = np.array([0.2, -1.7, 0.0])
CPLX1 = np.array([1.0, 0.15, 0.0])
SCF_POS = np.array([5.0, -2.07, 0.0])
TAIL_END = np.array([-1.9, 0.45, 0.0])


def make_complex(center):
    box = RoundedRectangle(corner_radius=0.3, width=4.6, height=2.5)
    back = box.copy().set_stroke(width=0).set_fill(BG, 1)
    dbox = DashedVMobject(box, num_dashes=40, dashed_ratio=0.6).set_color(PURPLE)
    axin = Rectangle(width=4.0, height=0.45, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                     fill_opacity=0.3).move_to([0, -0.9, 0])
    axin_lbl = T("Axin", 22, PURPLE).move_to(axin)
    ck1 = chip("CK1", PURPLE, 22, pad=0.16).move_to([1.2, 0.25, 0])
    gsk = chip("GSK3", PURPLE, 22, pad=0.16).move_to([-1.2, 0.25, 0])
    lbl = T("destruction complex", 22, PURPLE).move_to([0, 0.98, 0])
    g = VGroup(back, dbox, axin, axin_lbl, ck1, gsk, lbl)
    g.axin = axin
    return g.move_to(center)


class S04Wnt(SpokenScene):
    """Wnt binds Frizzled and LRP; Dishevelled and the LRP tail pull the destruction complex to the receptor;
    the line to the ligase is cut; new beta-catenin piles up."""

    def construct(self):
        MEM_Y = 1.9
        # --- the cell as it was: the assembly line from S03 (made -> complex -> ligase -> gone) ---------
        mem = Rectangle(width=12.6, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.35).move_to([0, MEM_Y, 0])
        out_t = T("outside", 22, GREY).move_to([5.5, MEM_Y + 0.55, 0])
        in_t = T("inside", 22, GREY).move_to([5.5, MEM_Y - 0.55, 0])
        cplx = make_complex(CPLX0)
        scf = bchip("SCF ligase", RED, 26).move_to(SCF_POS)
        src = arr([-6.1, LANE_Y, 0], [-5.3, LANE_Y, 0], GREEN)
        src_lbl = T("made", 24, GREEN).move_to([-5.7, LANE_Y - 0.5, 0])

        def line_arrow_fn():
            a = np.array([cplx.get_right()[0], cplx.get_center()[1] - 0.37, 0])
            b = scf.get_left() + [0, 0, 0]
            return arr(a + [0.05, 0, 0], b - [0.08, 0, 0], PURPLE, 4, 0.2)

        deliver = always_redraw(line_arrow_fn)
        self.add(mem, out_t, in_t, cplx, scf, src, src_lbl, deliver)

        discs = [disc() for _ in range(3)]
        runs = []
        for d in discs:
            d.move_to([SRC_X, LANE_Y, 0])
            runs.append(Succession(FadeIn(d, scale=0.5, run_time=0.2),
                                   d.animate(run_time=0.75, rate_func=linear).move_to([-1.3, LANE_Y, 0]),
                                   d.animate(run_time=0.2).set_stroke(GOLD, 4),
                                   d.animate(run_time=0.85, rate_func=linear).move_to([3.75, LANE_Y, 0]),
                                   FadeOut(d, scale=0.3, run_time=0.2)))

        # --- Wnt arrives -----------------------------------------------------------------------------------
        wnt = VGroup(Circle(radius=0.42, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.3),
                     T("Wnt", 24, YELLOW)).move_to([-5.4, 3.0, 0])
        self.at("That signal")
        self.play(FadeIn(wnt, shift=RIGHT * 0.3), LaggedStart(*runs, lag_ratio=0.5), run_time=3.4)
        self.at("nearby cell reads")
        self.play(wnt.animate.move_to([-3.3, 3.0, 0]), run_time=0.7)

        fz = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.5, stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.3).move_to([-3.3, MEM_Y, 0])
        fz_lbl = T("Frizzled", 24, BLUE).move_to([-4.85, 2.85, 0])
        lrp = RoundedRectangle(corner_radius=0.2, width=0.5, height=1.4, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([0.5, MEM_Y, 0])
        lrp_lbl = T("LRP5/6", 24, BLUE).move_to([-0.2, 2.9, 0])
        self.at("Its receptor is")
        self.play(FadeIn(fz, shift=DOWN * 0.15), FadeIn(fz_lbl, shift=RIGHT * 0.1), run_time=0.6)
        self.play(wnt.animate.move_to([-3.3, 2.95, 0]), run_time=0.4)
        self.at("brings it together")
        self.play(FadeIn(lrp, shift=LEFT * 0.2), run_time=0.4)
        self.play(lrp.animate.move_to([-1.9, MEM_Y, 0]), wnt.animate.move_to([-2.6, 2.95, 0]),
                  lrp_lbl.animate.move_to([-0.95, 2.9, 0]).set_opacity(1), run_time=1.5)
        self.play(Indicate(VGroup(fz, lrp), color=BLUE, scale_factor=1.12), run_time=0.9)

        dsh = bchip("Dishevelled", BLUE, 24).move_to([-4.2, 0.55, 0])
        dlink = Line([-3.3, MEM_Y - 0.75, 0], [-3.3, 0.55 + 0.1, 0], color=BLUE, stroke_width=4)
        self.at("recruits a protein")
        self.play(FadeIn(dsh, shift=UP * 0.2), Create(dlink), run_time=0.6)

        tail = Line([-1.9, MEM_Y - 0.7, 0], TAIL_END + [0, 0.22, 0], color=BLUE, stroke_width=5)
        self.at("the tail of")
        self.play(Create(tail), run_time=0.5)
        pb = pbadge().move_to(TAIL_END)
        self.at("is phosphorylated")
        self.play(FadeIn(pb, scale=0.4), run_time=0.4)

        def rope_fn():
            tx = cplx.get_left()[0]
            ty = min(max(TAIL_END[1], cplx.get_center()[1] - 0.8), cplx.get_center()[1] + 1.0)
            return Line(TAIL_END + [0.23, 0, 0], [tx, ty, 0], color=PURPLE, stroke_width=5)

        rope = always_redraw(rope_fn)
        self.at("then binds")
        self.play(Create(rope), run_time=0.6)
        self.play(Indicate(cplx.axin, color=PURPLE, scale_factor=1.05), run_time=0.5)

        # --- the complex is pulled to the receptor ----------------------------------------------------------
        self.at("is pulled")
        self.play(cplx.animate.move_to(CPLX1), run_time=1.5, rate_func=smooth)
        x_mid = (cplx.get_right() + scf.get_left()) / 2
        xmark = cross([4.0, -0.9, 0], 0.26, RED, 8)
        self.at("stops delivering")
        self.play(Create(xmark), run_time=0.4)
        self.at("to the ligase")
        self.play(pulse(scf, RED, 1.08), run_time=0.8)
        q = T("?", 44, GREY).move_to([4.95, -0.55, 0])
        self.at("still argued")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)

        # --- beta-catenin piles up ------------------------------------------------------------------------
        pos = pile_positions(13)
        newd = [disc().move_to([SRC_X, LANE_Y, 0]) for _ in pos]
        moves = [Succession(FadeIn(d, scale=0.5, run_time=0.15), d.animate(run_time=0.9).move_to(p))
                 for d, p in zip(newd, pos)]
        pile_lbl = T("β-catenin", 26, BETA).move_to([-1.8, -3.2, 0])
        self.at("newly made")
        self.play(LaggedStart(*moves, lag_ratio=0.14), Succession(Wait(1.9), FadeIn(pile_lbl, shift=UP * 0.1)))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tcf(SpokenScene):
    """the nucleus: TCF holds Groucho on the DNA (gene off); beta-catenin displaces Groucho and brings in
    the proteins that start transcription (gene on)."""

    def construct(self):
        # the pile carried over from S04
        pos = pile_positions(13)
        pile = VGroup(*[disc().move_to(p) for p in pos])
        pile_lbl = T("β-catenin", 26, BETA).move_to([-1.8, -3.2, 0])
        self.add(pile, pile_lbl)

        nuc = RoundedRectangle(corner_radius=0.8, width=12.0, height=4.8, stroke_color=GREY, stroke_width=4).move_to([0, 1.0, 0])
        nuc_lbl = T("nucleus", 24, GREY).move_to([-5.0, 3.0, 0])
        DNA_Y = -0.35
        dna = Line([-5.5, DNA_Y, 0], [5.5, DNA_Y, 0], color=GREY, stroke_width=9)
        self.at("In the nucleus")
        self.play(Create(nuc), FadeIn(nuc_lbl), Create(dna), run_time=0.8)

        tcf = bchip("TCF", ORANGE, 42).move_to([0.2, DNA_Y + 0.62, 0])
        self.at("a protein called")
        self.play(FadeIn(tcf, shift=DOWN * 0.3), run_time=0.6)
        gene = RoundedRectangle(corner_radius=0.15, width=3.4, height=0.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.3).move_to([3.5, DNA_Y, 0])
        gene_lbl = T("target genes", 26, GREY).move_to([3.5, DNA_Y - 0.58, 0])
        self.at("binds the DNA")
        self.play(Indicate(dna, color=TEXT, scale_factor=1.0), tcf.animate.shift(DOWN * 0.07), run_time=0.8)
        self.at("target genes")
        self.play(FadeIn(gene), FadeIn(gene_lbl, shift=UP * 0.1), run_time=0.6)

        sig = ghost("signal", YELLOW, 26).move_to([4.7, -2.5, 0])
        self.at("before a signal")
        self.play(FadeIn(sig, shift=DOWN * 0.1), Indicate(tcf[1:], color=ORANGE, scale_factor=1.08), run_time=0.7)
        self.play(FadeOut(sig), run_time=0.55)
        self.play(FadeIn(sig), run_time=0.55)
        self.play(FadeOut(sig), run_time=0.55)

        TOP_Y = DNA_Y + 1.95
        gro = bchip("Groucho", RED, 36).move_to([0.2, TOP_Y, 0])
        glink = Line(tcf.get_top(), gro.get_bottom(), color=RED, stroke_width=6)
        self.at("holds a")
        self.play(FadeIn(gro, shift=DOWN * 0.3), Create(glink), run_time=0.6)
        off = T("OFF", 40, RED, weight=BOLD).move_to([3.5, DNA_Y + 0.85, 0])
        self.at("keeps those genes")
        self.play(FadeIn(off, scale=0.7), run_time=0.5)

        # beta-catenin arrives, takes Groucho's place, and brings in the transcription proteins
        bcat = bchip("β-catenin", BETA, 36).move_to([-3.4, TOP_Y - 0.2, 0])
        self.at("simple model")
        self.play(Indicate(pile, color=BETA, scale_factor=1.05), run_time=0.6)
        self.at("enters the nucleus")
        rise = [d.animate(run_time=0.9).move_to([-3.4 + 0.12 * (i - 2.5), TOP_Y - 0.2, 0]).set_opacity(0.0)
                for i, d in enumerate(list(pile)[:6])]
        self.play(LaggedStart(*rise, lag_ratio=0.1), FadeIn(bcat, scale=0.6), run_time=1.2)
        self.at("pushes Groucho off")
        self.play(bcat.animate.move_to([0.2, TOP_Y, 0]),
                  gro.animate.shift(UP * 0.7 + LEFT * 2.6).set_opacity(0),
                  FadeOut(glink), run_time=0.8)
        blink = Line(tcf.get_top(), bcat.get_bottom(), color=BETA, stroke_width=6)
        self.add(blink)
        tp = bchip("transcription proteins", GREEN, 28).move_to([4.2, TOP_Y + 1.15, 0])
        self.at("brings in")
        self.play(FadeIn(tp, shift=LEFT * 0.4), run_time=0.4)
        self.play(tp.animate.move_to([0.2, TOP_Y + 1.15, 0]), run_time=0.6)
        on = T("ON", 40, GREEN, weight=BOLD).move_to([3.5, DNA_Y + 0.85, 0])
        self.at("start transcription")
        self.play(ReplacementTransform(off, on), run_time=0.6)

        rep = T("repressor", 28, RED).move_to([-4.85, DNA_Y + 0.62, 0])
        act = T("activator", 28, GREEN).move_to([-1.9, DNA_Y + 0.62, 0])
        mid = arr([-3.95, DNA_Y + 0.62, 0], [-3.0, DNA_Y + 0.62, 0], TEXT, 4, 0.2)
        self.at("from a repressor")
        self.play(FadeIn(rep, shift=UP * 0.1), run_time=0.5)
        self.at("into an activator")
        self.play(GrowArrow(mid), FadeIn(act, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """two tanks, one tap each: no signal (drain open, low) and Wnt (drain plugged, high)."""

    def construct(self):
        left = Tank(-3.3, 0.3, 3.6, 4.6, out_len=1.0, tap_len=1.0)
        right = Tank(3.3, 0.3, 3.6, 4.6, gate_color=YELLOW, out_len=1.0, tap_len=1.0)
        for t in (left, right):
            t.tap_on.set_value(1)
            t.out_on.set_value(1)
        l_lbl = T("no signal", 28, GREY).move_to([left.cx, left.floor - 0.45, 0])
        r_lbl = T("Wnt", 28, YELLOW, weight=BOLD).move_to([right.cx, right.floor - 0.45, 0])

        self.at("Without a signal")
        self.play(Create(left.walls), FadeIn(left.tap), FadeIn(l_lbl), run_time=0.8)
        self.add(*left.live_parts())
        self.at("stays open")
        self.play(Indicate(left.gate, color=RED, scale_factor=1.3), run_time=0.7)
        self.at("level stays low")
        self.play(Indicate(left.water, color=BETA, scale_factor=1.03), run_time=0.7)

        self.at("With")
        self.play(Create(right.walls), FadeIn(right.tap), FadeIn(r_lbl), run_time=0.8)
        self.add(*right.live_parts())
        self.at("is plugged")
        right.live = True
        self.play(right.k.animate.set_value(0.1), run_time=1.4, rate_func=smooth)
        self.play(Indicate(right.gate, color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("on destruction")
        self.play(Indicate(left.gate, color=RED, scale_factor=1.3), Indicate(right.gate, color=YELLOW, scale_factor=1.3),
                  run_time=0.8)
        self.at("not on synthesis")
        self.play(Indicate(left.tap, color=GREEN, scale_factor=1.04), Indicate(right.tap, color=GREEN, scale_factor=1.04),
                  run_time=0.8)
        self.at("always made")
        self.play(Indicate(left.tap, color=GREEN, scale_factor=1.04), Indicate(right.tap, color=GREEN, scale_factor=1.04),
                  run_time=0.6)
        self.at("always destroyed")
        self.play(Indicate(left.gate, color=RED, scale_factor=1.3), Indicate(right.gate, color=YELLOW, scale_factor=1.3),
                  run_time=0.6)
        ring = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=5).move_to(right.gate.get_center())
        self.at("one move")
        self.play(Create(ring), run_time=0.6)
        rule = T("Stop the destruction.", 44, TEXT, font=TITLE_FONT).move_to([0, -3.25, 0])
        self.at("Stop the destruction")
        self.play(Write(rule), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Stop the destruction, and the level rises."
