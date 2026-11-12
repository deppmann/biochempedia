"""A Tap, a Hole, a Level — organelles as environments.

COLOR MAP (fixed throughout)
  PROTON = red-orange dots; CALCIUM = TEAL; pumps/taps = GOLD;
  leaks/walls = GREY; cytosol reference = white dashed; chloroplast = GREEN.
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

PROTON = "#FF7043"
CALCIUM = TEAL
CELL_X = 2.55
LADDER_X = -5.25
CYTO_PH = 7.2


class FilmScene(SpokenScene):
    """A living compartment field: slow, continuous transport-scale motion."""
    FLOW_COLOR = PROTON

    def setup(self):
        super().setup()
        rng = np.random.default_rng(sum(map(ord, os.environ.get("KX_SCENE_ID", "scene"))))
        field = VGroup()
        for _ in range(96):
            d = Dot([rng.uniform(-6.8, 6.8), rng.uniform(-3.65, 3.65), 0],
                    radius=.06, color=self.FLOW_COLOR).set_opacity(.44)
            d.speed = rng.uniform(.72, .98)
            d.add_updater(lambda m, dt: m.shift(RIGHT * m.speed * dt) if m.get_x() < 6.9
                          else m.move_to([-6.8, m.get_y(), 0]))
            field.add(d)
        field.set_z_index(-20)
        self.add(field)


def arrow(a, b, color=GREY, width=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=0.22)


def ph_y(p):
    return -2.75 + (p - 4.0) * (5.5 / 4.5)


def proton(pos, r=0.075, opacity=1):
    return Dot(pos, radius=r, color=PROTON).set_opacity(opacity)


def calcium(pos, r=0.075, opacity=1):
    return Dot(pos, radius=r, color=CALCIUM).set_opacity(opacity)


def ladder(include_markers=False, compact=False):
    x = LADDER_X
    axis = Line([x, -2.75, 0], [x, 2.75, 0], color=GREY, stroke_width=4)
    title = T("pH", 30, TEXT, weight=BOLD).move_to([x, 3.15, 0])
    ticks = VGroup()
    labels = VGroup()
    for p in (4, 5, 6, 7, 8):
        y = ph_y(p)
        ticks.add(Line([x - .13, y, 0], [x + .13, y, 0], color=GREY, stroke_width=3))
        labels.add(M(str(p), 28, GREY).move_to([x - .48, y, 0]))
    cy = DashedLine([x - .75, ph_y(CYTO_PH), 0], [x + 4.0, ph_y(CYTO_PH), 0], color=TEXT, stroke_width=4)
    cyt = T("cytosol 7.2", 28, TEXT).move_to([x + 3.3, ph_y(CYTO_PH) + .34, 0])
    g = VGroup(axis, title, ticks, labels, cy, cyt)
    if include_markers:
        specs = [(4.7, "lysosome", PROTON), (5.5, "late endosome", PROTON),
                 (6.6, "Golgi", PROTON), (7.23, "nucleus", TEXT),
                 (7.9, "stroma", GREEN), (8.0, "matrix", BLUE)]
        compact_y = {"lysosome": -1.88, "late endosome": -1.02, "Golgi": -.12,
                     "nucleus": .72, "stroma": 2.05, "matrix": 2.6}
        for p, name, color in specs:
            d = Dot([x + .22, ph_y(p), 0], radius=.095, color=color)
            lab = T(name, 28, color).next_to(d, RIGHT, buff=.18)
            if compact:
                lab.move_to([x + 1.80, compact_y[name], 0])
            g.add(VGroup(d, lab))
    return g


def cell_world(full=True):
    cell = Ellipse(width=7.1, height=6.05, stroke_color=GREY, stroke_width=5,
                   fill_color=GREY, fill_opacity=.13).move_to([CELL_X, -.05, 0])
    lyso = Circle(radius=.68, color=PROTON, stroke_width=4, fill_color=PROTON,
                  fill_opacity=.12).move_to([1.45, 1.45, 0])
    golgi = VGroup(*[Arc(radius=.72 + .17 * i, start_angle=-1.15, angle=2.3,
                         color=PROTON, stroke_width=5) for i in range(3)]).move_to([3.25, 1.35, 0])
    er = VGroup(*[Arc(radius=.75 + .24 * i, start_angle=2.75, angle=2.75,
                      color=TEAL, stroke_width=5) for i in range(3)]).move_to([1.25, -.65, 0])
    nucleus = Circle(radius=1.0, color=TEXT, stroke_width=4, fill_color=TEXT,
                     fill_opacity=.035).move_to([3.45, -.55, 0])
    mito = RoundedRectangle(width=2.0, height=.92, corner_radius=.45, color=BLUE,
                            stroke_width=4, fill_color=BLUE, fill_opacity=.06).rotate(-.16).move_to([4.55, -2.05, 0])
    labels = VGroup(T("lysosome", 28, PROTON).next_to(lyso, DOWN, .12),
                    T("Golgi", 28, PROTON).next_to(golgi, RIGHT, .3),
                    T("ER", 28, TEAL).next_to(er, LEFT, .12),
                    T("nucleus", 28, TEXT).move_to(nucleus),
                    T("mitochondrion", 28, BLUE).move_to([4.95, -3.3, 0]))
    dots = VGroup(*[proton([x, y, 0], .045, .5) for x, y in
                    [(.2, 2.1), (2.5, 2.5), (4.8, 1.7), (5.1, -.2), (.25, -2.0), (2.2, -2.5)]])
    return VGroup(cell, lyso, golgi, er, nucleus, mito, labels, dots)


def marker(p, label, color=PROTON, side=RIGHT):
    d = Dot([LADDER_X + .2, ph_y(p), 0], radius=.12, color=color)
    t = T(label, 28, color).next_to(d, side, buff=.18)
    # Near-neutral labels live below the cytosol reference, never on top of it.
    if 6.55 <= p <= 7.35:
        t.move_to([LADDER_X + .5 + t.width / 2, ph_y(p) - .43, 0])
    return VGroup(d, t)


def container(level=.58, name="lysosome", color=PROTON, x=1.15):
    outline = RoundedRectangle(width=4.2, height=4.9, corner_radius=.28, color=GREY,
                               stroke_width=7, fill_color=GREY, fill_opacity=.13).move_to([x, -.2, 0])
    h = max(.04, 4.45 * level)
    fill = Rectangle(width=3.78, height=h, stroke_width=0, fill_color=color,
                     fill_opacity=.18).move_to([x, -2.42 + h / 2, 0])
    surface = Line([x - 1.85, -2.42 + h, 0], [x + 1.85, -2.42 + h, 0],
                   color=color, stroke_width=5)
    lab = T(name, 30, TEXT, weight=BOLD).move_to([x, 2.72, 0])
    return VGroup(fill, outline, surface, lab)


def tap_hole(x=1.15, tap_on=True, pump="V-ATPase (tap)"):
    tap = VGroup(Line([x - 1.45, 2.25, 0], [x - 1.45, 1.65, 0], color=GOLD, stroke_width=9),
                 Line([x - 1.78, 2.25, 0], [x - 1.12, 2.25, 0], color=GOLD, stroke_width=8))
    if not tap_on:
        tap.set_color(GREY)
    # Keep the top band clear for scene headings and place the name beside the tap.
    tl = T(pump, 28, GOLD if tap_on else GREY).move_to([x + .05, 1.55, 0])
    hole = Circle(radius=.16, color=GREY, fill_color=BG, fill_opacity=1,
                  stroke_width=5).move_to([x + 2.1, -1.55, 0])
    # The label sits below-left; all outflow arrows begin to the hole's right.
    hl = T("leak (hole)", 28, GREY).move_to([x + .75, -2.05, 0])
    return VGroup(tap, tl, hole, hl)


def stream(a, b, color=PROTON, n=5):
    return VGroup(*[Dot(interpolate(np.array(a), np.array(b), i / (n - 1)), radius=.075, color=color)
                    for i in range(n)])


class S00Hook(FilmScene):
    def construct(self):
        l = ladder()
        world = cell_world()
        self.play(Create(world[0]), FadeIn(l), run_time=.9)
        self.play(LaggedStart(*[FadeIn(m, scale=.8) for m in world[1:7]], lag_ratio=.08),
                  FadeIn(world[7]), run_time=1.0)
        self.at("a lysosome")
        lm = marker(4.7, "lysosome", PROTON)
        dense = VGroup(*[proton([1.45 + .38*np.cos(a), 1.45 + .38*np.sin(a), 0], .065)
                         for a in np.linspace(0, 2*np.pi, 8, endpoint=False)])
        self.play(Indicate(world[1], color=PROTON), FadeIn(lm), FadeIn(dense), run_time=.8)
        self.at("a mitochondrion")
        mm = marker(8.0, "matrix", BLUE)
        sparse = VGroup(proton([4.25, -2.0, 0], .055), proton([4.72, -2.08, 0], .055))
        self.play(Indicate(world[5], color=BLUE), FadeIn(mm), FadeIn(sparse), run_time=.8)
        self.at("Why does each settle")
        q = T("Why does each settle at its own number?", 34, TEXT, weight=BOLD).to_edge(UP, buff=.34)
        self.play(FadeIn(q, shift=DOWN*.15), lm.animate.shift(UP*.04), mm.animate.shift(DOWN*.04), run_time=.7)
        self.play(lm.animate.shift(DOWN*.04), mm.animate.shift(UP*.04), run_time=.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Organelles as environments"
    TITLE = "A Tap, a Hole, a Level"


class S02Ladder(FilmScene):
    def construct(self):
        l = ladder()
        world = cell_world()
        self.play(FadeIn(world), FadeIn(l), run_time=.8)
        self.at("Each marker")
        leads = VGroup()
        specs = [(4.7, "lysosome", PROTON), (8.0, "matrix", BLUE)]
        marks = VGroup()
        for p, name, col in specs:
            m = marker(p, name, col); marks.add(m)
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=.25), run_time=.8)
        self.at("white line")
        glow = DashedLine([LADDER_X-.8, ph_y(7.2), 0], [6.0, ph_y(7.2), 0], color=TEXT, stroke_width=7)
        self.play(ShowPassingFlash(glow, time_width=.5), run_time=1.0)
        self.at("Acid compartments")
        acid = Rectangle(width=1.6, height=ph_y(7.2)+2.75, stroke_width=0, fill_color=PROTON,
                         fill_opacity=.08).move_to([LADDER_X+.3, (-2.75+ph_y(7.2))/2, 0])
        new = VGroup(marker(6.6, "Golgi", PROTON), marker(5.5, "late endosome", PROTON))
        note = T("midpoint of 4.5 to 5.0", 28, PROTON).move_to([-3.65, -3.08, 0])
        self.play(FadeIn(acid), LaggedStart(*[FadeIn(m, shift=LEFT*.2) for m in new], lag_ratio=.3),
                  FadeIn(note), run_time=1.4)
        self.at("matrix")
        alkaline = Rectangle(width=1.6, height=2.75-ph_y(7.2), stroke_width=0, fill_color=BLUE,
                             fill_opacity=.08).move_to([LADDER_X+.3, (2.75+ph_y(7.2))/2, 0])
        tags = VGroup(T("acid", 28, PROTON).move_to([-6.4, -.55, 0]),
                      T("alkaline", 28, BLUE).move_to([-6.1, 2.62, 0]),
                      T("typical values, different systems", 28, GREY).move_to([-4.0, -3.35, 0]))
        self.play(FadeOut(note), FadeIn(alkaline), FadeIn(tags), Indicate(marks[1], color=BLUE), run_time=1.0)
        self.finish()


class S03Wall(FilmScene):
    def construct(self):
        ring = Circle(radius=2.35, color=GREY, stroke_width=12, fill_color=PROTON,
                      fill_opacity=.07).move_to([1.1, 0, 0])
        inside = VGroup(*[proton([1.1+1.25*np.cos(a), .9*np.sin(a), 0]) for a in np.linspace(0, 2*np.pi, 11, endpoint=False)])
        dim = VGroup(ladder().set_opacity(.28), T("cytosol", 30, TEXT).move_to([5.1, 2.6, 0]))
        self.add(dim, ring, inside)
        self.play(Indicate(ring, color=GREY, scale_factor=1.02), run_time=.9)
        self.at("A membrane")
        wall = T("membrane", 30, GREY).next_to(ring, UP, .22)
        self.play(FadeIn(wall), Indicate(ring, color=TEXT), run_time=.8)
        self.at("slowly")
        paths = [Line([2.9, .8-i*.7, 0], [5.2, .8-i*.7, 0]) for i in range(3)]
        moving = VGroup(*[proton(p.get_start()) for p in paths])
        self.add(moving)
        self.play(*[MoveAlongPath(d, p) for d,p in zip(moving, paths)], run_time=2.2, rate_func=linear)
        self.at("Protons trickle")
        leak = T("leaky wall", 28, GREY).move_to([3.85, -2.45, 0])
        more = proton([2.9, -.95, 0])
        self.add(more)
        self.play(FadeIn(leak), MoveAlongPath(more, Line([2.9,-.95,0],[5.2,-.95,0])), run_time=1.7, rate_func=linear)
        self.finish()


class S04Tap(FilmScene):
    def construct(self):
        l = ladder(); c = container(.02); th = tap_hole()
        reset = marker(7.2, "lysosome", PROTON)
        self.add(l, c, reset)
        self.play(Indicate(c[1], color=GREY, scale_factor=1.01), run_time=1.0)
        self.at("tap and a hole")
        self.play(FadeIn(th[0]), FadeIn(th[2:]), run_time=.7)
        self.at("proton pump")
        self.play(FadeIn(th[1]), Indicate(th[0], color=GOLD), run_time=.7)
        self.at("spending")
        atp = chip("ATP", GOLD, 28).move_to([-1.78, 2.72, 0])
        self.play(FadeIn(atp, scale=.8), run_time=.6)
        self.at("push protons in")
        s = stream([-.3,1.65,0],[-.3,-.2,0],PROTON,6)
        pump_arrow = arrow([-.3,1.7,0],[-.3,.2,0],GOLD,7)
        self.play(GrowArrow(pump_arrow), LaggedStart(*[FadeIn(d, shift=DOWN*.2) for d in s], lag_ratio=.12), run_time=1.5)
        self.finish()


class S05Fill(Scene):
    def construct(self):
        l = ladder(); c = container(.02); th = tap_hole(); m = marker(7.2,"lysosome",PROTON)
        self.add(l,c,th,m)
        high = container(.65)
        out = arrow([3.50,-1.55,0],[5.2,-1.55,0],GREY,7)
        tag = T("schematic", 28, GREY).move_to([5.65,-3.3,0])
        target = marker(5.5,"lysosome",PROTON)
        self.play(Transform(c,high), Transform(m,target), GrowArrow(out), FadeIn(tag), run_time=3.4, rate_func=smooth)
        self.wait(.1)


class S06Settle(FilmScene):
    def construct(self):
        l=ladder(); c=container(.65); th=tap_hole(); m=marker(5.5,"lysosome",PROTON)
        inflow=arrow([-.3,1.8,0],[-.3,.35,0],GOLD,7)
        out=arrow([3.50,-1.55,0],[4.55,-1.55,0],GREY,7)
        self.add(l,c,th,m,inflow,out)
        self.at("more leak back")
        out2=arrow([3.50,-1.55,0],[5.45,-1.55,0],GREY,7)
        self.play(Transform(out,out2), c[2].animate.shift(UP*.35), m.animate.shift(DOWN*.4), run_time=1.3)
        self.at("some level")
        eq=T("in  =  out",30,TEXT,weight=BOLD).move_to([4.85,.25,0])
        self.play(FadeIn(eq), Indicate(inflow,color=GOLD), Indicate(out,color=TEXT), run_time=1.0)
        self.at("level stops rising")
        curve=VMobject(color=PROTON,stroke_width=5)
        pts=[]
        for t in np.linspace(0,4,40): pts.append([3.9+t*.55,-3.0+1.0*(1-np.exp(-t)),0])
        curve.set_points_smoothly(pts)
        axes=VGroup(Line([3.75,-3.05,0],[6.3,-3.05,0],color=GREY),Line([3.75,-3.05,0],[3.75,-1.75,0],color=GREY))
        qtag=T("qualitative toy model",28,GREY).move_to([4.4,-3.35,0])
        self.play(Create(axes), Create(curve), FadeIn(qtag), run_time=1.6)
        self.at("no sensor")
        nosensor=T("no sensor\nneeded",30,GREEN,weight=BOLD,line_spacing=.85).move_to([5.1,1.1,0])
        self.play(ReplacementTransform(eq,nosensor), c[2].animate.shift(UP*.05), run_time=.8)
        self.play(c[2].animate.shift(DOWN*.05), run_time=.8)
        self.finish()


class S07Rule(FilmScene):
    def construct(self):
        l=ladder(); c=container(.65); th=tap_hole(); m=marker(5.5,"lysosome",PROTON)
        self.add(l,c,th,m)
        self.at("The level sits")
        rule=T("level = where pumping in meets leaking out",31,TEXT,weight=BOLD).to_edge(UP,.34)
        self.play(FadeIn(rule), run_time=.8)
        self.at("stronger pump")
        strong=Line([-.3,2.25,0],[-.3,.1,0],color=GOLD,stroke_width=13)
        hi=container(.82); lowm=marker(4.9,"more acid",PROTON)
        self.play(Create(strong),Transform(c,hi),Transform(m,lowm),run_time=1.8)
        self.at("leakier wall")
        wide=Circle(.28,color=GREY,fill_color=BG,fill_opacity=1,stroke_width=6).move_to([3.25,-1.55,0])
        lo=container(.42); highm=marker(6.2,"less acid",PROTON)
        self.play(FadeOut(strong),FadeIn(wide),Transform(c,lo),Transform(m,highm),run_time=1.8)
        baseline=container(.65); basem=marker(5.5,"lysosome",PROTON)
        self.play(FadeOut(wide),Transform(c,baseline),Transform(m,basem),run_time=1.1)
        self.finish()


def predict_frame():
    l=ladder(); c=container(.65); th=tap_hole(tap_on=False); m=marker(5.5,"lysosome",PROTON)
    clamp=chip("bafilomycin",RED,28).move_to([-2.15,2.62,0])
    cross=VGroup(Line([-.62,1.88,0],[.02,2.52,0],color=RED,stroke_width=8),Line([-.62,2.52,0],[.02,1.88,0],color=RED,stroke_width=8))
    q=T("Tap off: which way does the marker go?",32,TEXT,weight=BOLD).to_edge(UP,.34)
    arrows=VGroup(arrow([-2.9,ph_y(5.5),0],[-2.9,ph_y(6.25),0],TEXT),arrow([-2.5,ph_y(5.5),0],[-2.5,ph_y(4.75),0],TEXT))
    return VGroup(l,c,th,m,clamp,cross,q,arrows)


class S08Predict(FilmScene):
    def construct(self):
        l=ladder(); c=container(.65); th=tap_hole(); m=marker(5.5,"lysosome",PROTON)
        self.add(l,c,th,m)
        self.at("a drug")
        clamp=chip("bafilomycin",RED,28).move_to([-2.15,2.62,0])
        self.play(FadeIn(clamp,shift=RIGHT*.2),run_time=.7)
        self.at("tap shut")
        cross=VGroup(Line([-.62,1.88,0],[.02,2.52,0],color=RED,stroke_width=8),Line([-.62,2.52,0],[.02,1.88,0],color=RED,stroke_width=8))
        self.play(FadeIn(cross),th[0:2].animate.set_opacity(.35),run_time=.7)
        self.at("Watch")
        self.play(Indicate(m,color=TEXT),c[2].animate.shift(UP*.05),run_time=.8)
        self.at("Which way")
        q=T("Tap off: which way does the marker go?",32,TEXT,weight=BOLD).to_edge(UP,.34)
        arrs=VGroup(arrow([-2.9,ph_y(5.5),0],[-2.9,ph_y(6.25),0],TEXT),arrow([-2.5,ph_y(5.5),0],[-2.5,ph_y(4.75),0],TEXT))
        self.play(FadeIn(q),GrowArrow(arrs[0]),GrowArrow(arrs[1]),run_time=1.0)
        self.play(c[2].animate.shift(DOWN*.05),m.animate.scale(1.12),run_time=.8)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        f=predict_frame(); self.add(f)
        for _ in range(3):
            self.play(f[3].animate.scale(1.1),f[1][2].animate.shift(UP*.035),run_time=.7)
            self.play(f[3].animate.scale(1/1.1),f[1][2].animate.shift(DOWN*.035),run_time=.7)
        self.wait(.3)


class S10Reveal(FilmScene):
    def construct(self):
        l=ladder(); c=container(.65); th=tap_hole(tap_on=False); m=marker(5.5,"lysosome",PROTON)
        self.add(l,c,th,m)
        self.at("Up toward")
        low=container(.28); up=marker(6.7,"less acid",PROTON)
        out=arrow([3.50,-1.55,0],[5.25,-1.55,0],GREY,7)
        self.play(GrowArrow(out),Transform(c,low),Transform(m,up),run_time=1.7)
        self.at("hole keeps draining")
        short=arrow([3.50,-1.55,0],[4.25,-1.55,0],GREY,7)
        self.play(Transform(out,short),c[2].animate.shift(DOWN*.15),run_time=1.2)
        self.at("In Hila cells")
        gol=RoundedRectangle(width=2.0,height=2.25,corner_radius=.2,color=GREY,stroke_width=5,fill_color=PROTON,fill_opacity=.1).move_to([4.9,.75,0])
        gl=T("HeLa cells\nGolgi less acid",28,PROTON,line_spacing=.85).next_to(gol,DOWN,.32)
        clamp=T("tap off",28,RED).move_to([4.9,2.20,0])
        self.play(FadeOut(out),FadeIn(gol),FadeIn(gl),FadeIn(clamp),run_time=1.0)
        self.at("actively kept")
        kept=T("acidity is actively kept",31,GREEN,weight=BOLD).to_edge(UP,.34)
        base=container(.65); basem=marker(5.5,"lysosome",PROTON)
        self.play(FadeIn(kept),Transform(c,base),Transform(m,basem),th[0].animate.set_color(GOLD),th[1].animate.set_color(GOLD),run_time=1.4)
        self.finish()


class S11Golgi(FilmScene):
    def construct(self):
        l=ladder(); self.add(l)
        a=container(.72,"lysosome",PROTON,x=.2).scale(.72).shift(DOWN*.2)
        b=container(.48,"Golgi",PROTON,x=4.2).scale(.72).shift(DOWN*.2)
        pumps=VGroup(T("pump",28,GOLD).move_to([-.6,2.6,0]),T("pump",28,GOLD).move_to([3.4,2.6,0]))
        holes=VGroup(T("leak",28,GREY).move_to([.2,-2.55,0]),T("leak",28,GREY).move_to([4.2,-2.55,0]))
        ms=VGroup(marker(4.7,"lysosome",PROTON),marker(6.6,"Golgi",PROTON))
        self.play(FadeIn(a),FadeIn(b),FadeIn(pumps),FadeIn(holes),LaggedStart(*[FadeIn(x) for x in ms]),run_time=1.2)
        self.at("same pump family")
        self.play(Indicate(pumps[0],color=GOLD),Indicate(pumps[1],color=GOLD),run_time=.9)
        self.at("more pumps")
        ghost=T("pump?",28,GOLD).set_opacity(.45).next_to(pumps[0],RIGHT,.15)
        self.play(FadeIn(ghost),run_time=.7); self.play(FadeOut(ghost),run_time=.4)
        self.at("tighter wall")
        tight=T("smaller leak?",28,GREY).move_to([.2,-2.55,0])
        self.play(FadeOut(holes[0]),FadeIn(tight),run_time=.7)
        self.play(FadeOut(tight),FadeIn(holes[0]),run_time=.4)
        self.at("something else")
        q=T("?",60,TEXT,weight=BOLD).move_to([2.2,.15,0])
        self.play(FadeIn(q,scale=1.4),run_time=.7)
        self.at("still being worked out")
        note=T("which differs? still studied",28,TEXT).to_edge(UP,.34)
        tag=T("icons are not quantitative",28,GREY).to_edge(DOWN,.34)
        self.play(ReplacementTransform(q,note),FadeIn(tag),a[2].animate.shift(UP*.04),b[2].animate.shift(UP*.04),run_time=.9)
        self.finish()


class S12Nucleus(FilmScene):
    def construct(self):
        l=ladder(); world=cell_world(); self.play(FadeIn(l),FadeIn(world),run_time=.8)
        self.at("nucleus is different")
        self.play(world[1:5].animate.set_opacity(.2),Indicate(world[4],color=TEXT),run_time=.8)
        self.at("full of pores")
        nuc=world[4]; pores=VGroup(*[Dot(nuc.get_center()+1.0*np.array([np.cos(a),np.sin(a),0]),radius=.09,color=BG) for a in np.linspace(0,2*np.pi,12,endpoint=False)])
        self.play(FadeIn(pores),run_time=.8)
        self.at("pass through them quickly")
        paths=[Line([2.1,y,0],[4.75,y,0]) for y in (-1.0,-.55,-.1)]
        ions=VGroup(*[proton(p.get_start()) for p in paths])
        self.add(ions); self.play(*[MoveAlongPath(d,p) for d,p in zip(ions,paths)],run_time=1.5,rate_func=linear)
        rev=VGroup(*[proton(p.get_end()) for p in paths]); self.add(rev)
        self.play(*[MoveAlongPath(d,p.copy().reverse_points()) for d,p in zip(rev,paths)],run_time=1.4,rate_func=linear)
        self.at("stays close")
        nm=marker(7.23,"nucleus: near 7.2",TEXT)
        self.play(FadeIn(nm),Indicate(l[4],color=TEXT),run_time=.9)
        self.finish()


def calcium_gauge(er=.88, cy=.12):
    x=LADDER_X; axis=Line([x,-2.5,0],[x,2.45,0],color=CALCIUM,stroke_width=5)
    title=T("free calcium",28,CALCIUM,weight=BOLD).move_to([x,2.9,0])
    erd=Dot([x, -2.5+4.95*er,0],radius=.12,color=CALCIUM); ert=T("ER",28,CALCIUM).next_to(erd,RIGHT,.15)
    cyd=Dot([x, -2.5+4.95*cy,0],radius=.12,color=TEXT); cyt=T("cytosol",28,TEXT).next_to(cyd,RIGHT,.15)
    if abs(er-cy) < .15:
        sign = 1 if er > cy else -1
        ert.shift(UP * .28 * sign)
        cyt.shift(DOWN * .28 * sign)
    log=T("log scale",28,GREY).move_to([x,-2.9,0])
    return VGroup(axis,title,VGroup(erd,ert),VGroup(cyd,cyt),log)


class S13Calcium(FilmScene):
    FLOW_COLOR = CALCIUM
    def construct(self):
        g=calcium_gauge(.2,.12); c=container(.05,"ER",CALCIUM); c[1].set_color(CALCIUM)
        self.play(FadeIn(g),FadeIn(c),run_time=.8)
        self.at("calcium pump")
        th=tap_hole(pump="SERCA (tap)"); self.play(FadeIn(th),run_time=.8)
        self.at("SERCA fills")
        high=container(.82,"ER",CALCIUM); high[1].set_color(CALCIUM)
        s=stream([-.3,1.7,0],[-.3,-.1,0],CALCIUM,7)
        self.play(LaggedStart(*[FadeIn(d,shift=DOWN*.25) for d in s],lag_ratio=.1),Transform(c,high),Transform(g,calcium_gauge(.88,.12)),run_time=2.0)
        self.at("thousands of times")
        lab=T("thousands of\ntimes higher",29,CALCIUM,weight=BOLD,line_spacing=.85).move_to([-3.35,.3,0])
        self.play(FadeIn(lab),Indicate(g[2],color=CALCIUM),run_time=.9)
        self.at("leaks and release channels")
        out=arrow([3.50,-1.55,0],[5.35,-1.55,0],GREY,7); tag=T("schematic",28,GREY).move_to([5.65,-3.25,0])
        self.play(GrowArrow(out),FadeIn(tag),c[2].animate.shift(DOWN*.05),run_time=1.2)
        self.finish()


class S14Thaps(FilmScene):
    FLOW_COLOR = CALCIUM
    def construct(self):
        g=calcium_gauge(.88,.12); c=container(.82,"ER",CALCIUM); c[1].set_color(CALCIUM); th=tap_hole(pump="SERCA (tap)")
        self.add(g,c,th)
        self.at("plant compound")
        block=chip("thapsigargin",RED,28).move_to([-2.5,2.62,0]); self.play(FadeIn(block),run_time=.7)
        self.at("blocks SERCA")
        x=VGroup(Line([-.8,1.6,0],[0,2.4,0],color=RED,stroke_width=8),Line([-.8,2.4,0],[0,1.6,0],color=RED,stroke_width=8))
        self.play(FadeIn(x),th[0:2].animate.set_opacity(.3),run_time=.8)
        self.at("keeps leaking out")
        out=arrow([3.50,-1.55,0],[5.4,-1.55,0],GREY,7); self.play(FadeOut(block),GrowArrow(out),run_time=1.0)
        self.at("store runs down")
        low=container(.25,"ER",CALCIUM); low[1].set_color(CALCIUM)
        extras=VGroup(*[calcium([4.0+.35*i,-1.9+.2*(i%2),0]) for i in range(6)])
        self.play(Transform(c,low),Transform(g,calcium_gauge(.28,.35)),FadeIn(extras),run_time=1.8)
        self.at("rises for a while")
        self.play(extras.animate.shift(UP*.25).set_opacity(.15),Transform(g,calcium_gauge(.25,.18)),run_time=1.2)
        self.play(FadeOut(g),FadeIn(ladder()),FadeOut(extras),run_time=.9)
        self.finish()


def mito_container():
    outer=RoundedRectangle(width=5.3,height=3.6,corner_radius=1.5,color=GREY,stroke_width=5).move_to([1.25,-.15,0])
    inner=RoundedRectangle(width=4.45,height=2.75,corner_radius=1.2,color=BLUE,stroke_width=6,fill_color=BLUE,fill_opacity=.04).move_to(outer)
    lab=T("matrix",30,BLUE,weight=BOLD).move_to([1.25,-.15,0])
    return VGroup(outer,inner,lab)


class S15Flip(FilmScene):
    def construct(self):
        l=ladder(); mito=mito_container(); self.play(FadeIn(l),FadeIn(mito),run_time=.8)
        self.at("other way")
        mini=T("lysosome: pump in   •   mitochondrion: pump out",28,TEXT,weight=BOLD).to_edge(UP,.34)
        self.play(FadeIn(mini),run_time=.9)
        self.at("respiratory chain")
        pumps=T("respiratory chain (taps)",28,GOLD).move_to([1.25,2.95,0]); resp=T("while respiring",28,GREY).next_to(pumps,DOWN,.12)
        self.play(FadeIn(pumps),FadeIn(resp),run_time=.8)
        self.at("push protons out")
        paths=[Line([x,.6,0],[x,2.0,0]) for x in (.0,.8,1.6,2.4)]
        ds=VGroup(*[proton(p.get_start()) for p in paths]); self.add(ds)
        self.play(*[MoveAlongPath(d,p) for d,p in zip(ds,paths)],run_time=1.5,rate_func=linear)
        self.at("matrix sits above")
        mm=marker(8.0,"matrix 8",BLUE); leak=arrow([3.5,1.0,0],[3.5,.25,0],GREY,5)
        self.play(FadeIn(mm),GrowArrow(leak),mito[2].animate.scale(1.08),run_time=1.0)
        self.finish()


class S16Why(FilmScene):
    def construct(self):
        mito=mito_container(); self.add(mito)
        self.at("other way")
        q=T("Why outward?",36,TEXT,weight=BOLD).to_edge(UP,.34); self.play(FadeIn(q),run_time=.7)
        self.at("matrix was")
        bact=RoundedRectangle(width=5.0,height=2.55,corner_radius=1.2,color=BLUE,stroke_width=6,fill_color=BLUE,fill_opacity=.05).move_to([1.25,-.15,0])
        bl=T("free-living bacterium, long ago",28,BLUE).next_to(bact,DOWN,.25); cy=T("cytoplasm",30,TEXT).move_to(bact)
        self.play(FadeOut(mito[0]),Transform(mito[1],bact),ReplacementTransform(mito[2],cy),FadeIn(bl),run_time=1.5)
        self.at("during respiration")
        pumps=T("electron-transport chain",28,GOLD).move_to([1.25,1.95,0]); self.play(FadeIn(pumps),run_time=.7)
        self.at("pumped protons outward")
        paths=[Line([x,.4,0],[x,1.55,0]) for x in (0,.8,1.6,2.4)]
        dots=VGroup(*[proton(p.get_start()) for p in paths]); self.add(dots)
        host=Ellipse(width=9.0,height=6.6,color=GREY,stroke_width=4).move_to([1.25,-.1,0])
        self.play(*[MoveAlongPath(d,p) for d,p in zip(dots,paths)],Create(host),run_time=1.5,rate_func=linear)
        matrix=T("matrix",30,BLUE).move_to(bact); tag=T("cartoon",28,GREY).to_edge(DOWN,.34)
        self.play(ReplacementTransform(cy,matrix),FadeIn(tag),FadeOut(bl),run_time=.8)
        self.finish()


class S17Chloro(FilmScene):
    def construct(self):
        l=ladder(); mito=mito_container().scale(.55).move_to([2.6,1.55,0]); mito[2].scale(1/.55); self.add(l,mito)
        self.at("Chloroplasts")
        chl=RoundedRectangle(width=4.8,height=2.3,corner_radius=.8,color=GREEN,stroke_width=6,fill_color=GREEN,fill_opacity=.04).move_to([2.6,-1.65,0])
        stacks=VGroup(*[VGroup(*[Line([x-.35,y,0],[x+.35,y,0],color=GREEN,stroke_width=5) for y in (-1.95,-1.65,-1.35)]) for x in (1.5,2.6,3.7)])
        self.play(FadeIn(chl),FadeIn(stacks),run_time=1.0)
        self.at("stroma")
        st=T("stroma",30,GREEN,weight=BOLD).move_to([2.6,-2.45,0]); self.play(FadeIn(st),run_time=.7)
        self.at("in light")
        lamp=VGroup(Circle(.28,color=YELLOW,fill_color=YELLOW,fill_opacity=.7),*[Line(.42*np.array([np.cos(a),np.sin(a),0]),.7*np.array([np.cos(a),np.sin(a),0]),color=YELLOW,stroke_width=4) for a in np.linspace(0,2*np.pi,8,endpoint=False)]).move_to([5.65,-.65,0])
        self.play(FadeIn(lamp,scale=.7),run_time=.7)
        sm=marker(7.9,"stroma, in light",GREEN)
        paths=[Line([x,-1.65,0],[x,-1.3,0]) for x in (1.5,2.6,3.7)]
        ds=VGroup(*[proton(p.get_start()) for p in paths]); self.add(ds)
        self.play(*[MoveAlongPath(d,p) for d,p in zip(ds,paths)],FadeIn(sm),run_time=1.2)
        self.at("Every proton pump")
        panels=VGroup()
        for x, title, color, direction in ((-4.15,"lysosome",PROTON,DOWN),
                                           (0,"mitochondrion",BLUE,UP),
                                           (4.15,"chloroplast",GREEN,UP)):
            bucket=RoundedRectangle(width=3.55,height=4.55,corner_radius=.3,color=color,
                                    stroke_width=6,fill_color=color,fill_opacity=.055).move_to([x,-.25,0])
            heading=T(title,30,color,weight=BOLD).move_to([x,2.55,0])
            source=T("source:\na cytoplasm",28,TEXT,line_spacing=.8).move_to([x-.35,.25,0])
            y1,y2=(1.55,-1.35) if direction is DOWN else (-1.35,1.55)
            flow=arrow([x+1.15,y1,0],[x+1.15,y2,0],GOLD,8)
            panels.add(VGroup(bucket,heading,source,flow))
        source_rule=T("Every pump pushes out of a cytoplasm",32,TEXT,weight=BOLD).to_edge(UP,.34)
        self.play(FadeOut(l),FadeOut(mito),FadeOut(chl),FadeOut(stacks),FadeOut(st),
                  FadeOut(lamp),FadeOut(ds),FadeOut(sm),FadeIn(panels),FadeIn(source_rule),run_time=1.2)
        self.finish()


class S18Return(FilmScene):
    def construct(self):
        l=ladder(True,True); world=cell_world(); tag=T("typical values, different systems",28,GREY).move_to([-4.0,-3.35,0])
        self.play(FadeIn(l),FadeIn(world),FadeIn(tag),run_time=1.0)
        self.at("ongoing energy")
        taps=VGroup(*[Dot(p,radius=.13,color=GOLD) for p in ([1.1,1.45,0],[3.0,1.35,0],[3.55,1.35,0],[4.2,-2.05,0])])
        chl=RoundedRectangle(width=1.45,height=.6,corner_radius=.25,color=GREEN,stroke_width=4).move_to([.75,-2.25,0])
        ctap=Dot([.75,-2.25,0],radius=.13,color=GOLD)
        self.play(FadeIn(taps),FadeIn(chl),FadeIn(ctap),run_time=1.0)
        self.at("Acid lumens need")
        v=T("V-ATPase",28,GOLD).move_to([5.6,3.15,0]); self.play(FadeIn(v),Indicate(taps[0:3],color=GOLD),run_time=.9)
        self.at("respiration or light")
        rl=T("respiration   •   light",28,GOLD).move_to([2.0,3.4,0]); self.play(FadeIn(rl),Indicate(taps[3],color=GOLD),Indicate(ctap,color=GOLD),run_time=.9)
        self.at("Stop that input")
        off=T("input off",30,RED,weight=BOLD).to_edge(UP,.34).set_x(-3.0)
        self.play(FadeOut(v),FadeOut(rl),FadeIn(off),taps.animate.set_opacity(.15),ctap.animate.set_opacity(.15),run_time=.9)
        self.at("gradients run down")
        moved=ladder(False)
        drift=VGroup(marker(5.55,"lysosome →",PROTON),marker(6.25,"endosome →",PROTON),marker(6.9,"Golgi →",PROTON),marker(7.55,"← stroma",GREEN),marker(7.62,"← matrix",BLUE))
        drift[1][1].move_to([-3.82,-.15,0])
        drift[2][1].move_to([-4.05,.52,0])
        drift[3][1].move_to([-4.00,1.62,0])
        drift[4][1].move_to([-4.00,2.28,0])
        down=T("gradients run down",31,RED,weight=BOLD).move_to([2.6,3.5,0])
        self.play(FadeOut(l),FadeOut(off),FadeIn(moved),FadeIn(drift),FadeIn(down),run_time=1.8)
        self.play(world[0].animate.scale(1.01),run_time=.8)
        self.play(world[0].animate.scale(1/1.01),run_time=.8)
        self.finish()


class S19End(EndCard):
    LINE = "Each compartment's chemistry sits where pumping in meets leaking out."

