"""Neurulation and neural tube defects: the folds must be able to meet  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the neural plate / neural tube / the cells of the plate
  ORANGE = skin (the epidermis beside and over the plate)
  YELLOW = movement and reach: the folds' motion, hinge, cells in the act of pushing in
  TEAL   = planar cell polarity / Dishevelled signaling (the sideways sense of direction)
  RED    = disrupted, too far apart, open, failed
  GREEN  = meets, fused, closed, normal
  GREY   = labels, outlines, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
OY = 0.9          # y of the skin line in the cross-section
HALF = 6.2        # half-length of the skin line


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def sec(a, d, half=HALF, oy=OY, sc=1.0, cx=0.0):
    """Cross-section of the embryo's back. Skin (orange) either side; the plate (blue) is a groove
    whose edges (the fold tips) sit at x = +-a on the skin line and whose floor is d below it."""
    a = max(a, 0.02)
    plate = ParametricFunction(lambda p: np.array([a * np.cos(p), -d * np.sin(p), 0]),
                               t_range=[0, PI, PI / 60], color=BLUE, stroke_width=20)
    sl = Line([-half, 0, 0], [-a, 0, 0], color=ORANGE, stroke_width=9)
    sr = Line([a, 0, 0], [half, 0, 0], color=ORANGE, stroke_width=9)
    g = VGroup(sl, sr, plate)
    g.scale(sc, about_point=ORIGIN).shift([cx, oy, 0])
    return g


def tube(r=1.6, drop=0.0, half=HALF, oy=OY, sc=1.0, cx=0.0):
    """Closed tube: skin continuous over the top; tube a circle, drop below the skin (a gap if drop > 0)."""
    plate = ParametricFunction(lambda p: np.array([r * np.sin(p), -r - drop + r * np.cos(p), 0]),
                               t_range=[0, TAU, TAU / 80], color=BLUE, stroke_width=20)
    sl = Line([-half, 0, 0], [0, 0, 0], color=ORANGE, stroke_width=9)
    sr = Line([0, 0, 0], [half, 0, 0], color=ORANGE, stroke_width=9)
    g = VGroup(sl, sr, plate)
    g.scale(sc, about_point=ORIGIN).shift([cx, oy, 0])
    return g


def lab(text, color=TEXT, size=30, **kw):
    return T(text, size, color, **kw)


def darr(p, q, color=GREY, w=4):
    return DoubleArrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.22,
                       max_tip_length_to_length_ratio=0.3)


def parr(p, q, color=YELLOW, w=6):
    return Arrow(p, q, buff=0, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.4)


def flash(self, pt, color=GREEN, r=0.5):
    ring = Circle(radius=0.12, color=color, stroke_width=6).move_to(pt)
    self.play(ring.animate.scale(r / 0.12).set_stroke(opacity=0), run_time=0.6)
    self.remove(ring)


class S00Title(TitleCard):
    LESSON = "Neurulation and neural tube defects"
    TITLE = "If the Neural Tube Does Not Close"


# ---------------------------------------------------------------------------------------------
def bar_over(x0, x1, color=RED, y=OY + 0.5):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=12)


def heading(text, color=TEXT):
    return lab(text, color, 32).move_to([0, 3.15, 0])


def site_map():
    """Schematic axial map: locations, not a single embryo with both defects."""
    head = Arc(radius=0.78, start_angle=0.3, angle=PI-0.6,
               color=BLUE, stroke_width=12).move_to([0, 1.55, 0])
    cord = VGroup(Line([-0.4, 1.25, 0], [-0.4, -2.0, 0], color=BLUE, stroke_width=10),
                  Line([0.4, 1.25, 0], [0.4, -2.0, 0], color=BLUE, stroke_width=10))
    axis = DashedLine([0, 0.9, 0], [0, -1.5, 0], color=GREY, stroke_width=2)
    ends = VGroup(lab("head", GREY, 24).move_to([-1.5, 1.9, 0]),
                  lab("lower end", GREY, 24).move_to([-1.8, -1.85, 0]))
    return VGroup(head, cord, axis, ends)


def open_site(y):
    return DashedVMobject(Ellipse(width=1.9, height=1.0, color=RED, stroke_width=4),
                         num_dashes=16).move_to([0, y, 0])


def cell_patch(long=False):
    # Six representative cells, with no biological cell count implied.
    pts = ([(-0.6, 1.3), (0.6, 1.3), (-0.6, 0), (0.6, 0),
            (-0.6, -1.3), (0.6, -1.3)] if long else
           [(-1.7, 0.65), (0, 0.65), (1.7, 0.65),
            (-1.7, -0.65), (0, -0.65), (1.7, -0.65)])
    return VGroup(*[RoundedRectangle(corner_radius=0.18, width=1.1, height=1.05,
                      stroke_color=BLUE, stroke_width=3.5,
                      fill_color=BLUE, fill_opacity=0.28).move_to([x,y,0]) for x,y in pts])


class S01Flat(SpokenScene):
    def construct(self):
        m = site_map()
        title = heading("Where closure fails")
        self.at("If the neural tube")
        self.play(FadeIn(m), FadeIn(title), run_time=0.6)
        h, l = open_site(1.75), open_site(-1.85)
        hl = lab("anencephaly", RED, 30).move_to([3.4, 1.8, 0])
        ll = lab("open spina bifida", RED, 30).move_to([3.4, -1.8, 0])
        self.at("head end")
        self.play(Create(h), FadeIn(hl), run_time=0.6)
        self.at("lower end")
        self.play(Create(l), FadeIn(ll), run_time=0.6)
        stakes = lab("Fatal outcomes • weakness • paralysis", RED, 28).move_to([0,-3.05,0])
        self.at("These defects")
        self.play(FadeIn(stakes), run_time=0.5)
        self.at("Closure happens")
        timeline = Line([-5.8,0,0], [5.8,0,0], color=GREY, stroke_width=4)
        conception = VGroup(Line([-1.7,-0.2,0],[-1.7,0.2,0],color=GREY),
                             lab("conception", GREY, 26).move_to([-1.7,-0.7,0]))
        closure = VGroup(Line([4.5,-0.2,0],[4.5,0.2,0],color=GREEN),
                         lab("closure by about week 4", GREEN, 26).move_to([3.4,0.75,0]),
                         lab("after fertilization", GREY, 24).move_to([3.4,1.35,0]))
        self.play(FadeOut(VGroup(m,title,h,l,hl,ll,stakes)), Create(timeline),
                  FadeIn(conception), FadeIn(closure), run_time=0.8)
        early = lab("Often before pregnancy is recognized", TEXT, 28).move_to([0,-2.0,0])
        self.at("often before")
        self.play(FadeIn(early), run_time=0.5)
        folic = chip("folic acid", GREEN, 28).move_to([-4.5,0.9,0])
        marker = parr([-4.5,0.45,0],[-4.5,0.08,0],GREEN)
        self.at("Folic acid")
        self.play(FadeIn(folic), GrowArrow(marker), run_time=0.6)
        lower = lab("Lower risk • incomplete protection", GREEN, 28).move_to([0,-3.0,0])
        self.at("lowers the risk")
        self.play(FadeIn(lower), run_time=0.5)
        self.finish()


class S02Fold(SpokenScene):
    def construct(self):
        s = sec(2.8,0,oy=0.1)
        title = heading("Neural plate → neural tube")
        self.at("The brain")
        self.play(FadeIn(s), FadeIn(title), run_time=0.5)
        name = lab("neural plate", BLUE, 30).move_to([0,0.9,0])
        self.at("neural plate")
        self.play(FadeIn(name), run_time=0.4)
        inset = RoundedRectangle(width=2.7,height=0.8,corner_radius=0.15,
                                 color=BLUE,fill_color=BLUE,fill_opacity=0.25).move_to([4.3,1.9,0])
        inset_l = lab("top view", GREY, 24).move_to([4.3,2.95,0])
        self.at("It narrows")
        self.play(FadeIn(inset), FadeIn(inset_l), Transform(s,sec(1.8,0,oy=0.1)), run_time=0.45)
        self.play(inset.animate.stretch(0.5,0).stretch(2.1,1), run_time=0.65)
        self.at("It creases")
        wedge = Polygon([0,-0.75,0],[-0.3,-1.35,0],[0.3,-1.35,0],
                        color=YELLOW,fill_opacity=0.35)
        hinge = lab("hinge point",YELLOW,26).move_to([0,-1.9,0])
        self.play(Transform(s,sec(1.7,1.0,oy=0.1)),FadeIn(wedge),FadeIn(hinge),
                  FadeOut(inset),FadeOut(inset_l),run_time=0.65)
        self.at("edges rise")
        folds = lab("neural folds",BLUE,30).move_to([0,0.9,0])
        self.play(Transform(s,sec(1.15,2.0,oy=0.1)),ReplacementTransform(name,folds),
                  FadeOut(wedge),FadeOut(hinge),run_time=0.8)
        self.at("folds meet")
        self.play(Transform(s,sec(0.03,2.6,oy=0.1)), run_time=0.4)
        self.at("fuse")
        self.play(Transform(s,tube(1.3,oy=0.1)), run_time=0.5)
        self.at("tube separates")
        skin = lab("skin",ORANGE,28).move_to([4.8,0.8,0])
        tl = lab("neural tube",BLUE,30).move_to([4.0,-1.8,0])
        self.play(Transform(s,tube(1.3,drop=0.35,oy=0.1)),FadeOut(folds),FadeIn(tl),run_time=0.8)
        self.at("seals over")
        self.play(FadeIn(skin),Indicate(s[0:2],color=ORANGE,scale_factor=1),run_time=0.6)
        self.finish()


class S03Defects(SpokenScene):
    def construct(self):
        m = site_map().shift(LEFT*3)
        h = open_site(1.75).shift(LEFT*3)
        title = heading("Anencephaly",RED)
        tissue = Ellipse(width=1.25,height=0.6,color=BLUE,fill_color=BLUE,
                         fill_opacity=0.55).move_to([-3,1.75,0])
        self.at("In anencephaly")
        self.play(FadeIn(m),FadeIn(h),FadeIn(title),FadeIn(tissue),run_time=0.4)
        exposed = lab("exposed brain tissue",BLUE,30).move_to([2.5,1.5,0])
        self.at("exposed brain tissue")
        self.play(FadeIn(exposed),run_time=0.4)
        self.at("degenerates")
        self.play(tissue.animate.scale(0.2).set_opacity(0.1),run_time=0.65)
        outcome = lab("Stillborn or death\nsoon after birth",RED,30).move_to([2.5,-0.3,0])
        self.at("Affected babies")
        self.play(FadeIn(outcome),run_time=0.5)
        self.at("In one form")
        lesion = open_site(-1.85).shift(LEFT*3)
        lesion_cord = Line([-3,-1.25,0],[-3,-2.15,0],color=BLUE,stroke_width=15)
        newtitle = heading("Open spina bifida",RED)
        form = lab("myelomeningocele",RED,30).move_to([2.5,1.5,0])
        self.play(FadeOut(VGroup(h,tissue,exposed,outcome)),ReplacementTransform(title,newtitle),
                  FadeIn(lesion),FadeIn(form),run_time=0.6)
        self.at("cord lies")
        cord_l = lab("cord in the open lesion",BLUE,26).move_to([2.5,0.45,0])
        self.play(Create(lesion_cord),FadeIn(cord_l),run_time=0.55)
        consequence = lab("Weakness or paralysis\nLoss of bladder and bowel control",RED,26).move_to([1.8,-1.45,0])
        self.at("Weakness or paralysis")
        self.play(FadeIn(consequence),run_time=0.65)
        self.finish()


class S03Prevention(SpokenScene):
    def construct(self):
        title = heading("Randomized prevention trials")
        self.at("Randomized trials")
        self.play(FadeIn(title),run_time=0.5)
        pop = lab("RECURRENCE\nPrevious affected pregnancy",TEXT,30).move_to([0,2.0,0])
        self.at("previous affected pregnancy")
        self.play(FadeIn(pop),run_time=0.5)
        treatment = chip("folic acid before conception",GREEN,28).move_to([0,0.8,0])
        self.at("folic acid started")
        self.play(FadeIn(treatment),run_time=0.5)
        base = Rectangle(width=7,height=0.45,stroke_color=GREY,fill_color=GREY,fill_opacity=0.5).move_to([0,-0.5,0])
        reduced = Rectangle(width=7*0.28,height=0.45,stroke_color=GREEN,fill_color=GREEN,fill_opacity=0.65).align_to(base,LEFT)
        reduction = lab("≈72% relative reduction in recurrence",GREEN,32).move_to([0,-1.7,0])
        self.at("cut recurrence")
        self.play(FadeIn(base),run_time=0.35)
        self.at("about 72")
        self.play(Transform(base,reduced),FadeIn(reduction),run_time=0.7)
        self.at("A Hungarian trial")
        first = heading("Hungarian trial • first occurrence")
        left = lab("Multivitamin\ncontaining folic acid",GREEN,28).move_to([-3.2,1.35,0])
        right = lab("Trace-element\ncomparison",GREY,28).move_to([3.2,1.35,0])
        self.play(FadeOut(VGroup(pop,treatment,base,reduction)),ReplacementTransform(title,first),
                  FadeIn(left),FadeIn(right),run_time=0.65)
        zero = M("0",48,GREEN).move_to([-3.2,-0.1,0])
        six = M("6",48,RED).move_to([3.2,-0.1,0])
        counts = lab("Affected pregnancies",GREY,26).move_to([0,-1.2,0])
        self.at("no affected pregnancies")
        self.play(FadeIn(zero),FadeIn(counts),run_time=0.5)
        self.at("against six")
        self.play(FadeIn(six),run_time=0.5)
        support = lab("Supports prevention of a first occurrence",GREEN,28).move_to([0,-2.15,0])
        self.at("That supports")
        self.play(FadeIn(support),run_time=0.5)
        limit = lab("Cannot isolate folic acid’s effect",YELLOW,28).move_to([0,-3.05,0])
        self.at("But that trial alone")
        self.play(FadeOut(support),FadeIn(limit),run_time=0.5)
        self.finish()


class S04Squeeze(SpokenScene):
    def construct(self):
        title = heading("One route to closure failure")
        cells = cell_patch()
        self.at("Now consider")
        self.play(FadeIn(title),FadeIn(cells),run_time=0.5)
        ce = heading("Convergent extension",YELLOW)
        self.at("Convergent extension")
        self.play(ReplacementTransform(title,ce),run_time=0.4)
        self.at("cells push between")
        target = cell_patch(True)
        # Stagger the exchanges so the cells visibly slide between neighbours.
        self.play(LaggedStart(*[c.animate.move_to(t.get_center()) for c,t in zip(cells,target)],
                             lag_ratio=0.12),run_time=1.5)
        self.at("Planar cell polarity")
        polarity = heading("Planar cell polarity",TEAL)
        marks = VGroup(*[VGroup(Line(c.get_left()+RIGHT*0.12+DOWN*0.3,
                                       c.get_left()+RIGHT*0.12+UP*0.3,color=TEAL,stroke_width=5),
                               Line(c.get_right()+LEFT*0.12+DOWN*0.3,
                                    c.get_right()+LEFT*0.12+UP*0.3,color=TEAL,stroke_width=5)) for c in cells])
        self.play(ReplacementTransform(ce,polarity),FadeIn(marks),run_time=0.6)
        self.at("shared direction")
        direction = darr([-1.4,-2.6,0],[1.4,-2.6,0],TEAL)
        self.play(GrowFromCenter(direction),run_time=0.5)
        self.at("If the plate stays")
        wide = sec(3.6,0,half=3.6,sc=0.85,cx=-3.3,oy=0.5)
        narrow = sec(1.6,0,half=3.6,sc=0.85,cx=3.3,oy=0.5)
        wl = lab("wide plate",RED,28).move_to([-3.3,1.7,0])
        nl = lab("narrow plate",GREEN,28).move_to([3.3,1.7,0])
        self.play(FadeOut(VGroup(cells,marks,direction,polarity)),FadeIn(wide),FadeIn(narrow),
                  FadeIn(wl),FadeIn(nl),run_time=0.5)
        self.at("folds cannot meet")
        self.play(Transform(wide,sec(1.9,2.4,half=3.6,sc=0.85,cx=-3.3,oy=0.5)),
                  Transform(narrow,tube(1.2,half=3.6,sc=0.85,cx=3.3,oy=0.5)),run_time=0.7)
        result = VGroup(lab("folds stop short",RED,28).move_to([-3.3,-2.4,0]),
                        lab("folds meet",GREEN,28).move_to([3.3,-2.4,0]))
        self.play(FadeIn(result),run_time=0.35)
        self.finish()


class S05Frog(SpokenScene):
    def construct(self):
        s = sec(3.6,0)
        top = heading("Frog embryo",GREY)
        self.at("In frog embryos")
        self.play(FadeIn(s),FadeIn(top),run_time=0.6)
        bar = bar_over(-1.2,1.2)
        label = lab("Dishevelled disrupted at midline",RED,30).move_to([0,2.1,0])
        self.at("researchers disrupted")
        self.play(GrowFromCenter(bar),FadeIn(label),run_time=0.6)
        wide = darr([-3.6,0,0],[3.6,0,0],RED)
        wl = lab("plate stays wide",RED,28).move_to([0,-0.7,0])
        self.at("plate stayed wide")
        self.play(GrowFromCenter(wide),FadeIn(wl),run_time=0.5)
        self.at("still rose")
        arrows = VGroup(parr([-3.6,0.1,0],[-1.9,0.1,0]),parr([3.6,0.1,0],[1.9,0.1,0]))
        self.play(FadeOut(VGroup(wide,wl)),Transform(s,sec(1.9,2.4)),FadeIn(arrows),run_time=1.1)
        self.at("tube stayed open")
        gap = darr([-1.5,OY-0.6,0],[1.5,OY-0.6,0],RED,5)
        ol = lab("tube open",RED,34).move_to([0,OY-1.3,0])
        self.play(FadeOut(arrows),GrowFromCenter(gap),FadeIn(ol),run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        top = heading("Frog • regional comparison",GREY)
        left = sec(1.9,2.4,half=3.6,sc=0.85,cx=-3.3,oy=0.5)
        right = sec(3.6,0,half=3.6,sc=0.85,cx=3.3,oy=0.5)
        ll = lab("midline disrupted",RED,28).move_to([-3.3,2.05,0])
        rl = lab("sides disrupted",RED,28).move_to([3.3,2.05,0])
        bars = VGroup(bar_over(0.5,2.5,y=1.25),bar_over(4.1,6.1,y=1.25))
        self.at("Disrupting the sides")
        self.play(FadeIn(top),FadeIn(left),FadeIn(right),FadeIn(ll),FadeIn(rl),FadeIn(bars),run_time=0.5)
        self.at("instead left")
        self.play(Transform(right,sec(1.6,0,half=3.6,sc=0.85,cx=3.3,oy=0.5)),run_time=0.35)
        self.play(Transform(right,tube(1.2,half=3.6,sc=0.85,cx=3.3,oy=0.5)),run_time=0.55)
        results = VGroup(lab("open",RED,28).move_to([-3.3,-2.35,0]),
                         lab("closed",GREEN,28).move_to([3.3,-2.35,0]))
        self.play(FadeIn(results),run_time=0.3)
        self.at("Under those conditions")
        scope = lab("In this frog comparison",GREY,26).move_to([0,-3.1,0])
        self.play(FadeIn(scope),run_time=0.4)
        self.at("needed at the midline")
        self.play(Indicate(ll,color=TEAL,scale_factor=1.05),run_time=0.6)
        self.at("narrowing sets the distance")
        distance = darr([-4.65,0.0,0],[-1.95,0.0,0],YELLOW)
        self.play(GrowFromCenter(distance),run_time=0.6)
        self.at("In the loop tail mouse")
        mouse = heading("Loop-tail mouse • separate evidence",GREY)
        plate = RoundedRectangle(width=4.8,height=2.5,corner_radius=0.25,color=BLUE,
                                 fill_color=BLUE,fill_opacity=0.2).move_to([0,-0.2,0])
        mid = Line([0,-1.3,0],[0,0.9,0],color=RED,stroke_width=9)
        self.play(FadeOut(VGroup(left,right,ll,rl,bars,results,scope,distance)),
                  ReplacementTransform(top,mouse),FadeIn(plate),Create(mid),run_time=0.55)
        failed = lab("midline fails to extend before folding",RED,28).move_to([0,1.95,0])
        self.at("midline failed to extend")
        self.play(FadeIn(failed),Indicate(mid,color=RED,scale_factor=1),run_time=0.7)
        never = lab("closure never starts",RED,32).move_to([0,-2.5,0])
        self.at("closure never started")
        self.play(FadeIn(never),run_time=0.5)
        self.finish()


class S08Causes(SpokenScene):
    def construct(self):
        title = heading("Multiple contributing routes")
        polarity = chip("plate polarity",TEAL,28).move_to([-4.4,0.8,0])
        self.at("There are other routes")
        self.play(FadeIn(title),FadeIn(polarity),run_time=0.5)
        diabetes = chip("diabetes\nbefore pregnancy",RED,26).move_to([0,0.8,0])
        valproate = chip("valproic acid\nin early pregnancy",RED,26).move_to([4.4,0.8,0])
        self.at("Diabetes before pregnancy")
        self.play(FadeIn(diabetes),run_time=0.5)
        self.at("valproic acid")
        self.play(FadeIn(valproate),run_time=0.5)
        risk = lab("Spina bifida risk",RED,32).move_to([0,-1.5,0])
        routes = VGroup(*[parr([x,-0.05,0],[x*0.2,-1.0,0],RED,w=4) for x in [-4.4,0,4.4]])
        self.at("raise the risk")
        self.play(FadeIn(risk),*[GrowArrow(a) for a in routes],run_time=0.6)
        self.at("Most mothers")
        tests = heading("Most affected pregnancies",TEXT)
        measured = lab("Ordinary tests do not show\nfolate deficiency in most mothers",TEXT,32).move_to([0,0.8,0])
        self.play(FadeOut(VGroup(polarity,diabetes,valproate,risk,routes)),
                  ReplacementTransform(title,tests),FadeIn(measured),run_time=0.6)
        self.at("How folate prevents")
        unknown = lab("Folate → ? → prevention",YELLOW,36).move_to([0,-1.2,0])
        self.play(FadeIn(unknown),run_time=0.5)
        self.at("Its benefit is clear")
        benefit = heading("Folic acid lowers risk",GREEN)
        self.play(FadeOut(measured),ReplacementTransform(tests,benefit),unknown.animate.shift(UP*1.8),run_time=0.5)
        lower = VGroup(parr([-2.0,-0.1,0],[-2.0,-1.25,0],GREEN),
                       lab("lower risk",GREEN,34).move_to([0.5,-0.7,0]))
        self.at("lower risk")
        self.play(GrowArrow(lower[0]),FadeIn(lower[1]),run_time=0.7)
        remains = lab("Some defects still occur",RED,32).move_to([0,-2.0,0])
        self.at("some defects still occurring")
        self.play(FadeIn(remains),run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "If the neural tube stays open, defects follow; folic acid lowers risk."
