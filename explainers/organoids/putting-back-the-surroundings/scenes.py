"""Brains in a Dish, chapter 3: Putting Back the Surroundings, and Blaming a Mutation  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video; same map as chapter 1, plus three chapter-3 concepts)
  GREY   = outlines, spheroids, unlabelled cells, tissue panels, controls
  GOLD   = interneurons: the labelled ventral cells (also the title rule)
  RED    = patient cells, the defect, what is wrong (patient tracks, mutation, the 'other explanations' cards)
  TEAL   = evidence ticks, synaptic/graft response, the rule to keep
  AMBER  = the surroundings: what comes from outside the dish (vessels, microglia, the empty outline)
           (the ORANGE of chapter 1, whose skin cells do not appear in this chapter)
  BLUE   = radial glia / progenitor zones
  GREEN  = neurons
  PINK   = the L-type calcium channel and its blocker plug (new in this chapter)
  PURPLE = hairpin RNAs, CDK5RAP2 and its centrosome
  WHITE  = nuclei and the whisker (TEXT colour)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F29E4C"
PINK = "#E27BB0"
PURPLE = "#B69BEA"

SR = 2.1                                  # spheroid radius
LC = np.array([-3.4, -0.2, 0.0])          # left spheroid centre (cortical)
RC = np.array([3.4, -0.2, 0.0])           # right spheroid centre (ventral)
FL = np.array([-1.75, -0.2, 0.0])         # fused: left centre
FR = np.array([1.75, -0.2, 0.0])          # fused: right centre


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cpos(n, area, phi=0.0, k=0.8):
    """n points in a sunflower pattern inside a disc (offsets from the centre)."""
    out = []
    for i in range(n):
        r = area * k * np.sqrt((i + 0.5) / n)
        a = i * 2.39996 + phi
        out.append(np.array([r * np.cos(a), r * np.sin(a), 0.0]))
    return out


def dot(center, color=GREY, r=0.17, op=0.4, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to(center)


def dots(center, n, area, color=GREY, phi=0.0, r=0.17):
    return VGroup(*[dot(center + p, color, r) for p in cpos(n, area, phi)])


def sph(center, R=SR, color=GREY):
    return Circle(radius=R, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.14).move_to(center)


def union_outline(c1, c2, R=SR, color=GREY):
    """outline of two overlapping equal circles (centres c1, c2 at the same height)."""
    d = (c2[0] - c1[0]) / 2
    th = np.arctan2(np.sqrt(R * R - d * d), d)
    pts = [[c1[0] + R * np.cos(a), c1[1] + R * np.sin(a), 0] for a in np.linspace(th, TAU - th, 90)]
    pts += [[c2[0] + R * np.cos(a), c2[1] + R * np.sin(a), 0] for a in np.linspace(PI + th, 3 * PI - th, 90)]
    return Polygon(*pts, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.14)


def fused(scale=1.0, at=None):
    """the fused pair: union outline, cortical cells (grey) left, labelled ventral cells (gold) right."""
    u = union_outline(FL, FR)
    lc = dots(FL, 11, 1.5, GREY)
    rc = dots(FR, 11, 1.5, GOLD, phi=1.0)
    g = VGroup(u, lc, rc)
    if scale != 1.0:
        g.scale(scale)
    if at is not None:
        g.move_to(at)
    return g


def lab(text, size=24, color=TEXT, **kw):
    return T(text, max(26, size), color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ghost(r, center, color):
    return DashedVMobject(Circle(radius=r, stroke_color=color, stroke_width=3), num_dashes=20).move_to(center)


def tick(color=TEAL, s=0.5):
    m = VMobject(stroke_color=color, stroke_width=9)
    m.set_points_as_corners([[-0.5 * s, 0.0, 0], [-0.12 * s, -0.42 * s, 0], [0.6 * s, 0.5 * s, 0]])
    return m


def stamp(center, text="tested", color=TEAL):
    c = chip(text, color, 24, pad=0.16, fill_opacity=0.22)
    return c.move_to(center)


def neuron_cell(center, r=1.0, color=GOLD, nuc=0.42):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25).move_to(center)
    nucl = Circle(radius=nuc, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.6).move_to(center)
    return body, nucl


def channel(center, width=4.2, plug=False):
    """membrane bar with a channel cartoon (pink block with a pore); optional red plug in the pore."""
    mem = Rectangle(width=width, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45)
    blk = RoundedRectangle(corner_radius=0.1, width=1.0, height=1.05, stroke_color=PINK, stroke_width=4,
                           fill_color=PINK, fill_opacity=0.4)
    pore = Rectangle(width=0.2, height=1.05, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(mem, blk, pore)
    if plug:
        g.add(Rectangle(width=0.2, height=0.55, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.9)
              .move_to(pore.get_center() + UP * 0.15))
    return g.move_to(center)


def hairpin(stem=1.0, w=0.3, color=PURPLE):
    l = Line([-w / 2, -stem / 2, 0], [-w / 2, stem / 2, 0])
    r = Line([w / 2, -stem / 2, 0], [w / 2, stem / 2, 0])
    loop = Arc(radius=w / 2, start_angle=0, angle=PI, arc_center=[0, stem / 2, 0])
    return VGroup(l, r, loop).set_stroke(color, width=8)


def zone_set(center, R, scale):
    offs = [(-0.38, 0.30), (0.40, 0.38), (0.0, -0.42)]
    return VGroup(*[Circle(radius=R * 0.30 * scale, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
                    .move_to(center + np.array([R * x, R * y, 0])) for x, y in offs])


def glia(center):
    return Ellipse(width=0.34, height=0.85, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4).move_to(center)


def neu(center):
    return Circle(radius=0.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4).move_to(center)


def free_spots(rng, n, center, rad, taken, mind=0.46):
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        a, r = rng.uniform(0, TAU), rad * np.sqrt(rng.uniform(0, 1))
        p = center + np.array([r * np.cos(a), r * np.sin(a), 0])
        if all(np.linalg.norm(p - q) > mind for q in list(taken) + pts):
            pts.append(p)
    return pts


def jump_cell(x0, y=0.3, r=1.0, nuc=0.42, plen=5.0, sw_dx=2.3):
    """geometry pieces of one gold cell's jump: soma, nucleus, process, swelling, ghost of the start."""
    soma, nucl = neuron_cell(np.array([x0, y, 0]), r, GOLD, nuc)
    proc = Line([x0 + r * 0.9, y, 0], [x0 + plen, y, 0], stroke_color=GOLD, stroke_width=10)
    swell = Ellipse(width=r * 1.5, height=r * 1.2, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.35)
    swell.move_to([x0 + sw_dx, y, 0])
    return soma, nucl, proc, swell


# step curves: position against time; every jump is a fast rise followed by a pause (computed, not sketched)
def jumps(t, times, h, k=14.0):
    return float(sum(h * 0.5 * (1 + np.tanh(k * (t - ti))) for ti in times))


CTRL_T = [1.4, 3.6, 5.8, 8.0]
CTRL_H = 1.5
PAT_T = [0.9 + 1.0 * i for i in range(9)]
PAT_H = 0.45
FIX_H = 0.62


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Brains in a Dish: Stem Cells and Organoids"
    TITLE = "Putting Back the Surroundings, and Blaming a Mutation"
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 26, TEAL).move_to([0,2.6,0])
        lesson = T(self.LESSON, 28, GREY).move_to([0,1.8,0])
        rule = Line([-1.2,1.15,0],[1.2,1.15,0],color=GOLD,stroke_width=4)
        title = VGroup(T("Putting Back the Surroundings,",44,font=TITLE_FONT),
                       T("and Blaming a Mutation",44,font=TITLE_FONT)).arrange(DOWN,buff=0.3).move_to([0,-0.2,0])
        self.add(brand,lesson,rule)
        self.play(FadeIn(title),run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """a cortical organoid with an empty amber outline where interneurons should arrive."""

    def construct(self):
        org = sph(LC)
        oc = dots(LC, 11, 1.5, GREY)
        ol = lab("cortical organoid", 26).move_to(LC + DOWN * 2.6)
        self.play(FadeIn(org), FadeIn(oc), FadeIn(ol), run_time=0.6)

        self.at("interneurons")
        ring = [LC + 1.72 * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(0.3, 0.3 + TAU, 8)[:-1]]
        gh = VGroup(*[ghost(0.2, p, AMBER) for p in ring])
        gl = lab("cortical interneurons", 26, AMBER).move_to(LC + UP * 2.65)
        self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in gh], lag_ratio=0.1), FadeIn(gl), run_time=1.1)

        self.at("another region")
        vs = sph(RC)
        vc = dots(RC, 11, 1.5, GREY, phi=1.0)
        self.play(FadeIn(vs), FadeIn(vc), run_time=0.9)

        self.at("ventral forebrain")
        vl = lab("ventral forebrain", 26).move_to(RC + DOWN * 2.6)
        self.play(FadeIn(vl, shift=UP * 0.1), run_time=0.5)

        self.at("how could")
        a = arr(RC + LEFT * 2.2, LC + RIGHT * 2.2, AMBER, 6)
        q = T("?", 80, AMBER, weight=BOLD).move_to([0, 1.0, 0])
        self.play(GrowArrow(a), FadeIn(q, scale=0.6), run_time=0.9)

        self.at("get them")
        self.play(*[Indicate(g, color=AMBER, scale_factor=1.35) for g in gh], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Supply(SpokenScene):
    """credit card; a dorsal (cortical) and a ventral (subpallial) spheroid, grown separately."""

    def construct(self):
        org = sph(LC)
        oc = dots(LC, 11, 1.5, GREY)
        self.add(org, oc, lab("dorsal (cortical)",28).move_to(LC+DOWN*2.6))
        vs = sph(RC)
        vc = dots(RC, 11, 1.5, GREY, phi=1.0)
        self.play(FadeIn(vs, scale=0.85), FadeIn(vc, scale=0.85), FadeIn(lab("ventral (subpallial)",28).move_to(RC+DOWN*2.6)), run_time=0.6)

        self.at("In 2017")
        c1 = T("Birey, Andersen, Makinson, Pașca and colleagues", 26)
        c2 = T("Stanford, 2017", 24, GREY)
        cred = VGroup(c1, c2).arrange(DOWN, buff=0.14).move_to([0, 2.95, 0])
        box = SurroundingRectangle(cred, color=GREY, buff=0.2, corner_radius=0.12, stroke_width=2)
        self.play(FadeIn(cred, shift=DOWN * 0.1), Create(box), run_time=0.8)

        self.at("grew the two")
        l1 = lab("dorsal (cortical)", 26).move_to(LC + DOWN * 2.6)
        l2 = lab("ventral (subpallial)", 26).move_to(RC + DOWN * 2.6)
        self.wait(0.1)

        self.at("separately")
        gap = DashedLine([0, 1.9, 0], [0, -2.4, 0], color=GREY, stroke_width=3)
        self.play(Create(gap), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Fuse(SpokenScene):
    """ventral cells turn gold; the two spheroids are pressed together and merge."""

    def construct(self):
        lsph, lcells = sph(LC), dots(LC, 11, 1.5, GREY)
        rsph, rcells = sph(RC), dots(RC, 11, 1.5, GREY, phi=1.0)
        l1 = lab("dorsal (cortical)", 26).move_to(LC + DOWN * 2.6)
        l2 = lab("ventral (subpallial)", 26).move_to(RC + DOWN * 2.6)
        self.add(lsph, lcells, rsph, rcells, l1, l2)

        self.at("ventral cells")
        l3 = lab("labelled ventral cells", 26, GOLD).move_to(RC + DOWN * 2.6)
        self.play(*[c.animate.set_stroke(GOLD).set_fill(GOLD, 0.45) for c in rcells], Transform(l2, l3), run_time=0.5)

        self.at("then let one")
        L = VGroup(lsph, lcells)
        R = VGroup(rsph, rcells)
        self.play(l1.animate.move_to(FL+DOWN*2.6), l2.animate.move_to(FR+DOWN*2.6),
                  lcells.animate.shift(RIGHT*1.65), rcells.animate.shift(LEFT*1.65),
                  Transform(lsph, union_outline(FL,FR)), FadeOut(rsph), run_time=1.0)

        self.at("fuse")
        u = union_outline(FL, FR)
        self.wait(0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pair_labels():
    return VGroup(lab("cortical", 26).move_to(FL + DOWN * 2.5), lab("ventral (gold cells)", 26, GOLD).move_to(FR + DOWN * 2.5))


def predict_frame():
    chipp = chip("Predict", TEAL, 28).move_to([-5.4, 3.2, 0])
    l1 = T("Which way will the labelled cells move?", 30)
    l2 = T("And how?", 30, TEAL)
    g = VGroup(l1, l2).arrange(RIGHT, buff=0.3).move_to([0.9, 3.2, 0])
    return chipp, l1, l2


class S04Predict(SpokenScene):
    def construct(self):
        self.add(fused(), pair_labels())
        chipp, l1, l2 = predict_frame()
        self.play(FadeIn(chipp, shift=DOWN * 0.1), run_time=0.5)
        self.at("which way")
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.8)
        self.at("and how")
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        self.add(fused(), pair_labels())
        chipp, l1, l2 = predict_frame()
        self.add(chipp, l1, l2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Reveal(SpokenScene):
    """a broad stream of gold cells ventral -> cortical; only a trickle the other way."""

    def construct(self):
        u = union_outline(FL, FR)
        lcells = dots(FL, 11, 1.5, GREY)
        rcells = dots(FR, 11, 1.5, GOLD, phi=1.0)
        self.add(u, lcells, rcells, pair_labels())
        rng = np.random.default_rng(7)
        order = sorted(range(11), key=lambda i: rcells[i].get_center()[0])
        movers = [rcells[i] for i in order[:8]]
        taken = [c.get_center() for c in lcells] + [rcells[i].get_center() for i in order[8:]]
        spots = free_spots(rng, 8, FL, 1.8, taken, mind=0.48)
        self.wait(0.4)

        self.at("moved from")
        self.play(LaggedStart(*[m.animate.move_to(p) for m, p in zip(movers, spots)], lag_ratio=0.16), run_time=2.4)

        self.at("far more")
        big = arr([1.0,0.8,0], [-1.0,0.8,0], GOLD, 14, 0.45).set_y(0.8)
        bl = lab("ventral into cortical: far more often", 26, GOLD).move_to([0, 3.4, 0])
        self.play(GrowArrow(big), FadeIn(bl), run_time=0.9)

        self.at("the reverse")
        lone = max(lcells, key=lambda c: c.get_center()[0])
        tgt = free_spots(rng, 1, FR + DOWN * 0.3, 1.2, [c.get_center() for c in rcells] + [lone.get_center()])[0]
        small = arr([-1,-0.9,0], [1,-0.9,0], TEXT, 5, 0.25)
        sl = lab("reverse: only a trickle", 28, TEXT).move_to([0, -3.25, 0])
        self.play(GrowArrow(small), FadeIn(sl), lone.animate.move_to(tgt), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Jump(SpokenScene):
    def construct(self):
        start=np.array([-4.5,0.7,0]); target=np.array([1.0,0.7,0])
        soma,nucleus=neuron_cell(start,1.85,GOLD,0.75)
        process=Line(start+RIGHT*1.65,target,stroke_color=GOLD,stroke_width=14)
        swelling=Ellipse(width=1.65,height=1.4,color=GOLD,fill_opacity=0.4).move_to(target)
        self.add(soma,nucleus,T("One cell, one jump",34,GOLD).move_to([0,3.1,0]))
        captions=VGroup(*[T(t,28) for t in ["1  Process extends","2  Swelling forms","3  Nucleus follows"]]).arrange(RIGHT,buff=0.55).move_to([0,-2.65,0])
        self.at("leading process")
        self.play(Create(process),FadeIn(captions[0]),run_time=0.7)
        self.at("swelling forms")
        self.play(FadeIn(swelling),FadeIn(captions[1]),run_time=0.7)
        self.at("then the nucleus")
        old=ghost(1.85,start,TEXT)
        self.add(old)
        self.play(soma.animate.move_to(target),nucleus.animate.move_to(target),FadeOut(swelling),FadeOut(process),FadeIn(captions[2]),run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Fetal(SpokenScene):
    def construct(self):
        start=np.array([-5.0,0,0]); target=np.array([-2.0,0,0])
        soma,nucleus=neuron_cell(start,1.4,GREY,0.5)
        process=Line(start+RIGHT*1.2,target,color=GREY,stroke_width=12)
        swelling=Ellipse(width=1.5,height=1.2,color=GREY,fill_opacity=0.5).move_to(target)
        steps=VGroup(*[T(t,26) for t in ["extend", "swell", "follow"]]).arrange(RIGHT,buff=0.35).move_to([-3.6,-2.4,0])
        self.add(soma,nucleus,T("fetal interneuron",28).move_to([-3.6,3.0,0]),steps)
        self.at("Fetal",lead=0)
        self.play(Create(process),steps[0].animate.set_color(TEXT),run_time=0.8)
        self.play(FadeIn(swelling),Indicate(steps[1],color=TEXT),run_time=0.65)
        self.at("same way",lead=0.15)
        old=ghost(1.4,start,GREY)
        self.add(old)
        self.play(soma.animate.move_to(target),nucleus.animate.move_to(target),FadeOut(process),FadeOut(swelling),Indicate(steps[2],color=TEXT),run_time=0.85)
        self.at("once inside")
        C=np.array([3.4,0,0]); org=sph(C,2.7)
        ring=VGroup(*[dot(C+2.0*np.array([np.cos(a),np.sin(a),0]),GREY,0.2) for a in np.linspace(0,TAU,8,endpoint=False)])
        cell,nuc=neuron_cell(C,0.8,GOLD,0.3)
        self.play(FadeIn(VGroup(org,ring,cell,nuc)),FadeIn(T("cortical spheroid",28).move_to([3.4,3.15,0])),run_time=0.6)
        self.at("excitatory")
        links=VGroup(*[Line(c.get_center(),C+0.8*(c.get_center()-C)/np.linalg.norm(c.get_center()-C),color=TEAL,stroke_width=6) for c in list(ring)[::3]])
        self.play(Create(links),FadeIn(T("excitatory synaptic input",26,TEAL).move_to([3.4,-3.2,0])),run_time=0.5)
        self.play(Indicate(cell,color=TEAL),run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Beat(NarratedScene):
    def construct(self):
        C=np.array([2.4,0,0]); cell,nucleus=neuron_cell(C,0.8,GOLD,0.3)
        pic=VGroup(sph(C,2.6),VGroup(*[dot(C+2.0*np.array([np.cos(a),np.sin(a),0]),GREY,0.2) for a in np.linspace(0,TAU,8,endpoint=False)]),cell,nucleus,
                   T("excitatory synaptic input",28,TEAL).move_to([2.4,-3.1,0]),
                   T("fetal interneuron: same jump",28).move_to([-3.5,2.6,0]))
        fetal,fn=neuron_cell(np.array([-3.2,0,0]),1.05,GREY,0.4)
        pic.add(fetal,fn)
        self.add(pic.fade(0.45)); self.finish()


# ---------------------------------------------------------------------------------------------
class S10Ts(SpokenScene):
    """patient cells -> CACNA1C with a mutation -> the L-type calcium channel."""

    def construct(self):
        body, nucl = neuron_cell(np.array([-4.5, 0.5, 0]), 1.1, GOLD, 0.46)
        pl = lab("patient interneuron", 26, RED).move_to([-4.5, -1.2, 0])
        self.play(FadeIn(body, scale=0.6), FadeIn(nucl, scale=0.6), FadeIn(pl), run_time=0.8)

        self.at("Timothy syndrome")
        head = T("Timothy syndrome", 44, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(head), run_time=1.0)

        self.at("a mutation")
        bar = RoundedRectangle(corner_radius=0.15, width=3.6, height=0.6, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.25).move_to([0.2, 0.9, 0])
        gl = T("CACNA1C", 30).next_to(bar, UP, buff=0.2)
        mut = Rectangle(width=0.22, height=0.6, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(bar.get_center() + RIGHT * 0.7)
        ml = lab("gain-of-function", 26, RED).next_to(bar, DOWN, buff=0.3)
        self.play(FadeIn(bar), FadeIn(gl), run_time=0.7)
        self.play(FadeIn(mut, scale=2.0), FadeIn(ml), run_time=0.6)

        self.at("calcium channel")
        ch = channel([4.1, -0.5, 0], width=3.6).scale(1.3)
        a = arr([2.1, 0.9, 0], [3.7, 0.3, 0], GREY, 4, 0.2)
        cl = VGroup(lab("L-type calcium channel", 28, PINK), lab("Cav1.2", 28, PINK)).arrange(DOWN, buff=0.1).move_to([4.1, -2.1, 0])
        self.play(GrowArrow(a), FadeIn(ch), FadeIn(cl), FadeIn(lab("passes more calcium",26,PINK).move_to([0,-3.15,0])), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def make_axes(center, xl=10.0, yl=5.8, ymax=7.0):
    ax = Axes(x_range=[0, 10, 2], y_range=[0, ymax, 1], x_length=xl, y_length=yl,
              axis_config={"color": GREY, "include_ticks": False, "include_tip": True, "tip_length": 0.18, "stroke_width": 3})
    return ax.move_to(center)


def curve(ax, times, h, color, dashed=False, tmax=9.8, width=5):
    f = lambda t: jumps(t, times, h)
    c = ax.plot(f, x_range=[0, tmax, 0.02], color=color, stroke_width=width, use_smoothing=False)
    return DashedVMobject(c, num_dashes=90, dashed_ratio=0.6) if dashed else c


class S11Ts2(SpokenScene):
    """control (fewer, longer jumps) against patient (more, shorter jumps): less ground covered."""

    def construct(self):
        ax = make_axes([-0.9, -0.1, 0])
        tl = lab("time", 24, GREY).move_to([3.3,-3.4,0])
        dl = lab("distance moved", 24, GREY).next_to(ax.y_axis.get_end(), RIGHT, buff=0.2).shift(UP * 0.1)
        cc = curve(ax, CTRL_T, CTRL_H, GREY, dashed=True)
        pc = curve(ax, PAT_T, PAT_H, RED)
        cl = lab("control", 28, GREY).move_to(ax.c2p(9.8, jumps(9.8, CTRL_T, CTRL_H)) + RIGHT * 1.25)
        pl = lab("patient", 28, RED).move_to(ax.c2p(9.8, jumps(9.8, PAT_T, PAT_H)) + RIGHT * 1.25)
        sub = lab("illustrative tracks", 22, GREY).move_to([0.5, -3.55, 0])
        self.play(FadeIn(ax), FadeIn(tl), FadeIn(dl), FadeIn(sub), run_time=0.3)
        self.play(Create(cc), FadeIn(cl), run_time=0.6, rate_func=linear)
        self.play(Create(pc), FadeIn(pl), run_time=1.3, rate_func=linear)

        self.at("shorter ones")
        r1 = SurroundingRectangle(Line(ax.c2p(0.8, 0.0), ax.c2p(1.2, PAT_H)), color=RED, buff=0.12, stroke_width=3)
        r2 = SurroundingRectangle(Line(ax.c2p(1.2, 0.0), ax.c2p(1.6, CTRL_H)), color=GREY, buff=0.1, stroke_width=3)
        t1 = lab("shorter", 24, RED).next_to(r1, DOWN, buff=0.1).shift(LEFT * 0.2)
        t2 = lab("longer", 24, TEXT).next_to(r2, RIGHT, buff=0.12).shift(UP * 0.3)
        self.play(Create(r1), FadeIn(t1), run_time=0.6)
        self.play(Create(r2), FadeIn(t2), run_time=0.6)

        self.at("Overall")
        yp, yc = jumps(9.8, PAT_T, PAT_H), jumps(9.8, CTRL_T, CTRL_H)
        gap = DoubleArrow(ax.c2p(9.95, yp), ax.c2p(9.95, yc), buff=0.02, color=TEXT, stroke_width=4, tip_length=0.2)
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(t1), FadeOut(t2), Create(gap), run_time=0.8)

        self.at("less efficiently")
        eff = T("less efficient", 26, RED).next_to(gap,RIGHT,buff=0.15)
        self.play(FadeIn(eff, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Ts3(SpokenScene):
    def construct(self):
        pair=fused(0.78,at=[-3.6,0.15,0]).stretch(1.35,1)
        labels=VGroup(T("control cortex",26),T("patient ventral",26,RED)).arrange(DOWN,buff=0.15).move_to([-3.6,2.95,0])
        ax=make_axes([3.2,-0.2,0],xl=5.5,yl=5.6)
        cc=curve(ax,CTRL_T,CTRL_H,GREY,True); pc=curve(ax,PAT_T,PAT_H,RED)
        self.add(pair,labels,ax,T("distance moved",26).move_to([3.3,3.1,0]),T("time",26).move_to([5.7,-3.35,0]),T("illustrative tracks",26,GREY).move_to([2.8,-3.35,0]))
        self.play(Create(cc),FadeIn(T("control",26,GREY).move_to([3.0,2.45,0])),run_time=0.5)
        self.at("patient interneurons")
        self.play(Create(pc),run_time=0.7)
        self.at("the defect")
        df=T("the defect again",26,RED).move_to([3.2,3.55,0])
        self.play(FadeIn(df),run_time=0.4)
        self.at("in the interneurons themselves")
        self.play(Indicate(pair[2],color=GOLD),run_time=0.6)
        self.at("Blocking")
        ch=channel([-3.6,-2.5,0],width=4.8,plug=True)
        fixed=curve(ax,PAT_T,FIX_H,PINK)
        self.play(FadeIn(ch),FadeIn(T("L-type channel blocked",26,PINK).move_to([-3.6,-3.35,0])),FadeOut(df),Create(fixed),FadeIn(T("blocker: longer jumps",26,PINK).move_to([3.1,3.55,0])),run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mini_pair(center, s=0.4):
    a = Circle(radius=s, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to(center + LEFT * s * 0.85)
    b = Circle(radius=s, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.4).move_to(center + RIGHT * s * 0.85)
    return VGroup(a, b)


def mini_channel(center):
    return channel(center, width=1.2, plug=True).scale(0.75)


class S13Prog(SpokenScene):
    """teal ticks beside the fused hybrid and the channel blocker: evidence for a defect in the cell's own program."""

    def construct(self):
        cw, ch_ = 10.8, 1.3
        cx = -0.5
        cards = []
        for y, text in ((2.45, "fused to control cortex: the defect stayed"), (0.85, "blocking L-type channels: migration improved")):
            box = RoundedRectangle(corner_radius=0.16, width=cw, height=ch_, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12).move_to([cx, y, 0])
            t = lab(text, 26).move_to(box.get_center() + RIGHT * 0.65)
            cards.append((box, t))
        icon1 = mini_pair([cx - 4.3, 2.45, 0])
        icon2 = mini_channel([cx - 4.3, 0.85, 0])
        self.play(FadeIn(cards[0][0]), FadeIn(cards[0][1]), FadeIn(icon1), run_time=0.7)
        self.play(FadeIn(cards[1][0]), FadeIn(cards[1][1]), FadeIn(icon2), run_time=0.7)

        self.at("not the channel's")
        loc = chip("channel’s location", GREY, 28).move_to([cx, -0.65, 0])
        xx = Cross(loc, stroke_color=RED, stroke_width=2, scale_factor=1.0)
        self.play(FadeIn(loc), run_time=0.5)
        self.play(Create(xx), run_time=0.5)

        self.at("point to")
        t1 = tick().move_to([4.6, 2.45, 0])
        t2 = tick().move_to([4.6, 0.85, 0])
        self.play(FadeOut(loc), FadeOut(xx), run_time=0.4)
        self.play(Create(t1), Create(t2), run_time=0.8)

        self.at("own program")
        st = VGroup(T("evidence for a defect in", 38, TEAL), T("the cells’ own program (at least in part)", 30, TEAL)).arrange(DOWN, buff=0.15).move_to([cx, -1.2, 0])
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.9)

        self.at("An")
        asm = VGroup(mini_pair(ORIGIN, 0.5), chip("assembloid", GREY, 30)).arrange(RIGHT, buff=0.3).move_to([cx, -3.0, 0])
        self.play(FadeIn(asm, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cortex_shape(sc=1.0, center=(0.0, 0.1, 0.0)):
    e = Ellipse(width=8.0, height=4.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    return e.scale(sc).move_to(center)


def vessels(center, R):
    """amber vessels threaded through the graft (curves, not molecules)."""
    out = VGroup()
    for ang, off, ph in ((0.0, -0.4, 0.3), (0.0, 0.05, 1.1), (0.0, 0.5, 2.0), (1.57, -0.3, 0.7), (1.57, 0.3, 1.7), (0.8, 0.0, 2.6)):
        d = np.array([np.cos(ang), np.sin(ang), 0])
        n = np.array([-np.sin(ang), np.cos(ang), 0])
        f = lambda t, d=d, n=n, off=off, ph=ph: center + R * 0.9 * t * d + n * R * (off + 0.12 * np.sin(4 * t + ph))
        out.add(ParametricFunction(f, t_range=[-0.8, 0.8], stroke_color=AMBER, stroke_width=5))
    return out


class S14Host(SpokenScene):
    def construct(self):
        cortex=cortex_shape(1.18,[-0.3,0,0])
        snout=Polygon([3.9,1.0,0],[6,0,0],[3.9,-1,0],color=GREY,fill_opacity=0.15)
        ear=Circle(radius=0.65,color=GREY).move_to([2.9,2,0])
        eye=dot([4.2,0.55,0],TEXT,0.12,1,0)
        self.add(cortex,snout,ear,eye,T("newborn rat cortex",30).move_to([-0.5,3.2,0]),T("Pașca group, 2022",28,TEXT).move_to([2,-3.3,0]))
        graft=sph([-4.8,0,0],0.85,TEXT)
        self.at("Human organoids")
        label=T("human organoid",26).move_to([-4.7,-1.5,0])
        self.play(FadeIn(graft),FadeIn(label),run_time=0.5)
        self.at("transplanted")
        self.play(graft.animate.move_to([0.2,0.1,0]).scale(2.15),FadeOut(label),run_time=0.7)
        self.at("As the rats matured")
        self.play(FadeIn(chip("months later",TEXT,28,fill_opacity=0.4).move_to([-3,-3.1,0])),run_time=0.5)
        self.at("grafts gained")
        vs=vessels(np.array([0.2,0.1,0]),1.75)
        vl=T("blood vessels",28,AMBER).move_to([-3.5,1.8,0])
        leader=VMobject(color=AMBER,stroke_width=4).set_points_as_corners([vl.get_bottom()+DOWN*0.15,[-3.5,0.7,0],vs[1].point_from_proportion(0.25)])
        self.play(Create(vs),FadeIn(vl),Create(leader),run_time=0.65)
        self.at("responded")
        whisker=Line([5.8,0,0],[6.3,-1.7,0],color=TEXT,stroke_width=9)
        old_whisker=DashedVMobject(whisker.copy().set_stroke(GREY,4),num_dashes=8)
        self.add(whisker,old_whisker)
        self.play(Rotate(whisker,angle=-0.85,about_point=[5.8,0,0]),graft.animate.set_fill(TEAL,0.8).set_stroke(TEAL,8),
                  FadeIn(T("graft responds",28,TEAL).move_to([0.2,-2.15,0])),
                  FadeIn(T("whisker deflected",26).move_to([4.5,-2.4,0])),run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15Beat(NarratedScene):
    def construct(self):
        C=np.array([0.2,0.3,0])
        pic=VGroup(cortex_shape(1.18,[-0.3,0,0]),sph(C,1.19,TEAL),vessels(C,1.1),
                   T("graft responds",30,TEAL).move_to([0,-1.4,0]),
                   T("Pașca group, 2022",28).move_to([0,-3.3,0]))
        self.add(pic.fade(0.45)); self.finish()


# ---------------------------------------------------------------------------------------------
PL = np.array([-3.4, -0.2, 0])
PR = np.array([3.4, -0.2, 0])


class S16Hook(SpokenScene):
    """credit; patient organoid; microcephaly; CDK5RAP2; smaller progenitor zones; is the mutation to blame?"""

    def construct(self):
        c1 = T("Lancaster, Knoblich and colleagues, 2013", 26)
        cred = c1.move_to([0, 3.35, 0])
        self.add(cred)

        po = sph(PL, 1.9)
        pc = dots(PL, 9, 1.4, GREY, r=0.17)
        self.play(FadeIn(po, scale=0.8), FadeIn(pc, scale=0.8), run_time=0.9)

        self.at("grew organoids")
        pol = lab("organoid from a patient", 26).move_to(PL + DOWN * 2.45)
        self.play(FadeIn(pol, shift=UP * 0.1), run_time=0.6)

        self.at("microcephaly")
        ml = lab("microcephaly", 28, RED).move_to(PR + DOWN * 2.45)
        small = Ellipse(width=2.4, height=1.8, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to(PR)
        self.play(FadeIn(small, scale=0.6), FadeIn(ml), run_time=0.8)

        self.at("smaller than normal")
        norm = DashedVMobject(Ellipse(width=3.9, height=2.9, stroke_color=GREY, stroke_width=3), num_dashes=40).move_to(PR)
        nl = lab("normal size", 24, GREY).move_to(PR + UP * 1.9)
        self.play(Create(norm), FadeIn(nl), run_time=1.0)

        self.at("mutations")
        mt = lab("mutations in CDK5RAP2", 30, PURPLE).move_to([0, 2.45, 0])
        self.play(FadeIn(mt, shift=RIGHT * 0.1), run_time=0.5)
        self.at("gene called")
        self.wait(0.1)

        self.at("patient's organoids")
        co = sph(PR, 1.9)
        zp = zone_set(PL, 1.9, 0.62)
        zc = zone_set(PR, 1.9, 1.0)
        lp = lab("patient", 28, RED).move_to(PL + DOWN * 2.45)
        lc = lab("control", 28, GREY).move_to(PR + DOWN * 2.45)
        self.play(FadeOut(small), FadeOut(norm), FadeOut(nl), FadeOut(ml), FadeOut(cred), Transform(pc, zp), FadeTransform(pol, lp),
                  FadeIn(co), FadeIn(lc), run_time=0.8)

        self.at("smaller progenitor zones")
        zl = VGroup(lab("progenitor", 24, BLUE), lab("zones", 24, BLUE)).arrange(DOWN, buff=0.08).move_to([0, -0.2, 0])
        self.play(FadeIn(zc, scale=0.5), FadeIn(zl), run_time=0.9)
        self.play(Indicate(pc, color=BLUE, scale_factor=1.2), run_time=0.6)

        self.at("to blame")
        q = T("Is the mutation to blame?", 38).move_to([0, -3.35, 0])
        self.play(FadeIn(q, shift=UP * 0.1), Indicate(mt, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
ROW_Y = [1.05, -0.45, -1.95]
CARD_C = np.array([-4.6, 0, 0])


def heading(chipped=True, size=30, y1=3.25, y2=2.6):
    l1 = T("Name three other explanations,", size)
    l2 = T("and a control that tests each.", size, TEAL)
    g = VGroup(l1, l2).arrange(DOWN, buff=0.1).move_to([0.9, (y1 + y2) / 2, 0])
    chp = chip("Predict", TEAL, 28).move_to([-5.4, 3.0, 0])
    return chp, l1, l2


def slot(i):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=3.8, height=1.1, stroke_color=GREY, stroke_width=3),
                         num_dashes=40).move_to([-4.3, ROW_Y[i], 0])
    return VGroup(box, T("?", 44, GREY).move_to(box))


def ctrl_slot(i):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=8.2, height=1.1, stroke_color=GREY, stroke_width=3),
                         num_dashes=60).move_to([1.95, ROW_Y[i], 0])
    return VGroup(box, lab("a control that tests it", 28, TEXT).move_to(box))


def card(i, text):
    box = RoundedRectangle(corner_radius=0.16, width=3.8, height=1.1, stroke_color=RED, stroke_width=3,
                           fill_color=RED, fill_opacity=0.12).move_to([-4.3, ROW_Y[i], 0])
    return VGroup(box, T(text, 26).move_to(box))


def row_orgs(i, kind):
    y = ROW_Y[i]
    if kind == 0:
        g = VGroup(*[dot([x, y, 0], GREY, 0.4, 0.2, 4) for x in (-1.4, -0.4, 0.6)])
        lb = VGroup(lab("control organoids", 22), lab("from several people", 22)).arrange(DOWN, buff=0.06).move_to([3.1, y, 0])
    elif kind == 1:
        g = VGroup(*[dot([x, y, 0], RED, 0.4, 0.2, 4) for x in (-1.4, -0.4, 0.6)])
        lb = VGroup(lab("several clones", 22), lab("from the patient", 22, RED)).arrange(DOWN, buff=0.06).move_to([3.1, y, 0])
    else:
        g = VGroup()
        for cx in (-1.6, -0.3, 1.0):
            g.add(dot([cx - 0.32, y, 0], RED, 0.3, 0.2, 4), dot([cx + 0.32, y, 0], GREY, 0.3, 0.2, 4))
        lb = VGroup(lab("patient + control", 26), lab("repeated batches", 26)).arrange(DOWN, buff=0.06).move_to([3.05, y, 0])
    return g, lb


def stamp_at(i):
    return stamp([5.7, ROW_Y[i], 0], "helps", GREY)


def rows_done(n):
    """rebuild the first n finished rows (card, controls, label, stamp)."""
    out = VGroup()
    texts = ["genetic background", "a quirk of one line", "a bad batch"]
    for i in range(n):
        g, lb = row_orgs(i, i)
        out.add(card(i, texts[i]), g, lb, stamp_at(i))
    return out


class S17Predict(SpokenScene):
    def construct(self):
        chp, l1, l2 = heading()
        self.play(FadeIn(chp, shift=DOWN * 0.1), run_time=0.5)
        self.at("name three")
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(slot(i), scale=0.9) for i in range(3)], lag_ratio=0.25), run_time=1.2)
        self.at("and a control")
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(ctrl_slot(i)) for i in range(3)], lag_ratio=0.25), run_time=1.2)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        chp, l1, l2 = heading()
        self.add(chp, l1, l2, *[slot(i) for i in range(3)], *[ctrl_slot(i) for i in range(3)])
        self.finish()


def rows_stage(scene, done, current):
    """rebuild the heading, the finished rows and the open slots; returns objects of the current row's slots."""
    chp, l1, l2 = heading()
    scene.add(l1, l2, rows_done(done))
    open_slots = {}
    for i in range(done, 3):
        s, c = slot(i), ctrl_slot(i)
        scene.add(s, c)
        open_slots[i] = (s, c)
    return open_slots


class S19Bg(SpokenScene):
    def construct(self):
        sl = rows_stage(self, 0, 0)
        self.at("rest of that")
        c = card(0, "genetic background")
        self.play(FadeOut(sl[0][0]), FadeIn(c), run_time=0.6)

        self.at("several donors")
        g, lb = row_orgs(0, 0)
        self.play(FadeOut(sl[0][1]), LaggedStart(*[FadeIn(o, scale=0.5) for o in g], lag_ratio=0.3), FadeIn(lb), run_time=0.7)

        self.at("help")
        self.play(FadeIn(stamp_at(0), scale=1.4), run_time=0.5)

        self.at("only moving")
        note = T("only moving the gene itself really tests this", 28, TEAL).move_to([0, -3.3, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S20Line(SpokenScene):
    def construct(self):
        sl = rows_stage(self, 1, 1)
        self.at("quirk")
        c = card(1, "a quirk of one line")
        self.play(FadeOut(sl[1][0]), FadeIn(c), run_time=0.6)

        self.at("several clones")
        g, lb = row_orgs(1, 1)
        self.play(FadeOut(sl[1][1]), LaggedStart(*[FadeIn(o, scale=0.5) for o in g], lag_ratio=0.25), FadeIn(lb), run_time=1.0)

        self.at("test that")
        self.play(FadeIn(stamp_at(1), scale=1.4), run_time=0.5)
        self.finish()


class S21Batch(SpokenScene):
    def construct(self):
        sl = rows_stage(self, 2, 2)
        self.at("bad batch")
        c = card(2, "a bad batch")
        self.play(FadeOut(sl[2][0]), FadeIn(c), run_time=0.6)

        self.at("patient and control")
        g, lb = row_orgs(2, 2)
        self.play(FadeOut(sl[2][1]), FadeIn(g[0], scale=0.5), FadeIn(g[1], scale=0.5), FadeIn(lb), run_time=0.9)

        self.at("more than once")
        self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in list(g)[2:]], lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(stamp_at(2), scale=1.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cell_legend():
    return VGroup(VGroup(glia(ORIGIN),T("radial glia",26,BLUE)).arrange(RIGHT,buff=0.2),
                  VGroup(neu(ORIGIN),T("neurons",26,GREEN)).arrange(RIGHT,buff=0.2)).arrange(RIGHT,buff=0.7)


def panel(center, w=5.6, h=3.8):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.1).move_to(center)


GRID = [np.array([cx, cy, 0]) for cy in (1.0, 0.0, -1.0) for cx in (-1.8, -0.6, 0.6, 1.8)]


class S22Back(SpokenScene):
    def construct(self):
        _,l1,l2=heading(); self.add(l1,l2,rows_done(3))
        self.at("move the gene")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.3)
        gene=chip("CDK5RAP2",PURPLE,32).move_to([0,3.05,0])
        self.play(FadeIn(gene),run_time=0.4)
        self.at("put back")
        A=np.array([-3.3,-0.5,0]); B=np.array([3.3,-0.5,0])
        ca=VGroup(*[glia(A+p) for p in GRID]); cb=VGroup(*[glia(B+p) for p in GRID])
        legends=cell_legend().move_to([0,2.25,0])
        la=VGroup(T("patient tissue",26,RED),T("+ control vector",26)).arrange(DOWN,buff=0.1).move_to([-3.3,-3,0])
        lb=VGroup(T("patient tissue",26,RED),T("+ CDK5RAP2",26,PURPLE)).arrange(DOWN,buff=0.1).move_to([3.3,-3,0])
        self.play(FadeIn(VGroup(panel(A,h=3.8),panel(B,h=3.8),ca,cb,legends,la,lb)),run_time=0.5)
        # Dots mark exactly the cells receiving the gene, including recipient neurons.
        tags=VGroup(*[dot(B+p,PURPLE,0.08,1,0) for p in GRID])
        self.play(FadeIn(tags),run_time=0.4)
        self.at("kept more")
        self.play(*[Transform(ca[i],neu(A+GRID[i])) for i in range(2,12)],
                  *[Transform(cb[i],neu(B+GRID[i])) for i in range(5,12)],run_time=0.65)
        self.add(T("illustrative: 2/12 vs 5/12 radial glia",26,GREY).move_to([0,1.65,0]),stamp([0,-3.15,0]))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S23Kd(SpokenScene):
    def construct(self):
        A=np.array([-3.3,-0.5,0]); B=np.array([3.3,-0.5,0])
        ca=VGroup(*[glia(A+p) for p in GRID]); cb=VGroup(*[glia(B+p) for p in GRID])
        self.add(panel(A,h=4.4),panel(B,h=4.4),ca,cb,cell_legend().move_to([0,2.9,0]), T("CDK5RAP2 knockdown",26,PURPLE).move_to([0,3.55,0]),
                 T("control tissue",28).move_to([-3.3,-3.15,0]),T("control tissue",28).move_to([3.3,-3.15,0]))
        self.at("two different")
        h1=hairpin().move_to([-4.5,2.45,0]); h2=hairpin(1.1,0.5).move_to([5,2.45,0])
        self.play(FadeIn(VGroup(h1,h2,T("hairpin 1",26,PURPLE).move_to([-3,2.1,0]),T("hairpin 2",26,PURPLE).move_to([3.6,2.1,0]))),run_time=0.4)
        self.at("it lets")
        self.play(h1.animate.move_to(A),h2.animate.move_to(B),run_time=0.35)
        self.at("shift toward",lead=0.35)
        self.play(FadeOut(h1),FadeOut(h2),*[Transform(ca[i],neu(A+GRID[i])) for i in [0,2,4,6,8,10]],
                  *[Transform(cb[i],neu(B+GRID[i])) for i in [1,3,5,7,9,11]],run_time=0.55)
        self.add(stamp([0,-3.15,0]))
        self.finish()


class S24Beat(NarratedScene):
    def construct(self):
        pic=VGroup(cell_legend().move_to([0,3.1,0]))
        for x in [-3.3,3.3]:
            C=np.array([x,-0.5,0]); pic.add(panel(C,h=4.4),T("control tissue",28).move_to([x,-3.15,0]))
            pic.add(*[(neu(C+p) if i%2 else glia(C+p)) for i,p in enumerate(GRID)])
        self.add(pic.fade(0.45)); self.finish()


# ---------------------------------------------------------------------------------------------
class S25Fair(SpokenScene):
    """a dividing progenitor with its CDK5RAP2 centrosome in teal (the bet); ticks for rescue and knockdown (the result)."""

    def construct(self):
        C = np.array([-3.7, -0.1, 0])
        cellb = Circle(radius=2.55, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.2).move_to(C)
        nuc = Circle(radius=0.8, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.35).move_to(C)
        self.add(cellb,nuc,lab("dividing progenitor",28,BLUE).move_to([-3.7,-3.2,0]))

        self.at("good bet")
        bet = T("the bet", 40, TEAL).move_to([-3.7, 2.95, 0])
        self.play(FadeIn(bet, shift=DOWN * 0.1), run_time=0.7)

        self.at("centrosome")
        top, bot = C + UP * 1.6, C + DOWN * 1.6
        spindle = VGroup(*[Line(top, C + np.array([dx, 0, 0]), stroke_color=GREY, stroke_width=2) for dx in (-0.5, 0, 0.5)],
                         *[Line(bot, C + np.array([dx, 0, 0]), stroke_color=GREY, stroke_width=2) for dx in (-0.5, 0, 0.5)])
        chrom = VGroup(*[dot(C + np.array([dx, 0, 0]), TEXT, 0.09, 1.0, 0) for dx in (-0.45, -0.15, 0.15, 0.45)])
        c1 = Circle(radius=0.25, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.9).move_to(top)
        c2 = Circle(radius=0.25, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.9).move_to(bot)
        cl = lab("centrosome", 28, TEXT).move_to([-0.2, 2.05, 0])
        ll = Line(cl.get_left() + LEFT * 0.05, top + RIGHT * 0.3, stroke_color=TEAL, stroke_width=2)
        self.play(FadeOut(nuc), FadeIn(spindle), FadeIn(chrom), FadeIn(c1, scale=0.3), FadeIn(c2, scale=0.3), run_time=1.0)
        self.play(FadeIn(cl), Create(ll), run_time=0.6)

        self.at("dividing progenitor")
        dl = lab("dividing progenitor", 28, BLUE).move_to([-3.7, -2.75, 0])
        self.play(chrom[:2].animate.shift(UP * 0.65), chrom[2:].animate.shift(DOWN * 0.65), run_time=0.7)

        self.at("rescue and")
        r1 = VGroup(tick(TEAL, 0.7), T("rescue: more radial glia",28,TEAL)).arrange(RIGHT, buff=0.35).move_to([3.6, 1.2, 0])
        self.play(Create(r1[0]), FadeIn(r1[1]), run_time=0.6)
        self.at("knockdown")
        r2 = VGroup(tick(TEAL, 0.7), VGroup(T("knockdown:",28,TEAL),T("shift to neurons",28,GREEN)).arrange(DOWN,buff=0.12)).arrange(RIGHT, buff=0.35).move_to([4.2, -0.1, 0])
        r2.align_to(r1, LEFT)
        r2[1].arrange(DOWN,aligned_edge=LEFT,buff=0.12)
        r2[1].next_to(r2[0],RIGHT,buff=0.35).align_to(r2[0],UP)
        self.play(Create(r2[0]), FadeIn(r2[1]), run_time=0.6)

        self.at("organoid tissue")
        ot = VGroup(lab("in organoid tissue", 28)).move_to([3.7, -1.4, 0])
        self.play(FadeIn(ot, shift=UP * 0.1), run_time=0.7)

        self.at("a result")
        res = T("the result", 40, TEAL).move_to([3.9, 2.75, 0])
        self.play(FadeIn(res, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S26Q(SpokenScene):
    """a normal-looking organoid; the amber vessels and microglia it lacks."""

    def construct(self):
        org = sph(LC,2.6)
        oc = dots(LC, 11, 2.2, GREY)
        ol = lab("looks normal", 30).move_to(LC + DOWN * 3.0)
        self.play(FadeIn(org), FadeIn(oc), FadeIn(ol), run_time=0.7)

        self.add(DashedVMobject(RoundedRectangle(width=5.0,height=5.8,corner_radius=0.2,color=AMBER).move_to([3.9,-0.1,0]),num_dashes=50),T("missing surroundings",26,AMBER).move_to([3.9,3.35,0]))
        self.at("blood vessels")
        vp = [CubicBezier([0.9, 1.0, 0], [2.4, 1.9, 0], [3.8, 0.1, 0], [6.0, 1.0, 0], stroke_color=AMBER, stroke_width=6),
              CubicBezier([2.0, 1.45, 0], [2.3, 2.0, 0], [2.7, 2.2, 0], [3.0, 2.55, 0], stroke_color=AMBER, stroke_width=4),
              CubicBezier([3.6, 0.75, 0], [3.7, 0.3, 0], [3.5, 0.0, 0], [3.6, -0.3, 0], stroke_color=AMBER, stroke_width=4),
              CubicBezier([4.7, 0.85, 0], [4.9, 1.5, 0], [5.3, 1.9, 0], [5.6, 2.5, 0], stroke_color=AMBER, stroke_width=4)]
        ves = VGroup(*[DashedVMobject(v.set_stroke(width=10), num_dashes=7, dashed_ratio=0.78) for v in vp]).scale(0.82).move_to([3.9,0.9,0])
        vl = lab("blood vessels", 26, AMBER).move_to([3.9, 2.25, 0])
        self.play(Create(ves), FadeIn(vl), run_time=1.0)

        self.at("or")
        mc = np.array([3.9, -1.25, 0])
        body = ghost(0.55, mc, AMBER).set_stroke(width=7)
        procs=VGroup()
        for angle,length in [(0.2,1.1),(1.6,0.8),(2.8,1.2),(4.2,0.9),(5.5,1.0)]:
            u=np.array([np.cos(angle),np.sin(angle),0]); v=np.array([-u[1],u[0],0])
            root=mc+u*0.4; fork=mc+u*0.8; tip=mc+u*length
            for line in [Line(root,tip),Line(fork,tip+v*0.32),Line(fork,tip-v*0.3)]:
                procs.add(DashedVMobject(line.set_stroke(AMBER,7),num_dashes=3,dashed_ratio=0.8))
        body.add(dot(mc,TEXT,0.12,0.6,0))
        mlb = lab("microglia", 26, AMBER).move_to([3.9, -2.65, 0])
        self.play(Create(body), Create(procs), FadeIn(mlb), run_time=1.0)

        self.at("normal")
        self.play(Indicate(org, color=GREY, scale_factor=1.04), run_time=0.8)

        self.at("would not clear it",lead=0.35)
        q = T("?", 120, AMBER, weight=BOLD).move_to([0.25, -0.2, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S27Take(SpokenScene):
    """closing rule card, teal and amber: start with the program; test hardest where the surroundings matter; measure every feature."""

    def construct(self):
        first = chip("a first guess", GREY, 28).move_to([0, 3.3, 0])
        self.at("Use the program")
        self.play(FadeIn(first, shift=DOWN * 0.1), run_time=0.5)
        b1 = RoundedRectangle(corner_radius=0.18, width=11.2, height=1.3, stroke_color=TEAL, stroke_width=4,
                              fill_color=TEAL, fill_opacity=0.14).move_to([0, 2.0, 0])
        t1 = T("1  Start with the program", 36, TEAL).move_to(b1)
        self.play(FadeIn(b1), FadeIn(t1), run_time=0.8)

        self.at("then test")
        b2 = RoundedRectangle(corner_radius=0.18, width=11.2, height=1.3, stroke_color=AMBER, stroke_width=4,
                              fill_color=AMBER, fill_opacity=0.14).move_to([0, 0.4, 0])
        t2 = T("2  Test hardest where the surroundings matter", 36, AMBER).move_to(b2)
        self.play(FadeIn(b2), FadeIn(t2), run_time=0.8)

        self.at("measure every")
        b3 = RoundedRectangle(corner_radius=0.18, width=11.2, height=1.3, stroke_color=TEXT, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.14).move_to([0, -1.2, 0])
        t3 = T("3  Measure every feature", 36).move_to(b3)
        self.play(FadeIn(b3), FadeIn(t3), run_time=0.8)

        self.at("the dish adds")
        t4 = T("the dish adds stress of its own", 32, RED).move_to([0, -2.85, 0])
        self.play(FadeIn(t4, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S28End(EndCard):
    LINE = "Start with the program, test hardest where surroundings matter, measure every feature."
    def construct(self):
        lines=VGroup(*[T(t,38,font=TITLE_FONT) for t in ["Start with the program,","test hardest where surroundings matter,","measure every feature."]]).arrange(DOWN,buff=0.25).move_to([0,0.7,0])
        caveat=T("A first guess, not a verdict",28,GREY).move_to([0,-1.5,0])
        url=T("biochemistrypedia.com",28,TEAL).move_to([0,-2.5,0])
        self.play(FadeIn(lines),FadeIn(caveat),FadeIn(url),run_time=0.5)
        self.finish()

