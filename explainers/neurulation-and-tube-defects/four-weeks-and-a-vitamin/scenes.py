"""Neurulation and neural tube defects, chapter 3: Four Weeks, and a Vitamin  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole chapter; shared with chapters 1 and 2 where they overlap)
  BLUE   = the neural plate / neural tube (the embryo's structure)
  GREEN  = closed, fused; folic acid and the benefit it gives; the absolute change
  RED    = affected pregnancy, open, failed
  ORANGE = the embryo's clock (days after fertilization)
  TEAL   = the doctor's clock (weeks of pregnancy)
  YELLOW = the thing to look at: the question, the relative figure, caveats
  GREY   = labels, outlines, women who are not highlighted
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# shared geometry: both clocks share one day scale, so day 0 and day 28 line up top to bottom
# ---------------------------------------------------------------------------------------------
def X(day):
    return -2.0 + 0.25 * day


UY = 1.35      # upper clock bar y
LY = -1.35     # lower clock bar y


def tube_icon(closed=True, r=0.4):
    """Cross-section of the neural tube: a closed blue ring with a green seal, or an open ring with a red gap."""
    if closed:
        ring = Circle(radius=r, color=BLUE, stroke_width=9)
        seal = Line([-r * 0.55, r * 0.95, 0], [r * 0.55, r * 0.95, 0], color=GREEN, stroke_width=9)
        return VGroup(ring, seal)
    ring = Arc(radius=r, start_angle=PI / 2 + 0.7, angle=TAU - 1.4, color=BLUE, stroke_width=9)
    gap = Line([-r * 0.7, r * 1.15, 0], [r * 0.7, r * 1.15, 0], color=RED, stroke_width=0)
    tick1 = Line([-r * 0.75, r * 0.65, 0], [-r * 0.95, r * 1.2, 0], color=RED, stroke_width=7)
    tick2 = Line([r * 0.75, r * 0.65, 0], [r * 0.95, r * 1.2, 0], color=RED, stroke_width=7)
    return VGroup(ring, tick1, tick2)


def woman(color=GREY, s=1.0, badge=False):
    head = Circle(radius=0.2 * s, color=color, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0, 0.5 * s, 0])
    body = RoundedRectangle(corner_radius=0.25 * s, width=0.62 * s, height=0.62 * s, color=color,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    g = VGroup(head, body)
    if badge:
        g.add(Circle(radius=0.14 * s, color=RED, fill_color=RED, fill_opacity=1, stroke_width=0)
              .move_to([0.33 * s, 0.62 * s, 0]))
    return g


def mouse(s=1.0):
    body = Ellipse(width=1.7 * s, height=0.95 * s, color=GREY, fill_color=GREY, fill_opacity=0.85, stroke_width=0)
    head = Circle(radius=0.42 * s, color=GREY, fill_color=GREY, fill_opacity=0.85, stroke_width=0).move_to([0.95 * s, 0.12 * s, 0])
    ear = Circle(radius=0.22 * s, color=GREY, fill_color="#B8BEC9", fill_opacity=1, stroke_width=2).move_to([0.8 * s, 0.52 * s, 0])
    nose = Circle(radius=0.07 * s, color=RED, fill_color=RED, fill_opacity=1, stroke_width=0).move_to([1.35 * s, 0.1 * s, 0])
    eye = Circle(radius=0.05 * s, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0).move_to([1.12 * s, 0.22 * s, 0])
    tail = ParametricFunction(lambda t: np.array([(-0.8 - 0.9 * t) * s, (0.12 + 0.45 * t + 0.12 * np.sin(5 * t)) * s, 0]),
                              t_range=[0, 1, 0.02], color=GREY, stroke_width=5)
    return VGroup(tail, body, head, ear, nose, eye)


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw)


def left_at(mob, x, y):
    mob.move_to([x + mob.width / 2, y, 0])
    return mob


def right_at(mob, x, y):
    mob.move_to([x - mob.width / 2, y, 0])
    return mob


# All clock positions are computed on one shared day scale: pregnancy week=(day+14)/7.
def upper_clock(marker=True):
    g = VGroup(Rectangle(width=X(30)-X(0), height=.85, color=ORANGE,
                        fill_color=ORANGE, fill_opacity=.3).move_to([(X(30)+X(0))/2, UY, 0]))
    g.add(lab("days after fertilization", 30, ORANGE).move_to([-2.8, 2.8, 0]))
    for day in (0,7,14,21,28):
        g.add(Line([X(day), UY-.43,0],[X(day), UY-.63,0],color=ORANGE),
              M(str(day),30,ORANGE).move_to([X(day),UY-.94,0]))
    if marker:
        g.add(closure_marker())
    return g


def closure_marker():
    return VGroup(Line([X(28),UY+.43,0],[X(28),2.2,0],color=GREEN,stroke_width=4),
                  tube_icon(True,.4).move_to([X(28),2.7,0]),
                  lab("primary closure\ncomplete",28,GREEN).move_to([2.4,2.7,0]))


def lower_clock():
    g=VGroup(Rectangle(width=X(30)-X(-14),height=.85,color=TEAL,
                      fill_color=TEAL,fill_opacity=.3).move_to([(X(30)+X(-14))/2,LY,0]),
             lab("weeks of pregnancy",30,TEAL).move_to([-2.9,-.35,0]))
    for day in (-14,0,14,28):
        g.add(Line([X(day),LY-.43,0],[X(day),LY-.63,0],color=TEAL),
              M(str((day+14)//7),30,TEAL).move_to([X(day),LY-.94,0]))
    return g


def answer_marker():
    return VGroup(DashedLine([X(28),.1,0],[X(28),LY,0],color=GREEN),
                  Dot([X(28),LY,0],radius=.18,color=GREEN))


def predict_card():
    return VGroup(lab("Pause and predict",34,YELLOW,weight=BOLD).move_to([0,3.4,0]),
                  lab("Weeks of pregnancy at closure?",38,YELLOW).move_to([0,-3.15,0]))


class S00Title(TitleCard):
    LESSON = "Neurulation and neural tube defects"
    TITLE = "Four Weeks, and a Vitamin"

    def construct(self):
        self.add(lab("BIOCHEMISTRYPEDIA",26,TEAL).move_to([0,2,0]),
                 lab("Neurulation and neural tube defects",28,TEXT).move_to([0,1.1,0]),
                 T(self.TITLE,54,GOLD,font=TITLE_FONT).move_to([0,-.2,0]),
                 Line([-1,-1.25,0],[1,-1.25,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(lab("Four Weeks, and a Vitamin",44,GOLD).move_to([0,3.05,0]))
        tl=Arrow([-6.4,-2.5,0],[6.4,-2.5,0],buff=0,color=GREY)
        self.add(tl,lab("time",28,GREY).move_to([5.8,-3.05,0]))
        icon=tube_icon(True,1.5).move_to([3.6,-.45,0])
        self.at("tube closes")
        self.play(FadeIn(icon),Create(Line([3.6,-1.95,0],[3.6,-2.5,0],color=GREEN)),run_time=.45)
        self.add(lab("closed tube",32,GREEN).move_to([3.6,-3.15,0]))
        question=lab("When does prevention have to start?",42,YELLOW).move_to([0,1.9,0])
        self.at("when does prevention")
        self.play(FadeIn(question),FadeIn(Dot([-4.5,-2.5,0],color=YELLOW,radius=.16)),run_time=.5)
        self.finish()


def stage_embryo(lo,hi):
    # Dorsal schematic: broader head, narrowing tail; closure extends between open neuropores.
    outline=VMobject(color=GREY,stroke_width=4)
    outline.set_points_smoothly([[-.55,-2.15,0],[-.9,-1,0],[-1.05,.8,0],[-.65,2.05,0],
                               [0,2.25,0],[.65,2.05,0],[1.05,.8,0],[.9,-1,0],[.55,-2.15,0],[0,-2.35,0],[-.55,-2.15,0]])
    g=VGroup(outline,Line([0,lo,0],[0,hi,0],color=GREEN,stroke_width=12))
    for a,b in ((-2.0,lo),(hi,1.9)):
        if b-a>.05:
            g.add(Ellipse(width=.65,height=b-a,color=BLUE,fill_color=BLUE,fill_opacity=.25,stroke_width=6).move_to([0,(a+b)/2,0]))
    return g


class S02Carnegie(SpokenScene):
    def construct(self):
        specs=[(-4.3,"about Stage 10","folds first meet",-.3,.4),
               (0,"about Stage 11","head-end neuropore\ncloses",-.3,1.9),
               (4.3,"about Stage 12 to 13","tail-end neuropore\ncloses",-2,1.9)]
        groups=[]
        for x,name,desc,lo,hi in specs:
            e=stage_embryo(lo,hi).move_to([x,.25,0])
            groups.append(VGroup(e,lab(name,28,TEXT,weight=BOLD).move_to([x,3.1,0]),
                                 lab(desc,28,TEXT).move_to([x,-2.85,0])))
        self.add(*groups)
        self.at("Carnegie stages")
        self.play(*[Indicate(g[1],scale_factor=1.03) for g in groups],run_time=.5)
        self.at("defined by structure")
        self.play(*[Indicate(g[0][1],color=GREEN,scale_factor=1.05) for g in groups],run_time=.6)
        self.finish()


class S04Clock1(SpokenScene):
    def construct(self):
        # A single enlarged clock fills the first clock scene; zoom to paired scale next scene.
        up=upper_clock(False)
        up.scale(1.12).move_to([0,.45,0])
        question=lab("Primary closure: when?",40,TEXT).move_to([0,-2.25,0])
        self.add(up,question)
        self.at("fourth week")
        label=lab("by the end of about week 4",40,GREEN).move_to([0,-3.1,0])
        # Use the tick's transformed position, rather than the paired-clock coordinates.
        pos=up[-1].get_center()
        icon=tube_icon(True,.65).move_to([pos[0],pos[1]+2.15,0])
        self.play(FadeIn(icon),FadeIn(label),
                  Transform(question,lab("primary closure complete",40,GREEN).move_to(question)),run_time=.45)
        self.finish()


class S05Clock2(SpokenScene):
    def construct(self):
        self.add(upper_clock())
        low=lower_clock()
        self.at("pregnancy")
        self.play(FadeIn(low),run_time=.5)
        self.at("last menstrual period")
        lm=lab("last menstrual\nperiod",26,TEAL).move_to([-5.25,-.3,0])
        # title moves right to make room for the local starting-point label.
        self.play(low[1].animate.move_to([1,-.35,0]),FadeIn(lm),run_time=.4)
        self.at("starts about two weeks")
        br=VGroup(DoubleArrow([X(-14),-2.8,0],[X(0),-2.8,0],buff=0,color=TEAL),
                  lab("about 2 weeks earlier",28,TEAL).move_to([-3.75,-3.4,0]),
                  DashedLine([X(0),.1,0],[X(0),-.9,0],color=GREY))
        self.play(FadeIn(br),run_time=.5)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        self.add(upper_clock(),lower_clock(),predict_card())
        self.at("doctor's clock")
        self.play(Indicate(self.mobjects[1][0],color=TEAL,scale_factor=1.02),run_time=.6)
        self.finish()


class S07Pause(SpokenScene):
    def construct(self):
        self.add(upper_clock(),lower_clock(),predict_card())
        self.wait(self.narration_s)


class S08Rev(SpokenScene):
    def construct(self):
        self.add(upper_clock(),lower_clock())
        self.at("about six weeks")
        ans=lab("about 6 weeks",38,GREEN,weight=BOLD).move_to([2.5,-3.15,0])
        self.play(FadeIn(answer_marker()),FadeIn(ans),run_time=.45)
        self.at("many pregnancies")
        band=Rectangle(width=1.2,height=1.15,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).move_to([X(28),LY,0])
        msg=lab("often not yet recognized\nat about 6 weeks",30,YELLOW).move_to([-2.8,-3.05,0])
        self.play(FadeIn(band),FadeIn(msg),run_time=.45)
        self.finish()


class S09So(SpokenScene):
    def construct(self):
        clocks=VGroup(upper_clock(),lower_clock(),answer_marker())
        # Increase the separation of the clock rows without stretching the text.
        clocks[0].shift(UP*.25)
        clocks[1].shift(DOWN*.3)
        clocks[2].become(VGroup(
            DashedLine([X(28),.35,0],[X(28),LY-.3,0],color=GREEN),
            Dot([X(28),LY-.3,0],radius=.18,color=GREEN)))
        self.add(clocks)
        self.at("the vitamin")
        bar=Rectangle(width=X(28)-X(-17),height=.34,color=GREEN,fill_color=GREEN,fill_opacity=.7).move_to([(X(28)+X(-17))/2,-3.0,0])
        cap=lab("folic acid, from before conception",32,GREEN).move_to([0,-3.6,0])
        self.play(GrowFromEdge(bar,LEFT),FadeIn(cap),run_time=.45)
        self.finish()


def women_grid(cols,rows,sx,sy,s,cx,cy,badge=False,color=GREY):
    return [woman(color,s,badge).move_to([cx+(c-(cols-1)/2)*sx,cy-(r-(rows-1)/2)*sy,0])
            for r in range(rows) for c in range(cols)]


def credit(text,size=28):
    return lab(text,size,GOLD).move_to([0,3.2,0])


def mrc_group():
    return VGroup(*women_grid(6,2,1.65,1.9,1.45,0,.45,badge=True))


class S11Mrc(SpokenScene):
    def construct(self):
        self.add(credit("Medical Research Council Vitamin Study, 1991"),
                 lab("12 shown for illustration",26,TEXT).move_to([0,2.5,0]))
        ws=mrc_group()
        for w in ws: w[2].set_opacity(0)
        self.add(ws)
        self.at("had already had")
        self.play(*[w[2].animate.set_opacity(1) for w in ws],run_time=.45)
        self.add(lab("each had a previous affected pregnancy",30,RED).move_to([0,-2.25,0]))
        self.at("risk was high")
        self.play(FadeIn(lab("high risk of another",36,RED,weight=BOLD).move_to([0,-3.1,0])),run_time=.4)
        self.finish()


class S12Mrc2(SpokenScene):
    def construct(self):
        ws=mrc_group()
        self.add(credit("Medical Research Council Vitamin Study, 1991"),ws,
                 lab("12 shown for illustration",26,TEXT).move_to([0,2.5,0]))
        ch=chip("folic acid, 4 mg a day, from before conception",GREEN,28).move_to([0,-2.9,0])
        self.at("folic acid")
        self.play(FadeIn(ch),run_time=.4)
        self.at("cut recurrence")
        self.remove(ws,self.mobjects[2])
        big=M("about 72%",104,GREEN,weight=BOLD).move_to([0,.7,0])
        sub=lab("fewer recurrences",44,TEXT).move_to([0,-.8,0])
        self.play(FadeIn(big),FadeIn(sub),run_time=.45)
        self.finish()


class S13Rel(SpokenScene):
    def construct(self):
        ds=VGroup(*[Dot([-3.1+(c-4.5)*.59,-.1-(r-4.5)*.59,0],radius=.21,color=GREY)
                    for r in range(10) for c in range(10)])
        q=lab("72 of every 100 women?",32,TEXT).move_to([-3.1,3.25,0])
        rel=chip("relative change",GREY,32).move_to([3.45,1.25,0])
        ab=chip("absolute change",GREY,32).move_to([3.45,-1.25,0])
        self.add(ds,q,rel,ab)
        self.at("of every")
        self.play(*[d.animate.set_color(GREEN) for d in ds[:72]],run_time=.45)
        # Alignment transcribes the spoken "No" as "Now"; anchor to the preceding words.
        self.at("women spared", lead=-1.42)
        no=lab("No.",60,RED,weight=BOLD).move_to([3.45,0,0])
        self.play(FadeIn(no),*[d.animate.set_color(GREY) for d in ds],run_time=.35)
        self.at("that is a relative")
        self.play(rel.animate.set_color(YELLOW),FadeOut(no),run_time=.4)
        self.finish()


# Heights are derived from the narrated trial rates, affected pregnancies per 100.
BASE=-2.6
RATE_WITHOUT=3.5
RATE_WITH=1.0
UNIT=1.25
BX1=-2.75
BX2=.35


def chart_static():
    g=VGroup(lab("affected pregnancies",30,TEXT).move_to([-2,3.2,0]),
             lab("per 100 pregnancies",28,TEXT).rotate(PI/2).move_to([-6.1,-.1,0]))
    for v in range(5):
        y=BASE+v*UNIT
        g.add(lab(str(v),28,TEXT).move_to([-5.55,y,0]),
              Line([-5.2,y,0],[1.7,y,0],color=GREY,stroke_opacity=.28))
    g.add(Line([-5.2,BASE,0],[-5.2,2.4,0],color=GREY),
          lab("without\nfolic acid",28,TEXT).move_to([BX1,-3.25,0]),
          lab("with\nfolic acid",28,GREEN).move_to([BX2,-3.25,0]))
    return g


def bar_mob(x,v):
    return Rectangle(width=1.6,height=v*UNIT,color=RED,fill_color=RED,fill_opacity=.8).move_to([x,BASE+v*UNIT/2,0])


def value_label(x,v,text):
    # Solid background masks chart gridlines behind labels.
    t=lab(text,32,TEXT).move_to([x,BASE+v*UNIT+.35,0])
    bg=BackgroundRectangle(t,color=BG,fill_opacity=1,buff=.09)
    return VGroup(bg,t)


def s15_chart_group():
    return VGroup(chart_static(),bar_mob(BX1,RATE_WITHOUT),bar_mob(BX2,RATE_WITH),
                  value_label(BX1,RATE_WITHOUT,"about 3.5"),value_label(BX2,RATE_WITH,"about 1"))


def s15_notes():
    top=BASE+RATE_WITHOUT*UNIT; bottom=BASE+RATE_WITH*UNIT
    lines=VGroup(DashedLine([BX1+.8,top,0],[2.1,top,0],color=GREEN),
                 DashedLine([BX2+.8,bottom,0],[2.1,bottom,0],color=GREEN))
    br=DoubleArrow([2.1,bottom,0],[2.1,top,0],buff=0,color=GREEN)
    ab=lab("about 2.5\npercentage points\nfewer",38,GREEN).move_to([4.35,.1,0])
    rl=lab("about 72% fewer\n(relative)",38,YELLOW).move_to([4.35,2.65,0])
    return lines,br,ab,rl


class S14Abs(SpokenScene):
    def construct(self):
        b1=bar_mob(BX1,RATE_WITHOUT)
        self.add(chart_static(),b1,value_label(BX1,RATE_WITHOUT,"about 3.5"))
        self.at("without folic acid")
        self.play(Indicate(b1,scale_factor=1.03),run_time=.4)
        self.at("with it")
        self.play(GrowFromEdge(bar_mob(BX2,RATE_WITH),DOWN),FadeIn(value_label(BX2,RATE_WITH,"about 1")),run_time=.45)
        self.finish()


class S15Abs2(SpokenScene):
    def construct(self):
        self.add(s15_chart_group())
        lines,br,ab,rl=s15_notes()
        self.at("absolute fall")
        self.play(Create(lines),FadeIn(br),FadeIn(ab),run_time=.5)
        self.at("relative figure")
        self.play(FadeIn(rl),run_time=.4)
        self.finish()


class S16Beat(SpokenScene):
    def construct(self):
        self.add(s15_chart_group(),*s15_notes())
        self.finish()


class S17First(SpokenScene):
    def construct(self):
        self.add(lab("mothers with no earlier affected pregnancy",32,TEXT).move_to([0,3.25,0]),
                 lab("most affected babies",34,YELLOW).move_to([0,2.45,0]))
        ws=VGroup(*women_grid(8,3,1.2,1.5,.95,-1,-.15))
        self.add(ws)
        self.at("can a first case")
        q=chip("Can a first case be prevented?",YELLOW,36).move_to([0,-3.25,0])
        self.play(FadeIn(q),FadeIn(lab("?",136,YELLOW,weight=BOLD).move_to([5.1,-.15,0])),run_time=.5)
        self.finish()


def hung_boxes():
    g=VGroup()
    for x,color,name in [(-3.25,GREEN,"multivitamin"),(3.25,GREY,"trace elements")]:
        g.add(RoundedRectangle(width=5.8,height=4.1,corner_radius=.2,color=color).move_to([x,.1,0]),
              lab(name,32,color,weight=BOLD).move_to([x,1.6,0]))
    g.add(lab("with 0.8 mg folic acid",28,GREEN).move_to([-3.25,.9,0]))
    return g


def hung_static():
    return VGroup(credit("Czeizel and Dudás, 1992"),hung_boxes(),
                  *women_grid(4,2,1.05,1.1,.9,-3.25,-.55),
                  *women_grid(4,2,1.05,1.1,.9,3.25,-.55),
                  lab("group icons for illustration; not participant counts",26,TEXT).move_to([0,2.5,0]))


class S18Hung(SpokenScene):
    def construct(self):
        # Both arms, labels, and the count disclaimer are present from the first frame.
        g=hung_static(); self.add(g)
        self.at("took a multivitamin")
        self.play(Indicate(g[1][0],scale_factor=1.02,color=GREEN),run_time=.45)
        self.at("or trace elements")
        self.play(Indicate(g[1][2],scale_factor=1.02,color=GREY),run_time=.45)
        self.finish()


class S19Hung2(SpokenScene):
    def construct(self):
        self.add(hung_static())
        self.at("six affected")
        self.play(FadeIn(lab("6 affected",38,RED,weight=BOLD).move_to([3.25,-2.8,0])),run_time=.4)
        self.at("and none")
        self.play(FadeIn(lab("0 affected",38,GREEN,weight=BOLD).move_to([-3.25,-2.8,0])),run_time=.4)
        self.finish()


class S20Cave(SpokenScene):
    def construct(self):
        left=VGroup(RoundedRectangle(width=5.8,height=5.4,corner_radius=.2,color=YELLOW).move_to([-3.25,0,0]),
                    lab("small numbers",36,YELLOW).move_to([-3.25,2,0]),
                    lab("6",68,RED).move_to([-3.25,.9,0]),
                    lab("trace elements",30,TEXT).move_to([-3.25,.1,0]),
                    lab("vs 0",58,GREEN).move_to([-3.25,-.9,0]),
                    lab("multivitamin",30,TEXT).move_to([-3.25,-1.8,0]))
        self.add(left)
        self.at("a multivitamin cannot")
        right=VGroup(RoundedRectangle(width=5.8,height=5.4,corner_radius=.2,color=YELLOW).move_to([3.25,0,0]),
                     lab("not folic acid alone",32,YELLOW).move_to([3.25,2,0]),
                     chip("folic acid",GREEN,32).move_to([3.25,.6,0]),
                     lab("+",44,TEXT).move_to([3.25,-.3,0]),
                     chip("other vitamins",GREY,32).move_to([3.25,-1.3,0]))
        self.play(FadeIn(right),run_time=.45)
        self.finish()


class S21Open(SpokenScene):
    def construct(self):
        card=lab("Folic acid lowers risk,\ndoes not remove it",44,TEXT).move_to([0,2.3,0])
        bars=VGroup()
        for x,h,label in [(-2.7,2.9,"without folic acid"),(2.7,.85,"with folic acid")]:
            bars.add(Rectangle(width=1.65,height=h,color=RED,fill_color=RED,fill_opacity=.8).move_to([x,-2+h/2,0]),
                     lab(label,28,TEXT).move_to([x,-2.6,0]))
        bars.add(Line([-5,-2,0],[5,-2,0],color=GREY),lab("schematic risk; not to scale",26,GREY).move_to([0,-3.35,0]))
        self.add(card,bars)
        self.at("does not remove")
        nz=lab("remaining risk",32,YELLOW).move_to([2.7,-.4,0])
        self.play(FadeIn(nz),run_time=.4)
        self.at("most mothers")
        self.remove(card,bars,nz)
        # Qualitative gauge only. No sample dots or invented measured proportion.
        title=lab("mothers of affected babies",40,TEXT).move_to([0,2.7,0])
        small=Rectangle(width=.7,height=1.6,color=RED,fill_color=RED,fill_opacity=.45).move_to([-5.15,0,0])
        large=Rectangle(width=10.3,height=1.6,color=GREEN,fill_color=GREEN,fill_opacity=.3).move_to([.35,0,0])
        dl=lab("deficient",28,RED).move_to([-4.65,-1.55,0])
        lead=Line([-5.15,-.8,0],[-4.65,-1.25,0],color=RED)
        nl=lab("not deficient\nby ordinary tests",34,GREEN).move_to([1,-1.75,0])
        self.add(title,small,large,dl,lead,nl,
                 lab("schematic, not to scale",28,YELLOW).move_to([0,1.5,0]))
        self.at("not folate deficient")
        self.play(Indicate(nl,color=GREEN,scale_factor=1.04),run_time=.45)
        self.finish()


def mice_picture():
    g=VGroup(lab("some mouse mutants",36,TEXT).move_to([0,3.25,0]))
    for x,closed,label,color in [(-3.25,True,"folate-responsive",GREEN),(3.25,False,"folate-resistant",RED)]:
        m=mouse(1.1).move_to([x,1.8,0])
        if not closed:
            # A diagram tint distinguishes the response groups, not an anatomical trait.
            m[1].set_color(RED); m[2].set_color(RED)
        tube=tube_icon(closed,.7).move_to([x,-.65,0])
        # Route the connection beside the label, from the mouse to its tube.
        leader=VMobject(color=color,stroke_width=3).set_points_as_corners(
            [[x+1.45,1.5,0],[x+2.25,1.5,0],[x+2.25,-.65,0],[x+.85,-.65,0]])
        g.add(m,lab(label,30,color).move_to([x,.65,0]),tube,leader)
    return g


def unknown_card(show_answer=True):
    g=VGroup(RoundedRectangle(width=10.8,height=1.4,corner_radius=.2,color=YELLOW).move_to([0,-2.65,0]),
             lab("How does folate work?",36,TEXT).move_to([0,-2.35,0]))
    if show_answer:
        g.add(lab("Not known",34,YELLOW).move_to([0,-3,0]))
    return g


class S22Mice(SpokenScene):
    def construct(self):
        pic=mice_picture()
        # Begin with visible mice and caption, then reveal each response when named.
        self.add(pic[0],pic[1],pic[5])
        self.at("some mutants respond")
        self.play(*[FadeIn(pic[i]) for i in (2,3,4)],run_time=.45)
        self.at("others do not")
        self.play(*[FadeIn(pic[i]) for i in (6,7,8)],run_time=.45)
        self.at("how folate prevents")
        self.play(FadeIn(unknown_card(False)),run_time=.45)
        self.at("still not known")
        self.play(FadeIn(lab("Not known",34,YELLOW).move_to([0,-3,0])),run_time=.4)
        self.finish()


class S23Beat(SpokenScene):
    def construct(self):
        self.add(mice_picture(),unknown_card())
        self.finish()


def takeaway_clock():
    # Weeks of pregnancy; negative weeks give an explicit pre-conception region.
    def wx(w): return -5.6+(w+1)*1.4
    y=-.2
    g=VGroup(lab("weeks of pregnancy",34,TEAL).move_to([0,-1.7,0]),
             Line([wx(-1),y,0],[wx(7),y,0],color=TEAL,stroke_width=5))
    for w in range(0,8,2):
        g.add(Line([wx(w),y-.15,0],[wx(w),y+.15,0],color=TEAL),
              M(str(w),30,TEAL).move_to([wx(w),-.85,0]))
    # Conception is about pregnancy week 2, not pregnancy week 0.
    g.add(lab("conception",28,ORANGE).move_to([wx(2),.65,0]),
          Line([wx(2),.4,0],[wx(2),y+.15,0],color=ORANGE))
    return g,wx


class S24Take(SpokenScene):
    def construct(self):
        g,wx=takeaway_clock(); self.add(g)
        self.at("the tube often closes")
        mk=VGroup(tube_icon(True,.65).move_to([wx(6),1.7,0]),
                  Line([wx(6),1,0],[wx(6),0,0],color=GREEN),
                  lab("closure by about week 6",38,GREEN).move_to([1.4,3.1,0]))
        self.play(FadeIn(mk),run_time=.45)
        self.at("before a woman knows")
        msg=lab("often before pregnancy is known",40,YELLOW).move_to([0,-2.7,0])
        self.play(FadeIn(msg),run_time=.45)
        self.at("folic acid must")
        bar=Rectangle(width=wx(1.7)-wx(-1),height=.38,color=GREEN,fill_color=GREEN,fill_opacity=.65).move_to([(wx(1.7)+wx(-1))/2,1.6,0])
        label=lab("folic acid,\nbefore conception",36,GREEN).move_to([-3.6,2.65,0])
        self.play(GrowFromEdge(bar,LEFT),FadeIn(label),run_time=.45)
        self.finish()


class S25End(EndCard):
    LINE = "The tube often closes before pregnancy is known: folic acid comes first."

    def construct(self):
        line=lab("The tube often closes\nbefore pregnancy is known:\nfolic acid comes first.",58,TEXT).move_to([0,1.65,0])
        # Keep the correct pregnancy clock visible under the final statement.
        clock,wx=takeaway_clock()
        clock.scale(.85).move_to([0,-2.0,0])
        def end_pos(w,y): return [wx(w)*.85,-2.0+(y+.46)*.85,0]
        bar=Line(end_pos(-1,.35),end_pos(1.7,.35),color=GREEN,stroke_width=12)
        closure=tube_icon(True,.28).move_to(end_pos(6,.65))
        self.add(line,clock,bar,closure,
                 lab("biochemistrypedia.com",26,TEAL).move_to([0,-3.4,0]))
        self.finish()
