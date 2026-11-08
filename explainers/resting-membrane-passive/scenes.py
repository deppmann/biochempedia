"""The Standoff, review redraw.
COLOR MAP: blue #58C4DD K+, E_K, g_K; orange #F29E4C Na+, E_Na,
g_Na; yellow Vm; green zero net current; purple pump; grey context.
The script's historical 'purple K' notes are superseded by this shared series map.
All voltage distances, stretches, meter positions and current lengths use the model.
"""
import re
import numpy as np
from bp_style import *
ORANGE = '#F29E4C'
KC, NAC, VC, NETC = BLUE, ORANGE, YELLOW, GREEN
MUTED = '#BBC2CE'
EK, ENA, VM = -95., 60.6, -71.2
GK, GNA = 8.47, 1.53
AY = .35

def x(v):
    return -5.6 + (v + 105) / 175 * 11.2

def notation(s, size=34, color=TEXT):
    s = re.sub(r'([EIg])_(ion|Na|K)', r'\1<span rise="-5500" size="70%">\2</span>', s)
    s = s.replace('Vm', 'V<span rise="-5500" size="70%">m</span>')
    return MarkupText(s, font=FONT, font_size=size, color=color)

def label(s,y,size=34,color=TEXT):
    return notation(s,size,color).move_to([0,y,0])

def marker(v=VM):
    return VGroup(Line([x(v),AY-.25,0],[x(v),AY+.3,0],color=VC,stroke_width=5),
                  Dot([x(v),AY,0],radius=.13,color=VC))

def emark(v,k):
    col=KC if k else NAC
    t=notation('E_K = −95 mV' if k else 'E_Na = +60.6 mV',34,col)
    t.move_to([-4.45 if k else 4.5,1.95,0])
    return VGroup(Line([x(v),AY-.2,0],[x(v),AY+.25,0],color=col,stroke_width=5),
                  Line([x(v),AY+.3,0],[x(v),1.5,0],color=col,stroke_width=2),t)

def scale(k=True,na=True,vm=True):
    a=VGroup(RoundedRectangle(width=12.35,height=4.7,corner_radius=.16,
        stroke_color=GREY,stroke_width=1.5,fill_color=GREY,fill_opacity=.055).move_to([0,0,0]),
        Line([-5.6,AY,0],[5.6,AY,0],color=MUTED,stroke_width=3),
        label('voltage / mV',2.95,30,MUTED))
    for v in [-100,-50,0,50]:
        a.add(Line([x(v),AY-.1,0],[x(v),AY+.1,0],color=MUTED),
              notation(f'{v:+d}' if v>0 else str(v),30,MUTED).move_to([x(v),AY-.58,0]))
    if k: a.add(emark(EK,True))
    if na: a.add(emark(ENA,False))
    if vm:
        a.add(marker(),notation('Vm = −71.2 mV',34,VC).move_to([-2.45,1.45,0]))
    return a

def gap(k=True,y=-.9):
    lo,hi=(EK,VM) if k else (VM,ENA)
    col=KC if k else NAC
    a=VGroup(Line([x(lo),y,0],[x(hi),y,0],color=col,stroke_width=3))
    for v in [lo,hi]: a.add(Line([x(v),y-.13,0],[x(v),y+.13,0],color=col,stroke_width=3))
    text='Vm − E_K = +23.8 mV' if k else 'Vm − E_Na = −131.8 mV'
    t=notation(text,34,col).move_to([-2.65 if k else 1.15,y-.4,0])
    a.add(t)
    return a

def rope(k=True,thick=True,v=VM):
    start=EK if k else ENA
    # Offset from the axis so ticks remain legible; arrowheads end at the marker.
    return Arrow([x(start),AY+.37,0],[x(v),AY+.37,0],buff=0,
                 color=KC if k else NAC,stroke_width=(17 if k else 3.1) if thick else 4,
                 tip_length=.16,max_stroke_width_to_length_ratio=100)

def ropes(thick=True): return VGroup(rope(True,thick),rope(False,thick))

def cell():
    # A continuous soma outline opens into a long axon; branched dendrites
    # distinguish the neuron from an ellipse with isolated stubs.
    outline=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.07)
    outline.set_points_smoothly([
        [-1.15,.6,0],[-1.7,1.25,0],[-3,1.57,0],[-4.55,1.12,0],
        [-5.25,0,0],[-4.55,-1.12,0],[-3,-1.57,0],[-1.7,-1.15,0],
        [-1.1,-.55,0]])
    outline.add_points_as_corners([[-.65,-.38,0],[.45,-.38,0],[.45,-.12,0],
                                   [-.65,-.12,0],[-1.15,.6,0]])
    branches=VGroup()
    for points in [
        [[-4.65,.95,0],[-5.4,1.75,0],[-5.9,1.95,0]],
        [[-5.4,1.75,0],[-5.3,2.35,0]],
        [[-4.65,-.95,0],[-5.45,-1.7,0],[-5.95,-1.85,0]],
        [[-5.45,-1.7,0],[-5.3,-2.2,0]]]:
        branches.add(VMobject(color=GREY,stroke_width=4).set_points_as_corners(points))
    return VGroup(outline,branches)

def meter(glow=False):
    c=np.array([3.4,-.1,0]); radius=1.32
    def p(v,r=radius):
        angle=PI-(v+100)/150*PI
        return c+np.array([r*np.cos(angle),r*np.sin(angle),0])
    g=VGroup(RoundedRectangle(width=4.95,height=3.65,corner_radius=.2,color=GREY).move_to([3.4,.45,0]),
        Arc(radius=radius,start_angle=0,angle=PI,arc_center=c,color=MUTED))
    for v in [-100,-50,0,50]:
        g.add(Line(p(v,1.2),p(v,1.43),color=MUTED),notation(str(v) if v<=0 else '+50',30,MUTED).move_to(p(v,1.82)))
    needle=Line(c,p(VM,1.16),color=VC,stroke_width=6)
    if glow: g.add(Line(c,p(VM,1.16),color=VC,stroke_width=20,stroke_opacity=.22))
    g.add(needle,Dot(c,radius=.08,color=VC),notation('−71 mV',40,VC).move_to([3.4,-.9,0]))
    return g

def stream(outward=True):
    dots=VGroup(*[Dot(radius=.065,color=KC if outward else NAC) for _ in range(8)])
    dots.phase=0.
    def update(g,dt):
        g.phase+=dt*.65
        for i,d in enumerate(g):
            q=(g.phase+i/8)%1
            # Vertical paths cross the soma's top / bottom membrane, in lanes.
            lane=-3.65+(i%4)*.28
            d.move_to([lane,(.75+q*1.8) if outward else (-2.55+q*1.8),0])
    dots.add_updater(update); update(dots,0)
    return dots

def flow_arrow(k=True):
    return Arrow([-3, .85 if k else -2.55,0],[-3,2.55 if k else -.85,0],buff=0,
        color=KC if k else NAC,stroke_width=9,tip_length=.24)

def flow_labels(exact=False):
    return VGroup(notation('K+  ≈ +202 pA' if exact else 'K+  ≈ +200 pA',32,KC).move_to([-.7,2.35,0]),
                  notation('Na+  ≈ −202 pA' if exact else 'Na+  ≈ −200 pA',32,NAC).move_to([-.7,-2.35,0]))

def cell_view(flows=True,glow=False,exact=False):
    g=VGroup(cell(),meter(glow),stream(),stream(False))
    if flows: g.add(flow_arrow(),flow_arrow(False),flow_labels(exact))
    return g

def question():
    return VGroup(scale(),label('Which way does K+ current flow?',-1.35,38),
        notation('Pause and predict',30,MUTED).move_to([-1,-2.95,0]))

class S00Title(TitleCard):
    LESSON='The Resting Membrane and Passive Signals'
    TITLE='The Standoff'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',30,TEAL),T(self.LESSON,32,MUTED),
            T(self.TITLE,64,font=TITLE_FONT),Line(LEFT*1.5,RIGHT*1.5,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.5)
        self.play(FadeIn(g),run_time=.5); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        self.add(cell(),label('In a resting neuron, ions keep moving',3.1,36),
                 VGroup(T('Why does the voltage',36),T('hold still?',36)).arrange(DOWN,buff=.2).move_to([3.4,.1,0]))
        self.at('potassium leaks out')
        self.add(stream()); self.play(GrowArrow(flow_arrow()),FadeIn(notation('K+ out',34,KC).move_to([-.8,2.3,0])),run_time=.4)
        self.at('sodium leaks in')
        self.add(stream(False)); self.play(GrowArrow(flow_arrow(False)),FadeIn(notation('Na+ in',34,NAC).move_to([-.8,-2.3,0])),run_time=.4)
        self.at('So why does')
        self.play(Indicate(self.mobjects[2],scale_factor=1.03,color=TEXT),run_time=.35)
        self.finish()

class S02Cell(SpokenScene):
    def construct(self):
        self.add(cell(),stream(),stream(False),label('Made-up neuron • illustrative numbers',3.2,32,MUTED))
        self.at('resting at about'); self.play(FadeIn(meter()),run_time=.5); self.finish()

class S03Flows(SpokenScene):
    def construct(self):
        self.add(cell_view(False)); labels=flow_labels()
        self.at('Potassium current leaves'); self.play(GrowArrow(flow_arrow()),FadeIn(labels[0]),run_time=.4)
        self.at('Sodium current comes in'); self.play(GrowArrow(flow_arrow(False)),FadeIn(labels[1]),run_time=.4)
        self.finish()

class S04NotEq(SpokenScene):
    def construct(self):
        self.add(cell_view(glow=True),label('Neither ion is at equilibrium',-3.25,36))
        self.at('Yet the voltmeter needle')
        self.play(FadeIn(SurroundingRectangle(notation('−71 mV',40).move_to([3.4,-.9,0]),color=VC,buff=.15)),run_time=.35)
        self.finish()

class S05EqTerm(SpokenScene):
    def construct(self):
        self.add(cell().scale(.27).move_to([-5,2.4,0]),label('equilibrium potential',.65,52),label('E_ion',-.8,58,VC))
        self.at('Each ion has'); self.play(Indicate(self.mobjects[-1],color=VC),run_time=.8); self.finish()

class S06EqDef(SpokenScene):
    def construct(self):
        membrane=VGroup(*[Line([a,-2,0],[a,2,0],color=GREY,stroke_width=9) for a in [-.12,.12]])
        arrows=VGroup(Arrow([-.2,0,0],[-3.6,0,0],buff=0,color=TEXT,stroke_width=8),
                       Arrow([.2,0,0],[3.6,0,0],buff=0,color=TEXT,stroke_width=8))
        self.add(membrane,arrows,label('At an ion’s equilibrium potential',3.1,38),
                 T('outside',30,MUTED).move_to([-4.6,-2,0]),T('inside',30,MUTED).move_to([4.6,-2,0]))
        self.at('electrical force on'); self.play(FadeIn(notation('electrical force',34).move_to([-3,1.1,0])),run_time=.4)
        self.at('balances its concentration gradient'); self.play(FadeIn(notation('concentration gradient',34).move_to([3,1.1,0])),run_time=.4)
        self.at('There the ion'); self.play(FadeIn(label('equal forces → no net push',-3.15,38,TEXT)),run_time=.4); self.finish()

class S07ScaleK(SpokenScene):
    def construct(self):
        self.add(scale(False,False,False))
        self.at("Potassium's equilibrium potential"); self.play(FadeIn(emark(EK,True)),run_time=.5)
        self.add(label('An ion’s own balance voltage',-1.65,38,KC)); self.finish()

class S08ScaleNa(SpokenScene):
    def construct(self):
        self.add(scale(True,False,False),label('Each ion has its own equilibrium potential',-1.65,36))
        self.at('Sodium sits near'); self.play(FadeIn(emark(ENA,False)),run_time=.5); self.finish()

class S09Marker(SpokenScene):
    def construct(self):
        self.add(scale(vm=False),label('Vm = inside − outside',-1.6,44,VC))
        self.at('A marker on the scale'); self.play(FadeIn(marker()),run_time=.4)
        self.at('membrane potential'); self.play(FadeIn(notation('Vm = −71.2 mV',34,VC).move_to([-2.45,1.45,0])),run_time=.4); self.finish()

class S10Driving(SpokenScene):
    def construct(self):
        self.add(scale())
        self.at('The gap between'); self.play(Create(gap(True,-.75)),run_time=.5)
        self.at('the driving force'); self.play(Create(gap(False,-1.6)),run_time=.5)
        sign=label('+ outward     − inward',-3.45,34)
        self.at('Its sign gives'); self.play(FadeIn(sign),run_time=.35)
        self.at('Its size gives'); self.play(FadeOut(sign),run_time=.15)
        self.play(FadeIn(label('distance = strength of the driving force',-3.45,32,MUTED)),run_time=.3); self.finish()

class S11Ropes(SpokenScene):
    def construct(self):
        self.add(scale())
        self.at('Tie a rope'); self.play(Create(ropes(False)),run_time=.8)
        self.at("The rope's pull"); self.play(FadeIn(label('rope pull = ion current',-1.65,44)),run_time=.4); self.finish()

class S12Thick(SpokenScene):
    def construct(self):
        r=ropes(False); self.add(scale(),r,label('More open channels → thicker rope',-1.7,38))
        self.at('More open channels'); self.play(Transform(r[0],rope()),run_time=1)
        self.at('That is conductance'); self.play(FadeIn(label('thickness = conductance, g (nS)',-2.75,38)),run_time=.4); self.finish()

class S13Stretch(SpokenScene):
    def construct(self):
        self.add(scale(),label('longer stretch = bigger driving force',-2.7,38))
        v=ValueTracker(VM)
        ghost=always_redraw(lambda: marker(v.get_value()).set_opacity(.65))
        r=always_redraw(lambda: VGroup(Line([x(EK),AY+.37,0],[x(v.get_value()),AY+.37,0],color=KC,stroke_width=27,stroke_opacity=.12+.28*(v.get_value()-VM)/(-20-VM)),rope(True,True,v.get_value())))
        read=always_redraw(lambda: label(f'stretch = {v.get_value()-EK:.1f} mV',-1.55,40,KC))
        self.add(ghost,r,read)
        self.at('a rope pulls harder'); self.play(v.animate.set_value(-20),run_time=1.05)
        self.wait(.65); self.play(v.animate.set_value(VM),run_time=.65)
        self.remove(ghost,r,read); self.add(ropes(),label('stretch = 23.8 mV',-1.55,40,KC)); self.finish()

class S14Equation(SpokenScene):
    def construct(self):
        eq=VGroup(notation('I_ion =',50),notation('g_ion',50),notation('×',50),notation('(Vm − E_ion)',50)).arrange(RIGHT,buff=.2).move_to([0,.65,0])
        # The equation and its annotations stand alone on the scene background.
        self.add(eq)
        self.at('So current equals'); self.play(Indicate(eq,scale_factor=1.02,color=TEXT),run_time=.35)
        b=Brace(eq[3],DOWN,color=TEXT); bg=Brace(eq[1],DOWN,color=TEXT)
        self.at('conductance'); self.play(FadeIn(bg),FadeIn(notation('g: conductance',32).next_to(bg,DOWN,buff=.25).shift(LEFT*.6)),run_time=.3)
        self.at('driving force'); self.play(FadeIn(b),FadeIn(notation('driving force',34).next_to(b,DOWN,buff=.25)),run_time=.3); self.finish()

class S15Sign(SpokenScene):
    def construct(self):
        self.add(cell(),label('Current sign: positive charge',3.2,40))
        a=flow_arrow().set_color(TEXT); b=flow_arrow(False).set_color(TEXT)
        self.at('outward current'); self.play(GrowArrow(a),FadeIn(T('outward = positive (+)',36).move_to([2.8,1.5,0])),run_time=.4)
        self.at('positive charge leaving'); dot=Dot([-3,.85,0],color=WHITE,radius=.12); self.add(dot); self.play(dot.animate.move_to([-3,2.55,0]),run_time=.6)
        self.at('counts as positive'); self.play(GrowArrow(b),FadeIn(T('inward = negative (−)',36).move_to([2.8,-1.5,0])),run_time=.4); self.finish()

class S16Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0])
        self.at('Our cell rests above'); self.play(Indicate(q[0][-2],color=VC),run_time=1)
        self.at('which way does'); self.play(FadeIn(q[1:]),run_time=.4); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question())
        t=ValueTracker(5)
        ring=always_redraw(lambda: Arc(radius=.48,start_angle=PI/2,angle=max(.001,TAU*t.get_value()/5),color=VC,stroke_width=6).move_arc_center_to([4.65,-3,0]))
        number=always_redraw(lambda: T(str(max(1,int(np.ceil(t.get_value())))),30,VC).move_to([4.65,-3,0]))
        self.add(Circle(radius=.48,color=GREY).move_to([4.65,-3,0]),ring,number)
        self.play(t.animate.set_value(0),run_time=5,rate_func=linear)

class S18Reveal(SpokenScene):
    def construct(self):
        axis=scale(); axis[-1].move_to([-.3,1.45,0])
        axis[11][1].set_opacity(0)  # Clear the K label leader behind the pull caption.
        self.add(axis,gap(True,-.85),label('K+: outward current (+)',-2.7,44,KC))
        self.at('Outward'); self.play(GrowArrow(Arrow([x(VM),AY+.4,0],[x(EK),AY+.4,0],buff=0,color=KC,stroke_width=8)),
            FadeIn(notation('pull toward E_K',28,KC).move_to([-4.25,1.1,0])),run_time=.4)
        self.at('The driving force'); self.play(FadeIn(label('−71.2 − (−95) = +23.8 mV',-3.4,36,KC)),run_time=.4); self.finish()

class S19Sodium(SpokenScene):
    def construct(self):
        self.add(scale(),gap(True,-.75))
        self.at('Sodium is the opposite'); self.play(Create(gap(False,-1.6)),run_time=.5)
        self.at('The marker sits far below'); self.play(FadeIn(label('−71.2 − 60.6 = −131.8 mV',-3.4,34,NAC)),run_time=.4)
        self.at('so sodium is pushed in'); self.play(GrowArrow(Arrow([x(VM),AY+.4,0],[x(ENA),AY+.4,0],buff=0,color=NAC,stroke_width=8)),FadeIn(notation('pull toward E_Na',30,NAC).move_to([2.25,1.25,0])),
            FadeIn(notation('inward (−)',38,NAC).move_to([2.25,.75,0]).set_background_stroke(color=BG,width=7,opacity=1)),run_time=.4); self.finish()

class S20Tradeoff(SpokenScene):
    def construct(self):
        self.add(scale()); r=ropes().shift(DOWN*1.5)
        self.at('Potassium has much more conductance'); self.play(Create(r[0]),FadeIn(notation('g_K = 8.47 nS',34,KC).move_to([-4.2,-1.35,0])),run_time=.4)
        self.at('but a short stretch'); self.play(FadeIn(notation('stretch: 23.8 mV',34,KC).move_to([-4.2,-2.0,0])),run_time=.35)
        self.at('Sodium has less conductance'); self.play(Create(r[1]),FadeIn(notation('g_Na = 1.53 nS',34,NAC).move_to([1.75,-1.35,0])),run_time=.4)
        self.at('but a long stretch'); self.play(FadeIn(notation('stretch: 131.8 mV',34,NAC).move_to([1.75,-2.0,0])),run_time=.35)
        self.finish()

class S21Cancel(SpokenScene):
    def construct(self):
        # Full-width scale retained above the cell; labels remain at native size.
        inset=VGroup(Line([-5.6,1.95,0],[5.6,1.95,0],color=MUTED))
        for v in [-100,-50,0,50]:
            inset.add(Line([x(v),1.85,0],[x(v),2.05,0],color=MUTED),
                      notation(str(v) if v<=0 else '+50',30,MUTED).move_to([x(v),1.48,0]))
        for v,k in [(EK,True),(ENA,False)]:
            col=KC if k else NAC
            inset.add(Line([x(v),1.8,0],[x(v),2.8,0],color=col,stroke_width=3),
                      notation('E_K = −95 mV' if k else 'E_Na = +60.6 mV',34,col).move_to([-4.45 if k else 4.5,3.25,0]))
        inset.add(Dot([x(VM),1.95,0],color=VC),notation('Vm = −71.2 mV',34,VC).move_to([-2.45,2.65,0]))
        self.add(inset,cell().scale(.8).move_to([-4.3,-.9,0]))
        ik=GK*(VM-EK); ina=GNA*(VM-ENA)
        k=Arrow([-4.3,-.2,0],[-4.3,-.2+ik*.0065,0],buff=0,color=KC,stroke_width=9)
        n=Arrow([-4.3,-2.7,0],[-4.3,-2.7+abs(ina)*.0065,0],buff=0,color=NAC,stroke_width=9)
        self.at('The two currents'); self.play(GrowArrow(k),FadeIn(T('outward 202 pA',32,KC).move_to([2,.45,0])),run_time=.35)
        self.at('equal and opposite'); self.play(GrowArrow(n),FadeIn(T('inward 202 pA',32,NAC).move_to([2,-1.3,0])),run_time=.35)
        self.at('about 200 picoamperes'); self.play(FadeIn(notation('8.47 nS × 23.8 mV ≈ +202 pA',32,KC).move_to([2,-.3,0])),FadeIn(notation('1.53 nS × (−131.8 mV) ≈ −202 pA',32,NAC).move_to([2,-2.05,0])),run_time=.4)
        self.add(label('nS × mV = pA',-3.25,34)); self.finish()

class S22Meaning(SpokenScene):
    def construct(self):
        v=cell_view(glow=True)
        self.add(v,label('Rest: zero NET current',3.2,42,NETC),label('pump’s small direct current set aside',-3.25,30,MUTED))
        self.at('not zero current for each ion'); self.play(Indicate(v[-1],scale_factor=1.04,color=TEXT),run_time=.7); self.finish()

class S23Puzzle1(SpokenScene):
    def construct(self):
        axis=scale(); self.add(axis); prompt=label('Two puzzles remain',-1.9,42)
        self.at('Two puzzles remain'); self.play(FadeIn(prompt),run_time=.3)
        self.at('Why does the cell rest here'); self.play(FadeOut(prompt),run_time=.2)
        self.play(FadeIn(label('1. Where does it rest, and why there?',-1.65,36)),Indicate(axis[-2],color=VC,scale_factor=1.5),run_time=1.2); self.finish()

class S24Puzzle2(SpokenScene):
    def construct(self):
        self.add(scale(),label('1. Where does it rest, and why there?',-1.3,34))
        self.at('And what if we push'); self.play(FadeIn(label('2. What does a small nudge do?',-1.95,36)),run_time=.3)
        self.at('How big a change'); self.play(FadeIn(T('How big?',34).move_to([-3.8,-3.15,0])),run_time=.2)
        self.at('how fast'); self.play(FadeIn(T('How fast?',34).move_to([0,-3.15,0])),run_time=.2)
        self.at('and how far'); self.play(FadeIn(T('How far?',34).move_to([3.8,-3.15,0])),run_time=.2); self.wait(3.2); self.finish()

class S25Rule(SpokenScene):
    def construct(self):
        self.add(scale(),ropes(),label('Each ion’s open channels pull Vm',-1.95,38),label('toward that ion’s own E',-3,38))
        # Current = conductance × stretch; near-equal pulls are correct at rest.
        self.at("Each ion's open channels")
        arrows=VGroup()
        for current,col in [(GK*(VM-EK),KC),(GNA*(VM-ENA),NAC)]:
            start=[x(VM),-.85,0]; end=[x(VM)-current*.007,-.85,0]
            a=Arrow(start,end,buff=0,color=col,stroke_width=7).set_z_index(3)
            halo=Arrow(start,end,buff=0,color=BG,stroke_width=16).set_z_index(2)
            arrows.add(halo,a)
        self.play(FadeIn(arrows),run_time=.5)
        self.at('pull the voltage toward'); self.play(Indicate(arrows,scale_factor=1.07),run_time=1)
        self.add(label('pull = conductance × stretch',-1.4,30,MUTED)); self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        self.add(cell_view(glow=True,exact=True),label('Currents cancel: +202 pA and −202 pA',3.2,36,NETC),label('The needle stays still; ions keep moving',-3.25,34))
        self.at('Rest means the currents cancel'); self.play(Indicate(self.mobjects[-2],scale_factor=1.04),run_time=.6); self.finish()

class S27End(EndCard):
    LINE='Rest means the currents cancel, not that they stop.'
    def construct(self):
        self.add(VGroup(T('Rest means the currents cancel,',44,font=TITLE_FONT),T('not that they stop.',44,font=TITLE_FONT),T('biochemistrypedia.com',30,TEAL)).arrange(DOWN,buff=.45))
        self.finish()
