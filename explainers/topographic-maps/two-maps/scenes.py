"""Two Maps from One Retina — reviewed diagram redraw.
COLOR MAP: BLUE usual retinal axons/EphA; PURPLE extra-EphA knock-in;
ORANGE ephrin-A; YELLOW comparison/activity and extra-patch emphasis; RED failed prediction;
GREEN evidence; GREY anatomy. Empirical maps/zones are labelled schematic.
Toy model: L(x)=dose*(1+2*x), R*L=3; fixed endpoints clipped to target.
Pure rank: u=(3-R)/2; equal knock-in/unchanged populations take half each.
All toy endpoints and connecting traces are computed from these equations.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
config.background_color = BG


def label(s,x=0,y=0,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def heading(s): return label(s,0,3.35,32)


def bar(x,y,h,w=.6,color=GREY,opacity=.12):
    return RoundedRectangle(corner_radius=.09,width=w,height=h,stroke_color=color,
                            stroke_width=2,fill_color=color,fill_opacity=opacity).move_to([x,y,0])


def cell(x,y,op=1,color=BLUE,r=.15):
    return Circle(radius=r,stroke_color=color,stroke_width=2.5,
                  fill_color=color,fill_opacity=op).move_to([x,y,0])


def axline(a,b,color=BLUE,w=3,op=1):
    return Line(a,b,color=color,stroke_width=w,stroke_opacity=op)


def fixed(r,dose=1): return np.clip((3/(dose*np.asarray(r))-1)/2,0,1)
def rank(r): return (3-np.asarray(r))/2


def ribbon(y=0,dose=1,h=4.6,w=10.8):
    # Opacity is proportional to the actual concentration, with no second fill
    # obscuring the halving. Outline of the original dose is kept separately.
    g=VGroup()
    for i in range(64):
        u=(i+.5)/64
        g.add(Rectangle(width=w/64+.008,height=h,stroke_width=0,
                        fill_color=interpolate_color(ManimColor(BG),ManimColor(ORANGE),dose*(1+2*u)*.28),fill_opacity=1)
              .move_to([-w/2+w*u,y,0]))
    g.add(Rectangle(width=w,height=h,stroke_color=ORANGE,stroke_width=2,fill_opacity=0).move_to([0,y,0]))
    return g


def slope_frame(dose=1):
    return VGroup(heading('Does ligand amount matter?'),ribbon(-.1,dose),
                  label('front · low',-4.1,-2.8,28,ORANGE),
                  label('back · high',4.1,-2.8,28,ORANGE),
                  label('ephrin-A: low to high',0,2.65,28,ORANGE))


def mosaic(extra=False):
    pts=[(-2.65,1.15),(-1.65,1.48),(-.38,1.03),(.85,1.42),(2.35,.9),
         (-2.9,-.15),(-1.28,.15),(.10,-.12),(1.55,.02),(2.65,-.6),
         (-2.1,-1.31),(-.77,-1.5),(.7,-1.12),(1.83,-1.42)]
    knock={0,1,4,6,7,11,12}
    outline=Ellipse(width=7.5,height=4.8,stroke_color=GREY,fill_color=GREY,fill_opacity=.06)
    dots=VGroup(*[cell(x,y,.85 if i in knock else .22,PURPLE if i in knock else BLUE,.28)
                 for i,(x,y) in enumerate(pts)])
    bars=VGroup()
    for i,(x,y) in enumerate(pts):
        h=.32+(.55 if extra and i in knock else 0)
        bars.add(Rectangle(width=.13,height=h,stroke_width=0,
                          fill_color=PURPLE if i in knock else BLUE,fill_opacity=1)
                 .move_to([x+.43,y-.17+h/2,0]))
    return VGroup(outline,dots,bars)


ABS_Q='Where do both groups go?'
REL_Q='Where does each group go?'
LIG_Q='What does each reading predict now?'


def target_cell(x,y,col,answer=None):
    g=VGroup(bar(x,y,1.12,4.15,col,.045))
    if answer is None:
        g.add(label('?',x,y,32,col)); return g
    a,b=x-1.77,x+1.77
    g.add(axline([a,y,0],[b,y,0],GREY,7,.5))
    if answer=='crowd':
        us=fixed(np.linspace(7,5,5))
        for j,u in enumerate(us):g.add(cell(a+(b-a)*u,y+(j-2)*.21,color=col,r=.125))
    else:
        rs=np.linspace(3,1,5)
        us=fixed(rs) if answer=='normal' else (.5*rank(rs) if answer=='front' else .5+.5*rank(rs))
        for u in us:g.add(cell(a+(b-a)*u,y,color=col,r=.14))
    g.add(label('front',a,y-.72,26,GREY),label('back',b,y-.72,26,GREY))
    return g


def table(abs_done=False,rel_done=False,active=None,question=None,abs_first=False,rel_first=False):
    g=VGroup(heading('Toy predictions'),label('Axons',-4.85,2.42,28),
             label('Absolute',-.95,2.62,28),label('fixed threshold',-.95,2.12,26),
             label('Relative',3.65,2.62,28),label('pure rank',3.65,2.12,26),
             label('Knock-in',-4.8,1.0,28,PURPLE),label('5–7 units',-4.8,.45,26,PURPLE),
             label('Unchanged',-4.8,-1.03,28,BLUE),label('1–3 units',-4.8,-1.58,26,BLUE))
    g.add(target_cell(-.95,.9,PURPLE,'crowd' if abs_done or abs_first else None),
          target_cell(-.95,-1.15,BLUE,'normal' if abs_done else None),
          target_cell(3.65,.9,PURPLE,'front' if rel_done or rel_first else None),
          target_cell(3.65,-1.15,BLUE,'back' if rel_done else None))
    if active is not None:
        g.add(Rectangle(width=4.40,height=5.35,stroke_color=YELLOW,stroke_width=3)
              .move_to([-.95 if active==0 else 3.65,.28,0]))
    if question:g.add(label(question,0,-3.18,28,YELLOW))
    return g


def normal_panel(x,absolute=False,dose=1,mark=True,ligand_dose=None):
    if ligand_dose is None: ligand_dose=dose
    a,b=x-1.75,x+.65
    top,span=1.9,4.05
    g=VGroup(label('fixed threshold' if absolute else 'pure rank',x,2.83,29),
             bar(a,-.125,4.4,.32),bar(b,-.125,4.4,.48,ORANGE,.04))
    # Target ligand shading is retained even in the prediction reveal.
    for j in range(32):
        u=(j+.5)/32
        g.add(Rectangle(width=.44,height=span/32+.01,stroke_width=0,
                        fill_color=interpolate_color(ManimColor(BG),ManimColor(ORANGE),ligand_dose*(1+2*u)*.23),fill_opacity=1)
              .move_to([b,top-span*u,0]))
    traces=VGroup()
    for r in [3,2,1]:
        src=top-span*rank(r)
        u=fixed(r,dose) if absolute else rank(r)
        dst=top-span*u
        # Distinct horizontal offsets at the clamped back edge expose the pileup.
        tx=b+(.10*(2-r) if absolute and dose<1 and u==1 else 0)
        traces.add(cell(a,src,(r+1)/4,r=.15),
                   axline([a+.16,src,0],[tx-.12,dst,0],BLUE,3,(r+1)/4),
                   cell(tx,dst,(r+1)/4,r=.12),label(str(r),a-.45,src,26,BLUE))
    g.add(traces,label('retina',a,-2.72,26),label('target',b,-2.72,26),
          label('front',b+.83,2.12,26),label('back',b+.83,-2.22,26))
    if mark:
        mid=top-span*(fixed(2,dose) if absolute else rank(2))
        g.add(label('0.25' if absolute else '0.5',b+.83,mid,26,YELLOW))
    return g


def two_maps(ghosts=False,evidence=False):
    g=VGroup(heading('Two orderly maps · schematic'),
             label('temporal (most EphA)',-3.3,2.72,26),
             label('nasal (least EphA)',3.35,2.72,26))
    for sy,ty,col,base,name in [(2.05,.70,PURPLE,0,'knock-in'),(-.72,-2.05,BLUE,.5,'unchanged')]:
        g.add(label(name,-5.18,sy,26,col),label('retina',5.15,sy,26,GREY))
        # Each parallel bar shows the ENTIRE target, with its occupied half tinted.
        g.add(bar(0,ty,.44,9,ORANGE,.025),
              Rectangle(width=4.5,height=.40,stroke_width=0,fill_color=col,fill_opacity=.20)
              .move_to([-2.25 if base==0 else 2.25,ty,0]))
        for r in np.linspace(3,1,5):
            u=rank(r); sx=-3.6+7.2*u; tx=-4.5+9*(base+.5*u)
            # tiny inward display inset separates boundary dots across the two bars;
            # model coordinate remains exactly 0.5 for each population's boundary.
            g.add(cell(sx,sy,color=col,r=.12),
                  axline([sx,sy-.13,0],[tx,ty+.12,0],col,2.5),
                  cell(tx,ty,color=col,r=.115))
        bracket_y=ty-.42
        g.add(Line([-4.5+9*base,bracket_y,0],[9*base,bracket_y,0],color=col),
              label('front half' if base==0 else 'back half',-2.25 if base==0 else 2.25,ty-.78,26,col))
    if ghosts:
        g[43].set_opacity(0)
        g[44].move_to([5.65,-2.05,0])
        # Normal reference rings sit on their own rail, so no new ending hides one.
        for u in np.linspace(0,1,5):
            old=-4.5+9*u; new=-4.5+9*(.5+.5*u)
            g.add(DashedVMobject(Circle(radius=.17,color=BLUE,stroke_width=2.5),num_dashes=10)
                  .move_to([old,-3.05,0]))
            if u<1:
                g.add(Arrow([old,-2.86,0],[new,-2.25,0],buff=.05,color=BLUE,stroke_width=2,max_tip_length_to_length_ratio=.08))
        g.add(label('Hollow = normal; four moved back, nasal end stayed',0,-3.55,26,BLUE))
    else:g.add(label('front',-5.25,-2.05,26,GREY),label('back',5.2,-2.05,26,GREY))
    if evidence:
        # Keep the maps and reference positions, replacing only the top header.
        g[0].become(label('Absolute reading predicts: unchanged axons stay at hollow rings',0,3.38,26))
        g[23].become(label('✓ Fixed address in own receptor level: ruled out',0,-.08,27,GREEN))
    return g


def ligand_question(question=True):
    g=VGroup(normal_panel(-3.3,True,ligand_dose=.5),normal_panel(3.3,False,ligand_dose=.5),
             label('Half ephrin-A everywhere · toy predictions',0,3.52,28,ORANGE))
    if question:g.add(label(LIG_Q,0,-3.35,28,YELLOW))
    return g


def patches(extra=False,main=True,failed=False,dosage=False):
    g=VGroup(heading('Example: ephrin-A2 / ephrin-A5'),
             label('Double heterozygote · one working copy each',0,2.72,26),
             label('label from a small patch of temporal retina',0,2.12,26,BLUE),
             ribbon(-.10,.5,h=3.65),
             label('front · low ephrin-A',-3.9,-2.25,26,ORANGE),
             label('back · high ephrin-A',3.9,-2.25,26,ORANGE))
    outline=DashedVMobject(Circle(radius=.66,color=GREY,stroke_width=3),num_dashes=18).move_to([-2.8,-.1,0])
    g.add(outline,label('wild-type position',-2.8,-1.55,26,GREY))
    if main:g.add(cell(-2.8,-.1,.8,BLUE,.48),label('normal main zone',-2.8,1.15,27,BLUE))
    if extra:
        g.add(cell(2.35,-.1,.9,YELLOW,.35),label('extra patch, some animals',2.25,1.15,26,YELLOW))
    if failed:
        g.add(label('× Pure rank predicts: one zone, no patch',0,-2.93,28,RED))
    if dosage:g.add(label('Ligand dosage affects mapping accuracy',0,-3.5,27,ORANGE))
    return g


class S00Title(TitleCard):
    LESSON="Topographic Maps: Sperry's Eye and Eph Gradients"
    TITLE='Two Maps from One Retina'


class S01Question(SpokenScene):
    def construct(self):
        left=VGroup(label('address',-3.25,2.5,36,BLUE),cell(-3.25,.7,color=BLUE,r=.48),
                    bar(-3.25,-1.6,.65,4.8,BLUE),label('own EphA level: 2',-3.25,-.25,28,BLUE),
                    label('one level → one place?',-3.25,-2.65,28))
        left.add(Arrow([-3.25,-.6,0],[-3.25,-1.3,0],color=BLUE,buff=.03))
        right=VGroup(label('rank',3.25,2.5,36,YELLOW),label('compare with neighbours',3.25,-2.65,28))
        for i,r in enumerate([3,2,1]):
            x=1.5+i*1.7
            right.add(cell(x,.7,color=BLUE,r=.20+.09*r),label(str(r),x,-.2,30,YELLOW),
                      Rectangle(width=.35,height=.35*r,fill_color=BLUE,fill_opacity=.6,stroke_width=0).move_to([x,-1.45,0]))
        self.add(heading('What does an axon read?'),left,right)
        self.at('an address');self.play(Indicate(left[1],color=BLUE),run_time=.5)
        self.at('its rank');self.play(Indicate(right,color=YELLOW,scale_factor=1.03),run_time=.6)
        self.finish()


class S02Same(SpokenScene):
    def construct(self):
        a,b=normal_panel(-3.3,True),normal_panel(3.3,False)
        self.add(a,b)
        self.at('same order');self.play(FadeIn(label('Same order; different spacing',0,-3.35,28,GREEN)),run_time=.4)
        self.at('change some axons');self.play(Indicate(a[-7],color=PURPLE),Indicate(b[-7],color=PURPLE),run_time=.6)
        self.finish()


class S03Brown(SpokenScene):
    def construct(self):
        mouse=VGroup(Ellipse(width=7.6,height=4.0,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([-1,-.1,0]),
                     Circle(radius=1.35,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([2.3,.5,0]),
                     Circle(radius=.65,color=GREY).move_to([2.15,1.8,0]),Dot([3.1,.8,0],color=TEXT),
                     Arc(radius=1.3,start_angle=PI/2,angle=PI,color=GREY).move_to([-5,-.5,0]))
        target=cell(1.85,.65,color=GREEN,r=.19)
        brain=Ellipse(width=1.6,height=.95,color=GREY).move_to([2,.6,0])
        mouse.shift(UP*.25);brain.shift(UP*.25);target.shift(UP*.25)
        self.add(mouse,brain,target,heading('Brown, Lemke and colleagues · 2000'),
                 Line([1.85,.65,0],[1.2,-1.8,0],color=GREEN),
                 label('superior colliculus',1.2,-2.22,32,GREEN),
                 label('mouse version of the tectum',1.2,-2.93,30))
        self.at('built such');self.play(Indicate(target,color=GREEN,scale_factor=1.8),run_time=.6)
        self.finish()


class S04Isl2(SpokenScene):
    def construct(self):
        m=mosaic();m.remove(m[2]);self.add(m,heading('retina: ganglion cells'),
            label('● Isl2 on',-2.1,-2.93,30,PURPLE),label('● Isl2 off',2.1,-2.93,30,BLUE))
        self.at('about half');self.play(Indicate(m[1],color=PURPLE,scale_factor=1.04),run_time=.6)
        self.finish()


class S05Knockin(SpokenScene):
    def construct(self):
        gene=bar(0,-.75,2.48,10.7,BLUE)
        insert=chip('EphA3 coding sequence',PURPLE,46,pad=.32).move_to([0,2.25,0])
        arrow=Arrow([3.8,1.8,0],[3.8,.58,0],color=PURPLE,buff=.06)
        self.add(gene,label('Isl2 gene',0,-2.38,42,BLUE),insert,arrow,
                 label('knock-in',5.12,1.20,36,PURPLE))
        self.at('inserted the receptor');self.play(insert.animate.move_to([0,-.75,0]),run_time=1.6)
        self.at('do not normally');self.play(FadeIn(label('Mouse ganglion cells: no native EphA3',0,-3.25,30)),run_time=.5)
        self.finish()


class S06Neighbours(SpokenScene):
    def construct(self):
        m=mosaic();self.add(m,heading('Neighbours across the retina'),
            label('extra EphA3 + usual receptors',0,-2.92,28,PURPLE),
            label('usual receptors only',0,-3.48,28,BLUE),
            Rectangle(width=.14,height=.55,fill_color=PURPLE,fill_opacity=1,stroke_width=0).move_to([-3.85,-2.92,0]),
            Rectangle(width=.14,height=.25,fill_color=BLUE,fill_opacity=1,stroke_width=0).move_to([-2.75,-3.48,0]))
        self.at('at every point');self.play(Transform(m,mosaic(True)),run_time=.7)
        self.play(Indicate(m[2],color=YELLOW,scale_factor=1.10),run_time=.5)
        self.finish();self.wait(2)


class S07Table(SpokenScene):
    def construct(self):
        t=table()
        for i in [6,7,8,9]:t[i].set_opacity(0)
        self.add(t)
        self.at('adds four');self.play(FadeIn(label('+4 receptor units',0,-3.18,28,PURPLE)),run_time=.4)
        self.at('axons carry');self.play(t[6].animate.set_opacity(1),t[7].animate.set_opacity(1),run_time=.4)
        self.at('Their unchanged');self.play(t[8].animate.set_opacity(1),t[9].animate.set_opacity(1),run_time=.4)
        self.finish()


class S08PredictAbs(SpokenScene):
    def construct(self):
        t=table(active=0);self.add(t)
        self.at('Where do');self.play(FadeIn(label(ABS_Q,0,-3.18,28,YELLOW)),run_time=.3)
        self.finish()


class S09Pause(Scene):
    def construct(self):self.add(table(active=0,question=ABS_Q));self.wait(5)


class S10Abs(SpokenScene):
    def construct(self):
        t=table(active=0);self.add(t)
        self.at('crowd toward');new=table(active=0,abs_first=True)
        self.play(FadeOut(t),FadeIn(new),run_time=.55);t=new
        why=label('Knock-in axons need less ligand than the target has',0,-3.18,28,ORANGE)
        self.play(FadeIn(why),run_time=.3)
        self.at('keep exactly');new=table(True,active=0)
        self.play(FadeOut(t),FadeIn(new),run_time=.55);t=new
        self.finish()


class S11PredictRel(SpokenScene):
    def construct(self):
        t=table(True,active=1);self.add(t)
        self.at('Where does');self.play(FadeIn(label(REL_Q,0,-3.18,28,YELLOW)),run_time=.3)
        self.finish()


class S12Pause(Scene):
    def construct(self):self.add(table(True,active=1,question=REL_Q));self.wait(5)


class S13Rel(SpokenScene):
    def construct(self):
        t=table(True,active=1);self.add(t)
        self.at('outranks every');self.play(Indicate(t[7],color=YELLOW),Indicate(t[9],color=YELLOW),run_time=.6)
        self.at('take the front');new=table(True,active=1,rel_first=True)
        self.play(FadeOut(t),FadeIn(new),run_time=.5);t=new
        self.at('unchanged axons');new=table(True,True,1)
        self.play(FadeOut(t),FadeIn(new),run_time=.5);t=new
        self.finish()


class S14Result(SpokenScene):
    def construct(self):
        m=two_maps();self.add(m)
        self.at('two orderly maps');self.play(Indicate(m,scale_factor=1.015,color=GREEN),run_time=.65)
        self.finish()


class S15Look(SpokenScene):
    def construct(self):
        m=two_maps();self.add(m)
        self.at('Nothing about them');self.play(Transform(m,two_maps(True)),run_time=.6)
        self.at('somewhere new');self.play(Indicate(m[-1],color=BLUE,scale_factor=1.03),run_time=.5)
        self.finish()


class S16Meaning(SpokenScene):
    def construct(self):
        m=two_maps(True);self.add(m)
        self.at('An absolute reading');self.play(Transform(m[0],label('Absolute reading predicts: unchanged axons stay at hollow rings',0,3.38,26)),run_time=.35)
        self.at('cannot produce');self.play(m[0].animate.set_color(GREY),run_time=.4)
        self.at('other axons');self.play(Transform(m,two_maps(True,True)),run_time=.4)
        self.finish()


class S17Beat(Scene):
    def construct(self):self.add(two_maps(True,True));self.wait(3)


class S18Reverse(SpokenScene):
    def construct(self):
        g=slope_frame();self.add(g)
        # Original dose is an outline trace ABOVE the bar, keeping the former
        # shade/concentration visible while the filled bar is halved.
        old=VGroup(*[Line([-5.4+10.8*u,2.25,0],[-5.4+10.8*u,2.25+.22*(1+2*u)/3,0],
                         color=ORANGE,stroke_width=2,stroke_opacity=.35) for u in np.linspace(0,1,45)])
        self.at('by half');self.play(Transform(g[1],ribbon(-.1,.5)),FadeIn(old),
            FadeIn(label('½ ligand everywhere · faint top trace = original',0,-3.4,27,ORANGE)),run_time=.7)
        self.finish();self.wait(1.5)


class S19Predict(SpokenScene):
    def construct(self):self.add(ligand_question());self.finish()


class S20Pause(Scene):
    def construct(self):self.add(ligand_question());self.wait(5)


class S21Reveal(SpokenScene):
    def construct(self):
        g=ligand_question(False);self.add(g)
        self.at('map shifts back');self.play(Transform(g[0],normal_panel(-3.3,True,.5,False)),run_time=.7)
        self.add(label('map shifts back',-3.3,-3.17,27,ORANGE),
                 label('nasal axons run out of target',-3.3,-3.62,26,RED))
        self.at('nothing moves');self.play(Indicate(g[1],color=GREEN,scale_factor=1.015),run_time=.5)
        self.add(label('no rank changed: map stays',3.3,-3.17,26,GREEN))
        self.finish();self.wait(.8)


class S22Mice(SpokenScene):
    def construct(self):
        p=patches(main=False);self.add(p)
        # Preserve every existing label; reveal only the new main zone.
        main=VGroup(*list(patches())[-2:])
        self.at('kept a normal');self.play(FadeIn(main),run_time=.45)
        self.finish()


class S22bPatch(SpokenScene):
    def construct(self):
        p=patches();self.add(p)
        # Adding a zone must not morph unrelated text into new glyphs.
        extra=VGroup(*list(patches(True))[-2:])
        self.at('extra patch');self.play(FadeIn(extra),run_time=.45)
        self.play(Indicate(extra[0],color=YELLOW,scale_factor=1.45),run_time=.7)
        self.finish()


class S23RankFails(SpokenScene):
    def construct(self):
        p=patches(True);self.add(p)
        self.at('cannot give');self.play(FadeIn(patches(True,failed=True)[-1]),run_time=.35)
        self.at('amount of ligand');self.play(FadeIn(patches(True,failed=True,dosage=True)[-1]),run_time=.4)
        self.finish()


class S24Beat(Scene):
    def construct(self):self.add(patches(True,failed=True,dosage=True));self.wait(2)


class S25Both(SpokenScene):
    def construct(self):
        toys=VGroup(chip('fixed threshold',TEXT,28).move_to([-3.1,3.1,0]),chip('pure rank',TEXT,28).move_to([3.1,3.1,0]))
        self.add(toys,ribbon(.1,.7,h=3.7),label('front',-5.3,-2.05,26),label('back',5.3,-2.05,26))
        self.at('neither toy');self.play(*[toy[0].animate.set_stroke(GREY).set_fill(GREY,.12) for toy in toys],run_time=.4)
        self.at('slope sets');self.play(FadeIn(label('The slope sets the scale',0,2.49,30,ORANGE)),run_time=.4)
        ranked=VGroup()
        for i,r in enumerate(np.linspace(3,1,7)):
            x=-4.25+8.5*rank(r)
            ranked.add(cell(x,-2.45,(r+1)/4,BLUE,.17),label(str(i+1),x,-3.02,26,YELLOW))
        self.at('Comparison among');self.play(FadeIn(ranked),FadeIn(label('Comparison sets the order',0,-3.60,30,YELLOW)),run_time=.6)
        self.finish()


class S26Handoff(SpokenScene):
    def construct(self):
        timeline=VGroup(label('Overlapping in time',0,3.40,28,YELLOW),
                        Line([-5.4,2.97,0],[5.4,2.97,0],color=YELLOW,stroke_width=6),
                        label('coarse layout + activity sharpening',0,2.59,26))
        self.add(timeline,ribbon(-.6,.7,h=3.7))
        broad=VGroup(*[Ellipse(width=1.8,height=1.15,color=BLUE,fill_color=BLUE,fill_opacity=.35)
                      .move_to([x,-.5,0]) for x in [-3.6,0,3.6]])
        sharp=VGroup(*[cell(x,-.5,color=BLUE,r=.19) for x in [-3.6,0,3.6]])
        cells=VGroup(*[cell(x,1.70,.2,BLUE,.17) for x in np.linspace(-4.5,4.5,9)])
        self.add(broad,label('broad',0,-1.50,28,BLUE),
                 label('ephrin-A slope in target',0,-2.85,27,ORANGE))
        self.at('Correlated activity');self.play(FadeIn(cells),FadeIn(label('retina',-5.4,1.7,26,BLUE)),
            FadeIn(label('correlated firing',0,2.13,26,YELLOW)),run_time=.35)
        self.play(LaggedStart(*[c.animate.set_fill(YELLOW,.95).set_stroke(YELLOW) for c in cells],lag_ratio=.12),run_time=.85)
        self.add(*[Arrow([x,1.42,0],[x,.16,0],color=YELLOW,buff=.06,stroke_width=2) for x in [-3.6,0,3.6]])
        self.at('helps sharpen');self.play(Transform(broad,sharp),Transform(self.mobjects[3],label('broad → sharp',0,-1.50,28,BLUE)),run_time=.8)
        self.at('next unit');self.play(FadeIn(label('Next: Spontaneous Activity',0,-3.35,30,YELLOW)),run_time=.5)
        self.finish();self.wait(1.5)


class S27Takeaway(SpokenScene):
    def construct(self):
        self.add(ribbon(.15,.7,h=4.5),label("An axon's place is a rank, set against a slope.",0,-3.1,32,YELLOW))
        for r in np.linspace(3,1,7):
            self.add(cell(-4.8+9.6*rank(r),.15,(r+1)/4,BLUE,.23))
        self.finish()


class S28End(EndCard):
    LINE="An axon's place is a rank, set against a slope."
