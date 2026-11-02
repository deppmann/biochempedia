"""Chapter 1, schematic language routes (not anatomical tract reconstructions).
COLOR MAP: TEAL sound form / ventral; GOLD dorsal; PURPLE speech generation;
TEXT planner / execution; GREY structure; GREEN preserved; RED damage/failure;
AMBER impaired naming or erroneous output. No data traces or molecular structures.
"""
from bp_style import *

PURPLE = '#C49BFF'
AMBER = '#E3A349'
NOTE = '#C1C7D2'
S = [-4.25, .25, 0]
MPT = [-1.5, -1.5, 0]
P = [1.9, .25, 0]

# Keep word timing local: no edits to pipeline files or their sync.log.
class Timed(SpokenScene):
    def at(self, phrase, lead=.15, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02: self.wait(rest)


def label(txt, pos, size=28, color=TEXT):
    return T(txt, size, color).move_to(pos)


def heading(txt, color=TEXT):
    return label(txt, [0,3.42,0], 34, color)


def foot(txt):
    return label(txt,[0,-3.62,0],24,NOTE)


def node(txt,pos,color=TEXT):
    return chip(txt,color,size=28,pad=.18).move_to(pos).set_z_index(5)


def path(points,color,width=5):
    return VMobject(stroke_color=color,stroke_width=width).set_points_smoothly(points)


def cut(pos):
    x,y,_=pos
    return VGroup(*[Line([x+dx-.12,y-.22,0],[x+dx+.12,y+.22,0],color=RED,stroke_width=7) for dx in [-.13,.13]]).set_z_index(8)


def rp(pos):
    # Enlarge the entire persistent schematic, including all road endpoints.
    return np.array([-1.3, .3, 0]) + 1.12 * (np.array(pos) - [-1.3, .3, 0])


def ear_icon(pos, color=TEAL, height=.9):
    outer=path([[.15,-.45,0],[-.04,-.46,0],[-.13,-.28,0],[-.12,-.12,0],[-.32,.08,0],[-.31,.35,0],[-.11,.5,0],[.16,.48,0],[.31,.29,0],[.27,.06,0],[.12,-.08,0],[.08,-.25,0]],color,4)
    inner=path([[-.12,.16,0],[-.1,.32,0],[.08,.34,0],[.16,.2,0],[.02,.07,0],[-.02,-.08,0]],color,3)
    return VGroup(outer,inner).scale_to_fit_height(height).move_to(pos)


def brain():
    # Side view: posterior left, anterior right. Fissures distinguish lobes.
    b=path([[-5.55,-.35,0],[-5.65,1.15,0],[-4.8,2.3,0],[-2.9,2.8,0],[-.8,2.75,0],[1.3,2.35,0],[2.85,1.25,0],[3.05,-.1,0],[2.2,-1.05,0],[.6,-1.95,0],[-1.9,-2.18,0],[-4.1,-1.6,0],[-5.55,-.35,0]],NOTE,2)
    b.set_fill(GREY,.055)
    fiss=VGroup(path([[-.1,2.65,0],[-.55,1.8,0],[-.2,1.1,0]],GREY,2),path([[-4.8,-.4,0],[-3.2,-.7,0],[-1,-.65,0],[1.1,-.45,0]],GREY,2),path([[-4.65,2,0],[-4.85,.9,0],[-4.75,.6,0]],GREY,2))
    # Faint lobe fields sit behind the routes; no extra anatomical claims.
    lobes=VGroup(
        Polygon([-.1,2.65,0],[1.3,2.3,0],[2.8,1.2,0],[2.9,-.1,0],[1,-.5,0],[-.2,1.1,0],[-.55,1.8,0],stroke_width=0,fill_color=GREY,fill_opacity=.10),
        Polygon([-.1,2.65,0],[-2.9,2.68,0],[-4.6,2,0],[-4.75,.6,0],[-.2,1.1,0],[-.55,1.8,0],stroke_width=0,fill_color=TEAL,fill_opacity=.07),
        Polygon([-4.6,2,0],[-5.5,1.1,0],[-5.45,-.35,0],[-4.7,-1,0],[-4.75,.6,0],stroke_width=0,fill_color=GOLD,fill_opacity=.10))
    return VGroup(b,lobes,fiss,label('back',[-5.55,2.7,0],26,NOTE),label('front',[2.8,2.7,0],26,NOTE))


class Road(VGroup):
    def set_opacity(self, opacity, family=True):
        # Changing route brightness must never fill the open Bezier curves.
        self.set_stroke(opacity=opacity, family=family)
        for part in self.get_family():
            if isinstance(part, VMobject):
                part.set_fill(opacity=opacity if isinstance(part, ArrowTip) else 0, family=False)
        return self


def route(dorsal=True,ventral=True,speech=False):
    sound=node('sound form',S,TEAL); meaning=node('meaning',MPT,TEAL); planner=node('planner',P)
    # Roads meet node edges. Ventral arrows are spaced along the same road.
    vline=path([sound.get_bottom(),[-4.2,-1.4,0],[-3.3,-1.85,0],meaning.get_left()],TEAL)
    # Opposed arrows share the lower straightaway, in separate visible lanes.
    v=Road(vline,
           Arrow([-3.65,-1.7,0],[-2.5,-1.7,0],buff=0,color=TEAL,stroke_width=5,tip_length=.24,max_tip_length_to_length_ratio=.3),
           Arrow([-2.5,-2.04,0],[-3.65,-2.04,0],buff=0,color=TEAL,stroke_width=5,tip_length=.24,max_tip_length_to_length_ratio=.3))
    dline=path([sound.get_top(),[-3.6,1.85,0],[-.2,1.85,0],planner.get_top()],GOLD)
    d=Road(dline,Arrow([-.9,1.87,0],[.05,1.78,0],buff=0,color=GOLD,stroke_width=4))
    # Separate inner curves; never parallel to the lower ventral tract.
    a=CurvedArrow(meaning.get_top(),sound.get_right()+DOWN*.03,angle=-.65,color=PURPLE,stroke_width=5,tip_length=.2)
    b=CurvedArrow(sound.get_right()+UP*.12,planner.get_left()+UP*.12,angle=-.5,color=PURPLE,stroke_width=5,tip_length=.2)
    gen=Road(a,b)
    outline=brain()
    VGroup(outline,v,d,gen,sound,meaning,planner).scale(1.12,about_point=[-1.3,.3,0])
    g=VGroup(outline)
    if ventral:g.add(v)
    if dorsal:g.add(d)
    if speech:g.add(gen)
    g.add(sound,meaning,planner)
    return g,sound,meaning,planner,v,d,gen


def tests():
    return VGroup(*[node(t,[x,-2.78,0],NOTE) for t,x in zip(['fluency','comprehension','repetition','naming'],[-4.8,-1.5,2,4.9])])


def stage(title='',dim=False):
    g,s,m,p,v,d,gen=route(speech=True)
    if dim:
        for a in [v,d,gen]:a.set_opacity(.22)
    ts=tests()
    return g,s,m,p,v,d,gen,ts,heading(title)


def active(scene,ts,index,color=TEXT):
    scene.play(*[t.animate.set_color(color if i==index else NOTE) for i,t in enumerate(ts)],run_time=.25)


def travel(scene,mob,color=PURPLE,duration=1):
    # Flash each curve/arrow separately to preserve visible tips.
    pieces=list(mob) if isinstance(mob,VGroup) else [mob]
    scene.play(*[ShowPassingFlash(a.copy().set_color(color).set_stroke(width=9),time_width=.45) for a in pieces],run_time=duration)


def motor(extra=False):
    lines=['motor cortex','basal ganglia','cerebellum','brainstem']
    if extra:lines+=['nerves','muscles']
    title=T('motor system',28)
    entries=VGroup(*[T(t,26) for t in lines]).arrange(DOWN,buff=.22)
    words=VGroup(title,entries).arrange(DOWN,buff=.38)
    box=RoundedRectangle(width=3.05,height=words.height+.55,corner_radius=.18,color=NOTE,fill_color=BG,fill_opacity=1).move_to([5.12,.4,0]).set_z_index(2)
    words.move_to(box).set_z_index(3)
    rule=Line(box.get_left()+RIGHT*.22,box.get_right()+LEFT*.22,color=NOTE,stroke_width=1).set_y(title.get_bottom()[1]-.17).set_z_index(3)
    note=label('execution outside\nlanguage network',[5.12,box.get_bottom()[1]-.48,0],26,NOTE)
    # Keep a flat word group for the damage marker's muscles reference.
    return VGroup(box,VGroup(title,*entries),note,rule)


def pen(pos=[-.1,-1.6,0]):
    body=Polygon([-.38,-.13,0],[.23,.48,0],[.4,.31,0],[-.21,-.3,0],color=TEXT,fill_color=TEXT,fill_opacity=.15)
    tip=Polygon([-.38,-.13,0],[-.46,-.38,0],[-.21,-.3,0],color=TEXT)
    return VGroup(body,tip,Line([.15,.4,0],[.32,.23,0],color=TEXT)).move_to(pos)


def quiz(which):
    g,s,m,p,v,d,gen,ts,h=stage('Which tests suffer most?' if which==1 else 'What will she do?')
    c=cut(rp([-1.2,1.86,0] if which==1 else [-4.12,-1.05,0]))
    return VGroup(g,c,h,ts)


class S00Title(TitleCard):
    LESSON='Language and Lateralization'
    TITLE='One Route to Speech'
    def construct(self):
        self.add(heading(self.LESSON,TEAL),label(self.TITLE,[0,.35,0],56),Line([-2,-.7,0],[2,-.7,0],color=GOLD))
        self.wait(3)


class S01Question(Timed):
    def construct(self):
        self.add(heading('One syllable, yet much understood'))
        window=VGroup(Rectangle(width=2,height=2.4),Line([-1,0,0],[1,0,0]),Line([0,-1.2,0],[0,1.2,0])).set_color(NOTE).move_to([-4.55,1.25,0])
        bed=VGroup(RoundedRectangle(width=8.7,height=.75).move_to([-.2,-.9,0]),Line([-4.7,-1.28,0],[-4.7,-2.5,0]),Line([4.3,-1.28,0],[4.3,-2.5,0]),Line([-4.7,-1.28,0],[-4.7,.1,0])).set_color(NOTE)
        head=Circle(.55,color=TEXT).move_to([-2.9,.2,0]); body=Line([-2.4,-.05,0],[2.7,-.4,0],color=TEXT,stroke_width=15)
        ward=VGroup(window,bed,head,body).shift(RIGHT*.65)
        self.add(ward)
        self.at('could say'); bubble=VGroup(RoundedRectangle(width=2.6,height=1.2,color=TEXT,fill_color=BG,fill_opacity=1).move_to([.2,1.65,0]),label('tan',[.2,1.65,0],42)); tail=Polygon([-1.1,1.45,0],[-2.55,.8,0],[-.8,1.35,0],color=TEXT,fill_color=BG,fill_opacity=1)
        self.play(FadeIn(bubble),Create(tail),run_time=.4)
        self.at('Yet he appeared'); ear=ear_icon([4.7,1.45,0]); self.play(Create(ear),FadeIn(label('✓ follows speech',[3.3,2.35,0],30,GREEN)),run_time=.4)
        self.at('What exactly'); self.play(FadeIn(label('What exactly had broken?',[0,-3.05,0],38)),run_time=.3)
        self.finish()


class S02Rule(Timed):
    def construct(self):
        self.add(heading('The route to speech'))
        boxes=VGroup()
        for txt,x,c in [('what you want\nto say',-4.5,TEAL),('language\nnetwork',0,TEXT),('speech',4.5,TEXT)]:
            box=RoundedRectangle(width=3.3,height=2.1,color=c).move_to([x,.15,0]); boxes.add(VGroup(box,label(txt,box.get_center(),32,c)))
        self.add(boxes[0])
        self.at('You can say'); self.play(FadeIn(boxes[1:]),Create(VGroup(*[Arrow(boxes[i].get_right(),boxes[i+1].get_left(),buff=.08,color=TEXT) for i in range(2)])),run_time=.45)
        self.at('speaking hemisphere'); brace=Brace(boxes[1],UP,color=NOTE); self.play(Create(brace),FadeIn(label('speaking hemisphere',[0,2.25,0],28,NOTE)),run_time=.35)
        self.at('by an unbroken'); self.play(FadeIn(label('You can say only what reaches\nthe language network by an unbroken route.',[0,-2.25,0],32)),run_time=.4)
        self.finish()


class S03Rule2(Timed):
    def construct(self):
        self.add(heading('Each test travels part of the route'),foot('simplified sketch'))
        ns=VGroup(*[VGroup(RoundedRectangle(width=3.15,height=1.65,color=NOTE).move_to([x,.1,0]),label(t,[x,.1,0],32)) for t,x in [('what you want\nto say',-4.5),('language\nnetwork',0),('speech',4.5)]])
        ps=VGroup(*[DashedLine(ns[i].get_right(),ns[i+1].get_left(),color=NOTE,stroke_width=6) for i in range(2)])
        self.add(ns,ps)
        self.at('travels part'); travel(self,ps,TEXT,1.2)
        self.at('the pattern'); self.play(FadeIn(cut([2.2,.1,0])),run_time=.3)
        self.at('broken stretch'); self.play(FadeIn(label('The pattern points to a broken stretch',[0,-1.75,0],34)),run_time=.35)
        self.finish()


def hemispheres():
    h=VGroup()
    for x,name in [(-3,'Left'),(3,'Right')]:
        h.add(VGroup(Ellipse(width=4.3,height=4.65,color=NOTE,fill_color=GREY,fill_opacity=.07).move_to([x,.35,0]),Dot([x-1,.05,0],radius=.25,color=TEAL),label(name,[x,2.95,0],30)))
    h.add(label('front',[0,2.65,0],26,NOTE),label('back',[0,-2.1,0],26,NOTE))
    return h


class S04Soundform(Timed):
    def construct(self):
        h=hemispheres(); self.add(h)
        self.at('both hemispheres'); self.play(*[Indicate(a[1],color=TEAL) for a in h[:2]],run_time=.65)
        self.at('on the left'); g,s,m,p,v,d,gen=route(False,False); g.remove(s,m,p); spot=Dot(rp(S),radius=.3,color=TEAL)
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(g),ReplacementTransform(h[0][1].copy(),spot),FadeIn(heading('Left hemisphere • side view')),run_time=.6)
        self.at('at the back'); self.play(FadeIn(label('superior temporal lobe',[-3.75,-.63,0],28,NOTE).add_background_rectangle(color=BG,opacity=1,buff=.04)),Indicate(spot),run_time=.4)
        self.at('Here roughly'); self.play(FadeIn(label('roughly Wernicke’s area',[-3.75,-1.13,0],26,NOTE).add_background_rectangle(color=BG,opacity=1,buff=.04)),run_time=.3)
        self.at('sound form'); self.play(ReplacementTransform(spot,s),run_time=.45)
        self.finish()


class S05Ventral(Timed):
    def construct(self):
        g,s,m,p,v,d,gen=route(False,False);g.remove(m,p); self.add(g,heading('Ventral • lower road',TEAL))
        self.at('One road');self.play(Create(v[0]),run_time=.7)
        self.at('temporal lobe');self.play(FadeIn(label('temporal lobe',[.65,-.32,0],28,NOTE)),run_time=.3)
        self.at('to meaning');self.play(FadeIn(m),FadeIn(v[1:]),run_time=.4)
        self.at('understand spoon');spoon=VGroup(Ellipse(width=.45,height=.65,color=TEXT).move_to([-1.5,-.1,0]),Line([-1.5,-.43,0],[-1.5,-1.0,0],color=TEXT,stroke_width=5));self.play(Create(spoon),run_time=.5)
        self.at('Run backwards');self.play(v[2].animate.set_color(TEXT),run_time=.3);travel(self,v[0].copy().reverse_points(),TEAL,1.6);self.wait(2)
        self.finish()


class S06Dorsal(Timed):
    def construct(self):
        g,s,m,p,v,d,gen=route(False,True);g.remove(p);self.add(g,heading('Dorsal • upper road',GOLD))
        self.at('The other');self.play(Create(d),run_time=.8)
        self.at('parietal cortex');self.play(FadeIn(label('parietal cortex',[-2.1,2.38,0],28,NOTE)),run_time=.3)
        self.at('frontal lobe');fr=node('frontal lobe',rp(P));self.play(FadeIn(fr),run_time=.3)
        self.at('It links');travel(self,d,GOLD,1.4)
        self.finish()


class S07Planner(Timed):
    def construct(self):
        g,s,m,p,v,d,gen=route();self.add(g,heading('Planner • roughly Broca’s area'))
        self.at('assembles the phrase');self.play(Indicate(p),run_time=.5)
        lips=VGroup(path([[-.5,0,0],[-.2,.2,0],[0,.12,0],[.2,.2,0],[.5,0,0],[0,-.22,0],[-.5,0,0]],TEXT,3),Line([-.5,0,0],[.5,0,0],color=TEXT))
        tongue=VGroup(path([[-.5,.3,0],[-.5,-.25,0],[.4,-.25,0],[.5,0,0],[.2,.1,0],[-.25,.05,0]],TEXT,3))
        neck=VGroup(path([[-.4,.4,0],[-.25,.1,0],[-.25,-.4,0]],TEXT,3),path([[.4,.4,0],[.25,.1,0],[.25,-.4,0]],TEXT,3),RoundedRectangle(width=.3,height=.55,corner_radius=.06,color=TEXT))
        icons=VGroup()
        for i,(ic,txt) in enumerate([(lips,'lips'),(tongue,'tongue'),(neck,'larynx')]):ic.move_to([4.9,1.5-i*1.5,0]);icons.add(VGroup(ic,label(txt,[4.9,.95-i*1.5,0],26)))
        self.at('plans its');self.play(Create(Arrow(p.get_right(),[4.1,.25,0],buff=.1,color=TEXT)),run_time=.3)
        self.at('movements');self.play(LaggedStart(*[FadeIn(a) for a in icons],lag_ratio=.2),run_time=.6)
        self.finish()


class S08Speech(Timed):
    def construct(self):
        g,s,m,p,v,d,gen=route();self.add(g,heading('Speech generation',PURPLE))
        self.at('Spontaneous speech');self.play(Indicate(m),run_time=.45)
        self.at('finds each');self.play(Create(gen[0]),run_time=.55)
        self.at('reaches the same');self.play(Create(gen[1]),run_time=.55)
        self.at('The dorsal road');self.play(d.animate.set_opacity(.4),run_time=.4)
        self.at('The motor system');box=motor();self.play(FadeIn(box),Create(Arrow(p.get_right(),box[0].get_left(),buff=.03,color=TEXT)),run_time=.5)
        self.finish()


class S09Bilateral(Timed):
    def construct(self):
        h=hemispheres();self.add(h)
        ds=VGroup();vs=VGroup()
        for x in [-3,3]:
            # Reuse the actual side-view roads, scaled uniformly to each oval.
            _,_,_,_,v,d,_=route()
            for road in (v,d):road.scale(.4,about_point=rp(S)).shift(np.array([x-1,.05,0])-rp(S))
            ds.add(d.set_opacity(1 if x<0 else .45));vs.add(v)
        self.at('the dorsal road');self.play(Create(ds),run_time=.6)
        self.at('strongly');self.play(FadeIn(label('dominant dorsal',[-3,-2.45,0],28,GOLD)),FadeIn(label('fainter dorsal',[3,-2.45,0],28,GOLD)),run_time=.3)
        self.at('Understanding single');self.play(Create(vs),run_time=.5)
        self.at('both hemispheres');self.play(FadeIn(foot('Ventral road supports single words on both sides')),run_time=.3)
        self.finish()


class S10Tests(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Four bedside tests',True);self.add(g,h)
        self.at('four bedside');self.play(LaggedStart(*[FadeIn(t) for t in ts],lag_ratio=.15),run_time=.65)
        self.at('different part');self.play(v.animate.set_opacity(.65),d.animate.set_opacity(.65),gen.animate.set_opacity(.65),run_time=.5)
        self.finish()


class S11Fluency(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Fluency',True);self.add(g,ts,h)
        self.at('Fluency is judged');active(self,ts,0,PURPLE);self.play(gen.animate.set_opacity(1),run_time=.35)
        tags=VGroup(*[label(t,[4.9,y,0],26,NOTE) for t,y in [('phrase length',2),('rate',1.3),('effort',.6),('grammar',-.1)]])
        self.at('Phrase length');self.play(FadeIn(tags),run_time=.4)
        self.at('Several systems');note=label('planner: one of\nseveral contributors',[4.6,-1.25,0],26,NOTE);self.play(FadeIn(note),Indicate(p),run_time=.4)
        self.at('Comprehension links');self.remove(h);self.add(heading('Comprehension',TEAL));v.set_opacity(1);gen.set_opacity(.22);ts[0].set_color(NOTE);ts[1].set_color(TEAL);self.play(FadeOut(tags),FadeOut(note),run_time=.3);self.wait(3)
        self.finish()


class S12Repetition(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Repetition',True);self.add(g,ts,h)
        self.at('Repetition runs');active(self,ts,2,GOLD);self.play(d.animate.set_opacity(1),run_time=.3);travel(self,d,GOLD,.9)
        self.at('Naming runs');self.remove(h);self.add(heading('Naming',PURPLE));self.play(d.animate.set_opacity(.22),gen.animate.set_opacity(1),run_time=.3);active(self,ts,3,PURPLE)
        self.at('object to meaning');obj=pen([.5,-1.45,0]);self.play(Create(obj),FadeIn(label('seen object',[1.2,-2.12,0],26,NOTE)),Create(Arrow([.1,-1.5,0],m.get_right(),buff=.06,color=TEXT)),run_time=.4)
        self.at('to the planner');travel(self,gen,PURPLE,.6)
        self.finish()


class S13Naming(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Naming can fail at many stages');self.add(g,ts,h);ts[3].set_color(RED)
        self.at('damage at many');c=cut(gen[0].point_from_proportion(.15));self.play(FadeIn(c),run_time=.3)
        self.at('can spoil naming');self.play(c.animate.move_to(gen[0].point_from_proportion(.88)),Indicate(ts[3],color=RED),run_time=.4)
        self.at('That is why');self.play(c.animate.move_to(gen[1].point_from_proportion(.8)),Indicate(ts[3],color=RED),FadeIn(foot('Naming alone rarely separates syndromes')),run_time=.4)
        self.wait(2)
        self.finish()


class S14Broca(Timed):
    def construct(self):
        ts=tests();self.add(ts,heading('Broca aphasia'),foot('composed for teaching'),label('“Boy … cookie … uh … fall.”',[0,.65,0],54))
        self.at('speech is slow');self.play(Indicate(self.mobjects[-1],scale_factor=1.03),ts[0].animate.set_color(RED),run_time=.6)
        self.at('Comprehension is relatively');self.play(FadeIn(label('comprehension: relatively preserved',[0,-1.1,0],32,GREEN)),ts[1].animate.set_color(GREEN),run_time=.3)
        self.at('repetition is poor');self.play(FadeIn(label('repetition: poor',[0,-1.9,0],32,RED)),ts[2].animate.set_color(RED),run_time=.3)
        self.finish()


class S15Broca2(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Broca aphasia');self.add(g,ts,h)
        self.add(label('repetition',[-1.6,2.52,0],26,GOLD),label('fluency',[-.9,.65,0],26,PURPLE).add_background_rectangle(color=BG,opacity=1,buff=.08),label('comprehension',[-2.8,-.98,0],26,TEAL).add_background_rectangle(color=BG,opacity=1,buff=.06))
        self.at('toward the frontal');zone=Ellipse(width=3.7,height=2.85,color=RED,stroke_width=2).move_to(rp([1.3,.55,0])).set_z_index(1);self.play(Create(zone),run_time=.45)
        self.at('assembled and planned');self.play(FadeIn(foot('real lesions usually reach further')),run_time=.3)
        self.at('Speech and repetition');self.play(d.animate.set_opacity(.2),gen.animate.set_opacity(.2),ts[0].animate.set_color(RED),ts[2].animate.set_color(RED),run_time=.45)
        self.at('Simple comprehension');self.play(ts[1].animate.set_color(GREEN),run_time=.25);travel(self,v,TEAL,.8)
        self.finish()


class S16Wernicke(Timed):
    def construct(self):
        q=label('“the boy is over there\ndoing the tooken, you know.”',[0,.35,0],48)
        ts=tests();self.add(ts,heading('Wernicke aphasia'),q,foot('composed for teaching'))
        self.at('speech flows');self.play(Indicate(q,scale_factor=1.03),ts[0].animate.set_color(GREEN),run_time=.6)
        self.at('Words are swapped');self.play(q.animate.set_color(AMBER),run_time=.4)
        self.finish()


class S17Wernicke2(Timed):
    def construct(self):
        g,s,m,p,v,d,gen,ts,h=stage('Wernicke aphasia');self.add(g,ts,h)
        zone=Ellipse(width=3.2,height=3.6,color=RED,stroke_width=2).move_to(rp([-4,.25,0])).set_z_index(1)
        # Lesion precedes its consequences; leave node text fully opaque.
        self.at('Comprehension');self.play(Create(zone),run_time=.4);self.play(v.animate.set_opacity(.2),d.animate.set_opacity(.2),ts[1].animate.set_color(RED),ts[2].animate.set_color(RED),run_time=.4)
        self.at('damage sits');self.play(Indicate(zone,color=RED),run_time=.5)
        self.at('both roads begin');self.play(Indicate(s,color=RED),run_time=.4)
        self.at('touches several');wrong=node('tooken ×',[-2.7,.9,0],AMBER);self.play(FadeIn(wrong),run_time=.2);self.play(wrong.animate.move_to([.7,.9,0]),run_time=.9);self.play(FadeIn(foot('Speech flows; words carry errors')),run_time=.3)
        self.finish()


class S18Q1(Timed):
    def construct(self):
        q=quiz(1);self.add(q[0],q[3]);h=heading('Now you try');self.add(h)
        self.at('is impaired');self.play(FadeIn(q[1]),run_time=.35)
        self.at('speech generation still');travel(self,q[0][-4],PURPLE,.8)
        self.at('Which tests');self.play(FadeOut(h),FadeIn(q[2]),run_time=.3)
        self.finish()


def countdown(scene,which):
    scene.camera.background_color=BG;scene.add(quiz(which))
    ring=Circle(1,color=NOTE).move_to([4.65,.45,0]);sweep=Arc(radius=1,start_angle=PI/2,angle=-TAU,color=GOLD,stroke_width=8).move_to(ring)
    scene.add(ring,label('think',[4.65,.45,0],28,NOTE));scene.play(Create(sweep),run_time=5,rate_func=linear)


class S19Pause(Scene):
    def construct(self):countdown(self,1)


class S20Reveal1(Timed):
    def construct(self):
        q=quiz(1);self.add(q);ts=q[3]
        self.at('Repetition fails');self.play(ts[2].animate.set_color(RED),run_time=.3)
        self.at('Speech stays');self.play(ts[0].animate.set_color(GREEN),run_time=.3)
        self.at('sound errors');self.play(Indicate(ts[0],color=AMBER),run_time=.4)
        self.at('Comprehension is');self.play(ts[1].animate.set_color(GREEN),run_time=.3)
        self.at('Naming often');self.play(ts[3].animate.set_color(AMBER),run_time=.3)
        self.at('This is');self.play(FadeIn(node('Conduction\naphasia',[4.6,-.8,0],TEXT)),run_time=.3)
        self.wait(1.4) # label is readable for at least three seconds including tail
        self.finish()
        if self.elapsed()<16.3:self.wait(16.3-self.elapsed())


class S21Nonword(Timed):
    def construct(self):
        q=quiz(1);h=heading('Real words: a detour through meaning');self.add(q[0],q[1],q[3],h)
        g,s,m,p,v,d,gen=route(speech=True)
        dot=Dot(v[0].get_start(),radius=.15,color=TEXT).set_z_index(9)
        trace=VGroup(*[road.copy().set_color(TEXT).set_stroke(width=6).set_z_index(3) for road in [v[0],gen[0],gen[1]]])
        self.at('Real words');self.add(dot);self.play(MoveAlongPath(dot,v[0]),Create(trace[0]),run_time=2)
        self.at('with help from');self.play(MoveAlongPath(dot,gen[0]),Create(trace[1]),run_time=1.05)
        self.at('still reaches');self.play(MoveAlongPath(dot,gen[1]),Create(trace[2]),run_time=1.6)
        self.at('like');self.remove(dot,h,*trace);self.add(heading('blick • nonword'));card=node('blick',[-5.35,1.48,0]);feed=Arrow(card.get_bottom(),s.get_top(),buff=.06,color=GOLD,tip_length=.2);self.play(FadeIn(card),Create(feed),run_time=.3)
        self.at('lean on');stop=path([s.get_top(),rp([-3.6,1.85,0]),rp([-1.5,1.86,0])],GOLD);dot=Dot(s.get_top(),radius=.12,color=GOLD);self.add(dot);self.play(MoveAlongPath(dot,stop),run_time=.75);self.play(FadeIn(foot('Dorsal road: holds and maps the sounds')),Indicate(q[1],color=RED),run_time=.35)
        self.wait(2)
        self.finish()


class S22Q2(Timed):
    def construct(self):
        q=quiz(2);self.add(q[0],q[3]);h=heading('Now change the break');self.add(h)
        self.at('ventral road breaks');self.play(FadeIn(q[1]),run_time=.4)
        self.at('speech generation still');g,s,m,p,v,d,gen=route(speech=True);travel(self,gen,PURPLE,.8)
        self.at('What will');self.play(FadeOut(h),FadeIn(q[2]),run_time=.3)
        self.finish()


class S23Pause(Scene):
    def construct(self):countdown(self,2)


class S24Reveal2(Timed):
    def construct(self):
        q=quiz(2);q[0][2].set_opacity(.35);self.add(q);ts=q[3];g,s,m,p,v,d,gen=route(speech=True)
        self.at('Her speech');self.play(ts[0].animate.set_color(GREEN),run_time=.3)
        self.at('understands poorly');self.play(ts[1].animate.set_color(RED),run_time=.3)
        self.at('echo a sentence');self.play(ts[2].animate.set_color(GREEN),q[0][2].animate.set_opacity(1),run_time=.3);travel(self,d,GOLD,1.3)
        self.at('both ways');self.play(q[0][1][1:].animate.set_color(RED),run_time=.4)
        self.at('naming fails');self.play(ts[3].animate.set_color(RED),run_time=.3)
        self.at('speech grows empty');self.play(FadeIn(label('fluent,\nbut empty',[4.8,.7,0],30,AMBER)),run_time=.3)
        self.at('This is');self.play(FadeOut(q[2]),FadeIn(heading('Transcortical sensory aphasia')),run_time=.3)
        self.finish()


class S25Dysarthria(Timed):
    def construct(self):
        g,s,m,p,v,d,gen=route(speech=True);self.add(g,heading('Dysarthria'));box=motor(True)
        self.at('Weak or uncoordinated');self.play(FadeIn(box),run_time=.4)
        self.at('damage lies');ln=Line(box[1][-1].get_right()+RIGHT*.12,[6.2,box[1][-1].get_y(),0],color=TEXT);c=cut(ln.get_center());self.play(Create(ln),FadeIn(c),run_time=.3)
        self.at('beyond the language');self.play(Create(Arrow(p.get_right(),box[0].get_left(),buff=.03,color=TEXT)),run_time=.3)
        self.at('In isolated');self.play(FadeIn(foot('Isolated dysarthria')),run_time=.3)
        self.at('comprehension and writing');ear=ear_icon([-3.7,-2.8,0],GREEN,.65);pn=pen([.8,-2.8,0]).scale(.7);self.play(Create(ear),Create(pn),FadeIn(label('✓ listening',[-2.1,-2.8,0],28,GREEN)),FadeIn(label('✓ writing',[2.35,-2.8,0],28,GREEN)),run_time=.4)
        self.finish()


class S26Takeaway(Timed):
    def construct(self):
        block=label('The pattern of what fails points to\na broken stretch of the route.',[0,1.4,0],38)
        line=DashedLine([-4.8,-.1,0],[4.8,-.1,0],stroke_width=6,color=NOTE)
        self.add(block,line,cut([.4,-.1,0]),foot('simplified sketch'))
        self.at('broken stretch');travel(self,line,TEXT,.7)
        self.at('It does not');patch=Ellipse(width=1,height=.65,color=NOTE).move_to([-4,-1.8,0]);cross=Cross(patch,stroke_color=RED,stroke_width=6)
        self.play(Create(patch),Create(cross),FadeIn(label('not one small patch of cortex',[.7,-1.8,0],32)),run_time=.4)
        self.finish()


class S27End(EndCard):
    LINE='The pattern points to a broken stretch of the route.'
    def construct(self):
        self.add(label('The pattern points to\na broken stretch of the route.',[0,.4,0],44),label('biochemistrypedia.com',[0,-1.5,0],28,TEAL))
        self.wait(3.5)
