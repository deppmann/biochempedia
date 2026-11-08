"""Chapter 1 (Born Outside) of the chaptered film for "Tangential Migration: Interneurons and the Long Way Round"

COLOR MAP (one color per concept, whole film series; taken from scenes.old.py)
  ORANGE = inhibitory interneuron (the travelling cell), and the subpallium that makes them
  BLUE   = excitatory pyramidal neuron, and the pallium (cortex's own wall) that makes them
  TEAL   = the cue on the road (chemokine)
  PURPLE = the receptor on the travelling cell (the little tab), and "what the cell can read"
  RED    = broken / missing (receptor that cannot answer, cue that is absent)
  GREY   = tissue and structure: wall, fibres, eminences, progenitors, labels
  (script.json's visual notes say green/magenta; the series map above is used instead so that
   chapters 2 and 3 match the earlier film.)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
LUMEN = "#171a23"

CX, CY = 0.0, 0.1
R_OUT, R_IN = 2.7, 1.75
A_LGE, A_CGE, A_MGE = 205, 255, 305


def lab(text, color=TEXT, size=24, **kw):
    return T(text, max(26, size), color, **kw)


def pol(r, deg, c=(CX, CY)):
    return np.array([c[0] + r * np.cos(np.radians(deg)), c[1] + r * np.sin(np.radians(deg)), 0.0])


def unit(v):
    return v / np.linalg.norm(v)


# --------------------------------------------------------------------------- cell shapes
def tri(size=0.46, color=BLUE, op=0.9):
    return Triangle(stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).scale(size / 1.73)


def dot(r=0.2, color=ORANGE, op=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)


def tabbed(r=0.26, direction=RIGHT, color=ORANGE):
    """Travelling cell (orange) with its receptor tab (purple) on the leading side."""
    c = dot(r, color)
    ang = np.arctan2(direction[1], direction[0])
    t = RoundedRectangle(corner_radius=0.03, width=r * 0.4, height=r * 0.95, stroke_color=PURPLE, stroke_width=1.5,
                         fill_color=PURPLE, fill_opacity=1)
    t.rotate(ang).move_to(c.get_center() + unit(np.array([np.cos(ang), np.sin(ang), 0])) * (r + r * 0.12))
    g = VGroup(c, t)
    g.c, g.tab = c, t
    return g


# --------------------------------------------------------------------------- cortex strip (s01, s02)
def cortex_strip():
    strip = RoundedRectangle(corner_radius=0.3, width=11.8, height=5.6, stroke_color=GREY, stroke_width=2.5,
                             fill_color=GREY, fill_opacity=0.08).move_to([0, -0.3, 0])
    rnd = random.Random(7)
    tris, dots = VGroup(), VGroup()
    for r in range(5):
        for c in range(8):
            x = -5.0 + c * 1.43 + rnd.uniform(-0.18, 0.18)
            y = -0.3 + 2.2 - r * 1.1 + rnd.uniform(-0.1, 0.1)
            if r == (c * 3 + 1) % 5:
                dots.add(dot(0.28).move_to([x, y, 0]))
            else:
                tris.add(tri(0.64).move_to([x, y, 0]))
    g = VGroup(strip, tris, dots)
    g.strip, g.tris, g.dots = strip, tris, dots
    return g


def nearest(p, group, n):
    return sorted(group, key=lambda m: np.linalg.norm(m.get_center() - p))[:n]


def excite_links(g):
    src = g.tris[19]
    tg = nearest(src.get_center(), [t for t in g.tris if t is not src], 3)
    return VGroup(*[Arrow(src.get_center(), t.get_center(), buff=0.3, color=BLUE, stroke_width=5,
                          max_tip_length_to_length_ratio=0.3) for t in tg])


def inhib_links(g):
    src = g.dots[3]
    tg = nearest(src.get_center(), list(g.tris), 3)
    out = VGroup()
    for t in tg:
        a, b = src.get_center(), t.get_center()
        u = unit(b - a)
        end = b - u * 0.32
        ln = Line(a + u * 0.26, end, color=ORANGE, stroke_width=5)
        perp = np.array([-u[1], u[0], 0]) * 0.17
        out.add(VGroup(ln, Line(end + perp, end - perp, color=ORANGE, stroke_width=6)))
    return out


def legend_chips():
    a = chip("excitatory", BLUE, 24).move_to([2.3, 2.75, 0])
    b = chip("inhibitory", ORANGE, 24).move_to([5.0, 2.75, 0])
    return a, b


# --------------------------------------------------------------------------- cortical wall (s03, s04, s12)
WX0, WX1 = -3.6, 3.6
FIBX = [-2.7, -1.35, 0.0, 1.35, 2.7]


def wall():
    rect = Rectangle(width=8.0, height=5.9, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.08).move_to([0, -0.05, 0])
    surf = RoundedRectangle(corner_radius=0.06, width=8.0, height=0.16, stroke_width=0, fill_color=GREY,
                            fill_opacity=0.6).move_to([0, 3.0, 0])
    vent = Rectangle(width=8.0, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to([0, -2.75, 0])
    ls = lab("surface", GREY, 22).move_to([5.0, 3.0, 0])
    lv = lab("ventricle", GREY, 22).move_to([5.1, -2.75, 0])
    g = VGroup(rect, vent, surf, ls, lv)
    g.surf = surf
    return g


def fibres():
    return VGroup(*[Line([x, -2.5, 0], [x, 2.9, 0], color=GREY, stroke_width=3, stroke_opacity=0.85) for x in FIBX])


# --------------------------------------------------------------------------- hemisphere section (s06 - s11, s22)
def sector(a0, a1, col, op, sw=2.5):
    return AnnularSector(inner_radius=R_IN, outer_radius=R_OUT, angle=np.radians(a1 - a0), start_angle=np.radians(a0),
                         arc_center=np.array([CX, CY, 0]), stroke_color=col, stroke_width=sw, fill_color=col,
                         fill_opacity=op)


def swell(ang, op=0.55):
    e = Ellipse(width=1.15, height=0.95, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=op)
    e.rotate(np.radians(ang - 270)).move_to(pol(R_IN - 0.3, ang))
    return e


def section(stage="plain"):
    """stage: plain (all grey), pal (pallium blue), both (pallium blue, subpallium orange)."""
    lum = Circle(radius=R_IN, stroke_color=GREY, stroke_width=1.5, stroke_opacity=0.5, fill_color=LUMEN,
                 fill_opacity=1).move_to([CX, CY, 0])
    pal = sector(20, 160, BLUE if stage in ("pal", "both") else GREY, 0.5 if stage in ("pal", "both") else 0.15)
    sub = sector(160, 380, ORANGE if stage == "both" else GREY, 0.35 if stage == "both" else 0.15)
    g = VGroup(lum, pal, sub)
    g.lum, g.pal, g.sub = lum, pal, sub
    return g


def chip_at(text, color, pos, size=24):
    return chip(text, color, size).move_to(pos)


def leader(a, b, col=GREY, frm=0.0, trim=0.0):
    u = unit(b - a)
    return Line(a + u * frm, b - u * trim, color=col, stroke_width=2, stroke_opacity=0.75)


MK_X0, MK_X1, MK_Y = -6.2, -3.0, -3.05


def marker(f=0.0):
    ln = Line([MK_X0, MK_Y, 0], [MK_X1, MK_Y, 0], color=GREY, stroke_width=3)
    r = lab("rostral", GREY, 22).move_to([MK_X0 + 0.45, MK_Y - 0.42, 0])
    c = lab("caudal", GREY, 22).move_to([MK_X1 - 0.4, MK_Y - 0.42, 0])
    pl = Line([0, -0.3, 0], [0, 0.3, 0], color=TEXT, stroke_width=7).move_to([plane_x(f), MK_Y, 0])
    g = VGroup(ln, r, c, pl)
    g.plane = pl
    return g


def plane_x(f):
    return MK_X0 + 0.3 + f * (MK_X1 - MK_X0 - 0.6)


# --------------------------------------------------------------------------- rule card (s14 - s16, s20, s24)
def lag(seconds, anim):
    return Succession(Wait(seconds), anim) if seconds > 0.01 else anim


def top_labels():
    pl = lab("pallium", BLUE, 30).move_to([0, 3.3, 0])
    co = lab("= cortex", BLUE, 30).next_to(pl, RIGHT, buff=0.2)
    return pl, co


def rule_badge():
    r = rule_text().move_to([0, -0.2, 0])
    fit(r, max_w=10.8)
    r.scale(0.6).move_to([-3.5, 3.05, 0])
    bd = SurroundingRectangle(r, buff=0.15, corner_radius=0.15, color=GOLD, stroke_width=2.5)
    return r, bd


def card():
    return RoundedRectangle(corner_radius=0.3, width=11.6, height=4.6, stroke_color=GOLD, stroke_width=3,
                            fill_color=BG, fill_opacity=1)


def rule_text(size=38):
    """Two lines of the rule; returns (group, [word groups])."""
    texts = ["Born outside the cortex,", "steered by what the cell can read."]
    lines, words = [], []
    for tx in texts:
        t = T(tx, size, TEXT, font=TITLE_FONT)
        idx = 0
        for w in tx.split():
            words.append(VGroup(*t[idx: idx + len(w)]))
            idx += len(w)
        lines.append(t)
    g = VGroup(*lines).arrange(DOWN, buff=0.4)
    g.words = words   # born outside the cortex, | steered by what the cell can read.
    return g




def question_cortex():
    g=cortex_strip().scale(0.86).move_to([0,-0.9,0])
    q=T("Where do the inhibitory\nneurons come from?",44,TEXT,font=TITLE_FONT,line_spacing=1.25).move_to([0,2.65,0])
    return g,q


def coronal(caudal=False, stage="both"):
    lobes=VGroup()
    for side in (-1,1):
        outer=Ellipse(width=4.1 if not caudal else 3.7,height=5.3,stroke_color=GREY,stroke_width=3,
                      fill_color=BLUE if stage!="plain" else GREY,fill_opacity=0.2).move_to([side*2.05,0,0])
        # Tapered ventricular slit gives the schematic a medial indentation.
        vent=VMobject(stroke_color=GREY,stroke_width=2,fill_color=LUMEN,fill_opacity=1)
        w=1.0 if not caudal else 0.78
        vp=[[-0.25,1.45,0],[-w,0.65,0],[-w*0.9,-0.45,0],[-0.25,-1.45,0],
            [w*0.48,-0.85,0],[w*0.24,-0.05,0],[w*0.5,0.85,0],[-0.25,1.45,0]]
        vent.set_points_smoothly([np.array(v) for v in vp])
        vent.rotate(side*0.25).move_to([side*2.1,-0.05,0])
        if stage == "both":
            lower=Intersection(outer,Rectangle(width=4.5,height=2.8).move_to([side*2.05,-1.35,0]),
                               stroke_width=0,fill_color=ORANGE,fill_opacity=0.22)
            lobes.add(outer,lower,vent)
        else:
            lobes.add(outer,vent)
    mid=DashedLine([0,-2.8,0],[0,2.8,0],color=GREY,stroke_width=2)
    lobes.add(mid)
    return lobes


def eminences(caudal=False):
    positions=([[-2.55,-1.35,0]] if caudal else [[-2.75,-1.1,0],[-1.05,-1.65,0]])
    return VGroup(*[Ellipse(width=1.15,height=0.9,stroke_color=ORANGE,fill_color=ORANGE,fill_opacity=0.5).move_to(p) for p in positions])


def plane_tag(caudal=False):
    return lab("caudal section plane" if caudal else "rostral section plane",TEXT,30).move_to([0,3.25,0])


def paired_sections():
    out=VGroup()
    for x,caud in ((-3.2,False),(3.2,True)):
        tissue=coronal(caud).scale(0.62).move_to([x,0.5,0])
        es=eminences(caud).scale(0.62,about_point=ORIGIN).shift([x,0.5,0])
        title=lab("caudal section" if caud else "rostral section",TEXT,28).move_to([x,2.85,0])
        out.add(VGroup(tissue,es,title))
    return out


def source_names():
    a=lab("lateral ganglionic\neminence (LGE)",ORANGE,26).move_to([-4.65,-2.0,0])
    b=lab("medial ganglionic\neminence (MGE)",ORANGE,26).move_to([-1.45,-2.0,0])
    c=lab("caudal ganglionic\neminence (CGE)",ORANGE,26).move_to([3.2,-2.0,0])
    return VGroup(a,b,c)


def nursery():
    g=paired_sections(); ns=source_names()
    dots=VGroup()
    for panel in g:
        for e in panel[1]:
            dots.add(dot(0.19,TEXT).move_to(e))
    return g,ns,dots




def fault_panels(tall=False):
    stage=VGroup()
    cells=VGroup();cues=VGroup()
    for x in (-3.5,3.5):
        box=RoundedRectangle(width=5.8 if tall else 5.5,height=6.7 if tall else 5.7,corner_radius=0.25,color=GREY,fill_color=GREY,fill_opacity=0.05).move_to([x,0.2,0])
        road=DashedLine([x-1.6,-1.4,0],[x+1.6,1.0,0],color=GREY,stroke_width=5)
        cl=tabbed(0.6,RIGHT).shift([x-0.55,-0.6,0])
        cue=diamond(0.55).move_to([x+1.1,0.65,0])
        stage.add(box,road);cells.add(cl);cues.add(cue)
    return stage,cells,cues


def embryo(x,scale=1):
    body=VMobject(stroke_color=TEXT,stroke_width=4,fill_color=GREY,fill_opacity=0.22)
    pts=[[-0.2,1.7,0],[-1.4,1.15,0],[-1.55,-0.3,0],[-0.7,-1.6,0],[0.65,-1.5,0],
         [1.1,-0.55,0],[0.5,-0.1,0],[0.15,-0.9,0],[-0.6,-0.65,0],[-0.7,0.2,0],[0.3,0.35,0],[0.8,1.1,0],[-0.2,1.7,0]]
    body.set_points_smoothly([np.array(p) for p in pts])
    eye=dot(0.1,TEXT).move_to([-0.3,0.95,0])
    return VGroup(body,eye).scale(scale).move_to([x,-0.45,0])


def takeaway():
    lines=["Most cortical interneurons", "start outside the cortex;", "what they read helps steer them."]
    return VGroup(*[T(t,40,TEXT,font=TITLE_FONT) for t in lines]).arrange(DOWN,buff=0.42).move_to([0,0.25,0])


# =========================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Tangential Migration: Interneurons and the Long Way Round"
    TITLE = "Born Outside"


class S01Two(SpokenScene):
    def construct(self):
        g = cortex_strip()
        title = lab("cerebral cortex", TEXT, 30).move_to([0, 3.15, 0])
        self.add(g, title)
        self.at("Some excite", lead=0)
        a = Arrow(g.tris[0].get_center(), g.tris[1].get_center(), buff=0.43, color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        ca = lab("excitatory →", BLUE, 30).move_to([-3.0, -3.45, 0])
        self.play(GrowArrow(a), FadeIn(ca), run_time=0.4)
        self.at("Others inhibit", lead=0)
        src=g.dots[0].get_center()
        target=nearest(src,list(g.tris),1)[0].get_center()
        u=unit(target-src); end=target-u*0.43; perp=np.array([-u[1],u[0],0])*0.23
        bar=VGroup(Line(src+u*0.3,end,color=ORANGE,stroke_width=6),
                   Line(end+perp,end-perp,color=ORANGE,stroke_width=6))
        cb = lab("inhibitory ⊣", ORANGE, 30).move_to([3.0,-3.45,0])
        self.play(Create(bar), FadeIn(cb), run_time=0.4)
        self.finish()


class S02Fifth(SpokenScene):
    def construct(self):
        g = cortex_strip()
        g.scale(0.85).move_to([0,-0.5,0])
        self.add(g)
        big = T("in rodents: about 1 in 5", 44, TEXT, font=TITLE_FONT).move_to([0,3.15,0])
        row = VGroup(*[dot(0.34, GREY, 0.35) for _ in range(5)]).arrange(RIGHT,buff=0.6).move_to([0,2.35,0])
        self.add(row)
        self.at("roughly a fifth",lead=0)
        self.play(FadeIn(big),row[4].animate.set_color(ORANGE).set_fill(ORANGE,0.95),run_time=0.45)
        self.at("inhibitory interneurons",lead=0)
        sub=lab("inhibitory interneurons",ORANGE,30).move_to([0,-3.25,0])
        self.play(FadeIn(sub),*[Indicate(d,scale_factor=1.25) for d in g.dots],run_time=0.5)
        self.finish()


class S03Wall(SpokenScene):
    def construct(self):
        w = wall()
        lw = lab("cortical wall", GREY, 24).move_to([-5.4, 1.9, 0])
        self.play(FadeIn(w), FadeIn(lw), run_time=1.0)
        self.at("excitatory kind")
        starts = [[x, -2.4, 0] for x in FIBX]
        pyr = VGroup(*[tri(0.5).move_to(p) for p in starts])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pyr], lag_ratio=0.15), run_time=0.9)
        self.at("pyramidal neurons")
        lp = lab("pyramidal\nneurons\n(excitatory)", BLUE, 26).move_to([-5.25, -1.9, 0])
        self.play(FadeIn(lp), run_time=0.5)
        self.at("climb straight out")
        fb = fibres()
        lr = lab("radial glial\nfibre", GREY, 24).move_to([5.1, 0.3, 0])
        ar = Arrow(lr.get_left() + LEFT * 0.05, [2.75, 0.3, 0], buff=0.05, color=GREY, stroke_width=3)
        span = DoubleArrow([-4.0, -2.7, 0], [-4.0, 2.9, 0], buff=0, color=GREY, stroke_width=4)
        self.add(fb)
        self.bring_to_back(fb)
        fb.set_opacity(0)
        anims = [fb.animate(run_time=0.6).set_opacity(0.85)]
        for i, p in enumerate(pyr):
            anims.append(lag(0.6 + 0.2 * i, p.animate(run_time=3.0, rate_func=linear).move_to([p.get_center()[0], 2.35, 0])))
        anims.append(lag(1.2, AnimationGroup(FadeIn(lr), GrowArrow(ar))))
        anims.append(lag(3.8, GrowArrow(span)))
        self.play(AnimationGroup(*anims), run_time=4.6)
        self.finish()


def question_group():
    q = T("Where do the inhibitory\nneurons come from?", 48, TEXT, font=TITLE_FONT, line_spacing=0.8).move_to([0, 1.2, 0])
    ds = VGroup(*[dot(0.4, ORANGE, 0.0) for _ in range(6)]).arrange(RIGHT, buff=0.7).move_to([0, -1.6, 0])
    qs = VGroup(*[lab("?", ORANGE, 30).move_to(d) for d in ds])
    return q, ds, qs


class S04Q(SpokenScene):
    def construct(self):
        g,q=question_cortex()
        self.add(g,q)
        self.at("inhibitory neurons",lead=0)
        self.play(*[d.animate.set_fill(ORANGE,0) for d in g.dots],run_time=0.5)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        g,q=question_cortex()
        for d in g.dots: d.set_fill(ORANGE,0)
        self.add(g,q)
        for _ in range(2):
            self.play(*[d.animate.set_stroke(width=5) for d in g.dots],run_time=1.2)
            self.play(*[d.animate.set_stroke(width=2) for d in g.dots],run_time=1.2)
        self.finish()


# ---- hemisphere scenes
class S06Map(SpokenScene):
    def construct(self):
        g=coronal(stage="plain"); tag=plane_tag()
        dl=lab("dorsal",TEXT,28).move_to([0,2.75,0])
        vl=lab("ventral",TEXT,28).move_to([0,-2.95,0])
        lateral=lab("lateral",GREY,26).move_to([5.0,0,0])
        mid=lab("midline",GREY,26).move_to([0,-3.5,0])
        self.add(g,tag,dl,vl,lateral,mid,marker(0))
        self.at("dorsal part",lead=0)
        caps=VGroup(*[Arc(radius=2.0,start_angle=0.15,angle=PI-0.3,color=BLUE,stroke_width=24).stretch(1.2,1).move_to([x,1.55,0]) for x in (-2.05,2.05)])
        self.play(Create(caps),run_time=0.45)
        self.at("the pallium",lead=0)
        pl=lab("pallium",BLUE,32).move_to([-5.05,1.8,0])
        ln=leader(pl.get_right(),np.array([-3.3,2.0,0]))
        self.play(FadeIn(pl),Create(ln),run_time=0.4)
        self.at("forms the cortex",lead=0)
        co=lab("forms cortex",BLUE,28).move_to([5.0,1.8,0])
        self.play(FadeIn(co),run_time=0.35)
        self.finish()


def sec_state(stage="both", swells=(A_LGE, A_MGE)):
    sec = section(stage)
    sw = {a: swell(a) for a in swells}
    return sec, sw


class S07Sub(SpokenScene):
    def construct(self):
        g=coronal(); tag=plane_tag(); mk=marker(0)
        self.add(g,tag,mk)
        self.at("ventral part",lead=0)
        sl=lab("subpallium",ORANGE,32).move_to([4.8,-2.3,0])
        self.play(FadeIn(sl),run_time=0.3)
        self.at("bulges into",lead=0)
        es=eminences()
        self.play(GrowFromCenter(es),run_time=0.45)
        vl=lab("ventricle",TEXT,26).move_to([2.1,0.25,0])
        self.add(vl)
        self.at("as three",lead=0)
        self.remove(vl,sl)
        ng=coronal(True); ne=eminences(True); nt=plane_tag(True)
        self.play(ReplacementTransform(g,ng),ReplacementTransform(es,ne),Transform(tag,nt),
                  mk.plane.animate.move_to([plane_x(1),MK_Y,0]),run_time=0.6)
        self.finish()


class S08Ge(SpokenScene):
    def construct(self):
        g=paired_sections(); ns=source_names()
        self.add(g)
        # Labels connect to the two actual section planes, never a combined ring.
        targets=[g[0][1][0],g[0][1][1],g[1][1][0]]
        for cue,n,e in zip(("lateral","medial","and caudal"),ns,targets):
            self.at(cue,lead=0)
            ln=leader(n.get_top(),e.get_bottom())
            self.play(FadeIn(n),Create(ln),Indicate(e),run_time=0.3)
        self.at("not ganglia",lead=0)
        ng=chip("germinal zones, not ganglia",TEXT,30).move_to([0,-3.2,0])
        self.play(FadeIn(ng),run_time=0.3)
        self.finish()


def eminence_dots(color=TEXT, op=0.9, r=0.09):
    out = {}
    offs = [(-0.27, 0.0), (0.27, 0.0), (0.0, 0.2), (0.0, -0.2), (0.0, 0.0)]
    for a in (A_LGE, A_CGE, A_MGE):
        cen = pol(R_IN - 0.3, a)
        th = np.radians(a - 270)
        ds = VGroup()
        for ox, oy in offs:
            rx, ry = ox * np.cos(th) - oy * np.sin(th), ox * np.sin(th) + oy * np.cos(th)
            ds.add(dot(r, color, op).move_to(cen + np.array([rx, ry, 0])))
        out[a] = ds
    return out


class S09Nursery(SpokenScene):
    def construct(self):
        g,ns,ds=nursery(); self.add(g,ns)
        self.at("germinal zones",lead=0)
        gz=lab("temporary germinal zones",TEXT,30).move_to([0,3.45,0])
        self.play(FadeIn(gz),run_time=0.3)
        self.at("packed with",lead=0)
        self.play(FadeIn(ds),run_time=0.25)
        self.at("dividing progenitors",lead=0)
        title=lab("dividing progenitors",TEXT,30).move_to([0,-3.25,0])
        twins=ds.copy();self.add(twins)
        self.play(FadeIn(title),*[d.animate.shift(LEFT*0.24) for d in ds],
                  *[d.animate.shift(RIGHT*0.24) for d in twins],run_time=0.6)
        self.finish()


class S10Transmit(SpokenScene):
    def construct(self):
        g,ns,ds=nursery();self.add(g,ns,ds)
        pp=VGroup(*[dot(0.19,TEXT).move_to([x,1.65,0]) for x in (-4.47,-1.93,1.93,4.47)])
        self.add(pp)
        self.at("release glutamate",lead=0)
        trs=VGroup(*[tri(0.55).move_to(p) for p in pp])
        gl=lab("pallium: glutamate neurons",BLUE,30).move_to([0,3.45,0])
        self.play(*[ReplacementTransform(p,t) for p,t in zip(pp,trs)],FadeIn(gl),run_time=0.4)
        self.at("GABA",lead=0)
        ga=lab("subpallium: GABA neurons",ORANGE,30).move_to([0,-2.85,0])
        self.play(*[d.animate.set_color(ORANGE).set_fill(ORANGE,0.95) for d in ds],FadeIn(ga),run_time=0.35)
        self.at("main inhibitory transmitter",lead=0)
        cap=lab("the main inhibitory transmitter",TEXT,28).move_to([0,-3.5,0])
        self.play(FadeIn(cap),run_time=0.3)
        self.finish()


def route_points():
    main = [pol(R_IN - 0.3, A_MGE), np.array([0.45, -0.2, 0]), np.array([-0.2, 0.55, 0]), np.array([-0.9, 1.0, 0]),
            np.array([-1.5, 1.25, 0]), pol(2.25, 148)]
    branch = [pol(R_IN - 0.3, A_CGE), np.array([-0.35, -0.4, 0]), np.array([-0.2, 0.55, 0])]
    return main, branch


class S11Reveal(SpokenScene):
    def construct(self):
        g=paired_sections(); self.add(g)
        title=lab("rodents: most cortical interneurons",TEXT,30).move_to([0,3.5,0]);self.add(title)
        dest=lab("pallial wall → cortex",BLUE,28).move_to([0,-3.4,0])
        starts=[[-3.851,-0.523,0],[1.62,-0.34,0]]
        cells=VGroup(*[dot(0.12).move_to(p) for p in starts],
                     dot(0.12).move_to([-3.80,-0.68,0]))
        names=VGroup(lab("MGE",ORANGE,28).move_to([-2.0,-1.7,0]),lab("CGE",ORANGE,28).move_to([3.2,-1.7,0]))
        paths=[]; roads=VGroup()
        for pts in ([starts[0],[-4.9,-0.85,0],[-5.35,0.1,0],[-5.32,0.8,0],[-4.95,1.55,0],[-4.3,1.78,0]],
                    [starts[1],[1.35,-0.55,0],[1.12,0.2,0],[1.25,1.1,0],[1.7,1.85,0],[1.9,1.85,0]],
                    [[-3.80,-0.68,0],[-4.9,-1.05,0],[-5.53,0.1,0],[-5.5,0.8,0],[-5.03,1.72,0],[-4.3,1.94,0]]):
            path=VMobject().set_points_smoothly([np.array(p) for p in pts]);paths.append(path)
            roads.add(DashedVMobject(path,num_dashes=26).set_color(ORANGE).set_stroke(width=3,opacity=0.65))
        # The route and source cells are visible from the first narrated frame.
        self.add(roads,cells)
        self.at("medial",lead=0)
        self.play(FadeIn(names[0]),Create(leader(names[0].get_top(),g[0][1][1].get_bottom())),run_time=0.3)
        self.at("caudal",lead=0)
        self.play(FadeIn(names[1]),Create(leader(names[1].get_top(),g[1][1][0].get_bottom())),run_time=0.3)
        st=lab("striatum (from the LGE)",GREY,28).move_to([-3.4,-2.65,0])
        ln=leader(st.get_top(),g[0][1][0].get_bottom())
        self.play(g[0][1][0].animate.set_opacity(0.3),FadeIn(st),Create(ln),run_time=0.3)
        self.at("they travel",lead=0)
        self.play(FadeIn(dest),*[MoveAlongPath(c,p,rate_func=linear) for c,p in zip(cells,paths)],run_time=1.8)

        self.finish()


def RADIAL():
    t = lab("radial", GREY, 22).move_to([-4.9, -1.2, 0])
    ar = Arrow(t.get_right() + RIGHT * 0.05, [-2.8, -1.2, 0], buff=0.0, color=GREY, stroke_width=2.5,
               max_tip_length_to_length_ratio=0.15)
    return VGroup(t, ar)


def wall_frame(dot_x=None, tri_y=None, tri_op=0.4):
    """Wall with surface, a dotted tangential path, the orange cell and a faint radial climber."""
    w = wall()
    fb = fibres()
    path = DashedLine([-3.2, 0.9, 0], [3.2, 0.9, 0], color=ORANGE, stroke_width=4, dash_length=0.2)
    head = Triangle(fill_color=ORANGE, fill_opacity=1, stroke_width=0).scale(0.14).rotate(-PI / 2).move_to([3.3, 0.9, 0])
    c = dot(0.36, ORANGE).move_to([-3.0 if dot_x is None else dot_x, 0.9, 0])
    t = tri(0.75, BLUE, tri_op).move_to([-2.7, -2.4 if tri_y is None else tri_y, 0])
    g = VGroup(w, fb, path, head, c, t)
    g.c, g.t, g.path, g.head = c, t, path, head
    return g


class S12Name(SpokenScene):
    def construct(self):
        g = wall_frame()
        w, fb = g.submobjects[0], g.submobjects[1]
        self.add(w, fb)
        lr = RADIAL()
        pa = lab("parallel to\nthe surface", TEXT, 28).move_to([5.25, -0.4, 0])
        self.play(Create(g.path), FadeIn(g.head), FadeIn(g.c, scale=0.5), FadeIn(g.t), FadeIn(lr), run_time=0.5)
        self.play(g.c.animate(run_time=2.2, rate_func=linear).move_to([2.7, 0.9, 0]),
                  g.t.animate(run_time=2.2, rate_func=linear).move_to([-2.7, 2.35, 0]),
                  lag(0.4, FadeIn(pa)), run_time=2.2)
        self.at("tangential migration")
        tm = lab("tangential\nmigration", ORANGE, 32, weight=BOLD).move_to([5.25, 0.9, 0])
        self.play(FadeIn(tm, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


class S13Beat(NarratedScene):
    def construct(self):
        g = wall_frame(dot_x=2.7, tri_y=2.35, tri_op=0.45)
        lr = RADIAL()
        tm = lab("tangential\nmigration", ORANGE, 32, weight=BOLD).move_to([5.25, 0.9, 0])
        pa = lab("parallel to\nthe surface", TEXT, 28).move_to([5.25, -0.4, 0])
        self.add(g, lr, tm, pa)
        self.finish()


def card_with_header():
    c = card()
    h = T("THE ONE IDEA", 26, GOLD, weight=BOLD).move_to([0, 1.65, 0])
    return c, h


class S14Idea(SpokenScene):
    def construct(self):
        g = wall_frame(dot_x=2.7, tri_y=2.35, tri_op=0.45)
        lr = RADIAL()
        tm = lab("tangential\nmigration", ORANGE, 32, weight=BOLD).move_to([5.25, 0.9, 0])
        pa = lab("parallel to\nthe surface", TEXT, 28).move_to([5.25, -0.4, 0])
        old = VGroup(g, lr, tm, pa)
        self.add(old)
        c = card().shift(RIGHT * 14)
        t = T("The one idea", 60, TEXT, font=TITLE_FONT).shift(RIGHT * 14)
        self.at("Here is", lead=0.0)
        self.play(FadeOut(old), c.animate.shift(LEFT * 14), t.animate.shift(LEFT * 14), run_time=0.9)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        c, h = card_with_header()
        r = rule_text().move_to([0, -0.2, 0])
        fit(r, max_w=10.8)
        r.set_opacity(0)
        t = T("The one idea", 60, TEXT, font=TITLE_FONT)
        self.add(c, t)
        self.add(r)
        self.play(Transform(t, h), r.words[0].animate.set_opacity(1), run_time=0.45)
        W = r.words
        seq = [("outside", [1]), ("the cortex", [2, 3]), ("steered by", [4, 5]), ("what", [6]),
               ("the cell", [7, 8]), ("can read", [9, 10])]
        for cue, gi in seq:
            self.at(cue, lead=0.05)
            self.play(*[W[i].animate.set_opacity(1) for i in gi], run_time=0.3)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        c, h = card_with_header()
        r = rule_text().move_to([0, -0.2, 0])
        fit(r, max_w=10.8)
        self.add(c, h, r)
        self.finish()


# ---- the road
ROAD = [[-5.0, -1.3, 0], [-4.6, 0.2, 0], [-3.0, 1.0, 0], [-1.4, 0.4, 0], [-0.2, 0.0, 0], [0.6, 0.7, 0],
        [1.5, 2.2, 0], [3.5, 2.2, 0], [6.0, 2.2, 0]]


def road_scene():
    mge = Ellipse(width=1.7, height=1.4, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                  fill_opacity=0.3).move_to([-5.4, -1.9, 0])
    ml = lab("MGE", ORANGE, 24).move_to(mge)
    st = Ellipse(width=3.8, height=2.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                 fill_opacity=0.22).move_to([-3.0, -1.5, 0])
    sl = lab("striatum", GREY, 24).move_to(st)
    cx = Rectangle(width=5.9, height=4.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                   fill_opacity=0.08).move_to([3.65, 1.3, 0])
    cl = lab("cortex", BLUE, 24).move_to([5.5, -0.4, 0])
    lane = RoundedRectangle(corner_radius=0.3, width=5.0, height=0.9, stroke_color=ORANGE, stroke_width=1.5,
                            stroke_opacity=0.5, fill_color=ORANGE, fill_opacity=0.15).move_to([3.9, 2.2, 0])
    path = VMobject().set_points_smoothly([np.array(p, dtype=float) for p in ROAD])
    road = DashedVMobject(path, num_dashes=60).set_color(TEXT).set_stroke(width=4)
    return VGroup(mge, ml, st, sl, cx, cl, lane), road, path


def prop_near(path, target):
    best, bp = 9, 0
    for i in range(0, 1001):
        p = i / 1000
        d = np.linalg.norm(path.point_from_proportion(p) - np.array(target, dtype=float))
        if d < best:
            best, bp = d, p
    return bp


def diamond(size=0.3, color=TEAL, filled=True):
    d = Square(side_length=size * 1.4, stroke_color=color, stroke_width=3, fill_color=color,
               fill_opacity=0.9 if filled else 0.0).rotate(PI / 4)
    return d


class S17Cue(SpokenScene):
    def construct(self):
        title=lab("two turns along the route",TEXT,34).move_to([0,3.3,0])
        st=Ellipse(width=3.0,height=1.8,color=GREY,fill_color=GREY,fill_opacity=0.25).move_to([-3.4,-0.5,0])
        sl=lab("striatum",TEXT,28).move_to(st)
        cx=RoundedRectangle(width=5.3,height=4.3,corner_radius=0.2,color=BLUE,fill_color=BLUE,fill_opacity=0.08).move_to([3.4,0.1,0])
        lane=RoundedRectangle(width=4.6,height=0.95,corner_radius=0.3,color=ORANGE,fill_color=ORANGE,fill_opacity=0.15).move_to([3.4,1.2,0])
        labels=VGroup(lab("turn 1: round the striatum",TEXT,28).move_to([-3.4,2.55,0]),
                      lab("turn 2: into a lane",TEXT,28).move_to([3.4,2.55,0]),lab("cortex",BLUE,28).move_to([4.9,-1.6,0]))
        p1=VMobject().set_points_smoothly([np.array(p) for p in [[-5.3,-2.1,0],[-5.4,0.1,0],[-4.5,1.2,0],[-2.5,1.5,0],[-1.2,1.5,0]]])
        p2=VMobject().set_points_smoothly([np.array(p) for p in [[1.35,-1.5,0],[1.4,0.1,0],[2.2,1.2,0],[4.8,1.2,0]]])
        roads=VGroup(*[DashedVMobject(p,num_dashes=25).set_stroke(TEXT,4) for p in (p1,p2)])
        self.add(title,st,sl,cx,lane,labels,roads)
        c1=tabbed(0.32,RIGHT).shift([-4.4,1.5,0]);c2=tabbed(0.32,RIGHT).shift([2.5,1.2,0])
        c1.tab.set_opacity(0);c2.tab.set_opacity(0);self.add(c1,c2)
        self.at("road holds a cue",lead=0)
        repel=Triangle(color=TEAL,fill_color=TEAL,fill_opacity=1).scale(0.20).rotate(-PI/2)
        hold=diamond(0.25)
        # Contact is edge-to-edge with each leading receptor, above the path.
        repel.next_to(c1.tab,RIGHT,buff=0)
        hold.next_to(c2.tab,RIGHT,buff=0)
        tags=VGroup(lab("repel",TEAL,28).move_to([-1.4,0.8,0]),lab("hold",TEAL,28).move_to([3.3,0.15,0]),
                    lab("cue on the road",TEAL,30).move_to([-3.2,-2.9,0]))
        self.play(FadeIn(repel),FadeIn(hold),FadeIn(tags),run_time=0.4)
        self.at("cell carries",lead=0)
        rl=lab("receptor on the cell",PURPLE,30).move_to([3.1,-2.9,0])
        self.play(c1.tab.animate.set_opacity(1),c2.tab.animate.set_opacity(1),FadeIn(rl),run_time=0.35)
        self.play(Indicate(c1.tab,color=PURPLE),Indicate(c2.tab,color=PURPLE),run_time=0.7)
        self.finish()


class S18Either(SpokenScene):
    def construct(self):
        stage,cells,cues=fault_panels(tall=True)
        cues[1].set_fill(opacity=0).set_stroke(RED,opacity=0.45)
        self.add(stage,cells,cues)
        self.at("a fault can sit",lead=0)
        hl=lab("a fault in the cell",TEXT,30).move_to([-3.5,2.5,0])
        self.play(FadeIn(hl),cells[0].animate.shift(RIGHT*0.35+UP*0.25),run_time=0.4)
        self.at("cannot answer",lead=0)
        mark=lab("×",RED,60).move_to(cells[0].tab)
        stuck=lab("stalled: cannot answer",RED,28).move_to([-3.5,-2.05,0])
        trail=VGroup(*[dot(0.6,ORANGE).set_opacity(op).move_to([-5.35+i*0.4,-1.3+i*0.28,0])
                       for i,op in enumerate((0.07,0.13,0.22))])
        stop=Line(cells[0].get_right()+RIGHT*0.12+DOWN*0.5,
                  cells[0].get_right()+RIGHT*0.12+UP*0.5,color=RED,stroke_width=7)
        self.add(trail)
        self.play(FadeIn(mark),Create(stop),FadeIn(stuck),run_time=0.3)
        self.at("Or it can sit",lead=0)
        hr=lab("a fault in the road",TEXT,30).move_to([3.5,2.5,0])
        self.play(FadeIn(hr),cells[1].animate.shift(RIGHT*0.35+UP*0.25),run_time=0.35)
        self.at("lacks the cue",lead=0)
        ghost=diamond(0.55,RED,False).move_to(cues[1])
        nr=lab("stalled: cue missing",RED,28).move_to([3.5,-2.05,0])
        sr=stop.copy().shift(RIGHT*7)
        trail_r=trail.copy().shift(RIGHT*7)
        self.add(trail_r)
        self.play(ReplacementTransform(cues[1],ghost),FadeIn(nr),Create(sr),run_time=0.3)
        self.finish()


class S18bSwap(SpokenScene):
    def construct(self):
        stage,cells,cues=fault_panels();self.add(stage,cells,cues)
        labels=VGroup(lab("cell?",TEXT,32).move_to([-3.5,2.5,0]),lab("road?",TEXT,32).move_to([3.5,2.5,0]))
        self.add(labels)
        self.at("Swapping tissue",lead=0)
        # The open central gutter has no divider, titles or cells beneath the arrows.
        a=CurvedArrow([-0.65,1.2,0],[0.65,1.2,0],angle=-PI/2,color=TEXT,stroke_width=5)
        b=CurvedArrow([0.65,-0.2,0],[-0.65,-0.2,0],angle=-PI/2,color=TEXT,stroke_width=5)
        self.play(Create(a),Create(b),run_time=0.4)
        self.at("tells you which",lead=0)
        tag=lab("which one?",YELLOW,34).move_to([0,-2.95,0])
        ch=lab("answered in chapter two",TEXT,30).move_to([0,-3.55,0])
        self.play(FadeIn(tag),FadeIn(ch),run_time=0.35)
        self.finish()


class S19Lane(SpokenScene):
    def construct(self):
        cx=RoundedRectangle(width=12.4,height=6.5,corner_radius=0.2,color=BLUE,fill_color=BLUE,fill_opacity=0.06)
        lanes=VGroup(*[RoundedRectangle(width=11.3,height=1.4,corner_radius=0.35,color=ORANGE,fill_color=ORANGE,fill_opacity=0.15).move_to([0,y,0]) for y in (1.45,-1.1)])
        labels=VGroup(lab("cortex",BLUE,30).move_to([-5.3,2.9,0]),
                      lab("superficial stream",TEXT,28).move_to([0,2.5,0]),lab("deep stream",TEXT,28).move_to([0,-0.1,0]))
        cells=VGroup(*[tabbed(0.35,RIGHT).shift([x,y,0]) for y in (1.45,-1.1) for x in (-4,-1.4,1.2,3.8)])
        self.add(cx,lanes,labels,cells)
        self.at("chemokine signal",lead=0)
        cues=VGroup(*[diamond(0.16).move_to([x,y+0.38,0]) for y in (1.45,-1.1) for x in (-3,-0.4,2.2,4.8)])
        sg=lab("chemokine signal",TEAL,28).move_to([0,-2.25,0])
        self.play(FadeIn(cues),FadeIn(sg),run_time=0.3)
        self.at("helps keep",lead=0)
        lb=lab("needed to help hold cells in the lane",TEXT,28).move_to([0,-2.95,0])
        more=lab("one of several cues",TEXT,28).move_to([0,-3.55,0])
        self.play(*[c.animate.shift(RIGHT*0.6) for c in cells],FadeIn(lb),FadeIn(more),run_time=0.7)
        self.finish()


class S20Test(SpokenScene):
    def construct(self):
        c,h=card_with_header();r=rule_text().move_to([0,-0.2,0]);self.add(c,h,r)
        # The full rule remains readable through the final spoken word.
        self.at("hold on",lead=0)
        self.wait(max(0.05,self.narration_s-self.elapsed()))
        badge=lab("Born outside; steered by what the cell can read.",TEXT,28).move_to([0,3.15,0])
        self.play(FadeOut(c),FadeOut(h),Transform(r,badge),run_time=0.4)
        self.finish()


class S21Scope(SpokenScene):
    def construct(self):
        badge=lab("Born outside; steered by what the cell can read.",TEXT,28).move_to([0,3.15,0])
        a=embryo(0,1.3)
        title=lab("One limit: embryonic rodents",TEXT,36).move_to([0,2.25,0])
        label=lab("mouse and rat embryos",ORANGE,34).move_to([0,-3.1,0])
        self.add(badge,title,a,label)

        self.finish()


class S22Human(SpokenScene):
    def construct(self):
        top=lab("HUMAN · fetal forebrain",TEXT,34).move_to([0,3.2,0])
        # A distinct hemisphere profile. The folds are schematic, not a fetal age claim.
        brain=VMobject(stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=0.16)
        pts=[[-4,-1.8,0],[-4.6,-0.3,0],[-4.0,1.4,0],[-2.4,2.3,0],[0.1,2.45,0],[2.2,1.65,0],[3,0.1,0],[2.5,-1.6,0],[0.4,-2.1,0],[-1.4,-1.6,0],[-4,-1.8,0]]
        brain.set_points_smoothly([np.array(p) for p in pts])
        vent=Ellipse(width=3.9,height=1.3,color=GREY,fill_color=LUMEN,fill_opacity=1).rotate(0.15).move_to([-0.7,-0.4,0])
        ge=Ellipse(width=1.7,height=0.8,color=ORANGE,fill_color=ORANGE,fill_opacity=0.3).move_to([-1.0,-1.2,0])
        folds=VGroup()
        for fp in ([[-3.8,0.2,0],[-3.25,0.75,0],[-3.3,1.2,0],[-2.7,1.65,0]],
                   [[-2.35,2.12,0],[-2.0,1.55,0],[-2.25,1.1,0],[-1.7,0.65,0]],
                   [[-0.8,2.25,0],[-1.0,1.6,0],[-0.45,1.25,0],[-0.6,0.65,0]],
                   [[0.5,2.1,0],[0.2,1.6,0],[0.75,1.2,0],[0.65,0.6,0]],
                   [[1.8,1.5,0],[1.3,1.0,0],[1.8,0.45,0],[2.4,0.25,0]],
                   [[-3.65,-0.8,0],[-3.0,-1.15,0],[-2.5,-0.85,0]],
                   [[1.0,-1.75,0],[1.55,-1.1,0],[2.15,-1.05,0]]):
            folds.add(VMobject(stroke_color=BLUE,stroke_width=3).set_points_smoothly([np.array(v) for v in fp]))
        self.add(top,brain,folds,vent,ge)
        self.at("eminences are seen",lead=0)
        main=lab("eminences:\nmain source",ORANGE,30).move_to([-2.2,-2.85,0])
        l1=leader(main.get_top(),ge.get_left())
        self.play(FadeIn(main),Create(l1),run_time=0.35)
        self.at("cortical progenitors",lead=0)
        region=Arc(radius=2.1,start_angle=0.5,angle=1.5,color=ORANGE,stroke_width=10).move_to([-0.8,1.65,0])
        lc=lab("cortical wall:\nalso some\n(share under study)",ORANGE,26).move_to([4.8,0.15,0])
        l2=leader(lc.get_left(),region.get_start())
        self.play(Create(region),FadeIn(lc),Create(l2),run_time=0.3)
        self.finish()


class S24Take(SpokenScene):
    def construct(self):
        t=takeaway();self.add(t)
        self.at("outside the cortex",lead=0)
        self.play(t[1].animate.set_color(ORANGE),run_time=0.35)
        self.at("what they can read",lead=0)
        self.play(t[2].animate.set_color(PURPLE),run_time=0.35)
        self.finish()


class S25End(EndCard):
    LINE = "Most cortical interneurons start outside cortex; what they read helps steer them."
    def construct(self):
        t=takeaway();t[1].set_color(ORANGE);t[2].set_color(PURPLE)
        sub=lab("biochemistrypedia.com",TEAL,26).move_to([0,-2.4,0])
        self.add(t,sub);self.finish()

