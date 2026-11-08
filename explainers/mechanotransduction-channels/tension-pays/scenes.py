"""Tension Pays for Area — revised diagrams and transcript-timed beats.
COLOR MAP: BLUE channel body; GREY membrane/axes; YELLOW tension/work;
PURPLE area; GREEN open; RED closed/resting energy; GOLD title only.
Comparison identities only: SALMON channel A, MINT channel B (s10–s15).
All traces: P=1/(1+exp((2.7-T)*area/4.1)); T in pN/nm,
area in nm²; thermal energy=4.1 pN nm. Shared T50 is illustrative.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
SALMON='#FF9FAD'
MINT='#63E6BD'

# Use real transcript time with zero lead. The shared logger reports pre-wait
# time as 'now'; negative 'late' values in the old log were waiting, not drift.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target=self.t_of(phrase,nth)-lead
        if target-self.elapsed()>.001:
            self.wait(target-self.elapsed())
        if self.elapsed()-target>.14:
            raise ValueError(f'Late cue {phrase}: {self.elapsed()-target:.3f}s')


def heading(s):
    return T(s,34,font=TITLE_FONT).move_to([0,3.1,0])


def sub(base, suffix, size=38, color=TEXT):
    a=T(base,size,color); b=T(suffix,size*.70,color)
    b.next_to(a,RIGHT,buff=.015).shift(DOWN*.16)
    return VGroup(a,b)


def thermal(size=38,color=YELLOW):
    return VGroup(sub('k','B',size,color),T('·',size,color),sub('T','abs',size,color)).arrange(RIGHT,buff=.10)


def formula(parts,size=38):
    return VGroup(*[thermal(size,c) if s=='THERMAL' else T(s,size,c) for s,c in parts]).arrange(RIGHT,buff=.16)


def channel(x=0,y=0,opened=False,r=1.65):
    body=Circle(r,color=BLUE,fill_color=BLUE,fill_opacity=.20).move_to([x,y,0])
    pore=Circle(.48 if opened else .18,color=GREEN if opened else RED,
                fill_color=BG if opened else RED,fill_opacity=1,stroke_width=7).move_to(body)
    if opened:
        wedge=AnnularSector(inner_radius=.48,outer_radius=.75,angle=PI*1.65,start_angle=.18,
                            color=GREEN,fill_opacity=.8).move_to(body)
    else:
        wedge=Line(body.get_center()+LEFT*.45,body.get_center()+RIGHT*.45,color=RED,stroke_width=9)
    return VGroup(body,pore,wedge)


def sheet(w=9.4,h=4.4):
    return RoundedRectangle(width=w,height=h,corner_radius=.18,color=GREY,fill_color=GREY,fill_opacity=.10)


def force_arrows(x=4.7):
    return VGroup(Arrow([-x,0,0],[-x-1,0,0],buff=0,color=YELLOW,stroke_width=6),
                  Arrow([x,0,0],[x+1,0,0],buff=0,color=YELLOW,stroke_width=6))


def energy(t):
    yc=-.1; yo=yc+.9*(3-t)
    bars=VGroup(Line([-3.9,yc,0],[-1.1,yc,0],color=RED,stroke_width=9),
                Line([1.1,yo,0],[3.9,yo,0],color=GREEN,stroke_width=9))
    labs=VGroup(T('closed',30,RED).move_to([-2.5,-1.9,0]),T('open',30,GREEN).move_to([2.5,-1.9,0]))
    axis=VGroup(Arrow([-4.7,-1.5,0],[-4.7,2.8,0],buff=0,color=GREY),T('Energy',28).rotate(PI/2).move_to([-5.3,.7,0]))
    return VGroup(bars,labs,axis).shift(RIGHT*.45)


def gap(t):
    # Resting gap remains as reference; current gap narrows with tension.
    ref=VGroup(DoubleArrow([.35,-.1,0],[.35,2.6,0],color=RED,buff=0),T('ΔG₀',30,RED).move_to([-.25,2.45,0]))
    if t<2.99:
        ref.add(DoubleArrow([.8,-.1,0],[.8,-.1+.9*(3-t),0],buff=0,color=TEXT,tip_length=.12))
    return ref.shift(RIGHT*.45)


def tension_slider(t):
    return VGroup(Line([-4.5,-2.65,0],[4.5,-2.65,0],color=YELLOW),
                  Dot([-4.5+9*t/5,-2.65,0],color=YELLOW,radius=.13),
                  T('Tension',28,YELLOW).move_to([-3.1,-3.2,0]),
                  Line([.9,-2.85,0],[.9,-2.45,0],color=TEXT),
                  T('ΔG = 0',28).move_to([.9,-3.25,0]),
                  Line([.9,-2.85,0],[.9,-3.0,0],color=TEXT))


def prob(t,a):
    return 1/(1+np.exp(np.clip((2.7-np.asarray(t))*a/4.1,-700,700)))


def plot_base():
    ax=Axes(x_range=[0,5.4,1],y_range=[0,1,.5],x_length=10.6,y_length=4.5,
        axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([.1,-.05,0])
    labs=VGroup(T('Fraction open',28,GREEN).move_to([-3.9,2.65,0]),
        T('Tension',28,YELLOW).move_to([0,-3.1,0]),
        T('0',26).next_to(ax.c2p(0,0),LEFT,buff=.18),
        T('½',26).next_to(ax.c2p(0,.5),LEFT,buff=.18),
        T('1',26).next_to(ax.c2p(0,1),LEFT,buff=.18))
    return ax,labs


def curve(ax,a,color=GREEN):
    return ax.plot(lambda x:float(prob(x,a)),x_range=[0,5.4,.003],color=color,stroke_width=5,use_smoothing=False)


def halfmark(ax):
    return VGroup(DashedLine(ax.c2p(2.7,0),ax.c2p(2.7,.5),color=YELLOW),
        Dot(ax.c2p(2.7,.5),color=YELLOW,radius=.09),
        T('T₅₀',26,YELLOW).move_to(ax.c2p(2.7,0)+DOWN*.30))


def widthmark(ax,a=5):
    k=4.1/a
    p=ax.c2p(2.7,.5); q=ax.c2p(2.7+k,.5)
    return VGroup(Line(p,q,color=PURPLE,stroke_width=5),
        Line(p+DOWN*.10,p+UP*.10,color=PURPLE),Line(q+DOWN*.10,q+UP*.10,color=PURPLE),
        T('k',28,PURPLE).move_to((p+q)/2+DOWN*.35))


def comparison():
    ax,labs=plot_base()
    lines=VGroup(curve(ax,5,SALMON),curve(ax,300,MINT))
    # Direct labels with leaders, away from both traces.
    labels=VGroup(T('A: 5 nm²',28,SALMON).move_to([3.7,.65,0]),
        Line([3,.9,0],ax.c2p(4.15,prob(4.15,5)),color=SALMON),
        T('B: 300 nm²',28,MINT).move_to([2.5,3.1,0]),
        Line([1.5,2.9,0],ax.c2p(2.76,prob(2.76,300)),color=MINT))
    return ax,labs,lines,labels,halfmark(ax)


def prediction():
    # Equal closed footprints, area-gain rings whose AREAS differ exactly 60×.
    # Common inner radius .62; gain for B = π(1.72²−.62²).
    r0=.62; rb=1.72; ra=np.sqrt(r0*r0+(rb*rb-r0*r0)/60)
    icons=VGroup()
    for x,r,col in [(-3,ra,SALMON),(3,rb,MINT)]:
        ring=Annulus(inner_radius=r0,outer_radius=r,color=col,fill_opacity=.65,stroke_width=0).move_to([x,.15,0])
        core=Circle(r0,color=BLUE,fill_color=BLUE,fill_opacity=.15,stroke_width=1).move_to([x,.15,0])
        icons.add(VGroup(ring,core,Circle(r,color=col,stroke_width=2).move_to([x,.15,0])))
    labels=VGroup(T('A: 5 nm²',30,SALMON).move_to([-3,-1.9,0]),T('B: 300 nm²',30,MINT).move_to([3,-1.9,0]))
    axis=VGroup(Line([-5.3,-2.6,0],[5.3,-2.6,0],color=YELLOW,stroke_width=4),
        Line([0,-2.8,0],[0,-2.4,0],color=TEXT,stroke_width=5),
        T('Same tension · each 50% open',28).move_to([0,-3.25,0]))
    states=VGroup()
    for x in [-3,3]:
        states.add(VGroup(Rectangle(width=.8,height=.14,color=GREY).move_to([x,.42,0]),
            Rectangle(width=.4,height=.14,color=GREEN,fill_opacity=1).move_to([x-.2,.42,0]),
            T('50%',26,GREEN).move_to([x,-.02,0])))
    axis.add(T('Area gained to scale: B = 60 × A',24,PURPLE).move_to([0,-3.65,0]))
    return icons,labels,axis,states


def question():
    return VGroup(T('Which switches over the',32,font=TITLE_FONT),
        T('narrower range of tension?',32,font=TITLE_FONT)).arrange(DOWN,buff=.20).move_to([0,2.7,0])


def small_energy():
    # Large left panel, carried unchanged into the ratio scene.
    return VGroup(T('Energy',30).move_to([-3.7,2.5,0]),
        Line([-5.7,-1.35,0],[-3.9,-1.35,0],color=RED,stroke_width=8),
        Line([-3.1,1.45,0],[-1.3,1.45,0],color=GREEN,stroke_width=8),
        T('closed',30,RED).move_to([-4.8,-1.9,0]),T('open',30,GREEN).move_to([-2.2,2.0,0]),
        DoubleArrow([-3.5,-1.35,0],[-3.5,1.45,0],color=TEXT,buff=0),
        T('ΔG',32).move_to([-2.7,-.1,0]))


def empty_axis():
    ax=Axes(x_range=[0,5.4,1],y_range=[0,1,.5],x_length=5.1,y_length=4.6,
        axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([3.1,-.1,0])
    return VGroup(ax,T('Fraction open',28,GREEN).move_to([3.1,2.6,0]),T('Tension',28,YELLOW).move_to([3.1,-2.9,0]))


class S00Title(TitleCard):
    TITLE='Tension Pays for Area'
    LESSON='Piezo Channels and the Physics of Force'

class S01Question(TimedScene):
    def construct(self):
        mem=sheet(); c=channel(); ar=force_arrows()
        self.add(heading('Tension Pays for Area'),mem,c)
        self.at('Why should stretching')
        self.play(FadeIn(ar),run_time=.6)
        self.at('open a channel')
        self.play(Transform(c,channel(opened=True)),run_time=.7)
        self.finish()

class S02States(TimedScene):
    def construct(self):
        self.add(channel(-3),channel(3,opened=True))
        self.at('Start with the simplest')
        self.play(FadeIn(heading('Two possible states')),run_time=.5)
        self.at('either closed')
        self.play(FadeIn(T('closed',36,RED).move_to([-3,-2.3,0])),run_time=.28)
        self.at('or open')
        self.play(FadeIn(T('open',36,GREEN).move_to([3,-2.3,0])),run_time=.28)
        self.finish()

class S03Area(TimedScene):
    def construct(self):
        c=channel(-3); o=channel(3,opened=True)
        closed=T('closed',32,RED).move_to([-3,-2.3,0])
        opened=T('open',32,GREEN).move_to([3,-2.3,0])
        # Align the lowercase o glyphs, so the p descender cannot shift the baseline.
        opened.shift(UP*(closed[2].get_center()[1]-opened[0].get_center()[1]))
        self.add(c,o,closed,opened)
        self.at('The open state')
        ring=Annulus(inner_radius=1.65,outer_radius=2,color=PURPLE,fill_opacity=.5).move_to([3,0,0])
        self.play(Transform(o,channel(3,opened=True,r=2)),FadeIn(ring),run_time=1.2)
        self.at('plane of the membrane')
        self.play(FadeIn(heading('Top view: membrane plane')),run_time=.4)
        self.at('Call the extra amount')
        self.play(Indicate(ring,color=PURPLE,scale_factor=1.02),run_time=.35)
        self.at('the area gained')
        label=T('ΔA: area gained',30,PURPLE).move_to([-.2,-1.7,0])
        self.play(FadeIn(label),Create(Line(label.get_right()+RIGHT*.10,[1.65,-1.45,0],color=PURPLE)),run_time=.4)
        self.finish()

class S04Tension(TimedScene):
    def construct(self):
        self.add(sheet(),channel())
        self.at('Membrane tension')
        self.play(FadeIn(force_arrows()),run_time=.5)
        self.at('an in')
        self.play(FadeIn(heading('In-plane stretch')),run_time=.5)
        self.at('force per unit length')
        markers=VGroup(T('force',28,YELLOW).move_to([-5.25,.6,0]),
            Line([4.9,-2.15,0],[4.9,2.15,0],color=TEXT),
            Line([4.7,-2.15,0],[5.1,-2.15,0],color=TEXT),Line([4.7,2.15,0],[5.1,2.15,0],color=TEXT),
            T('length',28).rotate(PI/2).move_to([5.5,1.2,0]),T('T = force / length',38,YELLOW).move_to([0,-3,0]))
        self.play(FadeIn(markers),run_time=.6)
        self.finish()

class S05Work(TimedScene):
    def construct(self):
        mem=sheet(8,3.6); c=channel(r=1.35); ar=force_arrows(4); self.add(mem,c,ar)
        self.at('Stretching a membrane')
        self.play(Transform(mem,sheet(9.4,4.4)),Transform(ar,force_arrows(4.7)),
            Transform(c,channel(opened=True,r=1.65)),run_time=3.6)
        self.at('That work is')
        packet=chip('T × ΔA',YELLOW,32).move_to([-4.0,1.4,0])
        self.add(packet)
        self.at('tension times')
        # End outside the widened channel, with a clear visible gap to its rim.
        path=VMobject().set_points_smoothly([[-4,1.4,0],[-3.9,1.8,0],[-3.3,1.9,0],[-2.8,1.7,0]])
        self.play(MoveAlongPath(packet,path),Transform(mem,sheet(11,5.6)),
            Transform(ar,force_arrows(5.5)),Transform(c,channel(opened=True,r=2)),run_time=1.5)
        self.finish()

class S06Lower(TimedScene):
    def construct(self):
        e=energy(0); s=tension_slider(0); g=gap(0); self.add(e,s,g)
        self.at('So tension lowers')
        self.play(Transform(e,energy(2)),Transform(s,tension_slider(2)),Transform(g,gap(2)),run_time=2.5)
        self.finish()

class S07Equation(TimedScene):
    def construct(self):
        self.add(heading('Energy of open relative to closed'))
        a=T('ΔG',58).move_to([-4.3,.6,0]); eq=T('=',48).move_to([-2.8,.6,0]); b=T('ΔG₀',58,RED).move_to([-1,.6,0]); c=T('− T × ΔA',58,YELLOW).move_to([3.2,.6,0])
        self.at('Write it out'); self.play(FadeIn(a),run_time=.4)
        self.at('The energy difference')
        self.play(FadeIn(VGroup(Line([-5.2,-.2,0],[-3.4,-.2,0]),T('energy',28).move_to([-4.3,-1,0]),T('difference',28).move_to([-4.3,-1.6,0]))),run_time=.4)
        self.at('equals the resting')
        self.play(FadeIn(eq),FadeIn(b),FadeIn(VGroup(Line([-2.2,-.2,0],[.2,-.2,0],color=RED),T('resting preference',28,RED).move_to([-1,-1,0]),T('for closed',28,RED).move_to([-1,-1.6,0]))),run_time=.6)
        self.at('minus tension times')
        self.play(FadeIn(c),FadeIn(VGroup(Line([1.3,-.2,0],[5.1,-.2,0],color=YELLOW),T('work from',28,YELLOW).move_to([3.2,-1,0]),T('tension',28,YELLOW).move_to([3.2,-1.6,0]))),run_time=.6)
        self.finish()

class S08Slack(TimedScene):
    def construct(self):
        e=energy(0); s=tension_slider(0); g=gap(0); self.add(e,s,g)
        self.at('In a slack membrane'); self.wait(.2)
        self.at('As tension rises')
        self.play(Transform(e,energy(2)),Transform(s,tension_slider(2)),Transform(g,gap(2)),run_time=1.7)
        self.finish()

class S09Cross(TimedScene):
    def construct(self):
        e=energy(2); s=tension_slider(2); g=gap(2); self.add(e,s,g)
        self.at('At one particular tension')
        self.play(Transform(e,energy(3)),Transform(s,tension_slider(3)),Transform(g,gap(3)),run_time=1.6)
        self.at('the preference disappears')
        self.play(FadeOut(g),Indicate(s[4],color=YELLOW),run_time=.6)
        self.at('Above it')
        self.play(Transform(e,energy(4.5)),Transform(s,tension_slider(4.5)),run_time=1)
        self.finish()

class S10Predict(TimedScene):
    def construct(self):
        icons,labels,axis,states=prediction(); self.add(icons,labels)
        self.at('Two channels'); self.play(FadeIn(heading('Area gained on opening')),run_time=.5)
        self.at('each open half the time'); self.play(FadeIn(states),FadeIn(axis),run_time=.6)
        self.at('One gains'); self.play(Indicate(labels[0],color=SALMON),Indicate(icons[0][0],color=SALMON),run_time=.6)
        self.at('The other gains'); self.play(Indicate(labels[1],color=MINT),Indicate(icons[1][0],color=MINT),run_time=.6)
        self.finish()

class S11PredictQ(TimedScene):
    def construct(self):
        self.add(*prediction())
        self.at('Which one goes'); self.play(FadeIn(question()),run_time=.6); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(*prediction(),question()); self.wait(5)

class S13Reveal(TimedScene):
    def construct(self):
        ax,labs,lines,labels,half=comparison(); self.add(ax,labs,half)
        self.at('The 300 channel'); self.play(Create(lines[1]),FadeIn(labels[2:]),run_time=.8)
        self.at('each small rise'); self.play(Create(lines[0]),FadeIn(labels[:2]),run_time=.8)
        self.at('gives it sixty times'); self.play(FadeIn(T('300 ÷ 5 = 60',32,YELLOW).move_to([-3.2,1.1,0])),run_time=.5)
        self.finish()


def stepmark(ax):
    p=ax.c2p(2.62,0); q=ax.c2p(2.78,0)
    return VGroup(Line(p+DOWN*.05,p+DOWN*.45,color=YELLOW),Line(q+DOWN*.05,q+DOWN*.45,color=YELLOW),
        Line(p+DOWN*.4,q+DOWN*.4,color=YELLOW,stroke_width=5),
        T('same tiny step',26,YELLOW).move_to([2,-2.75,0]),Line([.65,-2.72,0],(p+q)/2+DOWN*.4,color=YELLOW))

class S14Reveal2(TimedScene):
    def construct(self):
        ax,labs,lines,labels,half=comparison(); self.add(ax,labs,lines,labels,half)
        dots=VGroup(*[Dot(ax.c2p(2.62,prob(2.62,a)),radius=.12,color=col) for a,col in [(5,SALMON),(300,MINT)]])
        self.at('a small change'); self.play(FadeIn(dots),FadeIn(stepmark(ax)),run_time=.4)
        self.at('swings it all')
        self.play(*[MoveAlongPath(dot,ax.plot(lambda x,a=a:float(prob(x,a)),x_range=[2.62,2.78,.001],use_smoothing=False)) for dot,a in zip(dots,[5,300])],run_time=2.4)
        self.finish()

class S15Hold(Scene):
    def construct(self):
        self.camera.background_color=BG
        ax,labs,lines,labels,half=comparison(); self.add(ax,labs,lines,labels,half,stepmark(ax))
        self.add(*[Dot(ax.c2p(2.78,prob(2.78,a)),radius=.12,color=c) for a,c in [(5,SALMON),(300,MINT)]])
        self.wait(3)

class S16Boltzmann(TimedScene):
    def construct(self):
        e=energy(2); self.add(e)
        self.at('To turn the energy'); self.wait(.2)
        self.at('into a curve')
        self.add(empty_axis())
        self.play(ReplacementTransform(e,small_energy()),run_time=.8)
        self.at('use the Boltzmann relation'); self.play(FadeIn(heading('Boltzmann relation')),run_time=.6)
        self.finish()

class S17Ratio(TimedScene):
    def construct(self):
        self.add(heading('Boltzmann relation'),small_energy(),empty_axis())
        self.at('For a two'); self.play(FadeOut(self.mobjects[-1]),run_time=.5)
        ratio=T('open / closed',40).move_to([2,1.25,0])
        rhs=formula([('= exp(',TEXT),('−ΔG',TEXT),('/ (',TEXT),('THERMAL',YELLOW),('))',TEXT)],38).move_to([2,-.15,0])
        pieces=VGroup(ratio,*rhs)
        self.at('the ratio of open to closed'); self.play(FadeIn(pieces[0]),run_time=.4)
        self.at('depends on'); self.play(FadeIn(pieces[1]),FadeIn(pieces[-1]),run_time=.4)
        self.at('the energy difference'); self.play(FadeIn(pieces[2]),Indicate(self.mobjects[1][-1]),run_time=.4)
        self.at('compared with thermal energy')
        self.add(pieces[3:5].set_opacity(1),
            T('Thermal energy ≈ 4.1 × 10⁻²¹ J at room temperature',30,'#FFFF00').move_to([0,-2.95,0]))
        rhs[3].set_color('#FFFF00').set_opacity(1)
        self.finish()

class S18Curve(TimedScene):
    def construct(self):
        ax,labs=plot_base()
        eq=formula([('P(open) = 1 / [1 + exp((',TEXT),('T₅₀',YELLOW),('− T) /',TEXT),('k',PURPLE),(')]',TEXT)],30).move_to([0,3.2,0])
        source=formula([('open / closed = exp(−ΔG / (',TEXT),('THERMAL',YELLOW),('))',TEXT)],30).move_to([0,3.2,0])
        self.add(ax,labs,source)
        self.at('For a two'); self.play(ReplacementTransform(source,eq),run_time=1)
        line=curve(ax,5)
        self.at('this gives the fraction'); self.play(Create(line),run_time=1.8)
        # Preview both fitted parameters, then emphasize each at its spoken name.
        half=halfmark(ax); width=widthmark(ax)
        self.add(half,width)
        self.at('Patch papers fit'); self.play(Indicate(line,color=GREEN,scale_factor=1.01),run_time=.7)
        self.at('That reading assumes'); self.play(FadeIn(T('Assumes normalized current tracks fraction open',26).move_to([0,-3.6,0])),run_time=.6)
        self.at('The curve has'); self.play(Indicate(eq[1],scale_factor=1.1),Indicate(eq[3],scale_factor=1.1),run_time=.6)
        self.at('a half'); self.play(Indicate(half,color=YELLOW),Indicate(eq[1],color=YELLOW),run_time=.6)
        self.at('a slope factor'); self.play(Indicate(width,color=PURPLE),Indicate(eq[3],color=PURPLE),run_time=.6)
        self.finish()

class S19T50(TimedScene):
    def construct(self):
        ax,labs=plot_base(); mark=halfmark(ax); self.add(ax,labs,curve(ax,5),mark)
        eq=formula([('T₅₀ =',YELLOW),('ΔG₀',RED),('/',TEXT),('ΔA',PURPLE)],42).move_to([1.4,2.9,0])
        self.at('Match the two forms'); self.play(FadeIn(eq),run_time=.7)
        self.at('The half'); self.play(Indicate(mark,color=YELLOW),run_time=.6)
        p=ax.c2p(2.7,.5)
        self.at('the resting preference')
        self.add(Arrow(p+UP*.1,eq[1].get_bottom(),buff=.12,color=RED),
            T('resting preference for closed',26,RED).next_to(eq[1],UP,buff=.25))
        self.at('divided by the area gained')
        self.add(Arrow(p+RIGHT*.15,eq[3].get_bottom(),buff=.12,color=PURPLE),
            T('area gained',26,PURPLE).next_to(eq[3],RIGHT,buff=.35))
        self.finish()

class S20K(TimedScene):
    def construct(self):
        ax,labs=plot_base(); a=ValueTracker(5)
        line=always_redraw(lambda:curve(ax,a.get_value()))
        br=always_redraw(lambda:widthmark(ax,a.get_value()))
        labs[0].move_to([-4.1,3.2,0])
        self.add(ax,labs,line,br)
        eq=formula([('k =',PURPLE),('THERMAL',YELLOW),('/',TEXT),('ΔA',PURPLE)],38).move_to([1.7,3.2,0])
        self.at('The slope factor'); self.play(FadeIn(eq),run_time=.6)
        self.at('divided by the area gained')
        slider=VGroup(Line([-2.4,2.55,0],[2.4,2.55,0],color=PURPLE),T('ΔA',28,PURPLE).move_to([-3.1,2.55,0]))
        dot=Dot([-2.4,2.55,0],color=PURPLE)
        self.add(slider.set_opacity(1),dot.set_opacity(1))
        self.at('More area means')
        caption=T('ΔA × 4     k ÷ 4',32,'#FFFFFF').move_to([2.65,-.9,0])
        self.add(caption)
        self.play(a.animate.set_value(20),dot.animate.move_to([2.4,2.55,0]),run_time=2.6)
        self.finish()

class S21Units(TimedScene):
    def construct(self):
        card=RoundedRectangle(width=11.5,height=5.3,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.06)
        self.add(card,heading('One unit note'))
        left=T('1 pN/nm',54,YELLOW).move_to([-3,.5,0]); right=T('1 mN/m',54,YELLOW).move_to([3,.5,0])
        self.at('One unit note'); self.play(FadeIn(T('Force per length',32).move_to([0,1.8,0])),run_time=.5)
        self.at('pico'); self.play(FadeIn(left),FadeIn(T('structural papers',30).move_to([-3,-.6,0])),run_time=.6)
        self.at('milli'); self.play(FadeIn(right),FadeIn(T('patch papers',30).move_to([3,-.6,0])),run_time=.6)
        self.at('are the same quantity'); self.play(FadeIn(T('=',54).move_to([0,.5,0])),FadeIn(T('The same tension',32,YELLOW).move_to([0,-1.8,0])),run_time=.6)
        self.finish()

class S22Takeaway(TimedScene):
    def construct(self):
        self.add(heading('Tension pays for area.'))
        self.at('That is the one idea'); self.play(FadeIn(T('ΔG = ΔG₀ − T × ΔA',48,YELLOW).move_to([0,1.9,0])),run_time=.7)
        self.at('Tension pays for area'); self.play(Indicate(self.mobjects[-1],color=YELLOW),run_time=.6)
        self.at('In a two')
        self.play(FadeIn(T('Two-state model',30).move_to([0,.8,0])),FadeIn(T('T₅₀ = ΔG₀ / ΔA',42).move_to([0,-.1,0])),run_time=.6)
        self.at('the area sets')
        note1=VGroup(sub('k','B',28),T(': Boltzmann’s constant',28)).arrange(RIGHT,buff=.1).move_to([0,-2.25,0])
        note2=VGroup(sub('T','abs',28),T(': absolute temperature',28)).arrange(RIGHT,buff=.1).move_to([0,-2.85,0])
        self.play(FadeIn(formula([('k =',PURPLE),('THERMAL',YELLOW),('/ ΔA',PURPLE)],40).move_to([0,-1.15,0])),
            FadeIn(note1),FadeIn(note2),FadeIn(T('T: membrane tension',28,YELLOW).move_to([0,-3.45,0])),run_time=.6)
        self.finish()

class S23End(EndCard):
    LINE='Tension pays for area; more area, a steeper switch.'
    def construct(self):
        lines=VGroup(T('Tension pays for area;',44,font=TITLE_FONT),T('more area, a steeper switch.',44,font=TITLE_FONT)).arrange(DOWN,buff=.45)
        self.play(FadeIn(lines),run_time=.6)
        self.add(T('Two-state model',28).move_to([0,-1.5,0]),T('biochemistrypedia.com',26,TEAL).move_to([0,-2.3,0]))
        self.finish()
