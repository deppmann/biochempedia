"""One Tug, Many Jobs (water and life, film 1): one polar molecule explains dissolving, cohesion, adhesion.

COLOR MAP (same in every scene, film and figure)
  OXYGEN END = RED (delta minus)       HYDROGEN ENDS = HB blue (delta plus)
  COVALENT BOND = short solid light-grey bar      HYDROGEN BOND = dashed GOLD line
  liquid WATER = pale BLUE fill        OIL = pale GREEN droplet     CELLULOSE = light BROWN
  sodium = PURPLE, chloride = GREEN squares.  Nothing here is a molecular structure: blocks and cartoons.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HB = "#4A86FF"        # hydrogen end (blue)
NEUT = "#7C8594"      # neutral molecule
LG = "#C8CCD4"        # light grey for bars and readable labels
PURPLE = "#B58CD9"    # sodium
OILC = "#A9D98C"      # oil
BROWN = "#B07A4A"     # cellulose
BROWNL = "#E0B07C"    # cellulose label
PANEL = "#171b26"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def wobble(m, amp=0.06, rot=0.0, speed=1.0, seed=0.0):
    """Slow jostle driven by an updater: shifts/rotates by the CHANGE in offset so it composes with animations."""
    m._wt = float(seed) * 3.1
    m._wo = np.zeros(3)
    m._wr = 0.0

    def u(mob, dt):
        mob._wt += dt * speed
        t = mob._wt
        o = np.array([amp * np.sin(1.3 * t + seed), amp * np.cos(1.7 * t + 2 * seed), 0.0])
        mob.shift(o - mob._wo)
        mob._wo = o
        if rot:
            r = rot * np.sin(1.1 * t + seed * 1.7)
            mob.rotate(r - mob._wr)
            mob._wr = r
    m.add_updater(u)
    return m


def blk(w, h, color, fill, r=0.15, sw=3):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill)


def mol(s=1.0, charged=False, letters=False):
    """A water molecule: big body block (O) at the point of a wide V, two small tip blocks (H), grey bars between.
    .O .Hl .Hr are VGroup(rect, label); .bl .br are the covalent bars."""
    oc = RED if charged else NEUT
    hc = HB if charged else NEUT
    fo, fh = (0.85, 0.85) if charged else (0.45, 0.45)
    sw = max(2.0, 3 * s ** 0.5)
    O = VGroup(blk(1.2 * s, 1.0 * s, oc, fo, 0.15 * s, sw).move_to([0, -0.65 * s, 0]))
    Hl = VGroup(blk(0.8 * s, 0.8 * s, hc, fh, 0.12 * s, sw).move_to([-1.6 * s, 0.75 * s, 0]))
    Hr = VGroup(blk(0.8 * s, 0.8 * s, hc, fh, 0.12 * s, sw).move_to([1.6 * s, 0.75 * s, 0]))
    if letters:
        for b, t, sz in ((O, "O", 46), (Hl, "H", 38), (Hr, "H", 38)):
            b.add(T(t, size=max(22, sz * s), color=TEXT, weight=BOLD).move_to(b[0]))
    bw = max(3, 9 * s)
    bl = Line(O[0].get_center(), Hl[0].get_center(), color=LG, stroke_width=bw)
    br = Line(O[0].get_center(), Hr[0].get_center(), color=LG, stroke_width=bw)
    g = VGroup(bl, br, O, Hl, Hr)
    g.O, g.Hl, g.Hr, g.bl, g.br = O, Hl, Hr, bl, br
    return g


def charge_anims(m):
    return [m.O[0].animate.set_fill(RED, 0.85).set_stroke(RED),
            m.Hl[0].animate.set_fill(HB, 0.85).set_stroke(HB),
            m.Hr[0].animate.set_fill(HB, 0.85).set_stroke(HB)]


def hmid(m):
    return (m.Hl.get_center() + m.Hr.get_center()) / 2


def face(m, target, end="O"):
    """Rotate m about its centre so its O end (or its pair of H tips) points at target."""
    c = m.get_center()
    v = (m.O.get_center() - c) if end == "O" else (hmid(m) - c)
    d = np.array(target) - c
    m.rotate(np.arctan2(d[1], d[0]) - np.arctan2(v[1], v[0]), about_point=c)
    return m


def gline(a, b, trim=0.0, w=5, op=1.0):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    L = np.linalg.norm(d)
    if L < 1e-6:
        return VGroup()
    u = d / L
    p0, p1 = a + u * trim, b - u * trim
    if np.linalg.norm(p1 - p0) < 0.2:
        return VGroup()
    ln = DashedLine(p0, p1, color=GOLD, stroke_width=w, dash_length=0.14, dashed_ratio=0.55)
    ln.set_opacity(op)
    return ln


def lbl(text, pos, color=TEXT, size=32, weight=NORMAL):
    return T(text, size=size, color=color, weight=weight).move_to(pos)


def clock_of(scene):
    c = ValueTracker(0.0)
    c.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(c)
    return c


def stage(fill=0.14, color=BLUE, w=12.8, h=6.4, y=-0.3):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=fill).move_to([0, y, 0])


def strider_icon(x, ybody, yfoot, s=1.0):
    body = Ellipse(width=1.3 * s, height=0.42 * s, color=LG, fill_color=LG, fill_opacity=0.9).move_to([x, ybody, 0])
    head = Circle(radius=0.15 * s, color=LG, fill_color=LG, fill_opacity=0.9).move_to([x + 0.75 * s, ybody + 0.08 * s, 0])
    legs = VGroup()
    for fx in (-1.7, -1.1, -0.55, 0.55, 1.1, 1.7):
        legs.add(Line([x + 0.35 * np.sign(fx) * s, ybody - 0.1 * s, 0], [x + fx * s, yfoot, 0], color=LG, stroke_width=4))
    return VGroup(legs, body, head)


def fly_in(scene, mob, shift, angle=0.0, run_time=1.5):
    final = mob.copy()

    def f(m, a):
        m.become(final.copy().rotate(-(1 - a) * angle, about_point=final.get_center()).shift(shift * (1 - a)))
    scene.play(UpdateFromAlphaFunc(mob, f), run_time=run_time)


# ----- the crowd (scenes 5 and 6) ------------------------------------------------------------
def build_crowd(scene, G):
    rng = np.random.RandomState(7)
    mols, base = VGroup(), []
    for r in range(5):
        for c in range(6):
            p = np.array([-5.3 + 2.1 * c + (0.5 if r % 2 else 0) + rng.uniform(-.15, .15), -2.0 + 1.2 * r + rng.uniform(-.1, .1), 0])
            m = mol(0.38, charged=True).move_to(p).rotate(rng.uniform(0, TAU))
            wobble(m, amp=0.1, rot=0.14, speed=0.8, seed=r * 6 + c)
            mols.add(m)
            base.append(p)
    cands = []
    for i, p in enumerate(base):
        cands.append([j for j, q in enumerate(base) if j != i and 1.0 < np.linalg.norm(p - q) < 2.5])
    clock = clock_of(scene)

    def lines():
        g = VGroup()
        t = clock.get_value()
        gv = G.get_value()
        if gv < 0.02:
            return g
        for i, m in enumerate(mols):
            u = t * 0.55 + i * 0.37
            k = int(u)
            f = u - k
            al = np.sin(np.pi * f) ** 0.6 * gv
            if al < 0.06 or not cands[i]:
                continue
            j = cands[i][(k + i) % len(cands[i])]
            tip = (m.Hl if i % 2 else m.Hr).get_center()
            g.add(gline(tip, mols[j].O.get_center(), trim=0.3, w=4, op=al))
        return g
    return mols, always_redraw(lines)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Water and life"
    TITLE = "One Tug, Many Jobs"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        xs = [-4.6, 0.0, 4.6]
        YC = -0.4
        frames = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.2, height=5.0, stroke_color=GREY, stroke_width=3,
                                           fill_color=PANEL, fill_opacity=1).move_to([x, YC, 0]) for x in xs])
        # panel 1: pond + strider
        ysurf = YC - 0.5
        pond = Rectangle(width=4.2, height=ysurf - (YC - 2.5), stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([xs[0], (ysurf + YC - 2.5) / 2, 0])
        surf = Line([xs[0] - 2.1, ysurf, 0], [xs[0] + 2.1, ysurf, 0], color=BLUE, stroke_width=5)
        strider = always_redraw(lambda: strider_icon(xs[0], ysurf + 0.85 + 0.05 * np.sin(clock.get_value() * 2), ysurf - 0.02, 1.0))
        dimples = VGroup(*[ArcBetweenPoints([xs[0] + fx - 0.18, ysurf, 0], [xs[0] + fx + 0.18, ysurf, 0], angle=1.3, color=BLUE, stroke_width=4)
                           for fx in (-1.7, -1.1, -0.55, 0.55, 1.1, 1.7)])
        # panel 2: glass + towel
        gw, gtop, gbot = 2.3, YC + 1.0, YC - 2.3
        glass2 = VGroup(Line([xs[1] - gw / 2, gtop, 0], [xs[1] - gw / 2, gbot, 0]), Line([xs[1] - gw / 2, gbot, 0], [xs[1] + gw / 2, gbot, 0]),
                        Line([xs[1] + gw / 2, gbot, 0], [xs[1] + gw / 2, gtop, 0])).set_stroke(LG, 5)
        wl = gbot + 1.1
        water2 = Rectangle(width=gw - 0.1, height=1.1, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([xs[1], gbot + 0.55 + 0.02, 0])
        towel = Rectangle(width=0.75, height=3.6, stroke_color=BROWN, stroke_width=3, fill_color=BROWN, fill_opacity=0.9).move_to([xs[1], YC + 0.0, 0])
        towel.move_to([xs[1], YC - 0.0 + 0.2, 0])
        ttop = towel.get_top()[1]
        stain = Rectangle(width=0.75, height=ttop - 0.2 - wl, stroke_width=0, fill_color=BLUE, fill_opacity=0.75).move_to([xs[1], (ttop - 0.2 + wl) / 2, 0])
        # panel 3: glass + salt
        glass3 = glass2.copy().shift(RIGHT * (xs[2] - xs[1]))
        water3 = water2.copy().shift(RIGHT * (xs[2] - xs[1]))
        grains = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([xs[2] + dx, gtop + 0.35 + dy, 0])
                          for dx, dy in ((-0.5, 0.0), (0.0, 0.15), (0.5, 0.0), (-0.25, 0.4), (0.25, 0.4))])
        for gr in grains:
            wobble(gr, amp=0.03, speed=1.5, seed=gr.get_x())
        wobble(towel, amp=0.0, rot=0.0)
        q = T("?", size=150, color=GOLD, weight=BOLD).move_to([0, 3.0, 0])
        for fr in frames:
            fr.z_index = -2
        p1 = VGroup(pond, surf, strider)
        p2 = VGroup(water2, towel, glass2)
        p3 = VGroup(water3, glass3)
        self.play(LaggedStart(FadeIn(frames[0]), FadeIn(frames[1]), FadeIn(frames[2]), lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3), run_time=0.8)
        self.at("three puzzles")
        self.play(GrowFromCenter(q), run_time=0.8)
        self.at("An insect")
        self.play(FadeIn(dimples), run_time=0.6)
        self.wait(0.4)
        self.play(Indicate(strider, color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("a paper towel")
        self.play(FadeIn(grains), run_time=0.3)
        stain.set_opacity(0.8)
        self.add(stain)
        self.play(GrowFromEdge(stain, DOWN), run_time=2.4, rate_func=linear)
        self.at("salt vanishes")
        self.play(*[gr.animate.shift(DOWN * (1.6 + 0.12 * i)) for i, gr in enumerate(grains)], run_time=1.0)
        self.play(*[gr.animate.scale(0.05).set_opacity(0) for gr in grains], run_time=1.2)
        self.wait(0.4)
        self.play(FadeOut(VGroup(frames, p1, p2, p3, stain, dimples, grains, q), scale=1.6), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
M0 = np.array([0.0, -0.3, 0.0])
SC = 1.7


class S02Molecule(SpokenScene):
    def construct(self):
        m = mol(SC, letters=True).move_to(M0)
        wobble(m, amp=0.04, rot=0.02, speed=0.8, seed=1)
        O, Hl, Hr = m.O, m.Hl, m.Hr
        self.at("water molecule")
        O_final = O.copy()
        O.shift(DOWN * 4)
        self.add(O)
        self.play(O.animate.shift(UP * 4), run_time=1.4)
        self.at("one oxygen atom")
        o_lbl = lbl("oxygen atom", O.get_center() + DOWN * 1.3, TEXT, 34)
        self.play(FadeIn(o_lbl, shift=UP * 0.1), run_time=0.5)
        self.at("two hydrogen atoms")
        h_lbl = lbl("two hydrogen atoms", [0, 3.2, 0], TEXT, 34)
        Hl_f, Hr_f = Hl.copy(), Hr.copy()
        Hl.shift(UP * 3 + LEFT * 2)
        Hr.shift(UP * 3 + RIGHT * 2)
        self.add(Hl, Hr)
        self.play(Hl.animate.shift(DOWN * 3 + RIGHT * 2), Hr.animate.shift(DOWN * 3 + LEFT * 2), FadeIn(h_lbl), run_time=1.5)
        self.at("Each hydrogen shares electrons")
        self.play(FadeOut(h_lbl), run_time=0.3)
        self.play(GrowFromPoint(m.bl, O.get_center()), GrowFromPoint(m.br, O.get_center()), run_time=1.6)
        self.add(m.bl, m.br)
        m.bl.set_z_index(-1)
        m.br.set_z_index(-1)
        self.at("covalent bond")
        cov = lbl("covalent bond: shared electrons", [0, 3.2, 0], LG, 34)
        self.play(FadeIn(cov, shift=DOWN * 0.1), Indicate(m.bl, color=TEXT, scale_factor=1.15), Indicate(m.br, color=TEXT, scale_factor=1.15), run_time=1.4)
        self.at("wide letter v")
        vee = VMobject().set_points_as_corners([Hl.get_center(), O.get_center(), Hr.get_center()]).set_stroke(TEXT, 14, opacity=0.35)
        vee.set_z_index(-2)
        self.play(Create(vee), run_time=1.2)
        self.play(Rotate(VGroup(m, vee), angle=0.22, about_point=m.get_center()), run_time=0.8)
        self.play(Rotate(VGroup(m, vee), angle=-0.22, about_point=m.get_center()), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Charges(SpokenScene):
    def construct(self):
        m = mol(SC, letters=True).move_to(M0)
        wobble(m, amp=0.04, rot=0.02, speed=0.8, seed=1)
        cloud = Ellipse(width=7.4, height=3.6, stroke_width=0, fill_color=LG, fill_opacity=0.22).move_to(M0)
        cloud.set_z_index(-1)
        self.add(m)
        self.at("Oxygen pulls the shared electrons closer")
        self.play(FadeIn(cloud), run_time=0.8)
        self.at("pulls the shared")
        tgt = Ellipse(width=2.6, height=1.9, stroke_width=0, fill_color=LG, fill_opacity=0.5).move_to(m.O.get_center())
        tgt.set_z_index(-1)
        self.play(Transform(cloud, tgt), run_time=1.8)
        self.at("the oxygen end becomes")
        self.play(m.O[0].animate.set_fill(RED, 0.85).set_stroke(RED), run_time=1.0)
        self.at("slightly negative")
        neg = lbl("δ−  slightly negative", m.O.get_center() + DOWN * 1.45, RED, 34, BOLD)
        self.play(FadeIn(neg, shift=UP * 0.1), run_time=0.5)
        self.at("Each hydrogen end becomes")
        self.play(m.Hl[0].animate.set_fill(HB, 0.85).set_stroke(HB), m.Hr[0].animate.set_fill(HB, 0.85).set_stroke(HB), run_time=1.0)
        self.at("slightly positive")
        pos = lbl("slightly positive", [0, 3.15, 0], HB, 34, BOLD)
        dl = lbl("δ+", m.Hl.get_center() + UP * 1.1, HB, 46, BOLD)
        dr = lbl("δ+", m.Hr.get_center() + UP * 1.1, HB, 46, BOLD)
        self.play(FadeIn(pos, shift=DOWN * 0.1), FadeIn(dl), FadeIn(dr), run_time=0.6)
        self.at("A molecule with charged ends")
        net = lbl("net charge: 0", [5.0, -2.9, 0], LG, 30)
        self.play(FadeIn(net), run_time=0.5)
        self.at("polar")
        pol = lbl("polar", [5.3, 0.3, 0], TEXT, 60, BOLD)
        self.play(Write(pol), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Hbond(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        big = mol(SC, charged=True, letters=True).move_to(M0)
        self.add(big)
        s = 1.05
        C1 = np.array([-3.5, 0.0, 0])
        m1 = mol(s, charged=True, letters=True).move_to(C1)
        self.play(ReplacementTransform(big, m1), run_time=1.0)
        wobble(m1, amp=0.05, rot=0.02, speed=0.8, seed=2)
        self.at("Bring in a neighbor")
        m2 = mol(s, charged=True, letters=True).move_to(ORIGIN)
        m2.rotate(0.95, about_point=ORIGIN)
        T0 = m1.O.get_center() + np.array([2.5, 0.75, 0])
        m2.shift(T0 - m2.Hl.get_center())
        fly_in(self, m2, RIGHT * 6.0 + UP * 0.8, angle=1.2, run_time=2.0)
        wobble(m2, amp=0.05, rot=0.02, speed=0.8, seed=5)
        self.at("Opposite charges attract")
        self.play(Indicate(m2.Hl[0], color=HB, scale_factor=1.25), Indicate(m1.O[0], color=RED, scale_factor=1.25), run_time=1.4)
        self.at("the blue end of one molecule")
        self.play(Indicate(m2.Hl[0], color=TEXT, scale_factor=1.3), run_time=1.0)
        self.at("the red end")
        self.play(Indicate(m1.O[0], color=TEXT, scale_factor=1.3), run_time=1.0)
        line = always_redraw(lambda: gline(m2.Hl.get_center(), m1.O.get_center(), trim=0.55, w=7))
        self.at("hydrogen bond")
        self.add(line)
        self.wait(0.4)
        mid = (m2.Hl.get_center() + m1.O.get_center()) / 2
        tag = lbl("hydrogen bond: between molecules", [0.5, -2.75, 0], GOLD, 34, BOLD)
        ptr = Line(tag.get_top() + UP * 0.05, mid + DOWN * 0.15, color=GOLD, stroke_width=3)
        self.play(FadeIn(tag), Create(ptr), run_time=0.8)
        self.at("dashed gold line")
        self.wait(0.6)
        self.play(Indicate(m1.bl, color=TEXT, scale_factor=1.2), Indicate(m2.br, color=TEXT, scale_factor=1.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Crowd(SpokenScene):
    def construct(self):
        G = ValueTracker(0.0)
        mols, lines = build_crowd(self, G)
        self.at("Liquid water holds")
        self.play(LaggedStart(*[FadeIn(m) for m in mols], lag_ratio=0.04), run_time=2.4)
        self.add(lines)
        self.at("Gold lines snap on")
        self.play(G.animate.set_value(1.0), run_time=0.6)
        gl = lbl("gold lines break and re-form", [-3.2, -3.5, 0], GOLD, 32, BOLD)
        self.at("break")
        self.play(FadeIn(gl), run_time=0.5)
        self.at("gray bonds inside each molecule")
        gr = lbl("grey bars stay", [4.0, -3.5, 0], LG, 32, BOLD)
        self.play(FadeIn(gr), *[Indicate(mols[i].bl, color=TEXT, scale_factor=1.5) for i in (3, 8, 13, 17, 22, 26)],
                  *[Indicate(mols[i].br, color=TEXT, scale_factor=1.5) for i in (3, 8, 13, 17, 22, 26)], run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
PANEL_X = [-4.4, 0.0, 4.4]
PANEL_Y = -1.3


def panels():
    return VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.0, height=3.4, stroke_color=BLUE, stroke_width=3,
                                     fill_color=PANEL, fill_opacity=1).move_to([x, PANEL_Y, 0]) for x in PANEL_X])


class S06Rule(SpokenScene):
    def construct(self):
        G = ValueTracker(1.0)
        mols, lines = build_crowd(self, G)
        self.add(mols, lines)
        self.at("Here is the one idea")
        self.wait(0.5)
        self.at("Water's charged ends tug on its neighbors")
        self.play(mols.animate.set_opacity(0.25), G.animate.set_value(0.3), run_time=1.0)
        arrow = Arrow([-6.0, 0.2, 0], [6.0, 0.2, 0], buff=0, color=GOLD, stroke_width=26, max_tip_length_to_length_ratio=0.12,
                      max_stroke_width_to_length_ratio=40)
        l1 = T("Water's charged ends tug on", size=40, color=TEXT)
        l2 = T("neighbors, ions and polar molecules", size=40, color=TEXT)
        sent = VGroup(l1, l2).arrange(DOWN, buff=0.15).move_to([0, 2.9, 0])
        self.play(GrowArrow(arrow), Write(l1), run_time=2.0)
        self.at("on ions")
        self.play(Write(l2), run_time=2.6)
        self.play(arrow.animate.set_opacity(0.35), run_time=0.8)
        self.at("Now watch it do three jobs")
        self.play(FadeOut(mols), G.animate.set_value(0.0), FadeOut(arrow), run_time=0.6)
        self.remove(lines)
        ps = panels()
        nums = VGroup(*[T(str(i + 1), size=64, color=GOLD, weight=BOLD).move_to(ps[i]) for i in range(3)])
        for p in ps:
            p.shift(DOWN * 4)
        self.add(ps)
        self.play(*[p.animate.shift(UP * 4) for p in ps], run_time=1.4)
        self.play(FadeIn(nums), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def crystal(origin=(-3.2, -0.8), side=0.8, signs=True):
    sq = {}
    g = VGroup()
    for i in range(4):
        for j in range(4):
            na = (i + j) % 2 == 0
            c = PURPLE if na else GREEN
            p = np.array([origin[0] - 1.6 + side / 2 + side * i, origin[1] - 1.6 + side / 2 + side * j, 0])
            b = VGroup(blk(side * 0.94, side * 0.94, c, 0.8, 0.08, 2).move_to(p))
            if signs:
                b.add(T("+" if na else "−", size=34, color=BG, weight=BOLD).move_to(p))
            sq[(i, j)] = b
            g.add(b)
    return g, sq


class S07Salt(SpokenScene):
    def construct(self):
        ps = panels()
        nums = VGroup(*[T(str(i + 1), size=64, color=GOLD, weight=BOLD).move_to(ps[i]) for i in range(3)])
        self.add(ps, nums)
        st = stage()
        self.at("Job one is dissolving")
        badge = lbl("Job 1: dissolving", [-4.3, 3.4, 0], GOLD, 36, BOLD)
        self.play(FadeOut(ps[1]), FadeOut(ps[2]), FadeOut(nums), Transform(ps[0], st), FadeIn(badge), run_time=1.6)
        # water molecules around the crystal
        origin = (-3.2, -0.9)
        side = 0.8
        cry, sq = crystal(origin, side)
        s = 0.38
        top_ions = [(1, 3), (3, 3)]       # sodium
        right_ions = [(3, 0), (3, 2)]     # chloride
        waters = []
        pairs = []
        for (i, j) in top_ions:
            ion = sq[(i, j)]
            c = ion.get_center() + UP * 1.0
            m = mol(s, charged=True).move_to(c).rotate(0.7 * (1 if i == 1 else -1))
            waters.append(m)
            pairs.append((ion, m, "O"))
        for (i, j) in right_ions:
            ion = sq[(i, j)]
            c = ion.get_center() + RIGHT * 1.35
            m = mol(s, charged=True).move_to(c).rotate(-0.9)
            waters.append(m)
            pairs.append((ion, m, "H"))
        extra = [(-0.4, 2.0), (1.6, 0.9), (2.2, -1.6), (1.0, -2.2), (-5.9, 1.5), (-5.9, -1.9), (0.4, -0.9), (5.4, -2.0)]
        rng = np.random.RandomState(3)
        for (x, y) in extra:
            m = mol(s, charged=True).move_to([x, y, 0]).rotate(rng.uniform(0, TAU))
            waters.append(m)
        for k, m in enumerate(waters):
            wobble(m, amp=0.09, rot=0.12, speed=0.9, seed=k + 1)
        wg = VGroup(*waters)
        self.at("Salt is made of")
        self.play(LaggedStart(*[FadeIn(w) for w in waters], lag_ratio=0.08), run_time=1.6)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in cry], lag_ratio=0.04), run_time=1.6)
        for b in cry:
            wobble(b, amp=0.015, speed=2.0, seed=b.get_x() + b.get_y())
        self.at("positive sodium")
        sodium_leg = VGroup(blk(0.5, 0.5, PURPLE, 0.8, 0.08, 2), T("sodium (+)", size=32, color=PURPLE, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([4.2, 1.9, 0])
        chl_leg = VGroup(blk(0.5, 0.5, GREEN, 0.8, 0.08, 2), T("chloride (−)", size=32, color=GREEN, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([4.2, 1.1, 0])
        self.play(FadeIn(sodium_leg), *[Indicate(sq[k], color=PURPLE, scale_factor=1.15) for k in sq if (k[0] + k[1]) % 2 == 0], run_time=1.2)
        self.at("negative chloride")
        self.play(FadeIn(chl_leg), *[Indicate(sq[k], color=GREEN, scale_factor=1.15) for k in sq if (k[0] + k[1]) % 2 == 1], run_time=1.2)
        self.at("Water's red ends face each sodium")
        anims = []
        for (ion, m, end) in pairs:
            if end == "O":
                c = m.get_center()
                v = m.O.get_center() - c
                d = ion.get_center() - c
                anims.append(Rotate(m, angle=np.arctan2(d[1], d[0]) - np.arctan2(v[1], v[0]), about_point=c))
        self.play(*anims, run_time=1.6)
        self.at("its blue ends face each chloride")
        anims = []
        for (ion, m, end) in pairs:
            if end == "H":
                c = m.get_center()
                v = hmid(m) - c
                d = ion.get_center() - c
                anims.append(Rotate(m, angle=np.arctan2(d[1], d[0]) - np.arctan2(v[1], v[0]), about_point=c))
        self.play(*anims, run_time=1.6)
        self.at("That pull of opposite charges")
        arrows = []
        for (ion, m, end) in pairs:
            d = m.get_center() - ion.get_center()
            u = d / np.linalg.norm(d)
            a = Arrow(ion.get_center() + u * 0.42, ion.get_center() + u * 0.95, buff=0, color=TEXT, stroke_width=5,
                      max_tip_length_to_length_ratio=0.5)
            arrows.append(a)
        tag = lbl("pull of opposite charges (not a hydrogen bond)", [0.8, -3.2, 0], TEXT, 28)
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(tag), run_time=1.0)
        self.at("lifts each ion off the crystal")
        anims = []
        for k, ((ion, m, end), a) in enumerate(zip(pairs, arrows)):
            d = m.get_center() - ion.get_center()
            u = d / np.linalg.norm(d)
            sh = u * (0.55 if end == "O" else 1.6)
            ring = Circle(radius=0.75, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.15).move_to((ion.get_center() + m.get_center()) / 2)
            ring.set_z_index(-1)
            self.add(ring)
            grp = VGroup(ion, m, a, ring)
            anims.append(grp.animate(rate_func=smooth).shift(sh))
        self.play(LaggedStart(*anims, lag_ratio=0.25), run_time=2.6)
        self.play(FadeOut(tag), run_time=0.4)
        self.at("So water is a solvent")
        solv = lbl("solvent", [4.3, -0.6, 0], GOLD, 60, BOLD)
        self.play(Write(solv), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Oil(SpokenScene):
    def construct(self):
        st = stage()
        badge = lbl("Job 1: dissolving", [-4.3, 3.4, 0], GOLD, 36, BOLD)
        self.add(st, badge)
        s = 0.3
        center = np.array([0.0, -0.3, 0.0])
        R = 2.3
        ring, rl = [], []
        for k in range(8):
            ang = TAU * k / 8 + 0.2
            p = center + np.array([1.55 * R * np.cos(ang), 0.95 * R * np.sin(ang) * 1.0, 0])
            p = center + np.array([2.2 * np.cos(ang) * 1.0, 2.2 * np.sin(ang), 0])
            m = mol(s, charged=True).move_to(p).rotate(ang + 0.3)
            ring.append(m)
        outer = [(-5.6, 2.1), (5.6, 2.1), (-5.6, -2.7), (5.6, -2.7), (-5.2, -0.3), (5.2, -0.3), (-3.6, -2.9), (3.6, -2.9)]
        rng = np.random.RandomState(11)
        others = [mol(s, charged=True).move_to([x, y, 0]).rotate(rng.uniform(0, TAU)) for x, y in outer]
        for k, m in enumerate(ring + others):
            wobble(m, amp=0.08, rot=0.1, speed=0.9, seed=k + 3)
        self.play(LaggedStart(*[FadeIn(m) for m in ring + others], lag_ratio=0.05), run_time=1.4)
        self.at("Now add some oil")
        drop = VGroup(Circle(radius=1.1, stroke_color=OILC, stroke_width=4, fill_color=OILC, fill_opacity=0.55),
                      T("mostly", size=30, color=TEXT, weight=BOLD).move_to([0, 0.28, 0]),
                      T("nonpolar", size=30, color=TEXT, weight=BOLD).move_to([0, -0.28, 0])).move_to(center)
        body = drop[0]
        txt = drop[1:]
        body.shift(UP * 2.4)
        self.add(body)
        self.play(body.animate.shift(DOWN * 2.4), run_time=1.5, rate_func=rush_from)
        wobble(body, amp=0.04, speed=1.0, seed=9)
        self.at("Oil molecules are mostly")
        txt.shift(RIGHT * 0)
        self.play(FadeIn(txt), run_time=0.6)
        for t_ in txt:
            wobble(t_, amp=0.04, speed=1.0, seed=9)
        self.at("Water molecules tug on each other")
        turns = [Rotate(m, angle=0.5 * (1 if k % 2 else -1), about_point=m.get_center()) for k, m in enumerate(ring)]
        self.play(*turns, run_time=1.2)
        links = always_redraw(lambda: VGroup(*[gline(ring[k].get_center(), ring[(k + 1) % 8].get_center(), trim=0.45, w=6) for k in range(8)]))
        self.add(links)
        self.wait(0.8)
        self.at("so the oil stays in its own drop")
        self.play(*[m.animate.shift(-(m.get_center() - center) * 0.1) for m in ring], Indicate(body, color=OILC, scale_factor=1.06), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
Y0 = -0.2


def surf_y(x, d):
    return Y0 - 0.55 * d * np.exp(-(x / 1.7) ** 2)


class S09Surface(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        d = ValueTracker(0.0)
        st = stage(fill=0.04)
        badge = lbl("Job 2", [-5.6, 3.4, 0], GOLD, 36, BOLD)
        self.add(st)
        # water body
        def water_poly():
            xs = np.linspace(-6.4, 6.4, 70)
            t = clock.get_value()
            pts = [[x, surf_y(x, d.get_value()) + 0.03 * np.sin(1.2 * x + 1.5 * t), 0] for x in xs]
            poly = Polygon(*pts, [6.4, -3.5, 0], [-6.4, -3.5, 0], stroke_width=0, fill_color=BLUE, fill_opacity=0.3)
            top = VMobject().set_points_as_corners(pts).set_stroke(BLUE, 6)
            return VGroup(poly, top)
        wat = always_redraw(water_poly)
        self.add(wat)
        rows = [(-0.65, 0.0), (-1.5, 0.57), (-2.35, 0.0)]
        mols_rows = []
        allm = VGroup()
        for r, (y, off) in enumerate(rows):
            row = []
            for c in range(11 if off == 0 else 10):
                x = -5.7 + 1.14 * c + off
                m = mol(0.26, charged=True).move_to([x, y, 0])
                m._bx, m._by, m._row = x, y, r
                m._ph = 0.0
                row.append(m)
                allm.add(m)
            mols_rows.append(row)

        def settle(m, dt=0):
            m._ph += dt
            depth = d.get_value() * [1.0, 0.7, 0.45][m._row]
            tx = m._bx
            ty = m._by - 0.55 * depth * np.exp(-(m._bx / 1.7) ** 2) + 0.03 * np.sin(1.2 * m._bx + 1.5 * clock.get_value()) + 0.025 * np.sin(2 * clock.get_value() + m._bx)
            m.shift(np.array([tx, ty, 0]) - m.get_center())
        for m in allm:
            m.add_updater(settle)
        self.add(allm)
        self.play(FadeIn(allm), run_time=0.8)
        self.at("Job two is sticking to itself")
        self.play(FadeIn(badge), run_time=0.5)
        top = mols_rows[0]
        self.at("called cohesion")
        links = always_redraw(lambda: VGroup(
            *[gline(top[k].get_center(), top[k + 1].get_center(), trim=0.3, w=5) for k in range(len(top) - 1)],
            *[gline(top[k].get_center(), mols_rows[1][k - 1].get_center(), trim=0.3, w=5) for k in range(1, len(top) - 1, 2) if k - 1 < len(mols_rows[1])]))
        coh = lbl("cohesion", [-4.6, 2.4, 0], GOLD, 40, BOLD)
        self.add(links)
        self.play(FadeIn(coh), run_time=1.0)
        self.at("At the surface")
        self.wait(0.2)
        self.at("pull each molecule sideways and down")
        arrs = VGroup()
        for k in (1, 3, 5, 7, 9):
            m = top[k]
            for off in (LEFT * 0.62, RIGHT * 0.62, DOWN * 0.5):
                a = Arrow(ORIGIN, off * 0.9, buff=0, color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.45)
                a.move_to(m.get_center() + off * 1.05 + UP * 0.02)
                a._m, a._off = m, off * 1.05

                def fol(mob, dt):
                    mob.move_to(mob._m.get_center() + mob._off)
                a.add_updater(fol)
                arrs.add(a)
        self.play(FadeIn(arrs), run_time=1.2)
        self.at("So the surface resists")
        def build_strider():
            dv = d.get_value()
            yb = surf_y(0, dv) + 1.3
            body = Ellipse(width=1.5, height=0.5, color=LG, fill_color=LG, fill_opacity=0.95).move_to([0, yb, 0])
            head = Circle(radius=0.17, color=LG, fill_color=LG, fill_opacity=0.95).move_to([0.85, yb + 0.1, 0])
            legs = VGroup()
            for fx in (-2.0, -1.3, -0.65, 0.65, 1.3, 2.0):
                legs.add(Line([0.4 * np.sign(fx), yb - 0.1, 0], [fx, surf_y(fx, dv) + 0.04, 0], color=LG, stroke_width=5))
            return VGroup(legs, body, head)
        strider = always_redraw(build_strider)
        self.add(strider)
        self.play(d.animate.set_value(1.0), run_time=2.6, rate_func=smooth)
        self.at("That is surface tension")
        stn = lbl("surface tension", [4.2, 2.4, 0], GOLD, 40, BOLD)
        self.play(FadeIn(stn), run_time=0.6)
        self.at("not a skin")
        skin = lbl("skin", [4.2, 1.5, 0], LG, 40)
        cross = Line(skin.get_left() + LEFT * 0.15, skin.get_right() + RIGHT * 0.15, color=RED, stroke_width=8)
        self.play(FadeIn(skin), run_time=0.4)
        self.play(Create(cross), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
POOLY = -1.5


def towel(P, A, C, H, t=0.0, pw=5.0):
    """Static build of picture 3 (cellulose strand in water). P patches, A adhesion lines, C cohesion lines, H climb 0..1."""
    g = VGroup()
    pts = [[x, POOLY + 0.05 * np.sin(1.3 * x + 1.6 * t), 0] for x in np.linspace(-pw, pw, 40)]
    g.add(Polygon(*pts, [pw, -3.5, 0], [-pw, -3.5, 0], stroke_width=0, fill_color=BLUE, fill_opacity=0.3))
    g.add(VMobject().set_points_as_corners(pts).set_stroke(BLUE, 5))
    top = POOLY + (2.1 - POOLY) * H + 0.05 * np.sin(2 * t)
    if H > 0.01:
        for sx in (-1, 1):
            g.add(Rectangle(width=0.9, height=top - POOLY, stroke_width=0, fill_color=BLUE, fill_opacity=0.5)
                  .move_to([sx * 0.95, (top + POOLY) / 2, 0]))
    g.add(blk(1.0, 5.6, BROWN, 0.95, 0.1, 3).move_to([0, 0.0, 0]))
    ys = [-1.1 + 1.1 * k for k in range(4)]
    if P > 0.01:
        for k in range(7):
            for sx in (-1, 1):
                c = RED if (k + (sx > 0)) % 2 == 0 else HB
                g.add(Square(side_length=0.22, stroke_width=0, fill_color=c, fill_opacity=P).move_to([sx * 0.5, -1.1 + 0.55 * k, 0]))
    ms = []
    for k, y in enumerate(ys):
        op = float(np.clip((top - (y - 0.3)) / 0.6, 0, 1))
        for sx in (-1, 1):
            if op <= 0.02:
                continue
            m = mol(0.22, charged=True).move_to([sx * 1.0, y, 0]).rotate(-sx * PI / 2)
            m.set_opacity(op)
            g.add(m)
            ms.append((k, sx, m, op))
    for (k, sx, m, op) in ms:
        if A > 0.02:
            g.add(gline(m.get_center(), [sx * 0.5, y_patch(k), 0], trim=0.0, w=5, op=A * op))
        if C > 0.02:
            for (k2, sx2, m2, op2) in ms:
                if sx2 == sx and k2 == k + 1:
                    g.add(gline(m.get_center(), m2.get_center(), trim=0.3, w=5, op=C * min(op, op2)))
    return g


def y_patch(k):
    return -1.1 + 0.55 * (2 * k)


class S10Towel(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        P, A, C, Hh = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        # carry the water from picture 2: same stage outline
        st = stage(fill=0.04)
        pic = always_redraw(lambda: towel(P.get_value(), A.get_value(), C.get_value(), Hh.get_value(), clock.get_value()))
        badge = lbl("Job 3", [-5.6, 3.4, 0], GOLD, 36, BOLD)
        self.add(st, pic)
        self.at("Job three is sticking to other things")
        self.play(FadeIn(badge), run_time=0.6)
        self.at("Paper is made of cellulose fibers")
        self.wait(0.2)
        self.at("cellulose fibers")
        cl = lbl("cellulose fibers", [3.6, 1.9, 0], BROWNL, 38, BOLD)
        cptr = Line(cl.get_left() + LEFT * 0.1, [0.62, 1.9, 0], color=BROWNL, stroke_width=3)
        self.play(FadeIn(cl), Create(cptr), run_time=0.8)
        self.at("with many polar parts")
        pl = lbl("polar parts", [-3.8, 2.4, 0], TEXT, 38, BOLD)
        pptr = Line(pl.get_right() + RIGHT * 0.1, [-0.6, 1.2, 0], color=TEXT, stroke_width=3)
        self.play(P.animate.set_value(1.0), FadeOut(cl), FadeOut(cptr), run_time=1.2)
        self.play(FadeIn(pl), Create(pptr), run_time=0.8)
        self.at("Water clings to them")
        self.play(Hh.animate.set_value(0.3), A.animate.set_value(1.0), FadeOut(pl), FadeOut(pptr), run_time=1.6)
        self.at("that is adhesion")
        ad = lbl("adhesion", [-4.1, -0.1, 0], GOLD, 40, BOLD)
        self.play(FadeIn(ad), run_time=0.6)
        self.at("Each climbing molecule pulls its neighbors")
        self.play(Hh.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        self.at("by cohesion")
        co = lbl("cohesion", [4.1, 0.6, 0], GOLD, 40, BOLD)
        self.play(C.animate.set_value(1.0), FadeIn(co), run_time=1.0)
        self.at("capillary action")
        cap = lbl("capillary action", [0, 3.2, 0], TEXT, 46, BOLD)
        self.play(FadeOut(ad), FadeOut(co), FadeIn(cap), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def leg_with_hairs(center, t_get=None, length=6.0, ang=-0.95):
    """A magnified strider leg: a thick grey stalk with fine hairs; hairs sway slowly."""
    g = VGroup()
    u = np.array([np.cos(ang), np.sin(ang), 0])
    n = np.array([-u[1], u[0], 0])
    a = center - u * length / 2
    b = center + u * length / 2
    g.add(Line(a, b, color=LG, stroke_width=26))
    hairs = VGroup()
    for k in range(18):
        p = a + u * (0.3 + k * (length - 0.6) / 17)
        for sgn in (-1, 1):
            h = Line(p, p + n * sgn * 0.75 + u * 0.12 * (k % 3 - 1), color=NEUT, stroke_width=4)
            h._sg = sgn
            h._ph = k * 0.7
            hairs.add(h)
    g.add(hairs)
    return g, hairs


def sway(hairs, clock):
    def u(m, dt):
        pass
    for h in hairs:
        h._base = h.copy()

        def up(mob, dt, h=h):
            a = 0.12 * np.sin(1.6 * clock.get_value() + h._ph)
            mob.become(h._base.copy().rotate(a, about_point=h._base.get_start()))
        h.add_updater(up)


class S11Predict(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        pic = towel(1, 1, 1, 1, 0.0)
        self.add(pic)
        self.at("Back to the strider")
        self.play(pic.animate.scale(0.55).move_to([-3.45, -0.55, 0]), run_time=1.6)
        div = DashedLine([0.3, 3.4, 0], [0.3, -3.5, 0], color=GREY, stroke_width=3)
        leg, hairs = leg_with_hairs(np.array([3.6, 0.2, 0]), length=5.2, ang=-1.0)
        sway(hairs, clock)
        self.at("Its legs are covered")
        self.play(FadeIn(div), FadeIn(leg[0]), run_time=0.8)
        self.play(FadeIn(hairs), run_time=1.0)
        hl = lbl("water-repellent hairs", [3.9, -3.1, 0], LG, 32, BOLD)
        self.play(FadeIn(hl), run_time=0.6)
        tw = lbl("paper towel", [-3.45, 3.0, 0], BROWNL, 34, BOLD)
        self.play(FadeIn(tw), run_time=0.4)
        self.at("like it climbs the towel")
        q = T("?", size=150, color=GOLD, weight=BOLD).move_to([0.3, 0.5, 0])
        self.play(GrowFromCenter(q), run_time=0.9)
        self.at("Pause and decide")
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=1.2)
        self.finish()


class S12Pause(NarratedScene):
    """Hold the question on screen, still but for a countdown ring."""

    def construct(self):
        clock = ValueTracker(0.0)
        pic = towel(1, 1, 1, 1, 0.0).scale(0.55).move_to([-3.45, -0.55, 0])
        leg, hairs = leg_with_hairs(np.array([3.6, 0.2, 0]), length=5.2, ang=-1.0)
        sway(hairs, clock)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        div = DashedLine([0.3, 3.4, 0], [0.3, -3.5, 0], color=GREY, stroke_width=3)
        hl = lbl("water-repellent hairs", [3.9, -3.1, 0], LG, 32, BOLD)
        tw = lbl("paper towel", [-3.45, 3.0, 0], BROWNL, 34, BOLD)
        q = T("?", size=150, color=GOLD, weight=BOLD).move_to([0.3, 0.5, 0])
        ring_bg = Circle(radius=0.55, stroke_color=GREY, stroke_width=6).move_to([0.3, 2.9, 0])
        t0 = ValueTracker(0.0)
        t0.add_updater(lambda m, dt: m.increment_value(dt))
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=TAU * max(0.0, 1 - t0.get_value() / 5.0),
                                         stroke_color=GOLD, stroke_width=8).move_to([0.3, 2.9, 0]) if t0.get_value() < 4.95 else VGroup())
        self.add(clock, t0, pic, leg, div, hl, tw, q, ring_bg, ring)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Reveal(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        leg, hairs = leg_with_hairs(np.array([-3.2, 0.5, 0]), length=5.0, ang=-1.05)
        sway(hairs, clock)
        hl = lbl("water-repellent hairs", [-4.2, -3.3, 0], LG, 32, BOLD)
        self.add(leg, hl)
        # water molecules scattered along the hairs
        rng = np.random.RandomState(5)
        ms = []
        start = [(-1.1 + 0.0 * k, 2.2 - 1.0 * k) for k in range(6)]
        for k, (x, y) in enumerate(start):
            m = mol(0.3, charged=True).move_to([x + rng.uniform(-.2, .2), y, 0]).rotate(rng.uniform(0, TAU))
            wobble(m, amp=0.08, rot=0.15, speed=0.9, seed=k)
            ms.append(m)
        bead_c = np.array([2.6, -0.2, 0.0])
        self.play(FadeIn(VGroup(*ms)), run_time=0.8)
        self.at("water clings only weakly")
        no = lbl("weak adhesion", [-1.1, 3.1, 0], GOLD, 34, BOLD)
        self.play(FadeIn(no), *[Indicate(m, color=TEXT, scale_factor=1.1) for m in ms], run_time=1.6)
        self.at("pulls itself into beads")
        ring_pos = [bead_c + 0.9 * np.array([np.cos(TAU * k / 6), np.sin(TAU * k / 6), 0]) for k in range(6)]
        for m in ms:
            m.clear_updaters()
        self.play(*[m.animate.move_to(p).rotate(0.4) for m, p in zip(ms, ring_pos)], run_time=2.2)
        bead = Circle(radius=1.45, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to(bead_c)
        bead.set_z_index(-1)
        wobble(bead, amp=0.04, speed=1.1, seed=2)
        for k, m in enumerate(ms):
            wobble(m, amp=0.04, rot=0.05, speed=1.1, seed=k + 2)
        bl_ = lbl("water beads up", [bead_c[0], 2.4, 0], BLUE, 34, BOLD)
        self.play(FadeIn(bead), FadeIn(bl_), run_time=1.0)
        self.at("Surface tension plus those hairs")
        self.play(FadeOut(bead), FadeOut(bl_), FadeOut(VGroup(*ms)), FadeOut(no), FadeOut(hl), FadeOut(leg), run_time=0.8)
        d = ValueTracker(0.0)
        wat = always_redraw(lambda: self._wat(d, clock))
        strider = always_redraw(lambda: self._strider(d))
        self.add(wat, strider)
        lab = lbl("surface tension + water-repellent hairs", [0, 3.15, 0], GOLD, 32, BOLD)
        self.play(d.animate.set_value(1.0), FadeIn(lab), run_time=2.4)
        self.finish()

    def _wat(self, d, clock):
        xs = np.linspace(-6.4, 6.4, 70)
        t = clock.get_value()
        pts = [[x, surf_y(x, d.get_value()) - 0.6 + 0.03 * np.sin(1.2 * x + 1.5 * t), 0] for x in xs]
        poly = Polygon(*pts, [6.4, -3.5, 0], [-6.4, -3.5, 0], stroke_width=0, fill_color=BLUE, fill_opacity=0.3)
        top = VMobject().set_points_as_corners(pts).set_stroke(BLUE, 6)
        return VGroup(poly, top)

    def _strider(self, d):
        dv = d.get_value()
        yb = surf_y(0, dv) - 0.6 + 1.3
        body = Ellipse(width=1.8, height=0.6, color=LG, fill_color=LG, fill_opacity=0.95).move_to([0, yb, 0])
        head = Circle(radius=0.2, color=LG, fill_color=LG, fill_opacity=0.95).move_to([1.0, yb + 0.12, 0])
        legs = VGroup()
        for fx in (-2.4, -1.6, -0.8, 0.8, 1.6, 2.4):
            legs.add(Line([0.5 * np.sign(fx), yb - 0.1, 0], [fx, surf_y(fx, dv) - 0.6 + 0.04, 0], color=LG, stroke_width=6))
        return VGroup(legs, body, head)


# ---------------------------------------------------------------------------------------------
def mini_panel(x, y=-0.6):
    return RoundedRectangle(corner_radius=0.2, width=3.1, height=3.1, stroke_color=BLUE, stroke_width=3,
                            fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])


class S14Wrap(SpokenScene):
    def construct(self):
        clock = clock_of(self)
        m = mol(1.3, charged=True, letters=True).move_to([0, 0, 0])
        wobble(m, amp=0.04, rot=0.02, speed=0.8, seed=1)
        self.play(FadeIn(m), run_time=0.8)
        self.at("So one molecule's bent shape")
        self.wait(0.2)
        self.at("help explain all three jobs")
        xs = [-5.0, -1.67, 1.67, 5.0]
        arrow = Arrow([-5.6, 1.45, 0], [5.6, 1.45, 0], buff=0, color=GOLD, stroke_width=20, max_tip_length_to_length_ratio=0.1,
                      max_stroke_width_to_length_ratio=40)
        self.play(m.animate.scale(0.4).move_to([0, 2.85, 0]), GrowArrow(arrow), run_time=1.4)
        pa, pb, pc, pd = [mini_panel(x) for x in xs]
        # a: salt pulled apart
        cr = VGroup(*[blk(0.34, 0.34, PURPLE if (i + j) % 2 == 0 else GREEN, 0.85, 0.04, 2).move_to([xs[0] - 0.9 + 0.36 * i, -0.9 + 0.36 * j, 0])
                      for i in range(3) for j in range(3)])
        ions = VGroup(*[blk(0.34, 0.34, c, 0.85, 0.04, 2).move_to([xs[0] + 0.7 + dx, y, 0]) for c, dx, y in ((PURPLE, 0.0, -0.3), (GREEN, 0.4, -0.9), (PURPLE, 0.1, -1.4))])
        for k, io in enumerate(ions):
            wobble(io, amp=0.07, speed=1.2, seed=k)
        la = VGroup(pa, cr, ions)
        # b: dimple + strider
        def bpic():
            dv = 1.0
            xsl = np.linspace(xs[1] - 1.45, xs[1] + 1.45, 30)
            pts = [[x, -1.0 - 0.4 * np.exp(-((x - xs[1]) / 0.9) ** 2) + 0.03 * np.sin(2 * clock.get_value() + 3 * x), 0] for x in xsl]
            top = VMobject().set_points_as_corners(pts).set_stroke(BLUE, 5)
            fill = Polygon(*pts, [xs[1] + 1.45, -2.1, 0], [xs[1] - 1.45, -2.1, 0], stroke_width=0, fill_color=BLUE, fill_opacity=0.35)
            yb = -1.4 + 1.0
            body = Ellipse(width=0.9, height=0.3, color=LG, fill_color=LG, fill_opacity=0.95).move_to([xs[1], yb, 0])
            legs = VGroup(*[Line([xs[1] + 0.25 * np.sign(fx), yb - 0.05, 0], [xs[1] + fx, -1.0 - 0.4 * np.exp(-(fx / 0.9) ** 2) + 0.02, 0], color=LG, stroke_width=4)
                            for fx in (-1.1, -0.65, -0.3, 0.3, 0.65, 1.1)])
            return VGroup(fill, top, legs, body)
        lb = VGroup(pb, always_redraw(bpic))
        # c: strand
        strand = blk(0.4, 2.5, BROWN, 0.95, 0.05, 2).move_to([xs[2], -0.35, 0])
        pool = Rectangle(width=2.9, height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=0.35).move_to([xs[2], -1.7, 0])
        films = VGroup(*[Rectangle(width=0.35, height=1.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.55).move_to([xs[2] + sx * 0.38, -0.95 + 0.0, 0]) for sx in (-1, 1)])
        lc = VGroup(pc, pool, strand, films)
        # d: thermometer + glass
        th_body = blk(0.34, 1.9, TEXT, 0.0, 0.17, 3).move_to([xs[3] - 0.7, -0.45, 0])
        th_fill = blk(0.2, 0.8, RED, 0.9, 0.1, 0).move_to([xs[3] - 0.7, -0.95, 0])
        bulb = Circle(radius=0.28, stroke_color=TEXT, stroke_width=3, fill_color=RED, fill_opacity=0.9).move_to([xs[3] - 0.7, -1.55, 0])
        glass = VGroup(Line([xs[3] + 0.25, 0.3, 0], [xs[3] + 0.25, -1.7, 0]), Line([xs[3] + 0.25, -1.7, 0], [xs[3] + 1.25, -1.7, 0]),
                       Line([xs[3] + 1.25, -1.7, 0], [xs[3] + 1.25, 0.3, 0])).set_stroke(LG, 5)
        gw = Rectangle(width=0.96, height=1.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([xs[3] + 0.75, -1.05, 0])
        ld = VGroup(pd, th_body, th_fill, bulb, glass, gw)
        labels = [lbl("dissolving", [xs[0], -2.6, 0], TEXT, 30, BOLD), lbl("surface tension", [xs[1], -2.6, 0], TEXT, 30, BOLD),
                  lbl("capillary action", [xs[2], -2.6, 0], TEXT, 30, BOLD), lbl("next: warming", [xs[3], -2.6, 0], GOLD, 30, BOLD)]
        self.play(LaggedStart(FadeIn(la), FadeIn(lb), FadeIn(lc), lag_ratio=0.35), run_time=2.2)
        self.play(LaggedStart(*[FadeIn(l) for l in labels[:3]], lag_ratio=0.2), run_time=0.9)
        self.at("The same tug helps make water slow to warm")
        self.play(FadeIn(ld), FadeIn(labels[3]), run_time=1.2)
        self.play(th_fill.animate.stretch_to_fit_height(1.1, about_edge=DOWN) if False else Indicate(th_fill, color=RED, scale_factor=1.3), run_time=1.2)
        self.at("as film two shows")
        self.play(Indicate(labels[3], color=GOLD, scale_factor=1.15), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15End(EndCard):
    LINE = "Water's charged ends tug on neighbors, ions and polar molecules."
