"""Animal body plans, film 1: similar bodies, different branches (Biochemistrypedia explainer)

COLOUR MAP (one colour per concept, whole film)
  BLUE   = ectoderm / outer layer        ORANGE = mesoderm / muscle / lining
  YELLOW = endoderm / gut lining         WHITE  = gut lumen
  CYAN   = fluid in a body cavity (pale)
  GREEN  = Spiralia   PURPLE = Ecdysozoa   GREY = Deuterostomia
  TEAL   = independent evidence (genes, many body features)
Everything not computed is schematic (cross-sections, tree shape).
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CYAN = "#BDEFF4"
PURPLE = "#B695E0"
WHITE_ = "#FFFFFF"
CREAM = "#EADFC2"
PINK = "#E88FA0"
TAN = "#D9C7A0"

X3 = {"plan": -4.4, "nem": 0.0, "earth": 4.4}
CY = 0.4
RS = 1.8
NAMES = {"plan": "planarian", "nem": "nematode", "earth": "earthworm"}


# ---------------------------------------------------------------- cross-sections
class Sec(VGroup):
    """Schematic cross-section. kind: plan (flat, tissue-filled), nem (pseudocoelom), earth (coelom).
    stage: layers (blue, orange, yellow, white), zone (+ cavity), full (+ lining round the gut for earth)."""

    def __init__(self, kind, R=RS, stage="layers", dots=True):
        super().__init__()
        self.kind, self.R = kind, R
        sy = 0.62 if kind == "plan" else 1.0
        A = lambda a, b, c, z, op=1: Annulus(inner_radius=a * R, outer_radius=b * R, color=c, fill_opacity=op,
                                             stroke_width=0).set_z_index(z).stretch(sy, 1)
        self.ecto = A(.86, 1.0, BLUE, 1)
        self.meso = A(.72, .86, ORANGE, 1)
        self.zone = A(.42, .72, ORANGE if kind == "plan" else CYAN, 2)
        self.inner = A(.42, .50, ORANGE, 3)
        self.yel = A(.30, .42, YELLOW, 4)
        self.lum = Circle(radius=.30 * R, color=WHITE_, fill_opacity=1, stroke_width=0).set_z_index(5).stretch(sy, 1)
        self.edge = Circle(radius=R, color=GREY, stroke_width=3).set_z_index(6).stretch(sy, 1)
        self.dots = VGroup()
        if kind != "plan" and dots and R > 0.85:
            for i in range(7):
                d = Dot(radius=.05, color=WHITE_).set_opacity(.85).set_z_index(3)
                d.ph, d.w, d.rr = i * 0.9, (0.5 + 0.12 * (i % 3)) * (1 if i % 2 else -1), 0.64 + 0.04 * (i % 4)
                d.add_updater(self._orbit(d))
                self.dots.add(d)
        self.add(self.ecto, self.meso, self.yel, self.lum, self.edge)
        if stage in ("zone", "full"):
            self.add(self.zone)
            if kind != "plan":
                self.add(self.dots)
        if stage == "full" and kind == "earth":
            self.add(self.inner)

    def _orbit(self, d):
        def f(m, dt):
            m.ph += m.w * dt
            c = self.lum.get_center()
            s = self.zone.width / 2
            m.move_to(c + np.array([np.cos(m.ph), np.sin(m.ph), 0]) * s * m.rr)
        return f

    def blank(self):
        """Outline only: the layers fade in later, one named colour at a time."""
        for p in (self.ecto, self.meso, self.yel, self.lum):
            p.set_fill(opacity=0)
        return self

    def put(self, x, y, scale=1.0):
        extras = [p for p in (self.zone, self.inner, self.dots) if p not in self.submobjects]
        c0 = self.get_center()
        self.move_to([x, y, 0])
        d = self.get_center() - c0
        for p in extras:
            p.shift(d)
        if scale != 1.0:
            self.scale(scale)
            for p in extras:
                p.scale(scale, about_point=self.get_center())
        return self


def names_row(which=("plan", "nem", "earth"), size=30):
    return {k: T(NAMES[k], size, weight=BOLD).move_to([X3[k], -1.9, 0]) for k in which}


# ---------------------------------------------------------------- worms
def make_worm(kind, y, x0=-4.2, x1=4.2, gut=1.0, amp=0.32, ph0=0.0, speed=2.0):
    """A wriggling worm built from a computed sine path. Ends stay put (amplitude is zero at both ends)."""
    N = 70
    u = np.linspace(0, 1, N)
    wid, col = (0.18, CREAM) if kind == "nem" else (0.5, PINK)
    body = VMobject(color=col, stroke_width=wid * 100).set_cap_style(CapStyleType.ROUND)
    gutl = VMobject(color=WHITE_, stroke_width=7).set_z_index(3)
    rings = VGroup(*[Line(ORIGIN, UP, color=BG, stroke_width=3) for _ in range(14)]) if kind == "earth" else VGroup()
    g = VGroup(body, gutl, rings)
    g.gfrac = ValueTracker(gut)
    g.t = ph0
    k = 2.0 if kind == "nem" else 1.4

    def path(t):
        env = np.sin(np.pi * u)
        return np.stack([x0 + (x1 - x0) * u,
                         y + amp * (1.4 if kind == "nem" else 0.8) * env * np.sin(2 * np.pi * k * u - t), 0 * u], 1)

    def upd(m, dt):
        m.t += dt * speed
        P = path(m.t)
        body.set_points_smoothly(P)
        n = int(m.gfrac.get_value() * N)
        if n >= 3:
            gutl.set_points_smoothly(P[:n]).set_stroke(opacity=1)
        else:
            gutl.set_points_as_corners([P[0], P[0] + RIGHT * .001]).set_stroke(opacity=0)
        for i, r in enumerate(rings):
            j = int((i + 1) / (len(rings) + 1) * (N - 1))
            tg = P[min(j + 1, N - 1)] - P[max(j - 1, 0)]
            nv = np.array([-tg[1], tg[0], 0])
            nv = nv / (np.linalg.norm(nv) + 1e-9) * 0.2
            r.put_start_and_end_on(P[j] - nv, P[j] + nv)
    g.add_updater(upd)
    upd(g, 0)
    return g


def planarian_worm(x, y, w=3.4):
    body = Ellipse(width=w, height=.8, color=TAN, fill_opacity=1, stroke_width=0)
    e = VGroup(Dot(radius=.06, color=BG).move_to(body.get_center() + [w * .3, .12, 0]),
               Dot(radius=.06, color=BG).move_to(body.get_center() + [w * .3, -.12, 0]))
    g = VGroup(body, e).move_to([x, y, 0])
    g.base = y
    g.t = 0.0

    def sway(m, dt):
        m.t += dt
        m.move_to([m.get_x(), m.base + .06 * np.sin(m.t * 3), 0])
    g.add_updater(sway)
    return g


def pulse(m, amp=0.08, period=1.6):
    m.pt = 0.0
    m.pl = 1.0

    def f(mm, dt):
        mm.pt += dt
        k = 1 + amp * np.sin(2 * np.pi * mm.pt / period)
        mm.scale(k / mm.pl)
        mm.pl = k
    m.add_updater(f)
    return m


class Sc(SpokenScene):
    """SpokenScene with slow drifting motes behind everything, so a held frame is never a dead frame."""

    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        W, H = config.frame_width, config.frame_height
        motes = VGroup()
        for _ in range(40):
            d = Dot(radius=rng.uniform(0.04, 0.08), color=rng.choice([TEAL, TEXT, GOLD])).set_opacity(rng.uniform(0.25, 0.5))
            d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.7, 3.7), 0])
            d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

            def drift(m, dt, W=W, H=H):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 3.8:
                    m.shift(DOWN * 7.6)
                if abs(m.get_x()) > 6.8:
                    m.shift(LEFT * 13.6 * (1 if m.get_x() > 0 else -1))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


# ================================================================ SCENES
class S00Title(TitleCard):
    TITLE = "Similar Bodies, Different Branches"
    LESSON = "Animal Body Plans"


class S01Question(Sc):
    def construct(self):
        nem = make_worm("nem", 1.6, gut=0.0, speed=2.2)
        earth = make_worm("earth", -1.3, gut=0.0, ph0=1.0, speed=1.6)
        ln = T("nematode", 34, weight=BOLD).move_to([0, 2.75, 0])
        le = T("earthworm", 34, weight=BOLD).move_to([0, -2.55, 0])
        self.add(nem, earth)
        self.play(FadeIn(nem), FadeIn(earth), run_time=0.4)
        self.at("nematode")
        self.play(FadeIn(ln, shift=DOWN * .1), run_time=0.5)
        self.at("earthworm")
        self.play(FadeIn(le, shift=UP * .1), run_time=0.5)
        self.at("are they close relatives")
        q = T("?", 110, color=YELLOW, weight=BOLD).move_to([0, 0.15, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        pulse(q, 0.12, 1.2)
        self.at("both are soft")
        self.play(Indicate(nem, scale_factor=1.0, color=WHITE_), Indicate(earth, scale_factor=1.0, color=WHITE_), run_time=1.4)
        self.at("each has a gut")
        self.play(FadeOut(q), run_time=0.4)
        mouth = [T("mouth", 30, color=WHITE_).move_to([-5.75, y, 0]) for y in (1.6, -1.3)]
        anus = [T("anus", 30, color=WHITE_).move_to([5.7, y, 0]) for y in (1.6, -1.3)]
        self.play(nem.gfrac.animate.set_value(1), earth.gfrac.animate.set_value(1), run_time=1.5, rate_func=linear)
        self.play(*[FadeIn(m) for m in mouth], run_time=0.4)
        self.at("anus")
        self.play(*[FadeIn(a) for a in anus], run_time=0.4)
        self.finish()


class S02Slice(Sc):
    def construct(self):
        nem = make_worm("nem", 1.6, speed=2.2)
        earth = make_worm("earth", -1.3, ph0=1.0, speed=1.6)
        ln = T("nematode", 34, weight=BOLD).move_to([0, 2.75, 0])
        le = T("earthworm", 34, weight=BOLD).move_to([0, -2.55, 0])
        self.add(nem, earth, ln, le)
        names = names_row()
        cut1 = DashedLine([0, 2.25, 0], [0, 0.95, 0], color=WHITE_, stroke_width=6)
        cut2 = DashedLine([0, -0.65, 0], [0, -1.95, 0], color=WHITE_, stroke_width=6)
        self.wait(0.15)
        self.play(Create(cut1), Create(cut2), run_time=0.9)
        sn = Sec("nem", stage="layers").blank().put(X3["nem"], CY)
        se = Sec("earth", stage="layers").blank().put(X3["earth"], CY)
        self.play(FadeOut(nem), FadeOut(earth), FadeOut(ln), FadeOut(le), FadeOut(cut1), FadeOut(cut2),
                  FadeIn(sn, scale=0.3), FadeIn(se, scale=0.3), run_time=1.4)
        self.play(FadeIn(names["nem"]), FadeIn(names["earth"]), run_time=0.5)
        self.at("add a third worm")
        pw = planarian_worm(-9.0, 2.95)
        self.add(pw)
        self.play(pw.animate.move_to([X3["plan"], 2.95, 0]), run_time=1.4)
        pw.base = 2.95
        self.at("flat planarian")
        cut = DashedLine([X3["plan"], 3.5, 0], [X3["plan"], 2.4, 0], color=WHITE_, stroke_width=6)
        sp = Sec("plan", stage="layers").blank().put(X3["plan"], CY)
        self.play(Create(cut), run_time=0.5)
        self.play(FadeOut(pw), FadeOut(cut), FadeIn(sp, scale=0.3), FadeIn(names["plan"]), run_time=1.0)
        self.at("now color the tissue layers")
        secs = [sp, sn, se]
        self.play(*[Indicate(s, scale_factor=1.04, color=WHITE_) for s in secs], run_time=1.5)
        sch = T("schematic", 26, color=TEXT).move_to([5.7, -3.45, 0])
        self.play(FadeIn(sch), run_time=0.4)
        self.at("outer layer is blue")
        c1 = chip("outer layer", BLUE, 30).move_to([X3["plan"], 3.3, 0])
        self.play(*[s.ecto.animate.set_fill(opacity=1) for s in secs], FadeIn(c1), run_time=0.8)
        self.at("middle layer")
        self.play(*[s.meso.animate.set_fill(opacity=1) for s in secs], run_time=0.8)
        self.at("mesoderm")
        c2 = chip("mesoderm", ORANGE, 30).move_to([0, 3.3, 0])
        self.play(FadeIn(c2), run_time=0.5)
        self.at("makes muscle")
        c2b = T("makes muscle", 28, color=ORANGE).move_to([0, 2.58, 0])
        self.play(FadeIn(c2b, shift=DOWN * .1), run_time=0.5)
        self.at("gut lining")
        c3 = chip("gut lining", YELLOW, 30).move_to([X3["earth"], 3.3, 0])
        self.play(*[s.yel.animate.set_fill(opacity=1) for s in secs],
                  *[s.lum.animate.set_fill(opacity=1) for s in secs], FadeIn(c3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- critters, DNA, stairs, tree
def critter(name):
    c = VGroup()
    if name == "nem":
        xs = np.linspace(-.3, .3, 20)
        c.add(VMobject(color=CREAM, stroke_width=6).set_points_smoothly([[x, .08 * np.sin(x * 14), 0] for x in xs]))
    elif name == "earth":
        c.add(Line([-.3, 0, 0], [.3, 0, 0], color=PINK, stroke_width=14).set_cap_style(CapStyleType.ROUND))
        for x in np.linspace(-.2, .2, 4):
            c.add(Line([x, -.07, 0], [x, .07, 0], color=BG, stroke_width=2))
    elif name == "plan":
        c.add(Ellipse(width=.6, height=.24, color=TAN, fill_opacity=1, stroke_width=0))
        c.add(Dot(radius=.025, color=BG).move_to([.18, .05, 0]), Dot(radius=.025, color=BG).move_to([.18, -.05, 0]))
    elif name == "arth":
        c.add(Ellipse(width=.46, height=.22, color=CREAM, fill_opacity=1, stroke_width=0))
        c.add(Circle(radius=.09, color=CREAM, fill_opacity=1, stroke_width=0).move_to([.3, 0, 0]))
        for x in (-.12, 0, .12):
            c.add(Line([x, 0, 0], [x - .06, .2, 0], color=CREAM, stroke_width=3),
                  Line([x, 0, 0], [x - .06, -.2, 0], color=CREAM, stroke_width=3))
    elif name == "snail":
        c.add(Line([-.3, -.12, 0], [.3, -.12, 0], color=TAN, stroke_width=9).set_cap_style(CapStyleType.ROUND))
        c.add(Circle(radius=.17, color=CREAM, fill_opacity=1, stroke_width=0).move_to([-.06, .05, 0]))
        c.add(Arc(radius=.08, start_angle=0, angle=4.5, color=BG, stroke_width=2).move_to([-.06, .05, 0]))
    elif name == "urch":
        c.add(Circle(radius=.13, color=CREAM, fill_opacity=1, stroke_width=0))
        for a in np.linspace(0, TAU, 12, endpoint=False):
            c.add(Line([.1 * np.cos(a), .1 * np.sin(a), 0], [.26 * np.cos(a), .26 * np.sin(a), 0], color=CREAM, stroke_width=3))
    elif name == "fish":
        c.add(Ellipse(width=.46, height=.24, color=CREAM, fill_opacity=1, stroke_width=0).shift(RIGHT * .06))
        c.add(Polygon([-.16, 0, 0], [-.34, .13, 0], [-.34, -.13, 0], color=CREAM, fill_opacity=1, stroke_width=0))
    return c


def dna_strand(x0=-6.2, x1=6.2, y=3.3, n=22, size=30):
    seq = "ACGTTGCAAGCTTAGCGTACCA"[:n]
    g = VGroup(*[T(ch, size, color=TEAL, weight=BOLD).move_to([x, y, 0]) for ch, x in zip(seq, np.linspace(x0, x1, n))])
    g.t = 0.0

    def wave(m, dt):
        m.t += dt
        for i, l in enumerate(m):
            l.set_opacity(0.4 + 0.6 * (0.5 + 0.5 * np.sin(m.t * 3.2 - i * 0.6)))
    g.add_updater(wave)
    return g


STEP_X = {"plan": -3.6, "nem": 0.0, "earth": 3.6}
STEP_TOP = {"plan": -2.2, "nem": -1.2, "earth": -0.2}
STEP_DESC = {"plan": "no cavity", "nem": "partial lining", "earth": "full lining"}
STEP_SC = 0.6


def step_blocks(solid=True):
    bl = {}
    for k in ("plan", "nem", "earth"):
        h = STEP_TOP[k] + 3.7
        r = Rectangle(width=3.6, height=h, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16 if solid else 0.05)
        r.move_to([STEP_X[k], -3.7 + h / 2, 0])
        bl[k] = r
    return bl


def step_pos(k):
    r = RS * STEP_SC * (0.62 if k == "plan" else 1.0)
    return [STEP_X[k], STEP_TOP[k] + r, 0]


def step_name(k):
    return T(NAMES[k], 28, weight=BOLD).move_to([STEP_X[k], (STEP_TOP[k] - 3.7) / 2 + 0.3, 0])


def step_desc(k):
    return T(STEP_DESC[k], 28).move_to([STEP_X[k], (STEP_TOP[k] - 3.7) / 2 - 0.25, 0])


def stairs_world(solid=True, text=True):
    bl = step_blocks(solid)
    secs = {k: Sec(k, stage="full").put(*step_pos(k)[:2], scale=STEP_SC) for k in ("plan", "nem", "earth")}
    nm = {k: step_name(k) for k in secs}
    ds = {k: step_desc(k) for k in secs}
    return bl, secs, nm, ds


TIPX = -1.55
TIPY = {"nem": 2.9, "arth": 1.9, "earth": 0.6, "snail": -0.4, "plan": -1.4, "urch": -2.6, "fish": -3.5}
TIPNAME = {"nem": "nematode", "arth": "arthropod", "earth": "earthworm", "snail": "snail", "plan": "planarian",
           "urch": "sea urchin", "fish": "fish"}
ICON = {"nem": "nem", "arth": "earth", "earth": "earth", "snail": "earth", "plan": "plan", "urch": "earth", "fish": "earth"}
COMB_Y = {"earth": 1.4, "nem": 0.2, "plan": -1.0}


def PL(*pts, color=TEXT, w=8):
    return VMobject(color=color, stroke_width=w).set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])


def tip(k, y):
    m = critter(k).move_to([TIPX + 0.45, y, 0])
    n = T(TIPNAME[k], 28).move_to([TIPX + 0.95, y, 0], aligned_edge=LEFT)
    return VGroup(m, n)


def tip_icon(k, y):
    return Sec(ICON[k], R=0.42, stage="full", dots=False).move_to([TIPX + 0.45, y, 0])


def comb_lines():
    return VGroup(PL((-6.5, 0.2), (-5.6, 0.2)),
                  PL((-5.6, 0.2), (-5.6, 1.4), (TIPX, 1.4)),
                  PL((-5.6, 0.2), (-4.2, 0.2), (-4.2, -1.0), (TIPX, -1.0)),
                  PL((-4.2, 0.2), (TIPX, 0.2)))


def t9_lines():
    return {"root": PL((-6.5, .9), (-5.4, .9)),
            "ecdy": VGroup(PL((-5.4, .9), (-5.4, 2.4), (-3.4, 2.4), color=PURPLE),
                           PL((-3.4, 2.4), (-3.4, 2.9), (TIPX, 2.9), color=PURPLE),
                           PL((-3.4, 2.4), (-3.4, 1.9), (TIPX, 1.9), color=PURPLE)),
            "earth": PL((-5.4, .9), (-5.4, .6), (TIPX, .6)),
            "plan": PL((-5.4, .9), (-5.4, -1.4), (TIPX, -1.4))}


def t10_lines():
    dash = lambda m: DashedVMobject(m, num_dashes=18, dashed_ratio=.6)
    return {"spir": VGroup(PL((-5.4, .9), (-5.4, -.4), (-3.6, -.4), color=GREEN),
                           PL((-3.6, -.4), (-3.6, .6), (TIPX, .6), color=GREEN),
                           PL((-3.6, -.4), (TIPX, -.4), color=GREEN),
                           PL((-3.6, -.4), (-3.6, -1.4), (TIPX, -1.4), color=GREEN)),
            "deut": VGroup(dash(PL((-5.9, .9), (-5.9, -3.0), (-3.6, -3.0), color=GREY)),
                           dash(PL((-3.6, -3.0), (-3.6, -2.6), (TIPX, -2.6), color=GREY)),
                           dash(PL((-3.6, -3.0), (-3.6, -3.5), (TIPX, -3.5), color=GREY)))}


def group_labels():
    ec = T("Ecdysozoa", 32, color=PURPLE, weight=BOLD).move_to([4.75, 2.4, 0])
    sp = T("Spiralia", 32, color=GREEN, weight=BOLD).move_to([4.75, -0.4, 0])
    de = VGroup(T("Deuterostomia", 32, color=GREY, weight=BOLD), T("traditional;", 26, color=GREY),
                T("support debated", 26, color=GREY)).arrange(DOWN, buff=0.08).move_to([4.75, -3.05, 0])
    return ec, sp, de


def brackets():
    e = PL((2.55, 3.15), (2.75, 3.15), (2.75, 1.65), (2.55, 1.65), color=PURPLE)
    s = PL((2.55, .85), (2.75, .85), (2.75, -1.65), (2.55, -1.65), color=GREEN)
    d = DashedVMobject(PL((2.55, -2.35), (2.75, -2.35), (2.75, -3.75), (2.55, -3.75), color=GREY), num_dashes=12, dashed_ratio=.6)
    return e, s, d


def moult_tick():
    return PL((-4.4, 2.15), (-4.4, 2.65), color=PURPLE, w=10)


def tree_final(names=True, icons=True, tick=True, labels=True):
    L9, L10 = t9_lines(), t10_lines()
    d = {"root": L9["root"], "ecdy": L9["ecdy"], "spir": L10["spir"], "deut": L10["deut"]}
    if icons:
        d["tips"] = VGroup(*[tip_icon(k, TIPY[k]) for k in TIPY])
        d["names"] = VGroup(*[T(TIPNAME[k], 28).move_to([TIPX + 0.95, TIPY[k], 0], aligned_edge=LEFT) for k in TIPY]) if names else VGroup()
    else:
        tg = [tip(k, TIPY[k]) for k in TIPY]
        d["tips"] = VGroup(*tg)
        d["names"] = VGroup()
    if labels:
        ec, sp, de = group_labels()
        be, bs, bd = brackets()
        d["labels"] = VGroup(ec, sp, de, be, bs, bd)
    else:
        d["labels"] = VGroup()
    d["tick"] = moult_tick() if tick else VGroup()
    d["tickl"] = T("moulting", 28, color=PURPLE).move_to([-4.5, 3.15, 0]) if (tick and names) else VGroup()
    return d


def question_world():
    bl = step_blocks(solid=False)
    sp = Sec("plan", stage="full").put(*step_pos("plan")[:2], scale=STEP_SC)
    ea = Sec("earth", stage="full").put(*step_pos("earth")[:2], scale=STEP_SC)
    nem = Sec("nem", stage="full").put(0, 1.65, scale=0.5)
    rm = DashedVMobject(Circle(radius=1.3, color=YELLOW, stroke_width=4), num_dashes=26).move_to([0, -0.4, 0])
    rmt = T("between?", 28, color=YELLOW).move_to([0, -0.4, 0])
    ro = DashedVMobject(Circle(radius=0.75, color=RED, stroke_width=4), num_dashes=16).move_to([-5.0, 1.6, 0])
    rot = T("?", 48, color=RED, weight=BOLD).move_to([-5.0, 1.6, 0])
    qm = T("?", 56, color=YELLOW, weight=BOLD).move_to([1.6, 1.7, 0])
    gl = T("many genes", 28, color=TEAL).move_to([-4.8, 2.65, 0])
    return dict(bl=bl, plan=sp, earth=ea, nem=nem, rm=rm, rmt=rmt, ro=ro, rot=rot, qm=qm, gl=gl)


def pulse(m, amp=0.08, period=1.6):
    m.pt = 0.0
    m.pl = 1.0

    def f(mm, dt):
        mm.pt += dt
        k = 1 + amp * np.sin(2 * np.pi * mm.pt / period)
        mm.scale(k / mm.pl)
        mm.pl = k
    m.add_updater(f)
    return m


def check(x, y, color=PURPLE, s=0.28):
    return PL((x - s, y), (x - s * .3, y - s * .8), (x + s, y + s * .8), color=color, w=10)


def crossmark(x, y, color=RED, s=0.26):
    return VGroup(PL((x - s, y - s), (x + s, y + s), color=color, w=10), PL((x - s, y + s), (x + s, y - s), color=color, w=10))


# ================================================================ SCENES 03 +
def base_row(stage, stages=None):
    secs = {k: Sec(k, stage=(stages or {}).get(k, stage)).put(X3[k], CY) for k in X3}
    return secs, names_row()


class S03Lumen(Sc):
    def construct(self):
        secs, nm = base_row("layers")
        self.add(*secs.values(), *nm.values())
        self.at("small white space")
        rings = [Circle(radius=0.30 * RS * (1 if k != "plan" else 1) + 0.18, color=WHITE_, stroke_width=6).move_to(secs[k].lum.get_center())
                 for k in X3]
        for r, k in zip(rings, X3):
            if k == "plan":
                r.stretch(0.62, 1)
        self.play(*[Create(r) for r in rings], run_time=1.2)
        self.at("gut lumen")
        lab = T("gut lumen (food)", 32, color=WHITE_).move_to([0, -2.85, 0])
        self.play(FadeIn(lab, shift=UP * .1), *[Indicate(r, scale_factor=1.25, color=WHITE_) for r in rings], run_time=1.2)
        self.at("not the body cavity")
        x = T("not the body cavity", 30, color=RED).move_to([0, 3.2, 0])
        self.play(FadeIn(x), run_time=0.6)
        self.at("if there is one")
        self.play(FadeOut(lab), FadeOut(x), *[FadeOut(r) for r in rings], run_time=0.6)
        zr = []
        for k in X3:
            c = DashedVMobject(Circle(radius=0.57 * RS, color=WHITE_, stroke_width=6), num_dashes=24).move_to(secs[k].lum.get_center())
            if k == "plan":
                c.stretch(0.62, 1)
            zr.append(c)
        self.play(*[Create(c) for c in zr], run_time=0.9)
        self.at("between gut and body wall")
        lab2 = T("body cavity?", 32, color=WHITE_).move_to([0, -2.85, 0])
        self.play(FadeIn(lab2, shift=UP * .1), *[Indicate(c, scale_factor=1.12, color=YELLOW) for c in zr], run_time=1.4)
        self.finish()


def row_after_s04():
    secs, nm = base_row("zone", {"earth": "layers"})
    t1 = T("no body cavity", 28, color=ORANGE).move_to([X3["plan"], -2.75, 0])
    t2 = T("pseudocoelom", 30, color=CYAN, weight=BOLD).move_to([0, -2.75, 0])
    return secs, nm, t1, t2


class S04Cavities(Sc):
    def construct(self):
        secs, nm = base_row("layers")
        self.add(*secs.values(), *nm.values())
        self.at("in the planarian")
        sp = secs["plan"]
        self.play(FadeIn(sp.zone), run_time=1.5)
        sp.add(sp.zone)
        self.at("there is no body cavity")
        t1 = T("no body cavity", 28, color=ORANGE).move_to([X3["plan"], -2.75, 0])
        self.play(FadeIn(t1, shift=UP * .1), run_time=0.6)
        self.at("in the nematode")
        sn = secs["nem"]
        self.play(Indicate(sn, scale_factor=1.05, color=WHITE_), run_time=1.0)
        self.at("a fluid space")
        self.play(FadeIn(sn.zone), FadeIn(sn.dots), run_time=1.5)
        sn.add(sn.zone, sn.dots)
        self.at("lined by mesoderm only")
        self.play(Indicate(sn.meso, scale_factor=1.0, color=WHITE_), run_time=1.6)
        self.at("that is a")
        t2 = T("pseudocoelom", 30, color=CYAN, weight=BOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(t2, shift=UP * .1), run_time=0.6)
        self.finish()


class S05Coelom(Sc):
    def construct(self):
        secs, nm, t1, t2 = row_after_s04()
        self.add(*secs.values(), *nm.values(), t1, t2)
        self.at("in the earthworm")
        se = secs["earth"]
        self.play(Indicate(se, scale_factor=1.05, color=WHITE_), run_time=1.0)
        self.at("the fluid space")
        self.play(FadeIn(se.zone), FadeIn(se.dots), run_time=1.5)
        se.add(se.zone, se.dots)
        self.at("on both sides")
        self.play(FadeIn(se.inner), Indicate(se.meso, scale_factor=1.0, color=WHITE_), run_time=1.6)
        se.add(se.inner)
        self.at("that is a true")
        t3 = T("coelom", 32, color=CYAN, weight=BOLD).move_to([X3["earth"], -2.75, 0])
        self.play(FadeIn(t3, shift=UP * .1), run_time=0.6)
        self.at("three worms")
        self.play(*[Indicate(s, scale_factor=1.06, color=WHITE_) for s in secs.values()], run_time=2.0)
        self.finish()


class S06Staircase(Sc):
    def construct(self):
        secs, nm = base_row("full")
        t1 = T("no body cavity", 28, color=ORANGE).move_to([X3["plan"], -2.75, 0])
        t2 = T("pseudocoelom", 30, color=CYAN, weight=BOLD).move_to([0, -2.75, 0])
        t3 = T("coelom", 32, color=CYAN, weight=BOLD).move_to([X3["earth"], -2.75, 0])
        self.add(*secs.values(), *nm.values(), t1, t2, t3)
        self.at("survey of the invertebrates")
        cap = T("Hyman: The Invertebrates", 34, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(t3), FadeIn(cap, shift=DOWN * .1), run_time=0.8)
        self.at("ordered animals this way")
        bl = step_blocks()
        self.play(*[GrowFromEdge(b, DOWN) for b in bl.values()], *[FadeOut(n) for n in nm.values()], run_time=1.6)
        self.at("no cavity")
        for k, key, d_at in (("plan", "no cavity", None), ("nem", "partial lining", None), ("earth", "full lining", None)):
            self.at(key if k != "earth" else "then a full one")
            self.play(secs[k].animate.scale(STEP_SC).move_to(step_pos(k)),
                      FadeIn(step_name(k)), FadeIn(step_desc(k), shift=UP * .1), run_time=1.0)
        self.at("looks like a staircase")
        ar = Arrow([-5.4, -0.2, 0], [3.0, 2.6, 0], color=YELLOW, stroke_width=7, buff=0)
        al = T("simple to complex?", 30, color=YELLOW).move_to([-3.9, 1.75, 0])
        self.play(GrowArrow(ar), FadeIn(al), run_time=1.6)
        self.finish()


class S07Predict(Sc):
    def construct(self):
        bl, secs, nm, ds = stairs_world()
        cap = T("Hyman: The Invertebrates", 34, font=TITLE_FONT).move_to([0, 3.4, 0])
        ar = Arrow([-5.4, -0.2, 0], [3.0, 2.6, 0], color=YELLOW, stroke_width=7, buff=0)
        al = T("simple to complex?", 30, color=YELLOW).move_to([-3.9, 1.75, 0])
        txt = VGroup(*nm.values(), *ds.values())
        self.add(*bl.values(), *secs.values(), txt, cap, ar, al)
        w = question_world()
        dna = dna_strand()
        self.at("now compare genes")
        self.play(FadeOut(cap), FadeOut(ar), FadeOut(al), FadeOut(txt),
                  *[b.animate.set_fill(opacity=0.05) for b in bl.values()], FadeIn(dna), FadeIn(w["gl"]), run_time=1.6)
        self.at("family tree")
        self.play(Indicate(dna, scale_factor=1.03, color=TEAL), run_time=1.4)
        self.at("where should the nematode land")
        self.play(secs["nem"].animate.scale(0.5 / STEP_SC).move_to([0, 1.65, 0]), FadeIn(w["qm"]), run_time=1.6)
        pulse(w["qm"], 0.12, 1.2)
        self.at("between the flatworm")
        self.play(Create(w["rm"]), FadeIn(w["rmt"]), run_time=1.4)
        self.at("somewhere else")
        self.play(Create(w["ro"]), FadeIn(w["rot"]), run_time=1.4)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        w = question_world()
        dna = dna_strand()
        self.add(*w["bl"].values(), w["plan"], w["earth"], w["nem"], w["rm"], w["rmt"], w["ro"], w["rot"], w["gl"], dna)
        qm = w["qm"]
        pulse(qm, 0.12, 1.2)
        self.add(qm)
        ring = Circle(radius=0.42, color=GREY, stroke_width=5).move_to([6.1, -3.2, 0])
        prog = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=max(0.01, TAU * prog.get_value()), color=YELLOW, stroke_width=8).move_to([6.1, -3.2, 0]))
        self.add(ring, arc)
        self.play(prog.animate.set_value(0.0), run_time=4.9, rate_func=linear)
        self.finish()


class S09Ecdysozoa(Sc):
    def construct(self):
        w = question_world()
        dna = dna_strand()
        self.add(*w["bl"].values(), w["plan"], w["earth"], w["nem"], w["rm"], w["rmt"], w["ro"], w["rot"], w["gl"], dna, w["qm"])
        pulse(w["qm"], 0.12, 1.2)
        comb = comb_lines()
        tp = {k: tip(k, COMB_Y[k]) for k in COMB_Y}
        self.at("somewhere else")
        # the staircase redraws as a branching tree
        self.play(*[FadeOut(b) for b in w["bl"].values()], FadeOut(w["rm"]), FadeOut(w["rmt"]), FadeOut(w["ro"]), FadeOut(w["rot"]),
                  FadeOut(w["gl"]), FadeOut(w["qm"]), FadeOut(dna),
                  ReplacementTransform(w["plan"], tp["plan"][0]), ReplacementTransform(w["earth"], tp["earth"][0]),
                  ReplacementTransform(w["nem"], tp["nem"][0]), *[FadeIn(tp[k][1]) for k in tp], Create(comb), run_time=2.0)
        self.at("the genes put the nematode")
        self.play(tp["nem"].animate.shift(RIGHT * 3.6), run_time=0.5)
        self.play(tp["nem"].animate.shift(UP * (TIPY["nem"] - COMB_Y["nem"])), run_time=0.6)
        L9 = t9_lines()
        ar = tip("arth", TIPY["arth"])
        self.at("arthropods")
        self.play(tp["nem"].animate.shift(LEFT * 3.6), FadeOut(comb), tp["earth"].animate.shift(DOWN * (COMB_Y["earth"] - TIPY["earth"])),
                  tp["plan"].animate.shift(DOWN * (COMB_Y["plan"] - TIPY["plan"])), Create(L9["root"]), Create(L9["earth"]), Create(L9["plan"]),
                  Create(L9["ecdy"]), FadeIn(ar, shift=LEFT * .3), run_time=1.6)
        self.at("both shed")
        skin = []
        for y in (TIPY["nem"], TIPY["arth"]):
            skin.append(Line([TIPX + 0.1, y + 0.28, 0], [TIPX + 0.8, y + 0.28, 0], color=CREAM, stroke_width=3))
        mo = T("moulting (ecdysis)", 30, color=CREAM).move_to([4.6, 2.4, 0])
        self.play(FadeIn(mo), *[s.animate.shift(DOWN * 0.5).set_opacity(0) for s in skin], run_time=1.8)
        self.at("names the group")
        lab = T("Ecdysozoa", 36, color=PURPLE, weight=BOLD).move_to([4.6, 2.4, 0])
        self.play(FadeOut(mo), FadeIn(lab), Indicate(L9["ecdy"], scale_factor=1.0, color=PURPLE), run_time=1.2)
        pulse(lab, 0.12, 1.4)
        self.finish()


class S10Spiralia(Sc):
    def construct(self):
        L9, L10 = t9_lines(), t10_lines()
        tp = {k: tip(k, TIPY[k]) for k in ("nem", "arth", "earth", "plan")}
        lab = T("Ecdysozoa", 32, color=PURPLE, weight=BOLD).move_to([4.75, 2.4, 0])
        be, bs, bd = brackets()
        self.add(L9["root"], L9["ecdy"], L9["earth"], L9["plan"], *tp.values(), lab, be)
        pulse(lab, 0.12, 1.4)
        self.at("the planarian moves")
        self.play(FadeOut(L9["plan"]), tp["plan"].animate.shift(RIGHT * 3.2 + UP * 0.5), run_time=1.2)
        self.play(tp["plan"].animate.shift(UP * 0.4), run_time=0.9)
        self.at("lands beside the earthworm")
        sn = tip("snail", TIPY["snail"])
        self.play(FadeOut(L9["earth"]), Create(L10["spir"]), tp["plan"].animate.shift(LEFT * 3.2 + DOWN * 0.9), run_time=1.6)
        self.at("a snail")
        self.play(FadeIn(sn, shift=LEFT * .3), run_time=0.8)
        self.at("group called")
        sp = T("Spiralia", 32, color=GREEN, weight=BOLD).move_to([4.75, -0.4, 0])
        self.play(FadeIn(sp), Create(bs), run_time=1.0)
        self.at("its relatives")
        ur, fi = tip("urch", TIPY["urch"]), tip("fish", TIPY["fish"])
        de = VGroup(T("Deuterostomia", 32, color=GREY, weight=BOLD), T("traditional;", 26, color=GREY),
                    T("support debated", 26, color=GREY)).arrange(DOWN, buff=0.08).move_to([4.75, -3.05, 0])
        self.play(Create(L10["deut"]), FadeIn(ur), FadeIn(fi), FadeIn(de), Create(bd), run_time=1.8)
        self.at("not an early")
        st = T("early, simple branch", 26, color=RED).move_to([4.75, -1.4, 0])
        self.play(FadeIn(st), run_time=0.5)
        strike = Line(st.get_left(), st.get_right(), color=RED, stroke_width=5)
        self.play(Create(strike), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(st), FadeOut(strike), run_time=0.6)
        self.finish()


class S11Scatter(Sc):
    def construct(self):
        d = tree_final(names=True, icons=False, tick=False, labels=True)
        d["names"] = VGroup()
        self.add(d["root"], d["ecdy"], d["spir"], d["deut"], d["tips"], d["labels"])
        self.at("mark each tip")
        icons = [tip_icon(k, TIPY[k]) for k in TIPY]
        anims = [ReplacementTransform(d["tips"][i][0], icons[i]) for i in range(len(TIPY))]
        self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=3.0)
        self.at("the cavity marks are scattered")
        self.play(*[Indicate(ic, scale_factor=1.3, color=WHITE_) for ic in icons], run_time=1.8)
        self.at("the molting mark")
        tk = moult_tick()
        tl = T("moulting", 28, color=PURPLE).move_to([-4.5, 3.15, 0])
        self.play(Create(tk), FadeIn(tl), run_time=1.0)
        self.play(Indicate(tk, scale_factor=1.4, color=WHITE_), run_time=1.2)
        self.finish()


class S12Grade(Sc):
    def construct(self):
        d = tree_final(names=True, icons=True, tick=True, labels=True)
        allt = vgroup_all(d)
        self.add(allt)
        # panels
        pl = RoundedRectangle(corner_radius=0.2, width=6.2, height=4.0, color=GREY, stroke_width=3).move_to([-3.55, 0.3, 0])
        pr = RoundedRectangle(corner_radius=0.2, width=6.2, height=4.0, color=PURPLE, stroke_width=3).move_to([3.55, 0.3, 0])
        self.at("animals that share")
        secs = [Sec(k, R=0.85, stage="full", dots=False).move_to([x, 0.5, 0]) for k, x in zip(("plan", "nem", "earth"), (-5.45, -3.55, -1.65))]
        gt = T("grade", 40, color=GREY, weight=BOLD).move_to([-3.55, 1.85, 0])
        gs = T("same level of organization", 28).move_to([-3.55, -1.0, 0])
        self.play(FadeOut(allt), Create(pl), *[FadeIn(s, scale=0.5) for s in secs], FadeIn(gt), run_time=1.8)
        self.play(FadeIn(gs, shift=UP * .1), run_time=0.8)
        self.at("a clade is something else")
        ct = T("clade", 40, color=PURPLE, weight=BOLD).move_to([3.55, 1.85, 0])
        node = PL((1.4, 0.3), (2.6, 0.3), color=PURPLE)
        f1 = PL((2.6, 0.3), (2.6, 0.95), (4.3, 0.95), color=PURPLE)
        f2 = PL((2.6, 0.3), (2.6, -0.35), (4.3, -0.35), color=PURPLE)
        n1 = T("nematode", 28).move_to([4.45, 0.95, 0], aligned_edge=LEFT)
        n2 = T("arthropod", 28).move_to([4.45, -0.35, 0], aligned_edge=LEFT)
        self.play(Create(pr), FadeIn(ct), Create(node), Create(f1), Create(f2), FadeIn(n1), FadeIn(n2), run_time=2.0)
        self.at("ancestor and all of its descendants")
        base = Circle(radius=0.28, color=WHITE_, stroke_width=6).move_to([1.4, 0.3, 0])
        cs = T("ancestor + all descendants", 28).move_to([3.55, -1.0, 0])
        self.play(Create(base), FadeIn(cs, shift=UP * .1), Indicate(n1, color=PURPLE, scale_factor=1.15),
                  Indicate(n2, color=PURPLE, scale_factor=1.15), run_time=2.0)
        self.finish()


def vgroup_all(d):
    return VGroup(*[v for v in d.values()])


def skeleton(scale=0.7, cx=-4.2, cy=1.0):
    d = tree_final(names=False, icons=True, tick=True, labels=False)
    g = VGroup(d["root"], d["ecdy"], d["spir"], d["deut"], d["tips"], d["tick"])
    g.scale(scale).move_to([cx, cy, 0])
    return g


class S13Rule(Sc):
    def construct(self):
        d = tree_final(names=True, icons=True, tick=True, labels=True)
        # carried from the end of film's tree: rebuild as the skeleton, small and to the left
        card = RoundedRectangle(corner_radius=0.2, width=7.4, height=4.5, color=GREY, stroke_width=3).move_to([3.0, 0.95, 0])
        h1 = T("one origin on a tree", 30, weight=BOLD).move_to([3.0, 2.65, 0])
        h2 = T("built from other evidence?", 30, weight=BOLD).move_to([3.0, 2.15, 0])
        self.at("a shared derived")
        sk = skeleton()
        self.play(FadeIn(sk), Create(card), FadeIn(h1), FadeIn(h2), run_time=2.0)
        self.at("it is a new state")
        node = Dot(radius=0.14, color=PURPLE).move_to(sk[0].get_center()) if False else None
        tk = sk[5]
        self.play(Indicate(tk, scale_factor=1.6, color=WHITE_), run_time=1.6)
        self.at("molting fits one origin")
        r1 = T("moulting", 32, color=PURPLE, weight=BOLD).move_to([0.9, 1.1, 0], aligned_edge=LEFT)
        ck = check(5.6, 1.1)
        self.play(FadeIn(r1), Create(ck), run_time=1.0)
        self.play(Indicate(sk[1], scale_factor=1.0, color=PURPLE), run_time=1.6)
        self.at("cavity type changes")
        r2 = T("cavity type", 32, weight=BOLD).move_to([0.9, -0.05, 0], aligned_edge=LEFT)
        cx = crossmark(5.6, -0.05)
        self.play(FadeIn(r2), Create(cx), run_time=1.0)
        self.play(*[Indicate(ic, scale_factor=1.5, color=WHITE_) for ic in sk[4]], run_time=1.8)
        self.at("to test any character")
        slab = RoundedRectangle(corner_radius=0.15, width=4.8, height=1.3, color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.12).move_to([-4.2, -2.55, 0])
        dna = dna_strand(-6.0, -2.4, -2.3, 12, 26)
        feats = VGroup(*[Sec(k, R=0.22, stage="full", dots=False).move_to([x, -2.95, 0]) for k, x in zip(("plan", "nem", "earth", "earth"), (-5.4, -4.6, -3.8, -3.0))])
        found = VGroup(slab, dna, feats).shift(DOWN * 1.2)
        self.add(found)
        self.play(found.animate.shift(UP * 1.2), run_time=2.2)
        self.at("many genes are one such source")
        ev = VGroup(T("other evidence:", 30, color=TEAL, weight=BOLD), T("many genes, many body features", 28, color=TEAL)).arrange(DOWN, buff=0.12).move_to([3.0, -2.45, 0])
        self.play(FadeIn(ev, shift=UP * .1), Indicate(dna, scale_factor=1.05, color=TEAL), run_time=1.6)
        self.finish()


class S14Close(Sc):
    def construct(self):
        div = Line([0, 3.5, 0], [0, -3.5, 0], color=GREY, stroke_width=3)
        self.add(div)
        self.at("a body plan")
        secs = [Sec(k, R=1.0, stage="full").move_to([x, 0.1, 0]) for k, x in zip(("plan", "nem", "earth"), (-5.4, -3.4, -1.4))]
        self.play(*[FadeIn(s, scale=0.6) for s in secs], run_time=1.0)
        self.at("describes")
        d1 = T("describes", 40, weight=BOLD).move_to([-3.4, 2.4, 0])
        self.play(FadeIn(d1, shift=DOWN * .1), run_time=0.8)
        self.at("independent evidence")
        sk = skeleton(0.56, 3.4, -0.15)
        dna = dna_strand(1.0, 5.8, -2.6, 16, 28)
        self.play(FadeIn(sk), FadeIn(dna), run_time=1.0)
        self.at("tests whom")
        d2 = T("tests ancestry", 40, color=TEAL, weight=BOLD).move_to([3.4, 3.2, 0])
        self.play(FadeIn(d2, shift=DOWN * .1), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "A body plan describes an animal; independent evidence tests its ancestry."
