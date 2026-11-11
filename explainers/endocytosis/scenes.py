"""A Loop and a One-Way Trip — endocytosis explainer.

COLOR MAP (fixed throughout)
  TEAL    LDL receptor / recycling path
  GOLD    LDL cargo / cholesterol / one-way path
  VIOLET  adaptors
  GREY    membranes and clathrin
  ORANGE  dynamin
  ROSE    acid endosome lumen / protons
  RED     lysosome outline
"""
from bp_style import *  # noqa: F401,F403
import numpy as np

VIOLET = "#B58CD9"
ORANGE = "#F29E4C"
ROSE = "#E86FA5"
NAVY = "#07172F"
WARM = "#393238"
LDL = GOLD
PI = np.pi

MEM_Y = 2.15
ENDO_C = np.array([-1.75, -0.65, 0.0])
ENDO_R = 1.28
LYSO_C = np.array([3.35, -1.62, 0.0])
LYSO_R = 0.86


def label(text, size=30, color=TEXT):
    t = T(text, size=size, color=color)
    bg = RoundedRectangle(corner_radius=0.08, width=t.width + 0.22, height=t.height + 0.14,
                          stroke_width=0, fill_color=BG, fill_opacity=0.88).move_to(t)
    return VGroup(bg, t)


def receptor(x, y=MEM_Y, scale=1.0, angle=0):
    """Teal membrane-spanning bar, with its cytosolic tail."""
    stem = RoundedRectangle(corner_radius=0.07, width=0.22, height=0.86,
                            stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.70)
    tail = Line([0, -0.42, 0], [0.15, -0.68, 0], color=TEAL, stroke_width=4)
    return VGroup(stem, tail).scale(scale).rotate(angle).move_to([x, y - 0.10, 0])


def ldl_dot(p, r=0.20):
    return Circle(radius=r, color=LDL, stroke_width=3,
                  fill_color=LDL, fill_opacity=0.92).move_to(p)


def membrane():
    return Line([-6.55, MEM_Y, 0], [6.55, MEM_Y, 0], color=GREY, stroke_width=13)


def compartment(center, radius, color=GREY, tint=NAVY, opacity=1.0):
    return Circle(radius=radius, stroke_color=color, stroke_width=7,
                  fill_color=tint, fill_opacity=opacity).move_to(center)


def backgrounds():
    outside = Rectangle(width=14.2, height=1.65, stroke_width=0,
                        fill_color=NAVY, fill_opacity=1).move_to([0, 3.18, 0])
    inside = Rectangle(width=14.2, height=6.35, stroke_width=0,
                       fill_color=WARM, fill_opacity=1).move_to([0, -1.03, 0])
    return VGroup(inside, outside)


def world_base(scene, acid=False, dim=1.0, ambient=True):
    """The fixed world. Returns a dict so every scene uses identical landmarks."""
    bg = backgrounds().set_opacity(dim)
    mem = membrane().set_opacity(dim)
    endo = compartment(ENDO_C, ENDO_R, ROSE if acid else GREY,
                       ROSE if acid else NAVY, 0.22 if acid else 1.0).set_opacity(dim)
    lyso = compartment(LYSO_C, LYSO_R, RED, NAVY, 1).set_opacity(dim)
    scene.add(bg, mem, endo, lyso)
    drifters = VGroup()
    if ambient:
        for i, (x, y) in enumerate([(-5.7, 3.05), (-4.0, 3.38), (2.65, 3.22), (5.25, 2.92)]):
            d = ldl_dot([x, y, 0], 0.13 + 0.015 * (i % 2)).set_opacity(0.72)
            speed = 0.10 + i * 0.015
            def drift(m, dt, speed=speed):
                m.shift(RIGHT * speed * dt)
                if m.get_x() > 6.75:
                    m.shift(LEFT * 13.4)
            d.add_updater(drift)
            drifters.add(d)
        scene.add(drifters)
    return {"bg": bg, "mem": mem, "endo": endo, "lyso": lyso, "drifters": drifters}


def endo_receptors(bound=True, count=4):
    recs, cargo = VGroup(), VGroup()
    angles = np.linspace(135, 405, count, endpoint=False)
    for deg in angles:
        a = np.radians(deg)
        n = np.array([np.cos(a), np.sin(a), 0])
        p = ENDO_C + n * ENDO_R
        r = receptor(0, 0, 0.70, angle=a - PI / 2).move_to(p)
        recs.add(r)
        if bound:
            cargo.add(ldl_dot(p - n * 0.48, 0.16))
    return recs, cargo


def surface_pairs(xs=(-1.35, -0.45, 0.45, 1.35), bound=True):
    rs, ls = VGroup(), VGroup()
    for x in xs:
        rs.add(receptor(x))
        if bound:
            ls.add(ldl_dot([x, MEM_Y + 0.62, 0], 0.18))
    return rs, ls


def curved_arrow(points, color, width=7):
    path = VMobject(color=color, stroke_width=width)
    path.set_points_smoothly([np.array(p, dtype=float) for p in points])
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12)
    if len(points) >= 2:
        v = np.array(points[-1]) - np.array(points[-2])
        tip.rotate(np.arctan2(v[1], v[0]) - PI / 2).move_to(points[-1])
    return VGroup(path, tip)


def pathway_traces():
    teal = curved_arrow([[-0.3, 2.52, 0], [-1.2, 0.7, 0], [-1.75, -0.65, 0],
                         [-0.2, 0.25, 0], [1.0, 1.3, 0], [0.35, 2.5, 0]], TEAL)
    gold = curved_arrow([[0.0, 2.75, 0], [-1.0, 0.5, 0], [-1.4, -0.75, 0],
                         [0.7, -1.2, 0], [2.55, -1.55, 0]], LDL)
    return teal, gold


def ambient_endosome_sweep(scene):
    """A slow sorting sweep that keeps a held world alive without crossing its labels."""
    sweep = Arc(radius=ENDO_R+.13, start_angle=0, angle=1.7,
                color=TEXT, stroke_width=5).move_arc_center_to(ENDO_C)
    sweep.set_opacity(.48)
    sweep.add_updater(lambda m, dt: m.rotate(.30*dt, about_point=ENDO_C))
    scene.add(sweep)
    return sweep


def acid_world(scene, with_receptors=True, with_cargo=True):
    w = world_base(scene, acid=True)
    recs, cargo = endo_receptors(bound=False)
    if with_receptors:
        scene.add(recs)
    if with_cargo:
        cargo = VGroup(*[ldl_dot(ENDO_C + [0.42*np.cos(i*PI/2), 0.42*np.sin(i*PI/2), 0], 0.16)
                         for i in range(4)])
        scene.add(cargo)
    return w, recs, cargo


class S00Hook(SpokenScene, TitleCard):
    TITLE = "A Loop and a One-Way Trip"
    LESSON = "Endocytosis"

    def construct(self):
        w = world_base(self)
        self.play(Create(w["mem"]), FadeIn(w["endo"]), FadeIn(w["lyso"]), run_time=0.8)
        r = receptor(0.1)
        cargo = ldl_dot([0.1, 3.18, 0], 0.20)
        self.play(FadeIn(r), cargo.animate.move_to([0.1, MEM_Y + 0.62, 0]), run_time=0.8)
        self.at("brings LDL")
        ves = Circle(radius=0.47, color=GREY, stroke_width=5, fill_color=NAVY, fill_opacity=1)
        pair = VGroup(receptor(0, 0, .48).move_to([0, .02, 0]), ldl_dot([0, .14, 0], .12))
        preview = VGroup(ves, pair).move_to([0.15, 1.10, 0])
        schem = label("schematic", 24, GREY).move_to([5.55, -3.35, 0])
        self.play(ReplacementTransform(VGroup(r.copy(), cargo.copy()), preview), FadeIn(schem), run_time=0.8)
        self.at("broken down")
        self.play(preview.animate.move_to(ENDO_C), run_time=0.8)
        frag = VGroup(*[ldl_dot(LYSO_C + [0.24*np.cos(k*PI/3), 0.24*np.sin(k*PI/3), 0], .075)
                        for k in range(6)])
        returning = receptor(ENDO_C[0], ENDO_C[1], .55)
        self.play(FadeOut(preview), FadeIn(frag), FadeIn(returning), run_time=0.55)
        self.play(returning.animate.move_to([.45, MEM_Y-.10, 0]), run_time=.65)
        self.play(Indicate(frag, color=LDL, scale_factor=1.18), run_time=0.5)
        self.at("how does the receptor")
        teal, gold = pathway_traces()
        q1 = T("?", 52, TEAL).move_to([1.65, 0.75, 0])
        q2 = T("?", 52, LDL).move_to([1.25, -2.05, 0])
        question = T("Cargo destroyed. Carrier saved. How?", 34, TEXT).move_to([0, 3.38, 0])
        self.play(FadeOut(w["drifters"]), Create(teal), FadeIn(q1), run_time=0.75)
        self.at("cargo to destruction")
        self.play(Create(gold), FadeIn(q2), FadeIn(question), run_time=0.85)
        self.at("over and over")
        dot = Dot(teal[0].get_start(), radius=.10, color=TEAL)
        self.play(MoveAlongPath(dot, teal[0]), run_time=1.2, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    TITLE = "A Loop and a One-Way Trip"
    LESSON = "Endocytosis"


class S02Bind(SpokenScene):
    def construct(self):
        world_base(self, ambient=False)
        ambient_endosome_sweep(self)
        xs = (-1.8, -0.6, 0.6, 1.8)
        rs, _ = surface_pairs(xs, False)
        self.add(rs)
        cargo = VGroup(*[ldl_dot([x + (-.15 if i % 2 else .15), 3.35 + .12*(i%2), 0], .18)
                         for i, x in enumerate(xs)])
        self.add(cargo)
        ldl_l = label("LDL", 30, LDL).move_to([-3.9, 3.25, 0])
        self.at("LDL in gold")
        self.play(FadeIn(ldl_l), *[c.animate.move_to([x, MEM_Y+.62, 0]) for c, x in zip(cargo, xs)], run_time=1.8)
        rec_l = label("receptor", 30, TEAL).move_to([3.9, 2.65, 0])
        self.at("receptor in teal")
        self.play(FadeIn(rec_l), Indicate(rs, color=TEAL, scale_factor=1.08), run_time=.8)
        out = T("outside", 30, TEXT).move_to([-5.15, 2.95, 0])
        cyt = T("cytosol", 30, TEXT).move_to([-5.15, 1.35, 0])
        self.at("grips it from outside")
        self.play(FadeIn(out), FadeIn(cyt), Indicate(cargo, color=LDL), run_time=.8)
        self.at("not entering")
        dash = DashedLine([0, 1.85, 0], [0, .45, 0], color=TEXT, stroke_width=4)
        cross = T("×", 64, RED, weight=BOLD).move_to([0, 1.2, 0])
        self.play(FadeOut(ldl_l), FadeOut(rec_l), FadeOut(out), FadeOut(cyt),
                  Create(dash), FadeIn(cross, scale=1.4), run_time=.7)
        self.play(FadeOut(dash), FadeOut(cross), run_time=.5)
        self.finish()


class S03Gather(SpokenScene):
    def construct(self):
        world_base(self)
        ambient_endosome_sweep(self)
        xs = (-1.8, -0.6, 0.6, 1.8)
        rs, cargo = surface_pairs(xs)
        self.add(rs, cargo)
        self.at("tail inside")
        self.play(*[Indicate(r[1], color=TEAL, scale_factor=1.5) for r in rs], run_time=.9)
        self.at("gathered into a pit")
        target = (-.72, -.24, .24, .72)
        self.play(*[r.animate.shift(RIGHT*(tx-x)) for r, x, tx in zip(rs, xs, target)],
                  *[l.animate.shift(RIGHT*(tx-x)) for l, x, tx in zip(cargo, xs, target)], run_time=1.2)
        ads = VGroup(*[RoundedRectangle(corner_radius=.05, width=.34, height=.28,
                                        color=VIOLET, fill_color=VIOLET, fill_opacity=.8,
                                        stroke_width=2).move_to([tx+.10, MEM_Y-.63, 0]) for tx in target])
        adlab = label("adaptors", 30, VIOLET).move_to([2.65, 1.0, 0])
        self.at("Adaptors in violet")
        for i, a in enumerate(ads):
            self.play(FadeIn(a, shift=UP*.35), run_time=.35)
            if i == 0:
                self.play(FadeIn(adlab), run_time=.25)
        self.at("hold the receptor tails")
        self.play(*[Indicate(VGroup(r[1], a), color=VIOLET, scale_factor=1.12)
                    for r, a in zip(rs, ads)], run_time=.8)
        self.at("inner face")
        self.play(FadeOut(adlab), Indicate(VGroup(*ads), color=VIOLET),
                  Indicate(membrane(), color=GREY), run_time=.8)
        self.finish()


def pit_membrane(depth=1.7, neck=.72):
    pts = [np.array([-6.55, MEM_Y, 0]), np.array([-neck, MEM_Y, 0]),
           np.array([-neck, MEM_Y-.35, 0]), np.array([-1.2, MEM_Y-depth, 0]),
           np.array([0, MEM_Y-depth-.42, 0]), np.array([1.2, MEM_Y-depth, 0]),
           np.array([neck, MEM_Y-.35, 0]), np.array([neck, MEM_Y, 0]), np.array([6.55, MEM_Y, 0])]
    m = VMobject(color=GREY, stroke_width=13)
    m.set_points_smoothly(pts)
    return m


def triskelion(p, scale=.26):
    hub = Dot(p, radius=.065, color=GREY)
    legs = VGroup()
    for a in (PI/2, PI/2+2*PI/3, PI/2+4*PI/3):
        q = np.array(p)+scale*np.array([np.cos(a), np.sin(a), 0])
        q2 = q+.15*np.array([np.cos(a+.7), np.sin(a+.7), 0])
        line = VMobject(color=GREY, stroke_width=4).set_points_as_corners([p, q, q2])
        legs.add(line)
    return VGroup(hub, legs)


class S04Cage(SpokenScene):
    def construct(self):
        w = world_base(self)
        rs, cargo = surface_pairs((-.72, -.24, .24, .72))
        ads = VGroup(*[RoundedRectangle(corner_radius=.05, width=.32, height=.25, color=VIOLET,
                                        fill_color=VIOLET, fill_opacity=.8).move_to([x+.08, MEM_Y-.62, 0])
                       for x in (-.72, -.24, .24, .72)])
        self.add(rs, cargo, ads)
        pieces = VGroup(*[triskelion([x, .75-.12*abs(x), 0]) for x in np.linspace(-1.55, 1.55, 9)])
        lab = label("clathrin", 30, GREY).move_to([3.4, .55, 0])
        self.at("clathrin builds")
        for i, p in enumerate(pieces):
            self.play(FadeIn(p, shift=UP*.35), run_time=.18)
            if i == 2:
                self.play(FadeIn(lab), run_time=.25)
        self.at("neither membrane nor cargo")
        self.play(pieces.animate.set_opacity(.25), ads.animate.set_opacity(1), run_time=.45)
        self.play(Indicate(ads, color=VIOLET, scale_factor=1.15), pieces.animate.set_opacity(1), run_time=.65)
        self.at("cage grows")
        deep = pit_membrane()
        self.play(FadeOut(lab), Transform(w["mem"], deep),
                  rs.animate.shift(DOWN*1.15), cargo.animate.shift(DOWN*1.15),
                  ads.animate.shift(DOWN*1.15), pieces.animate.shift(DOWN*.45), run_time=1.8)
        self.at("into a pit")
        self.play(Indicate(VGroup(w["mem"], pieces), color=GREY, scale_factor=1.02), run_time=.7)
        self.finish()


class S05Cut(SpokenScene):
    def construct(self):
        w = world_base(self)
        self.remove(w["mem"])
        pit = pit_membrane(2.1, .42)
        self.add(pit)
        ves = Circle(radius=1.15, color=GREY, stroke_width=12, fill_color=NAVY, fill_opacity=1).move_to([0, .22, 0])
        coat = VGroup(*[triskelion([1.45*np.cos(a), .22+1.45*np.sin(a), 0], .22)
                        for a in np.linspace(PI, 2*PI, 10)])
        rs, cargo = surface_pairs((-.6,-.2,.2,.6))
        rs.shift(DOWN*1.55); cargo.shift(DOWN*1.55)
        ads = VGroup(*[RoundedRectangle(corner_radius=.04,width=.25,height=.19,color=VIOLET,
                                        fill_color=VIOLET,fill_opacity=.8).move_to([x,.52,0])
                       for x in (-.6,-.2,.2,.6)])
        self.add(coat, rs, cargo, ads)
        ring = VGroup(*[Dot([.48*np.cos(a), 2.0+.15*np.sin(a), 0], radius=.09, color=ORANGE)
                        for a in np.linspace(0, 2*PI, 12, endpoint=False)])
        lab = label("dynamin", 30, ORANGE).move_to([2.15, 2.6, 0])
        self.at("orange wraps")
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN*.3) for d in ring], lag_ratio=.08), FadeIn(lab), run_time=1.0)
        self.at("using energy from GTP")
        gtp = chip("GTP", ORANGE, size=28).move_to([-2.0, 2.8, 0])
        self.play(FadeIn(gtp), ring.animate.scale(.72, about_point=[0,2.0,0]), run_time=.75)
        self.at("cuts it")
        free = VGroup(ves, coat, rs, cargo, ads)
        self.play(FadeOut(ring), FadeOut(lab), FadeOut(gtp), FadeOut(pit), FadeIn(membrane()),
                  free.animate.shift(DOWN*.55), run_time=.75)
        self.at("pinches free")
        self.play(free.animate.shift(DOWN*.55), run_time=.75)
        self.at("cage falls away")
        self.play(*[p.animate.shift(np.array([p.get_x()*.35, -.7, 0])).set_opacity(0) for p in coat],
                  ads.animate.shift(DOWN*.6).set_opacity(0), run_time=1.2)
        self.finish()


class S06Topology(SpokenScene):
    def construct(self):
        world_base(self)
        ves = Circle(radius=1.12, color=GREY, stroke_width=9, fill_color=NAVY, fill_opacity=1).move_to([1.05,.25,0])
        rs = VGroup(*[receptor(0,0,.65,a).move_to([1.05+1.12*np.cos(a),.25+1.12*np.sin(a),0])
                      for a in (PI, 4*PI/3, 5*PI/3, 2*PI)])
        cargo = VGroup(*[ldl_dot([1.05+.55*np.cos(a),.25+.55*np.sin(a),0],.15)
                         for a in (PI,4*PI/3,5*PI/3,2*PI)])
        self.add(ves, rs, cargo)
        self.at("Look inside")
        self.play(VGroup(ves,rs,cargo).animate.scale(1.28, about_point=[1.05,.25,0]), run_time=1.0)
        self.at("colour of the outside")
        link = Line([1.05,1.30,0],[1.05,2.72,0],color=TEXT,stroke_width=3)
        same = label("same as outside",30,TEXT).move_to([3.85,.25,0])
        self.play(Create(link), FadeIn(same), Indicate(ves, color=TEXT), run_time=.9)
        self.at("inside the cell")
        self.play(Indicate(ves, color=GREY, scale_factor=1.04), run_time=.8)
        self.at("no membrane has been crossed")
        halo = Circle(radius=ves.width/2, color=TEXT, stroke_width=14).move_to(ves)
        self.play(Create(halo), run_time=.55)
        self.play(FadeOut(halo), run_time=.55)
        self.at("topologically outside")
        topo = label("topologically outside",30,TEXT).move_to(same)
        self.play(FadeOut(same), FadeOut(link),
                  VGroup(ves,rs,cargo).animate.scale(1/1.28,about_point=[1.05,.25,0]).shift(LEFT*.5),
                  run_time=.55)
        self.play(FadeIn(topo), run_time=.55)
        self.finish()


class S06bRest(Scene):
    def construct(self):
        world_base(self)
        ves = Circle(radius=.82,color=GREY,stroke_width=8,fill_color=NAVY,fill_opacity=1).move_to([.55,.25,0])
        self.add(ves)
        self.play(ves.animate.move_to(ENDO_C+RIGHT*1.55), run_time=2.0, rate_func=linear)


class S07Fuse(SpokenScene):
    def construct(self):
        w = world_base(self)
        ves = Circle(radius=.72,color=GREY,stroke_width=7,fill_color=NAVY,fill_opacity=1).move_to([.3,-.15,0])
        vrs = VGroup(*[receptor(0,0,.55,a).move_to([.3+.72*np.cos(a),-.15+.72*np.sin(a),0]) for a in (2.1,3.2,4.3,5.4)])
        vls = VGroup(*[ldl_dot([.3+.3*np.cos(a),-.15+.3*np.sin(a),0],.13) for a in (2.1,3.2,4.3,5.4)])
        self.add(ves,vrs,vls)
        self.at("fuses with an early endosome")
        recs,cargo=endo_receptors(True)
        lab=label("early endosome",30,TEXT).move_to([-1.75,-2.35,0])
        sorting_sweep=Arc(radius=ENDO_R+0.13,start_angle=0,angle=2.25,color=TEXT,stroke_width=4).move_arc_center_to(ENDO_C)
        sorting_sweep.set_opacity(.55)
        sorting_sweep.add_updater(lambda m,dt: m.rotate(.34*dt,about_point=ENDO_C))
        self.play(FadeOut(ves),ReplacementTransform(vrs,recs),ReplacementTransform(vls,cargo),
                  w["endo"].animate.scale(1.08),FadeIn(lab),FadeIn(sorting_sweep),run_time=1.4)
        self.at("arrived together")
        self.play(*[Indicate(VGroup(r,l),color=LDL,scale_factor=1.08) for r,l in zip(recs,cargo)],run_time=.9)
        self.at("they must part here")
        brackets=VGroup(*[Line(r.get_center(),l.get_center(),color=TEXT,stroke_width=3) for r,l in zip(recs,cargo)])
        self.play(Create(brackets),run_time=.7)
        self.at("What is different")
        q=T("What is different about this compartment?",36,TEXT).move_to([0,3.35,0])
        shade=Rectangle(width=14.2,height=8,fill_color=BG,fill_opacity=.45,stroke_width=0)
        focus=compartment(ENDO_C,ENDO_R*1.13,TEXT,NAVY,1)
        self.play(FadeOut(w["drifters"]),FadeIn(shade),FadeIn(focus),FadeIn(q),run_time=.9)
        self.at("Think about it")
        self.play(focus.animate.scale(1.03),run_time=.55,rate_func=there_and_back)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        world_base(self,dim=.5,ambient=False)
        e=compartment(ENDO_C,ENDO_R*1.08,TEXT,NAVY,1)
        q=T("What is different about this compartment?",36,TEXT).move_to([0,3.35,0])
        self.add(e,q)
        sweep = Dot(e.get_top(), radius=.09, color=TEXT)
        orbit = Circle(radius=ENDO_R*1.08).move_to(ENDO_C)
        self.add(sweep)
        self.play(e.animate.scale(1.08), MoveAlongPath(sweep, orbit), run_time=2.25, rate_func=there_and_back)
        self.play(e.animate.scale(1.08), MoveAlongPath(sweep, orbit), run_time=2.25, rate_func=there_and_back)


class S10Acid(SpokenScene):
    def construct(self):
        w=world_base(self)
        recs,cargo=endo_receptors(True)
        self.add(recs,cargo)
        self.at("lumen is mildly acid")
        acid=compartment(ENDO_C,ENDO_R,ROSE,ROSE,.22)
        acid_sweep=Arc(radius=ENDO_R+.10,start_angle=0,angle=2.4,color=ROSE,stroke_width=7).move_arc_center_to(ENDO_C)
        acid_sweep.add_updater(lambda m,dt:m.rotate(.42*dt,about_point=ENDO_C))
        acidlab=label("mildly acid  •  pH about 6",30,ROSE).move_to([-1.75,-2.36,0])
        self.play(ReplacementTransform(w["endo"],acid),FadeIn(acid_sweep),FadeIn(acidlab),run_time=1.0)
        pumps=VGroup(*[RoundedRectangle(corner_radius=.04,width=.28,height=.18,color=ROSE,
                                       fill_color=ROSE,fill_opacity=.8).move_to(ENDO_C+ENDO_R*np.array([np.cos(a),np.sin(a),0]))
                       for a in (.2,1.2,2.7)])
        plab=label("proton pumps",28,ROSE).move_to([1.55,.0,0])
        self.at("proton pumps")
        self.play(FadeIn(pumps),FadeIn(plab),run_time=.65)
        pluses=VGroup(*[T("+",28,ROSE).move_to(ENDO_C+2.0*np.array([np.cos(a),np.sin(a),0])) for a in (.2,1.2,2.7)])
        self.play(*[p.animate.move_to(ENDO_C+.62*(p.get_center()-ENDO_C)) for p in pluses],FadeIn(pluses),run_time=1.1)
        self.at("acid is the signal")
        self.play(FadeOut(plab), Indicate(acidlab,color=ROSE),run_time=.7)
        self.at("let go")
        targets=[ENDO_C+[.35*np.cos(k*PI/2),.35*np.sin(k*PI/2),0] for k in range(4)]
        self.play(*[l.animate.move_to(p) for l,p in zip(cargo,targets)],run_time=1.0)
        self.at("This is the fork")
        fork=VGroup(Line(ENDO_C+[0,.2,0],ENDO_C+[-.55,-.4,0],color=TEAL,stroke_width=7),
                    Line(ENDO_C+[0,.2,0],ENDO_C+[.55,-.4,0],color=LDL,stroke_width=7))
        self.play(Create(fork),run_time=.7)
        self.finish()


class S11Fork(SpokenScene):
    def construct(self):
        w,recs,cargo=acid_world(self)
        self.at("paths split")
        self.play(Indicate(recs,color=TEAL),Indicate(cargo,color=LDL),run_time=.7)
        tube=RoundedRectangle(corner_radius=.22,width=2.55,height=.44,color=GREY,stroke_width=6,
                              fill_color=NAVY,fill_opacity=1).move_to([-.2,.35,0]).rotate(.55)
        self.at("thin tubule")
        self.play(GrowFromPoint(tube,ENDO_C+UP*ENDO_R),run_time=.8)
        marks=VGroup(*[receptor(0,0,.48,.55).move_to([-.95+.42*k,-.15+.25*k,0]) for k in range(4)])
        self.play(ReplacementTransform(recs,marks),run_time=1.0)
        carrier=VGroup(tube,marks)
        self.at("pinches off")
        self.play(carrier.animate.shift(UP*.35+RIGHT*.3),run_time=.65)
        self.at("back to the surface")
        surf=VGroup(*[receptor(x) for x in (-.6,-.2,.2,.6)])
        self.play(carrier.animate.move_to([0,1.55,0]),run_time=.8)
        self.play(FadeOut(carrier),FadeIn(surf),run_time=.65)
        self.at("ready to grip again")
        new=ldl_dot([.2,3.28,0],.18)
        self.add(new)
        self.play(new.animate.move_to([.2,MEM_Y+.62,0]),run_time=.8)
        self.finish()


class S12Oneway(SpokenScene):
    def construct(self):
        w,_,cargo=acid_world(self,with_receptors=False)
        surf,_=surface_pairs((-.6,-.2,.2,.6),False);self.add(surf)
        lab=label("early endosome",30,TEXT).move_to([-1.75,-2.35,0])
        self.add(lab)
        self.at("LDL stays behind")
        self.play(Indicate(cargo,color=LDL,scale_factor=1.2),run_time=.8)
        self.at("endosome matures")
        late=label("late endosome",30,TEXT).move_to(lab)
        self.play(Transform(lab,late),w["endo"].animate.set_stroke(ROSE),run_time=.9)
        self.at("passes it to a lysosome")
        lysolab=label("lysosome",30,RED).move_to([3.35,-3.02,0])
        self.play(w["endo"].animate.move_to(LYSO_C+LEFT*.65).scale(.72),cargo.animate.move_to(LYSO_C),
                  FadeIn(lysolab),run_time=1.2)
        self.play(FadeOut(w["endo"]),FadeOut(lab),Indicate(w["lyso"],color=RED),run_time=.55)
        self.at("enzymes break it down")
        frags=VGroup(*[ldl_dot(LYSO_C+[.42*np.cos(k*PI/5),.42*np.sin(k*PI/5),0],.07) for k in range(10)])
        self.play(ReplacementTransform(cargo,frags),run_time=1.0)
        self.at("release its cholesterol")
        out=label("cholesterol released",30,LDL).move_to([3.2,-3.0,0])
        self.play(FadeOut(lysolab),FadeIn(out),w["lyso"].animate.scale(1.06),run_time=.55,rate_func=there_and_back)
        self.finish()


class S13Rest(Scene):
    def construct(self):
        world_base(self,acid=True)
        rs,_=surface_pairs((-.6,-.2,.2,.6),False)
        frags=VGroup(*[ldl_dot(LYSO_C+[.4*np.cos(k*PI/4),.4*np.sin(k*PI/4),0],.07) for k in range(8)])
        new=ldl_dot([.2,3.3,0],.18)
        self.add(rs,frags,new)
        self.play(new.animate.move_to([.2,MEM_Y+.62,0]),run_time=2.0)


class S14Rule(SpokenScene):
    def construct(self):
        world_base(self,acid=True,ambient=False)
        ambient_endosome_sweep(self)
        surf,_=surface_pairs((-.6,-.2,.2,.6),False);self.add(surf)
        teal,gold=pathway_traces()
        labs=VGroup(*[label(s,30,TEAL).move_to(p) for s,p in zip(("bind","enter","release","return"),
                    ((-2.35,3.18,0),(-4.15,.80,0),(-3.35,-2.62,0),(1.45,3.18,0)))])
        self.at("receptor runs a loop")
        self.play(Create(teal),run_time=1.1)
        for phrase,lab in zip(("Bind","enter","release","return"),labs):
            self.at(phrase)
            self.play(FadeIn(lab),run_time=.35)
        self.at("one way trip")
        self.play(Create(gold),run_time=1.1)
        self.at("part at one place")
        ring=Circle(radius=1.48,color=TEXT,stroke_width=5).move_to(ENDO_C)
        self.play(Create(ring),Indicate(compartment(ENDO_C,ENDO_R,ROSE,ROSE,.2),color=ROSE),run_time=.8)
        self.finish()


class S14bRest(Scene):
    def construct(self):
        world_base(self,acid=True)
        teal,gold=pathway_traces();self.add(teal,gold)
        td=Dot(teal[0].get_start(),radius=.10,color=TEAL)
        gd=Dot(gold[0].get_start(),radius=.10,color=LDL)
        self.play(MoveAlongPath(td,teal[0]),MoveAlongPath(gd,gold[0]),run_time=2.5,rate_func=linear)


class S15Order(SpokenScene):
    def construct(self):
        world_base(self,acid=True,ambient=False)
        teal,gold=pathway_traces();self.add(teal,gold)
        ambient_endosome_sweep(self)
        names=("bind","enter","release","return")
        pos=((-2.35,3.18,0),(-4.15,.80,0),(-3.35,-2.62,0),(1.45,3.18,0))
        labs=VGroup(*[label(n,30,TEAL).move_to(p) for n,p in zip(names,pos)])
        self.add(labs)
        self.at("happen in order")
        for l in labs:
            self.play(Indicate(l,color=TEAL,scale_factor=1.13),run_time=.35)
        tag=label("one batch • schematic",24,GREY).move_to([5.05,-3.35,0])
        self.at("Follow one batch")
        dot=Dot(teal[0].get_start(),radius=.11,color=TEAL)
        self.play(FadeIn(tag),MoveAlongPath(dot,teal[0]),run_time=1.3,rate_func=linear)
        self.at("complete block")
        block=RoundedRectangle(corner_radius=.08,width=1.55,height=.48,color=GREY,stroke_width=3,
                               fill_color=GREY,fill_opacity=.92).move_to([-1.0,2.15,0])
        bt=label("blocked",30,GREY).move_to([-.85,2.88,0])
        self.play(FadeIn(block,shift=DOWN*.35),FadeIn(bt,shift=DOWN*.35),run_time=.7)
        self.at("stops its later handling")
        self.play(*[l.animate.set_opacity(.25) for l in labs[1:]],FadeOut(gold),run_time=1.1)
        self.at("reduce return rather than abolish it")
        self.play(FadeOut(block),FadeOut(bt),*[(l.animate.set_opacity(.55) if i==3 else l.animate.set_opacity(1))
                  for i,l in enumerate(labs)],FadeIn(gold),run_time=1.1)
        self.at("test each transition")
        self.play(*[Indicate(l,color=TEXT,scale_factor=1.12) for l in labs],run_time=.9)
        self.finish()


class S16Close(SpokenScene):
    def construct(self):
        world_base(self,acid=True)
        surf,_=surface_pairs((-.6,-.2,.2,.6),False);self.add(surf)
        teal,gold=pathway_traces();self.add(teal,gold)
        cargo=ldl_dot([.2,3.3,0],.18);self.add(cargo)
        self.at("carrier escapes")
        self.play(cargo.animate.move_to([.2,MEM_Y+.62,0]),
                  teal[0].animate.set_stroke(width=15),run_time=.65)
        self.play(teal[0].animate.set_stroke(width=7),run_time=.45)
        self.at("lets go in acid")
        td=Dot(teal[0].get_start(),radius=.11,color=TEAL)
        gd=Dot(gold[0].get_start(),radius=.11,color=LDL)
        self.play(MoveAlongPath(td,teal[0]),MoveAlongPath(gd,gold[0]),
                  teal[0].animate.set_stroke(width=14),gold[0].animate.set_stroke(width=14),
                  run_time=1.5,rate_func=linear)
        self.play(teal[0].animate.set_stroke(width=7),gold[0].animate.set_stroke(width=7),run_time=.5)
        self.at("patient's cells")
        self.play(teal.animate.set_opacity(.2),gold.animate.set_opacity(.2),run_time=.5)
        dishes=VGroup()
        for x in (-2.7,0,2.7):
            dish=VGroup(Ellipse(width=1.65,height=.48,color=GREY,stroke_width=4),
                        T("?",36,TEXT).move_to([0,.25,0])).move_to([x,-2.8,0])
            dishes.add(dish)
        pl=label("patient cells",28,TEXT).move_to([0,-3.45,0])
        self.play(LaggedStart(*[FadeIn(d,shift=UP*.3) for d in dishes],lag_ratio=.2),FadeIn(pl),run_time=1.0)
        self.at("how could you tell")
        self.play(*[Indicate(d,color=TEXT,scale_factor=1.06) for d in dishes],run_time=.7)
        self.finish()


class S17End(EndCard):
    LINE = "The receptor runs a loop; its LDL makes a one-way trip."

