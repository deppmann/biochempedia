"""Cochlear amplifier film: what a returning sound, a capacitance bell and a structure can and cannot show.

COLOR MAP (one colour per concept, whole film)
  BLUE   = the outer hair cell and prestin in its extended state (the subject)
  GREEN  = the contracted state and the capacitance it produces (the output we read)
  YELLOW = voltage and the stimulus impulse (the thing that moves)
  TEAL   = the sound that returns from the ear
  GREY   = structure, labels, things not measured
  RED    = crossed out / not shown by that measurement
"""
import numpy as np
from bp_style import *

VH, Z, KTE = -112.0, 0.70, 25.42


def occ(v, z=Z):
    return 1.0 / (1.0 + np.exp(-z * (v - VH) / KTE))


def nlc(v):
    f = occ(v)
    return 4 * f * (1 - f)


def mkaxes(w, h, xr, yr):
    return Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1], x_length=w, y_length=h, tips=False,
                axis_config={"color": GREY, "include_ticks": False, "stroke_width": 2.5})


def curve(ax, fn, xr, color, step=0.5, w=5):
    xs = np.arange(xr[0], xr[1] + 1e-9, step)
    pts = [ax.c2p(x, fn(x)) for x in xs]
    m = VMobject(color=color, stroke_width=w)
    m.set_points_as_corners(pts)
    return m


def bell_axes(w, h, cx, cy):
    ax = mkaxes(w, h, (-220, -20), (0, 1.15)).move_to([cx, cy, 0])
    return ax


def pulse(color=YELLOW, r=0.13):
    return Dot(radius=r, color=color)


# ------------------------------------------------------------------ title
class S00Title(TitleCard):
    LESSON = "The Cochlear Amplifier and Otoacoustic Emissions"
    TITLE = "What the returning sound leaves out"


# ------------------------------------------------------------------ 1 echo
class S01Echo(SpokenScene):
    def construct(self):
        y0 = 0.5
        yf = 2.55
        mic = chip("microphone", GREY, size=24)
        mic.move_to([-5.0, y0, 0])
        canal = Rectangle(width=4.6, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.08).move_to([-1.6, y0, 0])
        canal_l = T("closed ear canal", 22, GREY).next_to(canal, DOWN, buff=0.15)
        cochlea = chip("cochlea", BLUE, size=26).move_to([2.3, y0, 0])

        self.at("microphone sealed")
        self.play(FadeIn(mic), Create(canal), FadeIn(canal_l), run_time=0.9)
        self.at("the cochlea made")
        self.play(FadeIn(cochlea), run_time=0.6)
        d = pulse(TEAL).move_to(cochlea.get_left() + LEFT * 0.1)
        self.play(FadeIn(d), run_time=0.2)
        self.play(d.animate.move_to(mic.get_right() + RIGHT * 0.15), run_time=1.0)
        ret = T("returning sound", 22, TEAL).next_to(canal, UP, buff=0.15)
        self.play(FadeIn(ret), FadeOut(d), run_time=0.5)

        # plots
        def trace(tail):
            ax = mkaxes(5.3, 2.2, (0, 30), (-1.2, 1.2))
            ts = np.arange(0, 30.001, 0.04)
            pts = []
            for t in ts:
                if t < 4.0:
                    y = 0.95 * np.exp(-t / 1.1) * np.cos(2 * np.pi * 0.9 * t)
                elif t < 5.0:
                    y = 0.0
                else:
                    y = tail * np.exp(-(t - 5.0) / 14.0) * np.cos(2 * np.pi * 0.6 * (t - 5.0))
                pts.append([t, y])
            return ax, pts

        axn, ptn = trace(0.55)
        axn.move_to([-3.4, -0.55, 0])
        trn = VMobject(color=TEAL, stroke_width=3.5)
        trn.set_points_as_corners([axn.c2p(*p) for p in ptn])
        n5 = DashedLine(axn.c2p(5, -1.2), axn.c2p(5, 1.2), color=YELLOW, stroke_width=2.5)
        n5l = T("5 ms", 22, YELLOW).next_to(axn.c2p(5, -1.2), DOWN, buff=0.12)
        n0l = T("0", 22, GREY).next_to(axn.c2p(0, -1.2), DOWN, buff=0.12)
        titn = T("normal ears", 24, TEXT).next_to(axn, UP, buff=0.12)

        axd, ptd = trace(0.0)
        axd.move_to([3.4, -0.55, 0])
        trd = VMobject(color=TEAL, stroke_width=3.5)
        trd.set_points_as_corners([axd.c2p(*p) for p in ptd])
        d5 = DashedLine(axd.c2p(5, -1.2), axd.c2p(5, 1.2), color=YELLOW, stroke_width=2.5)
        d5l = T("5 ms", 22, YELLOW).next_to(axd.c2p(5, -1.2), DOWN, buff=0.12)
        d0l = T("0", 22, GREY).next_to(axd.c2p(0, -1.2), DOWN, buff=0.12)
        titd = T("ears with cochlear deafness", 24, TEXT).next_to(axd, UP, buff=0.12)
        sk = T("in this sketch", 22, GREY).move_to([0, -3.3, 0])

        self.at("brief impulses")
        self.play(FadeOut(ret), VGroup(mic, canal, canal_l, cochlea).animate.shift(UP * (yf - y0)), run_time=0.7)
        imp = pulse(YELLOW).move_to(mic.get_right() + RIGHT * 0.15)
        impl = T("brief impulse", 22, YELLOW).next_to(canal, UP, buff=0.15)
        self.play(FadeIn(imp), FadeIn(impl), run_time=0.3)
        self.play(imp.animate.move_to(cochlea.get_left() + LEFT * 0.1), run_time=0.9)
        self.play(FadeOut(imp), FadeIn(VGroup(axn, titn, n0l, sk)), run_time=0.6)
        initial = VMobject(color=YELLOW, stroke_width=3.5)
        initial.set_points_as_corners([axn.c2p(*p) for p in ptn if p[0] < 4.0])
        self.play(Create(initial), FadeOut(impl), run_time=0.8)
        self.at("slowly decaying")
        tailpts = [axn.c2p(*p) for p in ptn if p[0] >= 5.0]
        tail = VMobject(color=TEAL, stroke_width=3.5)
        tail.set_points_as_corners(tailpts)
        self.play(FadeIn(VGroup(n5, n5l)), run_time=0.4)
        self.play(Create(tail), run_time=2.0)
        self.at("in the ears")
        self.play(FadeIn(VGroup(axd, titd, d0l)), run_time=0.5)
        initd = VMobject(color=YELLOW, stroke_width=3.5)
        initd.set_points_as_corners([axd.c2p(*p) for p in ptd if p[0] < 4.0])
        flat = Line(axd.c2p(5, 0), axd.c2p(30, 0), color=TEAL, stroke_width=3.5)
        self.play(Create(initd), FadeIn(VGroup(d5, d5l)), run_time=0.8)
        self.at("it was absent")
        self.play(Create(flat), run_time=0.8)
        self.at("that supports")
        box = SurroundingRectangle(cochlea, color=TEAL, buff=0.1, stroke_width=4)
        src = T("source", 22, TEAL).next_to(cochlea, UP, buff=0.3)
        self.play(Create(box), FadeIn(src), run_time=0.6)
        self.at("identify a motor")
        mot = chip("motor?", GREY, size=26).move_to([5.2, yf, 0])
        ln = DashedLine(cochlea.get_right(), mot.get_left(), color=GREY)
        self.play(FadeIn(ln), FadeIn(mot), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ 2 fast
class S02Fast(SpokenScene):
    def construct(self):
        u = ValueTracker(0.0)
        bottom = -2.1
        cx = -3.0

        def cell():
            h = 4.1 - 1.0 * u.get_value()
            c = RoundedRectangle(corner_radius=0.6, width=1.4, height=h, stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.22)
            c.move_to([cx, bottom + h / 2, 0])
            return c

        cellm = always_redraw(cell)
        cl = T("outer hair cell", 24, BLUE).move_to([cx, 2.75, 0])
        mx = -1.1
        meter = Line([mx, bottom, 0], [mx, 1.7, 0], color=GREY, stroke_width=4)
        mk = always_redraw(lambda: Triangle(color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.17)
                           .rotate(PI / 2 * 3).move_to([mx - 0.22, bottom + 0.1 + 3.4 * u.get_value(), 0]))
        vl = T("voltage", 24, YELLOW).move_to([mx + 0.15, 2.2, 0])
        top_l = T("more positive", 22, GREY).next_to(meter, RIGHT, buff=0.2).align_to(meter, UP)
        self.at("shorten and lengthen")
        self.play(FadeIn(cellm), FadeIn(cl), Create(meter), FadeIn(mk), FadeIn(vl), run_time=0.8)
        self.play(u.animate.set_value(1.0), run_time=1.0)
        self.play(u.animate.set_value(0.0), run_time=1.0)
        self.add(top_l)
        self.at("is the motor")
        base = Line([cx, bottom - 0.05, 0], [cx, bottom - 0.5, 0], color=GREY)
        pc = chip("prestin", BLUE, size=26).move_to([cx, bottom - 0.9, 0])
        self.play(FadeIn(base), FadeIn(pc), run_time=0.6)
        self.play(u.animate.set_value(1.0), run_time=0.5)
        self.play(u.animate.set_value(0.0), run_time=0.5)
        self.at("think about speed")
        # tone: one cycle
        ax = mkaxes(4.9, 1.8, (0, 3), (-1.3, 1.3)).move_to([3.75, 2.1, 0])
        wv = ax.plot(lambda x: np.sin(2 * PI * x), x_range=[0, 3, 0.02], color=YELLOW, stroke_width=4)
        tl = T("tone at 20 kHz", 24, YELLOW).next_to(ax, UP, buff=0.1)
        self.play(FadeIn(tl), Create(ax), run_time=0.5)
        self.at("completes a cycle")
        self.play(Create(wv), run_time=1.2)
        br = BraceBetweenPoints(ax.c2p(0, -1.3), ax.c2p(1, -1.3), direction=DOWN, color=WHITE)
        brl = T("one cycle = 50 µs", 24, TEXT).next_to(br, DOWN, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.6)
        self.at("Preston responds")
        chem = chip("ATP hydrolysis", GREY, size=24).move_to([3.75, -0.3, 0])
        self.play(FadeIn(chem), run_time=0.5)
        cross = Cross(chem, stroke_color=RED, stroke_width=4)
        self.at("without burning")
        self.play(Create(cross), run_time=0.5)
        self.at("Membrane filtering")
        link = Line([mx - 0.25, bottom - 0.9, 0], pc.get_right(), color=YELLOW, stroke_width=5)
        link2 = Line([mx, bottom, 0], [mx, bottom - 0.9, 0], color=YELLOW, stroke_width=5)
        res = T("responds to voltage directly", 24, YELLOW).move_to([2.3, -3.0, 0])
        self.play(Create(link2), Create(link), FadeIn(res), run_time=0.6)
        self.play(u.animate.set_value(1.0), run_time=0.6)
        self.play(u.animate.set_value(0.0), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ 3 bell
class S03Bell(SpokenScene):
    def construct(self):
        # left: cell with prestin in the membrane, voltage clamp
        cell = RoundedRectangle(corner_radius=0.5, width=3.6, height=3.4, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.12).move_to([-4.2, 1.1, 0])
        cl = T("cell with prestin", 24, BLUE).move_to(cell)
        pip = Line([-1.4, 3.35, 0], [-2.9, 2.5, 0], color=YELLOW, stroke_width=5)
        pl = T("voltage clamp", 24, YELLOW).next_to(pip.get_start(), LEFT, buff=0.15).shift(UP * 0.25)
        mem = Rectangle(width=3.8, height=0.3, stroke_color=GREY, fill_color=GREY, fill_opacity=0.45,
                        stroke_width=2).move_to([-4.2, -0.6, 0])
        pr = RoundedRectangle(corner_radius=0.15, width=0.8, height=1.0, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.3).move_to([-4.2, -0.6, 0])
        ml = T("membrane", 22, GREY).next_to(mem, DOWN, buff=0.45).shift(LEFT * 1.0)
        prl = T("prestin", 22, BLUE).next_to(mem, DOWN, buff=0.45).shift(RIGHT * 0.9)
        # right: bell axes
        ax = mkaxes(6.2, 4.0, (-220, -20), (0, 1.15)).move_to([3.0, 0.4, 0])
        xl = T("membrane voltage", 24, YELLOW).next_to(ax, DOWN, buff=0.2)
        yl = T("capacitance, two-state model", 24, GREEN).next_to(ax, UP, buff=0.3).align_to(ax, LEFT)
        bell = curve(ax, nlc, (-220, -20), GREEN, 1.0, 6)

        self.at("how do you connect")
        self.play(FadeIn(cell), FadeIn(cl), run_time=0.5)
        self.play(Create(pip), FadeIn(pl), run_time=0.5)
        self.play(FadeIn(mem), FadeIn(pr), FadeIn(ml), FadeIn(prl), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.at("bell shaped")
        vt = ValueTracker(-215)
        dot = always_redraw(lambda: Dot(ax.c2p(vt.get_value(), nlc(vt.get_value())), radius=0.12, color=YELLOW))
        self.add(dot)
        self.play(Create(bell), vt.animate.set_value(-25), run_time=1.7, rate_func=linear)
        self.remove(dot)
        self.at("peaks at one")
        pk = DashedLine(ax.c2p(VH, 0), ax.c2p(VH, 1.0), color=GREY, stroke_width=3)
        pd = Dot(ax.c2p(VH, 1.0), radius=0.14, color=YELLOW)
        pkl = T("peak", 24, GREEN).next_to(pd, UP, buff=0.1)
        self.play(Create(pk), FadeIn(pd), FadeIn(pkl), run_time=0.6)
        self.at("movement of charge")
        q = Dot(radius=0.13, color=YELLOW).move_to(pr.get_center() + UP * 0.3)
        self.play(FadeIn(q), run_time=0.3)
        self.play(q.animate.move_to(pr.get_center() + DOWN * 0.3), run_time=0.8)
        self.play(q.animate.move_to(pr.get_center() + UP * 0.3), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 4 two states
class S04Twostate(SpokenScene):
    def construct(self):
        # left: two states and occupancy bar
        ext = chip("extended", BLUE, size=26).move_to([-5.1, 2.3, 0])
        con = chip("contracted", GREEN, size=26).move_to([-1.3, 2.3, 0])
        self.at("two states")
        self.play(FadeIn(ext), FadeIn(con), run_time=0.7)
        self.at("toward a contracted")
        arr = Arrow(ext.get_right(), con.get_left(), buff=0.1, color=YELLOW, stroke_width=5)
        dep = T("depolarization", 24, YELLOW).move_to([-3.2, 3.1, 0])
        self.play(GrowArrow(arr), FadeIn(dep), run_time=0.7)

        # occupancy bar
        W = 4.4
        f = ValueTracker(0.0)
        bx = -3.15

        def bar():
            fv = f.get_value()
            g = VGroup()
            gl = Rectangle(width=max(W * fv, 0.001), height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            bl = Rectangle(width=max(W * (1 - fv), 0.001), height=0.5, stroke_width=0, fill_color=BLUE,
                           fill_opacity=0.6)
            gl.move_to([bx - W / 2 + W * fv / 2, 1.1, 0])
            bl.move_to([bx + W / 2 - W * (1 - fv) / 2, 1.1, 0])
            return VGroup(bl, gl)

        barm = always_redraw(bar)
        outline = Rectangle(width=W, height=0.5, stroke_color=GREY, stroke_width=2.5).move_to([bx, 1.1, 0])
        barl = T("share of prestin in each state", 22, GREY).next_to(outline, UP, buff=0.12)
        
        # right: stacked plots
        axf = mkaxes(5.6, 2.3, (-220, -20), (0, 1.1)).move_to([3.4, 1.35, 0])
        axb = mkaxes(5.6, 2.3, (-220, -20), (0, 1.15)).move_to([3.4, -1.75, 0])
        tf = T("occupancy f of the contracted state", 22, GREEN).next_to(axf, UP, buff=0.1)
        tb = T("normalized capacitance", 22, GREEN).next_to(axb, UP, buff=0.1)
        cf = curve(axf, occ, (-220, -20), GREEN, 1.0, 5)
        cb = curve(axb, nlc, (-220, -20), GREEN, 1.0, 5)
        self.at("and colleagues fitted")
        self.add(barm, outline)
        self.play(FadeIn(barl), Create(axf), Create(axb), FadeIn(tf), FadeIn(tb), run_time=0.8)
        self.play(Create(cf), Create(cb), run_time=1.5)
        gerbil = T("gerbil prestin, cell line", 22, GREY).move_to([-3.15, -0.2, 0])
        self.play(FadeIn(gerbil), run_time=0.4)
        self.at("effective charge")
        par = M("Vh = −112 mV   z = 0.70", 24, YELLOW).move_to([-3.15, -0.9, 0])
        self.play(FadeIn(par), run_time=0.6)

        vx = ValueTracker(VH)
        vline = always_redraw(lambda: VGroup(
            DashedLine(axf.c2p(vx.get_value(), 0), axf.c2p(vx.get_value(), 1.1), color=YELLOW, stroke_width=2.5),
            DashedLine(axb.c2p(vx.get_value(), 0), axb.c2p(vx.get_value(), 1.15), color=YELLOW, stroke_width=2.5),
            Dot(axf.c2p(vx.get_value(), occ(vx.get_value())), radius=0.1, color=YELLOW),
            Dot(axb.c2p(vx.get_value(), nlc(vx.get_value())), radius=0.1, color=YELLOW)))
        r1 = M("f = 0.5   capacitance = 1 (peak)", 22, GREEN).move_to([-3.15, -1.9, 0])
        self.at("half the protein")
        self.play(FadeIn(vline), f.animate.set_value(0.5), FadeIn(r1), run_time=0.9)
        xl1 = M("−112 mV", 22, YELLOW).next_to(axb.c2p(VH, 0), DOWN, buff=0.12).shift(LEFT * 0.45)
        self.add(xl1)
        self.at("more positive")
        r2 = M("f = 0.798   capacitance = 0.644", 22, GREEN).move_to([-3.15, -2.5, 0])
        xl2 = M("−62 mV", 22, YELLOW).next_to(axb.c2p(-62, 0), DOWN, buff=0.12).shift(RIGHT * 0.45)
        self.play(vx.animate.set_value(-62), f.animate.set_value(occ(-62)), FadeIn(xl2), run_time=1.2)
        self.at("occupancy rises")
        self.play(FadeIn(r2), run_time=0.5)
        self.at("falls to about")
        pct = T("about 64% of the peak", 24, TEXT).move_to([-3.15, -3.15, 0])
        self.play(FadeIn(pct), Indicate(r2, color=GREEN), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ 5 limits
class S05Limits(SpokenScene):
    def construct(self):
        # left: charge movement and force unknown
        ax = mkaxes(4.4, 2.0, (-220, -20), (0, 1.15)).move_to([-3.9, 1.6, 0])
        bell = curve(ax, nlc, (-220, -20), GREEN, 1.0, 5)
        t1 = T("charge movement in a cell line", 22, GREEN).next_to(ax, UP, buff=0.12)
        self.at("charge movement")
        self.play(Create(ax), Create(bell), FadeIn(t1), run_time=1.0)
        fp = chip("force, power of a hair cell", GREY, size=24).move_to([-3.9, -1.0, 0])
        q = T("not read out", 24, RED).next_to(fp, DOWN, buff=0.2)
        self.at("how much force")
        self.play(FadeIn(fp), run_time=0.5)
        self.play(FadeIn(q), Create(DashedLine(ax.get_bottom() + DOWN * 0.2, fp.get_top(), color=GREY)),
                  run_time=0.6)

        # right: two purified protein schematics
        self.at("purified protein")
        pt = T("purified protein in chosen conditions", 22, GREY).move_to([3.0, 3.35, 0])

        def membrane_with(width, y, color, name):
            mem = Rectangle(width=4.6, height=0.28, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
            blob = RoundedRectangle(corner_radius=0.2, width=width, height=1.1, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=0.28)
            lab = T(name, 24, color)
            g = VGroup(mem, blob).move_to([3.0, y, 0])
            lab.next_to(g, RIGHT, buff=0.0)
            return g, lab

        gc, gcl = membrane_with(1.5, 2.2, BLUE, "")
        gs, gsl = membrane_with(1.5, 0.0, GREEN, "")
        lc = T("chloride", 24, BLUE).move_to([1.45, 1.75, 0])
        ls = T("salicylate", 24, GREEN).move_to([1.45, -0.45, 0])
        self.play(FadeIn(pt), FadeIn(gc), FadeIn(lc), FadeIn(gs), FadeIn(ls), run_time=0.9)
        self.at("differ by about")
        arr = DoubleArrow([2.5, 1.65, 0], [2.5, 0.75, 0], color=YELLOW, buff=0, stroke_width=5, tip_length=0.15)
        lab = VGroup(T("mean transmembrane area", 22, YELLOW), T("differs by about 200 Å²", 22, YELLOW)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        lab.move_to([2.8 + lab.width / 2, 1.2, 0])
        sch = T("schematic, not to scale", 22, GREY).move_to([3.0, -0.95, 0])
        self.play(GrowFromCenter(arr), FadeIn(lab), FadeIn(sch), run_time=0.9)
        self.at("compares two structures")
        cmp_ = T("two structures compared", 24, TEXT).move_to([3.0, -1.65, 0])
        self.play(FadeIn(cmp_), run_time=0.5)
        self.at("not a stroke")
        st = chip("stroke measured in a hair cell", GREY, size=24).move_to([3.0, -2.55, 0])
        self.play(FadeIn(st), run_time=0.4)
        self.play(Create(Cross(st, stroke_color=RED, stroke_width=6)), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ 6 rule
class S06Rule(SpokenScene):
    def construct(self):
        def icon_sound():
            ax = mkaxes(2.0, 1.0, (0, 30), (-1.2, 1.2))
            ts = np.arange(5, 30.01, 0.1)
            m = VMobject(color=TEAL, stroke_width=3.5)
            m.set_points_as_corners([ax.c2p(t, 0.9 * np.exp(-(t - 5) / 14) * np.cos(2 * np.pi * 0.6 * (t - 5)))
                                     for t in ts])
            return VGroup(ax, m)

        def icon_bell():
            ax = mkaxes(2.0, 1.0, (-220, -20), (0, 1.15))
            return VGroup(ax, curve(ax, nlc, (-220, -20), GREEN, 2.0, 4))

        def icon_struct():
            mem = Rectangle(width=2.0, height=0.2, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
            b = RoundedRectangle(corner_radius=0.15, width=0.8, height=0.8, stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.28)
            return VGroup(mem, b).move_to(ORIGIN)

        cols = []
        for x, ic, head, col, claim in [
            (-4.2, icon_sound(), "returning sound", TEAL, "supports a cochlear source"),
            (0.0, icon_bell(), "capacitance curve", GREEN, "reports charge movement"),
            (4.2, icon_struct(), "structures", BLUE, "show chosen preparation conditions"),
        ]:
            box = RoundedRectangle(corner_radius=0.2, width=3.8, height=4.0, stroke_color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.07).move_to([x, 0.2, 0])
            h = T(head, 26, col).move_to([x, 1.65, 0])
            ic.move_to([x, 0.4, 0])
            c1 = T(claim, 22, TEXT)
            fit(c1, max_w=3.4)
            c1.move_to([x, -1.2, 0])
            cols.append((box, h, ic, c1))

        self.at("different preparation")
        self.play(*[FadeIn(VGroup(c[0])) for c in cols], run_time=0.8)
        self.at("returning sound")
        self.play(FadeIn(cols[0][1]), FadeIn(cols[0][2]), run_time=0.5)
        self.play(FadeIn(cols[0][3]), run_time=0.5)
        self.at("capacitance curve")
        self.play(FadeIn(cols[1][1]), FadeIn(cols[1][2]), run_time=0.5)
        self.play(FadeIn(cols[1][3]), run_time=0.5)
        self.at("the structures")
        self.play(FadeIn(cols[2][1]), FadeIn(cols[2][2]), run_time=0.5)
        self.play(FadeIn(cols[2][3]), run_time=0.5)
        self.at("complementary views")
        line = T("complementary views, not one settled movie", 28, GOLD).move_to([0, -2.95, 0])
        self.play(FadeIn(line), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Read them as complementary views, not one settled movie."
