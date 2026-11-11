"""Same Brick, Different Snap.

COLOR MAP
  GOLD   anomeric carbon and glycosidic bond
  TEAL   carbon six
  BLUE   alpha, helices, starch/glycogen and fuel
  GREEN  beta, ribbons, cellulose and fiber
  RED    cannot / mismatch
  PURPLE enzymes and microbes
  TEXT   glucose tiles and neutral labels

Glucose is represented only by labelled tiles/cards.  No molecular structure is drawn.
Angles, pitch and three-dimensional cartoons are explicitly marked schematic.
"""
from bp_style import *  # noqa: F401,F403
import math

PURPLE = "#B58CE0"
TRACK_Y = 0.0


# --------------------------------------------------------------------- shared world
def track(y=TRACK_Y, color=GOLD, opacity=0.32):
    # A filled guide band reads as the shared assembly track without drawing a
    # line through the labels on the tiles that sit on it.
    return RoundedRectangle(corner_radius=.16, width=12.4, height=1.35,
                            stroke_width=0, fill_color=color,
                            fill_opacity=opacity * .22).move_to([0, y, 0]).set_z_index(-20)


def glucose_tile(scale=1.0, outline=TEXT, c6_up=True, flag=None):
    """A standard glucose tile: C6 tab, C1 gold pin, and carbon-4 port."""
    body = RoundedRectangle(corner_radius=0.16, width=1.3, height=1.3,
                            stroke_color=outline, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.15)
    word = T("glucose", 28, TEXT).scale(0.72)
    sy = 1 if c6_up else -1
    tab = RoundedRectangle(corner_radius=0.06, width=0.55, height=0.28,
                           stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.25,
                           stroke_width=2).move_to([0, sy * 0.65, 0])
    c6 = M("C6", 22, TEAL).scale(0.72).move_to(tab)
    pin = Dot([0.65, 0, 0], radius=0.105, color=GOLD)
    port = Circle(radius=0.13, stroke_color=TEXT, stroke_width=2).move_to([-0.65, 0, 0])
    four = M("4", 22, TEXT).scale(0.72).move_to(port)
    if scale < .6:
        # At bead scale these are repeated icons, not readable teaching labels.
        # Hiding their microtype also keeps rods and links from crossing text.
        word.set_opacity(0)
        c6.set_opacity(0)
        four.set_opacity(0)
    g = VGroup(body, word, tab, c6, pin, port, four)
    g.body, g.tab, g.pin, g.port = body, VGroup(tab, c6), pin, VGroup(port, four)
    if flag:
        fy = 1 if flag == "up" else -1
        stalk = Line([0.65, 0, 0], [0.92, fy * 0.52, 0], color=GOLD, stroke_width=4)
        oh = chip("OH", GOLD, size=24, pad=0.10).scale(0.72).move_to([1.03, fy * 0.72, 0])
        g.add(stalk, oh)
        g.flag = VGroup(stalk, oh)
    g.scale(scale)
    return g


def bob(mob, amplitude=0.04, period=3.0, phase=0.0):
    base = mob.get_y()
    clock = {"t": 0.0}
    def update(m, dt):
        clock["t"] += dt
        m.set_y(base + amplitude * math.sin(TAU * clock["t"] / period + phase))
    mob.add_updater(update)
    return mob


def joint_between(left, right, color=GOLD, width=8):
    return Line(left.get_right(), right.get_left(), color=color, stroke_width=width).set_z_index(-1)


def bread(center=(-3.7, 0.2, 0), scale=1.0):
    crust = RoundedRectangle(corner_radius=0.65, width=4.0, height=4.5,
                             stroke_color=BLUE, stroke_width=5,
                             fill_color=BLUE, fill_opacity=0.08)
    top = Arc(radius=1.0, start_angle=0, angle=PI, color=BLUE, stroke_width=5).stretch(1.75, 0).stretch(.65, 1).shift(UP * 2.0)
    pores = VGroup(*[Circle(radius=.12, color=BLUE, fill_color=BLUE, fill_opacity=.2)
                     .move_to(p) for p in [(-.9,.8,0),(.7,1.1,0),(-.3,-.4,0),(.8,-1.1,0),(-1.0,-1.3,0)]])
    label = T("bread", 32, BLUE).move_to([0, -1.75, 0])
    return VGroup(crust, top, pores, label).scale(scale).move_to(center)


def plank(center=(3.7, 0.2, 0), scale=1.0):
    box = RoundedRectangle(corner_radius=.12, width=4.0, height=4.5,
                           stroke_color=GREEN, stroke_width=5,
                           fill_color=GREEN, fill_opacity=.07)
    grain = VGroup(*[Arc(radius=1.0, start_angle=.1, angle=PI*.8,
                         color=GREEN, stroke_width=3).stretch(1.4, 0).stretch(.35, 1).move_to([0, y, 0])
                     for y in [-1.0, 0.1, 1.2]])
    label = T("wood", 32, GREEN).move_to([0, -1.75, 0])
    return VGroup(box, grain, label).scale(scale).move_to(center)


def gut_tube(width=4.0):
    path = VMobject(color=PURPLE, stroke_width=11)
    path.set_points_smoothly([[-width/2, .35, 0], [-1.2, -.25, 0], [-.4, .25, 0],
                              [.35, -.3, 0], [1.1, .25, 0], [width/2, -.25, 0]])
    return path


def schematic(pos=(5.15, -3.35, 0)):
    return T("schematic", 28, TEXT).set_opacity(.9).move_to(pos)


def lock_icon(pos):
    shackle = Arc(radius=.22, start_angle=0, angle=PI, color=GOLD, stroke_width=5).shift(UP*.16)
    body = RoundedRectangle(corner_radius=.05, width=.55, height=.45,
                            stroke_color=GOLD, fill_color=GOLD, fill_opacity=.2, stroke_width=3).shift(DOWN*.13)
    return VGroup(shackle, body).move_to(pos)


def helix_curve(color=BLUE, y=0.0, turns=2.0, width=10.0, amp=1.25):
    # The displayed curve follows the script's x=.35t, y=1.1 cos(2πt/6), rescaled to the frame.
    ts = np.linspace(0, 6 * turns, 240)
    xs = -width/2 + width * ts / (6 * turns)
    ys = y + amp * np.cos(TAU * ts / 6)
    pts = np.column_stack([xs, ys, np.zeros_like(xs)])
    v = VMobject(color=color, stroke_width=8)
    v.set_points_smoothly(pts)
    return v


def ribbon(y=0, width=10.8, color=GREEN):
    return RoundedRectangle(corner_radius=.18, width=width, height=.72,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=.20).move_to([0, y, 0])


def granule(radius=1.5, label="starch granule", center=ORIGIN):
    blob = Circle(radius=radius, stroke_color=BLUE, stroke_width=5,
                  fill_color=BLUE, fill_opacity=.15)
    arcs = VGroup(*[Arc(radius=radius*(.35+.16*i), start_angle=i*.7, angle=PI*1.4,
                        color=BLUE, stroke_width=3) for i in range(4)])
    lab = T(label, 30, BLUE).move_to([0, -radius-.35, 0])
    return VGroup(blob, arcs, lab).move_to(center)


class FilmScene(SpokenScene):
    """The carried assembly track, with slow belt motion during every sentence."""
    def setup(self):
        super().setup()
        belt = RoundedRectangle(corner_radius=.16, width=12.6, height=1.35,
                                stroke_width=0, fill_color=GREY,
                                fill_opacity=.17).set_z_index(-20)
        belt.add_updater(lambda m, dt: m.set_fill(
            GREY, opacity=.17 + .07 * math.sin(TAU * self.renderer.time / 2.4)))
        self.add(belt)


# -------------------------------------------------------------------------- scenes
class S00Hook(FilmScene):
    def construct(self):
        tr = track()
        br, wood = bread(), plank()
        self.add(tr, br, wood)
        # The aligner glued its first two tokens as "Starchin"; "bread and" is the
        # first exact transcript phrase and still leads the first visual beat.
        self.at("bread and")
        starch = ribbon(-.15, 3.6, BLUE).scale(.35).move_to([-3.7, .45, 0])
        sl = T("starch", 30, BLUE).next_to(starch, UP, buff=.15)
        self.play(GrowFromEdge(starch, LEFT), FadeIn(sl), br.animate.set_opacity(.4), run_time=1.0)
        self.at("cellulose in wood")
        cellu = ribbon(-.15, 3.6, GREEN).scale(.35).move_to([3.7, .45, 0])
        cl = T("cellulose", 30, GREEN).next_to(cellu, UP, buff=.15)
        self.play(GrowFromEdge(cellu, RIGHT), FadeIn(cl), wood.animate.set_opacity(.4), run_time=1.0)
        self.at("both pure glucose")
        left = VGroup(*[glucose_tile(.72).move_to([-4.5+i*1.15, 0, 0]) for i in range(3)])
        right = VGroup(*[glucose_tile(.72).move_to([2.2+i*1.15, 0, 0]) for i in range(3)])
        self.play(FadeOut(starch), FadeOut(cellu), FadeOut(sl), FadeOut(cl),
                  LaggedStart(*[FadeIn(t, shift=DOWN*.25) for t in [*left, *right]], lag_ratio=.12), run_time=1.2)
        self.at("why do you digest one")
        gut = gut_tube(4.4).move_to([0, -2.15, 0])
        self.play(FadeIn(gut, shift=UP*.2), run_time=.55)
        dots = VGroup(*[Dot(radius=.10, color=BLUE).move_to([-1.7+i*.3, -2.1, 0]) for i in range(5)])
        cross = VGroup(Line(UL*.35, DR*.35, color=RED, stroke_width=8),
                       Line(UR*.35, DL*.35, color=RED, stroke_width=8)).move_to([3.35, -1.25, 0])
        self.play(left.animate.move_to([-1.1, -1.6, 0]).scale(.55), FadeIn(dots),
                  right.animate.shift(UP*.3), FadeIn(cross, scale=1.5), run_time=1.1)
        self.at("The answer is one bond")
        a, b = glucose_tile(1.18).move_to([-.95, .35, 0]), glucose_tile(1.18).move_to([.95, .35, 0])
        j = joint_between(a, b, width=12)
        self.play(FadeOut(VGroup(br, wood, left, right, gut, dots, cross)), FadeIn(a), FadeIn(b), GrowFromCenter(j), run_time=1.0)
        self.at("pointing one of two ways")
        arrow = Arrow([0, .35, 0], [0, 1.8, 0], color=GOLD, stroke_width=8, buff=0)
        self.play(GrowArrow(arrow), run_time=.35)
        self.play(Rotate(arrow, PI, about_point=[0,.35,0]), run_time=.55)
        self.play(Rotate(arrow, -PI, about_point=[0,.35,0]), run_time=.55)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Carbohydrates"
    TITLE = "Same Brick, Different Snap"


class S02Ring(FilmScene):
    def construct(self):
        water = Rectangle(width=13.0, height=4.8, stroke_width=0, fill_color=BLUE, fill_opacity=.07).move_to([0,-.45,0])
        ripple = always_redraw(lambda: ParametricFunction(lambda t: [t, -2.45+.08*math.sin(2*t+self.renderer.time), 0],
                                   t_range=[-6.2,6.2], color=BLUE, stroke_width=3).set_opacity(.65))
        card = RoundedRectangle(corner_radius=.25, width=7.0, height=3.1, stroke_color=TEXT, stroke_width=4,
                                fill_color=TEXT, fill_opacity=.09)
        title = T("glucose chain", 34).move_to(card)
        c1 = chip("C1 carbonyl", GOLD, 30).move_to([2.25,.7,0])
        c5 = chip("C5–OH", TEAL, 30).move_to([-2.15,-.65,0])
        c6 = chip("C6", TEAL, 28).move_to([-2.25,1.05,0])
        arm = Line([-1.55,-.45,0], [-.5,-.2,0], color=TEAL, stroke_width=6)
        self.add(water, ripple)
        self.at("a glucose chain")
        self.play(FadeIn(card), FadeIn(title), FadeIn(c1), FadeIn(c5), FadeIn(c6), Create(arm), run_time=1.1)
        self.at("does not stay straight")
        self.play(Rotate(card, .08), Rotate(title, .08), rate_func=there_and_back, run_time=.7)
        self.at("carbon five swings around")
        self.play(c5.animate.move_to([1.35,-.15,0]), Rotate(arm, -1.0, about_point=arm.get_start()), run_time=1.3)
        self.at("attacks carbon one")
        self.play(c5.animate.next_to(c1, LEFT, buff=.05), Indicate(c1, color=GOLD), run_time=.8)
        self.at("The ring closes")
        tile = glucose_tile(2.1).move_to(ORIGIN)
        self.play(ReplacementTransform(VGroup(card,title,c1,c5,c6,arm), tile), run_time=1.0)
        self.at("on its own")
        enz = chip("enzyme", PURPLE, 32).move_to([-4.4,2.5,0])
        strike = Line(enz.get_corner(DL), enz.get_corner(UR), color=RED, stroke_width=8)
        tag = schematic()
        self.play(FadeIn(enz, shift=RIGHT*.2), Create(strike), FadeIn(tag), run_time=.65)
        self.play(VGroup(enz,strike).animate.shift(LEFT*2), FadeOut(VGroup(enz,strike)), run_time=.6)
        self.finish()


class S03Anomeric(FilmScene):
    def construct(self):
        tile = glucose_tile(2.85).move_to([-1.0,0,0])
        self.add(tile)
        self.at("Carbon 1 becomes")
        self.play(Indicate(tile.pin, color=GOLD, scale_factor=2.1), run_time=.9)
        self.at("the anomeric carbon")
        label = T("anomeric carbon", 34, GOLD).move_to([4.1,.25,0])
        arr = Arrow(label.get_left()+LEFT*.22, tile.pin.get_center()+RIGHT*.28,
                    color=GOLD, buff=0, stroke_width=5)
        self.play(FadeIn(label, shift=LEFT*.2), GrowArrow(arr), run_time=.8)
        self.at("new hydroxyl group")
        stalk = Line(tile.pin.get_center(), tile.pin.get_center()+UP*1.25+RIGHT*.35, color=GOLD, stroke_width=6)
        oh = chip("OH", GOLD, 30).move_to(stalk.get_end()+UP*.25)
        self.play(GrowFromPoint(stalk, tile.pin.get_center()), FadeIn(oh), run_time=.8)
        self.at("either face")
        flag = VGroup(stalk, oh)
        self.play(Rotate(flag, PI, about_point=tile.pin.get_center()), run_time=.7)
        self.play(Rotate(flag, -PI, about_point=tile.pin.get_center()), run_time=.7)
        self.finish()


class S04Faces(FilmScene):
    def construct(self):
        alpha = glucose_tile(2.35, BLUE, True, "down").move_to([-3.35,.45,0])
        beta = glucose_tile(2.35, GREEN, True, "up").move_to([3.35,.45,0])
        seed = glucose_tile(2.35).move_to(ORIGIN).set_opacity(.25)
        self.add(seed)
        self.at("Beta means")
        self.play(FadeOut(seed), FadeIn(beta, shift=RIGHT*.3), run_time=.65)
        b_lab = T("β: same face as C6", 32, GREEN).move_to([3.4,-2.25,0])
        self.play(FadeIn(b_lab), Indicate(VGroup(beta.tab,beta.flag), color=GREEN), run_time=.75)
        self.at("Alpha means")
        self.play(FadeIn(alpha, shift=LEFT*.3), run_time=.55)
        a_lab = T("α: opposite face", 32, BLUE).move_to([-3.4,-2.25,0])
        self.play(FadeIn(a_lab), Indicate(VGroup(alpha.tab,alpha.flag), color=BLUE), run_time=.75)
        self.at("snap to follow")
        link = DoubleArrow(alpha.flag.get_center(), beta.flag.get_center(), color=GOLD, buff=.35, stroke_width=5)
        self.play(GrowFromCenter(link), run_time=.55)
        self.play(Indicate(link, color=GOLD, scale_factor=1.05), run_time=.8)
        self.finish()


class S05Free(FilmScene):
    def construct(self):
        water = Rectangle(width=13,height=4.8,stroke_width=0,fill_color=BLUE,fill_opacity=.07).move_to([0,-.7,0])
        tiles = VGroup(*[glucose_tile(.62, GREEN if i<4 else BLUE, True, "up" if i<4 else "down")
                         .move_to([-4.5+(i%3)*4.5, .5-(i//3)*2.0,0]) for i in range(6)])
        self.add(water, tiles)
        self.at("ring keeps reopening")
        self.play(*[t.animate.stretch(1.25,0).stretch(.75,1) for t in tiles[::2]], run_time=.65)
        self.play(*[t.animate.stretch(.8,0).stretch(1/.75,1) for t in tiles[::2]], run_time=.65)
        self.at("flipping between alpha and beta")
        self.play(*[Rotate(t.flag, PI, about_point=t.pin.get_center()) for t in tiles[1::2]], run_time=.75)
        self.at("about two thirds")
        W, H = 8.0, .75
        green = Rectangle(width=.64*W,height=H,stroke_width=0,fill_color=GREEN,fill_opacity=.9).move_to([-4+.64*W/2,2.75,0])
        blue = Rectangle(width=.36*W,height=H,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to([-4+.64*W+.36*W/2,2.75,0])
        gl = T("β about 2/3", 30, BG, weight=BOLD).move_to(green)
        al = T("α about 1/3", 30, BG, weight=BOLD).move_to(blue).scale(.82)
        self.play(GrowFromEdge(green,LEFT), GrowFromEdge(blue,LEFT), FadeIn(gl), FadeIn(al), run_time=1.0)
        self.play(*[t.animate.shift(UP*.08) for t in tiles], rate_func=there_and_back, run_time=1.2)
        self.finish()


class S06Locked(FilmScene):
    def construct(self):
        tr=track(); a=glucose_tile(1.35).move_to([-1.7,0,0]); self.add(tr,a)
        self.at("bond that carbon")
        b=glucose_tile(1.35).move_to([4.8,0,0])
        self.play(b.animate.move_to([1.7,0,0]), run_time=1.0)
        self.at("carbon 4")
        j=joint_between(a,b,width=10)
        self.play(GrowFromPoint(j,a.pin.get_center()), Indicate(b.port,color=GOLD),run_time=.8)
        self.at("ring cannot open")
        self.play(a.animate.stretch(1.18,0),run_time=.35)
        self.play(a.animate.stretch(1/1.18,0),run_time=.35)
        self.play(Wiggle(a,scale_value=1.04,rotation_angle=.03),run_time=.55)
        self.at("locked in")
        lock=lock_icon(j.get_center()+UP*.55)
        self.play(FadeIn(lock,shift=DOWN*.3),run_time=.6)
        self.play(Indicate(lock,color=GOLD),run_time=.7)
        self.finish()


class S07Name(FilmScene):
    def construct(self):
        def row(y,color,flag):
            a=glucose_tile(1.15,color,True,flag).move_to([-.9,y,0]); b=glucose_tile(1.15,color).move_to([1.2,y,0])
            return VGroup(a,b,joint_between(a,b,width=9))
        top=row(1.7,BLUE,"down"); bottom=row(-1.45,GREEN,"up")
        top.add_updater(lambda m, dt: m.set_y(1.7 + .12 * math.sin(TAU * self.renderer.time / 2.8)))
        bottom.add_updater(lambda m, dt: m.set_y(-1.45 - .12 * math.sin(TAU * self.renderer.time / 2.8)))
        self.add(top,bottom)
        self.at("this 1 4 bond")
        self.play(Indicate(top[2],color=GOLD),Indicate(bottom[2],color=GOLD),run_time=.9)
        self.at("alpha face")
        ac=chip("starch: α-1,4",BLUE,32).move_to([-4.45,1.7,0])
        self.play(FadeIn(ac),Indicate(top[0].flag,color=BLUE),run_time=.75)
        self.at("beta face")
        bc=chip("cellulose: β-1,4",GREEN,32).move_to([-4.35,-1.45,0])
        self.play(FadeIn(bc),Indicate(bottom[0].flag,color=GREEN),run_time=.75)
        self.play(top.animate.shift(UP*.06),bottom.animate.shift(DOWN*.06),rate_func=there_and_back,run_time=1.1)
        self.finish()


class S08Angle(FilmScene):
    def construct(self):
        beta=glucose_tile(2.45,GREEN).move_to([-3.35,.25,0]); alpha=glucose_tile(2.45,BLUE).move_to([3.35,.25,0])
        bob(beta, .055, 2.8)
        bob(alpha, .055, 2.8, PI)
        in_b=Arrow([-5.8,.25,0],beta.get_left()+LEFT*.22,color=TEXT,buff=0,stroke_width=6)
        in_a=Arrow([.9,.25,0],alpha.get_left()+LEFT*.22,color=TEXT,buff=0,stroke_width=6)
        out_b=Arrow(beta.get_right()+RIGHT*.22,[-.9,.25,0],color=GOLD,buff=0,stroke_width=7)
        out_a=Arrow(alpha.get_right()+RIGHT*.22,[5.9,-1.7,0],color=GOLD,buff=0,stroke_width=7)
        self.add(beta,alpha,in_b,in_a)
        self.at("ring is puckered")
        self.play(Rotate(beta,.10),Rotate(alpha,-.10),rate_func=there_and_back,run_time=.9)
        self.at("points straight across")
        guide=DashedLine([-5.9,.25,0],[-.8,.25,0],color=GREEN,stroke_width=3)
        self.play(GrowArrow(out_b),Create(guide),run_time=.8)
        self.at("sharp angle")
        arc=Arc(radius=.8,start_angle=PI,angle=.72,color=BLUE,stroke_width=5).move_arc_center_to(alpha.get_right())
        self.play(GrowArrow(out_a),Create(arc),FadeIn(schematic()),run_time=.85)
        self.play(Rotate(alpha,.08),rate_func=there_and_back,run_time=1.0)
        self.finish()


class S09Predict(FilmScene):
    def construct(self):
        top=Line([-6,1.55,0],[6,1.55,0],color=BLUE,stroke_width=4)
        bot=Line([-6,-1.55,0],[6,-1.55,0],color=GREEN,stroke_width=4)
        ghosts=VGroup(*[glucose_tile(.27,BLUE).set_opacity(.28).move_to([-5.5+i*.58,1.55,0]) for i in range(20)],
                      *[glucose_tile(.27,GREEN).set_opacity(.28).move_to([-5.5+i*.58,-1.55,0]) for i in range(20)])
        labs=VGroup(T("α-1,4",30,BLUE).move_to([-5.5,2.55,0]),T("β-1,4",30,GREEN).move_to([-5.5,-2.55,0]))
        self.at("chain glucoses together")
        self.play(Create(top),Create(bot),FadeIn(labs),LaggedStart(*[FadeIn(g) for g in ghosts],lag_ratio=.015),run_time=1.3)
        self.at("runs straight")
        q=chip("Straight or bending?",TEXT,40,pad=.35,fill_opacity=.85).move_to(ORIGIN)
        q[0].set_fill(BG,opacity=.96)
        self.play(FadeIn(q,shift=DOWN*.35),run_time=.65)
        self.at("bends at every glucose")
        self.play(Indicate(ghosts[:20],color=BLUE,scale_factor=1.05),run_time=.75)
        self.at("Picture it first")
        self.play(Indicate(q,color=GOLD,scale_factor=1.05),run_time=.8)
        self.finish()


class S10Think(Scene):
    def construct(self):
        top=Line([-6,1.55,0],[6,1.55,0],color=BLUE,stroke_width=4)
        bot=Line([-6,-1.55,0],[6,-1.55,0],color=GREEN,stroke_width=4)
        ghosts=VGroup(*[glucose_tile(.27,BLUE).set_opacity(.28).move_to([-5.5+i*.58,1.55,0]) for i in range(20)],
                      *[glucose_tile(.27,GREEN).set_opacity(.28).move_to([-5.5+i*.58,-1.55,0]) for i in range(20)])
        q=chip("Straight or bending?",TEXT,40,pad=.35,fill_opacity=.85); q[0].set_fill(BG,opacity=.96)
        timer_bg=Line([-1.55,-.72,0],[1.55,-.72,0],color=GOLD,stroke_width=7).set_opacity(.18)
        progress=Line([-1.55,-.72,0],[1.55,-.72,0],color=GOLD,stroke_width=7)
        self.add(top,bot,ghosts,q,timer_bg)
        self.play(Create(progress),ghosts.animate.set_opacity(.36),run_time=4.5,rate_func=linear)


class S11Beta(FilmScene):
    def construct(self):
        ghosts=VGroup(*[glucose_tile(.34,GREEN).set_opacity(.25).move_to([-5.4+i*1.2,-.15,0]) for i in range(10)])
        self.add(ghosts)
        self.at("Beta runs straight")
        tiles=VGroup(*[glucose_tile(.34,GREEN,c6_up=(i%2==0)).move_to([-5.4+i*1.2,-.15,0]) for i in range(10)])
        bars=VGroup(*[Line(tiles[i].get_right(),tiles[i+1].get_left(),color=GOLD,stroke_width=6) for i in range(9)])
        self.play(LaggedStart(*[FadeIn(t,shift=UP*.35) for t in tiles],lag_ratio=.08),FadeOut(ghosts),run_time=1.35)
        self.at("like a rod")
        rod=Line([-6,-.15,0],[6,-.15,0],color=GREEN,stroke_width=5).set_z_index(-2)
        self.play(Create(rod),LaggedStart(*[Create(x) for x in bars],lag_ratio=.07),run_time=1.0)
        self.at("flipped from its neighbors")
        self.play(*[Rotate(t,PI,axis=RIGHT) for t in tiles[1::2]],run_time=.8)
        self.at("lies flat")
        rib=ribbon(-.15,12, GREEN).set_z_index(-3)
        lab=T("flat ribbon",32,GREEN).move_to([0,-1.35,0])
        self.play(FadeIn(rib),FadeIn(lab),run_time=.65)
        self.play(tiles.animate.shift(UP*.06),rate_func=there_and_back,run_time=.9)
        self.finish()


class S12Alpha(FilmScene):
    def construct(self):
        self.at("Alpha bends at every joint")
        pts=[np.array([-5.4+i*.85,1.65*math.cos(TAU*i/6),0]) for i in range(13)]
        tiles=VGroup(*[glucose_tile(.30,BLUE).move_to(p) for p in pts])
        links=VGroup(*[Line(pts[i],pts[i+1],color=GOLD,stroke_width=5) for i in range(12)]).set_z_index(-1)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles],lag_ratio=.06),LaggedStart(*[Create(l) for l in links],lag_ratio=.06),run_time=1.35)
        self.at("same way")
        self.play(tiles.animate.rotate(.12),rate_func=there_and_back,run_time=.6)
        self.at("winds into a helix")
        curve=helix_curve(BLUE,0,2,10.8,2.05)
        beads=VGroup(*[Dot(curve.point_from_proportion(i/12),radius=.14,color=BLUE) for i in range(13)])
        self.play(ReplacementTransform(VGroup(tiles,links),VGroup(curve,beads)),run_time=1.1)
        self.at("about 6 glucoses")
        bracket=Brace(Line([-5.4,-2.35,0],[0,-2.35,0]),DOWN,color=BLUE)
        lab=T("about 6 per turn",30,BLUE).next_to(bracket,DOWN,buff=.12)
        self.play(GrowFromCenter(bracket),FadeIn(lab),FadeIn(schematic()),run_time=.7)
        self.play(beads.animate.shift(UP*.12),rate_func=there_and_back,run_time=1.2)
        self.finish()


class S13Fiber(FilmScene):
    def construct(self):
        rows=VGroup(*[ribbon(y,10.5,GREEN) for y in [1.35,0,-1.35]])
        self.at("ribbons lie side by side")
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*(i-1)*.5) for i,r in enumerate(rows)],lag_ratio=.18),run_time=1.0)
        self.at("hydrogen bond")
        dashes=VGroup(*[DashedLine([x,.95,0],[x,.4,0],color=GOLD,stroke_width=4,dash_length=.12) for x in np.linspace(-4.5,4.5,9)],
                       *[DashedLine([x,-.4,0],[x,-.95,0],color=GOLD,stroke_width=4,dash_length=.12) for x in np.linspace(-4.5,4.5,9)])
        lab=T("hydrogen bonds",30,GOLD).move_to([0,2.65,0])
        self.play(LaggedStart(*[Create(d) for d in dashes],lag_ratio=.035),FadeIn(lab),run_time=1.0)
        self.at("rigid fibers")
        fibril=RoundedRectangle(corner_radius=.22,width=10.8,height=2.9,stroke_color=GREEN,stroke_width=6,fill_color=GREEN,fill_opacity=.28)
        fl=T("cellulose fibril",32,GREEN).move_to(fibril)
        self.play(ReplacementTransform(VGroup(rows,dashes),fibril),FadeOut(lab),run_time=.55)
        self.play(FadeIn(fl),run_time=.30)
        self.at("holds plants up")
        stem=Line([0,-3.5,0],[0,3.3,0],color=GREEN,stroke_width=18).set_z_index(-3)
        leaf1=Ellipse(width=1.7,height=.7,color=GREEN,fill_color=GREEN,fill_opacity=.25).rotate(.5).move_to([.8,2.2,0])
        leaf2=leaf1.copy().rotate(PI-1).move_to([-.8,1.25,0])
        self.play(FadeOut(fl), fibril.animate.scale(.45).move_to([0,-1.5,0]),
                  GrowFromEdge(stem,DOWN),FadeIn(leaf1),FadeIn(leaf2),run_time=1.0)
        self.finish()


class S14Fuel(FilmScene):
    def construct(self):
        fibril=RoundedRectangle(corner_radius=.2,width=3.3,height=5.0,stroke_color=GREEN,stroke_width=5,fill_color=GREEN,fill_opacity=.2).move_to([4.7,0,0])
        self.add(fibril,T("cellulose fibril",30,GREEN).rotate(PI/2).move_to(fibril))
        self.at("helices cannot lie flat")
        hs=VGroup(*[helix_curve(BLUE,y,1,5.7,.45).move_to([-2.3,y,0]) for y in [1.35,0,-1.35]])
        self.play(LaggedStart(*[FadeIn(h,shift=DOWN*.2) for h in hs],lag_ratio=.15),run_time=.85)
        no=chip("no fibril",RED,30).move_to([-2.3,-2.6,0])
        self.play(hs[0].animate.shift(DOWN*.3),hs[1].animate.shift(UP*.25),rate_func=there_and_back,run_time=.65)
        self.play(FadeIn(no),run_time=.35)
        self.at("compact granules")
        g1=granule(1.35,"starch granule (plant)",[-2.7,.5,0])
        self.play(ReplacementTransform(hs,g1),FadeOut(no),run_time=1.0)
        self.at("starch in plants")
        self.play(Indicate(g1[0],color=BLUE),run_time=.65)
        self.at("glycogen in animals")
        g2=granule(1.0,"glycogen particle (animal)",[.55,-1.25,0])
        self.play(FadeIn(g2,scale=.5),run_time=.7)
        self.at("Stored fuel")
        self.play(Indicate(g1,color=BLUE),Indicate(g2,color=BLUE),run_time=.9)
        self.finish()


class S15Enzyme(FilmScene):
    def construct(self):
        starch=granule(1.35,"starch",[-3.8,.55,0]); fibril=ribbon(.55,3.5,GREEN).rotate(PI/2).move_to([3.8,.55,0])
        fl=T("cellulose",30,GREEN).next_to(fibril,DOWN,buff=.25)
        gut=gut_tube(8.5).move_to([0,-2.65,0])
        self.add(starch,fibril,fl,gut)
        self.at("an enzyme that fits")
        body=Circle(radius=.75,stroke_color=PURPLE,stroke_width=5,fill_color=PURPLE,fill_opacity=.2)
        notch=Polygon([.15,.15,0],[.9,.55,0],[.9,-.55,0],color=BG,fill_color=BG,fill_opacity=1,stroke_width=0)
        enz=VGroup(body,notch).move_to([0,.55,0])
        enz_label=T("amylase",30,PURPLE).move_to([0,1.65,0])
        self.play(FadeIn(enz,scale=.6),FadeIn(enz_label),run_time=.7)
        self.at("amylases fit")
        self.play(enz.animate.move_to([-3.3,.55,0]),
                  enz_label.animate.move_to([-3.3,2.55,0]),run_time=.7)
        self.play(Rotate(enz,-.3),rate_func=there_and_back,run_time=.55)
        dots=VGroup(*[Dot([-3.6+i*.28,-1.0-i*.12,0],radius=.12,color=BLUE) for i in range(5)])
        self.play(FadeIn(dots),starch.animate.scale(.8),run_time=.7)
        self.play(dots.animate.move_to([0,-2.6,0]),run_time=.9)
        self.finish()


class S16Cow(FilmScene):
    def construct(self):
        fibril=ribbon(.8,5.1,GREEN).rotate(PI/2).move_to([-3.7,.25,0])
        enz=chip("amylase",PURPLE,30).move_to([-.7,.25,0])
        self.add(fibril,enz)
        self.at("no cellulase")
        cross=VGroup(Line(UL*.38,DR*.38,color=RED,stroke_width=9),
                     Line(UR*.38,DL*.38,color=RED,stroke_width=9)).move_to([-2.15,.25,0])
        lab=T("you: no cellulase",30,RED).move_to([-2.6,-2.65,0])
        self.play(enz.animate.shift(LEFT*.35),rate_func=there_and_back,run_time=.55)
        self.play(FadeIn(cross,scale=1.4),FadeIn(lab),run_time=.55)
        self.at("A cow")
        body=Ellipse(width=5.0,height=3.0,color=TEXT,stroke_width=5).move_to([3.2,.35,0])
        head=Circle(radius=.75,color=TEXT,stroke_width=5).move_to([5.55,1.0,0])
        legs=VGroup(*[Line([x,-.8,0],[x,-2.2,0],color=TEXT,stroke_width=6) for x in [1.8,4.1]])
        rumen=Circle(radius=1.0,color=PURPLE,fill_color=PURPLE,fill_opacity=.10).move_to([3.2,.2,0])
        cow=VGroup(body,head,legs,rumen)
        self.play(FadeOut(VGroup(enz,cross,lab)),FadeIn(cow,shift=LEFT*.6),fibril.animate.scale(.55).move_to(rumen),run_time=1.0)
        self.at("gut microbes")
        microbes=VGroup(*[Dot(rumen.get_center()+np.array([.45*math.cos(i),.45*math.sin(i),0]),radius=.12,color=PURPLE) for i in range(6)])
        ml=T("microbes: cellulase",30,PURPLE).move_to([3.2,2.8,0])
        self.play(LaggedStart(*[FadeIn(m,scale=.3) for m in microbes],lag_ratio=.12),FadeIn(ml),run_time=.8)
        self.at("make cellulase for it")
        free=VGroup(*[glucose_tile(.28,GREEN).move_to([1.8+i*.55,-2.7,0]) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(t,shift=UP*.25) for t in free],lag_ratio=.15),fibril.animate.scale(.82),run_time=1.0)
        self.finish()


class S17Return(FilmScene):
    def construct(self):
        br,wood=bread(scale=.72),plank(scale=.72)
        br.move_to([-4.75,.35,0]); wood.move_to([4.75,.35,0])
        a,b=glucose_tile(.9).move_to([-.8,.35,0]),glucose_tile(.9).move_to([.8,.35,0])
        j=joint_between(a,b,width=10)
        self.add(br,wood,a,b,j)
        self.at("brick never changes")
        self.play(Indicate(a,color=TEXT),Indicate(b,color=TEXT),run_time=.8)
        self.at("face of one bond")
        flag=Arrow([0,-.05,0],[0,-1.15,0],color=GOLD,stroke_width=7,buff=0)
        self.play(GrowArrow(flag),run_time=.5)
        self.at("alpha coils into fuel")
        hx=helix_curve(BLUE,-1.9,1,4.6,.6).move_to([-3.2,-1.9,0])
        self.play(Create(hx),br.animate.set_opacity(1),run_time=.9)
        self.at("beta runs straight")
        self.play(Rotate(flag,PI,about_point=[0,.35,0]),run_time=.5)
        rib=ribbon(-1.9,4.6,GREEN).move_to([3.2,-1.9,0])
        self.play(GrowFromEdge(rib,LEFT),wood.animate.set_opacity(1),run_time=.9)
        self.play(Rotate(flag,PI,about_point=[0,.35,0]),run_time=.55)
        self.play(Rotate(flag,-PI,about_point=[0,.35,0]),run_time=.55)
        self.finish()


class S18End(EndCard):
    LINE = "In 1,4-linked glucose, alpha coils into fuel; beta runs straight into fiber."

    def setup(self):
        super().setup()
        a = glucose_tile(.38).move_to([-.35, 2.85, 0])
        b = glucose_tile(.38).move_to([.35, 2.85, 0])
        j = joint_between(a, b, width=6)
        arrow = Arrow([0,3.30,0],[0,3.65,0],color=GOLD,stroke_width=5,buff=0)
        arrow.add_updater(lambda m, dt: m.rotate(
            .32 * dt * math.sin(TAU * self.renderer.time / 2.4), about_point=[0,2.85,0]))
        self.add(a, b, j, arrow)

