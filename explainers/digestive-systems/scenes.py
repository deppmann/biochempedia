"""Digestive systems: what told the stomach to start (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = an organ, gland or cell type (stomach, duodenum, pancreas, gallbladder, G cells, brainstem)
  ORANGE = food (a swallowed meal, fats and proteins)
  GREEN  = a secretion or response (acid juice, bicarbonate, enzymes, bile, the trypsin response)
  TEAL   = nerve route (vagus, nerve, acetylcholine receptors, the triggers of the cephalic phase)
  YELLOW = a hormone (gastrin, secretin, CCK) and the question mark of the opening
  RED    = cut, block, removed (cut vagus, atropine, 84% removed)
  GREY   = outlines, esophagus bar, blood bar, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tee(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def cross(center, s=0.2, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7))


def block(text, color=BLUE, w=3.0, h=1.4, size=28, label_at=None):
    box = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.14)
    lab = T(text, size, color)
    fit(lab, max_w=w - 0.3)
    lab.move_to(box if label_at is None else box.get_center() + np.array([label_at[0], label_at[1], 0]))
    return VGroup(box, lab)


def bar(x0, x1, y, color=GREY, h=0.32, op=0.35):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def dot(color=GREEN, r=0.11):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def scatter(n, x0, x1, y0, y1, color=GREEN, seed=1, r=0.11):
    rs = np.random.RandomState(seed)
    return VGroup(*[dot(color, r).move_to([rs.uniform(x0, x1), rs.uniform(y0, y1), 0]) for _ in range(n)])


def pulse(m, s=1.1):
    return m.animate(rate_func=there_and_back).scale(s)


def travel(dots, pts, rt=2.6, gap=0.4):
    pts = [np.array(p, float) for p in pts]
    for d in dots:
        d.move_to(pts[0])
    return [Succession(Wait(gap * i), MoveAlongPath(d, VMobject().set_points_as_corners(pts), run_time=rt,
                                                    rate_func=linear)) for i, d in enumerate(dots)]


# ---- the sham-feeding preparation, shared by s01 to s03 ------------------------------------
BY = 0.7                      # esophagus bar height
MOUTH = np.array([-5.2, BY, 0])
GAP_X = -1.9
STOM = np.array([4.1, BY, 0])
FLASK = np.array([4.1, -2.5, 0])


def prep(mid=False, fistula=False):
    d = {}
    d["mouth"] = bchip("mouth", BLUE, 30).move_to(MOUTH)
    d["bar1"] = bar(-4.3, -2.5, BY, h=0.45)
    d["mid"] = bar(-2.5, -1.3, BY, h=0.45)
    d["bar2"] = bar(-1.3, 2.2, BY, h=0.45)
    d["eso"] = T("esophagus", 24, GREY).move_to([1.0, BY + 0.6, 0])
    d["stom"] = block("stomach", BLUE, w=3.8, h=3.4, size=30, label_at=[0, 1.3]).move_to(STOM)
    d["neck"] = T("opening in the neck", 24, GREY).move_to([GAP_X, BY + 0.7, 0])
    if fistula:
        d["fline"] = Line(STOM + [0, -1.7, 0], FLASK + [0, 0.5, 0], color=GREY, stroke_width=6)
        d["flabel"] = T("gastric fistula", 24, GREY).move_to([2.6, -1.5, 0])
        d["flask"] = Rectangle(width=1.6, height=1.0, stroke_color=GREY, stroke_width=3).move_to(FLASK)
        d["fjuice"] = T("juice collected", 24, GREY).move_to(FLASK + [0, -0.78, 0])
    return d


def juice_fill(frac):
    h = max(0.02, 1.0 * frac)
    r = Rectangle(width=1.5, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.65)
    r.move_to([FLASK[0], FLASK[1] - 0.5 + h / 2, 0])
    return r


def food_run(food, scene, rt=1.4):
    """food chip travels the esophagus bar to the opening and drops out."""
    scene.play(food.animate.move_to([GAP_X, BY, 0]), run_time=rt, rate_func=linear)
    scene.play(food.animate.move_to([GAP_X, -1.7, 0]).set_opacity(0), run_time=0.9)


class S00Title(TitleCard):
    LESSON = "Digestive systems and nutrition"
    TITLE = "What told the stomach to start"


# ---------------------------------------------------------------------------------------------
class S01Dog(SpokenScene):
    def construct(self):
        t = prep()
        self.at("A dog eats")
        self.play(FadeIn(t["mouth"]), FadeIn(t["bar1"]), FadeIn(t["bar2"]), FadeIn(t["eso"]),
                  FadeIn(t["stom"]), run_time=0.9)
        food = bchip("food", ORANGE, 24).move_to(MOUTH + [1.3, 0, 0])
        self.play(FadeIn(food, shift=RIGHT * 0.2), run_time=0.5)
        self.at("falls out of an opening")
        self.play(food.animate.move_to([GAP_X, BY, 0]), FadeIn(t["neck"]), run_time=1.2, rate_func=linear)
        self.play(food.animate.move_to([GAP_X, -1.7, 0]).set_opacity(0), run_time=0.9)
        self.at("before it reaches")
        nofood = T("no food arrives", 24, RED).move_to([0.5, -0.1, 0])
        self.play(FadeIn(nofood, shift=UP * 0.1), run_time=0.6)
        self.at("pours out acid juice")
        dots = scatter(9, 3.0, 5.2, -0.1, 1.5, GREEN, seed=3)
        lab = T("acid juice", 26, GREEN).move_to([STOM[0], -0.6, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.12), FadeIn(lab), run_time=1.4)
        q = T("What told the stomach to start?", 34, YELLOW, font=TITLE_FONT).move_to([-3.0, 3.05, 0])
        box = bchip("?", GREY, 40).move_to([1.0, 3.0, 0])
        link = DashedLine([1.8, 2.85, 0], [3.4, 2.45, 0], color=YELLOW, stroke_width=4, dash_length=0.15)
        link.add_tip(tip_length=0.2)
        self.at("What told the stomach")
        self.play(FadeIn(q, shift=UP * 0.1), FadeIn(box), Create(link), run_time=0.9)
        self.play(Indicate(box[2], color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Sham(SpokenScene):
    def construct(self):
        t = prep(mid=True, fistula=True)
        for k in ("mouth", "bar1", "mid", "bar2", "eso", "stom"):
            self.add(t[k])
        self.at("opened the dog's esophagus")
        self.play(FadeOut(t["mid"]), FadeIn(t["neck"]), run_time=0.8)
        self.play(Indicate(t["neck"], color=YELLOW, scale_factor=1.1), run_time=0.5)
        food = bchip("food", ORANGE, 24).move_to(MOUTH + [1.3, 0, 0])
        self.at("so swallowed food")
        self.play(FadeIn(food), run_time=0.3)
        food_run(food, self, rt=1.2)
        self.at("A gastric fistula")
        self.play(Create(t["fline"]), FadeIn(t["flabel"]), FadeIn(t["flask"]), FadeIn(t["fjuice"]), run_time=1.0)
        note = T("expected: none", 24, GREY).move_to([1.5, -2.5, 0])
        self.at("flowed only when food")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.at("should make none")
        self.play(pulse(note, 1.1), run_time=0.6)
        self.at("Instead")
        x = Line(note.get_left() + [-0.1, 0, 0], note.get_right() + [0.1, 0, 0], color=RED, stroke_width=6)
        self.play(Create(x), run_time=0.4)
        delay = T("after some minutes", 24, TEXT).move_to([1.5, -2.5, 0])
        self.at("after a delay")
        self.play(FadeOut(note), FadeOut(x), FadeIn(delay), run_time=0.5)
        fill = juice_fill(0.02)
        self.add(fill)
        dots = scatter(8, 3.0, 5.2, -0.1, 1.5, GREEN, seed=5)
        self.at("abundant acid juice")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.1), run_time=1.0)
        drops = VGroup(*[dot() for _ in range(5)])
        anims = travel(drops, [STOM + [0, -0.4, 0], STOM + [0, -1.7, 0], FLASK + [0, 0.1, 0]], rt=1.4, gap=0.45)
        self.play(*anims, Transform(fill, juice_fill(0.8)), run_time=3.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Vagus(SpokenScene):
    def construct(self):
        t = prep(fistula=True)
        for k in ("mouth", "bar1", "bar2", "eso", "stom", "neck", "fline", "flabel", "flask", "fjuice"):
            self.add(t[k])
        fill = juice_fill(0.8)
        self.add(fill)
        dots = scatter(8, 3.0, 5.2, -0.1, 1.5, GREEN, seed=5)
        self.add(dots)
        stem = bchip("brainstem", BLUE, 26).move_to([1.0, 3.0, 0])
        vA = VMobject(color=TEAL, stroke_width=6).set_points_as_corners([[2.0, 3.25, 0], [3.9, 3.25, 0], [3.9, 2.4, 0]])
        vB = VMobject(color=TEAL, stroke_width=6).set_points_as_corners([[2.0, 2.75, 0], [3.4, 2.75, 0], [3.4, 2.4, 0]])
        vl = T("both vagus\nnerves", 24, TEAL, line_spacing=0.9).move_to([5.1, 2.95, 0])
        self.at("both vagus nerves")
        self.play(FadeIn(stem), Create(vA), Create(vB), FadeIn(vl), run_time=1.2)
        self.at("were cut")
        xa, xb = cross([2.8, 3.25, 0], 0.12), cross([2.8, 2.75, 0], 0.12)
        self.play(Create(xa), Create(xb), run_time=0.6)
        self.at("connect the brainstem")
        self.play(pulse(stem, 1.12), run_time=0.8)
        food = bchip("food", ORANGE, 24).move_to(MOUTH + [1.3, 0, 0])
        self.at("Now eating no longer")
        self.play(FadeOut(dots), FadeOut(fill), FadeIn(food), run_time=0.5)
        nj = T("no juice", 24, RED).move_to([2.45, -2.5, 0])
        food_run(food, self, rt=1.2)
        self.play(FadeIn(nj), run_time=0.4)
        ceph = bchip("cephalic phase", TEAL, 26).move_to([-3.9, -1.6, 0])
        sub = T("nerve-driven, in the dog", 22, GREY).move_to([-3.9, -2.2, 0])
        self.at("cephalic phase exists")
        self.play(FadeIn(ceph, shift=UP * 0.1), FadeIn(sub), run_time=0.7)
        row = VGroup(*[bchip(s, TEAL, 22) for s in ("sight", "smell", "taste", "chewing")]).arrange(RIGHT, buff=0.18)
        row.move_to([-3.4, 3.0, 0])
        rl = T("trigger the cephalic phase", 22, TEAL).move_to([-3.4, 2.4, 0])
        self.at("Sight smell taste")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in row], lag_ratio=0.45), run_time=2.0)
        self.play(FadeIn(rl), run_time=0.4)
        later = T("later phases: not ruled out", 28, GREY).move_to([-2.2, -3.1, 0])
        self.at("does not rule out later")
        self.play(FadeIn(later, shift=UP * 0.1), run_time=0.6)
        food2 = bchip("food", ORANGE, 24).move_to(STOM + [0, 0.2, 0])
        self.at("food is in the stomach")
        self.play(FadeOut(nj), FadeIn(food2, scale=0.5), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gastrin(SpokenScene):
    def construct(self):
        stom = block("stomach", BLUE, w=8.0, h=3.8, size=30, label_at=[0, 1.5]).move_to([0, 0.7, 0])
        blood = bar(-5.4, 5.4, -2.4, GREY, h=0.34, op=0.3)
        blab = T("blood", 24, GREY).move_to([-4.9, -2.95, 0])
        title = T("Later phases are partly chemical", 34, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("Later phases are partly")
        self.play(FadeIn(stom), Write(title), run_time=1.0)
        hdef = T("hormone: released into the blood, acts on distant target cells", 24, YELLOW).move_to([0, 3.2, 0])
        self.at("A hormone is a substance")
        self.play(FadeOut(title), FadeIn(hdef), Create(blood), FadeIn(blab), run_time=1.0)
        gchip = bchip("gastrin", YELLOW, 28).move_to([0, -1.75, 0])
        self.at("Gastrin is one")
        self.play(FadeIn(gchip, shift=UP * 0.15), run_time=0.6)
        gcell = bchip("G cells", BLUE, 26).move_to([-2.7, 1.1, 0])
        self.at("G cells in the stomach")
        self.play(FadeIn(gcell, scale=0.6), run_time=0.6)
        food = bchip("food, especially protein", ORANGE, 24).move_to([0.0, -0.3, 0])
        self.play(FadeIn(food, shift=RIGHT * 1.0), run_time=0.9)
        hd = VGroup(*[dot(YELLOW, 0.13) for _ in range(4)])
        self.at("release gastrin")
        self.add(hd)
        anims = travel(hd, [[-2.7, 0.7, 0], [-2.7, -2.4, 0], [3.0, -2.4, 0], [3.0, -0.5, 0]], rt=2.6, gap=0.4)
        self.play(*anims)
        acid = scatter(14, 2.4, 3.6, -0.9, 1.3, GREEN, seed=7)
        alab = T("more acid", 28, GREEN).move_to([2.9, 1.8, 0])
        self.at("more acid")
        self.play(FadeOut(hd), LaggedStart(*[FadeIn(d, scale=0.3) for d in acid], lag_ratio=0.08), FadeIn(alab), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Duodenum(SpokenScene):
    def construct(self):
        stom = block("stomach", BLUE, w=2.2, h=2.4, size=26, label_at=[0, 0.8]).move_to([-5.2, 0.2, 0])
        sacid = scatter(6, -5.9, -4.5, -0.8, 0.4, GREEN, seed=2)
        duo = block("duodenum", BLUE, w=3.0, h=1.4, size=26, label_at=[0, 0.38]).move_to([-0.4, 0.2, 0])
        chy = arr([-4.1, 0.2, 0], [-1.9, 0.2, 0], GREEN, w=6)
        chl = T("acid chyme", 22, GREEN).move_to([-3.0, 0.7, 0])
        note = T("duodenum: first part\nof the small intestine", 22, GREY, line_spacing=0.9).move_to([-4.4, -2.5, 0])
        self.at("Acid chyme then enters")
        self.play(FadeIn(stom), FadeIn(sacid), run_time=0.7)
        self.play(FadeIn(duo), GrowArrow(chy), FadeIn(chl), run_time=0.8)
        dacid = scatter(5, -1.4, 0.6, -0.3, 0.1, GREEN, seed=4)
        mvd = VGroup(*[dot() for _ in range(5)])
        mv = travel(mvd, [[-4.5, 0.2, 0], [-1.5, 0.2, 0]], rt=1.4, gap=0.2)
        self.at("first part of the small")
        self.play(FadeIn(note), run_time=0.5)
        self.play(*mv, FadeIn(dacid), run_time=2.0)

        panc = block("exocrine pancreas", BLUE, w=3.4, h=1.2, size=24).move_to([-0.4, 2.7, 0])
        gall = block("gallbladder", BLUE, w=3.0, h=1.2, size=26).move_to([-0.4, -2.5, 0])
        bld = Rectangle(width=0.34, height=5.2, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.3).move_to([3.0, 0.1, 0])
        blab = T("blood", 24, GREY).move_to([4.2, 0.1, 0])
        stubs = VGroup(bar(1.1, 2.83, 0.2, h=0.2, op=0.3), bar(1.3, 2.83, 2.7, h=0.2, op=0.3), bar(1.1, 2.83, -2.5, h=0.2, op=0.3))
        sec = bchip("secretin", YELLOW, 24).move_to([4.7, 1.6, 0])
        self.at("Its lining releases")
        self.play(FadeIn(panc), FadeIn(gall), Create(bld), FadeIn(blab), FadeIn(stubs), run_time=1.0)
        sd = VGroup(*[dot(YELLOW, 0.13) for _ in range(3)])
        self.play(FadeIn(sec, shift=LEFT * 0.2), run_time=0.4)
        self.add(sd)
        self.play(*travel(sd, [[0.7, 0.2, 0], [3.0, 0.2, 0], [3.0, 2.7, 0], [1.3, 2.7, 0]], rt=2.0, gap=0.3), run_time=2.6)
        a1 = arr([-1.2, 2.1, 0], [-1.2, 0.95, 0], GREEN, w=6)
        l1 = T("bicarbonate-rich\nfluid", 22, GREEN, line_spacing=0.9).move_to([-2.6, 1.65, 0])
        self.at("pancreatic duct cells")
        self.play(pulse(panc, 1.06), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.6)
        self.at("which neutralizes")
        self.play(FadeOut(dacid), FadeOut(mvd), FadeOut(sd), run_time=1.0)

        fp = bchip("fats, proteins", ORANGE, 22).move_to([-3.3, -1.6, 0])
        fa = arr([-2.5, -1.3, 0], [-1.7, -0.3, 0], ORANGE, w=4, tip=0.15)
        self.at("Fats and proteins")
        self.play(FadeIn(fp, shift=UP * 0.1), GrowArrow(fa), run_time=0.7)
        cck = bchip("CCK", YELLOW, 24).move_to([4.7, -1.3, 0])
        cd = VGroup(*[dot(YELLOW, 0.13) for _ in range(3)])
        cd2 = VGroup(*[dot(YELLOW, 0.13) for _ in range(3)])
        self.at("bring out")
        self.play(FadeIn(cck, shift=LEFT * 0.2), run_time=0.4)
        self.add(cd, cd2)
        a2 = arr([0.4, 2.1, 0], [0.4, 0.95, 0], GREEN, w=6)
        l2 = T("enzymes", 22, GREEN).move_to([1.55, 1.5, 0])
        self.at("drives the pancreas")
        self.play(*travel(cd, [[0.7, 0.2, 0], [3.0, 0.2, 0], [3.0, 2.7, 0], [1.3, 2.7, 0]], rt=2.0, gap=0.3),
                  *travel(cd2, [[0.7, 0.2, 0], [3.0, 0.2, 0], [3.0, -2.5, 0], [1.1, -2.5, 0]], rt=2.3, gap=0.3),
                  run_time=2.6)
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.6)
        a3 = arr([-0.4, -1.9, 0], [-0.4, -0.55, 0], GREEN, w=6)
        l3 = T("bile", 22, GREEN).move_to([-1.1, -1.2, 0])
        self.at("to contract and release")
        self.play(pulse(gall, 1.08), run_time=0.7)
        self.play(GrowArrow(a3), FadeIn(l3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Block(SpokenScene):
    def construct(self):
        tag = T("healthy human volunteers, one dose of CCK-8", 24, GREY).move_to([0, 3.35, 0])
        cck = bchip("CCK-8", YELLOW, 30).move_to([-5.3, 2.2, 0])
        nerve = bchip("nerve", TEAL, 28).move_to([-3.0, 2.2, 0])
        rec = bchip("acetylcholine receptors", TEAL, 24).move_to([0.4, 2.2, 0])
        panc = block("pancreas", BLUE, w=2.4, h=1.1, size=28).move_to([5.0, 2.2, 0])
        a1 = arr(cck.get_right(), nerve.get_left(), YELLOW, w=5, tip=0.18)
        a2 = arr(nerve.get_right(), rec.get_left(), TEAL, w=5, tip=0.18)
        a3 = arr(rec.get_right(), panc.get_left(), TEAL, w=5, tip=0.18)
        tl = T("trypsin", 22, GREEN).next_to(panc, DOWN, buff=0.12)
        self.at("Nerves and hormones overlap")
        self.play(FadeIn(cck, shift=RIGHT * 0.2), FadeIn(nerve), FadeIn(rec), FadeIn(panc), FadeIn(tl), run_time=0.8)
        self.play(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=0.8)
        self.at("Healthy human volunteers")
        self.play(FadeIn(tag), run_time=0.5)
        x0, L = -3.3, 7.0
        cap = T("pancreatic trypsin response (schematic bars)", 22, GREY).move_to([0, -0.05, 0])
        lab1 = T("CCK-8 alone", 26, TEXT).move_to([-5.0, -1.0, 0])
        lab2 = T("with atropine", 26, TEXT).move_to([-5.0, -2.1, 0])
        b1 = Rectangle(width=L, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.7).move_to([x0 + L / 2, -1.0, 0])
        self.at("at one dose")
        self.play(FadeIn(cap), FadeIn(lab1), GrowFromEdge(b1, LEFT), run_time=1.0)
        atro = bchip("atropine", RED, 28).move_to([0.4, 0.95, 0])
        self.at("Atropine blocks")
        self.play(FadeIn(atro, shift=UP * 0.1), run_time=0.5)
        self.play(Create(tee(atro.get_top(), rec.get_bottom(), RED)), run_time=0.6)
        self.at("many glands")
        self.play(pulse(rec, 1.1), run_time=0.6)
        rem = 0.16 * L
        b2 = Rectangle(width=L, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.7).move_to([x0 + L / 2, -2.1, 0])
        self.at("With atropine")
        self.play(FadeIn(lab2), GrowFromEdge(b2, LEFT), run_time=0.8)
        oth = DashedLine([-5.3, 2.55, 0], [-5.3, 2.95, 0], color=YELLOW, stroke_width=4)
        oth2 = VMobject(color=YELLOW, stroke_width=4).set_points_as_corners([[-5.3, 2.58, 0], [-5.3, 2.95, 0], [5.0, 2.95, 0], [5.0, 2.8, 0]])
        oth2 = DashedVMobject(oth2, num_dashes=60)
        othl = T("other routes", 22, YELLOW)
        othl = VGroup(Rectangle(width=othl.width + 0.3, height=othl.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1), othl).move_to([0.4, 2.95, 0])
        left = T("left under atropine", 22, GREEN).move_to([-2.6, -2.78, 0])
        gone = Rectangle(width=L - rem, height=0.8, stroke_color=RED, stroke_width=3, fill_color=RED,
                         fill_opacity=0.15).move_to([x0 + rem + (L - rem) / 2, -2.1, 0])
        gl = T("84% removed", 24, RED).move_to(gone)
        self.at("fell by")
        self.play(b2.animate.stretch_to_fit_width(rem, about_edge=LEFT), FadeIn(gone), FadeIn(gl), FadeIn(left), Create(oth2), FadeIn(othl), run_time=1.2)
        self.at("much of the hormone's effect")
        ctitle = T("a large cholinergic component", 22, TEAL).move_to([-3.2, 1.2, 0])
        self.play(FadeIn(ctitle), pulse(nerve, 1.15), pulse(rec, 1.08), run_time=0.9)
        rule = T("Block one route, then measure what remains.", 30, font=TITLE_FONT).move_to([0, -3.3, 0])
        self.at("Block")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Block one route, then measure what remains."
