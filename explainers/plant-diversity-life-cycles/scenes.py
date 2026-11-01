"""Plants on land: two bodies, one plant life cycle  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = haploid (n): the gametophyte, spores, eggs and sperm, the haploid arc of the loop
  ORANGE = diploid (2n): the sporophyte, the zygote, the diploid arc of the loop
  RED    = meiosis
  GREEN  = fertilization
  YELLOW = the highlight: a token travelling the loop, the question, the thing to notice
  GREY   = mitosis, outlines, notes, empty slots
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
CX, CY, RA, RB = 0.0, -0.2, 5.0, 2.5     # the life-cycle loop (an ellipse), clockwise


def rp(deg, k=1.0):
    a = np.radians(deg)
    return np.array([CX + k * RA * np.cos(a), CY + k * RB * np.sin(a), 0])


def seg(a, b, color, w=6):
    """loop segment from angle a to angle b (clockwise = decreasing angle)."""
    return ParametricFunction(lambda s: rp(a + (b - a) * s), t_range=[0, 1], color=color, stroke_width=w)


def tip(a, b, color):
    """small arrowhead at the middle of a loop segment."""
    m = rp((a + b) / 2)
    d = rp((a + b) / 2 - 1) - rp((a + b) / 2 + 1)
    ang = np.arctan2(d[1], d[0])
    t = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.17)
    t.rotate(ang - PI / 2).move_to(m)
    return t


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def pulse(c, color, s=1.12):
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s)


def marker(deg, color):
    p = rp(deg)
    return Circle(radius=0.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.9).move_to(p)


def cushion(w=4.8, h=2.0, n=15, color=BLUE):
    """a moss cushion as a schematic block: a rounded base with short upright shoots."""
    base = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.22)
    shoots = VGroup()
    for i in range(n):
        x = -w / 2 + 0.3 + i * (w - 0.6) / (n - 1)
        top = h / 2 - 0.1 - 0.16 * ((i * 7) % 5)
        shoots.add(Line([x, -h / 2 + 0.25, 0], [x, top, 0], color=color, stroke_width=4))
    g = VGroup(base, shoots)
    g.base = base
    return g


def two_blk(a, b, color):
    r = RoundedRectangle(corner_radius=0.25, width=4.4, height=2.2, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.18)
    return VGroup(r, two_line(a, b, color, 34, 28).move_to(r))


def two_line(a, b, color, s1=24, s2=22):
    l1 = T(a, s1, color, weight=BOLD)
    l2 = T(b, s2, TEXT)
    return VGroup(l1, l2).arrange(DOWN, buff=0.1)


class S00Title(TitleCard):
    LESSON = "Plants on Land"
    TITLE = "Two bodies, one plant life cycle"


# ---------------------------------------------------------------------------------------------
class S01Cushion(SpokenScene):
    """moss cushion (haploid) = human egg (one set); where is the diploid moss?"""

    def construct(self):
        cu = cushion(5.6, 2.7, 17).move_to([-3.4, 1.2, 0])
        cu_lbl = T("moss cushion", 28, BLUE).next_to(cu, DOWN, buff=0.2)
        cu_set = T("cells with one set: haploid", 24, BLUE).next_to(cu_lbl, DOWN, buff=0.08)
        self.at("green cushion of moss")
        self.play(FadeIn(cu, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(cu_lbl), run_time=0.4)
        self.at("haploid")
        self.play(FadeIn(cu_set), run_time=0.5)

        egg = Circle(radius=1.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([4.0, 1.3, 0])
        egg_lbl = T("human egg", 28, BLUE).next_to(egg, DOWN, buff=0.2)
        egg_set = T("one set", 24, BLUE).next_to(egg_lbl, DOWN, buff=0.08)
        eq = T("same count", 26, GREY).move_to([1.35, 1.3, 0])
        self.at("same count")
        self.play(FadeIn(egg), FadeIn(egg_lbl), FadeIn(egg_set), FadeIn(eq), run_time=0.8)

        body = T("your body: one set only as eggs and sperm form", 26, TEXT).move_to([0, -1.75, 0])
        self.at("In your body")
        self.play(FadeIn(body, shift=UP * 0.1), run_time=0.7)
        self.at("only cells")
        self.play(Indicate(egg, color=BLUE, scale_factor=1.15), run_time=0.8)

        q = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.0, height=1.1, stroke_color=YELLOW, stroke_width=4))
        ql = T("diploid moss?", 34, YELLOW, weight=BOLD)
        qg = VGroup(q, ql).move_to([0, -2.85, 0])
        ql.move_to(q)
        self.at("where is the diploid moss")
        self.play(Create(q), FadeIn(ql), run_time=0.9)
        self.play(Indicate(ql, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Two(SpokenScene):
    """two bodies alternating; then a mammal strip with no haploid body."""

    def construct(self):
        head = T("land plants", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        gam = RoundedRectangle(corner_radius=0.25, width=5.2, height=3.0, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.18).move_to([-3.3, 0.4, 0])
        gam_t = two_line("gametophyte", "haploid body", BLUE, 38, 30).move_to(gam)
        spo = RoundedRectangle(corner_radius=0.25, width=5.2, height=3.0, stroke_color=ORANGE, stroke_width=4,
                               fill_color=ORANGE, fill_opacity=0.18).move_to([3.3, 0.4, 0])
        spo_t = two_line("sporophyte", "diploid body: two sets", ORANGE, 38, 28).move_to(spo)
        self.at("Land plants grow two")
        self.play(Write(head), run_time=0.7)
        self.at("The haploid body")
        self.play(FadeIn(gam, scale=0.9), FadeIn(gam_t), run_time=0.8)
        self.at("the diploid body")
        self.play(FadeIn(spo, scale=0.9), FadeIn(spo_t), run_time=0.8)
        self.at("with two sets")
        self.play(Indicate(spo_t[1], color=ORANGE, scale_factor=1.12), run_time=0.8)

        self.at("Each body gives rise")
        a1 = CurvedArrow(gam.get_top() + RIGHT * 0.6, spo.get_top() + LEFT * 0.6, angle=-TAU / 6, color=GREY, stroke_width=6)
        a2 = CurvedArrow(spo.get_bottom() + LEFT * 0.6, gam.get_bottom() + RIGHT * 0.6, angle=-TAU / 6, color=GREY, stroke_width=5)
        self.play(Create(a1), run_time=0.8)
        self.play(Create(a2), run_time=0.8)
        alt = T("alternation of generations", 34, YELLOW).move_to([0, -3.15, 0])
        self.at("alternation of generations")
        self.play(FadeIn(alt, shift=UP * 0.1), run_time=0.7)

        # --- mammals ----------------------------------------------------------------------------
        self.at("In humans")
        self.play(*[FadeOut(m) for m in [gam, gam_t, spo, spo_t, a1, a2, alt]], run_time=0.5)
        mh = T("humans and other mammals", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Transform(head, mh), run_time=0.5)
        body = two_blk("body cells", "diploid", ORANGE).move_to([-3.6, 1.0, 0])
        eggs = two_blk("eggs and sperm", "haploid", BLUE).move_to([3.6, 1.0, 0])
        self.play(FadeIn(body), run_time=0.5)
        self.at("meiosis makes eggs")
        ar = Arrow(body.get_right(), eggs.get_left(), buff=0.1, color=RED, stroke_width=7, tip_length=0.3)
        ml = T("meiosis", 34, RED).next_to(ar, UP, buff=0.12)
        self.play(GrowArrow(ar), FadeIn(ml), FadeIn(eggs), run_time=0.9)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.2, height=1.5, stroke_color=GREY, stroke_width=3))
        slot_t = T("haploid body", 32, GREY).move_to(slot)
        slot_g = VGroup(slot, slot_t).move_to([0, -2.2, 0])
        slot_t.move_to(slot)
        x1 = Line(slot.get_corner(UL) + DR * 0.15, slot.get_corner(DR) + UL * 0.15, color=GREY, stroke_width=5)
        x2 = Line(slot.get_corner(UR) + DL * 0.15, slot.get_corner(DL) + UR * 0.15, color=GREY, stroke_width=5)
        self.at("no haploid body")
        self.play(Create(slot), FadeIn(slot_t), run_time=0.6)
        self.play(Create(x1), Create(x2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Events(SpokenScene):
    """a bare loop; meiosis and fertilization are the two places the number changes."""

    def construct(self):
        ring = Ellipse(width=2 * RA, height=2 * RB, color=GREY, stroke_width=5).move_to([CX, CY, 0])
        self.at("read any life cycle")
        self.play(Create(ring), run_time=self.beat(0.11))

        m = marker(-45, RED)
        ml = T("meiosis", 30, RED, weight=BOLD).move_to(rp(-45) + np.array([1.4, -0.65, 0]))
        mn = T("2n to n", 26, RED).next_to(ml, DOWN, buff=0.08)
        self.at("Meiosis halves")
        self.play(FadeIn(m, scale=1.8), FadeIn(ml), run_time=0.6)
        self.at("diploid to haploid")
        self.play(FadeIn(mn), run_time=0.4)

        f = marker(135, GREEN)
        fl = T("fertilization", 30, GREEN, weight=BOLD).move_to(rp(135) + np.array([-1.3, 0.85, 0]))
        fn = T("n to 2n", 26, GREEN).next_to(fl, DOWN, buff=0.08)
        fn.shift(LEFT * 0.0)
        self.at("Fertilization joins")
        self.play(FadeIn(f, scale=1.8), FadeIn(fl), run_time=0.6)
        self.at("restores the diploid number")
        self.play(FadeIn(fn), run_time=0.4)

        self.at("only two places")
        self.play(Indicate(m, color=RED, scale_factor=1.4), Indicate(f, color=GREEN, scale_factor=1.4), run_time=0.9)

        # the two arcs take their labels
        nar = seg(-45, -225, BLUE)
        dar = seg(135, -45, ORANGE)
        nl = T("haploid", 30, BLUE, weight=BOLD).move_to([-2.4, -0.95, 0])
        dl = T("diploid", 30, ORANGE, weight=BOLD).move_to([2.4, 0.6, 0])
        self.at("share one label")
        self.play(Create(nar), Create(dar), run_time=0.8)
        self.play(FadeIn(nl), FadeIn(dl), run_time=0.3)
        mit = T("mitosis: no change", 28, GREY).move_to([0, -0.1, 0])
        self.at("Mitosis")
        self.play(FadeIn(mit, scale=0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cycle(SpokenScene):
    """the five stages on the loop, a token travelling it."""

    def construct(self):
        nar = seg(-45, -225, BLUE)
        dar = seg(135, -45, ORANGE)
        m = marker(-45, RED)
        f = marker(135, GREEN)
        ml = T("meiosis", 28, RED, weight=BOLD).move_to(rp(-45) + np.array([1.3, -0.55, 0]))
        fl = T("fertilization", 28, GREEN, weight=BOLD).move_to(rp(135) + np.array([-1.3, 0.8, 0]))
        nl = T("haploid", 28, BLUE, weight=BOLD).move_to([-2.4, -0.95, 0])
        dl = T("diploid", 28, ORANGE, weight=BOLD).move_to([2.4, 0.6, 0])
        self.add(nar, dar, m, f, ml, fl, nl, dl)

        spo = bchip("sporophyte", ORANGE, size=26).move_to(rp(30))
        spores = bchip("spores", BLUE, size=26).move_to(rp(-85))
        gam = bchip("gametophyte", BLUE, size=26).move_to(rp(-145))
        eggs = bchip("eggs and sperm", BLUE, size=26).move_to(rp(-205))
        zyg = bchip("zygote", ORANGE, size=26).move_to(rp(105))
        tok = Dot(radius=0.16, color=YELLOW).move_to(rp(30)).set_z_index(1)
        for c in (spo, spores, gam, eggs, zyg):
            c.set_z_index(3)

        tips = [tip(30, -45, ORANGE), tip(-45, -85, BLUE), tip(-85, -145, BLUE), tip(-145, -205, BLUE),
                tip(-205, -255, GREEN), tip(-255, -330, ORANGE)]

        def go(a, b, t=1.0):
            path = seg(a, b, YELLOW)
            return MoveAlongPath(tok, path, run_time=t)

        self.at("cells of the sporophyte")
        self.play(FadeIn(spo, scale=0.9), FadeIn(tok), run_time=0.6)
        self.at("undergo meiosis")
        self.play(go(30, -45, 0.9), FadeIn(tips[0]), run_time=0.9)
        self.play(pulse(VGroup(m, m, m), RED) if False else Indicate(m, color=RED, scale_factor=1.5), run_time=0.5)
        self.at("spores")
        self.play(go(-45, -85, 0.6), FadeIn(spores, scale=0.9), FadeIn(tips[1]), run_time=0.6)
        nog = T("not gametes", 24, YELLOW).move_to(rp(-85) + np.array([2.4, -0.2, 0]))
        self.at("not gametes")
        self.play(FadeIn(nog, shift=LEFT * 0.1), run_time=0.5)

        self.at("divides by mitosis", nth=0)
        mit1 = T("mitosis", 24, GREY).move_to(rp(-115, 0.62))
        self.play(go(-85, -145, 1.0), FadeOut(nog), FadeIn(mit1), FadeIn(tips[2]), run_time=1.0)
        self.at("gametophyte")
        self.play(FadeIn(gam, scale=0.9), run_time=0.5)
        self.play(pulse(gam, BLUE), run_time=0.5)

        self.at("makes eggs and sperm")
        mit2 = T("mitosis", 24, GREY).move_to(rp(-178, 0.62))
        self.play(go(-145, -205, 1.0), FadeIn(mit2), FadeIn(tips[3]), run_time=1.0)
        self.play(FadeIn(eggs, scale=0.9), run_time=0.5)
        self.at("already haploid")
        self.play(Indicate(nl, color=BLUE, scale_factor=1.25), run_time=0.7)

        self.at("Fertilization gives")
        self.play(go(-205, -255, 1.0), FadeIn(tips[4]), run_time=1.0)
        self.play(Indicate(f, color=GREEN, scale_factor=1.5), FadeIn(zyg, scale=0.9), run_time=0.7)
        zl = T("the single fertilized cell", 26, TEXT).move_to([-0.2, 3.2, 0])
        self.at("single fertilized cell")
        self.play(FadeIn(zl), run_time=0.5)

        self.at("divides by mitosis", nth=1)
        mit3 = T("mitosis", 24, GREY).move_to(rp(70, 0.62))
        self.play(FadeOut(zl), go(-255, -330, 1.0), FadeIn(mit3), FadeIn(tips[5]), run_time=1.0)
        self.at("new sporophyte")
        self.play(pulse(spo, ORANGE), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Which(SpokenScene):
    """four plants, two blocks each: which body is the big one."""

    def construct(self):
        cols = [-4.65, -1.55, 1.55, 4.65]
        names = ["moss", "fern", "pine", "Arabidopsis"]
        heads = [T(n, 32, TEXT, weight=BOLD).move_to([x, 3.2, 0]) for n, x in zip(names, cols)]
        heads[3].set_x(4.65)
        side_s = T("sporophyte, diploid", 22, ORANGE).move_to([-5.45, 1.9, 0])
        side_g = T("gametophyte, haploid", 22, BLUE).move_to([-5.45, 1.9, 0])
        key = VGroup(T("sporophyte: diploid", 24, ORANGE), T("gametophyte: haploid", 24, BLUE)).arrange(RIGHT, buff=0.7)
        key.move_to([0, -3.35, 0])
        note = T("relative size only, not to scale", 22, GREY).move_to([0, -2.85, 0])
        y_s, y_g = 1.4, -1.15

        def block(x, y, big, color, label, w_big=2.95, h_big=2.15, w_s=1.5, h_s=0.75):
            w, h = (w_big, h_big) if big else (w_s, h_s)
            r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=4,
                                 fill_color=color, fill_opacity=0.24)
            r.move_to([x, y - (h_big - h) / 2 if False else y, 0])
            t = T(label, 24, color)
            if big:
                t.move_to(r)
            else:
                t.next_to(r, DOWN, buff=0.1)
            return VGroup(r, t)

        spec = [  # (sporophyte big?, sporophyte label, gametophyte label)
            (False, "stalk and capsule", "leafy green shoot"),
            (True, "frond", "prothallus"),
            (True, "tree", "pollen grain"),
            (True, "green plant", "pollen grain,\nembryo sac"),
        ]
        groups = []
        for x, (sbig, sl, gl) in zip(cols, spec):
            sp = block(x, y_s, sbig, ORANGE, sl)
            ga = block(x, y_g, not sbig, BLUE, gl)
            groups.append((sp, ga))
        self.add(key, note)
        order = [  # (header cue, [(which, cue), (which, cue)])  which: 0 = sporophyte block, 1 = gametophyte block
            ("In a moss", [(1, "leafy green shoot"), (0, "thin stalk")]),
            ("In a fern", [(0, "the frond"), (1, "small")]),
            ("In a pine", [(0, "the tree"), (1, "pollen grain")]),
            ("In the flowering plant", [(0, "the green plant"), (1, "the gametophytes are")]),
        ]
        for i, (hc, parts) in enumerate(order):
            self.at(hc)
            self.play(FadeIn(heads[i], shift=DOWN * 0.1), run_time=0.4)
            for which, c in parts:
                self.at(c)
                self.play(FadeIn(groups[i][which], scale=0.9), run_time=0.6)
        self.at("embryo sac")
        self.play(Indicate(groups[3][1], color=BLUE, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the diploid moss: the stalk and capsule on the cushion; size is not ploidy; the rule."""

    def construct(self):
        cu = cushion(5.8, 2.2, 17).move_to([-3.4, -0.55, 0])
        cu_lbl = T("moss cushion: haploid", 26, BLUE).next_to(cu, DOWN, buff=0.18)
        self.add(cu, cu_lbl)
        top = -0.55 + 1.1                                   # top of the cushion
        stalk = Rectangle(width=0.16, height=1.5, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([-3.4, top + 0.75, 0])
        cap = RoundedRectangle(corner_radius=0.15, width=0.8, height=0.9, stroke_color=ORANGE, stroke_width=4,
                               fill_color=ORANGE, fill_opacity=0.35).move_to([-3.4, top + 1.5 + 0.4, 0])
        sl = chip("stalk and capsule: diploid", ORANGE, size=26).move_to([0.2, top + 1.9, 0])
        self.at("diploid moss was there")
        self.play(Indicate(cu, color=YELLOW, scale_factor=1.03), run_time=0.7)
        self.at("stalk and capsule")
        self.play(GrowFromEdge(stalk, DOWN), run_time=0.7)
        self.play(FadeIn(cap, scale=0.7), FadeIn(sl, shift=LEFT * 0.2), run_time=0.6)
        self.at("grow from the zygote")
        zy = chip("zygote", ORANGE, size=26).move_to([-5.45, top + 0.7, 0])
        zar = Arrow(zy.get_right(), [-3.55, top + 0.7, 0], buff=0.08, color=ORANGE, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(zy, scale=0.9), GrowArrow(zar), run_time=0.6)

        p1 = VGroup(T("moss: the big body", 26, BLUE), T("is haploid", 26, BLUE)).arrange(DOWN, buff=0.06)
        p2 = VGroup(T("fern, pine, flowering plant:", 26, ORANGE), T("the big body is diploid", 26, ORANGE)).arrange(DOWN, buff=0.06)
        panel = VGroup(p1, p2).arrange(DOWN, buff=0.45).move_to([3.7, -0.5, 0])
        self.at("The big body")
        self.play(FadeIn(p1, shift=LEFT * 0.15), run_time=0.7)
        self.at("but the diploid sporophyte")
        self.play(FadeIn(p2, shift=LEFT * 0.15), run_time=0.7)
        self.at("do not guess from size")
        self.play(Indicate(panel, color=YELLOW, scale_factor=1.06), run_time=0.7)

        rule = T("Find meiosis and fertilization first,", 36, YELLOW, font=TITLE_FONT)
        rule2 = T("then label every stage.", 36, YELLOW, font=TITLE_FONT)
        rg = VGroup(rule, rule2).arrange(DOWN, buff=0.12).move_to([0, -3.0, 0])
        self.at("Find meiosis and fertilization first")
        self.play(FadeIn(rg, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Find meiosis and fertilization first, then label every stage."
