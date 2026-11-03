"""Chapter 2: A Limiting Supply.

COLOR MAP (from scenes.old.py, shared across the series)
BLUE = neuron, status undecided; GREEN = survival; RED = death / blocked;
YELLOW = neurotrophic factor / support; TEAL = neurons made / ceiling;
PURPLE = TrkA; GREY = target tissue, axes and structure.
CHAPTERS.md is kept unchanged under TASK.md's edit-only restriction.
All neuron counts and bar heights here are explicitly schematic, not data.
"""
from bp_style import *
import numpy as np

PURPLE = "#B58CD9"
LESSON = "The Neurotrophic Hypothesis Tested"
NY = [2.0 - 0.8 * i for i in range(6)]
WIN = [0, 2, 4]


def dot(p, color=BLUE, r=0.22, op=0.95):
    return Circle(radius=r, stroke_color=color, stroke_width=2,
                  fill_color=color, fill_opacity=op).move_to(p)


def to_state(d, color, op=0.95):
    return d.animate.set_stroke(color, opacity=op).set_fill(color, opacity=op * 0.95)


def heading(text, color=TEXT):
    return T(text, 34, color, font=TITLE_FONT).move_to([0, 3.1, 0])


def build_race(fed=False, survivors=False):
    # Reuses the six-neuron geometry and color-state model from scenes.old.py.
    indices = WIN if survivors else range(6)
    neurons = VGroup(*[VGroup(dot([-5.3, NY[i], 0], GREEN if fed and i in WIN else BLUE),
        Line([-5.08, NY[i], 0], [1.8, NY[i], 0], color=GREEN if fed and i in WIN else BLUE,
             stroke_width=4)) for i in indices])
    target = RoundedRectangle(corner_radius=0.25, width=3.4, height=5.2,
        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([3.5, 0, 0])
    label = T("target tissue", 28, GREY).move_to([3.5, 2.95, 0])
    note = T("Illustration · not neuron counts", 26, GREY).move_to([0, -3.45, 0])
    return neurons, target, label, note


ROWS = ["Remove target → more die", "Add target → fewer die",
        "Add factor → fewer die", "Remove factor → more die",
        "Most death when axons reach target"]


def checklist(n=0, ticks=(), dim5=False):
    rows = VGroup()
    for i in range(5):
        y = 2.0 - i * 1.12
        box = Square(side_length=0.38, color=GREY, stroke_width=2).move_to([-5.55, y, 0])
        line = T(ROWS[i], 28, GREY if dim5 and i == 4 else TEXT).move_to([-4.95, y, 0], aligned_edge=LEFT) if i < n else T(f"Prediction {i+1}", 28, GREY).move_to([-4.95, y, 0], aligned_edge=LEFT)
        row = VGroup(box, line)
        if i in ticks and i < n:
            tick = VMobject(color=GREEN, stroke_width=4).set_points_as_corners([
                [-5.69, y, 0], [-5.59, y - .12, 0], [-5.36, y + .16, 0]])
            row.add(tick)
        if i == 0 and i < n and i not in ticks:
            row.add(T("fits", 28, GREEN).next_to(line, RIGHT, buff=.3))
        rows.add(row)
    return rows


def reveal_row(scene, rows, index, n, duration=.5):
    old = rows[index][1]
    new = checklist(n, ticks=())[index][1]
    scene.play(FadeOut(old), FadeIn(new), run_time=duration)
    rows[index].remove(old)
    rows[index].add(new)


def question():
    return VGroup(heading("Predict"), T("Extra leg → more target", 42).move_to([0, 1.65, 0]),
        T("Lumbar motor neurons?", 46, BLUE).move_to([0, .15, 0]),
        VGroup(chip("Before normal loss?", TEXT, 32), chip("After normal loss?", TEXT, 32))
            .arrange(RIGHT, buff=.6).move_to([0, -1.45, 0]))


def bars(later=False):
    # Ordinal schematic only: illustrative birth ceiling minus normal/reduced loss.
    # No measured counts or quantitative inference is encoded in these heights.
    ceiling = 4.7
    loss = (2.5, 1.25) if later else (0, 0)
    head = heading("Later (after the normal loss)" if later else "Day 6 · before normal loss")
    baseline = -2.5
    base = VGroup(Line([-4.1, baseline, 0], [5.5, baseline, 0], color=GREY),
                  Line([-4.1, baseline, 0], [-4.1, 2.35, 0], color=GREY),
                  T("0", 26, GREY).move_to([-4.4, baseline, 0]),
                  T("Lumbar motor neurons (schematic)", 26).rotate(PI/2).move_to([-5.45, -.1, 0]))
    bs = VGroup(*[Rectangle(width=2.2, height=ceiling-d, color=BLUE, fill_color=BLUE,
        fill_opacity=.7).move_to([x, baseline+(ceiling-d)/2, 0]) for x,d in zip([-1.8, 2.8],loss)])
    labels = VGroup(T("Control", 28, BLUE).move_to([-1.8, -2.95, 0]),
                   T("Extra-leg graft", 28, BLUE).move_to([2.8, -2.95, 0]))
    note = T("Schematic bars · not data", 26, GREY).move_to([0, -3.48, 0])
    ref = VGroup(DashedLine([-3.9, 2.2, 0], [5.4, 2.2, 0], color=GREY),
                 T("Day-6 level", 26, GREY).move_to([4.2, 2.55, 0])) if later else VGroup()
    return VGroup(head, base, bs, labels, note, ref)


def compact_check(done=False):
    labels = ["1  Remove target", "2  Add target", "3  Add factor", "4  Remove factor", "5  Timing"]
    rows=VGroup()
    for i,label in enumerate(labels):
        box=Square(.32, color=GREY).move_to([-6.0, 1.7-i*.85, 0])
        txt=T(label, 30, TEXT if i<4 else GREY).next_to(box, RIGHT, buff=.2)
        row=VGroup(box,txt)
        if i==0 or (done and i==1):
            row.add(fits_mark(txt))
        rows.add(row)
    return rows


def fits_mark(txt):
    return T("fits",28,GREEN).next_to(txt,RIGHT,buff=.25)


def vigorous():
    return T("Embryos whose grafts moved vigorously", 28).move_to([0, 1.5, 0])


def caution():
    return VGroup(heading("One caution", RED), chip("Motor neurons", BLUE, 40).move_to([0, 1, 0]),
        T("Do not depend on NGF", 34, TEXT).move_to([0, -.5, 0]))


class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "A Limiting Supply"

    def construct(self):
        # The shared title layout, with its small brand raised to the 22 pt minimum.
        g = VGroup(T("BIOCHEMISTRYPEDIA", 22, TEAL), T(self.LESSON.upper(), 22, GREY),
                   T(self.TITLE, 54, font=TITLE_FONT), Line(LEFT*1.2, RIGHT*1.2, color=GOLD))
        g.arrange(DOWN, buff=.35)
        self.play(FadeIn(g), run_time=.65)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        n,t,l,note=build_race()
        l.move_to([3.5,2.3,0])
        title=heading("A Limiting Supply")
        self.add(title,t,note)
        self.at("If neurons")
        self.play(LaggedStart(*[FadeIn(x[0]) for x in n],lag_ratio=.08),run_time=.7)
        self.at("the target decides")
        self.play(FadeOut(title), FadeIn(l), *[Create(x[1]) for x in n],run_time=.8)
        self.at("what exactly")
        self.play(FadeIn(T("What would the target be doing?",34).move_to([0,3.25,0])),run_time=.35)
        self.play(Indicate(t,color=YELLOW,scale_factor=1.03),run_time=.7)
        self.finish()


class S02Line(SpokenScene):
    def construct(self):
        intro = VGroup(*build_race())
        self.add(intro)
        lines = VGroup(T("Neurons compete", 46, BLUE), T("for a limiting amount", 40),
            T("of neurotrophic factor", 40, YELLOW), T("for survival.", 46, GREEN)).arrange(DOWN, buff=.48)
        self.at("Neurons compete")
        self.play(FadeOut(intro), FadeIn(heading("The neurotrophic hypothesis")), FadeIn(lines[0]), run_time=.4)
        self.at("for a limiting")
        self.play(FadeIn(lines[1]), run_time=.4)
        self.at("of neurotrophic")
        self.play(FadeIn(lines[2]), run_time=.4)
        self.at("for survival")
        self.play(FadeIn(lines[3]), run_time=.4)
        self.finish()


class S03Supply(SpokenScene):
    def construct(self):
        n,t,l,note=build_race()
        self.add(n,t,l,note)
        # A fixed few particles (fewer than the six axons), released from inside the target.
        starts=[(4.5,NY[0]),(4.1,NY[2]),(4.5,NY[4])]
        factors=VGroup(*[dot([x,y,0],YELLOW,.2) for x,y in starts])
        label=T("neurotrophic factor",28,YELLOW).move_to([-1.7,2.9,0])
        self.at("The targets supply")
        self.play(FadeIn(factors),FadeIn(label),run_time=.4)
        self.play(LaggedStart(*[f.animate.move_to([2.4,starts[k][1],0]) for k,f in enumerate(factors)],lag_ratio=.25),run_time=1.2)
        self.at("Axons that reach")
        self.play(*[factors[k].animate.move_to([1.55,NY[i],0]) for k,i in enumerate(WIN)],run_time=.6)
        self.at("take it up")
        self.play(*[factors[k].animate.move_to([-5.3,NY[i],0]) for k,i in enumerate(WIN)],run_time=.55)
        self.finish()


class S04Apop(SpokenScene):
    def construct(self):
        n,t,l,note=build_race()
        factors=VGroup(*[dot([-5.3,NY[i],0],YELLOW,.13) for i in WIN])
        l.move_to([3.5,2.9,0])
        self.add(n,t,l,note,factors)
        legend=VGroup(dot([-6.2,2.9,0],GREEN,.12),T("fed",26,GREEN).move_to([-5.7,2.9,0],aligned_edge=LEFT),
                      dot([-4.7,2.9,0],RED,.12),T("unfed",26,RED).move_to([-4.2,2.9,0],aligned_edge=LEFT))
        self.at("get too little")
        self.play(*[n[i].animate.set_color(RED) for i in [1,3,5]],
                  *[n[i].animate.set_color(GREEN) for i in WIN],FadeIn(legend),run_time=.6)
        self.at("die by apoptosis")
        self.play(*[FadeOut(n[i]) for i in [1,3,5]],
                  FadeIn(T("Apoptosis",36,TEXT).move_to([-0.7,2.9,0])),run_time=1.5)
        self.at("program of cell death")
        self.play(FadeIn(T("Built-in program of cell death",32,TEXT).move_to([-2.9,-2.75,0])),run_time=.35)
        self.finish()


class S05Pred(SpokenScene):
    def construct(self):
        r = checklist(ticks=())
        self.add(heading("Predictions"), r)
        self.at("the hypothesis makes predictions")
        self.play(LaggedStart(*[Indicate(row[0], color=TEXT) for row in r], lag_ratio=.15), run_time=1.1)
        self.finish()


class S06P1(SpokenScene):
    def construct(self):
        rows=checklist(0)
        self.add(heading("Predictions"),rows)
        self.at("Remove the target")
        reveal_row(self,rows,0,1,.4)
        self.at("wing bud removal")
        self.play(FadeIn(T("Chick wing bud · 1934 and 1949",26,GREY).move_to([-4.95,1.5,0],aligned_edge=LEFT)),
                  *[rows[i].animate.shift(DOWN*.35) for i in range(1,5)],run_time=.35)
        self.at("fits",lead=.25)
        self.play(FadeIn(T("fits",28,GREEN).next_to(rows[0][1],RIGHT,buff=.3)),run_time=.2)
        self.finish()


class S07P2(SpokenScene):
    def construct(self):
        r = checklist(1)
        self.add(heading("Predictions"), r)
        self.at("Add target")
        reveal_row(self, r, 1, 2)
        self.finish()


class S08P3(SpokenScene):
    def construct(self):
        r = checklist(2)
        self.add(heading("Predictions"), r)
        self.at("Add factor")
        reveal_row(self, r, 2, 3, .45)
        self.at("Remove factor")
        reveal_row(self, r, 3, 4, .45)
        self.finish()


class S09P4(SpokenScene):
    def construct(self):
        r=checklist(4)
        self.add(heading("Predictions"),r)
        self.at("most of the death")
        reveal_row(self,r,4,5,.35)
        self.at("around the time")
        self.play(*[FadeOut(r[i]) for i in range(4)], r[4].animate.move_to([0,2.0,0]),run_time=.4)
        self.at("axons reach the target")
        axis=Arrow([-6.4,-1.3,0],[6.5,-1.3,0],buff=0,color=GREY,stroke_width=6)
        tick=Line([-1.8,-1.3,0],[-1.8,-.2,0],color=BLUE,stroke_width=6)
        arrival=T("Arrival",34,BLUE).move_to([-1.8,-1.85,0])
        etime=T("Embryonic time",30).move_to([5.0,-1.85,0])
        self.play(FadeIn(axis),FadeIn(etime),Create(tick),FadeIn(arrival),run_time=.6)
        self.at("begin to compete")
        bar=Line([-1.8,-.5,0],[4.4,-.5,0],color=RED,stroke_width=22)
        self.play(Create(bar),FadeIn(T("Death period",36,RED).move_to([1.3,.45,0])),run_time=.6)
        self.finish()


class S10List(SpokenScene):
    def construct(self):
        r = checklist(5)
        self.add(heading("Predictions"), r)
        self.at("the first four items")
        self.play(*[r[i][1].animate.set_color(BLUE) for i in range(4)], r[4].animate.set_opacity(.4), run_time=.6)
        self.finish()


class S111976(SpokenScene):
    def construct(self):
        r = checklist(5, dim5=True)
        self.add(heading("Testing prediction 2"), r)
        self.at("In 1976")
        self.play(FadeIn(T("Hollyday and Hamburger · 1976", 26, GREY).move_to([0, -3.25, 0])), run_time=.5)
        self.at("tested the second item")
        self.play(r[1][1].animate.set_color(BLUE), *[r[i].animate.set_opacity(.3) for i in [0, 2, 3, 4]], run_time=.5)
        self.finish()


class S12Graft(SpokenScene):
    def construct(self):
        # Large connected chick silhouette; tissue diagram, not anatomical data.
        body=Ellipse(width=3.2,height=4.4,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([-1.25,-.1,0])
        head=Circle(.62,color=GREY,fill_color=BG,fill_opacity=1).move_to([-1.65,2.05,0])
        eye=dot([-1.35,2.22,0],TEXT,.07)
        beak=Polygon([-1.08,2.2,0],[-.6,1.95,0],[-1.08,1.8,0],color=GREY,fill_opacity=.4)
        def leg(y,color):
            limb=VMobject(color=color,stroke_width=22).set_points_as_corners([[0,y,0],[1.3,y-.4,0],[1.8,y-1.15,0]])
            toes=VGroup(*[Line([1.8,y-1.15,0],[2.35,y-1.15+d,0],color=color,stroke_width=7) for d in [-.25,0,.25]])
            return VGroup(limb,toes)
        normal=leg(-.9,BLUE); extra=leg(.8,YELLOW)
        normal_label=VGroup(T("Normal leg",30,BLUE).move_to([4,-2.3,0]),Line([2.4,-2.05,0],[3,-2.3,0],color=BLUE))
        extra_label=VGroup(T("Grafted leg",30,YELLOW).move_to([4,.8,0]),Line([1.5,.1,0],[3,.8,0],color=YELLOW))
        self.add(heading("Extra target tissue"),body,head,eye,beak,normal,normal_label,
            T("Schematic chick embryo · not anatomy",26,GREY).move_to([0,-3.4,0]))
        self.at("They grafted")
        self.play(FadeIn(extra,shift=RIGHT*.6),FadeIn(extra_label),run_time=.7)
        self.at("beside the normal one")
        self.play(Indicate(normal,color=BLUE,scale_factor=1.04),run_time=.6)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        q = question()
        self.add(q[0])
        self.at("With more target")
        self.play(FadeIn(q[1]), run_time=.4)
        self.at("the lumbar motor neurons")
        self.play(FadeIn(q[2]), run_time=.4)
        self.at("before the normal loss")
        self.play(FadeIn(q[3][0]), run_time=.4)
        self.at("and after it")
        self.play(FadeIn(q[3][1]), run_time=.4)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(question(),T("Pause and predict",30,TEAL).move_to([0,-2.6,0]))
        track=Line([-4,-3.25,0],[4,-3.25,0],color=GREY,stroke_width=8)
        timer=Line([-4,-3.25,0],[4,-3.25,0],color=TEAL,stroke_width=8)
        self.add(track,timer)
        self.play(timer.animate.stretch(.001,0,about_point=LEFT*4+DOWN*3.25),run_time=5,rate_func=linear)


class S15Reveal1(SpokenScene):
    def construct(self):
        g=bars()
        self.add(g[0],g[1],g[3],g[4])
        self.at("At day six")
        self.play(*[GrowFromEdge(b,DOWN) for b in g[2]],run_time=.7)
        self.at("there were no more")
        self.play(Indicate(g[2],color=BLUE,scale_factor=1.02),run_time=.6)
        self.finish()


class S16Reveal2(SpokenScene):
    def construct(self):
        g=bars(True); qualifier=vigorous()
        self.add(g[0],g[1],g[3],g[4],qualifier,g[5])
        self.at("whose grafts moved vigorously")
        self.play(*[GrowFromEdge(b,DOWN) for b in g[2]],run_time=.75)
        self.finish()


class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(bars(True),vigorous())
        self.wait(3)


class S18Word(SpokenScene):
    def construct(self):
        rows=compact_check()
        head=heading("Predictions")
        self.add(head,rows)
        self.at("They proposed")
        self.play(FadeIn(fits_mark(rows[1][1])),run_time=.4)
        self.at("hypothanasia")
        self.play(ReplacementTransform(head,T("Hypothanasia",54,font=TITLE_FONT).move_to([0,3.1,0])),run_time=.5)
        self.at("not extra birth")
        self.play(FadeIn(T("not extra birth",46,TEAL).move_to([1.6,1.0,0])),run_time=.3)
        self.at("but reduced death")
        self.play(FadeIn(T("but reduced death",46,GREEN).move_to([1.6,-.25,0])),run_time=.3)
        self.finish()


class S19Caution(SpokenScene):
    def construct(self):
        g = caution()
        self.add(g[0])
        self.at("from motor neurons")
        self.play(FadeIn(g[1]), run_time=.4)
        self.at("do not depend")
        self.play(FadeIn(g[2]), run_time=.5)
        self.finish()


class S20Caution2(SpokenScene):
    def construct(self):
        self.add(caution())
        self.at("a limiting target resource")
        self.play(FadeIn(T("Supports a limiting target resource", 30, TEXT).move_to([0, -1.7, 0])), run_time=.5)
        self.at("nothing about which molecule")
        self.play(FadeIn(T("Says nothing about which molecule", 30, TEXT).move_to([0, -2.7, 0])), run_time=.5)
        self.finish()


class S21Open(SpokenScene):
    def construct(self):
        self.add(heading("Left open: which scarce resource?"),
                 T("Hollyday and Hamburger · 1976",26,GREY).move_to([0,2.5,0]))

        def card(x,dots):
            # Same neutral outline, fill and drawing for both: terminal, gap, target cell.
            frame=RoundedRectangle(width=5.0,height=5.0,corner_radius=.2,color=GREY).move_to([x,-.5,0])
            stem=Line([x,1.55,0],[x,1.9,0],color=GREY,stroke_width=10)
            term=RoundedRectangle(width=2.6,height=1.1,corner_radius=.5,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([x,1.0,0])
            post=RoundedRectangle(width=3.8,height=.6,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([x,-.9,0])
            if dots:
                gap=VGroup(*[dot([x+dx,-.15,0],TEXT,.14) for dx in (-.8,0,.8)])
            else:
                gap=DoubleArrow([x,.4,0],[x,-.6,0],buff=0,color=TEXT,tip_length=.18,stroke_width=5)
            ves=VGroup(*[dot([x+dx,1.0,0],GREY,.1,.7) for dx in (-.6,0,.6)])
            return VGroup(frame,stem,term,ves,post,gap)

        left=card(-3.6,False); right=card(3.6,True)
        self.at("left open")
        self.play(FadeIn(T("?",90,GREY).move_to([0,-.5,0])),run_time=.35)
        self.at("synaptic space")
        self.play(FadeIn(left),FadeIn(T("Synaptic space",32).move_to([-3.6,-2.0,0])),run_time=.5)
        self.at("a trophic agent")
        self.play(FadeIn(right),FadeIn(T("Trophic agent",32).move_to([3.6,-2.0,0])),run_time=.5)
        self.finish()


class S22Shape(SpokenScene):
    def construct(self):
        lines=VGroup(T("Make too many,",42),T("then let the target keep what it can feed.",34)).arrange(DOWN,buff=.3).move_to([0,2.35,0])
        n,t,l,note=build_race()
        diagram=VGroup(n,t,l).scale(.62).move_to([0,-1.0,0])
        pos=l.get_center(); l.become(T("target tissue",26,GREY).move_to(pos))
        factors=VGroup(*[dot(n[i][1].get_end()+RIGHT*.7,YELLOW,.15) for i in WIN])
        self.add(lines,t,l,note,factors)
        self.at("Make too many")
        self.play(FadeIn(n),run_time=.6)
        self.at("then let the target keep")
        self.play(*[factors[k].animate.move_to(n[i][0]) for k,i in enumerate(WIN)],run_time=.55)
        self.at("what it can feed")
        self.play(*[n[i].animate.set_color(GREEN) for i in WIN],*[FadeOut(n[i]) for i in [1,3,5]],run_time=.8)
        self.finish()


class S23Next(SpokenScene):
    def construct(self):
        rows=compact_check(True)
        q=T("?",100,GREY).move_to([4.0,0,0])
        self.add(heading("The next tests"),rows,q)
        self.at("The next tests")
        self.play(*[Indicate(rows[i],color=YELLOW,scale_factor=1.05) for i in [2,3]],run_time=.8)
        self.at("need a molecule")
        self.play(rows[2].animate.set_color(YELLOW),rows[3].animate.set_color(YELLOW),run_time=.35)
        self.at("nerve growth factor")
        ngf=VGroup(T("Nerve growth factor",40,YELLOW),chip("NGF",YELLOW,46)).arrange(DOWN,buff=.45).move_to([4.0,0,0])
        self.play(ReplacementTransform(q,ngf),*[Indicate(rows[i],color=YELLOW,scale_factor=1.05) for i in [2,3]],run_time=.7)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        self.add(heading("Takeaway"),T("The hypothesis predicts",36).move_to([0,1.8,0]))
        self.at("reduced death")
        self.play(FadeIn(T("Reduced death",52,GREEN).move_to([0,.55,0])),run_time=.35)
        self.at("not extra birth")
        self.play(FadeIn(T("not extra birth",40,TEAL).move_to([0,-.65,0])),run_time=.35)
        self.at("When counts change")
        self.play(FadeIn(T("When counts change,",34).move_to([0,-1.95,0])),
            FadeIn(T("ask which happened.",34).move_to([0,-2.65,0])),run_time=.4)
        self.finish()


class S25End(EndCard):
    LINE = "Reduced death, not extra birth. When counts change, ask which happened."

    def construct(self):
        g=VGroup(T("Reduced death, not extra birth.",40,font=TITLE_FONT),
            T("When counts change, ask which happened.",32),
            T("biochemistrypedia.com",26,TEAL)).arrange(DOWN,buff=.65)
        self.play(FadeIn(g),run_time=.45)
        self.finish()
