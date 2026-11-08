"""Vesicle budding, targeting and fusion: a vesicle needs three separate steps  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = membranes, the cell outline, structure, de-emphasized labels
  YELLOW = the vesicle (the thing that moves)
  ORANGE = cargo and the secretory enzyme pool
  BLUE   = the coat (Sar1, Sec23/24, outer cage, COPII)
  TEAL   = the address machinery (Rab, tether)
  PURPLE = SNAREs
  PINK   = the removers: GDI and NSF
  GREEN  = GTP on / a step that worked
  RED    = a block, a failed step, the 37 C shift
  GOLD   = ATP badge
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FB4"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def vesicle(r=0.34, cargo=True):
    c = Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.16)
    parts = [c]
    if cargo:
        for dx, dy in [(-0.32, 0.12), (0.28, -0.2), (0.05, 0.38), (-0.12, -0.36)]:
            parts.append(Dot([dx * r / 0.8, dy * r / 0.8, 0], radius=max(0.05, r * 0.15), color=ORANGE))
    g = VGroup(*parts)
    g.circ = c
    return g


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def tag(text, color, size=24):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def check(center, color=GREEN, s=0.3, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, 0.0, 0], c + [-s * 0.3, -s * 0.8, 0], color=color, stroke_width=w),
                  Line(c + [-s * 0.3, -s * 0.8, 0], c + [s, s * 0.8, 0], color=color, stroke_width=w))


def cross(center, color=RED, s=0.3, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def membrane_curve(y0, hfun, x0=-6.3, x1=6.3, sw=16):
    return always_redraw(lambda: ParametricFunction(lambda x: [x, y0 + hfun(x), 0], t_range=[x0, x1, 0.05],
                                                    color=GREY, stroke_width=sw))


def dome(x, bx, w, h):
    return h * np.exp(-(((x - bx) / w) ** 4))


class S00Title(TitleCard):
    LESSON = "Vesicle budding, targeting and fusion"
    TITLE = "A Vesicle Needs Three Separate Steps"


# ---------------------------------------------------------------------------------------------
class S01Stuck(SpokenScene):
    """sec1 at 37 C: vesicles form but pile up inside; the enzyme pool climbs to up to eightfold."""

    def construct(self):
        cx, cy = -1.6, -0.2
        cell = Ellipse(width=9.0, height=5.6, stroke_color=GREY, stroke_width=6, fill_color=GREY,
                       fill_opacity=0.07).move_to([cx, cy, 0])
        t25 = bchip("25 °C: grows", GREEN, 28).move_to([cx, 3.1, 0])
        self.at("grows at")
        self.play(FadeIn(cell, scale=0.95), FadeIn(t25), run_time=0.9)

        # enzyme-pool bar (1x -> up to 8x)
        bx = 5.3
        unit = 0.65
        frame_bar = RoundedRectangle(corner_radius=0.08, width=0.8, height=8 * unit, stroke_color=GREY,
                                     stroke_width=3).move_to([bx, -2.8 + 4 * unit, 0])
        level = ValueTracker(1.0)
        fill = always_redraw(lambda: Rectangle(width=0.8, height=level.get_value() * unit, stroke_width=0,
                                               fill_color=ORANGE, fill_opacity=0.9)
                             .move_to([bx, -2.8 + level.get_value() * unit / 2, 0]))
        pool_lbl = T("enzyme inside", 24, ORANGE).move_to([bx, -3.25, 0])
        one = M("1×", 24, GREY).next_to(frame_bar, LEFT, buff=0.15).align_to(frame_bar, DOWN).shift(UP * 0.1)

        # vesicle pile, inside the right half of the cell
        rng = np.random.RandomState(4)
        pos = []
        tries = 0
        while len(pos) < 15 and tries < 4000:
            tries += 1
            x, y = rng.uniform(-0.8, 1.5), rng.uniform(-2.0, 1.7)
            if ((x - cx) / 4.0) ** 2 + ((y - cy) / 2.35) ** 2 > 1:
                continue
            if all(np.hypot(x - p[0], y - p[1]) > 0.78 for p in pos):
                pos.append((x, y))
        pos.sort(key=lambda p: -p[0])
        ves = [vesicle(0.3) for _ in pos]
        for v in ves:
            v.move_to([-4.6, cy + rng.uniform(-0.9, 0.9), 0])

        t37 = bchip("37 °C", RED, 28).move_to([cx, 3.1, 0])
        self.at("degrees", nth=1)
        self.play(ReplacementTransform(t25, t37), FadeIn(frame_bar), FadeIn(fill), FadeIn(pool_lbl), FadeIn(one),
                  run_time=0.8)
        anims = []
        for v, p in zip(ves, pos):
            anims.append(AnimationGroup(FadeIn(v, run_time=0.4), v.animate(run_time=1.5).move_to([p[0], p[1], 0])))
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=2.7)
        wall_q = bchip("?", RED, 34).move_to([cx + 4.5, cy + 0.1, 0])
        out_arrow = DashedLine([cx + 3.5, cy + 0.1, 0], [cx + 6.0, cy + 0.1, 0], color=GREY, stroke_width=5)
        self.at("stay inside")
        self.play(Create(out_arrow), FadeIn(wall_q, scale=0.6), run_time=0.6)
        vl = T("membrane-bound vesicles", 24, YELLOW).move_to([cx - 1.8, 1.1, 0])
        self.at("rises up")
        self.play(level.animate.set_value(8.0), run_time=1.9)
        top = M("up to 8×", 28, ORANGE).move_to([bx, 2.9, 0])
        self.play(FadeIn(top), run_time=0.4)
        self.at("packed into")
        self.play(FadeIn(vl), run_time=0.4)
        ok = bchip("budding worked", GREEN, 26).move_to([cx - 1.4, -1.75, 0])
        self.at("vesicles formed")
        self.play(FadeIn(ok, scale=0.9), Indicate(VGroup(*ves), color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("later failed")
        self.play(Indicate(VGroup(*wall_q[1:]), color=RED, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Coat(SpokenScene):
    """Sar1-GTP -> Sec23/24 -> outer cage = COPII; the coat gathers cargo and bends the membrane into a bud."""

    def construct(self):
        y0 = -1.5
        w = 1.5
        hh = ValueTracker(0.0)
        mem = membrane_curve(y0, lambda x: dome(x, 0, w, hh.get_value()), sw=18)
        cyt = T("cytosol", 26, GREY).move_to([5.4, -0.9, 0])
        lum = T("ER lumen", 26, GREY).move_to([-5.2, -2.45, 0])
        cargo_pos = [(-1.9, -2.05), (-0.6, -2.1), (0.5, -2.05), (1.8, -2.1), (3.3, -2.05)]
        cargo = VGroup(*[Dot([x, y, 0], radius=0.16, color=ORANGE) for x, y in cargo_pos])
        cargo_lbl = T("cargo", 26, ORANGE).move_to([3.3, -2.55, 0])
        self.at("vesicle first needs")
        self.play(FadeIn(mem), FadeIn(cyt), FadeIn(lum), FadeIn(cargo), FadeIn(cargo_lbl), run_time=0.9)

        sar = VGroup(bchip("Sar1", BLUE, 34), bchip("GTP", GREEN, 26)).arrange(RIGHT, buff=0.12)
        sar.move_to([0, -0.8, 0]).shift(UP * 2.5)
        self.at("small switch")
        self.play(FadeIn(sar), run_time=0.4)
        self.at("binds the membrane")
        self.play(sar.animate.move_to([0, -0.8, 0]), run_time=0.8)

        sec = bchip("Sec23/24", BLUE, 34).move_to([0, 0.65, 0])
        a1 = arr([0, -0.3, 0], [0, 0.15, 0], BLUE, w=7, tip=0.25)
        self.at("brings in")
        self.play(FadeIn(sec, shift=DOWN * 0.3), GrowArrow(a1), run_time=0.6)
        cage = bchip("outer cage", BLUE, 34).move_to([0, 2.15, 0])
        a2 = arr([0, 1.2, 0], [0, 1.65, 0], BLUE, w=7, tip=0.25)
        self.at("outer cage")
        self.play(FadeIn(cage, shift=DOWN * 0.3), GrowArrow(a2), run_time=0.6)

        # coat arcs follow the dome height
        def arc(w0, off, sw, dashed, op):
            def mk():
                h = hh.get_value()
                curve = ParametricFunction(
                    lambda x: [x, y0 + h * np.exp(-((x / w0) ** 4)) + off, 0],
                    t_range=[-1.25 * w0, 1.25 * w0, 0.04], color=BLUE, stroke_width=sw, stroke_opacity=op)
                return DashedVMobject(curve, num_dashes=18, dashed_ratio=0.72) if dashed else curve
            return always_redraw(mk)
        inner = arc(w + 0.25, 0.28, 16, False, 0.9)
        outer = arc(w + 0.65, 0.7, 12, True, 0.7)
        copii = T("COPII", 48, BLUE, weight=BOLD).move_to([0, 3.0, 0])
        self.at("Together they make")
        self.play(FadeIn(inner), FadeIn(outer),
                  sar.animate.move_to([-4.7, -1.0, 0]), sec.animate.move_to([-4.7, 0.2, 0]),
                  cage.animate.move_to([4.5, 1.3, 0]),
                  FadeOut(a1), FadeOut(a2), FadeIn(copii, scale=0.9), run_time=1.2)
        pick = bchip("picks cargo", ORANGE, 28).move_to([-4.6, 3.0, 0])
        bend = bchip("bends membrane", BLUE, 28).move_to([4.6, 3.0, 0])
        self.at("grabs the cargo")
        gather = [(-0.8, -2.05), (-0.4, -2.1), (0.0, -2.05), (0.4, -2.1), (0.8, -2.05)]
        self.play(FadeIn(pick, scale=0.9), FadeOut(cargo_lbl),
                  *[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(cargo, gather)], run_time=0.9)
        self.at("bends the membrane")
        tgt = [(-0.8, -1.1), (0.8, -1.1), (0.0, -0.5), (-0.5, 0.2), (0.5, 0.2)]
        self.play(FadeIn(bend, scale=0.9),
                  hh.animate.set_value(3.2),
                  *[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(cargo, tgt)],
                  run_time=1.3)
        # pinch off
        ring = DashedVMobject(Circle(radius=1.85, stroke_color=BLUE, stroke_width=9, stroke_opacity=0.8),
                              num_dashes=22, dashed_ratio=0.72)
        ves = Circle(radius=1.6, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.12)
        cv = VGroup(ves, ring).move_to([0, y0 + 1.95, 0])
        self.at("into a bud")
        self.remove(inner, outer)
        self.play(FadeIn(cv), hh.animate.set_value(0.0), cargo.animate.shift(UP * 0.35), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Address(SpokenScene):
    """coated vesicle (coat can stay on to the Golgi); Rab-GDP lifted off the membrane by GDI; GEF loads GTP; Rab-GTP lights up; tethers catch the vesicle."""

    def construct(self):
        bar = RoundedRectangle(corner_radius=0.12, width=0.36, height=6.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to([5.0, -0.2, 0])
        tm = T("target membrane", 26, GREY).move_to([4.3, 3.3, 0])
        ves = vesicle(1.0).move_to([-4.4, 0.6, 0])
        ring = DashedVMobject(Circle(radius=1.3, stroke_color=BLUE, stroke_width=9, stroke_opacity=0.8),
                              num_dashes=18, dashed_ratio=0.72).move_to(ves)
        self.add(ves, ring)
        self.at("needs an address")
        self.play(FadeIn(bar), FadeIn(tm), run_time=0.8)

        # Rab on the target membrane with GDP
        rab = bchip("Rab", TEAL, 36).move_to([3.95, 1.5, 0])
        tail = Line([rab.get_right()[0], 1.5, 0], [4.8, 1.5, 0], color=TEAL, stroke_width=8)
        gdp = bchip("GDP", GREY, 26).move_to([3.95, 2.5, 0])
        rab_g = VGroup(rab, tail, gdp)
        self.at("small switch")
        self.play(FadeIn(rab_g, shift=LEFT * 0.4), run_time=0.7)

        # GDI lifts it into the cytosol
        gdi = bchip("GDI", PINK, 34).move_to([1.6, 1.5, 0])
        cup = Arc(radius=0.62, start_angle=PI / 2, angle=PI, color=PINK, stroke_width=8).move_to([3.2, 1.5, 0])
        cyt = T("cytosol", 26, GREY).move_to([-3.0, 3.0, 0])
        self.at("held in the cytosol")
        self.play(FadeIn(gdi, shift=RIGHT * 0.4), FadeIn(cup), FadeIn(cyt), run_time=0.7)
        held = VGroup(rab_g, gdi, cup)
        self.play(FadeOut(tail), held.animate.shift(LEFT * 2.6 + UP * 0.2), run_time=1.0)

        # GEF on the right membrane
        gef = bchip("GEF", GREY, 34).move_to([3.95, -0.6, 0])
        self.at("right membrane")
        self.play(FadeIn(gef, shift=LEFT * 0.3), FadeOut(gdi), FadeOut(cup),
                  rab_g.animate.shift(RIGHT * 2.6 + DOWN * 1.3), run_time=0.9)
        ry = rab.get_center()[1]
        tail3 = Line([rab.get_right()[0], ry, 0], [4.8, ry, 0], color=TEAL, stroke_width=8)
        self.add(tail3)
        gtp = bchip("GTP", GREEN, 26).move_to(gdp)
        glow = Ellipse(width=2.3, height=1.3, stroke_color=GREEN, stroke_width=8, stroke_opacity=0.55).move_to(rab)
        self.at("loads")
        self.play(ReplacementTransform(gdp, gtp), run_time=0.5)
        self.at("lights up")
        self.play(FadeIn(glow), Indicate(rab, color=GREEN, scale_factor=1.15), run_time=0.7)

        # tethers grow and catch the vesicle
        x0 = rab.get_left()[0] - 0.05
        t1 = Line([x0, ry + 0.14, 0], [x0, ry + 0.14, 0], color=TEAL, stroke_width=11)
        t2 = Line([x0, ry - 0.14, 0], [x0, ry - 0.14, 0], color=TEAL, stroke_width=11)
        end_x = -0.6
        self.at("recruits tethers")
        self.play(FadeOut(glow, run_time=0.2),
                  t1.animate.put_start_and_end_on([x0, ry + 0.14, 0], [end_x, ry + 0.14, 0]),
                  t2.animate.put_start_and_end_on([x0, ry - 0.14, 0], [end_x, ry - 0.14, 0]),
                  run_time=1.6)
        tl = T("tether", 28, TEAL).move_to([1.4, ry + 0.75, 0])
        self.play(FadeIn(tl), run_time=0.3)
        self.at("capture the vesicle")
        self.play(VGroup(ves, ring).animate.move_to([end_x - 1.0, ry, 0]), run_time=1.5)
        hook = Dot([end_x, ry, 0], radius=0.17, color=TEAL)
        self.play(FadeIn(hook, scale=2), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Fuse(SpokenScene):
    """three Q rods stand on the target, the R rod hangs from the vesicle; the overlap zippers; membranes merge; NSF resets."""

    def construct(self):
        xt = -5.0                       # target membrane (vertical bar)
        L = 2.9
        RV = 1.15
        rows = [1.2, 0.6, 0.0, -0.6]    # Qa, Qb, Qc, R
        base = xt + 0.09 + 0.02
        tip_q = base + L
        hmem = ValueTracker(0.0)
        mem = always_redraw(lambda: ParametricFunction(
            lambda y: [xt + dome(y, -0.6, 1.0, hmem.get_value()), y, 0], t_range=[-3.3, 3.3, 0.05],
            color=GREY, stroke_width=18))
        z = ValueTracker(0.0)
        start_c = tip_q - 0.3 + L + RV   # vesicle centre when the overlap is 0.3
        end_c = base + L + RV            # full overlap

        def cx():
            return start_c + (end_c - start_c) * z.get_value()

        ves = vesicle(RV)
        vy = (rows[2] + rows[3]) / 2
        ves.add_updater(lambda m: m.move_to([cx(), vy, 0]))
        ves.move_to([cx(), vy, 0])

        def rod(y, x_l, x_r, col=PURPLE):
            return RoundedRectangle(corner_radius=0.12, width=x_r - x_l, height=0.4, stroke_color=col,
                                    stroke_width=3, fill_color=col, fill_opacity=0.45).move_to([(x_l + x_r) / 2, y, 0])

        qrods = VGroup(*[rod(y, base, tip_q) for y in rows[:2]])
        rrod = always_redraw(lambda: VGroup(rod(rows[2], cx() - RV - L, cx() - RV), rod(rows[3], cx() - RV - L, cx() - RV)))
        lx = -6.2
        legend = VGroup(*[bchip(n, PURPLE, 26) for n in ["Qa", "Qb", "Qc", "R"]]).arrange(RIGHT, buff=0.25).move_to([3.4, 3.0, 0])
        qlab = VGroup()
        rlab = VGroup()

        def wind():
            lo, hi = cx() - RV - L, tip_q
            g = VGroup()
            x = lo + 0.2
            while x < hi - 0.1:
                g.add(Line([x - 0.12, rows[0] + 0.22, 0], [x + 0.12, rows[3] - 0.22, 0], color=TEXT,
                           stroke_width=3, stroke_opacity=0.6))
                x += 0.34
            return g
        wnd = always_redraw(wind)

        tm = T("target membrane", 26, GREY).move_to([-3.1, 3.2, 0])
        vl = T("vesicle", 28, YELLOW).move_to([cx() + RV + 0.9, vy, 0])
        tl1 = Line([xt + 0.2, 2.6, 0], [cx() - 0.8, vy + 0.8, 0], color=TEAL, stroke_width=10)
        tl2 = Line([xt + 0.2, -3.0, 0], [cx() - 0.8, vy - 0.8, 0], color=TEAL, stroke_width=10)
        tlab = T("tether", 28, TEAL).move_to([-2.6, -0.5, 0])

        self.add(mem, ves)
        self.at("Capture is not fusion")
        self.play(FadeIn(mem), FadeIn(ves), FadeIn(tl1), FadeIn(tl2), FadeIn(tlab), FadeIn(tm), FadeIn(vl),
                  run_time=1.0)
        self.at("resist merging")
        self.play(Indicate(VGroup(tl1, tl2), color=TEAL, scale_factor=1.0), run_time=0.9)
        self.at("SNAREs supply the force")
        self.play(FadeOut(tl1), FadeOut(tl2), FadeOut(tlab), FadeIn(qrods), FadeIn(rrod), run_time=0.8)
        self.add(rrod)
        self.at("Four motifs")
        self.play(FadeIn(legend), run_time=0.9)
        self.at("one bundle")
        self.play(FadeIn(wnd), Indicate(VGroup(qrods, rrod), color=PURPLE, scale_factor=1.05), run_time=0.8)
        self.add(wnd)

        self.at("zippers toward")
        vl.add_updater(lambda m: m.move_to([cx() + RV + 0.9, vy, 0]))
        self.play(z.animate.set_value(1.0), run_time=3.2, rate_func=smooth)
        vl.clear_updaters()
        # merge: the vesicle sinks into the target membrane
        self.at("until they fuse")
        self.remove(ves, rrod, wnd)
        ves_static = vesicle(RV).move_to([cx(), vy, 0])
        r_static = VGroup(rod(rows[2], cx() - RV - L, cx() - RV), rod(rows[3], cx() - RV - L, cx() - RV))
        self.add(ves_static, r_static)
        self.play(ves_static.animate.move_to([xt + RV + 0.12, vy, 0]), vl.animate.move_to([xt + 2 * RV + 1.0, vy, 0]),
                  FadeOut(r_static), FadeOut(qrods), FadeOut(qlab), FadeOut(rlab), run_time=0.8)
        self.play(FadeOut(ves_static), FadeOut(vl), hmem.animate.set_value(2.0), run_time=0.35)
        cis = VGroup(*[rod(y, base, base + 1.9) for y in rows])
        clab = VGroup(*[T(n, 26, PURPLE).move_to([lx, y, 0]) for n, y in zip(["Qa", "Qb", "Qc", "R"], rows)])
        self.play(hmem.animate.set_value(0.0), FadeIn(cis, shift=RIGHT * 0.3), run_time=0.7)
        self.at("all four sit")
        self.play(FadeIn(clab), FadeOut(legend), run_time=0.6)
        nsf = VGroup(bchip("NSF", PINK, 34), bchip("SNAP", PINK, 30)).arrange(RIGHT, buff=0.15).move_to([-0.4, 0.3, 0])
        atp = bchip("ATP", GOLD, 28).move_to([-0.4, 1.5, 0])
        self.at("uses")
        self.play(FadeIn(nsf, shift=LEFT * 0.3), run_time=0.6)
        self.at("ATP")
        self.play(FadeIn(atp, scale=0.8), run_time=0.5)
        spread = [2.4, 0.8, -0.8, -2.4]
        self.at("pull them apart")
        self.play(*[r.animate.move_to([r.get_center()[0], sy, 0]) for r, sy in zip(cis, spread)],
                  *[l.animate.move_to([lx, sy, 0]) for l, sy in zip(clab, spread)],
                  FadeOut(nsf), FadeOut(atp),
                  run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Apart(SpokenScene):
    """a table of three experiments; a token walks the steps bud, target, fuse and stops where each one fails."""

    def construct(self):
        cols = [-0.9, 2.2, 5.3]
        rows = [2.2, 0.0, -2.2]
        names = ["bud", "target", "fuse"]
        nodes = []
        for r in rows:
            rn = []
            for x, n in zip(cols, names):
                box = RoundedRectangle(corner_radius=0.16, width=2.4, height=1.5, stroke_color=GREY, stroke_width=3,
                                       fill_color=GREY, fill_opacity=0.1).move_to([x, r, 0])
                lab = T(n, 28, GREY).move_to([x, r + 0.48, 0])
                rn.append(VGroup(box, lab))
            nodes.append(rn)

        def spot(node):          # where the token rests inside a node (below the label)
            return node[0].get_center() + DOWN * 0.3

        arrows = []
        for rn in nodes:
            for a, b in zip(rn[:-1], rn[1:]):
                arrows.append(arr(a[0].get_right(), b[0].get_left(), GREY, w=4))
        nodes[2][0].set_opacity(0.0)      # liposomes: no budding step
        arrows.pop(4)
        self.at("Test tubes")
        self.play(FadeIn(VGroup(*[n for rn in nodes for n in rn]), lag_ratio=0.1), run_time=1.2)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.6)

        def paint(node, color):
            return [node[0].animate.set_stroke(color).set_fill(color, 0.22), node[1].animate.set_color(color)]

        lab1 = tag("GMP-PNP", ORANGE, 30).move_to([-4.6, rows[0], 0])
        lab2 = tag("GDI after docking", PINK, 30).move_to([-4.6, rows[1], 0])
        lab3 = tag("truncated HOPS", TEAL, 30).move_to([-4.6, rows[2], 0])

        # ---- row 1
        t1 = vesicle(0.34).move_to([-2.45, rows[0], 0])
        self.at("Vesicles made with")
        self.play(FadeIn(lab1), FadeIn(t1), run_time=0.6)
        self.at("still formed")
        self.play(t1.animate.move_to(spot(nodes[0][0])), run_time=0.7)
        self.play(*paint(nodes[0][0], GREEN), run_time=0.4)
        ring1 = DashedVMobject(Circle(radius=0.5, stroke_color=BLUE, stroke_width=8, stroke_opacity=0.85),
                               num_dashes=12, dashed_ratio=0.7).move_to(t1)
        self.at("kept their coat")
        self.play(FadeIn(ring1), run_time=0.5)
        self.at("failed to target")
        self.play(VGroup(t1, ring1).animate.move_to(spot(nodes[0][1])), run_time=0.6)
        self.play(*paint(nodes[0][1], RED), *paint(nodes[0][2], RED), run_time=0.6)

        # ---- row 2
        t2 = vesicle(0.34).move_to([-2.45, rows[1], 0])
        self.at("Once vesicles")
        self.play(FadeIn(lab2), FadeIn(t2), run_time=0.6)
        self.at("had docked")
        self.play(t2.animate.move_to(spot(nodes[1][1])), run_time=0.9)
        self.play(*paint(nodes[1][0], GREEN), *paint(nodes[1][1], GREEN), run_time=0.5)
        gdi = bchip("GDI", PINK, 22, pad=0.12).move_to([cols[2], rows[1] + 1.1, 0])
        self.at("no longer cared")
        self.play(FadeIn(gdi, shift=DOWN * 0.2), run_time=0.4)
        self.play(gdi.animate.shift(LEFT * 0.3), run_time=0.3)
        self.play(gdi.animate.shift(RIGHT * 1.0).set_opacity(0.0), run_time=0.4)
        self.play(t2.animate.move_to(spot(nodes[1][2])), run_time=0.7)
        self.play(*paint(nodes[1][2], GREEN), run_time=0.4)

        # ---- row 3
        t3 = Circle(radius=0.34, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.16)
        t3.move_to([-2.45, rows[2], 0])
        self.at("Truncated")
        self.play(FadeIn(lab3), FadeIn(t3), run_time=0.6)
        self.at("still tethered")
        self.play(t3.animate.move_to(spot(nodes[2][1])), run_time=0.9)
        self.play(*paint(nodes[2][1], GREEN), run_time=0.4)
        self.at("failed to promote")
        self.play(*paint(nodes[2][2], RED), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """three step chips; the sec1 token passes the coat and stalls; the rule."""

    def construct(self):
        head = bchip("sec1 at 37 °C", RED, 32).move_to([0, 3.0, 0])
        self.at("Back to")
        self.play(FadeIn(head), run_time=0.6)
        ys = -0.3
        c1 = bchip("coat", BLUE, 46, pad=0.45).move_to([-4.9, ys, 0])
        c2 = bchip("Rab + tether", TEAL, 46, pad=0.45).move_to([0.0, ys, 0])
        c3 = bchip("SNAREs", PURPLE, 46, pad=0.45).move_to([4.9, ys, 0])
        s1 = T("to bud", 30, GREY).next_to(c1, DOWN, buff=0.4)
        s2 = T("to be caught", 30, GREY).next_to(c2, DOWN, buff=0.4)
        s3 = T("to fuse", 30, GREY).next_to(c3, DOWN, buff=0.4)
        a1 = arr(c1.get_right(), c2.get_left(), GREY, w=6, tip=0.25)
        a2 = arr(c2.get_right(), c3.get_left(), GREY, w=6, tip=0.25)
        self.at("a coat to bud")
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(s1), run_time=0.6)
        self.at("and a tether")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.2), FadeIn(s2), run_time=0.7)
        self.at("SNAREs to fuse")
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.2), FadeIn(s3), run_time=0.7)

        tok = vesicle(0.5).move_to([c1.get_center()[0], ys + 1.7, 0])
        self.at("vesicles formed")
        self.play(FadeIn(tok, shift=DOWN * 0.3), run_time=0.5)
        ok = check([0, 0, 0], GREEN, 0.3, 9)
        ok.next_to(tok, RIGHT, buff=0.35)
        self.at("coat worked")
        self.play(Create(ok), c1[1].animate.set_stroke(GREEN), c1[2].animate.set_color(GREEN), run_time=0.7)
        self.play(tok.animate.move_to([(c1.get_right()[0] + c2.get_left()[0]) / 2, ys + 1.7, 0]),
                  FadeOut(ok), run_time=0.7)
        br = Brace(VGroup(c2, c3), direction=DOWN, color=RED, buff=1.3)
        q = bchip("?", RED, 44).next_to(br, DOWN, buff=0.15)
        self.at("later step failed")
        self.play(GrowFromCenter(br), FadeIn(q, scale=0.6), run_time=0.8)

        self.at("can fail alone")
        self.play(FadeOut(br), FadeOut(q), run_time=0.3)
        for c, col in [(c1, BLUE), (c2, TEAL), (c3, PURPLE)]:
            self.play(c[1].animate.set_stroke(RED).set_fill(RED, 0.2), c[2].animate.set_color(RED), run_time=0.35)
            self.play(c[1].animate.set_stroke(col).set_fill(col, 0.16), c[2].animate.set_color(col), run_time=0.35)
        self.at("separate steps")
        self.play(*[c.animate.scale(1.07) for c in (c1, c2, c3)], run_time=0.5)
        self.play(*[c.animate.scale(1 / 1.07) for c in (c1, c2, c3)], run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Budding, targeting and fusion are separate steps."
