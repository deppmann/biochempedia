"""Filter far more, take most back: one mammalian nephron  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = water
  YELLOW = salt (sodium chloride) and the salty tissue
  PINK   = blood and blood vessels
  GREEN  = filtrate and the tube (nephron segments)
  ORANGE = antidiuretic hormone (ADH) and its water channels
  RED    = the question, the unknown, a blocked path
  GREY   = outlines, labels, de-emphasized
All anatomy is schematic blocks and bars, not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E0688A"
ORANGE = "#F29E4C"
SW = 14   # tube stroke


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color, x, y, op=0.2, sw=3):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def lines(txt, size=24, color=GREY, **kw):
    return VGroup(*[T(s, size, color, **kw) for s in txt.split("\n")]).arrange(DOWN, buff=0.08)


def tube(a, b, color=GREEN, sw=SW):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=color, stroke_width=sw, cap_style=CapStyleType.ROUND)


def cross(x, y, s=0.22):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=RED, stroke_width=6),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=RED, stroke_width=6))


# nephron geometry (schematic, not to scale)
CAPX, CAPY = -5.2, 2.2
PX0, PX1 = -4.5, -1.8            # proximal tube x
DX, AX = -1.8, -0.6              # descending / ascending limb x
TOPY, BOTY = 2.2, -2.5
DIS1 = 1.5                       # distal tube end x
CDX = 2.6                        # collecting duct x
CDBOT = -3.0


def nephron(op=1.0):
    cap = box(1.3, 1.3, GREEN, CAPX, CAPY, op=0.1)
    glom = Circle(radius=0.3, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.5).move_to([CAPX, CAPY, 0])
    prox = tube([PX0, TOPY], [PX1, TOPY])
    desc = tube([DX, TOPY], [DX, BOTY], sw=8)
    bend = tube([DX, BOTY], [AX, BOTY], sw=8)
    asc = VGroup(tube([AX, BOTY], [AX, -0.8], sw=8), tube([AX, -0.8], [AX, TOPY], sw=20))
    dis = tube([AX, TOPY], [CDX, TOPY])
    cd = tube([CDX, TOPY], [CDX, CDBOT])
    parts = VGroup(cap, glom, prox, desc, bend, asc, dis, cd)
    parts.set_opacity(op) if op < 1 else None
    return dict(cap=cap, glom=glom, prox=prox, desc=desc, bend=bend, asc=asc, dis=dis, cd=cd, all=parts)


def tissue(x0, x1, y0=1.7, y1=-3.0, n=10, lo=0.02, hi=0.40):
    """Salty tissue: yellow, stronger toward the bottom (the papilla end)."""
    h = (y0 - y1) / n
    rs = VGroup()
    for i in range(n):
        r = Rectangle(width=x1 - x0, height=h + 0.005, stroke_width=0, fill_color=YELLOW,
                      fill_opacity=lo + (hi - lo) * i / (n - 1)).move_to([(x0 + x1) / 2, y0 - h * (i + 0.5), 0])
        rs.add(r)
    return rs


class S00Title(TitleCard):
    LESSON = "The Kidney"
    TITLE = "Filter Far More, Take Most Back"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        base, H = -3.0, 4.4
        ax = Line([-6.0, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        tag = T("adult human, per day (not to scale)", 26, GREY).to_edge(UP, buff=0.45)
        self.at("In an adult human")
        self.play(FadeIn(tag), Create(ax), run_time=0.6)
        bar = Rectangle(width=1.8, height=H, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
        bar.move_to([-1.2, base + H / 2, 0])
        bl = lines("filtered:\nabout 180 L\nof plasma", 26, BLUE).next_to(bar, LEFT, buff=0.4)
        self.at("filter about")
        self.play(GrowFromEdge(bar, DOWN), run_time=1.3)
        self.play(FadeIn(bl, shift=RIGHT * 0.1), run_time=0.5)
        four = T("about 4 x the water in the whole body", 26, BLUE).move_to([-1.2, 2.25, 0])
        self.at("four times")
        self.play(FadeIn(four, shift=DOWN * 0.1), run_time=0.7)
        sl = Rectangle(width=1.8, height=0.12, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
        sl.move_to([3.4, base + 0.06, 0])
        ul = lines("urine:\n1 to 2 L", 26, BLUE).move_to([3.4, -1.9, 0])
        self.at("one or two")
        self.play(FadeIn(sl), FadeIn(ul, shift=UP * 0.1), run_time=0.7)
        q = chip("?", RED, 44, pad=0.3).move_to([1.2, -0.4, 0])
        ql = lines("where does\nthe rest go?", 30, RED).move_to([1.7, 1.2, 0])
        self.at("Where does the rest go")
        self.play(FadeIn(q, scale=0.8), FadeIn(ql), run_time=0.8)
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=0.7)
        # the answer: most goes back into the blood, a sliver leaves as urine
        ret = Rectangle(width=1.8, height=H - 0.12, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
        ret.move_to([-4.0, base + (H - 0.12) / 2, 0])
        retbox = SurroundingRectangle(ret, color=PINK, buff=0.15, stroke_width=4)
        retl = lines("back into\nthe blood", 28, PINK).next_to(retbox, RIGHT, buff=0.3)
        self.at("Back into the blood")
        self.play(FadeOut(q), FadeOut(ql), FadeOut(bl), FadeOut(four), run_time=0.4)
        self.play(ReplacementTransform(bar, ret), run_time=1.2)
        self.play(Create(retbox), FadeIn(retl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Filter(SpokenScene):
    def construct(self):
        cap = RoundedRectangle(corner_radius=0.15, width=3.4, height=3.0, stroke_color=GREEN, stroke_width=3,
                               fill_color=GREEN, fill_opacity=0.08).move_to([-2.6, 0.6, 0])
        glom = box(2.0, 1.8, PINK, -2.6, 0.6, op=0.25)
        gl = T("glomerulus", 24, PINK).move_to(glom)
        capl = T("Bowman's capsule", 24, GREEN).move_to([-2.6, 2.5, 0])
        tube_path = VMobject(color=GREEN, stroke_width=SW)
        tube_path.set_points_as_corners([[-0.9, 0.6, 0], [0.6, 0.6, 0], [0.6, -0.7, 0], [4.9, -0.7, 0]])
        tube_tip = arr([4.4, -0.7, 0], [5.3, -0.7, 0], GREEN, 6)
        tubel = T("long tube", 24, GREEN).move_to([3.0, -0.2, 0])
        aff = arr([-6.2, 1.1, 0], [-3.6, 1.1, 0], PINK, 7)
        affl = lines("afferent\narteriole", 24, PINK).move_to([-5.3, 1.75, 0])
        eff_v = Line([-2.6, -0.3, 0], [-2.6, -1.6, 0], color=PINK, stroke_width=7)
        eff_h = arr([-2.6, -1.6, 0], [5.3, -1.6, 0], PINK, 7)
        effl = lines("efferent\narteriole", 24, PINK).move_to([-4.0, -1.9, 0])
        perl = T("peritubular capillaries", 24, PINK).move_to([2.0, -2.2, 0])
        fil = VGroup(arr([-1.55, 0.95, 0], [-1.05, 0.95, 0], GREEN, 5, 0.15),
                     arr([-1.55, 0.25, 0], [-1.05, 0.25, 0], GREEN, 5, 0.15))

        self.at("The working unit")
        self.play(FadeIn(cap), FadeIn(capl), run_time=0.6)
        self.play(FadeIn(glom), FadeIn(gl), Create(tube_path), FadeIn(tubel), run_time=1.0)
        self.at("afferent arteriole")
        self.play(GrowArrow(aff), FadeIn(affl), run_time=0.8)
        self.at("The efferent arteriole")
        self.play(Create(eff_v), GrowArrow(eff_h), FadeIn(effl), FadeIn(perl), run_time=1.2)
        self.at("Afferent in")
        self.play(Indicate(aff, color=PINK, scale_factor=1.12), run_time=0.7)
        self.at("efferent out")
        self.play(Indicate(eff_h, color=PINK, scale_factor=1.04), run_time=0.7)
        self.at("Blood pressure pushes")
        self.play(FadeIn(fil, shift=RIGHT * 0.15), run_time=0.8)
        self.play(FadeIn(tube_tip), run_time=0.2)
        c1 = chip("water", BLUE, 24).move_to([1.7, 1.5, 0])
        c2 = chip("small solutes", YELLOW, 24).move_to([4.5, 1.5, 0])
        self.at("holds water")
        self.play(FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        n1 = chip("no blood cells", GREY, 24).move_to([1.7, 2.55, 0])
        n2 = chip("very little protein", GREY, 24).move_to([4.7, 2.55, 0])
        self.at("but no blood cells")
        self.play(FadeIn(n1, shift=UP * 0.1), FadeIn(n2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tube(SpokenScene):
    def construct(self):
        nf = nephron()
        cap, glom, prox, desc, bend, asc, dis, cd = [nf[k] for k in ("cap", "glom", "prox", "desc", "bend", "asc", "dis", "cd")]
        capl = lines("Bowman's\ncapsule", 24, GREEN).move_to([CAPX, 0.95, 0])
        pl = T("proximal tubule", 24, GREEN).move_to([-3.15, 2.85, 0])
        ll = T("loop of Henle", 24, GREEN).move_to([-1.2, -3.1, 0])
        dl = T("distal tubule", 24, GREEN).move_to([0.6, 2.85, 0])
        cl = lines("collecting\nduct", 24, GREEN).move_to([4.0, -0.3, 0])
        self.at("The filtrate flows on")
        self.play(FadeIn(cap), FadeIn(glom), FadeIn(capl), run_time=0.7)
        path = VMobject()
        path.set_points_as_corners([[CAPX + 0.2, CAPY, 0], [PX1, TOPY, 0], [DX, BOTY, 0], [AX, BOTY, 0], [AX, TOPY, 0],
                                    [CDX, TOPY, 0], [CDX, CDBOT, 0]])
        dot = Dot(radius=0.14, color=TEXT).move_to([CAPX + 0.2, CAPY, 0])
        self.add(dot)
        self.play(Create(prox), FadeIn(pl), dot.animate.move_to([PX1, TOPY, 0]), run_time=1.0, rate_func=linear)
        self.at("the loop of")
        lp = VMobject()
        lp.set_points_as_corners([[DX, TOPY, 0], [DX, BOTY, 0], [AX, BOTY, 0], [AX, TOPY, 0]])
        self.play(Succession(Create(desc, run_time=0.7), Create(bend, run_time=0.2), Create(asc, run_time=0.7)),
                  MoveAlongPath(dot, lp), FadeIn(ll), run_time=1.6, rate_func=linear)
        self.at("the distal tubule")
        self.play(Create(dis), FadeIn(dl), dot.animate.move_to([CDX, TOPY, 0]), run_time=0.7, rate_func=linear)
        self.at("and the collecting duct")
        self.play(Create(cd), FadeIn(cl), dot.animate.move_to([CDX, CDBOT + 0.2, 0]), run_time=0.9, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.3)
        # reabsorption: tube back into the blood
        blood = Line([-4.0, 1.1, 0], [-2.3, 1.1, 0], color=PINK, stroke_width=10)
        bl = T("blood", 22, PINK).move_to([-3.15, 0.7, 0])
        self.at("or takes back")
        self.play(Create(blood), FadeIn(bl), run_time=0.7)
        up = lines("proximal tubule,\nin mammals:\nabout 60 to 70%\nof filtered sodium\nreabsorbed", 24, GREEN).move_to([4.7, 1.55, 0])
        a_na = arr([-3.7, 1.95, 0], [-3.7, 1.3, 0], YELLOW, 6, 0.16)
        self.at("of filtered sodium")
        self.play(GrowArrow(a_na), FadeIn(up), run_time=0.8)
        a_w = arr([-3.15, 1.95, 0], [-3.15, 1.3, 0], BLUE, 6, 0.16)
        wl = T("water follows", 24, BLUE).move_to([4.7, -2.5, 0])
        self.at("Water follows")
        self.play(GrowArrow(a_w), FadeIn(wl), run_time=0.7)
        a_g = arr([-2.6, 1.95, 0], [-2.6, 1.3, 0], GREY, 6, 0.16)
        gl = lines("almost all glucose\nand amino acids", 24, GREY).move_to([4.7, -1.6, 0])
        self.at("almost all the filtered glucose")
        self.play(GrowArrow(a_g), FadeIn(gl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dim_nephron(op=0.3):
    nf = nephron()
    nf["all"].set_opacity(op)
    return nf


class S04Loop(SpokenScene):
    def construct(self):
        nf = dim_nephron(0.3)
        self.add(nf["all"])
        for k in ("desc", "bend", "asc"):
            nf[k].set_opacity(1)
        sch = lines("schematic layout,\nnot anatomy", 22, GREY).move_to([4.9, 3.0, 0])
        self.add(sch)
        self.at("Now the loop of Henle")
        self.play(Indicate(VGroup(nf["desc"], nf["bend"], nf["asc"]), color=GREEN, scale_factor=1.03), run_time=0.8)
        # flow arrows, one per lane
        fd = arr([DX, 1.3, 0], [DX, 0.7, 0], TEXT, 5, 0.16)
        fa = arr([AX, -1.3, 0], [AX, -0.7, 0], TEXT, 5, 0.16)
        self.at("a hairpin")
        self.play(GrowArrow(fd), GrowArrow(fa), run_time=0.7)
        tal = lines("thick ascending\nlimb", 24, GREEN).move_to([1.0, 1.6, 0])
        self.at("The thick ascending limb")
        self.play(FadeIn(tal), run_time=0.5)
        salts = VGroup(*[arr([AX + 0.2, y, 0], [AX + 0.9, y, 0], YELLOW, 6, 0.16) for y in (0.5, 0.0, -0.5)])
        self.at("moves sodium chloride out")
        self.play(LaggedStart(*[GrowArrow(s) for s in salts], lag_ratio=0.25), run_time=1.3)
        wblock = VGroup(arr([AX + 0.2, 1.0, 0], [AX + 0.9, 1.0, 0], BLUE, 6, 0.16), cross(AX + 0.6, 1.0))
        self.at("nearly impermeable to water")
        self.play(FadeIn(wblock), run_time=0.6)
        sw = lines("salt leaves,\nwater stays", 24, YELLOW).move_to([4.9, 1.3, 0])
        self.at("Salt leaves")
        self.play(FadeIn(sw), run_time=0.5)
        t = tissue(-2.6, 3.4)
        t.set_z_index(-1)
        self.at("gets saltier")
        self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.12), run_time=1.5)
        self.play(FadeOut(sw), run_time=0.3)
        dl = lines("thin descending\nlimb", 24, GREEN).move_to([-4.1, 0.4, 0])
        self.at("The thin descending limb")
        self.play(FadeIn(dl), run_time=0.5)
        wats = VGroup(*[arr([DX - 0.15, y, 0], [DX - 0.75, y, 0], BLUE, 6, 0.16) for y in (0.1, -0.7, -1.5)])
        self.at("Water leaves it by osmosis")
        self.play(LaggedStart(*[GrowArrow(s) for s in wats], lag_ratio=0.25), run_time=1.1)
        ow = lines("water leaves\nby osmosis", 24, BLUE).move_to([4.9, 1.3, 0])
        self.play(FadeIn(ow), run_time=0.4)
        self.at("opposite directions")
        cc = lines("countercurrent:\nopposite lanes", 24, GREEN).move_to([4.9, -0.2, 0])
        self.play(FadeOut(ow), FadeIn(cc), Indicate(fd, color=TEXT), Indicate(fa, color=TEXT), run_time=0.9)
        self.at("In rat kidney slices")
        ra = arr([3.85, 1.6, 0], [3.85, -2.8, 0], YELLOW, 7, 0.22)
        rl = lines("osmolality\nrises (rat\nkidney slices)", 24, YELLOW).move_to([5.1, -0.9, 0])
        top = T("cortex", 24, GREY).move_to([5.1, 1.7, 0])
        bot = T("papilla", 24, GREY).move_to([5.1, -2.9, 0])
        self.play(FadeOut(cc), run_time=0.3)
        self.play(GrowArrow(ra), FadeIn(rl), FadeIn(top), FadeIn(bot), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Duct(SpokenScene):
    def construct(self):
        # start from the loop picture: dim nephron, salty tissue
        nf = dim_nephron(0.3)
        t = tissue(-2.6, 3.4)
        t.set_z_index(-1)
        self.add(nf["all"], t)
        # target layout: the duct fills the height at x = -1.25
        DXC = -1.25
        tis2 = tissue(-3.9, 1.4, y0=2.9, y1=-3.0)
        tis2.set_z_index(-1)
        duct = RoundedRectangle(corner_radius=0.1, width=0.9, height=5.9, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.12).move_to([DXC, -0.05, 0])
        dl = lines("collecting\nduct", 24, GREEN).move_to([-5.2, 2.3, 0])
        self.at("The collecting duct runs")
        self.play(FadeOut(nf["all"]), FadeOut(t), FadeIn(tis2), FadeIn(duct), FadeIn(dl), run_time=1.1)
        flow = arr([DXC, 2.7, 0], [DXC, 2.0, 0], GREEN, 6, 0.18)
        self.play(GrowArrow(flow), run_time=0.4)
        ys = (1.7, 0.7, -0.3, -1.3, -2.3)
        case = chip("with ADH", ORANGE, 30).move_to([4.2, 2.6, 0])
        chans = VGroup(*[Rectangle(width=0.34, height=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([DXC + s * 0.45, y, 0])
                         for y in ys for s in (-1, 1)])
        wat = VGroup(*[arr([DXC + s * 0.5, y, 0], [DXC + s * 1.3, y, 0], BLUE, 6, 0.16) for y in ys for s in (-1, 1)])
        res1 = lines("water leaves\nby osmosis;\nurine concentrated", 24, YELLOW).move_to([4.2, 1.3, 0])
        self.at("With anti")
        self.play(FadeIn(case, shift=DOWN * 0.1), run_time=0.5)
        self.at("insert stored water channels")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in chans], lag_ratio=0.1), run_time=1.1)
        self.at("Water leaves by osmosis")
        self.play(LaggedStart(*[GrowArrow(w) for w in wat], lag_ratio=0.08), FadeIn(res1), run_time=1.2)
        # reset to neutral and show the other case in the same beat
        case2 = chip("without ADH", GREY, 30).move_to([4.2, 2.6, 0])
        res2 = lines("duct nearly\nwater-tight;\ndilute urine", 24, BLUE).move_to([4.2, 1.3, 0])
        self.at("the duct stays nearly")
        self.play(FadeOut(chans), FadeOut(wat), FadeOut(res1), ReplacementTransform(case, case2), run_time=0.6)
        self.play(FadeIn(res2), run_time=0.5)
        # numbers
        base = -3.0
        k = 3.3 / 1200
        b1 = Rectangle(width=1.1, height=290 * k, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([3.5, base + 290 * k / 2, 0])
        b2 = Rectangle(width=1.1, height=1200 * k, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.4).move_to([5.1, base + 1200 * k / 2, 0])
        n1 = M("290", 24, GREY).next_to(b1, UP, buff=0.12)
        n2 = M("1,200", 24, YELLOW).next_to(b2, UP, buff=0.12)
        hd = lines("water-deprived\nadult human\n(mOsm/kg)", 22, GREY).move_to([4.3, 1.5, 0])
        bl1 = T("plasma", 22, GREY).move_to([3.5, -3.3, 0])
        bl2 = T("urine", 22, YELLOW).move_to([5.1, -3.3, 0])
        self.at("adult human can make")
        self.play(FadeOut(res2), FadeOut(case2), FadeIn(hd), run_time=0.5)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(n2), FadeIn(bl2), run_time=1.0)
        self.at("Plasma is about")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(n1), FadeIn(bl1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        title = T("three verbs, one nephron", 34, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        xs = (-4.2, 0.0, 4.2)

        def card(x, name, a_from, a_to, desc, up):
            hd = T(name, 34, GREEN, font=TITLE_FONT).move_to([x, 2.1, 0])
            bl = Line([x - 1.4, 1.1, 0], [x + 1.4, 1.1, 0], color=PINK, stroke_width=12)
            tb = Line([x - 1.4, -0.4, 0], [x + 1.4, -0.4, 0], color=GREEN, stroke_width=12)
            blt = T("blood", 22, PINK).move_to([x, 1.55, 0])
            tbt = T("tube", 22, GREEN).move_to([x, -0.85, 0])
            ar = arr([x, a_from, 0], [x, a_to, 0], YELLOW, 8, 0.25)
            d = lines(desc, 24, GREY).move_to([x, -1.9, 0])
            return hd, VGroup(bl, tb, blt, tbt), ar, d

        cards = [card(xs[0], "filtration", 0.9, -0.2, "fluid out of the\nblood into the tube", False),
                 card(xs[1], "reabsorption", -0.2, 0.9, "substances from the\ntube back into the blood", True),
                 card(xs[2], "secretion", 0.9, -0.2, "substances from the\nblood into the tube", False)]
        self.at("Three verbs")
        self.play(FadeIn(title), *[FadeIn(c[1]) for c in cards], run_time=0.6)
        self.at("Filtration pushes")
        self.play(FadeIn(cards[0][0]), GrowArrow(cards[0][2]), FadeIn(cards[0][3]), run_time=1.0)
        self.at("Reabsorption moves")
        self.play(FadeIn(cards[1][0]), GrowArrow(cards[1][2]), FadeIn(cards[1][3]), run_time=1.0)
        self.at("Secretion moves")
        self.play(FadeIn(cards[2][0]), GrowArrow(cards[2][2]), FadeIn(cards[2][3]), run_time=1.0)
        ban = chip("collecting duct: sets final water and salt in urine (mammals)", GOLD, 26).move_to([0, -3.0, 0])
        self.at("the collecting duct sets")
        self.play(FadeIn(ban, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The kidney filters far more than it lets go."
