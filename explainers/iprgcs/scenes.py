"""ipRGCs: light for the clock and the pupil  (Biochemistrypedia sensory explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Rebuilt 2026-10-31 so the film leads with the clock and the pupil (the field's main finding) and
treats pattern vision as a short side note at the end.

COLOR MAP (one color per concept, whole video)
  YELLOW = light, the clock and pupil outputs, and the open question mark
  BLUE   = rod and cone signals and their relay through bipolar cells
  GREEN  = the ipRGC and its own melanopsin response
  PURPLE = brain targets (brain, SCN, olivary pretectal nucleus, mood, learning)
  RED    = removed or lost (crossed out)
  GREY   = outlines, de-emphasized
  TEXT   = result labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell(cx, cy, w, h, color, fill=0.22, dashed=False):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill)
    if dashed:
        e = DashedVMobject(e, num_dashes=24)
        e.set_fill(color, fill)
    return e.move_to([cx, cy, 0])


def cross(center, s=0.35, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def light_arrow(x, ytop, ybot):
    return arr([x, ytop, 0], [x, ybot, 0], YELLOW, w=6)


def clock_icon(cx, cy, r=0.55):
    """A clock: ring and two hands. .h2 is the hand that turns; .c is the centre."""
    c = np.array([cx, cy, 0.0])
    ring = Circle(radius=r, stroke_color=YELLOW, stroke_width=4).move_to(c)
    h1 = Line(c, c + [0, r * 0.7, 0], color=YELLOW, stroke_width=4)
    h2 = Line(c, c + [r * 0.62 * np.cos(PI / 6), r * 0.62 * np.sin(PI / 6), 0], color=YELLOW, stroke_width=4)
    g = VGroup(ring, h1, h2)
    g.h2, g.c, g.r = h2, c, r
    return g


def dim_anims(g, o=0.3):
    """Animations that fade a flat group toward opacity o without turning its fill on."""
    return [m.animate.set_stroke(opacity=o).set_fill(opacity=m.get_fill_opacity() * o) for m in g.submobjects]


def dim_static(g, o=0.3):
    for m in g.submobjects:
        m.set_stroke(opacity=o)
        m.set_fill(opacity=m.get_fill_opacity() * o)
    return g


def eye_icon(cx, cy, w=1.5):
    """A pupil icon: eye outline, iris, dark pupil. .pup is the pupil."""
    c = [cx, cy, 0]
    eye = Ellipse(width=w, height=w * 0.57, stroke_color=YELLOW, stroke_width=4).move_to(c)
    iris = Circle(radius=w * 0.24, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to(c)
    pup = Circle(radius=w * 0.16, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c)
    g = VGroup(eye, iris, pup)
    g.pup = pup
    return g


def screen_striped(cx, cy, w=1.7, h=1.1):
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1)
    n = 6
    bw = w / (2 * n)
    bars = VGroup(*[Rectangle(width=bw, height=h - 0.08, stroke_width=0, fill_color=TEXT, fill_opacity=0.9)
                    .move_to([-w / 2 + bw * (1 + 2 * i), 0, 0]) for i in range(n)])
    return VGroup(frame, bars).move_to([cx, cy, 0])


def screen_grey(cx, cy, w=1.7, h=1.1):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3,
                     fill_color=GREY, fill_opacity=0.55).move_to([cx, cy, 0])


class S00Title(TitleCard):
    LESSON = "Melanopsin cells"
    TITLE = "Light for the Clock and the Pupil"


# ---------------------------------------------------------------------------------------------
class S01ClockPupil(SpokenScene):
    """no working rods or cones, yet clock and pupil respond: a small set of ganglion cells with melanopsin does it."""

    def construct(self):
        y = -1.0
        rc = cell(-4.9, y, 2.6, 1.2, BLUE)
        rc_t = T("rods and cones", 22, BLUE).move_to([-4.9, y, 0])
        bp = cell(-1.6, y, 1.9, 1.2, BLUE, fill=0.12)
        bp_t = T("bipolar", 22, BLUE).move_to([-1.6, y, 0])
        ip = cell(1.7, y, 2.6, 1.7, GREEN, fill=0.1)
        ip_t = T("ganglion cell", 22, GREEN).move_to([1.7, y, 0])
        br = chip("brain", PURPLE, size=24).move_to([5.4, y, 0])
        a1 = arr([-3.55, y, 0], [-2.6, y, 0])
        a2 = arr([-0.6, y, 0], [0.4, y, 0])
        a3 = arr([3.05, y, 0], [4.7, y, 0])
        chain = VGroup(rc, rc_t, bp, bp_t, ip, ip_t, a1, a2, a3, br)

        self.at("Take a mouse")
        la = light_arrow(-4.9, -3.0, -1.75)
        lt = T("light", 24, YELLOW).move_to([-4.0, -2.8, 0])
        self.play(FadeIn(chain, lag_ratio=0.1), GrowArrow(la), FadeIn(lt), run_time=1.2)

        self.at("rods or cones")
        x1 = cross([-4.9, y, 0], s=0.4)
        self.play(Create(x1), rc.animate.set_stroke(opacity=0.35).set_fill(opacity=0.05),
                  rc_t.animate.set_opacity(0.4), run_time=0.7)

        self.at("It still responds")
        hd = T("still responds to light", 28, TEXT).move_to([-3.4, 0.55, 0])
        self.play(FadeIn(hd, shift=UP * 0.1), Indicate(lt, color=YELLOW, scale_factor=1.2), run_time=0.8)

        self.at("body clock")
        ck = clock_icon(-1.2, 1.9, 0.6)
        ck_l = T("body clock shifts", 24, TEXT).move_to([-1.2, 3.05, 0])
        self.play(FadeOut(hd), Create(ck), FadeIn(ck_l), run_time=0.7)
        self.play(Rotate(ck.h2, angle=-PI / 3, about_point=ck.c), run_time=0.9)

        self.at("pupils still narrow")
        ey = eye_icon(4.3, 1.9, 1.6)
        ey_l = T("pupil narrows", 24, TEXT).move_to([4.3, 3.05, 0])
        self.play(FadeIn(ey), FadeIn(ey_l), run_time=0.6)
        self.play(ey.pup.animate.scale(0.45), run_time=0.8)

        self.at("A small set")
        q = T("?", 60, YELLOW, weight=BOLD).move_to([1.7, 0.45, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)

        self.at("retinal ganglion cells")
        self.play(ip.animate.set_fill(GREEN, 0.4), Indicate(ip_t, color=GREEN), FadeOut(q), run_time=0.8)

        self.at("doing this")
        g_ck = arr([1.4, -0.12, 0], [-1.0, 1.25, 0], GREEN, w=7)
        g_ey = arr([2.0, -0.12, 0], [3.9, 1.3, 0], GREEN, w=7)
        self.play(GrowArrow(g_ck), GrowArrow(g_ey), run_time=0.8)

        self.at("own light pigment")
        la2 = light_arrow(1.7, -3.1, -1.95)
        lt2 = T("light", 24, YELLOW).move_to([1.0, -2.85, 0])
        self.play(GrowArrow(la2), FadeIn(lt2), run_time=0.5)
        self.at("called melanopsin")
        mel = chip("melanopsin", GREEN, size=22, pad=0.12).move_to([1.7, y - 0.28, 0])
        self.play(ip_t.animate.move_to([1.7, y + 0.42, 0]), FadeIn(mel, scale=0.8), run_time=0.7)

        self.at("main route")
        self.play(Indicate(g_ck, color=YELLOW, scale_factor=1.15), Indicate(ck, color=YELLOW), run_time=1.0)
        self.at("drive the pupil")
        self.play(Indicate(g_ey, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.play(ey.pup.animate.scale(1.0 / 0.45), run_time=0.4)
        self.play(ey.pup.animate.scale(0.45), run_time=0.6)

        self.at("report how bright")
        nif = chip("non-image-forming", YELLOW, size=24).move_to([4.0, -2.5, 0])
        self.play(FadeIn(nif, shift=UP * 0.1), run_time=0.5)
        self.at("not what is in")
        nif2 = T("how bright, not what is in it", 22, YELLOW).move_to([4.0, -3.2, 0])
        self.play(FadeIn(nif2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Twojobs(SpokenScene):
    """one large ipRGC with two jobs: its own melanopsin response, and relay of rod and cone signals."""

    def construct(self):
        cx, cy = 1.6, 0.3
        c = cell(cx, cy, 3.6, 3.0, GREEN)
        name = T("ipRGC", 30, GREEN, weight=BOLD).move_to([cx, 1.38, 0])
        br = chip("brain", PURPLE, size=26).move_to([5.6, cy, 0])
        out = arr([2.95, cy, 0], [4.85, cy, 0])

        self.at("These cells are called")
        self.play(FadeIn(c, scale=0.9), FadeIn(out), FadeIn(br), run_time=0.8)
        self.at("Intrinsically Photosensitive")
        full = T("intrinsically photosensitive\nretinal ganglion cells", 24, GREEN, line_spacing=0.9).move_to([-3.6, 2.7, 0])
        self.play(FadeIn(full, shift=UP * 0.1), run_time=0.8)
        self.at("Ganglion Cells or")
        self.play(FadeIn(name, scale=1.2), run_time=0.6)

        self.at("makes its own light")
        la = light_arrow(cx, 3.35, 1.85)
        lt = T("light", 24, YELLOW).move_to([cx + 0.8, 3.0, 0])
        self.play(GrowArrow(la), FadeIn(lt), run_time=0.5)
        self.at("with melanopsin")
        mel = chip("melanopsin", GREEN, size=24).move_to([cx - 0.3, 0.65, 0])
        g_in = arr([2.4, 0.6, 0], [2.95, 0.38, 0], GREEN, w=6, tip=0.16)
        self.play(FadeIn(mel, scale=0.8), GrowArrow(g_in), run_time=0.5)
        j1 = T("job 1: its own light response", 24, GREEN).move_to([3.4, -2.5, 0])
        self.play(Indicate(mel, color=GREEN, scale_factor=1.12), FadeIn(j1, shift=UP * 0.1), run_time=0.8)

        self.at("It also relays")
        rc = cell(-4.9, -0.5, 2.7, 1.1, BLUE)
        rc_t = T("rods and cones", 22, BLUE).move_to([-4.9, -0.5, 0])
        b0 = arr([-3.5, -0.5, 0], [-2.8, -0.5, 0], BLUE, w=6)
        self.play(FadeIn(rc), FadeIn(rc_t), run_time=0.5)
        self.at("through bipolar cells")
        bp = cell(-2.0, -0.5, 1.5, 1.0, BLUE, fill=0.12)
        bp_t = T("bipolar", 22, BLUE).move_to([-2.0, -0.5, 0])
        b2 = arr([-1.25, -0.5, 0], [0.1, -0.5, 0], BLUE, w=6)
        b3 = arr([0.15, -0.5, 0], [2.85, 0.2, 0], BLUE, w=6, tip=0.18)
        self.play(GrowArrow(b0), FadeIn(bp), FadeIn(bp_t), run_time=0.5)
        self.play(GrowArrow(b2), GrowArrow(b3), run_time=0.6)
        j2 = T("job 2: relay of rod and cone signals", 24, BLUE).move_to([-3.1, -2.5, 0])
        self.play(FadeIn(j2, shift=UP * 0.1), run_time=0.5)

        self.at("two jobs")
        self.play(Indicate(j1, color=GREEN, scale_factor=1.08), Indicate(j2, color=BLUE, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Targets(SpokenScene):
    """ipRGC axons reach the SCN (clock) and the olivary pretectal nucleus (pupil); the two routes can be pulled apart."""

    def construct(self):
        ip = cell(-4.6, 0.2, 2.5, 1.7, GREEN)
        ip_t = T("ipRGC", 28, GREEN, weight=BOLD).move_to([-4.6, 0.2, 0])
        q1 = chip("?", YELLOW, size=40, pad=0.3).move_to([1.2, 2.3, 0])
        q2 = chip("?", YELLOW, size=40, pad=0.3).move_to([1.2, -2.3, 0])
        self.at("Where do these signals")
        self.play(FadeIn(ip), FadeIn(ip_t), FadeIn(q1), FadeIn(q2), run_time=0.8)

        self.at("axons reach")
        r1 = arr([-3.55, 0.7, 0], [-1.15, 2.2, 0], GREEN, w=6)
        self.play(GrowArrow(r1), run_time=0.6)
        self.at("suprachiasmatic nucleus")
        scn = chip("suprachiasmatic nucleus", PURPLE, size=24).move_to([1.2, 2.3, 0])
        self.play(ReplacementTransform(q1, scn), run_time=0.7)
        self.at("master clock")
        ck = clock_icon(5.1, 2.3, 0.55)
        ck_l = T("master clock", 22, TEXT).move_to([5.1, 1.4, 0])
        sc_a = arr([3.6, 2.3, 0], [4.4, 2.3, 0], PURPLE, w=5)
        self.play(GrowArrow(sc_a), Create(ck), FadeIn(ck_l), run_time=0.7)

        self.at("Light arriving there")
        dot = Dot([-3.4, 0.65, 0], radius=0.14, color=YELLOW)
        self.add(dot)
        self.play(MoveAlongPath(dot, Line([-3.4, 0.65, 0], [-1.3, 2.0, 0])), run_time=0.9, rate_func=linear)
        self.play(FadeOut(dot, scale=2.0), Indicate(scn, color=PURPLE), run_time=0.4)
        self.at("in step with day")
        self.play(Rotate(ck.h2, angle=-PI / 3, about_point=ck.c), run_time=1.0)
        self.at("called")
        pe = chip("photoentrainment", YELLOW, size=26).move_to([2.4, 0.35, 0])
        self.play(FadeIn(pe, shift=UP * 0.1), run_time=0.6)

        self.at("Other")
        r2 = arr([-3.55, -0.3, 0], [-1.25, -2.2, 0], GREEN, w=6)
        self.play(FadeOut(pe), GrowArrow(r2), run_time=0.8)
        self.at("olivary")
        opn = chip("olivary pretectal nucleus", PURPLE, size=24).move_to([1.2, -2.3, 0])
        self.play(ReplacementTransform(q2, opn), run_time=0.7)
        self.at("narrows the pupil")
        ey = eye_icon(5.1, -2.3, 1.4)
        ey_l = T("pupil narrows", 22, TEXT).move_to([5.1, -1.45, 0])
        op_a = arr([3.7, -2.3, 0], [4.35, -2.3, 0], PURPLE, w=5)
        self.play(GrowArrow(op_a), FadeIn(ey), FadeIn(ey_l), run_time=0.6)
        self.play(ey.pup.animate.scale(0.45), run_time=0.7)

        self.at("pulled apart")
        self.play(Indicate(r1, color=YELLOW, scale_factor=1.1), Indicate(r2, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("Remove one genetically")
        rm = chip("one genetically marked set removed", RED, size=24).move_to([2.3, -0.6, 0])
        xr = cross([-2.4, -1.25, 0], s=0.3)
        self.play(FadeIn(rm, shift=UP * 0.1), Create(xr), run_time=0.7)
        self.at("pupil reflex fails")
        fail = T("pupil reflex fails", 22, RED).move_to([5.1, -1.45, 0])
        self.play(FadeOut(ey_l), FadeIn(fail), r2.animate.set_color(GREY), op_a.animate.set_color(GREY),
                  *dim_anims(opn, 0.4), *dim_anims(ey, 0.35), run_time=0.8)
        self.at("still in trains")
        ck_l2 = T("still entrains", 22, TEXT).move_to([5.1, 1.4, 0])
        self.play(Transform(ck_l, ck_l2), Rotate(ck.h2, angle=-PI / 6, about_point=ck.c),
                  Indicate(scn, color=PURPLE), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04PigmentVsCells(SpokenScene):
    """experiment 1: remove only melanopsin (smaller deficits). Experiment 2: remove the cells (larger deficits)."""

    def panel(self, cx, stub0):
        cy = 1.65
        c = cell(cx, cy, 2.5, 1.7, GREEN)
        name = T("ipRGC", 24, GREEN, weight=BOLD).move_to([cx, cy - 0.5, 0])
        mel = chip("melanopsin", GREEN, size=22, pad=0.1).move_to([cx, cy + 0.32, 0])
        stub = arr([stub0, cy, 0], [cx - 1.25, cy, 0], BLUE, w=6)
        sl = T("rod and cone\nrelay", 22, BLUE, line_spacing=0.8).move_to([(stub0 + cx - 1.25) / 2, cy + 0.72, 0])
        return c, name, mel, stub, sl

    def outputs(self, cx):
        ck = clock_icon(cx - 1.1, -1.1, 0.5)
        ey = eye_icon(cx + 1.1, -1.1, 1.3)
        a1 = arr([cx - 0.5, 0.83, 0], [cx - 1.05, -0.5, 0], GREEN, w=5)
        a2 = arr([cx + 0.5, 0.83, 0], [cx + 1.05, -0.5, 0], GREEN, w=5)
        return ck, ey, a1, a2

    def construct(self):
        lx, rx = -3.3, 3.7
        div = Line([-0.25, 3.5, 0], [-0.25, -3.5, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        lc, ln, lm, ls, lsl = self.panel(lx, -6.2)
        rc_, rn, rm, rs, rsl = self.panel(rx, 0.8)
        lt = T("remove only melanopsin", 26, TEXT).move_to([lx, 3.1, 0])
        rt = T("remove the cells", 26, TEXT).move_to([rx, 3.1, 0])
        lck, ley, la1, la2 = self.outputs(lx)
        rck, rey, ra1, ra2 = self.outputs(rx)

        self.play(FadeIn(div), FadeIn(VGroup(lc, ln, lm, ls, lsl, rc_, rn, rm, rs, rsl)), run_time=1.0)
        self.at("Compare two experiments")
        self.play(FadeIn(lt), FadeIn(rt), run_time=0.7)

        self.at("Take away only melanopsin")
        xl = cross(lm.get_center(), s=0.28)
        self.play(Create(xl), lm.animate.set_opacity(0.35), run_time=0.6)

        self.at("still in train")
        lck_l = T("still entrains", 22, TEXT).move_to([lx - 1.1, -2.0, 0])
        self.play(GrowArrow(la1), Create(lck), FadeIn(lck_l), run_time=0.7)
        self.at("clock shifts less")
        ghost = lck.h2.copy().set_color(GREY).set_opacity(0.7)
        ghost.rotate(-PI / 3, about_point=lck.c)
        lck_l2 = T("shifts less", 22, TEXT).move_to([lx - 1.1, -2.0, 0])
        self.play(FadeIn(ghost), Transform(lck_l, lck_l2),
                  Rotate(lck.h2, angle=-PI / 6, about_point=lck.c), run_time=1.0)

        self.at("in steady bright light")
        self.play(GrowArrow(la2), FadeIn(ley), run_time=0.5)
        self.play(ley.pup.animate.scale(0.45), run_time=0.6)
        self.at("slowly widen")
        ley_l = T("narrows, then\nslowly widens", 22, TEXT, line_spacing=0.8).move_to([lx + 1.1, -2.2, 0])
        self.play(FadeIn(ley_l), ley.pup.animate.scale(1.65), run_time=1.6)

        self.at("Now take away the cells")
        ghost_c = cell(rx, 1.65, 2.5, 1.7, GREY, fill=0.05, dashed=True)
        self.play(FadeOut(rc_), FadeIn(ghost_c), rn.animate.set_color(GREY).set_opacity(0.5),
                  rm.animate.set_color(GREY).set_opacity(0.4), run_time=0.8)
        self.at("leave rods and cones")
        self.play(Indicate(rs, color=BLUE, scale_factor=1.1), Indicate(rsl, color=BLUE, scale_factor=1.1), run_time=1.0)

        self.at("clock and pupil deficits")
        dim_static(rck, 0.35)
        dim_static(rey, 0.35)
        ra1.set_color(GREY)
        ra2.set_color(GREY)
        rcl = T("larger deficit", 22, RED).move_to([rx - 1.1, -2.0, 0])
        rel = T("larger deficit", 22, RED).move_to([rx + 1.1, -2.0, 0])
        x1 = cross(rm.get_center(), s=0.28)
        x2 = cross(rs.get_center(), s=0.28)
        self.play(GrowArrow(ra1), GrowArrow(ra2), FadeIn(rck), FadeIn(rey), FadeIn(rcl), FadeIn(rel),
                  Create(x1), Create(x2), run_time=0.9)
        self.at("much like mice that lack")
        note = T("much like lacking melanopsin,\nrods and cones together", 22, TEXT, line_spacing=0.85).move_to([rx, -3.05, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Rule(SpokenScene):
    """summary: rods/cones and melanopsin both feed the ipRGC, which feeds clock and pupil; pigment = one job, cells = both."""

    def construct(self):
        cx, cy = -0.8, 1.0
        c = cell(cx, cy, 3.4, 2.2, GREEN)
        name = T("ipRGC", 28, GREEN, weight=BOLD).move_to([cx, 0.42, 0])
        mel = chip("melanopsin", GREEN, size=22, pad=0.12).move_to([cx, 1.4, 0])
        rc = chip("rods and cones", BLUE, size=22, pad=0.18).move_to([-4.9, cy, 0])
        b_in = arr([-3.65, cy, 0], [-2.5, cy, 0], BLUE, w=6)
        ck = clock_icon(3.4, 2.4, 0.55)
        ck_l = T("clock", 26, TEXT).move_to([4.6, 2.4, 0])
        ey = eye_icon(3.4, -0.4, 1.4)
        ey_l = T("pupil", 26, TEXT).move_to([4.9, -0.4, 0])
        b_ck = arr([0.75, 1.75, 0], [2.75, 2.3, 0], BLUE, w=6)
        b_ey = arr([0.7, 0.2, 0], [2.7, -0.35, 0], BLUE, w=6)
        g_ey = arr([0.25, 1.2, 0], [2.8, 0.15, 0], GREEN, w=6)

        self.at("So rods")
        self.play(FadeIn(c), FadeIn(name), FadeIn(rc), GrowArrow(b_in), run_time=0.8)
        self.at("clock and pupil signals")
        self.play(GrowArrow(b_ck), GrowArrow(b_ey), Create(ck), FadeIn(ey), FadeIn(ck_l), FadeIn(ey_l), run_time=0.9)

        self.at("melanopsin holds the pupil")
        self.play(FadeIn(mel, scale=0.8), GrowArrow(g_ey), run_time=0.6)
        steady = T("steady in bright light", 22, GREEN).move_to([3.4, -1.4, 0])
        self.play(FadeIn(steady, shift=UP * 0.1), ey.pup.animate.scale(0.5), run_time=0.7)

        self.at("Taking out the pigment")
        xm = cross(mel.get_center(), s=0.28)
        self.play(Create(xm), mel.animate.set_opacity(0.35), g_ey.animate.set_color(GREY), FadeOut(steady), run_time=0.7)
        self.at("removes one job")
        ca = chip("remove pigment: one job", RED, size=24).move_to([-3.5, -2.1, 0])
        self.play(FadeIn(ca, shift=UP * 0.1), run_time=0.5)

        self.at("Taking out the cells")
        ghost = cell(cx, cy, 3.4, 2.2, GREY, fill=0.05, dashed=True)
        self.play(FadeOut(xm), FadeOut(c), FadeIn(ghost), mel.animate.set_color(GREY).set_opacity(0.4),
                  name.animate.set_color(GREY).set_opacity(0.5), g_ey.animate.set_color(GREEN), run_time=0.8)
        self.at("removes both")
        x1 = cross([1.75, 2.05, 0], s=0.26)
        x2 = cross([1.7, -0.08, 0], s=0.26)
        x3 = cross([1.5, 0.7, 0], s=0.26)
        cb = chip("remove cells: both jobs", RED, size=24).move_to([3.5, -2.1, 0])
        self.play(Create(x1), Create(x2), Create(x3), FadeIn(cb, shift=UP * 0.1),
                  *dim_anims(ck, 0.35), *dim_anims(ey, 0.35), run_time=0.8)

        self.at("That is why")
        self.play(Indicate(ca, color=RED, scale_factor=1.08), Indicate(cb, color=RED, scale_factor=1.08), run_time=1.0)
        self.at("different questions")
        dq = T("different\nquestions", 24, YELLOW, weight=BOLD, line_spacing=0.85).move_to([0, -2.1, 0])
        self.play(FadeIn(dq, scale=1.1), run_time=0.5)

        self.at("When you can")
        ad = chip("remove in adult animals", GREY, size=24).move_to([-3.3, -3.25, 0])
        self.play(FadeIn(ad, shift=UP * 0.1), run_time=0.5)
        self.at("rewire targets")
        rw = T("development loss can rewire targets", 22, TEXT).move_to([2.9, -3.25, 0])
        self.play(FadeIn(rw), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Beyond(SpokenScene):
    """side notes: mood and learning, coarse pattern vision; the main job is still the clock and the pupil."""

    def construct(self):
        ip = cell(-4.6, 0.2, 2.5, 1.7, GREEN)
        ip_t = T("ipRGC", 28, GREEN, weight=BOLD).move_to([-4.6, 0.2, 0])
        self.at("In mice")
        mice = T("in mice", 28, GREY).move_to([0, 3.1, 0])
        self.play(FadeIn(ip), FadeIn(ip_t), FadeIn(mice), run_time=0.7)

        self.at("mood and learning")
        mood = chip("mood", PURPLE, size=28).move_to([0.2, 1.7, 0])
        learn = chip("learning", PURPLE, size=28).move_to([0.2, -1.3, 0])
        m_a = arr([-3.4, 0.6, 0], [-0.9, 1.6, 0], GREEN, w=6)
        l_a = arr([-3.4, -0.2, 0], [-1.1, -1.2, 0], GREEN, w=6)
        self.play(GrowArrow(m_a), FadeIn(mood), run_time=0.5)
        self.play(GrowArrow(l_a), FadeIn(learn), run_time=0.5)
        self.at("separate routes")
        sep = T("two separate routes, apparently", 24, TEXT).move_to([3.0, 0.2, 0])
        self.play(FadeIn(sep, shift=UP * 0.1), run_time=0.6)

        self.at("A smaller story")
        pv = chip("a smaller story: seeing patterns", YELLOW, size=26).move_to([0, 3.1, 0])
        self.play(FadeOut(VGroup(ip, ip_t, mice, mood, learn, m_a, l_a, sep)), FadeIn(pv), run_time=0.7)

        self.at("Mice lacking rod")
        head = T("mice lacking rod and cone signalling", 26, BLUE).move_to([0, 2.3, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("grating from plain")
        st = screen_striped(-2.8, 0.95, 3.4, 1.7)
        gr = screen_grey(2.8, 0.95, 3.4, 1.7)
        st_l = T("grating", 22, TEXT).move_to([-2.8, -0.15, 0])
        gr_l = T("plain grey", 22, TEXT).move_to([2.8, -0.15, 0])
        self.play(FadeIn(st), FadeIn(gr), FadeIn(st_l), FadeIn(gr_l), run_time=0.7)
        self.at("plain gray")
        tell = T("can tell them apart", 26, GREEN).move_to([0, -0.75, 0])
        self.play(FadeIn(tell, shift=UP * 0.1), run_time=0.5)

        self.at("mice lacking melanopsin")
        ml = T("mice lacking melanopsin", 24, GREEN).move_to([-2.8, -1.55, 0])
        self.play(FadeIn(ml), run_time=0.5)
        self.at("showed contrast")
        cd = T("contrast deficits", 24, TEXT).move_to([1.7, -1.55, 0])
        self.play(FadeIn(cd, shift=UP * 0.1), run_time=0.5)

        self.at("very coarse vision")
        c1 = chip("very coarse vision", GREY, size=26).move_to([-2.4, -2.7, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("not normal acuity")
        c2 = chip("not normal acuity", GREY, size=26).move_to([2.7, -2.7, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)

        self.at("The main job")
        old = VGroup(pv, head, st, gr, st_l, gr_l, tell, ml, cd, c1, c2)
        ip2 = cell(-4.2, 0.3, 2.8, 1.8, GREEN)
        ip2_t = T("ipRGC", 30, GREEN, weight=BOLD).move_to([-4.2, 0.3, 0])
        ck = clock_icon(2.4, 1.9, 0.8)
        ey = eye_icon(2.4, -1.4, 2.0)
        ck_l = T("body clock", 30, TEXT).move_to([4.9, 1.9, 0])
        ey_l = T("pupil reflex", 30, TEXT).move_to([4.9, -1.4, 0])
        g1 = arr([-3.0, 0.9, 0], [1.4, 1.8, 0], GREEN, w=10, tip=0.3)
        g2 = arr([-3.0, -0.3, 0], [1.3, -1.3, 0], GREEN, w=10, tip=0.3)
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(ip2), FadeIn(ip2_t), run_time=0.3)
        self.play(GrowArrow(g1), GrowArrow(g2), Create(ck), FadeIn(ey), FadeIn(ck_l), FadeIn(ey_l), run_time=0.9)
        self.at("still the clock")
        self.play(Indicate(ck, color=YELLOW, scale_factor=1.2), Indicate(g1, color=YELLOW, scale_factor=1.1),
                  Rotate(ck.h2, angle=-PI / 3, about_point=ck.c), run_time=1.0)
        self.play(Indicate(ey, color=YELLOW, scale_factor=1.15), Indicate(g2, color=YELLOW, scale_factor=1.1),
                  ey.pup.animate.scale(0.5), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "The main job of these cells is the clock and the pupil."
