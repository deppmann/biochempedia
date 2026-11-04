"""Brains in a Dish, chapter 2: Measured Against Fetal Cortex  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film; shared with chapter 1 where the concept recurs)
  YELLOW = oxygen (the reprogramming factors of chapter 1 do not appear here)
  BLUE   = radial glia
  PURPLE = intermediate progenitors
  GREEN  = neurons
  TEAL   = a match: the bands that join like with like (stem cells of chapter 1 do not appear here)
  RED    = limits: no oxygen, dying cells, stress genes, blurred identity
  AMBER  = the rule (blood is surroundings; where to look first); also "assumed" numbers
  PINK   = blood vessels (capillaries)
  WHITE  = cells and nuclei (TEXT colour)
  GREY   = outlines, tissue, dish, membrane, structure, dead cells
  GOLD   = title rule only

Every oxygen curve and every shaded oxygen gradient below is computed from the lesson's own equations:
  steady-state ball, uniform oxygen use Q, surface level C0, D = 2e-9 m2/s, radius 2 mm:
  C(r) = C0 + Q/(6D) (r^2 - R^2) + Q b^3/(3D) (1/r - 1/R)  outside an oxygen-free core of radius b,
  with C0 = Q (R^2 - 3 b^2 + 2 b^3 / R) / (6 D).
  thin shell: C0 = 100 uM, Q = 0.026 mol/m3/s (0.13 mm).  thick shell: C0 = 200 uM, Q = a tenth (0.62 mm).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AMBER = "#F2B134"
PINK = "#E889B5"
CORE_DARK = "#161A22"
CELL_FILL = "#0f1117"

# ---------------------------------------------------------------------------------------------
# the oxygen model (from the lesson)
# ---------------------------------------------------------------------------------------------
_D, _Q0, _RM = 2e-9, 0.026, 2e-3
CASES = {"thick": (200.0, 0.1), "thin": (100.0, 1.0)}   # (C0 in uM, fraction of the adult brain's use)


def shell_model(case):
    C0u, qf = CASES[case]
    C0, Q, D, R = C0u * 1e-3, _Q0 * qf, _D, _RM
    f = lambda b: Q * (R * R - 3 * b * b + 2 * b ** 3 / R) / (6 * D) - C0
    lo, hi = 0.0, R
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if f(m) > 0 else (lo, m)
    b = (lo + hi) / 2

    def C(r):  # mol/m3, for b <= r <= R
        return max(0.0, C0 + Q / (6 * D) * (r * r - R * R) + Q * b ** 3 / (3 * D) * (1 / r - 1 / R))
    return b, C


def oxy_rings(c, R, case, n=14):
    """Concentric discs shaded by the computed oxygen level, ending in a dark oxygen-free core."""
    b, C = shell_model(case)
    bf = b / _RM
    g = VGroup()
    for k in range(n):
        r0 = 1 - (1 - bf) * k / n
        r1 = 1 - (1 - bf) * (k + 1) / n
        rm = (r0 + r1) / 2
        level = min(1.0, C(rm * _RM) * 1e3 / 200.0)
        col = interpolate_color(ManimColor(CORE_DARK), ManimColor(YELLOW), 0.85 * level ** 0.75)
        g.add(Annulus(inner_radius=max(0.01, (r1 - 0.012) * R), outer_radius=r0 * R, stroke_width=0, fill_color=col, fill_opacity=1).move_to(c))
    g.add(Circle(radius=bf * R, stroke_width=0, fill_color=CORE_DARK, fill_opacity=1).move_to(c))
    return g.set_z_index(1)


CORE_FRAC = {k: shell_model(k)[0] / _RM for k in CASES}   # thick 0.69, thin 0.94


# ---------------------------------------------------------------------------------------------
# the organoid ball: tissue disc, oxygen shading, cells, outline
# ---------------------------------------------------------------------------------------------
def _poisson(seed, n, min_d, rad=0.93):
    rng = np.random.default_rng(seed)
    pts, tries = [], 0
    while len(pts) < n and tries < 30000:
        p = rng.uniform(-1, 1, 2)
        if np.linalg.norm(p) <= rad and all(np.linalg.norm(p - q) >= min_d for q in pts):
            pts.append(p)
        tries += 1
    return np.array(pts)


UNIT_CELLS = _poisson(7, 150, 0.165)
_rng = np.random.default_rng(11)
FRAG = _rng.uniform(-1.7, 1.7, (len(UNIT_CELLS), 3, 3))
FRAG[:, :, 2] = 0


def make_cells(c, R, dead=False, cf=None):
    cf = CORE_FRAC["thin"] if cf is None else cf
    cr = 0.05 * R
    g = VGroup()
    for i, (ux, uy) in enumerate(UNIT_CELLS):
        pos = np.array(c, float) + R * np.array([ux, uy, 0])
        if dead and np.hypot(ux, uy) < cf - 0.05:
            g.add(VGroup(*[Circle(radius=cr * 0.34, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.5)
                           .move_to(pos + cr * FRAG[i][j]) for j in range(3)]))
        else:
            g.add(Circle(radius=cr, stroke_color=TEXT, stroke_width=1.6, fill_color=CELL_FILL, fill_opacity=0.5)
                  .set_stroke(opacity=0.85).move_to(pos))
    return g.set_z_index(3)


def core_idx(cf=None):
    cf = CORE_FRAC["thin"] if cf is None else cf
    return [i for i, (ux, uy) in enumerate(UNIT_CELLS) if np.hypot(ux, uy) < cf - 0.05]


class Sph:
    def __init__(self, center, R=2.5, case=None, dead=False):
        self.c = np.array(center, float)
        self.R = R
        self.base = Circle(radius=R, stroke_width=0, fill_color=GREY, fill_opacity=0.16).move_to(self.c).set_z_index(0)
        self.rings = oxy_rings(self.c, R, case) if case else VGroup()
        self.cells = make_cells(self.c, R, dead)
        self.outline = Circle(radius=R, stroke_color=GREY, stroke_width=4).move_to(self.c).set_z_index(4)
        self.group = VGroup(self.base, self.rings, self.cells, self.outline)

    def pt(self, ang_deg, rfrac):
        a = np.radians(ang_deg)
        return self.c + self.R * rfrac * np.array([np.cos(a), np.sin(a), 0])


def oxygen_dots(sph, n=18, seed=3, r_lo=0.12, r_hi=0.6):
    """oxygen dots around the ball: returns (dots at start radius, final positions on the surface)."""
    rng = np.random.default_rng(seed)
    dots, finals = VGroup(), []
    for i in range(n):
        a = TAU * i / n + rng.uniform(-0.12, 0.12)
        r0 = sph.R + rng.uniform(r_lo + 0.2, r_hi)
        d = Circle(radius=0.085, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
        d.move_to(sph.c + r0 * np.array([np.cos(a), np.sin(a), 0]))
        dots.add(d)
        finals.append(sph.c + (sph.R + 0.13) * np.array([np.cos(a), np.sin(a), 0]))
    return dots.set_z_index(6), finals


def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dash_ring(c, r, color=RED, w=4, n=40):
    return DashedVMobject(Circle(radius=r, stroke_color=color, stroke_width=w), num_dashes=n).move_to(c).set_z_index(5)


# positions shared between scenes
SC_C = np.array([0.0, -0.3, 0.0])      # ball centred
SC_L = np.array([-3.1, -0.5, 0.0])     # ball at left (with a panel on the right)
R_B = 2.5


# ---------------------------------------------------------------------------------------------
# frames that more than one scene needs (the end frame of a scene is rebuilt by its successor)
# ---------------------------------------------------------------------------------------------
# All labels are >=26 pt; illustrative expression bars are explicitly schematic.
# Override only logging: render intermediates live in /tmp, not beside the final artifacts.
_BaseSpoken = SpokenScene
class SpokenScene(_BaseSpoken):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


def label(lines, x, y, size=30, color=TEXT, gap=0.12):
    if isinstance(lines, str):
        lines = [lines]
    return VGroup(*[T(t, size, color) for t in lines]).arrange(DOWN, buff=gap).move_to([x,y,0])


def core_hatch(c, radius):
    g = VGroup(Circle(radius=radius, stroke_width=0, fill_color='#080B12', fill_opacity=1).move_to(c))
    for y in np.arange(-radius+0.12, radius, 0.24):
        dx = np.sqrt(max(0, radius**2-y**2))
        g.add(Line(c+np.array([-dx,y,0]), c+np.array([dx,y,0]), color='#768397', stroke_width=2, stroke_opacity=0.8))
    g.add(Circle(radius=radius, stroke_color=RED, stroke_width=3, fill_opacity=0).move_to(c))
    return g.set_z_index(2)


def ball(c=SC_C, case='thin', dead=False, radius=R_B, cells=True):
    sph = Sph(c, radius, case, dead)
    shade = core_hatch(np.array(c), CORE_FRAC[case]*radius)
    sph.group.add(shade)
    if not cells:
        sph.cells.set_opacity(0)
    return sph


def no_blood():
    center = np.array([-4.45,0.3,0])
    tube = RoundedRectangle(width=1.7,height=0.55,corner_radius=0.2,stroke_color=PINK,fill_color=PINK,fill_opacity=0.2).move_to(center)
    cross = VGroup(Line(center+[-0.65,0.5,0],center+[0.65,-0.5,0],color=RED,stroke_width=6),Line(center+[-0.65,-0.5,0],center+[0.65,0.5,0],color=RED,stroke_width=6))
    return VGroup(tube,cross,label('no blood',-4.45,-0.65,32))


def question(sc):
    sph = Sph(SC_C)
    dots, ends = oxygen_dots(sph)
    for d,p in zip(dots,ends): d.move_to(p)
    ox = label('oxygen',4.5,1.25,32,YELLOW)
    arrow = arr([3.7,1.2,0], ends[1],YELLOW)
    q = label('What happens at the center?',0,3.05,38)
    backing=Circle(radius=.48,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(SC_C).set_z_index(7)
    qm = T('?',90,AMBER).move_to(SC_C).set_z_index(8)
    sc.add(backing)
    sc.add(sph.group,dots,no_blood(),ox,arrow,q,qm)
    return sph,dots


class S00Title(TitleCard):
    LESSON = 'Brains in a Dish: Stem Cells and Organoids'
    TITLE = 'Measured Against Fetal Cortex'
    def construct(self):
        g = VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28),label(['Measured Against','Fetal Cortex'],0,0,56),Line(LEFT*2,RIGHT*2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=0.4)
        self.play(FadeIn(g),run_time=0.35)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        sph=Sph(SC_C); self.add(sph.group)
        self.at('no blood'); self.play(FadeIn(no_blood()),run_time=0.35)
        dots,ends=oxygen_dots(sph)
        ox=label('oxygen',4.5,1.25,32,YELLOW)
        a=arr([3.7,1.2,0],ends[1],YELLOW)
        self.at('Every bit'); self.play(FadeIn(dots),FadeIn(ox),GrowArrow(a),run_time=0.45)
        self.at('diffuse in'); self.play(*[d.animate.move_to(p) for d,p in zip(dots,ends)],run_time=0.7)
        self.at('What happens'); self.add(Circle(radius=.48,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(SC_C).set_z_index(7)); self.play(FadeIn(label('What happens at the center?',0,3.05,38)),FadeIn(T('?',90,AMBER).move_to(SC_C).set_z_index(8)),run_time=0.4)
        self.finish()


class S02Pause(NarratedScene):
    def construct(self):
        question(self); self.finish()


class S03Use(SpokenScene):
    def construct(self):
        sph=Sph(SC_C); dots,ends=oxygen_dots(sph)
        for d,p in zip(dots,ends): d.move_to(p)
        self.add(sph.group,dots,label('oxygen is used as it moves inward',0,3.1,32,YELLOW))
        self.at('use oxygen')
        # Generous shell: computed 0.62 mm (31% of the 2 mm radius).
        target=ball(case='thick')
        self.play(FadeIn(target.rings),FadeIn(target.group[-1]),run_time=0.55)
        self.at('moves inward')
        self.play(*[d.animate.move_to(SC_C+(p-SC_C)*0.78).set_opacity(0) for d,p in zip(dots,ends)],run_time=0.6)
        # Two exact model endpoints on a single radius; labels sit outside the tissue.
        for case,y in [('thin',1.15),('thick',-1.0)]:
            end=SC_C+RIGHT*R_B*CORE_FRAC[case]
            a=Line(end,SC_C+RIGHT*R_B,color=AMBER,stroke_width=5).set_z_index(7)
            name='0.1 mm' if case=='thin' else '0.6 mm'
            l=label([name,'from surface'],4.4,y,28,AMBER)
            leader=Line([3.1,y,0],end,color=AMBER,stroke_width=2).set_z_index(7)
            tick=Line(end+UP*.12,end+DOWN*.12,color=AMBER,stroke_width=3).set_z_index(7)
            self.add(a,l,leader,tick)
        self.at('runs out'); self.play(FadeIn(label('2 mm radius; model range',0,-3.3,28)),run_time=0.3)
        self.finish()


# Large oxygen plot: 5.5 of 8 frame units high, model assumptions always visible.
PX0,PX1,PY0,PY1=-5.65,1.65,-2.65,2.85
DMAX,CMAX=0.7,220

def pp(d,c): return np.array([PX0+d/DMAX*(PX1-PX0),PY0+c/CMAX*(PY1-PY0),0])

def curve(case):
    b,C=shell_model(case)
    rs=np.linspace(_RM,b,140)
    return VMobject(color=YELLOW,stroke_width=6).set_points_as_corners([pp((_RM-r)*1e3,C(r)*1e3) for r in rs]),(_RM-b)*1e3


class S04Depth(SpokenScene):
    def construct(self):
        self.add(Line(pp(0,0),pp(.7,0),color=TEXT),Line(pp(0,0),pp(0,220),color=TEXT))
        for d in [0,.2,.4,.6]: self.add(label(f'{d:g}',pp(d,0)[0],-2.98,26))
        for c in [0,100,200]: self.add(label(str(c),-6.15,pp(0,c)[1],26))
        self.add(label('oxygen (µM)',-4.75,3.35,28),label('depth below surface (mm)',-2,-3.45,28))
        self.add(label(['ASSUMPTIONS','uniform tissue','steady state','surface: 100–200 µM','use: adult rate to 1/10','(both assumed)'],4.35,1.25,26,AMBER,gap=.2),label(['Model numbers,','not measurements'],4.35,-2.3,28,RED))
        # Full-brightness model traces remain legible throughout the assumptions.
        deep,dd=curve('thick'); shallow,ds=curve('thin')
        self.add(deep,shallow)
        dl=label(['surface 200 µM,','low use'],-.7,2.15,27,YELLOW)
        sl=label(['surface','100 µM,','high use'],-4.1,-.95,26,YELLOW)
        _,deepC=shell_model('thick'); _,thinC=shell_model('thin')
        self.add(dl,sl,
                 Line([-1.65,1.7,0],pp(.14,deepC(_RM-.14e-3)*1e3),color=YELLOW,stroke_width=2),
                 Line([-4.95,-.95,0],pp(.045,thinC(_RM-.045e-3)*1e3),color=YELLOW,stroke_width=2))
        self.at('oxygen reaches')
        self.play(FadeIn(label('about 0.1 to 0.6 mm',-1,3.35,28,AMBER)),run_time=.3)
        # Plain-word cues with offsets match the fixed digit tokens in the alignment.
        self.at('only about')
        self.play(Indicate(shallow,scale_factor=1,color=YELLOW),run_time=.45)
        self.add(Dot(pp(ds,0),color=RED),label('about 0.1 mm',-3.4,-1.95,27,RED),Line([-3.4,-2.2,0],pp(ds,0),color=RED,stroke_width=2))
        self.at('to')
        self.play(Indicate(deep,scale_factor=1,color=YELLOW),run_time=.45)
        self.add(Dot(pp(dd,0),color=RED),label('about 0.6 mm',.15,-1.65,27,RED),Line([.15,-1.9,0],pp(dd,0),color=RED,stroke_width=2))
        self.finish()


def estimate(sc, rule=False):
    c=np.array([-2.4,-.25,0]); sph=ball(c,case='thin',cells=False)
    sc.add(sph.group)
    sc.add(label('up to about 4 mm across',-2.4,3.15,30),DoubleArrow([-4.9,2.55,0],[.1,2.55,0],buff=0,color=TEXT))
    for case,y,lines in [('thin',.65,['about 4/5 of the volume','oxygen reaches 0.1 mm']),('thick',-1.85,['about 1/3 of the volume','oxygen reaches 0.6 mm'])]:
        r=R_B*CORE_FRAC[case]
        sc.add(dash_ring(c,r,RED,7 if case=='thin' else 4,n=32))
        p=c+r*np.array([np.cos(.25 if case=='thin' else -.55),np.sin(.25 if case=='thin' else -.55),0])
        sc.add(label(lines,3.55,y,28,RED),Line(p,[1.25,y,0],color=RED,stroke_width=2).set_z_index(8))
    sc.add(label('oxygen-free core (model)',-2.4,-3.15,30,RED))
    if not rule: sc.add(label('NO OXYGEN IN THIS MODEL',3.45,2.35,27))
    return sph


class S05Size(SpokenScene):
    def construct(self):
        sph=estimate(self)
        self.at('In this model'); self.play(Indicate(sph.group[-1],color=RED,scale_factor=1),run_time=.5)
        self.finish()


class S06Dies(SpokenScene):
    def construct(self):
        sph=ball(); self.add(sph.group,label('cells in the core die',0,3.15,36,RED))
        idx=core_idx()
        self.at('cells in the'); self.play(*[sph.cells[i].animate.set_color(GREY).set_fill(GREY,.65) for i in idx],run_time=.6)
        self.at('center of'); dead=make_cells(SC_C,R_B,True)
        self.play(*[Transform(sph.cells[i],dead[i]) for i in idx],run_time=.7)
        self.finish()


class S07Cortex(SpokenScene):
    def construct(self):
        sph=ball([-3.7,-.3,0],radius=2.25,dead=True)
        self.add(sph.group,label(['organoid: up to','about 4 mm'], -3.7,2.85,30),label('adult cortex (magnified)',3.1,3.1,30))
        panel=Rectangle(width=5.5,height=5.3,color=GREY).move_to([3.1,-.1,0]); self.add(panel)
        vessels=VGroup(*[Line([x,-2.55,0],[x,2.45,0],color=PINK,stroke_width=10) for x in [1.3,3.1,4.9]])
        cells=VGroup(*[dot([x,y,0],TEXT,.12) for x in [1.9,2.4,3.8,4.3,5.4] for y in [-2,-1,0,1,2]])
        self.add(cells)
        self.at('capillaries sit'); self.play(Create(vessels),run_time=.5)
        self.add(label('capillary',4.0,1.7,28,PINK),Line([4.3,1.4,0],[4.9,.8,0],color=PINK))
        self.at('tens of'); self.add(DoubleArrow([1.3,-2.9,0],[3.1,-2.9,0],buff=0,color=AMBER),label('tens of micrometres apart',3.1,-3.4,28,AMBER))
        self.finish()


class S08Spin(SpokenScene):
    def construct(self):
        sph=ball(dead=True); self.add(sph.group,label('faster spinning',0,3.25,36))
        arcs=VGroup(*[Arc(radius=2.85,start_angle=s,angle=1.1,arc_center=SC_C,color=GREY,stroke_width=6).add_tip(tip_length=.22) for s in [0,PI]])
        self.add(arcs)
        self.at('Faster spinning'); self.play(Rotate(arcs,TAU,about_point=SC_C),run_time=1.7)
        self.at('keeps the surface'); self.add(label(['only the surface','improves'],-4.85,.6,28,YELLOW))
        self.play(sph.outline.animate.set_color(YELLOW),Rotate(arcs,TAU,about_point=SC_C),run_time=1.0)
        self.at('cannot feed'); self.add(label(['deep core:','no oxygen'],4.9,-.2,30,RED))
        # Leader stays within the lower right arc's open quadrant.
        self.add(Line([3.5,-1,0],[1.15,-1,0],color=RED,stroke_width=3).set_z_index(8))
        self.finish()


def interface(sc, complete=True):
    sph=ball([-3.8,-.3,0],radius=2.1,dead=True); sc.add(sph.group)
    sc.add(label('shorter diffusion path',-3.8,2.7,30,YELLOW))
    slice_=RoundedRectangle(width=5.5,height=.85,corner_radius=.12,color=TEXT,fill_color=YELLOW,fill_opacity=.65).move_to([3.15,.25,0])
    cells=VGroup(*[dot([1+i*.52,.25,0],TEXT,.12) for i in range(9)])
    membrane=Line([.4,-.25,0],[5.9,-.25,0],color=TEXT,stroke_width=6)
    ml=label('membrane',4.7,-.85,28); lead=Line([4.7,-.6,0],[4.7,-.25,0],color=TEXT)
    liquid=Rectangle(width=5.5,height=2.2,stroke_width=0,fill_color=BLUE,fill_opacity=.16).move_to([3.15,-1.4,0])
    ll=label('liquid',2.1,-1.55,32)
    air=label('air',3.15,3,32)
    arrows=VGroup(*[arr([x,2.3,0],[x,.32,0],YELLOW,4) for x in [1.26,4.9]])
    ox=label('oxygen',3.15,2.55,28,YELLOW)
    objs=dict(slice=VGroup(slice_,cells,label('thin organoid slice',3.15,1.2,28)),layout=VGroup(liquid,membrane,ml,lead,ll,air,arrows,ox))
    if complete: sc.add(objs['layout'],objs['slice'])
    return objs


class S09Path(SpokenScene):
    def construct(self):
        o=interface(self,False)
        self.at('Slice the'); self.play(FadeIn(o['slice']),run_time=.35)
        self.at('grow it'); self.play(FadeIn(o['layout']),run_time=.4)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self): interface(self); self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        # Two labelled model rings remain visible beside the rule.
        estimate(self,True)
        rule=label(['cells bring the program;','the embryo brings the surroundings'],0,3.15,28,AMBER)
        # Move the diameter annotation out of the rule's space.
        for m in list(self.mobjects):
            if m.get_center()[1]>2.4: self.remove(m)
        self.add(rule,label('blood = surroundings',3.45,2.05,30,AMBER))
        self.at('The rule flags'); self.play(FadeIn(label('flagged to fail',3.45,1.45,30,RED)),run_time=.3)
        self.at('the estimate'); self.play(Indicate(self.mobjects[0],scale_factor=1,color=RED),run_time=.4)
        self.finish()


# Stable column positions from the question through the comparison scenes.
COLX=(-4.0,4.0); ROWS=(1.65,0,-1.65); CLASS_COL=(BLUE,PURPLE,GREEN)
CLASS_NAME=('radial glia','intermediate progenitors','neurons')


def dot(p,color=TEXT,r=.095,op=.55):
    return Circle(radius=r,color=color,stroke_width=2,fill_color=color,fill_opacity=op).move_to(p)


def panel(sc):
    for x,name in zip(COLX,['organoid','fetal cortex']):
        sc.add(RoundedRectangle(width=4.3,height=5.5,corner_radius=.2,color=GREY,stroke_width=2).move_to([x,0,0]),label(name,x,3.2,34))


def positions(x,k,n=18,rx=1.3,ry=.5):
    return [np.array([x+rx*np.sqrt((i+.5)/n)*np.cos(i*2.4),ROWS[k]+ry*np.sqrt((i+.5)/n)*np.sin(i*2.4),0]) for i in range(n)]


def clusters(x,counts=(18,18,18)):
    g=VGroup()
    for k,n in enumerate(counts):
        c=VGroup(*[dot(p,CLASS_COL[k],.08) for p in positions(x,k,n,rx=1.25*np.sqrt(n/24))])
        c.add(T(str(k+1),28,CLASS_COL[k]).move_to([x-1.7,ROWS[k],0]))
        g.add(c)
    return g


def neutral(x,seed):
    rng=np.random.default_rng(seed)
    return VGroup(*[dot([x+rng.uniform(-1.7,1.7),rng.uniform(-2.3,2.3),0]) for _ in range(45)])


def broad(sc,bands=True):
    panel(sc); groups=[clusters(COLX[0],(27,12,16)),clusters(COLX[1],(12,20,29))]
    sc.add(*groups)
    lines=VGroup(*[Line([-1.82,y,0],[1.82,y,0],color=TEAL,stroke_width=7,stroke_opacity=.65) for y in ROWS])
    names=VGroup(*[label(['intermediate','progenitors'] if k==1 else CLASS_NAME[k],0,ROWS[k]+(.65 if k==1 else .42),27,CLASS_COL[k],gap=.06) for k in range(3)])
    if bands: sc.add(lines,names)
    return groups,lines,names


class S12Q2(SpokenScene):
    def construct(self):
        panel(self); dots=[neutral(x,20+i) for i,x in enumerate(COLX)]
        self.add(*dots,T('?',110,AMBER))
        self.at('cell by cell'); self.play(*[d[0].animate.scale(1.5) for d in dots],run_time=.4)
        self.finish()


class S13How1(SpokenScene):
    def construct(self):
        self.add(label('single-cell RNA sequencing',0,3.1,38),label('one cell at a time',-4.6,.6,28),label('one bar per gene',3.7,1.9,30),label('messenger RNA counts',3.7,-2.9,28))
        box=RoundedRectangle(width=2.5,height=4.4,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.12).move_to([-1.1,-.2,0])
        self.add(box,label(['RNA','counter'],-1.1,1.0,30,TEAL),Line([-2.3,-.4,0],[.1,-.4,0],color=TEXT,stroke_width=4))
        cells=VGroup(*[dot([-3.5-i*.75,-.4,0],TEXT,.2) for i in range(3)])
        self.add(cells)
        self.add(label('schematic profiles',3.7,-2.25,27,AMBER))
        for i,phrase in enumerate(['Single cell','sequencing counts','thousands of']):
            self.at(phrase)
            self.play(cells[i].animate.move_to([-1.1,-.4,0]),run_time=.65)
            self.wait(.2)
            # Each cell becomes exactly one schematic profile at the outlet.
            counts=[3,8,2,5,9,4,7,2,6,4,8,3]
            row=VGroup(*[Rectangle(width=.19,height=.07*counts[(j+i)%12],stroke_width=0,fill_color=TEXT,fill_opacity=1).move_to([1.5+j*.36,.75-i*1.15+.035*counts[(j+i)%12],0]) for j in range(12)])
            source=row.copy().scale(.22).move_to([.3,-.4,0])
            self.play(ReplacementTransform(cells[i],source),run_time=.3)
            self.play(Transform(source,row),run_time=.55)
        self.finish()


class S14How2(SpokenScene):
    def construct(self):
        panel(self); dots=[neutral(x,20+i) for i,x in enumerate(COLX)]; self.add(*dots)
        self.at('similar profiles'); self.play(*[d.animate.set_color(CLASS_COL[i%3]) for g in dots for i,d in enumerate(g)],run_time=.5)
        self.at('grouped into')
        targets=[clusters(x) for x in COLX]
        self.play(*[FadeTransform(d,t) for d,t in zip(dots,targets)],run_time=.6)
        self.add(label('cluster = cells with similar profiles',0,-3.25,28))
        self.at('Then each')
        lines=VGroup(*[Line([-1.82,ya,0],[1.82,yb,0],color=TEAL,stroke_width=2,stroke_opacity=.55) for ya in ROWS for yb in ROWS])
        self.play(Create(lines),FadeIn(label('compare',0,2.6,30,TEAL)),run_time=.6)
        self.finish()


class S15Who(SpokenScene):
    def construct(self):
        # A dedicated credit card leaves no cluster borders or row numbers behind it.
        card=RoundedRectangle(width=10.5,height=5.6,corner_radius=.2,color=TEAL,fill_color=BG,fill_opacity=1)
        credit=label(['2020','Aparna Bhaduri and colleagues'],0,1.55,34,TEAL,gap=.35)
        self.add(card,credit)
        self.at('compared hundreds')
        self.play(FadeIn(label(['about 235,000 organoid cells','37 organoids','about 189,000 fetal cortex cells'],0,-.85,30,gap=.4)),run_time=.4)
        self.finish()


class S16Broad(SpokenScene):
    def construct(self):
        groups,lines,names=broad(self,False)
        for k,phrase in enumerate(['radial glia','intermediate progenitors','and neurons']):
            self.at(phrase); self.play(Create(lines[k]),FadeIn(names[k]),run_time=.4)
        self.at('Those are'); self.add(label('broad classes recognizable; proportions can differ',0,-3.1,28))
        self.at('program features'); self.add(label('program features',0,-3.6,28,AMBER))
        self.finish()


def sub_frame(sc):
    panel(sc)
    org=VGroup(*[dot(p,GREEN,.095) for p in positions(-4,1,24)])
    subs=VGroup(*[VGroup(*[dot(p,GREEN,.08) for p in positions(4,k,24)],T(s,30,GREEN).move_to([5.7,ROWS[k],0])) for k,s in enumerate('ABC')])
    sc.add(org,subs,label('fetal subtypes A, B, C',4,-3.25,28),label('organoid cluster',-4,-3.25,28))
    beams=VGroup(*[Line([-1.82,0,0],[1.82,y,0],color=TEAL,stroke_width=8,stroke_opacity=.6) for y in ROWS])
    return beams


class S17Sub(SpokenScene):
    def construct(self):
        beams=sub_frame(self)
        self.add(label('identity blurred',0,2.65,32,RED))
        self.at('An organoid cluster'); self.play(FadeIn(beams),run_time=.5)
        self.finish()


def satb(sc):
    panel(sc)
    sc.add(label(['cells with SATB2','(schematic)'],0,2.8,28,GREEN),label('upper-layer neurons',0,-3.3,30))
    bars=VGroup()
    for x,h in zip(COLX,[.85,4.25]):
        sc.add(Line([x-1.4,-2.3,0],[x+1.4,-2.3,0],color=TEXT))
        bars.add(Rectangle(width=1.5,height=h,color=GREEN,fill_color=GREEN,fill_opacity=.6).move_to([x,-2.3+h/2,0]))
    sc.add(bars)
    return bars


class S18Satb2(SpokenScene):
    def construct(self):
        bars=satb(self)
        self.at('much rarer'); self.play(Indicate(bars[0],color=GREEN,scale_factor=1.1),run_time=.4)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self): satb(self); self.finish()


def meter(frac,x,y0=-2.65,h=5.5,w=1.2):
    tube=RoundedRectangle(width=w,height=h,corner_radius=.12,color=TEXT,stroke_width=3).move_to([x,y0+h/2,0])
    fh=(h-.16)*frac
    fill=Rectangle(width=w-.16,height=fh,stroke_width=0,fill_color=RED,fill_opacity=.85).move_to([x,y0+.08+fh/2,0])
    return VGroup(tube,fill)


class S20Stress(SpokenScene):
    def construct(self):
        self.add(label('stress genes (schematic)',0,3.35,36,RED))
        a=meter(.8,-4.25); b=meter(.26,4.25); self.add(a,b,label('organoid',-4.25,-3.2,30),label('fetal cortex',4.25,-3.2,30))
        self.at('stress genes')
        c1=chip('glycolysis',RED,30).move_to([0,1.5,0]); c2=VGroup(RoundedRectangle(width=4.6,height=1.25,corner_radius=.15,color=RED,fill_color=RED,fill_opacity=.12),label(['endoplasmic reticulum','stress'],0,0,28,RED)).move_to([0,-.3,0])
        self.play(FadeIn(c1),FadeIn(c2),Create(Line([-3.6,1.7,0],[-1.25,1.5,0],color=RED)),Create(Line([-3.6,.3,0],[-2.3,-.3,0],color=RED)),run_time=.4)
        self.finish()


class S21Transplant(SpokenScene):
    def construct(self):
        outline=Ellipse(width=4.2,height=4.7,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([-4,-.1,0])
        self.add(outline,label('mouse cortex',-4,2.75,32),label('human organoid cells',-4,-3.15,28,GREEN))
        cells=VGroup(*[dot([-4.45+.3*(i%4),-.32+.22*(i//4),0],GREEN,.09) for i in range(12)])
        self.add(cells)
        m=meter(.8,-.65,h=2.9); self.add(m,label(['stress genes','(schematic)'],-.65,-3.2,27,RED))
        # The only human-cell group is inside the mouse outline; beams leave that group.
        subs=VGroup(*[VGroup(Circle(radius=.35,color=GREEN),T(s,30,GREEN)).move_to([5.4,y,0]) for s,y in zip('ABC',ROWS)])
        self.add(subs,label('fetal subtypes',4.5,2.8,30))
        beams=VGroup(*[Line([-3.25,-.1,0],[5.0,y,0],color=TEAL,stroke_width=3,stroke_opacity=.15) for y in ROWS]).set_z_index(-1)
        self.add(beams,label('identity blurred',3,-3.1,28,RED))
        self.at('Transplanted into'); self.play(cells.animate.move_to(outline.get_center()).scale(1.5),run_time=1.1)
        self.at('those stress genes'); self.play(Transform(m[1],meter(.36,-.65,h=2.9)[1]),run_time=.7)
        self.at('Some cells came'); self.play(beams.animate.set_stroke(width=3,opacity=.2),run_time=.4)
        self.at('more closely')
        self.play(FadeOut(beams[1]),FadeOut(beams[2]),beams[0].animate.set_stroke(width=7,opacity=1),run_time=.4)
        # Replace uncertainty caption at the same moment the identity sharpens.
        for obj in list(self.mobjects):
            if abs(obj.get_center()[1]+3.1)<.02 and obj.get_center()[0]>0: self.remove(obj)
        self.add(label('closer subtype match',3,-3.1,28,TEAL)); self.finish()


class S22Dish(SpokenScene):
    def construct(self):
        self.add(label(['The dish seems to','contribute to stress'],0,2.65,40,RED))
        dish=Polygon([-6,.7,0],[-5.5,-2.6,0],[1,-2.6,0],[1.5,.7,0],color=GREY,fill_color=GREY,fill_opacity=.16)
        sph=ball([-2.25,-.65,0],radius=1.65)
        self.add(dish,sph.group,label('culture dish',-2.25,-3.25,30),meter(.8,4.2,h=3.7),label(['stress genes','(schematic)'],4.2,1.65,27,RED))
        # The question mark keeps the causal interpretation tentative in the picture.
        self.add(DashedLine([-.1,-.65,0],[3.4,-.65,0],color=RED,stroke_width=3),label('?',1.8,-.15,40,AMBER))
        self.finish()


def rule_card(sc):
    bar=Line([-4.6,2.9,0],[4.6,2.9,0],color=AMBER,stroke_width=5)
    sc.add(bar,label('THE RULE',0,2.35,30,AMBER),label('Cells bring the program',0,1.1,42),label('The embryo brings the surroundings',0,-.1,36),label(['Program: broadly kept.','Surroundings: missing.'],0,-1.55,32,AMBER,gap=.15),label('So measure each feature.',0,-2.85,36,GREEN))


class S23Take(SpokenScene):
    def construct(self): rule_card(self); self.finish()


class S24Beat(NarratedScene):
    def construct(self): rule_card(self); self.finish()


class S25End(EndCard):
    LINE='Measure every feature; the rule only says where to look first.'
    def construct(self):
        self.add(label(['Measure every feature;','the rule only says where to look first.'],0,.4,40),label('biochemistrypedia.com',0,-1.5,28,TEAL))
        self.finish()
