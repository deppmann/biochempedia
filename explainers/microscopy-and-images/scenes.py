"""What Zoom Cannot Recover — microscopy-and-images teaching film.

COLOR MAP
  GREEN  fluorescent sources, emitted light, and individual Airy intensities
  BLUE   objective, collection cone, and optical measurement elements
  YELLOW distances, controls, questions, and illumination
  RED    lost/unrecoverable detail and the single recorded spot
  TEXT   detector sum and conclusions
  GREY   cell, detector, axes, and de-emphasised structure

Every intensity profile is sampled from the ideal Airy/Bessel expression used by
the lesson.  The bench is schematic; its geometry is deliberately not to scale.
"""
import numpy as np
from scipy.special import j1
from bp_style import *  # noqa: F401,F403


D_RAYLEIGH = 227.0
SOURCE_SEP = 150.0
LENS_X = -0.8
PLOT_LEFT, PLOT_RIGHT = 1.35, 6.25
PLOT_BASE, PLOT_TOP = -2.35, 1.05


def airy(x, d=D_RAYLEIGH):
    """Ideal lateral Airy cross-section; first zero is at |x| = d."""
    z = 3.83170597 * np.abs(np.asarray(x, dtype=float)) / d
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (2 * j1(z) / z) ** 2
    return np.where(z < 1e-7, 1.0, out)


def profile(fn, color=GREEN, width=4, opacity=1.0, y_scale=2.25):
    xs = np.linspace(-360, 360, 420)
    px = np.interp(xs, [-360, 360], [PLOT_LEFT + 0.18, PLOT_RIGHT - 0.18])
    pts = [[x, PLOT_BASE + y_scale * float(fn(nm)), 0] for x, nm in zip(px, xs)]
    mob = VMobject(fill_opacity=0).set_points_as_corners(pts)
    return mob.set_stroke(color, width=width, opacity=opacity)


def sum_profile(separation=SOURCE_SEP, color=TEXT, width=7, y_scale=1.55):
    h = separation / 2
    return profile(lambda x: airy(x - h) + airy(x + h), color, width, y_scale=y_scale)


def bracket(a, b, label, color=YELLOW, vertical=False, size=28):
    if vertical:
        line = Line(a, b, color=color, stroke_width=4)
        ticks = VGroup(Line(a + LEFT * .13, a + RIGHT * .13, color=color, stroke_width=4),
                       Line(b + LEFT * .13, b + RIGHT * .13, color=color, stroke_width=4))
        text = M(label, size, color).next_to(line, LEFT, buff=.18)
    else:
        line = Line(a, b, color=color, stroke_width=4)
        ticks = VGroup(Line(a + DOWN * .13, a + UP * .13, color=color, stroke_width=4),
                       Line(b + DOWN * .13, b + UP * .13, color=color, stroke_width=4))
        text = M(label, size, color).next_to(line, UP, buff=.16)
    return VGroup(line, ticks, text)


def vesicle(y, opacity=1.0):
    ring = Circle(.34, color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=.12)
    core = VGroup(*[Dot([.13*np.cos(a), .13*np.sin(a), 0], radius=.035, color=GREEN)
                    for a in np.linspace(0, 2*np.pi, 6, endpoint=False)])
    return VGroup(ring, core).move_to([-5.15, y, 0]).set_opacity(opacity)


def bench(two=True, dim_top=False, plot=True):
    cell = Ellipse(width=2.35, height=5.45, color=GREY, stroke_width=3,
                   fill_color=GREY, fill_opacity=.16).move_to([-5.15, -.25, 0])
    vtop = vesicle(.45, .22 if dim_top else 1)
    vbot = vesicle(-.75)
    lens = Ellipse(width=.78, height=4.65, color=BLUE, stroke_width=5,
                   fill_color=BLUE, fill_opacity=.16).move_to([LENS_X, -.15, 0])
    lens_label = T("objective", 28, BLUE).next_to(lens, DOWN, buff=.18)
    detector = RoundedRectangle(corner_radius=.16, width=5.15, height=4.35,
                                color=GREY, stroke_width=3, fill_color=GREY,
                                fill_opacity=.17).move_to([3.8, -.55, 0])
    screen_label = T("detector", 28, GREY).move_to([3.8, 1.9, 0])
    schematic = T("SCHEMATIC", 22, GREY).move_to([-5.15, 3.42, 0])
    sources = VGroup(vtop, vbot) if two else VGroup(vbot)
    out = VGroup(cell, sources, lens, lens_label, schematic)
    if plot:
        out.add(detector, screen_label)
    out.cell, out.sources, out.lens = cell, sources, lens
    return out


def packets(ys=(.45, -.75), start=-4.72, end=-1.35):
    """Continuously moving fluorescent packets for the carried optical bench."""
    group = VGroup()
    for row, y in enumerate(ys):
        for i in range(4):
            d = Dot([start + i*(end-start)/4, y + .07*np.sin(i), 0], radius=.055,
                    color=GREEN).set_opacity(.7)
            speed = .38 + .035*row
            def drift(m, dt, lo=start, hi=end, v=speed):
                m.shift(RIGHT*v*dt)
                if m.get_x() > hi:
                    m.set_x(lo)
            d.add_updater(drift)
            group.add(d)
        # A continuously travelling emission ripple is large enough to read as
        # motion at draft resolution, unlike isolated sub-pixel motes.
        xs = np.linspace(start, end, 90)
        ripple = VMobject(stroke_color=GREEN, stroke_width=10, stroke_opacity=.78)
        ripple.phase = row * np.pi / 2
        def ripple_motion(m, dt, xs=xs, y=y):
            m.phase += 14.0 * dt
            m.set_points_as_corners([[x, y + .24*np.sin(7.2*x - m.phase), 0] for x in xs])
        ripple.add_updater(ripple_motion)
        ripple_motion(ripple, 0)
        group.add(ripple)
    return group


def plot_axes():
    return VGroup(
        Line([PLOT_LEFT, PLOT_BASE, 0], [PLOT_RIGHT, PLOT_BASE, 0], color=GREY, stroke_width=2),
        Line([PLOT_LEFT, PLOT_BASE, 0], [PLOT_LEFT, PLOT_TOP, 0], color=GREY, stroke_width=2),
        T("position", 28, GREY).move_to([3.8, -2.78, 0]),
    )


def prediction_frame():
    b = bench(two=True)
    light = packets()
    sep = bracket(np.array([-5.68, -.75, 0]), np.array([-5.68, .45, 0]), "150 nm", vertical=True)
    # Stack the two measurements on one clear rail: the former side-by-side
    # layout made their labels collide at draft resolution.
    ray = bracket(np.array([-5.68, -2.88, 0]), np.array([-5.68, -1.06, 0]), "d ≈ 227 nm", vertical=True)
    ray[2].next_to(ray[0], RIGHT, buff=.18)
    question = T("TWO PEAKS OR ONE?", 38, YELLOW, weight=BOLD).move_to([3.8, 2.72, 0])
    placeholders = VGroup(*[
        DashedVMobject(Line([x, -2.2, 0], [x, .55, 0], color=GREY, stroke_width=3), 18)
        for x in (3.3, 4.3)
    ]).set_opacity(.38)
    return b, light, sep, ray, question, placeholders


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Microscopy and Images"
    TITLE = "What Zoom Cannot Recover"

    def construct(self):
        b = bench(two=True)
        light = packets()
        self.add(light)
        self.play(FadeIn(b.cell), FadeIn(b.sources, scale=.7), run_time=.8)
        self.at("150 nanometers apart")
        sep = bracket(np.array([-5.68, -.75, 0]), np.array([-5.68, .45, 0]), "150 nm", vertical=True)
        self.play(Create(sep), FadeIn(b[4]), run_time=.7)
        self.at("ordinary light microscope")
        self.play(FadeIn(VGroup(b.lens, b[3])), run_time=.7)
        detector_bits = VGroup(b[-2], b[-1])
        self.play(FadeIn(detector_bits), run_time=.6)
        markers = VGroup(Dot([3.45, -.3, 0], radius=.11, color=GREEN),
                         Dot([4.15, -.3, 0], radius=.11, color=GREEN))
        self.play(FadeIn(markers), run_time=.5)
        self.at("records one spot")
        spot = VGroup(*[Circle(r, stroke_width=0, fill_color=RED, fill_opacity=o)
                        for r, o in ((.9,.12),(.63,.25),(.36,.65))]).move_to([3.8,-.3,0])
        one = T("one recorded spot", 30, RED, weight=BOLD).move_to([3.8,-1.65,0])
        self.play(ReplacementTransform(markers, spot), FadeIn(one), run_time=1.0)
        self.at("Why can software zoom")
        q = T("WHY CAN'T ZOOM FIND TWO?", 34, YELLOW, weight=BOLD).move_to([.3, 3.18, 0])
        self.play(Write(q), spot.animate.scale(1.18), run_time=1.0)
        self.at("Follow the light")
        path = Arrow([-4.45, 2.55, 0], [5.65, 2.55, 0], buff=0, color=GREEN,
                     stroke_width=5, tip_length=.24)
        self.play(GrowArrow(path), run_time=1.1)
        self.at("missing detail is lost")
        self.play(Indicate(spot, color=RED, scale_factor=1.08), run_time=.8)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        b = bench(two=True).set_opacity(.34)
        light = packets()
        light.set_opacity(.35)
        title = T("What Zoom Cannot Recover", 52, TEXT, font=TITLE_FONT).move_to([0, 2.82, 0])
        rule = Line([-2.0, 2.36, 0], [2.0, 2.36, 0], color=GOLD, stroke_width=4)
        self.add(b, light)
        self.play(FadeIn(title, shift=UP*.15), GrowFromCenter(rule), run_time=.45)
        self.wait(.95)
        self.play(FadeOut(VGroup(title, rule)), run_time=.45)
        self.finish()


class S03OnePoint(SpokenScene):
    def construct(self):
        b = bench(two=True, dim_top=True)
        light = packets(ys=(-.62, -.88))
        self.add(b, light)
        self.at("Start with one point")
        self.play(Indicate(b.sources[1], color=GREEN, scale_factor=1.25), run_time=.7)
        self.at("every point becomes a blur")
        disc = VGroup(Circle(.95, color=GREEN, stroke_opacity=.22),
                      Circle(.66, color=GREEN, stroke_opacity=.35),
                      Circle(.34, stroke_width=0, fill_color=GREEN, fill_opacity=.8)).move_to([3.8,.15,0])
        self.play(LaggedStart(*[FadeIn(x, scale=.4) for x in reversed(disc)], lag_ratio=.2), run_time=1.2)
        self.at("bright center with faint rings")
        airy_label = T("Airy pattern", 30, GREEN).move_to([3.8,1.25,0])
        self.play(FadeIn(airy_label), disc.animate.scale(1.08), run_time=.9)
        self.at("This computed green curve")
        self.play(FadeOut(disc), FadeOut(airy_label), run_time=.6)
        ax = plot_axes()
        c = profile(lambda x: airy(x), GREEN, 6)
        lab = T("computed intensity", 28, GREEN).move_to([5.05,.92,0])
        self.play(Create(ax), Create(c), FadeIn(lab), run_time=1.4)
        pulse = c.copy().set_stroke(GREEN, width=10, opacity=.16)
        pulse.add_updater(lambda m, dt: m.set_opacity(.10 + .10 * (1 + np.sin(2.2 * self.renderer.time)) / 2))
        self.add(pulse)
        self.at("across the screen")
        self.play(ShowPassingFlash(c.copy().set_stroke(YELLOW, width=8), time_width=.35), run_time=1.0)
        self.finish()


class S04Aperture(SpokenScene):
    def construct(self):
        b = bench(two=True, dim_top=True)
        ax, c = plot_axes(), profile(lambda x: airy(x), GREEN, 5)
        self.add(b, ax, c, packets(ys=(-.75,)))
        self.at("Why does the point spread")
        q = T("WHY DOES A POINT SPREAD?", 34, YELLOW, weight=BOLD).move_to([3.8,1.12,0])
        self.play(FadeIn(q), c.animate.set_stroke(width=7), run_time=.8)
        self.at("Light diffracts")
        origin = np.array([-4.75,-.75,0])
        rays = VGroup(*[Line(origin, [LENS_X, y, 0], color=GREEN, stroke_width=3) for y in (-2.15,-1.35,-.75,-.15,.65)])
        self.play(FadeOut(q), LaggedStart(*[Create(r) for r in rays], lag_ratio=.12), run_time=1.2)
        self.at("finer pattern bends light")
        outer = VGroup(Line(origin,[LENS_X,2.0,0],color=GREEN,stroke_width=3),
                       Line(origin,[LENS_X,-2.7,0],color=GREEN,stroke_width=3))
        self.play(Create(outer), run_time=.9)
        self.at("lens collects only a cone")
        cone = Polygon(origin, [LENS_X,1.05,0], [LENS_X,-2.35,0], color=BLUE,
                       fill_color=BLUE, fill_opacity=.12, stroke_width=4)
        self.play(FadeIn(cone), outer.animate.set_opacity(.15), run_time=1.0)
        self.at("misses the objective")
        miss = T("fine detail missed", 28, RED).move_to([-2.7,2.45,0])
        self.play(FadeIn(miss), outer.animate.set_color(RED).set_opacity(.55), run_time=.8)
        self.at("Numerical aperture")
        arc = Arc(radius=1.0, start_angle=-.42, angle=.84, color=BLUE, stroke_width=7).move_arc_center_to(origin)
        na = T("numerical aperture", 30, BLUE).move_to([-3.15,2.55,0])
        self.play(Create(arc), FadeIn(na), FadeOut(miss), run_time=1.0)
        self.at("width of the collected cone")
        self.play(cone.animate.set_fill(opacity=.24), arc.animate.scale(1.12, about_point=origin), run_time=.9)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        b = bench(two=True, dim_top=True)
        ax = plot_axes()
        c = profile(lambda x: airy(x), GREEN, 6)
        computed = T("computed", 28, GREY).move_to([2.12, .88, 0])
        self.add(b, ax, c, computed, packets(ys=(-.62, -.88)))
        self.at("ideal lateral model")
        tag = T("Rayleigh, lateral", 28, YELLOW).move_to([3.8,1.18,0])
        self.play(FadeIn(tag), run_time=.6)
        self.at("Rayleigh distance equals")
        card = RoundedRectangle(corner_radius=.15,width=4.7,height=1.0,color=YELLOW,
                                fill_color=BG,fill_opacity=.94).move_to([3.8,2.75,0])
        formula = M("d = 0.61 λem / NA", 31, YELLOW).move_to(card)
        self.play(FadeIn(card), Write(formula), FadeOut(tag), run_time=1.0)
        self.at("Emission wavelength is")
        wave = FunctionGraph(lambda x:.13*np.sin(8*x),x_range=[-1.0,1.0],color=GREEN,stroke_width=4).move_to([-3.35,2.45,0])
        wl = T("emission wavelength", 28, GREEN).next_to(wave,DOWN,buff=.16)
        self.play(Create(wave), FadeIn(wl), run_time=.9)
        self.at("gets smaller with shorter")
        wave2 = FunctionGraph(lambda x:.13*np.sin(12*x),x_range=[-.72,.72],color=GREEN,stroke_width=4).move_to([-3.35,2.45,0])
        narrow1 = profile(lambda x: airy(x,190), GREEN, 6)
        self.play(Transform(wave,wave2), Transform(c,narrow1), run_time=1.2)
        self.at("or higher numerical aperture")
        origin=np.array([-4.75,-.75,0])
        cone=VGroup(Line(origin,[LENS_X,.7,0],color=BLUE,stroke_width=4),Line(origin,[LENS_X,-2.2,0],color=BLUE,stroke_width=4))
        cone2=VGroup(Line(origin,[LENS_X,1.25,0],color=BLUE,stroke_width=4),Line(origin,[LENS_X,-2.65,0],color=BLUE,stroke_width=4))
        narrow2=profile(lambda x: airy(x,165),GREEN,6)
        self.play(Create(cone),run_time=.5)
        self.play(Transform(cone,cone2),Transform(c,narrow2),run_time=1.1)
        dbr=bracket(np.array([3.8,.52,0]),np.array([4.84,.52,0]),"d",YELLOW,size=28)
        self.play(Create(dbr),run_time=.6)
        self.at("one resolution convention")
        convention=T("one convention",30,YELLOW,weight=BOLD).move_to([2.35,.82,0])
        self.remove(computed)
        self.play(FadeIn(convention),run_time=.7)
        self.at("not a universal border")
        self.play(convention.animate.set_color(RED),Circumscribe(convention,color=RED),run_time=.9)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        b, light, sep, ray, question, placeholders = prediction_frame()
        self.add(b, light)
        self.at("restore both vesicles")
        self.play(b.sources[0].animate.set_opacity(1), run_time=.7)
        self.at("separation is 150")
        self.play(Create(sep), run_time=.8)
        self.at("displayed Rayleigh distance")
        self.play(Create(ray), run_time=.8)
        self.at("Will the detector show")
        self.play(FadeIn(question,shift=DOWN*.12),run_time=.7)
        self.at("two peaks or one")
        self.play(LaggedStart(*[Create(p) for p in placeholders],lag_ratio=.25),Indicate(question,color=YELLOW),run_time=1.0)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        b, light, sep, ray, question, placeholders = prediction_frame()
        self.add(b, light, sep, ray, question, placeholders)
        shimmer = question.copy().set_opacity(.12)
        shimmer.add_updater(lambda m,dt: m.set_opacity(.08+.08*(1+np.sin(2*self.renderer.time))/2))
        self.add(shimmer)
        self.wait(4.5)


class S08Reveal(SpokenScene):
    def construct(self):
        b=bench(two=True)
        ax=plot_axes()
        self.add(b,ax,packets())
        h=SOURCE_SEP/2
        self.at("Each source still makes")
        a=profile(lambda x:airy(x-h),GREEN,4,.72,1.65)
        bcurve=profile(lambda x:airy(x+h),GREEN,4,.72,1.65)
        self.play(Create(a),Create(bcurve),run_time=1.3)
        self.at("intensities add point by point")
        plus=T("+",38,YELLOW,weight=BOLD).move_to([3.8,1.05,0])
        self.play(FadeIn(plus),ShowPassingFlash(a.copy().set_stroke(YELLOW,7)),ShowPassingFlash(bcurve.copy().set_stroke(YELLOW,7)),run_time=1.1)
        self.at("merge into one summed peak")
        summed=sum_profile(150)
        self.play(a.animate.set_opacity(.28),bcurve.animate.set_opacity(.28),Create(summed),FadeOut(plus),run_time=1.3)
        computed=T("computed curves",28,GREY).move_to([2.18,.82,0])
        self.play(FadeIn(computed),run_time=.4)
        self.at("no dip survives")
        nodip=T("no dip",30,RED,weight=BOLD).move_to([5.2,.88,0])
        self.play(FadeIn(nodip),Indicate(summed,color=RED,scale_factor=1.02),run_time=.9)
        self.at("They are unresolved here")
        spot=VGroup(*[Circle(r,stroke_width=0,fill_color=RED,fill_opacity=o) for r,o in ((.65,.12),(.4,.28),(.2,.7))]).move_to([3.8,.15,0])
        label=T("one recorded peak",30,RED,weight=BOLD).move_to([3.8,1.18,0])
        self.remove(computed)
        self.play(FadeOut(nodip), FadeIn(spot),FadeIn(label),run_time=.9)
        self.at("other methods may separate")
        self.play(label.animate.set_opacity(.45),summed.animate.set_stroke(width=8),run_time=.8)
        self.finish()


class S09Controls(SpokenScene):
    def construct(self):
        b=bench(two=True)
        ax=plot_axes(); s150=sum_profile(150)
        self.add(b,ax,s150,packets())
        sep_label=M("150 nm",28,YELLOW).move_to([-5.15,1.35,0])
        self.add(sep_label)
        self.at("Move the sources apart")
        s175=sum_profile(175)
        self.play(b.sources[0].animate.shift(UP*.15),b.sources[1].animate.shift(DOWN*.15),Transform(s150,s175),Transform(sep_label,M("175 nm",28,YELLOW).move_to(sep_label)),run_time=1.5)
        self.at("shallow dip opens")
        dip=Arrow([3.8,.85,0],[3.8,.3,0],buff=0,color=YELLOW,stroke_width=4,tip_length=.2)
        shallow=T("dip appears",28,YELLOW).move_to([3.8,1.22,0])
        self.play(GrowArrow(dip),FadeIn(shallow),run_time=.8)
        self.at("At that distance")
        s227=sum_profile(227)
        self.play(b.sources[0].animate.shift(UP*.25),b.sources[1].animate.shift(DOWN*.25),Transform(s150,s227),Transform(sep_label,M("d ≈ 227 nm",28,YELLOW).move_to(sep_label)),run_time=1.5)
        self.at("one quarter of peak height")
        dip_lab=T("Rayleigh: ≈26% dip",30,YELLOW,weight=BOLD).move_to([3.8,1.18,0])
        self.play(ReplacementTransform(shallow,dip_lab),dip.animate.scale(1.25,about_point=dip.get_start()),run_time=.9)
        self.at("clear dip is the convention")
        self.play(Circumscribe(dip_lab,color=YELLOW),ShowPassingFlash(s150.copy().set_stroke(YELLOW,9),time_width=.35),run_time=1.1)
        self.at("marks a clear dip")
        self.play(Indicate(dip,color=YELLOW,scale_factor=1.12),run_time=.8)
        self.at("not the first appearance")
        before=M("175 nm: first dip",28,GREY).move_to([3.8,3.12,0])
        atd=M("227 nm: Rayleigh",28,YELLOW).move_to([3.8,2.62,0])
        self.play(FadeIn(before),FadeIn(atd),run_time=.9)
        self.finish()


class S10Zoom(SpokenScene):
    def construct(self):
        b=bench(two=True); ax=plot_axes(); s=sum_profile(227)
        b.sources[0].shift(UP*.4); b.sources[1].shift(DOWN*.4)
        self.add(b,ax,s,packets())
        self.at("Return the vesicles")
        s150=sum_profile(150)
        self.play(b.sources[0].animate.shift(DOWN*.4),b.sources[1].animate.shift(UP*.4),Transform(s,s150),run_time=1.4)
        self.at("records one peak")
        record=T("DETECTOR RECORD",28,GREY).move_to([3.8,1.18,0])
        self.play(FadeIn(record),Indicate(s,color=RED,scale_factor=1.02),run_time=.8)
        self.at("Software zoom enlarges")
        frozen=VGroup(ax.copy(),s.copy(),record.copy()).scale(.52).move_to([-3.8,-.25,0])
        frame=RoundedRectangle(corner_radius=.15,width=4.8,height=4.6,color=GREY).move_to([-3.8,-.25,0])
        display=RoundedRectangle(corner_radius=.15,width=5.3,height=5.1,color=YELLOW).move_to([3.55,-.25,0])
        grid=VGroup(*[Line([1.05+i*.53,-2.4,0],[1.05+i*.53,1.9,0],color=GREY,stroke_width=1,stroke_opacity=.4) for i in range(11)],
                    *[Line([1.05,-2.4+i*.48,0],[6.05,-2.4+i*.48,0],color=GREY,stroke_width=1,stroke_opacity=.4) for i in range(10)])
        zoomcurve=s.copy().scale(1.18).move_to([3.55,-.45,0])
        self.play(FadeOut(VGroup(b,ax,s,record)),FadeIn(frame),FadeIn(frozen),FadeIn(display),Create(grid),Create(zoomcurve),run_time=1.4)
        zoomlab=T("SOFTWARE ZOOM",30,YELLOW,weight=BOLD).move_to([3.55,2.65,0])
        self.play(FadeIn(zoomlab),zoomcurve.animate.scale(1.22),grid.animate.scale(1.08),run_time=1.0)
        self.at("cannot add detail")
        cross=Cross(Dot([3.55,.2,0],radius=.3),stroke_color=RED,stroke_width=7).scale(1.35)
        missing=T("missing dip",28,RED).next_to(cross,DOWN,buff=.18)
        self.play(Create(cross),FadeIn(missing),run_time=.8)
        self.at("Optical magnification before")
        optical=T("OPTICAL MAGNIFICATION ≠ SOFTWARE ZOOM",28,BLUE,weight=BOLD).move_to([0,3.35,0])
        self.play(FadeIn(optical),run_time=.8)
        self.at("change sampling")
        self.play(Indicate(frame,color=BLUE),run_time=.7)
        self.at("different operation")
        self.play(Circumscribe(optical,color=BLUE),run_time=.7)
        self.at("Bigger display pixels")
        self.play(grid.animate.set_stroke(width=3,opacity=.65),zoomcurve.animate.scale(1.1),run_time=.9)
        self.at("cannot recover a missing dip")
        self.play(Indicate(cross,color=RED,scale_factor=1.25),run_time=.9)
        self.finish()


class S11ChangeMeasurement(SpokenScene):
    def construct(self):
        b=bench(two=True); light=packets()
        self.add(b,light)
        self.at("change how information enters")
        heading=T("CHANGE THE MEASUREMENT",38,YELLOW,weight=BOLD).move_to([.1,3.15,0])
        self.play(FadeIn(heading),run_time=.8)
        self.at("confocal pinhole")
        pin=VGroup(Rectangle(width=.35,height=4.3,color=BLUE,fill_color=BLUE,fill_opacity=.55),
                   Circle(.22,color=BG,fill_color=BG,fill_opacity=1)).move_to([LENS_X,-.15,0])
        conf=T("confocal",30,BLUE,weight=BOLD).move_to([-.8,2.45,0])
        haze=VGroup(*[Circle(.18+i*.06,color=GREEN,stroke_opacity=.18).move_to([-3.0,1.45+i*.2,0]) for i in range(5)])
        self.play(ReplacementTransform(b.lens,pin),FadeOut(b[3]),FadeIn(conf),FadeIn(haze),run_time=1.0)
        self.at("out-of-focus light reaches")
        self.play(haze.animate.shift(UP*.8).set_opacity(0),pin.animate.set_color(BLUE),run_time=1.0)
        self.at("Super resolution asks")
        stripes=VGroup(*[Line([-1.7+i*.32,-2.0,0],[-.7+i*.32,1.8,0],color=YELLOW,stroke_width=5) for i in range(6)])
        sr=T("super-resolution",30,YELLOW,weight=BOLD).move_to([-.8,2.45,0])
        self.remove(conf)
        self.add(sr)
        self.play(FadeOut(pin),LaggedStart(*[Create(x) for x in stripes],lag_ratio=.08),run_time=1.1)
        self.at("illumination or glowing molecules")
        self.play(stripes.animate.shift(RIGHT*.7),b.sources[0].animate.set_opacity(.2),b.sources[1].animate.set_opacity(1),run_time=.9)
        self.at("encode closer detail")
        self.play(b.sources[0].animate.set_opacity(1),b.sources[1].animate.set_opacity(.2),stripes.animate.shift(LEFT*1.2),run_time=.9)
        self.at("Electron microscopy")
        beam=VGroup(Rectangle(width=.65,height=4.5,color=GREY,fill_color=GREY,fill_opacity=.32),
                    Arrow([-.8,1.8,0],[-.8,-1.8,0],buff=0,color=TEXT,stroke_width=6,tip_length=.28)).move_to([LENS_X,-.15,0])
        em=T("electron microscopy",30,GREY,weight=BOLD).move_to([-.8,2.45,0])
        self.remove(sr)
        self.add(em)
        self.play(FadeOut(stripes),FadeIn(beam),run_time=1.0)
        self.at("different probe")
        self.play(ShowPassingFlash(beam[1].copy().set_stroke(YELLOW,9),time_width=.4),run_time=.9)
        self.at("Each change answers")
        path=VGroup(chip("confocal",BLUE,28),chip("super-resolution",YELLOW,28),chip("electron microscopy",GREY,28)).arrange(RIGHT,buff=.35).move_to([0,-3.35,0])
        self.play(LaggedStart(*[FadeIn(x,shift=UP*.1) for x in path],lag_ratio=.15),run_time=1.1)
        self.at("brings new limits")
        limits=T("new measurement • new limits",30,RED,weight=BOLD).move_to([3.8,1.25,0])
        self.play(FadeIn(limits),run_time=.8)
        self.finish()


class S12End(SpokenScene, EndCard):
    LINE = "Software zoom cannot add detail the measurement never captured."

    def construct(self):
        b=bench(two=True).set_opacity(.6); light=packets()
        self.add(b,light)
        self.at("microscope image is a measurement")
        statement=T("A MICROSCOPE IMAGE IS A MEASUREMENT",36,TEXT,weight=BOLD).move_to([.2,3.15,0])
        self.play(FadeIn(statement),run_time=.8)
        self.at("ask what was labeled")
        checks=[]
        for x,label in ((-5.15,"✓  label"),(-.8,"✓  separation"),(3.8,"✓  record")):
            item=T(label,28,TEXT,weight=BOLD).move_to([x,2.4,0]); checks.append(item)
        self.play(FadeIn(checks[0],shift=DOWN*.1),run_time=.7)
        self.at("instrument could separate")
        self.play(FadeIn(checks[1],shift=DOWN*.1),Indicate(b.lens,color=BLUE),run_time=.8)
        self.at("detector recorded")
        self.play(FadeIn(checks[2],shift=DOWN*.1),run_time=.7)
        self.at("Software Zoom makes")
        self.play(b.animate.scale(1.04),run_time=.8)
        self.at("same record bigger")
        self.play(b.animate.scale(1.08),run_time=.8)
        self.at("Software Zoom cannot")
        final=T("Software zoom cannot add detail\nthe measurement never captured.",52,TEXT,
                font=TITLE_FONT, line_spacing=.85)
        fit(final,max_w=11.7)
        rule=Line([-2.4,-1.05,0],[2.4,-1.05,0],color=GOLD,stroke_width=4)
        self.play(FadeOut(VGroup(b,light,statement,*checks)),FadeIn(final),GrowFromCenter(rule),run_time=1.1)
        self.at("never captured")
        shimmer = RoundedRectangle(corner_radius=.22, width=final.width + .8,
                                   height=final.height + .55, stroke_width=0,
                                   fill_color=GREEN, fill_opacity=.045).move_to(final)
        shimmer.set_z_index(-1)
        shimmer.add_updater(lambda m,dt:m.set_fill(opacity=.025+.045*(1+np.sin(2*self.renderer.time))/2))
        self.add(shimmer)
        self.play(Indicate(final,color=GREEN,scale_factor=1.03),run_time=.9)
        self.finish()
