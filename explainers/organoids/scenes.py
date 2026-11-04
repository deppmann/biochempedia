"""Brains in a Dish, chapter 1: The Program and the Surroundings  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole series; the old single film's map, with the two changes the new story needs)
  ROSE   = the starting skin cell (was ORANGE; moved off orange so AMBER stays unique)
  YELLOW = the four reprogramming factors / transcription factors
  STEM   = pale blue-white: pluripotent stem cells and the ball of them before it is steered
  TEAL   = THE PROGRAM: neural tissue, progenitor zones, whatever the cells do on their own
  GREEN  = young neurons; also a gene switched ON
  AMBER  = THE SURROUNDINGS: blood vessels, microglia, thalamic axons, interneurons from outside
  RED    = limits: the mutation, what is missing or fails, stress added by the dish
  CULTURE = lavender: changes acquired during culture
  BLUE   = moving medium and its oxygen / nutrient delivery
  GREY   = outlines, gel, DNA, structure, de-emphasised things
  WHITE  = nuclei (TEXT colour)
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ROSE = "#E58FA6"
STEM = "#C9D3E6"
AMBER = "#F0A030"
CULTURE = "#B4A0FF"  # culture-acquired changes; distinct from mutation and surroundings

class SpokenScene(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        target = self.t_of(phrase, nth) - lead
        rest = target - self.elapsed()
        with open('/tmp/organoid_fix_sync.log', 'a') as log:
            log.write(f"{os.environ.get('KX_SCENE_ID')} {phrase}: late={-rest:.2f}\n")
        if rest > 0.02:
            self.wait(rest)


NC = 46                       # cells in the ball / organoid
RC = 0.28                     # cell radius
BALL_R = 2.2
C0 = np.array([0.0, -0.1, 0.0])       # where the ball sits during the recipe
ORG_C = np.array([-3.5, -0.15, 0.0])  # where the organoid sits once it is on the left
FETAL_C = np.array([3.5, -2.1, 0.0])  # centre of the fetal-cortex arch
RING = [(12, 1.2), (14, 1.78), (20, 2.4)]
NEURAL_FROM = 22              # cells with index >= this turn teal in step 2
NEURON_FROM = 26              # cells with index >= this become neurons


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# helpers: cells, organoid, shapes
# ---------------------------------------------------------------------------------------------
def cell(r, color, nuc=True):
    g = VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22))
    if nuc:
        g.add(Circle(radius=r * 0.38, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.6))
    return g


def flat_cell(w, h, color, c):
    body = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22).move_to(c)
    nuc = Circle(radius=min(w, h) * 0.2, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.6).move_to(c)
    return VGroup(body, nuc)


def dot(p, color, r=RC):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45).move_to(p)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ball_pos(c, R=BALL_R):
    k = np.arange(NC)
    r = R * np.sqrt((k + 0.5) / NC)
    th = k * 2.39996
    return [c + np.array([ri * np.cos(t), ri * np.sin(t), 0]) for ri, t in zip(r, th)]


def ring_targets(c):
    bp = ball_pos(c)
    out, s = {}, 0
    for gi, (n, rad) in enumerate(RING):
        grp = sorted(range(s, s + n), key=lambda k: np.arctan2(bp[k][1] - c[1], bp[k][0] - c[0]))
        off = [0.3, 0.1, 0.0][gi]
        angs = sorted(np.arctan2(np.sin(off + TAU * j / n), np.cos(off + TAU * j / n)) for j in range(n))
        for k, a in zip(grp, angs):
            out[k] = c + rad * np.array([np.cos(a), np.sin(a), 0])
        s += n
    return out


def ball_cells(c, neural=False):
    ps = ball_pos(c)
    return VGroup(*[dot(p, TEAL if (neural and k >= NEURAL_FROM) else STEM) for k, p in enumerate(ps)])


def org_final(c):
    """cavity + the 46 cells in their rings (progenitors teal, neurons green)."""
    tg = ring_targets(c)
    cav = Circle(radius=0.8, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(c)
    cells = VGroup(*[dot(tg[k], GREEN if k >= NEURON_FROM else TEAL) for k in range(NC)])
    return cav, cells


def scatter_pos(seed=4):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < NC and tries < 200000:
        tries += 1
        p = P(rng.uniform(-5.9, 5.9), rng.uniform(-2.5, 2.2))
        if all(np.linalg.norm(p - q) > 0.7 for q in pts):
            pts.append(p)
    return pts


def tick(c, s=1.0, color=GREEN, w=7):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([c + np.array([-.16 * s, 0, 0]), c + np.array([-.04 * s, -.13 * s, 0]), c + np.array([.19 * s, .17 * s, 0])])
    return m


def cross(c, s=1.0, color=RED, w=7):
    return VGroup(Line(c + np.array([-.15 * s, .15 * s, 0]), c + np.array([.15 * s, -.15 * s, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-.15 * s, -.15 * s, 0]), c + np.array([.15 * s, .15 * s, 0]), color=color, stroke_width=w))


def squiggle(p0, p1, amp=0.12, n=3, color=AMBER, w=5):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    nrm = np.array([-d[1], d[0], 0]) / L
    f = lambda t: p0 + d * t + nrm * amp * np.sin(TAU * n * t)
    return ParametricFunction(f, t_range=[0, 1], stroke_color=color, stroke_width=w)


def flask():
    body = Polygon(P(-0.4, 1.8), P(0.4, 1.8), P(0.4, 0.8), P(1.5, -1.5), P(-1.5, -1.5), P(-0.4, 0.8),
                   stroke_color=GREY, stroke_width=4, fill_opacity=0)
    med = Polygon(P(-1.07, -0.6), P(1.07, -0.6), P(1.5, -1.5), P(-1.5, -1.5),
                  stroke_width=0, fill_color=GREY, fill_opacity=0.28)
    return VGroup(med, body)


# ---- the step tracker used in the recipe scenes ----
STEPS = ["1 Aggregate", "2 Steer", "3 Embed", "4 Spin"]


def tracker(active=0, show=True):
    chips = []
    for i, s in enumerate(STEPS):
        on = (i + 1 == active)
        col = TEXT if on else GREY
        lab = T(s, 32, col, weight=BOLD if on else NORMAL)
        box = RoundedRectangle(corner_radius=0.14, width=2.75, height=0.72, stroke_color=col, stroke_width=3 if on else 2,
                               fill_color=col, fill_opacity=0.22 if on else 0.04)
        chips.append(VGroup(box, lab.move_to(box)))
    g = VGroup(*chips).arrange(RIGHT, buff=0.3).move_to([0, 3.3, 0])
    return g


def bottom(text, color=TEXT, size=30):
    return T(text, size, color).move_to([0, -3.3, 0])


# ---- question-card pieces (scenes 10 to 15) ----
OPTS = ["progenitor zones\naround a cavity", "outer-radial-glia-like\ncells", "six layers of\nmature cortex", "blood vessels"]
OPT_Y = [1.9, 0.45, -1.0, -2.55]
OPT_X0 = 0.4
OPT_W = 6.3


def opt_rows():
    rows = []
    for t, y in zip(OPTS, OPT_Y):
        box = RoundedRectangle(corner_radius=0.14, width=OPT_W, height=1.05, stroke_color=GREY, stroke_width=2,
                               fill_color=GREY, fill_opacity=0.06).move_to([OPT_X0 + OPT_W / 2, y, 0])
        slot = Square(0.42, stroke_color=GREY, stroke_width=2).move_to([OPT_X0 + 0.5, y, 0])
        lab = T(t, 30, line_spacing=0.7).move_to([OPT_X0 + 1.0, y, 0], aligned_edge=LEFT)
        rows.append(VGroup(box, slot, lab))
    return rows


def slot_c(i):
    return P(OPT_X0 + 0.5, OPT_Y[i])


def header_q():
    return T("Which features appear on their own?", 30).move_to([0, 3.3, 0])


def qmarks():
    out = VGroup()
    for a in np.linspace(0, TAU, 7)[:-1] + 0.4:
        out.add(T("?", 34, GREY, weight=BOLD).move_to(ORG_C + 2.85 * np.array([np.cos(a), np.sin(a), 0])))
    return out


def legend_org():
    a = VGroup(Circle(radius=0.14, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.45), T("progenitors", 32, TEAL)).arrange(RIGHT, buff=0.2)
    b = VGroup(Circle(radius=0.14, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.45), T("young neurons", 32, GREEN)).arrange(RIGHT, buff=0.2)
    a.move_to([-4.0, -2.95, 0]); b.move_to([-3.7, -3.5, 0])
    return a, b


# ---- fetal cortex and the amber surroundings ----
FET_A0, FET_A1 = 35 * DEGREES, 145 * DEGREES
R_IN, R_MID, R_OUT = 1.8, 2.85, 3.7


def fetal(F=FETAL_C):
    teal = AnnularSector(inner_radius=R_IN, outer_radius=R_MID, angle=FET_A1 - FET_A0, start_angle=FET_A0, arc_center=F,
                         fill_color=TEAL, fill_opacity=0.45, stroke_color=TEAL, stroke_width=3)
    grn = AnnularSector(inner_radius=R_MID, outer_radius=R_OUT, angle=FET_A1 - FET_A0, start_angle=FET_A0, arc_center=F,
                        fill_color=GREEN, fill_opacity=0.40, stroke_color=GREEN, stroke_width=3)
    return VGroup(teal, grn)


def microglia(c, scale=1.0):
    g = VGroup(Circle(radius=0.17 * scale, stroke_color=AMBER, stroke_width=3, fill_color=AMBER, fill_opacity=0.6))
    for a in np.linspace(0, TAU, 7)[:-1] + 0.3:
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(d * 0.19 * scale, d * 0.42 * scale, color=AMBER, stroke_width=3))
    return g.move_to(c)


def amber_vessels(F=FETAL_C):
    return VGroup(*[squiggle(F + P(dx, 4.6), F + P(dx2, 3.0), 0.12, 3) for dx, dx2 in ((-0.8, -0.7), (0.0, 0.05), (0.8, 0.9))])


def amber_microglia(F=FETAL_C):
    return VGroup(microglia(F + P(2.4, 4.2)), microglia(F + P(-2.4, 4.2)),
                  arr(F + P(2.2, 3.95), F + P(1.9, 3.45), AMBER, 4, 0.2), arr(F + P(-2.2, 3.95), F + P(-1.9, 3.45), AMBER, 4, 0.2))


def amber_axons(F=FETAL_C):
    ends = [145, 135, 125]
    starts = [(-2.8, -0.9), (-2.2, -0.9), (-1.6, -0.9)]
    out = VGroup()
    for a, (sx, sy) in zip(ends, starts):
        e = F + 2.15 * P(np.cos(a * DEGREES), np.sin(a * DEGREES))
        out.add(squiggle(F + P(sx, sy), e, 0.07, 2))
    return out


def stream_path(F=FETAL_C):
    return CubicBezier(F + P(1.1, -0.6), F + P(1.3, 0.0), F + P(2.9, 0.1), F + P(2.3, 1.55))


def amber_stream_dots(F=FETAL_C, n=7):
    path = stream_path(F)
    return VGroup(*[Circle(radius=0.14, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.7)
                    .move_to(path.point_from_proportion(t)) for t in np.linspace(0.03, 0.95, n)])


def fetal_scene_base(withlabels=0):
    """organoid on the left, fetal cortex on the right. returns dict of parts."""
    cav, cells = org_final(ORG_C)
    f = fetal()
    parts = dict(cav=cav, cells=cells, fetal=f,
                 h_org=T("organoid", 28).move_to([ORG_C[0], 3.4, 0]),
                 h_fet=T("fetal cortex", 28).move_to([FETAL_C[0], 3.4, 0]),
                 vessels=amber_vessels(), mg=amber_microglia(), axons=amber_axons())
    return parts


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Brains in a Dish: Stem Cells and Organoids"
    TITLE = "The Program and the Surroundings"

    def construct(self):
        title=T(self.TITLE,48,font=TITLE_FONT)
        lesson=T(self.LESSON,32,TEAL)
        brand=T("BIOCHEMISTRYPEDIA",32,TEAL)
        card=VGroup(brand,title,lesson).arrange(DOWN,buff=.55)
        fit(card,max_w=12.3)
        self.add(card)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        title = T("The Program and the Surroundings", 40, font=TITLE_FONT).move_to(P(0,3.15))
        skin = flat_cell(2.2, 1.5, ROSE, P(-5.1,0.3))
        self.add(title, skin, T("skin cells",32,ROSE).move_to(P(-5.1,-1.2)))
        stem = cell(0.85,STEM).move_to(P(-1.9,0.3))
        self.at("reset them")
        self.play(GrowArrow(arr(P(-3.9,.3),P(-2.85,.3))), FadeIn(stem),
                  FadeIn(T("reset",32).move_to(P(-3.4,1.1))),FadeIn(T("stem cell",32,STEM).move_to(P(-1.9,-1.2))),run_time=.45)
        self.at("grow them")
        fl=flask().scale(.9).move_to(P(1.5,.3))
        self.play(GrowArrow(arr(P(-.95,.3),P(.1,.3))),FadeIn(fl),FadeIn(T("spinning flask",32).move_to(P(1.5,-1.8))),run_time=.45)
        self.at("weeks")
        self.play(FadeIn(T("weeks",32).move_to(P(3.5,1.2))),GrowArrow(arr(P(2.9,.3),P(4,.3))),run_time=.35)
        tissue=ball_cells(P(5.2,.3),True).scale(.48)
        self.at("Can that model")
        self.play(FadeIn(tissue),FadeIn(T("early cortex?",32,TEAL).move_to(P(5.1,-1.5))),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
CELL_C = P(-3.1, 0.0)
SPOTS = [P(-4.45, 1.15), P(-1.75, 1.15), P(-4.45, -1.15), P(-1.75, -1.15)]
FNAMES = ["Oct3/4", "Sox2", "Klf4", "c-Myc"]
GHOST_C = P(4.4, 0.2)


def s02_state():
    cellg = flat_cell(6.6, 4.4, ROSE, CELL_C)
    cell_l = T("skin cell", 30, ROSE).move_to([-3.1, -2.8, 0])
    gh = DashedVMobject(Circle(radius=1.9, stroke_color=STEM, stroke_width=4), num_dashes=32).move_to(GHOST_C)
    gh_l = T("embryonic state", 30, STEM).move_to([4.4, -2.5, 0])
    a = arr([0.55, 0.2, 0], [2.3, 0.2, 0], GREY)
    chips = VGroup(*[chip(n, YELLOW, 26, pad=0.17).move_to(s) for n, s in zip(FNAMES, SPOTS)])
    return cellg, cell_l, gh, gh_l, a, chips


class S02Reset(SpokenScene):
    def construct(self):
        skin=flat_cell(6.2,4.8,ROSE,P(-3,0))
        skin.remove(skin[1])
        nucleus=Ellipse(width=4.5,height=3.0,color=ROSE,fill_opacity=.08).move_to(P(-3,0))
        self.add(skin,nucleus,T("skin cell",36,ROSE).move_to(P(-3,-2.9)))
        target=DashedVMobject(Circle(1.7,color=STEM)).move_to(P(4.3,0))
        self.at("embryonic state")
        self.play(FadeIn(T("embryonic state",32,STEM).move_to(P(4.2,-2.4))),run_time=.25)
        factors=VGroup(*[chip(n,YELLOW,32).move_to(P(-5.6+2.0*i,3.1)) for i,n in enumerate(FNAMES)])
        for f in factors: f[0].set_fill(BG,1)
        self.at("Four transcription factors")
        self.play(FadeIn(factors),run_time=.25)
        self.play(*[f.animate.move_to(P(-4+2*(i%2),.65-1.3*(i//2))) for i,f in enumerate(factors)],run_time=1.1)
        self.play(GrowArrow(arr(P(.3,0),P(2.4,0),STEM,w=8,tip=.4)),FadeIn(target),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
GENE_X = [-5.5, -3.3, -1.1, 1.1, 3.3, 5.5]
BAR_Y = 0.6


class S03Tf(SpokenScene):
    def construct(self):
        skin=flat_cell(12.6,5.6,ROSE,P(0,-.2))
        skin.remove(skin[1])
        nucleus=Ellipse(width=11.7,height=4.4,color=ROSE).move_to(P(0,-.2))
        self.add(skin,nucleus,T("skin cell / nucleus",32,ROSE).move_to(P(0,-3.4)))
        xs=[-4.5,-1.5,1.5,4.5]
        dna=Line(P(-5.6,-.1),P(5.6,-.1),color=GREY,stroke_width=7)
        genes=VGroup(*[RoundedRectangle(width=2.0,height=.8,color=GREY,fill_opacity=.4).move_to(P(x,-.1)) for x in xs])
        factors=VGroup(*[chip(n,YELLOW,32).move_to(P(x,2.5)) for x,n in zip(xs,FNAMES)])
        for f in factors: f[0].set_fill(BG,1)
        self.add(dna,genes,factors,T("DNA",34).move_to(P(0,3.2)))
        self.at("bind DNA")
        self.play(*[f.animate.move_to(P(x,.65)) for f,x in zip(factors,xs)],run_time=.65)
        self.at("switch genes on")
        self.play(*[genes[i].animate.set_color(GREEN).set_fill(GREEN,.85) for i in range(3)],
                  *[FadeIn(T("ON",34,GREEN).move_to(P(x,-1.25))) for x in xs[:3]],run_time=.35)
        self.at("or off")
        self.play(genes[3].animate.set_fill(GREY,.02).set_stroke(GREY,opacity=.5),FadeIn(T("OFF",34,RED).move_to(P(xs[3],-1.25))),run_time=.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
IPS_C = P(0, -0.2)
IPS_R = 1.35
ICON_POS = [(0, 2.7), (4.8, 0.9), (3.0, -1.9), (-3.0, -1.9), (-4.8, 0.9)]
ICON_NAMES = ["neuron", "muscle", "blood", "liver", "gut"]


def cell_icon(kind, c, k=1.7):
    c = np.array(c, float)
    g = VGroup()
    if kind == "neuron":
        g.add(Circle(radius=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35))
        for a in (30, 110, 190, 270, 330):
            d = np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0])
            g.add(Line(d * 0.2, d * (0.45 if a != 270 else 0.55), color=GREY, stroke_width=3))
    elif kind == "muscle":
        g.add(RoundedRectangle(corner_radius=0.2, width=1.1, height=0.42, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3))
        for x in (-0.25, 0, 0.25):
            g.add(Line([x, -0.14, 0], [x, 0.14, 0], color=GREY, stroke_width=2))
    elif kind == "blood":
        g.add(Circle(radius=0.34, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3), Circle(radius=0.12, stroke_color=GREY, stroke_width=2))
    elif kind == "liver":
        g.add(RegularPolygon(6, radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3))
    else:
        g.add(RoundedRectangle(corner_radius=0.12, width=0.45, height=0.85, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3))
        for x in (-0.1, 0.1):
            g.add(Line([x, 0.5, 0], [x, 0.3, 0], color=GREY, stroke_width=2))
    return g.scale(k).move_to(c)


class S04Ips(SpokenScene):
    def construct(self):
        skin=flat_cell(5,3,ROSE,P(0,0))
        self.add(skin)
        self.at("induced pluripotent")
        ips=cell(1.25,STEM)
        full=T("iPS cell = induced pluripotent stem cell",34,STEM).move_to(P(0,3.25))
        self.play(ReplacementTransform(skin,ips),FadeIn(full),run_time=.65)
        self.at("Pluripotent means")
        meaning=T("pluripotent: can become any cell type",34,STEM).move_to(P(0,-3.35))
        positions=[(-4.9,1.3),(-2.6,-1.6),(0,2.25),(2.6,-1.6),(4.9,1.3)]
        self.play(ips.animate.scale(.65).move_to(P(0,-.2)),FadeIn(meaning),run_time=.45)
        self.at("any cell type")
        icons=VGroup(*[VGroup(cell_icon(n,P(x,y),1.8),T(n,32).move_to(P(x,y-1.0))) for n,(x,y) in zip(ICON_NAMES,positions)])
        self.play(FadeIn(icons),run_time=.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Genome(SpokenScene):
    CELL_AT = P(-2.6, -0.1)

    def construct(self):
        ips = cell(IPS_R, STEM).move_to(IPS_C)
        ips_l = T("iPS cell", 32, STEM).move_to(IPS_C + P(0, -1.2 - 0.45))
        self.add(ips, ips_l)
        big = Circle(radius=3.2, stroke_color=STEM, stroke_width=4, fill_color=STEM, fill_opacity=0.12).move_to(self.CELL_AT)
        self.play(ReplacementTransform(ips, big), FadeOut(ips_l), run_time=0.9)
        c = self.CELL_AT
        k = 1.2
        spec = [(-1.1, 0.9, 1.5, 0.15), (-0.35, 1.0, 1.1, -0.1), (0.5, 0.95, 1.7, 0.2), (1.2, 0.7, 1.2, -0.2),
                (-0.9, -0.9, 1.3, -0.15), (0.0, -0.95, 1.6, 0.1), (0.95, -0.8, 1.0, 0.25)]
        chroms = VGroup(*[RoundedRectangle(corner_radius=0.2, width=0.4, height=h * k, stroke_color=TEXT, stroke_width=2,
                                           fill_color=TEXT, fill_opacity=0.28).rotate(rot).move_to(c + P(x * k * 1.15, y * k * 1.15))
                          for x, y, h, rot in spec])
        head = T("the patient’s\ngenome", 38).move_to([3.9, 2.6, 0])
        self.at("made from")
        self.play(FadeIn(chroms, lag_ratio=0.12), run_time=1.1)
        self.at("carries the patient's")
        self.play(FadeIn(head), run_time=0.5)
        # mutation: a red band on chromosome 3 (upper middle)
        ch = chroms[3]
        band = Rectangle(width=0.48, height=0.26, stroke_color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.95).rotate(0.2).move_to(ch.get_center() + P(0.0, 0.25))
        mut_l = T("mutation", 34, RED).move_to([4.6, 1.5, 0])
        mut_line = Line(mut_l.get_left() + LEFT * 0.1, band.get_center() + RIGHT * 0.25, color=RED, stroke_width=3)
        self.at("mutation included")
        self.play(FadeIn(band, scale=2), run_time=0.5)
        self.play(Create(mut_line), FadeIn(mut_l), run_time=0.6)
        # new changes in culture: small grey marks on the right-hand chromosomes
        mark_at = [chroms[6].get_center() + P(0, 0.3), chroms[5].get_center() + P(0, 0.35), chroms[2].get_center() + P(0, -0.35)]
        marks = VGroup(*[Circle(radius=0.17, stroke_color=CULTURE, stroke_width=3, fill_color=CULTURE, fill_opacity=0.95).move_to(p) for p in mark_at])
        new_l = VGroup(T("new changes", 38, CULTURE), T("in culture", 38, CULTURE)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([4.5, -1.5, 0])
        new_lines = VGroup(Line(new_l.get_left()+LEFT*.15, marks[0].get_right(),color=CULTURE,stroke_width=3))
        self.at("pick up new")
        self.play(FadeIn(marks, scale=2, lag_ratio=0.3), run_time=0.9)
        self.play(FadeIn(new_l), Create(new_lines), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06R1(SpokenScene):
    def construct(self):
        sp = scatter_pos()
        dots = VGroup(*[dot(p, STEM) for p in sp])
        lab = bottom("stem cells", STEM)
        self.play(FadeIn(dots, lag_ratio=0.03), FadeIn(lab), run_time=0.9)
        self.at("four steps")
        tr = tracker(0)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tr], lag_ratio=0.2), run_time=1.0)
        self.at("gather the stem cells")
        tr2 = tracker(1)
        bp = ball_pos(C0)
        self.play(Transform(tr, tr2), *[d.animate.move_to(bp[i]) for i, d in enumerate(dots)], run_time=1.1)
        self.at("into a ball")
        lab2 = bottom("embryoid body", STEM)
        self.play(FadeTransform(lab, lab2), run_time=0.5)
        self.finish()


class S07R2(SpokenScene):
    def finish(self):
        super().finish()
        self.wait(1.5)

    def construct(self):
        cells = ball_cells(C0)
        lab = bottom("embryoid body", STEM)
        tr = tracker(1)
        self.add(cells, lab, tr)
        self.play(Transform(tr, tracker(2)), run_time=0.4)
        self.at("neural tissue")
        lab2 = bottom("neural tissue", TEAL)
        self.play(*[cells[k].animate.set_color(TEAL) for k in range(NEURAL_FROM, NC)], FadeTransform(lab, lab2), run_time=0.9)
        self.finish()


def gel_ball(c, scale=1.0, tealouter=True):
    gel = Circle(radius=BALL_R + 0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.16).move_to(c)
    cells = ball_cells(c, neural=tealouter)
    return gel, cells


class S08R3(SpokenScene):
    def finish(self):
        super().finish()
        self.wait(1.5)

    def construct(self):
        cells = ball_cells(C0, neural=True)
        lab = bottom("neural tissue", TEAL)
        tr = tracker(2)
        self.add(cells, lab, tr)
        self.play(Transform(tr, tracker(3)), run_time=0.4)
        self.at("droplet of gel")
        gel = Circle(radius=BALL_R + 0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.16).move_to(C0)
        lab2 = bottom("Matrigel", GREY)
        self.play(FadeIn(gel, scale=1.12), FadeTransform(lab, lab2), run_time=0.8)
        self.bring_to_front(cells)
        self.finish()


class S09R4(SpokenScene):
    def construct(self):
        self.add(tracker(4))
        # Large cutaway beside the flask: the gel occupies 80% of frame height.
        fl=flask().scale(1.65).move_to(P(3.9,-.1))
        self.add(fl)
        gel,cells=gel_ball(P(0,0))
        drop=VGroup(gel,cells).scale(3.2/2.7).move_to(P(-2.55,-.35))
        small=VGroup(*gel_ball(P(0,0))).scale(.29).move_to(P(3.9,-.95))
        self.add(drop,small,T("Matrigel",32).move_to(P(3.9,2.25)),
                 T("enlarged droplet",26,GREY).move_to(P(-2.55,-3.65)))
        flow=Arc(radius=1.85,start_angle=.15,angle=PI*1.45,arc_center=P(3.9,-.45),color=BLUE,stroke_width=6).add_tip()
        self.at("spin it")
        self.play(Rotate(small,angle=.4),run_time=.35)
        self.at("moving medium")
        routes=VGroup(arr(P(2.0,.55),P(-.5,.55),BLUE),arr(P(2.0,-1.55),P(-.5,-1.55),BLUE))
        self.play(Create(flow),*[GrowArrow(a) for a in routes],run_time=.45)
        labels=VGroup(T("oxygen",30,BLUE).move_to(P(1.25,1.05)),T("nutrients",30,BLUE).move_to(P(1.25,-2.05)))
        dots=VGroup(*[Dot(P(1.9+.22*(i%3),.55 if i<3 else -1.55),radius=.12,color=BLUE) for i in range(6)])
        self.at("oxygen and nutrients")
        self.play(FadeIn(labels),FadeIn(dots),run_time=.15)
        self.play(*[d.animate.move_to(P(-1.15-.42*(i%3),.55 if i<3 else -1.55)) for i,d in enumerate(dots)],run_time=.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def question_frame(with_q=True):
    cells = ball_cells(ORG_C, neural=True)
    rows = opt_rows()
    h = header_q()
    qm = qmarks()
    return cells, rows, h, qm


class S10Predict(SpokenScene):
    def construct(self):
        cells,rows,h,qm=question_frame()
        self.add(cells,h,*rows)
        self.at("which features")
        self.play(Indicate(h,color=TEAL,scale_factor=1.02),run_time=.5)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        cells, rows, h, qm = question_frame()
        self.add(cells, h, *rows, T("Pause and choose your answer",32,TEAL).move_to(P(-3.5,2.75)))
        self.finish()


class S12Zones(SpokenScene):
    def construct(self):
        cells = ball_cells(ORG_C, neural=True)
        rows = opt_rows()
        h = header_q()
        qm = qmarks()
        self.add(cells, h, *rows)
        tg = ring_targets(ORG_C)
        self.at("Zones of progenitors")
        leg_a, leg_b = legend_org()
        anims = [cells[k].animate.move_to(tg[k]).set_color(TEAL) for k in range(NC)]
        self.add(T("schematic • weeks →",26,GREY).move_to(P(-4,2.9)))
        self.play(*anims, FadeIn(leg_a), run_time=1.3)
        orad = radial_cells()
        radial_label=T("outer-radial-\nglia-like cells",22,TEAL).move_to(P(-.85,2.6))
        radial_leader=Line(radial_label.get_left()+DOWN*.15,P(-1.87,2.12),color=TEAL,stroke_width=2)
        # This is a kind of progenitor: reveal its morphology and answer on
        # the progenitor clause, rather than inserting an unspoken later beat.
        self.play(FadeIn(orad),FadeIn(radial_label),Create(radial_leader),
                  Create(tick(slot_c(1),1.3)),run_time=.3)
        cav = Circle(radius=0.8, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(ORG_C)
        cav_t = T("cavity", 32, GREY).move_to(ORG_C)
        self.at("fluid filled cavity")
        self.play(GrowFromCenter(cav), run_time=0.7)
        self.play(FadeIn(cav_t), run_time=0.3)
        t1 = tick(slot_c(0), 1.3)
        self.play(Create(t1), run_time=0.4)
        self.at("Young neurons")
        self.play(*[cells[k].animate.set_color(GREEN) for k in range(NEURON_FROM, NC)], FadeIn(leg_b), run_time=0.6)
        self.at("settle outside")
        self.play(Indicate(VGroup(*[cells[k] for k in range(NEURON_FROM, NC)]), color=GREEN, scale_factor=1.05), run_time=0.9)
        self.finish()


def radial_cells():
    g=VGroup()
    for a in (0.15, .55, .95):
        d=P(np.cos(a),np.sin(a))
        c=ORG_C+1.78*d
        g.add(dot(c,TEAL,.23),Line(c+.23*d,ORG_C+2.8*d,color=TEAL,stroke_width=4))
    return g


def org_state():
    cav, cells = org_final(ORG_C)
    cav_t = T("cavity", 32, GREY).move_to(ORG_C)
    cells.add(radial_cells())
    return cav, cells, cav_t


class S13Self(SpokenScene):
    def construct(self):
        cav,cells,cav_t=org_state()
        leg_a,leg_b=legend_org()
        self.add(cav,cells,cav_t,leg_a,leg_b)
        targets=[cells[k].get_center().copy() for k in range(NC)]
        scattered=ball_pos(ORG_C)
        self.at("No one placed")
        self.play(FadeOut(cav,cav_t),*[cells[k].animate.move_to(scattered[k]) for k in range(NC)],run_time=1.1)
        self.at("They arranged themselves")
        self.play(FadeIn(cav,cav_t),*[cells[k].animate.move_to(targets[k]) for k in range(NC)],run_time=1.0)
        self.at("self organization")
        self.play(FadeIn(T("self-organization",44,font=TITLE_FONT).move_to(P(3.5,.5))),run_time=.25)
        self.at("idea behind every organoid")
        self.play(FadeIn(T("the idea behind\nevery organoid",34,GREY).move_to(P(3.5,-.6))),run_time=.3)
        self.finish()


class S14Beat(NarratedScene):
    def construct(self):
        cav, cells, cav_t = org_state()
        leg_a, leg_b = legend_org()
        so = T("self-organization", 44, font=TITLE_FONT).move_to([3.5, 0.5, 0])
        sub = T("the idea behind\nevery organoid", 34, GREY).move_to([3.5, -0.4, 0])
        self.add(cav, cells, cav_t, leg_a, leg_b, so, sub)
        self.finish()


class S15Fail(SpokenScene):
    def construct(self):
        cav, cells, cav_t = org_state()
        leg_a, leg_b = legend_org()
        so = T("self-organization", 44, font=TITLE_FONT).move_to([3.5, 0.5, 0])
        sub = T("the idea behind\nevery organoid", 34, GREY).move_to([3.5, -0.4, 0])
        self.add(cav, cells, cav_t, leg_a, leg_b)
        rows = opt_rows()
        t1, t2 = tick(slot_c(0), 1.3), tick(slot_c(1), 1.3)
        rows[2][0].stretch_to_fit_height(1.45).shift(UP*.12)
        rows[2][1:].shift(UP*.32)
        self.add(header_q(),*rows,t1,t2)
        self.at("six layers")
        self.play(Indicate(rows[2][0], color=RED, scale_factor=1.03), run_time=0.7)
        self.at("form at best partly")
        x3 = cross(slot_c(2)+UP*.32, 1.3)
        n3 = T("at best partial", 32, RED).move_to([OPT_X0 + 1.0, OPT_Y[2] - 0.42, 0], aligned_edge=LEFT)
        self.play(Create(x3), FadeIn(n3), run_time=0.7)
        self.at("no blood vessels")
        x4 = cross(slot_c(3), 1.3)
        n4 = T("none", 32, RED).move_to([OPT_X0 + 1.0, OPT_Y[3] - 0.75, 0], aligned_edge=LEFT)
        self.play(Create(x4), FadeIn(n4), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def amber_vessels(F=FETAL_C):
    # Paired tube walls and a fork, entering across the surface.
    g=VGroup()
    for dx in (-.10,.10):
        g.add(VMobject(color=AMBER,stroke_width=4).set_points_as_corners([P(2.35+dx,2.4),P(2.35+dx,1.15),P(1.9+dx,.55)]))
        g.add(Line(P(2.35+dx,1.15),P(2.9+dx,.55),color=AMBER,stroke_width=4))
    return g


def amber_microglia(F=FETAL_C):
    return VGroup(microglia(P(5.4,1.7)),arr(P(5.4,1.2),P(4.8,.45),AMBER))


def amber_axons(F=FETAL_C):
    g=VGroup()
    for x in (1.7,2.15,2.6):
        end=P(x+.3,-.3)
        g.add(Line(P(x,-2.45),end,color=AMBER,stroke_width=2.5),Triangle(color=AMBER,fill_opacity=.6).scale(.10).move_to(end))
    return g


def stream_path(F=FETAL_C):
    return CubicBezier(P(6.1,-2.3),P(6,-1.5),P(5.9,-.6),P(5.35,.15))


def comparison():
    cav,cells,ct=org_state()
    f=fetal()
    heads=VGroup(T("organoid",36).move_to(P(-3.5,3.3)),T("fetal cortex",36).move_to(P(3.5,3.3)))
    la,lb=legend_org()
    return dict(cav=cav,cells=cells,ct=ct,f=f,heads=heads,legend=VGroup(la,lb),ves=amber_vessels(),mg=amber_microglia(),ax=amber_axons())


def comparison_labels():
    ves=T("blood vessels",32,AMBER).move_to(P(2.1,2.65))
    mg=T("microglia",32,AMBER).move_to(P(5.3,2.65))
    ax=T("axons from\nthalamus",32,AMBER).move_to(P(1.7,-3.05))
    return ves,mg,ax


def build_comparison(sc, count=3):
    p=comparison()
    sc.add(*[p[k] for k in ('cav','cells','ct','f','heads','legend')])
    labs=comparison_labels()
    for k,l in zip(('ves','mg','ax')[:count],labs[:count]): sc.add(p[k],l)
    return p,labs


class S16Fetal(SpokenScene):
    def construct(self):
        p,labs=build_comparison(self,0)
        self.at("fetal cortex")
        self.play(Indicate(p['f'],color=TEAL,scale_factor=1.02),run_time=.5)
        self.at("comes from the cells")
        a=T("from the cells",32,TEAL).move_to(P(4.6,-1.3))
        self.play(FadeIn(a),run_time=.25)
        self.at("from the body around")
        b=T("from the body\naround them",32,AMBER).move_to(P(4.6,-2.65))
        self.play(FadeIn(b),*[FadeIn(p[k]) for k in ('ves','mg','ax')],run_time=.35)
        self.finish()


class S17Amber1(SpokenScene):
    def construct(self):
        p,(lv,lm,la)=build_comparison(self,0)
        self.at("Blood vessels")
        self.play(FadeIn(p['ves']),FadeIn(lv),run_time=.25)
        self.at("Microglia")
        self.play(FadeIn(p['mg']),FadeIn(lm),run_time=.25)
        self.at("arrive from outside")
        outside=T("arriving\nfrom outside",24,AMBER).move_to(P(3.85,2.05))
        self.play(FadeIn(outside),Indicate(p['mg'][1],color=AMBER),run_time=.4)
        self.at("Axons bring input")
        self.play(FadeIn(p['ax']),FadeIn(la),run_time=.25)
        self.finish()


class S18Amber2(SpokenScene):
    def construct(self):
        p,_=build_comparison(self)
        dots=amber_stream_dots()
        starts=[d.get_center().copy() for d in dots]
        for d in dots: d.move_to(P(6.1,-2.3))
        lab=T("interneurons",32,AMBER).move_to(P(4.15,-1.85))
        self.at("interneurons stream")
        self.add(dots)
        self.play(FadeIn(lab),*[d.animate.move_to(t) for d,t in zip(dots,starts)],run_time=1.1)
        self.at("ventral forebrain")
        self.play(FadeIn(T("from ventral\nforebrain",32,AMBER).move_to(P(5,-3.05))),run_time=.25)
        self.finish()


class S19Missing(SpokenScene):
    def construct(self):
        p,_=build_comparison(self)
        self.add(amber_stream_dots(),T("from ventral\nforebrain",32,AMBER).move_to(P(5,-3.05)))
        # Clear, empty dashed symbols in the margin, outside the cell rings.
        ghost=VGroup()
        vessel=VGroup(Line(P(-6.45,1.9),P(-6.45,.8)),
                      Line(P(-6.45,1.25),P(-5.95,.8)))
        mg=microglia(P(-.5,1.95),1.2)
        axon=VGroup(Line(P(-6.45,-1.1),P(-6.45,-2.55)),
                    Line(P(-6.65,-1.4),P(-6.45,-1.1)),Line(P(-6.25,-1.4),P(-6.45,-1.1)))
        stream=VGroup(*[Circle(radius=.18).move_to(P(-.45,-.5-.55*i)) for i in range(3)])
        for source in (vessel,mg,axon,stream):
            for part in source.family_members_with_points():
                outline=part.copy().set_fill(opacity=0).set_stroke(AMBER,width=4,opacity=1)
                ghost.add(DashedVMobject(outline,num_dashes=6,dashed_ratio=.65))
        self.add(ghost)
        self.at("most of these")
        caption=T("most missing",36,RED).move_to(P(-3.5,2.85))
        self.play(FadeIn(caption),run_time=.15)
        self.at("are missing")
        self.play(FadeOut(ghost),run_time=.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rule_panels():
    tp = RoundedRectangle(corner_radius=0.25, width=6.0, height=5.4, stroke_color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.08).move_to([-3.35, 0.3, 0])
    ap = RoundedRectangle(corner_radius=0.25, width=6.0, height=5.4, stroke_color=AMBER, stroke_width=3,
                          fill_color=AMBER, fill_opacity=0.08).move_to([3.35, 0.3, 0])
    # teal icon: a ring of progenitors around a cavity
    ring = VGroup(Circle(radius=0.6, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1))
    for a in np.linspace(0, TAU, 11)[:-1]:
        ring.add(dot(1.1 * np.array([np.cos(a), np.sin(a), 0]), TEAL, 0.24))
    ring.move_to([-3.35, 1.45, 0])
    t1 = T("The cells", 46, TEAL, weight=BOLD).move_to([-3.35, -0.75, 0])
    t2 = T("bring the program", 32, TEAL).move_to([-3.35, -1.55, 0])
    # amber icon: vessel, microglia, interneurons
    v = amber_vessels().scale(.8).move_to(P(1.8,1.5))
    mg = microglia(P(3.3, 1.5), 1.5)
    ints = VGroup(*[Circle(radius=0.19, stroke_color=AMBER, stroke_width=2, fill_color=AMBER, fill_opacity=0.7).move_to(P(4.4 + 0.5 * i, 1.0 + 0.35 * i)) for i in range(3)])
    icons = VGroup(v, mg, ints)
    a1 = T("The embryo", 46, AMBER, weight=BOLD).move_to([3.35, -0.75, 0])
    a2 = T("brings the surroundings", 32, AMBER).move_to([3.35, -1.55, 0])
    return dict(tp=tp, ap=ap, ring=ring, t1=t1, t2=t2, icons=icons, a1=a1, a2=a2)


class S20Rule1(SpokenScene):
    def construct(self):
        r=rule_panels()
        self.add(T("The one idea to carry through",36).move_to(P(0,3.45)),r['tp'],r['ap'],r['ring'],r['icons'])
        self.at("The cells bring")
        self.play(FadeIn(r['t1']),FadeIn(r['t2']),run_time=.25)
        self.at("The embryo brings")
        self.play(FadeIn(r['a1']),FadeIn(r['a2']),run_time=.25)
        self.finish()


class S21Rule2(SpokenScene):
    def construct(self):
        r = rule_panels()
        hd = T("The one idea to carry through", 30, GREY).move_to([0, 3.45, 0])
        self.add(hd, *r.values())
        k = T("an organoid keeps this", 32, TEAL).move_to([-3.35, -3.2, 0])
        l = T("and loses most of this", 32, AMBER).move_to([3.35, -3.2, 0])
        self.at("organoid keeps the program")
        self.play(FadeIn(k), Indicate(r["tp"], color=TEAL, scale_factor=1.02), run_time=0.9)
        self.at("loses most of the surroundings")
        self.play(FadeIn(l), r["icons"].animate.set_opacity(0.18), run_time=1.0)
        self.finish()


def take_card():
    hd = T("A first guess at when to trust an organoid", 36, TEXT).move_to([0, 3.4, 0])
    rows = []
    spec = [("Trust it most", "for what the cells do on their own", TEAL, TEAL),
            ("Test it hardest", "where development needs something from outside", AMBER, AMBER),
            ("Measure every feature", "because the dish adds stress of its own", TEXT, RED)]
    for i, (a, b, c1, c2) in enumerate(spec):
        y = 1.8 - 2.0 * i
        bar = Rectangle(width=0.16, height=1.6, stroke_width=0, fill_color=c1, fill_opacity=1).move_to([-6.2, y, 0])
        l1 = T(a, 46, c1, weight=BOLD).move_to([-5.8, y + 0.4, 0], aligned_edge=LEFT)
        l2 = T(b, 32, c2).move_to([-5.8, y - 0.4, 0], aligned_edge=LEFT)
        rows.append(VGroup(bar, l1, l2))
    return hd, rows


class S22Take(SpokenScene):
    def construct(self):
        hd,rows=take_card()
        self.add(hd)
        self.at("trust it most")
        self.play(FadeIn(rows[0]),run_time=.25)
        self.at("Test it hardest")
        self.play(FadeIn(rows[1]),run_time=.25)
        self.at("measure every feature")
        self.play(FadeIn(VGroup(rows[2][0],rows[2][1])),run_time=.25)
        self.at("dish adds stress")
        self.play(FadeIn(rows[2][2]),run_time=.25)
        self.finish()


class S23Beat(NarratedScene):
    def construct(self):
        hd, rows = take_card()
        self.add(hd, *rows)
        self.finish()


class S24End(EndCard):
    LINE = "Trust the program. Test the surroundings. Measure every feature."

    def construct(self):
        lines=VGroup(T("Trust the program.",44,TEAL,font=TITLE_FONT),
                     T("Test the surroundings.",44,AMBER,font=TITLE_FONT),
                     T("Measure every feature.",44,font=TITLE_FONT)).arrange(DOWN,buff=.45)
        self.add(lines,T("biochemistrypedia.com",32,TEAL).move_to(P(0,-2.5)))
        self.finish()
