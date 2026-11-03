"""Chapter 3: Built by Strengthening, and Where the Idea Stops.
COLOR MAP, inherited verbatim in meaning from scenes.old.py:
YELLOW stimulus / question; BLUE ganglion cell / spikes; PURPLE starburst;
ORANGE calcium; GREEN preferred / outward; RED null / inhibition;
TEAL transmitters; GREY structure / unknowns. Preferred right, null left.
CHAPTERS.md is left unchanged because TASK.md permits editing only scenes.py.

Geometry (arr, inhib, bar, sac) reuses the reference helpers. Connection widths,
vesicle dots and synapse dots are qualitative, never measured counts. The
current step uses I=g*(Vhold-EI), g=1, Vhold=-60, EI=-70 from the lesson's
worked model; it has no invented kinetic curve. Rasters are schematic evenly
spaced spikes: the surviving example uses the lesson's made-up 2:1 response
ratio; the nonselective example uses 1:1. No digitized experimental traces.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def arr(a,b,color=GREY,w=5,tip=.22):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=tip,
                 max_tip_length_to_length_ratio=.45,max_stroke_width_to_length_ratio=12)

def inhib(a,b,color=RED,w=5):
    a,b=np.array(a,float),np.array(b,float)
    d=(b-a)/np.linalg.norm(b-a); p=np.array([-d[1],d[0],0])
    return VGroup(Line(a,b,color=color,stroke_width=w),
                  Line(b+p*.22,b-p*.22,color=color,stroke_width=w+2))

def bar(x,base,h,w=.85,color=RED,op=.75):
    return Rectangle(width=w,height=h,stroke_color=color,fill_color=color,
                     fill_opacity=op).move_to([x,base+h/2,0])

def sac(center,R=1.25,w=3,n=6):
    c=np.array(center,float)
    soma=Circle(radius=.22,color=PURPLE,fill_color=PURPLE,fill_opacity=.9).move_to(c)
    prims=[]
    for k in range(n):
        th=k*TAU/n; d=np.array([np.cos(th),np.sin(th),0])
        parts=[Line(c+.22*d,c+R*d)]
        for fr,sgn in ((.42,1),(.7,-1)):
            p=c+d*fr*R; a=th+sgn*.6
            parts.append(Line(p,p+.3*R*np.array([np.cos(a),np.sin(a),0])))
        prims.append(VGroup(*parts).set_stroke(PURPLE,w))
    return VGroup(soma,*prims)

def lab(text,x,y,color=TEXT,size=26):
    return T(text,size,color,line_spacing=1.1).move_to([x,y,0])

def head(text,color=TEXT): return lab(text,0,3.12,color,30)

def gang(c=(0,.2,0),r=.68):
    return VGroup(Circle(radius=r,color=BLUE,fill_color=BLUE,fill_opacity=.09).move_to(c),
                  Dot(c,radius=.26,color=BLUE))

# All waveforms below are evaluated analytic schematic models, not fitted data.
# Pulse model: exp(-((t-onset)/width)**2); current: g(t)*(Vhold-EI).
# Raster model: deterministic regular events at a specified qualitative rate.

def circuit(wn=14,wp=5):
    cells=VGroup(sac((-4,0,0),R=2.0),gang(r=1.1),sac((4,0,0),R=2.0)).stretch(1.2,1)
    p=inhib([-2,0,0],[-1.2,0,0],w=wp)
    n=inhib([2,0,0],[1.2,0,0],w=wn)
    labels=VGroup(lab('preferred side',-4,-2.35,GREEN,28),lab('ganglion cell',0,-2.35,BLUE,28),lab('null side',4,-2.35,RED,28))
    return VGroup(cells,p,n,labels)

def scissors(c=(0,0,0)):
    c=np.array(c,float)
    return VGroup(Circle(radius=.17,color=TEXT).move_to(c+[-.35,-.25,0]),
                  Circle(radius=.17,color=TEXT).move_to(c+[-.35,.25,0]),
                  Line(c+[-.22,-.2,0],c+[.45,.3,0],color=TEXT,stroke_width=5),
                  Line(c+[-.22,.2,0],c+[.45,-.3,0],color=TEXT,stroke_width=5))

def mini_panel(x,title,wn=5,wp=5,empty=False):
    box=RoundedRectangle(width=6.05,height=5.5,corner_radius=.15,color=GREY,stroke_width=2).move_to([x,.15,0])
    title=lab(title,x,2.35,TEXT,30)
    if empty: return VGroup(box,title,lab('?',x,.15,YELLOW,72))
    cells=VGroup(sac((x-1.95,.3,0),R=.92),gang((x,.3,0),r=.65),sac((x+1.95,.3,0),R=.92)).stretch(1.65,1,about_point=[x,.3,0])
    p=inhib([x-1,.3,0],[x-.65,.3,0],w=wp)
    n=inhib([x+1,.3,0],[x+.65,.3,0],w=wn)
    ls=VGroup(lab('preferred',x-1.8,-1.75,GREEN,26),lab('null',x+1.8,-1.75,RED,26))
    return VGroup(box,title,cells,p,n,ls)

def prediction_one():
    return VGroup(mini_panel(-3.15,'Early: P4, P7'),mini_panel(3.15,'Later',empty=True),
                  lab('Delete preferred input, or strengthen null input?',0,-3.05,YELLOW,28),
                  lab('Pause and predict',0,3.35,YELLOW,28))

def recording_pair(x,side):
    # Same pair type twice: two separate recordings, not one three-cell experiment.
    sign=-1 if side=='preferred' else 1
    sx=x+sign*1.65; gx=x-sign*1.15
    star=sac((sx,.65,0),R=.9); gc=gang((gx,.65,0),r=.62)
    link=inhib([sx-sign*.95,.65,0],[gx+sign*.7,.65,0],w=6)
    # Narrow pipette approaches along the space between radial branches.
    pip=VGroup()
    for cx in (sx,gx):
        pip.add(Polygon([cx,.87,0],[cx-.08,1.85,0],[cx+.08,1.85,0],color=TEXT,fill_color=GREY,fill_opacity=.25))
    label=lab('starburst on '+side+' side',x,2.25,GREEN if sign<0 else RED,26)
    labels=VGroup(lab('starburst',sx,-.7,PURPLE,26),lab('ganglion',gx,-.7,BLUE,26))
    return VGroup(star,gc,link,pip,label,labels)

def pairs():
    return VGroup(recording_pair(-3.15,'preferred'),recording_pair(3.15,'null'))

def pulse_trace(x,y,width,height,onsets,col=RED,pulse_width=.035):
    t=np.linspace(0,1,550)
    values=sum((np.exp(-((t-o)/pulse_width)**2) for o in onsets),np.zeros_like(t))
    return VMobject(color=col,stroke_width=4).set_points_as_corners(
        [np.array([x+width*u,y+height*v,0]) for u,v in zip(t,values)])

def current_plot(x,y):
    t=np.linspace(0,1,301); stimulus=(t>=.25)&(t<=.72)
    g=stimulus.astype(float); current=g*(-60-(-70))
    tr=VMobject(color=RED,stroke_width=4).set_points_as_corners(
        [[x+4.7*u,y+.07*v,0] for u,v in zip(t,current)])
    axes=VGroup(Line([x,y-.12,0],[x+4.9,y-.12,0],color=GREY),
        lab('time →',x+3.95,y-.48,TEXT,26),
        lab('inhibitory current (schematic)',x+2.35,y+1.15,RED,26),
        lab('starburst cell stimulated',x+2.35,y-1.05,YELLOW,26),
        Line([x+1.18,y-.18,0],[x+3.38,y-.18,0],color=YELLOW,stroke_width=6))
    return VGroup(axes,tr)

def development_result(adult=True):
    # Ordinal heights only: Wei et al. give no numerical ratio in the lesson.
    g=VGroup(head('Inhibition from one starburst cell',TEXT),
        lab('schematic · not to scale',0,2.65,TEXT,26))
    for x,title,heights in [(-3.15,'P4 / P7',(1.15,1.15)),(3.15,'Adult',(1.15,2.5 if adult else 1.15))]:
        g.add(lab(title,x,1.95,TEXT,30),Line([x-2,-1.5,0],[x+2,-1.5,0],color=GREY))
        for xx,h,col,name in [(x-.95,heights[0],GREEN,'preferred'),(x+.95,heights[1],RED,'null')]:
            g.add(bar(xx,-1.5,h,color=col),lab(name,xx,-1.95,col,26))
    g.add(lab('Strength of inhibition from one cell',0,-2.65,TEXT,28))
    return g

def preferred_link_inset():
    # Carry this same inset across the reveal and its strengthening takeaway.
    # The stem physically joins the intact link to the adult preferred bar.
    link=inhib([1.65,.05,0],[2.75,.05,0],color=GREEN,w=5)
    stem=Line([2.2,.05,0],[2.2,-.35,0],color=GREEN,stroke_width=4)
    sc=scissors().scale(1.5).move_to([2.2,1.0,0])
    cross=VGroup(Line([1.5,.45,0],[2.9,1.55,0],color=RED,stroke_width=4),
                 Line([1.5,1.55,0],[2.9,.45,0],color=RED,stroke_width=4))
    label=lab('preferred-side\nlink',-.1,.9,GREEN,24)
    pointer=Line([1.05,.65,0],[1.65,.05,0],color=GREEN,stroke_width=3)
    return VGroup(link,stem,sc,cross,label,pointer)

def raster_rows(x=0,y=0,width=8,counts=None,spacing=1.3):
    bases=VGroup(); ticks=VGroup()
    for j,(name,col) in enumerate([('preferred motion',GREEN),('null motion',RED)]):
        yy=y-j*spacing
        bases.add(lab(name,x-width/2,yy+.5,col,26).align_to([x-width/2,0,0],LEFT),
            Line([x-width/2,yy,0],[x+width/2,yy,0],color=GREY,stroke_width=2))
        if counts:
            ticks.add(VGroup(*[Line([x-width/2+t*width,yy,0],[x-width/2+t*width,yy+.35,0],color=BLUE,stroke_width=4)
                              for t in np.linspace(.07,.93,counts[j])]))
    return VGroup(bases,ticks)

def prediction_two():
    return VGroup(head('Pause and predict',YELLOW),lab('Ganglion cell spikes',0,2.4,BLUE,30),
        raster_rows(0,1.25,10,spacing=2.4),lab('Does direction selectivity vanish?',0,-2.05,YELLOW,34),
        lab('After reduced starburst GABA release',0,-3.05,TEAL,28))

def subset_result():
    return VGroup(lab('ON-OFF ganglion cell spikes',0,1.55,BLUE,30),
        raster_rows(-3.25,.25,5,(8,4)),raster_rows(3.25,.25,5,(6,6)),
        lab('Some cells: weaker than normal',-3.25,-1.8,BLUE,26),
        lab('Other cells: lose selectivity',3.25,-1.8,TEXT,26),
        lab('Normal: far fewer null spikes',-3.25,-2.35,GREY,22),
        lab('schematic responses · not measured spike times',0,-2.85,TEXT,24))

def timing_model():
    g=VGroup(head('Surviving cells: ganglion cell spikes',BLUE),raster_rows(0,1.9,10,(8,4)))
    for x,name,delay in [(-3.2,'preferred motion',.72),(3.2,'null motion',.46)]:
        g.add(lab(name,x,-.25,GREEN if x<0 else RED,26),
              pulse_trace(x-2.5,-2.15,5,1.1 if x<0 else .75,[.43],GREEN,.095),
              pulse_trace(x-2.5,-2.15,5,.8,[delay],RED,.095),
              Line([x-2.5,-2.2,0],[x+2.5,-2.2,0],color=GREY))
    g.add(lab('tuned excitation',-4,-2.65,GREEN,26),lab('inhibition',0,-2.65,RED,26),lab('time →',4,-2.65,TEXT,26),
          lab('Same inhibition size, different timing · schematic',0,-3.3,TEXT,26))
    return g

def sign_circuit():
    g=gang((-2.35,.15,0),r=1.45); branches=VGroup()
    for yy in (-1.1,.1,1.3):
        # Physical dendrites with explicit leftward preferred-direction arrows.
        c=np.array([3.8,yy,0]); tip=np.array([-.6,yy,0])
        b=VGroup(Dot(c,radius=.18,color=PURPLE),Line(c,tip,color=PURPLE,stroke_width=5))
        for xx in (1.5,2.5):
            b.add(Line([xx,yy,0],[xx-.45,yy+.35,0],color=PURPLE,stroke_width=3))
        b.add(arr([2.85,yy,0],[1.9,yy,0],PURPLE,w=5,tip=.2))
        b.add(Dot(tip,radius=.11,color=RED),inhib(tip,[-.9,yy,0],w=7)); branches.add(b)
    return VGroup(g,branches,lab('starburst cells',3.8,2.1,PURPLE,28),
        lab('inhibitory synapses',-.5,-1.8,RED,26),
        arr([-4.2,2.9,0],[-2.5,2.9,0],GREEN),lab('ganglion preferred →',.6,2.9,GREEN,28),
        arr([3,-2.55,0],[1,-2.55,0],RED),lab('strongest inhibition prefers ←',-2.1,-2.55,RED,28))

class S00Title(TitleCard):
    TITLE='Built by Strengthening, and Where the Idea Stops'
    LESSON='Computing Motion in the Retina'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,2.2,TEAL,26),lab(self.LESSON,0,1.4,TEXT,28),
            lab('Built by Strengthening,\nand Where the Idea Stops',0,-.1,TEXT,44),
            Line([-1.4,-1.6,0],[1.4,-1.6,0],color=GOLD,stroke_width=4)); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        self.add(circuit(),head('Adult wiring'))
        self.at('Was it built'); self.play(FadeIn(lab('Cut connections, or strengthen them?',0,-3.15,YELLOW,32)),run_time=.5); self.finish()

class S02Two(SpokenScene):
    def construct(self):
        p=mini_panel(-3.15,'Pruning'); s=mini_panel(3.15,'Strengthening'); self.add(p,s)
        sc=scissors((-4.4,1.5,0))
        self.at('delete the'); self.play(FadeIn(sc),run_time=.25)
        self.play(FadeOut(p[3]),run_time=.45); self.play(FadeOut(sc),run_time=.25)
        self.at('Strengthening would'); self.play(Indicate(s[3],color=GREEN),run_time=.5)
        self.at('grow the'); self.play(s[4].animate.set_stroke(width=16),run_time=.65); self.finish()

class S03Side(SpokenScene):
    def construct(self):
        self.add(circuit(),head('Null motion arrives from the null side',RED))
        spot=Dot([5.7,2.55,0],radius=.18,color=YELLOW)
        self.at('the null side'); self.play(FadeIn(spot),GrowArrow(arr([5.4,2.55,0],[-2.5,2.55,0],RED)),run_time=.4)
        self.at('stimulus comes'); self.play(spot.animate.move_to([-2.4,2.55,0]),run_time=.8); self.finish()

class S04Wei(SpokenScene):
    def construct(self):
        p=pairs(); self.add(p,head('Wei, Hamby, Zhou and Feller · 2011'))
        self.at('recorded pairs'); self.play(Indicate(p[0][3]),Indicate(p[1][3]),run_time=.6)
        self.at('mouse retina'); self.play(FadeIn(lab('Mouse retina · separate paired recordings',0,-1.65,TEXT,28)),run_time=.4)
        self.at('Each pair was'); self.play(FadeIn(lab('One starburst cell + one ganglion cell per pair',0,-2.45,TEXT,28)),run_time=.4)
        self.add(lab('One labelled ganglion-cell type · all prefer rightward motion',0,-3.15,TEXT,26)); self.finish()

class S05Stim(SpokenScene):
    def construct(self):
        p=pairs()
        # Cell names were established in s04; leave the trace captions clear.
        for pair in p: pair.remove(pair[-1])
        self.add(p,head('Wei, Hamby, Zhou and Feller · 2011'))
        a=current_plot(-5.7,-2.15); b=current_plot(.6,-2.15)
        self.add(a[0],b[0])
        self.at('They stimulated'); self.play(Flash(p[0][0].get_center(),color=YELLOW,flash_radius=1.05),p[0][0].animate.set_color(YELLOW),run_time=.6)
        self.at('at a time'); self.play(p[0][0].animate.set_color(PURPLE),Flash(p[1][0].get_center(),color=YELLOW,flash_radius=1.05),run_time=.6)
        self.at('measured the inhibition'); self.play(Create(a[1]),run_time=.4); self.play(Create(b[1]),run_time=.4); self.finish()

class S06Early(SpokenScene):
    def construct(self):
        c=circuit(7,7); self.add(c,head('Postnatal days 4 and 7 (P4, P7)'))
        self.at('inhibition was similar'); self.play(Indicate(c[1]),Indicate(c[2]),run_time=.65)
        self.add(lab('Same pair types · similar inhibition from both sides',0,-3.15,TEXT,28)); self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        self.add(prediction_one()); self.at('later recordings'); self.play(Indicate(self.mobjects[0][1][2],color=YELLOW),run_time=.8); self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_one())
        ring=Circle(radius=.18,color=YELLOW).move_to([5.8,3.35,0]); self.play(Create(ring),run_time=5,rate_func=linear)

class S09Reveal(SpokenScene):
    def construct(self):
        d=development_result(False); self.add(d)
        self.at('grew'); self.play(Transform(d[12],bar(4.1,-1.5,2.5,color=RED)),run_time=.65)
        self.at('stayed about the same')
        self.play(Indicate(d[10],color=GREEN),FadeIn(preferred_link_inset()),run_time=.5)
        self.at('still there')
        self.play(FadeOut(d[-1]),FadeIn(lab('Preferred side still present in adult retina',0,-2.65,TEXT,28)),run_time=.25)
        self.add(lab('Wholesale loss not seen; individual synapse turnover not measured',0,-3.35,TEXT,26)); self.finish()

class S10Strong(SpokenScene):
    def construct(self):
        self.add(development_result(),preferred_link_inset())
        self.at('strengthened one side'); self.play(FadeIn(lab('Strengthening, not pruning',0,-3.35,YELLOW,30)),run_time=.5); self.finish()

class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(development_result(),preferred_link_inset(),lab('Strengthening, not pruning',0,-3.35,YELLOW,30)); self.wait(2)

class S12Mf(SpokenScene):
    def construct(self):
        title=head('Morrie and Feller · 2015')
        evidence=VGroup(lab('Quantal events: more frequent, same size',0,2.35,TEXT,30),
            lab('preferred',-4.9,1.55,GREEN,26),pulse_trace(-3.3,.7,8.9,.6,[.25,.75],GREEN,.015),
            lab('null',-4.9,-.1,RED,26),pulse_trace(-3.3,-.95,8.9,.6,np.linspace(.07,.93,8),RED,.015),
            lab('Illustrative event trains · no measured event times',0,-1.75,TEXT,26),
            lab('Frequency alone is insufficient; further tests supported the conclusion',0,-2.65,TEXT,26))
        self.add(title,evidence)
        self.at('The authors concluded')
        dots=VGroup(lab('Authors concluded: more synapses per null-side pair',0,1.9,TEXT,30),
            lab('preferred',-4.7,.65,GREEN,26),lab('null',-4.7,-.75,RED,26))
        for yy,n in [(.65,3),(-.75,8)]:
            dots.add(Line([-2.8,yy,0],[4.7,yy,0],color=GREY),*[Dot([xx,yy,0],radius=.16,color=RED) for xx in np.linspace(-2.5,4.4,n)])
        dots.add(lab('Schematic synapse dots · not measured counts',0,-1.85,TEXT,26),lab('Supported by quantal events and further tests',0,-2.6,TEXT,26))
        self.play(ReplacementTransform(evidence,dots),run_time=.55)
        self.at('not stronger'); self.play(FadeIn(lab('Same strength per synapse',0,-3.3,YELLOW,28)),run_time=.4); self.finish()

class S13Pei(SpokenScene):
    def construct(self):
        star=sac((-4,0,0),R=1.8)
        trans=chip('vesicular GABA\ntransporter',TEAL,26).move_to([-3.9,-2.35,0])
        table=VGroup(lab('Before',.5,2.25,TEXT,28),lab('After',4,2.25,TEXT,28),
            lab('GABA',2.25,1.55,TEAL,28),lab('Acetylcholine',2.25,-.65,TEAL,28))
        groups=[]
        for yy in (.75,-1.45):
            for xx in (.5,4): groups.append(VGroup(*[Dot([xx+(i-2.5)*.34,yy,0],radius=.12,color=TEAL) for i in range(6)]))
        self.add(star,table,*groups,head('Pei and colleagues · 2015 · mouse'))
        self.at('Delete the'); self.play(FadeIn(trans),run_time=.4)
        badge=chip('deleted',RED,24).move_to([-3.9,-3.3,0])
        attachment=Line(trans.get_bottom(),badge.get_top(),color=RED,stroke_width=3)
        self.at('vesicular'); self.play(FadeIn(VGroup(attachment,badge)),run_time=.35)
        self.at('release drops'); self.play(FadeOut(VGroup(*groups[1][2:])),run_time=.5)
        self.add(lab('reduced, not gone',2.25,-.0,TEAL,26))
        self.at('acetylcholine stays'); self.play(Indicate(groups[3]),FadeIn(lab('unchanged',2.25,-2.15,TEAL,26)),run_time=.55)
        self.add(lab('Illustrative release symbols',2.25,-3.1,TEXT,26)); self.finish()

class S14Predict(SpokenScene):
    def construct(self):
        self.add(prediction_two()); self.at('what would happen'); self.play(Indicate(self.mobjects[0][3],color=YELLOW),run_time=.7); self.finish()

class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_two())
        self.play(Create(Circle(radius=.18,color=YELLOW).move_to([5.8,3.15,0])),run_time=5,rate_func=linear)

class S16Reveal(SpokenScene):
    def construct(self):
        r=subset_result(); r[1][1].set_opacity(0); r[2][1].set_opacity(0)
        self.add(r,head('Inhibition loses direction tuning',RED))
        bs=VGroup(bar(-3.5,2.05,.35,color=GREEN),bar(3.5,2.05,.7,color=RED)); self.add(bs,lab('preferred',-1.9,2.3,GREEN,26),lab('null',1.9,2.3,RED,26))
        self.at('lost its direction'); self.play(Transform(bs,VGroup(bar(-3.5,2.05,.45,color=GREEN),bar(3.5,2.05,.45,color=RED))),run_time=.6)
        # Results start neutral, then reveal both outcomes at the spoken result.
        r[1][1].set_opacity(0); r[2][1].set_opacity(0)
        self.at('survived in'); self.play(r[1][1].animate.set_opacity(1),r[2][1].animate.set_opacity(1),run_time=.65)
        self.add(lab('ON-OFF = responds to light onset and offset',0,-3.35,TEXT,26)); self.finish()

class S17Rest(SpokenScene):
    def construct(self):
        m=timing_model(); self.add(m[0],m[1])
        # Axes and direction labels establish the lower panel before its traces arrive.
        for k in (2,5,6,9,10,11,12): self.add(m[k])
        self.at('tuned excitation'); self.play(Create(m[3]),Create(m[7]),run_time=.55)
        self.at('timing of residual'); self.play(Create(m[4]),Create(m[8]),FadeIn(m[13]),run_time=.6)
        self.at('Direction tuning'); self.play(Indicate(m[4],color=RED),Indicate(m[8],color=RED),run_time=.7)
        self.at('some cells can'); self.play(Transform(m[0],head('Some cells stay selective without tuned inhibition',BLUE)),run_time=.5); self.finish()

class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; m=timing_model(); m[0].become(head('Some cells stay selective without tuned inhibition',BLUE)); self.add(m); self.wait(2)

class S19Rule(SpokenScene):
    def construct(self):
        c=sign_circuit(); self.add(c)
        self.at('strongest inhibition'); self.play(Indicate(c[1],color=RED,scale_factor=1.03),run_time=.6)
        self.at('roughly the direction'); self.play(FadeIn(lab('Input prefers roughly the direction the ganglion cell ignores',0,-3.35,TEXT,26)),run_time=.5); self.finish()

class S20Scope(SpokenScene):
    def construct(self):
        rows=VGroup(*[chip(t,c,30).move_to([0,y,0]) for t,c,y in [
            ('Best established: adult mouse and rabbit',BLUE,2.25),
            ('Primate: reported in macaque;\ncircuit less studied',TEXT,0),
            ('Fly: similar computation, different cells',TEXT,-2.25)]])
        # A full centred stack from the first frame; narration highlights each claim.
        self.add(rows)
        self.at('It is best'); self.play(Indicate(rows[0],scale_factor=1.03),run_time=.5)
        self.at('The primate circuit'); self.play(Indicate(rows[1],scale_factor=1.03),run_time=.5)
        self.at('the fly uses'); self.play(Indicate(rows[2],scale_factor=1.03),run_time=.5); self.finish()

class S21End(EndCard):
    LINE='Development strengthened one side. Some cells stay selective without tuned inhibition.'
    def construct(self):
        self.add(lab('Development strengthened one side.',0,1.15,TEXT,36),
            lab('Tuned inhibition matters.\nSome cells stay selective without it.',0,-.35,TEXT,34),
            lab('biochemistrypedia.com',0,-2,TEAL,26)); self.finish()
