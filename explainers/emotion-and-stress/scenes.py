"""Emotion and stress: One Signal, Three Routes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the tone (conditioned stimulus)
  GOLD   = the shock (unconditioned stimulus)
  BLUE   = freezing (the response, its bars, and the route once the lesion result names it)
  ORANGE = the pressure rise (the response, its bars, and the route once the lesion result names it)
  TEAL   = amygdala boxes (lateral and central)
  PURPLE = the two route boxes below the central amygdala (until a lesion names what each carries)
  RED    = a lesion (the X)
  GREY   = unpaired control, frames, axes, and every unanswered or unmeasured thing (dashed)
  PINK   = people (patient SM, the panic dots)
  TEXT   = the learned difference and the claims

GREEN = hormone chain and glucocorticoid (extension for this chapter).

All rat numbers are the lesson's invented numbers (worked problem), laid out in the design of the
1988 study; they are not that study's data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def nbox(text, color=BLUE, size=26, pad=0.2, dashed=False, min_w=0.0, min_h=0.0, fill=0.16):
    """A labelled box with an opaque backing. `text` may hold line breaks. Children: back, rect, label."""
    lines = VGroup(*[T(l, size, color if not dashed else GREY) for l in text.split("\n")]).arrange(DOWN, buff=0.07)
    w = max(lines.width + 2 * pad, min_w)
    h = max(lines.height + 2 * pad, min_h)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    if dashed:
        rect = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=GREY,
                                               stroke_width=3), num_dashes=44)
    else:
        rect = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                                fill_color=color, fill_opacity=fill)
    lines.move_to(back)
    return VGroup(back, rect, lines)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=4):
    """dashed arrow: the link is a question, not a result."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - d * 0.15, dash_length=0.14, color=color, stroke_width=w)
    perp = np.array([-d[1], d[0], 0])
    head = Polygon(b, b - d * 0.26 + perp * 0.13, b - d * 0.26 - perp * 0.13, stroke_width=0,
                   fill_color=color, fill_opacity=1)
    return VGroup(line, head)


def edge(src, dst, side_a="r", side_b="l"):
    """arrow between two nbox groups (box rect is child 1)."""
    pa = {"r": src[1].get_right(), "l": src[1].get_left(), "u": src[1].get_top(), "d": src[1].get_bottom()}[side_a]
    pb = {"r": dst[1].get_right(), "l": dst[1].get_left(), "u": dst[1].get_top(), "d": dst[1].get_bottom()}[side_b]
    return arr(pa, pb)


def sine(cx, cy, w, amp=0.17, cycles=3.5, color=YELLOW, sw=4):
    k = cycles * 2 * np.pi / w
    return ParametricFunction(lambda t: np.array([cx - w / 2 + t, cy + amp * np.sin(k * t), 0]),
                              t_range=[0, w], color=color, stroke_width=sw)


def zig(cx, cy, w, color=GOLD, sw=4):
    return Polygon(*[[cx+x*w,cy+y,0] for x,y in [(.12,.33),(-.38,-.03),(-.03,-.03),(-.15,-.33),(.38,.07),(.06,.07)]],color=color,fill_color=color,fill_opacity=1,stroke_width=1)


def tone_block(cx, cy, w=2.0, h=0.7):
    r = Rectangle(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.18)
    r.move_to([cx, cy, 0])
    return VGroup(r, sine(cx, cy, w * 0.8))


def shock_block(cx, cy, w=0.9, h=0.7):
    r = Rectangle(width=w, height=h, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.3)
    r.move_to([cx, cy, 0])
    return VGroup(r, zig(cx, cy, w * 0.8))


def xmark(box, color=RED, w=9, pad=0.12):
    r = box[1]
    x0, x1, y0, y1 = r.get_left()[0] + pad, r.get_right()[0] - pad, r.get_bottom()[1] + pad, r.get_top()[1] - pad
    return VGroup(Line([x0, y0, 0], [x1, y1, 0], color=color, stroke_width=w),
                  Line([x0, y1, 0], [x1, y0, 0], color=color, stroke_width=w))


def hit(box, on=True, base=PURPLE):
    """animations: tint a box red (lesioned) or back to its colour."""
    if on:
        return box[1].animate.set_stroke(RED).set_fill(RED, 0.4)
    return box[1].animate.set_stroke(base).set_fill(base, 0.16)


# The source film has no hormone kinetics model. The slow plot below is computed
# by linear interpolation of the LESSON'S ORDINAL observations (lag, peak tens
# of minutes later, return toward nonzero baseline), not fitted measurements.
# Its axes deliberately have no invented numerical times or concentrations.
# CHAPTERS.md is left unchanged: TASK.md's final edit restriction permits only
# scenes.py and the requested render/review artifacts.


def label(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


def rat_icon(color=TEXT):
    body = Ellipse(width=2.35, height=1.25, color=color, fill_color=color, fill_opacity=.2)
    head = Ellipse(width=.85, height=.8, color=color, fill_color=BG, fill_opacity=1).move_to([1.1,.2,0])
    ear = Circle(.23, color=color, fill_color=BG, fill_opacity=1).move_to([.92,.65,0])
    eye = Dot([1.27,.32,0], radius=.05, color=color)
    tail = VMobject(color=color, stroke_width=4).set_points_as_corners([[-1.1,0,0],[-1.65,-.2,0],[-1.9,-.05,0],[-2.15,-.35,0]])
    feet = VGroup(Line([-.6,-.45,0],[-.45,-.8,0],color=color), Line([.6,-.45,0],[.8,-.8,0],color=color))
    return VGroup(tail,body,head,ear,eye,feet)


def gauge(high=True):
    # A schematic dial, not a graph of an invented pressure measurement.
    face = Circle(1.05, color=ORANGE, fill_color=ORANGE, fill_opacity=.08)
    ticks = VGroup(*[Line(.86*np.array([np.cos(a),np.sin(a),0]),1.01*np.array([np.cos(a),np.sin(a),0]),color=ORANGE) for a in np.linspace(-.2,3.35,9)])
    a = .65 if high else 2.5
    needle = Arrow(ORIGIN,.8*np.array([np.cos(a),np.sin(a),0]),buff=0,color=ORANGE,stroke_width=6)
    return VGroup(face,ticks,needle,Dot(color=ORANGE,radius=.07))



def responses(high=True):
    r=rat_icon(BLUE).scale(1.8).move_to([-3.2,0,0])
    g=gauge(high).scale(1.8).move_to([3.3,0,0])
    return VGroup(r,g,label('freezing',-3.2,-2.1,BLUE,34),label('blood pressure',3.3,-2.1,ORANGE,34))


def thought(x=0,y=2):
    return VGroup(Ellipse(width=2.3,height=1.2,color=GREY).move_to([x,y,0]),label('?',x,y,GREY,44),Circle(.12,color=GREY).move_to([x-.6,y-.8,0]))


def clock_face(x,y,r=.6):
    face=Circle(r,color=TEXT).move_to([x,y,0])
    hand=Line([x,y,0],[x,y+r*.8,0],color=TEXT,stroke_width=4)
    return VGroup(face,hand,Dot([x,y,0],radius=.04,color=TEXT))


def running_clock(clock, speed):
    clock[1].add_updater(lambda m,dt:m.rotate(-speed*dt,about_point=clock[0].get_center()))
    return clock


def speed_tag(x,y,slow=False):
    cl=clock_face(x-.5,y,.18)
    return VGroup(cl,label('slow' if slow else 'fast',x+.15,y,GREEN if slow else TEXT,26))


def route_map(n=3,cue=True,tags=False):
    tone=VGroup(tone_block(-5.05,2.65,1.5,.55),label('tone',-5.05,3.15,YELLOW,26))
    la=nbox('lateral\namygdala\n(input)',TEAL,26,min_w=2.6,min_h=1.25).move_to([-5.05,1.05,0])
    c=nbox('central\namygdala\n(output)',TEAL,26,min_w=2.6,min_h=1.25).move_to([-5.05,-.95,0])
    inp=VGroup(tone,la,arr(tone[0].get_bottom(),la.get_top(),YELLOW),arr(la.get_bottom(),c.get_top(),TEAL),c)
    names=['caudal periaqueductal\ngray (PAG), midbrain','lateral\nhypothalamus','hypothalamus\npituitary → adrenal']
    cols=[BLUE,ORANGE,GREEN]; ys=[2,0,-2]
    targets=[nbox(t,col,26,min_w=3.5,min_h=1.15).move_to([-.15,y,0]) for t,col,y in zip(names,cols,ys)]
    r=VGroup(rat_icon(BLUE).scale(.68).move_to([4.65,2.15,0]),label('freezing',4.65,1.35,BLUE,26))
    g=VGroup(gauge().scale(.62).move_to([4.65,.15,0]),label('pressure rise',4.65,-.72,ORANGE,26))
    h=nbox('hormone',GREEN,28,min_w=2.5,min_h=1.15).move_to([4.65,-2,0])
    outs=[r,g,h]; links=VGroup(); nodes=VGroup()
    for i in range(n):
        start=c.get_right()+UP*(.35-i*.35)
        a=darr(start,targets[i].get_left(),cols[i]) if i==2 else arr(start,targets[i].get_left(),cols[i])
        link=VGroup(a,arr(targets[i].get_right(),outs[i].get_left(),cols[i]))
        links.add(link); nodes.add(targets[i],outs[i])
    m=VGroup(links,inp,nodes)
    if tags:
        m.add(*[speed_tag(2.8,ys[i]+.55,i==2) for i in range(n)])
    return m,c,targets,outs,links


def brain_view():
    brain=Ellipse(width=10.2,height=6.25,color=GREY,fill_color=GREY,fill_opacity=.09).move_to([.8,0,0])
    ear=Circle(.42,color=YELLOW).move_to([-5.6,.6,0])
    th=Dot([-1.7,.7,0],radius=.23,color=GREY)
    am=Ellipse(width=1.8,height=1,color=TEAL,fill_color=TEAL,fill_opacity=.6).rotate(.35).move_to([1.55,-.85,0])
    labs=VGroup(label('brain • schematic',.8,2.5,GREY,30),label('ear',-5.6,-.3,YELLOW,28),label('thalamus',-1.7,1.5,GREY,30),label('amygdala',2,-1.9,TEAL,34))
    path=VGroup(arr(ear.get_right(),th.get_left(),YELLOW),arr(th.get_center()+RIGHT*.25,am.get_left(),YELLOW))
    return VGroup(brain,ear,th,am,labs,path)


def timeline(y,paired=True):
    xs=(-4.65,-.55,3.55)
    tones=VGroup(*[tone_block(x,y,1.35,.85) for x in xs])
    shocks=VGroup(*[shock_block(x+(1.1 if paired else 2.15),y,.5,.85) for x in xs])
    axis=Arrow([-6.1,y-.65,0],[6.5,y-.65,0],buff=0,color=GREY)
    name=label('paired' if paired else 'unpaired control',0,y+1.2,BLUE if paired else GREY,32)
    legends=VGroup(label('tone',xs[0],y+.7,YELLOW,26),label('shock',xs[0]+(1.1 if paired else 2.15),y-.97,GOLD,26))
    return VGroup(tones,shocks,axis,name,legends)


def lesion_badge(box):
    # Reserve an opaque lower strip INSIDE the damaged node for X + lesion.
    # The tissue name remains above it; no mark is placed on a connection.
    r=box[1]
    y=r.get_bottom()[1]+.22
    x=r.get_center()[0]-.64
    backing=Rectangle(width=1.75,height=.4,stroke_width=0,
                      fill_color=BG,fill_opacity=1).move_to([x+.5,y,0])
    cross=VGroup(Line([x-.12,y-.12,0],[x+.12,y+.12,0],color=RED,stroke_width=5),
                 Line([x-.12,y+.12,0],[x+.12,y-.12,0],color=RED,stroke_width=5))
    return VGroup(backing,cross,label('lesion',x+.62,y,RED,26))


def lesion_picture():
    m,c,ts,outs,links=route_map(2)
    # Add a dedicated lesion row below each tissue label, inside its border.
    for node in [c,*ts[:2]]:
        for shape in node[:2]:
            shape.stretch_to_fit_height(shape.height+.55).shift(DOWN*.275)
    return m,c,ts,outs,links


def scope_map():
    m,c,ts,outs,links=route_map(3)
    # Centre the map and its frame; reserve a narrow outside strip for the question.
    m[1].shift(RIGHT*1.2)
    for o in outs: o.shift(LEFT*1.05)
    for o in outs[:2]: o[0].scale(.8)
    new_links=VGroup()
    for i,col in enumerate([BLUE,ORANGE,GREEN]):
        start=c.get_right()+UP*(.35-i*.35)
        a=darr(start,ts[i].get_left(),col) if i==2 else arr(start,ts[i].get_left(),col)
        new_links.add(VGroup(a,arr(ts[i].get_right(),outs[i].get_left(),col)))
    m.remove(links);m.add_to_back(new_links)
    m.add(*[speed_tag(2.25,y+.85,i==2) for i,y in enumerate([2,0,-2])])
    frame=RoundedRectangle(width=10.6,height=6.75,corner_radius=.18,color=GREY).move_to([0,.05,0])
    return m,frame,label('learned • outside cue • rats',0,-3.55,GREY,28)


class S00Title(TitleCard):
    LESSON='Emotion and Stress'
    TITLE='One Signal, Three Routes'


class S01Question(SpokenScene):
    def construct(self):
        chamber=RoundedRectangle(width=11.9,height=6.4,corner_radius=.2,color=GREY)
        r=rat_icon().scale(1.7).move_to([0,-1,0])
        speaker=VGroup(Rectangle(width=.4,height=.8,color=YELLOW),Polygon([.2,.4,0],[.8,.8,0],[.8,-.8,0],[.2,-.4,0],color=YELLOW)).move_to([-4.3,1.5,0])
        wave=sine(-1.5,1.5,3,.25)
        self.add(chamber,r)
        self.at('hears a tone'); self.play(FadeIn(speaker),Create(wave),FadeIn(label('tone',-1.5,2.3,YELLOW,30)),run_time=.4)
        self.at('mild shock'); self.play(FadeIn(shock_block(3.5,1.5,.9,1.2)),FadeIn(label('shock',3.5,2.5,GOLD,30)),run_time=.35)
        self.at('What does'); self.play(Indicate(r[2],color=TEAL),run_time=.5)
        self.finish()


class S02TwoThings(SpokenScene):
    def construct(self):
        v=responses(False); v[2].shift(DOWN*.55); self.add(v[0],v[1])
        self.at('Two things')
        feet=v[0][5]; tail=v[0][0]
        feet.add_updater(lambda m,dt:m.rotate(.11*np.sin(self.elapsed()*16),about_point=m.get_center()))
        tail.add_updater(lambda m,dt:m.rotate(.04*np.sin(self.elapsed()*14),about_point=m.get_right()))
        self.play(v[0].animate.shift(RIGHT*.6),run_time=1.2,rate_func=linear)
        self.at('stops moving'); feet.clear_updaters(); tail.clear_updaters()
        self.play(FadeIn(v[2]),FadeIn(label('still',-3.2,1.9,BLUE,28)),run_time=.25)
        self.at('blood pressure rises'); self.play(Transform(v[1],gauge(True).scale(1.8).move_to(v[1])),FadeIn(v[3]),run_time=.65)
        self.finish()


class S03NotFeeling(SpokenScene):
    def construct(self):
        v=responses(); b=thought(0,2.3); self.add(v)
        self.at('Neither one'); self.play(FadeIn(b),run_time=.3)
        self.at('feeling of fear'); self.play(Create(Line([-1,1.8,0],[1,2.8,0],color=RED,stroke_width=6)),run_time=.3)
        scored=nbox('scored',BLUE,28).move_to([-3.2,-3,0])
        readout=VGroup(nbox('readout',ORANGE,28),Line([-.6,0,0],[.6,0,0],color=ORANGE)).arrange(RIGHT,buff=.2).move_to([3.3,-3,0])
        self.at('both can be measured'); self.play(FadeIn(scored),FadeIn(readout),run_time=.5)
        self.at('trace them'); self.play(Indicate(v[0],color=BLUE),Indicate(v[1],color=ORANGE),run_time=.6)
        self.finish()


class S04Paired(SpokenScene):
    def construct(self):
        q=label('Is the response learned?',0,3.1,size=38); row=timeline(.3)
        # Rat silhouettes ground the group before the stimuli appear.
        rats=VGroup(*[rat_icon(BLUE).scale(.5).move_to([x,-2.25,0]) for x in (-4.3,0,4.3)])
        self.add(q,row[2],rats)
        self.at('one group'); self.play(FadeIn(row[3]),run_time=.3)
        self.at('hears tones'); self.play(FadeIn(row[0]),FadeIn(row[4][0]),run_time=.4)
        self.at('end in a shock'); self.play(FadeIn(row[1]),FadeIn(row[4][1]),run_time=.4)
        self.finish()


class S05Unpaired(SpokenScene):
    def construct(self):
        top=timeline(1.65); bottom=timeline(-1.7,False); self.add(top,bottom[2],bottom[3])
        self.at('same tones'); self.play(FadeIn(bottom[0]),FadeIn(bottom[4][0]),run_time=.3)
        self.at('same shocks'); self.play(FadeIn(bottom[1]),FadeIn(bottom[4][1]),run_time=.3)
        gap=DoubleArrow([-3.95,-1.7,0],[-2.8,-1.7,0],buff=.05,color=TEXT)
        self.at('kept apart'); self.play(GrowArrow(gap),FadeIn(label('far apart',-3.375,-1.0,size=28)),run_time=.4)
        self.finish()


class S06Difference(SpokenScene):
    def construct(self):
        # Values are the lesson's invented worked example, not 1988 measurements.
        base=-2.65; scale=.08
        axes=VGroup(Line([-4.8,base,0],[-4.8,2.6,0],color=GREY),Line([-4.8,base,0],[5.4,base,0],color=GREY))
        yl=label('freezing to tone\n(no numbers)',-5.65,.1,BLUE,26).rotate(PI/2)
        bars=VGroup(*[Rectangle(width=1.9,height=v*scale,color=col,fill_color=col,fill_opacity=.55).move_to([x,base+v*scale/2,0]) for x,v,col in [(-2.5,60,BLUE),(1.5,8,GREY)]])
        self.add(axes,yl,label('Tone alone',0,3.15,BLUE,34),label('paired',-2.5,-3.15,BLUE),label('unpaired',1.5,-3.15,GREY))
        self.at('the paired rats'); self.play(GrowFromEdge(bars[0],DOWN),GrowFromEdge(bars[1],DOWN),run_time=.6)
        bottom=base+8*scale; top=base+60*scale
        gap=Rectangle(width=1.9,height=top-bottom,color=GOLD,fill_color=GOLD,fill_opacity=.25).move_to([1.5,(bottom+top)/2,0])
        hatch=VGroup(*[Line([.6,y,0],[2.4,y+.3,0],color=GOLD,stroke_width=2) for y in np.arange(bottom+.05,top-.3,.35)])
        bracket=Brace(Line([2.8,bottom,0],[2.8,top,0]),RIGHT,color=GOLD)
        self.at('That difference'); self.play(FadeIn(gap),Create(hatch),GrowFromCenter(bracket),run_time=.4)
        self.at('what was learned'); self.play(FadeIn(label('learned',4.3,0,GOLD,32)),run_time=.3)
        self.finish()


class S07Amygdala(SpokenScene):
    def construct(self):
        b=brain_view(); self.add(b[0],b[1],b[4][0],b[4][1])
        self.at('Where is it learned'); self.play(FadeIn(b[2]),FadeIn(b[3]),FadeIn(b[4][2]),FadeIn(b[4][3]),run_time=.35)
        self.at('The tone travels'); self.play(Create(b[5]),run_time=.35)
        wave=sine(-5.6,.6,.65,.15,2)
        path=VMobject().set_points_as_corners([b[1].get_center(),b[2].get_center(),b[3].get_center()])
        self.play(MoveAlongPath(wave,path),run_time=.65)
        self.at('the amygdala'); self.play(FadeOut(wave),Indicate(b[3],color=TEAL),run_time=.4)
        self.finish()


class S08TwoStages(SpokenScene):
    def construct(self):
        b=brain_view(); self.add(b)
        a=nbox('lateral amygdala',TEAL,32,min_w=5,min_h=3.6).move_to([-3.4,0,0])
        c=nbox('central amygdala',TEAL,32,min_w=5,min_h=3.6).move_to([3.4,0,0])
        # Transform the glowing tissue into the empty input box, then fade in
        # clean text (never interpolate glyph outlines from the tissue shape).
        self.at('The lateral')
        self.play(FadeOut(VGroup(b[0],b[1],b[2],b[4],b[5])),
                  ReplacementTransform(b[3],VGroup(a[0],a[1])),run_time=.5)
        self.play(FadeIn(a[2]),run_time=.25)
        self.at('input stage'); self.play(FadeIn(label('input',-3.4,-.9,TEAL,32)),run_time=.3)
        self.at('The central')
        self.play(FadeIn(c[:2]),GrowArrow(arr(a.get_right(),c.get_left(),TEAL)),run_time=.3)
        self.at('sends the signal out')
        self.play(FadeIn(c[2]),FadeIn(label('output',3.4,-.9,TEAL,32)),run_time=.3)
        self.finish()


class S09RoutePag(SpokenScene):
    def construct(self):
        m,c,ts,outs,links=route_map(3); self.add(m[1])
        stubs=VGroup(*[links[i][0].copy().set_opacity(.45) for i in range(3)])
        self.add(stubs)
        self.at('leave it'); self.play(Indicate(stubs,color=TEXT),run_time=.35)
        self.at('One runs'); self.play(FadeIn(ts[0]),run_time=.4)
        self.at('periaqueductal gray'); self.play(Indicate(ts[0][1],color=BLUE),run_time=.4)
        self.at('It drives freezing'); self.play(GrowArrow(links[0][1]),FadeIn(outs[0]),run_time=.5)
        self.finish()


class S10RouteLh(SpokenScene):
    def construct(self):
        prior,*_=route_map(1); self.add(prior)
        m,c,ts,outs,links=route_map(2)
        self.at('A second runs'); self.play(Create(links[1][0]),FadeIn(ts[1]),run_time=.4)
        self.at('rise in blood pressure'); self.play(GrowArrow(links[1][1]),FadeIn(outs[1]),run_time=.5)
        self.finish()


class S11RouteHpa(SpokenScene):
    def construct(self):
        prior,c,*_=route_map(2); self.add(prior)
        chain=VGroup(*[nbox(t,GREEN,26,min_w=w,min_h=1.05).move_to([x,-1.55,0]) for t,x,w in [('hypothalamus\n(PVN)',-1.95,3),('pituitary',1.3,2.6),('adrenal',4.65,2.4)]])
        self.at('A third'); self.play(Create(darr(c.get_bottom(),chain[0].get_left(),GREEN)),run_time=.3)
        self.at('mostly indirect'); self.play(FadeIn(chain[0]),run_time=.35)
        self.at('pituitary'); self.play(GrowArrow(arr(chain[0].get_right(),chain[1].get_left(),GREEN)),FadeIn(chain[1]),run_time=.3)
        self.at('adrenal'); self.play(GrowArrow(arr(chain[1].get_right(),chain[2].get_left(),GREEN)),FadeIn(chain[2]),run_time=.3)
        # A continuous curved teardrop, with its hormone name on the body.
        drop=VMobject(stroke_color=GREEN,stroke_width=3,fill_color=GREEN,fill_opacity=.18)
        drop.start_new_path(np.array([3.1,-2.15,0]))
        drop.add_cubic_bezier_curve_to([2.9,-2.7,0],[1.25,-3.5,0],[3.1,-3.5,0])
        drop.add_cubic_bezier_curve_to([4.95,-3.5,0],[3.3,-2.7,0],[3.1,-2.15,0])
        hormone=VGroup(drop,label('cortisol',3.1,-3.13,GREEN,28),
                       label('corticosterone in rats',3.1,-3.65,GREEN,26))
        self.at('In people'); self.play(GrowArrow(arr(chain[2].get_bottom(),[3.65,-2.75,0],GREEN)),run_time=.3)
        self.at('is cortisol'); self.play(FadeIn(hormone),run_time=.25)
        self.finish()


class S12FastClock(SpokenScene):
    def construct(self):
        m,c,ts,outs,links=route_map(2); self.add(m)
        originals=[o.copy() for o in outs[:2]]
        link_originals=[l.copy() for l in links]
        for o in outs[:2]: o.set_opacity(.2)
        for l in links: l.set_opacity(.2)
        bar=Rectangle(width=8.5,height=.55,color=YELLOW).move_to([1.5,-2.25,0])
        fill=Rectangle(width=.02,height=.5,stroke_width=0,fill_color=YELLOW,fill_opacity=.4).move_to([-2.73,-2.25,0])
        start=self.elapsed()
        fill.add_updater(lambda z: z.stretch_to_fit_width(max(.02,min(8.45,(self.elapsed()-start)*1.3))).align_to(bar,LEFT).shift(RIGHT*.025))
        cl=running_clock(clock_face(2.55,1.05,.4),TAU*1.5)
        self.at('Two of these'); self.add(bar,fill,label('tone playing',1.5,-3,YELLOW,30),cl,label('seconds',3.9,1.05,size=28))
        self.at('are fast'); self.play(FadeIn(speed_tag(-3,1.65)),FadeIn(speed_tag(-2.85,-1.55)),run_time=.3)
        self.at('Freezing and'); self.play(*[Transform(o,orig) for o,orig in zip(outs[:2],originals)],*[Transform(l,orig) for l,orig in zip(links,link_originals)],run_time=.4)
        marks=VGroup(*[Line([x,-1.9,0],[x,-2.6,0],color=col,stroke_width=5) for x,col in [(.4,BLUE),(.8,ORANGE)]])
        self.play(Create(marks),run_time=.2)
        self.at('while the tone'); self.play(Indicate(bar,color=YELLOW),run_time=.4)
        self.finish()


class S13SlowClock(SpokenScene):
    def construct(self):
        # Qualitative ordinal model: lag, peak, clearance toward continuing secretion.
        # Dimensionless anchors encode only the lesson's ordering, never fitted data.
        ax=np.array([0,1,2,3,4,6,8,10],float); ay=np.array([.5,.5,.55,1.7,3.2,2,.8,.55],float)
        f=lambda t: np.array([-3.8+t*.94,-2.55+np.interp(t,ax,ay)*1.28,0])
        adrenal=nbox('3 • adrenal hormone',GREEN,32,min_w=3.6).move_to([-4.45,2.9,0])
        cl=running_clock(clock_face(-1.7,3,.35),.28)
        self.add(adrenal,cl,label('minutes',-.4,3,size=26),label('qualitative timing',3.9,3.15,TEXT,28))
        axes=VGroup(Line([-3.8,-2.55,0],[5.9,-2.55,0],color=GREY),Line([-3.8,-2.55,0],[-3.8,2,0],color=GREY))
        self.at('is slow'); self.play(Create(axes),FadeIn(label('hormone level',-5.35,-.25,GREEN,26).rotate(PI/2)),FadeIn(label('time after stress',1.5,-3.35,GREY,28)),run_time=.4)
        self.at('The adrenal must'); self.play(Create(DashedLine(f(0),f(10)*[1,0,1]+[0,f(0)[1],0],color=GREY)),Create(Line([-3.8,-2.4,0],[-3.8,-2.75,0],color=TEXT,stroke_width=4)),FadeIn(label('stress begins',-3.8,-2.99,size=26)),run_time=.4)
        rise=ParametricFunction(f,t_range=[0,4,.02],color=GREEN,stroke_width=6)
        fall=ParametricFunction(f,t_range=[4,10,.02],color=GREEN,stroke_width=6)
        self.at('so levels peak'); self.play(Create(rise),run_time=.65)
        bracket=VGroup(Line([-3.8,1.95,0],[-.04,1.95,0],color=GREEN),Line([-3.8,1.8,0],[-3.8,2.1,0],color=GREEN),Line([-.04,1.8,0],[-.04,2.1,0],color=GREEN))
        self.at('tens of minutes later'); self.play(Create(bracket),FadeIn(label('tens of minutes',-1.9,2.3,GREEN,26)),run_time=.4)
        self.at('Feedback then'); self.play(Create(fall),FadeIn(label('feedback limits release',3.1,1.5,GREEN,26)),GrowArrow(arr([3.1,1.15,0],f(6.5),GREEN)),run_time=.65)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        m,c,ts,outs,links=route_map(3,tags=True); self.add(m)
        self.at('here is the rule'); self.play(FadeIn(label('One node, separate routes',1.1,3.35,size=32)),run_time=.3)
        self.at('cue reaches'); self.play(Indicate(m[1][1],color=TEAL),Indicate(c,color=TEAL),run_time=.5)
        self.at('separate routes'); self.play(Indicate(links,color=TEXT),run_time=.4)
        self.finish()


class S15Cut(SpokenScene):
    def construct(self):
        m,c,ts,outs,links=lesion_picture(); self.add(m)
        originals=[o.copy() for o in outs[:2]]
        self.add(label('Simplified model • hormone branch not measured here',0,-3.35,GREY,26))
        badge=lesion_badge(ts[0]); cap=label('freezing lost, pressure kept',0,-2.5,BLUE,30)
        self.at('damaging neurons'); self.play(FadeIn(badge),run_time=.15)
        self.play(outs[0].animate.set_opacity(.18),FadeIn(cap),run_time=.15)
        self.wait(2.05)
        self.at('impaired mainly'); self.play(FadeOut(badge),FadeOut(cap),Transform(outs[0],originals[0]),run_time=.15)
        badge=lesion_badge(ts[1]); cap=label('pressure lost, freezing kept',0,-2.5,ORANGE,30)
        self.play(FadeIn(badge),run_time=.15)
        self.play(outs[1].animate.set_opacity(.18),FadeIn(cap),run_time=.15)
        self.wait(2.05)
        self.at('Damage to'); self.play(FadeOut(badge),FadeOut(cap),Transform(outs[1],originals[1]),run_time=.15)
        badge=lesion_badge(c); cap=label('both learned responses impaired',0,-2.5,RED,30)
        self.play(FadeIn(badge),run_time=.15)
        self.play(outs[0].animate.set_opacity(.18),outs[1].animate.set_opacity(.18),FadeIn(cap),run_time=.15)
        self.finish()


class S16Scope(SpokenScene):
    def construct(self):
        # Continue the shared-node result across the cut for one full second.
        old,c,ts,outs,links=lesion_picture()
        outs[0].set_opacity(.18); outs[1].set_opacity(.18)
        prev=VGroup(old,lesion_badge(c),label('both learned responses impaired',0,-2.5,RED,30),label('Simplified model • hormone branch not measured here',0,-3.35,GREY,26))
        self.add(prev); self.at('This map'); self.wait(1)
        m,f,l=scope_map(); self.play(FadeOut(prev),FadeIn(m),Create(f),run_time=.45)
        self.at('learned responses'); self.play(FadeIn(l),run_time=.3)
        self.finish()


class S17Limits(SpokenScene):
    def construct(self):
        m,f,l=scope_map(); self.add(m,f,l)
        self.at('does not say')
        bubble=thought(6.1,.15)
        bubble[0].stretch_to_fit_width(1.05)
        self.play(FadeIn(bubble),Create(DashedLine([5.4,-1.2,0],[5.4,1.4,0],color=GREY)),run_time=.4)
        self.at('Later chapters'); self.play(Indicate(bubble[1],color=TEXT,scale_factor=1.15),run_time=.7)
        self.at('where the map stops'); self.play(Indicate(f,color=TEXT,scale_factor=1),Indicate(bubble[0],color=TEXT,scale_factor=1),run_time=.6)
        self.finish()


class S18Takeaway(SpokenScene):
    def construct(self):
        m,c,ts,outs,links=route_map(3,tags=True); self.add(m)
        self.at('The amygdala'); self.play(FadeIn(label('The amygdala is needed to learn the threat',.65,3.45,TEAL,30)),Indicate(VGroup(m[1][1],c),color=TEAL),run_time=.6)
        self.at('Separate routes'); self.play(FadeIn(label('Separate routes respond: two fast, one slow',0,-3.35,size=30)),Indicate(links,color=TEXT),run_time=.6)
        self.at('two fast'); self.play(Indicate(VGroup(links[0],links[1]),color=TEXT),run_time=.4)
        self.at('one slow'); self.play(Indicate(links[2],color=GREEN),run_time=.35)
        self.finish()


class S19End(EndCard):
    LINE='The amygdala is needed to learn threats; routes respond separately.'
