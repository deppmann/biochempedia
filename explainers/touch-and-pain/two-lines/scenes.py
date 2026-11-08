"""Two Lines, Two Crossings: schematic anatomy, posterior view.
COLOR MAP: BLUE=fine touch/vibration/position; RED=pain/temperature;
GOLD=lesion; YELLOW=signal/crossing; GREY=anatomy/weakness.
Routes are schematic polylines, not measured anatomical or quantitative traces.
"""
import numpy as np
from bp_style import *

TOUCH, PAIN, CUT, SIG, STRUCT = BLUE, RED, GOLD, YELLOW, GREY

# Keep the shared word-level timing, without creating an extra sync.log artifact.
class Timed(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def label(s, x=0, y=3.15, color=TEXT, size=28):
    return T(s, size=size, color=color, line_spacing=.85).move_to([x,y,0])


def path(pts, color=TOUCH, width=6):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [np.array([x,y,0.]) for x,y in pts])


class Track(VGroup):
    """No background stroke: anatomy stays visible during route drawing."""
    def __init__(self, pts, color, tip=False):
        super().__init__()
        self.pts=pts
        self.line=path(pts,color)
        self.add(self.line)
        if tip:
            d=np.subtract(pts[-1],pts[-2]); a=np.arctan2(d[1],d[0])
            self.add(Triangle(stroke_width=0,fill_color=color,fill_opacity=1)
                     .scale(.10).rotate(a-PI/2).move_to([*pts[-1],0]))


def dashed(pts, color=PAIN):
    return DashedVMobject(path(pts,color,5),num_dashes=24,dashed_ratio=.6)


def leader(text, x, y, endpoint, color=STRUCT, size=26, below=False):
    t=label(text,x,y,color,size)
    side=RIGHT if endpoint[0]>x else LEFT
    start=t.get_bottom()+DOWN*.12 if below else t.get_edge_center(side)+side*.12
    return VGroup(Line(start,[*endpoint,0],color=color,stroke_width=1.6),t)


def mark(x,y,color=CUT):
    return VGroup(Line([x-.13,y-.13,0],[x+.13,y+.13,0],color=color,stroke_width=5),
                  Line([x-.13,y+.13,0],[x+.13,y-.13,0],color=color,stroke_width=5))


def ring(x,y):
    return Circle(radius=.22,color=SIG,stroke_width=4).move_to([x,y,0])


def travel(scene,tr,rt=.6):
    dot=Dot([*tr.pts[0],0],radius=.09,color=SIG)
    scene.add(dot)
    scene.play(MoveAlongPath(dot,path(tr.pts)),run_time=rt,rate_func=linear)
    scene.remove(dot)


def body(x=3.6):
    pts=[(-.4,2.1),(-.9,1.8),(-1.25,.4),(-.95,.25),(-.65,1.1),(-.65,-.55),(-.8,-2.8),(-.25,-2.8),(0,-.9),(.25,-2.8),(.8,-2.8),(.65,-.55),(.65,1.1),(.95,.25),(1.25,.4),(.9,1.8),(.4,2.1)]
    return VGroup(Polygon(*[[x+a,b,0] for a,b in pts],color=STRUCT,fill_color=STRUCT,fill_opacity=.09,stroke_width=3),
                  Circle(radius=.43,color=STRUCT).move_to([x,2.65,0]),
                  label('L',x-1.15,2.65,STRUCT,26),label('R',x+1.15,2.65,STRUCT,26),
                  label('back view · schematic',x,-3.25,STRUCT,26))


BODY_LEVELS={9:.75,10:.15,11:-.45,12:-1.05}


def shade(x,side,color,top=.15):
    s=side
    pts=[(.04*s,top),(.65*s,top),(.65*s,min(-.55,top)),(.78*s,-2.75),(.28*s,-2.75),(.04*s,-.9)]
    return Polygon(*[[x+a,b,0] for a,b in pts],stroke_width=0,fill_color=color,fill_opacity=.55)


def body_levels(x=3.6):
    g=VGroup(DashedLine([x-1.05,.15,0],[x+.95,.15,0],color=CUT,stroke_width=2))
    for n,y in BODY_LEVELS.items():
        g.add(Line([x+1.0,y,0],[x+1.15,y,0],color=CUT if n==10 else STRUCT),
              label('T'+str(n),x+1.6,y,CUT if n==10 else STRUCT,26))
    return g


def lesion_body(blue=True,red=True,reverse=False,top=-.75,x=3.6):
    g=VGroup(body(x))
    if blue:g.add(shade(x,-1 if reverse else 1,TOUCH,.15))
    if red:g.add(shade(x,1 if reverse else -1,PAIN,top))
    g.add(body_levels(x))
    return g


def slice_base():
    # Slender dorsal horns above; broader, rounded ventral horns below.
    outer=Ellipse(width=6.6,height=5.6,color=STRUCT,fill_color=STRUCT,fill_opacity=.1).move_to([-1,-.1,0])
    pts=[(-.12,.3),(-.68,1.25),(-1.08,2.0),(-1.19,1.96),(-1.02,1.12),(-.48,.05),(-1.25,-.45),(-1.7,-.95),(-1.7,-1.55),(-1.25,-1.85),(-.72,-1.7),(-.38,-.9),(0,-.5),(.38,-.9),(.72,-1.7),(1.25,-1.85),(1.7,-1.55),(1.7,-.95),(1.25,-.45),(.48,.05),(1.02,1.12),(1.19,1.96),(1.08,2.0),(.68,1.25),(.12,.3)]
    horn=Polygon(*[[x-1,y-.1,0] for x,y in pts],stroke_color=STRUCT,fill_color=STRUCT,fill_opacity=.55)
    return VGroup(outer,horn,label('dorsal · toward the back',-1,3.25,STRUCT,28),
                  label('L',-4.7,-.1,STRUCT,26),label('R',2.7,-.1,STRUCT,26),
                  leader('dorsal column',-.8,2.2,(-.6,1.75),TOUCH,26,below=True))


def root_lines():
    return VGroup(Track([(5,.65),(3,.65),(.6,1.4),(-.4,1.65)],TOUCH),
                  Track([(5,.05),(3,.05),(.6,.95),(.0,.8)],PAIN))


def tall_base():
    cord=Rectangle(width=3.8,height=5.0,color=STRUCT,fill_color=STRUCT,fill_opacity=.08).move_to([0,-.85,0])
    med=RoundedRectangle(width=4.0,height=.8,corner_radius=.12,color=STRUCT).move_to([0,2.15,0])
    return VGroup(cord,med,DashedLine([0,-3.35,0],[0,2.55,0],color=STRUCT,stroke_width=1.4),
                  label('medulla',0,2.39,STRUCT,26),label('L',-1.3,-2.8,STRUCT,26),
                  label('R',1.3,-2.8,STRUCT,26),label('spinal cord · dorsal view',0,-3.65,STRUCT,26))


def thalamus():
    # Text sits above the terminal, inside the same outlined compartment.
    return VGroup(RoundedRectangle(width=2.05,height=.7,corner_radius=.12,color=STRUCT).move_to([-.9,3.18,0]),
                  label('thalamus',-.9,3.31,STRUCT,26))


def blue_parts():
    a=Track([(2.4,-2.35),(.85,-2.35),(.85,2.05)],TOUCH)
    syn=Dot([.85,2.05,0],color=TOUCH,radius=.1)
    b=Track([(.75,2.05),(.5,2.05),(-.15,1.9),(-.9,2.05),(-.9,3.0)],TOUCH)
    terminal=Dot([-.9,3.0,0],color=TOUCH,radius=.1)
    c=dashed([(-1.08,3.0),(-2.3,3.0),(-2.3,3.62),(1.98,3.62)],TOUCH)
    cortex=chip('cortex',TOUCH,26).move_to([2.7,3.55,0])
    return a,syn,b,thalamus(),terminal,c,cortex


def blue_labels():
    return VGroup(leader('gracile / cuneate\nnucleus',4.35,1.35,(.85,2.05),TOUCH),
                  leader('internal arcuate\nfibres',-4.35,.9,(-.15,1.9),TOUCH),
                  leader('medial lemniscus',-4.35,2.55,(-.9,2.7),TOUCH))


def red_parts():
    a=Track([(2.7,-1.9),(1.15,-1.9),(1.15,-1.25),(.65,-1.25)],PAIN)
    syn=Dot([.65,-1.25,0],color=PAIN,radius=.1)
    b=Track([(.55,-1.25),(.55,-1.65),(-1.05,-1.65),(-1.05,3.0)],PAIN)
    return a,syn,b,Dot([-1.05,3.0,0],color=PAIN,radius=.1)


def red_labels():
    return VGroup(leader('contralateral\nopposite side',-4.25,.5,(-1.12,.5),PAIN),
                  leader('anterolateral cord',-4.15,-.4,(-1.12,-.4),PAIN),
                  leader('anterior white\ncommissure',-4.25,-1.9,(-.25,-1.65),PAIN))


LEVEL_Y={9:2.15,10:.75,11:-.65,12:-2.05}

def levels(x=-1.8):
    g=VGroup(Rectangle(width=3.4,height=6.25,color=STRUCT,fill_color=STRUCT,fill_opacity=.08).move_to([x,0,0]),
             DashedLine([x,-3.125,0],[x,3.125,0],color=STRUCT,stroke_width=1.5),
             label('L',x-.9,3.45,STRUCT,26),label('R',x+.9,3.45,STRUCT,26),
             label('dorsal view',x,-3.5,STRUCT,26))
    for n,y in LEVEL_Y.items():
        g.add(Line([x-1.7,y,0],[x+1.7,y,0],color=STRUCT,stroke_opacity=.25),label('T'+str(n),x-2.15,y+(.3 if n==11 else 0),STRUCT,26))
    return g


def cut(right=True,x=-1.8,caption=True):
    mid=x+.85 if right else x-.85
    g=VGroup(Rectangle(width=1.7,height=.48,stroke_color=CUT,fill_color=CUT,fill_opacity=.35).move_to([mid,.75,0]))
    if caption:
        g.add(leader('T10 hemisection\n'+('right' if right else 'left')+' half',2.6,2.55,(mid,1.02),CUT,28))
    return g


def question1():
    return VGroup(levels(),cut(),label('Which side loses touch?',2.9,.6,TOUCH,30),
                  label('Which side loses pain?',2.9,-.6,PAIN,30))


def stopped_route(color=TOUCH,x=-1.8,right=True):
    lane=x+((.85 if right else -.85) if color==TOUCH else (.45 if right else -.45))
    if color==TOUCH:
        pts=[(lane,-2.7),(lane,.44)]
    else:
        start=x+(-.85 if right else .85)
        pts=[(start,-2.7),(start,-.65),(start,.75),(lane,.75)]
        return VGroup(Track(pts,color),Dot([start,-.65,0],color=color,radius=.13),mark(lane,.75))
    return VGroup(Track(pts,color),mark(lane,.45))


def options():
    # A visible T11 relay starts the second axon; dashed crossings are alternatives.
    low=VGroup(dashed([(-2.65,.75),(-.65,.75)]),mark(-.65,.75))
    high=dashed([(-2.65,2.15),(-.65,2.15),(-.65,2.85)])
    return low,high


def fibre():
    return Track([(-5.8,-.65),(-2.65,-.65)],PAIN)


def relays():
    return VGroup(Track([(-2.65,-.65),(-2.65,2.15)],PAIN),
                  Dot([-2.65,-.65,0],color=PAIN,radius=.13))


def option_labels():
    return VGroup(leader('T10: lost',2.6,.75,(-.45,.75),PAIN,30),
                  leader('T9: spared ↑',2.6,1.9,(-.65,2.8),PAIN,30))


def option_frame():
    a,b=options()
    return VGroup(levels(),cut(caption=False),fibre(),relays(),a,b,option_labels(),
                  label('illustrative routes',2.4,3.2,STRUCT,28),label('or',2.5,1.33,STRUCT,26),
                  leader('dorsal horn\nrelay',-4.8,1.5,(-2.65,-.65),STRUCT,26))


def question2():
    return VGroup(lesion_body(reverse=True,x=-3.6),
                  label('Right leg: pain lost',2.4,1.8,PAIN,30),
                  label('Left leg: vibration lost',2.4,.7,TOUCH,30),
                  label('below the waist',2.4,-.25,STRUCT,26),
                  label('Which half of the cord is cut?',2,-1.5,size=29))


class S00Title(TitleCard):
    LESSON='Touch and Pain'
    TITLE='Two Lines, Two Crossings'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.4,TEAL,26),label(self.LESSON.upper(),0,.65,STRUCT,28))
        self.play(FadeIn(label(self.TITLE,0,-.35,size=46)),Create(Line([-1.2,-1.2,0],[1.2,-1.2,0],color=CUT)),run_time=.7)
        self.wait(2.3)


class S01Q(Timed):
    def construct(self):
        self.add(body(-3.7))
        # Match the blue/red routes in the following cross-section.
        root=VGroup(Rectangle(width=2.1,height=3.8,color=STRUCT).move_to([-.3,-.4,0]),
                    label('cord',-.3,1.8,STRUCT,28),label('one dorsal root',.3,-2.75,STRUCT,28),
                    Track([(-3.1,-1.7),(-1.6,-1.7),(-1.6,-1.1),(-.5,-1.1)],TOUCH),
                    Track([(-3.1,-2.15),(-1.4,-2.15),(-1.4,-1.5),(-.3,-1.5)],PAIN))
        touch=Circle(radius=.15,color=TOUCH).move_to([-3.1,-1.7,0])
        prick=Star(n=5,outer_radius=.17,inner_radius=.07,color=PAIN,fill_color=PAIN,fill_opacity=.8).move_to([-3.05,-2.15,0])
        self.add(root,touch,prick,leader('touch',-5.25,-1.45,(-3.3,-1.7),TOUCH),leader('prick',-5.25,-2.4,(-3.3,-2.15),PAIN))
        self.at('Touch and pain'); self.play(Indicate(touch),Indicate(prick),run_time=.45)
        self.at('How can'); self.play(FadeIn(label('One cut.',3.7,1.5,size=36)),FadeIn(label('Touch on one side,\npain on the other?',3.7,.1,size=30)),run_time=.4)
        self.finish()


class S02Slice(Timed):
    def construct(self):
        base=slice_base(); lines=root_lines(); self.add(base)
        self.at('Picture a slice'); self.play(Indicate(base[0],color=STRUCT,scale_factor=1),run_time=.4)
        self.at('Touch runs'); self.play(Create(lines[0]),FadeIn(label('touch',4.7,1.5,TOUCH,28)),run_time=.3)
        self.at('pain in red'); self.play(Create(lines[1]),FadeIn(label('pain',4.7,-.7,PAIN,28)),run_time=.3)
        self.finish()


class S03Blue(Timed):
    def construct(self):
        self.add(slice_base(),root_lines())
        self.at('The blue line'); self.play(FadeIn(label('Dorsal column–medial lemniscus',0,-3.3,TOUCH,28)),run_time=.25)
        self.at('fine touch'); self.play(FadeIn(label('fine touch',4.7,2.55,TOUCH,26)),run_time=.2)
        self.at('vibration'); self.play(FadeIn(label('vibration',4.7,2.1,TOUCH,26)),run_time=.2)
        self.at('position sense'); self.play(FadeIn(label('position sense',4.7,1.65,TOUCH,26)),run_time=.2)
        self.finish()


class S04Blue2(Timed):
    def construct(self):
        old=VGroup(slice_base(),root_lines()); self.add(old)
        self.at('Its main branch'); self.play(FadeOut(old),FadeIn(tall_base()),run_time=.35)
        a,s,*_=blue_parts(); self.play(Create(a),run_time=.45)
        self.at('on its own side'); self.play(FadeIn(leader('dorsal column',4,.7,(.9,.7),TOUCH)),FadeIn(leader('ipsilateral\nsame side',4,-.3,(.9,-.3),TOUCH)),run_time=.3)
        self.at('no synapse'); travel(self,a,.55)
        self.at('the medulla'); self.play(FadeIn(s),run_time=.2)
        branch=VGroup(Track([(.85,-2.35),(.4,-1.9)],TOUCH),Dot([.4,-1.9,0],color=TOUCH),
                      Track([(.85,-2.35),(.45,-2.6)],TOUCH),Dot([.45,-2.6,0],color=TOUCH))
        self.at('Other branches'); self.play(Create(branch),run_time=.25)
        self.at('dorsal horn'); self.play(FadeIn(leader('dorsal horn',4,-1.9,(.5,-1.9),STRUCT)),run_time=.2)
        self.finish()


class S05Blue3(Timed):
    def construct(self):
        a,s,b,th,term,c,ctx=blue_parts(); labs=blue_labels(); self.add(tall_base(),a,s,labs[0])
        self.at('a second axon'); self.play(Create(b),FadeIn(labs[1]),run_time=.45)
        self.at('climbs to the thalamus'); self.play(FadeIn(th),FadeIn(term),FadeIn(labs[2]),FadeIn(ctx),run_time=.3)
        self.at('A thalamic neuron'); self.play(Create(c),run_time=.5)
        self.finish()


class S06Blue4(Timed):
    def construct(self):
        self.add(tall_base(),*blue_parts(),blue_labels())
        self.at('crosses in the medulla'); self.play(Create(ring(-.1,1.95)),run_time=.3)
        self.play(FadeIn(leader('crosses in medulla',-4.2,-.35,(-.1,1.9),TOUCH)),run_time=.25)
        self.finish()


class S07Red(Timed):
    def construct(self):
        self.add(tall_base(),red_parts()[0])
        self.at('The red line'); self.play(FadeIn(label('Spinothalamic\npathway',-4.2,1.9,PAIN,30)),run_time=.25)
        self.at('pain and temperature'); self.play(FadeIn(label('pain + temperature',-4.2,.45,PAIN,26)),run_time=.25)
        self.finish()


class S08Red2(Timed):
    def construct(self):
        self.add(tall_base()); a,s,*_=red_parts()
        self.at('Its sensory axon'); self.play(Create(a),Create(Track([(1.15,-2.7),(1.15,-.8)],PAIN)),
                                                 FadeIn(leader("Lissauer’s tract",4,-2.7,(1.25,-2.4),PAIN)),run_time=.4)
        self.at('synapses in the dorsal horn'); self.play(FadeIn(s),FadeIn(leader('dorsal horn',4,-.35,(.65,-1.25),PAIN)),run_time=.3)
        self.at('near where it entered'); self.play(Create(ring(.65,-1.25)),run_time=.3)
        self.finish()


class S09Red3(Timed):
    def construct(self):
        a,s,b,term=red_parts(); labs=red_labels(); self.add(tall_base(),a,s,thalamus())
        self.at('The next axon'); self.play(Create(b),FadeIn(term),FadeIn(labs[2]),run_time=.5)
        self.at('within a segment'); self.play(Create(ring(0,-1.65)),run_time=.25)
        self.at('climbs the opposite side'); self.play(FadeIn(VGroup(labs[0],labs[1])),run_time=.3)
        travel(self,b,.55)
        self.finish()


class S10Red4(Timed):
    def construct(self):
        self.add(tall_base(),*red_parts(),thalamus(),red_labels())
        self.at('crosses in the spinal cord'); self.play(Create(ring(0,-1.65)),
            FadeIn(leader('crosses in the cord',3.9,-.5,(.15,-1.5),PAIN)),run_time=.35)
        self.finish()


class S11Predict(Timed):
    def construct(self):
        self.add(levels(),label('Predict the deficit',2.9,-2.5,STRUCT,28))
        self.at('cut the right half'); self.play(FadeIn(cut()),run_time=.35)
        self.at('Which side loses touch'); self.play(FadeIn(label('Which side loses touch?',2.9,.6,TOUCH,30)),run_time=.2)
        self.at('which loses pain'); self.play(FadeIn(label('Which side loses pain?',2.9,-.6,PAIN,30)),run_time=.2)
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question1(),label('pause and decide',2.9,-2.5,STRUCT,28)); self.wait(5)


class S13Touch(Timed):
    def construct(self):
        self.add(levels(-3.6),cut(x=-3.6,caption=False),lesion_body(blue=False,red=False),
                 label('Right-half cut at T10',0,3.5,CUT,28))
        self.at('Fine touch'); self.play(FadeIn(label('Fine touch\nvibration · position',.2,1.65,TOUCH,26)),run_time=.25)
        self.at('lost on the right'); self.play(FadeIn(shade(3.6,1,TOUCH)),
             FadeIn(leader('RIGHT: lost',.7,-.4,(3.95,-1.5),TOUCH,28)),run_time=.3)
        self.at('has not crossed yet'); self.play(Create(stopped_route(x=-3.6)),
            FadeIn(leader('not yet\ncrossed',-.1,-1.75,(-2.75,-1.75),TOUCH,26)),run_time=.4)
        self.finish()


class S14Pain(Timed):
    def construct(self):
        self.add(levels(-3.6),cut(x=-3.6,caption=False),lesion_body(blue=True,red=False),stopped_route(x=-3.6),
                 label('Right-half cut at T10',0,3.5,CUT,28))
        self.at('lost on the left'); self.play(FadeIn(shade(3.6,-1,PAIN,.15)),
             FadeIn(label('LEFT: pain lost',0,-3.6,PAIN,28)),run_time=.3)
        self.at('have already crossed'); self.play(Create(stopped_route(PAIN,x=-3.6)),
             FadeIn(leader('crossed from\nthe left',-.1,-1.6,(-3.6,.75),PAIN)),run_time=.5)
        self.finish()


class S15Follow(Timed):
    def construct(self):
        self.add(levels(),cut(),label('One left pain fibre',2.8,-1,PAIN,28))
        self.at('Follow one left'); self.play(Create(fibre()),FadeIn(Dot([-2.65,-.65,0],color=PAIN,radius=.13)),run_time=.35)
        self.at('entering one segment'); self.play(FadeIn(leader('entry at T11',-4.6,-1.5,(-3.8,-.65),PAIN)),run_time=.25)
        self.finish()


class S16Follow2(Timed):
    def construct(self):
        self.add(levels(),cut(caption=False),fibre(),Dot([-2.65,-.65,0],color=PAIN,radius=.13),label('illustrative routes',2.4,3.2,STRUCT,28))
        a,b=options()
        self.at('In this simple example'); self.play(Create(relays()),FadeIn(leader('dorsal horn\nrelay',-4.8,1.5,(-2.65,-.65),STRUCT)),run_time=.45)
        self.at('reaches the other side'); self.play(Create(a),FadeIn(label('T10',2.5,.75,PAIN,28)),run_time=.35)
        self.at('a segment or two higher'); self.play(Create(b),FadeIn(label('or',2.5,1.33,STRUCT,26)),FadeIn(label('T9',2.5,1.95,PAIN,28)),run_time=.35)
        self.finish()


class S17Follow3(Timed):
    def construct(self):
        a,b=options(); labs=option_labels()
        self.add(levels(),cut(caption=False),fibre(),relays(),a,b,label('illustrative routes',2.4,3.2,STRUCT,28),label('or',2.5,1.33,STRUCT,26),
                 leader('dorsal horn\nrelay',-4.8,1.5,(-2.65,-.65),STRUCT,26))
        self.at('Crossing at the cut'); self.play(Indicate(a,color=PAIN),run_time=.3)
        self.at('it is lost'); self.play(FadeIn(labs[0]),run_time=.2)
        self.at('Crossing above the cut'); self.play(Indicate(b,color=PAIN),run_time=.3)
        self.at('it is spared'); self.play(FadeIn(labs[1]),run_time=.2)
        self.finish()


class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(option_frame()); self.wait(2)


class S18Follow4(Timed):
    def construct(self):
        red=shade(-3.6,-1,PAIN,.15)
        self.add(lesion_body(blue=True,red=False,x=-3.6),red,
                 label('Left pain loss',2.5,2.1,PAIN,32),label('T10: right-half cut',2.5,3.1,CUT,28))
        self.at('pain loss on the left'); self.play(Indicate(red,color=PAIN),run_time=.25)
        self.at('begins one or two segments'); self.play(Transform(red,shade(-3.6,-1,PAIN,-.75)),
            FadeIn(label('begins about T11–T12',2.5,.8,PAIN,30)),
            FadeIn(label('1–2 segments below the cut',2.5,-.2,STRUCT,26)),run_time=.65)
        self.finish()


class S19Band(Timed):
    def construct(self):
        self.add(lesion_body(x=-3.8),label('Segmental sensory loss',2.3,3.2,size=32),
                 label('schematic · real borders are less sharp',1.6,-3.4,STRUCT,26))
        band=VGroup(Rectangle(width=.3,height=.6,stroke_width=0,fill_color=TOUCH,fill_opacity=1).move_to([-3.61,-.15,0]),
                    Rectangle(width=.3,height=.6,stroke_width=0,fill_color=PAIN,fill_opacity=1).move_to([-3.31,-.15,0]),
                    Rectangle(width=.65,height=.65,color=CUT,stroke_width=3).move_to([-3.46,-.15,0]))
        diagram=VGroup(Rectangle(width=5.8,height=4.3,color=STRUCT,fill_color=STRUCT,fill_opacity=.08).move_to([2.8,-.1,0]),
                       label('right dorsal entry zone',2.8,2.4,STRUCT,28))
        blue=Track([(5.45,1.0),(1.3,1.0)],TOUCH)
        red=Track([(5.45,-.9),(1.3,-.9)],PAIN)
        horn=VGroup(chip('dorsal horn',STRUCT,26).move_to([2.7,-1.65,0]),
                    Dot([1.3,-.9,0],color=PAIN,radius=.12),Line([1.45,-1.0,0],[2.3,-1.35,0],color=STRUCT))
        lesion=VGroup(Rectangle(width=.6,height=2.8,color=CUT,fill_color=CUT,fill_opacity=.18).move_to([1.3,.2,0]),
                       mark(1.3,1.0),mark(1.3,-.9),leader('cut',.45,.2,(1,.2),CUT,26))
        self.add(diagram,Track(blue.pts,STRUCT),Track(red.pts,STRUCT))
        self.at('at the cut itself'); self.play(FadeIn(band),run_time=.3)
        self.at('a narrow band'); self.play(Indicate(band,color=CUT),run_time=.3)
        self.at('sensory fibers entering there'); self.play(Create(blue),Create(red),
             FadeIn(label('touch fibres\nentering at the cut',3.8,1.5,TOUCH,26)),
             FadeIn(label('pain fibres\nentering at the cut',3.8,-.2,PAIN,26)),run_time=.4)
        self.at('the dorsal horn'); self.play(FadeIn(horn),FadeIn(lesion),run_time=.35)
        self.finish()


class S20Name(Timed):
    def construct(self):
        self.add(lesion_body(x=-3.6),label('Right: fine touch lost',2.4,1.2,TOUCH,29),label('Left: pain lost',2.4,.1,PAIN,29),
                 label('plus weakness on the cut side',2.4,-1.15,STRUCT,26))
        self.at('Fine touch lost'); self.play(FadeIn(label('Brown-Séquard pattern',1.8,2.75,size=34)),run_time=.25)
        self.finish()


class S21Predict2(Timed):
    def construct(self):
        self.add(body(-3.6),label('Run it backwards',2.4,3,STRUCT,30))
        self.at('Pain is lost'); self.play(FadeIn(shade(-3.6,1,PAIN,-.9)),FadeIn(label('Right leg: pain lost',2.4,1.8,PAIN,30)),
             FadeIn(label('below the waist',2.4,-.25,STRUCT,26)),run_time=.25)
        self.at('vibration in the left'); self.play(FadeIn(shade(-3.6,-1,TOUCH,-.9)),FadeIn(label('Left leg: vibration lost',2.4,.7,TOUCH,30)),run_time=.25)
        self.at('Which half'); self.play(FadeIn(label('Which half of the cord is cut?',2,-1.5,size=29)),run_time=.25)
        self.finish()


class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        # Match the puzzle's leg-only shading; no new lesion level in this puzzle.
        self.add(body(-3.6),shade(-3.6,1,PAIN,-.9),shade(-3.6,-1,TOUCH,-.9),
                 label('Right leg: pain lost',2.4,1.8,PAIN,30),label('Left leg: vibration lost',2.4,.7,TOUCH,30),
                 label('below the waist',2.4,-.25,STRUCT,26),label('Which half of the cord is cut?',2,-1.5,size=29),
                 label('pause and decide',2.4,-2.7,STRUCT,26)); self.wait(5)


class S23Reveal2(Timed):
    def construct(self):
        self.add(levels())
        self.at('The left half'); self.play(FadeIn(Rectangle(width=1.7,height=1.25,stroke_color=CUT,fill_color=CUT,fill_opacity=.35).move_to([-2.65,.75,0])),FadeIn(label('LEFT half cut',2.8,2.8,CUT,32)),run_time=.25)
        blue=stopped_route(x=-1.8,right=False)
        # Offset both the entry and ascent so neither route obscures the other.
        red=VGroup(Track([(-.75,-2.7),(-.75,-1.5),(-2.35,-1.5),(-2.35,.44)],PAIN),mark(-2.35,.45))
        self.at('Vibration rides the blue line'); self.play(Create(blue),FadeIn(label('vibration: same side',2.8,1.6,TOUCH,28)),run_time=.3)
        self.at('stays on its own side'); self.play(Create(red),FadeIn(label('Right-leg pain crosses below T10;\nthe left-half cut blocks its ascent.',2.8,-.3,PAIN,26)),
             FadeIn(label('Both lines stop at the cut',2.8,-2,STRUCT,26)),run_time=.35)
        self.finish()


class S24Takeaway(Timed):
    def construct(self):
        # The blue entry lies above the red crossing, keeping both routes distinct.
        base=VGroup(Rectangle(width=3.4,height=4.1,color=STRUCT).move_to([0,-.8,0]),
                    DashedLine([0,-2.85,0],[0,2.1,0],color=STRUCT),
                    RoundedRectangle(width=3.6,height=.7,corner_radius=.1,color=STRUCT).move_to([0,1.75,0]),
                    label('L',-1.3,-2.55,STRUCT,26),label('R',1.3,-2.55,STRUCT,26),
                    label('dorsal view',0,-3.15,STRUCT,26))
        blue=VGroup(Track([(2.5,-.55),(.9,-.55),(.9,1.65)],TOUCH),Dot([.9,1.65,0],color=TOUCH),
                    Track([(.8,1.65),(.4,1.65),(-.15,1.45),(-.75,1.65),(-.75,2.4)],TOUCH),Dot([-.75,2.4,0],color=TOUCH))
        red=VGroup(Track([(2.6,-1.15),(1.2,-1.15),(.6,-1.15)],PAIN),Dot([.6,-1.15,0],color=PAIN),
                   Track([(.5,-1.15),(.5,-1.6),(-1.2,-1.6),(-1.2,2.4)],PAIN),Dot([-1.2,2.4,0],color=PAIN))
        targets=VGroup(RoundedRectangle(width=2.1,height=.5,corner_radius=.1,color=STRUCT).move_to([-.8,2.45,0]),
                       label('thalamus',3.5,2.45,STRUCT,26),Line([.4,2.45,0],[2.65,2.45,0],color=STRUCT))
        self.add(base,targets,blue,red,label('For these two routes,',0,3.45,size=30),
                 label('where a line crosses tells you where the damage is.',0,2.9,size=28))
        self.at('For these two routes'); self.play(FadeIn(leader('Touch: medulla',-4.3,1.6,(-.2,1.5),TOUCH,28)),
             FadeIn(leader('Pain: spinal cord',3.9,-1.6,(.05,-1.6),PAIN,28)),run_time=.3)
        self.at('where a line crosses'); self.play(Create(ring(-.1,1.5)),Create(ring(0,-1.6)),run_time=.3)
        self.at('where the damage is'); self.play(FadeIn(label('the side of the deficit tells you the side of the cut',0,-3.65,size=27)),run_time=.25)
        self.finish()


class S25End(EndCard):
    LINE='For these two routes, where a line crosses tells you where the damage is.'
    def construct(self):
        self.add(label('For these two routes,',0,1.4,size=32),
                 label('where a line crosses tells you\nwhere the damage is.',0,.05,size=38),
                 label('the side of the deficit tells you the side of the cut',0,-1.45,STRUCT,27),
                 label('biochemistrypedia.com',0,-2.8,TEAL,26))
        self.wait(3.5)
