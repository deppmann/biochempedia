"""Semaphorins and repulsion: neuropilin catches, plexin signals  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  TEAL   = the growth cone and its axon
  YELLOW = Sema3A (and the brain membranes that carry it)
  BLUE   = neuropilin
  PURPLE = plexin (and its inner GAP part)
  ORANGE = R-Ras and the integrin adhesion it holds
  GOLD   = the GTP badge
  GREEN  = a response that happens
  RED    = a response that is blocked / switched off / lost
  GREY   = membranes, outlines, labels, the unknown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------
def fan_pts(a0, a1, r, c, n=11):
    c = np.array(c, float)
    pts = [c + np.array([0, 0.28, 0])]
    for a in np.linspace(a1, a0, n):
        pts.append(c + r * np.array([np.cos(a), np.sin(a), 0]))
    pts.append(c + np.array([0, -0.28, 0]))
    return pts


def fan(a0, a1, r, c):
    return Polygon(*fan_pts(a0, a1, r, c), color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25)


def filopodia(a0, a1, r, c, k=7):
    c = np.array(c, float)
    g = VGroup()
    for a in np.linspace(a0 + 0.05, a1 - 0.05, k):
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(c + r * d, c + (r + 0.5) * d, color=TEAL, stroke_width=3))
    return g


def shaft(c, x0=-6.3):
    return Rectangle(width=c[0] - x0, height=0.56, stroke_width=0, fill_color=TEAL,
                     fill_opacity=0.25).move_to([(c[0] + x0) / 2, c[1], 0])


def dots(points, color=YELLOW, r=0.13):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([p[0], p[1], 0]) for p in points])


def mem_bar(y, x0=-6.3, x1=6.3, h=0.34):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def rr(w, h, color, op=0.3, sw=3.5, r=0.18):
    return RoundedRectangle(corner_radius=min(r, w / 2.2, h / 2.2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=op)


def sema(x, y, w=1.3, h=0.55):
    e = Ellipse(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    return e.move_to([x, y, 0])


def semag(x, y, w=1.3, h=0.55, size=24):
    e = sema(x, y, w, h)
    t = T("Sema3A", size, BG).move_to(e)
    return VGroup(e, t)


class Rec(VGroup):
    """A receptor drawn as shapes: body outside, neck through the membrane, tail inside.
    parts: body (with label), neck, tail."""

    def __init__(self, name, color, x, ym=0.0, s=1.0, body_h=1.7, tail_h=0.38, tail_w=0.26):
        super().__init__()
        bw = 1.6 * s
        bh = body_h * s
        self.body = rr(bw, bh, color).move_to([x, ym + 0.17 + bh / 2, 0])
        self.lab = T(name, int(round(22 * max(1.0, s))), color).move_to(self.body)
        self.neck = Rectangle(width=0.3 * s, height=0.34, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, ym, 0])
        th = tail_h * s
        self.tail = rr(tail_w * s, th, color, op=0.5, sw=3, r=0.06).move_to([x, ym - 0.17 - th / 2, 0])
        self.add(self.body, self.lab, self.neck, self.tail)
        self.x, self.ym, self.s, self.color = x, ym, s, color

    def top(self):
        return self.body.get_top()[1]


def lab(text, size=26, color=GREY, **kw):
    return T(text, size, color, **kw)


def qbox(w=1.1, h=1.1, color=GREY):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3.5), num_dashes=24)
    q = T("?", 44, color, weight=BOLD)
    return VGroup(box, q)


class S00Title(TitleCard):
    LESSON = "Semaphorins and Repulsion"
    TITLE = "Neuropilin catches, plexin signals"


# ------------------------------------------------------------------------------------------
class S01Collapse(SpokenScene):
    def construct(self):
        c = np.array([-3.0, 0.0, 0.0])
        R = 3.0
        sh = shaft(c)
        fn = fan(-0.85, 0.85, R, c)
        fo = filopodia(-0.85, 0.85, R, c)
        gc = T("growth cone", 28, TEAL).move_to([-3.0, -2.95, 0])
        ax = T("axon", 26, TEAL).move_to([-5.0, 0.75, 0])
        self.at("A growth cone")
        self.play(FadeIn(sh), run_time=0.4)
        self.play(FadeIn(fn), FadeIn(fo), FadeIn(gc), FadeIn(ax), run_time=0.7)
        # yellow dots (brain membranes) approach
        pts = [(4.4, 0.5), (5.0, 0.0), (4.4, -0.5), (3.8, 0.0), (4.9, 0.8), (4.9, -0.8), (3.9, 0.7), (3.9, -0.7)]
        dd = dots(pts)
        dl = T("brain membranes", 26, YELLOW).move_to([4.4, 1.6, 0])
        self.at("Add brain membranes")
        self.play(FadeIn(dd, shift=LEFT * 0.4), FadeIn(dl), run_time=0.7)
        self.at("the fan folds")
        # tight cluster near the tip, fan folds
        pts2 = [(x - 1.7, y) for x, y in pts]
        thin = fan(-0.07, 0.07, R * 0.62, c)
        self.play(dd.animate.move_to(dd.get_center() + LEFT * 1.7), dl.animate.shift(LEFT * 1.7),
                  ReplacementTransform(fn, thin), FadeOut(fo), run_time=1.3)
        self.at("named collapsin")
        l2 = T("collapsin", 28, YELLOW).move_to(dl)
        self.play(FadeTransform(dl, l2), run_time=0.5)
        self.at("Today it is called")
        l3 = T("Sema3A", 28, YELLOW).move_to(l2)
        self.play(FadeTransform(l2, l3), run_time=0.5)
        self.at("about 10 picomolar")
        pm = T("about 10 picomolar", 26, GREY).next_to(dd, DOWN, buff=0.4)
        self.play(FadeIn(pm, shift=UP * 0.1), run_time=0.5)
        self.at("What does the growth cone use")
        q = qbox().move_to([0.3, 0.0, 0])
        ql = T("what hears it?", 26, TEXT).next_to(q, UP, buff=0.3)
        self.play(FadeIn(q, scale=0.9), FadeIn(ql), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
class S02Neuropilin(SpokenScene):
    def construct(self):
        mem = mem_bar(0.0)
        np_ = Rec("neuropilin", BLUE, 0.0, 0.0, s=1.3)
        sm = sema(4.5, 2.95, w=1.8, h=0.7)
        sm_l = T("Sema3A", 26, YELLOW).move_to(sm)
        sm_l.set_color(BG)
        sg = VGroup(sm, sm_l)
        self.at("is a secreted")
        self.play(FadeIn(mem), FadeIn(sg, shift=LEFT * 0.3), run_time=0.7)
        self.at("receptor")
        self.play(FadeIn(np_.body), FadeIn(np_.lab), FadeIn(np_.neck), FadeIn(np_.tail), run_time=0.8)
        self.at("It is called neuropilin")
        dock = sg.copy().move_to([0.0, np_.top() + 0.38, 0])
        self.at("binds")
        self.play(sg.animate.move_to([0.0, np_.top() + 0.38, 0]), run_time=0.8)
        self.at("tightly")
        self.play(Indicate(np_.body, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.at("look inside the cell")
        inside = T("inside the cell", 26, GREY).move_to([-3.6, -0.9, 0])
        self.play(FadeIn(inside), run_time=0.5)
        self.at("Its tail is only")
        tl = T("tail: about 40 amino acids", 26, BLUE).move_to([3.1, -0.85, 0])
        ln = Line(tl.get_left() + LEFT * 0.05, np_.tail.get_right() + RIGHT * 0.05, color=BLUE, stroke_width=2.5)
        self.play(FadeIn(tl), Create(ln), run_time=0.7)
        self.at("nothing that looks like")
        nl = T("no enzyme-like part", 26, GREY).next_to(tl, DOWN, buff=0.25)
        self.play(FadeIn(nl), run_time=0.5)
        self.at("Where is the wire")
        q = qbox(1.3, 1.1).move_to([0.0, -2.5, 0])
        wire = DashedLine(np_.tail.get_bottom(), q.get_top(), color=GREY, stroke_width=3.5)
        self.play(Create(wire), FadeIn(q, scale=0.9), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------
YM = -0.5
CS = 1.25


def complex_at(xn, xp, ym=YM, s=CS):
    n = Rec("neuropilin", BLUE, xn, ym, s=s)
    p = Rec("plexin", PURPLE, xp, ym, s=s, tail_h=1.3, tail_w=0.3)
    return n, p


class S03Plexin(SpokenScene):
    def construct(self):
        mem = mem_bar(YM)
        n, p = complex_at(-3.6, 3.6)
        sm = semag(-3.6, n.top() + 0.37, w=1.8, h=0.7)
        self.add(mem)
        self.play(FadeIn(n), FadeIn(sm), run_time=0.01)  # carried over from the last scene, rebuilt in place
        self.at("a second protein")
        self.play(FadeIn(p, shift=LEFT * 0.3), run_time=0.8)
        self.at("neither protein alone")
        t1 = T("alone: no shrinking", 26, RED).move_to([-3.6, -3.1, 0])
        t2 = T("alone: no shrinking", 26, RED).move_to([3.6, -3.1, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.play(FadeIn(t2), run_time=0.4)
        self.at("Together")
        tt = T("together: the cell shrinks", 28, GREEN).move_to([0.0, -3.1, 0])
        bridge = semag(0.0, n.top() + 0.37, w=5.0, h=0.7)
        self.play(FadeOut(t1), FadeOut(t2), n.animate.shift(RIGHT * 2.35), p.animate.shift(LEFT * 2.35),
                  ReplacementTransform(sm, bridge), run_time=1.0)
        self.play(FadeIn(tt), run_time=0.4)
        self.at("more tightly")
        tg = T("tighter grip on Sema3A", 26, YELLOW).move_to([0.0, 3.3, 0])
        self.play(FadeIn(tg), Indicate(bridge, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("Membrane semaphorins")
        tg2 = T("membrane semaphorins: plexin directly", 26, YELLOW).move_to([0.0, 3.3, 0])
        self.play(FadeTransform(tg, tg2), run_time=0.5)
        self.at("The secreted class")
        tg3 = T("secreted class 3: through neuropilin", 26, YELLOW).move_to([0.0, 3.3, 0])
        self.play(FadeTransform(tg2, tg3), Indicate(n.body, color=BLUE, scale_factor=1.05), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
class S04Split(SpokenScene):
    def construct(self):
        mem = mem_bar(YM)
        n, p = complex_at(-1.25, 1.25)
        bridge = semag(0.0, n.top() + 0.37, w=5.0, h=0.7)
        self.add(mem)
        self.play(FadeIn(n), FadeIn(p), FadeIn(bridge), run_time=0.01)
        self.at("A neuropilin without its tail")
        cl = T("neuropilin with no tail", 26, BLUE).move_to([0.0, -2.85, 0])
        self.play(FadeIn(cl), n.tail.animate.set_color(RED), run_time=0.5)
        self.play(FadeOut(n.tail), run_time=0.4)
        self.at("still supported collapse")
        r1 = T("collapse still works", 28, GREEN).move_to([0.0, -3.3, 0])
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("A plexin stripped")
        cl2 = T("plexin with no inner part", 26, PURPLE).move_to([0.0, -2.85, 0])
        self.play(FadeOut(r1), FadeTransform(cl, cl2), FadeIn(n.tail.set_color(BLUE)), run_time=0.5)
        self.play(p.tail.animate.set_color(RED), run_time=0.4)
        self.play(FadeOut(p.tail), run_time=0.3)
        self.at("blocked")
        r2 = T("Sema3A response blocked", 28, RED).move_to([0.0, -3.3, 0])
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("So neuropilin catches")
        a = T("catches", 30, BLUE).move_to([n.x, 3.3, 0])
        self.play(FadeOut(r2), FadeOut(cl2), FadeIn(p.tail.set_color(PURPLE)), FadeIn(a), run_time=0.6)
        self.at("Plexin signals")
        b = T("signals", 30, PURPLE).move_to([p.x, 3.3, 0])
        self.play(FadeIn(b), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------
class S05Gap(SpokenScene):
    def construct(self):
        mem = mem_bar(YM)
        n, p = complex_at(-1.25, 1.25)
        bridge = semag(0.0, n.top() + 0.37, w=5.0, h=0.7)
        self.add(mem)
        self.play(FadeIn(n), FadeIn(p), FadeIn(bridge), run_time=0.01)
        self.at("Inside the cell")
        # slide the view down to the inside: membrane rises, plexin inner part becomes the stage
        ym = 1.7
        px = -3.8
        newmem = mem_bar(ym)
        newtail = rr(0.3, 1.5, PURPLE, op=0.5, sw=3, r=0.06).move_to([px, ym - 0.17 - 0.75, 0])
        neck = Rectangle(width=0.3, height=0.34, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).move_to([px, ym, 0])
        pl = T("Plexin-B1", 28, PURPLE).move_to([px - 1.05, ym - 0.7, 0])
        frame_box = DashedVMobject(Rectangle(width=12.4, height=4.1, stroke_color=GREY, stroke_width=2.5), num_dashes=80).move_to([0, 0.35, 0])
        bs = T("separate example, best-studied case: Plexin-B1", 24, GREY).move_to([0.0, 2.95, 0])
        self.play(FadeIn(frame_box), FadeIn(bs), FadeOut(n), FadeOut(bridge), FadeOut(p.body), FadeOut(p.lab), FadeOut(p.neck),
                  ReplacementTransform(mem, newmem), ReplacementTransform(p.tail, newtail), FadeIn(neck), FadeIn(pl),
                  run_time=1.0)
        self.at("acts as a")
        gap = chip("GAP", PURPLE, size=32).move_to([px, -0.2, 0])
        self.play(FadeIn(gap, shift=UP * 0.2), run_time=0.6)
        self.at("hydrolysis")
        rras = chip("small GTPase", ORANGE, size=30).move_to([0.0, -0.2, 0])
        gtp = chip("GTP", GOLD, size=22, pad=0.14).next_to(rras, UP, buff=0.3)
        self.play(FadeIn(rras, shift=RIGHT * 0.3), FadeIn(gtp), run_time=0.7)
        self.at("switches")
        bar = Line(gap.get_right() + RIGHT * 0.1, rras.get_left() + LEFT * 0.12, color=RED, stroke_width=5)
        tee = Line(rras.get_left() + LEFT * 0.12 + UP * 0.25, rras.get_left() + LEFT * 0.12 + DOWN * 0.25, color=RED, stroke_width=6)
        self.play(Create(bar), Create(tee), FadeOut(gtp), rras[0].animate.set_stroke(GREY).set_fill(GREY, 0.16),
                  rras[1].animate.set_color(GREY), run_time=0.8)
        # reset R-Ras so the story reads in order: it is the target
        self.at("the target is")
        rras2 = chip("R-Ras", GREY, size=30).move_to(rras)
        self.play(FadeTransform(rras, rras2), run_time=0.5)
        rras = rras2
        self.at("helps hold")
        adh = chip("integrin adhesion", ORANGE, size=30).move_to([4.1, -0.2, 0])
        link = Arrow(rras.get_right() + RIGHT * 0.05, adh.get_left() + LEFT * 0.05, buff=0.05, color=GREY, stroke_width=5)
        self.play(GrowArrow(link), FadeIn(adh, shift=LEFT * 0.2), run_time=0.7)
        self.at("Switch it off")
        fall = T("adhesion falls", 32, RED).next_to(adh, DOWN, buff=0.4)
        self.play(adh[0].animate.set_stroke(RED).set_fill(RED, 0.1), adh[1].animate.set_color(RED).set_opacity(0.7),
                  link.animate.set_color(RED).set_opacity(0.3), FadeIn(fall), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        c = np.array([-4.0, 0.0, 0.0])
        R = 3.2
        sh = shaft(c)
        fn = fan(-0.85, 0.85, R, c)
        fo = filopodia(-0.85, 0.85, R, c)
        gc = T("growth cone", 28, TEAL).move_to([-5.3, -0.75, 0])
        self.at("Plexin signaling also")
        pc = chip("plexin", PURPLE, size=28).move_to([3.4, 2.6, 0])
        self.play(FadeIn(sh), FadeIn(fn), FadeIn(fo), FadeIn(gc), FadeIn(pc), run_time=0.9)
        self.at("family GTPases")
        c1 = chip("Rho-family GTPases", PURPLE, size=26).move_to([3.4, 1.35, 0])
        a1 = Arrow(pc.get_bottom(), c1.get_top(), buff=0.06, color=PURPLE, stroke_width=4)
        self.play(GrowArrow(a1), FadeIn(c1), run_time=0.6)
        self.at("proteins that act")
        c2 = chip("actin and microtubule\nproteins", PURPLE, size=26).move_to([3.4, 0.0, 0])
        xl = 0.35
        a2 = VGroup(Line(pc.get_left(), [xl, pc.get_center()[1], 0], color=PURPLE, stroke_width=4),
                    Line([xl, pc.get_center()[1], 0], [xl, c2.get_center()[1], 0], color=PURPLE, stroke_width=4),
                    Arrow([xl, c2.get_center()[1], 0], c2.get_left(), buff=0.04, color=PURPLE, stroke_width=4))
        self.play(FadeIn(a2), FadeIn(c2), run_time=0.6)
        self.at("The net result")
        head = T("local loss of\nactin and adhesion", 28, RED, line_spacing=0.9).move_to([3.4, 1.5, 0])
        self.play(FadeOut(c1), FadeOut(a1), FadeOut(c2), FadeOut(a2), FadeOut(pc), run_time=0.4)
        self.play(FadeIn(head), run_time=0.4)
        self.at("On one side")
        top_pts = [(c[0] + 3.9 * np.cos(a), c[1] + 3.9 * np.sin(a)) for a in (0.45, 0.65, 0.85)]
        dd = dots(top_pts)
        case = T("one side: a turn", 30, YELLOW).move_to([3.4, -0.9, 0])
        self.play(FadeIn(dd, shift=DOWN * 0.2), FadeIn(case), run_time=0.6)
        self.at("that means a turn")
        turned = fan(-1.25, 0.0, R, c)
        self.play(ReplacementTransform(fn, turned), FadeOut(fo), run_time=1.2)
        self.at("Everywhere at once")
        fn2 = fan(-0.85, 0.85, R, c)
        fo2 = filopodia(-0.85, 0.85, R, c)
        ring = [(c[0] + 3.9 * np.cos(a), c[1] + 3.9 * np.sin(a)) for a in np.linspace(-0.85, 0.85, 7)]
        dd2 = dots(ring)
        case2 = T("all round: collapse", 30, YELLOW).move_to([3.4, -0.9, 0])
        self.play(ReplacementTransform(turned, fn2), FadeIn(fo2), FadeOut(dd), FadeTransform(case, case2), run_time=0.7)
        self.play(FadeIn(dd2, shift=LEFT * 0.2), run_time=0.5)
        self.at("it means collapse")
        thin = fan(-0.07, 0.07, R * 0.62, c)
        self.play(ReplacementTransform(fn2, thin), FadeOut(fo2), run_time=1.1)
        self.at("Keep the split")
        self.play(FadeOut(dd2), FadeOut(case2), FadeOut(head), FadeOut(gc), FadeOut(thin), FadeOut(sh), run_time=0.6)
        self.at("Neuropilin catches")
        cn = chip("neuropilin catches the semaphorin", BLUE, size=32).move_to([0.0, 0.9, 0])
        self.play(FadeIn(cn, shift=UP * 0.15), run_time=0.6)
        self.at("Plexin sends")
        cp = chip("plexin sends the signal", PURPLE, size=32).move_to([0.0, -0.9, 0])
        self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Neuropilin catches the semaphorin. Plexin sends the signal."
