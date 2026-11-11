"""Reading a Broken Machine (chapter 2 of Cell shape, migration and cilia).

COLOR MAP (identical to chapter 1)
  TEAL    actin / interactive tag / scanning line
  YELLOW  dynein motion, ATP
  GREEN   visible output, mucus transport, 'looks normal'
  BLUE    complete A-tubule, cilium shaft
  PURPLE  incomplete B-tubule
  ORANGE  mechanical constraints: links, integrin clutch, 'same axoneme' bracket
  MAGENTA motor control
  GREY    body, membrane, dish, structure
  RED     cut / stopped / defective
Everything is schematic.
"""
import importlib.util
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

_here = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
_ch1_path = _here.parent / "scenes.py"
_spec = importlib.util.spec_from_file_location("ch1_scenes", str(_ch1_path))
_ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ch1)
PURPLE, ORANGE, MAGENTA = _ch1.PURPLE, _ch1.ORANGE, _ch1.MAGENTA
WorkbenchScene, arrow, small_label = _ch1.WorkbenchScene, _ch1.arrow, _ch1.small_label
long_pair, doublet_cross, split_bench = _ch1.long_pair, _ch1.doublet_cross, _ch1.split_bench

MUCUS = "#BFE3EC"
DUST = "#8A6F5A"
PINK = "#E58FA6"
WHITE = "#FFFFFF"


def lerp(a, b, u):
    return a + (b - a) * u


def now(scene):
    return scene.renderer.time


# ---------------------------------------------------------------- shared pieces
def body(cx=0.0, cy=0.0, s=1.0):
    """Grey human outline; .airway, .groin, .vessel are the three white circles."""
    P = lambda x, y: np.array([cx + x * s, cy + y * s, 0.0])
    sw = 15 * s
    head = Circle(radius=.48 * s, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to(P(0, 2.45))
    torso = RoundedRectangle(width=1.5 * s, height=2.55 * s, corner_radius=.5 * s, color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=.25).move_to(P(0, .72))
    limbs = VGroup(Line(P(-.85, 1.85), P(-1.45, -.45)), Line(P(.85, 1.85), P(1.45, -.45)),
                   Line(P(-.35, -.5), P(-.5, -3.0)), Line(P(.35, -.5), P(.5, -3.0)))
    limbs.set_stroke(GREY, sw, opacity=.5)
    for l in limbs:
        l.set_cap_style(CapStyleType.ROUND)
    r = max(.13, .27 * s)
    sw_c = max(3, 5 * s)
    mk = lambda p: Circle(radius=r, color=WHITE, stroke_width=sw_c, fill_color=WHITE, fill_opacity=0).move_to(p)
    g = VGroup(limbs, torso, head)
    g.limbs, g.torso, g.head = limbs, torso, head
    g.airway, g.groin, g.vessel = mk(P(0, 1.72)), mk(P(0, -.35)), mk(P(1.13, .75))
    g.circles = VGroup(g.airway, g.groin, g.vessel)
    g.add(g.circles)
    return g


def lit(c, on=1.0, speed=3.0, ph=0.0):
    """Make a white circle pulse (lit)."""
    c.pt = ph

    def f(m, dt):
        m.pt += dt
        m.set_fill(WHITE, on * (.22 + .22 * np.sin(speed * m.pt)))
    c.add_updater(f)
    return c


def qmark(size=96, pos=(0, 0, 0)):
    q = T("?", size, WHITE).move_to(pos)
    q.pt = 0.0

    def f(m, dt):
        m.pt += dt
        m.set_opacity(.6 + .4 * np.sin(3.2 * m.pt))
    q.add_updater(f)
    return q


def dish_icon():
    return VGroup(Circle(radius=.66, color=GREY, stroke_width=3, fill_color=TEAL, fill_opacity=.07),
                  Line([-.45, -.1, 0], [.45, -.1, 0], color=WHITE, stroke_width=4)).move_to([-5.9, 2.2, 0])


def ring9(cx, cy, r, arms="solid"):
    """9+2 cross-section: grey outline, nine blue/purple doublets, grey central pair, yellow outer arms."""
    dr = .18 * r
    outline = Circle(radius=r + dr * 2.2, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.05).move_to([cx, cy, 0])
    ds, solid, dashed = VGroup(), VGroup(), VGroup()
    for i in range(9):
        a = PI / 2 + TAU * i / 9
        u = np.array([np.cos(a), np.sin(a), 0])
        d = doublet_cross(dr, a - PI / 2)
        d.shift(np.array([cx, cy, 0]) + r * u - d[1].get_center())
        ds.add(d)
        p0 = np.array([cx, cy, 0]) + (r + dr) * u
        p1 = np.array([cx, cy, 0]) + (r + dr * 2.0) * u
        arm = VGroup(Line(p0, p1, color=YELLOW, stroke_width=max(3, 7 * r / 1.8)),
                     Circle(radius=dr * .32, color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=1).move_to(p1))
        solid.add(arm)
        dl = DashedVMobject(Line(p0, p1), num_dashes=3).set_stroke(YELLOW, max(3, 6 * r / 1.8))
        dc = DashedVMobject(Circle(radius=dr * .32).move_to(p1), num_dashes=6).set_stroke(YELLOW, 3)
        dashed.add(VGroup(dl, dc))
    cp = VGroup(*[Circle(dr * .8, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.25) for _ in range(2)])
    cp.arrange(RIGHT, buff=dr * .3).move_to([cx, cy, 0])
    g = VGroup(outline, ds, cp, solid if arms == "solid" else dashed)
    g.outline, g.ds, g.cp, g.solid, g.dashed = outline, ds, cp, solid, dashed
    return g


def drift_group(m, amp=.07, w=.9, ph=0.0):
    """Very slow floating of a whole diagram (no rotation)."""
    m.t0 = ph
    m.last = np.zeros(3)

    def f(mm, dt):
        mm.t0 += dt
        new = np.array([amp * np.sin(w * mm.t0), amp * .8 * np.cos(.8 * w * mm.t0), 0])
        mm.shift(new - mm.last)
        mm.last = new
    m.add_updater(f)
    return m


def cilia_row(scene, xs, y0, L, amp, mode="beat", color=BLUE, sw=8, wave=.8):
    """Cilia as straight rods whose tilt is computed from a travelling wave. amp: ValueTracker (0 = stopped)."""
    g = VGroup()
    for x in xs:
        c = Line([x, y0, 0], [x, y0 + L, 0], color=color, stroke_width=sw)
        c.set_cap_style(CapStyleType.ROUND)

        def f(m, dt, x=x):
            t = now(scene)
            th = np.sin(2.6 * t - wave * x)
            if mode == "stutter":
                th = th * (.45 + .55 * np.sin(1.1 * t + 2.0 * x) ** 2) + .25 * np.sin(5.3 * t + x)
            th = .65 * amp.get_value() * th
            m.put_start_and_end_on([x, y0, 0], [x + L * np.sin(th), y0 + L * np.cos(th), 0])
        c.add_updater(f)
        g.add(c)
    return g


def mouse(cx, cy, s=1.0):
    P = lambda x, y: np.array([cx + x * s, cy + y * s, 0])
    bodyo = Ellipse(width=2.8 * s, height=1.5 * s, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to(P(0, 0))
    head = Circle(radius=.5 * s, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to(P(1.55, .2))
    ear = Circle(radius=.25 * s, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to(P(1.35, .7))
    eye = Dot(P(1.8, .3), radius=.06, color=TEXT)
    tail = ParametricFunction(lambda t: P(-1.4 - 1.2 * t, -.1 + .5 * np.sin(3 * t)), t_range=[0, 1, .02], color=GREY, stroke_width=6)
    legs = VGroup(Line(P(-.6, -.7), P(-.6, -1.1)), Line(P(.6, -.7), P(.6, -1.1))).set_stroke(GREY, 8)
    return VGroup(tail, legs, bodyo, head, ear, eye)


def dyn_icon(center, arm_len=.9):
    """One doublet with a dashed (missing) dynein arm above it."""
    d = doublet_cross(.55, 0).move_to(center)
    top = d[1].get_center() + UP * .55
    arm = VGroup(DashedVMobject(Line(top, top + UP * arm_len), num_dashes=5).set_stroke(YELLOW, 9),
                 DashedVMobject(Circle(.15).move_to(top + UP * (arm_len + .1)), num_dashes=8).set_stroke(YELLOW, 4))
    return VGroup(d, arm)


# ---------------------------------------------------------------- scenes
class S00Link(WorkbenchScene, TitleCard):
    LESSON = "Cell shape, migration and cilia"
    TITLE = "Reading a Broken Machine"

    def construct(self):
        sl = ValueTracker(0.0)      # sliding of the cut pair
        cut = ValueTracker(0.0)     # 0 intact links, 1 cut
        u = ValueTracker(0.0)       # 0 big, 1 inset
        C0, C1 = np.array([0, -.1, 0]), np.array([-4.3, 2.6, 0])

        def pair():
            c = long_pair(origin=(-5.0, 0, 0), length=10.0, offset=.9, slide=sl.get_value(),
                          curved=.06 * (1 - cut.get_value()), links=False, anchor=False)
            k = cut.get_value()
            for s in np.linspace(1.2, 8.8, 5):
                if k < .5:
                    c.add(Line([-5 + s, -.45, 0], [-5 + s, .45, 0], color=ORANGE, stroke_width=6))
                else:
                    c.add(Line([-5 + s, -.45, 0], [-5 + s, .45, 0], color=ORANGE, stroke_width=6).set_opacity(.25))
                    c.add(T("×", 44, RED).move_to([-5 + s, 0, 0]))
            for i, s in enumerate(np.linspace(.8, 8.4, 8)):
                ph = (sl.get_value() * 3 + i * .37) % 1
                x = s + .3 * np.sin(2 * PI * ph)
                c.add(VGroup(Line([-5 + x, -.45, 0], [-5 + x + .35, -.1, 0], color=YELLOW, stroke_width=8),
                             Dot([-5 + x + .35, -.1, 0], .13, color=YELLOW)))
            sc = lerp(1, .26, u.get_value())
            c.scale(sc, about_point=ORIGIN)
            c.move_to(C0 * (1 - u.get_value()) + C1 * u.get_value())
            return c
        m = always_redraw(pair)
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD).move_to([0, 3.0, 0])
        title = T(self.TITLE, 46, font=TITLE_FONT).move_to([0, 2.3, 0])
        self.add(m)
        self.play(sl.animate.set_value(.25), FadeIn(brand), FadeIn(title), run_time=1.5, rate_func=linear)
        self.at("cut the links")
        self.play(cut.animate.set_value(1), FadeOut(brand), FadeOut(title), run_time=.6)
        self.at("doublets slid")
        self.play(sl.animate.set_value(1.6), run_time=2.9, rate_func=smooth)
        self.at("turn the question")
        b = body(1.4, 0, 1.0)
        b.circles.set_opacity(0)
        q = qmark(110, (-2.4, -.4, 0))
        sch = small_label("schematic", (5.0, -2.75, 0))
        self.play(u.animate.set_value(1), FadeIn(b.limbs), FadeIn(b.torso), FadeIn(b.head), FadeIn(q), FadeIn(sch), run_time=2.0)
        self.at("which part broke")
        self.play(sl.animate.set_value(2.0), run_time=1.0, rate_func=linear)
        self.at("where in the body")
        for c in b.circles:
            c.set_stroke(WHITE, 5, 1)
        self.play(LaggedStart(*[Create(c) for c in b.circles], lag_ratio=.3), run_time=1.3)
        drift_group(b, .05)
        self.finish()


def dish_world(scene):
    """The dish: grey ring, tinted water, six axoneme rods in two bundles."""
    dish = Circle(radius=2.45, color=GREY, stroke_width=6, fill_color=TEAL, fill_opacity=.07).move_to([0, -.4, 0])
    rods = VGroup()
    specs = [(-1.0, .6, .25), (-.88, .0, .22), (-1.05, -.7, .3), (.9, .3, -.2), (.75, -.5, -.15), (1.0, -1.0, -.25)]
    for x, y, a in specs:
        r = Line([x - .9, y - .9 * np.tan(a) - .4, 0], [x + .9, y + .9 * np.tan(a) - .4, 0], color=GREY, stroke_width=11)
        r.set_cap_style(CapStyleType.ROUND)
        r.ph = x * 3
        r.p0 = r.get_center().copy()

        def f(m, dt):
            t = now(scene)
            m.move_to(m.p0 + np.array([.09 * np.sin(.8 * t + m.ph), .09 * np.cos(.7 * t + m.ph), 0]))
        r.add_updater(f)
        rods.add(r)
    return dish, rods


class S01Dish(WorkbenchScene):
    def construct(self):
        b = body(0, 0, 1.0)
        for c in b.circles:
            c.set_stroke(WHITE, 5, 1)
        self.add(b)
        dish, rods = dish_world(self)
        title = T("1971: Summers and Gibbons", 32, TEXT).move_to([0, 2.72, 0])
        self.play(b.animate.shift(LEFT * 9), GrowFromCenter(dish), FadeIn(title), run_time=2.0)
        self.remove(b)
        ripples = VGroup(*[Circle(radius=.5, color=TEAL, stroke_width=3) for _ in range(3)]).move_to([0, -.4, 0])
        for k, rp in enumerate(ripples):
            rp.k = k

            def rip(m, dt):
                ph = ((now(self) * .35) + m.k / 3.0) % 1.0
                m.become(Circle(radius=.4 + 1.9 * ph, color=TEAL, stroke_width=3).move_to([0, -.4, 0]).set_stroke(TEAL, 3, opacity=.5 * (1 - ph)))
            rp.add_updater(rip)
        self.add(ripples)
        ur = VGroup(Circle(.42, color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=.3),
                    *[Line(.42 * np.array([np.cos(a), np.sin(a), 0]), .72 * np.array([np.cos(a), np.sin(a), 0]), color=PURPLE, stroke_width=4)
                      for a in np.linspace(0, TAU, 13)[:-1]]).move_to([-4.9, 1.5, 0])
        ul = T("sea urchin", 28, PURPLE).next_to(ur, DOWN, buff=.25)
        self.play(FadeIn(ur, shift=DOWN * .3), FadeIn(ul), run_time=1.0)
        self.at("sea urchin sperm")
        sperm = VGroup()
        for i in range(len(rods)):
            sperm.add(VGroup(Dot([-4.2, 1.5 - .1 * i, 0], .16, color=TEXT),
                             Line([-4.2, 1.5 - .1 * i, 0], [-3.6, 1.2 - .1 * i, 0], color=TEXT, stroke_width=4)))
        self.play(FadeIn(sperm), run_time=.4)
        self.play(LaggedStart(*[sp.animate.shift(RIGHT * (3.4 + .1 * i) + DOWN * (1.2 + .2 * i)) for i, sp in enumerate(sperm)], lag_ratio=.1), run_time=1.3)
        axl = T("axonemes", 30, TEXT).move_to([4.6, 1.2, 0])
        self.play(*[ReplacementTransform(sp, r) for sp, r in zip(sperm, rods)], FadeIn(axl), FadeOut(ur), FadeOut(ul), run_time=1.0)
        sch = small_label("schematic", (4.6, -2.75, 0))
        self.at("briefly treated")
        pairs = [(0, 1), (1, 2), (3, 4), (4, 5)]
        links = VGroup()
        for a, bq in pairs:
            l = Line(rods[a].get_center(), rods[bq].get_center(), color=ORANGE, stroke_width=6)
            l.add_updater(lambda m, dt, a=a, bq=bq: m.put_start_and_end_on(rods[a].get_center(), rods[bq].get_center()))
            links.add(l)
        self.play(FadeIn(links), FadeOut(axl), FadeIn(sch), run_time=.8)
        self.at("trypsin")
        blocks = VGroup(*[Square(.34, color=RED, stroke_width=3, fill_color=RED, fill_opacity=.7).move_to([-3.0 + 1.0 * i, 2.1, 0]) for i in range(3)])
        tl = T("trypsin", 32, "#FF8A80").move_to([-4.6, -.2, 0])
        self.add(blocks)
        self.play(FadeIn(tl), LaggedStart(*[bk.animate.move_to(l.get_center() + UP * .1) for bk, l in zip(blocks, [links[0], links[2], links[3]])], lag_ratio=.25), run_time=1.3)
        self.play(links.animate.set_color(RED), run_time=.4)
        self.play(FadeOut(links), blocks.animate.set_opacity(0), run_time=.7)
        self.at("then added")
        self.play(FadeOut(tl), run_time=.4)
        al = M("ATP 0.1 mM", 30, YELLOW).move_to([4.7, .4, 0])
        sp = VGroup(*[Dot([-1.6 + .4 * i, 1.7 + .1 * (i % 3) - 1.0 * (i % 4) * .0 - (i % 4) * .9, 0], .1, color=YELLOW) for i in range(9)])

        def fall(m, dt):
            for d in m:
                d.shift(DOWN * 1.4 * dt)
                if d.get_y() < -2.2:
                    d.shift(UP * 4.0)
        sp.add_updater(fall)
        self.add(sp)
        self.play(FadeIn(al), run_time=.8)
        self.finish()


class S02Slide(WorkbenchScene):
    def construct(self):
        dish, rods = dish_world(self)
        sch = small_label("schematic", (4.7, -2.75, 0))
        dark = Circle(radius=2.45, color=GREY, stroke_width=6, fill_color="#000000", fill_opacity=0).move_to([0, -.4, 0]).set_z_index(1)
        for r in rods:
            r.set_z_index(2)
        self.add(dish, rods, sch, dark)
        self.play(dark.animate.set_fill("#000000", 1), rods.animate.set_color(WHITE), run_time=1.6)
        self.at("did not beat")
        dl = T("did not beat", 34, WHITE).move_to([4.3, 1.4, 0])
        self.play(FadeIn(dl), run_time=.9)
        self.at("Groups of doublets")
        sl = ValueTracker(0.0)

        def bundle():
            g = VGroup()
            for i in range(9):
                grp = i // 3
                off = [-.8, 0, .8][grp] * sl.get_value()
                y = -.4 + (i % 3) * .28 - .28 + (grp - 1) * .35
                g.add(Line([-1.5 + off, y, 0], [1.5 + off, y, 0], color=WHITE, stroke_width=9).set_cap_style(CapStyleType.ROUND))
            g.set_z_index(3)
            return g
        bun = always_redraw(bundle)
        self.play(FadeOut(rods), FadeIn(bun), run_time=.8)
        self.at("slid out of the bundle")
        self.play(sl.animate.set_value(1.0), run_time=2.0)
        self.at("That dish test")
        tag = chip("test: do the motors work?", TEAL, 30).move_to([0, 2.6, 0]).set_z_index(5)
        self.play(FadeIn(tag, shift=DOWN * .2), run_time=.9)
        self.play(sl.animate.set_value(1.25), run_time=3.2, rate_func=linear)
        self.at("motors work")
        grp = VGroup(dish, dark, bun, dl, tag, sch)
        self.play(grp.animate.scale(.3).move_to([-5.9, 2.15, 0]), run_time=1.6)
        self.finish()


class S03Afzelius(WorkbenchScene):
    def construct(self):
        d = dish_icon()
        self.add(d)
        b = body(-3.0, 0, 1.0)
        for c in b.circles:
            c.set_stroke(WHITE, 5, 1)
        self.play(FadeIn(b), run_time=1.0)
        lit(b.groin)
        drift_group(b, .04)
        self.at("In 1976")
        sp = VGroup()
        for i in range(4):
            y = 1.9 - i * 1.15
            sp.add(VGroup(Ellipse(width=.5, height=.34, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.5).move_to([.2, y, 0]),
                          Line([.45, y, 0], [3.0, y, 0], color=TEXT, stroke_width=5)))
        lab = T("1976: sperm do not swim", 32, TEXT).move_to([3.2, 2.75, 0])
        self.at("four men")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * .3) for s in sp], lag_ratio=.2), run_time=1.2)
        self.at("sperm did not swim")
        self.play(FadeIn(lab), run_time=.9)
        self.at("Electron microscopy")
        ring = ring9(0.9, -.1, 1.9, arms="solid")
        self.play(FadeOut(sp), FadeOut(lab), b.animate.scale(.5).move_to([-5.9, -.55, 0]), run_time=1.0)
        self.play(FadeIn(ring.outline), LaggedStart(*[FadeIn(x, scale=.6) for x in ring.ds], lag_ratio=.05), FadeIn(ring.cp), run_time=1.3)
        drift_group(ring, .06)
        self.at("dynein arms")
        self.play(LaggedStart(*[FadeIn(a, scale=.5) for a in ring.solid], lag_ratio=.08), run_time=1.5)
        self.at("outer doublet")
        self.play(Indicate(ring.solid, color=YELLOW), run_time=1.2)
        self.at("were missing")
        ml = T("dynein arms\nmissing", 32, YELLOW, line_spacing=.8).move_to([4.9, 0, 0])
        self.play(ReplacementTransform(ring.solid, ring.dashed), FadeIn(ml), run_time=1.4)
        self.finish()


class PredictFrame:
    """Everything on the question card; built identically in s04 and s05."""
    def __init__(self):
        self.body = body(-5.9, -.55, .5)
        for c in self.body.circles:
            c.set_stroke(WHITE, 3, 1)
        self.ring_s = ring9(-1.9, -.55, 1.3, arms="dashed")
        self.ring_a = ring9(2.9, -.55, 1.3, arms="dashed")
        self.l_s = T("sperm tail", 28, TEXT).move_to([-1.9, -2.7, 0])
        self.l_a = T("airway cilium", 28, TEXT).move_to([2.9, -2.7, 0])
        self.brk = VGroup(Line([-1.9, 1.65, 0], [2.9, 1.65, 0], color=ORANGE, stroke_width=6),
                          Line([-1.9, 1.65, 0], [-1.9, 1.35, 0], color=ORANGE, stroke_width=6),
                          Line([2.9, 1.65, 0], [2.9, 1.35, 0], color=ORANGE, stroke_width=6))
        self.l_b = T("same basic axoneme", 30, ORANGE).move_to([.5, 2.1, 0])
        self.q = T("Arms missing: what else fails?", 40, WHITE).move_to([.2, 2.85, 0])
        self.qm = qmark(48, (-5.25, .5, 0))
        self.dish = dish_icon()


class S04Predict(WorkbenchScene):
    def construct(self):
        f = PredictFrame()
        carried = ring9(.9, -.1, 1.9, arms="dashed")
        ml = T("dynein arms\nmissing", 32, YELLOW, line_spacing=.8).move_to([4.9, 0, 0])
        b = f.body
        self.add(carried, ml, b, f.dish)
        lit(b.groin)
        drift_group(carried, .05)
        self.play(FadeOut(ml), run_time=.6)
        self.at("lining the airways")
        rs = f.ring_s
        ra = f.ring_a
        self.play(FadeOut(carried), FadeIn(rs), FadeIn(f.l_s), FadeIn(ra), FadeIn(f.l_a), run_time=1.2)
        lit(b.airway)
        self.at("same basic")
        self.play(Create(f.brk), FadeIn(f.l_b), run_time=1.6)
        self.at("So predict")
        self.play(FadeIn(f.q, shift=DOWN * .2), run_time=1.0)
        self.at("dynein arms")
        self.play(Indicate(VGroup(rs.dashed, ra.dashed), color=YELLOW), run_time=1.5)
        self.at("what else should fail")
        self.add(f.qm)
        drift_group(rs, .04)
        drift_group(ra, .04, ph=1.5)
        self.finish()


class S05Pause(WorkbenchScene):
    def construct(self):
        f = PredictFrame()
        lit(f.body.airway)
        lit(f.body.groin)
        self.add(f.body, f.dish, f.ring_s, f.ring_a, f.l_s, f.l_a, f.brk, f.l_b, f.q, f.qm)
        for r, ph in ((f.ring_s, 0), (f.ring_a, 1.0)):
            r.dashed.pt = ph

            def shimmer(m, dt):
                m.pt += dt
                m.set_opacity(.55 + .45 * np.sin(3 * m.pt))
            r.dashed.add_updater(shimmer)
            r.outline.pt = ph

            def pulse(m, dt):
                m.pt += dt
                m.set_stroke(GREY, 4 + 2 * np.sin(2.2 * m.pt))
            r.outline.add_updater(pulse)
        self.wait(4.5)


class S06Reveal(WorkbenchScene):
    def construct(self):
        amp = ValueTracker(1.0)
        flow = ValueTracker(1.0)
        xs = list(np.linspace(-5.4, 5.4, 12))
        sheet = RoundedRectangle(width=12.4, height=.5, corner_radius=.15, color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=.45).move_to([0, -2.55, 0])
        cil = cilia_row(self, xs, -2.3, 2.0, amp, wave=.9)
        mucus = Rectangle(width=12.4, height=.7, color=MUCUS, stroke_width=0, fill_color=MUCUS, fill_opacity=.28).move_to([0, .35, 0])
        mcap = T("mucus", 30, MUCUS).move_to([-5.3, 1.45, 0])
        specks = VGroup(*[Dot([-5.8 + 1.5 * i, .35 + .15 * ((i * 7) % 3 - 1), 0], .13, color=DUST) for i in range(8)])

        def sp(m, dt):
            for dd in m:
                dd.shift(RIGHT * 1.0 * flow.get_value() * dt)
                if dd.get_x() > 6.0:
                    dd.shift(LEFT * 12.0)
        specks.add_updater(sp)
        arrows = VGroup(*[arrow([-4.6 + 3.1 * i, .9, 0], [-3.0 + 3.1 * i, .9, 0], GREEN, 7) for i in range(4)])
        arrows.add_updater(lambda m, dt: m.set_opacity(flow.get_value()))
        self.play(FadeIn(sheet), FadeIn(mucus), run_time=.8)
        self.add(cil, specks)
        self.play(FadeIn(arrows), FadeIn(mcap), run_time=1.0)
        self.at("bronchitis")
        c1 = chip("bronchitis", RED, 30).move_to([-3.2, 2.55, 0])
        self.play(FadeIn(c1, shift=DOWN * .2), run_time=.8)
        self.at("sinusitis")
        c2 = chip("sinusitis", RED, 30).move_to([0.2, 2.55, 0])
        self.play(FadeIn(c2, shift=DOWN * .2), run_time=.8)
        self.at("Their airway cilia")
        self.play(FadeOut(c1), FadeOut(c2), run_time=.6)
        self.at("not moving mucus")
        pl = T("patients: cilia not beating", 32, RED).move_to([-1.0, 2.5, 0])
        self.play(amp.animate.set_value(0), flow.animate.set_value(0), FadeIn(pl), FadeOut(mcap), run_time=1.6)
        self.at("sweep called")
        inset_bg = RoundedRectangle(width=5.0, height=2.4, corner_radius=.15, color=GREEN, stroke_width=3,
                                    fill_color=BG, fill_opacity=1).move_to([3.5, 1.9, 0]).set_z_index(5)
        amp2 = ValueTracker(1.0)
        ic = cilia_row(self, [2.0, 2.7, 3.4, 4.1, 4.8], 1.0, .75, amp2, wave=1.2, sw=6).set_z_index(6)
        ia = arrow([2.0, 2.45, 0], [4.9, 2.45, 0], GREEN, 7).set_z_index(6)
        il = T("normal", 28, GREEN).move_to([5.1, 2.75, 0]).set_z_index(6)
        self.play(FadeOut(pl), FadeIn(inset_bg), FadeIn(ia), FadeIn(il), FadeIn(ic), run_time=1.0)
        self.at("mucociliary transport")
        mt = T("mucociliary transport", 32, GREEN).move_to([-2.9, 1.7, 0]).set_z_index(7)
        self.play(FadeIn(mt), Indicate(ia, color=GREEN), run_time=1.2)
        self.at("One missing part")
        gone = VGroup(sheet, cil, mucus, specks, arrows, inset_bg, ic, ia, il, mt)
        self.play(FadeOut(gone), run_time=.6)
        air = lit(Circle(.5, color=WHITE, stroke_width=6).move_to([-3.6, 1.2, 0]))
        sperm = lit(Circle(.5, color=WHITE, stroke_width=6).move_to([-3.6, -1.4, 0]), ph=1.0)
        al = T("airway", 30, WHITE).next_to(air, LEFT, buff=.3)
        sl = T("sperm", 30, WHITE).next_to(sperm, LEFT, buff=.3)
        icon = dyn_icon([3.4, -.5, 0])
        idl = T("missing dynein arm", 32, YELLOW).move_to([3.4, -2.2, 0])
        l1 = Line(air.get_right(), icon.get_left() + UP * .3, color=ORANGE, stroke_width=6)
        l2 = Line(sperm.get_right(), icon.get_left() + DOWN * .3, color=ORANGE, stroke_width=6)
        self.play(FadeIn(air), FadeIn(sperm), FadeIn(al), FadeIn(sl), FadeIn(icon), FadeIn(idl), run_time=.9)
        self.play(Create(l1), Create(l2), run_time=1.0)
        self.at("two organs")
        self.play(Indicate(air, color=WHITE), Indicate(sperm, color=WHITE), Indicate(icon, color=YELLOW), run_time=1.2)
        self.finish()


class S07Tissues(WorkbenchScene):
    def construct(self):
        rs = ring9(-2.6, -.4, 1.45, arms="solid")
        ra = ring9(2.6, -.4, 1.45, arms="solid")
        ls = T("sperm tail", 28, TEXT).move_to([-2.6, -2.7, 0])
        la = T("airway cilium", 28, TEXT).move_to([2.6, -2.7, 0])
        brk = VGroup(Line([-2.6, 1.7, 0], [-.35, 1.7, 0], color=ORANGE, stroke_width=6), Line([.35, 1.7, 0], [2.6, 1.7, 0], color=ORANGE, stroke_width=6),
                     Line([-2.6, 1.7, 0], [-2.6, 1.4, 0], color=ORANGE, stroke_width=6), Line([2.6, 1.7, 0], [2.6, 1.4, 0], color=ORANGE, stroke_width=6))
        self.add(rs, ra, ls, la, brk)
        drift_group(rs, .05)
        drift_group(ra, .05, ph=1.5)
        self.at("not perfect")
        gap = T("≠", 60, RED).move_to([0, 1.7, 0])
        self.play(FadeIn(gap, scale=1.4), run_time=1.0)
        self.at("differ in some")
        self.play(Indicate(VGroup(rs.solid[0], rs.solid[1], rs.solid[2]), color=WHITE, scale_factor=1.3),
                  Indicate(VGroup(ra.solid[1], ra.solid[2], ra.solid[3]), color=WHITE, scale_factor=1.3), run_time=1.6)
        dl = T("some dynein parts differ", 32, YELLOW).move_to([0, 2.8, 0])
        self.play(FadeIn(dl), run_time=.8)
        self.at("one mutation")
        hl = T("one mutation, different effects", 44, WHITE).move_to([0, 0, 0])
        self.play(*[FadeOut(x) for x in (rs, ra, ls, la, brk, gap, dl)], run_time=.8)
        self.play(FadeIn(hl, shift=UP * .2), run_time=1.0)
        drift_group(hl, .05)
        self.at("In mice lacking")
        mo = mouse(-4.9, 2.3, .55)
        self.play(hl.animate.scale(.75).move_to([0, -2.75, 0]), FadeIn(mo), run_time=1.3)
        self.at("protein called")
        blk = chip("Cfap53 missing", RED, 32).move_to([.1, 2.35, 0])
        self.play(FadeIn(blk, shift=DOWN * .2), run_time=.9)
        pxs = [-4.2, 0.0, 4.2]
        panels = []
        for px, name in zip(pxs, ["node", "windpipe", "brain ventricles"]):
            frame = RoundedRectangle(width=3.8, height=3.0, corner_radius=.15, color=GREY, stroke_width=3,
                                     fill_color=GREY, fill_opacity=.1).move_to([px, -.1, 0])
            nm = T(name, 28, TEXT).move_to([px, 1.15, 0])
            panels.append((frame, nm))
        arrs = [Arrow([.1, 2.0, 0], [px, 1.55, 0], buff=.1, color=TEXT, stroke_width=5, tip_length=.2) for px in pxs]
        ampn, ampw, ampv = ValueTracker(0.0), ValueTracker(1.0), ValueTracker(1.0)
        xs = lambda px: [px - 1.2, px - .4, px + .4, px + 1.2]
        sheets = [Line([px - 1.7, -1.35, 0], [px + 1.7, -1.35, 0], color=GREY, stroke_width=8) for px in pxs]
        cn = cilia_row(self, xs(pxs[0]), -1.3, 1.45, ampn, wave=.5, sw=7)
        cw = cilia_row(self, xs(pxs[1]), -1.3, 1.45, ampw, mode="stutter", wave=.9, sw=7)
        cv = cilia_row(self, xs(pxs[2]), -1.3, 1.45, ampv, mode="stutter", wave=1.3, sw=7)
        stop = VGroup(Circle(.33, color=RED, stroke_width=6), Line([-.2, -.2, 0], [.2, .2, 0], color=RED, stroke_width=6)).move_to([pxs[0] + 1.2, .45, 0])
        self.at("embryonic node")
        self.play(GrowArrow(arrs[0]), FadeIn(panels[0][0]), FadeIn(panels[0][1]), FadeIn(sheets[0]), run_time=1.0)
        self.add(cn)
        self.at("stopped completely")
        self.play(FadeIn(stop, scale=1.4), run_time=.9)
        self.at("Windpipe")
        self.play(GrowArrow(arrs[1]), FadeIn(panels[1][0]), FadeIn(panels[1][1]), FadeIn(sheets[1]), run_time=.9)
        self.add(cw)
        self.at("brain ventricle")
        self.play(GrowArrow(arrs[2]), FadeIn(panels[2][0]), FadeIn(panels[2][1]), FadeIn(sheets[2]), run_time=.9)
        self.add(cv)
        self.at("but abnormally")
        sch = small_label("schematic", (5.4, -2.75, 0))
        self.play(FadeIn(sch), run_time=.8)
        self.finish()


class S08Instrument(WorkbenchScene):
    def construct(self):
        lb = RoundedRectangle(width=5.8, height=4.2, corner_radius=.2, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.08).move_to([-3.35, -.45, 0])
        rb = RoundedRectangle(width=5.8, height=4.2, corner_radius=.2, color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.06).move_to([3.35, -.45, 0])
        lt = T("conventional EM", 32, TEXT).move_to([-3.35, 2.05, 0])
        rt = T("electron tomography", 32, TEAL).move_to([3.35, 2.05, 0])
        self.play(FadeIn(lb), FadeIn(rb), FadeIn(lt), FadeIn(rt), run_time=1.2)

        def scanner(box, ph, col):
            ln = Line(box.get_left() + RIGHT * .1, box.get_right() + LEFT * .1, color=col, stroke_width=3)
            ln.set_opacity(.6)
            ln.ph = ph
            ln.cy = box.get_center()[1]
            ln.cx = box.get_center()[0]

            def f(m, dt):
                m.move_to([m.cx, m.cy + 1.4 * np.sin(1.1 * now(self) + m.ph), 0])
            ln.add_updater(f)
            return ln
        sa, sb = scanner(lb, 0.0, GREY), scanner(rb, 1.5, TEAL)
        self.add(sa, sb)
        self.at("Patients with")
        pt = T("DNAH11 patients: nasal cilia", 30, TEXT).move_to([0, 2.95, 0])
        self.play(FadeIn(pt), run_time=.9)
        self.at("normal looking")
        ring = ring9(-3.35, -.1, 1.2, arms="solid")
        self.play(FadeIn(ring.outline), LaggedStart(*[FadeIn(x, scale=.6) for x in ring.ds], lag_ratio=.05), FadeIn(ring.cp), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(a, scale=.5) for a in ring.solid], lag_ratio=.05), run_time=1.0)
        drift_group(ring, .05)
        self.at("conventional electron")
        tick = T("✓ looks normal", 32, GREEN).move_to([-3.35, -2.2, 0])
        self.play(FadeIn(tick, shift=UP * .15), Indicate(lt, color=WHITE), run_time=1.0)
        self.at("Three dimensional")
        shrink = ValueTracker(0.0)
        rot = ValueTracker(0.0)
        cx, R = 3.35, 1.0
        ys = np.linspace(1.1, -1.6, 6)

        def tube():
            g = VGroup()
            g.add(Ellipse(width=2 * R + .35, height=.5, color=BLUE, stroke_width=3).move_to([cx, 1.5, 0]))
            g.add(Line([cx - R - .18, 1.5, 0], [cx - R - .18, -1.7, 0], color=BLUE, stroke_width=3))
            g.add(Line([cx + R + .18, 1.5, 0], [cx + R + .18, -1.7, 0], color=BLUE, stroke_width=3))
            t = rot.get_value()
            for i in range(9):
                ph = TAU * i / 9 + t
                z = np.cos(ph)
                x = cx + R * np.sin(ph)
                op = .35 + .65 * (z + 1) / 2
                g.add(Line([x, 1.4, 0], [x, -1.7, 0], color=BLUE, stroke_width=7).set_opacity(op))
                for j, y in enumerate(ys):
                    sz = .2
                    if j >= 4:
                        sz = .2 * (1 - .6 * shrink.get_value())
                    g.add(Square(sz, stroke_width=0, fill_color=YELLOW, fill_opacity=op).move_to([x + .1 + sz / 2, y, 0]))
            return g
        tb = always_redraw(tube)
        self.play(FadeIn(tb), rot.animate.set_value(1.6), run_time=1.0, rate_func=linear)
        self.play(rot.animate.set_value(3.8), run_time=2.2, rate_func=linear)
        self.at("less outer arm volume")
        lo = T("less outer-arm volume", 28, YELLOW).move_to([3.35, -2.25, 0]).set_z_index(5)
        self.play(shrink.animate.set_value(1.0), FadeIn(lo), rot.animate.set_value(5.4), run_time=1.3, rate_func=linear)
        self.at("near the base")
        self.play(Indicate(lo, color=YELLOW), rot.animate.set_value(6.6), run_time=1.0, rate_func=linear)
        tg = chip("one study", TEAL, 28).move_to([5.3, 2.95, 0])
        self.play(FadeIn(tg), rot.animate.set_value(9.0), run_time=.9, rate_func=linear)
        self.finish()


def neutrophil(defective=False, r=.75):
    body_ = Circle(radius=r, color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=.28)
    nuc = VGroup(*[Dot(radius=r * .17, color=WHITE).move_to([r * .35 * np.cos(a), r * .35 * np.sin(a), 0]) for a in (0, 2.1, 4.2)])
    blocks = VGroup()
    for a in (-1.0, -1.57, -2.14):
        p = np.array([r * np.cos(a), r * np.sin(a), 0])
        if defective:
            blk = DashedVMobject(Rectangle(width=.26, height=.44).move_to(p + DOWN * .12), num_dashes=10).set_stroke(ORANGE, 4)
        else:
            blk = Rectangle(width=.26, height=.44, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(p + DOWN * .12)
        blocks.add(blk)
    g = VGroup(body_, nuc, blocks)
    g.blocks = blocks
    return g


class S09Migration(WorkbenchScene):
    def construct(self):
        b = body(-5.9, -.55, .5)
        for c in b.circles:
            c.set_stroke(WHITE, 3, 1)
        lit(b.vessel)
        self.add(b)
        wall_y = -1.6
        vessel = Rectangle(width=11.2, height=2.6, stroke_width=0, fill_color=RED, fill_opacity=.14).move_to([.3, -.3, 0])
        wall_b = Line([-5.3, wall_y, 0], [5.9, wall_y, 0], color=PINK, stroke_width=12)
        wall_t = Line([-5.3, 1.0, 0], [5.9, 1.0, 0], color=PINK, stroke_width=12)
        self.play(FadeIn(vessel), Create(wall_b), Create(wall_t), run_time=1.2)
        n1 = neutrophil(False)
        n1.move_to([-3.9, -.82, 0])
        n1.blocks.set_opacity(0)
        self.add(n1)
        self.play(n1.animate.move_to([-.9, -.82, 0]).rotate(-4.0), run_time=2.2, rate_func=linear)
        self.at("integrins to grip")
        self.play(n1.blocks.animate.set_opacity(1), run_time=.6)
        il = T("integrin clutch", 30, ORANGE).move_to([-.9, .55, 0])
        self.play(FadeIn(il), n1.animate.move_to([-.2, -.85, 0]), run_time=.9)
        self.play(n1.animate.move_to([.55, -.9, 0]).stretch(1.15, 0).stretch(.85, 1), run_time=.9)
        bact = VGroup(*[Dot([3.2 + .4 * (i % 3), -2.45 - .25 * (i % 2), 0], .14, color=GREEN) for i in range(5)])
        self.add(bact)
        gm = T("grips the wall", 30, WHITE).move_to([-.9, 1.5, 0])
        self.at("without a working")
        self.play(FadeOut(il), FadeIn(gm), n1.animate.move_to([2.0, -2.35, 0]).scale(.7), run_time=2.2)
        self.at("beta two family")
        n2 = neutrophil(True)
        n2.move_to([-3.9, -.82, 0])
        dl = T("beta-2 integrin defective", 30, RED).move_to([-.4, 1.55, 0])
        self.play(FadeOut(gm), FadeOut(n1, shift=DOWN * .2), run_time=.5)
        self.play(FadeIn(dl), n2.animate.move_to([-1.5, -.82, 0]).rotate(-3.0), run_time=1.5, rate_func=linear)
        self.at("vessel wall")
        self.play(n2.animate.move_to([1.5, -.8, 0]).rotate(-2.0), run_time=1.5, rate_func=linear)
        self.at("largely fail")
        lad = T("leukocyte adhesion deficiency type I", 30, WHITE).move_to([0.3, 2.65, 0])
        self.play(FadeIn(lad), n2.animate.move_to([4.0, -.8, 0]).rotate(-3.0), run_time=2.1, rate_func=linear)
        self.at("infections are poorly")
        self.play(FadeOut(dl), n2.animate.move_to([6.3, -.8, 0]).rotate(-3.0), run_time=1.0, rate_func=linear)
        self.remove(n2)
        more = VGroup(*[Dot([2.9 + .35 * (i % 6) + (.15 if i > 5 else 0), -2.35 - .3 * (i // 6) - .1 * (i % 2), 0], .14, color=GREEN) for i in range(14)])
        self.play(FadeIn(more, lag_ratio=.15), run_time=2.2)
        self.finish()


class S10Idea(WorkbenchScene):
    def construct(self):
        bench = split_bench().set_opacity(.2).set_z_index(-10)
        self.add(bench)
        b = body(-4.4, -.1, 1.0)
        for c in b.circles:
            c.set_stroke(WHITE, 5, 1)
        self.play(FadeIn(b), run_time=1.0)
        for i, c in enumerate(b.circles):
            lit(c, ph=i)
        drift_group(b, .04)
        dyn = dyn_icon([1.4, 1.0, 0])
        dl = T("dynein arm", 32, YELLOW).next_to(dyn, RIGHT, buff=.3)
        clutch = DashedVMobject(Rectangle(width=.5, height=.9), num_dashes=24).set_stroke(ORANGE, 6).move_to([1.4, -1.9, 0])
        cl = T("integrin clutch", 32, ORANGE).next_to(clutch, RIGHT, buff=.3)
        self.at("tissue by tissue")
        self.play(*[Indicate(c, color=WHITE) for c in b.circles], run_time=1.5)
        self.at("which machine failed")
        self.play(bench.animate.set_opacity(.5), run_time=1.5)
        self.at("which part is defective")
        a1 = Arrow(b.airway.get_right(), dyn.get_left() + LEFT * .05, buff=.08, color=ORANGE, stroke_width=6)
        a2 = Arrow(b.groin.get_right(), dyn.get_bottom() + DOWN * .05, buff=.08, color=ORANGE, stroke_width=6)
        a3 = Arrow(b.vessel.get_right(), clutch.get_left() + LEFT * .05, buff=.08, color=ORANGE, stroke_width=6)
        self.play(FadeIn(dyn), FadeIn(dl), FadeIn(clutch), FadeIn(cl), GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=2.0)
        self.at("which tissue")
        self.play(*[Indicate(c, color=WHITE, scale_factor=1.5) for c in b.circles], run_time=1.5)
        self.at("with what instrument")
        self.play(Indicate(VGroup(a1, a2, a3), color=ORANGE), run_time=1.4)
        self.at("Motors and constraints")
        g_ = chip("constraint", ORANGE, 24).move_to([5.3, 2.8, 0])
        d_ = chip("motor control", MAGENTA, 24).move_to([2.55, 2.8, 0])
        self.play(bench.animate.set_opacity(.75), FadeIn(g_), FadeIn(d_), run_time=1.5)
        self.at("places to look")
        self.play(Indicate(g_, color=ORANGE), Indicate(d_, color=MAGENTA), run_time=1.4)
        self.finish()


class S11End(EndCard):
    LINE = "Read a phenotype backward to find the broken part, tissue by tissue."
