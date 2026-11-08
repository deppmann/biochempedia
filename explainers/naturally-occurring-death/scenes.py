"""Too Many, Then Fewer: chapter 1 of "Too Many Neurons: Naturally Occurring Cell Death" (Biochemistrypedia).

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film series; taken from the lesson's earlier single film)
  BLUE   = motor neurons that are present / healthy (dots, the column outline, "kept" counts)
  RED    = dying or lost neurons, the loss
  YELLOW = the limb and the target (the leg block, its support glow, the legs of the chick)
  GREY   = axes, outlines, axons, phagocytes, de-emphasized things and the questions
  TEXT   = headings and the rule itself
One dot = about 500 neurons (40 dots = the peak count, 24 dots = what is left).
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

GHOST = 0.30          # opacity of a lost neuron that is still shown as a trace
RX = 4.3              # x of the right-hand column of count cards
CAPC = "#BCC3CF"      # brighter grey for captions (readable at phone width)


def cap(text, size=28, color=CAPC, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def chip2(text, color, size=32, pad=0.2, fill_opacity=0.16, text_color=TEXT):
    """chip with a coloured box and bright text."""
    label = T(text, size=size, color=text_color)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill_opacity)
    return VGroup(box, label.move_to(box))


# ---- the 40 dots (the leg column at its peak) and which 16 are lost -------------------------------
def _unit_pts(n=40):
    ga = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        r = 0.88 * math.sqrt((i + 0.5) / n)
        out.append((r * math.cos(i * ga), r * math.sin(i * ga)))
    return out


UNIT = _unit_pts()
DYING = sorted(random.Random(11).sample(range(40), 16))
KEPT = [i for i in range(40) if i not in DYING]


def make_field(cx, cy, A, B, r):
    outline = Ellipse(width=2 * A, height=2 * B, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                      fill_opacity=0.07).move_to([cx, cy, 0])
    dots = VGroup(*[Dot([cx + A * u, cy + B * v, 0], radius=r, color=BLUE) for u, v in UNIT])
    return outline, dots


# ---- count cards on the right ----------------------------------------------------------------------
C1Y, C2Y = 1.7, -0.95
FX, FY, FA, FB, FR = -3.2, 0.1, 2.8, 3.0, 0.25     # the field in the counting scenes


def card(y, label, color=BLUE):
    box = RoundedRectangle(corner_radius=0.2, width=3.9, height=2.5, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08).move_to([RX, y, 0])
    lab = cap(label, 28).move_to([RX, y + 0.88, 0])
    return VGroup(box, lab)


def qmark(y, color=TEXT):
    return T("?", 80, color, weight=BOLD).move_to([RX, y - 0.2, 0])


def numval(y, top, num):
    a = cap(top, 28).move_to([RX, y + 0.2, 0])
    b = T(num, 60, BLUE, weight=BOLD).move_to([RX, y - 0.5, 0])
    return VGroup(a, b)


def day_counter(vt):
    return always_redraw(lambda: T(f"day {int(round(vt.get_value()))}", 48, TEXT, weight=BOLD).move_to([RX, 3.4, 0]))


def key_label():
    return cap("1 dot = about 500 neurons", 28).move_to([FX, -3.45, 0])


def credit():
    return T("Viktor Hamburger, 1975", 30, TEXT).move_to([RX, -2.68, 0])


def raw_chip():
    return chip2("raw counts, approximate", BLUE, size=28, pad=0.13).move_to([RX, -3.38, 0])


# ---- the spinal cord cross-section (schematic) ---------------------------------------------------------
CORD_C, CORD_S = (-3.0, 0.0), 1.05


def cord(cx, cy, s):
    outer = Ellipse(width=6.6 * s, height=5.8 * s, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                    fill_opacity=0.08).move_to([cx, cy, 0])
    R = [(0, .45), (.45, .7), (.65, 1.5), (1.0, 1.85), (1.3, 1.5), (1.2, .8), (1.7, .55), (2.4, .45), (2.6, -.2),
         (2.5, -1.0), (1.9, -1.7), (1.1, -1.55), (.6, -.9), (0, -.7)]
    pts = R + [(-x, y) for x, y in reversed(R[1:-1])]
    P = [[cx + x * s, cy + y * s, 0] for x, y in pts]
    gray = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.28)
    gray.set_points_smoothly(P + [P[0]])
    # the leg column sits fully inside the right ventral horn
    lmc = Ellipse(width=1.05 * s, height=1.2 * s, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                  fill_opacity=0.18).move_to([cx + 1.85 * s, cy - 0.85 * s, 0])
    return outer, gray, lmc


def cord_set():
    outer, gray, lmc = cord(*CORD_C, CORD_S)
    cp = cap("lumbar spinal cord, cross-section", 28).move_to([CORD_C[0], -3.5, 0])
    lab = T("leg column", 34, BLUE, weight=BOLD).move_to([1.9, -2.85, 0])
    la = arr(lab.get_left(), lmc.get_center() + RIGHT * 0.3 + DOWN * 0.3, BLUE, 4)
    return outer, gray, lmc, cp, lab, la


# ---- schematic plot frame ---------------------------------------------------------------------------
class Plot:
    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h

    def P(self, u, v):
        return np.array([self.x0 + u * self.w, self.y0 + v * self.h, 0.0])

    def curve(self, fn, u0, u1, color, w=6, n=70):
        pts = [self.P(u, fn(u)) for u in np.linspace(u0, u1, n)]
        return VMobject(stroke_color=color, stroke_width=w, fill_opacity=0).set_points_as_corners(pts)


# ---- phagocyte blob ---------------------------------------------------------------------------------
def blob(cx, cy, R, seed):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(2)]
    pts = []
    for k in range(24):
        th = 2 * math.pi * k / 24
        rr = R * (1 + 0.12 * math.sin(3 * th + ph[0]) + 0.08 * math.sin(5 * th + ph[1]))
        pts.append([cx + rr * math.cos(th), cy + rr * math.sin(th), 0])
    m = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4)
    m.set_points_smoothly(pts + [pts[0]])
    return m


# ---- the chick ----------------------------------------------------------------------------------------
def chick(x, y, t=0.0, walk=False, s=1.0):
    body = Ellipse(width=2.3 * s, height=1.8 * s, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                   fill_opacity=0.28).move_to([x, y, 0])
    head = Circle(radius=0.55 * s, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                  fill_opacity=0.28).move_to([x + 0.95 * s, y + 0.85 * s, 0])
    beak = Polygon([x + 1.45 * s, y + 0.95 * s, 0], [x + 1.95 * s, y + 0.8 * s, 0], [x + 1.45 * s, y + 0.65 * s, 0],
                   stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.6)
    eye = Dot([x + 1.12 * s, y + 0.98 * s, 0], radius=0.07 * s, color=TEXT)
    legs = VGroup()
    for hx, ph in ((x - 0.15 * s, 0.0), (x + 0.3 * s, math.pi)):
        ang = 2 * math.pi * t + ph
        sw = 0.38 * s * math.sin(ang) if walk else 0.0
        lift = 0.2 * s * max(0.0, math.cos(ang)) if walk else 0.0
        hip = [hx, y - 0.8 * s, 0]
        foot = [hx + sw, y - 1.65 * s + lift, 0]
        legs.add(Line(hip, foot, color=YELLOW, stroke_width=9))
        for dx, dy in ((0.32, 0.0), (0.26, 0.12), (0.26, -0.1)):
            legs.add(Line(foot, [foot[0] + dx * s, foot[1] + dy * s, 0], color=YELLOW, stroke_width=7))
    return VGroup(VGroup(body, head, beak, eye), legs)


def egg_parts(cx, cy):
    """whole egg, and the two shell halves cut along one zigzag crack."""
    W, H = 5.4, 6.5
    egg = Ellipse(width=W, height=H, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])
    zig = []
    xs = np.linspace(-3.0, 3.0, 12)
    for k, xx in enumerate(xs):
        zig.append([cx + xx, cy + 0.9 + (0.28 if k % 2 else -0.28), 0])
    top_poly = Polygon(*(zig + [[cx + 3.0, cy + 4, 0], [cx - 3.0, cy + 4, 0]]), stroke_width=0, fill_opacity=1)
    bot_poly = Polygon(*(zig + [[cx + 3.0, cy - 4, 0], [cx - 3.0, cy - 4, 0]]), stroke_width=0, fill_opacity=1)
    top = Intersection(egg, top_poly, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06)
    bot = Intersection(egg, bot_poly, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06)
    return egg, top, bot


# ---- the target block (s11) ---------------------------------------------------------------------------
BX, BW, BH = 4.4, 2.8, 5.8


def glow_rings():
    g = VGroup()
    for k, op in ((1, 0.16), (2, 0.10), (3, 0.05)):
        g.add(RoundedRectangle(corner_radius=0.3, width=BW + 0.22 * k, height=BH + 0.22 * k, stroke_width=0,
                               fill_color=YELLOW, fill_opacity=op).move_to([BX, 0, 0]))
    return g


def make_axons(dots):
    order = sorted(range(40), key=lambda i: -dots[i].get_center()[1])
    ty = {i: 2.4 - 4.8 * k / 39 for k, i in enumerate(order)}
    axons = []
    for i in range(40):
        p0 = dots[i].get_center()
        p3 = np.array([BX - BW / 2, ty[i], 0.0])
        p1 = p0 + np.array([1.9, 0, 0])
        p2 = p3 + np.array([-1.9, 0, 0])
        axons.append(CubicBezier(p0, p1, p2, p3, stroke_color=GREY, stroke_width=2.5, stroke_opacity=0.65))
    contacts = VGroup(*[Dot([BX - BW / 2, ty[i], 0], radius=0.07, color=YELLOW) for i in range(40)])
    return axons, contacts


def headline(text, y=3.25, size=44):
    return T(text, size, TEXT, font=TITLE_FONT).move_to([0, y, 0])


# =====================================================================================================
class S00Title(TitleCard):
    LESSON = "Too Many Neurons: Naturally Occurring Cell Death"
    TITLE = "Too Many, Then Fewer"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=24, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=26, color=CAPC)
        title = T(self.TITLE, size=66, font=TITLE_FONT)
        fit(title, max_w=11.8)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=5)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.4)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(title, shift=UP * 0.15), GrowFromCenter(rule), run_time=0.7)
        self.wait(1.6)                      # the full title and rule are held for 1.6 s
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        outer, gray, lmc, cp, lab, la = cord_set()
        c1, q1 = card(C1Y, "at the peak"), qmark(C1Y)
        c2, q2 = card(C2Y, "left afterwards"), qmark(C2Y)

        self.play(Create(outer), FadeIn(cp), FadeIn(c1), FadeIn(c2), run_time=0.45)
        self.at("motor neurons")
        self.play(FadeIn(gray), run_time=0.8)
        self.at("leg column")
        self.play(Create(lmc), FadeIn(lab), run_time=0.6)
        self.play(GrowArrow(la), run_time=0.3)
        self.at("at the peak")
        self.play(FadeIn(q1, scale=0.6), Indicate(c1, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.at("and how many")
        self.play(FadeIn(q2, scale=0.6), Indicate(c2, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S02Peak(SpokenScene):
    def construct(self):
        outer, gray, lmc, cp, lab, la = cord_set()
        c1, q1 = card(C1Y, "at the peak"), qmark(C1Y)
        c2, q2 = card(C2Y, "left afterwards"), qmark(C2Y)
        self.add(outer, gray, lmc, cp, lab, la, c1, q1, c2, q2)

        outline, dots = make_field(FX, FY, FA, FB, FR)
        vt = ValueTracker(4)
        ctr = day_counter(vt)
        key = key_label()
        val = numval(C1Y, "just over", "20,000")

        # zoom into the outlined column: the cord swells past the frame while the column becomes the field of dots
        c = lmc.get_center()
        self.play(outer.animate.scale(4, about_point=c).set_opacity(0),
                  gray.animate.scale(4, about_point=c).set_opacity(0),
                  FadeOut(VGroup(cp, lab, la)), ReplacementTransform(lmc, outline),
                  FadeIn(ctr), run_time=0.9)
        self.at("the column")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.05),
                  vt.animate(rate_func=linear).set_value(6), run_time=2.0)
        self.at("just over")
        self.play(FadeOut(q1), FadeIn(val, scale=0.9), run_time=0.6)
        self.at("motor neurons")
        self.play(FadeIn(key), Indicate(dots, color=BLUE, scale_factor=1.03), run_time=0.9)
        self.finish()


def stage_a(day, kept_only=False, c2_val=False, cred=False):
    outline, dots = make_field(FX, FY, FA, FB, FR)
    if kept_only:
        for i in DYING:
            dots[i].set_opacity(0)
    vt = ValueTracker(day)
    ctr = day_counter(vt)
    c1, c2 = card(C1Y, "at the peak"), card(C2Y, "left afterwards")
    v1 = numval(C1Y, "just over", "20,000")
    v2 = numval(C2Y, "about", "12,000") if c2_val else qmark(C2Y)
    key = key_label()
    objs = [outline, dots, ctr, c1, c2, v1, v2, key]
    cr = rw = None
    if cred:
        cr, rw = credit(), raw_chip()
        objs += [cr, rw]
    return dict(outline=outline, dots=dots, vt=vt, ctr=ctr, c1=c1, c2=c2, v1=v1, v2=v2, objs=objs)


class S03Raw(SpokenScene):
    def construct(self):
        st = stage_a(6)
        self.add(*st["objs"])
        dots = st["dots"]
        cr, raw = credit(), raw_chip()
        self.at("Hamburger's")
        self.play(FadeIn(cr, shift=UP * 0.15), run_time=0.6)
        self.at("raw counts")
        # the dots shimmer to say "approximate"
        self.play(FadeIn(raw, shift=UP * 0.15), Indicate(st["v1"], color=BLUE, scale_factor=1.08),
                  LaggedStart(*[Indicate(d, color=BLUE, scale_factor=1.45) for d in dots], lag_ratio=0.02),
                  run_time=0.8)
        self.at("from 1975")
        self.play(Indicate(cr, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.finish()


class S04Fall(SpokenScene):
    def construct(self):
        st = stage_a(6, cred=True)
        self.add(*st["objs"])
        dots, vt = st["dots"], st["vt"]
        dying = [dots[i] for i in DYING]
        centers = [d.get_center().copy() for d in dying]
        blobs = [blob(c[0], c[1], 0.48, k).set_z_index(2) for k, c in enumerate(centers)]
        for d in dying:
            d.set_z_index(3)  # keep the shrinking neuron visible inside its engulfing cell
        # label one phagocyte (the one furthest right)
        j = max(range(len(centers)), key=lambda k: centers[k][0])
        ph_lab = cap("phagocyte", 30).move_to([1.0, centers[j][1], 0])
        ph_arr = arr(ph_lab.get_left() + LEFT * 0.02, centers[j] + RIGHT * 0.6, GREY, 4)
        # 1) the dying dots darken and shrink while the days run to 10
        self.play(vt.animate(rate_func=linear).set_value(8),
                  LaggedStart(*[d.animate.set_color(RED).scale(0.6) for d in dying], lag_ratio=0.03), run_time=0.8)
        # 2) phagocytes engulf them
        self.play(LaggedStart(*[GrowFromCenter(b) for b in blobs], lag_ratio=0.05), FadeIn(ph_lab), GrowArrow(ph_arr),
                  *[d.animate.scale(0.55) for d in dying], vt.animate.set_value(10), run_time=0.8)
        self.wait(0.4)
        # 3) the engulfed neurons are cleared
        self.play(*[FadeOut(d, scale=0.3) for d in dying], *[FadeOut(b, scale=0.6) for b in blobs],
                  FadeOut(ph_lab), FadeOut(ph_arr), run_time=0.6)
        self.at("roughly")
        self.play(FadeOut(st["v2"]), FadeIn(numval(C2Y, "about", "12,000"), scale=0.9), run_time=0.7)
        self.at("are left")
        self.play(Indicate(VGroup(*[dots[i] for i in KEPT]), color=BLUE, scale_factor=1.06), run_time=0.7)
        self.finish()


class S05Beat(SpokenScene):
    def construct(self):
        st = stage_a(10, kept_only=True, c2_val=True, cred=True)
        self.add(*st["objs"])
        self.finish()


# -----------------------------------------------------------------------------------------------------
GROUND_Y = -2.53


class S06Fine(SpokenScene):
    def construct(self):
        cx, cy = 0.0, 0.0
        bx, by = -0.7, -0.5
        egg, top, bot = egg_parts(cx, cy)
        ch = chick(bx, by, s=1.2)
        both = T("both legs", 36, YELLOW, weight=BOLD).move_to([4.7, -1.6, 0])
        ba = arr(both.get_left() + LEFT * 0.05, [bx + 0.95, by - 1.75, 0], YELLOW, 5)
        ground = Line([-6.6, GROUND_Y, 0], [6.6, GROUND_Y, 0], color=GREY, stroke_width=3)

        self.play(Create(egg), run_time=0.6)
        self.play(FadeIn(ch[0], scale=0.9), FadeIn(ch[1], scale=0.9), run_time=0.6)
        self.at("embryo")
        self.play(Indicate(ch[0], color=GREY, scale_factor=1.04), run_time=0.7)
        self.at("both legs")
        self.add(both.set_opacity(1))
        self.play(GrowArrow(ba), Indicate(ch[1], color=YELLOW, scale_factor=1.15), run_time=0.9)
        self.at("hatch")
        self.remove(egg)
        # Discard the upper shell at the crack; no disconnected floating cap.
        self.add(bot)
        self.play(FadeOut(bot),
                  Create(ground), run_time=0.8)
        self.at("will walk")
        self.remove(ch[0], ch[1], bot, top, both, ba)
        xv, sv = ValueTracker(bx), ValueTracker(0)
        walker = always_redraw(lambda: chick(xv.get_value(), by, t=sv.get_value(), walk=True, s=1.2))
        self.add(walker)
        # the walk crosses the frame and is held for 3 s (the scene is padded past the narration)
        self.play(xv.animate(rate_func=linear).set_value(3.9), sv.animate(rate_func=linear).set_value(3.2),
                  run_time=3.0)
        self.wait(0.3)
        self.finish()


# -----------------------------------------------------------------------------------------------------
FORK_Y_TOP, FORK_Y_BOT = 1.8, -2.3


def fork_pieces():
    left = chip2("those neurons", GREY, size=58, pad=0.3).move_to([0, FORK_Y_TOP, 0])
    q = T("?", 140, TEXT, weight=BOLD).move_to([0, -0.25, 0])
    top = chip2("made, then died", RED, size=58, pad=0.3).move_to([-3.35, FORK_Y_BOT, 0])
    bot = chip2("never made", GREY, size=58, pad=0.3).move_to([3.85, FORK_Y_BOT, 0])
    a_top = arr([-0.9, FORK_Y_TOP - 0.7, 0], [-3.0, FORK_Y_BOT + 0.75, 0], GREY, 6)
    a_bot = arr([0.9, FORK_Y_TOP - 0.7, 0], [3.5, FORK_Y_BOT + 0.75, 0], GREY, 6)
    return left, q, top, bot, a_top, a_bot


def ghost_of(m):
    box = m[0]
    d = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height,
                                        stroke_color=GREY, stroke_width=3).move_to(m.get_center()), num_dashes=40)
    return VGroup(d, m[1].copy().set_opacity(0.55))


class S07Q1(SpokenScene):
    def construct(self):
        left, q, top, bot, a_top, a_bot = fork_pieces()
        g_top, g_bot = ghost_of(top), ghost_of(bot)
        head = headline("Question 1")
        self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(left, shift=DOWN * 0.2), run_time=0.5)
        self.at("questions")
        self.play(GrowArrow(a_top), GrowArrow(a_bot), FadeIn(q, scale=0.5), FadeIn(g_top), FadeIn(g_bot), run_time=0.8)
        self.at("how could anyone")
        self.play(Indicate(q, color=TEXT, scale_factor=1.2), run_time=0.7)
        self.at("made and then died")
        self.play(FadeOut(g_top), FadeIn(top), a_top.animate.set_color(RED), run_time=0.5)
        self.at("never made")
        self.play(FadeOut(g_bot), FadeIn(bot), a_bot.animate.set_color(TEXT), run_time=0.5)
        self.wait(1.0)
        self.finish()


class S08Q2(SpokenScene):
    def construct(self):
        left, q, top, bot, a_top, a_bot = fork_pieces()
        a_top.set_color(RED)
        head = headline("Question 1")
        self.add(head, left, q, top, bot, a_top, a_bot)
        head2 = headline("Question 2")
        outline, dots = make_field(-3.5, -0.1, 2.5, 2.7, 0.24)
        box = RoundedRectangle(corner_radius=0.25, width=5.6, height=3.1, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.07).move_to([3.7, -0.1, 0])
        txt = T("what decides\nhow many stay?", 46, TEXT, line_spacing=0.9).move_to(box)
        card2 = VGroup(box, txt)
        qa = arr(box.get_left(), [-0.85, -0.1, 0], GREY, 6)
        lab = T("how many stay", 34, BLUE, weight=BOLD).move_to([-3.5, -3.5, 0])
        self.play(FadeOut(VGroup(left, q, top, bot, a_top, a_bot)), Transform(head, head2),
                  FadeIn(outline), FadeIn(dots), run_time=0.4)
        self.at("what decides")
        self.play(FadeIn(card2, scale=0.9), GrowArrow(qa), run_time=0.4)
        self.at("how many stay")
        self.play(*[dots[i].animate.scale(0.25).set_color(RED).set_opacity(GHOST) for i in DYING], FadeIn(lab),
                  run_time=0.8)
        self.wait(1.3)       # hold the full question at least 3 s (the scene is padded past the narration)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def rule_lines():
    head = T("One idea", 44, TEAL, weight=BOLD).move_to([0, 3.35, 0])
    l1 = T("Make too many,", 58, TEXT, font=TITLE_FONT, t2c={"too many": BLUE}).move_to([0, 2.4, 0])
    l2 = T("then let the target", 58, TEXT, font=TITLE_FONT, t2c={"target": YELLOW}).move_to([0, 1.3, 0])
    l3 = T("keep what it can support.", 58, TEXT, font=TITLE_FONT).move_to([0, 0.2, 0])
    row = VGroup(*[Dot([-5.4 + 1.2 * k, -2.0, 0], radius=0.46, color=BLUE) for k in range(10)])
    return head, l1, l2, l3, row


LOST_ROW = (1, 4, 6, 8)


class S09Rule(SpokenScene):
    def construct(self):
        head, l1, l2, l3, row = rule_lines()
        head.move_to([0, 0.2, 0]).scale(2.0)          # "One idea" holds the whole frame while it is announced
        self.play(FadeIn(head, scale=0.9), run_time=0.7)
        self.at("make too many")
        self.play(head.animate.scale(0.5).move_to([0, 3.35, 0]), FadeIn(l1, shift=UP * 0.15), LaggedStart(*[FadeIn(d, scale=0.4) for d in row], lag_ratio=0.1),
                  run_time=1.0)
        self.at("then let the target")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.6)
        self.at("keep what it can support")
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.5)
        self.play(LaggedStart(*[row[i].animate.set_color(RED).set_opacity(GHOST) for i in LOST_ROW], lag_ratio=0.35),
                  run_time=1.4)
        self.finish()


class S10Beat(SpokenScene):
    def construct(self):
        head, l1, l2, l3, row = rule_lines()
        for i in LOST_ROW:
            row[i].set_color(RED).set_opacity(GHOST)
        self.add(head, l1, l2, l3, row)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def target_stage():
    """column on the left, leg block on the right, 40 axons between."""
    outline, dots = make_field(-4.6, 0.0, 1.7, 2.8, 0.2)
    axons, contacts = make_axons(dots)
    block = RoundedRectangle(corner_radius=0.25, width=BW, height=BH, stroke_color=YELLOW, stroke_width=4,
                             fill_color=YELLOW, fill_opacity=0.2).move_to([BX, 0, 0])
    label = T("target", 36, YELLOW, weight=BOLD).move_to([BX, 3.45, 0])
    leg = T("leg\nmuscles", 32, YELLOW, line_spacing=0.9).move_to([BX, 0.8, 0])
    glow = glow_rings()
    sup = T("support", 32, YELLOW, weight=BOLD).move_to([BX, -1.4, 0])
    glow.set_z_index(-2)
    outline.set_z_index(-1)
    for a in axons:
        a.set_z_index(0)
    block.set_z_index(1)
    contacts.set_z_index(2)
    dots.set_z_index(3)
    for m in (label, leg, sup):
        m.set_z_index(4)
    return dict(outline=outline, dots=dots, axons=axons, contacts=contacts, block=block, label=label, leg=leg,
                glow=glow, sup=sup)


class S11Target(SpokenScene):
    def construct(self):
        st = target_stage()
        outline, dots, axons, contacts = st["outline"], st["dots"], st["axons"], st["contacts"]
        mid_i = sorted(range(40), key=lambda i: dots[i].get_center()[1])[20]
        grow = cap("axons grow", 32).move_to([-0.4, 3.15, 0])
        conn = cap("axons connect", 32).move_to([-0.4, 3.15, 0])
        self.play(FadeIn(outline), FadeIn(dots), run_time=0.3)
        self.at("target")
        self.play(FadeIn(st["block"], scale=0.9), FadeIn(st["label"], shift=DOWN * 0.1), FadeIn(st["glow"]),
                  FadeIn(st["sup"]), run_time=0.5)
        self.at("tissue")
        self.play(Indicate(st["block"], color=YELLOW, scale_factor=1.03), run_time=0.6)
        self.at("axon")
        self.play(Create(axons[mid_i]), FadeIn(grow), run_time=0.4)
        self.at("grows to")
        self.play(LaggedStart(*[Create(a) for i, a in enumerate(axons) if i != mid_i], lag_ratio=0.02), run_time=0.85)
        self.at("connects with")
        self.play(LaggedStart(*[FadeIn(c, scale=2.5) for c in contacts], lag_ratio=0.02),
                  ReplacementTransform(grow, conn), run_time=0.7)
        self.at("muscles of")
        self.play(FadeIn(st["leg"], shift=UP * 0.1), run_time=0.5)
        self.at("the leg")
        self.play(Indicate(st["block"], color=YELLOW, scale_factor=1.03), Indicate(st["leg"], color=YELLOW),
                  run_time=0.7)
        self.finish()


# ---- s12, s13: three states of the experiment ----------------------------------------------------------
PX = [-4.7, 0.0, 4.7]
PSCALE = [0.55, 1.0, 1.4]
PGLOW = [0.35, 1.0, 1.6]
PNAME = ["less target", "normal target", "extra target"]
PSURV = ["survivors: fewer", "survivors: 24 of 40", "survivors: a few more"]
BLK_Y = 2.25
DOT_Y = -0.95


def lost_for(k):
    if k == 1:
        return list(DYING)
    if k == 0:
        return sorted(DYING + KEPT[:8])
    return DYING[:12]


def panel(k):
    cx = PX[k]
    s = PSCALE[k]
    bw, bh = 2.4 * s, 1.1 * s
    block = RoundedRectangle(corner_radius=0.2, width=bw, height=bh, stroke_color=YELLOW, stroke_width=4,
                             fill_color=YELLOW, fill_opacity=0.2).move_to([cx, BLK_Y, 0])
    glow = VGroup()
    for gk, op in ((1, 0.20), (2, 0.12), (3, 0.06)):
        glow.add(RoundedRectangle(corner_radius=0.3, width=bw + 0.2 * gk * PGLOW[k] + 0.1,
                                  height=bh + 0.14 * gk * PGLOW[k] + 0.1, stroke_width=0, fill_color=YELLOW,
                                  fill_opacity=min(0.55, op * PGLOW[k])).move_to([cx, BLK_Y, 0]))
    label = T(PNAME[k], 30, YELLOW, weight=BOLD).move_to([cx, 0.98, 0])
    outline, dots = make_field(cx, DOT_Y, 1.9, 1.65, 0.18)
    glow.set_z_index(-1)
    return dict(block=block, glow=glow, label=label, outline=outline, dots=dots)


def lose(p, k):
    for i in lost_for(k):
        p["dots"][i].set_color(RED).set_opacity(GHOST)


def panel_mobs(p):
    return [p["glow"], p["block"], p["label"], p["outline"], p["dots"]]


def lost_anims(ps):
    anims = []
    for k, p in enumerate(ps):
        for i in lost_for(k):
            anims.append(p["dots"][i].animate.set_color(RED).set_opacity(GHOST))
    return anims


def tag_chip(text):
    return chip2(text, GREY, size=27, pad=0.1).move_to([0, 3.55, 0])


def surv_lines():
    return [cap(PSURV[k], 28, TEXT).move_to([PX[k], -3.3, 0]) for k in range(3)]


def made_lines():
    return [cap("made: same", 28, BLUE).move_to([PX[k], -3.3, 0]) for k in range(3)]


class S12Scope1(SpokenScene):
    def construct(self):
        ps = [panel(k) for k in range(3)]
        tag = tag_chip("chick limb experiments")
        sv = surv_lines()
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        self.play(*[FadeIn(m) for m in panel_mobs(ps[1])], run_time=0.8)
        self.at("changing the target")
        self.play(*[FadeIn(m) for k in (0, 2) for m in panel_mobs(ps[k])], run_time=0.6)
        self.at("changed how many")
        self.play(LaggedStart(*lost_anims(ps), lag_ratio=0.02), run_time=1.3)
        self.at("survived")
        self.play(*[FadeIn(t, shift=UP * 0.1) for t in sv], run_time=0.7)
        self.finish()


class S13Scope1b(SpokenScene):
    def construct(self):
        ps = [panel(k) for k in range(3)]
        for k, p in enumerate(ps):
            lose(p, k)
            self.add(*panel_mobs(p))
        tag = tag_chip("chick limb experiments")
        tag2 = tag_chip("chick limb: survival, not production")
        sv, ml = surv_lines(), made_lines()
        self.add(tag, *sv)
        self.at("detectably")
        self.play(ReplacementTransform(tag, tag2), run_time=0.6)
        self.at("how many were made")
        # rewind: every state starts from the same 40 dots
        self.play(*[p["dots"][i].animate.set_color(BLUE).set_opacity(1) for k, p in enumerate(ps)
                    for i in lost_for(k)], *[FadeOut(t) for t in sv], run_time=0.7)
        self.at("made")
        self.play(*[FadeIn(t, shift=UP * 0.1) for t in ml], run_time=0.5)
        self.play(*[Indicate(p["dots"], color=BLUE, scale_factor=1.04) for p in ps], run_time=0.6)
        self.finish()


# -----------------------------------------------------------------------------------------------------
KC = -math.log(0.4) / 0.5        # f(0.5) = 0.6 of the peak, i.e. 12,000 of 20,000 at "normal"


def fsurv(u):
    """survivors as a fraction of the peak (schematic saturating curve through normal = 12,000)."""
    return 1 - math.exp(-KC * u)


def dial_parts(cx, cy, R, ud):
    arc = Arc(radius=R, start_angle=math.radians(-30), angle=math.radians(240), color=GREY,
              stroke_width=5).move_arc_center_to([cx, cy, 0])
    ticks = VGroup()
    for k in range(9):
        th = math.radians(210 - 240 * k / 8)
        ticks.add(Line([cx + 0.82 * R * math.cos(th), cy + 0.82 * R * math.sin(th), 0],
                       [cx + 0.98 * R * math.cos(th), cy + 0.98 * R * math.sin(th), 0], color=GREY, stroke_width=4))
    d = lambda: min(max((ud.get_value() - 0.25) / 0.75, 0), 1)
    needle = always_redraw(lambda: Line([cx, cy, 0],
                                        [cx + 0.8 * R * math.cos(math.radians(210 - 240 * d())),
                                         cy + 0.8 * R * math.sin(math.radians(210 - 240 * d())), 0],
                                        color=TEXT, stroke_width=7))
    hub = Dot([cx, cy, 0], radius=0.09, color=TEXT)
    glow = always_redraw(lambda: Circle(radius=0.2 + 0.7 * d(), stroke_width=0, fill_color=YELLOW,
                                        fill_opacity=0.3).move_to([cx, cy, 0]))
    lab = T("target", 30, YELLOW, weight=BOLD).move_to([cx, cy - R - 0.45, 0])
    return arc, ticks, needle, hub, glow, lab


class S14Dial(SpokenScene):
    def construct(self):
        pl = Plot(-3.0, -2.9, 7.0, 5.6)
        U_N, U_X, U_END, U0 = 0.5, 0.72, 0.88, 0.25
        u = ValueTracker(U_N)
        axes = VGroup(Line(pl.P(0, 0), pl.P(1.0, 0), color=GREY, stroke_width=4),
                      Line(pl.P(0, 0), pl.P(0, 1.04), color=GREY, stroke_width=4))
        yl = T("neurons that survive", 28, BLUE).rotate(PI / 2).move_to([-5.75, 0.0, 0])
        xl = T("amount of target", 28, YELLOW).move_to([pl.P(0.5, 0)[0], -3.5, 0])
        t12 = VGroup(Line(pl.P(0, 0.6) + LEFT * 0.15, pl.P(0, 0.6), color=GREY, stroke_width=4),
                     T("12,000", 28, BLUE, weight=BOLD).next_to(pl.P(0, 0.6) + LEFT * 0.15, LEFT, buff=0.12))
        t20 = VGroup(Line(pl.P(0, 1.0) + LEFT * 0.15, pl.P(0, 1.0), color=GREY, stroke_width=4),
                     T("20,000", 28, TEXT, weight=BOLD).next_to(pl.P(0, 1.0) + LEFT * 0.15, LEFT, buff=0.12))
        ceil = DashedLine(pl.P(0, 1.0), pl.P(1.0, 1.0), color=GREY, stroke_width=4)
        clab = T("all present at the peak", 32, TEXT, weight=BOLD).set_opacity(1).move_to([pl.P(0, 1.0)[0] + 0.2, 3.25, 0], aligned_edge=LEFT)
        clab.align_to(pl.P(0, 0), LEFT).shift(RIGHT * 0.15)
        sch = cap("schematic:\nshape not measured", 28, CAPC, line_spacing=0.9).move_to([pl.P(0.78, 0)[0], -2.0, 0])
        arc, ticks, needle, hub, glow, dlab = dial_parts(5.85, 0.3, 0.85, u)

        solid0 = pl.curve(fsurv, U0, U_N, BLUE, 8, 40)
        solid1 = pl.curve(fsurv, U_N, U_X, BLUE, 8, 40)
        dashed = DashedVMobject(pl.curve(fsurv, U_X, U_END, BLUE, 8, 40), num_dashes=14)
        normal_dot = Dot(pl.P(U_N, 0.6), radius=0.12, color=BLUE)
        marker = always_redraw(lambda: Dot(pl.P(u.get_value(), fsurv(u.get_value())), radius=0.15, color=BLUE))

        def bracket():
            ux = u.get_value()
            xx = pl.P(ux, 0)[0] + 0.0
            y0 = pl.P(0, fsurv(ux))[1]
            y1 = pl.P(0, 1.0)[1]
            return VGroup(Line([xx, y0, 0], [xx, y1, 0], color=RED, stroke_width=6),
                          Line([xx - 0.14, y0, 0], [xx + 0.14, y0, 0], color=RED, stroke_width=6),
                          Line([xx - 0.14, y1, 0], [xx + 0.14, y1, 0], color=RED, stroke_width=6))
        brk = always_redraw(bracket)
        dlabel = always_redraw(lambda: T("deaths", 28, RED, weight=BOLD).move_to(
            [pl.P(u.get_value(), 0)[0] + 0.95, (pl.P(0, fsurv(u.get_value()))[1] + pl.P(0, 1.0)[1]) / 2 + 0.1, 0]))
        nlab = cap("normal", 28, BLUE).move_to(pl.P(U_N, fsurv(U_N)) + np.array([0.85, -0.45, 0]))
        xlab = cap("extra leg:\na small rise", 28, BLUE, line_spacing=0.9).move_to(
            pl.P(U_X, fsurv(U_X)) + np.array([1.15, -0.7, 0]))
        ring = Circle(radius=0.25, stroke_color=BLUE, stroke_width=4).move_to(pl.P(U_X, fsurv(U_X)))
        ghost = DashedVMobject(Circle(radius=0.3, color=GREY, stroke_width=4).move_to([4.0, 3.25, 0]), num_dashes=12)
        glab = cap("not there", 28).move_to([5.4, 3.25, 0])

        self.play(FadeIn(VGroup(arc, ticks, hub, dlab)), FadeIn(glow), Create(axes), FadeIn(yl), FadeIn(xl), FadeIn(t12),
                  FadeIn(t20), Create(ceil), Create(solid0), FadeIn(needle), FadeIn(nlab), FadeIn(sch),
                  FadeIn(normal_dot), FadeIn(marker), FadeIn(brk), FadeIn(dlabel), FadeIn(clab), run_time=0.6)
        self.play(Create(solid1, rate_func=linear), u.animate(rate_func=linear).set_value(U_X),
                  Succession(Wait(0.7), AnimationGroup(FadeIn(xlab), Create(ring), run_time=0.2)), run_time=0.9)
        self.at("up to a ceiling")
        self.play(Create(dashed, rate_func=linear), u.animate(rate_func=linear).set_value(U_END),
                  run_time=1.0)
        self.at("rescue")
        self.play(Indicate(ceil, color=TEXT), Indicate(clab, color=TEXT, scale_factor=1.04), run_time=0.5)
        self.at("a neuron")
        self.play(FadeIn(ghost, scale=0.6), FadeIn(glab), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------------
def clock_parts(cx, cy, R, ang):
    face = Circle(radius=R, stroke_color=TEXT, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    ticks = VGroup(*[Line([cx + 0.82 * R * math.sin(k * math.pi / 6), cy + 0.82 * R * math.cos(k * math.pi / 6), 0],
                          [cx + 0.98 * R * math.sin(k * math.pi / 6), cy + 0.98 * R * math.cos(k * math.pi / 6), 0],
                          color=GREY, stroke_width=4) for k in range(12)])
    hand = always_redraw(lambda: Line([cx, cy, 0], [cx + 0.72 * R * math.sin(ang.get_value()),
                                                    cy + 0.72 * R * math.cos(ang.get_value()), 0],
                                      color=TEXT, stroke_width=7))
    hub = Dot([cx, cy, 0], radius=0.08, color=TEXT)
    return VGroup(face, ticks, hub), hand


class S15Own(SpokenScene):
    def construct(self):
        cx, cy = 1.4, 0.1
        A, B = 2.5, 2.85
        outline = Ellipse(width=2 * A, height=2 * B, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                          fill_opacity=0.07).move_to([cx, cy, 0])
        n = 18
        ga = math.pi * (3 - math.sqrt(5))
        pts = [(0.88 * math.sqrt((i + 0.5) / n) * math.cos(i * ga), 0.88 * math.sqrt((i + 0.5) / n) * math.sin(i * ga))
               for i in range(n)]
        dots = VGroup(*[Dot([cx + A * a, cy + B * b, 0], radius=0.27, color=BLUE) for a, b in pts])
        lost = random.Random(5).sample(range(n), 8)
        ang = ValueTracker(0.0)
        face, hand = clock_parts(5.55, 1.9, 0.95, ang)
        poplab = cap("e.g. early chick cervical motor neurons", 28).move_to([cx, -3.5, 0])
        blk = RoundedRectangle(corner_radius=0.25, width=2.3, height=3.6, stroke_color=YELLOW, stroke_width=4,
                               fill_color=YELLOW, fill_opacity=0.2).move_to([-5.0, 0.1, 0])
        blab = T("target", 34, YELLOW, weight=BOLD).move_to(blk)
        ar = Arrow([-3.75, 0.1, 0], [-1.3, 0.1, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.25,
                   stroke_opacity=0.5)
        xmark = VGroup(Line([-2.95, 0.55, 0], [-2.15, -0.35, 0], color=RED, stroke_width=10),
                       Line([-2.95, -0.35, 0], [-2.15, 0.55, 0], color=RED, stroke_width=10))
        tag = chip2("not every\npopulation", GREY, size=30, pad=0.2).move_to([5.45, -0.55, 0])

        self.play(FadeIn(outline), FadeIn(face), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.03),
                  FadeIn(poplab), run_time=0.8)
        self.add(ang, hand)
        ang.add_updater(lambda m, dt: m.increment_value(dt * 1.3))   # the clock keeps running on its own
        self.at("die")
        self.play(AnimationGroup(
            LaggedStart(*[dots[i].animate.set_color(RED).set_opacity(GHOST) for i in lost], lag_ratio=0.22),
            Succession(Wait(1.4), AnimationGroup(FadeIn(blk), FadeIn(blab), FadeIn(ar), FadeIn(xmark, scale=1.3),
                                                 run_time=0.8)),
            run_time=3.0))
        self.at("the lesson ends")
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.7)
        self.finish()


# -----------------------------------------------------------------------------------------------------
class S16Take(SpokenScene):
    def construct(self):
        head = T("Takeaway", 36, TEAL, weight=BOLD).move_to([0, 3.35, 0])
        l1 = T("The embryo makes too many,", 52, TEXT, font=TITLE_FONT, t2c={"too many": BLUE}).move_to([0, 2.4, 0])
        l2 = T("and in the limb, the target", 52, TEXT, font=TITLE_FONT, t2c={"target": YELLOW}).move_to([0, 1.4, 0])
        l3 = T("helps set how many survive.", 52, TEXT, font=TITLE_FONT).move_to([0, 0.4, 0])
        t1 = chip2("survival, not production (chick limb)", BLUE, size=34, pad=0.22).move_to([0, -1.0, 0])
        t2 = chip2("a dial with a ceiling", YELLOW, size=34, pad=0.22).move_to([0, -2.1, 0])
        t3 = chip2("not every population", GREY, size=34, pad=0.22).move_to([0, -3.2, 0])
        self.play(FadeIn(head), run_time=0.4)
        self.at("the embryo makes")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.6)
        self.at("in the limb")
        self.play(FadeIn(l2, shift=UP * 0.15), FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("helps set")
        self.play(FadeIn(l3, shift=UP * 0.15), FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.at("survive")
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S17End(EndCard):
    LINE = "Too many are made; the limb target helps set survival."

    def construct(self):
        line = T("Too many are made;\nthe limb target helps set survival.", size=56, font=TITLE_FONT, line_spacing=0.9)
        fit(line, max_w=12.2)
        sub = T("biochemistrypedia.com", size=30, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
