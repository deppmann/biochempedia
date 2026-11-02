"""Small Space, Big Change — reviewed animation.
COLOR MAP: YELLOW neuron / inside; BLUE potassium / outside / E_K;
GREEN astrocytes; TEAL pump; ORANGE oligodendrocytes; RED problem;
GREY axes / membranes; TEXT sodium. All traces: Hodgkin–Huxley RK4.
All concentration, volume and voltage geometry is computed from the model.
"""
import re
import numpy as np
from bp_style import *
from bp_style import T as _T

# A visible gap between lines, including question and end cards.
def T(text, size=30, color=TEXT, font=FONT, **kw):
    kw.setdefault('line_spacing', 1.2)
    if 'Eₖ' in text or 'Eₙₐ' in text:
        # Explicit lowered glyphs: the house font lacks Unicode subscript K/n.
        parts=[]
        for token in re.split('(Eₖ|Eₙₐ)',text):
            if not token: continue
            if token in ('Eₖ','Eₙₐ'):
                base=_T('E',size,color,font=font,**kw)
                sub=_T('K' if token=='Eₖ' else 'Na',size*.72,color,font=font,**kw)
                sub.next_to(base,RIGHT,buff=.02).shift(DOWN*.14)
                parts.append(VGroup(base,sub))
            else:
                parts.append(_T(token,size,color,font=font,**kw))
        # Text strips edge spaces; restore a readable word gap at each join.
        return VGroup(*parts).arrange(RIGHT,buff=.15)
    return _T(text, size, color, font=font, **kw)

NEUR, KC, ASTRO, BAD = YELLOW, BLUE, GREEN, RED
VI, VO, KI, KO = .8/3, .2, 140., 3.
EK = lambda k: 61.5*np.log10(k/KI)
VM = lambda k: 61.5*np.log10((k+.04*145)/(KI+.04*15))
X = lambda v: -5.6+(v+110)/180*11.2

def heading(s, color=TEXT):
    return T(s, 34, color).move_to([0,3.25,0])

def blob(x,y,w,h,color,fill=.16):
    return Ellipse(width=w,height=h,color=color,stroke_width=4,fill_color=color,fill_opacity=fill).move_to([x,y,0])

def kdot(p,r=.09):
    return Dot([p[0],p[1],0],radius=r,color=KC)

def rect(x,y,w,h,c,opacity=.65):
    return Rectangle(width=w,height=h,stroke_width=0,fill_color=c,fill_opacity=opacity).move_to([x,y,0])

def bracket(a,b,y,label,color=KC,above=True):
    # End caps and text are outside the measured span, never over the line.
    x1,x2=X(a),X(b)
    return VGroup(Line([x1,y,0],[x2,y,0],color=color,stroke_width=4),
        *[Line([x,y-.12,0],[x,y+.12,0],color=color,stroke_width=3) for x in (x1,x2)],
        T(label,28,color).move_to([(x1+x2)/2,y+(.35 if above else -.4),0]))

def bars(compact=False):
    base=-1.3 if compact else -2.3
    h=3.4 if compact else 4.6
    a=rect(-2.8,base+h/2,1.6,h,NEUR)
    b=rect(2.8,base+h*KO/KI/2,1.6,h*KO/KI,KC)
    labels=VGroup(T('inside neuron',28,NEUR).move_to([-2.8,base-.45,0]),
        T('outside',28,KC).move_to([2.8,base-.45,0]),
        M('140 mM',30,NEUR).move_to([-2.8,base+h+.35,0]),
        M('3 mM',30,KC).move_to([2.8,base+.48,0]))
    axis=VGroup(Line([-4.6,base,0],[4.5,base,0],color=GREY),
        Line([-4.6,base,0],[-4.6,base+h,0],color=GREY),
        T('[K⁺] (mM)',28).rotate(PI/2).move_to([-5.35,base+h/2,0]),
        Line([1.75,base+h*KO/KI,0],[3.85,base+h*KO/KI,0],color=KC,stroke_width=4))
    return VGroup(a,b,labels,axis)

def prediction_one():
    g=bars(True); g.set_opacity(.65)
    return VGroup(g,T('Which bar changes more?',30).move_to([0,-2.35,0]),
        T('Which change matters more for the voltage?',30).move_to([0,-3.12,0]))

def countdown(scene):
    ring=Circle(radius=.33,color=GREY,stroke_width=4).move_to([5.8,2.7,0])
    sweep=Arc(radius=.33,start_angle=PI/2,angle=TAU-.001,color=KC,stroke_width=7).move_to(ring)
    scene.add(ring,sweep)
    scene.play(Uncreate(sweep),run_time=5,rate_func=linear)

def voltage_scale():
    ax=Line([X(-110),0,0],[X(70),0,0],color=GREY,stroke_width=4)
    ticks=VGroup()
    for v in (-100,-60,-20,20,60):
        ticks.add(Line([X(v),-.22,0],[X(v),.22,0],color=GREY,stroke_width=3),
                  M(str(v).replace('-','−'),28).move_to([X(v),-.48,0]))
    ticks.add(T('mV',28).move_to([6.2,-.48,0]))
    na=VGroup(Line([X(60),0,0],[X(60),1.3,0],color=TEXT,stroke_width=3),
        Dot([X(60),0,0],radius=.15,color=TEXT),T('Eₙₐ',32).move_to([X(60),1.8,0]))
    return VGroup(ax,ticks,na)

def kmarker(k=10):
    x=X(EK(k))
    return VGroup(Line([x,0,0],[x,1.15,0],color=KC,stroke_width=4),
        Dot([x,0,0],radius=.18,color=KC),
        T('Eₖ',32,KC).move_to([x,1.5,0]),
        M(f'{EK(k):.1f}'.replace('-','−'),28,KC).move_to([x,2.02,0]))

def restmarker(k=3,v=None,before=False):
    v=VM(k) if v is None else v; x=X(v)
    return VGroup(Triangle(color=NEUR,fill_color=NEUR,fill_opacity=1).scale(.2).move_to([x,-1.02,0]),
        T(f"rest{' (before)' if before else ''}: {v:.0f} mV".replace('-','−'),28,NEUR).move_to([x,-1.5,0]))

def move_k(scene,old,k,duration=.7):
    new=kmarker(k)
    scene.play(Transform(old[0],new[0]),Transform(old[1],new[1]),
        FadeOut(VGroup(*old[2:])),FadeIn(VGroup(*new[2:])),run_time=duration)
    scene.remove(old,*new[2:]); scene.add(new)
    return new

def move_rest(scene,old,new,duration=.7):
    scene.play(Transform(old[0],new[0]),FadeOut(old[1]),FadeIn(new[1]),run_time=duration)
    scene.remove(old,new[1]); scene.add(new)
    return new

def kghost():
    return VGroup(Dot([X(EK(3)),0,0],radius=.15,color=KC),
        T('−102.6',26,KC).move_to([X(EK(3)),.65,0])).set_opacity(.4)

def prediction_two():
    return VGroup(voltage_scale(),kghost(),kmarker(10),restmarker(before=True),
        heading('Does rest also move 32 mV?'),bracket(EK(3),EK(10),2.35,'32 mV',KC,True))

def loop_diagram(color=GREY):
    nodes=VGroup(chip('more firing',NEUR,32).move_to([-3.5,1.65,0]),
        chip('more K⁺ outside',KC,32).move_to([3.1,1.65,0]),
        chip('closer to threshold',NEUR,30).move_to([0,-1.7,0]))
    arrows=VGroup(Arrow([-1.75,1.65,0],[.7,1.65,0],color=color,buff=.1,stroke_width=7),
        Arrow([3.1,.95,0],[1.65,-1.05,0],color=color,buff=.1,stroke_width=7),
        Arrow([-1.65,-1.05,0],[-3.5,.95,0],color=color,buff=.1,stroke_width=7))
    mini=VGroup(Line([-1.5,-2.7,0],[1.5,-2.7,0],color=GREY),
        Triangle(color=NEUR,fill_color=NEUR,fill_opacity=1).scale(.1).move_to([.55,-2.7,0]),
        Line([1.1,-2.95,0],[1.1,-2.4,0],color=NEUR),
        T('threshold',26,NEUR).move_to([2.8,-2.7,0]))
    return VGroup(nodes,arrows,mini)

def rule_card(top=True):
    return VGroup(T('Small space outside,',46,font=TITLE_FONT).move_to([0,2.3 if top else .8,0]),
        T('big change outside.',46,KC,font=TITLE_FONT).move_to([0,1.3 if top else -.5,0]))

def hh_model(current_fn=lambda t: 20 if 5<=t<6 else 0, duration=18):
    # Same HH rate equations, conductances and reversal potentials as the site.
    def rates(v):
        an = .1 if abs(v+55)<1e-6 else .01*(v+55)/(-np.expm1(-(v+55)/10))
        am = 1. if abs(v+40)<1e-6 else .1*(v+40)/(-np.expm1(-(v+40)/10))
        return am, 4*np.exp(-(v+65)/18), .07*np.exp(-(v+65)/20), 1/(1+np.exp(-(v+35)/10)), an, .125*np.exp(-(v+65)/80)
    a,b,c,d,e,f = rates(-65)
    state = np.array([-65., a/(a+b), c/(c+d), e/(e+f)])
    _,m,h,n = state
    el = -65 + (120*m**3*h*(-65-50)+36*n**4*(-65+77))/.3
    def rhs(s, current):
        v,m,h,n = s
        a,b,c,d,e,f = rates(v)
        return np.array([current-120*m**3*h*(v-50)-36*n**4*(v+77)-.3*(v-el),
                         a*(1-m)-b*m,c*(1-h)-d*h,e*(1-n)-f*n])
    pts=[]; dt=.02
    for i in range(round(duration/dt)+1):
        t=i*dt
        pts.append([t,state[0]])
        current=current_fn(t)
        k1=rhs(state,current); k2=rhs(state+dt*k1/2,current)
        k3=rhs(state+dt*k2/2,current); k4=rhs(state+dt*k3,current)
        state += dt/6*(k1+2*k2+2*k3+k4)
    return np.array(pts)


def hh_spike():
    data=hh_model()
    return VMobject(color=NEUR,stroke_width=5).set_points_as_corners(
        [[-5.8+t/18*5.7,-1.8+(v+80)/120*3.8,0] for t,v in data])


def block_traces():
    # A strong sustained drive in the SAME illustrative HH model produces a
    # depolarized steady state. The entire tail is integrated, never sketched.
    data=hh_model(lambda t: 0 if t<5 else (20 if t<65 else 250),duration=230)
    train=data[(data[:,0]>=5)&(data[:,0]<65)]
    tail=data[data[:,0]>=210]
    def path(samples,y):
        t0,t1=samples[0,0],samples[-1,0]
        return VMobject(color=NEUR,stroke_width=4).set_points_as_corners(
            [[-5+(t-t0)/(t1-t0)*10,y+(v+40)*.012,0] for t,v in samples])
    return path(train,-2.55),path(tail,-2.75)



class S00Title(TitleCard):
    TITLE='Small Space, Big Change'
    LESSON='Neurons and Glia at Work'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),28,GREY),
            T(self.TITLE,50,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        trace=hh_spike(); cell=blob(3.1,0,4.1,4.8,NEUR)
        neurites=VGroup(Line([1.3,1.15,0],[.65,2.4,0],color=NEUR,stroke_width=5),
            Line([1.3,-1.15,0],[.55,-2.4,0],color=NEUR,stroke_width=5))
        axes=VGroup(Line([-5.8,-1.8,0],[-.1,-1.8,0],color=GREY),
            Line([-5.8,-1.8,0],[-5.8,2.35,0],color=GREY),
            T('mV',28).move_to([-5.8,2.75,0]),T('ms',28).move_to([-.35,-2.3,0]),
            T('illustrative model spike',26,GREY).move_to([-3.1,-2.85,0]))
        self.add(trace,axes,cell,neurites,T('neuron',32,NEUR).move_to([3.1,0,0]))
        # Cursor follows the computed falling branch, not a hand-drawn curve.
        pts=trace.get_all_points(); peak=np.argmax(pts[:,1]); end=peak+np.argmin(pts[peak:,1])
        fall=VMobject().set_points_as_corners(pts[peak:end+1])
        cursor=Dot(fall.get_start(),color=KC,radius=.12)
        self.at('potassium leaving')
        # A staggered stream starts exactly on the curved membrane, and
        # moves only while the cursor follows the computed falling phase.
        ys=(-1.1,-.65,-.2,.25,.7,1.1)
        dots=VGroup(*[kdot((3.1+2.05*np.sqrt(1-(y/2.4)**2),y)) for y in ys])
        starts=[d.get_center().copy() for d in dots]
        def release(group,alpha):
            for i,(d,start) in enumerate(zip(group,starts)):
                phase=np.clip((alpha-i*.075)/.625,0,1)
                d.move_to(start+RIGHT*(1.35*phase))
                d.set_opacity(1 if alpha>=i*.075 else 0)
        self.add(cursor,dots,T('K⁺',30,KC).move_to([6,1.65,0]))
        self.play(MoveAlongPath(cursor,fall),UpdateFromAlphaFunc(dots,release),
            run_time=2.2,rate_func=linear)
        self.at('where does')
        self.play(FadeIn(heading('Where does the potassium go?',KC)),run_time=.35); self.finish()

class S02Space(SpokenScene):
    def construct(self):
        # Bright background channels, irregular packed polygons. The exact 4:1
        # volume key is explicitly separate from this schematic tissue section.
        seeds=np.array([[-3.7,-1.5],[-1.5,-1.45],[.5,-1.65],[3.1,-1.2],
            [-4, .6],[-2.1,.25],[.1,.45],[2.5,.6],[4,1.55],[-2.5,1.75],[.6,1.9]])
        cells=VGroup()
        for seed in seeds:
            poly=[np.array(v,dtype=float) for v in ((-4.8,-2.3),(4.8,-2.3),(4.8,2.3),(-4.8,2.3))]
            for other in seeds:
                normal=other-seed
                if np.linalg.norm(normal)<1e-8: continue
                cut=(other@other-seed@seed)/2
                clipped=[]
                for u,v in zip(poly,poly[1:]+poly[:1]):
                    fu,fv=u@normal-cut,v@normal-cut
                    if fu<=0: clipped.append(u)
                    if (fu<=0)!=(fv<=0): clipped.append(u+(v-u)*fu/(fu-fv))
                poly=clipped
            center=np.mean(poly,axis=0)
            poly=[center+np.sqrt(.8)*(v-center) for v in poly]
            cells.add(Polygon(*[[v[0],v[1],0] for v in poly],color=GREY,
                fill_color=BG,fill_opacity=1,stroke_width=2))
        tissue=VGroup(rect(0,0,9.6,4.6,KC,.6),cells)
        label=T('grey matter',30).move_to([0,2.7,0])
        tissue.scale(.3); self.add(tissue,label)
        self.at('into the gaps')
        self.play(tissue.animate.scale(1/.3),run_time=.65)
        self.at('those gaps')
        gap_center=np.array([-1.8,-.6,0])
        normal=np.array([-.6,1.7,0]); normal/=np.linalg.norm(normal)
        tangent=np.array([normal[1],-normal[0],0])
        u,v=gap_center-normal*.15,gap_center+normal*.15
        gap=VGroup(Line(u,v,color=KC,stroke_width=5),
            Line(u-tangent*.15,u+tangent*.15,color=KC),
            Line(v-tangent*.15,v+tangent*.15,color=KC),
            T('tens of nanometres',28,KC).move_to([0,-2.85,0]),
            Line(u,[-1,-2.5,0],color=KC))
        self.play(FadeIn(gap),run_time=.35)
        self.at('about a fifth')
        key=VGroup(rect(5.4,-.4,.7,3.2,NEUR,.65),rect(5.4,1.6,.7,.8,KC,.85),
            T('4 : 1',28).move_to([5.4,-2.6,0]))
        self.play(FadeOut(label),FadeIn(heading('About one fifth of the volume',KC)),FadeIn(key),run_time=.4); self.finish()

class S03Bars(SpokenScene):
    def construct(self):
        g=bars(); self.add(g)
        self.at('potassium is high'); self.play(Indicate(g[0],scale_factor=1.03),run_time=.45)
        self.at('outside it'); self.play(Indicate(g[1],scale_factor=1.15),run_time=.4)
        self.play(FadeIn(T('about 47 times',30).move_to([0,2.95,0])),run_time=.3); self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        g=bars(True); self.add(g)
        self.at('a burst')
        outline=blob(0,.2,1.4,1.8,NEUR,.05)
        dots=VGroup(*[kdot((.62,y)) for y in (-.15,.2,.55)])
        self.add(outline,dots,T('K⁺ released',28,KC).move_to([0,1.65,0]))
        self.play(LaggedStart(*[d.animate.move_to([2.8,y,0]) for d,y in zip(dots,(.2,.55,.9))],lag_ratio=.1),run_time=1.35)
        self.at('which concentration')
        q=prediction_one()
        self.play(FadeOut(outline),FadeOut(dots),g.animate.set_opacity(.65),FadeIn(q[1]),run_time=.35)
        self.at('and which change'); self.play(FadeIn(q[2]),run_time=.35); self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_one()); countdown(self)

class S06Volume(SpokenScene):
    def construct(self):
        self.add(heading('Outside changes more, in proportion',KC))
        neuron=blob(-3.6,0,3.3,3.6,NEUR)
        spikes=VGroup(*[hh_spike().scale(.32).move_to([x,-2.5,0]) for x in (-3.6,0,3.6)])
        dots=VGroup(*[kdot((-2.5,y)) for y in (-.6,0,.6)])
        self.add(neuron,spikes,T('firing neuron',30,NEUR).move_to([-3.6,0,0]),dots)
        self.at('in proportion')
        self.play(LaggedStart(*[d.animate.shift(RIGHT*4.5) for d in dots],lag_ratio=.1),run_time=1.2)
        self.at('take a simple model')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.mobjects[0]],run_time=.25)
        inside=rect(-1,0,8,4.7,NEUR,.12); outside=rect(4,0,2,4.7,KC,.7)
        self.add(inside,outside)
        self.at('the space outside')
        self.play(FadeIn(T('outside\n0.20',28,TEXT).move_to([4,0,0])),run_time=.3)
        self.at('and the firing neurons')
        span=VGroup(Line([-5,2.5,0],[3,2.5,0],color=NEUR),
            T('inside: 0.80',28,NEUR).move_to([-1,2.78,0]))
        firing=rect(-5+8/6,0,8/3,4.7,NEUR,.6)
        self.play(FadeIn(span),FadeIn(firing),run_time=.4)
        self.play(FadeIn(T('firing\nneurons\n0.80 / 3',28,TEXT).move_to([-3.67,0,0])),run_time=.3)
        self.add(T('firing neurons / outside = (0.80/3) / 0.20 = 1.33',27).move_to([0,-3.08,0])); self.finish()

class S07Four(SpokenScene):
    def construct(self):
        columns=VGroup(T('firing neurons',30,NEUR).move_to([-3.4,2.85,0]),
            T('outside',30,KC).move_to([3.4,2.85,0]))
        columns[1].align_to(columns[0],UP)
        self.add(heading('The same ions'),columns)
        bases=VGroup(*[Line([x-1.1,0,0],[x+1.1,0,0],color=GREY,stroke_width=3) for x in (-3.4,3.4)])
        self.add(bases,T('concentration change (mM)',27).move_to([0,-3.15,0]))
        inn=rect(-3.4,-1.9*.75/2,1.6,1.9*.75,NEUR); out=rect(3.4,1.9/2,1.6,1.9,KC)
        dots=VGroup(*[kdot((-3.4,y)) for y in (-1.15,-.85,-.55,-.25)])
        self.at('the same potassium'); self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to([3.4,y,0]) for d,y in zip(dots,(.35,.75,1.15,1.55))],lag_ratio=.1),GrowFromEdge(inn,UP),GrowFromEdge(out,DOWN),run_time=2.5,rate_func=linear)
        self.play(FadeOut(dots),FadeIn(M('−0.75 mM',30,NEUR).move_to([-3.4,-1.8,0])),
            FadeIn(M('+1 mM',30,KC).move_to([3.4,2.18,0])),run_time=.3)
        self.at('about one and a third')
        ratio=VGroup(Line([-1.7,1.4,0],[1.7,1.4,0],color=TEXT),
            T('1 : 0.75',30).move_to([0,.8,0]),T('= 1.33×',34,KC).move_to([0,-.1,0]))
        self.play(FadeIn(ratio),run_time=.4); self.finish()

class S08Start(SpokenScene):
    def construct(self):
        self.add(heading('The same transfer'))
        # Two explicit percent panels: each full starting bar is 100%.
        for x,name,c,value in ((-3.1,'outside',KC,'3 mM'),(3.1,'inside',NEUR,'140 mM')):
            self.add(T(name,30,c).move_to([x,2.62,0]),rect(x,-.35,2,3,c,.5),
                T(value,30,c).move_to([x,-2.35,0]),T('100% at start',26).move_to([x,.6,0]),
                Line([x-1.4,-1.85,0],[x+1.4,-1.85,0],color=GREY))
        self.at('one extra')
        gain=rect(-3.1,1.65,2,1,KC,.95)
        self.play(GrowFromEdge(gain,DOWN),run_time=.6)
        self.at('raises it by a third')
        self.play(FadeIn(T('4 mM  /  +33%',30,KC).move_to([-3.1,-3.08,0])),run_time=.25)
        self.at('losing three')
        loss=rect(3.1,1.15-3*(.75/140)/2,2,3*(.75/140),BAD,.95)
        self.play(FadeIn(loss),run_time=.3)
        self.at('about half a percent')
        self.play(FadeIn(T('139.25 mM / −0.5%',30,NEUR).move_to([3.1,-3.08,0])),run_time=.25); self.finish()

class S09Ratio(SpokenScene):
    def construct(self):
        self.add(heading("Potassium's equilibrium potential",KC))
        # Unicode subscripts avoid LaTeX while retaining the mathematical roles.
        formula=VGroup(T('Eₖ = 61.5 mV × log₁₀(',42),T('[K⁺]ₒ',44,KC),
            T('/',42),T('[K⁺]ᵢ',44,NEUR),T(')',42)).arrange(RIGHT,buff=.20)
        if formula.width>12.2: formula.scale_to_fit_width(12.2)
        formula.move_to([0,.9,0])
        self.add(formula,T('at 37 °C',28).move_to([-3,2.45,0]))
        pools=VGroup(chip('outside: 3 mM',KC,30).move_to([formula[1].get_x(),1.95,0]),
            chip('inside: 140 mM',NEUR,30).move_to([formula[3].get_x(),-.3,0]),
            T('outside / inside',32).move_to([0,-1.55,0]))
        self.add(pools)
        self.at('depends on the ratio')
        self.play(Indicate(VGroup(formula[1],formula[3]),scale_factor=1.06),run_time=.4)
        self.at('in this model')
        self.play(FadeOut(pools),run_time=.2)
        terms=VGroup(T('Δln[K⁺]ₒ ≈ +1/3',32,KC),T('Δln[K⁺]ᵢ ≈ −0.75/140',32,NEUR)).arrange(DOWN,buff=.45).move_to([0,-.35,0])
        self.play(FadeIn(terms),run_time=.4)
        self.at('the outside change')
        glow=SurroundingRectangle(formula[1],color=KC,buff=.055,stroke_width=4)
        self.play(Create(glow),FadeIn(T('+33% outside  /  −0.5% inside',30).move_to([0,-1.5,0])),run_time=.4)
        self.at('60 times')
        self.play(FadeIn(T('about 60×',46,KC).move_to([0,-2.3,0])),
            FadeIn(T('fractional-change ratio: (140 / 3) × 1.33 ≈ 62',27).move_to([0,-3.05,0])),run_time=.4); self.finish()

class S10Ceiling(SpokenScene):
    def construct(self):
        self.add(heading('Cat cortex: strong repetitive stimulation'))
        base=-2.4; top=2.25
        b=rect(-2.4,base+4.65*.3/2,2.2,4.65*.3,KC)
        self.add(b,Line([-4.5,base,0],[4.8,base,0],color=GREY),
            T('[K⁺]ₒ (mM)',30).rotate(PI/2).move_to([-5.3,0,0]),
            DashedLine([-4.1,base+4.65*.3,0],[4.5,base+4.65*.3,0],color=GREY),
            T('3 mM at rest',28).move_to([2.7,base+4.65*.3-.38,0]))
        label=always_redraw(lambda: T(f'{b.height/4.65*10:.0f} mM',32,KC).next_to(b,UP,buff=.15)); self.add(label)
        self.at('raised outside potassium')
        self.play(b.animate.stretch_to_fit_height(4.65).move_to([-2.4,base+4.65/2,0]),run_time=1.1)
        self.at('to a ceiling')
        self.play(Create(DashedLine([-4.1,top,0],[4.7,top,0],color=KC)),
            FadeIn(T('measured ceiling',28,KC).move_to([2.6,top+.4,0])),run_time=.35)
        # Qualitative band, explicitly not a measured activity range.
        self.add(rect(1.9,-.6,4.3,.45,KC,.18),T('ordinary activity',28).move_to([1.9,-.55,0]),
            T('far below ceiling (schematic)',27).move_to([0,-3.15,0])); self.finish()

class S11Shift(SpokenScene):
    def construct(self):
        self.add(voltage_scale(),heading('Potassium alone'),T('[K⁺]ᵢ held at 140 mM',28).move_to([2.3,-2.6,0]))
        mark=kmarker(3); self.add(mark,T('3 mM outside',28,KC).move_to([-4.4,-1.5,0]))
        self.at('sits about')
        self.add(kghost()); mark=move_k(self,mark,10,.8)
        self.add(T('10 mM outside',28,KC).move_to([-.8,-1.5,0]))
        self.at('more positive')
        self.play(FadeIn(bracket(EK(3),EK(10),-2.4,'Shift: +32 mV',KC,False)),run_time=.3); self.finish()

class S12Predict(SpokenScene):
    def construct(self):
        self.add(voltage_scale(),heading('Does rest also move 32 mV?'))
        self.add(kghost(),kmarker(10),restmarker(before=True))
        self.at('resting potential')
        self.at('move that far')
        self.play(FadeIn(bracket(EK(3),EK(10),2.35,'32 mV',KC,True)),run_time=.25); self.finish()

class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction_two()); countdown(self)

class S14Reveal(SpokenScene):
    def construct(self):
        self.add(voltage_scale(),kghost(),kmarker(10),heading('Less far, the same way',NEUR),
            bracket(EK(3),EK(10),2.35,'32 mV',KC,True))
        rest=restmarker(); self.add(rest)
        self.at('in a simple model')
        # Range is the displacement 10–21 mV from the initial rest, not E_K.
        lo,hi=VM(3)+10,VM(3)+21
        band=rect((X(lo)+X(hi))/2,-1.95,X(hi)-X(lo),.3,NEUR,.32)
        self.add(band,Line([X(hi),-1.95,0],[.3,-1.95,0],color=NEUR),
            T('10–21 mV: range in simple models',27,NEUR).next_to([.3,-1.95,0],RIGHT,buff=.15))
        self.at('it moves about')
        ghost=Triangle(color=NEUR,fill_color=NEUR,fill_opacity=.2).scale(.2).move_to([X(VM(3)),-1.02,0]); self.add(ghost, T(f'{VM(3):.0f}'.replace('-','−'),26,NEUR).move_to([X(VM(3))-1,-1.02,0]))
        rest=move_rest(self,rest,restmarker(10),.7)
        self.play(FadeIn(bracket(VM(3),VM(10),-2.65,'about 16 mV',NEUR,False)),run_time=.25); self.finish()

class S15Why(SpokenScene):
    def construct(self):
        rest=restmarker(10); self.add(voltage_scale(),kmarker(10),rest,heading('What sets the resting voltage?'))
        anchor=np.array([X(VM(10)),-1.02,0])
        # Equal short ropes express permeability weight, never distance to E_ion.
        self.at('permeable to potassium')
        thick=Line(anchor,anchor+LEFT*.85,color=KC,stroke_width=12)
        klab=T('potassium:\nlarge share',28,KC).next_to(thick,LEFT,buff=.5).shift(DOWN*.45)
        self.play(Create(thick),FadeIn(klab),run_time=.4)
        self.at('sodium pulls')
        thin=Line(anchor,anchor+RIGHT*1.15,color=TEXT,stroke_width=5)
        self.play(Create(thin),FadeIn(T('sodium: small share',28).next_to(thin,RIGHT,buff=.2)),run_time=.4)
        self.add(T('Rest sits between, closer to Eₖ',30).move_to([0,-3.1,0])); self.finish()

class S16Loop(SpokenScene):
    def construct(self):
        rest=restmarker(10); self.add(voltage_scale(),kmarker(10),rest,heading('A modest rise'))
        self.at('closer to threshold')
        th=DashedLine([X(-50),-.65,0],[X(-50),1.9,0],color=NEUR)
        self.play(Create(th),FadeIn(T('threshold: −50 mV (illustrative)',28,NEUR).move_to([1.8,2.4,0])),run_time=.25)
        # Preserve the derived ceiling position; a small visual nudge has no
        # invented voltage attached to it. Keep the old position as a ghost.
        self.add(rest[0].copy().set_opacity(.25))
        new=restmarker(10)
        new[0].shift(RIGHT*.12)
        new[1].become(T('rest: closer to threshold',28,NEUR).move_to([-1.5,-1.75,0]))
        rest=move_rest(self,rest,new,.5)
        self.at('fires more easily'); self.play(Indicate(rest[0]),run_time=.35)
        self.at('more firing releases')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(loop_diagram()),run_time=.25); self.finish()

class S17Seizure(SpokenScene):
    def construct(self):
        loop=loop_diagram(); self.add(loop)
        self.at('that loop')
        self.play(loop[1].animate.set_color(BAD),run_time=.2)
        label=T('A loop that can\nfeed a seizure',30,BAD).move_to([0,0,0])
        self.at('can feed')
        self.play(FadeIn(label),LaggedStart(*[Indicate(a,color=BAD,scale_factor=1.08) for a in loop[1]],lag_ratio=.08),run_time=.6)
        self.finish(); self.wait(1.5)

class S18Block(SpokenScene):
    def construct(self):
        # The familiar quantitative scale first; no position near E_Na implied.
        scale=voltage_scale(); mark=Dot([X(-40),0,0],radius=.2,color=NEUR)
        train,flat=block_traces()
        self.add(train,T('illustrative HH model',26,GREY).move_to([0,-3.25,0]))
        self.add(scale,mark,heading('A large, sustained rise',BAD),
            T('held depolarized',34,NEUR).move_to([X(-40),-1.25,0]))
        self.at('sodium channels')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        chans=VGroup()
        for x in (-3.7,0,3.7):
            chans.add(VGroup(Rectangle(width=1.7,height=3.4,color=TEXT,stroke_width=5),
                Line([-.45,-1.7,0],[-.45,1.7,0],color=GREY),Line([.45,-1.7,0],[.45,1.7,0],color=GREY)).move_to([x,.25,0]))
        self.add(chans,T('sodium channels',32).move_to([0,2.5,0]))
        self.at('inactivate')
        gates=VGroup(*[Line([x-.85,.25,0],[x+.85,.25,0],color=BAD,stroke_width=14) for x in (-3.7,0,3.7)])
        self.play(LaggedStart(*[Create(g) for g in gates],lag_ratio=.7),run_time=1.05)
        self.add(T('inactivated  →  unavailable',30,BAD).move_to([0,-2.05,0]))
        self.at('can stop firing')
        self.add(flat,
            T('Depolarization block: firing stops',30,BAD).move_to([0,-3.25,0])); self.finish(); self.wait(.8)

class S19Rule(SpokenScene):
    def construct(self):
        self.add(T('The rule',30,GREY).move_to([0,2.8,0]))
        card=rule_card(False)
        self.at('small space outside'); self.play(FadeIn(card[0]),run_time=.4)
        self.at('big change outside'); self.play(FadeIn(card[1]),run_time=.4); self.finish()

class S20Rule2(SpokenScene):
    def construct(self):
        self.add(rule_card(),T('The rule',28,GREY).move_to([0,3.3,0]))
        inn=chip('inside: −0.5%',NEUR,34).move_to([-3.5,-.7,0])
        out=chip('outside: +33%',KC,34).move_to([3.5,-.7,0])
        arrow=Arrow([-1.6,-.7,0],[1.6,-.7,0],color=KC,buff=.1,stroke_width=6)
        self.at('a little released potassium')
        self.add(inn.copy().set_opacity(.25),out.copy().set_opacity(.25))
        self.play(GrowArrow(arrow),FadeIn(T('same K⁺ released',28,KC).move_to([0,.1,0])),run_time=.4)
        self.at('a big change outside'); self.play(FadeIn(out),run_time=.35)
        self.at('a tiny one inside'); self.play(FadeIn(inn),run_time=.35)
        self.at('comes mostly from outside')
        self.play(FadeIn(T('In this model, Eₖ shifts mostly from outside',36,KC).move_to([0,-2.5,0])),run_time=.4); self.finish(); self.wait(1)

class S21Rule3(SpokenScene):
    def construct(self):
        self.add(rule_card(),T('The rule',28,GREY).move_to([0,3.3,0]))
        neuron=blob(0,-.75,3,2.5,NEUR); self.add(neuron,T('neuron',30,NEUR).move_to([0,-.75,0]))
        glia=VGroup(blob(-4.3,-.75,3.1,2.5,ASTRO),blob(4.3,-.75,3.1,2.5,ASTRO))
        labels=VGroup(*[T('astrocytes',28,ASTRO).move_to([x,-2.25,0]) for x in (-4.3,4.3)])
        self.at('resting potential depends')
        self.play(FadeIn(T('Rest depends on clearing the space',32,NEUR).move_to([0,-3.0,0])),run_time=.3)
        self.at('cells that keep clearing')
        self.play(FadeIn(glia),FadeIn(labels),run_time=.3)
        dots=VGroup(*[kdot((x,y)) for x in (-2.1,2.1) for y in (-1.2,-.7,-.2)])
        self.add(dots)
        # Two uptake pulses show ions crossing from the extracellular gap
        # into each astrocyte, then leave a filled state visible.
        for pulse in range(2):
            incoming=dots if pulse==0 else VGroup(*[kdot((x,y)) for x in (-2.1,2.1) for y in (-1.35,-.85,-.35)])
            self.add(incoming)
            self.play(LaggedStart(*[d.animate.shift((LEFT if d.get_x()<0 else RIGHT)*(1.35+.45*pulse)) for d in incoming],lag_ratio=.12),run_time=1.1,rate_func=linear)
        self.finish(); self.wait(2)

class S22End(EndCard):
    LINE='A little potassium changes outside in proportion; cells clear it.'
    def construct(self):
        line=T('A little K⁺: a big proportional change outside.\nRest depends on cells that clear it.',36,font=TITLE_FONT).move_to([0,.4,0])
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(T('biochemistrypedia.com',26,TEAL).move_to([0,-1.5,0])),run_time=.3); self.finish()
