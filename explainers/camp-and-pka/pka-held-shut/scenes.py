"""A kinase held shut by its own partner  (section film, lesson: cAMP and protein kinase A)

COLOR MAP (one color per concept, whole video)
  BLUE   = catalytic subunit (a complete kinase), its active-site slot is a dark notch
  PURPLE = regulatory subunit
  YELLOW = a target-like stretch / a substrate (the real target and the pseudosubstrate look alike)
  GOLD   = a phosphate group (P badge)
  TEAL   = cAMP and its binding sites
  RED    = off / blocked / cannot accept a phosphate
  GREEN  = free and phosphorylating (the classical model)
  GREY   = labels, outlines
Everything is schematic: subunit shapes are idealised and not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CY = 0.1          # vertical centre of the full complex


def pbadge(size=0.22):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def cross(at, s=0.2, color=RED):
    at = np.array(at, float)
    return VGroup(Line(at + [-s, -s, 0], at + [s, s, 0], color=color, stroke_width=7),
                  Line(at + [-s, s, 0], at + [s, -s, 0], color=color, stroke_width=7))


def build_side(sign, cy=CY):
    """one catalytic + one regulatory subunit and the stretch between them. sign -1 left, +1 right."""
    cx_c, cx_r = sign * 4.1, sign * 1.15
    C = RoundedRectangle(corner_radius=0.45, width=2.6, height=3.1, stroke_color=BLUE, stroke_width=4,
                         fill_color=BLUE, fill_opacity=0.25).move_to([cx_c, cy, 0])
    slot = RoundedRectangle(corner_radius=0.12, width=0.55, height=0.7, stroke_color=GREY, stroke_width=2.5,
                            fill_color=BG, fill_opacity=1).move_to([cx_c - sign * 1.025, cy, 0])
    R = RoundedRectangle(corner_radius=0.45, width=2.0, height=3.1, stroke_color=PURPLE, stroke_width=4,
                         fill_color=PURPLE, fill_opacity=0.25).move_to([cx_r, cy, 0])
    tab = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.5, stroke_color=YELLOW, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.55).move_to([sign * 2.7, cy, 0])
    lc = T("catalytic", 26, BLUE).move_to([cx_c, cy - 1.95, 0])
    lr = T("regulatory", 26, PURPLE).move_to([cx_r, cy - 1.95, 0])
    return dict(C=C, slot=slot, R=R, tab=tab, lc=lc, lr=lr)


def strip(labels, colors, size=28, buff=0.12):
    """a row of small chips: a target-like stretch of residues (text only, no structure)."""
    chips = [chip(t, c, size=size, pad=0.14) for t, c in zip(labels, colors)]
    return VGroup(*chips).arrange(RIGHT, buff=buff)


def pair_group(d):
    return VGroup(d["C"], d["slot"], d["R"], d["tab"], d["lc"], d["lr"])


# one shared place for the zoomed pair (scenes 2 and 3)
ZOOM, ZPOS = 1.3, np.array([0.1, -0.85, 0])


def zoomed_pair():
    d = build_side(-1)
    g = pair_group(d)
    g.scale(ZOOM).move_to(ZPOS)
    return d, g


class S00Title(TitleCard):
    LESSON = "cAMP and Protein Kinase A"
    TITLE = "A blank key holds the kinase shut"


# ---------------------------------------------------------------------------------------------
class S01Rest(SpokenScene):
    def construct(self):
        L, Rt = build_side(-1), build_side(+1)
        # the puzzle: one kinase, and what keeps it off?
        self.play(FadeIn(L["C"]), FadeIn(L["slot"]), run_time=0.7)
        q = chip("off?", RED, size=30).next_to(L["C"], UP, buff=0.3)
        self.at("What keeps a kinase off")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.5)

        title = T("Protein kinase A", 34, font=TITLE_FONT).move_to([-0.8, 3.0, 0])
        cam = chip("cAMP", TEAL, size=28).move_to([3.2, 3.0, 0])
        rd = Arrow(cam.get_left(), title.get_right() + RIGHT * 0.05, buff=0.1, color=TEAL, stroke_width=5,
                   tip_length=0.2)
        self.at("Protein kinase A")
        self.play(FadeOut(q), Write(title), run_time=0.8)
        self.at("reads cyclic")
        self.play(FadeIn(cam, shift=LEFT * 0.2), GrowArrow(rd), run_time=0.6)

        self.at("At rest")
        self.play(FadeIn(L["tab"]), FadeIn(L["R"]), FadeIn(Rt["R"]), FadeIn(Rt["tab"]),
                  FadeIn(Rt["C"]), FadeIn(Rt["slot"]), run_time=1.1)
        Rt["tab"].set_z_index(2); L["tab"].set_z_index(2)
        count = T("four subunits (schematic, not to scale)", 26, GREY).move_to([0, -2.95, 0])
        self.play(FadeIn(count), run_time=0.4)

        self.at("Two are catalytic")
        self.play(FadeIn(L["lc"]), FadeIn(Rt["lc"]),
                  Indicate(L["C"], color=BLUE, scale_factor=1.04), Indicate(Rt["C"], color=BLUE, scale_factor=1.04),
                  run_time=0.9)
        self.at("each is a complete kinase")
        tags = [T("a complete kinase", 24, GREY).move_to([x, CY - 2.45, 0]) for x in (-4.1, 4.1)]
        self.play(*[FadeIn(t) for t in tags], run_time=0.5)

        self.at("Two are regulatory")
        self.play(FadeOut(count), FadeIn(L["lr"]), FadeIn(Rt["lr"]),
                  Indicate(L["R"], color=PURPLE, scale_factor=1.04), Indicate(Rt["R"], color=PURPLE, scale_factor=1.04),
                  run_time=0.9)
        self.at("keep the catalytic ones")
        offs = [T("OFF", 34, RED, weight=BOLD).move_to([x, CY + 2.0, 0]) for x in (-4.1, 4.1)]
        self.play(*[FadeIn(o, scale=0.8) for o in offs], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Target(SpokenScene):
    def construct(self):
        # carried over: the full complex, then the right half leaves and the left pair zooms
        L, Rt = build_side(-1), build_side(+1)
        right = VGroup(*Rt.values())
        left_g = pair_group(L)
        self.add(left_g, right)
        self.play(FadeOut(right), left_g.animate.scale(ZOOM).move_to(ZPOS), run_time=1.0)
        tab, slot, C = L["tab"], L["slot"], L["C"]
        self.add(T("schematic, not to scale", 22, GREY).move_to([5.0, -3.55, 0]))

        # the target: Arg Arg Ser/Thr, with a phosphate
        self.at("The kinase phosphorylates")
        tgt = strip(["Arg", "Arg", "Ser/Thr"], [YELLOW, YELLOW, YELLOW]).move_to([-0.2, 2.6, 0])
        tlbl = T("target", 26, YELLOW).next_to(tgt, LEFT, buff=0.4)
        pb = pbadge().move_to([3.4, 2.6, 0])
        self.play(FadeIn(pb, shift=LEFT * 0.2), run_time=0.4)
        self.at("a serine or threonine")
        self.play(FadeIn(tgt[2], shift=DOWN * 0.1), run_time=0.4)
        self.play(pb.animate.move_to(tgt[2].get_corner(UR) + [0.1, 0.12, 0]), run_time=0.5)
        self.at("close after a pair")
        self.play(FadeIn(tgt[0], shift=RIGHT * 0.15), FadeIn(tgt[1], shift=RIGHT * 0.1), run_time=0.6)
        self.at("in its target")
        self.play(FadeIn(tlbl), run_time=0.4)

        self.at("Each regulatory subunit carries")
        self.play(Indicate(tab, color=YELLOW, scale_factor=1.25), run_time=0.8)
        link = DashedLine(tgt.get_bottom() + DOWN * 0.1, tab.get_top() + UP * 0.1, color=YELLOW, stroke_width=3)
        topy = C.get_top()[1] + 0.45
        like = T("looks like a target", 26, YELLOW).move_to([tab.get_center()[0] + 1.6, topy, 0])
        self.at("looks like such")
        self.play(Create(link), FadeIn(like), run_time=0.7)

        self.at("active site")
        asl = T("active site", 26, BLUE).move_to([C.get_center()[0] - 0.6, topy, 0])
        aar = Arrow(asl.get_bottom() + DOWN * 0.05, slot.get_top() + LEFT * 0.1 + UP * 0.05, buff=0.05, color=BLUE,
                    stroke_width=4, tip_length=0.18)
        self.play(FadeIn(asl), GrowArrow(aar), Indicate(slot, color=BLUE, scale_factor=1.3), run_time=0.8)
        self.at("where a substrate")
        ring = SurroundingRectangle(VGroup(slot, tab), color=GOLD, buff=0.12, corner_radius=0.12, stroke_width=3)
        sub = T("where a substrate would go", 26, GOLD).move_to([tab.get_center()[0] + 1.6, topy, 0])
        self.play(Create(ring), FadeOut(VGroup(like, link)), FadeIn(sub), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Blank(SpokenScene):
    def construct(self):
        d, g = zoomed_pair()
        self.add(g)
        tab, slot = d["tab"], d["slot"]
        self.add(T("schematic, not to scale", 22, GREY).move_to([5.0, -3.55, 0]))
        topy0 = d["C"].get_top()[1] + 0.45
        t1 = T("type I regulatory subunit", 26, PURPLE).move_to([d["R"].get_center()[0] + 0.5, topy0, 0])
        self.at("In type")
        self.play(FadeIn(t1), run_time=0.4)
        self.at("serine position")
        st = strip(["Arg", "Arg", "residue"], [YELLOW, YELLOW, RED]).move_to([-0.2, 2.65, 0])
        sl = T("the stretch", 26, YELLOW).next_to(st, LEFT, buff=0.4)
        self.play(FadeIn(st, shift=DOWN * 0.1), FadeIn(sl), run_time=0.7)
        self.at("cannot accept")
        pb = pbadge().move_to(st[2].get_corner(UR) + [0.5, 0.35, 0])
        self.remove(pb)
        self.play(FadeIn(pb), run_time=0.3)
        self.play(pb.animate.move_to(st[2].get_corner(UR) + [0.1, 0.12, 0]), run_time=0.4)
        x = cross(pb.get_center(), 0.3)
        self.play(Create(x), pb.animate.set_opacity(0.45), run_time=0.4)
        no = T("cannot accept a phosphate", 26, RED).next_to(st, DOWN, buff=0.2).shift(RIGHT * 0.9)
        self.play(FadeIn(no), run_time=0.4)

        self.at("So the stretch fits")
        self.play(tab.animate.shift(LEFT * 0.08), run_time=0.25)
        self.play(tab.animate.shift(RIGHT * 0.08), run_time=0.25)
        self.at("never phosphorylated")
        self.play(Indicate(st[2], color=RED, scale_factor=1.2), run_time=0.6)
        self.at("It is called")
        ps = T("pseudosubstrate", 30, YELLOW, weight=BOLD).move_to([-0.2, 3.3, 0])
        self.play(FadeOut(VGroup(pb, x, no, sl, t1)), FadeIn(ps), run_time=0.7)

        self.at("blank key")
        self.play(FadeOut(st), run_time=0.4)
        topy = d["C"].get_top()[1] + 0.45
        key = T("blank key", 28, YELLOW).move_to([d["R"].get_center()[0] + 0.3, topy, 0])
        lock = T("lock", 28, BLUE).move_to([d["C"].get_center()[0] - 0.4, topy, 0])
        ka = Arrow(key.get_bottom(), tab.get_top() + UP * 0.05, buff=0.08, color=YELLOW, stroke_width=4, tip_length=0.18)
        la = Arrow(lock.get_bottom() + DOWN * 0.05, slot.get_top() + LEFT * 0.1 + UP * 0.05, buff=0.05, color=BLUE,
                   stroke_width=4, tip_length=0.18)
        self.play(FadeIn(key), GrowArrow(ka), FadeIn(lock), GrowArrow(la), run_time=0.8)
        self.at("will not turn")
        self.play(Rotate(tab, 0.12, about_point=tab.get_center()), run_time=0.2)
        self.play(Rotate(tab, -0.24, about_point=tab.get_center()), run_time=0.3)
        self.play(Rotate(tab, 0.12, about_point=tab.get_center()), run_time=0.2)
        self.at("no working key")
        wk = chip("target", YELLOW, size=26).move_to([2.5, 2.7, 0])
        wp = pbadge().move_to(wk.get_corner(UR) + [0.05, 0.05, 0])
        wg = VGroup(wk, wp)
        self.play(FadeIn(wg), run_time=0.4)
        aim = tab.get_center() + UP * 0.75 + RIGHT * 0.1
        self.play(wg.animate.move_to(aim), run_time=0.6)
        bad = cross(tab.get_center() + UP * 0.35 + RIGHT * 0.1, 0.22)
        self.play(Create(bad), run_time=0.2)
        self.play(wg.animate.shift(UP * 0.9 + RIGHT * 1.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Release(SpokenScene):
    def construct(self):
        L, Rt = build_side(-1), build_side(+1)
        allm = [L[k] for k in ("C", "slot", "R", "tab", "lc", "lr")] + [Rt[k] for k in ("C", "slot", "R", "tab", "lc", "lr")]
        self.add(*allm)
        L["tab"].set_z_index(2); Rt["tab"].set_z_index(2)
        self.add(T("schematic, not to scale", 22, GREY).move_to([5.0, -3.55, 0]))

        # binding sites
        sites = []
        for s in (L, Rt):
            cxr = s["R"].get_center()[0]
            for dy in (0.6, -0.6):
                sites.append(Circle(radius=0.24, stroke_color=TEAL, stroke_width=4, fill_color=TEAL,
                                    fill_opacity=0.0).move_to([cxr, CY + dy, 0]))
        self.at("two binding sites")
        self.play(*[Create(c) for c in sites[:2]], run_time=0.7)
        s2 = T("2 sites", 24, TEAL).next_to(L["R"], UP, buff=0.25)
        self.play(FadeIn(s2), run_time=0.3)
        self.at("four in the whole")
        self.play(*[Create(c) for c in sites[2:]], FadeOut(s2), run_time=0.6)
        four = T("4 sites in all", 28, TEAL).move_to([0, 2.55, 0])
        self.play(FadeIn(four), run_time=0.4)

        # cAMP fills them
        self.at("fills them")
        camps = [chip("cAMP", TEAL, size=22, pad=0.1).move_to([s.get_center()[0] + (-0.0), 3.3, 0]) for s in sites]
        # stagger x so the four chips do not overlap
        xs = [-2.6, -1.0, 1.0, 2.6]
        for c, x in zip(camps, xs):
            c.move_to([x, 3.35, 0])
        self.play(FadeOut(four), FadeIn(VGroup(*camps)), run_time=0.3)
        self.play(*[c.animate.scale(0.3).move_to(s.get_center()).set_opacity(0) for c, s in zip(camps, sites)],
                  *[s.animate.set_fill(TEAL, 0.9) for s in sites], run_time=0.9)
        self.remove(*camps)

        # shape change, release
        self.at("changes shape")
        shape = [m.animate.stretch(0.78, 0) for m in (L["R"], Rt["R"])]
        self.play(*shape, *[s.animate.set_color(TEAL) for s in sites], run_time=0.7)
        self.at("lets go")
        self.play(L["tab"].animate.shift(RIGHT * 0.75), Rt["tab"].animate.shift(LEFT * 0.75), run_time=0.7)

        self.at("In the classical model")
        cm = T("classical model", 28, GREY).move_to([0, -2.95, 0])
        self.play(FadeIn(cm), run_time=0.4)
        self.at("come away free")
        dr = 0.85
        self.play(L["C"].animate.shift(LEFT * dr).set_stroke(GREEN), L["slot"].animate.shift(LEFT * dr),
                  L["lc"].animate.shift(LEFT * dr),
                  Rt["C"].animate.shift(RIGHT * dr).set_stroke(GREEN), Rt["slot"].animate.shift(RIGHT * dr),
                  Rt["lc"].animate.shift(RIGHT * dr), run_time=1.0)
        self.at("begin phosphorylating")
        outs = []
        for s, sg in ((L, -1), (Rt, 1)):
            t = chip("target", YELLOW, size=24).move_to([s["C"].get_center()[0], CY + 2.45, 0])
            p = pbadge(0.2).move_to(t.get_corner(UR) + [0.05, 0.05, 0])
            outs += [t, p]
        self.play(*[FadeIn(o, shift=DOWN * 0.1) for o in outs], run_time=0.7)

        self.at("anchoring protein")
        self.play(FadeOut(VGroup(*outs)), run_time=0.4)
        hedge = T("evidence: anchored kinase may act on nearby targets\nwithout fully coming apart", 24, GOLD, line_spacing=0.6).move_to([0, 2.6, 0])
        self.play(FadeIn(hedge), run_time=0.5)
        self.at("textbook picture")
        tb = T("the textbook picture", 28, GREEN).move_to(cm)
        self.play(ReplacementTransform(cm, tb), run_time=0.5)
        self.at("may not hold")
        nh = T("may not hold everywhere", 28, GOLD).move_to(tb)
        self.play(ReplacementTransform(tb, nh), run_time=0.5)

        # the rule: close it again, then cAMP fills the sites
        self.at("held shut")
        back = []
        back += [L["C"].animate.shift(RIGHT * dr).set_stroke(BLUE), L["slot"].animate.shift(RIGHT * dr),
                 L["lc"].animate.shift(RIGHT * dr),
                 Rt["C"].animate.shift(LEFT * dr).set_stroke(BLUE), Rt["slot"].animate.shift(LEFT * dr),
                 Rt["lc"].animate.shift(LEFT * dr),
                 L["tab"].animate.shift(LEFT * 0.75), Rt["tab"].animate.shift(RIGHT * 0.75)]
        back += [m.animate.stretch(1 / 0.78, 0) for m in (L["R"], Rt["R"])]
        back += [s.animate.set_fill(TEAL, 0.0).set_color(TEAL) for s in sites]
        self.play(FadeOut(VGroup(hedge, nh)), *back, run_time=1.0)
        rule = T("held shut by its own partner", 30, YELLOW).move_to([0, 2.7, 0])
        self.play(FadeIn(rule), run_time=0.4)
        self.at("fills the sites")
        self.play(FadeOut(rule), *[s.animate.set_fill(TEAL, 0.9) for s in sites],
                  *[m.animate.stretch(0.78, 0) for m in (L["R"], Rt["R"])],
                  L["tab"].animate.shift(RIGHT * 0.75), Rt["tab"].animate.shift(LEFT * 0.75),
                  L["C"].animate.shift(LEFT * dr).set_stroke(GREEN), L["slot"].animate.shift(LEFT * dr),
                  L["lc"].animate.shift(LEFT * dr),
                  Rt["C"].animate.shift(RIGHT * dr).set_stroke(GREEN), Rt["slot"].animate.shift(RIGHT * dr),
                  Rt["lc"].animate.shift(RIGHT * dr), run_time=1.2)
        self.finish()


class S05End(EndCard):
    LINE = "A kinase held shut by its own partner until cAMP fills the sites."
