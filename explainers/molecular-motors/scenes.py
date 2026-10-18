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
  TEXT   = numbers and equations
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


class S00Title(TitleCard):
    LESSON = "Molecular motors and cargo"
    TITLE = "Reading one motor in a trap"


# ------------------------------------------------------------------------------------------
class S01Jumps(SpokenScene):
    """a bead on one kinesin jumps 8 nm at a time, one ATP per jump; how do you watch it?"""

    def construct(self):
        TY, STEP, X0 = -1.0, 1.4, -4.2
        track = mk_track(TY)
        motion = rig(X0, TY)
        bead, motor = motion[0], motion[1]
        l_bead = T("bead", 26, YELLOW).move_to([X0 - 1.7, TY + 2.1, 0])
        l_kin = T("kinesin", 26, BLUE).move_to([X0 - 1.5, TY + 0.7, 0])
        l_mt = T("microtubule", 26, GREY).move_to([3.0, TY - 0.6, 0])
        l_plus = T("plus end", 24, GREY).move_to([5.4, TY - 1.1, 0])

        self.at("One kinesin molecule")
        self.play(FadeIn(track), FadeIn(motion, shift=DOWN * 0.2), FadeIn(l_bead), FadeIn(l_kin), FadeIn(l_mt), FadeIn(l_plus),
                  run_time=0.8)

        # --- jumps of 8 nm ---------------------------------------------------------------------
        self.at("moves in jumps")
        self.play(FadeOut(l_bead), FadeOut(l_kin), motion.animate.shift(RIGHT * STEP), run_time=0.4)
        br = dimline(X0, X0 + STEP, TY - 0.7, GREY)
        br_lbl = M("8 nm", 28).move_to([X0 + STEP / 2, TY - 1.3, 0])
        self.at("of 8 nanometers")
        self.play(Create(br), FadeIn(br_lbl), motion.animate.shift(RIGHT * STEP), run_time=0.5)

        # --- one ATP per jump ----------------------------------------------------------------------
        self.at("each jump costs")
        tag = T("at low load: one jump, one ATP", 30, GREEN).move_to([0, 2.55, 0])
        for k in range(2):
            atp = chip("ATP", GREEN, size=26).move_to([motion[1].get_center()[0] - 1.5, TY + 0.7, 0])
            self.play(FadeIn(atp, shift=RIGHT * 0.2), run_time=0.3)
            if k == 0:
                self.play(FadeIn(tag), run_time=0.3)
            self.play(atp.animate.move_to(motion[1].get_center()).scale(0.4).set_opacity(0),
                      motion.animate.shift(RIGHT * STEP), run_time=0.45)
            self.wait(0.2)

        # --- the preparation -----------------------------------------------------------------------
        self.at("These numbers come")
        prep = chip("purified proteins, in vitro", GOLD, size=28).move_to([0, 3.15, 0])
        self.play(FadeIn(prep, shift=DOWN * 0.15), run_time=0.5)

        # --- the question --------------------------------------------------------------------------
        self.at("how do you watch")
        q = T("?", 170, TEXT, weight=BOLD).move_to([4.7, TY + 2.2, 0])
        self.play(FadeIn(q, scale=0.4), Indicate(motion[0], color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S02Trap(SpokenScene):
    """gliding assay (many motors) -> optical trap holds one bead -> pull off centre -> F = kappa x"""

    def construct(self):
        # --- part A: gliding assay -----------------------------------------------------------------
        GY = -1.1
        glass = mk_track(GY)
        motors = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.35, height=1.4, stroke_color=BLUE,
                                           stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
                          .move_to([-5.2 + 1.3 * k, GY + 0.15 + 0.7, 0]) for k in range(9)])
        fil = VGroup(*[Circle(radius=0.17, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.8)
                       .move_to([-3.4 + 0.4 * i, GY + 1.72, 0]) for i in range(18)])
        l_glass = T("coverslip", 26, GREY).move_to([-5.0, GY - 0.6, 0])
        l_mot = T("many motors", 30, BLUE).move_to([0.5, GY - 0.65, 0])
        l_fil = T("filament", 26, GREY).move_to([0.0, GY + 2.6, 0])
        partA = VGroup(glass, motors, fil, l_glass, l_mot, l_fil)

        self.at("gliding assay")
        self.play(FadeIn(glass), FadeIn(motors), FadeIn(l_glass), FadeIn(fil), run_time=0.7)
        self.play(FadeIn(l_mot), FadeIn(l_fil), run_time=0.4)
        glide = max(0.4, self.t_of("To see one") - 0.25 - self.elapsed())
        self.play(fil.animate.shift(RIGHT * 2.0), l_fil.animate.shift(RIGHT * 2.0), run_time=glide, rate_func=linear)

        # --- part B: the trap -----------------------------------------------------------------------
        TY, CX, BY = -2.1, -3.2, 0.0
        self.at("an optical trap")
        self.play(FadeOut(partA), run_time=0.4)
        track = mk_track(TY)
        motion = rig(CX, TY, r=0.9, mh=1.0)
        by = motion[0].get_center()[1]
        self.play(FadeIn(track), FadeIn(motion, shift=DOWN * 0.2), run_time=0.7)

        self.at("focused laser")
        cn = cone(CX, by, 3.4)
        l_laser = T("laser", 28, TEAL).move_to([CX + 1.9, 3.0, 0])
        dot = Dot([CX, by, 0], radius=0.1, color=TEAL)
        self.add(cn)
        self.bring_to_front(motion)
        self.play(FadeIn(cn, shift=DOWN * 0.3), FadeIn(l_laser), FadeIn(dot), run_time=0.7)
        self.at("near its center")
        cl = DashedLine([CX, by, 0], [CX, TY + 0.2, 0], color=TEAL, stroke_width=3)
        l_tc = T("trap centre", 24, TEAL).move_to([CX, TY - 0.7, 0])
        self.play(Create(cl), FadeIn(l_tc), run_time=0.6)

        # --- pull off centre -------------------------------------------------------------------------
        sp = always_redraw(lambda: spring([CX, by, 0], [motion[0].get_center()[0] - 0.9, by, 0], rightward=True))
        fa = always_redraw(lambda: (arr([motion[0].get_center()[0], 1.2, 0],
                                        [motion[0].get_center()[0] - min(0.5 * (motion[0].get_center()[0] - CX), 2.1), 1.2, 0], RED)
                                    if motion[0].get_center()[0] - CX > 0.5 else VGroup()))
        self.add(sp, fa)
        self.bring_to_front(motion)
        self.at("Pull the bead off")
        self.play(motion.animate.shift(RIGHT * 2.4), run_time=1.0)
        l_F = T("F", 34, RED, weight=BOLD).move_to([motion[0].get_center()[0] - 1.1, 1.65, 0])
        xb = dimline(CX, CX + 2.4, 2.15, GREY)
        l_x = M("x", 30).move_to([CX + 1.2, 2.55, 0])
        self.at("pulls it back")
        self.play(FadeIn(l_F), Create(xb), FadeIn(l_x), run_time=0.6)
        self.at("weight on a spring")
        self.play(Indicate(sp, color=TEAL, scale_factor=1.12), run_time=0.8)

        # --- the equation ----------------------------------------------------------------------------
        self.at("The force is the")
        eq = M("F = −κx", 54, t2c={"F": RED, "κ": TEAL}).move_to([4.5, 1.9, 0])
        self.play(Write(eq), run_time=0.8)
        k_l = VGroup(M("κ", 30, TEAL), T("trap stiffness", 26, TEAL)).arrange(RIGHT, buff=0.3).move_to([4.5, 0.75, 0])
        x_l = VGroup(M("x", 30), T("distance from the centre", 26)).arrange(RIGHT, buff=0.3).move_to([4.5, -0.1, 0])
        k_l.align_to([1.5, 0, 0], LEFT)
        x_l.align_to([1.5, 0, 0], LEFT)
        self.at("stiffness")
        self.play(FadeIn(k_l, shift=RIGHT * 0.2), run_time=0.4)
        self.at("distance from the center")
        self.play(FadeIn(x_l, shift=RIGHT * 0.2), Indicate(xb, color=YELLOW), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
class S03Rate(SpokenScene):
    """position-time staircase: 400 nm in 0.5 s -> 800 nm/s -> 100 steps/s -> ~100 ATP/s"""

    def construct(self):
        O = np.array([-5.4, -2.5, 0])
        SX, SY = 12.4, 0.013            # units per second, units per nm
        X1, Y1 = 0.5 * SX, 400 * SY
        ax = VGroup(Line(O, O + RIGHT * (X1 + 0.3), color=GREY, stroke_width=3),
                    Line(O, O + UP * (Y1 + 0.2), color=GREY, stroke_width=3))
        ticks = VGroup()
        for t in (0, 0.25, 0.5):
            ticks.add(M(str(t), 22, GREY).move_to(O + RIGHT * t * SX + DOWN * 0.35))
        for y in (0, 200, 400):
            ticks.add(M(str(y), 22, GREY).move_to(O + UP * y * SY + LEFT * 0.5))
        xl = T("time (s)", 24, GREY).move_to(O + RIGHT * 3.2 + DOWN * 0.88)
        yl = T("position (nm)", 24, GREY).rotate(PI / 2).move_to(O + UP * 2.7 + LEFT * 1.25)
        axes = VGroup(ax, ticks, xl, yl)

        self.at("worked problem")
        self.play(FadeIn(axes), run_time=0.7)
        self.at("made up data")
        made = chip("made-up data", GOLD, size=26).move_to([4.5, 3.15, 0])
        self.play(FadeIn(made, shift=DOWN * 0.15), run_time=0.4)

        # staircase of 50 steps
        pts = [O]
        for i in range(50):
            x0, x1 = (i * 0.01) * SX, ((i + 1) * 0.01) * SX
            pts.append(O + np.array([x1, i * 8 * SY, 0]))
            pts.append(O + np.array([x1, (i + 1) * 8 * SY, 0]))
        stair = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4).set_fill(opacity=0)
        self.at("At low load")
        self.play(Create(stair, rate_func=linear), run_time=max(1.5, self.t_of("half a second") - 0.3 - self.elapsed()))
        end = O + np.array([X1, Y1, 0])
        d1 = DashedLine(end, [end[0], O[1], 0], color=GREY, stroke_width=2)
        d2 = DashedLine(end, [O[0], end[1], 0], color=GREY, stroke_width=2)
        dot = Dot(end, radius=0.1, color=YELLOW)
        L1 = M("400 / 0.5 = 800 nm/s", 27).move_to([4.2, 2.25, 0]).align_to([1.4, 0, 0], LEFT)
        self.at("half a second")
        self.play(Create(d1), Create(d2), FadeIn(dot), run_time=0.5)
        self.at("That is")
        self.play(Write(L1), run_time=0.8)

        # one step, magnified
        bx, by = 2.2, -2.9
        sw, sh = 0.7, 0.45
        pp = [[bx, by, 0], [bx + sw, by, 0], [bx + sw, by + sh, 0], [bx + 2 * sw, by + sh, 0],
              [bx + 2 * sw, by + 2 * sh, 0], [bx + 3 * sw, by + 2 * sh, 0]]
        st = VMobject().set_points_as_corners(pp).set_stroke(YELLOW, 5).set_fill(opacity=0)
        sb = vdimline(bx + 3 * sw + 0.2, by + sh, by + 2 * sh, GREY)
        sl = M("8 nm", 26).next_to(sb, RIGHT, buff=0.12)
        box = RoundedRectangle(corner_radius=0.1, width=3.7, height=1.75, stroke_color=GREY, stroke_width=2,
                               fill_opacity=0).move_to([bx + 1.65, by + 0.78, 0])
        L2 = M("800 / 8 = 100 steps/s", 27).move_to([4.2, 1.35, 0]).align_to([1.4, 0, 0], LEFT)
        self.at("Divide by")
        self.play(FadeIn(box), Create(st), Create(sb), FadeIn(sl), Write(L2), run_time=1.0)

        self.at("Near zero load")
        L3 = T("one ATP per step", 32, GREEN).move_to([4.2, 0.4, 0])
        L3.align_to(L2, LEFT)
        self.play(FadeIn(L3, shift=RIGHT * 0.2), run_time=0.5)
        self.at("burns about")
        L4 = M("≈ 100 ATP/s", 44, GREEN).move_to([4.2, -0.65, 0])
        L4.align_to(L2, LEFT)
        self.play(Write(L4), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S04Stall(SpokenScene):
    """the bead walks away from the trap centre in 8 nm steps until it stalls 120 nm out: F = kappa x = 6 pN"""

    def construct(self):
        TY, CX, R = -1.9, -5.4, 0.85
        U = 0.05                      # units per nm
        track = mk_track(TY, w=13.0, x=0.0)
        motion = rig(CX, TY, r=R, mh=0.9)
        by = motion[0].get_center()[1]
        cn = cone(CX, by, 2.5, hw=1.1)
        dot = Dot([CX, by, 0], radius=0.1, color=TEAL)
        cl = DashedLine([CX, by, 0], [CX, TY + 0.2, 0], color=TEAL, stroke_width=3)
        self.add(cn)
        self.play(FadeIn(track), FadeIn(motion), FadeIn(dot), Create(cl), run_time=0.8)
        self.bring_to_front(motion)

        sp = always_redraw(lambda: spring([CX, by, 0], [motion[0].get_center()[0] - R, by, 0], rightward=True))
        fa = always_redraw(lambda: (arr([motion[0].get_center()[0], 1.25, 0],
                                        [motion[0].get_center()[0] - min(0.35 * (motion[0].get_center()[0] - CX), 2.1), 1.25, 0], RED)
                                    if motion[0].get_center()[0] - CX > 0.5 else VGroup()))
        self.add(sp, fa)
        self.bring_to_front(motion)

        e1 = M("κ = 0.05 pN/nm", 28, t2c={"κ": TEAL}).move_to([4.4, 3.2, 0]).align_to([1.4, 0, 0], LEFT)
        t_start = self.t_of("pull against") - 0.2
        t_stall = self.t_of("walks until it stalls") + 0.2
        t_e1 = self.t_of("stiffness is") - 0.2
        self.at("pull against")
        dt = (t_stall - self.elapsed() - 0.15) / 15
        shown = False
        for i in range(15):
            anims = [motion.animate.shift(RIGHT * 8 * U)]
            if not shown and self.elapsed() >= t_e1:
                anims.append(Write(e1))
                shown = True
            self.play(*anims, run_time=min(0.3, dt * 0.7))
            self.wait(max(0.02, dt - min(0.3, dt * 0.7)))
        if not shown:
            self.play(Write(e1), run_time=0.5)
        bx = motion[0].get_center()[0]
        brk = dimline(CX, bx, TY - 0.7, GREY)
        l120 = M("120 nm", 30).move_to([(CX + bx) / 2, TY - 1.3, 0])
        l_F = T("F", 34, RED, weight=BOLD).move_to([bx - 1.0, 1.7, 0])
        self.at("from the center")
        self.play(Create(brk), FadeIn(l120), FadeIn(l_F), run_time=0.6)
        e2 = M("x = 120 nm", 28).move_to([4.4, 2.6, 0])
        e2.align_to(e1, LEFT)
        self.play(FadeIn(e2), run_time=0.4)

        self.at("Force is stiffness")
        e3 = M("F = 0.05 × 120 = 6 pN", 28, t2c={"F": RED}).move_to([4.1, 1.85, 0]).align_to(e1, LEFT)
        self.play(Write(e3), Indicate(motion, color=YELLOW, scale_factor=1.06), run_time=1.0)

        # the measured range 5 to 6 pN
        ax0, ps = 2.8, 0.55
        axis = Line([ax0, 0.45, 0], [ax0 + 7 * ps, 0.45, 0], color=GREY, stroke_width=3)
        tks = VGroup(*[Line([ax0 + k * ps, 0.45, 0], [ax0 + k * ps, 0.58, 0], color=GREY, stroke_width=3) for k in range(8)])
        nums = VGroup(*[M(str(k), 22, GREY).move_to([ax0 + k * ps, 0.12, 0]) for k in (0, 5, 6)])
        unit = M("pN", 22, GREY).move_to([ax0 + 7 * ps + 0.05, 0.12, 0])
        band = Rectangle(width=ps, height=0.34, stroke_width=0, fill_color=RED, fill_opacity=0.55).move_to(
            [ax0 + 5.5 * ps, 0.62, 0])
        cap = T("measured: 5 to 6 pN", 24, GREY).move_to([ax0 + 2.2, 1.12, 0])
        self.at("top of the range")
        self.play(FadeIn(axis), FadeIn(tks), FadeIn(nums), FadeIn(unit), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(band), Indicate(nums[2], color=RED), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------
class S05Work(SpokenScene):
    """6 pN x 8 nm = 48 pN nm, against 83 pN nm from one ATP: about 58 percent"""

    def construct(self):
        RX, RY = -4.3, 0.1               # rectangle centre
        rw, rh = 2.0, 3.0
        rect = Rectangle(width=rw, height=rh, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                         fill_opacity=0.28).move_to([RX, RY, 0])
        l6 = M("6 pN", 30, RED).move_to([RX - rw / 2 - 0.85, RY, 0])
        l8 = M("8 nm", 30).move_to([RX, RY - rh / 2 - 0.4, 0])
        w48 = VGroup(M("48", 52, ORANGE), M("pN·nm", 26, ORANGE)).arrange(DOWN, buff=0.1).move_to(rect)
        self.at("Work per step")
        self.play(Create(rect), run_time=0.8)
        self.at("force times distance")
        self.play(FadeIn(l6), FadeIn(l8), run_time=0.6)
        self.at("is 48")
        self.play(FadeIn(w48, scale=0.8), run_time=0.6)

        s = 0.075
        X0 = -1.9
        t_atp = T("ATP: about 50 kJ per mole", 28, GREEN).move_to([X0 + 3.6, 2.35, 0])
        t_atp.align_to([X0, 0, 0], LEFT)
        b_atp = Rectangle(width=83 * s, height=0.7, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                          fill_opacity=0.3).move_to([X0 + 83 * s / 2, 1.6, 0])
        v_atp = M("83 pN·nm", 28, GREEN).next_to(b_atp, RIGHT, buff=0.15)
        v_mol = T("for each molecule", 22, GREEN).move_to([X0 + 83 * s + 1.2, 1.12, 0])
        hedge = T("the true value depends on ATP, ADP and phosphate levels", 22, GREY).move_to([X0 + 3.9, 0.55, 0])
        hedge.align_to([X0, 0, 0], LEFT)
        self.at("Assume that one mole")
        self.play(FadeIn(t_atp), run_time=0.4)
        self.play(GrowFromEdge(b_atp, LEFT), run_time=0.8)
        self.at("each molecule")
        self.play(FadeIn(v_atp), FadeIn(v_mol), run_time=0.4)
        self.at("true value depends")
        self.play(FadeIn(hedge), run_time=0.5)

        t_w = T("work per step", 28, ORANGE).move_to([X0 + 1.0, -0.15, 0])
        t_w.align_to([X0, 0, 0], LEFT)
        b_w = Rectangle(width=48 * s, height=0.7, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                        fill_opacity=0.35).move_to([X0 + 48 * s / 2, -0.85, 0])
        v_w = M("48 pN·nm", 28, ORANGE).next_to(b_w, RIGHT, buff=0.15)
        res = M("48 / 83 ≈ 58%", 52).move_to([X0 + 3.2, -2.45, 0])
        self.at("At stall")
        self.play(FadeIn(t_w), GrowFromEdge(b_w, LEFT), run_time=0.8)
        self.play(FadeIn(v_w), run_time=0.3)
        self.at("about 58")
        self.play(Write(res), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------
class S06Caution(SpokenScene):
    """stiff link vs floppy tether; then two myosin numbers from two loading conditions must not be multiplied"""

    def lane(self, cx, floppy):
        TY, D = -1.3, 1.5
        x0 = cx - 1.9
        track = mk_track(TY, w=6.0, x=cx)
        mh, r = 0.8, 0.7
        motor = motor_blob(x0, TY, mh, 0.45)
        top = TY + 0.15 + mh
        bead = bead_circ(x0, top + 1.0 + r, r)
        link = Line([x0, top, 0], [x0, top + 1.0, 0], color=GREY, stroke_width=8)
        title = T("floppy tether" if floppy else "stiff link", 32).move_to([cx, 3.1, 0])
        return dict(TY=TY, D=D, x0=x0, track=track, motor=motor, bead=bead, link=link, title=title,
                    top=top, r=r)

    def construct(self):
        A = self.lane(-3.3, False)
        B = self.lane(3.3, True)
        for L in (A, B):
            L["grp"] = VGroup(L["track"], L["motor"], L["link"], L["bead"], L["title"])
        self.at("Two cautions")
        self.play(FadeIn(A["grp"]), FadeIn(B["grp"]), run_time=0.8)

        def brackets(L, bead_frac):
            x0, D, TY = L["x0"], L["D"], L["TY"]
            b1 = dimline(x0, x0 + D, TY - 0.75, BLUE)
            t1 = T("motor", 24, BLUE).next_to(b1, RIGHT, buff=0.15)
            b2 = dimline(x0, x0 + D * bead_frac, TY - 1.45, YELLOW)
            t2 = T("bead", 24, YELLOW).next_to(b2, RIGHT, buff=0.15)
            return VGroup(b1, t1, b2, t2)

        # stiff: bead keeps up with the motor
        self.at("bead moves as far")
        brA = brackets(A, 1.0)
        self.play(A["motor"].animate.shift(RIGHT * A["D"]), A["bead"].animate.shift(RIGHT * A["D"]),
                  A["link"].animate.shift(RIGHT * A["D"]), FadeIn(brA), run_time=0.9)

        # floppy: the link stretches and the bead lags
        self.at("A floppy tether")
        x0, D, top, r = B["x0"], B["D"], B["top"], B["r"]
        lag = 0.5
        new_link = spring([x0 + D, top, 0], [x0 + D * lag, top + 1.0, 0], n=4, amp=0.12, color=GREY, w=3)
        brB = brackets(B, lag)
        self.play(B["motor"].animate.shift(RIGHT * D), B["bead"].animate.shift(RIGHT * D * lag),
                  ReplacementTransform(B["link"], new_link), FadeIn(brB), run_time=0.9)
        self.at("underreports")
        self.play(Indicate(brB[2:], color=YELLOW, scale_factor=1.1), run_time=0.8)

        # --- two numbers, two conditions -------------------------------------------------------------
        self.at("never combine")
        ph1 = RoundedRectangle(corner_radius=0.14, width=4.0, height=1.2, stroke_color=GREY, stroke_width=2.5,
                               fill_opacity=0).move_to([-3.6, 1.2, 0])
        ph2 = ph1.copy().move_to([3.6, 1.2, 0])
        pt1 = T("one experiment", 28, GREY).move_to(ph1)
        pt2 = T("another experiment", 28, GREY).move_to(ph2)
        self.play(FadeOut(VGroup(A["grp"], B["grp"], brA, brB, new_link)), run_time=0.5)
        self.play(FadeIn(ph1), FadeIn(ph2), FadeIn(pt1), FadeIn(pt2), run_time=0.5)
        head = T("one muscle myosin, two experiments", 30, GREY).move_to([0, 3.1, 0])
        n1 = chip("about 11 nm", TEXT, size=44, pad=0.35).move_to([-3.6, 1.2, 0])
        n2 = chip("3 to 4 pN", RED, size=44, pad=0.35).move_to([3.6, 1.2, 0])
        g1 = chip("low load", GOLD, size=32).move_to([-3.6, -1.3, 0])
        g2 = chip("held still", GOLD, size=32).move_to([3.6, -1.3, 0])
        cross = VGroup(Line([-0.5, 0.7, 0], [0.5, 1.7, 0], color=RED, stroke_width=10),
                       Line([-0.5, 1.7, 0], [0.5, 0.7, 0], color=RED, stroke_width=10))
        nolbl = T("never combine", 28, RED).move_to([0, 0.1, 0])
        self.play(FadeIn(head), run_time=0.4)
        self.at("One muscle myosin")
        self.play(FadeOut(ph1), FadeOut(pt1), FadeIn(n1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Held still")
        self.play(FadeOut(ph2), FadeOut(pt2), FadeIn(n2, shift=LEFT * 0.2), run_time=0.5)
        self.at("two loading conditions")
        self.play(Create(cross), FadeIn(nolbl), run_time=0.6)
        self.play(FadeIn(g1, shift=UP * 0.2), FadeIn(g2, shift=UP * 0.2), run_time=0.6)
        k1 = Line(n1.get_bottom(), g1.get_top(), color=GOLD, stroke_width=5)
        k2 = Line(n2.get_bottom(), g2.get_top(), color=GOLD, stroke_width=5)
        self.at("Keep every number")
        self.play(FadeOut(cross), FadeOut(nolbl), Create(k1), Create(k2), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Keep every number tied to the preparation that measured it."
