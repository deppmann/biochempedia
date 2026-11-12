"""Competition (film 2): What Keeps Chthamalus High?  Connell's barnacle removal at Millport.

COLOUR MAP (carried from film 1, same constants): TEAL = Chthamalus (species 1), ORANGE = Balanus (species 2),
GREEN = passes / helped, RED = fails / crossed out, YELLOW = question / highlight.
One world: a side-on shore cross-section (rock, tide lines, sea) and a top-down patch split in two halves.
Every shore, barnacle, whelk and bar is a schematic cartoon; no value is a measurement.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

TC = TEAL
OC = "#F29E4C"
ROCK = "#8A8F98"
SEA = "#4C8FD6"
RING = "#FFFFFF"

# shore layout (x of the cone field and the label columns are the same in every shore scene)
CX0, CX1 = -3.0, 3.6
Y_TOP, Y_BOT = 3.2, -2.4          # rock top / sea level
Y_HIGH, Y_MID, Y_LOW = 3.0, 0.3, -2.0
Y_BOUND = 1.45                      # boundary between the two bands


def cone(color, x, y, w, h, op=0.95):
    return Polygon([x - w / 2, y, 0], [x + w / 2, y, 0], [x, y + h, 0], stroke_color=color, stroke_width=2,
                   fill_color=color, fill_opacity=op)


def band(color, rows, w, h, step, jit):
    g = VGroup()
    for r, y in enumerate(rows):
        x = CX0 + (step / 2 if r % 2 else 0) + 0.05
        i = 0
        while x <= CX1:
            g.add(cone(color, x + jit[(i + 3 * r) % len(jit)] * 0.08, y, w, h))
            x += step
            i += 1
    return g


JIT = [0.0, 1.0, -1.0, 0.5, -0.5, 1.0, -1.0, 0.0]
TEAL_ROWS = [1.55, 2.1, 2.65]
ORANGE_ROWS = [-1.8, -1.15, -0.5, 0.15, 0.7]


def tint(op):
    return dict(fill_opacity=op)


def make_sea():
    water = Rectangle(width=14.3, height=Y_BOT + 3.9, stroke_width=0, fill_color=SEA, fill_opacity=0.45).move_to([0, (Y_BOT - 3.9) / 2, 0])
    wave = VMobject(stroke_color=SEA, stroke_width=5)
    wave.tm = 0.0
    xs = np.linspace(-7.1, 7.1, 70)

    def up(m, dt):
        m.tm += dt
        m.set_points_as_corners([[x, Y_BOT + 0.07 * np.sin(1.3 * x + 2.2 * m.tm), 0] for x in xs])
    wave.add_updater(up)
    up(wave, 0)
    return VGroup(water, wave)


def make_rock():
    return Rectangle(width=14.3, height=Y_TOP - Y_BOT, stroke_width=0, fill_color=ROCK, fill_opacity=0.3).move_to([0, (Y_TOP + Y_BOT) / 2, 0])


def tide_lines(labels=True):
    g = VGroup()
    for y, n in [(Y_HIGH, "high tide"), (Y_MID, "mid-tide"), (Y_LOW, "low tide")]:
        g.add(DashedLine([-3.2, y, 0], [4.9, y, 0], color=SEA, stroke_width=3, dash_length=0.2).set_opacity(0.8))
        if labels:
            g.add(T(n, 26, "#8DB8EA").move_to([5.9, y + 0.0, 0]))
    return g


def schem(x=-5.9, y=-3.55):
    return T("schematic", 22, TEXT).set_opacity(0.8).move_to([x, y, 0])


def shore_base(scene, tides=True, tide_labels=True):
    rock, sea = make_rock(), make_sea()
    scene.add(rock, sea)
    tl = None
    if tides:
        tl = tide_lines(tide_labels)
        scene.add(tl)
        scene._tl = tl
    return rock, sea, tl


def breathe(m, amp=0.012, speed=1.6, phase=0.0):
    m.w0 = m.width
    m.tm = phase

    def up(mm, dt):
        mm.tm += dt
        mm.scale(mm.w0 * (1 + amp * np.sin(speed * mm.tm)) / mm.width)
    m.add_updater(up)
    return m


def pulse(m, f=1.03, t=1.4):
    return m.animate.scale(f).set_run_time(t).set_rate_func(there_and_back)


def backed(text, size=28, color=TEXT):
    t = T(text, size, color)
    r = Rectangle(width=t.width + 0.3, height=t.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    return VGroup(r, t)


def lines_label(lines, size=28, color=TEXT, align=LEFT):
    return VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=align, buff=0.12)


# ---------------------------------------------------------------- the top-down patch (s04 to s13)
PATCH_C = np.array([0.0, 0.0, 0.0])
PW, PH = 10.4, 5.0
# positions are cone BASE points (x, y); teal tips sit 0.75 above, oranges 0.85
TEAL_L = [(-3.4, 0.9), (-1.5, -0.4), (-3.2, -1.4)]
TEAL_R = [(x + 5.2, y) for x, y in TEAL_L]


def _oranges():
    out = []
    for tx, ty in TEAL_L:
        for dx, dy in [(-0.95, 0.0), (0.95, 0.05), (-0.5, -0.9), (0.55, -0.9), (-0.9, 0.95), (0.95, 0.95)]:
            x, y = tx + dx, ty + dy
            if not (-4.75 <= x <= -0.55 and -2.3 <= y <= 1.55):
                continue
            if any((x - a) ** 2 + (y - b) ** 2 < 0.85 ** 2 for a, b in out):
                continue
            if any((x - a) ** 2 + (y - b) ** 2 < 0.8 ** 2 for a, b in TEAL_L):
                continue
            out.append((x, y))
    return out


ORG_L = _oranges()
ORG_R = [(x + 5.2, y) for x, y in ORG_L]


def patch_world(numbers=True, scale=1.0, centre=PATCH_C, orange_left=True, orange_right=True):
    rock = RoundedRectangle(corner_radius=0.3, width=PW, height=PH, stroke_color=ROCK, stroke_width=4, fill_color=ROCK, fill_opacity=0.28)
    div = DashedLine([0, PH / 2, 0], [0, -PH / 2, 0], color=TEXT, stroke_width=4, dash_length=0.18)
    tl = VGroup(*[cone(TC, x, y, 0.7, 0.75) for x, y in TEAL_L + TEAL_R])
    ol = VGroup(*[cone(OC, x, y, 0.85, 0.85) for x, y in ORG_L])
    orr = VGroup(*[cone(OC, x, y, 0.85, 0.85) for x, y in ORG_R])
    nums = VGroup(*[T(str(i % 3 + 1), 22, TEXT, weight=BOLD).move_to([x, y + 1.05, 0]) for i, (x, y) in enumerate(TEAL_L + TEAL_R)])
    parts = dict(rock=rock, div=div, tl=tl, ol=ol, orr=orr, nums=nums)
    return parts


def place(parts, scale=1.0, centre=PATCH_C):
    allg = VGroup(*parts.values())
    allg.scale(scale).shift(centre)
    return allg


def groupall(parts, keys):
    return VGroup(*[parts[k] for k in keys])


def survival_frame(cx, cy_bottom, w=1.7, h=2.4, label=""):
    f = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([cx, cy_bottom + h / 2, 0])
    return f


def drop_clock(size=1.0):
    drop = VGroup(Circle(radius=0.5 * size, stroke_color=SEA, stroke_width=4, fill_color=SEA, fill_opacity=0.5).shift(DOWN * 0.15 * size),
                  Polygon([-0.43 * size, 0.0, 0], [0.43 * size, 0.0, 0], [0, 0.95 * size, 0], stroke_color=SEA, stroke_width=4, fill_color=SEA, fill_opacity=0.5))
    clk = VGroup(Circle(radius=0.3 * size, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1),
                 Line(ORIGIN, [0, 0.2 * size, 0], color=TEXT, stroke_width=4), Line(ORIGIN, [0.14 * size, 0, 0], color=TEXT, stroke_width=4)).move_to(drop.get_center() + DOWN * 0.15 * size)
    return VGroup(drop, clk)


def whelk(size=1.0):
    shell = Polygon([-0.5 * size, -0.35 * size, 0], [0.45 * size, -0.35 * size, 0], [0.2 * size, 0.55 * size, 0], [-0.4 * size, 0.3 * size, 0],
                    stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.5)
    sw = VGroup(*[Arc(radius=(0.12 + 0.1 * i) * size, start_angle=0, angle=PI * 1.2, color=TEXT, stroke_width=3).move_to([-0.05 * size, 0.0, 0]) for i in range(2)])
    foot = Ellipse(width=1.1 * size, height=0.22 * size, stroke_width=0, fill_color=RED, fill_opacity=0.8).move_to([0, -0.42 * size, 0])
    return VGroup(foot, shell, sw)


def check(x, y, c=GREEN, s=0.17):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.8, 0], color=c, stroke_width=6), Line([x - s * 0.3, y - s * 0.8, 0], [x + s * 1.1, y + s, 0], color=c, stroke_width=6))


def cross_mark(x, y, c=RED, s=0.3):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=c, stroke_width=8), Line([x - s, y + s, 0], [x + s, y - s, 0], color=c, stroke_width=8))


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Competition"
    TITLE = "What Keeps Chthamalus High?"

    def setup(self):
        super().setup()
        rock, sea, _ = shore_base(self, tides=False)
        rock.set_opacity(0.5)


# -------------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        # film 1's phase plane (computed isoclines, K1=100, K2=80, a=0.5), large at first
        ox, oy, W, H = -3.0, -2.6, 6.0, 4.6
        P = lambda x, y: np.array([ox + x / 170 * W, oy + y / 120 * H, 0])
        ax = VGroup(Line(P(0, 0), P(170, 0), color=GREY, stroke_width=4), Line(P(0, 0), P(0, 120), color=GREY, stroke_width=4))
        tl = Line(P(100, 0), P(40, 120), color=TC, stroke_width=7)
        ol = Line(P(0, 80), P(160, 0), color=OC, stroke_width=7)
        ring = Circle(radius=0.3, color=RING, stroke_width=6).move_to(P(80, 40))
        inset = VGroup(ax, tl, ol, ring)
        self.play(FadeIn(inset), run_time=1.2)
        self.at("species grow")
        self.play(Indicate(ring, scale_factor=1.5, color=RING), run_time=1.0)
        self.at("On a rocky")
        rock, sea = make_rock(), make_sea()
        tl_lines = tide_lines(False)
        bound = DashedLine([-6.0, Y_BOUND, 0], [6.0, Y_BOUND, 0], color=TEXT, stroke_width=4)
        self.play(FadeIn(rock), FadeIn(sea), inset.animate.scale(0.2).move_to([-6.0, 3.3, 0]).set_opacity(0.0), run_time=1.1)
        self.add(tl_lines)
        lab = T("Millport, Isle of Cumbrae, Scotland", 28, TEXT).move_to([0.6, 3.35, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), FadeIn(tl_lines), Create(bound), run_time=0.7)
        self.at("what keeps")
        q = T("?", 120, YELLOW, weight=BOLD).move_to([0, Y_BOUND + 0.05, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.8)
        self.at("just below")
        arr = Arrow([4.4, -0.8, 0], [4.4, Y_BOUND - 0.25, 0], buff=0, color=YELLOW, stroke_width=8, tip_length=0.3)
        self.play(GrowArrow(arr), run_time=0.8)
        self.play(q.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S02Bands(SpokenScene):
    def construct(self):
        shore_base(self)
        sc = schem()
        self.add(sc)
        t_cones = band(TC, TEAL_ROWS, 0.42, 0.5, 0.7, JIT)
        o_cones = band(OC, ORANGE_ROWS, 0.72, 0.7, 1.0, JIT)
        self.at("At Millport")
        self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in t_cones], lag_ratio=0.03), run_time=2.4)
        self.at("in teal", 0.4)
        tlab = T("Chthamalus", 32, TC, weight=BOLD).move_to([-4.9, 2.1, 0])
        self.play(FadeIn(tlab, shift=RIGHT * 0.2), run_time=0.7)
        self.at("Another barnacle", 0.1)
        self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in o_cones], lag_ratio=0.02), run_time=1.6)
        self.at("in orange", 0.4)
        olab = T("Balanus", 32, OC, weight=BOLD).move_to([-4.9, -0.5, 0])
        self.play(FadeIn(olab, shift=RIGHT * 0.2), run_time=0.7)
        self.at("rival", 0.3)
        hb = Rectangle(width=CX1 - CX0 + 0.9, height=0.22, stroke_color=YELLOW, stroke_width=0, fill_color=YELLOW, fill_opacity=0.6).move_to([(CX0 + CX1) / 2 + 0.05, Y_BOUND - 0.05, 0])
        self.play(FadeIn(hb), run_time=0.6)
        self.play(hb.animate.set_fill(opacity=0.25), rate_func=there_and_back, run_time=1.6)
        self.play(Indicate(hb, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.finish()


def shore_full(scene, tide_labels=True, labels=True):
    shore_base(scene, tide_labels=tide_labels)
    t_cones = band(TC, TEAL_ROWS, 0.42, 0.5, 0.7, JIT)
    o_cones = band(OC, ORANGE_ROWS, 0.72, 0.7, 1.0, JIT)
    tlab = T("Chthamalus", 32, TC, weight=BOLD).move_to([-4.9, 2.1, 0])
    olab = T("Balanus", 32, OC, weight=BOLD).move_to([-4.9, -0.5, 0])
    scene.add(t_cones, o_cones, schem())
    if labels:
        scene.add(tlab, olab)
    return t_cones, o_cones, tlab, olab


class S03Rivals(SpokenScene):
    def construct(self):
        t_cones, o_cones, tlab, olab = shore_full(self)
        self.at("Lower down", 0.0)
        self.play(Indicate(olab, color=OC, scale_factor=1.15), run_time=0.9)
        self.play(o_cones.animate.set_opacity(0.3), FadeOut(olab), FadeOut(self._tl), run_time=0.8)
        cw, ch, cy = 3.6, 2.9, -0.35
        cxs = [-4.0, 0.0, 4.0]
        cards = [RoundedRectangle(corner_radius=0.2, width=cw, height=ch, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=0.92).move_to([x, cy, 0]) for x in cxs]
        # 1 immersion
        ic1 = drop_clock(1.1).move_to([cxs[0], cy + 0.4, 0])
        l1 = T("longer immersion", 28, "#8DB8EA").move_to([cxs[0], cy - 0.85, 0])
        # 2 whelk
        ic2 = whelk(1.3).move_to([cxs[1], cy + 0.4, 0])
        l2 = T("predator: Thais", 28, RED).move_to([cxs[1], cy - 0.85, 0])
        # 3 crowding
        ic3 = VGroup(cone(OC, cxs[2] - 0.85, cy + 0.0, 0.85, 0.9), cone(TC, cxs[2], cy + 0.0, 0.7, 0.75), cone(OC, cxs[2] + 0.85, cy + 0.0, 0.85, 0.9))
        ar = VGroup(Arrow([cxs[2] - 1.7, cy + 0.95, 0], [cxs[2] - 0.8, cy + 0.95, 0], buff=0, color=OC, stroke_width=5, tip_length=0.18),
                    Arrow([cxs[2] + 1.7, cy + 0.95, 0], [cxs[2] + 0.8, cy + 0.95, 0], buff=0, color=OC, stroke_width=5, tip_length=0.18))
        l3 = T("crowding by Balanus", 26, OC).move_to([cxs[2], cy - 0.85, 0])
        qs = [T("?", 60, YELLOW, weight=BOLD).move_to([x + cw / 2 - 0.4, cy + ch / 2 - 0.4, 0]) for x in cxs]
        items = [(ic1, l1), (ic2, l2), (ic3, VGroup(l3, ar))]
        cues = ["longer time", "predators", "crowding"]
        for i in range(3):
            self.at(cues[i], 0.4)
            self.play(FadeIn(cards[i]), FadeIn(items[i][0], scale=0.6), run_time=0.8)
            self.play(FadeIn(items[i][1], shift=UP * 0.1), FadeIn(qs[i]), run_time=0.7)
            self.play(Indicate(items[i][0], scale_factor=1.12, color=TEXT), run_time=1.2)
        self.finish()


# -------------------------------------------------------------------------------------------------
def coin(r=0.42):
    face = Circle(radius=r, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.9)
    return VGroup(face, T("H", 26, BG, weight=BOLD))


class S04Split(SpokenScene):
    def construct(self):
        # zoom in from the shore: the shore fades and the patch grows from the place we looked
        rock, sea, tl = shore_base(self)
        t_cones = band(TC, TEAL_ROWS, 0.42, 0.5, 0.7, JIT)
        self.add(t_cones)
        parts = patch_world()
        pw = place(parts, 1.0, np.array([0, -0.45, 0]))
        pw.save_state()
        pw.scale(0.12).move_to([0, 2.0, 0]).set_opacity(0)
        self.at("Joseph Connell", 0.0)
        self.play(FadeOut(VGroup(rock, sea, tl, t_cones)), pw.animate.restore(), run_time=2.0)
        yr = T("Study published 1961", 26, TEXT).move_to([-4.2, -3.5, 0])
        self.play(FadeIn(yr), run_time=0.5)
        # breathe the oranges so the held frames are alive
        breathe(parts["ol"], 0.02, 1.8)
        breathe(parts["orr"], 0.02, 1.8, 1.0)
        self.at("changing", 0.2)
        self.play(Indicate(parts["orr"], color=OC, scale_factor=1.03), run_time=1.5)
        self.at("mapped", 0.2)
        self.play(FadeIn(parts["nums"], lag_ratio=0.15), Indicate(parts["tl"], color=TC, scale_factor=1.08), run_time=2.2)
        self.at("split each map", 0.2)
        self.play(Create(parts["div"]), run_time=1.6)
        self.at("coin toss", 0.2)
        c = coin().move_to([0, 3.15, 0])
        self.play(FadeIn(c, scale=0.5), run_time=0.5)
        self.play(c.animate.shift(UP * 0.5), rate_func=there_and_back, run_time=0.5)
        for _ in range(2):
            self.play(c.animate.stretch_to_fit_height(0.12), rate_func=there_and_back, run_time=0.3)
        self.at("chose one half", 0.2)
        lit = Rectangle(width=PW / 2, height=PH, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to([-PW / 4, -0.45, 0])
        lit.add_updater(lambda m, dt: m.set_fill(opacity=0.2 + 0.1 * np.sin(self.elapsed() * 3)))
        l1 = T("remove Balanus", 30, YELLOW, weight=BOLD).move_to([-2.9, 3.15, 0])
        l2 = T("untouched", 30, TEXT, weight=BOLD).move_to([2.9, 3.15, 0])
        self.play(FadeIn(lit), c.animate.move_to([-0.0, 3.15, 0]).scale(0.9), FadeIn(l1), run_time=1.0)
        self.play(FadeIn(l2), run_time=0.6)
        self.finish()


def patch_scene_base(scene, numbers=True, left_cleared=False, centre=np.array([0, -0.45, 0])):
    parts = patch_world()
    pw = place(parts, 1.0, centre)
    if left_cleared:
        parts["ol"].set_opacity(0)
    scene.add(pw)
    if not numbers:
        parts["nums"].set_opacity(0)
    breathe(parts["orr"], 0.02, 1.8, 1.0)
    if not left_cleared:
        breathe(parts["ol"], 0.02, 1.8)
    return parts


def half_labels(scene, lit=True):
    lit_r = Rectangle(width=PW / 2, height=PH, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to([-PW / 4, -0.45, 0])
    lit_r.add_updater(lambda m, dt: m.set_fill(opacity=0.2 + 0.1 * np.sin(scene.elapsed() * 3)))
    l1 = T("remove Balanus", 30, YELLOW, weight=BOLD).move_to([-2.9, 3.15, 0])
    l2 = T("untouched", 30, TEXT, weight=BOLD).move_to([2.9, 3.15, 0])
    scene.add(lit_r, l1, l2)
    scene.bring_to_back(lit_r)
    return lit_r, l1, l2


class S05Remove(SpokenScene):
    def construct(self):
        parts = patch_scene_base(self)
        lit, l1, l2 = half_labels(self)
        ol = parts["ol"]
        self.at("removed every", 0.2)
        order = sorted(range(len(ol)), key=lambda i: (-ol[i].get_center()[1]))
        # lift the oranges away one by one
        anims = [AnimationGroup(ol[i].animate.shift(UP * 0.9).set_opacity(0)) for i in order]
        for a in ol: a.clear_updaters()
        ol.clear_updaters()
        self.play(LaggedStart(*anims, lag_ratio=0.5), run_time=5.5)
        self.at("The other half", 0.1)
        self.play(Indicate(parts["orr"], color=OC, scale_factor=1.03), run_time=1.6)
        self.at("same height", 0.2)
        by = -3.05
        brace = VGroup(Line([-5.2, by, 0], [5.2, by, 0], color=TEXT, stroke_width=5), Line([-5.2, by, 0], [-5.2, by + 0.25, 0], color=TEXT, stroke_width=5),
                       Line([5.2, by, 0], [5.2, by + 0.25, 0], color=TEXT, stroke_width=5))
        txt = T("same height, same tide, same weather", 28, TEXT).move_to([0, -3.5, 0])
        self.play(Create(brace), run_time=1.0)
        self.play(FadeIn(txt, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06Recount(SpokenScene):
    def construct(self):
        parts = patch_scene_base(self, left_cleared=True)
        half_labels(self)
        by = -3.05
        brace = VGroup(Line([-5.2, by, 0], [5.2, by, 0], color=TEXT, stroke_width=5), Line([-5.2, by, 0], [-5.2, by + 0.25, 0], color=TEXT, stroke_width=5),
                       Line([5.2, by, 0], [5.2, by + 0.25, 0], color=TEXT, stroke_width=5))
        self.add(brace)
        self.at("came back", 0.2)
        cal = lambda n: VGroup(Rectangle(width=1.9, height=0.85, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1),
                               T(f"visit {n}", 28, TEXT, weight=BOLD)).move_to([0, 3.15, 0])
        c = cal(1)
        # the coin from the last scene turns into the calendar
        self.play(FadeIn(c), run_time=0.6)
        teal = parts["tl"]
        marks = VGroup()

        def visit(n):
            new = VGroup()
            for i, m in enumerate(teal):
                x, y = m.get_center()[:2]
                new.add(check(x - 0.45, y + 1.05))
            return new
        ticks = []
        for n in range(1, 4):
            if n > 1:
                self.play(Transform(c, cal(n)), run_time=0.4)
            ch = visit(n)
            if ticks:
                self.play(FadeOut(ticks[-1]), run_time=0.2)
            ticks.append(ch)
            self.play(LaggedStart(*[Create(k) for k in ch], lag_ratio=0.2), run_time=0.8)
            if n == 1:
                self.at("recounted", 0.3)
            self.play(Indicate(ch, color=GREEN, scale_factor=1.15), run_time=0.5)
        self.at("difference he intended", 0.2)
        lab = T("intended difference: Balanus present or removed", 28, YELLOW).move_to([0, -3.5, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.at("whether", 0.2)
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.04), Indicate(parts["orr"], color=OC, scale_factor=1.03), run_time=1.5)
        self.finish()


# -------------------------------------------------------------------------------------------------
SC = 0.72
SCENTRE = np.array([-2.7, 0.9, 0.0])
BAR_X = (3.4, 5.7)
BAR_BASE, BAR_H = -1.2, 3.3
UNDER = np.array([-2.7, -2.0, 0.0])        # the line of text under the small patch


def small_patch(scene):
    parts = patch_world()
    parts["nums"].set_opacity(0)
    parts["ol"].set_opacity(0)
    pw = place(parts, SC, SCENTRE)
    scene.add(pw)
    breathe(parts["orr"], 0.02, 1.8, 1.0)
    return parts, pw


def bars_empty(scene, with_q=True):
    fr = [survival_frame(x, BAR_BASE, 1.6, BAR_H) for x in BAR_X]
    labs = [lines_label(["cleared", "half"], 28, YELLOW, ORIGIN).move_to([BAR_X[0], BAR_BASE - 0.55, 0]), lines_label(["untouched", "half"], 28, TEXT, ORIGIN).move_to([BAR_X[1], BAR_BASE - 0.55, 0])]
    scene.add(*fr, *labs)
    return fr, labs


class S07Predict(SpokenScene):
    def construct(self):
        parts = patch_world()
        parts["nums"].set_opacity(0)
        parts["ol"].set_opacity(0)
        pw = place(parts, 1.0, np.array([0, -0.45, 0]))
        lit = Rectangle(width=PW / 2, height=PH, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to([-PW / 4, -0.45, 0])
        grp = VGroup(lit, pw)
        self.add(grp)
        self.at("Suppose", 0.0)
        self.play(grp.animate.scale(SC).move_to(SCENTRE), run_time=1.0)
        breathe(parts["orr"], 0.02, 1.8, 1.0)
        fr, labs = bars_empty(self)
        self.play(FadeIn(VGroup(*fr)), FadeIn(VGroup(*labs)), run_time=0.6)
        self.at("longer time underwater", 0.1)
        ic = drop_clock(1.6).move_to(SCENTRE)
        self.play(FadeIn(ic, scale=0.5), run_time=0.8)
        self.at("killed", 0.2)
        self.play(Indicate(parts["tl"], color=TC, scale_factor=1.1), run_time=1.2)
        self.at("did nothing", 0.2)
        self.play(Indicate(parts["orr"], color=OC, scale_factor=1.04), run_time=1.4)
        self.at("What would the cleared half", 0.2)
        q1 = T("?", 90, YELLOW, weight=BOLD).move_to(fr[0].get_center())
        self.play(FadeIn(q1, scale=1.4), Indicate(labs[0], color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("compared with", 0.2)
        q2 = T("?", 90, YELLOW, weight=BOLD).move_to(fr[1].get_center())
        self.play(FadeIn(q2, scale=1.4), run_time=0.8)
        self.play(q1.animate.shift(UP * 0.15), q2.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        parts, pw = small_patch(self)
        lit = Rectangle(width=PW / 2 * SC, height=PH * SC, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to(SCENTRE + [-PW / 4 * SC, 0, 0])
        fr, labs = bars_empty(self)
        ic = drop_clock(1.6).move_to(SCENTRE)
        grp = VGroup(pw, lit, *fr, *labs, ic)
        self.add(lit, ic)
        self.play(grp.animate.set_opacity(0.28), run_time=0.5)
        q = T("Better, worse, or the same?", 52, YELLOW, weight=BOLD).move_to([0, 0.9, 0])
        qb = Rectangle(width=q.width + 0.6, height=1.2, stroke_width=0, fill_color=BG, fill_opacity=0.8).move_to(q)
        cd = ValueTracker(1.0)
        c0 = np.array([0, -1.5, 0])
        ringc = always_redraw(lambda: Arc(radius=0.6, start_angle=PI / 2, angle=-TAU * max(cd.get_value(), 0.001), color=YELLOW, stroke_width=10).move_arc_center_to(c0))
        ringb = Circle(radius=0.6, color=GREY, stroke_width=4).move_to(c0)
        self.add(qb, q, ringb, ringc)
        self.play(cd.animate.set_value(0.0), run_time=4.4, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        parts, pw = small_patch(self)
        lit = Rectangle(width=PW / 2 * SC, height=PH * SC, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to(SCENTRE + [-PW / 4 * SC, 0, 0])
        fr, labs = bars_empty(self)
        ic = drop_clock(1.6).move_to(SCENTRE)
        self.add(lit, ic)
        self.at("immersion", 0.3)
        ghost = T("if immersion were the cause", 30, GREY).move_to(UNDER + UP * 0.3)
        gt = T("(schematic)", 24, GREY).move_to(UNDER + DOWN * 0.3)
        self.play(FadeIn(ghost), FadeIn(gt), run_time=0.8)
        self.at("both halves would", 0.2)
        gh = [Rectangle(width=1.6, height=1.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([x, BAR_BASE + 0.75, 0]) for x in BAR_X]
        self.play(*[GrowFromEdge(g, DOWN) for g in gh], run_time=1.6)
        self.play(Indicate(ic, scale_factor=1.08), run_time=1.5)
        self.at("That is not what Connell found", 0.2)
        crossm = cross_mark(SCENTRE[0], SCENTRE[1], RED, 0.9)
        h_hi, h_lo = 2.9, 0.7
        real = [Rectangle(width=1.6, height=h_hi, stroke_width=0, fill_color=TC, fill_opacity=0.95).move_to([BAR_X[0], BAR_BASE + h_hi / 2, 0]),
                Rectangle(width=1.6, height=h_lo, stroke_width=0, fill_color=TC, fill_opacity=0.95).move_to([BAR_X[1], BAR_BASE + h_lo / 2, 0])]
        self.play(FadeOut(ghost), FadeOut(gt), FadeOut(VGroup(*gh)), run_time=0.7)
        self.play(GrowFromEdge(real[0], DOWN), GrowFromEdge(real[1], DOWN), Create(crossm), ic.animate.set_opacity(0.4), run_time=2.0)
        self.at("kept free", 0.2)
        self.play(Indicate(parts["tl"], color=TC, scale_factor=1.12), Indicate(real[0], color=TC, scale_factor=1.05), run_time=1.6)
        self.at("survived well", 0.2)
        lab = lines_label(["removing Balanus", "helped Chthamalus"], 30, GREEN, ORIGIN).move_to(UNDER)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(real[0], color=GREEN, scale_factor=1.06), run_time=1.4)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S10How(SpokenScene):
    def construct(self):
        cw, ch, cy = 4.1, 4.4, 0.45
        cxs = [-4.3, 0.0, 4.3]
        gy = cy - 1.45
        panels = [RoundedRectangle(corner_radius=0.2, width=cw, height=ch, stroke_color=ROCK, stroke_width=4, fill_color=ROCK, fill_opacity=0.22).move_to([x, cy, 0]) for x in cxs]
        grounds = [Line([x - cw / 2 + 0.2, gy, 0], [x + cw / 2 - 0.2, gy, 0], color=TEXT, stroke_width=4) for x in cxs]
        tag_small = T("untouched half, close up", 30, TEXT).move_to([0, 3.35, 0])
        tracks = [ValueTracker(0.0) for _ in range(3)]
        t_s, t_u, t_c = tracks
        ease = lambda p: p * p * (3 - 2 * p)
        # smother: orange grows over the teal cone
        ts = cone(TC, cxs[0] + 0.45, gy, 1.0, 1.2)
        os_ = cone(OC, cxs[0], gy, 1.0, 1.0, 0.92)
        os_.add_updater(lambda m: m.become(cone(OC, cxs[0] - 1.0 + 0.9 * ease(t_s.get_value()), gy, 1.2 + 1.0 * ease(t_s.get_value()), 1.3 + 1.0 * ease(t_s.get_value()), 0.92)))
        # undercut: orange wedge slides under the teal cone and lifts it
        tu = cone(TC, cxs[1] - 0.4, gy, 1.1, 1.25)
        tu.add_updater(lambda m: m.become(cone(TC, cxs[1] - 0.4, gy + 0.6 * ease(t_u.get_value()), 1.1, 1.25)))
        ou = Polygon([0, 0, 0], [1, 0, 0], [0, 1, 0], stroke_color=OC, stroke_width=2, fill_color=OC, fill_opacity=0.95)

        def uw(m):
            p = ease(t_u.get_value())
            xr = cxs[1] + 1.8
            m.become(Polygon([xr, gy, 0], [xr, gy + 0.2 + 0.6 * p, 0], [xr - (0.3 + 1.9 * p), gy, 0], stroke_color=OC, stroke_width=2, fill_color=OC, fill_opacity=0.95))
        ou.add_updater(uw)
        # crush: two orange cones squeeze the teal
        tc_ = cone(TC, cxs[2], gy, 1.0, 1.2)
        tc_.add_updater(lambda m: m.become(cone(TC, cxs[2], gy, 1.0 * (1 - 0.35 * ease(t_c.get_value())), 1.2 * (1 + 0.25 * ease(t_c.get_value())))))
        oc1 = cone(OC, cxs[2] - 1.3, gy, 1.1, 1.2)
        oc2 = cone(OC, cxs[2] + 1.3, gy, 1.1, 1.2)
        oc1.add_updater(lambda m: m.become(cone(OC, cxs[2] - 1.3 + 0.8 * ease(t_c.get_value()), gy, 1.1, 1.2)))
        oc2.add_updater(lambda m: m.become(cone(OC, cxs[2] + 1.3 - 0.8 * ease(t_c.get_value()), gy, 1.1, 1.2)))
        self.add(*panels, *grounds, tag_small)
        self.at("watched how", 0.3)
        self.play(FadeIn(VGroup(ts, os_), shift=UP * 0.1), FadeIn(VGroup(tu, ou), shift=UP * 0.1), FadeIn(VGroup(tc_, oc1, oc2), shift=UP * 0.1), run_time=1.0)
        l1 = T("smother", 32, OC, weight=BOLD).move_to([cxs[0], cy - 1.95, 0])
        l2 = T("undercut", 32, OC, weight=BOLD).move_to([cxs[1], cy - 1.95, 0])
        l3 = T("crush", 32, OC, weight=BOLD).move_to([cxs[2], cy - 1.95, 0])
        self.at("growing", 0.2)
        self.play(t_s.animate.set_value(1.0), FadeIn(l1), run_time=1.2, rate_func=linear)
        self.at("undercut it", 0.2)
        self.play(t_u.animate.set_value(1.0), FadeIn(l2), run_time=0.9, rate_func=linear)
        self.at("crushed", 0.2)
        self.play(t_c.animate.set_value(1.0), FadeIn(l3), run_time=0.9, rate_func=linear)
        # keep the three actions looping so the frame is never frozen
        for t in tracks:
            t.set_value(1.0)
        self.at("interference competition", 0.3)
        tag = T("direct competition for space", 36, YELLOW, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), FadeOut(tag_small), run_time=0.9)
        self.play(*[t.animate.set_value(0.0) for t in tracks], run_time=1.2)
        self.at("one barnacle acting directly", 0.4)
        self.play(*[t.animate.set_value(1.0) for t in tracks], run_time=1.8)
        self.at("for space", 0.3)
        self.play(Indicate(tag, color=YELLOW, scale_factor=1.05), *[t.animate.set_value(0.0) for t in tracks], run_time=1.6)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S11Niche(SpokenScene):
    def construct(self):
        t_cones, o_cones, tlab, olab = shore_full(self, tide_labels=False, labels=False)
        self.at("So at Millport", 0.0)
        self.play(Indicate(o_cones, color=OC, scale_factor=1.02), run_time=1.5)
        self.at("lower limit", 0.2)
        line = Line([CX0 - 0.3, Y_BOUND - 0.05, 0], [CX1 + 0.4, Y_BOUND - 0.05, 0], color=OC, stroke_width=9)
        self.play(Create(line), run_time=1.2)
        self.at("could live", 0.3)
        fw = CX1 - CX0 + 0.6
        fund = DashedVMobject(Rectangle(width=fw, height=4.3, stroke_color=TC, stroke_width=6), num_dashes=70).move_to([(CX0 + CX1) / 2, 1.1, 0])
        fund_fill = Rectangle(width=fw, height=4.3, stroke_width=0, fill_color=TC, fill_opacity=0.12).move_to(fund)
        self.play(Create(fund), FadeIn(fund_fill), run_time=2.0)
        self.at("does live", 0.3)
        real = Rectangle(width=fw - 0.4, height=1.75, stroke_color=TC, stroke_width=7).move_to([(CX0 + CX1) / 2, 2.3, 0])
        self.play(Create(real), run_time=1.2)
        rlab = lines_label(["realized niche:", "where it does live,", "beside Balanus"], 24, TC, LEFT).move_to([-4.65, 2.3, 0])
        rlab.shift(RIGHT * (-6.55 - rlab.get_left()[0]))
        self.play(FadeIn(rlab, shift=RIGHT * 0.15), run_time=0.8)
        self.at("fundamental", 0.3)
        flab = lines_label(["fundamental niche:", "where it could live,", "with no competitors", "or enemies"], 24, TC, LEFT).move_to([-4.65, -0.1, 0])
        flab.shift(RIGHT * (-6.55 - flab.get_left()[0]))
        self.play(FadeIn(flab, shift=RIGHT * 0.15), Indicate(fund, color=TC, scale_factor=1.01), run_time=1.0)
        br = VGroup(Line([4.5, Y_BOUND - 0.15, 0], [4.5, -1.0, 0], color=OC, stroke_width=7), Line([4.3, Y_BOUND - 0.15, 0], [4.5, Y_BOUND - 0.15, 0], color=OC, stroke_width=7),
                    Line([4.3, -1.0, 0], [4.5, -1.0, 0], color=OC, stroke_width=7))
        bl = lines_label(["held out", "by Balanus"], 28, OC, LEFT).move_to([5.85, 0.1, 0])
        self.at("realized", 0.2)
        self.play(Create(br), FadeIn(bl, shift=LEFT * 0.15), run_time=1.2)
        self.play(Indicate(real, color=TC, scale_factor=1.02), run_time=1.5)
        self.finish()


# -------------------------------------------------------------------------------------------------
SCOT = [(-1.2, -3.2), (-0.2, -3.0), (0.8, -3.2), (1.4, -2.6), (1.2, -1.8), (1.8, -1.2), (1.6, -0.2), (2.0, 0.8), (1.2, 1.6), (1.0, 2.6), (0.2, 3.2),
        (-0.8, 3.0), (-1.4, 2.4), (-2.0, 2.0), (-1.8, 1.2), (-2.4, 0.6), (-1.6, 0.0), (-2.2, -0.6), (-1.6, -1.2), (-2.0, -1.9), (-1.5, -2.6)]


class S12Scope(SpokenScene):
    def construct(self):
        shore_full(self, tide_labels=True)
        shore_all = VGroup(*self.mobjects)
        cx = -0.4
        pts = [[x * 0.95 + cx, y * 0.95 + 0.0, 0] for x, y in SCOT]
        land = Polygon(*pts, stroke_color=TEXT, stroke_width=4, fill_color=ROCK, fill_opacity=0.4)
        pin_pos = np.array([cx - 1.45 * 0.95, -1.7 * 0.95, 0.0])
        pin = VGroup(Circle(radius=0.17, stroke_color=TC, stroke_width=4, fill_color=TC, fill_opacity=1), Line([0, -0.17, 0], [0, -0.55, 0], color=TC, stroke_width=5)).move_to(pin_pos + UP * 0.3)
        self.at("Keep the scope", 0.0)
        land.set_opacity(0)
        self.add(land)
        self.play(shore_all.animate.scale(0.06).move_to(pin_pos), land.animate.set_fill(ROCK, 0.4).set_stroke(TEXT, 4, 1.0), run_time=1.5)
        self.remove(shore_all)
        self.add(pin, schem(-5.9, -3.55))
        self.play(GrowFromCenter(pin), run_time=0.5)
        breathe(pin, 0.15, 3.0)
        land.tm = 0.0

        def glow(m, dt):
            m.tm += dt
            m.set_fill(ROCK, 0.4 + 0.18 * np.sin(1.8 * m.tm))
        land.add_updater(glow)
        ripple = Circle(radius=0.2, color=TC, stroke_width=5).move_to(pin_pos + UP * 0.3)
        ripple.tm = 0.0

        def rip(m, dt):
            m.tm += dt
            ph = (m.tm % 1.6) / 1.6
            m.become(Circle(radius=0.2 + 0.9 * ph, color=TC, stroke_width=5).move_to(pin_pos + UP * 0.3).set_stroke(opacity=1 - ph))
        ripple.add_updater(rip)
        self.add(ripple)
        l1 = T("one shore", 36, TC, weight=BOLD).move_to([pin_pos[0] - 2.7, pin_pos[1] + 0.2, 0])
        self.at("one shore", 0.3)
        self.play(FadeIn(l1, shift=RIGHT * 0.1), Indicate(pin, color=TC, scale_factor=1.3), run_time=0.8)
        self.at("one pair", 0.3)
        self.play(Indicate(pin, color=TC, scale_factor=1.3), run_time=0.9)
        self.at("one set of years", 0.3)
        self.play(Indicate(l1, color=TC, scale_factor=1.1), run_time=0.9)
        self.at("does not say", 0.3)
        others = [(-1.0, 1.5), (-0.2, 0.3), (0.4, 1.8), (-0.3, -0.9), (0.4, -2.0)]
        gp = VGroup(); qs = VGroup()
        for (x, y) in others:
            d = Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7).move_to([cx + x, y, 0])
            qm = T("?", 32, GREY, weight=BOLD).move_to([cx + x + 0.38, y + 0.1, 0])
            gp.add(d); qs.add(qm)
        self.play(LaggedStart(*[FadeIn(g, scale=0.5) for g in gp], lag_ratio=0.25), FadeIn(qs, lag_ratio=0.25), run_time=1.6)
        self.at("every coast", 0.0)
        ol = lines_label(["other shores:", "not tested here"], 34, GREY).move_to([4.6, 1.2, 0])
        self.play(FadeIn(ol, shift=LEFT * 0.15), run_time=0.9)
        self.at("strength", 0.2)
        d = lines_label(["strength:", "the design,", "not the", "generality"], 34, YELLOW, LEFT).move_to([4.6, -1.5, 0])
        self.play(FadeIn(d, shift=LEFT * 0.15), run_time=1.0)
        self.at("generality", 0.3)
        self.play(Indicate(d, color=YELLOW, scale_factor=1.05), run_time=1.2)
        self.play(Indicate(ol, color=GREY, scale_factor=1.05), run_time=1.2)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S13Rule(SpokenScene):
    def construct(self):
        sc = 0.75
        pc = np.array([-2.7, 0.9, 0.0])
        parts = patch_world()
        parts["nums"].set_opacity(0)
        pw = place(parts, sc, pc)
        self.add(pw)
        breathe(parts["orr"], 0.02, 1.8, 1.0)
        breathe(parts["ol"], 0.02, 1.8, 0.0)
        self.at("For a neighbor", 0.0)
        self.play(Indicate(parts["ol"], color=OC, scale_factor=1.04), Indicate(parts["orr"], color=OC, scale_factor=1.04), run_time=1.6)
        self.at("stays put", 0.3)
        self.play(Indicate(parts["tl"], color=TC, scale_factor=1.12), run_time=1.4)
        self.at("field test", 0.3)
        self.play(pw.animate.scale(1.03), rate_func=there_and_back, run_time=1.4)
        self.at("Remove it", 0.4)
        c = coin(0.4).move_to([-2.7, 3.35, 0])
        self.play(FadeIn(c, scale=0.5), run_time=0.3)
        self.play(c.animate.stretch_to_fit_height(0.12), rate_func=there_and_back, run_time=0.35)
        ol = parts["ol"]
        ol.clear_updaters()
        t1 = T("randomized removal", 28, YELLOW).move_to([0, -3.05, 0])
        self.play(LaggedStart(*[o.animate.shift(UP * 0.5).set_opacity(0) for o in ol], lag_ratio=0.1), FadeIn(t1), run_time=1.4)
        self.at("leave a matched half alone", 0.4)
        t2 = T("untouched comparison", 28, TEXT)
        t3 = T("controls", 28, GREEN)
        rowl = VGroup(t1.copy(), T("+", 28, TEXT), t2, T("+", 28, TEXT), t3).arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
        self.play(Transform(t1, rowl[0]), run_time=0.6)
        self.play(FadeIn(rowl[1]), FadeIn(t2), run_time=0.4)
        self.play(Indicate(parts["orr"], color=OC, scale_factor=1.03), run_time=1.5)
        self.at("If survival improves", 0.3)
        bx = (3.2, 5.4)
        bb = -0.9
        frs = [Rectangle(width=1.6, height=3.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([x, bb + 1.7, 0]) for x in bx]
        bl = [T("removed", 28, YELLOW).move_to([bx[0], bb - 0.35, 0]), T("untouched", 28, TEXT).move_to([bx[1], bb - 0.35, 0])]
        hh = [3.0, 1.0]
        rb = [Rectangle(width=1.6, height=h, stroke_width=0, fill_color=TC, fill_opacity=0.95).move_to([x, bb + h / 2, 0]) for x, h in zip(bx, hh)]
        title = T("survival", 30, TC, weight=BOLD).move_to([4.3, 3.0, 0])
        self.play(FadeIn(VGroup(*frs)), FadeIn(VGroup(*bl)), FadeIn(title), run_time=0.5)
        self.play(GrowFromEdge(rb[0], DOWN), GrowFromEdge(rb[1], DOWN), run_time=1.4)
        self.at("proper controls", 0.3)
        self.play(Transform(t2, rowl[2]), FadeIn(rowl[3]), FadeIn(rowl[4]), Indicate(rowl[4], color=GREEN, scale_factor=1.15), run_time=1.2)
        self.at("rule out", 0.2)
        self.play(pw.animate.scale(1.03), rate_func=there_and_back, run_time=1.6)
        self.at("neighbor was limiting", 0.2)
        self.play(Indicate(rb[0], color=GREEN, scale_factor=1.06), run_time=1.5)
        self.finish()


class S14End(EndCard):
    LINE = "Randomized, controlled removal: better survival is evidence the neighbour was limiting."
