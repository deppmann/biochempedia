"""Same Protein, Different Switch (evolution of development), Biochemistrypedia film.

COLOR MAP (whole film)
  BLUE   = marine fish and anything marine
  ORANGE = Paxton Lake fish and anything Paxton
  GOLD   = Pitx1 RNA (glows where the gene is used)
  PURPLE = Pitx1 protein (blob)
  GREY-WHITE = DNA, coding block
  TEAL   = enhancer (switch tab)
  RED    = broken / not working;  GREEN = same / tick / on
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DNA_C = "#B9BFCC"
LARVA = "#C9CED9"
CLK = [0.0]
PEL = (0.1, -0.68)
JAW = (1.4, -0.2)


def bubbles(sc, n=14, seed=1):
    rng = np.random.RandomState(seed)
    ds = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.03, 0.08), color=TEAL).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-6.9, 6.9), rng.uniform(-4, 4), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.25, 0.6))

        def up(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.2:
                m.shift(DOWN * 8.4)
        d.add_updater(up)
        ds.add(d)
    ds.set_z_index(-10)
    sc.add(ds)


def start(sc):
    CLK[0] = 0.0
    c = Dot(radius=0.01).set_opacity(0)

    def tk(m, dt):
        CLK[0] += dt
    c.add_updater(tk)
    sc.add(c)
    bubbles(sc)


def bob(m, amp=0.08, sp=1.4):
    m._b = 0.0

    def u(mm, dt):
        d = amp * np.sin(sp * CLK[0])
        mm.shift(UP * (d - mm._b))
        mm._b = d
    m.add_updater(u)
    return m


def pulse(m, amp=0.1, sp=3.2):
    m._f = 1.0

    def u(mm, dt):
        f = 1 + amp * np.sin(sp * CLK[0])
        mm.scale(f / mm._f)
        mm._f = f
    m.add_updater(u)
    return m


def fish(color, pos, s=1.0, pelvis="full"):
    st = dict(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22)
    body = Ellipse(width=3.6, height=1.4, **st)
    tail = Polygon([-1.7, 0, 0], [-2.6, 0.65, 0], [-2.6, -0.65, 0], **st)
    eye = Dot([1.2, 0.2, 0], radius=0.07, color=TEXT)
    pel = VGroup()
    if pelvis in ("full", "stub"):
        pel.add(RoundedRectangle(corner_radius=0.06, width=0.6, height=0.2, stroke_width=0,
                                 fill_color=TEXT, fill_opacity=0.9).move_to([PEL[0], PEL[1], 0]))
    if pelvis == "full":
        pel.add(Line([-0.05, -0.72, 0], [-0.5, -1.75, 0], color=TEXT, stroke_width=6),
                Line([0.25, -0.72, 0], [0.1, -1.75, 0], color=TEXT, stroke_width=6))
    g = VGroup(tail, body, eye, pel)
    g.scale(s, about_point=ORIGIN).shift(np.array([pos[0], pos[1], 0]))
    g.s, g.o, g.pel = s, np.array([pos[0], pos[1], 0.0]), pel
    return g


def loc(g, p):
    return g.o + np.array([p[0], p[1], 0]) * g.s


def glow(pt, r=0.3):
    return Circle(radius=r, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(pt)


def ring(pt, r=0.5, color=RED):
    return Circle(radius=r, stroke_color=color, stroke_width=6, fill_opacity=0).move_to(pt)


def xmark(pos, size=0.5, color=RED):
    p = np.array([pos[0], pos[1], 0])
    return VGroup(Line(p + [-size, -size, 0], p + [size, size, 0]), Line(p + [-size, size, 0], p + [size, -size, 0])).set_stroke(color, 9)


def tickm(pos, color=GREEN, k=1.0):
    p = np.array([pos[0], pos[1], 0])
    return VGroup(Line(p + np.array([-0.25, 0.0, 0]) * k, p + np.array([-0.07, -0.22, 0]) * k),
                  Line(p + np.array([-0.07, -0.22, 0]) * k, p + np.array([0.3, 0.26, 0]) * k)).set_stroke(color, 8)


def blob(color, pos, r=0.5):
    g = VGroup()
    for k, o in [(1, (0, 0)), (0.7, (0.7, 0.4)), (0.65, (-0.7, 0.3)), (0.6, (0.2, -0.7))]:
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=0.9)
              .move_to(np.array([pos[0], pos[1], 0]) + np.array([o[0], o[1], 0]) * r))
    return g


def gblob(pos, r=0.32):
    g = VGroup(Ellipse(width=r * 2.6, height=r * 1.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55).rotate(0.4),
               Ellipse(width=r * 1.2, height=r * 1.0, stroke_width=0, fill_color=GREY, fill_opacity=0.55).shift([r * 0.9, r * 0.5, 0]))
    return g.move_to([pos[0], pos[1], 0])


def dna_line(y):
    return Line([-6.5, y, 0], [6.5, y, 0], color=DNA_C, stroke_width=10)


def coding(y, x=-3.8, w=4.2):
    blk = RoundedRectangle(corner_radius=0.12, width=w, height=1.0, stroke_color=DNA_C, stroke_width=3,
                           fill_color="#2B2F3A", fill_opacity=1).move_to([x, y, 0])
    return VGroup(blk, T("Pitx1 coding part", 30).move_to(blk))


def tab(label, x, y, w=2.7, color=TEAL, up=True):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=0.75, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35 if up else 0.1)
    r.move_to([x, y + 0.55, 0])
    return VGroup(r, T(label, 30).move_to(r))


def wire(a, b):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=GOLD, stroke_width=5)


def bead_row(color, cx, y, n=9):
    xs = [cx + (i - (n - 1) / 2) * 0.5 for i in range(n)]
    g = VGroup(Line([xs[0], y, 0], [xs[-1], y, 0], color=color, stroke_width=3))
    for x in xs:
        g.add(Circle(radius=0.19, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x, y, 0]))
    return g


class S00Title(TitleCard):
    LESSON = "Evolution of development"
    TITLE = "Same Protein, Different Switch"


class S01Question(SpokenScene):
    def construct(self):
        start(self)
        f = fish(ORANGE, (-1.0, -0.5), 2.0, "none")
        f.shift(RIGHT * 8)
        self.add(f)
        self.play(f.animate.shift(LEFT * 8), run_time=1.4)
        bob(f)
        rg = DashedVMobject(Circle(radius=0.6, color=ORANGE, stroke_width=5)).move_to(loc(f, PEL))
        self.at("almost no")
        self.play(Create(rg), run_time=1.0)
        pb = blob(PURPLE, (4.9, 2.0), 0.7)
        pl = T("Pitx1 protein", 34, PURPLE).move_to([4.9, 0.75, 0])
        self.at("yet its")
        self.play(GrowFromCenter(pb), FadeIn(pl), run_time=1.0)
        un = T("unchanged", 34, GREEN).move_to([5.2, -0.2, 0])
        tk = tickm((un.get_left()[0] - 0.4, -0.2))
        self.at("unchanged")
        self.play(Create(tk), FadeIn(un), run_time=0.9)
        q = T("?", 150, YELLOW).move_to([2.6, 2.2, 0])
        self.at("so what")
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        pulse(q)
        self.at("kind of switch")
        q.clear_updaters()
        sw = chip("switch", TEAL, 40).move_to([2.6, 2.2, 0])
        self.play(Transform(q, sw), run_time=1.0)
        self.finish()


class S02Fish(SpokenScene):
    def construct(self):
        start(self)
        b = fish(BLUE, (-3.3, 0.7), 1.3, "full")
        b.shift(LEFT * 7)
        self.add(b)
        self.play(b.animate.shift(RIGHT * 7), run_time=2.2)
        bob(b)
        lb = T("marine", 34, BLUE).move_to([-3.3, 2.6, 0])
        self.play(FadeIn(lb), run_time=0.5)
        self.at("bony girdle")
        pl = T("pelvis", 34, TEXT).move_to([-5.3, -1.1, 0])
        self.play(Indicate(b.pel, color=WHITE, scale_factor=1.15), FadeIn(pl), run_time=1.4)
        self.at("version of your")
        dl = DashedLine([-3.5, -1.75, 0], [-3.5, -2.2, 0], color=GREY)
        hl = T("like your hips and legs", 34, TEXT).move_to([-3.3, -2.6, 0])
        sa = T("same ancestral structure", 30, TEXT).move_to([-3.3, -3.35, 0])
        self.play(Create(dl), FadeIn(hl), run_time=0.8)
        self.play(FadeIn(sa), run_time=0.8)
        o = fish(ORANGE, (3.5, 0.7), 1.3, "full")
        o.shift(RIGHT * 7)
        self.at("paxton lake")
        self.add(o)
        self.play(o.animate.shift(LEFT * 7), run_time=2.0)
        bob(o)
        pin = VGroup(Dot(radius=0.12, color=RED), T("Paxton Lake, British Columbia", 34, ORANGE)).arrange(RIGHT, buff=0.2).move_to([2.9, 2.7, 0])
        self.play(FadeIn(pin), run_time=0.8)
        self.at("greatly reduced")
        stub = o.pel
        self.play(stub[1].animate.scale(0.05, about_point=stub[1].get_top()).set_opacity(0),
                  stub[2].animate.scale(0.05, about_point=stub[2].get_top()).set_opacity(0), run_time=1.2)
        gl = T("greatly reduced", 34, ORANGE).move_to([3.5, -1.3, 0])
        self.play(FadeIn(gl), run_time=0.6)
        self.at("pelvic bones")
        none = T("most: none", 34, ORANGE).move_to([3.5, -1.3, 0])
        self.play(FadeOut(stub[0]), Transform(gl, none), run_time=1.2)
        self.finish()


class S03Gene(SpokenScene):
    def construct(self):
        start(self)
        y = 1.0
        ln = dna_line(y)
        cd = coding(y)
        self.play(Create(ln), run_time=1.2)
        self.play(FadeIn(cd), run_time=0.8)
        self.at("its protein")
        bl = blob(PURPLE, (-3.8, y), 0.6)
        lab = T("Pitx1 protein", 34, PURPLE).move_to([-3.8, 3.4, 0])
        self.play(GrowFromCenter(bl), run_time=0.5)
        self.play(bl.animate.move_to([-3.8, 2.4, 0]), FadeIn(lab), run_time=0.9)
        grp = VGroup(bl, lab)
        self.at("transcription factor")
        lab2 = T("transcription factor", 34, PURPLE).move_to(lab)
        self.play(Transform(lab, lab2), run_time=0.8)
        site = Rectangle(width=0.7, height=0.3, stroke_width=0, fill_color=WHITE, fill_opacity=0.7).move_to([1.0, y, 0])
        self.at("binds dna")
        self.play(grp.animate.shift(RIGHT * 4.8 + DOWN * 0.2), FadeIn(site), run_time=1.6)
        tg = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.9, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.05).move_to([4.7, y, 0])
        tl = T("other gene", 30, GREEN).move_to(tg)
        under = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.9, stroke_width=0, fill_color="#0E1118", fill_opacity=1).move_to(tg)
        tl.set_z_index(3)
        tg.set_z_index(2)
        under.set_z_index(1)
        self.at("switches other")
        self.add(under)
        self.play(FadeIn(tg), FadeIn(tl), run_time=0.9)
        self.at("on or off")
        self.play(tg.animate.set_fill(GREEN, 0.7), tl.animate.set_color(WHITE), run_time=0.8)
        self.at("in the")
        self.remove(under)
        self.play(FadeOut(grp), FadeOut(tl), FadeOut(tg), FadeOut(site), run_time=0.8)
        r1 = bead_row(BLUE, 0.6, -0.5)
        r2 = bead_row(ORANGE, 0.6, -1.5)
        r2.shift(RIGHT * 2.5)
        l1 = T("marine", 34, BLUE).move_to([-4.5, -0.5, 0])
        l2 = T("Paxton", 34, ORANGE).move_to([-4.5, -1.5, 0])
        self.play(FadeIn(r1), FadeIn(l1), FadeIn(r2), FadeIn(l2), run_time=1.0)
        self.at("that protein")
        self.play(r2.animate.shift(LEFT * 2.5), run_time=0.9)
        links = VGroup(*[Line([r1[i].get_x(), -0.72, 0], [r1[i].get_x(), -1.28, 0], color=GREEN, stroke_width=3) for i in range(1, 10)])
        st = T("same encoded protein (fish examined)", 34, GREEN)
        box = SurroundingRectangle(st, color=GREEN, buff=0.18, corner_radius=0.12)
        sg = VGroup(box, st).move_to([0, -3.0, 0])
        self.at("unchanged")
        self.play(Create(links), FadeIn(sg, scale=1.2), run_time=0.9)
        self.finish()


class S04Jobs(SpokenScene):
    def construct(self):
        start(self)
        f = fish(LARVA, (3.7, -1.0), 1.4, "stub")
        f.shift(RIGHT * 3)
        self.add(f)
        self.play(f.animate.shift(LEFT * 3), run_time=1.2)
        bob(f)
        gp = glow(loc(f, PEL))
        gj = glow(loc(f, JAW))
        bob(gp)
        bob(gj)
        hdr = T("Pitx1 used here", 34, GOLD).move_to([3.7, 0.8, 0])
        self.at("pelvis gene")
        self.play(FadeIn(gp, scale=0.3), FadeIn(hdr), run_time=0.9)
        pl = T("pelvic region", 32, GOLD).move_to([2.9, -2.8, 0])
        self.play(FadeIn(pl), run_time=0.5)
        self.at("the jaw")
        jl = T("jaw", 32, GOLD).move_to([5.7, -2.1, 0])
        self.play(FadeIn(gj, scale=0.3), FadeIn(jl), run_time=0.9)
        # mouse
        body = Ellipse(width=1.7, height=1.0, stroke_color=LARVA, stroke_width=3, fill_color=LARVA, fill_opacity=0.2)
        head = Circle(radius=0.42, stroke_color=LARVA, stroke_width=3, fill_color=LARVA, fill_opacity=0.2).move_to([1.05, 0.2, 0])
        ear = Circle(radius=0.2, stroke_color=LARVA, stroke_width=3).move_to([0.95, 0.65, 0])
        tail = ArcBetweenPoints([-0.85, 0, 0], [-1.7, 0.7, 0], angle=-1.2, color=LARVA, stroke_width=3)
        eye = Dot([1.2, 0.3, 0], radius=0.05, color=TEXT)
        mouse = VGroup(body, head, ear, tail, eye).scale(1.15).move_to([-4.2, 1.8, 0])
        pb = blob(PURPLE, (-1.3, 1.8), 0.4)
        xg = xmark((-1.3, 1.8), 0.45, GREY)
        self.at("mice with")
        self.play(FadeIn(mouse, shift=RIGHT * 0.3), run_time=0.9)
        self.play(FadeIn(pb), Create(xg), run_time=0.8)
        t1 = T("hind limbs malformed", 34, TEXT).move_to([-3.4, -0.1, 0])
        t2 = T("other defects", 34, TEXT).move_to([-3.4, -1.1, 0])
        t3 = T("does not survive", 34, RED).move_to([-3.4, -2.1, 0])
        self.at("dye")
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.6)
        self.at("malformed hind limbs")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("other defects")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.finish()


def predict_world(sc, text=True, x_on=True):
    """DNA with the coding block, larva on the right with gold RNA, grey blobs: the s05 frame."""
    ln = dna_line(2.5)
    cd = coding(2.5)
    f = fish(LARVA, (3.7, -1.0), 1.4, "stub")
    gp, gj = glow(loc(f, PEL)), glow(loc(f, JAW))
    xm = xmark((-1.55, 3.05), 0.28)
    bp, bj = gblob((3.85, 0.6)), gblob((5.6, 0.6))
    qp = T("?", 36, YELLOW).move_to(bp)
    qj = T("?", 36, YELLOW).move_to(bj)
    return dict(ln=ln, cd=cd, f=f, gp=gp, gj=gj, xm=xm, bp=bp, bj=bj, qp=qp, qj=qj)


class S05Predict(SpokenScene):
    def construct(self):
        start(self)
        w = predict_world(self)
        self.add(w["f"], w["gp"], w["gj"])
        for k in ("f", "gp", "gj"):
            bob(w[k])
        self.play(Create(w["ln"]), FadeIn(w["cd"]), run_time=1.2)
        self.at("broken")
        self.play(Create(w["xm"]), run_time=0.7)
        pp = blob(PURPLE, (3.85, 0.6), 0.3)
        pj = blob(PURPLE, (5.6, 0.6), 0.3)
        self.at("protein itself")
        self.play(FadeIn(pp), FadeIn(pj), run_time=0.8)
        t = VGroup(T("Broken protein:", 42, YELLOW), T("where is the damage?", 42, YELLOW)).arrange(DOWN, buff=0.25).move_to([-3.4, -0.6, 0])
        self.at("where would")
        self.play(FadeIn(t, shift=UP * 0.15), run_time=0.9)
        self.at("damage")
        self.play(Transform(pp, w["bp"]), Transform(pj, w["bj"]), run_time=1.0)
        self.play(FadeIn(w["qp"]), FadeIn(w["qj"]), run_time=0.6)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        start(self)
        w = predict_world(self)
        t = VGroup(T("Broken protein:", 42, YELLOW), T("where is the damage?", 42, YELLOW)).arrange(DOWN, buff=0.25).move_to([-3.4, -0.6, 0])
        self.add(w["ln"], w["cd"], w["f"], w["gp"], w["gj"], w["xm"], w["bp"], w["bj"], w["qp"], w["qj"], t)
        for k in ("f", "gp", "gj"):
            bob(w[k])
        rg = Circle(radius=0.55, color=YELLOW, stroke_width=8).move_to([-3.4, 1.0, 0]).rotate(PI / 2).flip()
        base = Circle(radius=0.55, color=GREY, stroke_width=3).move_to([-3.4, 1.0, 0])
        self.add(base)
        self.play(Create(rg), run_time=4.8, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        start(self)
        w = predict_world(self)
        t = VGroup(T("Broken protein:", 42, YELLOW), T("where is the damage?", 42, YELLOW)).arrange(DOWN, buff=0.25).move_to([-3.4, -0.6, 0])
        self.add(w["ln"], w["cd"], w["f"], w["gp"], w["gj"], w["xm"], w["bp"], w["bj"], w["qp"], w["qj"], t)
        for k in ("f", "gp", "gj"):
            bob(w[k])
        self.at("everywhere the gene")
        lab = VGroup(T("RNA made,", 42, GOLD), T("protein does not work", 42, RED)).arrange(DOWN, buff=0.25).move_to([-3.2, -0.6, 0])
        self.play(FadeOut(t), FadeOut(w["qp"]), FadeOut(w["qj"]), run_time=0.5)
        self.play(FadeIn(lab), run_time=0.6)
        dj = Square(0.55, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([5.6, 1.6, 0])
        dp = Square(0.55, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([3.85, 1.6, 0])
        self.at("fail in")
        self.play(FadeIn(dj), FadeIn(dp), run_time=0.8)
        rj = ring(loc(w["f"], JAW), 0.55)
        rp = ring(loc(w["f"], PEL), 0.55)
        self.at("the jaw")
        self.play(Create(rj), run_time=0.8)
        self.at("the pelvis")
        self.play(Create(rp), run_time=0.8)
        self.at("lake fish do not")
        o = fish(ORANGE, (-3.0, -1.0), 1.4, "none")
        o.shift(LEFT * 6)
        og = glow(loc(o, JAW))
        og.shift(LEFT * 6)
        self.add(o, og)
        self.play(FadeOut(lab), FadeOut(w["ln"]), FadeOut(w["cd"]), FadeOut(w["xm"]), run_time=0.6)
        self.play(o.animate.shift(RIGHT * 6), og.animate.shift(RIGHT * 6), run_time=1.6)
        bob(o)
        bob(og)
        cap = T("Pitx1 RNA kept in", 34, GOLD)
        cap2 = T("mouth and lower jaw", 34, GOLD)
        cp = VGroup(cap, cap2).arrange(DOWN, buff=0.12).move_to([-3.0, -3.0, 0])
        ban = T("not a broken protein", 46, TEXT).move_to([0, 3.1, 0])
        self.play(FadeIn(cp), FadeIn(ban), run_time=1.0)
        self.finish()


class S08Enhancer(SpokenScene):
    def construct(self):
        start(self)
        ln = dna_line(2.1)
        cd = coding(2.1)
        xm = xmark((-1.55, 2.65), 0.28)
        f = fish(LARVA, (3.7, -1.0), 1.4, "stub")
        self.add(ln, cd, xm, f)
        bob(f)
        self.at("the way out")
        self.play(FadeOut(xm), run_time=0.8)
        tp = tab("pelvic switch", 1.3, 2.1, up=False)
        tj = tab("jaw switch", 4.3, 2.1, up=False)
        el = T("enhancer: noncoding DNA", 32, TEAL).move_to([3.0, 3.45, 0])
        self.at("short stretch")
        self.play(FadeIn(tp[0]), FadeIn(tj[0]), FadeIn(el), run_time=1.0)
        self.at("have several")
        self.play(Indicate(tp[0], color=TEAL), Indicate(tj[0], color=TEAL), run_time=0.9)
        gj = glow(loc(f, JAW))
        gp = glow(loc(f, PEL))
        wj = wire((4.3, 2.0), loc(f, JAW))
        wp = wire((1.3, 2.0), loc(f, PEL))
        wj.set_z_index(-1)
        wp.set_z_index(-1)
        self.at("serve the jaw")
        self.play(FadeIn(tj[1]), tj[0].animate.set_fill(TEAL, 0.8), Create(wj), FadeIn(gj, scale=0.3), run_time=1.2)
        bob(gj)
        self.at("another the pelvis")
        self.play(FadeIn(tp[1]), tp[0].animate.set_fill(TEAL, 0.8), Create(wp), FadeIn(gp, scale=0.3), run_time=1.2)
        bob(gp)
        self.at("jobs can overlap")
        self.play(Indicate(gj, color=WHITE), Indicate(gp, color=WHITE), Indicate(wj, color=WHITE), Indicate(wp, color=WHITE), run_time=1.6)
        self.finish()


class S09Insitu(SpokenScene):
    def construct(self):
        start(self)
        dish = RoundedRectangle(corner_radius=0.3, width=8.6, height=4.4, stroke_color=TEXT, stroke_width=3,
                                fill_color=TEXT, fill_opacity=0.1).move_to([-2.4, -0.5, 0])
        f = fish(ORANGE, (-1.9, -0.5), 1.7, "none")
        self.play(FadeIn(dish), run_time=0.7)
        self.play(FadeIn(f, shift=RIGHT * 0.5), run_time=1.0)
        bob(f)
        wave = lambda y, ph: ParametricFunction(lambda t: np.array([t, y + 0.16 * np.sin(5 * t + ph), 0]), t_range=[2.9, 6.3], stroke_width=6)
        rna = wave(2.7, 0).set_color(GOLD)
        probe = wave(2.35, 0).set_color(TEAL)
        rl = T("Pitx1 RNA", 34, GOLD).move_to([4.6, 3.35, 0])
        self.at("labeled probe")
        self.play(Create(rna), FadeIn(rl), run_time=1.0)
        probe.shift(DOWN * 0.9 + RIGHT * 1.5)
        pl = T("probe", 34, TEAL).move_to([4.6, 0.7, 0])
        self.play(Create(probe), FadeIn(pl), run_time=0.6)
        self.at("pairs with")
        self.play(probe.animate.shift(UP * 1.3 + LEFT * 1.5), pl.animate.move_to([4.6, 1.8, 0]), run_time=1.2)
        self.at("gold mark")
        self.play(Indicate(rna, color=WHITE), run_time=1.2)
        tag = T("in situ hybridization, Paxton larva (corrected 2006 figures)", 24, GREY).move_to([-1.5, -3.55, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.at("gold sits")
        st = Ellipse(width=1.5, height=1.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to(loc(f, (1.35, -0.2)))
        mouth = T("mouth and\nlower jaw", 34, GOLD).move_to([4.6, -0.8, 0])
        self.play(GrowFromCenter(st), FadeIn(mouth), run_time=1.6)
        bob(st)
        ds = DashedVMobject(Circle(radius=0.5, color=TEXT, stroke_width=5)).move_to(loc(f, PEL))
        pl2 = T("where the pelvis forms", 32, TEXT).move_to([-1.7, -2.95, 0])
        self.at("where the pelvis")
        self.play(Create(ds), FadeIn(pl2), run_time=1.2)
        self.at("none")
        self.play(Indicate(ds, color=WHITE), run_time=1.0)
        self.finish()


class S10Meaning(SpokenScene):
    def construct(self):
        start(self)
        div = DashedLine([0, 3.9, 0], [0, -3.7, 0], color=GREY, stroke_width=2)
        yd = 2.0
        lo = Line([-6.5, yd, 0], [-0.4, yd, 0], color=DNA_C, stroke_width=10)
        lb = Line([0.4, yd, 0], [6.5, yd, 0], color=DNA_C, stroke_width=10)
        opj = tab("jaw switch", -2.1, yd)
        opp = tab("pelvic switch", -5.15, yd)
        bpj = tab("jaw switch", 4.9, yd)
        bpp = tab("pelvic switch", 1.8, yd)
        for tb in (opj, opp, bpj, bpp):
            tb[0].set_fill(TEAL, 0.8)
        fo = fish(ORANGE, (-3.4, -1.1), 1.0, "full")
        fb = fish(BLUE, (3.4, -1.1), 1.0, "full")
        self.play(FadeIn(div), Create(lo), Create(lb), FadeIn(opj), FadeIn(opp), FadeIn(bpj), FadeIn(bpp), FadeIn(fo), FadeIn(fb), run_time=0.7)
        bob(fo)
        bob(fb)
        hy = T("hypothesis", 36, YELLOW).move_to([0, 3.45, 0])
        self.at("suppose")
        self.play(FadeIn(hy), run_time=0.6)
        gjo, gjb = glow(loc(fo, (1.4, -0.2)), 0.25), glow(loc(fb, (1.4, -0.2)), 0.25)
        wjo = wire((-2.1, yd - 0.1), loc(fo, (1.4, -0.2)))
        wjb = wire((4.9, yd - 0.1), loc(fb, (1.4, -0.2)))
        self.at("jaw switch")
        self.play(Create(wjo), Create(wjb), run_time=0.8)
        self.play(FadeIn(gjo, scale=0.3), FadeIn(gjb, scale=0.3), run_time=0.6)
        bob(gjo)
        bob(gjb)
        gpb = glow(loc(fb, PEL), 0.25)
        wpb = wire((1.8, yd - 0.1), loc(fb, PEL))
        self.at("pelvic switch")
        flat = tab("pelvic switch", -5.15, yd, up=False)
        flat[0].stretch_to_fit_height(0.2).move_to([-5.15, yd + 0.2, 0])
        flat[0].set_stroke(RED, 3)
        crack = Line([-5.8, yd + 0.9, 0], [-4.5, yd + 0.2, 0], color=RED, stroke_width=6)
        self.play(Create(crack), run_time=0.5)
        self.play(Transform(opp[0], flat[0]), FadeOut(opp[1]), FadeOut(crack), Create(wpb), run_time=1.0)
        self.play(FadeIn(gpb, scale=0.3), run_time=0.6)
        bob(gpb)
        self.at("that body part")
        st = fo.pel
        self.play(*[m.animate.scale(0.1, about_point=m.get_top()) for m in st], run_time=2.0)
        self.at("other jobs")
        self.play(Indicate(gjo, color=WHITE, scale_factor=1.6), Indicate(gjb, color=WHITE, scale_factor=1.6), run_time=1.5)
        self.finish()


class S10bCompare(SpokenScene):
    def construct(self):
        start(self)
        fb = fish(BLUE, (-3.4, 2.1), 1.2, "full")
        fo = fish(ORANGE, (3.4, 2.1), 1.2, "stub")
        self.play(FadeIn(fb), FadeIn(fo), run_time=1.0)
        bob(fb)
        bob(fo)
        rows = [("same Pitx1 protein", -0.7), ("used in the jaw", -1.7), ("used in the pelvis", -2.7)]
        txt = [T(r, 34, TEXT).move_to([0, y, 0]) for r, y in rows]
        self.at("make the same")
        self.play(FadeIn(txt[0]), run_time=0.6)
        self.play(Create(tickm((-3.4, -0.7))), Create(tickm((3.4, -0.7))), run_time=0.8)
        gb, go = glow(loc(fb, JAW), 0.22), glow(loc(fo, JAW), 0.22)
        self.at("use it")
        self.play(FadeIn(txt[1]), run_time=0.6)
        self.play(Create(tickm((-3.4, -1.7))), Create(tickm((3.4, -1.7))), FadeIn(gb, scale=0.3), FadeIn(go, scale=0.3), run_time=0.9)
        bob(gb)
        bob(go)
        gpb = glow(loc(fb, PEL), 0.22)
        self.at("only the pelvic")
        self.play(FadeIn(txt[2]), run_time=0.6)
        box = Square(0.45, stroke_color=RED, stroke_width=4).move_to([3.4, -2.7, 0])
        self.play(Create(tickm((-3.4, -2.7))), FadeIn(gpb, scale=0.3), Create(box), FadeOut(fo.pel), run_time=1.0)
        bob(gpb)
        self.at("jaw use")
        self.play(Indicate(txt[1], color=GOLD), Indicate(gb, color=WHITE), Indicate(go, color=WHITE), run_time=1.4)
        foot = T("tissues compared: jaw and pelvis", 26, GREY).move_to([0, -3.55, 0])
        self.at("other tissues")
        self.play(FadeIn(foot), run_time=0.8)
        self.finish()


class S11Scope(SpokenScene):
    def construct(self):
        start(self)
        fb = fish(BLUE, (-3.4, 2.5), 1.0, "full")
        fo = fish(ORANGE, (3.4, 2.5), 1.0, "stub")
        gb, go, gpb = glow(loc(fb, JAW), 0.22), glow(loc(fo, JAW), 0.22), glow(loc(fb, PEL), 0.22)
        self.add(fb, fo, gb, go, gpb)
        for m in (fb, fo, gb, go, gpb):
            bob(m)
        tg = tab("pelvic switch", 0, 0.1, w=3.4)
        self.at("best studied")
        self.play(FadeIn(tg), run_time=0.8)
        tag = T("best-studied route, not the only one", 32, TEXT).move_to([0, -3.5, 0])
        self.at("not the only")
        self.play(FadeIn(tag), run_time=0.8)
        crack = Line([-0.6, 1.2, 0], [0.5, 0.45, 0], color=RED, stroke_width=7)
        self.at("missing gold mark")
        self.play(Create(crack), Indicate(tg, color=RED), run_time=1.4)
        a = T("the Pitx1 copy's\nown DNA?", 34, TEXT, line_spacing=0.9).move_to([-3.7, -1.9, 0])
        b = T("another gene that\nsupplies its regulators?", 34, TEXT, line_spacing=0.9).move_to([3.4, -1.9, 0])
        ba = SurroundingRectangle(a, color=TEXT, buff=0.2, corner_radius=0.12)
        bb = SurroundingRectangle(b, color=TEXT, buff=0.2, corner_radius=0.12)
        ar1 = Arrow([-0.7, 0.0, 0], [-3.3, -0.95, 0], color=YELLOW, buff=0.05)
        ar2 = Arrow([0.7, 0.0, 0], [3.2, -0.95, 0], color=YELLOW, buff=0.05)
        self.at("own dna")
        self.play(GrowArrow(ar1), FadeIn(a), Create(ba), run_time=1.2)
        self.at("another gene")
        self.play(GrowArrow(ar2), FadeIn(b), Create(bb), run_time=1.2)
        pulse(ar1, 0.05)
        pulse(ar2, 0.05)
        self.finish()


class S12End(EndCard):
    LINE = "Evolution changed where Pitx1 is used, not what it makes."
