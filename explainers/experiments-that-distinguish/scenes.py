"""Where the Twins Disagree.

COLOR MAP (one colour per concept, whole film)
  TEAL   = Model 1 / lysosome mechanism
  ORANGE = Model 2 / mitochondrion or alternative-target mechanism
  PURPLE = protein X / kinase / its message
  GOLD   = intervention, labelled cohort, or decisive result
  GREY   = shared structure, unchanged result, original curve
  WHITE  = questions and measured outlines

All plotted values below are computed from the lesson table or from the explicitly
schematic dose-response equation declared beside the helper that draws it.
"""
from bp_style import *  # noqa: F401,F403
import numpy as np

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
FRACS = ["N", "M", "L", "P", "S"]
PROTEIN = np.array([15, 20, 5, 20, 40], dtype=float)
LYSO = np.array([8, 25, 45, 12, 10], dtype=float)
MITO = np.array([10, 70, 15, 5, 0], dtype=float)
UNKNOWN = np.array([9, 24, 44, 13, 10], dtype=float)


def label(text, x=0, y=0, color=TEXT, size=30, **kw):
    return T(text, size=size, color=color, **kw).move_to([x, y, 0])


def twin_cell(x, color, radius=2.05):
    cell = Circle(radius, stroke_color=color, stroke_width=6,
                  fill_color=color, fill_opacity=0.18).move_to([x, 0.15, 0])
    # Slow breathing keeps the living subject alive while a sentence lands.
    cell._phase, cell._pulse = (0.7 if x > 0 else 0.0), 1.0
    def breathe(mob, dt):
        mob._phase += dt
        new = 1.0 + 0.035 * np.sin(mob._phase * 1.15)
        mob.scale(new / mob._pulse, about_point=mob.get_center())
        mob._pulse = new
    cell.add_updater(breathe)
    return cell


def protein_blob(x, y=0.15, scale=1.0):
    return Ellipse(width=0.76 * scale, height=0.54 * scale, color=PURPLE,
                   stroke_width=3, fill_color=PURPLE, fill_opacity=0.85).move_to([x, y, 0])


def twins(with_models=True, with_proteins=True):
    left, right = twin_cell(-3.15, TEAL), twin_cell(3.15, ORANGE)
    g = VGroup(left, right)
    if with_proteins:
        g.add(protein_blob(-3.15), protein_blob(3.15))
    if with_models:
        g.add(label("Model 1", -3.15, 2.75, TEAL, 32),
              label("Model 2", 3.15, 2.75, ORANGE, 32))
    return g


def bottom_bar(text="", color=GREY):
    box = RoundedRectangle(width=11.8, height=0.76, corner_radius=0.12,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.13).move_to([0, -3.18, 0])
    return VGroup(box, label(text, 0, -3.18, color, 30, weight=BOLD))


def tube(x, y, color=GREY, w=0.72, h=2.15):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.25,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.17).move_to([x, y, 0])
    body._phase, body._pulse = x * .4, 1.0
    def tube_breathe(mob, dt):
        mob._phase += dt
        new = 1.0 + .035 * np.sin(mob._phase * 1.1)
        mob.scale([new / mob._pulse, 1, 1], about_point=mob.get_center())
        mob._pulse = new
    body.add_updater(tube_breathe)
    pellet = Ellipse(width=w * 0.72, height=0.22, stroke_width=0,
                     fill_color=color, fill_opacity=0.6).move_to([x, y - h / 2 + 0.25, 0])
    pellet._phase, pellet._pulse = x, 1.0
    def settle(mob, dt):
        mob._phase += dt
        new = 1.0 + 0.05 * np.sin(mob._phase * 1.25)
        mob.scale(new / mob._pulse, about_point=mob.get_center())
        mob._pulse = new
    pellet.add_updater(settle)
    return VGroup(body, pellet)


def tube_row(cx, color, y=-0.45, spacing=0.83):
    xs = [cx + (i - 2) * spacing for i in range(5)]
    tubes = VGroup(*[tube(x, y, color) for x in xs])
    letters = VGroup(*[label(f, x, y - 1.38, TEXT, 28) for x, f in zip(xs, FRACS)])
    return VGroup(tubes, letters), xs


def chart_axes(center=(0, -0.1), width=9.1, height=4.7):
    cx, cy = center
    x0, y0 = cx - width / 2, cy - height / 2
    pane = Rectangle(width=width, height=height, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.16).move_to([cx, cy, 0]).set_z_index(-2)
    pane._phase, pane._pulse = 0.0, 1.0
    def live_readout(mob, dt):
        mob._phase += dt
        new = 1.0 + .025 * np.sin(mob._phase * 1.2)
        mob.scale([new / mob._pulse, 1, 1], about_point=mob.get_center())
        mob._pulse = new
    pane.add_updater(live_readout)
    axes = VGroup(pane, Line([x0, y0, 0], [x0 + width, y0, 0], color=GREY, stroke_width=3),
                  Line([x0, y0, 0], [x0, y0 + height, 0], color=GREY, stroke_width=3))
    xs = np.linspace(x0 + 0.8, x0 + width - 0.6, 5)
    labs = VGroup(*[label(f, x, y0 - 0.36, TEXT, 28) for x, f in zip(xs, FRACS)])
    return axes, labs, xs, y0, height


def profile_points(values, xs, y0, height, maxv=75):
    return [np.array([x, y0 + 0.28 + float(v) / maxv * (height - 0.62), 0])
            for x, v in zip(xs, values)]


def profile(values, xs, y0, height, color, dashed=False, width=5, opacity=1.0):
    pts = profile_points(values, xs, y0, height)
    segs = VGroup()
    for a, b in zip(pts, pts[1:]):
        line = DashedLine(a, b, dash_length=0.14, color=color, stroke_width=width) if dashed else Line(a, b, color=color, stroke_width=width)
        line.set_opacity(opacity)
        segs.add(line)
    dots = VGroup(*[Dot(p, radius=0.07, color=color).set_opacity(opacity) for p in pts])
    return VGroup(segs, dots)


def golgi_world(cell_x, color):
    outline = twin_cell(cell_x, color, 2.0)
    er = RoundedRectangle(width=0.72, height=1.42, corner_radius=0.12,
                          color=GREY, stroke_width=3, fill_opacity=0.12).move_to([cell_x - 1.05, 0.1, 0])
    er_lab = label("ER", cell_x - 1.05, 0.1, TEXT, 28)
    stack = VGroup(*[RoundedRectangle(width=0.88, height=0.28, corner_radius=0.12,
                                     color=TEAL if i == 0 else (GREY if i == 1 else ORANGE),
                                     stroke_width=3, fill_opacity=0.18).move_to([cell_x + 0.12, 0.58 - i * 0.48, 0])
                     for i in range(3)])
    gran = VGroup(*[Circle(0.16, color=GREY, fill_color=GREY, fill_opacity=0.22).move_to([cell_x + 1.18 + 0.24*(i%2), -0.22 + 0.38*(i//2), 0]) for i in range(4)])
    return VGroup(outline, er, er_lab, stack, gran), er, stack, gran


def dose_axes(cx, cy=-1.55, width=4.75, height=2.25):
    x0, y0 = cx - width/2, cy - height/2
    pane = Rectangle(width=width, height=height, stroke_width=0,
                     fill_color=GREY, fill_opacity=0.16).move_to([cx, cy, 0]).set_z_index(-2)
    pane._phase, pane._pulse = cx * .2, 1.0
    def live_readout(mob, dt):
        mob._phase += dt
        new = 1.0 + .03 * np.sin(mob._phase * 1.15)
        mob.scale([new / mob._pulse, 1, 1], about_point=mob.get_center())
        mob._pulse = new
    pane.add_updater(live_readout)
    ax = VGroup(pane, Line([x0, y0, 0], [x0+width, y0, 0], color=GREY, stroke_width=3),
                Line([x0, y0, 0], [x0, y0+height, 0], color=GREY, stroke_width=3),
                label("drug dose", cx, y0-0.42, TEXT, 28),
                T("growth", size=28, color=TEXT).rotate(PI/2).move_to([x0-0.42, cy, 0]))
    return ax, x0, y0, width, height


def dose_curve(x0, y0, width, height, shift=0.0, color=GREY, dashed=False, opacity=1.0):
    # Computed four-parameter logistic with top=1, bottom=0.08, Hill slope=1.35.
    u = np.linspace(0, 1, 60)
    logdose = -2.0 + 4.0*u
    response = 0.08 + 0.92/(1 + 10**(1.35*(logdose-shift)))
    pts = [np.array([x0 + q*width, y0 + 0.12 + r*(height-0.25), 0]) for q, r in zip(u, response)]
    vm = VMobject(color=color, stroke_width=5, fill_opacity=0).set_points_smoothly(pts).set_opacity(opacity)
    vm.set_fill(opacity=0)
    if not dashed:
        return vm
    return DashedVMobject(vm, num_dashes=24, dashed_ratio=0.55)


def strand(x, y, color=PURPLE, width=3.5):
    pts = [np.array([x-width/2 + width*i/36, y + 0.16*np.sin(i*0.75), 0]) for i in range(37)]
    return VMobject(color=color, stroke_width=6).set_points_smoothly(pts)


class ActiveScene(SpokenScene):
    """Use a slow, visible breath of the current readout while a cue is pending."""
    def wait(self, duration=1, stop_condition=None, frozen_frame=None):
        target = getattr(self, "active_readout", None)
        if duration >= .3 and target is not None and target in self.mobjects:
            self.play(target.animate.scale(1.035), rate_func=there_and_back, run_time=duration)
        else:
            super().wait(duration, stop_condition=stop_condition, frozen_frame=frozen_frame)


class S00Hook(TitleCard, SpokenScene):
    LESSON = "Experiments That Distinguish Mechanisms"
    TITLE = "Where the Twins Disagree"

    def construct(self):
        cells = twins(with_models=False, with_proteins=False)
        blobs = VGroup(protein_blob(-3.15), protein_blob(3.15))
        q = label("Does the right place tell you the job?", 0, 3.25, TEXT, 36, weight=BOLD)
        bar = bottom_bar()
        self.play(Create(cells), run_time=0.85)
        self.play(FadeIn(blobs), run_time=0.55)
        self.at("right place")
        self.play(blobs.animate.shift(UP*0.58), run_time=0.8)
        self.play(blobs.animate.shift(RIGHT*0.35), run_time=0.65)
        p = label("protein X", -3.15, 0.0, PURPLE, 28)
        p2 = p.copy().move_to([3.15, 0.0, 0])
        self.at("what it does")
        self.play(FadeIn(q), FadeIn(p), FadeIn(p2), run_time=0.7)
        self.at("two possible answers")
        models = VGroup(label("Model 1", -3.15, 2.75, TEAL, 32), label("Model 2", 3.15, 2.75, ORANGE, 32))
        self.play(FadeOut(p), FadeOut(p2), FadeIn(models), FadeIn(bar), blobs.animate.shift(DOWN*0.35), run_time=0.9)
        self.at("each true")
        self.play(blobs.animate.shift(LEFT*0.35), run_time=0.7)
        self.finish()


class S01Title(Scene):
    def construct(self):
        world = twins(with_models=True)
        title = T("Where the Twins Disagree", size=48, font=TITLE_FONT, color=TEXT, weight=BOLD).move_to([0, 3.15, 0])
        rule = Line([-2.0, 2.72, 0], [2.0, 2.72, 0], color=GOLD, stroke_width=4)
        self.add(world)
        self.play(FadeIn(title, shift=DOWN*0.12), GrowFromCenter(rule), world[2:].animate.shift(UP*0.22), run_time=0.7)
        self.play(world[2:].animate.shift(DOWN*0.44), run_time=0.65)
        self.play(world[2:].animate.shift(UP*0.22), run_time=0.55)
        self.wait(0.1)


class S02Rule(SpokenScene):
    def construct(self):
        world = twins()
        self.add(world)
        self.at("twins")
        bracket = BraceBetweenPoints([-5.2, 3.05, 0], [5.2, 3.05, 0], direction=UP, color=TEXT)
        twinlab = label("identical twins; different models", 0, 3.62, TEXT, 28)
        self.play(GrowFromCenter(bracket), FadeIn(twinlab), world[2:].animate.shift(UP*0.28), run_time=0.8)
        self.at("Every experiment")
        pip = VGroup(Line([0, 3.65, 0], [0, 2.45, 0], color=TEXT, stroke_width=7),
                     Line([0, 2.45, 0], [-3.15, 1.8, 0], color=TEXT, stroke_width=4),
                     Line([0, 2.45, 0], [3.15, 1.8, 0], color=TEXT, stroke_width=4))
        self.play(FadeOut(bracket), FadeOut(twinlab), Create(pip), run_time=0.8)
        self.at("both at once")
        flashes = VGroup(Circle(2.13, color=TEXT, stroke_width=9).move_to([-3.15,0.15,0]), Circle(2.13, color=TEXT, stroke_width=9).move_to([3.15,0.15,0]))
        self.play(FadeIn(flashes), world[2:].animate.shift(DOWN*0.38), run_time=0.35)
        self.play(FadeOut(flashes), FadeOut(pip), run_time=0.45)
        self.at("Here is the rule")
        bar = bottom_bar()
        same = label("SAME", -2.85, -3.18, GREY, 30, weight=BOLD)
        diff = label("DIFFERENT", 2.85, -3.18, GOLD, 30, weight=BOLD)
        divider = Line([0,-3.52,0],[0,-2.84,0],color=TEXT,stroke_width=2)
        pointer = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.12).rotate(PI).move_to([-2.85,-2.73,0])
        self.play(FadeIn(bar[0]), FadeIn(same), FadeIn(diff), Create(divider), FadeIn(pointer), run_time=0.65)
        self.at("only where")
        self.play(pointer.animate.move_to([2.85,-2.73,0]), run_time=1.0)
        self.at("twins disagree")
        self.play(pointer.animate.move_to([0,-2.73,0]), Indicate(diff, color=GOLD), run_time=0.8)
        self.finish()


class S03WhereSetup(SpokenScene):
    def construct(self):
        left, right = twin_cell(-3.15, TEAL), twin_cell(3.15, ORANGE)
        lyso = Circle(0.62, color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.13).move_to([-3.15,0.15,0])
        mito = RoundedRectangle(width=1.55,height=0.72,corner_radius=0.34,color=ORANGE,stroke_width=4,fill_opacity=0.13).move_to([3.15,0.15,0])
        blobs = VGroup(protein_blob(-3.15,0.15,.75), protein_blob(3.15,0.15,.75))
        self.play(Create(left), Create(right), run_time=0.7)
        self.at("where does")
        self.play(FadeIn(lyso), FadeIn(mito), run_time=0.7)
        self.play(FadeIn(blobs), run_time=0.45)
        self.at("in lysosomes")
        ll = label("lysosome", -3.15, -1.08, TEAL, 30)
        self.play(FadeIn(ll), lyso.animate.scale(1.08), run_time=0.65)
        self.at("in mitochondria")
        ml = label("mitochondrion", 3.15, -1.08, ORANGE, 30)
        self.play(FadeIn(ml), mito.animate.scale(1.08), run_time=0.65)
        self.at("Break both cells open")
        badges = VGroup(chip("Model 1", TEAL, 28).move_to([-3.15,3.15,0]), chip("Model 2", ORANGE, 28).move_to([3.15,3.15,0]))
        lrow,lxs = tube_row(-3.15,TEAL,-0.25,.72)
        rrow,rxs = tube_row(3.15,ORANGE,-0.25,.72)
        self.play(FadeOut(VGroup(left,right,ll,ml,lyso,mito,blobs)), FadeIn(badges), run_time=0.8)
        self.play(LaggedStart(*[Create(t) for t in list(lrow[0])+list(rrow[0])], lag_ratio=0.08), FadeIn(lrow[1]), FadeIn(rrow[1]), run_time=1.25)
        self.at("rising speeds")
        arrows = VGroup(Arrow([lxs[0],-2.18,0],[lxs[-1],-2.18,0],buff=0,color=TEAL,stroke_width=4), Arrow([rxs[0],-2.18,0],[rxs[-1],-2.18,0],buff=0,color=ORANGE,stroke_width=4))
        speed = label("rising spin speed",0,-2.65,TEXT,28)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(speed), run_time=0.8)
        self.finish()


class S04WhereSame(ActiveScene):
    def construct(self):
        lrow,lxs=tube_row(-3.15,TEAL,-0.25,.72); rrow,rxs=tube_row(3.15,ORANGE,-0.25,.72)
        badges=VGroup(chip("Model 1",TEAL,28).move_to([-3.15,3.15,0]),chip("Model 2",ORANGE,28).move_to([3.15,3.15,0]))
        self.add(lrow,rrow,badges)
        self.active_readout = VGroup(lrow, rrow)
        self.add(self.active_readout)
        # The aligner joins the spoken "tube L" as "tubel" in this scene.
        self.at("protein enriched")
        rings=VGroup(SurroundingRectangle(lrow[0][2],color=TEXT,buff=.08),SurroundingRectangle(rrow[0][2],color=TEXT,buff=.08))
        self.play(Create(rings),run_time=.7)
        base=-.88
        starts=VGroup(DashedLine([-3.75,base,0],[-2.55,base,0],color=TEXT),DashedLine([2.55,base,0],[3.75,base,0],color=TEXT))
        startlab=label("starting mix = 1",0,-2.18,TEXT,28)
        self.at("starting mix")
        self.play(Create(starts),FadeIn(startlab),run_time=.65)
        teal_fill=Rectangle(width=.46,height=1.35,stroke_width=0,fill_color=PURPLE,fill_opacity=.85).move_to([lxs[2],-.25,0])
        orange_fill=Rectangle(width=.46,height=.78,stroke_width=0,fill_color=PURPLE,fill_opacity=.85).move_to([rxs[2],-.54,0])
        self.at("teal twin")
        self.play(GrowFromEdge(teal_fill,DOWN),FadeIn(label("9-fold",lxs[2],1.38,PURPLE,28)),run_time=.9)
        self.at("also yes")
        enrichment=label("enrichment",0,1.38,PURPLE,28)
        self.play(GrowFromEdge(orange_fill,DOWN),FadeIn(label("3-fold",rxs[2],1.38,PURPLE,28)),FadeIn(enrichment),run_time=.9)
        self.at("plenty of mitochondria")
        minis=VGroup(*[RoundedRectangle(width=.34,height=.15,corner_radius=.07,color=ORANGE,fill_opacity=.5).move_to([rxs[2]+dx,-.35+dy,0]) for dx,dy in [(-.15,.2),(.15,0),(-.1,-.22)]])
        self.play(FadeIn(minis),run_time=.65)
        self.at("cannot choose")
        bar=bottom_bar("SAME: both yes",GREY)
        self.play(FadeIn(bar),run_time=.7)
        self.finish()


def predict_chart():
    axes,labs,xs,y0,h=chart_axes(center=(0,-.22),width=9.7,height=4.6)
    ly=profile(LYSO,xs,y0,h,TEAL,True,4,.62)
    mi=profile(MITO,xs,y0,h,ORANGE,True,4,.62)
    bars=VGroup(*[Rectangle(width=.62,height=.75,stroke_width=0,fill_color=GREY,fill_opacity=.72).move_to([x,y0+.375,0]) for x in xs])
    for i, b in enumerate(bars):
        b._phase, b._pulse, b._base = i * .55, 1.0, np.array([b.get_x(), y0, 0])
        def pulse(mob, dt):
            mob._phase += dt
            new = 1.0 + .22 * np.sin(mob._phase * 1.35)
            mob.scale([1, new / mob._pulse, 1], about_point=mob._base)
            mob._pulse = new
        b.add_updater(pulse)
    return axes,labs,xs,y0,h,ly,mi,bars


class S05WherePredict(ActiveScene):
    def construct(self):
        axes,labs,xs,y0,h,ly,mi,bars=predict_chart()
        self.at("all five tubes")
        self.play(Create(axes),FadeIn(labs),LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.1),run_time=1.0)
        self.active_readout = bars
        self.at("Each bar")
        self.play(bars.animate.set_fill(opacity=.7).scale(1.0),run_time=.7)
        self.at("Two faint tracks")
        scan_y=y0+h/2
        teal_scan=RoundedRectangle(width=.78,height=h-.16,corner_radius=.12,stroke_width=0,
                                   fill_color=TEAL,fill_opacity=.18).move_to([xs[0],scan_y,0])
        orange_scan=teal_scan.copy().set_fill(ORANGE,opacity=.18)
        self.add(teal_scan)
        self.play(Create(ly),teal_scan.animate.move_to([xs[-1],scan_y,0]),run_time=.95)
        orange_scan.move_to([xs[0],scan_y,0])
        self.remove(teal_scan)
        self.add(orange_scan)
        self.play(Create(mi),orange_scan.animate.move_to([xs[-1],scan_y,0]),run_time=.95)
        self.play(FadeOut(orange_scan),run_time=.25)
        tags=VGroup(chip("lysosome marker",TEAL,28).move_to([-3.8,2.58,0]),chip("mitochondrial marker",ORANGE,28).move_to([3.75,2.58,0]))
        note=label("computed from lesson table",4.15,-3.30,GREY,28)
        self.play(FadeIn(tags),FadeIn(note),run_time=.55)
        self.at("If the protein")
        q=label("Which track should it trace?",0,3.35,TEXT,36,weight=BOLD)
        self.play(FadeIn(q),bars.animate.set_fill(opacity=.45),run_time=.7)
        self.at("which track")
        self.play(bars.animate.scale(1.06),run_time=.45)
        self.play(bars.animate.scale(1/1.06),run_time=.45)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        axes,labs,xs,y0,h,ly,mi,bars=predict_chart()
        tags=VGroup(chip("lysosome marker",TEAL,28).move_to([-3.8,2.58,0]),chip("mitochondrial marker",ORANGE,28).move_to([3.75,2.58,0]))
        q=label("Which track should it trace?",0,3.35,TEXT,36,weight=BOLD)
        note=label("computed from lesson table",4.15,-3.30,GREY,28)
        self.add(axes,labs,ly,mi,bars,tags,q,note)
        self.play(bars.animate.scale(1.06),ly.animate.set_opacity(.85),run_time=1.0)
        self.play(bars.animate.scale(1/1.06),ly.animate.set_opacity(.62),mi.animate.set_opacity(.85),run_time=1.0)
        self.play(bars.animate.scale(1.06),mi.animate.set_opacity(.62),run_time=1.0)
        self.play(bars.animate.scale(1/1.06),ly.animate.set_opacity(.85),run_time=1.0)
        self.play(ly.animate.set_opacity(.62),run_time=.5)


class S07WhereDifferent(ActiveScene):
    def construct(self):
        axes,labs,xs,y0,h,ly,mi,bars=predict_chart()
        self.add(axes,labs,ly,mi,bars)
        self.active_readout = bars
        self.at("twins disagree")
        tealbars=VGroup(*[Rectangle(width=.32,height=max(.08,p[1]-y0),stroke_width=0,fill_color=TEAL,fill_opacity=.66).move_to([x-.2,(p[1]+y0)/2,0]) for x,p in zip(xs,profile_points(LYSO,xs,y0,h))])
        orangebars=VGroup(*[Rectangle(width=.32,height=max(.08,p[1]-y0),stroke_width=0,fill_color=ORANGE,fill_opacity=.66).move_to([x+.2,(p[1]+y0)/2,0]) for x,p in zip(xs,profile_points(MITO,xs,y0,h))])
        self.play(ReplacementTransform(bars.copy(),tealbars),ReplacementTransform(bars,orangebars),run_time=1.0)
        self.active_readout = VGroup(tealbars, orangebars)
        self.add(self.active_readout)
        bar=bottom_bar("DIFFERENT",GOLD)
        self.play(FadeIn(bar),run_time=.5)
        self.at("lesson's made")
        tag=chip("made-up teaching data",GREY,28).move_to([3.85,3.15,0])
        pts=profile_points(UNKNOWN,xs,y0,h)
        dots=VGroup(*[Dot(p,radius=.1,color=PURPLE) for p in pts])
        self.play(FadeIn(tag),LaggedStart(*[FadeIn(d,shift=DOWN*.2) for d in dots],lag_ratio=.16),run_time=1.2)
        line=profile(UNKNOWN,xs,y0,h,PURPLE,False,6,1)
        self.play(Create(line[0]),run_time=.75)
        self.at("whole profile")
        self.play(ShowPassingFlash(line[0].copy().set_stroke(width=12,color=TEXT),time_width=.5),run_time=1.1)
        self.at("still not proof")
        qm=label("?",5.15,1.7,TEXT,48,weight=BOLD)
        self.play(FadeIn(qm),run_time=.6)
        self.finish()


class S08Purity(SpokenScene):
    def construct(self):
        big=tube(0,-.15,TEXT,3.5,5.45)
        self.play(Create(big),run_time=.6)
        lys=VGroup(*[Circle(.27,color=TEAL,fill_color=TEAL,fill_opacity=.35).move_to([x,y,0]) for x,y in [(-.85,1.1),(.55,.8),(-.45,-.2),(.8,-1.2)]])
        mits=VGroup(*[RoundedRectangle(width=.72,height=.3,corner_radius=.14,color=ORANGE,fill_opacity=.35).move_to([x,y,0]) for x,y in [(.75,1.55),(-.75,.45),(.55,-.35),(-.55,-1.35)]])
        debris=VGroup(*[Triangle(color=GREY,fill_color=GREY,fill_opacity=.3).scale(.18).move_to([x,y,0]) for x,y in [(0,1.2),(-1.0,-.65),(1.05,.2)]])
        self.play(LaggedStart(*[FadeIn(m) for m in list(lys)+list(mits)+list(debris)],lag_ratio=.08),run_time=1.0)
        self.at("leans toward lysosomes")
        contents=VGroup(lys,mits,debris)
        self.play(contents.animate.shift(LEFT*.22),Rotate(big,angle=.07),run_time=.65)
        self.at("not purity")
        lab=chip("enriched, not pure",PURPLE,30).move_to([4.35,1.15,0])
        schematic=label("schematic",5.05,-3.25,GREY,28)
        self.play(contents.animate.shift(RIGHT*.22),Rotate(big,angle=-.07),FadeIn(lab),FadeIn(schematic),run_time=.75)
        self.at("mostly made of")
        qm=label("?",0,.05,TEXT,72,weight=BOLD)
        self.play(FadeIn(qm),lys.animate.shift(UP*.1),mits.animate.shift(DOWN*.1),run_time=.7)
        self.at("Hold that question")
        self.play(Indicate(qm,scale_factor=1.08),run_time=.7)
        self.finish()


class S09When(SpokenScene):
    def construct(self):
        lw,ler,lg,lgran=golgi_world(-3.15,TEAL); rw,rer,rg,rgran=golgi_world(3.15,ORANGE)
        self.play(FadeIn(lw),FadeIn(rw),run_time=.75)
        heading=label("In what order does it travel?",0,3.25,TEXT,34,weight=BOLD)
        self.at("in what order")
        self.play(FadeIn(heading),run_time=.55)
        self.at("Tag one batch")
        golds=VGroup(*[Dot([-4.2+dx,.1+dy,0],radius=.07,color=GOLD) for dx,dy in [(0,.3),(.1,0),(-.08,-.3)]],*[Dot([2.1+dx,.1+dy,0],radius=.07,color=GOLD) for dx,dy in [(0,.3),(.1,0),(-.08,-.3)]])
        self.play(FadeIn(golds),Flash([-4.2,.1,0],color=GOLD),Flash([2.1,.1,0],color=GOLD),run_time=.65)
        self.at("carriers ferry")
        lc=Circle(.22,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([-3.75,.1,0])
        self.play(FadeIn(lc),golds[:3].animate.move_to([-3.55,.45,0]),lc.animate.move_to([-3.05,.45,0]),run_time=.9)
        self.play(lc.animate.move_to([-2.6,0,0]),golds[:3].animate.move_to([-2.6,0,0]),run_time=.8)
        self.at("fixed Golgi compartments")
        self.play(Indicate(lg,scale_factor=1.03),run_time=.65)
        self.at("compartment itself matures")
        moving=rg[0].copy().set_color(GOLD)
        self.add(moving)
        self.play(golds[3:].animate.move_to([3.27,.58,0]),moving.animate.move_to([3.27,.1,0]).set_color(ORANGE),run_time=.85)
        back=Arrow([3.45,-.5,0],[3.05,.6,0],color=GREY,stroke_width=3,buff=.05)
        self.play(moving.animate.move_to([3.27,-.38,0]),GrowArrow(back),run_time=.75)
        buds=VGroup(Circle(.24,color=GOLD,fill_opacity=.25).move_to([-1.85,-.35,0]),Circle(.24,color=GOLD,fill_opacity=.25).move_to([4.45,-.35,0]))
        self.play(FadeIn(buds),run_time=.65)
        self.finish()


class S10WhenSame(SpokenScene):
    def construct(self):
        lw,ler,lg,lgran=golgi_world(-3.15,TEAL); rw,rer,rg,rgran=golgi_world(3.15,ORANGE)
        self.add(lw,rw)
        regions=[VGroup(ler,rer),VGroup(lg,rg),VGroup(lgran,rgran)]
        self.at("gold label")
        for reg in regions:
            self.play(reg.animate.set_color(GOLD),run_time=.65)
        ticks=VGroup()
        for cx in (-3.15,3.15):
            for i in range(3):
                ticks.add(Line([cx-.7+i*.7,-2.35,0],[cx-.25+i*.7,-2.35,0],color=GOLD,stroke_width=8))
        self.at("then the granules")
        self.play(LaggedStart(*[Create(t) for t in ticks],lag_ratio=.1),run_time=.85)
        note=label("order only; kinetics not specified",0,2.9,GREY,28)
        self.play(FadeIn(note),run_time=.5)
        self.at("cannot choose")
        bar=bottom_bar("SAME",GREY)
        self.play(FadeIn(bar),run_time=.7)
        self.at("Other tests can")
        arr=Arrow([4.9,2.6,0],[6.3,2.6,0],color=GOLD,stroke_width=6)
        self.play(GrowArrow(arr),run_time=.7)
        self.finish()


class S11CauseSetup(SpokenScene):
    def construct(self):
        cells=VGroup(twin_cell(-3.15,TEAL,1.25),twin_cell(3.15,ORANGE,1.25))
        self.play(FadeIn(cells),run_time=.6)
        self.at("cancer cells growing")
        daughters=VGroup(Circle(.34,color=TEAL).move_to([-4.55,1.25,0]),Circle(.34,color=ORANGE).move_to([4.55,1.25,0]))
        self.play(FadeIn(daughters,shift=OUT),cells.animate.scale(1.04),run_time=.7)
        self.at("block one kinase")
        kin=VGroup(chip("the kinase",PURPLE,28).move_to([-3.15,.25,0]),chip("the kinase",PURPLE,28).move_to([3.15,.25,0]))
        self.play(FadeIn(kin),run_time=.6)
        self.at("adds phosphate")
        phosph=VGroup(chip("phosphate",GOLD,28).move_to([-3.15,2.0,0]),chip("phosphate",GOLD,28).move_to([3.15,2.0,0]))
        self.play(FadeIn(phosph),run_time=.55)
        drug1=Dot([-4.5,.45,0],radius=.15,color=GOLD); drug2=drug1.copy().move_to([1.8,.45,0])
        alt=RoundedRectangle(width=.7,height=.45,corner_radius=.1,color=GREY,fill_opacity=.25).move_to([4.05,-.2,0])
        self.play(FadeOut(phosph),FadeIn(drug1),FadeIn(drug2),FadeIn(alt),drug1.animate.move_to([-3.75,.45,0]),drug2.animate.move_to([4.05,-.2,0]),run_time=.9)
        self.at("curve shows")
        left=dose_axes(-3.15,-1.65,4.7,2.0); right=dose_axes(3.15,-1.65,4.7,2.0)
        self.play(Create(left[0]),Create(right[0]),run_time=.75)
        curves=VGroup(dose_curve(*left[1:],color=TEAL),dose_curve(*right[1:],color=ORANGE))
        self.play(Create(curves),run_time=1.0)
        self.finish()


class S12CausePredict(SpokenScene):
    def construct(self):
        cells=VGroup(twin_cell(-3.15,TEAL,1.25),twin_cell(3.15,ORANGE,1.25))
        kin=VGroup(chip("the kinase",PURPLE,28).move_to([-3.15,.25,0]),chip("the kinase",PURPLE,28).move_to([3.15,.25,0]))
        left=dose_axes(-3.15,-1.65,4.7,2.0); right=dose_axes(3.15,-1.65,4.7,2.0)
        orig=VGroup(dose_curve(*left[1:],color=GREY,dashed=True,opacity=.6),dose_curve(*right[1:],color=GREY,dashed=True,opacity=.6))
        self.add(cells,kin,left[0],right[0],orig)
        self.at("kinase out")
        flashes=VGroup(Circle(.7,color=TEXT).move_to(kin[0]),Circle(.7,color=TEXT).move_to(kin[1]))
        labs=VGroup(label("kinase removed",-3.15,2.0,PURPLE,28),label("kinase removed",3.15,2.0,PURPLE,28))
        self.play(FadeIn(flashes),FadeOut(kin),run_time=.35); self.play(FadeOut(flashes),FadeIn(labs),run_time=.45)
        self.at("still grow")
        daughters=VGroup(Circle(.32,color=TEAL).move_to([-4.55,1.2,0]),Circle(.32,color=ORANGE).move_to([4.55,1.2,0]))
        self.play(FadeIn(daughters),cells.animate.scale(1.035),run_time=.7)
        self.at("Give the drug again")
        drug=VGroup(Dot([-4.55,.8,0],radius=.14,color=GOLD),Dot([1.75,.8,0],radius=.14,color=GOLD))
        self.play(FadeIn(drug),drug.animate.shift(RIGHT*.6),run_time=.7)
        self.at("shifts the curve right")
        teal=dose_curve(*left[1:],shift=.65,color=TEAL)
        self.play(Create(teal),daughters[0].animate.shift(LEFT*.18),run_time=1.0)
        self.at("leaves it put")
        orange=dose_curve(*right[1:],shift=0,color=ORANGE)
        self.play(Create(orange),daughters[1].animate.shift(RIGHT*.18),run_time=1.0)
        self.at("Mixed effects")
        mid=dose_curve(*left[1:],shift=.32,color=GOLD).set_opacity(.45)
        self.play(Create(mid),run_time=.75)
        self.finish()


class S13CauseReveal(ActiveScene):
    def construct(self):
        left=dose_axes(-3.15,-.3,5.2,4.55); right=dose_axes(3.15,-.3,5.2,4.55)
        orig=VGroup(dose_curve(*left[1:],color=GREY,dashed=True,opacity=.55),dose_curve(*right[1:],color=GREY,dashed=True,opacity=.55))
        teal=dose_curve(*left[1:],shift=.65,color=TEAL)
        orange=dose_curve(*right[1:],shift=0,color=ORANGE)
        self.add(left[0],right[0],orig,teal,orange)
        self.at("measured curve")
        measured=VGroup(dose_curve(*left[1:],shift=.04,color=GOLD),dose_curve(*right[1:],shift=.04,color=GOLD))
        self.play(Create(measured),run_time=1.1)
        self.active_readout = measured
        self.at("barely moves")
        gap=Polygon(*[np.array([-2.4,-1.7,0]),np.array([-1.25,-1.1,0]),np.array([-1.25,1.0,0]),np.array([-2.4,.25,0])],stroke_width=0,fill_color=TEAL,fill_opacity=.16)
        self.play(FadeIn(gap),Indicate(measured[0],scale_factor=1.02),run_time=.8)
        self.at("about the same dose")
        tick=label("✓",3.15,2.55,GOLD,44,weight=BOLD)
        self.play(FadeIn(tick),Indicate(orange,color=GOLD),run_time=.8)
        self.at("other targets")
        bar=bottom_bar("DIFFERENT",GOLD); cite=label("Lin and colleagues, 2017",4.3,3.25,GREY,28)
        self.play(FadeIn(bar),FadeIn(cite),run_time=.7)
        self.finish()


class S14Rescue(SpokenScene):
    def construct(self):
        cell=twin_cell(0,TEAL,2.85)
        msg=strand(-.55,.75,PURPLE,3.7); mlab=label("m R N A",-.55,1.42,PURPLE,28)
        blobs=VGroup(*[protein_blob(-1.2+i*.8,-.55,.55) for i in range(4)])
        count=VGroup(*[Circle(.2,color=TEAL).move_to([-1.05+i*.7,-1.75,0]) for i in range(4)])
        self.play(Create(cell),Create(msg),FadeIn(mlab),LaggedStart(*[FadeIn(b) for b in blobs],lag_ratio=.1),FadeIn(count),run_time=1.0)
        self.at("RNA interference")
        hair=VGroup(Arc(radius=.45,start_angle=-PI/2,angle=PI,color=TEXT,stroke_width=5),Arc(radius=.45,start_angle=PI/2,angle=PI,color=TEXT,stroke_width=5)).scale(.65).move_to([2.1,.75,0])
        self.play(FadeIn(hair),hair.animate.move_to([.45,.75,0]),run_time=.8)
        self.at("job fails")
        fragments=VGroup(*[Line([-.9+i*.45,.7,0],[-.65+i*.45,.85,0],color=PURPLE,stroke_width=5) for i in range(4)])
        self.play(ReplacementTransform(msg,fragments),FadeOut(blobs),count.animate.set_color(RED),run_time=.75)
        self.at("other messages")
        grey=strand(0,0,GREY,2.8); q=label("?",1.8,.05,TEXT,42)
        self.play(Create(grey),run_time=.5); self.play(grey.animate.set_opacity(.2),FadeIn(q),run_time=.55)
        self.at("put the protein back")
        resistant=strand(0,.9,PURPLE,3.8); rlab=label("resistant copy",0,1.58,PURPLE,28)
        self.play(FadeOut(fragments),FadeOut(mlab),Create(resistant),FadeIn(rlab),hair.animate.move_to([-.35,.9,0]),run_time=.8)
        self.play(hair.animate.move_to([2.0,.25,0]),run_time=.55)
        self.at("cannot touch")
        newblobs=VGroup(*[protein_blob(-1.2+i*.8,-.45,.55) for i in range(4)])
        newcount=VGroup(*[Circle(.2,color=TEAL).move_to([-1.4+i*.7,-1.75,0]) for i in range(5)])
        self.play(FadeIn(newblobs),Transform(count,newcount),run_time=.7)
        self.at("same protein")
        self.play(Indicate(newblobs,scale_factor=1.08),run_time=.65)
        self.at("yet escape")
        self.play(FadeOut(q),FadeIn(label("?",2.35,1.0,TEXT,48)),run_time=.6)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        world=twins(with_proteins=False)
        self.play(FadeIn(world),run_time=.6)
        # Three compact, faithful reminders; their positions do not move after landing.
        p1=RoundedRectangle(width=3.55,height=2.5,corner_radius=.15,color=GOLD,fill_opacity=.06).move_to([-4.05,-.25,0])
        p2=p1.copy().set_color(GREY).move_to([0,-.25,0]); p3=p1.copy().move_to([4.05,-.25,0])
        self.at("where does it live")
        bars=VGroup(*[Rectangle(width=.28,height=h,stroke_width=0,fill_color=PURPLE,fill_opacity=.75).move_to([-5.05+i*.5,-.55+h/2,0]) for i,h in enumerate([.3,.7,1.35,.45,.35])])
        self.play(FadeIn(p1),LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.1),run_time=.75)
        self.at("what order")
        steps=VGroup(*[RoundedRectangle(width=.58,height=.34,corner_radius=.1,color=GOLD,fill_opacity=.25).move_to([-0.85+i*.85,-.25,0]) for i in range(3)])
        self.play(FadeIn(p2),LaggedStart(*[FadeIn(s) for s in steps],lag_ratio=.2),run_time=.75)
        self.at("cause the defect")
        miniL=dose_axes(4.05,-.25,2.7,1.45); c1=dose_curve(*miniL[1:],color=GREY,dashed=True); c2=dose_curve(*miniL[1:],shift=.55,color=TEAL)
        self.play(FadeIn(p3),Create(miniL[0][:2]),Create(c1),Create(c2),run_time=.85)
        status=VGroup(label("DIFFERENT",-4.05,-1.88,GOLD,28,weight=BOLD),label("SAME",0,-1.88,GREY,28,weight=BOLD),label("DIFFERENT",4.05,-1.88,GOLD,28,weight=BOLD))
        self.play(FadeIn(status),run_time=.55)
        self.at("what each model predicts")
        heading=label("Predict both models first",0,3.28,TEXT,36,weight=BOLD)
        self.play(FadeIn(heading),run_time=.7)
        self.at("Agreeing twins")
        self.play(VGroup(p2,steps,status[1]).animate.set_opacity(.25),Indicate(VGroup(status[0],status[2]),color=GOLD),run_time=.8)
        self.finish()


class S16End(EndCard):
    LINE = "A result can choose only where the two models disagree."
