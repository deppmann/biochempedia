"""A Key Finds a Name, Not Relatives (grade 7 Life Science, film 2 of 2).

Same colour map as film 1 (one colour per box, lifted for the dark ground):
  DOMAIN = navy-blue   KINGDOM = indigo   PHYLUM = purple   CLASS = teal
  ORDER  = green       FAMILY  = gold     GENUS  = orange   SPECIES = coral red
One world: a slate-grey trail (the key) with white fork signposts and seven animal cards below it.
The key is drawn as a comb: the trail runs left to right, each fork drops a spur to one animal.
Everything not computed is schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

COL = ["#5B8DEF", "#8A7CF5", "#B574E6", "#3FB8C0", "#83C167", "#D4A843", "#F29E4C", "#FF6B5E"]
OUTLINE = "#1a1a22"
SLATE = "#7B8494"
SKIN = "#F1C9A5"

XS = [-5.4 + 1.8 * i for i in range(7)]
TY = 1.0
OLD = ["trout", "crab", "oyster", "star", "worm", "sponge", "nettle"]
NEW = ["trout", "oyster", "star", "crab", "worm", "sponge", "nettle"]
OLD_T = ["fins", "jointed\nlegs", "two-part\nshell", "five\narms", "ring-like\nsegments", "fixed,\nholes"]
NEW_T = ["fins", "two-part\nshell", "five\narms", "jointed\nlegs", "ring-like\nsegments", "fixed,\nholes"]
LABEL = dict(trout="brook\ntrout", crab="blue\ncrab", oyster="eastern\noyster", star="sea\nstar",
             worm="earth-\nworm", sponge="sponge", nettle="sea\nnettle")


# ------------------------------------------------------------------ cartoon icons
def _o(m, fill, sw=2.0):
    return m.set_fill(fill, 1).set_stroke(OUTLINE, sw)


def trout():
    g = VGroup()
    g.add(_o(Polygon([0.45, 0.0, 0], [0.82, 0.25, 0], [0.82, -0.25, 0]), "#7a8a45"))
    g.add(_o(Ellipse(width=1.15, height=0.5), "#8E9A4B").move_to([0, 0, 0]))
    g.add(_o(Polygon([-0.1, 0.22, 0], [0.15, 0.4, 0], [0.2, 0.2, 0]), "#7a8a45"))
    for p in [(-0.1, 0.05), (0.1, -0.08), (0.2, 0.08), (-0.25, -0.08), (0.0, 0.12)]:
        g.add(Dot([p[0], p[1], 0], radius=0.035, color="#F1E8C8"))
    g.add(Dot([-0.42, 0.06, 0], radius=0.045, color="#111"))
    return g


def crab():
    g = VGroup()
    for s in (-1, 1):
        for j in range(3):
            g.add(Line([s * 0.25, -0.1, 0], [s * (0.55 + 0.05 * j), -0.28 - 0.12 * j, 0], color="#3D7BD9", stroke_width=5))
        g.add(Line([s * 0.35, 0.05, 0], [s * 0.55, 0.32, 0], color="#3D7BD9", stroke_width=6))
        g.add(_o(Circle(radius=0.17), "#3D7BD9").move_to([s * 0.6, 0.42, 0]))
        g.add(_o(Polygon([s * 0.52, 0.5, 0], [s * 0.6, 0.66, 0], [s * 0.68, 0.5, 0]), "#3D7BD9", 1.5))
    g.add(_o(Ellipse(width=0.95, height=0.55), "#4A8DEB").move_to([0, -0.05, 0]))
    for s in (-1, 1):
        g.add(Dot([s * 0.12, 0.2, 0], radius=0.04, color="#111"))
    return g


def oyster():
    g = VGroup()
    g.add(_o(Ellipse(width=1.0, height=0.42), "#7E848E").move_to([0, -0.1, 0]))
    g.add(_o(Ellipse(width=0.98, height=0.42), "#A9AEB7").move_to([0.02, 0.12, 0]).rotate(0.08))
    for k in range(4):
        g.add(Arc(radius=0.3 + 0.07 * k, start_angle=0.5, angle=2.1, stroke_color="#7E848E", stroke_width=2).move_to([0.02, 0.12, 0]))
    g.add(Dot([-0.47, 0.0, 0], radius=0.05, color="#444"))
    return g


def star():
    g = VGroup(_o(Star(n=5, outer_radius=0.55, inner_radius=0.24), "#F0903A").rotate(PI / 2 - PI / 5 * 0))
    for k in range(5):
        a = PI / 2 + k * TAU / 5
        g.add(Dot([0.33 * np.cos(a), 0.33 * np.sin(a), 0], radius=0.04, color="#FFD9A8"))
    g.add(Dot([0, 0, 0], radius=0.05, color="#FFD9A8"))
    return g


def worm():
    g = VGroup()
    for k in range(10):
        x = -0.6 + 0.13 * k
        y = 0.12 * np.sin(1.3 * k)
        g.add(_o(Circle(radius=0.115), "#E89AA5" if k % 2 == 0 else "#D9808E", 1.5).move_to([x, y, 0]))
    g.add(Dot([-0.64, 0.14, 0], radius=0.03, color="#111"))
    return g


def sponge():
    g = VGroup()
    g.add(_o(Ellipse(width=1.1, height=0.3), "#7a7f89").move_to([0, -0.4, 0]))
    g.add(_o(RoundedRectangle(corner_radius=0.2, width=0.6, height=0.72), "#E8CF4C").move_to([0, -0.02, 0]))
    g.add(_o(Ellipse(width=0.4, height=0.14), "#8a6d12", 1.5).move_to([0, 0.34, 0]))
    for p in [(-0.12, 0.1), (0.1, 0.05), (-0.05, -0.12), (0.14, -0.15), (-0.17, -0.02)]:
        g.add(Dot([p[0], p[1], 0], radius=0.045, color="#8a6d12"))
    return g


def nettle():
    g = VGroup()
    for x0 in (-0.3, -0.15, 0.0, 0.15, 0.3):
        g.add(ParametricFunction(lambda t, x0=x0: np.array([x0 + 0.06 * np.sin(9 * t + x0 * 5), -0.05 - 0.7 * t, 0]),
                                 t_range=[0, 1], stroke_color="#F2C6DA", stroke_width=3))
    bell = Arc(radius=0.5, start_angle=0, angle=PI).set_fill("#E6D5F2", 0.95).set_stroke("#C9B3E0", 2)
    g.add(bell)
    return g


ICON = dict(trout=trout, crab=crab, oyster=oyster, star=star, worm=worm, sponge=sponge, nettle=nettle)


def icon(name, w=1.25, maxh=None):
    g = ICON[name]()
    g.set_width(w)
    lim = maxh if maxh else 0.66 * w
    if g.height > lim:
        g.set_height(lim)
    return g


def add_bob(body, ph, amp=0.05):
    body._off = 0.0
    st = {"t": 0.0}

    def u(m, dt):
        st["t"] += dt
        o = amp * np.sin(1.7 * st["t"] + ph)
        m.shift(UP * (o - m._off))
        m._off = o
    body.add_updater(u)


def Pulse(m, f=1.12):
    return m.animate(rate_func=there_and_back).scale(f)


def make_card(name, x, ph=0.0):
    rect = RoundedRectangle(corner_radius=0.15, width=1.6, height=1.9, stroke_color=SLATE, stroke_width=3,
                            fill_color="#252a3a", fill_opacity=1).move_to([x, -1.7, 0])
    body = icon(name, 1.25 if name not in ("nettle", "sponge") else 1.0, maxh=1.0).move_to([x, -1.27, 0])
    lab = T(LABEL[name], 22, TEXT, line_spacing=0.8).move_to([x, -2.25, 0])
    g = VGroup(rect, body, lab)
    g.body = body
    g.rect = rect
    add_bob(body, ph)
    return g


def make_post(i, trait):
    x = XS[i]
    ln = Line([x, TY, 0], [x, TY + 0.45, 0], color=TEXT, stroke_width=6)
    dot = Dot([x, TY, 0], radius=0.11, color=TEXT)
    lab = T(trait, 24, TEXT, weight=BOLD, line_spacing=0.8).next_to(ln, UP, buff=0.08)
    return VGroup(ln, dot, lab)


def trail_parts():
    main = Line([-6.4, TY, 0], [XS[6], TY, 0]).set_stroke(SLATE, 7)
    spurs = VGroup(*[Line([XS[i], TY, 0], [XS[i], -0.75, 0]).set_stroke(SLATE, 7) for i in range(7)])
    return main, spurs


def flow(x0, x1, y, n=4, speed=1.2):
    dots = VGroup(*[Dot([x0 + (x1 - x0) * i / n, y, 0], radius=0.07, color=TEXT).set_opacity(0.8) for i in range(n)])
    dots.set_z_index(3)

    def u(m, dt):
        for d in m:
            d.shift(RIGHT * speed * dt)
            if d.get_x() > x1:
                d.shift(LEFT * (x1 - x0))
    dots.add_updater(u)
    return dots


def name_tag(x, text=None, y=-3.0):
    rect = RoundedRectangle(corner_radius=0.12, width=3.9, height=0.55, stroke_color=COL[5], stroke_width=3,
                            fill_color=BG, fill_opacity=1)
    t = T(text, 26, TEXT, slant=ITALIC, weight=BOLD) if text else T("?", 30, COL[5], weight=BOLD)
    g = VGroup(rect, t).move_to([x, y, 0])
    g.txt = t
    return g


def pill(text, color=TEXT, size=22):
    t = T(text, size, color, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=0.38, stroke_color=color, stroke_width=2.5,
                         fill_color=BG, fill_opacity=1)
    g = VGroup(r, t)
    g.set_z_index(6)
    return g


# ------------------------------------------------------------------ nested boxes (film 1's world)
PX = [-4.5, -1.5, 1.5, 4.5]
PHY = ["crab", "star", "oyster", "trout"]
PHY_NAME = ["Arthropoda", "echinoderms", "mollusks", "Chordata"]


def rect_box(k, l, r, b, t, fill=0.14):
    return RoundedRectangle(corner_radius=0.18, width=r - l, height=t - b, stroke_color=COL[k], stroke_width=4,
                            fill_color=COL[k], fill_opacity=fill).move_to([(l + r) / 2, (t + b) / 2, 0])


def nest(with_texts=True):
    N = {}
    N["navy"] = rect_box(0, -6.5, 6.5, -3.45, 3.1)
    N["indigo"] = rect_box(1, -6.2, 6.2, -3.0, 2.45)
    N["phy"] = [rect_box(2, px - 1.35, px + 1.35, -2.5, 1.15) for px in PX]
    N["ico"] = {n: icon(n, 1.9).move_to([px, -0.45, 0]) for n, px in zip(PHY, PX)}
    if with_texts:
        def tab(k, text, top):
            p = pill(text, COL[k], 22)
            return p.move_to([(6.5 if k == 0 else 6.2) - 0.3 - p.width / 2, top, 0])
        N["tabs"] = [tab(0, "DOMAIN: Eukarya", 3.1), tab(1, "KINGDOM: Animalia", 2.45)]
        N["plab"] = []
        for px, nm in zip(PX, PHY_NAME):
            N["plab"].append(VGroup(T("phylum", 22, TEXT), T(nm, 26, COL[2], weight=BOLD)).arrange(DOWN, buff=0.05).move_to([px, 0.62, 0]))
        N["strip"] = []
        N["stxt"] = []
        for px in PX:
            s = VGroup(*[Square(0.26, fill_color=COL[i], fill_opacity=0.15, stroke_color=COL[i], stroke_width=2) for i in range(8)]).arrange(RIGHT, buff=0.04)
            s.move_to([px, -1.45, 0])
            N["strip"].append(s)
            N["stxt"].append(T("2 of 8 boxes\nshared with crab", 22, TEXT, line_spacing=0.8).move_to([px, -2.0, 0]))
    return N


def light2(s):
    return [s[0].animate.set_fill(COL[0], 1), s[1].animate.set_fill(COL[1], 1)]


def mini_key(order, cx, y=2.0):
    w = 0.62
    ic = VGroup(*[icon(n, w).move_to([cx - 2.4 + 0.8 * i, y, 0]) for i, n in enumerate(order)])
    line = Line([cx - 2.8, y - 0.45, 0], [cx + 2.8, y - 0.45, 0]).set_stroke(SLATE, 5)
    ring = Circle(radius=0.36, stroke_color=COL[5], stroke_width=4).move_to(ic[order.index("crab")])
    return VGroup(line, ic, ring)


class Base(SpokenScene):
    def until(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)

    def key_world(self, order, traits, n_posts=6, crab_gold=False, run_flow=True):
        P = {}
        main, spurs = trail_parts()
        P["main"], P["spurs"] = main, spurs
        P["posts"] = [make_post(i, traits[i]) for i in range(n_posts)]
        P["cards"] = {n: make_card(n, XS[i], 0.9 * i) for i, n in enumerate(order)}
        if crab_gold:
            P["cards"]["crab"].rect.set_stroke(COL[5], 6)
        self.add(main, spurs, *P["posts"], *P["cards"].values())
        if run_flow:
            P["flow"] = flow(-6.4, XS[6], TY)
            self.add(P["flow"])
        return P

    def counter(self, n):
        return T(f"steps: {n}", 30, TEXT, weight=BOLD).move_to([-6.55, 3.45, 0], aligned_edge=LEFT)

    def token(self, x):
        return icon("crab", 0.8).move_to([x, TY + 0.32, 0]).set_z_index(12)


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Sorting Living Things"
    TITLE = "A Key Finds a Name, Not Relatives"


# -------------------------------------------------------------------------------------------------
class S01Question(Base):
    def construct(self):
        water = Rectangle(width=14.3, height=2.6, fill_color="#1b4668", fill_opacity=1, stroke_width=0).move_to([0, 2.5, 0])
        wet = Rectangle(width=14.3, height=1.2, fill_color="#5b4a33", fill_opacity=1, stroke_width=0).move_to([0, 0.6, 0])
        sand = Rectangle(width=14.3, height=3.8, fill_color="#7d6643", fill_opacity=1, stroke_width=0).move_to([0, -1.9, 0])
        waves = VGroup(*[Line([-1.0, 0, 0], [1.0, 0, 0], color=TEXT, stroke_width=3).set_opacity(0.5).move_to([-4.5 + 4.4 * i, 1.55 + 0.55 * (i % 3), 0]) for i in range(5)])
        st = {"t": 0.0}

        def wav(m, dt):
            st["t"] += dt
            for i, w in enumerate(m):
                w.move_to([-4.5 + 4.4 * i + 0.5 * np.sin(0.9 * st["t"] + i), 1.55 + 0.55 * (i % 3) + 0.08 * np.sin(1.7 * st["t"] + i), 0])
        waves.add_updater(wav)
        self.add(water, wet, sand, waves)
        cr = icon("crab", 3.4).move_to([0, -0.4, 0])
        cs = {"t": 0.0}

        def side(m, dt):
            cs["t"] += dt
            m.move_to([0.45 * np.sin(0.8 * cs["t"]), -0.4 + 0.04 * np.sin(2.4 * cs["t"]), 0])
        cr.add_updater(side)
        self.play(FadeIn(cr, shift=UP * 0.3), run_time=1.2)
        lab = T("Chesapeake Bay", 30, TEXT, weight=BOLD).move_to([-4.6, 3.35, 0])
        tag = VGroup(RoundedRectangle(corner_radius=0.18, width=2.6, height=1.5, stroke_color=COL[5], stroke_width=4, fill_color=BG, fill_opacity=1),
                     T("?", 80, COL[5], weight=BOLD)).move_to([0, 2.15, 0])
        tag.add_updater(lambda m, dt: None)
        q = T("What is its name?", 44, TEXT, weight=BOLD).move_to([0, -3.05, 0])
        self.at("name of a crab")
        self.play(FadeIn(tag, shift=DOWN * 0.3), FadeIn(q), run_time=0.8)
        self.at("on the shore")
        self.play(FadeIn(lab), run_time=0.6)
        hand = VGroup(RoundedRectangle(corner_radius=0.2, width=0.9, height=0.7, fill_color=SKIN, fill_opacity=1, stroke_color=OUTLINE, stroke_width=2),
                      Line([-0.4, 0.1, 0], [-1.6, 0.45, 0], color=SKIN, stroke_width=18)).move_to([4.8, -0.9, 0])
        hs = {"t": 0.0}

        def wig(m, dt):
            hs["t"] += dt
            m.shift(LEFT * 0.4 * dt * np.cos(2.0 * hs["t"]))
        hand.add_updater(wig)
        self.at("you do not know")
        self.play(FadeIn(hand, shift=LEFT * 0.4), run_time=0.8)
        self.play(Indicate(tag[1], color=COL[5], scale_factor=1.25), run_time=1.0)
        post = VGroup(Line([-5.2, -2.6, 0], [-5.2, -1.2, 0], color=TEXT, stroke_width=6), Line([-5.2, -1.2, 0], [-5.9, -0.7, 0], color=TEXT, stroke_width=6),
                      Line([-5.2, -1.2, 0], [-4.5, -0.7, 0], color=TEXT, stroke_width=6), Dot([-5.2, -1.2, 0], radius=0.12, color=TEXT))
        self.at("a key can tell you")
        self.play(Create(post), run_time=1.0)
        self.play(Indicate(post, color=COL[5], scale_factor=1.15), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
def thumb():
    g = VGroup()
    for k in range(8):
        g.add(rect_box(k, -3 + 0.25 * k, 3 - 0.25 * k, -1.8 + 0.2 * k, 1.8 - 0.2 * k, 0.07))
    return g


def fork_sign(h=1.8, color=TEXT):
    g = VGroup(Line([0, -h / 2, 0], [0, 0, 0], color=color, stroke_width=7),
               Line([0, 0, 0], [-0.7 * h / 1.8, h / 2, 0], color=color, stroke_width=7),
               Line([0, 0, 0], [0.7 * h / 1.8, h / 2, 0], color=color, stroke_width=7),
               Dot([0, 0, 0], radius=0.14, color=color))
    return g


class S02Link(Base):
    def construct(self):
        th = thumb().move_to([0, 0, 0])
        self.play(LaggedStart(*[Create(r) for r in th], lag_ratio=0.2, run_time=2.4))
        self.play(Pulse(th, 1.04), run_time=1.0)
        self.at("this film uses a different tool")
        self.play(th.animate.scale(0.33).move_to([-5.5, 3.0, 0]), run_time=1.4)
        word = T("dichotomous key", 60, TEXT, weight=BOLD).move_to([0.8, 1.2, 0])
        sub = T("two choices at every step", 32, TEXT).move_to([0.8, 0.25, 0])
        self.at("dichotomous key")
        self.play(Write(word), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        fk = fork_sign(2.0).move_to([0.8, -2.0, 0])
        add_bob(fk, 0.0, 0.05)
        self.at("both tools matter")
        self.play(Create(fk), Pulse(th, 1.2), run_time=1.2)
        self.at("different jobs")
        self.play(Indicate(fk, color=COL[5], scale_factor=1.12), run_time=0.9)
        self.play(Pulse(th, 1.25), run_time=0.9)
        self.finish()


# -------------------------------------------------------------------------------------------------
def walker():
    g = VGroup(Circle(radius=0.2, fill_color=SKIN, fill_opacity=1, stroke_color=OUTLINE, stroke_width=2).move_to([0, 0.78, 0]),
               Line([0, 0.58, 0], [0, 0.2, 0], color=TEXT, stroke_width=6),
               Line([0, 0.5, 0], [-0.22, 0.28, 0], color=TEXT, stroke_width=5),
               Line([0, 0.5, 0], [0.22, 0.28, 0], color=TEXT, stroke_width=5),
               Line([0, 0.2, 0], [-0.17, -0.1, 0], color=TEXT, stroke_width=6),
               Line([0, 0.2, 0], [0.17, -0.1, 0], color=TEXT, stroke_width=6))
    return g


class S03Define(Base):
    def construct(self):
        main = Line([-6.2, 0, 0], [-1.5, 0, 0]).set_stroke(SLATE, 8)
        up = VGroup(Line([-1.5, 0, 0], [1.5, 1.5, 0]), Line([1.5, 1.5, 0], [4.2, 1.5, 0])).set_stroke(SLATE, 8)
        dn = VGroup(Line([-1.5, 0, 0], [1.5, -1.5, 0]), Line([1.5, -1.5, 0], [4.2, -1.5, 0])).set_stroke(SLATE, 8)
        post = VGroup(Line([-1.5, 0, 0], [-1.5, 0.55, 0], color=TEXT, stroke_width=7), Dot([-1.5, 0, 0], radius=0.14, color=TEXT)).set_z_index(5)
        fl = flow(-6.2, -1.5, 0.0, 3, 1.3)
        self.play(Create(main), run_time=1.8)
        self.add(fl)
        l1 = T("step = two choices", 30, COL[5], weight=BOLD).move_to([-3.9, 1.2, 0])
        self.at("two choice steps")
        self.play(FadeIn(post), Create(up), Create(dn), FadeIn(l1), run_time=1.3)
        l2 = T("traits you can see", 30, COL[3], weight=BOLD).move_to([-3.9, -1.2, 0])
        a = T("fins", 30, TEXT, weight=BOLD).move_to([2.9, 2.05, 0])
        b = T("no fins", 30, TEXT, weight=BOLD).move_to([2.9, -2.05, 0])
        self.at("traits you can see")
        self.play(FadeIn(l2), FadeIn(a), FadeIn(b), run_time=0.8)
        w = walker().move_to([-6.0, 0.5, 0])
        w.set_z_index(8)
        add_bob(w, 0.0, 0.04)
        self.at("each step splits")
        self.play(FadeIn(w), run_time=0.5)
        self.play(w.animate.move_to([-1.9, 0.5, 0]), run_time=2.0)
        self.play(Indicate(post, color=COL[5], scale_factor=1.3), run_time=0.8)
        tag = VGroup(RoundedRectangle(corner_radius=0.14, width=1.9, height=0.7, stroke_color=COL[5], stroke_width=3, fill_color=BG, fill_opacity=1),
                     T("a name", 30, TEXT, weight=BOLD)).move_to([5.5, 1.5, 0])
        self.at("you follow the choice")
        self.play(w.animate.move_to([1.5, 2.0, 0]), run_time=1.6)
        self.at("you reach a name")
        self.play(w.animate.move_to([4.2, 2.0, 0]), FadeIn(tag, shift=LEFT * 0.3), run_time=1.5)
        self.play(Indicate(tag, color=COL[5], scale_factor=1.15), run_time=0.9)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S04Walk(Base):
    def construct(self):
        main, spurs = trail_parts()
        cards = {n: make_card(n, XS[i], 0.9 * i) for i, n in enumerate(OLD)}
        self.play(LaggedStart(*[FadeIn(cards[n], shift=UP * 0.5) for n in OLD], lag_ratio=0.25, run_time=2.4))
        self.at("each from a different phylum")
        self.play(LaggedStart(*[Pulse(cards[n], 1.1) for n in OLD], lag_ratio=0.2, run_time=2.0))
        posts = [make_post(i, OLD_T[i]) for i in range(6)]
        self.at("step 1 asks")
        self.play(Create(main), Create(spurs), run_time=1.2)
        fl = flow(-6.4, XS[6], TY)
        self.add(fl)
        self.at("fins or no fins")
        self.play(FadeIn(posts[0]), run_time=0.6)
        self.play(Indicate(posts[0][2], color=COL[5], scale_factor=1.2), run_time=0.8)
        tk = self.token(-6.3)
        cn = self.counter(1)
        nof = T("no fins:\ngo to 2", 24, TEXT, line_spacing=0.8).move_to([XS[0] + 0.9, TY - 0.55, 0])
        self.at("the crab has no fins")
        self.play(FadeIn(tk, shift=DOWN * 0.2), run_time=0.5)
        self.play(tk.animate.move_to([XS[0], TY + 0.32, 0]), FadeIn(cn), run_time=1.0)
        self.play(FadeIn(nof), run_time=0.5)
        self.at("so we go on")
        self.play(tk.animate.move_to([XS[1], TY + 0.32, 0]), run_time=1.4)
        self.at("step 2 asks")
        self.play(FadeIn(posts[1]), Transform(cn, self.counter(2)), FadeOut(nof), run_time=0.8)
        self.at("jointed legs or no jointed legs")
        self.play(Indicate(posts[1][2], color=COL[5], scale_factor=1.2), run_time=0.9)
        self.at("the crab has jointed legs")
        self.play(Indicate(tk, color=COL[5], scale_factor=1.5), run_time=1.0)
        self.play(tk.animate.move_to([XS[1], -1.2, 0]), run_time=1.3)
        cards["crab"].rect.set_stroke(COL[5], 6)
        self.play(FadeOut(tk), Pulse(cards["crab"], 1.1), run_time=0.8)
        self.finish()


# -------------------------------------------------------------------------------------------------
def badge(n, x):
    return VGroup(Circle(radius=0.27, fill_color=BG, fill_opacity=1, stroke_color=COL[5], stroke_width=3),
                  T(str(n), 28, TEXT, weight=BOLD)).move_to([x, 0.15, 0]).set_z_index(9)


class S05Name(Base):
    def construct(self):
        P = self.key_world(OLD, OLD_T, crab_gold=True)
        cards = P["cards"]
        tag = name_tag(XS[1], None)
        self.at("the path ends at a name")
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.6)
        self.until(1.8)
        self.play(Transform(tag.txt, T("Callinectes sapidus", 26, TEXT, slant=ITALIC, weight=BOLD).move_to(tag.txt)), run_time=1.3)
        self.at("the blue crab")
        self.play(Pulse(cards["crab"], 1.12), run_time=0.9)
        self.at("look at the whole key")
        self.play(LaggedStart(*[Pulse(cards[n], 1.06) for n in OLD], lag_ratio=0.15, run_time=1.6))
        b1, b2, b3 = badge(1, XS[0]), badge(2, XS[1]), badge(3, XS[2])
        self.at("the trout comes off")
        self.play(FadeIn(b1, scale=1.3), run_time=0.6)
        self.at("the crab second")
        self.play(FadeIn(b2, scale=1.3), run_time=0.6)
        self.at("the oyster third")
        self.play(FadeIn(b3, scale=1.3), run_time=0.6)
        r1 = SurroundingRectangle(cards["trout"], buff=0.08, color=TEXT, stroke_width=2.5, corner_radius=0.15)
        r2 = SurroundingRectangle(cards["oyster"], buff=0.08, color=TEXT, stroke_width=2.5, corner_radius=0.15)
        n1 = T("neighbors", 22, TEXT, weight=BOLD).move_to([XS[0], -3.55, 0])
        n2 = T("neighbors", 22, TEXT, weight=BOLD).move_to([XS[2], -3.55, 0])
        self.play(Create(r1), Create(r2), FadeIn(n1), FadeIn(n2), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S06Shuffle(Base):
    def construct(self):
        P = self.key_world(OLD, OLD_T)
        posts, cards, spurs = P["posts"], P["cards"], P["spurs"]
        self.at("keep every question")
        self.play(LaggedStart(*[Indicate(p[2], color=COL[5], scale_factor=1.2) for p in posts], lag_ratio=0.12, run_time=1.0))
        self.at("change their order")
        self.play(*[p.animate.shift(UP * 0.7) for i, p in enumerate(posts)], run_time=0.6)
        perm = [3, 0, 5, 2, 1, 4]
        self.play(*[p[2].animate.set_opacity(0) for p in posts], run_time=0.2)
        self.play(*[p.animate.shift(RIGHT * (XS[perm[i]] - XS[i])) for i, p in enumerate(posts)], run_time=0.5)
        self.play(*[p[2].animate.set_opacity(1) for p in posts], run_time=0.2)
        perm2 = [4, 2, 0, 5, 3, 1]
        self.play(*[p[2].animate.set_opacity(0) for p in posts], run_time=0.2)
        self.play(*[p.animate.shift(RIGHT * (XS[perm2[i]] - XS[perm[i]])) for i, p in enumerate(posts)], run_time=0.6)
        note = T("same questions, new order", 32, COL[5], weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(note), run_time=0.3)
        newslot = [0, 3, 1, 2, 4, 5]
        self.at("ask about the two part shell")
        lands = [p.animate.shift(RIGHT * (XS[newslot[i]] - XS[perm2[i]]) + DOWN * 0.7) for i, p in enumerate(posts)]
        old_slot = {n: i for i, n in enumerate(OLD)}
        moves = [cards[n].animate.shift(RIGHT * (XS[NEW.index(n)] - XS[old_slot[n]])) for n in OLD if NEW.index(n) != old_slot[n]]
        self.play(*lands, *moves, run_time=1.6)
        self.play(*[p[2].animate.set_opacity(1) for p in posts], run_time=0.2)
        self.at("the five arms")
        self.play(Indicate(posts[3][2], color=COL[5], scale_factor=1.25), Indicate(posts[2][2], color=COL[5], scale_factor=1.25), run_time=1.0)
        self.at("before the jointed legs")
        self.play(Indicate(posts[1][2], color=COL[5], scale_factor=1.25), run_time=0.9)
        self.at("watch the branches redraw")
        self.play(LaggedStart(*[Indicate(s, color=COL[5], scale_factor=1.12) for s in spurs], lag_ratio=0.15, run_time=1.6))
        self.finish()


# -------------------------------------------------------------------------------------------------
class S07SameName(Base):
    def construct(self):
        P = self.key_world(NEW, NEW_T)
        cards = P["cards"]
        tk = self.token(-6.3)
        cn = self.counter(0)
        self.at("run the crab again")
        self.play(FadeIn(tk, shift=DOWN * 0.2), FadeIn(cn), run_time=0.6)
        before = T("before: 2", 26, TEXT).move_to([-3.4, 3.45, 0])
        for k in range(4):
            self.play(tk.animate.move_to([XS[k], TY + 0.32, 0]), run_time=0.7)
            self.play(Transform(cn, self.counter(k + 1)), run_time=0.2)
            if k == 1:
                self.play(FadeIn(before), run_time=0.4)
        self.play(tk.animate.move_to([XS[3], -1.2, 0]), run_time=1.0)
        cards["crab"].rect.set_stroke(COL[5], 6)
        self.play(FadeOut(tk), run_time=0.4)
        tag = name_tag(XS[3], None)
        self.at("the same name")
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.6)
        self.until(7.0)
        self.play(Transform(tag.txt, T("Callinectes sapidus", 26, TEXT, slant=ITALIC, weight=BOLD).move_to(tag.txt)), run_time=1.2)
        self.at("every animal keeps its name")
        self.play(LaggedStart(*[Pulse(cards[n], 1.08) for n in NEW], lag_ratio=0.2, run_time=2.0))
        r1 = SurroundingRectangle(cards["star"], buff=0.08, color=TEXT, stroke_width=2.5, corner_radius=0.15)
        r2 = SurroundingRectangle(cards["worm"], buff=0.08, color=TEXT, stroke_width=2.5, corner_radius=0.15)
        n1 = T("new neighbors", 22, TEXT, weight=BOLD).move_to([XS[2], -3.55, 0])
        n2 = T("new neighbors", 22, TEXT, weight=BOLD).move_to([XS[4], -3.55, 0])
        self.at("only its neighbors change")
        self.play(Create(r1), Create(r2), FadeIn(n1), FadeIn(n2), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
def duo():
    cs = make_card("star", -2.2).scale(1.6).move_to([-2.2, -0.3, 0])
    cc = make_card("crab", 2.2).scale(1.6).move_to([2.2, -0.3, 0])
    return cs, cc


class S08Predict(Base):
    def construct(self):
        P = self.key_world(NEW, NEW_T)
        cards = P["cards"]
        rest = VGroup(P["main"], P["spurs"], *P["posts"], P["flow"], *[c for n, c in cards.items() if n not in ("star", "crab")])
        self.at("the crab now sits right next to the sea star")
        self.play(FadeOut(rest), cards["star"].animate.scale(1.6).move_to([-2.2, -0.3, 0]),
                  cards["crab"].animate.scale(1.6).move_to([2.2, -0.3, 0]), run_time=2.2)
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([0, -0.3, 0])
        self.play(FadeIn(qm, scale=0.6), run_time=0.7)
        q = T("Closer relatives now?", 44, YELLOW, weight=BOLD).move_to([0, 2.85, 0])
        self.at("has the crab become more closely related")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.play(Indicate(qm, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.finish()


class S09Pause(Base):
    def construct(self):
        cs, cc = duo()
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([0, -0.3, 0])
        q = T("Closer relatives now?", 44, YELLOW, weight=BOLD).move_to([0, 2.85, 0])
        panel = RoundedRectangle(corner_radius=0.2, width=8.0, height=1.3, stroke_color=COL[6], stroke_width=3, fill_color=BG, fill_opacity=0.97).move_to([0, -2.75, 0])
        t = T("Pause and predict: yes or no?", 34, COL[6], weight=BOLD).move_to([0, -2.5, 0])
        bar = Rectangle(width=7.0, height=0.14, fill_color=COL[6], fill_opacity=1, stroke_width=0).move_to([0, -3.2, 0])
        self.add(cs, cc, qm, q, panel, t, bar)
        L0 = bar.get_left()
        st = {"t": 0.0}

        def shrink(m, dt):
            st["t"] += dt
            f = max(0.02, 1 - st["t"] / 5.0)
            m.stretch_to_fit_width(7.0 * f)
            m.move_to(L0 + RIGHT * 7.0 * f / 2)
        bar.add_updater(shrink)
        self.play(Indicate(qm, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S10Reveal(Base):
    def construct(self):
        N = nest()
        self.play(Create(N["navy"]), run_time=1.0)
        self.play(Create(N["indigo"]), FadeIn(N["tabs"][0]), FadeIn(N["tabs"][1]), run_time=1.2)
        hov = {n: icon(n, 1.1).move_to([px, 1.8, 0]) for n, px in zip(PHY[:3], PX[:3])}
        self.at("drop the animals into the boxes from the first film")
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.3) for h in hov.values()], lag_ratio=0.3, run_time=1.6))
        for h in hov.values():
            add_bob(h, 0.5)

        def drop(i, name):
            self.play(Create(N["phy"][i]), run_time=0.8)
            h = hov[name]
            h.clear_updaters()
            self.play(h.animate.become(icon(name, 1.9).move_to([PX[i], -0.45, 0])), run_time=0.9)
            add_bob(h, 0.9 * i)

        self.at("the crab is in phylum")
        drop(0, "crab")
        self.at("arthropoda")
        self.play(FadeIn(N["plab"][0]), run_time=0.7)
        self.at("the sea star and the oyster")
        drop(1, "star")
        self.play(FadeIn(N["plab"][1]), run_time=0.6)
        self.at("are each in a different phylum")
        drop(2, "oyster")
        self.play(FadeIn(N["plab"][2]), run_time=0.6)
        self.at("the crab shares only two boxes with each of them")
        self.play(FadeIn(N["strip"][1]), FadeIn(N["strip"][2]), FadeIn(N["stxt"][1]), FadeIn(N["stxt"][2]), run_time=0.8)
        self.play(*light2(N["strip"][1]), *light2(N["strip"][2]), run_time=1.2)
        self.at("the domain and the kingdom")
        self.play(Indicate(N["tabs"][0], color=COL[0], scale_factor=1.15), Indicate(N["tabs"][1], color=COL[1], scale_factor=1.15), run_time=1.4)
        self.play(Pulse(N["strip"][1], 1.1), Pulse(N["strip"][2], 1.1), run_time=0.9)
        self.finish()


def nest_full(scene, upto_trout=True):
    """Everything on screen at the end of film scene 10 (+ trout when asked)."""
    N = nest()
    parts = [N["navy"], N["indigo"], *N["tabs"]]
    names = PHY if upto_trout else PHY[:3]
    for i, n in enumerate(names):
        parts += [N["phy"][i], N["ico"][n], N["plab"][i]]
        add_bob(N["ico"][n], 0.9 * i)
    for i in ([1, 2, 3] if upto_trout else [1, 2]):
        parts += [N["strip"][i], N["stxt"][i]]
        s = N["strip"][i]
        s[0].set_fill(COL[0], 1)
        s[1].set_fill(COL[1], 1)
    scene.add(*parts)
    return N


class S11Trout(Base):
    def construct(self):
        N = nest()
        parts = [N["navy"], N["indigo"], *N["tabs"]]
        for i, n in enumerate(PHY[:3]):
            parts += [N["phy"][i], N["ico"][n], N["plab"][i]]
            add_bob(N["ico"][n], 0.9 * i)
        for i in (1, 2):
            parts += [N["strip"][i], N["stxt"][i]]
            N["strip"][i][0].set_fill(COL[0], 1)
            N["strip"][i][1].set_fill(COL[1], 1)
        self.add(*parts)
        tro = icon("trout", 1.1).move_to([PX[3], 1.8, 0])
        self.at("the crab shares just two boxes with the trout")
        self.play(FadeIn(tro, shift=DOWN * 0.3), run_time=0.7)
        self.play(Create(N["phy"][3]), run_time=0.7)
        self.play(tro.animate.become(icon("trout", 1.9).move_to([PX[3], -0.45, 0])), FadeIn(N["plab"][3]), run_time=0.8)
        add_bob(tro, 2.7)
        self.play(FadeIn(N["strip"][3]), FadeIn(N["stxt"][3]), run_time=0.5)
        self.play(*light2(N["strip"][3]), run_time=0.8)
        B = VGroup(N["navy"], N["indigo"], *N["phy"], N["ico"]["crab"], N["ico"]["star"], N["ico"]["oyster"], tro)
        Tx = VGroup(*N["tabs"], *N["plab"], *N["strip"][1:], *N["stxt"][1:])
        self.at("in either order")
        self.play(FadeOut(Tx), run_time=0.5)
        self.play(B.animate.scale(0.5).move_to([0, -1.6, 0]), run_time=1.2)
        k1, k2 = mini_key(OLD, -3.4), mini_key(NEW, 3.4)
        l1 = T("old order", 28, TEXT, weight=BOLD).move_to([-3.4, 3.2, 0])
        l2 = T("new order", 28, TEXT, weight=BOLD).move_to([3.4, 3.2, 0])
        a1 = Arrow([-3.4, 1.35, 0], [-0.7, 0.2, 0], buff=0.05, color=COL[5], stroke_width=5)
        a2 = Arrow([3.4, 1.35, 0], [0.7, 0.2, 0], buff=0.05, color=COL[5], stroke_width=5)
        self.at("the boxes stay the same")
        self.play(FadeIn(k1), FadeIn(k2), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.at("moving a question cannot make two animals closer relatives")
        self.play(Pulse(B, 1.06), run_time=1.0)
        self.play(Indicate(a1, color=COL[5]), Indicate(a2, color=COL[5]), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S12Why(Base):
    def construct(self):
        N = nest()
        tro = icon("trout", 1.9).move_to([PX[3], -0.45, 0])
        add_bob(tro, 2.7)
        ico = dict(N["ico"])
        ico["trout"] = tro
        for i, n in enumerate(PHY[:3]):
            add_bob(ico[n], 0.9 * i)
        B = VGroup(N["navy"], N["indigo"], *N["phy"], ico["crab"], ico["star"], ico["oyster"], tro)
        B.scale(0.5).move_to([0, -1.6, 0])
        k1, k2 = mini_key(OLD, -3.4), mini_key(NEW, 3.4)
        l1 = T("old order", 28, TEXT, weight=BOLD).move_to([-3.4, 3.2, 0])
        l2 = T("new order", 28, TEXT, weight=BOLD).move_to([3.4, 3.2, 0])
        a1 = Arrow([-3.4, 1.35, 0], [-0.7, 0.2, 0], buff=0.05, color=COL[5], stroke_width=5)
        a2 = Arrow([3.4, 1.35, 0], [0.7, 0.2, 0], buff=0.05, color=COL[5], stroke_width=5)
        self.add(B, k1, k2, l1, l2, a1, a2)
        self.play(FadeOut(VGroup(k1, k2, l1, l2, a1, a2)), B.animate.move_to([3.4, 0.95, 0]), run_time=1.5)
        trail = Line([-5.9, 2.9, 0], [-5.9, -0.7, 0]).set_stroke(SLATE, 7)
        ys = [2.5, 1.6, 0.7, -0.2]
        words = ["fins", "shell", "five arms", "jointed legs"]
        ws = [T(w, 34, COL[5], weight=BOLD).move_to([-5.45, y, 0], aligned_edge=LEFT) for w, y in zip(words, ys)]
        dots = VGroup(*[Dot([-5.9, y, 0], radius=0.13, color=TEXT) for y in ys])
        self.at("this key asks about traits")
        self.play(Create(trail), FadeIn(dots), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.2) for w in ws], lag_ratio=0.4, run_time=1.6))
        easy = T("chosen because\neasy to see", 28, TEXT, weight=BOLD, line_spacing=0.85).move_to([-3.4, -1.1, 0])
        self.at("easy to see")
        self.play(FadeIn(easy), run_time=0.7)
        self.at("not who is related")
        self.play(LaggedStart(*[Indicate(w, color=TEXT, scale_factor=1.15) for w in ws], lag_ratio=0.3, run_time=1.6))
        self.at("so its order alone")
        for perm in ([2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2], [0, 1, 2, 3]):
            self.play(*[w.animate.set_opacity(0) for w in ws], run_time=0.2)
            self.play(*[w.animate.move_to([-5.45 + w.width / 2, ys[perm[i]], 0]) for i, w in enumerate(ws)], run_time=0.5)
            self.play(*[w.animate.set_opacity(1) for w in ws], run_time=0.2)
        lab = T("shows how one\nclassification groups them", 26, TEXT, weight=BOLD, line_spacing=0.85).move_to([3.4, -1.3, 0])
        self.at("the boxes show how one classification groups them")
        self.play(FadeIn(lab), Pulse(B, 1.05), run_time=1.2)
        self.play(LaggedStart(*[Indicate(w, color=TEXT, scale_factor=1.12) for w in ws], lag_ratio=0.2, run_time=1.4))
        rule_t = T("Key: finds the name. Boxes: show the grouping.", 32, COL[5], weight=BOLD)
        fit(rule_t, max_w=11.0)
        rule = VGroup(RoundedRectangle(corner_radius=0.2, width=rule_t.width + 0.6, height=0.85, stroke_color=COL[5], stroke_width=3, fill_color=BG, fill_opacity=0.97),
                      rule_t)
        rule_t.move_to(rule[0])
        rule.move_to([0, -4.3, 0])
        self.at("to draw the boxes")
        self.play(rule.animate.move_to([0, -3.3, 0]), run_time=0.9)
        c1 = chip("body parts", COL[3], 24).move_to([0, -2.4, 0])
        c2 = chip("what living things do", COL[3], 24)
        c3 = chip("DNA", COL[3], 24)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3).move_to([0, -2.4, 0])
        self.at("compare body parts")
        self.play(FadeIn(c1), run_time=0.6)
        self.at("what living things do")
        self.play(FadeIn(c2), run_time=0.6)
        self.at("and dna")
        self.play(FadeIn(c3), run_time=0.6)
        self.play(Pulse(B, 1.05), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "A key finds the name; shared boxes show the grouping."
