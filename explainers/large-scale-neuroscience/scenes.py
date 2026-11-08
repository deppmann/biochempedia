"""Chapter 1: schematic diagrams, no recorded or fitted traces.
COLOR MAP: GREY physical sites/probe and neutral geometry; CHANNEL amber readout channels;
YELLOW inferred units; BLUE/PINK/LAVENDER/PEACH source-neuron identities;
WHITE discrete spike ticks (identity ticks carry a coloured source dot);
GREEN calcium fluorescence; LIME calcium entry; SENSOR steel-grey sensor;
TEAL branding only; TEXT white instructions;
PURPLE atlas (cluster identities: purple, cream, cobalt); CORAL synapse marks;
ORANGE animals; GOLD questions/rules; RED unjustified equivalence.
The calcium trace is a normalized first-order cascade, in relative time only.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PINK='#E58FB5'
PURPLE='#B58CD9'
CORAL='#F07878'
SKY='#4069F5'
CREAM='#F4F1AB'
LIME='#C4D966'
SENSOR='#AAB9CA'
CHANNEL='#D69A59'
SOURCE=[BLUE,PINK,'#A69AF5','#EAC09B']
SPIKE='#FFFFFF'

def bchip(text,color=BLUE,size=28):
    c=chip(text,color,size=size)
    c[0].set_fill(BG,1)
    return c

def neuron(color=BLUE,r=.55):
    soma=Circle(radius=r,color=color,fill_color=color,fill_opacity=.25,stroke_width=4)
    branches=VGroup(*[Line(r*np.array([np.cos(a),np.sin(a),0]),(r+.3)*np.array([np.cos(a),np.sin(a),0]),color=color,stroke_width=4) for a in [PI/2,5*PI/6,7*PI/6,3*PI/2]])
    return VGroup(soma,branches)

def probe(active=False):
    x=-4.5
    shank=Polygon([x-.55,3.35,0],[x+.55,3.35,0],[x+.55,-2.95,0],[x,-3.45,0],[x-.55,-2.95,0],color=GREY,fill_color=GREY,fill_opacity=.1)
    # Schematic packing only: 960 distinct marks, not a physical site-layout claim.
    sites=VGroup(*[Rectangle(width=.13,height=.014,stroke_width=0,fill_opacity=1,fill_color=CHANNEL if active and row<96 else GREY).move_to([x+(col-1.5)*.22,3.15-row*.025,0]).set_opacity(1 if not active or row<96 else .12) for row in range(240) for col in range(4)])
    return VGroup(shank,sites)

def opening_label():
    return VGroup(M('960',78,GREY),T('recording sites',36,GREY)).arrange(DOWN,buff=.2).move_to([1.25,2.1,0])

def opening_question():
    return VGroup(T('Does it record',42),T('960 neurons?',54,BLUE)).arrange(DOWN,buff=.3).move_to([1.25,-.35,0])

def schematic():
    return T('schematic site layout',26,GREY).move_to([-3.9,-3.65,0])

def ladder(labels=('sites','channels','units','neurons'),colors=(GREY,CHANNEL,YELLOW,BLUE)):
    rails=VGroup(*[Line([x,-2.9,0],[x,2.9,0],color=GREY) for x in [-2.6,2.6]])
    rows=VGroup(*[VGroup(Line([-2.6,y,0],[2.6,y,0],color=c),bchip(l,c,36).move_to([0,y,0])) for y,l,c in zip([-2.4,-.8,.8,2.4],labels,colors)])
    return rails,rows

def mouse():
    # A compact side profile: rounded back, pointed nose, small ear above the head.
    outline=VMobject(color=ORANGE,stroke_width=3,fill_color=ORANGE,fill_opacity=.08)
    outline.start_new_path([-1.05,-.25,0])
    outline.add_cubic_bezier_curve_to([-1.3,1.05,0],[-.1,1.18,0],[.25,.88,0])
    outline.add_cubic_bezier_curve_to([.2,1.3,0],[.65,1.3,0],[.65,.72,0])
    outline.add_cubic_bezier_curve_to([.75,.5,0],[.9,.15,0],[1.2,-.05,0])
    outline.add_cubic_bezier_curve_to([1.05,-.3,0],[.65,-.45,0],[.45,-.65,0])
    outline.add_cubic_bezier_curve_to([-.05,-1.0,0],[-.95,-.95,0],[-1.05,-.25,0])
    ear=CubicBezier([.35,.9,0],[.35,1.08,0],[.53,1.08,0],[.53,.9,0],color=ORANGE,stroke_width=2)
    eye=Dot([.85,.1,0],radius=.035,color=ORANGE)
    tail=VMobject(color=ORANGE,stroke_width=3)
    tail.start_new_path([-1.05,-.25,0])
    tail.add_cubic_bezier_curve_to([-1.65,-.45,0],[-1.65,.15,0],[-1.45,.5,0])
    tail.add_cubic_bezier_curve_to([-1.28,.8,0],[-1.45,1.1,0],[-1.7,1.02,0])
    # Sample the Beziers so scaling uses the visible outline rather than control handles.
    for path in (outline,ear,tail):
        points=[path.point_from_proportion(a) for a in np.linspace(0,1,200)]
        path.set_points_as_corners(points)
    return VGroup(outline,ear,eye,tail)

def quality_badge():
    label=T('quality score',26,GREY)
    track=Rectangle(width=1.8,height=.16,color=GREY,stroke_width=1)
    bar=Rectangle(width=1.25,height=.12,color=GREY,stroke_width=0,fill_opacity=1).align_to(track,LEFT)
    gauge=VGroup(track,bar)
    content=VGroup(label,gauge).arrange(DOWN,buff=.14)
    box=RoundedRectangle(width=content.width+.35,height=content.height+.3,corner_radius=.12,color=GREY,fill_color=BG,fill_opacity=1)
    return VGroup(box,content)

def rule_box(stage=1):
    h=3.0 if stage==1 else 5.8
    box=RoundedRectangle(width=11.8,height=h,corner_radius=.2,color=GOLD)
    y= .65 if stage==1 else 2.1
    lines=VGroup(T('Each number is a proxy.',44,GOLD).move_to([0,y,0]),T('One or more steps from your claim.',34).move_to([0,y-1.15,0]))
    if stage>=2:
        lines.add(T('Name each step.',38,TEXT).move_to([0,-.25,0]),T('Trust it only as far as it has been measured\nin conditions like yours.',32,line_spacing=1.3).move_to([0,-1.75,0]))
    return VGroup(box,lines)

def table():
    xs=[-4.9,-1.65,3.0]
    headings=VGroup(*[T(t,26,GREY).move_to([x,3.15,0]) for t,x in zip(['METHOD','NUMBER','STEP TO YOUR CLAIM'],xs)])
    specs=[('Probe','units','sites → channels\n→ units → neurons',YELLOW),('Calcium imaging','fluorescence','light → calcium → spikes',GREEN),('Any recording','units / trials','units → animals',ORANGE),('Atlas','clusters','cluster → cell type',PURPLE),('Connectome','synapses','count → strength',CORAL)]
    rows=VGroup()
    for i,(a,b,c,col) in enumerate(specs):
        y=1.95-i*1.12
        rows.add(VGroup(T(a,26,col).move_to([xs[0],y,0]),T(b,26,col).move_to([xs[1],y,0]),T(c,26,line_spacing=.8).move_to([xs[2],y,0]),Line([-6.3,y-.55,0],[6.3,y-.55,0],color=GREY,stroke_opacity=.4)))
    return VGroup(headings,rows)

# h(t) = exp(-t/tau_decay)-exp(-t/tau_rise), t>=0.
# Relative units only: the slow response illustrates lag/blur, not GCaMP kinetics.
def response_plot():
    x0=-4.8; y0=-2.45; sx=1.05
    axis=Arrow([-6,y0,0],[3.05,y0,0],buff=0,color=GREY,stroke_width=2)
    tick=Line([x0,y0,0],[x0,2.55,0],color=SPIKE,stroke_width=4)
    t=np.linspace(0,7.1,360); delayed=np.maximum(t-.85,0)
    h=np.exp(-delayed/1.8)-np.exp(-delayed/.42); h/=h.max()
    curve=VMobject(color=GREEN,stroke_width=5).set_points_as_corners([[-6,y0,0],[x0,y0,0]]+[[x0+sx*a,y0+4.25*b,0] for a,b in zip(t,h)])
    peak=.42*1.8/(1.8-.42)*np.log(1.8/.42)
    xp=x0+sx*(.85+peak)
    bracket=VGroup(Line([x0,2.9,0],[xp,2.9,0],color=GOLD),Line([x0,2.78,0],[x0,3.02,0],color=GOLD),Line([xp,2.78,0],[xp,3.02,0],color=GOLD),T('lag',28,GOLD).move_to([(x0+xp)/2,3.35,0]))
    labels=VGroup(T('spike',30,SPIKE).move_to([-5.7,2.4,0]),T('glow',32,GREEN).move_to([-.1,1.45,0]),T('relative time →',26,GREY).move_to([1.1,-2.95,0]),T('spike: a few milliseconds   •   glow: far slower',26).move_to([-1.6,-3.5,0]),T('schematic',26,GREY).move_to([1.6,3.15,0]))
    return VGroup(axis,tick,curve,bracket,labels)

def kettle():
    # Large stovetop kettle: attached arch handle and a closed, tapered spout.
    body=VMobject(color=GREY,fill_color=GREY,fill_opacity=.2,stroke_width=4)
    body.start_new_path([3.75,-1.65,0])
    body.add_cubic_bezier_curve_to([3.25,-.7,0],[3.65,.6,0],[4.1,.75,0])
    body.add_line_to(np.array([5.05,.75,0]))
    body.add_cubic_bezier_curve_to([5.65,.4,0],[5.8,-.8,0],[5.35,-1.65,0])
    body.close_path()
    spout=Polygon([5.45,-.7,0],[6.35,.85,0],[6.6,.85,0],[5.55,-1.3,0],color=GREY,fill_color=BG,fill_opacity=1,stroke_width=4)
    lid=VGroup(Line([4.0,.8,0],[5.2,.8,0],color=GREY,stroke_width=4),Dot([4.6,.98,0],radius=.12,color=GREY))
    handle=CubicBezier([3.85,.35,0],[3.05,2.7,0],[6.0,2.7,0],[5.3,.35,0],color=GREY,stroke_width=7)
    steam=VGroup()
    for i in range(4):
        puff=VMobject(color=GREY,stroke_width=3)
        x=6.25-.15*(i%2); y=1.15+i*.58
        puff.start_new_path([x,y,0])
        puff.add_cubic_bezier_curve_to([x-.35,y+.12,0],[x+.3,y+.3,0],[x-.05,y+.43,0])
        steam.add(puff)
    icon=VGroup(body,spout,lid,handle,steam)
    stove=VGroup(Line([3.5,-2.45,0],[6.6,-2.45,0],color=GREY),Line([3.9,-2.45,0],[3.9,-1.8,0],color=SPIKE,stroke_width=4),T('stove on',26).move_to([4.8,-2.95,0]))
    return VGroup(icon,stove)

class S00Title(TitleCard):
    LESSON='Recording Many Neurons: Imaging, Arrays and Atlases'
    TITLE='One Question for Every Number'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('Recording Many Neurons:\nImaging, Arrays and Atlases',28,GREY,line_spacing=1),fit(T(self.TITLE,46,font=TITLE_FONT),11.8),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6); self.finish()

class S01N(SpokenScene):
    def construct(self):
        p=probe(); label=opening_label(); q=opening_question()
        self.add(p[0],schematic())
        self.at('probe carries')
        count=ValueTracker(0)
        num=M('0',78,GREY).move_to(label[0])
        num.add_updater(lambda m:m.become(M(str(int(count.get_value())),78,GREY).move_to(label[0])))
        self.add(num)
        self.play(LaggedStart(*[FadeIn(VGroup(*p[1][i:i+40])) for i in range(0,960,40)],lag_ratio=.04),count.animate.set_value(960),run_time=1.5)
        num.clear_updaters()
        self.at('recording sites'); self.play(FadeIn(label[1]),run_time=.3)
        self.at('Does it record'); self.play(FadeIn(q),run_time=.4); self.finish()

class S02Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(probe(),opening_label(),opening_question(),schematic())
        ring=Circle(radius=.5,color=GOLD).move_to([1.25,-2.55,0])
        self.add(ring)
        self.play(Uncreate(ring),rate_func=linear,run_time=5)

class S03N(SpokenScene):
    def construct(self):
        p=probe(); q=opening_question(); label=opening_label(); self.add(p,q,label,schematic())
        answer=T('Not necessarily.',42,GOLD).move_to([1.25,-.4,0])
        self.at('Not necessarily')
        self.play(Transform(p,probe(True)),FadeOut(q),FadeIn(answer),run_time=.6)
        self.at('reads out only')
        count=VGroup(M('384',78,CHANNEL),T('read out at once',36,CHANNEL)).arrange(DOWN,buff=.2).move_to(label)
        self.play(FadeOut(label),FadeIn(count),run_time=.5)
        self.at('Each one read out')
        self.play(FadeOut(answer),FadeIn(bchip('384 channels',CHANNEL,40).move_to([1.25,-1,0])),run_time=.4); self.finish()

class S04N(SpokenScene):
    def construct(self):
        p=probe(True); self.add(p)
        sites=VGroup(*[Square(.5,color=CHANNEL,fill_color=CHANNEL,fill_opacity=.25).move_to([-4.5,y,0]) for y in [2,0,-2]])
        trains=VGroup(); ticks=VGroup(); dots=VGroup()
        for row,y in enumerate([2,0,-2]):
            trains.add(Line([-4.2,y,0],[1.35,y,0],color=GREY))
            for k,x in enumerate([-3.7,-2.8,-1.9]):
                ticks.add(Line([x,y,0],[x,y+.5,0],color=SPIKE,stroke_width=4)); dots.add(Dot([x,y+.65,0],radius=.09,color=SOURCE[k]))
        self.at('neurons are not'); self.play(FadeIn(sites),Create(trains),FadeIn(ticks),FadeIn(dots),run_time=.6)
        units=VGroup()
        for i,y in enumerate([2.35,.75,-.85]):
            box=RoundedRectangle(width=3.3,height=1.25,color=SOURCE[i],fill_color=SOURCE[i],fill_opacity=.06).move_to([3,y,0])
            units.add(VGroup(box,T('unit '+str(i+1),30,YELLOW).move_to([3.7,y,0])))
        self.at('Software sorts')
        self.play(FadeIn(units),*[dots[j].animate.move_to([1.95+(j//3)*.35,units[j%3].get_y(),0]) for j in range(9)],*[ticks[j].animate.move_to([1.95+(j//3)*.35,units[j%3].get_y(),0]).scale(.6) for j in range(9)],run_time=.8)
        count=T('3 channels, 3 units',32).move_to([3,-3.45,0]); self.add(count)
        self.at('more units than channels')
        extra=VGroup(RoundedRectangle(width=3.3,height=1.1,color=SOURCE[3]).move_to([3,-2.3,0]),T('unit 4',30,YELLOW).move_to([3.7,-2.3,0]),*[Line([x,-2.45,0],[x,-2.15,0],color=SPIKE,stroke_width=4) for x in [1.95,2.3,2.65]],*[Dot([x,-1.98,0],radius=.07,color=SOURCE[3]) for x in [1.95,2.3,2.65]])
        c4=T('3 channels, 4 units',32).move_to(count)
        self.play(FadeIn(extra),FadeOut(count),FadeIn(c4),run_time=.3)
        self.at('or fewer')
        c2=T('3 channels, 2 units',32).move_to(count)
        self.play(FadeOut(extra),FadeOut(units[2]),FadeOut(VGroup(*[dots[j] for j in [2,5,8]],*[ticks[j] for j in [2,5,8]])),FadeOut(c4),FadeIn(c2),run_time=.3); self.finish()

class S05N(SpokenScene):
    def construct(self):
        n=neuron().scale(1.7).move_to([-3.5,0,0]); ss=VGroup(*[Square(.75,color=GREY).move_to([3.8,y,0]) for y in [2.4,0,-2.4]])
        nl=T('neuron',30,BLUE).move_to([-3.5,1.9,0]); sl=T('neighbouring sites',30,GREY).move_to([3.8,3.2,0]); self.add(n,ss,nl,sl)
        self.at('One neuron shows up')
        links=VGroup(*[Line(n[0].get_right(),s.get_left(),color=BLUE,stroke_width=4) for s in ss]); self.play(Create(links),run_time=.6)
        self.at('one site')
        n2=neuron(PINK).scale(1.7).move_to([-3.5,-2,0])
        self.play(FadeOut(links),FadeOut(nl),FadeOut(sl),FadeIn(T('one site',30,GREY).move_to([3.8,1.1,0])),FadeOut(ss[0]),FadeOut(ss[2]),n.animate.move_to([-3.5,1.4,0]),FadeIn(n2),run_time=.35)
        links2=VGroup(Line(n[0].get_right(),ss[1].get_left(),color=BLUE,stroke_width=4),Line(n2[0].get_right(),ss[1].get_left(),color=PINK,stroke_width=4))
        self.play(Create(links2),run_time=.4); self.finish()

class S06N(SpokenScene):
    def construct(self):
        ns=VGroup(neuron(BLUE).scale(1.4).move_to([-4,2,0]),neuron(PINK).scale(1.4).move_to([-4,-2,0])); self.add(ns)
        merge=bchip('1 unit, 2 neurons',YELLOW,34).move_to([2,0,0]); quality=quality_badge().next_to(merge,DOWN,buff=.3)
        links=VGroup(*[Arrow(n[0].get_right(),merge.get_left(),buff=.08,color=n[0].get_color()) for n in ns])
        self.at('a unit can'); self.play(Create(links),FadeIn(merge),FadeIn(quality),run_time=.3)
        self.at('split one')
        units=VGroup(*[bchip('unit',YELLOW,32).move_to([2,y,0]) for y in [2.2,.5]])
        badges=VGroup(*[quality_badge().next_to(u,RIGHT,buff=.3) for u in units])
        caption=T('2 units, 1 neuron',34,YELLOW).move_to([2,-1.1,0])
        arrows=VGroup(*[Arrow(ns[0][0].get_right(),u.get_left(),buff=.08,color=BLUE) for u in units])
        self.play(FadeOut(links),FadeOut(merge),FadeOut(quality),FadeOut(ns[1]),run_time=.15)
        self.play(FadeIn(units),FadeIn(badges),FadeIn(caption),Create(arrows),run_time=.3)
        self.at('as an inference'); self.play(FadeIn(T('Each unit is an inference',34,YELLOW).move_to([0,-3.1,0])),run_time=.3)
        self.at('quality scores'); self.play(Indicate(badges,color=GOLD),run_time=.4); self.finish()

class S07N(SpokenScene):
    def construct(self):
        rails,rows=ladder(); self.add(rails)
        self.at('Notice the'); self.play(FadeIn(rows[0]),run_time=.4)
        for cue,i in [('then channels',1),('then units',2),('then neurons',3)]:
            self.at(cue); self.play(FadeIn(rows[i]),run_time=.25)
        self.at('Each rung'); self.play(FadeIn(T('?',54,GOLD).move_to([3.4,2.4,0])),run_time=.3); self.finish()

class S08N(SpokenScene):
    def construct(self):
        rails,rows=ladder(('spike','calcium in','sensor','glow'),(SPIKE,LIME,SENSOR,GREEN))
        self.add(T('Calcium imaging',36,GREEN).move_to([0,3.35,0]))
        self.at('has a ladder'); self.play(Create(rails),run_time=.4)
        for cue,i in [('A spike lets',0),('calcium in',1),('a sensor',2),('sensor glow',3)]:
            self.at(cue); self.play(FadeIn(rows[i]),run_time=.25)
        self.play(FadeIn(T('far slower than a spike',28,GREEN).move_to([0,-3.4,0])),run_time=.25); self.finish()

class S09N(SpokenScene):
    def construct(self):
        p=response_plot(); self.add(p[0],p[1],p[4])
        self.at('The glow is real'); self.play(Create(p[2]),run_time=.7)
        self.at('but it lags'); self.play(FadeIn(p[3]),run_time=.35)
        self.at('like steam')
        k=kettle(); self.play(FadeIn(k[0][0:4]),FadeIn(k[1]),run_time=.3)
        self.play(LaggedStart(*[FadeIn(puff,shift=UP*.45) for puff in k[0][4]],lag_ratio=.3),run_time=.5); self.finish()

class S09bHold(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(response_plot(),kettle()); self.wait(2)

class S10N(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(41)
        groups=VGroup(*[VGroup(*[Dot([*rng.uniform([-5.8,-2.8],[5.8,2.7]),0],radius=.095,color=col) for _ in range(n)]) for col,n in zip([PURPLE,CREAM,SKY],[22,34,27])]); self.add(groups)
        targets=[]
        for i,g in enumerate(groups):
            target=g.copy(); center=[(-4,-.5),(0,1.1),(4,-.7)][i]
            for d in target:
                xy=rng.normal(size=2)*[.65,.8]; xy=np.clip(xy,-1.5,1.5); d.move_to([center[0]+xy[0],center[1]+xy[1],0])
            targets.append(target)
        self.at('sorts cells into clusters'); self.play(*[Transform(g,t) for g,t in zip(groups,targets)],run_time=1)
        self.at('Is each cluster')
        labels=VGroup(*[T('type?',36,GOLD).move_to([x,y,0]) for x,y in [(-4,2.5),(0,3.25),(4,2.5)]])
        self.play(FadeIn(labels),run_time=.4)
        self.at('may be'); self.play(Indicate(labels,color=GOLD),run_time=.5); self.finish()

class S11N(SpokenScene):
    def construct(self):
        a=neuron().scale(2.1).move_to([-4.5,.65,0]); b=neuron(PINK).scale(2.1).move_to([4.5,.65,0]); self.add(a,b)
        axon=Line(a[0].get_right(),b[0].get_left(),color=GREY,stroke_width=5)
        marks=VGroup(*[Dot([x,.65,0],radius=.18,color=CORAL) for x in [-1.4,0,1.4]])
        self.at('counts synapses'); self.play(Create(axon),LaggedStart(*[GrowFromCenter(d) for d in marks],lag_ratio=.2),run_time=.6)
        count=bchip('3 synapses',CORAL,38).move_to([-2,-1.65,0]); self.add(count)
        self.at('Is a count')
        strength=VGroup(Rectangle(width=2.7,height=.4,color=GOLD),T('strength?',36,GOLD).move_to([0,.7,0])).move_to([3,-1.65,0])
        self.play(FadeIn(T('?',52,GOLD).move_to([.5,-1.65,0])),FadeIn(strength),run_time=.4)
        self.at('an assumption'); self.play(FadeIn(T('count → strength: assumption',34,RED).move_to([0,-3.2,0])),run_time=.4); self.finish()

class S12N(SpokenScene):
    def construct(self):
        units=VGroup(*[bchip('unit',YELLOW,28).move_to([x,y,0]) for y in [1.7,-1.1] for x in [-3.2,0,3.2]]); self.add(units)
        self.at('Units from one mouse')
        m=mouse().set_height(6.15).move_to([0,.35,0]); m.set_z_index(-1)
        self.play(FadeIn(m),*[u.animate.move_to([x,y,0]) for u,(x,y) in zip(units,[(-1.8,1),(-.3,1),(1.2,1),(-1.8,-.25),(-.3,-.25),(1.2,-.25)])],run_time=.7)
        self.at('share that mouse'); self.play(FadeIn(T('6 units, 1 mouse',42,ORANGE).move_to([0,-3.05,0])),run_time=.4); self.finish()

class S13N(SpokenScene):
    def construct(self):
        r=rule_box(); title=T('One idea',44,GOLD); self.add(r[0],title)
        self.at('Each of these numbers'); self.play(FadeOut(title),run_time=.15); self.play(FadeIn(r[1][0]),run_time=.3)
        self.at('one or more steps'); self.play(FadeIn(r[1][1]),run_time=.4); self.finish()

class S14N(SpokenScene):
    def construct(self):
        old=rule_box(); self.add(old)
        r=rule_box(2)
        self.at('Name each step'); self.play(Transform(old[0],r[0]),old[1].animate.move_to(r[1][:2]),FadeIn(r[1][2]),run_time=.5)
        self.at('Trust it only'); self.play(FadeIn(r[1][3]),run_time=.5); self.finish()

class S15N(SpokenScene):
    def construct(self):
        old=rule_box(2); self.add(old)
        box=RoundedRectangle(width=6.4,height=6.6,corner_radius=.2,color=GOLD).move_to([-3,0,0])
        lines=VGroup(T('Each number is a proxy.',32,GOLD),T('Name each step.',32,TEXT),T('Trust it only as far as\nit has been measured\nin conditions like yours.',28,line_spacing=1.1),T('More cells sharpen\neach animal’s estimate.',30,TEXT),T('More cells never count\nas more animals.',30,ORANGE)).arrange(DOWN,buff=.38).move_to([-3,0,0])
        m=mouse().set_height(2.6).move_to([3.4,1.55,0]); dots=VGroup(*[Dot([2.9+i*.3,1.35+j*.32,0],radius=.115,color=YELLOW) for i in range(4) for j in range(2)])
        lab=T('many cells, still 1 animal',26,ORANGE).move_to([3.5,-.55,0])
        self.at('More cells sharpen'); self.play(FadeOut(old),run_time=.2); self.clear(); self.play(FadeIn(box),FadeIn(lines[:4]),FadeIn(m),FadeIn(dots),FadeIn(lab),run_time=.4)
        self.at('But they never')
        many=VGroup(*[mouse().set_height(1.85).stretch_to_fit_width(1.75).move_to([1.4+i*2.15,-2.0,0]) for i in range(3)])
        self.play(FadeIn(lines[4]),FadeIn(many),FadeIn(T('3 animals',34,ORANGE).move_to([3.55,-3.45,0])),run_time=.4); self.finish()

class S16N(SpokenScene):
    def construct(self):
        t=table(); self.add(t[0][0])
        self.at('a row like this')
        # Rows reveal on separate beats; headers appear on their spoken phrases.
        self.play(FadeIn(t[1][0],shift=UP*.12),run_time=.4)
        self.at('the number it gives'); self.play(FadeIn(t[0][1]),LaggedStart(*[FadeIn(r,shift=UP*.12) for r in t[1][1:3]],lag_ratio=.8),run_time=.8)
        self.at('the step to your claim'); self.play(FadeIn(t[0][2]),LaggedStart(*[FadeIn(r,shift=UP*.12) for r in t[1][3:5]],lag_ratio=.8),run_time=.85); self.finish()

class S17N(SpokenScene):
    def construct(self):
        t=table(); self.add(t)
        self.at('It cannot show'); self.play(FadeOut(t),run_time=.35)
        q=bchip('Needed for behaviour?',GOLD,46).move_to([0,1,0]); self.play(FadeIn(q),run_time=.35)
        self.at('That takes a manipulation'); self.play(FadeIn(bchip('Test with a manipulation',TEXT,40).move_to([0,-1,0])),run_time=.4); self.finish()

class S18N(SpokenScene):
    def construct(self):
        t=table()
        t[0][2].move_to([1.4,3.15,0])
        for row in t[1]:
            row[2].move_to([1.4,row[0].get_y(),0])
            row[3].put_start_and_end_on([-6.3,row[3].get_y(),0],[3.45,row[3].get_y(),0])
        t[1][1][2].become(T('light → calcium\n→ spikes',26,line_spacing=.8).move_to([1.4,t[1][1][0].get_y(),0]))
        self.add(t)
        self.at('The next two films'); self.play(*[r.animate.set_opacity(.25) for i,r in enumerate(t[1]) if i not in [1,2]],run_time=.3)
        self.at('light to spikes'); self.play(Indicate(t[1][1],color=GREEN),FadeIn(bchip('light → spikes',GREEN,26).move_to([5.1,t[1][1][0].get_y(),0])),run_time=.4)
        self.at('cells to mice'); self.play(Indicate(t[1][2],color=ORANGE),FadeIn(bchip('cells → mice',ORANGE,26).move_to([5.1,t[1][2][0].get_y(),0])),run_time=.4); self.finish()

class S19End(EndCard):
    LINE='Name each step. Trust only what was measured in conditions like yours.'
    def construct(self):
        line=T('Name each step.\nTrust only what was measured\nin conditions like yours.',48,font=TITLE_FONT,line_spacing=1.2).move_to(ORIGIN)
        url=T('biochemistrypedia.com',32,TEAL).move_to([0,-2.45,0])
        self.play(FadeIn(line,shift=UP*.1),run_time=self.beat(.3))
        self.play(FadeIn(url),run_time=self.beat(.15)); self.finish()
