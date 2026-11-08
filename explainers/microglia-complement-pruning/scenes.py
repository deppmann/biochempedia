"""Chapter 1: Which Inputs Lose?
COLOR MAP shared with the series:
BLUE = eye A, opposite eye; ORANGE = eye B, same-side eye.
Eye A is QUIETER in both prediction and reveal; eye B is BUSIER.
PURPLE = microglia; YELLOW = complement; TEAL = receptor;
RED = silencing / receptor absent; GREY = relay neurons / astrocytes;
TEXT = firing activity. Fields and anatomy are explicitly schematic.
Visual-note correction: the microglia are purple, as in chapters 2 and 3.
"""
import os
from pathlib import Path
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
EYE_A, EYE_B = BLUE, ORANGE


class SpokenScene(BaseSpokenScene):
    """Cue on the spoken word, then log actual arrival (the shared log logs before waiting)."""
    def _words(self):
        wl = super()._words()
        # Correct only known aligner spellings; audio and script remain untouched.
        aliases = {"macroglia": "microglia", "compliment": "complement", "astrocites": "astrocytes"}
        return [(t, aliases.get(w, w)) for t, w in wl]

    def at(self, phrase, lead=-0.08, nth=0):
        spoken = self.t_of(phrase, nth)
        rest = spoken - lead - self.elapsed()
        if rest > 0:
            self.wait(rest)
        with open(Path(os.environ['KX_SCRIPT']).parent / 'sync.log', 'a') as log:
            log.write(f"{os.environ['KX_SCENE_ID']} {phrase!r}: spoken={spoken:.3f} actual={self.elapsed():.3f} delta={self.elapsed()-spoken:+.3f}\n")


def P(x, y):
    return np.array([x, y, 0.])


def unit(a):
    return P(np.cos(a * DEGREES), np.sin(a * DEGREES))


def line(a, b, col=GREY, w=4):
    return Line(a, b, color=col, stroke_width=w).set_cap_style(CapStyleType.ROUND)


def label(txt, x, y, col=TEXT, size=30):
    return T(txt, size, col).move_to(P(x, y))


def box(w, h, c=GREY, opacity=.08):
    return RoundedRectangle(width=w, height=h, corner_radius=.3, stroke_color=c,
                            stroke_width=3, fill_color=c, fill_opacity=opacity)


def microglia(c, scale=1):
    """Fine branched processes behind an opaque soma; no terminals drawn through the cell."""
    branches = VGroup()
    for i, a in enumerate(range(0, 360, 40)):
        end = c + unit(a + 8) * (1.8 + .12 * (i % 3)) * scale
        path = VMobject().set_points_smoothly([c + unit(a) * .4 * scale,
                    c + unit(a - 9) * 1.0 * scale, end])
        path.set_stroke(PURPLE, 5 * scale)
        branches.add(path)
        for f, turn in ((.57, 35), (.8, -38)):
            p = path.point_from_proportion(f)
            branches.add(line(p, p + unit(a + turn) * .65 * scale, PURPLE, 3 * scale))
    soma = Ellipse(width=1.2 * scale, height=.95 * scale, stroke_color=PURPLE,
                   fill_color=BG, fill_opacity=1, stroke_width=4).move_to(c)
    core = Ellipse(width=.85 * scale, height=.65 * scale, stroke_width=0,
                   fill_color=PURPLE, fill_opacity=.35).move_to(c)
    return VGroup(branches, soma, core)


def eye(c, col):
    return VGroup(Ellipse(width=1.7, height=1, color=col, stroke_width=4),
                  Circle(radius=.33, color=col, fill_color=col, fill_opacity=.65),
                  Dot(radius=.12, color=BG)).move_to(c)


# Large consistent territory map. It is a schematic of one side, not measured areas.
MAP_C = P(0, -.15)
PATCH_C = P(2.25, -.1)
PATCH_W, PATCH_H = 2.7, 2.6


def nucleus():
    return box(10.7, 5.15).move_to(MAP_C)


def patch(w=PATCH_W, h=PATCH_H, outline=False):
    return RoundedRectangle(width=w, height=h, corner_radius=.45,
        stroke_color=EYE_B, stroke_width=3,
        fill_color=EYE_B, fill_opacity=0 if outline else .65).move_to(PATCH_C)


def field_a():
    return box(10.35, 4.8, EYE_A, .28).move_to(MAP_C)


def map_labels():
    return VGroup(label('dLGN', -4.7, 3.05, GREY, 32),
                  label('eye A · opposite eye', -2.8, -3.12, EYE_A, 28),
                  label('eye B · same-side eye', 2.7, -3.12, EYE_B, 28))


def axon_fields(sorted_state=False):
    """Schematic arbor strokes, deterministic positions; no quantitative plot or data traces."""
    a, b = VGroup(), VGroup()
    for i in range(15):
        x = -4.65 + (i % 5) * 2.15
        y = -1.95 + (i // 5) * 1.65
        if sorted_state and .5 < x < 4.0 and -1.6 < y < 1.5:
            x = -2.9 + .3 * (i % 3)
        a.add(VGroup(line(P(x-.4, y-.25), P(x+.4, y+.25), EYE_A, 4),
                     Dot(P(x+.4, y+.25), radius=.09, color=EYE_A)))
        if sorted_state:
            x, y = 1.45 + (i % 4) * .52, -.95 + (i // 4) * .53
        else:
            x, y = -4.4 + (i % 5)*2.1, -1.75 + (i//5)*1.65
        b.add(VGroup(line(P(x-.32, y+.22), P(x+.32, y-.22), EYE_B, 4),
                     Dot(P(x+.32, y-.22), radius=.09, color=EYE_B)))
    return a, b


def overlap_fields():
    return (box(10.1, 4.6, EYE_A, .27).move_to(P(-.12, -.15)),
            box(10.1, 4.6, EYE_B, .27).move_to(P(.12, -.15)))


def sorted_map():
    a, b = axon_fields(True)
    # BG backing prevents the opposite-eye field showing through the same-side patch.
    backing = patch().set_fill(BG, 1).set_stroke(opacity=0)
    return VGroup(nucleus(), field_a(), backing, patch().set_stroke(opacity=0), a, b, map_labels())


DLGN = P(2.0, -.55)


def brain():
    # Bilobed coronal outline with a dorsal midline indentation and ventral hypothalamus.
    pts = [(0,2.2),(-.65,2.7),(-2.4,2.65),(-4,1.8),(-4.5,.4),(-4.1,-.9),
           (-2.9,-1.8),(-1.25,-2),(-.65,-2.6),(0,-2.75),(.65,-2.6),(1.25,-2),
           (2.9,-1.8),(4.1,-.9),(4.5,.4),(4,1.8),(2.4,2.65),(.65,2.7),(0,2.2)]
    out = VMobject().set_points_smoothly([P(*p) for p in pts])
    out.set_stroke(GREY, 4).set_fill(GREY, .08)
    th = VGroup(*[Ellipse(width=2.2, height=1.9, color=GREY, fill_color=GREY,
                fill_opacity=.23, stroke_width=2).move_to(P(s*.95,-.55)) for s in (-1,1)])
    ventricles = VGroup(*[ArcBetweenPoints(P(s*.3,1.5), P(s*2.8,.7), angle=s*.6,
                                          color=GREY, stroke_width=3) for s in (-1,1)])
    spot = Ellipse(width=.8, height=.55, color=TEXT, fill_color=TEXT, fill_opacity=.35).move_to(DLGN)
    return VGroup(out, th, ventricles, spot)


def brain_stage():
    return VGroup(brain(), label('newborn mouse brain · coronal schematic',0,-3.22,GREY,28),
                  label('thalamus',0,-.55,GREY,28), label('dLGN',4.6,-2.3,TEXT,30),
                  line(P(4.2,-2.0), DLGN+P(.3,-.2)))


def pathway():
    e = eye(P(-5.45,-.25),EYE_A).scale(.7)
    paths = VGroup()
    for j in range(3):
        p = VMobject().set_points_smoothly([P(-4.8,-.25+j*.13),P(-2.9,-1.4+j*.1),
                     P(.2,-1.7+j*.1),DLGN+P(-.05,j*.13)])
        paths.add(p.set_stroke(EYE_A,3))
    contacts = VGroup(*[Dot(DLGN+P(-.05,j*.13), radius=.1,color=EYE_A) for j in range(3)])
    return VGroup(e, paths, contacts)


class S00Title(TitleCard):
    LESSON = 'Microglia and Complement Prune Synapses'
    TITLE = 'Which Inputs Lose?'

    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',26,TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),26,GREY)
        title=T(self.TITLE,54,TEXT,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        content=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.35)
        fit(content)
        self.play(FadeIn(content),run_time=.5)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        self.add(brain_stage())
        self.at('some connections')
        path = pathway()
        self.play(FadeIn(path),run_time=.5)
        self.at('will be lost')
        self.play(path[2][0].animate.set_opacity(.15),run_time=.35)
        self.at('Which ones')
        q = label('?',2.1,.6,TEXT,70)
        leader = line(P(2.1,.18),DLGN+P(0,.2),TEXT,2)
        self.play(FadeIn(q),Create(leader),run_time=.35)
        self.at('carries them away')
        self.play(FadeIn(label('What carries a contact away?',0,3.2,PURPLE,32)),run_time=.35)
        self.finish()


class S02Relay(SpokenScene):
    def construct(self):
        stage, path = brain_stage(),pathway()
        self.add(stage,path)
        self.at('visual thalamus')
        self.play(Indicate(stage[0][1],color=TEXT),run_time=.45)
        self.at('the relay')
        # An actual continuous enlargement of the marked nucleus, followed by its diagram.
        self.play(stage.animate.scale(3,about_point=DLGN).shift(-DLGN),
                  path.animate.scale(3,about_point=DLGN).shift(-DLGN),run_time=.45)
        self.play(FadeOut(stage),FadeOut(path),FadeIn(nucleus()),
                  FadeIn(label('dLGN: visual relay in the thalamus',0,3.1,TEXT,32)),run_time=.2)
        self.at('axons from')
        bundle = VGroup()
        for j in range(6):
            col = EYE_A if j%2==0 else EYE_B
            y = -.5+j*.16
            end = P(.8+(j%3)*1.3,-1.5+(j//3)*2.1)
            p = VMobject().set_points_smoothly([P(-6,y),P(-4.8,y),P(-2,y),end])
            bundle.add(VGroup(p.set_stroke(col,4),Dot(end,radius=.13,color=col)))
        self.play(Create(bundle),FadeIn(label('optic tract',-4.8,-3.15,GREY,30)),
                  Create(line(P(-5.8,-.65),P(-5.8,-2.85),GREY,2)),run_time=.65)
        self.finish()


class S03Overlap(SpokenScene):
    def construct(self):
        fa,fb = overlap_fields()
        a,b = axon_fields()
        self.add(nucleus(),map_labels(),label('newborn',3.6,3.05,TEXT,32))
        # Both fields begin entering immediately: never an empty newborn nucleus.
        self.play(FadeIn(fa),FadeIn(fb),FadeIn(a),FadeIn(b),run_time=.5)
        self.at('eyes overlap')
        self.play(Indicate(VGroup(a,b),scale_factor=1.025,color=TEXT),run_time=.55)
        self.finish()


class S04Sort(SpokenScene):
    def construct(self):
        fa,fb = overlap_fields()
        a,b = axon_fields()
        self.add(nucleus(),fa,fb,a,b,map_labels())
        day=ValueTracker(3)
        cl=always_redraw(lambda: M(f'P{int(day.get_value()+.5):02d}',32,TEXT).move_to(P(3.9,3.05)))
        self.add(cl)
        self.at('Over roughly')
        aa,bb = axon_fields(True)
        # Nearly six seconds of continuous sorting, rather than two frozen states.
        self.play(Transform(fa,field_a()),Transform(fb,patch().set_stroke(opacity=0)),
                  Transform(a,aa),Transform(b,bb),day.animate.set_value(10),run_time=5.8,rate_func=linear)
        self.finish()


class S05Patch(SpokenScene):
    def construct(self):
        self.add(sorted_map(),M('P10',32,TEXT).move_to(P(3.9,3.05)))
        self.at('territory of the opposite')
        self.play(FadeIn(label('mostly opposite eye',-2.7,1.95,EYE_A,30)),run_time=.35)
        self.at('a small patch')
        outline=patch(outline=True)
        lead=line(P(3.1,-2.75),PATCH_C+P(.65,-1.3),EYE_B,2)
        self.play(Create(outline),Create(lead),run_time=.4)
        self.add(label('schematic',0,-3.65,GREY,26))
        self.finish()


KEEP=(2,4)  # two inputs from the SAME eye; losses include both eyes.


def cell_state(later=False):
    so=VGroup(Circle(radius=1.3,color=GREY,fill_color=GREY,fill_opacity=.13),
              label('relay neuron',0,0,GREY,28))
    ax=VGroup()
    for k in range(10):
        a=18+36*k
        col=EYE_A if k%2==0 else EYE_B
        ax.add(VGroup(line(unit(a)*3.1,unit(a)*1.45,col,5),
                      Dot(unit(a)*1.45,radius=.18,color=col)))
        if later and k not in KEEP:
            ax[-1].set_opacity(.1)
    return VGroup(so,ax,label('later' if later else 'many inputs',-4.6,2.9,TEXT,40 if later else 32),
                  label('schematic, not counts',3.9,-3.2,GREY,28))


class S06Cell(SpokenScene):
    def construct(self):
        state=cell_state()
        self.add(state) # full-strength start held throughout 'many retinal inputs'.
        self.at('ends with only')
        state.remove(state[2])
        self.add(label('later',-4.6,2.9,TEXT,40))
        self.play(*[state[1][k].animate.set_opacity(.1) for k in range(10) if k not in KEEP],run_time=1.15)
        self.finish()


class S07Left(SpokenScene):
    def construct(self):
        self.add(cell_state(True))
        self.at('are removed')
        # Span the four faded inputs on the right, rather than single out one loss.
        bracket=VGroup(line(P(3.35,-2.65),P(3.35,2.65),GREY,3),
                       line(P(3.0,2.65),P(3.35,2.65),GREY,3),
                       line(P(3.0,-2.65),P(3.35,-2.65),GREY,3))
        self.play(FadeIn(label('removed',4.8,0,GREY,34)),
                  Create(bracket),run_time=.35)
        self.finish()


class S08Two(SpokenScene):
    def construct(self):
        c1,c2=box(5.8,5.6,TEXT).move_to(P(-3.1,0)),box(5.8,5.6,PURPLE).move_to(P(3.1,0))
        self.add(c1,c2)
        self.at('which inputs lose')
        self.play(FadeIn(label('?',-3.1,.65,TEXT,130)),
                  FadeIn(label('Which inputs lose?',-3.1,-1.6,TEXT,32)),run_time=.4)
        self.at('what carries')
        self.play(FadeIn(label('?',3.1,.65,PURPLE,130)),
                  FadeIn(label('What carries them away?',3.1,-1.6,PURPLE,30)),run_time=.4)
        self.finish()


class S09Waves(SpokenScene):
    def construct(self):
        # The closed eye sits beside the retina, with a full eye outline and lashes.
        ret=box(7.8,4.8).move_to(P(1.7,-.4))
        cells=VGroup(*[Dot(P(-1.55+i*.72,(j-2)*.8-.4),radius=.12,color=GREY)
                      for i in range(10) for j in range(5)])
        left,right=P(-6.05,.3),P(-3.55,.3)
        upper=ArcBetweenPoints(left,right,angle=-1.15,color=GREY,stroke_width=3)
        lower=ArcBetweenPoints(right,left,angle=-1.15,color=GREY,stroke_width=3)
        lid=ArcBetweenPoints(left,right,angle=.55,color=TEXT,stroke_width=5)
        lashes=VGroup(*[line(lid.point_from_proportion(f),
                            lid.point_from_proportion(f)+P((f-.5)*.25,-.3),TEXT,3)
                        for f in (.15,.32,.5,.68,.85)])
        self.add(ret,cells,upper,lower,lid,lashes,
                 label('eyelids closed',-4.8,1.7,GREY,28),
                 label('young retina',1.7,2.8,GREY,28))
        # A schematic travelling excitation wave, not an empirical or quantitative trace.
        clock=ValueTracker(0)
        band=Rectangle(width=.75,height=4.45,stroke_width=0,fill_color=TEXT,fill_opacity=.14)
        def wave_x(): return -1.85+(clock.get_value()%2.35)/2.35*7.1
        band.add_updater(lambda m:m.move_to(P(wave_x(),-.4)))
        for d in cells:
            d.add_updater(lambda m:m.set_color(interpolate_color(ManimColor(GREY),ManimColor(TEXT),
                                float(np.exp(-((m.get_x()-wave_x())/.65)**2)))))
        clock.add_updater(lambda m,dt:m.increment_value(dt))
        self.add(clock,band)
        self.at('spontaneous waves')
        self.play(FadeIn(label('spontaneous retinal waves',0,-3.25,TEXT,32)),run_time=.35)
        self.finish()


# Eye colours identify eyes only; rate is conveyed by white pulse trains and neutral words.
PRE_C=P(2.6,-.15)


def prediction():
    so=Circle(radius=2.35,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.12).move_to(PRE_C)
    la=line(P(-5.6,1.15),P(.6,1.15),EYE_A,6)
    lb=line(P(-5.6,-1.4),P(.6,-1.4),EYE_B,6)
    return VGroup(label('Which inputs should lose more often?',0,3.2,TEXT,36),so,
                  label('relay neuron',2.8,-.15,GREY,30),la,lb,
                  Dot(P(.6,1.15),radius=.22,color=EYE_A),Dot(P(.6,-1.4),radius=.22,color=EYE_B),
                  label('eye A',-4.9,1.7,EYE_A,28),label('eye B',-4.9,-.85,EYE_B,28))


def option(txt,x,y):
    return VGroup(box(2.6,.75,TEXT),T(txt,30,TEXT)).move_to(P(x,y))


def pulses(ln,n,period):
    dots=VGroup(*[Dot(radius=.13,color=TEXT) for _ in range(n)])
    phase=ValueTracker(0)
    phase.add_updater(lambda m,dt:m.increment_value(dt))
    for i,d in enumerate(dots):
        d.add_updater(lambda m,i=i:m.move_to(ln.point_from_proportion((phase.get_value()/period+i/n)%1)))
    return Group(phase,dots)


class S10Predict(SpokenScene):
    def construct(self):
        g=prediction()
        self.add(g)
        self.at('activity biases')
        self.add(pulses(g[3],1,4.8),pulses(g[4],5,2.5))
        self.at('the busier')
        self.play(FadeIn(option('busier',-2.4,-2.35)),run_time=.3)
        self.at('the quieter')
        self.play(FadeIn(option('quieter',-2.4,2.15)),run_time=.3)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        g=prediction()
        self.add(g,option('quieter',-2.4,2.15),option('busier',-2.4,-2.35))
        # Fixed pulse trains preserve the comparison during the five-second decision pause.
        self.add(*[Dot(g[4].point_from_proportion(f),radius=.13,color=TEXT) for f in (.1,.28,.46,.64,.82)],
                 Dot(g[3].point_from_proportion(.4),radius=.13,color=TEXT))
        self.finish()


# Same patch geometry as s05. Eye A's large surround shrinks as eye B's patch expands.
# Old border remains visible, showing the direction without inventing measured values.
def reveal_map(expanded=False):
    g=sorted_map()
    if expanded:
        g[2].become(patch(5.3,4.2).set_fill(BG,1).set_stroke(opacity=0))
        g[3].become(patch(5.3,4.2).set_stroke(opacity=0))
    # Territory comparison, with full-size labels built separately below.
    g.remove(g[4],g[5],g[6])
    g.scale(.86).stretch(.84,1).move_to(P(0,-.85))
    return g


def old_border():
    # This shared interface was also the blue field's earlier inner boundary.
    outline=reveal_map()[2].copy().set_fill(opacity=0).set_stroke(EYE_B,3,opacity=.7)
    return VGroup(outline,label('earlier border',.5,.6,GREY,26),
                  line(P(1.5,.45),outline.get_top()+P(-.3,0),GREY,2))


def reveal_stage(final=False):
    mp=reveal_map(final)
    ea,eb=eye(P(-3,2.3),EYE_A),eye(P(3,2.3),EYE_B)
    if final: ea.set_opacity(.3)
    return VGroup(mp,ea,eb,label('eye A · treated',-3,3.25,EYE_A,30),
                  label('eye B · control',3,3.25,EYE_B,30),
                  label('eye-level schematic',0,-3.55,GREY,28),
                  label('dLGN',-3.7,.6,GREY,30))


def reveal_end():
    g=reveal_stage(True)
    g.add(old_border(),label('silenced',-3,1.48,GREY,28),
          label('do microglia follow?',0,-3.02,PURPLE,32))
    return g


class S12Reveal(SpokenScene):
    def construct(self):
        g=reveal_stage()
        self.add(g)
        activity_label=label('activity reduced',-3,1.48,GREY,28)
        self.at('change one')
        self.play(g[1].animate.set_opacity(.3),FadeIn(activity_label),run_time=.45)
        self.at('quieter ones')
        old=old_border()
        self.add(old)
        self.play(Transform(g[0],reveal_map(True)),run_time=1.15)
        self.at('silences one eye')
        # The later silencing test uses the same dimmed eye, with one manipulation label.
        self.remove(activity_label)
        self.play(FadeIn(label('silenced',-3,1.48,GREY,28)),run_time=.3)
        self.at('whether microglia')
        self.play(FadeIn(label('do microglia follow?',0,-3.02,PURPLE,32)),run_time=.35)
        self.finish()


class S13Beat(NarratedScene):
    def construct(self):
        self.add(reveal_end())
        self.finish()


class S14Microglia(SpokenScene):
    def construct(self):
        g=reveal_end()
        self.add(g)
        self.at('second question')
        stage=VGroup(nucleus(),label('dLGN',-4.5,2.95,GREY,32))
        # Context remains segregated; terminals sit outside the cell and its label area.
        terminals=VGroup(*[VGroup(line(P(x-.4,y),P(x+.4,y+.12),EYE_A,4),
                                 Dot(P(x+.4,y+.12),radius=.14,color=EYE_A))
                            for x,y in [(-4,-1.6),(-4,.4),(-3,1.7),(3.8,-1.5),(4,.8),(2.8,1.7)]])
        self.play(FadeOut(g),FadeIn(stage),FadeIn(terminals),run_time=.5)
        self.at('are microglia')
        mg=microglia(P(0,-.2),1.15)
        self.play(FadeIn(mg),FadeIn(label('microglia',0,3.35,PURPLE,34)),run_time=.4)
        self.at('resident immune cells')
        self.play(FadeIn(label('resident immune cells',0,-2.95,PURPLE,30)),run_time=.35)
        self.at('main phagocytes')
        self.play(FadeIn(label('main phagocytes',0,2.75,PURPLE,30)),run_time=.3)
        self.finish()


# Illustrated rows fill the frame. Empty row furniture is present at scene start;
# claims and named concepts enter only on their spoken cues.
ROW_Y=(1.75,-.15,-2.05)


def idea_header(): return label('The one idea to carry through',0,3.2,GREY,34)


def idea_frame():
    return VGroup(idea_header(),*[box(12,1.65).move_to(P(0,y)) for y in ROW_Y])


def idea_item(i):
    y=ROW_Y[i]
    if i==0:
        icon=VGroup(eye(P(-4.9,y+.1),EYE_A).scale(.6).set_opacity(.3),
                    eye(P(-3.6,y+.1),EYE_B).scale(.6))
        txt=VGroup(T('Relative activity biases',30,TEXT),T('which retinal inputs lose',30,TEXT)).arrange(DOWN,buff=.12).move_to(P(1.1,y))
    elif i==1:
        icon=microglia(P(-4.3,y),.38)
        txt=VGroup(T('Microglia take relatively more',30,PURPLE),T('from the quieter eye',30,PURPLE)).arrange(DOWN,buff=.12).move_to(P(1.1,y))
    else:
        icon=chip('complement',YELLOW,26).move_to(P(-4.3,y))
        txt=VGroup(T('Complement helps them eat',30,YELLOW),T('part of that',30,YELLOW)).arrange(DOWN,buff=.12).move_to(P(1.1,y))
    return VGroup(icon,txt)


class S15Idea(SpokenScene):
    def construct(self):
        # Reuse the prediction's comparison as a large first card during the introduction.
        intro=VGroup(box(12,5.8).move_to(P(0,-.2)),
            eye(P(-3,.7),EYE_A).scale(1.6).set_opacity(.3),
            eye(P(3,.7),EYE_B).scale(1.6),
            label('eye A · quieter',-3,-.55,EYE_A,32),
            label('eye B · busier',3,-.55,EYE_B,32),
            line(P(-5,-1.65),P(-1,-1.65),EYE_A,5),
            line(P(1,-1.65),P(5,-1.65),EYE_B,5),
            Dot(P(-3,-1.65),radius=.15,color=TEXT),
            *[Dot(P(x,-1.65),radius=.15,color=TEXT) for x in (1.3,2.15,3,3.85,4.7)])
        heading=idea_header()
        self.add(heading,intro)
        self.at('Relative activity biases')
        self.play(FadeOut(intro),FadeOut(heading),FadeIn(idea_frame()),FadeIn(idea_item(0)),run_time=.4)
        self.at('microglia take relatively')
        self.play(FadeIn(idea_item(1)),run_time=.35)
        self.at('Complement helps')
        self.play(FadeIn(idea_item(2)),run_time=.35)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        self.add(idea_frame(),*[idea_item(i) for i in range(3)])
        self.finish()


def scope_header(): return label('The rule has a scope',0,3.25,GREY,34)


def scope1(full=True):
    icon=VGroup(box(1.6,.9,EYE_A,.25),patch().scale(.2).move_to(P(.4,0))).move_to(P(-4.8,1.95))
    txt=label('Mouse dLGN',-1.6,2.15,TEXT,32)
    day=label('about P3 to P10',2.45,2.15,TEXT,32)
    return VGroup(box(12,1.3).move_to(P(0,2.1)),icon,txt,day if full else VGroup())


def scope2(full=True):
    return VGroup(box(12,1.45,YELLOW).move_to(P(0,.55)),
        chip('complement',YELLOW,26).move_to(P(-4.35,.55)),
        label('Needed for normal sorting',1.15,.85,YELLOW,30),
        label('Not shown to carry activity information',1.15,.22,GREY,28) if full else VGroup())


def scope_base(): return VGroup(scope_header(),scope1(),scope2())


class S17Scope1(SpokenScene):
    def construct(self):
        row=scope1(False)
        illustration=sorted_map()
        illustration.remove(illustration[6])
        illustration.scale(.65).move_to(P(0,-1.2))
        self.add(scope_header(),row[0],row[1],illustration,
                 label('eye territories · schematic',0,-3.3,GREY,28))
        self.at('mouse visual thalamus')
        self.play(FadeIn(row[2]),run_time=.35)
        self.at('first week')
        self.play(FadeIn(scope1()[3]),run_time=.35)
        self.finish()


class S18Scope3(SpokenScene):
    def construct(self):
        row=scope2(False)
        illustration=VGroup(nucleus(),*overlap_fields(),*axon_fields())
        illustration.scale(.52).move_to(P(0,-1.9))
        target=sorted_map()
        target.remove(target[6])
        target.scale(.52).move_to(P(0,-1.9))
        self.add(scope_header(),scope1(),row[0],row[1],illustration)
        self.at('needed for normal sorting')
        self.play(FadeIn(row[2]),Transform(illustration,target),run_time=1.0)
        self.at('did not show')
        self.play(FadeIn(scope2()[3]),run_time=.35)
        self.finish()


def astrocyte(c):
    body=Circle(radius=.42,color=GREY,fill_color=GREY,fill_opacity=.25).move_to(c)
    arms=VGroup(*[line(c+unit(a)*.3,c+unit(a)*1.05,GREY,6) for a in range(0,360,45)])
    return VGroup(arms,body)


class S19Scope4(SpokenScene):
    def construct(self):
        # Compact prior scope rows to give both phagocytes space and legible captions.
        self.add(scope_base())
        self.at('part means part')
        self.play(FadeIn(label('Part of the eating, not all',0,-.65,TEXT,32)),run_time=.3)
        self.at('eating goes on')
        mg=microglia(P(-3.4,-1.9),.5)
        syn=Dot(P(-1.8,-1.75),radius=.15,color=EYE_A)
        self.play(FadeIn(mg),FadeIn(syn),run_time=.3)
        self.at("without complement's receptor")
        # A receptor cup and stem can be crossed out without obscuring any words.
        rec=VGroup(line(P(-1.35,-1.45),P(-1.35,-1.8),TEAL,5),
                   line(P(-1.35,-1.8),P(-.85,-1.8),TEAL,5),
                   line(P(-.85,-1.8),P(-.85,-1.45),TEAL,5),
                   line(P(-1.1,-1.8),P(-1.1,-2.15),TEAL,5))
        cross=Cross(rec,stroke_color=RED,stroke_width=5).scale(1.25)
        self.play(FadeIn(rec),Create(cross),syn.animate.move_to(P(-3.4,-1.9)),
                  FadeIn(label('eats without the receptor',-3.1,-3.45,PURPLE,28)),run_time=.5)
        self.at('Astrocytes eat')
        ast=astrocyte(P(3.4,-1.95))
        syn2=Dot(P(4.65,-1.7),radius=.17,color=EYE_A)
        self.play(FadeIn(ast),FadeIn(syn2),FadeIn(label('astrocyte',3.4,-3.45,GREY,30)),run_time=.2)
        self.play(syn2.animate.move_to(P(3.4,-1.95)),run_time=.6)
        # Hold the full result for >3 seconds, so a three-second review sample catches it.
        self.wait(max(.01,9.4-self.elapsed()))
        self.finish()


class S20Take(SpokenScene):
    def construct(self):
        L=box(5.15,5.8,PURPLE).move_to(P(-3.75,0))
        R=box(5.15,5.8,YELLOW).move_to(P(3.75,0))
        # Two semantic lines each wrap within their box, preserving the requested clause breaks.
        lt=VGroup(T('Activity biases',30,TEXT),T('which inputs lose',30,TEXT),
                  T('and what microglia take',28,PURPLE)).arrange(DOWN,buff=.3).move_to(L)
        rt=VGroup(T('Complement helps',30,YELLOW),T('them eat',30,YELLOW),
                  T('part of it',30,YELLOW)).arrange(DOWN,buff=.3).move_to(R)
        self.add(L,R,lt,rt)
        self.at('two findings')
        self.at('still open')
        self.play(Create(DashedLine(P(-1.05,0),P(1.05,0),color=GREY,stroke_width=4)),
                  FadeIn(label('open',0,.75,TEXT,40)),run_time=.3)
        self.finish()


class S21End(EndCard):
    # Same Georgia EndCard as ch2/ch3; ch3 repeats both findings in its closing narration.
    LINE = 'How activity and complement connect is still open.'

    def construct(self):
        text=T(self.LINE,40,TEXT,font=TITLE_FONT)
        fit(text,max_w=11.5)
        footer=T('biochemistrypedia.com',28,TEAL)
        VGroup(text,footer).arrange(DOWN,buff=.4)
        self.play(FadeIn(text),FadeIn(footer),run_time=.5)
        self.finish()
