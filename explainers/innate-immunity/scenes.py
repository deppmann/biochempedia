"""Recognize and Respond: Innate Immunity. Word-timed schematic animation.

COLOR MAP (preserved from the original film)
  RED = microbes: spores, bacteria, budding yeast, infected cells
  BLUE = defender cells: phagocytes, macrophages, neutrophils, NK cells
  TEAL = complement pieces and blood proteins
  PURPLE = signals: interferon, mediators such as histamine
  ORANGE = lysosomes and antimicrobial peptides
  GREY = barriers, tissue, structural labels
  GREEN = cleared / protected / rebuilt
  YELLOW = recognition highlight
  GOLD = closing rule
  TEXT = labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CE0"
ORANGE = "#F2994A"
MIC, DEF, CMP, SIG, LYS, WALL, OK, HI, THR = RED, BLUE, TEAL, PURPLE, ORANGE, GREY, GREEN, YELLOW, GOLD


def arrow(a, b, color=TEXT, sw=6, tip=0.25, both=False):
    cls = DoubleArrow if both else Arrow
    return cls(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=sw,
               max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12, tip_length=tip)


def cell(x, y, r=0.5, color=DEF, op=0.25, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def dot(x, y, r=0.15, color=MIC):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0])


def spore(x, y, ang=0.6, L=0.55):
    d = np.array([np.cos(ang), np.sin(ang), 0]) * L / 2
    c = np.array([x, y, 0.0])
    return Line(c - d, c + d, color=MIC, stroke_width=8)


def yeast(x, y):
    a = Circle(radius=0.28, stroke_color=MIC, stroke_width=3, fill_color=MIC, fill_opacity=0.35).move_to([x, y, 0])
    b = Circle(radius=0.15, stroke_color=MIC, stroke_width=3, fill_color=MIC, fill_opacity=0.35).move_to([x + 0.32, y + 0.18, 0])
    return VGroup(a, b)


class Sc(SpokenScene):
    def rt(self, f):
        return min(max(0.4, self.beat(f)), 1.1)


def lg(v):
    return float(np.log10(v))


# Shared schematic receptor: an open cup on a short stem.
def receptor(x, y, color=DEF):
    return VGroup(Line([x-.3,y+.25,0], [x-.3,y-.15,0], color=color, stroke_width=5),
                  Line([x-.3,y-.15,0], [x+.3,y-.15,0], color=color, stroke_width=5),
                  Line([x+.3,y-.15,0], [x+.3,y+.25,0], color=color, stroke_width=5),
                  Line([x,y-.15,0], [x,y-.55,0], color=color, stroke_width=5))


def heading(text, color=TEXT):
    return T(text, 34, color).move_to([0, 3.15, 0])


class S00Title(TitleCard):
    LESSON = "Innate Immunity"
    TITLE = "Recognize and Respond: Innate Immunity"


class S08End(EndCard):
    LINE = "Keep microbes out, recognize intruders,\ngather defenses to clear them."


class S01Lead(Sc):
    def construct(self):
        wall = Rectangle(width=11.8, height=.35, stroke_width=0,
                         fill_color=WALL, fill_opacity=.8).move_to([0, 1.0, 0])
        microbes = VGroup(dot(-3,2.2), dot(-1,2.3), dot(2,2.1))
        resident = cell(1.3,-1.15,r=.95)
        rec = receptor(1.3,-.15)
        label = T("ready defenses",32,DEF).move_to([0,-3,0])
        self.at("Long before")
        self.play(FadeIn(wall), FadeIn(microbes), FadeIn(resident), Create(rec), run_time=.8)
        self.at("already defending itself")
        self.play(FadeIn(label), run_time=.6)
        self.at("Innate immunity")
        title = heading("Innate immunity: ready before contact")
        self.play(FadeIn(title), run_time=.6)
        self.at("Barriers keep")
        self.play(microbes[0].animate.move_to([-3,1.35,0]),
                  microbes[1].animate.move_to([-1,1.35,0]), run_time=.5)
        self.play(microbes[0].animate.shift(UP*.8+LEFT*.7),
                  microbes[1].animate.shift(UP*.9+LEFT*.3), run_time=.6)
        self.at("For the ones")
        gap = Rectangle(width=.8,height=.5,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([2,1,0])
        self.play(FadeIn(gap),microbes[2].animate.move_to([2,.5,0]),run_time=.7)
        self.at("receptors recognize")
        self.play(microbes[2].animate.move_to([1.3,-.02,0]),rec.animate.set_color(HI),run_time=.8)
        self.at("signs of damage")
        damage=chip("damage",WALL,24).move_to([-3,-.7,0])
        self.play(FadeIn(damage),run_time=.5)
        self.at("That recognition")
        self.play(FadeOut(damage),FadeOut(microbes[0]),FadeOut(microbes[1]),FadeOut(label),run_time=.5)
        self.at("inflammation")
        self.play(Transform(title,heading("Inflammation: gather the defenses",SIG)),run_time=.6)
        ph=cell(-4,-1.2,r=.55)
        protein=chip("blood proteins",CMP,24).move_to([4.3,-2.1,0])
        paths=VGroup(arrow([-3.2,-1.2,0],[-.1,-1.2,0],DEF),
                     arrow([3.5,-1.6,0],[2.5,-1.25,0],CMP))
        self.at("brings eating cells")
        self.play(FadeIn(ph),GrowArrow(paths[0]),run_time=.5)
        self.play(ph.animate.move_to([-.6,-1.2,0]),run_time=.7)
        self.at("blood proteins")
        self.play(FadeIn(protein),GrowArrow(paths[1]),run_time=.5)
        self.finish()


class S02Inflame(Sc):
    def construct(self):
        # Original tissue-above-vessel drawing, with a closed wall before sensing.
        tissue=Rectangle(width=12.4,height=4.4,stroke_color=WALL,stroke_width=2,
                         fill_color=WALL,fill_opacity=.08).move_to([0,1,0])
        gx=-1.5
        top_l=Line([-6.2,-1.3,0],[gx,-1.3,0],color=WALL,stroke_width=6)
        top_r=Line([gx,-1.3,0],[6.2,-1.3,0],color=WALL,stroke_width=6)
        bottom=Line([-6.2,-2.8,0],[6.2,-2.8,0],color=WALL,stroke_width=6)
        vessel=VGroup(top_l,top_r,bottom,T("small blood vessel",24,WALL).move_to([3.7,-3.25,0]))
        mac=cell(.6,1.35,r=.75,op=.3)
        ml=T("macrophage",26,DEF).move_to([.6,2.85,0])
        rec=receptor(.6,2.05)
        bact=dot(4.7,1.8,r=.25)
        step=T("1  sensing",32).move_to([-3.8,2.65,0])
        self.at("In a mammal")
        self.play(FadeIn(tissue),FadeIn(vessel),FadeIn(step),run_time=.6)
        self.at("resident cells")
        self.play(FadeIn(mac),FadeIn(ml),Create(rec),run_time=.7)
        self.at("TLR4")
        rl=T("TLR4",24,DEF).move_to([2.2,2.35,0])
        ligand=chip("LPS",MIC,24).move_to([4.2,.65,0])
        ll=T("bacterial outer-membrane molecule",24,MIC).move_to([2.5,-.55,0])
        self.play(FadeIn(rl),FadeIn(bact),FadeIn(ligand),run_time=.6)
        self.at("recognizes lipopolysaccharide")
        self.play(ligand.animate.move_to([.6,2.2,0]),rec.animate.set_color(HI),run_time=.8)
        self.at("outer membrane")
        self.play(FadeIn(ll),run_time=.5)
        self.at("Sensing switches")
        genes=chip("inflammatory genes ON",SIG,24).move_to([-3.6,1.1,0])
        self.play(FadeIn(genes),run_time=.6)
        self.at("Mediators such as")
        hist=chip("histamine",SIG,26).move_to([-3.8,-.45,0])
        self.play(FadeOut(ll),FadeOut(rl),FadeOut(ligand),FadeOut(genes),
                  Transform(step,T("2  open the vessel",32).move_to(step)),FadeIn(hist),run_time=.6)
        self.at("widen small vessels")
        self.play(bottom.animate.shift(DOWN*.3),hist.animate.shift(RIGHT*1.3),run_time=.7)
        self.at("loosen their lining")
        self.play(top_l.animate.put_start_and_end_on([-6.2,-1.3,0],[gx-.7,-1.3,0]),
                  top_r.animate.put_start_and_end_on([gx+.7,-1.3,0],[6.2,-1.3,0]),run_time=.6)
        fluid=VGroup(*[dot(gx+dx,-2,r=.11,color=DEF) for dx in (-.4,0,.4)])
        cp=chip("complement",CMP,22,pad=.1).move_to([1,-2.1,0])
        self.at("Fluid and plasma proteins")
        self.play(FadeOut(hist),FadeIn(fluid),FadeIn(cp),Transform(step,T("3  leak into tissue",32).move_to(step)),run_time=.5)
        self.at("leak into the tissue")
        self.play(fluid.animate.shift(UP*1.5),cp.animate.move_to([-3.4,-.25,0]),run_time=.8)
        neu=cell(-3.6,-2.1,r=.4)
        nl=T("neutrophil",24,DEF).move_to([-4.6,-2.25,0])
        self.at("Neutrophils squeeze")
        self.play(FadeOut(fluid),FadeOut(cp),FadeIn(neu),FadeIn(nl),
                  Transform(step,T("4  recruit cells",32).move_to(step)),run_time=.35)
        self.play(neu.animate.move_to([gx,-1.3,0]).stretch(.55,0),run_time=.4)
        self.play(neu.animate.move_to([3.2,.7,0]).stretch(1/.55,0),FadeOut(nl),run_time=.6)
        mono=cell(-.2,-2.1,r=.45,op=.12)
        mol=T("monocyte",24,DEF).move_to([1.6,-2.2,0])
        self.at("monocytes follow")
        self.play(FadeIn(mono),FadeIn(mol),run_time=.3)
        self.play(mono.animate.move_to([gx,-1.3,0]).stretch(.55,0),run_time=.4)
        self.play(mono.animate.move_to([2,-.05,0]).stretch(1/.55,0),FadeOut(mol),run_time=.6)
        self.at("Macrophages clear")
        self.play(mac.animate.move_to(bact),FadeOut(ml),FadeOut(rec),run_time=.5)
        self.play(FadeOut(bact,scale=.1),Transform(step,T("5  clear and repair",32).move_to(step)),run_time=.4)
        self.at("tissue rebuilds")
        self.play(tissue.animate.set_stroke(OK),
                  top_l.animate.put_start_and_end_on([-6.2,-1.3,0],[gx,-1.3,0]),
                  top_r.animate.put_start_and_end_on([gx,-1.3,0],[6.2,-1.3,0]),run_time=.6)
        self.finish()


class S03Walls(Sc):
    def construct(self):
        title=heading("Barriers come first",WALL)
        self.at("Barriers come first")
        self.play(FadeIn(title),run_time=.5)
        skin=VGroup(*[RoundedRectangle(width=1.5,height=.75,corner_radius=.08,
                    stroke_color=WALL,fill_color=WALL,fill_opacity=.3).move_to([x,y,0])
                    for y in (-.3,.5) for x in (-2.3,-.75,.8,2.35)])
        sl=T("skin: dead, tightly packed cells",30,WALL).move_to([0,-2,0])
        self.at("Skin's outer layer")
        self.play(FadeIn(skin),FadeIn(sl),run_time=.6)
        self.at("In airways")
        lining=Rectangle(width=.4,height=4,stroke_width=0,fill_color=WALL,fill_opacity=.8).move_to([1,0,0])
        mucus=Rectangle(width=.8,height=4,stroke_width=0,fill_color=WALL,fill_opacity=.23).move_to([.4,0,0])
        ticks=VGroup(*[Line([.8,y,0],[.2,y+.18,0],color=WALL,stroke_width=4) for y in np.arange(-1.8,1.9,.4)])
        ms=VGroup(dot(-2,1.2),dot(-2,-.4))
        al=T("airway: mucus + cilia",30,WALL).move_to([0,-2.7,0])
        self.play(FadeOut(skin),FadeOut(sl),FadeIn(lining),FadeIn(mucus),FadeIn(ms),FadeIn(al),run_time=.5)
        self.at("mucus traps")
        self.play(ms.animate.shift(RIGHT*2.2),run_time=.5)
        self.at("cilia carry")
        up=arrow([-1,0,0],[-1,2,0],WALL)
        self.play(Create(ticks),GrowArrow(up),ms.animate.shift(UP*2).set_opacity(0),run_time=.7)
        self.at("Stomach acid")
        acid=RoundedRectangle(width=6,height=3,corner_radius=.7,stroke_color=WALL,
                             fill_color=LYS,fill_opacity=.15)
        am=VGroup(dot(-1,0),dot(.5,.6),dot(1.5,-.5))
        ac=T("stomach acid",32,LYS).move_to([0,-2.4,0])
        self.play(*[FadeOut(m) for m in (lining,mucus,ticks,ms,al,up)],FadeIn(acid),FadeIn(am),FadeIn(ac),run_time=.5)
        self.at("kills many")
        self.play(FadeOut(am,scale=.1),run_time=.7)
        self.at("Lining cells release")
        lc=VGroup(*[cell(x,-.8,.5,color=WALL) for x in (-2.4,-.8,.8,2.4)])
        peptides=VGroup(*[dot(x,.4,r=.1,color=LYS) for x in (-2,-.4,1.2)])
        pl=T("antimicrobial peptides",28,LYS).move_to([0,1.9,0])
        self.play(FadeOut(acid),FadeOut(ac),FadeIn(lc),FadeIn(peptides),FadeIn(pl),run_time=.6)
        self.at("antimicrobial peptides")
        self.play(peptides.animate.shift(UP*.6),run_time=.6)
        self.at("harmless resident microbes")
        residents=VGroup(*[cell(x,.1,.32,color=MIC,op=.25) for x in (-2.4,-.8,.8,2.4)])
        rl=T("resident microbes occupy the space",28,MIC).move_to([0,-2.3,0])
        newcomer=dot(0,2.2,r=.22)
        self.play(FadeOut(peptides),FadeOut(pl),FadeIn(residents),FadeIn(rl),FadeIn(newcomer),run_time=.6)
        self.at("take the space")
        self.play(newcomer.animate.move_to([0,.85,0]),run_time=.5)
        self.play(newcomer.animate.shift(UP*1.2),run_time=.5)
        self.finish()


class S04Eat(Sc):
    def construct(self):
        ph=cell(1,0,r=2.1,op=.12)
        pl=T("phagocyte",32,DEF).move_to([1,2.7,0])
        microbe=dot(-3,0,r=.22)
        self.at("A microbe")
        self.play(FadeIn(ph),FadeIn(pl),FadeIn(microbe),run_time=.6)
        self.at("engulfs particles")
        self.play(microbe.animate.move_to([.5,.2,0]),run_time=.8)
        bubble=cell(.5,.2,r=.6,color=TEXT,op=0)
        self.play(Create(bubble),run_time=.4)
        ly=VGroup(cell(2.3,.9,.3,color=LYS,op=.5),cell(2.3,-.7,.3,color=LYS,op=.5))
        yl=T("lysosomes",28,LYS).move_to([3.8,-1.5,0])
        self.at("Lysosomes fuse")
        self.play(FadeIn(ly),FadeIn(yl),run_time=.4)
        self.play(ly[0].animate.move_to([.8,.65,0]),ly[1].animate.move_to([.8,-.25,0]),
                  bubble.animate.set_stroke(LYS).set_fill(LYS,opacity=.2),run_time=.7)
        self.at("usually kill it")
        self.play(FadeOut(microbe,scale=.1),run_time=.5)
        self.at("The evidence came")
        self.play(*[FadeOut(m) for m in (ph,pl,bubble,ly,yl)],run_time=.4)
        body=RoundedRectangle(corner_radius=.5,width=9,height=4.2,stroke_color=TEXT,
                              fill_color=TEXT,fill_opacity=.02).move_to([0,-.2,0])
        name=heading("Transparent water flea")
        self.at("transparent water flea")
        self.play(Create(body),FadeIn(name),run_time=.7)
        c1,c2=cell(-2,-.3,.65),cell(2,.5,.65)
        s1,s2=spore(-3,.5),spore(3,-.3)
        self.at("watched its blood cells")
        self.play(FadeIn(c1),FadeIn(c2),run_time=.4)
        self.at("swallow invading yeast spores")
        self.play(FadeIn(s1),FadeIn(s2),run_time=.3)
        self.play(s1.animate.move_to(c1),s2.animate.move_to(c2),run_time=.7)
        self.at("Where the cells destroyed")
        self.play(FadeOut(s1,scale=.1),FadeOut(s2,scale=.1),FadeOut(name),run_time=.4)
        intact=VGroup(body,c1,c2)
        self.play(intact.animate.scale(.6).move_to([-3.3,.35,0]),run_time=.6)
        good=T("spores destroyed\ninfection stops",28,OK,line_spacing=.8).move_to([-3.3,-1.8,0])
        self.play(FadeIn(good),run_time=.4)
        self.at("Where spores grew")
        body2=RoundedRectangle(corner_radius=.3,width=5.4,height=2.52,stroke_color=TEXT,
                               fill_opacity=0).move_to([3.3,.35,0])
        ys=VGroup(*[yeast(3.3+dx,.35+dy) for dx,dy in [(-1.6,.5),(-.7,-.6),(.3,.6),(1.5,-.4)]])
        bad=T("budding yeast grows\nflea dies",28,MIC,line_spacing=.8).move_to([3.3,-1.8,0])
        self.play(Create(body2),LaggedStart(*[FadeIn(y,scale=.4) for y in ys],lag_ratio=.12),run_time=.8)
        self.at("the flea died")
        self.play(body2.animate.set_stroke(MIC),FadeIn(bad),run_time=.5)
        self.finish()


class S05Complement(Sc):
    def construct(self):
        # Reuse the original complement chip split, microbe and phagocyte.
        mic=RoundedRectangle(corner_radius=.6,width=4.4,height=2.4,stroke_color=MIC,
                             stroke_width=4,fill_color=MIC,fill_opacity=.18).move_to([-2.4,-.3,0])
        ml=T("microbe",30,MIC).move_to(mic)
        title=heading("Complement: proteins in blood plasma",CMP)
        c3=chip("C3",CMP,34).move_to([-5.2,1.8,0])
        self.at("is a set", lead=.76)
        self.play(FadeIn(title),Create(mic),FadeIn(ml),FadeIn(c3),run_time=.7)
        self.at("is cut")
        c3b=chip("C3b",CMP,34).move_to([-3.7,1.85,0])
        c3a=chip("C3a",CMP,24,pad=.12).move_to([-5.5,2.1,0])
        cut=Line([-5.2,2.4,0],[-5.2,1.2,0],color=TEXT,stroke_width=4)
        self.play(Create(cut),run_time=.25)
        self.play(FadeOut(c3),FadeIn(c3b),FadeIn(c3a),FadeOut(cut),run_time=.4)
        self.at("sticks to a microbe")
        self.play(c3b.animate.move_to([-.2,.5,0]),run_time=.6)
        self.at("marks it for eating")
        ph=cell(4.8,-.3,r=1.45,op=.12)
        phl=T("phagocyte",28,DEF).move_to([4.8,1.6,0])
        reach=arrow([3,-.3,0],[.8,-.3,0],DEF)
        self.play(FadeIn(ph),FadeIn(phl),GrowArrow(reach),run_time=.7)
        self.at("The small pieces")
        self.play(FadeOut(title),FadeOut(reach),run_time=.4)
        self.at("a step later")
        c5a=chip("C5a",CMP,24,pad=.12).move_to([-1.8,1.5,0])
        self.play(FadeIn(c5a),run_time=.5)
        self.at("drift away")
        self.play(c3a.animate.move_to([-4.7,2.65,0]),c5a.animate.move_to([-1.7,2.65,0]),run_time=.6)
        self.at("promote inflammation")
        infl=T("promote inflammation",28,SIG).move_to([1.9,2.65,0])
        self.play(FadeIn(infl),run_time=.6)
        self.at("punch holes")
        hole=Rectangle(width=.8,height=.3,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([-2.4,-1.5,0])
        barrel=RoundedRectangle(corner_radius=.1,width=1.1,height=.55,stroke_color=CMP,
                                stroke_width=4,fill_opacity=0).move_to(hole)
        hl=T("holes in susceptible microbes",28,CMP).move_to([-2.4,-2.65,0])
        self.play(FadeIn(hole),Create(barrel),FadeIn(hl),run_time=.7)
        self.finish()


class S06Virus(Sc):
    def construct(self):
        infected=cell(-3.5,.3,1.3,color=MIC)
        neighbour=cell(3.5,.3,1.3,op=.12)
        il=T("infected cell",28,MIC).move_to([-3.5,-1.6,0])
        nl=T("nearby cell",28,DEF).move_to([3.5,-1.6,0])
        title=heading("Interferons alert nearby cells",SIG)
        self.at("Against viruses")
        self.play(FadeIn(infected),FadeIn(neighbour),FadeIn(il),FadeIn(nl),FadeIn(title),run_time=.6)
        ifn=VGroup(*[dot(-1.7,y,.12,color=SIG) for y in (-.1,.3,.7)])
        self.at("interferons from")
        self.play(FadeIn(ifn),run_time=.4)
        self.at("put nearby cells")
        self.play(ifn.animate.shift(RIGHT*3.6),run_time=.8)
        self.at("antiviral state")
        self.play(neighbour.animate.set_stroke(OK).set_fill(OK,opacity=.25),
                  Transform(nl,T("antiviral state",28,OK).move_to(nl)),FadeOut(ifn),run_time=.6)
        self.at("Natural killer cells")
        self.play(*[FadeOut(m) for m in (infected,neighbour,il,nl,title)],run_time=.35)
        nk=cell(-4.7,.1,.85,op=.3)
        nkl=T("NK cell",28,DEF).move_to([-4.7,-1.5,0])
        normal=cell(-.9,.1,.9,color=WALL)
        target=cell(4,.1,.9,color=MIC)
        badge=chip("MHC I",WALL,22,pad=.1).move_to([-.9,1.2,0])
        badge2=chip("MHC I",WALL,22,pad=.1).move_to([4,1.2,0])
        normal_l=T("normal cell",26,WALL).move_to([-.9,-1.5,0])
        target_l=T("infected / abnormal",26,MIC).move_to([4,-1.5,0])
        self.play(FadeIn(nk),FadeIn(nkl),FadeIn(normal),FadeIn(target),FadeIn(badge),
                  FadeIn(badge2),FadeIn(normal_l),FadeIn(target_l),run_time=.5)
        self.at("kill infected or abnormal cells")
        self.play(nk.animate.move_to([1.25,.1,0]),nkl.animate.move_to([1.25,-1.5,0]),run_time=.7)
        self.at("A cell that has lost")
        self.play(FadeOut(badge2),run_time=.6)
        self.at("normal surface protein")
        legend=heading("MHC class I: a brake on NK cells",WALL)
        self.play(FadeIn(legend),run_time=.6)
        self.at("removes a")
        self.play(nk.animate.move_to([3,.1,0]),nkl.animate.move_to([2.5,-2.3,0]),run_time=.4)
        self.play(FadeOut(target,scale=.2),FadeOut(target_l),run_time=.5)
        self.finish()


class S07Close(Sc):
    def construct(self):
        # Organism silhouettes, not molecular drawings.
        fly=VGroup(Ellipse(width=.65,height=1.1,color=WALL),
                   Ellipse(width=1,height=.5,color=WALL).rotate(.5).shift(LEFT*.5+UP*.2),
                   Ellipse(width=1,height=.5,color=WALL).rotate(-.5).shift(RIGHT*.5+UP*.2),
                   cell(0,.7,.23,color=WALL,op=.1)).move_to([-4,1,0])
        leaf=VGroup(Ellipse(width=1.1,height=1.8,color=WALL).rotate(-.4),
                    Line([0,-1.4,0],[0,.4,0],color=WALL,stroke_width=4)).move_to([0,1,0])
        mouse=VGroup(Ellipse(width=1.6,height=.9,color=WALL),cell(.65,.35,.32,color=WALL,op=.1),
                     Arc(radius=.5,start_angle=-PI/2,angle=PI,color=WALL).shift(LEFT*1.1)).move_to([4,1,0])
        labels=VGroup(*[T(t,28,WALL).move_to([x,-.5,0]) for t,x in (("fly",-4),("plant",0),("mouse",4))])
        self.at("Flies make no antibodies")
        self.play(FadeIn(fly),FadeIn(labels[0]),run_time=.6)
        self.at("flies and plants")
        self.play(FadeIn(leaf),FadeIn(mouse),FadeIn(labels[1:]),run_time=.5)
        recs=VGroup(*[receptor(x,-1.7) for x in (-4,0,4)])
        self.at("their own receptors")
        self.play(Create(recs),run_time=.6)
        self.at("Innate immunity does not")
        note=heading("Ready receptors")
        self.play(FadeIn(note),run_time=.5)
        self.at("build new receptors")
        new=chip("new B / T cell receptors",WALL,26).move_to([0,-3,0])
        strike=Line([-2.7,-3,0],[2.7,-3,0],color=MIC,stroke_width=4)
        self.play(FadeIn(new),Create(strike),run_time=.6)
        self.at("lacks their")
        self.play(Transform(note,heading("No B / T receptor-based memory",WALL)),run_time=.6)
        self.at("What it gives is speed")
        self.play(*[FadeOut(m) for m in (fly,leaf,mouse,labels,recs,new,strike)],
                  Transform(note,heading("Speed: recognize and respond",THR)),run_time=.6)
        # Three steps, with action at each cue in the closing sentence.
        wall=Rectangle(width=.25,height=2,stroke_width=0,fill_color=WALL,fill_opacity=.8).move_to([-4,0,0])
        m=dot(-5.2,.3,r=.18)
        wl=T("keep out",28,WALL).move_to([-4,-1.7,0])
        self.at("Keep microbes out")
        self.play(FadeIn(wall),FadeIn(m),FadeIn(wl),run_time=.3)
        self.play(m.animate.move_to([-4.4,.3,0]),run_time=.25)
        self.play(m.animate.shift(LEFT*.8),run_time=.3)
        rec=receptor(0,.2)
        ligand=dot(0,1.2,r=.18)
        rl=T("recognize",28,DEF).move_to([0,-1.7,0])
        self.at("recognize the ones")
        self.play(Create(rec),FadeIn(ligand),FadeIn(rl),run_time=.3)
        self.play(ligand.animate.move_to([0,.3,0]),rec.animate.set_color(HI),run_time=.5)
        defenders=VGroup(cell(3,-.6,.5),cell(5,-.6,.5))
        target=dot(4,.6,r=.18)
        dl=T("gather and clear",28,DEF).move_to([4,-1.7,0])
        self.at("gather the defenses")
        self.play(FadeIn(defenders),FadeIn(target),FadeIn(dl),run_time=.35)
        self.at("clear them")
        self.play(defenders[0].animate.move_to([3.6,.3,0]),defenders[1].animate.move_to([4.4,.3,0]),
                  FadeOut(target,scale=.1),run_time=.55)
        self.finish()
