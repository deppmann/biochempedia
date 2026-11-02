"""Chapter 3: A Mechanism Is Not a Cause.
COLOR MAP: ORANGE #F29E4C source; YELLOW #F5D547 serotonin;
BLUE #58C4DD readers; TEAL #3FB8C0 SERT; PURPLE #B58CD9 drug;
GREEN #83C167 remission / established; PINK #E58FB0 glia;
GOLD #D4A843 question / takeaway / relapse highlight;
GREY #8B93A1 structure / relapse. No molecular structures or invented traces.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
GREY = '#8B93A1'


def label(text, pos, size=32, color=TEXT):
    return T(text, size, color, line_spacing=1.15, disable_ligatures=True).move_to(pos)


def centered_label(text, pos, size=32, color=TEXT):
    return Paragraph(*text.split('\n'), alignment='center', font=FONT,
        font_size=size, color=color, line_spacing=1.15,
        disable_ligatures=True).move_to(pos)


def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.12,color=color,stroke_width=4)


def panel(w=5.8,h=3.7,color=GREY):
    return RoundedRectangle(width=w,height=h,corner_radius=.22,
        stroke_color=color,stroke_width=2.5,fill_color=color,fill_opacity=.07)


def pill():
    return VGroup(RoundedRectangle(width=1.5,height=.65,corner_radius=.32,
        color=PURPLE,fill_color=PURPLE,fill_opacity=.4),
        Line([0,-.3,0],[0,.3,0],color=PURPLE))


def person(color=GREEN):
    return VGroup(Circle(radius=.13,color=color,fill_color=color,fill_opacity=1).shift(UP*.28),
        RoundedRectangle(width=.35,height=.52,corner_radius=.13,color=color,
        fill_color=color,fill_opacity=.75).shift(DOWN*.16))


def cohort(relapsed=False):
    p=VGroup(*[person(GREY if relapsed and i<14 else GREEN) for i in range(21)])
    return p.arrange_in_grid(rows=3,cols=7,buff=(.64,.54)).scale(1.4).move_to([0,.35,0])


def cohort_heading():
    return label('21 patients',[0,3.15,0],38)


def legend(y=-3.15):
    return VGroup(Dot([-1.6,y,0],radius=.1,color=GREY),label('grey = relapsed',[.05,y,0],28))


def glass():
    cup=VMobject(color=GREY,stroke_width=4).set_points_as_corners([
        [-.55,.7,0],[-.38,-.65,0],[.38,-.65,0],[.55,.7,0]])
    liquid=Polygon([-.44,.02,0],[.44,.02,0],[.3,-.52,0],[-.3,-.52,0],
        stroke_width=0,fill_color=TEXT,fill_opacity=.2)
    return VGroup(liquid,cup,Line([-.55,.7,0],[.55,.7,0],color=GREY))


def session(n,x,named=True):
    title=label('Session '+str(n),[x,2.2,0],34,GOLD)
    p=person().scale(1.65).move_to([x-1.35,.45,0])
    g=glass().move_to([x+1.15,.45,0])
    arrow=arr([x-.75,.45,0],[x+.45,.45,0])
    name=label(('tryptophan-free' if n==1 else 'control') if named else 'identity concealed',
        [x,-1.1,0],32,YELLOW if n==1 and named else TEXT)
    note=label('should lower\nserotonin synthesis',[x,-2.3,0],28,YELLOW) if n==1 and named else VGroup()
    return VGroup(title,p,g,arrow,name,note)


def crossover(named=True):
    return VGroup(session(1,-3.25,named),session(2,3.25,named),
        label('Same patient · separate occasions',[0,3.2,0],32))


def question():
    return VGroup(label('Does this show that',[0,2.05,0],38),
        label('low serotonin causes depression?',[0,1,0],38,GOLD),
        Circle(radius=1,color=GOLD,stroke_width=6).move_to([0,-1.45,0]),
        label('5',[0,-1.45,0],44,GOLD))


def sert():
    # Opaque transporter occludes the membrane; the membrane never strikes through the pocket.
    mem=Rectangle(width=5,height=.35,color=GREY,fill_color=GREY,fill_opacity=.3)
    block=RoundedRectangle(width=2.4,height=3.4,corner_radius=.32,
        color=TEAL,fill_color=BG,fill_opacity=1)
    pocket=RoundedRectangle(width=1.25,height=.95,corner_radius=.2,
        color=TEAL,fill_color=TEAL,fill_opacity=.16).shift(UP*.45)
    return VGroup(mem,block,pocket)


def head():
    # A side-view silhouette: forehead, projecting nose, lips, chin and neck.
    outline=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.08)
    outline.set_points_as_corners([[-.65,-1.65,0],[-.65,-1.05,0],[-1.05,-.55,0],
        [-1.25,.25,0],[-1.15,1.1,0],[-.65,1.65,0],[.25,1.8,0],
        [.85,1.5,0],[1.02,.95,0],[1,.55,0],[1.42,.08,0],[1.04,-.03,0],
        [1.14,-.3,0],[.98,-.4,0],[.98,-.65,0],[.65,-.91,0],
        [.35,-.95,0],[.35,-1.65,0]])
    return VGroup(outline)


class S00Title(TitleCard):
    LESSON='Transmitter Systems and Drugs'
    TITLE='A Mechanism Is Not a Cause'
    def construct(self):
        brand=label('BIOCHEMISTRYPEDIA',[0,1.6,0],26,TEAL)
        lesson=label(self.LESSON,[0,.85,0],28,GREY)
        title=T(self.TITLE,44,font=TITLE_FONT,disable_ligatures=True).move_to([0,-.2,0])
        rule=Line([-1.2,-1.05,0],[1.2,-1.05,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.4)
        self.play(FadeIn(title),Create(rule),run_time=.65)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        target=sert().scale(1.1).move_to([-3.3,-.15,0])
        drug=pill().move_to([-5.25,2.3,0])
        h=head().scale(1.4).move_to([3,.1,0])
        self.add(target,drug,h,label('SERT',[-3.3,-2.6,0],34,TEAL),
            label('schematic',[-3.3,-3.2,0],26,GREY))
        self.at('blocks serotonin uptake')
        self.play(Indicate(target[2],color=TEAL),run_time=.6)
        self.at('was low serotonin')
        self.play(FadeIn(label('?', [5.4,1.5,0],72,GOLD)),
            FadeIn(label('the cause?',[3,-3.1,0],36,GOLD)),run_time=.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        target=sert().scale(1.5).move_to([0,.3,0])
        serotonin=Dot([0,.85,0],radius=.33,color=YELLOW)
        st=label('serotonin',[-3,1.6,0],30,YELLOW)
        leader=Line([-1.9,1.4,0],[-.45,.95,0],color=YELLOW)
        drug=pill().scale(.85).move_to([3.4,1.8,0])
        self.add(target,serotonin,st,leader,drug,label('SERT',[0,3.25,0],36,TEAL),
            label('schematic',[-4.9,-.65,0],26,GREY))
        self.at('drugs block')
        self.play(serotonin.animate.move_to([-3.1,1.6,0]),FadeOut(st),FadeOut(leader),
            drug.animate.move_to([0,.85,0]),run_time=.85)
        self.at('in the pocket')
        pocketlabel=label('binding pocket',[3.9,2.25,0],30,YELLOW)
        self.play(FadeIn(pocketlabel),Create(Line([2.6,2,0],[1,.95,0],color=YELLOW)),run_time=.4)
        self.at('where serotonin binds')
        card=VGroup(panel(8.2,1.25,GREEN),label('SSRIs block SERT · Established',[0,0,0],34,GREEN)).move_to([0,-3.02,0])
        self.play(FadeIn(card),run_time=.35)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        d=crossover()
        self.add(d)
        self.at('ran a blinded experiment')
        self.play(Transform(d[2],label('Delgado and colleagues · 1990',[0,3.2,0],34)),run_time=.4)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        p=cohort()
        self.add(p)
        self.at('They studied')
        self.play(FadeIn(cohort_heading()),run_time=.3)
        self.at('had remitted on antidepressants')
        self.play(FadeIn(label('Remitted on antidepressants',[0,-2.7,0],34,GREEN)),run_time=.35)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        d=crossover()
        self.add(d[0],d[2])
        self.at('with no tryptophan')
        self.play(Indicate(d[0][4]),run_time=.4)
        self.at("serotonin's building block")
        self.play(Indicate(d[0][5]),run_time=.4)
        self.at('on another occasion')
        self.play(FadeIn(d[1]),run_time=.55)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        self.add(label('Drink identity concealed',[0,3.15,0],36,GOLD))
        observers=VGroup(person().scale(2.4).move_to([-3.5,.6,0]),person(TEXT).scale(2.4).move_to([0,.6,0]))
        drinks=VGroup(glass().move_to([4,1,0]),glass().move_to([4,-1.25,0]))
        # Concealment is visible throughout, including before the spoken cue.
        blinds=VGroup(*[Rectangle(width=.64,height=.22,color=GOLD,
            fill_color=GOLD,fill_opacity=1).move_to(observer[0]) for observer in observers])
        tags=VGroup(*[VGroup(Rectangle(width=.65,height=.45,color=GOLD,
            fill_color=BG,fill_opacity=1),label('?',ORIGIN,26,GOLD)).move_to(drink)
            for drink in drinks])
        self.add(observers,drinks,label('patient',[-3.5,-1.3,0],32),label('rater',[0,-1.3,0],32),
            blinds,tags,label('Drink A',[5.55,1,0],26),label('Drink B',[5.55,-1.25,0],26))
        self.at('knew which drink')
        self.play(Indicate(tags,color=GOLD),run_time=.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        p=cohort()
        self.add(p,cohort_heading(),label('Tryptophan-free drink',[0,-2.5,0],32,YELLOW))
        self.at('14 of the 21')
        self.play(*[p[i].animate.set_color(GREY) for i in range(14)],run_time=.6)
        self.at('relapsed')
        self.play(Transform(self.mobjects[1],label('14 of 21 relapsed',[0,3.15,0],38)),FadeIn(legend()),run_time=.3)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        p=cohort(True)
        title=label('14 of 21 relapsed',[0,3.15,0],38)
        key=legend()
        self.add(p,title,key)
        self.at('returned to remission')
        self.play(LaggedStart(*[p[i].animate.set_color(GREEN) for i in range(14)],lag_ratio=.08),
            Transform(title,label('Back in remission',[0,3.15,0],38,GREEN)),FadeOut(key),run_time=1.45)
        self.at('within one to two days')
        self.play(FadeIn(label('24–48 hours · normal food',[0,-2.5,0],34,GREEN)),run_time=.3)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        self.add(cohort(),cohort_heading(),label('Control drink',[0,-2.5,0],34))
        self.at('no significant effect')
        self.play(FadeIn(label('No significant effect',[0,-3.15,0],32,GREEN)),run_time=.3)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        q=question()
        self.add(q)
        self.at('Does this show')
        self.play(Indicate(q[:2],color=GOLD),run_time=.3)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        q=question()
        self.add(q[:2])
        for n in range(5,0,-1):
            arc=Arc(radius=1,start_angle=PI/2,angle=TAU*n/5,color=GOLD,stroke_width=6).move_arc_center_to([0,-1.45,0])
            number=label(str(n),[0,-1.45,0],44,GOLD)
            self.add(arc,number)
            tracker=ValueTracker(TAU*n/5)
            arc.add_updater(lambda m: m.become(Arc(radius=1,start_angle=PI/2,angle=max(.001,tracker.get_value()),color=GOLD,stroke_width=6).move_arc_center_to([0,-1.45,0])))
            self.play(tracker.animate.set_value(TAU*(n-1)/5),run_time=1,rate_func=linear)
            arc.clear_updaters()
            self.remove(arc,number)


class S12(SpokenScene):
    def construct(self):
        p=cohort()
        self.add(p,label('It does not.',[0,3.45,0],38,GOLD))
        self.at('These patients were chosen')
        boundary=RoundedRectangle(width=10.1,height=5.35,corner_radius=.3,color=GOLD).move_to([0,.35,0])
        self.play(Create(boundary),run_time=.5)
        self.at('because an antidepressant')
        self.play(FadeIn(label('Selected because a drug helped',[0,-2.9,0],34,GOLD)),run_time=.35)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        a=VGroup(panel(5.9,4.6,GREEN).move_to([-3.15,0,0]),
            centered_label('Possible dependence',[-3.15,1.5,0],30,GREEN),
            centered_label('Some treated patients\nmay need serotonin\nto stay well',[-3.15,-.25,0],38,GREEN))
        # Qualify the fixed narration in the picture: pretreatment levels are unknown.
        b=VGroup(panel(5.9,4.6,GOLD).move_to([3.15,0,0]),
            centered_label('Baseline remains unknown',[3.15,1.5,0],30,GOLD),
            centered_label('Does not show that\nserotonin was low\nbefore treatment',[3.15,-.25,0],38,GOLD))
        self.add(a,b,label('What the experiment can tell us',[0,3.1,0],36))
        self.at('The result suggests')
        self.play(Indicate(a[0]),run_time=.4)
        self.at('A treatment can depend')
        self.play(Indicate(b[0]),run_time=.4)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        self.add(label('Depletion studies · groups by risk',[0,3.2,0],36),
            label('Rising vulnerability →',[0,2.45,0],30,GOLD))
        xs=[-4.2,0,4.2]
        headers=['Healthy\nNo family history','Healthy\nFamily history','Drug-free, recovered\nfrom depression']
        results=['No significant\nmood drop','Slight drop','Moderate drop']
        cards=[]
        for i,x in enumerate(xs):
            icons=VGroup(*[person() for _ in range(3)]).arrange(RIGHT,buff=.3).move_to([x,-.35,0])
            header=centered_label(headers[i],[x,1.1,0],28)
            header.shift(UP*(1.85-header.get_top()[1]))
            cards.append(VGroup(panel(3.9,4.9).move_to([x,-.4,0]),header,icons))
        self.add(*cards)
        for phrase,i in [('no significant mood drop',0),('dropped slightly',1),('dropped more',2)]:
            self.at(phrase)
            result=centered_label(results[i],[xs[i],-1.65,0],30,GREEN if i==0 else GOLD)
            # Align the final text baseline, even when a result wraps to two lines.
            result.shift(UP*(-2.05-result.get_bottom()[1]))
            self.play(FadeIn(result),run_time=.3)
        self.wait(2)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        self.add(panel(11.8,6),label('2022 umbrella review',[0,2.2,0],38),
            label('Low serotonin → depression?',[0,1,0],34,YELLOW))
        self.at('no consistent support')
        self.play(FadeIn(label('No consistent support\nfor this causal explanation',[0,-.35,0],40,GOLD)),run_time=.45)
        self.at('Other researchers dispute')
        self.play(FadeIn(label('Methods disputed',[0,-2.1,0],34,GOLD)),run_time=.35)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        self.add(panel(12.2,6.6),label('2018 network meta-analysis',[0,2.65,0],36))
        drugs=VGroup(*[pill().scale(.45) for _ in range(21)]).arrange_in_grid(rows=3,cols=7,buff=(.12,1.1)).move_to([-3.15,.1,0])
        self.add(drugs)
        self.at('21 antidepressants')
        self.play(FadeIn(label('21 antidepressants',[-3.15,-2.1,0],30,PURPLE)),run_time=.4)
        self.at('better than placebo')
        placebo=Circle(radius=.52,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([3.25,.15,0])
        self.play(FadeIn(placebo),FadeIn(label('placebo',[3.25,-.75,0],32)),
            FadeIn(label('better than',[3.25,1.25,0],32,GREEN)),run_time=.4)
        self.at('for acute major depression')
        self.play(FadeIn(label('Adults · acute\nmajor depression',[3.25,-1.75,0],30)),run_time=.35)
        self.at('Certainty ranged')
        self.play(FadeIn(label('Certainty: moderate to very low',[0,-2.85,0],32,GOLD)),run_time=.35)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        self.add(label('2022: no consistent support for a cause',[0,3.3,0],28,GOLD),
            label('2018: antidepressants beat placebo',[0,2.65,0],28,GREEN))
        h=head().scale(1.35).move_to([2.25,-.25,0])
        pain=VGroup(*[Line(a,b,color=RED,stroke_width=8) for a,b in [
            ([.35,.85,0],[-.15,1.05,0]),([.65,1.75,0],[.25,2.05,0]),
            ([1.8,2.05,0],[1.75,2.4,0]),([3.65,1.6,0],[4.1,1.85,0])]])
        tablet=VGroup(Circle(radius=.55,color=TEXT,fill_color=TEXT,fill_opacity=.95),
            Line([-.3,-.3,0],[.3,.3,0],color=GREY,stroke_width=3)).move_to([-3.6,.2,0])
        name=label('aspirin',[-3.6,-.85,0],32)
        self.add(h,pain,tablet,name)
        self.at('Aspirin relieves')
        self.play(VGroup(tablet,name).animate.shift(RIGHT*2.4),FadeOut(pain),run_time=1.1)
        self.at('not caused by a lack')
        self.play(FadeIn(label('Headache ≠ lack of aspirin',[0,-3.15,0],36,GOLD)),run_time=.35)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        p=cohort(True).scale(.76).move_to([0,.65,0])
        self.add(p,label('14 of 21 relapsed',[0,3.15,0],38),legend(-1.7))
        self.at('the tryptophan experiment')
        rings=VGroup(*[RoundedRectangle(width=.59,height=.99,corner_radius=.16,color=GOLD,stroke_width=3).move_to(p[i]) for i in range(14)])
        self.play(Create(rings),*[p[i].animate.set_opacity(.35) for i in range(14,21)],run_time=.55)
        self.at('suggests that')
        self.play(FadeIn(centered_label('May help explain response in treated patients',[0,-2.4,0],28,YELLOW)),
            FadeIn(centered_label('Does not show serotonin was low before treatment',[0,-3.05,0],28,YELLOW)),run_time=.35)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        left=VGroup(panel(5.9,4.5,PURPLE).move_to([-3.15,0,0]),label('A drug’s mechanism',[-3.15,1.45,0],32,PURPLE),centered_label('Evidence\nabout the drug',[-3.15,-.3,0],44))
        right=VGroup(panel(5.9,4.5,GOLD).move_to([3.15,0,0]),label('Not proof',[3.15,1.45,0],36,GOLD),centered_label('of what causes\nthe disease',[3.15,-.3,0],44))
        self.add(left,right)
        self.at('mechanism is evidence')
        self.play(Indicate(left[0],color=PURPLE),run_time=.4)
        self.at('It is not proof')
        self.play(Indicate(right[0],color=GOLD),run_time=.4)
        self.finish()


class S20End(EndCard):
    LINE='A drug’s mechanism is not proof of what causes the disease.'
    def construct(self):
        line=T('A drug’s mechanism is not proof\nof what causes the disease.',38,font=TITLE_FONT,
            line_spacing=1.3,disable_ligatures=True)
        # Explicitly centre each line; Text's default paragraph alignment is left.
        line=Paragraph('A drug’s mechanism is not proof','of what causes the disease.',
            alignment='center',font=TITLE_FONT,font_size=38,line_spacing=1.3)
        sub=label('biochemistrypedia.com',[0,0,0],26,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.65)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(sub),run_time=.3)
        self.finish()
