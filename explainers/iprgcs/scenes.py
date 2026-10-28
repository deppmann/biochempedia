"""ipRGCs: remove the cells, or the pigment?  (Biochemistrypedia sensory explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light, and the open question mark
  BLUE   = rod and cone signals and their relay through bipolar cells
  GREEN  = the ipRGC and its own melanopsin response
  PURPLE = brain targets (brain, dLGN)
  RED    = removed or lost (crossed out)
  GREY   = outlines, wild type, de-emphasized
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


def screen_striped(cx, cy, w=1.7, h=1.1):
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1)
    bars = VGroup(*[Rectangle(width=w / 11, height=h - 0.06, stroke_width=0, fill_color=TEXT, fill_opacity=0.9)
                    .move_to([-w / 2 + w / 11 * (1 + 2 * i) - w / 22 + w / 11, 0, 0]) for i in range(5)])
    g = VGroup(frame, bars)
    return g.move_to([cx, cy, 0])


def screen_grey(cx, cy, w=1.7, h=1.1):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).move_to([cx, cy, 0])


def light_arrow(x, ytop, ybot):
    return arr([x, ytop, 0], [x, ybot, 0], YELLOW, w=6)


def ip_unit(cx, cy, w=2.8, h=1.8):
    """ipRGC with its melanopsin chip inside and the rod-and-cone relay arriving from below."""
    c = cell(cx, cy, w, h, GREEN)
    name = T("ipRGC", 28, GREEN).move_to([cx, cy - h * 0.28, 0])
    mel = chip("melanopsin", GREEN, size=24, pad=0.14).move_to([cx, cy + h * 0.22, 0])
    rel_a = arr([cx, cy - h / 2 - 1.45, 0], [cx, cy - h / 2 - 0.02, 0], BLUE, w=6)
    rel_l = T("rod and cone relay", 24, BLUE).move_to([cx, cy - h / 2 - 1.85, 0])
    return {"cell": c, "name": name, "mel": mel, "arrow": rel_a, "label": rel_l}


class S00Title(TitleCard):
    LESSON = "Melanopsin cells: seeing without images"
    TITLE = "Remove the cells, or the pigment?"


# ---------------------------------------------------------------------------------------------
class S01Seeing(SpokenScene):
    """no working rods or cones, yet the clock shifts and the pupil narrows: non-image-forming -> which cells? -> the ipRGC with melanopsin."""

    def construct(self):
        y = -1.0
        rc = cell(-5.0, y, 1.5, 1.0, BLUE)
        rc_l = T("rods and cones", 22, BLUE).move_to([-5.0, y - 0.95, 0])
        bp = cell(-1.9, y, 1.5, 1.0, BLUE, fill=0.12)
        bp_l = T("bipolar cell", 22, BLUE).move_to([-1.9, y - 0.95, 0])
        ip = cell(1.4, y, 1.7, 1.1, GREEN, fill=0.12)
        ip_l = T("ganglion cell", 22, GREEN).move_to([1.4, y - 0.95, 0])
        br = chip("brain", PURPLE, size=24).move_to([5.3, y, 0])
        a1 = arr([-4.2, y, 0], [-2.75, y, 0])
        a2 = arr([-1.05, y, 0], [0.5, y, 0])
        a3 = arr([2.3, y, 0], [4.5, y, 0])
        retina = VGroup(rc, rc_l, bp, bp_l, ip, ip_l, a1, a2, a3, br)

        self.at("no working")
        lt = T("light", 24, YELLOW).move_to([-5.0, 0.95, 0])
        la = light_arrow(-5.0, 0.6, 0.25)
        self.play(FadeIn(retina, lag_ratio=0.12), FadeIn(lt), GrowArrow(la), run_time=0.6)
        self.at("rods or cones")
        x1 = cross([-5.0, y, 0])
        self.play(Create(x1), rc.animate.set_stroke(opacity=0.35).set_fill(opacity=0.05), run_time=0.6)

        self.at("still responds")
        hd = T("no rods or cones, yet light still works", 24, TEXT).move_to([3.6, 3.4, 0])
        self.play(FadeIn(hd), run_time=0.5)

        self.at("body clock")
        ck = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=4).move_to([2.6, 2.4, 0])
        hands = VGroup(Line(ck.get_center(), ck.get_center() + [0, 0.38, 0], color=YELLOW, stroke_width=4),
                       Line(ck.get_center(), ck.get_center() + [0.28, -0.12, 0], color=YELLOW, stroke_width=4))
        ck_l = T("body clock shifts", 22, TEXT).next_to(ck, DOWN, buff=0.15)
        self.play(Create(ck), Create(hands), FadeIn(ck_l), run_time=0.7)
        self.play(Rotate(hands[1], angle=-PI / 2, about_point=ck.get_center()), run_time=0.6)

        self.at("pupils still narrow")
        eye = Ellipse(width=1.5, height=0.85, stroke_color=GREY, stroke_width=4).move_to([5.2, 2.4, 0])
        iris = Circle(radius=0.36, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to(eye)
        pup = Circle(radius=0.24, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(eye)
        eye_l = T("pupil narrows", 22, TEXT).next_to(eye, DOWN, buff=0.15)
        self.play(FadeIn(eye), FadeIn(iris), FadeIn(pup), FadeIn(eye_l), run_time=0.6)
        self.play(pup.animate.scale(0.45), run_time=0.6)

        self.at("These are")
        nif = chip("non-image-forming", YELLOW, size=24).move_to([3.9, 0.55, 0])
        self.play(FadeIn(nif, shift=UP * 0.1), run_time=0.5)
        self.at("how bright")
        nif2 = T("how bright, not what is there", 22, YELLOW).next_to(nif, DOWN, buff=0.12)
        self.play(FadeIn(nif2), run_time=0.5)

        self.at("which cells detect")
        q = T("?", 64, YELLOW, weight=BOLD).move_to([1.4, 0.55, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)

        self.at("retinal ganglion cells")
        self.play(ip.animate.set_stroke(opacity=1).set_fill(GREEN, 0.4), Indicate(ip_l, color=GREEN),
                  FadeOut(q), run_time=0.9)
        self.at("own light pigment")
        la2 = light_arrow(1.4, 0.6, -0.2)
        self.play(GrowArrow(la2), run_time=0.5)
        self.at("pigment called")
        mel = chip("melanopsin", GREEN, size=24).move_to([1.4, -2.9, 0])
        self.play(FadeIn(mel, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Twojobs(SpokenScene):
    """one large ipRGC with two jobs: its own melanopsin response, and relay of rod and cone signals."""

    def construct(self):
        cx, cy = 1.0, 0.4
        c = cell(cx, cy, 3.8, 3.0, GREEN)
        name = T("ipRGC", 32, GREEN).move_to([cx, cy - 0.8, 0])
        br = chip("brain", PURPLE, size=26).move_to([5.4, cy, 0])
        out = arr([cx + 1.9, cy, 0], [4.55, cy, 0])
        self.at("These cells are called")
        self.play(FadeIn(c, scale=0.9), FadeIn(name), run_time=0.8)
        self.play(FadeIn(out), FadeIn(br), run_time=0.5)

        self.at("makes its own light response")
        la = light_arrow(cx, 3.3, 2.05)
        lt = T("light", 24, YELLOW).move_to([cx + 0.9, 2.95, 0])
        mel = chip("melanopsin", GREEN, size=28).move_to([cx, cy + 0.5, 0])
        j1 = T("job 1: its own light response", 26, GREEN).move_to([3.0, -2.4, 0])
        self.play(GrowArrow(la), FadeIn(lt), run_time=0.5)
        self.play(FadeIn(mel, scale=0.8), run_time=0.5)
        self.play(Indicate(mel, color=GREEN, scale_factor=1.12), FadeIn(j1, shift=UP * 0.1), run_time=0.8)

        self.at("relays signals that rods")
        rc = cell(-5.4, cy, 1.5, 1.0, BLUE)
        rc_l = T("rods and cones", 22, BLUE).move_to([-5.4, cy - 0.95, 0])
        bp = cell(-3.0, cy, 1.2, 0.9, BLUE, fill=0.12)
        bp_l = T("bipolar cell", 22, BLUE).move_to([-3.0, cy + 0.85, 0])
        b1 = arr([-4.55, cy, 0], [-3.7, cy, 0], BLUE, w=6)
        b2 = arr([-2.3, cy, 0], [cx - 1.9 - 0.02, cy, 0], BLUE, w=6)
        self.play(FadeIn(rc), FadeIn(rc_l), run_time=0.5)
        self.at("through bipolar cells")
        self.play(GrowArrow(b1), FadeIn(bp), FadeIn(bp_l), run_time=0.5)
        self.play(GrowArrow(b2), run_time=0.5)
        j2 = T("job 2: relay of rod and cone signals", 26, BLUE).move_to([-3.0, -3.0, 0])
        self.play(FadeIn(j2, shift=UP * 0.1), run_time=0.5)

        self.at("two jobs")
        self.play(Indicate(j1, color=GREEN, scale_factor=1.08), Indicate(j2, color=BLUE, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Grating(SpokenScene):
    """harder question, pattern vision: grating vs grey discriminated; labelled cells reach the dLGN; 0.16 vs 0.55 cycles per degree."""

    def construct(self):
        pv = T("pattern vision?", 30, YELLOW, weight=BOLD).move_to([3.6, 3.1, 0])
        self.play(FadeIn(pv), run_time=0.5)
        self.at("Mice lacking rod")
        head = T("In mice lacking rod and cone signalling", 24, GREY).move_to([-3.4, 3.1, 0])
        self.play(FadeIn(head), run_time=0.5)
        st = screen_striped(-5.0, 1.9)
        gr = screen_grey(-2.4, 1.9)
        st_l = T("grating", 22, TEXT).next_to(st, DOWN, buff=0.15)
        gr_l = T("equally bright grey", 22, TEXT).next_to(gr, DOWN, buff=0.15)
        self.play(FadeIn(st), FadeIn(gr), FadeIn(st_l), FadeIn(gr_l), run_time=0.8)
        self.at("discriminate a grating")
        disc = T("discriminated", 26, GREEN).move_to([-3.7, 0.2, 0])
        self.play(FadeIn(disc, shift=UP * 0.1), run_time=0.5)

        self.at("with a melanopsin")
        ip = cell(-5.0, -1.5, 1.5, 1.0, GREEN)
        ip_l = T("labelled cells", 22, GREEN).move_to([-5.0, -2.35, 0])
        dl = chip("dLGN", PURPLE, size=26).move_to([-2.0, -1.5, 0])
        ar = arr([-4.15, -1.5, 0], [-2.85, -1.5, 0], GREEN, w=6)
        self.play(FadeIn(ip), FadeIn(ip_l), run_time=0.5)
        self.at("heavily innervated")
        self.play(GrowArrow(ar), FadeIn(dl), run_time=0.6)
        cap = T("heavily innervate a brain target", 22, GREY).move_to([-3.5, -3.1, 0])
        self.play(FadeIn(cap), run_time=0.4)

        self.at("not normal acuity")
        base = -2.3
        sc = 6.0
        axis = Line([1.5, base, 0], [6.3, base, 0], color=GREY, stroke_width=3)
        b1 = Rectangle(width=1.3, height=0.16 * sc, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
        b1.move_to([2.9, base + 0.16 * sc / 2, 0])
        b2 = Rectangle(width=1.3, height=0.55 * sc, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
        b2.move_to([5.1, base + 0.55 * sc / 2, 0])
        l1 = T("no rod and cone\nsignalling", 22, BLUE, line_spacing=0.8).move_to([2.9, base - 0.65, 0])
        l2 = T("wild type", 22, GREY).move_to([5.1, base - 0.45, 0])
        unit = T("cycles per degree", 24, GREY).move_to([3.9, 2.4, 0])
        self.play(Create(axis), FadeIn(unit), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.at("Those mice")
        v1 = M("0.16", 28, BLUE).next_to(b1, UP, buff=0.12)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=0.7)
        self.at("Wild type mice")
        v2 = M("0.55", 28, GREY).next_to(b2, UP, buff=0.12)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pigment(SpokenScene):
    """lacking melanopsin -> contrast deficits; taking out the pigment removes one job, the cells remove both."""

    def construct(self):
        u = ip_unit(-3.2, 0.6, 3.6, 2.4)
        title = T("mice lacking melanopsin", 28, GREEN).move_to([-3.2, 3.15, 0])
        res = T("deficits in contrast sensitivity", 24, TEXT).move_to([-3.2, 2.55, 0])
        xm = cross(u["mel"].get_center(), s=0.3)
        self.play(FadeIn(title), FadeIn(u["cell"]), FadeIn(u["name"]), FadeIn(u["mel"]), GrowArrow(u["arrow"]), FadeIn(u["label"]), run_time=0.8)
        self.play(Create(xm), u["mel"].animate.set_opacity(0.35), run_time=0.4)
        self.at("deficits in contrast")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)

        self.at("look at what was removed")
        self.play(Indicate(u["name"], color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("removes one job")
        t1 = T("one job removed", 28, RED).move_to([-3.2, -3.25, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)

        self.at("Taking out the cells")
        v = ip_unit(3.2, 0.6, 3.6, 2.4)
        title2 = T("cells removed", 28, RED).move_to([3.2, 3.15, 0])
        ghost = cell(3.2, 0.6, 3.6, 2.4, GREY, fill=0.05, dashed=True)
        gname = v["name"].set_color(GREY).set_opacity(0.5)
        gmel = v["mel"].set_color(GREY).set_opacity(0.4)
        garr = v["arrow"].set_color(GREY).set_opacity(0.5)
        glab = v["label"].set_color(GREY).set_opacity(0.6)
        self.play(FadeIn(title2), FadeIn(ghost), FadeIn(gname), FadeIn(gmel), FadeIn(garr), FadeIn(glab), run_time=0.8)
        self.at("removes both")
        x2 = cross(v["mel"].get_center(), s=0.3)
        x3 = cross(v["arrow"].get_center(), s=0.3)
        t2 = T("both jobs removed", 28, RED).move_to([3.2, -3.25, 0])
        self.play(Create(x2), Create(x3), FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ablation(SpokenScene):
    """ablation removes both routes together, so it cannot say which one mattered."""

    def construct(self):
        u = ip_unit(-3.3, 0.9, 3.6, 2.4)
        self.at("picture an ablation")
        self.play(FadeIn(u["cell"]), FadeIn(u["name"]), FadeIn(u["mel"]), GrowArrow(u["arrow"]), FadeIn(u["label"]), run_time=1.0)
        head = T("ablation: cells removed", 28, RED).move_to([3.3, 2.9, 0])

        self.at("Remove the cells")
        ghost = cell(-3.3, 0.9, 3.6, 2.4, GREY, fill=0.05, dashed=True)
        self.play(FadeIn(head), FadeOut(u["cell"]), FadeIn(ghost), u["name"].animate.set_color(GREY).set_opacity(0.5),
                  u["mel"].animate.set_opacity(0.4), run_time=0.9)
        self.at("does worse")
        worse = T("animal does worse", 30, TEXT).move_to([3.3, 1.8, 0])
        self.play(FadeIn(worse, shift=UP * 0.1), run_time=0.5)

        self.at("lost the melanopsin response")
        x1 = cross(u["mel"].get_center(), s=0.3)
        self.play(Create(x1), run_time=0.4)
        self.at("rod and cone relay together")
        x2 = cross(u["arrow"].get_center(), s=0.3)
        self.play(Create(x2), u["arrow"].animate.set_color(GREY), u["label"].animate.set_color(GREY), run_time=0.6)
        lost = T("both lost together", 30, RED).move_to([3.3, 0.8, 0])
        self.play(FadeIn(lost, shift=UP * 0.1), run_time=0.5)

        self.at("cannot say which")
        q1 = T("pigment response?", 28, GREEN).move_to([3.3, -0.35, 0])
        q2 = T("rod and cone relay?", 28, BLUE).move_to([3.3, -1.05, 0])
        qq = T("?", 64, YELLOW, weight=BOLD).move_to([-3.3, 2.95, 0])
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(qq, scale=1.4), run_time=0.7)

        self.at("A task can fail")
        note = T("a task can fail without\nthe pigment mattering", 26, YELLOW, line_spacing=0.9).move_to([3.3, -2.45, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """compare knockouts with removed cells; adult timed manipulation; limits; the rule."""

    def construct(self):
        c1 = chip("melanopsin knockout", GREEN, size=26).move_to([-3.2, 2.6, 0])
        s1 = T("pigment gone, cells stay", 22, GREEN).next_to(c1, DOWN, buff=0.15)
        c2 = chip("ipRGCs removed", RED, size=26).move_to([3.2, 2.6, 0])
        s2 = T("cells gone", 22, RED).next_to(c2, DOWN, buff=0.15)
        both = arr([-0.55, 2.6, 0], [0.55, 2.6, 0], YELLOW)
        both2 = arr([0.55, 2.6, 0], [-0.55, 2.6, 0], YELLOW)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), FadeIn(s1), run_time=0.7)
        self.at("Compare melanopsin knockouts")
        self.play(Indicate(c1, color=GREEN, scale_factor=1.08), run_time=0.6)
        self.at("whose")
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeIn(s2), GrowArrow(both), GrowArrow(both2), run_time=0.7)

        self.at("Prefer an adult")
        c3 = chip("adult, timed manipulation", BLUE, size=26).move_to([0, 0.7, 0])
        s3 = T("loss during development can rewire targets", 22, GREY).next_to(c3, DOWN, buff=0.15)
        self.play(FadeIn(c3, scale=0.9), run_time=0.6)
        self.at("rewire targets")
        self.play(FadeIn(s3), run_time=0.5)

        self.at("remember the limits")
        c4 = chip("results come from mice", GREY, size=26).move_to([0, -1.0, 0])
        c5 = chip("grating discrimination: not normal acuity", GREY, size=26)
        c5.move_to([0, -2.0, 0])
        self.play(FadeIn(c4, shift=UP * 0.15), run_time=0.5)
        self.at("discrimination is not")
        self.play(FadeIn(c5, shift=UP * 0.15), run_time=0.5)

        self.at("Removing the cells and removing the pigment")
        self.play(Indicate(c1, color=GREEN, scale_factor=1.1), Indicate(c2, color=RED, scale_factor=1.1), run_time=1.0)
        dq = T("different questions", 30, YELLOW, weight=BOLD).move_to([0, -3.05, 0])
        self.at("answer different questions")
        self.play(FadeIn(dq, scale=1.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Removing the cells and removing the pigment answer different questions."
