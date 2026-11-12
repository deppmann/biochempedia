"""Osmoregulation, chapter 2: Where Does a Seabird's Salt Go?
Same world as chapter 1 (../scenes.py): water BLUE, sodium chloride ORANGE, outlines light grey,
DASHED arrow = passive leak, SOLID arrow + ATP tag = paid transport, the In / Out ledger bottom right.
The bird lives in the left-hand panel where the fish tank was."""
import importlib.util, math, os, sys
from pathlib import Path
import numpy as np
from bp_style import *

_here = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
_spec = importlib.util.spec_from_file_location("osmo_film1", _here.parent / "scenes.py")
F = importlib.util.module_from_spec(_spec)
sys.modules["osmo_film1"] = F
_spec.loader.exec_module(F)
for _n in ("ORANGE OUTL FILL TMAO_C TOP_W TOP_S BOT_W BOT_S TANK_L TANK_R TANK_T TANK_B P jitter flow dashed solid "
           "atp_chip solid_pair World Ledger mini RefLine RefPoly RefRect Tube sea_leaks").split():
    globals()[_n] = getattr(F, _n)

BC, BS = (-3.3, -0.9), 1.1          # the cormorant: centre of its body and scale
GREYL = "#7F8896"


def Q(x, y, s=BS, c=BC):
    return P(c[0] + x * s, c[1] + y * s)


def bird(s=BS, c=BC):
    kw = dict(color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1)
    q = lambda x, y: Q(x, y, s, c)
    tail = Polygon(q(-1.5, 0.15), q(-3.0, -0.05), q(-2.95, -0.35), q(-1.5, -0.5), **kw)
    neck = Polygon(q(0.7, 0.6), q(1.45, 0.7), q(1.95, 1.75), q(1.45, 1.8), **kw)
    body = Ellipse(width=3.4 * s, height=1.8 * s, **kw).move_to(q(0, 0))
    head = Ellipse(width=0.95 * s, height=0.62 * s, **kw).move_to(q(1.75, 1.95))
    bill = Polygon(q(2.1, 2.08), q(3.0, 2.0), q(3.12, 1.84), q(2.95, 1.8), q(2.1, 1.82), **kw)
    eye = Dot(q(1.95, 2.06), radius=0.07 * s, color=TEXT)
    wing = ArcBetweenPoints(q(-1.0, 0.25), q(0.5, 0.1), angle=-1.0, color=GREYL, stroke_width=4)
    g = VGroup(tail, neck, body, head, bill, eye, wing).set_z_index(3)
    g.tip, g.vent, g.q = q(3.05, 1.9), q(-1.35, -0.5), q
    return g


def gull(s=1.3, c=(-3.3, -0.7)):
    kw = dict(color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1)
    q = lambda x, y: P(c[0] + x * s, c[1] + y * s)
    tail = Polygon(q(-1.6, 0.1), q(-2.8, -0.05), q(-2.8, -0.4), q(-1.6, -0.4), **kw)
    neck = Polygon(q(0.9, 0.35), q(1.5, 0.45), q(1.95, 0.7), q(1.45, 1.0), **kw)
    body = Ellipse(width=3.4 * s, height=1.5 * s, **kw).move_to(q(0, 0))
    head = Ellipse(width=0.9 * s, height=0.8 * s, **kw).move_to(q(1.65, 0.85))
    bill = Polygon(q(2.05, 0.95), q(2.95, 0.85), q(3.0, 0.7), q(2.85, 0.68), q(2.05, 0.72), color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    eye = Dot(q(1.85, 0.95), radius=0.07 * s, color=TEXT)
    wing = ArcBetweenPoints(q(-1.2, 0.1), q(0.6, 0.15), angle=-1.0, color=GREYL, stroke_width=4)
    g = VGroup(tail, neck, body, head, bill, eye, wing).set_z_index(3)
    g.tip = q(2.95, 0.78)
    return g


def bob(m, amp=0.05, period=2.6):
    m.bt, m.bl = 0.0, 0.0

    def u(mm, dt):
        mm.bt += dt
        new = amp * math.sin(mm.bt * TAU / period)
        mm.shift(UP * (new - mm.bl))
        mm.bl = new
    m.add_updater(u)


def pulse(m, amp=0.12, period=1.2):
    m.pt, m.pl = 0.0, 1.0

    def u(mm, dt):
        mm.pt += dt
        f = 1 + amp * math.sin(mm.pt * TAU / period)
        mm.scale(f / mm.pl)
        mm.pl = f
    m.add_updater(u)


def panel_frame():
    return Rectangle(width=TANK_R - TANK_L, height=TANK_T - TANK_B, color=OUTL, stroke_width=4, fill_color="#232c42", fill_opacity=1).move_to(
        P((TANK_L + TANK_R) / 2, (TANK_T + TANK_B) / 2))


def body_dots(n=12, seed=5, z=4):
    return jitter(n, -4.9, -1.95, -1.55, -0.3, ORANGE, seed, 0.3, r=0.07, z=z)


def label_tl(txt, color=TEXT):
    t = T(txt, 34, color, weight=BOLD)
    return t.move_to(P(TANK_L + 0.05 + t.width / 2, 3.4))


def line_path(pts, color=OUTL, width=16, op=0.35):
    return Tube().set_points_as_corners(pts).set_stroke(color, width, opacity=op).set_fill(opacity=0).set_z_index(3)


def pipe(pts, colors, thick=True, period=3.0, r=0.07):
    ref = RefPoly().set_points_as_corners(pts).lock()
    tube = line_path(pts, OUTL, 16 if thick else 5, 0.35 if thick else 0.8)
    return VGroup(tube, flow(ref, colors, period=period, r=r))


def drip(a, b, colors, period=1.3, r=0.06):
    ref = RefLine(P(*a[:2]), P(*b[:2])).lock()
    return flow(ref, colors, period=period, r=r)


# ------------------------------------------------------------------ vials and the sodium gauge
class Vial:
    def __init__(self, x, y, w=0.9, h=1.5, n=0, seed=1):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.frame = VMobject().set_points_as_corners([P(x - w / 2, y + h / 2), P(x - w / 2, y - h / 2),
                                                       P(x + w / 2, y - h / 2), P(x + w / 2, y + h / 2)])
        self.frame.set_stroke(OUTL, 5).set_fill(opacity=0).set_z_index(5)
        self.liquid = Rectangle(width=w - 0.1, height=h * 0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.28)
        self.liquid.move_to(P(x, y - h / 2 + 0.05 + h * 0.35)).set_z_index(4)
        self.dots = jitter(n, x - w / 2 + 0.08, x + w / 2 - 0.08, y - h / 2 + 0.08, y - h / 2 + h * 0.7, ORANGE, seed, 0.25, r=0.05, z=5) if n else VGroup()

    def rim(self):
        return self.y + self.h / 2


class Gauge:
    """Two sodium columns (cloacal, beak) with one seawater tick; fills tied to their trackers."""
    CX, BX, X0, H, SW = 3.6, 4.7, -2.7, 5.6, 0.5

    def __init__(self, cl=0.0, bk=0.0):
        self.tc, self.tb = ValueTracker(cl), ValueTracker(bk)
        mk = lambda x: Rectangle(width=0.6, height=self.H, color=OUTL, stroke_width=4).move_to(P(x, self.X0 + self.H / 2))
        self.fc, self.fb = mk(self.CX), mk(self.BX)
        self.rc = Rectangle(width=0.5, height=0.01, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)
        self.rb = Rectangle(width=0.5, height=0.01, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)
        self.lc = T("cloacal", 26, ORANGE)
        self.lb = T("beak", 26, ORANGE)
        for m in (self.lc, self.lb):
            m.set_opacity(0)
        ty = self.y_of(self.SW)
        self.tick = Line(P(3.2, ty), P(5.2, ty), color=BLUE, stroke_width=7).set_z_index(6)
        self.tlab = T("seawater\nsodium", 24, BLUE).move_to(P(2.3, ty))
        self.top = T("sodium, schematic", 24, TEXT).move_to(P(5.1, 3.3))
        self.drv = VMobject()
        self.drv.add_updater(lambda m: self.place())
        self.frames = VGroup(self.fc, self.fb, self.top)
        self.tickg = VGroup(self.tick, self.tlab)
        self.place()

    def y_of(self, v):
        return self.X0 + self.H * v

    def place(self):
        for r, t, x, lab in ((self.rc, self.tc, self.CX, self.lc), (self.rb, self.tb, self.BX, self.lb)):
            h = max(self.H * t.get_value(), 0.01)
            r.stretch_to_fit_height(h)
            r.move_to(P(x, self.X0 + h / 2))
            lab.move_to(P(x - 0.42 - lab.width / 2 if x == self.CX else x + 0.42 + lab.width / 2, self.X0 + h))

    def add_to(self, sc):
        sc.add(self.frames, self.tickg, self.rc, self.rb, self.lc, self.lb, self.drv)


class Lab:
    """Bird, vials and gauge of the beak-and-cloaca experiment, in fixed places."""
    def __init__(self, cl=0.0, bk=0.0, beak_n=0, cloa_n=0):
        self.frame = panel_frame()
        self.bird = bird()
        self.bd = body_dots()
        self.vb = Vial(-0.2, -0.2, n=beak_n, seed=7)
        self.vc = Vial(-4.8, -2.35, n=cloa_n, seed=9)
        self.lab_b = T("beak drip", 28, TEXT).move_to(P(1.45, -1.3))
        self.lab_c = T("cloacal fluid\n(urine + feces)", 26, TEXT).move_to(P(-2.55, -2.55))
        self.g = Gauge(cl, bk)
        self.d_b = drip(self.bird.tip + P(0, -0.05), (0.06, self.vb.rim() - 0.05), [BLUE] * 3)
        self.d_c = drip(self.bird.vent, (-4.8, self.vc.rim() - 0.05), [TMAO_C] * 3, period=1.6)

    def base(self):
        return [self.frame, self.bird, self.bd]


# ------------------------------------------------------------------ the shared chart (water cost per salt)
CH0 = (-5.4, -1.7)
CX_, CY_ = 12.0, 0.5278


def chart(text=True):
    X = lambda c: CH0[0] + c * CX_
    Y = lambda v: CH0[1] + v * CY_
    axes = VGroup(Line(P(*CH0), P(5.5, CH0[1]), color=OUTL, stroke_width=5), Line(P(*CH0), P(CH0[0], 2.1), color=OUTL, stroke_width=5))
    cs = np.linspace(0.14, 0.9, 90)
    curve = VMobject().set_points_as_corners([P(X(c), Y(1 / c)) for c in cs]).set_stroke(BLUE, 8)
    ticks = []
    for name, c, col in (("cloacal fluid", 0.15, ORANGE), ("seawater sodium", 0.47, BLUE), ("beak fluid", 0.55, ORANGE)):
        guide = DashedLine(P(X(c), CH0[1]), P(X(c), Y(1 / c)), color=col, stroke_width=4, dash_length=0.12)
        dot = Dot(P(X(c), Y(1 / c)), radius=0.14, color=col).set_z_index(5)
        ticks.append((name, c, guide, dot, col))
    g = VGroup(axes, curve, *[t[2] for t in ticks], *[t[3] for t in ticks])
    g.axes, g.curve, g.ticks, g.X, g.Y = axes, curve, ticks, X, Y
    g.labels = VGroup()
    if text:
        rows = {"cloacal fluid": -2.2, "seawater sodium": -2.2, "beak fluid": -2.8}
        for name, c, guide, dot, col in ticks:
            t = T(name, 26, col).move_to(P(X(c), rows[name]))
            g.labels.add(t)
        g.xt = T("secretion concentration", 28, TEXT).move_to(P(0.1, -3.45))
        g.yt = T("water cost per\nunit of salt", 26, TEXT).rotate(PI / 2).move_to(P(-6.1, 0.2))
        g.title = T("water cost per mole of NaCl falls\nas secretion concentration rises", 26, TEXT).move_to(P(2.4, 1.35))
    return g


def card(txt, color, w, h, c, size=28):
    box = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.10)
    box.move_to(c)
    t = T(txt, size, TEXT).move_to(c)
    return VGroup(box, t)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Osmoregulation"
    TITLE = "Where Does a Seabird's Salt Go?"


class S01Hook(SpokenScene):
    def construct(self):
        sea = Rectangle(width=7.95, height=4.1, color=OUTL, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to(P(-2.775, -1.55))
        surf = Line(P(-6.75, 0.5), P(1.2, 0.5), color=BLUE, stroke_width=5).set_z_index(2)
        dots = jitter(26, -6.6, 1.05, -3.45, 0.35, ORANGE, 12, 0.45, z=1)
        b = bird(1.0, (-3.0, 0.15))
        fish = VGroup(Ellipse(width=0.9, height=0.45, color=TMAO_C, stroke_width=3, fill_color=TMAO_C, fill_opacity=0.9),
                      Polygon(P(-0.45, 0), P(-0.8, 0.22), P(-0.8, -0.22), color=TMAO_C, stroke_width=3, fill_color=TMAO_C, fill_opacity=0.9))
        fish.move_to(b.tip + P(0.1, -0.35)).set_z_index(4)
        self.play(FadeIn(sea), FadeIn(surf), FadeIn(b), run_time=1.0)
        self.at("salt water")
        self.play(FadeIn(dots), run_time=0.6)
        self.at("all around")
        self.play(b.animate.rotate(-1.0).shift(DOWN * 1.5), run_time=0.8)
        self.play(b.animate.rotate(1.0).shift(UP * 1.5), FadeIn(fish), run_time=0.8)
        kid = VGroup(Ellipse(width=1.5, height=2.3, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1),
                     Circle(radius=0.4, stroke_width=0, fill_color=BG, fill_opacity=1).shift(LEFT * 0.62)).move_to(P(2.9, 1.7))
        kl = T("kidney", 28, TEXT).move_to(P(2.9, 0.25))
        gbar = Rectangle(width=0.6, height=3.4, color=OUTL, stroke_width=4).move_to(P(6.0, 1.7))
        gfill = Rectangle(width=0.5, height=0.01, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to(P(6.0, 0.0))
        tick = Line(P(5.55, 2.6), P(6.45, 2.6), color=BLUE, stroke_width=7)
        tlab = T("seawater", 26, BLUE).move_to(P(4.45, 2.6))
        ulab = T("urine", 28, ORANGE).move_to(P(6.0, -0.4))
        self.at("Its kidneys cannot")
        self.play(FadeIn(kid), FadeIn(kl), FadeIn(gbar), FadeIn(ulab), run_time=0.6)
        self.add(gfill)
        self.play(gfill.animate.stretch_to_fit_height(1.7).move_to(P(6.0, 0.85)), run_time=1.0)
        self.at("as salty as the sea")
        self.play(FadeIn(tick), FadeIn(tlab), run_time=0.8)
        q = T("?", 96, YELLOW, weight=BOLD).move_to(P(-2.0, 2.9))
        self.at("so where does")
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.7)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.2)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        w = World(fish="bony", water="sea", label="SEA FISH", bar_on=False, body_n=6, tank_n=24)
        L = w.ledger
        L.set(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap="")
        parts = w.parts_list()
        self.play(*[FadeIn(m) for m in parts], run_time=1.4)
        self.at("water and salt")
        self.play(*L.anim(wi=0.9, wo=0.9, si=0.85, so=0.85, ws="ok", ss="ok", cap="balanced", capc=GREEN), run_time=2.0)
        self.at("of gains and losses")
        self.play(Indicate(L.bars["wi"], color=WHITE), Indicate(L.bars["si"], color=WHITE), run_time=1.0)
        self.play(Indicate(L.bars["wo"], color=WHITE), Indicate(L.bars["so"], color=WHITE), run_time=1.0)
        gl = w.gill_label()
        self.at("A sea fish pumps")
        pump = solid_pair("bony", BOT_S, -1, "out", tag=True)
        self.play(FadeIn(gl), Create(pump), run_time=1.5)
        self.at("across its gills")
        self.play(Indicate(gl, color=YELLOW, scale_factor=1.08), run_time=1.3)
        b = bird()
        lab = label_tl("CORMORANT")
        self.at("A bird has")
        self.play(FadeOut(w.fish), FadeOut(gl), FadeOut(pump), FadeOut(w.tank_dots), FadeOut(w.body_dots), FadeOut(w.label),
                  w.fill.animate.set_fill(BLUE, 0.0), FadeIn(b), FadeIn(lab),
                  *L.anim(so=0, ss="bad", cap="unbalanced", capc=RED), run_time=1.5)
        self.finish()


def bird_world(sc, state, dots=True):
    frame = panel_frame()
    b = bird()
    lab = label_tl("CORMORANT")
    L = Ledger(True)
    L.set(**state)
    items = [frame, b, lab, L.parts]
    if dots:
        bd = body_dots()
        items.append(bd)
    sc.add(*items)
    return frame, b, L


class S03Problem(SpokenScene):
    def construct(self):
        frame, b, L = bird_world(self, dict(wi=0.9, wo=0.9, si=0.85, so=0, ws="ok", ss="bad", cap="unbalanced", capc=RED), dots=False)
        bd = body_dots(8)
        self.add(bd)
        in_l = T("In (water): seawater,\nif it drank some", 28, BLUE).move_to(P(3.7, 2.55))
        out_l = T("Out (water): urine needed\nto carry its salt", 28, BLUE).move_to(P(3.7, 0.95))
        self.at("seawater's salt")
        self.play(*L.anim(wi=0.5, si=0.5, so=0, ws="ok", ss="none", cap=""), FadeIn(in_l), run_time=1.0)
        a = P(*b.vent[:2])
        urine = VGroup(Line(a, P(a[0], -3.35), color=BLUE, stroke_width=26, stroke_opacity=0.5).set_z_index(4),
                       flow(RefLine(a, P(a[0], -3.35)).lock(), [WHITE, BLUE, ORANGE, WHITE], period=1.6, r=0.07))
        ulab = T("urine", 28, BLUE).move_to(P(-3.95, -3.0))
        self.at("through its kidneys")
        self.play(FadeIn(urine), FadeIn(ulab), *L.anim(so=0.5, ss="ok"), run_time=1.2)
        self.at("would cost")
        self.play(FadeIn(out_l), *L.anim(wo=0.95), run_time=1.8)
        self.at("than it drank")
        self.play(*L.anim(ws="bad"), Indicate(L.bars["wo"], color=WHITE, scale_factor=1.12), run_time=1.0)
        self.at("The ledger cannot")
        self.play(*L.anim(cap="cannot balance", capc=RED), Indicate(L.bars["wi"], color=WHITE), Indicate(L.bars["wo"], color=WHITE), run_time=1.6)
        hx, hy = Q(1.75, 1.95)[:2]
        ring = DashedVMobject(Circle(radius=0.55, color=YELLOW, stroke_width=6), num_dashes=16).move_to(P(hx - 0.1, hy + 0.05))
        q = T("?", 64, YELLOW, weight=BOLD).move_to(P(hx - 0.1, hy + 0.05 + 1.05))
        self.at("Is there another")
        self.play(FadeIn(ring), FadeIn(q, shift=DOWN * 0.15), run_time=1.0)
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.finish()


class S04Team(SpokenScene):
    def construct(self):
        bench = VGroup(Rectangle(width=11.0, height=0.28, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1).move_to(P(0, -2.25)),
                       Line(P(-5.0, -2.4), P(-5.0, -3.7), color=OUTL, stroke_width=6), Line(P(5.0, -2.4), P(5.0, -3.7), color=OUTL, stroke_width=6))
        holder = RoundedRectangle(corner_radius=0.2, width=3.8, height=0.7, stroke_color=GREYL, stroke_width=4, fill_color=GREYL, fill_opacity=0.35).move_to(P(-1.0, -1.82))
        b = bird(1.15, (-1.0, -0.2))
        straps = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.2, height=1.05, stroke_color=GREYL, stroke_width=3, fill_color=GREYL, fill_opacity=0.6).move_to(P(x, -0.8)).set_z_index(5)
                          for x in (-1.9, -0.1)])
        rig = VGroup(b, straps)
        bob(rig)
        n1 = T("Schmidt-Nielsen,", 30, TEXT)
        n2 = T("Jørgensen", 30, TEXT)
        n3 = T("and Osaki, 1958", 30, TEXT)
        names = VGroup(n1, n2, n3).arrange(RIGHT, buff=0.25).move_to(P(0, 3.3))
        self.play(FadeIn(bench), FadeIn(holder), FadeIn(rig), run_time=1.5)
        self.play(FadeIn(n1, shift=DOWN * 0.1), run_time=0.7)
        self.at("Jorgensen")
        self.play(FadeIn(n2, shift=DOWN * 0.1), run_time=0.7)
        self.at("Asaki")
        self.play(FadeIn(n3, shift=DOWN * 0.1), run_time=0.7)
        dl = T("double-crested\ncormorant", 30, ORANGE).move_to(P(4.0, -0.6))
        self.at("They worked with")
        self.play(Circumscribe(b, color=YELLOW, buff=0.15), run_time=0.8)
        self.at("double")
        self.play(FadeIn(dl, shift=LEFT * 0.2), run_time=0.9)
        self.finish()


class S05Load(SpokenScene):
    def construct(self):
        frame, b = panel_frame(), bird()
        lab = label_tl("CORMORANT")
        flask = VGroup(Polygon(P(2.35, 1.65), P(3.05, 1.65), P(3.05, 1.1), P(3.7, 0.0), P(3.7, -0.5), P(1.7, -0.5), P(1.7, 0.0), P(2.35, 1.1),
                               color=OUTL, stroke_width=5, fill_color=FILL, fill_opacity=1),
                       Polygon(P(1.75, -0.45), P(3.65, -0.45), P(3.65, -0.02), P(1.75, -0.02), stroke_width=0, fill_color=ORANGE, fill_opacity=0.22))
        fdots = jitter(10, 1.85, 3.55, -0.4, -0.1, ORANGE, 3, 0.3, r=0.07, z=4)
        tubeA = pipe([P(1.8, 0.05), P(0.9, 0.5), P(0.15, 1.12)], [ORANGE] * 4, thick=True, period=2.2, r=0.09)
        tubeB = pipe([P(2.2, -0.45), P(0.4, -1.15), P(-1.42, -0.9)], [ORANGE] * 4, thick=False, period=2.4, r=0.07)
        la = T("by mouth", 30, TEXT).move_to(P(1.0, 1.85))
        lb = T("or by infusion", 30, TEXT).move_to(P(0.5, -2.35))
        bd = body_dots(16, 6)
        self.add(frame, b, lab)
        self.play(FadeIn(flask), FadeIn(fdots), run_time=1.0)
        self.at("by mouth")
        self.play(FadeIn(tubeA), FadeIn(la), FadeIn(bd), run_time=0.5)
        self.at("or by infusion")
        self.play(FadeIn(tubeB), FadeIn(lb), run_time=0.8)
        r1 = DashedVMobject(Circle(radius=0.45, color=YELLOW, stroke_width=6), num_dashes=14).move_to(b.tip + P(0.05, -0.05))
        r2 = DashedVMobject(Circle(radius=0.45, color=YELLOW, stroke_width=6), num_dashes=14).move_to(b.vent + P(0, -0.1))
        self.at("Then they collected")
        self.play(FadeOut(tubeA), FadeOut(tubeB), FadeOut(la), FadeOut(lb), FadeOut(flask), FadeOut(fdots), run_time=0.6)
        self.at("two separate fluids")
        self.play(FadeIn(r1), run_time=0.6)
        self.play(FadeIn(r2), run_time=0.6)
        self.at("compared them")
        self.play(Indicate(r1, color=YELLOW, scale_factor=1.2), Indicate(r2, color=YELLOW, scale_factor=1.2), run_time=1.4)
        self.finish()


class S06Vials(SpokenScene):
    def construct(self):
        lab = Lab()
        self.add(*lab.base(), label_tl("CORMORANT"))
        self.at("One vial")
        self.play(FadeIn(lab.vc.frame), FadeIn(lab.vc.liquid), run_time=1.0)
        self.add(lab.d_c)
        self.at("which is urine")
        self.play(FadeIn(lab.lab_c), run_time=1.0)
        self.at("The other")
        self.play(FadeIn(lab.vb.frame), FadeIn(lab.vb.liquid), run_time=0.9)
        self.at("clear fluid")
        self.add(lab.d_b)
        self.play(FadeIn(lab.lab_b), run_time=0.9)
        self.add(lab.g.rc, lab.g.rb, lab.g.lc, lab.g.lb, lab.g.drv)
        self.at("dripped from")
        self.play(FadeIn(lab.g.frames), run_time=0.5)
        self.at("the tip of")
        self.play(FadeIn(lab.g.tickg), run_time=0.8)
        self.finish()


def lab_state(sc, cl=0.0, bk=0.0, vials=True):
    lab = Lab(cl, bk)
    sc.add(*lab.base(), label_tl("CORMORANT"))
    sc.add(lab.vc.frame, lab.vc.liquid, lab.vb.frame, lab.vb.liquid, lab.lab_c, lab.lab_b, lab.d_c, lab.d_b)
    lab.g.add_to(sc)
    return lab


class S07Predict(SpokenScene):
    def construct(self):
        lab = lab_state(self)
        qb = T("?", 60, YELLOW, weight=BOLD).move_to(P(1.1, 0.0))
        qc = T("?", 60, YELLOW, weight=BOLD).move_to(P(-6.0, -2.4))
        card = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.8, color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(-0.3, 3.3))
        qt = T("which vial is saltier?", 32, YELLOW).move_to(card)
        self.at("Before the results")
        self.play(Indicate(lab.vb.frame, color=YELLOW, scale_factor=1.12), Indicate(lab.vc.frame, color=YELLOW, scale_factor=1.12), run_time=1.4)
        self.at("make a guess")
        self.play(FadeIn(qb, scale=0.6), FadeIn(qc, scale=0.6), run_time=0.8)
        self.at("Which vial")
        self.play(FadeIn(card), FadeIn(qt), run_time=0.9)
        self.play(Indicate(qb, color=YELLOW, scale_factor=1.3), Indicate(qc, color=YELLOW, scale_factor=1.3), run_time=1.4)
        self.finish()


class S08Pause(SpokenScene):
    def construct(self):
        lab = lab_state(self)
        qb = T("?", 60, YELLOW, weight=BOLD).move_to(P(1.1, 0.0))
        qc = T("?", 60, YELLOW, weight=BOLD).move_to(P(-6.0, -2.4))
        card = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.8, color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(-0.3, 3.3))
        qt = T("which vial is saltier?", 32, YELLOW).move_to(card)
        pulse(qb, 0.3, 1.4)
        pulse(qc, 0.3, 1.4)
        self.add(qb, qc, card, qt)
        ring_c = P(6.3, -3.3)
        base = Circle(radius=0.3, color=OUTL, stroke_width=4).move_to(ring_c)
        prog = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.3, start_angle=PI / 2, angle=max(prog.get_value(), 0.001) * TAU, arc_center=ring_c,
                                       color=YELLOW, stroke_width=7))
        self.add(base, arc)
        self.play(prog.animate.set_value(0.0), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        lab = lab_state(self)
        g = lab.g
        g.tickg.set_opacity(1)
        ghost = VGroup(DashedLine(P(3.2, g.y_of(0.82)), P(4.0, g.y_of(0.82)), color=YELLOW, stroke_width=5),
                       T("if the kidney\nran saltier", 24, YELLOW).move_to(P(2.1, g.y_of(0.82))))
        gx = Triangle(color=YELLOW, fill_opacity=0, stroke_width=4).scale(0.15).rotate(-PI / 2).move_to(P(3.75, g.y_of(0.82)))
        ghost.add(gx)
        dense = jitter(34, lab.vb.x - 0.37, lab.vb.x + 0.37, lab.vb.y - 0.67, lab.vb.y + 0.3, ORANGE, 7, 0.25, r=0.05, z=5)
        sparse = jitter(5, lab.vc.x - 0.37, lab.vc.x + 0.37, lab.vc.y - 0.67, lab.vc.y + 0.3, ORANGE, 9, 0.25, r=0.05, z=5)
        foot = T("concentrations only:\nnot the amount each\nroute carried", 24, TEXT).move_to(P(4.4, -3.3))
        lab.lab_b.set_z_index(6)
        ghost.shift(DOWN * 2.0)
        self.at("If the kidney route")
        self.play(FadeIn(ghost), ghost.animate.shift(UP * 2.0), run_time=2.2)
        self.at("would plot higher")
        self.play(Indicate(lab.vc.frame, color=YELLOW, scale_factor=1.12), Indicate(ghost, color=YELLOW, scale_factor=1.08), run_time=1.6)
        self.at("Instead")
        self.play(FadeOut(ghost), run_time=0.6)
        self.at("the beak vial filled")
        self.play(FadeIn(dense), g.tb.animate.set_value(0.4), g.lb.animate.set_opacity(1), run_time=2.6)
        self.at("The cloacal fluid")
        self.play(FadeIn(sparse), g.tc.animate.set_value(0.17), g.lc.animate.set_opacity(1), run_time=1.5)
        self.at("much less salty")
        self.play(FadeIn(foot, shift=UP * 0.1), run_time=1.0)
        self.finish()


class S10Level(SpokenScene):
    def construct(self):
        lab = lab_state(self, 0.17, 0.4)
        g = lab.g
        g.lb.set_opacity(1)
        g.lc.set_opacity(1)
        g.tickg.set_opacity(1)
        dense = jitter(34, lab.vb.x - 0.37, lab.vb.x + 0.37, lab.vb.y - 0.67, lab.vb.y + 0.3, ORANGE, 7, 0.25, r=0.05, z=5)
        sparse = jitter(5, lab.vc.x - 0.37, lab.vc.x + 0.37, lab.vc.y - 0.67, lab.vc.y + 0.3, ORANGE, 9, 0.25, r=0.05, z=5)
        self.add(dense, sparse)
        frac = ValueTracker(0.0)
        for i, d in enumerate(lab.bd[1:]):
            d.idx = i
            n = len(lab.bd) - 1
            d.add_updater(lambda m, n=n: m.set_opacity(0.9 if m.idx / n >= frac.get_value() else 0.0))
        path = [Q(0.4, 0.1), Q(1.0, 0.5), Q(1.6, 1.2), Q(1.8, 1.95), Q(3.05, 1.9)]
        outflow = flow(RefPoly().set_points_as_corners(path).lock(), [ORANGE] * 5, period=1.8, r=0.09, z=8)
        callout = T("about seawater\nor somewhat more", 22, ORANGE).move_to(P(1.85, 1.75))
        clock = Circle(radius=0.55, color=OUTL, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(P(1.1, 3.15))
        ang = ValueTracker(0.0)
        cc = clock.get_center()
        hand = always_redraw(lambda: Line(cc, cc + 0.45 * np.array([math.sin(ang.get_value()), math.cos(ang.get_value()), 0]),
                                          color=YELLOW, stroke_width=6))
        tl = T("~10 h", 32, YELLOW, weight=BOLD).move_to(P(2.35, 3.15))
        self.at("the beak fluid reached")
        self.play(g.tb.animate.set_value(0.5), run_time=2.4)
        self.at("or somewhat more")
        self.play(g.tb.animate.set_value(0.57), FadeIn(callout), run_time=1.6)
        self.at("and the glands")
        self.play(FadeIn(clock), FadeIn(hand), FadeIn(outflow), Indicate(lab.d_b, color=YELLOW, scale_factor=1.1), run_time=1.4)
        self.at("Steady secretion")
        self.play(ang.animate.set_value(TAU * 10 / 12), frac.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        self.at("within hours")
        self.play(FadeIn(tl, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


class S11Glands(SpokenScene):
    def construct(self):
        kw = dict(color=OUTL, stroke_width=5, fill_color=FILL, fill_opacity=1)
        skull = Ellipse(width=5.4, height=4.0, **kw).move_to(P(-2.6, 0.2))
        upper = Polygon(P(-0.5, 1.25), P(5.5, 0.55), P(5.7, 0.15), P(5.4, 0.08), P(-0.5, 0.0), **kw)
        lower = Polygon(P(-0.4, -0.12), P(4.6, -0.12), P(4.9, -0.55), P(-0.4, -0.95), **kw)
        eye = Dot(P(-1.0, 1.0), radius=0.12, color=TEXT)
        head = VGroup(lower, skull, upper, eye)
        cavity = Ellipse(width=1.6, height=0.55, color=GREYL, stroke_width=4, fill_opacity=0).move_to(P(0.75, 0.62)).set_z_index(5)
        lobe1 = Ellipse(width=1.7, height=0.95, color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.35).move_to(P(-3.0, 1.35)).rotate(0.2)
        lobe2 = Ellipse(width=1.7, height=0.95, color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.35).move_to(P(-2.0, 0.85)).rotate(0.2)
        glands = VGroup(lobe1, lobe2).set_z_index(4)
        gl = T("nasal salt glands\n(schematic)", 30, ORANGE).move_to(P(-4.6, 3.1))
        duct_pts = [P(-1.6, 1.05), P(-0.4, 0.85), P(0.4, 0.65), P(1.25, 0.5), P(1.5, 0.12)]
        duct = pipe(duct_pts, [ORANGE] * 5, thick=False, period=1.8, r=0.08)
        duct[0].set_stroke(ORANGE, 6, opacity=0.8).set_z_index(5)
        nostril = Ellipse(width=0.55, height=0.18, color=YELLOW, stroke_width=5, fill_opacity=0).move_to(P(1.55, 0.04)).set_z_index(6)
        nl = T("internal nostrils\n(inside the mouth)", 26, YELLOW).move_to(P(2.9, -1.75))
        nline = Line(P(2.4, -1.35), P(1.65, -0.08), color=YELLOW, stroke_width=3)
        mouth = pipe([P(1.5, 0.05), P(3.0, 0.03), P(5.3, 0.04)], [ORANGE] * 4, thick=False, period=2.0, r=0.08)
        mouth[0].set_stroke(ORANGE, 5, opacity=0.8).set_z_index(5)
        dropf = drip((5.45, 0.0), (5.45, -1.8), [ORANGE, BLUE, ORANGE], period=1.2, r=0.08)
        self.play(FadeIn(head), run_time=0.9)
        self.at("paired glands")
        self.play(FadeIn(glands), run_time=1.2)
        self.at("the nasal salt")
        self.play(FadeIn(gl), run_time=0.8)
        self.at("It ran out")
        self.play(FadeIn(cavity), Create(duct), run_time=1.5)
        self.at("internal nostrils")
        self.play(FadeIn(nostril), FadeIn(nl), FadeIn(nline), run_time=1.0)
        self.add(mouth)
        self.at("and dripped")
        self.play(FadeIn(dropf), run_time=0.8)
        self.play(Indicate(dropf, color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.finish()


class S12Ledger(SpokenScene):
    def construct(self):
        frame, b = panel_frame(), bird()
        lab = label_tl("CORMORANT")
        L = Ledger(True)
        L.set(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap="")
        bd = body_dots(8)
        self.play(FadeIn(frame), FadeIn(b), FadeIn(lab), FadeIn(bd), FadeIn(L.parts), run_time=1.2)
        self.play(Indicate(L.rowlab, color=WHITE, scale_factor=1.1), run_time=1.0)
        c = chart(True)
        foot = T("whole-bird balance also needs the volume and makeup\nof every input and output (not measured here)", 24, TEXT).move_to(P(0, 3.3))
        self.at("Getting rid of salt")
        self.play(FadeOut(frame), FadeOut(b), FadeOut(lab), FadeOut(bd), FadeOut(L.parts), Create(c.axes), run_time=0.9)
        self.at("costs water")
        self.play(FadeIn(c.yt), run_time=0.9)
        self.at("The saltier")
        self.play(FadeIn(c.xt), run_time=0.8)
        self.play(*[Create(t[2]) for t in c.ticks], *[FadeIn(t[3]) for t in c.ticks], *[FadeIn(lb) for lb in c.labels], run_time=1.2)
        self.at("the less water")
        self.play(Create(c.curve), FadeIn(c.title), run_time=1.0)
        self.at("each bit of salt")
        self.play(FadeIn(foot), run_time=1.0)
        self.finish()


class S13Gull(SpokenScene):
    def construct(self):
        frame = panel_frame()
        b = bird()
        g = gull(1.15, (-3.4, -0.7))
        lab = label_tl("CORMORANT")
        gl = label_tl("GULL")
        gau = Gauge(0.17, 0.57)
        gau.lc.set_opacity(0)
        gtri = Triangle(color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.17).rotate(-PI / 2)
        gt = ValueTracker(0.68)
        gtri.rotate(PI)
        gtri.add_updater(lambda m: m.move_to(P(5.35, gau.y_of(gt.get_value()))))
        gull_lab = T("gull", 26, YELLOW)
        gull_lab.add_updater(lambda m: m.move_to(P(6.3, gau.y_of(gt.get_value()))))
        bd = body_dots(10)
        gd = jitter(10, -4.9, -1.9, -1.3, -0.1, ORANGE, 6, 0.3, r=0.07, z=4)
        d_g = drip(g.tip + P(0, -0.05), (g.tip[0], -2.0), [ORANGE, BLUE, ORANGE], period=1.2, r=0.07)
        cap = T("Schmidt-Nielsen, described 1960", 26, TEXT).move_to(P(-3.3, -3.35))
        self.add(frame, b, lab, bd)
        gau.add_to(self)
        gau.lb.set_opacity(1)
        gau.lc.set_opacity(0)
        gau.tickg.set_opacity(1)
        self.at("Gulls reach")
        self.play(FadeOut(b), FadeOut(lab), FadeOut(bd), FadeIn(g), FadeIn(gl), FadeIn(gd), run_time=0.6)
        self.add(d_g, gtri, gull_lab)
        self.at("higher salt levels")
        self.play(gt.animate.set_value(0.88), run_time=1.6)
        # second experiment: salt removed by each route
        base = Line(P(1.0, -2.6), P(6.4, -2.6), color=OUTL, stroke_width=5)
        t_top = T("salt removed", 30, TEXT).move_to(P(3.7, 3.35))
        rg = Rectangle(width=1.3, height=0.01, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to(P(2.2, -2.6))
        rc = Rectangle(width=1.3, height=0.01, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to(P(4.6, -2.6))
        lg_ = T("salt gland", 28, ORANGE).move_to(P(2.2, -3.1))
        lc_ = T("cloaca", 28, ORANGE).move_to(P(4.6, -3.1))
        self.at("In a later experiment")
        self.play(FadeOut(gau.frames), FadeOut(gau.tickg), FadeOut(gau.rc), FadeOut(gau.rb), FadeOut(gau.lc), FadeOut(gau.lb),
                  FadeOut(gtri), FadeOut(gull_lab), FadeIn(base), FadeIn(t_top), FadeIn(cap), run_time=1.2)
        self.add(rg, rc)
        self.play(FadeIn(lg_), FadeIn(lc_), run_time=0.6)
        self.at("the salt gland removed")
        self.play(rg.animate.stretch_to_fit_height(4.6).move_to(P(2.2, -2.6 + 2.3)), run_time=2.0)
        self.at("as much salt as")
        self.play(rc.animate.stretch_to_fit_height(0.46).move_to(P(4.6, -2.6 + 0.23)), run_time=0.9)
        arrow = DoubleArrow(P(5.3, -2.1), P(5.3, 2.0), buff=0, color=YELLOW, stroke_width=6, tip_length=0.22)
        x10 = T("~10x", 40, YELLOW, weight=BOLD).move_to(P(6.15, 0.0))
        self.at("the cloaca")
        self.play(FadeIn(arrow), FadeIn(x10, scale=0.8), run_time=1.0)
        self.finish()


class S14Limits(SpokenScene):
    def construct(self):
        ca = card("shown: an extrarenal route\nthat clears a salt load", GREEN, 12.4, 2.0, P(0, 2.4), 30)
        ca[1].move_to(P(-1.6, 2.4))
        chk = VMobject().set_points_as_corners([P(-6.0, 2.4), P(-5.5, 1.9), P(-4.6, 2.9)]).set_stroke(GREEN, 12)
        kid = VGroup(Ellipse(width=0.7, height=1.0, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1),
                     Circle(radius=0.22, stroke_width=0, fill_color=BG, fill_opacity=1).shift(LEFT * 0.34)).move_to(P(4.9, 2.1))
        arc_pts = [P(3.5, 2.2), P(4.0, 3.0), P(5.7, 3.0), P(6.1, 2.2)]
        byp = VMobject().set_points_as_corners(arc_pts).set_stroke(ORANGE, 5)
        bypass = VGroup(byp, flow(RefPoly().set_points_as_corners(arc_pts).lock(), [ORANGE] * 4, period=2.0, r=0.09))
        cb = card("", GREYL, 12.4, 3.9, P(0, -1.15), 28)
        r1 = T("not shown:\nhow the gland concentrates salt", 28, TEXT)
        r2 = T("not shown:\nthat every bird has active salt glands", 28, TEXT)
        q1 = T("?", 64, YELLOW, weight=BOLD).move_to(P(-5.6, -0.2))
        q2 = T("?", 64, YELLOW, weight=BOLD).move_to(P(-5.6, -2.1))
        r1.move_to(P(-4.8 + r1.width / 2, -0.2))
        r2.move_to(P(-4.8 + r2.width / 2, -2.1))
        self.at("The experiment showed")
        self.play(FadeIn(ca), run_time=1.0)
        self.play(Create(chk), run_time=0.8)
        self.at("one that bypasses")
        self.play(FadeIn(kid), FadeIn(bypass), run_time=1.2)
        self.play(Indicate(ca[0], color=GREEN, scale_factor=1.02), run_time=1.4)
        self.at("It did not show")
        self.play(FadeIn(cb), run_time=0.8)
        self.at("how the gland")
        self.play(FadeIn(r1), FadeIn(q1, scale=0.6), run_time=1.0)
        self.play(Indicate(q1, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.at("or that every bird")
        self.play(FadeIn(r2), FadeIn(q2, scale=0.6), run_time=1.0)
        self.play(Indicate(q2, color=YELLOW, scale_factor=1.3), run_time=1.2)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        fw = mini("sea", -3.4)
        fw.ledger.set(wi=0.9, wo=0.9, si=0.85, so=0.85, ws="ok", ss="ok")
        fish_g = VGroup(fw.tank_g, fw.ledger.parts)
        cap1 = T("route out: gills", 30, TEXT).move_to(P(-3.4, -3.4))
        bmini = bird(0.62, (3.55, 1.45))
        bframe = Rectangle(width=6.2, height=3.4, color=OUTL, stroke_width=3).move_to(P(3.6, 1.45))
        c = chart(False)
        c.scale(0.55).move_to(P(3.6, -1.35))
        cpan = Rectangle(width=6.2, height=2.3, color=OUTL, stroke_width=3, fill_color=BG, fill_opacity=0.9).move_to(P(3.6, -1.35))
        cap2 = T("route out: salt glands;\nvolumes not measured", 30, TEXT).move_to(P(3.6, -3.35))
        bd = jitter(6, 2.0, 3.2, 1.1, 1.5, ORANGE, 4, 0.25, r=0.05, z=4)
        dm = drip(bmini.tip + P(0, -0.05), (bmini.tip[0], 0.2), [ORANGE, BLUE, ORANGE], period=1.2, r=0.06)
        self.play(FadeIn(fish_g), run_time=0.4)
        self.at("bookkeeping")
        self.play(FadeIn(cap1), Indicate(fw.ledger.panel, color=WHITE, scale_factor=1.03), run_time=1.2)
        self.at("The bird's second route")
        self.play(FadeIn(bframe), FadeIn(bmini), FadeIn(bd), FadeIn(dm), run_time=1.2)
        self.play(FadeIn(cpan), Create(c), FadeIn(cap2), run_time=1.6)
        self.at("how salty it runs")
        self.play(Indicate(c.curve, color=YELLOW, scale_factor=1.04), run_time=1.5)
        self.at("water cost")
        self.play(Indicate(c.curve, color=WHITE, scale_factor=1.04), run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "A more concentrated salt secretion costs less water per unit salt."
