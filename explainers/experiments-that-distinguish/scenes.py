"""Experiments that distinguish mechanisms: read the whole distribution  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  ORANGE = cytochrome oxidase / the mitochondrial marker
  BLUE   = acid phosphatase / the lysosome marker
  PURPLE = the unknown enzyme X
  GREY   = protein, tubes, membranes, outlines, the starting mixture
  YELLOW = the thing we are asking about / fraction L / the question mark
  GREEN  = enriched, measured activity (the gauge)
  RED    = not pure
  GOLD   = substrate (the little dots)
  PINK   = detergent
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FC0"

FR = ["N", "M", "L", "P", "S"]
PROT = [15, 20, 5, 20, 40]
CYT = [10, 70, 15, 5, 0]
ACP = [8, 25, 45, 12, 10]
XX = [9, 24, 44, 13, 10]


def rsa(a):
    return [x / p for x, p in zip(a, PROT)]


def bar(x, base, h, w, color, op=0.9):
    r = Rectangle(width=w, height=max(h, 0.03), stroke_width=0, fill_color=color, fill_opacity=op)
    return r.move_to([x, base + max(h, 0.03) / 2, 0])


def tube(x, y, w=1.0, h=1.9, pellet=True):
    t = RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREY, stroke_width=4,
                         fill_color=GREY, fill_opacity=0.10).move_to([x, y, 0])
    g = VGroup(t)
    if pellet:
        p = Ellipse(width=w * 0.72, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=0.85)
        p.move_to([x, y - h / 2 + 0.3, 0])
        g.add(p)
    return g


def rsa_plot(scale=0.5, base=-2.95, xs=(-4.8, -2.4, 0.0, 2.4, 4.8), w=0.6, gap=0.75):
    """Grouped bars of relative specific activity, computed from the lesson's table."""
    out = {"cyt": [], "acp": [], "x": [], "letters": [], "xs": xs, "base": base, "scale": scale}
    for name, arr, col, off in (("cyt", CYT, ORANGE, -gap), ("acp", ACP, BLUE, 0), ("x", XX, PURPLE, gap)):
        for i, v in enumerate(rsa(arr)):
            out[name].append(bar(xs[i] + off, base, v * scale, w, col))
    for i, f in enumerate(FR):
        out["letters"].append(T(f, 30).move_to([xs[i], base - 0.33, 0]))
    out["line"] = Line([xs[0] - 1.2, base, 0], [xs[-1] + 1.2, base, 0], color=GREY, stroke_width=3)
    return out


def val(text, bar_mob, color, size=22):
    return M(text, size, color).next_to(bar_mob, UP, buff=0.1)


def gauge(x, y_base, h, frac, title=None):
    frame = Rectangle(width=0.7, height=h, stroke_color=GREY, stroke_width=4).move_to([x, y_base + h / 2, 0])
    fill = bar(x, y_base, h * frac, 0.7, GREEN, 0.85)
    return frame, fill




def legend3():
    a = chip("cytochrome oxidase", ORANGE, size=22).move_to([-4.0, 3.1, 0])
    b = chip("acid phosphatase", BLUE, size=22).move_to([0.0, 3.1, 0])
    c = chip("unknown enzyme X", PURPLE, size=22).move_to([4.0, 3.1, 0])
    return a, b, c

def particle(cx, cy, r=1.25, closed=True):
    if closed:
        return Circle(radius=r, stroke_color=GREY, stroke_width=7).move_to([cx, cy, 0])
    arcs = VGroup()
    for k in range(4):
        a = Arc(radius=r, start_angle=k * PI / 2 + 0.3, angle=PI / 2 - 0.6, arc_center=[cx, cy, 0],
                stroke_color=GREY, stroke_width=7)
        arcs.add(a)
    return arcs

def ghost(text, x, y, color=PURPLE, op=0.45):
    c = chip(text, color, size=26)
    c.set_opacity(op)
    return c.move_to([x, y, 0])

# Additional uses of the existing palette:
# GREY = intended protein / mRNA / compartments; RED = defect or failed readout;
# GREEN = recovered behavior / measured readout; YELLOW = labelled cohort / questions.


def label(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


def arrow(a, b, color=GREY):
    return Arrow(a, b, buff=0.16, color=color, stroke_width=4, tip_length=0.2)


def cell(x, y, protein=True):
    outline = Circle(1.05, stroke_color=GREY, stroke_width=4,
                     fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])
    inside = chip('protein' if protein else 'depleted', GREY, size=24).move_to(outline)
    return VGroup(outline, inside)


def blot(names, levels, x=0, y=-1.8):
    """Schematic immunoblot: target row and equal loading-reference row."""
    g = VGroup(label('protein', x-4.6, y+0.25, GREY, 22),
               label('loading', x-4.6, y-0.55, GREY, 22))
    for i, (name, level) in enumerate(zip(names, levels)):
        cx = x-2.6+i*2.4
        g.add(label(name, cx, y+1, GREY, 22))
        g.add(Line([cx-.55,y+.25,0],[cx+.55,y+.25,0],
                   color=TEXT,stroke_width=9).set_opacity(level))
        g.add(Line([cx-.55,y-.55,0],[cx+.55,y-.55,0],color=GREY,stroke_width=9))
    return g


class S00Title(TitleCard):
    LESSON = 'Experiments That Distinguish Mechanisms'
    TITLE = 'Experiments That Distinguish Mechanisms'


class S01Cause(SpokenScene):
    def construct(self):
        c = cell(-3, .6)
        outcome = chip('normal behavior', GREEN, size=28).move_to([3,.6,0])
        a = arrow([-1.7,.6,0],[1,.6,0])
        self.at('Removing a protein')
        self.play(FadeIn(c), FadeIn(outcome), GrowArrow(a), run_time=.6)
        depleted = cell(-3,.6,False)
        defect = chip('defect', RED, size=28).move_to(outcome)
        self.at('can cause a defect')
        self.play(Transform(c,depleted), Transform(outcome,defect),run_time=.6)
        question = label('What caused the defect?',0,3,YELLOW,34)
        loss = chip('intended protein loss?',GREY,26).move_to([-3,-1.8,0])
        off = chip('off-target effect?',YELLOW,26).move_to([3,-1.8,0])
        self.at('but that alone')
        self.play(FadeIn(question), FadeIn(loss),run_time=.6)
        self.at('may affect something else')
        self.play(FadeIn(off),run_time=.6)
        control = chip('independent control',GREY,26).move_to([-3,-1.8,0])
        self.at('Use independent controls')
        self.play(ReplacementTransform(loss,control),FadeOut(off),run_time=.6)
        rescue = chip('rescue: protein returned',GREY,26).move_to([3,-1.8,0])
        self.at('then put the protein back')
        self.play(FadeIn(rescue),Transform(c,cell(-3,.6)),run_time=.7)
        self.at('If the defect goes away')
        self.play(Transform(outcome,chip('normal behavior',GREEN,28).move_to(outcome)),run_time=.6)
        evidence = label('Strong evidence',0,-3,GREEN,32)
        self.at('rescue is strong evidence')
        self.play(FadeIn(evidence),run_time=.6)
        self.at('finding a protein')
        self.play(*[FadeOut(m) for m in (c,outcome,a,control,rescue,evidence)],
                  Transform(question,label('Location + timing',0,2,YELLOW,34)),run_time=.7)
        location = chip('right place',GREY,30).move_to([-3,.3,0])
        timing = chip('right time',GREY,30).move_to([3,.3,0])
        self.play(FadeIn(location),FadeIn(timing),run_time=.5)
        causal = label('Cause still needs a test',0,-1.7,RED,32)
        self.at('does not show that it causes anything')
        self.play(FadeIn(causal),run_time=.7)
        self.at('These experiments test different questions')
        self.play(Indicate(causal,scale_factor=1.04),run_time=.7)
        self.finish()


class S02Rescue(SpokenScene):
    def construct(self):
        heading = label('Independent depletion + resistant rescue',0,3.1,TEXT,32)
        mrna = chip('original mRNA',GREY,30).move_to([0,.6,0])
        h1 = chip('hairpin 1',YELLOW,26).move_to([-3,1.9,0])
        site1 = Rectangle(width=1.1,height=.15,color=YELLOW,fill_opacity=1).move_to([-1,.1,0])
        self.at('A short hairpin')
        self.play(FadeIn(heading),FadeIn(mrna),FadeIn(h1),run_time=.6)
        self.at('by targeting its messenger')
        self.play(h1.animate.move_to([-2,-.8,0]),Create(site1),run_time=.6)
        h2 = chip('hairpin 2',YELLOW,26).move_to([3,-.8,0])
        site2 = site1.copy().move_to([1,.1,0])
        self.at('Use another hairpin')
        self.play(FadeIn(h2),Create(site2),run_time=.6)
        self.at('check that the protein is lost')
        b = blot(['control','hairpin 1','hairpin 2'],[1,.08,.08],y=-2)
        self.play(FadeOut(h1),FadeOut(h2),FadeOut(site1),FadeOut(site2),FadeIn(b),run_time=.6)
        self.at('For rescue')
        original = chip('original mRNA',GREY,28).move_to([-3,1.5,0])
        resistant = chip('rescue mRNA',GREY,28).move_to([-3,-.3,0])
        protein = chip('same protein',GREY,30).move_to([3,.6,0])
        a1 = arrow([-1.1,1.5,0],[1.5,.8,0])
        a2 = arrow([-1.1,-.3,0],[1.5,.4,0])
        self.play(FadeOut(b),Transform(mrna,original),FadeIn(resistant),run_time=.6)
        changes = VGroup(*[Rectangle(width=.2,height=.18,color=YELLOW,fill_opacity=1)
                           .move_to([-3+dx,-.75,0]) for dx in (-.55,0,.55)])
        self.at('silent mutations change the messenger')
        self.play(FadeIn(changes),run_time=.5)
        self.at('but keep the protein the same')
        self.play(GrowArrow(a1),GrowArrow(a2),FadeIn(protein),run_time=.7)
        hp = chip('hairpin',YELLOW,26).move_to([-3,-1.8,0])
        blocked = label('no pairing',0,-2.7,RED,26)
        self.at('The hairpin cannot pair')
        self.play(FadeIn(hp),run_time=.3)
        self.play(hp.animate.shift(UP*.4),run_time=.4)
        self.play(hp.animate.shift(DOWN*.4),FadeIn(blocked),run_time=.4)
        self.at('Check that the rescue protein')
        check = blot(['normal','empty vector','rescue'],[1,.08,1],y=-.3)
        self.play(*[FadeOut(m) for m in (mrna,resistant,protein,a1,a2,changes,hp,blocked)],FadeIn(check),run_time=.6)
        note = label('Rescue expression ≈ normal level',0,-2.5,GREEN,30)
        self.at('at about its normal level')
        self.play(FadeIn(note),run_time=.6)
        self.finish()


class S03SeparateJobs(SpokenScene):
    def construct(self):
        title = label('Which clathrin job matters?',0,3.1,TEXT,34)
        defect = chip('depleted: prolonged mitosis',RED,30).move_to([0,1.3,0])
        spindle = chip('spindle defect?',YELLOW,28).move_to([-3.2,-.7,0])
        indirect = chip('indirect: endocytosis?',YELLOW,28).move_to([3,-.7,0])
        self.at('Now ask which job matters')
        self.play(FadeIn(title),FadeIn(defect),FadeIn(spindle),FadeIn(indirect),run_time=.6)
        self.at('Depleting clathrin')
        self.play(Indicate(defect,scale_factor=1.03),run_time=.6)
        self.at('Was that a spindle defect')
        self.play(Indicate(spindle,scale_factor=1.03),run_time=.5)
        self.at('or an indirect effect')
        self.play(Indicate(indirect,scale_factor=1.03),run_time=.5)
        # Qualitative states, rather than invented quantitative measurements.
        heads=VGroup(label('resistant construct',-3.8,1.7,GREY,24),
                     label('mitosis duration',.2,1.7,GREY,24),
                     label('transferrin uptake',4,1.7,GREY,24))
        duration = Line([-.9,.22,0],[1.3,.22,0],color=GREY,stroke_width=5)
        rows=VGroup(duration,label('depleted',-3.8,.6,GREY,26),label('prolonged',.2,.6,RED,26),label('impaired',4,.6,RED,26))
        normal_time = Line([-.9,-.88,0],[-.15,-.88,0],color=GREY,stroke_width=5)
        full=VGroup(normal_time,label('full length',-3.8,-.5,GREY,26),label('rescued',.2,-.5,GREEN,26))
        partial_time = duration.copy().shift(DOWN*2.2)
        short=VGroup(label('shortened',-3.8,-1.6,GREY,26),label('partial rescue',.2,-1.6,GREEN,26))
        failed=label('not supported',4,-1.6,RED,26)
        self.at('resistant clathrin rescued mitosis')
        self.play(FadeOut(defect),FadeOut(spindle),FadeOut(indirect),FadeIn(heads),FadeIn(rows),FadeIn(full),run_time=.7)
        self.at('A shortened version partly rescued mitosis')
        self.play(FadeIn(short),FadeIn(partial_time),run_time=.3)
        self.play(Transform(partial_time,Line([-.9,-1.98,0],[.5,-1.98,0],color=GREY,stroke_width=5)),run_time=.6)
        self.at('while failing to support transferrin uptake')
        self.play(FadeIn(failed),run_time=.6)
        qualitative=label('Duration bars are qualitative',3.8,-2.5,GREY,22)
        self.play(FadeIn(qualitative),run_time=.3)
        rule=chip('separation of function',YELLOW,30).move_to([0,-3.15,0])
        self.at('Keeping part of one function')
        self.play(Indicate(short[1],scale_factor=1.06),Indicate(failed,scale_factor=1.06),run_time=.7)
        self.at('the jobs are separate')
        self.play(FadeIn(rule),run_time=.6)
        self.at('Score both functions')
        self.play(Indicate(heads[1:],scale_factor=1.04),run_time=.8)
        self.finish()


class S04PulseChase(SpokenScene):
    def construct(self):
        title=label('Follow one labelled batch',0,3.1,TEXT,34)
        batch=VGroup(*[Dot([x,.4,0],radius=.13,color=YELLOW) for x in (-.45,0,.45)])
        pulse=chip('pulse: labelled amino acid',YELLOW,28).move_to([-3.2,1.8,0])
        chase=chip('chase: unlabelled amino acid',GREY,28).move_to([3.1,1.8,0])
        self.at('A different question')
        self.play(FadeIn(title),FadeIn(pulse),FadeIn(chase),FadeIn(batch),run_time=.6)
        self.at('In what order')
        q=label('Which compartment comes first?',0,-1.4,YELLOW,30)
        self.play(FadeIn(q),run_time=.5)
        self.at('A short pulse')
        self.play(Indicate(pulse,scale_factor=1.03),Indicate(batch,scale_factor=1.1),run_time=.6)
        self.at('A chase with')
        self.play(FadeOut(pulse),chase.animate.move_to([0,1.8,0]),FadeOut(q),run_time=.6)
        self.at('In pancreatic slices')
        caption=label('Pancreatic slices • measured fractions',0,2.2,GREY,26)
        compartments=VGroup(*[chip(t,GREY,26).move_to([x,-.5,0])
                              for t,x in zip(('ER fragments','Golgi fractions','granule fraction'),(-4.3,0,4.3))])
        self.play(FadeOut(chase),FadeIn(caption),FadeIn(compartments),run_time=.6)
        self.at('label appeared first')
        self.play(batch.animate.move_to([-4.3,.4,0]),run_time=.6)
        self.at('then in Golgi fractions')
        self.play(batch.animate.move_to([0,.4,0]),run_time=.7)
        self.at('then in the granule fraction')
        self.play(batch.animate.move_to([4.3,.4,0]),run_time=.7)
        caveat=label('Early granule-fraction label: condensing vacuoles\nA fraction is not an organelle identification',0,-2.5,GREY,24)
        self.play(FadeIn(caveat),run_time=.6)
        self.at('That gives an order')
        self.play(Indicate(compartments,scale_factor=1.03),run_time=.6)
        self.at('It does not choose between')
        self.play(*[FadeOut(m) for m in (caption,compartments,batch,caveat)],
                  Transform(title,label('Same order; two possible mechanisms',0,3.1,TEXT,32)),run_time=.6)
        l=chip('budding + fusion',GREY,28).move_to([-3.2,1.8,0])
        r=chip('compartment maturation',GREY,28).move_to([3,1.8,0])
        # Fixed compartments exchange a labelled carrier on the left.
        source=VGroup(*[RoundedRectangle(width=1.25,height=.85,corner_radius=.2,color=GREY)
                         .move_to([x,0,0]) for x in (-5.4,-3.4,-1.4)])
        organelles=VGroup(*[label(t,x,-.85,GREY,22)
                            for t,x in zip(('ER','Golgi','granule'),(-5.4,-3.4,-1.4))])
        ves=VGroup(Circle(.23,color=YELLOW,fill_opacity=.15),Dot(radius=.08,color=YELLOW))
        ves.move_to([-5.4,0,0])
        # The labelled cargo stays inside one cisterna as its identity changes.
        def cisterna(name, width, height):
            membrane=RoundedRectangle(width=width,height=height,corner_radius=.3,color=GREY).move_to([3,0,0])
            cargo=VGroup(*[Dot([3+dx,0,0],radius=.09,color=YELLOW) for dx in (-.3,0,.3)])
            return VGroup(membrane,cargo,label(name,3,-1,GREY,24))
        mature=cisterna('ER',2.4,.7)
        self.at('vesicles budding and fusing')
        self.play(FadeIn(l),Create(source),FadeIn(organelles),FadeIn(ves),run_time=.4)
        self.play(ves.animate.move_to([-3.4,0,0]),run_time=.7)
        self.play(Indicate(source[1],scale_factor=1.05),run_time=.3)
        self.play(ves.animate.move_to([-1.4,0,0]),run_time=.7)
        self.play(Indicate(source[2],scale_factor=1.05),run_time=.3)
        self.at('and compartments maturing')
        self.play(FadeIn(r),FadeIn(mature),run_time=.4)
        self.play(Transform(mature,cisterna('Golgi',2,.95)),run_time=.7)
        self.play(Transform(mature,cisterna('granule',1.4,1.3)),run_time=.7)
        limit=label('Timing alone does not select a mechanism',0,-2.3,YELLOW,30)
        self.play(FadeIn(limit),run_time=.6)
        self.finish()


class S03Profile(SpokenScene):
    def construct(self):
        title=label('Where does enzyme X live?',0,3.15,TEXT,32)
        p=rsa_plot(scale=.39,base=-2.6)
        la,lb,lc=legend3()
        legends=VGroup(la,lb,lc).shift(DOWN*.85)
        axis=VGroup(p['line'],*p['letters'],label('Relative specific activity • made-up data',0,-3.63,GREY,22))
        acp=VGroup(*p['acp']); xx=VGroup(*p['x']); cyt=VGroup(*p['cyt'])
        self.at('Finally where does an enzyme live')
        self.play(FadeIn(title),FadeIn(axis),FadeIn(legends),
                  LaggedStart(*[GrowFromEdge(b,DOWN) for b in (*xx,*acp,*cyt)],lag_ratio=.03),run_time=.8)
        self.at('fractionation table')
        self.play(Indicate(axis,scale_factor=1),run_time=.5)
        self.at('enzyme X follows')
        self.play(Indicate(xx,scale_factor=1.02),run_time=.7)
        self.at('acid phosphatase profile')
        self.play(Indicate(acp,scale_factor=1.02),run_time=.7)
        self.at('rather than the mitochondrial marker')
        self.play(Indicate(cyt,scale_factor=1.02),run_time=.7)
        tag=chip('X: provisionally lysosomal',BLUE,28).move_to([0,3.15,0])
        self.at('That makes X provisionally lysosomal')
        self.play(ReplacementTransform(title,tag),run_time=.5)
        self.at('Enrichment is not purity')
        mixed=tube(-3,0,w=3.2,h=3,pellet=False)
        contents=VGroup(chip('acid phosphatase',BLUE,22).move_to([-3,.7,0]),
                        chip('X',PURPLE,26).move_to([-3,-.15,0]),
                        chip('cyt. oxidase',ORANGE,22).move_to([-3,-1,0]))
        mixnote=label('Fraction L\nenriched, mixed',2.5,0,YELLOW,32)
        self.play(*[FadeOut(m) for m in (axis,legends,acp,xx,cyt)],FadeIn(mixed),FadeIn(contents),FadeIn(mixnote),run_time=.7)
        self.at('Activity revealed by opening a membrane')
        mem=particle(-3,0)
        x=ghost('X',-3,0)
        frame,low=gauge(2,-1.6,2.8,.1)
        act=label('measured activity',2,-2.3,GREY,24)
        self.play(FadeOut(mixed),FadeOut(contents),FadeOut(mixnote),Create(mem),FadeIn(x),Create(frame),FadeIn(low),FadeIn(act),run_time=.5)
        self.play(ReplacementTransform(mem,particle(-3,0,closed=False)),
                  Transform(low,bar(2,-1.6,2.8,.7,GREEN,.85)),x.animate.set_opacity(1),run_time=.7)
        supports=label('Supports membrane enclosure',0,-3.1,GREEN,28)
        self.at('supports enclosure')
        self.play(FadeIn(supports),run_time=.5)
        self.at('A second lysosomal marker')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not tag],run_time=.4)
        gradient=tube(-3,0,w=1.8,h=3.4,pellet=False)
        bands=VGroup(Line([-3.6,-.5,0],[-2.4,-.5,0],color=BLUE,stroke_width=8),
                     Line([-3.6,-.8,0],[-2.4,-.8,0],color=PURPLE,stroke_width=8))
        gl=label('Second lysosomal marker + X\non a density gradient',-3,-2.5,GREY,24)
        self.play(FadeIn(gradient),FadeIn(bands),FadeIn(gl),run_time=.6)
        self.at('and imaging in intact cells')
        intact=particle(3,0,r=1.35)
        spots=VGroup(*[Dot([3+dx,dy,0],radius=.12,color=PURPLE) for dx,dy in ((-.5,.3),(.4,.5),(.1,-.5))])
        il=label('Image X in intact cells',3,-2.5,GREY,24)
        self.play(Create(intact),FadeIn(spots),FadeIn(il),run_time=.6)
        self.at('would help confirm the assignment')
        self.play(Indicate(tag,scale_factor=1.04),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Rescue tests causal attribution. Pulse-chase tests order. Fractionation tests compartment assignment."
