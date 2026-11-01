"""Molecular motors and cargo: reading one motor in an optical trap  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole video)
  BLUE   = the kinesin motor
  YELLOW = the bead it carries (and the bead's position trace)
  GREY   = the microtubule track, the glass, outlines, axes
  TEAL   = the optical trap: laser, trap centre, spring, stiffness kappa
  RED    = force (F, the restoring pull, the stall)
  GREEN  = ATP
  ORANGE = work done per step
  GOLD   = the preparation / condition a number belongs to
  PURPLE = myosin motors
  PINK   = dynein motors
  TEXT   = numbers, equations, adaptor
  GREY also marks actin and dynactin (labelled schematics)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
UP3 = np.array([0, 1, 0.0])


# ------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------
def mk_track(y, w=12.4, x=0.0):
    return RoundedRectangle(corner_radius=0.1, width=w, height=0.3, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])


def motor_blob(x, ty, h=0.9, w=0.5):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.4).move_to([x, ty + 0.15 + h / 2, 0])


def bead_circ(x, y, r=0.85):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                  fill_opacity=0.3).move_to([x, y, 0])


def rig(x, ty, r=0.85, mh=0.9):
    """a bead on top of one kinesin standing on a track whose centre line is y = ty"""
    m = motor_blob(x, ty, mh)
    b = bead_circ(x, ty + 0.15 + mh + r - 0.05, r)
    return VGroup(b, m)


def spring(p0, p1, n=8, amp=0.2, color=TEAL, w=4, rightward=False):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    if L < 0.35 or (rightward and d[0] < 0.35):
        return VGroup()
    u = d / L
    perp = np.array([-u[1], u[0], 0])
    pts = [p0, p0 + u * 0.12 * L]
    for i in range(1, 2 * n):
        pts.append(p0 + u * (0.12 * L + 0.76 * L * i / (2 * n)) + perp * amp * (1 if i % 2 else -1))
    pts += [p0 + u * 0.88 * L, p1]
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(color, w).set_fill(opacity=0)
    return m


def arr(a, b, color=GREY, w=6, tip=0.26):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def dimline(x0, x1, y, color=GREY, w=3, tick=0.14):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=w),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=w))


def vdimline(x, y0, y1, color=GREY, w=3, tick=0.14):
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=w),
                  Line([x - tick, y0, 0], [x + tick, y0, 0], color=color, stroke_width=w),
                  Line([x - tick, y1, 0], [x + tick, y1, 0], color=color, stroke_width=w))


def cone(cx, apex_y, top_y, hw=1.25):
    return Polygon([cx - hw, top_y, 0], [cx + hw, top_y, 0], [cx, apex_y, 0], stroke_width=0,
                   fill_color=TEAL, fill_opacity=0.28)


PURPLE = "#B58CD9"
PINK = "#DB83B0"


def family_motor(x, y, name, color=BLUE):
    body = motor_blob(x, y, h=0.65, w=0.65).set_color(color)
    label = T(name, 25, color).move_to([x, y + 1.25, 0])
    return VGroup(body, label)


def actin_track(y, w=10.4):
    return VGroup(*[Line([-w/2, y+d, 0], [w/2, y+d, 0],
                        color=GREY, stroke_width=4) for d in (-0.08, 0.08)])


def walker(x=-3, y=-1.5):
    # Two schematic heads, with flexible links to one cargo; no molecular geometry.
    a = motor_blob(x-0.6, y, h=0.5, w=0.55)
    b = motor_blob(x+0.6, y, h=0.5, w=0.55)
    cargo = bead_circ(x, y+2.15, r=0.65)
    links = VGroup(Line(a.get_top(), cargo.get_bottom(), color=BLUE, stroke_width=4),
                   Line(b.get_top(), cargo.get_bottom(), color=BLUE, stroke_width=4))
    return VGroup(a, b, cargo, links)


def walk_step(scene, m, moving, stride=1.2, duration=0.8, fuel=None):
    a, b, cargo, links = m
    head = m[moving]
    destination = head.get_center() + RIGHT*stride*2
    midpoint = (head.get_center()+destination)/2 + UP*0.8
    path = VMobject().set_points_smoothly([head.get_center(), midpoint, destination])
    # Follow the actual lifted head instead of interpolating two straight links.
    def follow_heads(group):
        for link, foot in zip(group, (a, b)):
            link.put_start_and_end_on(foot.get_top(), cargo.get_bottom())
    links.add_updater(follow_heads)
    anims = [MoveAlongPath(head, path), cargo.animate.shift(RIGHT*stride)]
    if fuel is not None:
        anims.append(fuel.animate.move_to(cargo.get_center()).scale(0.2).set_opacity(0))
    scene.play(*anims, run_time=duration)
    links.remove_updater(follow_heads)
    if fuel is not None:
        scene.remove(fuel)


class S00Title(TitleCard):
    LESSON = "Molecular motors and cargo"
    TITLE = "How Motors Move Cargo"


class S01Cargo(SpokenScene):
    def construct(self):
        cell = Ellipse(width=13, height=6, color=GREY, stroke_width=2).shift(DOWN*0.15)
        cargo = bead_circ(-3.4, 1.5, 0.42)
        tasks = T("cargo   •   chromosomes   •   muscle", 30).move_to([0, 3.2, 0])
        self.at("Cells carry cargo")
        self.play(Create(cell), FadeIn(cargo), FadeIn(tasks), run_time=0.6)
        self.play(cargo.animate.shift(RIGHT*2.2), run_time=0.8)
        self.at("motor proteins")
        motor = motor_blob(-1.2, -0.1)
        self.play(FadeIn(motor), run_time=0.5)
        self.at("A motor is an enzyme")
        atp = chip("ATP", GREEN, 28).move_to([-3, 0.8, 0])
        self.play(FadeIn(atp), run_time=0.5)
        self.at("into steps")
        self.play(atp.animate.move_to(motor).scale(0.2).set_opacity(0),
                  motor.animate.shift(RIGHT*1.4), cargo.animate.shift(RIGHT*1.4), run_time=0.7)
        self.at("The tracks are")
        act = actin_track(0.6, 8.6)
        mt = mk_track(-1.7, 8.6)
        labels = VGroup(T("actin", 25, GREY).move_to([-3.6, 0.1, 0]),
                        T("microtubule", 25, GREY).move_to([-3.1, -2.2, 0]))
        self.play(FadeOut(motor), FadeOut(cargo), FadeOut(tasks), FadeIn(act), FadeIn(mt), FadeIn(labels), run_time=0.7)
        self.at("each track has a direction")
        polarity = VGroup(T("−", 30, GREY).move_to([-4.7, 0.6, 0]),
                          T("+", 30, GREY).move_to([4.7, 0.6, 0]),
                          T("−", 30, GREY).move_to([-4.7, -1.7, 0]),
                          T("+", 30, GREY).move_to([4.7, -1.7, 0]))
        self.play(FadeIn(polarity), run_time=0.4)
        self.at("Myosins walk")
        myo = family_motor(0, 0.6, "myosin", PURPLE)
        self.play(FadeIn(myo), run_time=0.6)
        self.at("Kynesins and dyneins")
        kin = family_motor(-1.5, -1.7, "kinesin")
        dyn = family_motor(2.4, -1.7, "dynein", PINK)
        self.play(FadeIn(kin), FadeIn(dyn), run_time=0.6)
        self.at("So which motor")
        question = T("Which way? How do we know?", 32).move_to([0, 3.2, 0])
        self.play(FadeIn(question), run_time=0.6)
        self.finish()


class S02Direction(SpokenScene):
    def construct(self):
        act, mt = actin_track(0.8), mk_track(-1.5, 10.4)
        labels = VGroup(T("actin", 26, GREY).move_to([0, 0.25, 0]),
                        T("microtubule", 26, GREY).move_to([0, -2.05, 0]),
                        T("−", 30).move_to([-5.65, -1.5, 0]), T("+", 30).move_to([5.65, -1.5, 0]),
                        T("barbed +", 24, GREY).move_to([4.7, 0.25, 0]))
        myo = family_motor(-2.4, 0.8, "most myosins", PURPLE)
        self.at("Most myosins")
        self.play(FadeIn(act), FadeIn(mt), FadeIn(labels), FadeIn(myo), run_time=0.6)
        self.at("toward the barbed end")
        self.play(myo.animate.shift(RIGHT*3.2), run_time=1)
        self.at("moves toward the plus end")
        kin = family_motor(-2.5, -1.5, "kinesin-1")
        outward = arr([-1.8, -2.7, 0], [2, -2.7, 0], BLUE)
        outlabel = T("outward", 25, BLUE).move_to([0, -3.2, 0])
        self.play(FadeIn(kin), GrowArrow(outward), FadeIn(outlabel), run_time=0.5)
        self.play(kin.animate.shift(RIGHT*4), run_time=1)
        self.at("Cytoplasmic")
        self.play(FadeOut(kin), FadeOut(outward), FadeOut(outlabel), run_time=0.4)
        dyn = family_motor(2.5, -1.5, "cytoplasmic dynein", PINK)
        self.play(FadeIn(dyn), run_time=0.5)
        self.at("toward the minus end")
        inward = arr([2, -2.7, 0], [-1.8, -2.7, 0], PINK)
        inlabel = T("inward", 25, PINK).move_to([0, -3.2, 0])
        self.play(dyn.animate.shift(LEFT*4), GrowArrow(inward), FadeIn(inlabel), run_time=1)
        self.at("But the family")
        self.play(FadeOut(myo), FadeOut(dyn), FadeOut(inward), FadeOut(inlabel), run_time=0.5)
        self.at("Myosin 6")
        exceptions = VGroup(chip("myosin VI: exception", PURPLE, 26).move_to([-2.8, 2.8, 0]),
                            chip("ncd: exception", BLUE, 26).move_to([3.1, 2.8, 0]))
        self.play(FadeIn(exceptions[0]), run_time=0.6)
        self.at("a fly protein called")
        self.play(FadeIn(exceptions[1]), run_time=0.6)
        self.at("Direction has to be measured")
        rule = T("Measure each motor’s direction", 32).move_to([0, -3, 0])
        self.play(FadeIn(rule), run_time=0.6)
        self.finish()


class S03Step(SpokenScene):
    def construct(self):
        track = mk_track(-1.5)
        m = walker()
        title = T("One kinesin-1", 34, BLUE).move_to([0, 3.1, 0])
        self.at("How does one motor move")
        self.play(FadeIn(track), FadeIn(m), FadeIn(title), run_time=0.7)
        self.at("two heads that alternate")
        self.play(Indicate(VGroup(m[0], m[1]), scale_factor=1.15), run_time=0.6)
        self.at("hand over hand")
        walk_step(self, m, 0)
        self.at("One head holds on")
        self.play(Indicate(m[0], scale_factor=1.15), run_time=0.5)
        self.at("the other moves")
        walk_step(self, m, 1)
        self.at("processive")
        processive = T("processive: stays on the track", 28, BLUE).move_to([0, 2.15, 0])
        self.play(FadeIn(processive), run_time=0.5)
        self.at("many steps without letting go")
        walk_step(self, m, 0)
        self.at("The cargo advances")
        x = m[2].get_center()[0]
        measure = VGroup(dimline(x, x+1.2, -2.4), M("8 nm / cargo step", 28).move_to([x+0.6, -3, 0]))
        self.play(FadeIn(measure), run_time=0.5)
        walk_step(self, m, 1)
        self.at("each step costs")
        self.play(FadeOut(measure), FadeOut(processive), run_time=0.3)
        fuel = chip("1 ATP", GREEN, 28).move_to([m[2].get_x()-1.2, 1.6, 0])
        low = T("1 ATP / step • low load", 30, GREEN).move_to([0, 2.2, 0])
        self.play(FadeIn(fuel), FadeIn(low), run_time=0.5)
        walk_step(self, m, 0, fuel=fuel)
        self.at("These numbers come from", lead=0.6)
        prep = chip("purified proteins • in vitro", GOLD, 28).move_to([0, -3, 0])
        self.play(FadeIn(prep), run_time=0.3)
        self.finish()


class S04Trap(SpokenScene):
    def construct(self):
        ty, cx = -1.8, -4.1
        track = mk_track(ty)
        motion = rig(cx, ty, r=0.7, mh=0.85)
        by = motion[0].get_y()
        self.at("To watch one motor step")
        self.play(FadeIn(track), FadeIn(motion), run_time=0.6)
        self.at("an optical trap")
        cn = cone(cx, by, 3.2)
        centre = DashedLine([cx, by, 0], [cx, ty-0.4, 0], color=TEAL)
        centrelabel = T("trap centre", 24, TEAL).move_to([cx, -2.7, 0])
        self.play(FadeIn(cn), Create(centre), FadeIn(centrelabel), run_time=0.6)
        self.bring_to_front(motion)
        self.at("A focused laser")
        laser = T("focused laser", 26, TEAL).move_to([-1.8, 2.8, 0])
        self.play(FadeIn(laser), run_time=0.5)
        sp = always_redraw(lambda: spring([cx, by, 0], [motion[0].get_x()-0.7, by, 0], rightward=True))
        force = always_redraw(lambda: arr([motion[0].get_x(), 1.4, 0],
            [motion[0].get_x()-max(0.05, (motion[0].get_x()-cx)*0.5), 1.4, 0], RED))
        self.at("a bead pulled off center")
        self.add(sp)
        self.play(motion.animate.shift(RIGHT*1.6), run_time=0.8)
        self.at("feels a force")
        self.add(force)
        self.play(FadeIn(force), run_time=0.5)
        self.at("a weight on a spring")
        self.play(Indicate(sp, color=TEAL), run_time=0.6)
        self.at("The force is the stiffness")
        eq = VGroup(M("F = κ × x", 40), T("force magnitude", 24, RED),
                    T("stiffness × distance", 25)).arrange(DOWN, buff=0.3).move_to([3.3, 1.8, 0])
        self.play(FadeIn(eq), run_time=0.7)
        self.at("beads advanced in")
        steps = M("8 nm steps", 28).move_to([3.3, -0.4, 0])
        self.play(FadeIn(steps), run_time=0.4)
        for _ in range(3):
            self.play(motion.animate.shift(RIGHT*0.45), run_time=0.3)
            self.wait(0.2)
        self.at("against loads up to")
        measured = T("measured: 5–6 pN", 28, RED).move_to([3.3, -1.15, 0])
        self.play(FadeIn(measured), run_time=0.6)
        self.at("With made")
        example = chip("made-up example", GOLD, 27).move_to([3.3, 3.1, 0])
        self.play(FadeOut(eq), FadeOut(steps), FadeOut(measured), FadeOut(laser), FadeIn(example), run_time=0.6)
        self.at("a stiffness of")
        stiffness = M("κ = 0.05 pN/nm", 28, TEAL).move_to([3.3, 2, 0])
        self.play(FadeIn(stiffness), run_time=0.6)
        self.at("a stall at")
        self.play(motion.animate.shift(RIGHT*0.85), run_time=0.5)
        endx = motion[0].get_x()
        dist = VGroup(dimline(cx, endx, -2.3), M("120 nm", 28).move_to([(cx+endx)/2, -3, 0]))
        self.play(FadeIn(dist), run_time=0.5)
        self.at("give 6")
        result = M("F = 0.05 × 120", 28).move_to([3.3, 0.9, 0])
        answer = M("= 6 pN", 42, RED).move_to([3.3, 0, 0])
        self.play(FadeIn(result), FadeIn(answer), run_time=0.6)
        self.finish()


class S05Teams(SpokenScene):
    def construct(self):
        track = mk_track(-1.8)
        dyn = family_motor(-0.6, -1.8, "human dynein", PINK)
        self.at("Motors rarely work alone")
        self.play(FadeIn(track), FadeIn(dyn), run_time=0.6)
        self.at("In reconstitution experiments")
        prep = chip("reconstitution • purified proteins", GOLD, 27).move_to([0, 3.15, 0])
        self.play(FadeIn(prep), run_time=0.6)
        self.at("when it binds")
        dc = chip("dynactin", GREY, 27).move_to([2.7, 0.25, 0])
        adaptor = chip("activating adaptor", TEXT, 26).move_to([2.7, 1.3, 0])
        self.play(FadeIn(dc), FadeIn(adaptor), run_time=0.6)
        self.play(dc.animate.move_to([-0.6, 0.25, 0]), adaptor.animate.move_to([-0.6, 1.3, 0]), run_time=0.7)
        self.at("also binds cargo")
        vesicle = bead_circ(-0.6, 2.25, 0.5)
        cargo_label = T("cargo", 25, YELLOW).move_to([-2.3, 2.25, 0])
        self.play(FadeIn(vesicle), FadeIn(cargo_label), run_time=0.5)
        self.at("Some adapters recruit")
        second = family_motor(1.5, -1.8, "dynein", PINK)
        self.play(FadeIn(second), dc[0].animate.stretch_to_fit_width(4), run_time=0.6)
        self.at("more force")
        pull = VGroup(arr([1, -2.7, 0], [-2.3, -2.7, 0], RED),
                      T("more force", 27, RED).move_to([0, -3.25, 0]))
        self.play(FadeIn(pull), run_time=0.6)
        self.at("In muscle")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        # Each thin filament and the thick filament retain their lengths.
        left = VGroup(Line([-5, -1.8, 0], [-5, 1.5, 0], color=GREY, stroke_width=5),
                      Line([-5, 0.7, 0], [-0.8, 0.7, 0], color=GREY, stroke_width=6))
        right = VGroup(Line([5, -1.8, 0], [5, 1.5, 0], color=GREY, stroke_width=5),
                       Line([0.8, -1.3, 0], [5, -1.3, 0], color=GREY, stroke_width=6))
        thick = mk_track(-0.3, 5.5).set_color(PURPLE)
        heads = VGroup(Line([-1.9, -0.15, 0], [-2.5, 0.7, 0], color=PURPLE, stroke_width=6),
                       Line([1.9, -0.45, 0], [2.5, -1.3, 0], color=PURPLE, stroke_width=6))
        labels = VGroup(T("thin filaments", 27, GREY).move_to([0, 1.8, 0]),
                        T("thick filament", 27, PURPLE).move_to([0, -2, 0]),
                        T("muscle: many myosin heads", 32, PURPLE).move_to([0, 3.1, 0]))
        self.play(FadeIn(left), FadeIn(right), FadeIn(thick), FadeIn(heads), FadeIn(labels), run_time=0.6)
        self.at("each pole once")
        bent = VGroup(Line([-1.9, -0.15, 0], [-1.9, 0.7, 0], color=PURPLE, stroke_width=6),
                      Line([1.9, -0.45, 0], [1.9, -1.3, 0], color=PURPLE, stroke_width=6))
        self.play(Transform(heads, bent), left.animate.shift(RIGHT*0.6), right.animate.shift(LEFT*0.6), run_time=0.5)
        self.at("and let go")
        self.play(FadeOut(heads), run_time=0.4)
        self.at("thin filaments slide past")
        self.play(left.animate.shift(RIGHT*0.8), right.animate.shift(LEFT*0.8), run_time=1)
        self.at("no filament gets shorter")
        fixed = VGroup(dimline(-2.75, 2.75, -2.65, PURPLE),
                       T("filament lengths stay constant", 28).move_to([0, -3.25, 0]))
        self.play(FadeIn(fixed), run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        track = mk_track(-2, 10.4)
        m = walker(-3, -2)
        polarity = VGroup(T("−", 30, GREY).move_to([-5.6, -2, 0]),
                          T("+", 30, GREY).move_to([5.6, -2, 0]))
        self.at("Keep three things")
        self.play(FadeIn(track), FadeIn(m), FadeIn(polarity), run_time=0.6)
        self.at("Motors turn")
        line1 = T("ATP → steps along polar tracks", 32, GREEN).move_to([0, 3.5, 0])
        self.play(FadeIn(line1), run_time=0.5)
        fuel = chip("ATP", GREEN, 26).move_to([-4, 0.7, 0])
        self.play(FadeIn(fuel), run_time=0.3)
        walk_step(self, m, 0, fuel=fuel)
        self.at("The family gives the track")
        line2 = T("Family gives track; measure direction", 30, BLUE).move_to([0, 2.45, 0])
        self.play(FadeIn(line2), run_time=0.6)
        self.at("every number belongs")
        line3 = T("Numbers belong to their preparation", 30, GOLD).move_to([0, 1.4, 0])
        self.play(FadeIn(line3), run_time=0.6)
        self.at("One motor")
        prep = T("one motor", 28, GOLD).move_to([-3.4, -3.15, 0])
        self.play(FadeIn(prep), run_time=0.4)
        self.at("in vitro")
        vitro = T("in vitro", 28, GOLD).move_to([-0.4, -3.15, 0])
        self.play(FadeIn(vitro), run_time=0.4)
        self.at("loading condition")
        load = T("measured load", 28, GOLD).move_to([3.2, -3.15, 0])
        self.play(FadeIn(load), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Motors turn ATP into steps; each motor's direction must be measured."
