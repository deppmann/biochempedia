"""Chapter 1: A Route in Legs.
COLOR MAP: BLUE pioneer/cone; YELLOW cue/source; GREY tissue;
PURPLE follower; RED crossed-out map; TEXT labels.
Route segments have four labelled swatches (BLUE, GREEN, TEAL, GOLD).
P is schematic route geometry, not anatomical data. All gradient trajectories
integrate grad(sum(exp(-r/lambda))); all signal traces use receptor occupancy.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
P = [np.array([x,y,0.]) for x,y in [(-5,-1.9),(-3.1,.6),(-.7,-1.6),(1.6,.4),(4.5,1.9)]]
SOURCE=np.array([2.,.1,0.]); SECOND=np.array([-2.,.1,0.]); START=np.array([-3.9,-1.6,0.])
LEG_COLORS=[BLUE,GREEN,TEAL,GOLD]

def label(s,pos=ORIGIN,size=30,color=TEXT):
    return T(s,size=max(32,size),color=color).move_to(pos)

def heading(s):
    return label(s,[0,3.05,0],36)

def leader(a,b,color=GREY):
    return Line(a,b,color=color,stroke_width=2)

def cone(pos=ORIGIN,scale=1.,color=BLUE):
    fan=Polygon([-.55,-.42,0],[.15,-.78,0],[.82,-.42,0],[1.02,0,0],
                [.82,.42,0],[.15,.78,0],[-.55,.42,0],
                stroke_color=color,fill_color=color,fill_opacity=.3,stroke_width=3)
    fingers=VGroup(*[Line([.15,0,0],[1.55*np.cos(a),1.55*np.sin(a),0],color=color,stroke_width=3)
                    for a in np.linspace(-1.1,1.1,7)])
    shaft=VGroup(*[Line([-2.,y,0],[-.48,y,0],color=GREY,stroke_width=5) for y in [-.18,0,.18]])
    return VGroup(shaft,fan,fingers).scale(scale).move_to(pos)

def travel(gc,path):
    gc._heading=getattr(gc, "_heading", 0.)
    def update(mob,alpha):
        a=min(alpha,.999);p=path.point_from_proportion(a);q=path.point_from_proportion(min(a+.001,1.))
        theta=np.arctan2((q-p)[1],(q-p)[0]);mob.rotate(theta-mob._heading);mob._heading=theta
        mob.move_to(path.point_from_proportion(alpha))
    return UpdateFromAlphaFunc(gc,update)

def field(s=SOURCE,lam=1.65,radius=2.65):
    return VGroup(*[Circle(r,stroke_width=0,fill_color=YELLOW,fill_opacity=.09*np.exp(-r/lam)).move_to(s)
                    for r in np.linspace(radius,.15,30)])

def source(s=SOURCE):
    return Circle(.43,color=YELLOW,fill_color=YELLOW,fill_opacity=.7).move_to(s).set_z_index(2)

def trajectory(start=START,sources=(SOURCE,),stop=1.15,color=BLUE):
    x=np.array(start,dtype=float);ps=[x.copy()]
    for _ in range(1400):
        ds=[np.linalg.norm(s-x) for s in sources]
        if min(ds)<stop:break
        g=sum(np.exp(-r/1.65)*(s-x)/(1.65*max(r,1e-6)) for s,r in zip(sources,ds))
        x=x+.025*g/max(np.linalg.norm(g),1e-9);ps.append(x.copy())
    return VMobject().set_points_as_corners(ps).set_stroke(color,5)

def model(question=False):
    gc=cone(START,.74);gc.rotate(np.arctan2(*(SOURCE-START)[1::-1]))
    g=VGroup(field(),source(),gc,label('Ideal radial-gradient model',[-2.6,2.35,0],32),
             label('source',[3.8,-1.1,0],34,YELLOW))
    if question:g.add(heading('What shape is the path?'))
    return g

# Starting on opposite sides of the separatrix gives opposite destinations.
TWO_STARTS=[np.array([-1.3,-1.9,0]),np.array([1.2,-1.45,0])]
def two_paths():
    return [trajectory(s,(SOURCE,SECOND),stop=.85,color=c) for s,c in zip(TWO_STARTS,[BLUE,TEAL])]

def two_model():
    paths=two_paths();g=VGroup(field(),field(SECOND),source(),source(SECOND),
        label('Ideal radial-gradient model',[-2.6,2.35,0],32),
        label('Two starts → two destinations',[0,-3.1,0],30))
    for i,p in enumerate(paths):
        gc=cone(scale=.30,color=[BLUE,TEAL][i]);d=p.get_end()-p.point_from_proportion(.99)
        gc.rotate(np.arctan2(d[1],d[0])).move_to(p.get_end())
        g.add(p,gc,Dot(p.get_start(),color=[BLUE,TEAL][i],radius=.09))
    return g

def limb():
    return Polygon([-5.8,-2.6,0],[-5.9,-.8,0],[-4.2,1.8,0],[-1.7,2.4,0],[4.9,2.5,0],
                   [5.7,1.5,0],[3.1,-.1,0],[-.2,-2.5,0],color=GREY,fill_color=GREY,fill_opacity=.07)

def route(color=BLUE):
    return VMobject().set_points_as_corners(P).set_stroke(color,7)

def legs():
    return VGroup(*[Line(a,b,color=col,stroke_width=8) for a,b,col in zip(P[:-1],P[1:],LEG_COLORS)])

def points():
    return VGroup(*[Dot(p,radius=.14,color=TEXT) for p in P[1:-1]])

def route_stage(colored=False):
    return VGroup(limb(),legs() if colored else route(),points(),
        label('tip',[-5.2,-3.05,0],28),label('toward body',[4.6,-.5,0],28),
        label('Limb and route: schematic',[0,-3.1,0],28))

def rule1():
    return VGroup(label('A growth cone reads only',[0,2.25,0],32),
                  label('what is within its reach.',[0,1.65,0],32))

def rule_box(expanded=False):
    # The card grows only when a second rule is ready to appear.
    return RoundedRectangle(width=12.2,height=2.65 if expanded else 1.35,corner_radius=.18,
        color=TEXT,fill_color=BG,fill_opacity=1).move_to([0,1.325 if expanded else 1.95,0])

def mini_route():
    g=VGroup(legs(),points()).scale(.78).shift(DOWN*1.6)
    return g

class S00Title(TitleCard):
    LESSON='Pioneers, Guideposts and the Logic of Guidance Cues'
    TITLE='A Route in Legs'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',[0,1.65,0],28,TEAL),
                 label('Pioneers, Guideposts and the Logic of Guidance Cues',[0,.6,0],28))
        self.play(FadeIn(label(self.TITLE,[0,-.5,0],54)),run_time=.5);self.finish()

class S01Question(SpokenScene):
    def construct(self):
        limb=VGroup(Arc(radius=2.35,start_angle=PI/2,angle=PI,color=GREY).shift(LEFT*3.7),
                    Line([-3.7,2.35,0],[6.4,2.35,0],color=GREY),Line([-3.7,-2.35,0],[6.4,-2.35,0],color=GREY))
        cells=VGroup(*[Circle(.32,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([-4.9,y,0]) for y in [-.65,.65]])
        self.add(limb,cells,heading('First axons in a growing leg'),label('tip',[-5.1,-2.85,0],28),
                 label('body beyond frame →',[3.7,-2.85,0],28),label('AI illustration • schematic',[0,-3.45,0],28))
        self.at('first axons')
        tracks=VGroup(*[Line([-4.6,y,0],[-2.6,y,0],color=BLUE,stroke_width=6) for y in [-.65,.65]])
        tips=VGroup(*[cone([-2.4,y,0],.30) for y in [-.65,.65]])
        self.play(Create(tracks),FadeIn(tips),run_time=1.5)
        self.at('far end')
        self.play(GrowArrow(Arrow([.1,-1.1,0],[4.7,-1.1,0],buff=0,color=BLUE)),
                  FadeIn(label('empty tissue ahead',[2.4,-1.8,0],30)),run_time=.55)
        self.at('No earlier axons')
        self.play(FadeIn(label('No earlier axons ahead',[1.5,1.25,0],32)),run_time=.25)
        self.at('How do they',lead=.45)
        self.add(label('How do they find the way?',[1.4,.15,0],36));self.finish()

class S02Cone(SpokenScene):
    def construct(self):
        c=cone([-1.,0,0],1.55)
        self.add(c,label('Growth cone',[0,3.2,0],30),label('microtubules',[-3.9,-2.,0],28),
                 leader([-3.8,-1.65,0],[-3.,-.25,0]),label('actin fan',[-.1,-2.3,0],28),
                 leader([-.1,-1.95,0],[-.1,-.8,0]),label('filopodia',[2.6,2.,0],28),leader([2.2,1.7,0],[1.,1.2,0]))
        self.at('does not carry',lead=.55)
        mp=VGroup(Rectangle(width=1.5,height=1.25,color=GREY),
                  VMobject().set_points_as_corners([[-.6,-.3,0],[-.1,.3,0],[.5,-.1,0]]).set_stroke(GREY,3)).move_to([4.7,-.4,0])
        cross=VGroup(Line([3.8,-1.2,0],[5.6,.4,0],color=RED,stroke_width=6),Line([3.8,.4,0],[5.6,-1.2,0],color=RED,stroke_width=6))
        self.play(FadeIn(mp),Create(cross),FadeIn(label('No map',[4.7,-1.9,0],28)),run_time=.3);self.finish()

class S03Size(SpokenScene):
    def construct(self):
        c=cone([-1.,0,0],1.55);self.add(c,label('Growth cone',[0,3.2,0],30))
        self.at('roughly ten')
        bar=VGroup(Line([-1.5,-2.1,0],[.93,-2.1,0]),*[Line([x,-1.95,0],[x,-2.25,0]) for x in [-1.5,.93]])
        self.play(Create(bar),FadeIn(label('about 10 µm',[-.3,-2.7,0],30)),run_time=.35)
        self.at('filopodia reach farther')
        self.play(FadeIn(label('reach farther',[3.8,1.7,0],30)),Create(leader([3.,1.4,0],c[2][-1].get_end())),run_time=.35)
        self.at('It can touch')
        tip=c[2][3].get_end();wall=Line([tip[0],-1.6,0],[tip[0],1.6,0],color=GREY,stroke_width=7)
        self.play(Create(wall),FadeIn(Dot(tip,radius=.16,color=YELLOW)),run_time=.3)
        self.play(Flash(tip,color=YELLOW,flash_radius=.4),run_time=.5);self.finish()

class S04Compare(SpokenScene):
    def construct(self):
        c=cone([-1.,0,0],1.65);cloud=field(np.array([.6,1.2,0]),radius=1.6)
        self.add(cloud,c,heading('Compare the two sides'))
        self.at('its two sides')
        self.play(FadeIn(label('more',[3.4,1.25,0],32,YELLOW)),Create(leader([2.6,1.25,0],[1.,.9,0],YELLOW)),
                  FadeIn(label('less',[3.4,-1.3,0],32,YELLOW)),Create(leader([2.6,-1.3,0],[1.,-.9,0],YELLOW)),run_time=.3);self.finish()

class S05Setup(SpokenScene):
    def construct(self):
        m=model();self.add(m[2],m[3],heading('One source in uniform tissue'))
        self.at('One cell');self.play(FadeIn(m[1]),FadeIn(m[4]),run_time=.3)
        self.at('releases an attractant');self.play(FadeIn(m[0]),run_time=.6)
        self.at('heads straight up')
        d=(SOURCE-START)/np.linalg.norm(SOURCE-START)
        self.play(GrowArrow(Arrow(START+d*1.2,START+d*2.8,buff=0,color=YELLOW)),
                  FadeIn(label('up the gradient',[-.9,-2.6,0],30,YELLOW)),run_time=.5);self.finish()

class S06Predict(SpokenScene):
    def construct(self):
        self.add(model(True));self.at('What shape');self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(model(True))
        self.add(Circle(.35,color=TEXT).move_to([5.4,-2.5,0]))
        for n in range(5,0,-1):
            num=label(str(n),[5.4,-2.5,0],28);self.add(num);self.wait(1);self.remove(num)

class S08Straight(SpokenScene):
    def construct(self):
        m=model();gc=m[2];gc.rotate(-np.arctan2(*(SOURCE-START)[1::-1]));self.add(m,heading('A straight line to the source'))
        rings=VGroup(*[Circle(r,color=YELLOW,stroke_width=2,stroke_opacity=.5).move_to(SOURCE) for r in [.9,1.7,2.5]])
        self.at('straight line',lead=0)
        # The complete cone, including its forward filopodia, stops outside the cell.
        path=trajectory(stop=1.9).set_stroke(BLUE,7)
        self.play(Create(path),travel(gc,path),run_time=3.35,rate_func=linear)
        self.at('falls off equally');self.play(Create(rings),run_time=.7);self.finish()

class S09Uphill(SpokenScene):
    def construct(self):
        self.add(field(),source(),heading('Uphill points at the source'),label('Ideal radial-gradient model',[-2.6,2.35,0],32))
        starts=[START,np.array([-.4,1.8,0]),np.array([4.8,-1.9,0])]
        ps=[trajectory(s,stop=1.25) for s in starts];cs=[cone(s,.40) for s in starts]
        arrows=[]
        for s in starts:
            d=(SOURCE-s)/np.linalg.norm(SOURCE-s)
            arrows.append(Arrow(s+d*.65,s+d*1.2,color=YELLOW,buff=0,max_tip_length_to_length_ratio=.3))
        self.add(*cs,*[Dot(s,radius=.11,color=TEXT) for s in starts],*arrows,
                 label('starting positions',[0,-3.1,0],30))
        self.at('uphill always points');self.play(*[Create(p) for p in ps],*[travel(c,p) for c,p in zip(cs,ps)],run_time=2.15)
        self.at('the climb ends');self.play(Indicate(self.mobjects[1]),run_time=.35);self.finish()

class S10Two(SpokenScene):
    def construct(self):
        self.add(field(),source(),heading('Where it starts changes where it ends'),label('Ideal radial-gradient model',[-2.6,2.35,0],32))
        ps=two_paths();cs=[cone(s,.30,col) for s,col in zip(TWO_STARTS,[BLUE,TEAL])]
        self.add(*cs,*[Dot(s,radius=.08,color=col) for s,col in zip(TWO_STARTS,[BLUE,TEAL])],
            label('start 1',[-2.6,-2.65,0],32,BLUE),leader([-2.0,-2.4,0],TWO_STARTS[0],BLUE),
            label('start 2',[2.6,-2.65,0],32,TEAL),leader([2.0,-2.4,0],TWO_STARTS[1],TEAL))
        self.at('a second source');self.play(FadeIn(field(SECOND)),FadeIn(source(SECOND)),run_time=.35)
        self.at('the path can curve')
        self.play(FadeIn(label('One possible trajectory',[-3.2,-3.25,0],30,BLUE)),Create(ps[0]),travel(cs[0],ps[0]),run_time=1.5)
        self.at('Where it ends')
        self.play(FadeIn(label('Another trajectory',[3.2,-3.25,0],30,TEAL)),Create(ps[1]),travel(cs[1],ps[1]),run_time=1.55);self.finish()

class S11Oneway(SpokenScene):
    def construct(self):
        self.add(two_model(),heading('An attractant gives a destination'))
        self.at('not a list');self.play(FadeIn(label('Not a list of stops',[0,-2.5,0],32)),run_time=.25);self.finish()

class S12Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(two_model(),heading('An attractant gives a destination'),label('Not a list of stops',[0,-2.5,0],32));self.wait(2.5)

class S13Real(SpokenScene):
    def construct(self):
        self.add(limb(),heading('Real route'),label('tip',[-5.2,-3.05,0],28),label('toward body',[4.6,-.5,0],28),label('Limb and route: schematic',[0,-3.1,0],28),Dot(P[0],color=BLUE))
        self.at('reach a place');self.play(Create(Line(P[0],P[1],color=BLUE,stroke_width=7)),run_time=.65)
        self.at('go on from it');self.play(Create(Line(P[1],P[2],color=BLUE,stroke_width=7)),run_time=.7)
        self.at('first axons');self.play(Create(VMobject().set_points_as_corners(P[2:]).set_stroke(BLUE,7)),run_time=1.4)
        self.at('several sharp turns')
        self.play(FadeIn(points()),*[FadeIn(label(str(i+1),p+[0,.55,0],28)) for i,p in enumerate(P[1:-1])],run_time=.4);self.finish()

class S14New(SpokenScene):
    def construct(self):
        title=heading('A turn on the real route');self.add(route_stage(),title)
        self.at('A turn like');self.play(Create(Circle(.48,color=TEXT).move_to(P[1])),run_time=.3)
        self.at('reading something new');self.play(Transform(title,heading('Usually: something new is read here')),run_time=.3);self.finish()

class S15What(SpokenScene):
    def construct(self):
        # A dedicated enlarged turn with three simultaneously retained alternatives.
        turn=np.array([0.,-.9,0]);self.add(heading('What might be read at a turn?'),
            Line([-4.,-2.5,0],turn,color=BLUE,stroke_width=7),Line(turn,[4.,-2.5,0],color=BLUE,stroke_width=7),Circle(.5,color=TEXT).move_to(turn),
            label('Possible cues • schematic',[0,-3.15,0],28))
        icons=[VGroup(source(np.array([-4.,.9,0])),label('A cell it touches',[-4.,1.9,0],28)),
               VGroup(Line([-.65,.6,0],[.65,1.2,0],color=GREY,stroke_width=9),label('A tissue boundary',[0,1.9,0],28)),
               VGroup(field(np.array([4.,.9,0]),radius=.7),label('A different cue',[4.,1.9,0],28))]
        for phrase,icon,x in zip(['A cell','a boundary','a different cue'],icons,[-4.,0.,4.]):
            self.at(phrase);self.play(FadeIn(icon),Create(leader([x,.35,0],turn+[x*.1,.4,0])),run_time=.25)
        self.finish()

class S16Reach(SpokenScene):
    def construct(self):
        s=np.array([-4.4,.2,0]);c=cone([-2.2,.2,0],1.05)
        # A physical-distance strip: brightness samples the same exponential model.
        strip=VGroup(*[Rectangle(width=.24,height=3.3,stroke_width=0,fill_color=YELLOW,
                        fill_opacity=.7*np.exp(-x/1.65)).move_to([-4.2+x,.2,0]) for x in np.arange(0,9,.24)])
        self.add(strip,source(s),c,heading('A secreted cue thins with distance'),label('source',[-4.4,2.35,0],30,YELLOW),
            Line([-4.4,-2.3,0],[5.,-2.3,0],color=TEXT,stroke_width=3),label('distance from source',[0,-3.15,0],30))
        for x,txt in [(-4.4,'0'),(-1.1,'2λ'),(2.2,'4λ')]:
            self.add(Line([x,-2.2,0],[x,-2.4,0],color=TEXT,stroke_width=3),label(txt,[x,-2.7,0],32))
        self.at('A secreted cue')
        glow=Circle(.85,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).move_to(c);self.add(glow)
        self.play(c.animate.move_to([4.4,.2,0]),glow.animate.move_to([4.4,.2,0]).set_opacity(.02),run_time=2.0);self.finish()

class S17Reach2(SpokenScene):
    def construct(self):
        self.add(heading('Lost in noise • far from source'),label('left side',[-2.8,2.45,0],30,BLUE),label('right side',[1.,2.45,0],30,YELLOW))
        ax=Axes(x_range=[0,4,1],y_range=[0,.05,.01],x_length=11.2,y_length=3.8,tips=False,
            axis_config={'color':TEXT,'include_ticks':True,'stroke_width':3}).move_to([.35,-.4,0])
        self.add(ax,label('time (s)',[.4,-3.15,0],28),label('receptor occupancy (fraction)',[0,1.8,0],32))
        for t in range(5):self.add(label(str(t),ax.c2p(t,0)+[0,-.3,0],28))
        for v in [0,.02,.04]:self.add(label(f'{v:.2f}',ax.c2p(0,v)+[-.55,0,0],28))
        # 5000 independent receptors per side; expected concentration exp(-r/λ).
        rng=np.random.default_rng(7);xx=np.linspace(0,4,81);traces=VGroup()
        for r,col in [(6.9,BLUE),(7.1,YELLOW)]:
            conc=np.exp(-r/1.65);occ=conc/(1+conc)
            yy=rng.binomial(5000,occ,len(xx))/5000
            traces.add(VMobject().set_points_as_corners([ax.c2p(x,y) for x,y in zip(xx,yy)]).set_stroke(col,3))
        self.at('the difference across');self.play(Create(traces),run_time=1.4)
        self.at('lost in noise');self.play(Indicate(traces,scale_factor=1.01),run_time=.35);self.finish()

class S18Reach3(SpokenScene):
    def construct(self):
        self.add(heading('Simple diffusion model: estimated reach'))
        # Log ruler makes the 10 µm cone comparable with millimetre distances.
        def x(v):return -5.2+3.2*np.log10(v/10)
        self.add(Line([x(10),.5,0],[x(10000),.5,0],color=TEXT))
        for v,txt in [(10,'10 µm'),(100,'100 µm'),(1000,'1 mm'),(10000,'10 mm')]:
            self.add(Line([x(v),.35,0],[x(v),.65,0],color=TEXT),label(txt,[x(v),-.1,0],28))
        self.add(cone([x(10),1.3,0],.19),label('cone',[x(10),2.05,0],28,BLUE),
                 label('Distance from source • logarithmic ruler',[0,-.8,0],28),
                 label('Sensitivity, cue lifetime and receptor range',[0,-2.5,0],28),label('See Going deeper',[0,-3.15,0],28,TEAL))
        # The estimated span is visible before the spoken numeric range.
        span=Line([x(200),1.3,0],[x(4000),1.3,0],color=YELLOW,stroke_width=12)
        self.add(span,label('estimated range',[1.2,2.05,0],30,YELLOW))
        range_text=label('Hundreds of µm',[0,-1.55,0],32,YELLOW)
        self.at('hundreds of');self.add(range_text)
        self.at('to a few');self.play(Transform(range_text,label('Hundreds of µm to a few mm',[0,-1.55,0],32,YELLOW)),run_time=.3)
        self.at('an estimate');self.play(Transform(self.mobjects[0],heading('An estimate, not a fixed range')),run_time=.25);self.finish()

class S19Rule1(SpokenScene):
    def construct(self):
        r=rule1();self.add(heading('The local-reading rule'),rule_box(),r)
        gc=cone([0,-1.25,0],.9);ring=Circle(1.65,color=YELLOW,stroke_opacity=.8).move_to([0,-1.25,0])
        self.add(ring,gc,label('reach',[3.,-1.25,0],30,YELLOW),leader([2.35,-1.25,0],[1.65,-1.25,0],YELLOW))
        self.at('A growth cone');self.play(Indicate(r,scale_factor=1.02),run_time=.3)
        self.at('within its reach');self.play(Indicate(ring,scale_factor=1.05),run_time=.4);self.finish()

class S20Rule2(SpokenScene):
    def construct(self):
        box=rule_box();self.add(mini_route(),box,rule1())
        self.at('usually built')
        labs=VGroup(*[label(f'leg {i+1}',p,28,col) for i,p,col in zip(range(4),
            [[-3.8,-1.6,0],[-1.8,-2.85,0],[.8,-2.8,0],[3.8,-.9,0]],LEG_COLORS)])
        self.play(FadeIn(labs),run_time=.4)
        self.at('chain of legs');self.play(Transform(box,rule_box(True)),FadeIn(label('A chain of legs',[0,.7,0],32)),run_time=.3);self.finish()

class S21Rule3(SpokenScene):
    def construct(self):
        box=rule_box();self.add(mini_route(),box,rule1())
        cp=[p*.78+DOWN*1.6 for p in P[1:-1]]
        self.at('a choice point')
        for p,loc in zip(cp,[[-3.8,-.35,0],[-.5,-3.35,0],[3.9,-1.8,0]]):
            self.add(label('choice point',loc,28),leader(np.array(loc)+[0,-.22 if loc[1]>-1 else .22,0],p))
        self.at('reads something new')
        self.play(Transform(box,rule_box(True)),FadeIn(label('At a choice point: read something new',[0,.9,0],30)),run_time=.25)
        self.at('reads the same')
        self.play(FadeIn(label('or read the same thing differently.',[0,.35,0],30)),run_time=.25);self.finish()

class S22Slows(SpokenScene):
    def construct(self):
        # Keep the full route and coordinates from the preceding rule scenes.
        self.add(limb().set_stroke(opacity=.35).set_fill(opacity=.025),legs().set_opacity(.23),points().set_opacity(.5),
                 heading('A common behaviour at a choice point'),
                 Line(P[0],P[1],color=BLUE,stroke_width=8),
                 Line(P[1],P[2],color=GREEN,stroke_width=8),Dot(P[1],radius=.18,color=TEXT),
                 label('choice point',[-3.5,1.85,0],32),leader([-3.5,1.5,0],P[1]+UP*.25),
                 label('Schematic • shape and pausing vary',[0,-3.2,0],32))
        first=Line(P[0],P[1]);gc=cone(P[0],.5);self.add(gc)
        self.at('At many choice points',lead=0)
        self.play(travel(gc,first),run_time=1.8,rate_func=linear)
        self.at('pause');self.wait(.45)
        self.at('spread out')
        # Widen perpendicular to the incoming direction, keeping the cone at the dot.
        theta=gc._heading
        wide=gc.copy().rotate(-theta)
        wide[1].stretch(1.35,1);wide[2].stretch(1.7,1)
        wide.rotate(theta).move_to(P[1])
        self.play(Transform(gc,wide),run_time=.45)
        self.at('they choose')
        outgoing=Line(P[1],P[1]+.72*(P[2]-P[1]))
        self.play(travel(gc,outgoing),run_time=.85,rate_func=linear);self.finish()

def contact_path():
    path=VMobject().start_new_path(P[0])
    for i in range(1,len(P)-1):
        entry=P[i]+.2*(P[i-1]-P[i]);exit=P[i]+.2*(P[i+1]-P[i])
        path.add_line_to(entry);path.add_cubic_bezier_curve_to(P[i],P[i],exit)
    path.add_line_to(P[-1]);return path.set_stroke(BLUE,7)

class S23Takeaway(SpokenScene):
    def construct(self):
        # Rounded contact track retains the same route through the choice points.
        path=contact_path()
        lead_start=.56
        pioneer=cone(scale=.38)
        tangent=path.point_from_proportion(lead_start+.001)-path.point_from_proportion(lead_start)
        pioneer._heading=np.arctan2(tangent[1],tangent[0])
        pioneer.rotate(pioneer._heading).move_to(path.point_from_proportion(lead_start))
        pioneer_label=label('Pioneer',size=32,color=BLUE)
        pioneer_label.add_updater(lambda m:m.next_to(pioneer,DOWN,buff=.35))
        pioneer_label.update()
        self.add(path,pioneer,heading('Local readings, chained at choice points'),
                 pioneer_label,label('A contact path can curve',[0,-3.15,0],32,PURPLE))
        self.at('Not every bend');self.play(Indicate(path,scale_factor=1.02),run_time=.5)
        self.at('A pioneer axon')
        fp=VMobject().pointwise_become_partial(path,0,.88).shift(DOWN*.12).set_stroke(PURPLE,5)
        pp=VMobject().pointwise_become_partial(path,lead_start,1.)
        follower=cone(fp.get_start(),.30,PURPLE);self.add(follower)
        follower_label=label('Follower',[2.7,-1.5,0],32,PURPLE)
        # Both advance together; the follower traverses nearly the whole contact route.
        self.play(FadeIn(follower_label),run_time=.2)
        self.play(Create(fp),travel(follower,fp),travel(pioneer,pp),
                  run_time=2.8,rate_func=linear)
        self.add(leader([3.,-1.15,0],follower.get_center()+DOWN*.35,PURPLE))
        self.finish()

class S24End(EndCard):
    LINE='Local readings chain legs; pioneers can guide followers around curves.'
    def construct(self):
        self.add(label('Local readings, chained at choice points',[0,.8,0],38),
                 label('A pioneer can guide followers around curves',[0,-.3,0],34),
                 label('biochemistrypedia.com',[0,-1.7,0],28,TEAL));self.finish()
