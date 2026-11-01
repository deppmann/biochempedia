"""One hair, three kinds of touch neuron  (Biochemistrypedia explainer, Sensory Systems: the LTMR classes)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = Abeta RA-LTMR endings and label
  YELLOW = Adelta-LTMR endings and label
  ORANGE = C-LTMR endings and label
  TEAL   = Abeta SA1 (Merkel-associated) endings in the touch dome
  PURPLE = terminal Schwann cell (non-neuronal)
  GREEN  = field-LTMR ring and the one neuron with an arbor
  RED    = "no" (not a neuron count)
  GREY   = hair, follicle sheath, skin line, axis, neutral labels
  GOLD   = the rule to keep
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CLS = {"RA": BLUE, "AD": YELLOW, "C": ORANGE, "SA1": TEAL}
CNAME = {"RA": "Aβ RA", "AD": "Aδ", "C": "C", "SA1": "Aβ SA1"}


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def follicle(s=1.0, kind="awl", tails=False, dome=False):
    """Schematic hair follicle (side view): sheath, shaft, skin line, lanceolate pickets along the shaft.
    Built about the origin; caller moves the group."""
    top = {"guard": 2.5, "awl": 2.2, "zig": 1.9}[kind]
    pat = {"guard": ["RA"], "awl": ["RA", "AD", "C"], "zig": ["AD", "C"]}[kind]
    sw = max(2.0, 4 * s)
    sheath = RoundedRectangle(corner_radius=0.3 * s, width=1.5 * s, height=2.6 * s, stroke_color=GREY,
                              stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    if kind == "zig":
        pts = [(0, -1.0), (0, 1.3), (0.2, 1.45), (-0.2, 1.6), (0.0, top)]
        shaft = VMobject(stroke_color=GREY, stroke_width=3 + 4 * s, stroke_opacity=0.85)
        shaft.set_points_as_corners([np.array([x * s, y * s, 0]) for x, y in pts])
    else:
        shaft = Line([0, -1.0 * s, 0], [0, top * s, 0], color=GREY, stroke_width=3 + 4 * s, stroke_opacity=0.85)
    half = (2.2 if dome else 1.3) * s
    skin = Line([-1.3 * s, 1.3 * s, 0], [half, 1.3 * s, 0], color=GREY, stroke_width=3)
    n = len(pat)
    pk, tl = [], []
    for i, c in enumerate(pat):
        x = (i - (n - 1) / 2) * 0.32 * s if n > 1 else -0.3 * s
        p = RoundedRectangle(corner_radius=0.05 * s, width=0.16 * s, height=2.0 * s, stroke_width=0,
                             fill_color=CLS[c], fill_opacity=0.95).move_to([x, 0.0, 0])
        pk.append((c, p))
        if tails:
            tl.append((c, Line([x, -1.0 * s, 0], [x, -1.75 * s, 0], color=CLS[c], stroke_width=4)))
    parts = [skin, sheath, shaft] + [p for _, p in pk] + [t for _, t in tl]
    extra = []
    if dome:
        cx = 1.45 * s
        d = Sector(radius=0.5 * s, angle=PI, start_angle=0, stroke_color=TEAL, stroke_width=3,
                   fill_color=TEAL, fill_opacity=0.28).move_to([cx, 1.3 * s + 0.25 * s, 0])
        e = RoundedRectangle(corner_radius=0.05 * s, width=0.12 * s, height=1.0 * s, stroke_width=0,
                             fill_color=TEAL, fill_opacity=0.95).move_to([cx, 1.3 * s - 0.5 * s, 0])
        extra = [d, e]
        parts += extra
    g = VGroup(*parts)
    g.pk, g.tl, g.sheath, g.shaft, g.skin, g.s, g.extra = pk, tl, sheath, shaft, skin, s, extra
    g.pickets = VGroup(*[p for _, p in pk])
    return g


def place(f, x, y):
    """move a follicle so the centre of its SHEATH (not the whole group) sits at (x, y)."""
    f.shift(np.array([x, y, 0.0]) - f.sheath.get_center())
    return f


def schwann(f, s):
    b = Ellipse(width=1.7 * s, height=1.1 * s, stroke_color=PURPLE, stroke_width=3,
                fill_color=PURPLE, fill_opacity=0.3)
    b.move_to(f.sheath.get_center() + UP * 0.2 * s)
    b.set_z_index(-1)
    return b


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def label_line(a, b, color=GREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w)


def cls_text(c, size=30):
    return T(CNAME[c], size, CLS[c], weight=BOLD)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The low-threshold mechanoreceptors"
    TITLE = "One hair, three kinds of touch neuron"


def mini_fol(x, y):
    sheath = RoundedRectangle(corner_radius=0.22, width=0.8, height=1.6, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    shaft = Line([x, y - 0.65, 0], [x, y + 1.3, 0], color=GREY, stroke_width=6, stroke_opacity=0.85)
    skin = Line([x - 0.7, y + 0.8, 0], [x + 0.7, y + 0.8, 0], color=GREY, stroke_width=3)
    r = Ellipse(width=1.2, height=0.5, stroke_color=GREEN, stroke_width=4).move_to([x, y - 0.05, 0])
    return VGroup(skin, sheath, shaft), r


# Schematic traces throughout; spike counts are illustrative, not recordings.
def trace(x, y, color, mode='burst', width=2.4):
    pts = [[x, y, 0]]
    positions = {'burst': [0.18, 0.3, 2.08, 2.2], 'steady': list(np.arange(.2, 2.2, .23)),
                 'vibration': list(np.arange(.15, 2.3, .14)), 'hair': [.2, .33, .46],
                 'slow': [.45, 1.15, 1.85]}[mode]
    for t in positions:
        t = t * width / 2.4
        pts.extend([[x+t-.035,y,0], [x+t,y+.32,0], [x+t+.035,y,0]])
    pts.append([x+width,y,0])
    return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(pts)


def finger(x, y):
    return RoundedRectangle(width=.65, height=1.5, corner_radius=.3, stroke_color=TEXT,
                            stroke_width=4, fill_color=BG, fill_opacity=1).move_to([x,y,0])


def forearm():
    outline = RoundedRectangle(width=10.8, height=1.75, corner_radius=.65,
                               stroke_color=GREY, stroke_width=4).move_to([0,.35,0])
    hairs = VGroup(*[Line([x,1.23,0], [x+.12,1.57,0], color=GREY, stroke_width=2)
                     for x in (-3.8,-2.5,-1.2,.1,1.4,2.7,4)])
    return VGroup(outline, hairs)


class S01Split(SpokenScene):
    def construct(self):
        skin=Line([-5.8,1.3,0],[5.8,1.3,0],color=GREY,stroke_width=4)
        tip=finger(0,2.45)
        self.at('A light touch')
        self.play(Create(skin),FadeIn(tip),run_time=.6)
        self.play(tip.animate.shift(DOWN*.4),run_time=.5)
        specs=[('motion',BLUE,'burst'),('steady press\nand edges',TEAL,'steady'),
               ('vibration',GREY,'vibration'),('hair bend',YELLOW,'hair'),('gentle stroke',ORANGE,'slow')]
        branches=[]
        for i,(name,col,mode) in enumerate(specs):
            x=-5.05+i*2.52
            path=VMobject(stroke_color=col,stroke_width=3).set_points_as_corners([[0,1.2,0],[0,.8,0],[x,.1,0],[x,-.5,0]])
            wave=trace(x-1.02,-1.0,col,mode,2.04)
            lab=T(name,24,col).move_to([x,-1.85,0])
            branches.append(VGroup(path,wave,lab))
        self.at('Several kinds')
        self.play(*[Create(g[0]) for g in branches],run_time=.9)
        for i,cue in enumerate(('Some fire','Some keep firing','Some are most','Some catch','And some')):
            self.at(cue)
            self.play(Create(branches[i][1]),FadeIn(branches[i][2]),run_time=.7)
            dot=Dot([0,1.2,0],radius=.07,color=specs[i][1])
            self.play(MoveAlongPath(dot,branches[i][0]),run_time=.65,rate_func=linear)
            self.remove(dot)
        self.at('Each kind is')
        tag=chip('LTMR',GOLD,30).move_to([0,-3,0])
        self.play(FadeIn(tag),run_time=.6)
        self.finish()


class S02Classes(SpokenScene):
    def construct(self):
        head=T('Ending • response • speed',34,font=TITLE_FONT).move_to([0,3,0])
        self.at('Each class has')
        self.play(FadeIn(head),run_time=.6)
        # Two schematic end organs and their responses to the same held step.
        rows=[]
        for y,name,col,mode in ((1.3,'Merkel',TEAL,'steady'),(-1.3,'Pacinian',GREY,'burst')):
            if name=='Merkel':
                icon=VGroup(Line([-5.3,y-.2,0],[-4.2,y-.2,0],color=col,stroke_width=5),
                            *[Dot([x,y+.1,0],radius=.13,color=col) for x in (-5.1,-4.75,-4.4)])
            else:
                icon=VGroup(*[Ellipse(width=w,height=w*.6,color=col,stroke_width=3).move_to([-4.75,y,0]) for w in (1.15,.78,.4)])
            label=T(name,28,col).move_to([-2.6,y,0])
            step=VMobject(stroke_color=GREY,stroke_width=2).set_points_as_corners([[.3,y+.7,0],[.6,y+.7,0],[.6,y+1,0],[3.7,y+1,0],[3.7,y+.7,0],[4,y+.7,0]])
            wave=trace(.3,y-.2,col,mode,3.7)
            rows.append(VGroup(icon,label,step,wave))
        self.at('endings serve the steady')
        self.play(FadeIn(rows[0][:3]),Create(rows[0][3]),run_time=.9)
        self.at('corpuscles serve vibration')
        self.play(FadeIn(rows[1][:3]),Create(rows[1][3]),run_time=.9)
        self.at('At mouse hairs')
        self.play(FadeOut(VGroup(*rows)),Transform(head,T('Mouse hair afferents • mean speed',32,font=TITLE_FONT).move_to(head)),run_time=.5)
        x0,k=-2.5,.47
        axis=VGroup(Line([x0,-2.25,0],[x0+15*k,-2.25,0],color=GREY),
                    *[M(str(v),22,GREY).move_to([x0+v*k,-2.65,0]) for v in (0,5,10,15)],
                    T('m/s',24,GREY).move_to([5.5,-2.65,0]))
        self.play(FadeIn(axis),run_time=.4)
        bars=[]
        for c,v,y,cue in [('RA',13.6,1.45,'neurons conduct'),('AD',5.8,.1,'a delta neurons'),('C',.58,-1.25,'and C neurons')]:
            w=v*k
            bar=Rectangle(width=w,height=.55,stroke_width=0,fill_color=CLS[c],fill_opacity=.9).move_to([x0+w/2,y,0])
            lab=cls_text(c,30).move_to([-4.4,y,0])
            val=M(str(v),26,CLS[c]).next_to(bar,RIGHT,buff=.18)
            self.at(cue)
            self.play(FadeIn(lab),GrowFromEdge(bar,LEFT),FadeIn(val),run_time=.7)
            bars.append(VGroup(bar,lab,val))
        self.at('by far the slowest')
        self.play(Indicate(bars[2],color=ORANGE,scale_factor=1.04),run_time=.6)
        self.at('So one touch')
        self.play(FadeOut(VGroup(head,axis,*bars)),run_time=.35)
        target=chip('spinal cord',GREY,28).move_to([4.6,0,0])
        lanes=VGroup(*[Line([-3.8,y,0],[2.9,y,0],color=CLS[c],stroke_width=3) for c,y in [('RA',1.4),('AD',0),('C',-1.4)]])
        labs=VGroup(*[cls_text(c,26).move_to([-5.1,y,0]) for c,y in [('RA',1.4),('AD',0),('C',-1.4)]])
        note=T('Same distance • different arrival times',26,GREY).move_to([0,-2.8,0])
        self.play(FadeIn(target),Create(lanes),FadeIn(labs),FadeIn(note),run_time=.4)
        spikes=[Dot(l.get_start(),radius=.11,color=CLS[c]) for c,l in zip(('RA','AD','C'),lanes)]
        self.add(*spikes)
        # Duration is inversely proportional to the measured velocity.
        self.play(AnimationGroup(*[d.animate(run_time=2.8*.58/v,rate_func=linear).move_to(l.get_end()) for d,l,v in zip(spikes,lanes,(13.6,5.8,.58))]))
        self.finish()


class S03Fence(SpokenScene):
    def construct(self):
        s=1.2; f=place(follicle(s,'awl',tails=True),-2.8,-.2)
        title=T('One hair • several classes',32,font=TITLE_FONT).move_to([0,3.25,0])
        self.at('These classes can share')
        self.play(FadeIn(title),FadeIn(VGroup(f.skin,f.sheath,f.shaft)),run_time=.8)
        name=T('mouse awl/auchene hair',26,GREY).move_to([3.2,2.2,0])
        self.at("On a mouse's back")
        self.play(FadeIn(name),run_time=.6)
        self.at('from three classes')
        labels=VGroup(*[chip(CNAME[c],CLS[c],26) for c in ('RA','AD','C')]).arrange(RIGHT,buff=.3).move_to([2.8,1,0])
        self.play(LaggedStart(*[FadeIn(p) for _,p in f.pk],lag_ratio=.15),FadeIn(labels),run_time=.8)
        self.at('an axon branch')
        self.play(*[Create(t) for _,t in f.tl],run_time=.6)
        end=T('lanceolate endings',28,TEXT).move_to([3,.0,0])
        leader=label_line(end.get_left()+LEFT*.15,f.pk[-1][1].get_right()+RIGHT*.1)
        self.play(FadeIn(end),Create(leader),run_time=.6)
        self.at('like a picket')
        self.play(LaggedStart(*[Indicate(p,color=CLS[c],scale_factor=1.2) for c,p in f.pk],lag_ratio=.2),run_time=.9)
        self.at('with terminal Schwann cells')
        # Reuse the old Schwann-cell blob motif, positioned in the gaps between pickets.
        sch=VGroup(*[schwann(f,.19).stretch_to_fit_width(.18).stretch_to_fit_height(1.6).move_to([-2.8+dx,-.2,0]) for dx in (-.192,.192)])
        sl=T('terminal Schwann cells',26,PURPLE).move_to([3,-1,0])
        self.play(FadeIn(sch),FadeIn(sl),run_time=.7)
        self.at('Most hairs are also wrapped')
        ring=Ellipse(width=2.35,height=.75,stroke_color=GREEN,stroke_width=5).move_to([-2.8,-.75,0])
        field=chip('field-LTMR',GREEN,28).move_to([3,-2.3,0])
        self.play(Create(ring),FadeIn(field),run_time=1)
        self.finish()


class S04Map(SpokenScene):
    def construct(self):
        q=T('Which ending belongs to which neuron?',34,font=TITLE_FONT).move_to([0,2.6,0])
        self.at('How did anyone learn')
        self.play(FadeIn(q),run_time=.7)
        steps=VGroup(*[chip(t,GREY,28) for t in ('label','record','image')]).arrange(RIGHT,buff=2).move_to([0,.4,0])
        links=VGroup(*[arr(steps[i].get_right(),steps[i+1].get_left()) for i in (0,1)])
        self.at('and colleagues labeled')
        self.play(FadeIn(steps[0]),run_time=.6)
        self.at('checked each label')
        self.play(GrowArrow(links[0]),FadeIn(steps[1]),run_time=.6)
        wave=trace(-1.2,-1.3,BLUE,'burst')
        self.play(Create(wave),run_time=.6)
        self.at('until physiology confirms it')
        self.play(Indicate(steps[1],color=GOLD,scale_factor=1.08),run_time=.7)
        self.at('Then they imaged')
        self.play(GrowArrow(links[1]),FadeIn(steps[2]),run_time=.6)
        self.at('Guard hairs carry')
        self.play(FadeOut(VGroup(q,steps,links,wave)),run_time=.35)
        xs=(-4.4,0,4.3); fs=[]; groups=[]
        for x,kind,name in zip(xs,('guard','awl','zig'),('guard','awl/auchene','zigzag')):
            f=place(follicle(.83,kind,dome=(kind=='guard')),x,.25)
            name=T(name,28,TEXT).move_to([x,-1.3,0])
            desc={'guard':[('RA','Aβ RA'),('SA1','SA1 • touch dome')], 'awl':[('RA','Aβ RA'),('AD','Aδ'),('C','C')], 'zig':[('AD','Aδ'),('C','C')]}[kind]
            labs=VGroup(*[T(t,24,CLS[c]) for c,t in desc]).arrange(DOWN,buff=.16).move_to([x,-2.3,0])
            fs.append(f); groups.append(VGroup(f,name,labs))
        f=fs[0]
        self.play(FadeIn(VGroup(f.skin,f.sheath,f.shaft,f.pickets)),FadeIn(groups[0][1]),FadeIn(groups[0][2][0]),run_time=.7)
        self.at('in a touch dome')
        self.play(FadeIn(VGroup(*f.extra)),FadeIn(groups[0][2][1]),run_time=.6)
        self.at('aukine hairs carry')
        self.play(FadeIn(groups[1]),run_time=.8)
        self.at('Zigzag hairs carry')
        self.play(FadeIn(groups[2]),run_time=.8)
        self.at('The same combinations repeat')
        # Three repeated composite units keep the patch readable.
        trio=VGroup(*[f.copy() for f in fs])
        trio.scale_to_fit_width(3.6).move_to([-4.2,0,0])
        tiles=VGroup(trio,*[trio.copy().shift(RIGHT*d) for d in (4.2,8.4)])
        patch=RoundedRectangle(width=12.6,height=3.4,corner_radius=.25,stroke_color=GREY,stroke_width=2).move_to([0,0,0])
        head=T('Repeated combinations across mouse skin',30,font=TITLE_FONT).move_to([0,2.8,0])
        self.play(FadeOut(VGroup(*groups)),FadeIn(tiles),Create(patch),FadeIn(head),run_time=.8)
        self.finish()


class S05Human(SpokenScene):
    def construct(self):
        arm=forearm()
        head=T('Human hairy skin',32,font=TITLE_FONT).move_to([0,3.2,0])
        self.at('Your own skin')
        self.play(FadeIn(arm),FadeIn(head),run_time=.8)
        nerve=Line([-4,-.05,0],[4,-.05,0],color=ORANGE,stroke_width=5)
        electrode=Line([2.8,2.7,0],[1.2,1.5,0],color=TEXT,stroke_width=4)
        self.at('Recording single nerve fibers')
        self.play(Create(nerve),Create(electrode),run_time=.7)
        self.play(electrode.animate.shift(DOWN*1.55),run_time=.7)
        method=T('microneurography',28,TEXT).move_to([-2.4,2.2,0])
        self.at('a method called')
        self.play(FadeIn(method),run_time=.6)
        self.at('by how they fire')
        wave=trace(-4,-1.8,ORANGE,'slow',8)
        self.play(Create(wave),run_time=.8)
        self.at('In hairy skin')
        hand=finger(-3,2.15).rotate(-PI/3)
        self.play(FadeOut(method),FadeIn(hand),run_time=.4)
        self.at('respond to gentle stroking')
        self.play(hand.animate.shift(RIGHT*5.4),ShowPassingFlash(wave.copy().set_stroke(WHITE,5),time_width=.25),run_time=1.7)
        ct=T('Human C-tactile  ≈  mouse C-LTMR',28,ORANGE).move_to([0,-2.75,0])
        self.at('afferents behave like mouse')
        self.play(FadeIn(ct),run_time=.7)
        self.at('Reviews conclude')
        tag=chip('C-tactile: affective touch',ORANGE,28).move_to([0,2.6,0])
        self.play(FadeOut(head),FadeOut(hand),FadeOut(electrode),FadeIn(tag),run_time=.7)
        self.at('But not every')
        note=T('not the only route',28,GOLD).move_to([0,1.75,0])
        self.play(FadeIn(note),run_time=.6)
        self.finish()


class S06Why(SpokenScene):
    def construct(self):
        title=T('No single class reports a whole touch',32,font=TITLE_FONT).move_to([0,3.1,0])
        self.at('So why build')
        self.play(FadeIn(title),run_time=.6)
        poke=place(follicle(.65,'guard',dome=True),-4,-.1)
        stroke=place(follicle(.65,'awl'),.5,-.1)
        p=finger(-3.05,2.4).scale(.7); h=finger(-.2,2.1).scale(.7).rotate(-PI/3)
        self.at('In one model')
        model=T('Schematic model',24,GREY).move_to([0,-3.2,0])
        self.play(FadeIn(model),FadeIn(poke),FadeIn(stroke),run_time=.7)
        self.at('a poke at one spot')
        pl=T('poke',26,TEAL).move_to([-4,2.25,0])
        self.play(FadeIn(p),FadeIn(pl),run_time=.3)
        self.play(p.animate.shift(DOWN*.7),run_time=.4)
        self.at('mostly the Merkel endings')
        self.play(Indicate(VGroup(*poke.extra),color=TEAL,scale_factor=1.2),run_time=.7)
        pt=trace(-5,-1.5,TEAL,'steady',2)
        self.play(Create(pt),run_time=.5)
        self.at('a stroke across the fur')
        st=T('stroke',26,BLUE).move_to([.5,2.5,0])
        self.play(FadeIn(h),FadeIn(st),run_time=.3)
        self.play(h.animate.shift(RIGHT*1.4),run_time=.6)
        waves=VGroup(*[trace(-.5,-1.3-i*.48,CLS[c],mode,2) for i,(c,mode) in enumerate((('RA','burst'),('AD','hair'),('C','slow')))])
        self.at('a different mix')
        self.play(Create(waves),run_time=.6)
        self.at('The nervous system reads')
        cord=RoundedRectangle(width=1.7,height=3.4,corner_radius=.25,stroke_color=GREY,fill_color=GREY,fill_opacity=.12).move_to([5,0,0])
        cl=T('dorsal horn',24,GREY).move_to([5,-2.25,0])
        paths=VGroup(*[arr([1.7,-1.3-i*.48,0],[4.1,.7-i*.6,0],CLS[c],w=3) for i,c in enumerate(('RA','AD','C'))])
        merkel_path=VMobject(stroke_color=TEAL,stroke_width=3).set_points_as_corners([[-2.85,-1.5,0],[-2.5,-2.75,0],[3.6,-2.75,0],[4.1,-1.2,0]])
        self.play(Create(cord),FadeIn(cl),Create(paths),Create(merkel_path),run_time=.6)
        self.at('as the signals arrive')
        dots=[Dot(path.get_start(),radius=.08,color=CLS[c]) for path,c in zip(paths,('RA','AD','C'))]
        md=Dot(merkel_path.get_start(),radius=.08,color=TEAL)
        self.add(*dots,md)
        self.play(AnimationGroup(MoveAlongPath(md,merkel_path,run_time=.4,rate_func=linear),*[MoveAlongPath(d,path,run_time=t,rate_func=linear) for d,path,t in zip(dots,paths,(.25,.6,1.5))]))
        self.at('One caution when')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        warning=T('One neuron • many hairs',34,font=TITLE_FONT).move_to([0,2.9,0])
        soma=Circle(radius=.4,color=GREEN,fill_color=GREEN,fill_opacity=.3).move_to([-5.4,-1.8,0])
        xs=(-2.2,.3,2.8,5.1)
        bodies=[]; rings=[]; brs=[]
        for x in xs:
            body,ring=mini_fol(x,.2); bodies.append(body); rings.append(ring)
            brs.append(Line([x,-1.8,0],[x,-.6,0],color=GREEN,stroke_width=4))
        bus=Line([-5,-1.8,0],[5.1,-1.8,0],color=GREEN,stroke_width=4)
        self.play(FadeIn(warning),FadeIn(VGroup(*bodies)),run_time=.6)
        self.at('A single neuron branches')
        self.play(FadeIn(soma),Create(bus),LaggedStart(*[Create(b) for b in brs],lag_ratio=.15),
                  LaggedStart(*[Create(r) for r in rings],lag_ratio=.15),run_time=1.1)
        self.at('So endings at a hair')
        rule=T('Endings at a hair ≠ neuron count',32,GOLD).move_to([0,-3,0])
        self.play(FadeIn(rule),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Endings at a hair are not a count of neurons."
