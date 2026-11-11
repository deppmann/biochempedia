"""Purity Through Selective Loss -- one carried sample world.

COLOR MAP
  GOLD = active target; GREY = other protein; TEAL = retained sample/formulas
  RED = discarded material; BLUE = separation-property controls
"""
import math
from bp_style import *


WORLD_X = -3.35
VESSEL_W, VESSEL_H = 4.55, 5.15


def vessel(x=WORLD_X, y=0.25, w=VESSEL_W, h=VESSEL_H, opacity=1.0):
    body = RoundedRectangle(width=w, height=h, corner_radius=0.28, color=TEAL,
                            stroke_width=4, fill_color=TEAL, fill_opacity=0.055)
    body.move_to([x, y, 0]).set_opacity(opacity)
    body.phase = 0.0
    def breathe(m, dt):
        m.phase += dt
        m.set_fill(TEAL, opacity=opacity * (0.14 + 0.04 * math.sin(m.phase * 1.7)))
    body.add_updater(breathe)
    gate = RoundedRectangle(width=1.55, height=0.34, corner_radius=0.1, color=BLUE,
                            fill_color=BLUE, fill_opacity=0.3, stroke_width=3)
    gate.move_to(body.get_bottom() + DOWN * 0.12).set_opacity(opacity)
    return VGroup(body, gate)


def token_cloud(x=WORLD_X, y=0.35, gold=4, grey=36, scale=1.0, opacity=1.0):
    """Illustrative, deterministic token pile with gentle convection."""
    colors = [GOLD] * gold + [GREY] * grey
    g = VGroup()
    cols = 8 if len(colors) > 16 else 4
    for i, color in enumerate(colors):
        row, col = divmod(i, cols)
        px = x + (col - (cols - 1) / 2) * 0.47 * scale
        py = y - 1.62 * scale + row * 0.68 * scale
        d = Circle(radius=0.145 * scale, color=color, fill_color=color,
                   fill_opacity=0.92 if color == GOLD else 0.7, stroke_width=1.5)
        d.move_to([px, py, 0])
        d.phase = i * 0.71
        d.base = d.get_center().copy()
        def drift(m, dt):
            m.phase += dt * (0.72 + (m.phase % 0.21))
            m.move_to(m.base + [0.17 * math.sin(m.phase), 0.11 * math.cos(m.phase * 0.83), 0])
        d.add_updater(drift)
        g.add(d)
    g.set_opacity(opacity)
    return g


def tray(x=5.05, y=-2.55, opacity=1.0):
    box = RoundedRectangle(width=3.0, height=1.35, corner_radius=0.22, color=RED,
                           fill_color=RED, fill_opacity=0.08, stroke_width=3)
    lab = T("discard", 28, RED).next_to(box, DOWN, buff=0.14)
    return VGroup(box, lab).move_to([x, y, 0]).set_opacity(opacity)


def world(opacity=1.0, gold=4, grey=36, small=False):
    if small:
        v = vessel(-4.75, -0.1, 2.45, 3.7, opacity)
        tok = token_cloud(-4.75, -0.05, gold, grey, 0.58, opacity)
        tr = tray(-1.7, -2.85, opacity)
    else:
        v = vessel(opacity=opacity)
        tok = token_cloud(gold=gold, grey=grey, opacity=opacity)
        tr = tray(opacity=opacity)
    lab = T("schematic sample", 28, TEXT).move_to([2.35, -3.45, 0]).set_opacity(opacity)
    return VGroup(v, tok, tr, lab)


def counter(text, color, pos, size=30):
    val = M(text, size, color)
    box = RoundedRectangle(width=max(3.45, val.width + .42), height=0.82, corner_radius=0.14, color=color,
                           fill_color=color, fill_opacity=0.1, stroke_width=2.5)
    val.move_to(box)
    return VGroup(box, val).move_to(pos)


def percent_bar(label, value, color, y, x=1.0, width=5.1):
    lab = T(label, 28, color).move_to([x - width / 2, y + 0.52, 0], aligned_edge=LEFT)
    rail = RoundedRectangle(width=width, height=0.48, corner_radius=0.12, color=GREY,
                            fill_color=GREY, fill_opacity=0.08, stroke_width=2)
    rail.move_to([x, y, 0])
    fill = Rectangle(width=max(0.08, width * value), height=0.42, stroke_width=0,
                     fill_color=color, fill_opacity=0.92)
    fill.align_to(rail, LEFT).move_to([rail.get_left()[0] + fill.width / 2, y, 0])
    pct = M(f"{round(value * 100)}%", 30, color).next_to(rail, RIGHT, buff=0.18)
    return VGroup(lab, rail, fill, pct)


def scanner(x=WORLD_X, y=-1.8, w=4.1):
    return Rectangle(width=w, height=0.12, color=BLUE, fill_color=BLUE,
                     fill_opacity=0.9, stroke_width=0).move_to([x, y, 0])


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Protein purification techniques"
    TITLE = "Purity Through Selective Loss"

    def construct(self):
        w = world()
        self.play(FadeIn(w[0]), FadeIn(w[1]), FadeIn(w[2]), FadeIn(w[3]), run_time=1.0)
        self.at("losing nearly half")
        q = T("How can loss improve purity?", 38, TEXT, weight=BOLD).move_to([2.85, 2.85, 0])
        arrow = Arrow(w[0][1].get_right(), w[2][0].get_left(), color=RED, stroke_width=7, buff=0.1)
        moving = VGroup(*[m.copy().clear_updaters() for m in list(w[1])[2:18]])
        self.add(moving)
        self.play(FadeIn(q), GrowArrow(arrow),
                  *[m.animate.move_to(w[2][0].get_center() + [((i % 5)-2)*0.35, ((i//5)-1)*0.25, 0])
                    for i, m in enumerate(moving)], run_time=2.1)
        qm = T("?", 64, GOLD, weight=BOLD).move_to([3.9, 0.4, 0])
        self.play(FadeIn(qm, scale=1.4), run_time=0.45)
        self.at("answer becomes visible")
        gauges = VGroup(percent_bar("target kept", .5, GOLD, 0.85, x=3.15, width=3.1),
                        percent_bar("protein kept", .12, TEAL, -0.3, x=3.15, width=3.1))
        self.play(FadeOut(qm), FadeOut(q), FadeOut(arrow), FadeOut(moving), FadeIn(gauges), run_time=1.2)
        self.at("Gold tokens")
        golds = VGroup(*list(w[1])[:4])
        self.play(Indicate(golds, color=GOLD, scale_factor=1.18), run_time=0.8)
        self.at("whole gold and gray pile")
        bracket = SurroundingRectangle(w[1], color=TEAL, buff=0.18, stroke_width=4)
        self.play(Create(bracket), run_time=0.8)
        self.play(ShowPassingFlash(bracket.copy().set_stroke(width=9), run_time=1.7), run_time=1.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Protein purification techniques"
    TITLE = "Purity Through Selective Loss"

    def construct(self):
        w = world(opacity=0.25)
        self.add(w)
        brand = T("BIOCHEMISTRYPEDIA", 24, TEAL, weight=BOLD).move_to(UP * 1.0)
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT).move_to(DOWN * 0.05)
        fit(title, 11.5)
        self.play(FadeIn(brand, shift=UP * .1), GrowFromCenter(title), run_time=0.7)
        self.wait(0.9)
        self.play(FadeOut(brand), title.animate.scale(0.05).move_to(w[0][1]), w.animate.set_opacity(1), run_time=0.4)
        self.finish()


class S02Assay(SpokenScene):
    def construct(self):
        w = world(); self.add(w)
        scan = scanner(); self.add(scan)
        self.play(scan.animate.shift(UP * 3.9), run_time=1.8, rate_func=linear)
        self.at("assay that finds")
        c1 = counter("target activity", GOLD, [4.35, 1.25, 0])
        self.play(FadeIn(c1), Indicate(VGroup(*list(w[1])[:4]), color=GOLD), run_time=1.1)
        self.at("reaction reports activity")
        new1 = counter("4 activity units", GOLD, [4.35, 1.25, 0])
        self.play(Transform(c1, new1), run_time=1.0)
        self.play(Indicate(VGroup(*list(w[1])[:4]), color=GOLD), run_time=1.0)
        self.at("Total protein measures")
        wide = scanner(y=-1.6)
        c2 = counter("total protein, mg", TEAL, [4.35, -0.15, 0])
        self.play(Transform(scan, wide), scan.animate.shift(UP * 3.5), FadeIn(c2), run_time=1.6)
        new2 = counter("40 protein units", TEAL, [4.35, -0.15, 0])
        self.play(Transform(c2, new2), run_time=1.0)
        self.finish()


class S03Specific(SpokenScene):
    def construct(self):
        w = world(small=True); self.add(w)
        c1 = counter("target activity", GOLD, [1.8, 1.65, 0]); c2 = counter("total protein", TEAL, [1.8, 0.45, 0])
        self.add(c1, c2)
        self.at("100 000 activity")
        self.play(Transform(c1, counter("100,000 activity units", GOLD, [1.8, 1.65, 0], 27)), run_time=1.0)
        self.at("10 000 milligrams")
        self.play(Transform(c2, counter("10,000 mg total protein", TEAL, [1.8, .45, 0], 25)), run_time=1.0)
        self.at("Divide activity")
        frac = VGroup(M("100,000 activity units", 28, GOLD), Line(LEFT*2.4, RIGHT*2.4, color=TEXT, stroke_width=3),
                      M("10,000 mg protein", 28, TEAL)).arrange(DOWN, buff=.16).move_to([1.8, .2, 0])
        self.play(ReplacementTransform(c1, frac[0]), Create(frac[1]),
                  ReplacementTransform(c2, frac[2]), run_time=1.1)
        self.at("Specific activity is")
        result = counter("specific activity = 10 units/mg", TEAL, [1.8, -1.65, 0], 25)
        self.play(FadeIn(result, shift=UP*.2), Indicate(VGroup(*list(w[1])[:4]), color=GOLD), run_time=1.1)
        self.play(ShowPassingFlash(SurroundingRectangle(result, color=TEAL, buff=.08), run_time=1.8), run_time=1.8)
        self.finish()


class S04SaltStep(SpokenScene):
    def construct(self):
        w = world(small=True); self.add(w)
        a = percent_bar("target activity", 1, GOLD, 1.6, x=1.7, width=4.6)
        p = percent_bar("total protein", 1, TEAL, .35, x=1.7, width=4.6)
        self.add(a, p)
        self.at("keeps 90")
        a90 = percent_bar("target activity", .9, GOLD, 1.6, x=1.7, width=4.6)
        lost = Circle(.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(w[2][0].get_center())
        self.play(Transform(a, a90), FadeIn(lost, shift=RIGHT), run_time=1.3)
        self.at("only 30")
        p30 = percent_bar("total protein", .3, TEAL, .35, x=1.7, width=4.6)
        red_blocks = VGroup(*[Rectangle(width=.35, height=.26, color=RED, fill_color=RED, fill_opacity=.7)
                              for _ in range(7)]).arrange(RIGHT, buff=.12).move_to([2.7, -1.05, 0])
        self.play(Transform(p, p30), LaggedStart(*[FadeIn(b, shift=DOWN*.4) for b in red_blocks], lag_ratio=.08), run_time=1.4)
        self.at("Specific activity triples")
        sa10 = counter("specific activity  10", TEAL, [3.35, -1.75, 0])
        sa30 = counter("specific activity  30", TEAL, [3.35, -1.75, 0])
        self.play(FadeIn(sa10), run_time=.5)
        self.play(Transform(sa10, sa30), run_time=.8)
        self.play(Indicate(sa10, color=TEAL, scale_factor=1.13), run_time=.7)
        self.at("some target was lost")
        self.play(Indicate(lost, color=GOLD, scale_factor=1.5), Indicate(w[0], color=TEAL), run_time=1.0)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        w = world(small=True, gold=4, grey=10); self.add(w)
        a = percent_bar("target activity", .9, GOLD, 1.35, x=1.65, width=4.8)
        p = percent_bar("total protein", .3, TEAL, -.05, x=1.65, width=4.8)
        self.add(a, p)
        self.at("guiding idea")
        ba = SurroundingRectangle(a[2], color=GOLD, buff=.03)
        bp = SurroundingRectangle(p[2], color=TEAL, buff=.03)
        self.play(Create(ba), Create(bp), run_time=.8)
        self.play(ShowPassingFlash(ba.copy().set_stroke(width=8)), ShowPassingFlash(bp.copy().set_stroke(width=8)), run_time=1.7)
        self.at("larger fraction")
        self.play(a[2].animate.set_opacity(1), p[2].animate.set_opacity(.55), run_time=1.0)
        self.at("rises by the ratio")
        frac = VGroup(M("0.90", 34, GOLD), Line(LEFT*.8, RIGHT*.8, color=TEXT, stroke_width=3), M("0.30", 34, TEAL)).arrange(DOWN, buff=.1).move_to([1.1, -2.1, 0])
        ans = M("→  3-fold", 38, TEAL).next_to(frac, RIGHT, buff=.35)
        self.play(FadeIn(frac), run_time=.7); self.play(Write(ans), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = world(small=True, gold=4, grey=10); self.add(w)
        a = percent_bar("affinity: activity", 1, GOLD, 1.25, x=1.55, width=4.7)
        p = percent_bar("affinity: protein", 1, TEAL, -.2, x=1.55, width=4.7)
        self.add(a, p)
        self.at("keeps about 55")
        self.play(Transform(a, percent_bar("affinity: activity", .55, GOLD, 1.25, x=1.55, width=4.7)), run_time=2.0)
        self.at("keeps only 2")
        self.play(Transform(p, percent_bar("affinity: protein", .02, TEAL, -.2, x=1.55, width=4.7)), run_time=2.0)
        self.at("losing nearly half")
        q = T("?", 74, TEXT, weight=BOLD).move_to([3.0, -1.15, 0])
        card = chip("Failure or best step?", BLUE, size=38).move_to([3.0, -2.30, 0])
        self.play(FadeIn(q, scale=1.5), FadeIn(card, shift=UP*.2), run_time=1.0)
        self.play(q.animate.scale(1.06), rate_func=there_and_back, run_time=1.5)
        self.finish()


class S07Think(Scene):
    def construct(self):
        w = world(small=True, gold=2, grey=1); self.add(w)
        a = percent_bar("affinity: activity", .55, GOLD, 1.25, x=1.55, width=4.7)
        p = percent_bar("affinity: protein", .02, TEAL, -.2, x=1.55, width=4.7)
        q = T("?", 74, TEXT, weight=BOLD).move_to([3.0, -1.15, 0])
        card = chip("Failure or best step?", BLUE, size=38).move_to([3.0, -2.30, 0])
        self.add(a, p, q, card)
        self.play(q.animate.scale(1.06), rate_func=there_and_back, run_time=2.0)
        self.play(q.animate.scale(1.06), rate_func=there_and_back, run_time=2.0)
        self.wait(.5)


class S08Answer(SpokenScene):
    def construct(self):
        w = world(small=True, gold=2, grey=1); self.add(w)
        a = percent_bar("activity", .55, GOLD, 1.55, x=1.55, width=4.5)
        p = percent_bar("protein", .02, TEAL, .25, x=1.55, width=4.5)
        card = chip("best step", TEAL, size=38).move_to([1.5, 2.75, 0])
        self.play(FadeIn(card, scale=.8), FadeIn(a), FadeIn(p), run_time=.8)
        self.at("55 divided by 2")
        frac = VGroup(M("55%", 34, GOLD), Line(LEFT*.8, RIGHT*.8, color=TEXT, stroke_width=3), M("2%", 34, TEAL)).arrange(DOWN, buff=.08).move_to([.4, -1.45, 0])
        count = M("≈ 27-fold", 42, TEAL).next_to(frac, RIGHT, buff=.4)
        self.play(FadeOut(a), FadeOut(p), FadeIn(frac), run_time=.8)
        for n in (3, 9, 18, 27):
            nxt = M(f"≈ {n}-fold", 42, TEAL).move_to(count)
            if n == 3: self.play(FadeIn(nxt), run_time=.35); count = nxt
            else: self.play(Transform(count, nxt), run_time=.35)
        self.at("Specific activity jumps")
        sa = counter("1,100 units/mg", TEAL, [1.55, -.1, 0])
        self.play(FadeIn(sa), run_time=.45)
        for v in (5000, 12000, 21000, 30000):
            self.play(Transform(sa, counter(f"{v:,} units/mg", TEAL, [1.55, -.1, 0])), run_time=.35)
        beam = Rectangle(width=2.35, height=.24, color=TEAL, fill_color=TEAL,
                         fill_opacity=.78, stroke_width=0).move_to([-4.75,-1.75,0]).set_z_index(-1)
        self.play(FadeIn(beam), Indicate(card, color=TEAL), run_time=1.0)
        travel = self.t_of("best step") - .2 - self.elapsed()
        if travel > .02:
            self.play(beam.animate.shift(UP * 3.5), rate_func=linear, run_time=travel)
        self.at("best step")
        self.play(ShowPassingFlash(SurroundingRectangle(card, color=TEAL, buff=.12).set_stroke(width=8), run_time=1.8), run_time=1.8)
        remaining = self.narration_s + .4 - self.elapsed()
        if remaining > .02:
            self.play(beam.animate.shift(DOWN * .12), rate_func=there_and_back, run_time=remaining)
        self.finish()


class S09YieldFold(SpokenScene):
    def construct(self):
        w = world(small=True, gold=2, grey=1); self.add(w)
        vessel0 = vessel(-1.2, .6, 1.5, 2.3); vessel1 = vessel(5.2, .6, 1.5, 2.3)
        ribbon = Arrow(vessel0.get_right(), vessel1.get_left(), color=GOLD, stroke_width=12, buff=.1)
        self.play(FadeIn(vessel0), FadeIn(vessel1), GrowArrow(ribbon), run_time=1.2)
        settle = self.t_of("Yield is activity") - .2 - self.elapsed()
        if settle > .02:
            self.play(ShowPassingFlash(ribbon.copy().set_stroke(width=28), time_width=.55), run_time=settle)
        self.at("Yield is activity")
        yf = VGroup(M("activity now", 30, GOLD), Line(LEFT*1.5, RIGHT*1.5, color=TEXT), M("activity at start", 30, GOLD)).arrange(DOWN, buff=.12).move_to([2.0, 1.35, 0])
        yg = percent_bar("quantity retained", .36, GOLD, -1.0, x=2.0, width=4.6)
        self.play(FadeIn(yf), FadeIn(yg), run_time=1.2)
        self.at("Fold purification")
        ff = VGroup(M("specific activity now", 28, TEAL), Line(LEFT*2.0, RIGHT*2.0, color=TEXT), M("starting value", 28, TEAL)).arrange(DOWN, buff=.12).move_to([2.0, 1.2, 0])
        fg = percent_bar("enrichment", .95, TEAL, -2.35, x=2.0, width=4.6)
        self.play(FadeOut(yf), FadeIn(ff), FadeIn(fg), run_time=1.3)
        self.at("One tracks quantity")
        trade = DoubleArrow([-.3,-.35,0],[4.3,-.35,0], color=BLUE, stroke_width=5, buff=0)
        self.play(GrowFromCenter(trade), yg.animate.set_opacity(.7), fg.animate.set_opacity(1), run_time=1.0)
        self.play(trade.animate.shift(UP*.1), rate_func=there_and_back, run_time=2.0)
        self.finish()


class S10Route(SpokenScene):
    def construct(self):
        names = ["crude", "salt", "ion", "size", "affinity"]
        xs = [-5.4,-2.7,0,2.7,5.4]
        vs = VGroup(*[vessel(x, -1.25, 1.45, 1.7) for x in xs])
        clouds = VGroup(*[token_cloud(x, -1.25, 1, 2, .34) for x in xs])
        labs = VGroup(*[T(n,28,TEXT).move_to([x,-2.45,0]) for n,x in zip(names,xs)])
        self.play(LaggedStart(*[FadeIn(v) for v in vs], lag_ratio=.15), FadeIn(clouds), FadeIn(labs), run_time=1.3)
        self.at("yield falls")
        yields=[100,90,81,66,36]; ypts=[[x,-.2+v/100*1.55,0] for x,v in zip(xs,yields)]
        yl=VMobject(color=GOLD,stroke_width=6).set_points_as_corners(ypts)
        yd_pos=[[-5.4,1.72,0],[-2.7,1.58,0],[0,.64,0],[2.7,.50,0],[5.4,-.05,0]]
        yd=VGroup(*[M(f"{v}%",28,GOLD).move_to(p) for v,p in zip(yields,yd_pos)])
        self.play(Create(yl), LaggedStart(*[FadeIn(d) for d in yd],lag_ratio=.15),run_time=2.0)
        self.at("specific activity rises")
        folds=[1,3,9,110,3000]; fpts=[[x,.7+math.log10(v+1)/math.log10(3001)*2.0,0] for x,v in zip(xs,folds)]
        fl=VMobject(color=TEAL,stroke_width=6).set_points_as_corners(fpts)
        fd_pos=[[-5.4,.50,0],[-2.7,.64,0],[0,1.68,0],[2.7,2.15,0],[5.4,3.00,0]]
        fd=VGroup(*[M(f"{v:,}×",28,TEAL).move_to(p) for v,p in zip(folds,fd_pos)])
        note=T("fold, log scale",28,TEAL).move_to([4.35,3.55,0])
        source=T("computed from lesson table",28,TEXT).move_to([0,-3.25,0])
        self.play(Create(fl),LaggedStart(*[FadeIn(d) for d in fd],lag_ratio=.15),FadeIn(note),FadeIn(source),run_time=2.0)
        self.at("Step by step")
        arrows=VGroup(*[Arrow([xs[i]+.75,-1.25,0],[xs[i+1]-.75,-1.25,0],color=BLUE,buff=0) for i in range(4)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],lag_ratio=.22),run_time=1.5)
        self.finish()


class S11Properties(SpokenScene):
    def construct(self):
        w=world(); self.add(w)
        ledger=VGroup(percent_bar("yield",.36,GOLD,1.4,x=3.7,width=3.1),percent_bar("fold",.95,TEAL,.15,x=3.7,width=3.1))
        self.add(ledger)
        self.at("does not choose")
        wheel=Circle(1.9,color=BLUE,stroke_width=5).move_to([3.85,.75,0])
        spokes=VGroup(*[Line(wheel.get_center(),wheel.point_at_angle(a),color=BLUE,stroke_width=3) for a in (0,PI/2,PI,3*PI/2)])
        self.remove(ledger)
        self.play(Create(wheel),Create(spokes),run_time=1.2)
        labels=[T("solubility",28,BLUE),T("charge",28,BLUE),T("size",28,BLUE),T("binding",28,BLUE)]
        pos=[[2.95,1.4,0],[4.75,1.4,0],[3.05,.1,0],[4.7,.1,0]]
        for l,p in zip(labels,pos): l.move_to(p)
        self.at("solubility")
        self.play(FadeIn(labels[0]),Rotate(spokes,PI/2,about_point=wheel.get_center()),run_time=.8)
        self.at("charge")
        self.play(FadeIn(labels[1]),Rotate(spokes,PI/2,about_point=wheel.get_center()),run_time=.8)
        self.at("size")
        self.play(FadeIn(labels[2]),Rotate(spokes,PI/2,about_point=wheel.get_center()),run_time=.8)
        self.at("selective binding")
        self.play(FadeIn(labels[3]),Rotate(spokes,PI/2,about_point=wheel.get_center()),run_time=.8)
        self.at("assay every fraction")
        scan=scanner(); self.add(scan)
        c1=counter("activity",GOLD,[4.45,1.15,0]); c2=counter("total protein",TEAL,[4.45,.1,0])
        self.play(FadeOut(wheel),FadeOut(spokes),FadeOut(VGroup(*labels)),
                  scan.animate.shift(UP*3.8),FadeIn(c1),FadeIn(c2),run_time=1.5)
        self.finish()


class S12Limits(SpokenScene):
    def construct(self):
        w=world(); self.add(w)
        scan=scanner(); c1=counter("activity  4",GOLD,[4.4,.9,0]); c2=counter("total protein  40",TEAL,[4.4,-.25,0],26)
        self.add(scan,c1,c2)
        self.at("simplest form")
        assumption=chip("assumption: target stays equally active",TEAL,size=30).move_to([2.7,2.65,0]); fit(assumption,6.8)
        self.play(FadeIn(assumption,shift=DOWN*.2),run_time=.9)
        self.at("Inactivation")
        gold=list(w[1])[:4]
        self.play(gold[0].animate.set_opacity(.18),Transform(c1,counter("activity  3",GOLD,[4.4,.9,0])),run_time=1.2)
        self.at("Removing an inhibitor")
        inhibitor=chip("inhibitor",RED,size=28).move_to(gold[1].get_center()+RIGHT*.75)
        self.add(inhibitor)
        self.play(inhibitor.animate.move_to([5.8,-2.25,0]).set_opacity(.15),gold[1].animate.scale(1.3),Transform(c1,counter("activity  4",GOLD,[4.4,.9,0])),run_time=1.3)
        self.at("text below")
        tabs=VGroup(chip("inactivation?",BLUE,size=28),chip("inhibitor?",BLUE,size=28)).arrange(DOWN,buff=.2).move_to([2.0,-1.75,0])
        self.remove(assumption,inhibitor)
        self.play(FadeIn(tabs),run_time=1.0)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        w=world(); self.add(w)
        self.at("not a contest")
        arrow=Arrow(w[0][1].get_right(),w[2][0].get_left(),color=RED,stroke_width=8,buff=.1)
        moving=VGroup(*[m.copy().clear_updaters() for m in list(w[1])[5:24]])
        self.add(moving)
        self.play(GrowArrow(arrow),*[m.animate.move_to(w[2][0].get_center()+[((i%5)-2)*.33,((i//5)-1)*.22,0]) for i,m in enumerate(moving)],run_time=2.0)
        self.at("larger fraction")
        a=percent_bar("target activity",.9,GOLD,1.45,x=3.45,width=3.3)
        p=percent_bar("total protein",.3,TEAL,.15,x=3.45,width=3.3)
        self.play(FadeOut(moving),FadeIn(a),FadeIn(p),run_time=1.2)
        self.play(ShowPassingFlash(SurroundingRectangle(a[2],color=GOLD,buff=.1).set_stroke(width=8)),run_time=1.4)
        self.at("selective loss creates purity")
        sa=counter("specific activity ↑",TEAL,[3.8,-1.1,0])
        self.play(Transform(arrow,Arrow([1.2,-.9,0],[1.2,-2.4,0],color=RED,stroke_width=8,buff=0)),FadeIn(sa),run_time=1.2)
        self.play(Indicate(w[0],color=TEAL),run_time=1.2)
        self.finish()


class S14End(EndCard):
    LINE = "Good steps keep a larger fraction of target activity than total protein."

    def construct(self):
        w=world(opacity=.25,gold=4,grey=5); self.add(w)
        line=VGroup(T("Good steps keep a larger fraction of",38,TEXT,font=TITLE_FONT),
                    T("target activity than total protein.",38,TEXT,font=TITLE_FONT)).arrange(DOWN,buff=.2)
        line.move_to([1.0,.55,0]); fit(line,10.8)
        sub=T("biochemistrypedia.com",28,TEAL).move_to([1.0,-.65,0])
        back=RoundedRectangle(width=10.9,height=2.25,corner_radius=.2,stroke_width=0,
                              fill_color=BG,fill_opacity=.82).move_to([1.0,.15,0])
        self.play(FadeIn(back),FadeIn(line,shift=UP*.15),FadeIn(sub,shift=UP*.1),run_time=.8)
        self.wait(2.8)
        self.play(ShowPassingFlash(SurroundingRectangle(line,color=GOLD,buff=.18),run_time=.4),run_time=.4)
        self.finish()
