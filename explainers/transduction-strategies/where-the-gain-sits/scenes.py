"""COLOR MAP: YELLOW stimulus/latency; BLUE channels/receptors; PURPLE enzymes/gain;
GREEN current/activation; TEAL excitation; GREY membrane/axes; TEXT labels; RED negation.
All chips are cartoons, never molecular structures. Event rasters are schematic.
The timing inset is computed from unit-rate sequential first-order steps, not fitted data.
"""
from bp_style import *
import numpy as np

PURPLE = '#B58CD9'
LIGHT = '#BEC5D0'

# Keep word-aligned cues without creating an extra sync.log deliverable.
class SyncedScene(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def heading(s): return T(s,32,font=TITLE_FONT).move_to([0,3.18,0])
def note(s): return T(s,26,LIGHT).move_to([0,-3.18,0])
def bchip(s,c=PURPLE,size=28,pad=.3):
    g=chip(s,c,size=size,pad=pad,fill_opacity=.14)
    back=RoundedRectangle(width=g[0].width,height=g[0].height,corner_radius=.14,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(g)
    return VGroup(back,*g)
def arrow(a,b,c=PURPLE): return Arrow(a,b,buff=.12,color=c,stroke_width=4,tip_length=.18)
def span(a,b,y,c=YELLOW):
    return VGroup(Line([a,y,0],[b,y,0],color=c,stroke_width=4),*[Line([x,y-.12,0],[x,y+.12,0],color=c) for x in (a,b)])
def marker(n):
    y=(2.55,.2,-1.85)[n-1]
    dot=Dot([-5.9,y,0],radius=.1,color=YELLOW)
    return VGroup(dot,T('photon\nrung '+str(n),22,YELLOW).next_to(dot,RIGHT,buff=.2))

YS=(1.65,-.1,-1.85)
def ladder(tags=None,center=False):
    x=0 if center else -1.7
    rows=VGroup()
    for i,(y,s) in enumerate(zip(YS,('1  Rho* → transducin → PDE6','2  cGMP breakdown','3  CNG channels close'))):
        box=RoundedRectangle(width=7.6,height=1.15,corner_radius=.14,color=PURPLE if i<2 else BLUE,fill_opacity=.1)
        rows.add(VGroup(box,T(s,28,PURPLE if i<2 else BLUE)).move_to([x,y,0]))
    links=VGroup(*[arrow([x,YS[i]-.6,0],[x,YS[i+1]+.6,0],LIGHT) for i in range(2)])
    g=VGroup(rows,links); g.rows=rows; g.tags=VGroup()
    if tags:
        for i,s in tags.items(): g.tags.add(bchip(s).move_to([4.3,YS[i],0]))
        g.add(g.tags)
    return g

def question(): return VGroup(heading('Which step multiplies the signal more?'),ladder({0:'× ?',1:'× ?'}),note('If the two estimates combine'))
def pore(x,y,name,opened=False):
    walls=VGroup(*[RoundedRectangle(width=.28,height=1.5,corner_radius=.06,color=BLUE,fill_opacity=.4).move_to([x+d,y,0]) for d in (-.5,.5)])
    gate=Line([x-.36,y,0],[x+.36,y,0],color=BLUE,stroke_width=8)
    if opened: gate.set_opacity(0)
    g=VGroup(walls,gate,T(name,28,BLUE).move_to([x,y-1.15,0])); g.gate=gate
    return g

def flow(x,y): return arrow([x,y+1.2,0],[x,y-1.6,0],GREEN)

class S00Title(TitleCard):
    LESSON='Five Ways to Turn a Stimulus into a Current'
    TITLE='Where the Gain Sits, and What It Costs'
    def construct(self):
        self.add(heading(self.LESSON))
        self.play(FadeIn(T('Where the Gain Sits,\nand What It Costs',46,font=TITLE_FONT)),run_time=.7)
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,-2.4,0])); self.finish()

class S01Q(SyncedScene):
    def construct(self):
        l=ladder(center=True); self.add(l,heading('Where is the gain?'))
        ph=Dot([-4.9,2.65,0],radius=.15,color=YELLOW); lab=T('photon',26,YELLOW).next_to(ph,RIGHT,buff=.2)
        self.at('Follow one photon'); self.play(FadeIn(ph),FadeIn(lab),run_time=.3)
        self.play(ph.animate.move_to([-3.45,1.65,0]),lab.animate.move_to([-3.45,2.6,0]),l.rows[0][0].animate.set_fill(PURPLE,opacity=.3),run_time=.9)
        self.finish()

class S02Step1(SyncedScene):
    def construct(self):
        self.add(heading('1 · Switch on an effective complex'),marker(1))
        rh=bchip('activated rhodopsin\n(Rho*)',BLUE,36).move_to([-2.5,1.35,0])
        tr=bchip('transducin',PURPLE,36).move_to([-2.5,-.45,0]); pd=bchip('PDE6',PURPLE,36).move_to([-2.5,-2.05,0])
        self.add(rh)
        self.at('switches on transducin'); self.play(FadeIn(tr),GrowArrow(arrow(rh.get_bottom(),tr.get_top())),run_time=.5)
        self.at('which switches on'); self.play(FadeIn(pd),GrowArrow(arrow(tr.get_bottom(),pd.get_top())),run_time=.6)
        br=Brace(VGroup(tr,pd),RIGHT,color=PURPLE)
        self.at('counted each active'); self.play(GrowFromCenter(br),run_time=.4)
        label=T('effective complex',34,PURPLE).move_to([2.3,-.8,0])
        self.play(FadeIn(label),FadeIn(T('A counting unit',28,LIGHT).move_to([2.3,-1.5,0])),
            FadeIn(T('Exact molecular make-up depends on the model',26,LIGHT).move_to([0,-3.15,0])),run_time=.5)
        self.finish()

class S03Step2(SyncedScene):
    def construct(self):
        self.add(heading('2 · One complex, many cGMP molecules'),marker(2))
        enz=bchip('effective\ncomplex',PURPLE,32)
        dots=VGroup(*[Dot([3.3*np.cos(t),2.1*np.sin(t)-.1,0],radius=.12,color=PURPLE) for t in np.linspace(0,2*PI,24,endpoint=False)])
        self.add(enz,dots,T('cGMP',28,PURPLE).move_to([4.6,1.6,0]))
        self.at('breaks down'); self.play(LaggedStart(*[d.animate.set_opacity(.12) for d in dots],lag_ratio=.09),run_time=2.1)
        self.at('many molecules each'); self.play(FadeIn(note('Many molecules per complex · and many more…')),run_time=.4)
        self.finish()

class S04Step3(SyncedScene):
    def construct(self):
        self.add(heading('3 · Falling cGMP closes channels'),marker(3))
        p=pore(0,-.35,'CNG channel',True).scale(1.9,about_point=[0,-.35,0]); f=flow(0,-.35).scale(1.3)
        mem=VGroup(Line([-5.7,-.35,0],[-1,-.35,0],color=GREY,stroke_width=12),Line([1,-.35,0],[5.7,-.35,0],color=GREY,stroke_width=12))
        bound=VGroup(*[Dot([x,.75,0],radius=.15,color=PURPLE) for x in (-.75,.75)])
        lab=T('bound cGMP',28,PURPLE).move_to([-3,1.7,0]); link=arrow(lab.get_right(),bound[0].get_top())
        status=T('OPEN',32,GREEN).move_to([3,-1.7,0])
        self.add(mem,p,f,bound,lab,link,status)
        self.at('the fall in'); self.play(bound.animate.shift(UP*.7).set_opacity(0),FadeOut(lab),FadeOut(link),run_time=.7)
        self.at('closes cyclic'); self.play(p.gate.animate.set_opacity(1),FadeOut(f),FadeOut(status),run_time=.5)
        self.add(T('CLOSED',32,BLUE).move_to([3,-1.7,0]),note('Less cGMP → channels close')); self.finish()

class S05Total(SyncedScene):
    def construct(self):
        l=ladder(center=True).shift(UP*.3); self.add(l,heading('Gain down the rod’s ladder'))
        block=VGroup(T('≈ 2,000 cGMP hydrolysed per photon',32,PURPLE),T('mouse rods · Arshavsky & Burns 2014',26,LIGHT)).arrange(DOWN,buff=.2).move_to([0,-2.95,0])
        self.at('In mouse rods'); self.play(FadeIn(block),run_time=.6); self.finish()

class S06Yue(SyncedScene):
    def construct(self):
        l=ladder(); self.add(l,heading('A separate estimate of step 1'),note('Yue et al. 2019 · Gcaps-null mouse rods'))
        self.at('estimated about'); tag=bchip('≈ 12–14',PURPLE,34).move_to([4.3,1.95,0]); self.play(FadeIn(tag),run_time=.5)
        self.at('effective complexes'); self.play(FadeIn(T('complexes per\nactivated rhodopsin',24,PURPLE).move_to([4.25,.95,0])),run_time=.4)
        self.play(Indicate(l.rows[0][0],color=YELLOW,scale_factor=1.03),run_time=2)
        self.at('activated rhodopsin'); self.play(Circumscribe(l.rows[0],color=YELLOW,time_width=.7),run_time=2); self.finish()

class S07Predict(SyncedScene):
    def construct(self):
        q=question(); self.add(q[0],q[1])
        self.at('If these two estimates'); self.play(FadeIn(q[2]),run_time=.4)
        self.at('which step multiplies'); self.play(*[Indicate(t,scale_factor=1.13,color=YELLOW) for t in q[1].tags],run_time=1); self.finish()

class S08Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(question()); self.wait(5)

class S09Reveal(SyncedScene):
    def construct(self):
        l=ladder({0:'≈ ×13'}).scale(.85).shift(UP*.65)
        l.rows[2].set_opacity(.25)
        self.add(l,heading('If the two estimates combine'),note('Combination of separate estimates · illustrative'))
        self.add(T('Gcaps-null',24,LIGHT).move_to([3.65,1.45,0]))
        calc=T('2,000 cGMP per photon\n÷ 13 complexes\n≈ 150 per complex',24,PURPLE).move_to([4.15,.2,0])
        self.at('If they combine'); self.play(FadeIn(calc),run_time=.6)
        enz=bchip('PDE6',PURPLE,28).move_to([-1.5,-2.15,0])
        incoming=arrow([-5,-2.15,0],enz.get_left()); outgoing=arrow(enz.get_right(),[2,-2.15,0],LIGHT)
        self.add(enz,incoming,outgoing,T('cGMP',26,PURPLE).move_to([-4.8,-1.55,0]),T('products',26,LIGHT).move_to([1.8,-1.55,0]))
        self.at('Each complex would')
        for unused in range(6):
            ins=VGroup(*[Dot([-5.3+j*.5,-2.15,0],radius=.1,color=PURPLE) for j in range(3)])
            outs=VGroup(*[Dot(enz.get_right()+RIGHT*j*.3,radius=.1,color=LIGHT) for j in range(3)])
            self.add(ins,outs)
            self.play(ins.animate.shift(RIGHT*2.1),outs.animate.shift(RIGHT*2.0),run_time=.7,rate_func=linear)
            self.remove(ins,outs)
        self.at('That is an illustration')
        self.play(Transform(calc,T('≈ ×150\nIllustration, not a\nmeasured yield',26,PURPLE).move_to(calc)),run_time=.5)
        self.finish()

class S10Lamb(SyncedScene):
    def construct(self):
        l=ladder(); a=bchip('≈ ×13',PURPLE,30).move_to([4.4,1.65,0]); b=bchip('≈ ×150',PURPLE,30).move_to([4.4,-.1,0])
        self.add(l,a,b,heading('Model-dependent estimates · Lamb 2022'))
        self.add(*[T('illustrative',26,LIGHT).move_to([4.4,y-.8,0]) for y in (1.43,-.1)])
        self.at('other analyses put'); band=DashedVMobject(RoundedRectangle(width=7.9,height=1.4,corner_radius=.15,color=PURPLE).move_to(l.rows[0]),num_dashes=28); self.play(Create(band),run_time=.4)
        self.at('several times higher')
        larger=bchip('×13 → larger\nmodel-dependent',PURPLE,26,pad=.45).move_to([4.4,1.65,0])
        self.play(ReplacementTransform(a,larger),run_time=1.5,rate_func=smooth)
        self.at('the two factors')
        wide=bchip('≈ ×150',PURPLE,30).move_to(b)
        wide[0].stretch_to_fit_width(larger.width); wide[1].stretch_to_fit_width(larger.width)
        self.play(ReplacementTransform(b,wide),run_time=1.2,rate_func=smooth)
        self.add(note('Factors could be comparable · estimates remain illustrative')); self.finish()

class S11Either(SyncedScene):
    def construct(self):
        l=ladder({0:'≈ ×13',1:'≈ ×150'}).scale(.8).shift(UP*.7); l.rows[2].set_opacity(.3)
        for row in l.rows[:2]: row[0].set_fill(PURPLE,opacity=.27)
        self.add(l,heading('Both steps amplify'))
        self.at('The gain belongs')
        core=bchip('The gain belongs to particular enzymes,\nnot to the label',PURPLE,28,pad=.4).move_to([0,-2.2,0])
        self.play(FadeIn(core),run_time=.4)
        self.at('not to the receptor'); gp=bchip('GPCR',BLUE,26,pad=.2).move_to([2.5,-2.48,0]); self.play(FadeIn(gp),run_time=.25)
        self.play(Create(Line(gp.get_left(),gp.get_right(),color=RED,stroke_width=6)),run_time=.25)
        self.finish()

class S12Frog(SyncedScene):
    def construct(self):
        self.add(heading('A receptor step need not amplify'))
        mem=RoundedRectangle(width=11.8,height=3.8,corner_radius=1.5,color=GREY,stroke_width=8).move_to([0,-.2,0])
        self.add(mem,T('frog olfactory cilium',28,LIGHT).move_to([0,-.2,0]))
        receptors=VGroup(); slots=VGroup(); odors=VGroup()
        for y,sign in ((1.7,1),(-2.1,-1)):
            for x in (-4.2,-1.4,1.4,4.2):
                receptors.add(bchip('R',BLUE,28).move_to([x,y,0]))
                odors.add(Dot([x,y+sign*.52,0],radius=.13,color=YELLOW))
                slots.add(DashedVMobject(RoundedRectangle(width=1,height=.5,corner_radius=.08,color=LIGHT).move_to([x,y-sign*.75,0]),num_dashes=10))
        self.add(receptors,odors,T('odorant',26,YELLOW).move_to([-5.1,2.65,0]))
        self.at('In frog olfactory neurons'); self.play(FadeIn(slots),run_time=.4)
        self.add(T('empty slots: no active G protein',26,LIGHT).move_to([0,.4,0]))
        self.at('one bound receptor'); self.play(Indicate(receptors[0],color=YELLOW),run_time=.4)
        self.at('rarely activates'); active=bchip('G',PURPLE,26).move_to(slots[0]); self.remove(slots[0]); self.add(active)
        self.add(T('one rare active G protein',26,PURPLE).move_to([0,-.8,0]),note('Bhandawat, Reisert & Yau 2005 · schematic, not a frequency'))
        self.finish()

class S13Olflater(SyncedScene):
    def construct(self):
        self.add(heading('Olfaction · gain thought to come later'))
        mem=VGroup(*[Line([a,.8,0],[b,.8,0],color=GREY,stroke_width=10) for a,b in ((-6,.3),(1.7,4.1),(5.5,6))])
        ac=bchip('adenylyl\ncyclase',PURPLE,32).move_to([-4.6,.8,0]); camp=bchip('cAMP',PURPLE,32).move_to([-3,-1.65,0])
        p=pore(1,.8,'CNG').scale(1.3,about_point=[1,.8,0]); cl=pore(4.8,.8,'chloride').scale(1.3,about_point=[4.8,.8,0])
        p[2].move_to([2.1,-.7,0])
        self.add(mem,ac,p,cl,T('outside',26,LIGHT).move_to([-5,2.5,0]),T('inside',26,LIGHT).move_to([-5,-2.4,0]))
        self.at('Adenylyl cyclase makes'); self.play(GrowArrow(arrow(ac.get_bottom(),camp.get_top())),FadeIn(camp),run_time=.5)
        self.at('which opens channels'); self.play(GrowArrow(arrow(camp.get_right(),[.35,-.18,0])),p.gate.animate.set_opacity(0),run_time=.5)
        self.at('The calcium that enters'); ca=bchip('calcium',GREEN,28).move_to([1,2.5,0]); self.add(ca)
        self.play(GrowArrow(arrow([1,2.1,0],[1,-1.8,0],GREEN)),ca.animate.move_to([1,-2.4,0]),run_time=.8)
        self.at('opens a chloride'); self.play(GrowArrow(arrow(ca.get_right(),[4.15,-.18,0],GREEN)),cl.gate.animate.set_opacity(0),run_time=.5)
        self.play(GrowArrow(arrow([4.8,-.1,0],[4.8,2.5,0],GREEN)),run_time=.4)
        self.add(note('Calcium entry → chloride channel opens')); self.finish()

class S14Time(SyncedScene):
    def construct(self):
        self.add(heading('Each step has its own rate'))
        rows=VGroup(*[bchip(s,PURPLE if i<2 else BLUE,28).move_to([-3.7,1.6-i*1.65,0]) for i,s in enumerate(('1  activation','2  turnover','3  channel'))]); self.add(rows)
        clocks=VGroup()
        for y in (1.6,-.05,-1.7):
            c=Circle(radius=.36,color=LIGHT).move_to([-.9,y,0]); h=Line(c.get_center(),c.get_center()+UP*.3,color=TEXT); clocks.add(VGroup(c,h))
        self.at('Every rung is'); self.play(FadeIn(clocks),run_time=.3)
        self.play(Rotate(clocks[0][1],-2*PI,about_point=clocks[0][0].get_center()),run_time=1.1)
        self.at('or an enzyme'); self.play(Rotate(clocks[1][1],-2*PI,about_point=clocks[1][0].get_center()),run_time=1.1)
        self.play(Rotate(clocks[2][1],-2*PI,about_point=clocks[2][0].get_center()),run_time=.8)
        self.at('So the current rises')
        # Unit-rate sequential first-order model: direct=1-exp(-t), cascade=Erlang CDF k=3.
        ax=Axes(x_range=[0,8,2],y_range=[0,1,.5],x_length=5,y_length=3.3,tips=False,axis_config={'color':LIGHT}).move_to([3.25,.2,0])
        direct=ax.plot(lambda t:1-np.exp(-t),x_range=[0,8],color=BLUE)
        cascade=ax.plot(lambda t:1-np.exp(-t)*(1+t+t*t/2),x_range=[0,8],color=PURPLE)
        self.play(Create(ax),Create(direct),Create(cascade),run_time=.8)
        self.add(T('direct',26,BLUE).move_to([1.9,2.3,0]),T('cascade',26,PURPLE).move_to([4.5,2.3,0]),T('current',26,LIGHT).move_to([1.1,-2,0]),T('time →',26,LIGHT).move_to([4.5,-2,0]),note('No fixed cost per rung · schematic model, not to scale'))
        self.finish()

# Measured first-spike anchors only; other event marks are schematic, not recordings.
def latency_view():
    def xx(t): return -5.6+11.2*t/60
    g=VGroup(); axis=Line([xx(0),-2.25,0],[xx(60),-2.25,0],color=LIGHT); g.add(axis)
    for t in (0,20,25,40,60):
        g.add(Line([xx(t),-2.35,0],[xx(t),-2.15,0],color=LIGHT),T(str(t),26,LIGHT).move_to([xx(t),-2.65,0]))
    pulse=VMobject(color=YELLOW,stroke_width=4).set_points_as_corners([[-6,1.6,0],[xx(0),1.6,0],[xx(0),2.15,0],[5.7,2.15,0]])
    g.add(pulse,arrow([5.2,2.15,0],[6,2.15,0],YELLOW),T('high-dose odour pulse · 100 ms →',26,YELLOW).move_to([0,2.6,0]))
    for y,first,events in ((.55,25,(25,34,46,55)),(-1.15,40,(40,50,58))):
        g.add(Line([xx(0),y,0],[xx(60),y,0],color=GREY))
        for t in events: g.add(Line([xx(t),y,0],[xx(t),y+.7,0],color=GREEN,stroke_width=4))
        g.add(Arrow([xx(first),y+1.1,0],[xx(first),y+.72,0],buff=0,color=GREEN,stroke_width=5,tip_length=.16,max_tip_length_to_length_ratio=.45))
    g.add(T('first spike · 25 ms',26,GREEN).move_to([xx(25),1.9,0]),T('40 ms · slower neuron type',26,GREEN).move_to([3.1,-.05,0]))
    br=span(xx(0),xx(25),-.05); g.add(br,T('latency to first spike',26,YELLOW).move_to([-3.3,-.5,0]))
    g.br=br
    return g

class S15Spike(SyncedScene):
    def construct(self):
        v=latency_view(); self.add(heading('Earliest first spikes · about 25–40 ms'),v,note('Dissociated mouse olfactory neurons · Ghatpande & Reisert 2011 · ms'))
        self.at('the earliest first spikes'); self.play(Indicate(v.br,color=YELLOW,scale_factor=1.05),run_time=.7)
        self.at('a strong odor pulse'); self.play(Indicate(v[11],color=YELLOW,scale_factor=1.02),run_time=.5); self.finish()

class S16Label(SyncedScene):
    def construct(self):
        v=latency_view(); self.add(heading('Latency to a spike'),v,note('Dissociated mouse olfactory neurons · Ghatpande & Reisert 2011 · ms'))
        self.at('which includes more'); self.play(FadeOut(v),run_time=.3)
        # Ordered compartments deliberately use equal widths: no allocation of measured time.
        seg=VGroup(*[bchip(s,YELLOW,28) for s in ('solution\nexchange','membrane\ncharging','spike\ninitiation')]).arrange(RIGHT,buff=.08).move_to([0,.3,0])
        bracket=span(seg.get_left()[0],seg.get_right()[0],1.5)
        self.add(bracket,T('latency to a spike',32,YELLOW).move_to([0,2.2,0]),seg,T('0 · pulse onset',26,LIGHT).move_to([-4.3,1.95,0]),T('first spike',26,GREEN).move_to([4.5,1.95,0]))
        self.add(T('Ordered contributions, not to scale',28,LIGHT).move_to([0,-1.2,0]))
        self.at('It is not a'); self.add(T('Spike latency ≠ channel time constant',32,TEXT).move_to([0,-2.2,0])); self.finish()

def baseline_view():
    rows=VGroup()
    for y,label,places in ((1,'A · quiet',(-.5,)),(-1.5,'B · noisy',(-4.8,-3.7,-2.6,-1.5,-.3,.9,2,3.1,4.4,5.4))):
        base=Line([-5.5,y,0],[5.5,y,0],color=GREY)
        marks=VGroup(*[Line([x,y,0],[x,y+.65,0],color=GREEN,stroke_width=4) for x in places])
        rows.add(VGroup(base,marks,T('Neuron with receptor '+label,30,BLUE).move_to([0,y+1.05,0])))
    return rows

class S17Noise(SyncedScene):
    def construct(self):
        rows=baseline_view(); self.add(heading('Spontaneous activity · no odour'),note('Reisert 2010 · schematic event rasters, not recordings'))
        self.add(rows[0][2],rows[1][2])
        self.at('Spontaneous receptor activity'); self.play(Create(rows[0][0]),Create(rows[1][0]),run_time=.6)
        self.play(LaggedStart(*[Create(m) for m in rows[1][1]],lag_ratio=.3),Create(rows[0][1]),run_time=3,rate_func=linear)
        self.at('enter the cascade'); self.play(Indicate(rows[0][1],color=GREEN),run_time=.5)
        self.at('different levels of'); self.play(Indicate(rows[1][1],color=GREEN),run_time=.7); self.finish()

class S18Inverse(SyncedScene):
    def construct(self):
        rows=baseline_view(); self.add(rows,heading('Spontaneous activity · no odour initially'),note('Reisert 2010 · schematic event rasters, not recordings'))
        ligand=bchip('inverse-agonist odorant',YELLOW,28).move_to([2.5,-2.55,0])
        self.at('Inverse agonist odorants'); self.play(FadeIn(ligand),run_time=.2); self.play(ligand.animate.move_to([-3,-2.4,0]),run_time=.35)
        contact=arrow(ligand.get_top(),[-3,-1.5,0],YELLOW); self.add(contact)
        self.at('could quiet it'); marks=rows[1][1]; self.play(LaggedStart(*[FadeOut(m) for m in marks],lag_ratio=.03),run_time=.4)
        rows[1].remove(marks)
        old=rows[1][-1]; replacement=T('Neuron with receptor B · quieted',30,BLUE).move_to(old); rows[1].remove(old); self.remove(old); rows[1].add(replacement); self.add(replacement)
        # Quiet result stays visible while a compact two-row equivalence is built below.
        self.play(FadeOut(rows[0]),rows[1].animate.shift(UP*2.1),FadeOut(ligand),FadeOut(contact),run_time=.3)
        self.at('A cascade that multiplies')
        pairs=VGroup()
        for y,txt in ((-1.1,'receptor event'),(-2.35,'spontaneous event')):
            inp=bchip(txt,BLUE,28).move_to([-3.8,y,0]); out=bchip('amplified output',PURPLE,28).move_to([3.6,y,0]); a=arrow(inp.get_right(),out.get_left())
            pairs.add(VGroup(inp,out,a,T('×N',28,PURPLE).move_to([0,y+.4,0])))
        self.play(FadeIn(pairs[0]),run_time=.4)
        self.at('multiplies a spontaneous'); self.play(FadeIn(pairs[1]),run_time=.4); self.finish()

class S19Take(SyncedScene):
    def construct(self):
        self.add(heading('What sits between stimulus and pore?'))
        core=bchip('enzyme cascade',PURPLE,36).move_to([0,1.7,0]); self.add(core)
        for cue,txt,x,c in (('can buy gain','GAIN',-4,PURPLE),('They often pay','TIME',0,YELLOW),('they can amplify','SPONTANEOUS\nACTIVITY',4,GREEN)):
            target=T(txt,32,c).move_to([x,-.8,0]); self.at(cue)
            self.add(target); self.play(GrowArrow(arrow(core.get_bottom(),target.get_top(),c)),run_time=.3)
        self.add(T('Timing and signal-to-noise depend on kinetics, feedback,',26,LIGHT).move_to([0,-2.5,0]),T('filtering and where noise enters.',26,LIGHT).move_to([0,-3,0])); self.finish()

class S20End(EndCard):
    LINE='Enzymes can buy gain, often paying in time and amplified noise.'
    def construct(self):
        self.add(T('Enzymes between stimulus and pore',32,PURPLE).move_to([0,2,0]))
        self.play(FadeIn(T('can buy gain,\noften paying in time\nand amplified noise.',40,font=TITLE_FONT,line_spacing=1.2)),run_time=.6)
        self.add(T('biochemistrypedia.com',26,TEAL).move_to([0,-2.8,0])); self.finish()
