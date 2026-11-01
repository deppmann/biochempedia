"""Climate and biomes: temperature, water and seasonality  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = sunlight / solar energy (the Sun, rays, spots, energy gradient)
  TEAL   = the planet (Earth, its orbit)
  BLUE   = water: moist air, rain, the precipitation line
  ORANGE = dry: dry air, desert, dry-season marks
  RED    = heat: the temperature line, fire
  GREEN  = vegetation: trees, forest, predictions, the Af class chip
  GREY   = ground, axes, structure, de-emphasized
  TEXT   = air flow arrows, general labels
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
MONTHS = "JFMAMJJASOND"
RAIN = [140, 120, 150, 180, 200, 160, 140, 110, 90, 100, 130, 160]   # the lesson's made-up station, mm
TEMP = 26                                                            # degrees C every month


def arr(a, b, color=TEXT, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bt(text, size=24, color=TEXT, **kw):
    return T(text, size, color, **kw)


def mt(text, size=26, color=TEXT, **kw):
    return M(text, size, color, **kw)


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def sun_glyph(pos, r=0.34):
    core = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    return core.move_to(pos)


def earth_glyph(pos, r=0.62, tilt=23.4, color=TEAL):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to(pos)
    th = np.radians(tilt)
    up = np.array([np.sin(th), np.cos(th), 0.0])
    axis = Line(pos - up * (r + 0.42), pos + up * (r + 0.42), color=TEXT, stroke_width=4)
    npole = Dot(pos + up * (r + 0.42), radius=0.09, color=TEXT)
    g = VGroup(body, axis, npole)
    g.body, g.axis, g.npole, g.up = body, axis, npole, up
    return g


def tree(x, y, r=0.24, trunk=0.3):
    t = Line([x, y, 0], [x, y + trunk, 0], color=GREY, stroke_width=4)
    c = Circle(radius=r, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.85).move_to([x, y + trunk + r * 0.8, 0])
    return VGroup(t, c)


def flame(x, y, s=1.0):
    pts = [[0, 0.5, 0], [0.22, 0.12, 0], [0.12, -0.3, 0], [-0.12, -0.3, 0], [-0.22, 0.12, 0]]
    f = Polygon(*pts, stroke_width=0, fill_color=RED, fill_opacity=0.95).scale(s * 0.9)
    return f.move_to([x, y, 0])


# Composite schematic helpers retain the original tree, flame, beam and chart style.
def heading(text):
    return bt(text, 32, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])


def landscape(x, y, forest=True):
    base = Line([x-2.25,y,0], [x+2.25,y,0], color=GREY, stroke_width=4)
    if forest:
        plants = VGroup(*[tree(x+dx,y,0.4,0.65) for dx in (-1.65,-0.8,0,0.85,1.65)])
    else:
        plants = VGroup(Arc(radius=1.3, start_angle=0.2, angle=2.7, color=ORANGE).stretch(0.3,1).move_to([x,y+0.15,0]))
    return VGroup(base, plants)


def rain(x, y, n=5, width=3.5):
    return VGroup(*[Line([x+dx,y,0],[x+dx-0.12,y-0.38,0],color=BLUE,stroke_width=4)
                    for dx in np.linspace(-width/2,width/2,n)])


def monthly(x, y, wet=True):
    # Qualitative strips: deliberately no invented numerical climate data.
    months = VGroup(*[bt(m,22,GREY).move_to([x+(i-5.5)*0.38,y-0.75,0]) for i,m in enumerate(MONTHS)])
    hot = VGroup(*[Line([x+(i-5.5)*0.38,y+0.5,0],[x+(i-5.5)*0.38,y+0.85,0],color=RED,stroke_width=8) for i in range(12)])
    water = VGroup(*[Line([x+(i-5.5)*0.38,y-0.4,0],[x+(i-5.5)*0.38,y+(0.25 if wet else -0.27),0],color=BLUE,stroke_width=8) for i in range(12)])
    return VGroup(months, hot, water)


def prediction():
    a=chip('Climate',TEAL,28).move_to([-4.7,0.3,0])
    b=chip('Vegetation\nprediction',GREEN,28).move_to([0,0.3,0])
    c=chip('Observed\nvegetation',GREEN,28).move_to([4.7,0.3,0])
    ar=arr(a.get_right()+RIGHT*.15,b.get_left()-RIGHT*.15,GREY)
    check=bt('compare',24,GREY).move_to([2.6,1.3,0])
    link=DoubleArrow(b.get_right()+RIGHT*.15,c.get_left()-RIGHT*.15,buff=0,color=GREY,tip_length=.15)
    return VGroup(a,b,c,ar,check,link)


class S00Title(TitleCard):
    LESSON = 'Climate, biomes and environmental variation'
    TITLE = 'Temperature, Water and Biomes'

    def construct(self):
        title=heading(self.TITLE)
        forest=landscape(-3.2,-1.9)
        desert=landscape(3.2,-1.9,False)
        symbols=VGroup(bt('warmth + year-round rain',24,BLUE).move_to([-3.2,.4,0]),
                       bt('scarce rain',24,ORANGE).move_to([3.2,.4,0]),
                       rain(-3.2,-.1),sun_glyph([3.2,-.3,0]))
        self.play(FadeIn(title),FadeIn(forest),FadeIn(desert),FadeIn(symbols),run_time=.8)
        self.finish()


class S01Patterns(SpokenScene):
    def construct(self):
        h=heading('Temperature + water + seasonality')
        strips=VGroup(monthly(-3.2,1),monthly(3.2,1,False))
        key=bt('red: temperature     blue: rainfall     J–D: months',22,GREY).move_to([0,-.25,0])
        self.at('Temperature and water')
        self.play(FadeIn(h),FadeIn(strips),FadeIn(key),run_time=.8)
        definition=bt('Biome: similar climate, dominant vegetation and animals',24).move_to([0,-3.3,0])
        self.at('A biome is')
        self.play(FadeIn(definition),run_time=.6)
        forest=landscape(-3.2,-2.1)
        fl=bt('tropical wet forest',26,GREEN).move_to([-3.2,-2.6,0])
        self.at('Tropical wet forest')
        self.play(FadeIn(forest,shift=UP*.15),FadeIn(fl),run_time=.7)
        desert=landscape(3.2,-2.1,False)
        dl=bt('desert',26,ORANGE).move_to([3.2,-2.6,0])
        self.at('Desert fits')
        self.play(FadeIn(desert),FadeIn(dl),run_time=.6)
        self.at('So climate gives')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        p=prediction()
        self.play(FadeIn(p[0]),GrowArrow(p[3]),FadeIn(p[1]),run_time=.8)
        self.at('We can compare')
        self.play(FadeIn(p[2]),FadeIn(p[4]),GrowArrow(p[5]),run_time=.8)
        self.at('But climate does')
        warning=heading('A prediction to check')
        self.play(FadeIn(warning),run_time=.5)
        self.at('Fire and soils')
        mods=VGroup(flame(-1.8,-1.8),bt('fire',26,RED).move_to([-.8,-1.8,0]),
                    chip('soils',GREY,26).move_to([1.7,-1.8,0]))
        self.play(FadeIn(mods),run_time=.6)
        self.finish()


class S06Biome(SpokenScene):
    def construct(self):
        h=heading('Same rain, different soils')
        def soil(x, stored, nutrients):
            box=Rectangle(width=4.5,height=1.4,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([x,-.6,0])
            water=Rectangle(width=4.35,height=stored,color=BLUE,stroke_width=0,fill_opacity=.4).align_to(box,DOWN).move_to([x,box.get_bottom()[1]+stored/2,0])
            dots=VGroup(*[Dot([x+dx,-.25,0],radius=.07,color=GREY) for dx in np.linspace(-1.7,1.7,nutrients)])
            return VGroup(box,water,dots)
        soils=VGroup(soil(-3.1,.85,7),soil(3.1,.25,3))
        rains=VGroup(rain(-3.1,1.8),rain(3.1,1.8))
        labels=VGroup(bt('water storage + nutrients differ',26).move_to([0,-2.2,0]))
        self.at('Under the same rain')
        self.play(FadeIn(h),FadeIn(soils),FadeIn(rains),run_time=.7)
        self.at('water holding capacity')
        self.play(FadeIn(labels),soils[0][1].animate.set_opacity(.8),run_time=.7)
        self.at('different vegetation')
        plants=VGroup(tree(-3.1,.1,.45,.55),tree(3.1,.1,.25,.3))
        self.play(FadeIn(plants,shift=UP*.1),run_time=.6)
        self.at('Staver and colleagues')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        tag=heading('Observed tropical tree cover')
        region=bt('Africa • Australia • South America',24,GREY).move_to([0,2.4,0])
        forests=landscape(-3.2,-1.4)
        savanna=VGroup(Line([1,-1.4,0],[5.4,-1.4,0],color=GREY),tree(2,-1.4,.35,.55),tree(4.4,-1.4,.3,.5))
        names=VGroup(bt('forest',28,GREEN).move_to([-3.2,-2,0]),bt('savanna',28,GREEN).move_to([3.2,-2,0]))
        self.play(FadeIn(tag),FadeIn(region),FadeIn(forests),FadeIn(savanna),FadeIn(names),run_time=.5)
        context=bt('Wide rainfall range • short dry season',26,BLUE).move_to([0,1.7,0])
        self.at('Across a wide rainfall')
        self.play(FadeIn(context),run_time=.5)
        self.at('places were mostly')
        self.play(Indicate(forests,color=GREEN),Indicate(savanna,color=GREEN),run_time=.7)
        self.at('Fire was associated')
        fire=VGroup(flame(3.2,-.7),bt('fire associated with open vegetation',24,RED).move_to([0,-2.9,0]))
        self.play(FadeIn(fire),run_time=.6)
        self.at('also need not mean')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        h=heading('Climate can change before vegetation')
        clim=chip('Climate',TEAL,30).move_to([-3,1,0])
        veg=landscape(3,-1.4)
        self.play(FadeIn(h),FadeIn(clim),FadeIn(veg),run_time=.6)
        self.play(clim.animate.set_color(RED).shift(UP*.4),run_time=.6)
        self.at('That depends on')
        conditions=VGroup(*[chip(t,c,25) for t,c in [('dispersal',GREEN),('soils',GREY),('fire',RED),('time',TEXT)]]).arrange(RIGHT,buff=.4).move_to([0,-2.6,0])
        self.play(FadeIn(conditions),run_time=.6)
        self.finish()


class S04Cell(SpokenScene):
    def construct(self):
        h=heading('Where does climate come from?')
        self.at('Where does that')
        self.play(FadeIn(h),run_time=.5)
        # Reuse the old equal-width sunlight geometry, without the solar arithmetic.
        gy=-1.5; w=1.2; th=np.radians(60)
        d=np.array([np.sin(th),-np.cos(th),0]); p=np.array([np.cos(th),np.sin(th),0])
        mid=np.array([4.,gy,0]); c=mid-d*4
        t1,t2=c+p*w/2,c-p*w/2
        e1=t1+d*((t1[1]-gy)/(-d[1])); e2=t2+d*((t2[1]-gy)/(-d[1]))
        beams=VGroup(Polygon([-4.3,1.6,0],[-3.1,1.6,0],[-3.1,gy,0],[-4.3,gy,0],stroke_width=0,fill_color=YELLOW,fill_opacity=.3),
                     Polygon(t1,t2,e2,e1,stroke_width=0,fill_color=YELLOW,fill_opacity=.3))
        ground=VGroup(Line([-5.7,gy,0],[-1.5,gy,0],color=GREY),Line([1.8,gy,0],[6,gy,0],color=GREY))
        spots=VGroup(Line([-4.3,gy,0],[-3.1,gy,0],color=YELLOW,stroke_width=12),Line(e1,e2,color=YELLOW,stroke_width=12))
        labs=VGroup(bt('equal-width sunlight beams',26,YELLOW).move_to([0,2.2,0]),bt('concentrated',26).move_to([-3.7,-2.3,0]),bt('spread over more ground',26).move_to([3.5,-2.3,0]))
        self.at('Sunlight striking Earth')
        self.play(FadeIn(beams),Create(ground),Create(spots),FadeIn(labs),run_time=.8)
        self.at('Over the year')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        h=heading('Uneven energy input')
        gradient=VGroup(*[Rectangle(width=.4,height=1.2,stroke_width=0,fill_color=YELLOW,fill_opacity=.95-.75*i/23).move_to([-4.6+i*.4,.7,0]) for i in range(24)])
        labs=VGroup(bt('tropics: more',28,YELLOW).move_to([-4,1.9,0]),bt('poles: less',28,YELLOW).move_to([4,1.9,0]))
        self.play(FadeIn(h),FadeIn(gradient),FadeIn(labs),run_time=.6)
        self.at('The atmosphere and oceans')
        transport=VGroup(arr([-4,-.6,0],[4,-.6,0],RED),arr([-4,-2,0],[4,-2,0],RED),bt('atmosphere: heat poleward',24).move_to([0,-1.1,0]),bt('oceans: heat poleward',24).move_to([0,-2.5,0]))
        self.play(FadeIn(transport),run_time=.6)
        self.at('Near the equator')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        h=heading('Equator → subtropics')
        base=Line([-5.5,-2,0],[5.5,-2,0],color=GREY,stroke_width=4)
        labs=VGroup(bt('equator',26,BLUE).move_to([-3,-2.5,0]),bt('subtropics',26,ORANGE).move_to([3,-2.5,0]))
        rise=arr([-3,-1.7,0],[-3,1.9,0],BLUE)
        rl=bt('rises • cools',26,BLUE).move_to([-4.8,.3,0])
        self.play(FadeIn(h),Create(base),FadeIn(labs),run_time=.4)
        self.at('warm moist air rises')
        self.play(GrowArrow(rise),FadeIn(rl),run_time=.5)
        self.at('and drops rain')
        drops=rain(-3,1.5,5,1.6)
        self.play(FadeIn(drops,shift=DOWN*.2),run_time=.5)
        self.at('Dry air flows')
        aloft=arr([-2.8,2,0],[3,2,0],ORANGE)
        self.play(GrowArrow(aloft),run_time=.6)
        self.at('sinks in the subtropics')
        sink=arr([3,1.8,0],[3,-1.7,0],ORANGE)
        sl=bt('sinks',26,ORANGE).move_to([4.6,.3,0])
        self.play(GrowArrow(sink),FadeIn(sl),run_time=.5)
        self.at('It warms as')
        warm=bt('warms • rain suppressed',24,ORANGE).move_to([2.8,-3.2,0])
        self.play(FadeIn(warm),run_time=.5)
        self.at('This is the idealized')
        back=arr([2.8,-1.65,0],[-2.8,-1.65,0],TEXT)
        self.play(GrowArrow(back),Transform(h,heading('Idealized Hadley cell')),run_time=.6)
        self.at('It helps explain')
        desert=Arc(radius=1.2,start_angle=.15,angle=2.84,color=ORANGE).stretch(.25,1).move_to([3,-1.87,0])
        self.play(Indicate(drops,color=BLUE),Create(desert),
                  Transform(labs[0],bt('wet equator',26,BLUE).move_to([-3,-2.5,0])),
                  Transform(labs[1],bt('subtropical desert',26,ORANGE).move_to([3,-2.5,0])),run_time=.6)
        self.at('Mountains add')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        mountain=Polygon([-5,-2,0],[0,1.6,0],[5,-2,0],color=GREY,fill_color=GREY,fill_opacity=.18)
        wind=VGroup(arr([-5,0,0],[-.7,2.1,0],BLUE),arr([.7,2.1,0],[5,0,0],ORANGE))
        labels=VGroup(heading('Mountains reshape rainfall'),bt('wet windward slope',26,BLUE).move_to([-3.4,-2.8,0]),bt('dry rain shadow',26,ORANGE).move_to([3.4,-2.8,0]))
        self.play(FadeIn(mountain),FadeIn(wind),FadeIn(rain(-2.5,.6,5,1.5)),FadeIn(labels),run_time=.7)
        self.finish()


def plot_glyph(sheltered=True):
    ground=Rectangle(width=1.15,height=.28,color=GREY,fill_color=GREEN,fill_opacity=.3)
    grass=VGroup(*[Line([x,0,0],[x+.05,.3,0],color=GREEN,stroke_width=3) for x in (-.4,-.2,0,.2,.4)])
    g=VGroup(ground,grass)
    if sheltered:
        g.add(VGroup(Line([-.65,.6,0],[.65,.6,0],color=GREY,stroke_width=4),Line([-.6,.6,0],[-.6,0,0],color=GREY),Line([.6,.6,0],[.6,0,0],color=GREY)))
    return g


class S08RainTiming(SpokenScene):
    def construct(self):
        h=heading('Same total rain, different timing')
        self.at('Annual rainfall totals')
        self.play(FadeIn(h),run_time=.5)
        columns=[]
        for x,shelter,label in [(-4.3,False,'Natural rain'),(0,True,'Sheltered\nnatural pattern'),(4.3,True,'Sheltered\nfewer, larger')]:
            plots=VGroup(*[plot_glyph(shelter).move_to([x+dx,y,0]) for dx,y in [(-.8,.6),(.8,.6),(-.8,-.5),(.8,-.5)]])
            lab=bt(label,25).move_to([x,2,0])
            columns.append(VGroup(plots,lab))
        self.at('used shelters')
        self.play(FadeIn(columns[1]),FadeIn(columns[2]),run_time=.6)
        design=bt('Replicated plots • randomly assigned treatments',24,GREY).move_to([0,-2.2,0])
        self.play(FadeIn(design),run_time=.5)
        self.at('They kept the total constant')
        def events(x,large):
            n=3 if large else 9
            return VGroup(*[Rectangle(width=.22,height=.9 if large else .3,stroke_width=0,fill_color=BLUE,fill_opacity=.8).move_to([x+(i-(n-1)/2)*(.8 if large else .28),-1.4,0]) for i in range(n)])
        ev=VGroup(events(0,False),events(4.3,True))
        self.play(FadeIn(ev),run_time=.6)
        equal=bt('equal water totals',25,BLUE).move_to([2.1,-2.8,0])
        self.play(FadeIn(equal),run_time=.5)
        self.at('Soil moisture became')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        h=heading('Observed in the studied grassland')
        wave=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([[-5.8+i*.23,-.3+(.7 if i%2 else -.7),0] for i in range(15)])
        moisture=VGroup(bt('Soil moisture\nmore variable',26,BLUE).move_to([-4.2,1.5,0]),wave)
        self.play(FadeIn(h),Create(moisture),run_time=.5)
        self.at('plant production fell')
        production=VGroup(bt('Production',28,GREEN).move_to([0,1.5,0]),arr([0,.7,0],[0,-1.1,0],GREEN))
        self.play(FadeIn(production),run_time=.5)
        self.at('and species diversity rose')
        diversity=VGroup(bt('Diversity',28,GREEN).move_to([4.2,1.5,0]),arr([4.2,-1.1,0],[4.2,.7,0],GREEN))
        self.play(FadeIn(diversity),run_time=.5)
        self.at('That result applies')
        bound=bt('Result limited to this grassland',27).move_to([0,-2.2,0])
        self.play(FadeIn(bound),run_time=.5)
        self.at('Repeat it elsewhere')
        repeat=bt('Repeat elsewhere before generalizing',26,GREY).move_to([0,-3,0])
        self.play(FadeIn(repeat),run_time=.5)
        self.at('Compare unsheltered plots')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        self.play(FadeIn(heading('Check the shelter itself')),FadeIn(columns[0]),FadeIn(columns[1]),run_time=.6)
        compare=DoubleArrow([-2.7,.2,0],[-1.6,.2,0],buff=0,color=TEXT,tip_length=.18)
        self.play(GrowArrow(compare),run_time=.5)
        self.at('That checks whether')
        check=bt('Natural pattern in both • shelter effect?',27).move_to([0,-2,0])
        self.play(FadeIn(check),run_time=.5)
        self.finish()


def logger(x,y):
    box=RoundedRectangle(width=.42,height=.65,corner_radius=.06,color=TEXT,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    dot=Dot([x,y+.1,0],radius=.06,color=RED)
    return VGroup(box,dot)


class S09Microclimate(SpokenScene):
    def construct(self):
        h=heading('Paired local temperature loggers')
        forest=Line([-5.45,-1.6,0],[-.95,-1.6,0],color=GREY,stroke_width=4)
        canopy=VGroup(*[tree(-3.2+dx,-1.6,.8,2.15) for dx in (-1.2,0,1.2)])
        open_ground=Line([1,-1.6,0],[5.5,-1.6,0],color=GREY)
        logs=VGroup(logger(-3.2,-.7),logger(3.2,-.7))
        labs=VGroup(bt('under canopy',26,GREEN).move_to([-3.2,-2.3,0]),bt('nearby open habitat',26,GREY).move_to([3.2,-2.3,0]))
        self.at('Organisms also experience')
        self.play(FadeIn(h),FadeIn(forest),FadeIn(canopy),Create(open_ground),FadeIn(logs),FadeIn(labs),run_time=.8)
        self.at('were cooler on average')
        summary=bt('Understory: lower mean and maximum temperature',25,BLUE).move_to([0,2.35,0])
        # Qualitative thermometer bars share a baseline, without invented offsets.
        bars=VGroup(Line([-2.5,-1.4,0],[-2.5,-.2,0],color=BLUE,stroke_width=13),Line([3.9,-1.4,0],[3.9,.5,0],color=RED,stroke_width=13))
        self.play(FadeIn(summary),Create(bars),run_time=.6)
        self.at('In cold conditions')
        neutral=bt('Cold conditions',25,TEXT).move_to([0,2.35,0])
        self.play(ReplacementTransform(summary,neutral),FadeOut(bars),run_time=.3)
        self.at('canopies warmed the understory')
        cold=bt('Cold conditions: canopy warms the understory',25,RED).move_to([0,2.35,0])
        cold_bars=VGroup(Line([-2.5,-1.4,0],[-2.5,-.55,0],color=RED,stroke_width=13),Line([3.9,-1.4,0],[3.9,-1.1,0],color=BLUE,stroke_width=13))
        self.play(ReplacementTransform(neutral,cold),FadeIn(cold_bars),run_time=.7)
        self.at('The temperature an organism')
        note=bt('Local exposure differs from station temperature',25).move_to([0,-3.1,0])
        self.play(FadeIn(note),Indicate(logs[0],color=TEXT),run_time=.6)
        self.at('Climate predicts biomes')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        p=prediction()
        self.play(FadeIn(p),FadeIn(heading('Climate predicts biomes roughly')),run_time=.6)
        self.at('Local conditions modify')
        mods=chip('Local conditions',TEAL,28).move_to([0,-1.8,0])
        ar=arr([0,-1.3,0],[0,-.4,0],GREY)
        self.play(FadeIn(mods),GrowArrow(ar),run_time=.6)
        self.finish()


class S05Diagram(SpokenScene):
    def construct(self):
        # Original made-up station and its linked Walter–Lieth scales.
        x0,x1,y0,hgt=-5.7,1.3,-2,3.9
        def X(i): return x0+(i+.5)*(x1-x0)/12
        def Y(mm): return y0+mm*hgt/200
        h=heading('A smaller point: reading climate')
        title=bt('Made-up lowland station • 30-year means',22,GREY).move_to([-2.2,2.5,0])
        axes=VGroup(Line([x0,y0,0],[x0,Y(200),0],color=GREY),Line([x1,y0,0],[x1,Y(200),0],color=GREY),Line([x0,y0,0],[x1,y0,0],color=GREY))
        ticks=VGroup(*[mt(str(t),22,RED).move_to([x0-.45,Y(2*t),0]) for t in (0,20,40,60,80,100)],*[mt(str(m),22,BLUE).move_to([x1+.55,Y(m),0]) for m in (0,40,80,120,160,200)])
        months=VGroup(*[bt(m,22,GREY).move_to([X(i),y0-.35,0]) for i,m in enumerate(MONTHS)])
        units=VGroup(bt('°C',22,RED).move_to([x0-.45,2.2,0]),bt('mm',22,BLUE).move_to([x1+.55,2.2,0]))
        pts=[[X(i),Y(v),0] for i,v in enumerate(RAIN)]
        rline=VMobject(color=BLUE,stroke_width=5).set_points_as_corners(pts)
        tline=Line([x0,Y(2*TEMP),0],[x1,Y(2*TEMP),0],color=RED,stroke_width=5)
        humid=Polygon(*pts,[X(11),Y(2*TEMP),0],[X(0),Y(2*TEMP),0],stroke_width=0,fill_color=BLUE,fill_opacity=.2)
        self.at('A smaller point')
        self.play(FadeIn(h),FadeIn(title),FadeIn(axes),FadeIn(ticks),FadeIn(months),FadeIn(units),run_time=.7)
        self.at('made up station')
        self.play(Create(rline),Create(tline),FadeIn(humid),run_time=.8)
        warm=bt('warm + humid all year',24,BLUE).move_to([-2.3,-3,0])
        self.play(FadeIn(warm),run_time=.5)
        self.at('Its tropical rainforest climate')
        af=chip('Af climate',GREEN,28).move_to([4.35,1.3,0])
        pred=bt('Tropical wet\nforest prediction',26,GREEN).move_to([4.35,-.1,0])
        ar=arr([4.35,.8,0],[4.35,.4,0],GREY)
        self.play(FadeIn(af),GrowArrow(ar),FadeIn(pred),run_time=.6)
        self.at('That is a hypothesis')
        check=chip('Check observed\nvegetation',TEXT,25).move_to([4.35,-2,0])
        ar2=arr([4.35,-.7,0],[4.35,-1.3,0],GREY)
        self.play(FadeIn(check),GrowArrow(ar2),run_time=.6)
        self.finish()


class S07End(EndCard):
    # The complete requested visual is 18 words; use its first sentence to meet <=12.
    LINE = 'Temperature, water and seasonality organize biomes.'
