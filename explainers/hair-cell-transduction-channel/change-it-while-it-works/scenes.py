"""Change It While It Works — schematic cartoons, never molecular structures.
COLOR MAP: BLUE TMC1/candidate; TEAL partners; PURPLE delivery/anchors;
YELLOW calcium/current; TEXT other ions/actions; ORANGE reagent; PINK changed
residue; GREEN evidence; RED limitations; GREY membrane; GOLD title rule.
Every trace is I=N*i*P_open, with an ideal rectangular stimulus. Illustrative
amplitudes and qualitative ion icons are not measurements or permeability ratios.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
PINK = '#F2789F'


def title(s, color=TEXT):
    return T(s, 32, color).move_to([0, 3.2, 0])


def note(s, color=GREY, y=-3.15):
    return T(s, 27, color).move_to([0, y, 0])


def counters():
    out = VGroup()
    for x, symbol, label, color in [(-4.15,'N','channel\ncount',TEXT),
            (0,'i','one open\nchannel',BLUE),(4.15,'P_open','open\nprobability',TEXT)]:
        box = RoundedRectangle(width=3.65,height=3.25,corner_radius=.2,
            color=color,fill_color=color,fill_opacity=.09).move_to([x,-.25,0])
        sym = T(symbol, 66 if symbol != 'P_open' else 45,color).move_to([x,.35,0])
        lab = T(label,28,GREY,line_spacing=1).move_to([x,-1.1,0])
        out.add(VGroup(box,sym,lab))
    return out


def exclusion(m, label='removed'):
    # Cross BESIDE the label, never over its letters.
    x=m.get_right()[0]+.43; y=m.get_center()[1]
    return VGroup(Line([x-.15,y-.15,0],[x+.15,y+.15,0],color=RED,stroke_width=4),
        Line([x-.15,y+.15,0],[x+.15,y-.15,0],color=RED,stroke_width=4),
        T(label,26,RED).next_to(m,DOWN,buff=.28))


def model_line(N=100,x=-5,y=1.15,w=10.5,h=2.7):
    ts=np.array([0,.15,.15,.85,.85,1.])
    ps=np.array([0,0,.2,.2,0,0])
    current=N*(-15)*ps
    return VMobject(color=YELLOW,stroke_width=5).set_points_as_corners(
        [[x+t*w,y+v/300*h,0] for t,v in zip(ts,current)])


def plot(N=100,x=-5,y=1.15,w=10.5,h=2.7,labels=True):
    axes=VGroup(Line([x,y+.35,0],[x,y-h-.3,0],color=GREY),
                Line([x,y-h-.3,0],[x+w,y-h-.3,0],color=GREY))
    ticks=VGroup(T('0',26,GREY).move_to([x-.35,y,0]),
        T('time →',26,GREY).move_to([x+w-.7,y-h-.65,0]))
    lab=T('inward current ↓  •  illustrative',26,GREY).move_to([x+w/2,y+.85,0])
    return VGroup(axes,ticks,lab,model_line(N,x,y,w,h))


def channel(cys=False):
    membrane=Rectangle(width=12.4,height=1.05,color=GREY,fill_color=GREY,fill_opacity=.22)
    water=Rectangle(width=1.25,height=4.5,stroke_width=0,fill_color=BLUE,fill_opacity=.17)
    blocks=VGroup(*[RoundedRectangle(width=1.12,height=4.35,corner_radius=.15,
        color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([x,0,0]) for x in [-1.18,1.18]])
    lab=T('TMC1',30,BLUE).move_to([-3.7,-1.7,0])
    leader=Line([-2.85,-1.7,0],[-1.8,-1.4,0],color=BLUE)
    ml=T('cell membrane',26,GREY).move_to([4.25,0,0])
    g=VGroup(membrane,water,blocks,lab,leader,ml)
    if cys:
        g.add(chip('C',PINK,32,pad=.13).move_to([0,.8,0]))
    return g


def ion_stream(y=2.2,mixed=False):
    return VGroup(*[Dot([x,y+.26*(j%2),0],radius=.13,
        color=(TEXT if mixed and j%2 else YELLOW)) for j,x in enumerate([-.28,0,.28])])


def ion_key():
    return VGroup(Dot([-5.65,-2.45,0],radius=.12,color=YELLOW),
        T('Ca2+',24,YELLOW).move_to([-5.0,-2.45,0]),
        Dot([-3.95,-2.45,0],radius=.12,color=TEXT),
        T('other ion',24,TEXT).move_to([-2.95,-2.45,0]))


def chain(y=0, selected=5):
    boxes=VGroup(*[RoundedRectangle(width=.72,height=1.1,corner_radius=.1,
        color=BLUE,fill_color=BLUE,fill_opacity=.28).move_to([-4.8+j*.96,y,0]) for j in range(11)])
    boxes[selected].set_color(PINK).set_fill(PINK,.35)
    return boxes


def prediction1():
    return VGroup(title('Predict',TEAL),
        T('If TMC1 only delivered or anchored the channel,\nwhich counter would a point mutation change?',28,
            line_spacing=1).move_to([0,2.05,0]),counters(),
        VGroup(*[chip(s,TEAL,42,pad=.25).move_to([x,-2.8,0])
            for x,s in zip([-4.15,0,4.15],['N','i','P_open'])]))


def prediction2(question=True):
    p=plot();p[2].move_to([-2.3,2.55,0])
    marker=DashedLine([1.3,1.65,0],[1.3,-1.95,0],color=ORANGE)
    reagent=chip('reagent arrives',ORANGE,28).move_to([2.1,2.25,0])
    q=note('What does a change now rule out?',TEXT)
    return VGroup(title('Predict',TEAL),p,marker,reagent,q)


def vesicles():
    out=VGroup()
    for x,lab in [(-3.2,'turtle\nTMC1'),(3.2,'budgerigar\nTMC2')]:
        ring=Circle(radius=2.15,color=GREY,stroke_width=7).move_to([x,-.15,0])
        box=chip(lab,BLUE,30).move_to([x,-2.15,0])
        box[0].set_fill(BG,1)
        label=T('liposome',28,GREY).move_to([x,1.0,0])
        out.add(VGroup(ring,box,label))
    return out


class S00Title(TitleCard):
    LESSON="The Hair Cell's Transduction Channel"
    TITLE='Change It While It Works'


class S01Q(SpokenScene):
    def construct(self):
        c=counters(); self.add(title('Change It While It Works'),c)
        deletion=chip('delete a protein',RED,30).move_to([-1,-2.65,0])
        self.at('deleting a protein');self.play(FadeIn(deletion),run_time=.3)
        self.at('cannot reveal');self.play(FadeIn(exclusion(deletion,'cannot identify the pore')),run_time=.35)
        self.at('what experiment can');self.play(Indicate(c[1],color=PINK),Transform(c[1][1],T('?',138,PINK).move_to([0,.25,0])),run_time=.5)
        self.finish()


class S02Kaw(SpokenScene):
    def construct(self):
        genes=VGroup(*[VGroup(RoundedRectangle(width=4.4,height=3.3,corner_radius=.2,color=BLUE,
            fill_color=BLUE,fill_opacity=.12),T(s,56,BLUE)) for s in ['Tmc1','Tmc2']]).arrange(RIGHT,buff=1.4).move_to([-.2,.15,0])
        self.add(title('Kawashima and colleagues • 2011'),genes,note('neonatal mouse hair cells'))
        self.at('removed both');self.play(*[FadeIn(exclusion(g,'knocked out')) for g in genes],run_time=.5)
        self.finish()


class S03Flat(SpokenScene):
    def construct(self):
        self.add(title('Double null and rescue'),note('Illustrative • I = N × i × P_open',GREY))
        axes=VGroup(Line([-2.8,2.3,0],[-2.8,-2.55,0],color=GREY),Line([-2.8,-2.55,0],[5.7,-2.55,0],color=GREY),
            T('inward current',26,GREY).rotate(PI/2).move_to([-6.15,-.15,0]),T('time →',26,GREY).move_to([5,-2.85,0]))
        self.add(axes)
        flat=model_line(0,-2.7,1.65,8.2,.8)
        self.add(flat,T('double null',28,GREY).move_to([-4.65,1.7,0]),
            T('0',26,GREY).move_to([-3.1,1.65,0]),
            T('no conventional current',27,TEXT).move_to([1.4,2.3,0]))
        stim=Line([-1.47,2.75,0],[4.27,2.75,0],color=TEAL,stroke_width=8)
        self.add(stim,T('bundle push',26,TEAL).move_to([-4.6,2.65,0]))
        self.at('Putting back either');self.play(Create(model_line(100,-2.7,.05,8.2,.85)),
            FadeIn(T('+ TMC1',28,BLUE).move_to([-4.65,0,0])),
            FadeIn(T('0',26,GREY).move_to([-3.1,.05,0])),run_time=.4)
        self.at('gene restored it');self.play(Create(model_line(65,-2.7,-1.55,8.2,.85)),
            FadeIn(T('+ TMC2',28,BLUE).move_to([-4.65,-1.6,0])),
            FadeIn(T('0',26,GREY).move_to([-3.1,-1.55,0])),run_time=.4)
        self.wait(2.0);self.finish()


class S04Product(SpokenScene):
    def construct(self):
        c=counters();heading=title('Requirement and rescue = the product')
        self.add(c,heading,note('TMC proteins are in the pathway',GREEN))
        self.at('whole product');self.play(*[g[0].animate.set_stroke(YELLOW,5).set_fill(YELLOW,.2) for g in c],run_time=.45)
        self.at('cannot separate');self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        self.add(title('Pore or helper?  Same lost current.'))
        for x,lab,col,cue in [(-3.2,'pore',BLUE,'a pore'),(3.2,'helper',TEAL,'from its helpers')]:
            card=chip(lab,col,40).move_to([x,1.7,0])
            self.at(cue);self.play(FadeIn(card),FadeIn(exclusion(card)),
                FadeIn(plot(0,x=x-2.3,y=-.5,w=4.6,h=1.4)),run_time=.3)
        self.add(note('Requirement and rescue do not separate them',RED));self.wait(2.0);self.finish()


class S05Sharper(SpokenScene):
    def construct(self):
        c=chain();c.stretch(2,1);self.add(title('Change one residue; keep the channel working'),c,
            T('TMC1 • schematic residue blocks',30,BLUE).move_to([0,-2.4,0]))
        self.at('keeps the channel');self.play(Indicate(c,color=BLUE,scale_factor=1.04),run_time=.45)
        self.at('changes one amino');self.play(c[5].animate.stretch(1.7,1).set_fill(PINK,.65),
            FadeIn(note('one amino acid',PINK)),run_time=.5);self.finish()


class S06Bth(SpokenScene):
    def construct(self):
        c=chain();c.stretch(2,1);c[5].stretch(1.5,1)
        for j in range(11):
            if j != 5:c[j].shift(LEFT*.8 if j<5 else RIGHT*.8)
        self.add(title('Beethoven allele • mouse protein'),c,T('TMC1',30,BLUE).move_to([0,-2.4,0]))
        badge=chip('M412',PINK,58,pad=.4).move_to([0,-.05,0])
        self.at('Methionine');self.play(Transform(c[5],badge),run_time=.3)
        self.at('becomes lysine');self.play(Transform(c[5],chip('K',PINK,64,pad=.45).move_to(badge)),
            FadeIn(note('M412K • methionine → lysine',PINK)),run_time=.5);self.finish()


class S07Setup(SpokenScene):
    def construct(self):
        self.add(title('Pan and colleagues • 2013'),note('neonatal mouse inner hair cells'))
        genes=chip('Tmc2',BLUE,38).move_to([-.3,2.15,0]);self.add(genes)
        channels=VGroup()
        for x in [-4,0,4]:
            blocks=VGroup(*[RoundedRectangle(width=.65,height=2.7,corner_radius=.12,color=BLUE,fill_color=BLUE,fill_opacity=.3).move_to([x+dx,-.25,0]) for dx in [-.65,.65]])
            channels.add(VGroup(blocks,T('TMC1',30,BLUE).move_to([x,-2,0])))
        self.add(channels)
        self.at('lacking');self.play(FadeIn(exclusion(genes)),run_time=.35)
        self.at('every channel');self.play(*[Indicate(m[0],color=BLUE,scale_factor=1.06) for m in channels],
            FadeIn(T('every channel uses TMC1',29,BLUE).move_to([0,-2.6,0])),run_time=.5);self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        g=prediction1();self.add(g[0],g[2])
        self.at('If');self.play(FadeIn(g[1]),run_time=.3)
        self.at('what would');self.play(FadeIn(g[3]),run_time=.3);self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction1());self.wait(5)


class S10Reveal1(SpokenScene):
    def construct(self):
        c=counters();self.add(c,title('Otherwise normal channels'))
        caption=note('delivery of normal channels',PURPLE);self.add(caption)
        arrow=T('↓',54,PURPLE).move_to([-4.15,-2.5,0])
        self.at('fewer channels');self.play(c[0][0].animate.set_stroke(PURPLE,5),FadeIn(arrow),
            Transform(caption,note('delivery: fewer channels',PURPLE)),run_time=.35)
        self.at('A coupling defect');self.play(c[0][0].animate.set_stroke(TEXT,2.5),FadeOut(arrow),
            Transform(caption,note('coupling of normal channels',PURPLE)),run_time=.3)
        self.at('fewer open');self.play(c[2][0].animate.set_stroke(PURPLE,5),
            FadeIn(T('↓',54,PURPLE).move_to([4.15,-2.5,0])),Transform(caption,note('coupling: fewer open',PURPLE)),run_time=.35)
        self.at('Each open channel');self.play(c[1][0].animate.set_fill(BLUE,.3).set_stroke(BLUE,5),
            FadeIn(T('i unchanged',30,BLUE).move_to([0,2.1,0])),run_time=.4);self.finish()


class S11Reveal2(SpokenScene):
    def construct(self):
        self.add(title('Calcium permeability • qualitative Ca2+ counts'))
        ions=VGroup()
        for x,lab,col,count in [(-3.2,'one wild-type Tmc1 allele',BLUE,3),
                                 (3.2,'Beethoven Tmc1',PINK,1)]:
            self.add(T(lab,28,col).move_to([x,2.5,0]),
                VGroup(*[RoundedRectangle(width=.9,height=4.65,corner_radius=.13,
                    color=col,fill_color=col,fill_opacity=.3).move_to([x+dx,-.1,0])
                    for dx in [-.95,.95]]))
            ions.add(VGroup(*[Dot([x+(j-(count-1)/2)*.32,1.65,0],radius=.14,
                color=YELLOW) for j in range(count)]))
        self.add(ions)
        self.at('less calcium');self.play(ions.animate.shift(DOWN*3.25),
            FadeIn(T('normal',30,YELLOW).move_to([-3.2,-2.65,0])),
            FadeIn(T('reduced',30,YELLOW).move_to([3.2,-2.65,0])),run_time=.65)
        self.at('has been replicated');self.play(FadeIn(note('Calcium result replicated',GREEN,y=-3.1)),run_time=.3)
        self.at('disputed');self.play(FadeIn(note('single-channel current: disputed',GREY,y=-3.6)),run_time=.3)
        self.wait(2.2);self.finish()


class S12Meaning(SpokenScene):
    def construct(self):
        self.add(channel(),ion_key(),title('One residue in TMC1'),T('open',28,BLUE).move_to([0,-2.65,0]))
        ions=ion_stream(mixed=True);self.add(ions)
        self.at('which ions pass');self.play(ions.animate.shift(DOWN*4.3),
            FadeIn(chip('selectivity',GREEN,30).move_to([3.7,1.7,0])),
            FadeIn(T('a residue changed\nwhich ions pass',28,GREEN).move_to([-4,1.6,0])),run_time=.7)
        self.at('A deletion');self.play(FadeIn(note('A deletion cannot show this',RED)),run_time=.3);self.finish()


class S13Limit(SpokenScene):
    def construct(self):
        self.add(channel(),ion_key(),title('A partner can also change passage'))
        ions=ion_stream(mixed=True);self.add(ions)
        p=chip('partner',TEAL,34).move_to([5,1.55,0])
        self.at('a partner');self.play(FadeIn(p),run_time=.2);self.play(p.animate.move_to([3.1,1.55,0]),run_time=.5)
        self.at('change what passes')
        self.play(ions[0].animate.set_color(TEXT),ions[2].animate.set_color(TEXT),
            Indicate(p,color=TEAL),run_time=.25)
        self.play(ions.animate.shift(DOWN*4.2),run_time=.6)
        self.at('narrows the candidates');self.play(FadeIn(note('narrows the candidates • strong, not conclusive',RED)),run_time=.35);self.finish()


class S14Acute(SpokenScene):
    def construct(self):
        self.add(title('Pan and colleagues • 2018'))
        chains=VGroup(*[chain(y=y,selected=k) for y,k in [(1.65,2),(0,5),(-1.65,8)]])
        self.add(chains,T('TMC1 constructs',28,BLUE).move_to([0,-2.65,0]))
        self.at('change the channel');self.play(LaggedStart(*[Indicate(c,color=BLUE,scale_factor=1.02) for c in chains],lag_ratio=.1),run_time=.5)
        self.at('single cysteine substitutions');self.play(*[Transform(c[k],chip('C',PINK,34,pad=.22).move_to(c[k])) for c,k in zip(chains,[2,5,8])],
            FadeIn(note('one cysteine substitution per construct',PINK)),run_time=.65);self.finish()


class S15Deliver(SpokenScene):
    def construct(self):
        self.add(title('Deliver into a double-null hair cell'))
        cell=RoundedRectangle(width=11.4,height=5.5,corner_radius=.7,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([0,-.1,0])
        self.add(cell,T('hair cell • both genes absent',28,GREY).move_to([.4,2.2,0]))
        virus=VGroup(Circle(radius=1.2,color=TEXT),chip('TMC1 • C',PINK,24,pad=.08)).move_to([0,.6,0])
        label=T('virus carrying\nTMC1 with C',27,BLUE).move_to([0,-1.3,0]);self.add(virus,label)
        self.at('Delivered into');self.play(virus.animate.move_to([0,.3,0]),run_time=.6)
        self.at('restored a current');self.play(virus.animate.move_to([-3.4,.6,0]),
            label.animate.move_to([-3.4,-1.3,0]),Create(plot(100,x=-.7,y=.6,w=5.9,h=2.1)),run_time=.65);self.wait(2.2);self.finish()


class S16Reagent(SpokenScene):
    def construct(self):
        ch=channel(cys=True);self.add(ch,title('outside (water)'),T('inside the cell',28,GREY).move_to([0,-2.65,0]))
        reagent_note=note('membrane-impermeant',ORANGE)
        cloud=VGroup(*[Dot([-4.8+(j%4)*.45,2.1+(j//4)*.35,0],radius=.1,color=ORANGE) for j in range(8)])
        self.at('added a reagent');self.play(FadeIn(cloud),FadeIn(T('reagent',28,ORANGE).move_to([-4.1,2.8,0])),run_time=.3)
        self.at('cannot cross');self.play(cloud.animate.shift(DOWN*1.32),FadeIn(reagent_note),run_time=.55)
        self.at('reacts with cysteine');self.play(Transform(reagent_note,note('membrane-impermeant • reacts with cysteine in water',ORANGE)),Indicate(ch[-1],color=PINK),run_time=.45);self.finish()


class S17Predict(SpokenScene):
    def construct(self):
        g=prediction2();self.add(g[0],g[1])
        self.at('already flowing');self.play(Indicate(g[1][-1],color=YELLOW,scale_factor=1),run_time=.4)
        self.at('reagent arrives');g[3].shift(RIGHT*2.5);self.play(g[3].animate.shift(LEFT*2.5),Create(g[2]),run_time=.45)
        self.at('what does');self.play(FadeIn(g[4]),run_time=.3);self.finish()


class S18Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction2());self.wait(5)


class S19Reveal(SpokenScene):
    def construct(self):
        g=prediction2();self.add(g[1],g[2],g[3],title('Current existed first'))
        a=chip('altered synthesis',PURPLE,28).move_to([-3.6,-2.8,0]);b=chip('altered delivery',PURPLE,28).move_to([2.6,-2.8,0])
        self.at('altered synthesis');self.play(FadeIn(a),FadeIn(exclusion(a,'ruled out')),run_time=.3)
        self.at('or delivery');self.play(FadeIn(b),FadeIn(exclusion(b,'ruled out')),run_time=.3)
        self.at('current existed');self.play(Create(Line([-3.42,1.65,0],[1.3,1.65,0],color=GREEN)),
            FadeIn(T('current existed first',27,GREEN).move_to([-2.1,1.98,0])),run_time=.4);self.finish()


class S20Water(SpokenScene):
    def construct(self):
        ch=channel(cys=True);self.add(ch,ion_key(),title('Access from outside (water)'))
        before=ion_stream(y=1.05,mixed=True).shift(LEFT*4)
        self.add(before,T('before: mixed ions',27,TEXT).move_to([-4,1.85,0]))
        r=Dot([-.4,2.6,0],radius=.19,color=ORANGE);self.add(r)
        self.at('reached from outside');self.play(r.animate.scale(.4).move_to([.23,.8,0]),run_time=.55)
        after=ion_stream(y=1.05,mixed=True).shift(RIGHT*4)
        for ion in after:ion.set_color(TEXT)
        self.at('alters which ions');self.play(ch[-1][0].animate.set_fill(ORANGE,.6),
            FadeIn(after),FadeIn(T('after: other ions pass',27,GREEN).move_to([4,1.85,0])),run_time=.5)
        path=Arrow([0,2.65,0],[0,1.05,0],buff=0,color=BLUE,stroke_width=10,
            max_tip_length_to_length_ratio=.18)
        self.at('water filled route');self.play(ch[1].animate.set_fill(BLUE,.5),
            FadeIn(T('water-filled route',29,BLUE).move_to([3.8,-1.55,0])),
            GrowArrow(path),Create(Line([2,-1.4,0],[.45,1.6,0],color=BLUE,stroke_width=3)),run_time=.4)
        self.at('a pore would provide');self.play(FadeIn(note('as a pore would provide',GREEN)),run_time=.3);self.finish()


class S21Limit(SpokenScene):
    def construct(self):
        self.add(channel(cys=True),title('In the hair cell'),chip('native partners',TEAL,30).move_to([3.9,1.65,0]))
        self.at('reachable residue');self.play(FadeIn(T('lining the pore\nor beside it?',28,RED).move_to([-4,1.55,0])),run_time=.35)
        self.at('No purified');self.play(FadeIn(note('No purified mammalian TMC1 tested alone',RED)),run_time=.35);self.finish()


class S22Lipo(SpokenScene):
    def construct(self):
        v=vesicles();self.add(title('Jia and colleagues • 2020; truncated constructs'),v[0][0],v[0][2],v[1][0],v[1][2])
        self.at('truncated');self.play(FadeIn(v[0][1]),run_time=.3)
        self.at('and');self.play(FadeIn(v[1][1]),run_time=.3)
        self.at('responded to pressure');self.play(*[GrowArrow(Arrow([x,2.7,0],[x,2.03,0],buff=0,color=TEXT)) for x in [-3.2,3.2]],
            FadeIn(T('pressure',27,TEXT).move_to([0,2.4,0])),run_time=.3)
        dots=VGroup(*[Dot([x,-.6,0],radius=.14,color=YELLOW) for x in [-3.4,-3,-.0+3,3.4]])
        self.play(FadeIn(dots),run_time=.15);self.play(dots.animate.shift(DOWN*.9),FadeIn(T('channel\nactivity',28,YELLOW).move_to([0,.1,0])),run_time=.5);self.wait(2.2);self.finish()


class S23Lipolimit(SpokenScene):
    def construct(self):
        v=vesicles().scale(.8).shift(UP*.65);self.add(v)
        self.at('supports');self.play(FadeIn(title('Force-gated activity in a reduced system',GREEN)),run_time=.35)
        a=T('non-mammalian proteins',30,RED).move_to([0,-2.4,0])
        self.at('not mammalian');self.play(FadeIn(a),run_time=.3)
        self.at('not a native complex');self.play(FadeIn(T('not a native complex',30,RED).move_to([0,-3.05,0])),run_time=.3);self.finish()


class S24Take(SpokenScene):
    def construct(self):
        self.add(title('Each rung ruled out a different alternative'))
        rails=VGroup(*[Line([x,-3.25,0],[x,2.65,0],color=GREY,stroke_width=4) for x in [-6,6]])
        self.add(rails)
        labels=[('Loss + rescue','Needed; pore vs helper\nnot separated'),
            ('Mutation','Not only normal-channel delivery'),
            ('Acute change','Not altered synthesis or delivery'),
            ('Purified proteins','Works without the hair cell\n(reduced system)')]
        rungs=VGroup(*[VGroup(Line([-6,y-.55,0],[6,y-.55,0],color=GREY),
            T(a,28,BLUE).move_to([-5.65,y,0],aligned_edge=LEFT),
            T(b,26,GREEN).move_to([-1.4,y,0],aligned_edge=LEFT))
            for (a,b),y in zip(labels,[-2.65,-1.05,.55,2.15])])
        self.at('Each rung');self.play(LaggedStart(*[FadeIn(r,shift=UP*.1) for r in rungs],lag_ratio=.5),run_time=1.8)
        self.at('None alone');self.play(Indicate(rails,color=RED,scale_factor=1),run_time=.4);self.finish()


class S25End(EndCard):
    LINE='None alone proves the pore.'
