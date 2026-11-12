"""Three Claims in One Drought  (Biochemistrypedia explainer, film 1 of 2, level-up remake 2026-11-11)

COLOR MAP (one colour per concept, whole film; film 2 uses the same)
  GREY  = the population before selection, and its mean (dashed line)
  GOLD  = survivors / selected parents, and S, the selection differential (gold arrow)
  TEAL  = offspring (chicks), and R, the response (teal arrow)
  BLUE  = h squared: a round dial with a needle, scale 0 to 1
Finches are simple brown cartoon birds. All beak-depth plots are schematic ("illustrative"), not the
Grants' data. The pile of 60 grey dots is computed from normal quantiles; S is the real gap between the
mean of the 8 survivors and the mean of the 60; the chicks' pile is that same shape shifted by h2 x S.
The film keeps the pipeline's dark ground (not sand) so the colour map stays readable.
"""
import numpy as np
from statistics import NormalDist
from bp_style import *  # noqa: F401,F403

POP, SURV, OFF, HER = GREY, GOLD, TEAL, BLUE
BROWN = "#9A6A40"
BEAK = "#E8C27A"

# ---------------------------------------------------------------- the world (numbers)
N = 60
SD = 1.3
DX, DY, RAD = 0.38, 0.38, 0.18
AX_Y = -3.25
A_BASE = -2.98          # centre of the bottom dot row (parents)
B_BASE = 0.62           # centre of the bottom dot row of the chicks (row B)
Z = [NormalDist().inv_cdf((i + 0.5) / N) for i in range(N)]
SURV_IDX = [29, 45, 50, 52, 54, 56, 57, 59]


def pile_pos(xs, base):
    cnt, out = {}, []
    for x in xs:
        b = round(x / DX)
        k = cnt.get(b, 0)
        cnt[b] = k + 1
        out.append((b * DX, base + DY * k))
    return out


GREY_POS = pile_pos([-1.9 + SD * z for z in Z], A_BASE)
M0 = float(np.mean([p[0] for p in GREY_POS]))                       # mean before the drought
GOLD_POS = pile_pos([GREY_POS[i][0] for i in SURV_IDX], A_BASE)
MS = float(np.mean([p[0] for p in GOLD_POS]))                       # mean of survivors
S_LEN = MS - M0                                                      # S, in screen units
NC = 40
_off = [1.22 * NormalDist().inv_cdf((i + 0.37) / NC) for i in range(NC)]
_off = [o - float(np.mean(_off)) for o in _off]
CH_POS0 = pile_pos([M0 + o for o in _off], B_BASE)                  # chicks' pile at h2 = 0
H_MID = 0.5
DIAL_C = np.array([5.0, 1.3, 0.0])
DIAL_R = 1.25


# ---------------------------------------------------------------- small helpers
def L(text, size=28, color=TEXT, **kw):
    """Label with a dark halo so a dashed line passing behind never cuts it."""
    t = T(text, size, color, **kw)
    t.set_stroke(BG, 8, background=True)
    t.set_z_index(8)
    return t


def dots(pos, color, op=0.92, r=RAD):
    return VGroup(*[Dot([x, y, 0], radius=r, color=color).set_opacity(op) for x, y in pos])


def finch(s=1.0, beak=1.0, color=BROWN, flip=False):
    body = Ellipse(width=0.95 * s, height=0.6 * s).set_fill(color, 1).set_stroke(TEXT, 2.5)
    tail = Polygon([-0.4 * s, 0.05 * s, 0], [-0.8 * s, 0.24 * s, 0], [-0.72 * s, -0.1 * s, 0]).set_fill(color, 1).set_stroke(TEXT, 2.5)
    head = Circle(radius=0.22 * s).set_fill(color, 1).set_stroke(TEXT, 2.5).move_to([0.38 * s, 0.2 * s, 0])
    bh, ln = 0.07 * s * beak, 0.24 * s * (0.55 + 0.45 * beak)
    bk = Polygon([0.55 * s, 0.2 * s + bh, 0], [0.55 * s + ln, 0.18 * s, 0], [0.55 * s, 0.2 * s - bh, 0]).set_fill(BEAK, 1).set_stroke(TEXT, 2)
    eye = Dot([0.45 * s, 0.27 * s, 0], radius=0.035 * s, color=BG)
    legs = VGroup(Line([0.02 * s, -0.28 * s, 0], [0.0, -0.52 * s, 0]), Line([0.17 * s, -0.27 * s, 0], [0.17 * s, -0.52 * s, 0])).set_stroke(TEXT, max(2, 2.5 * s))
    g = VGroup(tail, legs, body, head, bk, eye)
    g.beak, g.legs = bk, legs
    if flip:
        g.flip(UP)
    return g


def bob(m, amp=0.05, w=1.5, ph=0.0):
    m._t = ph

    def u(mob, dt):
        mob._t += dt
        mob.shift(UP * amp * w * np.cos(w * mob._t) * dt)
    m.add_updater(u)


def axis_group(label=True):
    ax = Arrow([-5.6, AX_Y, 0], [3.3, AX_Y, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.25)
    g = VGroup(ax)
    if label:
        g.add(L("beak depth (mm)", 28).move_to([-1.1, -3.6, 0]))
    return g


def illustrative():
    return L("illustrative", 28, TEXT).move_to([5.45, 3.55, 0])


def mean_line(x, color, top=2.75):
    return DashedLine([x, AX_Y, 0], [x, top, 0], color=color, stroke_width=3.5, dash_length=0.16).set_z_index(-5)


def s_arrow(y=-0.12):
    return Arrow([M0, y, 0], [MS, y, 0], buff=0, color=SURV, stroke_width=9, tip_length=0.28)


def lamp(color, r=1.0):
    glow = Circle(radius=r * 1.35).set_fill(color, 0).set_stroke(width=0)
    bulb = Circle(radius=r).set_stroke(color, 6).set_fill(color, 0.0)
    base = RoundedRectangle(corner_radius=0.08, width=r * 0.9, height=r * 0.3).set_fill(GREY, 0.9).set_stroke(TEXT, 2).next_to(bulb, DOWN, buff=0)
    g = VGroup(glow, bulb, base)
    g.glow, g.bulb = glow, bulb
    return g


def light(g, color, on=True):
    return AnimationGroup(g.bulb.animate.set_fill(color, 0.9 if on else 0.0), g.glow.animate.set_fill(color, 0.28 if on else 0.0), run_time=0.8)


class Dial:
    """Round dial with a needle, scale 0 to 1, driven by a ValueTracker. h2 readout fills inside its own box."""
    def __init__(self, value, center=DIAL_C, r=DIAL_R):
        self.h = ValueTracker(value)
        self.c, self.r = center, r
        arc = Arc(radius=r, start_angle=0, angle=PI, arc_center=center, color=HER, stroke_width=8)
        base = Line(center + LEFT * r, center + RIGHT * r, color=HER, stroke_width=4)
        ticks = VGroup(*[Line(center + (r - 0.0) * np.array([np.cos(a), np.sin(a), 0]), center + (r - 0.22) * np.array([np.cos(a), np.sin(a), 0]), color=HER, stroke_width=4)
                         for a in np.linspace(0, PI, 6)])
        l0 = L("0", 30, HER).move_to(center + LEFT * r + DOWN * 0.4)
        l1 = L("1", 30, HER).move_to(center + RIGHT * r + DOWN * 0.4)
        hub = Dot(center, radius=0.1, color=HER)
        self.needle = Line(center, center, color=HER, stroke_width=7)
        self.readout = L("", 30, HER)
        self.title = L("h²", 40, HER).move_to(center + UP * (r + 0.4))
        self.box = RoundedRectangle(corner_radius=0.12, width=2.7, height=0.62).set_stroke(HER, 2.5).move_to(center + DOWN * 0.95)
        self.static = VGroup(arc, ticks, l0, l1, hub, self.title)
        self.readbox = VGroup(self.box, self.readout)

        def upd(_):
            v = self.h.get_value()
            th = PI * (1 - v)
            self.needle.become(Line(center, center + (r * 0.88) * np.array([np.cos(th), np.sin(th), 0]), color=HER, stroke_width=7))
            self.readout.become(L(f"h² = {v:.2f}", 30, HER).move_to(self.box))
        self.tick = ValueTracker(0)
        self.needle.add_updater(upd)
        upd(None)

    def mobs(self):
        return VGroup(self.static, self.needle, self.readbox)


def chick_pile(h):
    """The chicks' dots at dial value h: the h2 = 0 pile shifted right by h x S."""
    d = dots(CH_POS0, OFF)
    d.shift(RIGHT * h * S_LEN)
    return d


def tie_pile(pile, dial):
    base = [np.array([x, y, 0.0]) for x, y in CH_POS0]
    pile._t = 0.0

    def u(m, dt=0):
        m._t += dt
        sh = dial.h.get_value() * S_LEN
        for k, (d, b) in enumerate(zip(m, base)):
            d.move_to(b + RIGHT * sh + UP * 0.035 * np.sin(1.7 * m._t + 0.9 * k))
    pile.add_updater(u)
    u(pile)


def cloud_base():
    rng = np.random.RandomState(11)
    return [(rng.uniform(-4.4, 2.6), rng.uniform(1.0, 2.8), rng.uniform(0, 6.28)) for _ in range(NC)]


def cloud(t0=0.0):
    """Loose cloud of 60 teal chicks drifting; t0 keeps the drift continuous between scenes."""
    g = dots([(x, y) for x, y, _ in cloud_base()], OFF)
    g._t = t0
    base = cloud_base()

    def u(m, dt):
        m._t += dt
        for d, (x, y, ph) in zip(m, base):
            d.move_to([x + 0.12 * np.sin(0.9 * m._t + ph), y + 0.1 * np.cos(1.1 * m._t + 2 * ph), 0])
    g.add_updater(u)
    u(g, 0)
    return g


def post_world(sc, mean_labels=False, s_label=None, s=False, smean=False):
    """The world after the drought: axis, ghost pile, gold survivors, grey mean line, (S arrow)."""
    ax = axis_group()
    ghost = dots(GREY_POS, POP, op=0.13)
    gold = dots(GOLD_POS, SURV, op=1.0)
    for k, d in enumerate(gold):
        bob(d, 0.035, 1.7, ph=1.3 * k)
    gl = mean_line(M0, POP)
    out = {"ax": ax, "ghost": ghost, "gold": gold, "gl": gl}
    sc.add(gl, ghost, gold, ax, illustrative())
    if smean:
        out["sl"] = mean_line(MS, SURV)
        sc.add(out["sl"])
    if s:
        out["S"] = s_arrow()
        sc.add(out["S"])
    return out


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "How to Test an Evolutionary Explanation"
    TITLE = "Three Claims in One Drought"


# ---------------------------------------------------------------- s01
class S01Hook(SpokenScene):
    def construct(self):
        TOPY = lambda x: -3.9 + 1.8 * np.sqrt(max(0.0, 1 - (x / 6.6) ** 2))
        island = Ellipse(width=13.2, height=3.6).set_fill("#A9793E", 1).set_stroke("#7A5527", 3).move_to([0, -3.9, 0])
        sc = np.array([5.7, 2.9, 0])
        sun = Circle(radius=0.55).set_fill("#F5B041", 1).set_stroke(width=0).move_to(sc)
        rays = VGroup(*[Line(sc + 0.75 * np.array([np.cos(a), np.sin(a), 0]), sc + 1.05 * np.array([np.cos(a), np.sin(a), 0]), color="#F5B041", stroke_width=5)
                        for a in np.linspace(0, TAU, 12, endpoint=False)])
        rays.add_updater(lambda m, dt: m.rotate(0.35 * dt, about_point=sc))
        tufts = VGroup()
        for x in np.linspace(-5.4, 5.4, 12):
            y = TOPY(x)
            tufts.add(VGroup(*[Line([x + dx, y, 0], [x + dx * 1.8, y + 0.32, 0]) for dx in (-0.1, 0.0, 0.1)]).set_stroke("#5E9B4A", 4))
        # flock of 40 birds
        rng = np.random.RandomState(3)
        pts = []
        while len(pts) < 40:
            p = np.array([rng.uniform(-6.0, 6.0), rng.uniform(-1.2, 2.4), 0])
            if p[0] > 4.4 and p[1] > 1.6:
                continue
            if all(np.linalg.norm(p - q) > 0.78 for q in pts) or len(pts) > 0 and rng.rand() < 0.002:
                pts.append(p)
        birds = [finch(0.72).move_to(p) for p in pts]
        for i, b in enumerate(birds):
            bob(b, 0.06, 1.4 + 0.02 * i, ph=i)
        _low = sorted([i for i, p in enumerate(pts) if p[1] < 1.4], key=lambda i: pts[i][0])
        survivors = [_low[int(k)] for k in np.linspace(0, len(_low) - 1, 6)]
        cracks = VGroup()
        for x0 in (-4.2, -2.4, -0.6, 1.4, 3.0, 4.6):
            pts_c = [[x0, TOPY(x0), 0]]
            for k in range(4):
                pts_c.append([pts_c[-1][0] + rng.uniform(-0.35, 0.35), pts_c[-1][1] - 0.3, 0])
            cracks.add(VMobject().set_points_as_corners(pts_c).set_stroke("#4A2F12", 5))
        self.add(island, tufts, sun, rays)
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in birds], lag_ratio=0.04), run_time=2.0)
        self.at("drought")
        self.play(LaggedStart(*[Create(c) for c in cracks], lag_ratio=0.15), tufts.animate.set_stroke("#8B6B3A"), run_time=0.7)
        self.at("most of")
        dead = [b for i, b in enumerate(birds) if i not in survivors]
        for b in dead:
            b.clear_updaters()
        self.play(LaggedStart(*[AnimationGroup(b.animate.set_opacity(0).shift(UP * 0.7 + RIGHT * rng.uniform(0.3, 1.2))) for b in dead], lag_ratio=0.05), run_time=2.0)
        self.at("survivors had")
        news = []
        anims = []
        for i in survivors:
            c = birds[i].get_center()
            birds[i].clear_updaters()
            nb = finch(1.25, beak=2.1).move_to(c)
            news.append(nb)
            anims.append(ReplacementTransform(birds[i], nb))
        self.at("bigger")
        self.play(*anims, run_time=1.5)
        for k, nb in enumerate(news):
            bob(nb, 0.05, 1.3, ph=k)
        self.at("did the finches")
        q = chip("Did the finches just evolve?", color=TEXT, size=40).move_to([-0.7, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- s02
class S02Island(SpokenScene):
    def construct(self):
        box = RoundedRectangle(corner_radius=0.2, width=6.8, height=3.9).set_stroke(BLUE, 3).set_fill(BLUE, 0.12).move_to([-3.0, 1.0, 0])
        isl = VGroup(*[Ellipse(width=w, height=h).set_fill("#B58A4B", 1).set_stroke("#7A5527", 2).move_to([x, y, 0])
                       for x, y, w, h in [(-4.6, 1.5, 1.9, 1.0), (-3.0, 0.5, 1.3, 0.8), (-5.2, 0.2, 1.0, 0.6), (-1.8, 1.6, 0.9, 0.5), (-5.3, -0.45, 0.8, 0.45)]])
        daph = Dot([-1.1, 0.2, 0], radius=0.1, color="#B58A4B")
        ring = Circle(radius=0.3, color=GOLD, stroke_width=5).move_to(daph)
        dlab = L("Daphne Major", 30, TEXT).move_to([-2.5, -0.6, 0])
        dar = Arrow(dlab.get_right() + RIGHT * 0.3, ring.get_bottom() + DOWN * 0.02, buff=0.05, color=TEXT, stroke_width=4, tip_length=0.2)
        gal = L("Galápagos", 32, TEXT).move_to([-3.0, 2.55, 0])
        self.play(FadeIn(box), LaggedStart(*[FadeIn(i, scale=0.8) for i in isl], lag_ratio=0.2), FadeIn(daph), run_time=1.0)
        self.at("daphne major")
        self.play(Create(ring), FadeIn(dlab), Create(dar), run_time=0.9)
        self.at("in the gallipagos")
        self.play(FadeIn(gal), run_time=0.7)
        self.at("researchers")
        f = finch(3.2).move_to([3.7, 1.2, 0])
        bob(f, 0.04, 1.2)
        sheet = RoundedRectangle(corner_radius=0.12, width=6.8, height=2.3).set_stroke(TEXT, 3).set_fill(TEXT, 0.07).move_to([-3.0, -2.35, 0])
        self.play(FadeIn(f, shift=LEFT * 0.4), FadeIn(sheet), run_time=1.0)
        self.at("banded")
        band = Rectangle(width=0.4, height=0.28).set_fill("#E06C9F", 1).set_stroke(TEXT, 2).move_to(f.legs[0].get_center() + DOWN * 0.1)
        self.play(GrowFromCenter(band), run_time=0.6)
        # tally rows fill while the sentence runs
        rows = VGroup()
        rr = np.random.RandomState(5)
        for k in range(5):
            y = -1.65 - 0.42 * k
            rows.add(VGroup(Circle(radius=0.09).set_fill(TEXT, 0.9).set_stroke(width=0).move_to([-6.0, y, 0]),
                            Line([-5.7, y, 0], [-5.7 + rr.uniform(1.8, 4.6), y, 0]).set_stroke(TEXT, 6),
                            ))
        # calipers on the beak
        bx = f.beak.get_left()[0]
        bcy = f.beak.get_center()[1]
        stem_x = bx + 1.25
        op = ValueTracker(0.7)

        def cal(_):
            o = op.get_value()
            hh = 0.07 * 3.2 + 0.05
            yt, yb = bcy + hh + o, bcy - hh - o
            return VGroup(Line([stem_x, yt, 0], [stem_x, yb, 0]), Line([stem_x, yt, 0], [stem_x - 1.0, yt, 0]), Line([stem_x, yb, 0], [stem_x - 1.0, yb, 0])).set_stroke(TEXT, 5)
        c = always_redraw(lambda: cal(None))
        self.at("measured")
        self.add(c)
        self.play(op.animate.set_value(0.0), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows[:2]], lag_ratio=0.5), run_time=1.0)
        self.at("medium ground finch")
        lab = L("medium ground finch", 32, TEXT).move_to([3.8, -1.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows[2:]], lag_ratio=0.6), run_time=1.6)
        self.play(op.animate.set_value(0.6), run_time=0.7)
        self.play(op.animate.set_value(0.0), run_time=0.7)
        self.at("so they knew")
        self.play(Indicate(f.beak, color=GOLD, scale_factor=1.4), op.animate.set_value(0.5), run_time=1.0)
        self.play(op.animate.set_value(0.0), run_time=0.8)
        self.at("before the drought")
        self.play(Indicate(rows, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s03
class S03Dots(SpokenScene):
    def construct(self):
        f = finch(1.4).move_to([-3.5, 1.5, 0])
        bob(f, 0.05)
        tag = illustrative()
        self.play(FadeIn(f, scale=0.7), run_time=0.8)
        pile = dots(GREY_POS, POP)
        # the finch becomes a dot
        dot0 = Dot([-1.0, 1.5, 0], radius=RAD, color=POP)
        self.play(ReplacementTransform(f, dot0), run_time=0.8)
        ax = axis_group(label=False)
        self.at("on a line")
        self.play(Create(ax), dot0.animate.move_to([GREY_POS[30][0], AX_Y + 0.25, 0]), run_time=0.9)
        axl = L("beak depth (mm)", 28).move_to([-1.1, -3.6, 0])
        self.play(FadeIn(axl), FadeIn(tag), run_time=0.5)
        order = list(np.random.RandomState(2).permutation(N))
        for i, d in enumerate(pile):
            d.set_opacity(0)
            d.shift(UP * 3.6)
        self.add(pile)
        self.play(FadeOut(dot0), LaggedStart(*[d.animate.set_opacity(0.92).move_to([GREY_POS[i][0], GREY_POS[i][1], 0]) for i, d in [(int(j), pile[int(j)]) for j in order]], lag_ratio=0.035), run_time=2.0)
        self.at("shallow beaks")
        sh = L("← shallow", 32, TEXT).move_to([-4.6, -3.6, 0])
        self.play(FadeIn(sh, shift=RIGHT * 0.2), run_time=0.6)
        self.at("deep beaks")
        dp = L("deep →", 32, TEXT).move_to([2.4, -3.6, 0])
        self.play(FadeIn(dp, shift=LEFT * 0.2), run_time=0.6)
        self.at("before the drought")
        gl = mean_line(M0, POP)
        gt = L("mean before drought", 30, POP).move_to([M0 - 0.15 - 1.9, 3.55, 0])
        gt.set_color(TEXT)
        self.play(Create(gl), FadeIn(gt, shift=DOWN * 0.2), run_time=1.2)
        self.at("gray cloud")
        self.play(pile.animate.set_opacity(1.0), rate_func=there_and_back, run_time=1.4)
        self.finish()


# ---------------------------------------------------------------- s04
class S04Drought(SpokenScene):
    def construct(self):
        ax = axis_group()
        pile = dots(GREY_POS, POP)
        gl = mean_line(M0, POP)
        gt = L("mean before drought", 30, TEXT).move_to([M0 - 0.15 - 1.9, 3.55, 0])
        self.add(gl, pile, ax, illustrative(), gt)
        wind = VGroup(*[ParametricFunction(lambda t, a=a: np.array([t, 0.15 * np.sin(2.2 * t + a), 0]), t_range=[-1.4, 1.4]).set_stroke(TEXT, 5, opacity=0.8).move_to([-8.5, y, 0])
                        for a, y in [(0, 2.3), (1, 1.1), (2, -0.1), (3, -1.3), (4, -2.2)]])
        self.add(wind)
        self.play(LaggedStart(*[w.animate.shift(RIGHT * 17) for w in wind], lag_ratio=0.18), run_time=2.4, rate_func=linear)
        self.remove(wind)
        self.at("about 85")
        died = chip("about 85% died", color=TEXT, size=36).move_to([2.6, 1.6, 0])
        dead = [i for i in range(N) if i not in SURV_IDX]
        rng = np.random.RandomState(9)
        # more of the dead come from the left: order by position + noise
        dead.sort(key=lambda i: GREY_POS[i][0] + rng.normal(0, 0.9))
        self.play(FadeIn(died, scale=0.8), LaggedStart(*[pile[i].animate.set_opacity(0.13) for i in dead], lag_ratio=0.06), run_time=3.2)
        self.at("were not a random")
        golds = dots([GREY_POS[i] for i in SURV_IDX], SURV, op=1.0)
        self.add(golds)
        self.play(FadeOut(died), *[pile[i].animate.set_opacity(0.13) for i in SURV_IDX], Flash(golds, color=SURV, flash_radius=1.6, line_length=0.3), run_time=0.9)
        self.play(*[g.animate.move_to([x, y, 0]) for g, (x, y) in zip(golds, GOLD_POS)], run_time=1.6)
        self.at("larger birds")
        self.play(Indicate(golds, color=SURV, scale_factor=1.25), run_time=1.2)
        self.at("males")
        tags = VGroup(*[T("♂", 40, SURV).set_stroke(BG, 6, background=True).move_to([GOLD_POS[i][0], GOLD_POS[i][1] + 0.6, 0]) for i in (2, 4, 7)])
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tags], lag_ratio=0.3), run_time=1.2)
        self.at("survived best")
        self.play(Indicate(golds, color=SURV, scale_factor=1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s05
class S05Seeds(SpokenScene):
    def construct(self):
        w = post_world(self)
        self.remove(w["ax"])
        self.add(w["ax"])
        panel = RoundedRectangle(corner_radius=0.2, width=6.9, height=2.2).set_fill(BG, 1).set_stroke(TEXT, 3).move_to([-1.6, 2.1, 0])
        rng = np.random.RandomState(4)
        soft = VGroup(*[Dot([rng.uniform(-4.8, 1.6), rng.uniform(1.15, 2.85), 0], radius=0.06, color="#E8DCA8") for _ in range(34)])
        hard = VGroup(*[Ellipse(width=0.62, height=0.36).set_fill("#8B5A2B", 1).set_stroke("#5A3A1B", 3).rotate(rng.uniform(-0.6, 0.6)).move_to(p)
                        for p in [[-4.3, 1.7, 0], [-3.0, 2.4, 0], [-1.8, 1.5, 0], [-0.6, 2.3, 0], [0.5, 1.6, 0], [-2.4, 2.2, 0]]])
        self.play(FadeIn(panel), FadeIn(soft), FadeIn(hard), Indicate(w["gold"], color=SURV, scale_factor=1.2), run_time=1.4)
        self.at("food left")
        self.play(soft.animate.shift(RIGHT * 2.5 + UP * 0.6).set_opacity(0), run_time=1.8)
        self.remove(soft)
        self.at("large hard seeds")
        lab = L("large, hard seeds", 32, TEXT).move_to([-1.6, 3.55, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), hard.animate.scale(1.15), run_time=1.0)
        self.at("something was sorting")
        f = finch(2.0, beak=2.1, flip=True).move_to([4.9, 2.0, 0])
        bob(f, 0.04, 1.3)
        seed = Ellipse(width=0.7, height=0.4).set_fill("#8B5A2B", 1).set_stroke("#5A3A1B", 3).move_to([3.4, 1.95, 0])
        self.play(FadeIn(f, shift=LEFT * 0.4), FadeIn(seed), run_time=1.0)
        h1 = Ellipse(width=0.35, height=0.4).set_fill("#8B5A2B", 1).set_stroke("#5A3A1B", 3).move_to([3.22, 1.95, 0])
        h2 = Ellipse(width=0.35, height=0.4).set_fill("#8B5A2B", 1).set_stroke("#5A3A1B", 3).move_to([3.58, 1.95, 0])
        self.play(FadeOut(seed), FadeIn(h1), FadeIn(h2), run_time=0.2)
        self.play(h1.animate.shift(LEFT * 0.15 + DOWN * 0.1), h2.animate.shift(RIGHT * 0.15 + DOWN * 0.1), f.beak.animate.scale(0.8), run_time=0.8)
        self.at("and the seeds")
        dl = DashedLine([-0.2, 1.0, 0], [MS, -2.2, 0], color=SURV, stroke_width=5, dash_length=0.18)
        self.play(Create(dl), run_time=1.2)
        self.at("leading suspect")
        sus = L("suspect", 34, SURV).move_to([MS + 1.7, 0.1, 0])
        self.play(FadeIn(sus, shift=LEFT * 0.2), Indicate(w["gold"], color=SURV, scale_factor=1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s06
class S06S(SpokenScene):
    def construct(self):
        w = post_world(self)
        gt = L("mean before drought", 30, TEXT).move_to([M0 - 0.15 - 1.9, 3.55, 0])
        self.add(gt)
        self.play(Indicate(w["gold"], color=SURV, scale_factor=1.2), run_time=1.0)
        self.at("average now sits")
        sl = mean_line(MS, SURV)
        st = L("survivors' mean", 30, SURV).move_to([MS + 0.15 + 1.4, 3.55, 0])
        self.play(Create(sl), FadeIn(st, shift=DOWN * 0.2), run_time=1.4)
        self.at("to the right of the old")
        self.play(Indicate(gt, color=TEXT, scale_factor=1.08), run_time=1.0)
        self.at("that gap")
        arr = s_arrow()
        lab = L("selection through survival", 30, SURV).move_to([2.5, 0.62, 0])
        self.play(GrowArrow(arr), run_time=1.1)
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.8)
        self.at("if the survivors breed")
        sub = VGroup(L("if survivors breed about equally,", 30, TEXT), L("S = selection differential", 34, SURV)).arrange(DOWN, buff=0.15).move_to([3.2, 1.7, 0])
        self.play(FadeIn(sub[0], shift=UP * 0.2), run_time=1.0)
        self.at("selection differential")
        self.play(FadeIn(sub[1], shift=UP * 0.2), run_time=0.9)
        self.at("called s")
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        self.play(Indicate(sub[1], color=SURV, scale_factor=1.1), FadeIn(bigS, scale=1.4), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s07
class S07Notyet(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        self.add(bigS)
        self.at("so is that")
        frame_ = RoundedRectangle(corner_radius=0.1, width=5.0, height=1.0).set_fill(BG, 0.92).set_stroke(TEXT, 6)
        stamp = VGroup(frame_, T("EVOLUTION?", 44, TEXT, weight=BOLD)).move_to([0.8, -1.2, 0]).rotate(0.12)
        bob(stamp, 0.08, 1.6)
        self.play(FadeIn(stamp, shift=DOWN * 0.8), run_time=1.0)
        self.at("not yet shown")
        ny = L("not yet shown", 34, TEXT).move_to([4.9, -2.1, 0])
        self.play(FadeIn(ny, shift=LEFT * 0.3), run_time=0.8)
        self.at("survival tells you")
        self.play(Indicate(w["gold"], color=SURV, scale_factor=1.3), run_time=1.2)
        self.at("what their chicks")
        rowbox = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=7.2, height=2.9).move_to([-0.8, 1.9, 0]).set_stroke(OFF, 4), num_dashes=60)
        q = L("?", 140, OFF).move_to([-0.8, 1.9, 0])
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        self.play(FadeOut(stamp), FadeOut(ny), Create(rowbox), FadeIn(q, scale=0.7), FadeIn(rl), run_time=1.4)
        self.at("that depends")
        ar = Arrow([MS + 2.1, -1.9, 0], [MS + 2.1, 0.3, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.28)
        inh = L("inheritance", 34, TEXT).move_to([MS + 3.5, -0.8, 0])
        self.play(GrowArrow(ar), run_time=1.0)
        self.play(FadeIn(inh, shift=LEFT * 0.2), run_time=0.8)
        self.play(q.animate.scale(1.25), rate_func=there_and_back, run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s08
class S08H2(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        self.add(bigS)
        dial = Dial(0.0)
        self.add(dial.static)
        self.play(FadeIn(dial.static), FadeIn(dial.needle), FadeIn(dial.readbox), run_time=1.0)
        self.play(dial.h.animate.set_value(0.35), run_time=1.2)
        self.at("variation due to")
        parent = finch(2.0).move_to([-3.1, 1.9, 0])
        chick = finch(1.3, color="#B58763").move_to([-0.3, 1.8, 0])
        bob(parent, 0.04, 1.2)
        bob(chick, 0.04, 1.5, 1)
        self.play(FadeIn(parent, shift=RIGHT * 0.3), run_time=1.0)
        self.play(dial.h.animate.set_value(0.6), run_time=1.5)
        self.at("that is the part")
        self.play(FadeIn(chick, shift=RIGHT * 0.3), run_time=1.0)
        self.at("makes offspring")
        po = Circle(radius=0.32).move_to(parent.beak.get_center() + RIGHT * 0.1).set_stroke(HER, 5)
        co = Circle(radius=0.22).move_to(chick.beak.get_center() + RIGHT * 0.05).set_stroke(HER, 5)
        lab = L("resemble their parents", 30, HER).move_to([-4.5, 0.45, 0])
        self.play(Create(po), Create(co), run_time=1.0)
        self.at("resemble their parents")
        self.play(FadeIn(lab, shift=UP * 0.2), Indicate(po, color=HER, scale_factor=1.3), Indicate(co, color=HER, scale_factor=1.3), run_time=1.2)
        self.at("it runs from zero")
        self.play(FadeOut(lab), dial.h.animate.set_value(0.0), run_time=1.2)
        self.at("to one")
        self.play(dial.h.animate.set_value(1.0), run_time=1.6)
        self.at("in one population")
        ol = L("one population, one environment", 32, TEXT).move_to([-0.9, 3.4, 0])
        self.play(FadeIn(ol, shift=DOWN * 0.2), dial.h.animate.set_value(H_MID), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------- s09 / s10 shared
def predict_state(sc, t0):
    w = post_world(sc, smean=True, s=True)
    bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
    rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
    dial = Dial(0.0)
    cl = cloud(t0)
    q = chip("h² = 0: where do the chicks land?", color=TEXT, size=36).set_z_index(9).move_to([-0.7, 3.2, 0])
    sc.add(bigS, rl, dial.static, dial.needle, dial.readbox, cl, q)
    return w, dial, cl, q


class S09Predict(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        dial = Dial(H_MID)
        self.add(bigS, dial.static, dial.needle, dial.readbox)
        gp = sorted(GOLD_POS)
        pairs = VGroup(*[ArcBetweenPoints([gp[2 * k][0], gp[2 * k][1] + 0.2, 0], [gp[2 * k + 1][0], gp[2 * k + 1][1] + 0.2, 0], angle=-1.2).set_stroke(SURV, 5) for k in range(4)])
        self.at("pair up")
        self.play(Create(pairs), run_time=1.2)
        self.at("raise chicks")
        cl = cloud(0.0)
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        for d in cl:
            d.set_opacity(0)
        self.add(cl)
        self.play(*[d.animate.set_opacity(0.92) for d in cl], FadeIn(rl, shift=UP * 0.2), run_time=1.8)
        self.at("suppose")
        self.at("inherited at all")
        self.play(dial.h.animate.set_value(0.0), run_time=1.4)
        self.at("where on the line")
        q = chip("h² = 0: where do the chicks land?", color=TEXT, size=36).set_z_index(9).move_to([-0.7, 3.2, 0])
        self.play(FadeIn(q, shift=DOWN * 0.3), run_time=0.8)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        w, dial, cl, q = predict_state(self, 10.2)
        ang = ValueTracker(TAU)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=ang.get_value(), color=TEXT, stroke_width=8).move_to([5.5, -1.7, 0]))
        back = Circle(radius=0.5).set_stroke(GREY, 4).move_to([5.5, -1.7, 0])
        self.add(back, ring)
        self.play(ang.animate.set_value(0.001), run_time=5.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s11
class S11Zero(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        dial = Dial(0.0)
        cl = cloud(15.7)
        self.add(bigS, rl, dial.static, dial.needle, dial.readbox, cl)
        pile = dots(CH_POS0, OFF)
        order = list(np.random.RandomState(8).permutation(NC))
        cl.clear_updaters()
        self.play(LaggedStart(*[cl[int(j)].animate.move_to([CH_POS0[int(j)][0], CH_POS0[int(j)][1], 0]) for j in order], lag_ratio=0.03), run_time=2.6)
        self.remove(cl)
        tie_pile(pile, dial)
        self.add(pile)
        self.at("if the environment")
        lab = L("h² = 0, same environment", 32, TEXT).move_to([-1.0, 3.55, 0])
        tk = Line([M0, 0.62, 0], [M0, 2.75, 0], color=OFF, stroke_width=6).set_z_index(-4)
        self.play(FadeIn(lab, shift=DOWN * 0.2), Create(tk), run_time=1.0)
        self.at("however strong")
        self.play(Indicate(w["S"], color=SURV, scale_factor=1.1), run_time=1.2)
        self.at("average would not move")
        lab2 = L("h² = 0, same environment: no shift in the mean", 32, TEXT).move_to([-1.0, 3.55, 0])
        self.play(Transform(lab, lab2), Indicate(tk, color=OFF, scale_factor=1.25), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s12
class S12Dial(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        dial = Dial(0.0)
        pile = dots(CH_POS0, OFF)
        tie_pile(pile, dial)
        tk = Line([M0, 0.62, 0], [M0, 2.75, 0], color=OFF, stroke_width=6).set_z_index(-4)
        tk.add_updater(lambda m: m.move_to([M0 + dial.h.get_value() * S_LEN, 1.69, 0]))
        self.add(bigS, rl, dial.static, dial.needle, dial.readbox, pile, tk)
        self.wait(0.3)
        self.play(dial.h.animate.set_value(1.0), run_time=2.4)
        self.at("average lands on")
        lab = L("chicks' average = parents' average", 32, TEXT).move_to([-1.0, 3.55, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), Indicate(tk, color=OFF, scale_factor=1.25), run_time=1.4)
        self.at("for most real traits")
        self.play(FadeOut(lab), run_time=0.5)
        self.at("sits in between")
        self.play(dial.h.animate.set_value(H_MID), run_time=2.2)
        self.at("moves only part")
        lab2 = L("only part of the way", 34, OFF).move_to([-1.0, 3.55, 0])
        self.play(FadeIn(lab2, shift=DOWN * 0.2), run_time=0.8)
        self.at("part of the way")
        self.play(Indicate(tk, color=OFF, scale_factor=1.25), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s13
class S13R(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        dial = Dial(H_MID)
        pile = dots(CH_POS0, OFF)
        tie_pile(pile, dial)
        tk = Line([M0, 0.62, 0], [M0, 2.75, 0], color=OFF, stroke_width=6).set_z_index(-4)
        tk.add_updater(lambda m: m.move_to([M0 + dial.h.get_value() * S_LEN, 1.69, 0]))
        self.add(bigS, rl, dial.static, dial.needle, dial.readbox, pile, tk)
        self.wait(0.3)
        self.at("that part is the response")
        ry = 0.12
        r_arrow = always_redraw(lambda: Arrow([M0, ry, 0], [M0 + max(0.05, dial.h.get_value() * S_LEN), ry, 0], buff=0, color=OFF, stroke_width=9, tip_length=min(0.26, max(0.05, dial.h.get_value() * S_LEN * 0.5))))
        rlab = L("R = response", 30, OFF); rlab.next_to([M0 - 0.2, ry, 0], LEFT, buff=0.3)
        self.add(r_arrow)
        self.play(FadeIn(rlab, shift=RIGHT * 0.2), run_time=1.0)
        self.at("called r")
        self.play(Indicate(rlab, color=OFF, scale_factor=1.15), run_time=0.8)
        self.at("equation says")
        eq = VGroup(M("R", 42, OFF), M("=", 42, TEXT), M("h²", 42, HER), M("×", 42, TEXT), M("S", 42, SURV)).arrange(RIGHT, buff=0.2).move_to([4.95, -1.4, 0])
        self.play(FadeIn(eq[0], shift=UP * 0.2), run_time=0.6)
        self.at("equals h squared")
        self.play(FadeIn(eq[1]), run_time=0.4)
        self.play(FadeIn(eq[2], shift=UP * 0.2), run_time=0.7)
        self.at("times s")
        self.play(FadeIn(eq[3]), FadeIn(eq[4], shift=UP * 0.2), run_time=0.8)
        self.at("predicts how far")
        self.play(dial.h.animate.set_value(0.3), run_time=1.2)
        self.play(dial.h.animate.set_value(0.7), run_time=1.5)
        self.at("moves")
        self.play(dial.h.animate.set_value(H_MID), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s14 / s15
LX = [-4.35, 0.0, 4.35]
LCOL = [SURV, HER, OFF]
LNAMES = ["selection", "inheritance", "offspring changed"]


class S14Three(SpokenScene):
    def construct(self):
        w = post_world(self, smean=True, s=True)
        bigS = L("S", 54, SURV).move_to([MS + 0.55, -0.12, 0])
        rl = L("their chicks", 26, OFF).move_to([-5.75, 1.8, 0])
        dial = Dial(H_MID)
        pile = dots(CH_POS0, OFF)
        pile.shift(RIGHT * H_MID * S_LEN)
        r_arrow = Arrow([M0, 0.12, 0], [M0 + H_MID * S_LEN, 0.12, 0], buff=0, color=OFF, stroke_width=9, tip_length=0.26)
        self.add(bigS, rl, dial.static, dial.needle, dial.readbox, pile, r_arrow)
        allw = Group(*self.mobjects)
        self.wait(0.4)
        lamps = [lamp(c, 1.0).move_to([x, 1.0, 0]) for x, c in zip(LX, LCOL)]
        names = [L(n, 34, c).move_to([x, -1.1, 0]) for n, x, c in zip(LNAMES, LX, LCOL)]
        dial.needle.clear_updaters()
        self.play(FadeOut(allw), run_time=1.2)
        self.remove(*self.mobjects)
        self.at("three claims")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in lamps], lag_ratio=0.25), run_time=1.4)
        self.at("selection happened")
        self.play(light(lamps[0], LCOL[0]), FadeIn(names[0], shift=UP * 0.2), run_time=0.9)
        self.at("the trait is inherited")
        self.play(light(lamps[1], LCOL[1]), FadeIn(names[1], shift=UP * 0.2), run_time=0.9)
        self.at("the offspring changed")
        self.play(light(lamps[2], LCOL[2]), FadeIn(names[2], shift=UP * 0.2), run_time=0.9)
        self.at("each claim needs")
        ev = L("its own evidence", 38, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(ev, shift=UP * 0.2), *[light(l, c, False) for l, c in zip(lamps, LCOL)], run_time=1.0)
        self.finish()


def tally_icon():
    r = RoundedRectangle(corner_radius=0.12, width=3.3, height=2.3).set_stroke(SURV, 4).set_fill(SURV, 0.1)
    rows = VGroup(*[VGroup(Dot([-1.3, 0.8 - 0.42 * k, 0], radius=0.09, color=SURV), Line([-1.0, 0.8 - 0.42 * k, 0], [-1.0 + 1.6 - 0.2 * (k % 3), 0.8 - 0.42 * k, 0]).set_stroke(SURV, 6)) for k in range(5)])
    return VGroup(r, rows)


def pair_icon():
    a = finch(1.25).move_to([-0.7, 0.2, 0])
    b = finch(0.85, color="#B58763").move_to([0.95, 0.0, 0])
    oa = Circle(radius=0.2).set_stroke(HER, 4).move_to(a.beak.get_center() + RIGHT * 0.08)
    ob = Circle(radius=0.14).set_stroke(HER, 4).move_to(b.beak.get_center() + RIGHT * 0.05)
    return VGroup(a, b, oa, ob)


def teal_chicks_icon():
    fs = VGroup(*[finch(0.9, color=OFF).move_to([-0.7 + 1.55 * k, -0.4, 0]) for k in range(2)])
    bk = fs[1].beak
    cy = bk.get_center()[1]
    stem_x = bk.get_right()[0] + 0.35
    cal = VGroup(Line([stem_x, cy + 0.55, 0], [stem_x, cy - 0.55, 0]), Line([stem_x, cy + 0.2, 0], [stem_x - 0.5, cy + 0.2, 0]), Line([stem_x, cy - 0.2, 0], [stem_x - 0.5, cy - 0.2, 0])).set_stroke(TEXT, 4)
    return VGroup(fs, cal)


class S15Evidence(SpokenScene):
    def construct(self):
        lamps = [lamp(c, 0.85).move_to([x, 1.55, 0]) for x, c in zip(LX, LCOL)]
        names = [L(n, 36, c).move_to([x, 0.05, 0]) for n, x, c in zip(LNAMES, LX, LCOL)]
        eq = VGroup(M("R", 52, OFF), M("=", 52, TEXT), M("h²", 52, HER), M("×", 52, TEXT), M("S", 52, SURV)).arrange(RIGHT, buff=0.24).move_to([0, 3.3, 0])
        self.add(*lamps, *names, eq)
        icons = [tally_icon().scale(1.1).move_to([LX[0], -1.95, 0]), pair_icon().scale(1.15).move_to([LX[1], -1.95, 0]), teal_chicks_icon().scale(1.15).move_to([LX[2], -1.95, 0])]
        self.wait(0.2)
        self.play(FadeIn(icons[0], shift=UP * 0.5), run_time=1.0)
        self.at("lights the first")
        self.play(light(lamps[0], LCOL[0]), Indicate(names[0], color=SURV, scale_factor=1.1), run_time=1.0)
        self.at("comparing relatives")
        self.play(FadeIn(icons[1], shift=UP * 0.5), run_time=1.0)
        self.at("lights the second")
        self.play(light(lamps[1], LCOL[1]), Indicate(names[1], color=HER, scale_factor=1.1), run_time=1.0)
        self.at("only measuring")
        self.play(FadeIn(icons[2], shift=UP * 0.5), run_time=1.0)
        cal = icons[2][1]
        self.play(cal.animate.shift(LEFT * 0.1), run_time=0.6)
        self.at("lights the third")
        self.play(light(lamps[2], LCOL[2]), Indicate(names[2], color=OFF, scale_factor=1.1), run_time=1.0)
        self.at("to show that selection")
        self.play(Indicate(eq, color=TEXT, scale_factor=1.12), run_time=1.4)
        self.at("you need all three")
        self.play(*[Indicate(l, color=c, scale_factor=1.12) for l, c in zip(lamps, LCOL)], run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "Evolution needs selection, inheritance,\nand changed offspring."
