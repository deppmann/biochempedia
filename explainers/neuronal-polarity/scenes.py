"""Neuronal polarity: an axon is a state, not a stamp  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the axon (and the leading neurite that becomes it)
  BLUE   = dendrites and the dendrite protein MAP2
  GREY   = cell body, neurites that have not been chosen, outlines, bar baseline
  GREEN  = PIP3 and positive feedback
  RED    = negative feedback, a blocked step, the cut, loss of ankyrin G
  ORANGE = actin
  TEAL   = microtubules
  PURPLE = ankyrin G and the axon initial segment
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SOMA_FILL = "#262b36"

C0 = np.array([-4.3, 0.45, 0.0])     # cell body centre, same in every scene that shows the whole cell
SOMA_R = 0.72
BASE_Y = -3.3                      # baseline of the length chart
BAR_X0 = 2.3


def u(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


class Neuron:
    """Cell body plus neurites whose lengths are ValueTrackers. Lines redraw from the trackers."""

    def __init__(self, specs, center=C0, soma_r=SOMA_R):
        self.c = np.array(center, float)
        self.lines, self.tips, self.tr = [], [], []
        self.dirs = []
        grp = VGroup()
        for deg, L, col, w in specs:
            d = u(deg)
            tr = ValueTracker(L)
            ln = Line(self.c, self.c + d * L, color=col, stroke_width=w)
            ln.add_updater(lambda m, d=d, tr=tr: m.put_start_and_end_on(
                self.c + d * 0.02, self.c + d * max(tr.get_value(), 0.05)))
            tip = Dot(self.c + d * L, radius=0.075 + 0.012 * w, color=col)
            tip.add_updater(lambda m, d=d, tr=tr: m.move_to(self.c + d * max(tr.get_value(), 0.05)))
            self.lines.append(ln); self.tips.append(tip); self.tr.append(tr); self.dirs.append(d)
            grp.add(ln, tip)
        self.soma = Circle(radius=soma_r, stroke_color=GREY, stroke_width=4,
                           fill_color=SOMA_FILL, fill_opacity=1).move_to(self.c)
        self.group = VGroup(grp, self.soma)

    def recolor(self, i, col):
        return [self.lines[i].animate.set_color(col), self.tips[i].animate.set_color(col)]

    def point(self, i, L):
        return self.c + self.dirs[i] * L


DEND = [20, 110, 200, 290]
DLEN = (2.4, 2.1, 2.3, 2.2)


def mature(ax_len=10.3, dend_len=DLEN):
    specs = [(0, ax_len, YELLOW, 11)]
    for deg, L in zip(DEND, dend_len):
        specs.append((deg, L, BLUE, 8))
    return Neuron(specs)


def young(lengths=(2.3, 2.3, 2.3, 2.3, 2.3)):
    specs = [(0, lengths[0], GREY, 10)]
    for deg, L in zip(DEND, lengths[1:]):
        specs.append((deg, L, GREY, 10))
    return Neuron(specs)


class Chart:
    """Bars for neurite length, driven by the same trackers as the neuron."""

    def __init__(self, neuron, cols, s=0.55, order=None, x0=BAR_X0, dx=0.9):
        self.s = s
        self.bars = VGroup()
        self.n = neuron
        order = order or list(range(len(neuron.tr)))
        for k, i in enumerate(order):
            x = x0 + k * dx
            tr = neuron.tr[i]
            bar = Line([x, BASE_Y, 0], [x, BASE_Y + 0.1, 0], color=cols[i], stroke_width=26)
            bar.add_updater(lambda m, x=x, tr=tr: m.put_start_and_end_on(
                [x, BASE_Y, 0], [x, BASE_Y + max(tr.get_value() * s, 0.06), 0]))
            self.bars.add(bar)
        self.base = Line([x0 - 0.45, BASE_Y - 0.12, 0], [x0 + (len(order) - 1) * dx + 0.45, BASE_Y - 0.12, 0],
                         color=GREY, stroke_width=3)
        self.title = T("neurite length", 24, GREY).next_to(self.base, DOWN, buff=0.12)
        self.group = VGroup(self.bars, self.base, self.title)


def cutmark(p, color=RED, h=0.55):
    return DashedLine(p + UP * h, p + DOWN * h, color=color, stroke_width=5, dash_length=0.12)


def hdr(text, color=TEXT, size=30):
    return T(text, size, color, font=TITLE_FONT).to_edge(UP, buff=0.35)


class S00Title(TitleCard):
    LESSON = "Neuronal polarity"
    TITLE = "One Axon, Many Dendrites"


def cone(cx, cy, col, n_actin, mt_end, seed, sc=1.32):
    """schematic growth cone: shaft, fan, actin lines (orange), microtubules (teal)."""
    rng = np.random.RandomState(seed)
    W, H = 3.4 * sc, 2.6 * sc
    fan = Ellipse(width=W, height=H, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.08
                  ).move_to([cx, cy, 0])
    x_neck = cx - W / 2 + 0.05
    shaft_x0 = x_neck - 1.35
    shaft = VGroup(Line([shaft_x0, cy + 0.3, 0], [x_neck, cy + 0.42, 0], color=col, stroke_width=5),
                   Line([shaft_x0, cy - 0.3, 0], [x_neck, cy - 0.42, 0], color=col, stroke_width=5))
    actin = VGroup()
    for _ in range(n_actin):
        while True:
            x, y = rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2)
            if (x / (W / 2 * 0.93)) ** 2 + (y / (H / 2 * 0.9)) ** 2 < 0.85 and x > -W / 2 + 0.45:
                break
        a = rng.uniform(0, PI)
        c = np.array([cx + x, cy + y, 0]); dv = np.array([np.cos(a), np.sin(a), 0]) * 0.2 * sc
        actin.add(Line(c - dv, c + dv, color=ORANGE, stroke_width=4))
    mts = VGroup()
    for k, yo in enumerate((-0.2, 0.0, 0.2)):
        mts.add(Line([shaft_x0, cy + yo, 0], [mt_end - 0.2 * k, cy + yo, 0], color=TEAL, stroke_width=7))
    return dict(fan=fan, shaft=shaft, actin=actin, mts=mts, x_neck=x_neck, shaft_x0=shaft_x0, cx=cx, cy=cy)



def branches(n, color=BLUE):
    g = VGroup()
    for i in range(1, 5):
        d = n.dirs[i]; perp = np.array([-d[1], d[0], 0])
        end = n.tr[i].get_value()
        for side in (-1, 1):
            p = n.point(i, end * .65)
            g.add(Line(p, p + d * .6 + perp * .45 * side, color=color, stroke_width=4),
                  Line(n.point(i, end * .83), n.point(i, end) + d * .3, color=color, stroke_width=3))
    return g


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=.35)


class S01Domains(SpokenScene):
    def construct(self):
        n = mature(); b = branches(n)
        self.at('A neuron')
        self.play(FadeIn(n.group), Create(b), run_time=.6)
        dl = T('dendritic input', 26, BLUE).move_to([-3.9, -2.55, 0])
        al = T('axonal output', 26, YELLOW).move_to([3.1, -.4, 0])
        incoming = Arrow([-3.2, 2.4, 0], [-3.8, 1.5, 0], color=BLUE, buff=.1)
        self.at('takes in signals')
        self.play(FadeIn(dl), GrowArrow(incoming), run_time=.6)
        self.at('sends its output')
        pulse = Dot(n.point(0, 1), color=YELLOW, radius=.16)
        self.play(FadeIn(al), FadeIn(pulse), run_time=.3)
        self.play(pulse.animate.move_to(n.point(0, 10)), run_time=1.0)
        self.at('These branches differ')
        self.play(FadeOut(incoming), FadeOut(pulse), run_time=.3)
        self.at('That difference')
        head = hdr('Neuronal polarity')
        self.play(FadeIn(head), run_time=.5)
        self.at('Dendrites carry receptors')
        clear(self)
        dend = Line([-5.8, 1, 0], [-.8, 1, 0], color=BLUE, stroke_width=13)
        ax = Line([.8, 1, 0], [5.8, 1, 0], color=YELLOW, stroke_width=13)
        rec = VGroup(*[VGroup(Line([x-.13,1.05,0],[x-.13,1.5,0],color=BLUE),
                             Line([x+.13,1.05,0],[x+.13,1.5,0],color=BLUE),
                             Line([x-.13,1.05,0],[x+.13,1.05,0],color=BLUE)) for x in (-4.8,-3.3,-1.8)])
        rlab=T('neurotransmitter receptors',24,BLUE).move_to([-3.3,2.25,0])
        self.play(Create(dend),Create(rec),FadeIn(rlab),run_time=.7)
        self.at('The axon has')
        ch=chip('channels',YELLOW,24).move_to([2,2.25,0])
        ves=chip('vesicle machinery',YELLOW,24).move_to([4.5,-.1,0])
        self.play(Create(ax),FadeIn(ch),FadeIn(ves),run_time=.6)
        self.at('send proteins')
        cargos=VGroup(Dot([-6,.45,0],color=BLUE,radius=.14),Dot([0,.45,0],color=YELLOW,radius=.14))
        self.add(cargos)
        self.play(cargos[0].animate.move_to([-3.3,.45,0]),cargos[1].animate.move_to([3.3,.45,0]),run_time=1)
        self.at('How does it choose')
        q=T('Choose an axon • maintain distinct domains',30,GOLD).move_to([0,-2.15,0])
        self.play(FadeIn(q),run_time=.5)
        self.at('Start with a young')
        clear(self)
        y=young(); dish=Ellipse(width=6.2,height=5.8,color=GREY).move_to(C0)
        # The dish is centered on the cell but clipped neither at the left nor right.
        dish.stretch_to_fit_width(4.7)
        self.play(FadeIn(y.group),Create(dish),FadeIn(hdr('Young rat neuron • culture dish',GREY,28)),run_time=.7)
        self.finish()


class S02Race(SpokenScene):
    def construct(self):
        n=young((.8,)*5); ch=Chart(n,[GREY]*5)
        self.at('A rat hippocampal neuron')
        self.play(FadeIn(hdr('Cultured rat hippocampal neuron',GREY,28)),FadeIn(n.group),run_time=.5)
        self.at('grows several short neurites')
        self.play(*[t.animate.set_value(2.3) for t in n.tr],FadeIn(ch.group),run_time=1)
        self.at('After a day')
        self.play(FadeIn(T('a day or two',26,GREY).move_to([3.7,1.8,0])),run_time=.4)
        self.at('one grows much faster')
        self.play(n.tr[0].animate.set_value(5),run_time=1.2,rate_func=rate_functions.ease_in_sine)
        self.at('It becomes the axon')
        self.play(*n.recolor(0,YELLOW),ch.bars[0].animate.set_color(YELLOW),run_time=.5)
        self.at('The others grow as dendrites')
        self.play(*[a for i in range(1,5) for a in n.recolor(i,BLUE)],
                  *[ch.bars[i].animate.set_color(BLUE) for i in range(1,5)],Create(branches(n)),run_time=.8)
        self.at('The choice behaves')
        self.play(FadeIn(T('a race',44,GOLD,font=TITLE_FONT).move_to([3.7,.6,0])),run_time=.5)
        self.finish()


class S03Feedback(SpokenScene):
    def construct(self):
        n=young((5,2.3,2.3,2.3,2.3)); n.lines[0].set_color(YELLOW); n.tips[0].set_color(YELLOW)
        self.add(n.group)
        grows=chip('grows',YELLOW,26).move_to([1.7,2.15,0]); faster=chip('grows faster',YELLOW,26).move_to([4.7,2.15,0])
        loop=VGroup(CurvedArrow(grows.get_top(),faster.get_top(),angle=-PI/2,color=GREEN),
                    CurvedArrow(faster.get_bottom(),grows.get_bottom(),angle=-PI/2,color=GREEN))
        self.at('Positive feedback')
        self.play(FadeIn(grows),FadeIn(faster),Create(loop),run_time=.8)
        self.at('the more it grows')
        self.play(Indicate(loop,color=GREEN),run_time=.6)
        dots=VGroup(*[Dot(n.point(0,5)+np.array(p),radius=.08,color=GREEN) for p in [(-.4,.3,0),(-.2,-.3,0),(.2,.3,0),(.3,-.2,0)]])
        pip=T('PIP3',28,GREEN).move_to([1.1,-.5,0])
        self.at('A lipid called')
        self.play(FadeIn(dots),FadeIn(pip),run_time=.6)
        self.at('Blocking')
        k=chip('PI3-kinase',GREEN,26).move_to([3.7,-1,0]); cross=Cross(k,stroke_color=RED)
        self.play(FadeIn(k),Create(cross),run_time=.6)
        self.at('is reported to stop')
        # Reset to an unpolarized culture: blocking formation is not axon removal.
        reset=young()
        self.play(FadeOut(n.group),FadeOut(dots),FadeOut(pip),FadeIn(reset.group),
                  FadeIn(T('culture: no axon forms',26,RED).move_to([3.7,-2.1,0])),run_time=.7)
        self.at('Negative feedback')
        clear(self)
        self.add(n.group)
        bars=VGroup()
        for i in range(1,5):
            p=n.point(i,1.2); d=n.dirs[i]; v=np.array([-d[1],d[0],0])*.3
            bars.add(Line(p-v,p+v,color=RED,stroke_width=7))
        self.play(Create(bars),FadeIn(T('holds siblings back',30,RED).move_to([3.5,1.2,0])),run_time=.7)
        self.at('How it does that')
        self.play(FadeIn(T('mechanism less settled ?',30,GOLD).move_to([3.3,-.1,0])),run_time=.5)
        self.finish()


class S04Tip(SpokenScene):
    def construct(self):
        a=cone(-2.6,.4,YELLOW,18,-2.1,3,sc=1.05); b=cone(3.8,.4,GREY,60,1.8,5,sc=1.05)
        for k,m in enumerate(b['mts']):
            m.put_start_and_end_on(m.get_start(),[b['x_neck']+.2-.15*k,m.get_start()[1],0])
        outlines=VGroup(a['fan'],a['shaft'],b['fan'],b['shaft'])
        labels=VGroup(T('future axon',28,YELLOW).move_to([-2.6,2.5,0]),T('sibling',28,GREY).move_to([3.8,2.5,0]))
        self.at('At the growing tip')
        self.play(FadeIn(outlines),FadeIn(labels),run_time=.6)
        self.at('actin is looser')
        self.play(FadeIn(a['actin']),FadeIn(b['actin']),FadeIn(T('orange: actin',26,ORANGE).move_to([-3.1,-1.9,0])),run_time=.6)
        self.at('microtubules are more stable')
        self.play(Create(a['mts']),Create(b['mts']),FadeIn(T('teal: microtubules',26,TEAL).move_to([3,-1.9,0])),run_time=.7)
        self.at('Locally loosen actin')
        clear(self)
        # Two independent culture examples, rather than sequential treatments of one tip.
        left=Neuron([(0,2,GREY,9),(120,1.2,GREY,7),(240,1.2,GREY,7)],center=[-4.8,-.5,0],soma_r=.45)
        right=Neuron([(0,2,GREY,9),(120,1.2,GREY,7),(240,1.2,GREY,7)],center=[1.8,-.5,0],soma_r=.45)
        self.play(FadeIn(left.group),FadeIn(T('loosen actin locally',26,ORANGE).move_to([-3.5,2,0])),
                  FadeIn(Circle(radius=.35,color=ORANGE).move_to(left.point(0,2))),run_time=.6)
        self.at('or stabilize microtubules')
        self.play(FadeIn(right.group),FadeIn(T('stabilize microtubules',26,TEAL).move_to([3.2,2,0])),
                  FadeIn(Line(right.point(0,.6),right.point(0,2),color=TEAL,stroke_width=4).shift(DOWN*.2)),run_time=.7)
        self.at('can become the axon')
        self.play(left.tr[0].animate.set_value(3.2),right.tr[0].animate.set_value(3.2),
                  *left.recolor(0,YELLOW),*right.recolor(0,YELLOW),
                  FadeIn(T('can favor an axon',30,YELLOW).move_to([0,-2.5,0])),run_time=.9)
        self.at('The cytoskeleton')
        self.play(FadeIn(hdr('The cytoskeleton can tip the choice',GOLD,30)),run_time=.5)
        self.finish()


class S04bTracks(SpokenScene):
    def construct(self):
        self.at('Those microtubules')
        self.play(FadeIn(hdr('Tracks guide cargo',TEXT,32)),run_time=.5)
        def tracks(y, mixed=False):
            g=VGroup()
            for j in range(2):
                yy=y-j*.8; rev=mixed and j==1
                g.add(Line([-3.7,yy,0],[5.4,yy,0],color=TEAL,stroke_width=6),
                      T('+' if rev else '−',48,YELLOW if rev else BLUE,weight=BOLD).move_to([-4.05,yy,0]),
                      T('−' if rev else '+',48,BLUE if rev else YELLOW,weight=BOLD).move_to([5.75,yy,0]))
            return g
        ax=tracks(1.8); de=tracks(-1.1,True)
        self.at('In the axon')
        self.play(Create(ax),FadeIn(T('axon • nearly all + end out',26,YELLOW).move_to([1,2.7,0])),
                  FadeIn(T('cell-body\nend',40,GREY).move_to([-5.5,1.4,0])),run_time=.7)
        self.at('In vertebrate dendrites')
        self.play(Create(de),FadeIn(T('vertebrate dendrite • mixed',26,BLUE).move_to([1,-.35,0])),
                  FadeIn(T('cell-body\nend',40,GREY).move_to([-5.5,-1.5,0])),run_time=.7)
        self.at('A kinesin that prefers stable')
        motor=VGroup(Dot([-3,1.8,0],radius=.13,color=TEXT),Square(side_length=.25,color=YELLOW,fill_opacity=1).move_to([-3,2.15,0]))
        kl=T('kinesin → + end',28,YELLOW).move_to([.4,.45,0])
        self.play(FadeIn(motor),FadeIn(kl),run_time=.5)
        self.at('can steer cargo')
        self.play(motor.animate.shift(RIGHT*7.6),run_time=1.3)
        self.at('can carry cargo outward')
        dm=VGroup(Dot([-3,-1.9,0],radius=.13,color=TEXT),Square(side_length=.25,color=BLUE,fill_opacity=1).move_to([-3,-1.55,0]))
        dlab=T('dynein → − end',28,BLUE).move_to([.4,-2.65,0])
        self.play(FadeIn(dm),FadeIn(dlab),run_time=.4)
        self.play(dm.animate.shift(RIGHT*7.6),run_time=2)
        self.at('Different tracks help')
        self.play(FadeIn(T('Tracks help maintain distinct domains',26,GOLD).move_to([0,-3.4,0])),run_time=.6)
        self.finish()


class S05Hold(SpokenScene):
    def construct(self):
        n=mature(); self.add(n.group,branches(n))
        ais=Line(n.point(0,.95),n.point(0,2.95),color=PURPLE,stroke_width=26)
        ank=chip('ankyrin G',PURPLE,28).move_to([-.8,-2.4,0])
        lab=T('axon initial segment',28,PURPLE).move_to([.7,1.5,0])
        leader=Line(n.point(0,2.7)+UP*.2,lab.get_corner(DL)+DOWN*.12,
                    color=PURPLE,stroke_width=3)
        self.at('Near the cell body')
        self.play(FadeIn(ank),Create(ais),FadeIn(lab),Create(leader),run_time=.8)
        self.at('In many neurons')
        qualifier=hdr('Action potentials start here • in many neurons',TEXT,28)
        self.play(FadeIn(qualifier),run_time=.5)
        self.at('action potentials start here')
        p=Dot(n.point(0,1.7),radius=.22,color=TEXT)
        self.play(FadeIn(p),run_time=.25)
        self.play(p.animate.move_to(n.point(0,9.8)),run_time=1)
        self.play(FadeOut(p),run_time=.2)
        self.at('It also helps hold polarity')
        self.play(Indicate(ais,color=PURPLE),run_time=.6)
        self.at('Lower')
        culture=hdr('Culture • initial segment already formed',GREY,28)
        self.play(ReplacementTransform(qualifier,culture),Create(Cross(ank,stroke_color=RED)),run_time=.7)
        self.at('it falls apart')
        self.play(FadeOut(ais),FadeOut(lab),FadeOut(leader),run_time=.7)
        self.at('The dendrite protein')
        maplab=chip('MAP2',BLUE,26).move_to([-5.5,-2.4,0])
        dots=VGroup(*[Dot(n.point(0,.85+k*.32),radius=.08,color=BLUE) for k in range(7)])
        self.play(FadeIn(maplab),run_time=.5)
        self.at('enters the axon')
        moving=dots.copy().shift(LEFT*1.1)
        self.add(moving)
        self.play(Transform(moving,dots),run_time=.9)
        self.at('The near end gains')
        proximal=Line(n.point(0,SOMA_R),n.point(0,2.95),color=BLUE,stroke_width=13)
        spines=VGroup(*[Line(n.point(0,.9+k*.4),n.point(0,.9+k*.4)+UP*.35*(-1)**k,color=BLUE,stroke_width=4) for k in range(5)])
        self.play(Create(proximal),Create(spines),run_time=.7)
        self.at('while farther out')
        distal=VGroup(*[Dot(n.point(0,5+k*.8),radius=.09,color=YELLOW) for k in range(6)])
        self.play(FadeIn(distal),FadeIn(T('distal axonal proteins remain',24,YELLOW).move_to([3.7,-.8,0])),run_time=.7)
        self.at('Identity needs active maintenance')
        self.play(FadeOut(culture),FadeIn(hdr('Identity needs active maintenance',GOLD,32)),run_time=.6)
        self.finish()


def migrant(center=(0,0,0),axon=True):
    c=np.array(center,float)
    return VGroup(Line(c,c+UP*1.5,color=GREY,stroke_width=7),
                  Line(c,c+DOWN*2,color=YELLOW if axon else GREY,stroke_width=7),
                  Circle(radius=.42,color=GREY,fill_color=SOMA_FILL,fill_opacity=1).move_to(c))


class S06Tissue(SpokenScene):
    def construct(self):
        cell=migrant(axon=False)
        env=VGroup(*[Arrow([x,-2.5,0],[x,2.5,0],color=GREY,buff=.2,stroke_width=2) for x in (-3,3)])
        self.at('In tissue')
        self.play(FadeIn(cell),FadeIn(env),FadeIn(hdr('Environmental cues orient polarity',TEXT,30)),run_time=.7)
        self.at('Many cortical neurons')
        self.play(cell.animate.shift(UP*.65),FadeIn(T('migration ↑',26,GREY).move_to([4.6,1.1,0])),run_time=1.2)
        self.at('from the trailing process')
        self.play(cell[1].animate.set_color(YELLOW),FadeIn(T('trailing axon',28,YELLOW).move_to([3,-1.5,0])),run_time=.7)
        self.at('Cortical neurons lacking')
        clear(self)
        def chain(cx):
            lk=chip('LKB1',GREY,24).move_to([cx-1.85,2,0])
            sad=chip('SAD-A / SAD-B',GREY,24).move_to([cx+1.25,2,0])
            activation=Arrow(lk.get_right(),sad.get_left(),color=TEXT,buff=.12)
            act=T('activates',22,TEXT).move_to([cx-.6,2.65,0])
            return lk,sad,activation,act
        left_lk,left_sad,left_arrow,left_act=chain(-3.5)
        right_lk,right_sad,right_arrow,right_act=chain(3.5)
        left_sad.set_opacity(.35)
        self.play(*[FadeIn(m) for m in (left_lk,left_sad,left_act,right_lk,right_sad,right_act)],
                  GrowArrow(left_arrow),GrowArrow(right_arrow),run_time=.5)
        a=migrant((-4,-.8,0),False); b=migrant((3,-.8,0),False)
        self.at('LKB1')
        la=T('no LKB1',26,RED).move_to([-4,.9,0])
        self.play(FadeIn(a),FadeIn(la),Create(Cross(left_lk,stroke_color=RED)),run_time=.5)
        self.at('or both')
        lb=T('no SAD-A and no SAD-B',24,RED).move_to([3,.9,0])
        self.play(FadeIn(b),FadeIn(lb),Create(Cross(right_sad,stroke_color=RED)),run_time=.5)
        self.at('fail to form axons')
        self.play(a[1].animate.set_opacity(.15),b[1].animate.set_opacity(.15),
                  FadeIn(T('axon fails to form',26,RED).move_to([-4,-3.25,0])),
                  FadeIn(T('axon fails to form',26,RED).move_to([3,-3.25,0])),run_time=.6)
        self.at('The dish reveals mechanisms')
        clear(self)
        dish=Ellipse(width=5.2,height=4.5,color=GREY).move_to([-3.5,0,0])
        youngcell=Neuron([(d,1.3,GREY,7) for d in (0,72,144,216,288)],center=[-3.5,0,0],soma_r=.4)
        self.play(Create(dish),FadeIn(youngcell.group),FadeIn(T('dish: equal neurites',26,GREY).move_to([-3.5,-2.8,0])),run_time=.6)
        self.at('The developing brain')
        tissue=migrant((3.3,0,0)); arrow=Arrow([5,0,0],[5,2,0],color=GREY)
        self.play(FadeIn(tissue),GrowArrow(arrow),FadeIn(T('tissue: migrating neuron',26,TEXT).move_to([3.3,-2.8,0])),run_time=.7)
        self.at('a different starting point')
        self.play(FadeIn(hdr('Different starting points',GOLD,32)),run_time=.5)
        self.finish()


class S07End(EndCard):
    LINE = "In cultured neurons, one neurite wins a race to become the axon."
