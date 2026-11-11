"""Add Up the Proton Switches.

COLOR MAP
  GOLD   proton token
  ORANGE acid-type switch
  BLUE   base-type switch
  TEAL   net charge
  TEXT   pH cursor and primary labels

All quantitative pictures use Henderson-Hasselbalch occupancies.  Amino acids and
proteins are labelled blocks/blobs, never molecular structures.
"""
import numpy as np
from bp_style import *

ORANGE = "#F28E52"
PKA_C, PKA_N = 2.34, 9.60
AX_Y, AX_L, AX_R = -2.75, -5.75, 5.75


def px(p):
    return AX_L + (AX_R - AX_L) * p / 14.0


def acid_charge(p, pka=PKA_C):
    return -1.0 / (1.0 + 10.0 ** (pka - p))


def base_charge(p, pka=PKA_N):
    return 1.0 / (1.0 + 10.0 ** (p - pka))


def gly_charge(p):
    return acid_charge(p) + base_charge(p)


def motes(scene, n=16):
    rng = np.random.default_rng(sum(map(ord, scene.__class__.__name__)))
    field = VGroup()
    for _ in range(n):
        d = Dot([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0],
                radius=rng.uniform(.018, .035), color=GREY).set_opacity(rng.uniform(.10, .24))
        d.v = np.array([rng.uniform(-.045, .045), rng.uniform(.035, .09), 0])
        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.8:
                m.shift(DOWN * 7.6)
        d.add_updater(drift)
        field.add(d)
    field.set_z_index(-20)
    scene.add(field)
    return field


def stage_panel(color=GREY):
    """A dark filled field makes the active diagram read as one landscape."""
    return RoundedRectangle(corner_radius=.35, width=12.2, height=6.35, stroke_width=0,
                            fill_color=color, fill_opacity=.18).move_to([0,.15,0]).set_z_index(-5)


def ph_axis(cursor=None, compact=False):
    y = AX_Y
    line = Line([AX_L, y, 0], [AX_R, y, 0], color=GREY, stroke_width=6)
    ticks = VGroup(*[Line([px(i), y-.10, 0], [px(i), y+.10, 0], color=GREY, stroke_width=2)
                     for i in range(15)])
    labels = VGroup(M("0", 28, TEXT).next_to(line.get_left(), DOWN, buff=.18),
                    M("14", 28, TEXT).next_to(line.get_right(), DOWN, buff=.18),
                    T("pH", 30, TEXT, weight=BOLD).next_to(line, LEFT, buff=.25))
    g = VGroup(line, ticks, labels)
    if cursor is not None:
        cur = always_redraw(lambda: VGroup(
            Triangle(fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(.16).rotate(PI)
                .move_to([px(cursor.get_value()), y+.28, 0]),
            M(f"{cursor.get_value():.1f}", 28, TEXT).move_to([px(cursor.get_value()), y-.52, 0])))
        return g, cur
    return g


def token(scale=1.0, label=True):
    radius = max(.30, .32*scale) if label else .32*scale
    c = Circle(radius=radius, color=GOLD, fill_color=GOLD, fill_opacity=.95, stroke_width=2)
    if not label:
        return c
    return VGroup(c, M("H+", max(28, int(28*scale)), BG, weight=BOLD).move_to(c))


def socket(pos, color=GREY, scale=1.0):
    cup = Arc(radius=.43*scale, start_angle=PI, angle=PI, color=color, stroke_width=8*scale)
    stem = Line(DOWN*.15*scale, DOWN*.72*scale, color=color, stroke_width=8*scale)
    return VGroup(cup, stem).move_to(pos)


def switch_card(title, color, charge, x):
    box = RoundedRectangle(corner_radius=.28, width=5.35, height=5.0,
                           color=color, stroke_width=4, fill_color=color, fill_opacity=.18).move_to([x,.25,0])
    lab = T(title, 32, color, weight=BOLD).move_to([x,2.15,0])
    sock = socket([x,.55,0], color, 1.45)
    tok = token(1.15).move_to([x,1.15,0])
    badge = chip(charge, color, 42, .28, .22).move_to([x,-1.45,0])
    return VGroup(box, lab, sock, tok, badge)


def gly_world(cursor_value=0.0, questions=False, name="glycine"):
    p = ValueTracker(cursor_value)
    axis, cur = ph_axis(p)
    body = RoundedRectangle(corner_radius=.35, width=10.8, height=3.55, color=GREY,
                            stroke_width=4, fill_color=GREY, fill_opacity=.18).move_to([0,.25,0])
    name_m = T(name, 38, TEXT, weight=BOLD).move_to([0,1.55,0])
    left = socket([-3.35,.35,0], ORANGE, 1.05)
    right = socket([1.25,.35,0], BLUE, 1.05)
    lb = chip("?" if questions else "0", ORANGE, 36, .25, .18).move_to([-3.35,-.80,0])
    rb = chip("?" if questions else "+1", BLUE, 36, .25, .18).move_to([1.25,-.80,0])
    read_box = RoundedRectangle(corner_radius=.2, width=2.55, height=1.25, color=TEAL,
                                stroke_width=3, fill_color=TEAL, fill_opacity=.12).move_to([4.25,.15,0])
    read_lab = T("net charge", 28, TEAL).move_to([4.25,.52,0])
    read_val = M("?" if questions else "+1", 42, TEAL, weight=BOLD).move_to([4.25,-.02,0])
    return dict(p=p, axis=axis, cursor=cur, body=body, name=name_m, left=left, right=right,
                lb=lb, rb=rb, read_box=read_box, read_lab=read_lab, read_val=read_val)


def add_world(scene, w):
    scene.add(w["axis"], w["cursor"], w["body"], w["name"], w["left"], w["right"],
              w["lb"], w["rb"], w["read_box"], w["read_lab"], w["read_val"])


class S01Hook(SpokenScene):
    def construct(self):
        motes(self)
        p = ValueTracker(1.0)
        axis, cur = ph_axis(p)
        body = RoundedRectangle(corner_radius=.35, width=10.8, height=3.55, color=GREY,
                                stroke_width=4, fill_color=GREY, fill_opacity=.18).move_to([0,.25,0])
        name = T("glycine", 38, TEXT, weight=BOLD).move_to([0,1.55,0])
        sockets = VGroup(socket([-3.35,.25,0], ORANGE,1.1), socket([1.15,.25,0],BLUE,1.1))
        read_box = RoundedRectangle(corner_radius=.22, width=2.8, height=1.55, color=TEAL,
                                    stroke_width=4, fill_color=TEAL, fill_opacity=.14).move_to([4.15,.2,0])
        read_lab = T("net charge", 30, TEAL).move_to([4.15,.65,0])
        def value():
            q = gly_charge(p.get_value())
            s = "+1" if q > .5 else ("−1" if q < -.5 else "0")
            return M(s, 52, TEAL, weight=BOLD).move_to([4.15,-.03,0])
        val = always_redraw(value)
        self.add(axis, cur, body, name, sockets, read_box, read_lab, val)
        self.at("One amino acid")
        self.play(p.animate.set_value(7.0), run_time=2.9, rate_func=linear)
        self.play(p.animate.set_value(12.0), run_time=2.0, rate_func=linear)
        self.at("What decides")
        q = T("?", 64, TEXT, weight=BOLD).next_to(read_box, UP, buff=.05)
        self.play(FadeIn(q, scale=.4), read_box.animate.scale(1.08), run_time=.55)
        self.play(p.animate.set_value(5.5), run_time=2.0, rate_func=linear)
        self.at("proton switch")
        self.play(Indicate(sockets, color=TEXT, scale_factor=1.12), run_time=.65)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Amino acids"
    TITLE = "Add Up the Proton Switches"

    def construct(self):
        p = ValueTracker(5.0)
        ghost = RoundedRectangle(corner_radius=.35, width=10.8, height=3.5, color=GREY,
                                 fill_color=GREY, fill_opacity=.025, stroke_opacity=.22).move_to([0,.15,0])
        axis, cur = ph_axis(p)
        axis.set_opacity(.18); cur.set_opacity(.25)
        brand = T("AMINO ACIDS", 28, TEAL, weight=BOLD)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        fit(title, 11.5)
        rule = Line(LEFT*1.3, RIGHT*1.3, color=GOLD, stroke_width=5)
        group = VGroup(brand,title,rule).arrange(DOWN,buff=.35).move_to(UP*.3)
        self.add(ghost,axis,cur)
        self.play(FadeIn(group,shift=UP*.15), p.animate.set_value(8.0), run_time=1.0)
        self.play(p.animate.set_value(10.0), run_time=.7, rate_func=linear)
        self.finish()


class S03Switch(SpokenScene):
    def construct(self):
        motes(self,20)
        plate = RoundedRectangle(corner_radius=.35,width=9.2,height=4.8,color=GREY,stroke_width=4,
                                 fill_color=GREY,fill_opacity=.18).move_to(UP*.3)
        pivot = Dot([0,-.15,0],radius=.22,color=TEXT)
        lever = Line([-2.7,.25,0],[2.2,.25,0],color=TEXT,stroke_width=14)
        cup = socket([2.2,.55,0],GOLD,1.55)
        h = token(1.55).move_to([2.2,1.42,0])
        label = T("proton switch",38,TEXT,weight=BOLD).move_to([0,2.15,0])
        self.at("A proton switch")
        self.play(FadeIn(plate),GrowFromCenter(lever),FadeIn(pivot),FadeIn(cup),FadeIn(h),FadeIn(label),run_time=1.1)
        self.at("holds")
        self.play(cup.animate.scale(.82).shift(UP*.08),h.animate.shift(DOWN*.18),run_time=.55)
        self.at("lets it go")
        self.play(cup.animate.scale(1.22).shift(DOWN*.08),h.animate.shift(UP*1.45+RIGHT*.45),run_time=.8)
        self.at("protonated")
        state=T("protonated",38,GOLD,weight=BOLD).move_to([0,-2.55,0])
        self.play(h.animate.move_to([2.2,1.25,0]),Write(state),run_time=.75)
        self.at("deprotonated")
        new=T("deprotonated",38,TEXT,weight=BOLD).move_to(state)
        self.play(h.animate.shift(UP*1.5+RIGHT*.5),Transform(state,new),run_time=.75)
        self.finish()


class S04Pka(SpokenScene):
    def construct(self):
        motes(self)
        p=ValueTracker(4.0); held=ValueTracker(.5)
        axis,cur=ph_axis(p)
        line=DashedLine([px(4),AX_Y+.1,0],[px(4),2.45,0],color=ORANGE,dash_length=.14)
        tag=T("pKa (example)",30,ORANGE,weight=BOLD).move_to([px(4)-1.25,2.85,0])
        bases=VGroup(); toks=VGroup()
        for i in range(20):
            x=-4.9+(i%5)*1.35; y=2.15-(i//5)*.82
            bases.add(socket([x,y,0],GREY,.45)); toks.add(token(.42,False).move_to([x,y+.27,0]))
        gauge_box=RoundedRectangle(corner_radius=.22,width=3.1,height=3.8,color=TEAL,stroke_width=3,
                                   fill_color=TEAL,fill_opacity=.07).move_to([4.35,.65,0])
        gauge_bg=Rectangle(width=.72,height=2.45,color=GREY,stroke_width=2).move_to([4.35,.65,0])
        fill=always_redraw(lambda: Rectangle(width=.66,height=2.35*held.get_value(),stroke_width=0,
                            fill_color=TEAL,fill_opacity=.9).align_to(gauge_bg,DOWN).shift(UP*.05))
        read=always_redraw(lambda:T(f"holding H+: {int(round(100*held.get_value()))}%",28,TEAL,weight=BOLD)
                           .move_to([4.35,-1.55,0]))
        panel=RoundedRectangle(corner_radius=.3,width=7.35,height=4.3,stroke_width=0,
                               fill_color=GREY,fill_opacity=.18).move_to([-2.2,.65,0]).set_z_index(-5)
        self.at("Each switch")
        self.play(FadeIn(panel),LaggedStart(*[FadeIn(b,scale=.5) for b in bases],lag_ratio=.025),FadeIn(axis),FadeIn(cur),run_time=1.0)
        self.play(FadeIn(toks[:10]),run_time=.55)
        self.at("setpoint")
        self.play(Create(line),FadeIn(tag),panel.animate.set_fill(ORANGE,opacity=.18),run_time=.7)
        self.at("half the groups")
        self.play(FadeIn(gauge_box),FadeIn(gauge_bg),FadeIn(fill),FadeIn(read),run_time=.7)
        self.at("Below it")
        self.play(p.animate.set_value(3),held.animate.set_value(1/(1+10**-1)),FadeIn(toks[10:18]),run_time=1.0)
        self.at("Above it")
        self.play(p.animate.set_value(5),held.animate.set_value(1/(1+10**1)),FadeOut(toks[2:18]),run_time=1.0)
        self.finish()


class S05Tenfold(SpokenScene):
    def construct(self):
        motes(self)
        p=ValueTracker(5.0); released=ValueTracker(10/11)
        axis,cur=ph_axis(p)
        bases=VGroup(); toks=VGroup()
        for i in range(20):
            x=-4.9+(i%5)*1.35; y=2.15-(i//5)*.82
            bases.add(socket([x,y,0],GREY,.45)); toks.add(token(.42,False).move_to([x,y+.27,0]))
        line=DashedLine([px(4),AX_Y+.1,0],[px(4),2.9,0],color=ORANGE,dash_length=.14)
        labels=VGroup(T("pKa",28,ORANGE).move_to([px(4)-.62,-2.20,0]),T("pKa + 1",28,TEXT).move_to([px(5)+.72,-2.20,0]))
        panel=RoundedRectangle(corner_radius=.22,width=3.3,height=3.9,color=TEAL,stroke_width=3,
                               fill_color=TEAL,fill_opacity=.08).move_to([4.35,.65,0])
        ratio_lab=T("let go : hold",28,TEXT).move_to([4.35,1.85,0])
        ratio=always_redraw(lambda:M(f"{max(1,int(round(released.get_value()/(1-released.get_value()))))} : 1",42,TEAL,weight=BOLD).move_to([4.35,1.25,0]))
        barbg=Rectangle(width=2.25,height=.58,color=GREY).move_to([4.35,.15,0])
        bar=always_redraw(lambda:Rectangle(width=2.15*released.get_value(),height=.48,stroke_width=0,fill_color=TEAL,
                           fill_opacity=.9).align_to(barbg,LEFT).move_to([barbg.get_left()[0]+1.075*released.get_value(),.15,0]))
        pct=always_redraw(lambda:T(f"let go: {int(round(100*released.get_value()))}%",30,TEAL,weight=BOLD).move_to([4.35,-.55,0]))
        computed=T("computed",28,GREY).move_to([4.35,-1.15,0])
        grid_panel=RoundedRectangle(corner_radius=.3,width=7.35,height=4.3,stroke_width=0,
                                    fill_color=GREY,fill_opacity=.18).move_to([-2.2,.65,0]).set_z_index(-5)
        self.add(grid_panel,axis,cur,bases,line,labels,panel,ratio_lab,ratio,barbg,bar,pct,computed,toks[:2])
        self.at("Each pH unit")
        self.play(p.animate.set_value(4),released.animate.set_value(.5),FadeIn(toks[2:10]),
                  Indicate(labels,color=TEXT,scale_factor=1.08),run_time=1.1)
        self.at("tenfold")
        self.play(p.animate.set_value(5),released.animate.set_value(10/11),FadeOut(toks[2:10]),run_time=1.35,rate_func=smooth)
        self.at("91 percent")
        self.play(Indicate(pct,color=TEAL,scale_factor=1.15),run_time=.7)
        self.finish()


class S06Twokinds(SpokenScene):
    def construct(self):
        motes(self)
        left=switch_card("acid type (carboxyl)",ORANGE,"0",-3.0)
        right=switch_card("base type (amino)",BLUE,"+1",3.0)
        plus=T("+1",28,BG,weight=BOLD).move_to(left[3]); plus2=plus.copy().move_to(right[3])
        self.at("A proton carries")
        self.play(FadeIn(left[0]),FadeIn(right[0]),FadeIn(left[2]),FadeIn(right[2]),
                  FadeIn(left[3]),FadeIn(right[3]),FadeIn(plus),FadeIn(plus2),run_time=1.0)
        self.play(left[3].animate.shift(UP*.32),right[3].animate.shift(UP*.32),run_time=.65,rate_func=there_and_back)
        self.at("holding it")
        self.play(left[0].animate.set_fill(GOLD,opacity=.18),right[0].animate.set_fill(GOLD,opacity=.18),run_time=.55)
        self.at("one charge")
        self.play(Indicate(VGroup(plus,plus2),color=GOLD,scale_factor=1.35),run_time=.65)
        self.at("acid type")
        self.play(FadeIn(left[1]),FadeIn(left[4]),run_time=.6)
        self.at("goes from zero")
        minus=chip("−1",ORANGE,42,.28,.22).move_to(left[4])
        self.play(left[3].animate.shift(UP*1.6+LEFT*.4),plus.animate.shift(UP*1.6+LEFT*.4),Transform(left[4],minus),run_time=.9)
        self.at("base type")
        self.play(FadeIn(right[1]),FadeIn(right[4]),run_time=.6)
        self.at("goes from plus")
        zero=chip("0",BLUE,42,.28,.22).move_to(right[4])
        self.play(right[3].animate.shift(UP*1.6+RIGHT*.4),plus2.animate.shift(UP*1.6+RIGHT*.4),Transform(right[4],zero),run_time=.9)
        self.at("letting go")
        self.play(right[0].animate.set_fill(BLUE,opacity=.32),run_time=.75)
        self.at("not always negative")
        note=T("let go = neutral",34,BLUE,weight=BOLD).next_to(right[4],DOWN,buff=.32)
        self.play(Indicate(right[4],color=BLUE,scale_factor=1.18),Write(note),run_time=.75)
        self.finish()


class S07Glycine(SpokenScene):
    def construct(self):
        motes(self)
        w=gly_world(0.4)
        self.at("Glycine has two")
        self.play(FadeIn(w["body"]),FadeIn(w["name"]),FadeIn(w["axis"]),FadeIn(w["cursor"]),
                  w["left"].animate.shift(RIGHT*0),w["right"].animate.shift(LEFT*0),run_time=.9)
        self.play(FadeIn(w["left"],shift=LEFT*.8),FadeIn(w["right"],shift=RIGHT*.8),FadeIn(w["lb"]),FadeIn(w["rb"]),run_time=.7)
        lc=DashedLine([px(PKA_C),AX_Y+.1,0],[px(PKA_C),1.70,0],color=ORANGE,dash_length=.12)
        rc=DashedLine([px(PKA_N),AX_Y+.1,0],[px(PKA_N),1.70,0],color=BLUE,dash_length=.12)
        ltag=T("pKa 2.3",28,ORANGE).move_to([px(PKA_C)-.78,2.28,0]); rtag=T("pKa 9.6",28,BLUE).move_to([px(PKA_N)+.78,2.28,0])
        left_glow=Rectangle(width=4.55,height=3.35,stroke_width=0,fill_color=ORANGE,fill_opacity=.22).move_to([-2.25,.25,0]).set_z_index(-.5)
        right_glow=Rectangle(width=4.55,height=3.35,stroke_width=0,fill_color=BLUE,fill_opacity=.22).move_to([2.35,.25,0]).set_z_index(-.5)
        self.at("carboxyls")
        self.play(Create(lc),FadeIn(ltag),FadeIn(left_glow),run_time=.75)
        self.at("amino groups")
        self.play(Create(rc),FadeIn(rtag),FadeIn(right_glow),run_time=.75)
        self.at("whole idea")
        self.play(FadeIn(w["read_box"]),FadeIn(w["read_lab"]),run_time=.5)
        self.at("sum of the switches")
        eq=M("0 + +1 = +1",34,TEAL,weight=BOLD).move_to(w["read_val"])
        a1=Arrow(w["lb"].get_right(),w["read_box"].get_left()+UP*.2,buff=.12,color=ORANGE,stroke_width=4)
        a2=Arrow(w["rb"].get_right(),w["read_box"].get_left()+DOWN*.2,buff=.12,color=BLUE,stroke_width=4)
        self.play(GrowArrow(a1),GrowArrow(a2),FadeIn(eq),run_time=.8)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        motes(self)
        w=gly_world(0.4,True); add_world(self,w)
        lc=DashedLine([px(PKA_C),AX_Y+.1,0],[px(PKA_C),1.75,0],color=ORANGE,dash_length=.12)
        rc=DashedLine([px(PKA_N),AX_Y+.1,0],[px(PKA_N),1.75,0],color=BLUE,dash_length=.12)
        self.add(lc,rc)
        self.at("Your turn")
        self.play(w["p"].animate.set_value(7.4),run_time=1.8,rate_func=smooth)
        self.at("blood pH")
        blood=T("blood, about 7.4",30,TEXT,weight=BOLD).move_to([px(7.4),-1.95,0])
        self.play(FadeIn(blood,shift=UP*.1),run_time=.55)
        h1=token(.75).move_to([-3.35,1.0,0]); h2=token(.75).move_to([1.25,1.0,0])
        self.at("check each switch")
        self.play(FadeIn(h1),FadeIn(h2),Indicate(VGroup(w["lb"],w["rb"]),color=TEXT),run_time=.8)
        self.at("net charge")
        question=T("Glycine at pH 7.4: net charge?",40,TEXT,font=TITLE_FONT).move_to([0,3.15,0])
        self.play(Write(question),run_time=.75)
        self.finish()


class S09Hold(Scene):
    def construct(self):
        motes(self)
        w=gly_world(7.4,True); add_world(self,w)
        lc=DashedLine([px(PKA_C),AX_Y+.1,0],[px(PKA_C),1.75,0],color=ORANGE,dash_length=.12)
        rc=DashedLine([px(PKA_N),AX_Y+.1,0],[px(PKA_N),1.75,0],color=BLUE,dash_length=.12)
        q=T("Glycine at pH 7.4: net charge?",40,TEXT,font=TITLE_FONT).move_to([0,3.15,0])
        h=VGroup(token(.75).move_to([-3.35,1.0,0]),token(.75).move_to([1.25,1.0,0]))
        self.add(lc,rc,q,h)
        self.play(Indicate(VGroup(w["lb"],w["rb"]),color=TEXT,scale_factor=1.13),h.animate.shift(UP*.13),run_time=2.1,rate_func=there_and_back)
        self.play(Indicate(VGroup(w["lb"],w["rb"]),color=TEXT,scale_factor=1.13),h.animate.shift(UP*.13),run_time=2.1,rate_func=there_and_back)
        self.wait(.3)


class S10Answer(SpokenScene):
    def construct(self):
        motes(self)
        w=gly_world(7.4,True); add_world(self,w)
        lc=DashedLine([px(PKA_C),AX_Y+.1,0],[px(PKA_C),1.75,0],color=ORANGE,dash_length=.12)
        rc=DashedLine([px(PKA_N),AX_Y+.1,0],[px(PKA_N),1.75,0],color=BLUE,dash_length=.12)
        q=T("Glycine at pH 7.4: net charge?",40,TEXT,font=TITLE_FONT).move_to([0,3.15,0])
        h1=token(.75).move_to([-3.35,1.0,0]); h2=token(.75).move_to([1.25,1.0,0])
        self.add(lc,rc,q,h1,h2)
        self.at("above the carboxyl's")
        arr=Arrow([px(PKA_C),2.05,0],[px(7.4),2.05,0],color=ORANGE,stroke_width=5)
        self.play(FadeOut(q),GrowArrow(arr),run_time=.65)
        self.at("lets go")
        minus=chip("−1",ORANGE,36,.25,.18).move_to(w["lb"])
        self.play(h1.animate.shift(UP*1.5+LEFT*.4),Transform(w["lb"],minus),
                  w["body"].animate.set_fill(ORANGE,opacity=.30),run_time=.75)
        self.at("below the amino")
        arr2=Arrow([px(7.4),2.55,0],[px(PKA_N),2.55,0],color=BLUE,stroke_width=5)
        self.play(GrowArrow(arr2),run_time=.55)
        self.at("holds on")
        plus=chip("+1",BLUE,36,.25,.18).move_to(w["rb"])
        self.play(h2.animate.shift(DOWN*.35),Transform(w["rb"],plus),
                  w["body"].animate.set_fill(BLUE,opacity=.30),run_time=.7)
        self.at("sum is zero")
        equation=VGroup(M("−1 + +1",28,TEAL,weight=BOLD),M("= 0",32,TEAL,weight=BOLD)).arrange(DOWN,buff=.02).move_to(w["read_val"])
        self.play(Transform(w["read_val"],equation),Indicate(w["read_box"],color=TEAL),
                  w["body"].animate.set_fill(TEAL,opacity=.30),run_time=.75)
        self.at("zwitterion")
        zw=T("zwitterion",36,TEAL,weight=BOLD).move_to([0,-1.72,0])
        signs=VGroup(T("−",44,ORANGE,weight=BOLD).move_to([-3.35,1.45,0]),T("+",44,BLUE,weight=BOLD).move_to([1.25,1.45,0]))
        self.play(w["body"].animate.set_stroke(TEAL,6),FadeIn(signs,scale=.5),Write(zw),run_time=.75)
        self.finish()


class S11Sweep(SpokenScene):
    def construct(self):
        motes(self)
        panel=stage_panel(TEAL)
        axes=Axes(x_range=[0,14,2],y_range=[-1.1,1.1,.5],x_length=10.8,y_length=5.3,
                  axis_config={"color":GREY,"stroke_width":3,"include_tip":False}).move_to([.25,.15,0])
        xlab=T("pH",30,TEXT,weight=BOLD).next_to(axes.x_axis,DOWN,buff=.22)
        ylab=T("average net charge",28,TEAL,weight=BOLD).rotate(PI/2).next_to(axes.y_axis,LEFT,buff=.22)
        tag=T("computed",28,GREY).move_to([5.15,3.12,0])
        p=ValueTracker(0.0)
        curve=axes.plot(lambda x:gly_charge(x),x_range=[0,14,.03],color=TEAL,stroke_width=6)
        reveal=always_redraw(lambda:axes.plot(lambda x:gly_charge(x),x_range=[0,max(.01,p.get_value()),.03],color=TEAL,stroke_width=6))
        dot=always_redraw(lambda:Dot(axes.c2p(p.get_value(),gly_charge(p.get_value())),radius=.10,color=TEXT))
        scan=always_redraw(lambda:Line(axes.c2p(p.get_value(),-1.05),axes.c2p(p.get_value(),1.05),
                                       color=TEXT,stroke_width=6).set_opacity(.32))
        self.add(panel,axes,xlab,ylab,tag,dot,scan)
        self.at("Sweep")
        self.add(reveal)
        self.play(p.animate.set_value(14),run_time=3.25,rate_func=linear)
        self.at("steps down")
        labs=VGroup(T("about +1",28,TEAL).move_to(axes.c2p(1,.82)),T("about 0",28,TEAL).move_to(axes.c2p(6,.34)),T("about −1",28,TEAL).move_to(axes.c2p(12,-.82)))
        bands=VGroup(Rectangle(width=2.2,height=1.05,stroke_width=0,fill_color=TEAL,fill_opacity=.22).move_to(axes.c2p(1,.86)),
                     Rectangle(width=4.0,height=1.0,stroke_width=0,fill_color=TEAL,fill_opacity=.22).move_to(axes.c2p(6,0)),
                     Rectangle(width=2.2,height=1.05,stroke_width=0,fill_color=TEAL,fill_opacity=.22).move_to(axes.c2p(12,-.86)))
        self.play(LaggedStart(*[FadeIn(x) for pair in zip(bands,labs) for x in pair],lag_ratio=.10),run_time=1.15)
        self.at("centered on")
        lines=VGroup(DashedLine(axes.c2p(PKA_C,-1.05),axes.c2p(PKA_C,1.05),color=ORANGE,dash_length=.12),
                     DashedLine(axes.c2p(PKA_N,-1.05),axes.c2p(PKA_N,1.05),color=BLUE,dash_length=.12))
        self.play(Create(lines),panel.animate.set_fill(ORANGE,opacity=.34),run_time=.9)
        self.at("zero crossing")
        pi=(PKA_C+PKA_N)/2
        pdot=Dot(axes.c2p(pi,0),radius=.15,color=TEAL)
        plab=T("pI",34,TEAL,weight=BOLD).move_to(axes.c2p(pi-.75,-.36))
        halo=Circle(radius=.7,color=TEAL,stroke_width=8).move_to(pdot)
        self.play(FadeIn(pdot,scale=.3),FadeIn(plab),ShowPassingFlash(halo,time_width=.8),
                  panel.animate.set_fill(TEAL,opacity=.34),run_time=.8)
        self.finish()


class S12Pi(SpokenScene):
    def construct(self):
        motes(self)
        panel=stage_panel(TEAL)
        axes=Axes(x_range=[0,14,2],y_range=[-1.1,1.1,.5],x_length=10.8,y_length=5.3,
                  axis_config={"color":GREY,"stroke_width":3,"include_tip":False}).move_to([.25,.15,0])
        curve=axes.plot(lambda x:gly_charge(x),x_range=[0,14,.03],color=TEAL,stroke_width=6)
        l1=M("2.34",30,ORANGE).move_to(axes.c2p(PKA_C+.85,.72)); l2=M("9.60",30,BLUE).move_to(axes.c2p(PKA_N-.85,-.72))
        pi=(PKA_C+PKA_N)/2; dot=Dot(axes.c2p(pi,0),radius=.15,color=TEAL)
        values=VGroup(l1,l2)
        self.add(panel,axes,curve,values,dot)
        self.play(ShowPassingFlash(curve.copy().set_stroke(TEXT,14),time_width=.35),
                  panel.animate.set_fill(TEAL,opacity=.34),run_time=1.15)
        self.at("averaging")
        ans=M("(2.34 + 9.60) / 2 = 5.97",36,TEAL,weight=BOLD).move_to([0,3.15,0])
        self.play(l1.animate.move_to([-1.1,3.15,0]),l2.animate.move_to([1.1,3.15,0]),
                  panel.animate.set_fill(GREY,opacity=.18),run_time=.75)
        self.play(Transform(values,ans),run_time=.75)
        self.at("gives")
        self.play(panel.animate.set_fill(TEAL,opacity=.32),run_time=.65)
        self.at("simplest form")
        self.play(FadeOut(axes),FadeOut(curve),FadeOut(dot),FadeOut(values),
                  panel.animate.set_fill(GREY,opacity=.18),run_time=.7)
        rungs=VGroup(*[Line([-3.7,y,0],[3.7,y,0],color=GREY,stroke_width=9) for y in (1.65,0,-1.65)])
        charges=VGroup(M("+1",40,TEXT).next_to(rungs[0],LEFT,buff=.35),M("0",40,TEAL).next_to(rungs[1],LEFT,buff=.35),M("−1",40,TEXT).next_to(rungs[2],LEFT,buff=.35))
        note=T("predominant charge (schematic)",28,GREY).move_to([0,2.75,0])
        gaps=VGroup(M("2.34",34,ORANGE).move_to([2.5,.82,0]),M("9.60",34,BLUE).move_to([2.5,-.82,0]))
        self.play(LaggedStart(*[Create(r) for r in rungs],lag_ratio=.2),FadeIn(charges),FadeIn(note),FadeIn(gaps),run_time=1.0)
        self.at("latter's net zero rung")
        br=VGroup(BraceBetweenPoints([3.25,1.45,0],[3.25,.2,0],direction=RIGHT,color=ORANGE),
                  BraceBetweenPoints([3.25,-.2,0],[3.25,-1.45,0],direction=RIGHT,color=BLUE))
        self.play(rungs[1].animate.set_color(TEAL).set_stroke(width=13),FadeIn(br),run_time=.7)
        self.finish()


class S13Sidechain(SpokenScene):
    def construct(self):
        motes(self)
        p=ValueTracker(7.4); axis,cur=ph_axis(p)
        body=RoundedRectangle(corner_radius=.35,width=9.5,height=3.45,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.18).move_to([0,.25,0])
        name=T("amino acid",36,TEXT,weight=BOLD).move_to([0,1.25,0])
        top=socket([0,.25,0],GREY,1.15); side=T("side chain",28,TEXT).move_to([0,-.95,0])
        self.at("A side chain")
        self.play(FadeIn(axis),FadeIn(cur),FadeIn(body),FadeIn(name),GrowFromCenter(top),FadeIn(side),run_time=1.0)
        tok=token(.8).move_to([0,.95,0]); badge=chip("?",GREY,36).move_to([3.6,.15,0]); self.add(tok,badge)
        self.at("Glutamate's")
        gl=T("glutamate",36,TEXT,weight=BOLD).move_to(name); gb=chip("−1",ORANGE,38).move_to(badge)
        line=DashedLine([px(4),AX_Y+.1,0],[px(4),-1.58,0],color=ORANGE,dash_length=.12)
        self.play(Transform(name,gl),top.animate.set_color(ORANGE),Create(line),tok.animate.shift(UP*1.5),Transform(badge,gb),
                  body.animate.set_fill(ORANGE,opacity=.18),run_time=.9)
        self.at("negative")
        self.play(Indicate(body,color=ORANGE,scale_factor=1.02),run_time=.65)
        self.at("Lysine's")
        ly=T("lysine",36,TEXT,weight=BOLD).move_to(name); lb=chip("+1",BLUE,38).move_to(badge)
        line2=DashedLine([px(10.5),AX_Y+.1,0],[px(10.5),-1.58,0],color=BLUE,dash_length=.12)
        self.play(Transform(name,ly),top.animate.set_color(BLUE),ReplacementTransform(line,line2),tok.animate.move_to([0,.85,0]),Transform(badge,lb),
                  body.animate.set_fill(BLUE,opacity=.18),run_time=.9)
        self.at("positive")
        self.play(Indicate(body,color=BLUE,scale_factor=1.02),run_time=.65)
        self.at("Histidine's")
        hi=T("histidine",36,TEXT,weight=BOLD).move_to(name); hb=chip("0  mostly",BLUE,34).move_to(badge)
        line3=DashedLine([px(6),AX_Y+.1,0],[px(6),-1.58,0],color=BLUE,dash_length=.12)
        self.play(Transform(name,hi),ReplacementTransform(line2,line3),tok.animate.shift(UP*1.4),Transform(badge,hb),run_time=.9)
        self.at("mostly neutral")
        self.play(Indicate(badge,color=BLUE,scale_factor=1.12),run_time=.65)
        self.at("Inside a protein")
        protein=RoundedRectangle(corner_radius=1.0,width=11.2,height=4.5,color=TEAL,stroke_width=3,fill_color=TEAL,fill_opacity=.04).move_to([0,.25,0])
        pl=T("protein (schematic)",28,TEAL).move_to([0,2.95,0]); shift=T("can shift",28,BLUE).move_to([4.45,1.85,0])
        self.play(Create(protein),FadeIn(pl),line3.animate.shift(RIGHT*.85),FadeIn(shift),run_time=1.2)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        motes(self)
        p=ValueTracker(7.4); axis,cur=ph_axis(p)
        body=RoundedRectangle(corner_radius=.35,width=10.8,height=3.55,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.18).move_to([0,.25,0])
        sw=VGroup(socket([-3,.3,0],ORANGE,1),socket([0,.3,0],BLUE,1),socket([3,.3,0],BLUE,1))
        badges=VGroup(chip("−1",ORANGE,32),chip("+1",BLUE,32),chip("0",BLUE,32)).arrange(RIGHT,buff=1.55).move_to([0,-.8,0])
        read=chip("sum = 0",TEAL,36).move_to([4.2,1.55,0])
        self.add(axis,cur,body,sw,badges,read)
        self.at("list")
        self.play(LaggedStart(*[Indicate(x,color=TEXT,scale_factor=1.12) for x in sw],lag_ratio=.18),run_time=.75)
        self.at("compare")
        marks=VGroup(DashedLine([px(2.34),AX_Y,0],[px(2.34),1.9,0],color=ORANGE,dash_length=.12),DashedLine([px(9.6),AX_Y,0],[px(9.6),1.9,0],color=BLUE,dash_length=.12))
        self.play(Create(marks),Indicate(cur,color=TEXT),run_time=.7)
        self.at("add")
        total=chip("−1 + +1 + 0 = 0",TEAL,28).move_to(read)
        self.play(FadeOut(badges,shift=UP*.22),Transform(read,total),run_time=.8)
        self.at("sickle cell")
        self.play(FadeOut(VGroup(axis,cur,body,sw,badges,read,marks)),run_time=.55)
        strip=Arrow([-5.5,-2.2,0],[5.5,-2.2,0],buff=0,color=GREY,stroke_width=5)
        signs=VGroup(T("−",42,TEXT).move_to([-5.6,-2.7,0]),T("+",42,TEXT).move_to([5.6,-2.7,0]),T("schematic",28,GREY).move_to([0,-2.75,0]))
        normal=Ellipse(width=4.5,height=2.7,color=TEAL,fill_color=TEAL,fill_opacity=.18,stroke_width=4).move_to([-3,0,0])
        sickle=Ellipse(width=4.5,height=2.7,color=ORANGE,fill_color=ORANGE,fill_opacity=.18,stroke_width=4).move_to([3,0,0])
        nl=T("normal hemoglobin",30,TEAL,weight=BOLD).move_to(normal); sl=T("sickle hemoglobin",30,ORANGE,weight=BOLD).move_to([3,.82,0])
        self.play(GrowArrow(strip),FadeIn(signs),FadeIn(normal),FadeIn(sickle),FadeIn(nl),FadeIn(sl),run_time=1.0)
        self.at("A valine")
        acids=VGroup(chip("Glu switch",ORANGE,28).move_to([2.25,.12,0]),chip("Glu switch",ORANGE,28).move_to([3.75,-.62,0]))
        vals=VGroup(chip("Val (no switch)",GREY,28).move_to(acids[0]),chip("Val (no switch)",GREY,28).move_to(acids[1]))
        self.play(FadeIn(acids),run_time=.4)
        self.play(ReplacementTransform(acids,vals),sickle.animate.shift(RIGHT*.8),sl.animate.shift(RIGHT*.8),run_time=.85)
        self.at("beta chain")
        self.play(normal.animate.shift(RIGHT*.55),nl.animate.shift(RIGHT*.55),sickle.animate.shift(RIGHT*.45),sl.animate.shift(RIGHT*.45),vals.animate.shift(RIGHT*.45),run_time=.7)
        self.finish()


class S16End(EndCard):
    LINE = "Net charge is the sum of switches: pH against each pKa."

    def construct(self):
        left=Ellipse(width=4.4,height=2.5,color=TEAL,fill_opacity=.04,stroke_opacity=.18).move_to([-3,0,0])
        right=Ellipse(width=4.4,height=2.5,color=ORANGE,fill_opacity=.04,stroke_opacity=.18).move_to([3,0,0])
        line=T(self.LINE,40,TEXT,font=TITLE_FONT); fit(line,11.8)
        sub=T("biochemistrypedia.com",28,TEAL)
        g=VGroup(line,sub).arrange(DOWN,buff=.55)
        h=token(.75).move_to([-5.8,2.5,0])
        self.add(left,right,h)
        self.play(FadeIn(g,shift=UP*.15),h.animate.shift(RIGHT*3.5),run_time=1.4)
        self.play(h.animate.shift(RIGHT*3.5),run_time=1.4,rate_func=linear)
        self.finish()
