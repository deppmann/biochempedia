"""A Channel Shaped Like a Dome.
COLOR MAP: BLUE Piezo/surface, GREY membrane, YELLOW light/highlight,
PURPLE projected area, GREEN computed gain/open pore, RED closed/hedge,
ORANGE proposed tether, GOLD title rule. All protein shapes are cartoons.
Spherical cap: S=pi(a*a+h*h); fixed S during flattening. Response traces
are illustrative exponential models, not recordings or fitted data.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
LESSON_TITLE='Piezo Channels and the Physics of Force'


def label(s,y=3.15,color=TEXT,size=30):
    return T(s,size,color).move_to([0,y,0])


def note(s='schematic protein cartoon'):
    return label(s,-3.45,GREY,26)


def propeller(detail=False):
    arms=VGroup()
    for k in range(3):
        blocks=VGroup()
        for j in range(38 if detail else 9):
            u,v=(j//4,j%4) if detail and j<36 else ((.1 if detail else j),(j-36 if detail else 1.5))
            r=.65+.27*u; th=k*TAU/3+.13*u
            p=np.array([r*np.cos(th),r*np.sin(th),0])
            if detail: p+=np.array([-.15*(v-1.5)*np.sin(th),.15*(v-1.5)*np.cos(th),0])
            b=RoundedRectangle(width=.12 if detail else .57,height=.5 if detail else .82,corner_radius=.035,
                color=BLUE,fill_color=BLUE,fill_opacity=.7,stroke_width=1)
            blocks.add(b.rotate(th-PI/2).move_to(p))
        arms.add(blocks)
    return VGroup(arms,Circle(.3,color=BLUE,fill_color=BG,fill_opacity=1,stroke_width=6))


def cap(h=10,a=None,x=0,y=1.8,sc=.30,blades=False):
    if a is None: a=np.sqrt(296-h*h)
    xs=np.linspace(-a,a,121)
    if h<.001: ys=np.zeros_like(xs)
    else:
        R=(a*a+h*h)/(2*h)
        ys=-(np.sqrt(np.maximum(0,R*R-xs*xs))-(R-h))
    pts=[np.array([x+sc*u,y+sc*v,0]) for u,v in zip(xs,ys)]
    ribbon=Polygon(*(pts+[p+UP*.22 for p in pts[::-1]]),stroke_width=0,fill_color=BLUE,fill_opacity=.7)
    curve=VMobject(color=BLUE,stroke_width=7).set_points_as_corners(pts)
    g=VGroup(ribbon,curve)
    if blades:
        for i in [12,28,44,76,92,108]:
            t=pts[i+1]-pts[i-1]
            b=RoundedRectangle(width=.6,height=.34,corner_radius=.05,color=BLUE,fill_color=BLUE,fill_opacity=1)
            g.add(b.rotate(np.arctan2(t[1],t[0])).move_to(pts[i]+DOWN*.16))
    return g


def disc(a=14,x=0,y=-2.05,sc=.30):
    return Ellipse(width=2*a*sc,height=2*a*sc*.22,color=PURPLE,fill_color=PURPLE,fill_opacity=.38,stroke_width=3).move_to([x,y,0])


def old_disc(x=0,y=-2.05,sc=.30):
    return DashedVMobject(disc(14,x,y,sc).set_fill(opacity=0),num_dashes=50)


def prediction():
    return VGroup(cap(y=1.45,sc=.36),label('Flatten it without stretching it',3.2),
        label('Shadow bigger or smaller? By how much?',2.5,PURPLE,30),
        T('rim radius 14 nm',28,BLUE).move_to([0,1.95,0]),
        T('depth 10 nm',28,BLUE).move_to([0,-2.7,0]),note('idealized spherical cap · side view'))


def area_cap(h=10):
    return cap(h,x=-3.3,y=1.1,sc=.16)


def area_disc(a=14):
    # True top-down disc, using the exact same nm-to-screen scale as the cap.
    outer=Circle(a*.16,color=PURPLE,fill_color=PURPLE,fill_opacity=.65,stroke_width=3).move_to([3.2,-.15,0])
    inner=Circle(14*.16,stroke_width=0,fill_color=BG,fill_opacity=.6).move_to([3.2,-.15,0])
    return VGroup(outer,inner)


def area_old():
    return DashedVMobject(area_disc()[0].set_fill(opacity=0),num_dashes=60)


def gain_labels():
    return VGroup(T('616 nm²',28,PURPLE).move_to([3.2,-.15,0]),
        T('930 nm²',28,PURPLE).move_to([3.2,2.9,0]),
        Line([3.2,2.65,0],[3.2,2.4,0],color=PURPLE),
        T('gain ≈ 310 nm²',30,GREEN).move_to([-3.3,-1.8,0]),
        T('(πh² = 314 nm²)',28,GREEN).move_to([-3.3,-2.4,0]))


def flat_result():
    return VGroup(area_cap(0),area_disc(np.sqrt(296)),area_old(),gain_labels(),
        T('surface: 930 nm²',28,BLUE).move_to([-3.3,2,0]),note('idealized cap · side view (left), top view (right)'))


def beam_stage():
    membrane=Line([-5.8,1.55,0],[5.8,1.55,0],color=GREY,stroke_width=12)
    blocks=VGroup(*[RoundedRectangle(width=.75,height=.9,corner_radius=.1,color=BLUE,fill_color=BLUE,fill_opacity=.7).move_to([x,1.55,0]) for x in [-2,0,2]])
    beam=Line([-2.3,.4,0],[2.3,.4,0],color=BLUE,stroke_width=20)
    return VGroup(membrane,blocks,beam,T('intracellular beam',28,BLUE).move_to([0,-.2,0]),note('side view · schematic'))


class S00Title(TitleCard):
    LESSON=LESSON_TITLE
    TITLE='A Channel Shaped Like a Dome'
    def construct(self):
        title=VGroup(T('A Channel Shaped',50,font=TITLE_FONT),T('Like a Dome',50,font=TITLE_FONT)).arrange(DOWN,buff=.12)
        self.add(label('BIOCHEMISTRYPEDIA',2.3,TEAL,26),label(self.LESSON,1.6,GREY,26))
        self.play(FadeIn(title),run_time=.6)
        self.add(Line([-1.2,-1.4,0],[1.2,-1.4,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        p=propeller().scale(.9).move_to([2.5,-.1,0])
        self.add(p,label('Why so many helices?'),note())
        self.at('one ion channel')
        self.play(FadeIn(T('central pore',28,BLUE).move_to([2.5,-2.5,0])),Create(Line([2.5,-2.1,0],[2.5,-.5,0],color=BLUE)),run_time=.4)
        self.at('need 114')
        self.play(FadeIn(VGroup(M('114',100,BLUE),T('transmembrane\nhelices',30,BLUE)).arrange(DOWN,buff=.3).move_to([-3.5,.1,0])),run_time=.5)
        self.finish()


class S02Ge(SpokenScene):
    def construct(self):
        p=propeller().scale(.92).shift(DOWN*.25)
        self.add(p,label('Ge et al. · 2015 · mouse Piezo1 · 4.8 Å',size=28),note('trimer · schematic of coarse cryo-EM map'))
        for s,pos in [('arm 1',[4,.7,0]),('arm 2',[-3,2.1,0]),('arm 3',[-1,-2.8,0])]: self.add(T(s,28,BLUE).move_to(pos))
        self.at('the first map')
        self.play(Rotate(p,PI/6),run_time=4)
        self.finish()


class S03Blades(SpokenScene):
    def construct(self):
        p=propeller().scale(.72).move_to([-3.5,-.1,0])
        self.add(p,label('One arm → four-helix units',size=30),note())
        self.at('resolved each arm')
        self.play(p[0][1:].animate.set_opacity(.25),p[0][0].animate.set_color(YELLOW),run_time=.5)
        bundles=VGroup()
        for i in range(5):
            b=VGroup(*[RoundedRectangle(width=.22,height=.65,corner_radius=.05,
                color=YELLOW,fill_color=YELLOW,fill_opacity=.85).shift(RIGHT*j*.28) for j in range(4)])
            bundles.add(b.move_to([2.4,-2+i*.88,0]))
        connector=DashedLine(p[0][0].get_right()+RIGHT*.1,[1.7,.3,0],color=YELLOW)
        self.at('repeating units')
        self.play(FadeIn(bundles,shift=RIGHT*.25),Create(connector),run_time=.8)
        self.at('four helices')
        self.play(FadeIn(T('4 helices per unit',28,YELLOW).move_to([3.1,2.35,0])),run_time=.4)
        self.at('curved blades')
        # Five schematic bundles follow a computed arc about the enlarged pore.
        center=np.array([1.4,-1.3,0])
        targets=VGroup()
        for i,bundle in enumerate(bundles):
            theta=-.25+i*.375
            targets.add(bundle.copy().rotate(theta).move_to(center+2.8*np.array([np.cos(theta),np.sin(theta),0])))
        pore_ring=Circle(.33,color=BLUE,fill_color=BG,fill_opacity=1,stroke_width=6).move_to(center)
        blade_label=T('curved blade',30,YELLOW).move_to([4.9,1.8,0])
        blade_leader=Line([4.9,1.45,0],[3.9,.55,0],color=YELLOW)
        arc=Arc(radius=2.8,start_angle=-.25,angle=1.5,arc_center=center,color=YELLOW,stroke_width=3).set_stroke(opacity=.5)
        self.play(Transform(bundles,targets),Transform(connector,DashedLine(p[0][0].get_right()+RIGHT*.1,targets[-1].get_left()-RIGHT*.1,color=YELLOW)),Create(arc),FadeIn(pore_ring),FadeIn(blade_label),Create(blade_leader),run_time=.7)
        self.at('central pore')
        self.play(FadeIn(T('central pore',28,BLUE).move_to([.9,-2.8,0])),
            Create(Line([1,-2.45,0],[1.35,-1.7,0],color=BLUE)),run_time=.4)
        self.finish()


class S04Beam(SpokenScene):
    def construct(self):
        g=beam_stage();self.add(g)
        self.at('single residues')
        dot=Dot([-.8,.4,0],radius=.13,color=RED)
        self.play(FadeIn(dot),Flash(dot,color=RED),FadeIn(label('single residue mutated',2.7,RED,28)),run_time=.5)
        self.play(FadeOut(dot),run_time=.2)
        self.at('mechanical activation')
        plots=VGroup()
        for x,amp,name,col in [(-3.1,1,'wild type',BLUE),(3.1,.25,'mutant',RED)]:
            ax=Axes(x_range=[0,4,1],y_range=[0,1,1],x_length=4,y_length=1.8,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([x,-1.65,0])
            trace=ax.plot(lambda t:amp*np.exp(-(t-.6)/.85) if t>=.6 else 0,x_range=[0,4,.015],color=col,use_smoothing=False)
            plots.add(VGroup(ax,trace,T(name,28,col).move_to([x,-.65,0]),T('time',26,GREY).move_to([x,-2.9,0]),T('current',26,GREY).rotate(PI/2).move_to([x-2.4,-1.7,0])))
        self.remove(g[-1])
        self.add(note('normalized exponential models · not recordings'))
        self.play(FadeIn(plots),run_time=.5)
        self.finish()


class S05BeamMeaning(SpokenScene):
    def construct(self):
        g=beam_stage();self.add(g)
        self.at('matters for gating')
        call=T('tied to gating,\nnot only assembly',36,BLUE).move_to([0,-1.9,0])
        self.play(Indicate(g[2],color=YELLOW),FadeIn(call),Create(Line([0,-1,0],[0,.1,0],color=BLUE)),run_time=.6)
        self.finish()


class S06Count(SpokenScene):
    def construct(self):
        p=propeller(True).scale(.92).shift(DOWN*.25)
        self.add(p,label('2019 · mouse PIEZO2 · 6KG7',size=28),note('38 blocks per subunit · schematic, not atomic coordinates'))
        self.at('a structure of mouse')
        self.play(Rotate(p,.18),run_time=1)
        self.at('sharp enough to count')
        p[0][1:].set_opacity(.18)
        count=M('0',58,BLUE).move_to([4.7,1,0]);self.add(count,T('helices\ncounted',28,BLUE).move_to([4.7,-.1,0]))
        for n in range(1,39):
            self.play(p[0][0][n-1].animate.set_color(GREEN),Transform(count,M(str(n),58,GREEN).move_to(count)),run_time=1/15)
        self.finish()


class S07Numbers(SpokenScene):
    def construct(self):
        p=propeller(True).scale(.92).shift(DOWN*.25).rotate(.18);p[0][0].set_color(GREEN);p[0][1:].set_opacity(.18)
        self.add(p,label('38 per subunit',color=GREEN,size=36),note('schematic · 38 blocks in each arm'))
        self.at('the three')
        total=ValueTracker(38)
        counter=always_redraw(lambda:M(str(round(total.get_value())),48,BLUE).move_to([4.7,1,0]))
        self.add(counter,T('channel total',26,BLUE).move_to([4.5,.2,0]))
        self.play(p[0][1:].animate.set_opacity(1).set_color(BLUE),total.animate.set_value(114),run_time=.8)
        self.at('channel holds 114')
        self.play(FadeIn(T('3 × 38 = 114',38,BLUE).move_to([3.5,-2.7,0])),run_time=.5)
        self.finish()


class S08Apart(SpokenScene):
    def construct(self):
        self.add(label('Keep the two numbers apart'),note('schematic icons'))
        for x,num,title,full in [(-3.2,'38','one subunit (protomer)',False),(3.2,'114','one channel (trimer)',True)]:
            icon=propeller().scale(.45)
            if not full: icon[0][1:].set_opacity(.1)
            icon.move_to([x,1.25,0])
            self.add(RoundedRectangle(width=5.8,height=5.7,color=BLUE).move_to([x,-.15,0]),icon,M(num,82,BLUE).move_to([x,-.75,0]),T(title,27,BLUE).move_to([x,-2,0]))
        self.finish()


class S09Dome(SpokenScene):
    def construct(self):
        h=ValueTracker(0);self.add(always_redraw(lambda:cap(h.get_value(),y=1.7,sc=.34,blades=True)),label('Curved blades bow the membrane',color=BLUE),note('side view · schematic'))
        self.at('the curved blades')
        self.play(h.animate.set_value(10),run_time=1.6)
        self.finish()


class S10Size(SpokenScene):
    def construct(self):
        self.add(cap(y=1.5,sc=.34,blades=True),label('purified mouse PIEZO2',color=BLUE),note('side view · schematic'))
        self.at('about 28')
        self.play(FadeIn(VGroup(DoubleArrow([-4.76,2.15,0],[4.76,2.15,0],buff=0,color=GREY),T('28 nm across',28).move_to([0,2.65,0]))),run_time=.3)
        self.at('and 10 deep')
        self.play(FadeIn(VGroup(DoubleArrow([5.05,1.5,0],[5.05,-1.9,0],buff=0,color=GREY),T('10 nm\ndeep',28).move_to([5.8,-.2,0]))),run_time=.3)
        self.wait(3)
        self.finish()


class S11Surface(SpokenScene):
    def construct(self):
        # Oblique projection of the same spherical cap, tiled across its surface.
        a,h,sc=14,10,.35
        R=(a*a+h*h)/(2*h)
        limit=np.arcsin(a/R)
        def point(theta,phi):
            r=R*np.sin(theta)
            return np.array([sc*r*np.cos(phi),1.0+.24*sc*r*np.sin(phi)-sc*(R*np.cos(theta)-(R-h)),0])
        surface=VGroup()
        for lo,hi in zip(np.linspace(0,limit,19)[:-1],np.linspace(0,limit,19)[1:]):
            for phi in np.linspace(0,TAU,65)[:-1]:
                nxt=phi+TAU/64
                surface.add(Polygon(point(lo,phi),point(hi,phi),point(hi,nxt),point(lo,nxt),
                    stroke_width=0,fill_color=BLUE,fill_opacity=.65+.2*(1-np.sin(phi))/2))
        rim=Ellipse(width=2*a*sc,height=2*a*sc*.24,color=BLUE,stroke_width=3).move_to([0,1,0])
        self.add(surface.copy().set_fill(opacity=.15),rim,label('Two areas of a dome'),
            note('idealized spherical cap · oblique view'))
        self.at('its surface area')
        self.play(FadeIn(surface),FadeIn(T('surface area',32,BLUE).move_to([0,-2.95,0])),run_time=.6)
        self.finish()


class S12Projected(SpokenScene):
    def construct(self):
        self.add(cap(y=1.9,sc=.24),label('Light from above',color=YELLOW,size=28),note('idealized cap · side view and shadow plane'))
        self.at('its shadow')
        rays=VGroup(*[Arrow([x,2.65,0],[x,1.95,0],buff=0,color=YELLOW,stroke_width=3) for x in [-3,-1.5,0,1.5,3]])
        self.play(FadeIn(rays),FadeIn(disc(sc=.24,y=-1.65)),run_time=.6)
        self.add(T('surface area',28,BLUE).move_to([4.6,.7,0]),Line([3.5,.7,0],[2.3,.15,0],color=BLUE))
        self.at('the area it occupies')
        self.play(FadeIn(T('projected area (shadow)',30,PURPLE).move_to([0,-2.85,0])),Create(Line([0,-2.5,0],[0,-2.05,0],color=PURPLE)),run_time=.4)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        self.add(cap(y=1.45,sc=.36),label('Smooth cap · rim radius 14 nm · depth 10 nm',size=28),note('idealized spherical cap · side view'))
        self.at('flatten it without')
        self.play(Transform(self.mobjects[1],label('Flatten it without stretching it',3.2)),run_time=.4)
        self.at('does its shadow')
        self.play(FadeIn(label('Shadow bigger or smaller? By how much?',2.5,PURPLE,30)),FadeIn(T('rim radius 14 nm',28,BLUE).move_to([0,1.95,0])),FadeIn(T('depth 10 nm',28,BLUE).move_to([0,-2.7,0])),run_time=.4)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction());self.wait(5)


class S15Reveal(SpokenScene):
    def construct(self):
        self.add(area_cap(),note('idealized cap · side view (left), top view (right)'))
        self.at('it grows')
        self.play(FadeIn(label('It grows.',color=GREEN,size=36)),run_time=.3)
        self.at('the curved cap')
        self.play(FadeIn(T('surface = π(a² + h²)\n= π(14² + 10²)\n≈ 930 nm²',28,BLUE).move_to([-3.3,2.2,0])),run_time=.4)
        self.at('a shadow of about')
        self.play(FadeIn(area_disc()),FadeIn(T('πa² = π × 14²\n≈ 616 nm²',30,PURPLE).move_to([3.2,-.15,0])),run_time=.5)
        self.finish()


class S16Flat(SpokenScene):
    def construct(self):
        h=ValueTracker(10)
        self.add(always_redraw(lambda:area_cap(h.get_value())),always_redraw(lambda:area_disc(np.sqrt(296-h.get_value()**2))),area_old(),T('616 nm²',28,PURPLE).move_to([3.2,-.15,0]),note('idealized cap · side view (left), top view (right)'))
        self.at('flattened')
        self.play(h.animate.set_value(0),run_time=2)
        self.at('about 930')
        self.play(FadeIn(T('surface: 930 nm²',28,BLUE).move_to([-3.3,2,0])),FadeIn(T('930 nm²',28,PURPLE).move_to([3.2,2.9,0])),Create(Line([3.2,2.65,0],[3.2,2.4,0],color=PURPLE)),run_time=.4)
        self.at('the gain is')
        self.play(FadeIn(T('gain ≈ 310 nm²',30,GREEN).move_to([-3.3,-1.8,0])),FadeIn(T('(πh² = 314 nm²)',28,GREEN).move_to([-3.3,-2.4,0])),run_time=.4)
        self.finish()


class S17Hold(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(flat_result());self.wait(3)


class S18Depth(SpokenScene):
    def construct(self):
        h=ValueTracker(10)
        def example(a,x):
            outer=disc(np.sqrt(a*a+100-h.get_value()**2),x,-1.1,.15).set_fill(GREEN,opacity=.9).set_stroke(GREEN)
            inner=disc(a,x,-1.1,.15).set_fill(PURPLE,opacity=1)
            edge=DashedVMobject(disc(a,x,-1.1,.15).set_fill(opacity=0),num_dashes=40)
            return VGroup(cap(h.get_value(),a=np.sqrt(a*a+100-h.get_value()**2),x=x,y=1.5,sc=.15),outer,inner,edge)
        self.add(always_redraw(lambda:example(11,-3.2)),always_redraw(lambda:example(17,3.2)),
            label('gain = πh² = π × 10² ≈ 314 nm²',3.15,GREEN,30),
            label('depth, not width',2.55,GREEN,28),
            note('idealized caps · same depth, different widths'))
        for x in [-3.2,3.2]:
            self.add(T('initial depth 10 nm',28,BLUE).move_to([x,2.0,0]),
                chip('314 nm² gained',GREEN,28).move_to([x,-2.45,0]))
        self.at('the gain depends')
        self.play(h.animate.set_value(0),run_time=1.2)
        self.at('not on how wide')
        self.play(Indicate(self.mobjects[3],color=GREEN,scale_factor=1.04),run_time=.3)
        self.finish()


class S19Idealized(SpokenScene):
    def construct(self):
        self.add(cap(x=-3.2,y=1.7,sc=.19),cap(x=3.2,y=1.7,sc=.19,blades=True),label('Idealized geometry versus the real dome',size=30),T('IDEALIZED',34,RED).move_to([-3.2,.6,0]),T('not a measurement',28,RED).move_to([-3.2,-1.6,0]),T('protein blades\n+ bent lipid',30,BLUE).move_to([3.2,-1.6,0]),Line([0,-2.6,0],[0,2.4,0],color=GREY),note('right: schematic cartoon, not an atomic structure'))
        self.at('idealized geometry')
        self.play(Indicate(self.mobjects[3],color=RED),run_time=.5)
        self.at('protein blades')
        self.play(Indicate(self.mobjects[1],color=BLUE),run_time=.5)
        self.finish()


class S20Favours(SpokenScene):
    def construct(self):
        h=ValueTracker(10)
        self.add(always_redraw(lambda:area_cap(h.get_value())),always_redraw(lambda:area_disc(np.sqrt(296-h.get_value()**2))),area_old(),note('idealized cap · side view (left), top view (right)'))
        self.at('flattening increases')
        self.play(h.animate.set_value(0),run_time=1.7)
        self.at('anything that favors')
        self.play(FadeIn(T('favours more\nprojected area',30,PURPLE).move_to([-3.3,-1.6,0])),run_time=.4)
        self.at('favors the flat state')
        self.play(Create(Arrow([-3.3,-.8,0],[-3.3,.8,0],buff=0,color=PURPLE)),FadeIn(T('flat state',32,BLUE).move_to([-3.3,2,0])),run_time=.4)
        self.finish()


def pore(x,y,opened=False):
    mask=Rectangle(width=1.2,height=.55,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    gap=.5 if opened else .18
    gates=VGroup(*[Rectangle(width=.34,height=.6,color=GREEN if opened else RED,fill_color=GREEN if opened else RED,fill_opacity=1).move_to([x+d,y,0]) for d in [-gap,gap]])
    return VGroup(mask,gates)


class S21Model(SpokenScene):
    def construct(self):
        self.add(label('Proposed coupling · leading model',color=BLUE),label('still debated',2.5,RED,30),note('schematic · pore states shown for contrast'))
        self.add(cap(x=-3.3,y=1.6,sc=.16),pore(-3.3,0),T('curved · pore closed',28,RED).move_to([-3.3,-1.2,0]))
        gate=pore(3.2,1.6)
        self.add(cap(0,x=3.2,y=1.6,sc=.16),gate,T('flattened',28,BLUE).move_to([3.2,.65,0]))
        self.at('help open')
        self.play(gate[1][0].animate.shift(LEFT*.32).set_color(GREEN),gate[1][1].animate.shift(RIGHT*.32).set_color(GREEN),FadeIn(T('pore open',32,GREEN).move_to([3.2,-1.2,0])),Create(Arrow([-1,-2.2,0],[1.2,-2.2,0],color=BLUE)),run_time=.7)
        self.finish()


class S22Takeaway(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=11.5,height=5.8,corner_radius=.2,color=BLUE),
            label('Leading model',2.15,BLUE,34),
            T('Area gain',72,PURPLE).move_to([0,.35,0]),
            label('from flattening a curved membrane',-1.35,BLUE,32))
        self.at('a dome is a device')
        self.play(Indicate(self.mobjects[2],color=PURPLE,scale_factor=1.04),run_time=.7)
        self.finish()


class S23End(EndCard):
    LINE='A dome is a device for gaining area.'
    def construct(self):
        self.add(VGroup(T('A dome is a device',48,font=TITLE_FONT),T('for gaining area.',48,font=TITLE_FONT)).arrange(DOWN,buff=.15),label('In the leading model',2,BLUE,32),label('biochemistrypedia.com',-2,TEAL,26))
        self.finish()
