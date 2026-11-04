"""Synapse elimination, chapter 2: A Contest at Every Junction  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, same as chapter 1 and the old single film)
  BLUE   = motor axon A (and, in the first half, the one motor neuron we follow), its branches and terminals
  ORANGE = motor axon B and its terminals
  TEAL   = acetylcholine receptor sites on the muscle
  VIOLET = receptors bound by the fluorescent snake toxin (the label)
  YELLOW = activity (impulses), questions
  RED    = retreating, lost, removed
  GREEN  = kept / preserved / yes
  GREY   = muscle fiber, outlines, de-emphasised
  TEXT   = timers, labels, tracer
  GOLD   = credit cards (who did the experiment)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
VIOLET = "#C58BF2"


def bchip(text, color, size=28):
    """chip with tight padding, for the strip along the bottom of the frame"""
    return chip(text, color, size=size, pad=0.15)

# ----------------------------------------------------------------------------------------------
# the arbor: one motor neuron whose branches reach six muscle fibers
# ----------------------------------------------------------------------------------------------
OBIG = (-5.4, 0.0)
SOMA_R = 0.65
SXB, SYB = 7.5 / 3.2, 1.0 / 0.3          # unit glyph (width 3.2, tips at +-0.75) -> big arbor (tips at +-2.5)
TIPY = [0.75, 0.45, 0.15, -0.15, -0.45, -0.75]
FY = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]   # fiber rows = tip rows in the big arbor


def ar_geom(origin, sx, sy):
    o = np.array([origin[0], origin[1], 0.0])

    def P(u):
        return o + np.array([u[0] * sx, u[1] * sy, 0.0])
    nodes = [P((1.4, 0.45))] * 3 + [P((1.4, -0.45))] * 3
    ends = [P((3.2, y)) for y in TIPY]
    return o, P((0.7, 0)), P((1.4, 0.45)), P((1.4, -0.45)), nodes, ends


def arbor_mobs(origin, sx, sy, color, ws, soma_r=None):
    o, n1, mu, md, nodes, ends = ar_geom(origin, sx, sy)
    trunk = Line(o, n1, color=color, stroke_width=ws[0])
    lu = Line(n1, mu, color=color, stroke_width=ws[1])
    ld = Line(n1, md, color=color, stroke_width=ws[1])
    tips = [Line(nodes[i], ends[i], color=color, stroke_width=ws[2]) for i in range(6)]
    if soma_r:
        soma = Circle(radius=soma_r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.9).move_to(o)
    else:
        soma = Dot(radius=0.1, color=color).move_to(o)
    soma.set_z_index(2)
    g = VGroup(trunk, lu, ld, *tips, soma)
    return dict(g=g, trunk=trunk, lu=lu, ld=ld, tips=tips, soma=soma, nodes=nodes, ends=ends)


def make_halo(a, op=0.35, extra=16, tip_extra=12):
    """glow behind one axon: 9 line halos (trunk, lu, ld, six tips) + the soma ring"""
    parts = []
    for j, ln in enumerate([a["trunk"], a["lu"], a["ld"], *a["tips"]]):
        parts.append(ln.copy().set_stroke(BLUE, width=ln.get_stroke_width() + (extra if j < 3 else tip_extra), opacity=op))
    s = a["soma"]
    parts.append(Circle(radius=s.width / 2 + 0.03, stroke_color=BLUE, stroke_width=22, stroke_opacity=op,
                        fill_opacity=0).move_to(s.get_center()))
    return VGroup(*parts)


class ArborView:
    """The big arbor with fibers, boutons and labels. retr = {tip index: (fraction left, color)}."""

    def __init__(self, retr=None, boutons=True, color=BLUE, halo=False):
        retr = retr or {}
        a = arbor_mobs(OBIG, SXB, SYB, color, (11, 8, 6), soma_r=SOMA_R)
        self.a = a
        self.tips, self.nodes, self.ends = a["tips"], a["nodes"], a["ends"]
        self.fibers = [RoundedRectangle(corner_radius=0.2, width=5.0, height=0.62, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.2).move_to([3.7, y, 0]) for y in FY]
        self.flabel = T("muscle fibers", 24, GREY).move_to([5.0, FY[5], 0])
        self.slabel = T("motor neuron", 26, color).move_to([OBIG[0], -1.3, 0])
        self.bout = []
        for i in range(6):
            b = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.46, stroke_color=color, stroke_width=3,
                                 fill_color=color, fill_opacity=0.6).move_to(self.ends[i] + np.array([0.05, 0, 0]))
            self.bout.append(b)
        self.hal = make_halo(a, 0.35, 16, 12) if halo else None
        for i, (frac, col) in retr.items():
            nend = self.nodes[i] + (self.ends[i] - self.nodes[i]) * max(frac, 0.002)
            self.tips[i].become(Line(self.nodes[i], nend, color=col, stroke_width=6))
            if frac > 0:
                self.bout[i].move_to(nend + np.array([0.05, 0, 0])).set_color(col)
                if self.hal is not None:
                    self.hal[3 + i].become(Line(self.nodes[i], nend).set_stroke(BLUE, width=18, opacity=0.35))
            else:
                self.tips[i].set_opacity(0)
                self.bout[i].set_opacity(0)
                if self.hal is not None:
                    self.hal[3 + i].set_opacity(0)
        self.boutons = boutons

    def parts(self):
        out = []
        if self.hal is not None:
            out += list(self.hal)
        out += [*self.fibers, self.flabel, *self.a["g"], self.slabel]
        if self.boutons:
            out += self.bout
        return out

    def add_to(self, scene):
        scene.add(*self.parts())
        return self


def retract(v, i, frac=0.0, color=None):
    """Animations that pull tip i back to `frac` of its length (0 = gone back to the branch point).
    The bouton leaves with the branch (it fades while it travels back), so nothing is left in the gap."""
    node, end = v.nodes[i], v.ends[i]
    tip = v.tips[i]
    nend = node + (end - node) * max(frac, 0.002)
    stub = Line(node, nend, color=color or tip.get_color(), stroke_width=6)
    anims = [Transform(tip, stub)]
    b = v.bout[i]
    if frac <= 0:
        anims.append(b.animate.move_to(node).set_opacity(0))
    else:
        anims.append(b.animate.move_to(nend + np.array([0.05, 0, 0])).set_color(color or tip.get_color()))
    if v.hal is not None:
        hs = Line(node, nend).set_stroke(BLUE, width=18, opacity=0.0 if frac <= 0 else 0.35)
        anims.append(Transform(v.hal[3 + i], hs))
    return anims


def restore(v, i, color=BLUE):
    end = v.ends[i]
    full = Line(v.nodes[i], end, color=color, stroke_width=6)
    anims = [Transform(v.tips[i], full), v.bout[i].animate.move_to(end + np.array([0.05, 0, 0])).set_color(color)]
    if v.hal is not None:
        anims.append(Transform(v.hal[3 + i], Line(v.nodes[i], end).set_stroke(BLUE, width=18, opacity=0.35)))
    return anims


def lost_marks():
    """six small red arrows (one per junction) and the 'branches lost ?' label"""
    arrows = [Arrow([2.95, y, 0], [2.45, y, 0], buff=0, color=RED, stroke_width=6, max_tip_length_to_length_ratio=0.5)
              for y in FY]
    lab = VGroup(T("branches lost", 28, RED), T("?", 44, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.25)
    lab.move_to([4.3, 3.3, 0])
    return arrows, lab


def badge(y, d):
    return T(f"day {d}", 28, RED, weight=BOLD).move_to([4.6, y, 0])


def clock(x, y, ang, r=0.26):
    c = Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    h = Line([x, y, 0], [x + 0.78 * r * np.cos(ang), y + 0.78 * r * np.sin(ang), 0], color=TEXT, stroke_width=4)
    return VGroup(c, h)


def spin(c, w):
    ctr = c[0].get_center()
    c[1].add_updater(lambda m, dt: m.rotate(-w * dt, about_point=ctr))


LOST = {4: 2, 1: 4, 3: 6, 0: 8}                 # tip -> day it retreated (chapter schematic)
CLOCK_ANG = [0.3, 2.0, 3.9, 5.2, 1.1, 4.4]
CLOCK_W = [0.7, 1.25, 0.45, 1.6, 0.95, 0.55]    # different speeds: separate clocks


def counter_text(d, pos=(0, 3.25)):
    return M(f"day {d}", 32, TEXT).move_to([pos[0], pos[1], 0])


def counter(tr, pos=(0, 3.25)):
    t = counter_text(int(round(tr.get_value())), pos)
    st = {"d": int(round(tr.get_value()))}

    def upd(m):
        d = int(round(tr.get_value()))
        if d != st["d"]:
            st["d"] = d
            m.become(counter_text(d, pos))
    t.add_updater(upd)
    return t


def s05_state(scene):
    v = ArborView({i: (0, BLUE) for i in LOST}, halo=True).add_to(scene)
    bs = [badge(FY[i], d) for i, d in LOST.items()]
    ct = counter_text(10)
    scene.add(*bs, ct)
    return v, bs, ct


def stays_badges():
    return [T("stays", 28, BLUE, weight=BOLD).move_to([4.6, FY[i], 0])
            for i in range(6) if i not in LOST]


def s06_state(scene, spinning=False):
    v, bs, ct = s05_state(scene)
    ct.set_opacity(0)
    v.flabel.move_to([4.6, -2.99, 0])
    bs += stays_badges()
    scene.add(*bs)
    cl = [clock(3.25, FY[i], CLOCK_ANG[i], r=0.28) for i in range(6)]
    cap = T("a separate contest at every junction", 28, TEXT).move_to([0, -3.4, 0])
    scene.add(*cl, cap)
    if spinning:
        for k, c in enumerate(cl):
            spin(c, CLOCK_W[k])
    return v, bs, ct, cl, cap


# ----------------------------------------------------------------------------------------------
# a muscle with nine motor axons coming in from the spinal cord (the credit scene)
# ----------------------------------------------------------------------------------------------
NAX = 8
AXY = [2.15 - k * 0.66 for k in range(NAX)]
AX_X0, AX_X1 = -6.0, 5.6
GSX = (AX_X1 - AX_X0) / 3.2
GSY = 0.26 / 0.75
LIT = (2, 5)                                   # two of eight glow; axon 2 is the one we follow
MUS_C, MUS_W = 2.45, 8.1                       # muscle box x centre and width


def glyph(k, lit):
    m = arbor_mobs((AX_X0, AXY[k]), GSX, GSY, BLUE if lit else GREY, (3.5, 3.0, 2.6), soma_r=0.17)
    g = m["g"]
    if not lit:
        g.set_opacity(0.6)
    halo = make_halo(m, op=0.4 if lit else 0.0, extra=12, tip_extra=3) if k in LIT else None
    return g, halo


def credit(l1, l2=None, y=3.2):
    t1 = T(l1, 26, TEXT)
    parts = [t1]
    if l2:
        parts.append(T(l2, 24, GREY))
    g = VGroup(*parts).arrange(DOWN, buff=0.1)
    box = RoundedRectangle(corner_radius=0.15, width=g.width + 0.5, height=g.height + 0.3, stroke_color=GOLD,
                           stroke_width=3, fill_color=BG, fill_opacity=0.95).move_to(g)
    return VGroup(box, g).move_to([0, y, 0])


def wl_card(y=2.75):
    return credit("Walsh and Lichtman, 2003", "two-color imaging of one living junction", y=y)


def s03_mobs(lit=LIT, card=True):
    rect = RoundedRectangle(corner_radius=0.3, width=MUS_W, height=5.5, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([MUS_C, -0.15, 0])
    cord = RoundedRectangle(corner_radius=0.2, width=1.05, height=5.5, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([AX_X0, -0.15, 0])
    lab = T("muscle", 26, GREY).move_to([MUS_C, -3.3, 0])
    clab = T("spinal cord", 24, GREY).move_to([-5.7, -3.3, 0])
    gl = [glyph(k, k in lit) for k in range(NAX)]
    cd = credit("Keller-Peck, Lichtman and colleagues, 2001", "transgenic mice")
    return rect, cord, lab, clab, gl, cd


def s03_state(scene, lit=LIT, card=True):
    rect, cord, lab, clab, gl, cd = s03_mobs(lit, card)
    scene.add(rect, cord, lab, clab)
    for g, h in gl:
        if h is not None:
            scene.add(h)
        scene.add(g)
    if card:
        scene.add(cd)
    return rect, cord, lab, clab, gl, cd


# ----------------------------------------------------------------------------------------------
# the junction stage (one muscle fiber, eight receptor sites, two axons)
# ----------------------------------------------------------------------------------------------
N, SP = 8, 1.45
XS = [(i - 3.5) * SP for i in range(N)]
YT, RY, YTOP = 1.0, -0.35, 2.9
BOUND = (0, 2, 5, 6)


def bead(x, y, color, w=SP * 0.84, op=0.55):
    return RoundedRectangle(corner_radius=0.14, width=w, height=1.2, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def stage(kA=5, colored=True, bound=()):
    d = {}
    d["muscle"] = RoundedRectangle(corner_radius=0.2, width=N * SP + 0.6, height=2.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.22).move_to([0, -0.95, 0])
    d["mlabel"] = T("muscle fiber", 24, GREY).move_to([0, -1.78, 0])
    d["rlabel"] = T("acetylcholine receptor sites", 24, TEAL).move_to([0, -1.2, 0])
    d["tlabel"] = T("axon terminals", 26, GREY).move_to([0, 2.15, 0])
    d["rec"] = [RoundedRectangle(corner_radius=0.08, width=SP * 0.78, height=0.8,
                                 stroke_color=VIOLET if i in bound else TEAL, stroke_width=3,
                                 fill_color=VIOLET if i in bound else TEAL,
                                 fill_opacity=0.85 if i in bound else 0.55).move_to([x, RY, 0]) for i, x in enumerate(XS)]
    cA, cB = (BLUE, ORANGE) if colored else (TEXT, TEXT)
    d["shA"] = Line([XS[0], YTOP, 0], [XS[0], YT, 0], color=cA, stroke_width=10)
    d["shB"] = Line([XS[-1], YTOP, 0], [XS[-1], YT, 0], color=cB, stroke_width=10)
    d["lineA"] = Line([XS[0], YT, 0], [XS[kA - 1], YT, 0], color=cA, stroke_width=10) if kA > 1 else VGroup()
    d["lineB"] = Line([XS[-1], YT, 0], [XS[kA], YT, 0], color=cB, stroke_width=10) if N - kA > 1 else VGroup()
    d["bead"] = [bead(XS[i], YT, (cA if i < kA else cB), op=0.55 if colored else 0.3) for i in range(N)]
    d["la"] = T("axon A", 28, BLUE).move_to([XS[0], 3.4, 0])
    d["lb"] = T("axon B", 28, ORANGE).move_to([XS[-1], 3.4, 0])
    return d


def base_group(d):
    return [d["muscle"], d["mlabel"], d["rlabel"], *d["rec"]]


def axon_group(d):
    return [d["lineA"], d["lineB"], d["shA"], d["shB"], *d["bead"]]


def tall_stage():
    """The same muscle fiber and receptors, drawn tall to fill the frame (credit scene). Same order as base_group."""
    muscle = RoundedRectangle(corner_radius=0.25, width=N * SP + 0.6, height=4.6, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.22).move_to([0, -1.35, 0])
    ml = T("muscle fiber", 24, GREY).move_to([0, -3.35, 0])
    rl = T("acetylcholine receptor sites", 26, TEAL).move_to([0, -2.85, 0])
    rec = [RoundedRectangle(corner_radius=0.1, width=SP * 0.78, height=2.8, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.55).move_to([x, -1.0, 0]) for x in XS]
    return [muscle, ml, rl, *rec]


def legend_purple():
    sw = Square(0.28, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET, fill_opacity=0.85)
    tx = T("purple = labelled receptors", 24, TEXT)
    return VGroup(sw, tx).arrange(RIGHT, buff=0.2).move_to([0, 2.65, 0])


def legend_ab(y=-3.0, x=0.0):
    a = VGroup(Square(0.28, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.8), T("axon A", 26, BLUE)).arrange(RIGHT, buff=0.15)
    b = VGroup(Square(0.28, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.8), T("axon B", 26, ORANGE)).arrange(RIGHT, buff=0.15)
    return VGroup(a, b).arrange(RIGHT, buff=0.8).move_to([x, y, 0])


def pdot(x, y):
    return Dot(radius=0.14, color=YELLOW).move_to([x, y, 0])


def bracket(x0, x1, y, color):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=6),
                  Line([x0, y, 0], [x0, y + 0.22, 0], color=color, stroke_width=6),
                  Line([x1, y, 0], [x1, y + 0.22, 0], color=color, stroke_width=6))


def cellbar(cx, cy, kA, cell=0.5, h=0.6):
    cells = []
    for i in range(N):
        c = BLUE if i < kA else ORANGE
        cells.append(Rectangle(width=cell, height=h, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.8)
                     .move_to([cx + (i - 3.5) * cell, cy, 0]))
    return VGroup(*cells)


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Synapse Elimination: One Muscle Fiber, One Axon"
    TITLE = "A Contest at Every Junction"


class S01Q(SpokenScene):
    def construct(self):
        v = ArborView(boutons=False)
        # draw the muscle fibers and the (large) cell body first
        self.play(*[FadeIn(f) for f in v.fibers], FadeIn(v.flabel), GrowFromCenter(v.a["soma"]), FadeIn(v.slabel),
                  run_time=0.6)
        self.at("loses many branches")
        self.play(Create(v.a["trunk"]), Create(v.a["lu"]), Create(v.a["ld"]), run_time=0.5)
        self.at("many branches")
        self.play(LaggedStart(*[Create(t) for t in v.tips], lag_ratio=0.2), run_time=1.0)
        self.play(*[FadeIn(b, scale=0.5) for b in v.bout], run_time=0.5)
        self.at("Does it pull them all back")
        arrows, lab = lost_marks()
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), FadeIn(lab, shift=DOWN * 0.15),
                  run_time=0.9)
        self.at("on one schedule")
        q = bchip("one schedule?", TEXT, size=30).move_to([0, -3.4, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S02Program(SpokenScene):
    def construct(self):
        v = ArborView().add_to(self)
        arrows, lab = lost_marks()
        self.add(*arrows, lab)
        self.at("one program")
        chp = bchip("one program for the whole arbor?", TEXT, size=28).move_to([0, -3.4, 0])
        self.play(FadeIn(chp, shift=UP * 0.2), run_time=0.5)
        self.at("whole arbor")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=13.3, height=5.9, stroke_color=TEXT,
                                              stroke_width=4).move_to([0, 0, 0]), num_dashes=70)
        self.play(Create(box), run_time=0.9)
        self.at("would retreat")
        allat = VGroup(T("all at once", 30, RED, weight=BOLD)).move_to([4.3, 3.3, 0])
        anims = []
        for i in range(6):
            anims += retract(v, i, 0.0)
        self.play(ReplacementTransform(lab, allat), run_time=0.3)
        self.play(*anims, run_time=2.5)
        self.wait(1.0)                                   # hold the empty arbor
        self.finish()


class S03Kp(SpokenScene):
    def construct(self):
        rect, cord, lab, clab, gl, cd = s03_mobs(lit=())
        allm = [rect, cord, lab, clab]
        for g, h in gl:
            if h is not None:
                allm.append(h)
            allm.append(g)
        self.play(*[FadeIn(m) for m in allm], run_time=0.7)
        self.at("keller peck")
        self.play(FadeIn(cd, shift=DOWN * 0.15), run_time=0.7)
        self.at("small random subset")
        anims = []
        for k in LIT:
            g0, h = gl[k]
            anims.append(g0.animate.set_color(BLUE).set_opacity(1.0))
            anims.append(h.animate.set_stroke(opacity=0.4))
        self.play(*anims, run_time=0.9)
        self.at("axons glow")
        hs = [gl[k][1] for k in LIT]
        self.play(*[h.animate.set_stroke(opacity=0.7) for h in hs], run_time=0.4)
        self.play(*[h.animate.set_stroke(opacity=0.4) for h in hs], run_time=0.5)
        self.finish()


class S04Trace(SpokenScene):
    def construct(self):
        rect, cord, lab, clab, gl, cd = s03_state(self)
        FOL = LIT[0]
        lit_g, lit_h = gl[FOL]
        v = ArborView(halo=True)
        others = [rect, cord, lab, clab, cd] + [gl[k][0] for k in range(NAX) if k != FOL] \
                 + [gl[k][1] for k in LIT if k != FOL]
        one = bchip("one glowing axon, followed", BLUE, size=28).move_to([0, -3.4, 0])
        self.play(*[FadeOut(o) for o in others], ReplacementTransform(lit_g, v.a["g"]),
                  ReplacementTransform(lit_h, v.hal),
                  *[FadeIn(f) for f in v.fibers], FadeIn(v.flabel), FadeIn(v.slabel),
                  *[FadeIn(b, scale=0.5) for b in v.bout], FadeIn(one, shift=UP * 0.2), run_time=0.9)
        self.at("every branch")
        big = v.a
        flashes = [ShowPassingFlash(m.copy().set_color(TEXT).set_stroke(width=13), time_width=0.7)
                   for m in [big["trunk"], big["lu"], big["ld"], *big["tips"]]]
        self.play(LaggedStart(*flashes, lag_ratio=0.18), run_time=1.9)
        self.at("Each axon was losing branches")
        anims = []
        for i in (1, 3, 4):
            anims += retract(v, i, 0.55, RED)
        chp = bchip("losing branches", RED, size=28).move_to([0, -3.4, 0])
        self.play(*anims, ReplacementTransform(one, chp), run_time=1.1)
        self.finish()


class S05Times(SpokenScene):
    def construct(self):
        v = ArborView({1: (0.55, RED), 3: (0.55, RED), 4: (0.55, RED)}, halo=True).add_to(self)
        chp = bchip("losing branches", RED, size=28).move_to([0, -3.4, 0])
        self.add(chp)
        dv = ValueTracker(0)
        ct = counter(dv)
        self.at("Its branches withdrew")
        # rewind to the start of the record
        rest = []
        for i in (1, 3, 4):
            rest += restore(v, i)
        self.play(*rest, FadeOut(chp), FadeIn(ct), run_time=0.7)
        self.play(dv.animate.set_value(2), run_time=0.5, rate_func=linear)
        bs = []

        def event(tip, d, nxt, rt=0.7):
            b = badge(FY[tip], d)
            bs.append(b)
            self.play(*retract(v, tip, 0.0), FadeIn(b, scale=0.6), dv.animate.set_value(nxt), run_time=rt, rate_func=linear)

        self.at("different times")
        event(4, 2, 3.4)
        self.play(dv.animate.set_value(4), run_time=0.35, rate_func=linear)
        self.at("different junctions")
        event(1, 4, 5.4)
        self.play(dv.animate.set_value(6), run_time=0.45, rate_func=linear)
        self.at("without an obvious")
        event(3, 6, 7.4)
        self.play(dv.animate.set_value(8), run_time=0.2, rate_func=linear)
        self.at("spatial pattern")
        event(0, 8, 9.2)
        self.play(dv.animate.set_value(10), run_time=0.4, rate_func=linear)
        self.finish()


class S06Local(SpokenScene):
    def construct(self):
        v, bs, ct = s05_state(self)
        self.at("They did not go together")
        self.play(*[Indicate(b, color=RED, scale_factor=1.25) for b in bs],
                  FadeOut(ct), v.flabel.animate.move_to([4.6, -2.99, 0]),
                  *[FadeIn(b) for b in stays_badges()], run_time=0.9)
        self.at("a separate contest")
        cl = [clock(3.25, FY[i], CLOCK_ANG[i], r=0.28) for i in range(6)]
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cl], lag_ratio=0.12), run_time=0.9)
        for k, c in enumerate(cl):
            spin(c, CLOCK_W[k])
        self.at("at every junction")
        cap = T("a separate contest at every junction", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S07Beat(NarratedScene):
    def construct(self):
        s06_state(self, spinning=True)
        self.finish()


class S08Wl(SpokenScene):
    def construct(self):
        v, bs, ct, cl, cap = s06_state(self)
        tall = tall_stage()
        card = wl_card()
        self.play(*[FadeOut(m) for m in v.parts() + bs + [ct] + cl + [cap]], *[FadeIn(m) for m in tall], run_time=1.0)
        self.at("Mark Walsh")
        self.play(FadeIn(card, shift=DOWN * 0.15), run_time=0.6)
        self.at("watched one of")
        self.play(*[Indicate(r, color=TEAL, scale_factor=1.1) for r in tall[3:]], run_time=0.9)
        self.finish()


class S09Colours(SpokenScene):
    def construct(self):
        d = stage(5, colored=False)
        tall = tall_stage()
        card = wl_card()
        self.add(*tall, card)
        # carry the tall fiber from the credit scene into the working layout
        self.play(*[ReplacementTransform(a, b) for a, b in zip(tall, base_group(d))], FadeOut(card), run_time=0.5)
        self.at("motor axons")
        self.play(Create(d["shA"]), Create(d["shB"]), FadeIn(d["lineA"]), FadeIn(d["lineB"]),
                  *[FadeIn(b) for b in d["bead"]], FadeIn(d["tlabel"]), run_time=0.9)
        self.at("different colors")
        self.play(VGroup(d["shA"], d["lineA"], *d["bead"][:5]).animate.set_color(BLUE),
                  VGroup(d["shB"], d["lineB"], *d["bead"][5:]).animate.set_color(ORANGE),
                  FadeIn(d["la"]), FadeIn(d["lb"]), run_time=0.8)
        self.at("The same living junction")
        dv = ValueTracker(0)
        ct = counter(dv)
        frame = DashedVMobject(SurroundingRectangle(VGroup(d["muscle"], *d["bead"]), buff=0.12, color=TEXT,
                                                    stroke_width=4, corner_radius=0.2), num_dashes=80)
        flab = T("same junction, imaged again and again", 26, TEXT).move_to([0, -2.75, 0])
        self.play(Create(frame), FadeIn(flab, shift=UP * 0.1), FadeIn(ct), run_time=0.8)
        self.at("imaged again and again")
        for day in (0, 3, 6):
            self.play(Indicate(frame, color=WHITE, scale_factor=1.02), dv.animate.set_value(day), run_time=0.5,
                      rate_func=linear)
        self.at("over days")
        lab = T("over days", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(lab), run_time=0.5)  # counter holds at day 6
        self.finish()


class S10Label(SpokenScene):
    def construct(self):
        d = stage(5, colored=True)
        self.add(*base_group(d), *axon_group(d), d["la"], d["lb"], d["tlabel"])
        self.at("A fluorescent snake toxin")
        tox = bchip("fluorescent snake toxin", VIOLET, size=28).move_to([0, -3.05, 0])
        self.play(FadeIn(tox, shift=UP * 0.2), run_time=0.6)
        self.at("marked the receptors")
        dots = [Dot(radius=0.13, color=VIOLET).move_to([XS[i], -2.75, 0]) for i in BOUND]
        self.add(*dots)
        leg = legend_purple()
        self.play(*[dt.animate.move_to([XS[i], RY, 0]) for dt, i in zip(dots, BOUND)], FadeIn(leg, shift=DOWN * 0.1),
                  run_time=0.9)
        self.play(*[FadeOut(dt) for dt in dots],
                  *[d["rec"][i].animate.set_stroke(VIOLET).set_fill(VIOLET, 0.85) for i in BOUND], run_time=0.5)
        self.at("The dose was small")
        l1 = T("low dose: only some receptors bound", 26, VIOLET)
        l2 = T("transmission preserved", 26, GREEN)
        gtxt = VGroup(l1, l2).arrange(DOWN, buff=0.1)
        box = RoundedRectangle(corner_radius=0.14, width=gtxt.width + 0.5, height=gtxt.height + 0.35, stroke_color=VIOLET,
                               stroke_width=2.5, fill_color=VIOLET, fill_opacity=0.16).move_to(gtxt)
        tag = VGroup(box, l1, l2).move_to([0, -3.1, 0])
        l2.set_opacity(0)
        self.play(ReplacementTransform(tox, tag), run_time=0.6)
        self.at("transmission still worked")
        a, b = pdot(XS[0], YTOP), pdot(XS[-1], YTOP)
        self.add(a, b)
        self.play(a.animate.move_to([XS[0], YT, 0]), b.animate.move_to([XS[-1], YT, 0]), run_time=0.7, rate_func=linear)
        free = [d["rec"][i] for i in range(N) if i not in BOUND]
        self.play(FadeOut(a), FadeOut(b), *[Indicate(r, color=YELLOW, scale_factor=1.2) for r in free],
                  l2.animate.set_opacity(1), run_time=0.9)
        self.finish()


def s11_state(scene, question=True):
    d = stage(5, colored=True, bound=BOUND)
    ct = counter_text(0)
    br = VGroup(bracket(XS[0] - 0.6, XS[4] + 0.6, -2.35, BLUE), bracket(XS[5] - 0.6, XS[7] + 0.6, -2.35, ORANGE))
    leg = legend_purple()
    scene.add(*base_group(d), *axon_group(d), d["la"], d["lb"], ct, leg)
    q = None
    if question:
        scene.add(br)
        q = T("Does the bigger territory win?", 34, TEXT).move_to([0, -2.85, 0])
        scene.add(q)
    return d, ct, br, q


class S11Predict(SpokenScene):
    def construct(self):
        d = stage(5, colored=True, bound=BOUND)
        ct = counter_text(0)
        leg = legend_purple()
        self.add(*base_group(d), *axon_group(d), d["la"], d["lb"], ct, leg)
        pre = bchip("Predict", TEXT, size=34).move_to([0, -3.0, 0])
        self.play(FadeIn(pre, shift=UP * 0.2), run_time=0.5)
        self.at("Axon A starts")
        br = VGroup(bracket(XS[0] - 0.6, XS[4] + 0.6, -2.35, BLUE), bracket(XS[5] - 0.6, XS[7] + 0.6, -2.35, ORANGE))
        self.play(Create(br[0]), run_time=0.7)
        self.at("more of the receptor map")
        self.play(Indicate(VGroup(*d["bead"][:5]), color=BLUE, scale_factor=1.04), Create(br[1]), run_time=1.0)
        self.at("Does the bigger territory win")
        q = T("Does the bigger territory win?", 34, TEXT).move_to([0, -2.85, 0])
        self.play(ReplacementTransform(pre, q), run_time=0.7)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        s11_state(self)
        opts = [chip(t, TEXT, size=26, pad=0.12) for t in ("bigger wins", "smaller wins", "can't tell")]
        row = VGroup(*opts).arrange(RIGHT, buff=0.5).move_to([-0.6, -3.5, 0])
        tr = ValueTracker(0)

        def ring():
            ang = max(1e-3, TAU * (1 - tr.get_value()))
            c = np.array([5.5, -3.5, 0.0])
            return VGroup(Circle(radius=0.3, stroke_color=GREY, stroke_width=3).move_to(c),
                          Arc(radius=0.3, start_angle=PI / 2, angle=ang, stroke_color=YELLOW, stroke_width=7,
                              arc_center=c))
        rg = always_redraw(ring)
        self.add(rg)
        for o in opts:
            self.play(FadeIn(o, shift=UP * 0.15), run_time=0.4)
            self.wait(0.5)
        self.play(tr.animate.set_value(1.0), run_time=max(0.5, self.narration_s - self.elapsed() - 0.3), rate_func=linear)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        rows = [(1.75, 5, 8), (0.45, 3, 8), (-0.85, 6, 0), (-2.15, 2, 0)]   # (y, A's start, end: 8 = A holds, 0 = B holds)
        XSTART, XEND, XANS = -4.3, 0.95, 5.2
        h1 = T("start", 28, TEXT).move_to([XSTART, 3.3, 0])
        h2 = T("typical end state", 28, TEXT).move_to([XEND, 3.3, 0])
        h3 = VGroup(T("did the bigger", 26, TEXT), T("start win?", 26, TEXT)).arrange(DOWN, buff=0.05).move_to([XANS, 3.3, 0])
        starts = [cellbar(XSTART, y, k, h=0.7) for y, k, _ in rows]
        ends = [cellbar(XEND, y, e, h=0.7) for y, _, e in rows]
        arrs = [Arrow([-2.0, y, 0], [-1.3, y, 0], buff=0, color=GREY, stroke_width=5) for y, _, _ in rows]
        labs = []
        for y, k, e in rows:
            bigger_a = k > 4
            wins = (bigger_a and e == 8) or ((not bigger_a) and e == 0)
            labs.append(T("yes" if wins else "no", 44, GREEN if wins else RED, weight=BOLD).move_to([XANS, y, 0]))
        leg = legend_ab(y=-3.0, x=-2.2)
        tag = T("other junctions • schematic, not data", 24, GREY).move_to([-2.2, -3.55, 0])
        self.play(FadeIn(h1), LaggedStart(*[FadeIn(s) for s in starts], lag_ratio=0.15), FadeIn(tag), FadeIn(leg),
                  run_time=1.2)
        self.at("The starting territory")
        self.play(ShowPassingFlash(SurroundingRectangle(VGroup(*starts), color=TEXT, buff=0.15, stroke_width=6),
                                  time_width=1.0), run_time=0.9)
        self.at("did not reliably")
        self.play(FadeIn(h2), FadeIn(h3),
                  LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(e)) for a, e in zip(arrs, ends)], lag_ratio=0.3),
                  run_time=1.4)
        self.at("predict the winner")
        self.play(LaggedStart(*[FadeIn(l, scale=0.7) for l in labs], lag_ratio=0.2), run_time=0.9)
        self.wait(2.0)                                   # hold the finished table
        self.finish()


class S14Shift(SpokenScene):
    def construct(self):
        o = np.array([-5.0, -2.65, 0.0])
        W, H = 10.4, 5.35

        def c2p(t, s):
            return o + np.array([t / 10.0 * W, s * H, 0.0])

        def share(t):
            """axon A's share of the receptor map in one junction: starts at 5 of 8, rises, then falls back (schematic)"""
            return 0.625 + 0.17 * np.exp(-((t - 3.0) / 1.5) ** 2) - 0.52 / (1 + np.exp(-(t - 6.8) / 1.0))

        ts = np.linspace(0, 10, 2001)
        tcross = float(ts[np.argmax(np.array([share(t) for t in ts]) < 0.5)])

        outline = Rectangle(width=W, height=H, stroke_color=GREY, stroke_width=3).move_to(c2p(5, 0.5))
        ylab = [T("0%", 26, GREY).move_to(c2p(0, 0) + np.array([-0.55, 0, 0])),
                T("50%", 26, GREY).move_to(c2p(0, 0.5) + np.array([-0.6, 0, 0])),
                T("100%", 26, GREY).move_to(c2p(0, 1) + np.array([-0.7, 0, 0]))]
        xlab = [T(str(k), 26, GREY).move_to(c2p(k, 0) + np.array([0, -0.36, 0])) for k in (0, 5, 10)]
        xt = T("days", 26, GREY).move_to([0.2, -3.55, 0])
        yt = T("axon A's share of the receptor map", 26, GREY).move_to([-2.0, 3.25, 0])
        tag = T("one junction, schematic", 26, GREY).move_to([4.6, 3.25, 0])
        tr = ValueTracker(0.05)

        def area():
            tmax = tr.get_value()
            tt = np.linspace(0, tmax, max(4, int(tmax * 24)))
            pa = [c2p(t, share(t)) for t in tt]
            A = Polygon(c2p(0, 0), *pa, c2p(tt[-1], 0), stroke_width=0, fill_color=BLUE, fill_opacity=0.6)
            B = Polygon(*pa, c2p(tt[-1], 1), c2p(0, 1), stroke_width=0, fill_color=ORANGE, fill_opacity=0.6)
            ln = VMobject(stroke_color=TEXT, stroke_width=5).set_points_as_corners(pa)
            return VGroup(A, B, ln)

        ar = always_redraw(area)
        self.add(ar)
        d0 = Dot(c2p(0, share(0)), radius=0.1, color=TEXT)
        a0text = T("day 0: 5 of 8 sites (62%)", 26, TEXT)
        a0bg = RoundedRectangle(corner_radius=0.12, width=a0text.width + 0.3,
                                height=a0text.height + 0.22, stroke_width=0,
                                fill_color=BG, fill_opacity=1)
        a0 = VGroup(a0bg, a0text).move_to(c2p(0.6, 0.47), aligned_edge=LEFT).set_z_index(3)
        l0 = Line(c2p(0, share(0)), a0.get_left() + np.array([-0.05, 0.0, 0]), color=TEXT, stroke_width=3)
        la = T("axon A", 30, TEXT).move_to(c2p(1.3, 0.17))
        lb = T("axon B", 30, TEXT).move_to(c2p(1.3, 0.92))
        self.play(Create(outline), *[FadeIn(m) for m in ylab + xlab + [xt, yt, tag, la, lb, d0, a0, l0]], run_time=0.5)
        self.at("shift one way")
        self.play(tr.animate.set_value(4.4), run_time=0.65, rate_func=linear)
        self.at("then back")
        self.play(tr.animate.set_value(tcross), run_time=0.27, rate_func=linear)
        dl = DashedLine(c2p(tcross, 0), c2p(tcross, 1), color=TEXT, stroke_width=3)
        rl = T("the lead reverses", 26, TEXT).move_to(c2p(tcross + 0.25, 0.93), aligned_edge=LEFT)
        self.play(Create(dl), FadeIn(rl), run_time=0.2)
        self.play(tr.animate.set_value(10.0), run_time=0.5, rate_func=linear)
        self.finish()


class S15Takeover(SpokenScene):
    def construct(self):
        d = stage(5, colored=True, bound=BOUND)          # the same 5 vs 3 map as the predict scene
        dv = ValueTracker(0)
        ct = counter(dv)
        tag = T("schematic: typical, not every junction", 24, GREY).move_to([0, -3.4, 0])
        leg = legend_purple()
        self.add(*base_group(d), *axon_group(d), d["la"], d["lb"], ct, tag, leg)
        lineA, lineB = d["lineA"], d["lineB"]
        self.at("withdrew")
        # axon A withdraws from its sites, the one nearest axon B first, 0.9 s per site
        for k, i in enumerate([4, 3, 2, 1, 0]):
            anims = [FadeOut(d["bead"][i], shift=LEFT * 0.3), dv.animate.set_value(1.2 * (k + 1))]
            if i >= 2:
                anims.append(Transform(lineA, Line([XS[0], YT, 0], [XS[i - 1], YT, 0], color=BLUE, stroke_width=10)))
            elif i == 1:
                anims.append(FadeOut(lineA))
            else:
                anims += [FadeOut(d["shA"]), FadeOut(d["la"])]
            self.play(*anims, run_time=0.9, rate_func=linear)
        self.at("The other extended")
        # B grows into each vacated site from its own edge (no overlap with its neighbour)
        for k, i in enumerate([4, 3, 2, 1, 0]):
            nb = bead(XS[i], YT, ORANGE)
            self.play(FadeIn(nb),
                      Transform(lineB, Line([XS[-1], YT, 0], [XS[i], YT, 0], color=ORANGE, stroke_width=10)),
                      dv.animate.set_value(6 + 0.8 * (k + 1)), run_time=0.5, rate_func=linear)
        self.wait(1.2)
        self.finish()


def s16_state(scene):
    d = stage(0, colored=True, bound=BOUND)
    d["shA"].set_opacity(0)
    d["la"].set_opacity(0)
    ct = counter_text(10)
    tag = T("schematic: typical, not every junction", 24, GREY).move_to([0, -3.4, 0])
    leg = legend_purple()
    scene.add(*base_group(d), d["lineB"], d["shB"], *d["bead"], d["lb"], ct, tag, leg)
    return d


class S16Beat(NarratedScene):
    def construct(self):
        s16_state(self)
        self.finish()


class S17Take(SpokenScene):
    def construct(self):
        ys = [2.4, 0.0, -2.4]
        xl = -2.4
        XI = -4.3

        def text_rows(a, b, y, color=TEXT):
            g = VGroup(T(a, 50, color), T(b, 50, color)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            g.move_to([0, y, 0]).align_to([xl, 0, 0], LEFT)
            return g

        r1, r2, r3 = (text_rows("starting size alone", "does not reliably decide", ys[0]),
                      text_rows("each junction runs", "its own contest", ys[1]),
                      text_rows("what tips it is", "the next question", ys[2]))
        big = Rectangle(width=1.6, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7)
        q1 = T("?", 72, TEXT, weight=BOLD)
        small = Rectangle(width=0.75, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.7)
        icon1 = VGroup(big, q1, small).arrange(RIGHT, buff=0.25).move_to([XI, ys[0], 0])
        cl = [clock(x, ys[1], CLOCK_ANG[k], r=0.42) for k, x in enumerate([XI - 1.15, XI, XI + 1.15])]
        qm = T("?", 140, YELLOW, weight=BOLD).move_to([XI, ys[2], 0])
        # Keep the complete, vertically centred card visible from the start;
        # brighten each thought as its sentence arrives.
        for mob in (icon1, r1, *cl, r2, qm, r3):
            mob.set_opacity(0.35)
            self.add(mob)
        self.at("So starting size alone")
        self.play(icon1.animate.set_opacity(1), r1[0].animate.set_opacity(1), run_time=0.7)
        self.at("does not reliably decide")
        self.play(r1[1].animate.set_opacity(1), Indicate(q1, color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.play(Indicate(big, color=WHITE, scale_factor=1.1), run_time=0.5)
        self.play(Indicate(small, color=WHITE, scale_factor=1.1), run_time=0.5)
        self.at("Each junction runs")
        self.play(LaggedStart(*[c.animate.set_opacity(1) for c in cl], lag_ratio=0.15), r2[0].animate.set_opacity(1),
                  run_time=0.8)
        for k, c in enumerate(cl):
            spin(c, CLOCK_W[k])
        self.at("its own contest")
        self.play(r2[1].animate.set_opacity(1), run_time=0.6)
        self.at("what tips it")
        self.play(qm.animate.set_opacity(1), r3[0].animate.set_opacity(1), run_time=0.6)
        self.at("is the next question")
        self.play(r3[1].animate.set_opacity(1), run_time=0.6)
        self.finish()


class S18End(EndCard):
    LINE = "Starting size alone does not reliably predict a junction's winner."

    def construct(self):
        l1 = T("Starting size alone does not", 46, font=TITLE_FONT)
        l2 = T("reliably predict a junction's winner.", 46, font=TITLE_FONT)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.2)
        fit(g, max_w=12.4)
        sub = T("biochemistrypedia.com", 24, color=TEAL)
        allg = VGroup(g, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(g, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
