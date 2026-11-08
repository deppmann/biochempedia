"""Reelin and the Reeler Mouse, chapter 1: Same Neurons, Wrong Order  (Biochemistrypedia chapter film)

COLOR MAP (one color per concept, whole chapter series; taken from scenes.old.py and extended)
  ORANGE = the first-born neurons: the preplate (marginal zone and subplate cells come from it)
  RAMP   = six blues, darkest to lightest = six illustrative birth cohorts of the cortical plate,
           earliest-born darkest (replaces the old film's single BLUE / GREEN waves)
  YELLOW = Reelin, and the Cajal-Retzius cells that make it (the marginal-zone cells)
  LIME   = the radioactive birthdating label (new in this chapter)
  RED    = the reeler problem: a block, a stop, a missing part, a wrong stack
  GREY   = tissue, membranes, outlines, labels, cells whose identity is not yet known
  GOLD   = credits and years (title rule colour); in later chapters also the phosphate badge
  TEAL / PURPLE / PINK / WHITE baton = later chapters (receptors, Dab1, kinases, relay baton)

LAYOUT: one fixed cortex slab, ventricle at the bottom, pial surface at the top. Single-slab scenes put
it at x = -2.8 (widened); the split screens put the normal cortex at x = -4.0 and reeler at x = +4.0.
"""
import numpy as np
import kx_manim
kx_manim.TAIL = 0.0  # Match the final audio; do not append 0.4 s to every scene.
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
LIME = "#C6F135"
RAMP = ["#3A56C8", "#4F86DE", "#69B0EA", "#8FD0F0", "#BDE8F7", "#EAF8FD"]   # cohorts 1..6, earliest to latest

DR = 0.22
LA = [(i - 3) * 0.53 for i in range(7)]          # seven lanes per row
NL = len(LA)
HALF = 0.265                                       # half a lane: new waves climb in the gaps
CXL, CXR = -4.0, 4.0
SCX, SINGLE_W, SINGLE_SPREAD = -2.8, 6.6, 1.6
SW, S_TOP, S_BOT = 4.4, 3.3, -2.6
STEP = 0.62
ROW = {k: 2.35 - (6 - k) * STEP for k in range(1, 7)}   # resting rows of the six cohorts in the finished cortex
Y_MZ, Y_SUB, Y_BORN, Y_PRE = 2.95, -1.4, -2.0, 2.0
LX = 1.25                                        # left edge of the labels beside a single slab


# ---------------------------------------------------------------- helpers
def lab(text, color=TEXT, size=26, **kw):
    return T(text, max(26, size), color, **kw)


def left_of(mob, x, y):
    return mob.move_to([x, y, 0]).align_to([x, 0, 0], LEFT)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def dot(x, y, color, r=DR, op=0.8):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def slab(cx):
    width = SINGLE_W if cx == SCX else SW
    body = Rectangle(width=width, height=S_TOP - S_BOT, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.06).move_to([cx, (S_TOP + S_BOT) / 2, 0])
    band = Rectangle(width=width, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([cx, S_BOT + 0.2, 0])
    return VGroup(body, band)


def cohort(cx, k, y, dx=0.0, color=None):
    spread = SINGLE_SPREAD if cx == SCX else 1
    row = VGroup(*[dot(cx + (l + dx) * spread, y, color or RAMP[k - 1]) for l in LA])
    row.lane_shift = dx * spread
    return row


def mz_dots(cx, color=ORANGE):
    return VGroup(*[dot(cx + LA[i] * (SINGLE_SPREAD if cx == SCX else 1), Y_MZ, color) for i in (0, 2, 4, 6)])


def sub_dots(cx):
    return VGroup(*[dot(cx + LA[i] * (SINGLE_SPREAD if cx == SCX else 1), Y_SUB, ORANGE) for i in (1, 3, 5)])


def pre_sheet(cx, y=Y_PRE):
    return VGroup(*[dot(cx + l * (SINGLE_SPREAD if cx == SCX else 1), y, ORANGE) for l in LA])


def make_mouse(scale=2.4):
    body = Ellipse(width=1.1, height=.55, color=TEXT, fill_opacity=.65)
    head = Circle(radius=.23, color=TEXT, fill_opacity=.65).shift(RIGHT * .58 + UP * .15)
    ears = VGroup(*[Circle(radius=.14, color=TEXT, fill_color=TEXT, fill_opacity=.5).shift(RIGHT * x + UP * .38) for x in (.43, .65)])
    snout = Ellipse(width=.28, height=.16, color=TEXT, fill_opacity=.65).shift(RIGHT * .78 + UP * .08)
    eye = Dot([.67, .2, 0], radius=.035, color=BG)
    nose = Dot([.91, .08, 0], radius=.035, color="#E8789F")
    paws = VGroup(*[Ellipse(width=.22, height=.09, color=TEXT, fill_opacity=.8).shift(RIGHT * x + DOWN * .28) for x in (-.3, .33)])
    tail = CubicBezier([-.52, -.02, 0], [-1.35, -.45, 0], [-1.5, .65, 0], [-.95, .55, 0], color="#E8789F", stroke_width=4)
    return VGroup(tail, body, paws, head, ears, snout, eye, nose).scale(scale)


def climb(scene, new, below, run, delay=0.4, extra=(), y=None):
    """New wave appears in the birth zone, climbs (in the gaps) to the top row; the waves below step down one row."""
    scene.play(FadeIn(new, scale=0.6), run_time=0.15)
    y = ROW[6] if y is None else y
    shifts = AnimationGroup(*[b.animate.shift(DOWN * STEP) for b in below], run_time=min(0.8, run * 0.5))
    route = VMobject().set_points_as_corners([new.get_center(), [new.get_x(), y, 0], [new.get_x() - getattr(new, "lane_shift", HALF), y, 0]])
    anims = [MoveAlongPath(new, route, run_time=run), Succession(Wait(run * delay), shifts)]
    anims += list(extra)
    scene.play(AnimationGroup(*anims, run_time=run))


# ------------------------------------------------------- the reeler cortex (same six cohorts, 42 dots)
N = 6 * NL


def make_rs(seed=11):
    rng = np.random.RandomState(seed)
    ys = [2.45 - 0.72 * r for r in range(6)]           # top to bottom
    slots = [(LA[c] + rng.uniform(-.08, .08), ys[r] + rng.uniform(-.1, .1)) for r in range(6) for c in range(NL)]
    cohorts = np.repeat(np.arange(1, 7), NL)
    order = np.argsort(cohorts + rng.normal(0, 2.0, N))
    fin = [0] * N                                    # fin[slot] = cohort sitting there after birthdating
    for p, i in enumerate(order):
        fin[p] = int(cohorts[i])
    scr = [int(x) for x in rng.permutation(cohorts)]   # scr[slot] = cohort in the first, scrambled picture
    dest = [0] * N                                   # dot j starts in slot j and ends in a slot of its own cohort
    for k in range(1, 7):
        src = [j for j in range(N) if scr[j] == k]
        dst = [p for p in range(N) if fin[p] == k]
        for a, b in zip(src, dst):
            dest[a] = b
    dark = [j for j in range(N) if scr[j] in (1, 2)]   # mid: the two earliest cohorts first, others swap out of the way
    mid = list(range(N))
    for j in dark:
        mid[j] = dest[j]
    targets = {dest[j] for j in dark}
    vacated = [j for j in dark if j not in targets]
    displaced = [o for o in range(N) if scr[o] not in (1, 2) and o in targets]
    for o, v in zip(displaced, vacated):
        mid[o] = v
    return slots, fin, scr, dest, mid


SLOTS, FIN, SCR, DEST, MID = make_rs()
OUT_OF_PLACE = [j for j in range(N) if abs(SCR[j] - (DEST[j] // NL + 1)) >= 2]


def rpos(j, state, cx=CXR):
    slot = {"scr": j, "mid": MID[j], "fin": DEST[j]}[state]
    x, y = SLOTS[slot]
    return np.array([cx + x, y, 0])


def reeler_dots(state="scr", colored=False, cx=CXR):
    return VGroup(*[Circle(radius=DR, stroke_color=RAMP[SCR[j] - 1] if colored else GREY, stroke_width=2.5,
                           fill_color=RAMP[SCR[j] - 1] if colored else GREY, fill_opacity=.8 if colored else .5).move_to(rpos(j, state, cx))
                    for j in range(N)])


def normal_stack(cx=CXL):
    return VGroup(*[cohort(cx, k, ROW[k]) for k in range(1, 7)])


def split_frame(state="scr", colored=False):
    """both cortices, rebuilt in the same place every time."""
    sn, sr = slab(CXL), slab(CXR)
    ln = lab("normal", TEXT, 26).move_to([CXL, -3.5, 0])
    lr = lab("reeler", RED, 26).move_to([CXR, -3.5, 0])
    return sn, sr, VGroup(normal_stack(), mz_dots(CXL, YELLOW), sub_dots(CXL)), reeler_dots(state, colored), ln, lr


def card(text, color=TEXT, size=24):
    return chip(text, color, size, pad=0.2)


def sched_rows():
    rows = VGroup()
    for cx in (CXL, CXR):
        rows.add(VGroup(*[dot(cx + (i - 2.5) * .6, -2.85, RAMP[i], r=.20,op=1) for i in range(6)]))
    return rows


def credit73():
    return T("Caviness and Sidman, 1973", 30, GOLD, font=TITLE_FONT).move_to([0, 3.5, 0])


def cortex_base(cx=SCX):
    return VGroup(slab(cx), lab("ventricle", TEXT, 26).move_to([cx, S_BOT+.2, 0]),
                  lab("pial surface", TEXT, 26).move_to([cx, 3.55, 0]))


def zone_labels():
    return VGroup(left_of(lab("marginal zone", YELLOW, 32), LX, Y_MZ),
                  left_of(lab("subplate", ORANGE, 32), LX, Y_SUB),
                  Line([SCX+SINGLE_W/2,Y_MZ,0],[LX-.15,Y_MZ,0],color=YELLOW),
                  Line([SCX+SINGLE_W/2,Y_SUB,0],[LX-.15,Y_SUB,0],color=ORANGE))


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Reelin and the Reeler Mouse"
    TITLE = "Same Neurons, Wrong Order"


class S01Q(SpokenScene):
    def construct(self):
        title = lab("Same Neurons, Wrong Order", GOLD, 36).move_to([0,3.25,0])
        base = make_mouse(4.6).move_to([0,-.35,0])
        mouse = base.copy()
        # Sinusoidal sway is schematic gait, not a biological data trace.
        path = ParametricFunction(lambda t: np.array([-4.7+9.4*t, -2.5+.5*np.sin(6*PI*t), 0]), t_range=[0,1], color=RED)
        self.add(title, mouse, path)
        self.at("mouse reels")
        self.play(mouse.animate.rotate(.22).shift(LEFT*.8), run_time=.5)
        self.play(mouse.animate.rotate(-.44).shift(RIGHT*1.6), run_time=.6)
        self.play(mouse.animate.rotate(.44).shift(LEFT*1.6), run_time=.6)
        a=lab("walking problem?", TEXT,32).move_to([-3.3,2.25,0])
        b=lab("building problem?",TEXT,32).move_to([3.3,2.25,0])
        self.at("walking problem")
        self.play(FadeIn(a),mouse.animate.rotate(-.22).shift(RIGHT*.8),run_time=.45)
        self.at("building problem")
        self.play(FadeIn(b),run_time=.4)
        self.finish()


class S021951(SpokenScene):
    def construct(self):
        credit=lab("Falconer, 1951",GOLD,40).move_to([0,3.2,0])
        mouse=make_mouse(4.5).move_to([0,-.5,0])
        cb=Ellipse(width=2,height=1.4,color=ORANGE,fill_opacity=.3).move_to([3.8,-1.8,0])
        cbl=lab("cerebellum",ORANGE,28).move_to([3.8,-2.85,0])
        self.add(credit,mouse)
        self.at("named this mutant")
        tag=chip("reeler",RED,34).move_to([-3.5,1.8,0])
        self.play(FadeIn(tag),mouse.animate.scale(.7).shift(LEFT*1.4),run_time=.35)
        self.play(FadeOut(mouse),FadeOut(tag),run_time=.3)
        self.remove(mouse,tag)
        self.play(FadeIn(cb),FadeIn(cbl),run_time=.35)
        self.at("Its cortex")
        cortex=Ellipse(width=7.5,height=4.8,color=TEXT,fill_color=GREY,fill_opacity=.15).move_to([-1,0,0])
        folds=VGroup(*[Arc(radius=1.1,start_angle=.2,angle=2,color=GREY).stretch(1.5,0).move_to([-2.7+1.7*i,.2,0]) for i in range(3)])
        cl=lab("cerebral cortex",TEXT,38).move_to([-1,1.6,0])
        self.play(FadeOut(cb),FadeOut(cbl),run_time=.2)
        self.remove(cb,cbl)
        self.play(FadeIn(cortex),Create(folds),run_time=.3)
        self.play(FadeIn(cl),run_time=.25)
        self.at("deeper puzzle")
        self.play(FadeIn(T("?",90,YELLOW).move_to([-1,-.8,0])),run_time=.4)
        self.finish()


class S03Dir(SpokenScene):
    def construct(self):
        cx = SCX
        sl = slab(cx)
        vent = lab("ventricle", TEXT, 26).move_to([cx, S_BOT + .2, 0])
        axis = arr([LX - .35, -2.3, 0], [LX - .35, 3.0, 0], GREY, 5)
        self.add(sl, vent)
        self.at("direction")
        self.play(GrowArrow(axis), run_time=.6)
        deep = left_of(lab("deep: near the ventricle", TEXT, 34), LX, -2.35)
        self.at("Deep means")
        self.play(sl[1].animate.set_fill(opacity=.6), FadeIn(deep), run_time=.6)
        dots = VGroup(*[dot(cx + l * SINGLE_SPREAD, Y_BORN, ORANGE) for l in LA])
        born = left_of(lab("neurons are born here", ORANGE, 28), LX, -1.65)
        self.at("neurons are born")
        self.play(FadeIn(dots, scale=.5), FadeIn(born), run_time=.6)
        top = Line([cx - SINGLE_W / 2, S_TOP, 0], [cx + SINGLE_W / 2, S_TOP, 0], color=TEXT, stroke_width=8)
        sup = left_of(lab("superficial: outer surface", TEXT, 32), LX, 2.85)
        pial = left_of(lab("pial surface", TEXT, 26), LX, 3.45)
        self.at("Superficial means")
        self.play(FadeOut(born), Create(top), FadeIn(sup), FadeIn(pial), run_time=.7)
        self.remove(born)
        self.finish()


class S04Preplate(SpokenScene):
    def construct(self):
        pre=pre_sheet(SCX,Y_BORN).set_fill(opacity=.25)
        name=left_of(lab("preplate",ORANGE,38),LX,Y_PRE)
        band=Rectangle(width=SINGLE_W,height=.5,color=ORANGE,fill_opacity=.18).move_to([SCX,Y_PRE,0])
        self.add(cortex_base(),pre)
        self.at("first neurons")
        self.play(pre.animate.set_y(Y_PRE),run_time=1.1)
        self.at("thin sheet")
        self.play(FadeIn(band),FadeIn(name),run_time=.35)
        w=cohort(SCX,1,Y_BORN,dx=HALF)
        w.set_fill("#B5CAF4",opacity=.9)
        self.at("next neurons")
        self.play(FadeIn(w),run_time=.15)
        self.play(w.animate.set_y(Y_PRE),run_time=.5)
        self.at("split it")
        self.play(*[pre[i].animate.set_y(Y_MZ if i%2==0 else Y_SUB) for i in range(7)],
                  w.animate.shift(LEFT*HALF*SINGLE_SPREAD).set_y(ROW[6]),FadeOut(band),
                  name.animate.set_y(.4),run_time=.75)
        self.finish()


class S05Zones(SpokenScene):
    def construct(self):
        mz=mz_dots(SCX)
        self.add(cortex_base(),mz,sub_dots(SCX),cohort(SCX,1,ROW[6]))
        mzl=left_of(lab("marginal zone",YELLOW,34),LX,Y_MZ)
        cr=left_of(lab("Cajal-Retzius cells",YELLOW,30),LX,2.35)
        self.at("marginal zone")
        self.play(FadeIn(mzl),run_time=.35)
        self.at("with the")
        self.play(FadeIn(cr),mz.animate.set_color(YELLOW),run_time=.4)
        sub=left_of(lab("subplate",ORANGE,34),LX,Y_SUB)
        self.at("Below sits")
        self.play(FadeIn(sub),run_time=.35)
        cp=left_of(lab("cortical plate",TEXT,30),LX,.8)
        lead=Line([SCX+SINGLE_W/2,.8,0],[LX-.15,.8,0],color=TEXT)
        self.play(FadeIn(cp),Create(lead),run_time=.35)
        self.finish()


class S06Waves(SpokenScene):
    def construct(self):
        c1=cohort(SCX,1,ROW[6])
        self.add(cortex_base(),mz_dots(SCX,YELLOW),sub_dots(SCX),c1,zone_labels())
        cap=lab("Schematic: six illustrative birth cohorts",TEXT,26).move_to([0,-3.25,0])
        self.add(cap)
        waves=[c1]
        self.at("Each later wave")
        for k in (2,3,4):
            new=cohort(SCX,k,Y_BORN,dx=HALF)
            climb(self,new,waves,.7,delay=.35)
            waves.append(new)
        self.at("and settles")
        for k in (5,6):
            new=cohort(SCX,k,Y_BORN,dx=HALF)
            climb(self,new,waves,.8,delay=.35)
            waves.append(new)
        self.finish()


class S07Inside(SpokenScene):
    def construct(self):
        cx = SCX
        sl = slab(cx)
        vent = lab("ventricle", TEXT, 26).move_to([cx, S_BOT + .2, 0])
        mz = mz_dots(cx, YELLOW)
        sub = sub_dots(cx)
        cap = lab("Schematic: six illustrative birth cohorts", TEXT, 26).move_to([0,-3.25,0])
        self.add(cortex_base(), mz, sub, normal_stack(SCX), cap, zone_labels())
        inside = left_of(lab("inside-out", TEXT, 48, font=TITLE_FONT), LX, .55)
        self.at("So the cortex")
        self.play(FadeIn(inside),run_time=.35)
        early = left_of(lab("early-born: deep", RAMP[1], 34), LX, ROW[1])
        ea = arr([LX - .1, ROW[1], 0], [cx + SINGLE_W / 2 + .05, ROW[1], 0], RAMP[1], 4)
        self.at("Early born")
        self.play(FadeIn(early), Create(ea), run_time=.5)
        late = left_of(lab("late-born: near surface", RAMP[5], 32), LX, ROW[6])
        la = arr([LX - .1, ROW[6], 0], [cx + SINGLE_W / 2 + .05, ROW[6], 0], RAMP[5], 4)
        self.at("late")
        self.play(FadeIn(late), Create(la), run_time=.5)
        self.finish()


class S08Q(SpokenScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("scr", False)
        self.at("Is")
        self.play(FadeIn(VGroup(sn, sr, ns, rd, ln, lr)), run_time=.9)
        a = card("wrong neurons?", TEXT, 28).move_to([0, 1.3, 0])
        self.at("wrong neurons")
        self.play(FadeIn(a, shift=DOWN * .15), Indicate(rd, scale_factor=1.04, color=RED), run_time=.7)
        b = card("wrong place?", TEXT, 28).move_to([0, -0.5, 0])
        self.at("wrong place")
        self.play(FadeIn(b, shift=DOWN * .15), run_time=.5)
        self.finish()


class S09Bd(SpokenScene):
    def construct(self):
        credit=lab("Caviness and Sidman",GOLD,36).move_to([0,3.25,0])
        cell=Circle(radius=2.5,color=TEXT,fill_color=GREY,fill_opacity=.12).move_to([-2.5,-.3,0])
        nuc=Circle(radius=1.35,color=TEXT).move_to([-2.5,-.3,0])
        dna=chip("DNA",TEXT,32).move_to([-2.5,-.3,0])
        nl=lab("nucleus",TEXT,28).move_to([-2.5,-2.15,0])
        self.add(credit,cell,nuc,dna,nl,Line([-2.5,-1.7,0],[-2.5,-1.9,0],color=TEXT))
        self.at("used birth dating")
        self.play(FadeIn(lab("birthdating",TEXT,44).move_to([3,1.9,0])),run_time=.4)
        pulse=VGroup(*[Dot([2.6+.4*(i%3),.4+.45*(i//3),0],radius=.13,color=LIME) for i in range(6)])
        label=lab("radioactive\nbuilding block",LIME,30).move_to([3,-.8,0])
        self.at("a radioactive building block")
        self.play(FadeIn(pulse),FadeIn(label),run_time=.4)
        self.at("label cells")
        self.play(*[pulse[i].animate.move_to([-3.2+.65*(i%3),-.95+1.3*(i//3),0]) for i in range(6)],nuc.animate.set_color(LIME),run_time=.55)
        self.at("copying their")
        self.play(dna.animate.set_color(LIME),FadeIn(lab("copying DNA",LIME,30).move_to([3,-2,0])),run_time=.45)
        self.finish()


def cell_at(x,y,r=.55):
    return Circle(radius=r,color=TEXT,fill_color=GREY,fill_opacity=.15).move_to([x,y,0])


def dots_in(c,n):
    return [np.array([c[0]+.28*np.cos(2*PI*i/n),c[1]+.28*np.sin(2*PI*i/n),0]) for i in range(n)]


class S10Dil(SpokenScene):
    def construct(self):
        parent=cell_at(-1,2.65,r=.65)
        marks=VGroup(*[Dot(p,radius=.10,color=LIME) for p in dots_in((-1,2.65),8)])
        title=lab("pulsed label",LIME,32).move_to([1.5,2.65,0])
        self.add(parent,marks,title)
        self.at("Each division")
        self.play(Indicate(marks,color=LIME),run_time=.3)
        l,r=cell_at(-3.2,.95,r=.65),cell_at(1.2,.95,r=.65)
        self.at("shares the label")
        self.play(ReplacementTransform(parent,VGroup(l,r)),FadeOut(title),
                  *[marks[i].animate.move_to(dots_in((-3.2,.95) if i<4 else (1.2,.95),4)[i%4]) for i in range(8)],run_time=.65)
        self.add(Line([-1,2,0],[-3.2,1.6,0],color=GREY),Line([-1,2,0],[1.2,1.6,0],color=GREY))
        once=lab("divides once more",TEXT,30).move_to([-4.45,2.2,0])
        once_link=Line([-4.1,1.9,0],[-3.5,1.55,0],color=TEXT)
        self.at("A cell that")
        self.play(FadeIn(once),Create(once_link),l.animate.set_stroke(LIME,width=4),run_time=.3)
        a,b=cell_at(-4.6,-.85,r=.65),cell_at(-1.5,-.85,r=.65)
        self.at("once more")
        self.play(ReplacementTransform(l,VGroup(a,b)),FadeOut(once),FadeOut(once_link),
                  *[marks[i].animate.move_to(dots_in((-4.6,-.85) if i<2 else (-1.5,-.85),2)[i%2]) for i in range(4)],run_time=.55)
        self.add(Line([-3.2,.3,0],[-4.6,-.2,0],color=GREY),Line([-3.2,.3,0],[-1.5,-.2,0],color=GREY))
        stops=lab("never divides again",RED,30).move_to([-1.2,-2.15,0])
        stop_link=Line([-1.5,-1.5,0],[-1.5,-1.85,0],color=RED)
        c,d=cell_at(-5.4,-2.7),cell_at(-3.8,-2.7)
        self.at("never again")
        self.play(FadeIn(stops),Create(stop_link),b.animate.set_stroke(LIME,width=5),
                  ReplacementTransform(a,VGroup(c,d)),
                  marks[0].animate.move_to([-5.4,-2.7,0]),marks[1].animate.move_to([-3.8,-2.7,0]),run_time=.3)
        self.add(Line([-4.6,-1.5,0],[-5.4,-2.15,0],color=GREY),Line([-4.6,-1.5,0],[-3.8,-2.15,0],color=GREY))
        cortex=Rectangle(width=2.2,height=4.5,color=TEXT).move_to([4.6,-.1,0])
        row=Line([3.5,-.85,0],[5.7,-.85,0],color=LIME,stroke_width=4)
        settled=dot(4.6,-.85,LIME,r=.24)
        link=arr([-.75,-.85,0],[4.25,-.85,0],LIME)
        self.at("heavily")
        self.play(b.animate.set_fill(LIME,opacity=.3),FadeIn(cortex),Create(row),GrowArrow(link),FadeIn(settled),
                  FadeIn(lab("heavily labelled",LIME,30).move_to([-1.2,-3.1,0])),
                  FadeIn(lab("settles here",LIME,30).move_to([4.6,-2.85,0])),run_time=.55)
        self.finish()


def predict_cards():
    head=chip("Predict",GOLD,38,fill_opacity=1).move_to([0,3.1,0])
    head[1].set_color(BG)
    def panel(text,y):
        box=RoundedRectangle(width=9.6,height=1.65,corner_radius=.15,color=TEXT,fill_color=BG,fill_opacity=1)
        label=lab(text,TEXT,30)
        return VGroup(box,label).move_to([0,y,0])
    return head,panel("Wrong neurons made:\nbirthdating shows?",1.25),panel("Right neurons misplaced:\nbirthdating shows?",-1.1)


class S11Predict(SpokenScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("scr", False)
        comparison=VGroup(sn,sr,ns,rd,ln,lr)
        comparison.save_state()
        comparison.set_opacity(.16)
        self.add(sn, sr, ns, rd, ln, lr)
        head, a, b = predict_cards()
        self.at("Predict")
        self.play(FadeIn(head), run_time=.4)
        self.at("If Reeler made")
        self.play(FadeIn(a, shift=DOWN * .15), run_time=.5)
        self.at("if it misplaced")
        self.play(FadeIn(b, shift=DOWN * .15), run_time=.5)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("scr", False)
        head, a, b = predict_cards()
        comparison=VGroup(sn,sr,ns,rd,ln,lr)
        comparison.save_state()
        comparison.set_opacity(.16)
        self.add(sn, sr, ns, rd, ln, lr, head, a, b)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("scr", False)
        head, a, b = predict_cards()
        comparison=VGroup(sn,sr,ns,rd,ln,lr)
        comparison.save_state()
        comparison.set_opacity(.16)
        self.add(sn, sr, ns, rd, ln, lr, head, a, b)
        credit = credit73()
        self.at("In 1973")
        self.play(FadeOut(VGroup(head, a, b)), FadeIn(credit), comparison.animate.restore(), run_time=.5)
        self.at("same classes")
        self.play(*[rd[j].animate.set_fill(RAMP[SCR[j] - 1], opacity=.8).set_stroke(RAMP[SCR[j] - 1]) for j in range(N)], run_time=.9)
        rows = sched_rows()
        same = lab("same birth schedule", TEXT, 26).move_to([0, -2.85, 0])
        self.at("born on the same")
        self.add(rows,same)
        self.wait(.4)
        self.finish()


class S14Order(SpokenScene):
    def construct(self):
        sn,sr,ns,rd,ln,lr=split_frame("scr",True)
        self.add(sn,sr,ns,rd,ln,lr)
        self.at("What changed")
        self.play(*[rd[j].animate.move_to(rpos(j,"fin")) for j in range(N)],run_time=1.25)
        what=lab("changed:\nthe order",TEXT,30).move_to([0,1.6,0])
        self.play(FadeIn(what),run_time=.3)
        note=lab("early-born:\nnear surface\n\nlate-born:\ndeep",TEXT,28).move_to([0,-.65,0])
        self.at("Early born")
        self.play(FadeIn(note),run_time=.35)
        self.finish()


class S15Rough(SpokenScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("fin", True)
        self.add(sn, sr, ns, rd, ln, lr)
        inv = lab("roughly inverted", TEXT, 30).move_to([0, 1.6, 0])
        self.at("roughly inverted")
        self.play(FadeIn(inv, shift=DOWN * .1), run_time=.5)
        rings = VGroup(*[Circle(radius=DR + .1, stroke_color=TEXT, stroke_width=3.5).move_to(rpos(j, "fin")) for j in OUT_OF_PLACE])
        scat = lab("a lot of scatter:\nnot a mirror image", RED, 28, line_spacing=.8).move_to([0, 0.2, 0])
        self.at("a lot of scatter")
        self.play(Create(rings), FadeIn(scat), run_time=.7)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        sn, sr, ns, rd, ln, lr = split_frame("fin", True)
        inv = lab("roughly inverted", TEXT, 30).move_to([0, 1.6, 0])
        rings = VGroup(*[Circle(radius=DR + .1, stroke_color=TEXT, stroke_width=3.5).move_to(rpos(j, "fin")) for j in OUT_OF_PLACE])
        scat = lab("a lot of scatter:\nnot a mirror image", RED, 28, line_spacing=.8).move_to([0, 0.2, 0])
        self.add(sn, sr, ns, rd, ln, lr, inv, rings, scat)
        self.finish()


R_STACK = [1.85, 1.23, 0.61]   # where later waves stop in reeler, under the unsplit sheet
Y_SUPER = 2.5


class S17Split(SpokenScene):
    def construct(self):
        pre=pre_sheet(SCX,2.5)
        title=left_of(lab("reeler",RED,40),LX,3.0)
        label=left_of(lab("preplate — unsplit\n(superplate)",ORANGE,32),LX,2.0)
        bar=Line([SCX-2.95,2.15,0],[SCX+2.95,2.15,0],color=RED,stroke_width=8)
        self.add(cortex_base(),pre,title,label)
        w1=cohort(SCX,1,Y_BORN)
        self.at("fails to split")
        self.play(Create(bar),FadeIn(w1),run_time=.25)
        self.play(w1.animate.set_y(1.6),run_time=.75)
        note=left_of(lab("later waves\nstop beneath",RED,34),LX,-.5)
        self.at("Later waves")
        self.play(FadeIn(note),run_time=.2)
        w2,w3=cohort(SCX,2,Y_BORN),cohort(SCX,3,Y_BORN)
        self.play(FadeIn(w2),run_time=.15)
        self.play(w2.animate.set_y(.8),run_time=.55)
        self.at("stop beneath")
        self.play(FadeIn(w3),run_time=.15)
        self.play(w3.animate.set_y(0),run_time=.55)
        self.finish()


class S18Idea(SpokenScene):
    def construct(self):
        head=lab("Mainly placement",RED,42).move_to([0,3,0])
        row=VGroup(*[dot(-5.7+i*.65,-.2,RAMP[i],r=.26) for i in range(6)])
        born=lab("born in order",TEXT,32).move_to([-4,1,0])
        step=chip("stacking",TEXT,34).move_to([.4,-.2,0])
        col=VGroup(*[dot(4.8,-1.9+i*.7,RAMP[i],r=.26) for i in range(6)])
        self.add(head,row,born,step)
        missing=chip("missing protein",YELLOW,32).move_to([.4,1.8,0])
        self.at("the missing protein")
        self.play(FadeIn(missing),run_time=.35)
        self.at("is needed")
        self.play(Transform(missing,chip("Reelin signalling",YELLOW,30).move_to([.4,1.8,0])),
                  GrowArrow(arr([.4,1.2,0],[.4,.35,0],YELLOW)),run_time=.4)
        self.at("to stack")
        self.play(GrowArrow(arr([-2.1,-.2,0],[-.9,-.2,0],TEXT)),GrowArrow(arr([1.7,-.2,0],[4.2,-.2,0],TEXT)),FadeIn(col),run_time=.45)
        self.at("right way up")
        self.play(FadeIn(lab("stacked by Reelin signalling",TEXT,30).move_to([0,-3,0])),run_time=.35)
        self.finish()


class S19Idea2(SpokenScene):
    def construct(self):
        old=VGroup(cohort(CXL,1,ROW[4]),cohort(CXL,2,ROW[5]),cohort(CXL,3,ROW[6]))
        left=lab("with Reelin signalling",YELLOW,28).move_to([CXL,3.55,0])
        mz=mz_dots(CXL,YELLOW)
        mzl=lab("marginal zone",YELLOW,28).move_to([0,2.95,0])
        leader=Line([CXL+1.9,Y_MZ,0],[-1.25,Y_MZ,0],color=YELLOW)
        self.add(slab(CXL),old,left,mz,mzl,leader)
        new=cohort(CXL,4,Y_BORN,dx=HALF)
        self.at("each new wave")
        climb(self,new,list(old),1.6,delay=.4)
        self.at("at the top")
        self.play(FadeIn(lab("finish just under the zone",TEXT,26).move_to([CXL,-3.05,0])),run_time=.3)
        right=lab("without Reelin signalling",RED,28).move_to([CXR,3.55,0])
        elders=VGroup(cohort(CXR,1,ROW[6]),cohort(CXR,2,ROW[5]),cohort(CXR,3,ROW[4]))
        self.at("Without it")
        self.play(FadeIn(slab(CXR)),FadeIn(right),FadeIn(elders),run_time=.3)
        rng=np.random.RandomState(5)
        wave=cohort(CXR,4,Y_BORN)
        self.at("newcomers tend")
        self.play(FadeIn(wave),run_time=.15)
        self.play(*[m.animate.set_y(ROW[3]+d) for m,d in zip(wave,[-.05,.12,-.3,.05,.36,-.18,.1])],run_time=.65)
        self.at("stop beneath")
        self.play(FadeIn(lab("stop beneath their elders",RED,26).move_to([CXR,-3.05,0])),run_time=.3)
        self.finish()


class S20Take(SpokenScene):
    def construct(self):
        head=lab("Takeaway",GOLD,42).move_to([0,3.4,0])
        row=VGroup(*[dot(-5.2+i*.9,.25,RAMP[i],r=.36,op=1) for i in range(6)])
        born=lab("born first → born last",TEXT,30).move_to([-2.95,-.65,0])
        made=lab("made on schedule",TEXT,38).move_to([-2.95,1.5,0])
        col=VGroup(*[dot(3,2.25-.72*i,RAMP[i],r=.33,op=1) for i in range(6)])
        labels=VGroup(lab("surface",TEXT,30).move_to([4.6,2.25,0]),lab("deep",TEXT,30).move_to([4.4,-1.35,0]))
        self.add(head,row,born,made)
        self.at("wrong way up")
        self.add(col,labels,lab("roughly inverted, with scatter",RED,30).move_to([0,-2.15,0]))
        self.wait(.4)
        self.at("Next")
        self.play(FadeIn(lab("Next: where does Reelin come from?",YELLOW,32).move_to([0,-3.15,0])),run_time=.3)
        self.finish()


class S21End(EndCard):
    LINE = "Reeler neurons form on schedule; their stacking is roughly inverted."

    def construct(self):
        line=T("Reeler neurons form on schedule;\ntheir stacking is roughly inverted.",size=42,font=TITLE_FONT,line_spacing=1.15)
        sub=lab("biochemistrypedia.com",TEAL,26).move_to([0,-1.7,0])
        self.add(line,sub)
        self.finish()

