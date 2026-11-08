"""The Sixty-Fold Gap: revised, word-synchronized schematic animation.
COLOR MAP: BLUE channel/patch fit; GREY membrane; YELLOW tension;
PURPLE projected area; GREEN computed prediction/average; RED uncertainty;
GOLD title rule. All curves are computed, never hand-drawn data.
Population: fixed logistic-quantile offsets, common Boltzmann slope factor.
Footprint: illustrative linear-elastic exponential relaxation, not published data.
"""
import numpy as np
from bp_style import *

PURPLE='#B58CD9'
K_STRUCT=4.1/300
TH0=1.239
L_CAP=5.4


def label(s,x=0,y=0,size=28,color=TEXT):
    return (MarkupText(s.replace('kᵦ','k<sub>B</sub>'),font=FONT,font_size=size,color=color) if 'kᵦ' in s else T(s,size,color)).move_to([x,y,0])


def logistic(t,t50=2.7,k=.8):
    return 1/(1+np.exp(np.clip((t50-t)/k,-700,700)))


def cap_pts(theta,sc=1,cx=0,y0=0):
    th=max(float(theta),.001); r=L_CAP/(2*th)
    return [[cx+sc*r*np.sin(p), y0+sc*r*(np.cos(p)-np.cos(th)),0]
            for p in np.linspace(-th,th,101)]


def dome(theta=TH0,sc=1,cx=0,y0=0,half=2.9,w=9):
    p=cap_pts(theta,sc,cx,y0)
    return VGroup(Line([cx-half,y0,0],p[0],color=GREY,stroke_width=w),
                  VMobject(stroke_color=BLUE,stroke_width=w).set_points_as_corners(p),
                  Line(p[-1],[cx+half,y0,0],color=GREY,stroke_width=w))


def area_disc(x,y,outer=1.15,inner=.9):
    return VGroup(Circle(outer,color=PURPLE,fill_color=PURPLE,fill_opacity=.45,stroke_width=3),
        Circle(inner,color=BLUE,fill_color=BG,fill_opacity=1,stroke_width=3)).move_to([x,y,0])


def classes():
    return VGroup(dome(sc=1.25,cx=-3.2,y0=0).stretch(1.25,1,about_point=[0,0,0]),
        dome(0,sc=1.25,cx=3.2,y0=0),
        label('curved class · 7WLT',-3.2,3.2,28,BLUE),
        label('flattened class · 7WLU',3.2,3.2,28,BLUE),
        Circle(.9,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([-3.2,-1.85,0]),
        VGroup(Annulus(inner_radius=.9,outer_radius=1.25,color=PURPLE,fill_opacity=.6,stroke_width=0),
            Circle(.9,color=BLUE,fill_color=BLUE,fill_opacity=.15)).move_to([3.2,-1.85,0]),
        label('side views',0,-.5,26,GREY),
        label('top views: projected area',0,-3.45,26,GREY))


def plot_axes():
    ax=Axes(x_range=[0,6,1],y_range=[0,1,.5],x_length=11.1,y_length=4.45,
        axis_config={'color':GREY,'include_tip':False,'tick_size':.06}).move_to([.25,-.1,0])
    ticks=VGroup(*[M(str(i),26,GREY).next_to(ax.c2p(i,0),DOWN,buff=.12) for i in range(7)],
        *[M(s,26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.14) for s,v in [('.5',.5),('1',1)]])
    return ax,VGroup(ax,ticks,label('tension (mN/m)',.3,-3.1,28,YELLOW),label('normalized current',-6.45,-.1,26,GREY).rotate(PI/2))


def curve(ax,t50=2.7,k=.8,color=BLUE,width=6):
    return ax.plot(lambda t:logistic(t,t50,k),x_range=[0,6,.002],color=color,stroke_width=width,use_smoothing=False)


def prediction_frame():
    g=VGroup(label('How steep would the current curve be?',0,3.3,34),
        label('k = kᵦT / ΔA     ΔA = 300 nm²',0,2.55,36,PURPLE))
    for x,title,col in [(-3.25,'measured patch fit',BLUE),(3.25,'your prediction here',GREEN)]:
        ax=Axes(x_range=[0,6,1],y_range=[0,1,.5],x_length=5.1,y_length=3.9,
            axis_config={'color':GREY,'include_tip':False,'tick_size':.06}).move_to([x,-.45,0])
        if x<0: g.add(ax,curve(ax))
        else: g.add(VGroup(*[DashedLine(a.get_start(),a.get_end(),dash_length=.12,color=GREY) for a in [ax.x_axis,ax.y_axis]]))
        g.add(*[M(str(i),26,GREY).next_to(ax.c2p(i,0),DOWN,buff=.12) for i in range(7)],
            *[M(v,26,GREY).next_to(ax.c2p(0,y),LEFT,buff=.12) for v,y in [('.5',.5),('1',1)]],
            label(title,x,1.95,28,col),label('tension (mN/m)',x,-3.05,28,YELLOW),
            label('normalized current',x-3.15,-.45,26,GREY).rotate(PI/2))
    return g


def width_bracket(ax,lo,hi,y,color):
    a=ax.c2p(lo,y); b=ax.c2p(hi,y)
    return VGroup(Line(a,b,color=color,stroke_width=4),
        Line(a+DOWN*.12,a+UP*.12,color=color,stroke_width=4),
        Line(b+DOWN*.12,b+UP*.12,color=color,stroke_width=4))


def comparison(show_title=True):
    ax,g=plot_axes()
    p=curve(ax,1.9,K_STRUCT,GREEN); m=curve(ax)
    wp=width_bracket(ax,1.9-2.197*K_STRUCT,1.9+2.197*K_STRUCT,.76,GREEN)
    wm=width_bracket(ax,2.7-2.197*.8,2.7+2.197*.8,.075,BLUE)
    lp=label('0.06 mN/m',-.3,1.55,28,GREEN)
    lead=Line(lp.get_left()+LEFT*.1,ax.c2p(1.9,.76)+RIGHT*.12,color=GREEN)
    lm=label('3.5 mN/m',.1,-1.5,28,BLUE)
    top=label('3.5 / 0.06 ≈ 60',0,3.2,38,PURPLE)
    foot=VGroup(label('calculated from structure + stiffness: T₅₀ = 1.9 mN/m',0,2.65,26,GREEN),
        label('patch fit: T₅₀ = 2.7 mN/m;  k = 0.8 mN/m',0,-3.5,26,BLUE))
    # Resolve the narrow width in a labeled inset; the original brackets retain their shared scale.
    za=Axes(x_range=[1.8,2,.1],y_range=[0,1,1],x_length=2.45,y_length=1.25,
        axis_config={'color':GREY,'include_tip':False,'tick_size':.04}).move_to([-3.65,1.05,0])
    zoom=VGroup(RoundedRectangle(width=3.3,height=2.7,corner_radius=.12,
            color=GREY,fill_color=BG,fill_opacity=1).move_to([-3.65,1.05,0]),
        za,za.plot(lambda t:logistic(t,1.9,K_STRUCT),x_range=[1.8,2,.0005],color=GREEN,use_smoothing=False),
        label('tension zoom ×6.6',-3.65,2.1,23,GREY),
        width_bracket(za,1.9-2.197*K_STRUCT,1.9+2.197*K_STRUCT,.55,GREEN),
        label('0.06 mN/m',-3.65,.0,26,GREEN),
        label('1.8        1.9        2.0',-3.65,.24,22,GREY))
    return ax,VGroup(g,p,m,wp,wm,lp,lead,lm,foot,top if show_title else VGroup(),zoom)


def slot_header(n,text):
    return VGroup(chip(str(n),RED,size=28).move_to([-5.8,3.25,0]),label(text,.25,3.25,32))


def population_frame():
    ax,g=plot_axes()
    offsets=2.7+.8*np.log(np.linspace(.08,.92,9)/(1-np.linspace(.08,.92,9)))
    cs=VGroup(*[curve(ax,t,K_STRUCT,BLUE,4).set_stroke(opacity=.7) for t in offsets])
    ticks=VGroup(*[Line(ax.c2p(t,0)+DOWN*.12,ax.c2p(t,0)+UP*.22,color=YELLOW,stroke_width=4) for t in offsets])
    return ax,g,cs,ticks


def footprint(bent=True):
    p=cap_pts(TH0,1.4,0,.0); a=p[-1][0]
    cap=VMobject(stroke_color=BLUE,stroke_width=12).set_points_as_corners(p)
    skirts=VGroup()
    for sign in [-1,1]:
        pts=[[sign*(a+x),-1.6*(1-np.exp(-x/1.15)) if bent else 0,0] for x in np.linspace(0,6-a,100)]
        skirts.add(VMobject(stroke_color=GREY,stroke_width=10).set_points_as_corners(pts))
    return VGroup(cap,skirts,label('Piezo',0,2.35,30,BLUE),
        label('membrane footprint · elasticity model (2018)',0,3.3,30),
        label('illustrative side view',0,-3.5,26,GREY))


class S00Title(TitleCard):
    LESSON='Piezo Channels and the Physics of Force'
    TITLE='The Sixty-Fold Gap'
    def construct(self):
        self.add(label(self.LESSON,0,1.2,30,GREY),label(self.TITLE,0,0,56),
            Line([-2,-.9,0],[2,-.9,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(label('Structural comparison vs two-state reading of the current',0,3.1,28,GREY),
            label('structural comparison',-3.2,-.8,28,GREY),label('effective two-state area',3.2,-.8,28,GREY))
        self.at('gains hundreds')
        self.play(FadeIn(label('300 nm²',-3.2,.6,80,PURPLE)),run_time=.35)
        self.at('about five')
        q=label('Do they describe the same change?',0,-2.55,38)
        self.play(FadeIn(label('5 nm²',3.2,.6,80,PURPLE)),FadeIn(q),run_time=.35)
        self.at('Do they describe')
        self.play(Indicate(q,scale_factor=1.02),run_time=.35)
        self.finish()


class S02Yang(SpokenScene):
    def construct(self):
        v=Circle(2.35,color=GREY,stroke_width=10)
        particles=VGroup(*[chip('Piezo1',BLUE,size=26).move_to([2.2*np.cos(t),2.2*np.sin(t),0]) for t in [.4,2,3.6,5.2]])
        for part in particles: part[0].set_fill(BG,opacity=1)
        self.add(v,particles,label('Yang and colleagues, 2022',0,3.3,36),label('lipid vesicle',0,-2.9,30,GREY),label('cryo-EM',4.65,2.3,32))
        self.at('purified mouse')
        self.play(Indicate(particles,scale_factor=1.04),run_time=.5)
        self.at('microscopy sorted it')
        bins=VGroup(*[VGroup(RoundedRectangle(width=4.5,height=3.1,color=GREY),
            label('class '+c,y=.95,size=30,color=BLUE),dome(theta,sc=.63,y0=-.4,half=1.8)).move_to([x,-.1,0])
            for c,theta,x in [('A',TH0,-3),('B',0,3)]])
        self.play(FadeOut(v),FadeOut(self.mobjects[3]),FadeIn(bins),*[part.animate.move_to([xx,-1.2,0]) for part,xx in zip(particles,[-3.75,-2.25,2.25,3.75])],run_time=.8)
        self.at('from one sample')
        self.play(FadeIn(label('two resolved classes · one sample',0,-2.2,32)),run_time=.4)
        self.finish()


class S03Classes(SpokenScene):
    def construct(self):
        g=classes(); self.add(g)
        self.at('Between them was')
        self.play(Indicate(g[5],scale_factor=1.06),run_time=.6)
        self.at('300 square')
        self.play(FadeIn(label('≈ 300 nm²',0,-1.85,37,PURPLE)),run_time=.4)
        self.finish()


class S04Hedge(SpokenScene):
    def construct(self):
        g=classes(); self.add(g,label('≈ 300 nm²',0,-1.85,37,PURPLE))
        self.at('Their abstract hedges')
        tag=VGroup(label('Yang et al. hedge:',3.2,1.68,28,RED),label('gating transition?',3.2,1,30,RED))
        self.play(FadeIn(tag),run_time=.5); self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        self.add(prediction_frame()); self.at('coupled to opening')
        self.play(Indicate(self.mobjects[0][1],scale_factor=1.03),run_time=.6); self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction_frame(),label('Pause and predict',0,-3.55,32,YELLOW))
        ring=Circle(.32,color=YELLOW).move_to([5.9,-3.45,0]); self.add(ring)
        self.wait(5)


class S07Reveal(SpokenScene):
    def construct(self):
        self.add(label('Nearly vertical',0,3.3,38,GREEN),label('k: Boltzmann slope factor',-1.45,2.45,36),
            label('kᵦT = 4.1 × 10⁻²¹ J',-1.45,1.45,36,PURPLE))
        eq=label('k = (4.1 × 10⁻²¹ J)',-1.45,.45,36,PURPLE)
        den=label('÷ (300 × 10⁻¹⁸ m²)',-1.45,-.35,36,PURPLE)
        self.at('Nearly vertical'); self.play(FadeIn(eq),FadeIn(den),run_time=.55)
        self.at('The channel would')
        self.play(FadeIn(label('≈ 0.014 mN/m',-1.45,-1.35,40,GREEN)),run_time=.4)
        # An honest magnification resolves the predicted sigmoid rather than a step.
        ax=Axes(x_range=[1.8,2,.1],y_range=[0,1,.5],x_length=2.4,y_length=4.2,
            axis_config={'color':GREY,'include_tip':False}).move_to([4.65,.2,0])
        c=ax.plot(lambda t:logistic(t,1.9,K_STRUCT),x_range=[1.8,2,.0005],color=GREEN,use_smoothing=False)
        zoom=VGroup(ax,c,label('zoom',4.65,2.65,28,GREEN),label('1.8    1.9    2.0',4.65,-2.3,26,GREY),label('mN/m',4.65,-2.85,26,YELLOW))
        zoom.add(label('normalized current',6.35,.2,26,GREY).rotate(PI/2),*[label(v,3.25,y,26,GREY) for v,y in [('0',-1.9),('.5',.2),('1',2.3)]])
        self.play(FadeIn(zoom),run_time=.6)
        self.at('over a tiny range')
        self.play(FadeIn(label('10–90% width: 4.4k ≈ 0.06 mN/m',-.8,-2.65,36,GREEN)),run_time=.4)
        self.finish()


class S08Compare(SpokenScene):
    def construct(self):
        ax,g=comparison(False); self.add(g)
        self.at('about sixty times')
        self.play(FadeIn(label('3.5 / 0.06 ≈ 60',0,3.2,38,PURPLE)),run_time=.4)
        self.at('tensions are')
        self.play(Indicate(g[8],scale_factor=1.015),run_time=.5)
        self.at('The slopes are')
        self.play(Indicate(VGroup(g[3],g[4]),scale_factor=1.08),run_time=.5); self.finish()


class S09Hold(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(comparison()[1]); self.wait(3)


class S10Geometry(SpokenScene):
    def construct(self):
        h=ValueTracker(10)
        def cap():
            d=max(.001,h.get_value()); a=np.sqrt(296-d*d); r=296/(2*d)
            pts=[[x*.24, .1+.24*(np.sqrt(r*r-x*x)-(r-d)),0] for x in np.linspace(-a,a,101)]
            return VMobject(stroke_color=BLUE,stroke_width=11).set_points_as_corners(pts)
        d=always_redraw(cap)
        self.add(label('Idealized Piezo2 · different paralog · a calculation',0,3.3,30,GREY),d,
            Line([-4.7,.1,0],[4.7,.1,0],color=GREY,stroke_width=5),
            label('a = 14 nm',-2.1,-.7,30,YELLOW),label('h = 10 nm',5.1,1.6,28,YELLOW),
            DoubleArrow([0,.1,0],[0,2.5,0],color=YELLOW,buff=0).shift(RIGHT*3.4))
        area=area_disc(0,-1.8,1.03,.84); self.add(area,label('projected area',-3.6,-1.8,28,PURPLE))
        dims=VGroup(self.mobjects[3],self.mobjects[4],self.mobjects[5])
        radius_arrow=DoubleArrow([-3.36,-.2,0],[0,-.2,0],color=YELLOW,buff=0)
        self.add(radius_arrow); dims.add(radius_arrow)
        self.at('On paper')
        self.play(FadeIn(label('surface ≈ 930 nm²; shadow ≈ 616 nm²',0,-3.25,32)),run_time=.4)
        self.at('dome gains about')
        self.play(h.animate.set_value(0),*[FadeOut(m) for m in dims],area[0].animate.set_fill(opacity=.85),run_time=1.5)
        self.at('square nanometers')
        self.play(FadeIn(label('930 − 616 ≈ 310 nm²',3.4,-1.8,32,PURPLE)),run_time=.4)
        self.finish()


class S11Open(SpokenScene):
    def construct(self):
        self.add(label('Why is the measured switch so shallow?',0,2.9,34))
        slots=VGroup(*[VGroup(RoundedRectangle(width=3.5,height=3.7,color=GREY,stroke_width=3),
            label(str(i+1),y=.85,size=56,color=RED),label(s,y=-.65,size=32)).move_to([x,-.4,0])
            for i,(s,x) in enumerate([('shape',-4.1),('population',0),('structure',4.1)])])
        self.add(slots); self.at('The question is open')
        self.play(FadeIn(label('Open question · three testable answers',0,-3.2,32,RED)),run_time=.4); self.finish()


class S12Spring(SpokenScene):
    def construct(self):
        h=ValueTracker(10)
        def profile(depth):
            depth=max(depth,.001); a=np.sqrt(296-depth*depth); r=296/(2*depth)
            pts=[[x*.31,-1.1+.31*(np.sqrt(r*r-x*x)-(r-depth)),0] for x in np.linspace(-a,a,101)]
            return VMobject(stroke_color=BLUE,stroke_width=9).set_points_as_corners(pts)
        d=always_redraw(lambda:profile(h.get_value()))
        self.add(slot_header(1,'Not two states?'),d,Line([-6,-1.1,0],[6,-1.1,0],color=GREY))
        def spring():
            top=-1.1+.31*h.get_value()
            pts=[[0,-2.2,0],[0,-2,0]]+[[.22*(-1)**i,-2+(top+1.85)*i/12,0] for i in range(13)]+[[0,top,0]]
            return VMobject(stroke_color=GREY,stroke_width=4).set_points_as_corners(pts)
        self.add(always_redraw(spring),Line([-.6,-2.2,0],[.6,-2.2,0],color=GREY))
        ghosts=VGroup(*[profile(v).set_stroke(width=4,opacity=.45) for v in [10,7.5,5,2.5,.001]])
        self.at('the dome may')
        self.play(LaggedStart(*[Create(c) for c in ghosts],lag_ratio=.2),run_time=1.9)
        self.at('If it flattens gradually')
        caption=label('flattens gradually',0,-3.2,34,BLUE); self.add(caption)
        readouts=VGroup()
        for i,v in enumerate([10,7.5,5,2.5,0]):
            yy=2-i*.8 if i<4 else -1.9
            # Round all geometric areas to the same two significant figures as s10.
            gain=int(round(np.pi*(100-v*v)/10)*10)
            readout=label(f'+{gain} nm²',5.15,yy,26,PURPLE)
            readouts.add(Line([.5,-1.1+.31*v,0],readout.get_left()+LEFT*.2,color=PURPLE,stroke_width=2),readout)
        self.play(FadeIn(readouts),h.animate.set_value(0),run_time=2.1)
        self.at('one area no longer')
        self.play(Transform(caption,label('One area no longer describes it',0,-3.2,34,PURPLE)),run_time=.4)
        self.finish()


class S13Population(SpokenScene):
    def construct(self):
        ax,g,cs,ticks=population_frame(); self.add(g,slot_header(2,'A population curve'),ticks)
        self.at('Second')
        self.play(LaggedStart(*[Create(c) for c in cs],lag_ratio=.1),run_time=1.5)
        self.at('Uneven tension across')
        self.play(FadeIn(label('each curve = a channel group, offset in T₅₀',0,2.6,28,BLUE)),run_time=.4)
        self.add(label('illustrative model · yellow ticks mark T₅₀',0,-3.5,26,GREY)); self.finish()


class S14Lowerbound(SpokenScene):
    def construct(self):
        ax,g,cs,ticks=population_frame(); self.add(g,cs,ticks)
        self.at('otherwise identical')
        a=chip('identical switches',GREY,size=26).move_to([-4.3,3.2,0]); self.play(FadeIn(a),run_time=.4)
        self.at('at equilibrium')
        b=chip('equilibrium',GREY,size=26).move_to([-.5,3.2,0]); self.play(FadeIn(b),run_time=.4)
        self.at('fixed offsets')
        c=chip('fixed T₅₀ offsets',GREY,size=26).move_to([3.5,3.2,0]); self.play(FadeIn(c),run_time=.4)
        self.add(label('illustrative model · normalized current',0,2.55,28,GREY))
        u=(np.arange(1501)+.5)/1501; offsets=2.7+.8*np.log(u/(1-u))
        avg=ax.plot(lambda t:float(np.mean(logistic(t,offsets,K_STRUCT))),x_range=[0,6,.012],color=GREEN,stroke_width=8,use_smoothing=False)
        self.at('Then averaging broadens')
        self.play(cs.animate.set_stroke(opacity=.22),Create(avg),run_time=1.1)
        # Wide blue dashes remain visible around the green average even where the fits coincide.
        measured=DashedVMobject(curve(ax,width=13),num_dashes=32,dashed_ratio=.5)
        self.play(Create(measured),FadeIn(label('green: average     blue dashes: patch fit',0,-3.5,26)),run_time=.65)
        head=VGroup(a,b,c)
        self.at('underestimates their common')
        result=label('Slope-derived area < common opening area',0,3.2,32,PURPLE)
        self.play(*[FadeOut(m) for m in head],run_time=.2)
        self.remove(a,b,c,head)
        self.play(FadeIn(result),run_time=.2)
        self.at('Outside that model')
        self.play(Transform(result,label('Effective area · not a guaranteed bound',0,3.2,32,RED)),run_time=.5)
        self.at('And the published curve')
        self.play(Transform(result,label('Published fit also pools different patches',0,3.2,32,BLUE)),run_time=.5)
        self.finish()


class S15Flattened(SpokenScene):
    def construct(self):
        self.add(slot_header(3,'Flattened does not establish open'))
        boxes=VGroup(*[RoundedRectangle(width=5.6,height=5.5,color=GREY,stroke_width=3).move_to([x,-.2,0]) for x in [-3.55,3.55]])
        # Both visual counterparts are present before the narrator questions the equivalence.
        tr=VMobject(stroke_color=GREEN,stroke_width=6).set_points_as_corners([[1.15,-.8,0],[2.1,-.8,0],[2.1,.65,0],[3.9,.65,0],[3.9,-.8,0],[5.95,-.8,0]])
        self.add(boxes,dome(0,sc=.93,cx=-3.55,y0=-.05,half=2.45),tr,
            label('flattened class',-3.55,1.85,32,BLUE),label('schematic',-3.55,-2.2,26,GREY),
            label('current recording',3.55,1.85,32,GREEN),label('schematic I(t)',3.55,-2.2,26,GREY))
        self.at('may not be')
        self.play(FadeIn(label('?',0,-.2,64,RED)),run_time=.2)
        self.at('A structure is not')
        self.add(label('A structure is not a current recording',0,-3.25,34,RED)); self.finish()


class S16Footprint(SpokenScene):
    def construct(self):
        flat=footprint(False); bent=footprint(True)
        self.add(flat,label('Haselwandter & MacKinnon',0,-2.75,28,GREY))
        self.at('the membrane bends away')
        self.play(Transform(flat[1],bent[1]),run_time=1)
        tag=label('footprint',4.4,-.2,30,GREY)
        self.play(FadeIn(tag),Create(Line([4.4,-.55,0],[4.4,-1.22,0],color=GREY)),run_time=.4)
        self.finish()


class S17Work(SpokenScene):
    def construct(self):
        shape=footprint()
        # Reserve a separate row above Piezo for the work caption.
        shape[3].move_to([0,3.55,0]).scale(.9)
        self.add(shape,label('footprint',4.55,-.4,30,GREY))
        self.at('That skirt reaches')
        self.play(Create(DoubleArrow([-6,-2.65,0],[6,-2.65,0],color=GREY,buff=0)),
            FadeIn(label('span of the membrane footprint',0,-3.05,28,GREY)),run_time=.6)
        self.at('so tension does work')
        a=cap_pts(TH0,1.4)[-1][0]
        arrows=VGroup(*[Arrow([s*x,y,0],[s*(x+.9),y-.2,0],buff=0,color=YELLOW,stroke_width=7,
            max_tip_length_to_length_ratio=.3) for s in [-1,1] for x,y in [(3.3,-.55),(4.8,-1.1)]])
        self.play(FadeIn(arrows),run_time=.5)
        self.at('as well as on')
        rim=VGroup(*[Arrow([s*(a-.25),.2,0],[s*(a+.7),.2,0],buff=0,color=YELLOW,stroke_width=7,
            max_tip_length_to_length_ratio=.3) for s in [-1,1]])
        bracket=VGroup(Line([-6.2,-2.1,0],[6.2,-2.1,0],color=YELLOW,stroke_width=4),
            Line([-6.2,-1.7,0],[-6.2,-2.1,0],color=YELLOW,stroke_width=4),
            Line([6.2,-1.7,0],[6.2,-2.1,0],color=YELLOW,stroke_width=4))
        self.play(FadeIn(rim),FadeIn(label('work done here: footprint + channel',0,2.95,28,YELLOW)),
            shape[0].animate.set_color(YELLOW),shape[1].animate.set_color(YELLOW),Create(bracket),run_time=.5)
        self.finish()


class S18Apart(SpokenScene):
    def construct(self):
        self.add(label('Keep the two apart',0,3.2,40,RED))
        a=VGroup(RoundedRectangle(width=5.8,height=5.5,color=GREY),
            label('elasticity model',y=1.85,size=34),label('cap surface area',y=.85,size=30,color=PURPLE),
            label('≈ 390 nm²',y=.05,size=48,color=PURPLE),label('radius of curvature',y=-.95,size=29,color=BLUE),
            label('10.2 nm',y=-1.6,size=36,color=BLUE),label('model inputs',y=-2.25,size=28,color=GREY)).move_to([-3.05,-.3,0])
        b=VGroup(RoundedRectangle(width=5.8,height=5.5,color=GREY),label('structural comparison',y=1.85,size=31),
            label('≈ 300 nm²',y=.2,size=54,color=PURPLE),label('in-plane expansion',y=-1.25,size=30,color=GREY)).move_to([3.05,-.3,0])
        self.add(a); self.at('not the structural'); self.play(FadeIn(b),run_time=.4); self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        self.add(label('Open problem',0,3.2,42,RED),label('5 nm²',-3.2,1.25,78,PURPLE),
            label('effective two-state area',-3.2,.1,28,GREY),label('structural difference',3.2,.1,28,GREY))
        self.at('nor hundreds'); self.play(FadeIn(label('300 nm²',3.2,1.25,78,PURPLE)),run_time=.3)
        self.at('has been shown')
        line=label('Neither is established as the opening area',0,-1.1,34,RED)
        self.play(FadeIn(line),run_time=.4)
        self.at('The structural expansion')
        self.play(Transform(line,label('The structural difference is observed',0,-1.1,34,GREEN)),
            FadeIn(label('Which part opens the pore?',0,-2.65,44)),run_time=.4)
        self.finish()


class S20End(EndCard):
    LINE='Which part of the 300 nm² couples to opening is still open.'
    def construct(self):
        self.add(label('Which part of the 300 nm²',0,.85,44),label('couples to opening is still open.',0,-.15,44),label('biochemistrypedia.com',0,-1.65,28,TEAL))
        self.finish()
