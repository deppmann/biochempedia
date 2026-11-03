"""Chapter 2: Four Cells and One Switch.
COLOR MAP: VIOLET inner lineage; ORANGE outer lineage; TEAL Notch on;
GREY neutral cells / Notch off; RED warming / Notch removal; YELLOW Numb.
All timeline coordinates derive from the narrated 0, 14, 20 hours.
Pulse windows indicate experimental interventions, not continuous Notch activity.
"""
from bp_style import *
import numpy as np
ORANGE='#F29E4C'
VIOLET='#A98BE0'
OFF='#B8BEC9'
LESSON_TITLE='Asymmetric Division: Numb and the Neuroblast'

def label(text,color=TEXT,x=0,y=0,size=28):
    return T(text,size=size,color=color).move_to([x,y,0])
def head(text): return label(text,x=0,y=3.25,size=30)
def cell(c,r,color=GREY,op=.14):
    return Circle(radius=r,stroke_color=color,stroke_width=4,fill_color=color,fill_opacity=op).move_to(c)
def arr(a,b,color=TEAL): return Arrow(a,b,buff=0,color=color,stroke_width=6,tip_length=.23)
def node(text,x,y,color=GREY,r=.46,size=28):
    return VGroup(cell([x,y,0],r,color),label(text,color,x,y-r-.36,size)) if text else VGroup(cell([x,y,0],r,color))
def tree(blank=False,neurons=False):
    root=VGroup(cell([0,2.2,0],.43),label('precursor',TEXT,1.55,2.2,28))
    mids=VGroup(*[VGroup(cell([x,.45,0],.47,c),label(n,c,x+(-1.35 if x<0 else 1.35),.45,28)) for x,c,n in [(-2.8,VIOLET,'inner'),(2.8,VIOLET if neurons else ORANGE,'inner' if neurons else 'outer')]])
    xs=[-4.4,-1.3,1.3,4.4]
    leaves=VGroup(*[node('neuron' if neurons else ('?' if blank else ['neuron','sheath','hair','socket'][i]),x,-1.65,VIOLET if neurons or i<2 else ORANGE) for i,x in enumerate(xs)])
    if neurons:
        for n in leaves: n[0].set_fill(VIOLET,.65)
    edges=VGroup(*[Line([0,1.77,0],[x,.92,0],color=c) for x,c in [(-2.8,VIOLET),(2.8,VIOLET if neurons else ORANGE)]],*[Line([(-2.8 if i<2 else 2.8),-.02,0],[x,-1.19,0],color=VIOLET if neurons or i<2 else ORANGE) for i,x in enumerate(xs)])
    return VGroup(edges,root,mids,leaves)
def compact_tree(neurons=False):
    t=tree(blank=not neurons,neurons=neurons)
    t[0].stretch(.73,0,about_point=ORIGIN).shift(LEFT*1.45)
    for group in [t[1], *t[2], *t[3]]:
        for m in group:
            c=m.get_center(); m.move_to([c[0]*.73-1.45,c[1],0])
    t[1][1].next_to(t[1][0],RIGHT,buff=.25)
    for i,n in enumerate(t[2]): n[1].next_to(n[0],LEFT if i==0 else RIGHT,buff=.22)
    return t

def blank_badges():
    # One badge per division (branch point), evenly spaced and clear of node labels and branches.
    bs=[chip('Notch ?',OFF,size=26).move_to(p) for p in ([-1.95,2.2,0],[-4.3,1.4,0],[4.3,1.4,0])]
    leaders=VGroup(Line(bs[0].get_right(),[-.43,2.2,0],color=OFF),Line(bs[1].get_right(),[-3.2,.72,0],color=OFF),Line(bs[2].get_left(),[3.2,.72,0],color=OFF))
    return VGroup(leaders,VGroup(*bs))
def sisters(): return VGroup(cell([-2.1,.25,0],2.1),cell([2.1,.25,0],2.1))
def receptor():
    return VGroup(RoundedRectangle(width=.38,height=1.25,corner_radius=.08,color=TEAL,fill_color=TEAL,fill_opacity=.6).move_to([.15,.65,0]),RoundedRectangle(width=.7,height=.42,corner_radius=.06,color=TEAL,fill_color=TEAL,fill_opacity=.9).move_to([.7,.65,0]))
def delta(): return RoundedRectangle(width=.65,height=.6,corner_radius=.07,color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([-.45,.65,0])
def signal_labels():
    return VGroup(label('Delta',TEAL,-1.6,2.9,30),label('Notch',TEAL,1.5,2.9,30),Line([-1.4,2.6,0],[-.45,1.02,0],color=TEAL),Line([1.3,2.6,0],[.15,1.35,0],color=TEAL))
def signal_stage(): return VGroup(sisters(),receptor(),delta(),signal_labels())
def thermal_stage():
    therm=VGroup(RoundedRectangle(width=.6,height=3.6,corner_radius=.28,color=OFF).move_to([-2.1,.1,0]),cell([-2.1,-1.9,0],.55,OFF,.15),Line([-2.1,-1.9,0],[-2.1,.1,0],color=TEAL,stroke_width=15))
    return VGroup(therm,chip('Notch',TEAL,size=60).move_to([1.4,.1,0]))
def tx(h): return -4.8+9.6*h/20

def timeline():
    axis=Line([tx(0),-.45,0],[tx(20),-.45,0],color=OFF,stroke_width=5)
    ticks=VGroup(*[VGroup(Line([tx(h),-.6,0],[tx(h),-.3,0],color=OFF),label(str(h),OFF,tx(h),-.95,30)) for h in [0,14,20]])
    pupa=VGroup(Ellipse(width=.65,height=1.15,color=GOLD,fill_color=GOLD,fill_opacity=.25).move_to([-5.65,1,0]),label('pupa',GOLD,-5.65,2,26))
    bracket=VGroup(Line([tx(14),-1.55,0],[tx(20),-1.55,0],color=OFF),*[Line([tx(h),-1.4,0],[tx(h),-1.7,0],color=OFF) for h in [14,20]],label('precursors divide',TEXT,2.9,-2.1,28))
    return VGroup(axis,ticks,pupa,bracket,label('hours after pupa formation',OFF,0,-3.05,28))
def pulse(a,b):
    return Rectangle(width=tx(b)-tx(a),height=1.35,color=RED,fill_color=RED,fill_opacity=.65).move_to([(tx(a)+tx(b))/2,.65,0])
def window_stage(late=False):
    return VGroup(head('Notch removed by warming'),timeline(),pulse(14,20) if late else pulse(0,14),label('around division' if late else 'before division',TEXT,-.6,2.05,32))
def mini_window(late=False):
    # A compact, fully labelled intervention strip; labels remain full size.
    return VGroup(label('Notch removed '+('14–20 h' if late else '0–14 h'),RED,0,3.3,28),Rectangle(width=2 if late else 4.6,height=.18,color=RED,fill_color=RED,fill_opacity=.7).move_to([2.3 if late else -.7,2.8,0]))
SKIN_R=1.0
SKIN_C=[(0,-.35),(-2.8,1.0),(2.8,1.0),(-2.8,-1.7),(2.8,-1.7)]
def skin_patch(all_precursors=False):
    return VGroup(*[VGroup(cell([x,y,0],SKIN_R,VIOLET if i==0 or all_precursors else GREY,.4 if i==0 or all_precursors else .08),label('precursor' if i==0 or all_precursors else 'skin',TEXT,x,y,26)) for i,(x,y) in enumerate(SKIN_C)])
def bristle(x=0):
    return VGroup(Ellipse(width=1.15,height=.4,color=ORANGE,fill_color=ORANGE,fill_opacity=.3).move_to([x,-.8,0]),Polygon([x-.13,-.7,0],[x+.13,-.7,0],[x+.5,1.7,0],color=ORANGE,fill_color=ORANGE,fill_opacity=.65))
TC=(5.85,2.15); TR=.72
def window_strip():
    x0=-6.7; k=.19
    xs=lambda h:x0+k*h
    ticks=VGroup(*[VGroup(Line([xs(h),1.7,0],[xs(h),2.0,0],color=OFF),label(str(h)+(' h' if h==0 else ''),OFF,xs(h)+(.1 if h==0 else 0),1.4,26)) for h in [0,14,20]])
    return VGroup(label('Notch removed 14–20 h',RED,-4.7,2.7,28),Line([xs(0),1.85,0],[xs(20),1.85,0],color=OFF,stroke_width=4),Rectangle(width=xs(20)-xs(14),height=.3,color=RED,fill_color=RED,fill_opacity=.75).move_to([(xs(14)+xs(20))/2,2.2,0]),ticks)
def prompt():
    return VGroup(tree(blank=True),head('Pulse while the lineage divides'),label('What cells should the sense organs contain?',TEXT,0,-3.25,28),window_strip())
def timer(): return VGroup(Circle(radius=TR,color=OFF,stroke_width=6).move_to([*TC,0]),label('5',TEXT,TC[0],TC[1],48))
def reveal(): return VGroup(tree(neurons=True),head('Notch absent during division'),label('No shaft · no socket',TEXT,0,-3.1,34))
def inner_pair():
    t=tree(neurons=True)
    return VGroup(t[0][:2],t[1],t[2])
def two_uses():
    # The gap separates two removal experiments, not two continuous activity bars.
    tl=timeline(); tl[-1].move_to([-2.5,-1.85,0]).set(font_size=26)
    a=pulse(0,14); a.stretch_to_fit_width(a.width-.16).shift(LEFT*.08)
    b=pulse(14,20); b.stretch_to_fit_width(b.width-.16).shift(RIGHT*.08)
    def brk(x0,x1): return VGroup(Line([x0,1.6,0],[x1,1.6,0],color=TEAL,stroke_width=5),Line([x0,1.6,0],[x0,1.42,0],color=TEAL,stroke_width=5),Line([x1,1.6,0],[x1,1.42,0],color=TEAL,stroke_width=5))
    sw1=Square(.26,color=RED,fill_color=RED,fill_opacity=.75).move_to([-6.3,-2.8,0]); sw2=Square(.26,color=TEAL,fill_color=TEAL,fill_opacity=.9).move_to([-6.3,-3.35,0])
    t1=label('Red = warmed, Notch removed.',TEXT,-6.0+2.6,-2.8,26); t2=label('Teal bracket = Notch is needed in both windows.',TEAL,-6.0+3.5,-3.35,26)
    legend=VGroup(sw1,t1,sw2,t2)
    for t_,sw in ((t1,sw1),(t2,sw2)): t_.next_to(sw,RIGHT,buff=.2)
    return VGroup(head('Notch is used twice'),tl,a,label('pick the precursor',TEXT,-1.6,2.2,30),b,label('split its\nprogeny',TEXT,3.4,2.2,30),legend,brk(tx(0)+.08,tx(14)-.08),brk(tx(14)+.08,tx(20)-.08))
def table_base():
    return VGroup(head('One switch at every division'),label('Division',TEXT,-4.4,2.25,30),label('Notch off',OFF,-.4,2.25,30),label('Notch on',TEAL,3.9,2.25,30),Line([-6,1.8,0],[6,1.8,0],color=OFF),*[Line([-6,y,0],[6,y,0],color=GREY,stroke_opacity=.35) for y in [.1,-1.65,-3.35]])
def row(i):
    y=[.95,-.8,-2.55][i]
    a,b,c=[('first division\n(the precursor)','inner precursor','outer precursor'),('outer precursor','hair cell','socket cell'),('inner precursor','neuron','sheath cell')][i]
    g=VGroup(label(a,[TEXT,ORANGE,VIOLET][i],-4.35,y,28),chip(b,OFF,size=28,fill_opacity=.24).move_to([-.4,y,0]),chip(c,TEAL,size=28).move_to([3.9,y,0]))
    g[1][1].set_color(VIOLET if i in [0,2] else ORANGE); g[2][1].set_color(VIOLET if i==2 else ORANGE)
    return g
def takeaway():
    return VGroup(label('Notch is a switch used at every division.',TEXT,0,3.05,34),label('One daughter hears it, and one does not.',TEXT,0,2.35,30),cell([-2.8,-.15,0],1.9,OFF,.2),cell([2.8,-.15,0],1.9,TEAL,.3),chip('does not hear',OFF,size=30).move_to([-2.8,-2.55,0]),chip('hears Notch',TEAL,size=30).move_to([2.8,-2.55,0]))

class S00Title(TitleCard):
    LESSON=LESSON_TITLE
    TITLE='Four Cells and One Switch'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',size=26,color=TEAL),T(self.LESSON,size=28,color=GREY),T(self.TITLE,size=48,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.35)
        self.play(FadeIn(g),run_time=.6); self.finish()
class S01Question(SpokenScene):
    def construct(self):
        self.add(tree(),head('Where in the lineage does Notch act?'))
        self.at('one sister hears'); self.play(FadeIn(blank_badges()),run_time=.4); self.finish()
class S02Notch(SpokenScene):
    def construct(self):
        c=sisters(); r=receptor(); d=delta(); labs=signal_labels()
        self.add(c,chip('Explore: Notch signaling lesson',TEAL,size=28).move_to([0,-3.05,0]))
        self.at('a receptor'); self.play(FadeIn(r),FadeIn(labs[1]),Create(labs[3]),run_time=.4)
        self.at('touching cells'); self.play(Indicate(c,scale_factor=1.01,color=OFF),run_time=.4)
        self.at('a ligand called'); self.play(FadeIn(d,shift=LEFT*.3),run_time=.35)
        self.at('delta'); self.play(FadeIn(labs[0]),Create(labs[2]),run_time=.3)
        self.at('activates it'); self.play(d.animate.shift(RIGHT*.1),Flash([.15,.65,0],color=TEAL,flash_radius=.7),r.animate.set_fill(TEAL,1),run_time=.6); self.finish()
class S03Cut(SpokenScene):
    def construct(self):
        g=signal_stage(); self.add(g)
        nucleus=cell([2.45,-.5,0],1.2,OFF,.1)
        gene=RoundedRectangle(width=1.4,height=.38,corner_radius=.06,color=OFF).move_to([2.45,-.95,0])
        self.add(nucleus,gene,label('nucleus',OFF,4.6,-1.35,28))
        self.at('it is cut'); self.play(Flash([.38,.65,0],color=TEXT,flash_radius=.65),g[1][1].animate.shift(RIGHT*.5).set_fill(TEAL,1),run_time=.4)
        self.at('its inner part'); self.play(g[1][1].animate.move_to([2.45,-.2,0]).scale(1.3),run_time=.55)
        self.at('switch genes on'); self.play(gene.animate.set_color(TEAL).set_fill(TEAL,1),FadeIn(label('genes on',TEAL,2.45,-2.35,30)),run_time=.35); self.finish()
class S04Ts(SpokenScene):
    def construct(self):
        self.add(thermal_stage(),label('1990 · temperature-sensitive Notch',TEXT,0,3.2,30),label('Volker Hartenstein · James Posakony',TEXT,0,2.5,30)); self.finish()
class S05Ts2(SpokenScene):
    def construct(self):
        g=thermal_stage(); self.add(g,head('Temperature-sensitive Notch'))
        cool=label('cool',TEAL,-2.1,2.5,34); tag=chip('working',TEAL,size=34).move_to([1.4,-1.5,0])
        self.at('works at a low'); self.play(FadeIn(cool),FadeIn(tag),run_time=.25)
        self.at('fails at a higher'); self.play(g[0][2].animate.set_color(RED).put_start_and_end_on([-2.1,-1.9,0],[-2.1,1.6,0]),g[1].animate.set_color(OFF),Transform(cool,label('warm',RED,-2.1,2.5,34)),Transform(tag,chip('off',OFF,size=40).move_to([1.4,-1.5,0])),run_time=.35); self.finish()
class S06Pulse(SpokenScene):
    def construct(self):
        self.add(timeline(),head('Notch removed by warming'),label('short pulses · schematic',RED,-.5,2.1,30))
        self.at('chosen window'); self.play(FadeIn(pulse(6,7.5)),run_time=.35)
        self.at('short pulses'); self.play(FadeIn(pulse(10,11.5)),FadeIn(pulse(17,18.5)),run_time=.4); self.finish()
class S07Early(SpokenScene):
    def construct(self):
        self.add(window_stage()); self.at('before the bristle'); self.play(Indicate(timeline()[3],scale_factor=1.03,color=OFF),run_time=.4); self.finish()
class S08EarlyResult(SpokenScene):
    def construct(self):
        g=skin_patch(); self.add(g,mini_window())
        self.at('extra precursors'); self.play(Transform(g,skin_patch(True)),run_time=.6); self.finish()
class S08bLateral(SpokenScene):
    def construct(self):
        g=skin_patch(); tag=chip('normal',TEAL,size=28).move_to([-4.8,2.7,0]); self.add(g,tag,head('The usual explanation'))
        c=np.array([0,-.35,0]); ends=[]
        for (x,y) in SKIN_C[1:]:
            d=np.array([x,y+.35,0.]); u=d/np.linalg.norm(d); ends.append((c+u*1.2,c+u*2.0))
        arrows=VGroup(*[arr(a,b) for a,b in ends])
        crosses=VGroup(*[VGroup(Line((a+b)/2+np.array([-.13,-.13,0]),(a+b)/2+np.array([.13,.13,0]),color=RED,stroke_width=6),Line((a+b)/2+np.array([-.13,.13,0]),(a+b)/2+np.array([.13,-.13,0]),color=RED,stroke_width=6)) for a,b in ends])
        self.at('signals to its'); self.play(*[GrowArrow(a) for a in arrows],run_time=.4)
        self.at('through notch'); mid=(ends[1][0]+ends[1][1])/2; n=label('Notch',TEAL,mid[0]-.5,mid[1]+.58,28); self.play(FadeIn(n),run_time=.3)
        self.at('stay skin cells'); self.play(Indicate(g[2],color=TEAL),run_time=.4)
        self.at('without notch'); self.play(arrows.animate.set_color(OFF).set_opacity(.22),n.animate.set_color(OFF),FadeIn(crosses),Transform(tag,chip('no Notch',OFF,size=28).move_to([-4.8,2.7,0])),run_time=.3)
        self.at('become precursors'); self.play(Transform(g,skin_patch(True)),run_time=.5); self.finish()
class S08cBristles(SpokenScene):
    def construct(self):
        xs=[-4.8,-2.4,0,2.4,4.8]
        cells=VGroup(*[node('precursor',x,-1.6,VIOLET,r=.55,size=26) for x in xs]); self.add(cells,head('Each extra precursor makes a normal bristle'))
        self.at('formed a normal'); self.play(*[GrowFromEdge(bristle(x).shift(DOWN*.25),DOWN) for x in xs],run_time=.6); self.finish()
class S09Late(SpokenScene):
    def construct(self):
        self.add(window_stage(True)); self.at('around the time'); self.play(Indicate(timeline()[3],scale_factor=1.03,color=OFF),run_time=.4); self.finish()
class S10Predict(SpokenScene):
    def construct(self):
        self.add(prompt()); self.at('what cells should'); self.play(FadeIn(timer()),run_time=.3); self.finish()
class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prompt())
        ring=Circle(radius=TR,color=OFF,stroke_width=6).move_to([*TC,0]); self.add(ring)
        for n in range(5,0,-1):
            digit=label(str(n),TEXT,TC[0],TC[1],48); self.add(digit)
            arc=Arc(radius=TR,start_angle=PI/2,angle=-TAU/5,color=TEAL,stroke_width=12).move_arc_center_to([*TC,0]).rotate(-(5-n)*TAU/5,about_point=[*TC,0])
            self.play(Create(arc),run_time=1,rate_func=linear); self.remove(digit)
class S12Reveal(SpokenScene):
    def construct(self):
        t=compact_tree(); self.add(t,head('Notch absent during division'))
        b=bristle().scale(1.4).move_to([4.9,.15,0])
        shaft=label('shaft',ORANGE,3.55,1.3,30); socket=label('socket',ORANGE,3.45,-1.5,30)
        l1=Line(shaft.get_right()+RIGHT*.05,b[1].get_center()+LEFT*.1,color=ORANGE,stroke_width=3)
        l2=Line(socket.get_right()+RIGHT*.05,b[0].get_left()+RIGHT*.15,color=ORANGE,stroke_width=3)
        self.add(b,shaft,socket,l1,l2)
        gone=VGroup(DashedVMobject(Circle(radius=1.95,color=OFF,stroke_width=4).move_to([4.9,.15,0]),num_dashes=28),Line([4.2,-.55,0],[5.6,.85,0],color=RED,stroke_width=8),Line([4.2,.85,0],[5.6,-.55,0],color=RED,stroke_width=8))
        self.at('only of neurons'); self.play(Transform(t,compact_tree(True)),run_time=.5)
        self.at('no shaft'); self.play(FadeOut(b[1]),FadeOut(shaft),FadeOut(l1),run_time=.35)
        self.at('no socket'); self.play(FadeOut(b[0]),FadeOut(socket),FadeOut(l2),FadeIn(gone),FadeIn(label('No shaft · no socket',TEXT,0,-3.2,42)),run_time=.35); self.finish()
class S13Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(reveal()); self.wait(2)
class S14Reading(SpokenScene):
    def construct(self):
        t=tree(blank=True); self.add(t,head('No Notch · walk down the map'))
        self.at('first division gives'); self.play(Indicate(t[1][0],color=OFF),run_time=.35)
        self.at('two inner precursors'); target=tree(neurons=True); self.play(Transform(t[2],target[2]),Transform(t[0][1],target[0][1]),run_time=.5); self.finish()
class S14bWalk(SpokenScene):
    def construct(self):
        t=tree(blank=True); target=tree(neurons=True); t[2].become(target[2]); t[0][1].become(target[0][1]); self.add(t,head('No Notch · two inner precursors'))
        self.at('gives two neurons'); self.play(Transform(t[3],target[3]),Transform(t[0],target[0]),run_time=.55)
        self.at('a sheath cell'); self.play(FadeIn(label('4 neurons',VIOLET,0,-3.1,34)),run_time=.3); self.finish()
class S15Meaning(SpokenScene):
    def construct(self):
        R=2.2; cx=3.55; cy=-.1
        mini=VGroup(Line([0,1.0,0],[-.7,-.3,0],color=VIOLET),Line([0,1.0,0],[.7,-.3,0],color=ORANGE),cell([0,1.0,0],.22),cell([-.7,-.3,0],.26,VIOLET,.5),cell([.7,-.3,0],.26,ORANGE,.5),
                    Line([-.96,-.3,0],[-cx+np.sqrt(R*R-.04),-.3,0],color=VIOLET,stroke_width=3),Line([.96,-.3,0],[cx-np.sqrt(R*R-.04),-.3,0],color=ORANGE,stroke_width=3))
        gl=cell([-cx,cy,0],R,OFF,.06); gr=cell([cx,cy,0],R,OFF,.06)
        self.add(head('Two branches · different Notch requirements'),mini,gl,gr)
        ln=label('inner branch → neuron',VIOLET,-cx,2.65,30); lr=label('outer branch → hair + socket',ORANGE,cx,2.65,30)
        nl=label('neuron',VIOLET,-cx,cy,44)
        br=bristle().scale(1.35).move_to([cx,cy,0]); shaft=label('shaft',ORANGE,cx+1.25,.95,28); socket=label('socket',ORANGE,cx+1.15,-1.0,28)
        self.at('the neuron'); self.play(gl.animate.set_color(VIOLET).set_fill(VIOLET,.35),FadeIn(ln),FadeIn(nl),run_time=.35)
        self.at('notch off fate'); self.play(FadeIn(chip('Notch off',OFF,size=32).move_to([-cx,-3.1,0])),run_time=.3)
        self.at('the outer branch'); self.play(gr.animate.set_color(ORANGE).set_fill(ORANGE,.25),FadeIn(lr),run_time=.35)
        self.at('shaft and socket'); self.play(GrowFromEdge(br,DOWN),FadeIn(shaft),FadeIn(socket),run_time=.4)
        self.at('needs notch'); self.play(FadeIn(chip('needs Notch',TEAL,size=32).move_to([cx,-3.1,0])),run_time=.3); self.finish()
class S16Twice(SpokenScene):
    def construct(self):
        g=two_uses(); self.add(g[0],g[1],g[6])
        self.at('pick the precursor',lead=.5); self.play(FadeIn(g[2]),FadeIn(g[3]),FadeIn(g[7]),run_time=.3)
        self.at('split its progeny',lead=.5); self.play(FadeIn(g[4]),FadeIn(g[5]),FadeIn(g[8]),run_time=.3); self.finish()
class S17Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(two_uses()); self.wait(2)
class S18Guo(SpokenScene):
    def construct(self):
        CX=-5.3
        box=RoundedRectangle(width=3.0,height=3.6,corner_radius=.2,stroke_color=OFF,stroke_width=2.5,fill_color=OFF,fill_opacity=.08).move_to([CX,.1,0])
        yr=label('1996',TEAL,CX,1.45,44)
        n1=label('Ming Guo',TEXT,CX,.45,30); n2=label('Lily Jan',TEXT,CX,-.3,30); n3=label('Yuh Nung Jan',TEXT,CX,-1.05,30)
        mL,mR=-.47,3.13; RX=(mL+mR)/2
        root=cell([RX,2.0,0],.43)
        mids=VGroup(cell([mL,.3,0],.43,VIOLET),cell([mR,.3,0],.43,ORANGE))
        lx=[mL-1.0,mL+1.0,mR-1.0,mR+1.0]
        leaves=VGroup(*[node(n,x,-2.0,VIOLET if i<2 else ORANGE,r=.37,size=26) for i,(n,x) in enumerate(zip(['neuron','sheath','hair','socket'],lx))])
        edges=VGroup(*[Line([RX,1.57,0],[x,.73,0],color=c) for x,c in [(mL,VIOLET),(mR,ORANGE)]],*[Line([mL if i<2 else mR,-.13,0],[x,-1.63,0],color=VIOLET if i<2 else ORANGE) for i,x in enumerate(lx)])
        sL=-2.45; sR=mR+.43+.5+1.05; sT=RX+.43+.5+1.05
        self.add(box,yr,root,mids,leaves,edges,head('Notch at every division'),label('precursor',TEXT,RX-.43-.3-.83,2.0,28),label('inner',VIOLET,mL-.95,-.35,28),label('outer',ORANGE,mR+.95,-.35,28))
        def switch(x,y):
            return VGroup(Line([x-.8,y,0],[x+.8,y,0],color=OFF,stroke_width=8),Dot([x-.8,y,0],radius=.22,color=OFF),Dot([x+.8,y,0],radius=.22,color=TEAL),label('off',OFF,x-.8,y+.55,30),label('on',TEAL,x+.8,y+.55,30))
        self.at('ming guo'); self.play(FadeIn(n1),run_time=.3)
        self.at('lily jan'); self.play(FadeIn(n2),run_time=.3)
        self.at('nung jan'); self.play(FadeIn(n3),run_time=.3)
        self.at('went further'); self.play(Indicate(VGroup(root,mids,edges),scale_factor=1.02,color=TEAL),run_time=.5)
        self.at('two way switch'); self.play(FadeIn(switch(sT,2.0)),run_time=.3)
        self.at('at each division'); self.play(FadeIn(switch(sL,.3)),FadeIn(switch(sR,.3)),run_time=.4); self.finish()
class S19Fill1(SpokenScene):
    def construct(self):
        r=row(0); a=cell([-.4,.95,0],.5,OFF,.2); b=cell([3.9,.95,0],.5,TEAL,.2); self.add(table_base(),r[0],a,b)
        self.at('the inner precursor'); self.play(ReplacementTransform(a,r[1]),run_time=.3)
        self.at('the outer precursor'); self.play(ReplacementTransform(b,r[2]),run_time=.3); self.finish()
class S20Fill2(SpokenScene):
    def construct(self):
        r=row(1); self.add(table_base(),row(0),r[0])
        self.at('the hair cell'); self.play(FadeIn(r[1]),run_time=.3)
        self.at('the socket cell'); self.play(FadeIn(r[2]),run_time=.3); self.finish()
class S21Fill3(SpokenScene):
    def construct(self):
        r=row(2); self.add(table_base(),row(0),row(1),r[0])
        self.at('the neuron is'); self.play(FadeIn(r[1]),run_time=.3)
        self.at('the sheath cell'); self.play(FadeIn(r[2]),run_time=.3); self.finish()
class S22Side(SpokenScene):
    def construct(self):
        self.add(sisters()); tag=chip('hears Notch',TEAL,size=28).move_to([2.1,-2.55,0])
        self.at('one daughter hears'); self.play(FadeIn(tag),run_time=.3)
        self.at('side by side'); self.play(Indicate(sisters(),scale_factor=1.01,color=OFF),run_time=.5)
        self.at('either could signal')
        # Both arrows are centred on the shared membrane at x=0 and stacked as a pair.
        a=VGroup(*[Arrow(p,q,buff=0,color=TEAL,stroke_width=11,tip_length=.38,max_tip_length_to_length_ratio=.35) for p,q in [([-1.0,.7,0],[1.0,.7,0]),([1.0,-.2,0],[-1.0,-.2,0])]])
        self.play(FadeOut(tag),*[GrowArrow(x) for x in a],run_time=.4)
        self.at('what stops one'); self.play(FadeIn(label('?',TEXT,-2.1,.25,220)),FadeIn(label('What stops one from hearing?',TEXT,0,-3.15,34)),run_time=.3); self.finish()
class S23Takeaway(SpokenScene):
    def construct(self):
        g=takeaway(); self.add(g[0],g[2],g[3])
        self.at('one daughter hears'); self.play(FadeIn(g[1]),FadeIn(g[5]),run_time=.3)
        self.at('one does not'); self.play(FadeIn(g[4]),run_time=.3); self.finish()
class S24End(EndCard):
    LINE='Notch is a switch used at every division.'
    def construct(self):
        self.add(takeaway(),label('biochemistrypedia.com',TEAL,0,-3.45,28)); self.finish()
