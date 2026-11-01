"""Digestive systems: what told the stomach to start (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = an organ, gland or cell type (stomach, duodenum, pancreas, gallbladder, G cells, brainstem)
  ORANGE = food (a swallowed meal, fats and proteins)
  GREEN  = a secretion or response (acid juice, bicarbonate, enzymes, bile, the trypsin response)
  TEAL   = nerve route (vagus, nerve, acetylcholine receptors, the triggers of the cephalic phase)
  YELLOW = a hormone (gastrin, secretin, CCK) and the question mark of the opening
  RED    = cut, block, removed (cut vagus, atropine, 84% removed)
  GREY   = outlines, esophagus bar, blood bar, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tee(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def cross(center, s=0.2, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


def block(text, color=BLUE, w=3.0, h=1.4, size=28, label_at=None):
    box = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.14)
    lab = T(text, size, color)
    fit(lab, max_w=w - 0.3)
    lab.move_to(box if label_at is None else box.get_center() + np.array([label_at[0], label_at[1], 0]))
    return VGroup(box, lab)


def bar(x0, x1, y, color=GREY, h=0.32, op=0.35):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def dot(color=GREEN, r=0.11):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def scatter(n, x0, x1, y0, y1, color=GREEN, seed=1, r=0.11):
    rs = np.random.RandomState(seed)
    return VGroup(*[dot(color, r).move_to([rs.uniform(x0, x1), rs.uniform(y0, y1), 0]) for _ in range(n)])


def pulse(m, s=1.1):
    return m.animate(rate_func=there_and_back).scale(s)


def travel(dots, pts, rt=2.6, gap=0.4):
    pts = [np.array(p, float) for p in pts]
    for d in dots:
        d.move_to(pts[0])
    return [Succession(Wait(gap * i), MoveAlongPath(d, VMobject().set_points_as_corners(pts), run_time=rt,
                                                    rate_func=linear)) for i, d in enumerate(dots)]


# ---- the sham-feeding preparation, shared by s01 to s03 ------------------------------------
BY = 0.7                      # esophagus bar height
MOUTH = np.array([-5.2, BY, 0])
GAP_X = -1.9
STOM = np.array([4.1, BY, 0])
FLASK = np.array([4.1, -2.5, 0])


def prep(mid=False, fistula=False):
    d = {}
    d["mouth"] = bchip("mouth", BLUE, 30).move_to(MOUTH)
    d["bar1"] = bar(-4.3, -2.5, BY, h=0.45)
    d["mid"] = bar(-2.5, -1.3, BY, h=0.45)
    d["bar2"] = bar(-1.3, 2.2, BY, h=0.45)
    d["eso"] = T("esophagus", 24, GREY).move_to([1.0, BY + 0.6, 0])
    d["stom"] = block("stomach", BLUE, w=3.8, h=3.4, size=30, label_at=[0, 1.3]).move_to(STOM)
    d["neck"] = T("opening in the neck", 24, GREY).move_to([GAP_X, BY + 0.7, 0])
    if fistula:
        d["fline"] = Line(STOM + [0, -1.7, 0], FLASK + [0, 0.5, 0], color=GREY, stroke_width=6)
        d["flabel"] = T("gastric fistula", 24, GREY).move_to([2.6, -1.5, 0])
        d["flask"] = Rectangle(width=1.6, height=1.0, stroke_color=GREY, stroke_width=3).move_to(FLASK)
        d["fjuice"] = T("juice collected", 24, GREY).move_to(FLASK + [0, -0.78, 0])
    return d


def juice_fill(frac):
    h = max(0.02, 1.0 * frac)
    r = Rectangle(width=1.5, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.65)
    r.move_to([FLASK[0], FLASK[1] - 0.5 + h / 2, 0])
    return r


def food_run(food, scene, rt=1.4):
    """food chip travels the esophagus bar to the opening and drops out."""
    scene.play(food.animate.move_to([GAP_X, BY, 0]), run_time=rt, rate_func=linear)
    scene.play(food.animate.move_to([GAP_X, -1.7, 0]).set_opacity(0), run_time=0.9)


# Nutrients retain the food color ORANGE; microbes are BLUE cell types.
# All paths are schematic compartments, never molecular structures.
def heading(s):
    return T(s, 34, font=TITLE_FONT).move_to([0, 3.15, 0])


def clear_stage(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.35)


def lining(y=0):
    return VGroup(Line([-5.7, y, 0], [5.7, y, 0], color=BLUE, stroke_width=10),
                  T("gut lumen", 24, GREY).move_to([-4.8, y+1, 0]),
                  T("body", 26, BLUE).move_to([-4.8, y-1, 0]),
                  T("gut lining", 24, BLUE).move_to([4.7, y+0.45, 0]))


def absorption_image():
    wall = lining()
    ns = VGroup(*[dot(ORANGE, .15).move_to([x, 1.3, 0]) for x in (-1, 0, 1)])
    arrow = arr([0, .9, 0], [0, -1.4, 0], ORANGE)
    return wall, ns, arrow


def gut_map(y=0):
    names = ("mouth", "stomach", "small intestine", "large intestine")
    xs = (-5, -2, 1.3, 4.9)
    boxes = VGroup(*[block(n, w=2.7 if i>1 else 2.3, h=1.2, size=24).move_to([x,y,0])
                     for i,(x,n) in enumerate(zip(xs,names))])
    arrows = VGroup(*[arr(a.get_right(), b.get_left(), ORANGE, w=4, tip=.16)
                      for a,b in zip(boxes, list(boxes)[1:])])
    return VGroup(boxes, arrows)


class S00Title(TitleCard):
    LESSON = "Digestive systems and nutrition"
    TITLE = "From Food to Usable Nutrients"

    def construct(self):
        title = heading(self.TITLE)
        meal = bchip("meal", ORANGE, 30).move_to([-4, 1.2, 0])
        small = VGroup(*[dot(ORANGE,.16).move_to([x,1.2,0]) for x in (-.5,0,.5)])
        wall = Line([2,-1.5,0],[2,2,0],color=BLUE,stroke_width=10)
        lab = T("gut lining",24,BLUE).move_to([3.6,2.3,0])
        a = arr([-2.8,1.2,0],[-.9,1.2,0],ORANGE)
        b = arr([.8,1.2,0],[3.7,1.2,0],ORANGE)
        self.play(FadeIn(title),FadeIn(meal),Create(wall),FadeIn(lab),run_time=.7)
        self.play(GrowArrow(a),FadeIn(small),GrowArrow(b),run_time=.8)
        self.finish()


class S01Meal(SpokenScene):
    def construct(self):
        wall = lining()
        meal = bchip("large food molecules",ORANGE,28).move_to([0,1.7,0])
        self.at("An animal")
        self.play(FadeIn(wall),FadeIn(meal),run_time=.6)
        ns = VGroup(*[dot(ORANGE,.16).move_to([x,1.7,0]) for x in (-1,0,1)])
        self.at("food is broken")
        self.play(ReplacementTransform(meal,ns),run_time=.7)
        self.at("to cross")
        self.play(ns.animate.shift(DOWN*3.2),run_time=1.2)
        self.at("The gut breaks")
        clear_stage(self)
        gm=gut_map(.6)
        self.play(FadeIn(gm),run_time=.5)
        bead=dot(ORANGE,.14).move_to([-5,.24,0])
        self.add(bead)
        self.play(bead.animate.move_to([1.3,.24,0]),run_time=.7)
        out=arr([1.3,-.1,0],[1.3,-1.6,0],ORANGE)
        lab=T("nutrients, water, salts → body",26,ORANGE).move_to([0,-2.2,0])
        self.at("absorbs nutrients")
        self.play(GrowArrow(out),FadeIn(lab),run_time=.7)
        self.at("eliminates what")
        self.play(bead.animate.move_to([6.4,.24,0]).set_opacity(0),run_time=.9)
        self.at("Different regions")
        self.play(pulse(gm[0][1]),pulse(gm[0][2]),run_time=.8)
        self.at("In humans")
        clear_stage(self)
        si=block("small intestine",w=9,h=3.6,size=32,label_at=[0,1.3])
        si.move_to([0,.5,0])
        main=T("Main site: digestion + nutrient absorption",28,ORANGE).move_to([0,-2.3,0])
        self.play(FadeIn(si),FadeIn(main),run_time=.7)
        self.at("Its folds")
        clear_stage(self)
        # Increasing surface detail at three successively enlarged scales.
        surf=VMobject(color=BLUE,stroke_width=7).set_points_smoothly(
            [[x,.7*np.sin(x*2),0] for x in np.linspace(-5.3,5.3,100)])
        label=T("folds",30,BLUE).move_to([0,2.2,0])
        self.play(Create(surf),FadeIn(label),run_time=.5)
        self.at("velae")
        villi=VMobject(color=BLUE,stroke_width=7).set_points_smoothly(
            [[x,.9*np.sin(x*4),0] for x in np.linspace(-5.3,5.3,150)])
        self.play(Transform(surf,villi),Transform(label,T("villi · enlarged lining",30,BLUE).move_to(label)),run_time=.45)
        self.at("microvillae")
        micro=VGroup(*[Line([x,-.5,0],[x,.8,0],color=BLUE,stroke_width=6) for x in np.linspace(-5.2,5.2,35)])
        self.play(ReplacementTransform(surf,micro),Transform(label,T("microvilli · cell surface",30,BLUE).move_to(label)),run_time=.5)
        self.at("multiply the surface")
        self.play(FadeIn(T("More surface for absorption",28).move_to([0,-2,0])),run_time=.5)
        self.at("where nutrients cross")
        ds=VGroup(*[dot(ORANGE,.14).move_to([x,1.4,0]) for x in (-2,0,2)])
        self.add(ds)
        self.play(ds.animate.shift(DOWN*2.7),run_time=1.2)
        self.finish()


class S02Human(SpokenScene):
    def construct(self):
        self.at("Teeth grind food")
        teeth=VGroup(*[Rectangle(width=.6,height=.6,color=TEXT).move_to([x,y,0]) for x in (-.8,0,.8) for y in (-.8,.8)])
        food=dot(ORANGE,.45)
        self.play(FadeIn(heading("Teeth")),FadeIn(teeth),FadeIn(food),run_time=.4)
        bits=VGroup(*[dot(ORANGE,.12).move_to([x,.1*(i%2),0]) for i,x in enumerate(np.linspace(-.7,.7,5))])
        self.play(teeth.animate.stretch(.6,1),ReplacementTransform(food,bits),run_time=.7)
        self.at("The stomach mixes")
        clear_stage(self)
        stom=block("stomach",w=5,h=3,size=30,label_at=[0,1]).move_to([-3,0,0])
        mix=bchip("food + acid + enzymes",GREEN,24).move_to([-3,-.3,0])
        self.play(FadeIn(stom),FadeIn(mix),run_time=.5)
        self.play(mix.animate(rate_func=there_and_back).shift(RIGHT*.5),run_time=.6)
        self.at("The pancreas sends")
        clear_stage(self)
        duo=block("small intestine",w=5,h=2.1,size=28,label_at=[0,-.5]).move_to([2,-.6,0])
        panc=block("pancreas",w=3,h=1.1,size=28).move_to([-3,2,0])
        flow=arr([-2,1.4,0],[.8,.4,0],GREEN)
        sec=bchip("enzymes + bicarbonate",GREEN,24).move_to([2,2.1,0])
        acid=bchip("acid",GREEN,24).move_to([2,-.2,0])
        self.play(FadeIn(duo),FadeIn(panc),GrowArrow(flow),FadeIn(sec),FadeIn(acid),run_time=.8)
        self.at("Bicarbonate neutralizes acid")
        self.play(Transform(acid,bchip("acid neutralized",GREY,24).move_to(acid)),run_time=.8)
        self.at("Bile salts break")
        clear_stage(self)
        organs=VGroup(bchip("liver",BLUE,24),bchip("gallbladder",BLUE,24),bchip("bile salts",GREEN,24)).arrange(RIGHT,buff=.8).move_to([0,2.4,0])
        links=VGroup(*[arr(a.get_right(),b.get_left(),GREEN,w=4,tip=.15) for a,b in zip(organs,list(organs)[1:])])
        drop=dot(ORANGE,.75).move_to([-2,0,0])
        self.play(FadeIn(organs),FadeIn(links),FadeIn(drop),run_time=.5)
        drops=VGroup(*[dot(ORANGE,.22).move_to([x,y,0]) for x,y in ((1,0),(2,0),(3,0),(1.5,-.8),(2.5,-.8))])
        self.at("smaller droplets")
        self.play(ReplacementTransform(drop,drops),run_time=.7)
        self.at("lipase can reach")
        lip=bchip("lipase",GREEN,24).move_to([2,-2,0])
        self.play(FadeIn(lip),pulse(drops),run_time=.6)
        self.at("Enzymes split molecules")
        clear_stage(self)
        enzyme=bchip("enzymes: split molecules",GREEN,28).move_to([0,2.4,0])
        mol=block("large molecule",ORANGE,w=3,h=1,size=26).move_to([0,.5,0])
        self.play(FadeIn(enzyme),FadeIn(mol),run_time=.4)
        subs=VGroup(*[bchip("subunit",ORANGE,22).move_to([x,-.5,0]) for x in (-2,0,2)])
        self.play(ReplacementTransform(mol,subs),run_time=.6)
        self.at("Bile is not")
        self.play(FadeIn(T("Bile disperses fat droplets; it is not an enzyme.",26,GREEN).move_to([0,-2,0])),run_time=.5)
        self.at("Most absorbed sugars")
        clear_stage(self)
        vill=RoundedRectangle(width=3,height=5,corner_radius=1.4,color=BLUE).move_to([-3,0,0])
        vl=T("villus",26,BLUE).move_to([-3,3,0])
        blood=bchip("blood capillary",GREY,26).move_to([3,1.2,0])
        sugar=bchip("sugars + amino acids",ORANGE,24).move_to([-3,1.2,0])
        self.play(Create(vill),FadeIn(vl),FadeIn(blood),FadeIn(sugar),run_time=.5)
        self.play(sugar.animate.move_to([2.8,2.3,0]),GrowArrow(arr([-1.3,1.2,0],[1,1.2,0],ORANGE)),run_time=1)
        self.at("Most absorbed fat")
        fat=bchip("fat particles",ORANGE,24).move_to([-3,-1.4,0])
        lymph=bchip("lacteal: lymph vessel",GREY,24).move_to([3,-1.4,0])
        self.play(FadeIn(fat),FadeIn(lymph),run_time=.4)
        self.play(fat.animate.move_to([3,-2.5,0]),GrowArrow(arr([-1.3,-1.4,0],[.8,-1.4,0],ORANGE)),run_time=.9)
        self.at("The large intestine")
        clear_stage(self)
        li=block("large intestine",w=5,h=2.4,size=32).move_to([-3,0,0])
        water=bchip("water + salts",ORANGE,28).move_to([-3,-1.9,0])
        body=bchip("body",BLUE,30).move_to([4,0,0])
        self.play(FadeIn(li),FadeIn(water),FadeIn(body),GrowArrow(arr([- .3,0,0],[3,0,0],ORANGE)),run_time=.7)
        self.play(water.animate.move_to([4,-1.5,0]),run_time=1)
        self.finish()


class S03Designs(SpokenScene):
    def construct(self):
        self.at("Gut designs differ")
        self.play(FadeIn(heading("Different diets, different gut designs")),run_time=.6)
        self.at("A cow ferments")
        cow=T("Cow",30,BLUE).move_to([-5.6,1.6,0])
        stomach=RoundedRectangle(width=7.6,height=1.7,corner_radius=.2,color=BLUE).move_to([.5,1.6,0])
        st=T("one stomach · compartments",24,BLUE).move_to([.5,2.7,0])
        ferment=bchip("fermentation",BLUE,24).move_to([-1.6,1.6,0])
        acid=bchip("acid-secreting region",BLUE,24).move_to([2.4,1.6,0])
        ca=arr(ferment.get_right(),acid.get_left(),ORANGE,w=4,tip=.15)
        self.play(FadeIn(cow),Create(stomach),FadeIn(st),FadeIn(ferment),FadeIn(acid),GrowArrow(ca),run_time=.8)
        self.at("A horse ferments")
        horse=T("Horse",30,BLUE).move_to([-5.6,-.7,0])
        si=bchip("small intestine",BLUE,24).move_to([-1.6,-.7,0])
        hf=bchip("fermentation",BLUE,24).move_to([2.4,-.7,0])
        ha=arr(si.get_right(),hf.get_left(),ORANGE)
        self.play(FadeIn(VGroup(horse,si,hf,ha)),run_time=.7)
        self.at("Gut length alone")
        clear_stage(self)
        ruler=VGroup(Line([-5.5,0,0],[5.5,0,0],color=GREY),*[Line([x,-.15,0],[x,.15,0],color=GREY) for x in range(-5,6)])
        factors=T("diet     •     body size     •     ancestry",30,BLUE).move_to([0,2,0])
        self.play(Create(ruler),FadeIn(factors),FadeIn(T("Gut length alone is no simple guide to diet",28).move_to([0,-1.7,0])),run_time=.8)
        self.finish()


class S04Microbes(SpokenScene):
    def construct(self):
        self.at("Who breaks down")
        self.play(FadeIn(heading("Who breaks down the fiber?")),run_time=.6)
        self.at("Microbes ferment cellulose")
        cell=bchip("microbes",BLUE,28).move_to([0,1.4,0])
        fiber=bchip("cellulose",ORANGE,28).move_to([-4,0,0])
        acids=bchip("short-chain fatty acids",ORANGE,26).move_to([2.5,0,0])
        self.play(FadeIn(cell),FadeIn(fiber),GrowArrow(arr([-2.8,0,0],[-.3,0,0],BLUE)),run_time=.7)
        self.at("release short")
        self.play(FadeIn(acids),run_time=.5)
        self.at("which the host absorbs")
        host=bchip("host body",BLUE,28).move_to([2.5,-2,0])
        self.play(FadeIn(host),GrowArrow(arr([2.5,-.5,0],[2.5,-1.4,0],ORANGE)),run_time=.7)
        self.at("Cows digest microbes")
        clear_stage(self)
        title=heading("Cow · microbial cells move downstream")
        rum=block("rumen + reticulum",w=4.5,h=2.6,size=26,label_at=[0,.8]).move_to([-3.6,.4,0])
        abo=block("abomasum",w=4,h=2.6,size=28,label_at=[0,.8]).move_to([3.3,.4,0])
        microbes=bchip("microbes",BLUE,24).move_to([-3.6,0,0])
        self.play(FadeIn(title),FadeIn(rum),FadeIn(abo),FadeIn(microbes),GrowArrow(arr([-1.3,.4,0],[1.2,.4,0],ORANGE)),run_time=.7)
        self.at("pass into")
        self.play(microbes.animate.move_to([3.3,0,0]),run_time=1.2)
        self.play(ReplacementTransform(microbes,T("microbes digested",24,GREEN).move_to([3.3,-.1,0])),FadeIn(T("acid-secreting compartment",24,BLUE).move_to([3.3,-1.6,0])),run_time=.6)
        self.at("Horses ferment")
        clear_stage(self)
        h=block("Horse: cecum + colon",w=8,h=3,size=30,label_at=[0,1])
        ms=VGroup(*[bchip("microbe",BLUE,22).move_to([x,-.3,0]) for x in (-2,0,2)])
        self.play(FadeIn(h),FadeIn(ms),run_time=.6)
        self.at("Rabbits ferment")
        clear_stage(self)
        title=heading("Rabbit · recover microbial protein")
        names=("mouth","stomach","small intestine","cecum")
        boxes=VGroup(*[bchip(n,BLUE,24).move_to([x,.7,0]) for n,x in zip(names,(-5,-2,1.5,5))])
        arrows=VGroup(*[arr(a.get_right(),b.get_left(),ORANGE,w=4,tip=.15) for a,b in zip(boxes,list(boxes)[1:])])
        pellet=bchip("soft cecal pellets",ORANGE,24).move_to([3,-1.7,0])
        self.play(FadeIn(title),FadeIn(boxes),FadeIn(arrows),run_time=.6)
        self.at("They eat soft")
        loop=VMobject(color=ORANGE,stroke_width=4).set_points_as_corners([[5,.2,0],[5,-2.7,0],[-5,-2.7,0],[-5,.2,0]])
        self.play(Create(loop),FadeIn(pellet),run_time=.8)
        self.at("sending microbes")
        protein=bchip("microbes + protein",ORANGE,24).move_to([-5,1.8,0])
        self.play(FadeOut(pellet),FadeIn(protein),run_time=.4)
        self.at("through the stomach")
        self.play(protein.animate.move_to([-2,1.8,0]),run_time=.6)
        self.at("small intestine for")
        self.play(protein.animate.move_to([1.5,1.8,0]),run_time=.6)
        self.at("digestion and absorption")
        self.play(FadeOut(protein),FadeIn(T("protein digested → nutrients absorbed",26,ORANGE).move_to([0,-1,0])),run_time=.7)
        self.finish()


class S03Vagus(SpokenScene):
    def construct(self):
        self.at("Nerves and hormones")
        title=heading("Nerves and hormones coordinate the gut")
        self.play(FadeIn(title),run_time=.6)
        self.at("Gut wall nerves")
        tube=VGroup(bar(-5.5,5.5,.8,BLUE,h=.2),bar(-5.5,5.5,-.8,BLUE,h=.2))
        circuit=VGroup(*[dot(TEAL,.18).move_to([x,1.7,0]) for x in (-2,0,2)],Line([-2,1.7,0],[2,1.7,0],color=TEAL))
        food=dot(ORANGE,.3).move_to([-3,0,0])
        self.play(FadeIn(tube),FadeIn(circuit),FadeIn(food),run_time=.4)
        self.play(tube.animate(rate_func=there_and_back).stretch(.6,1),food.animate.shift(RIGHT*5),run_time=1)
        self.at("In Pavlov's dogs")
        clear_stage(self)
        t=prep(fistula=True)
        # Old sham-feeding preparation, in its original positions.
        diagram=VGroup(*[t[k] for k in ("mouth","bar1","bar2","eso","stom","neck","fline","flabel","flask","fjuice")])
        stem=bchip("brainstem",BLUE,24).move_to([1,3.1,0])
        nerves=VGroup(*[VMobject(color=TEAL,stroke_width=5).set_points_as_corners([[2,3.3-d,0],[3.7-d,3.3-d,0],[3.7-d,2.4,0]]) for d in (0,.45)])
        evidence=T("Evidence in dogs · sham feeding",26,GREY).move_to([-2.9,-3.1,0])
        self.play(FadeIn(diagram),FadeIn(stem),Create(nerves),FadeIn(evidence),run_time=.5)
        food=bchip("food",ORANGE,24).move_to(MOUTH+[1,0,0])
        self.at("eating triggered")
        self.add(food)
        food_run(food,self,rt=.55)
        self.at("even when food")
        drops=VGroup(*[dot() for _ in range(3)])
        fill=juice_fill(.7)
        self.play(*travel(drops,[STOM+[0,-.3,0],STOM+[0,-1.7,0],FLASK],rt=.7,gap=.12),FadeIn(fill),run_time=1.1)
        self.at("Cutting both vagus")
        cuts=VGroup(cross([2.8,3.3,0],.15),cross([2.8,2.85,0],.15))
        self.play(Create(cuts),run_time=.4)
        self.at("stopped that response")
        self.play(FadeOut(drops),FadeOut(fill),FadeIn(T("eating-triggered juice stops",24,RED).move_to([-.8,-1,0])),run_time=.6)
        self.at("This showed nervous")
        self.play(Transform(evidence,T("Nervous control before food arrives · dogs",25,TEAL).move_to(evidence)),run_time=.7)
        self.finish()


class S04Gastrin(SpokenScene):
    def construct(self):
        stom=block("stomach",BLUE,w=8,h=3.8,size=30,label_at=[0,1.5]).move_to([0,.7,0])
        blood=bar(-5.4,5.4,-2.4,GREY,h=.34,op=.3)
        blab=T("blood",24,GREY).move_to([-4.9,-2.95,0])
        gcell=bchip("G cells",BLUE,26).move_to([-2.7,1.1,0])
        self.at("Hormones travel in blood")
        self.play(FadeIn(stom),FadeIn(gcell),Create(blood),FadeIn(blab),run_time=.5)
        self.at("Food in the stomach")
        food=bchip("food",ORANGE,26).move_to([0,-.3,0])
        self.play(FadeIn(food),run_time=.4)
        self.at("brings out gastrin")
        hormone=bchip("gastrin",YELLOW,24).move_to([0,-1.7,0])
        hd=VGroup(*[dot(YELLOW,.13) for _ in range(2)])
        self.play(FadeIn(hormone),run_time=.2)
        self.add(hd)
        self.play(*travel(hd,[[-2.7,.7,0],[-2.7,-2.4,0],[3,-2.4,0],[3,-.5,0]],rt=.8,gap=.1),run_time=1)
        self.at("which increases acid")
        acid=scatter(6,2.4,3.6,-.9,1.3,GREEN,seed=7)
        self.play(FadeOut(hd),FadeIn(acid),FadeIn(T("more acid",26,GREEN).move_to([3,1.8,0])),run_time=.5)
        self.finish()


class S05Duodenum(SpokenScene):
    def construct(self):
        duo=block("duodenum",BLUE,w=3.4,h=1.6,size=26,label_at=[0,.45]).move_to([-.7,0,0])
        panc=block("pancreas",BLUE,w=3.4,h=1.1,size=26).move_to([-.7,2.5,0])
        gall=block("gallbladder",BLUE,w=3.4,h=1.1,size=26).move_to([-.7,-2.5,0])
        bld=Rectangle(width=.34,height=5.3,color=GREY,fill_opacity=.3).move_to([3.2,0,0])
        blab=T("blood",24,GREY).move_to([4.3,0,0])
        acid=bchip("acid",GREEN,22).move_to([-.7,-.2,0])
        self.at("Acid entering the duodenum")
        self.play(FadeIn(VGroup(duo,panc,gall,bld,blab,acid)),run_time=.6)
        self.at("brings out secretin")
        hormone=bchip("secretin",YELLOW,24).move_to([4.9,1.8,0])
        hd=VGroup(*[dot(YELLOW,.12) for _ in range(2)])
        self.play(FadeIn(hormone),run_time=.2)
        self.add(hd)
        self.play(*travel(hd,[[.7,0,0],[3.2,0,0],[3.2,2.5,0],[1,2.5,0]],rt=.9,gap=.12),run_time=1.1)
        self.at("which drives pancreatic")
        a=arr([-1.3,1.9,0],[-1.3,.85,0],GREEN)
        lab=T("bicarbonate",24,GREEN).move_to([-3.4,1.4,0])
        self.play(FadeOut(hd),GrowArrow(a),FadeIn(lab),run_time=.5)
        self.at("bicarbonate secretion")
        self.play(Transform(acid,bchip("neutralized",GREY,22).move_to(acid)),run_time=.7)
        self.at("Fats and proteins")
        self.play(FadeOut(a),FadeOut(lab),FadeOut(hormone),Transform(acid,bchip("fats + proteins",ORANGE,22).move_to(acid)),run_time=.5)
        self.at("bring out CCK")
        cck=bchip("CCK",YELLOW,24).move_to([4.9,1.8,0])
        self.play(FadeIn(cck),run_time=.2)
        hd1=VGroup(dot(YELLOW,.13)); hd2=VGroup(dot(YELLOW,.13))
        self.add(hd1,hd2)
        self.play(*travel(hd1,[[.7,0,0],[3.2,0,0],[3.2,2.5,0],[1,2.5,0]],rt=.9),
                  *travel(hd2,[[.7,0,0],[3.2,0,0],[3.2,-2.5,0],[1,-2.5,0]],rt=.9),run_time=1)
        self.at("which drives pancreatic enzyme")
        ae=arr([-.7,1.9,0],[-.7,.85,0],GREEN)
        le=T("enzymes",24,GREEN).move_to([-3,1.3,0])
        self.play(FadeOut(hd1),FadeOut(hd2),GrowArrow(ae),FadeIn(le),run_time=.6)
        self.at("gallbladder contraction")
        self.play(pulse(gall,1.08),run_time=.5)
        ab=arr([-.7,-1.9,0],[-.7,-.85,0],GREEN)
        lb=T("bile",24,GREEN).move_to([-2,-1.4,0])
        self.at("to release bile")
        self.play(GrowArrow(ab),FadeIn(lb),run_time=.5)
        self.finish()


class S06Essential(SpokenScene):
    def construct(self):
        self.at("Finally an essential nutrient")
        title=heading("Essential depends on the animal")
        food=bchip("food",ORANGE,30).move_to([-4,0,0])
        animal=block("animal",w=4,h=2,size=30).move_to([3,0,0])
        a=arr([-3,0,0],[.8,0,0],ORANGE)
        lab=T("essential nutrient",28,ORANGE).move_to([-1,1,0])
        self.play(FadeIn(title),FadeIn(food),FadeIn(animal),GrowArrow(a),FadeIn(lab),run_time=.7)
        self.at("cannot make enough")
        self.play(FadeIn(T("cannot make enough",26,RED).move_to([3,-1.7,0])),run_time=.5)
        self.at("Requirements differ")
        clear_stage(self)
        self.play(FadeIn(heading("Requirements differ")),run_time=.4)
        self.at("Humans need dietary")
        human=bchip("human",BLUE,28).move_to([3,1.5,0])
        vit=bchip("dietary vitamin C",ORANGE,26).move_to([-3,1.5,0])
        self.play(FadeIn(human),FadeIn(vit),GrowArrow(arr([-1,1.5,0],[2,1.5,0],ORANGE)),run_time=.6)
        self.at("Cats need dietary")
        cat=bchip("cat",BLUE,28).move_to([3,-.1,0])
        tau=bchip("dietary taurine",ORANGE,26).move_to([-3,-.1,0])
        self.play(FadeIn(cat),FadeIn(tau),GrowArrow(arr([-1,-.1,0],[2,-.1,0],ORANGE)),run_time=.6)
        self.at("which adult humans make")
        self.play(FadeIn(T("adult humans → make taurine",28,BLUE).move_to([0,-1.8,0])),run_time=.6)
        # Closing visual bridges directly into the silent end card.
        self.wait(1.1)
        clear_stage(self)
        wall,ns,arrow=absorption_image()
        self.play(FadeIn(wall),FadeIn(ns),GrowArrow(arrow),run_time=.4)
        self.play(ns.animate.shift(DOWN*2.7),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "Digestion breaks food into small molecules the gut can absorb."
    def construct(self):
        wall,ns,arrow=absorption_image()
        ns.shift(DOWN*2.7)
        self.add(wall,ns,arrow)
        self.play(FadeIn(heading(self.LINE)),run_time=.6)
        self.finish()
