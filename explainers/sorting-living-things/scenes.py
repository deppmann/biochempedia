"""Eight Boxes and a Name (grade 7 Life Science, film 1).

COLOUR MAP (one colour per box, same in every scene; lifted for the dark ground)
  DOMAIN = navy-blue   KINGDOM = indigo   PHYLUM = purple   CLASS = teal
  ORDER  = green       FAMILY  = gold     GENUS  = orange   SPECIES = coral red
One world: seven cartoon living things in a row, nested boxes closing around them.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

COL = ["#5B8DEF", "#8A7CF5", "#B574E6", "#3FB8C0", "#83C167", "#D4A843", "#F29E4C", "#FF6B5E"]
LEVEL = ["DOMAIN", "KINGDOM", "PHYLUM", "CLASS", "ORDER", "FAMILY", "GENUS", "SPECIES"]
NAMES = ["Eukarya", "Animalia", "Chordata", "Aves", "Accipitriformes", "Cathartidae", "Cathartes", "Cathartes aura"]
OUTLINE = "#1a1a22"

# geometry of the one world
ORDER_L = ["pine", "crab", "trout", "cardinal", "hawk", "black", "turkey"]
X = {n: -4.5 + 1.65 * i for i, n in enumerate(ORDER_L)}
AY = -0.95
FIRST = [0, 1, 2, 3, 4, 5, 6, 6]
TOP = [3.0 - 0.42 * k for k in range(8)]
BOT = [-3.45 + 0.1 * k for k in range(8)]
RGT = [6.6 - 0.03 * k for k in range(8)]
EXCL_AT = {"pine": 2, "crab": 3, "trout": 4, "cardinal": 5, "hawk": 6, "black": 7}  # boxes closed before it is out


def left_of(k):
    return X[ORDER_L[FIRST[k]]] - 0.85 + (0.08 if k == 7 else 0.0)


# ------------------------------------------------------------------ cartoon icons
def _o(m, fill, sw=2.0):
    return m.set_fill(fill, 1).set_stroke(OUTLINE, sw)


def bird(body, head, tail, crest=False, hook=False, mask=False, beak="#E8D9A8"):
    g = VGroup()
    g.add(_o(Polygon([0.4, -0.05, 0], [0.8, 0.02, 0], [0.74, -0.32, 0], [0.38, -0.22, 0]), tail))
    g.add(_o(Ellipse(width=0.95, height=0.5), body).move_to([0.0, -0.1, 0]))
    g.add(_o(Line([-0.3, 0.02, 0], [-0.5, 0.22, 0]), body).set_stroke(body, 9))
    g.add(_o(Circle(radius=0.16), head).move_to([-0.52, 0.27, 0]))
    g.add(_o(Polygon([-0.66, 0.31, 0], [-0.9, 0.2, 0], [-0.66, 0.2, 0]), beak, 1.5))
    if hook:
        g.add(Dot([-0.9, 0.2, 0], radius=0.03, color=OUTLINE))
    if crest:
        g.add(_o(Polygon([-0.5, 0.4, 0], [-0.36, 0.62, 0], [-0.32, 0.36, 0]), body))
    if mask:
        g.add(Circle(radius=0.07, stroke_width=0, fill_color="#222", fill_opacity=1).move_to([-0.62, 0.25, 0]))
    g.add(Dot([-0.5, 0.31, 0], radius=0.03, color="#111"))
    g.add(_o(Ellipse(width=0.55, height=0.26), _shade(body)).move_to([0.05, -0.1, 0]))
    g.add(Line([-0.1, -0.33, 0], [-0.12, -0.5, 0], color="#C9A36B", stroke_width=3))
    g.add(Line([0.1, -0.33, 0], [0.1, -0.5, 0], color="#C9A36B", stroke_width=3))
    return g


def _shade(c):
    col = ManimColor(c).to_rgb() * 0.75
    return ManimColor.from_rgb(col)


def turkey_vulture():
    return bird("#6B4A2F", RED, "#4a3220", hook=True)


def black_vulture():
    return bird("#4a4a52", "#A9ADB5", "#33333a", hook=True)


def hawk():
    return bird("#8B5E3C", "#8B5E3C", "#C2572B", hook=True)


def cardinal():
    return bird("#E23B3B", "#E23B3B", "#B82828", crest=True, mask=True, beak="#F29E4C")


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
            g.add(Line([s * 0.25, -0.1 - 0.0 * j, 0], [s * (0.55 + 0.05 * j), -0.28 - 0.12 * j, 0], color="#3D7BD9", stroke_width=5))
        g.add(Line([s * 0.35, 0.05, 0], [s * 0.55, 0.32, 0], color="#3D7BD9", stroke_width=6))
        g.add(_o(Circle(radius=0.17), "#3D7BD9").move_to([s * 0.6, 0.42, 0]))
        g.add(_o(Polygon([s * 0.52, 0.5, 0], [s * 0.6, 0.66, 0], [s * 0.68, 0.5, 0]), "#3D7BD9", 1.5))
    g.add(_o(Ellipse(width=0.95, height=0.55), "#4A8DEB").move_to([0, -0.05, 0]))
    for s in (-1, 1):
        g.add(Dot([s * 0.12, 0.2, 0], radius=0.04, color="#111"))
    return g


def pine():
    g = VGroup()
    g.add(Line([-0.5, -0.45, 0], [0.5, 0.35, 0], color="#8B5E3C", stroke_width=7))
    for i in range(6):
        x = -0.35 + 0.17 * i
        y = -0.45 + 0.8 * (x + 0.5) / 1.0 * 1.0 - 0.0
        y = -0.45 + (x + 0.5) * 0.8
        for dx, dy in [(-0.12, 0.3), (0.2, -0.22), (0.0, 0.34), (0.22, -0.05)]:
            g.add(Line([x, y, 0], [x + dx, y + dy, 0], color="#4FA85A", stroke_width=3))
    g.add(_o(Ellipse(width=0.32, height=0.42), "#9A6B3C").move_to([0.12, -0.2, 0]).rotate(0.6))
    return g


def bacterium(c="#B7E36B"):
    return RoundedRectangle(corner_radius=0.08, width=0.34, height=0.17, fill_color=c, fill_opacity=1, stroke_color=OUTLINE, stroke_width=1.5)


ICON = dict(pine=pine, crab=crab, trout=trout, cardinal=cardinal, hawk=hawk, black=black_vulture, turkey=turkey_vulture)
LABEL = dict(pine="pine\ntwig", crab="blue\ncrab", trout="brook\ntrout", cardinal="cardinal", hawk="red-tailed\nhawk",
             black="black\nvulture", turkey="turkey\nvulture")


def icon(name, w=1.45):
    g = ICON[name]()
    g.set_width(w)
    if g.height > 0.66 * w:
        g.set_height(0.66 * w)
    return g


def add_bob(body, ph, amp=0.06):
    body._off = 0.0
    st = {"t": 0.0}

    def u(m, dt):
        st["t"] += dt
        o = amp * np.sin(1.7 * st["t"] + ph)
        m.shift(UP * (o - m._off))
        m._off = o
    body.add_updater(u)


def animal(name, w=1.45, ph=None):
    body = icon(name, w).move_to([0, 0, 0])
    lab = T(LABEL[name], 22, TEXT, line_spacing=0.8).move_to([0, -1.0, 0])
    g = VGroup(body, lab)
    g.body = body
    add_bob(body, ph if ph is not None else ORDER_L.index(name) * 0.9)
    g.move_to([X[name], AY - 0.45, 0])  # centre of group so body sits near AY
    g.shift(UP * 0.0)
    return g


def animals(n_closed):
    A = {n: animal(n) for n in ORDER_L}
    for n, k in EXCL_AT.items():
        if n_closed >= k:
            A[n].set_opacity(0.45).shift(DOWN * 0.12)
    return A


def out_anim(a):
    return a.animate.set_opacity(0.45).shift(DOWN * 0.12)


def rect_for(k, left=None, dashed=False):
    L = left_of(k) if left is None else left
    R, t, b = RGT[k], TOP[k], BOT[k]
    r = RoundedRectangle(corner_radius=0.18, width=R - L, height=t - b, stroke_color=COL[k], stroke_width=4,
                         fill_color=COL[k], fill_opacity=0.05).move_to([(L + R) / 2, (t + b) / 2, 0])
    if dashed:
        r = DashedVMobject(r, num_dashes=60, dashed_ratio=0.55)
    return r


def tab_for(k, text=None):
    s = text or f"{k + 1} {LEVEL[k]}: {NAMES[k]}"
    t2s = {}
    if k == 6 and "Cathartes" in s:
        t2s = {"Cathartes": ITALIC}
    if k == 7:
        t2s = {"Cathartes aura": ITALIC}
    txt = Text(s, font=FONT, font_size=22, color=COL[k], weight=BOLD, t2s=t2s)
    pill = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.3, height=0.38, stroke_color=COL[k], stroke_width=2.5,
                            fill_color=BG, fill_opacity=1)
    g = VGroup(pill, txt)
    g.move_to([RGT[k] - 0.3 - g.width / 2, TOP[k], 0])
    g.set_z_index(6)
    return g


def counter(n):
    return T(f"boxes: {n}", 26, TEXT, weight=BOLD).move_to([-6.55, 3.55, 0], aligned_edge=LEFT)


def pill_note(text, color=TEXT, size=22, w=None, **kw):
    t = T(text, size, color, **kw)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.2, stroke_color=color, stroke_width=1.5,
                         fill_color=BG, fill_opacity=0.97)
    g = VGroup(r, t)
    g.set_z_index(8)
    return g


def plantae_tag():
    return T("kingdom\nPlantae", 22, TEXT, line_spacing=0.8).move_to([X["pine"], 0.1, 0])


def coragyps_tag():
    return T("Coragyps", 24, TEXT, slant=ITALIC).move_to([X["black"], -0.4, 0])


def Pulse(m, f=1.12):
    return m.animate(rate_func=there_and_back).scale(f)


class Base(SpokenScene):
    def until(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)

    def world(self, n, tags=True, show_bact=True):
        """Settled state with n boxes closed. Returns dict of parts."""
        P = {"A": animals(n)}
        P["R"] = [rect_for(k) for k in range(n)]
        P["T"] = [tab_for(k) for k in range(n)]
        P["C"] = counter(n) if n else None
        self.add(*P["R"], *P["A"].values(), *P["T"])
        if P["C"]:
            self.add(P["C"])
        P["tags"] = []
        if tags and n >= 3:
            P["tags"].append(plantae_tag())
        if tags and n >= 8:
            pass
        self.add(*P["tags"])
        if show_bact:
            P["bact"] = self.bacteria()
        return P

    def bacteria(self):
        g = VGroup()
        pos = [(-6.2, -0.2), (-5.9, -1.0), (-6.3, -1.7), (-6.0, 0.5)]
        for i, (x, y) in enumerate(pos):
            b = bacterium().move_to([x, y, 0]).rotate(0.5 * i)
            b.base = np.array([x, y, 0.0])
            b.ph = i * 1.3
            st = {"t": 0.0}

            def u(m, dt, st=st):
                st["t"] += dt
                m.move_to(m.base + np.array([0.12 * np.sin(1.1 * st["t"] + m.ph), 0.12 * np.cos(0.9 * st["t"] + m.ph), 0]))
            b.add_updater(u)
            g.add(b)
        lab = T("bacteria", 22, TEXT).move_to([-6.1, -2.3, 0])
        g.add(lab)
        self.add(g)
        return g

    def card(self, lines, center, w, h, size=30):
        r = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=COL[6], stroke_width=3, fill_color=BG, fill_opacity=0.97)
        t = T(lines, size, TEXT, line_spacing=0.9)
        g = VGroup(r, t).move_to(center)
        g.set_z_index(9)
        return g


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Sorting Living Things"
    TITLE = "Eight Boxes and a Name"


# -------------------------------------------------------------------------------------------------
class S01Question(Base):
    def construct(self):
        road = Rectangle(width=14.3, height=1.3, fill_color="#2a2d36", fill_opacity=1, stroke_width=0).move_to([0, -3.3, 0])
        dashes = VGroup(*[Rectangle(width=0.9, height=0.12, fill_color="#F5D547", fill_opacity=0.9, stroke_width=0).move_to([-7.4 + 2.0 * i, -3.3, 0]) for i in range(9)])

        def roll(m, dt):
            m.shift(LEFT * 2.4 * dt)
            if m.get_center()[0] < -8.0:
                m.shift(RIGHT * 18.0)
        for d in dashes:
            d.add_updater(roll)
        self.add(road, dashes)
        # three turkey vultures circling
        vs = VGroup(*[icon("turkey", 1.9) for _ in range(3)])
        st = {"t": 0.0}

        def circ(m, dt):
            st["t"] += dt
            for i, v in enumerate(vs):
                a = 0.7 * st["t"] + i * 2.09
                v.move_to([0.2 + 3.9 * np.cos(a), 1.95 + 0.75 * np.sin(a), 0])
        vs.add_updater(circ)
        circ(vs, 0)
        self.play(FadeIn(vs), run_time=1.0)
        q0 = T("buzzard?", 44, YELLOW, weight=BOLD).move_to([0, 0.4, 0])
        self.at("a vulture a buzzard")
        self.play(FadeIn(q0, scale=1.2), run_time=0.7)
        self.at("dark birds")
        self.play(FadeOut(q0), run_time=0.4)
        lab = T("Virginia highway", 28, TEXT).move_to([-4.6, 3.45, 0])
        self.at("a virginia highway")
        self.play(FadeIn(lab), run_time=0.6)
        # car
        car = VGroup(
            RoundedRectangle(corner_radius=0.25, width=3.4, height=0.9, fill_color="#D6453D", fill_opacity=1, stroke_color=OUTLINE, stroke_width=3).move_to([0, 0, 0]),
            RoundedRectangle(corner_radius=0.25, width=1.9, height=0.8, fill_color="#D6453D", fill_opacity=1, stroke_color=OUTLINE, stroke_width=3).move_to([-0.1, 0.7, 0]),
            RoundedRectangle(corner_radius=0.15, width=1.5, height=0.55, fill_color="#BFE3F5", fill_opacity=1, stroke_color=OUTLINE, stroke_width=2).move_to([-0.1, 0.72, 0]),
            Circle(radius=0.2, fill_color="#F1C9A5", fill_opacity=1, stroke_color=OUTLINE, stroke_width=2).move_to([-0.45, 0.75, 0]),
            Circle(radius=0.38, fill_color="#222", fill_opacity=1, stroke_color="#888", stroke_width=3).move_to([-1.0, -0.5, 0]),
            Circle(radius=0.38, fill_color="#222", fill_opacity=1, stroke_color="#888", stroke_width=3).move_to([1.0, -0.5, 0]),
        )
        car.move_to([-9.0, -2.05, 0])
        self.at("someone in the car")
        self.play(car.animate.move_to([-4.2, -2.05, 0]), run_time=1.3)
        bub = VGroup(RoundedRectangle(corner_radius=0.25, width=3.1, height=1.0, fill_color=BG, fill_opacity=1, stroke_color=YELLOW, stroke_width=3.5),
                     Polygon([-0.5, -0.5, 0], [-0.1, -0.5, 0], [-0.6, -0.95, 0], fill_color=BG, fill_opacity=1, stroke_color=YELLOW, stroke_width=3.5),
                     T("Buzzards!", 38, YELLOW, weight=BOLD)).move_to([-3.6, -0.3, 0])
        bub[2].move_to(bub[0])
        self.at("look")
        self.play(FadeIn(bub, shift=UP * 0.2), run_time=0.6)
        # British visitor
        vis = VGroup(
            Circle(radius=0.28, fill_color="#F1C9A5", fill_opacity=1, stroke_color=OUTLINE, stroke_width=2).move_to([0, 1.3, 0]),
            RoundedRectangle(corner_radius=0.15, width=0.8, height=1.2, fill_color="#3E6FB8", fill_opacity=1, stroke_color=OUTLINE, stroke_width=2).move_to([0, 0.45, 0]),
            Line([0.3, 0.8, 0], [0.7, 1.45, 0], color="#F1C9A5", stroke_width=8),
            RoundedRectangle(corner_radius=0.05, width=0.46, height=0.3, fill_color="#C8102E", fill_opacity=1, stroke_color=TEXT, stroke_width=2).move_to([0, 0.55, 0]),
        )
        vis.move_to([5.9, -2.15, 0])
        tb = VGroup(Ellipse(width=3.7, height=2.3, fill_color=BG, fill_opacity=1, stroke_color=TEXT, stroke_width=3),
                    icon("hawk", 1.3).move_to([0, 0.35, 0]),
                    T("buzzard (in Britain)", 22, TEXT).move_to([0, -0.7, 0])).move_to([4.2, -0.15, 0])
        self.at("a visitor from britain")
        self.play(FadeIn(vis, shift=LEFT * 0.4), run_time=0.8)
        self.at("looks up")
        self.play(FadeIn(tb, scale=0.8), run_time=0.8)
        q = T("?", 150, RED, weight=BOLD).move_to([0.2, -0.2, 0])
        self.at("for a hawk")
        self.play(FadeIn(q, scale=1.5), run_time=0.6)
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S02Plan(Base):
    def construct(self):
        tv = icon("turkey", 2.2).move_to([-3.5, -0.6, 0])
        hk = icon("hawk", 2.2).move_to([3.5, -0.6, 0])
        add_bob(tv, 0.0)
        add_bob(hk, 1.5)
        word = chip("buzzard", YELLOW, size=48).move_to([0, 2.2, 0])
        a1 = Arrow(word.get_bottom() + LEFT * 0.4, tv.get_top() + UP * 0.2, buff=0.1, color=YELLOW, stroke_width=6)
        a2 = Arrow(word.get_bottom() + RIGHT * 0.4, hk.get_top() + UP * 0.2, buff=0.1, color=YELLOW, stroke_width=6)
        lab = T("one word, two birds", 32, TEXT).move_to([0, 0.2, 0])
        self.add(word, tv, hk)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(lab), run_time=0.7)
        self.at("one name")
        self.play(FadeOut(VGroup(a1, a2, lab, word, tv, hk)), run_time=0.5)
        A = {n: animal(n) for n in ORDER_L}
        self.play(LaggedStart(*[FadeIn(A[n], shift=DOWN * 1.4) for n in ORDER_L], lag_ratio=0.3, run_time=2.4))
        self.at("to see where")
        P = self.bacteria()
        self.play(FadeIn(P, shift=RIGHT * 0.5), run_time=0.8)
        self.at("one inside the next")
        for n in ORDER_L:
            self.play(Pulse(A[n], 1.12), run_time=0.45)
        self.finish()


# -------------------------------------------------------------------------------------------------
def cell(nucleus=True, r=0.7):
    g = VGroup(Circle(radius=r, fill_color="#2a3a4a", fill_opacity=1, stroke_color=TEXT, stroke_width=3))
    if nucleus:
        g.add(Circle(radius=r * 0.32, fill_color=COL[0], fill_opacity=1, stroke_color=TEXT, stroke_width=2))
    return g


class S03Domain(Base):
    def construct(self):
        A = animals(0)
        self.add(*A.values())
        Pb = self.bacteria()
        r = rect_for(0)
        self.at("start with one huge box")
        self.play(Create(r), run_time=1.9)
        tab = tab_for(0)
        c = counter(1)
        self.at("domain eukarya")
        self.play(FadeIn(tab), FadeIn(c), run_time=0.7)
        self.at("it holds living things")
        cl = cell(True, 0.75).move_to([-1.2, 1.4, 0])
        self.play(FadeIn(cl), run_time=0.8)
        nuc = T("nucleus", 30, COL[0], weight=BOLD).move_to([1.2, 1.4, 0])
        nl = Arrow(nuc.get_left() + LEFT * 0.05, cl[1].get_right(), buff=0.08, color=COL[0], stroke_width=5)
        self.at("have a nucleus")
        self.play(FadeIn(nuc), GrowArrow(nl), run_time=0.7)
        self.play(Indicate(cl[1], color=TEXT, scale_factor=1.4), run_time=0.9)
        self.at("all seven fit inside")
        self.play(FadeOut(VGroup(cl, nuc, nl)), run_time=0.6)
        for n in ORDER_L:
            self.play(Pulse(A[n], 1.12), run_time=0.27)
        self.at("the bacteria stay outside")
        cl2 = cell(False, 0.55).move_to([-6.05, 1.5, 0])
        self.play(FadeIn(cl2), Indicate(Pb[0], color=TEXT), Indicate(Pb[1], color=TEXT), run_time=0.9)
        nn = T("no\nnucleus", 22, TEXT, line_spacing=0.8).move_to([-6.05, 2.5, 0])
        self.at("no nucleus")
        self.play(FadeIn(nn), run_time=0.6)
        self.finish()


class S04Kingdom(Base):
    def construct(self):
        P = self.world(1)
        A = P["A"]
        r = rect_for(1, left=left_of(0) + 0.12)
        self.at("a smaller box closes inside")
        self.play(Create(r), run_time=1.8)
        tab = tab_for(1)
        c2 = counter(2)
        self.at("kingdom animalia")
        self.play(FadeIn(tab), Transform(P["C"], c2), run_time=0.7)
        self.at("the animals")
        for n in ORDER_L[1:]:
            self.play(Pulse(A[n], 1.12), run_time=0.25)
        self.at("the pine twig is left outside")
        self.play(Transform(r, rect_for(1)), out_anim(A["pine"]), run_time=1.4)
        tg = plantae_tag()
        self.at("plants are another")
        self.play(FadeIn(tg, shift=UP * 0.15), run_time=0.7)
        self.play(Indicate(tg, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


class S05Phylum(Base):
    def construct(self):
        P = self.world(2)
        A = P["A"]
        r = rect_for(2, left=left_of(1) + 0.12)
        self.at("next comes the phylum")
        self.play(Create(r), run_time=2.2)
        tab = tab_for(2)
        self.at("ours is chordata")
        self.play(FadeIn(tab), Transform(P["C"], counter(3)), run_time=0.7)
        ROD, CORD = "#F5D547", "#58C4DD"
        lines_rod, lines_cord = VGroup(), VGroup()
        for n in ("trout", "cardinal"):
            x = X[n]
            lines_rod.add(Line([x - 0.5, AY + 0.5 - 0.0, 0], [x + 0.5, AY + 0.5, 0], color=ROD, stroke_width=7))
            lines_cord.add(Line([x - 0.5, AY + 0.66, 0], [x + 0.5, AY + 0.66, 0], color=CORD, stroke_width=7))
        l_rod = T("flexible rod", 30, ROD, weight=BOLD).move_to([-0.6, 1.5, 0])
        l_cord = T("hollow nerve cord", 30, CORD, weight=BOLD).move_to([2.7, 1.5, 0])
        self.at("flexible rod")
        self.play(Create(lines_rod), FadeIn(l_rod), run_time=1.0)
        self.at("hollow nerve cord")
        self.play(Create(lines_cord), FadeIn(l_cord), run_time=1.0)
        note = T("at least early in life (schematic)", 24, TEXT).move_to([1.2, 0.8, 0])
        self.at("at least early in life")
        self.play(FadeIn(note), run_time=0.8)
        self.at("fish birds and people")
        for n in ("trout", "cardinal", "hawk", "black", "turkey"):
            self.play(Pulse(A[n], 1.12), run_time=0.5)
        self.at("the crab has neither")
        self.play(FadeOut(VGroup(lines_rod, lines_cord, l_rod, l_cord, note)), run_time=0.5)
        self.play(Indicate(A["crab"], color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("left outside")
        self.play(Transform(r, rect_for(2)), out_anim(A["crab"]), run_time=1.3)
        self.finish()


class S06ClassOrder(Base):
    def construct(self):
        P = self.world(3)
        A = P["A"]
        r = rect_for(3, left=left_of(2) + 0.12)
        self.at("the class box")
        self.play(Create(r), run_time=0.9)
        tab = tab_for(3)
        self.at("is ivies")
        self.play(FadeIn(tab), Transform(P["C"], counter(4)), run_time=0.7)
        self.at("the birds")
        for n in ("cardinal", "hawk", "black", "turkey"):
            self.play(Pulse(A[n], 1.12), run_time=0.2)
        self.at("the trout is left outside")
        self.play(Transform(r, rect_for(3)), out_anim(A["trout"]), run_time=1.3)
        r5 = rect_for(4, left=left_of(3) + 0.12)
        self.at("then comes the order")
        self.play(Create(r5), run_time=1.5)
        tab5 = tab_for(4)
        self.at("in our database")
        self.play(FadeIn(tab5), Transform(P["C"], counter(5)), run_time=0.7)
        db = pill_note("in one database (ITIS)", TEXT, 22).move_to([4.2, 0.4, 0])
        self.play(FadeIn(db), run_time=0.6)
        self.at("holds hawks")
        for n in ("hawk", "black", "turkey"):
            self.play(Pulse(A[n], 1.12), run_time=0.5)
        self.at("the cardinal is left outside")
        self.play(FadeOut(db), run_time=0.4)
        self.play(Transform(r5, rect_for(4)), out_anim(A["cardinal"]), run_time=1.3)
        self.finish()


class S07Family(Base):
    def construct(self):
        P = self.world(5)
        A = P["A"]
        r = rect_for(5, left=left_of(4) + 0.12)
        self.at("the family box")
        self.play(Create(r), run_time=1.4)
        tab = tab_for(5)
        self.at("new world vultures")
        self.play(FadeIn(tab), Transform(P["C"], counter(6)), run_time=0.7)
        self.play(Pulse(A["black"], 1.12), Pulse(A["turkey"], 1.12), run_time=0.8)
        self.at("so the hawk is left outside")
        self.play(Transform(r, rect_for(5)), out_anim(A["hawk"]), run_time=1.3)
        self.at("two bareheaded vultures")
        rh = T("red head", 24, RED, weight=BOLD).move_to([X["turkey"], 0.25, 0])
        gh = T("grey head", 24, "#C4C8D0", weight=BOLD).move_to([X["black"], 0.25, 0])
        self.play(FadeIn(gh, shift=UP * 0.1), FadeIn(rh, shift=UP * 0.1), run_time=0.8)
        self.play(Pulse(A["black"], 1.15), Pulse(A["turkey"], 1.15), run_time=0.9)
        self.finish()


def clock_icon():
    face = Circle(radius=0.3, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1)
    hand = Line(ORIGIN, UP * 0.22, color=COL[6], stroke_width=4)
    g = VGroup(face, hand).move_to([6.2, 3.55, 0])
    hand.add_updater(lambda m, dt: m.rotate(-1.2 * dt, about_point=face.get_center()))
    return g


class S08Predict(Base):
    def construct(self):
        P = self.world(6)
        A = P["A"]
        self.play(Pulse(A["black"], 1.15), run_time=0.9)
        self.at("turkey vulture")
        self.play(Pulse(A["turkey"], 1.15), run_time=0.9)
        dr = rect_for(6, left=left_of(5) + 0.12, dashed=True)
        self.at("will it also fit")
        self.play(Create(dr), run_time=1.2)
        tab = tab_for(6, "7 GENUS: ?")
        card = self.card("Will the black vulture fit\nin the genus box too?", [-0.9, 1.2, 0], 5.6, 1.7, 30)
        ck = clock_icon()
        self.at("the genus")
        self.play(FadeIn(tab), FadeIn(card, shift=UP * 0.15), FadeIn(ck), run_time=0.8)
        self.finish()


class S09Pause(Base):
    def construct(self):
        P = self.world(6)
        A = P["A"]
        dr = rect_for(6, left=left_of(5) + 0.12, dashed=True)
        tab = tab_for(6, "7 GENUS: ?")
        r = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.5, stroke_color=COL[6], stroke_width=3, fill_color=BG, fill_opacity=0.97)
        t1 = T("Pause and predict: in or out?", 26, COL[6], weight=BOLD).move_to([0, 0.75, 0])
        t2 = T("Will the black vulture fit\nin the genus box too?", 30, TEXT, line_spacing=0.9).move_to([0, -0.05, 0])
        card = VGroup(r, t1, t2).move_to([-0.9, 1.35, 0]).set_z_index(9)
        bar = Rectangle(width=5.0, height=0.14, fill_color=COL[6], fill_opacity=1, stroke_width=0).move_to([-0.9, 0.4, 0]).set_z_index(10)
        ck = clock_icon()
        self.add(dr, tab, card, bar, ck)
        L0 = bar.get_left()
        st = {"t": 0.0}

        def shrink(m, dt):
            st["t"] += dt
            f = max(0.02, 1 - st["t"] / 5.0)
            m.stretch_to_fit_width(5.4 * f)
            m.move_to(L0 + RIGHT * 5.4 * f / 2)
        bar.add_updater(shrink)
        self.finish()


class S10Reveal(Base):
    def construct(self):
        P = self.world(6)
        A = P["A"]
        dr = rect_for(6, left=left_of(5) + 0.12, dashed=True)
        tabq = tab_for(6, "7 GENUS: ?")
        self.add(dr, tabq)
        self.at("among our seven")
        self.play(Pulse(A["black"], 1.12), Pulse(A["turkey"], 1.12), run_time=1.0)
        solid = rect_for(6, left=left_of(5) + 0.12)
        self.at("genus box closes")
        self.play(ReplacementTransform(dr, solid), run_time=0.6)
        self.play(Transform(solid, rect_for(6)), run_time=1.1)
        tab = tab_for(6)
        self.at("turkey vulture alone")
        self.play(ReplacementTransform(tabq, tab), Transform(P["C"], counter(7)), run_time=0.8)
        self.at("black vulture belongs")
        self.play(out_anim(A["black"]), run_time=1.0)
        tg = coragyps_tag()
        self.at("called")
        self.play(FadeIn(tg, shift=UP * 0.15), run_time=0.7)
        # tally strip, top right
        sq = VGroup(*[Square(0.3, fill_color=COL[i], fill_opacity=0.18, stroke_color=COL[i], stroke_width=2) for i in range(8)]).arrange(RIGHT, buff=0.08).move_to([4.7, 3.55, 0])
        tl = T("6 of 8 boxes shared", 26, TEXT, weight=BOLD).move_to([1.2, 3.55, 0])
        tl.align_to(sq, LEFT).shift(LEFT * 0.35 + RIGHT * 0).set_x(sq.get_left()[0] - 0.3 - tl.width / 2)
        self.at("it shares six boxes")
        self.play(FadeIn(sq), FadeIn(tl), run_time=0.6)
        for i in range(6):
            self.play(sq[i].animate.set_fill(COL[i], 1), run_time=0.28)
        note = pill_note("other Cathartes species not shown", TEXT, 22).move_to([-0.1, 0.48, 0])
        self.at("not seven")
        self.play(FadeIn(note), Indicate(sq[6], color=TEXT), run_time=0.8)
        self.play(Pulse(A["turkey"], 1.12), run_time=0.8)
        self.finish()


class S11Species(Base):
    def construct(self):
        P = self.world(7)
        cg = coragyps_tag()
        self.add(cg)
        A = P["A"]
        r = rect_for(7, left=left_of(6) + 0.0)
        self.at("the last of our eight")
        self.play(Create(r), run_time=1.6)
        tab = tab_for(7)
        self.at("the species")
        self.play(FadeIn(tab), Transform(P["C"], counter(8)), run_time=0.7)
        # inset nest
        panel = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.5, stroke_color=COL[7], stroke_width=3, fill_color=BG, fill_opacity=0.97).move_to([-0.9, 1.5, 0])
        nest = Arc(radius=0.75, start_angle=PI, angle=PI, color="#9A6B3C", stroke_width=10).move_to([-2.8, 1.45, 0])
        a1 = icon("turkey", 0.85).move_to([-3.2, 1.75, 0])
        a2 = icon("turkey", 0.85).move_to([-2.4, 1.75, 0])
        a2.flip()
        for m in (panel, nest, a1, a2):
            m.set_z_index(9)
        self.at("a species is a group")
        self.play(FadeIn(panel), FadeIn(nest), FadeIn(a1), FadeIn(a2), run_time=0.9)
        lab = T("can mate in nature,\nyoung can also reproduce", 22, TEXT, line_spacing=0.85).move_to([0.0, 2.0, 0]).set_z_index(9)
        heart = T("+", 44, COL[7], weight=BOLD).move_to([-2.8, 2.25, 0]).set_z_index(10)
        self.at("can mate in nature")
        self.play(FadeIn(heart, scale=1.4), FadeIn(lab), run_time=0.8)
        chick = icon("turkey", 0.5).move_to([-2.8, 1.0, 0]).set_z_index(10)
        self.at("their young")
        self.play(FadeIn(chick, shift=UP * 0.3), run_time=0.8)
        st = {"t": 0.0}

        def hop(m, dt):
            st["t"] += dt
            m.move_to([-2.8, 1.0 + 0.07 * abs(np.sin(3.0 * st["t"])), 0])
        chick.add_updater(hop)
        self.at("can also reproduce")
        self.play(Indicate(chick, color=COL[7], scale_factor=1.3), run_time=0.9)
        note = T("a useful rule, with limits", 22, TEXT, weight=BOLD).move_to([0.0, 0.8, 0]).set_z_index(9)
        self.at("this is a useful rule")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.at("sex cells")
        self.play(Indicate(heart, color=COL[7], scale_factor=1.3), run_time=0.8)
        self.at("it has limits")
        self.play(Indicate(note, color=COL[7], scale_factor=1.12), run_time=0.9)
        self.finish()


class S12Name(Base):
    def construct(self):
        P = self.world(8)
        P["tags"].append(coragyps_tag())
        self.add(P["tags"][-1])
        keep = VGroup(P["T"][6], P["T"][7])
        rest = VGroup(*[m for m in self.mobjects if m not in keep.submobjects and m is not keep and m not in P["bact"].submobjects and m is not P["bact"]])
        self.play(Pulse(P["T"][6], 1.15), Pulse(P["T"][7], 1.15), run_time=0.5)
        self.play(FadeOut(rest), FadeOut(P["bact"]), run_time=0.5)
        gname = T("Cathartes", 76, COL[6], slant=ITALIC, weight=BOLD)
        aura = T("aura", 76, COL[7], slant=ITALIC, weight=BOLD)
        row = VGroup(gname, aura).arrange(RIGHT, buff=0.45).move_to([0, 1.7, 0])
        pill = SurroundingRectangle(gname, buff=0.25, color=COL[6], stroke_width=4, corner_radius=0.2)
        self.at("labeled cathartes")
        self.play(ReplacementTransform(P["T"][6], VGroup(pill, gname)), run_time=1.0)
        gl = T("genus name", 30, COL[6]).next_to(gname, DOWN, buff=0.45)
        self.play(FadeIn(gl), run_time=0.5)
        self.at("add a second word")
        self.play(Write(aura), run_time=1.0)
        sl = T("second word", 30, COL[7]).next_to(aura, DOWN, buff=0.45).align_to(gl, UP)
        self.at("second word")
        self.play(FadeIn(sl), run_time=0.5)
        sp = VGroup(gname.copy(), aura.copy()).arrange(RIGHT, buff=0.45).move_to([0, -1.3, 0])
        box = SurroundingRectangle(sp, buff=0.3, color=COL[7], stroke_width=5, corner_radius=0.25)
        self.at("you have the species name")
        self.play(ReplacementTransform(P["T"][7], box), FadeOut(gl), FadeOut(sl), run_time=0.6)
        self.play(TransformFromCopy(gname, sp[0]), TransformFromCopy(aura, sp[1]), run_time=0.8)
        br = Brace(box, DOWN, color=COL[7], buff=0.1)
        bl = T("species name", 32, COL[7], weight=BOLD).next_to(br, DOWN, buff=0.15)
        self.at("cathartes aura", nth=0)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.8)
        self.finish()


class S13Rules(Base):
    def construct(self):
        name = T("Cathartes aura", 80, TEXT, slant=ITALIC, weight=BOLD).move_to([0.7, 2.1, 0])
        self.add(name)
        self.play(Indicate(name, color=TEXT, scale_factor=1.04), run_time=0.8)
        capC = SurroundingRectangle(name[0], buff=0.1, color=COL[6], stroke_width=5)
        capl = T("capital", 30, COL[6], weight=BOLD).next_to(capC, UP, buff=0.15)
        self.at("capital letter")
        self.play(Create(capC), FadeIn(capl), run_time=0.8)
        lowa = SurroundingRectangle(name[10], buff=0.1, color=COL[7], stroke_width=5)
        lowl = T("lowercase", 30, COL[7], weight=BOLD).next_to(lowa, DOWN, buff=0.15)
        self.at("lowercase")
        self.play(Create(lowa), FadeIn(lowl), run_time=0.8)
        self.at("print both words")
        self.play(FadeOut(VGroup(capC, capl, lowa, lowl)), run_time=0.5)
        ptag = T("print", 30, TEXT, weight=BOLD).move_to([-5.9, 2.1, 0])
        self.play(FadeIn(ptag), run_time=0.5)
        it = T("in italics", 30, TEXT, weight=BOLD).move_to([-5.9, 1.55, 0])
        self.at("italics")
        self.play(FadeIn(it), Indicate(name, color=TEXT, scale_factor=1.04), run_time=0.6)
        hand = T("Cathartes aura", 76, TEXT, weight=BOLD, font="Bradley Hand").move_to([0.7, 0.35, 0])
        htag = T("by hand", 30, TEXT, weight=BOLD).move_to([-5.9, 0.35, 0])
        self.at("underline both")
        self.play(FadeIn(hand), FadeIn(htag), run_time=0.6)
        self.at("both by hand")
        u1 = Line(hand.get_corner(DL) + DOWN * 0.08, hand.get_corner(DL) + RIGHT * hand.width * 0.55 + DOWN * 0.08, color=COL[6], stroke_width=6)
        u2 = Line(hand.get_corner(DL) + RIGHT * hand.width * 0.6 + DOWN * 0.08, hand.get_corner(DR) + DOWN * 0.08, color=COL[7], stroke_width=6)
        self.play(Create(u1), Create(u2), run_time=1.0)
        # globe + two speech bubbles
        self.play(FadeOut(VGroup(ptag, it, htag)), run_time=0.4)
        self.at("a scientist in japan")
        globe = VGroup(Circle(radius=0.65, stroke_color=BLUE, stroke_width=3, fill_color="#1d3550", fill_opacity=1),
                       Line([-0.65, 0, 0], [0.65, 0, 0], color=BLUE, stroke_width=2),
                       Ellipse(width=1.0, height=1.3, stroke_color=BLUE, stroke_width=2),
                       Ellipse(width=1.0, height=1.3, stroke_color=BLUE, stroke_width=2)).move_to([0, -1.0, 0])
        st = {"t": 0.0}

        def spin(m, dt):
            st["t"] += dt
            for j, mer in enumerate((globe[2], globe[3])):
                mer.stretch_to_fit_width(0.06 + 1.24 * abs(np.cos(1.1 * st["t"] + j * 1.5)))
                mer.move_to(globe[0].get_center())
        globe.add_updater(spin)
        tvi = icon("turkey", 1.7).move_to([0, -2.55, 0])
        add_bob(tvi, 0.5)
        bj = VGroup(RoundedRectangle(corner_radius=0.2, width=4.4, height=1.6, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1),
                    T("Japan", 24, TEXT), T("Cathartes aura", 36, TEXT, slant=ITALIC)).move_to([-4.4, -2.5, 0])
        bj[1].move_to(bj[0].get_center() + UP * 0.38); bj[2].move_to(bj[0].get_center() + DOWN * 0.2)
        bv = bj.copy().move_to([4.4, -2.5, 0])
        bv[1].become(T("Virginia", 24, TEXT).move_to(bv[0].get_center() + UP * 0.38))
        self.play(FadeIn(globe), FadeIn(bj, shift=RIGHT * 0.3), run_time=0.9)
        self.at("who writes")
        self.play(FadeIn(bv, shift=LEFT * 0.3), run_time=0.8)
        a1 = Arrow(bj.get_right(), tvi.get_left() + LEFT * 0.1, buff=0.1, color=COL[7], stroke_width=5)
        a2 = Arrow(bv.get_left(), tvi.get_right() + RIGHT * 0.1, buff=0.1, color=COL[7], stroke_width=5)
        self.at("means the same bird")
        self.play(FadeIn(tvi), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.at("you see in virginia")
        self.play(Pulse(tvi, 1.2), run_time=0.9)
        self.finish()


class S14Buzzard(Base):
    def construct(self):
        div = DashedLine([0, 3.6, 0], [0, -3.6, 0], color=GREY, stroke_width=3)
        tv = icon("turkey", 2.7).move_to([-3.4, 0.8, 0])
        add_bob(tv, 0.0)
        n1 = T("Cathartes aura", 38, COL[7], slant=ITALIC, weight=BOLD).move_to([-3.4, -1.3, 0])
        l1 = T("Virginia", 30, TEXT, weight=BOLD).move_to([-3.4, 3.1, 0])
        self.add(div, tv, n1, l1)
        bz = chip("buzzard", YELLOW, size=40).move_to([-1.4, 2.0, 0])
        st = {"t": 0.0}

        def flo(m, dt):
            st["t"] += dt
            m.move_to([-1.4 + 0.1 * np.sin(1.2 * st["t"]), 2.0 + 0.15 * np.sin(2.1 * st["t"]), 0])
        bz.add_updater(flo)
        self.play(FadeIn(bz), run_time=0.6)
        hk = icon("hawk", 2.7).move_to([3.4, 0.8, 0])
        add_bob(hk, 1.4)
        l2 = T("Britain", 30, TEXT, weight=BOLD).move_to([3.4, 3.1, 0])
        self.at("britain")
        self.play(FadeIn(hk, shift=LEFT * 0.4), FadeIn(l2), run_time=0.9)
        self.at("has its own name")
        self.play(FadeOut(bz), run_time=0.8)
        n2 = T("Buteo buteo", 38, GREEN, slant=ITALIC, weight=BOLD).move_to([3.4, -1.3, 0])
        self.until(3.5)
        self.play(Write(n2), run_time=1.3)
        self.at("two names")
        self.play(Pulse(n1, 1.12), Pulse(n2, 1.12), run_time=1.0)
        self.at("two birds")
        self.play(Pulse(tv, 1.1), Pulse(hk, 1.1), run_time=1.0)
        self.finish()


class S15Rule(Base):
    def construct(self):
        P = self.world(8, show_bact=False)
        cg = coragyps_tag()
        self.add(cg)
        A = P["A"]
        panel = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.5, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.98).move_to([-0.9, 1.5, 0]).set_z_index(8)

        def strip(n_lit, y):
            s = VGroup(*[Square(0.3, fill_color=COL[i], fill_opacity=(1 if i < n_lit else 0.15), stroke_color=COL[i], stroke_width=2) for i in range(8)]).arrange(RIGHT, buff=0.06)
            s.move_to([0, y, 0]).set_z_index(9)
            s.set_x(0.3)
            return s
        sb, sh = strip(6, 2.3), strip(5, 1.75)
        lb = T("black vulture", 24, TEXT, weight=BOLD).set_z_index(9)
        lh = T("hawk", 24, TEXT, weight=BOLD).set_z_index(9)
        lb.move_to([-3.5 + lb.width / 2, 2.3, 0]); lh.move_to([-3.5 + lh.width / 2, 1.75, 0])
        self.at("the black vulture stayed")
        self.play(FadeIn(panel), FadeIn(lb), run_time=0.6)
        self.play(FadeIn(sb), Pulse(A["black"], 1.15), run_time=0.9)
        self.at("and the hawk left sooner")
        self.play(FadeIn(lh), FadeIn(sh), Pulse(A["hawk"], 1.15), run_time=0.9)
        rule = T("More shared boxes =\ngrouped more closely.", 30, GREEN, weight=BOLD, line_spacing=0.9).move_to([-0.9, 0.85, 0]).set_z_index(9)
        self.at("the more boxes two living things share")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.9)
        self.at("the more closely")
        self.play(Indicate(rule, color=GREEN, scale_factor=1.06), run_time=0.9)
        note = T("walls can move when scientists\nlearn more (schematic)", 22, TEXT, line_spacing=0.85).move_to([-0.9, 2.05, 0]).set_z_index(9)
        self.at("scientists can redraw")
        self.play(FadeOut(VGroup(sb, sh, lb, lh)), FadeIn(note), run_time=0.6)
        r = P["R"][4]
        self.play(Transform(r, rect_for(4, left=left_of(4) - 0.3)), run_time=0.9, rate_func=there_and_back)
        self.play(Transform(r, rect_for(4, left=left_of(4) - 0.3)), run_time=0.9, rate_func=there_and_back)
        self.finish()


class S16End(EndCard):
    LINE = "The more boxes two living things share, the more closely they're grouped."
