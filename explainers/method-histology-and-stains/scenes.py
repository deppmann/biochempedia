"""Histology and Stains, timed to the supplied Kokoro narration.

BLUE: glass and microscope optics. GREY: tissue structure and inactive detail.
PURPLE: Nissl, Gram violet and DNA-stained chromatin. GOLD: antibody signal,
dates and the guiding rule. RED: binding failure and Gram counterstain.
"""
from bp_parts import *
from bp_style import EndCard


PURPLE = "#B58CD9"
VIOLET_INK = "#4C306A"
PINK = "#F793AB"
PALE = "#DED8D9"
TISSUE = "#A99EAB"
INK = "#292033"
GLASS = "#293E50"
QUESTION = "Can this stain prove they fuse?"
RATIO = 200 / 20


def xy(x, y):
    return np.array([x, y, 0.0])


def oval(x, y, w, h, color, rim=None, opacity=1):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=opacity,
                   stroke_color=rim or color, stroke_width=2 if rim else 0).move_to(xy(x, y))


def line(points, color, width=3):
    return VMobject().set_points_as_corners([xy(*p) for p in points]).set_stroke(color, width)


def branch(points, color=INK, width=4):
    return VMobject().set_points_smoothly([xy(*p) for p in points]).set_stroke(color, width)


def heading(text, color=TEXT):
    return fit_text(text, max_w=11.5, size=38, min_size=30).move_to(xy(0, 3.35))


def outline():
    return RoundedRectangle(corner_radius=0.3, width=11.7, height=5.68,
                            color=BLUE, stroke_width=2, fill_color=GLASS, fill_opacity=1)


def stage():
    """Fixed glass slide, stage edge and holding clips, shared across specimens."""
    glass = outline()
    bevel = line([(-5.6, -2.73), (-5.4, -2.91), (5.4, -2.91), (5.6, -2.73)], GLASS, 6)
    clips = VGroup(*[
        RoundedRectangle(width=0.67, height=1.12, corner_radius=0.11, color=BLUE,
                         stroke_width=2, fill_color=GLASS, fill_opacity=1).move_to(xy(x, 0.35))
        for x in (-5.77, 5.77)
    ])
    return VGroup(bevel, glass, clips)


def section(color=PALE):
    points = [(4.94*np.cos(t), 2.44*np.sin(t)) for t in np.linspace(0, TAU, 22, endpoint=False)]
    points = [(x*(1 + 0.027*np.cos(3*i)), y + 0.095*np.cos(1.7*i)) for i, (x, y) in enumerate(points)]
    return VMobject().set_points_smoothly([xy(*p) for p in points + points[:1]]).set_fill(
        color, 1).set_stroke(TEXT, 2, opacity=0.66)


def focus(w=7.3, h=3.5, x=0, y=0, color=WHITE):
    """Moving illumination within the specimen, as the microscope field comes into focus."""
    rings = VGroup(*[oval(x, y, w*f, h*f, color, opacity=0.13)
                     for f in (1, 0.81, 0.62, 0.43)])
    base = rings.get_center().copy()
    clock = 0.0

    def rack_light(field, dt):
        nonlocal clock
        clock += dt
        field.move_to(base + RIGHT*.65*np.sin(1.36*clock) + UP*.27*np.sin(1.79*clock))
        field.set_fill(opacity=.13 + .057*np.sin(2.48*clock))

    return rings.add_updater(rack_light)


def soma(x, y, r=0.15, color=VIOLET_INK, nucleus=PALE):
    body = oval(x, y, 2*r, 1.7*r, color).rotate(-0.22)
    return VGroup(body, oval(x + 0.13*r, y, r*0.71, r*0.63, nucleus))


def cortical_positions():
    rng = np.random.default_rng(16)
    for row, (y, count, span) in enumerate(((1.57, 14, 3.25), (0.98, 19, 4.04),
                                              (0.37, 24, 4.49), (-0.40, 13, 4.40),
                                              (-1.15, 19, 3.95), (-1.67, 13, 3.18))):
        for x in np.linspace(-span, span, count):
            yield x + rng.uniform(-0.09, 0.09), y + 0.06*np.cos(x) + rng.uniform(-0.15, 0.15), row


def nissl_bodies():
    return VGroup(*(VGroup(*[soma(x, y, 0.125 + 0.017*((index + row) % 3))
                            for index, (x, y, r) in enumerate(cortical_positions()) if r == row])
                    for row in range(6)))


def crowd():
    rng = np.random.default_rng(33)
    threads = VGroup()
    bodies = VGroup()
    for i, (x, y, _) in enumerate(cortical_positions()):
        bodies.add(soma(x, y, 0.20, INK, TISSUE))
        if i % 2:
            dx, dy = rng.uniform(-1.15, 1.15), rng.uniform(-0.90, 0.90)
            points = [(x, y), (x + dx*.35, y + dy*.85), (x + dx*.93, y + dy*.4),
                      (x + dx, y + dy)]
            points = [(px, py) if (px/4.74)**2 + (py/2.29)**2 < 0.93 else (px*.82, py*.78)
                      for px, py in points]
            threads.add(branch(points, INK, 2.8))
    return VGroup(threads, bodies)


def contact_paths():
    """Terminal segments shared by the whole section and the junction enlargement."""
    return ([(-0.59, 0.19), (-0.33, 0.08), (-0.17, 0.06), (-0.02, 0.04)],
            [(0.02, 0.04), (0.19, -0.05), (0.37, -0.08), (0.59, -0.17)])


def neuron(x, y, scale=1, direction=1):
    paths = [
        [(0, 0), (-.34, .52), (-.38, .98), (-.64, 1.47)],
        [(-.38, .98), (-.09, 1.39), (.05, 1.74)],
        [(-.38, .98), (-.92, 1.12), (-1.22, 1.37)],
        [(-.34, .52), (-.80, .59), (-1.18, .83)],
        [(0, 0), (.42, .35), (.77, .58), (1.04, .99)],
        [(.77, .58), (1.10, .57), (1.41, .76)],
        [(0, 0), (-.19, -.53), (.03, -1.05), (-.05, -1.56)],
        [(-.19, -.53), (-.62, -.73), (-.86, -1.02)],
        [(.03, -1.05), (.43, -1.25), (.55, -1.51)],
    ]
    trees = VGroup(*[branch([(x + direction*scale*a, y + scale*b) for a,b in p],
                            width=(3.6 if i in (0, 4, 6) else 2.1))
                     for i, p in enumerate(paths)])
    return VGroup(oval(x, y, .47*scale, .58*scale, INK).rotate(.28*direction), trees)


def golgi_neurons():
    left, right = contact_paths()
    return VGroup(neuron(-2.00, -0.36, 1.06), neuron(2.13, 0.52, .84, -1),
                  neuron(3.65, -0.62, .49),
                  VGroup(branch([(-2.0, -.36), (-1.56, -.22), (-1.07, .02), left[0]], width=3.7),
                         branch(left, width=3.2), branch(right, width=3.2),
                         branch([right[-1], (.96, -.02), (1.52, .04), (2.13, .52)], width=3.7)))


def target_cell(x, y, r=.37, marked=False):
    body = oval(x, y, 2*r, 1.62*r, GOLD if marked else TISSUE,
                rim=INK if marked else GREY).rotate(-.25)
    nucleus = oval(x-.07*r, y, .61*r, .66*r, INK if marked else "#736779")
    return VGroup(body, nucleus)


def antibody(x, y, scale=1, rotation=0, color=GOLD):
    """A conventional Y-shaped marker, drawn as a single icon."""
    marker = VGroup(line([(0, -.24), (0, 0), (-.19, .23)], color, 5),
                    line([(0, 0), (.19, .23)], color, 5))
    return marker.scale(scale).rotate(rotation).move_to(xy(x, y))


class S01Hook(SpokenScene):
    def construct(self):
        tissue = section()
        light = focus(color="#7C6B89")
        cells = crowd()
        self.add(stage(), tissue, light)
        self.at("see one cell")
        self.play(FadeIn(cells[1][53], scale=0.9), run_time=0.55)
        self.at("every cell at once")
        self.remove(cells[1][53])
        self.play(tissue.animate.set_fill("#937B94"), FadeIn(cells[1], shift=RIGHT*.14),
                  run_time=1.7)
        self.at("dark crowd of bodies")
        self.play(LaggedStart(*(Create(t) for t in cells[0]), lag_ratio=.045), run_time=2.6)
        self.at("no eye can follow")
        x, y, _ = list(cortical_positions())[53]
        ring = Circle(radius=.37, color=YELLOW, stroke_width=4).move_to(xy(x, y))
        self.play(Create(ring), run_time=.35)
        self.play(FadeIn(T("?", 52, YELLOW).move_to(xy(x, -3.35))), run_time=.45)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Histology and Stains"
    TITLE = "Making Cells Stand Out in Tissue"

    def construct(self):
        tissue, cells = section("#937B94"), crowd()
        title = T(self.TITLE, 47, font=TITLE_FONT).move_to(xy(0, 3.35))
        self.add(stage(), tissue, cells)
        self.play(FadeOut(cells), tissue.animate.set_fill(PALE), run_time=.56)
        self.play(FadeIn(title, shift=UP*.10), run_time=.37)
        self.wait(.63)
        self.play(FadeOut(title), run_time=.43)


class S03Nissl(SpokenScene):
    def construct(self):
        tissue = section()
        rows = nissl_bodies()
        self.add(stage(), tissue, focus())
        self.at("one target at a time")
        self.play(tissue.animate.set_fill("#C9B0D8"), FadeIn(rows[2], shift=RIGHT*.22), run_time=1.45)
        self.at("stain binds the")
        name = heading("Nissl stain", PURPLE)
        self.play(FadeIn(name), run_time=.45)
        self.at("rich cytoplasm")
        self.play(LaggedStart(*(FadeIn(rows[i], shift=RIGHT*.21) for i in (0, 1, 3, 4, 5)),
                              lag_ratio=.36), run_time=3.45)
        self.at("cell bodies light up")
        self.play(FadeIn(caption("Cell bodies and layers", color=PURPLE, y=-3.4)), run_time=.55)
        self.at("finding layer boundaries")
        braces = VGroup(*[line([(4.34, y), (4.57, y), (4.57, y+.40), (4.34, y+.40)],
                                VIOLET_INK, 3) for y in (-1.45, -.46, .31)])
        self.play(LaggedStart(*(Create(b) for b in braces), lag_ratio=.22), run_time=1.12)
        self.finish()


class S04Golgi(SpokenScene):
    def construct(self):
        tissue, rows = section("#C9B0D8"), nissl_bodies()
        old = heading("Nissl stain", PURPLE)
        self.add(stage(), tissue, focus(), rows, old)
        self.at("branches stay hidden")
        self.play(FadeOut(old), run_time=.47)
        self.play(FadeOut(rows), tissue.animate.set_fill(PALE), run_time=1.65)
        neurons = golgi_neurons()
        for n in neurons[:3]:
            n[0].save_state()
            n[0].scale(.65).set_opacity(0)
        self.at("golgi stain")
        title = heading("Golgi stain")
        self.play(FadeIn(title), run_time=.6)
        self.at("the opposite problem")
        self.play(LaggedStart(*(Restore(n[0]) for n in neurons[:3]), lag_ratio=.67), run_time=4.05)
        self.at("including their branching")
        self.play(LaggedStart(*(LaggedStart(*(Create(b) for b in n[1]), lag_ratio=.12)
                                 for n in neurons[:3]), Create(neurons[3]), lag_ratio=.22), run_time=4)
        self.at("stands out whole")
        self.play(FadeIn(caption("Whole neuron shape", y=-3.4)), run_time=.47)
        self.finish()


class S05Immuno(SpokenScene):
    def construct(self):
        coords = [(-3.7, .8), (-2.3, 1.42), (-.64, 1.22), (1.3, 1.48), (3.15, 1.01),
                  (-3.85, -.63), (-2.03, -.09), (.03, -.04), (2.2, .04), (3.58, -.55),
                  (-2.9, -1.25), (-1.3, -1.45), (.74, -1.35), (2.4, -1.24)]
        cells = VGroup(*(target_cell(x, y) for x, y in coords))
        selected = (1, 7, 13)
        self.add(stage(), section(), focus(), cells)
        self.at("one chosen protein")
        markers = [antibody(x-.95, y+.51, .93, -PI/2, INK)
                   for x, y in (coords[i] for i in selected)]
        self.play(LaggedStart(*(FadeIn(m, shift=LEFT*.48) for m in markers), lag_ratio=.34),
                  run_time=1.4)
        self.at("use immunostaining")
        self.play(FadeIn(heading("Immunostaining", GOLD)), run_time=.56)
        self.at("antibody binds")
        self.play(LaggedStart(*(m.animate.shift(RIGHT*.39 + DOWN*.51) for m in markers),
                              lag_ratio=.31), run_time=2.06)
        self.at("marking only cells")
        self.play(LaggedStart(*(Transform(cells[i], target_cell(*coords[i], marked=True))
                               for i in selected), lag_ratio=.45), run_time=2.15)
        self.at("reveals only its target")
        self.play(FadeIn(caption("One chosen target", color=GOLD, y=-3.4)), run_time=.6)
        self.finish()


def enlarged_tips():
    left, right = contact_paths()
    tips = [(10*x, 10*(y-.04)) for x, y in (left[-1], right[0])]
    shapes = (
        ((-5.15, 1.52), ((-3.30, 1.47), (-3.18, .61), (-1.18, .25)),
         ((-.70, .16), (tips[0][0], .14), tips[0]),
         ((tips[0][0], -.16), (-.78, -.22), (-1.34, -.30)),
         ((-2.74, -.56), (-3.60, -.42), (-5.15, -.53))),
        ((5.15, -1.69), ((3.43, -1.70), (3.16, -1.09), (1.32, -.44)),
         ((.77, -.26), (tips[1][0], -.16), tips[1]),
         ((tips[1][0], .16), (.83, .17), (1.39, .09)),
         ((2.63, -.05), (3.54, -.49), (5.15, -.20))),
    )
    tips_group = VGroup()
    for start, *curves in shapes:
        tip = VMobject(fill_color=INK, fill_opacity=1, stroke_width=0)
        tip.start_new_path(xy(*start))
        for controls in curves:
            tip.add_cubic_bezier_curve_to(*(xy(*point) for point in controls))
        tip.close_path()
        tips_group.add(tip)
    return tips_group


def junction_blur():
    return VGroup(*(oval(0, 0, w, w, "#725584", opacity=.10)
                    for w in (4, 3.63, 3.18, 2.74, 2.24, 1.71, 1.15)),
                  Circle(radius=2, color=VIOLET_INK, stroke_width=2, stroke_opacity=.62))


def gap_marker():
    return VGroup(line([(-.20, -.42), (-.20, -.18)], YELLOW, 3),
                  line([(.20, -.42), (.20, -.18)], YELLOW, 3),
                  line([(-.20, -.39), (.20, -.39)], YELLOW, 3))


def gap_labels():
    return heading("Light microscope limit ≈ 200 nm", PURPLE), T(
        "≈ 20 nm gap", 30, INK, weight=BOLD).move_to(xy(0, -1.16))


def prediction_card():
    return question_card(QUESTION, y=-3.41, size=38).move_to(xy(0, -3.41))


def zoom_glass():
    return RoundedRectangle(width=10.9, height=5.20, corner_radius=.34, color=TEXT,
                            stroke_width=2, fill_color=PALE, fill_opacity=1)


class S06PredictQ(SpokenScene):
    def construct(self):
        glass, small = section(), golgi_neurons()
        light = focus()
        tips, blur = enlarged_tips(), junction_blur()
        limit, gap = gap_labels()
        self.add(stage(), glass, light, small)
        self.at("test a limit")
        zoom = Circle(radius=.52, color=VIOLET_INK, stroke_width=3)
        self.play(Create(zoom), run_time=.53)
        self.play(FadeOut(small), FadeOut(zoom, scale=4), Transform(glass, zoom_glass()),
                  FadeIn(tips, scale=.28), run_time=1.45)
        self.remove(light)
        light = focus(w=7, h=3.7)
        self.add(light, tips)
        self.at("points closer than")
        self.play(FadeIn(blur, scale=.58), run_time=1.50)
        self.play(FadeIn(limit), run_time=.48)
        self.play(blur[:-1].animate.set_fill(opacity=.20), run_time=1.75)
        self.at("the gap between")
        self.play(Create(gap_marker()), blur[:-1].animate.set_fill(opacity=.10), run_time=1.38)
        self.at("about 20 nanometers")
        self.play(FadeIn(gap), run_time=.54)
        self.at("stain branches look joined")
        self.play(blur[:-1].animate.set_fill(opacity=.25), run_time=1.38)
        self.at("prove they fuse")
        self.play(FadeIn(prediction_card()), run_time=.53)
        self.play(FadeOut(light), blur[:-1].animate.set_fill(opacity=.10),
                  run_time=self.narration_s + .4 - self.elapsed(), rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        config.background_color = BG
        self.camera.background_color = BG
        self.add(stage(), zoom_glass(), enlarged_tips(), junction_blur(), gap_marker(),
                 *gap_labels(), prediction_card())
        self.wait(4.5)


def depth_layers():
    layers = VGroup()
    for i in range(3):
        band = section(["#867789", "#A498AE", PALE][i]).stretch(.49, dim=1)
        spec = golgi_neurons().stretch(.49, dim=1)
        layers.add(VGroup(band, spec))
    return layers


class S08LimitsOptics(SpokenScene):
    def construct(self):
        specimen, tips, blur = zoom_glass(), enlarged_tips(), junction_blur()
        measure = gap_marker()
        limit, gap = gap_labels()
        question = prediction_card()
        self.add(stage(), specimen, tips, blur, measure, limit, gap, question)
        self.at("now", lead=0)
        answer = caption("No", size=36, color=GOLD, y=-3.4).move_to(xy(0, -3.4))
        self.play(swap(question, answer), blur[:-1].animate.set_fill(opacity=.23),
                  run_time=.72, rate_func=linear)
        self.at("divide 200")
        self.play(FadeOut(answer), run_time=.27)
        equation = VGroup(*(M(s, 35, YELLOW) for s in ("200 nm", "÷", "20 nm", "=", f"{RATIO:g}")))
        equation.arrange(RIGHT, buff=.30).move_to(xy(0, -3.4))
        self.play(FadeIn(equation[0]), blur.animate.set_fill(opacity=.17), run_time=.74)
        self.at("by 20 nanometers")
        self.play(LaggedStart(FadeIn(equation[1]), FadeIn(equation[2]), lag_ratio=.44),
                  blur.animate.set_fill(opacity=.07), run_time=.92)
        self.at("you get 10")
        self.play(LaggedStart(FadeIn(equation[3]), FadeIn(equation[4]), lag_ratio=.44),
                  blur.animate.set_fill(opacity=.14), run_time=1.26)
        self.at("10 times below")
        self.play(blur.animate.set_fill(opacity=.04), run_time=1.28)
        self.at("section can be")
        layers = depth_layers()
        self.play(FadeOut(VGroup(limit, gap, equation)), run_time=.29)
        self.play(FadeOut(VGroup(specimen, tips, blur, measure)), FadeIn(layers), run_time=.48)
        self.at("100 micrometers")
        self.play(layers[0].animate.shift(DOWN*1.14 + RIGHT*.29),
                  layers[2].animate.shift(UP*1.18 + LEFT*.31), run_time=1.45)
        self.play(FadeIn(heading("100 µm or more thick")), run_time=.53)
        self.at("stacking branches")
        self.play(layers[0].animate.shift(DOWN*.18 + RIGHT*.14),
                  layers[2].animate.shift(UP*.18 + LEFT*.13), run_time=1.65)
        self.finish()


class S09LimitsBinding(SpokenScene):
    def construct(self):
        self.add(stage())
        panels = TwoPanel("Chick cell", "Human muscle fibre", colors=(BLUE, TEXT),
                          width=10.9, top=2.63, bottom=-2.65, size=29)
        x_left, x_right = -2.83, 2.83
        cell = target_cell(x_left + .12, -.09, 1.29)
        cell[0].set_fill(PALE)
        site = RoundedRectangle(width=.44, height=.75, corner_radius=.12, stroke_width=0,
                                fill_color=VIOLET_INK, fill_opacity=1).move_to(xy(x_left-1.02, -.29))
        marker = antibody(x_left-1.5, 1.25, 1.33, -PI/2)
        self.add(panels.left_frame, panels.left_head, focus(3.8, 2.8, x_left, -.48, color=BLUE), cell, site)
        self.at("antibody against")
        self.play(FadeIn(marker, shift=DOWN*.20), run_time=.66)
        self.play(marker.animate.move_to(xy(x_left-1.87, .65)), run_time=1.25)
        self.at("miss the chick")
        self.play(marker.animate.move_to(xy(x_left-1.83, -.91)), run_time=1.32,
                  rate_func=linear)
        self.at("its site is masked")
        cover = oval(x_left-1.16, -.29, .55, .91, GREY, rim=TEXT)
        self.play(FadeIn(cover, scale=.65), run_time=.49)
        self.play(marker.animate.move_to(xy(x_left-1.57, -.47)), run_time=.47)
        self.play(marker.animate.move_to(xy(x_left-1.94, -.91)).rotate(-.65), run_time=.58)
        self.at("in 1994")
        date = heading("Smerdu and colleagues · 1994", GOLD)
        self.play(FadeIn(date), FadeIn(panels.right_frame), run_time=.6)
        self.add(focus(3.8, 2.3, x_right, .14, color=PURPLE))
        fibre = RoundedRectangle(width=3.92, height=1.37, corner_radius=.62,
                                 stroke_width=2, stroke_color=TEXT, fill_color="#AE778D",
                                 fill_opacity=1).move_to(xy(x_right, .02))
        ribs = VGroup(*[oval(x_right+d, .02, .075, 1.05, "#653A58", opacity=.67)
                        for d in np.linspace(-1.49, 1.49, 15)])
        self.at("studied human fibers")
        self.play(FadeIn(VGroup(fibre, ribs), scale=.72), run_time=1.05)
        self.play(FadeIn(panels.right_head), run_time=.33)
        self.at("labeled type IIb")
        old = boxed_label("Label: type IIb", PINK, size=29).move_to(xy(x_right, -1.63))
        old.box.set_fill(BG, 1)
        self.play(FadeIn(old), run_time=.57)
        self.at("those fibers express")
        self.play(ribs.animate.set_fill("#F1B2CA"), run_time=1.20)
        self.at("type IIx myosin")
        new = boxed_label("Mostly type IIx myosin", GOLD, size=29).move_to(xy(x_right, -1.63))
        self.play(swap(old, new), run_time=.77)
        self.play(fibre.animate.set_fill("#855976"), run_time=2.45)
        self.at("stains label named")
        self.play(FadeIn(caption("The stain named the wrong protein", color=GOLD, y=-3.40)), run_time=.67)
        self.finish()


class S10UnlockedGolgi(SpokenScene):
    def construct(self):
        neurons = golgi_neurons()
        self.add(stage(), section(), focus(color="#7E6A8B"))
        self.at("stains unlocked")
        self.play(LaggedStart(*(FadeIn(n[0], scale=.7) for n in neurons[:3]), lag_ratio=.53), run_time=2.2)
        self.at("in 1873")
        title = heading("1873 · Golgi stain", GOLD)
        self.play(FadeIn(title), run_time=.63)
        self.at("golgi stain filled")
        self.play(LaggedStart(*(LaggedStart(*(Create(b) for b in n[1]), lag_ratio=.12)
                                 for n in neurons[:3]), Create(neurons[3]), lag_ratio=.17), run_time=3.65)
        self.at("separate cells versus")
        question = caption("Separate cells or a fused network?", y=-3.4)
        ring = Circle(radius=.45, color=VIOLET_INK, stroke_width=3).move_to(xy(0, .04))
        self.play(Create(ring), run_time=.75)
        self.play(FadeIn(question), run_time=.55)
        self.at("with evidence")
        self.play(ring.animate.scale(1.24), run_time=1.25, rate_func=there_and_back)
        self.at("settling the gap")
        self.play(FadeOut(ring), run_time=.44)
        delay = caption("About 80 years later", color=GOLD, y=-3.4)
        self.play(swap(question, delay), run_time=.83)
        self.at("the electron microscope")
        self.play(swap(delay, caption("Electron microscopy settles the gap", color=GOLD, y=-3.4)),
                  run_time=.8)
        self.finish()


def smear_field():
    return RoundedRectangle(width=10.6, height=4.94, corner_radius=.58,
                            stroke_color=BLUE, stroke_width=1.7, fill_color="#B9BFCB",
                            fill_opacity=1)


def bacterium(x, y, thick, color=TISSUE, archaeal=False):
    if archaeal:
        return oval(x, y, 2.43, 1.91, color, rim=INK)
    w, h = 2.81, 1.51
    coat = RoundedRectangle(width=w, height=h, corner_radius=.73, color=INK,
                            stroke_width=2.4, fill_color=INK if thick else BLUE,
                            fill_opacity=1)
    inset = .37 if thick else .20
    cell = RoundedRectangle(width=w-inset, height=h-inset, corner_radius=(h-inset)/2-.018,
                             color=VIOLET_INK if thick else INK, stroke_width=2,
                             fill_color=color, fill_opacity=1)
    return VGroup(coat, cell).move_to(xy(x, y))


def wash(color):
    return VGroup(*(oval(-3.18, 0, 2.8*f, 4.04*f, color, opacity=.14)
                    for f in (1, .80, .61, .43)))


class S11UnlockedGram(SpokenScene):
    def construct(self):
        self.add(stage())
        field = smear_field()
        thick = bacterium(-2.85, .30, True)
        thin = bacterium(2.85, .30, False)
        cells = VGroup(thick, thin).set_z_index(2)
        self.at("in 1884")
        self.play(FadeIn(field, shift=RIGHT*.62), run_time=.79)
        self.add(focus(w=7.7, h=3.5))
        self.play(FadeIn(heading("1884 · Gram stain", GOLD)), run_time=.65)
        self.at("stain sorting bacteria")
        self.play(LaggedStart(*(FadeIn(c, scale=.83) for c in cells), lag_ratio=.72), run_time=2.35)
        self.at("cells take up")
        dye = wash(VIOLET_INK).set_z_index(1)
        self.play(FadeIn(dye), run_time=.32)
        self.play(dye.animate.shift(RIGHT*6.36), thick[1].animate.set_fill(VIOLET_INK),
                  thin[1].animate.set_fill(VIOLET_INK), run_time=1.13)
        self.at("alcohol wash")
        rinse = wash(WHITE).set_z_index(1)
        self.play(FadeOut(dye), FadeIn(rinse), run_time=.35)
        self.play(rinse.animate.shift(RIGHT*6.36), run_time=1.06)
        self.play(FadeOut(rinse), run_time=.44)
        self.at("thick peptidoglycan wall")
        thick_label = boxed_label("Thick wall", INK, size=29, fill_opacity=.06).set_z_index(3).move_to(xy(-2.85, -1.49))
        self.play(thick[0].animate.set_stroke(VIOLET_INK, 6), run_time=.69)
        self.play(FadeIn(thick_label), run_time=.42)
        self.at("stay purple")
        self.play(thick[1].animate.set_fill("#714892"), run_time=1.70, rate_func=there_and_back)
        self.at("thin walled cells lose")
        self.play(thin[1].animate.set_fill(PALE), run_time=.57)
        thin_label = boxed_label("Thin wall", INK, size=29, fill_opacity=.06).set_z_index(3).move_to(xy(2.85, -1.49))
        self.play(FadeIn(thin_label), run_time=.39)
        self.at("red counter stain")
        red = wash(RED).shift(RIGHT*3.8).set_z_index(1)
        self.play(FadeIn(red), run_time=.34)
        self.play(red.animate.shift(RIGHT*2.55), thin[1].animate.set_fill(PINK), run_time=1.23)
        self.play(FadeOut(red), run_time=.41)
        self.at("some archaea")
        archaeon = bacterium(0, .39, False, TISSUE, archaeal=True)
        self.play(FadeIn(archaeon, scale=.63), run_time=.73)
        arch_label = boxed_label("Some archaea", INK, size=28, fill_opacity=.06).set_z_index(3).move_to(xy(0, -1.49))
        self.play(FadeIn(arch_label), run_time=.38)
        self.at("and stain purple")
        self.play(archaeon.animate.set_fill(VIOLET_INK), run_time=.87)
        self.at("reads the envelope")
        self.play(FadeIn(caption("Reads envelope, not domain", color=GOLD, y=-3.4)), run_time=.68)
        self.finish()


def embryo_section():
    return VGroup(section("#ABA6BC"),
                  branch([(-4.55, -.31), (-3.32, -.83), (-1.28, -.88), (.29, -.45),
                          (2.1, .49), (4.45, .59)], "#D3CDD6", 14),
                  branch([(-4.41, .50), (-3.2, .69), (-.79, .39), (1.4, -.11),
                          (3.2, -.86), (4.31, -.58)], "#D3CDD6", 12))


def embryo_cell(x, y, marked=False, scale=1):
    cell = oval(x, y, .92, .71, "#C9C2CD", rim="#85778A").rotate(.30)
    nucleus = oval(x, y, .53, .47, "#E8E0E6", rim="#8F7998")
    nucleolus = oval(x+.04, y+.045, .11, .11, "#927FA5")
    body = VGroup(cell, nucleus, nucleolus)
    if marked:
        body.add(oval(x-.115, y-.025, .23, .205, VIOLET_INK))
    return body.scale(scale)


class S12UnlockedQuail(SpokenScene):
    def construct(self):
        self.add(stage())
        specimen = embryo_section()
        positions = [(-3.75, .37), (-3.05, 1.13), (-2.99, -.81), (-1.85, .05),
                     (-1.56, -1.26), (-.88, 1.42), (-.79, -.53), (.31, .64),
                     (.55, -1.54), (1.45, -1.14), (2.34, 1.51), (3.03, -.42), (3.58, .68)]
        chick = VGroup(*(embryo_cell(x, y, scale=.83+.06*(i%3))
                         for i, (x, y) in enumerate(positions)))
        self.at("nicole")
        self.play(FadeIn(specimen, shift=RIGHT*.62), run_time=.75)
        self.add(focus())
        self.play(FadeIn(heading("Nicole Le Douarin", GOLD)), run_time=.59)
        self.at("DNA stain")
        self.play(FadeIn(chick, shift=RIGHT*.16), run_time=.89)
        quail = embryo_cell(-2.7, -.03, True, 1.25)
        self.at("track migrating cells")
        self.play(FadeIn(quail, scale=.69), run_time=.67)
        self.at("quail nuclei show")
        compare = VGroup(embryo_cell(-1.78, .16, True, 2.07),
                         embryo_cell(1.78, .16, False, 2.07))
        self.play(FadeOut(VGroup(quail, chick)), FadeIn(compare, scale=.64), run_time=1.08)
        labels = VGroup(boxed_label("Quail nucleus", INK, size=29, fill_opacity=.06).move_to(xy(-1.78, -1.49)),
                        boxed_label("Chick nucleus", INK, size=29, fill_opacity=.06).move_to(xy(1.78, -1.49)))
        self.at("dense chromatin mass")
        self.play(FadeIn(labels[0]), run_time=.55)
        self.at("chick nuclei lack")
        self.play(FadeIn(labels[1]), run_time=.55)
        self.at("grafted quail cells")
        self.play(FadeOut(labels), run_time=.27)
        self.play(FadeOut(compare), FadeIn(chick), FadeIn(quail), run_time=.52)
        self.play(quail.animate.move_to(xy(-.80, .43)), run_time=1.39)
        self.at("without fading")
        daughter = quail.copy()
        self.add(daughter)
        self.play(quail.animate.move_to(xy(.25, -.29)).scale(.83),
                  daughter.animate.move_to(xy(.77, .69)).scale(.83), run_time=2.58)
        self.at("across every tissue")
        self.play(quail.animate.shift(RIGHT*1.52), daughter.animate.shift(RIGHT*.86 + UP*.42),
                  run_time=1.42)
        self.at("reports only what")
        self.play(FadeIn(caption("A stain reports what it binds", color=GOLD, y=-3.4)),
                  run_time=.58)
        self.finish()


class S13End(EndCard):
    LINE = "A stain reveals only its target; match it to your question."
