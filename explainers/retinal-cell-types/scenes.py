"""Many Maps, Not One Picture — review redraw.
COLOR MAP: GOLD ganglion output / example type 1 / brightness channel;
TEAL example type 2 / small-object channel; VIOLET example type 3 / direction;
SLATE bipolar and amacrine circuits; CORAL a feature combined in the brain;
GREY anatomy and absent information. Meadow colors are scene content only.
All mosaics and receptive filters are illustrative models, not measured data.
The sample values and coverage counts are computed from the drawn geometry.
"""
import numpy as np
from bp_style import *

VIOLET = '#B58CD9'
CORAL = '#F08C82'
SLATE = '#A5B2C8'
COLORS = (GOLD, TEAL, VIOLET)
CENTER = np.array([-2.65, -.12, 0.])
R = 2.88
# Broad, fingered wings, compact body, small head and a fanned tail.
BIRD = np.array([[-1.0,.13],[-.87,.28],[-.91,.40],[-.72,.31],[-.73,.45],
 [-.55,.34],[-.33,.23],[-.11,.15],[-.08,.37],[.02,.43],[.10,.34],
 [.12,.15],[.35,.24],[.61,.38],[.77,.47],[.74,.31],[.94,.40],
 [.89,.23],[1.04,.18],[.76,.03],[.38,-.04],[.12,-.03],
 [.13,-.24],[.25,-.44],[.02,-.37],[-.20,-.44],[-.11,-.22],[-.13,-.03],[-.42,-.03],[-.76,.02]])


def label(s, p, color=TEXT, size=30):
    return T(s, size, color).move_to(p)


def heading(s, color=TEXT):
    return label(s, [0,3.27,0], color, 34)


def arrow(a,b,c=GREY):
    return Arrow(a,b,buff=.08,color=c,stroke_width=4,tip_length=.18)


def hawk(color=BG):
    return Polygon(*[[x,y,0] for x,y in BIRD],color=color,fill_opacity=1,stroke_width=0)


def field(w=7.3,h=5.3):
    sky=Rectangle(width=w,height=h*.48,stroke_width=0,fill_color='#91ACBA',fill_opacity=1).move_to([0,h*.26,0])
    grass=Rectangle(width=w,height=h*.52,stroke_width=0,fill_color='#496D51',fill_opacity=1).move_to([0,-h*.24,0])
    blades=VGroup(*[Line([x,-h*.40,0],[x+.1,-h*.28,0],color='#81916C',stroke_width=2) for x in np.linspace(-w*.46,w*.46,20)])
    bird=hawk().scale(w*.22).move_to([0,-h*.18,0])
    return VGroup(sky,grass,blades,bird,Rectangle(width=w,height=h,color=GREY))


def inside_bird(x,y):
    # Ray casting against exactly the same silhouette drawn by hawk().
    hit=False
    for a,b in zip(BIRD,np.roll(BIRD,-1,axis=0)):
        if (a[1]>y)!=(b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            hit=not hit
    return hit


def intensity(x,y):
    return .08 if inside_bird(x/.95,(y+.36)/.95) else (.83 if y>.03 else .39)


def response(x,y,kind):
    if kind==0:
        surround=np.mean([intensity(x+dx,y+dy) for dx,dy in ((.16,0),(-.16,0),(0,.16),(0,-.16))])
        return np.clip(.5+2.0*(intensity(x,y)-surround),0,1)
    return float(inside_bird(x/.95,(y+.36)/.95))


def filter_panel(kind,w=3.3,h=1.6):
    c=COLORS[kind]
    parts=[Rectangle(width=w,height=h,color=c,fill_color='#272C36',fill_opacity=1)]
    if kind==0:
        # Local center-minus-surround response on the same meadow coordinates.
        nx,ny=40,22
        for x in np.linspace(-1.5,1.5,nx):
            for y in np.linspace(-1,1,ny):
                v=response(x,y,0)
                if abs(v-.5)>.02:
                    parts.append(Rectangle(width=w/nx*1.02,height=h/ny*1.02,stroke_width=0,
                        fill_color=interpolate_color(ManimColor('#525D73'),ManimColor('#F4E6B9'),v),fill_opacity=1).move_to([x*w/3.1,y*h/2.1,0]))
    else:
        parts.append(hawk(c).scale(min(w*.25,h*.60/.87)).move_to([0,-h*.17,0]))
        if kind==2:
            parts.append(arrow([-w*.34,h*.25,0],[w*.34,h*.25,0],c))
    return VGroup(*parts)


def mouse():
    head=Ellipse(width=2.0,height=1.65,color=GREY,fill_color='#313640',fill_opacity=1)
    ears=VGroup(Circle(radius=.48,color=GREY,fill_color=BG,fill_opacity=1).shift(LEFT*.55+UP*.9),Circle(radius=.42,color=GREY).shift(RIGHT*.55+UP*.83))
    nose=Dot([-.93,-.1,0],radius=.12,color=TEXT)
    eye=VGroup(Circle(radius=.24,color=TEXT).shift(LEFT*.3+UP*.2),Dot([-.3,.2,0],radius=.13,color=GOLD))
    whisk=VGroup(*[Line([-.85,-.2,0],[-1.5,y,0],color=GREY) for y in (-.5,-.2,.1)])
    return VGroup(ears,head,nose,eye,whisk)


def tube(x1=.35,x2=5.8,y=0,h=1.6,many=False,plain=False):
    shell=RoundedRectangle(width=x2-x1,height=h,corner_radius=h*.46,color=GREY,stroke_width=3,
        fill_color='#202530',fill_opacity=1).move_to([(x1+x2)/2,y,0])
    lines=VGroup()
    n=43 if many else 3
    for i in range(n):
        off=(i/(n-1)-.5)*h*.73
        def point(t,off=off,i=i):
            # Smooth, convergent axon paths inside a bounded anatomical tube.
            return [x1+.16+(x2-x1-.32)*t,y+off*(.65+.3*np.sin(PI*t))+.045*np.sin(TAU*t+i)*np.sin(PI*t),0]
        lines.add(ParametricFunction(point,t_range=[0,1],color=GREY if plain else COLORS[i%3],stroke_width=1.5 if many else 5))
    return VGroup(shell,lines)


def retina():
    # All layer labels sit to the right of their actual cells, outside the bands.
    ys=[2.1,.6,-.65,-2.1]
    bands=VGroup(*[RoundedRectangle(width=8.4,height=.7,corner_radius=.12,color=GREY,stroke_opacity=.35,fill_color=GREY,fill_opacity=.04).move_to([-1.65,y,0]) for y in ys])
    photo=VGroup(*[RoundedRectangle(width=.24,height=.6,corner_radius=.10,color=GREY).move_to([x,2.1,0]) for x in (-5,-3.4,-1.8,-.2,1.4)])
    bp=VGroup(*[VGroup(Line([x,1.72,0],[x,-.1,0],color=SLATE,stroke_width=3),Dot([x,.6,0],radius=.14,color=SLATE)) for x in (-5,-3.4,-1.8,-.2,1.4)])
    am=VGroup(*[VGroup(Dot([x,-.65,0],radius=.14,color=SLATE),Line([x-.6,-.65,0],[x+.6,-.65,0],color=SLATE,stroke_width=3)) for x in (-4.2,-1,1)])
    gc=VGroup(*[VGroup(Dot([x,-2.1,0],radius=.19,color=GOLD),Line([x,-1.9,0],[x,-1.05,0],color=GOLD),Line([x-.4,-1.1,0],[x+.4,-1.1,0],color=GOLD)) for x in (-5,-3.4,-1.8,-.2,1.4)])
    ax=VGroup(*[VMobject(color=GOLD,stroke_width=2).set_points_as_corners([[x,-2.27,0],[x,-2.65-j*.06,0],[2.8,-2.65-j*.06,0],[3.5,-2.3-j*.06,0],[5.8,-2.3-j*.06,0]]) for j,x in enumerate((-5,-3.4,-1.8,-.2,1.4))])
    shell=RoundedRectangle(width=2.6,height=.72,corner_radius=.25,color=GREY).move_to([4.55,-2.42,0])
    return VGroup(bands,photo,bp,am,gc,VGroup(shell,ax))


def retina_labels():
    labs=VGroup(*[label(s,[4.4,y,0],c,28) for s,y,c in [('photoreceptors',2.1,GREY),('bipolar cells',.6,SLATE),('amacrine cells',-.65,SLATE),('ganglion cells',-1.9,GOLD)]])
    labs[3]=VGroup(labs[3],Line([2.65,-2.1,0],[3.0,-1.9,0],color=GOLD,stroke_width=2))
    return labs


def positions(kind=0):
    rng=np.random.default_rng(714+kind)
    pts=[]
    step=(.84,1.12,.67)[kind]
    for r in range(-5,6):
        for col in range(-5,6):
            x=(col+.5*(r%2))*step
            y=r*step*.866
            x,y=x*(1+.085*x),y*(1+.085*x)
            x,y=np.array([x,y])+rng.uniform(-.09,.09,2)*step
            if kind: x+=.13*kind; y-=.11*kind
            if np.hypot(x,y)<R-.23:
                pts.append(np.array([x,y,0.]))
    return pts


def sheet_base():
    outline=Circle(radius=R,color=GREY,fill_color=GREY,fill_opacity=.035).move_to(CENTER)
    disc=Circle(radius=.15,color=TEXT,fill_color=GREY,fill_opacity=.5).move_to(CENTER+[2.25,0,0])
    # Orientation mark persists through every top view.
    return VGroup(outline,disc)


def dots(kind=0,sampled=False):
    c=COLORS[kind]
    return VGroup(*[Dot(CENTER+p,radius=.10 if kind!=2 else .082,color=c,
        fill_opacity=(.20+.8*response(p[0]*.53,p[1]*.38,kind)) if sampled else 1) for p in positions(kind)])


def links(kind=0):
    pts=positions(kind); pairs=set()
    for i,p in enumerate(pts):
        j=min((j for j in range(len(pts)) if i!=j),key=lambda j:np.linalg.norm(p-pts[j]))
        pairs.add(tuple(sorted((i,j))))
    return VGroup(*[Line(CENTER+pts[i],CENTER+pts[j],buff=.13,color=COLORS[kind],stroke_width=1.5,stroke_opacity=.45) for i,j in sorted(pairs)])


def arbors(kind=0):
    result=VGroup()
    for p in positions(kind):
        rad=(.88,1.10,.67)[kind]*(1+.085*p[0])
        disk=Circle(radius=rad).move_to(CENTER+p)
        clipped=Intersection(disk,Circle(radius=R).move_to(CENTER),color=COLORS[kind],stroke_width=1,stroke_opacity=.28,fill_color=COLORS[kind],fill_opacity=.035)
        result.add(clipped)
    return result


def key():
    return VGroup(*[VGroup(Dot(radius=.09,color=c),T(f'type {i+1}',28,c)).arrange(RIGHT,buff=.15) for i,c in enumerate(COLORS)]).arrange(RIGHT,buff=.48).move_to([-2.65,-3.28,0])


def maps(sampled=True):
    return VGroup(sheet_base(),dots(0,sampled),dots(1,sampled),dots(2,sampled),key())


def feed(many=False):
    nerve=tube(many=many)
    entries=VGroup()
    for y,off,c in zip((1.6,.2,-1.3),(.55,0,-.55),COLORS):
        edge_x=CENTER[0]+np.sqrt(R*R-(y-CENTER[1])**2)
        entries.add(CubicBezier([edge_x,y,0],[edge_x+.24,y,0],[.1,off,0],[.55,off,0],color=c,stroke_width=4))
    return VGroup(nerve,entries,label('optic nerve',[3.15,-1.38,0],GREY,30))


def predict():
    return VGroup(maps(),feed(),heading('Each type draws one map'),label('So the optic nerve carries…?',[3.1,2.15,0],TEXT,28))


def brain():
    shape=RoundedRectangle(width=3.0,height=4.7,corner_radius=.9,color=GREY,fill_color=GREY,fill_opacity=.07).move_to([4.5,0,0])
    return VGroup(shape,label('brain',[4.5,2.75,0],TEXT,32))


def camera():
    lens=VGroup(RoundedRectangle(width=1.7,height=1.25,corner_radius=.16,color=GREY).move_to([-4.9,-1.5,0]),Circle(radius=.43,color=TEXT).move_to([-4.9,-1.5,0]))
    cable=VMobject(color=GREY,stroke_width=7).set_points_smoothly([[-4,-1.5,0],[-2.8,-1.5,0],[-1.5,-2.3,0],[.1,-1.5,0],[2,-1.5,0]])
    plug=VGroup(Rectangle(width=.55,height=.5,color=TEXT).move_to([2.2,-1.5,0]),Line([2.47,-1.35,0],[2.8,-1.35,0],color=TEXT),Line([2.47,-1.65,0],[2.8,-1.65,0],color=TEXT))
    screen=VGroup(Rectangle(width=2.2,height=1.6,color=GREY).move_to([4.4,-1.5,0]),Line([4.4,-2.3,0],[4.4,-2.7,0],color=GREY),Line([3.8,-2.7,0],[5,-2.7,0],color=GREY))
    return VGroup(lens,cable,plug,screen,label('camera cable',[0,-2.85,0],GREY,30))


def eye_nerve():
    return VGroup(mouse().move_to([-4.4,1.45,0]),tube(-2.8,5.65,1.5,1.05,plain=True),label('optic nerve',[1.4,2.45,0],GREY,30))


class S00Title(TitleCard):
    TITLE='Many Maps, Not One Picture'
    LESSON='Parallel Channels Out of the Eye'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',[0,1.5,0],TEAL,28),
            label(self.LESSON.upper(),[0,.7,0],GREY,28),
            fit(label(self.TITLE,[0,-.25,0],TEXT,49),max_w=12.2),
            Line([-1.4,-1.15,0],[1.4,-1.15,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        f=field().move_to([-2.35,.1,0]); m=mouse().scale(1.25).move_to([3.65,.6,0])
        n=tube(4.0,6.1,.55,.65,plain=True)
        question=label('What does the optic nerve tell the brain?',[0,-3.15,0],TEXT,32)
        self.add(f,m,n,question,label('optic nerve',[4.4,-1.05,0],GREY,28),label('mouse',[3.8,2.65,0],GREY,28))
        self.add(Line([5.65,.2,0],[5.65,-.7,0],color=GREY,stroke_width=2))
        # Continuous glide throughout the spoken scene, entirely within the meadow.
        f[3].shift(LEFT*.9)
        f[3].add_updater(lambda mob,dt: mob.shift(RIGHT*(1.8/(self.narration_s+.4))*dt))
        self.at('What does')
        self.play(Indicate(n[0],color=TEXT,scale_factor=1.04),run_time=.6)
        self.finish()
        f[3].clear_updaters()


class S02Gc(SpokenScene):
    def construct(self):
        r=retina(); self.add(r.copy().set_color(GREY),heading('Retina → optic nerve'),retina_labels()[0])
        self.at('through ganglion cells')
        self.play(FadeIn(r[4]),FadeIn(r[5]),FadeIn(retina_labels()[3]),run_time=.55)
        self.finish()


class S03Out(SpokenScene):
    def construct(self):
        r=retina(); self.add(r,retina_labels()[0],retina_labels()[3],heading('Retina → optic nerve'))
        self.at("retina's only output")
        self.play(FadeIn(label('The retina’s only output neurons',[0,-3.35,0],GOLD,30)),run_time=.35)
        self.at('their axons')
        self.play(Indicate(r[5][1],color=GOLD,scale_factor=1.02),run_time=.4)
        self.at('optic nerve')
        self.play(FadeIn(label('optic nerve',[4.55,-3.05,0],GREY,28)),run_time=.25)
        self.finish()


class S04Cable(SpokenScene):
    def construct(self):
        self.add(eye_nerve(),camera())
        self.at('carry a picture')
        self.play(FadeIn(label('?',[0,-.15,0],TEXT,54)),run_time=.3)
        self.at('like a camera cable')
        self.play(Indicate(self.mobjects[1][1],color=TEXT,scale_factor=1.02),run_time=.45)
        self.finish()


class S05No(SpokenScene):
    def construct(self):
        c=camera(); q=label('?',[0,-.15,0],TEXT,54); self.add(eye_nerve(),c,q)
        self.at('It does not')
        self.play(FadeOut(c),FadeOut(q),run_time=.45)
        tiles=VGroup(*[Dot([-4.9+(i%14)*.76,-.6-(i//14)*.65,0],radius=.14,color=COLORS[i%3]) for i in range(42)])
        self.at('more than forty')
        self.play(LaggedStart(*[FadeIn(d) for d in tiles],lag_ratio=.009),FadeIn(label('more than 40 types of ganglion cell (mouse)',[0,-3,0],TEXT,31)),run_time=.65)
        self.finish()


class S06Filter(SpokenScene):
    def construct(self):
        src=field(3.8,5.0).move_to([-4.05,0,0])
        names=('brightness','small object','one direction')
        panes=VGroup(*[Ellipse(width=.55,height=1.15,color=c,fill_color=c,fill_opacity=.22).move_to([-.45,y,0]) for c,y in zip(COLORS,(2.1,0,-2.1))])
        outputs=VGroup(*[VGroup(filter_panel(i,4.5,1.4).move_to([3.4,y,0]),label(names[i],[3.4,y+.89,0],COLORS[i],28)) for i,y in enumerate((2.1,0,-2.1))])
        self.add(src,label('One scene',[-4.05,3.27,0],TEXT,34),panes,outputs)
        self.at('Each type')
        self.play(*[GrowArrow(arrow([-2.05,y*.7,0],[-.8,y,0],c)) for c,y in zip(COLORS,(2.1,0,-2.1))],run_time=.35)
        self.at('its own filter')
        self.play(Indicate(outputs,scale_factor=1.015),*[GrowArrow(arrow([-.1,y,0],[1,y,0],c)) for c,y in zip(COLORS,(2.1,0,-2.1))],run_time=.5)
        self.finish()


class S07Simple(SpokenScene):
    def construct(self):
        p=filter_panel(0,11.7,5.65).move_to([0,-.2,0])
        self.add(p,heading('Local brightness differences',GOLD))
        self.at('local differences')
        self.play(Indicate(p[1:],color=GOLD,scale_factor=1.015),run_time=.65)
        self.finish()


class S08Select(SpokenScene):
    def construct(self):
        p=VGroup(Rectangle(width=11.7,height=5.65,color=TEAL,fill_color='#272C36',fill_opacity=1),
            hawk(TEAL).scale(.48).move_to([-2,-.7,0])).shift(DOWN*.2); title=heading('Small moving object',TEAL)
        direction=arrow([-3.8,1.45,0],[3.8,1.45,0],TEAL)
        self.add(p,title,direction)
        self.at('a small object')
        self.play(Indicate(p[1],color=TEXT,scale_factor=1.15),run_time=.3)
        self.at('moving')
        self.play(p[1].animate.shift(RIGHT*1.5),run_time=.5)
        self.at('motion in one direction')
        self.play(FadeOut(direction),ReplacementTransform(p,filter_panel(2,11.7,5.65).move_to([0,-.2,0])),ReplacementTransform(title,heading('One direction',VIOLET)),run_time=.4)
        self.finish()


class S09Built(SpokenScene):
    def construct(self):
        r=retina(); labs=retina_labels()
        self.add(r[0],r[1],r[4],r[5],labs[0],labs[3],heading('Filters built inside the retina'))
        rays=VGroup(*[arrow([x,2.87,0],[x,2.47,0],TEXT) for x in (-5,-3.4,-1.8,-.2,1.4)])
        self.add(rays,label('light',[-6.05,2.75,0],TEXT,28))
        self.at('Bipolar')
        self.play(FadeIn(r[2]),FadeIn(labs[1]),run_time=.35)
        self.at('amacrine circuits')
        self.play(FadeIn(r[3]),FadeIn(labs[2]),run_time=.35)
        self.at('build each filter')
        self.play(Indicate(VGroup(r[2],r[3]),color=SLATE,scale_factor=1.025),run_time=.5)
        self.at('any spike')
        spike=Dot([2.8,-2.7,0],radius=.12,color=GOLD); self.add(spike)
        self.play(spike.animate.move_to([5.8,-2.4,0]),run_time=.65); self.remove(spike)
        self.finish()


class S10Sheet(SpokenScene):
    def construct(self):
        r=retina(); self.add(r,heading('From cross-section to top view'))
        base=sheet_base()
        self.at('look down')
        flat=Rectangle(width=5.76,height=.4,color=GREY).move_to(CENTER)
        self.play(ReplacementTransform(r,flat),run_time=.4)
        grey_dots=dots().set_color(GREY).set_opacity(.55)
        self.play(ReplacementTransform(flat,base),FadeIn(grey_dots),run_time=.6)
        self.add(label('optic disc',[3,1.8,0],GREY,28),Line(CENTER+[2.25,.18,0],[1.8,1.8,0],color=GREY),label('top view',[3,-.2,0],TEXT,32))
        self.at('light up one type')
        self.play(ReplacementTransform(grey_dots,dots()),FadeIn(label('one illustrative type',[3,-1.2,0],GOLD,28)),run_time=.45)
        self.finish()


class S11Space(SpokenScene):
    def construct(self):
        self.add(sheet_base(),dots(),links(),heading('A spaced mosaic'),label('Illustrative type',[3,2.15,0],GOLD,30),label('Fairly even gaps;\nregularity varies',[3,.5,0],TEXT,28))
        self.at('keep some distance')
        self.play(Indicate(links(),color=GOLD,scale_factor=1.02),run_time=.65)
        self.finish()


class S12Cover(SpokenScene):
    def construct(self):
        d=dots(); self.add(sheet_base(),d,heading('Overlapping dendritic arbors'),label('Illustrative',[3,2.15,0],GOLD,30))
        a=arbors()
        self.at('Their dendrites')
        self.play(FadeIn(a),run_time=.6); self.bring_to_front(d)
        self.at('spacing and arbor size')
        self.play(FadeIn(label('Smaller / denser',[2.9,.65,0],GOLD,28)),FadeIn(label('Larger / wider gaps',[2.9,-.45,0],GOLD,28)),run_time=.4)
        self.add(arrow([1.2,.65,0],[-4.35,.65,0],GOLD),arrow([1.2,-.45,0],[-.65,-.45,0],GOLD))
        self.finish()


class S13Mosaic(SpokenScene):
    def construct(self):
        d=dots(); base=sheet_base(); l=links()
        # The scene and each sample share the same sheet coordinates.
        meadow=field(2*R,2*R).move_to(CENTER)
        clipped=VGroup(*[Intersection(part,Circle(radius=R).move_to(CENTER),
            fill_color=part.get_fill_color(),fill_opacity=.65,stroke_width=0)
            for part in (meadow[0],meadow[1],meadow[3])])
        sampled=VGroup()
        for p in positions():
            dark=inside_bird(p[0]/(2*R*.22),(p[1]+2*R*.18)/(2*R*.22))
            value=.08 if dark else (.83 if p[1]>2*R*.02 else .39)
            sampled.add(Dot(CENTER+p,radius=.115,color=interpolate_color(ManimColor('#59471F'),ManimColor('#FFF0B7'),value),
                stroke_color=GOLD,stroke_width=1.5))
        preview=VGroup(Circle(radius=R,color=GOLD),sampled.copy().shift(-CENTER))
        preview.scale(.80).move_to([3.55,.25,0])
        self.add(base,d,l,heading('Mosaic',GOLD))
        self.at('called a mosaic')
        self.play(FadeOut(l),FadeIn(clipped),run_time=.45); self.bring_to_front(d)
        self.play(Transform(d,sampled),run_time=.55)
        self.at('So one type')
        self.play(FadeIn(preview),FadeIn(label('one type = one map',[3.55,-2.6,0],GOLD,28)),run_time=.5)
        self.finish()


class S14Layer(SpokenScene):
    def construct(self):
        first=dots(0); second=dots(1); third=dots(2)
        def specimen(kind):
            c=COLORS[kind]; radius=(.88,1.10,.67)[kind]
            return VGroup(Circle(radius=radius,color=c,stroke_width=4,fill_color=c,fill_opacity=.07).move_to([3.2,.65,0]),
                Dot([3.2,.65,0],radius=.12,color=c),label(f'type {kind+1} arbor',[3.2,-.9,0],c,30))
        sample=specimen(0)
        self.add(sheet_base(),first,heading('Three mosaics on the same retina'),key()[0],sample,
            label('Own spacing and arbor size',[3.2,-2,0],TEXT,26))
        self.at('Lay a second type')
        self.play(first.animate.set_opacity(.25),FadeIn(second),FadeIn(key()[1]),Transform(sample,specimen(1)),run_time=.55)
        # Keep the active type and its one readable arbor still before the next.
        self.at('Then a third')
        self.play(second.animate.set_opacity(.25),FadeIn(third),FadeIn(key()[2]),Transform(sample,specimen(2)),run_time=.45)
        self.finish()


class S15Predict(SpokenScene):
    def construct(self):
        p=predict(); self.add(p[0],p[1],p[2])
        self.at('Predict')
        self.play(FadeIn(label('Predict',[3.1,2.65,0],GOLD,32)),run_time=.3)
        self.at('what does the optic nerve')
        self.play(FadeIn(p[3]),run_time=.35)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(predict(),label('Pause and predict',[3.1,2.65,0],GOLD,32))
        ring=Circle(radius=.45,color=GREY).move_to([3.1,-2.4,0]); self.add(ring)
        self.play(Create(Arc(radius=.45,start_angle=PI/2,angle=-TAU,color=GOLD,stroke_width=6).move_to(ring)),run_time=5,rate_func=linear)


class S17Reveal(SpokenScene):
    def construct(self):
        f=feed(); self.add(maps(),f,heading('Overlapping maps of the same scene'))
        self.at('More than forty')
        self.play(Transform(f,feed(True)),run_time=.6)
        bracket=VGroup(Line([.55,1.3,0],[5.65,1.3,0],color=TEXT),Line([.55,1.12,0],[.55,1.3,0],color=TEXT),Line([5.65,1.12,0],[5.65,1.3,0],color=TEXT))
        self.add(bracket,label('more than 40 maps',[3.1,1.85,0],TEXT,32))
        self.at('each filtered differently')
        self.play(FadeIn(label('Each filtered differently',[3.1,-2.25,0],TEXT,28)),run_time=.3)
        self.finish()


class S18Combine(SpokenScene):
    def construct(self):
        self.add(brain(),tube(-5.8,2.85,0,1.7,True),heading('Combine maps → new features'))
        paths=VGroup(Line([1.7,.45,0],[4.4,0,0],color=GOLD,stroke_width=5),Line([1.7,-.45,0],[4.4,0,0],color=TEAL,stroke_width=5))
        self.add(paths,label('optic nerve',[-2,-1.55,0],GREY,30))
        self.at('combine maps')
        ds=VGroup(Dot([1.7,.45,0],radius=.13,color=GOLD),Dot([1.7,-.45,0],radius=.13,color=TEAL)); self.add(ds)
        self.play(*[d.animate.move_to([4.4,0,0]) for d in ds],run_time=.45)
        self.at('new features')
        self.remove(ds)
        self.play(FadeIn(Dot([4.4,0,0],radius=.24,color=CORAL)),FadeIn(label('new feature',[4.4,-1.2,0],CORAL,28)),run_time=.3)
        self.finish()


class S19Lost(SpokenScene):
    def construct(self):
        src=field(3.4,4.7).move_to([-4.45,0,0])
        self.add(src,brain(),tube(-2.6,3.05,0,1.7,True),heading('Lost before the brain'),label('optic nerve',[.1,-1.55,0],GREY,30))
        # Remove the actual full-width texture, so the meadow stays visibly emptier.
        detail=src[2]; detail.set_stroke(TEXT,width=4)
        self.add(label('If no map carries\na fine texture…',[-4.45,-2.85,0],TEXT,28))
        self.at('information that no map carries')
        self.play(detail.animate.set_color(GREY).move_to([-3.0,0,0]),run_time=.75)
        self.at('is gone')
        self.play(detail.animate.shift(DOWN*1.75).set_opacity(.3),run_time=.5)
        self.play(FadeOut(detail,shift=DOWN*.6),run_time=.3)
        self.finish()


class S20Test(SpokenScene):
    def construct(self):
        group_label=label('One spaced mosaic',[3.1,1.6,0],GOLD,30)
        regular=VGroup(*[Dot(CENTER+[x,y,0],radius=.10,color=GOLD)
            for y in np.arange(-2.1,2.2,.7) for x in np.arange(-2.1,2.2,.7) if np.hypot(x,y)<R-.23])
        self.add(sheet_base(),regular,heading('One apparent group'),group_label)
        self.at('really two')
        second=dots(1).set_color(GOLD)
        self.play(ReplacementTransform(group_label,label('Two mosaics pooled',[3.1,1.6,0],GOLD,30)),ReplacementTransform(regular,dots()),FadeIn(second),FadeIn(label('If two types\nare merged…',[3.1,.2,0],TEXT,32)),run_time=.45)
        pts=positions(); qs=positions(1); pairs=[]
        for p in pts:
            q=min(qs,key=lambda q:np.linalg.norm(p-q))
            if np.linalg.norm(p-q)<.35: pairs.append((p,q))
        circles=VGroup(*[Ellipse(width=.65,height=.48,color=TEXT,stroke_width=5).move_to(CENTER+(p+q)/2) for p,q in pairs[:5]])
        self.at('spacing usually looks less regular')
        self.add(label('Near-touching pairs',[3.1,-1.35,0],TEXT,28))
        self.play(Create(circles),run_time=.45)
        self.finish()


class S21Cov(SpokenScene):
    def construct(self):
        # Four real circles of each shade cover exactly the marked probe point.
        # Other circles are deliberately outside the probe's radius.
        probe=CENTER.copy(); rad=1.18
        sets=[np.array([[-.68,-.65,0],[.68,-.65,0],[-.68,.65,0],[.68,.65,0]]),
              np.array([[-.82,-.25,0],[.82,-.25,0],[-.25,.82,0],[.25,-.82,0]])]
        shades=(GOLD,'#FFF1CD'); groups=VGroup(); counts=[]
        self.add(sheet_base()[0],heading('Arbors covering the marked point'))
        for points,c in zip(sets,shades):
            counts.append(sum(np.linalg.norm(p)<rad for p in points))
            g=VGroup()
            for p in points:
                g.add(Circle(radius=rad,color=c,stroke_width=3,stroke_opacity=1,fill_color=c,fill_opacity=.06 if c==GOLD else 0).move_to(probe+p),Dot(probe+p,radius=.10,color=c))
            if c!=GOLD:
                for ring in g[::2]: ring.set_stroke(opacity=.85)
            groups.add(g)
        self.add(groups,Dot(probe,radius=.12,color=TEXT),label('×',probe, TEXT,28))
        rows=VGroup(label(f'Type A alone: {counts[0]}',[3.0,1.75,0],shades[0],28),label(f'Type B alone: {counts[1]}',[3.0,.95,0],shades[1],28),label(f'Pooled: {sum(counts)}',[3.0,.05,0],TEXT,34),label(f'A comparable\nsingle type: {counts[0]}',[3.0,-1.0,0],TEXT,30))
        self.add(rows,label('Illustrative',[ -2.65,-3.28,0],GREY,28),label('A clue, not proof',[3.0,-2.65,0],TEXT,30))
        self.at('more arbors cover each point')
        self.play(Indicate(groups[0],color=shades[0],scale_factor=1.04),Indicate(rows[0],color=shades[0]),run_time=.45)
        self.play(Indicate(groups[1],color=shades[1],scale_factor=1.04),Indicate(rows[1],color=shades[1]),run_time=.45)
        self.play(Indicate(groups,color=TEXT,scale_factor=1.02),Indicate(rows[2],color=TEXT),run_time=.4)
        self.at('than for comparable types')
        self.play(Indicate(rows[3],color=TEXT,scale_factor=1.04),run_time=.5)
        self.at('These are clues')
        self.play(Indicate(self.mobjects[-1],color=TEXT,scale_factor=1.04),run_time=.45)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        m=maps(); f=feed(True); self.add(m,f,heading('Parallel channels out of the eye'))
        self.at('One type')
        takeaway=label('One type, one mosaic, one map.',[0,-3.28,0],TEXT,34)
        self.remove(m[4])
        self.play(FadeIn(takeaway),Indicate(m[1],color=GOLD,scale_factor=1.02),run_time=.35)
        self.at('one mosaic')
        l=links(); self.play(Create(l),run_time=.35)
        self.at('one map')
        self.play(Indicate(f[0][1],scale_factor=1.02),run_time=.35)
        self.finish()


class S23End(EndCard):
    LINE='One type, one mosaic, one map.'
    def construct(self):
        self.add(fit(label(self.LINE,[0,.3,0],TEXT,43),max_w=12),label('biochemistrypedia.com',[0,-.8,0],TEAL,28))
        self.finish()
