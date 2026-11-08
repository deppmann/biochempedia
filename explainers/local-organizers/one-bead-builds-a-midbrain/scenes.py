"""Local organizers, chapter 2: One Bead Builds a Midbrain  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Geometry is one flat strip of neural tube, front at LEFT.  Real midbrain = XM..XI (3.0 wide).
The bead sits at BX, so the "new midbrain" BX..XM is the mirror image of the real one about XM,
which is also the midpoint between the bead and the real isthmus in the toy model.

COLOR MAP (one color per concept, whole film; same as the lesson's earlier film and chapters 1 and 3)
  BLUE   = forebrain tissue
  GREEN  = midbrain tissue (also the new, induced midbrain)
  PURPLE = hindbrain tissue (rhombomere 1 and behind), also cerebellum
  TEAL   = Otx2
  PINK   = Gbx2
  YELLOW = FGF8 and the organizer / bead (the signal source)
  ORANGE = Wnt1
  #508FF0 = Engrailed-on host cells; TEXT = graft outlines and summed signal
  RED    = repression, loss, removal
  GREY   = tube outline, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08BB4"
ORANGE = "#F29E4C"
FORE, MID, HIND = BLUE, GREEN, PURPLE
OTX, GBX, FGF, WNT = TEAL, PINK, YELLOW, ORANGE
DARKG = ManimColor("#2B5B33")
BRIGHTG = ManimColor(GREEN)

XL, XR = -6.3, 6.3
XM = -1.6      # front end of the real midbrain (= midpoint between bead and real isthmus)
XI = 1.4       # the real isthmus
BX = -4.6      # the bead
GX = -3.6      # the quail graft
LAM = 1.4      # toy model decay length (made-up number)


# ---------------------------------------------------------------------------------------------
# generic helpers
def at_dt(scene, phrase, dt, lead=0.2):
    """Wait until dt seconds after the narrator starts `phrase` (for words a transcript may spell oddly)."""
    rest = scene.t_of(phrase) + dt - lead - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def rect(x0, x1, cy, h, col, op=0.25, sw=0):
    return Rectangle(width=x1 - x0, height=2 * h, stroke_width=sw, stroke_color=col,
                     fill_color=col, fill_opacity=op).move_to([(x0 + x1) / 2, cy, 0])


class Strip:
    """Flat strip of neural tube, front at left: forebrain | midbrain | isthmus | hindbrain."""

    def __init__(self, cy, h, labels=True):
        self.cy, self.h = cy, h
        self.fore = rect(XL, XM, cy, h, FORE)
        self.mid = rect(XM, XI, cy, h, MID)
        self.hind = rect(XI, XR, cy, h, HIND)
        self.out = Rectangle(width=XR - XL, height=2 * h, stroke_color=GREY, stroke_width=4,
                             fill_opacity=0).move_to([(XL + XR) / 2, cy, 0])
        self.line = DashedLine([XI, cy - h - 0.12, 0], [XI, cy + h + 0.12, 0], color=TEXT, stroke_width=3)
        ly = cy + h + 0.38
        self.lab = VGroup(T("forebrain", 30, FORE).move_to([-3.2, ly, 0]),
                          T("midbrain", 30, MID).move_to([-0.1, ly, 0]),
                          T("hindbrain", 30, HIND).move_to([3.9, ly, 0]))
        self.body = VGroup(self.fore, self.mid, self.hind, self.out, self.line)
        self.all = VGroup(self.body, self.lab) if labels else VGroup(self.body)


def bead(pos, r=0.22):
    return Circle(radius=r, stroke_color=BG, stroke_width=2, fill_color=FGF, fill_opacity=1).move_to(pos)


def rings(pos, radii=(0.4, 0.62, 0.84), ops=(0.9, 0.55, 0.28), w=3.5):
    return VGroup(*[Circle(radius=r, stroke_color=FGF, stroke_width=w, stroke_opacity=o, fill_opacity=0).move_to(pos)
                    for r, o in zip(radii, ops)])


def pulse(scene, pos, r0=0.25, grow=3.2, rt=1.0):
    ring = Circle(radius=r0, stroke_color=FGF, stroke_width=4, fill_opacity=0).move_to(pos)
    scene.add(ring)
    scene.play(ring.animate.scale(grow).set_stroke(opacity=0), run_time=rt)
    scene.remove(ring)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(c, color=RED, s=0.45):
    p = np.array(c, float)
    return VGroup(Line(p + [-s, -s * 0.8, 0], p + [s, s * 0.8, 0], color=color, stroke_width=7),
                  Line(p + [-s, s * 0.8, 0], p + [s, -s * 0.8, 0], color=color, stroke_width=7))


def tcell(pos, r=0.2, kind="plain", col=TEXT):
    """A cell seen by its nucleus. plain = chick; dotted = quail (dotted outline and a dot)."""
    if kind == "plain":
        return Circle(radius=r, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.12).move_to(pos)
    ring = DashedVMobject(Circle(radius=r, color=col).move_to(pos), num_dashes=9, color=col).set_stroke(col, width=3)
    return VGroup(ring, Dot(pos, radius=r * 0.32, color=col))


def new_mid(cy, h, op=0.45, stroke=GREEN):
    return RoundedRectangle(corner_radius=0.3, width=2.65, height=2 * h - 0.10, stroke_color=stroke,
                            stroke_width=3.5, fill_color=MID, fill_opacity=op).move_to([BX, cy, 0])


# Keep timing diagnostics on stdout: the only persistent outputs are the requested artifacts.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=0.12, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        print(f'CUE {os.environ.get("KX_SCENE_ID")} {phrase}: late={max(0,-rest):.2f}')
        if rest > 0.02:
            self.wait(rest)

# The unchanged toy model: two exponential sources, lambda = 1.4 (illustrative).
CYT, HT = 1.75, 1.15
Y0, HS = -2.95, 2.35

def py(v): return Y0 + HS * v
def sig(x, xs): return np.exp(-abs(x-xs)/LAM)
def tot(x): return sig(x,BX)+sig(x,XI)
def curve(f, color=TEXT, x0=XL, x1=XR):
    m=VMobject().set_points_as_corners([[x,py(f(x)),0] for x in np.linspace(x0,x1,320)])
    return m.set_stroke(color,5)
def under(f, x0=XL, x1=XR):
    pts=[[x0,Y0,0]]+[[x,py(f(x)),0] for x in np.linspace(x0,x1,240)]+[[x1,Y0,0]]
    return Polygon(*pts,stroke_width=0,fill_color=FGF,fill_opacity=.18)
def slices(x0,x1,cy,h,n=12):
    w=(x1-x0)/n
    return VGroup(*[rect(x0+i*w,x0+(i+1)*w,cy,h,
        interpolate_color(DARKG,BRIGHTG,float(np.clip(tot(x0+(i+.5)*w),0,1))),.95,2)
        for i in range(n)])
def label(text,x,y,size=30,col=TEXT): return T(text,size,col).move_to([x,y,0])
def header(text): return label(text,0,3.5,36)

class Toy:
    def __init__(self):
        self.st=Strip(CYT,HT,False)
        self.st.line.set_opacity(0)
        self.bead=bead([BX,CYT,0],.24)
        self.isrc=bead([XI,CYT,0],.24)
        self.rb=rings([BX,CYT,0],(.42,.65,.9))
        self.ri=rings([XI,CYT,0],(.42,.65,.9))
        self.lb=label('bead',BX,3.45,32,FGF)
        self.li=label('real isthmus',XI,3.45,32,FGF)
        self.leaders=VGroup(Line([BX,3.16,0],[BX,2.05,0],color=FGF),Line([XI,3.16,0],[XI,2.05,0],color=FGF))
        self.axes=VGroup(arr([XL,Y0,0],[6.45,Y0,0],GREY,3),arr([XL,Y0,0],[XL,-.48,0],GREY,3))
        self.yl=label('signal',-5.55,-.32,28,GREY)
        self.xl=label('position along the tube',3.6,-3.42,28,GREY)
        self.title=label('Toy model · illustrative numbers',.7,-.12,34,TEXT)
        self.cb=curve(lambda x:sig(x,BX),FGF)
        self.ci=curve(lambda x:sig(x,XI),FGF)
        self.ct=curve(tot)
        self.ft=under(tot)
        self.ml=DashedLine([XM,Y0,0],[XM,-.55,0],color=GREY,stroke_width=3)
        self.mt=label('midpoint',XM,-3.42,30)
    def base(self,scene,total=False):
        scene.add(self.st.body,self.bead,self.isrc,self.lb,self.li,self.leaders,self.axes,self.yl,self.xl,self.title)
        if total: scene.add(self.ft,self.ct)
        else: scene.add(self.rb,self.ri,self.cb,self.ci)
    def parts(self,scene):
        self.base(scene,True)
        scene.add(slices(BX,XM,CYT,HT),slices(XM,XI,CYT,HT),self.bead,self.isrc,self.lb,self.li,self.leaders)
        scene.add(label('back',BX+.75,1.05),label('back',XI-.75,1.05))

def mirror_parts():
    return VGroup(label('front',XM,1.05),
        arr([BX+1.3,1.05,0],[XM-.65,1.05,0],TEXT,3),arr([XI-1.3,1.05,0],[XM+.65,1.05,0],TEXT,3))

def mirror_outline():
    # Open sides keep the midpoint's front label clear of the bracket.
    lo,hi=CYT-HT,CYT+HT
    edges=[Line([BX,y,0],[XM,y,0],color=TEXT,stroke_width=5) for y in (lo,hi)]
    corners=[Line([x,y,0],[x,y+d,0],color=TEXT,stroke_width=5)
             for x in (BX,XM) for y,d in ((lo,.2),(hi,-.2))]
    return VGroup(*edges,*corners)

def mirror_tag():
    txt=label('mirror image',(BX+XM)/2,2.48,30)
    bg=BackgroundRectangle(txt,color=BG,fill_opacity=.95,buff=.09)
    return VGroup(bg,txt,Line([(BX+XM)/2,2.75,0],[(BX+XM)/2,2.9,0],color=TEXT,stroke_width=3))

class S00Title(TitleCard):
    LESSON='Local Organizers: The Midbrain-Hindbrain Boundary'
    TITLE='One Bead Builds a Midbrain'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.65,28,TEAL),
            label('LOCAL ORGANIZERS: THE MIDBRAIN-HINDBRAIN BOUNDARY',0,.85,25,GREY),
            label(self.TITLE,0,-.15,52),Line([-1.2,-1,0],[1.2,-1,0],color=FGF,stroke_width=4))
        self.wait(self.narration_s)

class S01Q(SpokenScene):
    def construct(self):
        cy,h=.2,2.3
        st=Strip(cy,h)
        self.add(st.body,st.lab)
        bands=VGroup(rect(XI-.65,XI-.1,cy,h,WNT,.8),rect(XI+.1,XI+.65,cy,h,FGF,.8))
        chips=VGroup(chip('Wnt1',WNT,30).move_to([XI-.9,-2.8,0]),chip('Fgf8',FGF,30).move_to([XI+.9,-2.8,0]))
        self.at('a source'); self.play(FadeIn(bands),FadeIn(chips),run_time=.35)
        self.at('add it'); b=bead([BX,3.35,0],.28); self.add(b)
        self.at('somewhere new'); self.play(b.animate.move_to([BX,cy,0]),run_time=.55)
        self.at('watch what'); self.play(FadeIn(rings([BX,cy,0],(.65,1,1.35))),FadeIn(label('?',BX+1,cy,52)),run_time=.5)
        self.finish()

class S02Suff(SpokenScene):
    def construct(self):
        definition=VGroup(label('sufficient: adding it where it is normally absent',0,3,30),label('produces the structure',0,2.45,30))
        box=Rectangle(width=4.8,height=3.3,color=FORE,fill_color=FORE,fill_opacity=.16).move_to([-3.5,-.1,0])
        structure=Ellipse(width=4.3,height=3.3,color=MID,fill_color=MID,fill_opacity=.08).move_to([3.6,-.1,0])
        a=arr([-.6,-.1,0],[1,-.1,0],TEXT,6)
        self.add(definition,box,a,structure,label('normally absent here',-3.5,-2.3,30),label('structure',3.6,-2.3,32))
        b=bead([-3.5,1.5,0],.3); self.add(b,label('factor',-3.5,2.05,32,FGF))
        self.at('adding it'); self.play(b.animate.move_to([-3.5,-.1,0]),run_time=.7)
        self.at('produces the'); self.play(structure.animate.set_fill(MID,.55).set_stroke(MID,5),run_time=.65)
        self.finish()

def embryo(x,kind):
    outline=Ellipse(width=5.5,height=4.8,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.1).move_to([x,.3,0])
    cells=VGroup(*[tcell([x+dx,.3+dy,0],.25,kind) for dx in (-1.6,-.8,0,.8,1.6) for dy in (-1.4,-.7,0,.7,1.4) if (dx/2.3)**2+(dy/2)**2<1])
    return VGroup(outline,cells)
class S03Graft(SpokenScene):
    def construct(self):
        q,h=embryo(-3.4,'dotted'),embryo(3.4,'plain')
        self.add(q,h,label('quail embryo',-3.4,3.15,32),label('chick embryo',3.4,3.15,32),label('dotted nuclei = quail     plain = chick',0,-2.9,30))
        self.at('grafted quail'); arrow=arr([-1,.3,0],[1,.3,0],TEXT,5); self.play(GrowArrow(arrow),run_time=.6)
        self.at('look different'); self.play(Indicate(q[1],color=FGF,scale_factor=1.04),run_time=.8)
        self.finish()

def piece(x,y,h):
    return VGroup(rect(x-.55,x+.55,y,h,HIND,.6,3),*[tcell([x+dx,y+dy,0],.17,'dotted') for dx in (-.27,.27) for dy in (-.65,0,.65)])
class S04Graft2(SpokenScene):
    def construct(self):
        # Two 2.6-unit strips use 65% of frame height together.
        d,h=Strip(1.65,1.3,False),Strip(-1.45,1.3,False)
        pc=piece(XI+.7,1.65,1.2)
        self.add(d.body,h.body,pc,label('quail donor',-4.5,2.55,30),label('chick forebrain',-4.5,-3.2,30),label('junction',3.5,2.55,28),arr([2.6,2.55,0],[XI+.1,2.55,0],TEXT,3))
        self.at('martinez'); self.play(FadeIn(label('Martínez, Wassef and Alvarado-Mallart, 1991',0,3.45,28,GREY)),run_time=.35)
        self.at('moved tissue'); self.play(Indicate(pc,color=TEXT,scale_factor=1.08),run_time=.5)
        self.at('just behind'); self.play(Indicate(d.line,color=FGF),run_time=.5)
        self.at('into the forebrain'); self.play(pc.animate.move_to([-3.6,-1.45,0]),run_time=.55)
        self.wait(.65)
        self.finish()

HCY,HH=.25,2.2
EN='#508FF0'  # Engrailed-positive host nuclei; dotted quail nuclei remain white.
def host_world(done=False):
    st=Strip(HCY,HH,False)
    graft=piece(-2.7,HCY,2.05)
    cells=VGroup(*[tcell([x,y,0],.26,'plain',MID if done else FORE) for x in (-4.4,-3.6,-1.8,-1) for y in (-1.1,-.4,.3,1,1.7)])
    return st,graft,cells
class S05Host(SpokenScene):
    def construct(self):
        st,g,c=host_world(); self.add(st.body,g,c,label('quail graft',-2.7,3.15,32))
        self.at('graft turned'); en=label('Engrailed on',-2.7,-2.65,34,EN)
        self.play(c.animate.set_stroke(EN,4).set_fill(EN,.8),FadeIn(en),run_time=.5)
        self.at('later they'); self.wait(.15)
        growth=RoundedRectangle(width=4.4,height=4.1,corner_radius=.6,color=MID,fill_color=MID,fill_opacity=.25).move_to([-2.7,HCY,0])
        self.play(FadeIn(growth),c.animate.set_stroke(MID,3).set_fill(MID,.8),FadeIn(label('midbrain',.7,-2.65,34,MID)),run_time=.7)
        self.add(g)
        self.at('instruct its'); self.play(FadeIn(label('the junction instructs its neighbours',0,-3.35,30)),run_time=.4)
        self.finish()
class S06Beat(NarratedScene):
    def construct(self):
        st,g,c=host_world(True); c.set_fill(MID,.8)
        growth=RoundedRectangle(width=4.4,height=4.1,corner_radius=.6,color=MID,fill_color=MID,fill_opacity=.25).move_to([-2.7,HCY,0])
        self.add(st.body,growth,c,g,label('quail graft',-2.7,3.15,32),label('Engrailed on',-2.7,-2.65,34,EN),label('midbrain',.7,-2.65,34,MID),label('the junction instructs its neighbours',0,-3.35,30))
        self.wait(self.narration_s)

SCY,SH=.2,2.25
class S07Bead(SpokenScene):
    def construct(self):
        st=Strip(SCY,SH); self.add(st.body,st.lab)
        question=label('What was the message?',0,-2.8,34); self.add(question)
        self.at('soaked'); b=bead([BX,3.35,0],.28); bl=label('FGF8 bead',-2.8,3.35,30,FGF)
        self.play(FadeIn(b),FadeIn(bl),run_time=.4)
        self.at('placed them'); self.play(b.animate.move_to([BX,SCY,0]),FadeOut(bl),FadeOut(question),run_time=.65)
        self.play(FadeIn(label('Crossley, Martínez and Martin, 1996',0,-3.4,28,GREY)),run_time=.3)
        self.at('the diencephalon'); self.play(FadeIn(VGroup(label('diencephalon',BX,-2.55,30,FORE),Line([BX,-2.25,0],[BX,-1.95,0],color=FORE))),run_time=.35)
        self.at('back of the'); halo=rings([BX,SCY,0],(.65,.95,1.2),(.95,.8,.6)); en=label('Engrailed on',BX,1.8,30,EN)
        halo.set_color(EN); self.play(FadeIn(halo),FadeIn(en),run_time=.5)
        self.at('midbrain formed'); nm=new_mid(SCY,SH)
        self.play(FadeOut(halo),FadeOut(en),GrowFromCenter(nm),FadeIn(label('extra',BX,-.95,30,MID),label('midbrain',BX,-1.45,30,MID)),run_time=.65)
        self.add(b); self.finish()

def prediction1():
    st=Strip(SCY,SH,False); nm=new_mid(SCY,SH)
    return VGroup(st.body,nm,bead([BX,SCY,0],.27),rect(XI+.1,XI+.7,SCY,SH,FGF,.8),
        label('bead',BX,2.85,30,FGF),label('new midbrain',BX,-1.45,28,MID),label('real midbrain',-.1,2.85,30,MID),label('real isthmus',XI,-2.55,30,FGF))
Q1='Which way will the new midbrain face?'
class S08Predict(SpokenScene):
    def construct(self):
        self.add(prediction1())
        self.at('predict'); self.play(FadeIn(header('Predict')),run_time=.3)
        self.at('which way'); self.play(FadeIn(label(Q1,0,-3.35,34)),FadeIn(label('?',BX,SCY+.85,60)),run_time=.5)
        self.finish()
class S09Pause(NarratedScene):
    def construct(self):
        self.add(prediction1(),header('Predict'),label(Q1,0,-3.35,34),label('?',BX,SCY+.85,60)); self.wait(self.narration_s)

class S10Rev(SpokenScene):
    def construct(self):
        st=Strip(.15,2.35,False); nm=new_mid(.15,2.35); self.add(st.body,nm,bead([BX,.15,0],.25),label('bead',BX,3.1,32,FGF),label('real isthmus',XI,3.1,32,FGF))
        self.at('built in reverse')
        parts=VGroup(slices(BX,XM,.15,2.35),slices(XM,XI,.15,2.35))
        names=VGroup(label('back',BX+.5,-1.55),label('front',XM-.55,-1.55),label('front',XM+.65,-1.55),label('back',XI-.4,-1.55))
        self.play(FadeOut(nm),FadeIn(parts),FadeIn(names),run_time=.55); self.add(bead([BX,.15,0],.25))
        self.at('mirror image'); self.play(FadeIn(label('mirror image',-3.1,-3,36)),Create(DashedLine([XM,-2.4,0],[XM,2.6,0],color=TEXT)),run_time=.4)
        self.at('parts that normally'); self.play(Indicate(names[3],scale_factor=1.2),run_time=.45)
        self.at('formed nearest'); self.play(Indicate(names[0],scale_factor=1.2),run_time=.45); self.finish()

class S11Geom(SpokenScene):
    def construct(self):
        t=Toy(); initial=slices(BX,XM,CYT,HT); self.add(t.st.body,initial,t.bead,t.lb,t.leaders[0])
        self.at('reverse the order'); self.play(Indicate(t.bead,color=FGF,scale_factor=1.5),run_time=.4)
        self.at('toy model'); self.play(FadeOut(initial),FadeIn(t.axes),FadeIn(t.yl),FadeIn(t.xl),FadeIn(t.title),run_time=.6)
        self.at('second source'); self.play(FadeIn(t.isrc),FadeIn(t.li),FadeIn(t.leaders[1]),run_time=.5)
        self.at('and the real'); self.play(FadeIn(t.rb),Create(t.cb),run_time=.6)
        self.at('isthmus send'); self.play(FadeIn(t.ri),Create(t.ci),run_time=.6)
        self.at('same signal'); self.play(Indicate(t.cb,scale_factor=1),Indicate(t.ci,scale_factor=1),run_time=.5); self.finish()
class S12Geom2(SpokenScene):
    def construct(self):
        t=Toy(); t.base(self)
        cell=tcell([-2.5,1.75,0],.3,'plain')
        cell_lab=label('one cell',-1.9,2.8,28)
        self.at('a cell cannot'); self.play(FadeIn(cell),FadeIn(cell_lab),run_time=.4)
        self.at('which source'); self.play(Indicate(t.rb,scale_factor=1.05),Indicate(t.ri,scale_factor=1.05),run_time=.5)
        self.at('gets the sum'); self.play(t.cb.animate.set_stroke(opacity=.25),t.ci.animate.set_stroke(opacity=.25),Create(t.ct),FadeIn(t.ft),run_time=.65)
        self.at('the sum falls'); self.play(FadeOut(cell),FadeOut(cell_lab),run_time=.25)
        d=Dot([BX,py(tot(BX)),0],color=TEXT)
        self.add(d); self.play(MoveAlongPath(d,curve(tot,x0=BX,x1=XM)),run_time=.8)
        self.at('midpoint'); self.play(Create(t.ml),FadeIn(t.mt),run_time=.4)
        self.at('rises toward'); self.play(MoveAlongPath(d,curve(tot,x0=XM,x1=XI)),run_time=.9); self.remove(d); self.finish()
class S13Geom3(SpokenScene):
    def construct(self):
        t=Toy(); t.base(self,True)
        self.at('in a normal'); self.play(FadeIn(slices(XM,XI,CYT,HT)),run_time=.5); self.add(t.isrc,t.li,t.leaders[1])
        self.at('build the back'); self.play(FadeIn(label('back',XI-.75,1.05,32)),run_time=.4)
        self.at('cells next to'); self.play(FadeIn(slices(BX,XM,CYT,HT)),run_time=.5); self.add(t.bead,t.lb,t.leaders[0])
        self.at('get a lot'); self.play(Indicate(t.bead,color=FGF,scale_factor=1.4),run_time=.35)
        self.at('so they build'); self.play(FadeIn(label('back',BX+.75,1.05,32)),run_time=.4); self.finish()
class S13bGeom4(SpokenScene):
    def construct(self):
        t=Toy(); t.parts(self)
        self.at('farther from'); d=Dot([BX,py(tot(BX)),0],color=TEXT); self.add(d)
        self.play(MoveAlongPath(d,curve(tot,x0=BX,x1=XM)),run_time=1.3)
        self.at('parts run toward'); self.play(FadeIn(mirror_parts()),run_time=.5)
        self.at('between'); self.play(Create(t.ml),FadeIn(t.mt),run_time=.4)
        self.at('wrong way'); box=mirror_outline()
        self.play(Create(box),FadeIn(mirror_tag()),run_time=.5); self.remove(d); self.finish()
class S14Beat(NarratedScene):
    def construct(self):
        t=Toy(); t.parts(self); self.add(mirror_parts(),t.ml,t.mt,mirror_outline(),mirror_tag()); self.wait(self.narration_s)

class S15Caution(SpokenScene):
    def construct(self):
        st=Strip(.4,1.9,False)
        response=RoundedRectangle(width=3.5,height=3.5,corner_radius=.3,color=MID,fill_color=MID,fill_opacity=.2).move_to([-4.35,.4,0])
        b=bead([BX,.4,0],.32)
        self.add(st.body,response,b,label('FGF8 bead',BX,1.75,30,FGF),header('Tissue around the bead'))
        self.at('switched on'); self.play(FadeIn(label('Engrailed-2 on',-4.35,2.75,32,EN)),response.animate.set_stroke(EN,4),run_time=.5)
        self.at('its own'); f=rect(-3.9,-3.4,.25,.9,FGF,.8,3); w=rect(-3.2,-2.7,.25,.9,WNT,.8,3)
        self.play(FadeIn(f),FadeIn(chip('Fgf8',FGF,32).move_to([-4.7,-2.1,0])),run_time=.4)
        at_dt(self,'its own',1.6)
        self.play(FadeIn(w),FadeIn(chip('Wnt1',WNT,32).move_to([-2.75,-2.1,0])),run_time=.4)
        self.at('that induced'); self.play(FadeIn(label('induced, isthmus-like organizer',1.6,2.75,30,FGF)),FadeIn(label('Fgf8 and Wnt1: from later bead experiments',0,-2.85,28)),FadeIn(label('Neither organizer nor bead gradient is established as the sole cause.',0,-3.45,26)),run_time=.5)
        self.finish()

def prediction2():
    st=Strip(.4,2,False)
    return VGroup(st.body,new_mid(.4,2),bead([BX,.4,0],.28),rect(XI+.1,XI+.7,.4,2,FGF,.8),
        label('bead made midbrain',-3.9,2.95,30,MID),label('cerebellum side',3.9,2.95,30,HIND),
        chip('Fgf8',FGF,30).move_to([XI+.4,-2.2,0]),label('Why midbrain?',0,-3.15,40),label('?',BX,1.3,60))
class S16Predict(SpokenScene):
    def construct(self):
        self.add(prediction2()); self.at('predict'); self.play(FadeIn(header('Predict')),run_time=.3)
        self.at('made midbrain'); self.play(Indicate(self.mobjects[0][1],color=MID,scale_factor=1.03),run_time=.5)
        self.at('side that builds'); self.play(Indicate(self.mobjects[0][0][2],color=HIND,scale_factor=1.03),run_time=.5); self.finish()
class S17Pause(NarratedScene):
    def construct(self):
        self.add(prediction2(),header('Predict')); self.wait(self.narration_s)

class S18Rev2(SpokenScene):
    def construct(self):
        # Both responsive tissues are present from the opening frame.
        boxes=VGroup(*[RoundedRectangle(width=5.7,height=3.3,corner_radius=.2,color=c,fill_color=c,fill_opacity=.2).move_to([x,1.15,0]) for x,c in ((-3.2,OTX),(3.2,GBX))])
        self.add(boxes,label('forebrain (diencephalon)',-3.2,3.3,28,FORE),label('rhombomere 1',3.2,3.3,30,HIND),label('responsive tissue only; dose and timing matter',0,-3.4,28))
        self.at('its cells carry'); self.play(FadeIn(chip('Otx2',OTX,34).move_to([-3.2,-.1,0])),FadeIn(chip('Gbx2',GBX,34).move_to([3.2,-.1,0])),run_time=.4)
        self.at('can respond'); sources=VGroup(*[VGroup(rings([x,1.5,0],(.45,.7,.95)),bead([x,1.5,0],.25)) for x in (-3.2,3.2)])
        self.play(FadeIn(sources),run_time=.5)
        # The two controls sit directly below their respective outcome panels.
        def controls(x):
            parts=VGroup()
            for dx,title in ((-1.35,'dose'),(1.35,'duration')):
                cx=x+dx; cy=-2.35
                parts.add(Arc(radius=.52,start_angle=0,angle=PI,color=FGF).move_arc_center_to([cx,cy,0]),
                    Line([cx,cy,0],[cx+.26,cy+.43,0],color=FGF,stroke_width=5),
                    label('low',cx-.63,cy-.18,22),label('high',cx+.63,cy-.18,22),
                    label(title,cx,cy-.65,28,FGF))
            parts.add(arr([x,-2.05,0],[x,-1.45,0],FGF,3))
            return parts
        dials=VGroup(controls(-3.2),controls(3.2))
        self.at('at this dose'); self.play(FadeIn(dials),run_time=.4)
        self.at('response was'); self.play(FadeIn(chip('midbrain',MID,36).move_to([-3.2,-1.05,0])),run_time=.5)
        self.at('or cerebellum'); self.play(FadeIn(chip('cerebellum',HIND,36).move_to([3.2,-1.05,0])),run_time=.5)
        self.at('depends on'); self.play(Indicate(dials,color=FGF,scale_factor=1.04),run_time=.6); self.finish()

class S19Rev3(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=5.6,height=3.6,corner_radius=.2,color=OTX,fill_color=OTX,fill_opacity=.2).move_to([3,.7,0])
        oc=chip('Otx2',TEXT,42).move_to([3,1.3,0])
        self.add(box,oc,header('A strong or lasting FGF8 source'))
        self.at('with a strong'); src=bead([-3.7,.7,0],.7); rg=rings([-3.7,.7,0],(1,1.4,1.8))
        self.play(FadeIn(src),FadeIn(rg),FadeIn(label('FGF8',-3.7,-1.65,36,FGF)),GrowArrow(arr([-1.5,.7,0],[-.1,.7,0],FGF,6)),run_time=.7)
        self.at('in later'); self.play(FadeIn(label('Martínez and colleagues, 1999',0,-3.4,28,GREY)),run_time=.4)
        self.at('off and'); self.play(Create(cross([3,1.3,0],RED,.7)),run_time=.4)
        at_dt(self,'off and',.85)
        self.play(FadeIn(chip('Gbx2 on',GBX,36).move_to([3,-.05,0])),run_time=.45)
        self.at('then isthmus'); self.play(FadeIn(chip('isthmus',FGF,40).move_to([-1.2,-1.9,0])),run_time=.4)
        self.at('cerebellum like'); self.play(FadeIn(chip('cerebellum-like tissue',HIND,38).move_to([3.25,-1.9,0])),run_time=.45); self.finish()

class S20Take(SpokenScene):
    def construct(self):
        self.add(header('Takeaway'))
        # All rows share the same icon centre and text left edge.
        def row_text(text,y,size=44):
            return T(text,size).move_to([-.8,y,0],aligned_edge=LEFT)
        source=VGroup(bead([-4.8,1.9,0],.3),rings([-4.8,1.9,0],(.5,.75)))
        self.at('the line is',lead=0); self.play(FadeIn(source),FadeIn(row_text('A line becomes a source.',1.9)),run_time=.25)
        icon2=chip('Signal',FGF,38).move_to([-4.8,-.25,0])
        self.at('signal tells',lead=0); self.play(FadeIn(icon2),FadeIn(row_text('which part',-.25,48)),run_time=.25)
        icon3=chip('Repressor',OTX,38).move_to([-4.8,-2.5,0])
        text3=VGroup(row_text('which region',-2.12,46),row_text('it can become',-2.9,46))
        self.at('repressor sets',lead=0); self.play(FadeIn(icon3),FadeIn(text3),run_time=.25); self.finish()

class S21End(EndCard):
    LINE='Signal guides parts; repressors set which region cells can become.'
    def construct(self):
        self.add(label('Signal guides parts;',0,.65,44),label('repressors set which region cells can become.',0,-.25,36),label('biochemistrypedia.com',0,-1.6,28,TEAL))
        self.wait(self.narration_s)
