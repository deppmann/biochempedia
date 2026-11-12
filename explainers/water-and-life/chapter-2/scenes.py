"""Where the Sunshine Goes (water and life, film 2).

COLOR MAP (identical to film 1)
  OXYGEN END = RED                 HYDROGEN ENDS = HB blue
  COVALENT BOND = light-grey bar  HYDROGEN BOND = dashed GOLD
  liquid WATER = pale BLUE        SAND = TAN
  ENERGY = ORANGE dots            CELLULOSE = BROWN

Cartoons and blocks are schematic. No molecular structure is shown.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HB = "#4A86FF"
LG = "#C8CCD4"
TAN = "#D3A86B"
ORANGE = "#F39A3D"
PANEL = "#171b26"
SKY = "#243044"


def lbl(s, p, color=TEXT, size=32, weight=NORMAL):
    return T(s, size=size, color=color, weight=weight).move_to(p)


def clock_of(scene):
    c = ValueTracker(0)
    c.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(c)
    return c


def block(w, h, color, opacity=0.55, radius=0.18):
    return RoundedRectangle(corner_radius=radius, width=w, height=h, stroke_color=color,
                            stroke_width=4, fill_color=color, fill_opacity=opacity)


def mol(s=1.0, letters=False):
    """The same wide-V block cartoon used in chapter 1."""
    O = VGroup(block(1.2*s, 1.0*s, RED, .85, .15*s).move_to([0, -.65*s, 0]))
    Hl = VGroup(block(.8*s, .8*s, HB, .85, .12*s).move_to([-1.6*s, .75*s, 0]))
    Hr = VGroup(block(.8*s, .8*s, HB, .85, .12*s).move_to([1.6*s, .75*s, 0]))
    if letters:
        for g, ch, fs in ((O, "O", 42), (Hl, "H", 34), (Hr, "H", 34)):
            g.add(T(ch, size=max(22, fs*s), weight=BOLD).move_to(g[0]))
    bl = Line(O[0], Hl[0], color=LG, stroke_width=max(3, 8*s)).set_z_index(-1)
    br = Line(O[0], Hr[0], color=LG, stroke_width=max(3, 8*s)).set_z_index(-1)
    g = VGroup(bl, br, O, Hl, Hr)
    g.O, g.Hl, g.Hr = O, Hl, Hr
    return g


def gline(a, b, w=4, opacity=1):
    a, b = np.array(a), np.array(b)
    d = b-a
    if np.linalg.norm(d) < .2:
        return VGroup()
    u = d/np.linalg.norm(d)
    return DashedLine(a+u*.22, b-u*.22, color=GOLD, stroke_width=w,
                      dash_length=.12, dashed_ratio=.55).set_opacity(opacity)


def energy_dot(p, r=.11):
    return Dot(p, radius=r, color=ORANGE)


def thermometer(x, y, level, label=None, scale=1.0):
    """A large readout whose fill is tied directly to level (0..1)."""
    h = 3.1*scale
    tube = RoundedRectangle(corner_radius=.18, width=.48*scale, height=h,
                            stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    bulb = Circle(radius=.34*scale, stroke_color=TEXT, stroke_width=3,
                  fill_color=RED, fill_opacity=.95).move_to([x, y-h/2-.12*scale, 0])
    val = float(np.clip(level, 0, 1))
    fh = (.25 + 2.5*val)*scale
    fill = RoundedRectangle(corner_radius=.1, width=.23*scale, height=fh,
                            stroke_width=0, fill_color=RED, fill_opacity=.95)
    fill.move_to([x, tube.get_bottom()[1]+.14*scale+fh/2, 0])
    g = VGroup(tube, fill, bulb)
    if label:
        g.add(lbl(label, [x, y+h/2+.38*scale, 0], size=28))
    return g


def sand_particles(center=(-3.4, -.7), vigor=0, stretch=0, t=0):
    """Computed particle positions and neighbor springs for the sand cartoon."""
    pts = []
    for r in range(3):
        for c in range(4):
            x = center[0] - 1.35 + .9*c + .12*(r%2)
            y = center[1] - .85 + .8*r
            phase = 1.7*r + 2.3*c
            x += vigor*.10*np.sin(5*t+phase)
            y += vigor*.09*np.cos(4.3*t+phase)
            pts.append(np.array([x, y, 0]))
    springs = VGroup()
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            d = np.linalg.norm(pts[i]-pts[j])
            if .65 < d < 1.05:
                mid = (pts[i]+pts[j])/2
                a = pts[i] + (pts[i]-mid)*.06*stretch
                b = pts[j] + (pts[j]-mid)*.06*stretch
                springs.add(Line(a, b, color=LG, stroke_width=2, stroke_opacity=.55))
    dots = VGroup(*[Dot(p, radius=.17, color=TAN) for p in pts])
    return VGroup(springs, dots)


def water_web(center=(3.2, -.7), vigor=0, web=1, t=0):
    """A moving wide-V water crowd with partner-changing computed gold links."""
    ms, pts = VGroup(), []
    for r in range(3):
        for c in range(4):
            base = np.array([center[0]-1.45+.95*c+.14*(r%2), center[1]-.9+.85*r, 0])
            ph = 1.3*r+2.1*c
            p = base + vigor*np.array([.10*np.sin(4.4*t+ph), .09*np.cos(4.9*t+ph), 0])
            m = mol(.18).move_to(p).rotate(.25*np.sin(.9*t+ph))
            ms.add(m); pts.append(p)
    links = VGroup()
    shift = int(t*.7) % 2
    for r in range(3):
        for c in range(3):
            if (c+r+shift)%2 == 0:
                i, j = r*4+c, r*4+c+1
                links.add(gline(pts[i], pts[j], 3, web))
    return VGroup(links, ms)


def pair_world(sand_level=.8, water_level=.8, t=0, night=False, streams=False):
    """The carried side-by-side world for scenes 3, 4, 5, 7, 8 and 9."""
    sky = Rectangle(width=13.2, height=6.8, stroke_width=0, fill_color=SKY if night else PANEL,
                    fill_opacity=1).move_to([0, -.15, 0]).set_z_index(-5)
    sb = block(5.4, 3.25, TAN, .22).move_to([-3.35, -.75, 0])
    wb = block(5.4, 3.25, BLUE, .22).move_to([3.35, -.75, 0])
    ly = -2.75 if streams else 1.25   # night view: names below the blocks so the stream never crosses them
    sl = lbl("dry sand   100 g", [-3.35, ly, 0], TAN, 30, BOLD)
    wl = lbl("water   100 g", [3.35, ly, 0], BLUE, 30, BOLD)
    st = thermometer(-5.55, -.45, sand_level, scale=.72)
    wt = thermometer(5.55, -.45, water_level, scale=.72)
    particles = sand_particles((-3.2, -.75), .25, .1, t)
    web = water_web((3.2, -.75), .25, 1, t)
    g = VGroup(sky, sb, wb, sl, wl, st, wt, particles, web)
    if streams:
        for x in (-4.1, -3.45, -2.8, 2.6, 3.25, 3.9):
            yy = .95 + .1*np.sin(t*2+x)
            d = energy_dot([x, yy, 0], .09)
            d.shift(UP*((t*.45 + abs(x)*.17) % 0.65))
            g.add(d)
        g.add(lbl("same energy loss per minute", [0, 2.95, 0], ORANGE, 30, BOLD))
    return g


class S00Title(TitleCard):
    LESSON = "Water and life"
    TITLE = "Where the Sunshine Goes"


class S01Question(SpokenScene):
    def construct(self):
        c = clock_of(self)
        sun = Circle(radius=.62, color=ORANGE, fill_color=ORANGE, fill_opacity=.95).move_to([0, 2.75, 0])
        sand = Polygon([-6.7, .6, 0], [0, .6, 0], [0, -3.5, 0], [-6.7, -3.5, 0],
                       stroke_width=0, fill_color=TAN, fill_opacity=.75)
        water = Polygon([0, .6, 0], [6.7, .6, 0], [6.7, -3.5, 0], [0, -3.5, 0],
                        stroke_width=0, fill_color=BLUE, fill_opacity=.55)
        rays = VGroup(*[energy_dot([x, 1.7, 0]) for x in (-4.8, -3.2, -1.6, 1.6, 3.2, 4.8)])
        self.play(FadeIn(VGroup(sand, water)), GrowFromCenter(sun), run_time=1.0)
        self.at("Same sun")
        self.play(FadeIn(rays), rays.animate.shift(DOWN*1.5), run_time=1.5)
        foot = VGroup(Ellipse(width=1.25, height=2.1, color=TEXT, fill_color=TEXT, fill_opacity=.18),
                      *[Circle(radius=.12, color=TEXT, fill_color=TEXT, fill_opacity=.5) for _ in range(4)])
        foot[0].rotate(-.3); foot.move_to([-3.2, -.8, 0])
        hand = RoundedRectangle(corner_radius=.35, width=1.2, height=2.4, color=TEXT,
                                fill_color=TEXT, fill_opacity=.18).rotate(.65).move_to([3.2, -.8, 0])
        self.at("Why is the beach")
        self.play(FadeIn(foot), foot.animate.shift(UP*.75), run_time=1.1, rate_func=there_and_back)
        self.at("while the water")
        self.play(FadeIn(hand), run_time=.7)
        q = T("?", size=120, color=GOLD, weight=BOLD).move_to([0, -.7, 0])
        self.play(GrowFromCenter(q), run_time=.7)
        self.at("The first film")
        inset = RoundedRectangle(corner_radius=.18, width=3.1, height=2.25, color=BLUE,
                                 fill_color=PANEL, fill_opacity=.96).move_to([4.8, 2.35, 0])
        crowd = always_redraw(lambda: water_web((4.8, 2.25), .45, .9, c.get_value()).scale(.48))
        inset.set_z_index(-1)
        self.play(FadeIn(inset), run_time=.7)
        self.add(crowd)
        self.wait(.4)
        self.at("Now we follow")
        path = Arrow(sun.get_bottom(), inset.get_left()+LEFT*.15, buff=.2, color=ORANGE, stroke_width=6)
        self.play(GrowArrow(path), Indicate(inset, color=GOLD, scale_factor=1.04), run_time=1.3)
        self.finish()


class S02Temperature(SpokenScene):
    def construct(self):
        c = clock_of(self); speed = ValueTracker(.25); level = ValueTracker(.25)
        box = block(8.2, 5.2, BLUE, .08).move_to([-.65, -.25, 0])
        bases = [(-3.6+1.25*(i%6), -1.7+1.25*(i//6)) for i in range(18)]
        def dots():
            t, v = c.get_value(), speed.get_value()
            return VGroup(*[Dot([x+.16*v*np.sin((3+i%3)*t+i), y+.16*v*np.cos((4+i%4)*t+2*i), 0],
                                 radius=.15, color=BLUE) for i,(x,y) in enumerate(bases)])
        particles = always_redraw(dots)
        therm = always_redraw(lambda: thermometer(5.35, -.15, level.get_value(), scale=1.0))
        self.add(particles, therm)
        self.play(FadeIn(box), run_time=1.0)
        self.at("what does a thermometer")
        self.play(Indicate(therm, color=GOLD, scale_factor=1.05), run_time=.9)
        self.at("Temperature tracks")
        cap = lbl("temperature reflects average kinetic energy", [0, 3.1, 0], TEXT, 32, BOLD)
        self.play(FadeIn(cap), run_time=.7)
        self.at("Faster jiggling")
        self.play(speed.animate.set_value(1.0), level.animate.set_value(.9), run_time=1.6)
        self.at("slower jiggling")
        self.play(speed.animate.set_value(.12), level.animate.set_value(.12), run_time=1.6)
        self.finish()


class S03Blocks(SpokenScene):
    def construct(self):
        c = clock_of(self)
        world = always_redraw(lambda: pair_world(.25, .25, c.get_value()))
        self.at("Take equal masses")
        self.add(world)
        self.wait(1.4)
        self.at("Give each exactly")
        meters = VGroup()
        dots = VGroup()
        for x in (-3.35, 3.35):
            meters.add(block(3.2, .7, ORANGE, .08).move_to([x, 2.45, 0]))
            dots.add(VGroup(*[energy_dot([x-1.15+.33*i, 2.45, 0], .1) for i in range(8)]))
        self.play(FadeIn(meters), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=.12), run_time=1.6)
        tag = lbl("836.8 J each", [0, 3.25, 0], ORANGE, 32, BOLD)
        self.play(FadeIn(tag), run_time=.5)
        self.at("Then watch")
        self.play(*[Indicate(d, color=ORANGE, scale_factor=1.06) for d in dots], run_time=1.0)
        self.finish()


class S04Sand(SpokenScene):
    def construct(self):
        c = clock_of(self); vigor=ValueTracker(.2); stretch=ValueTracker(.1); level=ValueTracker(.25)
        sb = block(10.2, 5.2, TAN, .18).move_to([-.5, -.35, 0])
        pic = always_redraw(lambda: sand_particles((-.8, -.55), vigor.get_value(), stretch.get_value(), c.get_value()).scale(1.5))
        therm = always_redraw(lambda: thermometer(5.35, -.25, level.get_value()))
        meter = block(5.0, .65, ORANGE, .06).move_to([-.8, 2.65, 0])
        ed = VGroup(*[energy_dot([-2.65+.52*i, 2.65, 0], .12) for i in range(8)])
        self.add(sb, pic, therm, meter, ed)
        self.at("particles vibrate harder")
        self.play(ed.animate.shift(DOWN*1.0).set_opacity(.35), vigor.animate.set_value(1), run_time=1.5)
        self.at("pulls between them stretch")
        self.play(stretch.animate.set_value(1), run_time=1.25)
        acct = lbl("one account: faster vibration + stretched attractions", [0, -3.25, 0], TEXT, 28, BOLD)
        self.play(FadeIn(acct), run_time=.5)
        self.at("thermometer climbs")
        self.play(level.animate.set_value(.9), run_time=1.1)
        tag = lbl("about +10 °C", [4.85, 2.8, 0], RED, 30, BOLD)
        calc = M("836.8 ÷ (100 × 0.8) ≈ 10.5 °C", size=28, color=TAN).move_to([0, 3.35, 0])
        schem = lbl("schematic", [-5.25, 2.8, 0], LG, 28)
        self.play(FadeIn(tag), FadeIn(calc), FadeIn(schem), run_time=.6)
        self.finish()


class S05Water(SpokenScene):
    def construct(self):
        c=clock_of(self); vigor=ValueTracker(.2); web=ValueTracker(1); level=ValueTracker(.25)
        wb=block(10.2,5.2,BLUE,.18).move_to([-.5,-.35,0])
        pic=always_redraw(lambda: water_web((-.8,-.55),vigor.get_value(),web.get_value(),c.get_value()).scale(1.5))
        therm=always_redraw(lambda: thermometer(5.35,-.25,level.get_value()))
        meter=block(5,.65,ORANGE,.06).move_to([-.8,2.65,0])
        ed=VGroup(*[energy_dot([-2.65+.52*i,2.65,0],.12) for i in range(8)])
        self.add(wb,pic,therm,meter,ed)
        self.at("molecules speed up")
        self.play(ed.animate.shift(DOWN*.8).set_opacity(.35),vigor.animate.set_value(1),run_time=1.4)
        self.at("web of hydrogen bonds")
        halo=SurroundingRectangle(wb,buff=.08,color=GOLD,stroke_width=6)
        self.play(FadeIn(halo),run_time=.45)
        self.play(FadeOut(halo),run_time=.45)
        self.at("stretches")
        self.play(web.animate.set_value(.25),run_time=.8)
        self.at("bends")
        self.play(Rotate(pic,angle=.08),run_time=.5)
        self.at("rearranges")
        self.play(web.animate.set_value(1),run_time=1.0)
        acct=lbl("one account: faster motion + rearranging hydrogen-bond web",[0,-3.25,0],TEXT,28,BOLD)
        self.at("that takes extra energy")
        self.play(FadeIn(acct),run_time=.6)
        self.at("thermometer climbs")
        self.play(level.animate.set_value(.39),run_time=1.0)
        tag=lbl("about +2 °C",[4.9,2.8,0],RED,30,BOLD)
        calc=M("836.8 ÷ (100 × 4.18) = 2.0 °C",size=28,color=BLUE).move_to([0,3.35,0])
        schem=lbl("schematic",[-5.25,2.8,0],LG,28)
        self.play(FadeIn(tag),FadeIn(calc),FadeIn(schem),run_time=.6)
        self.finish()


class S06Specific(SpokenScene):
    def construct(self):
        c=clock_of(self); hs=ValueTracker(.05); hw=ValueTracker(.05)
        title=lbl("specific heat   (J per g per °C)",[0,3.25,0],TEXT,36,BOLD)
        def bars():
            a=Rectangle(width=3,height=max(.04,hs.get_value()),stroke_color=TAN,stroke_width=4,fill_color=TAN,fill_opacity=.65).move_to([-2.2,-2.6+hs.get_value()/2,0])
            b=Rectangle(width=3,height=max(.04,hw.get_value()),stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.65).move_to([2.2,-2.6+hw.get_value()/2,0])
            return VGroup(a,b)
        bars_m=always_redraw(bars)
        self.add(bars_m)
        self.play(FadeIn(title),run_time=.8)
        self.at("energy needed")
        self.play(hs.animate.set_value(.8),run_time=1.0)
        sand=lbl("dry sand ≈ 0.8",[-2.2,-3.15,0],TAN,30,BOLD)
        self.play(FadeIn(sand),run_time=.4)
        self.at("Per gram")
        per=lbl("per gram",[0,2.55,0],GOLD,30,BOLD)
        self.play(FadeIn(per),run_time=.4)
        self.at("water needs about five")
        self.play(hw.animate.set_value(4.18),run_time=2.0)
        water=lbl("water ≈ 4.18",[2.2,-3.15,0],BLUE,30,BOLD)
        five=lbl("about 5×",[4.95,1.7,0],GOLD,36,BOLD)
        self.play(FadeIn(water),FadeIn(five),run_time=.6)
        self.at("specific heat is high")
        hi=SurroundingRectangle(Rectangle(width=3,height=4.18).move_to([2.2,-.51,0]),buff=.08,color=BLUE,stroke_width=6)
        self.play(FadeIn(hi),run_time=.4); self.play(FadeOut(hi),run_time=.4)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        c=clock_of(self); sl=ValueTracker(.88); wl=ValueTracker(.88)
        world=always_redraw(lambda: pair_world(sl.get_value(),wl.get_value(),c.get_value(),True,True))
        self.at("Night falls")
        self.add(world)
        self.wait(1.1)
        moon=Circle(radius=.42,color=LG,fill_color=LG,fill_opacity=.85).move_to([5.4,2.2,0])
        self.play(GrowFromCenter(moon),run_time=.6)
        self.at("same steady rate")
        self.play(sl.animate.set_value(.76),wl.animate.set_value(.76),run_time=1.4)
        self.at("Will the water's")
        q=lbl("Water temperature: faster or slower?",[0,2.3,0],GOLD,38,BOLD)
        self.play(FadeOut(moon),run_time=.25)
        self.play(FadeIn(q),run_time=.45)
        self.at("Pause and decide")
        self.play(Indicate(q,color=GOLD,scale_factor=1.06),run_time=1.0)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        c=clock_of(self)
        world=always_redraw(lambda: pair_world(.76,.76,c.get_value(),True,True))
        q=lbl("Water temperature: faster or slower?",[0,2.3,0],GOLD,38,BOLD)
        bg=Circle(radius=.48,color=LG,stroke_width=5).move_to([5.9,2.85,0])
        ring=always_redraw(lambda: Arc(radius=.48,start_angle=PI/2,angle=TAU*max(0,1-c.get_value()/5),
                                      color=GOLD,stroke_width=7).move_to(bg))
        self.add(world,q,bg,ring)
        self.wait(5)


class S09Reveal(SpokenScene):
    def construct(self):
        c=clock_of(self); sl=ValueTracker(.76); wl=ValueTracker(.76); reform=ValueTracker(.25)
        world=always_redraw(lambda: pair_world(sl.get_value(),wl.get_value(),c.get_value(),True,True))
        self.add(world)
        ans=lbl("SLOWER",[0,2.3,0],GOLD,52,BOLD)
        self.at("Slower")
        self.play(FadeIn(ans,scale=1.3),run_time=.7)
        self.at("five times as much")
        self.play(sl.animate.set_value(.28),wl.animate.set_value(.66),run_time=2.0)
        self.at("hydrogen bonds reform")
        bonds=VGroup(gline([2.25,-1.35,0],[3.05,-1.35,0],6),
                     gline([3.25,-.45,0],[4.05,-.45,0],6),
                     gline([2.7,.35,0],[3.5,.35,0],6))
        self.play(LaggedStart(*[Create(x) for x in bonds],lag_ratio=.25),reform.animate.set_value(1),run_time=1.4)
        released=VGroup(*[energy_dot([2.2+.42*i,.55+.12*(i%2),0],.09) for i in range(6)])
        self.at("give energy back")
        self.play(LaggedStart(*[FadeIn(d,shift=UP*.4) for d in released],lag_ratio=.12),run_time=1.0)
        self.at("water stays warm")
        self.play(sl.animate.set_value(.12),wl.animate.set_value(.56),FadeOut(ans),run_time=1.4)
        schem=lbl("schematic",[-5.35,-3.25,0],LG,28)
        self.play(FadeIn(schem),run_time=.4)
        self.finish()


def vessel(x,w,h,level=.75):
    outline=VGroup(Line([x-w/2,h/2,0],[x-w/2,-h/2,0]),Line([x-w/2,-h/2,0],[x+w/2,-h/2,0]),Line([x+w/2,-h/2,0],[x+w/2,h/2,0])).set_stroke(LG,5)
    water=Rectangle(width=w-.08,height=(h-.1)*level,stroke_width=0,fill_color=BLUE,fill_opacity=.55).move_to([x,-h/2+(h-.1)*level/2+.05,0])
    return VGroup(water,outline)


class S10Capacity(SpokenScene):
    def construct(self):
        c=clock_of(self); cup_l=ValueTracker(.25); bath_l=ValueTracker(.25)
        cup=vessel(-3.7,2.2,2.7); bath=vessel(2.4,6.2,3.6)
        ripples=always_redraw(lambda: VGroup(
            Line([-4.72,.33+.035*np.sin(1.7*c.get_value()),0],[-2.68,.33+.035*np.sin(1.7*c.get_value()+1),0],color=BLUE,stroke_width=5),
            Line([-.55,.46+.04*np.sin(1.4*c.get_value()),0],[5.35,.46+.04*np.sin(1.4*c.get_value()+1),0],color=BLUE,stroke_width=5)))
        show=ValueTracker(0)
        def jig():
            t=c.get_value(); gs=VGroup()
            for cx,hw,ys in ((-3.7,.85,(-1.0,-.55,-.1)),(2.4,2.7,(-1.5,-1.0,-.55,-.1))):
                n=4 if cx<0 else 11
                for i in range(n):
                    for k,y in enumerate(ys):
                        if (i+k)%2: continue
                        x=cx-hw+(i+.5)*2*hw/n+.3*np.sin(2.2*t+i*1.7+k)
                        gs.add(Dot([x,y+.18*np.cos(1.9*t+i+k*2.3),0],radius=.09,color=WHITE).set_opacity(.85*show.get_value()))
            return gs
        self.add(always_redraw(jig))
        self.add(ripples)
        self.at("bay is not one gram")
        self.play(FadeIn(cup),FadeIn(bath),show.animate.set_value(1),run_time=1.1)
        self.at("Heat capacity")
        eq=lbl("heat capacity = mass × specific heat",[0,3.25,0],GOLD,36,BOLD)
        self.play(FadeIn(eq),run_time=.7)
        self.at("warm a whole object")
        self.play(Indicate(cup,color=BLUE,scale_factor=1.04),Indicate(bath,color=BLUE,scale_factor=1.03),run_time=1.1)
        self.at("A cup and a bathtub")
        cl=lbl("same specific heat",[-3.7,-2.55,0],BLUE,28,BOLD)
        bl=lbl("same specific heat",[2.4,-2.55,0],BLUE,28,BOLD)
        self.play(FadeIn(cl),FadeIn(bl),run_time=.6)
        self.at("bathtub has far more")
        mass=lbl("much more mass",[4.9,2.15,0],TEXT,32,BOLD)
        self.play(FadeIn(mass),run_time=.6)
        lamps=VGroup(*[VGroup(Arc(radius=.42,start_angle=0,angle=PI,color=ORANGE,stroke_width=8),Line([0,0,0],[0,-.65,0],color=ORANGE,stroke_width=5)).move_to([x,2.25,0]) for x in (-3.7,2.4)])
        self.at("same heater")
        self.play(FadeIn(lamps),run_time=.5)
        dots=VGroup(*[energy_dot([x,1.3-.33*i,0],.1) for x in (-3.7,2.4) for i in range(4)])
        self.play(FadeIn(dots),run_time=.6)
        ct=always_redraw(lambda: thermometer(-5.5,-.1,cup_l.get_value(),scale=.7))
        bt=always_redraw(lambda: thermometer(5.9,-.1,bath_l.get_value(),scale=.7))
        self.add(ct,bt)
        self.play(cup_l.animate.set_value(.88),bath_l.animate.set_value(.35),run_time=2.2)
        self.finish()


def bay(t=0, with_life=False):
    surface=.65+.06*np.sin(1.4*t)
    xs=np.linspace(-6.7,6.7,60)
    pts=[[x,surface+.08*np.sin(.7*x+1.2*t),0] for x in xs]
    water=Polygon(*pts,[6.7,-3.55,0],[-6.7,-3.55,0],stroke_width=0,fill_color=BLUE,fill_opacity=.5)
    top=VMobject().set_points_as_corners(pts).set_stroke(BLUE,5)
    return VGroup(water,top)


class S11Bay(SpokenScene):
    def construct(self):
        c=clock_of(self); b=always_redraw(lambda: bay(c.get_value()))
        self.at("picture the bay")
        self.add(b)
        self.wait(1.0)
        sun=Circle(radius=.55,color=ORANGE,fill_color=ORANGE,fill_opacity=.9).move_to([-4.9,2.7,0])
        ed=VGroup(*[energy_dot([-4.9+.7*i,1.75,0],.11) for i in range(7)])
        self.play(GrowFromCenter(sun),FadeIn(ed),run_time=.8)
        self.at("Waves and currents")
        arrows=VGroup(ArcBetweenPoints([-4,.3,0],[-1,-2.3,0],angle=.7,color=TEXT,stroke_width=7),ArcBetweenPoints([1,-2.3,0],[4,.3,0],angle=.7,color=TEXT,stroke_width=7))
        for a in arrows: a.add_tip(tip_length=.22)
        self.play(Create(arrows),ed.animate.arrange_in_grid(2,4,buff=.7).move_to([0,-1.2,0]),run_time=2.0)
        self.at("huge mass of water")
        self.play(ShowPassingFlash(Line([-6.2,-2.9,0],[6.2,-2.9,0],color=BLUE,stroke_width=8)),run_time=1.0)
        self.at("water evaporates")
        vap=VGroup(*[ArcBetweenPoints([x,.8,0],[x+.2,2.0,0],angle=.3,color=LG,stroke_width=4) for x in (3.5,4.3,5.1)])
        loss=VGroup(*[energy_dot([x,2.15,0],.09) for x in (3.5,4.3,5.1)])
        lab=lbl("evaporation",[4.35,2.75,0],TEXT,30,BOLD)
        self.play(Create(vap),FadeIn(loss),FadeIn(lab),run_time=1.3)
        schem=lbl("schematic",[-5.45,-3.15,0],LG,28)
        self.play(FadeIn(schem),run_time=.4)
        self.finish()


class S12Three(SpokenScene):
    def construct(self):
        c=clock_of(self); b=always_redraw(lambda: bay(c.get_value()).set_opacity(.28))
        self.add(b)
        title=lbl("THREE THINGS KEEP A BAY STEADY",[0,3.2,0],TEXT,36,BOLD)
        self.at("three things")
        self.play(FadeIn(title),run_time=.7)
        xs=(-4.2,0,4.2)
        panels=VGroup(*[block(3.7,4.4,BLUE,.08).move_to([x,-.3,0]) for x in xs])
        self.play(FadeIn(panels),run_time=.6)
        self.at("Each gram is slow")
        one=block(1.35,1.35,BLUE,.55).move_to([xs[0],.1,0])
        mini=water_web((xs[0],.1),.2,1,c.get_value()).scale(.35)
        l1=lbl("each gram",[xs[0],-1.75,0],BLUE,30,BOLD); l1b=lbl("slow to warm",[xs[0],-2.25,0],TEXT,28)
        self.play(FadeIn(one),FadeIn(mini),FadeIn(l1),FadeIn(l1b),run_time=1.0)
        self.at("huge mass")
        deep=Rectangle(width=2.7,height=2.6,stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.45).move_to([0,.0,0])
        arr=ArcBetweenPoints([-.8,.7,0],[.8,-.8,0],angle=.8,color=TEXT,stroke_width=6).add_tip(tip_length=.2)
        l2=lbl("huge mass",[0,-1.75,0],BLUE,30,BOLD); l2b=lbl("mixing",[0,-2.25,0],TEXT,28)
        self.play(FadeIn(deep),Create(arr),FadeIn(l2),FadeIn(l2b),run_time=1.0)
        self.at("evaporation")
        vap=VGroup(*[ArcBetweenPoints([xs[2]+dx,-.5,0],[xs[2]+dx+.15,1.0,0],angle=.3,color=LG,stroke_width=4) for dx in (-.7,0,.7)])
        l3=lbl("evaporation",[xs[2],-1.75,0],BLUE,30,BOLD); l3b=lbl("carries heat away",[xs[2],-2.25,0],TEXT,28)
        self.play(Create(vap),FadeIn(l3),FadeIn(l3b),run_time=1.0)
        self.finish()


def fish(p,s=.7):
    body=Ellipse(width=1.25*s,height=.65*s,color=LG,fill_color=LG,fill_opacity=.7).move_to(p)
    tail=Triangle(color=LG,fill_color=LG,fill_opacity=.7).scale(.35*s).rotate(-PI/2).next_to(body,LEFT,buff=-.08)
    eye=Dot(body.get_center()+RIGHT*.35*s+UP*.1*s,radius=.04,color=BG)
    return VGroup(tail,body,eye)


class S13Life(SpokenScene):
    def construct(self):
        c=clock_of(self); air=ValueTracker(.5); wat=ValueTracker(.5)
        b=always_redraw(lambda: bay(c.get_value()))
        grasses=VGroup(*[ArcBetweenPoints([x,-3.3,0],[x+.2,-1.6,0],angle=.2,color="#7FAE74",stroke_width=8) for x in (-5,-4.5,-4,4.5,5)])
        animals=VGroup(fish([-2,-1.2,0]),fish([1.6,-2.2,0],.85))
        crab=VGroup(Circle(radius=.38,color=HB,fill_color=HB,fill_opacity=.65),Line([-1,0,0],[1,0,0],color=HB,stroke_width=5)).move_to([0,-2.7,0])
        self.add(b)
        self.play(FadeIn(grasses),FadeIn(animals),FadeIn(crab),run_time=1.2)
        self.at("gentler daily swings")
        buoy=VGroup(Circle(radius=.32,color=YELLOW,fill_color=YELLOW,fill_opacity=.95),Line([0,-.3,0],[0,-1.2,0],color=YELLOW,stroke_width=5)).move_to([3.3,.85,0])
        self.play(FadeIn(buoy),run_time=.6)
        at=always_redraw(lambda: thermometer(5.5,2.05,air.get_value(),"air",.55))
        wt=always_redraw(lambda: thermometer(5.5,-1.55,wat.get_value(),"water",.55))
        self.add(at,wt)
        self.play(air.animate.set_value(.95),wat.animate.set_value(.6),run_time=1.0)
        self.play(air.animate.set_value(.1),wat.animate.set_value(.42),run_time=1.0)
        self.at("A buoy")
        self.play(Indicate(buoy,color=YELLOW,scale_factor=1.12),run_time=.9)
        self.at("measured both")
        self.play(air.animate.set_value(.82),wat.animate.set_value(.56),run_time=1.0)
        note=lbl("air and water temperature",[0,2.9,0],TEXT,32,BOLD)
        self.play(FadeIn(note),run_time=.5)
        self.finish()


class S14End(EndCard):
    LINE = "Each gram of water warms slowly; a whole bay, slower still."
