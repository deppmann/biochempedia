"""Filter far more, take most back: one nephron, one ledger  (Biochemistrypedia explainer, remade 2026-11-11)

COLOUR MAP: blood RED; filtrate and urine YELLOW; salt (sodium) ORANGE dots; water BLUE drops;
glucose GREEN squares; drug PURPLE diamonds; protein and urea grey. Everything is a schematic cartoon.
One world: a nephron lying left to right (cup at the left, long tube, open exit at the right) with one
blood vessel running above it. Every scene that continues the picture rebuilds it in the same place.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F08A3C"
PURPLE = "#B388EB"
PROT = "#A7AEBB"

TUBE_Y, TUBE_X0, TUBE_X1, TUBE_H = -0.6, -3.7, 6.3, 0.9
CAP_Y, CAP_H = 2.15, 0.6
KNOT = np.array([-5.65, -0.6, 0.0])
ROW_Y = {"glucose": -2.5, "sodium": -2.86, "drug": -3.22, "water": -3.58}


# ---------------------------------------------------------------- moving particles
class Route:
    def __init__(self, pts):
        self.p = [np.array([x, y, 0.0]) for x, y in pts]
        d = [np.linalg.norm(self.p[i + 1] - self.p[i]) for i in range(len(self.p) - 1)]
        self.cum = np.concatenate([[0.0], np.cumsum(d)])
        self.L = float(self.cum[-1])

    def at(self, s):
        s = min(max(s, 0.0), self.L)
        i = min(int(np.searchsorted(self.cum, s, side="right") - 1), len(self.p) - 2)
        seg = self.cum[i + 1] - self.cum[i]
        t = 0.0 if seg < 1e-9 else (s - self.cum[i]) / seg
        return self.p[i] * (1 - t) + self.p[i + 1] * t


def shape(kind):
    if kind == "water":
        return Dot(radius=0.11, color=BLUE)
    if kind == "salt":
        return Dot(radius=0.11, color=ORANGE)
    if kind == "glucose":
        return Square(0.22, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    if kind == "drug":
        return Square(0.24, stroke_width=0, fill_color=PURPLE, fill_opacity=1).rotate(PI / 4)
    if kind == "urea":
        return Dot(radius=0.08, color=PROT)
    if kind == "protein":
        return Dot(radius=0.17, color=PROT)
    if kind == "cell":
        return Circle(radius=0.13, stroke_color=TEXT, stroke_width=1.5, fill_color=RED, fill_opacity=1)
    raise ValueError(kind)


def step(m, dt):
    if m.gate.get_value() < 0.5:
        m.set_opacity(0)
        m.cur = 0
        return
    if not m.started:
        m.started = True
        m.s = m.s0
    m.clk += dt
    waiting = False
    if m.s_hop is not None and not m.decided and m.s >= m.s_hop:
        on = m.trig is not None and m.trig.get_value() > 0.5
        if m.policy == "wait":
            if on:
                m.tw += dt
                if m.tw >= m.lag:
                    m.route, m.decided = m.route_hop, True
                else:
                    waiting = True
            else:
                waiting = True
        else:
            m.decided = True
            if on:
                m.route = m.route_hop
    if waiting:
        m.s = m.s_hop
        j = np.array([0.05 * np.sin(m.clk * 3 + m.ph), 0.05 * np.cos(m.clk * 2.3 + m.ph), 0])
    else:
        m.s += m.speed * dt
        j = 0
        if m.s > m.route.L + 0.05:
            m.s, m.decided, m.tw, m.route = -m.gapd, False, 0.0, m.route0
    if m.s < 0:
        m.set_opacity(0)
        m.cur = 0
        return
    m.move_to(m.route.at(m.s) + j)
    f = min(1.0, m.s / 0.25, (m.route.L - m.s) / 0.5) if m.fade else 1.0
    m.cur = m.base * max(f, 0)
    m.set_opacity(m.cur)


def fstep(m, dt):
    ld = m.leader
    if ld.gate.get_value() < 0.5 or not ld.started or ld.s < m.off or ld.cur <= 0:
        m.set_opacity(0)
        return
    m.move_to(ld.route.at(ld.s - m.off) + np.array([0.0, m.dy, 0.0]))
    m.set_opacity(ld.cur / ld.base * m.base)


def make_stream(kind, n, gate, *, hop=None, trig=None, policy="wait", speed=0.9, start="knot", spacing=0.7,
                pre=False, seed=0, lag=0.35, nohop=0, faint=0, follow=None, y_off=0.0):
    """n particles of one kind. hop=(xlo, xhi) is where they cross between tube and vessel; the last `nohop`
    never cross; the last `faint` are drawn at 40% (schematic stragglers). follow='water' adds a drop behind each hopper."""
    rng = random.Random(seed)
    lanes_t = np.linspace(-0.27, 0.27, 5)
    lanes_c = np.linspace(-0.17, 0.17, 5)
    out, fol = VGroup(), VGroup()
    for i in range(n):
        m = shape(kind)
        yt = TUBE_Y + lanes_t[(i * 2) % 5] + y_off
        yc = CAP_Y + lanes_c[(i * 3) % 5]
        hops = hop is not None and i < n - nohop
        if hops:
            hx = hop[0] + (hop[1] - hop[0]) * ((i * 0.618 + 0.1) % 1.0)
        if start == "knot":
            r_str = Route([(-5.95, yt), (-4.3, yt), (TUBE_X1 + 0.25, yt)])
            r_hop = Route([(-5.95, yt), (-4.3, yt), (hx, yt), (hx + 0.55, yc), (6.3, yc)]) if hops else r_str
            s_hop = hx + 5.95 if hops else None
        else:  # starts in the vessel and crosses into the tube
            hx = hx if hops else 0.0
            r_str = Route([(hx - 1.3, yc), (6.3, yc)])
            r_hop = Route([(hx - 1.3, yc), (hx, yc), (hx + 0.45, yt), (TUBE_X1 + 0.25, yt)])
            s_hop = 1.3
        period = max(spacing * n, r_str.L / speed + 0.4)
        m.route0 = m.route = r_str
        m.route_hop, m.s_hop, m.trig, m.policy = r_hop, s_hop, trig, policy
        m.gate, m.speed, m.fade, m.started, m.decided = gate, speed, True, False, False
        m.s0 = rng.uniform(0, r_str.L * 0.9) if pre else -(i * spacing + 0.1) * speed
        m.gapd = max(0.3, period * speed - r_str.L)
        m.lag, m.tw, m.clk, m.ph, m.cur = lag * (i % 7) + rng.uniform(0, 0.2), 0.0, 0.0, rng.uniform(0, 6), 0.0
        m.base = 0.4 if i >= n - faint else 1.0
        m.set_opacity(0)
        m.add_updater(step)
        out.add(m)
        if follow and hops:
            f = shape(follow)
            f.leader, f.off, f.dy, f.base = m, 0.42, 0.0, 1.0
            f.set_opacity(0)
            f.add_updater(fstep)
            fol.add(f)
    return VGroup(out, fol)


def bounce_stream(kind, n, gate, seed=0):
    """Cells and proteins that run at the barrier and bounce back (a closed loop inside the knot)."""
    rng = random.Random(seed)
    out = VGroup()
    for i in range(n):
        m = shape(kind)
        y = -0.6 + rng.uniform(-0.3, 0.3)
        x0 = -6.0 + rng.uniform(0, 0.4)
        r = Route([(x0, y), (-4.85, y), (x0 + 0.5, y + rng.uniform(-0.2, 0.2)), (x0, y)])
        m.route0 = m.route = r
        m.route_hop, m.s_hop, m.trig, m.policy = r, None, None, "chance"
        m.gate, m.speed, m.fade, m.started, m.decided = gate, 0.8, False, False, False
        m.s0, m.gapd, m.lag, m.tw, m.clk, m.ph, m.cur, m.base = rng.uniform(0, r.L), 0.0, 0, 0.0, 0.0, 0.0, 0.0, 1.0
        m.set_opacity(0)
        m.add_updater(step)
        out.add(m)
    return out


def blood_stream(gate, n=14):
    pts = [(-6.5, 2.9), (-6.1, 0.15)]
    for a in np.linspace(115, 425, 16):
        pts.append((KNOT[0] + 0.42 * np.cos(np.radians(a)), KNOT[1] + 0.42 * np.sin(np.radians(a))))
    pts += [(-5.3, 0.2), (-5.2, CAP_Y), (6.15, CAP_Y)]
    r = Route(pts)
    out = VGroup()
    rng = random.Random(3)
    for i in range(n):
        m = shape("cell")
        m.route0 = m.route = r
        m.route_hop, m.s_hop, m.trig, m.policy = r, None, None, "chance"
        m.gate, m.speed, m.fade, m.started, m.decided = gate, 1.5, True, False, False
        m.s0, m.gapd, m.lag, m.tw, m.clk, m.ph, m.cur, m.base = r.L * i / n, 0.2, 0, 0.0, 0.0, 0.0, 0.0, 1.0
        m.set_opacity(0)
        m.add_updater(step)
        out.add(m)
    return out


# ---------------------------------------------------------------- the world
def world_parts():
    cap = RoundedRectangle(corner_radius=0.45, width=3.0, height=3.0, stroke_color=GREY, stroke_width=4,
                           fill_color=YELLOW, fill_opacity=0.07).move_to([-5.2, -0.6, 0])
    patch = Rectangle(width=0.1, height=TUBE_H - 0.06, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([-3.7, TUBE_Y, 0])
    tw = TUBE_X1 - (TUBE_X0 - 0.2)
    tfill = Rectangle(width=tw, height=TUBE_H, stroke_width=0, fill_color=YELLOW, fill_opacity=0.15).move_to([(TUBE_X1 + TUBE_X0 - 0.2) / 2, TUBE_Y, 0])
    tl = VGroup(*[Line([TUBE_X0, TUBE_Y + s * TUBE_H / 2, 0], [TUBE_X1, TUBE_Y + s * TUBE_H / 2, 0], color=GREY, stroke_width=4) for s in (1, -1)])
    knot = VGroup(Circle(radius=0.7, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.2),
                  Arc(radius=0.4, start_angle=0.4, angle=4.6, stroke_color=RED, stroke_width=3),
                  Arc(radius=0.2, start_angle=2.0, angle=4.2, stroke_color=RED, stroke_width=3)).move_to(KNOT)
    cw = 6.2 - (-5.2)
    cfill = Rectangle(width=cw, height=CAP_H, stroke_width=0, fill_color=RED, fill_opacity=0.16).move_to([(6.2 - 5.2) / 2, CAP_Y, 0])
    cl = VGroup(*[Line([-5.2, CAP_Y + s * CAP_H / 2, 0], [6.2, CAP_Y + s * CAP_H / 2, 0], color=RED, stroke_width=3) for s in (1, -1)])
    aff = Line([-6.5, 2.9, 0], [-6.1, 0.15, 0], color=RED, stroke_width=16).set_opacity(0.45)
    eff = Line([-5.3, 0.2, 0], [-5.2, CAP_Y, 0], color=RED, stroke_width=16).set_opacity(0.45)
    return dict(cap=cap, patch=patch, tfill=tfill, tl=tl, knot=knot, cfill=cfill, cl=cl, aff=aff, eff=eff)


class Base(SpokenScene):
    def world(self, blood=True):
        w = world_parts()
        self.w = w
        for k in ("cap", "patch", "tfill", "tl", "knot", "cfill", "cl", "aff", "eff"):
            self.add(w[k])
        self.blood_gate = ValueTracker(1 if blood else 0)
        self.blood = blood_stream(self.blood_gate)
        self.add(self.blood)
        return w

    def seg(self, x0, x1, text, color=TEXT, y=-1.35, ty=-1.75):
        ln = VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                    Line([x0, y, 0], [x0, y + 0.15, 0], color=color, stroke_width=4),
                    Line([x1, y, 0], [x1, y + 0.15, 0], color=color, stroke_width=4))
        t = T(text, 28, color).move_to([(x0 + x1) / 2, ty, 0])
        return VGroup(ln, t)

    def ledger(self, lit=True):
        words = ["excreted", "=", "filtered", "-", "reabsorbed", "+", "secreted"]
        ts = VGroup(*[T(w, 30, TEXT if lit else GREY) for w in words]).arrange(RIGHT, buff=0.3)
        if not lit:
            ts.set_opacity(0.5)
        box = RoundedRectangle(corner_radius=0.15, width=ts.width + 0.7, height=0.78, stroke_color=GOLD, stroke_width=3)
        g = VGroup(box, ts).move_to([0, 3.35, 0])
        self.terms = [ts[0], ts[2], ts[4], ts[6]]
        self.ops = [ts[1], ts[3], ts[5]]
        self.lbar = g
        return g

    def light(self, i, color=TEXT, rt=0.35):
        t = self.terms[i]
        anims = [t.animate.set_color(color).set_opacity(1)]
        if i > 0:
            anims.append(self.ops[i - 1].animate.set_color(TEXT).set_opacity(1))
        self.play(*anims, run_time=rt)

    def rows(self, keys, final=True):
        g = VGroup()
        for k in keys:
            g.add(row(k, final))
        return g


ROWTXT = {
    "glucose": ("glucose:", GREEN, "nearly all taken back, almost none excreted"),
    "sodium": ("sodium:", ORANGE, "most taken back, a small share excreted"),
    "drug": ("some drugs:", PURPLE, "filtered + secreted, so more can leave"),
    "water": ("water:", BLUE, "about 99% taken back"),
}


def row(k, final=True, text=None):
    lab, col, res = ROWTXT[k]
    a = T(lab, 28, col).move_to([-6.4, ROW_Y[k], 0], aligned_edge=LEFT)
    g = VGroup(a)
    if final or text:
        b = T(text or res, 28, TEXT).next_to(a, RIGHT, buff=0.15)
        g.add(b)
    return g


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "The Kidney"
    TITLE = "Filter Far More, Take Most Back"


class S01Question(SpokenScene):
    def construct(self):
        base, H = -3.0, 5.4
        floor = Line([-6.2, base, 0], [6.2, base, 0], color=GREY, stroke_width=3)
        bar = Rectangle(width=3.0, height=H, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                        fill_opacity=0.28).move_to([-3.2, base + H / 2, 0])
        lab = T("180 L filtered per day", 30, YELLOW).move_to([-3.2, 3.05, 0])
        sub = T("adult human", 24, TEXT).next_to(lab, DOWN, buff=0.08)
        sub.move_to([-3.2, 2.72, 0])
        bar.move_to([-3.2, base + H / 2 - 0.2, 0]) if False else None
        sliver = Rectangle(width=3.0, height=0.06, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([3.2, base + 0.03, 0])
        ulab = T("1 to 2 L urine per day", 30, YELLOW).move_to([3.2, -1.9, 0])
        uarr = Arrow([3.2, -2.3, 0], [3.2, -2.85, 0], color=YELLOW, buff=0, stroke_width=6)
        q = T("?", 170, RED, weight=BOLD).move_to([0.1, 0.1, 0])
        self.play(Create(floor), run_time=0.5)
        self.at("kidneys filter")
        self.play(GrowFromEdge(bar, DOWN), run_time=2.5)
        self.at("liters of plasma")
        self.play(FadeIn(lab, shift=DOWN * 0.1), FadeIn(sub), run_time=0.6)
        drops = VGroup()
        rng = random.Random(5)
        for _ in range(16):
            d = Dot(radius=0.07, color=YELLOW).set_opacity(0.7)
            d.move_to([-3.2 + rng.uniform(-1.2, 1.2), base + rng.uniform(0.1, H - 0.1), 0])
            d.vy = rng.uniform(0.5, 0.9)

            def up(m, dt):
                m.shift(UP * m.vy * dt)
                if m.get_y() > base + H - 0.1:
                    m.set_y(base + 0.1)
            d.add_updater(up)
            drops.add(d)
        self.add(drops)
        self.at("you pass")
        self.play(GrowFromEdge(sliver, DOWN), run_time=0.6)
        self.at("one or two")
        self.play(FadeIn(ulab, shift=UP * 0.1), GrowArrow(uarr), run_time=0.7)
        self.at("why would")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        q.t = 0.0

        def pulse(m, dt):
            m.t += dt
            m.set_height(1.5 * (1 + 0.12 * np.sin(m.t * 4)))
        q.add_updater(pulse)
        self.finish()


class S02Nephron(Base):
    def construct(self):
        w = world_parts()
        self.w = w
        self.add(w["cap"], w["knot"])
        self.blood_gate = ValueTracker(0)
        self.blood = blood_stream(self.blood_gate)
        self.add(self.blood)
        # the cup and the tube first, then the name
        self.play(Create(w["cap"]), FadeIn(w["knot"]), run_time=1.4)
        nlab = T("nephron", 40, GOLD).move_to([1.3, 0.95, 0])
        narr = Arrow([1.3, 0.55, 0], [1.3, -0.12, 0], color=GOLD, buff=0, stroke_width=6)
        self.at("nephron")
        self.play(FadeIn(nlab, shift=DOWN * 0.1), GrowArrow(narr), run_time=0.6)
        self.at("attached")
        self.play(FadeIn(w["patch"]), FadeIn(w["tfill"], shift=RIGHT * 0.3), Create(w["tl"]), run_time=2.0)
        self.at("blood enters")
        self.play(FadeOut(nlab), FadeOut(narr), Create(w["aff"]), run_time=0.6)
        self.blood_gate.set_value(1)
        self.play(FadeIn(w["cfill"]), Create(w["cl"]), Create(w["eff"]), run_time=0.8)
        alab = T("afferent arteriole", 30, RED).move_to([-6.7, 3.35, 0], aligned_edge=LEFT)
        aarr = Arrow([-6.2, 3.1, 0], [-6.4, 2.6, 0], color=RED, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.5)
        self.at("knot of capillaries")
        self.play(Indicate(w["knot"], color=RED, scale_factor=1.12), run_time=1.0)
        glab = T("glomerulus", 30, TEXT).move_to([-5.4, -2.7, 0])
        garr = Arrow([-5.5, -2.4, 0], [-5.6, -1.4, 0], color=TEXT, buff=0, stroke_width=5)
        self.at("glomerulus")
        self.play(FadeIn(glab, shift=UP * 0.1), GrowArrow(garr), run_time=0.6)
        self.at("afferent arteriole")
        self.play(FadeIn(alab, shift=DOWN * 0.1), GrowArrow(aarr), run_time=0.6)
        elab = T("efferent arteriole", 30, RED).move_to([-4.9, 1.35, 0], aligned_edge=LEFT)
        self.at("it leaves")
        self.play(FadeIn(elab, shift=RIGHT * 0.1), Indicate(w["eff"], color=RED), run_time=0.8)
        sch = T("schematic", 22, GREY).move_to([5.8, -3.6, 0])
        self.play(FadeIn(sch), run_time=0.4)
        self.finish()


class S03Filter(Base):
    def construct(self):
        self.world()
        g = ValueTracker(0)
        mix = VGroup(make_stream("water", 8, g, speed=1.0, seed=1, spacing=0.4),
                     make_stream("salt", 6, g, speed=1.0, seed=2, spacing=0.5),
                     make_stream("glucose", 6, g, speed=1.0, seed=3, spacing=0.5),
                     make_stream("urea", 6, g, speed=1.0, seed=4, spacing=0.5))
        gb = ValueTracker(0)
        bounce = VGroup(bounce_stream("cell", 3, gb, 1), bounce_stream("protein", 2, gb, 2))
        self.add(mix, bounce)
        barrier = DashedVMobject(Circle(radius=0.98, color=TEXT, stroke_width=4), num_dashes=24).move_to(KNOT)
        self.play(Create(barrier), run_time=0.8)
        g.set_value(1)
        gb.set_value(1)
        blab = T("barrier", 30, TEXT).move_to([-5.4, -2.7, 0])
        barr = Arrow([-5.4, -2.4, 0], [-5.4, -1.62, 0], color=TEXT, buff=0, stroke_width=5)
        self.at("a barrier")
        self.play(FadeIn(blab, shift=UP * 0.1), GrowArrow(barr), run_time=0.6)
        cl = T("Bowman's capsule", 30, TEXT).move_to([-2.3, 1.3, 0])
        carr = Arrow([-3.4, 1.05, 0], [-3.85, 0.7, 0], color=TEXT, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.5)
        self.at("bowman's capsule")
        self.play(FadeIn(cl, shift=DOWN * 0.1), GrowArrow(carr), run_time=0.6)
        fl = T("filtrate", 32, YELLOW).move_to([-0.3, -1.75, 0])
        farr = Arrow([-0.3, -1.45, 0], [-0.3, -1.1, 0], color=YELLOW, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.9)
        self.at("this fluid")
        self.play(FadeOut(blab), FadeOut(barr), FadeOut(cl), FadeOut(carr), FadeIn(fl, shift=UP * 0.1), FadeIn(farr), run_time=0.6)
        chips = []
        for name, col, x in (("water", BLUE, -0.6), ("salt", ORANGE, 1.25), ("glucose", GREEN, 3.0), ("urea", PROT, 5.2)):
            c = chip(name, col, 28)
            c.move_to([x, -2.9, 0])
            chips.append(c)
        for name, c in zip(("carries water", "salt", "glucose", "urea"), chips):
            self.at(name if name != "carries water" else "carries water")
            self.play(FadeIn(c, shift=UP * 0.1), run_time=0.4)
        bl = T("blood cells", 30, RED).move_to([-5.3, -2.7, 0])
        pl = T("protein", 30, PROT).move_to([-3.0, -2.7, 0])
        self.at("no blood cells")
        self.play(FadeIn(bl, shift=UP * 0.1), Indicate(bounce[0], color=RED), run_time=0.8)
        self.at("very little protein")
        self.play(FadeIn(pl, shift=UP * 0.1), Indicate(bounce[1], color=PROT), run_time=0.8)
        self.finish()


class S04Ledger(Base):
    def construct(self):
        self.world()
        g = ValueTracker(1)
        trig = ValueTracker(0)
        gs = ValueTracker(0)
        ts = ValueTracker(0)
        back = VGroup(make_stream("water", 8, g, hop=(-3.4, -2.4), trig=trig, policy="chance", pre=True, seed=1, speed=0.9),
                      make_stream("salt", 6, g, hop=(-3.4, -2.4), trig=trig, policy="chance", pre=True, seed=2, speed=0.9),
                      make_stream("glucose", 6, g, hop=(-3.4, -2.4), trig=trig, policy="chance", pre=True, seed=3, speed=0.9))
        added = make_stream("drug", 5, gs, hop=(3.2, 4.0), trig=ts, policy="wait", start="cap", seed=4, spacing=0.5)
        self.add(back, added)
        up = Arrow([-2.95, -0.1, 0], [-2.95, 1.75, 0], color=TEXT, buff=0, stroke_width=8)
        down = Arrow([3.6, 1.75, 0], [3.6, -0.1, 0], color=TEXT, buff=0, stroke_width=8)
        rl = T("reabsorbed (taken back)", 30, TEXT).move_to([-1.9, 1.3, 0], aligned_edge=LEFT)
        sl = T("secreted (added)", 30, TEXT).move_to([3.1, 0.55, 0], aligned_edge=RIGHT)
        self.at("takes substances back")
        trig.set_value(1)
        self.play(GrowArrow(up), run_time=0.6)
        self.at("that is reabsorption")
        self.play(FadeIn(rl, shift=RIGHT * 0.1), run_time=0.6)
        self.at("adds substances")
        gs.set_value(1)
        self.play(GrowArrow(down), run_time=0.6)
        ts.set_value(1)
        self.at("that is secretion")
        self.play(FadeIn(sl, shift=LEFT * 0.1), run_time=0.6)
        self.at("keep a ledger")
        self.play(FadeOut(up), FadeOut(down), FadeOut(rl), FadeOut(sl), run_time=0.5)
        bar = self.ledger(lit=False)
        self.play(FadeIn(bar, shift=DOWN * 0.2), run_time=0.7)
        self.at("what leaves")
        self.light(0)
        self.at("what was filtered")
        self.light(1)
        self.at("minus what was taken back")
        self.light(2)
        self.at("plus what was added")
        self.light(3)
        self.finish()


class S05Glucose(Base):
    def construct(self):
        self.world()
        bar = self.ledger(True)
        self.add(bar)
        g = ValueTracker(0)
        trig = ValueTracker(0)
        glu = make_stream("glucose", 10, g, hop=(-3.2, -0.9), trig=trig, policy="wait", speed=0.9, seed=7, spacing=0.45, nohop=1, faint=1, lag=0.3)
        self.add(glu)
        r_lab = T("glucose:", 28, GREEN).move_to([-6.4, ROW_Y["glucose"], 0], aligned_edge=LEFT)
        three = [T(x, 28, c).set_opacity(0.45) for x, c in (("glucose", GREEN), ("sodium", ORANGE), ("a drug", PURPLE))]
        stubs = VGroup(*three).arrange(RIGHT, buff=0.6).move_to([-3.6, -3.0, 0])
        self.at("three substances")
        self.play(FadeIn(stubs, shift=UP * 0.1), run_time=0.8)
        self.at("first glucose")
        g.set_value(1)
        self.play(FadeOut(stubs), FadeIn(r_lab), run_time=0.6)
        sch = T("schematic", 22, GREY).move_to([5.8, -3.6, 0])
        self.at("filtered at about")
        self.play(Indicate(self.w["knot"], color=GREEN, scale_factor=1.1), run_time=0.8)
        seg = self.seg(-3.5, -0.7, "proximal tubule", TEXT)
        self.at("proximal tubule")
        self.play(FadeIn(seg, shift=UP * 0.1), run_time=0.6)
        res = T("nearly all taken back", 28, TEXT).next_to(r_lab, RIGHT, buff=0.15)
        self.at("takes almost all")
        trig.set_value(1)
        self.play(FadeIn(res), FadeIn(sch), run_time=0.6)
        res2 = T("nearly all taken back, almost none excreted", 28, TEXT).next_to(r_lab, RIGHT, buff=0.15)
        self.at("almost none")
        self.play(Transform(res, res2), run_time=0.7)
        self.finish()


class S06Sodium(Base):
    def construct(self):
        self.world()
        self.add(self.ledger(True), row("glucose"))
        g = ValueTracker(0)
        t1 = ValueTracker(0)
        t2 = ValueTracker(0)
        s1 = make_stream("salt", 9, g, hop=(-3.2, -2.3), trig=t1, policy="wait", speed=0.9, seed=11, spacing=0.4, follow="water", lag=0.45)
        s2 = make_stream("salt", 3, g, hop=(0.4, 2.6), trig=t2, policy="wait", speed=0.9, seed=12, spacing=0.4, nohop=1, lag=0.5)
        self.add(s1, s2)
        r_lab = T("sodium:", 28, ORANGE).move_to([-6.4, ROW_Y["sodium"], 0], aligned_edge=LEFT)
        self.at("next sodium")
        g.set_value(1)
        self.play(FadeIn(r_lab, shift=UP * 0.1), run_time=0.6)
        self.at("takes back about")
        t1.set_value(1)
        seg = self.seg(-3.5, -0.7, "60 to 70% of sodium", ORANGE)
        seg[1].move_to([-1.4, -1.75, 0])
        self.play(FadeIn(seg, shift=UP * 0.1), run_time=0.7)
        self.at("and water follows")
        self.play(Indicate(s1[1], color=BLUE, scale_factor=1.6), run_time=1.2)
        self.at("later stretches")
        t2.set_value(1)
        seg2 = self.seg(0.4, 4.0, "later stretches", ORANGE)
        seg2[1].move_to([2.6, -1.75, 0])
        self.play(FadeIn(seg2, shift=UP * 0.1), run_time=0.7)
        res = T("most taken back, a small share excreted", 28, TEXT).next_to(r_lab, RIGHT, buff=0.15)
        self.at("only a small share")
        self.play(FadeIn(res), run_time=0.7)
        self.finish()


class S07Drug(Base):
    def construct(self):
        self.world()
        self.add(self.ledger(True), row("glucose"), row("sodium"))
        g = ValueTracker(0)
        gs = ValueTracker(0)
        ts = ValueTracker(0)
        filt = make_stream("drug", 4, g, speed=0.9, seed=21, spacing=1.6)
        extra = make_stream("drug", 6, gs, hop=(-3.0, -0.4), trig=ts, policy="wait", start="cap", seed=22, spacing=0.6, speed=0.9, lag=0.5)
        self.add(filt, extra)
        r_lab = T("some drugs:", 28, PURPLE).move_to([-6.4, ROW_Y["drug"], 0], aligned_edge=LEFT)
        self.at("some drugs")
        self.play(FadeIn(r_lab, shift=UP * 0.1), run_time=0.6)
        self.at("they are filtered")
        g.set_value(1)
        self.play(Indicate(self.w["knot"], color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.at("and the proximal tubule")
        gs.set_value(1)
        seg = self.seg(-3.5, -0.7, "proximal tubule", TEXT)
        self.play(FadeIn(seg, shift=UP * 0.1), run_time=0.6)
        sarr = Arrow([-1.7, 1.75, 0], [-1.7, -0.1, 0], color=PURPLE, buff=0, stroke_width=8)
        sarr.rotate(PI, about_point=sarr.get_center())
        sl = T("secreted", 30, PURPLE).move_to([-0.9, 0.85, 0], aligned_edge=LEFT)
        self.at("also secretes")
        ts.set_value(1)
        self.play(GrowArrow(sarr), FadeIn(sl), run_time=0.6)
        res = T("filtered + secreted, so more can leave", 28, TEXT).next_to(r_lab, RIGHT, buff=0.15)
        ex = T("leaves: more than was filtered", 28, PURPLE).move_to([6.5, -1.75, 0], aligned_edge=RIGHT)
        self.at("so more of the drug")
        self.play(FadeOut(sarr), FadeOut(sl), FadeIn(res), FadeIn(ex, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


class S08Water(Base):
    def construct(self):
        self.world()
        bar = self.ledger(True)
        self.add(bar)
        g = ValueTracker(1)
        trig = ValueTracker(0)
        wat = make_stream("water", 26, g, hop=(-3.0, 5.7), trig=trig, policy="chance", pre=True, speed=1.0, seed=31, nohop=1, spacing=0.4)
        self.add(wat)
        blue = Rectangle(width=12.4, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([0, -3.3, 0])
        sliver = Rectangle(width=0.12, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([6.14, -3.3, 0])
        l180 = T("180 L filtered", 30, BLUE).move_to([-6.2, -2.65, 0], aligned_edge=LEFT)
        self.at("biggest entry")
        self.play(FadeIn(blue, shift=UP * 0.1), run_time=0.8)
        self.at("of everything filtered")
        self.play(FadeIn(l180), run_time=0.5)
        l99 = T("about 99% taken back", 30, BLUE).move_to([0.6, -2.65, 0])
        self.at("about 99")
        trig.set_value(1)
        self.play(FadeIn(l99, shift=UP * 0.1), run_time=0.6)
        ul = T("1 to 2 L urine", 30, YELLOW).move_to([6.4, -2.65, 0], aligned_edge=RIGHT)
        uarr = Arrow([6.14, -2.9, 0], [6.14, -3.02, 0], color=YELLOW, buff=0, stroke_width=5, max_tip_length_to_length_ratio=1)
        self.at("so the filter")
        self.play(FadeIn(sliver), FadeIn(ul, shift=UP * 0.1), run_time=0.6)
        self.at("take back does")
        self.play(self.terms[2].animate.set_color(GOLD), Indicate(self.terms[2], color=GOLD, scale_factor=1.25), run_time=1.2)
        self.finish()


# -------- predict frame (s09, s10, s11 share it, rebuilt in the same place)
def dial(cx, frac_tracker, label_text):
    cy, r = 0.9, 1.9
    track = Arc(radius=r, start_angle=PI, angle=-PI, stroke_color=GREY, stroke_width=10).move_to([cx, cy + 0, 0], aligned_edge=DOWN)
    track.move_to([cx, cy + r * 0.0, 0])
    track = Arc(radius=r, start_angle=PI, angle=-PI, arc_center=[cx, cy, 0], stroke_color=GREY, stroke_width=10)
    val = always_redraw(lambda: Arc(radius=r, start_angle=PI, angle=-PI * max(frac_tracker.get_value(), 0.001),
                                    arc_center=[cx, cy, 0], stroke_color=BLUE, stroke_width=10))
    needle = always_redraw(lambda: Line([cx, cy, 0], [cx + 1.6 * np.cos(PI - PI * frac_tracker.get_value()),
                                                       cy + 1.6 * np.sin(PI - PI * frac_tracker.get_value()), 0],
                                        color=TEXT, stroke_width=6))
    num = always_redraw(lambda: M(f"{frac_tracker.get_value() * 100:.0f}%", 48, TEXT).move_to([cx, cy + 0.65, 0]))
    lab = T("take-back", 30, BLUE).move_to([cx, cy - 0.45, 0])
    return VGroup(track, val, needle, num, lab)


def urine_bar(cx):
    return Rectangle(width=4.0, height=0.55, stroke_color=YELLOW, stroke_width=3).move_to([cx, -0.75, 0])


class S09Predict(Base):
    def construct(self):
        t1, t2 = ValueTracker(0), ValueTracker(0)
        d1, d2 = dial(-3.4, t1, ""), dial(3.4, t2, "")
        b1, b2 = urine_bar(-3.4), urine_bar(3.4)
        c1 = chip("about 1% more urine", TEXT, 30).move_to([-3.0, -2.7, 0])
        c2 = chip("much more", TEXT, 30).move_to([2.2, -2.7, 0])
        self.add(d1)
        self.play(t1.animate.set_value(0.99), run_time=0.8)
        self.at("tube took back")
        self.add(d2)
        self.play(t2.animate.set_value(0.98), run_time=1.4)
        self.at("instead of")
        self.play(Indicate(d1[3], color=GOLD), run_time=1.0)
        self.at("would urine rise")
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.7)
        ul = T("urine", 28, YELLOW)
        self.at("about 1")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("much more")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("pause and decide")
        self.play(Indicate(c1, color=GOLD), Indicate(c2, color=GOLD), run_time=1.2)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        t1, t2 = ValueTracker(0.99), ValueTracker(0.98)
        self.add(dial(-3.4, t1, ""), dial(3.4, t2, ""), urine_bar(-3.4), urine_bar(3.4))
        self.add(chip("about 1% more urine", TEXT, 30).move_to([-3.0, -2.7, 0]), chip("much more", TEXT, 30).move_to([2.2, -2.7, 0]))
        q = T("Pause and decide", 32, GOLD).move_to([0, 3.4, 0])
        track = Circle(radius=0.5, stroke_color=GREY, stroke_width=6).move_to([5.9, -2.9, 0])
        tv = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(1 - tv.get_value(), 0.001),
                                         arc_center=[5.9, -2.9, 0], stroke_color=GOLD, stroke_width=8))
        self.add(q, track, ring)
        self.play(tv.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S11Reveal(Base):
    def construct(self):
        t1, t2 = ValueTracker(0.99), ValueTracker(0.98)
        self.add(dial(-3.4, t1, ""), dial(3.4, t2, ""))
        b1, b2 = urine_bar(-3.4), urine_bar(3.4)
        c1 = chip("about 1% more urine", TEXT, 30).move_to([-3.0, -2.7, 0])
        c2 = chip("much more", TEXT, 30).move_to([2.2, -2.7, 0])
        self.add(b1, b2, c1, c2)
        u1, u2 = ValueTracker(0), ValueTracker(0)
        f1 = always_redraw(lambda: Rectangle(width=max(u1.get_value() * 4.0 / 3.6, 0.01), height=0.55, stroke_width=0,
                                             fill_color=YELLOW, fill_opacity=0.9).move_to([-5.4 + max(u1.get_value() * 4.0 / 3.6, 0.01) / 2, -0.75, 0]))
        f2 = always_redraw(lambda: Rectangle(width=max(u2.get_value() * 4.0 / 3.6, 0.01), height=0.55, stroke_width=0,
                                             fill_color=YELLOW, fill_opacity=0.9).move_to([1.4 + max(u2.get_value() * 4.0 / 3.6, 0.01) / 2, -0.75, 0]))
        n1 = always_redraw(lambda: T(f"{u1.get_value():.1f} L", 34, YELLOW).move_to([-3.4, -1.45, 0]))
        n2 = always_redraw(lambda: T(f"{u2.get_value():.1f} L", 34, YELLOW).move_to([3.4, -1.45, 0]))
        self.add(f1, f2, n1, n2)
        self.at("much more")
        self.play(u1.animate.set_value(1.8), u2.animate.set_value(3.6), c2[0].animate.set_stroke(GOLD, 6).set_fill(GOLD, 0.3),
                  run_time=2.0)
        dbl = T("x 2", 54, GOLD, weight=BOLD).move_to([0, -0.75, 0])
        self.play(FadeIn(dbl, scale=0.6), run_time=0.6)
        sl = T("a thin sliver of 180 L", 30, BLUE).move_to([0, -3.5, 0])
        self.at("thin sliver")
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.6)
        self.at("shift the take back")
        self.play(t1.animate.set_value(0.985), t2.animate.set_value(0.975), run_time=1.0)
        self.play(t1.animate.set_value(0.99), t2.animate.set_value(0.98), run_time=1.0)
        self.at("that sliver changes")
        self.play(Indicate(f1, color=GOLD), Indicate(f2, color=GOLD), Indicate(dbl, color=GOLD), run_time=1.4)
        self.finish()


class S12Scope(Base):
    def construct(self):
        self.world()
        g1, g2 = ValueTracker(1), ValueTracker(0)
        on = ValueTracker(1)
        a = make_stream("water", 20, g1, hop=(-3.3, -1.0), trig=on, policy="chance", pre=True, speed=0.9, seed=41, nohop=5, spacing=0.5)
        b = make_stream("water", 20, g2, hop=(-3.3, -1.0), trig=on, policy="chance", pre=True, speed=0.9, seed=42, nohop=5, spacing=0.5, y_off=0.0)
        self.add(a, b)
        fl = chip("filtration rises", BLUE, 30).move_to([2.0, 0.9, 0])
        self.at("when filtration rises")
        g2.set_value(1)
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.6)
        seg = self.seg(-3.5, -0.7, "takes back about the same share", TEXT)
        seg[1].move_to([-0.3, -1.75, 0])
        self.at("the proximal tubule")
        self.play(FadeOut(fl), FadeIn(seg, shift=UP * 0.1), run_time=0.7)
        # last stretches glow
        late = Rectangle(width=1.6, height=TUBE_H, stroke_width=0, fill_color=GOLD, fill_opacity=0.35).move_to([2.8, TUBE_Y, 0])
        cd = Rectangle(width=2.6, height=TUBE_H, stroke_width=0, fill_color=GOLD, fill_opacity=0.55).move_to([4.9, TUBE_Y, 0])
        s_late = self.seg(2.0, 3.6, "late distal tubule", GOLD)
        s_cd = self.seg(3.6, 6.2, "collecting duct", GOLD, y=-2.3, ty=-2.7)
        hl = T("hormones", 30, GOLD).move_to([0.6, 0.95, 0])
        icons = VGroup(*[RegularPolygon(6, radius=0.15, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9) for _ in range(5)])
        xs = [2.5, 3.1, 4.2, 4.9, 5.6]
        for ic, x in zip(icons, xs):
            ic.move_to([x, CAP_Y - 0.4, 0])
        self.at("hormones make")
        self.play(FadeOut(seg), FadeIn(late), FadeIn(cd), FadeIn(hl, shift=UP * 0.1), FadeIn(icons), run_time=0.8)
        self.play(AnimationGroup(*[ic.animate.move_to([x, TUBE_Y + TUBE_H / 2 + 0.18, 0]) for ic, x in zip(icons, xs)],
                                 lag_ratio=0.2), run_time=1.0)
        fa = T("fine adjustments", 30, GOLD).move_to([0.6, 0.95, 0])
        self.at("fine adjustments")
        self.play(FadeIn(s_late, shift=UP * 0.1), Transform(hl, fa), run_time=0.7)
        self.at("mainly the collecting duct")
        self.play(FadeIn(s_cd, shift=UP * 0.1), Indicate(cd, color=GOLD, scale_factor=1.05), run_time=0.8)
        ur = T("urine: about 1.5 L", 30, YELLOW).move_to([-2.5, -3.5, 0])
        self.play(FadeIn(ur, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13Close(Base):
    def construct(self):
        self.world()
        bar = self.ledger(True)
        self.add(bar)
        on = ValueTracker(1)
        g = ValueTracker(1)
        gd = ValueTracker(0)
        wat = make_stream("water", 12, g, hop=(-3.2, 5.5), trig=on, policy="chance", pre=True, speed=1.0, seed=51, nohop=1, spacing=0.5)
        glu = make_stream("glucose", 5, g, hop=(-3.2, -1.0), trig=on, policy="chance", pre=True, speed=1.0, seed=52, spacing=0.8)
        sod = make_stream("salt", 6, g, hop=(-3.2, 2.5), trig=on, policy="chance", pre=True, speed=1.0, seed=53, nohop=1, spacing=0.8)
        drg = make_stream("drug", 4, gd, hop=(-3.0, 2.0), trig=on, policy="chance", start="cap", pre=True, speed=1.0, seed=54, spacing=0.8)
        self.add(wat, glu, sod, drg)
        gd.set_value(1)
        self.at("and the take back")
        self.play(Indicate(self.terms[2], color=GOLD, scale_factor=1.1), run_time=1.0)
        rw = {k: row(k) for k in ROWTXT}
        self.at("glucose")
        self.play(FadeIn(rw["glucose"]), run_time=0.5)
        self.at("sodium")
        self.play(FadeIn(rw["sodium"]), run_time=0.5)
        self.at("a drug")
        self.play(FadeIn(rw["drug"]), run_time=0.5)
        self.at("and water")
        self.play(FadeIn(rw["water"]), run_time=0.5)
        self.at("all fit one ledger")
        self.play(Indicate(self.lbar, color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("filtered minus")
        self.play(Indicate(self.terms[1], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at("minus taken")
        self.play(Indicate(self.terms[2], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at("plus added")
        self.play(Indicate(self.terms[3], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.finish()


class S14End(EndCard):
    LINE = "The take-back, not the filter, largely sets how much urine leaves."
