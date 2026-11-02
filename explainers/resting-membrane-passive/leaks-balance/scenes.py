"""Where the Leaks Balance — revised chapter 2.
COLOR MAP: BLUE potassium (K+, EK, gK, PK); ORANGE sodium (Na+, ENa,
gNa, PNa); YELLOW voltage; GREEN balance / zero current; PURPLE pump;
GREY structures and secondary terms. Neutral white for instructional cues.
Rope positions, force arrows and gap bars are computed from sum(gE)/sum(g).
Rope stroke widths share a linear conductance scale within each scene (minimum 10).
The scale-all view uses a smaller shared scale to keep doubled ropes inside the pins.
"""
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
MUTED = "#BBC2CE"
KC, NAC, VC, NETC = BLUE, ORANGE, YELLOW, GREEN
EK, ENA, GK, GNA = -95., 60.6, 8.47, 1.53

def balance(gk=GK, gna=GNA):
    return (gk*EK + gna*ENA)/(gk+gna)
REST = balance()

def X(v):
    return -5.3 + (v-EK)/(ENA-EK)*10.6

def label(text, y=3.05, size=34, color=TEXT):
    return fit(T(text,size,color),12.2).move_to([0,y,0])

def bchip(text, color=TEXT, size=28, **kw):
    c=chip(text,color,size=size,**kw)
    back=RoundedRectangle(corner_radius=.14,width=c[0].width,height=c[0].height,
                          stroke_width=0,fill_color=BG,fill_opacity=1).move_to(c[0])
    return VGroup(back,*c)

class Rope(VGroup):
    def __init__(self,v=REST,gk=GK,gna=GNA,readout=None,numbers=False,stroke_scale=12.5,readout_y=2.05):
        super().__init__()
        self.stroke_scale=stroke_scale
        self.readout_y=readout_y
        self.k=Line([-5.3,.45,0],[X(v),.45,0],color=KC,stroke_width=max(10,stroke_scale*gk))
        self.na=Line([X(v),.45,0],[5.3,.45,0],color=NAC,stroke_width=max(10,stroke_scale*gna))
        self.pins=VGroup(*[Line([x,-.8,0],[x,1.45,0],color=c,stroke_width=8)
                               for x,c in [(-5.3,KC),(5.3,NAC)]])
        self.ends=VGroup(T("EK  −95 mV",28,KC).move_to([-4.65,-1.12,0]),
                         T("ENa  +60.6 mV",28,NAC).move_to([4.5,-1.12,0]))
        self.dot=VGroup(Line([X(v),-.25,0],[X(v),1.1,0],color=VC,stroke_width=9),
                        Square(side_length=.42,color=VC,fill_color=VC,fill_opacity=1).rotate(PI/4).move_to([X(v),.45,0]))
        self.readout=T(readout or "Vm ?",32,VC).move_to([np.clip(X(v),-4.5,4.5),readout_y,0])
        self.add(self.k,self.na,self.pins,self.ends,self.dot,self.readout)
        if numbers:
            self.add(rope_numbers())

    def change(self,scene,v,gk=GK,gna=GNA,seconds=1.1,readout=None):
        new=Rope(v,gk,gna,readout or "Vm",stroke_scale=self.stroke_scale,readout_y=self.readout_y)
        scene.play(Transform(self.k,new.k),Transform(self.na,new.na),
                   Transform(self.dot,new.dot),Transform(self.readout,new.readout),run_time=seconds)

def rope_numbers():
    return VGroup(M("gK = 8.47 nS",28,KC).move_to([-3.6,1.35,0]),
                  M("gNa = 1.53 nS",28,NAC).move_to([3.45,1.35,0]))

def pulls(v=REST,gk=GK,gna=GNA):
    # Ohm's law; a shared scale maps pA to arrow length.
    ik,ina=gk*(v-EK),gna*(ENA-v)
    scale=5.2/max(ik,ina)
    x=X(v)
    # Stack the opposing vectors, each centred below the voltage marker.
    # A shared scale preserves the current magnitudes; neither vector clips at EK.
    return VGroup(Arrow([x+ik*scale/2,-1.85,0],[x-ik*scale/2,-1.85,0],buff=0,
                        color=KC,stroke_width=54,tip_length=.65,max_stroke_width_to_length_ratio=30,
                        max_tip_length_to_length_ratio=.18),
                  Arrow([x-ina*scale/2,-2.5,0],[x+ina*scale/2,-2.5,0],buff=0,
                        color=NAC,stroke_width=54,tip_length=.65,max_stroke_width_to_length_ratio=30,
                        max_tip_length_to_length_ratio=.18))

def gaps():
    x=X(REST)
    # Main gap ruler uses the very same voltage-to-position mapping as the ropes.
    lines=VGroup(Line([-5.3,-1.9,0],[x,-1.9,0],color=KC,stroke_width=14),
                 Line([x,-1.9,0],[5.3,-1.9,0],color=NAC,stroke_width=14))
    ticks=VGroup(*[Line([a,-1.65,0],[a,-2.1,0],color=TEXT,stroke_width=3) for a in [-5.3,x,5.3]])
    nums=VGroup(M(f"{REST-EK:.1f} mV",28,KC).move_to([-4.5,-2.55,0]),
                M(f"{ENA-REST:.1f} mV",28,NAC).move_to([.85,-2.55,0]))
    return VGroup(lines,ticks,nums)

def predict():
    return VGroup(Rope(v=0,numbers=True),label("Which end, and how far along?"),
                  T("Pause",28,TEXT).move_to([0,-2.9,0]))

def algebra():
    colors={"gK":KC,"gNa":NAC}
    return VGroup(fit(M("gK (Vm − EK) + gNa (Vm − ENa) = 0",42,t2c=colors),12).move_to([0,1.1,0]),
                  fit(M("Vm (gK + gNa) = gK EK + gNa ENa",42,t2c=colors),12).move_to([0,-.65,0]))

def average(extra=False):
    colors={"gK":KC,"gNa":NAC,"gX":MUTED,"EX":MUTED}
    top=M("gK EK + gNa ENa"+(" + gX EX" if extra else ""),36,t2c=colors)
    bot=M("gK + gNa"+(" + gX" if extra else ""),36,t2c=colors)
    top.move_to([.7,.5,0]); bot.move_to([.7,-.65,0])
    w=max(top.width,bot.width)+.4
    bar=Line([.7-w/2,-.05,0],[.7+w/2,-.05,0],color=TEXT,stroke_width=3)
    eq=M("Vm =",36,VC).next_to(bar,LEFT,buff=.4)
    body=VGroup(eq,top,bar,bot)
    box=SurroundingRectangle(body,color=NETC,buff=.4,corner_radius=.18)
    return VGroup(body,box).scale(1.25).move_to([0,-.1,0])

def ghk(colored=False,numeric=False):
    colors={"PK[K]o":KC,"PK[K]i":KC,"PNa[Na]o":NAC,"PNa[Na]i":NAC,
            "PCl[Cl]i":GREY,"PCl[Cl]o":GREY} if colored else {}
    top=M("4 + 0.04 × 145 = 9.8" if numeric else "PK[K]o + PNa[Na]o + PCl[Cl]i",30,t2c=colors)
    bot=M("140 + 0.04 × 15 = 140.6" if numeric else "PK[K]i + PNa[Na]i + PCl[Cl]o",30,t2c=colors)
    top.move_to([.4,.6,0]); bot.move_to([.4,-.65,0])
    bar=Line([-4.45,0,0],[5.25,0,0],color=TEXT,stroke_width=3)
    prefix=M("Vm = (RT/F) ×",36,VC).move_to([0,2.0,0])
    ln=M("ln",36).move_to([-6,0,0])
    par=VGroup(T("(",100).stretch_to_fit_height(2.4).move_to([-5.1,0,0]),
               T(")",100).stretch_to_fit_height(2.4).move_to([5.8,0,0]))
    return VGroup(prefix,top,bar,bot,par,ln)

def ratios():
    a=VGroup(T("Permeability",34),M("1 : 0.04",42),T("K : Na",28,MUTED)).arrange(DOWN,buff=.42).move_to([-3.1,1.5,0])
    b=VGroup(T("Conductance",34),M("8.47 : 1.53",38),M("≈ 1 : 0.18",30,MUTED)).arrange(DOWN,buff=.42).move_to([3.1,1.5,0])
    # Anchor both headings and primary ratios to exactly the same baselines.
    for group in [a,b]:
        group[0].align_to([0,2.6,0],UP); group[1].set_y(1.35); group[2].set_y(.4)
    return VGroup(a,b)

def membrane(flat=False):
    kfill=Rectangle(width=11.8,height=1.8,stroke_width=0,fill_color=KC,fill_opacity=.09 if flat else .38).move_to([0,-1.15,0])
    nfill=Rectangle(width=11.8,height=1.8,stroke_width=0,fill_color=NAC,fill_opacity=.09 if flat else .38).move_to([0,1.15,0])
    mem=Rectangle(width=11.8,height=.5,color=MUTED,fill_color=GREY,fill_opacity=.35)
    names=VGroup(T("OUTSIDE",28,TEXT).move_to([-4.7,2.4,0]),T("INSIDE",28,TEXT).move_to([-4.9,-2.4,0]))
    channels=VGroup(bchip("K+ leak",KC).move_to([-3.6,0,0]),bchip("Na+ leak",NAC).move_to([-1,0,0]))
    return VGroup(kfill,nfill,mem,names,channels)

def pump_shape():
    # Protein cartoon, no atom/bond geometry. Two moving gates expose the cavity.
    blob=VMobject(stroke_color=PURPLE,stroke_width=5,fill_color=PURPLE,fill_opacity=.35)
    blob.set_points_smoothly([[-.6,-1,0],[-.9,-.4,0],[-.65,.4,0],[-.65,.95,0],
                              [0,1.18,0],[.65,.95,0],[.65,.4,0],[.9,-.4,0],[.6,-1,0],[-.6,-1,0]])
    inner=Line([-.5,-.8,0],[.5,-.8,0],color=PURPLE,stroke_width=10)
    outer=Line([-.5,.8,0],[.5,.8,0],color=PURPLE,stroke_width=10)
    return VGroup(blob,inner,outer).move_to([2.7,0,0])

class S00Title(TitleCard):
    LESSON="The Resting Membrane and Passive Signals"
    TITLE="Where the Leaks Balance"

class S01Question(SpokenScene):
    def construct(self):
        r=Rope(v=0,readout="?"); self.add(r)
        self.at("Potassium has")
        self.play(Indicate(r.k,color=KC,scale_factor=1.02),run_time=.7)
        self.at("So why")
        self.play(FadeIn(label("Why not rest at potassium’s mark?")),run_time=.5)
        self.finish()

class S02Ropes(SpokenScene):
    def construct(self):
        r=Rope(v=0,readout="Vm  0 mV")
        name=T("Potassium",28,KC).move_to([-3.6,1.35,0])
        self.add(r,label("Two leaks, one balance"),name)
        nums=rope_numbers()
        self.at("Back to the scale")
        self.play(Indicate(r.pins,scale_factor=1.02),run_time=.5)
        self.at("Potassium's rope")
        self.play(Transform(name,nums[0]),run_time=.45)
        self.at("Sodium's rope")
        self.play(FadeIn(nums[1]),run_time=.45)
        self.finish()

class S03Settle(SpokenScene):
    def construct(self):
        r=Rope(v=0,gk=GNA,gna=GNA,readout="Vm")
        self.add(r,label("Equal ropes: the principle"),
                 T("Imagine equal ropes",30,TEXT).move_to([2.9,1.35,0]))
        self.at("The marker slides")
        mid=balance(GNA,GNA)
        r.change(self,mid,gk=GNA,gna=GNA,seconds=1.7)
        self.at("equal and opposite")
        self.play(FadeIn(pulls(mid,GNA,GNA)),run_time=.5)
        self.at("That spot")
        self.play(FadeIn(label("balance point",-3.4,36,NETC)),run_time=.5)
        self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        p=predict(); self.add(p[0])
        self.at("Which end")
        self.play(FadeIn(p[1]),run_time=.4)
        self.at("And roughly")
        self.play(FadeIn(p[2]),run_time=.4)
        self.finish()

class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(predict())
        ring=Circle(radius=.55,color=MUTED,stroke_width=5).move_to([1.65,-2.85,0])
        arc=Arc(radius=.55,start_angle=PI/2,angle=TAU,color=VC,stroke_width=7).move_arc_center_to([1.65,-2.85,0])
        self.add(ring,arc)
        self.play(UpdateFromAlphaFunc(arc,lambda m,a:m.become(Arc(radius=.55,start_angle=PI/2,
                  angle=max(.001,TAU*(1-a)),color=VC,stroke_width=7).move_arc_center_to([1.65,-2.85,0]))),run_time=5,rate_func=linear)

class S06Reveal1(SpokenScene):
    def construct(self):
        r=Rope(v=0); self.add(r)
        self.at("Nearer potassium")
        cue=label("Nearer potassium",color=KC)
        self.play(FadeIn(cue),run_time=.3)
        r.change(self,REST,seconds=.8)
        self.at("are equal")
        self.play(FadeIn(pulls()),run_time=.45)
        self.at("the thin rope")
        self.play(Transform(cue,label("Longer gap, smaller conductance")),run_time=.5)
        self.finish()

class S07Reveal2(SpokenScene):
    def construct(self):
        r=Rope()
        ratio=label("8.47 / 1.53 ≈ 5.5",size=38)
        # Set the ratio as stable text from frame zero; no morphing glyph artefacts.
        self.add(r,ratio)
        x=X(REST)
        bracket=VGroup(
            Line([-5.3,-1.75,0],[x,-1.75,0],color=KC,stroke_width=10),
            Line([x,-1.75,0],[5.3,-1.75,0],color=NAC,stroke_width=10),
            *[Line([v,-1.4,0],[v,-2.1,0],color=TEXT,stroke_width=4)
              for v in [-5.3,x,5.3]])
        self.add(bracket,T("Total gap: 155.6 mV",26,MUTED).move_to([.8,-.7,0]))
        self.at("Potassium's rope")
        self.at("times stronger")
        self.play(Indicate(ratio,color=TEXT,scale_factor=1.04),run_time=.6)
        self.at("So the marker")
        self.add(label("5.5 times closer to EK",1.35,32))
        # One common unit makes the short and long gaps directly comparable.
        unit=.95
        bars=VGroup()
        for y,n,c,txt in [(-2.5,1,KC,f"1 unit · {REST-EK:.1f} mV"),
                           (-3.2,(ENA-REST)/(REST-EK),NAC,
                            f"5.5 units · {ENA-REST:.1f} mV")]:
            bar=Rectangle(width=n*unit,height=.34,stroke_width=0,
                          fill_color=c,fill_opacity=1).move_to([-5.3+n*unit/2,y,0])
            divisions=VGroup(*[Line([-5.3+i*unit,y-.17,0],[-5.3+i*unit,y+.17,0],
                                    color=BG,stroke_width=2) for i in range(1,int(n)+1)])
            caption=T(txt,27,c).move_to([3.1,y,0])
            bars.add(bar,divisions,caption)
        self.add(bars)
        self.finish()

class S08Reveal3(SpokenScene):
    def construct(self):
        r=Rope(readout="Vm"); self.add(r,gaps())
        self.at("That puts rest")
        self.play(Transform(r.readout,T("Vm = −71.2 mV",36,VC).move_to([-3.7,2.05,0])),run_time=.5)
        self.at("And the two gaps")
        self.play(FadeIn(label("Driving-force sizes")),run_time=.4)
        self.at("driving forces")
        signed=VGroup(M("Vm − EK = +23.8 mV",27,KC),M("Vm − ENa = −131.8 mV",27,NAC)).arrange(RIGHT,buff=.7).move_to([0,-3.25,0])
        self.play(FadeIn(signed),run_time=.5)
        self.finish()

class S09Algebra(SpokenScene):
    def construct(self):
        a=algebra(); self.add(label("The balance, in symbols",color=NETC))
        self.at("The algebra")
        self.play(FadeIn(a[0]),run_time=.6)
        self.at("Set the currents")
        self.play(Indicate(a[0],color=NETC,scale_factor=1.02),run_time=.6)
        self.at("solve for the voltage")
        self.play(FadeIn(a[1],shift=DOWN*.2),run_time=.55)
        self.finish()

class S10Average(SpokenScene):
    def construct(self):
        a=algebra(); self.add(a)
        self.at("The resting potential")
        a_target=algebra().scale(.82).arrange(DOWN,buff=.35).move_to([0,2.3,0]).set_opacity(.55)
        self.play(Transform(a,a_target),FadeIn(average()),run_time=.7)
        self.at("as an average")
        self.play(FadeIn(label("average of the E’s",-1.95,30,NETC)),run_time=.35)
        self.play(FadeIn(T("(8.47 × −95 + 1.53 × 60.6) / 10",28).move_to([0,-2.6,0])),
                  FadeIn(label("= −71.2 mV",-3.35,34,VC)),run_time=.5)
        self.finish()

class S11Weights(SpokenScene):
    def construct(self):
        a=average(); self.add(a,label("average of the E’s",-2.15,32,NETC))
        self.at("Each one")
        self.play(Indicate(a[0][1],color=KC,scale_factor=1.03),run_time=.5)
        self.at("weighted by its conductance")
        self.play(FadeIn(label("Conductance gives each ion its weight",size=32)),run_time=.5)
        self.at("More ions")
        self.play(Transform(a,average(True)),run_time=.6)
        self.at("above and below")
        self.wait(2)
        self.play(Transform(a,average()),run_time=.5)
        self.finish()

class S12Shortcut(SpokenScene):
    def construct(self):
        rule=VGroup(T("Rule of thumb",32,MUTED),T("Nearest the biggest conductance",36),
                    T("Works for two; can fail for three or more",28,MUTED)).arrange(DOWN,buff=.4).move_to([0,1.5,0])
        box=SurroundingRectangle(rule,buff=.4,color=MUTED,corner_radius=.2)
        self.add(rule,box)
        self.at("Do not shorten")
        good=bchip("Use the weighted average",NETC,size=38).move_to([0,-1.7,0])
        self.play(FadeIn(good),run_time=.6)
        self.at("that shortcut can fail")
        self.play(Create(Cross(rule[1],stroke_color=RED,stroke_width=5)),run_time=.6)
        self.finish()

class S13Open(SpokenScene):
    def construct(self):
        r=Rope(readout="Vm"); self.add(r,label("1 / 3   Change one ion’s channels"))
        ghost=DashedLine([X(REST),-.3,0],[X(REST),1.5,0],color=MUTED)
        self.add(ghost,T("baseline",28,MUTED).move_to([X(REST)+1.1,-1.95,0]),
                 Line([X(REST),-.4,0],[X(REST)+1.1,-1.65,0],color=MUTED,stroke_width=2))
        self.at("Three consequences")
        self.at("Open more")
        self.play(FadeIn(T("Open more Na+ channels",32,NAC).move_to([2.6,1.8,0])),run_time=.4)
        r.change(self,REST,gna=GNA*3,seconds=.6)
        self.at("balance point slides")
        r.change(self,balance(gna=GNA*3),gna=GNA*3,seconds=1.2)
        self.finish()

class S14Close(SpokenScene):
    def construct(self):
        r=Rope(readout="Vm"); self.add(r,label("2 / 3   Close some Na+ channels"))
        ghost=DashedLine([X(REST),-.3,0],[X(REST),1.5,0],color=MUTED)
        self.add(ghost,T("baseline",28,MUTED).move_to([X(REST)+1.1,-1.95,0]),
                 Line([X(REST),-.4,0],[X(REST)+1.1,-1.65,0],color=MUTED,stroke_width=2))
        self.at("Close some")
        r.change(self,REST,gna=GNA*.5,seconds=.65)
        self.at("it slides away")
        self.add(label("Toward EK",-3.15,32,KC))
        r.change(self,balance(gna=GNA*.5),gna=GNA*.5,seconds=1.5)
        self.wait(max(.1,5.3-self.elapsed()))
        self.finish()

class S15ScaleAll(SpokenScene):
    def construct(self):
        r=Rope(readout="Vm = −71.2 mV",stroke_scale=7,readout_y=2.55)
        self.add(r,label("3 / 3   Scale every leak together",3.45,32))
        trace=DashedLine([X(REST),-.3,0],[X(REST),1.2,0],color=VC,stroke_width=4)
        self.add(trace)
        self.at("Scale every leak")
        r.change(self,REST,gk=2*GK,gna=2*GNA,seconds=1,readout="Vm = −71.2 mV")
        tags=VGroup(T("×2",32,KC).move_to([-4.5,1.8,0]),T("×2",32,NAC).move_to([.8,1.1,0]))
        self.play(FadeIn(tags),run_time=.3)
        self.at("balance point stays")
        self.play(FadeIn(label("Same passive balance point",-1.85,32,NETC)),run_time=.45)
        self.play(FadeIn(label("No injected current; pump’s direct current omitted",-3.35,26,MUTED)),run_time=.4)
        self.at("something else changes")
        self.play(FadeIn(bchip("Something else changes…",TEXT,size=28).move_to([0,-2.6,0])),run_time=.4)
        self.finish()

class S16DoubleNa(SpokenScene):
    def construct(self):
        r=Rope(readout="Vm = −71.2 mV"); self.add(r)
        self.at("Double the sodium")
        self.play(FadeIn(label("gNa  1.53 → 3.06 nS",color=NAC)),run_time=.4)
        r.change(self,REST,gna=2*GNA,seconds=.6,readout="Vm = −71.2 mV")
        self.at("rest moves toward")
        r.change(self,balance(gna=2*GNA),gna=2*GNA,seconds=1,readout="Vm")
        self.at("But only part")
        self.play(Transform(r.readout,T("Vm ≈ −53.7 mV",36,VC).move_to([-2,2.05,0])),run_time=.4)
        self.at("because potassium's rope")
        self.play(FadeIn(T("(8.47 × −95 + 3.06 × 60.6) / 11.53",28).move_to([0,-2.45,0])),run_time=.5)
        self.finish()

class S17Total(SpokenScene):
    def construct(self):
        self.add(Rope(readout="Vm = −71.2 mV"),
                 T("Keep this cell’s total leak",30).move_to([-2.8,3.2,0]))
        self.at("Keep one number")
        self.wait(.3)
        self.at("its total leak")
        tag=bchip("gK + gNa = 10 nS",TEXT,size=27).to_corner(UR,buff=.55)
        self.play(FadeIn(tag),run_time=.6)
        self.at("the next chapter")
        self.play(FadeIn(label("For the next chapter",-2.6,32)),run_time=.4)
        self.finish()

class S18GhkQ(SpokenScene):
    def construct(self):
        self.add(label("Concentrations + permeabilities",3.2,34))
        self.at("Often you know")
        self.play(FadeIn(ghk()),run_time=.8)
        self.at("Then you calculate")
        self.play(FadeIn(label("Goldman–Hodgkin–Katz",-2.7,36,TEXT)),run_time=.6)
        self.finish()

class S19GhkSame(SpokenScene):
    def construct(self):
        g=ghk(); self.add(g)
        self.at("It writes the same")
        tag=label("same zero-net-current condition",-2.3,32,NETC)
        self.play(FadeIn(tag),Indicate(g,color=NETC,scale_factor=1.015),run_time=.7)
        self.at("Each ion counts")
        c=ghk(True)
        self.play(Transform(g,c),run_time=.6)
        self.play(FadeIn(label("Written in permeabilities",-3.2,30,TEXT)),run_time=.4)
        self.finish()

class S20GhkResult(SpokenScene):
    def construct(self):
        g=ghk(True); self.add(g,label("PK = 1    PNa = 0.04    PCl = 0",3.2,30))
        self.at("For our cell")
        n=ghk(numeric=True)
        self.play(Transform(g[1],n[1]),run_time=.4)
        self.play(Transform(g[3],n[3]),run_time=.4)
        pref=M("Vm = 26.72 mV ×",34,VC).move_to(g[0])
        self.play(Transform(g[0],pref),FadeIn(label("RT/F = 26.72 mV  at 37 °C",-1.9,28,MUTED)),run_time=.3)
        self.at("the same rest")
        value=26.72*np.log((4+.04*145)/(140+.04*15))
        self.play(FadeIn(label(f"Vm ≈ {value:.1f} mV".replace('-', '−'),-3,44,VC)),run_time=.5)
        self.finish()

class S21PVsG(SpokenScene):
    def construct(self):
        r=ratios(); self.add(r)
        self.at("Permeability and conductance")
        brace=VMobject(stroke_color=MUTED,stroke_width=4,fill_opacity=0)
        brace.start_new_path(np.array([-5.7,-.5,0]))
        brace.add_cubic_bezier_curve_to(np.array([-5.7,-1.05,0]),np.array([-5.45,-1.05,0]),np.array([-4.9,-1.05,0]))
        brace.add_line_to(np.array([-.7,-1.05,0]))
        brace.add_cubic_bezier_curve_to(np.array([-.25,-1.05,0]),np.array([-.3,-1.5,0]),np.array([0,-1.5,0]))
        brace.add_cubic_bezier_curve_to(np.array([.3,-1.5,0]),np.array([.25,-1.05,0]),np.array([.7,-1.05,0]))
        brace.add_line_to(np.array([4.9,-1.05,0]))
        brace.add_cubic_bezier_curve_to(np.array([5.45,-1.05,0]),np.array([5.7,-1.05,0]),np.array([5.7,-.5,0]))
        self.play(GrowFromCenter(brace),run_time=.6)
        self.at("the same channels")
        self.play(FadeIn(label("same cell · same channels",-2.1,36,TEXT)),run_time=.5)
        self.finish()

class S22PVsG2(SpokenScene):
    def construct(self):
        self.add(ratios())
        self.at("Permeability describes")
        self.play(FadeIn(T("Property of the pathway",28,TEXT).move_to([-3.1,-.65,0])),run_time=.5)
        self.at("Conductance here")
        b=VGroup(T("Chord conductance",28),M("g = I / (Vm − Eion)",28)).arrange(DOWN,buff=.4).move_to([3.1,-.65,0])
        self.play(FadeIn(b),run_time=.6)
        self.at("the gap between")
        bar=VGroup(Line([-4,-2.5,0],[3.5,-2.5,0],color=VC,stroke_width=8),
                   Line([-4,-2.2,0],[-4,-2.8,0],color=TEXT,stroke_width=5),
                   Line([3.5,-2.2,0],[3.5,-2.8,0],color=VC,stroke_width=5),
                   T("Eion",28,TEXT).move_to([-4.8,-2.5,0]),
                   T("Vm",28,VC).move_to([4.15,-2.5,0]),
                   T("Driving force: Vm − Eion",28,VC).move_to([0,-1.8,0]))
        self.play(Create(bar[0]),FadeIn(VGroup(*bar[1:])),run_time=.7)
        self.at("It also depends")
        self.play(FadeIn(label("Depends on ions on each side and voltage",-3.15,29,MUTED)),run_time=.6)
        self.finish()

class S23Which(SpokenScene):
    def construct(self):
        def card(lines,x,color=TEXT):
            g=VGroup(*[T(s,32 if i==0 else 28,color if i==0 else TEXT) for i,s in enumerate(lines)]).arrange(DOWN,buff=.38).move_to([x,0,0])
            box=RoundedRectangle(width=5.5,height=5.2,corner_radius=.2,color=color,fill_color=color,fill_opacity=.06).move_to([x,0,0])
            return VGroup(box,g)
        a=card(["Reason with the","balance point","Which way, and why?"],-3,NETC)
        b=card(["Calculate with GHK","Given concentrations","and permeabilities"],3)
        self.add(a[0],b[0])
        self.at("reason with the balance")
        self.play(FadeIn(a[1]),run_time=.6)
        self.at("Calculate with the")
        self.play(FadeIn(b[1][0]),run_time=.6)
        self.at("when you have")
        self.play(FadeIn(VGroup(*b[1][1:])),run_time=.5)
        self.finish()

class S24Pump(SpokenScene):
    def construct(self):
        m=membrane(); self.add(m)
        self.at("One more piece")
        self.wait(.4)
        self.at("Left alone")
        self.play(FadeIn(label("Leaks run the gradients down",3.25,34)),run_time=.4)
        k=VGroup(*[Dot([-3.6+.25*(i%3-1),-1.4-.25*(i//3),0],radius=.10,color=KC) for i in range(8)])
        n=VGroup(*[Dot([-1+.25*(i%3-1),1.4+.25*(i//3),0],radius=.10,color=NAC) for i in range(8)])
        self.add(k,n)
        self.play(LaggedStart(*[d.animate.shift(UP*3.0) for d in k],lag_ratio=.12),
                  LaggedStart(*[d.animate.shift(DOWN*3.0) for d in n],lag_ratio=.12),
                  m[0].animate.set_opacity(.09),m[1].animate.set_opacity(.09),run_time=2.1)
        self.at("gradients down")
        self.finish()

class S25Pump2(SpokenScene):
    def construct(self):
        m=membrane(flat=True); self.add(m)
        pump=pump_shape()
        self.at("The sodium potassium pump")
        self.play(FadeIn(pump),FadeIn(label("Na+/K+ pump",3.25,36,PURPLE)),run_time=.6)
        self.at("puts the ions back")
        atp=bchip("ATP",PURPLE,size=28).move_to([5,-1.35,0])
        self.play(FadeIn(atp),pump[1].animate.rotate(-PI/3,about_point=pump[1].get_left()),run_time=.5)
        self.at("Three sodium go out")
        count=label("3 Na+ out · 2 K+ in · per ATP",-3.15,30,PURPLE)
        self.add(count)
        n=VGroup(*[Dot([2.35+i*.35,-1.6,0],radius=.15,color=NAC) for i in range(3)])
        self.add(n)
        self.play(*[d.animate.move_to([2.35+i*.35,0,0]) for i,d in enumerate(n)],run_time=.25)
        self.play(pump[1].animate.rotate(PI/3,about_point=pump[1].get_left()),
                  pump[2].animate.rotate(PI/3,about_point=pump[2].get_left()),run_time=.15)
        self.play(Succession(*[d.animate.move_to([2.35+i*.35,1.6,0]) for i,d in enumerate(n)]),run_time=.5)
        self.at("two potassium come in")
        k=VGroup(*[Dot([3.45+i*.4,1.6,0],radius=.15,color=KC) for i in range(2)])
        self.add(k)
        self.play(*[d.animate.move_to([2.5+i*.4,0,0]) for i,d in enumerate(k)],run_time=.25)
        self.play(pump[2].animate.rotate(-PI/3,about_point=pump[2].get_left()),
                  pump[1].animate.rotate(-PI/3,about_point=pump[1].get_left()),run_time=.15)
        self.play(Succession(*[d.animate.move_to([2.5+i*.4,-1.6,0]) for i,d in enumerate(k)]),run_time=.5)
        self.at("for each")
        self.play(atp.animate.move_to([3.65,-.7,0]).scale(.5),
                  m[0].animate.set_opacity(.38),m[1].animate.set_opacity(.38),run_time=.45)
        self.play(FadeOut(atp),pump[1].animate.rotate(PI/3,about_point=pump[1].get_left()),run_time=.35)
        self.finish()

class S26Steady(SpokenScene):
    def construct(self):
        m=membrane()
        m.remove(m[3],m[4])
        cell=VGroup(m,pump_shape()).scale(.52).move_to([-3.25,.1,0])
        names=VGroup(T("OUTSIDE",26).move_to([-4.9,1.6,0]),T("INSIDE",26).move_to([-5.1,-1.35,0]))
        leaks=VGroup(bchip("K+ leak",KC,size=26).move_to([-5.1,.1,0]),
                     bchip("Na+ leak",NAC,size=26).move_to([-3.35,.1,0]))
        self.add(cell,names,leaks)
        self.at("rest is a steady")
        self.play(FadeIn(label("Rest is a steady state",3.1,40,NETC)),run_time=.5)
        self.at("kept up by the pump")
        net=VGroup(T("Leaks balanced by pump",30,NETC),M("net current = 0",30,NETC)).arrange(DOWN,buff=.25).move_to([3,1.6,0])
        ions=VGroup(Dot([-5.1,-.65,0],radius=.1,color=KC),Dot([-3.35,.85,0],radius=.1,color=NAC))
        self.add(ions)
        self.play(FadeIn(net),ions[0].animate.shift(UP*1.5),ions[1].animate.shift(DOWN*1.5),run_time=.6)
        self.at("It is not")
        caveat=VGroup(T("Not an equilibrium",32),T("Gradients held away",28,MUTED),T("from equilibrium",28,MUTED)).arrange(DOWN,buff=.2).move_to([3,-.2,0])
        self.play(FadeIn(caveat),run_time=.6)
        self.at("The pump's own current")
        arrow=Arrow([-1.8,-.35,0],[-1.8,1,0],color=PURPLE,stroke_width=5,buff=0)
        self.play(GrowArrow(arrow),FadeIn(T("outward current",27,PURPLE).move_to([-3.5,-2.25,0])),run_time=.5)
        self.at("shift rest a little")
        baseline=Line([1.8,-1.65,0],[4.3,-1.65,0],color=MUTED)
        voltage=Dot([3.4,-1.65,0],radius=.13,color=VC)
        self.add(baseline,voltage)
        nudge=VGroup(Arrow([3.4,-1.65,0],[2.8,-1.65,0],color=VC,buff=0),T("somewhat more negative",27,VC).move_to([3,-2.25,0]))
        self.play(GrowArrow(nudge[0]),voltage.animate.shift(LEFT*.6),FadeIn(nudge[1]),run_time=.6)
        self.at("In many cells")
        self.play(FadeIn(label("Small in many cells; the size varies",-3.25,28,MUTED)),run_time=.5)
        self.finish()

class S27Takeaway(SpokenScene):
    def construct(self):
        self.add(Rope(readout="Vm = −71.2 mV"))
        self.at("With no current injected")
        self.play(FadeIn(label("No injected current",3.25,28,MUTED)),run_time=.4)
        self.at("pump's own current")
        self.play(FadeIn(label("Pump’s direct current set aside",-1.9,28,MUTED)),run_time=.4)
        self.at("rest is where")
        self.play(FadeIn(label("Rest is where the leaks balance",-2.65,34,NETC)),run_time=.5)
        self.at("average of the")
        self.play(FadeIn(label("Conductance-weighted average of reversal potentials",-3.4,26)),run_time=.5)
        self.finish()

class S28End(EndCard):
    LINE="Rest is where the leaks balance."
