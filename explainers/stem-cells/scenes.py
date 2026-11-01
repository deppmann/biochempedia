"""Stem cells: chance decides which stem cell wins  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a stem cell, unlabelled (plain)
  GREY   = crypt outline, differentiated / short-lived cells, structure
  GREEN  = the label: the tamoxifen-induced mark, a labelled clone, labelled cells in the model
  YELLOW = tamoxifen (the drug) and the highlighted dividing step
  PURPLE, ORANGE, PINK = the other reporter colours (clones of a different colour)
  RED    = lost / crossed out / not shown
  TEAL   = the arithmetic and the plotted curve
  GOLD   = the open question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E87FB0"
CLONE = [GREEN, PURPLE, ORANGE, PINK]

CX = -3.3                 # crypt centre x
R = 2.0                   # crypt half width
CC = -1.3                 # y of the centre of the crypt's rounded bottom
TOP = CC + 3.6            # top of the crypt walls


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def crypt(cx=CX, k=1.0, h=3.6):
    r_ = R * k
    cc = -3.3 + r_
    left = Line([cx - r_, cc + h, 0], [cx - r_, cc, 0], color=GREY, stroke_width=5)
    arc = Arc(radius=r_, start_angle=PI, angle=PI, arc_center=[cx, cc, 0], color=GREY, stroke_width=5)
    right = Line([cx + r_, cc, 0], [cx + r_, cc + h, 0], color=GREY, stroke_width=5)
    return VGroup(left, arc, right)


def base_pos(cx=CX, k=1.0):
    cc = -3.3 + R * k
    return [np.array([cx + 1.45 * k * np.cos(np.radians(a)), cc + 1.45 * k * np.sin(np.radians(a)), 0]) for a in (190, 230, 270, 310, 350)]


def cell(color=BLUE, r=0.4, fill=0.35, sw=4):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


def rise_pos(cx=CX):
    return [[np.array([cx + dx, CC + 1.05 + 0.75 * k, 0]) for dx in (-1.2, -0.4, 0.4, 1.2)] for k in range(4)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross(mob, color=RED, w=7):
    d = 0.5 * mob.width
    h = 0.5 * mob.height
    c = mob.get_center()
    return VGroup(Line(c + [-d, h, 0], c + [d, -h, 0], color=color, stroke_width=w),
                  Line(c + [-d, -h, 0], c + [d, h, 0], color=color, stroke_width=w))



MINI_W, MINI_H = 0.68, 0.46
PITCH_X, PITCH_Y = 0.76, 0.58

def division(cx, ytop, c_parent, c1, c2, r=0.6, dx=1.0, drop=2.3):
    p = cell(c_parent, r).move_to([cx, ytop, 0])
    d1 = cell(c1, r).move_to([cx - dx, ytop - drop, 0])
    d2 = cell(c2, r).move_to([cx + dx, ytop - drop, 0])
    a1 = arr(p.get_bottom(), d1.get_top(), GREY, w=4, tip=0.2)
    a2 = arr(p.get_bottom(), d2.get_top(), GREY, w=4, tip=0.2)
    return p, d1, d2, a1, a2

def bars_for(colors_state, x0=1.4):
    """rows of horizontal bars: cells per clone colour (computed from the crypt's current state)."""
    order = [GREEN, PURPLE, ORANGE, PINK, BLUE]
    g = VGroup()
    for i, c_ in enumerate(order):
        n = sum(1 for s in colors_state if s == c_)
        w = max(0.001, 0.62 * n)
        b = Rectangle(width=w, height=0.38, stroke_width=0 if n == 0 else 2, stroke_color=c_, fill_color=c_, fill_opacity=0.55)
        b.move_to([x0 + w / 2, 1.05 - 0.62 * i, 0])
        g.add(b)
    return g

def swatches(x0=0.9):
    return VGroup(*[Circle(radius=0.17, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.35).move_to([x0, 1.05 - 0.62 * i, 0])
                    for i, c_ in enumerate([GREEN, PURPLE, ORANGE, PINK, BLUE])])

def mini_crypt():
    box = RoundedRectangle(corner_radius=0.1, width=MINI_W, height=MINI_H, stroke_color=GREY, stroke_width=2)
    dots = VGroup(*[Dot([(i - 2) * 0.118, 0, 0], radius=0.05, color=BLUE) for i in range(5)])
    return VGroup(box, dots)

def small_base():
    """Three illustrative cells, using the original crypt geometry."""
    return VGroup(*[cell(BLUE, 0.38).move_to(base_pos()[i]) for i in (1, 2, 3)])


def stream():
    return VGroup(*[cell(GREY, 0.32).move_to([CX, y, 0]) for y in (-0.6, 0.8, 2.2)])


def tag(text, x, y, color=TEXT, size=28):
    return T(text, size, color, line_spacing=0.85).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Stem cells and tissue renewal"
    TITLE = "How Stem Cells Keep a Tissue New"


class S01Lead(SpokenScene):
    def construct(self):
        cr, flow = crypt(), stream()
        name = tag("mouse small intestine", 3.3, 2.9, GREY, 26)
        renew = tag("new lining\nevery few days", 3.3, 1.3, size=36)
        self.at("The lining")
        self.play(Create(cr), FadeIn(flow), FadeIn(name), FadeIn(renew), run_time=0.8)
        self.at("replaced every few days")
        self.play(flow.animate.shift(UP * 0.7), run_time=0.65)
        self.play(FadeOut(flow[-1], shift=UP * 0.5), run_time=0.4)
        self.at("Yet the animal")
        life = tag("kept for life", 3.3, -0.5, size=36)
        self.play(FadeIn(life), run_time=0.6)
        base = small_base()
        self.at("Stem cells make")
        self.play(FadeIn(base, scale=0.8), run_time=0.6)
        self.at("bottom of pockets")
        cryptlabel = tag("crypt", -3.3, 3, GREY)
        self.play(FadeIn(cryptlabel), Indicate(base, color=GOLD), run_time=0.6)
        self.at("They keep making")
        up = arr([-1.0, -2.1, 0], [0.4, 0.8, 0], BLUE)
        output = tag("makes specialized cells", 3.3, 0.9, GREY, 28)
        self.play(FadeOut(VGroup(renew, life, name)), GrowArrow(up), FadeIn(output),
                  flow[0].animate.move_to([CX, 0, 0]), flow[1].animate.move_to([CX, 1.6, 0]), run_time=0.8)
        self.at("And they keep")
        loop = CurvedArrow([-2.5, -2.0, 0], [-2.7, -2.8, 0], angle=-PI*1.5, color=BLUE)
        own = tag("makes more stem cells", 3.3, -1.6, BLUE)
        self.play(Create(loop), FadeIn(own), Indicate(base, color=BLUE), run_time=0.8)
        self.at("tested over time")
        time = bchip("tested over time", TEAL, 28).move_to([3.3, -3, 0])
        self.play(FadeIn(time), run_time=0.6)
        self.finish()


class S02Trace(SpokenScene):
    def construct(self):
        cr, base, flow = crypt(), small_base(), stream()
        self.add(cr, base, flow)
        question = tag("Which cells do it?", 3.3, 1.6, GOLD, 36)
        self.at("How would you prove")
        self.play(FadeIn(question), run_time=0.6)
        note = tag("gene expression\nis not fate", 3.3, 0, size=32)
        self.at("Expressing a gene")
        self.play(FadeIn(note), run_time=0.6)
        self.at("scientists trace cells")
        self.play(Indicate(base[1], color=GREEN), run_time=0.7)
        tam = bchip("tamoxifen", YELLOW, 28).move_to([3.3, -2.3, 0])
        a = arr(tam.get_left(), [-2.8, -2.7, 0], YELLOW)
        self.at("drug tamoxifen")
        self.play(FadeOut(note), FadeIn(tam), GrowArrow(a), run_time=0.65)
        mark = tag("Lgr5 cell: permanent mark", 3.3, -0.4, GREEN, 26)
        self.at("permanent mark")
        self.play(base[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.65), FadeIn(mark), run_time=0.6)
        self.at("Every daughter inherits")
        self.play(*[c.animate.set_stroke(GREEN).set_fill(GREEN, 0.6) for c in flow], run_time=0.9)
        bar = Line([0.6, 2.2, 0], [6.0, 2.2, 0], color=GREY)
        ends = VGroup(tag("day 0", 1, 2.7, GREY, 24), tag("day 60", 5.5, 2.7, GREY, 24))
        dot = Dot([0.6, 2.2, 0], color=GREEN)
        self.at("Over 60 days")
        self.play(FadeOut(VGroup(question, tam, a, mark)), Create(bar), FadeIn(ends), FadeIn(dot), run_time=0.6)
        ribbon = RoundedRectangle(width=0.8, height=5.0, corner_radius=0.3, stroke_width=0,
                                  fill_color=GREEN, fill_opacity=0.2).move_to([CX, -0.2, 0]).set_z_index(-1)
        self.at("label filled ribbons")
        self.play(dot.animate.move_to([6.0, 2.2, 0]), FadeIn(ribbon), run_time=1.3)
        # Schematic epithelial cell icons; each carries its own type label.
        icons = VGroup()
        for y, label, shape in zip((0.95, 0.0, -0.95, -1.9),
                                   ("absorptive", "goblet", "enteroendocrine", "Paneth"),
                                   (Rectangle(width=.45, height=.6), Circle(radius=.28), Triangle().scale(.28), Square(side_length=.48))):
            shape.set_stroke(GREEN, 3).set_fill(GREEN, .35).move_to([1.2, y, 0])
            icons.add(VGroup(shape, T(label, 24, GREEN).next_to(shape, RIGHT, buff=.3)))
        self.at("every kind of epithelial")
        self.play(FadeIn(icons), run_time=0.8)
        multi = bchip("multipotent within the gut", GREEN, 26).move_to([3.3, -0.1, 0])
        self.at("That shows multipotency")
        self.play(FadeOut(icons), FadeIn(multi), run_time=0.6)
        plu = bchip("pluripotent", RED, 28).move_to([3.3, -1.7, 0])
        self.at("It does not show")
        self.play(FadeIn(plu), Create(cross(plu)), run_time=0.7)
        self.finish()


class S03Pool(SpokenScene):
    def construct(self):
        cr = crypt(-3.4, 1.25, 2.6)
        pos = base_pos(-3.4, 1.25)
        state = [GREEN, PURPLE, ORANGE, PINK, GREEN]
        cells = [cell(c, .45).move_to(p) for c, p in zip(state, pos)]
        head = tag("How does the pool\nstay the same size?", 3.1, 2.3, size=32)
        self.at("How does the pool")
        self.play(Create(cr), FadeIn(VGroup(*cells)), FadeIn(head), run_time=.8)
        clock = VGroup(Circle(radius=.36, color=GREY), Line(ORIGIN, UP*.26, color=TEXT),
                       Line(ORIGIN, RIGHT*.18, color=TEXT)).move_to([-5.7, 2.8, 0])
        clock_t = tag("about once a day", -3.1, 2.8, GREY, 24)
        self.at("divide about once a day")
        self.play(FadeIn(clock), FadeIn(clock_t), run_time=.5)
        self.play(Rotate(clock[1], -TAU, about_point=clock[0].get_center()), run_time=.6)
        p, d1, d2, a1, a2 = division(3.1, 1.1, BLUE, BLUE, BLUE, r=.42, dx=.9, drop=1.4)
        sym = tag("symmetric division", 3.1, -1.2, BLUE, 26)
        self.at("most divisions are symmetric")
        self.play(FadeOut(head), FadeIn(p), run_time=.3)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(d1), FadeIn(d2), FadeIn(sym), run_time=.7)
        chance = tag("stay or leave\nby chance", 3.1, .7, size=32)
        self.at("Daughters stay or leave")
        self.play(FadeOut(VGroup(p,d1,d2,a1,a2,sym)), FadeIn(chance), run_time=.5)
        # An illustrative neighbour-copy trajectory, not a measured time series.
        def replace(src, dst):
            new = cells[src].copy().move_to(cells[dst])
            moving = cells[src].copy()
            self.add(moving)
            self.play(moving.animate.move_to(cells[dst]), FadeOut(cells[dst], shift=UP*.7), run_time=.4)
            self.remove(moving)
            self.add(new)
            cells[dst] = new
        self.at("Some clones take over")
        replace(0,1); replace(4,3)
        self.at("while others vanish")
        replace(1,2)
        self.play(Indicate(VGroup(*cells), color=GREEN, scale_factor=1.04), run_time=.5)
        balance = bchip("population balance", TEAL, 30).move_to([3.1, -1.4, 0])
        self.at("The population keeps the balance")
        self.play(FadeOut(chance), FadeIn(balance), run_time=.6)
        self.finish()


class S04Niche(SpokenScene):
    def construct(self):
        cr, base = crypt(), small_base()
        self.add(cr, base)
        q = tag("Stay or leave?", 3.2, 2.6, GOLD, 36)
        self.at("What tells a daughter")
        self.play(FadeIn(q), run_time=.6)
        niche = bchip("niche = neighbours", TEXT, 28).move_to([3.2, 1.1, 0])
        self.at("Its neighbors")
        self.play(FadeIn(niche), run_time=.6)
        # Signals use labelled translucent fields rather than molecular drawings.
        wnt = VGroup(*[Rectangle(width=3.3, height=.55, stroke_width=0, fill_color=BLUE,
                                 fill_opacity=.3*(1-i/6)).move_to([CX, -2.25+i*.55, 0]) for i in range(6)]).set_z_index(-2)
        wt = tag("Wnt: stay stem", 3.2, -.3, BLUE, 28)
        self.at("signals keep cells")
        self.play(FadeIn(wnt), FadeIn(wt), Indicate(base, color=BLUE), run_time=.7)
        bmp = VGroup(*[Rectangle(width=3.3, height=.5, stroke_width=0, fill_color=GREY,
                                 fill_opacity=.05+i*.045).move_to([CX, -.1+i*.5, 0]) for i in range(5)]).set_z_index(-1)
        bt = tag("BMP: specialize", 3.2, -1.4, GREY, 28)
        self.at("Higher up")
        self.play(FadeIn(bmp), FadeIn(bt), run_time=.7)
        self.at("cells help stem cells grow")
        self.play(FadeOut(VGroup(q,niche,wt,bt,wnt,bmp)), run_time=.35)
        dish = Arc(radius=1.25, start_angle=PI, angle=PI, color=GREY).move_to([3.2,-.2,0])
        pan = cell(GREY, .35).move_to([2.6,-.2,0])
        sc = cell(BLUE,.35).move_to([3.7,-.2,0])
        dishlabel = tag("Paneth + stem cell\nin a dish",3.2,1.5,size=28)
        self.play(Create(dish), FadeIn(pan), FadeIn(sc), FadeIn(dishlabel), run_time=.6)
        self.play(sc.animate.scale(1.25), run_time=.5)
        self.at("But in the living gut")
        living = tag("living gut",3.2,2.4,size=32)
        pan2 = cell(GREY,.3).move_to([-3.3,-1.6,0])
        pl = tag("Paneth",-3.3,-.7,GREY,24)
        self.play(FadeOut(VGroup(dish,pan,sc,dishlabel)),FadeIn(living),FadeIn(pan2),FadeIn(pl),run_time=.6)
        self.at("survived without them")
        survives = tag("stem cells persist",3.2,1.1,BLUE,28)
        self.play(FadeOut(VGroup(pan2,pl)),FadeIn(survives),Indicate(base,color=BLUE),run_time=.7)
        tel = Ellipse(width=3.3,height=.28,color=BLUE,fill_opacity=.25).move_to([CX,-3.55,0])
        source = tag("Wnt from beneath the lining",2.8,-1.4,BLUE,26)
        a = arr([-1.7,-3.4,0],[-1,-2.3,0],BLUE)
        self.at("cells beneath the lining")
        self.play(FadeIn(tel),FadeIn(source),GrowArrow(a),run_time=.6)
        off = cross(a,w=4)
        drop = tag("Wnt off → less proliferation",2.8,-2.7,RED,24)
        self.at("was needed")
        self.play(FadeOut(survives), Create(off),a.animate.set_opacity(.15),FadeIn(drop),run_time=.5)
        self.at("more than one source")
        self.play(Indicate(source,color=BLUE),run_time=.6)
        self.finish()


class S05Injury(SpokenScene):
    def construct(self):
        cr,base = crypt(),small_base()
        progenitors = VGroup(*[cell(GREY,.38).move_to([x,-.5,0]) for x in (-4.3,-3.3,-2.3)])
        label = tag("progenitor cells",3.2,1.3,GREY,30)
        self.at("Fates are less fixed")
        self.play(Create(cr),FadeIn(base),FadeIn(progenitors),run_time=.7)
        self.at("stem cells were killed")
        self.play(base.animate.set_opacity(.15),run_time=.2)
        self.play(base.animate.set_opacity(1),run_time=.2)
        self.play(FadeOut(base),run_time=.3)
        self.at("Progenitor cells")
        self.play(FadeIn(label),Indicate(progenitors,color=GREY),run_time=.6)
        fates = tag("toward absorptive\nor secretory cells",3.2,-.1,GREY,28)
        self.at("on their way to becoming")
        self.play(progenitors.animate.shift(UP*.45),FadeIn(fates),run_time=.7)
        back = CurvedArrow([-1.8,.1,0],[-2.5,-2.7,0],angle=-PI/2,color=BLUE)
        reset = tag("back to stem state",3.2,-1.6,BLUE,28)
        self.at("went back and rebuilt")
        self.play(Create(back),FadeIn(reset),run_time=.4)
        self.play(*[c.animate.move_to(p).set_stroke(BLUE).set_fill(BLUE,.35)
                    for c,p in zip(progenitors,[base_pos()[i] for i in (1,2,3)])],run_time=1)
        injury = bchip("after injury only",YELLOW,30).move_to([3.2,2.8,0])
        self.at("That is an injury result")
        self.play(FadeIn(injury),run_time=.6)
        caution = tag("not an everyday role\nfor mature cells",3.2,.4,TEXT,28)
        self.at("It does not mean")
        self.play(FadeOut(VGroup(label,fates)),FadeIn(caution),run_time=.6)
        self.finish()


class S06Reset(SpokenScene):
    def construct(self):
        question = tag("How far back can a cell go?",0,3.1,GOLD,36)
        self.at("How far back")
        self.play(FadeIn(question),run_time=.6)
        gh = tag("Gurdon · 1962",-3.4,2.1,GREY,28)
        egg = cell(GREY,.85).move_to([-3.4,.1,0])
        el = tag("egg without\nits own nucleus",-3.4,-1.3,GREY,24)
        nucleus = Dot([-5.7,1.2,0],radius=.18,color=BLUE)
        nl = tag("gut-cell nucleus",-4.8,2.65,BLUE,24)
        pipette = VGroup(Line([-6.1,1.55,0],[-4.7,.55,0],color=GREY,stroke_width=5),
                         Line([-6.2,1.35,0],[-4.7,.55,0],color=GREY,stroke_width=3))
        self.at("In 1962")
        self.play(FadeIn(gh),FadeIn(egg),FadeIn(el),run_time=.6)
        self.at("put a nucleus")
        self.play(FadeIn(nucleus),FadeIn(nl),Create(pipette),run_time=.6)
        self.at("into a frog egg")
        self.play(nucleus.animate.move_to(egg.get_center()),pipette.animate.shift(RIGHT*.4+DOWN*.2),run_time=.9)
        # Qualitative outcomes: no invented numerical success fraction.
        failed = VGroup(*[VGroup(cell(GREY,.23),cross(cell(GREY,.23),w=3)).move_to([x,-2.5,0])
                          for x in (-5,-4.2,-3.4)])
        outcome = tag("most failed",-4.2,-3.15,RED,24)
        tad = VGroup(Ellipse(width=.55,height=.32,color=BLUE,fill_opacity=.5),
                     CubicBezier([.2,0,0],[.5,.4,0],[.8,-.3,0],[1,.1,0],color=BLUE)).move_to([-2,-2.4,0])
        self.at("A small fraction")
        self.play(FadeOut(VGroup(pipette,nl)),FadeIn(failed),FadeIn(outcome),FadeIn(tad),run_time=.7)
        self.play(tad.animate.shift(RIGHT*.4),run_time=.6)
        yh = tag("Yamanaka lab · 2006",3.3,2.1,GREY,28)
        fibro = Ellipse(width=2,height=.7,color=GREY,fill_opacity=.3).rotate(.25).move_to([3.2,.2,0])
        fl = tag("mouse fibroblast",3.2,-.9,GREY,26)
        self.at("In 2006")
        self.play(FadeOut(VGroup(egg,el,nucleus,failed,outcome)),FadeIn(yh),FadeIn(fibro),FadeIn(fl),run_time=.6)
        factors = VGroup(*[bchip(str(i+1),YELLOW,22).move_to([1.6+i*1.05,1.15,0]) for i in range(4)])
        ft = tag("four transcription factors",3.2,2.9,YELLOW,24)
        self.at("four transcription factors")
        self.play(FadeOut(question),FadeIn(factors),FadeIn(ft),run_time=.6)
        self.at("turn mouse fibroblasts")
        self.play(*[f.animate.move_to(fibro.get_center()).set_opacity(0) for f in factors],run_time=.9)
        plur = cell(BLUE,.7).move_to([3.2,.2,0])
        layers = VGroup(*[VGroup(cell(GREY,.2).move_to([x,-1.6,0]),
                                tag(t,x,-2.1,GREY,22))
                          for x,t in ((1.2,"ectoderm"),(3.2,"mesoderm"),(5.2,"endoderm"))])
        self.at("into pluripotent cells")
        self.play(Transform(fibro,plur),ReplacementTransform(fl,tag("pluripotent",3.2,-.9,BLUE,26)),FadeIn(layers),run_time=.7)
        self.at("Specialized cells can be reset")
        reset = tag("specialized state → reset",-3.2,.4,BLUE,30)
        self.play(FadeOut(VGroup(gh,tad)),FadeIn(reset),run_time=.7)
        no = bchip("not totipotent",RED,28).move_to([-3.2,-1.2,0])
        self.at("Pluripotent is not totipotent")
        self.play(FadeIn(no),run_time=.6)
        safe = bchip("not proof of safety",RED,28).move_to([-3.2,-2.6,0])
        self.at("passing these tests")
        self.play(FadeIn(safe),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Stem cells make every lining cell type and keep their numbers."
