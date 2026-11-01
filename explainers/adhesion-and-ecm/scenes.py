"""Adhesion and the extracellular matrix: two grips, each wired to a cable  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = calcium
  BLUE   = cadherin (the outer arms and the tail)
  PURPLE = integrin (alpha and beta lobes)
  ORANGE = the matrix (mesh, fibronectin, RGD tag, laminin, basement membrane)
  TEAL   = adaptor proteins inside the cell (catenins, p120, talin, vinculin, plectin)
  GREEN  = actin filaments
  PINK   = keratin filaments
  GOLD   = force and myosin
  RED    = blocked (myosin crossed out)
  GREY   = cells, membranes, labels
"""


import numpy as np


from bp_style import *  # noqa: F401,F403


PURPLE = "#B58CD9"


ORANGE = "#F29E4C"


PINK = "#E87DB0"


def bchip(text, color=BLUE, size=24, pad=0.14):
    c = chip(text, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def cell_rect(cx, cy, w, h, op=0.16):
    return RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=op).move_to([cx, cy, 0])


def mem_v(x, y0, y1, w=0.22):
    return RoundedRectangle(corner_radius=0.08, width=w, height=y1 - y0, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([x, (y0 + y1) / 2, 0])


def mem_h(y, x0=-6.3, x1=6.3, h=0.22):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([(x0 + x1) / 2, y, 0])


def beaded(p0, p1, color=GREEN, spacing=0.3, r=0.1):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    n = int(np.linalg.norm(p1 - p0) / spacing) + 1
    ln = Line(p0, p1, color=color, stroke_width=3)
    dots = [Dot(p0 + (p1 - p0) * i / max(n - 1, 1), radius=r, color=color) for i in range(n)]
    return VGroup(ln, *dots)


def rods(p0, p1, color=PINK, seg=0.34):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    n = int(np.linalg.norm(p1 - p0) / seg)
    out = []
    for i in range(n):
        out.append(RoundedRectangle(corner_radius=0.05, width=seg - 0.05, height=0.15, stroke_width=0,
                                    fill_color=color, fill_opacity=0.95).move_to(p0 + (p1 - p0) * (i + 0.5) / n))
    return VGroup(*out)


def link(a, b, color=TEAL, w=3):
    return Line(a, b, color=color, stroke_width=w)


def lobe(x, y, label, h=1.7, w=0.5):
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=PURPLE, stroke_width=3,
                         fill_color=PURPLE, fill_opacity=0.35).move_to([x, y, 0])
    t = T(label, 24, TEXT).move_to(r)
    return VGroup(r, t)


MEM_X = 2.0


def arm_pts(side, y, bend, sp=0.42):
    """side -1 = left cell, +1 = right cell. bend 0 = stiff and straight, >0 = limp, drooping."""
    dx = -side
    p = np.array([side * MEM_X + dx * 0.15, y, 0.0])
    pts = [p.copy()]
    for k in range(1, 5):
        ang = -bend * k
        p = p + sp * np.array([dx * np.cos(ang), np.sin(ang), 0.0])
        pts.append(p.copy())
    return pts


def arm_mob(pts):
    lines = VGroup(*[Line(pts[i], pts[i + 1], color=BLUE, stroke_width=4) for i in range(4)])
    beads = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.24, height=0.24, stroke_color=BLUE,
                                      stroke_width=2, fill_color=BLUE, fill_opacity=0.5).move_to(p) for p in pts])
    return VGroup(lines, beads)


def ca_dots(pts):
    return VGroup(*[Dot((pts[i] + pts[i + 1]) / 2, radius=0.08, color=YELLOW) for i in range(4)])


YS = [1.7, 0.0, -1.7]


LIMP = 0.3


def junction_cells():
    a = cell_rect(-4.15, -0.1, 4.3, 5.8)
    b = cell_rect(4.15, -0.1, 4.3, 5.8)
    ma = mem_v(-MEM_X, -3.0, 2.8)
    mb = mem_v(MEM_X, -3.0, 2.8)
    return a, b, ma, mb


def stiff_arms(ys=YS):
    out = {}
    for y in ys:
        out[(y, -1)] = arm_mob(arm_pts(-1, y, 0.0))
        out[(y, 1)] = arm_mob(arm_pts(1, y, 0.0))
    return out


def ca_all(ys=YS):
    g = VGroup()
    for y in ys:
        g.add(ca_dots(arm_pts(-1, y, 0.0)), ca_dots(arm_pts(1, y, 0.0)))
    return g


class S00Title(TitleCard):
    LESSON = "Adhesion and the extracellular matrix"
    TITLE = "Two Grips, Each Wired to a Cable"


def mesh_tiles(x0=-6.3, x1=6.3, y0=-3.0, y1=-1.75, tw=0.9):
    tiles = []
    x = x0
    while x + tw <= x1 + 1e-6:
        c = x + tw / 2
        g = VGroup(Line([x, y0, 0], [x + tw, y1, 0], color=ORANGE, stroke_width=2.5),
                   Line([x, y1, 0], [x + tw, y0, 0], color=ORANGE, stroke_width=2.5))
        g.cx = c
        tiles.append(g)
        x += tw
    return tiles


def focal_chain(x0=0.0, with_labels=True):
    """integrin + fibronectin + talin + vinculin + actin, built at centre x0."""
    d = {}
    d["alpha"] = lobe(x0 - 0.3, -0.9, "α")
    d["beta"] = lobe(x0 + 0.3, -0.9, "β")
    d["fn_beads"] = VGroup(*[Dot([x0, y, 0], radius=0.09, color=ORANGE) for y in (-2.95, -2.7, -2.45)])
    d["fn_line"] = Line([x0, -3.0, 0], [x0, -2.25, 0], color=ORANGE, stroke_width=3)
    d["rgd"] = bchip("RGD", ORANGE, 22, 0.1).move_to([x0, -2.0, 0])
    d["talin"] = bchip("talin", TEAL, 24).move_to([x0 + 0.65, 0.5, 0])
    d["actin"] = beaded([x0 - 2.8, 2.2, 0], [x0 + 2.8, 2.2, 0], GREEN)
    d["tlink"] = link([x0 + 0.65, 0.5 + d["talin"].height / 2, 0], [x0 + 0.65, 2.2, 0])
    d["bt"] = link([x0 + 0.3, -0.05, 0], [x0 + 0.3, 0.5 - d["talin"].height / 2, 0])
    d["vinc"] = bchip("vinculin", TEAL, 24).move_to([x0 + 2.6, 1.3, 0])
    d["vlink"] = VGroup(link([x0 + 2.6 - d["vinc"].width / 2, 1.3, 0], [x0 + 0.65 + d["talin"].width / 2, 0.5, 0]),
                        link([x0 + 2.6, 1.3 + d["vinc"].height / 2, 0], [x0 + 2.6, 2.2, 0]))
    d["l_int"] = T("integrin", 26, PURPLE).move_to([x0 - 1.7, -0.25, 0])
    d["l_fn"] = btext("fibronectin", 24, ORANGE).move_to([x0 + 1.45, -2.55, 0])
    d["l_act"] = T("actin", 26, GREEN).move_to([x0 - 2.2, 2.75, 0])
    return d


def rod_row(unf=(), y=0.0, n=13, ew=0.55, uw=1.45, gap=0.07, h=0.9):
    widths = [uw if i in unf else ew for i in range(n)]
    total = sum(widths) + gap * (n - 1)
    x = -total / 2
    items = []
    for i, w in enumerate(widths):
        hh = 0.12 if i in unf else h
        r = RoundedRectangle(corner_radius=min(0.08, hh / 2), width=w, height=hh, stroke_color=TEAL, stroke_width=2.5,
                             fill_color=TEAL, fill_opacity=0.8 if i in unf else 0.3).move_to([x + w / 2, y, 0])
        items.append(r)
        x += w + gap
    g = VGroup(*items)
    g.total = total
    return g


UNF = (2, 6, 10)


class S07End(EndCard):
    LINE = "Integrins grip the matrix, cadherins grip neighbours; both wire to the cytoskeleton."


# Rebuilt beats for the checked Kokoro narration. All diagrams are schematic.
def clear_scene(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.35)


def heading(text, color=TEXT):
    return T(text, 30, color).move_to([0, 3.15, 0])


def simple_attachment(x, keratin=False):
    """Two-column comparison, with unscaled readable labels."""
    filament = rods([x-2.3, 2.1, 0], [x+2.3, 2.1, 0]) if keratin else beaded([x-2.3,2.1,0],[x+2.3,2.1,0])
    name = T('keratin' if keratin else 'actin',24,PINK if keratin else GREEN).move_to([x,2.65,0])
    adaptor = bchip('plectin' if keratin else 'talin / vinculin',TEAL,22).move_to([x,.85,0])
    receptor = bchip('integrin α6β4' if keratin else 'integrin',PURPLE,22).move_to([x,-.65,0])
    ligand = bchip('laminin-332' if keratin else 'fibronectin',ORANGE,22).move_to([x,-2.05,0])
    connectors = VGroup(link([x,2.1,0],adaptor.get_top()),link(adaptor.get_bottom(),receptor.get_top()),link(receptor.get_bottom(),ligand.get_top(),ORANGE))
    return VGroup(filament,name,adaptor,receptor,ligand,connectors)


class S03Integrin(SpokenScene):
    def construct(self):
        cell=cell_rect(0,1.25,12.4,4.2)
        mem=mem_h(-.9)
        mesh=VGroup(*mesh_tiles())
        d=focal_chain()
        mat=T('extracellular matrix',26,ORANGE).move_to([-3.7,-3.35,0])
        self.at('Integrins connect cells')
        self.play(FadeIn(cell),FadeIn(mem),FadeIn(mesh),FadeIn(d['alpha']),FadeIn(d['beta']),FadeIn(d['l_int']),run_time=.6)
        self.at('extracellular matrix')
        self.play(FadeIn(mat),Indicate(mesh,color=ORANGE,scale_factor=1.02),run_time=.65)
        generic=VGroup(link([.3,-.05,0],[.3,2.2,0]),d['actin'],T('cytoskeleton',26,GREEN).move_to([-3.9,2.7,0]))
        self.at('link to the cytoskeleton')
        self.play(FadeIn(generic),run_time=.65)
        signal=VGroup(arr([1,-.65,0],[3,1,0],TEAL),T('signal',24,TEAL).move_to([3.7,1.1,0]))
        self.at('send signals')
        self.play(FadeIn(signal),run_time=.5)
        pull=arr([-2.5,-2.4,0],[-4.7,-2.4,0],GOLD,w=8)
        self.at('a pull outside')
        self.play(GrowArrow(pull),run_time=.5)
        self.at('own filaments')
        self.play(Indicate(generic,color=GOLD,scale_factor=1.03),run_time=.65)
        self.at('Each integrin pairs')
        self.play(FadeOut(signal),FadeOut(pull),FadeOut(generic),FadeOut(mat),FadeOut(mesh),run_time=.4)
        self.at('an alpha subunit')
        self.play(Indicate(d['alpha'],color=PURPLE),run_time=.5)
        self.at('a beta subunit')
        self.play(Indicate(d['beta'],color=PURPLE),run_time=.5)
        self.at('Many recognize')
        self.play(FadeIn(VGroup(d['fn_line'],d['fn_beads'],d['rgd'],d['l_fn'])),run_time=.7)
        self.at('Talin binds')
        self.play(FadeIn(d['talin']),Create(d['bt']),run_time=.6)
        self.at('links it to actin')
        self.play(FadeIn(d['actin']),Create(d['tlink']),FadeIn(d['l_act']),run_time=.6)
        self.at('Vinculin reinforces')
        self.play(FadeIn(d['vinc']),Create(d['vlink']),run_time=.65)
        self.at('These complexes gather')
        clear_scene(self)
        culture=cell_rect(0,1,11,3.5)
        base=VGroup(*mesh_tiles(-6.3,6.3,-2.6,-1.6))
        clusters=VGroup(*[VGroup(*[RoundedRectangle(width=.22,height=.65,corner_radius=.07,color=PURPLE,fill_opacity=.4).move_to([x+dx,-.85,0]) for dx in (-.3,0,.3)]) for x in (-3.5,0,3.5)])
        cables=VGroup(*[beaded([x-1,1.2,0],[x+1,1.2,0]) for x in (-3.5,0,3.5)])
        ties=VGroup(*[link([x,1.2,0],[x,-.5,0]) for x in (-3.5,0,3.5)])
        self.play(FadeIn(culture),FadeIn(base),FadeIn(clusters),FadeIn(cables),FadeIn(ties),FadeIn(heading('cultured cell',GREY)),run_time=.6)
        self.at('focal adhesions')
        self.play(FadeIn(T('focal adhesions',28,PURPLE).move_to([0,-3.15,0])),Indicate(clusters,color=PURPLE),run_time=.6)
        self.finish()


class S04Exception(SpokenScene):
    def construct(self):
        left=simple_attachment(-3.3)
        self.at('Not every integrin')
        self.play(FadeIn(left),FadeIn(T('focal adhesion',24,GREY).move_to([-3.3,3.25,0])),run_time=.5)
        self.at('pin basal skin cells')
        right=simple_attachment(3.3,True)
        cell=cell_rect(3.3,.65,5.8,4.8)
        title=T('basal skin cell',24,GREY).move_to([3.3,3.25,0])
        band=RoundedRectangle(width=5.8,height=.38,corner_radius=.05,color=ORANGE,fill_opacity=.25).move_to([3.3,-2.8,0])
        bm=T('basement membrane',22,ORANGE).move_to([3.3,-3.35,0])
        self.play(FadeIn(cell),FadeIn(title),FadeIn(band),FadeIn(bm),run_time=.6)
        self.at('Integrin alpha')
        self.play(FadeIn(right[3]),run_time=.5)
        self.at('binds laminin')
        self.play(FadeIn(right[4]),Create(right[5][2]),run_time=.5)
        self.at('connects through plectin')
        self.play(FadeIn(right[2]),Create(right[5][1]),run_time=.6)
        self.at('keratin filaments')
        self.play(FadeIn(right[0]),FadeIn(right[1]),Create(right[5][0]),FadeIn(btext('hemidesmosome',22,GREY).move_to([4.85,0,0])),run_time=.65)
        self.finish()
        self.wait(1.5)


class S01Calcium(SpokenScene):
    def construct(self):
        a,b,ma,mb=junction_cells()
        cells=VGroup(a,ma,b,mb)
        arms=VGroup(*stiff_arms().values())
        calcium=ca_all()
        self.at('The other grip')
        self.play(FadeIn(cells),FadeIn(arms),FadeIn(heading('neighbouring epithelial cells',GREY)),run_time=.5)
        self.at('need calcium')
        label=T('cadherin + calcium',26,BLUE).move_to([0,-3.45,0])
        self.play(FadeIn(calcium),FadeIn(label),Indicate(arms,color=BLUE,scale_factor=1.03),run_time=.6)
        self.at('Remove calcium')
        limp=VGroup(*[arm_mob(arm_pts(s,y,LIMP)) for y in YS for s in (-1,1)])
        self.play(FadeOut(calcium),Transform(arms,limp),Transform(label,T('calcium removed',26,YELLOW).move_to(label)),run_time=.65)
        self.at('they let go')
        self.play(a.animate.shift(LEFT*.4),ma.animate.shift(LEFT*.4),b.animate.shift(RIGHT*.4),mb.animate.shift(RIGHT*.4),*[m.animate.shift(LEFT*.4 if i%2==0 else RIGHT*.4) for i,m in enumerate(arms)],run_time=.65)
        self.at('Put it back')
        self.play(FadeIn(calcium),Transform(label,T('calcium restored',26,YELLOW).move_to(label)),run_time=.45)
        self.at('knit together again')
        self.play(a.animate.shift(RIGHT*.4),ma.animate.shift(RIGHT*.4),b.animate.shift(LEFT*.4),mb.animate.shift(LEFT*.4),Transform(arms,VGroup(*stiff_arms().values())),run_time=.7)
        self.finish()


class S02Cadherin(SpokenScene):
    def construct(self):
        a,b,ma,mb=junction_cells()
        arms=VGroup(*stiff_arms((0.,)).values())
        tails=VGroup(*[Line([s*2,0,0],[s*2.65,0,0],color=BLUE,stroke_width=4) for s in (-1,1)])
        self.at('A classical')
        self.play(FadeIn(VGroup(a,b,ma,mb,arms)),FadeIn(heading('classical cadherin',BLUE)),run_time=.5)
        self.at('crosses the membrane once')
        self.play(Create(tails),run_time=.55)
        self.at('the same kind')
        self.play(Indicate(arms,color=BLUE,scale_factor=1.04),run_time=.55)
        betas=VGroup(*[bchip('β-catenin',TEAL,24).move_to([s*3.6,0,0]) for s in (-1,1)])
        alphas=VGroup(*[bchip('α-catenin',TEAL,24).move_to([s*3.6,-1.15,0]) for s in (-1,1)])
        ba=VGroup(*[link([s*3.6,-.3,0],[s*3.6,-.85,0]) for s in (-1,1)])
        acts=VGroup(*[beaded([s*2.5,-2.35,0],[s*5.9,-2.35,0]) for s in (-1,1)])
        aa=VGroup(*[link([s*3.6,-1.45,0],[s*3.6,-2.35,0]) for s in (-1,1)])
        self.at('binds its tail')
        self.play(FadeIn(betas),run_time=.5)
        self.at('and recruits')
        self.play(FadeIn(alphas),Create(ba),run_time=.5)
        self.at('couples the junction to actin')
        self.play(FadeIn(acts),Create(aa),FadeIn(T('actin',26,GREEN).move_to([0,-3,0])),run_time=.65)
        self.at('These contacts gather')
        clear_scene(self)
        cells=VGroup(cell_rect(-3,0,5.6,4.3),cell_rect(3,0,5.6,4.3))
        belt=VGroup(*[VGroup(Line([-.45,y,0],[.45,y,0],color=BLUE,stroke_width=7),Line([-4.9,y,0],[-.45,y,0],color=GREEN,stroke_width=3),Line([.45,y,0],[4.9,y,0],color=GREEN,stroke_width=3)) for y in (-.55,0,.55)])
        self.play(FadeIn(cells),FadeIn(belt),FadeIn(heading('adherens junction',BLUE)),run_time=.65)
        self.finish()


class SMatrix(SpokenScene):
    def construct(self):
        self.at('What does the matrix')
        mesh=VGroup(*mesh_tiles(-6.3,6.3,-2.5,2.4))
        self.play(FadeIn(mesh),FadeIn(heading('extracellular matrix',ORANGE)),run_time=.5)
        self.at('Collagen cables')
        clear_scene(self)
        cables=VGroup(*[Line([-4.4,y,0],[4.4,y,0],color=ORANGE,stroke_width=7) for y in (-.25,0,.25)])
        pulls=VGroup(arr([-4.5,0,0],[-6,0,0],GOLD),arr([4.5,0,0],[6,0,0],GOLD))
        self.play(Create(cables),FadeIn(heading('collagen cables',ORANGE)),FadeIn(pulls),FadeIn(T('resist pulling',26,GOLD).move_to([0,-1.8,0])),run_time=.6)
        self.at('Elastic fibers')
        clear_scene(self)
        elastic=VMobject(color=ORANGE,stroke_width=6).set_points_smoothly([[x,.35*np.sin(x*3),0] for x in np.linspace(-3,3,60)])
        self.play(Create(elastic),FadeIn(heading('elastic fibres',ORANGE)),run_time=.45)
        self.at('stretch and recoil')
        self.play(elastic.animate.stretch(1.7,0),rate_func=there_and_back,run_time=1.1)
        self.at('makes networks')
        clear_scene(self)
        net=VGroup(*mesh_tiles(-5.4,5.4,-2.2,-.6))
        grip=VGroup(lobe(-.3,.25,'α'),lobe(.3,.25,'β'))
        self.play(FadeIn(net),FadeIn(grip),FadeIn(heading('fibronectin network',ORANGE)),run_time=.6)
        self.at('Basement membranes')
        clear_scene(self)
        top=VGroup(*mesh_tiles(-5.4,5.4,.25,1.15))
        bottom=VGroup(*mesh_tiles(-5.4,5.4,-1.15,-.25))
        ties=VGroup(*[link([x,-.25,0],[x,.25,0],ORANGE) for x in (-4,-2,0,2,4)])
        labs=VGroup(T('laminin network',26,ORANGE).move_to([0,1.9,0]),T('type IV collagen network',26,ORANGE).move_to([0,-1.9,0]))
        self.play(FadeIn(top),FadeIn(bottom),Create(ties),FadeIn(labs),FadeIn(heading('basement membrane: a thin sheet',ORANGE)),run_time=.65)
        self.at('Proteoglycans draw in water')
        clear_scene(self)
        gel=RoundedRectangle(width=8,height=3.2,corner_radius=.4,color=ORANGE,fill_opacity=.15)
        pg=VGroup(*[VGroup(Line([x,-1,0],[x,1,0],color=ORANGE,stroke_width=5),*[Line([x-.35,y,0],[x+.35,y,0],color=ORANGE,stroke_width=3) for y in (-.6,0,.6)]) for x in (-2,0,2)])
        water=VGroup(*[bchip('water',GREY,22).move_to([x,y,0]) for x,y in ((-5,1),(5,-1))])
        self.play(FadeIn(gel),FadeIn(pg),FadeIn(water),FadeIn(heading('proteoglycan gel',ORANGE)),run_time=.5)
        self.play(water[0].animate.move_to([-1,.3,0]),water[1].animate.move_to([1,-.3,0]),run_time=.65)
        self.at('resist compression')
        arrows=VGroup(arr([0,2.6,0],[0,1.65,0],GOLD),arr([0,-2.6,0],[0,-1.65,0],GOLD))
        self.play(FadeIn(arrows),run_time=.5)
        self.at('helps keep the matrix hydrated')
        ha=T('hyaluronan: hydration',26,ORANGE).move_to([0,-3.15,0])
        self.play(FadeIn(ha),Indicate(gel,color=ORANGE,scale_factor=1.03),run_time=.6)
        self.at('also stores growth factors')
        clear_scene(self)
        net=VGroup(*mesh_tiles(-5.4,5.4,-1.7,1))
        factors=VGroup(*[bchip('growth factor',TEAL,22).move_to([x,-.35,0]) for x in (-3,0,3)])
        self.play(FadeIn(net),FadeIn(factors),FadeIn(heading('stored growth factors',TEAL)),run_time=.6)
        self.at('cut or pulled')
        self.play(net.animate.stretch(1.1,0),factors.animate.shift(UP*2),run_time=.7)
        self.at('mechanical support')
        self.play(FadeIn(T('mechanical support',26,ORANGE).move_to([-3,-3,0])),run_time=.45)
        self.at('biochemical cues')
        self.play(FadeIn(T('biochemical cues',26,TEAL).move_to([3,-3,0])),run_time=.45)
        self.finish()


class S05Talin(SpokenScene):
    def construct(self):
        self.at('Some of these connections')
        d=simple_attachment(-2.6)
        self.play(FadeIn(d),run_time=.5)
        myosin=bchip('myosin II',GOLD,26).move_to([3,2.1,0])
        pull=arr([.2,2.1,0],[1.8,2.1,0],GOLD,w=8)
        self.at('A cell pulls')
        self.play(FadeIn(myosin),GrowArrow(pull),run_time=.6)
        self.at('Stretching purified')
        clear_scene(self)
        folded=rod_row(n=5,ew=.9,y=.4)
        self.play(FadeIn(folded),FadeIn(heading('purified talin',TEAL)),run_time=.45)
        self.play(Transform(folded,rod_row(unf=(2,),n=5,ew=.9,uw=3,y=.4)),run_time=.7)
        self.at('exposes hidden')
        site=Dot([0,.4,0],radius=.16,color=TEXT)
        label=T('exposed vinculin-binding site',26,TEAL).move_to([0,-2,0])
        vin=bchip('vinculin',TEAL,26).move_to([0,1.8,0])
        self.play(FadeIn(site),FadeIn(label),FadeIn(vin),Create(link([0,.6,0],[0,1.5,0])),run_time=.6)
        self.at('In a reconstituted')
        clear_scene(self)
        title=heading('reconstituted complex',TEAL)
        labels=VGroup(T('cadherin–catenin',24,TEAL).move_to([-3,2.1,0]),T('actin',24,GREEN).move_to([3,2.1,0]))
        rows=VGroup(*[VGroup(bchip('contact',TEAL,22).move_to([-3,y,0]),beaded([1,y,0],[5,y,0]),link([-2.3,y,0],[1,y,0])) for y in (1,0,-1)])
        self.play(FadeIn(title),FadeIn(labels),FadeIn(rows),run_time=.6)
        self.at('some bonds')
        self.play(FadeOut(rows[2][2]),run_time=.4)
        self.at('last longer under load')
        load=arr([4,-2,0],[5.7,-2,0],GOLD)
        self.play(FadeIn(load),Indicate(VGroup(rows[0][2],rows[1][2]),color=GOLD,scale_factor=1.02),run_time=.6)
        self.at('over a limited range')
        self.play(FadeIn(T('moderate load • limited force range',26,GOLD).move_to([0,-3.1,0])),run_time=.5)
        self.at('Matrix mechanics')
        clear_scene(self)
        bases=VGroup(*[RoundedRectangle(width=4.8,height=.55,corner_radius=.12,color=ORANGE,fill_opacity=.2).move_to([x,-.9,0]) for x in (-3.2,3.2)])
        cells=VGroup(cell_rect(-3.2,.2,2.4,1.6),cell_rect(3.2,.2,3.7,1.3))
        labs=VGroup(T('different substrate mechanics',26,ORANGE).move_to([0,-2,0]),T('can bias cell behaviour',26,GREY).move_to([0,-3,0]))
        self.play(FadeIn(bases),FadeIn(cells),FadeIn(labs),FadeIn(heading('culture result',GREY)),run_time=.65)
        self.at('Adhesions connect')
        clear_scene(self)
        left=simple_attachment(-3.3)
        # Compact second receptor chain, with labels kept at full size.
        receptor=bchip('cadherin',BLUE,24).move_to([3.3,-.65,0])
        cats=bchip('β- / α-catenin',TEAL,22).move_to([3.3,.85,0])
        act=beaded([1,2.1,0],[5.6,2.1,0])
        neighbour=bchip('next cell',GREY,24).move_to([3.3,-2.05,0])
        right=VGroup(receptor,cats,act,neighbour,T('actin',24,GREEN).move_to([3.3,2.65,0]),link(receptor.get_top(),cats.get_bottom()),link(cats.get_top(),[3.3,2.1,0]),link(receptor.get_bottom(),neighbour.get_top(),BLUE))
        self.play(FadeIn(left),FadeIn(right),run_time=.6)
        self.at('some links change when pulled')
        self.play(Indicate(left[2][1],color=GOLD),Indicate(cats[1],color=GOLD),FadeIn(T('some links respond to force',28,GOLD).move_to([0,-3.3,0])),run_time=.8)
        self.finish()
