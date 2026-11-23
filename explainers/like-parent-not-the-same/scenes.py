"""Overhead kitchen-table illustrations for Like Their Parents, Not the Same."""
from bp_parts import *

# Color map. Shared setup palette: blue for the guiding idea, teal for activity,
# gold for observation, green for living material, red for safety. Paper, wood
# and skin use neutral illustration colors.
TABLE, TABLE_EDGE = "#254349", "#47656A"
PAPER, RIM = "#FEF7E6", "#DACFB4"
INK, WOOD = "#243538", "#9A633F"
POD, PEAS, PALE = "#39724A", "#80B85F", "#BDD18B"
SKIN, SMALL_HAND = "#C78360", "#E9AF86"
APPLE, PEPPER, SEED = "#C74843", "#E2A83B", "#663F31"
PAGE = "#FFF1D7"
ORIGIN_PLATE = np.array([0.0, -0.65, 0.0])
REVEAL_PLATE = np.array([1.78, -0.12, 0.0])
CM = 0.78


def xy(x, y):
    return np.array([x, y, 0.0])


def panel(w, h, fill, edge=None, radius=0.2):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, fill_color=fill,
                            fill_opacity=1, stroke_color=edge or fill, stroke_width=2 if edge else 0)


def oval(w, h, fill, edge=None, stroke=2):
    return Ellipse(width=w, height=h, fill_color=fill, fill_opacity=1,
                   stroke_color=edge or fill, stroke_width=stroke if edge else 0)


def shape(points, fill, edge=None, stroke=2):
    path = VMobject(fill_color=fill, fill_opacity=1, stroke_color=edge or fill,
                    stroke_width=stroke if edge else 0)
    path.set_points_smoothly([xy(*point) for point in [*points, points[0]]])
    return path


def line(a, b, color=INK, width=2):
    return Line(xy(*a), xy(*b), color=color, stroke_width=width)


def table():
    top = panel(13.16, 7.04, TABLE, TABLE_EDGE, 0.38).shift(DOWN * 0.04)
    # Short grain lines stay in the margins, away from labels and the work area.
    grain = VGroup(*(line((x, y), (x + w, y), TABLE_EDGE, 1.1) for x, y, w in
                    [(-6.22, 1.93, .59), (-6.2, -1.74, .32), (-6.26, -2.9, .86),
                     (5.64, -.88, .58), (5.6, -2.64, .58)]))
    return VGroup(top, grain).set_z_index(-3)


def plate(center=ORIGIN_PLATE):
    shadow = oval(8.25, 4.72, "#183239").shift(DOWN * .10)
    raised = oval(8.2, 4.68, PAPER, RIM, 3)
    well = oval(7.43, 3.94, PAPER, RIM, 1.4)
    return VGroup(shadow, raised, well).move_to(center)


def pea(w=.72, h=None, fill=PEAS):
    h = w if h is None else h
    body = oval(w, h, fill, POD, 2.5)
    shine = oval(w*.27, h*.12, "#DFE6AB").rotate(.36).move_to(xy(-w*.15, h*.20))
    return VGroup(body, shine)


def pea_row(center=ORIGIN_PLATE, y=.22, varied=False, count=5, step=1.15):
    sizes = [(.72, .72, PEAS)] * count
    if varied:
        sizes = [(.77, .77, PEAS), (.68, .68, PEAS), (.70, .70, PALE),
                 (.67, .67, PEAS), (.49, .29, PEAS)]
    return VGroup(*(pea(w, h, color).move_to(center + xy((i-(count-1)/2)*step, y))
                    for i, (w, h, color) in enumerate(sizes)))


def pod_valves(count=5):
    length = 6.35 if count == 5 else 5.23
    shell = shape([(-3.18, .05), (-2.55, .75), (-1.25, .91), (.15, .75), (1.7, .66),
                   (3.18, .19), (2.48, -.48), (1.05, -.73), (-.70, -.67), (-2.28, -.40)],
                  POD, "#244F37", 3)
    lining = shape([(-2.94, .07), (-2.33, .43), (-.8, .52), (.8, .42), (2.85, .19),
                    (2.15, -.29), (.64, -.43), (-1.09, -.37), (-2.31, -.20)], "#A5C37F")
    stem = ArcBetweenPoints(xy(-3.82, .48), xy(-3.05, .08), angle=1.1,
                            color=POD, stroke_width=7)
    lid = shape([(-3.15, .08), (-2.59, .69), (-1.36, .85), (.0, .7), (1.45, .60),
                 (3.15, .19), (2.26, -.39), (.88, -.53), (-.68, -.45), (-2.16, -.33)],
                "#55955B", "#2D6044", 2.5)
    seam = ArcBetweenPoints(xy(-2.96, .10), xy(2.92, .18), angle=-.22,
                            color="#ADD08E", stroke_width=2.8)
    bottom = VGroup(shell, lining, stem).stretch_to_fit_width(length + .58)
    top = VGroup(lid, seam).stretch_to_fit_width(length)
    return bottom, top


def pod(center=ORIGIN_PLATE, opened=False, count=5):
    base, lid = pod_valves(count)
    base.move_to(center + DOWN*.22)
    lid.move_to(center + DOWN*.12)
    group = VGroup(base)
    if opened:
        lid.shift(UP*.72).rotate(.045)
        group.add(lid, pea_row(center, y=-.10, count=count, step=1.06))
    else:
        group.add(lid)
    return group


def ruler(center, tilt=0):
    width = CM * 9
    face = panel(width, .75, "#F1CE88", "#B38046", .09)
    ticks = VGroup()
    for i in range(1, 45):
        x = -width/2 + i*CM/5
        tick_height = .25 if i % 5 == 0 else .12
        ticks.add(line((x, .32), (x, .32-tick_height), INK, 1.5))
    return VGroup(face, ticks).rotate(tilt).move_to(center)


def ruler_unit(center):
    # The bracket spans one major division of the ruler.
    x = center[0] - CM*1.5
    y = center[1] - .57
    mark = VGroup(line((x, y), (x + CM, y), WOOD, 3),
                  line((x, y-.10), (x, y+.10), WOOD, 2),
                  line((x+CM, y-.10), (x+CM, y+.10), WOOD, 2))
    return VGroup(mark, T("1 cm", 31, WOOD).move_to(xy(x + CM/2, y-.37)))


def leaf(w=1.08, h=.56, color="#78A762"):
    body = shape([(-.58, 0), (-.03, .29), (.58, .03), (.05, -.24)],
                 color, POD, 2)
    vein = line((-.56, 0), (.32, .03), POD, 1.8)
    return VGroup(body, vein).stretch_to_fit_width(w).stretch_to_fit_height(h)


def plant(center, scale=1):
    stem = CubicBezier(xy(-.87, -1.5), xy(-.26, -.55), xy(-.58, .75),
                       xy(.18, 1.34), color=POD, stroke_width=8)
    shoots = VGroup(line((-.55, -.86), (0, -.41), POD, 4),
                    line((-.43, -.45), (-1.07, -.13), POD, 4),
                    line((-.33, .10), (.34, .53), POD, 4),
                    line((-.22, .66), (-.68, .87), POD, 4))
    leaves = VGroup(leaf(1.27, .65).rotate(.49).move_to(xy(.42, -.25)),
                    leaf(1.15, .64).rotate(-.38).move_to(xy(-1.22, -.02)),
                    leaf(1.1, .59).rotate(.51).move_to(xy(.59, .70)),
                    leaf(.78, .47).rotate(-.37).move_to(xy(-.71, .88)),
                    leaf(.63, .40).rotate(.96).move_to(xy(.16, 1.38)))
    curling = ArcBetweenPoints(xy(.04, 1.0), xy(.65, 1.23), angle=-2.0,
                              color=GREEN, stroke_width=3)
    return VGroup(stem, shoots, leaves, curling).scale(scale).move_to(center)


def twig(center, scale=1):
    stem = line((-2.4, -.8), (2.15, .92), WOOD, 6)
    leaves = VGroup()
    for i, (x, y, w, theta) in enumerate([(-1.54, .16, 1.35, 2.27), (-.85, -.75, 1.48, -.69),
                                          (-.50, .67, 1.58, 2.05), (.34, -.17, 1.71, -.63),
                                          (.65, 1.14, 1.51, 2.0), (1.68, .72, 1.40, .34)]):
        leaves.add(leaf(w, .66 + .045*(i%3)).rotate(theta).move_to(xy(x, y)))
    return VGroup(stem, leaves).scale(scale).move_to(center)


def hand(center, angle=0, scale=1, adult=True, pose="open"):
    color = SKIN if adult else SMALL_HAND
    if pose == "thumb":
        points = [(-.59,-1.10),(.55,-1.10),(.63,-.32),(.50,.29),(.29,.35),
                  (.10,.41),(.02,.73),(-.20,.78),(-.35,.60),(-.38,.33),(-.62,.28),(-.70,-.31)]
    elif pose == "point":
        points = [(-.59,-1.15),(.54,-1.15),(.69,-.29),(.52,.20),(.26,.28),
                  (.16,1.15),(-.03,1.24),(-.14,1.11),(-.19,.28),(-.55,.19),(-.68,-.19)]
    elif pose == "curl":
        points = [(-.61,-1.13),(.60,-1.13),(.71,-.37),(.74,.14),(.48,.48),
                  (.12,.48),(-.16,.40),(-.36,.44),(-.63,.32),(-.72,-.05)]
    else:
        points = [(-.57,-1.19),(.56,-1.19),(.65,-.46),(.82,.11),(.75,.39),(.50,.26),
                  (.33,.13),(.39,.94),(.23,1.04),(.13,.90),(.05,1.15),(-.13,1.16),
                  (-.22,1.02),(-.35,1.07),(-.47,.91),(-.53,.58),(-.64,.64),(-.77,.48),(-.77,-.21)]
    palm = shape(points, color, "#9D5A41", 2.7)
    cuff = panel(1.14, .42, TEAL if adult else GOLD, radius=.09).move_to(xy(0,-1.08))
    detail = VGroup()
    if pose == "curl":
        for x in [-.32, 0, .32]:
            detail.add(ArcBetweenPoints(xy(x-.11,.12), xy(x+.08,.16), angle=-1,
                                        color="#9D5A41", stroke_width=2))
    return VGroup(palm, cuff, detail).scale(scale).rotate(angle).move_to(center)


def pencil(center, angle=-.13, scale=1):
    barrel = panel(2.3, .22, "#E2AB48", "#A87332", .05)
    eraser = panel(.24, .22, "#E18A88", radius=.04).move_to(xy(-1.12,0))
    tip = Polygon(xy(1.13,-.11), xy(1.45,0), xy(1.13,.11), fill_opacity=1,
                  fill_color="#F1CF9E", stroke_width=0)
    graphite = Polygon(xy(1.36,-.03), xy(1.46,0), xy(1.36,.03), fill_opacity=1,
                       fill_color=INK, stroke_width=0)
    return VGroup(barrel, eraser, tip, graphite).scale(scale).rotate(angle).move_to(center)


def notebook(center=xy(-4.55, -1.58), ruled=True):
    cover = panel(2.90, 2.28, "#CAA976", "#A98560", .12)
    page = panel(2.68, 2.08, PAGE, radius=.11).shift(UP*.06)
    rules = VGroup(*(line((-.98,y),(.98,y),"#C7AB85",1.4) for y in
                     ([-.1,-.47,-.84] if ruled else [])))
    loops = VGroup(*(ArcBetweenPoints(xy(x,-.99),xy(x-.15,-.80),angle=-2.4,
                                      color=WOOD,stroke_width=2) for x in [-1.11,-.64,-.17,.3,.77]))
    title = T("Our guess", 33, INK, weight=BOLD).shift(UP*.54)
    return VGroup(cover, page, rules, loops, title).move_to(center)


def scribble(note, end=.48):
    return ArcBetweenPoints(note.get_center()+xy(-.92,-.30), note.get_center()+xy(end,-.30),
                            angle=.13, color="#355D66", stroke_width=3)


def apple(center, cut=False, scale=1):
    if not cut:
        body = shape([(-.04,.66),(-.67,.84),(-1.05,.42),(-.98,-.28),(-.60,-.86),
                      (-.10,-.81),(.49,-.86),(.91,-.42),(1.03,.25),(.76,.76),(.31,.79)],
                     APPLE,"#8B3430",3)
        stalk = line((-.04,.52),(.12,1.05),WOOD,6)
        blade = leaf(.6,.30).rotate(.43).move_to(xy(.36,.96))
        glint = oval(.23,.60,"#E77965").rotate(-.34).move_to(xy(-.63,.30))
        drawing = VGroup(body, stalk, blade, glint)
    else:
        edge = oval(2.09,2.02,APPLE,"#8B3430",3)
        flesh = oval(1.94,1.86,"#F5DCA3")
        star = Star(n=5,outer_radius=.63,inner_radius=.27,fill_color="#B9855A",
                    fill_opacity=1,stroke_width=0)
        pockets = VGroup(*(oval(.13,.32,SEED).rotate(a).move_to(xy(-.39*np.sin(a),.39*np.cos(a)))
                           for a in np.linspace(0, TAU, 5, endpoint=False)))
        drawing = VGroup(edge,flesh,star,pockets)
    return drawing.scale(scale).move_to(center)


def pepper(center, cut=False, scale=1):
    outline = [(-.12,.82),(-.63,.91),(-.91,.53),(-.88,-.35),(-.61,-.95),
               (-.23,-.94),(.10,-1.01),(.62,-.87),(.83,-.38),(.84,.44),(.56,.91)]
    body = shape(outline, PEPPER, "#AB7633", 3)
    stalk = ArcBetweenPoints(xy(-.03,.76),xy(.24,1.28),angle=-.68,color=POD,stroke_width=9)
    if cut:
        flesh = shape(outline, "#FCE4A0", "#BC8638", 2).scale(.82)
        pith = shape([(-.58,.57),(0,.78),(.54,.6),(.20,.46),(.07,-.54),(-.11,.21)],"#FFF2D4")
        inside = VGroup(flesh, pith, *(oval(.17,.12,"#D5AD67").rotate(i*.5).move_to(xy(x,y))
                                      for i,(x,y) in enumerate([(-.35,.38),(-.15,.28),(.14,.43),(.35,.42),(.22,.19)])))
    else:
        inside = VGroup(*(ArcBetweenPoints(xy(x,.63),xy(x+.03,-.76),angle=.45,
                                          color="#F6CF72",stroke_width=5) for x in [-.42,.15,.49]))
    return VGroup(body, inside, stalk).scale(scale).move_to(center)


def board(center=ORIGIN, scale=1):
    base = panel(7.5,5.14,"#BC8E63","#8B6246",.38)
    bevel = panel(7.12,4.78,"#C99D71","#D8B38B",.30)
    grip = panel(1.1,.24,TABLE,"#946C4E",.1).move_to(xy(0,2.03))
    return VGroup(base,bevel,grip).scale(scale).move_to(center)


def knife(center, angle=0, scale=1):
    blade = Polygon(xy(-.76,.26),xy(1.97,.35),xy(1.81,.04),xy(1.22,-.34),xy(-.76,-.34),
                    fill_color="#DCE5E5",fill_opacity=1,stroke_color="#81999D",stroke_width=2)
    handle = panel(1.48,.55,"#354249","#607378",.15).move_to(xy(-1.39,-.04))
    studs = VGroup(*(Dot(xy(x,-.04),radius=.046,color=RIM) for x in [-1.78,-1.06]))
    return VGroup(blade,handle,studs).scale(scale).rotate(angle).move_to(center)


def seed(w=.28, h=.44, color=SEED):
    return shape([(0,.5),(.34,.05),(.25,-.41),(-.12,-.5),(-.35,-.17)],
                 color, "#9C734F", 1.5).stretch_to_fit_width(w).stretch_to_fit_height(h)


def cat(center, scale=1):
    body = oval(1.21,1.05,"#AE7557","#794F40").shift(DOWN*.35)
    tail = ArcBetweenPoints(xy(.36,-.73),xy(1.08,-.19),angle=1.9,color="#AE7557",stroke_width=12)
    ears = VGroup(*(Polygon(xy(s*.10,.65),xy(s*.50,1.12),xy(s*.63,.48),
                           fill_color="#AE7557",fill_opacity=1,stroke_color="#794F40",stroke_width=2)
                    for s in [-1,1]))
    face = oval(1.25,1.03,"#BC8668","#794F40").shift(UP*.36)
    eyes = VGroup(Dot(xy(-.22,.46),radius=.06,color=INK),Dot(xy(.22,.46),radius=.06,color=INK))
    nose = oval(.16,.10,"#71463E").move_to(xy(0,.25))
    whiskers = VGroup(*(line((s*.42,.24),(s*.70,y),"#794F40",1.4)
                        for s in [-1,1] for y in [.16,.32]))
    return VGroup(tail, body, ears, face, eyes, nose, whiskers).scale(scale).move_to(center)


def caterpillar(center):
    segments = VGroup(*(oval(.61,.61,"#83AB5D",POD).move_to(xy(x,y)) for x,y in
                        [(-1,-.45),(-.61,-.58),(-.20,-.56),(.22,-.48),(.58,-.30),(.83,-.03)]))
    head = oval(.68,.72,"#A7BF67",POD).move_to(xy(1.04,.27))
    eyes = VGroup(Dot(xy(.94,.35),radius=.045,color=INK),Dot(xy(1.17,.35),radius=.045,color=INK))
    antennae = VGroup(line((.91,.57),(.80,.83),POD,2),line((1.15,.56),(1.3,.79),POD,2))
    return VGroup(segments, head, eyes, antennae).move_to(center)


def butterfly(center):
    left = shape([(-.06,.07),(-.58,1.05),(-1.04,.94),(-1.07,.30),(-.74,.03),
                  (-.92,-.48),(-.58,-.73),(-.21,-.48)],"#DE9351","#96583C",2.5)
    spot = oval(.33,.46,"#F6CD83").rotate(.36).move_to(xy(-.63,.48))
    wing = VGroup(left,spot)
    right = wing.copy().flip(UP,about_point=ORIGIN)
    body = oval(.17,.99,"#684E44")
    antennae = VGroup(line((-.04,.41),(-.25,.76),WOOD,2),line((.04,.41),(.25,.76),WOOD,2))
    return VGroup(wing,right,body,antennae).move_to(center)


def family_art(center):
    return VGroup(cat(xy(-1.08,.22),1.11),cat(xy(.66,-.23),.66),
                  cat(xy(2.04,-.61),.53)).move_to(center)


def insect_art(center):
    return VGroup(caterpillar(xy(-1.25,-.78)).scale(.68),
                  butterfly(xy(1.05,.52)).scale(.92)).move_to(center)


def book(center=xy(0,.08)):
    cover = panel(10,4.6,"#9B654A","#C5956B",.23)
    left = panel(4.81,4.28,PAGE,"#E2D0AA",.16).move_to(xy(-2.42,.08))
    right = left.copy().move_to(xy(2.42,.08))
    gutter = line((0,-2.05),(0,2.19),"#C1A280",3)
    edges = VGroup(*(line((a,-1.93-i*.07),(b,-1.93-i*.07),"#C1A280",1)
                     for a,b in [(-4.58,-.32),(.32,4.58)] for i in range(2)))
    return VGroup(cover,left,right,gutter,edges).move_to(center)


def book_pictures():
    return family_art(xy(-2.46,.07)), insect_art(xy(2.46,.07))


def bowl(center):
    return VGroup(oval(3.0,2.35,"#559799","#AFD0C8",3),
                  oval(2.60,1.92,"#37656C","#89B5B2",2),
                  *(pea(.37).move_to(xy(x,y)) for x,y in [(-.66,.35),(-.2,.42),(.24,.22),(-.41,-.27),(.08,-.22)]),
                  *(seed(.17,.27).move_to(xy(x,y)) for x,y in [(.63,.28),(.56,-.33),(.84,-.09)])).move_to(center)


def phone(center):
    return VGroup(panel(2.38,3.8,"#213537","#B1C1BE",.28),
                  panel(2.04,3.34,"#213537","#698889",.21),
                  T("911",66,TEXT,weight=BOLD),
                  panel(.63,.08,GREY,radius=.04).shift(DOWN*1.56)).move_to(center)


def crossed_mouth(center):
    lips = shape([(-.92,-.04),(-.40,.24),(0,.16),(.36,.24),(.92,-.04),
                  (.46,-.37),(0,-.41),(-.50,-.30)],"#B47162","#713C37",2)
    slash = line((-.87,-.93),(.87,.92),RED,8)
    ring = Circle(radius=1.29,color=RED,stroke_width=6)
    return VGroup(lips,line((-.70,-.08),(.70,-.08),"#713C37",3),ring,slash).move_to(center)


def washing():
    basin = panel(8,4.75,"#8CAEB2","#BCD2CE",.48)
    well = panel(7.22,3.97,"#3F737D","#B2CECB",.64)
    tap = VGroup(panel(.53,.72,"#BBCECA","#829EA0",.2).move_to(xy(0,1.47)),
                 oval(.66,.24,"#D2DFD9","#829EA0").move_to(xy(0,1.16)))
    hands = VGroup(hand(xy(-.95,-.18),-.60,1.21),hand(xy(.93,-.23),.70,1.18))
    foam = VGroup(*(Circle(radius=r,color="#D4F1E7",stroke_width=2.2,fill_color="#BDE0E1",fill_opacity=.69)
                    .move_to(xy(x,y)) for x,y,r in [(-.58,.02,.29),(-.22,-.16,.31),(.21,.07,.37),
                    (.62,-.15,.27),(.54,.37,.22),(-.18,.36,.23),(-.83,.44,.15),(.9,.47,.11),(.12,.72,.14)]))
    return VGroup(basin,well,tap), hands, foam


def predict_world():
    return VGroup(plate(REVEAL_PLATE), pea_row(REVEAL_PLATE),
                  ruler(REVEAL_PLATE+xy(0,-1.7), -.105))


def predict_question():
    return question_card("Next to a ruler,\nwhat will you see?", left=-6.18, y=.34,
                         size=35, max_w=3.55, color=YELLOW).question


def measured_world():
    measure = ruler(REVEAL_PLATE+xy(0,-.48))
    row = pea_row(REVEAL_PLATE, varied=True)
    baseline = measure.get_top()[1] + .07
    for sample in row:
        sample.shift(UP * (baseline - sample.get_bottom()[1]))
    return VGroup(plate(REVEAL_PLATE), row, measure)


class S01Hook(SpokenScene):
    def construct(self):
        p = plate()
        base, lid = pod_valves()
        base.move_to(ORIGIN_PLATE+DOWN*.22)
        lid.move_to(ORIGIN_PLATE+DOWN*.12)
        q = question_card("All the same?", y=2.70, size=50, color=YELLOW).question.move_to(xy(0,2.70))
        self.add(table(), p, base, lid)
        self.at("are all the peas")
        self.play(FadeIn(q, shift=UP*.10), run_time=.7)
        self.at("they can look")
        peas = pea_row(ORIGIN_PLATE,y=-.10,step=1.06)
        self.play(lid.animate.shift(UP*.55).rotate(.032), run_time=.78)
        self.play(FadeIn(peas),lid.animate.shift(UP*.17).rotate(.013),run_time=.82)
        self.at("a ruler can")
        example = ruler(xy(0,-2.23),-.08).scale(.79)
        self.play(FadeIn(example, shift=UP*.4), run_time=.92)
        self.at("look for differences")
        self.play(FadeOut(q),FadeOut(example, shift=DOWN*.20),run_time=.58)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Like Their Parents, Not the Same"
    TITLE = "Like Their Parents, Not the Same: Parent Guide"

    def construct(self):
        p, shells = plate(), pod(opened=True)
        self.add(table(),p,shells)
        title = T(self.TITLE, 42, TEXT, font=TITLE_FONT).move_to(xy(0,2.58))
        self.play(FadeIn(title,shift=UP*.13),run_time=.46)
        for i,m in enumerate(shells[-1]):
            bob(m,amp=.025,speed=4.08,seed=i)
        self.wait(1.54)


class S03Payoff(SpokenScene):
    def construct(self):
        shells = pod(opened=True)
        self.add(table(),plate(),shells)
        self.at("here is the idea")
        vine = plant(xy(-4.58,1.68),.82)
        arrow = CurvedArrow(xy(-3.65,1.60),xy(-2.16,.51),angle=-.38,color=GREEN,stroke_width=3)
        self.play(FadeIn(vine,shift=UP*.18), run_time=1.2)
        self.at("offspring the young")
        self.play(Create(arrow),run_time=.8)
        rule = T("Offspring: alike, not identical",38,BLUE).move_to(xy(1.05,2.55))
        self.play(FadeIn(rule),run_time=.55)
        self.at("but not identical")
        self.play(Indicate(shells[-1],color=GREEN,scale_factor=1.085),run_time=1.4)
        self.at("along the way")
        self.play(FadeOut(rule),FadeOut(arrow),FadeOut(vine),run_time=.55)
        labels = [T(t,29,GOLD).move_to(xy(x,2.53)) for t,x in
                  [("Look closely",-3.9),("Measure",0),("Same or different",3.7)]]
        for cue,label in zip(("looking closely","measuring","sorting"),labels):
            self.at(cue)
            self.play(FadeIn(label,shift=UP*.12),
                      shells.animate.shift(RIGHT*.40 if cue == "measuring" else LEFT*.20)
                      .rotate(-.10 if cue == "measuring" else .05),run_time=.60)
        self.at("it takes about")
        self.play(*(FadeOut(label) for label in labels),run_time=.31)
        dial_face = Circle(radius=.35,color=TEAL,stroke_width=3).move_to(xy(-1.77,2.52))
        minute = line((-1.77,2.52),(-1.77,2.28),TEAL,3)
        hour = line((-1.77,2.52),(-1.92,2.55),TEAL,3)
        clock = VGroup(dial_face,hour,minute,T("30 minutes",35,TEXT).move_to(xy(.46,2.52)))
        self.play(FadeIn(clock),run_time=.42)
        self.play(Rotate(minute,-.65,about_point=xy(-1.77,2.52)),run_time=.8)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        produce = VGroup(*(pod(xy(-3.27,y)).scale(.55).rotate(a) for y,a in
                           [(1.38,.19),(.22,-.09),(-.99,.10)]))
        a = apple(xy(.73,.52),scale=1.27)
        bell = pepper(xy(3.65,.48),scale=1.28)
        self.add(table())
        self.at("set out three")
        self.play(LaggedStart(*(FadeIn(p,shift=RIGHT*.42) for p in produce),lag_ratio=.22),run_time=1.79)
        self.at("an apple")
        self.play(FadeIn(a,shift=UP*.25),run_time=.65)
        self.at("sweet bell pepper")
        self.play(FadeIn(bell,shift=UP*.25),run_time=.7)
        self.at("add a ruler")
        p = plate(xy(-2.44,-.17)).scale(.68)
        ruler_prop = ruler(xy(2.62,-1.05),-.14).scale(.60)
        pen = pencil(xy(3.04,-1.72))
        self.play(FadeOut(produce),FadeOut(a),FadeOut(bell),FadeIn(ruler_prop),run_time=.59)
        self.at("paper plate")
        self.play(FadeIn(p,shift=RIGHT*.30),run_time=.60)
        self.at("pencil")
        self.play(FadeIn(pen,shift=LEFT*.23),run_time=.42)
        self.at("cutting board")
        surface = board(xy(3.15,1.45),.55)
        cutter = knife(xy(3.20,1.22),-.20,.63)
        grown = hand(cutter[1].get_center()+UP*.32,PI-.20,.47,pose="curl")
        self.play(FadeIn(surface,shift=LEFT*.36),run_time=.57)
        self.at("knife")
        self.play(FadeIn(cutter,shift=LEFT*.36),FadeIn(grown,shift=LEFT*.36),run_time=.4)
        self.at("animal family pictures")
        picture_book = book(xy(-1.35,.08)).scale(.85)
        family, insects = book_pictures()
        family.scale(.81).move_to(xy(-3.47,.06))
        insects.scale(.80).move_to(xy(.65,.06))
        self.play(FadeOut(p),FadeOut(ruler_prop),FadeOut(pen),FadeOut(surface),FadeOut(cutter),
                  FadeOut(grown),FadeIn(picture_book),run_time=.65)
        self.play(FadeIn(family),FadeIn(insects),run_time=.50)
        self.at("set out five")
        branch = twig(xy(.03,.01),2.05)
        self.play(FadeOut(picture_book),FadeOut(family),FadeOut(insects),
                  FadeIn(branch,shift=DOWN*.15),run_time=.88)
        self.at("one tree")
        self.play(Rotate(branch,.13),run_time=1.22)
        self.at("safe to touch")
        self.play(branch.animate.shift(UP*.11),run_time=.81)
        self.finish()


class S14Safety(SpokenScene):
    def construct(self):
        p = plate(xy(-.83,-.32))
        grown = hand(xy(-1.71,1.64),PI-.32,1.12).set_z_index(2)
        child = hand(xy(-2.53,-1.50),-.42,.79,adult=False)
        self.add(table(),p)
        self.at("stay with your child")
        self.play(FadeIn(grown,shift=DOWN*.55),FadeIn(child,shift=UP*.40),run_time=1.22)
        self.at("you do all the cutting")
        worktop = board(xy(4.90,.48),.42)
        cutter = knife(xy(4.90,.14),-.28,.63).set_z_index(1)
        grasp = hand(cutter[1].get_center()+UP*.42,PI-.28,.68,pose="curl").set_z_index(2)
        self.play(FadeIn(worktop),run_time=.55)
        self.play(Transform(grown,grasp),FadeIn(cutter,shift=LEFT*.24),run_time=.92)
        self.at("peas and seeds")
        dish = bowl(xy(-.42,.25))
        caution = boxed_label("Choking hazard under 4", RED, 33).move_to(xy(-.20,2.66))
        self.play(FadeOut(worktop),FadeOut(cutter),FadeIn(dish),run_time=.73)
        self.at("choking hazards")
        self.play(FadeIn(caution),run_time=.59)
        self.at("keep them out")
        self.play(dish.animate.move_to(xy(3.93,1.29)),grown.animate.move_to(xy(4.77,1.78)),
                  run_time=.94)
        self.at("call 911")
        mobile = phone(xy(.05,-.13))
        emergency = boxed_label("Choking: call 911",RED,36).move_to(xy(.05,2.64))
        self.play(FadeOut(caution),FadeOut(p),FadeOut(child),FadeOut(dish),FadeOut(grown),run_time=.30)
        self.play(FadeIn(mobile,shift=UP*.23),FadeIn(emergency),run_time=.75)
        self.at("keep leaves and seeds")
        stop = crossed_mouth(xy(.1,-.04))
        samples = VGroup(leaf(2.4,1.17).rotate(.5).move_to(xy(-3.44,-.05)),
                         seed(.75,1.15).rotate(-.21).move_to(xy(3.12,-.07)))
        self.play(FadeOut(mobile),FadeOut(emergency),FadeIn(samples),run_time=.56)
        self.play(FadeIn(stop,scale=.86),run_time=.62)
        self.finish()


class S15SafetyFood(SpokenScene):
    def construct(self):
        left = pea(.92).move_to(xy(-4.20,.15))
        peanut = shape([(-.27,.62),(.13,.63),(.37,.33),(.27,.02),(.45,-.28),(.28,-.62),
                        (-.22,-.64),(-.41,-.34),(-.26,-.01),(-.42,.26)],"#D6AC76",WOOD,2)
        peanut.move_to(xy(-1.99,.10))
        a = apple(xy(.56,.16))
        bell = pepper(xy(3.63,.15))
        options = VGroup(left,peanut,a,bell)
        p = plate(xy(0,.05)).stretch_to_fit_width(11.76)
        self.add(table(),p)
        self.at("check for pea")
        self.play(LaggedStart(*(FadeIn(m,shift=UP*.24) for m in options),lag_ratio=.43),run_time=2.4)
        self.at("allergies first")
        allergy = T("Check for allergies",38,RED,weight=BOLD).move_to(xy(0,2.87))
        self.play(FadeIn(allergy),run_time=.55)
        self.at("a child with an allergy")
        adult = hand(xy(2.77,-1.99),-.64,.62)
        young = hand(xy(-3.51,-1.94),.28,.54,adult=False)
        self.play(FadeIn(young,shift=UP*.28),FadeIn(adult,shift=UP*.28),run_time=.90)
        self.at("you handle the samples")
        self.play(adult.animate.shift(UP*.38),run_time=1.38)
        self.at("sweet bell pepper")
        self.play(FadeOut(allergy),FadeOut(adult),FadeOut(young),FadeOut(left),FadeOut(peanut),FadeOut(a),
                  bell.animate.move_to(xy(-1.70,.16)).scale(1.46),run_time=1.20)
        self.at("skip hot peppers")
        hot = shape([(-1.15,-.64),(-.45,-.48),(.23,-.01),(.29,.49),(.62,.64),
                     (.94,.36),(.83,-.23),(.15,-.67),(-.50,-.76)],APPLE,"#8E3A38",2).move_to(xy(2.2,.05))
        bar = line((1.32,-.87),(3.02,.96),RED,6)
        self.play(FadeIn(hot),Create(bar),run_time=.78)
        self.at("wash the produce")
        sink, hands, suds = washing()
        self.play(FadeOut(p),FadeOut(bell),FadeOut(hot),FadeOut(bar),FadeIn(sink),FadeIn(hands),run_time=.67)
        self.play(hands.animate.shift(UP*.21),FadeIn(suds,shift=UP*.31),run_time=1.50)
        self.at("keep activity samples")
        clean_plate = plate()
        washed = VGroup(pod(xy(-1,-.59)).scale(.51),apple(xy(1.4,-.55),scale=.66),
                        pepper(xy(2.49,-.56),scale=.64))
        carrier = hand(xy(2.37,-1.68),-.33,.56)
        cap = T("Samples, not snacks",37,GOLD).move_to(xy(0,2.68))
        self.play(FadeOut(sink),FadeOut(hands),FadeOut(suds),run_time=.24)
        self.play(FadeIn(clean_plate),FadeIn(washed,shift=UP*.31),
                  FadeIn(carrier,shift=UP*.31),run_time=.65)
        self.play(FadeOut(carrier,shift=DOWN*.28),FadeIn(cap),run_time=.61)
        self.finish()


class S05PredictChild(SpokenScene):
    def construct(self):
        p = plate(REVEAL_PLATE)
        closed = pod(REVEAL_PLATE).scale(.9)
        holder = hand(xy(2.88,-1.38),-.65,.92)
        self.add(table(),p,closed,holder)
        self.at("hold up a closed pod")
        self.play(closed.animate.shift(UP*.55).rotate(.16),
                  holder.animate.shift(UP*.55).rotate(.16),run_time=1.17)
        self.at("and ask")
        q = question_card("Will they all be the same?",y=2.70,size=40).question.move_to(xy(0,2.70))
        self.play(FadeIn(q,shift=UP*.12),run_time=.56)
        self.at("write down")
        note = notebook()
        writing = scribble(note)
        pen = pencil(xy(-4.57,-2.30),PI,.39)
        self.play(FadeIn(note,shift=RIGHT*.38),run_time=.64)
        tip_start = writing.get_start()
        pen.shift(tip_start-pen.get_left()+DOWN*.05+RIGHT*.04)
        self.play(FadeIn(pen),run_time=.31)
        self.play(Create(writing),pen.animate.shift(RIGHT*.99),run_time=1.26)
        self.at("check it together")
        self.play(FadeOut(pen,shift=DOWN*.28),closed.animate.shift(DOWN*.55).rotate(-.16),
                  FadeOut(holder,shift=DOWN*.54),run_time=1.12)
        self.finish()


class S06OpenLineUp(SpokenScene):
    def construct(self):
        p = plate(REVEAL_PLATE)
        pod_center = REVEAL_PLATE+UP*.36
        base,lid = pod(pod_center).scale(.9)
        peas = pea_row(pod_center,y=-.1,step=1.06)
        left = hand(xy(.37,1.02),-2.65,.76,adult=False,pose="thumb")
        right = hand(xy(1.20,-1.28),.03,.76,adult=False,pose="thumb")
        self.add(table(),p,base,lid)
        self.at("child split")
        self.play(FadeIn(left,shift=DOWN*.35),FadeIn(right,shift=UP*.35),run_time=.67)
        self.play(lid.animate.shift(UP*.42).rotate(.03),left.animate.shift(UP*.15),
                  right.animate.shift(DOWN*.12),run_time=.55)
        self.play(FadeIn(peas),lid.animate.shift(UP*.28).rotate(.02),left.animate.shift(UP*.25),
                  right.animate.shift(DOWN*.25),run_time=.53)
        self.at("line up the peas")
        row = pea_row(REVEAL_PLATE,y=-.55)
        self.play(FadeOut(left),FadeOut(right),
                  LaggedStart(*(m.animate.move_to(goal) for m,goal in zip(peas,row)),lag_ratio=.18),
                  VGroup(base,lid).animate.scale(.75).shift(UP*.47),run_time=2.0)
        self.at("in the order")
        self.play(LaggedStart(*(Indicate(m,color=PEAS,scale_factor=1.12) for m in peas),lag_ratio=.36),
                  run_time=1.61)
        self.at("count those peas")
        marks = VGroup(*(T(str(i),29,INK,weight=BOLD).move_to(m.get_center()+DOWN*.64)
                         for i,m in enumerate(peas,1)))
        self.play(LaggedStart(*(FadeIn(mark,shift=UP*.12) for mark in marks),lag_ratio=.28),
                  run_time=1.1)
        self.at("then count the peas")
        second_center = xy(-4.45,.12)
        second = pod(second_center,count=3,opened=True).scale(.67)
        self.play(FadeIn(second,shift=RIGHT*.30),run_time=1.14)
        self.play(LaggedStart(*(Indicate(m,color=PEAS,scale_factor=1.14) for m in second[-1]),lag_ratio=.25),
                  run_time=1.0)
        self.at("the numbers often differ")
        one = T("5 peas",40,GOLD).move_to(xy(1.78,2.73))
        two = T("3 peas",40,GOLD).move_to(xy(-4.45,1.50))
        self.play(FadeIn(one),FadeIn(two),run_time=.60)
        self.finish()


class S07PredictParent(SpokenScene):
    def construct(self):
        p, peas, measure = predict_world()
        self.add(table(),p,peas.shift(DOWN*.77))
        self.at("now a question")
        self.play(peas.animate.shift(UP*.77),run_time=2.1)
        self.at("the peas look like twins")
        self.play(LaggedStart(*(Indicate(m,color=PEAS,scale_factor=1.09) for m in peas),lag_ratio=.26),
                  run_time=1.56)
        self.at("when you lay them")
        self.play(FadeIn(measure,shift=UP*.48),run_time=1.25)
        self.at("what do you expect")
        self.play(FadeIn(predict_question(),shift=RIGHT*.19),run_time=.73)
        # A last slow rock lands exactly on the pose used during the pause.
        angles = [m.copy() for m in peas]
        def rock(group, alpha):
            for index, (m, original) in enumerate(zip(group,angles)):
                m.become(original).rotate((-1)**index * .15 * np.sin(PI*alpha))
        self.play(UpdateFromAlphaFunc(peas,rock,rate_func=linear),
                  measure.animate(rate_func=lambda a: np.sin(PI*a)).shift(UP*.60),run_time=1.51)
        self.finish()


class S08PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(table(),predict_world(),predict_question())
        self.wait(4.5)


class S09MeasureReveal(SpokenScene):
    def construct(self):
        p, peas, rule = predict_world()
        q = predict_question()
        self.add(table(),p,peas,rule,q)
        self.at("measure each pea")
        aligned = measured_world()
        self.play(FadeOut(q,run_time=.45,rate_func=linear),Transform(rule,aligned[2],run_time=1.32))
        self.play(Transform(peas,aligned[1]),run_time=1.06)
        self.at("most garden peas")
        unit = ruler_unit(aligned[2].get_center())
        self.play(Create(unit[0]),run_time=.75)
        self.at("one centimeter")
        self.play(FadeIn(unit[1]),run_time=.68)
        self.at("a little smaller")
        smaller_peas = VGroup(*peas[1:])
        self.play(smaller_peas.animate.shift(UP*.96),rate_func=there_and_back,run_time=2.10)
        highlights = VGroup()
        labels = VGroup()
        for cue,index,text_,x in [("the biggest",0,"Bigger",-.58),("the smallest",4,"Tiny and flat",4.40),
                                  ("are paler",2,"Paler",1.78)]:
            self.at(cue)
            sample = peas[index]
            ring = oval(sample.width+.24,sample.height+.24,PAPER,"#A16D32",3).set_fill(opacity=0)
            ring.move_to(sample)
            tag = T(text_,32,GOLD).move_to(xy(x,2.72))
            highlights.add(ring)
            labels.add(tag)
            self.play(Create(ring),FadeIn(tag),run_time=.65)
        self.at("then go back")
        note = notebook(ruled=False)
        guess = VGroup(note,scribble(note,end=.17))
        self.play(FadeOut(highlights),FadeOut(labels),FadeOut(unit),FadeIn(guess,shift=RIGHT*.44),run_time=.90)
        self.at("what did the ruler show")
        mark = T("✓ ?",41,POD,weight=BOLD).move_to(note.get_center()+xy(.79,-.41))
        self.play(FadeIn(mark),run_time=.53)
        self.finish()


class S10WhySizes(SpokenScene):
    def construct(self):
        vine = plant(xy(-4.43,1.10),1.29)
        shell = pod(xy(-.24,1.56)).scale(.61)
        p, peas, rule = measured_world()
        self.add(table(),p,peas,rule)
        self.at("came from one plant")
        self.play(FadeIn(vine,shift=UP*.28),run_time=1.05)
        self.at("a bigger pea")
        pair = VGroup(peas[0],peas[-1])
        middle = VGroup(*peas[1:4])
        self.play(FadeOut(middle),FadeIn(shell,shift=DOWN*.21),run_time=.81)
        self.at("the same parent plant")
        label = T("One parent plant",35,BLUE).move_to(xy(-1.05,2.94))
        self.play(FadeIn(label),pair.animate.arrange(RIGHT,buff=.58,aligned_edge=DOWN)
                  .move_to(xy(1.78,.32)),run_time=1.42)
        self.at("much of the difference")
        # One path branches towards both peas. The parcels are schematic.
        ends = [m.get_top()+UP*.08 for m in pair]
        root = xy(-.07,1.11)
        routes = [CubicBezier(root,xy(.7,1.02),end+UP*.39,end,color=POD,stroke_width=2.5)
                  for end in ends]
        self.play(*(Create(path) for path in routes),
                  rule.animate.shift(DOWN*.20),run_time=.88)
        self.at("food reached each pea")
        parcels = [Dot(root,radius=r,color=GOLD) for r in [.12,.075]]
        self.add(*parcels)
        self.play(*(MoveAlongPath(m,path) for m,path in zip(parcels,routes)),
                  pair.animate.scale(1.19),run_time=1.73)
        self.play(*(FadeOut(m,shift=DOWN*.07) for m in parcels),run_time=.42)
        self.finish()


class S11ApplePepperLeaves(SpokenScene):
    def construct(self):
        chopping = board()
        fruit = apple(xy(0,-.20),scale=1.50)
        grip = hand(xy(-1.7,.62),-PI/2,.95,pose="curl")
        blade = knife(xy(.75,-1.31),PI,1.05)
        self.add(table(),chopping,fruit,grip,blade)
        self.at("across its middle")
        self.play(blade.animate.shift(UP*.70),run_time=1.02)
        self.at("reveal a star")
        self.play(FadeOut(fruit),FadeOut(grip,shift=LEFT*.42),FadeOut(blade,shift=DOWN*.42),run_time=.30)
        self.play(FadeIn(apple(xy(-.96,-.07),cut=True,scale=1.33),shift=RIGHT*.29),
                  FadeIn(apple(xy(1.89,-.09),cut=True,scale=1.21),shift=LEFT*.29),run_time=.77)
        halves = VGroup(*self.mobjects[-2:])
        self.at("cut the pepper")
        bell = pepper(xy(.52,-.16),scale=1.45)
        grip = hand(xy(-1.02,-.37),-PI/2,.94,pose="curl")
        blade = knife(xy(1.80,.37),PI/2,.82)
        self.play(FadeOut(halves),run_time=.20)
        self.play(FadeIn(bell),FadeIn(grip),FadeIn(blade),run_time=.25)
        self.at("from top to bottom")
        self.play(blade.animate.shift(LEFT*1.14+DOWN*.50),run_time=1.00)
        inner = pepper(xy(.52,-.16),cut=True,scale=1.52)
        self.play(FadeOut(bell),FadeOut(grip,shift=LEFT*.39),FadeOut(blade,shift=DOWN*.37),
                  FadeIn(inner),run_time=.60)
        self.at("line up five seeds")
        rows = VGroup()
        for i, (y,color) in enumerate([(.62,SEED),(-.95,"#E5C281")]):
            row = VGroup(*(seed(.32+(.07*((j+i)%3)),.54 if i == 0 else .38,color)
                           .rotate(.13*(-1)**j).move_to(xy(-1.14+.84*j,y)) for j in range(5)))
            fruit_thumb = (apple if i == 0 else pepper)(xy(-2.42,y),cut=True,scale=.46)
            rows.add(VGroup(fruit_thumb,*row))
        self.play(FadeOut(inner),run_time=.26)
        self.play(LaggedStart(*(FadeIn(sample,shift=RIGHT*.16) for row in rows for sample in row),
                             lag_ratio=.12),run_time=1.68)
        self.at("compare their sizes")
        self.play(rows[0][2].animate.scale(1.18),rows[1][2].animate.scale(1.18),
                  rate_func=there_and_back,run_time=1.38)
        self.at("compare the leaves")
        branch = twig(xy(-3.63,.18),.59).rotate(.37)
        leaves = VGroup(*(leaf(w,h).rotate(a).move_to(xy(x,y)) for w,h,a,x,y in
                          [(3.76,1.42,.04,.8,1.24),(2.82,1.12,.17,.61,-.08),(1.82,.71,-.08,.11,-1.21)]))
        self.play(FadeOut(rows),FadeOut(chopping),FadeIn(branch),FadeIn(leaves,shift=RIGHT*.26),run_time=.86)
        self.at("measure the longest")
        rule = ruler(xy(.7,-2.19)).scale(.86)
        longest = leaves[0].get_center()[0]
        interval = lambda a,b,y: VGroup(line((a,y),(b,y),GOLD,3),
                                        line((a,y-.11),(a,y+.11),GOLD,2),
                                        line((b,y-.11),(b,y+.11),GOLD,2))
        top = interval(longest-1.88,longest+1.88,2.31)
        low = interval(-.80,1.02,-1.65)
        self.play(FadeIn(rule,shift=UP*.29),Create(top),run_time=.68)
        self.at("and shortest")
        self.play(Create(low),run_time=.62)
        self.finish()


class S12Animals(SpokenScene):
    def construct(self):
        spread = book()
        cats, bugs = book_pictures()
        self.add(table(),spread)
        self.at("show kittens with their mother")
        self.play(FadeIn(cats[0],shift=UP*.18),run_time=.50)
        self.play(LaggedStart(*(FadeIn(m,shift=RIGHT*.19) for m in cats[1:]),lag_ratio=.25),run_time=1.20)
        self.at("how are they alike")
        self.play(cats[1].animate.scale(1.13),rate_func=there_and_back,run_time=.80)
        self.at("show a caterpillar")
        self.play(FadeIn(bugs[0],shift=RIGHT*.30),run_time=.62)
        self.at("and a butterfly")
        self.play(FadeIn(bugs[1],scale=.85),run_time=.82)
        self.at("sort the pictures")
        mats = TwoPanel("Look alike at first", "Look different at first", colors=(GOLD,TEAL),
                        bottom=-2.11,top=2.06)
        copies = cats.copy().shift(DOWN*.50), bugs.copy().shift(DOWN*.50)
        self.add(*copies)
        self.play(FadeOut(spread),FadeOut(cats),FadeOut(bugs),run_time=.42)
        self.play(FadeIn(mats),run_time=.59)
        self.at("babies that look like")
        self.play(copies[0].animate.move_to(xy(-3.16,-.51)).scale(1.12),run_time=1.56)
        self.at("babies that look different")
        self.play(copies[1].animate.move_to(xy(3.16,-.51)).scale(1.18),run_time=1.70)
        self.finish()


class S13KindRule(SpokenScene):
    def construct(self):
        spread = book()
        cats, bugs = book_pictures()
        front = panel(4.91,4.5,"#9B654A","#C5956B",.24).move_to(xy(2.43,.10))
        front_art = cat(xy(2.43,.11),.99)
        closed = VGroup(front,front_art)
        peas = VGroup(plate(),pod(opened=True))
        self.add(table(),spread,cats,bugs)
        self.at("keep the talk")
        self.play(FadeOut(cats),FadeOut(bugs),
                  Transform(spread,closed),run_time=.85)
        self.at("plants and animals")
        self.play(FadeOut(spread,shift=RIGHT*.45),run_time=.32)
        self.play(FadeIn(peas,shift=UP*.30),run_time=.72)
        self.at("do not ask")
        tag = T("Plants and animals only",39,TEAL).move_to(xy(0,2.64))
        self.play(FadeIn(tag),peas.animate.shift(UP*.23),run_time=.77)
        self.at("many children")
        self.play(peas.animate.scale(1.15).rotate(.13),run_time=2.65)
        self.at("blended families")
        self.play(peas.animate.rotate(-.13),run_time=1.10)
        self.at("the question can hurt")
        self.play(FadeOut(tag),peas.animate.shift(DOWN*.23),run_time=.89)
        self.finish()


class S16Return(SpokenScene):
    def construct(self):
        p, peas, measure = measured_world()
        sheet = notebook()
        guess = VGroup(sheet,scribble(sheet))
        self.add(table(),p,peas,measure)
        self.at("return to your")
        self.play(FadeIn(guess,shift=RIGHT*.30),run_time=.83)
        self.at("have them show you")
        child = hand(xy(-1.35,-1.52),-.33,.75,adult=False,pose="point")
        self.play(FadeIn(child,shift=UP*.23),run_time=.66)
        self.play(child.animate.shift(RIGHT*2.31).rotate(-.42),run_time=1.69)
        self.at("count the peas and seeds")
        dish = bowl(xy(-4.47,.79)).scale(.75)
        grown = hand(xy(-3.31,1.12),PI+.27,.83)
        self.play(FadeOut(child),FadeOut(guess),FadeIn(dish),FadeIn(grown),run_time=.48)
        self.play(LaggedStart(*(m.animate.scale(.43).move_to(dish.get_center()+xy(.10*j,-.15+.15*(j%2)))
                              for j,m in enumerate(peas)),lag_ratio=.13),run_time=1.15)
        self.at("clear the table")
        self.play(FadeOut(dish,shift=LEFT*.30),FadeOut(grown,shift=LEFT*.30),FadeOut(peas,shift=LEFT*.30),
                  FadeOut(p,shift=DOWN*.23),FadeOut(measure,shift=RIGHT*.23),run_time=1.14)
        self.at("wash everyone's hands")
        sink,hands,foam = washing()
        self.play(FadeIn(sink),FadeIn(hands,shift=UP*.25),run_time=.63)
        self.play(FadeIn(foam,shift=UP*.22),hands.animate.shift(UP*.16),run_time=1.23)
        self.at("peas from")
        p = plate(REVEAL_PLATE)
        pair = pea_row(REVEAL_PLATE,varied=True)
        self.play(FadeOut(sink),FadeOut(hands),FadeOut(foam),run_time=.29)
        self.play(FadeIn(p),FadeIn(pair,shift=UP*.29),run_time=.89)
        self.at("alike in some ways")
        self.play(LaggedStart(*(Indicate(m,color=PEAS,scale_factor=1.09) for m in pair),lag_ratio=.31),
                  run_time=2.0)
        self.finish()


class S17End(EndCard):
    LINE = "Offspring are like their parents, but not identical."
