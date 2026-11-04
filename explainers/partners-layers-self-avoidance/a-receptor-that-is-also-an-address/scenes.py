"""Chapter 3: A Receptor That Is Also an Address  (Biochemistrypedia chaptered film)

COLOR MAP (one colour per concept, shared by every chapter of this lesson)
  BLUE   = the P2 receptor: its neurons, its marked axons, its glomerulus (the channel we follow)
  ORANGE = the M12 receptor and M12's own glomerulus
  PURPLE, PINK, SAND = other receptor types (other neurons in the nose); PURPLE also = Dscam1 (self-avoidance panel)
  YELLOW = Sidekick (matching label that binds its own kind)
  WHITE  = the odorant (the smell molecule)
  GREEN  = pulled together / stick;  RED = pushed apart / missing / failed
  GOLD   = cards and headings ("Predict.", "Rule 1", "Takeaway")
  GREY   = neutral cells, structure, neuropil, the bulb and the nose outline
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB6"
SAND = "#C8A97E"
OTHERS = [PURPLE, PINK, SAND]


class SpokenScene(SpokenScene):
    """Give each completed visual a readable hold, including after the last word."""
    def finish(self):
        self.wait(2.4)
        super().finish()



# ------------------------------------------------------------------------------------------------
# helpers
def P(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def path(pts, color, w=5, op=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op, fill_opacity=0)
    m.set_points_smoothly([P(x, y) for x, y in pts])
    return m


def tag(text, size=24, color=GREY):
    return T(text, max(26, size), color)


def cup(pos, ang=PI, color=BLUE, s=1.0):
    """A receptor drawn as a small cup that opens in direction `ang` (stem on the membrane)."""
    d = np.array([np.cos(ang), np.sin(ang), 0.0])
    r = 0.15 * s
    p = P(pos[0], pos[1])
    sw = max(3.0, 5 * s)
    arc = Arc(radius=r, start_angle=ang + PI / 2, angle=PI, arc_center=p + d * r, stroke_color=color, stroke_width=sw)
    stem = Line(p - d * 0.14 * s, p, color=color, stroke_width=sw)
    return VGroup(arc, stem)


def neu(x, y, color=GREY, s=1.0, fill=0.35):
    """A nose neuron: soma, short dendrite to the left, receptor cup at its tip."""
    r = 0.27 * s
    back = Circle(r, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(P(x, y))
    soma = Circle(r, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=fill).move_to(P(x, y))
    dend = Line(P(x - r, y), P(x - r - 0.3 * s, y), color=color, stroke_width=3.5)
    c = cup((x - r - 0.3 * s, y), PI, color, 1.0 * s)
    return VGroup(back, soma, dend, c)


def tint(n, color, fill=0.35):
    return [n[1].animate.set_stroke(color).set_fill(color, fill), n[2].animate.set_color(color),
            n[3].animate.set_color(color)]


def glom(x, y, color=BLUE, r=0.35, op=0.55):
    return Circle(r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(P(x, y))


def strip():
    return RoundedRectangle(corner_radius=0.3, width=3.4, height=5.9, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.08).move_to(P(-4.5, -0.05))


def bulb(cx=3.4, cy=0.0, w=5.4, h=6.2):
    return Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.08).move_to(P(cx, cy))


NEU = {'A0': (-5.2, 2.45), 'A1': (-5.2, 1.45), 'A2': (-5.2, 0.3), 'A3': (-5.2, -0.8), 'A4': (-5.2, -1.9),
       'B0': (-4.2, 1.95), 'B1': (-4.2, 0.65), 'B2': (-4.2, -0.45), 'B3': (-4.2, -1.55), 'B4': (-4.2, -2.6),
       'C0': (-3.2, 2.4), 'C1': (-3.2, 1.4), 'C2': (-3.2, 0.2), 'C3': (-3.2, -0.9), 'C4': (-3.2, -2.0)}
BLUES = ['A2', 'B1', 'C2', 'A3', 'B3', 'C4']
OTHER_IDS = [k for k in NEU if k not in BLUES]
OTHER_COL = {k: OTHERS[i % 3] for i, k in enumerate(OTHER_IDS)}
P_ID = 'B1'          # the neuron followed in the opening scene

# axons of the six blue neurons to the two glomeruli of the bulb (top = medial, bottom = lateral)
G_TOP, G_BOT = (2.3, 1.5), (2.3, -1.5)
AXONS = {
    'A2': [(-4.9, .3), (-3.0, .55), (-1.5, .95), (0.0, 1.3), (1.1, 1.5), (2.05, 1.35)],
    'B1': [(-3.9, .65), (-2.6, .85), (-1.0, 1.2), (0.2, 1.4), (1.1, 1.5), (2.05, 1.5)],
    'C2': [(-2.9, .2), (-1.8, .55), (-0.4, 1.2), (1.1, 1.5), (2.05, 1.65)],
    'A3': [(-4.9, -.8), (-3.0, -.95), (-1.5, -1.2), (0.0, -1.4), (1.1, -1.5), (2.05, -1.35)],
    'B3': [(-3.9, -1.55), (-2.5, -1.5), (-1.0, -1.45), (1.1, -1.5), (2.05, -1.5)],
    'C4': [(-2.9, -2.0), (-1.7, -1.9), (-0.4, -1.6), (1.1, -1.5), (2.05, -1.65)],
}


def nose_neurons(blue_col=BLUE, others=True, tinted=False):
    """dict id -> neuron group. Blue ones are blue; others grey (or tinted by receptor type)."""
    out = {}
    for k, (x, y) in NEU.items():
        if k in BLUES:
            out[k] = neu(x, y, blue_col)
        elif others:
            out[k] = neu(x, y, OTHER_COL[k] if tinted else GREY)
    return out


# the predict stage (scenes 10-17): locus on top, marked neurons left, bulb right
PB = (2.8, -0.75, 6.8, 5.8)
NX = -4.15
NYS = [0.3, -1.2, -2.7]
YES = [0.2, -1.1, -2.2]
P2G = (1.5, 0.45)
NEWG = (1.65, -1.35)
M12G = (4.8, -2.1)


def bchip(text, color=BLUE, size=26, pad=0.18, fill_opacity=0.16):
    c = chip(text, color, size=size, pad=pad, fill_opacity=fill_opacity)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def locus(y, coding_text="P2 receptor", coding_col=BLUE):
    prom = bchip("P2 promoter", GREY)
    cod = bchip(coding_text, coding_col)
    mk = bchip("marker", BLUE, fill_opacity=0.55)
    row = VGroup(prom, cod, mk).arrange(RIGHT, buff=0.35).move_to(P(0.9, y))
    line = Line(P(row.get_left()[0] - 0.25, y), P(row.get_right()[0] + 0.6, y), color=GREY, stroke_width=4)
    name = tag("P2 locus", 24, GREY).next_to(row, LEFT, buff=0.45)
    return line, prom, cod, mk, name


def pred_neurons(cup_col=None):
    g = VGroup()
    for y in NYS:
        n = neu(NX, y, BLUE, 1.6)
        if cup_col is None:
            n = VGroup(n[0], n[1], n[2])
        else:
            n[3].set_color(cup_col)
        g.add(n)
    return g


def pred_seg1():
    return VGroup(*[path([(NX + 0.4, y), (-2.7, 0.5 * (y + ye)), (0.85, ye)], BLUE, 5) for y, ye in zip(NYS, YES)])


def pred_seg2():
    out = []
    for ye, d in zip(YES, (0.2, 0.0, -0.2)):
        out.append(path([(0.85, ye), (1.0, 0.5 * (ye + NEWG[1])), (1.1, NEWG[1] + d), (NEWG[0] - 0.25, NEWG[1] + d * 0.5)],
                        BLUE, 5))
    return VGroup(*out)


def qmarks():
    return VGroup(*[T("?", 54, GREY).move_to(P(x, y)) for x, y in [(1.1, ye) for ye in YES]])


def qtext(text):
    return T(text, 30, TEXT).move_to(P(-1.3, -3.4)).add_background_rectangle(color=BG, buff=.08)


# ------------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Choosing a Partner: Layers, Self-Avoidance and Smell"
    TITLE = "A Receptor That Is Also an Address"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 26, TEAL)
        title = Paragraph("A Receptor That Is", "Also an Address", alignment="center",
                          font_size=52, font=TITLE_FONT, color=TEXT, line_spacing=1.2).move_to(ORIGIN)
        brand.move_to(P(0, 2.5))
        rule = Line(P(-1.3, -2), P(1.3, -2), color=GOLD, stroke_width=4)
        self.add(brand)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.5)
        self.finish()

# ------------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        st, bl = strip(), bulb()
        n = neu(-4.2, 0.3, BLUE, 2.5)
        rec = tag("receptor", 28, BLUE).move_to(P(-4.5, -1.4))
        axon = path([(-3.5, .3), (-1.8, -.6), (.1, .5), (1.5, 1.4), (3.0, 1.4)], BLUE, 10)
        q = T("?", 80, GOLD).move_to(P(3.5, 1.4))
        smell = Dot(P(-6.0, 2.0), radius=.16, color=TEXT)
        sl = tag("smell", 28, TEXT).move_to(P(-4.8, 2.4))
        self.add(st, bl, tag("nose", 28, TEXT).move_to(P(-4.5, 3.35)),
                 tag("olfactory bulb", 28, TEXT).move_to(P(3.4, 3.35)), n)
        self.at("protein")
        self.play(FadeIn(rec), Indicate(n[3]), run_time=.5)
        self.at("detects")
        self.play(FadeIn(smell), FadeIn(sl), run_time=.3)
        self.play(smell.animate.move_to(n[3].get_center()), run_time=.6)
        self.at("also tell")
        self.play(Create(axon), run_time=1)
        self.at("where to go")
        self.play(FadeIn(q), run_time=.4)
        self.finish()

# ------------------------------------------------------------------------------------------------
class S02Buck(SpokenScene):
    def construct(self):
        yr = M("1991", 50, GOLD).move_to(P(0, 3))
        credit = T("Linda Buck and Richard Axel", 30).move_to(P(0, 2.15))
        # A labelled receptor chip, not a molecular structure.
        receptor = chip("seven-helix\nreceptor", BLUE, size=36, pad=.45).move_to(P(-3, -.2))
        membrane = Rectangle(width=5.5, height=.55, color=GREY, fill_opacity=.2).move_to(P(-3, -.2))
        note = T("schematic", 26, TEXT).move_to(P(-3, -1.65))
        stats = VGroup(M("100+", 54), T("genes in rat", 28),
                       M("~1,000", 54), T("genes in mouse, later", 28)).arrange(DOWN, buff=.3).move_to(P(3.2, -.4))
        receptor[0].set_fill(BG, 1)
        self.add(membrane, receptor, note, yr)
        self.at("linda buck")
        self.play(FadeIn(credit), run_time=.5)
        self.at("found the")
        self.play(Indicate(receptor, color=TEXT), run_time=.6)
        self.at("genes")
        self.play(FadeIn(stats), run_time=.6)
        self.finish()

# ------------------------------------------------------------------------------------------------
class S03Rule1(SpokenScene):
    def construct(self):
        st = strip()
        neus = nose_neurons(others=True)
        ring = Circle(0.5, stroke_color=TEXT, stroke_width=3).move_to(P(*NEU[P_ID]))
        h = T("RULE 1", 30, GOLD).move_to(P(2.4, 1.9))
        l1 = T("one neuron", 50, font=TITLE_FONT).move_to(P(2.4, 0.8))
        l2 = T("one receptor", 50, BLUE, font=TITLE_FONT).move_to(P(2.4, -0.4))
        l3 = tag("rare exceptions", 28, TEXT).move_to(P(2.4, -1.5))
        self.add(st)
        self.play(FadeIn(VGroup(*neus.values()), lag_ratio=0.04), run_time=0.9)
        self.at("rule is")
        self.play(FadeIn(h), run_time=0.4)
        self.at("one neuron")
        self.play(Create(ring), FadeIn(l1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("one receptor")
        anims = [FadeOut(ring), FadeIn(l2, shift=RIGHT * 0.2), Indicate(neus[P_ID][3], color=TEXT, scale_factor=1.6)]
        for k in OTHER_IDS:
            anims += tint(neus[k], OTHER_COL[k])
        self.play(*anims, run_time=0.9)
        self.at("rare exceptions")
        self.play(FadeIn(l3), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S04Scatter(SpokenScene):
    def construct(self):
        st = strip()
        neus = nose_neurons(tinted=True)
        zone = DashedVMobject(RoundedRectangle(width=3.5, height=5.95, corner_radius=.3, color=TEXT, stroke_width=3).move_to(P(-4.5, -0.05)),
                              num_dashes=40)
        zl = tag("one zone of the nose", 30, TEXT).move_to(P(2, -1.2))
        za = arr(P(-.3, -1.2), P(-2.7, -1.2), TEXT, 4)
        lc = cup((0.5, 1.6), PI, BLUE, 1.8)
        lt = tag("same receptor", 32, BLUE).move_to(P(2.5, 1.6))
        self.add(st, *neus.values())
        self.at("same receptor")
        self.play(*[a for k in OTHER_IDS for a in
                    [neus[k][1].animate.set_stroke(GREY).set_fill(GREY, 0.35), neus[k][2].animate.set_color(GREY),
                     neus[k][3].animate.set_color(GREY)]], FadeIn(lc), FadeIn(lt), Create(Line(P(.1, 1.6), P(-2.85, .2), color=BLUE, stroke_width=3)), run_time=0.8)
        self.at("scattered")
        self.play(*[Indicate(neus[k][1], color=TEXT, scale_factor=1.35) for k in BLUES], run_time=1.0)
        self.at("zone")
        self.play(Create(zone), FadeIn(zl), GrowArrow(za), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S05Converge(SpokenScene):
    def construct(self):
        neus = nose_neurons()
        for n in neus.values(): n.set_z_index(3)
        ax = VGroup(*[path([(NEU[k][0]+.3, NEU[k][1]), (-1, (NEU[k][1]+1.5)/2), (.6,1.5), (2.1,1.5)], BLUE, 5) for k in BLUES])
        g = glom(*G_TOP, r=.45)
        self.add(strip(), *neus.values(), bulb(cy=.2,h=5.8),
                 tag("nose", 28, TEXT).move_to(P(-4.5, 3.35)),
                 tag("olfactory bulb", 28, TEXT).move_to(P(3.4, 3.35)))
        self.at("axons")
        self.play(Create(ax), run_time=1)
        self.at("glomeruli")
        self.play(GrowFromCenter(g), FadeIn(tag("glomerulus", 28, BLUE).move_to(P(4.3,1.5))), run_time=.5)
        self.at("olfactory bulb")
        self.play(FadeIn(T("one receptor, one channel", 30, BLUE).move_to(P(1.5,-3.2))), run_time=.5)
        self.finish()

# ------------------------------------------------------------------------------------------------
class S06Glom(SpokenScene):
    def construct(self):
        rs = np.random.RandomState(7)
        BC = P(-1.7, -0.1)
        R = 2.9
        ball = Circle(R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(BC)
        name = T("glomerulus", 34).move_to(P(-1.7, 3.3))

        def wander(n, col, w):
            pts = []
            for i in range(n):
                a = rs.uniform(0, 2 * PI)
                r = rs.uniform(0.2, R - 0.45)
                pts.append((BC[0] + r * np.cos(a), BC[1] + r * np.sin(a)))
            return path(pts, col, w, 0.85)

        tangle = VGroup(*[wander(5, GREY, 3) for _ in range(7)])
        syn = VGroup(*[Circle(0.07, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to(
            P(BC[0] + rs.uniform(-1.8, 1.8), BC[1] + rs.uniform(-1.8, 1.8))) for _ in range(9)])
        lab = VGroup(T("neuropil", 38, TEXT),
                     T("a tangle of\naxons, dendrites\nand synapses", 28, TEXT, line_spacing=0.9),
                     T("no cell bodies\ninside the ball", 26, TEXT)).arrange(DOWN, buff=0.35).move_to(P(4.6, 1.0))
        ax = VGroup(*[path([(-6.3, y0), (-4.6, y0 * 0.6), (-3.2, y0 * 0.5), (-2.0, y0 * 0.3), (-1.0, y0 * 0.2 - 0.1)],
                           BLUE, 5) for y0 in (1.6, 0.0, -1.5)])
        bn = VGroup()
        for y0 in (1.4, -1.5):
            soma = Circle(0.38, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.4).move_to(P(2.0, y0))
            den = path([(1.65, y0), (1.1, y0 * 0.6), (0.2, y0 * 0.2), (-0.6, y0 * 0.1 - 0.1)], GREY, 4)
            bn.add(VGroup(den, soma))
        self.at("glomerulus")
        self.play(GrowFromCenter(ball), FadeIn(name), run_time=0.8)
        self.at("neuropill")
        self.play(Create(tangle, lag_ratio=0.1), FadeIn(syn, lag_ratio=0.1), FadeIn(lab, shift=LEFT * 0.2), FadeIn(tag("synapses", 28, TEXT).move_to(P(-4.8,-2.9))), Create(Line(P(-4,-2.7), syn[0].get_center(), color=TEXT, stroke_width=2)), run_time=0.9)
        self.at("sensory axons")
        self.play(*[Create(a) for a in ax], run_time=1.0)
        self.at("bulb neurons")
        self.play(FadeIn(bn, lag_ratio=0.3), FadeIn(T("bulb neurons\n(cell bodies lie outside)", 26, TEXT).move_to(P(4.1,-2.3))), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S07P2(SpokenScene):
    def construct(self):
        yr = M("1996", 48, GOLD).move_to(P(-5.2, 3.2))
        credit = T("Peter Mombaerts and colleagues", 28, TEXT).move_to(P(0.2, 3.2))
        line, prom, cod, mk, name = locus(1.5)
        soma = Circle(1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to(P(-4.9, -0.9))
        axon = path([(-3.75, -.9), (-2.5, .0), (0.0, -1.1), (2.5, -.1), (5.2, -.8)], GREY, 11)
        tip = Circle(0.28, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(P(5.2, -.8))
        nlab = tag("a neuron and its axon", 26, GREY).move_to(P(0, -2.7))
        mlab = tag("marked axon", 28, BLUE).move_to(P(0, -2.7))
        self.play(FadeIn(VGroup(line, prom, cod, mk, name)), FadeIn(VGroup(soma, axon, tip)), FadeIn(nlab),
                  run_time=0.4)
        self.at("1996")
        self.play(FadeIn(yr, shift=DOWN * 0.1), run_time=0.5)
        self.at("peter")
        self.play(FadeIn(credit), run_time=0.6)
        self.at("marked axons")
        self.play(Indicate(mk[1:], color=TEXT, scale_factor=1.15),
                  axon.animate.set_color(BLUE), tip.animate.set_fill(BLUE), soma.animate.set_stroke(BLUE).set_fill(BLUE, 0.35),
                  ReplacementTransform(nlab, mlab), run_time=1.2)
        self.at("p2 promoter")
        self.play(Indicate(prom[1:], color=TEXT, scale_factor=1.15), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S08Pair(SpokenScene):
    def construct(self):
        neus = nose_neurons()
        for n in neus.values(): n.set_z_index(3)
        ax = VGroup(*[path([(NEU[k][0]+.3,NEU[k][1]), (-1,(NEU[k][1]+1.5)/2),(.6,1.5),(2.1,1.5)], BLUE,5) for k in BLUES])
        ax2 = VGroup(*[path([(NEU[k][0]+.3,NEU[k][1]),(-1,-1.6),(2,-1.5),(4.5,-1.5)],BLUE,5) for k in BLUES[3:]])
        g1,g2 = glom(*G_TOP,r=.45),glom(4.8,-1.5,r=.45)
        midline = DashedLine(P(.6,-2.8),P(.6,2.8),color=TEXT,stroke_width=2)
        cue = tag("midline",26,TEXT).move_to(P(.35,3.35))
        self.add(strip(),*neus.values(),bulb(cy=.2,h=5.8),ax,g1,
                 tag("nose",28,TEXT).move_to(P(-4.5,3.35)),
                 tag("olfactory bulb",28,TEXT).move_to(P(3.4,3.35)))
        self.at("two glomeruli")
        self.play(Create(ax2),GrowFromCenter(g2),run_time=.6)
        self.at("one medial")
        self.play(Create(midline),FadeIn(cue),FadeIn(tag("medial",28,BLUE).move_to(P(3.9,1.5))),run_time=.5)
        self.at("one lateral")
        self.play(FadeIn(tag("lateral",28,BLUE).move_to(P(4.8,-.65))),run_time=.5)
        self.at("one receptor")
        self.play(FadeIn(T("one receptor, one channel",30,BLUE).move_to(P(-3.7,-3.2))),run_time=.4)
        self.at("about two glomeruli")
        self.play(FadeIn(T("about two glomeruli per bulb",28,TEXT).move_to(P(3.3,-3.2))),run_time=.5)
        self.finish()

# ------------------------------------------------------------------------------------------------
def surface_cups(center, r, angles, s, color=BLUE):
    g = VGroup()
    for a in angles:
        pos = (center[0] + r * np.cos(a), center[1] + r * np.sin(a))
        g.add(cup(pos, a, color, s))
    return g


class S09Address(SpokenScene):
    def construct(self):
        soma = Circle(1.1,color=BLUE,fill_opacity=.3).move_to(P(-1.35,-.35))
        dend = VGroup(Line(P(-4.7,1.35),P(-2.2,.35),color=BLUE,stroke_width=9),
                      Line(P(-3.65,.93),P(-3.9,2.35),color=BLUE,stroke_width=7),
                      Line(P(-3.9,1.03),P(-4.9,-.15),color=BLUE,stroke_width=7))
        ax = path([(-.25,-.35),(1.0,-1.75),(2.8,-1.4),(3.65,-.4)],BLUE,10)
        term = Circle(.8,color=BLUE,fill_opacity=.3).move_to(P(4.25,.0))
        dc = VGroup(cup((-4.7,1.35),PI,BLUE,1.8),
                    cup((-3.9,2.35),PI/2,BLUE,1.8),
                    cup((-4.9,-.15),PI,BLUE,1.8))
        tc = surface_cups((4.25,0),.8,[0,PI/3,-PI/3],1.8)
        self.add(soma,dend,ax,term,
                 tag("soma",28,TEXT).move_to(P(-1.35,-1.95)),
                 tag("dendrite",28,TEXT).move_to(P(-3.9,3.2)),
                 tag("axon",28,TEXT).move_to(P(1.3,-2.35)),
                 tag("axon terminal",28,TEXT).move_to(P(4.4,-1.3)))
        self.at("receptor protein")
        self.play(FadeIn(dc),FadeIn(tag("receptors",28,BLUE).move_to(P(-4.5,-1.15))),run_time=.5)
        self.at("also reaches")
        self.play(ShowPassingFlash(ax.copy().set_color(TEXT)),run_time=.7)
        self.at("axon terminals")
        self.play(FadeIn(tc),run_time=.5)
        self.at("address")
        self.play(FadeIn(T("?",76,GOLD).move_to(P(5.8,1.2))),
                  FadeIn(T("part of the address?",36,GOLD).move_to(P(0,-3.25))),run_time=.5)
        self.finish()

# ------------------------------------------------------------------------------------------------
class S10Predict1(SpokenScene):
    def construct(self):
        h = T("Predict.", 40, GOLD).move_to(P(-5.2, 3.3))
        line, prom, cod, mk, name = locus(2.65)
        bl = bulb(*PB)
        nn = pred_neurons(None)
        ax = pred_seg1()
        x1 = VGroup()
        dl = tag("deleted", 26, RED).next_to(cod, UP, buff=0.18).add_background_rectangle(color=BG,buff=.08).set_z_index(5)
        kp = tag("kept", 26, BLUE).next_to(mk, UP, buff=0.18).add_background_rectangle(color=BG,buff=.08).set_z_index(5)
        qm = qmarks()
        qt = qtext("Where do the axons go?")
        self.play(FadeIn(h), FadeIn(VGroup(line, prom, cod, mk, name)), FadeIn(bl), FadeIn(nn), Create(ax), run_time=0.9)
        self.at("delete")
        self.play(FadeIn(x1), cod[2].animate.set_color(GREY), FadeIn(dl), run_time=0.7)
        self.at("keep the marker")
        self.play(Indicate(mk[1:], color=TEXT, scale_factor=1.15), FadeIn(kp), run_time=0.7)
        self.at("where do the axons go")
        self.play(FadeIn(qt), FadeIn(qm, lag_ratio=0.3), run_time=0.9)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        h = T("Predict.", 40, GOLD).move_to(P(-5.2, 3.3))
        line, prom, cod, mk, name = locus(2.65)
        cod[2].set_color(GREY)
        x1 = VGroup()
        dl = tag("deleted", 26, RED).next_to(cod, UP, buff=0.18).add_background_rectangle(color=BG,buff=.08).set_z_index(5)
        kp = tag("kept", 26, BLUE).next_to(mk, UP, buff=0.18).add_background_rectangle(color=BG,buff=.08).set_z_index(5)
        self.add(h, line, prom, cod, mk, name, x1, dl, kp, bulb(*PB), pred_neurons(None), pred_seg1(), qmarks(), qtext("Where do the axons go?"))
        self.wait(self.narration_s + 0.4)


# ------------------------------------------------------------------------------------------------
class S12Reveal1(SpokenScene):
    def construct(self):
        self.add(bulb(*PB).shift(UP*.3),pred_neurons(None).shift(UP*.3),pred_seg1().shift(UP*.3),
                 *[VGroup(cup((NX-.91,y+.3),PI,GREY,1.6),
                          Line(P(NX-1.25,y+.63),P(NX-.75,y-.03),color=RED,stroke_width=5)) for y in NYS],
                 tag("Wang, Axel and colleagues, 1998",26,TEXT).move_to(P(0,3.2)),
                 tag("P2 receptor deleted",28,RED).move_to(P(-3.9,1.7)))
        # Irregular schematic routes stay within the convex bulb outline.
        routes = [
            [(.85,.2),(.9,-.1),(2.1,.8),(3.2,.4),(2.7,-.4),(3.9,-.9),(4.6,.2)],
            [(.85,-1.1),(1,-1),(1.8,-1.8),(2.8,-2.3),(3.5,-1.4),(4.7,-1.7),(5.2,-.9)],
            [(.85,-2.2),(1,-2.3),(2,-1.2),(2.6,-1.5),(3.1,-.4),(4.2,-.1),(4.7,.6)]]
        wd=VGroup(*[path(r,BLUE,5) for r in routes])
        wd.shift(UP*.3)
        self.at("wandered")
        self.play(Create(wd),run_time=1)
        self.at("failed to form")
        self.play(FadeIn(T("axons wander, no P2 glomerulus",30,RED).move_to(P(.6,-2.8)).add_background_rectangle(color=BG,buff=.12)),run_time=.5)
        self.at("receptor is needed")
        self.play(FadeIn(T("the receptor is needed",32,BLUE).move_to(P(-2.5,2.45))),run_time=.5)
        self.finish()

# ------------------------------------------------------------------------------------------------
def caveat_frame():
    hd = VGroup(Triangle(color=GOLD, stroke_width=5).scale(0.4), T("!", 30, GOLD, weight=BOLD))
    hd[1].move_to(hd[0].get_center() + DOWN * 0.05)
    ct = T("Caveat", 40, GOLD)
    head = VGroup(hd, ct).arrange(RIGHT, buff=0.3).move_to(P(-4.4, 3.2))
    g1 = bchip("P2 receptor gene", BLUE, 26)
    g2 = bchip("another receptor gene", PINK, 26)
    row = VGroup(g1, g2).arrange(RIGHT, buff=1.0).move_to(P(0.3, 1.7))
    return head, g1, g2, row


class S13Caveat(SpokenScene):
    def construct(self):
        head, g1, g2, row = caveat_frame()
        soma = Circle(1.2, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to(P(1.2, -1.1))
        stem = Line(P(0.0, -1.1), P(-1.2, -1.1), color=BLUE, stroke_width=8)
        c1 = cup((-1.2, -1.1), PI, BLUE, 2.6)
        x1 = VGroup(Line(P(-2.1, -0.5), P(-1.2, -1.7), color=RED, stroke_width=7),
                    Line(P(-2.1, -1.7), P(-1.2, -0.5), color=RED, stroke_width=7))
        c2 = cup((-1.2, -1.1), PI, PINK, 2.6)
        sw = tag("no working receptor", 26, RED).move_to(P(-1.2, -2.75))
        on = arr(P(g2.get_center()[0], 1.25), P(1.9, 0.2), PINK, 6)
        nl = tag("a second receptor", 26, PINK).move_to(P(4.6, 0.6))
        self.play(FadeIn(g1), FadeIn(soma), FadeIn(stem), FadeIn(c1), run_time=0.3)
        self.at("caveat")
        self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.6)
        self.at("without a working")
        self.play(Create(x1), g1[2].animate.set_color(GREY), FadeIn(sw), run_time=0.8)
        self.at("switch on")
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.7)
        self.at("second receptor")
        self.play(GrowArrow(on), FadeOut(c1), FadeOut(x1), FadeIn(c2), FadeIn(nl), soma.animate.set_stroke(PINK).set_fill(PINK, 0.3),
                  stem.animate.set_color(PINK), FadeOut(sw), FadeIn(T("so a deletion is harder to read",32,GOLD).move_to(P(0,-3.2))), run_time=1.0)
        self.finish()


class S14Beat1(NarratedScene):
    def construct(self):
        head, g1, g2, row = caveat_frame()
        g1[2].set_color(GREY)
        soma = Circle(1.2, stroke_color=PINK, stroke_width=5, fill_color=PINK, fill_opacity=0.3).move_to(P(1.2, -1.1))
        stem = Line(P(0.0, -1.1), P(-1.2, -1.1), color=PINK, stroke_width=8)
        c2 = cup((-1.2, -1.1), PI, PINK, 2.6)
        on = arr(P(g2.get_center()[0], 1.25), P(1.9, 0.2), PINK, 6)
        nl = tag("a second receptor", 26, PINK).move_to(P(4.6, 0.6))
        grp = VGroup(head, g1, g2, soma, stem, c2, on, nl, T("so a deletion is harder to read",32,GOLD).move_to(P(0,-3.2)))
        self.add(grp)
        self.wait(self.narration_s + 0.4)


# ------------------------------------------------------------------------------------------------
def pred_bulb_glom():
    p2 = glom(*P2G)
    m12 = glom(*M12G, color=ORANGE)
    p2l = tag("P2 glomerulus", 26, BLUE).move_to(P(3.85, .5))
    m12l = tag("M12 glomerulus", 26, ORANGE).move_to(P(4.65, -3.15))
    return p2, m12, p2l, m12l


class S15Predict2(SpokenScene):
    def construct(self):
        h = T("Predict.", 40, GOLD).move_to(P(-5.2, 3.3))
        line, prom, cod, mk, name = locus(2.65)
        m12c = bchip("M12 receptor", ORANGE).move_to(cod.get_center())
        qt = qtext("Where do the axons go now?")
        bl = bulb(*PB)
        nn = pred_neurons(BLUE)
        ax = pred_seg1()
        p2, m12, p2l, m12l = pred_bulb_glom()
        qm = qmarks()
        qm.remove(*qm[1:])
        q = T("?", 54, GREY).move_to(P(1.15, -1.1))
        self.play(FadeIn(h), FadeIn(VGroup(line, prom, cod, mk, name)), FadeIn(bl), FadeIn(nn), Create(ax),
                  FadeIn(VGroup(p2, m12, p2l, m12l)), run_time=0.9)
        self.at("put the")
        stage = m12c.copy().move_to(P(-2.7, 1.6))
        self.play(FadeIn(stage, shift=UP * 0.1), run_time=0.5)
        self.at("in place of")
        self.play(FadeOut(cod, shift=UP * 0.4), stage.animate.move_to(cod.get_center()),
                  *[n[3].animate.set_color(ORANGE) for n in nn], run_time=0.9)
        self.at("where do the axons go now")
        self.play(FadeIn(q, scale=1.3), FadeIn(qt), run_time=0.6)
        self.finish()


class S16Pause(NarratedScene):
    def construct(self):
        h = T("Predict.", 40, GOLD).move_to(P(-5.2, 3.3))
        line, prom, cod, mk, name = locus(2.65, "M12 receptor", ORANGE)
        p2, m12, p2l, m12l = pred_bulb_glom()
        q = T("?", 54, GREY).move_to(P(1.15, -1.1))
        nn = pred_neurons(ORANGE)
        self.add(h, line, prom, cod, mk, name, bulb(*PB), nn, pred_seg1(), p2, m12, p2l, m12l, q, qtext("Where do the axons go now?"))
        self.wait(self.narration_s + 0.4)


class S17Reveal2(SpokenScene):
    def construct(self):
        h = T("Predict.", 40, GOLD).move_to(P(-5.2, 3.3))
        line, prom, cod, mk, name = locus(2.65, "M12 receptor", ORANGE)
        p2, m12, p2l, m12l = pred_bulb_glom()
        q = T("?", 54, GREY).move_to(P(1.15, -1.1))
        nn = pred_neurons(ORANGE)
        seg2 = pred_seg2()
        qt = qtext("Where do the axons go now?")
        newg = glom(*NEWG)
        nl = T("marked axons’\nglomerulus", 26, BLUE).move_to(P(1.35, -2.65)).add_background_rectangle(color=BG, buff=.08)
        far = DoubleArrow(P(NEWG[0] + 0.75, NEWG[1] - 0.1), P(M12G[0] - 0.85, M12G[1] + 0.1), buff=0, color=TEXT, stroke_width=4,
                          tip_length=0.2)
        fl = tag("far", 28, TEXT).move_to(P(3.3, -1.15))
        self.add(h, line, prom, cod, mk, name, bulb(*PB), nn, pred_seg1(), p2, m12, p2l, m12l, q, qt)
        self.at("converged")
        self.play(FadeOut(q), FadeOut(h), FadeOut(qt), *[Create(a) for a in seg2], run_time=0.9)
        self.at("p2 glomerulus")
        self.play(GrowFromCenter(newg), FadeIn(nl), Create(DashedVMobject(Circle(.95,color=BLUE,stroke_width=2).move_to(P(*P2G)),num_dashes=24)), run_time=1.0)
        self.at("far from m12")
        self.play(GrowArrow(far), FadeIn(fl), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
def helps_frame():
    head = T("the label that guides the axon", 34, GOLD).move_to(P(0, 3.0))
    b1 = RoundedRectangle(corner_radius=0.25, width=5.0, height=2.6, stroke_color=BLUE, stroke_width=4,
                          fill_color=BLUE, fill_opacity=0.25).move_to(P(-3.2, 0.5))
    t1 = T("receptor", 44, BLUE).move_to(b1)
    b2 = RoundedRectangle(corner_radius=0.25, width=5.0, height=2.6, stroke_color=GREY, stroke_width=4,
                          fill_color=GREY, fill_opacity=0.15).move_to(P(3.2, 0.5))
    t2 = T("other features\nof the neuron", 36, GREY, line_spacing=0.9).move_to(b2)
    plus = T("+", 60, TEXT).move_to(P(0, 0.5))
    cap = T("the receptor is part of the label, not all of it", 32, TEXT).move_to(P(0, -1.9))
    return head, VGroup(b1, t1), VGroup(b2, t2), plus, cap


class S18Helps(SpokenScene):
    def construct(self):
        head, a, b, plus, cap = helps_frame()
        self.play(FadeIn(head), run_time=0.4)
        self.at("receptor helps")
        self.play(GrowFromCenter(a), run_time=0.7)
        self.at("other features")
        self.play(FadeIn(plus), FadeIn(b, shift=LEFT * 0.3), run_time=0.8)
        self.at("count too")
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S19Beat2(NarratedScene):
    def construct(self):
        head, a, b, plus, cap = helps_frame()
        grp = VGroup(head, a, b, plus, cap)
        self.add(grp)
        self.wait(self.narration_s + 0.4)


# ------------------------------------------------------------------------------------------------
def pair_lines(cx, color, half=1.1, top=1.1, bot=-1.0, s=1.5):
    """two axon-like lines with a row of cups facing each other; returns (lines, cups_left, cups_right, ys)."""
    lines = VGroup()
    for x in (cx - half, cx + half):
        lines.add(VGroup(Line(P(x, top), P(x, bot), color=color, stroke_width=11),
                         Circle(0.17, stroke_width=0, fill_color=color, fill_opacity=1).move_to(P(x, bot))))
    ys = [0.6, -0.2]
    cl = VGroup(*[cup((cx - half + 0.07, y), 0.0, color, s) for y in ys])
    cr = VGroup(*[cup((cx + half - 0.07, y), PI, color, s) for y in ys])
    return lines, cl, cr, ys


class S20Analogy(SpokenScene):
    def construct(self):
        cx_l, cx_r = -3.4, 3.4
        ln_l, cl_l, cr_l, ys = pair_lines(cx_l, BLUE, half=1.2, top=2.4, bot=-1.8)
        ys = [1.5, 0.3, -.9]
        cl_l = VGroup(*[cup((cx_l - 1.2 + 0.07, y), 0.0, BLUE, 1.7) for y in ys])
        cr_l = VGroup(*[cup((cx_l + 1.2 - 0.07, y), PI, BLUE, 1.7) for y in ys])
        ln_r, _, _, _ = pair_lines(cx_r, YELLOW, half=1.2, top=2.4, bot=-1.8)
        cl_r = VGroup(*[cup((cx_r - 1.2 + 0.07, y), 0.0, YELLOW, 1.7) for y in ys])
        cr_r = VGroup(*[cup((cx_r + 1.2 - 0.07, y), PI, YELLOW, 1.7) for y in ys])
        bonds = VGroup(*[Line(P(cx_r - 1.2 + 0.07 + 0.55, y), P(cx_r + 1.2 - 0.07 - 0.55, y), color=YELLOW, stroke_width=6)
                         for y in ys])
        rl = VGroup(T("receptor",28,BLUE).move_to(P(-4.9,-2.9)), T("receptor",28,BLUE).move_to(P(-1.9,-2.9)))
        sl = T("Sidekick", 34, YELLOW).move_to(P(cx_r, -2.7))
        q = T("?", 64, GREY).move_to(P(cx_l, 0.4))
        nb = tag("no known bond", 28, TEXT).move_to(P(cx_l, -2.15))
        self.add(T("not a match between receptors",34,GOLD).move_to(P(0,3.25)))
        self.add(ln_l,cl_l,cr_l,rl)
        self.at("shared label")
        self.play(FadeIn(ln_l), FadeIn(cl_l), FadeIn(cr_l), FadeIn(rl), run_time=0.9)
        self.at("unlike sidekick")
        self.play(FadeIn(ln_r), FadeIn(cl_r), FadeIn(cr_r), FadeIn(sl), run_time=0.8)
        self.play(Create(bonds), run_time=0.7)
        self.at("not known to bind")
        self.play(FadeIn(q, scale=1.3), FadeIn(nb), run_time=0.8)
        self.at("other axons")
        self.play(Indicate(VGroup(cl_l[1], cr_l[1]), color=TEXT, scale_factor=1.3), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------------
def panel(cx, title, color, dashed=False):
    r = RoundedRectangle(corner_radius=0.25, width=4.0, height=6.0, stroke_color=GREY, stroke_width=3)
    r.move_to(P(cx, -0.4))
    if dashed:
        r = DashedVMobject(r, num_dashes=60)
    t = T(title, 28, color).move_to(P(cx, 2.15))
    return VGroup(r, t)


def mini_pair(cx, color):
    half = 0.9
    lines = VGroup()
    for x in (cx - half, cx + half):
        lines.add(VGroup(Line(P(x, 1.3), P(x, -1.2), color=color, stroke_width=9),
                         Circle(0.15, stroke_width=0, fill_color=color, fill_opacity=1).move_to(P(x, -1.2))))
    ys = [0.7, -0.1, -0.9]
    cl = VGroup(*[cup((cx - half + 0.06, y), 0.0, color, 1.5) for y in ys])
    cr = VGroup(*[cup((cx + half - 0.06, y), PI, color, 1.5) for y in ys])
    return lines, cl, cr, ys, half


class S21Idea(SpokenScene):
    def construct(self):
        cxs = [-4.4, 0.0, 4.4]
        p1 = panel(cxs[0], "Layers", YELLOW)
        p2 = panel(cxs[1], "Self-avoidance", PURPLE)
        p3 = panel(cxs[2], "Smell (analogy)", BLUE, dashed=True)
        L1, c1l, c1r, ys, half = mini_pair(cxs[0], YELLOW)
        L2, c2l, c2r, _, _ = mini_pair(cxs[1], PURPLE)
        L3, c3l, c3r, _, _ = mini_pair(cxs[2], BLUE)
        b1 = VGroup(*[Line(P(cxs[0] - half + 0.06 + 0.45, y), P(cxs[0] + half - 0.06 - 0.45, y), color=YELLOW, stroke_width=5) for y in ys])
        b2 = VGroup(*[Line(P(cxs[1] - half + 0.06 + 0.45, y), P(cxs[1] + half - 0.06 - 0.45, y), color=PURPLE, stroke_width=5) for y in ys])
        same = VGroup(tag("same", 24, TEXT).move_to(P(cxs[0], -1.75)), tag("same", 24, TEXT).move_to(P(cxs[1], -1.75)))
        g_arr = VGroup(arr(P(cxs[0] - 1.7, 1.7), P(cxs[0] - 1.1, 1.7), GREEN, 5), arr(P(cxs[0] + 1.7, 1.7), P(cxs[0] + 1.1, 1.7), GREEN, 5))
        r_arr = VGroup(arr(P(cxs[1] - 1.1, 1.7), P(cxs[1] - 1.7, 1.7), RED, 5), arr(P(cxs[1] + 1.1, 1.7), P(cxs[1] + 1.7, 1.7), RED, 5))
        o1 = tag("stick", 30, TEXT).move_to(P(cxs[0], -2.55))
        o2 = tag("retreat", 30, TEXT).move_to(P(cxs[1], -2.55))
        ban = T("the cell decides what same means", 30, TEXT).move_to(P(0, 3.4))
        q = T("?", 56, GREY).move_to(P(cxs[2], 0.0))
        nm = tag("no known match", 26, TEXT).move_to(P(cxs[2], -1.75))
        o3 = VGroup(T("receptor-dependent", 26, BLUE), T("sorting", 26, BLUE)).arrange(DOWN, buff=0.1).move_to(P(cxs[2], -2.9))
        nm2 = T("still being\nworked out", 26, TEXT, line_spacing=1.0).move_to(P(cxs[2], -1.85))
        self.add(ban,p1,p2,L1,c1l,c1r,o1,o2)
        self.at("layers")
        self.play(FadeIn(p1), FadeIn(L1), FadeIn(c1l), FadeIn(c1r), run_time=0.8)
        self.at("avoidance")
        self.play(FadeIn(p2), FadeIn(L2), FadeIn(c2l), FadeIn(c2r), run_time=0.8)
        self.at("a match says")
        self.play(Create(b1), Create(b2), run_time=0.6)
        self.play(FadeIn(same), Indicate(VGroup(b1, b2), color=TEXT, scale_factor=1.1), run_time=0.8)
        self.at("the cell decides")
        self.play(GrowFromCenter(g_arr), GrowFromCenter(r_arr), Indicate(o1, color=GREEN), Indicate(o2, color=RED), run_time=1.0)
        self.at("smell shares")
        self.play(FadeIn(p3), FadeIn(L3), FadeIn(c3l), FadeIn(c3r), run_time=0.9)
        self.at("no receptor")
        self.play(FadeIn(q, scale=1.3), FadeIn(nm), run_time=0.8)
        self.at("how the receptor sorts")
        self.play(FadeIn(o3, shift=UP * 0.1), Indicate(VGroup(c3l, c3r), color=TEXT, scale_factor=1.3), run_time=0.9)
        self.at("worked out")
        self.play(ReplacementTransform(nm, nm2), Indicate(q, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S22Take(SpokenScene):
    def construct(self):
        head = T("Takeaway", 38, GOLD).move_to(P(-5.0, 3.3))
        bl = Ellipse(width=4.8, height=5.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.08).move_to(P(3.6, .7))
        ys = [2.25, .9, -.45, -1.8]
        nn = VGroup(*[neu(-3.9, y, GREY, 1.7) for y in ys])
        gl = glom(3.0, 1.0, BLUE, 0.65)
        axs = VGroup(*[path([(-3.44, y), (-2.5, 1.0 + (y - 1.0) * 0.5), (0.0, 1.0 + (y - 1.0) * 0.2), (1.6, 1.0 + (y - 1.0) * 0.06),
                             (2.6, 1.0 + (y - 1.0) * 0.05)], BLUE, 5) for y in ys])
        ch = tag("one channel", 28, BLUE).move_to(P(-0.2, 2.9))
        l1 = T("receptor identity helps axons of one channel converge", 28, TEXT).move_to(P(0, -2.6))
        of = VGroup(*[DashedVMobject(Circle(0.58, color=GREY, stroke_width=3).move_to(P(-3.9, y)), num_dashes=16) for y in ys])
        l2 = T("other features of the neuron count too", 28, TEXT).move_to(P(0, -3.12))
        ft = tag("Activity refines these maps later.", 26, TEXT).move_to(P(0, -3.65))
        self.play(FadeIn(head), FadeIn(nn), FadeIn(bl), run_time=0.6)
        self.at("in smell")
        self.play(*[n[1].animate.set_stroke(BLUE).set_fill(BLUE, 0.35) for n in nn],
                  *[n[2].animate.set_color(BLUE) for n in nn], *[n[3].animate.set_color(BLUE) for n in nn], run_time=0.7)
        self.at("receptor identity")
        self.play(*[Indicate(n[3], color=TEXT, scale_factor=1.6) for n in nn], run_time=0.9)
        self.at("axons of one channel")
        self.play(*[Create(a) for a in axs], run_time=1.4)
        self.play(GrowFromCenter(gl), FadeIn(ch), FadeIn(l1, shift=UP * 0.1), run_time=0.7)
        self.at("other features")
        self.play(FadeIn(of), FadeIn(l2), FadeIn(ft), run_time=0.6)
        self.finish()


class S23End(EndCard):
    LINE = "Receptor identity helps axons of one channel converge."

    def construct(self):
        line = Paragraph("Receptor identity helps axons", "of one channel converge.", alignment="center",
                         font_size=40, font=TITLE_FONT, color=TEXT, line_spacing=1.3).move_to(P(0,.4))
        sub = T("biochemistrypedia.com",26,TEAL).move_to(P(0,-1.7))
        self.play(FadeIn(line),run_time=.7)
        self.play(FadeIn(sub),run_time=.3)
        self.finish()