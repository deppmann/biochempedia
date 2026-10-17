"""DNA replication: why halfway? (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PURPLE = old, heavy strand / heavy DNA band
  BLUE   = new, light strand / light DNA band
  TEAL   = hybrid DNA band (one old strand, one new strand)
  YELLOW = what was observed / the highlighted thing / the question
  GREEN  = model survives (fits the data)
  RED    = model ruled out
  GREY   = tubes, outlines, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
OLD, NEW, HYB = PURPLE, BLUE, TEAL


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bar(colors, w, h):
    """One strand: a row of coloured segments (a single colour is one segment)."""
    if isinstance(colors, str):
        colors = [colors]
    n = len(colors)
    rs = [Rectangle(width=w / n, height=h, stroke_width=0, fill_color=c, fill_opacity=1) for c in colors]
    return VGroup(*rs).arrange(RIGHT, buff=0)


def duplex(top, bottom, w=2.6, h=0.2, gap=0.08):
    """Two strands drawn as bars. Each argument is a colour or a list of segment colours."""
    t, b = bar(top, w, h), bar(bottom, w, h)
    g = VGroup(t, b).arrange(DOWN, buff=gap)
    g.top_s, g.bot_s = t, b
    return g


PATCH_A = ([OLD, NEW, NEW, OLD, NEW, OLD], [NEW, OLD, OLD, NEW, OLD, NEW])      # half old, scattered
PATCH_Q = ([OLD, NEW, NEW, NEW], [NEW, NEW, OLD, NEW])                          # a quarter old


def make_tube(h=3.6, w=1.7):
    t = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.06)
    t.ypos = lambda f: t.get_top()[1] - 0.4 + (-(h - 0.8)) * f
    return t


def band(tube, frac, color, thick=0.3, wfac=1.0):
    return Rectangle(width=(tube.width - 0.2) * wfac, height=thick, stroke_width=0, fill_color=color,
                     fill_opacity=0.92).move_to([tube.get_center()[0], tube.ypos(frac), 0])


def side_label(text, color, tube, frac, size=26):
    t = T(text, size, color)
    return t.move_to([tube.get_right()[0] + 0.25 + t.width / 2, tube.ypos(frac), 0])


def cross(mob, color=RED, pad=0.1):
    x = VGroup(Line(mob.get_corner(UL) + [-pad, pad, 0], mob.get_corner(DR) + [pad, -pad, 0]),
               Line(mob.get_corner(UR) + [pad, pad, 0], mob.get_corner(DL) + [-pad, -pad, 0]))
    return x.set_color(color).set_stroke(width=8)


def status(text, color, x, y=-3.15):
    return chip(text, color, size=24, pad=0.15).move_to([x, y, 0])


COLX = [-4.3, 0.0, 4.3]


def title(text, x, color=TEXT, y=3.1, size=30):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def dup_set(kind, w=2.6):
    """daughters of one copying round from a heavy parent, for each model."""
    if kind == "con":
        return [duplex(OLD, OLD, w), duplex(NEW, NEW, w)]
    if kind == "semi":
        return [duplex(OLD, NEW, w), duplex(OLD, NEW, w)]
    return [duplex(*PATCH_A, w=w), duplex(*PATCH_A, w=w)]


NAMES = {"con": "Conservative", "semi": "Semiconservative", "dis": "Dispersive"}
KINDS = ["con", "semi", "dis"]


class S00Title(TitleCard):
    LESSON = "DNA replication"
    TITLE = "Why halfway? Counting old strands"


# ---------------------------------------------------------------------------------------------
class S01Halfway(SpokenScene):
    """heavy band -> spin in CsCl -> after one generation one band halfway -> why?"""

    def construct(self):
        tube = make_tube(5.8).move_to([-1.6, -0.1, 0])
        lab_l = side_label("light", NEW, tube, 0)
        lab_h = side_label("heavy", OLD, tube, 1)
        self.at("grew")
        self.play(FadeIn(tube), FadeIn(lab_l), FadeIn(lab_h), run_time=0.6)

        head = T("E. coli grown in heavy nitrogen", 26, GREY).move_to([4.0, 2.2, 0])
        dup = duplex(OLD, OLD, w=3.6, h=0.3, gap=0.12).move_to([4.0, 0.9, 0])
        dlab = T("heavy DNA", 28, OLD).next_to(dup, DOWN, buff=0.3)
        hb = band(tube, 1, OLD, 0.35)
        self.at("all of its DNA was heavy")
        self.play(FadeIn(head), FadeIn(dup), FadeIn(dlab), GrowFromCenter(hb), run_time=0.8)

        nit = chip("ordinary nitrogen added", NEW, 26).move_to([4.0, -1.4, 0])
        self.at("ordinary nitrogen")
        self.play(FadeIn(nit, shift=UP * 0.2), run_time=0.6)

        spin = T("spun in\ncaesium chloride", 26, GREY).move_to([-4.6, 1.9, 0])
        self.at("spun")
        self.play(FadeIn(spin), run_time=0.5)

        lab_m = side_label("hybrid", HYB, tube, 0.5)
        self.at("settle in separate bands")
        self.play(FadeIn(lab_m), run_time=0.5)

        # after one generation: the heavy band becomes a single hybrid band halfway
        gen = T("after one generation", 28, YELLOW).move_to([4.0, 2.2, 0])
        slots = VGroup(*[RoundedRectangle(corner_radius=0.14, width=1.6, height=0.9, stroke_color=YELLOW,
                                          stroke_width=3, fill_opacity=0) for _ in range(2)]).arrange(RIGHT, buff=0.5).move_to(dup)
        qs = VGroup(*[T("?", 44, YELLOW, weight=BOLD).move_to(s) for s in slots])
        mb = band(tube, 0.5, HYB, 0.35)
        self.at("After one generation")
        self.play(ReplacementTransform(hb, mb), ReplacementTransform(head, gen),
                  ReplacementTransform(dup, slots), FadeIn(qs), FadeOut(dlab), FadeOut(nit), run_time=1.0)

        self.at("halfway between")
        self.play(Indicate(mb, color=YELLOW, scale_factor=1.25), run_time=0.9)
        q = T("?", 110, YELLOW, weight=BOLD).move_to([-3.7, tube.ypos(0.5), 0])
        self.at("Why halfway")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def build_models_cols(with_parent=True):
    """columns of s02 (also the starting point of s03). returns dict of mobjects."""
    d = {}
    for k, x in zip(KINDS, COLX):
        d[k + "_title"] = title(NAMES[k], x, y=3.0, size=28)
        ds = dup_set(k)
        ds[0].move_to([x, -0.35, 0]); ds[1].move_to([x, -1.35, 0])
        d[k + "_d"] = ds
        if with_parent:
            d[k + "_p"] = duplex(OLD, OLD).move_to([x, 1.65, 0])
    return d


class S02Models(SpokenScene):
    def construct(self):
        d = build_models_cols()
        desc = {"con": "old pair stays whole", "semi": "one old, one new", "dis": "patchwork"}
        parents = VGroup(*[d[k + "_p"] for k in KINDS])
        plab = T("heavy parent", 24, OLD).move_to([0, 2.35, 0])
        self.at("Three ideas")
        self.play(FadeIn(parents), FadeIn(plab), run_time=0.7)

        legend = VGroup(
            VGroup(Rectangle(width=0.5, height=0.2, stroke_width=0, fill_color=OLD, fill_opacity=1), T("old strand", 24, OLD)).arrange(RIGHT, buff=0.2),
            VGroup(Rectangle(width=0.5, height=0.2, stroke_width=0, fill_color=NEW, fill_opacity=1), T("new strand", 24, NEW)).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.9).move_to([0, -3.2, 0])

        def copy_into(kind, phrase):
            x = COLX[KINDS.index(kind)]
            ds = d[kind + "_d"]
            arrows = VGroup(arr_down([x - 0.7, 1.15], [x - 0.7, 0.2]), arr_down([x + 0.7, 1.15], [x + 0.7, 0.2]))
            self.at(phrase)
            if kind == "con":
                # parent stays; a new pair is built
                self.play(FadeIn(d[kind + "_title"]), run_time=0.3)
                self.play(TransformFromCopy(d[kind + "_p"], ds[0]), run_time=0.7)
                self.play(TransformFromCopy(d[kind + "_p"], ds[1]), run_time=0.7)
            else:
                self.play(FadeIn(d[kind + "_title"]), run_time=0.3)
                self.play(TransformFromCopy(d[kind + "_p"], ds[0]), TransformFromCopy(d[kind + "_p"], ds[1]), run_time=0.9)
            lab = T(desc[kind], 24, GREY).move_to([x, -2.4, 0])
            self.play(FadeIn(lab), run_time=0.3)
            d[kind + "_lab"] = lab

        copy_into("con", "Conservative copying")
        copy_into("semi", "gives each daughter")
        copy_into("dis", "Dispersive copying")
        self.at("Old strands are purple")
        self.play(FadeIn(legend), run_time=0.5)
        self.finish()


def arr_down(a, b):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)


# ---------------------------------------------------------------------------------------------
class S03First(SpokenScene):
    def construct(self):
        d = build_models_cols(with_parent=False)
        tubes, mobs = {}, []
        for k, x in zip(KINDS, COLX):
            ds = d[k + "_d"]
            self.add(d[k + "_title"], *ds)
        # shrink daughters to the top, make tubes
        ys = [2.3, 1.7]
        anims = []
        for k, x in zip(KINDS, COLX):
            for dd, y in zip(d[k + "_d"], ys):
                anims.append(dd.animate.scale(0.62).move_to([x, y, 0]))
            t = make_tube(3.6).move_to([x, -1.0, 0])
            tubes[k] = t
        self.at("Now predict")
        self.play(*anims, run_time=0.8)
        self.play(*[FadeIn(tubes[k]) for k in KINDS], run_time=0.5)
        ll = T("light", 24, NEW).move_to([-5.7, tubes["con"].ypos(0), 0])
        lh = T("heavy", 24, OLD).move_to([-5.7, tubes["con"].ypos(1), 0])
        self.play(FadeIn(ll), FadeIn(lh), run_time=0.4)

        bands = {}
        bands["con"] = VGroup(band(tubes["con"], 1, OLD), band(tubes["con"], 0, NEW))
        bands["semi"] = band(tubes["semi"], 0.5, HYB)
        bands["dis"] = band(tubes["dis"], 0.5, HYB)
        self.at("gives a heavy band")
        self.play(FadeIn(bands["con"][0], scale=0.6), run_time=0.4)
        self.at("and a light band")
        self.play(FadeIn(bands["con"][1], scale=0.6), run_time=0.4)

        ymid = tubes["con"].ypos(0.5)
        line = DashedLine([-5.0, ymid, 0], [5.3, ymid, 0], color=YELLOW, stroke_width=4, dash_length=0.2)
        seen = T("seen", 26, YELLOW).move_to([5.9, ymid, 0])
        self.at("hybrid band that was seen")
        self.play(Create(line), FadeIn(seen), run_time=0.8)
        xc = cross(VGroup(tubes["con"]).copy().scale(0.8))
        self.at("rules it out")
        self.play(Create(xc), FadeIn(status("ruled out", RED, COLX[0])), run_time=0.6)

        self.at("predicts that hybrid")
        self.play(GrowFromCenter(bands["semi"]), run_time=0.5)
        self.play(FadeIn(status("fits", GREEN, COLX[1])), run_time=0.3)
        self.at("So does dispersive")
        self.play(GrowFromCenter(bands["dis"]), run_time=0.5)
        self.play(FadeIn(status("fits", GREEN, COLX[2])), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Second(SpokenScene):
    def construct(self):
        xs = [COLX[0], COLX[1], COLX[2]]
        t_semi = make_tube(3.6).move_to([xs[0], -1.0, 0])
        t_obs = make_tube(3.6).move_to([xs[1], -1.0, 0])
        t_dis = make_tube(3.6).move_to([xs[2], -1.0, 0])
        ti = [title("Semiconservative", xs[0], y=3.1, size=28), title("Seen", xs[1], YELLOW, y=3.1, size=28),
              title("Dispersive", xs[2], y=3.1, size=28)]
        # the hybrids carried over from the first generation
        semi0 = [duplex(OLD, NEW, 1.6).move_to([xs[0], 2.3 - 0.0, 0]), duplex(OLD, NEW, 1.6).move_to([xs[0], 1.7, 0])]
        dis0 = [duplex(*PATCH_A, w=1.6).move_to([xs[2], 2.3, 0]), duplex(*PATCH_A, w=1.6).move_to([xs[2], 1.7, 0])]
        ll = T("light", 24, NEW).move_to([-5.7, t_semi.ypos(0), 0])
        lh = T("heavy", 24, OLD).move_to([-5.7, t_semi.ypos(1), 0])
        self.add(*ti, *semi0, *dis0, t_semi, t_obs, t_dis, ll, lh)

        # semiconservative: 2 hybrids -> 2 hybrid + 2 light
        semi1 = [duplex(OLD, NEW, 1.2), duplex(NEW, NEW, 1.2), duplex(OLD, NEW, 1.2), duplex(NEW, NEW, 1.2)]
        pos = [(xs[0] - 0.8, 2.3), (xs[0] + 0.8, 2.3), (xs[0] - 0.8, 1.7), (xs[0] + 0.8, 1.7)]
        for m, p in zip(semi1, pos):
            m.move_to([p[0], p[1], 0])
        dis1 = [duplex(*PATCH_Q, w=1.2) for _ in range(4)]
        pos2 = [(xs[2] - 0.8, 2.3), (xs[2] + 0.8, 2.3), (xs[2] - 0.8, 1.7), (xs[2] + 0.8, 1.7)]
        for m, p in zip(dis1, pos2):
            m.move_to([p[0], p[1], 0])
        mb_semi = VGroup(band(t_semi, 0.5, HYB), band(t_semi, 0, NEW))
        mb_dis = band(t_dis, 0.25, HYB)

        self.at("second generation decides")
        self.wait(0.6)
        self.at("splits each hybrid")
        self.play(ReplacementTransform(VGroup(*semi0), VGroup(*semi1)), run_time=1.0)
        self.at("equal amounts")
        self.play(GrowFromCenter(mb_semi[0]), GrowFromCenter(mb_semi[1]), run_time=0.8)

        self.at("Dispersive copying makes")
        self.play(ReplacementTransform(VGroup(*dis0), VGroup(*dis1)), run_time=0.9)
        tick = M("1/4", 24, TEXT).move_to([t_dis.get_right()[0] + 0.6, t_dis.ypos(0.25), 0])
        self.at("one band")
        self.play(GrowFromCenter(mb_dis), FadeIn(tick), run_time=0.7)

        obs = VGroup(band(t_obs, 0.5, HYB), band(t_obs, 0, NEW))
        t_obs.set_stroke(YELLOW)
        self.at("saw hybrid and light")
        self.play(GrowFromCenter(obs[0]), GrowFromCenter(obs[1]), t_obs.animate.set_stroke(YELLOW, 5), run_time=0.8)
        self.at("dispersive copying is out")
        xc = cross(VGroup(t_dis).copy().scale(0.8))
        self.play(Create(xc), FadeIn(status("ruled out", RED, xs[2])), FadeIn(status("fits", GREEN, xs[0])), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def lineage():
    gens = [[("H", "H")]]
    for _ in range(3):
        nxt = []
        for a, b in gens[-1]:
            nxt += [(a, "L"), (b, "L")]
        gens.append(nxt)
    return gens


def col(c):
    return OLD if c == "H" else NEW


class S05Third(SpokenScene):
    def construct(self):
        gens = lineage()
        ys = [2.65, 1.2, -0.25, -1.7]
        cx, sp, w = 1.0, 1.28, 1.1
        rows = []
        for g, y in zip(gens, ys):
            n = len(g)
            r = []
            for i, (a, b) in enumerate(g):
                r.append(duplex(col(a), col(b), w=w, h=0.2, gap=0.08).move_to([cx + (i - (n - 1) / 2) * sp, y, 0]))
            rows.append(r)
        labels = ["start", "1 round", "2 rounds", "3 rounds"]
        labs = [T(t, 24, GREY).move_to([-5.45, y, 0]) for t, y in zip(labels, ys)]
        self.at("Now count")
        self.play(FadeIn(labs[0]), run_time=0.3)
        self.at("one heavy duplex")
        self.play(FadeIn(rows[0][0]), run_time=0.5)

        def step(k, phrase):
            self.at(phrase)
            anims = [FadeIn(labs[k])]
            for j, p in enumerate(rows[k - 1]):
                anims.append(TransformFromCopy(p, rows[k][2 * j]))
                anims.append(TransformFromCopy(p, rows[k][2 * j + 1]))
            self.play(*anims, run_time=0.9)

        step(1, "After one round")
        step(2, "After two rounds")
        step(3, "After three rounds")

        # ring the two original heavy strands
        rings = VGroup(*[SurroundingRectangle(rows[3][i].top_s, color=YELLOW, buff=0.07, stroke_width=4) for i in (0, 4)])
        self.at("never multiply")
        self.play(Create(rings), run_time=0.7)
        s1 = T("25% hybrid", 34, HYB, weight=BOLD)
        s2 = T("75% light", 34, NEW, weight=BOLD)
        summ = VGroup(s1, s2).arrange(RIGHT, buff=1.2).move_to([cx, -3.05, 0])
        self.at("that is 25")
        self.play(FadeIn(s1, shift=UP * 0.15), run_time=0.5)
        self.at("and 75")
        self.play(FadeIn(s2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        tubes = [make_tube(3.6).move_to([x, -0.7, 0]) for x in COLX]
        ti = [title(NAMES[k], x, y=3.0, size=28) for k, x in zip(KINDS, COLX)]
        bs = [VGroup(band(tubes[0], 1, OLD), band(tubes[0], 0, NEW)), band(tubes[1], 0.5, HYB), band(tubes[2], 0.5, HYB)]
        ymid = tubes[0].ypos(0.5)
        line = DashedLine([-5.2, ymid, 0], [5.4, ymid, 0], color=YELLOW, stroke_width=4, dash_length=0.2)
        dots = VGroup(*[Circle(radius=0.14, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([x - 0.0, ymid, 0]) for x in COLX])
        avg = T("same average", 26, YELLOW).move_to([0, 1.65, 0])
        self.at("average heavy content")
        self.play(FadeIn(VGroup(*ti)), FadeIn(VGroup(*tubes)), *[FadeIn(b) for b in bs], run_time=0.8)
        self.play(Create(line), FadeIn(avg), run_time=0.7)

        self.at("Only the way")
        self.play(Indicate(bs[0], color=WHITE, scale_factor=1.15), Indicate(bs[1], color=WHITE, scale_factor=1.15),
                  Indicate(bs[2], color=WHITE, scale_factor=1.15), run_time=1.0)
        gen = chip("second generation", YELLOW, 26).move_to([0, -3.15, 0])
        b2 = [VGroup(band(tubes[0], 1, OLD, 0.15), band(tubes[0], 0, NEW, 0.45)),
              VGroup(band(tubes[1], 0.5, HYB), band(tubes[1], 0, NEW)), band(tubes[2], 0.25, HYB)]
        self.at("generation where")
        self.play(FadeOut(line), FadeOut(avg), *[FadeOut(b) for b in bs], run_time=0.4)
        self.play(FadeIn(gen, shift=UP * 0.15), *[FadeIn(b) for b in b2], run_time=0.6)
        bs = b2

        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in [*ti, *tubes, *bs, gen]], run_time=0.6)
        dup = duplex(TEXT, NEW, w=6.0, h=0.5, gap=0.15).move_to([0, 0.2, 0])
        lo = T("one parental strand", 32, TEXT).next_to(dup.top_s, UP, buff=0.35)
        ln = T("one new strand", 32, NEW).next_to(dup.bot_s, DOWN, buff=0.35)
        self.at("Each new helix")
        self.play(FadeIn(dup, scale=0.9), run_time=0.6)
        self.play(FadeIn(lo), FadeIn(ln), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Each new helix holds one parental strand and one new strand."
