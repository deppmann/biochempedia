"""History of life: a fossil date is a floor  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = fossils and traces of life (mounds, fossil bed, fossil dots)
  YELLOW = a measured date, the minimum age, the bracket
  ORANGE = parent atoms (uranium)
  GREEN  = daughter atoms (lead)
  PURPLE = rock and ash (zircon crystal, ash beds)
  TEAL   = one species / lineage drawn as a line
  RED    = where the truth could lie (older), unknown, gone
  GREY   = axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AX_Y = -0.4          # y of the Dresser timeline (s01 and s06)
PIN_X = 2.2          # x of the 3.48 Ga pin


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def mounds(cx, base_y, scale=1.0):
    """three layered mounds side by side (simple half-ellipse outlines, nothing molecular)."""
    specs = [(1.3, 1.25), (1.6, 1.9), (1.1, 1.0)]    # (half width, height)
    gap = 0.18
    total = sum(2 * a for a, _ in specs) + gap * 2
    x = -total / 2
    parts = []
    for a, h in specs:
        xc = x + a
        for k, f in enumerate([1.0, 0.72, 0.45]):
            t = np.linspace(0, np.pi, 40)
            pts = [[xc + a * f * np.cos(u), base_y_local + h * f * np.sin(u), 0] for u in t] if False else None
            pts = [[xc + a * f * np.cos(u), h * f * np.sin(u), 0] for u in t]
            poly = Polygon(*pts, stroke_color=BLUE, stroke_width=3.5 if k == 0 else 2.5,
                           fill_color=BLUE, fill_opacity=0.28 if k == 0 else 0.0)
            parts.append(poly)
        x += 2 * a + gap
    base = Line([-total / 2 - 0.2, 0, 0], [total / 2 + 0.2, 0, 0], color=GREY, stroke_width=5)
    g = VGroup(*parts, base)
    g.scale(scale)
    g.move_to([cx, base_y, 0], aligned_edge=DOWN)
    return g


def dresser_timeline():
    """axis, zone and pin positions shared by s01 and s06."""
    axis = Arrow([5.9, AX_Y, 0], [-6.2, AX_Y, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
    older = T("older", 24, GREY).move_to([-5.5, AX_Y + 0.4, 0])
    younger = T("younger", 24, GREY).move_to([5.0, AX_Y + 0.4, 0])
    pin = Line([PIN_X, AX_Y, 0], [PIN_X, 0.75, 0], color=YELLOW, stroke_width=4)
    tick = Dot([PIN_X, AX_Y, 0], radius=0.12, color=YELLOW)
    lab = T("3.48 Ga", 30, YELLOW, weight=BOLD).move_to([PIN_X + 1.0, AX_Y - 0.5, 0])
    zone = DashedVMobject(Rectangle(width=7.9, height=1.75, stroke_color=RED, stroke_width=3.5,
                                    fill_color=RED, fill_opacity=0.08).move_to([-2.25, -1.17, 0]), num_dashes=60)
    qs = VGroup(*[T("?", 44, RED, weight=BOLD).move_to([x, -1.25, 0]) for x in (-5.2, -3.6, -2.0, -0.4)])
    return axis, older, younger, pin, tick, lab, zone, qs


GRID = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

def atom(color, r=0.38):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)

def crystal(center, w, h, states, d, r):
    """states: 'U' uranium or 'P' lead for the four grid slots."""
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=PURPLE, stroke_width=4,
                           fill_color=PURPLE, fill_opacity=0.14).move_to(center)
    dots = VGroup()
    for (gx, gy), s in zip(GRID, states):
        dots.add(atom(ORANGE if s == "U" else GREEN, r).move_to(np.array(center) + np.array([gx * d, gy * d, 0])))
    return box, dots

def hourglass(cx, cy):
    top = Polygon([cx - 1, cy + 1.7, 0], [cx + 1, cy + 1.7, 0], [cx, cy, 0], stroke_color=GREY, stroke_width=4)
    bot = Polygon([cx, cy, 0], [cx + 1, cy - 1.7, 0], [cx - 1, cy - 1.7, 0], stroke_color=GREY, stroke_width=4)
    return VGroup(top, bot)

def sand_top(cx, cy, f):
    L = 1.7 * np.sqrt(0.78 * max(f, 0.001))
    hw = L / 1.7
    return Polygon([cx - hw, cy + L, 0], [cx + hw, cy + L, 0], [cx, cy, 0], stroke_width=0,
                   fill_color=ORANGE, fill_opacity=0.85)

def sand_bot(cx, cy, f):
    L = 1.7 * (1 - np.sqrt(1 - 0.78 * max(f, 0.001)))
    hw_floor = 0.95
    hw_top = 0.95 * (1 - L / 1.7)
    return Polygon([cx - hw_floor, cy - 1.65, 0], [cx + hw_floor, cy - 1.65, 0],
                   [cx + hw_top, cy - 1.65 + L, 0], [cx - hw_top, cy - 1.65 + L, 0],
                   stroke_width=0, fill_color=GREEN, fill_opacity=0.85)

# Additional schematic colors: BLUE sky / oxygen, PURPLE ozone / UV;
# GOLD iridium / surface mat. Red alga uses muted red, distinct from RED loss.
TAKE_HOME = "Life remade the planet; extinctions and radiations reshaped life."


def heading(text, color=TEXT):
    return T(text, 36, color, font=TITLE_FONT).move_to([0, 3.1, 0])


def life_icon(kind):
    if kind == 'alga':
        g = VGroup(Line([0, 0, 0], [0, 1.15, 0], color='#B85A70', stroke_width=6))
        for y in (.3, .6, .9):
            for s in (-1, 1):
                g.add(Line([0, y, 0], [s*.32, y+.28, 0], color='#B85A70', stroke_width=5))
        return g
    if kind == 'animal':
        g = VGroup(Ellipse(width=.8, height=1.25, color=BLUE, fill_opacity=.16))
        for y in np.linspace(-.42, .42, 7):
            g.add(Line([-.28, y, 0], [.28, y+.08, 0], color=BLUE, stroke_width=2))
        return g
    g = VGroup(Line([0, 0, 0], [0, 1.1, 0], color=TEAL, stroke_width=5))
    for s, y in [(-1, .35), (1, .65)]:
        g.add(Ellipse(width=.5, height=.23, color=TEAL, fill_opacity=.4).rotate(s*.6).move_to([s*.23, y, 0]))
    return g


def sweep_parts():
    # Deliberately expanded late milestones keep labels legible.
    axis = VGroup(arr([-6.1, -.65, 0], [6.1, -.65, 0]),
                  T('older', 22, GREY).move_to([-5.6, -1.18, 0]),
                  T('younger', 22, GREY).move_to([5.5, -1.18, 0]),
                  T('milestones • spacing schematic', 22, GREY).move_to([0, -3.35, 0]))
    xs = [-5, -2.8, -.4, 2, 4.4]
    labels = [('Dresser', '3.48 billion'), ('oxygen', '2.4 billion'),
              ('red alga', '>1 billion'), ('animals', '558 million'), ('land plants', '470 million')]
    icons = [mounds(-5, -.55, .17), Dot([-2.8, .15, 0], radius=.24, color=BLUE)]
    icons += [life_icon(k).move_to([x, .15, 0]) for k, x in zip(['alga','animal','plant'], xs[2:])]
    milestones = VGroup()
    for x, icon, (name, date) in zip(xs, icons, labels):
        milestones.add(VGroup(icon, Line([x, -.65, 0], [x, -.4, 0], color=YELLOW),
                             T(name, 22).move_to([x, 1.25, 0]),
                             T(date, 22, YELLOW).move_to([x, -1.85, 0]),
                             T('years ago', 22, GREY).move_to([x, -2.25, 0])))
    notches = VGroup(*[Line([x, -.88, 0], [x, -.42, 0], color=RED, stroke_width=5)
                        for x in np.linspace(5.15, 5.9, 5)])
    return axis, milestones, notches


def strata(cx=0, cy=0, w=3.5):
    bed = Rectangle(width=w, height=2, color=BLUE, fill_opacity=.12).move_to([cx,cy,0])
    fossils = VGroup(*[Ellipse(width=.55, height=.28, color=BLUE, fill_opacity=.7).move_to([cx+dx,cy+dy,0])
                      for dx,dy in [(-.9,.4),(.1,.55),(.85,.1),(-.4,-.25)]])
    label = T('fossil bed', 26, BLUE).move_to([cx,cy-.7,0])
    ashes = VGroup(*[VGroup(Rectangle(width=w, height=.6, color=PURPLE, fill_opacity=.3).move_to([cx,cy+y,0]),
                              T('ash', 24, PURPLE).move_to([cx,cy+y,0])) for y in (1.4,-1.4)])
    return VGroup(bed, fossils, label), ashes


class S00Title(TitleCard):
    LESSON = 'History of Life and Macroevolution'
    TITLE = 'How Life Remade the Planet'


class S01Sweep(SpokenScene):
    def construct(self):
        axis, marks, notches = sweep_parts()
        title = heading('Most of the story was microbial')
        sky = Rectangle(width=12.2,height=1.6,stroke_width=0,fill_color=ORANGE,fill_opacity=.12).move_to([0,.35,0]).set_z_index(-1)
        self.at('For most of its history')
        self.play(Create(axis), FadeIn(title), FadeIn(sky), run_time=.8)
        self.at('Rocks')
        self.play(FadeIn(marks[0], shift=DOWN*.2), run_time=.7)
        self.at('traces of microbes')
        self.play(Indicate(marks[0][0], color=BLUE), run_time=.7)
        self.at('Oxygen began')
        self.play(FadeOut(title), FadeIn(marks[1]), sky.animate.set_fill(BLUE, .18), run_time=1)
        self.at('algae')
        self.play(FadeIn(marks[2],shift=DOWN*.4),run_time=.6)
        self.at('animals by about')
        self.play(FadeIn(marks[3],shift=DOWN*.4),run_time=.6)
        self.at('plants on land')
        self.play(FadeIn(marks[4],shift=DOWN*.4),run_time=.6)
        self.at('And five times')
        self.play(Create(notches),run_time=.7)
        self.at('mass extinctions')
        self.play(FadeIn(heading('Five mass extinctions', RED)),run_time=.5)
        self.finish()


class S02Oxygen(SpokenScene):
    def construct(self):
        sea = VGroup(Rectangle(width=12,height=2.5,stroke_width=0,fill_color=BLUE,fill_opacity=.12).move_to([0,-1.7,0]),
                     Line([-6,-.45,0],[6,-.45,0],color=BLUE,stroke_width=4))
        cells=VGroup(*[Ellipse(width=1.15,height=.65,color=BLUE,fill_opacity=.25).move_to([x,-1.7,0]) for x in (-3,0,3)])
        oxy=VGroup(*[Dot([x,y,0],radius=.09,color=BLUE) for x,y in [(-5,.4),(-3,1.2),(-1,.5),(1,1.2),(3,.6),(5,1.1)]])
        title=heading('Oxygen builds up in the air')
        self.at('The Great Oxidation Event')
        self.play(FadeIn(sea),FadeIn(cells),FadeIn(title),run_time=.6)
        self.at('first big buildup')
        self.play(LaggedStart(*[FadeIn(d,shift=UP*.3) for d in oxy],lag_ratio=.1),run_time=1)
        note=T('Oxygen-making photosynthesis had already begun',26,GREY).move_to([0,-3.2,0])
        self.at('It was not the start')
        self.play(FadeIn(note),run_time=.5)
        aerobic=T('aerobic metabolism',28,BLUE).move_to([0,-2.5,0])
        self.at('aerobic metabolism spread')
        self.play(cells.animate.set_fill(BLUE,.65),FadeIn(aerobic),run_time=.7)
        band=VGroup(Line([-5.8,1.95,0],[5.8,1.95,0],color=PURPLE,stroke_width=7),T('ozone shield',24,PURPLE).move_to([0,2.35,0]))
        self.at('An ozone layer')
        self.play(Create(band),FadeOut(title),run_time=.6)
        rays=VGroup(*[VGroup(arr([x,3.25,0],[x+.35,2.02,0],PURPLE,3),arr([x+.35,2.02,0],[x+1,2.95,0],PURPLE,3)) for x in (-4,2)])
        self.at('ultraviolet light')
        self.play(LaggedStart(*[Create(r) for r in rays],lag_ratio=.15),run_time=.8)
        self.at('cope with')
        self.play(cells[0].animate.set_stroke(RED,7),cells[2].animate.set_stroke(RED,7),
                  Transform(note,T("oxygen's harm",28,RED).move_to([0,-3.2,0])),run_time=.8)
        self.finish()


def world_map():
    # Simple continent silhouettes; columns are illustrative sites, not coordinates.
    outlines=[ [(-5,1.8),(-3.7,2.4),(-2.6,1.5),(-3.3,.8),(-3.1,.2),(-4,.5)],
               [(-3,.2),(-2.1,-.1),(-1.8,-1),(-2.4,-2),(-2.8,-.8)],
               [(-.7,1.5),(.5,2.3),(2.1,2),(3.8,2.3),(5.2,1.3),(3.7,.6),(1.5,.8),(.4,.3)],
               [(-.4,.8),(1,.7),(1.4,-.2),(.4,-1.6),(-.2,-.7)],
               [(3.6,-1.2),(4.8,-1.1),(5.1,-1.8),(3.8,-1.9)] ]
    return VGroup(*[Polygon(*[[x,y,0] for x,y in pts],color=GREY,stroke_width=2,fill_opacity=.12) for pts in outlines])


class S03Impact(SpokenScene):
    def construct(self):
        definition=VGroup(heading('Mass extinction'),T('More than ¾ of species lost',36,RED),T('in a geologically short time',28,GREY).move_to([0,-.8,0]))
        self.at('A mass extinction')
        self.play(FadeIn(definition),run_time=.6)
        world=world_map()
        title=heading('End-Cretaceous • 66 million years ago')
        self.at('At the end of the Cretaceous')
        self.play(FadeOut(definition),run_time=.25)
        self.play(FadeIn(world),FadeIn(title),run_time=.45)
        cols=VGroup(); bands=VGroup()
        for x in (-4,0,4):
            col=VGroup(*[Rectangle(width=.65,height=.45,color=PURPLE,fill_opacity=.6).move_to([x,y,0]) for y in (.2,.65,1.1)])
            cols.add(col); bands.add(Line([x-.33,.45,0],[x+.33,.45,0],color=GOLD,stroke_width=7))
        ir=T('iridium at the boundary',28,GOLD).move_to([0,-2.55,0])
        self.at('Iridium')
        self.play(FadeIn(cols),FadeIn(ir),run_time=.6)
        self.at('widely separated sites')
        self.play(Create(bands),run_time=.7)
        crater=VGroup(Ellipse(width=.75,height=.28,color=GOLD).move_to([-3.15,.12,0]),
                      Line([-3.15,0,0],[-4.2,-1.6,0],color=GOLD),T('Chicxulub • Mexico',24,GOLD).move_to([-4.2,-2.05,0]))
        self.at('A buried crater')
        self.play(Create(crater),run_time=.8)
        pair=VGroup(T('impact',28,RED).move_to([-3,.9,0]),T('extinction',28,RED).move_to([3,.9,0]),
                    Line([-3,.3,0],[-3,-.5,0],color=PURPLE,stroke_width=10),Line([3,.3,0],[3,-.5,0],color=PURPLE,stroke_width=10))
        bracket=VGroup(DoubleArrow([-3,-1,0],[3,-1,0],buff=0,color=YELLOW),T('synchrony • within 32,000 years',28,YELLOW).move_to([0,-1.6,0]))
        self.at('Dating puts impact')
        self.play(FadeOut(VGroup(world,title,cols,bands,ir,crater)),run_time=.25)
        self.play(FadeIn(pair),Create(bracket),run_time=.55)
        self.at('The impact triggered')
        self.play(GrowArrow(arr([-1.8,.9,0],[1.6,.9,0],RED)),FadeIn(heading('Impact triggered the extinction',RED)),run_time=.8)
        self.finish()


class S04Permian(SpokenScene):
    def construct(self):
        title=heading('End-Permian • 252 million years ago')
        grid=VGroup(*[Ellipse(width=.65,height=.35,color=BLUE,fill_opacity=.7).move_to([x,y,0]) for y in (1.5,.6,-.3,-1.2) for x in (-3,-1.5,0,1.5,3)])
        self.at('The end of the Permian')
        self.play(FadeIn(title),FadeIn(grid),run_time=.7)
        estimate=T('≈81% of marine species • one estimate',30,RED).move_to([0,-2.5,0])
        self.at('about 81')
        self.play(*[g.animate.set_color(GREY).set_fill(GREY,.15) for g in grid[:16]],FadeIn(estimate),run_time=1)
        bed,ashes=strata(-2,0)
        local=heading('Meishan, China')
        self.at('At Meishan in China')
        self.play(FadeOut(VGroup(grid,title,estimate)),run_time=.25)
        self.play(FadeIn(bed),FadeIn(local),run_time=.45)
        self.at('dated ash beds')
        self.play(FadeIn(ashes),run_time=.6)
        bracket=VGroup(Line([.2,-1.4,0],[.6,-1.4,0],color=YELLOW),Line([.6,-1.4,0],[.6,1.4,0],color=YELLOW),Line([.2,1.4,0],[.6,1.4,0],color=YELLOW))
        duration=VGroup(T('≈60,000 years',32,YELLOW),T('wide uncertainty',26,GREY)).arrange(DOWN,buff=.2).move_to([3.2,0,0])
        self.at('took about')
        self.play(Create(bracket),FadeIn(duration),run_time=.7)
        note=T('A clock for one place',30,YELLOW).move_to([0,-2.6,0])
        self.at('That is a clock')
        self.play(FadeIn(note),run_time=.5)
        self.at('Any proposed cause')
        self.play(Transform(note,T('Any proposed cause must fit this clock',30,YELLOW).move_to([0,-2.6,0])),Indicate(bracket,color=YELLOW),run_time=.7)
        self.finish()


def flask(x):
    outline=Polygon([x-.45,1.65,0],[x+.45,1.65,0],[x+.45,.8,0],[x+1.45,-1.6,0],[x-1.45,-1.6,0],[x-.45,.8,0],color=GREY,stroke_width=4)
    liquid=Polygon([x-.83,0,0],[x+.83,0,0],[x+1.37,-1.5,0],[x-1.37,-1.5,0],stroke_width=0,fill_color=BLUE,fill_opacity=.16)
    cells=VGroup(*[Ellipse(width=.22,height=.11,color=BLUE,fill_opacity=.8).move_to([x+dx,y,0]) for dx,y in [(-.4,-.4),(.35,-.4),(-.65,-1.1),(0,-1),(.7,-1.15)]])
    return VGroup(outline,liquid,cells)


class S05Radiation(SpokenScene):
    def construct(self):
        trunk=Line([-5,0,0],[-1,0,0],color=TEAL,stroke_width=6)
        boundary=Line([-1.3,-2,0],[-1.3,2,0],color=RED,stroke_width=5)
        lab=T('end-Cretaceous extinction',24,RED).move_to([-2.4,-2.6,0])
        branches=VGroup(*[Line([-1,0,0],[5,y,0],color=TEAL,stroke_width=4) for y in (-1.8,-.6,.6,1.8)])
        self.at('Extinctions also')
        self.play(Create(trunk),Create(boundary),FadeIn(lab),run_time=.6)
        self.at('Placental mammals diversified')
        self.play(Create(branches),FadeIn(heading('Placental mammals diversify')),run_time=.9)
        caution=T('Timing fits release from competition; does not prove it',25,GREY).move_to([0,-3.25,0])
        self.at('but does not prove it')
        self.play(FadeIn(caution),run_time=.5)
        a,b=flask(-3),flask(3)
        title=heading('One genotype • different environments')
        still=T('still broth',28).move_to([-3,2.2,0]); shaken=T('shaken broth',28).move_to([3,2.2,0])
        self.at('A flask can test')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(a[0]),FadeIn(a[1]),FadeIn(title),FadeIn(still),run_time=.45)
        self.at('in still broth')
        self.play(FadeIn(a[2]),run_time=.5)
        mat=Line([-3.8,0,0],[-2.2,0,0],color=GOLD,stroke_width=10)
        variants=VGroup(*[RoundedRectangle(width=.24,height=.17,corner_radius=.04,color=TEAL,fill_opacity=.8).move_to([-3+dx,y,0]) for dx,y in [(-.6,-1.1),(0,-1),(.7,-1.15)]])
        self.at('New heritable types')
        self.play(Create(mat),ReplacementTransform(a[2][2:],variants),run_time=.8)
        self.at('In shaken broth')
        self.play(FadeIn(b),FadeIn(shaken),run_time=.6)
        self.play(b.animate.shift(RIGHT*.12),run_time=.15)
        self.play(b.animate.shift(LEFT*.24),run_time=.15)
        self.play(b.animate.shift(RIGHT*.12),run_time=.15)
        self.at('These were new types')
        self.play(FadeIn(T('New heritable types ≠ new species',30,YELLOW).move_to([0,-2.7,0])),run_time=.6)
        self.finish()


class S06Dates(SpokenScene):
    def construct(self):
        box,dots=crystal([-2,0,0],3,2.9,'UUUU',.65,.28)
        title=heading('How do we know when?')
        self.at('How do we know when')
        self.play(FadeIn(title),run_time=.4)
        self.at('Zircon in volcanic ash')
        self.play(FadeIn(box),FadeIn(dots),FadeIn(T('zircon',28,PURPLE).move_to([-2,-2,0])),run_time=.6)
        key=VGroup(T('uranium',30,ORANGE),T('↓',30,GREY),T('lead',30,GREEN)).arrange(DOWN,buff=.25).move_to([2.5,0,0])
        self.at('Uranium decays to lead')
        self.play(FadeIn(key),dots[0].animate.set_color(GREEN).set_fill(GREEN,.9),run_time=.6)
        self.at('at a steady rate')
        self.play(dots[1].animate.set_color(GREEN).set_fill(GREEN,.9),run_time=.6)
        bed,ashes=strata(-2,0)
        bracket=VGroup(Line([.1,-1.4,0],[.5,-1.4,0],color=YELLOW),Line([.5,-1.4,0],[.5,1.4,0],color=YELLOW),Line([.1,1.4,0],[.5,1.4,0],color=YELLOW),T('age bracket',30,YELLOW).move_to([3,0,0]))
        self.at('Ash beds above and below')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        self.play(FadeIn(bed),FadeIn(ashes),run_time=.4)
        self.at('bracket its age')
        self.play(Create(bracket),run_time=.5)
        axis,older,younger,pin,tick,lab,zone,qs=dresser_timeline()
        self.at('But the oldest fossil')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        self.play(Create(axis),FadeIn(older),FadeIn(younger),FadeIn(heading('The oldest fossil is a floor')),run_time=.4)
        self.at('Life existed by')
        self.play(Create(pin),FadeIn(tick),FadeIn(lab),FadeIn(mounds(PIN_X,1.05,.45)),run_time=.6)
        self.at('It may be older')
        self.play(FadeIn(zone),FadeIn(qs),FadeIn(T('Life may be older',30,RED).move_to([0,-3,0])),run_time=.6)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        axis,marks,notches=sweep_parts()
        self.at('So the history of life')
        self.play(Create(axis),FadeIn(marks),Create(notches),run_time=.7)
        chips=VGroup(*[chip(t,c,26) for t,c in [('transitions',BLUE),('extinctions',RED),('radiations',TEAL)]]).arrange(RIGHT,buff=.5).move_to([0,2.8,0])
        self.at('transitions that')
        self.play(FadeIn(chips[0]),run_time=.4)
        self.at('extinctions that')
        self.play(FadeIn(chips[1]),run_time=.4)
        self.at('radiations that')
        self.play(FadeIn(chips[2]),run_time=.4)
        line=VGroup(T('Fossil dates tell us when life existed,',34,font=TITLE_FONT),T('at the latest.',38,YELLOW,font=TITLE_FONT)).arrange(DOWN,buff=.25)
        self.at('with fossil dates')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(line),run_time=.55)
        self.finish()


class S08End(EndCard):
    LINE = TAKE_HOME
