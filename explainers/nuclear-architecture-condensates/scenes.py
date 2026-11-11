"""Bigger or Brighter? — a single carried-world explainer.

COLOR MAP
  BLUE   protein molecules
  TEAL   droplets / dense phase
  ORANGE binding sites / parking spaces
  YELLOW saturation concentration
  PURPLE DNA / chromatin
  GREY   nuclei, dials, gauges, axes
  TEXT   words and neutral marks
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LEFT_C = np.array([-3.35, 0.15, 0.0])
RIGHT_C = np.array([3.35, 0.15, 0.0])
NUC_R = 2.35


def nucleus(c, r=NUC_R):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4,
                  fill_color=GREY, fill_opacity=0.22).move_to(c)


def glow(p, r=.34, opacity=.30):
    return VGroup(
        Circle(radius=r * 1.65, stroke_width=0, fill_color=BLUE, fill_opacity=opacity * .18).move_to(p),
        Circle(radius=r * 1.15, stroke_width=0, fill_color=TEXT, fill_opacity=opacity * .22).move_to(p),
        Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=opacity).move_to(p),
    )


SPOT_OFFSETS = [(-.95, .9), (.65, 1.05), (0, .15), (-1.05, -.75), (.9, -.72)]


def glows(c, scale=1.0):
    return VGroup(*[glow(c + np.array([x, y, 0]) * scale, .30 * scale)
                    for x, y in SPOT_OFFSETS])


def protein_field(c, n=36, seed=1, radius=NUC_R):
    """Deterministic drifting protein field, wrapped inside its nucleus."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        a = rng.uniform(0, TAU)
        rr = np.sqrt(rng.uniform(.04, (radius - .18) ** 2))
        d = Dot(c + [rr * np.cos(a), rr * np.sin(a), 0], radius=.065, color=BLUE)
        d.set_opacity(.62)
        d.velocity = np.array([rng.uniform(-.32, .32), rng.uniform(-.28, .28), 0])

        def drift(m, dt, centre=c.copy(), lim=radius - .15):
            m.shift(m.velocity * dt)
            delta = m.get_center() - centre
            if np.linalg.norm(delta[:2]) > lim:
                m.shift(-2 * m.velocity * dt)
                m.velocity *= -1
        d.add_updater(drift)
        dots.add(d)
    return dots


def base_world(with_glows=True, labels=True, scale=1.0, y_shift=0):
    lc = LEFT_C * scale + UP * y_shift
    rc = RIGHT_C * scale + UP * y_shift
    r = NUC_R * scale
    outlines = VGroup(nucleus(lc, r), nucleus(rc, r))
    dots = VGroup(protein_field(lc, 36, 11, r), protein_field(rc, 36, 17, r))
    gs = VGroup(glows(lc, scale), glows(rc, scale)) if with_glows else VGroup()
    labs = VGroup()
    if labels:
        labs = VGroup(T("droplets", 28, TEAL), T("binding sites", 28, ORANGE))
        labs[0].move_to(lc + UP * (r + .32))
        labs[1].move_to(rc + UP * (r + .32))
    schematic = T("schematic", 28, GREY).move_to([-5.65, 3.42, 0])
    return outlines, dots, gs, labs, schematic


def droplet_set(c=LEFT_C, radii=(.30, .30, .30, .30, .30), scale=1.0):
    ds = VGroup()
    for (x, y), r in zip(SPOT_OFFSETS, radii):
        p = c + np.array([x, y, 0]) * scale
        disc = Circle(radius=r * scale, stroke_color=TEAL, stroke_width=3,
                      fill_color=TEAL, fill_opacity=.52).move_to(p)
        ds.add(disc)
    return ds


def site_cluster(p, occupancy=2, scale=1.0):
    bars = VGroup(*[RoundedRectangle(width=.13 * scale, height=.42 * scale,
                                     corner_radius=.04, stroke_color=ORANGE,
                                     stroke_width=2, fill_color=ORANGE, fill_opacity=.28)
                    for _ in range(4)]).arrange(RIGHT, buff=.045 * scale).move_to(p)
    parked = VGroup(*[Dot(bars[i].get_center(), radius=.055 * scale, color=BLUE)
                      for i in range(min(occupancy, 4))])
    return VGroup(bars, parked)


def site_set(c=RIGHT_C, occupancy=2, scale=1.0):
    return VGroup(*[site_cluster(c + np.array([x, y, 0]) * scale, occupancy, scale)
                    for x, y in SPOT_OFFSETS])


def dna_under_sites(c=RIGHT_C):
    strands = VGroup()
    for x, y in SPOT_OFFSETS:
        p = c + [x, y, 0]
        pts = [p + [-.42, -.10, 0], p + [-.2, .08, 0], p + [0, -.06, 0],
               p + [.2, .08, 0], p + [.42, -.10, 0]]
        line = VMobject(stroke_color=PURPLE, stroke_width=3).set_points_smoothly(pts)
        strands.add(line)
    return strands


def dial(value=.30):
    centre = np.array([0, 2.65, 0])
    arc = Arc(radius=.72, start_angle=PI, angle=-PI, color=GREY, stroke_width=5).move_to(centre)
    ticks = VGroup(*[Line(centre + [(.62) * np.cos(PI-a), (.62) * np.sin(PI-a), 0],
                              centre + [(.76) * np.cos(PI-a), (.76) * np.sin(PI-a), 0],
                              color=GREY, stroke_width=3) for a in np.linspace(0, PI, 7)])
    angle = PI - value * PI
    needle = Line(centre, centre + [.58*np.cos(angle), .58*np.sin(angle), 0],
                  color=TEXT, stroke_width=5)
    hub = Dot(centre, radius=.08, color=TEXT)
    label = T("total protein", 28).next_to(arc, UP, buff=.12)
    return VGroup(arc, ticks, needle, hub, label)


def gauge(x, level=.28, width=3.7):
    box = RoundedRectangle(width=width, height=.48, corner_radius=.12,
                           stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.07)
    box.move_to([x, -2.48, 0])
    fill = Rectangle(width=max(.04, (width-.16)*level), height=.30, stroke_width=0,
                     fill_color=BLUE, fill_opacity=.28)
    fill.move_to(box.get_left() + RIGHT * (.08 + fill.width/2))
    needle = Line(DOWN*.28, UP*.28, color=TEXT, stroke_width=5)
    needle.move_to(box.get_left() + RIGHT * (.08 + (width-.16)*level))
    lab = T("outside", 28).next_to(box, DOWN, buff=.12)
    return VGroup(box, fill, needle, lab)


def question_card():
    text = T("Double it. What do the gauges do?", 31, weight=BOLD)
    box = RoundedRectangle(width=text.width + .5, height=text.height + .34,
                           corner_radius=.14, stroke_color=TEXT, stroke_width=2,
                           fill_color=BG, fill_opacity=.92)
    return VGroup(box, text).move_to([0, 3.18, 0])


def side_labels():
    return VGroup(T("bigger, not brighter", 28, TEAL).move_to([-3.35, -3.55, 0]),
                  T("brighter, not bigger", 28, ORANGE).move_to([3.35, -3.55, 0]))


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Nuclear architecture and condensates"
    TITLE = "Bigger or Brighter?"

    def construct(self):
        outlines, dots, gs, _, schematic = base_world(labels=False)
        seen = T("what the microscope sees", 30).move_to([0, 3.2, 0])
        q = T("?", 62, weight=BOLD).move_to([0, .15, 0])
        self.play(Create(outlines), FadeIn(dots), FadeIn(gs), FadeIn(seen),
                  FadeIn(q), FadeIn(schematic), run_time=.9)
        self.at("droplet of that protein")
        left_drops = droplet_set()
        left_lab = T("droplets", 28, TEAL).move_to(LEFT_C + UP * 2.67)
        self.play(FadeOut(gs[0]), FadeIn(left_drops), FadeIn(left_lab), run_time=.8)
        self.at("cluster of binding sites")
        sites = site_set()
        right_lab = T("binding sites", 28, ORANGE).move_to(RIGHT_C + UP * 2.67)
        self.play(FadeOut(gs[1]), FadeIn(sites), FadeIn(right_lab), run_time=.8)
        self.at("many copies")
        dna = dna_under_sites()
        self.play(Create(dna), run_time=.7)
        self.at("look alike")
        self.play(FadeOut(left_drops), FadeOut(sites), FadeOut(dna), FadeIn(gs), run_time=.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        outlines, dots, gs, labs, schematic = base_world()
        title = T("Bigger or Brighter?", 52, font=TITLE_FONT)
        shade = Rectangle(width=10.8, height=1.25, stroke_width=0,
                          fill_color=BG, fill_opacity=.82).move_to([0, 2.7, 0])
        self.add(outlines, dots, gs, labs, schematic)
        self.play(FadeIn(shade), Write(title), run_time=.7)
        self.play(gs.animate.set_opacity(.72), rate_func=there_and_back, run_time=.9)
        self.finish()


class S02Bodies(SpokenScene):
    def construct(self):
        outlines, dots, gs, labs, schematic = base_world()
        self.add(outlines, dots, gs, labs, schematic)
        self.at("no membrane")
        dashed = VGroup(*[DashedVMobject(Circle(.48, color=GREY).move_to(c + [-.95,.9,0]), 22)
                          for c in (LEFT_C, RIGHT_C)])
        self.play(Create(dashed), run_time=.55)
        self.play(FadeOut(dashed), run_time=.5)
        self.at("the nucleolus")
        nucs = VGroup(*[Ellipse(width=1.45, height=1.15, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=.25).move_to(c + [0,-.95,0])
                        for c in (LEFT_C, RIGHT_C)])
        nl = T("nucleolus", 30).move_to([0, -.85, 0])
        leaders = VGroup(Line(nl.get_left() + LEFT * .12,
                              nucs[0].get_right() + RIGHT * .12, color=GREY),
                         Line(nl.get_right() + RIGHT * .12,
                              nucs[1].get_left() + LEFT * .12, color=GREY))
        self.play(FadeIn(nucs), FadeIn(nl), Create(leaders), run_time=.75)
        self.at("builds ribosomal subunits")
        sub = chip("ribosomal subunit", TEXT, 28).move_to(LEFT_C + [0, -2.78, 0])
        self.play(FadeIn(sub, shift=UP * .25), run_time=.8)
        self.at("weak sticky patches")
        self.play(FadeOut(nl), FadeOut(leaders), FadeOut(sub), run_time=.3)
        mag = Circle(1.55, stroke_color=TEXT, stroke_width=3, fill_color=BG,
                     fill_opacity=.94).move_to([0,.1,0])
        core = RoundedRectangle(width=1.25, height=.8, corner_radius=.35,
                                stroke_color=BLUE, fill_color=BLUE, fill_opacity=.5).move_to(mag)
        patches = VGroup(*[Dot(core.get_center()+v, radius=.085, color=TEXT)
                           for v in ([0,.4,0],[0,-.4,0],[-.62,0,0],[.62,0,0])])
        neigh = VGroup(*[RoundedRectangle(width=.7,height=.5,corner_radius=.22,
                                          stroke_color=BLUE,fill_color=BLUE,fill_opacity=.38).move_to(core.get_center()+v)
                         for v in ([0,1.02,0],[-1.02,0,0],[1.02,0,0])])
        links = VGroup(Line(patches[0], neigh[0].get_bottom(), color=TEXT, stroke_width=3),
                       Line(patches[2], neigh[1].get_right(), color=TEXT, stroke_width=3),
                       Line(patches[3], neigh[2].get_left(), color=TEXT, stroke_width=3))
        patch_lab = T("weak sticky patches", 28).next_to(mag, DOWN, buff=.15)
        self.play(GrowFromCenter(mag), FadeIn(core), FadeIn(patches), FadeIn(neigh),
                  Create(links), FadeIn(patch_lab), run_time=1.0)
        self.at("That is multivalency")
        multi = T("multivalency", 34, TEAL, weight=BOLD).move_to([0,-2.05,0])
        self.play(FadeIn(multi), links.animate.set_opacity(.3), run_time=.4)
        self.play(links.animate.set_opacity(1), neigh.animate.rotate(.12), run_time=.65)
        self.play(FadeOut(VGroup(mag,core,patches,neigh,links,patch_lab,multi)), run_time=.5)
        self.finish()


class S03Checks(SpokenScene):
    def construct(self):
        outlines, dots, gs, labs, schematic = base_world()
        self.add(outlines, dots, gs, labs, schematic)
        checks = VGroup(T("round",28), T("merge?",28), T("refills",28)).arrange(RIGHT,buff=1.1).move_to([0,-3.2,0])
        self.play(FadeIn(checks), run_time=.6)
        self.at("look round")
        ticks = VGroup(T("✓",30,GREEN).next_to(checks[0],DOWN,.08),
                       T("✓",30,GREEN).next_to(checks[0],DOWN,.08).shift(RIGHT*.45))
        self.play(gs.animate.scale(1.06), FadeIn(ticks), run_time=.6)
        self.at("Droplets fuse")
        target = glow(LEFT_C + [0,.15,0], .42)
        self.play(gs[0][0].animate.move_to(LEFT_C+[-.18,.2,0]),
                  gs[0][1].animate.move_to(LEFT_C+[.18,.2,0]), run_time=.55)
        self.play(FadeOut(VGroup(gs[0][0],gs[0][1])), FadeIn(target), run_time=.55)
        self.at("drift together")
        self.play(gs[1][0].animate.move_to(RIGHT_C+[-.18,.2,0]),
                  gs[1][1].animate.move_to(RIGHT_C+[.18,.2,0]), run_time=.7)
        cut = VGroup(site_cluster([-.23,0,0],2), site_cluster([.23,0,0],2)).scale(.75)
        bubble = Circle(.68, color=TEXT, fill_color=BG, fill_opacity=.95)
        cut.move_to(bubble)
        bubble.move_to(RIGHT_C+[-1.45,-1.3,0]); cut.move_to(bubble)
        mticks = VGroup(T("✓",30,GREEN).next_to(checks[1],DOWN,.08).shift(LEFT*.2),
                        T("✓?",30,YELLOW).next_to(checks[1],DOWN,.08).shift(RIGHT*.35))
        self.play(FadeIn(bubble), FadeIn(cut), FadeIn(mticks), run_time=.55)
        self.at("Bleach one")
        flash = VGroup(*[Circle(.5, stroke_color=TEXT, stroke_width=7).move_to(c+[0,.15,0]) for c in (LEFT_C,RIGHT_C)])
        dark = VGroup(*[Circle(.36, stroke_width=0, fill_color=BG, fill_opacity=.95).move_to(c+[0,.15,0]) for c in (LEFT_C,RIGHT_C)])
        self.play(FadeIn(flash), FadeIn(dark), run_time=.25)
        self.play(FadeOut(flash), run_time=.25)
        self.at("glows again")
        self.play(dark[0].animate.set_opacity(0), run_time=1.1)
        self.play(dark[1].animate.set_opacity(0), run_time=1.7)
        refill_ticks = VGroup(T("✓",30,GREEN).next_to(checks[2],DOWN,.08).shift(LEFT*.2),
                              T("✓",30,GREEN).next_to(checks[2],DOWN,.08).shift(RIGHT*.25))
        self.play(FadeIn(refill_ticks), run_time=.3)
        self.at("concentrated there")
        result = T("concentrated, but how?", 38, weight=BOLD).move_to([0,-3.05,0])
        self.play(FadeOut(VGroup(checks,ticks,mticks,refill_ticks,bubble,cut)), FadeIn(result), run_time=.7)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        outlines, dots, gs, labs, schematic = base_world()
        self.add(outlines,dots,gs,labs,schematic)
        self.at("Give both nuclei one dial")
        d = dial(.30)
        self.play(FadeIn(d), run_time=.8)
        self.at("Add a gauge")
        gauges = VGroup(gauge(-3.35,.28), gauge(3.35,.28))
        self.play(FadeIn(gauges[0]), run_time=.5)
        self.play(FadeIn(gauges[1]), run_time=.5)
        self.at("double the protein")
        ghost = dial(.60)[2].set_opacity(.35)
        self.play(FadeIn(ghost), run_time=.6)
        self.at("What will each outside gauge do")
        q = question_card()
        self.play(FadeOut(d), FadeOut(labs), FadeIn(q), run_time=.65)
        self.finish()


class S05Think(NarratedScene):
    def construct(self):
        outlines,dots,gs,_,schematic=base_world(labels=False)
        gauges=VGroup(gauge(-3.35,.28),gauge(3.35,.28)); q=question_card()
        self.add(outlines,dots,gs,schematic,gauges,q)
        self.play(gs.animate.set_opacity(.78), gauges.animate.set_opacity(.85),
                  rate_func=there_and_back, run_time=2.0)
        self.finish()


class S06Droplets(SpokenScene):
    def construct(self):
        outlines,dots,gs,labs,schematic=base_world()
        d=dial(.30); gauges=VGroup(gauge(-3.35,.28),gauge(3.35,.28)); q=question_card()
        self.add(outlines,dots,gs,schematic,gauges,q)
        self.play(FadeOut(q), FadeIn(labs), FadeIn(d),
                  gauges[1].animate.set_opacity(.35), gs[1].animate.set_opacity(.35), run_time=.5)
        self.at("needle holds still")
        sat = T("saturation", 28, YELLOW).next_to(gauges[0][0], UP, buff=.10)
        tick = Line(DOWN*.28,UP*.28,color=YELLOW,stroke_width=6).move_to(gauges[0][2])
        self.play(FadeIn(tick), FadeIn(sat), run_time=.5)
        self.at("salt water")
        world = VGroup(outlines,dots,gs,labs,schematic,d,gauges,tick,sat)
        beaker=VGroup(Line([-1.55,1.2,0],[-1.55,-1.25,0],color=GREY,stroke_width=5),
                      Line([-1.55,-1.25,0],[1.55,-1.25,0],color=GREY,stroke_width=5),
                      Line([1.55,-1.25,0],[1.55,1.2,0],color=GREY,stroke_width=5))
        water=Rectangle(width=2.9,height=1.35,stroke_width=0,fill_color=BLUE,
                        fill_opacity=.18).move_to([0,-.52,0])
        grains=VGroup(*[Dot([-1.0+.5*i,1.55+.15*(i%2),0],radius=.09,color=TEXT)
                        for i in range(5)])
        pile=Polygon([-1.2,-1.2,0],[0,-.05,0],[1.2,-1.2,0],
                     fill_color=TEXT,fill_opacity=.55,stroke_width=0)
        blab=T("saturated salt water",30).move_to([0,2.35,0])
        self.play(FadeOut(world),FadeIn(beaker),FadeIn(water),FadeIn(grains),FadeIn(blab),run_time=.6)
        self.at("forms a second phase")
        self.play(grains.animate.shift(DOWN*2.35), GrowFromCenter(pile), run_time=1.2)
        self.at("At equilibrium")
        self.play(FadeOut(VGroup(beaker,water,grains,pile,blab)),FadeIn(world),run_time=.55)
        self.at("saturation concentration")
        fullsat=T("saturation concentration",28,YELLOW).move_to([-3.35,-1.92,0])
        self.play(Transform(sat,fullsat),run_time=.5)
        self.at("The extra builds")
        old=droplet_set(); new=droplet_set(radii=(.50,.47,.48,.46,.49))
        self.play(FadeOut(gs[0]),FadeIn(old),Transform(old,new),
                  Transform(d[2],dial(.60)[2]),run_time=1.8)
        self.at("denser phase")
        dense=T("dense phase",30,TEAL).move_to([0,.15,0])
        self.play(FadeIn(dense),run_time=.4)
        self.at("take up more room")
        self.play(FadeOut(dense),old.animate.scale(1.04),rate_func=there_and_back,run_time=.8)
        self.at("Bigger not brighter")
        lab=side_labels()[0]
        self.play(FadeIn(lab),run_time=.55)
        self.finish()


class S07Sites(SpokenScene):
    def construct(self):
        outlines,dots,_,labs,schematic=base_world(with_glows=False)
        drops=droplet_set(radii=(.50,.47,.48,.46,.49)).set_opacity(.38)
        sites=site_set(occupancy=1)
        d=dial(.30); gauges=VGroup(gauge(-3.35,.28),gauge(3.35,.28))
        leftlab=side_labels()[0]
        self.add(outlines,dots,drops,sites,labs,schematic,d,gauges,leftlab)
        self.play(drops.animate.set_opacity(.25),gauges[0].animate.set_opacity(.4),run_time=.35)
        self.at("needle climbs")
        high=gauge(3.35,.72)
        self.play(Transform(gauges[1],high),Transform(d[2],dial(.60)[2]),run_time=1.25)
        self.at("parking spaces")
        lot=RoundedRectangle(width=2.35,height=1.35,corner_radius=.12,stroke_color=GREY,
                             fill_color=BG,fill_opacity=.94).move_to([5.1,1.55,0])
        spaces=VGroup(*[Rectangle(width=.42,height=.48,stroke_color=ORANGE,stroke_width=2)
                        for _ in range(8)]).arrange_in_grid(2,4,buff=.1).move_to(lot)
        cars=VGroup(*[RoundedRectangle(width=.27,height=.18,corner_radius=.06,
                                       stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to(spaces[i]) for i in range(3)])
        plab=T("parking spaces",28).next_to(lot,UP,.10)
        self.play(FadeOut(labs[1]),FadeIn(lot),Create(spaces),FadeIn(cars),FadeIn(plab),run_time=.8)
        self.at("plenty still free")
        self.play(cars.animate.shift(RIGHT*.05),rate_func=there_and_back,run_time=.7)
        self.at("Some protein is parked")
        morecars=VGroup(*[RoundedRectangle(width=.27,height=.18,corner_radius=.06,
                                           stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to(spaces[i]) for i in range(3,6)])
        self.play(FadeIn(morecars,shift=LEFT*.25),run_time=.7)
        self.at("outside rises")
        road=Arrow([4.0,.55,0],[6.15,.55,0],buff=0,color=BLUE,stroke_width=4)
        car=RoundedRectangle(width=.3,height=.19,corner_radius=.06,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to(road.get_start())
        self.play(GrowArrow(road),car.animate.move_to(road.get_end()),run_time=1.0)
        self.at("spots fill in")
        filled=site_set(occupancy=4)
        self.play(Transform(sites,filled),run_time=1.1)
        self.at("grow no bigger")
        rings=VGroup(*[SurroundingRectangle(x,buff=.05,color=ORANGE,stroke_width=2) for x in sites])
        self.play(Create(rings),run_time=.45)
        self.at("Brighter not bigger")
        rlab=side_labels()[1]
        self.play(FadeOut(rings),FadeOut(VGroup(lot,spaces,cars,morecars,plab,road,car)),
                  FadeIn(labs[1]),FadeIn(rlab),run_time=.6)
        self.finish()


class S08Hold(NarratedScene):
    def construct(self):
        outlines,dots,_,labs,schematic=base_world(with_glows=False)
        drops=droplet_set(radii=(.50,.47,.48,.46,.49)); sites=site_set(occupancy=4)
        gauges=VGroup(gauge(-3.35,.28),gauge(3.35,.72)); labels=side_labels()
        tick=Line(DOWN*.28,UP*.28,color=YELLOW,stroke_width=6).move_to(gauges[0][2])
        self.add(outlines,dots,drops,sites,labs,schematic,gauges,labels,tick)
        self.play(drops.animate.set_fill(opacity=.65),rate_func=there_and_back,run_time=2.2)
        self.finish()


def small_world():
    scale=.62; shift=1.35
    lc=LEFT_C*scale+UP*shift; rc=RIGHT_C*scale+UP*shift; r=NUC_R*scale
    outlines=VGroup(nucleus(lc,r),nucleus(rc,r))
    dots=VGroup(protein_field(lc,36,11,r),protein_field(rc,36,17,r))
    drops=droplet_set(lc,(.45,.42,.44,.41,.43),scale)
    sites=site_set(rc,4,scale)
    labs=VGroup(T("droplets",28,TEAL).move_to(lc+UP*(r+.26)),
                T("binding sites",28,ORANGE).move_to(rc+UP*(r+.26)))
    return lc,rc,outlines,dots,drops,sites,labs


def graph_axes(cx):
    o=np.array([cx-2.3,-2.75,0]); w=4.6; h=2.2
    panel=RoundedRectangle(width=5.55,height=7.0,corner_radius=.18,stroke_color=GREY,
                           stroke_width=2,fill_color=GREY,fill_opacity=.10).move_to([cx,.05,0])
    axes=VGroup(panel,Line(o,o+RIGHT*w,color=GREY,stroke_width=3),Line(o,o+UP*h,color=GREY,stroke_width=3),
                T("total protein",28).move_to(o+[w/2,-.40,0]),
                T("outside",28).rotate(PI/2).move_to(o+[-.29,h/2,0]),
                T("computed schematic",28,GREY).move_to(o+[w*.64,h+.22,0]))
    return o,w,h,axes


class S09KeepTurning(SpokenScene):
    def construct(self):
        lc,rc,outlines,dots,drops,sites,labs=small_world()
        lo,lw,lh,lax=graph_axes(-3.35); ro,rw,rh,rax=graph_axes(3.35)
        self.add(outlines,dots,drops,sites,labs)
        self.play(FadeIn(lax),FadeIn(rax),run_time=.8)
        self.at("Keep turning")
        tracker=ValueTracker(0)
        dialdot=always_redraw(lambda: Dot([-.2+tracker.get_value()*.4,3.25,0],radius=.1,color=TEXT))
        dialline=Line([-.2,3.25,0],[.2,3.25,0],color=GREY,stroke_width=4)
        self.add(dialline,dialdot)
        sweep_start = self.elapsed()
        def phase_readout():
            f = np.clip((self.elapsed()-sweep_start)/max(self.narration_s, 1), 0, 1)
            x = 10*f
            y = min(x, 1)
            return Line(lo+[lw*f,0,0], lo+[lw*f,lh*y/10,0], color=TEAL, stroke_width=7)
        def site_readout():
            f = np.clip((self.elapsed()-sweep_start)/max(self.narration_s, 1), 0, 1)
            total = 10*f
            roots = np.roots([1,5-total,-total])
            y = max(float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>=0)
            return Line(ro+[rw*f,0,0], ro+[rw*f,rh*y/10,0], color=ORANGE, stroke_width=7)
        live_readouts = VGroup(always_redraw(phase_readout), always_redraw(site_readout))
        self.add(live_readouts)
        self.play(tracker.animate.set_value(1),run_time=.7)
        self.at("parking lot fills up")
        self.play(sites.animate.set_opacity(1),run_time=.6)
        self.at("brighten more slowly")
        self.play(sites.animate.set_fill(opacity=.42),run_time=.7)
        self.at("needle climbs faster")
        # Site model: total = outside + 4*outside/(1+outside), solved numerically.
        totals=np.linspace(0,10,81)
        outs=[]
        for total in totals:
            roots=np.roots([1,5-total,-total])
            outs.append(max(float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>=0))
        rpts=[ro+[rw*t/10,rh*min(y/10,1),0] for t,y in zip(totals,outs)]
        rcurve=VMobject(stroke_color=ORANGE,stroke_width=6).set_points_smoothly(rpts)
        guide=DashedLine(ro,ro+[rw,rh,0],color=GREY,stroke_width=2)
        self.play(Create(guide),Create(rcurve),run_time=1.7,rate_func=linear)
        self.at("droplets keep taking up more room")
        # Phase model: outside=min(total,1); dense fraction=(total-1)/(50-1).
        lpts=[lo+[lw*t/10,lh*t/10,0] for t in np.linspace(0,1,12)]
        lpts += [lo+[lw*t/10,lh*.1,0] for t in np.linspace(1,10,60)]
        lcurve=VMobject(stroke_color=TEAL,stroke_width=6).set_points_as_corners(lpts)
        sat=DashedLine(lo+[0,lh*.1,0],lo+[lw,lh*.1,0],color=YELLOW,stroke_width=3)
        slab=T("saturation",28,YELLOW).move_to(lo+[lw*.72,lh*.1+.35,0])
        bigger=droplet_set(lc,(.58,.55,.57,.54,.56),.62)
        self.play(Create(sat),FadeIn(slab),Create(lcurve),Transform(drops,bigger),run_time=1.7,rate_func=linear)
        self.at("needle stays put")
        self.play(Indicate(lcurve,color=YELLOW,scale_factor=1),run_time=.6)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        lc,rc,outlines,dots,drops,sites,labs=small_world()
        lo,lw,lh,lax=graph_axes(-3.35); ro,rw,rh,rax=graph_axes(3.35)
        lcurve=VMobject(stroke_color=TEAL,stroke_width=6).set_points_as_corners([lo,lo+[lw*.1,lh*.1,0],lo+[lw,lh*.1,0]])
        totals=np.linspace(0,10,60); outs=[]
        for total in totals:
            roots=np.roots([1,5-total,-total]); outs.append(max(float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>=0))
        rcurve=VMobject(stroke_color=ORANGE,stroke_width=6).set_points_smoothly([ro+[rw*t/10,rh*y/10,0] for t,y in zip(totals,outs)])
        self.add(outlines,dots,drops,sites,labs,lax,rax,lcurve,rcurve)
        def phase_readout(f):
            y = min(10*f, 1)
            return Line(lo+[lw*f,0,0],lo+[lw*f,lh*y/10,0],color=TEAL,stroke_width=7)
        def site_readout(f):
            total = 10*f
            roots = np.roots([1,5-total,-total])
            y = max(float(x.real) for x in roots if abs(x.imag)<1e-8 and x.real>=0)
            return Line(ro+[rw*f,0,0],ro+[rw*f,rh*y/10,0],color=ORANGE,stroke_width=7)
        self.at("here is the test")
        q_text=T("Where\ndoes\nthe extra\ngo?",28,weight=BOLD,line_spacing=.72)
        q_back=RoundedRectangle(width=q_text.width+.28,height=q_text.height+.28,
                                corner_radius=.08,stroke_width=0,
                                fill_color=BG,fill_opacity=1)
        q=VGroup(q_back,q_text.move_to(q_back)).move_to([0,.35,0])
        self.play(FadeIn(q),run_time=.65)
        self.at("Add more protein")
        markers=VGroup(phase_readout(.22),site_readout(.22))
        self.play(Create(markers),run_time=.8)
        self.at("watch where the extra goes")
        self.play(Transform(markers,VGroup(phase_readout(.42),site_readout(.42))),run_time=.9)
        self.at("At equilibrium")
        self.play(Transform(markers,VGroup(phase_readout(.62),site_readout(.62))),run_time=.9)
        self.at("one protein")
        self.play(Indicate(drops,color=TEAL,scale_factor=1.04),run_time=.8)
        self.at("more droplet volume")
        la=Arrow(q.get_left(),lc+[.2,-.25,0],buff=.15,color=TEAL,stroke_width=5)
        bigger=droplet_set(lc,(.56,.53,.55,.52,.54),.62)
        self.play(GrowArrow(la),Transform(drops,bigger),run_time=1.2)
        self.at("outside held still")
        self.play(Indicate(lcurve,color=YELLOW,scale_factor=1),run_time=.55)
        self.at("onto those sites")
        ra=Arrow(q.get_right(),rc+[-.2,-.25,0],buff=.15,color=ORANGE,stroke_width=5)
        self.play(GrowArrow(ra),sites.animate.set_opacity(1),run_time=1.0)
        self.at("until they are full")
        self.play(Indicate(sites,color=ORANGE,scale_factor=1.03),run_time=.7)
        self.finish()


class S11Scope(SpokenScene):
    def construct(self):
        lc,rc,outlines,dots,drops,sites,labs=small_world()
        self.add(outlines,dots,drops,sites,labs)
        self.at("one protein")
        one=chip("one protein, on its own",TEXT,28).move_to([lc[0],-.72,0])
        self.play(FadeIn(one),run_time=.55)
        self.at("many kinds of molecule")
        tag1=chip("many kinds",TEXT,28).move_to([-4.7,-1.45,0])
        ring=Circle(radius=.18,stroke_color=YELLOW,stroke_width=4).move_to(drops[2])
        self.play(FadeOut(one),FadeIn(tag1),Create(ring),run_time=.65)
        self.at("form on chromatin")
        tag2=chip("on chromatin",TEXT,28).move_to([0,-1.45,0])
        strand=VMobject(stroke_color=PURPLE,stroke_width=4).set_points_smoothly([[-1.2,-.7,0],[-.5,-.5,0],[.2,-.72,0],[.9,-.5,0]])
        self.play(FadeOut(tag1),FadeIn(tag2),Create(strand),
                  drops[1].animate.move_to([-.5,-.5,0]),run_time=.75)
        self.at("tiny spots")
        tag3=chip("tiny spots",TEXT,28).move_to([4.7,-1.45,0])
        tiny=glow(rc+[.75,.55,0],.13,.35)
        self.play(FadeOut(tag2),FadeIn(tag3),Transform(sites[0],tiny),run_time=.7)
        self.at("a clue not a proof")
        clue=T("a clue, not a proof",40,weight=BOLD).move_to([0,-2.45,0])
        self.play(FadeOut(tag3),FadeIn(clue),run_time=.6)
        self.at("The text below")
        self.play(strand.animate.set_opacity(.35),ring.animate.set_opacity(.35),
                  sites[0].animate.set_opacity(.35),run_time=.9)
        self.finish()


class S12End(EndCard):
    LINE = "Where extra protein goes is a clue to how a spot formed."

