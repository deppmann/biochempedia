"""Myelination, chapter 2: The Axon Sets the Dose

COLOR MAP (one colour per concept, shared with the other chapters; from scenes.old.py)
  BLUE   = the axon
  PURPLE = Schwann cell and its myelin sheath (the glial membrane wrapped around the axon)
  ORANGE = neuregulin-1 type III, the tethered signal on the axon surface (the "dose")
  ROSE   = ErbB3 / ErbB2 receptors; TEAL = Gpr126
  GREEN  = an active intracellular signal (kinase on, cAMP)
  GOLD   = highlights: the row or answer being asked about, contact, readouts
  TAN    = basal lamina
  GREY   = labels, outlines, table lines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TAN = "#C2A878"
ROSE = "#EF8EAD"
HI = YELLOW  # table-row highlight

# ------------------------------------------------------------------ shared builders
def mark(base, direction, length=0.45, head=0.11, color=ORANGE):
    d = np.array(direction, dtype=float)
    d = d / np.linalg.norm(d)
    p0 = np.array(base, dtype=float)
    p1 = p0 + d * length
    return VGroup(Line(p0, p1, color=color, stroke_width=3.5), Dot(p1, radius=head, color=color))


def marks_ring(c, r, spacing=0.45, length=0.3, head=0.09):
    n = max(6, int(round(2 * np.pi * r / spacing)))
    g = VGroup()
    for k in range(n):
        a = 2 * np.pi * k / n
        d = [np.cos(a), np.sin(a), 0]
        g.add(mark([c[0] + r * d[0], c[1] + r * d[1], 0], d, length, head))
    return g


def axon_circle(c, r=1.0, label=None, size=24):
    circ = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([c[0], c[1], 0])
    g = VGroup(circ)
    if label:
        g.add(T(label, size, BLUE).move_to(circ))
    g.set_z_index(3)
    return g


def sheath_ring(c, r_ax, R):
    """The myelin sheath as a ring between r_ax and R (R just above r_ax draws a hairline)."""
    R = max(R, r_ax + 0.03)
    out = Circle(radius=R, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.38).move_to([c[0], c[1], 0])
    inner = Circle(radius=r_ax, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([c[0], c[1], 0])
    lines = VGroup(*[Circle(radius=r_ax + (R - r_ax) * f, stroke_color=PURPLE, stroke_width=1.5, stroke_opacity=0.8, fill_opacity=0).move_to([c[0], c[1], 0])
                     for f in (0.25, 0.5, 0.75)])
    g = VGroup(out, inner, lines)
    g.set_z_index(2)
    return g


def blob(c, w, h, label=None, size=22):
    e = Ellipse(width=w, height=h, stroke_color=PURPLE, stroke_width=3.5, fill_color=PURPLE, fill_opacity=0.28).move_to([c[0], c[1], 0])
    g = VGroup(e)
    if label:
        g.add(T(label, size, PURPLE).move_to(e))
    return g


def spiral(c, r_out, r_in, turns, width=5):
    return ParametricFunction(
        lambda t: np.array([c[0] + (r_out - (r_out - r_in) * t / (TAU * turns)) * np.cos(t),
                            c[1] + (r_out - (r_out - r_in) * t / (TAU * turns)) * np.sin(t), 0.0]),
        t_range=[0, TAU * turns, 0.05], color=PURPLE, stroke_width=width)



# Reuse transcript timing without writing auxiliary logs into the chapter folder.
_BaseSpokenScene = SpokenScene
class SpokenScene(_BaseSpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


def label(text, x=0, y=3.2, color=TEXT, size=30):
    return T(text, size, color).move_to([x,y,0])


def choices(a,b,y=-3.2):
    # Parallel choices have separate columns and a common baseline.
    return VGroup(chip(a,GOLD,26).move_to([-3.25,-3.2,0]),
                  chip(b,GOLD,26).move_to([3.25,-3.2,0]))


# The same four objects persist from the transplant question into its answer.
CENTERS=[-4.65,1.55]
def moved():
    g=VGroup()
    for x in CENTERS:
        g.add(axon_circle([x,0.65],1.15),blob([x+2.7,0.65],1.8,2.0))
    return g

def moved_labels():
    return VGroup(label('Schwann cells from a bare-axon nerve',0,3.2,PURPLE),
                  label('new host: normally myelinated axons',0,-1.1,BLUE))

def graft_final():
    g=VGroup(moved(),moved_labels())
    for x in CENTERS:
        g.add(spiral([x,0.65],1.65,1.18,4))
    g.add(label('wrapped',0,2.3,PURPLE))
    g.add(reverse_row())
    g.add(label('In peripheral nerve, the axon decides.',0,-3.35,TEXT,36))
    return g

def reverse_row():
    return VGroup(label('reverse swap: cells from large-axon nerve, now beside thin axons',0,-1.65,PURPLE,26),
        *[VGroup(axon_circle([x,-2.45],0.36),blob([x+1.3,-2.45],1.65,1.2)) for x in [-5,-.5]],
        label('stayed bare',3.35,-2.45,BLUE,32))

# A stable, one-sided population of membrane-tethered proteins, shared by s07/s08.
MARK_X=[-5.6,-4.35,-3.1,-1.8,-0.45,0.9,2.3,3.75,5.2]
def signal_base():
    return VGroup(Rectangle(width=12.4,height=2.2,color=BLUE,fill_color=BLUE,fill_opacity=.22).move_to([0,-.7,0]),
        label('axon',-4.8,-.7,BLUE,34))
def surface_marks():
    return VGroup(*[mark([x,.4,0],[0,1,0],.55) for x in MARK_X]).set_z_index(4)
def signal_labels():
    return VGroup(label('neuregulin-1, type III',0,3.2,ORANGE,36),
        label("a protein on the axon's surface",0,-2.8,ORANGE,30))

# Dose table: omit untested None; fill Normal as a labelled reference when compared.
ROWS=['Half','Normal','Extra']
TX=[-6.5,-3.65,-1.7,.1]; TOP=2.9; RH=1.25
G={'half':.75,'normal':.65,'extra':.55}
PX,PY,RAX=3.65,.15,1.2
RR={k:RAX/v for k,v in G.items()}
def tcell(row,col,text,color):
    return label(text,(TX[col]+TX[col+1])/2,TOP-RH*(row+1.5),color,28)
def table(done=()):
    g=VGroup()
    for y in [TOP-i*RH for i in range(5)]:
        g.add(Line([TX[0],y,0],[TX[-1],y,0],color=GREY,stroke_width=2))
    for x in TX:
        g.add(Line([x,TOP,0],[x,TOP-4*RH,0],color=GREY,stroke_width=2))
    for i,t in enumerate(['type III dose','sheath','g ratio']):
        g.add(label(t,(TX[i]+TX[i+1])/2,TOP-RH/2,[ORANGE,PURPLE,GOLD][i],28))
    for i,t in enumerate(ROWS):
        g.add(tcell(i,0,t,TEXT))
    for key in dict.fromkeys(['normal', *done]):
        i=['half','normal','extra'].index(key)
        g.add(tcell(i,1,{'half':'thinner','normal':'reference','extra':'thicker'}[key],PURPLE),
              tcell(i,2,f'{G[key]:.2f}',GOLD))
    return g

def row_hi(i):
    return Rectangle(width=TX[-1]-TX[0],height=RH,color=GOLD,fill_color=GOLD,fill_opacity=.1).move_to([(TX[0]+TX[-1])/2,TOP-RH*(i+1.5),0])
def normal_outline():
    return DashedVMobject(Circle(radius=RR['normal'],color=GREY),num_dashes=44).move_to([PX,PY,0])
def dose_question(extra=False):
    return VGroup(table(['half'] if extra else []),row_hi(2 if extra else 0),axon_circle([PX,PY],RAX,'axon',28),normal_outline(),
                  label('sheath?   g ratio?',PX,2.75,GOLD,30),
                  label('dashed: normal reference',PX,-2.35,TEXT,26))
def dose_notes():
    return VGroup(label('g values illustrative; normal near 0.6–0.7',0,-2.8,TEXT,26),
        label('Michailov, Nave et al., 2004; Taveggia et al., 2005',0,-3.4,TEXT,26))
def trio():
    g=VGroup()
    for x,key in zip([-4.7,0,4.7],['half','normal','extra']):
        r=1.1
        g.add(sheath_ring([x,0],r,r/G[key]),axon_circle([x,0],r),
            label(key,x,2.65,ORANGE,32),label(f'g = {G[key]:.2f}',x,-2.5,GOLD,30))
    g.add(label('dose down  ←  normal  →  dose up',0,3.4,ORANGE,28),
          label('illustrative g values',0,-3.35,TEXT,26))
    return g

# Culture drawn in cross section: the same concentric membrane turns as other scenes.
DISH_C=[0,-.15,0]; CULT_X=[-3.9,0,3.9]; CULT_Y=-.1
def culture_base():
    return VGroup(Ellipse(width=12.5,height=5.6,color=GREY).move_to(DISH_C),
        *[axon_circle([x,CULT_Y],.7) for x in CULT_X],
        label('sympathetic neurons: normally bare',0,3.2,BLUE,32),
        label('culture dish • axon cross sections',0,-2.5,TEXT,26))
def culture_marks():
    return VGroup(*[marks_ring([x,CULT_Y],.7,.45,.22,.07) for x in CULT_X]).set_z_index(4)
def culture_cells():
    return VGroup(*[blob([x+.1,1.35],1.65,.8) for x in CULT_X])
def culture_labels():
    return VGroup(label('extra type III',-3.8,-1.65,ORANGE,28),label('Schwann cells',0,2.25,PURPLE,28))
def culture_question():
    return VGroup(culture_base(),culture_marks(),culture_cells(),culture_labels(),label('What will the cells do?',0,-3.3,GOLD,32))
def culture_wraps():
    return VGroup(*[sheath_ring([x,CULT_Y],.7,1.18) for x in CULT_X])

def comparison(wrapped=True):
    g=VGroup()
    for x in [-3.4,3.4]:
        g.add(RoundedRectangle(width=6,height=5.2,corner_radius=.25,color=GREY).move_to([x,0,0]),
              axon_circle([x,-.3],.85),label('control: bare axons' if x<0 else 'extra type III',x,2.1,BLUE if x<0 else ORANGE,30))
        if x<0 or not wrapped:
            g.add(blob([x,1],1.8,.65))
        if x>0:
            if not wrapped: g.add(marks_ring([x,-.3],.85,.45,.2,.07))
            if wrapped:
                g.add(sheath_ring([x,-.3],.85,1.45),label('wrapped axons',x,-2.05,PURPLE,30))
    return g

class S00Title(TitleCard):
    LESSON='Myelination: Wrapping the Axon So the Signal Jumps'
    TITLE='The Axon Sets the Dose'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.7,TEAL,26),label('MYELINATION',0,.8,TEXT,28),
            T(self.TITLE,52,font=TITLE_FONT).move_to([0,-.3,0]),Line([-1.2,-1.2,0],[1.2,-1.2,0],color=GOLD))
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        cell=blob([-3.3,.4],4.5,4.5)
        right=blob([3.4,.4],4.7,4.3)
        grooves=VGroup()
        for x,y in [(1.32,.4),(2.5,-1.5),(4.35,-1.5)]:
            grooves.add(Circle(radius=.48,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0]),axon_circle([x,y],.27))
        self.add(cell,right,grooves,axon_circle([-3.3,.4],1.15),
            label('Schwann cell',-3.3,3.2,PURPLE,30),label('Schwann cell',3.4,3.2,PURPLE,30))
        self.at('large axon')
        self.play(FadeIn(label('large axon',-3.3,-2.25,BLUE)),run_time=.5)
        turns=label('dozens of turns',-3.3,-2.9,PURPLE)
        self.at('wraps it in')
        self.play(Create(spiral([-3.3,.4],1.95,1.18,6)),FadeIn(turns),run_time=1.3)
        self.at('beside a thin')
        self.play(FadeIn(label('thin axons in grooves',3.4,-2.25,BLUE,28)),run_time=.6)
        bare=label('no wrap',3.4,-2.9,PURPLE)
        self.at('wraps nothing')
        self.play(FadeIn(bare),run_time=.35)
        self.at('who decides')
        self.play(FadeOut(turns),FadeOut(bare),
            FadeIn(label('Who decides? glia or axon?',0,-3.05,GOLD,40)),run_time=.3)
        self.finish()

class S02Graft(SpokenScene):
    def construct(self):
        cells=[]
        for x,bare in [(-3.35,True),(3.35,False)]:
            self.add(RoundedRectangle(width=6.1,height=4.6,corner_radius=.2,color=GREY).move_to([x,.3,0]),
                label('nerve with bare axons' if bare else 'nerve with large axons',x,3.15,BLUE,28))
            for y in [1.3,-.8]:
                self.add(axon_circle([x-1.25,y],.3 if bare else .75))
            cg=VGroup(*[blob([x+1.25,y],1.5,1.15) for y in [1.3,-.8]])
            cells.append(cg); self.add(cg)
        self.add(label('Schwann cells',0,-2.5,PURPLE,30))
        self.at('two laboratories')
        self.play(FadeIn(label('Aguayo laboratory; Weinberg and Spencer, 1970s',0,-3.25,TEXT,28)),run_time=.4)
        self.at('swapped schwann cells')
        a=CurvedArrow([-2.1,2.15,0],[4.6,2.15,0],angle=-.55,color=PURPLE)
        b=CurvedArrow([4.6,-1.65,0],[-2.1,-1.65,0],angle=-.55,color=PURPLE)
        self.play(Create(a),Create(b),cells[0].animate(path_arc=-.8).shift(RIGHT*6.7),cells[1].animate(path_arc=-.8).shift(LEFT*6.7),run_time=1.5)
        self.finish()

class S03Q(SpokenScene):
    def construct(self):
        self.add(moved(),label('Schwann cells from a bare-axon nerve',0,3.2,PURPLE))
        self.at('now meet axons')
        self.play(FadeIn(moved_labels()[1]),run_time=.5)
        self.at('what do they')
        self.play(FadeIn(label('Predict: what do they do?',0,-2,GOLD,36)),run_time=.4)
        self.finish()
class S04Pause(NarratedScene):
    def construct(self):
        self.add(moved(),moved_labels(),choices('the glia decides: cells stay bare','the axon decides: cells wrap',-2.3)); self.finish()
class S05R(SpokenScene):
    def construct(self):
        self.add(moved(),moved_labels())
        self.at('they myelinated')
        self.play(*[Create(spiral([x,.65],1.65,1.18,4)) for x in CENTERS],FadeIn(label('wrapped',0,2.3,PURPLE)),run_time=1.4)
        self.at('the reverse swap')
        self.play(FadeIn(reverse_row(),shift=UP*.25),run_time=.7)
        self.at('the axon decides')
        self.play(FadeIn(label('In peripheral nerve, the axon decides.',0,-3.35,TEXT,36)),run_time=.4); self.finish()
class S06Beat(NarratedScene):
    def construct(self):
        self.add(graft_final()); self.finish()
class S07Signal(SpokenScene):
    def construct(self):
        self.add(signal_base(),label('The axon carries a signal',0,3.2,TEXT,36))
        self.at('the main one')
        self.play(Indicate(self.mobjects[0][0],color=ORANGE),run_time=.4)
        self.at('is')
        self.remove(self.mobjects[1])
        self.play(FadeIn(surface_marks()),FadeIn(signal_labels()[0]),run_time=.65)
        self.at('a protein on')
        self.play(FadeIn(signal_labels()[1]),run_time=.4); self.finish()
class S08Tether(SpokenScene):
    def construct(self):
        mk=surface_marks(); self.add(signal_base(),mk,signal_labels())
        self.at('schwann cell reads')
        process=RoundedRectangle(width=3,height=.8,corner_radius=.25,color=PURPLE,fill_color=PURPLE,fill_opacity=.4).move_to([0,2.1,0])
        tag=label('Schwann cell process',3.85,2.1,PURPLE,28)
        self.play(FadeIn(process),FadeIn(tag),run_time=.45)
        self.at('by touch')
        # The bottom edge meets the protein heads at y=1.06; only these two lie beneath it.
        self.play(process.animate.move_to([0,1.45,0]),
            *[mk[i].animate.set_color(GOLD) for i in [4,5]],run_time=.35)
        self.finish()

# Rose receptors remain distinct from the cyan axon and purple glial membrane.
def receptor(x,lit=False):
    return VGroup(RoundedRectangle(width=1.45,height=2.4,corner_radius=.2,color=ROSE,fill_color=ROSE,fill_opacity=.3).move_to([x,-.6,0]),
        Rectangle(width=.4,height=.6,color=ROSE,fill_color=ROSE,fill_opacity=.7).move_to([x,.85,0]),
        RoundedRectangle(width=2.05,height=1.05,corner_radius=.2,color=GREEN,fill_color=GREEN,fill_opacity=.85 if lit else .08).move_to([x,1.65,0]),
        label('kinase',x,1.65,TEXT,28))
class S09Rec(SpokenScene):
    def construct(self):
        self.add(label('Schwann cell: receptor close-up',0,3.35,PURPLE,32),
            Rectangle(width=12.5,height=.2,color=PURPLE,fill_opacity=.5,fill_color=PURPLE).move_to([0,.85,0]),
            Rectangle(width=12.5,height=.45,color=BLUE,fill_opacity=.25,fill_color=BLUE).move_to([0,-2.95,0]),label('axon membrane',4.3,-3.5,BLUE,26))
        e3=receptor(-2.6); n3=label('ErbB3',-2.6,2.65,ROSE,32)
        ligand=mark([-2.6,-2.72,0],[0,1,0],.75,.16)
        self.at('two receptors')
        self.play(FadeIn(e3),run_time=.45)
        self.at('erb b3')
        bound=label('bound neuregulin',-4.45,-2.05,ORANGE,26)
        self.play(FadeIn(n3),GrowFromPoint(ligand,ligand[0].get_start()),FadeIn(bound),run_time=.45)
        self.at('erb b2')
        e2=receptor(2.6,True); n2=label('ErbB2',2.6,2.65,ROSE,32)
        no=label('no ligand',2.6,-2.05,TEXT,26)
        self.play(FadeIn(e2),FadeIn(n2),FadeIn(no),run_time=.45)
        self.at('paired')
        self.play(e3.animate.shift(RIGHT*1.575),n3.animate.shift(RIGHT*1.575),ligand.animate.shift(RIGHT*1.575),e2.animate.shift(LEFT*1.575),n2.animate.shift(LEFT*1.575),FadeOut(bound),FadeOut(no),run_time=.3)
        self.at('they signal')
        self.play(e3[2].animate.set_fill(GREEN,opacity=.85),e2[2].animate.set_fill(GREEN,opacity=1).set_stroke(GREEN,width=5),GrowArrow(Arrow([2.3,1.65,0],[4.7,1.65,0],color=GREEN)),run_time=.4); self.finish()

class S10Amount(SpokenScene):
    def construct(self):
        self.add(label('same length of axon',0,3.3,TEXT,34))
        # Cylinders: cross sections plus equal axial lengths show membrane area per length.
        groups=[]; marks=[]
        for x,r,name in [(-3.7,1.55,'large axon'),(3.1,.65,'thin axon')]:
            front=axon_circle([x-.6,.3],r)
            back=Circle(radius=r,color=BLUE,fill_color=BLUE,fill_opacity=.1).move_to([x+.6,.9,0])
            lines=VGroup(*[Line([x-.6,.3+s*r,0],[x+.6,.9+s*r,0],color=BLUE) for s in [-1,1]])
            groups.append(VGroup(back,lines,front,label(name,x,-2,BLUE,30)))
            marks.append(marks_ring([x-.6,.3],r,.5,.25,.08))
        self.add(*groups)
        self.at('more membrane')
        self.play(FadeIn(label('one micrometre of axon',0,-2.7,TEXT,28)),run_time=.4)
        self.at('if the density')
        self.play(FadeIn(label('if density is similar',0,2.65,ORANGE,30)),FadeIn(VGroup(*marks)),run_time=.6)
        self.at('carries more')
        self.play(Indicate(marks[0],color=GOLD),run_time=.5)
        self.at('could the amount')
        self.play(FadeIn(label('Could the amount be the message?',0,-3.4,GOLD,34)),run_time=.4); self.finish()
class S11Q1(SpokenScene):
    def construct(self):
        self.add(table(),axon_circle([PX,PY],RAX,'axon',28))
        self.at('give mice half')
        self.play(FadeIn(row_hi(0)),run_time=.4)
        self.at('what happens to')
        self.play(FadeIn(normal_outline()),FadeIn(label('sheath?   g ratio?',PX,2.75,GOLD,30)),FadeIn(label('dashed: normal reference',PX,-2.35,TEXT,26)),run_time=.5); self.finish()
class S12Pause(NarratedScene):
    def construct(self):
        self.add(dose_question(),choices('thinner sheath / higher g?','thicker sheath / lower g?',-2.75)); self.finish()
class S13R1(SpokenScene):
    def construct(self):
        fr=dose_question(); self.add(fr)
        self.at('the sheaths were thinner')
        self.remove(fr[4]); self.play(FadeIn(sheath_ring([PX,PY],RAX,RR['half'])),FadeIn(tcell(0,1,'thinner',PURPLE)),run_time=.75)
        self.at('ratio went up')
        self.play(FadeIn(tcell(0,2,'0.75',GOLD)),FadeIn(label('g = 0.75',PX,2.75,GOLD,34)),FadeIn(dose_notes()),run_time=.5); self.finish()
class S14Q2(SpokenScene):
    def construct(self):
        self.add(dose_question(True)); self.at('predict the sheath'); self.play(Indicate(row_hi(2),color=GOLD),run_time=.5); self.finish()
class S15Pause(NarratedScene):
    def construct(self):
        self.add(dose_question(True),choices('thinner sheath / higher g?','thicker sheath / lower g?',-2.75)); self.finish()
class S16R2(SpokenScene):
    def construct(self):
        fr=dose_question(True); self.add(fr)
        self.at('thicker myelin'); self.remove(fr[4])
        self.play(FadeIn(sheath_ring([PX,PY],RAX,RR['extra'])),FadeIn(tcell(2,1,'thicker',PURPLE)),run_time=.7)
        self.at('lower g ratio')
        self.play(FadeIn(tcell(2,2,'0.55',GOLD)),FadeIn(label('g = 0.55 (illustrative)',PX,2.75,GOLD,28)),run_time=.5)
        self.at('the dose changed')
        self.clear(); self.add(trio())
        self.at('the sheath followed')
        self.play(*[Indicate(m,color=PURPLE,scale_factor=1.04) for m in self.mobjects[0] if isinstance(m,VGroup)],run_time=.6); self.finish()
class S17Beat(NarratedScene):
    def construct(self):
        self.add(trio()); self.finish()
class S18Q3(SpokenScene):
    def construct(self):
        self.add(culture_base())
        self.at('extra type 3')
        self.play(FadeIn(culture_marks()),FadeIn(culture_labels()[0]),run_time=.6)
        self.at('add schwann cells')
        self.play(FadeIn(culture_cells(),shift=DOWN*.3),FadeIn(culture_labels()[1]),run_time=.5)
        self.at('what then')
        self.play(FadeIn(label('What will the cells do?',0,-3.3,GOLD,32)),run_time=.4); self.finish()
class S19Pause(NarratedScene):
    def construct(self):
        self.add(culture_base(),culture_marks(),culture_cells(),culture_labels(),choices('stay bare?', 'wrap the axons?',-2.75)); self.finish()
class S20R3(SpokenScene):
    def construct(self):
        cells=culture_cells(); marks=culture_marks(); self.add(culture_base(),marks,cells,culture_labels())
        self.at('the schwann cells myelinated')
        self.play(*[ReplacementTransform(c,spiral([x,CULT_Y],1.18,.73,4)) for c,x in zip(cells,CULT_X)],FadeOut(marks),run_time=1.1)
        self.play(FadeIn(label('myelinated • Taveggia et al., Salzer laboratory, 2005',0,-3.3,TEXT,28)),run_time=.3); self.finish()
class S21Instr(SpokenScene):
    def construct(self):
        fr=comparison(False); self.add(fr)
        self.at('changed what the glia')
        self.play(ReplacementTransform(fr[-2],spiral([3.4,-.3],1.45,.88,4)),FadeOut(fr[-1]),run_time=.8)
        self.at('the outcome followed')
        self.play(FadeIn(label('wrapped axons',3.4,-2.05,PURPLE,28)),FadeIn(label('The outcome followed the delivery.',0,-3.3,TEXT,36)),run_time=.5); self.finish()
class S22Link(SpokenScene):
    def construct(self):
        self.add(comparison().scale(.75).move_to([0,.85,0]))
        self.at('instructive')
        self.play(FadeIn(label('type III is instructive',0,3.25,GOLD,42)),run_time=.4)
        self.at('same permissive')
        factor=chip('supply factor',ORANGE,26).move_to([-4.7,-2.15,0])
        outcome=chip('outcome changes?',GOLD,26).move_to([-.5,-2.15,0])
        test=VGroup(factor,outcome,
            Arrow(factor.get_right(),outcome.get_left(),buff=.12,color=TEXT),
            label('yes → instructive',4.2,-1.85,GOLD,26),
            label('no → permissive?',4.2,-2.5,TEXT,26),
            Arrow([1.6,-2.15,0],[2.65,-2.15,0],buff=.12,color=TEXT))
        self.play(FadeIn(test),run_time=.4)
        self.at('neurotrophic hypothesis')
        self.play(FadeIn(label('neurotrophic hypothesis lesson',0,-3.3,TEXT,28)),run_time=.4); self.finish()
class S23Rule(SpokenScene):
    def construct(self):
        dc=np.array([-3.6,.15,0]); angle=lambda v:np.radians(225-270*v)
        def point(v,r): return dc+r*np.array([np.cos(angle(v)),np.sin(angle(v)),0])
        dial=Arc(radius=2.5,start_angle=angle(0),angle=-1.5*PI,arc_center=dc,color=GREY,stroke_width=5)
        self.add(dial,label('type III dose',-3.6,-2.7,ORANGE,32),label('low',-5.55,-2,TEXT,26),label('high',-1.65,-2,TEXT,26),
            Line(point(.5,2.3),point(.5,2.7),color=GOLD,stroke_width=6),label('threshold',-3.6,3.25,GOLD,30),axon_circle([3.5,.1],1.35))
        needle=Line(dc,point(.2,2.15),color=ORANGE,stroke_width=7); self.add(needle)
        bare=label('bare',3.5,-2.8,BLUE,34)
        self.at('an axon stays bare'); self.play(FadeIn(bare),run_time=.3)
        self.at('above it'); self.remove(bare)
        thin=sheath_ring([3.5,.1],1.35,1.55)
        self.play(Transform(needle,Line(dc,point(.6,2.15),color=ORANGE,stroke_width=7)),FadeIn(thin),run_time=.45)
        self.at('helps thicken')
        self.play(Transform(needle,Line(dc,point(.95,2.15),color=ORANGE,stroke_width=7)),Transform(thin,sheath_ring([3.5,.1],1.35,2.3)),FadeIn(label('thicker sheath',3.5,-2.8,PURPLE,32)),run_time=.8); self.finish()
class S24Match(SpokenScene):
    def construct(self):
        self.add(label('a proposal',0,3.35,GOLD,40),label('illustrative: g = 0.65; 17 nm per turn',0,-3.4,TEXT,28))
        rings=VGroup(); mk=VGroup()
        # Shared physical scale. Turn counts derive from t=(D/g-D)/2, at 17 nm/turn.
        for D,x in [(2,-5.1),(5,-1.8),(10,3.4)]:
            r=D*.135; n=round((D/.65-D)/2/.017)
            self.add(axon_circle([x,.3],r),label(f'{D} µm',x,-2.2,BLUE,30),label(f'about {n} turns',x,-2.8,PURPLE,28))
            sheath=sheath_ring([x,.3],r,r/.65)
            sheath[0].set_fill(PURPLE,opacity=.65).set_stroke(PURPLE,width=4)
            sheath[2].set_stroke(PURPLE,width=2.5,opacity=1)
            rings.add(sheath); mk.add(marks_ring([x,.3],r,.4,.19,.065))
        self.add(mk.set_z_index(5))
        self.at('one readout could')
        self.play(*[FadeIn(r) for r in rings],run_time=1.1)
        self.at('that is a proposal')
        self.play(FadeIn(label('not yet shown',0,2.65,GOLD,30)),run_time=.4); self.finish()
class S25Perm(SpokenScene):
    def construct(self):
        cell=Ellipse(width=11.2,height=5.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.15).move_to([0,-.15,0])
        ax=axon_circle([-2.7,-.15],1.15); mk=marks_ring([-2.7,-.15],1.15,.5,.28,.09).set_z_index(4)
        self.add(cell,ax,mk,label('Schwann cell',1.9,1.5,PURPLE,32),label('type III: decisive',-3.25,-3.35,ORANGE,30))
        self.at('not enough alone')
        self.play(Indicate(mk,color=ORANGE),run_time=.5)
        self.at('basal lamina')
        lam=Ellipse(width=12.4,height=6.2,color=TAN,stroke_width=6).move_to([0,-.15,0])
        self.play(Create(lam),FadeIn(label('basal lamina • required',0,3.35,TAN,30)),run_time=.65)
        self.at('its own receptor')
        rx=chip('Gpr126',TEAL,30).move_to([2.5,-1.1,0]); self.play(FadeIn(rx),run_time=.5)
        self.at('gpr126')
        self.play(GrowArrow(Arrow([2.5,-.65,0],[2.5,.25,0],buff=0,color=GREEN)),FadeIn(chip('cAMP',GREEN,30).move_to([2.5,.65,0])),run_time=.65)
        self.at('both are required')
        self.play(FadeIn(label('required',2.5,-1.9,TAN,30)),run_time=.4)
        self.at('also tunes')
        arrow=Arrow([-5.7,1.3,0],[-3.45,.95,0],buff=0,color=TAN,stroke_width=6)
        self.play(GrowArrow(arrow),FadeIn(label('tunes response',0,-2.2,TAN,28)),run_time=.7); self.finish()
class S26Take(SpokenScene):
    def construct(self):
        self.add(label('In nerve, the axon sets the dose,',0,2.6,TEXT,42),axon_circle([0,-1],1.25))
        self.at('and the dose is')
        self.play(FadeIn(label('and the dose is the main signal for the wrap.',0,1.6,GOLD,38)),run_time=.4)
        self.at('the wrap')
        self.play(Create(spiral([0,-1],1.95,1.28,5)),FadeIn(marks_ring([0,-1],1.25,.5,.25,.08).set_z_index(5)),run_time=.65); self.finish()
class S27End(EndCard):
    LINE='In nerve, the axon sets the dose.'
