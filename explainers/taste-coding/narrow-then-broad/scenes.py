"""Chapter 2: narrow at threshold, broader with strength.
COLOR MAP: sweet = orange; bitter = purple; sour = teal; neuron/wire = green.
Quantitative model: main input = blue; second input = purple; criterion = teal.
Outcome (ensemble only): crosses = gold, does not = grey. Stimulus/cue = yellow.
All traces and heights use activation=c/(1+c), response=weight*activation.
Schematic neuron tiles and arbitrary model proportions are explicitly labelled.
"""
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
SWEET, BITTER, SOUR = '#F2A65A', PURPLE, TEAL
GREY = '#ADB5C3'

def label(s,x=0,y=3.15,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def cross(p,r=.22):
    p=np.array(p)
    return VGroup(Line(p+[-r,-r,0],p+[r,r,0],color=RED,stroke_width=5),
                  Line(p+[-r,r,0],p+[r,-r,0],color=RED,stroke_width=5))

def cell(name,color,p,w=2.4):
    return VGroup(RoundedRectangle(width=w,height=1.05,corner_radius=.2,color=color,
                                   fill_opacity=.17),T(name,28,color)).move_to(p)

def neuron(p,r=.65,color=None):
    return Circle(radius=r,color=GREEN,stroke_width=4,fill_color=color or GREEN,
                  fill_opacity=.8 if color else .1).move_to(p)

def dual(p,r=.65,active=True,colors=(BITTER,SOUR)):
    parts=VGroup(*[Sector(radius=r,start_angle=a,angle=PI,color=c,
                           stroke_width=0,fill_opacity=.85 if active else .08)
                  for a,c in [(PI/2,colors[0]),(-PI/2,colors[1])]])
    parts.add(Circle(radius=r,color=GREEN,stroke_width=4))
    return parts.move_to(p)

def wire(a,b):
    return Line(a,b,color=GREEN,stroke_width=5)

def taste_legend(y=-2.6):
    return VGroup(*[chip(n,c,28).move_to([x,y,0]) for n,c,x in
                    [('sweet',SWEET,-3.4),('bitter',BITTER,0),('sour',SOUR,3.4)]])

def panel(mode,x=0,silenced=False,blocked=False,lit=True):
    """Fixed geometry across the prediction, two tests and inference."""
    title=label('A · convergence' if mode=='A' else 'B · one cell,\ntwo chemicals',x,2.95,28)
    b=cell('bitter cells',BITTER,[x+1.25,.65,0])
    n=dual([x,-1.6,0],.7,lit)
    bw=wire(b.get_bottom(),[x+.2,-.9,0])
    if mode=='A':
        s=cell('sour cells',SOUR,[x-1.25,.65,0])
        sw=wire(s.get_bottom(),[x-.2,-.9,0])
        cells=VGroup(s,b); wires=VGroup(sw,bw); chemicals=VGroup()
        if silenced:
            s.set_color(GREY); sw.set_color(GREY)
            chemicals.add(cross([x-2.42,1.18,0]))
    else:
        acid=chip('acid',SOUR,28).move_to([x-1.35,2.02,0])
        bitter=chip('bitter',BITTER,28).move_to([x+1.65,2.02,0])
        chemicals=VGroup(acid,bitter,
            Arrow(acid.get_bottom(),b.get_top()+[-.55,0,0],buff=.06,color=SOUR,tip_length=.16,max_tip_length_to_length_ratio=.5),
            Arrow(bitter.get_bottom(),b.get_top()+[.55,0,0],buff=.06,color=BITTER,tip_length=.16,max_tip_length_to_length_ratio=.5))
        cells=VGroup(b); wires=VGroup(bw)
    if blocked:
        b.set_color(GREY); bw.set_color(GREY)
        chemicals.add(cross(b.get_corner(UR),.22))
    return VGroup(title,cells,wires,n,chemicals)

def alternatives(silenced=False,blocked=False,lit=True):
    return VGroup(panel('A',-3.25,silenced,blocked,lit),panel('B',3.25,silenced,blocked,lit))

QUESTION='Under each idea, what happens\nto the bitter–sour neurons?'

def dual_tags(g):
    # Taste chips touch the lower sides of the split neuron.
    for p in g:
        x=p[3].get_center()[0]
        p.add(chip('bitter',BITTER,28).next_to(p[3],LEFT,buff=0),
              chip('sour',SOUR,28).next_to(p[3],RIGHT,buff=0))
    return g

def question_stage():
    return VGroup(dual_tags(alternatives(True)),label(QUESTION,0,-3.02,28,YELLOW),
                  label('pause and predict',0,3.55,28,YELLOW))

def reveal_stage():
    g=dual_tags(alternatives(True)); g[0].set_opacity(.35)
    g[0][3].set_color(GREY)
    return VGroup(g,label('predicted acid loss; not seen',-3.25,1.9,28),
                  label('if silencing worked',-2.65,-2.65,28),
                  label('bitter–sour neuron remains',3.25,-3.05,28),
                  neuron([-5.2,-3.1,0],.45).set_stroke(GREY),label('sour only',-3.8,-3.1,28))

def grid(broad=False):
    ns=VGroup()
    for i,(x,y) in enumerate([(x,y) for y in [1,-1] for x in [-3.5,0,3.5]]):
        colors=[SWEET,BITTER,SOUR]
        ns.add(dual([x,y,0],.72,colors=(colors[i%3],colors[(i+1)%3])) if broad and i<5 else neuron([x,y,0],.72,colors[i%3]))
    return ns

def slider(high=False,y=2.75):
    return VGroup(Line([-2.6,y,0],[2.6,y,0],color=GREY,stroke_width=4),
                  Dot([2.6 if high else -2.6,y,0],radius=.13,color=YELLOW),
                  label('low',-3.45,y,28),label('high',3.55,y,28))

BASE=-2.3
SCALE=4.55

def bar(v,x,c):
    return Rectangle(width=1.4,height=max(.012,SCALE*v),color=c,fill_opacity=.7,
                     stroke_width=3).move_to([x,BASE+SCALE*v/2,0])

def chart(a=1/3,w=.4,weights=False,relative=False,predict=False,neutral=False):
    vals=[1,w] if weights else [a,w*a]
    xs=[-2.1,1.25]; colors=[BLUE,PURPLE]
    axis=VGroup(Line([-4.65,BASE,0],[3.35,BASE,0],color=GREY),
                Line([-4.65,BASE,0],[-4.65,2.25,0],color=GREY),
                label('input weight' if weights else 'response, arbitrary units',-6.0,0,28).rotate(PI/2))
    for v in [0,.5,1]:
        y=BASE+SCALE*v
        axis.add(Line([-4.75,y,0],[-4.55,y,0],color=GREY),label(str(v),-5.12,y,28))
    bars=VGroup(*[bar(v,x,c) for v,x,c in zip(vals,xs,colors)])
    names=VGroup(*[label(t,x,-2.85,28,c) for t,x,c in zip(['main input','second input'],xs,colors)])
    ty=BASE+SCALE*(a*.5 if relative else .25)
    nums=VGroup()
    for v,x,c in zip(vals,xs,colors):
        ny=BASE+SCALE*v+.32
        if abs(ny-ty)<.3: ny=ty+.4
        nums.add(label(f'{v:.2f}'.rstrip('0').rstrip('.'),x,ny,30,c))
    threshold=VGroup(DashedLine([-4.5,ty,0],[3.35,ty,0],color=TEAL,stroke_width=3),
                     label('illustrative\nfraction of best' if relative else 'threshold\n0.25',4.95,ty+.1,28,TEAL))
    if weights: threshold.set_opacity(0)
    if predict:
        bars[1]=bar(.62,xs[1],GREY).set_fill(opacity=0).set_stroke(opacity=.45)
        nums=VGroup(label('?',xs[1],.9,40,YELLOW))
    if neutral:
        bars=VGroup(bar(.4*(1/3),-.8,BLUE)); nums=VGroup(); names=VGroup(label('one neuron’s signal',0,-2.85,28))
    return VGroup(axis,bars,names,nums,threshold)

def model_note(): return label('illustrative model',0,-3.48,28)

def low_question():
    return VGroup(chart(predict=True),slider(),label('Weak input: crosses at low? At high?',0,3.5,30,YELLOW),
                  model_note(),label('pause and predict',4.75,1.7,28,YELLOW))

def result_chart(high=False):
    return VGroup(chart(8/9 if high else 1/3),slider(high),
                  label('looks broad' if high else 'looks narrow',0,3.5,32),model_note())

def change_chart(scene,g,new,rt=.6):
    # Move only geometric marks; never interpolate glyphs or numerical text.
    scene.play(FadeOut(g[3]),FadeOut(g[4][1]),run_time=.12)
    scene.play(Transform(g[1],new[1]),Transform(g[4][0],new[4][0]),run_time=rt)
    g[3].become(new[3]); g[4][1].become(new[4][1])
    scene.play(FadeIn(g[3]),FadeIn(g[4][1]),run_time=.15)

def ensemble(active=False):
    weights=[.32,.4,.48,.62,.2,.15]; a=8/9
    g=VGroup()
    for x,w in zip([-4.7,-2.8,-.9,1,2.9,4.8],weights):
        c=GOLD if w*a>.25 else GREY
        n=neuron([x,1.4,0],.48,c if active else None)
        h=4.6*w*a; base=-2.3
        b=Rectangle(width=.95,height=h,color=c,fill_opacity=.75).move_to([x,base+h/2,0])
        g.add(VGroup(n,b,label(f'w {w:g}',x,2.32,28),label(f'{w*a:.2f}',x,base+h+.25,28,c)))
    line=DashedLine([-5.5,-2.3+4.6*.25,0],[5.5,-2.3+4.6*.25,0],color=TEAL)
    # Short responses use a side label so the criterion never strikes their values.
    for v in g:
        if abs(v[3].get_y()-line.get_y())<.3: v[3].shift(UP*.55)
    axis=VGroup(Line([-5.5,-2.3,0],[-5.5,.55,0],color=GREY))
    for v in [0,.5]:
        y=-2.3+4.6*v
        axis.add(Line([-5.65,y,0],[-5.4,y,0],color=GREY),label(str(v),-6.05,y,28))
    return VGroup(g,line,label('0.25',6.05,line.get_y(),28,TEAL),axis)

def ensemble_labels(data=True):
    return VGroup(label('weak-input response (weight × activation)',0,3.45,30),
      label('illustrative model · high strength',0,2.78,28),
      label('gold: crosses    grey: does not',0,-2.75,28),
      label('model proportions are arbitrary',0,-3.3,28),
      label('data: 35 of 41 broadened',0,-3.35,28,YELLOW) if data else VGroup())

class S00Title(TitleCard):
    LESSON='Taste from Tongue to Cortex'
    TITLE='Narrow at Threshold, Broader with Strength'
    def construct(self):
        self.add(label(self.LESSON,0,2.5,28),T('Narrow at Threshold,\nBroader with Strength',44,font=TITLE_FONT,line_spacing=1.15))
        self.add(Line([-1,-1.4,0],[1,-1.4,0],color=GOLD)); self.wait(self.narration_s)

class S01Q(SpokenScene):
    def construct(self):
        bud=Ellipse(width=2.4,height=4.2,color=GREY).move_to([-4.8,0,0])
        cells=VGroup(*[cell('',c,[-4.8,y,0],.65) for y,c in zip([-1.3,0,1.3],[SWEET,BITTER,SOUR])])
        fibres=VGroup(*[wire([-4.35,y,0],[1.7,y,0]) for y in [-1.3,0,1.3]])
        dest=RoundedRectangle(width=2.4,height=3.8,color=GREEN).move_to([3,0,0])
        self.add(bud,cells,label('taste bud',-4.8,2.65,30),dest,label('to the\nbrain',3,0,32))
        self.at('each taste fiber'); self.play(Create(fibres),run_time=.45)
        self.at('carry one taste'); self.play(FadeIn(label('one taste per fibre?',0,3.25,36,YELLOW)),run_time=.3)
        pattern=VGroup(*[Dot([x,y,0],radius=.11,color=c) for y,c in zip([-1.3,0,1.3],[SWEET,BITTER,SOUR]) for x in [-2.6,-1.9,-.4]])
        other=VGroup(RoundedRectangle(width=11.8,height=1.25,corner_radius=.18,color=GREY,stroke_opacity=.4,fill_opacity=.03).move_to([0,-2.95,0]),
          label('or a pattern across fibres?',1.3,-2.95,32,YELLOW))
        for y in [-2.6,-2.95,-3.3]:
            other.add(wire([-5.5,y,0],[-3.7,y,0]))
        for i,c in enumerate([SWEET,BITTER,SOUR]):
            for j in range(3): other.add(Dot([-5.25+j*.6,-2.6-i*.35,0],radius=.07,color=c))
        self.at('a pattern across'); self.play(FadeIn(pattern),FadeIn(other),run_time=.4); self.finish()

class S02Line(SpokenScene):
    def construct(self):
        ys=[2.25,0,-2.25]
        pops=VGroup(*[cell(n+' cells',c,[-4.4,y,0],3) for n,c,y in zip(['sweet','bitter','sour'],[SWEET,BITTER,SOUR],ys)])
        ws=VGroup(*[wire([-2.9,y,0],[3.8,y,0]) for y in ys]); self.add(pops)
        self.at('listened only'); self.play(Create(ws),run_time=.5)
        self.at('a labeled line'); self.play(FadeIn(label('labelled line',0,3.4,34)),run_time=.3)
        self.at('Its activity'); self.play(FadeIn(VGroup(*[chip(n,c,30).move_to([4.9,y,0]) for n,c,y in zip(['sweet','bitter','sour'],[SWEET,BITTER,SOUR],ys)])),run_time=.3); self.finish()

class S03Imaging(SpokenScene):
    def construct(self):
        ns=VGroup(*[neuron([x,y,0],.65) for y in [.7,-1.15] for x in [-3.5,0,3.5]])
        field=RoundedRectangle(width=10.3,height=4.1,color=GREY).move_to([0,-.2,0])
        lens=VGroup(
          Rectangle(width=1.05,height=.27,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([0,2.86,0]),
          Polygon([-.48,2.73,0],[.48,2.73,0],[.29,2.07,0],[-.29,2.07,0],color=GREY,fill_color=GREY,fill_opacity=.3),
          Rectangle(width=.6,height=.2,color=GREY,fill_color=GREY,fill_opacity=.5).move_to([0,1.98,0]),
          Ellipse(width=.62,height=.16,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([0,1.85,0]))
        self.add(field,ns,label('anaesthetized mice',0,-3.45,28))
        self.at('and colleagues imaged'); self.play(FadeIn(lens),FadeIn(label('Barretto and colleagues · 2015',0,3.4,30)),run_time=.35)
        self.at('geniculate ganglion neurons'); self.play(FadeIn(label('geniculate ganglion neurons',0,-2.65,30,GREEN)),run_time=.3)
        self.at('flowed over the tongue')
        for i,(name,c) in enumerate([('sweet',SWEET),('bitter',BITTER),('sour',SOUR)]):
            stim=chip(name+' over tongue',c,28).move_to([-3.9,2.45,0])
            self.play(FadeIn(stim),ns[i].animate.set_fill(c,.9),run_time=.2)
            self.play(stim.animate.shift(RIGHT*.4),run_time=.8)
            self.play(FadeOut(stim),ns[i].animate.set_fill(GREEN,.1),run_time=.15)
        self.finish()

class S04Most(SpokenScene):
    def construct(self):
        ns=grid(); self.add(ns,taste_legend(-2.7),label('responding neurons',0,3.25,32))
        self.at('strongly activated'); self.play(*[Indicate(n,scale_factor=1.1,color=[SWEET,BITTER,SOUR][i%3]) for i,n in enumerate(ns)],run_time=.5)
        self.at('only one'); self.play(FadeIn(label('one tested taste per neuron',0,-3.45,30)),run_time=.3); self.finish()

class S05Odd(SpokenScene):
    def construct(self):
        n=dual([0,-.15,0],2.35)
        self.add(n,label('bitter–sour neuron',0,3.2,36),
                 chip('bitter',BITTER,32).next_to(n,LEFT,buff=0),chip('sour',SOUR,32).next_to(n,RIGHT,buff=0))
        self.at('Some neurons'); self.play(Indicate(n,scale_factor=1.025,color=GREEN),run_time=.4); self.finish()

class S06Converge(SpokenScene):
    def construct(self):
        g=panel('A'); g.scale(1.15)
        self.add(g[0],g[3],g[1])
        self.at('gets input'); self.play(Create(g[2]),run_time=.35)
        self.at('both sour and bitter'); self.play(Indicate(g[1],scale_factor=1.02),run_time=.25); self.finish()

class S07Onecell(SpokenScene):
    def construct(self):
        g=panel('B'); g.scale(1.15); self.add(g[0],g[3],g[1])
        self.at('listens only'); self.play(Create(g[2]),run_time=.3)
        self.at('bitter cells'); self.play(FadeIn(g[4][1]),Create(g[4][3]),run_time=.3)
        self.at('acid also activates'); self.play(FadeIn(g[4][0]),Create(g[4][2]),run_time=.35); self.finish()

class S08Q(SpokenScene):
    def construct(self):
        g=dual_tags(alternatives()); self.add(g)
        self.at('the sour cells'); new=dual_tags(alternatives(True)); self.play(FadeOut(g),FadeIn(new),run_time=.25)
        self.at('Under each idea'); self.play(FadeIn(label(QUESTION,0,-3.02,28,YELLOW)),FadeIn(label('pause and predict',0,3.55,28,YELLOW)),run_time=.3); self.finish()

class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_stage()); self.wait(5)

class S10Reveal(SpokenScene):
    def construct(self):
        g=dual_tags(alternatives(True)); sour=neuron([-5.2,-3.1,0],.45,SOUR)
        self.add(g,sour,label('sour only',-3.8,-3.1,28,SOUR))
        self.at('responses disappeared'); self.play(sour.animate.set_fill(GREY,.1).set_stroke(GREY),run_time=.35)
        self.at('class was still there')
        dimmed=g[0].copy().set_opacity(.35); dimmed[3].set_color(GREY)
        self.play(Transform(g[0],dimmed),FadeIn(label('predicted acid loss; not seen',-3.25,1.9,28)),FadeIn(label('if silencing worked',-2.65,-2.65,28)),FadeIn(label('bitter–sour neuron remains',3.25,-3.05,28)),run_time=.35); self.finish()

class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(reveal_stage()); self.wait(3)

class S12Block(SpokenScene):
    def construct(self):
        g=alternatives(); self.add(g)
        self.at('were blocked instead'); new=alternatives(blocked=True); self.play(FadeOut(g),FadeIn(new),run_time=.3)
        self.at('class disappeared')
        sour_only=dual(new[0][3].get_center(),.7,colors=(BITTER,SOUR))
        sour_only[0].set_fill(BITTER,.08)
        dark=dual(new[1][3].get_center(),.7,active=False)
        self.play(Transform(new[0][3],sour_only),Transform(new[1][3],dark),
                  FadeIn(label('both ideas predict this',0,-2.8,34,YELLOW)),
                  FadeIn(label('bitter–sour class gone in both',0,-3.4,28)),run_time=.35); self.finish()

class S13Rule(SpokenScene):
    def construct(self):
        g=panel('B',0); g[0].shift(DOWN*.15); self.add(g)
        self.at('authors concluded'); self.play(FadeIn(label('✓',2.9,.65,58,GREEN)),FadeIn(label('support for labelled lines',0,3.65,28,GREEN)),run_time=.3)
        self.at('acid drives'); self.play(Indicate(g[4][0],scale_factor=1.07),run_time=.35)
        self.at('through bitter cells'); self.play(Indicate(g[2],color=YELLOW,scale_factor=1),run_time=.35)
        self.at('For these neurons'); self.play(FadeIn(label('the fibre reports which cell population is active\nnot which chemical is on the tongue',0,-2.95,30)),run_time=.12); self.finish()

class S14Wu(SpokenScene):
    def construct(self):
        ns=grid(); sl=slider(y=2.45)
        self.add(ns,sl,taste_legend(-2.75),label('Wu and colleagues · 2015',0,3.45,32),label('six schematic tiles · anaesthetized mice',0,-3.45,28))
        self.at('compared low'); self.play(Indicate(ns,scale_factor=1.02),run_time=.3)
        self.at('Tuning broadened'); self.play(Transform(sl,slider(True,y=2.45)),FadeOut(ns),FadeIn(grid(True)),run_time=.5)
        self.play(FadeIn(label('split fill: two or more tastes',-1.4,-2.05,28)),FadeIn(label('did not broaden',4.15,-2.15,28)),run_time=.25); self.finish()

class S15Broaden(SpokenScene):
    def construct(self):
        ns=grid(); sl=slider(y=2.45); self.add(ns,sl,taste_legend(-2.75),label('same neurons · six schematic tiles',0,3.45,30))
        self.at('most became more broadly tuned'); self.play(Transform(sl,slider(True,y=2.45)),FadeOut(ns),FadeIn(grid(True)),
          FadeIn(label('split: two or more tastes',-1.4,-2.05,28)),FadeIn(label('did not broaden',4.15,-2.15,28)),FadeIn(label('35 of 41 broadened · data, within-neuron',0,-3.45,28,YELLOW)),run_time=.4); self.finish()

class S16Threshold(SpokenScene):
    def construct(self):
        g=chart(neutral=True); self.add(g[0],g[2],g[4],label('one neuron · fixed criterion',0,3.35,32),model_note())
        self.at('its signal crosses'); self.play(GrowFromEdge(g[1],DOWN),run_time=.4)
        self.at('a fixed threshold'); self.play(Transform(g[1],VGroup(bar(.4*(8/9),-.8,BLUE))),run_time=.45); self.finish()

class S17Inputs(SpokenScene):
    def construct(self):
        g=chart(weights=True); self.add(g[0],g[2],label('input weights',0,3.4,34),model_note())
        self.at('a full input'); self.play(GrowFromEdge(g[1][0],DOWN),FadeIn(g[3][0]),run_time=.4)
        self.at('a weak one'); self.play(GrowFromEdge(g[1][1],DOWN),FadeIn(g[3][1]),run_time=.4); self.finish()

class S18MadeUp(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,9,2],y_range=[0,1,.5],x_length=9.4,y_length=4.7,axis_config={'include_tip':False,'color':GREY}).move_to([.15,-.1,0])
        curve=ax.plot(lambda c:c/(1+c),x_range=[0,9,.025],color=BLUE,use_smoothing=False)
        self.add(ax,label('illustrative, not data',0,3.45,32,YELLOW),label('concentration',0,-3.2,30),
                 label('each input\n(activation, 0 to 1)',-4.4,2.9,28))
        for v in [0,.5,1]: self.add(label(str(v),-5.1,ax.c2p(0,v)[1],28))
        for v in [0,4,8]: self.add(label(str(v),ax.c2p(v,0)[0],-2.85,28))
        self.at('Each input saturates'); self.play(Create(curve),run_time=1)
        self.at('concentration rises'); self.play(FadeIn(VGroup(Dot(ax.c2p(.5,1/3),color=YELLOW),Dot(ax.c2p(8,8/9),color=YELLOW))),
          FadeIn(label('low: 0.33',-2.8,-.5,30)),FadeIn(label('high: 0.89',2.4,2.55,30)),run_time=.3); self.finish()

class S19Q(SpokenScene):
    def construct(self):
        self.add(low_question()); self.at('does the weak input'); self.finish()

class S20Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(low_question()); self.wait(5)

class S21Low(SpokenScene):
    def construct(self):
        q=low_question(); self.add(q)
        self.at('the main input crosses'); g=chart(); self.play(FadeOut(q),FadeIn(VGroup(g,slider(),model_note(),label('response = weight × activation',0,3.5,30))),run_time=.3)
        self.at('the weak one stays below'); self.play(Indicate(g[1][1],scale_factor=1.04),FadeIn(label('0.4 × 0.33 = 0.13',4.55,1.6,28,PURPLE)),run_time=.35)
        self.at('neuron looks narrow'); self.play(FadeIn(label('looks narrow',4.6,.7,32)),run_time=.25); self.finish()

class S22High(SpokenScene):
    def construct(self):
        g=chart(); sl=slider(); self.add(g,sl,model_note(),label('response = weight × activation',0,3.5,30))
        self.at('At high strength'); self.play(Transform(sl,slider(True)),run_time=.35)
        self.at('weak input climbs'); change_chart(self,g,chart(8/9),.55)
        self.at('now looks broad'); self.play(FadeIn(label('looks broad',4.7,1.6,32)),run_time=.25); self.finish()

class S23Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(result_chart(True)); self.wait(3)

class S24Never(SpokenScene):
    def construct(self):
        g=chart(1,w=.2); marker=label('full activation = 1, weak input = 0.2',0,3.5,30)
        self.add(g,marker,model_note())
        self.at('a weak input'); self.play(Indicate(g[1][1],scale_factor=1.04),run_time=.3)
        self.at('never reaches'); self.play(Indicate(g[4],scale_factor=1.01),run_time=.3)
        self.at('Whenever the main response'); sl=slider(); self.play(FadeOut(marker),run_time=.12); self.play(FadeIn(label('weak input never reaches 0.25',0,3.5,30,YELLOW)),FadeIn(sl),run_time=.2); change_chart(self,g,chart(1/3,w=.2),.45)
        self.at('the neuron responds'); self.play(Transform(sl,slider(True)),run_time=.25); change_chart(self,g,chart(8/9,w=.2),.45)
        self.at('in this panel only'); self.play(Indicate(g[1][1],scale_factor=1.04),run_time=.25); self.finish()

class S25Most(SpokenScene):
    def construct(self):
        g=ensemble(True); labels=ensemble_labels(False); self.add(g,labels)
        self.at('different weak inputs differ'); self.play(*[Indicate(v[1],scale_factor=1.025) for v in g[0]],run_time=.35)
        self.at('Some broaden'); self.play(*[Indicate(v[0],color=GOLD,scale_factor=1.04) for v in g[0][:4]],run_time=.3)
        self.at('some do not'); self.play(*[Indicate(v[0],color=GREY,scale_factor=1.04) for v in g[0][4:]],run_time=.3)
        self.at('found most broadened'); self.play(FadeOut(labels[3]),run_time=.1); self.play(FadeIn(label('data: 35 of 41 broadened · model proportions arbitrary',0,-3.35,28,YELLOW)),run_time=.2); self.finish()

class S26Data(SpokenScene):
    def construct(self):
        g=ensemble(True); labs=ensemble_labels(False); labs.remove(labs[3]); self.add(g,labs,label('data: 35 of 41 broadened · model proportions arbitrary',0,-3.35,28,YELLOW))
        self.at('Those data fit'); self.play(FadeOut(labs[1]),run_time=.1); self.play(FadeIn(label('compatible, not proof',0,2.78,30)),run_time=.2)
        self.at('do not show'); self.play(g.animate.set_opacity(.2),run_time=.35); self.finish()

class S27Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; labs=ensemble_labels(False); labs.remove(labs[3],labs[1]); self.add(ensemble(True).set_opacity(.2),labs,label('compatible, not proof',0,2.78,30),label('data: 35 of 41 broadened · model proportions arbitrary',0,-3.35,28,YELLOW)); self.wait(2)

class S28Criterion(SpokenScene):
    def construct(self):
        g=chart(); sl=slider(); note=model_note(); self.add(g,sl,label('relative criterion',0,3.5,32),note)
        self.at("neuron's own best"); new=chart(relative=True)
        self.play(Transform(g[4][0],new[4][0]),run_time=.35)
        g[3].become(new[3]); g[4][1].become(new[4][1])
        count=label('inputs above the line: 1',0,-3.5,28); self.remove(note); self.add(count)
        self.at('all inputs rose alike'); high=chart(8/9,relative=True)
        self.play(Transform(sl,slider(True)),Transform(g[1],high[1]),
                  Transform(g[4][0],high[4][0]),
                  *[g[3][i].animate.move_to(high[3][i]) for i in range(2)],
                  g[4][1].animate.move_to(high[4][1]),run_time=.4)
        g[3].become(high[3])
        count.become(label('inputs above the line: 1 at low, 1 at high',0,-3.5,28))
        self.at('breadth would not change'); self.play(Indicate(count,scale_factor=1.02),run_time=.25); self.finish()

class S29Take(SpokenScene):
    def construct(self):
        self.add(label('“Narrow” depends on…',0,3.4,38))
        cards=VGroup(*[cell(t,c,[0,y,0],8.5) for t,c,y in [('stimulus panel',SWEET,2),('concentration range',YELLOW,.2),('response criterion',TEAL,-1.6)]])
        for c in cards: c[0].stretch(1.3,1)
        self.add(*[c[0].copy().set_opacity(.25) for c in cards])
        self.at('the panel'); self.play(FadeIn(cards[0]),run_time=.2)
        self.at('the concentration'); self.play(FadeIn(cards[1]),run_time=.2)
        self.at('the criterion'); self.play(FadeIn(cards[2]),run_time=.2)
        self.at("laboratories'"); self.play(FadeIn(label('The results need not conflict.\nWhat explains the difference is not settled.',0,-2.95,30)),run_time=.2); self.finish()

class S30End(EndCard):
    LINE='Narrow depends on the panel, the concentration and the criterion.'
    def construct(self):
        self.add(T('Narrow depends on the panel,\nthe concentration and the criterion.',34,font=TITLE_FONT),label('biochemistrypedia.com',0,-1.55,28,TEAL)); self.wait(self.narration_s)
