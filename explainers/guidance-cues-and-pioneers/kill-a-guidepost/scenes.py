"""Chapter 2: Kill a Guidepost.
COLOR MAP: BLUE pioneer axons / Ti1; YELLOW guideposts; RED ablation /
abnormal branches; GREY tissue / other neurons' axons; TEXT labels.
Route-leg key: BLUE distal leg, ORANGE return leg, PURPLE ascending leg,
GREEN proximal leg. These distinguish schematic legs, not measured data.
Only the narrated Cx1 endpoint and one tissue boundary are marked;
no cue type is assigned to the other two schematic legs.
All paths are qualitative tissue schematics; no quantitative traces are used.
"""
from bp_style import *
import numpy as np

PURPLE = '#B58CD9'
LIGHT = '#CDD2DC'
P = [np.array([x,y,0.]) for x,y in [(-5.4,-2.9),(-3.1,1.0),(-.9,-2.3),(1.1,.7),(2.8,2.9)]]
Q = [np.array([x,y,0.]) for x,y in [(-5.4,-3.0),(-.8,2.0),(5.3,-2.9)]]
OFFS = [UP*.10, DOWN*.10]
LEG_COLORS = [BLUE, '#F39B52', PURPLE, GREEN]


def path(points,color=BLUE,width=6):
    return VMobject().set_points_as_corners(points).set_stroke(color,width)


def label(txt,y=3.25,color=TEXT,size=32):
    return T(txt,size=size,color=color).move_to([0,y,0])


def gcone(color=BLUE):
    return VGroup(Dot(radius=.10,color=color), *[
        Line(.08*np.array([np.cos(a),np.sin(a),0]),.19*np.array([np.cos(a),np.sin(a),0]),color=color,stroke_width=3)
        for a in np.linspace(0,TAU,7,endpoint=False)]).set_z_index(4)


def pair(pos,r=.24):
    # Cells above the bend: axons touch the lower edge, never cross the cells.
    return VGroup(*[Circle(radius=r,color=YELLOW,fill_opacity=.38,stroke_width=3)
        .move_to(pos+np.array([dx,.48,0])) for dx in (-.29,.29)]).set_z_index(5)


def cxlabel(pos=Q[1],text='Cx1'):
    name=T(text,30,YELLOW)
    name.move_to(pos+[1.2+name.width/2,.85,0])
    return VGroup(name,Line(pos+[.6,.63,0],pos+[1.05,.85,0],color=YELLOW,stroke_width=2))


def tube(): return path(P,GREY,65).set_stroke(opacity=.2)


def neurons():
    return VGroup(*[Circle(radius=.23,color=BLUE,fill_opacity=.4).move_to(P[0]+[dx,0,0]) for dx in (-.28,.28)])


def route(stop=5,color=BLUE):
    return VGroup(*[path([p+o for p in P[:stop]],color) for o in OFFS])


def cones(i): return VGroup(*[gcone().move_to(P[i]+o) for o in OFFS])


def walk(scene,h,a,b,rt=.8):
    ls=VGroup(*[Line(P[a]+o,P[b]+o,color=BLUE,stroke_width=6) for o in OFFS])
    scene.play(Create(ls),*[v.animate.move_to(P[b]+o) for v,o in zip(h,OFFS)],run_time=rt)


def cns(): return chip('central nervous\nsystem',LIGHT,26).move_to([4.9,2.65,0])


def pioneer_label():
    return VGroup(T('pioneers of\nthe distal leg',28,BLUE).move_to([-4.75,.65,0]),
        Line([-4.65,-.05,0],[-4.2,-.6,0],color=BLUE,stroke_width=2))


def turn_base(cells=True,arrived=False,turned=False):
    end=Q[1] if arrived else Q[0]+.34*(Q[1]-Q[0])
    pts=[Q[0],Q[1],Q[2]] if turned else [Q[0],end]
    ax=VGroup(*[path([p+o for p in pts]) for o in OFFS])
    heads=VGroup(*[gcone().move_to((Q[2] if turned else end)+o) for o in OFFS])
    return VGroup(path(Q,GREY,90).set_stroke(opacity=.18),ax,heads,pair(Q[1]) if cells else VGroup())


def arrive(scene,b):
    scene.play(*[h.animate.move_to(Q[1]+o) for h,o in zip(b[2],OFFS)],
        *[Transform(l,Line(Q[0]+o,Q[1]+o,color=BLUE,stroke_width=6)) for l,o in zip(b[1],OFFS)],run_time=.65)


def turn(scene,b):
    ls=VGroup(*[Line(Q[1]+o,Q[2]+o,color=BLUE,stroke_width=6) for o in OFFS])
    scene.play(Create(ls),*[h.animate.move_to(Q[2]+o) for h,o in zip(b[2],OFFS)],run_time=.7)


def missing(pos=Q[1]):
    return DashedVMobject(Ellipse(width=1.2,height=.85,color=LIGHT).move_to(pos+UP*.48),num_dashes=14)


def branches():
    return VGroup(*[Line(Q[1],e,color=RED,stroke_width=6) for e in
        [[-4,2.8,0],[1.7,2.65,0],[3.9,.55,0],[1.6,-1.6,0]]])


def failed(needed=False):
    g=VGroup(turn_base(False,True),branches(),missing())
    if needed: g.add(T('needed at this turn',30,YELLOW).move_to([3.5,-.7,0]))
    return g


def zoom_failed():
    # 1.6x turn detail, with incoming/outgoing tissue clipped to the safe frame.
    c=np.array([-1.25,.35,0])
    tissue=path([[-5.4,-3.2,0],c,[5.4,-3.2,0]],GREY,110).set_stroke(opacity=.18)
    ax=VGroup(*[Line([-5.4,-3.2,0],c+o,color=BLUE,stroke_width=7) for o in OFFS])
    fan=VGroup(*[Line(c,p,color=RED,stroke_width=7) for p in
        [[-5.2,1.65,0],[.2,2.85,0],[4.8,1.2,0],[2.5,-3.05,0]]])
    gap=missing(c).scale(1.6,about_point=c)
    return VGroup(tissue,ax,fan,gap)


def predictions():
    panels=VGroup()
    for x,normal in [(-3.3,True),(3.3,False)]:
        box=RoundedRectangle(width=6.3,height=6.25,corner_radius=.18,color=GREY,stroke_opacity=.6).move_to([x,-.25,0])
        title=T('only on the way' if normal else 'needed',32).move_to([x,2.35,0])
        pp=[np.array([x-2.25,-2.9,0]),np.array([x-.45,1.35,0]),np.array([x+2.3,-2.3,0])]
        tissue=path(pp,GREY,65).set_stroke(opacity=.18)
        start=Line(pp[0],pp[1],color=BLUE,stroke_width=7)
        if normal: out=Line(pp[1],pp[2],color=GREEN,stroke_width=7)
        else:
            out=VGroup(*[DashedLine(pp[1],pp[1]+d,color=LIGHT,stroke_width=4,dash_length=.14) for d in
                [np.array([-.9,-1.3,0]),np.array([1,-.6,0]),np.array([2,-1.8,0])]],
                T('?',48).move_to([x+1.2,-.6,0]))
        panels.add(VGroup(box,title,tissue,start,out))
    return panels


def question(): return label('Which happened?',3.3,size=34)


def timer():
    c=np.array([5.8,3.2,0])
    return VGroup(Circle(radius=.36,color=GREY).move_to(c),T('5',26).move_to(c))


def legs(): return VGroup(*[Line(P[i],P[i+1],color=col,stroke_width=9) for i,col in enumerate(LEG_COLORS)])


def legkey():
    return VGroup(*[VGroup(Line([2.95,1.65-i*1.25,0],[3.45,1.65-i*1.25,0],color=col,stroke_width=7),
        T('leg '+str(i+1),26).move_to([5.1,1.5-i*1.25,0])) for i,col in enumerate(LEG_COLORS)])


def cuekey():
    # Only the two narrated examples receive a cue assignment.
    names=['leg 1: Cx1', 'leg 2', 'leg 3', 'leg 4']
    return VGroup(*[VGroup(
        Line([2.95,1.65-i*1.25,0],[3.45,1.65-i*1.25,0],color=col,stroke_width=7),
        T(names[i],26).move_to([5.1,1.5-i*1.25,0])) for i,col in enumerate(LEG_COLORS)])


def tissue_boundary(i=3):
    d=P[i+1]-P[i];n=np.array([-d[1],d[0],0])/np.linalg.norm(d)
    return Line(P[i]+n*.30,P[i+1]+n*.30,color=LEG_COLORS[i],stroke_width=7)


def legreadings():
    boundary=tissue_boundary()
    # The label is anchored directly to the green boundary, on its left.
    name=T('tissue boundary',26,GREEN).rotate(boundary.get_angle())
    d=P[4]-P[3];n=np.array([-d[1],d[0],0])/np.linalg.norm(d)
    name.move_to(boundary.get_center()+n*.25)
    return VGroup(cxlabel(P[1]),name)


def intact_legs(readings=False):
    g=VGroup(tube(),legs(),neurons(),cuekey() if readings else legkey())
    if readings:
        g.add(pair(P[1]),tissue_boundary(),legreadings())
    return g


def rulecard():
    return VGroup(T('choice point',32).move_to([0,3.2,0]),
        T('A place where the growth cone picks its next path.',27).move_to([0,2.55,0]))


def choices():
    return VGroup(*[Dot(p+DOWN*.22,radius=.085,color=TEXT).set_z_index(6) for p in P[1:-1]])


def rule_diagram(cells=False):
    g=VGroup(tube(),route(),neurons(),choices(),pair(P[1]) if cells else VGroup())
    # Fill the width and reserve a clear band above for the definition.
    g.stretch(1.4,0,about_point=ORIGIN).stretch(.82,1,about_point=ORIGIN)
    g.shift([1.76,-.55,0])
    for cell in [*g[2], *g[4]]:
        cell.stretch(1/1.4,0).stretch(1/.82,1)
    return g


TAKEAWAY='Remove one guidepost and the pioneers\nlose their normal route at that turn.'

def takeaway(result=True):
    fan=VGroup(*[Line(P[1],P[1]+v,color=RED,stroke_width=6) for v in
        [np.array([-1.5,1.,0]),np.array([1.8,.6,0]),np.array([1.5,-.8,0])]])
    diagram=VGroup(tube(),neurons(),route(2),missing(P[1]),fan,pair(P[1]))
    # Transform cells, gap and branches together to preserve their alignment.
    diagram.stretch(1.3,0,about_point=ORIGIN).stretch(.70,1,about_point=ORIGIN)
    diagram.move_to([0,-1.05,0])
    for cell in [*diagram[1], *diagram[5]]:
        cell.stretch(1/1.3,0).stretch(1/.70,1)
    diagram[3].set_opacity(1 if result else 0)
    diagram[4].set_opacity(1 if result else 0)
    diagram[5].set_opacity(0 if result else 1)
    return VGroup(T(TAKEAWAY,34,font=TITLE_FONT).move_to([0,2.9,0]),
        T('A guidepost is one cue among several.',28).move_to([0,1.65,0]),diagram)


class S00Title(TitleCard):
    LESSON='Pioneers, Guideposts and the Logic of Guidance Cues'
    TITLE='Kill a Guidepost'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('Pioneers, Guideposts and the\nLogic of Guidance Cues',28,LIGHT),T(self.TITLE,54,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.65);self.finish()


class S01Question(SpokenScene):
    def construct(self):
        b=turn_base();self.add(b,label('Does it need that cell to make the turn?',3.3,size=32))
        # Only the incoming axon exists until contact; the outgoing limb grows afterward.
        self.at('touches a cell');arrive(self,b)
        self.at('it turns');turn(self,b)
        self.at('does it need');self.play(Indicate(b[3],color=YELLOW),run_time=.5);self.finish()


class S02Case(SpokenScene):
    def construct(self):
        body=VGroup(Ellipse(width=2,height=3.8,color=LIGHT,fill_opacity=.12).move_to([0,-.25,0]),
            Circle(radius=.65,color=LIGHT,fill_opacity=.12).move_to([0,2.4,0]),
            Line([0,1.65,0],[0,1.75,0],color=LIGHT))
        limbs=VGroup(*[path([[s*.8,y,0],[s*2,y-.4,0],[s*3.8,y-1.5,0]],GREY,16) for s in (-1,1) for y in (.9,0,-.9)])
        target=limbs[4].copy().set_stroke(YELLOW,22)
        caption=label('schematic, not to scale',-3.35,LIGHT,28)
        name=T('grasshopper embryo',30).move_to([-3.7,2.5,0])
        self.add(body,limbs,target,caption)
        self.at('the leg');self.play(Indicate(target,color=YELLOW),run_time=.5)
        self.at('grasshopper embryo');self.play(FadeIn(name),run_time=.35)
        tip=RoundedRectangle(width=6.2,height=6.3,corner_radius=1.5,color=GREY,fill_opacity=.12).move_to([-1,0,0])
        self.play(FadeOut(body),FadeOut(limbs),FadeOut(name),FadeOut(caption),Transform(target,tip),FadeIn(T('leg tip',28,LIGHT).move_to([-1,-2.8,0])),run_time=.65);self.finish()


class S03Ti1(SpokenScene):
    def construct(self):
        tip=RoundedRectangle(width=6.2,height=6.3,corner_radius=1.5,color=GREY,fill_opacity=.12).move_to([-1,0,0])
        ns=VGroup(*[Circle(radius=.8,color=BLUE,fill_opacity=.35,stroke_width=5).move_to([-1,y,0]) for y in (-1.15,1.15)])
        self.add(tip,ns,T('leg tip',28,LIGHT).move_to([-1,-2.8,0]))
        self.at('near the tip');self.play(Indicate(tip,color=LIGHT,scale_factor=1.02),run_time=.45)
        self.at('pair of sensory');self.play(Indicate(ns,color=BLUE),run_time=.45)
        self.at('called');self.play(FadeIn(T('Ti1',42,BLUE).move_to([3,.2,0])),Create(Line([0,.2,0],[2,.2,0],color=BLUE)),run_time=.4);self.finish()


class S04Pioneers(SpokenScene):
    def construct(self):
        h=cones(0);self.add(tube(),neurons(),h)
        self.at('first axons');walk(self,h,0,1,1.0)
        self.at('central nervous system');self.play(FadeIn(cns()),run_time=.35)
        self.at('far part');self.play(FadeIn(pioneer_label()),run_time=.4)
        self.at('no earlier axons');self.play(Indicate(h,color=BLUE),run_time=.5);self.finish()


class S04bJoin(SpokenScene):
    def construct(self):
        h=cones(1);self.add(tube(),neurons(),route(2),h,pioneer_label(),cns())
        self.at('pioneers there');self.play(Indicate(h,color=BLUE),run_time=.5)
        early=VGroup(*[path([P[2]+o,P[3]+o,P[4]+o],LIGHT,9) for o in OFFS])
        self.at('the body');self.play(Create(early),FadeIn(T("other neurons’\naxons",28,LIGHT).move_to([4.7,.4,0])),run_time=.45)
        self.at('they join');walk(self,h,1,2,.8);self.finish()


class S05Turns(SpokenScene):
    def construct(self):
        self.add(tube(),neurons())
        self.at('several turns');self.play(LaggedStart(*[Flash(p,color=LIGHT,line_length=.18,flash_radius=.3) for p in P[1:-1]],lag_ratio=.2),run_time=.7)
        posts=VGroup(pair(P[1]),pair(P[2]))
        self.at('young neurons');self.play(FadeIn(posts),run_time=.45)
        self.at('touch just');self.play(Indicate(posts,color=YELLOW),run_time=.6);self.finish()


class S06Cx1(SpokenScene):
    def construct(self):
        b=turn_base();self.add(b)
        self.at('one of these');self.play(Indicate(b[3],color=YELLOW),run_time=.45)
        self.at('pair of cells');arrive(self,b)
        self.at('called');self.play(FadeIn(cxlabel()),run_time=.3)
        turn(self,b);self.finish()


class S07Touch(SpokenScene):
    def construct(self):
        self.add(turn_base(True,True,True),cxlabel())
        self.at('touching is not');self.play(FadeIn(label('Touching is not needing.',3.35,size=34)),run_time=.4)
        self.at('and turn there');self.finish()


class S08Who(SpokenScene):
    def construct(self):
        self.add(turn_base(True,True,True),cxlabel())
        self.at('David');self.play(FadeIn(label('David Bentley and Michael Caudy, 1983',3.35,size=32)),run_time=.4)
        self.at('the direct question');self.finish()


class S09Kill(SpokenScene):
    def construct(self):
        b=turn_base();lab=cxlabel();self.add(b,lab)
        crosses=VGroup(*[VGroup(Line(c.get_center()+[-.2,-.2,0],c.get_center()+[.2,.2,0],color=RED,stroke_width=5),Line(c.get_center()+[-.2,.2,0],c.get_center()+[.2,-.2,0],color=RED,stroke_width=5)) for c in b[3]])
        self.at('selectively destroyed');self.play(Create(crosses),b[3].animate.set_color(RED),run_time=.4)
        self.wait(.65)
        self.play(FadeOut(b[3]),FadeOut(crosses),FadeOut(lab),Create(missing()),FadeIn(cxlabel(text='Cx1 destroyed')),run_time=.5)
        self.at('before the pioneer');self.play(Indicate(b[2],color=BLUE),run_time=.5);self.finish()


class S10Options(SpokenScene):
    def construct(self):
        p=predictions();self.add(p[0][0],p[0][2],p[1][0],p[1][2])
        self.at('only on the way');self.play(FadeIn(p[0][1]),run_time=.3)
        self.at('should look normal');self.play(Create(p[0][3]),Create(p[0][4]),run_time=.55)
        self.at('if it is needed');self.play(FadeIn(p[1][1]),run_time=.3)
        self.at('should go wrong');self.play(Create(p[1][3]),Create(p[1][4]),run_time=.6);self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        self.add(predictions());self.at('which happened');self.play(FadeIn(question()),FadeIn(timer()),run_time=.3);self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(predictions(),question())
        clock=timer();self.add(clock)
        for n in range(5,0,-1):
            ring=Arc(radius=.36,start_angle=PI/2,angle=-TAU,color=YELLOW,stroke_width=5).move_arc_center_to([5.8,3.2,0])
            self.remove(clock[1]);clock[1]=T(str(n),26).move_to([5.8,3.2,0]);self.add(clock[1],ring)
            self.play(Uncreate(ring),run_time=1,rate_func=linear)


class S13Reveal(SpokenScene):
    def construct(self):
        b=turn_base(False);self.add(b,missing())
        self.at('failed to take');arrive(self,b)
        self.at('sent branches');self.play(LaggedStart(*[Create(l) for l in branches()],lag_ratio=.15),run_time=1);self.finish()


class S14Need(SpokenScene):
    def construct(self):
        self.add(failed());self.at('cones need');self.play(FadeIn(T('needed at this turn',30,YELLOW).move_to([3.5,-.7,0])),run_time=.4);self.finish()


class S15Beat1(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(failed(True));self.wait(2.5)


class S16Narrow(SpokenScene):
    def construct(self):
        g=failed();caption=label('this turn, this preparation',3.35,size=32);self.add(g)
        self.at('conclusion is narrow');self.play(Transform(g,zoom_failed()),FadeIn(caption),run_time=.85)
        self.at('this turn');self.finish()


class S17What(SpokenScene):
    def construct(self):
        g=zoom_failed();self.add(g)
        a=chip('adhesion?',LIGHT,30).move_to([3,1.9,0])
        s=chip('signal?',LIGHT,30).move_to([3,-.5,0])
        arrows=VGroup(*[Arrow(g[3].get_right(),box.get_left(),color=LIGHT,buff=.15)
            for box in (a,s)])
        self.at('adhesion');self.play(g[2].animate.set_opacity(.18),
            FadeIn(a),GrowArrow(arrows[0]),run_time=.35)
        self.at('or a');self.play(FadeIn(s),GrowArrow(arrows[1]),run_time=.35);self.finish()


class S18Later(SpokenScene):
    def construct(self):
        self.add(tube(),neurons())
        self.at('later work');self.play(FadeIn(label('Caudy and Bentley',3.45,LIGHT,28)),run_time=.3)
        self.at('full route');self.play(Create(legs()),run_time=.65)
        self.at('several legs');self.play(FadeIn(legkey()),run_time=.4);self.finish()


class S19Legs(SpokenScene):
    def construct(self):
        g=intact_legs();self.add(g,label('Cue types • schematic examples',3.5,LIGHT,28))
        readings=legreadings();key=cuekey()
        self.at('read from guideposts');self.play(FadeIn(pair(P[1])),FadeIn(readings[0]),
            Transform(g[3][0],key[0]),run_time=.5)
        self.at('boundaries');self.play(Create(tissue_boundary()),FadeIn(readings[1]),run_time=.5);self.finish()


class S20Several(SpokenScene):
    def construct(self):
        self.add(intact_legs(True),label('schematic examples',-3.5,LIGHT,24))
        self.at('one important cue');self.play(FadeIn(label('one important cue among several',3.5,size=30)),run_time=.4);self.finish()


class S21Rule(SpokenScene):
    def construct(self):
        g=rule_diagram();dots=g[3];self.add(g[0],g[1],g[2],rulecard())
        self.at('choice point');self.play(FadeIn(dots),run_time=.35)
        self.at('picks its next');self.play(*[Indicate(d,color=TEXT,scale_factor=1.5) for d in dots],run_time=.6);self.finish()


class S22Mark(SpokenScene):
    def construct(self):
        g=rule_diagram(True);self.add(*g[:4],rulecard())
        self.at('a guide post cell');self.play(FadeIn(g[4]),run_time=.35)
        pos=P[1]*np.array([1.4,.82,1])+np.array([1.76,-.55,0])
        self.at('guide that choice');self.play(FadeIn(cxlabel(pos)),run_time=.3);self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        card=takeaway(False);self.add(card)
        self.at('remove');self.play(card[2][5].animate.set_opacity(0),
            card[2][3].animate.set_opacity(1),run_time=.6)
        self.at('lose their normal');card[2][4].set_opacity(1)
        self.play(Create(card[2][4]),run_time=.7);self.finish()


class S24End(EndCard):
    LINE='Remove one guidepost and the pioneers lose their normal route at that turn.'
    def construct(self):
        self.add(takeaway(True));self.finish()
