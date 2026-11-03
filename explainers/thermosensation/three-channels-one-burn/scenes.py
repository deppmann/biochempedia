"""Three Channels, One Burn: labelled cartoons, no molecular structures.
COLOR MAP: ORANGE #F29E4C warm sensory fibre; BLUE cool fibre / TRPM8;
YELLOW heat / signal; GREEN retained behaviour; RED removal; GREY anatomy.
Spike rasters use an illustrative regular-rate model, not experimental traces:
r(rest)=2, r(cool)=4, r(warm)=0.5 Hz; TRPM8 loss sets all rates to zero.
These rates illustrate the lesson's ongoing-rate model, without estimating data.
"""
from bp_style import *
import numpy as np

ORANGE = '#F29E4C'
STIM, REPORT, GONE, COOL = YELLOW, GREEN, RED, BLUE
NAMES = ['TRPV1', 'TRPM3', 'TRPA1']


def arr(a, b, color=STIM, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=.19,
                 max_tip_length_to_length_ratio=.4)


def cross(c, s=.23):
    c=np.array(c)
    return VGroup(Line(c+[-s,-s,0],c+[s,s,0],color=GONE,stroke_width=6),
                  Line(c+[-s,s,0],c+[s,-s,0],color=GONE,stroke_width=6))


def centered(text, size=30, color=TEXT, font=FONT):
    return VGroup(*[T(line,size,color,font=font) for line in text.split('\n')]).arrange(DOWN,buff=.13)


def block(name, pos, color=GREY, width=2.6, height=1.35, lit=False, size=30):
    box=RoundedRectangle(width=width,height=height,corner_radius=.17,
                         stroke_color=color,stroke_width=3,fill_color=color,
                         fill_opacity=.25 if lit else .07).move_to(pos)
    text=centered(name,size).move_to(box.get_center())
    return VGroup(box,text)


def knockout(b):
    # The X is outside the block; the channel name always stays bright.
    return cross(b.get_left()+LEFT*.37)


def heading(text):
    return T(text,34,font=TITLE_FONT).move_to([0,3.28,0])


def response(out, lit):
    color=REPORT if lit else GREY
    return out[0].animate.set_stroke(color).set_fill(color,.25 if lit else .04)


def series():
    bs=VGroup(*[block(n,[x,1.1,0],width=2.8,height=2.5) for n,x in zip(NAMES,[-4.2,0,4.2])])
    out=block('acute withdrawal',[0,-1.65,0],REPORT,width=4.5,height=1.45,lit=True)
    path=VGroup(Line([4.2,-.15,0],[4.2,-1.65,0],color=STIM,stroke_width=5),
                arr([4.2,-1.65,0],[2.38,-1.65,0]))
    arrows=VGroup(arr([-2.7,1.1,0],[-1.5,1.1,0]),
                  arr([1.5,1.1,0],[2.7,1.1,0]),path)
    return bs,arrows,out


def parallel(lit=True):
    bs=VGroup(*[block(n,[-3.65,y,0],height=1.5) for n,y in zip(NAMES,[2,0,-2])])
    out=block('acute\nwithdrawal',[3.65,0,0],REPORT if lit else GREY,
              width=3.7,height=2.3,lit=lit,size=32)
    arrows=VGroup(*[arr(b.get_right()+RIGHT*.13,[1.65,y,0]) for b,y in zip(bs,[.75,0,-.75])])
    return bs,arrows,out


def series_question():
    return T('What would each single knockout do?',32).move_to([0,-3.03,0])


def parallel_question():
    return T('What would remove the reflex?',32).move_to([0,-3.12,0])


def retained():
    return T('response retained',28,REPORT).move_to([3.65,-1.7,0])


def assay_note():
    return centered('acute withdrawal absent\nin the reported assays\n(2018)',26,TEXT).move_to([3.65,-2.23,0])


def triple_frame():
    bs,a,out=parallel(False)
    return VGroup(heading('All three removed'),bs,out,assay_note(),*[knockout(b) for b in bs])


def preference_pair():
    wd=block('acute\nwithdrawal',[-3.5,-.65,0],width=5.0,height=3.2,size=36)
    pref=block('preference for\nmoderate\ntemperatures',[3.35,-.65,0],REPORT,width=5.1,height=3.2,lit=True,size=32)
    q=T('?',58,GONE).move_to([3.35,2.08,0])
    unknown=T('source unknown',26).move_to([.15,2.1,0])
    lead=Line([1.65,2.1,0],[2.7,2.1,0],color=GREY)
    a=arr([3.35,1.65,0],[3.35,1.08,0],REPORT)
    tag=VGroup(T('not these three channels alone',28,REPORT).move_to([3.2,-2.65,0]),
               T('same mice, all three channels removed',28).move_to([0,-3.3,0]))
    return wd,pref,VGroup(q,unknown,lead,a),tag


def raster(rate,x0,x1,y,color=COOL):
    # Regular point process: event times t_k=(k+1/2)/r, on a 4-s window.
    base=Line([x0,y,0],[x1,y,0],color=GREY,stroke_width=2)
    times=np.arange(.5/rate,4,1/rate) if rate else []
    spikes=VGroup(*[Line([x0+(x1-x0)*t/4,y,0],[x0+(x1-x0)*t/4,y+.34,0],color=color,stroke_width=3) for t in times])
    return VGroup(base,spikes)


def cool_panel(compact=False, lost=False):
    cx=-3.5 if compact else 0
    title=T('Cool line',32,COOL).move_to([cx,3.22,0])
    xleft=-5.65 if compact else -4.9
    xright=-.8 if compact else 5.1
    ending=Circle(.35,color=COOL,fill_opacity=.22).move_to([xleft,1.65,0])
    axon=Line([xleft+.35,1.65,0],[xright,1.65,0],color=COOL,stroke_width=7)
    channel=block('TRPM8',[xleft+1.1,2.4,0],COOL,width=2.2,height=1.0,size=28)
    # Short leader anchors the TRPM8 tag to the sensory ending.
    ending=VGroup(ending,Line([xleft,2.0,0],[xleft+1.1,1.9,0],color=COOL,stroke_width=3))
    traces=VGroup()
    labels=VGroup()
    for name,rate,y,color in [('rest',2,.65,COOL),('cool',4,-.45,COOL),('warm',.5,-1.55,STIM)]:
        labels.add(T(name,28,color).move_to([xleft+.15,y+.17,0]))
        traces.add(raster(0 if lost else rate,xleft+1.25,xright,y,color))
    note=T('silent: nothing to slow' if lost else 'schematic firing',26).move_to([cx,-2.3,0])
    g=VGroup(title,ending,axon,channel,labels,traces,note)
    if lost:
        g.add(knockout(channel))
    return g


def split_heat():
    bs=VGroup(*[block(n,[1.7,y,0],width=2.25,height=1.25,size=30) for n,y in zip(NAMES,[2,.25,-1.5])])
    out=block('acute\nwithdrawal',[5.0,.25,0],REPORT,width=2.65,height=2.0,lit=True,size=30)
    arrows=VGroup(*[arr(b.get_right()+RIGHT*.07,[3.6,y,0],w=4) for b,y in zip(bs,[.9,.25,-.4])])
    return bs,arrows,out


def warmth_lost():
    return centered('warmth lost\nmouse forepaw task',26,GONE).move_to([-3.5,-3.05,0])


class S00Title(TitleCard):
    TITLE='Three Channels, One Burn'
    LESSON='Hot, Warm, Cool and Cold'


class S01Q(SpokenScene):
    def construct(self):
        heat=block('painful heat',[-4.6,-.35,0],STIM,width=2.6,height=2.2)
        channel=block('TRPV1',[-.8,-.35,0],height=2.2)
        # Paw cartoon: pad plus four toes, not a labelled rectangle.
        paw=VGroup(Ellipse(width=1.65,height=1.1,color=GREY,fill_opacity=.35),
                   *[Circle(.24,color=GREY,fill_opacity=.35).move_to([x,.65+(.1 if abs(x)<.3 else 0),0]) for x in [-.62,-.2,.22,.64]]).move_to([4.1,-.35,0])
        surface=Line([2.6,-1.55,0],[5.7,-1.55,0],color=STIM,stroke_width=10)
        label=T('hot surface',28,STIM).move_to([4.1,-2.12,0])
        pawlabel=T('mouse paw',28).move_to([4.1,1.25,0])
        pawgroup=VGroup(paw,pawlabel)
        self.at('Mice without',lead=0)
        self.add(heading('A missing channel, a retained reflex'),heat,channel,pawgroup,surface,label,
                 arr([-3.2,-.35,0],[-2.2,-.35,0]),knockout(channel))
        self.at('keep much')
        self.play(pawgroup.animate.shift(UP*1.1),run_time=.65)
        self.at('so what else')
        bypass=DashedVMobject(arr([-4.6,.95,0],[2.95,1.35,0]),num_dashes=24)
        self.play(Create(bypass),FadeIn(T('?',38,STIM).move_to([-.5,1.65,0])),
                  FadeIn(T('What else senses the burn?',34).move_to([0,-3.1,0])),run_time=.35)
        self.finish()


class S02M3(SpokenScene):
    def construct(self):
        positions=[[-3.5,1.1,0],[0,1.1,0],[3.5,1.1,0],[-1.75,-1.25,0],[1.75,-1.25,0]]
        cells=VGroup(*[VGroup(Circle(.85,color=GREY,fill_opacity=.12),Line([.85,0,0],[1.3,.3,0],color=GREY)).move_to(p) for p in positions])
        self.at('In',lead=0)
        self.add(cells,heading('2011 · small mouse sensory neurons'))
        self.at('was found')
        stimulus=T('heat stimulus',28,STIM).move_to([-4.7,-2.9,0])
        stimuli=VGroup(arr([-5.5,-2.45,0],[-4.5,.75,0]),
                        arr([-4.0,-2.45,0],[-2.7,-1.35,0]))
        self.play(FadeIn(stimulus),*[GrowArrow(a) for a in stimuli],run_time=.4)
        self.at('heat sensitivity')
        # Qualitative cluster: explicitly a subset, never a proportion estimate.
        tags=VGroup(*[T('TRPM3',24).move_to(cells[i][0]) for i in [0,3]])
        self.play(*[cells[i][0].animate.set_stroke(ORANGE).set_fill(ORANGE,.32) for i in [0,3]],FadeIn(tags),run_time=.4)
        self.at('some small')
        self.play(FadeIn(T('a subset',28,ORANGE).move_to([-1.95,-2.45,0])),run_time=.35)
        self.finish()


class S03M3b(SpokenScene):
    def construct(self):
        b=block('TRPM3',[0,.4,0],width=4.6,height=3.9,size=42)
        self.at('Mice lacking',lead=0)
        x=knockout(b)
        self.add(b,x,heading('Mouse · channel removed'))
        self.at('avoided noxious')
        note=T('less avoidance of noxious heat',32,STIM).move_to([0,-2.65,0])
        self.play(FadeIn(note),run_time=.35)
        self.at('was a third')
        bs=VGroup(*[block(n,[xx,.25,0],height=3.5,width=3.3,size=34) for n,xx in zip(NAMES,[-4.3,0,4.3])])
        tags=VGroup(*[T(t,26).move_to([xx,-2.08,0]) for t,xx in zip(['known','reported 2011','candidate'],[-4.3,0,4.3])])
        self.clear()
        self.add(heading('Three candidates for heat'))
        self.play(ReplacementTransform(b,bs[1]),FadeIn(bs[0]),FadeIn(bs[2]),FadeIn(tags),run_time=.45)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        bs,a,out=series()
        self.add(bs)
        self.at('Suppose the three',lead=0)
        self.play(FadeIn(heading('Suppose: in series')),run_time=.3)
        self.at('each passing')
        self.play(Create(a),FadeIn(out),run_time=.65)
        self.at('What would each')
        self.play(FadeIn(series_question()),run_time=.3)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(heading('Suppose: in series'),*series(),series_question())
        self.add(T('Pause and predict',26,TEAL).move_to([-4.65,-1.65,0]))
        bar=Line([-5.8,-3.55,0],[5.8,-3.55,0],color=TEAL,stroke_width=4)
        self.play(Create(bar),run_time=5,rate_func=linear)


class S06Reveal(SpokenScene):
    def construct(self):
        bs,a,out=series()
        title=heading('Prediction if the channels were in series')
        self.add(bs,a,out,title)
        self.at('In series',lead=0)
        xs=VGroup(*[knockout(b) for b in bs])
        self.at('every single knockout')
        # All three individual cases appear in turn, never an unreadable name.
        self.add(xs[0])
        self.at('would abolish',lead=0)
        self.play(response(out,False),a.animate.set_opacity(.12),run_time=.15)
        for i in [1,2]:
            self.play(ReplacementTransform(xs[i-1],xs[i]),run_time=.2)
            self.wait(.28)
        self.at('They do not',lead=0)
        self.play(response(out,True),FadeOut(a),
                  Transform(title,heading('Observed: each single knockout retains withdrawal')),
                  FadeIn(T('Single knockouts do not abolish withdrawal',29,REPORT).move_to([0,-3.05,0])),run_time=.2)
        # Cycle the observed single-knockout outcomes with an unchanged green box.
        previous=xs[2]
        for i in [0,1]:
            self.remove(previous)
            previous=knockout(bs[i])
            self.add(previous); self.wait(.35)
        self.finish()


class S07Predict2(SpokenScene):
    def construct(self):
        bs,a,out=series(); pbs,pa,po=parallel()
        self.add(bs,a,out)
        self.at('Now',lead=0)
        self.play(FadeOut(a),run_time=.2)
        self.at('suppose they work')
        self.play(Transform(bs,pbs),Transform(out,po),FadeIn(heading('Suppose: in parallel')),run_time=.5)
        self.play(Create(pa),run_time=.4)
        self.at('What would it')
        self.play(FadeIn(parallel_question()),run_time=.3)
        self.finish()


class S08Pause2(Scene):
    def construct(self):
        self.camera.background_color=BG
        bs,a,out=parallel()
        self.add(heading('Suppose: in parallel'),bs,a,out,parallel_question(),
                 T('Pause and predict',26,TEAL).move_to([3.65,-2.18,0]))
        bar=Line([-5.8,-3.58,0],[5.8,-3.58,0],color=TEAL,stroke_width=4)
        self.play(Create(bar),run_time=5,rate_func=linear)


class S09Reveal2(SpokenScene):
    def construct(self):
        bs,a,out=parallel()
        self.add(bs,a,out)
        self.at('All three at once',lead=0)
        # The answer is visible from the start of 'All three at once'.
        self.remove(a)
        self.add(heading('All three removed'),*[knockout(b) for b in bs])
        out[0].set_stroke(GREY).set_fill(GREY,.04)
        self.at('In',lead=0)
        self.play(FadeIn(assay_note()),run_time=.3)
        self.at('mice lacking')
        self.at('lacked acute')
        self.at('in the reported')
        self.finish()


class S10Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(triple_frame()); self.wait(3)


class S11Redund(SpokenScene):
    def construct(self):
        bs,a,out=parallel()
        self.add(bs,a,out)
        self.at('The channels',lead=0)
        self.at('redundant for')
        self.play(FadeIn(heading('Redundant for this reflex')),run_time=.3)
        self.at('Remove one',lead=0)
        self.play(Create(knockout(bs[0])),a[0].animate.set_opacity(.08),FadeIn(retained()),run_time=.3)
        self.at('others carry')
        self.play(Indicate(a[1:],color=STIM,scale_factor=1.03),run_time=.45)
        self.finish()


class S12Redund2(SpokenScene):
    def construct(self):
        bs,a,out=parallel(); a[0].set_opacity(.08)
        r=retained()
        self.add(bs,a,out,knockout(bs[0]),r,heading('Redundant for this reflex'))
        self.at('Remove all',lead=0)
        # Reset outcome and remove routes in the very same beat.
        self.remove(r,a)
        self.add(T('acute withdrawal absent',26).move_to([3.65,-1.7,0]))
        out[0].set_stroke(GREY).set_fill(GREY,.04)
        self.play(*[Create(knockout(bs[i])) for i in [1,2]],run_time=.3)
        self.at('acute reflex'); self.at('nothing left')
        self.finish()


class S13Pref(SpokenScene):
    def construct(self):
        wd,pref,source,tag=preference_pair()
        self.at('but',lead=0)
        self.add(wd,tag,heading('Withdrawal and temperature preference'))
        self.play(FadeIn(source),run_time=.3)
        self.at('still preferred')
        self.play(FadeIn(pref),run_time=.4)
        self.finish()


class S14Pref2(SpokenScene):
    def construct(self):
        wd,pref,source,tag=preference_pair()
        self.add(wd,pref,source,tag)
        self.at('Withdrawal and preference',lead=0)
        self.add(heading('Different behaviors'))
        self.at('Whatever supports',lead=0)
        self.play(Indicate(source[0],color=GONE,scale_factor=1.25),run_time=1.6)
        self.at('not exhausted')
        self.play(Indicate(pref[0],color=REPORT,scale_factor=1.02),run_time=.5)
        self.finish()


class S15Idea(SpokenScene):
    def construct(self):
        c=cool_panel()
        self.at('Set this beside',lead=0)
        self.add(c[0],c[1],c[2],c[4][0],c[5][0],c[6])
        self.at('resting firing')
        self.play(FadeIn(c[4][1:]),FadeIn(c[5][1:]),
                  FadeIn(T('cool: faster · warm: slower',28).move_to([0,-3.15,0])),run_time=.55)
        self.at('depends on')
        self.play(FadeIn(c[3]),run_time=.35)
        self.finish()


class S16Idea2(SpokenScene):
    def construct(self):
        c=cool_panel(); compact=cool_panel(True,True)
        self.add(c)
        self.at('so losing',lead=0)
        x=knockout(c[3]); self.add(x)
        silent=cool_panel(lost=True)
        self.play(Transform(c[5],silent[5]),Transform(c[6],silent[6]),run_time=.35)
        self.at('cost warmth')
        wl=T('warmth lost · mouse forepaw task',28,GONE).move_to([0,-3.15,0])
        self.play(FadeIn(wl),run_time=.3)
        self.at('Here',lead=0)
        bs,a,out=split_heat()
        self.play(Transform(c,compact),FadeOut(x),Transform(wl,warmth_lost()),
                  FadeIn(T('Heat withdrawal',30,STIM).move_to([3.5,3.22,0])),
                  FadeIn(bs),FadeIn(out),Create(a),run_time=.5)
        self.at('can each carry',lead=0)
        self.finish()


class S17Idea3(SpokenScene):
    def construct(self):
        c=cool_panel(True,True);bs,a,out=split_heat()
        self.add(c,warmth_lost(),T('Heat withdrawal',30,STIM).move_to([3.5,3.22,0]),bs,a,out)
        self.at('Here',lead=0)
        self.at('losing',lead=0)
        self.play(Create(knockout(bs[0])),a[0].animate.set_opacity(.08),run_time=.3)
        self.at('did not abolish',lead=0)
        self.play(FadeIn(centered('burn survives\nresponse retained',27,REPORT).move_to([3.5,-3,0])),run_time=.3)
        self.finish()


class S18Take(SpokenScene):
    def construct(self):
        self.at('In mice',lead=0)
        self.add(heading('Mice · acute heat withdrawal'))
        top=VGroup(*[block(n,[x,1.55,0],width=2.05,height=1.6,size=27) for n,x in zip(NAMES,[-4.65,-1.9,.85])])
        bottom=top.copy().shift(DOWN*3.65)
        yes=block('response\nretained',[4.55,1.55,0],REPORT,width=2.8,height=1.8,lit=True,size=28)
        no=block('withdrawal\nabsent',[4.55,-2.1,0],width=2.8,height=1.8,size=28)
        arrows=VGroup(*[arr([b.get_x(),.62,0],[b.get_x(),.2,0]) for b in top])
        def bus(removed):
            active=[b.get_x() for i,b in enumerate(top) if i != removed]
            return VGroup(Line([min(active),.2,0],[2.65,.2,0],color=STIM,stroke_width=4),
                          Line([2.65,.2,0],[2.65,1.55,0],color=STIM,stroke_width=4),
                          arr([2.65,1.55,0],[3.02,1.55,0]))
        route=bus(0)
        xs=[knockout(b) for b in top]
        lower=VGroup(bottom,no,*[knockout(b) for b in bottom],
                     T('all three removed',26).move_to([0,-.85,0]),
                     T('reported assays',28).move_to([0,-3.42,0]))
        self.add(T('any one removed',26).move_to([0,2.72,0]),top,yes,route,arrows,xs[0])
        arrows[0].set_opacity(0)
        self.at('acute heat withdrawal')
        self.at('survives the loss')
        self.at('any one of',lead=0)
        for i in [1,2]:
            self.remove(xs[i-1]); self.add(xs[i])
            arrows[i-1].set_opacity(1); arrows[i].set_opacity(0)
            self.remove(route); route=bus(i); self.add(route)
            self.wait(.5)
        # Bring in the three-loss comparison only after the spoken single-loss claim.
        self.play(FadeIn(lower),run_time=.35)
        self.finish()


class S19End(EndCard):
    LINE='Mice retain acute heat withdrawal\nwithout one channel, not all three.'

    def construct(self):
        line=centered(self.LINE,40,font=TITLE_FONT)
        fit(line,max_w=11.5)
        scope=T('In the reported assays',28).next_to(line,DOWN,buff=.5)
        site=T('biochemistrypedia.com',26,TEAL).next_to(scope,DOWN,buff=.35)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(scope),FadeIn(site),run_time=.3)
        self.finish()
