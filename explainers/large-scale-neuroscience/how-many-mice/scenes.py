"""Chapter 3: all data, simulation grids and curves come from the supplied model.
COLOR MAP: GREY structure/trials; BLUE neurons; TEAL signal/manipulation;
YELLOW units/rates; ORANGE mouse A; PINK mouse B; PURPLE sessions;
RED pooled count/false alarms; GREEN animal count; GOLD questions/rules.
"""
import numpy as np
from scipy.stats import t as student_t
from bp_style import *
PURPLE, ORANGE, PINK = '#B58CD9', '#F29E4C', '#E58FB5'
RATES = np.array([8, 2, 4, 8, 2, 2])
POOLED = RATES.mean()
SESSION_MEANS = [RATES[:2].mean(), RATES[2:4].mean(), 2., 2.]
MOUSE_MEANS = [np.mean(SESSION_MEANS[:2]), np.mean(SESSION_MEANS[2:])]
ANIMAL = np.mean(MOUSE_MEANS)


def mouse(color=GREEN, w=3.6):
    # Continuous silhouette; opaque fill masks all hidden strokes.
    body=VMobject(color=color,stroke_width=3,fill_color=BG,fill_opacity=1)
    body.set_points_smoothly([[-1.35,-.2,0],[-1.2,.65,0],[-.4,1.0,0],[.45,.85,0],[.65,1.12,0],[1.0,1.05,0],[1.05,.65,0],[1.55,.15,0],[1.25,-.45,0],[.4,-.85,0],[-.7,-.8,0],[-1.35,-.2,0]])
    tail=CubicBezier([-1.35,-.2,0],[-1.55,-.75,0],[-2.1,-1.1,0],[-2.05,-.55,0],color=color,stroke_width=3)
    eye=Dot([1.23,.22,0],radius=.04,color=color)
    return VGroup(tail,body,eye).scale(w/3.6)


def dots(n=100, cols=10, step=.25, radius=.06):
    rows=int(np.ceil(n/cols))
    return VGroup(*[Dot([(i%cols-(cols-1)/2)*step,((rows-1)/2-i//cols)*step,0],radius=radius,color=YELLOW) for i in range(n)])


def mice_stage():
    icons=VGroup(*[mouse(w=3.55).move_to([x,2.2,0]) for x in (-4.2,0,4.2)])
    ds=VGroup(*[dots(step=.36,radius=.07).move_to([x,-.85,0]) for x in (-4.2,0,4.2)])
    return icons,ds


def pile():
    cloud=dots(300,20,.32,.065).move_to([0,-.65,0])
    for i,d in enumerate(cloud):
        d.set_color(interpolate_color(ManimColor(YELLOW),ManimColor([ORANGE,PINK,YELLOW][i//100]),.55))
    return cloud


def question():
    return T('How often will a standard test\ncall the drug effect significant?',34,line_spacing=1.1).move_to([-.8,2.95,0])


def pool_label():
    return M('n = 300',40,RED).move_to([0,-3.45,0])


def dataset():
    headers=VGroup(); boxes=VGroup(); rates=VGroup(); tags=VGroup()
    for x,col,name,vals in [(-4.15,ORANGE,'A',[[8,2],[4,8]]),(4.15,PINK,'B',[[2],[2]])]:
        headers.add(VGroup(mouse(col,w=1.65).move_to([x-1.3,3.05,0]),T('mouse '+name,36,col).move_to([x+.85,3.05,0])))
        for k,(y,vs) in enumerate(zip([1.25,-1.0],vals)):
            box=VGroup(RoundedRectangle(width=4.0,height=2.0,corner_radius=.12,color=PURPLE),T('session '+str(k+1),30,PURPLE).move_to([0,.65,0])).move_to([x,y,0])
            r=VGroup(*[VGroup(Dot(radius=.1,color=YELLOW),M(str(v),48,YELLOW)).arrange(RIGHT,buff=.18) for v in vs]).arrange(RIGHT,buff=.7).move_to([x,y-.25,0])
            boxes.add(box); rates.add(r)
        tags.add(T(str(sum(map(len,vals)))+' units',28,col).move_to([x,-2.55,0]))
    footer=VGroup(T('Invented dataset • rates in spikes per second',26,GREY),T('Each unit: mean of 4 stimulus presentations',26,GREY)).arrange(DOWN,buff=.16).move_to([0,-3.35,0])
    return headers,boxes,rates,tags,footer


def mean_bar(value,x,color,name):
    h=value*.95
    bar=Rectangle(width=2.1,height=h,color=color,fill_opacity=.5).move_to([x,-1.55+h/2,0])
    val=M(f'{value:.2f}',40,color).next_to(bar,UP,buff=.15)
    lab=T(name,28,color).move_to([x,-2.05,0])
    return VGroup(bar,val,lab)


def comparison():
    bars=VGroup(mean_bar(POOLED,-2.8,RED,'pooled mean'),mean_bar(ANIMAL,2.8,GREEN,'animal mean'))
    baseline=Line([-5.8,-1.55,0],[5.8,-1.55,0],color=GREY)
    mouse_means=VGroup(M('A 5.5',38,ORANGE).move_to([-2.8,-2.7,0]),M('B 2',38,PINK).move_to([2.8,-2.7,0]))
    return VGroup(baseline,bars,T('Mean rate • spikes per second',30,GREY).move_to([0,3.55,0]),M('(5.5 + 2) / 2 = 3.75',30,GREEN).move_to([0,-3.4,0]),mouse_means)


def simulation_rates():
    rng=np.random.default_rng(20261102)
    av=rng.normal(size=(300000,3))+rng.normal(0,.2,size=(300000,3))
    grand=av.mean(1)
    ss=4*rng.chisquare(297,300000)+100*((av-grand[:,None])**2).sum(1)
    unit=np.mean(abs(grand)/np.sqrt(ss/299/300)>student_t.ppf(.975,299))
    animal=np.mean(abs(grand)/(av.std(1,ddof=1)/np.sqrt(3))>student_t.ppf(.975,2))
    return unit,animal

SIM_UNIT,SIM_MOUSE=simulation_rates()
N_UNIT,N_MOUSE=round(100*SIM_UNIT),round(100*SIM_MOUSE)


def grid(x=0):
    return VGroup(*[Square(.49,color=GREY,stroke_width=1,fill_color=GREY,fill_opacity=.25).move_to([x+(i%10-4.5)*.55,2.5-(i//10)*.55,0]) for i in range(100)])


def painted(g,n):
    for s in g[:n]: s.set_fill(RED,1).set_stroke(RED)
    return g


def grid_head(x,label):
    return T(label,34,RED if label.startswith('units') else GREEN).move_to([x,3.25,0])


def percent(x,n,col):
    return M(f'{n}%',44,col).move_to([x,-3.2,0])


def sim_notes():
    return VGroup(T('Illustrative normal-shift model',28,GREY),T('3 mice × 100 units',28,GREY),T('Mouse SD 1 • unit SD 2',28,GREY),T('Two-sided t-test at 5%',28,GREY),T('300,000 experiments',28,GREY),T('Each square = 1 percentage point',26,GREY)).arrange(DOWN,buff=.35).move_to([3.4,0,0])


def error_plot(m=3):
    # x=log10(units); SE=sqrt(mouse variance/m + unit variance/(m*u)).
    axes=Axes(x_range=[0,2,1],y_range=[0,1.5,.5],x_length=9.7,y_length=5.45,tips=False,axis_config={'color':GREY,'include_numbers':False}).move_to([.65,.12,0])
    labels=VGroup(T('Units per mouse • log spacing',28).move_to([.65,-3.3,0]),T('standard error of the drug effect',28).rotate(PI/2).move_to([-5.45,.12,0]))
    for x,lab in [(0,'1'),(1,'10'),(2,'100')]: labels.add(M(lab,26,GREY).next_to(axes.c2p(x,0),DOWN,buff=.13))
    for y in [0,.5,1.,1.5]: labels.add(M(f'{y:.1f}' if y else '0',26,GREY).next_to(axes.c2p(0,y),LEFT,buff=.15))
    curve=axes.plot(lambda z:np.sqrt(1/m+4/(m*10**z)),x_range=[0,2,.01],color=YELLOW,stroke_width=6,use_smoothing=False)
    return axes,labels,curve


def lesson_points(ax,m=3):
    g=VGroup()
    for u in [1,10,100]:
        se=np.sqrt(1/m+4/(m*u)); pos=ax.c2p(np.log10(u),se)
        # All labels are above the trace; endpoint labels turn inward.
        offset={1:np.array([.5,.4,0]),10:np.array([0,.48,0]),100:np.array([-.55,.5,0])}[u]
        g.add(Dot(pos,radius=.085,color=YELLOW),M(f'{se:.2f}',28,YELLOW).move_to(pos+offset))
    return g


def floor_line(ax,m=3):
    return DashedLine(ax.c2p(0,1/np.sqrt(m)),ax.c2p(2,1/np.sqrt(m)),dash_length=.2,dashed_ratio=.65,color=GREEN,stroke_width=6)


def floor_label(ax,m=3):
    return T(('floor '+format(1/np.sqrt(m),'.3f' if m==12 else '.2f')),28,GREEN).move_to(ax.c2p(1.45,1/np.sqrt(m))+DOWN*.42)


class S00Title(TitleCard):
    LESSON='Recording Many Neurons: Imaging, Arrays and Atlases'
    TITLE='How Many Mice?'
    def construct(self):
        self.add(T('Recording Many Neurons:\nImaging, Arrays and Atlases',28,GREY).move_to([0,1.65,0]))
        self.play(FadeIn(T(self.TITLE,58,font=TITLE_FONT)),Create(Line([-1.5,-.7,0],[1.5,-.7,0],color=GOLD)),run_time=.65)
        self.finish()


class S01N(SpokenScene):
    def construct(self):
        cloud=pile().move_to(ORIGIN); icons,ds=mice_stage()
        self.at('300 units'); self.add(cloud)
        self.at('recorded from'); self.play(Transform(cloud,VGroup(*[d for cluster in ds for d in cluster])),FadeIn(icons),run_time=.9)
        self.at('How many samples'); self.play(FadeIn(T('How many samples is that?',36).move_to([0,-3.15,0])),run_time=.4)
        self.finish()


class S02N(SpokenScene):
    def construct(self):
        icon=mouse(w=8.4).move_to([0,-.1,0]); d=dots(step=.19,radius=.05).move_to([-.15,-.1,0])
        self.at('Units recorded'); self.add(icon,d)
        genes=chip('genes',GREEN,30).move_to([-4,2.9,0]); dose=chip('drug dose',GREEN,30).move_to([3.7,2.9,0])
        halo=Ellipse(width=9.5,height=5.3,color=GREEN,stroke_opacity=.6).move_to(icon)
        self.at('its genes'); self.play(FadeIn(genes),Create(halo),Create(Line(genes.get_bottom(),halo.point_at_angle(2.1),color=GREEN)),run_time=.4)
        self.at('drug dose'); self.play(FadeIn(dose),Create(Line(dose.get_bottom(),halo.point_at_angle(1.0),color=GREEN)),run_time=.4)
        self.finish()


class S03N(SpokenScene):
    def construct(self):
        icon=mouse(w=8.4).move_to([0,-.1,0]); d=dots(step=.19,radius=.05).move_to([-.15,-.25,0]); self.add(icon,d)
        box=RoundedRectangle(width=2.6,height=2.8,color=PURPLE).move_to([-.15,-.1,0])
        self.at('one session'); self.play(Create(box),run_time=.4)
        tag=T('alertness that day',28,PURPLE).move_to([-3.65,2.85,0])
        self.at("day's alertness"); self.play(FadeIn(tag),Create(Line(tag.get_bottom(),box.get_top()+LEFT*.7,color=PURPLE)),run_time=.4)
        track=Line([.32,-1.3,0],[.32,1,0],color=PURPLE,stroke_width=5); lab=T('probe track',28,PURPLE).move_to([3.7,2.85,0])
        self.at('probe track'); self.play(Create(track),FadeIn(lab),Create(Line(lab.get_bottom(),track.get_top(),color=PURPLE)),run_time=.4)
        self.at('If that mouse'); self.play(FadeIn(T('Illustrative model: a shared shift',28,GREY).move_to([0,-3.1,0])),run_time=.3)
        self.at('shift together'); ghost=d.copy().set_opacity(.2); self.add(ghost)
        self.play(d.animate.shift(UP*.55),GrowArrow(Arrow([-1.8,-.25,0],[-1.8,.65,0],buff=0,color=YELLOW)),run_time=.8)
        self.finish()


class S04N(SpokenScene):
    def construct(self):
        headers,boxes,rates,tags,foot=dataset()
        self.at('Take a small'); self.add(headers,foot)
        self.at('two mice'); self.play(Create(boxes),run_time=.55)
        self.at('mouse A'); self.play(FadeIn(rates[:2]),FadeIn(tags[0]),run_time=.45)
        self.at('and mouse'); self.play(FadeIn(rates[2:]),FadeIn(tags[1]),run_time=.45)
        self.finish()


class S05N(SpokenScene):
    def construct(self):
        headers,boxes,rates,tags,foot=dataset(); self.add(headers,boxes,rates,tags)
        bar=Rectangle(width=1.5,height=4.75,color=RED,fill_opacity=.35).move_to([-1.3,-.125,0])
        base=Line([-2.1,-2.5,0],[1.5,-2.5,0],color=GREY)
        label=M('4.33',40,RED).next_to(bar,UP,buff=.2)
        self.at('Pool every unit'); self.add(base)
        targets=VGroup(*[Dot([-1.3+((i%2)-.5)*.52,-1.8+(i//2)*1.35,0],radius=.16,color=ORANGE if i<4 else PINK) for i in range(6)])
        copies=VGroup(*[r[0].copy() for group in rates for r in group]); self.add(copies)
        self.play(Transform(copies,targets),GrowFromEdge(bar,DOWN),FadeIn(label),run_time=1.1)
        self.play(FadeIn(T('pooled mean • A 4 : B 2',28,RED).move_to([0,-2.95,0])),FadeIn(M('26 / 6 = 4.33',30,RED).move_to([0,-3.5,0])),run_time=.3)
        self.at('twice as much'); self.play(Indicate(tags[0],color=ORANGE),Indicate(copies[:4],color=ORANGE),run_time=.7)
        self.finish()


class S06N(SpokenScene):
    def construct(self):
        headers,boxes,rates,tags,foot=dataset(); self.add(headers,boxes,rates,tags)
        heading=T('Rates • spikes per second',26,GREY).move_to([0,3.65,0]); self.add(heading)
        means=VGroup(*[M(f'{v:g}',48,PURPLE).move_to(r) for v,r in zip(SESSION_MEANS,rates)])
        self.at('average within')
        # Move each observed unit to a shared session centre before showing its mean.
        self.play(*[unit.animate.move_to(group.get_center()) for group in rates for unit in group],run_time=.65)
        self.play(*[ReplacementTransform(r,m) for r,m in zip(rates,means)],run_time=.4)
        self.at('each animal')
        am=M('5.5',48,ORANGE).move_to([-4.15,.3,0]); bm=M('2',48,PINK).move_to([4.15,.3,0])
        self.play(FadeOut(boxes),FadeOut(tags),ReplacementTransform(means[:2],am),ReplacementTransform(means[2:],bm),run_time=.65)
        arithmetic=VGroup(M('(5 + 6) / 2 = 5.5',28,ORANGE),M('(2 + 2) / 2 = 2',28,PINK),M('(5.5 + 2) / 2 = 3.75',30,GREEN)).arrange(DOWN,buff=.35).move_to([0,-1.6,0])
        self.play(FadeIn(arithmetic),run_time=.35)
        self.at('The animal mean')
        self.play(*[FadeOut(o) for o in list(self.mobjects) if o is not heading],run_time=.25)
        comp=comparison()
        self.play(ReplacementTransform(heading,comp[2]),FadeIn(comp[:2]),FadeIn(comp[3:]),run_time=.5)
        self.finish()


class S06bHold(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(comparison()); self.wait(2)


class S07N(SpokenScene):
    def construct(self):
        self.at('For a claim')
        self.add(T('A claim about mice',38).move_to([0,2.9,0]),M('n = 2 mice',68,GREEN).move_to([0,1.35,0]))
        old=M('6 units × 4 presentations = 24',32,RED).move_to([0,-1.1,0])
        self.add(old,VGroup(mouse(ORANGE,w=2.5),mouse(PINK,w=2.5)).arrange(RIGHT,buff=1.3).move_to([0,-2.9,0]))
        self.at('the sample is'); self.play(Indicate(self.mobjects[1],color=GREEN),run_time=.5)
        self.at('not 24'); self.play(ReplacementTransform(old,T('24 unit-trials ≠ 2 independent mice',32,RED).move_to(old)),run_time=.5)
        self.finish(); self.wait(2)


class S08N(SpokenScene):
    def construct(self):
        icons,_=mice_stage(); self.at('Now a harder'); self.add(icons,T('Invented variances',28,GREY).move_to([0,3.4,0]))
        columns=VGroup()
        # Paired columns have identical means, making the null visible.
        vals=np.array([-.9,-.55,-.2,.2,.55,.9])
        for x,spread in zip((-4.2,0,4.2),(.75,1.,1.3)):
            for dx,lab in [(-.7,'before'),(.7,'after')]:
                col=VGroup(*[Dot([x+dx,-.65+v*spread,0],radius=.105,color=YELLOW) for v in vals])
                columns.add(col,T(lab,26).move_to([x+dx,-2.25,0]))
            columns.add(Line([x-1.25,-.65,0],[x+1.25,-.65,0],color=GREEN,stroke_width=3),T('mean',24,GREEN).move_to([x+1.55,-.25,0]),T('same mean, effect = 0',24,GREEN).move_to([x,-2.85,0]))
        self.play(FadeIn(columns),run_time=.65)
        self.at('does nothing'); self.play(FadeIn(T('True drug effect: zero',38,GREEN).move_to([0,-3.5,0])),run_time=.5)
        self.finish()


class S09N(SpokenScene):
    def construct(self):
        icons,clusters=mice_stage(); self.add(icons)
        for cluster,col in zip(clusters,[ORANGE,PINK,YELLOW]): cluster.set_color(col)
        ds=VGroup(*[d for cluster in clusters for d in cluster])
        self.at('Record'); self.play(FadeIn(ds),run_time=.6)
        label=T('100 units per mouse',30,YELLOW).move_to([0,-3,0])
        self.at('from each'); self.play(FadeIn(label),run_time=.35)
        self.at('Treat all'); target=pile()
        for i,d in enumerate(target): d.set_color([ORANGE,PINK,YELLOW][i//100])
        self.play(ReplacementTransform(ds,target),FadeOut(icons),FadeOut(label),run_time=2)
        self.play(FadeIn(pool_label()),Transform(target,pile()),run_time=.4)
        self.finish()


class S10N(SpokenScene):
    def construct(self):
        self.add(pile(),pool_label()); self.at('How often'); self.add(question()); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(pile(),pool_label(),question())
        ring=Circle(radius=.74,color=GOLD,stroke_width=6).move_to([3.8,2.85,0]); self.add(ring)
        self.play(Uncreate(ring),rate_func=linear,run_time=5)


class S12N(SpokenScene):
    def construct(self):
        g=grid(-3); self.at('in a simulation'); self.add(g,grid_head(-3,'units as n'),sim_notes())
        self.at('about'); self.play(*[s.animate.set_fill(RED,1).set_stroke(RED) for s in g[:N_UNIT]],FadeIn(percent(-3,N_UNIT,RED)),run_time=.7)
        self.finish()


class S13N(SpokenScene):
    def construct(self):
        g=painted(grid(-3),N_UNIT); h=grid(3)
        self.add(g,grid_head(-3,'units as n'),percent(-3,N_UNIT,RED))
        self.at('The same test'); self.add(h,grid_head(3,'mice as n'))
        self.at('about five'); self.play(*[s.animate.set_fill(RED,1).set_stroke(RED) for s in h[:N_MOUSE]],FadeIn(percent(3,N_MOUSE,GREEN)),run_time=.6)
        self.finish(); self.wait(1)


class S14N(SpokenScene):
    def construct(self):
        g=painted(grid(-3),N_UNIT); h=painted(grid(3),N_MOUSE)
        right_percent=percent(3,N_MOUSE,GREEN)
        self.add(g,h,grid_head(-3,'units as n'),grid_head(3,'mice as n'),percent(-3,N_UNIT,RED),right_percent)
        self.play(h.animate.scale(.9).shift(UP*.2),right_percent.animate.move_to([3,-2.65,0]),run_time=.3)
        self.at('That is'); self.play(Create(SurroundingRectangle(h,buff=.1,color=GREEN)),run_time=.5)
        note=T('nominal 5% rate,\ntest assumptions met',28,GREEN).move_to([3,-3.4,0])
        self.at('false alarm rate'); self.play(FadeIn(note),Create(Line([5.2,-3.0,0],[5.2,h.get_bottom()[1]-.1,0],color=GREEN)),run_time=.3)
        self.at('when its assumptions'); self.play(Indicate(note,color=GREEN,scale_factor=1.03),run_time=.3)
        self.finish()


class S15N(SpokenScene):
    def construct(self):
        naive=np.sqrt((4+2/3)/300); correct=np.sqrt(1/3+4/300)
        axes=Axes(x_range=[-.8,.8,.4],y_range=[0,1,1],x_length=8.8,y_length=4.9,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to([.7,.2,0])
        baseline=Line(axes.c2p(-.8,0),axes.c2p(.8,0),color=GREY)
        zero=DashedLine(axes.c2p(0,0),axes.c2p(0,1),color=GREY)
        bars=VGroup()
        for y,se,col,label in [(.78,naive,RED,'units as n'),(.31,correct,GREEN,'mice as n')]:
            left=axes.c2p(-se,y); right=axes.c2p(se,y)
            bar=VGroup(Line(left,right,color=col,stroke_width=7),*[Line(p+DOWN*.2,p+UP*.2,color=col,stroke_width=4) for p in [left,right]],Dot(axes.c2p(0,y),color=col))
            bars.add(VGroup(bar,T(label,28,col).move_to([-4.8,left[1],0]),M(f'SE {se:.3f}',28,col).move_to([2.7,left[1]+.6,0])))
        labs=VGroup(T('Standard error',36).move_to([0,3.25,0]),T('Estimated drug effect (true value 0)',28).move_to([.7,-2.95,0]))
        for v in [-.8,-.4,0,.4,.8]: labs.add(M(f'{v:g}',26,GREY).next_to(axes.c2p(v,0),DOWN,buff=.13))
        self.at('Counting units'); self.add(baseline,zero,bars,labs)
        self.at('far too narrow'); self.play(Indicate(bars[0],color=RED),run_time=.6)
        self.at('This is called'); self.play(FadeIn(T('pseudoreplication',34,RED).move_to([0,-3.55,0])),run_time=.5)
        self.finish()


class S16N(SpokenScene):
    def construct(self):
        ax,labels,curve=error_plot(); self.at('Are more units'); self.add(ax,labels,T('3 mice, fixed spread',28,GREY).move_to([2.7,3.35,0]))
        self.play(Create(curve),run_time=2.8)
        self.at('they average out'); self.play(FadeIn(lesson_points(ax)),run_time=.7)
        self.finish()


class S17N(SpokenScene):
    def construct(self):
        ax,labels,curve=error_plot(); self.add(ax,labels,curve,lesson_points(ax),T('3 mice, fixed spread',28,GREY).move_to([2.7,3.35,0]))
        self.at('But no number'); self.play(Indicate(curve,color=YELLOW,scale_factor=1.01),run_time=.8)
        self.at('The error stops'); self.play(Create(floor_line(ax)),FadeIn(floor_label(ax)),run_time=.8)
        self.finish()


class S18N(SpokenScene):
    def construct(self):
        ax,labels,curve=error_plot(); line=floor_line(ax); lab=floor_label(ax)
        # Spaced count dots avoid silhouettes colliding with the plot labels.
        self.add(ax,labels,curve,line,lab)
        icons=VGroup(*[Dot([-.9+i*.43,3.35,0],radius=.12,color=GREEN) for i in range(12)])
        count=T('3 mice',28,GREEN).move_to([5.65,3.35,0]); self.add(icons[:3],count)
        fixed=T('mouse spread held fixed',28,GREEN).move_to(ax.c2p(.45,1/np.sqrt(3))+DOWN*.4); self.at('With the spread'); self.add(fixed)
        formula=T('floor = mouse SD /\n√(number of mice)',26,GREEN).move_to([-1.8,-2.05,0]); self.add(formula)
        self.at('only more mice'); arrow=Arrow(ax.c2p(1.9,1/np.sqrt(3)),ax.c2p(1.9,1/np.sqrt(12)),buff=0,color=GREEN)
        self.play(FadeIn(icons[3:],shift=LEFT*.4),Transform(count,T('12 mice',28,GREEN).move_to(count)),Transform(curve,error_plot(12)[2]),Transform(line,floor_line(ax,12)),Transform(lab,floor_label(ax,12)),fixed.animate.move_to([1,-.7,0]),GrowArrow(arrow),run_time=2.4)
        self.play(FadeIn(M('0.289',28,GREEN).next_to(arrow,RIGHT,buff=.18)),run_time=.25)
        self.finish(); self.wait(1)


class S19N(SpokenScene):
    def construct(self):
        outer=RoundedRectangle(width=12.2,height=6.15,corner_radius=.2,color=GREEN).move_to([0,.35,0])
        title=T('Animal',30,GREEN).move_to([-4.9,3.03,0]); sess=VGroup(); grids=VGroup()
        for x in [-3,3]:
            sess.add(VGroup(RoundedRectangle(width=5.45,height=4.9,corner_radius=.15,color=PURPLE).move_to([x,0,0]),T('Session',28,PURPLE).move_to([x,2.05,0])))
            lines=VGroup(*[Line([x-1.65,-1.8+i*.85,0],[x+1.65,-1.8+i*.85,0],color=GREY) for i in range(4)],*[Line([x-1.65+j*1.1,-1.8,0],[x-1.65+j*1.1,.75,0],color=GREY) for j in range(4)])
            obs=VGroup(*[Dot([x-1.1+j*1.1,-1.375+i*.85,0],radius=.12,color=YELLOW) for i in range(3) for j in range(3)])
            grids.add(VGroup(lines,obs,T('units',26,YELLOW).rotate(PI/2).move_to([x-2.15,-.55,0]),T('stimulus presentations\n(trials)',26,GREY,line_spacing=.9).move_to([x,1.35,0])))
        self.at('So report every level'); self.add(outer,title)
        self.play(FadeIn(sess),run_time=.4); self.play(FadeIn(grids),run_time=.5)
        self.at('say which level'); self.play(FadeIn(T('animals > sessions > units × trials',30,GOLD).move_to([0,-3.15,0])),run_time=.45)
        self.finish()


class S20N(SpokenScene):
    def construct(self):
        # Same five methods/steps and gold rounded box as chapter 1's table/rule.
        box=RoundedRectangle(width=12.2,height=6.7,corner_radius=.2,color=GOLD)
        specs=[('Probe','sites → channels → units → neurons',YELLOW),('Calcium imaging','light → calcium → spikes',GREEN),('Any recording','units → animals',GREEN),('Atlas','cluster → cell type',PURPLE),('Connectome','count → strength',PINK)]
        rows=VGroup()
        for i,(method,step,col) in enumerate(specs):
            y=2.15-i*.91
            row=VGroup(T(method,26,col).move_to([-4.1,y,0]),T(step,26).move_to([1.9,y,0]),Line([-5.7,y-.4,0],[5.7,y-.4,0],color=GREY,stroke_opacity=.4))
            if i!=2: row.set_opacity(.4)
            rows.add(row)
        self.at('Each of these'); self.add(box,rows,T('Each number is a step from your claim',30,GOLD).move_to([0,2.95,0]))
        self.at('Count your sample'); self.play(Create(RoundedRectangle(width=11.6,height=.8,corner_radius=.1,color=GREEN).move_to([0,2.15-2*.91,0])),FadeIn(T('Count your sample at the level of the claim.',30,GREEN).move_to([0,-2.85,0])),run_time=.6)
        self.finish()


class S21N(SpokenScene):
    def construct(self):
        q=T('Needed for behaviour?',44,GOLD).move_to([0,2.85,0])
        pathway=chip('pathway',TEAL,48).scale(1.15).move_to([-3.6,.35,0]); behaviour=chip('behaviour',GREEN,48).scale(1.15).move_to([3.6,.35,0])
        arrow=Arrow(pathway.get_right(),behaviour.get_left(),buff=.1,color=GREY,stroke_width=5)
        mark=T('?',54,GOLD).move_to([0,1.35,0])
        self.at('And none of this'); self.add(q,pathway,behaviour,arrow,mark)
        self.at('That takes'); manip=chip('manipulation',TEAL,44).move_to([0,-1.8,0])
        self.play(FadeIn(manip),GrowArrow(Arrow(manip.get_top(),[0,.65,0],buff=.1,color=TEAL,stroke_width=7)),pathway.animate.set_opacity(.3),run_time=.8)
        self.play(FadeIn(T('Test whether behaviour changes',32,GOLD).move_to([1,-2.9,0])),run_time=.4)
        self.finish()


class S22End(EndCard):
    LINE='Count your sample at the level of the claim.'
    def construct(self):
        line=fit(T(self.LINE,40,font=TITLE_FONT),11.5)
        sub=T('biochemistrypedia.com',26,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.4)
        self.play(FadeIn(line),run_time=self.beat(.3))
        self.play(FadeIn(sub),run_time=self.beat(.15))
        self.finish()
