"""Biodiversity and ecosystem function, timed to the supplied Kokoro narration.

COLOR MAP (retained from the original film)
  BLUE = species A; ORANGE = species B
  GREY = benchmarks, axes, generic species and experimental structure
  GOLD = net effect and biomass totals
  GREEN = complementarity and gains
  RED = selection
  TEXT = best-monoculture benchmark and plain labels
All plots are schematic, without numerical yield measurements.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BASE = -2.8          # y of the axis baseline
K = 0.011            # units per g/m2 : 400 -> 4.4
UNIT = "grams dry biomass per m²"
XA, XB, XM, BW = -3.8, -1.4, 1.5, 1.5


def hbar(x, v, color, k=K, w=BW, op=0.45):
    r = Rectangle(width=w, height=v * k, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op)
    return r.move_to([x, BASE + v * k / 2, 0])


def side_label(word, val, y, color, x=5.2, vs=30):
    return VGroup(T(word, 26, color), M(val, vs, color)).arrange(DOWN, buff=0.08).move_to([x, y, 0])


def vlabel(text, mob, color=TEXT, size=28):
    return M(text, size, color).next_to(mob, UP, buff=0.12)


def axis(x0=-4.9, x1=2.5):
    return Line([x0, BASE, 0], [x1, BASE, 0], color=GREY, stroke_width=3)


def dashed(y, x0=-4.9, x1=2.5, color=GREY):
    return DashedLine([x0, y, 0], [x1, y, 0], color=color, stroke_width=3, dash_length=0.15)


def yy(v, k=K):
    return BASE + v * k


def chart(full=True):
    """Bars A alone 400, B alone 100, mixture (A 300 + B 100). Returns a dict of the pieces."""
    d = {}
    d["axis"] = axis()
    d["barA"] = hbar(XA, 400, BLUE)
    d["barB"] = hbar(XB, 100, ORANGE)
    d["valA"] = vlabel("400", d["barA"])
    d["valB"] = vlabel("100", d["barB"])
    d["nameA"] = T("A alone", 26, BLUE).move_to([XA, BASE - 0.4, 0])
    d["nameB"] = T("B alone", 26, ORANGE).move_to([XB, BASE - 0.4, 0])
    mA = hbar(XM, 300, BLUE)
    mB = hbar(XM, 100, ORANGE)
    mB.move_to([XM, yy(300) + 100 * K / 2, 0])
    d["mixA"], d["mixB"] = mA, mB
    d["mix"] = VGroup(mA, mB)
    d["tA"] = M("A 300", 22, TEXT).move_to(mA)
    d["tB"] = M("B 100", 22, TEXT).move_to(mB)
    d["valM"] = vlabel("400", mB)
    d["nameM"] = T("A + B together", 26, TEXT).move_to([XM, BASE - 0.4, 0])
    d["unit"] = T(UNIT, 22, GREY).to_corner(UL, buff=0.5).shift(DOWN * 0.55)
    return d


def add_all(scene, d, keys):
    scene.add(*[d[k] for k in keys])


STATIC = ["axis", "barA", "barB", "valA", "valB", "nameA", "nameB", "mixA", "mixB", "tA", "tB", "valM", "nameM", "unit"]


RK = 4.4  # units per 1.0 relative yield
RX = [-3.3, 0.6]
RW = 2.2


def rbar(x, v, color):
    r = Rectangle(width=RW, height=v * RK, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
    return r.move_to([x, BASE + v * RK / 2, 0])


def backed(g):
    back = Rectangle(width=g.width + 0.12, height=g.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(g)
    out = VGroup(back, g)
    out.set_z_index(5)
    return out


def ry(v):
    return BASE + v * RK


# New schematic helpers extend the original rectangles, dashed benchmarks and chips.
def heading(text):
    return T(text, 34).move_to([0, 3.05, 0])


def tuft(color, height=1.0):
    return VGroup(*[Line([0, 0, 0], [dx, height * h, 0], color=color, stroke_width=4)
                    for dx, h in [(-0.2, 0.7), (0, 1), (0.2, 0.85)]])


def grassplot(x, rich=True, y=-0.8):
    ground = Line([x-1.7, y, 0], [x+1.7, y, 0], color=GREY, stroke_width=3)
    colors = [BLUE, ORANGE, GREY, BLUE, ORANGE] if rich else [BLUE]*5
    plants = VGroup(*[tuft(c, h).shift([x-1.3+i*0.65, y, 0])
                       for i, (c,h) in enumerate(zip(colors, [1.1, 1.5, 1.25, 1.7, 1.3] if rich else [0.85]*5))])
    return VGroup(ground, plants)


def schematic_bar(x, height, color=GOLD, y=-1.9, width=1.4):
    # Reuse the original baseline-aligned bar helper, with schematic heights.
    return hbar(x, height, color, k=1, w=width).shift(UP*(y-BASE))


def trace(values, x0, x1, base, color, scale=1):
    points = [[x, base+scale*v, 0] for x,v in zip(np.linspace(x0,x1,len(values)), values)]
    return VMobject().set_points_as_corners(points).set_stroke(color, 4)


def timeseries(rich, center):
    t = np.linspace(0, 6, 90)
    vals = 0.14*np.sin(2.3*t)+0.11*np.sin(4.1*t+0.4) if rich else 0.5*np.sin(2.3*t)+0.3*np.sin(4.1*t+0.4)
    return VGroup(Line([-5.3,center-0.85,0],[4.2,center-0.85,0],color=GREY),
                  trace(vals,-5.3,4.2,center,GOLD),
                  T('richer community' if rich else 'species-poor community',26).move_to([-2.8,center+1.1,0]))


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.45)


class S00Title(TitleCard):
    LESSON = 'Biodiversity and ecosystem function'
    TITLE = 'More Species, More Biomass'

    def construct(self):
        title = T(self.TITLE, 48, font=TITLE_FONT).move_to([0,1,0])
        sub = T(self.LESSON, 26, GREY).move_to([0,2.1,0])
        plots = VGroup(grassplot(-3,False),grassplot(3,True)).shift(DOWN*0.7)
        rule = Line(LEFT*1.2,RIGHT*1.2,color=GOLD).move_to([0,0.2,0])
        self.play(FadeIn(title), FadeIn(sub), Create(rule), FadeIn(plots),run_time=0.9)
        self.finish()


class S01Mixture(SpokenScene):
    def construct(self):
        head=heading('Experimental grasslands')
        poor,rich=grassplot(-3,False),grassplot(3,True)
        names=VGroup(T('fewer species',28).move_to([-3,-1.5,0]),T('more species',28).move_to([3,-1.5,0]))
        self.at('Grassland experiments')
        self.play(FadeIn(head),FadeIn(poor),FadeIn(rich),FadeIn(names),run_time=0.7)
        self.at('generally grow more')
        bars=VGroup(schematic_bar(-3,1.25),schematic_bar(3,2.3))
        self.play(ReplacementTransform(poor,bars[0]),ReplacementTransform(rich,bars[1]),
                  Transform(head,heading('Harvested aboveground biomass')),names.animate.shift(DOWN*0.85),run_time=1)
        pattern=T('More plant species → generally more biomass',30,GOLD).move_to([0,-2.9,0])
        self.play(FadeIn(pattern),run_time=0.6)
        self.at('Losing species')
        self.play(Indicate(names[0],color=GREY),Indicate(bars[0],color=GOLD),run_time=0.8)
        self.at('Richer communities')
        clear(self)
        top,bottom=timeseries(False,1.4),timeseries(True,-1.2)
        self.play(FadeIn(top),FadeIn(bottom),FadeIn(T('Across years →',24,GREY).move_to([4.6,-3,0])),run_time=0.8)
        self.at('At Cedar Creek')
        site=T('Cedar Creek · Minnesota',28).move_to([0,3.1,0])
        self.play(FadeIn(site),run_time=0.5)
        self.at('individual species became')
        t=np.linspace(0,6,90)
        species=VGroup(trace(0.5*np.sin(2.7*t),-5.3,4.2,-1.2,BLUE),
                       trace(0.4*np.sin(4.4*t+0.8),-5.3,4.2,-1.2,ORANGE))
        self.play(bottom[1].animate.set_stroke(width=7),Create(species),run_time=0.8)
        self.at('the whole community')
        self.play(FadeOut(species),Indicate(bottom[1],color=GOLD),run_time=0.8)
        self.finish()


class S03Two(SpokenScene):
    def construct(self):
        self.at('Why can a mixture')
        question=heading('Why can a mixture produce more?')
        self.play(FadeIn(question),run_time=0.5)
        ct=chip('complementarity',GREEN,30).move_to([-3.2,2.1,0])
        st=chip('selection',RED,30).move_to([3.2,2.1,0])
        # Original two-panel drawing: yield bars above dashed expectations.
        bars=VGroup(schematic_bar(-4.2,1.8,BLUE,y=-0.9,width=1),schematic_bar(-2.2,1.8,ORANGE,y=-0.9,width=1))
        expected=VGroup(dashed(0,-4.9,-3.5),dashed(0,-2.9,-1.5))
        cap=T('monoculture prediction',22,GREY).move_to([-3.2,-1.4,0])
        self.at('Complementarity means')
        self.play(FadeIn(ct),FadeIn(bars),Create(expected),FadeIn(cap),run_time=0.7)
        self.at('do better together')
        ups=VGroup(*[Arrow([x,0,0],[x,0.9,0],buff=0,color=GREEN) for x in [-4.9,-1.5]])
        self.play(GrowArrow(ups[0]),GrowArrow(ups[1]),run_time=0.6)
        self.at('use resources differently')
        resources=VGroup(chip('resource use A',BLUE,22).move_to([-4.4,-2.2,0]),
                         chip('resource use B',ORANGE,22).move_to([-1.8,-2.2,0]))
        resource_arrows=VGroup(*[Arrow([x,-1.85,0],[x,-1.02,0],buff=0.05,color=c) for x,c in [(-4.2,BLUE),(-2.2,ORANGE)]])
        self.play(FadeOut(cap),FadeIn(resources),Create(resource_arrows),run_time=0.7)
        self.at('Legumes adding nitrogen')
        leg=chip('legumes → nitrogen → neighbors',GREEN,22).move_to([-3.2,-2.2,0])
        self.play(ReplacementTransform(resources,leg),FadeOut(resource_arrows),run_time=0.7)
        self.at('Selection is another')
        dots=VGroup(*[Circle(radius=0.3,stroke_color=RED if i==2 else GREY,
                       fill_color=RED if i==2 else GREY,fill_opacity=0.5).move_to([1.4+i*1.15,0,0]) for i in range(4)])
        rc=T('random draw',26,GREY).move_to([3.2,1.1,0])
        self.play(FadeIn(st),FadeIn(rc),FadeIn(dots),run_time=0.6)
        self.at('productive species that dominates')
        dom=VGroup(T('productive species',24,RED),T('dominates',24,RED)).arrange(DOWN,buff=0.1).move_to([3.2,-1.8,0])
        self.play(dots[2].animate.scale(2),*[dots[i].animate.scale(0.6) for i in (0,1,3)],FadeIn(dom),run_time=0.9)
        self.at('Both can act together')
        eq=VGroup(M('net effect =',28,GOLD),T('complementarity',28,GREEN),M('+',28),T('selection',28,RED)).arrange(RIGHT,buff=0.2).move_to([0,-3.1,0])
        self.play(FadeOut(ups),FadeIn(eq),run_time=0.6)
        self.at('partition separates')
        clear(self)
        self.play(FadeIn(heading('Loreau–Hector partition')),FadeIn(eq.copy().move_to([0,1.2,0])),run_time=0.7)
        acct=chip('yield accounting',GOLD,32).move_to([0,-0.1,0])
        self.play(FadeIn(acct),run_time=0.5)
        self.at('does not identify')
        mech=T('Biological mechanism needs more evidence',30).move_to([0,-1.8,0])
        self.play(FadeIn(mech),run_time=0.7)
        self.finish()


class S04Stability(SpokenScene):
    def construct(self):
        self.at('Now ask what steadier')
        self.play(FadeIn(heading('Temporal stability')),run_time=0.5)
        formula=VGroup(T('mean total biomass',30,GOLD),Line(LEFT*2.1,RIGHT*2.1,color=TEXT),
                       T('standard deviation',30,GREY)).arrange(DOWN,buff=0.2).move_to([3.6,0.5,0])
        t=np.linspace(0,8,100)
        # Deterministic independent random sequences, without paired opposing waves.
        rng=np.random.default_rng(17)
        a=rng.uniform(-0.55,0.55,15); b=rng.uniform(-0.55,0.55,15)
        # Both species and their sum use the same vertical scale.
        av=0.65+0.65*a; bv=0.65+0.65*b
        total=trace(av+bv,-5.6,0.3,-1.6,GOLD)
        ax=Line([-5.6,-1.8,0],[0.3,-1.8,0],color=GREY)
        label=T('Total = A + B · years →',23).move_to([-2.7,-2.25,0])
        self.at('Temporal stability is')
        self.play(FadeIn(formula),Create(ax),Create(total),FadeIn(label),run_time=0.8)
        self.at('species fluctuate independently')
        species=VGroup(trace(av,-5.6,0.3,-1.6,BLUE),trace(bv,-5.6,0.3,-1.6,ORANGE))
        self.play(Create(species),run_time=0.8)
        self.at('partly cancel in the total')
        self.play(Indicate(total,color=GOLD),run_time=0.7)
        self.at('A higher mean production')
        self.play(total.animate.shift(UP*0.45),species.animate.shift(UP*0.225),Indicate(formula[0],color=GOLD),run_time=0.8)
        self.at('Resistance means')
        clear(self)
        self.play(FadeIn(heading('Disturbance and recovery are separate')),run_time=0.5)
        baseline=dashed(1.1,-5.8,5.8)
        event=Rectangle(width=1.5,height=2.9,stroke_width=0,fill_color=GREY,fill_opacity=0.15).move_to([-0.3,-0.3,0])
        el=T('disturbance',24,GREY).move_to([-0.3,1.8,0])
        path=trace([0,0,-1.7],-5.5,0.2,1.1,GOLD)
        r=chip('resistance: change during',GOLD,24).move_to([-3,-2.5,0])
        self.play(Create(baseline),FadeIn(event),FadeIn(el),Create(path),FadeIn(r),run_time=0.8)
        self.at('Resilience means')
        recovery=trace([-1.7,-0.8,0],0.2,5.5,1.1,GOLD)
        rl=chip('resilience: return afterwards',GOLD,24).move_to([3,-2.5,0])
        self.play(Create(recovery),FadeIn(rl),run_time=0.8)
        self.at('greater resistance')
        note=T('Grassland synthesis:\ngreater resistance',24).move_to([-3,-3.36,0])
        self.play(FadeIn(note),Indicate(r,color=GOLD),run_time=0.7)
        self.at('no detectable diversity effect')
        result=VGroup(T('Recovery one year later:',23),T('no detectable diversity effect',23,GREY)).arrange(DOWN,buff=0.12).move_to([3,-3.36,0])
        self.play(FadeIn(result),run_time=0.8)
        self.finish()


class S05Experiments(SpokenScene):
    def construct(self):
        self.at('How do we know')
        head=heading('Assign richness; draw species at random')
        self.play(FadeIn(head),run_time=0.5)
        pool=VGroup(*[Dot([x,1.3,0],radius=0.18,color=c) for x,c in zip([-1.2,-0.4,0.4,1.2],[BLUE,ORANGE,GREY,BLUE])])
        poor,rich=grassplot(-3,False,y=-1.3),grassplot(3,True,y=-1.3)
        self.at('randomly chosen species')
        self.play(FadeIn(pool),FadeIn(poor),FadeIn(rich),run_time=0.5)
        seeds=VGroup(pool[0].copy(),pool[1:3].copy())
        self.add(seeds)
        self.play(seeds[0].animate.move_to([-3,-0.4,0]),seeds[1].animate.move_to([3,-0.4,0]),run_time=0.6)
        self.play(FadeOut(seeds),run_time=0.2)
        self.at('same seed mass')
        mass=T('Equal total seed mass in every plot',30).move_to([0,-2.4,0])
        self.play(FadeIn(mass),run_time=0.5)
        self.at('They clipped')
        clear(self)
        h=heading('Measure aboveground biomass each year')
        plant=grassplot(-4.3,True,y=-1)
        cut=Line([-5.9,-0.7,0],[-2.7,-0.7,0],color=TEXT,stroke_width=5)
        dry=chip('dry',GOLD,30).move_to([0,0,0])
        weigh=chip('weigh',GOLD,30).move_to([4.2,0,0])
        self.play(FadeIn(h),FadeIn(plant),Create(cut),run_time=0.3)
        self.at('dried')
        self.play(ReplacementTransform(plant[1],dry),FadeOut(cut),run_time=0.35)
        self.at('weighed the plants')
        self.play(TransformFromCopy(dry,weigh),run_time=0.4)
        self.at('Random composition prevents')
        clear(self)
        rand=chip('random composition',GREY,32).move_to([0,1,0])
        msg=VGroup(T('Researchers do not hand-pick',30),T('productive species for richer plots',30)).arrange(DOWN,buff=0.2).move_to([0,-0.7,0])
        self.play(FadeIn(rand),FadeIn(msg),run_time=0.7)
        self.at('repeated the logic')
        clear(self)
        cedar=chip('Cedar Creek',GREY,28).move_to([-4,0,0])
        mn=T('Minnesota',24,GREY).move_to([-4,-0.9,0])
        sites=VGroup(*[Dot([2.5+(i%4)*0.8,0.5-(i//4),0],radius=0.13,color=GREY) for i in range(8)])
        eu=T('8 European BIODEPTH sites',27).move_to([2.8,1.6,0])
        link=Arrow([-2.5,0,0],[1.6,0,0],color=GREY,buff=0.1)
        self.play(FadeIn(cedar),FadeIn(mn),GrowArrow(link),FadeIn(sites),FadeIn(eu),run_time=0.8)
        self.at('Across those sites')
        result=VGroup(T('Species loss → lower average biomass',30,GOLD),T('Overall pattern across sites',24,GREY)).arrange(DOWN,buff=0.2).move_to([0,-2.3,0])
        self.play(FadeIn(result),run_time=0.7)
        self.finish()


class S06Field(SpokenScene):
    def construct(self):
        self.at('Real landscapes')
        self.play(FadeIn(heading('Field associations need caution')),run_time=0.5)
        soil=chip('soil moisture / fertility',GREY,30).move_to([0,1.8,0])
        richness=chip('more species',TEXT,30).move_to([-3,-0.5,0])
        biomass=chip('more biomass',GOLD,30).move_to([3,-0.5,0])
        arrows=VGroup(Arrow([-0.8,1.35,0],[-2.7,0.05,0],color=GREY,buff=0.1),
                      Arrow([0.8,1.35,0],[2.7,0.05,0],color=GREY,buff=0.1))
        self.at('Wetter or more fertile soil')
        self.play(FadeIn(soil),FadeIn(richness),FadeIn(biomass),Create(arrows),run_time=0.9)
        assoc=DashedLine([-1.4,-0.5,0],[1.4,-0.5,0],color=GOLD)
        cap=T('positive association',25,GOLD).move_to([0,-1.5,0])
        self.at('Field studies found positive')
        self.play(Create(assoc),FadeIn(cap),run_time=0.6)
        self.at('adjusting for environmental differences')
        adjusted=T('Adjusted for measured environment',26,GREY).move_to([0,2,0])
        self.play(ReplacementTransform(soil,adjusted),arrows.animate.set_opacity(0.3),run_time=0.7)
        self.at('an unmeasured variable')
        unknown=chip('unmeasured variable?',GREY,30).move_to([0,1.9,0])
        self.play(ReplacementTransform(adjusted,unknown),arrows.animate.set_opacity(1),run_time=0.7)
        self.at('Experiments assign richness')
        exp=T('Experiments: assigned richness',27).move_to([0,-2.35,0])
        self.play(FadeIn(exp),run_time=0.6)
        self.at('Surveys need that extra caution')
        caution=T('Surveys: association, with residual uncertainty',26,GREY).move_to([0,-3.1,0])
        self.play(FadeIn(caution),run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        self.at('One smaller point')
        self.play(FadeIn(heading('Smaller point: the benchmark')),run_time=0.5)
        # Original A-alone, B-alone, stacked-mixture drawing, stripped of numerical yields.
        d=chart()
        self.play(Create(d['axis']),FadeIn(d['barA']),FadeIn(d['barB']),
                  FadeIn(d['nameA']),FadeIn(d['nameB']),run_time=0.6)
        self.at('A mixture can beat')
        self.play(GrowFromEdge(d['mixA'],DOWN),GrowFromEdge(d['mixB'],DOWN),FadeIn(d['nameM']),run_time=0.7)
        self.at('the average monoculture')
        average=dashed(yy(250))
        avg=T('average',28,GREY).move_to([4.5,yy(250),0])
        self.play(Create(average),FadeIn(avg),run_time=0.6)
        self.at('without beating the best')
        best=dashed(yy(400),color=TEXT)
        lab=T('best',28,TEXT).move_to([4.5,yy(400),0])
        self.play(Create(best),FadeIn(lab),run_time=0.6)
        self.at('Extra yield against the average')
        note=T('Above the average ≠ above the best',30,GOLD).move_to([0,2.35,0])
        self.play(FadeIn(note),run_time=0.6)
        self.finish()


class S07End(EndCard):
    TITLE = 'More Species, More Biomass'
    LINE = 'More plant species generally mean more biomass and steadier production.'

    def construct(self):
        title=T(self.TITLE,40,font=TITLE_FONT).move_to([0,2.9,0])
        line=T(self.LINE.replace('mean ', 'mean\n'),32,font=TITLE_FONT).move_to([0,1.5,0])
        field=grassplot(-2.5,True,y=-1.2)
        biomass=schematic_bar(3,2.2,y=-1.2)
        label=T('biomass',26,GOLD).move_to([3,-1.8,0])
        self.play(FadeIn(title),FadeIn(line),FadeIn(field),GrowFromEdge(biomass,DOWN),FadeIn(label),run_time=0.8)
        self.finish()
