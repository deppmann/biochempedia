"""Pitch Becomes Place: equation-driven illustrative mechanics.
COLOR MAP: YELLOW sound/voltage; BLUE membrane; ORANGE high frequency;
PURPLE low frequency; TEAL hair cells/tonotopy; GREEN amplification;
GOLD stiffness; GREY passive response. No molecular structures.
Envelopes are asymmetric Gaussian illustrative models from scenes.old.py,
not digitized experimental data. Greenwood positions use the lesson equation.
"""
import numpy as np
from bp_style import *

ORANGE, PURPLE = '#F29E4C', '#B58CD9'
GREY = '#ADB5C4'
X0, X1, LEN = -5.5, 5.5, 11.

def label(s,x,y,color=TEXT,size=28):
    return T(s,size=size,color=color).move_to([x,y,0])

def trace(xs,ys,color,sw=5):
    return VMobject().set_points_as_corners(np.c_[xs,ys,np.zeros_like(xs)]).set_stroke(color,sw).set_fill(opacity=0)

def width_at(f): return .65+1.35*f

def strip(cy=-1.8,mapped=False,scale=1):
    g=VGroup()
    for i in range(48):
        a,b=i/48,(i+1)/48
        col=interpolate_color(ManimColor(ORANGE),ManimColor(PURPLE),(a+b)/2) if mapped else BLUE
        g.add(Polygon([X0+LEN*a,cy+scale*width_at(a)/2,0],[X0+LEN*b,cy+scale*width_at(b)/2,0],
                      [X0+LEN*b,cy-scale*width_at(b)/2,0],[X0+LEN*a,cy-scale*width_at(a)/2,0],
                      stroke_width=0,fill_color=col,fill_opacity=.5))
    return g

def haircell(h=.7,w=.4,color=TEAL):
    body=RoundedRectangle(width=w,height=h,corner_radius=w*.32,color=color,fill_opacity=.3).move_to([0,h/2,0])
    k=max(.35,h*.19)
    bundle=VGroup(*[Line([dx*w,h,0],[dx*w,h+k*f,0],color=color,stroke_width=4) for dx,f in [(-.3,.45),(0,.72),(.3,1)]])
    g=VGroup(body,bundle); g.body=body; g.bundle=bundle
    return g

def cells(active=(),cy=-1.8,scale=1):
    if isinstance(active,(int,float)): active=(active,)
    g=VGroup()
    # Keep the two demonstrated places exactly centred on their guide lines.
    for f in [.07,.1775,.28,.3925,.5,.6075,.715,.85,.93]:
        col=GREEN if any(abs(f-a)<.065 for a in active) else TEAL
        g.add(haircell(color=col).shift([X0+LEN*f,cy+scale*width_at(f)/2,0]).set_opacity(1 if col==GREEN else .65))
    return g

def stage(mapped=False,active=()):
    return VGroup(strip(mapped=mapped),cells(active),label('base',-5.1,-3.05),label('apex',5.1,-3.05))

def peak_curve(x,xp,h,wl,wr):
    return h*np.exp(-np.where(x<xp,(x-xp)/wl,(x-xp)/wr)**2)

def curve(xp=.28,h=1.0,wl=1.5,wr=.65,color=ORANGE,y0=1.2):
    xs=np.linspace(X0,X1,480)
    return trace(xs,y0+peak_curve(xs,X0+LEN*xp,h,wl,wr),color)

def env(xp=.28,amp=1.0,color=ORANGE):
    # The envelope and oscillatory trace use exactly the same model.
    xs=np.linspace(0,LEN,480); s=xs/(LEN*xp)
    e=np.exp(-((s-1)/np.where(s<1,.62,.055 if xp>.7 else .3))**2)
    return trace(X0+xs,1.2+amp*e,color,4)

def wave(xp=.28,t=0,amp=1.0,color=ORANGE,front=1):
    xs=np.linspace(0,LEN,480); s=xs/(LEN*xp)
    e=np.exp(-((s-1)/np.where(s<1,.62,.055 if xp>.7 else .3))**2)
    phi=2*np.pi*4*(.35*s+.65*s**3)  # increasing local wavenumber: slows toward the peak
    gate=np.clip((front*LEN-xs)*5,0,1)
    return trace(X0+xs,1.2+amp*e*np.sin(phi-2*np.pi*.7*t)*gate,color)

def guide(f,col):
    x=X0+LEN*f
    return DashedLine([x,1.15,0],[x,-1.8+width_at(f)/2+.7,0],color=col,stroke_width=2)

def axis(y=1.2): return Line([X0,y,0],[X1,y,0],color=GREY,stroke_width=2)
def model_note(): return label('Illustrative mechanical model',-3.1,-3.5,GREY,26)

def peak_labels():
    return VGroup(label('high tone',-2.6,2.8,ORANGE,30),label('low tone',4,2.8,PURPLE,30))

def question():
    xs=np.linspace(-5.5,-3.4,100)
    return VGroup(stage(active=(.28,)),axis(),env().set_stroke(opacity=.35),
                  trace(xs,1.2+.32*np.sin(2*np.pi*(xs+5.5)/1.4),PURPLE),
                  label('low tone',-4.8,2.55,PURPLE),label('Where will it peak?',0,3.05,PURPLE,36),
                  label('?',4.8,2.55,PURPLE,64))

def row_view(inner=False):
    mem=Rectangle(width=12.3,height=.30,color=BLUE,fill_opacity=.5).move_to([0,-2.50,0])
    cs=VGroup(*[haircell(3.45,1.05,TEAL).scale(1.3,about_point=ORIGIN).shift([x,-2.35,0]) for x in [-4,-.8,1.8,4.4]])
    for i,c in enumerate(cs):
        c.set_color(TEAL if i==0 else GREEN).set_opacity(1 if (i==0)==inner else .28)
    names=VGroup(label('inner hair cell',-4,3.5,TEAL,28),label('outer hair cells',1.8,3.5,GREEN,30),
                 label('1 inner row',-4,-2.93,TEAL,26),label('3 outer rows',1.8,-2.93,GREEN,26))
    return VGroup(mem,cs,names)

def brace(deflected=False):
    # Fixed upper contact; shortening raises the lower membrane.
    c=haircell(4.55,1.35).shift([-3.6,-2.55,0])
    if deflected: c.bundle.rotate(-.85,about_point=c.body.get_top())
    lower=Rectangle(width=4.3,height=.22,color=BLUE,fill_opacity=.5).move_to([-3.6,-2.66,0])
    upper=Rectangle(width=4.3,height=.22,color=GREY,fill_opacity=.35).move_to([-3.6,2.98,0])
    return VGroup(c,lower,upper)

def loop_brace():
    b=brace()
    # Derive membrane position from the actual cell bottom at every frame,
    # including after bundle rotation, rather than guessing a displacement.
    b[1].add_updater(lambda bar: bar.move_to(b[0].get_bottom()+DOWN*.19))
    b[1].update()
    return b

def loop_labels(n):
    # Clockwise circuit, deliberately spatial rather than a vertical text list.
    specs=[('membrane\nmoves',(.5,1.9),BLUE),('bundle\npushed',(4.5,1.9),TEAL),
           ('voltage\nswings',(4.5,-.2),YELLOW),('prestin changes\nlength',(.5,-.2),GREEN),
           ('adds energy\nnear the peak',(.5,-2.25),GREEN)]
    g=VGroup(*[label(s,*p,c,28) for s,p,c in specs[:n]])
    if n>=4:
        g[3].become(VGroup(T('prestin changes',size=28,color=GREEN),T('length',size=28,color=GREEN))
                    .arrange(DOWN,aligned_edge=LEFT,buff=.14).move_to([.3,-.2,0]))
    paths=[((1.7,1.9),(3.3,1.9)),((4.5,1.1),(4.5,.6)),((3.4,-.2),(2.35,-.2)),((.5,-.9),(.5,-1.5))]
    for a,b in paths[:max(0,n-1)]: g.add(Arrow([*a,0],[*b,0],color=GREY,buff=.05))
    if n==5:
        g.add(VMobject().set_points_as_corners([[1.9,-2.3,0],[6,-2.3,0],[6,3.1,0],[.5,3.1,0],[.5,2.65,0]]).set_stroke(GREEN,3),
              Arrow([.5,3.1,0],[.5,2.6,0],color=GREEN,buff=0,tip_length=.16))
    return g

def meter(x=-1.4,y=.7,positive=True):
    return VGroup(label('voltage',x,y+1.1,YELLOW,26),Line([x,y-.65,0],[x,y+.65,0],color=YELLOW),
                  label('+',x+.35,y+.65,YELLOW),label('−',x+.35,y-.65,YELLOW),
                  Dot([x,y+(.48 if positive else -.48),0],color=YELLOW,radius=.12))

def comparison(active=True):
    g=VGroup(axis(-2.55),label('base',-5.1,-3),label('apex',5.1,-3),
             curve(.55,2.9,3,1.3,GREY,-2.55),
             label("Békésy's measured peak",-3.25,1.15,GREY,28),label('(dead cochleas)',-3.25,.65,GREY,26))
    # Leader attaches the label to the broad illustrative envelope.
    g.add(Line([-3,.2,0],[-1.6,-.75,0],color=GREY,stroke_width=2))
    if active: g.add(curve(.55,4.8,1,.5,GREEN,-2.55),label('living ear',3,2.1,GREEN,30))
    return g

class S00Title(TitleCard):
    LESSON='Hearing and Balance'
    TITLE='Pitch Becomes Place'

class S01Question(SpokenScene):
    def construct(self):
        xs=np.linspace(-5.2,5.2,500)
        self.add(label('High or low?',0,3.1,size=40),trace(xs,1.25+.65*np.sin(9*np.pi*xs/5.2),ORANGE),
                 trace(xs,-1.25+.65*np.sin(2*np.pi*xs/5.2),PURPLE))
        self.at('How does your ear')
        self.play(FadeIn(label('high • many cycles per second',0,2.35,ORANGE,30)),run_time=.4)
        self.at('whether a tone')
        self.play(FadeIn(label('low • few cycles per second',0,-2.4,'#D8B7F4',30)),run_time=.4)
        self.finish()

class S02Uncoil(SpokenScene):
    def construct(self):
        ts=np.linspace(0,5*np.pi,400)
        r=2.8-2.45*ts/ts[-1]
        pts=np.c_[-r*np.cos(ts),r*np.sin(ts),np.zeros_like(ts)]
        k=ValueTracker(0)
        straight=np.c_[np.linspace(X0,X1,len(ts)),np.full_like(ts,-.6),np.zeros_like(ts)]
        coil=always_redraw(lambda:VMobject().set_points_smoothly((1-k.get_value())*pts+k.get_value()*straight).set_stroke(BLUE,24))
        base=label('base',-3.6,-.3,BLUE)
        self.add(coil,base,label('cochlea',0,3.2,BLUE,34))
        self.at('Uncoil the cochlea')
        self.play(k.animate.set_value(1),base.animate.move_to([-5.5,-3.35,0]),run_time=2.9)
        tube=RoundedRectangle(width=11.7,height=4.9,corner_radius=.5,color=BLUE).move_to([0,-.45,0])
        self.remove(coil); self.add(tube)
        self.at('Along it runs')
        self.play(FadeIn(strip()),FadeIn(label('basilar membrane',0,-3.35,BLUE,28)),run_time=.35)
        self.at('carrying the hair cells')
        snd=Arrow([-6.5,-.5,0],[-5.5,-.5,0],color=YELLOW,buff=0)
        self.play(FadeIn(cells()),FadeIn(label('hair cells',0,1.5,TEAL)),GrowArrow(snd),FadeIn(label('sound in',-5.5,2.55,YELLOW,26)),run_time=.5)
        self.finish()

class S03Gradient(SpokenScene):
    def construct(self):
        self.add(strip(cy=-.3,scale=2.35),cells(cy=-.3,scale=2.35),label('base',-5.1,-3.25),label('apex',5.1,-3.25))
        self.at('Near the base')
        self.play(GrowArrow(Arrow([-6.5,-.3,0],[-5.5,-.3,0],buff=0,color=YELLOW)),FadeIn(label('sound in',-5.8,1.75,YELLOW,26)),Create(Line([-6,1.42,0],[-6,-.1,0],color=YELLOW,stroke_width=2)),run_time=.4)
        self.at('narrow and stiff')
        self.play(FadeIn(label('narrow and stiff',-3.7,-1.9,GOLD)),Create(Line([-4,-1.6,0],[-5,-1,0],color=GOLD)),run_time=.4)
        self.at('Toward the apex')
        self.play(FadeIn(label('wide and floppy',2.5,-3.2,GOLD)),Create(Line([3,-2.9,0],[4.9,-2.3,0],color=GOLD)),run_time=.5)
        self.finish()

class S04Natural(SpokenScene):
    def construct(self):
        st=strip(cy=-.3,scale=2.35)
        self.add(st,cells(cy=-.3,scale=2.35),label('base',-5.1,-3.25),label('apex',5.1,-3.25))
        self.at('each place has')
        self.play(Transform(st,strip(cy=-.3,scale=2.35,mapped=True)),run_time=.7)
        self.at('natural frequency')
        self.play(FadeIn(label('natural frequency',0,3.3,size=34)),run_time=.3)
        self.at('high where')
        self.play(FadeIn(label('high',-4,-1.8,ORANGE,34)),run_time=.3)
        self.at('low where')
        self.play(FadeIn(label('low',3,-2.9,PURPLE,34)),run_time=.3)
        self.finish()

class S05Wave(SpokenScene):
    def construct(self):
        self.add(stage(),axis(),label('travelling wave',0,3.1,YELLOW,34),model_note())
        p=ValueTracker(-.5)
        def ripple():
            xs=np.linspace(0,LEN,420); q=p.get_value()
            ys=1.2+.45*np.exp(-((xs-q)/.8)**2)*np.sin(2*np.pi*(xs-q)/.65)
            return trace(X0+xs,ys,YELLOW)
        w=always_redraw(ripple)
        def moving_guide():
            f=np.clip(p.get_value()/LEN,0,1); x=X0+LEN*f
            return DashedLine([x,1.17,0],[x,-1.8+width_at(f)/2+.75,0],color=YELLOW,stroke_width=2).set_opacity(np.clip((LEN+.6-p.get_value())/1.1,0,1))
        self.add(w,always_redraw(moving_guide))
        self.at('Sound sets up')
        self.play(p.animate.set_value(1.8),run_time=1)
        self.at('that moves')
        self.play(p.animate.set_value(12.2),run_time=max(.2,self.narration_s+.35-self.elapsed()),rate_func=linear)
        self.finish()

class S06High(SpokenScene):
    def construct(self):
        self.add(stage(),axis(),label('high tone',-2.5,3.05,ORANGE,34),model_note())
        a=ValueTracker(.3); tm=ValueTracker(0)
        w=always_redraw(lambda:wave(.28,tm.get_value(),a.get_value()))
        self.add(w)
        self.at('slows and grows')
        self.play(a.animate.set_value(1.0),tm.animate.set_value(1.07142857),run_time=2,rate_func=linear)
        self.at('close to the base')
        self.play(Create(guide(.28,ORANGE)),run_time=.4)
        self.finish()

class S07Peak(SpokenScene):
    def construct(self):
        st=stage(); self.add(st,axis(),wave(.28,1.07142857),label('high tone',-2.5,3.05,ORANGE,34),model_note(),guide(.28,ORANGE))
        self.at('It peaks there')
        self.play(Create(env()),Transform(st[1],cells(.28)),run_time=.55)
        self.at('then dies away')
        self.play(FadeIn(label('dies away',.7,1.65,ORANGE)),run_time=.35)
        self.finish()

class S08Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q)
        self.at('a low tone enters')
        self.play(Indicate(q[3],color=PURPLE,scale_factor=1.1),run_time=.6)
        self.at('Where will its wave peak')
        self.play(Indicate(q[-1],color=PURPLE),run_time=.6)
        self.finish()

class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question()); self.wait(5)

class S10Reveal(SpokenScene):
    def construct(self):
        st=stage(active=(.28,)); self.add(st,axis(),env().set_stroke(opacity=.35),label('low tone',4,3.05,PURPLE,34),model_note())
        fr=ValueTracker(.22); tm=ValueTracker(0)
        w=always_redraw(lambda:wave(.85,tm.get_value(),1.0,PURPLE,fr.get_value())); self.add(w)
        self.at('near the apex')
        self.play(fr.animate.set_value(1),tm.animate.set_value(1.07142857),run_time=1.1)
        self.at('where the membrane')
        self.play(Create(env(.85,1.0,PURPLE)),Transform(st[1],cells((.28,.85))),Create(guide(.85,PURPLE)),run_time=.6)
        self.finish()

class S11Place(SpokenScene):
    def construct(self):
        self.add(stage(True,(.28,.85)),axis(),env(),env(.85,1.0,PURPLE),peak_labels(),guide(.28,ORANGE),guide(.85,PURPLE),
                 label('frequency → position • tonotopy',0,3.55,TEAL,32),label('high',-3.9,-2.7,'#FFC285',26),label('low',3.8,-3.12,'#D8B7F4',26))
        self.at('Frequency becomes position')
        self.finish()

class S12Ruler(SpokenScene):
    def construct(self):
        def px(f): return X1-LEN*np.log10(f/165.4+.88)/2.1
        self.add(strip(cy=.1,mapped=True,scale=1.7),label('Greenwood map • human cochlea',0,3.4,size=30),
                 label('mm from apex',-3.9,2.75,GREY,26),label('base',-5.7,-1.25),label('apex',5.8,-1.9))
        hi=VGroup(); fs=[16000,8000,4000,2000,1000]
        for f in fs:
            x=px(f); mm=35*np.log10(f/165.4+.88)/2.1
            hi.add(Line([x,.1+1.7*width_at((x-X0)/LEN)/2,0],[x,1.55,0],color=ORANGE),
                   label(f'{f//1000} kHz',x,1.85,ORANGE,26),label(f'{mm:.1f}',x,2.3,GREY,26))
        self.at('Above about'); self.play(FadeIn(hi),run_time=.5)
        brackets=VGroup()
        for a,b in zip(fs,fs[1:]):
            xa,xb=px(a),px(b)
            brackets.add(Line([xa,.9,0],[xb,.9,0],color=ORANGE),Line([xa,.8,0],[xa,1,0],color=ORANGE),
                         Line([xb,.8,0],[xb,1,0],color=ORANGE),label('≈ 5 mm',(xa+xb)/2,.5,ORANGE,26))
        self.at('each doubling of frequency'); self.play(FadeIn(brackets),run_time=.45)
        low=VGroup()
        # Ordered callouts fan out below their real, increasingly close tick positions.
        for f,lx,ly in [(500,.5,-2.5),(250,2.1,-2.5),(125,3.7,-2.5),(62,5.2,-2.5)]:
            x=px(f); bottom=.1-1.7*width_at((x-X0)/LEN)/2
            low.add(Line([x,bottom+.2,0],[x,bottom-.12,0],color=PURPLE,stroke_width=4),
                    Line([x,bottom-.12,0],[lx,ly+.25,0],color=PURPLE),label(f'{f} Hz',lx,ly,PURPLE,26))
        self.at('nearly the same length'); self.play(FadeIn(low),run_time=.45)
        self.add(Line([-5.5,-3.1,0],[5.5,-3.1,0],color=GREY),Line([-5.5,-3,0],[-5.5,-3.2,0],color=GREY),Line([5.5,-3,0],[5.5,-3.2,0],color=GREY),label('35 mm assumed',0,-3.55,GREY,26))
        self.finish()

class S13Bekesy(SpokenScene):
    def construct(self):
        self.add(comparison(False),label('Georg von Békésy • 1961 Nobel Prize',0,3.25,size=30))
        self.at('His peaks were far broader')
        self.play(Create(curve(.55,4.8,1,.5,GREEN,-2.55)),FadeIn(label('living ear',3,2.1,GREEN,30)),run_time=.7)
        self.finish()

class S14Ohc(SpokenScene):
    def construct(self):
        rv=row_view(); rv[1][1:].set_opacity(.28); self.add(rv)
        self.at('adds energy')
        self.play(FadeIn(label('adds energy',0,-3.5,GREEN,36)),run_time=.35)
        self.at('the outer hair cells')
        self.play(rv[1][0].animate.set_opacity(.22),rv[1][1:].animate.set_opacity(1),run_time=.35)
        self.play(*[Indicate(c,color=GREEN,scale_factor=1.06) for c in rv[1][1:]],run_time=.6)
        self.finish()

class S15Prestin(SpokenScene):
    def construct(self):
        c=haircell(4.1,1.65).shift([0,-2.85,0]); v=meter(-2.6,.4)
        self.add(c,v,label('outer hair cell',0,3.5,TEAL,30))
        self.at('They change length')
        self.play(Transform(v,meter(-2.6,.4,False)),c.animate.stretch(1.2,1,about_point=c.get_bottom()),run_time=.6)
        self.at('when their voltage changes')
        self.play(Transform(v,meter(-2.6,.4)),c.animate.stretch(.8/1.2,1,about_point=c.get_bottom()),run_time=.65)
        self.play(Transform(v,meter(-2.6,.4,False)),c.animate.stretch(1/.8,1,about_point=c.get_bottom()),run_time=.5)
        self.at('The motor is')
        self.play(FadeIn(label('electromotility',3,1.8,TEAL,34)),run_time=.3)
        self.at('membrane protein called')
        self.play(FadeIn(chip('prestin',GREEN,34).move_to([3,.2,0])),FadeIn(VGroup(T('voltage driven',size=30),T('not ATP',size=30)).arrange(DOWN,buff=.25).move_to([3,-1.3,0])),run_time=.45)
        self.finish()

class S16Brace(SpokenScene):
    def construct(self):
        b=brace(); self.add(b[0])
        self.at('is braced between'); self.play(FadeIn(b[1:]),run_time=.4)
        self.at('basilar membrane')
        lower_name=label('basilar membrane',2,-2.65,BLUE,30)
        self.play(FadeIn(lower_name),run_time=.35)
        self.at('structures above it')
        self.play(FadeIn(label('structures above',2,2.98,GREY,30)),run_time=.35)
        arrows=VGroup(Arrow([-4.65,-1.8,0],[-4.65,-2.55,0],color=GREEN,buff=0),Arrow([-4.65,2.2,0],[-4.65,2.85,0],color=GREEN,buff=0))
        self.play(FadeIn(arrows),b[0].animate.stretch(.84,1,about_point=b[0].get_top()),b[1].animate.shift(UP*.86),lower_name.animate.shift(UP*.86),run_time=.65)
        self.finish()

class S17Loop1(SpokenScene):
    def construct(self):
        b=loop_brace(); self.add(b,label('outer hair cell',-3.6,3.5,TEAL,28))
        self.at('The membrane moves')
        self.play(b[0].animate.stretch(.917,1,about_point=b[0].get_top()),FadeIn(loop_labels(1)),run_time=.55)
        self.at("cell's bundle is pushed")
        self.play(Rotate(b[0].bundle,-.85,about_point=b[0].body.get_top()),FadeIn(loop_labels(2)[1:]),
                  GrowArrow(Arrow([-5,2.45,0],[-3.8,2.45,0],color=YELLOW,buff=0)),run_time=.55)
        self.finish()

class S18Loop2(SpokenScene):
    def construct(self):
        b=loop_brace(); b[0].stretch(.917,1,about_point=b[0].get_top()); b[0].bundle.rotate(-.85,about_point=b[0].body.get_top()); self.add(b,loop_labels(2),label('outer hair cell',-3.6,3.5,TEAL,28))
        v=meter(-5.8,.3)
        self.at('Its voltage swings')
        self.play(FadeIn(loop_labels(3)[2:]),FadeIn(v),run_time=.4)
        self.at('shortens and lengthens')
        self.play(FadeIn(loop_labels(4)),b[0].animate.stretch(.8,1,about_point=b[0].get_top()),Transform(v,meter(-5.8,.3,False)),run_time=.65)
        self.play(b[0].animate.stretch(1.25,1,about_point=b[0].get_top()),Transform(v,meter(-5.8,.3)),run_time=.65)
        self.finish()

class S19Loop3(SpokenScene):
    def construct(self):
        b=loop_brace(); b[0].stretch(.917,1,about_point=b[0].get_top()); b[0].bundle.rotate(-.85,about_point=b[0].body.get_top()); self.add(b,loop_labels(4))
        force=always_redraw(lambda:Arrow(b[1].get_center()+LEFT*1.3,b[1].get_center()+LEFT*1.3+UP*.95,color=GREEN,buff=0))
        self.at('Its push is timed'); self.add(force)
        self.play(b[0].animate.stretch(.85,1,about_point=b[0].get_top()),run_time=.6)
        self.at('go with')
        force.clear_updaters(); self.remove(force)
        down=always_redraw(lambda:Arrow(b[1].get_center()+LEFT*1.3,b[1].get_center()+LEFT*1.3+DOWN*.75,color=GREEN,buff=0)); self.add(down)
        self.play(b[0].animate.stretch(1/.85,1,about_point=b[0].get_top()),run_time=.6)
        self.at('like pushing a swing')
        self.play(FadeIn(loop_labels(5)),run_time=.4)
        self.at('That adds energy')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        self.add(comparison(False)); growing=curve(.55,2.9,3,1.3,GREY,-2.55); self.add(growing)
        self.play(Transform(growing,curve(.55,4.8,1,.5,GREEN,-2.55)),FadeIn(label('living ear',3,2.1,GREEN,30)),run_time=1.1)
        self.finish()

class S20Motor(SpokenScene):
    def construct(self):
        self.add(comparison(),label('the same switch, used as a motor',0,3.25,GREEN,32))
        self.at('It sharpens tuning')
        self.play(FadeIn(label('sharper tuning',3.6,.8,GREEN,28)),run_time=.4)
        self.at('raises sensitivity')
        self.play(FadeIn(label('more sensitivity',3.6,.1,GREEN,28)),run_time=.4)
        self.finish()

# Fixed mechanical-response threshold; loss of amplification raises the required
# sound INPUT. Curves remain on the same response scale in both panels.
def response(x,h,wl,wr,col):
    xs=np.linspace(x-2.05,x+2.05,300)
    return trace(xs,-2.5+peak_curve(xs,x,h,wl,wr),col)

def detection(active=True):
    g=VGroup(label('quiet',-3,-3, size=32),label('loud',1.1,-3,size=32),
             label('Illustrative response model',0,3.4,GREY,26))
    for x in [-3,1.1]:
        g.add(Line([x-1.8,-2.5,0],[x+1.8,-2.5,0],color=GREY))
    g.add(Line([-5.35,-2.5,0],[-5.35,2.6,0],color=GREY),label('relative response',-6,0,GREY,26).rotate(PI/2))
    threshold=label('illustrative\ndetection threshold\nfor this tone',4.65,.15,YELLOW,26)
    g.add(DashedLine([-5.25,.15,0],[threshold.get_left()[0]-.32,.15,0],color=YELLOW),threshold)
    g.add(response(-3,3.25 if active else 1,.45 if active else 1.1,.3 if active else .75,GREEN if active else GREY),
          response(1.1,4.8 if active else 4.15,.45 if active else 1.1,.3 if active else .75,GREEN if active else GREY))
    return g

def boosts():
    g=VGroup()
    for x,h in [(-4.5,1.65),(-.5,.55)]:
        bar=Rectangle(width=.3,height=h,color=GREEN,fill_opacity=.5).move_to([x,-2.5+h/2,0])
        g.add(bar,label('boost',x,-2.95,GREEN,26),haircell(.7,.4,GREEN).shift([x+.5,-2.5,0]))
    return g

class S21Loss(SpokenScene):
    def construct(self):
        d=detection(); self.add(d); bars=boosts()
        self.at('The boost is largest'); self.play(FadeIn(bars),run_time=.5)
        self.at('Lose the outer hair cells')
        self.play(FadeOut(bars),Transform(d,detection(False)),run_time=2.1)
        self.at('threshold of hearing rises')
        self.play(FadeIn(label('quiet sounds fall\nbelow the threshold',-3,.85,GREY,26)),run_time=.4)
        self.at('quiet sounds drop below it')
        self.play(Indicate(d[-2],color=PURPLE,scale_factor=1),run_time=.5)
        self.finish()

class S22Loud(SpokenScene):
    def construct(self):
        self.add(detection(False),response(1.1,4.8,.45,.3,GREEN).set_stroke(opacity=.5))
        self.at('If the inner hair cells')
        self.play(FadeIn(label('inner hair cells + nerve fibres still work',0,-3.6,TEAL,26)),run_time=.5)
        self.at('sounds above the new threshold')
        self.play(FadeIn(label('still heard',4.75,2.5,GREEN,28)),run_time=.5)
        self.at('But tuning blurs')
        self.play(FadeIn(label('broad tuning',4.8,-1.6,GREY,28)),Create(Line([3.5,-1.6,0],[2,-1.5,0],color=GREY)),run_time=.5)
        self.finish()

class S23Ihc(SpokenScene):
    def construct(self):
        rv=row_view(True); self.add(rv)
        self.at('Inner hair cells'); self.play(Indicate(rv[1][0],color=TEAL,scale_factor=1.04),run_time=.5)
        fibres=VGroup(*[Line([-4+d,-2.50,0],[-4+1.7*d,-3.3,0],color=TEAL,stroke_width=3) for d in np.linspace(-.45,.45,9)],
                     *[Line([x,-2.50,0],[x,-3.18,0],color=GREY,stroke_width=1.5) for x in [-.8,1.8,4.4]])
        # Row labels retain exactly their s14 position; mask the short fibre sections
        # behind them with opaque backgrounds, keeping both labels and fibres legible.
        for l in rv[2][2:]: l.add_background_rectangle(color=BG,opacity=1,buff=.08)
        self.at('supply most of the auditory nerve')
        fibres.add(Line([-4.8,-3.3,0],[-3.2,-3.3,0],color=TEAL,stroke_width=3))
        self.play(Create(fibres),FadeIn(label('auditory nerve',-3.9,-3.6,TEAL,26)),run_time=.6)
        self.bring_to_front(rv[2])
        self.at('They report the place')
        bar=VGroup(Line([-.5,-3.42,0],[5.5,-3.42,0],color=BLUE),Dot([3,-3.42,0],color=GREEN,radius=.12),
                   label('base',-.5,-3.64,size=22),label('apex',5.5,-3.64,size=22),label('active place',2.8,-3.64,GREEN,22))
        self.play(FadeIn(bar),run_time=.4)
        self.finish()

class S24Takeaway(SpokenScene):
    def construct(self):
        st=stage(True,(.28,.85))
        self.add(st,axis(),env(),env(.85,1.0,PURPLE),peak_labels(),guide(.28,ORANGE),guide(.85,PURPLE))
        self.at('The brain reads pitch')
        # Nerves emerge below the membrane at the two active-cell positions.
        # Their stems start outside its body and converge on a downward output.
        roots=[(X0+LEN*f,-1.8-width_at(f)/2-.06) for f in (.28,.85)]
        nerve=VGroup(*[Line([x,y,0],[x,-3.15,0],color=TEAL) for x,y in roots],
                     Line([roots[0][0],-3.15,0],[roots[1][0],-3.15,0],color=TEAL),
                     Arrow([.4,-3.15,0],[.4,-3.65,0],color=TEAL,buff=0,tip_length=.16),
                     label('to the brain',2.2,-3.6,TEAL,30))
        self.play(FadeIn(nerve),run_time=.4)
        self.at('from where the active cells are'); self.finish(); self.wait(2.5)

class S25End(EndCard):
    LINE='The brain reads pitch from where the active cells are.'
