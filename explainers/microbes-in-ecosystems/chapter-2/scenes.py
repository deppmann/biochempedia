"""When the Killer Is a Recycler — chapter 2.

COLOR MAP (fixed across the film)
  GREEN       nitrogen / matter moving on
  ORANGE      phosphorus
  PURPLE      bacteria
  RED         viruses and rinderpest
  ALGA        algae and living landscape
  DARK_GREY   host-to-pathogen harm and structure
  TAN         dead organic matter / dry grass

All pictures are schematic cartoons.  There are no molecular structures.
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#8C67B5"
ORANGE = "#F29E4C"
ALGA = "#758B3A"
DARK_GREY = "#59616B"
TAN = "#B88A57"
CREAM = "#F4EBD8"
INK = "#24303A"
WATER = "#74B9D0"
GOLDEN = "#D2A64B"


def cream_ground():
    r = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=CREAM, fill_opacity=1)
    r.set_z_index(-100)
    r.layout_ok = True
    # A quiet, moving paper/water texture keeps long spoken holds alive without adding a claim.
    texture = VGroup(*[
        Circle(radius=1.15 + .16 * (i % 3), stroke_width=0, fill_color=WATER,
               fill_opacity=.13).move_to([-6.8 + i * 1.38, -2.7 + (i % 4) * 1.75, 0])
        for i in range(11)
    ])
    texture.set_z_index(-99)
    texture._drift = 0.0

    def drift(mob, dt):
        mob._drift += dt
        mob.shift(RIGHT * .32 * dt)
        for c in mob:
            if c.get_left()[0] > 7.2:
                c.shift(LEFT * 15.2)
    texture.add_updater(drift)
    return VGroup(r, texture)


def label(text, size=30, color=INK, **kw):
    return T(text, size=size, color=color, **kw)


def virus(at=ORIGIN, r=0.16):
    """Nearly round virus particle; deliberately not a cube."""
    c = Circle(radius=r, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.75).move_to(at)
    return c


def bacterium(at=ORIGIN, scale=1.0):
    return RoundedRectangle(corner_radius=0.16 * scale, width=0.72 * scale, height=0.28 * scale,
                            stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                            fill_opacity=0.72).rotate(0.18).move_to(at)


def alga(at=ORIGIN, r=0.55):
    return Circle(radius=r, stroke_color=ALGA, stroke_width=4, fill_color=ALGA,
                  fill_opacity=0.35).move_to(at)


def nutrient(at=ORIGIN, color=GREEN, r=0.09):
    return Dot(at, radius=r, color=color)


def padlock(at=ORIGIN, open_=False, scale=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.52, stroke_color=DARK_GREY,
                            stroke_width=4, fill_color=DARK_GREY, fill_opacity=0.15)
    shackle = Arc(radius=0.25, start_angle=0, angle=PI, stroke_color=DARK_GREY, stroke_width=4)
    shackle.next_to(body, UP, buff=-0.05)
    if open_:
        shackle.rotate(-0.7, about_point=shackle.get_right()).shift(RIGHT * 0.12)
    return VGroup(body, shackle).scale(scale).move_to(at)


def tracker(usable=False):
    line = Line([-4.8, -3.15, 0], [4.8, -3.15, 0], color=DARK_GREY, stroke_width=7)
    left = label("locked", 28, DARK_GREY).move_to([-5.15, -3.52, 0])
    right = label("usable", 28, GREEN).move_to([5.1, -3.52, 0])
    mark = Dot([4.3 if usable else -4.3, -3.15, 0], radius=0.16, color=GREEN if usable else DARK_GREY)
    return VGroup(line, left, right, mark)


def ocean_band():
    water = Rectangle(width=14.4, height=6.0, stroke_width=0, fill_color=WATER,
                      fill_opacity=0.40).move_to([0, -0.55, 0])
    surface = Line([-7.1, 2.45, 0], [7.1, 2.45, 0], color=WATER, stroke_width=6)
    return VGroup(cream_ground(), water, surface)


def infected_alga_world(burst=False, usable=False):
    g = VGroup(ocean_band())
    if not burst:
        cell = alga([0, 0.1, 0], 1.45)
        dots = VGroup(*[nutrient([x, y, 0]) for x, y in
                        [(-.55, .45), (-.1, .72), (.5, .38), (-.65, -.2), (0, -.15), (.6, -.42)]])
        g.add(cell, dots, padlock([0, 0.05, 0], scale=0.85))
    else:
        fragments = VGroup(*[Arc(radius=1.15, start_angle=a, angle=0.55, color=ALGA,
                                stroke_width=7).shift([0, .05, 0]) for a in np.linspace(0, TAU, 7)[:-1]])
        debris = VGroup(*[Ellipse(width=.48, height=.24, fill_color=TAN, fill_opacity=.65,
                                  stroke_color=TAN, stroke_width=2).rotate(i*.7).move_to(p)
                           for i, p in enumerate([[-1.1,.5,0],[-.45,-.5,0],[.45,.65,0],[1.1,-.25,0],[0,.05,0]])])
        g.add(fragments, debris, padlock([0, 0.1, 0], open_=usable, scale=.85))
    g.add(tracker(usable))
    return g


def flask_world(with_virus=False):
    body = RoundedRectangle(corner_radius=.25, width=5.2, height=4.2, stroke_color=DARK_GREY,
                            stroke_width=5, fill_color=WATER, fill_opacity=.20).move_to([0, -.25, 0])
    neck = Rectangle(width=1.7, height=1.25, stroke_color=DARK_GREY, stroke_width=5,
                     fill_color=CREAM, fill_opacity=1).move_to([0, 2.3, 0])
    neck.set_z_index(-1)
    cells = VGroup(*[alga(p, .34) for p in [[-1.5,.8,0],[0,.9,0],[1.35,.45,0],[-1.1,-.7,0],[.35,-.55,0],[1.55,-1.25,0]]])
    g = VGroup(cream_ground(), neck, body, cells)
    if with_virus:
        g.add(VGroup(*[virus(p, .13) for p in [[-.7,1.3,0],[.8,.2,0],[-.2,-1.25,0],[1.7,-.4,0]]]))
    return g


def animal(at, color=INK, scale=.75):
    body = Ellipse(width=1.0, height=.5, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=.3)
    head = Circle(radius=.2, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=.3).next_to(body, RIGHT, buff=-.02)
    legs = VGroup(*[Line([x,-.18,0],[x,-.55,0],color=color,stroke_width=3) for x in (-.3,.25)])
    return VGroup(body, head, legs).scale(scale).move_to(at)


def tree(at, scale=1.0):
    trunk = Line([0,-.55,0],[0,.25,0], color=TAN, stroke_width=6)
    crown = Circle(radius=.48, stroke_color=ALGA, stroke_width=3, fill_color=ALGA,
                   fill_opacity=.55).move_to([0,.55,0])
    return VGroup(trunk, crown).scale(scale).move_to(at)


def savanna_world(tree_count=3, herd=4, short_grass=False, green=False):
    ground_col = ALGA if green else GOLDEN
    ground = Rectangle(width=14.4, height=3.45, stroke_width=0, fill_color=ground_col,
                       fill_opacity=.48).move_to([0,-1.8,0])
    horizon = Line([-7.1,-.08,0],[7.1,-.08,0], color=ground_col, stroke_width=5)
    grass_h = .25 if short_grass else .7
    grass = VGroup(*[Line([x,-2.75,0],[x+.08,-2.75+grass_h,0], color=ground_col, stroke_width=3)
                     for x in np.linspace(-6.4,6.4,25)])
    herd_pts = np.linspace(-3.7, 3.2, max(herd,1))
    animals = VGroup(*[animal([x, -1.0-(i%2)*.55, 0], scale=.62) for i,x in enumerate(herd_pts[:herd])])
    tree_pts = [(-5.2,-.8),(5.1,-.9),(-2.1,-.5),(2.1,-.55),(0,-.35),(3.8,-.5),(-3.8,-.35)]
    trees = VGroup(*[tree([x,y,0], .8+(i%2)*.15) for i,(x,y) in enumerate(tree_pts[:tree_count])])
    return VGroup(cream_ground(), ground, horizon, grass, animals, trees)


def prediction_backdrop():
    return savanna_world(tree_count=3, herd=4)


def answer_cards():
    more = chip("more trees", ALGA, 30).move_to([-2.3, 2.35, 0])
    fewer = chip("fewer trees", TAN, 30).move_to([2.3, 2.35, 0])
    return VGroup(more, fewer)


class S00Title(TitleCard):
    LESSON = "Microbes in Bodies and Ecosystems"
    TITLE = "When the Killer Is a Recycler"


class S01Link(SpokenScene):
    def construct(self):
        self.add(ocean_band())
        host = alga([-3.3, .5, 0], 1.05)
        pathogens = VGroup(*[virus([2.6+i*.45, .6+(i%2)*.45, 0], .18) for i in range(4)])
        arrow = Arrow([-2.0,.5,0],[1.8,.5,0], color=DARK_GREY, stroke_width=7, tip_length=.3)
        self.at("Some pathogens kill")
        self.play(FadeIn(host), FadeIn(pathogens), run_time=.8)
        self.at("That arrow")
        self.play(GrowArrow(arrow), run_time=.7)
        q = label("Where does the cell's matter go?", 38, INK, font=TITLE_FONT).move_to([0,-1.7,0])
        self.at("where does that")
        self.play(Write(q), arrow.animate.shift(UP*.3), run_time=1.0)
        bob(pathogens, amp=.08, speed=1.2)
        self.finish()


class S02Question(SpokenScene):
    def construct(self):
        world = infected_alga_world()
        self.add(world)
        v = virus([-4.8, .4, 0], .22)
        self.at("Picture a virus")
        self.play(FadeIn(v), v.animate.move_to([-1.72,.35,0]), run_time=1.6)
        self.at("cell held nitrogen")
        self.play(Indicate(world[2], color=GREEN, scale_factor=1.08), run_time=.8)
        q = label("Where does the nitrogen go?", 38, GREEN, font=TITLE_FONT).move_to([0,2.95,0])
        self.at("Where is that nitrogen")
        self.play(Write(q), run_time=.9)
        pulse(world[-1][0], base=7, amp=1.5, speed=2)
        self.finish()


class S03Viruses(SpokenScene):
    def construct(self):
        self.add(ocean_band())
        viruses = VGroup(*[virus(p,.12) for p in [[-5,1.5,0],[-4,.5,0],[-2.8,1.7,0],[-1.5,.2,0],
                                                   [0,1.4,0],[1.2,.3,0],[2.5,1.5,0],[4,.5,0],[5.2,1.4,0]]])
        rods = VGroup(*[bacterium(p,.9) for p in [[-4,-1.2,0],[-1.8,-1.45,0],[.2,-1.1,0]]])
        algae = VGroup(alga([3.2,-1.25,0],.5), alga([5,-1.05,0],.45))
        self.at("Ocean water holds")
        self.play(LaggedStart(*[FadeIn(v) for v in viruses], lag_ratio=.08), FadeIn(rods), FadeIn(algae), run_time=1.2)
        ph = label("bacteriophage (phage): infects bacteria", 27, PURPLE).move_to([-3.05,2.85,0])
        self.at("called a bacteriophage")
        self.play(viruses[1].animate.move_to(rods[0].get_top()), FadeIn(ph), run_time=.9)
        other = label("other viruses: infect algae", 27, RED).move_to([4.1,2.85,0])
        self.at("Other ocean viruses")
        self.play(viruses[-2].animate.move_to(algae[0].get_top()), FadeIn(other), run_time=.9)
        self.add(scope_tag("schematic", color=DARK_GREY))
        bob(viruses, amp=.05, speed=1.1)
        self.finish()


class S04Flask(SpokenScene):
    def construct(self):
        flask = flask_world(False)
        self.add(flask[0])
        self.at("Researchers built")
        self.play(FadeIn(VGroup(*flask[1:3])), run_time=.8)
        title = label("lab model ecosystem", 34, INK).move_to([0,3.15,0])
        self.play(FadeIn(title), run_time=.4)
        self.at("with an ocean alga")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in flask[3]], lag_ratio=.1), run_time=1.0)
        name = label("Phaeocystis", 32, ALGA).move_to([-4.6,.4,0])
        self.play(FadeIn(name), run_time=.4)
        dropper = VGroup(Line([3.6,3.0,0],[2.2,1.8,0],color=DARK_GREY,stroke_width=9),
                         Triangle(color=RED, fill_color=RED, fill_opacity=.55).scale(.16).move_to([2.0,1.65,0]))
        self.at("Then they added")
        self.play(FadeIn(dropper), run_time=.5)
        vs = VGroup(*[virus([2.0,1.4-i*.55,0],.13) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(v, shift=DOWN*.25) for v in vs], lag_ratio=.15), run_time=1.0)
        bob(flask[3], amp=.04, speed=1.3)
        self.finish()


class S05Burst(SpokenScene):
    def construct(self):
        world = infected_alga_world(False)
        self.add(world)
        vs = VGroup(*[virus(p,.18) for p in [[-2,.8,0],[-1.7,-.4,0],[1.8,.5,0]]])
        self.at("viruses infected")
        self.play(FadeIn(vs), vs.animate.shift(RIGHT*.35), run_time=.9)
        burst = infected_alga_world(True)
        self.at("cells burst")
        self.play(FadeOut(VGroup(*world[1:-1], vs)), FadeIn(VGroup(*burst[1:-1])), run_time=.9)
        self.at("spilling much")
        self.play(*[m.animate.shift((m.get_center()/max(np.linalg.norm(m.get_center()),.2))*0.55)
                    for m in burst[1:-1]], run_time=.8)
        dead = label("algae dead", 34, DARK_GREY).move_to([0,2.95,0])
        self.at("algae were dead")
        self.play(FadeIn(dead), run_time=.5)
        q = label("Nitrogen gone too?", 38, GREEN, font=TITLE_FONT).move_to([0,-2.25,0])
        self.at("Was their nitrogen")
        self.play(Write(q), run_time=.8)
        pulse(burst[-1][0], base=7, amp=1.5, speed=2)
        self.finish()


class S06Bacteria(SpokenScene):
    def construct(self):
        world = infected_alga_world(True)
        self.add(world)
        bacteria = VGroup(*[bacterium(p,.85) for p in [[-2,.8,0],[-1.5,-.7,0],[1.6,.8,0],[2,-.6,0],[-.4,1.3,0]]])
        self.at("bacteria swarmed")
        self.play(LaggedStart(*[FadeIn(b, shift=-b.get_center()*.18) for b in bacteria], lag_ratio=.12), run_time=1.1)
        debris = world[2]
        self.at("broke them down")
        self.play(debris.animate.scale(.55), bacteria.animate.shift(UP*.12), run_time=.9)
        ns = VGroup(*[nutrient(p,GREEN) for p in [[-2.7,.2,0],[-1.4,1.25,0],[.5,1.45,0],[2.7,.3,0],[-.5,-1.2,0]]])
        ps = VGroup(*[nutrient(p,ORANGE) for p in [[-2.2,-1.1,0],[1.4,1.1,0],[2.2,-1.0,0]]])
        self.at("water gained nitrogen")
        self.play(FadeIn(ns), FadeIn(ps), Transform(world[3], padlock([0,.1,0],open_=True,scale=.85)),
                  world[-1][-1].animate.move_to([4.3,-3.15,0]).set_color(GREEN), run_time=1.2)
        survivors = VGroup(alga([-4.8,.3,0],.55), bacterium([4.7,.2,0],1.15))
        self.at("Algae and bacteria")
        self.play(FadeIn(survivors), ns[0].animate.move_to([-4.8,.3,0]), ps[-1].animate.move_to([4.7,.2,0]), run_time=1.0)
        bob(bacteria, amp=.06, speed=1.5)
        self.finish()


class S07Recycler(SpokenScene):
    def construct(self):
        self.add(cream_ground())
        panels = TwoPanel("virus infects alga", "matter moves on", colors=(RED, GREEN), top=3.1, bottom=-2.5)
        panels.set_color(DARK_GREY)
        self.play(FadeIn(panels), run_time=.7)
        left = VGroup(alga(ORIGIN,.75), virus([-.95,.4,0],.18))
        panels.put(left,"left")
        right = VGroup(*[nutrient(p, GREEN, .11) for p in [[-.7,.5,0],[0,.8,0],[.7,.3,0],[-.5,-.5,0],[.5,-.6,0]]],
                       bacterium([0,-.1,0],1.2))
        panels.put(right,"right")
        self.at("nitrogen was not destroyed")
        self.play(FadeIn(left), run_time=.6)
        self.at("went back into")
        self.play(FadeIn(right), run_time=.8)
        rule = caption("A killer can be part of a recycling chain.", color=INK)
        self.at("A killer can")
        self.play(FadeIn(rule), run_time=.7)
        steps = VGroup(chip("virus",RED,28), chip("bacteria",PURPLE,28), chip("other life",ALGA,28)).arrange(RIGHT,buff=.9).move_to([0,.15,0])
        arrows = VGroup(*[Arrow(steps[i].get_right(),steps[i+1].get_left(),buff=.12,color=GREEN,tip_length=.2) for i in range(2)])
        self.at("Virus then bacteria")
        self.play(FadeOut(VGroup(panels,left,right)), FadeIn(steps), GrowArrow(arrows[0]), run_time=.9)
        self.at("then other living")
        self.play(GrowArrow(arrows[1]), run_time=.6)
        bob(steps, amp=.04, speed=1.2)
        self.finish()


class S08Serengeti(SpokenScene):
    def construct(self):
        flask = flask_world(True).scale(.18).move_to([-5.7,2.8,0])
        self.add(cream_ground(), flask)
        self.at("zoom out")
        self.play(flask.animate.scale(.08), FadeIn(savanna_world(3,5)[1:]), run_time=1.3)
        place = label("Serengeti, East Africa", 40, INK, font=TITLE_FONT).move_to([0,3.1,0])
        self.at("the Serengeti")
        self.play(Write(place), run_time=.8)
        rp = VGroup(virus([0,1.85,0],.3), label("rinderpest",30,RED).move_to([0,1.35,0]))
        self.at("Rinderpest is")
        self.play(FadeIn(rp), run_time=.7)
        cattle = label("cattle",28,INK).move_to([-3.4,-2.35,0])
        wild = label("wildebeest",28,INK).move_to([3.1,-3.25,0])
        self.at("cattle and")
        self.play(FadeIn(cattle), run_time=.4)
        self.at("such as wildebeest")
        self.play(FadeIn(wild), rp[0].animate.shift(RIGHT*1.0), run_time=.7)
        bob(rp, amp=.06, speed=1.2)
        self.finish()


class S09Wiped(SpokenScene):
    def construct(self):
        sav = savanna_world(3,4)
        self.add(sav)
        year = chip("1960s", DARK_GREY, 34).move_to([-5.3,2.9,0])
        self.at("In the 1960s")
        self.play(FadeIn(year), run_time=.6)
        rp = VGroup(virus([0,1.7,0],.34), label("rinderpest",30,RED).move_to([0,1.15,0]))
        syringe = VGroup(Line([-4,2.2,0],[-3.2,1.4,0],color=WATER,stroke_width=8),
                         Line([-4.2,2.4,0],[-3.8,2.0,0],color=WATER,stroke_width=4))
        self.add(rp)
        self.at("vaccinating cattle")
        self.play(FadeIn(syringe), syringe.animate.shift(RIGHT*2.0), run_time=1.0)
        self.at("virus was gone")
        self.play(FadeOut(rp, scale=.2), FadeOut(syringe), run_time=.8)
        chain = VGroup(*[chip(x,DARK_GREY,24) for x in ["rinderpest gone","?","?","?"]]).arrange(RIGHT,buff=.35).move_to([.5,2.75,0])
        self.play(FadeIn(chain), run_time=.7)
        q = label("What happened to the land?",38,INK,font=TITLE_FONT).move_to([0,-3.35,0])
        self.at("What happened")
        self.play(Write(q), run_time=.7)
        bob(sav[4], amp=.035, speed=1.2)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        back = prediction_backdrop()
        cards = answer_cards()
        self.add(back)
        self.at("question to try")
        self.play(FadeIn(cards, shift=DOWN*.2), run_time=.8)
        q = question_card("With rinderpest gone: more trees or fewer trees?", y=-3.15, color=INK)
        self.at("With rinderpest gone")
        self.play(FadeIn(q), run_time=.7)
        pulse(cards[0][0], base=3, amp=1.2, speed=2)
        pulse(cards[1][0], base=3, amp=1.2, speed=2)
        bob(back[4], amp=.035, speed=1.1)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.add(prediction_backdrop(), answer_cards(),
                 question_card("With rinderpest gone: more trees or fewer trees?", y=-3.15, color=INK))
        ring, run = countdown(5, center=[6.0,-3.0,0])
        self.add(ring)
        self.play(run)


def evidence_chain(stage=0):
    texts = ["rinderpest gone", "more wildebeest", "more grass eaten", "fewer fires", "more trees"]
    cols = [GREEN if i <= stage else DARK_GREY for i in range(5)]
    boxes = VGroup()
    for text, col in zip(texts, cols):
        txt = fit_text(text, max_w=2.0, size=24, min_size=24, max_lines=2, color=col)
        box = RoundedRectangle(corner_radius=.12, width=2.28, height=.92, stroke_color=col,
                               stroke_width=2.5, fill_color=col, fill_opacity=.10)
        txt.move_to(box)
        boxes.add(VGroup(box, txt))
    boxes.arrange(RIGHT, buff=.18).move_to([0,2.85,0])
    return boxes


class S12Reveal(SpokenScene):
    def construct(self):
        world = savanna_world(3,4)
        cards = answer_cards()
        self.add(world,cards)
        self.at("More trees")
        self.play(Indicate(cards[0],color=ALGA,scale_factor=1.15),FadeOut(cards[1]),run_time=.7)
        chain = evidence_chain(0)
        self.at("decades of records")
        self.play(FadeOut(cards[0]),FadeIn(chain),run_time=.8)
        more_world = savanna_world(3,8)
        self.at("wildebeest numbers rose")
        self.play(FadeOut(world[4]),FadeIn(more_world[4]),Transform(chain,evidence_chain(1)),run_time=1.0)
        short = savanna_world(3,8,short_grass=True)
        self.at("ate more grass")
        self.play(Transform(world[3],short[3]),Transform(chain,evidence_chain(2)),run_time=1.0)
        self.add(scope_tag("schematic", color=DARK_GREY))
        bob(more_world[4],amp=.035,speed=1.2)
        self.finish()


class S13Fire(SpokenScene):
    def construct(self):
        world = savanna_world(3,8,short_grass=True)
        chain = evidence_chain(2)
        self.add(world,chain)
        fires = VGroup(*[Triangle(color=ORANGE,fill_color=ORANGE,fill_opacity=.75).scale(.3).move_to(p)
                         for p in [[-4,-2.1,0],[-1.5,-2.0,0],[1,-2.2,0],[3.5,-2.0,0]]])
        self.at("fuel for fires")
        self.play(FadeIn(fires),run_time=.6)
        self.at("Fewer fires burned")
        self.play(FadeOut(fires[1:]),fires[0].animate.scale(.5),Transform(chain,evidence_chain(3)),run_time=.9)
        greener = savanna_world(7,8,short_grass=True,green=True)
        self.at("more young trees survived")
        self.play(FadeIn(greener[5][3:]),Transform(world[1],greener[1]),Transform(chain,evidence_chain(4)),run_time=1.1)
        supported = caption("records + computer models supported this chain",color=INK,size=28)
        self.at("analysis supported")
        self.play(FadeIn(supported),run_time=.7)
        self.add(scope_tag("schematic", color=DARK_GREY))
        bob(world[4],amp=.035,speed=1.1)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        self.add(cream_ground())
        tp = TwoPanel("flask scale", "landscape scale", colors=(WATER,ALGA), top=3.05,bottom=-2.45)
        left = VGroup(alga([0,.35,0],.65),bacterium([-.7,-.55,0],1.0),
                      *[nutrient(p,c,.1) for p,c in [([-.7,.6,0],GREEN),([.65,.4,0],ORANGE),([.45,-.5,0],GREEN)]])
        right = VGroup(tree([-1,0,0],.8),tree([.8,.1,0],1.0),animal([0,-.8,0],scale=.7))
        tp.put(left,"left"); tp.put(right,"right")
        self.at("Two scales")
        self.play(FadeIn(tp),run_time=.7)
        self.at("In the flask")
        self.play(FadeIn(left),run_time=.8)
        lcap = label("matter moves on",32,GREEN).move_to([-3.25,-1.95,0])
        self.play(FadeIn(lcap),run_time=.5)
        self.at("On the savannah")
        self.play(FadeIn(right),run_time=.8)
        rcap = label("populations change",32,ALGA).move_to([3.25,-1.95,0])
        self.play(FadeIn(rcap),run_time=.5)
        rule = caption("RECYCLE AND RESHAPE",size=34,color=INK)
        self.at("Viruses that burst")
        self.play(FadeIn(rule),Indicate(left,color=GREEN),run_time=.8)
        self.at("Pathogens can reshape")
        self.play(Indicate(right,color=ALGA),run_time=.8)
        bob(left,amp=.04,speed=1.1); bob(right,amp=.04,speed=1.3)
        self.finish()


class S15End(EndCard):
    LINE = "Viruses that burst cells can recycle matter; pathogens can reshape ecosystems."
