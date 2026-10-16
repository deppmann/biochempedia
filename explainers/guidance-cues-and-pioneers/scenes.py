"""Guidance cues and pioneers: a long route in short legs  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = pioneer axons and their growth cones
  YELLOW = guidepost cells
  GREEN  = the normal route, cut into legs
  RED    = destroyed guidepost, abnormal branches
  PURPLE = follower axons
  GREY   = tissue (corridor, boundaries), the central nervous system, labels
  TEXT   = the beam of light, question marks
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

P = [np.array(p + [0.0]) for p in ([-5.5, -2.6], [-3.5, 0.2], [-1.3, -2.0], [0.9, 1.0], [3.1, 2.5])]
OFFS = [np.array([0.1, 0.2, 0]), np.array([-0.1, -0.2, 0])]   # two pioneer axons side by side
CNS_POS = np.array([5.0, 2.55, 0])
LEG_LABEL_POS = np.array([3.4, -2.6, 0])


def tube():
    t = VMobject()
    t.set_points_as_corners(P)
    t.set_stroke(GREY, width=90, opacity=0.16)
    return t


def cns():
    c = chip("central\nnervous system", GREY, size=22)
    return c.move_to(CNS_POS)


def gcone(color=BLUE):
    core = Circle(radius=0.11, stroke_width=0, fill_color=color, fill_opacity=1)
    spikes = VGroup(*[Line(0.11 * np.array([np.cos(a), np.sin(a), 0]), 0.22 * np.array([np.cos(a), np.sin(a), 0]),
                           color=color, stroke_width=3) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(core, spikes).set_z_index(4)


def pioneers(at=0):
    return VGroup(*[gcone().move_to(P[at] + o) for o in OFFS])


def walk(scene, gcs, a, b, rt, trail):
    anims = []
    for g, o in zip(gcs, OFFS):
        ln = Line(P[a] + o, P[b] + o, color=BLUE, stroke_width=5).set_z_index(2)
        trail.add(ln)
        anims += [Create(ln), g.animate.move_to(P[b] + o)]
    scene.play(*anims, run_time=rt)


def post(i, r=0.27, cluster=False):
    if cluster:
        back = Circle(radius=0.42, stroke_width=0, fill_color=BG, fill_opacity=1)
        dots = [Circle(radius=0.15, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45).move_to(p)
                for p in ([-0.17, -0.1, 0], [0.17, -0.1, 0], [0.0, 0.2, 0])]
        return VGroup(back, *dots).move_to(P[i]).set_z_index(3)
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    ring = Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.45)
    return VGroup(back, ring).move_to(P[i]).set_z_index(3)


def cross(i, s=0.42):
    c = P[i]
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=RED, stroke_width=8),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=RED, stroke_width=8)).set_z_index(3)


def leg(i):
    d = P[i + 1] - P[i]
    u = d / np.linalg.norm(d)
    return Line(P[i] + u * 0.3, P[i + 1] - u * 0.3, color=GREEN, stroke_width=11).set_stroke(opacity=0.6).set_z_index(1)


class S00Title(TitleCard):
    LESSON = "Pioneers, guideposts and guidance cues"
    TITLE = "A Long Route in Short Legs"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        tb = tube()
        leg_lbl = T("grasshopper embryo leg", 24, GREY).move_to(LEG_LABEL_POS)
        self.at("young leg")
        self.play(Create(tb), FadeIn(leg_lbl), run_time=1.0)
        gcs = pioneers(0)
        lbl = T("first axons", 24, BLUE).next_to(gcs, DOWN, buff=0.3)
        self.at("first axons")
        self.play(FadeIn(gcs, scale=0.5), FadeIn(lbl), run_time=0.6)
        c = cns()
        self.at("central nervous system")
        self.play(FadeIn(c, shift=LEFT * 0.2), run_time=0.6)
        qs = VGroup(*[T("?", 48, TEXT, weight=BOLD).move_to((P[i] + P[i + 1]) / 2) for i in range(4)])
        self.at("nothing to follow")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.25), run_time=1.2)
        self.at("kill one")
        self.play(Indicate(qs[0], color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("which way to go")
        self.play(Wiggle(gcs, scale_value=1.3, rotation_angle=0.05 * TAU), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Legs(SpokenScene):
    def construct(self):
        tb = tube()
        c = cns()
        gcs = pioneers(0)
        lbl = T("first axons", 24, BLUE).next_to(gcs, DOWN, buff=0.3)
        self.add(tb, c, gcs, lbl)
        # the map that is not there
        mp = chip("map", GREY, size=30).move_to([-3.4, 2.4, 0])
        xx = VGroup(Line([-0.45, -0.45, 0], [0.45, 0.45, 0], color=RED, stroke_width=6),
                    Line([-0.45, 0.45, 0], [0.45, -0.45, 0], color=RED, stroke_width=6)).move_to(mp)
        self.at("does not carry a map")
        self.play(FadeIn(mp), run_time=0.4)
        self.play(Create(xx), run_time=0.4)
        self.at("one stretch at a time")
        self.play(FadeOut(mp), FadeOut(xx), run_time=0.4)
        legs = VGroup(*[leg(i) for i in range(4)])
        self.at("short legs")
        self.play(LaggedStart(*[Create(l) for l in legs], lag_ratio=0.5), run_time=1.6)
        lbl2 = T("pioneers", 24, BLUE).next_to(gcs, DOWN, buff=0.3)
        self.at("called pioneers")
        self.play(ReplacementTransform(lbl, lbl2), run_time=0.5)
        posts = VGroup(post(1), post(2), post(3))
        pl = T("guidepost cells", 24, YELLOW).move_to([-1.4, -3.0, 0])
        self.at("guidepost cells")
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in posts], lag_ratio=0.3), FadeIn(pl), run_time=1.0)
        trail = VGroup()
        self.at("At a guidepost")
        walk(self, gcs, 0, 1, 1.0, trail)
        self.at("stops")
        self.play(Indicate(posts[0], color=YELLOW, scale_factor=1.35), run_time=0.8)
        self.at("changes course")
        walk(self, gcs, 1, 2, 0.7, trail)
        self.play(Indicate(posts[1], color=YELLOW, scale_factor=1.35), run_time=0.5)
        walk(self, gcs, 2, 3, 0.7, trail)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cut(SpokenScene):
    def construct(self):
        tb = tube()
        c = cns()
        legs = VGroup(*[leg(i) for i in range(4)])
        posts = VGroup(post(1, cluster=True), post(2), post(3))
        gcs = pioneers(0)
        self.add(tb, c, legs, posts, gcs)
        ti = chip("Ti1", BLUE, size=24).move_to([-5.75, -1.45, 0])
        self.at("pair of nerve cells")
        self.play(FadeIn(ti), run_time=0.5)
        cx = chip("Cx1 cells", YELLOW, size=24).move_to([-1.95, 0.25, 0])
        self.at("guidepost cells called")
        self.play(FadeIn(cx), Indicate(posts[0], color=YELLOW, scale_factor=1.4), run_time=0.7)
        trail = VGroup()
        self.at("growth cones touch")
        walk(self, gcs, 0, 1, 0.9, trail)
        self.play(Indicate(posts[0], color=YELLOW, scale_factor=1.3), run_time=0.6)
        # start again, before the growth cones arrive
        self.at("Bentley and")
        back = [g.animate.move_to(P[0] + o) for g, o in zip(gcs, OFFS)]
        self.play(FadeOut(trail), *back, run_time=0.8)
        q = T("?", 44, TEXT, weight=BOLD).next_to(posts[0], UP, buff=0.2)
        self.at("need them")
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        beam = Line([-3.5, 3.2, 0], P[1] + UP * 0.3, color=TEXT, stroke_width=9)
        bl = T("focused light", 24, TEXT).next_to(beam.get_start(), RIGHT, buff=0.2)
        self.at("focused light")
        self.play(Create(beam), FadeIn(bl), FadeOut(q), run_time=0.5)
        x = cross(1)
        self.play(Flash(P[1], color=TEXT, flash_radius=0.7), FadeOut(posts[0]), Create(x),
                  cx[0].animate.set_stroke(RED).set_fill(RED, 0.16), cx[1].animate.set_color(RED), run_time=0.6)
        self.play(FadeOut(beam), FadeOut(bl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lost(SpokenScene):
    def construct(self):
        tb = tube()
        c = cns()
        legs = VGroup(*[leg(i) for i in range(4)])
        posts = VGroup(post(2), post(3))
        x = cross(1)
        cx = chip("Cx1 cells", RED, size=24).move_to([-1.95, 0.25, 0])
        gcs = pioneers(0)
        ti = chip("Ti1", BLUE, size=24).move_to([-5.75, -1.45, 0])
        self.add(tb, c, legs, posts, x, cx, gcs, ti)
        trail = VGroup()
        self.at("failed to take")
        walk(self, gcs, 0, 1, 1.0, trail)
        ends = [np.array(p + [0.0]) for p in ([-4.9, 1.0], [-4.1, 2.1], [-3.0, 2.2], [-2.0, 1.5])]
        brs = VGroup(*[ArcBetweenPoints(P[1] + [0, 0.15, 0], e, angle=0.5 * (-1) ** k, color=RED, stroke_width=5)
                       for k, e in enumerate(ends)])
        self.at("abnormal directions")
        self.play(LaggedStart(*[Create(b) for b in brs], lag_ratio=0.25), run_time=1.5)
        need = T("needed at this turn", 30, YELLOW).move_to([3.4, -0.5, 0])
        self.at("that cell is needed")
        self.play(FadeIn(need, shift=DOWN * 0.15), run_time=0.5)
        ad = chip("adhesion?", GREY, size=26).move_to([2.5, -1.6, 0])
        sg = chip("a signal?", GREY, size=26).move_to([5.0, -1.6, 0])
        self.at("adhesion")
        self.play(FadeIn(ad, scale=0.8), run_time=0.5)
        self.at("or a signal")
        self.play(FadeIn(sg, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05More(SpokenScene):
    def construct(self):
        tb = tube()
        c = cns()
        legs = VGroup(*[leg(i) for i in range(4)])
        posts = VGroup(post(1, cluster=True), post(2), post(3))
        gcs = pioneers(4)
        ax = VGroup(*[VMobject().set_points_as_corners([P[i] + o for i in range(5)]).set_stroke(BLUE, 5)
                      for o in OFFS]).set_z_index(2)
        self.add(tb, c, ax, gcs)
        self.at("several legs")
        self.play(LaggedStart(*[Create(l) for l in legs], lag_ratio=0.4), run_time=1.5)
        self.at("partly from guideposts")
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in posts], lag_ratio=0.25), run_time=0.8)
        bars = VGroup()
        for i in (0, 3):
            m = (P[i] + P[i + 1]) / 2
            d = P[i + 1] - P[i]
            n = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
            bars.add(Line(m - n * 0.65, m + n * 0.65, color=GREY, stroke_width=9))
        bl = T("tissue boundaries", 24, GREY).move_to([4.3, 0.3, 0])
        self.at("boundaries")
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.4), FadeIn(bl), run_time=1.0)
        self.at("one important cue")
        self.play(Indicate(posts[0], color=YELLOW, scale_factor=1.5), run_time=0.9)
        pl = T("pioneers", 24, BLUE).move_to([-5.5, -3.3, 0])
        self.add(pl)
        fol = VGroup(*[VMobject().set_points_as_corners([P[i] + [0, dy, 0] for i in range(5)]).set_stroke(PURPLE, 4)
                       for dy in (-0.3, -0.44, -0.58)]).set_z_index(2)
        fl = T("followers", 24, PURPLE).move_to([-3.0, -3.2, 0])
        self.at("called followers")
        self.play(*[Create(f) for f in fol], FadeIn(fl), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        tb = tube()
        c = cns()
        posts = VGroup(post(1, cluster=True), post(2), post(3))
        near = VGroup(*[Line(P[0] + o, P[1] + o, color=BLUE, stroke_width=5) for o in OFFS]).set_z_index(2)
        far = VGroup(*[VMobject().set_points_as_corners([P[i] + o for i in range(1, 5)]).set_stroke(BLUE, 5)
                       for o in OFFS]).set_z_index(2)
        gcs = pioneers(4)
        self.add(tb, c, near, far, gcs, posts)
        path = VMobject().set_points_as_corners(P).set_stroke(YELLOW, 10).set_z_index(2)
        self.at("steer a whole")
        self.play(ShowPassingFlash(path, time_width=0.6), run_time=2.2)
        legs = VGroup(*[leg(i) for i in range(4)])
        self.at("one stretch at a time")
        self.play(LaggedStart(*[Create(l) for l in legs], lag_ratio=0.7), run_time=2.2)
        self.at("other cells")
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.4) for p in posts], run_time=0.9)
        x = cross(1)
        self.at("remove one")
        self.play(FadeOut(posts[0]), Create(x), run_time=0.6)
        ends = [np.array(p + [0.0]) for p in ([-4.9, 1.0], [-4.1, 2.1], [-3.0, 2.2], [-2.0, 1.5])]
        brs = VGroup(*[ArcBetweenPoints(P[1] + [0, 0.15, 0], e, angle=0.5 * (-1) ** k, color=RED, stroke_width=5)
                       for k, e in enumerate(ends)])
        stuck = pioneers(1)
        self.at("lose their normal")
        self.play(FadeOut(far), FadeOut(gcs), FadeOut(legs[1:]), FadeIn(stuck),
                  LaggedStart(*[Create(b) for b in brs], lag_ratio=0.2), run_time=1.2)
        rule = T("a long route, in short legs", 36, GOLD, font=TITLE_FONT).move_to([-2.4, 3.05, 0])
        self.at("Keep this rule")
        self.play(FadeIn(rule, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A long route is steered in short legs."
