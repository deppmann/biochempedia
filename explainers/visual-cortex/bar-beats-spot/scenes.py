"""Why a Bar Beats a Spot, revised after the frame review.

COLOR MAP: GREEN = ON / excitation; MAGENTA = OFF / inhibition;
BLUE = cortical cells, spikes, tuning; YELLOW = light;
ORANGE = threshold / measurement; GREY = structure; GOLD = title rule.
All curves integrate the signed rectangular field (six +1, twelve -0.5).
The toy rate is max(0, sum - 2). Rasters use reproducible irregular events.
"""
from functools import lru_cache
import numpy as np
from bp_style import *

MAGENTA = '#E68BD3'
ORANGE = '#F29E4C'
GREY = '#B8C0CF'


def label(s, p, size=28, color=TEXT):
    return T(s, size, color, line_spacing=1.15).move_to(p)


def heading(s):
    return label(s, [0, 3.3, 0], 32)


def strips(x=-3.8, height=5.64, width=.94):
    g = VGroup()
    for i, c in enumerate((MAGENTA, GREEN, MAGENTA)):
        rect = Rectangle(width=width, height=height, color=c, stroke_width=3,
                         fill_color=c, fill_opacity=.23).move_to([x+(i-1)*width, 0, 0])
        g.add(rect)
    return g


def grid(x=-3.8, size=.94, labels=True, y=0):
    g = VGroup()
    for col in range(3):
        column = VGroup()
        for row in range(6):
            c = GREEN if col == 1 else MAGENTA
            sq = Square(side_length=size, color=c, stroke_width=2.8,
                        fill_color=c, fill_opacity=.20).move_to([x+(col-1)*size, y+(2.5-row)*size, 0])
            item = VGroup(sq)
            if labels:
                item.add(label('+1' if col == 1 else '−0.5', sq.get_center(), 26, c))
            column.add(item)
        g.add(column)
    return g


def light(x=-3.8, kind='bar', size=.94, y=0):
    w,h = {'bar': (size,6*size), 'across': (3*size,size),
           'all': (3*size,6*size), 'spot': (size,size)}[kind]
    cy = y + (.5*size if kind in ('spot','across') else 0)
    return Rectangle(width=w, height=h, color=YELLOW, stroke_width=5,
                     fill_color=YELLOW, fill_opacity=.20).move_to([x,cy,0])


def raster(n=0, x=3.2, y=-2.15, width=4.5, text='toy cell spikes', tick_h=.38):
    base = Line([x-width/2,y,0], [x+width/2,y,0], color=GREY, stroke_width=2.5)
    rng = np.random.default_rng(140+n)
    positions = np.sort(rng.uniform(.03,.97,n))
    ticks = VGroup(*[Line([x-width/2+p*width,y+.03,0],
                         [x-width/2+p*width,y+tick_h,0], color=BLUE, stroke_width=3.5)
                    for p in positions])
    words = T(text,26,BLUE,line_spacing=1.15).next_to(base,DOWN,buff=.24) if text else VGroup()
    return VGroup(base,ticks,words)


def meter(value=0, x=-.75):
    y0 = -.9
    scale = .59
    axis = Line([x,-2.72,0],[x,2.72,0],color=GREY,stroke_width=3)
    ticks = VGroup()
    for v in (-3,0,2,6):
        p = y0+v*scale
        ticks.add(Line([x-.10,p,0],[x+.8,p,0],color=GREY,stroke_width=2),
                  label(str(v),[x-.40,p,0],26))
    th = DashedLine([x-.12,y0+2*scale,0],[x+1.12,y0+2*scale,0],color=ORANGE,stroke_width=4)
    th_label = label('threshold 2\n(made up)',[x+3.0,y0+2*scale,0],28,ORANGE)
    fill = Rectangle(width=.68,height=max(.025,abs(value)*scale),stroke_width=0,
                     fill_color=GREEN if value>=0 else MAGENTA,fill_opacity=.85)
    fill.move_to([x+.4,y0+value*scale/2,0])
    val = label(f'sum {value:+g}' if value else 'sum 0',[x+.5,3.2,0],36)
    rate = label(f'rate {max(0,value-2):g} a.u.',[3.2,-1.1,0],32,BLUE)
    return VGroup(axis,ticks,th,th_label,fill,val,rate)


def stage(kind=None, value=0, title=''):
    g = grid()
    m = meter(value)
    r = raster(round(max(0,value-2)*4))
    out = VGroup(g,m,r)
    if kind:
        out.add(light(-4.74 if kind=='off' else -3.8, 'bar' if kind=='off' else kind))
    if title:
        out.add(label(title,[-3.8,3.25,0],30,YELLOW))
    return out


def compact_meter(x, value):
    y0=-2.65; sc=.85
    axis=Line([x,y0,0],[x,y0+6*sc,0],color=GREY,stroke_width=3)
    fill=Rectangle(width=.55,height=max(.025,value*sc),stroke_width=0,
                   fill_color=GREEN,fill_opacity=.85).move_to([x+.35,y0+value*sc/2,0])
    th=DashedLine([x-.13,y0+2*sc,0],[x+1,y0+2*sc,0],color=ORANGE,stroke_width=4)
    nums=VGroup(*[label(str(v),[x-.3,y0+v*sc,0],26) for v in (0,2,6)])
    val=label(f'+{value}',[x+.4,2.95,0],34,GREEN)
    rate=label(f'rate {max(0,value-2)}',[x+.55,-3.25,0],26,BLUE)
    return VGroup(axis,fill,th,nums,val,rate)


def comparison(spot_result=True):
    a=VGroup(grid(-4.75,y=.05),light(-4.75,'bar',y=.05),
             label('bar',[-4.75,3.35,0],32,YELLOW),compact_meter(-2.65,6),
             raster(16,-4.75,-3.35,2.7,'',.30))
    b=VGroup(grid(1.65,y=.05),light(1.65,'spot',y=.05),
             label('spot',[1.65,3.35,0],32,YELLOW))
    if spot_result:
        b.add(compact_meter(3.75,1),raster(0,1.65,-3.35,2.7,'',.30))
    return VGroup(a,b)


def question_one():
    q=label('Small spot on the ON strip,\nor a bar along it?', [0,2.95,0],34)
    return VGroup(q,grid(-3.5,.76,False,y=-.45),grid(3.5,.76,False,y=-.45),
                  light(-3.5,'spot',.76,y=-.45),light(3.5,'bar',.76,y=-.45),
                  label('spot',[-3.5,-3.2,0],30,YELLOW),label('bar',[3.5,-3.2,0],30,YELLOW))


def question_two():
    return VGroup(heading('Light over the whole field?'),grid(0),light(0,'all'))


def countdown(scene):
    t=ValueTracker(0)
    ring=always_redraw(lambda: Arc(radius=.50,start_angle=PI/2,
        angle=-max(.001,TAU*(1-t.get_value()/5)),color=YELLOW,stroke_width=7).shift([5.3,-2.6,0]))
    num=always_redraw(lambda: label(str(max(1,int(np.ceil(5-t.get_value())))),[5.3,-2.6,0],30,YELLOW))
    scene.add(ring,num)
    scene.play(t.animate.set_value(5),run_time=5,rate_func=linear)


@lru_cache(maxsize=8)
def tuning(height=6):
    # Midpoint quadrature: ON width one, two OFF widths one; bar length=field length.
    xx,yy=np.meshgrid(np.linspace(-1.5,1.5,240,endpoint=False)+3/480,
                      np.linspace(-height/2,height/2,480,endpoint=False)+height/960)
    weights=np.where(abs(xx)<.5,1.,-.5)
    angles=np.linspace(0,180,361)
    vals=[]
    for deg in angles:
        a=np.deg2rad(deg)
        along=xx*np.cos(a)+yy*np.sin(a)
        across=-xx*np.sin(a)+yy*np.cos(a)
        vals.append(float(np.sum(weights*((abs(along)<=height/2)&(abs(across)<=.5)))*3*height/weights.size))
    return angles,np.array(vals)


def model_value(deg,height=6):
    a,v=tuning(height)
    return float(np.interp(deg,a,v))


def plot(x=3.6,y=.4,width=4.5,height=3.6,field_h=6,normalized=False,axis_text=True):
    a,v=tuning(field_h)
    if normalized: v=v/field_h
    ax=Axes(x_range=[0,180,90],y_range=[0,1.08 if normalized else 6.5,1],
        x_length=width,y_length=height,tips=False,axis_config={'color':GREY,'stroke_width':3,'include_ticks':False}).move_to([x,y,0])
    c=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([ax.c2p(aa,max(0,vv)) for aa,vv in zip(a,v)])
    labels=VGroup(*[label(f'{d}°',ax.c2p(d,0)+DOWN*.28,26) for d in (0,90,180)])
    labels.add(label('response',ax.get_top()+UP*.3,26,BLUE))
    if axis_text:
        labels.add(label('bar orientation', [x,ax.c2p(90,0)[1]-.80,0],26))
    return VGroup(ax,labels,c)


def neuron(p=(.8,0,0)):
    body=Circle(.70,color=BLUE,fill_color=BLUE,fill_opacity=.25,stroke_width=4)
    g=VGroup(body)
    for d in (RIGHT,UR,DR):
        g.add(Line(d*.70,d*1.15,color=BLUE,stroke_width=4))
    return g.move_to(p)


def lgn(x,y,off=False,r=.62):
    outer=MAGENTA if not off else GREEN
    inner=GREEN if not off else MAGENTA
    return VGroup(Circle(r,color=outer,fill_color=outer,fill_opacity=.17,stroke_width=3),
                  Circle(r*.44,color=inner,fill_color=inner,fill_opacity=.8,stroke_width=3),
                  label('−' if off else '+',[0,0,0],26,BG)).move_to([x,y,0])


def wiring(full=False):
    fields=VGroup(*[lgn(-4,y) for y in (1.45,0,-1.45)])
    cell=neuron()
    # ON routes pass above/below the OFF column, with the middle route in its gap.
    arrows=VGroup()
    for yy,end in zip((1.45,0,-1.45),(.40,0,-.40)):
        start=np.array([-3.38,yy,0]); stop=np.array([.13,end,0])
        if yy:
            sign=np.sign(yy)
            bends=[[-3.0,sign*2.55,0],[-.25,sign*2.55,0]]
            path=VMobject(color=GREEN,stroke_width=3).set_points_as_corners([start,*bends])
            arrows.add(VGroup(path,Arrow(bends[-1],stop,buff=0,color=GREEN,
                                        stroke_width=3,max_tip_length_to_length_ratio=.08)))
        else:
            arrows.add(Arrow(start,stop,buff=0,color=GREEN,stroke_width=3,
                             max_tip_length_to_length_ratio=.08))
    names=VGroup(label('LGN (lateral geniculate nucleus)\ncells with ON centres',[-3.9,-3.12,0],26,GREEN),
                 label('one cortical cell',[3.6,-1.5,0],28,BLUE))
    group=VGroup(fields,cell,arrows,names)
    if full:
        s=strips(-4,4.3,.78)
        # A clearly separated OFF column beside the aligned ON row.
        off=VGroup(*[lgn(-2.3,y,True,.40) for y in (1.8,.6,-.6,-1.8)])
        routes=VGroup()
        for source, end_y in zip(off,(.36,.13,-.13,-.36)):
            routes.add(Arrow(source.get_right(),[.13,end_y,0],buff=0,
                             color=MAGENTA,stroke_width=3,
                             max_tip_length_to_length_ratio=.08))
        names[0].become(label('LGN cells\n(ON-centre and OFF-centre)',[-3.9,-3.12,0],26))
        group.add(s,off,routes)
        group.remove(s); group.add_to_back(s)
    return group


class S00Title(TitleCard):
    LESSON='Visual Cortex'
    TITLE='Why a Bar Beats a Spot'
    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',[0,1.4,0],26,TEAL)
        lesson=label(self.LESSON.upper(),[0,.7,0],28,GREY)
        title=label(self.TITLE,[0,-.3,0],52)
        rule=Line([-1.2,-1.2,0],[1.2,-1.2,0],color=GOLD,stroke_width=4)
        self.add(brand,lesson)
        self.play(FadeIn(title),Create(rule),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(label('Why does a bar at the right angle\nbeat a spot?',[0,2.8,0],36))
        self.at('Spots of light')
        a=Circle(.5,color=YELLOW,fill_color=YELLOW,fill_opacity=.8).move_to([-3.4,-.4,0])
        self.add(a,label('spot',[-3.4,-2.9,0],32,YELLOW))
        self.at('So why would')
        self.play(FadeIn(light(3.4,'bar',.65,y=-.4)),
                  FadeIn(label('bar at the right angle',[3.1,-2.9,0],30,YELLOW)),run_time=.5)
        self.finish()


class S02Setup(SpokenScene):
    def construct(self):
        body=Ellipse(width=4.5,height=2.3,color=GREY,stroke_width=4).move_to([-2,-1.05,0])
        head=Circle(.86,color=GREY,stroke_width=4).move_to([-.05,.1,0])
        ears=VGroup(Polygon([-.75,.65,0],[-.8,1.5,0],[-.18,.94,0],color=GREY,stroke_width=4),
                    Polygon([.18,.94,0],[.72,1.46,0],[.78,.44,0],color=GREY,stroke_width=4))
        tail=Arc(radius=1.0,start_angle=PI/2,angle=PI,color=GREY,stroke_width=4).move_to([-4.7,-1.0,0])
        face=VGroup(Line([.22,.35,0],[.56,.30,0],color=GREY,stroke_width=4),
                    Line([.72,-.05,0],[1.04,-.05,0],color=GREY,stroke_width=4))
        cat=VGroup(body,head,ears,tail,face)
        scr=Rectangle(width=2.0,height=5.1,color=GREY,stroke_width=4).move_to([4,0,0])
        elec=Line([-2.2,2.3,0],[-.60,.66,0],color=BLUE,stroke_width=6)
        self.at('David')
        self.add(cat,scr,heading('Hubel and Wiesel · cat V1'),
                 label('screen',[4,-3.05,0],30),label('anaesthetized cat',[-2.3,-2.85,0],30))
        self.at('recorded single cells')
        self.play(Create(elec),FadeIn(label('electrode',[-2.6,2.65,0],30,BLUE)),run_time=.5)
        self.finish()


class S03Electrode(SpokenScene):
    def construct(self):
        scr=Rectangle(width=2.4,height=4.5,color=GREY,stroke_width=4).move_to([-4.6,0,0])
        c=neuron((2,.45,0)).scale(1.25)
        endpoint=c[0].point_at_angle(PI/4)
        e=Line([4.5,2.8,0],endpoint,color=BLUE,stroke_width=6)
        self.add(scr,c,label('screen',[-4.6,-2.8,0],30),label('one cell',[2,-1.0,0],30,BLUE))
        self.at('An electrode')
        self.play(Create(e),FadeIn(label('electrode',[4.6,3.2,0],30,BLUE)),run_time=.5)
        self.at('counted its spikes')
        self.play(FadeIn(raster(7,x=2.6,y=-2.35,text='spikes (schematic)')),run_time=.5)
        self.at('while light was')
        proj=Rectangle(width=1,height=.7,color=GREY,stroke_width=4).move_to([-.8,1.8,0])
        beam=Polygon([-1.3,1.8,0],[-3.4,1.8,0],[-3.4,-1.7,0],color=YELLOW,stroke_width=3,fill_color=YELLOW,fill_opacity=.13)
        self.play(FadeIn(proj),FadeIn(beam),FadeIn(label('projector',[-.8,2.6,0],28)),run_time=.5)
        self.finish()


class S04Spots(SpokenScene):
    def construct(self):
        self.add(heading('Same cell: spot versus aligned bar'))
        for x in (-3.4,3.4):
            self.add(Rectangle(width=4.2,height=3.6,color=GREY,stroke_width=3).move_to([x,.5,0]))
        self.at('Spots often')
        self.add(Dot([-3.4,.5,0],radius=.33,color=YELLOW),label('spot',[-3.4,2.7,0],30,YELLOW),
                 raster(2,-3.4,-2.2,4.1,'spikes (schematic)'))
        self.at('A slit or bar')
        self.play(FadeIn(Rectangle(width=.6,height=3.1,color=YELLOW,stroke_width=5,fill_color=YELLOW,fill_opacity=.7).move_to([3.4,.5,0])),
                  FadeIn(label('bar at the right angle',[3.4,2.7,0],28,YELLOW)),
                  FadeIn(raster(18,3.4,-2.2,4.1,'spikes (schematic)')),run_time=.4)
        # Both results remain visible for comparison, including the full sparse-raster hold.
        self.finish()


class S05Map(SpokenScene):
    def construct(self):
        frame=Rectangle(width=3.2,height=5.7,color=GREY,stroke_width=3).move_to([-3.7,0,0])
        spot=Dot([-4.64,2.35,0],radius=.24,color=YELLOW)
        self.at('For cells')
        self.add(frame,spot,label('mapping with small spots',[1.9,1.6,0],30))
        self.at('they mapped the field')
        for row in range(6):
            for col in range(3):
                p=[-3.7+(col-1)*.94,2.35-row*.94,0]
                c=GREEN if col==1 else MAGENTA
                self.play(spot.animate.move_to(p),run_time=.10)
                self.add(label('+' if col==1 else '−',p,30,c))
        self.at('simple cells')
        self.play(FadeIn(label('simple cell',[2,2.8,0],34,BLUE)),run_time=.3)
        self.at('on and off subregions')
        self.play(FadeOut(spot),FadeIn(label('ON +\nLight here raises firing',[2,.3,0],28,GREEN)),
                  FadeIn(label('OFF −\nLight here lowers firing',[2,-1.5,0],28,MAGENTA)),run_time=.4)
        self.finish()


class S06Layout(SpokenScene):
    def construct(self):
        s=strips(); self.add(s,label('Long, narrow subregions',[1.8,2.4,0],30),
            label('ON +\nLight here raises firing',[2,.7,0],28,GREEN),
            label('OFF −\nLight here lowers firing',[2,-1.3,0],28,MAGENTA))
        for i,sign in enumerate(('−','+','−')):
            self.add(label(sign,[-3.8+(i-1)*.94,0,0],36,GREEN if i==1 else MAGENTA))
        self.at('long and narrow'); self.play(Indicate(s,scale_factor=1.02,color=TEXT),run_time=.6)
        self.at('a narrow on strip'); self.play(Indicate(s[1],color=GREEN),run_time=.6)
        self.at('off strip on each side'); self.play(Indicate(VGroup(s[0],s[2]),color=MAGENTA),run_time=.6)
        self.finish()


class S07Grid(SpokenScene):
    def construct(self):
        s=strips(); self.add(s)
        self.at('Picture the field'); self.play(ReplacementTransform(s,grid()),run_time=.6)
        self.at('values'); self.add(meter(),label('Numbers made up for teaching',[0,-3.35,0],28))
        self.at('Plus and minus are balanced')
        self.add(label('ON +6 + OFF −6 = 0',[-3.6,3.3,0],28))
        self.at('many real simple cells')
        self.add(label('Toy cell: no\nspontaneous firing',[3.1,-2.3,0],28))
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        self.at('which will win'); self.add(question_one()); self.finish()


class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_one()); countdown(self)


class S10Reveal(SpokenScene):
    def construct(self):
        comp=comparison(False)
        self.at('The bar wins'); self.add(comp[0])
        self.at('It lands on plus'); self.play(Indicate(comp[0][0][1],color=GREEN,scale_factor=1.02),run_time=.6)
        self.at('The spot collects')
        self.play(FadeIn(comparison()[1]),run_time=.35)
        self.finish()


class S11Threshold(SpokenScene):
    def construct(self):
        s=stage('spot',1,'Spot: +1 only')
        s[2].shift(UP*.35)
        self.add(s)
        self.at('clears its threshold')
        # Pulse the threshold itself without changing the represented threshold value.
        self.play(s[1][2].animate.set_stroke(width=10),run_time=.35)
        self.play(s[1][2].animate.set_stroke(width=4),run_time=.35)
        self.at('The spot falls short')
        gap=VGroup(Line([.4,-.31,0],[.9,-.31,0],color=YELLOW,stroke_width=5),
                   Line([.9,-.31,0],[.9,.28,0],color=YELLOW,stroke_width=5),
                   Line([.4,.28,0],[.9,.28,0],color=YELLOW,stroke_width=5))
        self.add(gap,label('needs more than 2',[3.2,1.55,0],28,YELLOW))
        self.at('That is one reason')
        self.add(label('Real simple cells could still give\nweak responses to spots.',[3.4,-3.35,0],28))
        self.finish()


class S12Rotate(SpokenScene):
    def construct(self):
        a=ValueTracker(90)
        g=grid(-3.7)
        # The bar is clipped to the field: no illuminated area outside the modelled patch.
        def bar_shape():
            bar=Rectangle(width=5.64,height=.94).rotate(a.get_value()*DEGREES).move_to([-3.7,0,0])
            boundary=Rectangle(width=2.82,height=5.64).move_to([-3.7,0,0])
            return Intersection(bar,boundary,color=YELLOW,stroke_width=5,fill_color=YELLOW,fill_opacity=.22)
        b=always_redraw(bar_shape)
        p=plot(3.8,.5,4.3,3.7,axis_text=False); ax=p[0]
        ref=p[2].copy().set_stroke(opacity=.22)
        def trail():
            angles=np.linspace(a.get_value(),90,max(2,int((90-a.get_value())*2)+2))
            return VMobject(color=BLUE,stroke_width=5).set_points_as_corners([ax.c2p(t,max(0,model_value(t))) for t in angles])
        curve=always_redraw(trail)
        dot=always_redraw(lambda: Dot(ax.c2p(a.get_value(),max(0,model_value(a.get_value()))),color=YELLOW,radius=.10))
        y0=-2.7; sc=.85; x=.0
        axis=Line([x,y0,0],[x,2.4,0],color=GREY,stroke_width=3)
        th=DashedLine([x-.12,y0+2*sc,0],[x+.65,y0+2*sc,0],color=ORANGE,stroke_width=4)
        fill=always_redraw(lambda: Rectangle(width=.5,height=max(.025,max(0,model_value(a.get_value()))*sc),stroke_width=0,
                    fill_color=GREEN,fill_opacity=.85).move_to([x+.3,y0+max(0,model_value(a.get_value()))*sc/2,0]))
        val=always_redraw(lambda: label(('sum 0.0' if round(model_value(a.get_value()),1)==0 else f'sum {model_value(a.get_value()):+.1f}'),[.15,3.2,0],28))
        ticks=VGroup(*[label(str(v),[x-.35,y0+v*sc,0],26) for v in (0,2,6)])
        self.add(g,b,p[:2],ref,curve,dot,axis,th,fill,val,ticks,
                 label('bar orientation\n0° = horizontal\n90° = along the ON strip',[3.8,-2.95,0],26))
        self.at('Now turn the bar')
        self.play(a.animate.set_value(0),run_time=4.4,rate_func=linear)
        b.clear_updaters()
        self.play(Transform(b,light(-3.7,'across')),run_time=.25)
        self.at('the sum falls')
        self.add(label('+1 − 0.5 − 0.5 = 0',[-3.0,-3.4,0],30))
        self.wait(2.1)
        self.finish()


class S13Predict2(SpokenScene):
    def construct(self):
        self.at('Now light'); self.add(question_two()); self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_two()); countdown(self)


class S15Reveal2(SpokenScene):
    def construct(self):
        self.at('Plus and minus'); self.add(stage('all',0,'+6 − 6 = 0'))
        self.at('so diffuse light')
        self.add(label('rate = max(0, 0 − 2) = 0',[1.2,-3.35,0],28,BLUE))
        self.finish()


class S16Offbar(SpokenScene):
    def construct(self):
        s=stage('off',-3,'OFF strip')
        # Reserve the whole right lower band for the two raster comparisons.
        s.remove(s[2]); s[1][6].move_to([3.2,-.8,0])
        s[1][3].move_to([3.2,.15,0])
        self.at('A bar'); self.add(s)
        self.at('negative sum'); self.play(Indicate(s[1][4],color=MAGENTA),run_time=.5)
        self.at('This toy cell')
        self.add(raster(0,3.3,-1.55,4.6,'no spontaneous firing,\nso nothing to slow'))
        self.at('A cell with spontaneous firing')
        self.add(label('With spontaneous firing',[3.25,2.9,0],28,BLUE),
                 raster(11,1.8,2.05,2.35,''),raster(2,4.6,2.05,2.35,''),
                 label('bar off',[1.8,1.5,0],26),label('bar on',[4.6,1.5,0],26,YELLOW))
        self.at('would slow down'); self.finish()


class S17Shape(SpokenScene):
    def construct(self):
        s=strips(-3.8); b=light();
        note=label('To a first approximation,\norientation selectivity\ncomes from the shape\nof the field.',[2.3,.5,0],32)
        result=label('ON strip: sum +6',[-3.8,-3.3,0],28,GREEN)
        self.add(s,b,note,result)
        self.at('orientation selectivity')
        self.remove(result)
        self.play(b.animate.shift(LEFT*.94),run_time=1.1)
        result.become(label('OFF strip: sum −3',[-3.8,-3.3,0],28,MAGENTA))
        self.add(result)
        self.wait(.8)
        self.remove(result)
        self.play(b.animate.shift(RIGHT*.94),run_time=1.1)
        result.become(label('ON strip: sum +6',[-3.8,-3.3,0],28,GREEN))
        self.add(result)
        self.at('To a first approximation')
        self.remove(result)
        self.play(b.animate.shift(LEFT*.94),run_time=.8)
        result.become(label('OFF strip: sum −3',[-3.8,-3.3,0],28,MAGENTA))
        self.add(result)
        self.at('it comes from')
        self.remove(result)
        self.play(b.animate.shift(RIGHT*.94),run_time=.8)
        result.become(label('ON strip: sum +6',[-3.8,-3.3,0],28,GREEN))
        self.add(result)
        self.finish()


class S18Longer(SpokenScene):
    def construct(self):
        a=ValueTracker(90)
        self.add(label('Width held fixed',[0,3.55,0],28))
        fields=VGroup(strips(-4.4,1.65,.55).shift(UP*1.45),strips(2.1,1.65,.55).shift(UP*1.45))
        self.add(fields,label('short',[-5.7,2.7,0],28),label('long',[.7,2.7,0],28))
        self.at('Make the strips longer')
        self.play(Transform(fields[1],strips(2.1,3.3,.55).shift(UP*1.45)),run_time=.8)
        plots=[]
        for x,h in ((-3.4,3),(3.1,6)):
            p=plot(x,-1.8,4.8,2.0,h,True); plots.append(p)
            self.add(p[:2])
        def turning(x,h):
            return always_redraw(lambda: Intersection(
                Rectangle(width=h*.55,height=.55).rotate(a.get_value()*DEGREES).move_to([x,1.45,0]),
                Rectangle(width=1.65,height=h*.55).move_to([x,1.45,0]),
                color=YELLOW,stroke_width=4,fill_color=YELLOW,fill_opacity=.22))
        self.add(turning(-4.4,3),turning(2.1,6))
        for fx,h,p in ((-2.1,3,plots[0]),(4.4,6,plots[1])):
            self.add(Line([fx,.1,0],[fx,2.5,0],color=GREY,stroke_width=3),
                label('relative sum',[fx+.5,2.8,0],26))
            self.add(always_redraw(lambda fx=fx,h=h: Rectangle(width=.45,height=max(.025,model_value(a.get_value(),h)/h*2.4),
                stroke_width=0,fill_color=GREEN,fill_opacity=.8).move_to([fx+.3,.1+max(0,model_value(a.get_value(),h)/h)*1.2,0])))
        self.at('Now the sum falls faster')
        self.play(a.animate.set_value(35),run_time=2.0,rate_func=linear)
        self.at('tuning is sharper')
        self.play(*[Create(p[2]) for p in plots],run_time=.7)
        self.finish()


class S19Iceberg(SpokenScene):
    def construct(self):
        p=plot(0,.2,10.8,4.9); ax=p[0]; a,v=tuning()
        p[2].set_color(GREY); p[1].remove(p[1][3]); p[1][-1].move_to([0,-2.85,0])
        self.add(p,label('drive',[-6.1,2.85,0],28),label('0',ax.c2p(0,0)+LEFT*.28,26))
        sum_label=label('sum',[1.7,2.9,0],30,GREY)
        lead=Line(sum_label.get_left(),ax.c2p(96,model_value(96)),color=GREY,stroke_width=2.5)
        self.add(sum_label,lead)
        self.at('The threshold sharpens')
        th=DashedLine(ax.c2p(0,2),ax.c2p(180,2),color=ORANGE,stroke_width=4)
        self.play(Create(th),FadeIn(label('threshold 2',ax.c2p(155,2)+UP*.35,28,ORANGE)),run_time=.5)
        inds=np.where(v>2)[0]
        shade=Polygon(ax.c2p(a[inds[0]],2),*[ax.c2p(a[i],v[i]) for i in inds],ax.c2p(a[inds[-1]],2),
                      stroke_width=0,fill_color=BLUE,fill_opacity=.3)
        self.play(FadeIn(shade),run_time=.4)
        self.at('Measured spike tuning')
        spikes=VMobject(color=BLUE,stroke_width=6).set_points_as_corners([ax.c2p(aa,max(0,vv-2)) for aa,vv in zip(a,v)])
        st=label('spikes',[-2.2,.8,0],30,BLUE)
        sl=Line(st.get_right(),ax.c2p(83,max(0,model_value(83)-2)),color=BLUE,stroke_width=2.5)
        self.play(FadeOut(shade),p[2].animate.set_stroke(opacity=.45),Create(spikes),FadeIn(st),Create(sl),run_time=.7)
        self.add(label('Circuits within cortex contribute too.',[0,-3.45,0],28))
        self.finish()


class S20Row(SpokenScene):
    def construct(self):
        w=wiring(); faint=strips(-4,4.3,.78)
        self.add(heading('How might such a field be built?'),faint,w[1],w[3][1])
        self.at('suggested geniculate cells')
        scattered=VGroup(*[lgn(x,y) for x,y in ((-4.7,1.45),(-3.3,0),(-4.6,-1.45))])
        self.play(FadeIn(scattered),FadeIn(w[3][0]),run_time=.5)
        self.at('in a')
        self.play(ReplacementTransform(scattered,w[0]),run_time=.6)
        self.at('exciting one cortical cell')
        self.play(FadeOut(faint),Create(w[2]),run_time=.6)
        self.finish()


class S21Strip(SpokenScene):
    def construct(self):
        w=wiring(); full=wiring(True); self.add(w)
        self.at('an elongated on strip')
        # Keep the circles and their input arrows; the aligned centres pool into a strip behind them.
        self.play(FadeIn(full[0][1]),run_time=.7)
        self.at('Their surrounds could add')
        # Surround colour flows outward into the two flanks, retaining the source circles.
        self.play(TransformFromCopy(w[0][0][0],full[0][0]),
                  TransformFromCopy(w[0][2][0],full[0][2]),run_time=.8)
        self.at('cells beside the row')
        self.play(FadeIn(full[-2]),FadeIn(label('OFF-centre\nLGN cells',[-1.07,1.95,0],22,MAGENTA)),run_time=.5)
        self.at('could strengthen them')
        self.play(Create(full[-1]),run_time=.6)
        self.finish()


class S22Proposal(SpokenScene):
    def construct(self):
        w=wiring(True); self.add(w,heading('Proposed 1962'))
        self.at('They offered this'); self.wait(.2)
        self.at('Recordings in the')
        note=label('Aligned input:\nsupported by\n1990s recordings',[4.0,1.9,0],28,GREEN)
        self.add(note,label('ON-centre cells feed\nthe ON strip.\nOFF-centre cells feed\nthe OFF strips.',[4.0,-.1,0],26))
        self.play(Indicate(w[3],color=GREEN,scale_factor=1.02),run_time=.6)
        self.at('Exactly how the flanks')
        self.add(label('How the flanks are built:\nless settled',[3.65,-2.6,0],28,MAGENTA))
        self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        c=comparison()
        self.at('So a bar beats'); self.add(c)
        self.at('it collects plus'); self.play(Indicate(c[0][0][1],color=GREEN,scale_factor=1.02),run_time=.6)
        self.at('A spot collects'); self.play(Indicate(c[1][0][1][2],color=YELLOW,scale_factor=1.05),run_time=.5)
        self.finish()


class S24End(EndCard):
    LINE='A bar beats a spot because it collects plus all along the ON strip.'
    def construct(self):
        line=label('A bar beats a spot because it collects plus\nall along the ON strip.',[0,.4,0],38)
        self.add(line,label('biochemistrypedia.com',[0,-1.2,0],28,TEAL))
        self.finish()
