"""Where the Reader Works — protein-sorting explainer.

COLOR MAP
  GOLD/YELLOW = address or signal sequence
  TEAL        = SRP and SRP receptor
  BLUE        = readers that act after release (TOM, PEX5)
  INDIGO      = ER membrane, lumen, and Sec61
  ORANGE      = mitochondrion
  MAGENTA     = peroxisome
  PINK        = GTP
  RED         = cutting, blocked, or cannot enter
  GREY/WHITE  = structure, chain, and neutral labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

INDIGO = "#7779E8"
ORANGE = "#F29E4C"
MAGENTA = "#D96BB0"
PINK = "#F0A3C4"
GOLD = YELLOW
ER_Y = -2.15
RIBO_POS = np.array([-2.25, 0.9, 0.0])


def ambient(seed=1):
    """Visible cytosol specks with slow continuous drift."""
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(46):
        d = Dot([rng.uniform(-6.25, 6.25), rng.uniform(-3.35, 3.35), 0],
                radius=rng.uniform(0.08, 0.16), color=GREY)
        d.set_opacity(rng.uniform(0.25, 0.48))
        d.v = np.array([rng.uniform(-0.8, 0.8), rng.uniform(0.48, 0.88), 0])
        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.55: m.shift(DOWN * 7.0)
            if m.get_x() > 6.5: m.shift(LEFT * 13.0)
            if m.get_x() < -6.5: m.shift(RIGHT * 13.0)
        d.add_updater(drift)
        dots.add(d)
    dots.set_z_index(-20)
    return dots


def bead_chain(n=13, gold=4, r=0.14, vertical=False, gold_at_end=False):
    b = VGroup(*[Circle(radius=r, stroke_width=1.5, stroke_color=BG,
                        fill_color=TEXT, fill_opacity=1) for _ in range(n)])
    b.arrange(DOWN if vertical else RIGHT, buff=0.035)
    ids = range(n-gold, n) if gold_at_end else range(gold)
    for i in ids: b[i].set_fill(GOLD)
    return b


def ribosome(pos=RIBO_POS, scale=1.0, cutaway=False):
    big = Ellipse(width=3.15, height=2.15, stroke_color=GREY, stroke_width=4,
                  fill_color=GREY, fill_opacity=0.26)
    small = Ellipse(width=2.25, height=1.15, stroke_color=GREY, stroke_width=4,
                    fill_color=GREY, fill_opacity=0.32).shift(UP * 1.25 + LEFT * 0.25)
    tunnel = ArcBetweenPoints(np.array([-0.45, 1.2, 0]), np.array([0.72, -0.96, 0]),
                              angle=-0.55, color=BG, stroke_width=15)
    mouth = Dot([0.72, -0.96, 0], radius=0.13, color=BG)
    g = VGroup(big, small, tunnel, mouth).scale(scale).move_to(pos)
    if cutaway:
        big.set_fill(GREY, 0.12)
        tunnel.set_stroke(GOLD, width=10, opacity=0.5)
    return g


def er_world(opacity=1.0):
    lumen = Rectangle(width=13.4, height=1.55, stroke_width=0,
                      fill_color=INDIGO, fill_opacity=0.13 * opacity).move_to([0, -3.02, 0])
    membrane = VGroup(
        RoundedRectangle(width=7.0, height=.32, corner_radius=.12, stroke_color=INDIGO,
                         fill_color=INDIGO, fill_opacity=.45, stroke_width=3).move_to([-3.2, ER_Y, 0]),
        RoundedRectangle(width=4.55, height=.32, corner_radius=.12, stroke_color=INDIGO,
                         fill_color=INDIGO, fill_opacity=.45, stroke_width=3).move_to([4.02, ER_Y, 0]))
    sec = VGroup(*[RoundedRectangle(width=.35, height=.72, corner_radius=.1,
                                    stroke_color=INDIGO, fill_color=INDIGO, fill_opacity=.75,
                                    stroke_width=3).move_to([x, ER_Y, 0]) for x in (.55, 1.35)])
    lab = T("ER lumen", 28, INDIGO).move_to([-4.9, -3.05, 0])
    g = VGroup(lumen, membrane, sec, lab).set_opacity(opacity)
    return g


def mitochondrion(pos=(5.45, .15, 0), scale=1.0):
    outer = RoundedRectangle(width=3.0, height=3.55, corner_radius=.9, stroke_color=ORANGE,
                             stroke_width=4, fill_color=ORANGE, fill_opacity=.08)
    inner = RoundedRectangle(width=2.25, height=2.8, corner_radius=.65, stroke_color=ORANGE,
                             stroke_width=3, stroke_opacity=.65)
    return VGroup(outer, inner).scale(scale).move_to(pos)


def peroxisome(pos=(-5.65, 2.55, 0), scale=1.0):
    return Circle(radius=.7, stroke_color=MAGENTA, stroke_width=4,
                  fill_color=MAGENTA, fill_opacity=.1).scale(scale).move_to(pos)


def gel(scale=1.0, pos=(-4.9, 2.05, 0), labels=True):
    box = RoundedRectangle(width=3.1, height=2.35, corner_radius=.18,
                           stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=.9)
    lane1 = Rectangle(width=.72, height=1.52, stroke_color=GREY, stroke_width=1).move_to([-0.65, -.1, 0])
    lane2 = lane1.copy().move_to([.65, -.1, 0])
    hi = RoundedRectangle(width=.58, height=.18, corner_radius=.06, stroke_width=0,
                          fill_color=TEXT, fill_opacity=1).move_to([-.65, .28, 0])
    lo = hi.copy().move_to([.65, -.12, 0])
    bracket = BraceBetweenPoints(np.array([-.08, -.12, 0]), np.array([-.08, .28, 0]),
                                 direction=RIGHT, color=GOLD)
    q = T("?", 34, GOLD, weight=BOLD).next_to(bracket, RIGHT, buff=.06)
    parts = [box, lane1, lane2, hi, lo, bracket, q]
    if labels:
        a = T("test tube", 28, TEXT).move_to([-.65, .94, 0])
        b = T("cells", 28, TEXT).move_to([.65, .94, 0])
        parts += [a, b]
    return VGroup(*parts).scale(scale).move_to(pos)


def world(seed=2, er_opacity=1.0, labels=True):
    r = ribosome()
    e = er_world(er_opacity)
    m = mitochondrion()
    p = peroxisome()
    parts = [ambient(seed), e, m, p, r]
    if labels:
        parts += [T("exit tunnel", 28, TEXT).move_to([.45, .30, 0]),
                  T("schematic, not to scale", 22, TEXT).move_to([5.05, -3.48, 0])]
    return VGroup(*parts)


def reveal_chain(scene, chain, run_time=1.5):
    scene.play(LaggedStart(*[FadeIn(x, scale=.45) for x in chain], lag_ratio=.12), run_time=run_time)


def question_card():
    return T("Membranes added after release: does it get in?", 30, TEXT, weight=BOLD).move_to([.9, 3.25, 0])


def padlock():
    shackle = Arc(radius=.22, start_angle=0, angle=PI, color=RED, stroke_width=5)
    body = RoundedRectangle(width=.52, height=.42, corner_radius=.07, stroke_color=RED,
                            fill_color=RED, fill_opacity=.25, stroke_width=4).next_to(shackle, DOWN, buff=-.04)
    return VGroup(shackle, body)


def dark_chip(text, color, size=28):
    """Readable chip that masks any compartment line behind its label."""
    c = chip(text, color, size)
    c[0].set_fill(BG, opacity=.92)
    return c


class S00Hook(SpokenScene):
    def construct(self):
        self.add(ambient(0))
        g = gel(1.35, (-3.9, .35, 0))
        self.play(FadeIn(g[0]), FadeIn(VGroup(g[1], g[2], g[-2], g[-1])), run_time=.55)
        self.at("made in a test tube")
        self.play(GrowFromCenter(g[3]), run_time=.55)
        self.at("longer than")
        self.play(GrowFromCenter(g[4]), run_time=.55)
        self.at("extra piece")
        self.play(GrowFromCenter(g[5]), FadeIn(g[6], scale=.5), run_time=.65)
        self.at("why does the cell")
        inset = gel(.54, (-5.65, 2.55, 0), labels=False)
        self.play(FadeOut(VGroup(g[-2], g[-1])), Transform(g, inset), run_time=.7)
        w = world(3)
        self.play(LaggedStart(FadeIn(w[1], shift=UP*.25), FadeIn(w[2], shift=LEFT*.2),
                              FadeIn(w[3], shift=DOWN*.2), FadeIn(w[4], scale=.9),
                              FadeIn(VGroup(*w[5:])), lag_ratio=.12), run_time=1.15)
        ch = bead_chain(7, 3, r=.13, vertical=True).move_to([-.88, -1.0, 0])
        reveal_chain(self, ch, .75)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Protein sorting"
    TITLE = "Where the Reader Works"


class S02Address(SpokenScene):
    def construct(self):
        self.add(world(4), gel(.54, (-5.65, 2.55, 0), labels=False))
        ch = bead_chain(13, 4, r=.15, vertical=True).move_to([-.82, -.6, 0])
        reveal_chain(self, ch, 1.15)
        self.at("an address")
        addr = T("address", 32, GOLD, weight=BOLD).move_to([.55, -.72, 0])
        self.play(FadeIn(addr), Indicate(VGroup(*ch[:4]), color=GOLD), run_time=.7)
        self.at("own chain")
        targets = [np.array([0, -2.15, 0]), np.array([5.1, .2, 0]), np.array([-5.6, 2.5, 0])]
        arr = VGroup(*[DashedLine(ch[:4].get_center(), t, color=GOLD, stroke_opacity=.55) for t in targets])
        self.play(Create(arr), run_time=.4); self.play(FadeOut(arr), run_time=.25)
        self.at("signal sequence")
        sig = T("signal sequence", 28, GOLD).move_to([1.05, -1.28, 0])
        self.play(FadeIn(sig, shift=UP*.1), run_time=.45)
        self.at("amino terminal end")
        amino = T("amino end", 28, TEXT).move_to([.85, .95, 0])
        self.play(FadeIn(amino), ch[0].animate.scale(1.3), run_time=.45)
        self.at("hides the newest part")
        cut = ribosome(cutaway=True)
        hidden = bead_chain(5, 0, r=.12, vertical=True).move_to([-2.12, 1.0, 0]).set_opacity(.6)
        hidlab = T("still hidden", 28, GREY).move_to([-5.15, 1.45, 0])
        self.play(FadeIn(cut), FadeIn(hidden), FadeIn(hidlab), run_time=.8)
        self.at("emerges first")
        self.play(FadeOut(cut), FadeOut(hidden), FadeOut(hidlab), Indicate(VGroup(*ch[:4]), color=GOLD), run_time=.8)
        self.finish()


class S04Srp(SpokenScene):
    def construct(self):
        w = world(5); self.add(w)
        ch = bead_chain(9, 4, r=.15, vertical=True).move_to([-.82, -.5, 0])
        self.add(ch)
        srp = RoundedRectangle(width=1.6, height=.78, corner_radius=.2, stroke_color=TEAL,
                               fill_color=TEAL, fill_opacity=.35, stroke_width=4).move_to([.55, -.78, 0])
        self.play(FadeIn(srp, shift=RIGHT*.7), run_time=.7)
        self.at("SRP binds")
        sl = T("SRP", 30, TEAL, weight=BOLD).move_to(srp)
        self.play(FadeIn(sl), run_time=.45)
        self.at("reads the address")
        self.play(srp.animate.move_to([.2, -.7, 0]), sl.animate.move_to([.2, -.7, 0]), Indicate(VGroup(*ch[:4]), color=GOLD), run_time=.7)
        self.play(ch.animate.shift(DOWN*.18), rate_func=there_and_back, run_time=1.8)
        gauge = RoundedRectangle(width=2.2, height=.75, corner_radius=.15, stroke_color=GREY,
                                 stroke_width=2).move_to([2.4, 2.35, 0])
        fill = Rectangle(width=1.75, height=.3, stroke_width=0, fill_color=GREEN,
                         fill_opacity=.9).align_to(gauge, LEFT).shift(RIGHT*.18)
        gl = T("elongation, schematic", 28, TEXT).next_to(gauge, UP, buff=.14)
        self.at("translations slowed")
        self.play(FadeIn(gauge), FadeIn(gl), FadeIn(fill), run_time=.5)
        self.play(fill.animate.stretch_to_fit_width(.35).set_color(RED).align_to(gauge, LEFT).shift(RIGHT*.18), run_time=1.0)
        self.at("membranes arrived")
        moving = VGroup(ribosome(), ch, srp, sl)
        self.play(moving.animate.shift(DOWN*1.05 + RIGHT*2.65), FadeOut(w[4]), FadeOut(w[5]), run_time=1.25)
        self.finish()


class S05Hands(SpokenScene):
    def construct(self):
        w = world(6); w[4].set_opacity(0); w[5].set_opacity(0); self.add(w)
        r = ribosome(pos=(.4, -.15, 0), scale=.82)
        ch = bead_chain(7, 4, r=.13, vertical=True).move_to([1.58, -1.2, 0])
        srp = chip("SRP", TEAL, 28).move_to([.6, -1.25, 0])
        rec = dark_chip("SRP receptor", TEAL).move_to([-2.5, -1.95, 0])
        self.add(r, ch, srp, rec)
        self.at("docks on its receptor")
        self.play(srp.animate.next_to(rec, UP, buff=.08), run_time=.65)
        self.at("Sec61")
        sec = T("Sec61 channel", 28, INDIGO).move_to([2.3, -2.8, 0])
        self.play(FadeIn(sec), run_time=.45)
        self.at("two hands")
        h1 = ArcBetweenPoints([-1.25,-1.35,0],[-.25,-1.5,0],angle=-1.3,color=TEAL,stroke_width=12)
        h2 = ArcBetweenPoints([-.25,-1.5,0],[-1.2,-1.85,0],angle=-1.3,color=TEAL,stroke_width=12)
        self.play(ReplacementTransform(VGroup(srp,rec), VGroup(h1,h2)), run_time=.7)
        self.at("both hold GTP")
        discs = VGroup(*[VGroup(Circle(radius=.42, color=PINK, fill_color=PINK, fill_opacity=1),
                                     T("GTP", 24, BG, weight=BOLD)).move_to(p) for p in ((-.35,-1.15,0),(-1.05,-2.0,0))])
        self.play(FadeIn(discs, scale=.5), run_time=.55)
        self.at("hand the ribosome")
        self.play(VGroup(r,ch).animate.shift(RIGHT*1.0 + DOWN*.2), run_time=1.0)
        self.finish()


class S06Thread(SpokenScene):
    def construct(self):
        w = world(7); w[4].set_opacity(0); w[5].set_opacity(0); self.add(w)
        r = ribosome(pos=(1.4,-.3,0), scale=.78)
        chain = bead_chain(14,4,r=.13,vertical=True).move_to([1.35,-1.25,0])
        hands = VGroup(*[Arc(radius=.55,start_angle=a,angle=1.1,color=TEAL,stroke_width=10) for a in (0,PI)]).move_to([-.2,-1.45,0])
        discs = VGroup(*[Circle(radius=.22,color=PINK,fill_color=PINK,fill_opacity=1).move_to(p) for p in ((-.45,-1.3,0),(.1,-1.7,0))])
        self.add(r, chain, hands, discs)
        self.at("threading in")
        self.play(chain.animate.shift(DOWN*.9), run_time=.8)
        self.at("hydrolysis opens")
        used = T("GTP used", 28, TEXT).move_to([-.45,-2.75,0])
        self.play(hands.animate.scale(1.4).set_opacity(.35), discs.animate.scale(.3).set_color(GREY), FadeIn(used), run_time=.7)
        self.at("enters unfolded")
        self.play(chain.animate.shift(DOWN*.6), FadeOut(used), run_time=.8)
        self.at("Signal peptidase")
        scissors = T("✂", 50, RED).move_to([2.1,-2.55,0])
        pl = dark_chip("signal peptidase", RED).move_to([4.15,-2.65,0])
        self.play(FadeIn(scissors), FadeIn(pl), run_time=.55)
        self.at("snips off the address")
        self.play(VGroup(*chain[:4]).animate.shift(LEFT*1.1).set_opacity(0), Rotate(scissors,.4), run_time=.7)
        self.at("test tube kept")
        gi = gel(.8,(-4.8,1.95,0),labels=False)
        goldseg = Rectangle(width=.45,height=.16,stroke_width=0,fill_color=GOLD,fill_opacity=1).move_to([-5.3,2.2,0])
        self.play(FadeIn(gi), FadeIn(goldseg), run_time=.65)
        self.at("no membrane")
        self.play(er_world().animate.set_opacity(.3), scissors.animate.set_opacity(.3), run_time=.5)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        self.add(ambient(8), mitochondrion(), peroxisome(), ribosome(),
                 T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        self.at("Back to the test tube")
        gi = gel(.6,(-5.45,2.45,0),labels=False); self.play(FadeIn(gi), run_time=.5)
        chain = bead_chain(15,4,r=.15).move_to([.45,.05,0])
        self.at("chain is finished")
        reveal_chain(self,chain,1.0)
        self.at("and released")
        self.play(chain.animate.shift(DOWN*.45+RIGHT*.5), run_time=.55)
        self.at("Does the protein")
        er = er_world(); q = question_card()
        self.play(FadeIn(er,shift=UP*.4),FadeIn(q,shift=DOWN*.1),run_time=.7)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        self.add(ambient(9), mitochondrion(), peroxisome(), ribosome(), er_world(), question_card(),
                 gel(.6,(-5.45,2.45,0),labels=False), T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        chain=bead_chain(15,4,r=.15).move_to([.95,-.4,0])
        self.add(chain)
        self.play(chain.animate.shift(UP*.12+RIGHT*.1),rate_func=there_and_back,run_time=4.5)


class S10Reveal(SpokenScene):
    def construct(self):
        self.add(ambient(10), mitochondrion(), peroxisome(), ribosome(), er_world(),
                 T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        q=question_card(); chain=bead_chain(15,4,r=.15).move_to([.95,-.4,0]); self.add(q,chain)
        self.at("stays outside")
        self.play(FadeOut(q),chain.animate.shift(DOWN*.65),run_time=.55)
        self.play(chain.animate.shift(UP*.35),run_time=.35)
        tag=dark_chip("not inside",RED).move_to([2.25,.55,0]); self.play(FadeIn(tag),run_time=.4)
        self.at("no ribosome to steer")
        srp=dark_chip("SRP",TEAL).move_to([.0,.55,0]); tether=DashedLine(srp.get_left(),[-1.05,.2,0],color=TEAL)
        self.play(FadeIn(srp),Create(tether),run_time=.6)
        self.at("other routes")
        other=bead_chain(8,2,r=.11).move_to([-3.2,-1.3,0]); gap=T("other routes",28,INDIGO).move_to([-3.2,-2.85,0])
        self.play(FadeIn(other),FadeIn(gap),run_time=.45)
        self.play(other.animate.shift(DOWN*1.5),run_time=.8)
        self.play(FadeOut(other),FadeOut(gap),run_time=.35)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        self.add(world(11))
        self.at("here is the idea")
        line1=VGroup(T("WHERE:",34,TEXT,weight=BOLD),T("the address",34,GOLD,weight=BOLD)).arrange(RIGHT,buff=.18).move_to([2.6,3.1,0])
        self.play(Write(line1),run_time=.75)
        self.at("Where and how")
        line2=VGroup(T("WHEN:",34,TEXT,weight=BOLD),T("where its reader works",34,TEAL,weight=BOLD)).arrange(RIGHT,buff=.18).move_to([2.6,2.5,0])
        self.play(Write(line2),run_time=.8)
        self.at("as the chain grows")
        ch=bead_chain(7,3,r=.13,vertical=True).move_to([-.85,-.75,0]); srp=dark_chip("SRP",TEAL).move_to([.1,-.75,0])
        self.play(FadeIn(ch),FadeIn(srp),Indicate(srp,color=TEAL),run_time=.7)
        self.at("after release")
        tom=dark_chip("TOM",BLUE).move_to([4.35,.45,0]); pex=dark_chip("PEX5",BLUE).move_to([-4.35,1.65,0])
        self.play(FadeIn(tom),FadeIn(pex),Indicate(VGroup(tom,pex),color=BLUE),run_time=.8)
        self.play(VGroup(line1,line2).animate.scale(.62).move_to([3.85,2.85,0]),run_time=.65)
        self.finish()


class S12Mito(SpokenScene):
    def construct(self):
        w=world(12,er_opacity=.3); self.add(w)
        rules=VGroup(T("WHERE: address",28,GOLD),T("WHEN: reader location",28,TEAL)).arrange(DOWN,buff=.08).move_to([3.65,3.0,0]); self.add(rules)
        ch=bead_chain(15,4,r=.14,vertical=True).move_to([-.82,-.55,0])
        pluses=VGroup(*[T("+",20,GOLD,weight=BOLD).next_to(ch[i],RIGHT,buff=.08) for i in range(4)])
        ch.add(pluses)
        reveal_chain(self,ch,1.1)
        poslab=T("positive on one face",28,GOLD).move_to([1.55,1.25,0]); self.play(FadeIn(poslab),run_time=.45)
        self.play(ch.animate.shift(DOWN*.18), rate_func=there_and_back, run_time=1.2)
        self.at("import gate")
        tom=dark_chip("TOM",BLUE).move_to([4.15,.45,0]); self.play(FadeIn(tom),run_time=.5)
        self.at("released before")
        loose=ch.copy().arrange_in_grid(rows=3,buff=.04).move_to([2.5,.0,0])
        self.play(Transform(ch,loose),FadeOut(poslab),run_time=.7)
        self.play(ch.animate.move_to([2.5,.15,0]),run_time=.75)
        self.at("ribosome sitting")
        r2=ribosome(pos=(5.1,1.5,0),scale=.45); q=T("?",38,TEXT).next_to(r2,LEFT,buff=.1)
        self.play(FadeIn(r2),FadeIn(q),run_time=.55)
        self.at("Hold that question")
        self.play(FadeOut(r2),FadeOut(q),run_time=.5)
        self.finish()


def mito_close():
    outer=RoundedRectangle(width=5.1,height=6.2,corner_radius=1.0,stroke_color=ORANGE,stroke_width=5,fill_color=ORANGE,fill_opacity=.06).move_to([2.9,0,0])
    inner=RoundedRectangle(width=3.8,height=5.0,corner_radius=.8,stroke_color=ORANGE,stroke_width=4).move_to([3.25,0,0])
    tom=dark_chip("TOM",BLUE).move_to([.38,1.55,0])
    tim=dark_chip("TIM23 complex",ORANGE).move_to([1.35,-1.25,0])
    matrix=T("matrix",30,ORANGE).move_to([4.25,-2.0,0])
    return VGroup(outer,inner,tom,tim,matrix)


class S13Unfold(SpokenScene):
    def construct(self):
        mc=mito_close(); self.add(ambient(13),mc,T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        loose=bead_chain(16,4,r=.14).arrange_in_grid(rows=4,buff=.04).move_to([-3.6,.35,0])
        self.add(loose)
        self.at("chaperones")
        dots=VGroup(*[VGroup(Dot(radius=.14,color=GREY),T("C",15,BG,weight=BOLD)).move_to(p) for p in ((-4,.8,0),(-3.3,.1,0),(-3.8,-.3,0))])
        lab=T("chaperones",28,GREY).move_to([-3.55,-1.1,0]); self.play(FadeIn(dots),FadeIn(lab),run_time=.6)
        self.at("To cross Tom")
        self.play(loose.animate.move_to([-.95,.3,0]),FadeOut(dots),FadeOut(lab),run_time=.7)
        self.at("TIM23 complex")
        self.play(Indicate(mc[3],color=ORANGE),run_time=.5)
        self.at("partly unfolded")
        thread=bead_chain(16,4,r=.13).move_to([1.3,.0,0]).rotate(-.2)
        self.play(Transform(loose,thread),run_time=1.2)
        self.play(loose.animate.shift(RIGHT*1.65),run_time=.8)
        self.finish()


class S13bPull(SpokenScene):
    def construct(self):
        self.add(ambient(14),mito_close(),T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        thread=bead_chain(17,4,r=.13).move_to([1.55,.15,0]).rotate(-.2); self.add(thread)
        self.at("membrane potential")
        signs=VGroup(*[T("+",25,GOLD).move_to([.85,y,0]) for y in (-.5,.95,2.0)],
                     *[T("−",25,TEXT).move_to([1.7,y,0]) for y in (-.5,.95,2.0)])
        lab=T("membrane potential",28,TEXT).move_to([-2.8,2.5,0]); self.play(FadeIn(signs),FadeIn(lab),run_time=.55)
        self.at("pulls on")
        arrow=Arrow([-.6,.7,0],[2.0,.35,0],color=GOLD,stroke_width=6); self.play(GrowArrow(arrow),thread.animate.shift(RIGHT*.7),run_time=.7)
        self.at("HSB70")
        clamps=VGroup(dark_chip("Hsp70 (ATP)",GREY).move_to([3.0,-.6,0]),
                      dark_chip("Hsp70",GREY).move_to([4.3,-1.05,0]))
        self.play(FadeIn(clamps[0]),run_time=.5)
        self.play(thread.animate.shift(RIGHT*.65),ReplacementTransform(clamps[0],clamps[1]),run_time=.8)
        back=Arrow([3.0,-1.85,0],[2.15,-1.85,0],color=GREY); cross=T("×",40,RED).move_to(back)
        self.at("grip the chain")
        self.play(FadeIn(back),FadeIn(cross),Indicate(clamps[1],color=GREY),run_time=.55)
        self.finish()


class S14Mtx(SpokenScene):
    def construct(self):
        self.add(ambient(15),mito_close(),T("Eilers and Schatz, 1986",22,GREY).move_to([3.1,-3.4,0]))
        cargo=VGroup(bead_chain(4,4,r=.13),dark_chip("DHFR (mouse enzyme)",GREY)).arrange(RIGHT,buff=.12).move_to([-3.25,.95,0])
        self.at("mouse enzyme")
        self.play(FadeIn(cargo),run_time=.5)
        self.at("goes in too")
        thread=bead_chain(14,4,r=.12).move_to([1.5,1.0,0]); self.play(Transform(cargo,thread),run_time=.9); self.play(cargo.animate.shift(RIGHT*1.4),run_time=.6)
        self.at("methotrexate")
        locked=VGroup(bead_chain(4,4,r=.13),dark_chip("DHFR",GREY),padlock()).arrange(RIGHT,buff=.12).move_to([-3.0,-.55,0])
        drug=T("methotrexate (drug)",28,RED).move_to([-3.0,-1.5,0]); self.play(FadeIn(locked),FadeIn(drug),run_time=.55)
        self.at("import stops")
        self.play(locked.animate.move_to([-.6,-.1,0]),run_time=.65)
        blocked=dark_chip("complete import blocked",RED).move_to([-2.5,-2.55,0]); self.play(FadeIn(blocked),run_time=.45)
        control=bead_chain(10,3,r=.1).move_to([-2.4,2.25,0]); ctl=T("normal precursor: still enters",28,GREEN).move_to([-2.25,2.9,0])
        self.play(FadeIn(control),FadeIn(ctl),run_time=.35); self.play(control.animate.shift(RIGHT*2.0),run_time=.7)
        self.at("had to unfold")
        self.play(Indicate(locked,color=RED),run_time=.55)
        self.finish()


class S15Skl(SpokenScene):
    def construct(self):
        w=world(16,er_opacity=.3); self.add(w)
        rcut=ribosome(cutaway=True); self.add(rcut)
        chain=bead_chain(14,0,r=.14,vertical=True).move_to([-.82,-.55,0])
        hidden=bead_chain(3,3,r=.13,vertical=True,gold_at_end=True).move_to([-2.0,1.1,0]); self.add(hidden)
        self.at("last three amino acids")
        skl=T("SKL",30,GOLD,weight=BOLD).move_to([-4.55,1.45,0]); self.play(FadeIn(skl),run_time=.5)
        self.at("leave the tunnel")
        self.play(FadeOut(w[5]),run_time=.3)
        reveal_chain(self,chain,1.0)
        self.at("chain is released")
        gold=bead_chain(3,3,r=.14,vertical=True).next_to(chain,UP,buff=.03)
        self.play(FadeIn(gold),FadeOut(hidden),FadeOut(skl),VGroup(chain,gold).animate.shift(RIGHT*.9+DOWN*.25),run_time=.75)
        self.at("read afterwards")
        flash=Circle(radius=.38,color=GOLD,stroke_width=4).move_to([-1.55,-.2,0]); self.play(Create(flash),FadeOut(flash),run_time=.65)
        self.finish()


class S16Pex5(SpokenScene):
    def construct(self):
        self.add(ambient(17),er_world(.3),mitochondrion(),T("schematic, not to scale",22,TEXT).move_to([5.05,-3.48,0]))
        p=peroxisome(pos=(-4.7,.6,0),scale=1.75); self.add(p)
        ball=VGroup(*bead_chain(15,0,r=.13)).arrange_in_grid(rows=4,buff=.02).move_to([.8,.2,0])
        skl=VGroup(*bead_chain(3,3,r=.13)).arrange(RIGHT,buff=.02).next_to(ball,RIGHT,buff=.02); self.add(ball,skl)
        self.at("PEX 5")
        pex=chip("PEX5",BLUE,28).move_to([2.65,.35,0]); self.play(FadeIn(pex),run_time=.5)
        self.at("carries")
        self.play(pex.animate.next_to(skl,RIGHT,buff=.05),run_time=.4)
        self.at("finished protein")
        self.play(VGroup(ball,skl,pex).animate.move_to([-3.0,.55,0]),run_time=.7)
        self.at("stays folded")
        tick=T("✓  can stay folded",30,GREEN,weight=BOLD).move_to([1.8,-1.2,0]); self.play(FadeIn(tick),run_time=.5)
        self.at("still debated")
        debate=dark_chip("crossing: debated, not settled",MAGENTA).move_to([-3.75,-1.35,0]); blur=Circle(radius=.55,color=MAGENTA,fill_color=MAGENTA,fill_opacity=.18).move_to([-3.6,.55,0])
        self.play(FadeOut(pex),FadeIn(blur),FadeIn(debate),run_time=.55)
        self.play(VGroup(ball,skl).animate.move_to([-4.7,.55,0]),run_time=.8)
        self.finish()


class S17Return(SpokenScene):
    def construct(self):
        self.add(world(18),gel(.5,(-5.75,2.65,0),labels=False))
        rules=VGroup(T("WHERE: the address",28,GOLD,weight=BOLD),T("WHEN: where its reader works",28,TEAL,weight=BOLD)).arrange(DOWN,buff=.08).move_to([2.9,2.85,0]); self.add(rules)
        self.at("address points the way")
        self.play(Indicate(rules,color=GOLD),run_time=.6)
        ermini=VGroup(bead_chain(7,3,r=.09),dark_chip("SRP",TEAL)).arrange(DOWN,buff=.08).move_to([-3.45,-.55,0])
        self.at("SRP meets growing chains")
        self.play(FadeIn(ermini),ermini.animate.shift(DOWN*.7),run_time=.7)
        mito=bead_chain(10,3,r=.08).arrange_in_grid(rows=2,buff=.02).move_to([2.8,.3,0])
        self.at("finished ones")
        self.play(FadeIn(mito),mito.animate.move_to([4.2,.3,0]),run_time=.7)
        pball=VGroup(*bead_chain(11,0,r=.08)).arrange_in_grid(rows=3,buff=.01).move_to([-5.15,1.1,0]); pex=dark_chip("PEX5",BLUE).next_to(pball,RIGHT,buff=.08)
        self.play(FadeIn(pball),FadeIn(pex),VGroup(pball,pex).animate.move_to([-5.25,1.45,0]),run_time=.7)
        self.at("Mitochondria need")
        self.play(Transform(mito,bead_chain(10,3,r=.08).move_to([4.2,.3,0])),run_time=.6)
        self.at("take them folded")
        chlor=VGroup(T("chloroplasts:",28,GREEN),T("mostly like mitochondria",28,GREEN)).arrange(DOWN,buff=.06).move_to([1.7,-.85,0]); self.play(FadeIn(chlor),Indicate(pball,color=GREEN),run_time=.7)
        self.finish()


class S18End(EndCard):
    LINE = "An exposed address guides where; its machinery helps shape when."
