"""Chapter 3: One Dial.
COLOR MAP (inherited unchanged from scenes.old.py / shared chapter reference):
GREY = uncommitted ectoderm, structure and labels; ORANGE = epidermis / skin;
BLUE = neural; YELLOW = BMP / BMP4; GREEN = BMP catchers;
PURPLE = organizer / dorsal mesoderm; PINK = BMP receptor; RED = jammed receptor.
Smad1, MAPK, FGF and the dial use neutral TEXT/GREY (no new fate colors).
Only quantitative curve: s14 uses the steady free-diffusion sphere solution
C(r)/C(a)=a/r, with a=20 micrometres, from the lesson's free-diffusion
assumptions (Going deeper: illustrative isolated-cell radii 15–25 micrometres).
Dial positions are categorical illustrations, not numerical measurements.
"""
import re
import numpy as np
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58AC0'
SECONDARY = '#C4CAD5'

# The reference film's cell and receptor cartoons, enlarged for this chapter.
def cell(p, r=0.42, color=GREY):
    return Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.28).move_to([*p[:2], 0])

def tick(p, w=0.5, color=PINK):
    return RoundedRectangle(corner_radius=0.05, width=w, height=0.16,
                            stroke_width=0, fill_color=color, fill_opacity=1).move_to([*p[:2], 0])

def dot(p, r=0.09, color=YELLOW):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([*p[:2], 0])

def label(s, x, y, size=28, color=TEXT):
    if '\n' in s:
        # Every line is its own centred text, so two-line labels are truly centred.
        return VGroup(*[T(l, size=size, color=color) for l in s.split('\n')]
                      ).arrange(DOWN, buff=.16).move_to([x, y, 0])
    return T(s, size=size, color=color).move_to([x, y, 0])

def bt(s, size, color, x, yb):
    """Text whose baseline (not bounding box) sits at y=yb, so rows and headers line up."""
    t = T(s, size=size, color=color)
    ref = T(re.sub('[gjpqy,]', 'x', s), size=size, color=color)
    desc = t.height - ref.height
    t.move_to([x, 0, 0])
    t.shift(UP * (yb - desc - t.get_bottom()[1]))
    return t

def heading(s):
    return label(s, 0, 3.12, 32)

# Four rows remain in exactly the same positions through the table sequence.
XS = [-4.5, -1.45, 1.5, 4.65]
YS = [1.45, 0.25, -0.95, -2.15]
DATA = [
    ['intact cap', 'working', 'high', 'epidermis'],
    ['dominant-negative\nreceptor', 'jammed', 'low', 'neural'],
    ['separated cells', 'still signaling', '?', 'neural'],
    ['separated cells\n+ BMP4', 'working', 'high enough', 'epidermis'],
]

def entry(row, col, value=None):
    s = DATA[row][col] if value is None else value
    color = TEXT
    if col == 1: color = RED if s == 'jammed' else PINK if s in ('working', 'still signaling') else SECONDARY
    if col == 3: color = BLUE if s == 'neural' else ORANGE
    lines = s.split('\n')
    pitch = .48
    top = YS[row] - .13 + (len(lines) - 1) * pitch / 2
    return VGroup(*[bt(l, 26, color, XS[col], top - i * pitch) for i, l in enumerate(lines)])

def table(n=4, note=False):
    grid = VGroup(*[Line([-6.15, y, 0], [6.15, y, 0], color=GREY, stroke_opacity=.4)
                    for y in [2.1, .85, -.35, -1.55, -2.78]])
    heads = VGroup(*[bt(s, 26, SECONDARY, x, 2.42) for x, s in zip(XS, ['condition', 'receptors', 'Smad1 output', 'fate'])])
    rows = VGroup(*[VGroup(*[entry(r, c) for c in range(4)]) for r in range(n)])
    g = VGroup(grid, heads, rows)
    if note:
        g.add(output_note())
    return g

def row_light(r):
    return RoundedRectangle(width=12.4, height=1.12, corner_radius=.12,
                            stroke_color=TEXT, fill_opacity=.04, fill_color=TEXT).move_to([0, YS[r], 0])

def output_note():
    return label("Smad1 output: model's reading; not measured in every row", 0, -3.25, 26, SECONDARY)

# Categorical dial; these angles are illustrative states, never measured traces.
# Each hand has its own colour in every dial scene: outside = yellow (BMP), membrane = pink
# (receptor), inside = teal (MAPK). Each arm is a sleeve, cuff, palm and three fingers on the rim.
HAND_COL = [YELLOW, PINK, TEAL]
HAND_REST = .4
HAND_LIT = .95

def make_arm(col, sleeve_end=4.95):
    def part(m, w=3):
        m.set_stroke(color=col, width=w)
        m.set_fill(color=col, opacity=HAND_REST)
        return m
    sleeve = part(Polygon([sleeve_end, .24, 0], [3.55, .15, 0], [3.55, -.35, 0], [sleeve_end, -.44, 0]))
    cuff = part(RoundedRectangle(width=.2, height=.64, corner_radius=.06).move_to([3.5, -.1, 0]))
    palm = part(RoundedRectangle(width=.62, height=.72, corner_radius=.18).move_to([3.1, -.1, 0]))
    fingers = [part(RoundedRectangle(width=.66, height=.15, corner_radius=.07).move_to([x, y, 0]), 2)
               for x, y in [(2.74, .17), (2.64, -.1), (2.74, -.37)]]
    return VGroup(sleeve, cuff, palm, *fingers)

def dial(high=None, hands=True):
    c = np.array([0., -.1, 0.])
    face = Circle(radius=2.4, color=SECONDARY, stroke_width=4).move_to(c)
    ticks = VGroup(*[Line(c + 2.12*np.array([np.cos(a), np.sin(a), 0]),
                         c + 2.3*np.array([np.cos(a), np.sin(a), 0]), color=SECONDARY)
                     for a in np.linspace(.3, PI-.3, 9)])
    a = PI/2 if high is None else .45 if high is True else PI-.45 if high is False else float(high)
    needle = Arrow(c, c+1.83*np.array([np.cos(a), np.sin(a), 0]), buff=0,
                   color=TEXT, stroke_width=7, max_tip_length_to_length_ratio=.17)
    names = VGroup(label('Smad1', 0, -.8, 38), label('in the nucleus', 0, -1.4, 28, SECONDARY),
                   label('low · neural', -4.35, 1.8, 28, BLUE),
                   label('high · skin', 4.35, 1.8, 28, ORANGE))
    grips = VGroup()
    if hands:
        for i, (angle, name, x, y) in enumerate([(PI, 'outside the cell', -4.5, -.95),
                                                  (-PI/2, 'at the membrane', 2.45, -3.2),
                                                  (0, 'inside the cell', 4.5, -.95)]):
            col = HAND_COL[i]
            arm = make_arm(col, 3.7 if angle == -PI/2 else 4.95)
            arm.rotate(angle, about_point=c)
            grips.add(VGroup(arm, label(name, x, y, 28, col)))
    g = VGroup(face, ticks, needle, dot(c, .13, TEXT), names, grips)
    g.needle, g.grips, g.center_point = needle, grips, c
    return g

def light(d, i, on=True):
    """Animation that lights (or dims) one hand."""
    return d.grips[i][0].animate.set_fill(opacity=HAND_LIT if on else HAND_REST).set_stroke(width=5 if on else 3)

def turn(scene, d, high, duration=.7):
    a = PI/2 if high is None else .45 if high is True else PI-.45 if high is False else float(high)
    c = d.center_point
    target = Arrow(c, c+1.83*np.array([np.cos(a), np.sin(a), 0]), buff=0,
                   color=TEXT, stroke_width=7, max_tip_length_to_length_ratio=.17)
    scene.play(Transform(d.needle,target),run_time=duration)

def hand_turn(scene, d, i, angle, keep=False):
    scene.play(light(d, i), run_time=.2)
    # A small wrist rotation makes the hand, as well as the needle, act.
    scene.play(Rotate(d.grips[i][0], angle=.09, about_point=d.center_point), run_time=.12)
    turn(scene, d, angle, .35)
    scene.play(Rotate(d.grips[i][0], angle=-.09, about_point=d.center_point), run_time=.1)
    if not keep:
        scene.play(light(d, i, False), run_time=.15)

def active_cell():
    c = Ellipse(width=10,height=4.9,color=BLUE,fill_color=BLUE,fill_opacity=.22).move_to([0,-.1,0])
    rec = tick((0,2.35),1.15)
    glow = RoundedRectangle(width=1.45,height=.55,corner_radius=.2,stroke_width=0,
                            fill_color=PINK,fill_opacity=.2).move_to(rec)
    arrows = VGroup(*[Arrow([x,2.08,0],[x,1.35,0],buff=0,color=PINK) for x in [-.4,.4]])
    return VGroup(c,glow,rec,dot((0,2.8),.17),arrows,
                  label('BMP receptor active',0,3.3,28,PINK),
                  label('separated cell',0,-2.95,28,BLUE))

QUESTION = 'Receptors active, so how does the dial fall?'
def puzzle():
    c=active_cell()
    # Keep the active receptor visible above a large, centred question.
    q=label('Receptors active,\nso how does the dial fall?',0,-.25,36)
    return VGroup(c,q)

def cascade():
    c = Ellipse(width=10.5,height=5,color=BLUE,fill_color=BLUE,fill_opacity=.22).move_to([0,-.5,0])
    receptor=chip('growth factor receptor',TEXT,size=28).move_to([0,2.42,0])
    receptor[0].set_fill(BG,opacity=1)
    factor=label('growth factor (e.g. FGF)',0,3.45,30)
    blocks=VGroup(*[chip(name,TEXT,size=30).move_to([x,y,0])
                    for name,x,y in [('kinase',-2.2,.7),('kinase',0,-.65),('MAPK',2.2,-2)]])
    arrows=VGroup(Arrow(receptor.get_bottom(),blocks[0].get_top(),buff=.12,color=SECONDARY),
                  *[Arrow(blocks[i].get_right(),blocks[i+1].get_top(),buff=.12,color=SECONDARY) for i in range(2)])
    return VGroup(c,receptor,factor,blocks,arrows,
                  label('separated cell',0,-3.45,28,BLUE))

def pulse_cell(scene, c, n, total):
    """Slow receptor pulse and a downstream arrow flash, so the held question frame keeps moving."""
    each = total / n
    for _ in range(n):
        scene.play(c[1].animate.set_opacity(.55), Indicate(c[2], color=PINK, scale_factor=1.2),
                   ShowPassingFlash(c[4].copy().set_stroke(width=8), time_width=.6), run_time=each*.5)
        scene.play(c[1].animate.set_opacity(.2), run_time=each*.5)

class S00Title(TitleCard):
    LESSON = 'Neural Induction: The Default Model'
    TITLE = 'One Dial'
    def construct(self):
        # Same house card, with every label meeting this task's 22 pt minimum.
        g = VGroup(T('BIOCHEMISTRYPEDIA', size=22, color=TEAL),
                   T(self.LESSON, size=26, color=GREY),
                   T(self.TITLE, size=62, font=TITLE_FONT),
                   Line(LEFT*1.2, RIGHT*1.2, color=GOLD, stroke_width=4)).arrange(DOWN, buff=.4)
        self.play(FadeIn(g), run_time=.65)
        self.finish()

class S01(SpokenScene):
    def construct(self):
        poses=[(-4,.2),(0,-.6),(4,.2)]
        cells=VGroup(*[cell((x,y),1.25,BLUE) for x,y in poses])
        glows=VGroup(*[RoundedRectangle(width=1.35,height=.5,corner_radius=.22,stroke_width=0,
                                        fill_color=PINK,fill_opacity=.45).move_to([x,y+1.25,0]) for x,y in poses])
        receptors=VGroup(*[VGroup(tick((x,y+1.25),.8),dot((x,y+1.6),.13)) for x,y in poses])
        self.play(FadeIn(cells),FadeIn(glows),FadeIn(receptors),FadeIn(label('separated cells',0,3.15,32)),
                  FadeIn(label('receptors active',0,2.35,28,PINK)),run_time=.7)
        self.play(glows.animate.set_opacity(.15),run_time=.35)
        self.at('turn neural')
        self.play(*[FadeIn(label('neural',x,y,34,TEXT)) for x,y in poses],run_time=.4)
        self.at('yet their')
        self.play(*[Flash(r[0],color=PINK,flash_radius=.55) for r in receptors],
                  *[Indicate(r[0],color=PINK,scale_factor=1.3) for r in receptors],
                  glows.animate.set_opacity(.55),run_time=.8)
        self.play(glows.animate.set_opacity(.2),run_time=.5)
        self.at('How can both')
        self.play(FadeIn(label('How can both be true?',0,-3,38)),glows.animate.set_opacity(.5),run_time=.4)
        self.finish()

class S02(SpokenScene):
    def construct(self):
        self.at('Start by')
        self.play(Create(table(0)), run_time=1.0)
        self.finish()

class S03(SpokenScene):
    def construct(self):
        self.add(table(0))
        for phrase, col in [('The intact cap',0), ('receptors working',1), ('output high',2), ('epidermis',3)]:
            self.at(phrase)
            self.play(FadeIn(entry(0,col)), run_time=.28)
        self.finish()

class S04(SpokenScene):
    def construct(self):
        self.add(table(1))
        for phrase,col in [('The dominant negative',0),('receptors jammed',1),('output low',2),('neural',3)]:
            self.at(phrase)
            self.play(FadeIn(entry(1,col)), run_time=.28)
        self.finish()

class S05(SpokenScene):
    def construct(self):
        self.add(table(2))
        self.at('Separated cells')
        self.play(FadeIn(entry(2,0)), FadeIn(entry(2,1)), run_time=.4)
        self.at('neural')
        self.play(FadeIn(entry(2,3)), run_time=.3)
        self.at('Leave their output')
        self.play(FadeIn(entry(2,2)), run_time=.4)
        self.finish()

class S06(SpokenScene):
    def construct(self):
        self.add(table(3))
        self.at('Separated cells with')
        self.play(FadeIn(entry(3,0)), FadeIn(entry(3,1)), run_time=.55)
        self.at('output high enough')
        self.play(FadeIn(entry(3,2)), run_time=.4)
        self.at('epidermis')
        self.play(FadeIn(entry(3,3)), run_time=.3)
        self.finish()

class S07(SpokenScene):
    def construct(self):
        self.add(table(4))
        self.at('The output column')
        self.play(Create(SurroundingRectangle(VGroup(*[entry(r,2) for r in range(4)]),buff=.16,color=SECONDARY)),run_time=.45)
        self.at("the model's reading")
        self.play(FadeIn(output_note()),run_time=.4)
        self.finish()

class S08(SpokenScene):
    def construct(self):
        tab=table(4,True)
        self.add(tab)
        self.at('Read down')
        self.play(Indicate(VGroup(*[entry(r,c) for r in range(4) for c in [2,3]]),scale_factor=1.02,color=TEXT),run_time=.6)
        self.at('In these four conditions')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        d=dial(None)
        self.play(FadeIn(d),run_time=.45)
        self.at('the cells made skin')
        high=VGroup(label('intact cap / + BMP4',3.8,3.1,26,ORANGE),
                    Arrow([3.7,2.8,0],[1.95,1.3,0],buff=.12,color=ORANGE))
        self.play(FadeIn(high),run_time=.45)
        self.at('Where it was low')
        low=VGroup(label('dominant-negative',-3.8,3.1,26,BLUE),
                   Arrow([-3.7,2.8,0],[-1.95,1.3,0],buff=.12,color=BLUE))
        unknown=VGroup(label('separated: ?',-4.4,-2.1,28,SECONDARY),
                       DashedLine([-3.1,-2.1,0],[-1.3,-1.9,0],color=SECONDARY))
        self.play(FadeIn(low),FadeIn(unknown),run_time=.45)
        self.finish()

class S09(SpokenScene):
    def construct(self):
        # Plain background: three clean centred lines, nothing behind them.
        self.at('In a')
        self.play(FadeIn(label('Hemmati-Brivanlou and Melton',0,1.5,34)),
                  FadeIn(label('1997 review',0,.5,30,SECONDARY)),run_time=.4)
        self.at('called this')
        self.play(FadeIn(label('the default model',0,-.8,48)),run_time=.45)
        self.finish()

class S10(SpokenScene):
    def construct(self):
        low=chip('low BMP output',YELLOW,size=32).move_to([-3.9,1.65,0])
        neural=chip('neural',BLUE,size=36).move_to([4,1.65,0])
        high=chip('high BMP output',YELLOW,size=32).move_to([-3.9,-1.85,0])
        skin=chip('epidermis',ORANGE,size=36).move_to([4,-1.85,0])
        a=Arrow(low.get_right(),neural.get_left(),buff=.2,color=BLUE,stroke_width=5)
        b=Arrow(high.get_right(),skin.get_left(),buff=.2,color=ORANGE,stroke_width=5)
        self.add(heading('Early frog cap cultures'),low)
        self.at('neural is the fate')
        self.play(GrowArrow(a),FadeIn(neural),run_time=.55)
        self.at('cells can still respond')
        self.play(FadeIn(label('competent cells',0,-3.15,30,SECONDARY)),run_time=.35)
        self.at('such as')
        fgf=label('FGF-dependent input',0,-.1,28,SECONDARY)
        self.play(FadeIn(fgf),GrowArrow(Arrow([0,.3,0],[0,1.65,0],color=SECONDARY,buff=.05)),run_time=.5)
        self.at('intact')
        self.play(FadeIn(high),run_time=.3)
        self.at('promotes epidermis')
        self.play(GrowArrow(b),FadeIn(skin),run_time=.5)
        self.finish()

class S11(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=12,height=4.5,corner_radius=.25,color=SECONDARY).move_to([0,-.2,0])
        self.add(box,heading('“Default” is operational'))
        self.at('Default is an operational word')
        self.play(FadeIn(label('low BMP pathway output  →  neural',0,1.4,34,BLUE)),run_time=.45)
        self.at('in these cultures')
        self.play(FadeIn(label('in these early cap cultures',0,.4,32)),run_time=.4)
        self.at('with competent cells')
        self.play(FadeIn(label('competent cells + other inputs\n(such as FGF) intact',0,-.7,30,SECONDARY)),run_time=.45)
        self.at('not a fate')
        no=label('“no signals at all”',0,-1.95,34,SECONDARY)
        strike=Line(no.get_left()+LEFT*.3,no.get_right()+RIGHT*.3,color=TEXT,stroke_width=5)
        self.play(FadeIn(no),Create(strike),run_time=.5)
        self.finish()

class S12(SpokenScene):
    def construct(self):
        self.add(table(4,True))
        self.at('Now the third row')
        self.play(Create(row_light(2)),run_time=.55)
        self.at('The first explanation')
        self.play(FadeIn(label('First explanation: dilution',0,3.5,29)),run_time=.6)
        self.finish()

class S13(SpokenScene):
    def construct(self):
        dish=RoundedRectangle(width=6.2,height=3.4,corner_radius=.5,color=SECONDARY).move_to([0,-.1,0])
        cells=VGroup(*[cell((x,-.2),.8) for x in [-1.6,0,1.6]])
        dots=VGroup(*[dot((x,y),.11) for x,y in [(-.8,.25),(-.8,-.65),(.8,.25),(.8,-.65),(-.55,.8),(.55,.8),(-.5,-1),(.5,-1)]])
        caption=label('close',0,2.3,32,SECONDARY)
        self.add(dish,cells,dots,caption)
        self.at('Separation spreads')
        self.wait(.45)
        self.play(dish.animate.stretch_to_fit_width(12.5).stretch_to_fit_height(6.6),
                  cells[0].animate.move_to([-4.5,1.5,0]),cells[1].animate.move_to([0,-2.2,0]),
                  cells[2].animate.move_to([4.5,.4,0]),
                  *[d.animate.move_to([(-3+i*.9),.8-(i%3)*1.1,0]) for i,d in enumerate(dots)],
                  FadeOut(caption),run_time=1.7)
        self.at('large volume of fluid')
        self.play(FadeIn(label('far · large volume of fluid',0,2.65,30,SECONDARY)),run_time=.35)
        self.at('they pass to one another')
        self.play(*[d.animate.shift((RIGHT if i%2 else LEFT)*.7).set_opacity(.5) for i,d in enumerate(dots)],run_time=.9)
        self.at('would be diluted away')
        self.play(FadeOut(VGroup(*dots[:4])),run_time=.5)
        self.play(*[d.animate.set_opacity(.15).shift(DOWN*.3) for d in dots[4:]],run_time=.6)
        self.play(FadeOut(VGroup(*dots[4:])),run_time=.5)
        self.finish()

class S14(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[20,220,40],y_range=[0,1.01,.25],x_length=10.4,y_length=5.2,
                  tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.25,-.25,0])
        curve = ax.plot(lambda r:20/r,x_range=[20,220],color=YELLOW,stroke_width=5,use_smoothing=False)
        self.add(ax,label('relative BMP concentration',-2.9,2.8,26,YELLOW),
                 label('distance from a cell',.4,-3.32,26,GREY))
        self.at('It was a fair guess')
        self.play(Create(curve),FadeIn(heading('A fair guess')),run_time=.9)
        self.at('spreads freely')
        marker = dot(ax.c2p(20,1),.13)
        near = cell((-4.95,-2.75),.18)
        far = cell((-4.25,-2.75),.18)
        self.add(marker,near,far)
        self.play(MoveAlongPath(marker,curve),far.animate.move_to([5,-2.75,0]),run_time=1.3,rate_func=linear)
        self.at('physics of diffusion')
        self.play(FadeIn(label('free diffusion · illustrative',3.4,2.8,26,SECONDARY)),run_time=.4)
        self.finish()

class S15(SpokenScene):
    def construct(self):
        c=active_cell()
        self.add(c)
        self.at('But later work')
        self.play(c[1].animate.set_opacity(.4),run_time=.4)
        self.at('receptors keep signaling')
        self.play(Indicate(c[2],color=PINK,scale_factor=1.25),
                  ShowPassingFlash(c[4].copy().set_stroke(width=7)),run_time=.8)
        self.at('So how could')
        self.play(FadeIn(label('Receptors active,\nso how does the dial fall?',0,-.25,36)),run_time=.45)
        pulse_cell(self,c,2,max(.5,self.narration_s-self.elapsed()-.2))
        self.finish()

class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        c=active_cell()
        self.add(c,label('Receptors active,\nso how does the dial fall?',0,-.25,36))
        pulse_cell(self,c,4,5.0)

class S17(SpokenScene):
    def construct(self):
        g=cascade()
        # Separation first, then the cell with its receptor, then the cascade lights in order.
        pair=VGroup(cell((-1,0),1),cell((1,0),1))
        self.add(pair,label('separation',0,3.2,34))
        self.at('Separation switches on')
        self.play(pair[0].animate.shift(LEFT*3),pair[1].animate.shift(RIGHT*3),run_time=.6)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(VGroup(g[0],g[1],g[5])),run_time=.35)
        self.at('lasting signaling')
        self.play(FadeIn(g[3]),FadeIn(g[4]),run_time=.5)
        self.at('a kinase cascade')
        self.play(Indicate(g[1],color=YELLOW,scale_factor=1.06),run_time=.4)
        self.play(LaggedStart(*[Indicate(b,color=YELLOW,scale_factor=1.12) for b in g[3]],lag_ratio=.6),run_time=1.15)
        self.at('usually started by')
        self.play(Indicate(g[1],color=YELLOW,scale_factor=1.08),run_time=.5)
        self.at('such as')
        self.play(FadeIn(g[2]),run_time=.4)
        self.play(LaggedStart(*[Indicate(b,color=YELLOW,scale_factor=1.05) for b in [g[1],*g[3]]],lag_ratio=.3),run_time=.8)
        self.finish()

class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(cascade())
        self.wait(2.5)

def smad_marked(mark=True):
    bar=RoundedRectangle(width=9.6,height=2.2,corner_radius=.16,color=TEXT,
                         fill_color=TEXT,fill_opacity=.12).move_to([0,-.15,0])
    linker=Rectangle(width=1.65,height=2.2,color=SECONDARY,fill_color=SECONDARY,fill_opacity=.25).move_to(bar)
    g=VGroup(bar,linker,label('Smad1',-3,-.15,40))
    if mark: g.add(chip('P',TEXT,size=32).move_to([0,-.15,0]))
    return g

class S19(SpokenScene):
    def construct(self):
        g=smad_marked(False)
        self.add(g,heading('MAPK'))
        p=chip('P',TEXT,size=32).move_to([0,2.1,0])
        self.at('phosphorylate')
        self.add(p)
        self.play(p.animate.move_to([0,-.15,0]),run_time=.65)
        self.at('in its middle')
        self.play(Indicate(g[1],color=YELLOW,scale_factor=1.04),run_time=.4)
        self.at('or linker')
        self.play(FadeIn(label('linker region',0,-2.6,32,SECONDARY)),
                  GrowArrow(Arrow([0,-2.2,0],[0,-1.3,0],buff=.08,color=SECONDARY)),run_time=.4)
        self.finish()

class S20(SpokenScene):
    def construct(self):
        # Same cartoon bar, zoomed to meet a large nuclear envelope.
        g=smad_marked().scale(.48).move_to([-3.7,.1,0])
        g[2].become(label('Smad1',-4.9,.1,28))
        g[3].become(chip('P',TEXT,size=28).move_to([-3.7,.1,0]))
        nucleus=Circle(radius=2.7,color=SECONDARY,stroke_width=6).move_to([3.3,-.1,0])
        self.add(g,nucleus,label('nucleus',3.3,-.1,36,SECONDARY),
                 label('can keep out of the nucleus',0,3.2,32))
        self.at('That can keep')
        self.play(g.animate.shift(RIGHT*2),run_time=.55)
        self.at('out of the nucleus')
        self.play(g.animate.shift(LEFT*1.2),FadeIn(label('stays out',-3.4,1.7,32)),run_time=.45)
        self.at('mark it for destruction')
        pieces=VGroup(*[Rectangle(width=.6,height=.6,color=TEXT,fill_color=TEXT,fill_opacity=.5)
                        .move_to([-5+i*.65,-.2-(i%2)*.8,0]) for i in range(7)])
        self.play(ReplacementTransform(g,pieces),FadeIn(label('can mark for destruction',-2.5,-2.9,28,SECONDARY)),run_time=.4)
        self.play(pieces.animate.shift(DOWN*.4).set_opacity(.08),run_time=.55)
        self.finish()

class S21(SpokenScene):
    def construct(self):
        d=dial(None)
        self.add(d)
        self.at('The cells need this activity')
        self.play(FadeIn(label('In separated cells, MAPK activity\nis needed for neural fate',0,3.05,28)),run_time=.45)
        self.at('The dial still goes down')
        hand_turn(self,d,2,PI-.45,keep=True)
        self.at('by a different hand')
        self.play(Indicate(d.grips[2][0],color=TEAL,scale_factor=1.06),run_time=.5)
        self.finish()

class S22(SpokenScene):
    def construct(self):
        d=dial(False)
        self.add(d)
        self.at('the fourth row')
        self.play(FadeIn(label('Row 4 · separated cells + BMP4 → epidermis',0,3.13,28,ORANGE)),run_time=.4)
        self.at('The damping is partial')
        damping=VGroup(label('partial MAPK damping',4.55,1.0,26,TEAL),
                       Line([4.55,.72,0],[4.55,.32,0],color=TEAL,stroke_width=3),dot((4.55,.3),.07,TEAL))
        self.play(light(d,2),FadeIn(damping),run_time=.4)
        self.at('enough added')
        bmp=VGroup(*[dot((-5.4+i*.5,.55),.14) for i in range(3)])
        self.play(FadeIn(bmp),FadeIn(label('extra BMP4',-4.55,1.05,26,YELLOW)),run_time=.4)
        self.at('can push the output back up')
        self.play(light(d,0),bmp.animate.shift(RIGHT*2.1),run_time=.3)
        turn(self,d,1.0,.7)
        self.finish()

class S23(SpokenScene):
    def construct(self):
        d=dial(1.0)
        self.add(d)
        self.at('That is why')
        self.play(FadeIn(heading('The rule names the dial')),run_time=.35)
        self.at('SMOD1')
        ring=SurroundingRectangle(VGroup(d[4][0],d[4][1]),buff=.15,color=YELLOW,stroke_width=5,corner_radius=.15)
        self.play(Create(ring),d[4][0].animate.set_color(YELLOW),Indicate(VGroup(d[4][0],d[4][1]),color=YELLOW,scale_factor=1.08),run_time=.7)
        self.at('It does not name')
        fluid=label('BMP in the fluid',-4.5,-2.35,32,TEXT)
        strike=Line(fluid.get_left()+LEFT*.15,fluid.get_right()+RIGHT*.15,color=TEXT,stroke_width=5)
        self.play(FadeIn(fluid),run_time=.3)
        self.play(Create(strike),fluid.animate.set_opacity(.9),run_time=.45)
        self.finish()

class S24(SpokenScene):
    def construct(self):
        d=dial(True)
        self.add(d)
        self.at('The takeaway')
        self.play(FadeIn(heading('Three hands can turn the dial down')),run_time=.4)
        for phrase,i,angle in [('Outside the cell',0,1.1),('at the membrane',1,1.9),('or inside it',2,PI-.45)]:
            self.at(phrase)
            hand_turn(self,d,i,angle)
        self.finish()

class S25End(EndCard):
    LINE = 'Three hands can turn the dial down.'
    def construct(self):
        line=T(self.LINE,size=40,font=TITLE_FONT)
        fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',size=26,color=TEAL)
        g=VGroup(line,sub).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6)
        self.finish()
