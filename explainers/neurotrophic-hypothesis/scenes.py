"""Chapter 1: Too Small, or Lost?
COLOR MAP: BLUE neurons; GREEN survivors (only in conclusion diagrams);
RED dying cells/removal; YELLOW target support/NGF; TEAL dividing cells;
GREY anatomy/axes; GOLD guiding rule. All counts are schematic, not data.
No molecular structures or quantitative traces.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as _SpokenScene

class SpokenScene(_SpokenScene):
    # Word cues are audio-relative. No anticipatory lead or per-scene silent tail.
    def at(self, phrase, lead=0, nth=0):
        return super().at(phrase, lead=lead, nth=nth)
    def finish(self):
        remaining = self.narration_s - self.elapsed()
        if remaining > .001:
            self.wait(remaining)

def label(s,x=0,y=3.05,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])

def dot(p,color=BLUE,r=.24):
    return Circle(radius=r,stroke_color=color,stroke_width=2.5,
                  fill_color=color,fill_opacity=1).move_to(p)

def ganglion(center,n=7,sp=.56,radius=.24):
    # Stable positions allow a population to lose cells without moving survivors.
    positions=[(0,.65),(-.65,-.35),(.65,-.35),(-.7,.65),(.7,.65),(-1.3,-.35),(1.3,-.35),(-.65,-1.25),(.65,-1.25),(0,-1.25)]
    return VGroup(*[dot(np.array(center)+np.array([x*sp/.56,y*sp/.56,0]),r=radius) for x,y in positions[:n]])

def arr(a,b,color=GREY):
    return Arrow(a,b,buff=.18,color=color,stroke_width=4,tip_length=.2)

def note():
    return label('Schematic counts · not experimental data',y=-3.35,size=26,color=GREY)

def wing(center=(-4,0,0),scale=1):
    w=VMobject(color=GREY,fill_color=GREY,fill_opacity=.2,stroke_width=3)
    w.set_points_smoothly([[-.5,-.7,0],[.2,-.55,0],[.8,.1,0],[.55,.8,0],[-.2,.6,0],[-.5,-.7,0]])
    return w.scale(scale).move_to(center)

def embryo():
    # Curled trunk, flexed tail, large head and eye of an early chick embryo.
    body=VMobject(color=GREY,fill_color=GREY,fill_opacity=.15,stroke_width=4)
    body.set_points_smoothly([[.1,1.7,0],[-.9,1.2,0],[-1.2,.2,0],[-1.1,-1.2,0],[-.3,-2.1,0],[.6,-1.9,0],[.8,-1.3,0],[.1,-1.5,0],[-.25,-.7,0],[.15,.4,0],[.7,1.1,0],[.1,1.7,0]])
    head=Ellipse(width=2.1,height=1.65,color=GREY,fill_color=GREY,fill_opacity=.18).move_to([.25,1.8,0])
    eye=dot([.7,1.9,0],GREY,.15)
    return VGroup(body,head,eye,wing([-1.75,.3,0],1.55),wing([.65,.05,0],.7))

def removed_bud(e):
    return DashedVMobject(e[3].copy().set_fill(opacity=0).set_stroke(RED),num_dashes=12)

def cord():
    return VGroup(Ellipse(width=2,height=4,color=GREY,fill_color=GREY,fill_opacity=.13).move_to([-4,0,0]),
                  label('Spinal cord',-4,-2.55,28,GREY))

def anatomy():
    return cord(),ganglion([-.7,.1,0],7,sp=.65,radius=.29)

def histories(lost=True):
    a=ganglion([-3.8,1.3,0],5,sp=.52)
    b=ganglion([-3.8,-1.55,0],7,sp=.52)
    if lost:
        for d in b[5:]: d.set_opacity(.12)
    final=ganglion([4,.1,0],5,sp=.75,radius=.33)
    return VGroup(a,b,final,
        arr([-2.3,1.3,0],[2.5,.55,0]),arr([-2.3,-1.55,0],[2.5,-.05,0]),
        label('Few made, all stay',-3.8,2.62,28),label('Many made, some lost',-3.8,-.25,28),
        label('Number of neurons: 5',-3.8,.4,26,BLUE),
        label('Number of neurons: 7 → 5',-3.8,-2.45,26,BLUE),
        label('Same small ganglion',3.9,-1.25,28),note())

def questions():
    return VGroup(label('What are the two histories?',y=3.42,size=32),
                  label('What would you measure to tell them apart?',y=-3.1,size=28))

def branch_picture():
    h=histories()
    # Compact mini-paths ending at one common count.
    h[5].become(label('Never made?',-3.8,2.62,30))
    h[6].become(label('Made, then lost?',-3.8,-.25,30))
    h[9].become(label('One final count',3.9,-1.25,28))
    return VGroup(*h[:10])

def time_strip(marks=False):
    cells=VGroup(*[ganglion([x,.15,0],n,sp=.58,radius=.25) for x,n in zip([-4,0,4],[7,7,5])])
    counts=VGroup(*[label(str(n),x,-1.3,40,BLUE) for x,n in zip([-4,0,4],[7,7,5])])
    axis=VGroup(arr([-5.6,-2,0],[5.7,-2,0]),
        *[Line([x,-2.15,0],[x,-1.85,0],color=GREY) for x in [-4,0,4]],
        label('Embryo stage (earlier → later)',y=-2.65,size=28,color=GREY))
    heading=label('Neurons counted',y=2.75,size=32)
    g=VGroup(cells,counts,axis,heading,note())
    if marks:
        g.add(VGroup(*[dividing(cells[i][0].get_center()) for i in [0,1]]),
              dying_marks())
    return g

def dying_marks():
    # The two cells lost between stage 2 and stage 3 (7 -> 5), beside the late ganglion.
    return VGroup(*[dying([x,.15,0]) for x in [5.45,6.0]])

def dividing(p):
    return VGroup(Circle(radius=.36,color=TEAL,stroke_width=4).move_to(p),
                  T('+',40,TEAL).move_to(p))

def dying(p,r=.25):
    return dot(p,'#252A34',r).set_stroke(RED,width=4)

def state_key(kind,x,y):
    glyph=dividing([x-1.1,y,0]) if kind=='Dividing' else dying([x-1.3,y,0])
    return VGroup(glyph,label(kind,x+.2,y,28,TEAL if kind=='Dividing' else RED))

def fibres(cells):
    middle = np.mean([d.get_center()[1] for d in cells])
    paths=[]
    for d in cells:
        direction=UP if d.get_center()[1]>middle else DOWN
        start=d.get_top() if direction[1]>0 else d.get_bottom()
        paths.append(CubicBezier(start,start+direction*.25,
                     start+direction*.55+RIGHT*.15,start+direction*.72+RIGHT*.12,
                     color=BLUE,stroke_width=3))
    return VGroup(*paths)

def fibre_label():
    return VGroup(label('Fibres',-3.5,-2.45,30,BLUE),
        arr([-3.9,-2.12,0],[-4.2,-1.55,0],BLUE))

def pair(with_fibres=False,late=False):
    a=ganglion([-3.4,.1,0],7,sp=.8,radius=.31)
    b=ganglion([2.7,.1,0],7,sp=.8,radius=.31)
    fs=VGroup(fibres(a),fibres(b))
    if late:
        for d in b[5:]: d.set_fill('#252A34',1).set_stroke(RED,width=4)
        for f in fs[1][5:]: f.set_opacity(.12)
    labs=VGroup(label('Other side (comparison)',-3.3,2.5,28,GREY),
                label('Operated side',3,2.5,28,GREY),note())
    return VGroup(a,b,labs,fs if with_fibres else VGroup())

def limb_link(with_cord=False):
    if with_cord:
        cd=Ellipse(width=1.5,height=3.2,color=GREY,fill_color=GREY,fill_opacity=.13).move_to([2.3,0,0])
        return VGroup(wing([-4.2,0,0],2.25),cd,ganglion([4.9,0,0],5,sp=.8,radius=.32),
                  label('Limb',-4.2,-2.25,32,GREY),label('Spinal cord',2.3,-2.25,28,GREY),
                  label('Ganglion',4.9,-2.25,30,BLUE))
    return VGroup(wing([-4,0,0],2.25),ganglion([3.2,0,0],5,sp=.85,radius=.34),
                  label('Limb',-4,-2.25,32,GREY),label('Ganglion',3.2,-2.25,32,BLUE))

def made_lost(y=3.4):
    return VGroup(label('Made,',0,0,44,TEXT),label('then lost.',0,0,44,RED)).arrange(RIGHT,buff=.28).move_to([0,y,0])

def conclusions(n=3):
    texts=['1   Made in excess, then lost','2   Kept or not depends on the target',
           '3   Target supplies something; too little → compete']
    return VGroup(*[label(t,y=2.15-i*.85,size=28) for i,t in enumerate(texts[:n])])

def conclusion_key():
    return VGroup(dot([-4.7,-2.75,0],BLUE,.12),label('Neuron',-3.8,-2.75,26,BLUE),
                  dot([-.9,-2.75,0],GREEN,.12),label('Survivor',.2,-2.75,26,GREEN))

IDEA_Y=(1.85,.9,.1)

def idea_base(compact=False):
    # Compact card: the end state of s27 and all of s28, so nothing jumps.
    if compact:
        return VGroup(label('One guiding idea',y=3.1,size=30,color=GREY),
            Line([-5.5,2.6,0],[5.5,2.6,0],color=GOLD),
            label('Make too many,',y=IDEA_Y[0],size=44,color=BLUE),
            label('then let the target keep',y=IDEA_Y[1],size=34),
            label('what it can feed.',y=IDEA_Y[2],size=36))
    return VGroup(label('One guiding idea',y=3.1,size=30,color=GREY),
        Line([-5.5,2.6,0],[5.5,2.6,0],color=GOLD),
        label('Make too many,',y=1.5,size=60,color=BLUE),
        label('then let the target keep',y=.05,size=48),
        label('what it can feed.',y=-1.25,size=54))

def ngf_lines():
    return VGroup(chip('Nerve growth factor (NGF)',YELLOW,32).move_to([0,-1.0,0]),
        label('NGF, acting as a survival factor,',y=-1.85,size=30),
        label('decides how many neurons made stay alive.',y=-2.45,size=30))

class S00Title(TitleCard):
    LESSON='The Neurotrophic Hypothesis Tested'
    TITLE='Too Small, or Lost?'
    def finish(self):
        if self.narration_s > self.elapsed(): self.wait(self.narration_s-self.elapsed())

class S01Q(SpokenScene):
    def construct(self):
        e=embryo().scale(1.15); outline=removed_bud(e); name=label('Chick embryo',0,-3.05,28,GREY)
        self.add(e,name)
        self.at('Remove one wing bud'); self.play(e[3].animate.set_fill(RED,.35).set_stroke(RED),run_time=.3)
        self.play(FadeOut(e[3]),FadeIn(outline),run_time=.9)
        e[3].set_opacity(0)  # Keep the removed child hidden when its parent moves.
        g=ganglion([-.3,-.5,0],5,sp=.4,radius=.2)
        self.at('The neurons serving'); self.play(e.animate.shift(LEFT*2.9),outline.animate.shift(LEFT*2.9),name.animate.shift(LEFT*2.9),FadeIn(g),FadeIn(label('Fewer neurons',-.2,-1.6,28,BLUE)),run_time=.5)
        self.at('Were they never made'); self.play(FadeIn(label('Never made?',3.3,2.7,30)),
            FadeIn(ganglion([2.4,1.5,0],5,sp=.38,radius=.18)),
            GrowArrow(arr([3.3,1.5,0],[4.3,1.5,0])),FadeIn(ganglion([5.1,1.5,0],5,sp=.38,radius=.18)),run_time=.4)
        b=ganglion([2.4,-.8,0],7,sp=.38,radius=.18)
        self.at('Or were they made'); self.play(FadeIn(label('Made, then lost?',3.6,.3,30)),FadeIn(b),run_time=.35)
        self.at('and then lost'); self.play(*[d.animate.set_opacity(.12) for d in b[5:]],
            GrowArrow(arr([3.3,-.8,0],[4.3,-.8,0])),FadeIn(ganglion([5.1,-.8,0],5,sp=.38,radius=.18)),run_time=.4)
        self.finish()

class S02Target(SpokenScene):
    def construct(self):
        soma=dot([-4.8,0,0],r=.65)
        dendrites=VGroup(*[Line([-5.25,y,0],[-6,2*y,0],color=BLUE,stroke_width=4) for y in [-.4,0,.4]])
        muscle=VGroup(*[RoundedRectangle(width=2.4,height=.3,corner_radius=.14,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([3.6,1.05+i*.36,0]) for i in range(4)])
        gland=VGroup(*[Ellipse(width=.9,height=1.1,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([3.6+dx,-1.5+dy,0]) for dx,dy in [(-.5,0),(.4,0),(0,.6)]])
        self.add(soma,dendrites,muscle,gland,label('Neuron',-4.8,-1.4,30,BLUE))
        glow=VGroup(*[m.copy().set_fill(opacity=0).set_stroke(YELLOW,width=16,opacity=.22) for m in list(muscle)+list(gland)])
        self.add(glow); glow.set_opacity(0)
        self.at('A target is'); self.play(FadeIn(label('Targets',3.6,3,38,YELLOW)),
            *[m.animate.set_fill(YELLOW,.3).set_stroke(YELLOW,3) for m in list(muscle)+list(gland)],
            *[g.animate.set_stroke(YELLOW,width=16,opacity=.22) for g in glow],run_time=.5)
        ax=VGroup(Line([-4.1,0,0],[.8,0,0],color=BLUE,stroke_width=5),Line([.8,0,0],[2.3,1.6,0],color=BLUE,stroke_width=5),Line([.8,0,0],[2.5,-1.5,0],color=BLUE,stroke_width=5))
        self.at('an axon grows'); self.play(Create(ax),FadeIn(label('Axon',-1.5,.5,30,BLUE)),run_time=.6)
        self.at('a limb muscle'); self.play(FadeIn(label('Limb muscle',3.6,.35,28)),run_time=.3)
        self.at('or a gland'); self.play(FadeIn(label('Gland',3.6,-2.8,28)),run_time=.3)
        self.finish()

class S03Ganglion(SpokenScene):
    def construct(self):
        c,g=anatomy(); self.add(c[0],g)
        self.at('A ganglion is'); self.play(FadeIn(label('Ganglion',-.6,2.6,34,BLUE)),GrowArrow(arr([-.6,2.1,0],[-.6,1.2,0],BLUE)),run_time=.35)
        self.at('neuron cell bodies'); self.play(Indicate(g,color=BLUE,scale_factor=1.07),run_time=.4)
        self.at('spinal cord'); self.play(FadeIn(c[1]),run_time=.3)
        self.finish()

class S04Spinal(SpokenScene):
    def construct(self):
        c,g=anatomy(); self.add(c,g)
        self.at('Spinal ganglia sit'); self.play(FadeIn(label('Spinal ganglion',-.6,2.6,30,BLUE)),run_time=.3)
        self.at('sensory neurons'); self.play(FadeIn(label('Sensory neurons',-.9,-2.55,26,BLUE)),run_time=.3)
        chain=VGroup(*[ganglion([3.1,y,0],3,sp=.4,radius=.23) for y in [1.25,0,-1.25]])
        self.at('Sympathetic ganglia'); self.play(Create(Line([3.1,1.7,0],[3.1,-1.5,0],color=GREY)),FadeIn(chain),FadeIn(label('Sympathetic ganglia',3.1,2.6,28,BLUE)),run_time=.4)
        self.at('sympathetic nervous system'); self.play(FadeIn(label('Sympathetic nervous system',3.1,-2.55,26,BLUE)),run_time=.3)
        self.finish()

class S051934(SpokenScene):
    def construct(self):
        e=embryo().scale(1.12); self.add(e,label('Hamburger · 1934',y=3.3,size=32))
        self.at('removed one wing bud'); self.play(FadeOut(e[3]),FadeIn(removed_bud(e)),FadeIn(label('Bud removed',-5.2,.3,30,RED)),GrowArrow(arr([-3.9,.3,0],[-3.2,.3,0],RED)),run_time=.4)
        self.at('from chick embryos'); self.play(FadeIn(label('Comparison',3.8,.3,30,GREY)),GrowArrow(arr([2.5,.3,0],[1.3,.1,0])),run_time=.4)
        self.at('about three days old'); self.play(FadeIn(label('Chick embryo · about 3 days old',y=-3.1,size=30,color=GREY)),run_time=.3)
        self.finish()

class S06Result(SpokenScene):
    def construct(self):
        p=pair(); self.add(p,label('Later in development',y=3.15,size=32),label('Bud removed',3,-2.15,28,RED))
        self.at('reduced'); self.play(*[FadeOut(d) for d in p[1][5:]],FadeIn(label('Smaller ganglion',3,-1.25,30,BLUE)),run_time=.4)
        self.finish(); self.wait(1)  # Read the reduced result before the interpretation.

class S07First(SpokenScene):
    def construct(self):
        l=limb_link(True); self.add(l,label('First reading · 1934',y=3.15,size=32))
        self.at('the limb controlling'); self.play(GrowArrow(arr([-2.3,0,0],[1.2,0,0])),run_time=.5)
        self.at('how many cells grew'); self.play(FadeIn(label('Limb controls how many cells grow?',y=2.1,size=32)),run_time=.4)
        self.finish()

class S08Hidden(SpokenScene):
    def construct(self):
        b=branch_picture(); g=ganglion([0,-.2,0],5,sp=1.3,radius=.5); caption=label('One final count',y=-2.1,size=32)
        self.add(g,caption)
        self.at('one count at the end'); self.play(Indicate(g,color=BLUE),run_time=.4)
        self.at('two possible histories'); self.play(Transform(g,b[2]),Transform(caption,b[9]),FadeIn(VGroup(*[b[i] for i in [0,1,3,4,5,6,7,8]])),run_time=.5)
        self.finish()

class S09Predict(SpokenScene):
    def construct(self):
        self.add(branch_picture()); q=questions()
        self.at('What are the two histories'); self.play(FadeIn(q[0]),run_time=.3)
        self.at('And what would you measure'); self.play(FadeIn(q[1]),run_time=.3)
        self.finish()

class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(branch_picture(),questions(),label('Pause the video to predict',3.6,2.1,26,TEAL)); self.wait(5)

class S11Reveal1(SpokenScene):
    def construct(self):
        h=histories(False); self.add(note())
        self.at('Fewer neurons'); self.play(FadeIn(h[0]),FadeIn(h[5]),FadeIn(h[7]),run_time=.3)
        self.at('might have been made'); self.play(GrowArrow(h[3]),FadeIn(h[2]),FadeIn(h[9]),run_time=.4)
        self.at('Or the normal number'); self.play(FadeIn(h[1]),FadeIn(h[6]),FadeIn(h[8]),run_time=.4)
        self.at('and then lost'); self.play(*[d.animate.set_opacity(.12) for d in h[1][5:]],GrowArrow(h[4]),run_time=.6)
        self.finish()

class S12Reveal2(SpokenScene):
    def construct(self):
        h=histories(); self.add(h)
        self.at('Both give a small ganglion'); self.play(Indicate(h[2],color=BLUE),run_time=.4)
        strip=time_strip()
        self.at('To separate them'); self.play(FadeOut(h),FadeIn(VGroup(*strip[2:])),run_time=.35)
        self.at('you count at a series'); self.play(LaggedStart(*[FadeIn(VGroup(strip[0][i],strip[1][i])) for i in range(3)],lag_ratio=.3),run_time=.7)
        self.finish()

class S13Marks(SpokenScene):
    def construct(self):
        s=time_strip(); self.add(s)
        self.at('cells that are dividing'); self.play(FadeIn(VGroup(*[dividing(s[0][i][0].get_center()) for i in [0,1]])),FadeIn(state_key('Dividing',-2.5,1.65)),run_time=.4)
        self.at('cells that are dying'); self.play(FadeIn(dying_marks()),FadeIn(state_key('Dying cells',2.6,1.65)),run_time=.4)
        self.finish()

class S141949(SpokenScene):
    def construct(self):
        e=embryo().scale(.7).move_to([-3.7,-.2,0]); g=ganglion([2.3,-.2,0],7,sp=.75,radius=.3)
        self.add(e,g,label('1949',y=3.15,size=44,color=TEAL),label('Chick spinal ganglia',2.5,-2.3,30,GREY))
        self.at('Hamburger and'); self.play(FadeIn(label('Hamburger and Rita Levi-Montalcini',y=2.2,size=32)),run_time=.4)
        self.at('did exactly that'); self.play(GrowArrow(arr([-1.8,0,0],[.5,0,0])),run_time=.4)
        self.finish()

class S15Stage(SpokenScene):
    def construct(self):
        self.add(label('Follow ganglia stage by stage',y=3.15,size=32),note())
        xs=[-1.6,1.6,4.8]
        self.add(label('Other side',-4.5,1.4,28,GREY),label('Operated side',-4.5,-.4,28,GREY),
            arr([-3.2,-2.3,0],[6.2,-2.3,0]),label('Embryo stage (earlier → later)',1.6,-2.75,28,GREY))
        mk=lambda x,y,n: ganglion([x,y,0],n,sp=.5,radius=.22)
        control=VGroup(*[mk(x,1.3,7) for x in xs])
        operated=VGroup(*[mk(x,-.5,7) for x in xs])
        tag=label('− limb tissue',-4.5,-1.1,28,RED)
        # First stage is already on screen with its tag when the scene opens.
        self.add(control[0],operated[0],tag)
        self.at('stage by stage'); self.play(LaggedStart(*[FadeIn(VGroup(control[i],operated[i])) for i in [1,2]],lag_ratio=.3),run_time=.7)
        self.at('after removing'); self.play(*[FadeOut(d) for d in operated[2][5:]],run_time=.35)
        for d in operated[2][5:]: d.set_opacity(0)
        # Reset the previous outcome before presenting the adding experiment.
        self.at('or adding limb tissue'); self.play(FadeOut(operated),Transform(tag,label('+ limb tissue',-4.5,-1.1,28,YELLOW)),run_time=.2)
        added=VGroup(*[mk(x,-.5,n) for x,n in zip(xs,[7,7,9])])
        self.play(FadeIn(added),run_time=.3); self.finish()

class S16Found(SpokenScene):
    def construct(self):
        p=pair(True); self.add(p[:3],label('Early stages',y=3.15,size=32))
        self.at('and grew'); self.play(Create(p[3]),FadeIn(fibre_label()),run_time=.5)
        self.finish()

class S17Dying(SpokenScene):
    def construct(self):
        p=pair(True); self.add(p,label('Later stages',y=3.15,size=32),fibre_label())
        self.at('Degenerating cells'); self.play(*[d.animate.set_fill('#252A34',1).set_stroke(RED,width=4) for d in p[1][5:]],FadeIn(state_key('Dying cells',2.7,-2.15)),run_time=.4)
        self.at('became conspicuous later'); self.play(*[f.animate.set_opacity(.12) for f in p[3][1][5:]],run_time=.4)
        self.finish()

class S18Reveal(SpokenScene):
    def construct(self):
        self.add(pair(True,True),state_key('Dying cells',2.7,-2.15))
        m=made_lost()
        self.at('The neurons had been made'); self.play(FadeIn(m[0]),run_time=.35)
        self.at('Then they were lost'); self.play(FadeIn(m[1]),run_time=.35)
        self.finish()

class S19Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(pair(True,True),state_key('Dying cells',2.7,-2.15),made_lost()); self.wait(3)

class S20Alive(SpokenScene):
    def construct(self):
        l=limb_link(); self.add(l)
        self.at('seemed to keep'); self.play(GrowArrow(arr([-2.3,0,0],[1.1,0,0])),run_time=.35)
        self.at('neurons alive'); self.play(FadeIn(label('Helps keep neurons alive?',y=2.7,size=38)),run_time=.35)
        self.at('It was not only'); self.play(FadeIn(label('Beyond making neurons',y=-3.05,size=28,color=GREY)),run_time=.35)
        self.finish()

class S21C1(SpokenScene):
    def construct(self):
        g=ganglion([0,-.2,0],7,sp=.95,radius=.36)
        self.add(label('Three conclusions',y=3.15,size=34),conclusion_key(),g)
        self.at('First neurons are made'); self.play(FadeIn(conclusions(1)),Indicate(g,color=BLUE,scale_factor=1.03),run_time=.35)
        self.at('and then lost'); self.play(*[FadeOut(d) for d in g[5:]],*[d.animate.set_color(GREEN) for d in g[:5]],run_time=.5)
        self.finish()

class S22C2(SpokenScene):
    def construct(self):
        self.add(label('Three conclusions',y=3.15,size=34),conclusions(1),conclusion_key())
        g=ganglion([0,-.2,0],5,sp=.95,radius=.36).set_color(GREEN); self.add(g)
        target=wing([3.8,-.6,0],1.5)
        self.at('Second'); self.play(g.animate.shift(DOWN*.5),FadeIn(conclusions(2)[1]),run_time=.3)
        self.at('whether they are kept'); self.play(g.animate.move_to([-3.2,-.5,0]),FadeIn(target),FadeIn(label('Target',3.8,-2.1,28,GREY)),run_time=.3)
        self.at('depends on the target'); self.play(GrowArrow(arr([2.5,-.5,0],[-1.2,-.5,0])),run_time=.4)
        self.finish()

class S23C3(SpokenScene):
    def construct(self):
        c=conclusions(); self.add(label('Three conclusions',y=3.15,size=34),c[:2],conclusion_key())
        supply=chip('?',YELLOW,42).move_to([.2,-1.15,0]); target=wing([4.3,-1.15,0],1.1)
        tlabel=label('Target',4.3,-2.35,28,GREY)
        cells=ganglion([-4.2,-1.15,0],5,sp=.6,radius=.26).set_color(GREEN)
        self.at('Third the target'); self.play(FadeIn(c[2]),FadeIn(target),FadeIn(tlabel),run_time=.3)
        self.at('must supply something'); self.play(FadeIn(supply),FadeIn(cells),FadeIn(label('Something the target supplies',.5,-2.05,26,YELLOW)),run_time=.4)
        self.at('If it supplies too little'); self.play(GrowArrow(arr([3.2,-1.15,0],[1,-1.15,0],YELLOW)),run_time=.35)
        self.at('they must in effect compete'); self.play(*[Create(CubicBezier(d.get_top(),d.get_top()+UP*.4,np.array([-.45,-.35,0]),np.array([-.45,-1.15,0]),color=GREY)) for d in cells],run_time=.5)
        self.finish()

class S24Not(SpokenScene):
    def construct(self):
        c=conclusions(); self.add(label('Three conclusions',y=3.15,size=34),c)
        box=DashedVMobject(SurroundingRectangle(c[2],buff=.25,color=YELLOW),num_dashes=40)
        self.at('Neither the something'); self.play(Create(box),FadeIn(chip('?',YELLOW,64).move_to([0,-1.15,0])),run_time=.4)
        self.at('They were inferences'); self.play(FadeIn(label('Inferred · not yet shown',y=-2.6,size=36,color=YELLOW)),run_time=.4)
        self.finish()

class S25Earn(SpokenScene):
    def construct(self):
        self.add(label('The neurotrophic hypothesis',y=2.6,size=40))
        rows=VGroup(*[VGroup(Square(side_length=.65,color=GREY).move_to([-1.5,y,0]),label('Test '+str(i+1),.2,y,34)) for i,y in enumerate([1,.0,-1])])
        self.at('would have to earn them'); self.play(Create(rows),run_time=.5)
        self.at('one test at a time'); self.play(FadeIn(label('One test at a time',y=-2.7,size=36,color=TEAL)),run_time=.4)
        self.finish()

class S26Idea(SpokenScene):
    def construct(self):
        c=idea_base(); g=ganglion([0,0,0],7,sp=.85,radius=.32)
        self.add(c[:2],g)
        self.at('make too many'); self.play(FadeOut(g),FadeIn(c[2]),run_time=.4)
        self.at('then let the target'); self.play(FadeIn(c[3]),run_time=.4)
        self.at('keep what it can feed'); self.play(FadeIn(c[4]),run_time=.4)
        self.finish()

class S27Idea2(SpokenScene):
    def construct(self):
        c=idea_base(); self.add(c); n=ngf_lines()
        self.at('The test case is'); self.play(c[2].animate.scale(44/60).move_to([0,IDEA_Y[0],0]),c[3].animate.scale(34/48).move_to([0,IDEA_Y[1],0]),c[4].animate.scale(36/54).move_to([0,IDEA_Y[2],0]),run_time=1.0)
        self.at('nerve growth factor'); self.play(FadeIn(n[0]),run_time=.35)
        self.at('Acting as a survival factor'); self.play(FadeIn(n[1]),run_time=.35)
        self.at('it decides how many'); self.play(FadeIn(n[2]),run_time=.35)
        self.finish()

class S28Idea3(SpokenScene):
    def construct(self):
        self.add(idea_base(True),ngf_lines())
        self.at('above the number made'); self.play(FadeIn(label('Never above the number made.',y=-3.3,size=34,color=TEAL)),run_time=.4)
        self.finish()

class S29Take(SpokenScene):
    def construct(self):
        g=ganglion([0,-.2,0],5,sp=1.4,radius=.5); l=label('One count = a size',y=2.8,size=40)
        self.add(g,l,note())
        s=time_strip(True); s[3].become(label('Counts across time = a history',y=2.75,size=36))
        s.add(state_key('Dividing',-2.5,1.65),state_key('Dying cells',2.6,1.65))
        self.at('history'); self.play(FadeOut(g),FadeOut(l),FadeIn(s),run_time=.4)
        self.finish()

class S30End(EndCard):
    LINE='Count across time before you decide.'
    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT); fit(line,max_w=11.5)
        sub=T('biochemistrypedia.com',26,TEAL)
        self.add(VGroup(line,sub).arrange(DOWN,buff=.4)); self.finish()
    def finish(self):
        if self.narration_s > self.elapsed(): self.wait(self.narration_s-self.elapsed())
