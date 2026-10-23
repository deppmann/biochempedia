"""Daily and seasonal rhythms: how living things keep time  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light and day length (the light cue)
  INDIGO = darkness / night
  BLUE   = temperature (cold nights, warming climate)
  GREEN  = plants and plant growth
  ORANGE = animals and their responses (monarch, owl, squirrel, groundhog)
  GOLD   = a vocabulary word (the label that appears as the word is spoken)
  RED    = crossed out / "not"
  GREY   = outlines, structure, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

INDIGO = "#8E8CF2"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def vocab(text, size=32):
    """A vocabulary label: gold chip with bold text."""
    label = T(text, size=size, color=GOLD, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 0.5, height=label.height + 0.4,
                           stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.14)
    return VGroup(box, label.move_to(box))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def monarch(scale=1.0):
    """A schematic butterfly: four wing ellipses and a body bar."""
    def wing(w, h, ang, dx, dy):
        return Ellipse(width=w, height=h, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                       fill_opacity=0.45).rotate(ang).shift([dx, dy, 0])
    parts = [wing(0.8, 0.5, 0.5, -0.45, 0.22), wing(0.8, 0.5, -0.5, 0.45, 0.22),
             wing(0.55, 0.38, -0.4, -0.35, -0.2), wing(0.55, 0.38, 0.4, 0.35, -0.2),
             RoundedRectangle(corner_radius=0.05, width=0.1, height=0.9, stroke_width=0, fill_color=TEXT,
                              fill_opacity=1)]
    return VGroup(*parts).scale(scale)


def tree(scale=1.0):
    trunk = Rectangle(width=0.3, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                      fill_opacity=0.35).shift(DOWN * 0.55)
    crown = Circle(radius=0.75, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                   fill_opacity=0.4).shift(UP * 0.5)
    bl = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color="#F7A8C8", fill_opacity=0.95).move_to(
        [0.5 * np.cos(a) * r, 0.5 + 0.5 * np.sin(a) * r, 0]) for a, r in
        [(0.4, 1), (1.5, 0.8), (2.6, 1), (3.7, 0.75), (4.7, 1), (5.7, 0.8), (1.0, 0.3), (3.0, 0.25), (5.0, 0.3)]])
    return VGroup(trunk, crown, bl).scale(scale)


def cross(mob, color=RED, pad=0.15):
    w, h = mob.width / 2 + pad, mob.height / 2 + pad
    c = mob.get_center()
    return VGroup(Line(c + [-w, h, 0], c + [w, -h, 0], color=color, stroke_width=7),
                  Line(c + [-w, -h, 0], c + [w, h, 0], color=color, stroke_width=7))


def calendar_icon():
    body = RoundedRectangle(corner_radius=0.1, width=1.5, height=1.3, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.12)
    bar = Rectangle(width=1.5, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to(
        body.get_top() + DOWN * 0.15)
    cells = VGroup(*[Square(0.2, stroke_color=GREY, stroke_width=2).move_to(body.get_center() + [(i - 1) * 0.38, -(j - 0.2) * 0.3 - 0.05, 0])
                     for i in range(3) for j in range(2)])
    return VGroup(body, bar, cells)


def eye_icon():
    e = Ellipse(width=1.3, height=0.65, stroke_color=GREY, stroke_width=4)
    p = Circle(radius=0.19, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.5)
    return VGroup(e, p)


def bar_track(w, color, frac=1.0, h=0.32):
    track = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                             fill_opacity=0)
    fill = RoundedRectangle(corner_radius=0.1, width=max(0.12, w * frac), height=h, stroke_width=0,
                            fill_color=color, fill_opacity=0.85)
    fill.align_to(track, LEFT)
    return track, fill


class S00Title(TitleCard):
    LESSON = "Daily and seasonal rhythms"
    TITLE = "How Living Things Keep Time"


# ---------------------------------------------------------------------------------------------
class S01Calendar(SpokenScene):
    def construct(self):
        mon = monarch(1.7).move_to([-3.8, 0.6, 0])
        tr = tree(1.4).move_to([3.8, 0.7, 0])
        cal = calendar_icon().scale(1.0).move_to([-3.8, 3.0, 0])
        cal_l = T("calendar", 24, GREY).next_to(cal, RIGHT, buff=0.25)
        eye = eye_icon().move_to([3.8, 3.05, 0])
        eye_l = T("eyes", 24, GREY).next_to(eye, RIGHT, buff=0.25)
        c1 = chip("Fall: monarchs fly south", ORANGE, size=26).move_to([-3.6, -1.6, 0])
        c2 = chip("Spring: cherry trees bloom", GREEN, size=26).move_to([3.6, -1.6, 0])
        self.at("Every fall")
        self.play(FadeIn(mon, shift=DOWN * 0.3), run_time=0.7)
        self.play(FadeIn(c1), run_time=0.5)
        self.play(mon.animate.shift(DOWN * 0.25), run_time=1.2)
        self.at("Every spring")
        self.play(FadeIn(tr, scale=0.9), run_time=0.7)
        self.play(FadeIn(c2), run_time=0.5)
        self.at("no calendar")
        self.play(FadeIn(cal), FadeIn(cal_l), run_time=0.5)
        x1 = cross(cal)
        self.play(Create(x1), run_time=0.5)
        self.at("no eyes")
        self.play(FadeIn(eye), FadeIn(eye_l), run_time=0.5)
        x2 = cross(eye)
        self.play(Create(x2), run_time=0.5)
        self.at("how do plants")
        q = T("How do they know?", 50, TEXT, font=TITLE_FONT).move_to([0, -2.85, 0])
        self.play(Write(q), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Day(SpokenScene):
    def construct(self):
        X0, SEG, Y = -3.9, 2.5, 1.0
        segs = []
        for i in range(4):
            day = (i % 2 == 0)
            col = YELLOW if day else INDIGO
            r = Rectangle(width=SEG, height=0.9, stroke_color=col, stroke_width=2, fill_color=col,
                          fill_opacity=0.28 if day else 0.38).move_to([X0 + SEG * (i + 0.5), Y, 0])
            lab = T("light" if day else "dark", 24, col).move_to(r)
            segs.append(VGroup(r, lab))
        self.at("Start with one day")
        self.play(FadeIn(segs[0]), run_time=0.5)
        self.play(FadeIn(segs[1]), run_time=0.5)
        self.at("circadian rhythm")
        voc = vocab("circadian rhythm", 34).move_to([0, 3.05, 0])
        self.play(FadeIn(voc, scale=0.9), run_time=0.6)
        self.at("repeats about")
        self.play(FadeIn(segs[2]), FadeIn(segs[3]), run_time=0.7)
        L = X0 + 0.05
        R = X0 + 2 * SEG - 0.05
        yb = Y + 0.65
        br = VGroup(Line([L, yb, 0], [R, yb, 0], color=TEXT, stroke_width=3),
                    Line([L, yb - 0.15, 0], [L, yb, 0], color=TEXT, stroke_width=3),
                    Line([R, yb - 0.15, 0], [R, yb, 0], color=TEXT, stroke_width=3))
        bl = T("about every 24 hours", 26, TEXT).next_to(br, UP, buff=0.12)
        self.play(Create(br), FadeIn(bl), run_time=0.8)
        self.at("Light and darkness")
        self.play(Indicate(segs[0], color=YELLOW, scale_factor=1.08), Indicate(segs[1], color=INDIGO, scale_factor=1.08),
                  run_time=1.0)
        # owl row and squirrel row
        yo, ys = -0.5, -1.8
        owl_l = T("owl", 28, ORANGE).move_to([-5.3, yo, 0])
        sq_l = T("tree squirrel", 24, ORANGE).move_to([-5.0, ys, 0])
        track_o = Line([X0, yo - 0.4, 0], [X0 + 4 * SEG, yo - 0.4, 0], color=GREY, stroke_width=1.5)
        track_s = Line([X0, ys - 0.4, 0], [X0 + 4 * SEG, ys - 0.4, 0], color=GREY, stroke_width=1.5)
        owl_blocks = VGroup(*[Rectangle(width=SEG - 0.3, height=0.7, stroke_color=ORANGE, stroke_width=2,
                                        fill_color=ORANGE, fill_opacity=0.75).move_to([X0 + SEG * (i + 0.5), yo, 0])
                              for i in (1, 3)])
        sq_blocks = VGroup(*[Rectangle(width=SEG - 0.3, height=0.7, stroke_color=ORANGE, stroke_width=2,
                                       fill_color=ORANGE, fill_opacity=0.75).move_to([X0 + SEG * (i + 0.5), ys, 0])
                             for i in (0, 2)])
        self.at("Many owls")
        self.play(FadeIn(owl_l), Create(track_o), run_time=0.5)
        self.play(FadeIn(owl_blocks[0], scale=0.6), run_time=0.5)
        self.play(FadeIn(owl_blocks[1], scale=0.6), run_time=0.5)
        self.at("rest in the day")
        rest = T("rest", 24, GREY).move_to([X0 + SEG * 0.5, yo, 0])
        self.play(FadeIn(rest), run_time=0.4)
        self.at("Tree squirrels")
        self.play(FadeIn(sq_l), Create(track_s), run_time=0.5)
        self.play(FadeIn(sq_blocks[0], scale=0.6), run_time=0.5)
        self.play(FadeIn(sq_blocks[1], scale=0.6), run_time=0.5)
        self.at("In many animals")
        # steady darkness: every light segment turns dark, squirrel row fades, owl row keeps its beat
        new_segs = []
        anims = []
        for i in (0, 2):
            r = Rectangle(width=SEG, height=0.9, stroke_color=INDIGO, stroke_width=2, fill_color=INDIGO,
                          fill_opacity=0.38).move_to(segs[i][0])
            lab = T("dark", 24, INDIGO).move_to(r)
            anims += [Transform(segs[i][0], r), Transform(segs[i][1], lab)]
        self.play(*anims, FadeOut(sq_blocks), FadeOut(sq_l), FadeOut(track_s), FadeOut(rest), run_time=1.0)
        an_l = T("another animal", 21, ORANGE).move_to([-5.3, ys, 0])
        track_a = Line([X0, ys - 0.4, 0], [X0 + 4 * SEG, ys - 0.4, 0], color=GREY, stroke_width=1.5)
        an_blocks = VGroup(*[Rectangle(width=SEG - 0.3, height=0.7, stroke_color=ORANGE, stroke_width=2,
                                       fill_color=ORANGE, fill_opacity=0.75).move_to([X0 + SEG * (i + 0.5), ys, 0])
                             for i in (0, 2)])
        ex_l = T("one example", 20, GREY).next_to(owl_l, DOWN, buff=0.08)
        self.play(FadeIn(an_l), Create(track_a), FadeIn(an_blocks, scale=0.6), FadeIn(ex_l), run_time=0.8)
        self.play(FadeOut(br), FadeOut(bl), run_time=0.3)
        st = T("steady darkness", 28, INDIGO).move_to([X0 + 2 * SEG, 2.2, 0])
        self.play(FadeIn(st), run_time=0.5)
        self.play(Indicate(VGroup(owl_blocks, an_blocks), color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.at("inside the body")
        body = chip("part of the timing comes from inside the body", TEAL, size=26).move_to([0.5, -3.0, 0])
        self.play(FadeIn(body, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bend(SpokenScene):
    N, ELL, W = 6, 0.85, 1.6
    X0, Y0 = -1.4, -3.3

    def stem(self, k):
        k = max(k, 1e-4)
        R = 1.0 / k
        cells = VGroup()
        for i in range(self.N):
            s0, s1 = i * self.ELL, (i + 1) * self.ELL
            def cp(s, side):
                a = k * s
                cx = self.X0 + R * (1 - np.cos(a))
                cy = self.Y0 + R * np.sin(a)
                nx, ny = -np.cos(a), np.sin(a)  # left normal
                return np.array([cx + side * nx, cy + side * ny, 0])
            hw = self.W / 2
            left = [cp(s0, hw), cp(s1, hw), cp(s1, 0), cp(s0, 0)]
            right = [cp(s0, 0), cp(s1, 0), cp(s1, -hw), cp(s0, -hw)]
            cells.add(Polygon(*left, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.32))
            cells.add(Polygon(*right, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN, fill_opacity=0.18))
        return cells

    def construct(self):
        kt = ValueTracker(0.0)
        st = always_redraw(lambda: self.stem(kt.get_value()))
        self.at("Plants respond too")
        self.play(FadeIn(st), run_time=0.8)
        self.at("plant growth")
        voc = vocab("tropism", 34).move_to([-4.3, 3.0, 0])
        self.play(FadeIn(voc, scale=0.9), run_time=0.6)
        self.at("Light shines")
        arrows = VGroup(*[arr([6.3, y, 0], [4.3, y, 0], YELLOW, w=7, tip=0.3) for y in (-0.8, 0.4, 1.6)])
        lt = T("light", 30, YELLOW).move_to([5.3, 2.4, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), FadeIn(lt), run_time=1.2)
        self.at("shaded side")
        sh = T("shaded side", 28, TEXT).move_to([-5.0, -1.6, 0])
        sh_a = arr([-3.85, -1.6, 0], [-2.35, -1.6, 0], TEXT, w=4, tip=0.18)
        self.play(FadeIn(sh), GrowArrow(sh_a), run_time=0.6)
        self.at("grow longer")
        lg = T("longer cells", 28, GREEN, weight=BOLD).move_to([-5.0, -2.2, 0])
        d1 = max(0.8, self.t_of("lit side") - self.t_of("grow longer") - 0.2)
        self.play(kt.animate.set_value(0.12), FadeIn(lg), run_time=d1, rate_func=linear)
        self.at("lit side")
        lit = T("lit side", 28, TEXT).move_to([1.5, -2.6, 0])
        lit_a = arr([0.55, -2.6, 0], [-0.55, -2.6, 0], TEXT, w=4, tip=0.18)
        self.play(FadeIn(lit), GrowArrow(lit_a), run_time=0.5)
        self.at("The longer side")
        d2 = max(0.8, self.t_of("bend toward the light") - self.t_of("The longer side"))
        self.play(kt.animate.set_value(0.22), run_time=d2, rate_func=smooth)
        self.at("bend toward the light")
        self.play(Indicate(st, color=GREEN, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Season(SpokenScene):
    def construct(self):
        PX, PW, PY, PH = [-4.2, 0.0, 4.2], 3.85, -1.8, 3.4
        TOPY = PY + PH / 2 - 0.55
        head = T("Fall and winter in Virginia", 40, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.at("Now think about")
        self.play(Write(head), run_time=1.0)
        c_day = chip("short days", YELLOW, size=26).move_to([PX[0], 2.0, 0])
        c_cold = chip("cold nights", BLUE, size=26).move_to([PX[1], 2.0, 0])
        c_food = chip("food hard to find", GREY, size=26).move_to([PX[2], 2.0, 0])
        self.at("Days are short")
        self.play(FadeIn(c_day, shift=DOWN * 0.2), run_time=0.5)
        self.at("nights are cold")
        self.play(FadeIn(c_cold, shift=DOWN * 0.2), run_time=0.5)
        self.at("hard to find")
        self.play(FadeIn(c_food, shift=DOWN * 0.2), run_time=0.5)
        # cues -> responses
        self.at("Cues like")
        rail = Line([PX[0], 1.05, 0], [PX[2], 1.05, 0], color=GREY, stroke_width=4)
        drops = VGroup(*[arr([x, 1.05, 0], [x, 0.3, 0], GREY, w=4, tip=0.18) for x in PX])
        s1 = Line([PX[0], 1.5, 0], [PX[0], 1.05, 0], color=YELLOW, stroke_width=5)
        s2 = Line([PX[1], 1.5, 0], [PX[1], 1.05, 0], color=BLUE, stroke_width=5)
        cue_l = T("cues", 26, TEXT).move_to([PX[2], 1.05 + 0.0, 0])
        self.play(Create(s1), Create(s2), run_time=0.5)
        self.play(Create(rail), FadeOut(c_food), FadeIn(cue_l.set_x(2.3).set_y(1.45)), run_time=0.6)
        self.play(*[GrowArrow(d) for d in drops], run_time=0.6)
        panels = [RoundedRectangle(corner_radius=0.18, width=PW, height=PH, stroke_color=GREY, stroke_width=2.5,
                                   fill_opacity=0).move_to([x, PY, 0]) for x in PX]
        self.play(*[Create(p) for p in panels], run_time=0.6)
        # --- panel 1: migration
        self.at("Monarchs migrate")
        va = chip("Virginia", GREY, size=24).move_to([PX[0], -1.4, 0])
        so = chip("south", GREY, size=24).move_to([PX[0], -3.05, 0])
        down = arr([PX[0] - 0.9, -1.8, 0], [PX[0] - 0.9, -2.65, 0], ORANGE, w=6, tip=0.25)
        mon = monarch(0.5).move_to([PX[0] + 0.95, -1.95, 0])
        self.play(FadeIn(va), FadeIn(so), FadeIn(mon), run_time=0.5)
        self.at("south in fall")
        self.play(GrowArrow(down), mon.animate.move_to([PX[0] + 0.95, -2.55, 0]), run_time=1.3)
        self.at("Migration is")
        v1 = vocab("migration", 28).move_to([PX[0], TOPY, 0])
        self.play(FadeIn(v1, scale=0.9), run_time=0.5)
        self.at("and back")
        up = DashedLine([PX[0] - 0.55, -2.65, 0], [PX[0] - 0.55, -1.9, 0], color=ORANGE, stroke_width=5,
                        dash_length=0.18)
        up_t = arr([PX[0] - 0.55, -2.15, 0], [PX[0] - 0.55, -1.8, 0], ORANGE, w=5, tip=0.22)
        sm = VGroup(*[monarch(0.2).move_to([PX[0] + 0.6 + 0.0 * k, y, 0]) for k, y in enumerate([-2.5, -2.25, -2.0])])
        sm.arrange(RIGHT, buff=0.1).move_to([PX[0] + 0.7, -1.95, 0])
        back_l = VGroup(T("and back, over", 18, ORANGE), T("several generations", 18, ORANGE)).arrange(
            DOWN, buff=0.05).move_to([PX[0] + 0.7, -2.4, 0])
        self.play(Create(up), FadeIn(up_t), FadeOut(mon), FadeIn(sm, shift=UP * 0.3), FadeIn(back_l), run_time=1.0)
        # --- panel 2: dormancy
        self.at("Dormancy is")
        v2 = vocab("dormancy", 28).move_to([PX[1], TOPY, 0])
        self.play(FadeIn(v2, scale=0.9), run_time=0.5)
        g_l = T("growth", 26, GREEN).move_to([PX[1], -1.45, 0])
        tr_, fl_ = bar_track(2.8, GREEN, 1.0)
        VGroup(tr_, fl_).move_to([PX[1], -2.0, 0])
        fl_.align_to(tr_, LEFT)
        self.play(FadeIn(g_l), Create(tr_), FadeIn(fl_), run_time=0.5)
        self.at("Growth slows")
        small = fl_.copy().stretch_to_fit_width(0.14).align_to(tr_, LEFT)
        self.play(Transform(fl_, small), run_time=1.5)
        self.at("stays alive")
        alive = chip("still alive", GREEN, size=26).move_to([PX[1], -2.95, 0])
        self.play(FadeIn(alive, shift=UP * 0.2), run_time=0.6)
        # --- panel 3: hibernation
        self.at("Hibernation is")
        v3 = vocab("hibernation", 28).move_to([PX[2], TOPY, 0])
        self.play(FadeIn(v3, scale=0.9), run_time=0.5)
        self.at("dormancy in animals")
        link = arr([PX[1] + 1.25, TOPY, 0], [PX[2] - 1.5, TOPY, 0], GOLD, w=5, tip=0.2)
        self.play(GrowArrow(link), run_time=0.6)
        t_l = T("body temperature", 25, ORANGE).move_to([PX[2], -1.45, 0])
        tr2, fl2 = bar_track(2.8, ORANGE, 1.0)
        VGroup(tr2, fl2).move_to([PX[2], -2.0, 0])
        fl2.align_to(tr2, LEFT)
        self.play(FadeIn(t_l), Create(tr2), FadeIn(fl2), run_time=0.5)
        self.at("body temperature drops")
        small2 = fl2.copy().stretch_to_fit_width(1.0).align_to(tr2, LEFT)
        self.play(Transform(fl2, small2), run_time=1.5)
        self.at("less stored fat")
        fat = chip("less stored fat used", ORANGE, size=23).move_to([PX[2], -2.95, 0])
        self.play(FadeIn(fat, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Instinct(SpokenScene):
    def construct(self):
        self.at("Are these behaviors learned")
        q = T("Learned?", 60, TEXT, font=TITLE_FONT).move_to([0, 2.9, 0])
        self.play(Write(q), run_time=1.0)
        self.at("Mostly not")
        strike = Line(q.get_left() + LEFT * 0.15, q.get_right() + RIGHT * 0.15, color=RED, stroke_width=7)
        mn = T("mostly not", 30, RED).next_to(q, RIGHT, buff=0.5)
        self.play(Create(strike), FadeIn(mn), run_time=0.8)
        self.at("An instinct")
        voc = vocab("instinct", 54).move_to([0, 1.1, 0])
        self.play(FadeIn(voc, scale=0.9), run_time=0.7)
        self.at("inherits")
        a1 = chip("inherited", GREY, size=32).move_to([-3.0, -0.4, 0])
        a2 = chip("without being taught", GREY, size=32).move_to([2.9, -0.4, 0])
        l1 = Line(voc.get_bottom() + LEFT * 0.4, a1.get_top(), color=GREY, stroke_width=3)
        l2 = Line(voc.get_bottom() + RIGHT * 0.4, a2.get_top(), color=GREY, stroke_width=3)
        self.play(Create(l1), FadeIn(a1), run_time=0.6)
        self.at("without being taught")
        self.play(Create(l2), FadeIn(a2), run_time=0.6)
        self.at("A monarch flying south")
        mon = monarch(1.1).move_to([-3.4, -1.9, 0])
        south = chip("south", GREY, size=28).move_to([-3.4, -3.2, 0])
        dn = arr([-3.4, -2.55, 0], [-3.4, -2.9, 0], ORANGE, w=6, tip=0.2)
        self.play(FadeIn(mon), run_time=0.4)
        self.play(GrowArrow(dn), FadeIn(south), mon.animate.shift(DOWN * 0.15), run_time=1.0)
        self.at("never made the trip")
        nm = chip("never made this trip before", ORANGE, size=32).move_to([1.9, -2.3, 0])
        self.play(FadeIn(nm, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        self.at("So how do they know")
        q = T("How do they know?", 44, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(q), run_time=1.0)
        self.at("such as light")
        XS = [-4.3, 0.0, 4.3]
        c1 = chip("light", YELLOW, size=28).move_to([XS[0], 1.5, 0])
        c2 = chip("day length", YELLOW, size=28).move_to([XS[1], 1.5, 0])
        c3 = chip("temperature", BLUE, size=28).move_to([XS[2], 1.5, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.5)
        self.at("day length")
        self.play(FadeIn(c2, shift=DOWN * 0.2), run_time=0.5)
        self.at("temperature")
        self.play(FadeIn(c3, shift=DOWN * 0.2), run_time=0.5)
        cue_t = T("cues", 26, GREY).move_to([-0.0, 2.3, 0])
        rail = Line([XS[0], 0.75, 0], [XS[2], 0.75, 0], color=GREY, stroke_width=4)
        stems = VGroup(*[Line([x, 1.1, 0], [x, 0.75, 0], color=GREY, stroke_width=4) for x in XS])
        down = arr([0, 0.75, 0], [0, 0.1, 0], GREY, w=5, tip=0.22)
        resp = chip("responses of living things", TEXT, size=30).move_to([-1.9, -0.45, 0])
        self.play(Create(stems), Create(rail), GrowArrow(down), run_time=0.7)
        self.play(FadeIn(resp), run_time=0.5)
        self.at("inherited instincts")
        inst = vocab("many are instincts", 28).move_to([3.7, -0.45, 0])
        lk = arr([resp.get_right()[0] + 0.05, -0.45, 0], [inst.get_left()[0] - 0.05, -0.45, 0], GOLD, w=4, tip=0.18)
        self.play(GrowArrow(lk), FadeIn(inst, scale=0.9), run_time=0.7)
        # years timeline
        self.at("last for many years")
        ax = Arrow([-5.8, -2.55, 0], [5.8, -2.55, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        yl = T("many years", 26, GREY).move_to([4.4, -3.0, 0])
        mk = Rectangle(width=0.35, height=0.6, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                       fill_opacity=0.6).move_to([-0.7, -2.15, 0])
        mk_l = T("timing of a response", 24, ORANGE).move_to([-3.8, -3.05, 0])
        self.play(Create(ax), FadeIn(yl), FadeIn(mk), FadeIn(mk_l), run_time=0.8)
        self.at("warming climate")
        wc = chip("a warming climate", BLUE, size=26).move_to([-3.5, -1.55, 0])
        wa = arr([-1.8, -1.7, 0], [-1.0, -2.0, 0], BLUE, w=4, tip=0.2)
        self.play(FadeIn(wc, shift=DOWN * 0.15), GrowArrow(wa), run_time=0.6)
        self.at("can shift")
        self.play(mk.animate.shift(RIGHT * 1.2), run_time=0.9)
        self.play(mk.animate.shift(LEFT * 2.1), run_time=1.1)
        sh = T("timing can shift", 28, TEXT, weight=BOLD).move_to([3.0, -1.6, 0])
        sh2 = T("earlier or later", 22, GREY).move_to([3.0, -2.05, 0])
        self.play(FadeIn(sh), FadeIn(sh2), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Living things respond to cues like light, day length and temperature."
