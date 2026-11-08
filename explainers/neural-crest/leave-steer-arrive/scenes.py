"""Neural crest, chapter 3: Leave, Steer, Arrive: The Puzzle Solved.

COLOR MAP (extends the lesson's earlier film; chapters 1 and 2 share it)
  YELLOW = neural crest cells (and their front in the gut toy model)
  BLUE   = surface proteins of crest cells: Cadherin-6B clasps and the EDNRB receptor
  VIOLET = genes and transcription factors that act inside the cell (Snail2, SOX10)
  RED    = repulsion, exclusion, failure, missing (back half, ephrin-B, semaphorin 3F, no neurons)
  GREEN  = permitted route (front half) and attractive direction (the chemokine gradient)
  TEAL   = enteric (gut-wall) nerve cells and their precursors
  TEXT   = melanocytes (neutral white, as in the earlier film)
  ORANGE = the EDN3 signal
  GREY   = embryonic structure and labels
  GOLD   = predict cards and explanatory highlights
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

VIOLET = "#B48CE8"
ORANGE = "#EE9B4D"
DARK = "#3A3F4C"
LGREY = "#C3C9D6"   # brighter grey for readable corner labels and notes
FX, FY = 6.8, 3.8


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, x, y, size=24, color=TEXT, left=False, **kw):
    m = T(text, size, color, **kw).move_to([x, y, 0])
    if left:
        m.align_to(np.array([x, 0, 0]), LEFT)
    return m


def cell(r=0.3, x=0, y=0, op=0.9, color=YELLOW):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color,
                  fill_opacity=op).move_to([x, y, 0])


def arr(a, b, color=GREY, sw=4, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=sw, tip_length=tip, max_tip_length_to_length_ratio=0.4)


def tbar(a, b, color=VIOLET, w=0.3, sw=5):
    a = np.array(a, float)
    b = np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=sw), Line(b + n * w, b - n * w, color=color, stroke_width=sw + 1))


def xmark(x, y, s=0.25, color=RED, sw=6):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=sw),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=sw))


def chip_dim(c, a):
    return [c[0].animate.set_stroke(opacity=a).set_fill(opacity=0.16 * a), c[1].animate.set_opacity(a)]


def chip_set(c, a):
    c[0].set_stroke(opacity=a)
    c[0].set_fill(opacity=0.16 * a)
    c[1].set_opacity(a)


def after(delay, anim):
    return Succession(Wait(delay), anim) if delay > 0.01 else anim


def corner_label():
    return lab("chick experiments", 5.1, 3.5, 26, LGREY)


class Timer:
    """A quiet draining ring for the think-time pauses."""

    @staticmethod
    def make(scene, center, secs, r=0.38):
        v = ValueTracker(0)
        ring = Circle(radius=r, stroke_color=GREY, stroke_width=3, stroke_opacity=0.5).move_to(center)
        arc = always_redraw(lambda: Arc(radius=r, start_angle=PI / 2, angle=max(2 * PI * (1 - v.get_value()), 1e-3),
                                        arc_center=center, stroke_color=GOLD, stroke_width=6))
        scene.add(ring, arc)
        return v


class QA:
    """Logs any text outside the frame or overlapping other text at the end of each scene."""

    def qa(self, tag="end"):
        try:
            texts = []
            for m in self.mobjects:
                for f in m.get_family():
                    if isinstance(f, Text) and len(f.submobjects) and f.submobjects[0].get_fill_opacity() > 0.1:
                        texts.append(f)
            log = []
            for f in texts:
                l, r, t, b = f.get_left()[0], f.get_right()[0], f.get_top()[1], f.get_bottom()[1]
                if l < -FX or r > FX or t > FY or b < -FY:
                    log.append(f"OUT   {f.text!r} x[{l:.2f},{r:.2f}] y[{b:.2f},{t:.2f}]")
            for i in range(len(texts)):
                for j in range(i + 1, len(texts)):
                    a, c = texts[i], texts[j]
                    if (a.get_left()[0] < c.get_right()[0] - 0.03 and c.get_left()[0] < a.get_right()[0] - 0.03 and
                            a.get_bottom()[1] < c.get_top()[1] - 0.03 and c.get_bottom()[1] < a.get_top()[1] - 0.03):
                        log.append(f"OVER  {a.text!r} / {c.text!r}")
            import os
            from pathlib import Path
            d = Path(os.environ["KX_SCRIPT"]).parent / "scratch"
            d.mkdir(exist_ok=True)
            with open(d / "qa.log", "a") as lg:
                lg.write(f"{os.environ.get('KX_SCENE_ID')} {tag}: {len(texts)} texts, {len(self.mobjects)} objects\n")
                for line in log:
                    lg.write("   " + line + "\n")
        except Exception as e:  # never let QA break a render
            print("qa failed", e)

    def finish(self):
        self.qa()
        super().finish()


class Sc(QA, SpokenScene):
    pass


class Still(QA, NarratedScene):
    pass




# ---------------------------------------------------------------------------------------------
# title
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Neural Crest: Cells That Leave Home"
    TITLE = "Leave, Steer, Arrive: The Puzzle Solved"


# ---------------------------------------------------------------------------------------------
# s01: the question as three icons (built in their final place)
# ---------------------------------------------------------------------------------------------
class S01Q(Sc):
    def construct(self):
        X = [-4.2, 0.0, 4.2]
        LY = -3.1
        # icon 1: a sheet of cells, one lets go
        r1 = 0.62
        sy = -0.9
        row = [cell(r1, X[0] + dx, sy, 0.85) for dx in (-1.3, 0, 1.3)]
        sheet = VGroup(*row)
        l1 = lab("let go", X[0], LY, 34)
        ghost = DashedVMobject(Circle(radius=r1, color=GREY, stroke_width=3).move_to([X[0], sy, 0]), num_dashes=14)
        up = arr([X[0], sy + 0.85, 0], [X[0], sy + 1.9, 0], YELLOW, 6)
        # icon 2: a forked path with unknown ends
        stem = Line([X[1], -2.2, 0], [X[1], -0.6, 0], color=GREY, stroke_width=12)
        br1 = Line([X[1], -0.6, 0], [X[1] - 1.7, 1.7, 0], color=GREY, stroke_width=12)
        br2 = Line([X[1], -0.6, 0], [X[1] + 1.7, 1.7, 0], color=GREY, stroke_width=12)
        q1 = T("?", 72, GOLD, weight=BOLD).move_to([X[1] - 1.9, 2.5, 0])
        q2 = T("?", 72, GOLD, weight=BOLD).move_to([X[1] + 1.9, 2.5, 0])
        walker = cell(0.45, X[1], -1.9)
        l2 = lab("find its way", X[1], LY, 34)
        # icon 3: a broken link
        cy = 0.2
        lk1 = RoundedRectangle(corner_radius=0.55, width=2.1, height=1.25, stroke_color=TEXT, stroke_width=11).move_to([X[2] - 1.2, cy, 0])
        lk2 = RoundedRectangle(corner_radius=0.55, width=2.1, height=1.25, stroke_color=TEXT, stroke_width=11).move_to([X[2] + 1.2, cy, 0])
        crack = VMobject(color=RED, stroke_width=9).set_points_as_corners(
            [[X[2] + dx, cy + dy, 0] for dx, dy in [(-0.2, 1.1), (0.3, 0.5), (-0.3, -0.1), (0.3, -0.7), (-0.15, -1.2)]])
        l3 = lab("a step fails", X[2], LY, 34)
        icons = [VGroup(sheet, ghost, up), VGroup(stem, br1, br2, walker, q1, q2), VGroup(lk1, lk2, crack)]
        for icon, x in zip(icons, X):
            icon.scale(1.08, about_point=np.array([x, 0, 0]))
        self.play(*[FadeIn(icon) for icon in icons], run_time=0.5)
        self.at("let go")
        self.play(row[1].animate.shift(UP * 2.9), FadeIn(l1), run_time=0.6)
        self.at("find its way")
        self.play(Indicate(walker, scale_factor=1.25), FadeIn(l2), run_time=0.6)
        self.at("what happens")
        self.play(Indicate(crack, color=RED), FadeIn(l3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s02-s07: Snail2 and Cadherin-6B (chick experiments)
# ---------------------------------------------------------------------------------------------
SHEET_X = [-3.9, -1.95, 0.0, 1.95, 3.9]
SHEET_Y = -0.35


def sheet_bodies():
    return [Ellipse(width=1.8, height=3.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                    fill_opacity=0.3).move_to([x, SHEET_Y, 0]) for x in SHEET_X]


def sheet_clasps():
    out = []
    for g in range(4):
        gx = (SHEET_X[g] + SHEET_X[g + 1]) / 2
        out.append(VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.5, height=0.32, stroke_color=BLUE,
                                             stroke_width=2.5, fill_color=BLUE, fill_opacity=0.85)
                            .move_to([gx, SHEET_Y + dy, 0]) for dy in (0.6, -0.6)]))
    return out


class S02Grip(Sc):
    def construct(self):
        bodies, clasps = sheet_bodies(), sheet_clasps()
        crest = lab("crest cells", 0, -2.5, 28, YELLOW)
        gx = (SHEET_X[1] + SHEET_X[2]) / 2
        clasp_lbl = lab("clasps", gx, 2.15, 28, BLUE)
        leader = Line([gx, 1.85, 0], [gx, SHEET_Y + 0.6 + 0.22, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(VGroup(*bodies)), FadeIn(VGroup(*clasps)), FadeIn(crest), run_time=0.7)
        self.play(FadeIn(clasp_lbl), Create(leader), run_time=0.5)
        mid = bodies[2]
        for m in bodies + clasps:
            m.save_state()
        self.at("loosen its grip")
        # one cell lets go: its clasps thin out and it lifts away
        thin = [c.animate.stretch(0.35, 0).set_opacity(0.4) for c in (clasps[1], clasps[2])]
        self.play(mid.animate.shift(UP * 0.75), *thin, run_time=1.0)
        corner = corner_label()
        self.at("in chick")
        self.play(FadeIn(corner), run_time=0.5)
        self.at("called")
        chipc = chip("Cadherin-6B", BLUE, size=32).move_to([gx, 2.2, 0])
        self.play(ReplacementTransform(clasp_lbl, chipc), run_time=0.7)
        self.at("helps hold")
        self.play(mid.animate.shift(DOWN * 0.75), Restore(clasps[1]), Restore(clasps[2]), run_time=0.7)
        self.play(*[Indicate(c, color=BLUE, scale_factor=1.3) for c in clasps], run_time=0.8)
        self.finish()


class S03Snail(Sc):
    def construct(self):
        bodies, clasps = sheet_bodies(), sheet_clasps()
        crest = lab("crest cells", 0, -2.5, 28, YELLOW)
        corner = corner_label()
        self.add(*bodies, *clasps, crest, corner)
        nucs = [Circle(radius=0.72, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET, fill_opacity=0.28)
                .move_to([x, SHEET_Y, 0]) for x in SHEET_X]
        labs = [T("Snail2", 26, VIOLET).move_to([x, SHEET_Y, 0]) for x in SHEET_X]
        xm = [xmark(x, SHEET_Y + 1.15, 0.2, RED, 7) for x in SHEET_X]
        DY = 1.2

        def grp(i):
            return [bodies[i], nucs[i], labs[i]]

        self.at("transcription factor")
        self.play(*[FadeIn(n) for n in nucs], run_time=0.6)
        self.at("snail 2")
        self.play(*[FadeIn(l) for l in labs], run_time=0.5)
        self.at("is needed")
        # control beat: every cell leaves
        ctl = lab("control: all cells leave", -6.6, 3.35, 26, LGREY, left=True)
        self.play(*[m.animate.shift(UP * DY) for i in range(5) for m in grp(i)], *[FadeOut(c) for c in clasps],
                  FadeIn(ctl), run_time=0.7)
        self.wait(0.2)
        self.at("block it", lead=0.35)
        # reset and block Snail2 in every cell
        self.play(*[m.animate.shift(DOWN * DY) for i in range(5) for m in grp(i)], *[FadeIn(c) for c in clasps],
                  FadeOut(ctl), run_time=0.4)
        self.play(*[n.animate.set_stroke(color=GREY).set_fill(GREY, opacity=0.15) for n in nucs],
                  *[l.animate.set_color(GREY) for l in labs], *[Create(x) for x in xm], run_time=0.5)
        self.at("fewer cells leave")
        fl = lab("fewer cells leave", 1.25, 2.25, 28, LGREY, left=True)
        self.play(*[m.animate.shift(UP * DY) for m in grp(2)], *[x.animate.shift(UP * DY) for x in [xm[2]]],
                  FadeOut(clasps[1]), FadeOut(clasps[2]), FadeIn(fl), run_time=0.7)
        self.finish()


def pred_parts():
    snail = chip("Snail2", VIOLET, size=36).move_to([-4.4, 2.0, 0])
    gene = chip("Cadherin-6B gene", BLUE, size=36).move_to([2.7, 2.0, 0])
    tb = tbar(snail.get_right() + RIGHT * 0.12, gene.get_left() + LEFT * 0.15, VIOLET)
    dashed = VGroup(DashedLine(snail.get_right() + RIGHT * 0.12, gene.get_left() + LEFT * 0.15, color=VIOLET, stroke_width=5, dash_length=0.14),
                    Line(gene.get_left() + LEFT * 0.15 + UP * 0.3, gene.get_left() + LEFT * 0.15 + DOWN * 0.3, color=VIOLET, stroke_width=6))
    qm = T("?", 44, GOLD, weight=BOLD).move_to([-0.9, 2.65, 0])
    hyp = VGroup(dashed, qm)
    lowered = VGroup(arr([-4.4, 1.35, 0], [-4.4, 0.85, 0], VIOLET, 5), lab("lowered", -4.4, 0.45, 26, VIOLET))
    # RNA mini-plot: control bar, test bar, time ticks
    base_y = -2.45
    bar_c = Rectangle(width=1.2, height=1.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                      fill_opacity=0.55).move_to([-5.2, base_y + 0.6, 0])
    bar = Rectangle(width=1.2, height=1.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.55).move_to([-3.4, base_y + 0.6, 0])
    ref = DashedLine([-5.9, base_y + 1.2, 0], [-2.6, base_y + 1.2, 0], color=GREY, stroke_width=3, dash_length=0.12)
    axis = Line([-5.9, base_y, 0], [-2.6, base_y, 0], color=GREY, stroke_width=3)
    t_c = lab("control", -5.2, base_y - 0.35, 26, LGREY)
    t_n = lab("test", -3.4, base_y - 0.35, 26, LGREY)
    rname = lab("Cadherin-6B RNA (relative to control)", -6.6, -3.55, 26, BLUE, left=True)
    return dict(snail=snail, gene=gene, tb=tb, hyp=hyp, lowered=lowered, bar=bar, bar_c=bar_c, ref=ref, axis=axis,
                t_c=t_c, t_n=t_n, rname=rname, card=pred_card())


def pred_card():
    cx, cy = 3.4, -0.9
    box = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.2, stroke_color=GOLD, stroke_width=3,
                           fill_color=GOLD, fill_opacity=0.07).move_to([cx, cy, 0])
    head = T("PREDICT", 24, GOLD, weight=BOLD).move_to([cx, cy + 1.2, 0])
    l1 = T("Snail2 lowered", 30, VIOLET).move_to([cx, cy + 0.55, 0])
    l2 = T("Cadherin-6B RNA:", 30, BLUE).move_to([cx, cy - 0.1, 0])
    upa = arr([cx - 2.1, cy - 1.25, 0], [cx - 2.1, cy - 0.65, 0], GOLD, 6)
    txt = T("up or down?", 34, GOLD).move_to([cx, cy - 0.95, 0])
    dna = arr([cx + 2.1, cy - 0.65, 0], [cx + 2.1, cy - 1.25, 0], GOLD, 6)
    g = VGroup(box, head, l1, l2, upa, txt, dna)
    g.upa, g.dna, g.txt = upa, dna, txt
    return g


def test_bar_ghost(p):
    g = DashedVMobject(Rectangle(width=1.2, height=1.2, color=GREY, stroke_width=3).move_to(p["bar"]), num_dashes=20)
    q = T("?", 40, GOLD, weight=BOLD).move_to(p["bar"])
    return VGroup(g, q)


def add_pred_final(scene):
    p = pred_parts()
    chip_set(p["snail"], 0.4)
    ghost = test_bar_ghost(p)
    scene.add(corner_label(), p["snail"], p["gene"], p["hyp"], p["lowered"], p["bar_c"], p["ref"], p["axis"],
              p["t_c"], p["t_n"], p["rname"], ghost, p["card"])
    p["ghost"] = ghost
    return p


class S04Pred(Sc):
    def construct(self):
        p = pred_parts()
        self.play(FadeIn(p["snail"]), FadeIn(p["gene"]), FadeIn(corner_label()), run_time=0.5)
        self.at("switching off")
        self.play(Create(p["hyp"]), run_time=0.9)
        self.at("lower snail")
        ghost = test_bar_ghost(p)
        self.play(*chip_dim(p["snail"], 0.4), FadeIn(p["lowered"]), FadeIn(p["bar_c"]), FadeIn(p["ref"]),
                  FadeIn(p["axis"]), FadeIn(p["t_c"]), FadeIn(p["t_n"]), FadeIn(p["rname"]), FadeIn(ghost), run_time=0.8)
        self.at("what happens to")
        self.play(FadeIn(p["card"]), run_time=0.8)
        self.finish()


class S05Pause(Still):
    def construct(self):
        add_pred_final(self)
        v = Timer.make(self, [6.35, -3.3, 0], 5.0, r=0.35)
        self.play(v.animate(run_time=4.6, rate_func=linear).set_value(1))
        self.finish()


class S06Rev(Sc):
    def construct(self):
        p = add_pred_final(self)
        plot = VGroup(*[p[k] for k in ("bar_c", "ref", "axis", "t_c", "t_n", "ghost")])
        plot.scale(1.12, about_point=np.array([-4.3, -2.45, 0]))
        self.play(FadeOut(p["ghost"]), run_time=0.3)
        self.remove(p["ghost"])
        self.play(Indicate(p["bar_c"], color=BLUE, scale_factor=1.1), run_time=0.5)
        self.at("rises")
        new_bar = Rectangle(width=1.344, height=2.688, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                            fill_opacity=0.55).move_to([-3.292, -2.45 + 1.344, 0])
        self.play(GrowFromEdge(new_bar, DOWN), run_time=0.9)
        self.at("half an hour")
        t30 = lab("30 min", -3.4, -2.8, 26, GOLD)
        self.play(Transform(p["t_n"], t30), run_time=0.5)
        self.at("just as predicted")
        self.play(p["card"].upa.animate.set_color(GREEN), p["card"].dna.animate.set_opacity(0.2),
                  Transform(p["card"].txt, T("up", 34, GREEN).move_to(p["card"].txt)), run_time=0.7)
        self.at("concluded")
        self.play(FadeOut(p["card"]), run_time=0.6)
        self.at("represses")
        # direct binding, shown as a separate inset; the main condition (Snail2 lowered) stays
        strip = Rectangle(width=4.8, height=0.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([3.3, -1.7, 0])
        sn = chip("Snail2", VIOLET, size=28).move_to([1.7, -0.7, 0])
        touch = tbar([1.7, -1.05, 0], [1.7, -1.48, 0], VIOLET, w=0.25)
        gl = lab("Cadherin-6B gene", 3.3, -2.45, 26, BLUE)
        il = lab("binds the gene", 4.9, -0.7, 26, VIOLET)
        solid = VGroup(Line(p["snail"].get_right() + RIGHT * 0.12, p["gene"].get_left() + LEFT * 0.15, color=VIOLET, stroke_width=5),
                       Line(p["gene"].get_left() + LEFT * 0.15 + UP * 0.3, p["gene"].get_left() + LEFT * 0.15 + DOWN * 0.3, color=VIOLET, stroke_width=6))
        inset = VGroup(strip, sn, touch, gl, il)
        inset.scale(1.15, about_point=np.array([3.3, -1.7, 0]))
        self.play(FadeIn(strip), FadeIn(sn), Create(touch), FadeIn(gl), FadeIn(il),
                  FadeOut(p["hyp"]), FadeIn(solid), run_time=0.9)
        self.at("directly")
        self.play(Indicate(solid, color=VIOLET, scale_factor=1.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s07: the brake
# ---------------------------------------------------------------------------------------------
def dep_row(y, name, xs, ghosts, result):
    name_m = lab(name, -6.6, y, 28, TEXT, left=True)
    track = Arrow([-1.9, y, 0], [3.7, y, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.18)
    dots = VGroup(*[cell(0.26, x, y, 0.9) for x in xs])
    gh = VGroup(*[DashedVMobject(Circle(radius=0.26, color=GREY, stroke_width=2.5).move_to([x, y, 0]), num_dashes=10)
                  for x in ghosts])
    res = lab(result, 4.35, y, 30, TEXT, left=True)
    return name_m, VGroup(track, gh), dots, res


class S07Brake(Sc):
    def construct(self):
        self.add(corner_label())
        ya, yb, yc = 1.65, 0.3, -1.05
        r1 = dep_row(ya, "control", [1.3, 1.7, 2.1], [], "normal")
        r2 = dep_row(yb, "Snail2 lowered", [1.7], [1.3, 2.1], "reduced")
        r3 = dep_row(yc, "Cadherin-6B lowered", [-1.3, -0.9, -0.5], [], "early")
        head = lab("time of leaving", 0.9, 2.75, 28, LGREY)
        dep = lab("departure", 4.35, 2.75, 28, LGREY, left=True)
        earlier = lab("earlier", -1.9, -1.85, 26, LGREY, left=True)
        later = lab("later", 3.7, -1.85, 26, LGREY)
        later.align_to(np.array([3.7, 0, 0]), RIGHT)
        self.play(FadeIn(head), FadeIn(dep), FadeIn(earlier), FadeIn(later), *[FadeIn(m) for m in r1 + r2], run_time=0.9)
        self.at("instead")
        self.play(FadeIn(r3[0]), FadeIn(r3[1]), run_time=0.4)
        self.at("cells leave early")
        self.play(FadeIn(r3[2]), FadeIn(r3[3]), run_time=0.8)
        yy = -3.05
        snail = chip("Snail2", VIOLET, size=28).move_to([-5.2, yy, 0])
        cad = chip("Cadherin-6B", BLUE, size=28).move_to([-0.9, yy, 0])
        leave = chip("cells leave", YELLOW, size=28).move_to([4.5, yy, 0])
        tb2 = tbar(cad.get_right() + RIGHT * 0.08, leave.get_left() + LEFT * 0.12, BLUE)
        mid = (tb2[0].get_start()[0] + tb2[0].get_end()[0]) / 2
        brake = lab("a brake", mid, yy + 0.45, 28, GOLD)
        self.at("it is a")
        self.play(FadeIn(cad), FadeIn(leave), Create(tb2), FadeIn(brake), run_time=0.9)
        self.at("snail 2 probably")
        tb1 = DashedLine(snail.get_right() + RIGHT * 0.08, cad.get_left() + LEFT * 0.4, color=VIOLET, stroke_width=5, dash_length=0.14)
        bar1 = Line(cad.get_left() + LEFT * 0.4 + UP * 0.3, cad.get_left() + LEFT * 0.4 + DOWN * 0.3, color=VIOLET, stroke_width=6)
        self.play(FadeIn(snail), Create(tb1), Create(bar1), run_time=0.8)
        self.at("at least partly")
        self.play(Indicate(tb1, color=VIOLET, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s08-s10: steering by exclusion
# ---------------------------------------------------------------------------------------------
BX = [-4.5, -1.5, 1.5, 4.5]
BY, BH = -0.15, 4.2


class S08Routes(Sc):
    def construct(self):
        tube = RoundedRectangle(corner_radius=0.3, width=12.2, height=0.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.2).move_to([0, 2.9, 0])
        tl = lab("neural tube", 4.6, 2.9, 26, LGREY)
        blocks = VGroup(*[Rectangle(width=2.8, height=BH, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([x, BY, 0]) for x in BX])
        divs = VGroup(*[DashedLine([x, BY + BH / 2, 0], [x, BY - BH / 2, 0], color=GREY, stroke_width=2, dash_length=0.12) for x in BX])
        front = [Rectangle(width=1.4, height=BH, stroke_width=0, fill_color=GREEN, fill_opacity=0).move_to([x - 0.7, BY, 0]) for x in BX]
        back = [Rectangle(width=1.4, height=BH, stroke_width=0, fill_color=RED, fill_opacity=0).move_to([x + 0.7, BY, 0]) for x in BX]
        self.add(*front, *back)
        self.play(FadeIn(tube), FadeIn(tl), FadeIn(blocks), FadeIn(divs), run_time=0.9)
        self.at("the chick trunk")
        self.play(FadeIn(lab("chick trunk", 5.4, 3.55, 26, LGREY)), run_time=0.4)
        ytop = BY + BH / 2 + 0.3
        dots = [[cell(0.18, x - 0.7, 1.65 - j * 1.2) for j in range(3)] for x in BX]
        for g in dots:
            for d in g:
                d.set_opacity(0)
        self.add(*[d for g in dots for d in g])
        self.at("crest cells")
        self.play(*[d.animate.set_opacity(0.95) for g in dots for d in g], run_time=0.4)
        self.at("pass")
        ylab = BY - BH / 2 - 0.4
        flabs = [lab("front", x - 0.7, ylab, 26, GREEN) for x in BX]
        blabs = [lab("back", x + 0.7, ylab, 26, RED) for x in BX]
        slab = lab("sclerotome", BX[0], -3.55, 28, LGREY)
        brace = Brace(blocks[0], DOWN, buff=0.75, color=LGREY)
        self.play(*[f.animate.set_fill(GREEN, opacity=0.3) for f in front],
                  *[b.animate.set_fill(RED, opacity=0.3) for b in back],
                  *[FadeIn(t) for t in flabs + blabs], FadeIn(slab), FadeIn(brace), run_time=0.4)
        self.play(*[d.animate.shift(DOWN * 1.05) for g in dots for d in g], run_time=1.5, rate_func=linear)
        self.finish()


PY0, PH = 0.1, 5.9


def halves_parts():
    pf = Rectangle(width=6.3, height=PH, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.16).move_to([-3.25, PY0, 0])
    pb = Rectangle(width=6.3, height=PH, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.16).move_to([3.25, PY0, 0])
    lf = lab("front half", -3.25, 2.4, 28, GREEN)
    lb = lab("back half", 3.25, 2.4, 28, RED)
    specs = [(1.4, 0.0, 0.9), (3.8, 1.1, 0.7), (3.8, -1.1, 0.7), (1.6, 1.65, 0.0), (1.6, -1.65, 0.0)]
    red_cells = VGroup(*[Circle(radius=r, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.5).move_to([x, y, 0])
                         for x, y, r in specs if r > 0])
    bl = lab("back-half cells", 3.8, -2.55, 26, RED)
    return pf, pb, lf, lb, red_cells, bl


def lollipops(centers=((1.4, 0.0, 0.9), (3.8, 1.1, 0.7), (3.8, -1.1, 0.7))):
    out = VGroup()
    for cx, cy, r in centers:
        for ang in (150, 175, 200, 225, 130):
            a = np.radians(ang)
            d = np.array([np.cos(a), np.sin(a), 0])
            c = np.array([cx, cy, 0])
            p0, p1 = c + d * r, c + d * (r + 0.38)
            out.add(VGroup(Line(p0, p1, color=RED, stroke_width=4), Dot(p1, radius=0.08, color=RED)))
    return out


def ephrin_label():
    ic = VGroup(Line([0, 0, 0], [0.25, 0, 0], color=RED, stroke_width=4), Dot([0.25, 0, 0], radius=0.08, color=RED))
    t = T("ephrin-B (chick studies)", 26, TEXT)
    g = VGroup(ic, t).arrange(RIGHT, buff=0.15)
    return g.move_to([3.1, -2.05, 0])


def sema_label():
    ic = Square(side_length=0.2, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.9).rotate(PI / 4)
    t = T("semaphorin 3F (mouse studies)", 26, TEXT)
    g = VGroup(ic, t).arrange(RIGHT, buff=0.15)
    return g.move_to([-3.2, -3.45, 0])


class S09Ephrin(Sc):
    def construct(self):
        pf, pb, lf, lb, rc, bl = halves_parts()
        crest = cell(0.55, -4.8, 0.0)
        self.play(FadeIn(pf), FadeIn(pb), FadeIn(lf), FadeIn(lb), FadeIn(rc), FadeIn(crest), run_time=0.3)
        self.at("back half")
        self.play(FadeIn(bl), run_time=0.4)
        self.at("repels")
        self.play(crest.animate.move_to([-0.05, 0.0, 0]), run_time=1.0, rate_func=smooth)
        lol = lollipops()
        self.add(ephrin_label())
        self.play(FadeIn(lol), Flash(np.array([0.5, 0.0, 0]), color=TEXT, line_length=0.3, flash_radius=0.45, run_time=0.5))
        self.wait(0.5)
        self.at("in check", lead=0.3)
        self.play(crest.animate.move_to([-3.8, 0.0, 0]), run_time=1.0)
        self.finish()


class S10Sema(Sc):
    def construct(self):
        pf, pb, lf, lb, rc, bl = halves_parts()
        crest = cell(0.55, -3.8, 0.0)
        self.add(pf, pb, lf, lb, rc, bl, crest, lollipops(), ephrin_label().move_to([3.4, -3.45, 0]))
        self.at("semaphorin")
        pts = [(1.0, 2.0), (2.5, 2.0), (5.3, 2.0), (2.6, -2.0), (1.0, -2.0), (0.6, 1.0), (0.6, -1.0), (5.2, -2.0)]
        dia = VGroup(*[Square(side_length=0.22, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.9).rotate(PI / 4).move_to([x, y, 0]) for x, y in pts])
        self.play(LaggedStart(*[FadeIn(d) for d in dia], lag_ratio=0.1), FadeIn(sema_label()), run_time=0.9)
        self.play(crest.animate.move_to([-0.05, 0.0, 0]), run_time=0.9, rate_func=smooth)
        self.play(Flash(np.array([0.5, 0.0, 0]), color=TEXT, line_length=0.3, flash_radius=0.4, run_time=0.4))
        self.play(crest.animate.move_to([-3.8, 0.0, 0]), run_time=0.9)
        self.at("neither is known")
        q = VGroup(DashedVMobject(Circle(radius=0.42, color=GOLD, stroke_width=3), num_dashes=12), T("?", 40, GOLD, weight=BOLD)).move_to([5.45, 0.65, 0])
        ql = lab("other\ncues?", 5.45, -0.3, 26, GOLD, line_spacing=0.9)
        self.play(FadeIn(q), FadeIn(ql), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s11: crest cells steer each other
# ---------------------------------------------------------------------------------------------
CR = 0.85   # one cell size for the whole scene


def cil_cell(cx, cy, facing_right, r=CR):
    """A cell with protrusions; returns (body, contact protrusions, other protrusions)."""
    body = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).move_to([cx, cy, 0])

    def prot(deg):
        a = np.radians(deg)
        c = np.array([cx, cy, 0]) + (r + 0.12) * np.array([np.cos(a), np.sin(a), 0])
        return Ellipse(width=0.85, height=0.36, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW,
                       fill_opacity=0.6).rotate(a).move_to(c)

    base = [0, 28, -28] if facing_right else [180, 152, 208]
    others = [75, 115, 245, 285] if facing_right else [105, 65, 295, 255]
    others += [150, 205] if facing_right else [30, -25]
    return body, VGroup(*[prot(d) for d in base]), VGroup(*[prot(d) for d in others])


class S11Cil(Sc):
    def construct(self):
        y = 0.4
        ab, ac, ao = cil_cell(-3.8, y, True)
        bb, bc, bo = cil_cell(3.8, y, False)
        A, B = VGroup(ab, ac, ao), VGroup(bb, bc, bo)
        crest_l = lab("crest cells", 0, -2.0, 28, YELLOW)
        self.play(FadeIn(A), FadeIn(B), FadeIn(crest_l), run_time=0.6)
        self.at("when two touch")
        self.play(A.animate.shift(RIGHT * 2.4), B.animate.shift(LEFT * 2.4), run_time=0.7, rate_func=linear)
        # centres are now at -1.4 and 1.4: the facing protrusions just touch at the middle
        cl = lab("contact", 0, 2.3, 30, TEXT)
        ld = Line([0, 1.95, 0], [0, y + 0.15, 0], color=TEXT, stroke_width=3)
        self.play(Flash(np.array([0, y, 0]), color=TEXT, line_length=0.3, flash_radius=0.45, run_time=0.3),
                  FadeIn(cl), Create(ld), FadeOut(crest_l), run_time=0.4)
        self.at("collapse protrusions")
        col = lab("protrusions collapse", 0, 2.3, 30, GOLD)
        self.play(ShrinkToCenter(ac), ShrinkToCenter(bc), Transform(cl, col), run_time=0.8)
        self.at("move apart")
        la = arr([-1.5, -1.9, 0], [-3.1, -1.9, 0], GREY, 5)
        lb_ = arr([1.5, -1.9, 0], [3.1, -1.9, 0], GREY, 5)
        self.play(A.animate.shift(LEFT * 2.2), B.animate.shift(RIGHT * 2.2), GrowArrow(la), GrowArrow(lb_),
                  FadeOut(cl), FadeOut(ld), run_time=1.2)
        self.at("edge cells")
        cluster = VGroup(cell(CR, 0, 0.2, 0.5))
        arrows = VGroup()
        for k in range(6):
            a = np.radians(90 + 60 * k)
            d = np.array([np.cos(a), np.sin(a), 0])
            c = np.array([0, 0.2, 0]) + 1.8 * d
            cluster.add(cell(CR, c[0], c[1], 0.5))
            arrows.add(arr(c + (CR + 0.1) * d, c + (CR + 0.65) * d, YELLOW, 5))
        note = lab("edge cells\nmove outward", 5.0, 0.2, 28, LGREY, line_spacing=0.9)
        self.play(FadeOut(A), FadeOut(B), FadeOut(la), FadeOut(lb_), FadeIn(cluster), run_time=0.6)
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(note), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s12: the recipe
# ---------------------------------------------------------------------------------------------
def recipe_rows():
    ys = [2.15, 0.0, -2.15]
    card = RoundedRectangle(corner_radius=0.3, width=13.0, height=6.9, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.05)
    cx = [-5.2, -4.2]
    r = 0.48
    r1 = VGroup(cell(r, cx[0] + 0.2, ys[0], 0.8), cell(r, cx[1] + 0.2, ys[0], 0.8),
                arr([cx[0] - 0.4, ys[0], 0], [cx[0] - 1.1, ys[0], 0], RED, 6), arr([cx[1] + 0.8, ys[0], 0], [cx[1] + 1.5, ys[0], 0], RED, 6),
                lab("contact pushes apart", -2.3, ys[0], 38, TEXT, left=True))
    r2 = VGroup(cell(r, cx[0] + 0.2, ys[1], 0.8), cell(r, cx[1] + 0.2, ys[1], 0.8),
                arr([cx[0] - 1.1, ys[1], 0], [cx[0] - 0.4, ys[1], 0], YELLOW, 6), arr([cx[1] + 1.5, ys[1], 0], [cx[1] + 0.8, ys[1], 0], YELLOW, 6),
                lab("attraction holds", -2.3, ys[1], 38, TEXT, left=True))
    grad = VGroup(*[Rectangle(width=0.36, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.1 + 0.14 * i)
                    .move_to([-6.45 + 0.36 * i, ys[2] - 0.0, 0]) for i in range(0)])
    gx = [-6.45 + 0.0]
    r3 = VGroup(cell(r, cx[0] + 0.2, ys[2], 0.8), cell(r, cx[1] + 0.2, ys[2], 0.8),
                arr([cx[1] + 0.8, ys[2], 0], [cx[1] + 1.7, ys[2], 0], GREEN, 6),
                lab("chemokine steers", -2.3, ys[2], 38, TEXT, left=True))
    return card, r1, r2, r3


class S12Recipe(Sc):
    def construct(self):
        card, r1, r2, r3 = recipe_rows()
        r1.set_opacity(0.6)
        r3.set_opacity(0.3)
        self.add(card, r1, r2, r3)
        self.at("attraction")
        self.play(Indicate(r2, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("chemokine")
        self.play(r3.animate.set_opacity(1.0), Indicate(r3, color=GREEN, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s13: a cluster follows the chemokine better than a lone cell
# ---------------------------------------------------------------------------------------------
class S13Cluster(Sc):
    def construct(self):
        grad = VGroup(*[Rectangle(width=1.05, height=5.4, stroke_width=0, fill_color=GREEN, fill_opacity=0.02 + 0.03 * i)
                        .move_to([-6.0 + 1.05 * i, -0.1, 0]) for i in range(12)])
        low = lab("low", -6.3, -3.3, 26, LGREY, left=True)
        high = lab("high", 6.4, -3.3, 26, LGREY)
        high.align_to(np.array([6.5, 0, 0]), RIGHT)
        chem = lab("chemokine", 0, -3.3, 28, GREEN)
        gl = Arrow([-5.2, -3.3, 0], [-1.6, -3.3, 0], buff=0, color=GREEN, stroke_width=4, tip_length=0.18)
        gr = Arrow([1.6, -3.3, 0], [5.4, -3.3, 0], buff=0, color=GREEN, stroke_width=4, tip_length=0.18)
        frog = lab("frog cranial crest", -6.6, 3.5, 28, LGREY, left=True)
        cl_pos = [(-0.35, -0.35), (0.35, -0.35), (-0.35, 0.35), (0.35, 0.35)]
        cluster = VGroup(*[cell(0.32, -5.0 + dx, 1.0 + dy, 0.85) for dx, dy in cl_pos])
        lone = cell(0.32, -5.0, -0.9, 0.85)
        t_cl = always_redraw(lambda: lab("cluster", cluster.get_center()[0], cluster.get_center()[1] + 0.95, 28, YELLOW))
        t_lo = always_redraw(lambda: lab("lone cell", lone.get_center()[0], lone.get_center()[1] + 0.7, 28, YELLOW))
        self.add(grad)
        self.play(FadeIn(frog), FadeIn(low), FadeIn(high), FadeIn(chem), Create(gl), Create(gr),
                  FadeIn(cluster), FadeIn(lone), FadeIn(t_cl), FadeIn(t_lo), run_time=0.7)
        self.at("a cluster follows")
        # the lone cell wanders: sideways and back, little net progress
        path_l = ParametricFunction(lambda t: np.array([-5.0 + 1.5 * t + 0.9 * np.sin(2 * np.pi * 2.5 * t),
                                                        -0.9 + 0.7 * np.sin(2 * np.pi * 3.1 * t + 1.0) - 0.7 * np.sin(1.0), 0]),
                                    t_range=[0, 1], use_smoothing=False)
        self.play(cluster.animate.shift(RIGHT * 9.4), MoveAlongPath(lone, path_l), run_time=3.0, rate_func=linear)
        self.at("trunk crest")
        self.play(FadeIn(lab("less clear for trunk crest of birds and mammals", 0, 2.85, 26, LGREY)), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s14: the puzzle returns
# ---------------------------------------------------------------------------------------------
def tile(x, caption):
    box = RoundedRectangle(corner_radius=0.25, width=3.9, height=4.2, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.1).move_to([x, 0.3, 0])
    cap = lab(caption, x, -1.2, 26)
    return box, cap


def ear_icon(x, y, s=1.0):
    outer = Ellipse(width=1.3 * s, height=2.0 * s, stroke_color=TEXT, stroke_width=5, fill_opacity=0).move_to([x, y, 0])
    inner = Arc(radius=0.42 * s, start_angle=PI * 0.5, angle=PI * 1.1, stroke_color=TEXT, stroke_width=4).move_to([x + 0.05 * s, y - 0.05 * s, 0])
    lobe = Dot([x, y - 0.45 * s, 0], radius=0.08 * s, color=TEXT)
    return VGroup(outer, inner, lobe)


def puzzle_group():
    xs = [-4.4, 0.0, 4.4]
    t1, c1 = tile(xs[0], "hearing loss")
    t2, c2 = tile(xs[1], "white forelock")
    t3, c3 = tile(xs[2], "gut without\nnerve cells")
    ear = ear_icon(xs[0], 0.85, 1.3)
    head = Circle(radius=1.25, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([xs[1], 0.75, 0])
    hair = Sector(radius=1.29, angle=PI, start_angle=0, fill_color=DARK, fill_opacity=1, stroke_width=0, arc_center=np.array([xs[1], 0.75, 0]))
    lock = Ellipse(width=0.55, height=1.15, stroke_width=0, fill_color=WHITE, fill_opacity=1).rotate(-0.25).move_to([xs[1] + 0.2, 1.7, 0])
    tube = VGroup(*[Rectangle(width=1.1, height=1.2, stroke_color=GREY, stroke_width=2.5, fill_color=(TEAL if i < 2 else GREY),
                              fill_opacity=(0.4 if i < 2 else 0.15)).move_to([xs[2] - 1.1 + 1.1 * i, 0.85, 0]) for i in range(3)])
    return VGroup(t1, c1, t2, c2, t3, c3, ear, head, hair, lock, tube)


class S14Puzzle(Sc):
    def construct(self):
        g = puzzle_group()
        g.save_state()
        g.scale(0.22).move_to([6.2, 3.2, 0])
        self.add(g)
        self.play(Restore(g), run_time=1.1)
        self.at("syndrome")
        self.play(FadeIn(lab("Waardenburg syndrome type 4", 0, 3.2, 36, GOLD)), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s15, s16: the three genes in two lineages, and the ear
# ---------------------------------------------------------------------------------------------
def lineages(cy=-0.45, h=4.3, w=5.5, names_inside_top=False):
    """Two lineage ovals. Chips sit fully inside each oval; the names sit just below it."""
    top, bot = cy + h / 2, cy - h / 2
    en = Ellipse(width=w, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.16).move_to([-3.3, cy, 0])
    me = Ellipse(width=w, height=h, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.1).move_to([3.3, cy, 0])
    en_l = lab("enteric precursors", -3.3, bot - 0.38, 28, TEAL)
    me_l = lab("melanocytes", 3.3, bot - 0.38, 28, TEXT)
    ry = top - 1.15
    sy = cy - 0.45
    sox_e = chip("SOX10", VIOLET, size=28).move_to([-3.3, sy, 0])
    sox_m = chip("SOX10", VIOLET, size=28).move_to([3.3, sy, 0])
    rec_e = chip("EDNRB", BLUE, size=28).move_to([-3.3, ry, 0])
    rec_m = chip("EDNRB", BLUE, size=28).move_to([3.3, ry, 0])
    edn = chip("EDN3", ORANGE, size=32).move_to([0, 3.15, 0])
    a1 = arr([-0.7, 2.9, 0], [-2.9, ry + 0.38, 0], ORANGE, 5)
    a2 = arr([0.7, 2.9, 0], [2.9, ry + 0.38, 0], ORANGE, 5)
    return dict(en=VGroup(en, en_l, sox_e, rec_e), me=VGroup(me, me_l, sox_m, rec_m), sox=VGroup(sox_e, sox_m),
                rec=VGroup(rec_e, rec_m), edn=edn, arrows=VGroup(a1, a2), a1=a1, a2=a2, ovals=(en, me), names=(en_l, me_l),
                cy=cy, h=h)


class S15Genes(Sc):
    def construct(self):
        L = lineages()
        self.play(FadeIn(L["en"][0]), FadeIn(L["me"][0]), FadeIn(L["en"][1]), FadeIn(L["me"][1]), run_time=0.8)
        self.at("are", lead=0.0)
        self.play(FadeIn(L["sox"]), run_time=0.6)
        self.at("endothelin receptor")
        self.play(FadeIn(L["rec"]), run_time=0.6)
        self.at("and endothelin")
        self.play(FadeIn(L["edn"]), *[GrowArrow(a) for a in L["arrows"]], run_time=0.9)
        self.finish()


class S16Ear(Sc):
    def construct(self):
        L = lineages(cy=1.15, h=3.0, w=5.4)
        self.add(L["en"], L["me"], L["edn"], L["arrows"])
        en_o, me_o = L["ovals"]
        # the ear is waiting at the lower right
        self.at("need them")
        self.play(en_o.animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), run_time=0.8)
        self.at("so do")
        self.play(me_o.animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), run_time=0.6)
        self.at("including")
        ex, ey = 0.7, -2.0
        wire = CubicBezier([1.5, 0.05, 0], [1.3, -0.5, 0], [ex, -0.5, 0], [ex, ey + 1.6, 0]).set_color(GOLD).set_stroke(width=6)
        self.play(Create(wire), run_time=0.9)
        self.at("inner ear")
        ear = ear_icon(ex, ey, 1.6)
        self.play(FadeIn(ear), FadeIn(lab("inner ear", ex - 2.4, ey, 30, TEXT)), run_time=0.7)
        self.at("for hearing")
        self.play(FadeIn(lab("hearing", ex - 2.4, ey - 0.6, 28, GOLD)), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s17-s20: the gut toy model
# ---------------------------------------------------------------------------------------------
GX0, GX1, GN = -5.6, 5.6, 7
GL = GX1 - GX0
SEG_K = 6 / 7
GY, GH = 0.1, 3.4
LBL_Y = GY + GH / 2 + 0.5
END_Y = GY - GH / 2 - 0.4
CLK = np.array([6.0, 3.15, 0])


def gut_outline(y, h, x0, x1):
    return RoundedRectangle(corner_radius=min(0.3, h * 0.4), width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_opacity=0).move_to([(x0 + x1) / 2, y, 0])


def gut_dividers(y, h, x0, x1):
    return VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=GREY, stroke_width=2) for x in np.linspace(x0, x1, GN + 1)[1:-1]])


def gut_trail(y, h, x0, fx):
    w = max(fx - x0, 0.01)
    return Rectangle(width=w, height=h - 0.1, stroke_width=0, fill_color=TEAL, fill_opacity=0.5).move_to([x0 + w / 2, y, 0])


def gut_front(y, h, fx):
    return VGroup(Line([fx, y - h / 2 + 0.06, 0], [fx, y + h / 2 - 0.06, 0], color=YELLOW, stroke_width=8),
                  *[cell(0.14 if h < 1 else 0.2, fx, y + dy, 1.0) for dy in (-h * 0.28, 0, h * 0.28)])


def gut_static(y, h, x0, x1, fx):
    return VGroup(gut_outline(y, h, x0, x1), gut_trail(y, h, x0, fx), gut_dividers(y, h, x0, x1), gut_front(y, h, fx))


class GutRig:
    def __init__(self):
        self.p = ValueTracker(0)
        self.k = 1.0
        self.outline = gut_outline(GY, GH, GX0, GX1)
        self.div = gut_dividers(GY, GH, GX0, GX1)
        self.trail = always_redraw(lambda: gut_trail(GY, GH, GX0, self.fx()))
        self.front = always_redraw(lambda: gut_front(GY, GH, self.fx()))
        self.ring = Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to(CLK)
        self.pie = always_redraw(lambda: Sector(radius=0.5, angle=max(2 * PI * (1 - self.p.get_value()), 1e-3), start_angle=PI / 2,
                                                fill_color=GOLD, fill_opacity=0.8, stroke_width=0, arc_center=CLK))
        self.clock_lbl = lab("fixed time", 4.55, CLK[1], 26, LGREY)
        self.clock = VGroup(self.ring, self.clock_lbl)

    def fx(self):
        return GX0 + self.k * self.p.get_value() * GL


def toy_label():
    return lab("toy model: one-front approximation;\nreal routes are more complex", -3.1, 3.3, 26, LGREY, line_spacing=0.9)


def mouth_label():
    return lab("mouth end", -4.8, END_Y, 28, LGREY)


def anal_label():
    return lab("anal end", 4.9, END_Y, 28, LGREY)


def slow_label():
    return lab("slower front", -4.0, LBL_Y, 28, YELLOW)


def predict_card():
    box = RoundedRectangle(corner_radius=0.2, width=9.0, height=1.45, stroke_color=GOLD, stroke_width=3,
                           fill_color=GOLD, fill_opacity=0.07).move_to([0, -3.05, 0])
    head = T("PREDICT", 24, GOLD, weight=BOLD).move_to([0, -2.65, 0])
    q = T("Which part stays empty?", 36, GOLD).move_to([0, -3.3, 0])
    return VGroup(box, head, q)


class S17Pred(Sc):
    def construct(self):
        r = GutRig()
        self.play(FadeIn(toy_label()), FadeIn(r.outline), FadeIn(r.div), FadeIn(mouth_label()), FadeIn(anal_label()), run_time=0.8)
        self.at("one front")
        self.add(r.trail, r.front, r.pie)
        self.play(FadeIn(r.clock), run_time=0.5)
        self.at("moves down the gut")
        # the normal front reaches the anal end exactly as the clock runs out
        self.play(r.p.animate(run_time=1.9, rate_func=linear).set_value(1))
        self.play(Indicate(r.ring, color=GOLD, scale_factor=1.25), run_time=0.8)
        self.at("slow it", lead=0.45)
        sl = slow_label()
        r.k = 1.0
        self.play(r.p.animate.set_value(0), run_time=0.45)
        r.k = SEG_K
        self.play(FadeIn(sl), r.p.animate(run_time=1.1, rate_func=linear).set_value(0.5))
        self.at("which part stays empty")
        self.play(FadeIn(predict_card()), run_time=0.8)
        self.finish()


def s17_final(scene):
    r = GutRig()
    r.k = SEG_K
    r.p.set_value(0.5)
    scene.add(toy_label(), r.outline, r.div, mouth_label(), anal_label(), r.trail, r.front, r.clock, r.pie, slow_label(), predict_card())
    return r


class S18Pause(Still):
    def construct(self):
        s17_final(self)
        v = Timer.make(self, [6.2, -3.15, 0], 5.0, r=0.35)
        self.play(v.animate(run_time=4.6, rate_func=linear).set_value(1))
        self.finish()


class S19Rev(Sc):
    def construct(self):
        r = GutRig()
        r.k = SEG_K
        r.p.set_value(0.5)
        anl = anal_label()
        self.add(toy_label(), r.outline, r.div, mouth_label(), anl, r.trail, r.front, r.clock, r.pie, slow_label())
        self.play(r.p.animate(run_time=1.9, rate_func=linear).set_value(1))
        self.play(Indicate(anl, color=GOLD, scale_factor=1.2), run_time=0.6)
        self.at("in the model")
        self.play(FadeIn(lab("neurons", 0.0, LBL_Y, 28, TEAL)), run_time=0.6)
        self.at("that segment")
        x0 = GX0 + SEG_K * GL
        seg = Rectangle(width=GX1 - x0 - 0.12, height=GH - 0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([(x0 + GX1) / 2 + 0.06, GY, 0])
        dash = DashedVMobject(Rectangle(width=GX1 - x0 - 0.2, height=GH - 0.2, stroke_color=RED, stroke_width=4).move_to([(x0 + GX1) / 2 + 0.06, GY, 0]), num_dashes=20)
        self.play(FadeIn(seg), Create(dash), FadeIn(lab("no neurons", (x0 + GX1) / 2, LBL_Y, 28, RED)), run_time=0.8)
        self.finish()


def clinic_sketch(y0, parts, width=56):
    """Wavy tube; parts is a list of (t0, t1) pieces. Returns VGroup of pieces (all teal)."""
    out = VGroup()
    for t0, t1 in parts:
        f = ParametricFunction(lambda t: [t, y0 + 0.3 * np.sin(1.3 * t), 0], t_range=[t0, t1], use_smoothing=False)
        f.set_stroke(color=TEAL, width=width, opacity=0.6)
        out.add(f)
    return out


class S20Toy(Sc):
    def construct(self):
        # rebuild the end of s19
        x0 = GX0 + SEG_K * GL
        old = gut_static(GY, GH, GX0, GX1, x0)
        seg = Rectangle(width=GX1 - x0 - 0.12, height=GH - 0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([(x0 + GX1) / 2 + 0.06, GY, 0])
        dash = DashedVMobject(Rectangle(width=GX1 - x0 - 0.2, height=GH - 0.2, stroke_color=RED, stroke_width=4).move_to([(x0 + GX1) / 2 + 0.06, GY, 0]), num_dashes=20)
        others = VGroup(toy_label(), mouth_label(), slow_label(), anal_label(), seg, dash,
                        lab("neurons", 0.0, LBL_Y, 28, TEAL),
                        lab("no neurons", (x0 + GX1) / 2, LBL_Y, 28, RED),
                        VGroup(Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to(CLK), lab("fixed time", 4.55, CLK[1], 26, LGREY)))
        self.add(old, others)
        self.at("toy model")
        new = gut_static(2.85, 0.8, -5.0, 5.0, -5.0 + SEG_K * 10.0)
        # Inset the fill inside the rounded left cap, with no protruding cyan edge.
        new[1].become(gut_trail(2.85, 0.8, -4.92, -5.0 + SEG_K * 10.0))
        toy = lab("toy model", -4.9, 3.5, 28, GOLD, left=True)
        toy.shift(RIGHT * 0)
        self.play(FadeOut(others), ReplacementTransform(old, new), FadeIn(toy), run_time=0.8)
        self.at("clinic")
        # clinical band: mouth end labelled from the start, short empty segment at the anal end
        ty = -0.65
        typ = clinic_sketch(ty, [(-5.2, 3.7), (3.7, 5.2)], width=72)
        tl = lab("typical pattern", -2.8, ty + 1.15, 30, TEAL)
        mo = lab("mouth end", -5.0, ty - 1.0, 26, LGREY)
        self.play(FadeIn(typ), FadeIn(tl), FadeIn(mo), run_time=0.8)
        self.at("the empty segment")
        es = lab("empty segment", 4.0, ty - 1.0, 26, LGREY)
        self.play(typ[1].animate.set_stroke(color=GREY, opacity=0.55), FadeIn(es), run_time=0.7)
        self.at("anal end")
        an = lab("anal end", 4.9, ty + 1.15, 26, LGREY)
        self.play(FadeIn(an), run_time=0.5)
        self.at("rare cases")
        # reflow: the typical band moves up, the rare pattern appears below it
        grp = VGroup(typ, tl, mo, es, an)
        ry = -2.3
        rare = clinic_sketch(ry, [(-5.2, -0.2), (-0.2, 1.4), (1.4, 5.2)])
        rl = lab("rare: skips a segment", -2.8, ry + 1.15, 30, TEAL)
        self.play(grp.animate.shift(UP * 1.15), FadeIn(rare), FadeIn(rl), run_time=0.5)
        self.at("skip a segment")
        self.play(rare[1].animate.set_stroke(color=GREY, opacity=0.55), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s21: Treacher Collins
# ---------------------------------------------------------------------------------------------
class S21Warn(Sc):
    def construct(self):
        a = chip("an early step fails", RED, size=42).move_to([-3.5, 0.2, 0])
        b = chip("wider damage", GREY, size=42).move_to([4.0, 0.2, 0])
        dl = DashedLine(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, color=GREY, stroke_width=5, dash_length=0.16)
        nm = lab("not always", (a.get_right()[0] + b.get_left()[0]) / 2, 0.95, 32, GOLD)
        self.play(FadeIn(a), run_time=0.6)
        self.at("need not mean")
        self.play(Create(dl), FadeIn(nm), run_time=0.7)
        self.at("wider damage")
        self.play(FadeIn(b), run_time=0.5)
        self.at("syndrome", lead=0.9)
        hx, hy = -1.6, -0.25
        head = Ellipse(width=3.8, height=5.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([hx, hy, 0])
        eyes = VGroup(*[Ellipse(width=0.7, height=0.28, stroke_color=TEXT, stroke_width=2.5).move_to([hx + dx, 0.55, 0]) for dx in (-0.8, 0.8)])
        lids = [Arc(radius=0.4, start_angle=PI * 0.15, angle=PI * 0.7, stroke_color=GREY, stroke_width=5).move_to([hx + dx, 0.92, 0]) for dx in (-0.8, 0.8)]
        ears = [Arc(radius=0.5, start_angle=PI / 2, angle=PI, stroke_color=GREY, stroke_width=5).move_to([hx - 1.9 - 0.2, 0.1, 0]),
                Arc(radius=0.5, start_angle=-PI / 2, angle=PI, stroke_color=GREY, stroke_width=5).move_to([hx + 1.9 + 0.2, 0.1, 0])]
        cheeks = [Ellipse(width=1.05, height=0.55, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to([hx + dx * 1.45, -0.55, 0]) for dx in (-0.75, 0.75)]
        jaw = ParametricFunction(lambda t: [hx + 1.9 * np.cos(t), hy + 2.5 * np.sin(t), 0], t_range=[-2.5, -0.64]).set_stroke(color=GREY, width=6)
        face = VGroup(head, eyes, *lids, *ears, *cheeks, jaw)
        crest = VGroup(*[cell(0.14, hx + (i - 5) * 0.42, 2.45 - 0.02 * (i - 5) ** 2, 0.9) for i in range(11)])
        face.scale(1.12, about_point=np.array([hx, hy, 0]))
        cl = lab("cranial crest cells", hx, 3.4, 26, YELLOW)
        title = lab("Treacher Collins\nsyndrome", 4.3, 2.75, 34, TEXT, line_spacing=0.9)
        self.play(FadeOut(a), FadeOut(b), FadeOut(dl), FadeOut(nm), FadeIn(face), FadeIn(crest), FadeIn(cl), FadeIn(title), run_time=0.9)
        self.at("cuts crest numbers")
        keep = [0, 3, 5, 8]
        gone = VGroup(*[crest[i] for i in range(11) if i not in keep])
        fewer = lab("fewer crest cells, early", hx, 3.4, 26, YELLOW)
        self.play(FadeOut(gone), Transform(cl, fewer), run_time=1.0)
        self.at("mainly")
        rv = lab("regional vulnerability", 4.3, -3.3, 30, GOLD)
        self.play(FadeIn(rv), run_time=0.5)

        def mark(items, label, y, target):
            ld = Line([2.15, y, 0], target, color=RED, stroke_width=2.5)
            return [m.animate.set_color(RED).set_stroke(width=8) for m in items], callouts[{"eyelids": 0, "ears": 1, "cheekbones, jaw": 2}[label]].animate.set_color(RED), Create(ld)
        # Establish the three callouts together, then highlight each named region.
        callouts = VGroup(lab("eyelids", 2.0, 1.1, 36, LGREY, left=True),
                          lab("ears", 2.0, 0.1, 36, LGREY, left=True),
                          lab("cheekbones, jaw", 2.0, -0.9, 36, LGREY, left=True))
        self.add(callouts)
        self.at("the face")
        ms, t1, l1 = mark([cheeks[0], cheeks[1], jaw], "cheekbones, jaw", -0.9, [hx + 1.09 + 0.52, -0.6, 0])
        self.play(*ms, t1, l1, run_time=0.5)
        self.at("ears")
        ms, t2, l2 = mark(ears, "ears", 0.1, [hx + 2.1 + 0.5, 0.1, 0])
        self.play(*ms, t2, l2, run_time=0.4)
        self.at("eyelids")
        ms, t3, l3 = mark(lids, "eyelids", 1.1, [hx + 0.8 + 0.2, 1.1, 0])
        self.play(*ms, t3, l3, run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s22: the take-home
# ---------------------------------------------------------------------------------------------
def req_box(text, color=LGREY, w=3.95, h=1.55):
    box = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.35)
    t = T(text, 28, TEXT, line_spacing=0.9).move_to(box)
    return VGroup(box, t)


class S22Take(Sc):
    def construct(self):
        en = req_box("enteric precursors", TEAL, w=4.7, h=1.0).move_to([-3.3, 0.9, 0])
        me = req_box("melanocytes", TEXT, w=4.7, h=1.0).move_to([3.3, 0.9, 0])
        sentence = lab("Tissues that fail together often share a requirement", 0, 2.8, 32, GOLD)
        if sentence.width > 12.8:
            sentence.scale_to_fit_width(12.8)
        self.play(FadeIn(sentence), FadeIn(en), FadeIn(me), run_time=0.6)
        self.at("fail together")
        s1 = SurroundingRectangle(en, color=RED, buff=0.14, stroke_width=4)
        s2 = SurroundingRectangle(me, color=RED, buff=0.14, stroke_width=4)
        self.play(Create(s1), Create(s2), run_time=0.6)
        self.at("share a requirement")
        self.play(Indicate(sentence, color=GOLD, scale_factor=1.02), run_time=0.7)
        self.at("depends on")
        self.play(FadeIn(lab("which tissues fail depends on", 0, -0.55, 30, LGREY)), run_time=0.6)
        yy = -2.35
        c1 = req_box("where the gene\nis needed").move_to([-4.2, yy, 0])
        c2 = req_box("the variant").move_to([0, yy, 0])
        c3 = req_box("each tissue's\nsensitivity").move_to([4.2, yy, 0])
        self.at("where the gene")
        self.play(FadeIn(c1), run_time=0.6)
        self.at("the variant")
        self.play(FadeIn(c2), run_time=0.6)
        self.at("and each")
        self.play(FadeIn(c3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s23: the guiding idea returns
# ---------------------------------------------------------------------------------------------
class S23Idea(Sc):
    def construct(self):
        title = lab("One border, many destinations", 0, 3.3, 36, GOLD)
        border = VGroup(Line([-5.4, -2.4, 0], [-5.4, 2.4, 0], color=YELLOW, stroke_width=8),
                        *[cell(0.3, -5.4, y, 0.9) for y in (-1.6, -0.55, 0.55, 1.6)])
        bl = lab("border", -5.4, -3.0, 28, YELLOW)
        self.play(FadeIn(title), FadeIn(border), FadeIn(bl), run_time=0.6)
        self.at("many destinations")
        names = [("gut neurons", TEAL), ("melanocytes", TEXT), ("sensory neurons", LGREY), ("facial bone and cartilage", LGREY)]
        ys = [1.95, 0.65, -0.65, -1.95]

        def dest(n, c, y):
            box = RoundedRectangle(corner_radius=0.14, width=5.8, height=0.95, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.16)
            return VGroup(box, T(n, 28, c).move_to(box)).move_to([3.6, y, 0])
        chips = [dest(n, c, y) for (n, c), y in zip(names, ys)]
        arrows = [arr([-4.9, 0, 0], [0.65, c.get_center()[1], 0], GREY, 3) for c in chips]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c), GrowArrow(a)) for c, a in zip(chips, arrows)], lag_ratio=0.2), run_time=1.2)
        self.at("start")
        # the start biases the options: the border brightens, two routes are favoured
        self.play(arrows[0].animate.set_stroke(color=YELLOW, width=9), arrows[1].animate.set_stroke(color=YELLOW, width=6),
                  Indicate(border, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.at("the journey")
        # the journey helps choose: one cell travels a route and settles on its destination
        walker = cell(0.28, -4.9, 0, 1.0)
        self.add(walker)
        self.play(arrows[0].animate.set_stroke(color=GREY, width=3), arrows[1].animate.set_stroke(color=GREY, width=3),
                  MoveAlongPath(walker, Line([-4.9, 0, 0], [0.55, ys[2], 0])), arrows[2].animate.set_stroke(color=YELLOW, width=9), run_time=0.6)
        self.at("helps choose")
        self.play(Indicate(chips[2], color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


class S24End(EndCard):
    LINE = "The start biases the options, and the journey helps choose."
