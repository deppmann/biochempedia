"""Reading a Patch — revised, model-computed animation.
COLOR MAP: BLUE current/channels; GREY apparatus/membrane; YELLOW tension;
PURPLE area; GREEN computed results/recovery; RED caution; GOLD title rule.
Geometry is schematic, never a molecular structure.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as HouseSpokenScene
PURPLE = '#B58CD9'
config.background_color = BG

# Keep audio boundaries exact: the house finish adds a tail to every scene,
# which otherwise accumulates into several seconds of narration/scene drift.
class SpokenScene(HouseSpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        remaining = self.t_of(phrase, nth) - lead - self.elapsed()
        if remaining > .02:
            self.wait(remaining)
    def finish(self):
        remaining = self.narration_s - self.elapsed()
        if remaining > .02:
            self.wait(remaining)

def txt(s, x=0, y=0, size=30, color=TEXT):
    return T(s, size, color).move_to([x,y,0])

def formula(s, x=0, y=0, size=32, color=TEXT):
    # Pango subscripts, including the multi-letter absolute-temperature suffix.
    s = s.replace('k_B', 'k<sub>B</sub>').replace('T_abs', 'T<sub>abs</sub>')
    s = s.replace('ΔA_eff', 'ΔA<sub>eff</sub>').replace('ΔG₀,eff', 'ΔG₀,<sub>eff</sub>')
    return MarkupText(s, font=FONT, font_size=size, color=color).move_to([x,y,0])

def boltzmann(t, mid=2.7, k=.8):
    return 1/(1+np.exp((mid-t)/k))

def plot(x=0, y=0, w=10.4, h=4.9, xmax=6, step=1):
    ax=Axes(x_range=[0,xmax,step], y_range=[0,1,.5], x_length=w,y_length=h,
            axis_config=dict(color=GREY,include_tip=False,stroke_width=2,tick_size=.06))
    # Explicit range endpoints; Axes adds margins around the numerical origin.
    ax.shift(np.array([x-w/2,y-h/2,0])-ax.c2p(0,0))
    ticks=VGroup(*[formula(str(i),size=26).next_to(ax.c2p(i,0),DOWN,buff=.12)
                         for i in range(0,xmax+1,step)],
                 *[formula(s,size=26).next_to(ax.c2p(0,v),LEFT,buff=.12)
                         for s,v in [('0',0),('0.5',.5),('1',1)]])
    names=VGroup(txt('I / Imax',x-w/2+.6,y+h/2+.38,26,BLUE),
                 txt('Tension (mN/m)',x,y-h/2-.85,26,YELLOW))
    return ax,VGroup(ax,ticks,names)

def curve(ax, mid=2.7, color=BLUE, xmax=6):
    return ax.plot(lambda t:boltzmann(t,mid),x_range=[0,xmax,.025],color=color,stroke_width=5)

def current_frame():
    ax,base=plot(y=-.05,h=3.95)
    p=ax.c2p(2,boltzmann(2))
    point=VGroup(DashedLine(ax.c2p(2,0),p,color=GREEN),DashedLine(ax.c2p(0,boltzmann(2)),p,color=GREEN),
                 Dot(p,color=GREEN,radius=.1),txt('29%',-1.1,.05,34,GREEN),
                 txt('2.0 (from s07)',-1.73,-2.86,26,GREEN))
    # The marked x label replaces the ordinary tick at 2.
    base[1][2].set_opacity(0)
    base[2][1].move_to([2.5,-2.86,0])
    calc=formula('I/Imax = 1 / [1 + exp((2.7 − 2.0)/0.8)]',y=3.2,size=29)
    result=formula('= 1/(1 + e⁰·⁸⁷⁵) ≈ 1/3.40 ≈ 0.29   (fit values)',y=-3.45,size=27,color=GREEN)
    return base,curve(ax),calc,point,result

# Circle and cap share exactly the same centre and radius.
CENTER=np.array([-2.6,-.9,0]); RAD=2.65; HALF=2.05
EDGE=CENTER[1]+np.sqrt(RAD**2-HALF**2)
def patch(bulge=True):
    xx=np.linspace(-HALF,HALF,100)
    yy=np.sqrt(RAD**2-xx**2)+CENTER[1] if bulge else np.full_like(xx,EDGE)
    cap=VMobject(color=GREY,stroke_width=8).set_points_as_corners(
        [np.array([CENTER[0]+x,y,0]) for x,y in zip(xx,yy)])
    walls=VGroup(*[Line([CENTER[0]+s*HALF,EDGE,0],[CENTER[0]+s*2.55,3.0,0],color=GREY,stroke_width=5) for s in [-1,1]])
    # Lower cell boundary remains visibly attached to both seal points.
    body=VMobject(color=GREY,stroke_width=4).set_points_as_corners([
        [CENTER[0]-HALF,EDGE,0],[-5.7,-.2,0],[-5.5,-2.6,0],[-.1,-2.6,0],[.2,-.2,0],[CENTER[0]+HALF,EDGE,0]])
    ch=VGroup(*[RoundedRectangle(width=.3,height=.48,corner_radius=.05,color=BLUE,fill_opacity=.65,fill_color=BLUE)
                .move_to([CENTER[0]+a,np.sqrt(RAD**2-a*a)+CENTER[1] if bulge else EDGE,0]) for a in [-1,0,1]])
    return VGroup(body,walls,cap,ch)

def radius(text='R = radius of curvature'):
    end=CENTER+np.array([RAD*np.cos(.9),RAD*np.sin(.9),0])
    r=VGroup(Dot(CENTER,color=BLUE,radius=.06),Line(CENTER,end,color=BLUE,stroke_width=3))
    r.add(txt(text,-2.5,-1.6,27,BLUE))
    return r

def pressure():
    return Arrow([-2.6,3.0,0],[-2.6,1.95,0],buff=0,color=YELLOW,stroke_width=6)

def cell_view():
    cell=Ellipse(width=7.4,height=5.45,color=GREY,stroke_width=7).move_to([-1,-.35,0])
    channels=VGroup(*[RoundedRectangle(width=.33,height=.5,corner_radius=.05,color=BLUE,fill_color=BLUE,fill_opacity=.6)
                      .move_to([x,-.35+2.725*np.sqrt(1-((x+1)/3.7)**2),0]) for x in [-1.6,-1,-.4]])
    # Closed glass silhouette; the narrow rim follows the cell surface.
    glass=Polygon([-1.2,3.65,0],[.3,3.65,0],[-.05,2.285,0],[-.85,2.373,0],
                  color=TEXT,stroke_width=4,fill_color=TEXT,fill_opacity=.08)
    opening=Ellipse(width=.805,height=.12,color=TEXT,stroke_width=3).rotate(-.11).move_to([-.45,2.329,0])
    pip=VGroup(glass,opening)
    return VGroup(cell,channels,pip,txt('HEK293t cell',-1,-.6,34),txt('mouse Piezo1',-4.2,3.05,29,BLUE),
                  Line([-3.0,2.85,0],[-1.6,2.32,0],color=BLUE),txt('Lewis and Grandl',3.6,-2.8,28))

def question():
    return VGroup(txt('Find the effective area',y=3,size=40,color=PURPLE),
        formula('k = k_B T_abs / ΔA',y=1.6,size=46),formula('k = 0.8 mN/m  (fit values)',y=.1,size=32,color=YELLOW),
        formula('k_B T_abs = 4.1 × 10⁻²¹ J',y=-1.2,size=34),formula('ΔA = ?',y=-2.6,size=50,color=PURPLE))

def area_frame():
    a=VGroup(txt('Effective two-state area',y=3.1,size=36,color=PURPLE),
        formula('ΔA = k_B T_abs / k',y=2.15,size=40),
        formula('= (4.1 × 10⁻²¹ J)/(0.8 × 10⁻³ N/m)  (fit values)',y=1.1,size=27),
        formula('= 5.1 × 10⁻¹⁸ m² ≈ 5 nm²',y=.1,size=36,color=GREEN),
        formula('J ÷ (N/m) = m²',x=-3,y=-.85,size=28))
    # Areas, rather than side lengths, differ by sixty-fold. Geometric comparison only.
    big=Square(side_length=2.2,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([2.6,-2,0])
    small=Square(side_length=2.2/np.sqrt(60),color=PURPLE,fill_color=PURPLE,fill_opacity=.8).move_to([-3.0,-2,0])
    a.add(VGroup(big,small,txt('5 nm²',-3,-3.45,32,PURPLE),
                 txt('≈ 300 nm², about 60 times larger',2.6,-3.45,26),
                 txt('Structural area comparison',2.6,-.65,24,GREY)))
    return a

def estimates():
    left=VGroup(txt('Mouse Piezo1',-3.1,2.25,32,BLUE),formula('≈ 5 nm²',-3.1,1.35,44,PURPLE),
                txt('Current–tension fit',-3.1,.4,30),
                txt('Lewis and Grandl',-3.1,-.65,26))
    right=VGroup(txt('Human PIEZO1',3.0,2.25,32,BLUE),formula('6 to 20 nm²',3.0,1.35,44,PURPLE),
                txt('Bacterial MscL channel',3.0,.4,32,YELLOW),txt('Calibrated in the same patch',3.0,-.15,26),
                txt('Bae and colleagues, 2013',3.0,-.65,26))
    # Equal spacing in log(area), showing an order of magnitude, not equality.
    def pos(v): return np.array([-4.8+9.6*np.log10(v)/np.log10(30),-2.05,0])
    line=VGroup(Line(pos(1),pos(30),color=GREY),*[VGroup(Line(pos(v)+DOWN*.1,pos(v)+UP*.1),
                     formula(str(v),size=26).move_to(pos(v)+DOWN*.4)) for v in [1,5,10,20,30]],
                Line(pos(6),pos(20),color=PURPLE,stroke_width=12),Dot(pos(5),color=PURPLE,radius=.12),
                txt('Effective area (nm²) · logarithmic scale',y=-3.2,size=26))
    return left,right,line

class S00Title(TitleCard):
    LESSON='Piezo Channels and the Physics of Force'
    TITLE='Reading a Patch'
    def construct(self):
        self.add(VGroup(txt('BIOCHEMISTRYPEDIA',size=26,color=TEAL),txt(self.LESSON,size=30),
                 txt(self.TITLE,size=60),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.5))
        self.wait(self.narration_s)

class S01Question(SpokenScene):
    def construct(self):
        ax,base=plot(y=.2,h=5)
        self.add(base)
        self.at('A patch recording'); self.play(Create(curve(ax)),run_time=1.2)
        self.at('Can you read'); self.play(FadeIn(txt('?',-.3,1,76,PURPLE)),run_time=.3)
        self.finish()

class S02Lewis(SpokenScene):
    def construct(self):
        g=cell_view(); g[2].shift(UP*.65)
        self.add(g)
        self.at('They recorded'); self.play(g[2].animate.shift(DOWN*.65),run_time=.7)
        self.finish()

class S03Cellattached(SpokenScene):
    def construct(self):
        g=cell_view(); self.add(g)
        self.at('the pipette seals')
        seal=VGroup(*[Dot(pt,radius=.075,color=GREEN) for pt in [[-.85,2.373,0],[-.05,2.285,0]]])
        self.play(Create(seal),run_time=.45)
        self.at('It records the channels')
        closeup=patch(False)
        zoom=closeup.copy().scale(.12).move_to(seal.get_center())
        self.add(zoom)
        self.play(Transform(zoom,closeup),FadeOut(g),FadeOut(seal),run_time=.65)
        self.play(FadeIn(txt('Cell-attached seal',3.25,1.6,32,GREEN)),
                  FadeIn(txt('Channels under\nthe pipette tip',3.25,-.2,30,BLUE)),run_time=.25)
        self.finish()

class S04Imaging(SpokenScene):
    def construct(self):
        p=patch(False); self.add(p,txt('Camera view',3.3,2.9,32))
        self.at('They pressurized'); self.play(Transform(p,patch()),FadeIn(pressure()),run_time=.85)
        self.at('and imaged it')
        # Camera inset contains a second view of the actual cap and its fitted circle.
        fitted=Circle(radius=RAD,color=BLUE,stroke_width=2).move_to(CENTER)
        camera=VGroup(patch()[2],fitted).scale(.65).move_to([3.3,.1,0])
        self.play(FadeIn(camera),Create(Rectangle(width=4.1,height=4.1,color=GREY).move_to([3.3,.1,0])),run_time=.5)
        self.at('So the patch radius'); self.play(Create(radius()),FadeIn(txt('Circle fitted to dome',3.3,-2.5,27,BLUE)),run_time=.5)
        self.finish()

class S05Laplace(SpokenScene):
    def construct(self):
        diagram=VGroup(patch(),pressure(),radius()).scale(1.08,about_point=[-2.6,0,0]).shift(DOWN*.35)
        self.add(diagram,txt('Young–Laplace relation',y=3.4,size=38),
                 txt('Spherical patch · uniform tension',y=-3.45,size=34))
        self.at('pressure becomes tension')
        self.play(FadeIn(formula('T = R × Δp / 2',3.15,1.5,44,YELLOW)),
                  FadeIn(txt('T = membrane tension',3.15,.5,31,YELLOW)),run_time=.5)
        self.at('pressure difference')
        label=txt('Δp = pressure difference',3.0,-.65,29,YELLOW)
        self.play(FadeIn(label),Create(Line(label.get_left()+LEFT*.12,diagram[1].get_center(),color=YELLOW)),run_time=.4)
        self.finish()

class S06Numbers(SpokenScene):
    def construct(self):
        self.add(patch(),pressure(),txt('Illustrative patch',y=3.4,size=36),txt('Invented round numbers',y=-3.3,size=32,color=YELLOW))
        self.at('a radius of'); self.play(FadeIn(radius('R = 2.0 µm')),run_time=.4)
        self.at('under'); self.play(FadeIn(formula('Δp = 2000 Pa',3.1,1.5,34,YELLOW)),
                  Create(Line([1.1,1.5,0],[-2.4,2.5,0],color=YELLOW)),run_time=.4)
        self.finish()

class S07Tension(SpokenScene):
    def construct(self):
        self.add(patch(),pressure(),radius('R = 2.0 µm'),txt('Invented round numbers',y=-3.3,size=30,color=YELLOW),
            formula('Δp = 2000 Pa',3.15,2.5,30,YELLOW),
            formula('T = (2.0 × 10⁻⁶ m)',3.15,1.3,29),formula('× (2000 N/m²) / 2',3.15,.65,29),
            formula('m × N/m² = N/m',3.15,-2.3,27))
        self.at('The tension comes'); self.play(FadeIn(formula('= 2.0 × 10⁻³ N/m',3.15,-.3,30)),run_time=.35)
        self.at('out at'); self.play(FadeIn(formula('= 2.0 mN/m',3.15,-1.3,38,GREEN)),run_time=.35)
        self.finish()

class S08Fit(SpokenScene):
    def construct(self):
        ax,base=plot(y=.0,h=4.7); self.add(base)
        self.at('Now the fit'); self.play(Create(curve(ax)),run_time=1.0)
        self.at('a half activation tension')
        mid=VGroup(DashedLine(ax.c2p(2.7,0),ax.c2p(2.7,.5),color=YELLOW),Dot(ax.c2p(2.7,.5),color=YELLOW))
        self.play(Create(mid),FadeIn(formula('T50 = 2.7 ± 0.1 mN/m',2.0,3.25,29,YELLOW)),run_time=.45)
        self.at('a slope factor')
        bracket=DoubleArrow(ax.c2p(1.9,.18),ax.c2p(3.5,.18),buff=0,color=YELLOW)
        self.play(Create(bracket),FadeIn(formula('2k',-2.55,-2.02,27,YELLOW)),
                  FadeIn(formula('k = 0.8 ± 0.1 mN/m',2.3,-1.75,28,YELLOW)),run_time=.45)
        self.finish()

class S09Current(SpokenScene):
    def construct(self):
        base,c,calc,p,r=current_frame(); self.add(base,c,calc)
        self.at('predicts about', lead=-.26); self.play(FadeIn(p),run_time=.4)
        self.at('of the plateau current'); self.play(FadeIn(r),run_time=.3)
        self.finish()
class S10Hold(Scene):
    def construct(self): self.add(*current_frame()); self.wait(3)
class S11Predict(SpokenScene):
    def construct(self):
        q=question(); self.add(q[0],q[2])
        self.at('You know how'); self.play(FadeIn(q[1]),FadeIn(q[3]),run_time=.5)
        self.at('Can you find'); self.play(FadeIn(q[4]),run_time=.3)
        self.finish()
class S12Pause(Scene):
    def construct(self):
        self.add(question(),txt('Pause and try it',4.2,-2.8,28,TEAL)); self.wait(5)
class S13Reveal(SpokenScene):
    def construct(self):
        a=area_frame(); self.add(a[0],a[1])
        self.at('run the fit backwards'); self.play(FadeIn(a[2]),FadeIn(a[4]),run_time=.5)
        self.at('The effective area'); self.play(FadeIn(a[3]),GrowFromCenter(a[5]),run_time=.7)
        self.finish()
class S14Hold(Scene):
    def construct(self): self.add(area_frame()); self.wait(3)

class S15Dg0(SpokenScene):
    def construct(self):
        self.add(formula('ΔG₀,eff = T50 × ΔA_eff',y=3.25,size=40),
            formula('(2.7 × 10⁻³ N/m)(5.1 × 10⁻¹⁸ m²)  (fit values)',y=2.4,size=27))
        r1=Rectangle(width=2.0,height=1.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([-3,-.2,0])
        r2=Rectangle(width=3.5,height=1.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([2.2,-.2,0])
        labels=VGroup(txt('ΔA',-3,-1.4,30,PURPLE),txt('Larger assigned ΔA',2.2,-1.4,28,PURPLE),
            txt('T50',-5,-.2,30,YELLOW),txt('Same fitted T50',y=-2.05,size=28,color=YELLOW))
        self.add(r1,labels[0],labels[2])
        self.at('about'); self.play(FadeIn(formula('≈ 1.4 × 10⁻²⁰ J ≈ 3.4 k_B T_abs',y=1.5,size=32,color=GREEN)),run_time=.4)
        self.at('It comes from both'); self.play(TransformFromCopy(r1,r2),FadeIn(labels[1]),FadeIn(labels[3]),
            FadeIn(txt('Energy scales with assigned area',y=-2.65,size=28)),run_time=.7)
        self.at('An underestimated area alone')
        caution=chip('No general bound on the molecular energy',RED,size=28).move_to([0,-3.5,0])
        self.play(FadeIn(caution),run_time=.4); self.finish()

class S16Bae(SpokenScene):
    def construct(self):
        a,b,line=estimates(); self.add(a,txt('Two routes to the same order',y=3.35,size=36))
        self.at('An independent route'); self.play(FadeIn(b),FadeIn(line),run_time=.7)
        self.finish()
class S17Assume(SpokenScene):
    def construct(self):
        a,b,line=estimates(); self.add(a,b,txt('Two routes to the same order',y=3.35,size=36))
        self.at('Both estimates assume')
        tag=chip('Assumes a two-state switch',RED,size=40).move_to([0,-2.2,0])
        links=VGroup(Line(a[1].get_bottom()+DOWN*.1,tag.get_top()+LEFT*2,color=RED),
                     Line(b[1].get_bottom()+DOWN*.1,tag.get_top()+RIGHT*2,color=RED))
        # Route around card captions so leaders visibly terminate at the actual values.
        links=VGroup(VMobject(color=RED).set_points_as_corners([a[1].get_left(),[-5.8,1.35,0],[-5.8,-1.4,0],tag.get_left()]),
                     VMobject(color=RED).set_points_as_corners([b[1].get_right(),[5.9,1.35,0],[5.9,-1.4,0],tag.get_right()]))
        self.play(Create(links),FadeIn(tag),run_time=.6)
        self.at('Hold on to'); self.play(Indicate(tag,scale_factor=1.03),run_time=.5); self.finish()
class S18Caution(SpokenScene):
    def construct(self):
        ax,base=plot(x=-3.1,y=.2,w=4.7,h=4.8,xmax=6,step=2)
        self.add(base,curve(ax),txt('1  What the number is',3.0,2.6,31,BLUE))
        self.at('This is a normalized current'); self.play(FadeIn(txt('Normalized current',3.0,1.7,30,BLUE)),run_time=.3)
        self.at('for mouse'); self.play(FadeIn(txt('Mouse Piezo1 · HEK293t',3.0,.8,28)),run_time=.3)
        self.at('at room temperature'); self.play(FadeIn(txt('Room temperature\nCell-attached',3.0,-.35,28)),run_time=.3)
        self.at('It is not a fraction'); self.play(FadeIn(txt('2  What it is not',3.0,-1.65,31,RED)),
                    FadeIn(txt('A fraction of neurons',3.0,-2.5,29,RED)),run_time=.4); self.finish()

class S19Prepulse(SpokenScene):
    def construct(self):
        ax,a=plot(x=-3.25,y=-.25,w=4.65,h=4.5,xmax=5,step=1)
        bx,b=plot(x=3.25,y=-.25,w=4.65,h=4.5,xmax=5,step=1)
        self.add(a,b,txt('Without prepulse',-3.25,3.4,32),txt('After prepulse',3.25,3.4,32),
            curve(ax,2.2,xmax=5),formula('T50 = 2.2',-2.0,-1.75,28,YELLOW),
            txt('Illustrative slopes; reported T50s',-3.25,2.8,26))
        self.at('a five')
        self.play(FadeIn(txt('5 s · +5 mmHg prepulse',3.25,2.7,27,YELLOW)),run_time=.35)
        ghost=curve(bx,2.2,color=GREY,xmax=5).set_stroke(opacity=.45)
        self.add(ghost,DashedLine(bx.c2p(2.2,0),bx.c2p(2.2,.5),color=GREY,stroke_opacity=.5),
                 Dot(bx.c2p(2.2,.5),color=GREY,radius=.06))
        self.at('lowered the'); self.play(TransformFromCopy(ghost,curve(bx,1.4,xmax=5)),run_time=.75)
        self.at('from')
        self.play(Create(DashedLine(ax.c2p(2.2,0),ax.c2p(2.2,.5),color=YELLOW)),run_time=.25)
        self.at('to')
        self.play(Create(DashedLine(bx.c2p(1.4,0),bx.c2p(1.4,.5),color=YELLOW)),
            FadeIn(formula('T50 = 1.4',4.1,-1.75,28,YELLOW)),run_time=.3); self.finish()

class S20Why(SpokenScene):
    def construct(self):
        blocks=VGroup(*[RoundedRectangle(width=1,height=1.4,corner_radius=.12,color=GREY if i<2 else BLUE,
                fill_color=GREY if i<2 else BLUE,fill_opacity=.5).move_to([x,0,0]) for i,x in enumerate([-3.6,-1.2,1.2,3.6])])
        mem=Line([-5.5,0,0],[5.5,0,0],color=GREY,stroke_width=7)
        inactive=VGroup(*[txt('Inactivated',x,-1.2,27) for x in [-3.6,-1.2]])
        arrows=VGroup(Arrow([-3,1.5,0],[-5.5,1.5,0],color=YELLOW,buff=0),Arrow([3,1.5,0],[5.5,1.5,0],color=YELLOW,buff=0))
        self.add(mem,blocks,inactive,arrows,txt('Authors’ interpretation',y=3.2,size=40,color=TEAL),txt('Resting tension',y=2.1,size=30,color=YELLOW))
        self.at('Relieves Resting Tension')
        shorter=VGroup(Arrow([-3,1.5,0],[-3.8,1.5,0],color=YELLOW,buff=0),Arrow([3,1.5,0],[3.8,1.5,0],color=YELLOW,buff=0))
        self.play(Transform(arrows,shorter),FadeIn(txt('Prepulse → less resting tension',y=-2.3,size=32,color=YELLOW)),run_time=.7)
        self.at('channels it had inactivated recover')
        self.play(*[b.animate.set_color(BLUE).set_fill(BLUE,opacity=.5) for b in blocks[:2]],FadeOut(inactive,shift=DOWN*.15),
            FadeIn(txt('All 4 active · 2 recovered',y=-1.2,size=34,color=GREEN)),run_time=.75)
        self.at('so less added tension'); self.play(FadeIn(txt('Less added tension needed',y=-3.2,size=30,color=GREEN)),run_time=.35); self.finish()

class S21Mix(SpokenScene):
    def construct(self):
        fitbox=RoundedRectangle(width=6.0,height=4.9,color=BLUE).move_to([-3.1,-.1,0])
        finding=txt('Sensitivity depends on prior tension',y=3.2,size=40,color=YELLOW)
        self.add(finding,fitbox,txt('Current–tension fit',-3.1,1.65,34,BLUE),
            formula('T50 = 2.7',-3.1,.65,40,YELLOW),formula('k = 0.8 mN/m',-3.1,-.25,36,YELLOW),
            txt('Prepulse protocol',3.3,1.65,34),formula('2.2 →',2.8,.5,40,YELLOW),
            txt('Different protocols',y=-3.35,size=34,color=RED))
        # The value appears only once, then visibly leaves its own protocol.
        wrong=formula('1.4',4.35,.5,44,YELLOW)
        self.add(wrong,txt('mN/m',3.3,-.35,30,YELLOW))
        self.at('Do not mix')
        self.play(wrong.animate.move_to([-3.1,-1.6,0]),run_time=.65)
        self.play(Create(Cross(wrong,stroke_color=RED,stroke_width=7)),run_time=.25)
        self.at('The shift is the finding'); self.play(Indicate(finding,scale_factor=1.025),run_time=.45)
        self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        self.add(txt('Read as a two-state switch',y=3.0,size=40,color=RED),formula('ΔA = k_B T_abs / k',y=1.4,size=58,color=PURPLE),
            formula('0.8 mN/m  →  ≈ 5 nm²',y=-.4,size=58,color=GREEN),
            txt('The slope factor k itself is a tension',y=-2.6,size=33,color=YELLOW))
        self.at('The slope factor implies an area'); self.play(Indicate(self.mobjects[1],scale_factor=1.04),run_time=.6); self.finish()
class S23End(EndCard):
    LINE='Read as a two-state switch, the slope factor implies an area.'
    def construct(self):
        self.add(txt('Read as a two-state switch,',y=1.1,size=54),txt('the slope factor implies an area.',y=-.2,size=54),
            txt('biochemistrypedia.com',y=-1.7,size=28,color=TEAL))
        self.wait(self.narration_s)
