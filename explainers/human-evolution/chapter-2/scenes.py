"""A Clock Made of Cuts (human-evolution film, chapter 2)

COLOUR MAP (same as chapter 1, plus the DNA colour): TEAL = Homo sapiens; ORANGE = Neanderthal DNA;
GOLD = dated things, tags, citations; GREY/LBL = outlines and labels. Chromosomes, maps and stacks are
simple labelled cartoons; segment lengths are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C38"
LBL = "#C9D1DE"

AFR = [(-4.6, 2.0), (-3.4, 3.0), (-1.2, 3.2), (0.6, 3.0), (1.4, 2.4), (1.8, 1.2), (2.4, 0.2), (3.2, -0.4),
       (2.2, -0.9), (1.6, -2.0), (0.6, -3.4), (-0.4, -3.5), (-1.0, -2.2), (-1.4, -0.6), (-2.6, -0.6),
       (-3.8, 0.2), (-4.8, 0.8)]
ASIA = [(1.9, 2.8), (3.0, 3.4), (5.5, 3.3), (6.5, 2.0), (5.4, 0.6), (4.3, -0.5), (3.6, 0.3), (2.9, 1.4), (2.3, 2.1)]
EUR = [(-0.2, 3.0), (0.2, 3.8), (1.4, 4.2), (2.6, 4.0), (3.0, 3.4), (1.9, 2.8), (0.6, 3.0)]
PIN_SIB, PIN_BUL = (3.4, 2.7), (2.0, 3.5)


class Atlas:
    def __init__(self, s=0.8, cx=0.0, cy=-0.5):
        self.s, self.cx, self.cy = s, cx, cy

    def P(self, x, y):
        return np.array([self.cx + (x - 0.85) * self.s, self.cy + (y + 0.05) * self.s, 0.0])

    def land(self):
        g = VGroup()
        for pts in (AFR, ASIA, EUR):
            g.add(Polygon(*[self.P(*p) for p in pts], stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.3))
        return g


def pin(col=TEXT):
    tri = Polygon([0, 0, 0], [-0.17, 0.4, 0], [0.17, 0.4, 0], stroke_width=0, fill_color=col, fill_opacity=1)
    head = Circle(radius=0.2, stroke_width=0, fill_color=col, fill_opacity=1).move_to([0, 0.52, 0])
    dot = Dot(radius=0.07, color=BG).move_to([0, 0.52, 0])
    return VGroup(tri, head, dot)


def pin_at(p, col=TEXT, h=None):
    g = pin(col)
    if h:
        g.scale(h / g.height)
    g.move_to(p + UP * g.height / 2)
    return g


def motes(seed, n=18, col=(GOLD, TEAL, GREY)):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.07, 0.13), color=col[rng.randint(len(col))])
        d.set_opacity(rng.uniform(0.35, 0.7))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.1, 0.3))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.0:
                m.shift(DOWN * 8.0)
            if abs(m.get_x()) > 7.1:
                m.shift(LEFT * 14.2 * np.sign(m.get_x()))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-5)
    return g


def pulse_chip(c, rate=2.4, phase=0.0):
    c.pt = phase

    def up(x, dt):
        x.pt += dt
        a = 0.35 + 0.65 * abs(np.sin(rate * x.pt))
        x[0].set_stroke(opacity=a)
        x[1].set_opacity(a)
    c.add_updater(up)
    return c


def breathe(m, a=0.55, b=1.0, rate=2.0):
    m.bt = 0.0

    def up(x, dt):
        x.bt += dt
        x.set_fill(opacity=a + (b - a) * (0.5 + 0.5 * np.sin(rate * x.bt)))
    m.add_updater(up)
    return m


def tag(text, size=28, col=GOLD):
    return chip(text, color=col, size=size, pad=0.16, fill_opacity=0.22)


def schem():
    return T("schematic", 22, LBL).move_to([6.1, -3.55, 0])


def checklist(scale=1.0):
    a = T("What was dated?", 34, GOLD, weight=BOLD)
    b = T("Where did it lie?", 34, TEAL, weight=BOLD)
    t = VGroup(a, b).arrange(DOWN, buff=0.18)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 1.7, height=t.height + 0.9, stroke_color=TEXT,
                           stroke_width=3, fill_color=BG, fill_opacity=0.92)
    g = VGroup(box, t)
    g.a, g.b = a, b
    return g.scale(scale)


def person(h=1.0, col=TEAL):
    head = Circle(radius=0.18 * h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.55)
    body = RoundedRectangle(corner_radius=0.2 * h, width=0.55 * h, height=0.62 * h, stroke_color=col,
                            stroke_width=3, fill_color=col, fill_opacity=0.55)
    head.move_to([0, 0.5 * h, 0])
    body.move_to([0, -0.02 * h, 0])
    return VGroup(head, body)


# ---------- chromosomes ----------
X0, LEN = -5.6, 11.2
YA, YB = 1.2, -1.2
BH = 1.2
BLOCK = (0.32, 0.66)


def clip(ivs, lo, hi):
    return [(max(a, lo), min(b, hi)) for a, b in ivs if min(b, hi) - max(a, lo) > 1e-6]


def bar(y, ivs=(), lo=0.0, hi=1.0, h=BH, x0=X0, L=LEN, minw=0.0):
    xa, xb = x0 + lo * L, x0 + hi * L
    base = Rectangle(width=xb - xa, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                     fill_opacity=0.45).move_to([(xa + xb) / 2, y, 0])
    g = VGroup(base)
    for a, b in ivs:
        a2, b2 = max(a, lo), min(b, hi)
        if b2 - a2 <= 1e-6:
            continue
        w = max((b2 - a2) * L, minw)
        g.add(Rectangle(width=w, height=h, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                        fill_opacity=0.85).move_to([x0 + (a2 + b2) / 2 * L, y, 0]))
    return g


def bar1(y, iv=None, h=BH, x0=X0, L=LEN, minw=0.0):
    """A bar with exactly two parts (teal base + one orange piece), so bars can Transform into each other."""
    base = Rectangle(width=L, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                     fill_opacity=0.45).move_to([x0 + L / 2, y, 0])
    if iv is None:
        o = Rectangle(width=0.02, height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0).move_to([x0 + L / 2, y, 0])
    else:
        w = max((iv[1] - iv[0]) * L, minw)
        o = Rectangle(width=w, height=h, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                      fill_opacity=0.85).move_to([x0 + (iv[0] + iv[1]) / 2 * L, y, 0])
    return VGroup(base, o)


def flecks(n=16, seed=3, w=0.012):
    rs = np.random.RandomState(seed)
    return [((i + 0.2 + 0.6 * rs.rand()) / n, (i + 0.2 + 0.6 * rs.rand()) / n + w) for i in range(n)]


PRES = [(a, a + 0.006) for a, _ in flecks(12, 3)]
HIS = [(0.12, 0.19), (0.25, 0.32), (0.4, 0.46), (0.55, 0.62), (0.7, 0.76), (0.84, 0.9)]


# ---------- stacks (the clue) ----------
SBASE = -2.6


def stack(x, n):
    rows = VGroup()
    for i in range(n):
        y = SBASE + 0.18 + i * 0.36
        l = Rectangle(width=0.76, height=0.32, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                      fill_opacity=0.8).move_to([x - 0.4, y, 0])
        r = Rectangle(width=0.76, height=0.32, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                      fill_opacity=0.8).move_to([x + 0.4, y, 0])
        rows.add(VGroup(l, r))
    return rows


def stack_label(text, x):
    return T(text, 28, TEXT).move_to([x, -3.1, 0])


# ---------- generation panel ----------
PX0, PL = -6.3, 8.8
PYS = [2.5, 1.54, 0.58, -0.38, -1.34, -2.3]
GENS = [0, 1, 2, 5, 10, 100]
LOST = {0: (), 1: (), 2: (5,), 5: (2, 5), 10: (2, 5), 100: (2, 5)}


def _sim():
    out = []
    for i in range(6):
        rs = np.random.RandomState(50 + i)
        a, b = BLOCK
        st = {0: (a, b)}
        for gen in range(1, 101):
            for _ in range(rs.poisson(1.0)):
                c = rs.rand()
                if a < c < b:
                    if rs.rand() < 0.5:
                        b = c
                    else:
                        a = c
            st[gen] = (a, b)
        out.append(st)
    return out


SIM = _sim()


def panel(g):
    out = VGroup()
    for i, y in enumerate(PYS):
        iv = None if i in LOST[g] else SIM[i][g]
        out.add(bar1(y, iv, h=0.5, x0=PX0, L=PL, minw=0.12))
    return out


def counter_text(g):
    return M(str(g), 56, GOLD, weight=BOLD).move_to([4.7, 2.5, 0])


def counter_head():
    return T("generations", 28, LBL).move_to([4.7, 3.3, 0])


def clock(c, r, tr, w=3):
    face = Circle(radius=r, color=TEXT, stroke_width=w + 1)
    ticks = VGroup(*[Line(c + 0.86 * r * np.array([np.sin(k * TAU / 12), np.cos(k * TAU / 12), 0]),
                          c + 0.98 * r * np.array([np.sin(k * TAU / 12), np.cos(k * TAU / 12), 0]),
                          color=TEXT, stroke_width=w) for k in range(12)])
    face.move_to(c)
    hand = always_redraw(lambda: Line(c, c + 0.75 * r * np.array([np.sin(TAU * tr.get_value()),
                                                                  np.cos(TAU * tr.get_value()), 0]),
                                       color=GOLD, stroke_width=5))
    return VGroup(face, ticks), hand


def lineup_objs(x0=-2.9, L=7.0, ys=(1.9, 0.3, -1.3), h=0.9, full=True):
    names = ["Bacho Kiro", "Ust'-Ishim", "present day"]
    ivs = [[(0.06, 0.38), (0.48, 0.80), (0.88, 0.9)], [(a * 0.9 + 0.04, a * 0.9 + 0.04 + 0.07) for a in
                                                         (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.93)], PRES]
    bars, labs, gens = VGroup(), VGroup(), VGroup()
    gl = ["about 7 or fewer", "232–430", "~1,500–2,000"]
    for i, y in enumerate(ys):
        bars.add(bar(y, ivs[i], h=h, x0=x0, L=L, minw=0.06))
        labs.add(T(names[i], 28, TEXT).move_to([x0, y + 0.72, 0], aligned_edge=LEFT))
        gens.add(T(gl[i], 28, GOLD).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT))
    return bars, labs, gens


# ===========================================================================================
class S00Title(TitleCard):
    LESSON = "Human Evolutionary History: An African Origin and Archaic Ancestry"
    TITLE = "A Clock Made of Cuts"


class S01Link(SpokenScene):
    def construct(self):
        self.add(motes(21))
        card = checklist(1.4).move_to([0, 0.4, 0])
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.at("Fossils show")
        self.play(Indicate(card.b, color=TEAL, scale_factor=1.15), run_time=1.2)
        self.at("not who had children")
        who = T("not who had children together", 32, LBL).move_to([0, -1.6, 0])
        self.play(FadeIn(who, shift=UP * 0.15), run_time=0.8)
        self.at("That needs DNA")
        dna = T("DNA", 80, TEXT, font=TITLE_FONT, weight=BOLD).move_to([0, 0.2, 0])
        self.play(card.animate.scale(0.5).move_to([-4.7, 3.1, 0]), FadeOut(who), GrowFromCenter(dna), run_time=1.3)
        self.at("If you carry")
        pr = person(4.6).move_to([0, -0.2, 0])
        self.play(FadeOut(dna), GrowFromCenter(pr), run_time=1.2)
        self.at("Neanderthal DNA")
        fleck = Circle(radius=0.24, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.95).move_to([0.0, -0.2, 0])
        self.play(GrowFromCenter(fleck), run_time=0.7)
        nl = T("Neanderthal DNA", 32, ORANGE).move_to([3.6, -0.2, 0])
        ln = Line(fleck.get_right(), nl.get_left() + LEFT * 0.1, color=ORANGE, stroke_width=3)
        self.play(Create(ln), FadeIn(nl), run_time=0.8)
        self.at("when did it")
        wh = tag("when?", 44, GOLD).move_to([-3.6, 0.9, 0])
        self.play(GrowFromCenter(wh), run_time=0.6)
        pulse_chip(wh)
        self.finish()


class S02Clue(SpokenScene):
    def construct(self):
        self.add(motes(22))
        a = T("a clue", 72, TEXT, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.play(Write(a), run_time=1.4)
        self.at("A draft Neanderthal genome")
        nb = bar(3.1, [(0, 1)], h=0.5, x0=-6.3, L=4.6)
        nl = T("Neanderthal (draft)", 28, ORANGE).move_to([-1.4, 3.1, 0], aligned_edge=LEFT)
        self.play(FadeOut(a), Create(nb), FadeIn(nl), run_time=1.2)
        self.at("compared with genomes")
        lb = bar(2.2, [], h=0.5, x0=-6.3, L=4.6)
        ll = T("living people", 28, TEAL).move_to([-1.4, 2.2, 0], aligned_edge=LEFT)
        ar = DoubleArrow([-4.0, 2.55, 0], [-4.0, 2.75, 0], buff=0, color=LBL, stroke_width=4, tip_length=0.12)
        self.play(Create(lb), FadeIn(ll), FadeIn(ar), run_time=1.2)
        self.at("It shared more variants")
        ticks = VGroup(*[Line([-6.0 + 0.9 * k, 2.4, 0], [-6.0 + 0.9 * k, 2.9, 0], color=TEXT, stroke_width=4)
                         for k in range(1, 5)])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.25), run_time=1.4)
        self.at("sites where genomes differ")
        vt = VGroup(T("variants =", 28, TEXT), T("sites that differ", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([4.5, 2.7, 0])
        self.play(FadeIn(vt, shift=LEFT * 0.2), Indicate(ticks, color=TEXT), run_time=1.2)
        self.at("with sampled Eurasians")
        se = stack(-3.2, 8)
        sel = stack_label("Eurasian + Neanderthal share", -3.2)
        self.play(FadeOut(vt), FadeOut(ar), FadeIn(sel), LaggedStart(*[GrowFromEdge(r, DOWN) for r in se], lag_ratio=0.12), run_time=1.6)
        self.at("than with sampled")
        sa = stack(3.2, 5)
        sal = stack_label("African + Neanderthal share", 3.2)
        self.play(FadeIn(sal), LaggedStart(*[GrowFromEdge(r, DOWN) for r in sa], lag_ratio=0.12), run_time=1.3)
        gt = tag("Green et al., 2010", 28, GOLD).move_to([0, -0.9, 0])
        self.play(FadeOut(ticks), FadeOut(nl), FadeOut(ll), FadeIn(gt), FadeIn(schem()), run_time=0.8)
        self.finish()


class S03Notwhen(SpokenScene):
    def construct(self):
        self.add(motes(23))
        se, sa = stack(-3.2, 8), stack(3.2, 5)
        self.add(se, sa, stack_label("Eurasian + Neanderthal share", -3.2), stack_label("African + Neanderthal share", 3.2), schem())
        self.at("The team read")
        for r in se:
            self.play(Indicate(r, color=ORANGE, scale_factor=1.04), run_time=0.12)
        self.at("suggesting interbreeding")
        t1 = T("a clue to mixing", 30, GOLD, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.16, width=4.0, height=1.9, stroke_color=GOLD, stroke_width=2.5,
                               fill_color=GOLD, fill_opacity=0.18).move_to([-3.2, 1.35, 0])
        t1.move_to([-3.2, 1.9, 0])
        self.play(FadeIn(box), Write(t1), run_time=1.2)
        self.at("But a clue is not proof")
        t2 = T("not proof", 30, TEXT).move_to([-3.2, 1.3, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.at("it gives no date")
        t3 = T("no date", 30, TEXT).move_to([-3.2, 0.8, 0])
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.8)
        self.at("An old African population")
        t4 = T("or old population structure?", 28, LBL)
        b4 = RoundedRectangle(corner_radius=0.16, width=t4.width + 0.4, height=0.8, stroke_color=LBL,
                              stroke_width=2.5, fill_color=LBL, fill_opacity=0.12)
        g4 = VGroup(b4, t4.move_to(b4)).move_to([3.2, 0.7, 0])
        g4.set_opacity(0.6)
        self.play(FadeIn(g4, shift=DOWN * 0.15), run_time=1.0)
        self.at("split into partly separate")
        self.play(*[r[0].animate.shift(LEFT * 0.3) for r in sa], *[r[1].animate.shift(RIGHT * 0.3) for r in sa], run_time=1.6)
        self.at("could produce some")
        self.play(g4.animate.set_opacity(1.0), Indicate(g4, color=LBL), run_time=1.2)
        for r in sa:
            self.play(Indicate(r, color=ORANGE, scale_factor=1.04), run_time=0.12)
        self.finish()


class S04Chromosome(SpokenScene):
    def construct(self):
        self.add(motes(24))
        se, sa = stack(-3.2, 8), stack(3.2, 5)
        sl = VGroup(stack_label("Eurasian + Neanderthal share", -3.2), stack_label("African + Neanderthal share", 3.2))
        self.add(se, sa, sl)
        self.at("So look along")
        self.play(se.animate.shift(LEFT * 8), sa.animate.shift(RIGHT * 8), sl.animate.set_opacity(0), run_time=1.4)
        self.remove(se, sa, sl)
        outline = Rectangle(width=LEN, height=BH, stroke_color=TEAL, stroke_width=3).move_to([0, YA, 0])
        self.play(Create(outline), run_time=1.6)
        self.at("Picture one teal chromosome")
        b = bar(YA)
        self.play(FadeIn(b[0]), run_time=0.9)
        self.remove(outline)
        self.at("in a modern human")
        ml = T("modern human", 30, TEAL).move_to([-5.6, 0.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.7)
        self.at("It carries one long orange block")
        a, c = BLOCK
        ob = Rectangle(width=(c - a) * LEN, height=BH, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                       fill_opacity=0.85).move_to([X0 + (a + c) / 2 * LEN, YA, 0])
        self.play(GrowFromCenter(ob), run_time=1.4)
        breathe(ob, 0.6, 0.95, 2.0)
        self.at("inherited from a Neanderthal ancestor")
        il = T("inherited from a Neanderthal ancestor", 32, ORANGE).move_to([ob.get_center()[0], 2.55, 0])
        self.play(FadeIn(il, shift=DOWN * 0.15), run_time=1.0)
        self.at("At first the block")
        dl = DoubleArrow(ob.get_corner(DL) + DOWN * 0.35, ob.get_corner(DR) + DOWN * 0.35, buff=0, color=ORANGE, stroke_width=5)
        ut = T("long and unbroken", 40, TEXT, font=TITLE_FONT).move_to([ob.get_center()[0], -0.9, 0])
        self.play(GrowFromCenter(dl), run_time=0.9)
        self.play(Write(ut), run_time=1.2)
        self.finish()


class S05Cuts(SpokenScene):
    def construct(self):
        self.add(motes(25))
        A, B = [BLOCK], []
        barA = bar(YA, A)
        self.add(barA)
        self.at("Each time eggs")
        ch = T("making eggs and sperm", 32, LBL).move_to([0, -3.0, 0])
        self.play(FadeIn(ch, shift=UP * 0.1), run_time=0.8)
        self.at("paired chromosomes swap")
        barB = bar(YB, B)
        pl = T("paired chromosomes", 32, TEAL).move_to([0, -3.0, 0])
        self.play(FadeOut(ch), GrowFromCenter(barB), FadeIn(pl), run_time=1.2)

        def cut(c, A, B, barA, barB):
            x = X0 + c * LEN
            line = DashedLine([x, YA + 1.0, 0], [x, YB - 1.0, 0], color=TEXT, stroke_width=5)
            self.play(Create(line), run_time=0.5)
            pcs = [bar(YA, A, 0, c), bar(YA, A, c, 1), bar(YB, B, 0, c), bar(YB, B, c, 1)]
            self.remove(barA, barB)
            self.add(*pcs)
            self.play(pcs[1].animate.shift(DOWN * (YA - YB)), pcs[3].animate.shift(UP * (YA - YB)), run_time=1.1)
            nA = clip(B, 0, c) + clip(A, c, 1)
            nB = clip(A, 0, c) + clip(B, c, 1)
            self.remove(*pcs, line)
            bA, bB = bar(YA, nA), bar(YB, nB)
            self.add(bA, bB)
            return nA, nB, bA, bB

        self.at("swap pieces")
        A, B, barA, barB = cut(0.12, A, B, barA, barB)
        self.at("This is recombination")
        self.remove(pl)
        rt = T("recombination", 52, GOLD, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.play(Write(rt), run_time=1.0)
        A, B, barA, barB = cut(0.84, A, B, barA, barB)
        self.at("A swap inside the orange block")
        A, B, barA, barB = cut(0.52, A, B, barA, barB)
        self.at("in the copy")
        ar = Arrow([0, 0.0, 0], barA.get_center() + DOWN * 0.7, buff=0, color=TEXT, stroke_width=5)
        lab = T("copy passed to a child", 32, TEXT).move_to([0, 0.0, 0]).shift(DOWN * 0.0)
        lab.move_to([-1.6, -0.05, 0])
        ar = Arrow(lab.get_right() + RIGHT * 0.1, [barA.get_center()[0] + 1.3, YA - 0.65, 0], buff=0.05, color=TEXT, stroke_width=5)
        self.play(FadeIn(lab, shift=UP * 0.1), GrowArrow(ar), run_time=1.0)
        for p in barA[1:]:
            breathe(p, 0.55, 1.0, 3.0)
        self.finish()


class S06Counter(SpokenScene):
    def construct(self):
        self.add(motes(26))
        A = bar(YA, [BLOCK])
        self.add(A)
        self.play(Indicate(A[1], color=ORANGE, scale_factor=1.05), run_time=1.2)
        self.at("the swaps pile up")
        P = panel(0)
        ch, cn = counter_head(), counter_text(0)
        self.play(*[TransformFromCopy(A, P[i]) for i in range(1, 6)], ReplacementTransform(A, P[0]),
                  FadeIn(ch), FadeIn(cn), run_time=1.2)
        cur = {"g": 0, "cn": cn, "P": P}

        def go(g, rt=0.7):
            newP, ncn = panel(g), counter_text(g)
            self.play(*[Transform(cur["P"][i], newP[i]) for i in range(6)], Transform(cur["cn"], ncn), run_time=rt)
            cur["g"] = g

        go(1)
        go(2, 0.6)
        self.at("Some descendants keep")
        P = cur["P"]
        whole = [i for i in range(6) if i not in LOST[2] and abs(SIM[i][2][0] - BLOCK[0]) < 1e-9 and abs(SIM[i][2][1] - BLOCK[1]) < 1e-9]
        short = [i for i in range(6) if i not in LOST[2] and i not in whole]
        lost = list(LOST[2])
        self.whole, self.short = whole, short

        def outline(idx, col):
            return VGroup(*[SurroundingRectangle(P[i], color=col, buff=0.08, stroke_width=4) for i in idx])

        o1 = outline(whole, TEXT)
        l1 = T("kept whole", 32, TEXT).move_to([4.7, 0.9, 0])
        self.play(Create(o1), FadeIn(l1), run_time=0.8)
        self.at("Some keep a shorter")
        o2 = outline(short, GOLD)
        l2 = T("shorter piece", 32, GOLD).move_to([4.7, 0.9, 0])
        self.play(FadeOut(o1), FadeOut(l1), Create(o2), FadeIn(l2), run_time=0.8)
        self.at("and some lose it")
        o3 = outline(lost, RED)
        l3 = T("lost", 32, RED).move_to([4.7, 0.9, 0])
        self.play(FadeOut(o2), FadeOut(l2), Create(o3), FadeIn(l3), run_time=0.8)
        self.at("Across many descendants")
        self.play(FadeOut(o3), FadeOut(l3), run_time=0.5)
        go(5, 0.7)
        go(10, 0.7)
        self.at("the orange pieces that survive")
        go(100, 1.0)
        self.at("get shorter on average")
        la = T("shorter", 32, GOLD).move_to([4.7, 0.7, 0])
        lb = T("on average", 32, GOLD).move_to([4.7, 0.2, 0])
        self.play(FadeIn(la, shift=UP * 0.1), FadeIn(lb, shift=UP * 0.1), run_time=0.8)
        self.add(schem())
        self.play(Indicate(VGroup(la, lb), color=GOLD), run_time=1.0)
        self.finish()


class S07Clock(SpokenScene):
    def construct(self):
        self.add(motes(27))
        P = panel(100)
        ch, cn = counter_head(), counter_text(100)
        self.add(P, ch, cn)
        c = np.array([-3.9, 0.3, 0])
        tr = ValueTracker(0.0)
        face, hand = clock(c, 1.9, tr)
        self.play(FadeOut(P), FadeOut(ch), ReplacementTransform(cn, face), FadeIn(hand), run_time=0.9)
        self.at("makes length a clock")
        self.play(tr.animate.set_value(0.12), run_time=1.0, rate_func=linear)
        self.at("Long orange segments")
        b1 = bar(1.4, [(0.1, 0.85)], h=0.9, x0=0.9, L=5.6)
        self.play(GrowFromEdge(b1, LEFT), run_time=1.2)
        t1 = T("recent", 40, TEAL, weight=BOLD).move_to([3.7, 0.5, 0])
        self.at("recently")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.8)
        self.play(tr.animate.set_value(0.2), run_time=1.5, rate_func=linear)
        self.at("Short flecks")
        b2 = bar(-1.3, flecks(8, 5, 0.006), h=0.9, x0=0.9, L=5.6, minw=0.06)
        self.play(FadeIn(b2), tr.animate.set_value(1.1), run_time=2.0, rate_func=linear)
        t2 = T("long ago", 40, GOLD, weight=BOLD).move_to([3.7, -2.2, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.play(tr.animate.set_value(1.5), run_time=2.0, rate_func=linear)
        self.finish()


class S08Present(SpokenScene):
    def construct(self):
        self.add(motes(28))
        self.at("Today")
        b = bar(0.6, [], h=1.2)
        lb = T("present-day non-African", 32, TEAL).move_to([0, 1.8, 0])
        self.play(Create(b), FadeIn(lb), run_time=0.8)
        self.at("after far more generations")
        c = np.array([-6.0, 3.2, 0])
        tr = ValueTracker(0.0)
        face, hand = clock(c, 0.6, tr, 2)
        self.play(FadeIn(face), FadeIn(hand), run_time=0.5)
        gt = T("~1,500–2,000 generations (model-based)", 30, GOLD).move_to([0, -1.2, 0])
        self.play(tr.animate.set_value(3.0), FadeIn(gt, shift=UP * 0.1), run_time=1.6, rate_func=linear)
        self.at("the Neanderthal pieces in living")
        fl = VGroup(*bar(0.6, PRES, h=1.2, minw=0.06)[1:])
        self.play(LaggedStart(*[GrowFromCenter(f) for f in fl], lag_ratio=0.15), run_time=1.8)
        self.at("are short")
        at = T("average ~0.05–0.07 cM", 34, ORANGE, weight=BOLD).move_to([0, -2.3, 0])
        self.play(FadeIn(at, shift=UP * 0.1), Indicate(fl, color=ORANGE), run_time=1.2)
        self.at("The cutting has run")
        cuts = VGroup(*[DashedLine([X0 + (a + 0.006) * LEN + 0.0, 1.3 + 0.0, 0], [X0 + (a + 0.006) * LEN, -0.1, 0], color=TEXT, stroke_width=3)
                        for a, _ in PRES[::2]])
        self.play(LaggedStart(*[Create(c_) for c_ in cuts], lag_ratio=0.15), tr.animate.set_value(7.5), run_time=2.0, rate_func=linear)
        self.finish()


HX0, HL, YH, YP = -6.3, 9.6, 0.9, -1.2


def predict_frame(sc, reveal=False):
    """Rebuilt in one place for s09, s10, s11. Returns dict of objects."""
    at = Atlas(0.3, 4.9, 2.5)
    land = at.land()
    pn = pin_at(at.P(*PIN_SIB), TEXT, h=0.3)
    fig = person(0.8, TEAL).move_to(at.P(*PIN_SIB) + LEFT * 0.0 + DOWN * 0.0).shift(DOWN * 0.0)
    his = bar(YH, HIS if reveal else [], h=0.9, x0=HX0, L=HL, minw=0.1)
    pres = bar(YP, PRES, h=0.9, x0=HX0, L=HL, minw=0.06)
    hl = T("Ust'-Ishim, ~45,000 years ago", 30, TEAL).move_to([HX0, 1.95, 0], aligned_edge=LEFT)
    pl = T("present day", 30, TEAL).move_to([HX0, -0.2, 0], aligned_edge=LEFT)
    cover = Rectangle(width=HL * 0.82, height=0.9, stroke_color=LBL, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([HX0 + HL / 2, YH, 0])
    q = T("?", 56, TEXT, weight=BOLD).move_to(cover)
    cov = VGroup(cover, q)
    c1 = chip("longer?", TEXT, 32).move_to([5.1, 0.4, 0])
    c2 = chip("shorter?", TEXT, 32).move_to([5.1, -0.7, 0])
    return dict(at=at, land=land, pn=pn, fig=fig, his=his, pres=pres, hl=hl, pl=pl, cov=cov, c1=c1, c2=c2)


class S09Predict(SpokenScene):
    def construct(self):
        self.add(motes(29))
        at = Atlas(0.8, 0.0, -0.5)
        land = at.land()
        self.at("Now meet")
        self.play(Create(land), run_time=1.6)
        p = pin_at(at.P(*PIN_SIB), TEXT, h=0.9)
        pos = p.get_center().copy()
        p.shift(UP * 1.0).set_opacity(0)
        self.at("a man who lived")
        self.play(p.animate.move_to(pos).set_opacity(1), run_time=0.7)
        fig = person(1.4, TEAL).move_to(at.P(*PIN_SIB) + DOWN * 1.1 + RIGHT * 0.9)
        lab = T("Ust'-Ishim", 36, TEAL, weight=BOLD).next_to(fig, DOWN, buff=0.15)
        lab.set_stroke(BG, width=12, background=True)
        self.play(FadeIn(fig, shift=UP * 0.2), FadeIn(lab), run_time=0.8)
        self.at("western Siberia")
        ag = T("~45,000 years ago", 32, GOLD).move_to([-3.4, 2.7, 0])
        self.play(FadeIn(ag, shift=RIGHT * 0.2), Indicate(p, color=TEXT), run_time=0.7)
        self.at("long before us")
        self.play(Indicate(ag, color=GOLD), run_time=1.0)
        F = predict_frame(self)
        self.at("Will his orange segments")
        small = VGroup(land, p, fig, lab)
        self.play(FadeOut(ag), ReplacementTransform(small, VGroup(F["land"], F["pn"], F["fig"])), run_time=1.2)
        self.play(FadeIn(F["his"]), FadeIn(F["hl"]), FadeIn(F["pres"]), FadeIn(F["pl"]), FadeIn(F["cov"]), run_time=1.0)
        self.at("longer or shorter")
        self.play(FadeIn(F["c1"]), FadeIn(F["c2"]), run_time=0.7)
        pulse_chip(F["c1"], 2.4, 0.0)
        pulse_chip(F["c2"], 2.4, 0.65)
        self.at("than yours")
        self.play(Indicate(F["pres"], color=ORANGE, scale_factor=1.02), run_time=1.0)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        self.add(motes(30))
        F = predict_frame(self)
        self.add(F["land"], F["pn"], F["fig"], F["his"], F["pres"], F["hl"], F["pl"], F["cov"], F["c1"], F["c2"])
        pulse_chip(F["c1"], 2.4, 0.0)
        pulse_chip(F["c2"], 2.4, 0.65)
        bt = ValueTracker(0)
        barx = always_redraw(lambda: Rectangle(width=max(0.01, 13.6 * bt.get_value()), height=0.2, stroke_width=0,
                                               fill_color=TEXT, fill_opacity=0.8).move_to([-6.8, -3.7, 0], aligned_edge=LEFT))
        self.add(barx)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * max(0.001, tr.get_value()),
                                         color=TEXT, stroke_width=6).move_to([-5.6, -2.7, 0]))
        back = Circle(radius=0.4, color=GREY, stroke_width=3).move_to([-5.6, -2.7, 0])
        self.add(back, ring)
        self.play(tr.animate.set_value(1), bt.animate.set_value(1), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S11Reveal(SpokenScene):
    def construct(self):
        self.add(motes(31))
        F = predict_frame(self)
        self.add(F["land"], F["pn"], F["fig"], F["his"], F["pres"], F["hl"], F["pl"], F["cov"], F["c1"], F["c2"])
        self.at("Longer")
        rev = predict_frame(self, True)
        self.play(F["cov"].animate.shift(UP * 1.0).set_opacity(0), Transform(F["his"], rev["his"]), run_time=1.2)
        yes = chip("longer? yes", TEAL, 32).move_to(F["c1"])
        self.play(Transform(F["c1"], yes), FadeOut(F["c2"]), run_time=0.8)
        self.at("Fewer generations")
        gt = T("232–430 generations (single-pulse fit)", 30, GOLD).move_to([HX0, -2.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(gt, shift=UP * 0.1), Indicate(F["his"][1:], color=ORANGE), run_time=1.2)
        self.at("From their lengths")
        self.play(Indicate(F["his"][1:], color=ORANGE, scale_factor=1.06), run_time=1.0)
        self.at("Fu and colleagues")
        ft = T("gene flow 7,000–13,000 years before him", 30, GOLD).move_to([HX0, -3.25, 0], aligned_edge=LEFT)
        ct = T("(Fu et al., 2014)", 24, LBL).move_to([4.5, -3.25, 0])
        self.play(FadeIn(ft, shift=UP * 0.1), FadeIn(ct), run_time=1.2)
        self.at("how long before his life")
        self.play(Indicate(ft, color=GOLD), run_time=1.4)
        self.finish()


def tree(x, base=-2.0, top=1.3):
    ys = np.linspace(base + 0.55, top, 4)
    g = VGroup()
    ln = Line([x, base + 0.45, 0], [x, top, 0], color=TEAL, stroke_width=3)
    g.add(ln)
    for y in ys[:-1]:
        g.add(Dot([x, y, 0], radius=0.1, color=TEAL))
    anc = Circle(radius=0.24, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9).move_to([x, top, 0])
    return g, anc


class S12Bacho(SpokenScene):
    def construct(self):
        self.add(motes(32))
        at = Atlas(0.8, 0.0, -0.5)
        land = at.land()
        self.play(Create(land), run_time=1.2)
        self.at("Cave in Bulgaria")
        p = pin_at(at.P(*PIN_BUL), TEXT, h=0.9)
        pos = p.get_center().copy()
        p.shift(UP * 1.0).set_opacity(0)
        self.play(p.animate.move_to(pos).set_opacity(1), run_time=0.7)
        cl = T("Bacho Kiro Cave", 36, TEXT, weight=BOLD).move_to(at.P(*PIN_BUL) + LEFT * 2.8 + UP * 0.4)
        self.play(FadeIn(cl, shift=RIGHT * 0.2), run_time=0.7)
        self.at("three early Homo sapiens")
        at2 = Atlas(0.25, 5.3, 2.4)
        land2 = at2.land()
        p2 = pin_at(at2.P(*PIN_BUL), TEXT, h=0.3)
        cl2 = T("Bacho Kiro Cave, Bulgaria", 28, TEXT).move_to([-6.3, 3.3, 0], aligned_edge=LEFT)
        self.play(ReplacementTransform(VGroup(land, p), VGroup(land2, p2)), FadeOut(cl), FadeIn(cl2), run_time=1.2)
        figs = VGroup(*[person(1.0).move_to([x, -2.0, 0]) for x in (-5.4, -3.6, -1.8)])
        self.play(LaggedStart(*[GrowFromCenter(f) for f in figs], lag_ratio=0.3), run_time=1.2)
        hs = T("early Homo sapiens", 30, TEAL).move_to([-3.6, -3.1, 0])
        self.play(FadeIn(hs), run_time=0.6)
        self.at("Each had a Neanderthal ancestor")
        trees = [tree(x) for x in (-5.4, -3.6, -1.8)]
        self.play(LaggedStart(*[GrowFromCenter(t[1]) for t in trees], lag_ratio=0.3), run_time=1.2)
        nl = T("Neanderthal ancestor", 28, ORANGE).move_to([-3.6, 2.0, 0])
        self.play(FadeIn(nl, shift=DOWN * 0.1), run_time=0.6)
        self.at("only a few generations back")
        self.play(LaggedStart(*[Create(t[0]) for t in trees], lag_ratio=0.3), run_time=1.6)
        self.play(FadeOut(nl), run_time=0.3)
        gt = T("about 7 generations or fewer", 28, GOLD).move_to([-3.6, 2.0, 0])
        self.play(FadeIn(gt, shift=DOWN * 0.1), run_time=0.7)
        self.at("That was a separate")
        st = tag("a separate, recent contact", 30, GOLD).move_to([1.3, 1.0, 0]).set_opacity(1)
        self.play(FadeIn(st, shift=LEFT * 0.2), *[Indicate(t[1], color=ORANGE, scale_factor=1.4) for t in trees], run_time=1.2)
        self.at("in their own family trees")
        self.play(*[Indicate(t[0], color=ORANGE) for t in trees], run_time=1.2)
        b = bar(0.1, [], h=1.0, x0=0.3, L=6.2)
        self.play(FadeIn(b), FadeOut(st), run_time=0.8)
        self.at("Their orange runs")
        runs = VGroup(*bar(0.1, [(0.06, 0.42), (0.52, 0.82), (0.9, 0.915), (0.95, 0.965)], h=1.0, x0=0.3, L=6.2, minw=0.1)[1:])
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in runs], lag_ratio=0.3), run_time=1.6)
        self.at("the longest of all")
        t1 = T("longest segments 17–54 cM", 30, ORANGE, weight=BOLD).move_to([3.4, -1.1, 0])
        t2 = T("(Hajdinjak et al., 2021)", 24, LBL).move_to([3.4, -2.0, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), FadeIn(t2), Indicate(runs, color=ORANGE), run_time=1.2)
        self.finish()


class S13Lineup(SpokenScene):
    def construct(self):
        self.add(motes(33))
        bars, labs, gens = lineup_objs()
        self.at("Line the three up")
        base = VGroup(*[VGroup(b[0]) for b in bars])
        self.play(LaggedStart(*[Create(b[0]) for b in bars], lag_ratio=0.3), FadeIn(labs), run_time=1.6)
        axis = Arrow([-6.55, 2.5, 0], [-6.55, -1.9, 0], buff=0, color=LBL, stroke_width=4)
        self.play(GrowArrow(axis), run_time=0.8)
        self.at("long runs")
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in bars[0][1:]], lag_ratio=0.3), FadeIn(gens[0]), run_time=1.4)
        self.at("medium pieces")
        self.play(LaggedStart(*[GrowFromCenter(r) for r in bars[1][1:]], lag_ratio=0.12), FadeIn(gens[1]), run_time=1.4)
        self.at("A living person")
        self.play(LaggedStart(*[GrowFromCenter(r) for r in bars[2][1:]], lag_ratio=0.1), FadeIn(gens[2]), run_time=1.8)
        sk = VGroup(stack(0, 8), stack(0, 5))
        self.at("The surplus was a clue")
        s1, s2 = stack(-5.4, 8), stack(-3.9, 5)
        mini = VGroup(s1, s2).scale(0.3).move_to([-5.0, -3.0, 0])
        ct = tag("clue", 28, GOLD).move_to([-3.4, -3.0, 0])
        self.play(FadeIn(mini), FadeIn(ct), run_time=1.0)
        self.add(schem())
        self.at("The lengths test it")
        br = Brace(bars, RIGHT, buff=0.15, color=GOLD)
        tt = VGroup(T("test", 30, GOLD, weight=BOLD), T("and date", 30, GOLD, weight=BOLD)).arrange(DOWN, buff=0.1).next_to(br, RIGHT, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(tt), run_time=1.2)
        self.play(Indicate(bars, color=ORANGE, scale_factor=1.02), run_time=1.2)
        self.finish()


class S14Scope(SpokenScene):
    def construct(self):
        self.add(motes(34))
        bars, labs, gens = lineup_objs()
        grp = VGroup(bars, labs, gens)
        self.add(grp)
        self.at("One caution travels")
        card = RoundedRectangle(corner_radius=0.2, width=7.4, height=4.0, stroke_color=GOLD, stroke_width=4,
                                fill_color=BG, fill_opacity=0.96).move_to([0.6, 0.0, 0])
        head = T("one caution", 40, GOLD, font=TITLE_FONT).move_to([0.6, 1.35, 0])
        card.shift(RIGHT * 9)
        self.play(grp.animate.set_opacity(0.3), card.animate.shift(LEFT * 9), run_time=1.4)
        self.play(FadeIn(head), run_time=0.6)
        self.at("It gives an average")
        l1 = T("average", 40, TEXT, weight=BOLD).move_to([0.6, 0.5, 0])
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.8)
        self.at("for one main period")
        l2 = T("one main period of mixing", 34, TEXT, weight=BOLD).move_to([0.6, -0.4, 0])
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.at("And it says when")
        l3 = T("when, not how much", 40, GOLD, weight=BOLD).move_to([0.6, -1.3, 0])
        self.play(FadeIn(l3, shift=UP * 0.15), run_time=0.8)
        self.at("not how much ancestry")
        self.play(Indicate(l3, color=GOLD), run_time=1.5)
        self.finish()


class S15End(EndCard):
    LINE = "Long segments mean recent mixing: length is the clock."
