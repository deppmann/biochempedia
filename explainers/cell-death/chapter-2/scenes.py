"""A Look Is Not a Cause: cell death, chapter 2.

COLOUR MAP (carried from chapter 1, one colour per concept)
  BLUE   plasma membrane          TEAL   caspases
  YELLOW phosphatidylserine       GREEN  phagocyte
  RED    spilled contents, alarms GREY   nucleus, outlines, machinery blocks
  new:   PURPLE annexin V clips   ORANGE propidium iodide dots
"""
import math
from bp_style import *  # noqa: F401,F403

PURPLE = "#A07BE0"
ORANGE = "#F29A3D"
WHITE = "#FFFFFF"
SPILL_BASE = 0.0


# ------------------------------------------------------------------ shared helpers
def P3(c):
    c = list(c)
    return np.array(c + [0.0] * (3 - len(c)), dtype=float)


def cue_run(scene, phrase, *anims, lead=0.2, minimum=0.3, **kw):
    """Play animations so that they end right when the phrase is about to be spoken."""
    t = max(minimum, scene.t_of(phrase) - lead - scene.elapsed())
    scene.play(*anims, run_time=t, **kw)


def at_t(scene, sec):
    rest = sec - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def pulse_stroke(m, base=9.0, swing=1.6, speed=1.4):
    m._pt = 0.0

    def up(mm, dt):
        mm._pt += dt
        mm.set_stroke(width=base + swing * math.sin(speed * mm._pt))
    m.add_updater(up)


def pulse_fill(m, color, base=0.17, swing=0.04, speed=1.3):
    m._ft = 0.0

    def up(mm, dt):
        mm._ft += dt
        mm.set_fill(color, opacity=base + swing * math.sin(speed * mm._ft))
    m.add_updater(up)


def bob(m, amp=0.06, speed=1.1, phase=0.0, axis=UP):
    """Slow ambient drift, incremental so it can coexist with animations."""
    m._bt = phase

    def up(mm, dt):
        old = math.sin(speed * mm._bt)
        mm._bt += dt
        mm.shift(axis * amp * (math.sin(speed * mm._bt) - old))
    m.add_updater(up)
    return m


def card(text, size=40, color=WHITE):
    t = T(text, size, color, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 0.7, height=t.height + 0.42,
                           stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=0.9)
    return VGroup(box, t.move_to(box))


def block(w=1.4, h=0.6, color=GREY, label=None, size=26, fill=0.35):
    b = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=fill)
    g = VGroup(b)
    if label:
        g.add(T(label, size, WHITE).move_to(b))
    return g


def scissors(scale=1.0, color=TEAL):
    a = Line(0.28 * DL, 0.38 * UR, color=color, stroke_width=5)
    b = Line(0.28 * UL, 0.38 * DR, color=color, stroke_width=5)
    h1 = Circle(radius=0.12, color=color, stroke_width=4).move_to(0.39 * DL)
    h2 = Circle(radius=0.12, color=color, stroke_width=4).move_to(0.39 * UL)
    return VGroup(a, b, h1, h2).scale(scale)


def nuc_at(c, r):
    return Circle(radius=r * 0.31, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.24).move_to(
        P3(c) + r * np.array([0.38, 0.34, 0]))


def intact(c, r, nuc=True, blk=False):
    """A sealed cell: body, ring, nucleus (and an unlabelled machinery block)."""
    c = P3(c)
    body = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.17).move_to(c)
    ring = Circle(radius=r, color=BLUE, stroke_width=9).move_to(c)
    pulse_fill(body, BLUE)
    pulse_stroke(ring)
    g = VGroup(body, ring)
    g.body, g.ring = body, ring
    g.nuc = nuc_at(c, r) if nuc else None
    if nuc:
        g.add(g.nuc)
    g.blk = None
    if blk:
        g.blk = block(r * 0.62, r * 0.30).move_to(c + r * np.array([-0.30, -0.42, 0]))
        g.add(g.blk)
    return g


def torn(c, r, g=-0.6, L=None, nuc=True, blk=False):
    """A torn cell: ring with a gap at angle g, RED contents seeping out of it slowly."""
    c = P3(c)
    L = L if L is not None else 0.75 * r
    body = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.10).move_to(c)
    arcs = Arc(radius=r, start_angle=g + 0.30, angle=TAU - 0.60, color=BLUE, stroke_width=9).move_arc_center_to(c)
    anchor = Dot(c, radius=0.001).set_opacity(0)
    k = ValueTracker(1.0)
    dots = VGroup()
    n = 8
    for i in range(n):
        d = Dot(radius=0.09 + 0.02 * (i % 2), color=RED)
        d.ph = i / n
        d.jit = ((i * 37) % 11 - 5) / 10.0
        d.arcs = arcs

        def up(m, dt, anchor=anchor, arcs=arcs, k=k):
            m.ph = (m.ph + dt * 0.11) % 1.0
            kk = k.get_value()
            cc = anchor.get_center()
            rr = arcs.width / 2
            dv = np.array([math.cos(g), math.sin(g), 0])
            pp = np.array([-dv[1], dv[0], 0])
            m.move_to(cc + (rr + 0.04) * dv + dv * L * m.ph * kk * (rr / r) + pp * m.jit * 0.45 * m.ph * (rr / r))
            m.set_opacity(max(0.0, min(1.0, (1 - m.ph) * 1.6, kk * 2)))
        d.add_updater(up)
        dots.add(d)
    pulse_stroke(arcs, 9, 0.8, 1.0)
    grp = VGroup(body, arcs)
    grp.body, grp.ring = body, arcs
    grp.nuc = nuc_at(c, r) if nuc else None
    if nuc:
        grp.add(grp.nuc)
    grp.blk = None
    if blk:
        grp.blk = block(r * 0.62, r * 0.30).move_to(c + r * np.array([-0.30, -0.42, 0]))
        grp.add(grp.blk)
    grp.add(anchor, dots)
    grp.k, grp.dots, grp.anchor = k, dots, anchor
    return grp


def scale_about(m, factor, point):
    return m.animate.scale(factor, about_point=np.array(point, dtype=float))


def apop(c, r):
    """Shrunken apoptotic cell from chapter 1: blue ring, nucleus pieces, teal scissors, two blebs."""
    c = P3(c)
    f = r / 2.18
    ring = Circle(radius=r, color=BLUE, stroke_width=9, fill_color=BLUE, fill_opacity=0.17).move_to(c)
    pulse_stroke(ring)
    frags = VGroup(*[Circle(radius=0.18 * f, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.38).move_to(c + f * np.array(d))
                     for d in ([-0.35, 0.26, 0], [0.22, 0.32, 0], [-0.18, -0.27, 0], [0.34, -0.22, 0])])
    sc = VGroup(scissors(0.72 * f).move_to(c + f * np.array([-0.46, 0.34, 0])),
                scissors(0.64 * f).move_to(c + f * np.array([0.50, -0.26, 0])))
    bl = VGroup(Circle(radius=0.31 * f, color=BLUE, stroke_width=6, fill_color=BLUE, fill_opacity=0.04).move_to(c + f * np.array([r / f + 0.23, 0.42, 0])),
                Circle(radius=0.23 * f, color=BLUE, stroke_width=6, fill_color=BLUE, fill_opacity=0.04).move_to(c + f * np.array([-0.52, r / f + 0.13, 0])))
    return VGroup(ring, frags, sc, bl)


def phagocyte(c, r):
    c = P3(c)
    edge = Circle(radius=r, color=GREEN, stroke_width=8, fill_color=GREEN, fill_opacity=0.18).move_to(c)
    pulse_fill(edge, GREEN, 0.18, 0.03)
    return edge


def pair_state():
    """End of the hook: sealed-and-eaten pair on the left, torn cell on the right."""
    ph = phagocyte([-3.7, -0.9], 1.7)
    inner = apop([-3.7, -0.9], 0.62)
    lab1 = T("sealed and eaten", 30, WHITE).move_to([-3.7, -3.05, 0])
    t = torn([3.0, -0.9], 1.5, g=-0.6, L=1.3)
    lab2 = T("torn early", 30, WHITE).move_to([3.0, -3.05, 0])
    return ph, inner, lab1, t, lab2


# ------------------------------------------------------------------ chapter 2 scenes
class S00Hook(SpokenScene):
    def construct(self):
        big = torn([0, -0.2], 2.7, g=-0.6, L=2.2)
        self.play(FadeIn(big, scale=0.85), run_time=1.2)
        self.at("what killed it")
        q = card("What killed it?", 44).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        self.at("an accident")
        a = T("accident?", 36, WHITE, weight=BOLD).move_to([-5.9, 0.6, 0])
        p = T("program?", 36, WHITE, weight=BOLD).move_to([5.9, 0.6, 0])
        for m, ph in ((a, 0), (p, 1.5)):
            m._t = ph

            def up(mm, dt):
                mm._t += dt
                mm.set_opacity(0.7 + 0.3 * math.sin(2.6 * mm._t))
            m.add_updater(up)
        self.play(a.animate.move_to([-4.85, 0.6, 0]), run_time=0.9)
        self.at("a program")
        self.play(p.animate.move_to([4.85, 0.6, 0]), run_time=0.9)
        self.wait(0.2)
        self.at("chapter 1 showed")
        ph, inner, lab1, t, lab2 = pair_state()
        self.play(FadeOut(a), FadeOut(p),
                  scale_about(big, 1.5 / 2.7, [0, -0.2, 0]),
                  run_time=0.9)
        self.play(big.animate.shift(np.array([3.0, -0.9, 0]) - np.array([0, -0.2, 0])), run_time=1.1)
        self.at("a peptotic cell")
        self.play(FadeIn(ph, shift=RIGHT * 0.4), FadeIn(inner, shift=RIGHT * 0.4), run_time=1.0)
        self.play(FadeIn(lab1), run_time=0.5)
        self.at("a necrotic cell")
        self.play(FadeIn(lab2), Indicate(big.ring, color=BLUE, scale_factor=1.04), run_time=0.9)
        self.play(FadeOut(q), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        ph, inner, lab1, t, lab2 = pair_state()
        self.add(ph, inner, lab1, t, lab2)
        title = T("A Look Is Not a Cause", 56, WHITE, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.wait(1.2)


class S02Pair(SpokenScene):
    def construct(self):
        ph, inner, lab1, t, lab2 = pair_state()
        self.add(ph, inner, lab1, t, lab2)
        right_c = np.array([3.3, -0.5, 0])
        left_c = np.array([-3.3, -0.5, 0])
        a = apop(left_c, 1.8).shift(LEFT * 4)
        self.play(FadeOut(ph), FadeOut(inner), FadeOut(lab1), FadeOut(lab2),
                  scale_about(t, 1.8 / 1.5, [3.0, -0.9, 0]),
                  a.animate.shift(RIGHT * 4), run_time=1.6)
        self.play(t.animate.shift(right_c - np.array([3.0 + 0.0, -0.9, 0])), run_time=0.5)
        self.at("taught as a pair")
        lb = VGroup(Line([-3.3, 2.4, 0], [-3.3, 2.8, 0]), Line([-3.3, 2.8, 0], [0, 2.8, 0])).set_stroke(WHITE, 5)
        rb = VGroup(Line([0, 2.8, 0], [3.3, 2.8, 0]), Line([3.3, 2.8, 0], [3.3, 2.4, 0])).set_stroke(WHITE, 5)
        pair_l = T("taught as a pair", 34, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        self.play(Create(lb), Create(rb), run_time=0.9)
        self.play(FadeIn(pair_l, shift=DOWN * 0.1), run_time=0.5)
        self.at("1972")
        tag = T("1972: Kerr, Wyllie, Currie", 28, WHITE).move_to([-3.3, 1.95, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.6)
        self.at("was the programmed")
        al = T("apoptosis: programmed", 30, WHITE).move_to([-3.3, -2.85, 0])
        self.play(Write(al), run_time=1.0)
        self.at("the accident")
        n1 = T("necrosis:", 30, WHITE)
        n2 = T("accident", 30, WHITE)
        nl = VGroup(n1, n2).arrange(RIGHT, buff=0.2).move_to([3.3, -2.85, 0])
        self.play(Write(nl), run_time=0.9)
        self.at("has not survived")
        strike = Line(n2.get_left() + LEFT * 0.08, n2.get_right() + RIGHT * 0.08, color=WHITE, stroke_width=6)
        self.play(Create(strike), run_time=0.5)
        self.play(FadeOut(n2), FadeOut(strike), lb.animate.shift(LEFT * 0.25 + UP * 0.1).set_opacity(0.45),
                  rb.animate.shift(RIGHT * 0.25 + UP * 0.1).set_opacity(0.45), run_time=0.9)
        self.finish()


def machinery_dial(c, r):
    """Unlabelled grey block and a white dial, driven by one tracker."""
    v = ValueTracker(0.0)
    blk = block(r * 0.62, r * 0.34).move_to(P3(c) + r * np.array([-0.32, -0.45, 0]))
    dc = P3(c) + r * np.array([0.34, -0.45, 0])
    face = Circle(radius=0.38, color=WHITE, stroke_width=4).move_to(dc)
    needle = Line(ORIGIN, RIGHT * 0.3, color=WHITE, stroke_width=6)

    def nd(m):
        ang = math.radians(210 - 180 * v.get_value())
        m.put_start_and_end_on(dc, dc + 0.3 * np.array([math.cos(ang), math.sin(ang), 0]))
    needle.add_updater(nd)

    def br(m):
        x = v.get_value()
        m.set_fill(interpolate_color(ManimColor(GREY), ManimColor(WHITE), x), opacity=0.15 + 0.6 * x)
        m.set_stroke(interpolate_color(ManimColor(GREY), ManimColor(WHITE), x), width=3 + 2 * x)
    blk[0].add_updater(br)
    return v, blk, VGroup(face, needle)


class S03Regulated(SpokenScene):
    def construct(self):
        c, r = np.array([0, -0.2, 0]), 2.1
        cell = intact(c, r)
        self.play(FadeIn(cell, scale=0.9), run_time=1.0)
        self.at("dedicated machinery")
        v, blk, dial = machinery_dial(c, r)
        self.play(FadeIn(blk, scale=0.8), FadeIn(dial), run_time=0.8)
        bob(blk, 0.05)
        self.at("genes or drugs")
        gene = chip("gene change", WHITE, 30).move_to([-4.7, 0.6, 0])
        self.play(FadeIn(gene, shift=RIGHT * 0.3), run_time=0.45)
        self.play(v.animate.set_value(1), run_time=0.75)
        self.play(v.animate.set_value(0), run_time=0.75)
        pill = VGroup(
            RoundedRectangle(corner_radius=0.17, width=0.9, height=0.36, stroke_color=WHITE, stroke_width=3,
                             fill_color=WHITE, fill_opacity=0.15),
            Line([0, -0.18, 0], [0, 0.18, 0], color=WHITE, stroke_width=3),
        ).rotate(0.5).move_to([4.7, 0.6, 0])
        self.play(FadeOut(gene), FadeIn(pill, shift=LEFT * 0.3), run_time=0.45)
        self.play(v.animate.set_value(1), run_time=0.7)
        self.play(v.animate.set_value(0), run_time=0.7)
        lab = T("regulated: dedicated machinery", 36, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        self.play(FadeOut(pill), FadeIn(lab, shift=DOWN * 0.1), v.animate.set_value(0.5), run_time=0.6)
        self.at("still look necrotic")
        self.play(scale_about(VGroup(cell, blk, dial), 1.4, c), v.animate.set_value(1.0), run_time=1.0)
        nr = c
        tr = torn(nr, r * 1.4, g=-0.4, L=1.6, nuc=False)
        tr.nuc = None
        self.remove(cell.body, cell.ring)
        cell.remove(cell.body, cell.ring)
        self.add(tr)
        self.play(Indicate(tr.ring, color=BLUE, scale_factor=1.03), run_time=0.8)
        self.at("three such deaths")
        three = []
        for x in (-4.3, 0, 4.3):
            cc = intact(c, r, blk=True)
            three.append((x, cc))
        self.play(FadeOut(VGroup(tr, cell, blk, dial, lab)), *[FadeIn(cc, scale=0.9) for x, cc in three], run_time=0.6)
        for x, cc in three:
            cc.scale(1.75 / r, about_point=c)
        self.play(*[cc.animate.shift(np.array([x, 0.4, 0]) - c) for x, cc in three], run_time=1.4)
        labs = VGroup(*[T(str(i + 1), 48, WHITE, weight=BOLD).move_to([x, -2.35, 0]) for i, (x, cc) in enumerate(three)])
        self.play(FadeIn(labs, shift=UP * 0.15), run_time=0.8)
        self.finish()


ROW = (-4.3, 0.0, 4.3)
ROW_Y = 0.4
ROW_R = 1.75
BIG_C = np.array([0, -0.1, 0])
BIG_R = 2.6


def row_cells():
    return [intact([x, ROW_Y], ROW_R, blk=True) for x in ROW]


def big_cell_setup(scene, cell, ripk=False):
    """Move a row cell to the centre as a big cell (the camera move)."""
    src = np.array([cell.ring.get_center()[0], ROW_Y, 0])
    return [scale_about(cell, BIG_R / ROW_R, src), ]


class S04Necroptosis(SpokenScene):
    def construct(self):
        cells = row_cells()
        labs = VGroup(*[T(str(i + 1), 48, WHITE, weight=BOLD).move_to([x, -2.35, 0]) for i, x in enumerate(ROW)])
        self.add(*cells, labs)
        c1 = cells[0]
        src = np.array([ROW[0], ROW_Y, 0])
        self.play(FadeOut(cells[1]), FadeOut(cells[2]), FadeOut(labs), FadeOut(c1.blk), run_time=0.6)
        c1.remove(c1.blk)
        c1.scale(BIG_R / ROW_R, about_point=src)
        self.play(c1.animate.shift(BIG_C - src), run_time=1.4)
        rip = block(1.5, 0.62, GREY).move_to(BIG_C + np.array([-1.2, 0.7, 0]))
        mlk = block(1.5, 0.62, GREY).move_to(BIG_C + np.array([-0.5, -1.15, 0]))
        self.play(FadeIn(rip, scale=0.8), FadeIn(mlk, scale=0.8), run_time=0.9)
        bob(rip, 0.05, 1.0, 0.0)
        bob(mlk, 0.05, 1.2, 1.0)
        self.at("activated")
        rl = T("RIPK3", 28, WHITE, weight=BOLD).move_to(rip)
        self.play(FadeIn(rl), rip.animate.set_fill(GREY, 0.6), run_time=0.7)
        self.at("adds phosphate")
        ptag = Circle(radius=0.24, color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(rip.get_bottom() + DOWN * 0.1)
        ptxt = T("P", 26, WHITE, weight=BOLD).move_to(ptag)
        pg = VGroup(ptag, ptxt)
        self.play(FadeIn(pg, scale=0.5), run_time=0.35)
        self.play(pg.animate.move_to(mlk.get_top() + UP * 0.18), run_time=0.7)
        ml = T("MLKL", 28, WHITE, weight=BOLD).move_to(mlk)
        self.play(FadeIn(ml), mlk[0].animate.set_fill(WHITE, 0.45).set_stroke(WHITE), run_time=0.7)
        self.play(FadeOut(pg), run_time=0.3)
        self.at("clusters of")
        small = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.3, stroke_color=WHITE, stroke_width=3,
                                          fill_color=WHITE, fill_opacity=0.4).move_to(mlk.get_center() + 0.35 * np.array([math.cos(i), math.sin(i), 0]) )
                         for i in range(6)])
        self.play(FadeOut(ml), ReplacementTransform(mlk, small), run_time=0.7)
        # three clusters of two
        cl = []
        angs = (math.radians(205), math.radians(245), math.radians(285))
        for i in range(3):
            tgt = BIG_C + (BIG_R - 0.35) * np.array([math.cos(angs[i]), math.sin(angs[i]), 0])
            cl.append(tgt)
        self.play(*[small[2 * i].animate.move_to(BIG_C + 0.9 * np.array([math.cos(angs[i]), math.sin(angs[i]), 0]) + 0.2 * LEFT) for i in range(3)],
                  *[small[2 * i + 1].animate.move_to(BIG_C + 0.9 * np.array([math.cos(angs[i]), math.sin(angs[i]), 0]) + 0.2 * RIGHT) for i in range(3)],
                  run_time=1.0)
        self.at("plasma membrane")
        moves = []
        for i in range(3):
            a = angs[i]
            n = np.array([math.cos(a), math.sin(a), 0])
            tg = np.array([-math.sin(a), math.cos(a), 0])
            moves.append(small[2 * i].animate.move_to(BIG_C + (BIG_R - 0.32) * n - 0.17 * tg).rotate(a + PI / 2))
            moves.append(small[2 * i + 1].animate.move_to(BIG_C + (BIG_R - 0.32) * n + 0.17 * tg).rotate(a + PI / 2))
        self.play(*moves, run_time=1.5)
        lab = T("necroptosis", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        tag = T("mammalian model", 28, WHITE).move_to([0, -3.4, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(tag), run_time=0.5)
        self.finish()


def cell1_final():
    ring = Circle(radius=BIG_R, color=BLUE, stroke_width=9, fill_color=BLUE, fill_opacity=0.17).move_to(BIG_C)
    nuc = Circle(radius=0.8, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.24).move_to(BIG_C + np.array([1.0, 0.9, 0]))
    rip = block(1.5, 0.62, GREY, "RIPK3").move_to(BIG_C + np.array([-1.2, 0.7, 0]))
    clus = VGroup()
    for a in (math.radians(205), math.radians(245), math.radians(285)):
        n = np.array([math.cos(a), math.sin(a), 0])
        tg = np.array([-math.sin(a), math.cos(a), 0])
        for s in (-1, 1):
            clus.add(RoundedRectangle(corner_radius=0.08, width=0.5, height=0.3, stroke_color=WHITE, stroke_width=3,
                                      fill_color=WHITE, fill_opacity=0.4).rotate(a + PI / 2).move_to(BIG_C + (BIG_R - 0.32) * n + 0.17 * s * tg))
    lab = T("necroptosis", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0])
    return VGroup(ring, nuc, rip, clus, lab)


def ring_patch(c, r, ang):
    n = np.array([math.cos(ang), math.sin(ang), 0])
    p = Rectangle(width=0.3, height=0.62, stroke_width=0, fill_color=BG, fill_opacity=1)
    p.rotate(ang).move_to(P3(c) + r * n)
    return p


def streamer(origin, direction, n=3, L=1.8, speed=0.22, active=None):
    """RED dots cycling outward from a pore. Stateless in position, gated by active tracker."""
    dots = VGroup()
    for i in range(n):
        d = Dot(radius=0.09, color=RED)
        d.ph = i / n
        d.jit = ((i * 7) % 5 - 2) / 8.0

        def up(m, dt):
            m.ph = (m.ph + dt * speed) % 1.0
            a = active.get_value() if active else 1.0
            m.move_to(np.array(origin) + direction * L * m.ph + UP * m.jit * m.ph)
            m.set_opacity(max(0, 1 - m.ph) * a)
        d.add_updater(up)
        dots.add(d)
    return dots


class S05Pyroptosis(SpokenScene):
    def construct(self):
        old = cell1_final()
        self.add(old)
        cell2 = intact(BIG_C, BIG_R)
        cell2.shift(RIGHT * 9)
        self.play(old.animate.shift(LEFT * 9), cell2.animate.shift(LEFT * 9), run_time=1.3)
        self.remove(old)
        gl = [(-1.3, 0.85), (-1.0, -0.45), (0.8, -1.4)]
        gds = [block(1.3, 0.42, GREY).move_to(BIG_C + np.array([x, y, 0])) for x, y in gl]
        gtxt = T("gasdermin", 24, WHITE).move_to(BIG_C + np.array([0.9, -0.3, 0]))
        sc = scissors(1.2).move_to([-4.6, 2.3, 0])
        self.play(*[FadeIn(g, scale=0.8) for g in gds], FadeIn(gtxt), FadeIn(sc), run_time=0.6)
        for g in gds:
            bob(g, 0.04, 1.0, g.get_x())
        halves = []
        pores = []
        pang = [math.radians(a) for a in (35, 0, -35)]
        for i, g in enumerate(gds):
            self.play(sc.animate.move_to(g.get_center() + 0.0 * UP), run_time=0.4)
            lh = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.42, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.4).move_to(g.get_center() + 0.35 * LEFT)
            rh = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.42, stroke_color=WHITE, stroke_width=3,
                                  fill_color=WHITE, fill_opacity=0.5).move_to(g.get_center() + 0.35 * RIGHT)
            self.play(Indicate(sc, color=TEAL, scale_factor=1.3), FadeOut(g), FadeIn(lh), FadeIn(rh), run_time=0.3)
            halves.append((lh, rh))
        # one freed piece from each travels to the membrane band
        self.at("freeing fragments")
        mv = []
        for i, (lh, rh) in enumerate(halves):
            n = np.array([math.cos(pang[i]), math.sin(pang[i]), 0])
            mv.append(rh.animate.move_to(BIG_C + (BIG_R - 0.3) * n).rotate(pang[i]))
        self.play(*mv, FadeOut(gtxt), sc.animate.move_to([-4.6, 2.3, 0]), run_time=1.3)
        self.at("form pores")
        act = ValueTracker(0.0)
        patches = VGroup(*[ring_patch(BIG_C, BIG_R, a) for a in pang])
        self.add(patches)
        self.play(FadeIn(patches, scale=0.5), FadeOut(VGroup(*[rh for lh, rh in halves])), run_time=0.8)
        self.add(patches)
        outs = VGroup(*[streamer(BIG_C + (BIG_R + 0.05) * np.array([math.cos(a), math.sin(a), 0]), RIGHT, 3, 1.8, 0.2, act) for a in pang])
        self.add(outs)
        pl = T("pores", 30, WHITE, weight=BOLD).move_to([4.3, 2.45, 0])
        self.play(act.animate.set_value(1.0), FadeIn(pl), run_time=1.0)
        pyro = T("pyroptosis", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        self.play(FadeIn(pyro, shift=DOWN * 0.1), FadeOut(VGroup(*[lh for lh, rh in halves])), run_time=0.6)
        self.at("often but not always")
        tag = T("often, not always", 26, WHITE).move_to([-4.6, -0.1, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.at("inflammatory")
        cl = T("inflammatory\ncaspases", 28, TEAL, weight=BOLD, line_spacing=0.8).move_to([-4.6, 0.95, 0])
        self.play(FadeIn(cl), Indicate(sc, color=TEAL, scale_factor=1.3), run_time=0.8)
        self.finish()


class S06Ferroptosis(SpokenScene):
    def construct(self):
        # carry cell 2 out, cell 3 in
        out2 = VGroup(
            Circle(radius=BIG_R, color=BLUE, stroke_width=9, fill_color=BLUE, fill_opacity=0.17).move_to(BIG_C),
            T("pyroptosis", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0]))
        for a in (35, 0, -35):
            out2.add(ring_patch(BIG_C, BIG_R, math.radians(a)))
        self.add(out2)
        cell3 = intact(BIG_C, BIG_R)
        cell3.shift(RIGHT * 9)
        self.play(out2.animate.shift(LEFT * 9), cell3.animate.shift(LEFT * 9), run_time=1.5)
        self.remove(out2)
        self.at("driven by")
        flab = T("ferroptosis", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        band = Arc(radius=7.6, start_angle=PI / 2 - 0.85, angle=1.7, color=BLUE, stroke_width=34).move_arc_center_to([0, -7.4, 0])
        self.play(FadeOut(cell3.body), FadeOut(cell3.nuc), ReplacementTransform(cell3.ring, band), FadeIn(flab), run_time=1.4)
        self.at("iron dependent")
        iron = Dot([0, 1.5, 0], radius=0.17, color=GREY)
        il = T("iron", 28, WHITE).move_to([0, 2.05, 0])
        self.play(FadeIn(iron, scale=2.0), FadeIn(il), run_time=0.6)
        bob(iron, 0.05)
        ang_list = [0.18, -0.22, 0.47]
        patches = VGroup()

        def pt(a):
            return np.array([0, -7.4, 0]) + 7.6 * np.array([math.sin(a), math.cos(a), 0])

        def patch(a):
            n = np.array([math.sin(a), math.cos(a), 0])
            tg = np.array([math.cos(a), -math.sin(a), 0])
            g = VGroup(Arc(radius=7.6, start_angle=PI / 2 - a - 0.05, angle=0.1, color=RED, stroke_width=42).move_arc_center_to([0, -7.4, 0]))
            for j, s in enumerate((-0.12, 0.0, 0.12)):
                p0 = pt(a) + tg * s * 1.3
                g.add(Line(p0 + n * 0.12, p0 + n * (0.34 + 0.1 * (j % 2)) + tg * 0.06, color=RED, stroke_width=5))
            return g
        spark = Dot([0, 1.5, 0], radius=0.13, color=WHITE)
        self.add(spark)
        for i, a in enumerate(ang_list):
            self.play(spark.animate(path_arc=-1.0).move_to(pt(a) + UP * 0.15), run_time=0.45)
            pa = patch(a)
            patches.add(pa)
            self.play(FadeIn(pa), run_time=0.2)
            self.play(spark.animate(path_arc=1.0).move_to([0.1 * i, 1.5, 0]), run_time=0.45)
            if i == 0:
                self.at("lipids")
                dl = T("lipid damage", 32, WHITE, weight=BOLD).move_to([4.2, 0.95, 0])
                self.dl = dl
                self.play(FadeIn(dl), run_time=0.5)
        self.at("gpx4")
        gp = block(1.5, 0.64, GREY, "GPX4", 28).move_to([-4.2, 1.2, 0])
        self.play(FadeIn(gp, scale=0.8), run_time=0.7)
        bob(gp, 0.05)
        self.at("reducing damaging")
        b1 = T("lipid hydroperoxide", 26, RED).move_to([-4.2, 2.35, 0])
        self.play(FadeIn(b1, shift=DOWN * 0.1), run_time=0.7)
        at_t(self, self.t_of("reducing damaging") + 1.5)
        b2 = T("reduced lipid product", 26, TEXT).move_to([-4.2, 2.35, 0])
        self.play(ReplacementTransform(b1, b2), gp[0].animate.set_fill(WHITE, 0.5), run_time=0.8)
        self.at("drugs that trap iron")
        cage = VGroup(*[Line([x, -0.3, 0], [x, 0.3, 0], color=WHITE, stroke_width=5) for x in (-0.3, -0.1, 0.1, 0.3)],
                      Line([-0.34, 0.3, 0], [0.34, 0.3, 0], color=WHITE, stroke_width=6),
                      Line([-0.34, -0.3, 0], [0.34, -0.3, 0], color=WHITE, stroke_width=6)).move_to([0, 3.2, 0])
        self.play(cage.animate.move_to(iron.get_center()), spark.animate.move_to([0.5, 1.5, 0]), run_time=1.0)
        self.play(FadeOut(spark), FadeOut(patches), FadeOut(self.dl), run_time=0.6)
        ct = T("cultured cells", 26, WHITE).move_to([2.6, 1.5, 0])
        self.play(FadeIn(ct), run_time=0.5)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        cells = []
        for x in ROW:
            cells.append(torn([x, -0.3], 1.9, g=-1.4, L=1.0, nuc=False))
        for cc in cells:
            self.add(cc)
        rip = block(1.1, 0.46, GREY, "RIPK3", 24).move_to([ROW[0] - 0.1, 0.1, 0])
        self.add(rip)
        self.wait(1.0)
        self.at("a death's look")
        rule = T("Look = endpoint, not cause", 44, WHITE, weight=BOLD).move_to([0, 3.4, 0])
        self.play(Write(rule), run_time=1.6)
        self.at("block the machinery")
        bar = RoundedRectangle(corner_radius=0.05, width=1.25, height=0.1, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(rip.get_center() + LEFT * 1.4 + UP * 0.36)
        blk_l = T("blocked", 26, WHITE).next_to(rip, DOWN, buff=0.15)
        self.play(bar.animate.move_to(rip.get_center() + UP * 0.36), FadeIn(blk_l), run_time=0.8)
        c1 = cells[0]
        circ = Circle(radius=1.75, color=BLUE, stroke_width=9).move_to([ROW[0], -0.3, 0])
        self.play(Transform(c1.ring, circ), c1.k.animate.set_value(0), c1.body.animate.set_fill(BLUE, 0.17),
                  scale_about(VGroup(c1.body, c1.ring), 1.75 / 1.9, [ROW[0], -0.3, 0]), run_time=1.7)
        dl = T("death changed", 32, WHITE, weight=BOLD).move_to([ROW[0], -2.75, 0])
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.6)
        self.finish()


def dish_group(c=(-1.5, 0.0), R=3.55, clips=True, ring_color=BLUE):
    c = np.array([c[0], c[1], 0.0])
    dish = Circle(radius=R, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.18).move_to(c)
    cell = apop(c, 1.35)
    heads = VGroup(*[Dot(c + (1.35 + 0.08) * np.array([math.cos(a), math.sin(a), 0]), radius=0.085, color=YELLOW)
                     for a in np.linspace(0, TAU, 9, endpoint=False)])
    return dish, cell, heads


class S08Dyes(SpokenScene):
    def construct(self):
        c = np.array([-1.5, 0.0, 0.0])
        dish, cell, heads = dish_group()
        self.play(FadeIn(dish, scale=0.9), run_time=1.0)
        self.play(FadeIn(cell, scale=0.5), run_time=0.9)
        self.add(heads)
        heads.add_updater(lambda m, dt, c=c: m.rotate(0.22 * dt, about_point=c))
        self.play(FadeIn(heads, scale=0.5), run_time=0.7)
        self.at("two dyes")
        # clips arrive at yellow heads
        clips = VGroup()
        for i, h in enumerate(heads):
            a = math.atan2(*(h.get_center() - c)[1::-1])
            start = c + 3.0 * np.array([math.cos(a + 0.35), math.sin(a + 0.35), 0])
            cp = Arc(radius=0.26, start_angle=a + PI / 2 - 1.1, angle=2.2, color=PURPLE, stroke_width=10).move_arc_center_to(start)
            clips.add(cp)
        self.add(clips)
        for i, cp in enumerate(clips):
            bob(cp, 0.35, 1.2 + 0.1 * i, i, axis=np.array([math.cos(i), math.sin(i), 0]))
        self.play(FadeIn(clips), run_time=0.5)
        part = []
        for i, h in enumerate(heads):
            part.append(clips[i].animate.shift(-0.45 * (clips[i].get_center() - h.get_center())))
        cue_run(self, "anaxin", *part, rate_func=linear)
        movers = []
        for i, h in enumerate(heads):
            a = math.atan2(*(h.get_center() - c)[1::-1])
            movers.append(clips[i].animate.move_arc_center_to(h.get_center() + 0.1 * np.array([math.cos(a), math.sin(a), 0])))
        self.play(*movers, run_time=2.0)
        ring_p = Circle(radius=1.35 + 0.28, color=PURPLE, stroke_width=6).move_to(c)
        clips.add_updater(lambda m, dt, c=c: m.rotate(0.22 * dt, about_point=c))
        al = T("annexin V: flag", 32, PURPLE, weight=BOLD).move_to([4.4, 1.5, 0])
        self.play(Create(ring_p), FadeIn(al, shift=LEFT * 0.2), run_time=1.0)
        self.at("propidium iodide")
        dots = VGroup()
        rng = [(1.0, 2.2), (-0.8, 2.6), (2.0, 1.0), (-2.4, -1.2), (0.5, -2.5), (-2.9, 0.4), (2.3, -1.2), (-0.3, 2.9)]
        for i, (dx, dy) in enumerate(rng):
            d = Dot(c + np.array([dx, dy, 0]), radius=0.1, color=ORANGE)
            ang = math.radians(40 + 45 * i)
            d.v = np.array([math.cos(ang), math.sin(ang), 0]) * (0.6 + 0.06 * i)

            def up(m, dt, c=c):
                m.shift(m.v * dt)
                dv = m.get_center() - c
                dist = np.linalg.norm(dv)
                lim = 1.35 + 0.28 + 0.15
                if dist < lim:
                    nn = dv / max(dist, 1e-6)
                    m.v = m.v - 2 * np.dot(m.v, nn) * nn
                    m.move_to(c + nn * lim)
                if dist > 3.2:
                    nn = dv / dist
                    m.v = m.v - 2 * np.dot(m.v, nn) * nn
                    m.move_to(c + nn * 3.15)
            d.add_updater(up)
            dots.add(d)
        self.add(dots)
        self.play(FadeIn(dots), run_time=0.8)
        pl = T("propidium iodide", 32, ORANGE, weight=BOLD).move_to([4.4, -1.5, 0])
        self.play(FadeIn(pl, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


def grid_parts():
    x0, x1, y0, y1 = -3.5, 6.1, -2.9, 2.9
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    boxes = VGroup()
    for xa, xb, ya, yb in ((x0, xm, y0, ym), (xm, x1, y0, ym), (x0, xm, ym, y1), (xm, x1, ym, y1)):
        boxes.add(Rectangle(width=xb - xa, height=yb - ya, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([(xa + xb) / 2, (ya + yb) / 2, 0]))
    names = ["neither", "leak only", "flag only", "flag + leak"]
    tags = VGroup()
    for b, nme in zip(boxes, names):
        tags.add(T(nme, 26, WHITE).move_to(b.get_corner(UL) + np.array([0.18 + 0.0, -0.3, 0]), aligned_edge=LEFT))
    for t, b in zip(tags, boxes):
        t.move_to(b.get_center() + np.array([0, b.height / 2 - 0.35, 0]))
    xl = T("PI (leak)", 30, ORANGE, weight=BOLD).move_to([xm, -3.45, 0])
    yl = T("annexin V (flag)", 30, PURPLE, weight=BOLD).rotate(PI / 2).move_to([-4.15, ym, 0])
    return boxes, tags, xl, yl, boxes[2].get_center() + DOWN * 0.2, boxes[3].get_center() + DOWN * 0.2


class S09Boxes(SpokenScene):
    def construct(self):
        c = np.array([-1.5, 0.0, 0.0])
        dish, cell, heads = dish_group()
        ring_p = Circle(radius=1.35 + 0.28, color=PURPLE, stroke_width=6).move_to(c)
        clips = VGroup(*[Arc(radius=0.17, start_angle=0, angle=2.2, color=PURPLE, stroke_width=7).move_arc_center_to(h.get_center()) for h in heads])
        world = VGroup(dish, cell, heads, ring_p, clips)
        self.add(world)
        boxes, tags, xl, yl, p_flag, p_both = grid_parts()
        corner = np.array([-5.4, 2.45, 0])
        self.play(world.animate.scale(0.34, about_point=c).shift(corner - c), run_time=1.4)
        self.play(FadeIn(boxes), FadeIn(xl), FadeIn(yl), run_time=1.0)
        self.at("one of four boxes")
        self.play(FadeIn(tags), run_time=0.8)
        wd = Dot(corner, radius=0.2, color=WHITE)
        self.at("often becomes flagged")
        self.play(FadeIn(wd, scale=2), run_time=0.4)
        self.play(wd.animate(path_arc=-0.6).move_to(p_flag), run_time=1.5)
        bob(wd, 0.04, 1.3)
        clk_c = np.array([-5.6, -1.7, 0.0])
        self.at("after secondary")
        face = Circle(radius=0.45, color=WHITE, stroke_width=3).move_to(clk_c)
        hand = Line(clk_c, clk_c + 0.32 * UP, color=WHITE, stroke_width=4)
        ct = T("time\n(schematic)", 24, WHITE, line_spacing=0.8).move_to(clk_c + DOWN * 1.0)
        self.play(FadeIn(VGroup(face, hand, ct)), run_time=0.3)
        sc_c = corner
        dcell_c = world[1][0].get_center()
        orange = VGroup(*[Dot(dcell_c + 0.75 * np.array([math.cos(a), math.sin(a), 0]), radius=0.05, color=ORANGE) for a in np.linspace(0, TAU, 7, endpoint=False)])
        torn_ring = Arc(radius=1.35 * 0.34, start_angle=0.3, angle=TAU - 0.6, color=BLUE, stroke_width=6).move_arc_center_to(dcell_c)
        self.play(Rotate(hand, angle=-TAU, about_point=clk_c), FadeIn(orange), run_time=1.1, rate_func=linear)
        self.play(FadeOut(world[1][0]), FadeIn(torn_ring), *[o.animate.move_to(dcell_c) for o in orange], run_time=0.8)
        glow = Circle(radius=0.2, color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.8).move_to(dcell_c)
        self.at("flagged and leaky")
        self.play(FadeIn(glow), wd.animate.move_to(p_both), run_time=1.3)
        self.at("staining states")
        sv = card("state, not verdict", 40).move_to([1.3, -1.5, 0])
        self.play(FadeIn(sv, scale=0.9), run_time=0.8)
        self.finish()


def dna_line(y, x0, x1):
    return Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=8)


class S10Markers(SpokenScene):
    def construct(self):
        xs = (-4.55, 0.0, 4.55)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.2, height=5.7, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.08).move_to([x, 0, 0]) for x in xs])
        self.play(FadeIn(cards, shift=UP * 0.2, lag_ratio=0.25), run_time=1.4)
        at_t(self, 1.6)
        # card 1: DNA snaps, free ends glow
        x = xs[0]
        dna = VGroup(dna_line(0.9, x - 1.7, x - 0.9), dna_line(0.9, x - 0.9, x - 0.1), dna_line(0.9, x - 0.1, x + 0.7), dna_line(0.9, x + 0.7, x + 1.7))
        self.play(Create(dna, lag_ratio=0.3), run_time=0.9)
        self.play(dna[1].animate.shift(DOWN * 0.12), dna[2].animate.shift(UP * 0.12), dna[3].animate.shift(RIGHT * 0.12 + DOWN * 0.1), run_time=0.8)
        ends = VGroup(*[Dot(p, radius=0.11, color=WHITE) for p in (
            dna[0].get_end(), dna[1].get_start() + DOWN * 0.12 + RIGHT * 0.05, dna[1].get_end() + DOWN * 0.12,
            dna[2].get_start() + UP * 0.12, dna[2].get_end() + UP * 0.12, dna[3].get_start() + DOWN * 0.1 + RIGHT * 0.12)])
        for e in ends:
            e._t = 0.0

            def up(m, dt):
                m._t += dt
                m.set_opacity(0.6 + 0.4 * math.sin(4 * m._t))
            e.add_updater(up)
        self.play(FadeIn(ends, scale=2.0), run_time=0.5)
        ic1 = apop([x - 1.0, -1.0], 0.62)
        ic2 = torn([x + 1.0, -1.0], 0.62, g=-0.6, L=0.4, nuc=False)
        gl1 = VGroup(Dot(ic1[0].get_center() + 0.1 * UP, radius=0.1, color=WHITE), Dot(ic2.ring.get_center(), radius=0.1, color=WHITE))
        self.play(FadeIn(ic1), FadeIn(ic2), run_time=0.5)
        self.play(FadeIn(gl1, scale=2.0), run_time=0.5)
        self.at("free dna ends")
        t1 = T("TUNEL", 36, WHITE, weight=BOLD).move_to([x, 2.25, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.1), run_time=0.6)
        # card 2: caspase-3 switched on, but is it the killer?
        at_t(self, 6.9)
        x = xs[1]
        sc = scissors(1.8).move_to([x - 0.9, 0.7, 0])
        sc.set_opacity(0.0)
        self.add(sc)
        self.play(sc.animate.set_opacity(1.0), run_time=0.4)
        for _ in range(2):
            self.play(sc[0].animate.rotate(0.35), sc[1].animate.rotate(-0.35), run_time=0.25)
            self.play(sc[0].animate.rotate(-0.35), sc[1].animate.rotate(0.35), run_time=0.25)
        rc = intact([x + 0.8, -1.0], 0.75)
        rc.nuc.set_opacity(0)
        q = T("?", 64, WHITE, weight=BOLD).move_to([x + 0.8, -0.95, 0])
        self.play(FadeIn(rc), run_time=0.5)
        self.play(FadeIn(q, scale=1.6), run_time=0.5)
        self.at("cleaved caspase")
        t2 = T("cleaved\ncaspase-3", 32, WHITE, weight=BOLD, line_spacing=0.8).move_to([x, 2.15, 0])
        self.play(FadeIn(t2, shift=DOWN * 0.1), run_time=0.6)
        # card 3: LDH leaks out of a torn membrane
        at_t(self, 11.7)
        x = xs[2]
        ring = Arc(radius=0.95, start_angle=0.35, angle=TAU - 0.7, color=BLUE, stroke_width=8).move_arc_center_to([x - 0.8, 0.5, 0])
        dots = VGroup(*[Dot([x - 1.2 + 0.4 * (i % 3), 0.25 + 0.35 * (i // 3), 0], radius=0.09, color=RED) for i in range(5)])
        beaker = VGroup(Line([x + 0.8, -0.8, 0], [x + 0.8, -2.0, 0]), Line([x + 0.8, -2.0, 0], [x + 1.8, -2.0, 0]),
                        Line([x + 1.8, -2.0, 0], [x + 1.8, -0.8, 0])).set_stroke(WHITE, 5)
        self.play(FadeIn(ring), FadeIn(dots), FadeIn(beaker), run_time=0.8)
        for i, d in enumerate(dots):
            bob(d, 0.08, 1.0 + 0.2 * i, i, axis=np.array([math.cos(2 * i), math.sin(2 * i), 0]))
        ml = T("medium", 26, WHITE).move_to([x + 1.3, -2.4, 0])
        self.play(FadeIn(ml), run_time=0.4)
        self.at("ldh")
        ldh = T("LDH", 30, RED, weight=BOLD).move_to([x - 0.8, 1.9, 0])
        self.play(FadeIn(ldh), run_time=0.5)
        self.at("leaks through")
        paths = []
        for i, d in enumerate(dots):
            tgt = np.array([x + 1.0 + 0.3 * (i % 3), -1.7 + 0.3 * (i // 3) + 0.2, 0])
            paths.append(d.animate(path_arc=-0.8).move_to(tgt))
        self.play(AnimationGroup(*paths, lag_ratio=0.2), run_time=2.2)
        self.finish()


def macro_world(state="start", r=2.0, c=(-1.9, 0.45)):
    """Mouse macrophage with RED LDH dots, beaker 'medium'. state selects what is carried."""
    c = np.array([c[0], c[1], 0.0])
    outline = Circle(radius=r + 0.28, color=GREEN, stroke_width=7, fill_color=GREEN, fill_opacity=0.10).move_to(c)
    ring = Circle(radius=r, color=BLUE, stroke_width=9, fill_color=BLUE, fill_opacity=0.14).move_to(c)
    pulse_stroke(ring)
    cell = VGroup(outline, ring)
    cell.outline, cell.ring = outline, ring
    dots = VGroup()
    for i in range(8):
        d = Dot(radius=0.1, color=RED)
        d.ph = i * 0.9
        d.base = np.array([math.cos(i * 0.8 + 0.3), math.sin(i * 0.8 + 0.3), 0]) * (0.45 + 0.17 * (i % 4))
        d.ring = ring

        def up(m, dt):
            m.ph += dt
            cc = m.ring.get_center()
            rr = m.ring.width / 2
            s = rr / r
            m.move_to(cc + s * (m.base + 0.18 * np.array([math.sin(0.9 * m.ph + 1), math.cos(0.7 * m.ph), 0])))
        d.add_updater(up)
        dots.add(d)
    cell.add(dots)
    cell.dots = dots
    bx = 4.7
    beaker = VGroup(Line([bx - 0.9, 1.4, 0], [bx - 0.9, -1.3, 0]), Line([bx - 0.9, -1.3, 0], [bx + 0.9, -1.3, 0]),
                    Line([bx + 0.9, -1.3, 0], [bx + 0.9, 1.4, 0])).set_stroke(WHITE, 6)
    bl = T("medium", 28, WHITE).move_to([bx, -1.85, 0])
    return cell, beaker, bl


class S11Ask(SpokenScene):
    def construct(self):
        # card 3 grows into the main picture
        xs = (-4.55, 0.0, 4.55)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4.2, height=5.7, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.08).move_to([x, 0, 0]) for x in xs])
        cell, beaker, bl = macro_world()
        ringx = Arc(radius=0.95, start_angle=0.35, angle=TAU - 0.7, color=BLUE, stroke_width=8).move_arc_center_to([xs[2] - 0.8, 0.5, 0])
        self.add(cards[2], ringx)
        self.play(FadeOut(cards[2]), FadeOut(ringx), FadeIn(cell, scale=0.5), FadeIn(beaker), FadeIn(bl), run_time=1.6)
        ml = T("mouse macrophage", 26, GREEN).move_to([-1.9, -2.75, 0])
        self.play(FadeIn(ml), run_time=0.5)
        self.at("removed")
        # NINJ1 block sits in the BLUE ring, lifted out
        a = math.radians(125)
        pos = np.array([-1.9, 0.45, 0]) + 2.0 * np.array([math.cos(a), math.sin(a), 0])
        nb = block(0.55, 0.3, GREY, fill=0.7).rotate(a - PI / 2).move_to(pos)
        self.play(FadeIn(nb, scale=0.5), run_time=0.5)
        aside = np.array([-5.6, 2.2, 0])
        self.play(nb.animate.move_to(aside).rotate(-(a - PI / 2)).scale(1.7), run_time=1.4)
        cross = VGroup(Line(aside + 0.45 * UL, aside + 0.45 * DR), Line(aside + 0.45 * UR, aside + 0.45 * DL)).set_stroke(WHITE, 7)
        self.play(Create(cross), run_time=0.4)
        nl = T("NINJ1", 28, WHITE, weight=BOLD).next_to(nb, DOWN, buff=0.25)
        self.play(FadeIn(nl), run_time=0.5)
        self.at("then they triggered")
        c = np.array([-1.9, 0.45, 0])
        bolt = Polygon(c + [-0.3, 3.4, 0], c + [0.4, 2.7, 0], c + [0.05, 2.7, 0], c + [0.55, 1.6, 0], c + [-0.1, 2.1, 0], c + [0.15, 2.1, 0],
                       stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.9)
        self.play(FadeIn(bolt, shift=DOWN * 0.4), run_time=0.35)
        mac_block = block(1.2, 0.5, GREY, fill=0.8).move_to(c + np.array([0.0, -1.2, 0]))
        dark = Circle(radius=1.95, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to(c)
        self.play(FadeOut(bolt), FadeIn(dark), FadeIn(mac_block), run_time=1.0)
        self.play(mac_block[0].animate.set_fill(WHITE, 0.6).set_stroke(WHITE), run_time=0.6)
        self.at("will ldh pour out")
        q = card("Will LDH pour out?", 42).move_to([0, 3.35, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
        glow = beaker.copy().set_stroke(WHITE, 12).set_opacity(0.3)
        glow._t = 0.0

        def up(m, dt):
            m._t += dt
            m.set_opacity(0.2 + 0.2 * math.sin(3 * m._t))
        glow.add_updater(up)
        self.add(glow)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        cell, beaker, bl = macro_world()
        c = np.array([-1.9, 0.45, 0])
        dark = Circle(radius=1.95, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to(c)
        mac_block = block(1.2, 0.5, GREY, fill=0.8).move_to(c + np.array([0.0, -1.2, 0]))
        mac_block[0].set_fill(WHITE, 0.6).set_stroke(WHITE)
        ml = T("mouse macrophage", 26, GREEN).move_to([-1.9, -2.75, 0])
        q = card("Will LDH pour out?", 42).move_to([0, 3.35, 0])
        self.add(cell, dark, mac_block, beaker, bl, ml, q)
        self.play(cell.ring.animate.scale(1.03), run_time=2.25, rate_func=there_and_back)
        self.play(cell.ring.animate.scale(1.03), run_time=2.25, rate_func=there_and_back)


class S13Answer(SpokenScene):
    def construct(self):
        cell, beaker, bl = macro_world()
        c = np.array([-1.9, 0.45, 0])
        dark = Circle(radius=1.95, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to(c)
        mac_block = block(1.2, 0.5, GREY, fill=0.8).move_to(c + np.array([0.0, -1.2, 0]))
        mac_block[0].set_fill(WHITE, 0.6).set_stroke(WHITE)
        ml = T("mouse macrophage", 26, GREEN).move_to([-1.9, -2.75, 0])
        q = card("Will LDH pour out?", 42).move_to([0, 3.35, 0])
        self.add(cell, dark, mac_block, beaker, bl, ml, q)
        self.play(FadeOut(q), FadeOut(ml), run_time=0.5)
        # a tiny trickle: two dots reach the beaker
        self.add(dark)
        two = VGroup(*[Dot(c + np.array([1.2, 0.3 * i, 0]), radius=0.1, color=RED) for i in range(2)])
        ll = T("little LDH", 30, RED, weight=BOLD).move_to([4.7, 1.95, 0])
        self.play(FadeIn(two), run_time=0.3)
        self.play(*[d.animate(path_arc=-0.5).move_to([4.5 + 0.35 * i, -1.0, 0]) for i, d in enumerate(two)], FadeIn(ll), run_time=1.6)
        self.at("stayed swollen")
        self.play(scale_about(VGroup(cell, dark, mac_block), 1.2, c), run_time=1.0)
        self.play(VGroup(cell, dark, mac_block).animate.shift(DOWN * 0.45), run_time=0.5)
        dl = T("dead, still sealed", 36, WHITE, weight=BOLD).move_to([-1.9, 3.4, 0])
        self.at("like balloons")
        self.play(FadeIn(dl, shift=DOWN * 0.1), cell.ring.animate.set_stroke(BLUE, 12), run_time=0.8)
        self.play(cell.ring.animate.scale(1.02), run_time=0.8, rate_func=there_and_back)
        self.at("separate steps")
        b1 = VGroup(RoundedRectangle(corner_radius=0.12, width=3.3, height=0.7, stroke_color=WHITE, stroke_width=3),
                    T("1  death", 28, WHITE)).arrange(ORIGIN) if False else None
        s1 = chip("1  death  ✓", WHITE, 28).move_to([-3.6, -3.15, 0])
        s2 = chip("2  final tear", WHITE, 28).move_to([0.6, -3.15, 0])
        s2[0].set_fill(BG, 0.9)
        arr = Arrow(s1.get_right(), s2.get_left(), color=WHITE, buff=0.12, stroke_width=5)
        nin = block(1.3, 0.5, GREY, "NINJ1", 24, fill=0.15).move_to([3.1, -3.15, 0]).set_opacity(0.55)
        self.play(FadeIn(s1, shift=UP * 0.2), run_time=0.6)
        self.play(GrowArrow(arr), FadeIn(s2, shift=UP * 0.2), FadeIn(nin), run_time=0.9)
        self.at("ldh measures the tear")
        ra = Arrow([4.7, -1.4, 0], s2.get_top() + RIGHT * 0.5 + UP * 0.1, color=RED, buff=0.05, stroke_width=7)
        self.play(GrowArrow(ra), run_time=1.0)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        # rebuild the end of the previous scene, then zoom back to the torn cell
        c = np.array([-1.9, 0.45, 0])
        cell, beaker, bl = macro_world()
        dark = Circle(radius=1.95, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to(c)
        mb = block(1.2, 0.5, GREY, fill=0.8).move_to(c + np.array([0.0, -1.2, 0]))
        mb[0].set_fill(WHITE, 0.6).set_stroke(WHITE)
        cg = VGroup(cell, dark, mb)
        cg.scale(1.2, about_point=c).shift(DOWN * 0.45)
        dl = T("dead, still sealed", 36, WHITE, weight=BOLD).move_to([-1.9, 3.4, 0])
        ll = T("little LDH", 30, RED, weight=BOLD).move_to([4.7, 1.95, 0])
        two = VGroup(*[Dot([4.5 + 0.35 * i, -1.0, 0], radius=0.1, color=RED) for i in range(2)])
        s1 = chip("1  death  \u2713", WHITE, 28).move_to([-3.6, -3.15, 0])
        s2 = chip("2  final tear", WHITE, 28).move_to([0.6, -3.15, 0])
        old = VGroup(cg, beaker, bl, dl, ll, two, s1, s2)
        self.add(old)
        big = torn([0, -0.3], 2.3, g=-0.6, L=1.9)
        big.shift(RIGHT * 0)
        self.play(FadeOut(old), FadeIn(big, scale=0.8), run_time=1.4)
        q = card("What killed it?", 44).move_to([0, 3.3, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
        self.at("its look")
        t1 = T("RIPK3 + MLKL", 30, WHITE, weight=BOLD).move_to([-4.8, 1.2, 0])
        t2 = T("gasdermin", 30, WHITE, weight=BOLD).move_to([4.8, 1.2, 0])
        t3 = T("iron-dependent lipid damage", 30, WHITE, weight=BOLD).move_to([0, -3.4, 0])
        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.3)
        self.at("how it ended")
        self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(t3, shift=UP * 0.2), run_time=0.6)
        self.at("block each candidate")
        bar = RoundedRectangle(corner_radius=0.05, width=t1.width + 0.3, height=0.07, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(t1.get_center() + LEFT * 3)
        self.play(bar.animate.move_to(t1.get_center()), t1.animate.set_opacity(0.55), run_time=1.0)
        self.at("watch what changes")
        circ = Circle(radius=2.3, color=BLUE, stroke_width=9).move_to([0, -0.3, 0])
        self.play(Transform(big.ring, circ), big.k.animate.set_value(0), big.body.animate.set_fill(BLUE, 0.17), run_time=1.6)
        q2 = card("Test it.", 44).move_to([0, 3.3, 0])
        self.play(ReplacementTransform(q, q2), run_time=0.7)
        self.finish()


class S15End(EndCard):
    LINE = "A death's look names an endpoint, not a cause."
