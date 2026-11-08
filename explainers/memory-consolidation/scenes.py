"""A Part Recalls the Whole — word-timed chapter 1.

COLOR MAP (from scenes.old.py, shared across the chapters):
YELLOW active cells; BLUE light/opsin tags; GREEN successful recall/positive links;
RED silencing/failed recall/negative links; ORANGE candidate region or wrong cue;
PURPLE controls; GOLD open question; GREY resting cells and structural outlines.
Rate heatmaps additionally use the brief's dark-blue to yellow scale.
No measured data are invented: track/maze drawings are labelled schematics.
Model equations: src/components/HopfieldPatternCompletion.astro.
"""
import itertools
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PAT = np.array([1, 1, -1, -1])
CUE = np.array([-1, 1, -1, -1])
W = np.outer(PAT, PAT) / 4
np.fill_diagonal(W, 0)
POS = [np.array(p, float) for p in [(-3.5, 2.05, 0), (3.5, 2.05, 0), (3.5, -1.65, 0), (-3.5, -1.65, 0)]]

def energy(s, w=W):
    return float(-.5 * s @ w @ s)

# Reused cell/cartoon and arrow construction from scenes.old.py.
def cell(p, r=.46):
    p = np.array([p[0], p[1], 0.])
    soma = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(p)
    stubs = VGroup()
    for ang in (100, 215, 325):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(p+d*r, p+d*(r+.17), color=GREY, stroke_width=3))
    g = VGroup(soma, stubs)
    g.soma, g.stubs, g.p = soma, stubs, p
    return g

def active(c, on=True):
    c.soma.set_stroke(YELLOW if on else GREY).set_fill(YELLOW if on else BG, 1)
    c.stubs.set_color(YELLOW if on else GREY)
    return c

def light(c, on=True):
    col = YELLOW if on else GREY
    return AnimationGroup(c.soma.animate.set_stroke(col).set_fill(col if on else BG, 1), c.stubs.animate.set_color(col))

def arr(a, b, color=GREY, w=4):
    return Arrow(a, b, buff=.6, color=color, stroke_width=w, max_tip_length_to_length_ratio=.12)

def label(txt, y=3.15, size=30, color=TEXT):
    return T(txt, size, color).move_to([0, y, 0])

def unit(i, state):
    c = Circle(.57, color=GREY, fill_color=BG, fill_opacity=1).move_to(POS[i])
    sign = M('+' if state > 0 else '−', 42, YELLOW).move_to(c)
    n = T(str(i+1), 28, GREY).next_to(c, LEFT if i in (0,3) else RIGHT, buff=.36)
    return VGroup(c, sign, n)

def network(state=PAT, links=True):
    edges = VGroup()
    if links:
        for i,j in itertools.combinations(range(4),2):
            p = W[i,j] > 0
            ln = Line(POS[i], POS[j], color=GREEN if p else RED, stroke_width=4)
            edges.add(ln if p else DashedVMobject(ln, num_dashes=18))
    nodes = VGroup(*[unit(i,s) for i,s in enumerate(state)])
    edges.set_z_index(-1)
    return VGroup(edges,nodes)

def model_note():
    return label('Teaching model • not hippocampal measurements', -3.35, 26, GREY)

def cue_ring():
    return Circle(.72, color=ORANGE, stroke_width=4).move_to(POS[0])

def opaque_chip(text,color):
    g=chip(text,color,28); g[0].set_fill(BG,1); return g

def votes(reveal=False):
    # Curved vote lanes start exactly at the source soma and avoid the links.
    starts=[POS[1]+UP*.57,POS[2]+LEFT*.57,POS[3]+LEFT*.57]
    ends=[POS[0]+UP*.72,POS[0]+np.array([.57,-.44,0]),POS[0]+LEFT*.72]
    arrows=VGroup(*[CurvedArrow(a,b,angle=angle,color=GOLD,stroke_width=5,tip_length=.22) for a,b,angle in zip(starts,ends,[.12,-.65,-.55])])
    centers=[(0,1.4,0),(1.5,-.2,0),(-5.25,.1,0)]
    tags=VGroup(*[chip('+1/4' if reveal else '?',YELLOW if reveal else GOLD,28).move_to(p) for p in centers])
    for t in tags: t[0].set_fill(BG,1)
    return VGroup(arrows,tags)


def question_frame():
    return VGroup(network(CUE), cue_ring(), votes(), label('Which way does unit 1 go?',3.15,34,GOLD), model_note())

# Track positions and spike events are a reproducible illustrative recording.
# Rates are calculated as counts / dwell time, never drawn freehand.
SPIKE_X = np.array([-4.8,-2,-1.2,-.9,-.7,-.5,-.35,-.1,.1,.3,.5,.75,1.1,1.4,3.8])
BIN_EDGES = np.linspace(-5.5,5.5,12)
COUNTS = np.histogram(SPIKE_X,BIN_EDGES)[0]
DWELL = np.ones(11)
RATES = COUNTS/DWELL
SERIES=[YELLOW,BLUE,GREEN,ORANGE,PURPLE]
def route(x):
    return np.array([x,-.6+.9*np.sin(x*.65),0])
def track():
    return RoundedRectangle(width=11.4,height=4.5,corner_radius=.3,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([0,-.45,0])
def spikes():
    return VGroup(*[Dot(route(x),radius=.085,color=RED) for x in SPIKE_X])
def bins(heat=False):
    # Exact 2-D bin counts from the same spike positions used in the recording.
    # Illustrative dwell is one second in every floor bin.
    row_edges=np.array([-2.7,-1.2,.3,1.8])
    counts=np.histogram2d(SPIKE_X,[route(x)[1] for x in SPIKE_X],bins=[BIN_EDGES,row_edges])[0]
    rates=counts/np.ones_like(counts)
    out=VGroup()
    for row,y in enumerate([-1.95,-.45,1.05]):
        for column,(a,b) in enumerate(zip(BIN_EDGES[:-1],BIN_EDGES[1:])):
            x=(a+b)/2
            col=interpolate_color(ManimColor('#15305D'),ManimColor(YELLOW),float(rates[column,row]/rates.max()))
            out.add(Rectangle(width=1,height=1.5,stroke_color=GREY,stroke_width=1,fill_color=col,fill_opacity=.95 if heat else .02).move_to([x,y,0]))
    return out


def rat(p):
    body = Ellipse(width=.65,height=.36,color=TEXT,fill_color=TEXT,fill_opacity=1).move_to(p)
    nose = Triangle(color=TEXT,fill_color=TEXT,fill_opacity=1).scale(.12).rotate(-PI/2).next_to(body,RIGHT,buff=-.08)
    tail = Line(body.get_left(),body.get_left()+LEFT*.45+DOWN*.13,color=GREY)
    return VGroup(body,nose,tail)

def sequence():
    cs=VGroup(*[cell([-4.6+2.3*i,2],.62) for i in range(5)])
    for i,c in enumerate(cs):
        c.soma.set_stroke(SERIES[i]); c.add(T(str(i+1),28,SERIES[i]).next_to(c,UP,buff=.12))
    fields=VGroup(*[Rectangle(width=2,height=.56,stroke_color=SERIES[i],fill_color=SERIES[i],fill_opacity=.3).move_to([-4.6+2.3*i,-.25-.44*i,0]) for i in range(5)])
    return cs,fields

def cluster(all_on=False,thick=2):
    # Preserve the five place cells' identities and left-to-right order.
    cs,_=sequence()
    for i,c in enumerate(cs):
        c.shift(DOWN*[3.1,.1,1.6,.1,3.1][i]); active(c,all_on)
    ed=VGroup()
    for i,j in itertools.combinations(range(5),2):
        a,b=cs[i].soma.get_center(),cs[j].soma.get_center(); d=(b-a)/np.linalg.norm(b-a)
        ed.add(Line(a+d*.62,b-d*.62,color=GREY,stroke_width=thick))
    for c in cs:
        c[-1].next_to(c.soma,DOWN,buff=.22).set_background_stroke(color=BG,width=6)
    ed.set_z_index(-1)
    return VGroup(ed,cs)

def landscape():
    # Every vertex is an exact state, segments are guides along single flips.
    states=[CUE.copy(),PAT.copy(),CUE.copy()]
    state=CUE.copy()
    for i in (1,2,3,0):
        state=state.copy(); state[i]*=-1; states.append(state)
    ax=Axes(x_range=[-.4,6.4,1],y_range=[-1.8,.7,.5],x_length=11,y_length=5.3,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.3,.1,0])
    pts=[ax.c2p(i,energy(st)) for i,st in enumerate(states)]
    curve=VMobject(color=BLUE,stroke_width=5).set_points_as_corners(pts)
    return ax,curve,pts

def landscape_labels(ax,pts):
    labs=VGroup(T('energy',28).move_to([-5.35,3.05,0]),T('0',28).next_to(ax.c2p(0,0),LEFT,buff=.18),T('−1.5',28).next_to(ax.c2p(0,-1.5),LEFT,buff=.18))
    for text,p,x,y,col in [('stored pattern',pts[1],-3.6,-2.95,GREEN),('ridge',pts[3],.4,2.95,GREY),('inverse (−, −, +, +)',pts[5],3.65,-2.85,GREY)]:
        t=T(text,28,col).move_to([x,y,0]); labs.add(t,Line(t.get_top() if y<0 else t.get_bottom(),p,buff=.12,color=col,stroke_width=2))
    labs.add(T('a quirk of this model',26,GREY).move_to([3.65,-3.4,0]))
    return labs


def maze(x=0,r=2.1,cues=4):
    pool=Circle(r,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([x,0,0])
    platform=DashedVMobject(Circle(r*.12,color=GREY,stroke_width=3),num_dashes=10).move_to([x+r*.4,r*.35,0])
    symbols=[Triangle(color=GREY).scale(.30),Square(.52,color=GREY),Star(n=5,outer_radius=.31,color=GREY),VGroup(Line(LEFT*.2,RIGHT*.2,color=GREY),Line(DOWN*.2,UP*.2,color=GREY))]
    positions=[(UP+LEFT)/np.sqrt(2),(UP+RIGHT)/np.sqrt(2),(DOWN+RIGHT)/np.sqrt(2),(DOWN+LEFT)/np.sqrt(2)]
    cue=VGroup(*[symbols[i].move_to(np.array([x,0,0])+positions[i]*(r+.43)) for i in range(cues)])
    return VGroup(pool,platform,cue)

def search_path(x=0,r=2.1,poor=False):
    # Schematic search trajectories, not quantitative plots or experimental data.
    pts=([( -.7,-.5),(-.4,.5),(.4,.8),(.6,.2),(-.5,-.3),(.3,-.7),(.7,-.4),(-.2,.4)] if poor else [(-.7,-.5),(-.3,-.1),(.3,.25),(.5,.4),(.35,.5),(.25,.3),(.45,.2),(.4,.35)])
    return VMobject(color=RED if poor else GREEN,stroke_width=6).set_points_as_corners([np.array([x+a*r,b*r,0]) for a,b in pts])

class S00Title(TitleCard):
    LESSON='Plasticity, Networks and Consolidation'
    TITLE='A Part Recalls the Whole'

    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',22,TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=T(self.TITLE,54,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        group=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.32)
        self.play(FadeIn(group),run_time=.65)
        self.finish()

class S01(SpokenScene):
    def construct(self):
        notes=VGroup(*[VGroup(Ellipse(width=.48,height=.34,fill_color=YELLOW,fill_opacity=1,color=YELLOW).move_to([x,y,0]),Line([x+.2,y,0],[x+.2,y+1.2,0],color=YELLOW,stroke_width=5)) for x,y in [(-4.8,-.9),(-3.4,-.4),(-2,-.7)]])
        corner=VGroup(Line([1,-2.8,0],[1,1.4,0],color=GREY),Line([1,-2.8,0],[6,-2.8,0],color=GREY))
        staff=VGroup(Rectangle(width=5.8,height=5.6,color=GREY).move_to([-3.35,-.4,0]),*[Line([-6,y,0],[-.7,y,0],color=GREY,stroke_opacity=.6) for y in [-1.2,-.8,-.4,0,.4]])
        extra=notes.copy().scale(.7).shift(DOWN*1.65+RIGHT*.15)
        room=VGroup(Line([1,1.4,0],[6,1.4,0],color=GREY),Line([6,1.4,0],[6,-2.8,0],color=GREY),Rectangle(width=1.4,height=2.6,color=GREY).move_to([4.8,-1.5,0]),Rectangle(width=1.7,height=1.5,color=GREY).move_to([2.5,.1,0]))
        self.add(label('Why does a part recall the whole?',3.15,38,GOLD))
        self.at('a fragment'); self.play(FadeIn(notes,shift=RIGHT*.2),Create(corner),run_time=.9)
        self.at('A few notes'); self.play(Create(staff),FadeIn(extra),Create(room),run_time=1.35)
        self.at('the rest returns'); self.play(Indicate(notes),run_time=.4); self.finish()

class S02(SpokenScene):
    def construct(self):
        mouse=rat(route(-5.2)); self.add(track(),mouse,label('Schematic recording',-3.2,26,GREY))
        inset=VGroup(cell([2.7,2.9],.26),Line([3.6,3.45,0],[2.8,3,0],color=TEXT),T('electrode',26).move_to([4.7,3.25,0]),T('one hippocampal cell',26).move_to([.2,2.9,0]))
        self.at('one hippocampal cell'); self.play(FadeIn(inset),run_time=.5)
        self.at('Each spike')
        last=route(-5.2)
        for x in SPIKE_X:
            now=route(x)
            self.play(mouse.animate.move_to(now),Create(Line(last,now,color=GREY,stroke_width=3)),run_time=.075)
            self.add(Dot(now,radius=.085,color=RED)); last=now
        self.play(mouse.animate.move_to(route(5.2)),Create(Line(last,route(5.2),color=GREY)),run_time=.15); self.finish()

class S03(SpokenScene):
    def construct(self):
        self.add(track(),spikes()); b=bins()
        self.at('Divide the floor'); self.play(Create(b),run_time=.6)
        idx=5; n=int(COUNTS[idx]); hi=Rectangle(width=1,height=1.5,color=GOLD,stroke_width=5).move_to([0,-.45,0])
        txt=T(f'{n} spikes',30,RED).move_to([2.4,2.85,0]); leader=Line(txt.get_bottom(),hi.get_top(),color=GOLD)
        self.at("each bin's spikes"); self.add(txt); self.play(Create(hi),Create(leader),run_time=.5)
        self.at('time spent there'); self.play(FadeIn(T('1 second spent',30).move_to([-2.7,2.85,0])),FadeIn(label(f'rate = {n} spikes / 1 s = {n} per second',-3.2,32)),run_time=.5); self.finish()

class S04(SpokenScene):
    def construct(self):
        self.add(track(),bins(True))
        field=T('place field',30,YELLOW).move_to([-2.2,2.7,0]); lead=Arrow(field.get_bottom(),[0,.2,0],buff=.15,color=YELLOW)
        self.at('a place field'); self.play(FadeIn(field),GrowArrow(lead),run_time=.35)
        c=cell([4,2.65],.4)
        self.at('this is a place cell'); self.play(FadeIn(c),FadeIn(T('place cell',28).next_to(c,LEFT)),run_time=.35)
        bar=VGroup(*[Rectangle(width=.35,height=.25,stroke_width=0,fill_color=interpolate_color(ManimColor('#15305D'),ManimColor(YELLOW),i/10),fill_opacity=1).move_to([-1.75+.35*i,-2.95,0]) for i in range(11)])
        self.add(bar,T('0',28).next_to(bar,LEFT),T(str(int(RATES.max())),28).next_to(bar,RIGHT),T('spikes per second',28).move_to([0,-3.5,0])); self.finish()

class S05(SpokenScene):
    def construct(self):
        cs,fs=sequence(); self.add(cs,track().stretch_to_fit_height(3).move_to([0,-1.2,0])); m=rat([-5.5,-1,0]); self.add(m)
        self.at('Each place cell'); self.play(FadeIn(fs),run_time=.4)
        self.at('fires in its own stretch')
        for i,c in enumerate(cs):
            anim=[m.animate.move_to([-4.6+2.3*i,fs[i].get_y(),0]),c.soma.animate.set_fill(SERIES[i],.95)]
            if i: anim.append(cs[i-1].soma.animate.set_fill(GREY,.25))
            self.play(*anim,run_time=.38)
        self.at('a sequence of cells'); self.add(label('One run → a sequence of cells',-3.2,32)); self.finish()

class S06(SpokenScene):
    def construct(self):
        cs,fs=sequence()
        for c in cs: c[-1].next_to(c.soma,DOWN,buff=.2)
        self.add(cs,fs,track().stretch_to_fit_height(3).move_to([0,-1.2,0]))
        outline=RoundedRectangle(width=11.6,height=2.25,corner_radius=.5,color=YELLOW).move_to([0,1.95,0])
        other=RoundedRectangle(width=6,height=2.4,corner_radius=.5,color=PURPLE).move_to([2.6,1.65,0])
        self.add(label('One run, one set of cells, fired in order',-3.2,30))
        self.at('firing in order')
        for i,c in enumerate(cs): self.play(c.soma.animate.set_fill(SERIES[i],.85),run_time=.12)
        self.play(Create(outline),run_time=.3)
        self.play(Create(other),FadeIn(T('sets can overlap',28,PURPLE).move_to([3,3.4,0])),run_time=.3)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        n=network(links=False); self.add(model_note(),label('stored pattern (+, +, −, −)',-2.75,28))
        self.at('Now store a pattern'); self.play(FadeIn(n),run_time=.75)
        full=network()
        q=label('agree: positive link',3.15,29,GREEN)
        self.at('Agreeing units'); self.play(Create(VGroup(*[e for e in full[0] if not isinstance(e,DashedVMobject)])),FadeIn(q),run_time=.6)
        self.at('disagreeing units'); self.play(Create(VGroup(*[e for e in full[0] if isinstance(e,DashedVMobject)])),ReplacementTransform(q,label('disagree: negative link',3.15,29,RED)),run_time=.6)
        self.add(n[1],opaque_chip('+1/4',GREEN).move_to([0,2.05,0]),opaque_chip('−1/4',RED).move_to([3.5,.2,0])); self.finish()

class S08(SpokenScene):
    def construct(self):
        n=network(); self.add(n,model_note())
        self.at('Start from'); self.play(FadeIn(label('cue (−, +, −, −)',3.15,32,ORANGE)),run_time=.4)
        self.at('Unit 1 wrong'); self.play(Transform(n[1][0],unit(0,-1)),Create(cue_ring()),run_time=.5); self.finish()

class S09(SpokenScene):
    def construct(self):
        self.add(network(CUE),cue_ring(),model_note())
        v=votes(); self.at('Each partner'); self.play(LaggedStart(*[Create(a) for a in v[0]],lag_ratio=.15),run_time=.9)
        formula=label('vote = link × state',-2.65,27)
        self.at('link time state'); self.play(FadeIn(v[1]),FadeIn(formula),run_time=.5)
        self.at('Which way'); self.play(FadeIn(label('Which way does unit 1 go?',3.15,34,GOLD)),FadeOut(formula),run_time=.5); self.finish()

class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question_frame()); self.wait(5)

class S11(SpokenScene):
    def construct(self):
        n=network(CUE); v=votes(); q=label('Which way does unit 1 go?',3.15,34,GOLD)
        ring=cue_ring(); self.add(n,ring,v,q,model_note())
        self.at('All three votes'); self.play(Transform(v[1],votes(True)[1]),ReplacementTransform(q,label('field = +3/4',3.15,34,YELLOW)),run_time=.6)
        assert np.isclose(W[0]@CUE,.75)
        self.at('Unit 1 flips'); self.play(Transform(n[1][0],unit(0,1)),FadeOut(ring),run_time=.55)
        self.at('the stored pattern'); self.add(label('✓ stored pattern (+, +, −, −)',-2.75,30,GREEN)); self.play(FadeOut(v),run_time=.25); self.finish()

def violated_picture():
    n=network(CUE); marks=VGroup()
    for k,(i,j) in enumerate(itertools.combinations(range(4),2)):
        bad=W[i,j]*CUE[i]*CUE[j]<0; n[0][k].set_color(RED if bad else GREEN)
        if bad:
            a=.32 if j==2 else .5
            marks.add(T('×',52,RED).move_to(POS[i]*(1-a)+POS[j]*a).set_background_stroke(color=BG,width=8))
    return n,marks

class S12(SpokenScene):
    def construct(self):
        n,marks=violated_picture(); key=label('violated +1/4, satisfied −1/4',3.15,30)
        read=label('Cue: 3 violated • energy 0',-2.6,30,RED)
        self.add(n,marks,key,read,model_note())
        self.at('violates three'); self.play(Indicate(marks),run_time=.5)
        self.at('the stored pattern None'); target=network(); target[0].set_color(GREEN)
        self.play(Transform(n,target),FadeOut(marks),ReplacementTransform(read,label('Stored: 0 violated • energy −1.5',-2.6,30,GREEN)),run_time=.35); self.wait(max(0,7.6-self.elapsed())); self.finish()

class S12b(SpokenScene):
    def construct(self):
        n=network(); self.add(n)
        ax,curve,pts=landscape(); ball=Dot(pts[0]+UP*.15,radius=.15,color=YELLOW)
        self.at('Each flip removes'); self.play(n.animate.scale(.09).move_to(pts[0]+UP*.15),run_time=.45)
        self.play(ReplacementTransform(n,ball),Create(ax),Create(curve),FadeIn(landscape_labels(ax,pts)),run_time=.75)
        self.at('the state rolls'); self.play(MoveAlongPath(ball,Line(pts[0]+UP*.15,pts[1]+UP*.15)),run_time=1.1)
        self.finish()

class S13(SpokenScene):
    def construct(self):
        ax,curve,pts=landscape(); old=VGroup(ax,curve,landscape_labels(ax,pts),Dot(pts[1]+UP*.15,radius=.15,color=YELLOW)); c=cluster()
        self.add(old)
        self.at('So here is'); self.play(FadeOut(old),FadeIn(c),run_time=.65)
        self.at('Learning strengthens links'); self.play(c[0].animate.set_stroke(GREEN,width=8),*[light(x) for x in c[1]],run_time=1)
        self.at('active together'); self.add(label('Active together → stronger links',-2.85,34)); self.finish()

class S14(SpokenScene):
    def construct(self):
        c=cluster(True,8); c[0].set_color(GREEN); self.add(c)
        self.at('Later'); self.play(*[light(x,False) for x in c[1]],run_time=.3)
        self.at('a fragment'); self.add(label('A close-enough fragment pulls the rest back on',-2.85,32,YELLOW)); self.play(light(c[1][0]),light(c[1][1]),run_time=.4)
        self.at('pulls the rest'); self.play(LaggedStart(*[light(x) for x in c[1][2:]],lag_ratio=.3),ShowPassingFlash(c[0].copy().set_color(YELLOW),time_width=.5),run_time=1)
        self.finish()

class S15(SpokenScene):
    def construct(self):
        c=cluster(True,8); c[0].set_color(GREEN); self.add(c)
        self.at('In this model'); self.add(label('In the model, recall =',-2.45,44,GREEN),label('the group completing itself',-3.15,44,GREEN)); self.finish()



class S16(SpokenScene):
    def construct(self):
        # Stylized curled anatomical outline, deliberately labelled schematic.
        outline=VMobject(color=GREY,stroke_width=4).set_points_smoothly([[-5,-1,0],[-5,1,0],[-3.5,2.5,0],[0,2.7,0],[3,2,0],[5,0,0],[4,-2,0],[1,-2.5,0],[-1,-1.7,0],[0,-.7,0],[2,-.8,0],[3,-.1,0],[2,1,0],[-1,1.2,0],[-3,.3,0],[-5,-1,0]])
        ca=Ellipse(width=7,height=2.8,color=ORANGE,fill_color=ORANGE,fill_opacity=.12).move_to([0,.4,0])
        cs=VGroup(*[cell(q,.43) for q in [(-2.5,.3),(-.8,1.1),(1.3,.9),(2.3,-.4),(-.4,-.6)]])
        self.add(outline,ca,cs,label('CA3 • schematic hippocampus',3.2,30),label('Modelled as an attractor network',-3.15,32))
        self.at('has dense recurrent')
        arrows=VGroup(*[CurvedArrow(cs[i].p,cs[j].p,angle=.55,color=GREEN,stroke_width=4,tip_length=.18).scale(.72,about_point=(cs[i].p+cs[j].p)/2) for i,j in [(0,1),(1,2),(2,3),(3,4),(4,0),(1,4),(4,1)]])
        loop=CurvedArrow([-2.75,.6,0],[-2.15,.65,0],angle=-4.9,color=GREEN,tip_length=.18)
        self.play(Create(arrows),Create(loop),run_time=1.1); self.finish()

def groups():
    pts=[(-4.7,1.1),(-3.3,2),(-2.2,.4),(-.7,1.6),(.8,.3),(1.8,1.9),(2.6,-.6),(.1,-1.5),(-3.7,-1.1)]
    cs=VGroup(*[cell(p,.43) for p in pts])
    sets=[(0,1,2,8),(2,3,4,7),(4,5,6,7),(2,7,8)]
    edges=set()
    for group in sets:
        edges.update(itertools.combinations(group,2))
    ed=VGroup(*[Arrow(cs[i].p,cs[j].p,buff=.56,color=GREEN,stroke_width=3,tip_length=.16) for i,j in sorted(edges)])
    outlines=VGroup(*[Ellipse(width=w,height=h,color=GREY,stroke_opacity=.35).move_to([x,y,0]) for x,y,w,h in [(-3.6,.4,3.9,4.6),(-.8,.3,4.4,4.4),(1.5,.3,4.4,4.8),(-2,-.8,4.6,3.5)]])
    return VGroup(outlines,ed,cs)

def dial(text='threshold',count=0):
    center=np.array([4.8,-.2,0]); cir=Circle(1.15,color=GREY).move_to(center)
    angle=PI*.85-count*PI*.18
    needle=Line(center,center+.9*np.array([np.cos(angle),np.sin(angle),0]),color=ORANGE,stroke_width=6)
    return VGroup(cir,needle,T(text,30).move_to([4.8,-1.8,0]),T(f'{count} active',28,YELLOW).move_to([4.8,-2.4,0]))

class S17(SpokenScene):
    def construct(self):
        g=groups(); g.scale(.8).shift(LEFT*.6); d=dial('inhibition',0)
        self.add(g,d,label('The idea has limits',3.45,34,GOLD),T('excitatory only',30,GREEN).move_to([-1,2.7,0]),label('Some models, many stored groups',-3.1,30))
        self.wait(1.7)
        self.play(light(g[2][0]),Transform(d,dial('inhibition',1)),run_time=.6)
        self.at('connections are excitatory'); self.play(g[1].animate.set_stroke(width=4),light(g[2][1]),Transform(d,dial('inhibition',2)),run_time=.7)
        self.at('inhibition helps'); self.play(Indicate(d),run_time=.7); self.finish()

def failure_group(x):
    cs=VGroup(*[cell([x+a,b],.38) for a,b in [(-1.7,.3),(-.8,1.2),(0,-.2),(.85,1.1),(1.7,-.3),(.6,-1.5)]])
    ed=VGroup(*[Arrow(cs[i].p,cs[j].p,buff=.48,color=GREEN,stroke_width=3,tip_length=.15) for i,j in [(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(5,3)]])
    outlines=VGroup(RoundedRectangle(width=3.1,height=3.1,corner_radius=.6,color=GREY,stroke_opacity=.35).move_to([x-.85,.5,0]),RoundedRectangle(width=3.1,height=4,corner_radius=.6,color=GREY,stroke_opacity=.35).move_to([x+.85,-.2,0]))
    return VGroup(outlines,ed,cs)

class S17b(SpokenScene):
    def construct(self):
        left=failure_group(-3.25); right=failure_group(3.25)
        self.add(left,right,Line([0,-2.6,0],[0,2.1,0],color=GREY),label('Possible failure modes • some models',3.25,32),T('Low threshold',30,ORANGE).move_to([-3.25,2.55,0]),T('High threshold',30,ORANGE).move_to([3.25,2.55,0]))
        self.at('a low threshold'); self.play(light(left[2][0]),run_time=.4)
        self.at('activity spread'); self.play(light(left[2][1]),light(left[2][2]),run_time=.5)
        self.at('other groups'); self.play(LaggedStart(*[light(c) for c in left[2][3:]],lag_ratio=.18),FadeIn(T('spreads beyond its group',28,YELLOW).move_to([-3.25,-2.95,0])),run_time=.65)
        self.at('a high one'); self.play(light(right[2][0]),run_time=.4)
        self.at('unable to recruit'); self.play(light(right[2][0],False),FadeIn(T('Weak cue fades',30,RED).move_to([3.25,-2.95,0])),run_time=.6); self.wait(max(0,9.8-self.elapsed())); self.finish()

class S18(SpokenScene):
    def construct(self):
        g=groups(); g.scale(.8).shift(LEFT*.6); d=dial('inhibition',0)
        self.add(g,d,label('One possible retrieval • model network',3.25,30),label('More active cells → more inhibition',-3.1,30))
        self.at('Feedback inhibition'); self.play(light(g[2][0]),Transform(d,dial('inhibition',1)),run_time=.5)
        self.at('tracks the total'); self.play(light(g[2][1]),Transform(d,dial('inhibition',2)),run_time=.6)
        self.at('keep activity sparse'); self.play(light(g[2][2]),Transform(d,dial('inhibition',3)),run_time=.7)
        self.at('With suitable connections'); self.play(Indicate(VGroup(*g[2][:3])),run_time=.8)
        self.at('a fragment'); self.play(Indicate(g[2][0]),run_time=.5)
        self.at('complete its own pattern'); self.play(light(g[2][8]),Transform(d,dial('inhibition',4)),FadeIn(T('Only its stored group stays active',28,YELLOW).move_to([-1,-2.45,0])),run_time=.8); self.finish()



# Multi-pattern Hebbian energy, same equation generalized by summing outer products.
# Three orthogonal 24-unit patterns; their majority mixture is a stable false memory.
def loaded_landscape():
    # Three 24-unit Hebbian memories; the fourth changes the mixture basins.
    base=np.array(list(itertools.product([-1,1],repeat=3))).T
    extra=np.array([1,-1,-1,-1,-1,1,1,1])
    oldmix=np.sign(base.sum(axis=0))
    newmix=np.sign(base[0]+base[1]+extra)
    before_patterns=np.tile(base,(1,3))
    after_patterns=np.tile(np.vstack([base,extra]),(1,3))
    def weights(pats):
        w=pats.T@pats/24; np.fill_diagonal(w,0); return w
    wb,wa=weights(before_patterns),weights(after_patterns)
    a=np.tile(base[0],3); b=np.tile(base[1],3)
    oldmix=np.tile(oldmix,3); newmix=np.tile(newmix,3)
    assert np.all(oldmix*(wb@oldmix)>0) and np.any(oldmix*(wa@oldmix)<0)
    assert np.all(newmix*(wa@newmix)>0)
    start=a.copy(); start[0]*=-1; start[1]*=-1
    states=[start]; indices=[]
    for target in (a,oldmix,newmix,b):
        st=states[-1].copy()
        # Prefer lower next-state energy while preserving single-unit steps.
        while np.any(st!=target):
            candidates=[]
            for k in np.where(st!=target)[0]:
                q=st.copy(); q[k]=target[k]; candidates.append((energy(q,wa),k,q))
            _,_,st=min(candidates,key=lambda x:x[0]); states.append(st.copy())
        indices.append(len(states)-1)
    st=states[-1].copy()
    for k in (0,1):
        st=st.copy(); st[k]*=-1; states.append(st)
    ax=Axes(x_range=[-1,len(states),2],y_range=[-14,-4,2],x_length=11,y_length=4.6,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([.3,-.1,0])
    ax.x_axis.set_opacity(0)
    ax.y_axis.shift(LEFT*.3)
    def graph(w):
        pts=[ax.c2p(k,energy(st,w)) for k,st in enumerate(states)]
        return VMobject(color=BLUE,stroke_width=5).set_points_as_corners(pts),pts
    before,bp=graph(wb); after,pts=graph(wa)
    return ax,before,after,pts,indices,bp

class S19(SpokenScene):
    def construct(self):
        ax,before,after,pts,idx,bp=loaded_landscape()
        self.add(ax,before,label('Adding stored patterns • 24-cell model',3.45,30),T('energy (relative scale)',26).move_to([-3.8,2.7,0]),label('Successive single-cell flips →',-3.5,26,GREY))
        olddot=Dot(bp[idx[1]],radius=.08,color=GREY)
        old=T('old valley',26,GREY).next_to(olddot,UP,buff=.3)
        self.add(olddot,old)
        # The stored basin is the downhill interval around the first minimum.
        y=-2.65
        span=Line([bp[0][0],y,0],[bp[6][0],y,0],color=GREEN,stroke_width=7)
        spantext=T('stored basin',26,GREEN).next_to(span,DOWN,buff=.12)
        self.add(span,spantext)
        middle=before.copy().interpolate(before,after,.4)
        middle_dot=Dot(.6*bp[idx[1]]+.4*pts[idx[1]],radius=.08,color=GREY)
        t=T('spurious mixture',27,ORANGE).move_to([pts[idx[2]][0],-3,0])
        self.at('Storing more patterns'); self.play(Transform(before,middle),Transform(olddot,middle_dot),run_time=1.4)
        self.at('reshapes the landscape')
        # Keep deforming across both three-second samples; shrink the displayed
        # downhill interval and reveal the new valley at their narration times.
        self.play(Transform(before,after),olddot.animate.move_to(pts[idx[1]]),
            Transform(old,T('old valley flattened',26,GREY).move_to([pts[idx[1]][0],1.2,0])),
            Succession(Wait(1.76),AnimationGroup(Transform(span,Line([pts[0][0],y,0],[pts[3][0],y,0],color=GREEN,stroke_width=7)),spantext.animate.move_to([pts[2][0],-3,0]),run_time=.6),Wait(1.54)),
            Succession(Wait(2.66),FadeIn(t,run_time=.35),Wait(.89)),run_time=3.9)
        k=idx[2]-2; q=idx[0]+1
        poor=Dot(pts[k]+UP*.15,radius=.15,color=ORANGE); good=Dot(pts[q]+UP*.15,radius=.15,color=YELLOW)
        poorlabel=T('poor cue',26,ORANGE).next_to(poor,RIGHT,buff=.2)
        goodlabel=T('good cue',26,YELLOW).next_to(good,UP,buff=.3)
        self.at('A poor cue'); self.add(poor,good,poorlabel,goodlabel)
        self.at('roll into the wrong'); self.play(MoveAlongPath(poor,VMobject().set_points_as_corners([p+UP*.15 for p in pts[k:idx[2]+1]])),MoveAlongPath(good,Line(pts[q]+UP*.15,pts[idx[0]]+UP*.15)),FadeOut(poorlabel),FadeOut(goodlabel),run_time=1.1); self.finish()


class S20(SpokenScene):
    def construct(self):
        m=maze(r=2.35); self.add(m,label('NMDA receptors deleted',3.5,30),label('Water maze • schematic',-3.5,26,GREY))
        pt=m[1].get_center(); pl=T('hidden platform',28).move_to([4.5,1.7,0]); self.add(pl,Line(pl.get_left(),pt,color=GREY,buff=.2))
        self.at('pyramidal cells'); self.add(label('CA3 pyramidal cells only',2.95,28))
        mouse=rat([-1.65,-1.18,0]).scale(.6); self.add(mouse)
        self.at('learned a water maze'); path=search_path(r=2.35); self.play(Create(path),MoveAlongPath(mouse,path),run_time=1)
        self.at('normally'); self.add(T('learned normally',32,GREEN).move_to([4.3,-2.7,0])); self.wait(max(0,8.7-self.elapsed())); self.finish()

class S21(SpokenScene):
    def construct(self):
        a=maze(-3.3,2.25,4); b=maze(3.3,2.25,4)
        self.add(a,b,T('All cues',32).move_to([-3.3,3.3,0]))
        for m,x in [(a,-3.3),(b,3.3)]:
            t=T('hidden platform',26).move_to([x,-2.65,0]); self.add(t,Line(t.get_top(),m[1].get_center(),buff=.18,color=GREY,stroke_opacity=.5))
        self.at('recalled the platform'); self.play(Create(search_path(-3.3,2.25)),FadeIn(T('normal recall',30,GREEN).move_to([-3.3,-3.25,0])),run_time=.7)
        self.at('With few'); self.play(FadeOut(VGroup(*b[2][1:])),run_time=.3)
        self.add(T('Few cues',32).move_to([3.3,3.3,0]))
        self.at('searched poorly'); self.play(Create(search_path(3.3,2.25,True)),FadeIn(T('impaired search',30,RED).move_to([3.3,-3.25,0])),run_time=.65); self.finish()

class S22(SpokenScene):
    def construct(self):
        a=VGroup(maze(-4.45,1.65,4),search_path(-4.45,1.65))
        b=VGroup(maze(0,1.65,1),search_path(0,1.65,True))
        ax,curve,pts=landscape()
        plot=VGroup(ax,curve).stretch_to_fit_width(3.4).stretch_to_fit_height(3.65).move_to([4.45,-.1,0])
        self.add(a,b,plot,label('Consistent with completion in CA3',3.4,34,GOLD),label('Inferred from behaviour • not recorded in CA3',-3.15,32,GOLD))
        for text,x in [('All cues',-4.45),('Few cues',0),('Model energy',4.45)]: self.add(T(text,28).move_to([x,2.45,0]))
        self.add(T('normal',30,GREEN).move_to([-4.45,-2.3,0]),T('impaired',30,RED).move_to([0,-2.3,0]),T('energy',25).move_to([3.15,1.95,0]),T('stored',25,GREEN).move_to([3.35,-2.3,0]),T('inverse',25,GREY).move_to([5.45,-2.3,0]))
        self.finish()



TAKEAWAY='A close-enough cue can recall the whole,\nif the network is not too full.'
def takeaway_card():
    return VGroup(T('In this model',30,GREY),T(TAKEAWAY,40,font=TITLE_FONT,line_spacing=1.25),T('biochemistrypedia.com',28,TEAL)).arrange(DOWN,buff=.6)

class S23(SpokenScene):
    def construct(self):
        self.add(takeaway_card()); self.finish()


class S24End(EndCard):
    LINE=TAKEAWAY
    def construct(self):
        self.add(takeaway_card()); self.finish()
