"""Caught in the Act (chapter 3 of "Microglia and Complement Prune Synapses")

COLOR MAP (shared by all chapters; taken from scenes.old.py)
  BLUE   = inputs from eye A (here: the eye that is silenced or boosted in the drug tests)
  ORANGE = inputs from eye B (here: the control / untreated eye)
  YELLOW = the complement tag (C1q, C3b, iC3b)
  PURPLE = microglia, the eater, and uptake bars
  TEAL   = complement receptor 3, the reader
  RED    = silenced eye (TTX), mice without the receptor or C3
  GREEN  = boosted (more active) eye (forskolin)
  GREY   = outlines, lysosome, unknown
  WHITE  = acid-reporting dye glow
  PURPLE = also the visibly mixed overlap zone
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
EYE_A, EYE_B = BLUE, ORANGE


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


def _unit(deg):
    return P(np.cos(np.radians(deg)), np.sin(np.radians(deg)))


def rcap(line):
    line.set_cap_style(CapStyleType.ROUND)
    return line


def bulb(c, color=BLUE, r=0.45, op=0.45):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(c)


def tag_dots(c, r, n=8, a0=0.0, rad=0.1):
    return VGroup(*[Dot(radius=rad, color=YELLOW).move_to(c + r * _unit(np.degrees(a0) + 360 * k / n)) for k in range(n)])


def branch(c, ang, ln, sx, w=13, op=0.55, bend=7):
    pts = [c + _unit(ang) * 0.6 * sx, c + _unit(ang + bend) * 0.55 * ln, c + _unit(ang + bend * 1.5) * 0.8 * ln,
           c + _unit(ang + bend * 1.6) * ln]
    m = VMobject().set_points_smoothly(pts).set_stroke(PURPLE, w, opacity=op)
    m.set_cap_style(CapStyleType.ROUND)
    t0 = c + _unit(ang + bend * 1.2) * 0.7 * ln
    tw = rcap(Line(t0, t0 + _unit(ang + 50) * 0.5 * sx, color=PURPLE, stroke_width=w * 0.7, stroke_opacity=op))
    return VGroup(m, tw)


def microglia(c, sx=1.0, procs=((160, 1.7), (20, 1.7), (260, 1.5))):
    body = Ellipse(width=1.65 * sx, height=1.5 * sx, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE,
                   fill_opacity=0.3).move_to(c)
    g = VGroup(*([branch(c, a, ln * sx, sx) for a, ln in procs] + [body]))
    g.body = body
    return g


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vbar(x, base, w, h, color, op=0.5):
    h = max(h, 0.02)
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to(P(x, base + h / 2))


def hbar(x0, y, w, h, color, op=0.5):
    w = max(w, 0.02)
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to(P(x0 + w / 2, y))


def terr(x0, x1, cy, h, color, op=0.35):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to(P((x0 + x1) / 2, cy))


def eye(c, color, r=0.8):
    ring = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    pupil = Circle(radius=r * 0.42, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    g = VGroup(ring, pupil).move_to(c)
    g.ring, g.pupil = ring, pupil
    return g


def injection(c, color, r=1.6):
    direction = P(.8, -.6)
    tip = c + P(-.8, .6) * (r * .64)
    needle_start = tip - direction * .95
    barrel_center = needle_start - direction * .6
    barrel = Rectangle(width=1.2, height=.46, stroke_color=color, stroke_width=4,
                       fill_color=color, fill_opacity=.45).rotate(-np.arctan2(.6, .8)).move_to(barrel_center)
    back = barrel_center - direction * .6
    cross = P(.6, .8)
    return VGroup(barrel, Line(needle_start, tip, color=TEXT, stroke_width=5),
                  Line(back, back - direction * .4, color=color, stroke_width=5),
                  Line(back - direction * .4 - cross * .36, back - direction * .4 + cross * .36,
                       color=color, stroke_width=5))


def speck(c, color, r=0.13):
    return Dot(radius=r, color=color).move_to(c)


def frag(c, color):
    """a piece of a presynaptic terminal: a blob with a few vesicle dots."""
    b = bulb(c, color, 0.3, 0.5)
    v = VGroup()  # no unlabelled vesicle dots
    return VGroup(b, v)


def words_line(words, size=28, color=TEXT, under=()):
    """a line built word by word so single words can be underlined. returns (VGroup line, {word: underline})."""
    ws = [T(w, size, color) for w in words]
    g = VGroup(*ws).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
    uls = {}
    for w, m in zip(words, ws):
        if w in under:
            uls[w] = Line(m.get_corner(DL) + DOWN * 0.08, m.get_corner(DR) + DOWN * 0.08, color=GOLD, stroke_width=5)
    return g, uls


# fixed layouts that several scenes share ------------------------------------------------------
CELL_C = P(0.0, 0.3)
INSIDE = [(-0.8, 0.3), (-0.2, 0.7), (0.5, 0.4), (0.7, -0.3), (-0.4, -0.4)]
INSIDE_COL = [EYE_A, EYE_B, EYE_B, EYE_A, EYE_B]


def big_cell(c, sx=2.5, procs=((150, 1.7), (30, 1.7), (210, 1.5), (330, 1.5))):
    return microglia(c, sx, procs)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Microglia and Complement Prune Synapses"
    TITLE = "Caught in the Act"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        C = P(0.0, 0.0)
        mg = microglia(C, 2.3, procs=((150, 1.7), (30, 1.7), (210, 1.7), (330, 1.7)))
        ml = T("microglia", 30, PURPLE).move_to(C + P(0, -2.55))
        terms = VGroup()
        spots = [(-5.2, 1.6, EYE_A), (-5.0, -1.4, EYE_B), (5.2, 1.4, EYE_B), (5.0, -1.6, EYE_A), (-2.6, 2.9, EYE_B), (2.7, -2.9, EYE_A)]
        for x, y, col in spots:
            terms.add(bulb(P(x, y), col, 0.42, 0.5))
        self.add(T("purple: microglia · orange and blue: retinal inputs",26).move_to(P(0,3.45)))
        self.play(FadeIn(mg, scale=0.85), FadeIn(ml), run_time=0.5)
        self.at("retinal inputs")
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in terms], lag_ratio=0.15), run_time=1.0)
        self.at("catch them doing it")
        ring = DashedVMobject(Circle(radius=1.9, stroke_color=TEXT, stroke_width=4).move_to(C), num_dashes=28)
        q1 = T("?", 90, TEXT, font=TITLE_FONT).move_to(P(0.0, 0.1))
        self.play(Create(ring), FadeIn(q1, scale=0.6), run_time=0.8)
        self.at("choose what they eat")
        self.play(FadeOut(q1), run_time=0.3)
        qa = T("?", 64, GREY, font=TITLE_FONT).move_to(P(-3.8, 0.1))
        qb = T("?", 64, GREY, font=TITLE_FONT).move_to(P(3.8, 0.1))
        self.play(FadeIn(qa), FadeIn(qb), *[Indicate(terms[i], color=TEXT, scale_factor=1.35) for i in (0, 3)],
                  run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Schafer(SpokenScene):
    def construct(self):
        credit=VGroup(T("2012",112,GOLD,font=TITLE_FONT),T("Dorothy Schafer",58),
                      T("and colleagues",32,GREY),T("Stevens laboratory",40)).arrange(DOWN,buff=.4)
        self.add(credit)
        self.at("set out to look")
        self.play(Indicate(credit[1],color=GOLD,scale_factor=1.04),run_time=.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tracers(SpokenScene):
    def construct(self):
        a,b=P(-3.3,.4),P(3.3,.4)
        ya,yb=eye(a,EYE_A,1.55),eye(b,EYE_B,1.55)
        p4=chip("P4",TEXT,size=32).move_to(P(0,.4))
        legend=T("blue tracer                     orange tracer",30).move_to(P(0,-2.2))
        self.add(ya,yb,p4,legend)
        self.at("colored tracer")
        sa,sb=injection(a,EYE_A,1.55),injection(b,EYE_B,1.55)
        self.play(FadeIn(sa,shift=P(-.24,.18)),FadeIn(sb,shift=P(-.24,.18)),run_time=.45)
        da,db=speck(sa[1].get_start(),EYE_A,.19),speck(sb[1].get_start(),EYE_B,.19)
        self.add(da,db)
        self.play(da.animate.move_to(a),db.animate.move_to(b),run_time=.65)
        self.play(FadeOut(da),FadeOut(db),ya.ring.animate.set_fill(EYE_A,.75),yb.ring.animate.set_fill(EYE_B,.75),run_time=.3)
        self.at("a day later")
        self.play(FadeOut(VGroup(ya,yb,p4,legend,sa,sb)),run_time=.3)
        box=VGroup(terr(-5.4,0,0,4.6,EYE_A),terr(0,5.4,0,4.6,EYE_B))
        self.add(chip("P5",TEXT,size=36).move_to(P(-4.9,3.15)),T("visual thalamus · dLGN",36).move_to(P(1,3.15)),box)
        self.at("visual thalamus")
        self.play(Indicate(box,scale_factor=1.02),run_time=.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cell_with_specks(sx=2.5, c=CELL_C):
    cell = big_cell(c, sx)
    ins = VGroup(*[speck(c + P(dx, dy) * (sx / 2.2), col, 0.17) for (dx, dy), col in zip(INSIDE, INSIDE_COL)])
    return cell, ins


class S04Inside(SpokenScene):
    def construct(self):
        c=P(0,.65)
        cell=big_cell(c,3.0,procs=((165,1.35),(15,1.35)))
        ins=VGroup(*[speck(c+P(dx,dy)*1.2,col,.19) for (dx,dy),col in zip(INSIDE,INSIDE_COL)])
        outs=VGroup(speck(P(-4,1.9),EYE_A,.19),speck(P(4,-.5),EYE_B,.19))
        header=T("3D reconstruction",32).move_to(P(0,3.35))
        numerator=T("volume of retinal label inside the cell",28,EYE_A)
        denominator=T("volume of the whole microglial cell",28,PURPLE)
        eq=VGroup(T("engulfment index (%)",30),numerator,Line(LEFT*3.8,RIGHT*3.8,color=GREY),denominator,
                  T("× 100",28)).arrange(DOWN,buff=.1).move_to(P(0,-2.55))
        # Cell above, full formula below: neither is cropped or hidden by the other.
        cell.scale(.83,about_point=c); ins.shift(UP*.3)
        self.add(cell,ins,outs,header,eq)
        self.at("does not show")
        self.play(Indicate(outs,color=TEXT),run_time=.5)
        self.at("only label inside")
        self.play(FadeOut(outs,run_time=1.0),numerator.animate.set_color(GOLD),run_time=1.0)
        self.at("the cell counts")
        self.play(denominator.animate.set_color(GOLD),run_time=.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
LYS_C = CELL_C + P(0.0, 0.05)


def lysosome(c=LYS_C, r=1.65):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to(c)


LYS_SPECKS = [(-0.55, 0.4), (0.15, 0.62), (0.58, 0.14), (0.35, -0.5), (-0.35, -0.42)]


class S05Lyso(SpokenScene):
    def construct(self):
        cell, ins = cell_with_specks()
        self.add(cell)
        self.play(FadeIn(ins), run_time=0.5)
        self.at("sat inside")
        lys = lysosome()
        ll = T("lysosome", 28, GREY).move_to(P(0, -1.65))
        moves = [s.animate.move_to(LYS_C + P(*p)) for s, p in zip(ins, LYS_SPECKS)]
        self.play(FadeIn(lys), *moves, FadeIn(ll), run_time=1.0)
        self.at("digestive compartments")
        ll2 = T("lysosome: the cell's digestive compartment", 28, GREY).move_to(P(0, -3.2))
        self.play(Indicate(lys, color=TEXT, scale_factor=1.15), ReplacementTransform(ll, ll2), run_time=0.9)
        self.at("a dye that glows")
        dye = T("acid-reporting dye", 28, TEXT).move_to(P(0, 3.3))
        self.play(lys.animate.set_fill(TEXT, 0.5).set_stroke(TEXT), 
                  FadeIn(dye, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


class S06Pre(SpokenScene):
    def construct(self):
        cell = big_cell(CELL_C)
        lys = lysosome()
        ins = VGroup(*[speck(LYS_C + P(*p), col, 0.14) for p, col in zip(LYS_SPECKS, INSIDE_COL)])
        dye_label=T("acid-reporting dye",28).move_to(P(0,3.3))
        self.add(cell, lys, ins, dye_label)
        lys.set_fill(TEXT,.35).set_stroke(TEXT)
        self.at("mainly presynaptic")
        fr = VGroup(frag(LYS_C + P(-0.5, 0.35), EYE_A), frag(LYS_C + P(0.5, 0.45), EYE_B), frag(LYS_C + P(0.0, -0.5), EYE_B))
        pc = chip("presynaptic", TEXT, size=34).move_to(P(0, 3.3))
        self.play(ReplacementTransform(ins, fr), ReplacementTransform(dye_label,pc), run_time=0.6)
        self.at("from retinal terminals")
        rt = T("pieces of retinal terminals", 30, TEXT).move_to(P(0, -3.2))
        ar = arr(rt.get_top() + P(0, 0.05), LYS_C + P(0, -1.15), TEXT)
        self.play(FadeIn(rt, shift=UP * 0.1), GrowArrow(ar), run_time=0.7)
        self.finish()


class S07Beat(NarratedScene):
    def construct(self):
        cell = big_cell(CELL_C)
        lys = lysosome()
        fr = VGroup(frag(LYS_C + P(-0.5, 0.35), EYE_A), frag(LYS_C + P(0.5, 0.45), EYE_B), frag(LYS_C + P(0.0, -0.5), EYE_B))
        pc = chip("presynaptic", TEXT, size=34).move_to(P(0, 3.3))
        rt = T("pieces of retinal terminals", 30, TEXT).move_to(P(0, -3.2))
        ar = arr(rt.get_top() + P(0, 0.05), LYS_C + P(0, -1.15), TEXT)
        self.add(cell, lys, fr, pc, rt, ar)
        pointer=arr(P(3.4,1.3),P(.8,.8),TEXT)
        label=T("terminal fragment",28).move_to(P(4.4,1.8))
        self.play(GrowArrow(pointer),FadeIn(label),run_time=.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Clock(SpokenScene):
    def construct(self):
        base = -2.7
        ax = Line(P(-1.6, base), P(6.2, base), color=GREY, stroke_width=3)
        sch = chip("schematic", GREY, size=26, pad=0.14).move_to(P(5.4, 3.3))
        ttl = T("retinal material inside microglia", 28, TEXT).move_to(P(-1.5, 3.3))
        clk = Circle(radius=1.4, stroke_color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=0.06).move_to(P(-4.4, 0.2))
        hand = rcap(Line(clk.get_center(), clk.get_center() + P(0, 1.0), color=TEXT, stroke_width=7))
        hand2 = rcap(Line(clk.get_center(), clk.get_center() + P(0.55, 0.0), color=GREY, stroke_width=7))
        ticks = VGroup(*[Line(clk.get_center() + _unit(a) * 1.15, clk.get_center() + _unit(a) * 1.32, color=GREY, stroke_width=4)
                         for a in range(0, 360, 90)])
        self.add(T("uptake",26).rotate(PI/2).move_to(P(-1.9,-.2)))
        self.play(FadeIn(ax), FadeIn(ttl), FadeIn(sch), run_time=0.5)
        self.at("a clock")
        self.play(FadeIn(clk), FadeIn(ticks), FadeIn(hand), FadeIn(hand2), run_time=0.5)
        self.play(Rotate(hand, angle=-2 * PI * 0.4, about_point=clk.get_center()), run_time=0.9)
        self.at("high at")
        b5 = vbar(0.6, base, 2.0, 0.02, PURPLE)
        l5 = T("P5", 34, TEXT).move_to(P(0.6, base - 0.45))
        self.add(b5)
        self.play(Transform(b5, vbar(0.6, base, 2.0, 0.8 * 6, PURPLE)), FadeIn(l5), run_time=0.9)
        self.at("much lower")
        b9 = vbar(4.4, base, 2.0, 0.02, PURPLE)
        l9 = T("P9", 34, TEXT).move_to(P(4.4, base - 0.45))
        self.add(b9)
        self.play(Transform(b9, vbar(4.4, base, 2.0, 0.1 * 6, PURPLE)), FadeIn(l9), run_time=0.9)
        self.play(GrowArrow(arr(P(1.8,-2.9),P(3.2,-2.9),TEXT)),run_time=.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
BASE9 = -2.0
H9 = 0.8 * 4.5  # schematic volume model: normal .8, knockout .4


class S09Reader(SpokenScene):
    def construct(self):
        ax = Line(P(-6.2, BASE9), P(6.2, BASE9), color=GREY, stroke_width=3)
        ttl = T("retinal material inside microglia", 30, TEXT).move_to(P(-1.0, 3.3))
        sch = chip("schematic", GREY, size=26, pad=0.14).move_to(P(5.4, 3.3))
        nb = vbar(-4.3, BASE9, 2.2, 0.02, PURPLE)
        nl = T("normal", 30, TEXT).move_to(P(-4.3, BASE9 - 0.5))
        self.add(nb,T("uptake",26).rotate(PI/2).move_to(P(-6.3,.3)))
        self.play(FadeIn(ax), FadeIn(ttl), FadeIn(sch), FadeIn(nl), Transform(nb, vbar(-4.3, BASE9, 2.2, H9, PURPLE)), run_time=1.0)
        self.at("tag and a reader")
        tg = chip("tag", YELLOW, size=28).move_to(P(-5.2, 2.3))
        rd = chip("reader", TEAL, size=28).move_to(P(-3.4, 2.3))
        self.play(FadeIn(tg, shift=DOWN * 0.1), FadeIn(rd, shift=DOWN * 0.1), run_time=0.6)
        self.at("without complement receptor")
        c3l = T("no CR3\nthe reader", 30, RED, line_spacing=0.6).move_to(P(0.0, BASE9 - 0.65))
        g1 = DashedVMobject(Rectangle(width=2.2, height=H9, stroke_color=GREY, stroke_width=3).move_to(P(0.0, BASE9 + H9 / 2)), num_dashes=40)
        g2 = DashedVMobject(Rectangle(width=2.2, height=H9, stroke_color=GREY, stroke_width=3).move_to(P(4.3, BASE9 + H9 / 2)), num_dashes=40)
        self.play(FadeOut(tg), FadeOut(rd), FadeIn(c3l, shift=UP * 0.1), run_time=0.6)
        self.at("or C3")
        c3b = T("no C3\nthe tag source", 30, RED, line_spacing=0.6).move_to(P(4.3, BASE9 - 0.65))
        self.play(FadeIn(c3b, shift=UP * 0.1), run_time=0.6)
        self.at("took up")
        k1 = vbar(0.0, BASE9, 2.2, 0.02, RED, 0.4)
        k2 = vbar(4.3, BASE9, 2.2, 0.02, RED, 0.4)
        self.add(k1, k2)
        half = DashedLine(P(-3.2, BASE9 + H9 / 2), P(5.4, BASE9 + H9 / 2), color=GREY, stroke_width=3)
        self.play(Transform(k1, vbar(0.0, BASE9, 2.2, H9 / 2, RED, 0.4)), Transform(k2, vbar(4.3, BASE9, 2.2, H9 / 2, RED, 0.4)),
                  Create(half), FadeIn(T("about half",26,TEXT).move_to(P(2.15,.25))), FadeOut(g1), FadeOut(g2), run_time=1.0)
        self.finish()


class S10Later(SpokenScene):
    def construct(self):
        self.add(T("mice without CR3 or C3, later",34,RED).move_to(P(0,3.2)))
        maps=[]
        for cx,overlap,label in [(-3.4,.18,"normal"),(3.3,1.5,"without CR3 or C3")]:
            cy=.35; w=5.1; h=3.8
            g=VGroup(terr(cx-w/2,cx+overlap/2,cy,h,EYE_A),terr(cx-overlap/2,cx+w/2,cy,h,EYE_B),
                     Rectangle(width=overlap,height=h,stroke_width=0,fill_color=PURPLE,fill_opacity=.9).move_to(P(cx,cy)),
                     T(label,28).move_to(P(cx,2.65)))
            maps.append(g)
        self.add(maps[0])
        self.at("more overlap")
        self.play(FadeIn(maps[1]),run_time=.5)
        self.add(T("dLGN territories: overlap at about P10",28,PURPLE).move_to(P(0,-2.15)))
        self.at("extra retinal synapses")
        self.play(FadeIn(chip("retinal synapses: more · about a month",TEXT,size=32).move_to(P(0,-3.05))),run_time=.5)
        self.finish()


class S11Part(SpokenScene):
    def construct(self):
        bars=VGroup(vbar(-4.3,BASE9,2.2,H9,PURPLE),vbar(0,BASE9,2.2,H9/2,RED),vbar(4.3,BASE9,2.2,H9/2,RED))
        self.add(T("retinal material inside microglia",26).rotate(PI/2).move_to(P(-6.3,.3)))
        self.add(bars,Line(P(-6.2,BASE9),P(6.2,BASE9),color=GREY),
                 T("retinal material inside microglia",30).move_to(P(-1,3.3)),chip("schematic",GREY,size=26).move_to(P(5.4,3.3)),
                 T("normal",30).move_to(P(-4.3,-2.6)),T("no CR3\nreader",30,RED).move_to(P(0,-2.8)),
                 T("no C3\ntag source",30,RED).move_to(P(4.3,-2.8)))
        self.at("half the eating remained")
        self.play(bars[1].animate.set_fill(RED,.85),bars[2].animate.set_fill(RED,.85),run_time=.5)
        self.at("is one")
        ghost=VGroup(*[DashedVMobject(vbar(x,BASE9+H9/2,2.2,H9/2,YELLOW,0),num_dashes=24) for x in [0,4.3]])
        self.play(Create(ghost),run_time=.4)
        self.at("of several")
        self.play(FadeIn(chip("other routes: about half remains",TEXT,size=28).move_to(P(1.9,2.4))),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Ttx(SpokenScene):
    def construct(self):
        a,b=P(-3.3,0),P(3.3,0)
        ya,yb=eye(a,EYE_A,1.6),eye(b,EYE_B,1.6)
        self.add(ya,yb,T("key question",40,GOLD).move_to(P(0,3.25)))
        self.at("silence one eye")
        sa,sb=injection(a,RED),injection(b,TEXT)
        self.play(FadeIn(sa,shift=P(-.24,.18)),FadeIn(sb,shift=P(-.24,.18)),run_time=.4)
        self.at("with tetrodotoxin")
        silenced(ya)
        self.add(T("tetrodotoxin (TTX)",32,RED).move_to(P(-3.3,2.3)),T("silenced",30,RED).move_to(P(-3.3,-2.2)),
                 T("matched control",32).move_to(P(3.3,2.3)),T("control injection",30,GREY).move_to(P(3.3,-2.2)))
        self.at("which blocks")
        self.play(FadeIn(T("TTX blocks sodium channels",30).move_to(P(0,-3.25))),run_time=.4)
        self.finish()


def pred_scene(scene, animate=True):
    C = P(0.0, -0.9)
    cell = microglia(C, 2.3, procs=((160, 1.7), (20, 1.7), (200, 1.5), (340, 1.5)))
    ins = VGroup(*[speck(C + P(dx, dy), col, 0.15) for (dx, dy), col in zip(
        [(-0.9, 0.3), (-0.3, 0.7), (0.5, 0.45), (0.8, -0.2), (-0.5, -0.4), (0.1, -0.1)], [EYE_A, EYE_B, EYE_A, EYE_B, EYE_B, EYE_A])])
    leg_a = T("blue: the silenced eye", 26, EYE_A).move_to(P(-3.7, -3.4))
    leg_b = T("orange: the control eye", 26, EYE_B).move_to(P(3.7, -3.4))
    return cell, ins, leg_a, leg_b


class S13Predict(SpokenScene):
    def construct(self):
        cell, ins, la, lb = pred_scene(self)
        pr = T("Predict", 44, GOLD, font=TITLE_FONT).move_to(P(0, 3.3))
        self.play(FadeIn(cell, scale=0.85), FadeIn(ins), FadeIn(la), FadeIn(lb), FadeIn(pr), run_time=0.9)
        self.at("remove less active inputs")
        q1 = T("If microglia remove less active inputs,", 32, TEXT).move_to(P(0, 2.5))
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.6)
        self.at("whose material")
        q2 = T("whose material should they hold more of?", 32, TEXT).move_to(P(0, 1.9))
        self.play(FadeIn(q2, shift=DOWN * 0.1), run_time=0.6)
        self.at("hold more of")
        self.play(*[Indicate(s, color=TEXT, scale_factor=1.6) for s in ins], run_time=0.8)
        self.finish()


class S14Pause(NarratedScene):
    def construct(self):
        cell, ins, la, lb = pred_scene(self)
        pr = T("Predict", 44, GOLD, font=TITLE_FONT).move_to(P(0, 3.3))
        q1 = T("If microglia remove less active inputs,", 32, TEXT).move_to(P(0, 2.5))
        q2 = T("whose material should they hold more of?", 32, TEXT).move_to(P(0, 1.9))
        self.add(cell, ins, la, lb, pr, q1, q2)
        choices=VGroup(chip("silenced eye?",EYE_A,size=28).move_to(P(-4.7,1.15)),chip("control eye?",EYE_B,size=28).move_to(P(4.7,1.15)))
        self.play(FadeIn(choices),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
BB = -2.7
BH = 3.4
XA, XB = -3.0, 3.0


def eyes_pair():
    ya = eye(P(XA, 1.8), EYE_A, 0.65)
    yb = eye(P(XB, 1.8), EYE_B, 0.65)
    return ya, yb


def silenced(ya):
    ya.ring.set_fill(EYE_A, 0.28).set_stroke(RED, opacity=1, width=6)
    ya.pupil.set_stroke(EYE_A, opacity=1)


class S15Reveal(SpokenScene):
    def construct(self):
        ya, yb = eyes_pair()
        silenced(ya)
        sa = T("TTX, silenced", 26, RED).move_to(P(XA, 3.0))
        sb = T("matched control", 26, GREY).move_to(P(XB, 3.0))
        sch = chip("schematic", GREY, size=26, pad=0.12).move_to(P(5.4, 3.45))
        ax = Line(P(-5.2, BB), P(5.2, BB), color=GREY, stroke_width=3)
        self.play(FadeIn(ya), FadeIn(yb), FadeIn(sa), FadeIn(sb), FadeIn(ax), FadeIn(sch), run_time=0.6)
        fm = T("engulfed label per unit of that eye's input", 28).move_to(P(0,-3.3))
        yl = T("relative uptake",26).rotate(PI/2).move_to(P(-6, -.5))
        self.add(fm,yl)
        self.at("silenced eye's material")
        ba = vbar(XA, BB, 2.2, 0.02, EYE_A)
        bb = vbar(XB, BB, 2.2, 0.02, EYE_B)
        self.add(ba, bb)
        self.play(Transform(ba, vbar(XA, BB, 2.2, (.2/.2)*3.2, EYE_A)), Transform(bb, vbar(XB, BB, 2.2, (.1/.2)*(.2/.2)*3.2, EYE_B)), run_time=1.0)
        self.at("relative to")
        self.play(Indicate(fm,color=GOLD,scale_factor=1.02), run_time=0.4)
        self.at("that eye's input")
        self.play(Indicate(fm, color=GOLD, scale_factor=1.05), run_time=0.7)
        self.finish()


class S16Forskolin(SpokenScene):
    def construct(self):
        ya, yb = eyes_pair()
        silenced(ya)
        sa = T("TTX, silenced", 26, RED).move_to(P(XA, 3.0))
        sb = T("matched control", 26, GREY).move_to(P(XB, 3.0))
        sch = chip("schematic", GREY, size=26, pad=0.12).move_to(P(5.4, 3.45))
        ax = Line(P(-5.2, BB), P(5.2, BB), color=GREY, stroke_width=3)
        ba = vbar(XA, BB, 2.2, (.2/.2)*3.2, EYE_A)
        bb = vbar(XB, BB, 2.2, (.1/.2)*(.2/.2)*3.2, EYE_B)
        fm = T("engulfed label per unit of that eye's input", 28, TEXT).move_to(P(0, BB - 0.6))
        self.add(ya, yb, sa, sb, sch, ax, ba, bb, fm,T("relative uptake",26).rotate(PI/2).move_to(P(-6,-.5)))
        self.at("boost one eye")
        sa2 = T("forskolin, more active", 26, GREEN).move_to(P(XA, 3.0))
        sb2 = T("untreated", 26, GREY).move_to(P(XB, 3.0))
        self.play(Transform(ba, vbar(XA, BB, 2.2, 0.02, EYE_A)), Transform(bb, vbar(XB, BB, 2.2, 0.02, EYE_B)),
                  ReplacementTransform(sa, sa2), ReplacementTransform(sb, sb2),
                  ya.ring.animate.set_fill(EYE_A, 0.8).set_stroke(GREEN, opacity=1.0, width=7),
                  ya.pupil.animate.set_stroke(EYE_A, opacity=1.0), run_time=0.8)
        self.at("relatively more")
        self.play(Transform(ba, vbar(XA, BB, 2.2, (.1/.2)*3.2, EYE_A)), Transform(bb, vbar(XB, BB, 2.2, (.2/.2)*3.2, EYE_B)), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def big_arrow(a, b, color, w=22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.6, max_tip_length_to_length_ratio=1.0,
                 max_stroke_width_to_length_ratio=100)


def opposite_layout():
    base=DashedLine(P(-5.8,0),P(5.8,0),color=GREY)
    fixed=VGroup(base,T("no change",28,GREY).move_to(P(0,.3)),
                 T("TTX",38,RED).move_to(P(-3.3,3.25)),T("forskolin",38,GREEN).move_to(P(3.3,3.25)),
                 T("treated eye: eating per unit of its input",32).move_to(P(0,-3.35)))
    actual=VGroup(big_arrow(P(-4,0),P(-4,2.35),RED),big_arrow(P(2.3,0),P(2.3,-2.3),GREEN))
    damage=VGroup(big_arrow(P(-2.3,0),P(-2.3,2.35),GREY,12),big_arrow(P(4,0),P(4,2.35),GREY,12),
                  T("damage only:\nup both times",28,GREY).move_to(P(-3.3,-1.4)),
                  T("damage only:\nup both times",28,GREY).move_to(P(4.65,-1.4)))
    return fixed,actual,damage


class S17Opposite(SpokenScene):
    def construct(self):
        fixed,actual,damage=opposite_layout()
        self.add(fixed)
        self.at("opposite directions")
        self.play(FadeIn(actual),run_time=.6)
        self.at("damaged axons")
        self.play(FadeIn(damage[2:]),run_time=.4)
        self.at("raise eating of its own eye")
        self.play(GrowArrow(damage[0]),run_time=.5)
        self.at("both times")
        self.play(GrowArrow(damage[1]),run_time=.4)
        self.finish()


class S18Beat(NarratedScene):
    def construct(self):
        self.add(*opposite_layout())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Why(SpokenScene):
    def construct(self):
        C = P(0, 0)
        ring = DashedVMobject(Circle(radius=3.05, color=TEXT).move_to(C), num_dashes=40)
        cell = microglia(C, 2.0)
        self.add(cell, T("local input", 32).move_to(P(-4.6, 2.7)),
                 chip("invented numbers", GREY, size=26).move_to(P(4.5, 3.1)))
        self.at("near one")
        self.play(Create(ring), run_time=0.5)
        self.at("one eye's input")
        # Nine equal terminal symbols versus one: 10 local units per symbol.
        terminals = VGroup(*[bulb(2.5*_unit(18+36*k), EYE_B if k<9 else EYE_A, .23) for k in range(10)])
        counts=VGroup(T("9 orange · 90 units",24,EYE_B).move_to(P(0,.1)),
                      T("1 blue · 10 units",24,EYE_A).move_to(P(0,-.6)))
        self.play(FadeIn(terminals),FadeIn(counts), run_time=.6)
        self.at("far outnumber")
        self.play(Indicate(counts[0],scale_factor=1.04), run_time=.3)
        self.at("the others")
        self.play(Indicate(counts[1],scale_factor=1.04), run_time=.3)
        self.add(T("microglial cell", 28, PURPLE).move_to(P(0,-3.4)))
        self.finish()


XS = -5.4  # left end of the input bars in s20


class S20Fair(SpokenScene):
    def construct(self):
        cc = P(-2.1,-.9)
        cell = Circle(radius=1.85, color=PURPLE, fill_color=PURPLE, fill_opacity=.2).move_to(cc)
        self.add(chip("invented numbers", GREY, size=26).move_to(P(4.6,3.25)),
                 T("local input",30).move_to(P(-4.7,3.25)),cell,
                 T("no preference",28,PURPLE).move_to(P(-2.1,-3.2)))
        self.at("90 units from one eye")
        ob=hbar(-5.8,2.3,8.1,.55,EYE_B)
        self.play(FadeIn(ob),FadeIn(T("90 orange",28,EYE_B).move_to(P(3.6,2.3))),run_time=.4)
        self.at("and 10 from the other")
        bb=hbar(-5.8,1.65,.9,.55,EYE_A)
        self.play(FadeIn(bb),FadeIn(T("10 blue",28,EYE_A).move_to(P(-3.5,1.65))),run_time=.4)
        self.at("no preference")
        self.play(Indicate(cell, color=PURPLE),run_time=.4)
        self.at("a tenth of each")
        frac=VGroup(T("takes 0.1 of",28),T("each eye's input",28)).arrange(DOWN,buff=.12).move_to(P(3.3,.55))
        self.add(hbar(-5.8,2.3,8.1*.1,.55,EYE_B,.95),hbar(-5.8,1.65,.9*.1,.55,EYE_A,.95))
        dots=VGroup(*[speck(P(-5.75+.085*k,2.3),EYE_B,.04) for k in range(9)],speck(P(-5.755,1.65),EYE_A,.04))
        self.add(dots)
        self.play(FadeIn(frac), *[d.animate.scale(3.25).move_to(cc+P(-.65+.65*(k%3),.65-.65*(k//3))) for k,d in enumerate(dots[:9])],
                  dots[9].animate.scale(3.25).move_to(cc+P(0,-1.05)),run_time=.7)
        self.at("it holds")
        raw=VGroup(vbar(1.6,-2.6,.9,9*.24,EYE_B),vbar(4.3,-2.6,.9,1*.24,EYE_A),
                   T("9 orange",28,EYE_B).move_to(P(1.6,-3.1)),T("1 blue",28,EYE_A).move_to(P(4.3,-3.1)))
        self.play(FadeIn(raw),run_time=.4)
        self.finish()


B21 = -2.5
RS = 0.5   # raw units to height
PS = 22.0   # per unit fraction to height


class S21Twice(SpokenScene):
    def construct(self):
        base=-2.55; xo,xb=-4.7,-2.1; scale=.48
        self.add(chip("invented numbers",GREY,size=26).move_to(P(4.6,3.3)),
                 T("held inside (units)",30).move_to(P(-3.4,3.25)),
                 Line(P(-5.8,base),P(-.8,base),color=GREY))
        bo=vbar(xo,base,1.25,9*scale,EYE_B); bb=vbar(xb,base,1.25,scale,EYE_A)
        val=T("1",30,EYE_A).move_to(P(xb,base+scale+.35))
        label=T("blue",26,EYE_A).move_to(P(xb,-3.05))
        self.add(bo,bb,val,label,T("orange",26,EYE_B).move_to(P(xo,-3.05)),T("9",30,EYE_B).move_to(P(xo,2.1)))
        self.at("silence the minor")
        # Replace the label atomically; never crossfade two strings in the same place.
        self.remove(label)
        self.add(T("blue, silenced",26,RED).move_to(P(xb,-3.05)))
        self.at("twice the fraction")
        frac=T("blue fraction: 0.1 → 0.2",30,EYE_A).move_to(P(3.1,2.25))
        self.play(FadeIn(frac),run_time=.35)
        self.at("two tenths")
        self.play(Transform(bb,vbar(xb,base,1.25,2*scale,EYE_A)),
                  Transform(val,T("2",30,EYE_A).move_to(P(xb,base+2*scale+.35))),run_time=.5)
        self.add(DashedLine(P(-3.95,base+9*scale),P(-1.3,base+9*scale),color=GREY))
        self.at("instead of one tenth")
        self.add(T("orange fraction: 0.1",28,EYE_B).move_to(P(3.1,1.55)))
        self.at("it holds two units")
        self.play(Indicate(bb,color=EYE_A),run_time=.4)
        self.at("still fewer than nine")
        # Derived from the same raw counts and available local input.
        self.add(T("held / local input",30).move_to(P(3.1,.65)),Line(P(.6,base),P(5.8,base),color=GREY))
        bars=VGroup(vbar(1.9,base,1.2,(9/90)*12,EYE_B),vbar(4.4,base,1.2,(2/10)*12,EYE_A))
        labels=VGroup(T("0.1",28,EYE_B).move_to(P(1.9,-1.0)),T("0.2",28,EYE_A).move_to(P(4.4,.15)),
                      T("9 / 90",26,EYE_B).move_to(P(1.9,-3.05)),T("2 / 10",26,EYE_A).move_to(P(4.4,-3.05)),
                      T("twice the fraction",28).move_to(P(3.1,-3.6)))
        self.play(FadeIn(bars),FadeIn(labels),run_time=.5)
        self.finish()


class S22Fair2(SpokenScene):
    def construct(self):
        cy = -0.3
        box = RoundedRectangle(corner_radius=0.25, width=11.4, height=4.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.06).move_to(P(0, cy))
        tA = terr(-5.4, 0.1, cy, 3.0, EYE_A)
        tB = terr(-0.1, 5.4, cy, 3.0, EYE_B)
        bl = T("visual thalamus", 26, GREY).move_to(P(-4.3, cy + 1.86))
        self.play(FadeIn(box), FadeIn(tA), FadeIn(tB), FadeIn(bl), run_time=0.8)
        self.at("compares each eye")
        card = chip("each eye compared with its own local input", TEXT, size=30).move_to(P(0, 3.0))
        self.play(FadeIn(card, shift=DOWN * 0.1), run_time=0.7)
        self.at("measured where")
        C = P(2.4, cy)
        ring = DashedVMobject(Circle(radius=1.15, stroke_color=TEXT, stroke_width=5).move_to(C), num_dashes=20)
        cell = Ellipse(width=1.0, height=0.9, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.5).move_to(C)
        self.play(Create(ring), FadeIn(cell, scale=0.5), run_time=0.7)
        self.at("sampled")
        nt = T("a whole-nucleus map cannot give the local numbers", 28, GREY).move_to(P(0, -3.35))
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Limits(SpokenScene):
    def construct(self):
        hd = T("Limits", 52, GOLD, font=TITLE_FONT).move_to(P(0, 3.2))
        self.play(FadeIn(hd), run_time=0.5)
        self.at("this compares whole eyes")
        ix, tx = -5.4, -4.2
        i1 = VGroup(eye(P(ix - 0.4, 1.5), EYE_A, 0.5), eye(P(ix + 0.4, 1.5), EYE_B, 0.5))
        r1 = T("whole eyes, not single synapses", 40, TEXT).move_to(P(tx, 1.5), aligned_edge=LEFT)
        self.play(FadeIn(i1, scale=0.7), FadeIn(r1, shift=RIGHT * 0.15), run_time=0.8)
        self.at("it does not show")
        i2 = T("?", 90, YELLOW, font=TITLE_FONT).move_to(P(ix, -0.5))
        r2a = T("how activity becomes a mark", 40, TEXT)
        r2b = T("still open", 28, GREY)
        r2 = VGroup(r2a, r2b).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(P(tx, -0.5), aligned_edge=LEFT)
        self.play(FadeIn(i2, scale=0.7), FadeIn(r2, shift=RIGHT * 0.15), run_time=0.8)
        self.at("later imaging elsewhere")
        c3 = P(ix, -2.5)
        cc = Circle(radius=0.7, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35).move_to(c3)
        r3a = T("bites, not whole synapses", 40, TEXT)
        r3b = T("seen by imaging in other preparations", 28, GREY)
        r3 = VGroup(r3a, r3b).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(P(tx, -2.5), aligned_edge=LEFT)
        self.play(FadeIn(cc, scale=0.7), FadeIn(r3, shift=RIGHT * 0.15), run_time=0.8)
        self.at("take bites")
        notch = Circle(radius=0.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c3 + P(0.62, 0.25))
        piece = Circle(radius=0.25, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.5).move_to(c3 + P(0.62, 0.25))
        self.play(FadeIn(notch), FadeIn(piece), run_time=0.2)
        self.play(piece.animate.move_to(c3 + P(1.0, 0.95)), run_time=0.6)
        self.finish()


def under_word(line_text, word, size, left_x, y, color=GOLD):
    """underline one word of a single-line Text placed with its left edge at left_x (measures prefix widths)."""
    idx = line_text.index(word)
    pre = T(line_text[: idx + len(word)], size)
    w = T(word, size)
    x1 = left_x + pre.width
    x0 = x1 - w.width
    return Line(P(x0, y), P(x1, y), color=color, stroke_width=5)


class S24Idea(SpokenScene):
    def construct(self):
        self.add(T("the idea again",44,GOLD,font=TITLE_FONT).move_to(P(0,3.3)))
        cell=Circle(radius=1.05,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to(P(-1.5,.7))
        less=bulb(P(-5.3,1.6),EYE_A,.4);more=bulb(P(-5.3,-.6),EYE_B,.4)
        self.add(cell,less,more,T("less active eye",26,EYE_A).move_to(P(-5.1,2.45)),
                 T("more active eye",26,EYE_B).move_to(P(-5.1,-1.5)),T("microglia",28,PURPLE).move_to(P(-1.5,-.8)))
        self.at("relative activity biases")
        self.play(GrowArrow(arr(P(-4.75,1.5),P(-2.6,1.1),EYE_A,10)),GrowArrow(arr(P(-4.75,-.5),P(-2.6,.3),EYE_B,3)),run_time=.6)
        line1,u1=words_line(["relative","activity","biases"],28,under=("biases",))
        line2,u2=words_line(["how","much","material","is","taken"],28,under=("taken",))
        left=VGroup(line1,line2).arrange(DOWN,buff=.35).move_to(P(-3.4,-2.3))
        # Build underlines after positioning the text so they sit below the glyphs.
        marks=VGroup(*[Line(m.get_corner(DL)+DOWN*.16,m.get_corner(DR)+DOWN*.16,
                            color=GOLD,stroke_width=4) for m in (line1[-1],line2[-1])])
        self.add(left,marks)
        self.at("helps them")
        terminal=bulb(P(5,1),EYE_B,.75)
        tags=tag_dots(P(5,1),.9,8)
        target=microglia(P(2.1,1),.9,procs=((130,1.4),(240,1.3)))
        reader=Arc(radius=.38,start_angle=-PI/2,angle=PI,color=TEAL,stroke_width=7).move_to(P(2.9,1))
        self.add(terminal,tags,target,reader,T("complement",28,YELLOW).move_to(P(4.9,2.5)))
        self.at("part of it")
        bite=bulb(P(4.4,.7),EYE_B,.23)
        notch=Circle(radius=.25,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(P(4.4,.7))
        self.add(notch,bite)
        self.play(bite.animate.move_to(P(2.1,1)),run_time=.6)
        self.add(T("helps take part of it",30).move_to(P(3.5,-2.3)))
        self.at("how the two connect")
        gap=VGroup(DashedLine(P(-.35,1),P(.7,1),color=TEXT),
                   chip("open",TEXT,size=26).move_to(P(.15,1.85)))
        self.play(FadeIn(gap),FadeIn(T("How the two connect is still open.",32,TEXT).move_to(P(0,-3.4))),run_time=.5)
        self.finish()


class S25End(EndCard):
    LINE = "How the two connect is still open."
    def construct(self):
        line=VGroup(T("Activity biases how much microglia take.",38,font=TITLE_FONT),
                    T("Complement helps them take part of it.",38,font=TITLE_FONT),
                    T(self.LINE,44,GOLD,font=TITLE_FONT)).arrange(DOWN,buff=.6)
        self.add(line,T("biochemistrypedia.com",26,TEAL).move_to(P(0,-3)))
        self.finish()
