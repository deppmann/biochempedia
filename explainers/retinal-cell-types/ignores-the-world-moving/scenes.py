"""Chapter 2. COLOR MAP: BLUE ganglion cells; YELLOW excitation/light;
GREY inhibition/outlines; ORANGE recording; PURPLE retina; GOLD caveats;
TEAL brand; TEXT neutral labels. All spike counts are illustrative lesson data.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'


def heading(text,color=TEXT):
    return T(text,30,color,font=TITLE_FONT).move_to([0,3.48,0])


def arr(a,b,color=GREY,w=5,buff=.08):
    return Arrow(a,b,buff=buff,color=color,stroke_width=w,tip_length=.2,
                 max_tip_length_to_length_ratio=.35,max_stroke_width_to_length_ratio=12)


def brake(a,b,dashed=False):
    a=np.array(a,dtype=float); b=np.array(b,dtype=float)
    d=b-a; p=np.array([-d[1],d[0],0]); p=p/np.linalg.norm(p)*.32
    line=DashedLine(a,b,color='#B5BFCD',stroke_width=6,dash_length=.16,dashed_ratio=.65) if dashed else Line(a,b,color='#B5BFCD',stroke_width=6)
    return VGroup(line,Line(b-p,b+p,color='#B5BFCD',stroke_width=8))


def gcell(color=BLUE,s=1):
    soma=Circle(radius=.28,stroke_color=color,stroke_width=4,fill_color=color,fill_opacity=.35)
    parts=[soma]
    for dx in (-.35,0,.35):
        parts.extend([Line([dx*.4,.26,0],[dx*1.2,.95,0],color=color,stroke_width=4),
          Line([dx*1.2,.95,0],[dx*1.2-.15,1.25,0],color=color,stroke_width=3),
          Line([dx*1.2,.95,0],[dx*1.2+.15,1.25,0],color=color,stroke_width=3)])
    parts.append(Line([.28,0,0],[1.4,0,0],color=color,stroke_width=4))
    return VGroup(*parts).scale(s)


def raster(n=0,y=-2.85):
    base=Line([-5.7,y,0],[5.7,y,0],color=BLUE,stroke_width=3)
    ticks=VGroup(*[Line([x,y,0],[x,y+.38,0],color=BLUE,stroke_width=3) for x in np.linspace(-5.4,5.4,n)])
    labels=VGroup(T('W3 spikes',26,BLUE).move_to([-4.6,-3.45,0]),
       T('illustrative, schematic',26,GREY).move_to([2.9,-3.45,0]))
    return VGroup(base,ticks,labels)


def texture(offset=0):
    pts=[]
    for y in np.arange(-2.55,2.56,.34):
        for x0 in np.arange(-3.8,3.81,.42):
            x=(x0+offset+3.8)%7.6-3.8
            if 2.23<np.hypot(x/1.3,y)<2.74:
                pts.append(Line([x,y+.24,0],[x,y+.36,0],color=GREY,stroke_width=4))
    return VGroup(*pts)


def field():
    ring=Annulus(inner_radius=2.2,outer_radius=2.85,color=GREY,fill_opacity=.3).stretch(1.3,0).shift(UP*.3)
    centre=Circle(radius=1.75,color=BLUE,stroke_width=3).shift(UP*.5)
    cell=gcell(s=1.5); cell.shift(np.array([0,-.7,0])-cell[0].get_center())
    patch=VGroup(*[Dot([x,y,0],radius=.045,color=YELLOW) for x in np.arange(-1.25,-.74,.125) for y in np.arange(.45,1.06,.15)])
    return VGroup(ring,texture(),centre,patch,cell,T('W3',26,BLUE).move_to([-.85,-.65,0]))


def field_labels():
    return VGroup(T('centre',26,BLUE).move_to([4.7,.7,0]),Line([3.9,.7,0],[1.35,.7,0],color=BLUE),
      T('distant\nsurround',26,GREY).move_to([-5.05,1.7,0]),Line([-4.1,1.7,0],[-3.05,1.7,0],color=GREY),
      T('far outside',26,GREY).move_to([4.8,2.2,0]),Line([3.9,2.2,0],[2.8,2.2,0],color=GREY))


def still_tag(f):
    edge=f[0].get_right()
    return VGroup(T('still',26,GREY).move_to(edge+RIGHT*1.2+DOWN*2),
                  Line(edge+RIGHT*.7+DOWN*1.85,f[0].get_center()+[3.25,-1.3,0],color=GREY,stroke_width=3))


def move_field(scene,f,whole=False,seconds=2.5):
    c=f[2].get_center()
    cues=[arr(c+[-1,-2,0],c+[1.1,-2,0],YELLOW)]
    if whole: cues.append(arr(c+[-1,2,0],c+[1.1,2,0],GREY))
    else: cues.append(still_tag(f))
    scene.add(*cues)
    anim=[f[3].animate.shift(RIGHT*2)]
    if whole:
        shift=f[0].get_center()-np.array([0,.3,0])
        anim.append(UpdateFromAlphaFunc(f[1],lambda m,a:m.become(texture(2*a).shift(shift))))
    scene.play(*anim,run_time=seconds,rate_func=linear)

def prediction():
    f=field(); f[3].shift(RIGHT*2)
    return VGroup(f,raster(),heading('Predict • centre only: what would it do?',YELLOW))


def inputs():
    on=chip('ON',YELLOW,34).move_to([-4,1.25,0]); off=chip('OFF',YELLOW,34).move_to([-4,-1.25,0])
    w=gcell(s=2.25).move_to([2,.3,0]); name=T('W3',30,BLUE).move_to([2,-2.1,0])
    arrows=VGroup(arr(on.get_right(),[-.3,.3,0],YELLOW,6),arr(off.get_right(),[-.3,.3,0],YELLOW,6),arr([-.3,.3,0],[.7,.3,0],YELLOW,13))
    return VGroup(on,off,w,name,arrows)


def lightstep(up=True):
    y=1.25 if up else -1.25
    points=[[-5.7,y-.25,0],[-5.3,y-.25,0],[-5.3,y+.25,0],[-4.9,y+.25,0]]
    if not up: points=[[x,2*y-yy,z] for x,yy,z in points]
    return VGroup(VMobject(color=YELLOW,stroke_width=4).set_points_as_corners(points),T('light ↑' if up else 'light ↓',26,YELLOW).move_to([-4,y-.85,0]))


def circuit():
    source=chip('excitation',YELLOW,28).move_to([-4.7,.1,0])
    w=gcell(s=2.3).move_to([2.1,.3,0]); wl=T('W3',30,BLUE).move_to([2,-2.1,0])
    link=arr(source.get_right(),[.8,-.8,0],YELLOW,8)
    surround=chip('surround',GREY,28).move_to([-4.5,2.2,0])
    return VGroup(source,w,wl,link,surround)


def wide():
    soma=Circle(radius=.35,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([-4,.8,0])
    branches=VGroup()
    for dest in ([4.6,2.2,0],[4.8,.5,0],[4.4,-1.4,0]):
        mid=np.array([-.8,(dest[1]+.8)/2,0])
        branches.add(Line([-3.65,.8,0],mid,color=GREY,stroke_width=5),Line(mid,dest,color=GREY,stroke_width=4))
        for frac in (.35,.7):
            p=mid+(np.array(dest)-mid)*frac
            branches.add(Line(p,p+np.array([.7,.65,0]),color=GREY,stroke_width=3),Line(p,p+np.array([.6,-.55,0]),color=GREY,stroke_width=3))
    return VGroup(soma,branches)


def relay():
    b=chip('bipolar cells',GREY,30).move_to([-4,2.35,0])
    v=gcell(YELLOW,1.4); v.shift(np.array([-1,0,0])-v[0].get_center())
    w=gcell(s=1.75); w.shift(np.array([3,-1.65,0])-w[0].get_center())
    links=VGroup(arr([-2.8,2.2,0],[-1.4,1.7,0],YELLOW,6),arr([1,.0,0],[2.7,.5,0],YELLOW,6))
    direct=VGroup(DashedLine([-2.7,2.5,0],[5.6,2.5,0],color=GREY),DashedLine([5.6,2.5,0],[5.6,.7,0],color=GREY),arr([5.6,.7,0],[3.6,.55,0],GREY)).set_opacity(.55)
    labels=VGroup(T('VG3 amacrine cell',28,YELLOW).move_to([-1,-1,0]),T('W3',30,BLUE).move_to([3,-2.6,0]))
    return VGroup(b,v,w,links,direct,labels)


def sky():
    box=Rectangle(width=11,height=4.6,stroke_color=GREY,fill_color='#ADB9CC',fill_opacity=1).move_to([0,.35,0])
    ground=Rectangle(width=10.9,height=1,stroke_width=0,fill_color='#596474',fill_opacity=1).move_to([0,-1.42,0])
    tex=VGroup(*[Polygon([x,-1.8,0],[x+.4,-.7-(i%3)*.15,0],[x+.8,-1.8,0],stroke_width=0,fill_color='#303A49',fill_opacity=1) for i,x in enumerate(np.arange(-5.3,4.7,.9))])
    shape=Polygon([-1,1.5,0],[0,1.05,0],[1,1.5,0],[.25,.65,0],[0,.8,0],[-.25,.65,0],stroke_color=BG,fill_color=BG,fill_opacity=1).shift(LEFT*2)
    return VGroup(box,ground,tex,shape)


def slide_sky(scene,s,seconds=2.5,extra=(),distance=2.2):
    # Finite viewport; terrain is redrawn as a wrapped landscape, not drifting outside the frame.
    initial=s[2].copy()
    def shifted(m,a):
        g=initial.copy()
        for p in g:
            x=p.get_center()[0]+distance*a
            if x>s[0].get_right()[0]-.2: x-=s[0].width-.4
            p.set_x(x)
        clipped=VGroup(*[Intersection(p,s[0],stroke_width=0,fill_color=p.get_fill_color(),fill_opacity=1) for p in g])
        m.become(clipped)
    scene.play(UpdateFromAlphaFunc(s[2],shifted),s[3].animate.shift(RIGHT*distance),*extra,run_time=seconds,rate_func=linear)


def jamb():
    body=Circle(radius=.38,color=BLUE,fill_opacity=.35).move_to([-3,-.6,0]); dend=VGroup()
    for y in (.1,1,1.9):
        dend.add(Line([-2.8,-.5,0],[.3,y,0],color=BLUE,stroke_width=4),Line([.3,y,0],[2.9,y+.25,0],color=BLUE,stroke_width=3),Line([.3,y,0],[2.7,y-.3,0],color=BLUE,stroke_width=3))
    return VGroup(body,dend,Line([-3.4,-.6,0],[-4.8,-.6,0],color=BLUE,stroke_width=4))


class S00Title(TitleCard):
    TITLE='The Cell That Ignores the World Moving'
    LESSON='Parallel Channels Out of the Eye'
    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',26,TEAL)
        lesson=T(self.LESSON,26,GREY)
        title=T('The Cell That Ignores\nthe World Moving',44,font=TITLE_FONT,line_spacing=1,should_center=True)
        g=VGroup(brand,lesson,title,Line(LEFT*1.4,RIGHT*1.4,color=GOLD)).arrange(DOWN,buff=.45).move_to(ORIGIN)
        self.play(FadeIn(g),run_time=.7); self.finish()


class S01Q(SpokenScene):
    def construct(self):
        left=sky().scale(.53).move_to([-3.1,0,0]); right=sky().scale(.53).move_to([3.1,0,0])
        # Taller than the original postcard panels.
        left.stretch(1.3,1); right.stretch(1.3,1)
        self.add(heading('How could one cell tell a moving object\nfrom a moving world?').shift(DOWN*.35),left,right,T('object moves',28).move_to([-3.1,-2.3,0]),T('world moves',28).move_to([3.1,-2.3,0]))
        self.at('a moving object'); self.play(left[3].animate.shift(RIGHT*1.3),run_time=1)
        self.at('a moving world'); slide_sky(self,right,1,distance=1.1)
        self.finish()


class S02Who(SpokenScene):
    def construct(self):
        cell=gcell(s=2).move_to([0,0,0]); end=cell[0].get_center()
        self.add(Ellipse(width=10,height=5.2,color=GREY),Rectangle(width=7.8,height=3.9,color=PURPLE,fill_opacity=.12),cell)
        self.at('Zhang and colleagues'); self.play(FadeIn(heading('Zhang and colleagues, 2012')),run_time=.4)
        self.at('recorded from'); self.play(Create(Line([4.8,2.5,0],end,color=ORANGE,stroke_width=6)),FadeIn(Dot(end,color=ORANGE,radius=.1)),run_time=.5)
        self.at('isolated mouse retina'); self.play(FadeIn(T('W3 cells • isolated mouse retina',28,BLUE).move_to([0,-3,0])),run_time=.4); self.finish()


class S03Spot(SpokenScene):
    def construct(self):
        c=gcell(s=2).move_to([2,.4,0]); spot=Circle(radius=1,color=YELLOW,fill_color=YELLOW,fill_opacity=.1).move_to([-2.7,.5,0]); r=raster()
        self.add(c,spot,r,heading('Local light change'),T('light over receptive field',26,YELLOW).move_to([-2.7,2.1,0]),arr([-1.5,.5,0],[.3,.5,0],YELLOW))
        self.at('Brighten a small spot'); self.play(spot.animate.set_fill(opacity=.85),FadeIn(T('brighter ↑',30,YELLOW).move_to([-2.7,-1.1,0])),run_time=.6)
        self.at('and it fires'); self.play(Create(r[1].become(raster(8)[1])),run_time=.6); self.finish()


class S04Dim(SpokenScene):
    def construct(self):
        c=gcell(s=2).move_to([2,.4,0]); spot=Circle(radius=1,color=YELLOW,fill_color=YELLOW,fill_opacity=.85).move_to([-2.7,.5,0]); r=raster()
        self.add(c,spot,r,heading('Local light change'),T('light over receptive field',26,YELLOW).move_to([-2.7,2.1,0]),arr([-1.5,.5,0],[.3,.5,0],YELLOW))
        self.at('Dim the same spot'); self.play(spot.animate.set_fill(opacity=.03),FadeIn(T('dimmer ↓',30,YELLOW).move_to([-2.7,-1.1,0])),run_time=.6)
        self.at('it fires again'); self.play(Create(r[1].become(raster(8)[1])),run_time=.6); self.finish()


class S05Onoff(SpokenScene):
    def construct(self):
        g=inputs(); self.add(g[2],g[3],heading('Two signs of local light change'))
        self.at('from the on'); self.play(FadeIn(g[0]),GrowArrow(g[4][0]),run_time=.4)
        self.at('light goes up'); self.play(FadeIn(lightstep()),run_time=.4)
        self.at('from the off'); self.play(FadeIn(g[1]),FadeIn(lightstep(False)),GrowArrow(g[4][1]),GrowArrow(g[4][2]),run_time=.5); self.finish()


class S06That(SpokenScene):
    def construct(self):
        g=inputs(); self.add(g,lightstep(),lightstep(False))
        self.at('either sign excites it'); self.play(FadeIn(heading('Either sign of local change excites W3',YELLOW)),run_time=.4)
        self.at('The two inputs add'); self.play(g[4][2].animate.set_stroke(width=20),FadeIn(T('ON and OFF inputs add, not cancel',30,YELLOW).move_to([0,-3,0])),run_time=.6); self.finish()


class S07Obj(SpokenScene):
    def construct(self):
        f=field(); labels=field_labels(); self.add(f,labels[:2],raster(),heading('Object moves; background stays still'))
        self.at('patch moves'); move_field(self,f,seconds=2.5)
        self.at('background stays still'); self.wait(.4)
        self.at('a wide ring'); self.play(FadeIn(labels[2:]),run_time=.4); self.finish()


class S08Many(SpokenScene):
    def construct(self):
        f=field(); f[3].shift(RIGHT*2); r=raster(); h=heading('Object moves; background stays still'); self.add(f,r,field_labels(),h)
        self.at('fires many spikes'); self.play(Create(r[1].become(raster(40)[1])),run_time=.7)
        self.at('Say 40'); self.play(Transform(h,heading('≈40 spikes • object moves',YELLOW)),run_time=.3); self.finish()


class S09Scene(SpokenScene):
    def construct(self):
        f=field(); self.add(f,raster(),heading('Whole scene moves'))
        self.at('whole scene moves together'); move_field(self,f,True,2.5)
        self.at('exactly the same stimulus'); self.play(FadeIn(T('centre stimulus\nunchanged',26,YELLOW).move_to([4.9,0,0])),run_time=.4); self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        p=prediction(); h=heading('Whole scene moves'); self.add(p[0],p[1],h)
        self.at('Predict'); self.play(Transform(h,p[2]),run_time=.3)
        self.at('If the cell listened'); self.add(T('?',42,YELLOW).move_to([0,-2.65,0])); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction())
        q=T('?',42,YELLOW).move_to([0,-2.65,0]); self.add(q)
        for _ in range(5): self.play(q.animate.set_opacity(.25),run_time=.5); self.play(q.animate.set_opacity(1),run_time=.5)


class S12Reveal(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p[0],p[1]); predicted=VGroup(*[Line(t.get_start(),t.get_end(),color='#AAB4C2',stroke_width=4) for t in raster(40)[1]])
        cap=heading('Predicted: just as much • ≈40',GREY)
        self.at('It would fire just as much'); self.play(FadeIn(predicted),FadeIn(cap),run_time=.4)
        self.at('It does not'); self.play(predicted.animate.set_opacity(.3),FadeOut(cap),run_time=.25)
        self.at('nearly silent'); self.play(Create(p[1][1].become(raster(3)[1])),FadeIn(heading('Observed: ≈3 • grey ticks: ≈40 predicted',BLUE)),run_time=.5)
        self.at('Say three spikes'); self.wait(.3); self.finish()


class S13Surround(SpokenScene):
    def construct(self):
        f=field(); f[3].shift(RIGHT*2); self.add(f,raster(3),heading('Surround motion suppresses W3'))
        self.at('far out in the surround'); self.play(UpdateFromAlphaFunc(f[1],lambda m,a:m.become(texture(2*a))),run_time=1.4)
        self.at('must be silencing it'); self.play(Create(brake([-3,.5,0],f[4][0].get_top())),run_time=.6); self.finish()


class S14Two(SpokenScene):
    def construct(self):
        g=circuit(); self.add(g,heading('Suppression at two sites'))
        pre=g[3].point_from_proportion(.82)
        soma=g[1][0].get_center()
        premark=Circle(radius=.34,color=GOLD).move_to(pre)
        postmark=Circle(radius=.74,color=GOLD).move_to(soma)
        before=T('before the cell\n(presynaptic)',28,GOLD).move_to([-1.7,-2.35,0])
        on=T('on the cell\n(postsynaptic)',28,GOLD).move_to([4.6,-2.35,0])
        self.at('two places at once')
        self.play(Create(premark),Create(postmark),Create(Line(before.get_top()+UP*.1,premark.get_bottom(),color=GOLD)),
          Create(Line(on.get_top()+UP*.1,postmark.get_right(),color=GOLD)),FadeIn(before),FadeIn(on),run_time=.6); self.finish()

class S15Pre(SpokenScene):
    def construct(self):
        g=circuit(); self.add(g,heading('Presynaptic suppression'))
        self.at('presynaptic'); self.play(Create(brake([-3.4,2.2,0],[-1.7,-.45,0])),run_time=.4)
        self.at('excitation is suppressed')
        self.play(Transform(g[3],VGroup(arr(g[0].get_right(),[-1.7,-.45,0],YELLOW,10),arr([-1.65,-.45,0],[.8,-.8,0],YELLOW,3))),FadeIn(T('full input',26,YELLOW).move_to([-4,-1.25,0])),FadeIn(T('less excitation',26,YELLOW).move_to([-.25,-1.6,0])),run_time=.6)
        self.at('less of it arrives'); dot=Dot(g[0].get_right(),radius=.14,color=YELLOW); self.add(dot)
        self.play(dot.animate.move_to([-1.7,-.45,0]),run_time=.8); self.play(dot.animate.scale(.4).move_to([.8,-.8,0]),run_time=1.2); self.remove(dot); self.finish()


class S16Post(SpokenScene):
    def construct(self):
        g=circuit(); g[3].set_stroke(width=3); self.add(g,T('less excitation',26,YELLOW).move_to([-1,-1.5,0]),heading('Postsynaptic inhibition'))
        self.at('postsynaptic'); self.wait(.3)
        self.at('Inhibition lands'); soma=g[1][0].get_top(); dend=g[1][6].get_center()
        route=VGroup(Line(g[4].get_right(),[4,2.2,0],color='#B5BFCD',stroke_width=6),brake([4,2.2,0],soma),brake([.2,2.2,0],dend))
        self.play(Create(route),run_time=.8); self.finish()


class S17Wf(SpokenScene):
    def construct(self):
        w=wide(); cell=gcell(s=1.5).move_to([2.4,-.9,0]); self.add(w,cell,T('W3',28,BLUE).move_to(cell[0].get_center()+[-.9,-.3,0]),heading('Wide processes span surround → centre'))
        self.at('in other species'); self.play(FadeIn(T('Similar cells • other species',28,GREY).move_to([0,-2.6,0])),run_time=.4)
        self.at('proposed'); self.play(Create(brake(w[1][0].get_end(),cell[0].get_top(),True)),run_time=.5)
        self.at('amacrine cells'); self.play(FadeIn(T('wide-field amacrine • proposed source',28,GREY).move_to([0,-3.35,0])),run_time=.4); self.finish()


class S18Vg3(SpokenScene):
    def construct(self):
        r=relay(); self.add(r[0],r[2],r[4],r[5][1])
        self.at('Where does the excitation come from'); self.play(FadeIn(heading('Where does excitation come from?')),run_time=.4)
        self.at('does not come straight')
        unknown=chip('?',YELLOW,36).move_to([-1,.4,0])
        path=VGroup(arr(r[0].get_bottom(),unknown.get_top(),YELLOW,6),arr(unknown.get_right(),[2.7,.5,0],YELLOW,6))
        note=T('Much arrives indirectly',28,YELLOW).move_to([-3,-1.3,0])
        bracket=VGroup(Line([-4.8,-.7,0],[-1,-.7,0],color=YELLOW),Line([-1,-.7,0],unknown.get_bottom(),color=YELLOW))
        self.play(FadeIn(note),Create(path),FadeIn(unknown),Create(bracket),run_time=.4); self.finish()


class S19Vg3b(SpokenScene):
    def construct(self):
        r=relay(); self.add(r[0],r[2],r[4],r[5][1],heading('Excitation through an interneuron'))
        self.at('It arrives through'); self.play(FadeIn(r[1]),Create(r[3]),FadeIn(r[5][0]),run_time=.6)
        self.at('an excitatory amacrine cell'); self.play(FadeIn(T('excitatory',28,YELLOW).move_to([-1,-1.7,0])),FadeIn(T('Krishnaswamy and colleagues, 2015',26,TEXT).move_to([0,-3.35,0])),run_time=.4); self.finish()


class S20Inter(SpokenScene):
    def construct(self):
        r=relay(); self.add(r,heading('Excitation is routed through an interneuron'),T('excitatory',28,YELLOW).move_to([-1,-1.7,0]))
        self.at('circuit that builds the selection'); self.play(Create(SurroundingRectangle(r,color=GOLD,buff=.2)),FadeIn(T('Circuit before the ganglion cell',28,GOLD).move_to([0,-3.35,0])),run_time=.5)
        self.at('before the ganglion cell'); self.play(Indicate(r[2],color=BLUE),run_time=.4); self.finish()


class S20bTwo(SpokenScene):
    def construct(self):
        v=gcell(YELLOW,1.45); v.shift(np.array([-3.2,.7,0])-v[0].get_center())
        # Axon runs down to a single synapse above the W3 dendrites.
        v[-1].put_start_and_end_on(v[0].get_bottom(),[-3.2,.08,0])
        w=gcell(s=1.6); w.shift(np.array([-3.2,-2.3,0])-w[0].get_center())
        wf=wide().scale(.85).stretch(.78,0).move_to([2.5,.6,0])
        b=chip('bipolar',GREY,26).move_to([-5.1,2.7,0])
        direct=VGroup(DashedLine([-5.7,2.3,0],[-5.7,-2.3,0],color=GREY),arr([-5.7,-2.3,0],[-3.7,-2.3,0],GREY)).set_opacity(.45)
        self.add(v,w,b,direct,arr([-4.5,2.7,0],[-3.7,2.4,0],YELLOW),heading('Two amacrine cells, two jobs'),T('VG3 amacrine cell',26,YELLOW).move_to([-2,2.8,0]),T('W3',28,BLUE).move_to([-3.2,-3.1,0]))
        self.at('VG3 brings excitation in'); self.play(GrowArrow(arr(v[-1].get_end(),[-3.2,-.78,0],YELLOW)),FadeIn(T('excitation in',26,YELLOW).move_to([-4.7,.15,0])),run_time=.5)
        self.at('Wide field cells'); self.play(FadeIn(wf),FadeIn(T('wide-field amacrine',28,GREY).move_to([3.2,2.9,0])),run_time=.5)
        self.at('the proposed break'); self.play(Create(brake(wf[1][2].get_end(),w[0].get_right(),True)),FadeIn(T('proposed brake\n(other species)',28,GREY).move_to([3.4,-2.5,0])),run_time=.5); self.finish()

class S21Question(SpokenScene):
    def construct(self):
        f=field().shift(LEFT*.8); h=heading('W3 asks…',BLUE); self.add(f,raster(),h)
        self.at('answers one question'); self.wait(.3)
        self.at('Is something small'); self.add(T('Is something small\nmoving differently\nfrom everything\nelse?',26,YELLOW).move_to([4.7,.3,0])); move_field(self,f,seconds=2); self.finish()


class S22Scene(SpokenScene):
    def construct(self):
        s=sky(); r=raster(); self.add(s,r,heading('Whole image moves together'))
        self.at('eye or head turns'); slide_sky(self,s,2.5)
        self.play(Create(r[1].become(raster(3)[1])),run_time=.5); self.finish()


class S23Hawk(SpokenScene):
    def construct(self):
        s=sky(); r=raster(); self.add(s,r)
        self.at('proposed these cells'); self.play(FadeIn(heading('Proposed alarm neuron',GOLD)),run_time=.4)
        self.at('overhead predators'); self.play(s[3].animate.shift(RIGHT*3.8),Create(r[1].become(raster(40)[1])),run_time=2.5,rate_func=linear); self.finish()


class S24Hedge(SpokenScene):
    def construct(self):
        c=gcell(s=1.55).move_to([0,.4,0]); end=c[0].get_center()
        self.add(heading('Hypothesis',GOLD),Ellipse(width=9,height=3.9,color=GREY).move_to([0,.5,0]),Rectangle(width=6,height=2.9,color=PURPLE,fill_opacity=.12).move_to([0,.5,0]),c,Line([3.7,2.3,0],end,color=ORANGE,stroke_width=5),T('Tested in isolated retina',28).move_to([0,-2.1,0]),T('Behavioral test of necessity: not done',28,GOLD).move_to([0,-3.1,0]))
        self.at('That is a hypothesis'); self.wait(.3)
        self.at('experiments used isolated retina'); self.play(Indicate(c),run_time=.5)
        self.at('no behavioral test'); self.play(Indicate(self.mobjects[-1],color=GOLD),run_time=.5); self.finish()


class S25Jamb(SpokenScene):
    def construct(self):
        c=jamb(); self.add(c)
        self.at('A second channel'); self.play(FadeIn(heading('JAM-B • Kim and colleagues, 2008',BLUE)),run_time=.4)
        self.at('an off'); self.play(FadeIn(chip('OFF',YELLOW,28).move_to([-3,-2.1,0])),run_time=.35)
        self.at('lopsided dendritic arbor'); self.play(Indicate(c[1],color=PURPLE,scale_factor=1.04),run_time=.6); self.finish()


class S26Jamb2(SpokenScene):
    def construct(self):
        c=jamb(); bar=Line([-3.5,-1.1,0],[-3.5,2.2,0],color=YELLOW,stroke_width=9)
        self.add(c,heading('Preferred direction: soma → dendrites'),T('soma',28,BLUE).move_to([-4.7,-1.4,0]),Line([-4,-1.25,0],[-3.2,-.85,0],color=BLUE),T('dendrites',28,BLUE).move_to([3.9,1.8,0]),arr([-2.7,2.8,0],[2.7,2.8,0],YELLOW),T('illustrative, schematic',26,GREY).move_to([2.5,-3.4,0]))
        r=raster(); r[2].become(T('JAM-B spikes',26,BLUE).move_to([-4.5,-3.4,0])); self.add(r)
        self.at('preferred movement'); self.play(Create(bar),run_time=.3)
        self.at('from the cell body'); self.play(bar.animate.shift(RIGHT*.5),run_time=.4)
        self.at('toward the dendrites'); self.play(bar.animate.shift(RIGHT*5.8),Create(r[1].become(raster(8)[1])),run_time=2.5,rate_func=linear)
        self.wait(1.2); self.finish()


class S27Take(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=8.5,height=5.9,color=PURPLE).move_to([-2,-.2,0])
        v=gcell(YELLOW,1.1); v.shift(np.array([-4.5,1,0])-v[0].get_center())
        w=gcell(s=1.35); w.shift(np.array([-.4,.25,0])-w[0].get_center())
        wf=wide().scale(.72).move_to([-2.5,-1.1,0])
        others=VGroup()
        for y in (-1.35,-2.45):
            c=gcell(s=.62); c.shift(np.array([.4,y,0])-c[0].get_center()); others.add(c)
        self.add(box,v,w,wf,T('retina',28,PURPLE).move_to([-5.4,2.6,0]),T('VG3',28,YELLOW).move_to([-4.5,.35,0]),T('W3',28,BLUE).move_to([.4,.85,0]),T('proposed brake',26,GREY).move_to([-3.6,-2.85,0]),arr(v[-1].get_end(),[-.65,1.65,0],YELLOW),brake(wf[1][0].point_from_proportion(.4),w[0].get_left(),True))
        self.at('filter is built inside the retina'); self.play(FadeIn(heading('The filter is built inside the retina')),run_time=.4)
        self.at('scene motion this cell ignores')
        quiet=arr(w[-1].get_end(),[6.3,.25,0],GREY,3,buff=0)
        outputs=VGroup(*[arr(c[-1].get_end(),[6.3,c[0].get_y(),0],BLUE,buff=0) for c in others])
        self.play(FadeIn(quiet),FadeIn(others),FadeIn(outputs),FadeIn(T('W3 quiet',26,GREY).move_to([4.5,.85,0])),FadeIn(T('other channels',26,BLUE).move_to([4.5,-3.1,0])),FadeIn(T('scene motion →',28,YELLOW).move_to([4.5,-.8,0])),run_time=.5)
        self.at('still travels in other channels'); pulses=VGroup(*[Dot(c[-1].get_end(),color=YELLOW) for c in others]); self.add(pulses)
        self.play(*[d.animate.move_to([6.1,d.get_y(),0]) for d in pulses],run_time=1.4); self.finish()

class S28End(EndCard):
    LINE='The filter is built inside the retina.'
