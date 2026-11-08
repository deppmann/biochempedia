"""Needed Is Not Stored — reviewed animation.
COLOR MAP (shared with scenes.old.py): BLUE declarative memory; PURPLE skill
learning; TEAL working memory; ORANGE amnesic patients; GOLD Parkinson's;
YELLOW chance; GREY neutral structure/control; GREEN preserved; RED lost.
Anatomy is schematic, never a segmentation or a scale reconstruction.
Blink traces are computed from a Boolean event model: closure = learned AND
pre-puff window OR reflex AND post-puff window. Only event order is encoded;
there is no fitted physiological waveform or invented measurement.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def tick(c=GREEN, s=.22, w=6):
    return VGroup(Line([-s,0,0],[-s*.3,-s*.8,0],color=c,stroke_width=w),
                  Line([-s*.3,-s*.8,0],[s,s*.9,0],color=c,stroke_width=w))


def cross(c=RED, s=.23, w=6):
    return VGroup(Line([-s,-s,0],[s,s,0],color=c,stroke_width=w),
                  Line([-s,s,0],[s,-s,0],color=c,stroke_width=w))


def arr(a,b,color=GREY,w=4):
    return Arrow(a,b,buff=.1,color=color,stroke_width=w,tip_length=.18)


def lab(t,y=3.15,c=TEXT,size=30):
    return T(t,size,c).move_to([0,y,0])


def leader(a,b):
    return VGroup(Dot(a,radius=.055,color=TEXT),Line(a,b,color=GREY,stroke_width=2))


def dim(m, opacity):
    """Dim existing paint without filling previously transparent line paths."""
    for part in m.family_members_with_points():
        part.set_stroke(opacity=part.get_stroke_opacity()*opacity)
        part.set_fill(opacity=part.get_fill_opacity()*opacity)
    return m


class Blink:
    """Full-size timing diagram. Logical times are schematic, without units."""
    def __init__(self,learned=True,reflex=True,title='Eyelid closure · timing schematic'):
        self.base=VGroup(lab(title,3.2,GREY,28),
            Line([-4.9,-1.6,0],[5.8,-1.6,0],color=GREY),
            Line([-4.9,-1.6,0],[-4.9,1.65,0],color=GREY),
            T('closed',26,GREY).move_to([-5.7,1.1,0]),
            T('open',26,GREY).move_to([-5.65,-1.5,0]),
            T('time →',26,GREY).move_to([5,-3.05,0]))
        self.events=VGroup(Line([-4.6,-2.2,0],[1.1,-2.2,0],color=TEXT,stroke_width=9),
            T('tone',26).move_to([-2.8,-2.8,0]),
            DashedLine([1.1,-2.4,0],[1.1,2.25,0],color=GREY),
            T('puff',26).move_to([1.1,2.65,0]))
        self.learned=self.segment(-4.8,1.1,learned,False,PURPLE)
        self.reflex=self.segment(1.1,5.6,False,reflex,GREEN)
        self.group=VGroup(self.base,self.events,self.learned,self.reflex)

    @staticmethod
    def segment(a,b,learned,reflex,col):
        # Evaluate the Boolean model immediately before/after each event boundary.
        edges=[a]+[x for x in (-2.5,.35,1.65,2.8) if a<x<b]+[b]
        def state(t):
            return int((learned and -2.5<=t<.35) or (reflex and 1.65<=t<2.8))
        pts=[]
        for i in range(len(edges)-1):
            lo,hi=edges[i:i+2]; v=state((lo+hi)/2)
            pts.extend([[lo,-1.5+2.6*v,0],[hi,-1.5+2.6*v,0]])
        return VMobject(color=col,stroke_width=6,fill_opacity=0).set_points_as_corners(pts)


def question_frame():
    b=Blink(False,True,title='Pause and predict')
    b.base[0].move_to([0,3.3,0])
    b.reflex.set_stroke(color=GREY,opacity=.25).set_fill(opacity=0)
    q=T('Paralysed? Would the reflex blink survive?',30).move_to([-.3,2.5,0])
    # Shift puff label into its own clear lane above the marker.
    b.events[-1].move_to([1.1,1.9,0]); b.events[2].put_start_and_end_on([1.1,-2.4,0],[1.1,1.5,0])
    m=T('?',60,GREY).move_to([3.6,.1,0])
    return b,q,m


def rabbit():
    head=Ellipse(width=4.1,height=2.8,color=GREY,fill_color=GREY,fill_opacity=.07).move_to([.7,.4,0])
    ears=VGroup(*[Ellipse(width=.65,height=2,color=GREY).rotate(a).move_to([x,2.1,0])
        for x,a in ((-.2,-.2),(.8,.1))])
    eye=Dot([1.65,.9,0],radius=.16,color=TEXT)
    nose=Dot([2.65,.35,0],radius=.12,color=GREY)
    return VGroup(head,ears,eye,nose)


def brain():
    """Neutral puzzle brain only; species-specific brains are used subsequently."""
    return human().scale(.8)


# Projected inferior-oblique human schematic. Posterior is at the TOP.
# The same local coordinates are kept in s12–s17: posterior hippocampus y=1.05;
# anterior hippocampus y=-.15; amygdala y=-1.1; EC x=±1.6, y=-1.0.
def hemi_points(side):
    # Outer convex cortex and a nearly straight medial wall meet at the cleft.
    a=np.linspace(-np.pi/2,np.pi/2,73)
    x=.09+2.48*np.cos(a)*(1+.035*np.cos(12*a))
    y=2.48*np.sin(a)
    outer=np.column_stack((side*x,y,np.zeros_like(x)))
    yy=np.linspace(2.48,-2.48,25)
    inner=np.column_stack((side*(.09+.025*np.sin(yy*4)),yy,np.zeros_like(yy)))
    return np.vstack((outer,inner,outer[:1]))


def human():
    depth=np.array([.28,.18,0])
    surfaces=VGroup(); folds=VGroup()
    for side in (-1,1):
        p=hemi_points(side)
        surfaces.add(Polygon(*(p+depth),color=GREY,stroke_width=1.5,
            fill_color=GREY,fill_opacity=.08))
        # Shaded ribbons connect the front and back cortical surfaces.
        for i in range(0,72,6):
            q=p[i:i+7]
            surfaces.add(Polygon(*q,*(q[::-1]+depth),color=GREY,stroke_width=.6,
                fill_color=GREY,fill_opacity=.16))
        surfaces.add(Polygon(*p,color=GREY,stroke_width=2,
            fill_color=GREY,fill_opacity=.045))
        for j,y in enumerate((-1.8,-1.05,-.25,.6,1.4,2.0)):
            w=2.1*np.sqrt(max(.1,1-(y/2.5)**2))
            pts=[[side*.3,y,0],[side*.7,y+.16,0],[side*1.05,y-.12,0],
                [side*(w*.8),y+.1,0],[side*w,y-.12,0]]
            folds.add(VMobject(color=GREY,stroke_width=1.7,fill_opacity=0)
                .set_points_smoothly(pts).set_fill(opacity=0).set_stroke(opacity=.55))
            pts2=[[side*1.05,y-.12,0],[side*1.25,y-.35,0],[side*1.4,y-.42,0]]
            folds.add(VMobject(color=GREY,stroke_width=1.4,fill_opacity=0)
                .set_points_smoothly(pts2).set_fill(opacity=0).set_stroke(opacity=.5))
    return VGroup(surfaces,folds)


def holes(which):
    shapes=VGroup()
    for s in (-1,1):
        if which=='hp':
            p=VMobject().set_points_smoothly([[s*.6,.55,0],[s*.55,-.25,0],
                [s*.85,-.65,0],[s*1.2,-.45,0],[s*1,-.05,0],[s*.95,.55,0],[s*.6,.55,0]])
        elif which=='am':
            p=Ellipse(width=.95,height=.65).rotate(s*.4).move_to([s*.95,-1.12,0])
        else:
            p=VMobject().set_points_smoothly([[s*1.35,-.45,0],[s*1.9,-.5,0],
                [s*1.85,-1.85,0],[s*1.4,-1.9,0],[s*1.35,-.45,0]])
        p.set_fill(opacity=0).set_stroke(RED,width=3)
        shapes.add(DashedVMobject(p,num_dashes=24))
    return shapes


def remnants():
    # Periodic tapered ovals have a continuous outline, including the inferior tip.
    angle=np.linspace(0,TAU,97)
    x=.8+.34*np.cos(angle)*(1+.16*np.sin(angle))
    y=1.18+.66*np.sin(angle)
    return VGroup(*[VMobject(color=GREEN,fill_color=GREEN,fill_opacity=.28,stroke_width=4)
        .set_points_smoothly(np.column_stack((side*x,y,np.zeros_like(x)))).close_path()
        for side in (-1,1)])


def positioned(m):
    return m.shift(LEFT*1.8)


def anatomy_caption():
    return VGroup(T('H.M. · human brain',30,ORANGE).move_to([-1.65,3.15,0]),
        T('2,401 block-face images · schematic',26,GREY).move_to([-1.65,-3.25,0]))


def all_holes():
    return VGroup(*(holes(k) for k in ('hp','am','ec')))


def circuit(y=1.55):
    tone=chip('tone',GREY,28).move_to([-5,y,0])
    store=chip('store?',GREY,30).move_to([-1.8,y,0])
    eye=chip('eyelid',GREY,28).move_to([4.9,y,0])
    incoming=arr(tone.get_right(),store.get_left())
    cable=Line(store.get_right(),eye.get_left(),color=TEXT,stroke_width=6)
    return VGroup(tone,store,eye,incoming,cable)


def mini_trace(cx,cy,learned=False,reflex=True,w=4.4,h=1.35):
    """Same model and puff coordinate as Blink; 26-pt labels stay unscaled."""
    def xy(x,y): return [cx+(x+.1)*w/10.7,cy+(y+.2)*h/3.2,0]
    axes=VGroup(Line(xy(-4.9,-1.6),xy(5.8,-1.6),color=GREY),
        Line(xy(-4.9,-1.6),xy(-4.9,1.65),color=GREY))
    labels=VGroup(T('closed',26,GREY).move_to([cx-w/2-.45,cy+.56,0]),
        T('open',26,GREY).move_to([cx-w/2-.4,cy-.56,0]),
        T('tone',26).move_to([cx-.8,cy-h/2-.58,0]),
        T('puff',26).move_to([xy(1.1,0)[0],cy+h/2+.35,0]),
        T('time →',26,GREY).move_to([cx+w/2-.4,cy-h/2-.58,0]))
    events=VGroup(DashedLine(xy(1.1,-2),xy(1.1,1.8),color=GREY),
        Line(xy(-4.6,-2.1),xy(1.1,-2.1),color=TEXT,stroke_width=5))
    traces=VGroup()
    for a,b,l,r,col in ((-4.8,1.1,learned,False,PURPLE),(1.1,5.6,False,reflex,GREEN)):
        t=Blink.segment(a,b,l,r,col)
        t.apply_function(lambda p:np.array(xy(p[0],p[1])))
        t.set_stroke(width=4)
        traces.add(t)
    return VGroup(axes,labels,events,traces)


class S00Title(TitleCard):
    TITLE='Needed Is Not Stored'
    LESSON='Memory Systems'


class S01(SpokenScene):
    def construct(self):
        b=human().scale(.9).shift(LEFT*3.2)
        r=RoundedRectangle(width=.9,height=1.5,corner_radius=.2,color=GREY,
            fill_color=GREY,fill_opacity=.4).move_to([-2.3,-.2,0])
        label=T('damaged structure',28).move_to([-3.2,-3,0])
        lead=leader(r.get_bottom(),[-3.2,-2.65,0])
        mem=chip('memory',BLUE,40).move_to([3,1.3,0])
        link=Line(r.get_right(),mem.get_left(),color=BLUE,stroke_width=4)
        self.add(b,r,label,lead,mem,link)
        self.at('damage to a structure')
        self.play(r.animate.set_color(RED),run_time=.3)
        self.at('wipes out a memory')
        hole=DashedVMobject(r.copy().set_fill(opacity=0),num_dashes=18)
        self.play(ReplacementTransform(r,hole),FadeOut(mem),FadeOut(link),run_time=.4)
        self.at('was the memory')
        self.play(FadeIn(T('Stored\nthere?',56).move_to([3,.1,0])),run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        r=rabbit(); self.add(r)
        speaker=Polygon([-5,.3,0],[-4.5,.3,0],[-3.8,-.2,0],[-3.8,1.5,0],[-4.5,1,0],[-5,1,0],color=GREY)
        nozzle=Rectangle(width=1.1,height=.4,color=GREY).move_to([4.7,.9,0])
        self.at('In rabbits')
        self.play(FadeIn(T('Rabbit · schematic',28,GREY).move_to([-4.1,2.9,0])),run_time=.3)
        tone=VGroup(Line([-4.7,-2.1,0],[1.7,-2.1,0],color=TEXT,stroke_width=10),
            T('tone',28).move_to([-2.5,-2.8,0]))
        puff=VGroup(Line([1.4,-2.4,0],[1.4,-1.8,0],color=TEXT,stroke_width=8),
            T('puff',28).move_to([1.4,-2.8,0]))
        self.at('a tone is paired')
        self.play(FadeIn(speaker),FadeIn(T('tone',28).move_to([-4.5,1.9,0])),
            GrowArrow(arr([-3.6,1.1,0],[-.55,2.5,0])),Create(tone),run_time=.4)
        self.at('a puff of air')
        self.play(FadeIn(nozzle),FadeIn(T('puff of air',28).move_to([4.7,1.9,0])),
            GrowArrow(arr([4,.9,0],[2,.9,0])),FadeIn(puff),run_time=.4)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        b=Blink(False,False); self.add(b.group)
        self.at('After training')
        self.play(Transform(b.learned,Blink().learned),run_time=.5)
        self.at('before the puff')
        self.play(FadeIn(T('conditioned response\nbefore puff',28,PURPLE).move_to([-2,1.9,0])),run_time=.3)
        self.at('The puff itself')
        self.play(Transform(b.reflex,Blink().reflex),run_time=.5)
        self.at('a reflex blink')
        self.play(FadeIn(T('reflex blink',28,GREEN).move_to([3.8,1.9,0])),run_time=.3)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        # Rabbit dorsal view: cerebellum caudal to (below) the cerebrum.
        hemis=VGroup(*[Ellipse(width=2.3,height=3.1,color=GREY,fill_color=GREY,fill_opacity=.08)
            .move_to([x,.85,0]) for x in (-1.2,1.2)])
        cereb=Ellipse(width=4.7,height=1.5,color=GREY).move_to([0,-1.7,0])
        folds=VGroup(*[Arc(radius=.8,start_angle=.1,angle=2.9,color=GREY).stretch_to_fit_height(.3)
            .move_to([x,-1.7,0]) for x in (-1.4,-.45,.45,1.4)])
        region=Ellipse(width=1.25,height=1.1,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([1.65,-1.7,0])
        eye=Dot([2.5,2.1,0],radius=.15,color=TEXT)
        self.add(hemis,cereb,folds,region,eye,lab('Rabbit brain · dorsal schematic',3.2,GREY,28))
        self.at('In 1982')
        self.play(FadeIn(T('Thompson lab\n1982 study',28).move_to([-4.7,.7,0])),run_time=.35)
        self.at('removed the lateral cerebellum')
        hole=VGroup(region.copy().set_stroke(width=0).set_fill(BG,opacity=1),
            DashedVMobject(region.copy().set_color(RED).set_fill(opacity=0),num_dashes=18))
        name=T('lateral\ncerebellum',28).move_to([4.7,-1.7,0])
        self.play(ReplacementTransform(region,hole),FadeIn(name),
            Create(leader([2.3,-1.7,0],[3.6,-1.7,0])),run_time=.5)
        self.at('on the same side')
        self.play(FadeIn(T('trained eye',28).move_to([4.6,2.1,0])),
            FadeIn(T('same side',28).move_to([4.7,.25,0])),
            Create(leader([2.65,2.1,0],[3.4,2.1,0])),run_time=.4)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        b=Blink(False,True,title='After lesion · eyelid timing schematic'); self.add(b.group)
        self.at('was abolished')
        self.play(Transform(b.learned,Blink(False).learned),
            FadeIn(T('conditioned response: gone',28,PURPLE).move_to([-2.3,1.9,0])),
            FadeIn(T('reflex intact',28,GREEN).move_to([3.8,1.9,0])),run_time=.4)
        self.wait(2.1)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        b,q,m=question_frame(); self.add(b.group)
        self.at('Was the eyelid')
        self.play(FadeIn(q),run_time=.35)
        self.at('what would happen')
        self.play(FadeIn(m),run_time=.35)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        b,q,m=question_frame(); self.add(b.group,q,m); self.wait(5)


class S08(SpokenScene):
    def construct(self):
        b,q,m=question_frame(); self.add(b.group,q,m)
        self.at('It would fail too')
        fail=T('would fail',28,GREY).move_to([3.6,1.65,0])
        self.play(FadeOut(m),FadeIn(fail),run_time=.3)
        m=fail
        self.at('but the reflex blink survived')
        self.play(FadeOut(q),FadeOut(m),Transform(b.reflex,Blink().reflex),
            Transform(b.events,Blink().events),
            Transform(b.base[0],lab('Reflex spared after lesion',3.2,GREY,28)),run_time=.45)
        answer=VGroup(tick(),T('can still move',30,GREEN)).arrange(RIGHT,buff=.25).move_to([3.75,1.9,0])
        self.play(FadeIn(answer),run_time=.3)
        self.at('could still move')
        self.play(Indicate(answer,color=GREEN,scale_factor=1.025),run_time=.3)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        b=Blink(False,True,title='Other eye · eyelid timing schematic'); self.add(b.group)
        eyes=VGroup(*[Ellipse(width=.65,height=.35,color=GREY).move_to([x,2.6,0]) for x in (-4.7,-2.3)])
        eyes.add(cross(s=.18).move_to([-4.7,2.6,0]),tick(s=.16).move_to([-2.3,2.6,0]),
            T('lesioned side',26,GREY).move_to([-4.7,2.05,0]),
            T('other eye',26,GREY).move_to([-2.3,2.05,0]))
        self.at('the other eye'); self.play(FadeIn(eyes),run_time=.3)
        self.at('could still be conditioned')
        self.play(Transform(b.learned,Blink().learned),run_time=.45)
        self.at('could still hear')
        self.play(FadeIn(T('✓ can hear',28,GREEN).move_to([-2.8,-3.35,0])),run_time=.3)
        self.at('still learn')
        self.play(FadeIn(T('✓ can learn',28,GREEN).move_to([-1.65,1.55,0])),run_time=.3)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        title=lab('Single dissociation + controls',3.15,TEXT,34)
        rows=VGroup()
        for y,name,evidence in ((1.95,'paralysis','reflex spared'),(.55,'deafness','other eye: tone heard'),
                (-.85,'general loss of learning','other eye: learned')):
            n=T(name,28,GREY).move_to([-3.6,y,0])
            strike=Line(n.get_left(),n.get_right(),color=GREY,stroke_width=2)
            ev=T(evidence,28,GREEN).move_to([3.2,y,0])
            rows.add(VGroup(n,strike,arr([-1,y,0],[.9,y,0]),ev))
        self.add(title)
        self.at('With these controls'); self.play(FadeIn(rows),run_time=.45)
        self.at('the lost response')
        self.play(FadeIn(lab('Good evidence:',-2,TEXT,32)),run_time=.3)
        self.at('is needed for it')
        self.play(FadeIn(lab('cerebellum needed for the learned response',-2.7,GREEN,30)),
            FadeIn(lab('Controls do not establish where it is stored',-3.35,GREY,26)),run_time=.35)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        top=circuit(1.9); bot=circuit(-.9)
        self.add(top,lab('Needed for what?',3.25,TEXT,34))
        # Compact axes preserve label size; each trace sits in its own row.
        t1=mini_trace(2.6,.35,False,True,w=4.6,h=.65)
        t2=mini_trace(2.6,-2.45,False,True,w=4.6,h=.65)
        # Both trials lose only the learned closure; the post-puff reflex survives.
        for trace in (t1,t2):
            trace[1][4].set_opacity(0)  # No time label over the circuit below.
        self.at('But needed for what'); self.wait(.1)
        self.at('A lost response'); self.play(FadeIn(bot),run_time=.3)
        self.at('a lost store')
        self.play(top[1].animate.set_opacity(.2),
            FadeIn(T('store erased',28).move_to([-4.6,.65,0])),FadeIn(t1),run_time=.35)
        self.at('a cut output route')
        gap=VGroup(Line([.3,-.9,0],[1.3,-.9,0],color=BG,stroke_width=12),cross().move_to([.8,-.9,0]))
        self.play(FadeIn(gap),FadeIn(T('cable cut',28).move_to([-4.6,-2.15,0])),FadeIn(t2),
            FadeIn(T('same flat\nconditioned trace',26,GREY).move_to([-3.8,-3.05,0])),run_time=.4)
        self.finish()


class S11bSilence(SpokenScene):
    def construct(self):
        c=circuit(2.05); self.add(c,lab('Output route · timing schematic',3.3,TEXT,32))
        train=mini_trace(-2.7,-1,False,True,w=3.9,h=1.45)
        test=mini_trace(3.9,-1,False,True,w=3.9,h=1.45)
        # Panels are separated; both preserve open/closed, tone, and puff labels.
        phase1=chip('training: drug on',RED,28).move_to([-3.25,.8,0])
        phase2=chip('test: drug off',GREEN,28).move_to([3.4,.8,0])
        train_label=T('training',28).move_to([-3.25,.8,0])
        test_label=T('test (later)',28,GREY).move_to([3.4,.8,0])
        scaffold=VGroup(test[0].copy(),test[1].copy(),test[2].copy()).set_opacity(.55)
        self.add(train,train_label,scaffold,test_label)
        silence=VGroup(T('silenced',28,RED).move_to([1,2.85,0]),arr([1,2.6,0],[1,2.08,0],RED))
        self.at('A later experiment'); self.wait(.1)
        self.at('silenced the output route')
        self.play(c[4].animate.set_color(GREY).set_opacity(.25),FadeIn(silence),run_time=.35)
        self.at('only during training')
        self.play(ReplacementTransform(train_label,phase1),run_time=.35)
        self.at('No learned response appeared')
        absent=T('no learned response',28,PURPLE).move_to([-2.7,-2.75,0])
        self.play(FadeIn(absent),run_time=.3)
        self.at('Once the drug wore off')
        self.play(c[4].animate.set_color(TEXT).set_opacity(1),FadeOut(silence),ReplacementTransform(test_label,phase2),FadeOut(scaffold),FadeIn(test),run_time=.4)
        self.at('it was there')
        learned=mini_trace(3.9,-1,True,True,w=3.9,h=1.45)
        self.play(Transform(test[3],learned[3]),FadeIn(T('learned response',28,PURPLE).move_to([3.8,-2.75,0])),run_time=.35)
        self.at('The rabbits had learned')
        self.play(FadeIn(lab('Needed to express, not where it was learned',-3.4,GREEN,28)),run_time=.3)
        self.finish()


def slice_volume():
    """Clip the actual brain silhouettes into horizontal section slabs."""
    def clip(poly,bound,above):
        out=[]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            ain=(a[1]>=bound) if above else (a[1]<=bound)
            bin=(b[1]>=bound) if above else (b[1]<=bound)
            if ain: out.append(a)
            if ain!=bin:
                t=(bound-a[1])/(b[1]-a[1]); out.append(a+t*(b-a))
        return out
    slabs=VGroup()
    for y in np.linspace(-2.65,2.25,15):
        band=VGroup()
        for s in (-1,1):
            p=list(hemi_points(s)[:-1]); p=clip(clip(p,y,True),y+.36,False)
            if len(p)>2:
                band.add(Polygon(*p,color=GREY,stroke_width=1.3,fill_color=GREY,fill_opacity=.16))
        slabs.add(band)
    return positioned(slabs)


def reconstruction_volume():
    """Restacked section faces with oblique side walls and visible depth."""
    slabs=slice_volume()
    volume=VGroup()
    depth=np.array([.58,.38,0])
    for band in slabs:
        for face in band:
            points=face.get_vertices()
            sides=VGroup(*[Polygon(a,b,b+depth,a+depth,color=GREY,
                stroke_width=.8,fill_color=GREY,fill_opacity=.28)
                for a,b in zip(points,np.roll(points,-1,axis=0))])
            volume.add(face.copy().shift(depth).set_fill(GREY,opacity=.12),sides,
                face.copy().set_fill(BG,opacity=.8).set_stroke(GREY,width=1.3))
    return volume


class S12(SpokenScene):
    def construct(self):
        b=positioned(human()); cap=anatomy_caption()
        cap[1].become(T('inferior oblique · schematic',26,GREY).move_to([-1.65,-3.25,0]))
        regions=positioned(VGroup(*[Ellipse(width=1.7,height=3.3,color=GREY).move_to([x,-.15,0]) for x in (-1.25,1.25)]))
        self.add(b,regions,cap)
        question=T('Which\nstructure?',38).move_to([4.1,.8,0])
        self.at('raises a second limit'); self.play(FadeIn(question),run_time=.4)
        died=T('died 2008',28).move_to([4.1,2.45,0])
        self.at('After his death'); self.play(FadeOut(question),FadeIn(died),run_time=.35)
        self.at('it was cut into')
        slabs=slice_volume()
        plane=Polygon([-4.6,2.5,0],[.7,2.5,0],[1.05,2.8,0],[-4.25,2.8,0],color=TEXT,fill_color=TEXT,fill_opacity=.12)
        self.add(slabs)
        self.play(FadeOut(regions),Create(plane),run_time=.2)
        self.play(plane.animate.shift(DOWN*5.1),run_time=.7)
        self.play(FadeOut(b),FadeOut(plane),*[s.animate.shift(RIGHT*(.06*i)+UP*(.008*i)) for i,s in enumerate(slabs)],run_time=.45)
        self.at('and rebuilt')
        self.play(Transform(slabs,reconstruction_volume()),run_time=.65)
        self.play(FadeIn(regions),
            Transform(cap[1],anatomy_caption()[1]),
            FadeIn(T('3D reconstruction\nschematic',28,GREY).move_to([4.1,.5,0])),run_time=.4)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        origin=np.array([-1.8,0,0])
        def enlarge(m): return m.scale(1.16,about_point=origin)
        cap=anatomy_caption(); cap[0].set_y(3.45); cap[1].set_y(-3.45)
        self.add(enlarge(reconstruction_volume()),cap,T('Missing tissue',32,RED).move_to([4.1,2.8,0]))
        for phrase,k,text,y,anchor in (
            ('the front of the hippocampus','hp','1  front of\nhippocampus',1.25,[-.65,.15,0]),
            ('most of the amygdala','am','2  most of\namygdala',-.25,[-.45,-1.1,0]),
            ('nearly all the entorhinal cortex','ec','3  nearly all\nentorhinal cortex',-1.95,[.1,-1.85,0])):
            self.at(phrase)
            self.play(Create(enlarge(positioned(holes(k)))),
                FadeIn(T(text,30).move_to([4.35,y,0])),
                Create(leader(origin+1.16*(np.array(anchor)-origin),[2.65,y,0])),run_time=.4)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        b=dim(positioned(human()),.35)
        missing=dim(positioned(all_holes()),.35)
        r=positioned(remnants())
        self.add(b,missing,anatomy_caption())
        self.at('the back of the hippocampus')
        pointer=leader([-.65,1.35,0],[2.7,2.25,0])
        self.play(FadeIn(r),FadeIn(T('posterior\nhippocampus',32,GREEN).move_to([4.15,2.25,0])),
            Create(pointer),run_time=.4)
        # Magnified inset retains the original positions and a visible zoom leader.
        zoom=remnants().scale(2.3).move_to([-1.8,.1,0])
        self.at('on both sides')
        self.play(Transform(r,zoom),FadeOut(b),FadeOut(missing),
            Transform(pointer,leader([.6,.8,0],[2.7,2.25,0])),FadeIn(T('about 2 cm³\neach side',30).move_to([4.15,.75,0])),
            FadeIn(T('posterior detail · enlarged',26,GREY).move_to([-1.8,-1.9,0])),run_time=.4)
        cells=VGroup(*[Dot([x+dx,y,0],radius=.075,color=TEXT)
            for x in (-3.7,.1) for dx,y in ((-.12,-.45),(.1,.1),(-.04,.5))])
        wrong=VGroup(T('both hippocampi',28,GREY),T('removed',28,GREY))
        wrong.arrange(DOWN,buff=.18).move_to([4.15,-1.65,0])
        sl=VGroup(*[Line(line.get_left(),line.get_right(),color=RED,stroke_width=3)
            for line in wrong])
        self.at('with neurons still present')
        self.play(FadeIn(cells),FadeIn(T('neurons in CA1–CA4',28).move_to([-1.8,-2.5,0])),
            FadeIn(VGroup(wrong,sl,T('incorrect',26,RED).move_to([4.15,-2.6,0]))),run_time=.35)
        self.wait(3.1)
        self.finish()


def route():
    # Reuse the same anatomy; leaders turn the missing EC and remnant into a circuit.
    b=dim(positioned(human()),.25)
    h=dim(positioned(all_holes()),.6)
    r=positioned(remnants())
    ec=T('entorhinal cortex\nmissing',28).move_to([4.2,-1.8,0])
    hp=T('posterior hippocampus\nremains',28,GREEN).move_to([4.05,1.9,0])
    names=VGroup(ec,hp,leader([.1,-1.5,0],ec.get_left()+LEFT*.2),
        leader([-.65,1.25,0],hp.get_left()+LEFT*.2))
    # Route physically connects the right missing EC to the posterior remnant.
    cable=arr([-.15,-1.4,0],[-.95,1.1,0],TEXT,6)
    center=np.array([-.39,-.65,0]); direction=np.array([-.8,2.5,0]); direction/=np.linalg.norm(direction)
    cut=VGroup(Line(center-direction*.3,center+direction*.3,color=BG,stroke_width=13),
        cross().move_to(center))
    return VGroup(b,h,r),names,cable,cut


class S15(SpokenScene):
    def construct(self):
        anatomy,names,cable,cut=route()
        cap=anatomy_caption()
        self.add(anatomy,cap,names)
        self.at('The entorhinal cortex'); self.play(Indicate(anatomy[1][2],color=RED,scale_factor=1.03),run_time=.35)
        self.at('the main cortical')
        route_label=T('main cortical route\ninto the hippocampus',28).move_to([4.55,.2,0])
        # The cable itself lies on the anatomy, between its named endpoints.
        self.play(GrowArrow(cable),FadeIn(route_label),run_time=.4)
        self.at('What remained may')
        self.play(FadeIn(cut),run_time=.3)
        self.at('largely cut off')
        self.play(FadeOut(cap[1]),FadeIn(lab('May have been largely cut off',-3.2,TEXT,32)),run_time=.3)
        self.wait(2.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        anatomy,names,cable,cut=route()
        # The disconnected route holds through the first sentence, then zooms to tissue.
        cap=anatomy_caption(); previous=VGroup(anatomy,names,cable,cut,cap)
        self.add(previous)
        self.at('The authors offered')
        title=lab('A model, not a measurement',3.25,TEXT,34)
        self.play(FadeOut(cap),FadeIn(title),run_time=.35)
        section=RoundedRectangle(width=5.3,height=3.8,corner_radius=.15,color=GREY,
            fill_color=GREY,fill_opacity=.08).move_to([-3.25,-.1,0])
        cells=VGroup(*[VGroup(Circle(radius=.18,color=GREY,fill_color=GREY,fill_opacity=.4),
            Dot(radius=.055,color=TEXT)).move_to([-3.25+dx,-.1+dy,0])
            for dx,dy in ((-1.7,.9),(-.5,1.1),(.9,.7),(1.7,-.7),(.2,-.8),(-1.4,-.9))])
        detail=VGroup(section,cells,T('cell bodies in a section',30).move_to([-3.25,-2.55,0]))
        self.at('Living cells in a section')
        self.play(FadeOut(VGroup(anatomy,names,cable,cut)),FadeIn(detail),run_time=.45)
        self.at('do not prove')
        self.play(FadeIn(T('Connected?\n\nWorking?',42).move_to([3.4,0,0])),
            FadeIn(lab('Cell bodies alone cannot answer',-3.25,GREY,28)),run_time=.35)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        b=dim(positioned(human()),.45)
        hs=positioned(all_holes()); r=dim(positioned(remnants()),.5)
        region=positioned(VGroup(*[DashedVMobject(RoundedRectangle(width=2,height=2.8,corner_radius=.5,
            color=ORANGE).move_to([x,-.95,0]),num_dashes=35) for x in (-1.25,1.25)]))
        cap=anatomy_caption()
        lesion_label=T('lesion, both sides',30,ORANGE).move_to([3.8,2.9,0])
        lesion_leads=VGroup(*[leader([x,.45,0],lesion_label.get_left()+LEFT*.2) for x in (-3.05,-.55)])
        self.add(b,hs,r,region,cap,lesion_label,lesion_leads)
        self.at('his amnesia followed'); self.wait(.1)
        self.at('a medial temporal lesion'); self.play(Indicate(region,color=ORANGE,scale_factor=1.015),run_time=.35)
        self.at('on both sides'); self.wait(.1)
        self.at('His case alone cannot')
        # Arrows terminate at the actual right-side anatomical outlines.
        names=VGroup(*[T(n+' ?',28).move_to([4.8,y,0]) for n,y in
            (('hippocampus',.55),('amygdala',-.95),('entorhinal cortex',-2.45))])
        targets=[[-1,.05,0],[-.85,-1.12,0],[-.15,-1.5,0]]
        arrows=VGroup(*[arr(name.get_left()+LEFT*.15,target,TEXT,3)
            for name,target in zip(names,targets)])
        self.play(FadeOut(cap[1]),Create(arrows),FadeIn(names),
            FadeIn(lab('One case cannot assign amnesia to one structure',-3.25,TEXT,28)),run_time=.45)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        # Large columns stay populated for the entire spoken conclusion.
        cards=VGroup(*[RoundedRectangle(width=5.8,height=6.1,corner_radius=.25,color=GREY,
            fill_color=GREY,fill_opacity=.05).move_to([x,0,0]) for x in (-3.15,3.15)])
        rabbit_icon=rabbit().scale(.46).move_to([-4.45,1.65,0])
        hm=human().scale(.36).move_to([-1.85,1.65,0])
        examples=VGroup(rabbit_icon,hm,T('rabbit',28,GREY).move_to([-4.45,.35,0]),
            T('H.M.',28,ORANGE).move_to([-1.85,.35,0]))
        question=T('Where\nmemories live',46,GREY).move_to([3.15,1.35,0])
        self.add(cards,examples,question)
        self.at('Crossed failures show'); self.wait(.1)
        self.at('is needed for a task')
        self.play(FadeIn(tick(s=.58).move_to([-3.15,-.65,0])),
            FadeIn(T('needed\nfor a task',46,GREEN).move_to([-3.15,-2,0])),run_time=.45)
        self.at('They do not tell you')
        self.play(FadeIn(cross(s=.58).move_to([3.15,-.65,0])),
            question.animate.set_opacity(.45),
            FadeIn(T('cannot locate\nthe memory store',36).move_to([3.15,-2,0])),run_time=.45)
        self.finish()


class S19End(EndCard):
    LINE='Lesions show what is needed;\nthey do not locate memory stores.'
