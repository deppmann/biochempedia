"""Same Factor, Second Job  (Developmental Neuroscience, competition for targets, chapter 6)

COLOR MAP (one color per concept, same as the other chapters; taken from scenes.old.py)
  BLUE   = a neuron whose fate is not yet decided (here also the chick motor neurons)
  GREEN  = a neuron that survives, and the fibres of survivors
  RED    = a neuron that dies; "more death"
  YELLOW = nerve growth factor (NGF)
  PURPLE = the receptor TrkA (its level)
  PINK   = signaling downstream of TrkA (the length of its signal)
  ORANGE = BDNF (the released factor, as in the other chapters)
  TEAL   = the receptor p75
  TEXT   = plain labels (white); also curare molecules (white blobs) in this film
  GOLD   = the question mark, pulses of activity, and one highlight at a time
  GREY   = targets, muscle, spinal cord, outlines, axes (light grey LGREY = chick motor axons)
  OTHER  = several unnamed factors, one hue each (orchid, sand, periwinkle, peach; none green): chick motor neurons only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E8789F"
TEAL = "#3FB8C0"
DARK = "#0f1117"
LGREY = "#B8BFCC"
OTHER = ["#E37BD9", "#D2B48C", "#9AA5FF", "#FFC8A0"]


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# helpers
def soma(p, color=BLUE, r=0.27, op=0.9):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to(p)
    c.set_z_index(3)
    return c


def to_state(d, color, op=0.9):
    return d.animate.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)


def dot(p, color, r=0.1):
    d = Circle(radius=r, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=1).move_to(p)
    d.set_z_index(4)
    return d


def ngf_dot(p, r=0.1):
    return dot(p, YELLOW, r)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(cx, cy, w, h, color=GREY, op=0.12, r=0.25, sw=3):
    b = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                         fill_color=color, fill_opacity=op).move_to(P(cx, cy))
    b.set_z_index(0)
    return b


def left_text(s, x, y, size=26, color=TEXT, font=FONT, **kw):
    t = T(s, size, color, font=font, **kw)
    return t.move_to(P(x + t.width / 2, y))


def gang_outline(cx, cy, w, h):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.08).move_to(P(cx, cy))


def gang_cells(cx, cy, w, h, sp=0.9, r=0.28, color=BLUE, op=0.85):
    rng = np.random.RandomState(11)
    m = r + 0.12
    pts = []
    for j in range(-12, 13):
        for i in range(-12, 13):
            x = i * sp + (sp / 2 if j % 2 else 0.0)
            y = j * sp * 0.866
            if (x / (w / 2 - m)) ** 2 + (y / (h / 2 - m)) ** 2 <= 1.0:
                pts.append((x + rng.uniform(-0.05, 0.05), y + rng.uniform(-0.05, 0.05)))
    return VGroup(*[soma(P(cx + x, cy + y), color, r, op) for x, y in pts])


def strike(c, color=TEXT, w=9):
    ln = Line(c.get_left() + RIGHT * 0.02, c.get_right() + LEFT * 0.02, color=color, stroke_width=w).move_to(c.get_center())
    ln.set_z_index(8)
    return ln


def check(cx, cy, s=0.17, color=GREEN, w=6):
    a, b, c = P(cx - s, cy), P(cx - s * 0.25, cy - s * 0.85), P(cx + s * 1.1, cy + s * 0.95)
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b, c, color=color, stroke_width=w))


def leader(a, b, color=LGREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w)


def tree(root, ang, length, depth, offs0, offs, shrink=0.78):
    """Deterministic branching tree. Returns levels: levels[d] = list of (p0, p1) segments."""
    levels, cur = [], [(np.array(root, float), ang, length)]
    for d in range(depth):
        segs, nxt = [], []
        for p, a, L in cur:
            q = p + L * np.array([np.cos(a), np.sin(a), 0.0])
            segs.append((p, q))
            for o in (offs0 if d == 0 else offs):
                nxt.append((q, a + o, L * shrink))
        levels.append(segs)
        cur = nxt
    return levels


def lines_of(segs, color=GREEN, w=3.0):
    return VGroup(*[Line(p, q, color=color, stroke_width=w) for p, q in segs])


class Dial:
    """A half-circle gauge with a needle. val 0 = far left, 1 = far right."""

    def __init__(self, cx, cy, r, color=GREY, val=0.5, band=False, sw=6):
        self.c, self.r, self.val = P(cx, cy), r, val
        arc = Arc(radius=r, start_angle=0, angle=PI, arc_center=self.c, stroke_color=color, stroke_width=sw)
        base = Line(P(cx - r, cy), P(cx + r, cy), stroke_color=color, stroke_width=3)
        parts = [arc, base]
        if band:
            parts.append(Arc(radius=r, start_angle=PI * 0.35, angle=PI * 0.3, arc_center=self.c,
                             stroke_color=GREEN, stroke_width=sw + 8))
        self.frame = VGroup(*parts)
        th = PI * (1 - val)
        self.needle = Line(self.c, self.c + 0.86 * r * np.array([np.cos(th), np.sin(th), 0]),
                           stroke_color=TEXT, stroke_width=6)
        self.hub = Dot(self.c, radius=0.13, color=TEXT)
        self.needle.set_z_index(5)
        self.hub.set_z_index(6)

    def all(self):
        return VGroup(self.frame, self.needle, self.hub)

    def sweep(self, new):
        a = Rotate(self.needle, PI * (self.val - new), about_point=self.c)
        self.val = new
        return a


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "Same Factor, Second Job"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        NP = P(-4.6, 0)
        n = soma(NP, BLUE, 1.2, 0.85)
        dend = VGroup(*[Line(NP + 1.15 * np.array([np.cos(a), np.sin(a), 0]), NP + 1.95 * np.array([np.cos(a), np.sin(a), 0]),
                             color=BLUE, stroke_width=5) for a in (2.2, 3.14, 4.08)])
        glow = Circle(radius=1.7, stroke_width=0, fill_color=GREEN, fill_opacity=0.0).move_to(NP)
        tgt = box(3.5, 0, 6.2, 5.6, GREY, 0.12, 0.3, 3)
        tlab = T("target", 28, GREY).move_to(P(3.5, -2.45))
        axon = Line(P(-3.4, 0), P(0.4, 0), color=GREEN, stroke_width=6)
        fan = lines_of([(P(0.4, 0), P(1.9, 1.0)), (P(0.4, 0), P(2.0, 0.0)), (P(0.4, 0), P(1.9, -1.0))], GREEN, 4)
        q = T("?", 170, GOLD, weight=BOLD).move_to(P(4.5, 0.2))

        self.at("If a neuron")
        self.play(FadeIn(n, scale=0.6), FadeIn(dend), run_time=0.6)
        self.at("survives")
        self.play(to_state(n, GREEN, 0.9), dend.animate.set_color(GREEN), glow.animate.set_fill(GREEN, opacity=0.18), run_time=0.6)
        self.at("does it innervate")
        self.play(Create(axon), run_time=0.8)
        self.at("its target")
        self.play(FadeIn(tgt), FadeIn(tlab), Create(fan), run_time=0.4)
        self.at("normally")
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
G1 = (-2.4, 0.1, 7.2, 5.4)


def s02_final():
    d = {}
    d["out"] = gang_outline(*G1)
    d["cells"] = gang_cells(*G1, sp=0.95, r=0.3, color=GREEN, op=0.85)
    d["glab"] = T("sympathetic ganglion", 26, GREY).move_to(P(G1[0], -3.3))
    d["bax"] = chip("Bax", RED, 50, pad=0.28, fill_opacity=0.3).move_to(P(4.6, 1.3))
    d["ngf"] = chip("NGF", YELLOW, 50, pad=0.28, fill_opacity=0.3).move_to(P(4.6, -0.9))
    d["xb"] = strike(d["bax"], TEXT, 10)
    d["xn"] = strike(d["ngf"], TEXT, 10)
    return d


class S02(SpokenScene):
    def construct(self):
        d = s02_final()
        cells = d["cells"]
        for c in cells:
            c.set_stroke(BLUE, opacity=1.0).set_fill(BLUE, opacity=0.85)

        self.at("Go back")
        self.play(FadeIn(d["out"]), FadeIn(d["glab"]), LaggedStart(*[FadeIn(c, scale=0.4) for c in cells], lag_ratio=0.01),
                  run_time=0.8)
        self.at("lacking both")
        self.play(FadeIn(d["bax"], scale=0.7), run_time=0.4)
        self.play(Create(d["xb"]), run_time=0.4)
        self.at("and NGF")
        self.play(FadeIn(d["ngf"], scale=0.7), run_time=0.4)
        self.play(Create(d["xn"]), run_time=0.4)
        self.at("their sympathetic")
        self.play(Indicate(d["glab"], color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("survive")
        self.play(*[to_state(c, GREEN, 0.85) for c in cells], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
BODY_G = (-5.2, 0.0, 2.8, 5.6)
ROW_X, ROW_W, ROW_H = 0.8, 5.6, 2.3
ROW_Y = {"sal": 2.55, "heart": 0.0, "trach": -2.55}
NAMES = {"sal": "salivary glands", "heart": "heart", "trach": "trachea"}
FIB_YS = np.linspace(-0.95, 0.95, 12)


def dashed_ghost(segs, num=18):
    return VGroup(*[DashedVMobject(Line(p, q, color=GREY, stroke_width=2.6, stroke_opacity=0.45), num_dashes=num) for p, q in segs])


class Body:
    def __init__(self):
        self.out = gang_outline(*BODY_G)
        self.cells = gang_cells(*BODY_G, sp=0.6, r=0.17, color=GREEN, op=0.85)
        self.glab = T("ganglion", 24, GREY).move_to(P(-5.2, -3.1))
        self.legend = T("dotted = normal", 24, GREY).move_to(P(-5.2, -3.55))
        self.rows = {k: box(ROW_X, y, ROW_W, ROW_H, GREY, 0.1, 0.2, 3) for k, y in ROW_Y.items()}
        self.names = {k: left_text(NAMES[k], 3.85, y + 0.3, 26, TEXT) for k, y in ROW_Y.items()}
        self.tag = T("at birth", 30, GOLD).move_to(P(-5.2, 3.35))
        self.status = {"sal": left_text("no innervation", 3.85, ROW_Y["sal"] - 0.3, 24, LGREY),
                       "heart": left_text("greatly reduced", 3.85, ROW_Y["heart"] - 0.3, 24, LGREY),
                       "trach": left_text("near normal", 3.85, ROW_Y["trach"] - 0.3, 24, LGREY)}
        # ghost of the normal fibre pattern, dotted grey, in every box
        self.ghost = {}
        for k, y in ROW_Y.items():
            segs = [(P(-3.8, y + o), P(-2.0, y + o)) for o in (-0.25, 0, 0.25)]
            segs += [(P(-2.0, y + 0.3 * (yy / 0.95)), P(3.3, y + yy)) for yy in FIB_YS]
            self.ghost[k] = dashed_ghost(segs, 20)
        # heart: one thin trunk and three thin fibres
        yh = ROW_Y["heart"]
        self.h_trunk = Line(P(-3.8, yh), P(-2.0, yh), color=GREEN, stroke_width=3)
        self.h_fib = lines_of([(P(-2.0, yh), P(1.9, yh - 0.55)), (P(-2.0, yh), P(2.7, yh + 0.05)),
                               (P(-2.0, yh), P(2.2, yh + 0.65))], GREEN, 3)
        # trachea: a thick trunk and a dense field of fibres
        yt = ROW_Y["trach"]
        self.t_trunk = VGroup(*[Line(P(-3.8, yt + o), P(-2.0, yt + o), color=GREEN, stroke_width=5) for o in (-0.25, 0, 0.25)])
        self.t_fib = lines_of([(P(-2.0, yt + 0.3 * (yy / 0.95)), P(3.3, yt + yy)) for yy in FIB_YS], GREEN, 2.8)
        for m in [*self.ghost.values()]:
            m.set_z_index(1)
        for m in (self.h_trunk, self.h_fib, self.t_trunk, self.t_fib):
            m.set_z_index(2)

    def base(self):
        return [self.out, self.cells, self.glab, self.legend, self.tag, *self.rows.values(), *self.names.values(),
                *self.ghost.values()]


class S03(SpokenScene):
    def construct(self):
        big = s02_final()
        b = Body()
        self.add(big["out"], big["cells"], big["glab"], big["bax"], big["ngf"], big["xb"], big["xn"])
        self.play(Transform(big["out"], b.out), Transform(big["cells"], b.cells), Transform(big["glab"], b.glab),
                  FadeOut(VGroup(big["bax"], big["ngf"], big["xb"], big["xn"])), run_time=0.7)
        self.at("targets")
        self.play(LaggedStart(*[FadeIn(b.rows[k]) for k in ROW_Y], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(b.names[k], shift=LEFT * 0.15) for k in ROW_Y], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(b.ghost[k]) for k in ROW_Y], lag_ratio=0.2), run_time=0.5)
        self.at("at birth")
        self.play(FadeIn(b.tag, shift=DOWN * 0.1), FadeIn(b.legend), run_time=0.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        b = Body()
        self.add(*b.base())
        self.at("is missing")
        self.play(FadeIn(b.status["sal"], shift=LEFT * 0.1), run_time=0.5)
        self.at("some targets")
        self.play(Indicate(b.rows["sal"], color=GOLD, scale_factor=1.03), run_time=0.8)
        self.at("such as the salivary")
        self.play(Indicate(b.ghost["sal"], color=GOLD, scale_factor=1.0), Indicate(b.names["sal"], color=GOLD, scale_factor=1.1),
                  run_time=0.9)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        b = Body()
        self.add(*b.base(), b.status["sal"])
        self.at("greatly reduced")
        self.play(Create(b.h_trunk), run_time=0.4)
        self.play(LaggedStart(*[Create(f) for f in b.h_fib], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(b.status["heart"], shift=LEFT * 0.1), run_time=0.4)
        self.at("such as the heart")
        self.play(Indicate(b.names["heart"], color=GOLD, scale_factor=1.1), run_time=0.7)
        self.at("a few")
        self.play(LaggedStart(*[Create(t) for t in b.t_trunk], lag_ratio=0.2), run_time=0.6)
        self.play(LaggedStart(*[Create(f) for f in b.t_fib], lag_ratio=0.06), run_time=1.3)
        self.at("near normal")
        self.play(FadeIn(b.status["trach"], shift=LEFT * 0.1), Indicate(b.names["trach"], color=GOLD, scale_factor=1.1),
                  run_time=0.7)
        self.finish()


def body_full():
    b = Body()
    return b, [*b.base(), *b.status.values(), b.h_trunk, b.h_fib, b.t_trunk, b.t_fib]


class S06(SpokenScene):
    def construct(self):
        b, mobs = body_full()
        frame = VGroup(*mobs)
        self.add(frame)
        card = box(0.4, 0.0, 9.4, 4.2, GOLD, 0.0, 0.3, 3)
        card.set_fill(DARK, opacity=1.0).set_z_index(10)
        l1 = T("survival", 56, GREEN, font=TITLE_FONT).move_to(P(0.4, 1.2))
        l2 = T("does not mean", 34, GREY).move_to(P(0.4, 0.1))
        l3 = T("normal innervation", 56, TEXT, font=TITLE_FONT).move_to(P(0.4, -1.1))
        for t in (l1, l2, l3):
            t.set_z_index(11)
        self.play(FadeOut(frame), run_time=0.3)
        self.remove(frame)
        self.play(FadeIn(card), run_time=0.15)
        self.at("survival")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.5)
        self.at("does not mean")
        self.play(FadeIn(l2), run_time=0.4)
        self.at("normal")
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TBOX = (0.3, -0.2, 12.6, 6.4)
PC, PW, PH = (2.8, -0.2), 7.4, 5.4          # the NGF patch inside the target
TIPX = PC[0] - PW / 2                        # where the axons meet the patch


def target_box():
    return box(*TBOX, GREY, 0.1, 0.3, 3)


def patch_dots(n=22, seed=3, cx=3.0, cy=0.0, w=5.2, h=4.4, r=0.09):
    rng = np.random.RandomState(seed)
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y <= 1:
            pts.append(P(cx + x * w / 2, cy + y * h / 2))
    return VGroup(*[ngf_dot(p, r) for p in pts])


def patch_ellipse(op=0.08):
    return Ellipse(width=PW, height=PH, stroke_color=YELLOW, stroke_width=2, stroke_opacity=0.5,
                   fill_color=YELLOW, fill_opacity=op).move_to(P(*PC))


class S07(SpokenScene):
    def construct(self):
        tbox = target_box()
        tlab = T("target", 26, GREY).move_to(P(-5.1, 2.65))
        patch = patch_ellipse(0.06)
        dots = patch_dots(26, cx=PC[0], cy=PC[1], w=PW - 0.8, h=PH - 0.8, r=0.1)
        chp = chip("NGF", YELLOW, 32).move_to(P(5.5, 2.4))
        yA = PC[1]
        lv = tree(P(TIPX, yA), 0.0, 1.8, 4, [-0.5, 0.0, 0.5], [-0.4, 0.4], 0.82)
        axon = Line(P(-6.7, yA), P(TIPX, yA), color=GREEN, stroke_width=6)
        tip = dot(P(TIPX, yA), GREEN, 0.16)
        trunk = lines_of(lv[0], GREEN, 7)
        br = [lines_of(lv[1], GREEN, 6), lines_of(lv[2], GREEN, 5), lines_of(lv[3], GREEN, 4)]

        self.add(tbox, tlab, patch, axon, tip)
        self.at("NGF")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.02), FadeIn(chp), patch.animate.set_fill(YELLOW, 0.12),
                  run_time=0.6)
        self.play(Create(trunk[0]), run_time=0.55)
        self.at("grow")
        self.play(Create(br[0]), run_time=0.3)
        self.at("and branch")
        self.play(LaggedStart(Create(br[1]), Create(br[2]), lag_ratio=0.5), run_time=1.2)
        self.finish()


S08_Y = [1.9, -0.2, -2.3]
ZCX = 1.9


def s08_trees():
    return [tree(P(TIPX, y), 0.0, 2.2, 3, [-0.18, 0.18], [-0.2, 0.2], 0.84) for y in S08_Y]


def zone_dots(seed=5):
    rng = np.random.RandomState(seed)
    out = []
    for y in S08_Y:
        k = 0
        while k < 9:
            x, yy = rng.uniform(-1, 1), rng.uniform(-1, 1)
            if x * x + yy * yy <= 1:
                out.append(ngf_dot(P(ZCX + x * 3.4, y + yy * 0.85), 0.1))
                k += 1
    return VGroup(*out)


def s08_parts():
    d = {"box": target_box(), "patch": patch_ellipse(0.06)}
    lvs = s08_trees()
    d["axon"] = [Line(P(-6.7, y), P(TIPX, y), color=GREEN, stroke_width=5) for y in S08_Y]
    d["trunk"] = [lines_of(lv[0], GREEN, 7) for lv in lvs]
    d["b1"] = [lines_of(lv[1], GREEN, 6) for lv in lvs]
    d["b2"] = [lines_of(lv[2], GREEN, 5) for lv in lvs]
    d["terr"] = [Ellipse(width=7.4, height=2.0, stroke_width=0, fill_color=GREEN, fill_opacity=0.2).move_to(P(ZCX + 0.2, y)) for y in S08_Y]
    d["dots"] = zone_dots()
    d["chip"] = chip("NGF", YELLOW, 32).move_to(P(5.5, 2.5))
    return d


class S08(SpokenScene):
    def construct(self):
        d = s08_parts()
        tlab = T("target", 26, GREY).move_to(P(-5.1, 2.65))
        self.add(d["box"], tlab, d["patch"], *d["axon"])
        self.at("the factor that", lead=0.0)
        self.play(FadeIn(d["chip"]),
                  LaggedStart(*[FadeIn(x, scale=0.4) for x in d["dots"]], lag_ratio=0.02), run_time=0.9)
        self.at("who lives")
        self.play(*[Indicate(a, color=GOLD, scale_factor=1.0) for a in d["axon"]], run_time=0.6)
        self.at("also")
        self.play(Indicate(d["chip"], color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("helps decide")
        rng = np.random.RandomState(2)
        self.play(*[x.animate.shift(P(rng.uniform(-0.2, 0.2), rng.uniform(-0.15, 0.15))) for x in d["dots"]], run_time=0.8)
        self.at("each survivor covers", lead=0.0)
        self.play(*[Create(t) for t in d["trunk"]], run_time=0.5)
        self.play(*[Create(t) for t in d["b1"]], run_time=0.4)
        self.play(*[Create(t) for t in d["b2"]], run_time=0.4)
        self.play(*[FadeIn(t) for t in d["terr"]], run_time=0.8)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        d = s08_parts()
        tlab = T("target", 26, GREY).move_to(P(-5.1, 2.65))
        frame = VGroup(d["box"], tlab, d["patch"], *d["axon"], *d["trunk"], *d["b1"], *d["b2"], *d["terr"], d["dots"], d["chip"])
        self.add(frame)
        intro = T("the broader task is called", 36, GREY).move_to(P(0, 0.85))
        wa = T("systems", 72, TEXT, font=TITLE_FONT)
        wb = T("matching", 72, TEXT, font=TITLE_FONT)
        lab = VGroup(wa, wb).arrange(RIGHT, buff=0.4).move_to(P(0, -0.15))
        rule = Line(P(-4.6, -0.95), P(4.6, -0.95), color=GOLD, stroke_width=5)
        for t in (intro, wa, wb, rule):
            t.set_z_index(11)
        plate = box(0, 0.0, 11.4, 3.0, GOLD, 0.0, 0.3, 3).set_fill(DARK, opacity=1.0).set_z_index(10)
        self.play(FadeOut(frame), FadeIn(plate), run_time=0.4)
        self.remove(frame)
        self.play(FadeIn(intro), run_time=0.4)
        self.at("systems")
        self.play(FadeIn(wa, shift=UP * 0.15), run_time=0.4)
        self.at("matching")
        self.play(FadeIn(wb, shift=UP * 0.15), Create(rule), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
D10 = [("neurons", -4.1, 0.7), ("innervation", 4.1, 0.7), ("synapses", -4.1, -2.5), ("dendrites", 4.1, -2.5)]


class S10(SpokenScene):
    def construct(self):
        R = 1.7
        head = T("systems matching", 32, GOLD, font=TITLE_FONT).move_to(P(0, 3.45))
        dials = [Dial(x, y, R, GREY, 0.5, band=True) for _, x, y in D10]
        ticks = [VGroup(check(x - 0.62, y + R + 0.34, 0.15, GREEN, 5), T("matched", 24, GREEN).move_to(P(x + 0.25, y + R + 0.34)))
                 for _, x, y in D10]
        labs = [T(n, 30, TEXT).move_to(P(x, y - 0.5)) for n, x, y in D10]
        chp = chip("NGF", YELLOW, 40).move_to(P(0, -0.8))
        a1 = arr(P(-0.95, -0.5), P(-2.45, 0.55), YELLOW, 7, 0.28)
        a2 = arr(P(0.95, -0.5), P(2.45, 0.55), YELLOW, 7, 0.28)
        d3 = DashedLine(P(-0.9, -1.2), P(-2.5, -2.0), color=YELLOW, stroke_width=5, dash_length=0.18).add_tip(tip_length=0.25)
        d4 = DashedLine(P(0.9, -1.2), P(2.5, -2.0), color=YELLOW, stroke_width=5, dash_length=0.18).add_tip(tip_length=0.25)
        for dd in (d3, d4):
            dd.set_opacity(0.7)
        lab_some = T("NGF acts on several\nof these", 28, YELLOW, line_spacing=0.9).move_to(P(0, 1.8))
        lab_not = T("not shown here", 26, LGREY).move_to(P(0, -2.45))
        self.add(head)
        self.at("each target gets")
        self.play(LaggedStart(*[FadeIn(VGroup(d.all(), t)) for d, t in zip(dials, ticks)], lag_ratio=0.25), run_time=1.0)
        self.at("number of neurons")
        self.play(FadeIn(labs[0], shift=UP * 0.1), Indicate(dials[0].frame, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.at("amount of innervation")
        self.play(FadeIn(labs[1], shift=UP * 0.1), Indicate(dials[1].frame, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.at("synapses and dendrite")
        self.play(FadeIn(labs[2], shift=UP * 0.1), Indicate(dials[2].frame, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.at("dendrite shapes")
        self.play(FadeIn(labs[3], shift=UP * 0.1), Indicate(dials[3].frame, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.at("NGF acts on", lead=0.0)
        self.play(FadeIn(chp, scale=0.7), run_time=0.4)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.at("several")
        self.play(FadeIn(lab_some, shift=UP * 0.1), Create(d3), Create(d4), FadeIn(lab_not), run_time=0.7)
        self.play(Indicate(dials[0].frame, color=YELLOW, scale_factor=1.06), Indicate(dials[1].frame, color=YELLOW, scale_factor=1.06),
                  run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
MS_Y = [1.9, 0.95, 0.0, -0.95, -1.9]


def motor_system():
    cord = box(-4.8, 0.0, 1.7, 6.0, GREY, 0.12, 0.8, 3)
    somas = VGroup(*[soma(P(-4.5, y), BLUE, 0.3, 0.9) for y in MS_Y])
    musc = Ellipse(width=6.2, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(P(3.2, -0.1))
    axons = VGroup(*[Line(P(-4.2, y), P(0.6, -0.1 + y * 0.38), color=LGREY, stroke_width=3.5) for y in MS_Y])
    return cord, somas, axons, musc


class S11(SpokenScene):
    def construct(self):
        cord, somas, axons, musc = motor_system()
        cl = T("spinal cord", 26, GREY).move_to(P(-4.8, -3.45))
        ml = T("limb muscle", 28, GREY).move_to(P(3.2, -1.9))
        b1 = T("different system", 38, GOLD).move_to(P(-2.6, 3.4))
        b2 = T("different variable", 38, GOLD).move_to(P(2.6, 3.4))
        tag = T("chick embryo", 34, GOLD).move_to(P(0.2, 3.4))
        self.at("now a different system")
        self.play(FadeIn(cord), FadeIn(cl), FadeIn(musc), FadeIn(ml), FadeIn(b1, shift=DOWN * 0.1), run_time=0.8)
        self.at("different variable")
        self.play(FadeIn(b2, shift=DOWN * 0.1), run_time=0.5)
        self.at("chick motor neurons", lead=0.0)
        self.play(FadeOut(b1), FadeOut(b2), run_time=0.3)
        self.play(FadeIn(tag, shift=DOWN * 0.1), LaggedStart(*[FadeIn(s, scale=0.4) for s in somas], lag_ratio=0.12),
                  run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.1), run_time=0.3)
        self.at("muscle activity")
        pulses = [dot(a.get_start(), GOLD, 0.13) for a in axons]
        alab = T("activity (impulses)", 30, GOLD).move_to(P(-0.6, 2.7))
        self.add(*pulses)
        self.play(FadeIn(alab, shift=DOWN * 0.1), *[MoveAlongPath(p, a) for p, a in zip(pulses, axons)],
                  Indicate(musc, color=GOLD, scale_factor=1.08), run_time=0.9)
        self.play(*[FadeOut(p) for p in pulses], run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
RX = [-4.2, -1.4, 1.4, 4.2]


def junction():
    muscle = box(0, -2.55, 12.4, 1.8, GREY, 0.25, 0.25, 3)
    mlab = T("muscle", 30, TEXT).move_to(P(-4.9, -2.75))
    recs = []
    for x in RX:
        l = Rectangle(width=0.3, height=0.8, stroke_color=LGREY, stroke_width=2, fill_color=LGREY, fill_opacity=0.6).move_to(P(x - 0.4, -1.2))
        r = Rectangle(width=0.3, height=0.8, stroke_color=LGREY, stroke_width=2, fill_color=LGREY, fill_opacity=0.6).move_to(P(x + 0.4, -1.2))
        recs.append(VGroup(l, r))
    bulb = Ellipse(width=6.0, height=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25).move_to(P(0, 1.6))
    axon = Line(P(0, 2.35), P(0, 3.8), color=BLUE, stroke_width=8)
    nlab = T("nerve", 30, TEXT).move_to(P(0.5, 3.1), aligned_edge=LEFT)
    return muscle, mlab, VGroup(*recs), bulb, axon, nlab


class S12(SpokenScene):
    def construct(self):
        muscle, mlab, recs, bulb, axon, nlab = junction()
        clab = T("curare", 32, TEXT).move_to(P(5.55, 3.2))
        cur = [dot(P(5.2 + 0.7 * (i % 2), 2.4 - 0.5 * (i // 2)), TEXT, 0.22) for i in range(4)]
        alab = T("acetylcholine receptors", 30, TEXT).move_to(P(0, -0.15))
        al = [leader(P(-1.9, -0.38), P(-1.8, -0.75)), leader(P(1.9, -0.38), P(1.8, -0.75))]
        st_on = T("responds", 32, GOLD).move_to(P(1.5, -2.75))
        st_off = T("no response", 32, TEXT).move_to(P(1.5, -2.75))
        self.add(muscle, mlab, recs, bulb, axon, nlab)
        # baseline: the nerve fires and the muscle responds
        pulse = dot(P(0, 3.6), GOLD, 0.22)
        self.add(pulse)
        self.play(pulse.animate.move_to(P(0, 1.6)), run_time=0.25)
        sig = [arr(P(x * 0.9, 0.7), P(x, -0.45), GOLD, 5, 0.18) for x in RX]
        self.play(FadeOut(pulse), *[GrowArrow(s) for s in sig], muscle.animate.set_fill(GOLD, opacity=0.6), FadeIn(st_on), run_time=0.3)
        self.at("blocks")
        self.play(*[FadeOut(s) for s in sig], muscle.animate.set_fill(GREY, opacity=0.25), FadeOut(st_on),
                  FadeIn(clab), LaggedStart(*[FadeIn(c, scale=0.4) for c in cur], lag_ratio=0.1), run_time=0.5)
        self.at("the acetylcholine")
        # first drop to the cleft height at the far edge, then slide to its receptor
        self.play(*[Succession(c.animate.move_to(P(6.1 if x > 0 else -6.1, 0.1)), c.animate.move_to(P(x, -1.2)))
                    for c, x in zip(cur, RX)], run_time=1.0)
        self.at("receptors")
        cl2 = leader(P(5.35, -0.55), P(4.45, -1.05), TEXT)
        self.play(FadeIn(alab, shift=UP * 0.1), *[Create(x) for x in al], clab.animate.move_to(P(5.85, -0.25)), Create(cl2),
                  run_time=0.5)
        self.at("of muscle")
        self.play(Indicate(muscle, color=GREY, scale_factor=1.0), run_time=0.5)
        self.at("the muscle stops")
        self.play(FadeOut(alab), *[FadeOut(x) for x in al], run_time=0.2)
        pulse2 = dot(P(0, 3.6), GOLD, 0.22)
        self.add(pulse2)
        self.play(pulse2.animate.move_to(P(0, 1.6)), run_time=0.35)
        sig2 = [arr(P(x * 0.9, 0.7), P(x, -0.45), GOLD, 5, 0.18) for x in RX]
        self.play(FadeOut(pulse2), *[GrowArrow(s) for s in sig2], FadeIn(st_off), run_time=0.35)
        self.at("to its nerve")
        self.play(*[FadeOut(s) for s in sig2], Indicate(nlab, color=GOLD, scale_factor=1.1), run_time=0.6)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        n1 = T("Robert Pittman", 46, TEXT, font=TITLE_FONT).move_to(P(-6.5, 2.4), aligned_edge=LEFT)
        n2 = T("Ronald Oppenheim", 46, TEXT, font=TITLE_FONT).move_to(P(-6.5, 1.3), aligned_edge=LEFT)
        EC = P(3.2, 0.3)
        egg = Ellipse(width=4.4, height=4.6, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.1).move_to(EC)
        cc = EC + P(0, -0.1)
        curl = Arc(radius=1.05, start_angle=PI * 0.15, angle=PI * 1.5, arc_center=cc, stroke_color=LGREY, stroke_width=16)
        head = Circle(radius=0.48, stroke_color=LGREY, stroke_width=3, fill_color=LGREY, fill_opacity=0.5).move_to(
            cc + P(1.05 * np.cos(PI * 0.15), 1.05 * np.sin(PI * 0.15)))
        eye = dot(head.get_center() + P(0.15, 0.1), DARK, 0.07)
        embryo = VGroup(curl, head, eye)
        pip = Rectangle(width=0.45, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to(P(3.2, 3.4))
        tip = Polygon(P(2.98, 3.0), P(3.42, 3.0), P(3.2, 2.7), stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        pipette = VGroup(pip, tip)
        drop = dot(P(3.2, 2.6), TEXT, 0.18)
        clab = T("curare", 32, TEXT).move_to(P(1.6, 3.4))
        elab = T("chick embryo", 28, GREY).move_to(P(3.5, -2.55))
        TY = -3.1
        tl = Arrow(P(-6.4, TY), P(6.4, TY), buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        axl = T("embryonic days", 26, GREY).move_to(P(5.2, -3.58))
        WX0, WX1 = -4.4, 0.6
        cbar = Rectangle(width=WX1 - WX0, height=0.3, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9).move_to(P((WX0 + WX1) / 2, -2.5))
        cbl = T("curare", 26, TEXT).move_to(P(-5.6, -2.5))
        seg = Rectangle(width=WX1 - WX0, height=0.55, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.9).move_to(P((WX0 + WX1) / 2, TY))
        segl = T("motor neuron death", 26, DARK, weight=BOLD).move_to(seg)

        self.at("Robert Pittman")
        self.play(FadeIn(n1, shift=RIGHT * 0.2), FadeIn(egg), FadeIn(embryo), run_time=0.6)
        self.at("Ronald Oppenheim")
        self.play(FadeIn(n2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("gave")
        self.play(FadeIn(pipette), Create(tl), FadeIn(axl), run_time=0.6)
        self.at("curare to")
        self.add(drop)
        self.play(FadeIn(clab), drop.animate.move_to(P(3.2, 1.0)), GrowFromEdge(cbar, LEFT), FadeIn(cbl), run_time=0.7)
        self.at("chick embryos")
        self.play(FadeIn(elab), FadeOut(drop, scale=0.5), Indicate(cbar, color=GOLD, scale_factor=1.0), run_time=0.5)
        self.at("during the period")
        self.play(Indicate(cbar, color=GOLD, scale_factor=1.0), run_time=0.7)
        self.at("motor neuron death")
        self.play(FadeIn(seg), FadeIn(segl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
M14_Y = [0.6 + o for o in (-1.8, -0.9, 0.0, 0.9, 1.8)]
MUSC14 = P(3.9, 0.5)


def motor14():
    cord = box(-3.9, 0.6, 1.6, 5.2, GREY, 0.12, 0.8, 3)
    somas = VGroup(*[soma(P(-3.9, y), BLUE, 0.3, 0.9) for y in M14_Y])
    musc = Ellipse(width=5.4, height=2.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(MUSC14)
    axons = VGroup(*[Line(P(-3.6, y), P(1.45, 0.5 + (y - 0.6) * 0.3), color=LGREY, stroke_width=3.5) for y in M14_Y])
    labs = VGroup(T("spinal cord", 26, GREY).move_to(P(-3.9, 3.55)),
                  T("motor neurons", 26, TEXT).move_to(P(-1.2, 2.6)),
                  leader(P(-2.3, 2.6), P(-3.55, 2.42), LGREY, 2))
    return cord, somas, axons, musc, labs


def s14_dots():
    return [dot(MUSC14 + P(dx, dy), TEXT, 0.14) for dx, dy in [(-1.0, 0.35), (-0.3, -0.35), (0.4, 0.4), (1.0, -0.15), (0.2, 0.0)]]


def s14_question():
    more = chip("more death", RED, 44).move_to(P(-3.3, -3.05))
    less = chip("less death", GREEN, 44).move_to(P(3.3, -3.05))
    q = T("?", 100, GOLD, weight=BOLD).move_to(P(0, -3.05))
    return more, less, q


def s14_mlab():
    return T("muscle (curare = white dots)", 26, TEXT).move_to(P(3.9, -1.3))


class S14(SpokenScene):
    def construct(self):
        cord, somas, axons, musc, labs = motor14()
        more, less, q = s14_question()
        wlab = T("a winner", 26, GREEN).move_to(P(-1.6, 0.22))
        mlab = s14_mlab()
        cur = s14_dots()
        self.at("if active")
        self.play(FadeIn(VGroup(cord, somas, axons, musc, labs)), run_time=0.4)
        pulses = [dot(a.get_start(), GOLD, 0.12) for a in axons]
        self.add(*pulses)
        self.play(*[MoveAlongPath(p, a) for p, a in zip(pulses, axons)], run_time=0.5)
        self.play(*[FadeOut(p) for p in pulses], run_time=0.1)
        self.at("help an axon win")
        win = axons[2]
        self.play(win.animate.set_color(GREEN).set_stroke(width=7), to_state(somas[2], GREEN, 0.9), FadeIn(wlab), run_time=0.7)
        self.at("what should paralysis")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cur], lag_ratio=0.15), musc.animate.set_fill(GREY, opacity=0.08),
                  FadeIn(mlab), run_time=0.8)
        self.at("motor neuron death")
        self.play(FadeIn(more, shift=RIGHT * 0.2), FadeIn(less, shift=LEFT * 0.2), FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        cord, somas, axons, musc, labs = motor14()
        axons[2].set_color(GREEN).set_stroke(width=7)
        somas[2].set_stroke(GREEN, opacity=1.0).set_fill(GREEN, opacity=0.9)
        musc.set_fill(GREY, opacity=0.08)
        wlab = T("a winner", 26, GREEN).move_to(P(-1.6, 0.22))
        more, less, q = s14_question()
        guess = chip("Pause and predict", GOLD, 32).move_to(P(3.9, 3.4))
        self.add(cord, somas, axons, musc, labs, wlab, s14_mlab(), *s14_dots(), more, less, q, guess)
        self.finish()


# ---------------------------------------------------------------------------------------------
BAX, BW = -4.3, 2.4
BB = -2.7   # chart baseline


def bar(x, h, color, op=0.85):
    return Rectangle(width=BW, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(P(x, BB + h / 2))


def chart_axes():
    ax = VGroup(Line(P(-5.0, BB), P(5.0, BB), color=GREY, stroke_width=3), Line(P(-5.0, BB), P(-5.0, 3.1), color=GREY, stroke_width=3),
                *[Line(P(-5.0, BB + 1.4 * k), P(-4.82, BB + 1.4 * k), color=GREY, stroke_width=3) for k in range(1, 5)])
    yl = T("motor neurons alive", 26, GREY).rotate(PI / 2).move_to(P(-5.6, 0.2))
    return ax, yl


class S16(SpokenScene):
    def construct(self):
        ax, yl = chart_axes()
        ctl = bar(-2.2, 3.0, BLUE)
        cl = T("control", 30, TEXT).move_to(P(-2.2, BB - 0.45))
        tl = T("curare", 30, TEXT).move_to(P(2.8, BB - 0.45))
        exp = DashedVMobject(Rectangle(width=BW, height=1.8, stroke_color=RED, stroke_width=5).move_to(P(2.8, BB + 0.9)), num_dashes=40)
        el = T("expected", 28, RED).move_to(P(2.8, BB + 2.3))
        act = bar(2.8, 3.8, GREEN)
        sch = T("schematic, no counts", 26, GREY).move_to(P(3.6, 3.45))
        self.add(ax, yl, sch)
        self.at("you might expect")
        self.play(GrowFromEdge(ctl, DOWN), FadeIn(cl), FadeIn(tl), run_time=0.6)
        self.at("more death")
        self.play(Create(exp), FadeIn(el), run_time=0.7)
        self.at("instead")
        self.play(FadeOut(exp), FadeOut(el), GrowFromEdge(act, DOWN), run_time=1.6)
        self.play(Indicate(act, color=GREEN, scale_factor=1.04), run_time=0.6)
        self.finish()


CARD_Y = -0.1


def card_left():
    cd = box(-3.6, CARD_Y, 6.4, 6.0, GREY, 0.1, 0.3, 3)
    ic_n = soma(P(-5.75, 0.85), BLUE, 0.8)
    ic_a = Line(P(-4.95, 0.85), P(-3.2, 0.85), color=LGREY, stroke_width=6)
    ic_m = Ellipse(width=2.6, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(P(-1.95, 0.85))
    ps = [dot(P(-4.6 + 0.6 * i, 0.85), GOLD, 0.16) for i in range(3)]
    tx = T("active connections\nhelp an axon win", 32, TEXT, line_spacing=0.9).move_to(P(-3.6, -2.0))
    return cd, VGroup(ic_n, ic_a, ic_m, *ps), tx


def card_right(saved=True):
    cd = box(3.6, CARD_Y, 6.4, 6.0, GREY, 0.1, 0.3, 3)
    sy = [2.0, 1.2, 0.4, -0.4]
    ns = VGroup(*[soma(P(1.2, y), GREEN if saved else BLUE, 0.3) for y in sy])
    ax = VGroup(*[Line(P(1.5, y), P(4.1, 0.8 + (y - 0.8) * 0.4), color=LGREY, stroke_width=4.5) for y in sy])
    ic_m = Ellipse(width=2.6, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to(P(5.4, 0.8))
    cs = VGroup(*[dot(ic_m.get_center() + P(dx, dy), TEXT, 0.12) for dx, dy in [(-0.6, 0.2), (0.0, 0.45), (0.6, 0.15), (0.1, -0.4)]])
    cross = VGroup(Line(P(2.4, 1.3), P(3.2, 0.3), color=TEXT, stroke_width=10), Line(P(2.4, 0.3), P(3.2, 1.3), color=TEXT, stroke_width=10))
    cross.set_z_index(8)
    tx = T("silencing the connection\nsaved neurons", 32, TEXT, line_spacing=0.9).move_to(P(3.6, -2.0))
    return cd, VGroup(ns, ax, ic_m, cs), cross, tx


class S17(SpokenScene):
    def construct(self):
        lc, li, lt = card_left()
        rc, ri, cross, rt = card_right(False)
        ga = arr(P(-0.4, CARD_Y), P(-0.05, CARD_Y), GOLD, 7, 0.22)
        gb = arr(P(0.4, CARD_Y), P(0.05, CARD_Y), GOLD, 7, 0.22)
        clash = T("contradiction", 40, GOLD).move_to(P(0, 3.45))
        self.add(lc, li, lt)
        pulses = [li[3 + i] for i in range(3)]
        self.at("that looked")
        self.play(FadeIn(rc), FadeIn(ri), *[p.animate.shift(RIGHT * 1.3) for p in pulses], run_time=0.6)
        self.at("contradiction")
        self.play(GrowArrow(ga), GrowArrow(gb), FadeIn(clash, shift=UP * 0.1), run_time=0.7)
        self.at("silencing the connection")
        self.play(FadeIn(rt, shift=UP * 0.1), FadeIn(cross, scale=1.4), run_time=0.5)
        self.at("saved neurons")
        self.play(*[to_state(n, GREEN, 0.9) for n in ri[0]], Indicate(rt, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        card = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=10.6, height=3.2, stroke_color=GREY, stroke_width=4).move_to(P(0, 0.7)),
                              num_dashes=70)
        t1 = T("explanations", 60, TEXT, font=TITLE_FONT).move_to(P(0, 0.7))
        t2 = T("interpretations", 60, GOLD, font=TITLE_FONT).move_to(P(0, 0.7))
        hold = T("held loosely", 40, TEXT).move_to(P(0, -2.0))
        grp = VGroup(card, t1)
        self.at("the usual")
        self.play(Create(card), FadeIn(t1), run_time=0.8)
        self.at("interpretations")
        self.play(Transform(t1, t2), run_time=0.6)
        self.at("hold them loosely")
        self.play(FadeIn(hold, shift=UP * 0.1), run_time=0.4)
        self.play(Rotate(grp, 0.05), run_time=0.45)
        self.play(Rotate(grp, -0.1), run_time=0.45)
        self.play(Rotate(grp, 0.05), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX_ALL = [-4.5, -3.0, -1.5, 1.5, 3.0, 4.5]
MY = -2.35    # top surface of the muscle band


def bouton(x):
    c = Circle(radius=0.17, stroke_color=LGREY, stroke_width=2, fill_color=TEXT, fill_opacity=0.95).move_to(P(x, MY + 0.17))
    c.set_z_index(4)
    return c


def explain_parts():
    muscle = box(0, -3.0, 12.4, 1.3, GREY, 0.25, 0.25, 3)
    mlab = T("paralysed muscle", 28, TEXT).move_to(P(0, -3.05))
    R, CL, CR = P(0, 1.3), P(-2.2, -0.1), P(2.2, -0.1)
    stem = Line(P(0, 3.8), R, color=LGREY, stroke_width=6)
    base = VGroup(Line(R, CL, color=LGREY, stroke_width=4), Line(R, CR, color=LGREY, stroke_width=4),
                  Line(CL, P(-1.5, MY + 0.3), color=LGREY, stroke_width=3), Line(CR, P(1.5, MY + 0.3), color=LGREY, stroke_width=3))
    new = VGroup(*[DashedVMobject(Line(c, P(x, MY + 0.3), color=LGREY, stroke_width=3.5), num_dashes=14)
                   for c, x in [(CL, -3.0), (CL, -4.5), (CR, 3.0), (CR, 4.5)]])
    b_old = VGroup(bouton(-1.5), bouton(1.5))
    b_new = VGroup(bouton(-4.5), bouton(-3.0), bouton(3.0), bouton(4.5))
    return muscle, mlab, stem, base, new, b_old, b_new


class S19(SpokenScene):
    def construct(self):
        muscle, mlab, stem, base, new, b_old, b_new = explain_parts()
        tag = T("possible explanation", 34, GOLD).move_to(P(-3.9, 3.4))
        nb = T("new branches", 28, TEXT).move_to(P(-5.3, -0.5))
        nbl = leader(P(-4.05, -0.62), P(-3.4, -1.05))
        ns = T("new synapses", 28, TEXT).move_to(P(5.4, -0.95))
        nsl = leader(P(5.0, -1.2), P(4.65, -2.0))
        self.at("the most common")
        self.play(FadeIn(tag, shift=DOWN * 0.1), Create(stem), run_time=0.6)
        self.play(Create(base), FadeIn(b_old), run_time=0.9)
        self.at("muscle may")
        self.play(FadeIn(muscle), FadeIn(mlab), run_time=0.6)
        self.at("more nerve branching")
        self.play(LaggedStart(*[Create(n) for n in new], lag_ratio=0.2), FadeIn(nb), Create(nbl), run_time=1.0)
        self.at("and more synapses")
        self.play(LaggedStart(*[FadeIn(b, scale=0.3) for b in b_new], lag_ratio=0.15), run_time=0.7)
        self.play(FadeIn(ns, shift=UP * 0.1), Create(nsl), run_time=0.4)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        muscle, mlab, stem, base, new, b_old, b_new = explain_parts()
        tag = T("possible explanation", 34, GOLD).move_to(P(-3.9, 3.4))
        nb = T("new branches", 28, TEXT).move_to(P(-5.3, -0.5))
        nbl = leader(P(-4.05, -0.62), P(-3.4, -1.05))
        ns = T("new synapses", 28, TEXT).move_to(P(5.4, -0.95))
        nsl = leader(P(5.0, -1.2), P(4.65, -2.0))
        self.add(muscle, mlab, stem, base, new, b_old, b_new, tag, nb, nbl, ns, nsl)
        bx = BX_ALL
        near = [dot(P(x, -0.55 - 0.15 * (i % 2)), TEXT, 0.13) for i, x in enumerate(bx)]
        far = [dot(P(x, -1.0), TEXT, 0.13) for x in [-3.75, -2.25, 0.0, 2.25, 3.75]]
        lab = T("trophic support", 30, TEXT).move_to(P(-5.0, 0.55))
        ll = leader(P(-4.6, 0.3), P(-4.5, -0.4))
        self.at("give each motor")
        self.play(FadeOut(nb), FadeOut(nbl), FadeOut(ns), FadeOut(nsl),
                  LaggedStart(*[FadeIn(d, scale=0.4) for d in near + far], lag_ratio=0.05), FadeIn(lab), Create(ll), run_time=0.8)
        self.at("more access")
        self.play(*[d.animate.move_to(P(x, MY + 0.55)) for d, x in zip(near, bx)], FadeOut(ll), run_time=0.9)
        self.at("trophic support")
        self.play(*[Indicate(d, color=GOLD, scale_factor=1.5) for d in near], run_time=0.8)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        pos = [P(-3.0, 0.4), P(0.0, -0.7), P(3.0, 0.4)]
        ns = VGroup(*[soma(p, BLUE, 0.85, 0.85) for p in pos])
        nchip = chip("NGF", YELLOW, 48, pad=0.26, fill_opacity=0.3).move_to(P(0, 2.8))
        x = strike(nchip, TEXT, 10)
        rng = np.random.RandomState(8)
        dots = []
        for i in range(16):
            ang = rng.uniform(0, 2 * PI)
            rad = rng.uniform(4.3, 5.4)
            p = P(rad * np.cos(ang) * 1.15, 0.0 + rad * np.sin(ang) * 0.62 - 0.2)
            p[0] = float(np.clip(p[0], -6.3, 6.3)); p[1] = float(np.clip(p[1], -3.3, 3.5))
            if abs(p[0]) < 1.8 and p[1] > 2.0:
                p[1] = 1.5
            dots.append(dot(p, OTHER[i % 4], 0.14))
        lab = T("several factors", 32, TEXT).move_to(P(0, -3.35))
        self.at("note that chick")
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in ns], lag_ratio=0.2), run_time=0.9)
        self.at("do not depend")
        self.play(FadeIn(nchip, scale=0.7), run_time=0.5)
        self.play(Create(x), run_time=0.4)
        self.at("they draw on")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.03), run_time=0.7)
        self.at("several factors")
        tgt = []
        for i, d in enumerate(dots):
            c = min(pos, key=lambda q: np.linalg.norm(q - d.get_center()))
            v = c - d.get_center()
            v = v / np.linalg.norm(v)
            tgt.append(d.animate.move_to(c - v * 1.15))
        self.play(*tgt, FadeIn(lab, shift=UP * 0.1), run_time=1.4)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        tag = T("other systems", 34, TEXT).move_to(P(-4.4, 3.45))
        pre = Ellipse(width=4.8, height=4.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(P(-3.7, 0.2))
        post = Ellipse(width=4.8, height=4.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to(P(3.7, 0.2))
        prl = T("active neuron", 30, TEXT).move_to(P(-3.7, -2.55))
        pol = T("target", 30, TEXT).move_to(P(3.7, -2.55))
        pl = T("active synapse", 28, GOLD).move_to(P(0, -2.9))
        pll = leader(P(0, -2.6), P(0, -0.6), GOLD, 2.5)
        ves = [dot(P(-3.2 + 0.55 * (i % 2), -0.5 + 0.7 * (i // 2)), ORANGE, 0.16) for i in range(4)]
        bdnf = chip("BDNF", ORANGE, 36).move_to(P(0, 1.6))
        self.at("in other systems")
        self.play(FadeIn(tag, shift=RIGHT * 0.1), FadeIn(pre), FadeIn(post), FadeIn(prl), FadeIn(pol), run_time=0.8)
        self.at("activity")
        self.play(Indicate(pre, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("winner")
        self.play(pre.animate.set_stroke(GREEN, opacity=1.0).set_fill(GREEN, opacity=0.3), run_time=0.7)
        self.at("active")
        self.play(FadeIn(pl, shift=UP * 0.1), Create(pll), FadeIn(bdnf, shift=DOWN * 0.1),
                  LaggedStart(*[FadeIn(v, scale=0.4) for v in ves], lag_ratio=0.1), run_time=0.8)
        self.at("release more")
        outs = [v.animate.move_to(P(-0.6 + 0.4 * i, 0.4 - 0.5 * (i % 2))) for i, v in enumerate(ves)]
        self.play(*outs, run_time=0.7)
        self.at("BDNF")
        self.play(Indicate(bdnf, color=ORANGE, scale_factor=1.15), *[v.animate.shift(RIGHT * 2.2) for v in ves], run_time=0.9)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        R = 2.6
        dm = Dial(-3.7, -0.4, R, GREY, 0.5, sw=7)
        dn = Dial(3.7, -0.4, R, BLUE, 0.5, sw=7)
        lm = T("muscle activity", 38, TEXT).move_to(P(-3.7, -1.85))
        ln = T("neuron activity", 38, BLUE).move_to(P(3.7, -1.85))
        marks = []
        for cx in (-3.7, 3.7):
            marks += [T("low", 28, LGREY).move_to(P(cx - R, -0.78)), T("high", 28, LGREY).move_to(P(cx + R, -0.78))]
        div = DashedLine(P(0, 2.6), P(0, -2.4), color=GOLD, stroke_width=4)
        no = T("need not conflict", 44, GOLD).move_to(P(0, -3.0))
        self.at("activity in the muscle")
        self.play(FadeIn(dm.all()), FadeIn(dn.all()), FadeIn(lm), FadeIn(ln), *[FadeIn(m) for m in marks], run_time=0.8)
        self.at("competing neurons")
        self.play(Indicate(dn.frame, color=BLUE, scale_factor=1.03), run_time=0.7)
        self.at("different variables")
        self.play(Create(div), dm.sweep(0.1), run_time=0.8)
        self.play(dm.sweep(0.5), run_time=0.5)
        self.play(dn.sweep(0.9), run_time=0.8)
        self.play(dn.sweep(0.5), run_time=0.5)
        self.at("need not conflict")
        self.play(FadeIn(no, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rule_panel():
    d = {}
    d["head"] = T("The rule", 42, GOLD, font=TITLE_FONT).move_to(P(0, 3.45))
    d["pl"] = box(-3.5, 0.0, 6.8, 5.6, GREY, 0.05, 0.3, 2)
    d["pr"] = box(3.6, 0.0, 6.8, 5.6, GREY, 0.05, 0.3, 2)
    d["tb"] = box(-3.5, 1.7, 6.0, 1.7, GREY, 0.14, 0.2)
    d["tl"] = T("target", 34, TEXT).move_to(P(-3.5, 2.2))
    d["dts"] = VGroup(*[ngf_dot(P(-3.5 + dx, 1.4), 0.17) for dx in (-1.1, -0.37, 0.37, 1.1)])
    xs = np.linspace(-6.0, -1.0, 8)
    d["row"] = VGroup(*[soma(P(x, -0.3), BLUE, 0.35) for x in xs])
    d["cap1"] = T("The target sets\nhow many.", 40, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to(P(-3.5, -1.95))
    d["big"] = soma(P(3.6, 0.55), BLUE, 0.85, 0.9)
    d["nl"] = T("each neuron", 30, GREY).move_to(P(3.6, 2.35))
    loop = Arc(radius=1.45, start_angle=PI * 0.3, angle=PI * 1.5, arc_center=P(3.6, 0.55), stroke_color=PURPLE, stroke_width=9)
    loop.add_tip(tip_length=0.32)
    d["loop"] = loop
    d["cap2"] = T("The neurons\ndecide which.", 40, GREEN, font=TITLE_FONT, line_spacing=0.9).move_to(P(3.6, -1.95))
    d["keep"] = [0, 2, 5, 7]
    return d


class S24(SpokenScene):
    def construct(self):
        d = rule_panel()
        self.add(d["pl"], d["pr"], d["tb"], d["tl"], d["row"], d["big"], d["nl"])
        self.play(FadeIn(d["head"], shift=DOWN * 0.15), run_time=0.5)
        self.at("the target sets")
        self.play(FadeIn(d["cap1"], shift=UP * 0.1), LaggedStart(*[FadeIn(x, scale=0.3) for x in d["dts"]], lag_ratio=0.2), run_time=0.8)
        self.at("how many")
        self.play(Indicate(d["dts"], color=GOLD, scale_factor=1.25), run_time=0.8)
        self.at("the neurons decide")
        self.play(Create(d["loop"]), FadeIn(d["cap2"], shift=UP * 0.1), run_time=0.9)
        self.at("which")
        self.play(*[to_state(d["row"][i], GREEN, 0.9) if i in d["keep"] else to_state(d["row"][i], RED, 0.3) for i in range(8)],
                  to_state(d["big"], GREEN, 0.9), Indicate(d["cap2"], color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


def rule_final_group():
    d = rule_panel()
    for i in range(8):
        if i in d["keep"]:
            d["row"][i].set_stroke(GREEN, opacity=1.0).set_fill(GREEN, opacity=0.9)
        else:
            d["row"][i].set_stroke(RED, opacity=0.6).set_fill(RED, opacity=0.3)
    d["big"].set_stroke(GREEN, opacity=1.0).set_fill(GREEN, opacity=0.9)
    return VGroup(d["pl"], d["pr"], d["tb"], d["tl"], d["dts"], d["row"], d["cap1"], d["big"], d["nl"], d["loop"], d["cap2"])


class S25(SpokenScene):
    def construct(self):
        C = P(-1.9, 0.0)
        RN, RR = 1.4, 2.5
        tag = T("published model", 32, GOLD).move_to(P(4.3, 3.4))
        n = soma(C, BLUE, RN, 0.85)
        nchip = chip("NGF", YELLOW, 44).move_to(P(3.6, 0.0))
        dts = VGroup(*[ngf_dot(P(2.5, 0.55 - 0.55 * i), 0.15) for i in range(3)])
        top = Arc(radius=RR, start_angle=0, angle=PI, arc_center=C, stroke_color=PURPLE, stroke_width=11)
        top.add_tip(tip_length=0.34)
        bot = Arc(radius=RR, start_angle=PI, angle=PI, arc_center=C, stroke_color=PINK, stroke_width=11)
        bot.add_tip(tip_length=0.34)
        tl = T("TrkA level", 36, PURPLE).move_to(P(-1.9, 3.15))
        bl = T("signal duration", 36, PINK).move_to(P(-1.9, -3.15))
        self.add(tag, n, nchip, dts)
        self.at("grows", lead=0.0)
        self.play(n.animate.scale(1.2), to_state(n, GREEN, 0.9), run_time=0.5)
        self.at("because NGF")
        self.play(Indicate(nchip, color=YELLOW, scale_factor=1.1), run_time=0.4)
        surf = [C + (RN * 1.2) * np.array([np.cos(a), np.sin(a), 0.0]) + RIGHT * 0.1 for a in (0.3, 0.0, -0.3)]
        self.play(*[d.animate.move_to(s) for d, s in zip(dts, surf)], run_time=0.6)
        self.at("raises track a")
        self.play(Create(top), FadeIn(tl, shift=DOWN * 0.1), run_time=0.8)
        self.at("lengthens its signal")
        self.play(Create(bot), FadeIn(bl, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        WC, LC = P(-3.9, 0.5), P(3.9, 0.5)
        RN = 1.45
        tag = T("proposed model", 32, GOLD).move_to(P(0, 3.4))
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GREEN, fill_opacity=o).move_to(WC) for r, o in ((2.1, 0.10), (1.8, 0.18))])
        winner = soma(WC, GREEN, RN, 0.9)
        loser = soma(LC, BLUE, RN, 0.9)
        rec = RoundedRectangle(corner_radius=0.08, width=0.4, height=1.4, stroke_color=TEXT, stroke_width=4, fill_color="#2FE0E8",
                               fill_opacity=1.0).move_to(P(LC[0] - RN - 0.28, 0.5))
        rec.set_z_index(6)
        rl = T("p75", 36, "#2FE0E8", weight=BOLD).move_to(P(LC[0] - RN - 0.45, 1.5))
        arrow = arr(P(WC[0] + RN + 0.2, 0.5), P(LC[0] - RN - 0.6, 0.5), ORANGE, 9, 0.3)
        al = T("punishment", 32, ORANGE).move_to(P(0, 1.2))
        at = T("BDNF, NT-4", 28, ORANGE).move_to(P(0, -0.2))
        bw = 2.6
        wbar = Rectangle(width=bw, height=0.28, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.9).move_to(P(WC[0], -1.75))
        lbar = Rectangle(width=bw, height=0.28, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.9).move_to(P(LC[0], -1.75))
        wl = T("time left", 26, LGREY).move_to(P(WC[0], -2.3))
        ll = T("time left", 26, LGREY).move_to(P(LC[0], -2.3))
        wbar2 = Rectangle(width=bw * 0.7, height=0.28, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.9).move_to(
            P(WC[0] - bw / 2 + bw * 0.35, -1.75))
        lbar2 = Rectangle(width=bw * 0.12, height=0.28, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.9).move_to(
            P(LC[0] - bw / 2 + bw * 0.06, -1.75))
        self.add(tag)
        self.play(FadeIn(glow), FadeIn(winner, scale=0.7), FadeIn(loser, scale=0.7), GrowArrow(arrow), FadeIn(al), FadeIn(at),
                  FadeIn(wbar), FadeIn(lbar), FadeIn(wl), FadeIn(ll), run_time=0.5)
        self.at("through p 75")
        self.play(FadeIn(rec, shift=LEFT * 0.2), FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)
        self.play(Indicate(rec, color="#2FE0E8", scale_factor=1.25), run_time=0.5)
        self.at("die sooner")
        self.play(to_state(loser, RED, 0.2), to_state(winner, GREEN, 0.7),
                  Transform(lbar, lbar2), Transform(wbar, wbar2), run_time=1.3)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        panel = rule_final_group()
        panel.scale_to_fit_width(8.6).move_to(P(-2.3, 0.35))
        frame = box(-2.3, 0.3, 9.0, 4.9, GOLD, 0.0, 0.3, 3)
        scope = chip("mouse sympathetic neurons", GREEN, 28).move_to(P(-2.3, -2.95))
        rc = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=3.9, height=4.9, stroke_color=GREY, stroke_width=4).move_to(P(4.75, 0.3)),
                            num_dashes=60)
        r1 = T("chick motor\nneurons", 34, TEXT, line_spacing=0.9).move_to(P(4.75, 1.0))
        r2 = T("need their\nown account", 32, GOLD, line_spacing=0.9).move_to(P(4.75, -0.9))
        self.at("the rule is scoped")
        self.play(FadeIn(panel), Create(frame), run_time=0.8)
        self.at("to mouse sympathetic")
        self.play(FadeIn(scope, shift=UP * 0.1), run_time=0.6)
        self.at("chick motor neurons", lead=0.0)
        self.play(Create(rc), FadeIn(r1), run_time=0.7)
        self.at("need their own")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.finish()


def take_card(cx, cy, text, color, dashed=False):
    w, h = 6.3, 2.95
    if dashed:
        cd = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to(P(cx, cy)), num_dashes=50)
    else:
        cd = box(cx, cy, w, h, color, 0.08, 0.25, 3)
    tx = T(text, 28, color if color != GREY else LGREY, line_spacing=0.9).move_to(P(cx, cy - 0.5))
    return cd, tx


class S28(SpokenScene):
    def construct(self):
        head = T("Takeaway", 42, GOLD, font=TITLE_FONT).move_to(P(0, 3.4))
        XL, XR, YT, YB = -3.3, 3.3, 1.35, -1.8
        c1, t1 = take_card(XL, YT, "NGF supply sets how many\nsympathetic neurons survive.", TEXT)
        c2, t2 = take_card(XR, YT, "The neurons' own feedback\ndecides which.", GREEN)
        c3, t3 = take_card(XL, YB, "NGF also shapes how much of\nmany targets they cover.", TEXT)
        c4, t4 = take_card(XR, YB, "Muscle activity is a different\nvariable, in a different system.", GREY, True)
        # icons (top part of each card)
        kept = (0, 2, 4)
        i1 = VGroup(*[soma(P(XL - 1.0 + 0.5 * k, YT + 0.78), BLUE, 0.2, 0.9) for k in range(5)])
        i2 = VGroup(soma(P(XR, YT + 0.78), GREEN, 0.35, 0.9),
                    Arc(radius=0.62, start_angle=PI * 0.3, angle=PI * 1.5, arc_center=P(XR, YT + 0.78), stroke_color=PURPLE, stroke_width=5))
        i3b = box(XL, YB + 0.78, 2.6, 0.9, GREY, 0.12, 0.15, 2)
        i3f = lines_of([(P(XL - 1.3, YB + 0.78), P(XL + 0.6, YB + 1.08)), (P(XL - 1.3, YB + 0.78), P(XL + 1.1, YB + 0.78)),
                        (P(XL - 1.3, YB + 0.78), P(XL + 0.6, YB + 0.48))], GREEN, 3.5)
        i4 = Ellipse(width=1.8, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(P(XR, YB + 0.78))
        self.at("takeaway", lead=0.0)
        self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(c1), FadeIn(i1), FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("survive", lead=0.0)
        self.play(*[to_state(i1[k], GREEN, 0.9) if k in kept else to_state(i1[k], RED, 0.3) for k in range(5)], run_time=0.6)
        self.at("own feedback", lead=0.0)
        self.play(FadeIn(c2), FadeIn(i2), FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.at("and NGF also", lead=0.0)
        self.play(FadeIn(c3), FadeIn(i3b), FadeIn(t3, shift=UP * 0.1), run_time=0.8)
        self.at("cover", lead=0.0)
        self.play(LaggedStart(*[Create(f) for f in i3f], lag_ratio=0.2), run_time=0.6)
        self.at("muscle activity", lead=0.0)
        self.play(Create(c4), FadeIn(i4), FadeIn(t4, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S29End(EndCard):
    LINE = "In mouse sympathetic neurons, NGF supply sets how many; feedback decides which."

    def construct(self):
        l1 = T("In mouse sympathetic neurons, NGF supply sets how many;", 38, TEXT, font=TITLE_FONT)
        l2 = T("feedback decides which.", 38, TEXT, font=TITLE_FONT)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(l1, l2, sub).arrange(DOWN, buff=0.35, center=True)
        fit(g, max_w=12.0)
        g.move_to(ORIGIN)
        self.play(FadeIn(VGroup(l1, l2), shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
