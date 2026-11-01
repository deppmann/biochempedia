"""Bacterial and phage genetics: three routes to new genes  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  BLUE   = DNA: the chromosome ring and the map line
  PURPLE = a marker gene (a, b, c, d) wherever it appears
  ORANGE = the Hfr donor cell
  GREEN  = the recipient cell, and recombinant colonies
  GOLD   = F and the origin of transfer
  YELLOW = time and gaps, in minutes
  RED    = a missing ability, the blender break, absent
  GREY   = outlines, plates, labels
All numbers are the lesson's worked problem (a): Hfr 1 a 8, b 14, c 20, d 31 min; Hfr 2 d 4, c 15, b 21, a 27 min.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DEG = 3.6                                   # degrees of ring per minute (100 minutes = 360 degrees)
T1 = {"a": 8, "b": 14, "c": 20, "d": 31}    # Hfr strain 1 times of entry
T2 = {"d": 4, "c": 15, "b": 21, "a": 27}    # Hfr strain 2 times of entry
GEN_ANG = {k: 90 - DEG * v for k, v in T1.items()}   # origin 1 at 90 degrees, clockwise


def pt(c, r, ang):
    a = np.radians(ang)
    return np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])


def cell(color, w=4.4, h=4.0, cr=1.3, op=0.14):
    return RoundedRectangle(corner_radius=cr, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=op)


def gene_chip(name, size=26):
    return chip(name, PURPLE, size=size, pad=0.14)


def ring_with_genes(c, r, names="abcd", lab=0.42, size=26):
    ring = Circle(radius=r, stroke_color=BLUE, stroke_width=6).move_to(c)
    dots, labs = VGroup(), VGroup()
    for n in names:
        d = Dot(pt(c, r, GEN_ANG[n]), radius=0.11, color=PURPLE)
        l = T(n, size, PURPLE, weight=BOLD).move_to(pt(c, r + lab, GEN_ANG[n]))
        dots.add(d); labs.add(l)
    return ring, dots, labs


def small_pair(x, y, s=1.0):
    d = cell(ORANGE, 1.2 * s, 1.2 * s, 0.4 * s).move_to([x - 0.95 * s, y, 0])
    r = cell(GREEN, 1.2 * s, 1.2 * s, 0.4 * s).move_to([x + 0.95 * s, y, 0])
    b = Line(d.get_right(), r.get_left(), color=GREY, stroke_width=6)
    return VGroup(d, r, b)


def plate(x, y, w=3.4, h=1.9):
    e = Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    return e


def colonies(x, y, n=6, seed=1):
    rng = np.random.RandomState(seed)
    ds = VGroup()
    while len(ds) < n:
        dx, dy = rng.uniform(-1.1, 1.1), rng.uniform(-0.5, 0.5)
        if (dx / 1.2) ** 2 + (dy / 0.6) ** 2 < 1:
            ds.add(Dot([x + dx, y + dy, 0], radius=0.11, color=GREEN))
    return ds


# --- timeline rows ---------------------------------------------------------------------------
def X(t):
    return -4.8 + 0.28 * t


def row(y, times, order):
    """line from 0 to 35 min with marker chips and their times. Returns dict of parts."""
    line = Line([X(0), y, 0], [X(35), y, 0], color=BLUE, stroke_width=6)
    chips, tl, sticks = {}, {}, {}
    for n in order:
        x = X(times[n])
        chips[n] = gene_chip(n).move_to([x, y + 0.62, 0])
        sticks[n] = Line([x, y, 0], [x, y + 0.3, 0], color=PURPLE, stroke_width=4)
        tl[n] = M(f"{times[n]} min", 24, YELLOW).move_to([x, y + 1.2, 0])
    return line, chips, tl, sticks


def brackets(y, xs, labels, color=YELLOW):
    g = VGroup()
    for (x0, x1), lb in zip(zip(xs[:-1], xs[1:]), labels):
        ln = VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                    Line([x0, y - 0.12, 0], [x0, y + 0.12, 0], color=color, stroke_width=4),
                    Line([x1, y - 0.12, 0], [x1, y + 0.12, 0], color=color, stroke_width=4))
        g.add(VGroup(ln, M(lb, 26, color).move_to([(x0 + x1) / 2, y - 0.38, 0])))
    return g


def origin_mark(x, y, direction):
    """gold dot on the line with a short arrow along it, pointing `direction` (+1 right, -1 left)."""
    dot = Dot([x, y, 0], radius=0.17, color=GOLD)
    ar = Arrow([x + 0.2 * direction, y, 0], [x + 0.95 * direction, y, 0], buff=0, color=GOLD, stroke_width=7,
               tip_length=0.22, max_tip_length_to_length_ratio=0.6)
    lb = T("origin", 22, GOLD).move_to([x, y - 0.45, 0])
    return VGroup(dot, ar, lb)


# Schematic DNA paths below represent chromosomes, never chemical structures.
def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.05, 0])


def phage(x, y, cargo=True):
    coat = RoundedRectangle(width=1.25, height=1.0, corner_radius=0.25,
                            stroke_color=GREY, stroke_width=4).move_to([x, y, 0])
    tail = Line([x, y-.5, 0], [x, y-1, 0], color=GREY, stroke_width=5)
    feet = VGroup(Line([x, y-1, 0], [x-.35, y-1.2, 0], color=GREY),
                  Line([x, y-1, 0], [x+.35, y-1.2, 0], color=GREY))
    g = VGroup(coat, tail, feet)
    if cargo:
        g.add(Line([x-.35, y, 0], [x+.35, y, 0], color=PURPLE, stroke_width=8))
    return g


class S00Title(TitleCard):
    LESSON = "Bacterial and phage genetics"
    TITLE = "Three Routes to New Genes"

    def construct(self):
        title = T(self.TITLE, 46, font=TITLE_FONT).move_to([0, 2.7, 0])
        recipient = cell(GREEN, 2.5, 1.6, .6).move_to([0, -.4, 0])
        lab = T("recipient", 24, GREEN).move_to([0, -1.7, 0])
        free = VGroup(Line([-5, .3, 0], [-3.4, .3, 0], color=BLUE, stroke_width=7),
                      T("free DNA", 24, BLUE).move_to([-4.2, 1.2, 0]))
        pair = small_pair(0, -2.75, .7)
        virus = phage(4.3, .7)
        arrows = VGroup(Arrow([-3,.3,0],[-1.5,-.2,0],color=BLUE),
                        Arrow([3,.1,0],[1.5,-.2,0],color=BLUE))
        self.play(FadeIn(title), FadeIn(recipient), FadeIn(lab), run_time=.5)
        self.play(FadeIn(free), FadeIn(pair), FadeIn(virus), Create(arrows), run_time=.8)
        self.finish()


class S01Puzzle(SpokenScene):
    def construct(self):
        self.at("Bacteria can inherit")
        h = heading("Genes can arrive from another cell")
        r1 = cell(GREEN, 2.2, 1.4, .5).move_to([0,-.8,0])
        self.play(FadeIn(h), FadeIn(r1), run_time=.5)
        panels = VGroup(*[RoundedRectangle(width=4, height=4.3, corner_radius=.2,
                         stroke_color=GREY, stroke_opacity=.5).move_to([x, 0, 0]) for x in (-4.3,0,4.3)])
        self.at("three routes")
        self.play(Create(panels), r1.animate.move_to([-4.3,-.8,0]), run_time=.5)
        self.at("Transformation takes up")
        dna = Line([-5, .8,0],[-3.6,.8,0],color=BLUE,stroke_width=7)
        l1 = T("Transformation",26,BLUE).move_to([-4.3,1.65,0])
        self.play(FadeIn(l1), Create(dna), run_time=.6)
        self.play(dna.animate.move_to(r1), run_time=1)
        self.at("Conjugation passes")
        pair = small_pair(0,-.5,.75)
        l2 = T("Conjugation",26,ORANGE).move_to([0,1.65,0])
        dot = Dot(pair[0].get_center(), color=PURPLE, radius=.13)
        self.play(FadeIn(pair),FadeIn(l2),FadeIn(dot),run_time=.5)
        self.play(dot.animate.move_to(pair[1]),run_time=1)
        self.at("Transduction brings")
        r3 = cell(GREEN,2.2,1.2,.4).move_to([4.3,-1.1,0])
        virus = phage(4.3,.65)
        l3 = T("Transduction",26,GREY).move_to([4.3,1.65,0])
        self.play(FadeIn(r3),FadeIn(virus),FadeIn(l3),run_time=.6)
        self.play(virus[3].animate.move_to(r3),run_time=1)
        self.at("new genes")
        acquired = gene_chip("new gene").move_to(r1)
        self.play(ReplacementTransform(dna,acquired), Indicate(dot), Indicate(virus[3]),run_time=.7)
        self.at("even without meiosis")
        note = T("New genes without meiosis",28,GREEN).move_to([0,-2.85,0])
        self.play(FadeIn(note),run_time=.5)
        self.at("map genes")
        self.play(FadeOut(VGroup(panels,r1,l1,pair,l2,dot,r3,virus,l3,acquired,note,h)),run_time=.4)
        line, ch, times, sticks = row(0,T1,"abcd")
        self.play(FadeIn(heading("Gene order and linked markers")),Create(line),
                  *[FadeIn(ch[n]) for n in "abcd"],run_time=.7)
        self.at("which genes travel together")
        link = SurroundingRectangle(VGroup(ch['a'],ch['b']),color=PURPLE,buff=.2)
        self.play(Create(link),run_time=.6)
        self.finish()


class S02Hfr(SpokenScene):
    def construct(self):
        cd, cr = np.array([-3.7,0,0]), np.array([3.7,0,0])
        donor, recip = cell(ORANGE,4,4,1.2).move_to(cd), cell(GREEN,4,4,1.2).move_to(cr)
        ring = Circle(radius=1.15,color=BLUE,stroke_width=6).move_to(cd+[0,.3,0])
        fc = Circle(radius=.3,color=GOLD,stroke_width=5).move_to(cd+[0,-1.2,0])
        ft = T("F",26,GOLD).next_to(fc,LEFT,buff=.2)
        dl = T("F+ donor",28,ORANGE).move_to([-3.7,-2.6,0])
        rl = T("F− recipient",28,GREEN).move_to([3.7,-2.6,0])
        bridge = Line([-1.7,0,0],[1.7,0,0],color=GREY,stroke_width=8)
        self.at("In E coli")
        self.play(FadeIn(donor),FadeIn(recip),Create(ring),FadeIn(dl),FadeIn(rl),run_time=.6)
        self.at("a small DNA circle")
        self.play(Create(fc),FadeIn(ft),run_time=.5)
        self.at("When F transfers itself")
        copy = fc.copy()
        self.play(Create(bridge),run_time=.3)
        self.play(copy.animate.move_to(cr+[0,-1.2,0]),run_time=1)
        self.at("becomes")
        self.play(Transform(rl,T("F+ recipient",28,GREEN).move_to(rl)),run_time=.5)
        self.at("Chromosomal genes move")
        rare = T("Chromosome transfer: rare",26,GREY).move_to([0,2.9,0])
        self.play(FadeIn(rare),run_time=.5)
        self.at("But F can join")
        arc = Arc(radius=1.15,start_angle=70*DEGREES,angle=40*DEGREES,
                  arc_center=cd+[0,.3,0],color=GOLD,stroke_width=12)
        self.play(FadeOut(copy),Transform(rl,T("F− recipient",28,GREEN).move_to(rl)),
                  ReplacementTransform(fc,arc),ft.animate.move_to(cd+[0,1.9,0]),FadeOut(rare),run_time=.8)
        self.at("That donor is called")
        self.play(Transform(dl,T("Hfr donor",28,ORANGE).move_to(dl)),run_time=.5)
        self.at("Transfer now pulls")
        markers=VGroup(*[gene_chip(n).move_to(cd+[-.8+i*.55,.2,0]) for i,n in enumerate("abcd")])
        self.play(FadeIn(markers),run_time=.3)
        for i,m in enumerate(markers):
            self.play(m.animate.move_to([2.5+i*.8,0,0]),run_time=.45)
        trailing=chip("trailing F",GOLD,size=22).move_to([-.7,.8,0])
        self.play(FadeIn(trailing),run_time=.4)
        self.at("Pairs usually break")
        cross=VGroup(Line([-.3,-.35,0],[.3,.35,0],color=RED,stroke_width=6),
                     Line([-.3,.35,0],[.3,-.35,0],color=RED,stroke_width=6))
        self.play(Create(cross),FadeOut(bridge),run_time=.5)
        self.at("recipients rarely become")
        self.play(Indicate(rl,color=GREEN),Indicate(trailing,color=GOLD),run_time=.6)
        self.finish()


class S08Transduction(SpokenScene):
    def construct(self):
        self.at("Phages move host genes")
        self.play(FadeIn(heading("Phages carry host DNA")),run_time=.5)
        ring=Circle(radius=1.3,color=BLUE,stroke_width=6).move_to([-3.7,-.5,0])
        vl=phage(-3.7,1.5,False)
        left=T("Generalized",28,GREY).move_to([-3.7,2.55,0])
        self.at("In generalized transduction")
        self.play(FadeIn(left),Create(ring),FadeIn(vl),run_time=.6)
        frag=Arc(radius=1.3,start_angle=200*DEGREES,angle=45*DEGREES,
                 arc_center=ring.get_center(),color=PURPLE,stroke_width=12)
        self.at("sometimes packs")
        self.play(Create(frag),run_time=.4)
        packed=Line([-4.05,1.5,0],[-3.35,1.5,0],color=PURPLE,stroke_width=8)
        self.play(TransformFromCopy(frag,packed),run_time=.8)
        self.at("Any part can be carried")
        self.play(Rotate(frag,angle=100*DEGREES,about_point=ring.get_center()),run_time=.7)
        self.play(FadeIn(T("Any host region",24,PURPLE).move_to([-3.7,-2.5,0])),run_time=.4)
        self.at("In specialized transduction")
        right=T("Specialized",28,GREY).move_to([3.4,2.55,0])
        host=Line([.7,-.5,0],[6.2,-.5,0],color=BLUE,stroke_width=7)
        lam=chip("lambda",GREY,size=26).move_to([3.4,-.5,0])
        gal=gene_chip("gal").move_to([1.4,-.5,0])
        bio=gene_chip("bio").move_to([5.5,-.5,0])
        for box in (lam,gal,bio):
            box[0].set_fill(BG,opacity=1)
        self.play(FadeIn(right),Create(host),FadeIn(lam),FadeIn(gal),FadeIn(bio),run_time=.6)
        self.at("attachment site inaccurately")
        cut=VGroup(lam.copy(),gal.copy())
        self.play(cut.animate.shift(UP*1.7),FadeOut(lam),FadeOut(gal),run_time=.9)
        self.at("takes a neighboring gene")
        self.play(Indicate(cut[1],color=PURPLE),run_time=.6)
        self.at("Only genes beside")
        self.play(FadeIn(T("Only site neighbours",24,PURPLE).move_to([3.4,-2.5,0])),run_time=.6)
        self.finish()


class S09Integration(SpokenScene):
    def construct(self):
        self.at("Delivery and stable inheritance")
        self.play(FadeIn(heading("Delivery → integration")),run_time=.5)
        # A chromosome drawn as a closed track with a flat matching region.
        track=VMobject(color=BLUE,stroke_width=7).set_points_as_corners(
            [[-3,0,0],[-3,-1.8,0],[3,-1.8,0],[3,0,0],[1.8,0,0],[-1.8,0,0],[-3,0,0]])
        segment=Line([-1.8,0,0],[1.8,0,0],color=BLUE,stroke_width=8)
        fragment=Line([-1.8,1.8,0],[1.8,1.8,0],color=PURPLE,stroke_width=8)
        fl=T("linear donor fragment",26,PURPLE).move_to([0,2.5,0])
        cl=T("recipient chromosome",26,BLUE).move_to([0,-2.5,0])
        self.play(Create(track),FadeIn(cl),run_time=.6)
        self.at("A linear donor fragment")
        self.play(Create(fragment),FadeIn(fl),run_time=.6)
        self.at("matching stretch")
        self.add(segment)
        self.play(fragment.animate.shift(DOWN*.8),fl.animate.shift(DOWN*.5),Indicate(segment),run_time=.7)
        self.at("an even number of crossovers")
        crosses=VGroup(*[VGroup(Line([x-.2,.1,0],[x+.2,.9,0],color=YELLOW,stroke_width=5),
                                      Line([x+.2,.1,0],[x-.2,.9,0],color=YELLOW,stroke_width=5)) for x in (-1.55,1.55)])
        self.play(Create(crosses),run_time=.6)
        self.at("at least")
        self.play(FadeIn(T("2 crossovers: one on each side",26,YELLOW).move_to([0,-3.2,0])),run_time=.5)
        self.at("one on each side")
        self.play(fragment.animate.move_to(segment),FadeOut(segment),FadeOut(crosses),FadeOut(fl),run_time=.8)
        self.finish()


class S03Blender(SpokenScene):
    def construct(self):
        self.at("Selection makes rare recombinants")
        head=heading("Selection reveals recombinants")
        p=plate(0,0,5,2.7)
        self.play(FadeIn(head),FadeIn(p),run_time=.6)
        self.at("Only cells with every selected ability")
        cs=colonies(0,0,4,seed=5)
        note=T("Every selected ability → growth",28,GREEN).move_to([0,-2.3,0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cs],lag_ratio=.2),FadeIn(note),run_time=1)
        self.at("Interrupted mating")
        self.play(FadeOut(VGroup(p,cs,note)),Transform(head,heading("Interrupted mating")),run_time=.5)
        pairs=[small_pair(x,.4,1) for x in (-4.2,0,4.2)]
        labels=VGroup(*[T(t,24,YELLOW).move_to([x,1.9,0]) for x,t in zip((-4.2,0,4.2),("earlier","later","latest"))])
        self.play(*[FadeIn(p) for p in pairs],FadeIn(labels),run_time=.6)
        self.at("Break HFR pairs apart")
        for pair in pairs:
            self.play(FadeOut(pair[2]),pair[0].animate.shift(LEFT*.3),pair[1].animate.shift(RIGHT*.3),run_time=.35)
        self.at("score which donor genes")
        plates=VGroup(*[plate(x,0,2.9,1.4) for x in (-4.2,0,4.2)])
        dots=VGroup(*[colonies(x,0,n,seed=n) for x,n in zip((-4.2,0,4.2),(1,2,3))])
        scores=VGroup(*[T(t,26,PURPLE).move_to([x,-1.25,0]) for x,t in zip((-4.2,0,4.2),("a inherited","a, b inherited","a, b, c inherited"))])
        self.play(FadeOut(VGroup(*pairs)),FadeIn(plates),FadeIn(dots),FadeIn(scores),run_time=.7)
        self.at("A colony reports both")
        self.play(FadeIn(T("Colony = entry + integration",30,GREEN).move_to([0,-3,0])),run_time=.6)
        self.finish()


class S04Gaps(SpokenScene):
    def construct(self):
        line,ch,tl,sticks=row(.1,T1,"abcd")
        self.at("Markers")
        self.play(FadeIn(heading("Hfr strain 1: first appearance")),Create(line),
                  *[FadeIn(ch[n]) for n in "abcd"],run_time=.5)
        self.at("8")
        self.play(FadeIn(tl['a']),FadeIn(sticks['a']),run_time=.25)
        self.at("14")
        self.play(FadeIn(tl['b']),FadeIn(sticks['b']),run_time=.25)
        self.at("20")
        self.play(FadeIn(tl['c']),FadeIn(sticks['c']),run_time=.25)
        self.at("31")
        self.play(FadeIn(tl['d']),FadeIn(sticks['d']),run_time=.25)
        self.at("With steady transfer")
        self.play(FadeIn(T("Assume steady transfer",26,GREY).move_to([0,2.25,0])),run_time=.4)
        self.at("their gaps are")
        br=brackets(-1,[X(T1[n]) for n in "abcd"],["6","6","11"])
        self.play(FadeIn(br),run_time=.6)
        self.at("The gaps are the map")
        self.play(line.animate.set_stroke(width=10),FadeIn(T("a — 6 — b — 6 — c — 11 — d",30,BLUE).move_to([0,-2.7,0])),run_time=.7)
        self.finish()


class S05Reverse(SpokenScene):
    def construct(self):
        self.at("Another HFR strain")
        h=heading("The same map, read backwards")
        l1,ch1,_,_=row(1,T1,"abcd")
        l2,ch2,_,_=row(-1.4,T2,"dcba")
        br1=brackets(.4,[X(T1[n]) for n in "abcd"],["6","6","11"])
        br2=brackets(-2.1,[X(T2[n]) for n in "dcba"],["11","6","6"])
        self.play(FadeIn(h),Create(l1),FadeIn(VGroup(*ch1.values())),FadeIn(br1),run_time=.5)
        self.at("reads the same map backwards")
        self.play(Create(l2),FadeIn(VGroup(*ch2.values())),FadeIn(br2),run_time=.6)
        self.at("Different origins and orientations")
        o1,o2=origin_mark(X(0),1,1),origin_mark(X(35),-1.4,-1)
        self.play(FadeIn(o1),FadeIn(o2),FadeOut(br2),run_time=.4)
        self.play(*[ch2[n].animate.move_to([X(T1[n]),-.78,0]) for n in "abcd"],run_time=.6)
        self.at("overlapping orders")
        self.play(Indicate(VGroup(*ch1.values())),Indicate(VGroup(*ch2.values())),run_time=.5)
        self.at("close into a circle")
        self.play(FadeOut(VGroup(h,l1,l2,*ch1.values(),*ch2.values(),br1,o1,o2)),run_time=.25)
        ring,dots,labs=ring_with_genes(np.array([0,-.2,0]),2.4)
        self.play(Create(ring),FadeIn(dots),FadeIn(labs),run_time=.7)
        self.finish()


class S06Circle(SpokenScene):
    def construct(self):
        ring,dots,labs=ring_with_genes(np.array([0,-.2,0]),2.4)
        self.add(ring,dots,labs)
        self.at("Phage transfer gives a finer map")
        self.play(FadeOut(labs), VGroup(ring,dots).animate.scale(.45).move_to([-4.8,.4,0]),run_time=.7)
        region=Line([-2.5,.4,0],[5.5,.4,0],color=BLUE,stroke_width=7)
        zoom=Arrow([-3.5,.4,0],[-2.6,.4,0],buff=.1,color=GREY)
        frame=RoundedRectangle(width=8.6,height=1.3,corner_radius=.25,color=GREY).move_to([1.5,.4,0])
        self.play(Create(region),Create(zoom),Create(frame),FadeIn(heading("Within one P1 fragment")),run_time=.7)
        a,b,c=[gene_chip(n).move_to([x,.4,0]) for n,x in zip("xyz",(-1.5,-.2,4.5))]
        for box in (a,b,c):
            box[0].set_fill(BG,opacity=1)
        self.at("Genes carried together")
        self.play(FadeIn(a),FadeIn(b),FadeIn(c),run_time=.5)
        self.at("must be close")
        close=brackets(-.4,[-1.5,-.2],["close"])
        far=brackets(-1.65,[-1.5,4.5],["farther"])
        self.play(FadeIn(close),FadeIn(far),run_time=.6)
        self.at("Closer genes travel together more often")
        self.play(FadeIn(T("x + y: more often",26,GREEN).move_to([-2.8,-2.8,0])),
                  FadeIn(T("x + z: less often",26,GREY).move_to([3,-2.8,0])),run_time=.7)
        self.at("These frequencies compare distances")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.35)
        self.play(FadeIn(heading("What the readout tells us")),
                  FadeIn(chip("Two-factor frequency → proximity",BLUE,size=30).move_to([0,1,0])),run_time=.6)
        self.at("ordering genes needs")
        self.play(FadeIn(chip("Three-factor counts → order",PURPLE,size=30).move_to([0,-1,0])),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Transformation — free DNA; Conjugation — contact; Transduction — phage."

    def construct(self):
        lines=VGroup(T("Transformation — free DNA",30,BLUE),
                     T("Conjugation — contact",30,ORANGE),
                     T("Transduction — phage",30,GREY)).arrange(DOWN,buff=.35).move_to([0,1.25,0])
        delivery=T("Linear chromosome fragment: delivery → integration",26,GREEN).move_to([0,-1.1,0])
        maps=T("Gene transfer → genetic maps",30,TEXT,font=TITLE_FONT).move_to([0,-2.3,0])
        self.play(FadeIn(lines),run_time=.6)
        self.play(FadeIn(delivery),FadeIn(maps),run_time=.6)
        self.finish()
