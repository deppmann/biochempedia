"""Chapter 1: One in Two Thousand. All quantitative bars are computed.

COLOR MAP (from scenes.old.py, shared across the chapter series):
BLUE (neutral blue-grey) = unchosen receptor gene / non-one model bars; RED = repressive chromatin / silencing;
GREEN = chosen active gene / stable endpoint; TEAL = enhancer hubs only;
GOLD = key / Lsd1-dependent opening and slider control;
ORANGE = receptor RNA / receptor expressed; PURPLE = stress and feedback;
GOLD = lineage mark / title rule; GREY = nucleus, outlines and labels.
"""
import math
import numpy as np
from bp_style import *

BLUE = "#8397AC"
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LESSON = "One Receptor per Neuron: How Olfactory Neurons Choose"


# The tile, nucleus and arrow vocabulary is retained from scenes.old.py.
def tile(color=BLUE, s=.46, op=.35):
    return RoundedRectangle(corner_radius=.08, width=s, height=s,
        stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op)


def arr(a, b, color=GREY):
    return Arrow(a, b, buff=.1, color=color, stroke_width=4, tip_length=.2)


def label(s, y=3.15, color=GREY, size=28):
    return T(s, size, color).move_to([0, y, 0])


def nucleus():
    return Ellipse(width=11.8, height=5.3, stroke_color=GREY,
                   fill_color=GREY, fill_opacity=.035)


def candidates(dim=False, chosen=False):
    # Exactly 1,000 paired positions, uniformly distributed inside an ellipse.
    # Compound paths keep the 2,000 little tokens cheap to render.
    paths = [VMobject(stroke_width=.45, stroke_color=BLUE,
                      fill_color=BLUE, fill_opacity=.55) for _ in range(2)]
    for i in range(1000):
        r = math.sqrt((i+.5)/1000)
        theta = i * math.pi * (3-math.sqrt(5))
        x, y = 5.48*r*math.cos(theta), 2.38*r*math.sin(theta)
        for k, dx in enumerate((-.038, .038)):
            p = np.array([x+dx, y, 0])
            pts = [p+[-.023,-.023,0], p+[.023,-.023,0],
                   p+[.023,.023,0], p+[-.023,.023,0], p+[-.023,-.023,0]]
            paths[k].append_vectorized_mobject(VMobject().set_points_as_corners(pts))
    g = VGroup(*paths)
    if dim:
        g.set_opacity(.18)
    win = tile(GREEN, .20, .95).move_to([.8,.3,0])
    return VGroup(nucleus(), g, *([win] if chosen else []))


def lock_icon(color=PURPLE):
    body = RoundedRectangle(width=.65, height=.52, corner_radius=.07,
        stroke_color=color, fill_color=color, fill_opacity=.25)
    arch = Arc(radius=.23, start_angle=0, angle=PI, color=color,
               stroke_width=5).shift(UP*.27)
    return VGroup(body, arch)


def key_icon():
    return VGroup(Circle(radius=.25, color=GOLD),
        Line([.25,0,0],[1.05,0,0],color=GOLD,stroke_width=7),
        Line([.8,0,0],[.8,-.22,0],color=GOLD,stroke_width=7),
        Line([1.03,0,0],[1.03,-.22,0],color=GOLD,stroke_width=7))


def alarm():
    # Separate stem and dot: no font-dependent exclamation glyph.
    tri=Triangle(color=PURPLE,fill_color=PURPLE,fill_opacity=.18).scale(.85)
    mark=VGroup(Line([0,.38,0],[0,.03,0],color=PURPLE,stroke_width=7),
                Dot([0,-.17,0],radius=.055,color=PURPLE))
    return VGroup(tri,mark)


def cover(t):
    """A visibly opaque chromatin cover with three broad bands."""
    w,h=t.width+.12,t.height+.14
    lid=RoundedRectangle(width=w,height=h,corner_radius=.09,
        color=RED,fill_color="#42242A",fill_opacity=.95,stroke_width=2).move_to(t)
    for dy in (-.18,0,.18):
        lid.add(Line(t.get_center()+[-w*.42,dy,0],t.get_center()+[w*.42,dy,0],
                     color=RED,stroke_width=3))
    return lid


def phases(states=(0,0,0), dominant=False):
    g=VGroup()
    titles=("Early\nprogenitor","Late precursor →\nimmature neuron","Mature\nneuron")
    for i,x in enumerate((-4.25,0,4.25)):
        panel=RoundedRectangle(width=3.95,height=5.8,corner_radius=.18,
            color=GREY,fill_color=GREY,fill_opacity=.035).move_to([x,0,0])
        title=T(titles[i],26).move_to([x,2.15,0])
        contents=VGroup()
        if states[i]:
            for j in range(9):
                t=tile(BLUE,.63,.28).move_to([x+(j%3-1)*1.04,.8-(j//3)*1.05,0])
                if i==0: t.add(cover(t))
                elif i==1 and j in (1,4,6):
                    t.set_stroke(ORANGE).set_fill(ORANGE,.28)
                    if dominant: t.set_opacity(.25 if j!=4 else 1)
                    if dominant and j==4: t.set_fill(GREEN,.58).set_stroke(GREEN)
                elif i==2 and j==4: t.set_fill(GREEN,.95).set_stroke(GREEN)
                contents.add(t)
            if i==1:
                for j in (1,4,6):
                    contents.add(Circle(radius=.46,color=TEAL,stroke_width=3).move_to(contents[j]))
            if i==2:
                contents.add(Circle(radius=.49,color=PURPLE,stroke_width=5).move_to(contents[4]))
            text=("Silenced","Then one dominates" if dominant else "Several, weakly","One gene\none allele")[i]
            contents.add(T(text,26,(RED,ORANGE,GREEN)[i]).move_to([x,-2.24,0]))
        g.add(VGroup(panel,title,contents))
    return g


def poisson(m):
    a=[math.exp(-m)*m**k/math.factorial(k) for k in range(3)]
    return a+[1-sum(a)]


def chart(m=.1, live=False, reference=False):
    # All bar heights and live labels come from the same Poisson probabilities.
    g=VGroup(label("Unselected Poisson model",3.25,TEXT,30))
    left,right,base,top=-4.8,2.1,-1.6,2.55
    g.add(Line([left,base,0],[right,base,0],color=GREY),
          Line([left,base,0],[left,top,0],color=GREY))
    for v in (0,.25,.5,.75,1):
        y=base+(top-base)*v
        g.add(T(f"{v*100:.0f}%",26,GREY).move_to([-5.48,y,0]),
              Line([left-.08,y,0],[left,y,0],color=GREY))
    g.add(T("Share of neurons",26,GREY).rotate(PI/2).move_to([-6.2,.5,0]))
    probs=poisson(m)
    if reference:
        y=base+(top-base)/math.e
        g.add(DashedLine([left,y,0],[right,y,0],color=GREEN,stroke_opacity=.55),
              T("37%",26,GREEN).move_to([2.7,y,0]))
    for k,(x,p) in enumerate(zip((-3.85,-2.15,-.45,1.25),probs)):
        h=max(.006,(top-base)*p)
        bar=Rectangle(width=1.08,height=h,stroke_width=2 if k==1 else 0,
            stroke_color=GREEN,fill_color=GREEN if k==1 else BLUE,fill_opacity=.85)
        bar.move_to([x,base+h/2,0]);g.add(bar)
        g.add(T(("0","1","2","3+")[k],28,GREEN if k==1 else GREY).move_to([x,-1.98,0]))
        if live and (k==1 or (k==0 and abs(m-1)<.015)):
            g.add(T(f"{100*p:.0f}%",28,GREEN if k==1 else TEXT).move_to([x,base+h+.24,0]))
    g.add(T("Receptors per neuron",26,GREY).move_to([-1.35,-2.45,0]))
    return g


def formula():
    return T("P(exactly one)\n= m × e^(−m)",28,GREEN).move_to([4.65,1.9,0])


def slider(m=.1):
    return VGroup(Line([-3.8,-2.95,0],[2.4,-2.95,0],color=GREY),
        Dot([-3.8+6.2*(m-.1)/2.9,-2.95,0],radius=.12,color=GOLD),
        T(f"m = {m:.1f}   average escapes per neuron",26,GOLD).move_to([-.5,-3.45,0]))


def peak_banner():
    return T("Maximum\n1/e ≈ 37%\nat m = 1",30,GREEN).move_to([4.65,-.5,0])


QUESTION="Largest fraction with exactly one?"
def question_frame(question=True):
    g=VGroup(chart(.1),slider(.1),formula())
    if question:
        h=4.15*poisson(.1)[1]
        outline=Rectangle(width=1.2,height=h+.1,color=GREEN,stroke_width=5).move_to([-2.15,-1.6+h/2,0])
        g.add(outline,T("?",40,GREEN).move_to([-2.15,-1.6+h+.48,0]),
              T("Largest fraction\nwith exactly one?",28).move_to([4.65,-.55,0]))
    return g


def competition():
    g=VGroup()
    for x,y in ((-4,.4),(0,1),(4,.4)):
        g.add(VGroup(Circle(radius=1.3,color=TEAL,fill_color=TEAL,fill_opacity=.08).move_to([x,y,0]),
                     tile(ORANGE,.95,.32).move_to([x,y,0])))
    return g


def library(opened=False):
    books=VGroup();chains=VGroup()
    for i,x in enumerate((-4.5,-3,-1.5,0,1.5,3,4.5)):
        b=RoundedRectangle(width=.9,height=4.35,corner_radius=.09,
            color=GREEN if opened and i in (1,3,5) else BLUE,
            fill_color=GREEN if opened and i in (1,3,5) else BLUE,
            fill_opacity=.25).move_to([x,-.15,0])
        b.add(Line([x-.32,-2.15,0],[x-.32,1.85,0],color=GREY,stroke_width=2))
        for y in (1.55,1.68,1.81):
            b.add(Line([x-.2,y,0],[x+.38,y,0],color=GREY,stroke_width=2))
        b.add(Rectangle(width=.48,height=.62,color=GREY,stroke_width=2).move_to([x,.8,0]))
        books.add(b)
        ch=VGroup(*[Ellipse(width=.46,height=.30,color=RED,stroke_width=4).move_to([x+dx,-.45,0]) for dx in (-.3,0,.3)])
        if opened and i in (1,3,5):ch.set_opacity(0)
        chains.add(ch)
    shelf=Line([-5.4,-2.42,0],[5.4,-2.42,0],color=GREY,stroke_width=9)
    return VGroup(books,chains,shelf)


def bell_icon():
    return VGroup(Arc(radius=.5,start_angle=0,angle=PI,color=PURPLE,stroke_width=7),
        Line([-.5,0,0],[.5,0,0],color=PURPLE,stroke_width=7),
        Dot([0,-.14,0],radius=.09,color=PURPLE))


def copies(chosen=False):
    g=VGroup()
    for i,x in enumerate((-2.8,2.8)):
        t=tile(GREEN if chosen and i==0 else BLUE,2.45,.75 if chosen and i==0 else .25).move_to([x,.1,0])
        g.add(t)
    return g


def magnified(chosen=False):
    # A nucleus overview plus a labelled zoom: the pairs are readable in the inset.
    field=candidates().scale(.56).move_to([-3.1,.25,0])
    box=RoundedRectangle(width=5.2,height=4.7,corner_radius=.2,color=GREY).move_to([3.15,.25,0])
    pairs=VGroup()
    for j in range(6):
        x=1.75+(j%2)*2.65;y=1.55-(j//2)*1.35
        pair=VGroup(tile(BLUE,.62,.3).move_to([x-.39,y,0]),tile(BLUE,.62,.3).move_to([x+.39,y,0]))
        pairs.add(pair)
    if chosen:pairs[2][0].set_stroke(GREEN).set_fill(GREEN,.95)
    leader=VGroup(Line([-.7,1.4,0],[.55,2.3,0],color=GREY),Line([-.7,-.8,0],[.55,-1.8,0],color=GREY))
    return VGroup(field,box,pairs,leader,T("Magnified patch · paired alleles",26,GREY).move_to([3.15,-2.55,0]))


class S00Title(TitleCard):
    LESSON=LESSON
    TITLE="One in Two Thousand"
    def construct(self):
        self.add(label("BIOCHEMISTRYPEDIA",2.3,TEAL,26),
            T("One Receptor per Neuron:\nHow Olfactory Neurons Choose",28,GREY).move_to([0,1.1,0]))
        self.play(FadeIn(T(self.TITLE,52,font=TITLE_FONT).move_to([0,-.5,0])),run_time=.7)
        self.add(Line([-1.2,-1.5,0],[1.2,-1.5,0],color=GOLD,stroke_width=4));self.finish()


class S01(SpokenScene):
    def construct(self):
        g=magnified();self.add(g)
        self.at("carries about")
        self.play(FadeIn(label("About 1,000 receptor genes",3.25,TEXT,32)),run_time=.35)
        self.at("in each")
        self.play(FadeIn(T("2 genome copies",28,BLUE).move_to([-3.1,-2,0])),run_time=.35)
        self.at("It uses")
        self.play(g[2][2][0].animate.set_stroke(GREEN).set_fill(GREEN,.95),
                  g[0][1].animate.set_opacity(.3),run_time=.5)
        self.at("one gene")
        self.wait(.5)
        self.play(FadeIn(T("How?",42).move_to([-3.1,-3,0])),run_time=.3);self.finish()


class S02(SpokenScene):
    def construct(self):
        self.add(T("1994",78,GOLD).move_to([0,2.65,0]))
        pair=copies(True).scale(.72).move_to([0,-.8,0]);self.add(pair)
        self.add(T("One receptor gene · two alleles",28,GREY).move_to([0,-2.15,0]))
        self.at("Chess and colleagues")
        self.play(FadeIn(T("Chess and colleagues",36).move_to([0,1.35,0])),run_time=.4)
        self.at("in Richard")
        self.play(FadeIn(T("Richard Axel’s laboratory",28,GREY).move_to([0,.65,0])),run_time=.4)
        self.at("made the puzzle")
        self.play(FadeIn(label("One allele per neuron’s receptor RNA",-3.05,ORANGE,32)),run_time=.4);self.finish()


class S03(SpokenScene):
    def construct(self):
        g=copies();self.add(g,label("Two alleles of one receptor gene",3.25,TEXT,32))
        self.add(T("Maternal copy",30,GREY).move_to([-2.8,-1.7,0]),T("Paternal copy",30,GREY).move_to([2.8,-1.7,0]))
        self.at("receptor transcript")
        rna=VGroup(*[Line([-3.2+dx,1.55,0],[-2.95+dx,2.35,0],color=ORANGE,stroke_width=6) for dx in (0,.4,.8)])
        self.play(g[0].animate.set_stroke(GREEN).set_fill(GREEN,.75),FadeIn(rna,shift=UP*.2),
            FadeIn(T("RNA",28,ORANGE).move_to([-1.25,2.1,0])),run_time=.5)
        self.at("just one")
        self.play(FadeIn(label("RNA from one allele",-2.8,ORANGE,32)),run_time=.35);self.finish()


class S04(SpokenScene):
    def construct(self):
        g=magnified();self.add(g,label("About 2,000 candidates",3.25,TEXT,32))
        self.at("A mature neuron")
        self.play(g[2][2][0].animate.set_stroke(GREEN).set_fill(GREEN,.95),g[0][1].animate.set_opacity(.3),run_time=.5)
        c=Circle(radius=.85,color=TEXT).move_to([-3.1,-1.1,0])
        hand=Line(c.get_center(),c.get_center()+UP*.67,color=TEXT,stroke_width=6)
        # Keep the clock below the nucleus and turn continuously while the winner stays lit.
        self.play(g[0].animate.scale(.7).shift(UP*1.3),
            Transform(g[3][1],Line([-1,1,0],[.55,-1.8,0],color=GREY)),run_time=.25)
        self.add(c,hand,T("Choice persists",28,GREEN).move_to([-3.1,-2.45,0]))
        angular_speed=-1.5*PI/(self.narration_s+.4-self.elapsed())
        hand.add_updater(lambda h,dt:h.rotate(angular_speed*dt,about_point=c.get_center()))
        self.at("keeps using it")
        self.finish()
        hand.clear_updaters()


class S05(SpokenScene):
    def construct(self):
        g=copies(True);self.add(g)
        self.add(T("Maternal allele",28,GREY).move_to([-2.8,-1.65,0]),T("Paternal allele",28,GREY).move_to([2.8,-1.65,0]))
        self.at("singular choice")
        self.play(FadeIn(label("Singular choice",3.1,GREEN,42)),run_time=.35)
        self.at("One gene")
        a=T("One gene",30).move_to([-2.8,-2.5,0]);self.play(FadeIn(a),run_time=.3)
        self.at("from one allele")
        b=T("One gene, one allele",30).move_to([-2.8,-2.5,0]);self.play(Transform(a,b),run_time=.3)
        self.at("nearly every")
        self.play(FadeIn(label("Nearly every mature mouse neuron",-3.35,GREY,28)),run_time=.3);self.finish()


class S06(SpokenScene):
    def construct(self):
        g=phases((0,0,1));self.add(g[2])
        self.at("not every stage")
        self.play(FadeIn(g[0]),FadeIn(g[1]),run_time=.5)
        self.at("Picture three broad phases")
        self.play(FadeIn(label("Broad phases · no sharp boundaries",-3.4,GREY,28)),run_time=.35);self.finish()


class S07(SpokenScene):
    def construct(self):
        g=phases();self.add(g)
        self.at("the receptor genes")
        self.play(Transform(g[0],phases((1,0,0))[0]),run_time=.65)
        self.at("little or no")
        self.play(FadeIn(label("Little or no receptor RNA",-3.4,ORANGE,28)),run_time=.35);self.finish()


class S08(SpokenScene):
    def construct(self):
        g=phases((1,0,0));self.add(g)
        self.at("several receptors")
        target=phases((1,1,0))[1]
        rings=VGroup(*list(target[2][9:12]));target[2].remove(*rings)
        self.play(Transform(g[1],target),run_time=.55)
        self.at("single cell data")
        self.play(FadeIn(rings),FadeIn(label("Inferred hubs, from single-cell data",-3.4,TEAL,28)),run_time=.5)
        self.at("competing enhancer hubs")
        self.play(g[1][2][4].animate.set_fill(GREEN,.58).set_stroke(GREEN),
            *[g[1][2][j].animate.set_opacity(.25) for j in (1,6)],
            Transform(g[1][2][-1],T("Then one dominates",26,ORANGE).move_to([0,-2.24,0])),run_time=.65)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        g=phases((1,1,0),True);self.add(g)
        self.at("one gene")
        target=phases((1,1,1),True)[2];ring=target[2][9];target[2].remove(ring)
        self.play(Transform(g[2],target),run_time=.55)
        self.at("feedback helps")
        self.play(FadeIn(ring),FadeIn(label("Feedback helps hold the choice",-3.4,PURPLE,28)),run_time=.45);self.finish()


class S10(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=11.7,height=5.6,corner_radius=.2,color=GREY))
        genes=VGroup(*[tile(BLUE,.9,.25).move_to([(j%4-1.5)*2.5,(1-j//4)*1.6,0]) for j in range(12)])
        lids=VGroup(*[cover(t) for t in genes]);self.add(genes,lids)
        self.at("Suppose each gene")
        self.play(FadeIn(label("Independent escapes?",3.3,TEXT,32)),run_time=.35)
        self.at("small chance")
        for j in (2,8,5):
            self.play(FadeOut(lids[j]),genes[j].animate.set_fill(GREEN,.75).set_stroke(GREEN),run_time=.3)
        self.at("independent of")
        self.play(Indicate(genes[8],color=GREEN),run_time=.5);self.finish()


class S11(SpokenScene):
    def construct(self):
        self.add(label("The toy model’s assumptions",3.15,TEXT,36))
        cards=VGroup(*[chip(t,BLUE,30).move_to([0,y,0]) for t,y in (
            ("Independent small chance",1.7),("Nothing shuts off genes or removes neurons",0),("All counted at one observation time",-1.7))])
        self.add(cards[0])
        self.at("nothing afterwards")
        self.play(FadeIn(cards[1]),run_time=.4)
        self.at("at the same time")
        self.play(FadeIn(cards[2]),run_time=.4)
        self.at("Poisson distribution")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(chart(.1)),FadeIn(slider(.1)),FadeIn(formula()),run_time=.6);self.finish()


class S12(SpokenScene):
    def construct(self):
        self.add(question_frame(False))
        self.at("You can set")
        self.play(Indicate(self.mobjects[0][1][1],color=GOLD),run_time=.5)
        self.at("What is the largest")
        q=question_frame();self.play(*[FadeIn(m) for m in q[3:]],run_time=.4);self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(question_frame())
        # Quiet pulses mark thinking time without adding a new scientific claim.
        ring=Rectangle(width=1.28,height=4.15*poisson(.1)[1]+.18,color=GREEN,stroke_width=3).move_to([-2.15,-1.6+4.15*poisson(.1)[1]/2,0])
        self.add(ring)
        for _ in range(5):
            self.play(ring.animate.set_stroke(opacity=.2),run_time=.5)
            self.play(ring.animate.set_stroke(opacity=1),run_time=.5)


class S14(SpokenScene):
    def construct(self):
        m=ValueTracker(.1)
        g=always_redraw(lambda:chart(m.get_value(),live=True,reference=True))
        s=always_redraw(lambda:slider(m.get_value()));self.add(g,s,formula())
        self.at("In this model")
        # Reach m=1 on “peaks at”; the narration’s answer precedes its causal explanation.
        self.play(m.animate.set_value(1),run_time=max(.5,self.t_of("peaks at")-.2-self.elapsed()),rate_func=linear)
        self.at("peaks at")
        self.play(FadeIn(peak_banner()),run_time=.25)
        self.wait(.35)
        self.play(m.animate.set_value(3),run_time=.65,rate_func=linear)
        self.play(m.animate.set_value(1),run_time=.65,rate_func=linear);self.finish()


class S15Beat(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(chart(1,True,True),slider(1),formula(),peak_banner());self.wait(2.5)


def paired_chart(m,x):
    left=x-1.75;right=x+2.0;base=-1.85;top=2.65;g=VGroup();bars=VGroup()
    g.add(T(f"m = {m:g}",32).move_to([x,.0+3.25,0]),
        Line([left,base,0],[right,base,0],color=GREY),Line([left,base,0],[left,top,0],color=GREY))
    for v in (0,.5,1):
        g.add(T(f"{100*v:.0f}%",26,GREY).move_to([left-.55,base+4.5*v,0]))
    g.add(T("Share of neurons",26,GREY).rotate(PI/2).move_to([left-1.15,.4,0]))
    for i,(dx,p) in enumerate(zip((-.95,.0,.95,1.9),poisson(m))):
        xx=left+.5+i*.92;h=max(.006,4.5*p)
        bars.add(Rectangle(width=.64,height=h,stroke_width=0,fill_color=GREEN if i==1 else BLUE,fill_opacity=.85).move_to([xx,base+h/2,0]))
        g.add(T(("0","1","2","3+")[i],28,GREEN if i==1 else GREY).move_to([xx,-2.2,0]))
    g.add(T("Receptors per neuron",26,GREY).move_to([x+.2,-2.7,0]));return VGroup(g,bars)


class S16(SpokenScene):
    def construct(self):
        rare=paired_chart(.1,-3.25);common=paired_chart(3,3.4)
        # Both complete axes are present before comparing their distributions.
        self.add(rare,common[0])
        self.at("most neurons")
        self.play(FadeIn(T("90% none · 9% one",30,TEXT).move_to([-3.25,-3.4,0])),run_time=.35)
        self.at("much more common")
        self.play(FadeIn(common[1]),
            FadeIn(T("15% one · 80% two or more",28,TEXT).move_to([3.4,-3.4,0])),run_time=.5)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        base,top=-1.9,2.7;left=-4.6
        self.add(label("Exactly one receptor per neuron",3.3,TEXT,34),
            Line([left,base,0],[5.1,base,0],color=GREY),Line([left,base,0],[left,top,0],color=GREY),
            T("Share of neurons",28,GREY).rotate(PI/2).move_to([-6.05,.4,0]))
        for v in (0,.5,1):
            self.add(T(f"{v*100:.0f}%",28,GREY).move_to([-5.2,base+(top-base)*v,0]),
                DashedLine([left,base+(top-base)*v,0],[5.1,base+(top-base)*v,0],color=GREY,stroke_opacity=.25))
        for x,p,c in ((-2.35,poisson(1)[1],BLUE),(2.7,.97,GREEN)):
            h=(top-base)*p
            self.add(Rectangle(width=1.9,height=h,stroke_width=0,fill_color=c,fill_opacity=.85).move_to([x,base+h/2,0]))
        self.add(T("Unregulated model\nat most 37%",28,BLUE).move_to([-2.35,-2.55,0]),
            T("Mature mouse neurons\nnearly all · schematic",28,GREEN).move_to([2.7,-2.55,0]),
            T("37%",30,BLUE).move_to([-2.35,base+4.6/math.e+.25,0]))
        self.at("is insufficient")
        self.play(FadeIn(label("The unregulated model is insufficient",-3.4,TEXT,30)),run_time=.4);self.finish()
        self.wait(1)


class S18(SpokenScene):
    def construct(self):
        g=competition();self.add(g,label("Mouse experiments",3.25,TEXT,34))
        self.at("support competition")
        self.play(FadeIn(T("Competition",30,TEAL).move_to([0,-1.15,0])),
            g[1][1].animate.set_fill(GREEN,.9).set_stroke(GREEN).scale(1.35),
            g[0].animate.set_fill(opacity=.02).set_stroke(opacity=.25),g[2].animate.set_fill(opacity=.02).set_stroke(opacity=.25),run_time=.65)
        self.at("stabilization")
        self.play(FadeIn(Circle(radius=.92,color=PURPLE,stroke_width=6).move_to(g[1][1])),
            FadeIn(T("Stabilization",30,PURPLE).move_to([0,-2.05,0])),run_time=.45)
        self.at("does not identify")
        self.play(FadeIn(label("Arithmetic alone does not identify the mechanism",-3.25,TEXT,28)),run_time=.4);self.finish()


def sequence_panel(i,text):
    x=(-4.3,0,4.3)[i];color=(RED,TEAL,PURPLE)[i]
    panel=RoundedRectangle(width=3.6,height=5.7,corner_radius=.2,color=color,fill_color=color,fill_opacity=.05).move_to([x,-.1,0])
    caption=T(text,26,color)
    if caption.width>3.05:caption.scale_to_fit_width(3.05)
    g=VGroup(panel,caption.move_to([x,-2.3,0]))
    if i==0:
        for j in range(6):
            t=tile(BLUE,.8,.3).move_to([x+(j%2-.5)*1.3,1.55-(j//2)*1.2,0]);g.add(t,cover(t))
    elif i==1:
        for dx,dy in ((-.85,.4),(.85,.4),(0,1.8)):
            g.add(Circle(radius=.63,color=TEAL,fill_color=TEAL,fill_opacity=.08).move_to([x+dx,dy,0]),tile(ORANGE,.65,.35).move_to([x+dx,dy,0]))
    else:
        g.add(tile(GREEN,1.3,.9).move_to([x,.9,0]),bell_icon().move_to([x-.8,-.5,0]),key_icon().scale(.7).set_opacity(.3).move_to([x+.8,-.5,0]))
    return g


class S19(SpokenScene):
    def construct(self):
        sentence=T("Silence → competition → stable choice",42).move_to([0,3.35,0]);self.add(sentence)
        panels=[sequence_panel(i,t) for i,t in enumerate(("Silence every gene","Let a few compete","Hold the winner"))]
        self.add(*[p[0] for p in panels])
        self.at("Silence every gene")
        self.play(sentence.animate.scale(.7),FadeIn(VGroup(*panels[0][1:])),run_time=.45)
        self.at("let a few compete")
        self.play(FadeIn(VGroup(*panels[1][1:])),run_time=.4)
        self.at("lock in the winner")
        self.play(FadeIn(VGroup(*panels[2][1:])),run_time=.4);self.finish()


class S20(SpokenScene):
    def construct(self):
        genes=VGroup(*[tile(BLUE,1,.3).move_to([(j%4-1.5)*2.6,1.5-(j//4)*2.3,0]) for j in range(8)])
        lids=VGroup(*[cover(t) for t in genes]);self.add(genes)
        self.at("Repressive chromatin")
        self.play(LaggedStart(*[FadeIn(t,shift=DOWN*.2) for t in lids],lag_ratio=.05),
            FadeIn(label("Repressive chromatin covers receptor genes",3.25,RED,30)),run_time=.65)
        self.at("A few are")
        self.play(*[FadeOut(lids[j],shift=UP*.8) for j in (1,4,6)],
            *[genes[j].animate.set_fill(ORANGE,.4).set_stroke(ORANGE) for j in (1,4,6)],run_time=.55)
        self.at("enhancer hubs")
        self.play(*[FadeIn(Circle(radius=.83,color=TEAL,stroke_width=4).move_to(genes[j])) for j in (1,4,6)],
            FadeIn(label("Inferred competing enhancer hubs",-3.15,TEAL,30)),run_time=.45);self.finish()


class S21(SpokenScene):
    def construct(self):
        g=competition();g[1][1].set_fill(GREEN,.95).set_stroke(GREEN);self.add(g)
        self.at("RNA helps")
        rna=VGroup()
        for sign in (-1,1):
            for dy in (-.14,.14):
                rna.add(Line([sign*.7,1+dy,0],[sign*2.8,.4+dy,0],color=ORANGE,stroke_width=5))
        self.play(Create(rna),FadeIn(label("RNA helps quiet rivals",3.2,ORANGE,30)),run_time=.45)
        self.at("quiet its rivals")
        self.play(g[0].animate.set_fill(opacity=.02).set_stroke(opacity=.22),g[2].animate.set_fill(opacity=.02).set_stroke(opacity=.22),run_time=.45)
        self.at("receptor protein")
        p=chip("Receptor protein",ORANGE,28).move_to([-1.7,-1.6,0])
        path=arr(g[1][1].get_bottom(),[-1.7,-1.1,0],ORANGE)
        self.play(GrowArrow(path),FadeIn(p,shift=DOWN*.2),run_time=.45)
        self.at("stress signal")
        a=alarm().move_to([2.3,-1.6,0])
        self.play(GrowArrow(arr(p.get_right(),[1.45,-1.6,0],PURPLE)),FadeIn(a),
            FadeIn(T("Stress signal",28,PURPLE).move_to([2.3,-2.95,0])),run_time=.45);self.finish()


class S22(SpokenScene):
    def construct(self):
        win=tile(GREEN,1.25,.95).move_to([-4.2,.4,0]);a=alarm().move_to([-.3,.4,0])
        key=key_icon().scale(1.7).move_to([3.9,.4,0])
        self.add(win,a,key,T("Chosen receptor",28,GREEN).move_to([-4.2,-1.3,0]),
            T("Stress signal",28,PURPLE).move_to([-.3,-1.3,0]),T("Lsd1",34,TEXT).move_to([3.9,-1.3,0]),
            arr([-3.35,.4,0],[-1.3,.4,0],PURPLE),arr([.8,.4,0],[2.4,.4,0],PURPLE))
        self.at("turns down")
        self.play(key.animate.set_opacity(.2),run_time=.6)
        self.at("an enzyme")
        self.play(FadeIn(label("New receptor expression depends on Lsd1",3.2,TEXT,30)),run_time=.4)
        self.at("Further escapes")
        field=candidates(dim=True).scale(.95)
        field[0].set_fill(opacity=.02).set_stroke(opacity=.3)
        field[1].set_opacity(.12)
        field.set_z_index(-5)
        self.play(FadeIn(field),FadeIn(label("Further escapes become rare",-3.2,GREY,32)),run_time=.45);self.finish()


class S23(SpokenScene):
    def construct(self):
        lib=library();self.add(lib)
        self.at("a library")
        self.play(FadeIn(label("A library analogy",3.3,TEXT,34)),run_time=.35)
        self.at("A key frees")
        k=key_icon().move_to([-3,2.6,0]);self.play(FadeIn(k),run_time=.2)
        # The key visits precisely books 2, 4 and 6; no chained book is read.
        for j in (1,3,5):
            self.play(k.animate.move_to([(-4.5+j*1.5),1.7,0]),run_time=.13)
            self.play(FadeOut(lib[1][j]),lib[0][j].animate.set_fill(GREEN,.3).set_stroke(GREEN),run_time=.13)
        self.play(k.animate.move_to([-5.6,2.65,0]),run_time=.15)
        self.at("compete to be read")
        self.play(*[lib[0][i].animate.shift(UP*.25) for i in (1,3,5)],run_time=.4);self.finish()


class S24(SpokenScene):
    def construct(self):
        lib=library(True)
        for i in (1,3,5):lib[0][i].shift(UP*.25)
        k=key_icon().move_to([-5.6,2.65,0]);self.add(lib,k,label("A library analogy",3.3,TEXT,34))
        self.at("loudest reader")
        # Sound begins at the right edge of book 4, above the neighbouring chain.
        waves=VGroup(*[Arc(radius=r,start_angle=-.6,angle=1.2,color=ORANGE,stroke_width=4).shift([.52,1.0,0]) for r in (.18,.32,.46)])
        self.play(lib[0][3].animate.set_fill(GREEN,.75).scale(1.12),Create(waves),run_time=.3)
        self.at("drowns out")
        self.play(*[lib[0][i].animate.scale(.8).set_opacity(.25).shift(DOWN*.4) for i in (1,5)],run_time=.45)
        self.at("a bell rings")
        bell=bell_icon().move_to([5.45,2.65,0])
        self.play(FadeIn(bell),FadeOut(waves),run_time=.2)
        self.play(Rotate(bell,.4),run_time=.12)
        self.play(Rotate(bell,-.8),run_time=.22)
        self.play(Rotate(bell,.4),run_time=.12)
        self.at("key is taken away")
        self.play(k.animate.shift(UP*2).set_opacity(0),run_time=.5)
        self.at("new books rarely")
        self.play(FadeIn(label("New books rarely open",-3.15,GREY,30)),run_time=.35);self.finish()


class S25(SpokenScene):
    def construct(self):
        # Keep the books at full size; pointers map the analogy onto visible objects.
        lib=library(True).shift(DOWN*.25);self.add(lib)
        key=key_icon().move_to([-5.65,2.8,0]);bell=bell_icon().move_to([5.5,2.8,0]);self.add(key,bell)
        self.at("the chains are")
        ch=T("Chains = repressive chromatin",28,RED).move_to([0,-3.2,0])
        self.play(FadeIn(ch),Create(VMobject(color=RED).set_points_as_corners([[-4.98,-.7,0],[-5.55,-.7,0],[-5.55,-2.95,0],[-3.4,-2.95,0]])),run_time=.45)
        self.at("The key is")
        kt=T("Key = Lsd1-dependent\nstep (candidate)",28,GOLD).move_to([-2.4,2.95,0])
        self.play(FadeIn(kt),Create(Line(key.get_right()+RIGHT*.12,kt.get_left()+LEFT*.12,color=GOLD)),run_time=.45)
        self.at("The bell is")
        bt=T("Bell = stress pathway",28,PURPLE).move_to([2.3,2.8,0])
        self.play(FadeIn(bt),Create(Line([4.3,2.8,0],[4.9,2.8,0],color=PURPLE)),run_time=.4)
        # The unspoken extra RNA/hub/lock mappings are deliberately omitted.
        self.finish()


class S26(SpokenScene):
    def construct(self):
        self.add(label("The chapters ahead",3.2,TEXT,38))
        road=VGroup(Line([-4.3,.3,0],[4.3,.3,0],color=GREY),*[Circle(radius=.2,color=GREY).move_to([x,.3,0]) for x in (-4.3,0,4.3)])
        self.add(road)
        self.at("the silence")
        self.play(FadeOut(road),FadeIn(sequence_panel(0,"The silence")),run_time=.35)
        self.at("competing hubs")
        self.play(FadeIn(sequence_panel(1,"Competing hubs")),GrowArrow(Arrow([-2.47,.1,0],[-1.83,.1,0],buff=.02,color=GREY,stroke_width=5)),run_time=.35)
        self.at("and the lock")
        self.play(FadeIn(sequence_panel(2,"The lock")),GrowArrow(Arrow([1.83,.1,0],[2.47,.1,0],buff=.02,color=GREY,stroke_width=5)),run_time=.35);self.finish()


class S27End(EndCard):
    LINE="Silence genes, let a few compete;\nfeedback helps hold the winner."
