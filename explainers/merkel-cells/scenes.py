"""Chapter 1: Two Receptors, One Nerve.

COLOR MAP, shared with scenes.old.py (CHAPTERS.md is outside the edit scope):
ORANGE #F29E4C: Merkel cells; PURPLE #B58CD9: afferent ending/axon;
BLUE: Piezo2; YELLOW: spikes; GREEN: preserved responses;
RED: excluded lineage; TEAL: synaptic signal; GOLD: phases/cautions;
GREY: skin, stimulus, neutral labels. Rasters are schematic, not recordings.
The deterministic spike_times model and pair/ticks geometry are reused from
scenes.old.py. No fitted or invented experimental curves are drawn.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def pair(cx=0, cy=0, s=1, cell_color=ORANGE, fibre=2):
    body = RoundedRectangle(corner_radius=.55*s, width=2*s, height=1.7*s,
        stroke_color=cell_color, stroke_width=4, fill_color=cell_color,
        fill_opacity=.22).move_to([cx, cy, 0])
    disc = RoundedRectangle(corner_radius=.08*s, width=1.5*s, height=.22*s,
        stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([cx, cy-1.15*s, 0])
    line = Line(disc.get_bottom(), disc.get_bottom()+DOWN*fibre*s,
        color=PURPLE, stroke_width=7)
    g = VGroup(body, line, disc)
    g.body, g.line, g.disc = body, line, disc
    return g


def ticks(xs, y, h=.8, color=YELLOW, w=4):
    return VGroup(*[Line([x, y-h/2, 0], [x, y+h/2, 0], color=color,
                        stroke_width=w) for x in xs])


def spike_times():
    rng = np.random.default_rng(7)
    ts, t = [], .15
    for i in range(9):
        ts.append(t)
        t += .11 + .025*i
    t = ts[-1] + .55
    while t < 8.8:
        ts.append(t)
        t += float(rng.gamma(1.2, .5)) + .12
    return ts


def channel_label(pos):
    g = chip('Piezo2',BLUE,26).move_to(pos)
    g[0].set_fill(BG,1)
    g.set_z_index(3)
    return g


def heading(text, color=TEXT):
    return T(text, 32, color, weight=BOLD).move_to([0, 3.05, 0])


def raster(y=0, ra=False, x0=-4.5, x1=5.7, h=1.05):
    fx = lambda t: x0+(x1-x0)*t/10
    ts = [.15, .35, .6, 9.3, 9.55, 9.8] if ra else spike_times()
    base = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_opacity=.4)
    tk = ticks([fx(t) for t in ts], y, h)
    return VGroup(base, tk)


def stimulus(y=-2.25, x0=-4.5, x1=5.7):
    bounds = [x0, x0+(x1-x0)*.19, x0+(x1-x0)*.91, x1]
    g = VGroup()
    for a,b,name in zip(bounds[:-1], bounds[1:], ['press','hold','lift']):
        g.add(Rectangle(width=b-a-.06, height=.19, stroke_width=0,
                       fill_color=GREY, fill_opacity=.7).move_to([(a+b)/2,y,0]))
        g.add(T(name,26,GREY).move_to([(a+b)/2,y-.48,0]))
    return g


def phase_view():
    r = raster(.5)
    st = stimulus(-1.3)
    title = heading('SA1 afferent')
    note = T('schematic · time →',26,GREY).move_to([0,-3.15,0])
    return VGroup(title,r,st,note)


def phase_box(dynamic=True, y=.5):
    a,b = (-4.65,-2.45) if dynamic else (-2.3,4.65)
    return RoundedRectangle(width=b-a,height=1.65,corner_radius=.12,
        stroke_color=GOLD,stroke_width=3).move_to([(a+b)/2,y,0])


def skin():
    # Piecewise straight section: a touch dome beside a guard hair, no data curve.
    epidermis = Polygon([-5.9,.5,0],[-3,.5,0],[-2.3,1.8,0],[2.6,1.8,0],
        [3.3,.5,0],[5.9,.5,0],[5.9,-1.3,0],[-5.9,-1.3,0],
        color=GREY,fill_color=GREY,fill_opacity=.13,stroke_width=3)
    cells = VGroup(*[RoundedRectangle(width=.95,height=.78,corner_radius=.3,
        color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([x,-.65,0])
        for x in [-1.5,0,1.5]])
    hair = Polygon([3.7,-1.5,0],[4,-1.5,0],[3.5,2.65,0],[3.3,2.65,0],
                   color=GREY,fill_color=GREY,fill_opacity=.8)
    follicle=Ellipse(width=.85,height=2.3,color=GREY).move_to([3.75,-.45,0])
    dermis=Rectangle(width=11.8,height=1.35,color=GREY,stroke_width=2,
        fill_color=GREY,fill_opacity=.07).move_to([0,-1.975,0])
    return VGroup(VGroup(epidermis,dermis),cells,VGroup(follicle,hair))


def branches():
    ax = VGroup(Line([0,-3,0],[0,-2.1,0],color=PURPLE,stroke_width=8))
    for x in [-1.5,0,1.5]:
        ax.add(Line([0,-2.1,0],[x,-1.25,0],color=PURPLE,stroke_width=6))
        ax.add(RoundedRectangle(width=.85,height=.16,corner_radius=.06,
            stroke_width=0,fill_color=PURPLE,fill_opacity=1).move_to([x,-1.17,0]))
    return ax


def routes(labels=False):
    p = pair(0,.65,1.65,fibre=1.25)
    a = Arrow([-5.5,-1.25,0],p.disc.get_left(),buff=.12,color=PURPLE,stroke_width=7)
    b = Arrow([5.5,.9,0],p.body.get_right(),buff=.12,color=ORANGE,stroke_width=7)
    g = VGroup(p,a,b)
    if labels:
        g.add(route_label(a),route_label(b,False))
    return g


def route_label(arrow, ending=True):
    text=T('ending’s own\ntransduction' if ending else 'the Merkel cell,\nthrough a synapse',28,PURPLE if ending else ORANGE)
    text.move_to([-4,-2.1,0] if ending else [4.2,1.85,0])
    start=text.get_top()+UP*.12 if ending else text.get_bottom()+DOWN*.12
    end=arrow.get_center()+(DOWN*.12 if ending else UP*.12)
    return VGroup(text,Line(start,end,color=PURPLE if ending else ORANGE))


def prediction(question=True):
    p = pair(-4.65,.25,1.18,fibre=1.3)
    a = Arrow([-6.35,-1.1,0],p.disc.get_left(),buff=.07,color=PURPLE,stroke_width=7)
    b = Arrow([-2.2,1.1,0],p.body.get_right(),buff=.07,color=ORANGE,stroke_width=7)
    ending=T('ending',28,PURPLE).move_to([-5.65,-2.25,0])
    cell=T('Merkel cell',28,ORANGE).move_to([-4.6,1.95,0])
    labs = VGroup(ending,cell,
        Line(ending.get_top(),a.get_center()+DOWN*.12,color=PURPLE),
        Line(cell.get_right(),b.get_center()+UP*.12,color=ORANGE))
    r = raster(-.35,x0=-1.75,x1=6.1,h=1.9)
    boxes = VGroup(RoundedRectangle(width=1.65,height=2.35,corner_radius=.1,color=GOLD).move_to([-.95,-.35,0]),
                   RoundedRectangle(width=6.15,height=2.35,corner_radius=.1,color=GOLD).move_to([3.05,-.35,0]))
    phase = VGroup(T('dynamic',26,GOLD).move_to([-.95,-1.8,0]),T('static',26,GOLD).move_to([3.25,-1.8,0]))
    tags = VGroup(*[RoundedRectangle(width=w,height=.72,corner_radius=.1,color=GREY).move_to([x,1.65,0]) for x,w in [(-.85,2.5),(3.55,4.1)]])
    q = T('Which route makes which phase?',32,YELLOW).move_to([0,-3.2,0])
    note = T('schematic SA1 firing · time →',26,GREY).move_to([2.2,2.65,0])
    g = VGroup(p,a,b,labs,r,boxes,phase,tags,note,stimulus(-2.25,x0=-1.75,x1=6.1))
    if question: g.add(q)
    g.tags, g.q = tags,q
    return g


def answer():
    g=prediction(False)
    g.tags[0].set_color(PURPLE); g.tags[1].set_color(ORANGE)
    g.add(T('mainly ending',26,PURPLE).move_to(g.tags[0]),
          T('mainly Merkel cell',26,ORANGE).move_to(g.tags[1]),
          T('mouse touch domes; onset source still argued',26,GREY).move_to([0,-3.15,0]))
    return g


def idea():
    return VGroup(T('The ending mainly feels the change.',36,PURPLE).move_to([0,1.1,0]),
                  T('The Merkel cell mainly holds the press.',36,ORANGE).move_to([0,-.65,0]),
                  T('in mouse touch domes',28,GREY).move_to([0,-2.25,0]))


class S00Title(TitleCard):
    TITLE = 'Two Receptors, One Nerve'
    LESSON = 'Merkel Cells: Touch Receptors That Are Not Neurons'

    def construct(self):
        # Full lesson title stays >=22 pt by wrapping rather than scaling.
        self.add(T('BIOCHEMISTRYPEDIA',22,TEAL).move_to([0,2.4,0]),
                 VGroup(T('Merkel Cells: Touch Receptors',26,GREY),T('That Are Not Neurons',26,GREY)).arrange(DOWN,buff=.25).move_to([0,1.2,0]))
        self.play(FadeIn(T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.4,0])),run_time=.8)
        self.add(Line([-1.2,-1.5,0],[1.2,-1.5,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        # Side view: nail above, fleshy pad flattened against a narrow coin rim.
        finger=VMobject(color=GREY,fill_color=GREY,fill_opacity=.25,stroke_width=4)
        finger.set_points_smoothly([[-5.7,2.25,0],[-2.5,2.2,0],[.1,1.95,0],
            [2.2,1.25,0],[2.7,.35,0],[2.25,-.25,0],[1.15,-.55,0],
            [.4,-.55,0],[-.3,-.2,0],[-2.8,-.1,0],[-5.7,-.2,0]])
        finger.close_path()
        nail=RoundedRectangle(width=2.5,height=.72,corner_radius=.28,color=GREY,
            fill_color=BG,fill_opacity=.7).rotate(-.2).move_to([.3,1.5,0])
        creases=VGroup(*[Arc(radius=.65,start_angle=-.7,angle=1.4,color=GREY).move_to([x,.65,0]) for x in [-3.4,-2.95]])
        coin=RoundedRectangle(width=.8,height=2.55,corner_radius=.13,color=GOLD,
            fill_color=GOLD,fill_opacity=.24).move_to([.8,-2.05,0])
        rim=VGroup(*[Line([.47,y,0],[1.13,y,0],color=GOLD,stroke_width=2) for y in np.arange(-3.12,-.85,.2)])
        self.add(heading('What keeps reporting the edge?',YELLOW),finger,nail,creases,coin,rim,
                 T('fingertip',28,GREY).move_to([-4,-1.1,0]),
                 T('coin edge',28,GOLD).move_to([3.4,-1.8,0]),
                 Line([2.45,-1.8,0],[1.2,-1.8,0],color=GOLD))
        self.at('Press a fingertip')
        self.play(VGroup(finger,nail,creases).animate.shift(DOWN*.22),run_time=.8)
        self.at('hold it still')
        self.play(FadeIn(T('press and hold',28,TEXT).move_to([-3.5,-2.5,0])),run_time=.3)
        self.finish()

class S02Rafast(SpokenScene):
    def construct(self):
        r = raster(1.2,ra=True)
        self.add(r[0],stimulus(-2.1),T('schematic · time →',26,GREY).move_to([0,-3.2,0]))
        self.at('Some nerve fibers')
        self.play(FadeIn(T('rapidly adapting (RA)',30,PURPLE).move_to([0,2.6,0])),run_time=.4)
        self.at('fire only while')
        self.play(LaggedStart(*[Create(t) for t in r[1]],lag_ratio=.12),run_time=1.4)
        self.at('they go quiet')
        self.play(FadeIn(T('quiet during the hold',28,GREY).move_to([0,-.3,0])),run_time=.35)
        self.finish()


class S03Sa1(SpokenScene):
    def construct(self):
        ra = raster(1.3,ra=True)
        sa = raster(-.7)
        self.add(ra, T('RA',26,PURPLE).move_to([-5.45,1.3,0]),sa[0],stimulus(-2.4),T('schematic · time →',26,GREY).move_to([0,3.1,0]))
        self.at('Others keep firing')
        self.play(LaggedStart(*[Create(t) for t in sa[1]],lag_ratio=.05),run_time=2)
        self.at('One such class')
        self.play(FadeIn(T('slowly adapting type I (SA1)',28,PURPLE).move_to([0,.35,0])),run_time=.5)
        self.finish()


class S04Macaque(SpokenScene):
    def construct(self):
        finger=RoundedRectangle(width=5.2,height=2.0,corner_radius=.8,color=GREY,fill_opacity=.15).move_to([-3.35,1.35,0])
        strip=Rectangle(width=5.3,height=.18,color=GREY,fill_opacity=.3).move_to([-3.35,-1.8,0])
        positions=[(-1,0),(0,0),(1,0),(-1,1),(1,1),(-1,2),(0,2),(1,2)]
        dots=VGroup(*[Dot([-3.35+x*.8,-1.5+y*.65,0],radius=.16,color=GREY) for x,y in positions])
        grid=VGroup(*[Square(side_length=1.15,color=GREY).move_to([3.2+x*1.25,-1.2+y*1.25,0]) for y in range(3) for x in [-1,0,1]])
        active=VGroup(*[Square(side_length=.98,stroke_width=0,fill_color=YELLOW,fill_opacity=.7).move_to([3.2+x*1.25,-1.2+y*1.25,0]) for x,y in positions])
        self.add(finger,strip,dots,grid,heading('macaque fingertip recordings'),T('raised pattern',28,GREY).move_to([-3.35,-2.8,0]),T('SA1 spatial firing',28,YELLOW).move_to([3.2,-2.8,0]))
        self.at('In macaque fingertips')
        self.play(finger.animate.shift(DOWN*.25),run_time=.5)
        self.at('its firing carried')
        self.play(LaggedStart(*[FadeIn(a) for a in active],lag_ratio=.2),run_time=2)
        self.at('such as raised')
        self.play(Indicate(dots,color=YELLOW),Indicate(active,color=YELLOW),run_time=.7)
        self.finish()

class S05Dynamic(SpokenScene):
    def construct(self):
        self.add(phase_view())
        self.at('Its firing has')
        self.wait(.4)
        self.at('a fast burst')
        self.play(Create(phase_box()),run_time=.5)
        self.at('dynamic phase')
        self.play(FadeIn(T('dynamic phase',28,GOLD).move_to([-3.55,2,0])),run_time=.4)
        self.finish()


class S06Static(SpokenScene):
    def construct(self):
        v = phase_view()
        self.add(v,phase_box(),T('dynamic phase',28,GOLD).move_to([-3.55,2,0]))
        self.at('then firing through')
        self.play(Create(phase_box(False)),run_time=.6)
        self.at('irregular gaps')
        self.play(Indicate(v[1][1][9:],color=YELLOW,scale_factor=1.08),run_time=.6)
        self.at('static phase')
        self.play(FadeIn(T('static phase: irregular intervals',26,GOLD).move_to([1.4,2,0])),run_time=.4)
        self.finish()


class S07Surprise(SpokenScene):
    def construct(self):
        outline=RoundedRectangle(width=11,height=4.5,corner_radius=1.6,color=GREY,fill_opacity=.1).move_to([0,.2,0])
        band=Rectangle(width=9.3,height=1.4,color=GREY,fill_opacity=.12).move_to([0,-.8,0])
        cells=VGroup(*[RoundedRectangle(width=1.5,height=1.2,corner_radius=.4,color=GREY).move_to([x,-.85,0]) for x in [-3.4,-1.7,0,1.7,3.4]])
        cells[2].set_color(ORANGE).set_fill(ORANGE,.3)
        q=T('?',42,YELLOW).move_to(cells[2])
        drawing=VGroup(outline,band,cells,q)
        self.add(drawing,heading('not a neuron?',YELLOW),T('fingertip skin: base of the epidermis',28,GREY).move_to([0,-3,0]))
        self.at('Now the surprise')
        self.play(drawing.animate.scale(1.12),run_time=.7)
        self.at('The cell that')
        self.play(Indicate(cells[2],color=ORANGE),run_time=.7)
        self.finish()

class S08Lineage(SpokenScene):
    def construct(self):
        cell=pair(0,-1.1,1.45).body
        self.add(cell)
        self.at('It is the')
        self.play(FadeIn(heading('Merkel cell',ORANGE)),run_time=.3)
        self.at('In mice')
        self.add(T('mouse lineage tracing',28,GREY).move_to([0,2.15,0]))
        self.at('comes from')
        prog=chip('epidermal\nprogenitors',GREY,34).move_to([-4,1.1,0])
        arrow=Arrow([-2.7,.8,0],[-1.1,-.4,0],color=ORANGE,buff=.1)
        self.play(FadeIn(prog),GrowArrow(arrow),run_time=.4)
        self.at('not from neural')
        neural=chip('neural\ncrest',GREY,34).move_to([4,1.1,0])
        no=Arrow([2.9,.8,0],[1.1,-.4,0],color=GREY,buff=.1)
        mid=no.get_center()
        cross=VGroup(Line(mid+[-.28,.32,0],mid+[.28,-.32,0],color=RED,stroke_width=6),Line(mid+[-.28,-.32,0],mid+[.28,.32,0],color=RED,stroke_width=6))
        self.play(FadeIn(neural),GrowArrow(no),Create(cross),run_time=.5)
        self.finish()

def dome_labels():
    return VGroup(T('touch dome',28,GREY).move_to([0,2.35,0]),Line([0,2.05,0],[0,1.8,0],color=GREY),
        T('Merkel cells (basal layer)',28,ORANGE).move_to([-2.9,-3.15,0]),Line([-2.2,-2.85,0],[-1.5,-1,0],color=ORANGE),
        T('guard hair',26,GREY).move_to([5,2.7,0]),Line([4.3,2.7,0],[3.5,2.45,0],color=GREY))


class S09Dome(SpokenScene):
    def construct(self):
        sk=skin(); labs=dome_labels()
        self.add(sk[0],heading('hairy mouse skin'))
        self.at('cells cluster')
        self.play(FadeIn(sk[1]),FadeIn(VGroup(labs[2],labs[3])),run_time=.4)
        self.at('touch domes')
        self.play(FadeIn(VGroup(labs[0],labs[1])),run_time=.3)
        self.at('guard hairs')
        self.play(FadeIn(sk[2]),FadeIn(VGroup(labs[4],labs[5])),run_time=.3)
        self.finish()

class S10Ending(SpokenScene):
    def construct(self):
        self.add(skin(),heading('hairy mouse skin'),dome_labels())
        ax=branches()
        self.at('An afferents branched ending')
        self.play(Create(ax[0]),*[Create(ax[i]) for i in [1,3,5]],run_time=.65)
        self.at('makes disc')
        self.play(*[FadeIn(ax[i]) for i in [2,4,6]],run_time=.3)
        self.add(T('one afferent, usually',28,PURPLE).move_to([2.5,-3.15,0]))
        self.finish()

class S11Routes(SpokenScene):
    def construct(self):
        old=VGroup(skin(),branches(),dome_labels())
        g=routes()
        self.add(old)
        self.at('So force can')
        self.play(ReplacementTransform(old,g[0]),run_time=.5)
        self.add(heading('Two routes, one fibre'))
        self.play(GrowArrow(g[1]),GrowArrow(g[2]),run_time=.35)
        self.at('by two roots')
        self.play(Indicate(VGroup(g[1],g[2]),scale_factor=1.04),run_time=.3)
        self.finish()

def disc_channel(g):
    icon=Rectangle(width=.22,height=.4,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to(g[0].disc.get_left()+RIGHT*.25)
    label=T('makes Piezo2',28,BLUE).move_to([3,-2.15,0])
    lead=Line(label.get_left()+LEFT*.12,icon.get_bottom(),color=BLUE)
    return VGroup(icon,label,lead)


class S12Route1(SpokenScene):
    def construct(self):
        g=routes(); self.add(g,heading('Two routes, one fibre'))
        self.at('The ending makes')
        self.play(FadeIn(disc_channel(g)),FadeIn(route_label(g[1])),run_time=.4)
        self.at('Even without')
        self.remove(g[0].body,g[2]); g[0].remove(g[0].body); g.remove(g[2])
        self.add(T('no Merkel cell',30,GREY).move_to([0,.65,0]))
        self.at('it still responds')
        d=Dot(g[0].disc.get_center(),radius=.12,color=YELLOW)
        self.play(FadeIn(d),run_time=.1)
        self.play(d.animate.move_to(g[0].line.get_end()),run_time=.6)
        self.play(FadeOut(d),FadeIn(T('touch response remains',28,GREEN).move_to([3.2,-3.0,0])),run_time=.2)
        self.finish()

class S13Route2(SpokenScene):
    def construct(self):
        g=routes(labels=True)
        self.add(g[0].line,g[0].disc,g[1],g[3],heading('Two routes, one fibre'),disc_channel(g))
        self.at('or the merkle cell')
        self.play(FadeIn(g[0].body),GrowArrow(g[2]),FadeIn(g[4]),run_time=.5)
        self.at('through its own')
        self.play(FadeIn(channel_label([0,.95,0])),run_time=.3)
        self.at('passes the signal')
        ves=VGroup(*[Dot([x,-.95,0],radius=.075,color=TEAL) for x in [-.75,-.38,0,.38,.75]])
        self.play(FadeIn(ves),run_time=.2)
        self.at('across a synapse')
        self.play(FadeIn(T('synapse',28,TEAL).move_to([3,-.7,0])),Create(Line([2.1,-.7,0],[.85,-.95,0],color=TEAL)),run_time=.3)
        self.finish()

class S14Predict(SpokenScene):
    def construct(self):
        g = prediction()
        self.add(g)
        self.at('Predict')
        self.wait(.3)
        self.at('One route reports')
        self.play(Indicate(g[5][0],color=GOLD,scale_factor=1.04),run_time=.6)
        self.at('One route holds')
        self.play(Indicate(g[5][1],color=GOLD,scale_factor=1.04),run_time=.6)
        self.at('Which would you')
        self.play(Indicate(g.q,color=YELLOW,scale_factor=1.03),run_time=.4)
        self.finish()


class S15Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(prediction(),T('pause and guess',22,GREY).move_to([-4.85,-3.15,0]))
        self.wait(5)


class S16Reveal(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g)
        self.at('In mouse touch domes')
        self.play(ReplacementTransform(g.q,T('mouse touch domes; onset source still argued',26,GREY).move_to([0,-3.15,0])),run_time=.3)
        self.at('the ending mainly')
        self.play(FadeIn(T('mainly ending',26,PURPLE).move_to(g.tags[0])),g.tags[0].animate.set_color(PURPLE),run_time=.35)
        self.at('mainly holds')
        self.play(FadeIn(T('mainly Merkel cell',26,ORANGE).move_to(g.tags[1])),g.tags[1].animate.set_color(ORANGE),run_time=.35)
        self.finish()

class S17Idea(SpokenScene):
    def construct(self):
        g = idea()
        prior = answer()
        self.add(prior)
        self.at('That is the idea')
        self.wait(.4)
        self.at('The ending mainly')
        self.play(FadeOut(prior),FadeIn(heading('The idea')),FadeIn(g[0]),FadeIn(g[2]),run_time=.5)
        self.at('and the Merkel')
        self.play(FadeIn(g[1]),run_time=.5)
        self.finish()


class S18Hold(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(heading('The idea'),idea())
        self.wait(3)


class S19Scope(SpokenScene):
    def construct(self):
        # Separate word objects make the hedge the only underlined text.
        rows=VGroup(*[VGroup(T(prefix,26,color),T('mainly',26,color),T(phase,26,color)).arrange(RIGHT,buff=.12)
            for prefix,phase,color in [('ending:', 'change',PURPLE),('Merkel cell:', 'hold',ORANGE)]])
        rows.arrange(DOWN,buff=.22,aligned_edge=LEFT).move_to([-3.2,2.8,0])
        sk=skin().stretch(.95,1).shift(DOWN*1.1)
        self.add(sk,rows,T('mouse touch domes',28,GREY).move_to([3.5,3.15,0]))
        self.at('This is mouse')
        self.wait(.2)
        self.at('the word mainly')
        self.play(*[Create(Underline(row[1],color=GOLD)) for row in rows],run_time=.4)
        self.at('may help with')
        self.play(FadeIn(T('Merkel cell may also help onset',26,ORANGE).move_to([-2.8,1.75,0])),run_time=.4)
        self.finish()

class S20Rat(SpokenScene):
    def construct(self):
        dome=VGroup(skin(),branches()).scale(.56).move_to([-3.4,1.05,0])
        follicle=Ellipse(width=2.3,height=3.2,color=GREY).move_to([3.3,1.15,0])
        whisker=Line([3.3,.7,0],[2.8,2.8,0],color=GREY,stroke_width=7)
        cells=VGroup(*[RoundedRectangle(width=.58,height=.48,corner_radius=.15,color=ORANGE,fill_color=ORANGE,fill_opacity=.25).move_to([3.3+dx,.1,0]) for dx in [-.65,0,.65]])
        nerve=VGroup(Line([3.3,-.55,0],[3.3,-.2,0],color=PURPLE,stroke_width=5),*[Line([3.3,-.2,0],[3.3+dx,-.18,0],color=PURPLE,stroke_width=4) for dx in [-.65,0,.65]])
        self.add(dome,T('mouse touch dome',28,GREY).move_to([-3.6,3.2,0]))
        self.at('Rat whiskers')
        self.play(FadeIn(VGroup(follicle,whisker,cells,nerve)),FadeIn(T('rat whisker follicle',28,GREY).move_to([3.2,3.2,0])),run_time=.4)
        self.at('another laboratory argues')
        self.add(T('another laboratory’s reading',22,GOLD).move_to([0,3.65,0]))
        self.at('merkle cells drive')
        r=raster(-1.85,h=.8)
        boxes=VGroup(phase_box(True,y=-1.85),phase_box(False,y=-1.85)).stretch(.7,1).set_color(ORANGE)
        self.play(FadeIn(r),Create(boxes),FadeIn(stimulus(-2.65)),run_time=.4)
        self.at('both phases')
        self.add(T('rat whisker follicles: Merkel cells drive both phases',26,ORANGE).move_to([0,-3.5,0]))
        # Both arrows leave the basal Merkel-cell cluster and go straight down to the boxes.
        self.play(*[GrowArrow(Arrow(cells.get_bottom(),box.get_top(),color=ORANGE,buff=.06,stroke_width=5)) for box in boxes],run_time=.4)
        self.finish()

class S21Take(SpokenScene):
    def construct(self):
        g=answer(); self.add(g)
        # Explicitly connect each coloured route to the phase it mainly supplies.
        title=VGroup(T('Two receptors feed one nerve;',30,TEXT),T('each mainly makes one phase (mouse touch domes)',28,TEXT)).arrange(DOWN,buff=.12).move_to([0,3.25,0])
        self.remove(g[8]); g.remove(g[8])
        self.add(title)
        self.at('Keep this')
        self.wait(.15)
        self.at('two receptors feed')
        self.play(Indicate(VGroup(g[1],g[2]),scale_factor=1.08),run_time=.4)
        self.at('each mainly makes')
        # Strong phase-specific outputs, with thin secondary contributions.
        purple=Arrow(g[0].disc.get_right(),g[5][0].get_left(),color=PURPLE,stroke_width=13,buff=.08)
        orange=VGroup(Line(g[0].body.get_right(),[-2.3,1.05,0],color=ORANGE,stroke_width=7),
            Line([-2.3,1.05,0],[3.25,1.05,0],color=ORANGE,stroke_width=7),
            Arrow([3.25,1.05,0],g[5][1].get_top(),color=ORANGE,stroke_width=7,buff=0,max_tip_length_to_length_ratio=.55))
        secondary=Arrow(g[0].body.get_right(),g[5][0].get_corner(UL),color=ORANGE,stroke_width=2,buff=.08)
        self.play(FadeOut(g[2]),GrowArrow(purple),Create(orange),GrowArrow(secondary),run_time=.5)
        self.finish()

class S22End(EndCard):
    LINE = 'The Merkel cell mainly holds the press.'
