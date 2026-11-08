"""Reelin and the reeler mouse, chapter 3: Needed, But What Does It Say?  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, same in every chapter)
  ORANGE = the first-born neurons (the first thin sheet)
  BLUE   = the next-born neurons
  GREEN  = the last-born neurons (the later-born neuron we follow)
  YELLOW = Reelin and the place it is made (a band, a spot, a bath)
  TEAL   = the two receptors (not used in this chapter)
  PURPLE = Dab1, the adaptor
  PINK   = the Src-family kinases (not used in this chapter)
  GOLD   = a phosphate group (not used in this chapter)
  RED    = a problem: a stop, a cross, a missing or failed result
  GREY   = tissue, membranes, the radial glial fiber, outlines, labels
  TEXT   = cards, arrows, ticks and neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403
import os
from pathlib import Path

# Keep pipeline scratch files outside the chapter deliverables.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E8789F"

# ---------------------------------------------------------------- layout of the cortex, as in the earlier film
SL_W, SL_H = 4.4, 5.7
DR = 0.17
LA = [-1.8, -1.08, -0.36, 0.36, 1.08, 1.8]
LB = [-1.44, -0.72, 0.0, 0.72, 1.44]
LSUB = [-1.44, 0.0, 1.44]
Y_CR, Y_LATE, Y_EARLY, Y_SUB = 2.58, 1.45, 0.35, -0.8


def lab(text, color=GREY, size=26):
    return T(text, size, color)


def left_at(mob, x, y):
    """Move a mobject so its left edge is at x and its centre at y."""
    return mob.move_to([x, y, 0]).align_to([x, 0, 0], LEFT)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def tick(center, size=0.28, color=TEXT, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -0.02, 0], c + [-size * 0.3, -size * 0.8, 0], color=color, stroke_width=w),
                  Line(c + [-size * 0.3, -size * 0.8, 0], c + [size, size * 0.9, 0], color=color, stroke_width=w))


def dot_neuron(x, y, color, r=DR):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.65).move_to([x, y, 0])


# ---------------------------------------------------------------- cortex pieces scaled by k
def rows(cx, cy, k, state, seed=0):
    """(orange, blue, green) groups. state: 'reeler' (scattered, inverted) or 'normal'.
    The orange group always holds six neurons: even indexes can go to the top, odd ones to the subplate row."""
    r = max(DR * k, 0.11)

    def N(x, y, c):
        return dot_neuron(cx + x * k, cy + y * k, c, r)

    if state == "normal":
        o = VGroup(*[N(LA[i], Y_CR, ORANGE) if i % 2 == 0 else N(LSUB[(i - 1) // 2], Y_SUB, ORANGE) for i in range(6)])
        b = VGroup(*[N(x, Y_EARLY, BLUE) for x in LB])
        g = VGroup(*[N(x, Y_LATE, GREEN) for x in LA])
    elif state == "tidy":   # more organised, still a little loose
        rng = np.random.RandomState(seed + 5)
        j = lambda: rng.uniform(-0.1, 0.1)
        o = VGroup(*[N(LA[i] + j(), Y_CR + j(), ORANGE) if i % 2 == 0 else N(LSUB[(i - 1) // 2] + j(), Y_SUB + j(), ORANGE) for i in range(6)])
        b = VGroup(*[N(x + j(), Y_EARLY + j(), BLUE) for x in LB])
        g = VGroup(*[N(x + j(), Y_LATE + j(), GREEN) for x in LA])
    else:
        def dis(y, color, lanes):
            rng = np.random.RandomState(int((y + 4) * 100) + seed)
            return VGroup(*[N(x + rng.uniform(-.12, .12), y + rng.uniform(-.42, .42), color) for x in lanes])
        o, b, g = dis(2.1, ORANGE, LA), dis(1.1, BLUE, LB), dis(-0.1, GREEN, LA)
    return o, b, g


def body(cx, cy, k, idx=0):
    """Tissue outline plus ventricular band. idx 3 (bath) keeps the slice interior clear of yellow."""
    fill = "#181A21" if idx == 3 else GREY
    rect = Rectangle(width=SL_W * k, height=SL_H * k, stroke_color=GREY, stroke_width=3,
                     fill_color=fill, fill_opacity=1 if idx == 3 else 0.07).move_to([cx, cy, 0])
    vz = Rectangle(width=SL_W * k, height=0.55 * k, stroke_width=0, fill_color=GREY, fill_opacity=0.22
                   ).move_to([cx, cy - SL_H * k / 2 + 0.275 * k, 0])
    g = VGroup(rect, vz)
    g.set_z_index(1 if idx == 3 else 0)
    return g


def source(idx, cx, cy, k):
    """Where the Reelin is made: 1 = band below the cortex, 2 = one small patch, 3 = bath around the slice."""
    if idx == 1:
        s = Rectangle(width=SL_W * k, height=0.55 * k, stroke_width=0, fill_color=YELLOW, fill_opacity=0.5
                      ).move_to([cx, cy - SL_H * k / 2 + 0.275 * k, 0])
        s.set_z_index(2)
    elif idx == 2:
        s = Circle(radius=0.26 * k, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9
                   ).move_to([cx, cy + 0.5 * k, 0])
        s.set_z_index(2)
    else:
        s = RoundedRectangle(corner_radius=0.2, width=SL_W * k + 1.0, height=SL_H * k + 1.0, stroke_color=YELLOW,
                             stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.2).move_to([cx, cy, 0])
        s.set_z_index(-1)
    return s


# small panels used in the overview scenes
PCX = (-4.7, 0.0, 4.7)
PCY, PK = -0.1, 0.75
PLAB = ("below the cortex", "one small spot", "medium bathing a slice")


def small_bodies():
    return [body(PCX[i], PCY, PK, i + 1) for i in range(3)]


def small_sources():
    return [source(i + 1, PCX[i], PCY, PK) for i in range(3)]


def small_labels(color=TEXT):
    return [lab(PLAB[i], color, 26).move_to([PCX[i], -3.3, 0]) for i in range(3)]


# big panel used in the result scenes
BCX, BCY, BK = -3.4, 0.0, 0.95
RX = -0.2    # left edge of the right-hand column


def legend(x=4.55, y0=-1.15, dy=0.6):
    g = VGroup()
    for i, (n, c) in enumerate((("first-born", ORANGE), ("next-born", BLUE), ("last-born", GREEN))):
        d = dot_neuron(x, y0 - i * dy, c, 0.13)
        t = left_at(lab(n, TEXT, 28), x + 0.25, y0 - i * dy)
        g.add(d, t)
    return g


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Reelin and the reeler mouse"
    TITLE = "Needed, But What Does It Say?"


class S01Q(SpokenScene):
    def construct(self):
        cx, cy, k = 3.5, 0.0, 0.95
        sl = body(cx, cy, k)
        nrm = VGroup(*rows(cx, cy, k, "normal"))
        reelin = chip("Reelin", YELLOW, 40).move_to([-3.6, 0.5, 0])
        link = arr([-2.2, 0.5, 0], [0.9, 0.5, 0], YELLOW, 10)
        key=VGroup(*[VGroup(dot_neuron(0,0,c,0.12),lab(n,TEXT,26)).arrange(RIGHT,buff=0.15) for n,c in [("first-born",ORANGE),("next-born",BLUE),("last-born",GREEN)]]).arrange(RIGHT,buff=0.5).move_to([2.4,-3.35,0])
        self.add(key)
        self.play(FadeIn(sl), FadeIn(nrm), FadeIn(reelin), GrowArrow(link), run_time=0.5)
        self.at("shows that")
        x = cross(reelin.get_center(), 0.5)
        rl = VGroup(*rows(cx, cy, k, "reeler"))
        self.play(Create(x), link.animate.set_color(TEXT).set_opacity(0.9), Transform(nrm, rl), run_time=0.9)
        self.at("needed")
        need = lab("needed", TEXT, 34).move_to([-3.6, -1.1, 0])
        self.play(FadeIn(need), run_time=0.5)
        self.at("can it show")
        bub = RoundedRectangle(corner_radius=0.3, width=1.5, height=1.1, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.08).move_to([-3.6, 2.2, 0])
        q = T("?", 52, TEXT, weight=BOLD).move_to(bub)
        tail = Polygon([-3.9, 1.68, 0], [-3.3, 1.68, 0], [-3.6, 1.25, 0], stroke_width=0, fill_color=TEXT, fill_opacity=0.08)
        self.play(FadeOut(x), FadeOut(need), FadeOut(link), FadeIn(bub), FadeIn(tail), FadeIn(q), run_time=0.6)
        self.at("what the signal says")
        says = lab("what it says", TEXT, 34).move_to([-3.6, -1.1, 0])
        self.play(FadeIn(says), run_time=0.5)
        self.finish()


class S02Fuel(SpokenScene):
    def construct(self):
        road_y = -0.8
        main = Line([-6.4, road_y, 0], [0.4, road_y, 0], stroke_width=34, color=GREY).set_stroke(opacity=0.35)
        up = VMobject(stroke_width=34, stroke_color=GREY, fill_opacity=0).set_points_as_corners([[0.4, road_y, 0], [2.4, 1.3, 0], [6.3, 1.3, 0]]).set_stroke(opacity=0.35)
        dn = VMobject(stroke_width=34, stroke_color=GREY, fill_opacity=0).set_points_as_corners([[0.4, road_y, 0], [2.4, -2.9, 0], [6.3, -2.9, 0]]).set_stroke(opacity=0.35)
        road = VGroup(main, up, dn)
        # the car: body, cabin, two wheels and a driver
        cab = Polygon([-0.55, 0.3, 0], [-0.3, 0.8, 0], [0.55, 0.8, 0], [0.8, 0.3, 0], stroke_color=TEXT, stroke_width=3,
                      fill_color=TEXT, fill_opacity=0.25)
        bod = RoundedRectangle(corner_radius=0.18, width=2.4, height=0.7, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.25).move_to([0, 0, 0])
        wheels = VGroup(*[Circle(radius=0.3, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([x, -0.35, 0]) for x in (-0.75, 0.75)])
        head = Circle(radius=0.17, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.9).move_to([0.1, 0.62, 0])
        car = VGroup(cab, bod, wheels, head).scale(1.35).move_to([-4.8, road_y + 0.6, 0])
        # the fuel gauge
        gc = np.array([-4.8, 2.0, 0.0])
        arc = Arc(radius=0.95, start_angle=0, angle=PI, stroke_color=YELLOW, stroke_width=6).move_to(gc + [0, 0.35, 0])
        base = Line(gc + [-0.95, 0, 0], gc + [0.95, 0, 0], stroke_color=YELLOW, stroke_width=4)
        needle = Line(gc, gc + [0.8 * np.cos(0.35), 0.8 * np.sin(0.35), 0], stroke_color=TEXT, stroke_width=6)
        # needle starts near full (angle small => pointing right = full)
        gauge = VGroup(arc, base, needle)
        glab = lab("fuel", YELLOW, 28).move_to(gc + [0, -0.42, 0])
        self.at("The fuel")
        self.play(FadeIn(road), FadeIn(car), FadeIn(gauge), FadeIn(glab), run_time=0.8)
        self.at("needed for the trip")
        needle2 = Line(gc, gc + [0.8 * np.cos(2.3), 0.8 * np.sin(2.3), 0], stroke_color=TEXT, stroke_width=6)
        self.play(car.animate.move_to([-0.9, road_y + 0.6, 0]), Transform(needle, needle2), run_time=1.5)
        self.at("does not choose")
        dash = DashedLine(gc + [0.9, -0.3, 0], [-0.6, -0.1, 0], color=YELLOW, stroke_width=4)
        no = cross([-2.5, 0.5, 0], 0.28)
        self.play(Create(dash), run_time=0.4)
        self.play(Create(no), run_time=0.3)
        self.at("where the car goes")
        pick = lab("driver chooses", TEXT, 30).move_to([2.5, 3.55, 0])
        self.play(FadeOut(dash), FadeOut(no), FadeIn(pick), car.animate.move_to([2.7, 2.28, 0]), run_time=0.7)
        self.play(car.animate.move_to([4.5, 2.28, 0]), run_time=0.5)
        self.finish()


def card_frame(cx, w=6.2, h=5.6, cy=-0.1):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])


class S03Words(SpokenScene):
    def construct(self):
        cA, cB = -3.4, 3.4
        fa, fb = card_frame(cA), card_frame(cB)
        ha = chip("permissive", TEXT, 36).move_to([cA, 2.0, 0])
        hb = chip("instructive", TEXT, 36).move_to([cB, 2.0, 0])
        self.at("permissive signal")
        sig = chip("signal", YELLOW, 28).move_to([cA - 1.9, 0.5, 0])
        gl = Line([cA - 0.55, 0.0, 0], [cA - 0.55, 1.0, 0], stroke_color=TEXT, stroke_width=8)
        gr = Line([cA + 0.15, 0.0, 0], [cA + 0.15, 1.0, 0], stroke_color=TEXT, stroke_width=8)
        gate = VGroup(gl, gr)
        out = chip("outcome", TEXT, 28).move_to([cA + 1.65, 0.5, 0])
        a1 = arr(sig.get_right(), [cA - 0.7, 0.5, 0], YELLOW, 5)
        self.play(FadeIn(fa), FadeIn(ha), FadeIn(sig), FadeIn(gate), GrowArrow(a1), run_time=0.8)
        other = chip("something else", TEXT, 28).move_to([cA, -1.0, 0])
        self.add(other)
        self.at("allows an outcome")
        a2 = arr([cA + 0.3, 0.5, 0], out.get_left(), TEXT, 5)
        self.play(gl.animate.shift(LEFT * 0.25), gr.animate.shift(RIGHT * 0.25), FadeIn(out), GrowArrow(a2), run_time=0.8)
        self.at("something else chooses")
        a3 = arr(other.get_top() + [0.8, 0, 0], out.get_bottom(), GREY, 5)
        self.play(FadeIn(other), GrowArrow(a3), run_time=0.7)
        da = left_at(lab("allows an outcome that", TEXT, 28), cA - 2.6, -2.15)
        db = left_at(lab("something else chooses", TEXT, 28), cA - 2.6, -2.55)
        self.play(FadeIn(da), FadeIn(db), run_time=0.4)
        self.at("instructive signal")
        sig2 = chip("signal", YELLOW, 28).move_to([cB - 1.7, 0.5, 0])
        out2 = chip("outcome", TEXT, 28).move_to([cB + 1.7, 0.5, 0])
        a4 = arr(sig2.get_right(), out2.get_left(), YELLOW, 9, 0.3)
        self.play(FadeIn(fb), FadeIn(hb), FadeIn(sig2), FadeIn(out2), run_time=0.7)
        self.at("chooses the outcome")
        self.play(GrowArrow(a4), run_time=0.7)
        dc = left_at(lab("chooses the outcome itself", TEXT, 28), cB - 2.6, -2.35)
        self.play(FadeIn(dc), run_time=0.4)
        self.finish()


def cortex_with_band(cx, cy, k, with_chip=False):
    sl = body(cx, cy, k)
    band = Rectangle(width=SL_W * k, height=0.55 * k, stroke_width=0, fill_color=YELLOW, fill_opacity=0.5
                     ).move_to([cx, cy + SL_H * k / 2 - 0.275 * k, 0])
    band.set_z_index(2)
    return sl, band


class S04Move(SpokenScene):
    def construct(self):
        cx, cy, k = -2.7, -0.15, 1.16
        sl, band = cortex_with_band(cx, cy, k)
        rl = lab("Reelin source", YELLOW, 32).move_to([3.8, 2.5, 0])
        self.add(sl, band, rl)
        self.at("cannot tell")
        x = cross(band.get_center(), 0.4)
        cards = VGroup(lab("permissive", TEXT, 30), T("?",48,RED), lab("instructive",TEXT,30)).arrange(DOWN,buff=0.35).move_to([3.8,0,0])
        self.play(Create(x), band.animate.set_opacity(0.15), FadeIn(cards), run_time=0.5)
        self.at("one test")
        test = VGroup(lab("a test of a",TEXT,32),lab("spatial message",TEXT,32)).arrange(DOWN).move_to([3.8,0.3,0])
        self.play(FadeOut(cards), FadeOut(x), FadeIn(test), band.animate.set_opacity(0.6), run_time=0.4)
        self.at("keep the signal present")
        self.play(Indicate(band,color=YELLOW),run_time=0.5)
        self.at("change where it is")
        bottom = [cx, cy - SL_H * k / 2 + 0.275 * k, 0]
        self.play(band.animate.move_to(bottom), run_time=0.8)
        self.wait(2.0)
        spot = source(2, cx, cy, k)
        self.play(Transform(band, spot), run_time=0.9)
        self.wait(3.3)
        self.finish()


def icon_stop(cx, cy):
    oct_ = RegularPolygon(n=8, radius=1.0, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.35).rotate(PI / 8).move_to([cx, cy, 0])
    t = T("STOP", 32, TEXT, weight=BOLD).move_to(oct_)
    return VGroup(oct_, t)


class S05Three(SpokenScene):
    def construct(self):
        head=lab("three simple proposals",TEXT,38).move_to([0,3.2,0])
        stop=icon_stop(-4.5,0.3).scale(1.4)
        fib=Line([-0.65,-1.7,0],[-0.65,2.0,0],color=GREY,stroke_width=12)
        # A palm with four long open fingers and an extended thumb.
        palm=RoundedRectangle(width=0.85,height=1.0,corner_radius=0.2,color=TEXT,fill_color=GREEN,fill_opacity=0.3).move_to([0.55,0.0,0])
        fingers=VGroup(*[Line([0.25+i*0.22,0.4,0],[0.12+i*0.32,1.2+0.15*(i%2),0],color=TEXT,stroke_width=7) for i in range(4)])
        thumb=Line([0.2,-0.1,0],[-0.25,0.35,0],color=TEXT,stroke_width=7)
        hand=VGroup(palm,fingers,thumb)
        src=Circle(radius=0.6,color=YELLOW,fill_color=YELLOW,fill_opacity=0.7).move_to([5.4,0.5,0])
        neuron=dot_neuron(3.3,-0.4,GREEN,0.4)
        arrow=arr([3.5,0,0],[4.8,0.5,0],TEXT,8)
        labels=VGroup(*[lab(t,TEXT,30).move_to([x,-2.35,0]) for x,t in [(-4.5,"stop here"),(0,"let go of glial fiber"),(4.5,"come here")]])
        self.add(head,stop,fib,hand,src,neuron,arrow,labels)
        self.at("stop here")
        self.play(Indicate(stop,color=RED),run_time=0.4)
        self.at("let go")
        self.play(hand.animate.shift(RIGHT*0.35),run_time=0.6)
        self.at("come here")
        self.play(neuron.animate.shift(RIGHT*0.45+UP*0.2),run_time=0.4)
        self.finish()


class S06Tests(SpokenScene):
    def construct(self):
        bodies = small_bodies()
        srcs = small_sources()
        labs = small_labels()
        self.play(*[FadeIn(b) for b in bodies], run_time=0.7)
        self.at("below the cortex")
        self.play(FadeIn(srcs[0]), FadeIn(labs[0]), run_time=0.6)
        self.at("one small spot")
        self.play(FadeIn(srcs[1]), FadeIn(labs[1]), run_time=0.6)
        self.at("medium bathing")
        self.play(FadeIn(srcs[2]), FadeIn(labs[2]), run_time=0.6)
        self.finish()


def predict_frame(sc, animate=False):
    bodies, srcs, labs = small_bodies(), small_sources(), small_labels()
    qs = VGroup(*[T("?", 80, TEXT, weight=BOLD).move_to([PCX[i], PCY - 0.75, 0]).set_z_index(5) for i in range(3)])
    pred = chip("Predict", GOLD, 34).move_to([-4.0, 3.3, 0])
    cond = left_at(lab("if Reelin means: come here", TEXT, 30), -2.4, 3.3)
    return bodies, srcs, labs, qs, pred, cond


class S07Predict(SpokenScene):
    def construct(self):
        bodies, srcs, labs, qs, pred, cond = predict_frame(self)
        self.add(*bodies, *srcs, *labs)
        self.at("predict")
        self.play(FadeIn(pred), run_time=0.5)
        self.at("means come here")
        self.play(FadeIn(cond), run_time=0.6)
        self.at("what should happen")
        self.play(FadeIn(qs), run_time=0.6)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        bodies, srcs, labs, qs, pred, cond = predict_frame(self)
        self.add(*bodies, *srcs, *labs, qs, pred, cond)
        self.wait(self.narration_s)


# ---------------------------------------------------------------- the three experiments
def credit(text, x, y, stacked=False):
    # Wrap long attribution rather than shrinking it against the right edge.
    if stacked:
        if "Jossin" in text:
            text = "Jossin, Goffinet and\ncolleagues, 2004"
        else:
            text = text.replace(", ", "\n")
    m = T(text, 34, GOLD, line_spacing=0.8)
    fit(m, max_w=5.8)
    return m.move_to([2.8, min(y, 3.05), 0])


def experiment(sc, idx, who, note, cue):
    bb, bs = body(BCX, BCY, BK, idx), source(idx, BCX, BCY, BK)
    cr = credit(who, 2.8, 3.05, stacked=True)
    desc = VGroup(*[lab(line, TEXT, 34) for line in note]).arrange(DOWN, buff=0.3).move_to([2.8, 0.9, 0])
    fit(desc, max_w=6.4)
    sc.add(bs, bb, cr, desc)
    label = lab(PLAB[idx-1], YELLOW, 32).move_to([BCX, -3.55 if idx == 3 else -3.15, 0])
    sc.add(label)
    sc.at(cue)
    sc.play(Indicate(bs, color=YELLOW, scale_factor=1.08), run_time=0.6)
    sc.finish()


class S09R1(SpokenScene):
    def construct(self):
        experiment(self,1,"Curran laboratory, 2002",["Reelin made below the cortex","at the ventricular zone","in reeler mice"],"made")


class S10R1b(SpokenScene):
    def construct(self):
        cx, cy, k = BCX, BCY, BK
        bb, bs = body(cx, cy, k, 1), source(1, cx, cy, k)
        o, b, g = rows(cx, cy, k, "reeler")
        cr = credit("Curran laboratory, 2002", 3.4, 3.25)
        vzl = lab("ventricular zone", YELLOW, 30).move_to([cx,-3.15,0])
        self.add(bb, bs, cr, vzl,legend(x=0.1,y0=-0.6,dy=0.6))
        self.play(FadeIn(o), FadeIn(b), FadeIn(g), run_time=0.6)
        self.at("split")
        tgt = []
        for i, m in enumerate(o):
            if i % 2 == 0:
                tgt.append(m.animate.move_to([cx + LA[i] * k, cy + Y_CR * k, 0]))
            else:
                tgt.append(m.animate.move_to([cx + LSUB[(i - 1) // 2] * k, cy + Y_SUB * k, 0]))
        c1 = left_at(chip("preplate split", ORANGE, 34), RX, 2.3)
        self.play(*tgt, FadeIn(c1), run_time=1.0)
        self.at("ataxia")
        c2 = left_at(chip("ataxia rescued", TEXT, 34), RX, 1.3)
        self.play(FadeIn(c2), run_time=0.5)
        self.at("not every defect")
        c3 = left_at(chip("not every defect", RED, 34), RX, 0.4)
        self.play(FadeIn(c3), run_time=0.5)
        self.at("neurons did not")
        ghost=DashedLine([cx,-0.4,0],[cx,-2.1,0],color=TEXT,stroke_width=6)
        tip=arr([cx,-1.7,0],[cx,-2.2,0],TEXT,6)
        x=cross([cx,-1.35,0],0.48,w=9)
        note=VGroup(lab("No downward migration",TEXT,30),lab("toward the source",TEXT,30)).arrange(DOWN).move_to([3.0,-2.7,0])
        self.play(FadeIn(ghost),FadeIn(tip),FadeIn(x),FadeIn(note),run_time=0.4)
        self.finish()


def p2_start(cx,cy,k):
    """Neutral intermingled schematic, not an assertion about initial layers."""
    groups=[]
    for j,col in enumerate((ORANGE,BLUE,GREEN)):
        groups.append(VGroup(*[dot_neuron(cx+(-1.65+0.46*i)*k,cy+(-1.8+0.30*((i+j)%3))*k,col,0.13) for i in range(8)]))
    return groups


def ring_pos(cx, cy, k, radius, i, off):
    ang = np.radians(225 - 45 * i + off)
    return [cx + radius * k * np.cos(ang), cy + 0.5 * k + radius * k * np.sin(ang), 0]


class S11R2(SpokenScene):
    def construct(self):
        experiment(self,2,"Nakajima laboratory, 2010",["Reelin made in","one small patch","of mouse cortex"],"one small patch")


class S12R2b(SpokenScene):
    def construct(self):
        cx, cy, k = BCX, BCY, BK
        bb, bs = body(cx, cy, k, 2), source(2, cx, cy, k)
        cr = credit("Nakajima laboratory, 2010", 3.4, 3.25)
        key = VGroup(Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9),
                     lab("Reelin made in one small patch", TEXT, 26))
        key[0].move_to([RX + 0.2, 1.9, 0])
        left_at(key[1], RX + 0.55, 1.9)
        self.add(bb, bs, cr, key, lab("schematic: initial positions unspecified",TEXT,26).move_to([BCX,-3.15,0]))
        o, b, g = p2_start(cx, cy, k)
        for m in (o, b, g):
            m.set_z_index(3)
        lg = legend(x=RX + 0.2, y0=0.7, dy=0.6)
        self.at("later born neurons")
        self.play(FadeIn(o), FadeIn(b), FadeIn(g), FadeIn(lg), run_time=0.8)
        self.at("passed earlier born")
        # Later cohorts visibly pass the preceding cohort toward the source.
        for grp, radius, off, travel in ((o, 1.55, 0, 0.7), (b, 1.1, 15, 1.3), (g, 0.62, 30, 1.6)):
            self.play(*[m.animate.move_to(ring_pos(cx,cy,k,radius,i,off)) for i,m in enumerate(grp)],run_time=travel,rate_func=smooth)
        self.at("inside out")
        ins = left_at(lab("inside-out arrangement", TEXT, 30), RX, -2.3)
        self.play(FadeIn(ins), run_time=0.5)
        self.finish()


class S13R3(SpokenScene):
    def construct(self):
        experiment(self,3,"Jossin, Goffinet and colleagues, 2004",["Reelin added to medium","bathing reeler slices"],"added")


class S14R3b(SpokenScene):
    def construct(self):
        cx,cy,k=BCX,BCY,BK
        self.add(source(3,cx,cy,k),body(cx,cy,k,3),credit("Jossin, Goffinet and colleagues, 2004",3,3.2))
        # An assay of organization, not a reconstruction of birth-order lamination.
        rng=np.random.RandomState(24)
        cells=VGroup(*[dot_neuron(cx+rng.uniform(-1.7,1.7),rng.uniform(-1.7,2.0),TEXT,0.14).set_z_index(3) for _ in range(18)])
        self.add(cells)
        assay=lab("short-term slice assay",TEXT,30).move_to([3.0,2.35,0])
        self.add(assay)
        self.at("more organized")
        targets=[]
        for i in range(18):
            # Still overlapping broad rows; no tidy stack or birth-order claim.
            targets.append([cx+(-1.6+(i%6)*0.64)+rng.uniform(-0.12,0.12),-0.7+(i//6)*0.65+rng.uniform(-0.45,0.45),0])
        caption=lab("more organized",TEXT,34).move_to([3.0,1.4,0])
        self.play(*[m.animate.move_to(t) for m,t in zip(cells,targets)],FadeIn(caption),run_time=0.65)
        self.at("without")
        normal=VGroup(lab("No Reelin from",TEXT,30),lab("its normal source",TEXT,30)).arrange(DOWN).move_to([3.0,0.2,0])
        self.play(FadeIn(normal),run_time=0.4)
        self.at("whether")
        note=VGroup(lab("? tissue distribution",YELLOW,30),lab("not measured",YELLOW,30)).arrange(DOWN).move_to([3.0,-1.45,0])
        leader=Line([-1.2,-0.8,0],[0,-1.45,0],color=YELLOW,stroke_width=3)
        self.play(FadeIn(note),Create(leader),run_time=0.45)
        self.add(dot_neuron(0.3,-2.8,TEXT,0.14),VGroup(lab("Neurons: birth waves",TEXT,26),lab("not measured",TEXT,26)).arrange(DOWN).move_to([3.0,-2.8,0]))
        self.finish()


# ---------------------------------------------------------------- the three results against the three proposals
def grid_frame():
    xs=(-0.8,2.0,5.0); ys=(1.3,0,-1.3)
    names=("below the\ncortex","one small\nspot","medium bathing\na slice")
    heads=VGroup(*[lab(n,TEXT,30).move_to([x,2.75,0]) for x,n in zip(xs,names)])
    rowl=VGroup(*[left_at(lab(n,TEXT,30),-6.3,y) for y,n in zip(ys,("stop here","let go","come here"))])
    lines=VGroup(Line([-6.3,2,0],[6.5,2,0],color=GREY),Line([-2.5,3.35,0],[-2.5,-1.9,0],color=GREY))
    note=VGroup(lab("Simplest form of each proposal",TEXT,34),lab("✓ fits    × does not fit    ? depends on details",TEXT,32),lab("Bath: tissue distribution was not measured",YELLOW,30)).arrange(DOWN,buff=0.22).move_to([0,-2.85,0])
    return xs,ys,heads,rowl,lines,note


TABLE={0:(False,False,None),1:(None,False,None),2:(False,True,None)}




def mark(x, y, v):
    if v is True:
        return tick([x, y, 0])
    if v is False:
        return cross([x, y, 0], 0.26, RED, 6)
    return T("?", 40, GREY, weight=BOLD).move_to([x, y, 0])


class S15None(SpokenScene):
    def construct(self):
        xs,ys,heads,rowl,lines,note=grid_frame()
        self.add(heads,lines,note)
        self.at("no single")
        self.play(FadeIn(rowl[0]), *[FadeIn(mark(xs[c],ys[0],TABLE[0][c])) for c in range(3)],run_time=0.55)
        self.at("fits all")
        self.play(FadeIn(rowl[1]), *[FadeIn(mark(xs[c],ys[1],TABLE[1][c])) for c in range(3)],run_time=0.55)
        self.at("three results")
        self.play(FadeIn(rowl[2]), *[FadeIn(mark(xs[c],ys[2],TABLE[2][c])) for c in range(3)],run_time=0.55)
        self.finish()
        # Preserve final audio; add reading time before the following silent beat.
        self.wait(max(0.1, 12.0 - self.elapsed()), frozen_frame=False)


class S16Beat(NarratedScene):
    def construct(self):
        xs, ys, heads, rowl, lines, note = grid_frame()
        marks = VGroup(*[mark(xs[c], ys[r], TABLE[r][c]) for r in range(3) for c in range(3)])
        self.add(heads, rowl, lines, note, marks)
        self.wait(self.narration_s)


# ---------------------------------------------------------------- when does a neuron read Reelin?
FX = -4.3          # the radial glial fiber, and the cortex slab centre
SLW, SLTOP, SLBOT = 3.8, 2.75, -3.25
PLATE_TOP, PLATE_BOT = 2.15, 0.2
TL_X = 2.2
TL_Y = (-1.5, 0.0, 1.5)


def cortex_slab():
    h = SLTOP - SLBOT
    rect = Rectangle(width=SLW, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06
                     ).move_to([FX, (SLTOP + SLBOT) / 2, 0])
    vz = Rectangle(width=SLW, height=0.45, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([FX, SLBOT + 0.225, 0])
    plate = Rectangle(width=SLW, height=PLATE_TOP - PLATE_BOT, stroke_width=0, fill_color=GREY, fill_opacity=0.28
                      ).move_to([FX, (PLATE_TOP + PLATE_BOT) / 2, 0])
    mz = Rectangle(width=SLW, height=SLTOP - PLATE_TOP, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2
                   ).move_to([FX, (SLTOP + PLATE_TOP) / 2, 0])
    iz=Rectangle(width=SLW,height=PLATE_BOT-(SLBOT+0.45),stroke_width=0,fill_color=BLUE,fill_opacity=0.14).move_to([FX,(PLATE_BOT+SLBOT+0.45)/2,0])
    return VGroup(rect, iz, vz, plate, mz)


def plate_label():
    labels=VGroup()
    for name,y,col in [("marginal zone",2.45,YELLOW),("cortical plate",1.15,TEXT),("intermediate zone",-1.9,TEXT)]:
        labels.add(left_at(lab(name,col,26),-2.1,y))
        labels.add(Line([-2.4,y,0],[-2.18,y,0],color=col,stroke_width=2))
    return labels


def multi(c, scale=1.0, seed=0):
    rng = np.random.RandomState(seed)
    c = np.array(c, float)
    soma = Circle(radius=0.3 * scale, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.65).move_to(c)
    angs = np.array([0.3, 1.5, 2.6, 3.9, 5.2]) + rng.uniform(-0.3, 0.3, 5)
    procs = []
    for a in angs:
        u = np.array([np.cos(a), np.sin(a), 0.0])
        L = rng.uniform(0.7, 1.0) * scale
        procs.append(Line(c + 0.3 * scale * u, c + (0.3 * scale + L) * u, stroke_color=GREEN, stroke_width=4))
    return VGroup(soma, *procs)


def fiber(x=FX, y0=-2.8, y1=2.15):
    return Line([x, y0, 0], [x, y1, 0], stroke_color=GREY, stroke_width=9)


def timeline_parts(states):
    """states: 'done', 'active', 'future' for the three dots."""
    line = Arrow([TL_X, -2.0, 0], [TL_X, 2.15, 0], buff=0, color=GREY, stroke_width=7, tip_length=0.32)
    names = ("multipolar", "climbs a glial fiber", "somal translocation")
    dots, labs_ = [], []
    for y, s, n in zip(TL_Y, states, names):
        if s == "done":
            d = Circle(radius=0.15, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35)
            col = GREY
        elif s == "active":
            d = Circle(radius=0.2, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=1)
            col = TEXT
        else:
            d = Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_opacity=0)
            col = GREY
        d.move_to([TL_X, y, 0])
        dots.append(d)
        labs_.append(left_at(lab(n, col, 28), TL_X + 0.4, y))
    return VGroup(line,lab("stage",TEXT,34).move_to([TL_X,-2.7,0])), dots, labs_


def header():
    return lab("a typical later-born neuron", TEXT, 30).move_to([-3.5, 3.3, 0])


class S17When(SpokenScene):
    def construct(self):
        slab = cortex_slab()
        n = multi([FX - 0.3,-1.3,0],0.85,seed=1)
        line, dots, labs_ = timeline_parts(("future", "future", "future"))
        self.add(slab, n, header(), plate_label(), line, *dots, *labs_)
        self.at("multipolar")
        active_line, active_dots, active_labs = timeline_parts(("active", "future", "future"))
        self.play(Transform(dots[0], active_dots[0]), Transform(labs_[0], active_labs[0]), run_time=0.7)
        self.at("wandering below")
        waypoints = [([FX + 0.5, -0.9, 0], 3), ([FX - 0.4, -1.5, 0], 4), ([FX + 0.1, -1.1, 0], 5)]
        for c, sd in waypoints[:1]:
            self.play(Transform(n, multi(c, 0.85, seed=sd)), run_time=0.9)
        self.at("cortical plate")
        for c, sd in waypoints[1:]:
            self.play(Transform(n, multi(c, 0.85, seed=sd)), run_time=1.0)
        self.finish()


def bipolar_parts(fx, y):
    soma = Circle(radius=0.3, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.65).move_to([fx + 0.34, y, 0])
    lead = Line([fx + 0.34, y + 0.3, 0], [fx + 0.06, y + 0.85, 0], stroke_color=GREEN, stroke_width=5)
    trail = Line([fx + 0.34, y - 0.3, 0], [fx + 0.06, y - 0.8, 0], stroke_color=GREEN, stroke_width=5)
    grips = VGroup(Circle(radius=0.07, stroke_color=TEXT, fill_color=TEXT, fill_opacity=1).move_to([fx + 0.06, y + 0.85, 0]),
                   Circle(radius=0.07, stroke_color=TEXT, fill_color=TEXT, fill_opacity=1).move_to([fx + 0.06, y - 0.8, 0]))
    return soma, lead, trail, grips


class S18Climb(SpokenScene):
    def construct(self):
        slab = cortex_slab()
        pl = plate_label()
        hd = header()
        line, dots, labs_ = timeline_parts(("done", "active", "future"))
        n = multi([FX + 0.1, -1.1, 0], 1.0, seed=5)
        self.add(slab, pl, hd, line, dots[0], labs_[0], n)
        fb = fiber()
        self.play(Create(fb), run_time=0.4)
        self.at("takes hold")
        soma, lead, trail, grips = bipolar_parts(FX, -1.4)
        self.play(FadeOut(n[1:]), n[0].animate.move_to(soma.get_center()), Create(lead), Create(trail), FadeIn(grips), run_time=0.6)
        self.at("radial glial fiber")
        fl = left_at(lab("radial glial fiber", GREY, 26), -2.1, -3.0)
        self.play(FadeIn(fl), run_time=0.4)
        self.at("and climbs")
        climber = VGroup(n[0], lead, trail, grips)
        c2 = dots[1].copy().set_fill(GREEN, 1).set_stroke(GREEN)
        self.play(climber.animate.shift(UP * 2.45), FadeIn(dots[1]), FadeIn(labs_[1]), run_time=1.8)
        self.finish()


class S19Soma(SpokenScene):
    def construct(self):
        slab = cortex_slab()
        pl = plate_label()
        hd = header()
        line, dots, labs_ = timeline_parts(("done", "done", "future"))
        fb = fiber()
        soma, lead, trail, grips = bipolar_parts(FX, 1.05)
        self.add(slab, pl, hd, line, dots[0], dots[1], labs_[0], labs_[1], fb, soma, lead, trail, grips)
        self.at("near the top")
        self.play(Indicate(soma, color=GREEN, scale_factor=1.15), run_time=0.6)
        self.at("anchors")
        # the neuron lets go of the fiber and sends its leading process up into the marginal zone
        anchor_pt = [FX + 0.06, 2.5, 0]
        lead2 = Line(soma.get_top(), anchor_pt, stroke_color=GREEN, stroke_width=5)
        anc = Circle(radius=0.13, stroke_color=TEXT, stroke_width=3, fill_color=GREEN, fill_opacity=1).move_to(anchor_pt)
        self.play(Transform(lead, lead2), FadeOut(grips), fb.animate.set_opacity(0.3), run_time=0.9)
        self.play(FadeIn(anc, scale=0.5), run_time=0.3)
        self.at("marginal zone")
        mzl = left_at(lab("marginal zone", YELLOW, 26), FX + SLW / 2 + 0.3, 2.45)
        self.play(Indicate(pl[0],color=YELLOW,scale_factor=1.0), run_time=0.4)
        self.at("pulls its cell body")
        new_soma_y = 1.85
        lead3 = Line([FX + 0.34, new_soma_y + 0.3, 0], anchor_pt, stroke_color=GREEN, stroke_width=5)
        self.play(soma.animate.move_to([FX + 0.34, new_soma_y, 0]), Transform(lead, lead3), FadeOut(trail), run_time=1.5)
        self.at("somal translocation")
        d3, l3 = timeline_parts(("active", "active", "active"))[1][2], timeline_parts(("active", "active", "active"))[2][2]
        self.play(FadeIn(d3, scale=1.6), FadeIn(l3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- Reelin's link to the stages
CARD_X = (-4.5, 0.0, 4.5)
CARD_Y, CARD_W, CARD_H = 0.15, 3.5, 3.4


def stage_cards():
    cards = VGroup(*[RoundedRectangle(corner_radius=0.2, width=CARD_W, height=CARD_H, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=0.06).move_to([x, CARD_Y, 0]) for x in CARD_X])
    # 1 multipolar
    m = multi([CARD_X[0], CARD_Y, 0], 1.0, seed=2)
    # 2 climbing a fiber
    fx = CARD_X[1] - 0.2
    fb = Line([fx, CARD_Y - 1.4, 0], [fx, CARD_Y + 1.4, 0], stroke_color=GREY, stroke_width=9)
    s, l, t, g = bipolar_parts(fx, CARD_Y - 0.1)
    c2 = VGroup(fb, s, l, t, g)
    # 3 translocation
    band = Rectangle(width=CARD_W - 0.06, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.2).move_to([CARD_X[2], CARD_Y + CARD_H / 2 - 0.28, 0])
    soma = Circle(radius=0.3, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.65).move_to([CARD_X[2], CARD_Y - 0.15, 0])
    lead = Line([CARD_X[2], CARD_Y + 0.15, 0], [CARD_X[2], CARD_Y + 1.45, 0], stroke_color=GREEN, stroke_width=5)
    anc = Circle(radius=0.13, stroke_color=TEXT, stroke_width=3, fill_color=GREEN, fill_opacity=1).move_to([CARD_X[2], CARD_Y + 1.45, 0])
    c3 = VGroup(band, lead, soma, anc)
    titles = VGroup(lab("multipolar", TEXT, 28).move_to([CARD_X[0], -2.0, 0]),
                    lab("climbing", TEXT, 28).move_to([CARD_X[1], -2.0, 0]),
                    lab("somal translocation", TEXT, 28).move_to([CARD_X[2], -2.0, 0]))
    arrows = VGroup(arr([-2.7, CARD_Y, 0], [-1.8, CARD_Y, 0], GREY, 5), arr([1.8, CARD_Y, 0], [2.7, CARD_Y, 0], GREY, 5))
    return cards, m, c2, c3, titles, arrows


def pathway_chips():
    r = chip("Reelin", YELLOW, 28)
    d = chip("Dab1", PURPLE, 28)
    p = chip("Rap1", TEXT, 28)
    a1 = arr([0, 0, 0], [0.6, 0, 0], GREY, 5)
    a2 = arr([0, 0, 0], [0.6, 0, 0], GREY, 5)
    g = VGroup(r, a1, d, a2, p).arrange(RIGHT, buff=0.15).move_to([0, 3.2, 0])
    return g


class S20Stages(SpokenScene):
    def construct(self):
        cards, m, c2, c3, titles, arrows = stage_cards()
        pw = pathway_chips()
        self.add(cards, m, c2, c3, titles, arrows)
        self.play(FadeIn(pw[0]), run_time=0.01)
        self.at("signaling through")
        self.play(FadeIn(pw[1]), FadeIn(pw[2]), run_time=0.5)
        self.at("and", nth=1)
        self.play(FadeIn(pw[3]), FadeIn(pw[4]), run_time=0.5)
        self.at("has been linked")
        self.wait(0.3)
        self.at("both the turn")
        glow=arr([-2.7,CARD_Y,0],[-1.8,CARD_Y,0],YELLOW,10,0.3)
        g3=RoundedRectangle(corner_radius=0.2,width=CARD_W,height=CARD_H,stroke_color=YELLOW,stroke_width=6).move_to([CARD_X[2],CARD_Y,0])
        cad=VGroup(lab("the turn",TEXT,28),lab("N-cadherin adhesion",TEXT,26)).arrange(DOWN).move_to([-2.5,-2.9,0])
        fin=lab("the final step",TEXT,28).move_to([4.5,-2.85,0])
        self.play(Transform(arrows[0],glow),Create(g3),FadeIn(cad),FadeIn(fin),run_time=0.45)
        self.finish()


def toggle(x, y, on=False):
    track = RoundedRectangle(corner_radius=0.25, width=1.0, height=0.5, stroke_color=YELLOW if on else GREY, stroke_width=3,
                             fill_color=YELLOW if on else GREY, fill_opacity=0.45 if on else 0.15).move_to([x, y, 0])
    knob = Circle(radius=0.19, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([x + (0.25 if on else -0.25), y, 0])
    return VGroup(track, knob).scale(1.65).move_to([x,y,0])


class S21Switch(SpokenScene):
    def construct(self):
        cards,m,c2,c3,titles,arrows=stage_cards()
        self.add(cards,m,c2,c3,titles,arrows)
        view=lab("one view",TEXT,32).move_to([-4.5,3.5,0])
        self.add(view)
        tg1,tg2=toggle(-4.5,2.55),toggle(4.5,2.55)
        ad1=lab("adhesion",TEXT,36).move_to([-4.5,-2.8,0])
        ad2=lab("adhesion",TEXT,36).move_to([4.5,-2.8,0])
        self.add(tg1,tg2,ad1,ad2)
        self.at("a command")
        cmd=lab("command?",GREY,30).move_to([-0.5,3.35,0]).set_opacity(0.65)
        self.play(FadeIn(cmd),run_time=0.3)
        self.at("a switch")
        sw=lab("more like a switch",TEXT,30).move_to([3.8,3.35,0])
        self.play(FadeIn(sw),run_time=0.35)
        self.at("flipped at")
        self.play(Transform(tg1, toggle(-4.5, 2.55, True)),
                  cards[0].animate.set_stroke(YELLOW, width=6), run_time=0.55)
        self.at("particular stages")
        self.play(Transform(tg2, toggle(4.5, 2.55, True)),
                  cards[2].animate.set_stroke(YELLOW, width=6), run_time=0.55)
        self.wait(1.0)

        self.finish()


def option_gradient(cx, cy):
    bars = VGroup(*[Rectangle(width=0.4, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.05 + 0.05 * i).move_to([cx + (i - 3.5) * 0.4, cy, 0]) for i in range(8)])
    return bars


def option_boundary(cx, cy):
    left = Rectangle(width=1.6, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.3).move_to([cx - 0.8, cy, 0])
    right = Rectangle(width=1.6, height=1.6, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([cx + 0.8, cy, 0])
    edge = Line([cx, cy - 0.9, 0], [cx, cy + 0.9, 0], stroke_color=TEXT, stroke_width=5)
    return VGroup(left, right, edge)


def option_adhesive(cx, cy):
    fb = Line([cx - 0.9, cy - 0.85, 0], [cx - 0.9, cy + 0.85, 0], stroke_color=GREY, stroke_width=9)
    cell = Circle(radius=0.4, stroke_color=GREEN, stroke_width=2.5, fill_color=GREEN, fill_opacity=0.65).move_to([cx + 0.7, cy, 0])
    links = VGroup(*[Line([cx - 0.8, cy + dy, 0], [cx + 0.3, cy + dy * 0.6, 0], stroke_color=TEXT, stroke_width=4) for dy in (-0.3, 0.0, 0.3)])
    return VGroup(fb, cell, links)


class S22Open(SpokenScene):
    def construct(self):
        xs=(-4.4,0,4.4)
        self.add(lab("the essential cue",TEXT,36).move_to([0,3.3,0]))
        pics=[option_gradient(xs[0],0.2),option_boundary(xs[1],0.2),option_adhesive(xs[2],0.2)]
        for x,pic,name in zip(xs,pics,("gradient","boundary","adhesive state")):
            pic.stretch(2.0,1)
            for part in pic.family_members_with_points():
                part.set_fill(opacity=part.get_fill_opacity()*0.65)
                part.set_stroke(opacity=0.55)
            box=RoundedRectangle(width=3.9,height=4.3,corner_radius=0.2,color=GREY,stroke_width=2).move_to([x,0.2,0]).set_stroke(opacity=0.5)
            self.add(box,pic,lab(name,TEXT,30).move_to([x,-2.4,0]))
        self.add(lab("Reelin: low → high",YELLOW,26).move_to([-4.4,2.6,0]))
        self.at("not settled")
        self.play(FadeIn(chip("open question",TEXT,36).move_to([0,-3.25,0])),run_time=0.4)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        cx, cy, k = -4.3, -0.15, 1.13
        sl = body(cx, cy, k)
        nrm = VGroup(*rows(cx, cy, k, "normal"))
        X0 = -1.6
        l1 = left_at(lab("Neurons are born in order.", TEXT, 30), X0, 3.0)
        l2 = left_at(lab("Reelin signalling is needed to stack that", TEXT, 30), X0, 2.45)
        l3 = left_at(lab("order the right way up.", TEXT, 30), X0, 1.9)
        rule = Line([X0, 1.3, 0], [6.5, 1.3, 0], stroke_color=GOLD, stroke_width=3)
        tk = left_at(chip("Takeaway", GOLD, 30), X0, 0.75)
        key=VGroup(*[VGroup(dot_neuron(0,0,c,0.12),lab(n,TEXT,26)).arrange(RIGHT,buff=0.15) for n,c in [("first-born",ORANGE),("next-born",BLUE),("last-born",GREEN)]]).arrange(RIGHT,buff=0.5).move_to([2.4,-3.35,0])
        self.add(key)
        for name, y in [("marginal-zone neurons", 3.35),
                        ("cortical plate", -0.55), ("subplate neurons", -1.6)]:
            self.add(lab(name, TEXT, 28).move_to([cx, y, 0]))
        self.add(lab("Orange: first-born preplate", ORANGE, 26).move_to([cx, -2.35, 0]),
                 lab("split into these two rows", ORANGE, 26).move_to([cx, -2.8, 0]))
        self.play(FadeIn(sl), FadeIn(nrm), FadeIn(l1), FadeIn(l2), FadeIn(l3), Create(rule), FadeIn(tk), run_time=0.8)
        self.at("signaling helps")
        t1 = left_at(lab("Reelin signalling helps each new wave", TEXT, 34), X0, -0.05)
        t2 = left_at(lab("tend to finish its climb at the top.", TEXT, 34), X0, -0.65)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.7)
        self.at("that alone")
        t3 = left_at(lab("That alone does not show that neurons", RED, 34), X0, -1.65)
        t4 = left_at(lab("steer toward Reelin.", RED, 34), X0, -2.25)
        self.play(FadeIn(t3), FadeIn(t4), run_time=0.7)
        self.finish()


class S24End(EndCard):
    LINE = "Reelin helps new waves tend to finish at the top."
